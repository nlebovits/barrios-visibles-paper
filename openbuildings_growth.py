#!/usr/bin/env python3
"""Estimate post-Census construction from Google Open Buildings Temporal.

This script measures change, not level. Open Buildings Temporal runs one model
over uniform annual Sentinel-2 stacks, so a ratio between two of its own years
is meaningful. Its absolute counts are not comparable with Census dwellings or
with VIDA footprints, and no such comparison is made here. Only the growth
rates leave this script.

Method:

1. Take the radios that census_dwelling_footprint.py already selected: RENABAP
   coverage at or above 95 percent, horizontal regime, outside CABA.
2. Sum the `building_fractional_count` band over each radio for 2021, 2022 and
   2023. Google documents this band as the source for deriving a building count
   over an area.
3. Form the 2021 to 2022 and 2022 to 2023 growth rates per radio.
4. Aggregate over the same radios, weighting by the current VIDA footprint
   count, so that a radio contributes in proportion to the footprints whose
   dating is in question.
5. Carry the 2022 to 2023 rate forward to the VIDA snapshot date and report how
   much of the observed footprint-to-dwelling ratio construction could explain.

Dates. Each annual layer is inferred at 30 June. Census Day is 18 May 2022, six
weeks before the 2022 layer. The VIDA snapshot is September 2024, which is 26
months after the 2022 layer and about 15 months after the last available layer.

    pixi run openbuildings-growth -- --census-path /path/to/radios.parquet

The script asserts the published selection before it writes anything, so a
changed upstream input fails loudly rather than silently moving the result.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
import rasterio
import requests
from rasterio.features import geometry_mask
from rasterio.warp import transform_geom
from rasterio.windows import Window, from_bounds

from census_dwelling_footprint import (
    OUTPUT_DIR as ANALYSIS_DIR,
)
from census_dwelling_footprint import (
    PRIMARY_THRESHOLD,
)

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
CACHE_DIR = DATA_DIR / "ob-temporal-manifests"
OUTPUT_DIR = ROOT / "outputs" / "openbuildings-growth"

BUCKET = "https://storage.googleapis.com/open-buildings-temporal-data"
LIST_API = "https://storage.googleapis.com/storage/v1/b/open-buildings-temporal-data/o"
BAND = 1  # building_fractional_count, per the ingestion manifests
NODATA = -99.0

YEARS = (2021, 2022, 2023)
# Argentina spans UTM zones 18S to 21S.
EPSG_CODES = (32718, 32719, 32720, 32721)

INFERENCE_DAY = "06-30"
CENSUS_DAY = pd.Timestamp("2022-05-18")
VIDA_DATE = pd.Timestamp("2024-09-15")

# Publication values. The selection comes from census_dwelling_footprint.py, so
# these pin both scripts to the same radio set. The usable 2022 to 2023 set is
# the subset with valid imagery in both years.
EXPECTED_TARGET_RADIOS = 460
EXPECTED_2022_2023 = {"n_radios": 356, "vida_footprints": 200_094}
LAYER_2022 = pd.Timestamp("2022-06-30")
LAYER_2023 = pd.Timestamp("2023-06-30")


def manifest_names() -> list[str]:
    """Every manifest for the Argentine UTM zones and the wanted years."""
    names: list[str] = []
    token = None
    while True:
        params = {
            "prefix": "v1/manifests/",
            "maxResults": "1000",
            "fields": "items(name),nextPageToken",
        }
        if token:
            params["pageToken"] = token
        page = requests.get(LIST_API, params=params, timeout=120).json()
        names.extend(item["name"] for item in page.get("items", []))
        token = page.get("nextPageToken")
        if not token:
            break
    wanted = [
        name
        for name in names
        if any(f"EPSG_{code}_" in name for code in EPSG_CODES)
        and any(f"_{year}_{INFERENCE_DAY.replace('-', '_')}" in name for year in YEARS)
    ]
    return sorted(wanted)


def build_tile_index() -> pd.DataFrame:
    """One row per GeoTIFF, with its UTM extent, from the ingestion manifests.

    Each manifest lists its sources with an affine transform and a pixel size,
    which gives the exact extent without opening any raster.
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    index_path = CACHE_DIR / "tile_index.parquet"
    if index_path.exists():
        return pd.read_parquet(index_path)

    rows: list[dict] = []
    names = manifest_names()
    print(f"Reading {len(names)} ingestion manifests")
    for position, name in enumerate(names, start=1):
        cached = CACHE_DIR / name.rsplit("/", 1)[-1]
        if not cached.exists():
            response = requests.get(f"{BUCKET}/{name}", timeout=300)
            response.raise_for_status()
            cached.write_bytes(response.content)
        manifest = json.loads(cached.read_text())
        prefix = manifest["uriPrefix"].replace("gs://open-buildings-temporal-data/", "")
        epsg = int(name.split("EPSG_")[1][:5])
        year = int(name.rsplit("_", 3)[1])
        for tileset in manifest["tilesets"]:
            for source in tileset["sources"]:
                affine = source["affineTransform"]
                size = source["dimensions"]
                scale = affine["scaleX"]
                xmin = affine["translateX"]
                ymax = affine["translateY"]
                rows.append(
                    {
                        "path": prefix + source["uris"][0],
                        "epsg": epsg,
                        "year": year,
                        "xmin": xmin,
                        "ymin": ymax - size["height"] * scale,
                        "xmax": xmin + size["width"] * scale,
                        "ymax": ymax,
                    }
                )
        if position % 10 == 0 or position == len(names):
            print(f"  [{position}/{len(names)}] {len(rows):,} tiles")
    index = pd.DataFrame(rows)
    index.to_parquet(index_path, index=False)
    return index


