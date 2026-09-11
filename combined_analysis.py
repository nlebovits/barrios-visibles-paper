#!/usr/bin/env python3
"""Report the population branch and the dwelling-inventory branch together.

Two analyses of the same settlements have been living apart. The population
branch allocates census-radio population into barrio polygons by area and
compares it with footprints times a persons-per-footprint multiplier. The
inventory branch takes whole radios above a coverage threshold and compares
footprints with Census dwellings and households directly, with no multiplier
and no allocation. Each answers a different question, and neither replaces the
other.

This script runs both, restores three diagnostics that previously existed only
as prose, and writes one report that keeps the units straight.

What it adds:

    Adjacent-radio classification   radios containing a barrio, radios within
                                    2 km below 1 percent coverage, and radios
                                    beyond 2 km, compared on persons per
                                    private dwelling
    Provincial ratios               the population-branch ratio by province at
                                    every coverage threshold
    Raw footprint-to-family ratio   footprints over RENABAP families, which the
                                    manuscript states but never computed

Axis order. These files declare OGC:CRS84, which is longitude then latitude.
DuckDB's spheroid functions and its EPSG:4326 alias both assume latitude then
longitude, so passing the geometry straight in returns wrong magnitudes. This
script sidesteps the whole question by projecting to an equal-area projection
once and doing planar maths in metres.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import duckdb
import pandas as pd

import census_comparison as population_branch

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs" / "combined"
DASYMMETRIC_SWEEP = ROOT / "outputs" / "dasymmetric" / "coverage_sweep_dasymmetric.csv"
INVENTORY_SUMMARY = (
    ROOT
    / "outputs"
    / "census-dwelling-footprint"
    / "census_dwelling_footprint_summary.csv"
)
REDATAM_PATH = DATA_DIR / "census_2022_redatam.parquet"

# Lambert azimuthal equal area centred on Argentina. Areas are exact by
# construction and distances hold to about one percent across the country,
# which is ample for a 2 km classification.
PROJECTION = "+proj=laea +lat_0=-38 +lon_0=-64 +datum=WGS84 +units=m +no_defs"

ADJACENT_DISTANCE_M = 2000.0
ADJACENT_COVERAGE = 0.01
THRESHOLDS = population_branch.THRESHOLDS
MULTIPLIER = 3.35

# The archived validation table, for comparison only. The query that produced
# it was not preserved, so a reimplementation is not expected to match exactly.
ARCHIVED_ADJACENT = {
    "Contains barrio": (7_695, 7_795_633, 3.18),
    "Border, below 1 percent": (30_285, 24_342_739, 2.55),
    "Distant, beyond 2 km": (20_391, 12_110_393, 2.33),
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


def load(con: duckdb.DuckDBPyConnection, census: Path, settlements: Path) -> None:
    con.execute(f"""
        CREATE TEMP TABLE tracts AS SELECT * FROM '{quote(census)}';
        CREATE TEMP TABLE barrios AS
        SELECT id_renabap, provincia, renabap_families, building_count, geometry
        FROM '{quote(settlements)}';

        CREATE TEMP TABLE tracts_m AS
        SELECT COD_2022, PROV, POB_TOT_P, VIV_TOT_P,
               ST_Transform(geometry, 'OGC:CRS84', '{PROJECTION}') AS g
        FROM tracts;
        CREATE TEMP TABLE barrios_m AS
        SELECT id_renabap, provincia, renabap_families, building_count,
               ST_Transform(geometry, 'OGC:CRS84', '{PROJECTION}') AS g
        FROM barrios;
    """)
    totals = con.execute("""
        SELECT (SELECT COUNT(*) FROM tracts), (SELECT SUM(POB_TOT_P) FROM tracts),
               (SELECT SUM(VIV_TOT_P) FROM tracts), (SELECT COUNT(*) FROM barrios),
               (SELECT SUM(building_count) FROM barrios)
    """).fetchone()
    if totals != (66_502, 45_618_784, 17_783_028, 6_467, 1_969_975):
        raise RuntimeError(f"Unexpected input totals: {totals}")


def build_overlap(con: duckdb.DuckDBPyConnection) -> None:
    """Radio coverage and the barrio-radio intersection, in metres."""
    con.execute("""
        CREATE TEMP TABLE overlap AS
        SELECT t.COD_2022, b.id_renabap, b.provincia, b.renabap_families,
               b.building_count,
               ST_Area(t.g) AS tract_area,
               ST_Area(b.g) AS barrio_area,
               ST_Area(ST_Intersection(t.g, b.g)) AS intersection_area,
               t.POB_TOT_P, t.VIV_TOT_P
        FROM tracts_m t JOIN barrios_m b ON ST_Intersects(t.g, b.g)
        WHERE ST_Area(ST_Intersection(t.g, b.g)) > 0;

        CREATE TEMP TABLE tract_coverage AS
        SELECT COD_2022,
               MAX(tract_area) AS tract_area,
               SUM(intersection_area) AS barrio_area_in_tract,
               SUM(intersection_area) / NULLIF(MAX(tract_area), 0) AS coverage
        FROM overlap GROUP BY COD_2022;
    """)


def adjacent_radios(con: duckdb.DuckDBPyConnection, redatam: Path) -> pd.DataFrame:
    """Classify every radio by its relation to the nearest barrio.

    The supplement describes the rule: radios with at least 1 percent barrio
    coverage, radios within 2 km below that coverage, and radios beyond 2 km,
    urban radios only. The distance query itself was not preserved, so this is
    a reimplementation of the stated rule rather than a reproduction of the
    original one.

    The urban filter uses REDATAM VIVIENDA_URP. A radio counts as urban when
    most of its private dwellings fall in category 1, Urbano.
    """
    con.execute(f"""
        CREATE TEMP TABLE urban AS
        SELECT id_geo AS COD_2022,
               SUM(conteo) FILTER (WHERE valor_categoria = '1') AS urban_dwellings,
               SUM(conteo) AS total_dwellings
        FROM '{quote(redatam)}'
        WHERE codigo_variable = 'VIVIENDA_URP'
        GROUP BY id_geo;

        CREATE TEMP TABLE near_barrio AS
        SELECT DISTINCT t.COD_2022
        FROM tracts_m t JOIN barrios_m b
          ON ST_DWithin(t.g, b.g, {ADJACENT_DISTANCE_M});

        CREATE TEMP TABLE radio_class AS
        SELECT
            t.COD_2022,
            t.POB_TOT_P,
            t.VIV_TOT_P,
            ST_Area(t.g) / 1e6 AS area_km2,
            COALESCE(u.urban_dwellings, 0) > COALESCE(u.total_dwellings, 0) / 2.0
                AS is_urban,
            CASE
                WHEN COALESCE(c.coverage, 0) >= {ADJACENT_COVERAGE}
                    THEN 'Contains barrio'
                WHEN n.COD_2022 IS NOT NULL THEN 'Border, below 1 percent'
                ELSE 'Distant, beyond 2 km'
            END AS radio_class
        FROM tracts_m t
        LEFT JOIN tract_coverage c USING (COD_2022)
        LEFT JOIN near_barrio n USING (COD_2022)
        LEFT JOIN urban u USING (COD_2022);
    """)
    return con.execute("""
        SELECT
            radio_class,
            COUNT(*) AS radios,
            SUM(POB_TOT_P)::BIGINT AS population,
            SUM(VIV_TOT_P)::BIGINT AS private_dwellings,
            SUM(POB_TOT_P)::DOUBLE / NULLIF(SUM(VIV_TOT_P), 0)
                AS persons_per_private_dwelling,
            MEDIAN(POB_TOT_P / NULLIF(area_km2, 0)) AS median_pop_per_km2
        FROM radio_class
        WHERE is_urban
        GROUP BY radio_class
        ORDER BY CASE radio_class
            WHEN 'Contains barrio' THEN 1
            WHEN 'Border, below 1 percent' THEN 2 ELSE 3 END
    """).df()


def provincial_ratios(con: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    """The population-branch ratio by province, at every coverage threshold.

    This repeats the barrio-level aggregation the published sweep uses,
    including the rule that a barrio is retained only when the eligible radios
    cover at least half of it, and groups the result by province.
    """
    values = ",".join(f"({threshold})" for threshold in THRESHOLDS)
    return con.execute(f"""
        WITH detail AS (
            SELECT o.*, tc.coverage
            FROM overlap o JOIN tract_coverage tc USING (COD_2022)
        ),
        barrio_aggregates AS (
            SELECT
                threshold,
                provincia,
                id_renabap,
                MAX(building_count) AS buildings,
                SUM(POB_TOT_P * intersection_area / NULLIF(tract_area, 0))
                    AS census_population,
                SUM(intersection_area) / MAX(barrio_area)
                    AS retained_barrio_fraction
            FROM detail
            CROSS JOIN (VALUES {values}) thresholds(threshold)
            WHERE coverage >= threshold
            GROUP BY threshold, provincia, id_renabap
        )
        SELECT
            threshold,
            provincia,
            COUNT(*) AS barrios,
            SUM(buildings)::BIGINT AS buildings,
            ROUND(SUM(census_population))::BIGINT AS census_population,
            ROUND(SUM(buildings) * {MULTIPLIER})::BIGINT AS footprint_population,
            SUM(buildings) * {MULTIPLIER} / NULLIF(SUM(census_population), 0)
                AS ratio
        FROM barrio_aggregates
        WHERE retained_barrio_fraction >= 0.5
        GROUP BY threshold, provincia
        HAVING SUM(census_population) > 0
        ORDER BY threshold, ratio DESC
    """).df()


def family_ratio(con: duckdb.DuckDBPyConnection) -> dict:
    """Footprints over RENABAP families. The manuscript states 59 percent."""
    footprints, families = con.execute(
        "SELECT SUM(building_count), SUM(renabap_families) FROM barrios"
    ).fetchone()
    return {
        "footprints": int(footprints),
        "renabap_families": int(families),
        "ratio": footprints / families,
        "excess_pct": footprints / families - 1,
    }


def inventory_rows() -> pd.DataFrame:
    """The dwelling-inventory branch, as census_dwelling_footprint.py wrote it."""
    if not INVENTORY_SUMMARY.exists():
        raise FileNotFoundError(
            f"{INVENTORY_SUMMARY} is missing. Run census_dwelling_footprint.py first."
        )
    summary = pd.read_csv(INVENTORY_SUMMARY)
    return summary[
        (summary["coverage_measure"] == "union")
        & (summary["inventory"] == "vida")
        & (summary["stratum"] == "All eligible")
        & (summary["footprint_filter"] == "No filter")
    ].sort_values("threshold")


def write_report(
    sweep: list[dict],
    dasymmetric: pd.DataFrame,
    sensitivity: list[dict],
    inventory: pd.DataFrame,
    adjacent: pd.DataFrame,
    provincial: pd.DataFrame,
    families: dict,
) -> None:
    top = provincial[provincial["threshold"] == 0.0].head(8)
    areal_by_threshold = {
        round(float(row["threshold"]), 2): float(row["ratio"]) for row in sweep
    }
    lines = [
        "# Combined report: population branch and dwelling-inventory branch",
        "",
        "Two analyses of the same settlements, run together and reported with",
        "their units kept separate. They answer different questions and neither",
        "replaces the other.",
        "",
        "| Branch | Unit | Compares | Multiplier | Allocation |",
        "| --- | --- | --- | --- | --- |",
        "| Population | Barrio | Footprint-implied against Census population | "
        f"x{MULTIPLIER} persons per footprint | Radio population split by area |",
        "| Inventory | Whole radio | Footprints against Census dwellings and "
        "households | None | None |",
        "",
        "**They are not independent.** Both rest on the same VIDA footprint",
        "count, so an error on the footprint side moves both in the same",
        "direction. Agreement between them is consistency, not corroboration.",
        "",
        "## 1. Population branch",
        "",
        "Allocation is by footprint share, from `dasymmetric_allocation.py`.",
        "The areal column is the superseded method, kept for comparison and",
        "still asserted by `census_comparison.py` so the published figures stay",
        "verifiable.",
        "",
        "| Minimum radio coverage | Barrios | Areal ratio | Dasymmetric ratio |",
        "| ---: | ---: | ---: | ---: |",
        *[
            f"| {row.threshold:.0%} | {row.barrios:,} | "
            f"{areal_by_threshold.get(round(row.threshold, 2), float('nan')):.2f} | "
            f"{row.legacy_population_ratio:.2f} |"
            for row in dasymmetric.itertuples()
        ],
        "",
        "Areal weighting produced a gradient from 2.62 to 1.88. Footprint-share",
        "allocation removes it: the same sweep on the same filter is flat near",
        "1.9, and the two agree at 95 percent coverage, where a radio is almost",
        "all barrio and the choice of weight stops mattering.",
        "",
        "### Superseded areal sweep",
        "",
        "| Minimum radio coverage | Barrios | Footprints | Census population | "
        f"Footprint population (x{MULTIPLIER}) | Ratio |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in sweep:
        lines.append(
            f"| {float(row['threshold']):.0%} | {int(row['barrios']):,} | "
            f"{int(row['buildings']):,} | {int(row['census_population']):,} | "
            f"{int(row['footprint_population']):,} | {float(row['ratio']):.2f} |"
        )
    lines += [
        "",
        "Persons-per-footprint sensitivity at the 75 percent threshold:",
        "",
        "| Multiplier | Footprint population | Census population | Ratio |",
        "| ---: | ---: | ---: | ---: |",
        *[
            f"| {float(row['multiplier']):.2f} | "
            f"{int(row['footprint_population']):,} | "
            f"{int(row['census_population']):,} | {float(row['ratio']):.2f} |"
            for row in sensitivity
        ],
        "",
        "## 2. Dwelling-inventory branch",
        "",
        "Whole radios, no multiplier, no allocation. The unit is the radio, so",
        "these counts are not comparable with the barrio counts above.",
        "",
        "| Minimum radio coverage | Radios | Barrios | Footprints | "
        "Occupied dwellings | Households | FP / occupied | FP / household |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        *[
            f"| {row.threshold:.0%} | {row.n_radios:,} | {row.n_barrios:,} | "
            f"{row.footprints:,} | {row.dwellings_occupied_broad:,} | "
            f"{row.households:,} | "
            f"{row.ratio_totals_per_occupied_broad:.2f} | "
            f"{row.ratio_totals_per_household:.2f} |"
            for row in inventory.itertuples()
        ],
        "",
        "## 3. Adjacent radios",
        "",
        "If barrio residents were enumerated at nearby formal addresses rather",
        "than missed, radios bordering a barrio should show inflated occupancy.",
        "Urban radios only. Classes are: at least "
        f"{ADJACENT_COVERAGE:.0%} barrio coverage; within "
        f"{ADJACENT_DISTANCE_M / 1000:.0f} km below that coverage; and beyond.",
        "",
        "| Radio class | Radios | Population | Persons per private dwelling | "
        "Median pop per km2 |",
        "| --- | ---: | ---: | ---: | ---: |",
        *[
            f"| {row.radio_class} | {row.radios:,} | {row.population:,} | "
            f"{row.persons_per_private_dwelling:.2f} | "
            f"{row.median_pop_per_km2:,.0f} |"
            for row in adjacent.itertuples()
        ],
        "",
        "Against the archived validation table, whose query was not preserved:",
        "",
        "| Radio class | Archived radios | Here | Archived ratio | Here |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in adjacent.itertuples():
        archived = ARCHIVED_ADJACENT.get(row.radio_class)
        if archived is None:
            continue
        lines.append(
            f"| {row.radio_class} | {archived[0]:,} | {row.radios:,} | "
            f"{archived[2]:.2f} | {row.persons_per_private_dwelling:.2f} |"
        )
    lines += [
        "",
        "Private dwellings may be unoccupied or hold more than one household, so",
        "persons per private dwelling is an occupancy diagnostic and not a",
        "household size.",
        "",
        "## 4. Ratio by province",
        "",
        "The population-branch ratio, grouped by province. Nothing in the",
        "repository computed this before. It recovers the three provincial",
        "outliers the blog post cites as evidence that area weighting inflates",
        "the unfiltered ratio. Highest eight at the unfiltered threshold:",
        "",
        "| Province | Barrios | Census population | Ratio |",
        "| --- | ---: | ---: | ---: |",
        *[
            f"| {row.provincia} | {row.barrios:,} | {row.census_population:,} | "
            f"{row.ratio:.2f} |"
            for row in top.itertuples()
        ],
        "",
        "Against the figures the blog post quotes:",
        "",
        "| Province | Blog | Computed here |",
        "| --- | ---: | ---: |",
        *[
            f"| {row.provincia} | {claim} | {row.ratio:.2f} |"
            for claim, row in (
                (
                    name,
                    provincial[
                        (provincial["threshold"] == 0.0)
                        & (provincial["provincia"] == province)
                    ].iloc[0],
                )
                for province, name in (
                    ("San Juan", "7x"),
                    ("La Pampa", "4x"),
                    ("Santa Cruz", "4x"),
                )
            )
        ],
        "",
        "The full sweep by province is in `provincial_ratios.csv`. Province-level",
        "values at low coverage thresholds carry the allocation artefact the",
        "sweep exists to control, and should not be quoted on their own.",
        "",
        "## 5. Footprints against RENABAP families",
        "",
        f"{families['footprints']:,} footprints against "
        f"{families['renabap_families']:,} recorded families is a ratio of "
        f"{families['ratio']:.3f}, an excess of {families['excess_pct']:.1%}.",
        "This is the raw comparison the manuscript states and did not compute.",
        "",
        "## 6. Footprint baselines",
        "",
        "The two branches sit on different footprint counts, and this is a known",
        "unresolved gap rather than an error introduced here.",
        "",
        "| Source | Footprints |",
        "| --- | ---: |",
        f"| Population and inventory branches | {families['footprints']:,} |",
        "| Archived settlement estimates | 1,967,013 |",
        "| Difference | 2,962 across 302 settlements |",
        "",
        "## 7. Method notes",
        "",
        "Geometry is projected once to an equal-area projection centred on",
        "Argentina, and every area and distance is planar metres from there.",
        "These files declare OGC:CRS84, which is longitude then latitude, while",
        "DuckDB's spheroid functions and its EPSG:4326 alias assume latitude",
        "then longitude. Projecting first avoids the mismatch rather than",
        "correcting for it.",
        "",
        "The adjacent-radio and provincial tables are new implementations of",
        "rules described in prose. They are not reproductions of the original",
        "queries, which were not preserved.",
        "",
    ]
    (OUTPUT_DIR / "report.md").write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--census-path", type=Path, required=True)
    parser.add_argument("--settlements-path", type=Path, required=True)
    parser.add_argument("--redatam-path", type=Path, default=REDATAM_PATH)
    parser.add_argument("--temp-dir", type=Path, default=Path("/tmp/duckdb-bv"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    results = population_branch.run_analysis(args.census_path, args.settlements_path)
    population_branch.verify(results)
    print("Population branch verified against the published sweep")

    con = connect(args.temp_dir)
    load(con, args.census_path, args.settlements_path)
    build_overlap(con)
    adjacent = adjacent_radios(con, args.redatam_path)
    provincial = provincial_ratios(con)
    families = family_ratio(con)
    con.close()

    inventory = inventory_rows()
    adjacent.to_csv(OUTPUT_DIR / "adjacent_radios.csv", index=False)
    provincial.to_csv(OUTPUT_DIR / "provincial_ratios.csv", index=False)
    (OUTPUT_DIR / "family_ratio.json").write_text(
        json.dumps(families, indent=2) + "\n", encoding="utf-8"
    )
    if not DASYMMETRIC_SWEEP.exists():
        raise FileNotFoundError(
            f"{DASYMMETRIC_SWEEP} is missing. Run dasymmetric_allocation.py first."
        )
    write_report(
        results["coverage_sweep"],
        pd.read_csv(DASYMMETRIC_SWEEP),
        results["multiplier_sensitivity"],
        inventory,
        adjacent,
        provincial,
        families,
    )
    print(adjacent.to_string(index=False))
    print(f"\nWrote {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
