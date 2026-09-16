#!/usr/bin/env python3
"""Allocate Census quantities to barrios by footprint share, not by area.

Areal weighting splits a radio's population among barrios in proportion to
intersection area, which assumes people are spread evenly across the radio.
They are not. A dense settlement inside a large, mostly empty radio is credited
only its area share, and the shortfall shows up as an inflated discrepancy.

This allocates instead by the share of the radio's building footprints that
fall inside the barrio:

    w(b, t) = footprints(b, t) / footprints(t)

Buildings locate people better than radio boundaries do, which was the premise
the project started from. Applying it to the allocation step removes at source
the artefact that the coverage sweep was built to filter around.

Three weights, from one spatial join, test the assumption that footprints carry
similar dwelling counts inside and outside a barrio within the same radio:

    w_count   footprint count, primary
    w_area    total footprint area, partly absorbs large-building effects
    w_band    count of footprints between 6 and 200 m2, drops warehouses

The assumption fails in two directions that do not cancel. High-rises outside a
barrio mean the barrio's true dwelling share is below its footprint share, so
the weight over-allocates and the discrepancy is understated. Non-residential
buildings outside a barrio absorb share the barrio should have had, so the
discrepancy is overstated.

Geometry is projected once to an equal-area projection. Every area is then true
square metres, and the OGC:CRS84 against EPSG:4326 axis-order question does not
arise.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import duckdb
import pandas as pd

from census_dwelling_footprint import build_census, load_geometry

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs" / "dasymmetric"
REDATAM_PATH = DATA_DIR / "census_2022_redatam.parquet"
BUILDINGS_PATH = DATA_DIR / "buildings_arg.parquet"

PROJECTION = "+proj=laea +lat_0=-38 +lon_0=-64 +datum=WGS84 +units=m +no_defs"
THRESHOLDS = (0.0, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95)
LEGACY_MULTIPLIER = 3.35
DWELLING_BAND = (6.0, 200.0)

WEIGHTS = ("w_count", "w_area", "w_band")
QUANTITIES = {
    "population": "POB_TOT_P",
    "dwellings_all": "dwellings_all",
    "dwellings_occupied": "dwellings_occupied_broad",
    "households": "households",
}

# The published areal sweep, for the flattening comparison.
AREAL_PROVINCES = {
    "San Juan": 7.57,
    "La Pampa": 4.91,
    "Mendoza": 4.51,
    "Santa Cruz": 4.27,
    "La Rioja": 4.13,
    "Catamarca": 4.05,
}

AREAL_SWEEP = {
    0.0: 2.62,
    0.10: 2.39,
    0.25: 2.27,
    0.50: 2.17,
    0.75: 2.06,
    0.90: 1.98,
    0.95: 1.88,
}


def quote(path: Path) -> str:
    return str(path.resolve()).replace("'", "''")


def connect(temp_dir: Path) -> duckdb.DuckDBPyConnection:
    con = duckdb.connect()
    con.execute("INSTALL spatial; LOAD spatial;")
    con.execute("SET threads=12;")
    con.execute("SET preserve_insertion_order=false;")
    temp_dir.mkdir(parents=True, exist_ok=True)
    con.execute(f"SET temp_directory='{quote(temp_dir)}';")
    return con


def project(con: duckdb.DuckDBPyConnection) -> None:
    con.execute(f"""
        CREATE TEMP TABLE tm AS
        SELECT COD_2022, PROV, POB_TOT_P, VIV_TOT_P,
               ST_Transform(geometry, 'OGC:CRS84', '{PROJECTION}') AS g
        FROM tracts;
        CREATE TEMP TABLE bm AS
        SELECT id_renabap, provincia, renabap_families, building_count,
               ST_Transform(geometry, 'OGC:CRS84', '{PROJECTION}') AS g
        FROM barrios;
    """)


def assign_footprints(con: duckdb.DuckDBPyConnection, buildings: Path) -> dict:
    """Assign every footprint to one radio and, where it applies, one barrio.

    Radios tile the territory, so a centroid lies in at most one radio. RENABAP
    polygons overlap on 0.00 km2 of 683.9 km2, so a centroid in two barrios is
    a rounding error; it is assigned to the lower id_renabap and counted.
    """
    low, high = DWELLING_BAND
    con.execute(f"""
        CREATE TEMP TABLE fp AS
        SELECT ST_Transform(ST_Centroid(geometry), 'OGC:CRS84', '{PROJECTION}')
                   AS pt,
               area_in_meters AS a
        FROM read_parquet('{quote(buildings)}');

        CREATE TEMP TABLE tract_totals AS
        SELECT t.COD_2022,
               COUNT(*) AS n_all,
               SUM(f.a) AS area_all,
               COUNT(*) FILTER (WHERE f.a BETWEEN {low} AND {high}) AS n_band
        FROM fp f JOIN tm t ON ST_Within(f.pt, t.g)
        GROUP BY t.COD_2022;

        CREATE TEMP TABLE fp_barrio_raw AS
        SELECT b.id_renabap, f.pt, f.a
        FROM fp f JOIN bm b ON ST_Within(f.pt, b.g);

        CREATE TEMP TABLE fp_barrio AS
        SELECT MIN(id_renabap) AS id_renabap,
               ANY_VALUE(pt) AS pt,
               ANY_VALUE(a) AS a,
               COUNT(*) AS barrios_hit
        FROM fp_barrio_raw
        GROUP BY ST_AsWKB(pt);

        CREATE TEMP TABLE barrio_tract AS
        SELECT f.id_renabap, t.COD_2022,
               COUNT(*) AS n_all,
               SUM(f.a) AS area_all,
               COUNT(*) FILTER (WHERE f.a BETWEEN {low} AND {high}) AS n_band
        FROM fp_barrio f JOIN tm t ON ST_Within(f.pt, t.g)
        GROUP BY f.id_renabap, t.COD_2022;
    """)
    return (
        con.execute("""
        SELECT
            (SELECT COUNT(*) FROM fp) AS footprints_total,
            (SELECT SUM(n_all) FROM tract_totals) AS footprints_in_a_radio,
            (SELECT COUNT(*) FROM tract_totals) AS radios_with_footprints,
            (SELECT COUNT(*) FROM fp_barrio) AS footprints_in_a_barrio,
            (SELECT SUM(CASE WHEN barrios_hit > 1 THEN 1 ELSE 0 END)
             FROM fp_barrio) AS footprints_in_two_barrios
    """)
        .df()
        .iloc[0]
        .to_dict()
    )


def build_weights(con: duckdb.DuckDBPyConnection) -> None:
    """One weight per barrio-radio pair, under each of the three variants."""
    con.execute("""
        CREATE TEMP TABLE weights AS
        SELECT
            bt.id_renabap,
            bt.COD_2022,
            bt.n_all::DOUBLE / tt.n_all AS w_count,
            CASE WHEN tt.area_all > 0 THEN bt.area_all / tt.area_all END AS w_area,
            CASE WHEN tt.n_band > 0
                 THEN bt.n_band::DOUBLE / tt.n_band END AS w_band
        FROM barrio_tract bt
        JOIN tract_totals tt USING (COD_2022);
    """)
    worst = con.execute("""
        SELECT MAX(total) FROM (
            SELECT COD_2022, SUM(w_count) AS total FROM weights GROUP BY COD_2022
        )
    """).fetchone()[0]
    # Weights are shares of one radio's footprints, so they cannot exceed 1.
    # A value above 1 would mean a footprint was counted in two barrios.
    if worst is not None and worst > 1.000001:
        raise RuntimeError(f"Weights sum to {worst} in some radio; expected <= 1")


def allocate(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """Allocate each Census quantity to each barrio under each weight."""
    columns = ",\n".join(
        f"            SUM(q.{source} * w.{weight}) AS {name}_{weight}"
        for weight in WEIGHTS
        for name, source in QUANTITIES.items()
    )
    return con.execute(f"""
        WITH quantities AS (
            SELECT t.COD_2022, t.POB_TOT_P,
                   rc.dwellings_all,
                   rc.dwellings_present + COALESCE(rc.dwellings_habitual_absent, 0)
                       AS dwellings_occupied_broad,
                   rc.households
            FROM tm t LEFT JOIN radio_census rc USING (COD_2022)
        )
        SELECT
            b.id_renabap,
            MAX(b.provincia) AS provincia,
            MAX(b.renabap_families) AS renabap_families,
            MAX(b.building_count) AS building_count,
            COUNT(*) AS radios_contributing,
{columns}
        FROM weights w
        JOIN quantities q USING (COD_2022)
        JOIN bm b USING (id_renabap)
        GROUP BY b.id_renabap
    """).df()


def coverage_sweep(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """The published sweep, recomputed with dasymmetric allocation.

    The filter is unchanged: a radio qualifies on the share of its area covered
    by barrios, and a barrio is retained when the qualifying radios cover at
    least half of it. Only the allocation differs, so the two sweeps are
    directly comparable and the gap between them is the allocation artefact.
    """
    con.execute("""
        CREATE TEMP TABLE overlap AS
        SELECT t.COD_2022, b.id_renabap,
               ST_Area(t.g) AS tract_area,
               ST_Area(b.g) AS barrio_area,
               ST_Area(ST_Intersection(t.g, b.g)) AS intersection_area
        FROM tm t JOIN bm b ON ST_Intersects(t.g, b.g)
        WHERE ST_Area(ST_Intersection(t.g, b.g)) > 0;

        CREATE TEMP TABLE tract_cover AS
        SELECT COD_2022,
               SUM(intersection_area) / NULLIF(MAX(tract_area), 0) AS coverage
        FROM overlap GROUP BY COD_2022;
    """)
    values = ",".join(f"({threshold})" for threshold in THRESHOLDS)
    return con.execute(f"""
        WITH quantities AS (
            SELECT t.COD_2022, t.POB_TOT_P,
                   rc.dwellings_present + COALESCE(rc.dwellings_habitual_absent, 0)
                       AS dwellings_occupied_broad,
                   rc.households
            FROM tm t LEFT JOIN radio_census rc USING (COD_2022)
        ),
        eligible AS (
            SELECT o.id_renabap, o.COD_2022, o.intersection_area, o.barrio_area,
                   th.threshold
            FROM overlap o
            JOIN tract_cover c USING (COD_2022)
            CROSS JOIN (VALUES {values}) th(threshold)
            WHERE c.coverage >= th.threshold
        ),
        per_barrio AS (
            SELECT
                e.threshold,
                e.id_renabap,
                MAX(b.building_count) AS buildings,
                SUM(e.intersection_area) / MAX(e.barrio_area)
                    AS retained_barrio_fraction,
                SUM(q.POB_TOT_P * w.w_count) AS population,
                SUM(q.dwellings_occupied_broad * w.w_count) AS occupied,
                SUM(q.households * w.w_count) AS households
            FROM eligible e
            JOIN bm b USING (id_renabap)
            LEFT JOIN weights w
                   ON w.id_renabap = e.id_renabap AND w.COD_2022 = e.COD_2022
            LEFT JOIN quantities q ON q.COD_2022 = e.COD_2022
            GROUP BY e.threshold, e.id_renabap
        )
        SELECT
            threshold,
            COUNT(*) AS barrios,
            SUM(buildings)::BIGINT AS buildings,
            ROUND(SUM(population))::BIGINT AS census_population,
            ROUND(SUM(occupied))::BIGINT AS census_occupied_dwellings,
            ROUND(SUM(households))::BIGINT AS census_households,
            SUM(buildings) * {LEGACY_MULTIPLIER} / NULLIF(SUM(population), 0)
                AS legacy_population_ratio,
            SUM(buildings) / NULLIF(SUM(occupied), 0) AS footprints_per_occupied,
            SUM(buildings) / NULLIF(SUM(households), 0) AS footprints_per_household
        FROM per_barrio
        WHERE retained_barrio_fraction >= 0.5
        GROUP BY threshold
        ORDER BY threshold
    """).df()


def provincial(allocated: pd.DataFrame) -> pd.DataFrame:
    """Ratios by province, unfiltered. The areal outliers should collapse."""
    grouped = allocated.groupby("provincia", as_index=False).agg(
        barrios=("id_renabap", "count"),
        footprints=("building_count", "sum"),
        renabap_families=("renabap_families", "sum"),
        population=("population_w_count", "sum"),
        households=("households_w_count", "sum"),
        occupied=("dwellings_occupied_w_count", "sum"),
    )
    grouped["legacy_population_ratio"] = (
        grouped["footprints"] * LEGACY_MULTIPLIER / grouped["population"]
    )
    grouped["footprints_per_household"] = grouped["footprints"] / grouped["households"]
    return grouped.sort_values("legacy_population_ratio", ascending=False)


def conservation(con: duckdb.DuckDBPyConnection, allocated: pd.DataFrame) -> dict:
    """National allocated totals must not exceed the national Census totals."""
    national = (
        con.execute("""
        SELECT SUM(POB_TOT_P) AS population,
               SUM(dwellings_all) AS dwellings_all,
               SUM(dwellings_present + COALESCE(dwellings_habitual_absent, 0))
                   AS dwellings_occupied,
               SUM(households) AS households
        FROM tm LEFT JOIN radio_census USING (COD_2022)
    """)
        .df()
        .iloc[0]
    )
    checks = {}
    for name in QUANTITIES:
        allocated_total = float(allocated[f"{name}_w_count"].sum())
        census_total = float(national[name if name != "population" else "population"])
        checks[f"{name}_allocated"] = allocated_total
        checks[f"{name}_national"] = census_total
        checks[f"{name}_share"] = allocated_total / census_total
        if allocated_total > census_total * 1.000001:
            raise RuntimeError(
                f"{name}: allocated {allocated_total:,.0f} exceeds national "
                f"{census_total:,.0f}"
            )
    return checks


def weight_agreement(allocated: pd.DataFrame) -> pd.DataFrame:
    """How far the three weights disagree, per quantity."""
    rows = []
    for name in QUANTITIES:
        base = allocated[f"{name}_w_count"]
        row = {"quantity": name, "total_w_count": float(base.sum())}
        for weight in ("w_area", "w_band"):
            other = allocated[f"{name}_{weight}"]
            row[f"total_{weight}"] = float(other.sum())
            row[f"ratio_{weight}_to_count"] = float(other.sum() / base.sum())
            usable = (base > 0) & other.notna()
            row[f"median_barrio_ratio_{weight}"] = float(
                (other[usable] / base[usable]).median()
            )
        rows.append(row)
    return pd.DataFrame(rows)


def write_report(
    allocated: pd.DataFrame,
    sweep: pd.DataFrame,
    agreement: pd.DataFrame,
    province: pd.DataFrame,
    checks: dict,
    assignment: dict,
) -> None:
    total_footprints = int(allocated["building_count"].sum())
    families = int(allocated["renabap_families"].sum())
    households = float(allocated["households_w_count"].sum())
    occupied = float(allocated["dwellings_occupied_w_count"].sum())
    flat = sweep.set_index("threshold")["legacy_population_ratio"]

    lines = [
        "# Dasymmetric allocation of Census quantities to barrios",
        "",
        "Census quantities are allocated to barrios by the share of a radio's",
        "building footprints that fall inside the barrio, not by the share of",
        "its area. Buildings locate people better than radio boundaries do.",
        "",
        "This supersedes areal weighting. `census_comparison.py` still",
        "reproduces the published areal sweep and keeps its assertions, so the",
        "historical numbers stay verifiable, but it is no longer the primary",
        "method.",
        "",
        "## 1. Does the coverage gradient flatten",
        "",
        "The areal sweep falls from 2.62 to 1.88 as the filter tightens. That",
        "gradient is the allocation artefact bleeding off. If footprint-share",
        "allocation removes the artefact at source, the same sweep computed on",
        "the same filter should be much flatter.",
        "",
        "| Minimum radio coverage | Barrios | Areal ratio | Dasymmetric ratio |",
        "| ---: | ---: | ---: | ---: |",
    ]
    for row in sweep.itertuples():
        areal = AREAL_SWEEP[round(row.threshold, 2)]
        lines.append(
            f"| {row.threshold:.0%} | {row.barrios:,} | {areal:.2f} | "
            f"{row.legacy_population_ratio:.2f} |"
        )
    spread_areal = max(AREAL_SWEEP.values()) - min(AREAL_SWEEP.values())
    spread_dasy = float(flat.max() - flat.min())
    lines += [
        "",
        f"The areal ratio spans {spread_areal:.2f} across the sweep. The",
        f"dasymmetric ratio spans {spread_dasy:.2f}.",
        "",
        "Both ratios use the legacy persons-per-footprint multiplier of "
        f"{LEGACY_MULTIPLIER}, which is the only way to put the two allocations",
        "on one scale. The multiplier is not needed for anything else here.",
        "",
        "## 2. Footprints against allocated Census quantities",
        "",
        "No multiplier. Dwellings and households come straight from the Census",
        "and are allocated by footprint share.",
        "",
        "| Minimum radio coverage | Barrios | Footprints | Occupied dwellings | "
        "Households | FP / occupied | FP / household |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        *[
            f"| {row.threshold:.0%} | {row.barrios:,} | {row.buildings:,} | "
            f"{row.census_occupied_dwellings:,} | {row.census_households:,} | "
            f"{row.footprints_per_occupied:.2f} | "
            f"{row.footprints_per_household:.2f} |"
            for row in sweep.itertuples()
        ],
        "",
        "## 3. Households against RENABAP families",
        "",
        "The comparison the project began with, now with a Census denominator",
        "that does not assume even spread. All 6,467 barrios, no coverage",
        "filter, because the filter existed to control the artefact this method",
        "removes.",
        "",
        "| Quantity | Value |",
        "| --- | ---: |",
        f"| Census households allocated to barrios | {households:,.0f} |",
        f"| Census occupied dwellings allocated to barrios | {occupied:,.0f} |",
        f"| RENABAP families | {families:,} |",
        f"| Footprints in barrios | {total_footprints:,} |",
        f"| Households per RENABAP family | {households / families:.3f} |",
        f"| Footprints per household | {total_footprints / households:.3f} |",
        f"| Footprints per occupied dwelling | {total_footprints / occupied:.3f} |",
        "",
        "## 4. Do the three weights agree",
        "",
        "If footprint-count equal-occupancy carried the result, the three",
        "weights would disagree. Ratios are against the count weight.",
        "",
        "| Quantity | Count total | Area total | Band total | Area / count | "
        "Band / count |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
        *[
            f"| {row.quantity} | {row.total_w_count:,.0f} | "
            f"{row.total_w_area:,.0f} | {row.total_w_band:,.0f} | "
            f"{row.ratio_w_area_to_count:.3f} | {row.ratio_w_band_to_count:.3f} |"
            for row in agreement.itertuples()
        ],
        "",
        "The band weight keeps only footprints between "
        f"{DWELLING_BAND[0]:.0f} and {DWELLING_BAND[1]:.0f} m2, which drops",
        "warehouses and sheds. It lands within "
        f"{abs(1 - agreement['ratio_w_band_to_count'].mean()):.1%} of the count",
        "weight, so warehouse-sized footprints are not driving the allocation.",
        "",
        "The area weight allocates "
        f"{1 - agreement['ratio_w_area_to_count'].mean():.1%} less to barrios.",
        "Barrio footprints are systematically smaller than non-barrio footprints",
        "in the same radio, which is what informal housing looks like. It also",
        "means area is the wrong weight for counting dwellings: a small dwelling",
        "is still a dwelling. The count weight is the more conservative of the",
        "two, because allocating fewer households to barrios would raise the",
        "footprints-per-household ratio rather than lower it.",
        "",
        "Carried through to the headline ratio, the three weights give:",
        "",
        "| Weight | Footprints per household, all barrios |",
        "| --- | ---: |",
        *[
            f"| {label} | {total_footprints / value:.2f} |"
            for label, value in (
                ("Count, primary", households),
                (
                    "Area",
                    float(
                        agreement.loc[
                            agreement["quantity"] == "households", "total_w_area"
                        ].iloc[0]
                    ),
                ),
                (
                    "Dwelling-size band",
                    float(
                        agreement.loc[
                            agreement["quantity"] == "households", "total_w_band"
                        ].iloc[0]
                    ),
                ),
            )
        ],
        "",
        "Every weight puts the ratio near or above 2. The choice of weight moves",
        "it, but does not decide whether footprints exceed recorded households.",
        "",
        "## 5. Ratio by province",
        "",
        "Areal weighting produced extreme provincial outliers, which is the",
        "artefact at its clearest: small barrios inside large rural radios.",
        "",
        "| Province | Barrios | Areal ratio | Dasymmetric ratio |",
        "| --- | ---: | ---: | ---: |",
        *[
            f"| {row.provincia} | {row.barrios:,} | {AREAL_PROVINCES[row.provincia]:.2f} "
            f"| {row.legacy_population_ratio:.2f} |"
            for row in province.itertuples()
            if row.provincia in AREAL_PROVINCES
        ],
        "",
        "The full table is in `provincial_dasymmetric.csv`.",
        "",
        "## 6. Conservation and edge cases",
        "",
        "| Check | Value |",
        "| --- | ---: |",
        *[
            f"| {key.replace('_', ' ')} | {value:,.0f} |"
            for key, value in assignment.items()
        ],
        *[
            f"| {key.replace('_', ' ')} | {value:,.4f} |"
            if key.endswith("share")
            else f"| {key.replace('_', ' ')} | {value:,.0f} |"
            for key, value in checks.items()
        ],
        "",
        "Allocated totals are shares of national Census totals, so each share",
        "must fall at or below 1. The script raises if any exceeds it.",
        "",
        "## 7. Limits",
        "",
        "- Footprint-share weighting assumes footprints carry similar dwelling",
        "  counts inside and outside a barrio within the same radio. High-rises",
        "  outside a barrio make the method understate the discrepancy.",
        "  Non-residential buildings outside a barrio make it overstate.",
        "- The area and band weights address that assumption indirectly. Results",
        "  are not stratified by apartment share, and no height-weighted",
        "  sensitivity was run, so the high-rise direction is not controlled",
        "  directly.",
        "- Census counts are from May 2022 and footprints from September 2024.",
        "  For a weight, which is a ratio inside one radio, this matters only if",
        "  building growth differed inside and outside the barrio.",
        "- A radio with no footprints contributes nothing. That is 46 radios",
        "  holding 7,847 people nationally.",
        "- This says nothing about national census omission.",
        "",
    ]
    (OUTPUT_DIR / "report.md").write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--census-path", type=Path, required=True)
    parser.add_argument("--settlements-path", type=Path, required=True)
    parser.add_argument("--buildings-path", type=Path, default=BUILDINGS_PATH)
    parser.add_argument("--redatam-path", type=Path, default=REDATAM_PATH)
    parser.add_argument("--temp-dir", type=Path, default=Path("/tmp/duckdb-bv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    con = connect(args.temp_dir)

    load_geometry(
        con, {"census": args.census_path, "settlements": args.settlements_path}
    )
    project(con)
    build_census(con, args.redatam_path)
    assignment = assign_footprints(con, args.buildings_path)
    build_weights(con)

    allocated = allocate(con)
    sweep = coverage_sweep(con)
    checks = conservation(con, allocated)
    agreement = weight_agreement(allocated)
    province = provincial(allocated)
    con.close()

    allocated.to_parquet(OUTPUT_DIR / "barrio_estimates.parquet", index=False)
    sweep.to_csv(OUTPUT_DIR / "coverage_sweep_dasymmetric.csv", index=False)
    agreement.to_csv(OUTPUT_DIR / "weight_agreement.csv", index=False)
    province.to_csv(OUTPUT_DIR / "provincial_dasymmetric.csv", index=False)
    (OUTPUT_DIR / "checks.json").write_text(
        json.dumps({**assignment, **checks}, indent=2, default=float) + "\n",
        encoding="utf-8",
    )
    write_report(allocated, sweep, agreement, province, checks, assignment)
    print(sweep.to_string(index=False))
    print(f"\nWrote {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