def target_radios(census_path: Path) -> pd.DataFrame:
    """The radios the main analysis already selected, with their geometry.

    The strata are not recomputed here. They are read from the per-radio output
    of census_dwelling_footprint.py, so the two analyses cannot drift apart.
    """
    per_radio = ANALYSIS_DIR / "census_dwelling_footprint_by_radio.parquet"
    if not per_radio.exists():
        raise FileNotFoundError(
            f"{per_radio} is missing. Run census_dwelling_footprint.py first."
        )
    frame = pd.read_parquet(per_radio)
    selected = frame[
        (frame["coverage_union"] >= PRIMARY_THRESHOLD)
        & frame["horizontal_regime"]
        & ~frame["is_caba"]
        & (frame["redatam_flag"] == "SI")
    ].copy()

    con = duckdb.connect()
    con.execute("INSTALL spatial; LOAD spatial;")
    geometry = con.execute(f"""
        SELECT COD_2022, ST_AsGeoJSON(geometry) AS geojson,
               ST_XMin(geometry) AS lon_min, ST_YMin(geometry) AS lat_min,
               ST_XMax(geometry) AS lon_max, ST_YMax(geometry) AS lat_max
        FROM '{str(census_path.resolve()).replace("'", "''")}'
    """).df()
    con.close()
    merged = selected.merge(geometry, on="COD_2022", how="left")
    if merged["geojson"].isna().any():
        raise RuntimeError("Some selected radios have no geometry")
    return merged


