#!/usr/bin/env python3
"""Reproduce the Census 2022 robustness checks reported in the article.

SUPERSEDED. This script allocates radio population to barrios in proportion to
intersection area, which assumes population is spread evenly across a radio.
dasymmetric_allocation.py replaces that with allocation by footprint share, and
is the project's primary method.

This file is retained deliberately. Its assertions pin the published sweep, so
it remains a regression guard on the historical numbers and keeps the article's
figures verifiable. The coverage gradient it reports, 2.62 down to 1.88, is
largely an artefact of the areal assumption: under dasymmetric allocation the
same sweep on the same filter is flat near 1.9.

The publication calculation starts from settlement-level footprint counts and
INDEC census-radio aggregates. It does not treat footprints as population
observations: the population side remains conditional on an explicit
persons-per-footprint multiplier.

Frozen mode expects two files from the forthcoming submission-version Zenodo
deposit. Until that version is published, pass the recovered inputs explicitly:

    pixi run census-comparison -- \
      --settlements-path /path/to/barrios-hilbert.parquet \
      --census-path /path/to/radios-hilbert.parquet

Live mode downloads the processed census-radio file from Source Cooperative.
It is useful for rebuilding the comparison, but it is not the exact frozen
publication path because the upstream object can change.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import duckdb
import requests

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs" / "census-comparison"

CENSUS_PATH = DATA_DIR / "census_2022_radios.parquet"
SETTLEMENTS_PATH = DATA_DIR / "census_settlement_counts.parquet"
CENSUS_LIVE_URL = (
    "https://data.source.coop/nlebovits/censo-argentino/2022/radios.parquet"
)

# This is intentionally unset until the author publishes a new version of the
# data deposit containing both files. A concept DOI must not be substituted.
CENSUS_ZENODO_RECORD_ID = "REPLACE_WITH_VERSION_RECORD_ID"
ZENODO_API = "https://zenodo.org/api/records"

# Recovered inputs used for Paper II and its validation report.
EXPECTED_SHA256 = {
    "census_2022_radios.parquet": (
        "ade36a340854bf3e616ff28f34527ba193aa515274c503929877f831276a4936"
    ),
    "census_settlement_counts.parquet": (
        "a90503b0ef3ad5e9359cb93fba7363cf7bb872ecbb9be84fc446ea40da5ac012"
    ),
}

THRESHOLDS = (0.0, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95)
MULTIPLIERS = (2.80, 3.12, 3.35)

EXPECTED_SWEEP = {
    0.0: (6467, 1_969_975, 2_518_282, 2.62),
    0.10: (3566, 1_681_066, 2_352_845, 2.39),
    0.25: (2151, 1_364_480, 2_010_840, 2.27),
    0.50: (1089, 959_971, 1_479_959, 2.17),
    0.75: (544, 607_405, 990_041, 2.06),
    0.90: (304, 405_682, 687_672, 1.98),
    0.95: (223, 305_226, 542_938, 1.88),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    with requests.get(url, stream=True, timeout=300) as response:
        response.raise_for_status()
        with temporary.open("wb") as stream:
            for block in response.iter_content(8 * 1024 * 1024):
                if block:
                    stream.write(block)
    temporary.replace(destination)


def download_zenodo_inputs() -> None:
    if CENSUS_ZENODO_RECORD_ID.startswith("REPLACE_"):
        raise RuntimeError(
            "The Census inputs are not in Zenodo record 22656880. Publish the "
            "prepared new dataset version, set CENSUS_ZENODO_RECORD_ID to its "
            "version-specific record id, or pass --census-path and "
            "--settlements-path."
        )
    response = requests.get(f"{ZENODO_API}/{CENSUS_ZENODO_RECORD_ID}", timeout=60)
    response.raise_for_status()
    entries = {item["key"]: item for item in response.json().get("files", [])}
    for name, destination in (
        ("census_2022_radios.parquet", CENSUS_PATH),
        ("census_settlement_counts.parquet", SETTLEMENTS_PATH),
    ):
        if name not in entries:
            raise RuntimeError(f"Zenodo record has no {name}")
        expected_md5 = entries[name]["checksum"].split(":", 1)[1]
        if destination.exists():
            actual_md5 = hashlib.md5(destination.read_bytes()).hexdigest()
            if actual_md5 == expected_md5:
                continue
        download(entries[name]["links"]["self"], destination)
        actual_md5 = hashlib.md5(destination.read_bytes()).hexdigest()
        if actual_md5 != expected_md5:
            destination.unlink()
            raise RuntimeError(f"Checksum failure for {name}")


def prepare_inputs(args: argparse.Namespace) -> tuple[Path, Path]:
    census = args.census_path or CENSUS_PATH
    settlements = args.settlements_path or SETTLEMENTS_PATH
    if args.source == "live" and not census.exists():
        download(CENSUS_LIVE_URL, census)
    elif args.source == "zenodo" and not (census.exists() and settlements.exists()):
        download_zenodo_inputs()

    for path in (census, settlements):
        if not path.exists():
            raise FileNotFoundError(path)
    if not args.allow_changed_inputs:
        for path, archive_name in (
            (census, "census_2022_radios.parquet"),
            (settlements, "census_settlement_counts.parquet"),
        ):
            actual = sha256(path)
            expected = EXPECTED_SHA256[archive_name]
            if actual != expected:
                raise RuntimeError(
                    f"{path} has sha256 {actual}; expected {expected}. "
                    "Use --allow-changed-inputs only for an explicitly nonpublication run."
                )
    return census, settlements


def quote(path: Path) -> str:
    return str(path.resolve()).replace("'", "''")


def run_analysis(census: Path, settlements: Path) -> dict[str, list[dict]]:
    con = duckdb.connect()
    con.execute("INSTALL spatial; LOAD spatial;")
    census_sql = quote(census)
    settlements_sql = quote(settlements)

    con.execute(f"""
        CREATE TEMP TABLE tracts AS
        SELECT * FROM '{census_sql}';
        CREATE TEMP TABLE barrios AS
        SELECT
            id_renabap,
            provincia,
            renabap_families,
            building_count,
            geometry
        FROM '{settlements_sql}';
    """)

    input_totals = con.execute("""
        SELECT
            (SELECT COUNT(*) FROM tracts),
            (SELECT SUM(POB_TOT_P) FROM tracts),
            (SELECT SUM(VIV_TOT_P) FROM tracts),
            (SELECT COUNT(*) FROM barrios),
            (SELECT SUM(building_count) FROM barrios)
    """).fetchone()
    if input_totals != (66_502, 45_618_784, 17_783_028, 6_467, 1_969_975):
        raise RuntimeError(f"Unexpected publication input totals: {input_totals}")

    con.execute("""
        CREATE TEMP TABLE tract_coverage AS
        SELECT
            r.COD_2022,
            MAX(r.PROV) AS provincia,
            MAX(r.POB_TOT_P) AS census_population,
            MAX(r.VIV_TOT_P) AS census_private_dwellings,
            ST_Area_Spheroid(MAX(r.geometry)) AS tract_area,
            SUM(ST_Area_Spheroid(ST_Intersection(r.geometry, b.geometry)))
                AS barrio_area_in_tract
        FROM tracts r
        JOIN barrios b ON ST_Intersects(r.geometry, b.geometry)
        GROUP BY r.COD_2022;

        CREATE TEMP TABLE allocation_detail AS
        SELECT
            b.id_renabap,
            b.provincia,
            b.renabap_families,
            b.building_count,
            ST_Area_Spheroid(b.geometry) AS barrio_area,
            r.COD_2022,
            r.POB_TOT_P,
            r.VIV_TOT_P,
            ST_Area_Spheroid(r.geometry) AS tract_area,
            ST_Area_Spheroid(ST_Intersection(b.geometry, r.geometry))
                AS intersection_area,
            tc.barrio_area_in_tract / NULLIF(tc.tract_area, 0)
                AS tract_coverage
        FROM barrios b
        JOIN tracts r ON ST_Intersects(b.geometry, r.geometry)
        JOIN tract_coverage tc USING (COD_2022)
        WHERE ST_Area_Spheroid(ST_Intersection(b.geometry, r.geometry)) > 0;
    """)

    values = ",".join(f"({threshold})" for threshold in THRESHOLDS)
    sweep = (
        con.execute(f"""
        WITH barrio_aggregates AS (
            SELECT
                threshold,
                id_renabap,
                MAX(building_count) AS buildings,
                SUM(POB_TOT_P * intersection_area / NULLIF(tract_area, 0))
                    AS census_population,
                SUM(intersection_area) / MAX(barrio_area)
                    AS retained_barrio_fraction
            FROM allocation_detail
            CROSS JOIN (VALUES {values}) thresholds(threshold)
            WHERE tract_coverage >= threshold
            GROUP BY threshold, id_renabap
        )
        SELECT
            threshold,
            COUNT(*) AS barrios,
            SUM(buildings) AS buildings,
            ROUND(SUM(census_population))::BIGINT AS census_population,
            ROUND(SUM(buildings) * 3.35)::BIGINT AS footprint_population,
            ROUND(SUM(buildings) * 3.35 / SUM(census_population), 2)
                AS ratio
        FROM barrio_aggregates
        WHERE retained_barrio_fraction >= 0.5
        GROUP BY threshold
        ORDER BY threshold
    """)
        .fetchdf()
        .to_dict("records")
    )

    occupancy = (
        con.execute("""
        SELECT 'National' AS scope, COUNT(*) AS tracts,
            SUM(POB_TOT_P)::BIGINT AS population,
            SUM(VIV_TOT_P)::BIGINT AS private_dwellings,
            ROUND(SUM(POB_TOT_P)::DOUBLE / SUM(VIV_TOT_P), 2) AS persons_per_dwelling
        FROM tracts
        UNION ALL
        SELECT 'All barrio-intersecting', COUNT(*),
            SUM(census_population)::BIGINT,
            SUM(census_private_dwellings)::BIGINT,
            ROUND(SUM(census_population)::DOUBLE / SUM(census_private_dwellings), 2)
        FROM tract_coverage
        UNION ALL
        SELECT 'Coverage >= ' || CAST(ROUND(threshold * 100) AS INTEGER) || '%',
            COUNT(*), SUM(census_population)::BIGINT,
            SUM(census_private_dwellings)::BIGINT,
            ROUND(SUM(census_population)::DOUBLE / SUM(census_private_dwellings), 2)
        FROM tract_coverage
        CROSS JOIN (VALUES (0.10),(0.25),(0.50),(0.75),(0.90),(0.95)) t(threshold)
        WHERE barrio_area_in_tract / NULLIF(tract_area, 0) >= threshold
        GROUP BY threshold
        ORDER BY scope
    """)
        .fetchdf()
        .to_dict("records")
    )

    selected = next(row for row in sweep if float(row["threshold"]) == 0.75)
    multiplier_sensitivity = [
        {
            "multiplier": multiplier,
            "buildings": selected["buildings"],
            "census_population": selected["census_population"],
            "footprint_population": round(selected["buildings"] * multiplier),
            "ratio": round(
                selected["buildings"] * multiplier / selected["census_population"],
                2,
            ),
        }
        for multiplier in MULTIPLIERS
    ]

    join_checks = (
        con.execute("""
        WITH pairs AS (
            SELECT id_renabap, COD_2022, COUNT(*) AS occurrences,
                ST_Area_Spheroid(ST_Intersection(b.geometry, r.geometry)) AS overlap,
                ST_Area_Spheroid(b.geometry) AS barrio_area,
                ST_Area_Spheroid(r.geometry) AS tract_area
            FROM barrios b
            JOIN tracts r ON ST_Intersects(b.geometry, r.geometry)
            GROUP BY id_renabap, COD_2022, b.geometry, r.geometry
        )
        SELECT
            SUM(CASE WHEN occurrences > 1 THEN 1 ELSE 0 END)::BIGINT
                AS duplicate_pairs,
            SUM(CASE WHEN overlap < barrio_area AND overlap < tract_area
                     THEN 1 ELSE 0 END)::BIGINT AS partial_overlaps
        FROM pairs
    """)
        .fetchdf()
        .to_dict("records")
    )
    con.close()
    return {
        "coverage_sweep": sweep,
        "occupancy_diagnostics": occupancy,
        "multiplier_sensitivity": multiplier_sensitivity,
        "join_checks": join_checks,
    }


def verify(results: dict[str, list[dict]]) -> None:
    failures: list[str] = []
    for row in results["coverage_sweep"]:
        threshold = float(row["threshold"])
        expected = EXPECTED_SWEEP[threshold]
        actual = (
            int(row["barrios"]),
            int(row["buildings"]),
            int(row["census_population"]),
            float(row["ratio"]),
        )
        if actual != expected:
            failures.append(f"coverage {threshold}: {actual} != {expected}")
    expected_sensitivity = {2.80: 1.72, 3.12: 1.91, 3.35: 2.06}
    for row in results["multiplier_sensitivity"]:
        if float(row["ratio"]) != expected_sensitivity[float(row["multiplier"])]:
            failures.append(f"multiplier result differs: {row}")
    if failures:
        raise RuntimeError("Publication checks failed:\n" + "\n".join(failures))


def write_outputs(
    results: dict[str, list[dict]], census: Path, settlements: Path
) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {
        "census_input": {"path": str(census), "sha256": sha256(census)},
        "settlement_input": {
            "path": str(settlements),
            "sha256": sha256(settlements),
        },
    }
    (OUTPUT_DIR / "input_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    for name, rows in results.items():
        destination = OUTPUT_DIR / f"{name}.csv"
        with destination.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    lines = [
        "# Census 2022 robustness outputs",
        "",
        "## Coverage sweep",
        "",
        "| Minimum tract coverage | Barrios | Buildings | Census population | Footprint population (×3.35) | Ratio |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in results["coverage_sweep"]:
        lines.append(
            f"| {float(row['threshold']):.0%} | {int(row['barrios']):,} | "
            f"{int(row['buildings']):,} | {int(row['census_population']):,} | "
            f"{int(row['footprint_population']):,} | {float(row['ratio']):.2f} |"
        )
    lines.extend(
        [
            "",
            "The adjacent-tract values in the recovered validation report are not "
            "generated here because its exact distance-classification query was not "
            "preserved. See `paper/supplement.md` and `REPRODUCIBILITY.md`.",
            "",
        ]
    )
    (OUTPUT_DIR / "summary.md").write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=("zenodo", "live"), default="zenodo")
    parser.add_argument("--census-path", type=Path)
    parser.add_argument("--settlements-path", type=Path)
    parser.add_argument("--allow-changed-inputs", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    census, settlements = prepare_inputs(args)
    results = run_analysis(census, settlements)
    verify(results)
    write_outputs(results, census, settlements)
    print(f"Verified publication results and wrote {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
