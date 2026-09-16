#!/usr/bin/env python3
"""Download the pre-Census Microsoft building footprints for the eligible radios.

The analysis in census_dwelling_footprint.py counts VIDA footprints from a
September 2024 snapshot against Census counts from May 2022. This script fetches
a building inventory whose imagery ends before Census Day, so that a second
count can exclude post-Census construction by provenance rather than by
argument.

Provenance. Microsoft's own copies of the 2022 releases are gone. Both 2022
link tables survive in the git history of microsoft/GlobalMLBuildingFootprints,
at commits 4d0848095f (2022-07-13) and 5e2bf4d8d3 (2022-10-12), and every URL
in them points at minedbuildings.blob.core.windows.net, which now answers
"409 Public access is not permitted on this storage account". The project README
gives the reason: "Older versions will not be moved."

The Planetary Computer copy survives, and it keeps the 2022 releases. Two
Argentina releases are fetched here.

    2022-06-14  released 27 days after Census Day, one partition for the whole
                country, 22 parts, geometry only
    2023-04-25  partitioned by Bing level-9 quadkey, carries meanHeight

Both declare imagery from 2014-04-15 to 2021-06-06. That end date is eleven
months before Census Day, so neither inventory can contain a building
constructed after the Census.

The 2022 release is not spatially partitioned, so all of Argentina is fetched.
The 2023 release is, so only the quadkeys that intersect an eligible radio are.
Files are cached and skipped on a rerun when their sha256 already matches.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
import urllib.parse
from pathlib import Path

import requests

from census_dwelling_footprint import (
    MASTER_THRESHOLD,
    build_coverage,
    connect,
    load_geometry,
)

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

REGION = "Argentina"

# The 2022 release predates spatial partitioning, so its whole-country
# partition is fetched. The 2023 release is quadkey-partitioned.
RELEASES = {
    "2022-06-14": f"global/2022-06-14/ml-buildings.parquet/RegionName={REGION}",
    "2023-04-25": f"delta/2023-04-25/ml-buildings.parquet/RegionName={REGION}",
}
PARTITIONED = {"2023-04-25"}

STAC_SEARCH = "https://planetarycomputer.microsoft.com/api/stac/v1/search"
SAS_URL = (
    "https://planetarycomputer.microsoft.com/api/sas/v1/token/"
    "bingmlbuildings/footprints"
)
BLOB_ROOT = "https://bingmlbuildings.blob.core.windows.net/footprints"

# Declared by every Argentina item in the collection. Checked, not assumed.
EXPECTED_IMAGERY = ("2014-04-15T00:00:00+00:00", "2021-06-06T00:00:00+00:00")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class Sas:
    """A Planetary Computer SAS token. It expired after about an hour in
    testing, so refresh it rather than carrying one across a long download."""

    def __init__(self) -> None:
        self._token = ""
        self._fetched = 0.0

    def get(self, force: bool = False) -> str:
        if force or not self._token or time.time() - self._fetched > 1800:
            response = requests.get(SAS_URL, timeout=60)
            response.raise_for_status()
            self._token = response.json()["token"]
            self._fetched = time.time()
        return self._token


def eligible_bboxes(census: Path, settlements: Path, temp_dir: Path) -> list[tuple]:
    con = connect(temp_dir)
    load_geometry(con, {"census": census, "settlements": settlements})
    build_coverage(con)
    rows = con.execute("""
        SELECT ST_XMin(geometry), ST_YMin(geometry),
               ST_XMax(geometry), ST_YMax(geometry)
        FROM eligible
    """).fetchall()
    con.close()
    return rows


def argentina_items() -> list[dict]:
    """Every Argentina item, with its quadkey and declared imagery range.

    The msbuildings:quadkey property is null on some items, so the quadkey is
    read from the item id, which has the form Argentina_<quadkey>_<date>.
    """
    body = {
        "collections": ["ms-buildings"],
        "query": {"msbuildings:region": {"eq": REGION}},
        "limit": 100,
    }
    items: list[dict] = []
    token = None
    while True:
        payload = dict(body)
        if token:
            payload["token"] = token
        response = requests.post(STAC_SEARCH, json=payload, timeout=120)
        response.raise_for_status()
        page = response.json()
        for feature in page.get("features", []):
            properties = feature["properties"]
            match = re.match(rf"{REGION}_(\d+)_", feature["id"])
            quadkey = match.group(1) if match else None
            if quadkey is None:
                href = feature["assets"]["data"]["href"]
                quadkey = href.rsplit("quadkey=", 1)[-1]
            items.append(
                {
                    "id": feature["id"],
                    "quadkey": quadkey,
                    "bbox": feature["bbox"],
                    "start_datetime": properties.get("start_datetime"),
                    "end_datetime": properties.get("end_datetime"),
                }
            )
        following = [
            link for link in page.get("links", []) if link.get("rel") == "next"
        ]
        if not following:
            break
        token = following[0]["body"]["token"]
    return items


def overlaps(item_bbox: list[float], boxes: list[tuple]) -> bool:
    xmin, ymin, xmax, ymax = item_bbox[0], item_bbox[1], item_bbox[2], item_bbox[3]
    return any(
        xmin <= bxmax and xmax >= bxmin and ymin <= bymax and ymax >= bymin
        for bxmin, bymin, bxmax, bymax in boxes
    )


def list_blobs(prefix: str, sas: Sas) -> list[str]:
    for attempt in (0, 1):
        url = (
            "https://bingmlbuildings.blob.core.windows.net/footprints"
            f"?restype=container&comp=list&prefix={urllib.parse.quote(prefix)}"
            f"&{sas.get(force=bool(attempt))}"
        )
        response = requests.get(url, timeout=120)
        if response.status_code == 403 and attempt == 0:
            continue
        response.raise_for_status()
        return [
            name
            for name in re.findall(r"<Name>([^<]+)</Name>", response.text)
            if name.endswith(".parquet")
        ]
    return []


def download_blob(name: str, destination: Path, sas: Sas) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    for attempt in (0, 1):
        url = f"{BLOB_ROOT}/{urllib.parse.quote(name)}?{sas.get(force=bool(attempt))}"
        with requests.get(url, stream=True, timeout=600) as response:
            if response.status_code == 403 and attempt == 0:
                continue
            response.raise_for_status()
            with temporary.open("wb") as stream:
                for block in response.iter_content(8 * 1024 * 1024):
                    if block:
                        stream.write(block)
        temporary.replace(destination)
        return


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--census-path", type=Path, required=True)
    parser.add_argument("--settlements-path", type=Path, required=True)
    parser.add_argument("--temp-dir", type=Path, default=Path("/tmp/duckdb-bv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    boxes = eligible_bboxes(args.census_path, args.settlements_path, args.temp_dir)
    print(f"Eligible radios at >={MASTER_THRESHOLD:.0%} coverage: {len(boxes):,}")

    items = argentina_items()
    print(f"{REGION} items in the collection: {len(items)}")
    ranges = {(item["start_datetime"], item["end_datetime"]) for item in items}
    if ranges != {EXPECTED_IMAGERY}:
        raise RuntimeError(
            f"Declared imagery range changed: {sorted(ranges)}. "
            f"Expected only {EXPECTED_IMAGERY}."
        )

    sas = Sas()
    for release, prefix in RELEASES.items():
        directory = DATA_DIR / f"ms-buildings-{release}"
        directory.mkdir(parents=True, exist_ok=True)

        if release in PARTITIONED:
            quadkeys = [
                item["quadkey"]
                for item in items
                if item["quadkey"].isdigit() and overlaps(item["bbox"], boxes)
            ]
            prefixes = [f"{prefix}/quadkey={quadkey}/" for quadkey in quadkeys]
            print(f"{release}: {len(prefixes)} of {len(items)} quadkeys intersect")
        else:
            prefixes = [f"{prefix}/"]
            print(f"{release}: one whole-country partition")

        files: list[dict] = []
        for index, one in enumerate(prefixes, start=1):
            for name in list_blobs(one, sas):
                destination = directory / name.rsplit("/", 1)[-1]
                if not destination.exists():
                    download_blob(name, destination, sas)
                files.append(
                    {
                        "blob": name,
                        "file": destination.name,
                        "bytes": destination.stat().st_size,
                        "sha256": sha256(destination),
                    }
                )
            if index % 10 == 0 or index == len(prefixes):
                print(f"  [{index}/{len(prefixes)}] {len(files)} file(s) so far")

        manifest = {
            "collection": "ms-buildings",
            "release": release,
            "region": REGION,
            "prefix": prefix,
            "spatially_partitioned": release in PARTITIONED,
            "imagery_start": EXPECTED_IMAGERY[0],
            "imagery_end": EXPECTED_IMAGERY[1],
            "census_day": "2022-05-18",
            "files": files,
            "total_bytes": sum(entry["bytes"] for entry in files),
        }
        (directory / "manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )
        print(
            f"{release}: wrote {len(files)} file(s), "
            f"{manifest['total_bytes'] / 1e9:.2f} GB, to {directory}"
        )


if __name__ == "__main__":
    main()