def utm_epsg(lon: float, lat: float) -> int:
    zone = int((lon + 180) // 6) + 1
    return (32700 if lat < 0 else 32600) + zone


def tiles_for(index: pd.DataFrame, epsg: int, year: int, bounds: tuple) -> pd.DataFrame:
    xmin, ymin, xmax, ymax = bounds
    candidates = index[(index["epsg"] == epsg) & (index["year"] == year)]
    return candidates[
        (candidates["xmin"] < xmax)
        & (candidates["xmax"] > xmin)
        & (candidates["ymin"] < ymax)
        & (candidates["ymax"] > ymin)
    ]


def _tile_sum(
    path: str, geometry: dict, bounds: tuple, exclude: list[tuple]
) -> tuple[float, int]:
    """Sum the fractional-count band inside one polygon, within one tile.

    Tiles overlap: 12.5 km squares laid on a grid that repeats across S2 cell
    boundaries, so 186 of the target radios fall in more than one tile. Summing
    them naively would count the overlap twice. `exclude` carries the extents of
    the tiles already read for this radio, and any pixel whose centre falls in
    one of them is dropped here.

    Nodata is excluded rather than treated as zero, so a radio that falls partly
    outside the imagery shows up as a pixel-count shortfall instead of a silent
    undercount.
    """
    url = f"/vsicurl/{BUCKET}/{path}"
    with rasterio.open(url) as src:
        window = from_bounds(*bounds, transform=src.transform)
        window = window.round_offsets().round_lengths()
        window = Window(
            max(0, int(window.col_off)),
            max(0, int(window.row_off)),
            int(window.width),
            int(window.height),
        )
        window = window.intersection(Window(0, 0, src.width, src.height))
        if window.width <= 0 or window.height <= 0:
            return 0.0, 0
        data = src.read(BAND, window=window)
        transform = src.window_transform(window)
        mask = geometry_mask(
            [geometry], out_shape=data.shape, transform=transform, invert=True
        )
    if exclude:
        columns = transform.c + (np.arange(data.shape[1]) + 0.5) * transform.a
        rows = transform.f + (np.arange(data.shape[0]) + 0.5) * transform.e
        for xmin, ymin, xmax, ymax in exclude:
            inside_x = (columns >= xmin) & (columns < xmax)
            inside_y = (rows >= ymin) & (rows < ymax)
            mask &= ~(inside_y[:, None] & inside_x[None, :])
    valid = mask & (data != NODATA) & np.isfinite(data)
    return float(data[valid].sum()), int(valid.sum())


def sum_year(
    index: pd.DataFrame, epsg: int, year: int, geometry: dict, bounds: tuple
) -> tuple[float, int, int]:
    """Sum one radio for one year across every tile it touches, once each.

    A tile that fully contains the radio is read first, so the common case
    finishes after one read and needs no exclusion arithmetic.
    """
    tiles = tiles_for(index, epsg, year, bounds)
    if tiles.empty:
        return 0.0, 0, 0
    contains = (
        (tiles["xmin"] <= bounds[0])
        & (tiles["xmax"] >= bounds[2])
        & (tiles["ymin"] <= bounds[1])
        & (tiles["ymax"] >= bounds[3])
    )
    ordered = pd.concat([tiles[contains], tiles[~contains]])
    total, pixels, used = 0.0, 0, []
    for tile in ordered.itertuples():
        one, count = _tile_sum(tile.path, geometry, bounds, used)
        total += one
        pixels += count
        used.append((tile.xmin, tile.ymin, tile.xmax, tile.ymax))
        if contains.any():
            break
    return total, pixels, len(used)


def _radio_record(row, index: pd.DataFrame) -> dict:
    lon = (row.lon_min + row.lon_max) / 2
    lat = (row.lat_min + row.lat_max) / 2
    epsg = utm_epsg(lon, lat)
    projected = transform_geom("EPSG:4326", f"EPSG:{epsg}", json.loads(row.geojson))
    coordinates = np.array(
        [point for ring in projected["coordinates"] for point in _ring(ring)]
    )
    bounds = (
        coordinates[:, 0].min(),
        coordinates[:, 1].min(),
        coordinates[:, 0].max(),
        coordinates[:, 1].max(),
    )
    record = {"COD_2022": row.COD_2022, "epsg": epsg}
    for year in YEARS:
        total, pixels, tiles = sum_year(index, epsg, year, projected, bounds)
        record[f"count_{year}"] = total
        record[f"pixels_{year}"] = pixels
        record[f"tiles_{year}"] = tiles
    return record


def extract(radios: pd.DataFrame, index: pd.DataFrame, workers: int) -> pd.DataFrame:
    from concurrent.futures import ThreadPoolExecutor, as_completed

    records: list[dict] = []
    started = time.time()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [
            pool.submit(_radio_record, row, index) for row in radios.itertuples()
        ]
        for position, future in enumerate(as_completed(futures), start=1):
            records.append(future.result())
            if position % 25 == 0 or position == len(futures):
                rate = (time.time() - started) / position
                print(
                    f"  [{position}/{len(futures)}] {rate:.2f}s per radio, "
                    f"{rate * (len(futures) - position) / 60:.0f} min left"
                )
    return pd.DataFrame(records)


def _ring(ring):
    """Yield coordinate pairs from a polygon or multipolygon ring."""
    if ring and isinstance(ring[0][0], (int, float)):
        return ring
    return [point for part in ring for point in _ring(part)]


MIN_PIXEL_COVERAGE = 0.9


def growth(counts: pd.DataFrame, radios: pd.DataFrame) -> pd.DataFrame:
    """Per-radio growth, with years of missing imagery excluded.

    A tile can exist for a year and still carry no valid data over a given
    radio. That returns a sum of zero, which is missing imagery rather than an
    absence of buildings, and treating it as a real count produces a spurious
    -100 percent. A year is therefore used only when its valid-pixel count
    reaches 90 percent of the best-covered year for that radio.
    """
    frame = radios.merge(counts, on="COD_2022", how="inner")
    pixels = frame[[f"pixels_{year}" for year in YEARS]]
    reference = pixels.max(axis=1)
    for year in YEARS:
        frame[f"valid_{year}"] = (reference > 0) & (
            frame[f"pixels_{year}"] >= MIN_PIXEL_COVERAGE * reference
        )
    for early, late in ((2021, 2022), (2022, 2023)):
        usable = (
            frame[f"valid_{early}"]
            & frame[f"valid_{late}"]
            & (frame[f"count_{early}"] > 0)
        )
        frame[f"usable_{early}_{late}"] = usable
        frame[f"growth_{early}_{late}"] = np.where(
            usable, frame[f"count_{late}"] / frame[f"count_{early}"] - 1, np.nan
        )
    frame["weight"] = frame["vida_footprints_all"]
    return frame


def _weighted(values: pd.Series, weights: pd.Series) -> float | None:
    usable = values.notna() & weights.notna() & (weights > 0)
    if not usable.any():
        return None
    return float((values[usable] * weights[usable]).sum() / weights[usable].sum())


def _quantiles(values: pd.Series, weights: pd.Series) -> dict:
    usable = values.notna() & weights.notna() & (weights > 0)
    if not usable.any():
        return {}
    order = values[usable].sort_values()
    cumulative = weights[order.index].cumsum() / weights[usable].sum()
    result = {}
    for level in (0.10, 0.25, 0.50, 0.75, 0.90):
        position = cumulative.searchsorted(level)
        position = min(position, len(order) - 1)
        result[level] = float(order.iloc[position])
    return result


def summarise(frame: pd.DataFrame) -> dict:
    summary = {
        "n_radios_extracted": int(len(frame)),
        "n_radios_dropped_for_imagery": int(
            (~frame["usable_2022_2023"] | ~frame["usable_2021_2022"]).sum()
        ),
    }
    for early, late in ((2021, 2022), (2022, 2023)):
        column = f"growth_{early}_{late}"
        usable = frame[frame[f"usable_{early}_{late}"]]
        values, weights = usable[column], usable["weight"]
        summary[f"{column}_n_radios"] = int(len(usable))
        summary[f"{column}_totals"] = (
            usable[f"count_{late}"].sum() / usable[f"count_{early}"].sum() - 1
            if usable[f"count_{early}"].sum()
            else None
        )
        summary[f"{column}_weighted_mean"] = _weighted(values, weights)
        summary[f"{column}_median_unweighted"] = float(values.median())
        for level, value in _quantiles(values, weights).items():
            summary[f"{column}_weighted_p{int(level * 100)}"] = value
        summary[f"{column}_radios_with_growth"] = int((values > 0).sum())
        summary[f"{column}_radios_with_decline"] = int((values < 0).sum())
        summary[f"{column}_vida_footprints"] = int(usable["vida_footprints_all"].sum())
        summary[f"{column}_occupied_dwellings"] = int(
            usable["dwellings_occupied_broad"].sum()
        )
        summary[f"{column}_households"] = int(usable["households"].sum())
    # The attribution uses the 2022 to 2023 subset, so the Census and VIDA
    # totals quoted alongside it must come from those same radios.
    summary["n_radios"] = summary["growth_2022_2023_n_radios"]
    summary["vida_footprints"] = summary["growth_2022_2023_vida_footprints"]
    summary["occupied_dwellings"] = summary["growth_2022_2023_occupied_dwellings"]
    summary["households"] = summary["growth_2022_2023_households"]
    return summary


def attribute(summary: dict) -> dict:
    """How much of the observed footprint-to-dwelling ratio construction could
    explain, if the measured rate held to the VIDA snapshot date.

    Only the Open Buildings growth rate is used. Its absolute counts never
    touch the Census or VIDA totals.
    """
    observed = summary["vida_footprints"] / summary["occupied_dwellings"]
    span = (VIDA_DATE - CENSUS_DAY).days / 365.25
    result = {
        "observed_vida_ratio": observed,
        "years_census_to_vida": span,
        "extrapolated_months_beyond_2023_layer": (VIDA_DATE - LAYER_2023).days / 30.44,
    }
    for label, rate in (
        ("central", summary["growth_2022_2023_totals"]),
        ("weighted_mean", summary["growth_2022_2023_weighted_mean"]),
        ("earlier_period", summary["growth_2021_2022_totals"]),
        ("upper_p90", summary["growth_2022_2023_weighted_p90"]),
    ):
        if rate is None:
            continue
        factor = (1 + rate) ** span
        adjusted = observed / factor
        result[f"{label}_annual_rate"] = rate
        result[f"{label}_growth_factor"] = factor
        result[f"{label}_ratio_at_census_date"] = adjusted
        result[f"{label}_share_of_excess_explained"] = (
            (observed - adjusted) / (observed - 1) if observed > 1 else None
        )
    return result


def make_plots(frame: pd.DataFrame, summary: dict) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(figsize=(7.0, 5.0))
    for column, colour, label in (
        ("growth_2021_2022", "#8e8e8e", "2021 to 2022"),
        ("growth_2022_2023", "#1f4e79", "2022 to 2023"),
    ):
        values = frame[column].dropna()
        weights = frame.loc[values.index, "weight"]
        axes.hist(
            values.clip(-0.3, 0.5),
            bins=60,
            weights=weights,
            histtype="step",
            linewidth=1.6,
            color=colour,
            label=f"{label} (weighted mean {summary[f'{column}_weighted_mean']:.1%})",
        )
    axes.axvline(0, color="black", linestyle="--", linewidth=1)
    axes.set_xlabel("Annual growth in Open Buildings fractional count")
    axes.set_ylabel("VIDA footprints in radios at this growth rate")
    axes.set_title(
        f"Building growth in {summary['n_radios']:,} horizontal non-CABA radios "
        f"with >={PRIMARY_THRESHOLD:.0%} RENABAP coverage"
    )
    axes.legend(fontsize=8)
    axes.grid(True, alpha=0.25)
    figure.tight_layout()
    figure.savefig(OUTPUT_DIR / "fig_growth_distribution.png", dpi=160)
    plt.close(figure)

    figure, axes = plt.subplots(figsize=(7.0, 5.0))
    values = frame["growth_2022_2023"].dropna()
    weights = frame.loc[values.index, "weight"]
    order = values.sort_values()
    cumulative = weights[order.index].cumsum() / weights[order.index].sum()
    axes.plot(order.values, cumulative.values, color="#1f4e79", linewidth=1.8)
    axes.axvline(0, color="black", linestyle="--", linewidth=1)
    axes.axvline(
        summary["growth_2022_2023_totals"],
        color="#c0392b",
        linestyle=":",
        linewidth=1.5,
        label=f"totals rate {summary['growth_2022_2023_totals']:.1%}",
    )
    axes.set_xlim(-0.2, 0.4)
    axes.set_xlabel("Annual growth, 2022 to 2023")
    axes.set_ylabel("Cumulative share of VIDA footprints")
    axes.set_title("Footprint-weighted distribution of building growth")
    axes.legend(fontsize=8)
    axes.grid(True, alpha=0.25)
    figure.tight_layout()
    figure.savefig(OUTPUT_DIR / "fig_growth_cumulative.png", dpi=160)
    plt.close(figure)


def write_report(summary: dict, attribution: dict, frame: pd.DataFrame) -> None:
    central = attribution["central_share_of_excess_explained"]
    lines = [
        "# Post-Census construction from Open Buildings Temporal",
        "",
        "This analysis uses Open Buildings Temporal for change only. Its absolute",
        "counts are never compared with Census dwellings or with VIDA footprints.",
        "One model runs over uniform annual Sentinel-2 stacks, so a ratio between",
        "two of its own years is meaningful even though its levels are not",
        "comparable with a footprint inventory.",
        "",
        "## Scope",
        "",
        f"The dwelling analysis selected {summary['n_radios_extracted']:,} radios:",
        f"RENABAP coverage at or above {PRIMARY_THRESHOLD:.0%}, horizontal regime,",
        "outside CABA.",
        "",
        "Open Buildings does not cover every year everywhere. A tile can exist",
        "for a year and still carry no valid data over a given radio, which",
        "returns a sum of zero. That is missing imagery, not an absence of",
        "buildings, and counting it would produce a spurious fall of 100",
        "percent. A year is used only when its valid-pixel count reaches",
        f"{MIN_PIXEL_COVERAGE:.0%} of the best-covered year for that radio.",
        f"That drops {summary['n_radios_dropped_for_imagery']:,} radios from at",
        "least one comparison.",
        "",
        f"The {summary['n_radios']:,} radios usable for 2022 to 2023 hold "
        f"{summary['vida_footprints']:,} VIDA footprints, "
        f"{summary['occupied_dwellings']:,} occupied private dwellings, and "
        f"{summary['households']:,} households. Those are the radios the",
        "attribution below uses.",
        "",
        "Each annual layer is inferred at 30 June. Census Day is 18 May 2022, six",
        "weeks before the 2022 layer. The VIDA snapshot is September 2024, which",
        f"is {attribution['extrapolated_months_beyond_2023_layer']:.0f} months",
        "after the last available layer.",
        "",
        "## Measured growth",
        "",
        "| Period | Radios | Totals | Weighted mean | Weighted median | "
        "Weighted p25 to p75 |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for early, late in ((2021, 2022), (2022, 2023)):
        key = f"growth_{early}_{late}"
        lines.append(
            f"| {early} to {late} | {summary[f'{key}_n_radios']:,} | "
            f"{summary[f'{key}_totals']:.1%} | "
            f"{summary[f'{key}_weighted_mean']:.1%} | "
            f"{summary[f'{key}_weighted_p50']:.1%} | "
            f"{summary[f'{key}_weighted_p25']:.1%} to "
            f"{summary[f'{key}_weighted_p75']:.1%} |"
        )
    lines += [
        "",
        "Weights are the current VIDA footprint count, so a radio counts in",
        "proportion to the footprints whose dating is in question.",
        "",
        "| Period | Radios growing | Radios declining |",
        "| --- | ---: | ---: |",
        *[
            f"| {early} to {late} | "
            f"{summary[f'growth_{early}_{late}_radios_with_growth']:,} | "
            f"{summary[f'growth_{early}_{late}_radios_with_decline']:,} |"
            for early, late in ((2021, 2022), (2022, 2023))
        ],
        "",
        "## How much construction could explain",
        "",
        "The observed footprint-to-dwelling ratio in these radios is "
        f"{attribution['observed_vida_ratio']:.2f}. Carrying each growth rate",
        f"forward over the {attribution['years_census_to_vida']:.2f} years from",
        "Census Day to the VIDA snapshot gives the ratio that would have held at",
        "Census Day, and therefore the share of the excess above parity that",
        "construction could account for.",
        "",
        "| Rate used | Annual rate | Growth factor | Ratio at Census Day | "
        "Share of excess explained |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for label, name in (
        ("central", "2022 to 2023 totals"),
        ("weighted_mean", "2022 to 2023 weighted mean"),
        ("earlier_period", "2021 to 2022 totals"),
        ("upper_p90", "2022 to 2023 weighted p90"),
    ):
        if f"{label}_annual_rate" not in attribution:
            continue
        lines.append(
            f"| {name} | {attribution[f'{label}_annual_rate']:.1%} | "
            f"{attribution[f'{label}_growth_factor']:.3f} | "
            f"{attribution[f'{label}_ratio_at_census_date']:.2f} | "
            f"{attribution[f'{label}_share_of_excess_explained']:.1%} |"
        )
    lines += [
        "",
        "On the central rate, construction after Census Day accounts for",
        f"{central:.0%} of the excess above one footprint per occupied dwelling.",
        "The p90 row is deliberately generous: it applies to every radio the rate",
        "that only the fastest-growing tenth reached.",
        "",
        "## Limits",
        "",
        "- Radios without full imagery coverage in both years of a comparison",
        "  are excluded rather than counted as zero. The excluded set is not",
        "  random, because imagery gaps follow cloud and orbit patterns.",
        "- The last layer is 2023, so the final "
        f"{attribution['extrapolated_months_beyond_2023_layer']:.0f} months to the",
        "  VIDA snapshot are extrapolated at the measured rate rather than",
        "  observed.",
        "- The effective resolution is about 4 m, so adjacent small structures",
        "  merge. That biases the level, which is not used here. It biases the",
        "  growth rate only if the merging changed between years.",
        "- Google documents year-to-year spatial jitter and temporal instability.",
        "  Aggregating over a whole radio and over hundreds of radios reduces it",
        "  but does not remove it.",
        "- A growth rate in fractional building count is not a growth rate in",
        "  dwellings. A new structure in an existing plot counts here.",
        "- This says nothing about national census omission.",
        "",
        "## Provenance",
        "",
        "`GOOGLE/Research/open-buildings-temporal/v1`, band",
        "`building_fractional_count`, read from",
        "`gs://open-buildings-temporal-data/v1/geotiffs/`. Tile extents come from",
        "the ingestion manifests under `v1/manifests/`, cached in",
        "`data/ob-temporal-manifests/`. Pixels equal to the nodata value of -99",
        "are excluded rather than counted as zero.",
        "",
    ]
    (OUTPUT_DIR / "report.md").write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--census-path", type=Path, required=True)
    parser.add_argument("--limit", type=int, help="Process only the first N radios")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--skip-plots", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    radios = target_radios(args.census_path)
    if args.limit:
        radios = radios.head(args.limit)
    elif len(radios) != EXPECTED_TARGET_RADIOS:
        raise RuntimeError(
            f"Selected {len(radios):,} radios, and the publication run selected "
            f"{EXPECTED_TARGET_RADIOS:,}. The per-radio input has changed."
        )
    print(f"Target radios: {len(radios):,}")

    index = build_tile_index()
    print(f"Tile index: {len(index):,} tiles across {index['epsg'].nunique()} zones")

    cache = OUTPUT_DIR / "openbuildings_raw_counts.parquet"
    if cache.exists() and not args.refresh:
        counts = pd.read_parquet(cache)
        counts = counts[counts["COD_2022"].isin(radios["COD_2022"])]
        print(f"Reusing cached counts for {len(counts):,} radios ({cache.name})")
    else:
        counts = extract(radios, index, args.workers)
        counts.to_parquet(cache, index=False)
    frame = growth(counts, radios)
    summary = summarise(frame)
    if not args.limit:
        observed = {k: int(summary[k]) for k in EXPECTED_2022_2023}
        if observed != EXPECTED_2022_2023:
            raise RuntimeError(
                f"Usable 2022 to 2023 set is {observed}, and the publication "
                f"run had {EXPECTED_2022_2023}."
            )
    attribution = attribute(summary)

    columns = [
        "COD_2022",
        "provincia",
        "departamento",
        "coverage_union",
        "pct_departamento",
        "vida_footprints_all",
        "dwellings_all",
        "dwellings_occupied_broad",
        "households",
        "epsg",
        *[f"count_{year}" for year in YEARS],
        *[f"pixels_{year}" for year in YEARS],
        *[f"tiles_{year}" for year in YEARS],
        "growth_2021_2022",
        "growth_2022_2023",
        "weight",
    ]
    frame[columns].to_parquet(
        OUTPUT_DIR / "openbuildings_growth_by_radio.parquet", index=False
    )
    pd.DataFrame([summary]).to_csv(
        OUTPUT_DIR / "openbuildings_growth_summary.csv", index=False
    )
    (OUTPUT_DIR / "attribution.json").write_text(
        json.dumps(attribution, indent=2) + "\n", encoding="utf-8"
    )
    write_report(summary, attribution, frame)
    if not args.skip_plots:
        make_plots(frame, summary)
    print(f"Wrote {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
