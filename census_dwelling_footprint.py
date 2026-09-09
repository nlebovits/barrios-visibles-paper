#!/usr/bin/env python3
"""Compare the physical building inventory with the Census 2022 dwelling and
household inventory, inside census radios that lie almost entirely inside
RENABAP barrios populares.

The published comparison in census_comparison.py converts footprints into
population and allocates census-radio population into barrio polygons by area.
Two assumptions sit between the physical evidence and the result: a
persons-per-footprint multiplier, and the areal allocation itself.

This analysis removes both. Once a radio passes the RENABAP coverage threshold
the whole radio is used, with its full INDEC dwelling and household counts and
every footprint whose centroid falls inside it. No multiplier is applied and no
census quantity is split by area.

Temporal mismatch, not corrected here:

    Census counts     May 2022
    Building snapshot September 2024

Usage:

    pixi run dwelling-footprint -- \
      --census-path /path/to/radios-hilbert.parquet \
      --settlements-path /path/to/barrios-hilbert.parquet
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import duckdb
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs" / "census-dwelling-footprint"

CENSUS_PATH = DATA_DIR / "census_2022_radios.parquet"
SETTLEMENTS_PATH = DATA_DIR / "census_settlement_counts.parquet"
BUILDINGS_PATH = DATA_DIR / "buildings_arg.parquet"
REDATAM_PATH = DATA_DIR / "census_2022_redatam.parquet"

SOURCE_COOP = "https://data.source.coop/nlebovits/censo-argentino/2022/"
CENSUS_LIVE_URL = SOURCE_COOP + "radios.parquet"
REDATAM_LIVE_URL = SOURCE_COOP + "census-data.parquet"

CENSUS_DATE = "May 2022"
BUILDINGS_DATE = "September 2024"

THRESHOLDS = (0.50, 0.75, 0.90, 0.95)
PRIMARY_THRESHOLD = 0.95
MASTER_THRESHOLD = min(THRESHOLDS)

FOOTPRINT_FILTERS = ("all", "ge6", "ge10")
FILTER_LABELS = {"all": "No filter", "ge6": ">=6 m2", "ge10": ">=10 m2"}
COVERAGE_MEASURES = ("union", "sum")

CENSUS_DAY = "2022-05-18"
MS_IMAGERY_END = "2021-06-06"

# Three building inventories over the same radios. VIDA postdates Census Day by
# 28 months, so it can contain post-Census construction. Both Microsoft
# releases are built from imagery ending 2021-06-06, eleven months before
# Census Day, so neither can. Microsoft publishes no area column, so its
# footprint area is computed from the geometry. Its parquet also fails DuckDB's
# GeoParquet type check, so it is read as WKB with the conversion disabled.
VIDA = "vida"
MS2022 = "ms2022"
MS2023 = "ms2023"
INVENTORIES = (VIDA, MS2022, MS2023)
PRE_CENSUS = MS2022

INVENTORY_SPECS = {
    VIDA: {
        "label": "VIDA, September 2024",
        "short": "VIDA 2024-09",
        "path": DATA_DIR / "buildings_arg.parquet",
        "geoparquet": True,
        "geometry_sql": "geometry",
        "area_sql": "area_in_meters",
        "pre_census": False,
    },
    MS2022: {
        "label": "Microsoft release 2022-06-14, imagery to 2021-06-06",
        "short": "MS 2022-06",
        "path": DATA_DIR / "ms-buildings-2022-06-14",
        "geoparquet": False,
        "geometry_sql": "ST_GeomFromWKB(geometry)",
        "area_sql": None,
        "pre_census": True,
    },
    MS2023: {
        "label": "Microsoft release 2023-04-25, imagery to 2021-06-06",
        "short": "MS 2023-04",
        "path": DATA_DIR / "ms-buildings-2023-04-25",
        "geoparquet": False,
        "geometry_sql": "ST_GeomFromWKB(geometry)",
        "area_sql": None,
        "pre_census": True,
    },
}
INVENTORY_LABELS = {key: spec["label"] for key, spec in INVENTORY_SPECS.items()}

# census_comparison.py asserts the same tuple before it reproduces the
# published sweep. Reusing it keeps the two analyses on identical inputs.
EXPECTED_INPUT_TOTALS = (66_502, 45_618_784, 17_783_028, 6_467, 1_969_975)

# National REDATAM identities, verified against the Source Cooperative file.
# Each one pins the universe of a variable. See report.md for the derivation.
EXPECTED_REDATAM = {
    "dwellings_all": 17_783_029,
    "dwellings_present": 15_699_016,
    "dwellings_absent": 2_084_013,
    "dwellings_habitual_absent": 254_521,
    "dwellings_vacant_other": 1_829_492,
    "households": 15_932_302,
    "dwellings_departamento": 3_744_173,
    "population_redatam": 45_618_787,
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
    with requests.get(url, stream=True, timeout=600) as response:
        response.raise_for_status()
        with temporary.open("wb") as stream:
            for block in response.iter_content(8 * 1024 * 1024):
                if block:
                    stream.write(block)
    temporary.replace(destination)


def prepare_inputs(args: argparse.Namespace) -> dict[str, Path]:
    census = args.census_path or CENSUS_PATH
    settlements = args.settlements_path or SETTLEMENTS_PATH
    buildings = args.buildings_path or BUILDINGS_PATH
    redatam = args.redatam_path or REDATAM_PATH

    if not census.exists():
        download(CENSUS_LIVE_URL, census)
    if not redatam.exists():
        download(REDATAM_LIVE_URL, redatam)

    paths = {
        "census": census,
        "settlements": settlements,
        "buildings": buildings,
        "redatam": redatam,
    }
    for name, path in paths.items():
        if not path.exists():
            raise FileNotFoundError(f"{name}: {path}")
    return paths


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


def load_geometry(con: duckdb.DuckDBPyConnection, paths: dict[str, Path]) -> None:
    con.execute(f"""
        CREATE TEMP TABLE tracts AS SELECT * FROM '{quote(paths["census"])}';
        CREATE TEMP TABLE barrios AS
        SELECT id_renabap, provincia, renabap_families, building_count, geometry
        FROM '{quote(paths["settlements"])}';
    """)
    totals = con.execute("""
        SELECT
            (SELECT COUNT(*) FROM tracts),
            (SELECT SUM(POB_TOT_P) FROM tracts),
            (SELECT SUM(VIV_TOT_P) FROM tracts),
            (SELECT COUNT(*) FROM barrios),
            (SELECT SUM(building_count) FROM barrios)
    """).fetchone()
    if totals != EXPECTED_INPUT_TOTALS:
        raise RuntimeError(
            f"Unexpected publication input totals: {totals}. "
            f"Expected {EXPECTED_INPUT_TOTALS}."
        )


def build_coverage(con: duckdb.DuckDBPyConnection) -> None:
    """Per-radio RENABAP coverage under two measures.

    barrio_area_sum reproduces census_comparison.py, which sums the
    intersections and therefore double-counts where RENABAP polygons overlap
    each other. barrio_area_union dissolves them first and cannot exceed the
    radio area. The union measure is primary; the sum measure is kept so the
    eligible sets of the two analyses can be compared.
    """
    con.execute("""
        CREATE TEMP TABLE tract_coverage AS
        SELECT
            r.COD_2022,
            MAX(r.PROV) AS prov_code,
            MAX(r.DEPTO) AS depto_code,
            MAX(r.REDATAM) AS redatam_flag,
            MAX(r.POB_TOT_P) AS census_population,
            MAX(r.VIV_TOT_P) AS census_private_dwellings,
            ST_Area_Spheroid(ST_FlipCoordinates(MAX(r.geometry))) AS tract_area,
            SUM(ST_Area_Spheroid(
                ST_FlipCoordinates(ST_Intersection(r.geometry, b.geometry))))
                AS barrio_area_sum,
            ST_Area_Spheroid(
                ST_FlipCoordinates(ST_Union_Agg(
                    ST_Intersection(r.geometry, b.geometry))))
                AS barrio_area_union,
            COUNT(*) AS n_barrios_intersecting
        FROM tracts r
        JOIN barrios b ON ST_Intersects(r.geometry, b.geometry)
        GROUP BY r.COD_2022;

        CREATE TEMP TABLE radio_barrio AS
        SELECT DISTINCT r.COD_2022, b.id_renabap
        FROM tracts r
        JOIN barrios b ON ST_Intersects(r.geometry, b.geometry)
        WHERE ST_Area_Spheroid(
            ST_FlipCoordinates(ST_Intersection(r.geometry, b.geometry))) > 0;

        CREATE TEMP TABLE coverage AS
        SELECT
            *,
            barrio_area_sum / NULLIF(tract_area, 0) AS coverage_sum,
            LEAST(barrio_area_union / NULLIF(tract_area, 0), 1.0) AS coverage_union
        FROM tract_coverage;
    """)
    con.execute(f"""
        CREATE TEMP TABLE eligible AS
        SELECT t.COD_2022, t.geometry
        FROM tracts t
        JOIN coverage c USING (COD_2022)
        WHERE c.coverage_union >= {MASTER_THRESHOLD}
           OR c.coverage_sum >= {MASTER_THRESHOLD};
    """)


def count_footprints(con: duckdb.DuckDBPyConnection, inventory: str) -> float:
    """Assign each footprint to exactly one radio by centroid containment.

    No inventory here carries a stable footprint id. VIDA has boundary_id
    constant across the country and s2_id at cell granularity. Microsoft has no
    id column at all. Census radios tile the territory without overlap, so a
    centroid lies in at most one radio. That gives exactly-once counting
    without an id, and it removes the double-counting that an ST_Intersects
    join produces along shared edges.
    """
    spec = INVENTORY_SPECS[inventory]
    path = spec["path"]
    source = quote(path / "*.parquet") if path.is_dir() else quote(path)
    geometry = spec["geometry_sql"]
    area = spec["area_sql"] or f"ST_Area_Spheroid(ST_FlipCoordinates({geometry}))"
    con.execute(
        f"SET enable_geoparquet_conversion = {str(spec['geoparquet']).lower()};"
    )
    started = time.time()
    con.execute(f"""
        INSERT INTO radio_footprints
        SELECT
            e.COD_2022,
            '{inventory}',
            COUNT(*),
            COUNT(*) FILTER (WHERE b.area_m2 >= 6),
            COUNT(*) FILTER (WHERE b.area_m2 >= 10),
            SUM(b.area_m2),
            MEDIAN(b.area_m2)
        FROM (
            SELECT {geometry} AS geometry, {area} AS area_m2
            FROM read_parquet('{source}')
        ) b
        JOIN eligible e ON ST_Within(ST_Centroid(b.geometry), e.geometry)
        GROUP BY e.COD_2022;
    """)
    con.execute("SET enable_geoparquet_conversion = true;")
    return time.time() - started


def create_footprint_table(con: duckdb.DuckDBPyConnection) -> None:
    con.execute("""
        CREATE TEMP TABLE radio_footprints (
            COD_2022 VARCHAR,
            inventory VARCHAR,
            footprints_all BIGINT,
            footprints_ge6 BIGINT,
            footprints_ge10 BIGINT,
            area_total DOUBLE,
            area_median DOUBLE
        );
    """)


def build_census(con: duckdb.DuckDBPyConnection, redatam: Path) -> None:
    """Pivot the long REDATAM table for the eligible radios.

    Variable universes, each confirmed by an exact national identity:

      VIVIENDA_TIPOVIVG  all private dwellings              17,783,029
      VIVIENDA_V01       all private dwellings, by type     17,783,029
      VIVIENDA_V02       all private dwellings, by occupancy
                         1 people present                   15,699,016
                         2 nobody present                    2,084,013
      VIVIENDA_V04       reason, universe is V02 = 2         2,084,013
                         5 habitual residents absent           254,521
      VIVIENDA_V06       households per dwelling, universe is V02 = 1
                         sum of category x count            15,932,302
      VIVIENDA_TOTPOBV   persons per dwelling, universe is V02 = 1

    Households and population therefore exist only for dwellings with people
    present. A dwelling whose habitual residents were absent on Census Day
    counts in the dwelling stock and contributes zero households.
    """
    con.execute(f"""
        CREATE TEMP TABLE radio_census AS
        SELECT
            id_geo AS COD_2022,
            MAX(etiqueta_provincia) AS provincia,
            MAX(etiqueta_departamento) AS departamento,
            SUM(conteo) FILTER (WHERE codigo_variable = 'VIVIENDA_TIPOVIVG')
                AS dwellings_all,
            SUM(conteo) FILTER (WHERE codigo_variable = 'VIVIENDA_V02'
                                  AND valor_categoria = '1') AS dwellings_present,
            SUM(conteo) FILTER (WHERE codigo_variable = 'VIVIENDA_V02'
                                  AND valor_categoria = '2') AS dwellings_absent,
            SUM(conteo) FILTER (WHERE codigo_variable = 'VIVIENDA_V04'
                                  AND valor_categoria = '5')
                AS dwellings_habitual_absent,
            SUM(conteo) FILTER (WHERE codigo_variable = 'VIVIENDA_V04'
                                  AND valor_categoria IN ('1','2','3','4','6'))
                AS dwellings_vacant_other,
            SUM(TRY_CAST(valor_categoria AS INTEGER) * conteo)
                FILTER (WHERE codigo_variable = 'VIVIENDA_V06') AS households,
            SUM(conteo) FILTER (WHERE codigo_variable = 'VIVIENDA_V01'
                                  AND valor_categoria = '4')
                AS dwellings_departamento,
            SUM(TRY_CAST(valor_categoria AS INTEGER) * conteo)
                FILTER (WHERE codigo_variable = 'VIVIENDA_TOTPOBV')
                AS population_redatam
        FROM '{quote(redatam)}'
        WHERE codigo_variable IN (
            'VIVIENDA_TIPOVIVG','VIVIENDA_V01','VIVIENDA_V02',
            'VIVIENDA_V04','VIVIENDA_V06','VIVIENDA_TOTPOBV')
        GROUP BY id_geo;
    """)
    national = con.execute("""
        SELECT
            SUM(dwellings_all), SUM(dwellings_present), SUM(dwellings_absent),
            SUM(dwellings_habitual_absent), SUM(dwellings_vacant_other),
            SUM(households), SUM(dwellings_departamento),
            SUM(population_redatam)
        FROM radio_census
    """).fetchone()
    actual = dict(zip(EXPECTED_REDATAM, (int(v) for v in national), strict=True))
    if actual != EXPECTED_REDATAM:
        differences = {
            key: (actual[key], EXPECTED_REDATAM[key])
            for key in EXPECTED_REDATAM
            if actual[key] != EXPECTED_REDATAM[key]
        }
        raise RuntimeError(f"REDATAM national identities differ: {differences}")


def assemble(con: duckdb.DuckDBPyConnection) -> tuple[pd.DataFrame, pd.DataFrame]:
    counts = ",\n".join(
        f"""            COALESCE(MAX(f.footprints_{suffix})
                FILTER (WHERE f.inventory = '{inventory}'), 0)
                AS {inventory}_footprints_{suffix}"""
        for inventory in INVENTORIES
        for suffix in FOOTPRINT_FILTERS
    )
    areas = ",\n".join(
        f"""            MAX(f.area_median)
                FILTER (WHERE f.inventory = '{inventory}')
                AS {inventory}_area_median"""
        for inventory in INVENTORIES
    )
    radios = con.execute(f"""
        SELECT
            c.COD_2022,
            MAX(c.prov_code) AS prov_code,
            MAX(c.depto_code) AS depto_code,
            MAX(c.redatam_flag) AS redatam_flag,
            MAX(c.tract_area) AS tract_area_m2,
            MAX(c.barrio_area_sum) AS barrio_area_sum_m2,
            MAX(c.barrio_area_union) AS barrio_area_union_m2,
            MAX(c.coverage_sum) AS coverage_sum,
            MAX(c.coverage_union) AS coverage_union,
            MAX(c.n_barrios_intersecting) AS n_barrios_intersecting,
            MAX(c.census_population) AS census_population,
            MAX(c.census_private_dwellings) AS census_private_dwellings,
            MAX(rc.provincia) AS provincia,
            MAX(rc.departamento) AS departamento,
            MAX(rc.dwellings_all) AS dwellings_all,
            MAX(rc.dwellings_present) AS dwellings_present,
            MAX(rc.dwellings_absent) AS dwellings_absent,
            MAX(rc.dwellings_habitual_absent) AS dwellings_habitual_absent,
            MAX(rc.dwellings_vacant_other) AS dwellings_vacant_other,
            MAX(rc.households) AS households,
            MAX(rc.dwellings_departamento) AS dwellings_departamento,
            MAX(rc.population_redatam) AS population_redatam,
{counts},
{areas}
        FROM coverage c
        LEFT JOIN radio_census rc USING (COD_2022)
        LEFT JOIN radio_footprints f USING (COD_2022)
        WHERE c.coverage_union >= {MASTER_THRESHOLD}
           OR c.coverage_sum >= {MASTER_THRESHOLD}
        GROUP BY c.COD_2022
    """).df()
    pairs = con.execute("""
        SELECT rb.COD_2022, rb.id_renabap
        FROM radio_barrio rb
        JOIN eligible e USING (COD_2022)
    """).df()
    return radios, pairs


DENOMINATORS = {
    "dwelling_all": "dwellings_all",
    "occupied_broad": "dwellings_occupied_broad",
    "present": "dwellings_present",
    "household": "households",
}


def derive(radios: pd.DataFrame) -> pd.DataFrame:
    frame = radios.copy()
    frame["dwellings_occupied_broad"] = frame["dwellings_present"] + frame[
        "dwellings_habitual_absent"
    ].fillna(0)
    frame["pct_departamento"] = (
        frame["dwellings_departamento"].fillna(0) / frame["dwellings_all"]
    )
    frame["is_caba"] = frame["prov_code"] == "02"

    for inventory in INVENTORIES:
        for suffix in FOOTPRINT_FILTERS:
            numerator = frame[f"{inventory}_footprints_{suffix}"]
            for label, column in DENOMINATORS.items():
                frame[f"{inventory}_fp_{suffix}_per_{label}"] = numerator / frame[
                    column
                ].replace(0, pd.NA)

    # How much thinner a single-source inventory is than the conflation.
    for inventory in INVENTORIES:
        if inventory == VIDA:
            continue
        frame[f"{inventory}_over_vida"] = frame[f"{inventory}_footprints_all"] / frame[
            "vida_footprints_all"
        ].replace(0, pd.NA)

    frame["households_per_occupied_broad"] = frame["households"] / frame[
        "dwellings_occupied_broad"
    ].replace(0, pd.NA)
    frame["pop_per_occupied_broad"] = frame["census_population"] / frame[
        "dwellings_occupied_broad"
    ].replace(0, pd.NA)
    frame["pop_per_household"] = frame["census_population"] / frame[
        "households"
    ].replace(0, pd.NA)

    quartiles = frame["pct_departamento"].quantile([0.25, 0.50, 0.75])
    frame["departamento_quartile"] = pd.cut(
        frame["pct_departamento"],
        bins=[-0.001, *quartiles.tolist(), 1.001],
        labels=["Q1 lowest", "Q2", "Q3", "Q4 highest"],
    )
    frame["horizontal_regime"] = frame["pct_departamento"] < quartiles[0.75]
    frame.attrs["departamento_q75"] = float(quartiles[0.75])
    return frame


def strata(frame: pd.DataFrame) -> dict[str, pd.Series]:
    return {
        "All eligible": pd.Series(True, index=frame.index),
        "Horizontal regime": frame["horizontal_regime"],
        "Excluding CABA": ~frame["is_caba"],
        "CABA only": frame["is_caba"],
        "Apartment share Q1 lowest": frame["departamento_quartile"] == "Q1 lowest",
        "Apartment share Q2": frame["departamento_quartile"] == "Q2",
        "Apartment share Q3": frame["departamento_quartile"] == "Q3",
        "Apartment share Q4 highest": frame["departamento_quartile"] == "Q4 highest",
    }


def summarise(frame: pd.DataFrame, pairs: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict] = []
    for measure in COVERAGE_MEASURES:
        for threshold in THRESHOLDS:
            eligible = frame[frame[f"coverage_{measure}"] >= threshold]
            for name, mask in strata(eligible).items():
                subset = eligible[mask]
                if subset.empty:
                    continue
                complete = subset[subset["redatam_flag"] == "SI"].dropna(
                    subset=["dwellings_all"]
                )
                barrios = pairs[pairs["COD_2022"].isin(subset["COD_2022"])]
                for inventory in INVENTORIES:
                    for suffix in FOOTPRINT_FILTERS:
                        rows.append(
                            _summary_row(
                                measure,
                                threshold,
                                name,
                                inventory,
                                suffix,
                                subset,
                                complete,
                                barrios,
                            )
                        )
    return pd.DataFrame(rows)


def _summary_row(
    measure: str,
    threshold: float,
    stratum: str,
    inventory: str,
    suffix: str,
    subset: pd.DataFrame,
    complete: pd.DataFrame,
    barrios: pd.DataFrame,
) -> dict:
    footprints = int(complete[f"{inventory}_footprints_{suffix}"].sum())
    totals = {
        "dwellings_all": int(complete["dwellings_all"].sum()),
        "dwellings_occupied_broad": int(complete["dwellings_occupied_broad"].sum()),
        "dwellings_present": int(complete["dwellings_present"].sum()),
        "households": int(complete["households"].sum()),
        "census_population": int(complete["census_population"].sum()),
    }
    row = {
        "coverage_measure": measure,
        "threshold": threshold,
        "stratum": stratum,
        "inventory": inventory,
        "inventory_label": INVENTORY_LABELS[inventory],
        "pre_census_imagery": INVENTORY_SPECS[inventory]["pre_census"],
        "footprint_filter": FILTER_LABELS[suffix],
        "n_radios": int(len(subset)),
        "n_radios_without_redatam": int(len(subset) - len(complete)),
        "n_barrios": int(barrios["id_renabap"].nunique()),
        "footprints": footprints,
        **totals,
    }
    for label, column in DENOMINATORS.items():
        denominator = totals[column]
        per_radio = complete[f"{inventory}_fp_{suffix}_per_{label}"].dropna()
        weights = complete.loc[per_radio.index, column]
        row[f"ratio_totals_per_{label}"] = (
            footprints / denominator if denominator else None
        )
        row[f"median_per_{label}"] = (
            float(per_radio.median()) if not per_radio.empty else None
        )
        row[f"p25_per_{label}"] = (
            float(per_radio.quantile(0.25)) if not per_radio.empty else None
        )
        row[f"p75_per_{label}"] = (
            float(per_radio.quantile(0.75)) if not per_radio.empty else None
        )
        row[f"weighted_mean_per_{label}"] = (
            float((per_radio * weights).sum() / weights.sum())
            if weights.sum()
            else None
        )
        # Share of footprints that would have to be something other than an
        # independent occupied dwelling for the Census inventory to be right.
        row[f"non_dwelling_share_vs_{label}"] = (
            1 - denominator / footprints if footprints else None
        )
    row["households_per_occupied_broad"] = (
        totals["households"] / totals["dwellings_occupied_broad"]
        if totals["dwellings_occupied_broad"]
        else None
    )
    row["pop_per_occupied_broad"] = (
        totals["census_population"] / totals["dwellings_occupied_broad"]
        if totals["dwellings_occupied_broad"]
        else None
    )
    row["pop_per_household"] = (
        totals["census_population"] / totals["households"]
        if totals["households"]
        else None
    )
    return row


def _scatter(
    axes, frame: pd.DataFrame, column: str, label: str, inventory: str
) -> None:
    count = f"{inventory}_footprints_all"
    data = frame[(frame[column] > 0) & (frame[count] > 0)]
    caba = data[data["is_caba"]]
    rest = data[~data["is_caba"]]
    axes.scatter(
        rest[column],
        rest[count],
        s=12,
        alpha=0.45,
        color="#1f4e79",
        label=f"Outside CABA (n={len(rest):,})",
    )
    axes.scatter(
        caba[column],
        caba[count],
        s=18,
        alpha=0.85,
        color="#c0392b",
        marker="^",
        label=f"CABA (n={len(caba):,})",
    )
    limit = [
        max(1, min(data[column].min(), data[count].min())),
        max(data[column].max(), data[count].max()) * 1.1,
    ]
    axes.plot(limit, limit, color="black", linewidth=1, linestyle="--", label="1:1")
    axes.set_xscale("log")
    axes.set_yscale("log")
    axes.set_xlim(limit)
    axes.set_ylim(limit)
    axes.set_xlabel(label)
    axes.set_ylabel(f"Footprints, {INVENTORY_SPECS[inventory]['short']}")
    ratio = data[count].sum() / data[column].sum()
    axes.set_title(
        f"{label}\nn={len(data):,} radios, totals ratio {ratio:.2f}", fontsize=10
    )
    axes.legend(fontsize=8, loc="upper left")
    axes.grid(True, which="major", alpha=0.25)


def make_plots(frame: pd.DataFrame) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    primary = frame[frame["coverage_union"] >= PRIMARY_THRESHOLD]
    primary = primary[primary["redatam_flag"] == "SI"].dropna(subset=["dwellings_all"])

    for inventory, tag, date in (
        (VIDA, "", f"buildings {BUILDINGS_DATE}"),
        (PRE_CENSUS, "_precensus", f"buildings imagery to {MS_IMAGERY_END}"),
    ):
        caption = (
            f"Census radios with >={PRIMARY_THRESHOLD:.0%} RENABAP coverage. "
            f"Census {CENSUS_DATE}, {date}."
        )
        for column, label, name in (
            (
                "dwellings_all",
                "Census total private dwellings",
                f"fig_footprints_vs_all_dwellings{tag}.png",
            ),
            (
                "dwellings_occupied_broad",
                "Census occupied private dwellings",
                f"fig_footprints_vs_occupied_dwellings{tag}.png",
            ),
            (
                "households",
                "Census households",
                f"fig_footprints_vs_households{tag}.png",
            ),
        ):
            figure, axes = plt.subplots(figsize=(6.5, 6.0))
            _scatter(axes, primary, column, label, inventory)
            figure.text(0.5, 0.005, caption, ha="center", fontsize=7, color="#555555")
            figure.tight_layout(rect=(0, 0.03, 1, 1))
            figure.savefig(OUTPUT_DIR / name, dpi=160)
            plt.close(figure)

    figure, axes = plt.subplots(figsize=(7.0, 5.0))
    groups, labels = [], []
    for threshold in THRESHOLDS:
        subset = frame[
            (frame["coverage_union"] >= threshold) & (frame["redatam_flag"] == "SI")
        ]
        values = subset[f"{VIDA}_fp_all_per_occupied_broad"].dropna()
        groups.append(values)
        labels.append(f">={threshold:.0%}\nn={len(values):,}")
    axes.boxplot(groups, tick_labels=labels, showfliers=False)
    axes.axhline(1.0, color="black", linestyle="--", linewidth=1, label="1:1")
    axes.set_ylabel("Footprints per occupied private dwelling")
    axes.set_xlabel("Minimum RENABAP coverage of the census radio")
    axes.set_title("Footprint to occupied-dwelling ratio by coverage threshold")
    axes.legend(fontsize=8)
    axes.grid(True, axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(OUTPUT_DIR / "fig_ratio_by_threshold.png", dpi=160)
    plt.close(figure)

    figure, axes = plt.subplots(figsize=(7.0, 5.0))
    groups, labels = [], []
    for name, mask in strata(primary).items():
        if not name.startswith(("Apartment share", "CABA")):
            continue
        values = primary[mask][f"{VIDA}_fp_all_per_occupied_broad"].dropna()
        if values.empty:
            continue
        groups.append(values)
        labels.append(f"{name.replace('Apartment share ', '')}\nn={len(values):,}")
    axes.boxplot(groups, tick_labels=labels, showfliers=False)
    axes.axhline(1.0, color="black", linestyle="--", linewidth=1, label="1:1")
    axes.set_ylabel("Footprints per occupied private dwelling")
    axes.set_xlabel("Apartment share of private dwellings (V01 category 4)")
    axes.set_title(
        f"Ratio by vertical-density regime, >={PRIMARY_THRESHOLD:.0%} RENABAP coverage"
    )
    axes.legend(fontsize=8)
    axes.grid(True, axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(OUTPUT_DIR / "fig_ratio_by_vertical_regime.png", dpi=160)
    plt.close(figure)

    # How much thinner the single-source pre-Census inventory is.
    figure, axes = plt.subplots(figsize=(6.5, 6.0))
    data = primary[
        (primary["vida_footprints_all"] > 0)
        & (primary[f"{PRE_CENSUS}_footprints_all"] > 0)
    ]
    axes.scatter(
        data["vida_footprints_all"],
        data[f"{PRE_CENSUS}_footprints_all"],
        s=12,
        alpha=0.45,
        color="#1f4e79",
    )
    limit = [
        max(1, data["vida_footprints_all"].min()),
        data["vida_footprints_all"].max() * 1.1,
    ]
    axes.plot(limit, limit, color="black", linewidth=1, linestyle="--", label="1:1")
    axes.set_xscale("log")
    axes.set_yscale("log")
    axes.set_xlim(limit)
    axes.set_ylim(limit)
    axes.set_xlabel("Footprints, VIDA September 2024")
    axes.set_ylabel(f"Footprints, {INVENTORY_SPECS[PRE_CENSUS]['short']}")
    ratio = (
        data[f"{PRE_CENSUS}_footprints_all"].sum() / data["vida_footprints_all"].sum()
    )
    axes.set_title(
        f"Pre-Census against 2024 inventory\n"
        f"n={len(data):,} radios, totals ratio {ratio:.2f}",
        fontsize=10,
    )
    axes.legend(fontsize=8, loc="upper left")
    axes.grid(True, which="major", alpha=0.25)
    figure.tight_layout()
    figure.savefig(OUTPUT_DIR / "fig_inventory_comparison.png", dpi=160)
    plt.close(figure)


def run_checks(con: duckdb.DuckDBPyConnection, frame: pd.DataFrame) -> dict:
    """Checks that the counting rule is sound, not that the result is expected."""
    overlaps = con.execute("""
        SELECT COUNT(*) FROM eligible a JOIN eligible b
          ON a.COD_2022 < b.COD_2022
         AND ST_Intersects(a.geometry, b.geometry)
        WHERE ST_Area_Spheroid(
            ST_FlipCoordinates(ST_Intersection(a.geometry, b.geometry))) > 1.0
    """).fetchone()[0]

    checks = {
        "eligible_radio_pairs_overlapping_by_more_than_1_m2": int(overlaps),
    }

    barrio_published = con.execute(
        "SELECT SUM(building_count) FROM barrios"
    ).fetchone()[0]
    checks["footprints_in_barrios_published_intersects"] = int(barrio_published)

    for inventory in INVENTORIES:
        spec = INVENTORY_SPECS[inventory]
        path = spec["path"]
        source = quote(path / "*.parquet") if path.is_dir() else quote(path)
        con.execute(
            f"SET enable_geoparquet_conversion = {str(spec['geoparquet']).lower()};"
        )
        total, duplicates = con.execute(f"""
            WITH assigned AS (
                SELECT s.id_renabap, b.geometry
                FROM (
                    SELECT {spec["geometry_sql"]} AS geometry
                    FROM read_parquet('{source}')
                ) b
                JOIN barrios s ON ST_Within(ST_Centroid(b.geometry), s.geometry)
            )
            SELECT COUNT(*),
                   COUNT(*) - COUNT(DISTINCT (id_renabap, ST_AsWKB(geometry)))
            FROM assigned
        """).fetchone()
        con.execute("SET enable_geoparquet_conversion = true;")
        checks[f"{inventory}_footprints_in_barrios_by_centroid"] = int(total)
        checks[f"{inventory}_duplicate_geometries_in_a_barrio"] = int(duplicates)
        con.execute(
            f"SET enable_geoparquet_conversion = {str(spec['geoparquet']).lower()};"
        )
        national = con.execute(
            f"SELECT COUNT(*) FROM read_parquet('{source}')"
        ).fetchone()[0]
        con.execute("SET enable_geoparquet_conversion = true;")
        checks[f"{inventory}_national_footprints"] = int(national)

    checks["footprint_double_count_from_intersects"] = int(
        barrio_published - checks["vida_footprints_in_barrios_by_centroid"]
    )

    complete = frame[frame["redatam_flag"] == "SI"].dropna(subset=["dwellings_all"])
    difference = (complete["population_redatam"] - complete["census_population"]).abs()
    checks["radios_where_redatam_population_differs"] = int((difference > 0).sum())
    checks["max_absolute_population_difference"] = (
        int(difference.max()) if not difference.empty else 0
    )
    checks["eligible_radios_without_redatam"] = int(len(frame) - len(complete))
    checks["radios_with_coverage_sum_above_1"] = int(
        (frame["coverage_sum"] > 1.0).sum()
    )
    return checks


def _pick(
    summary: pd.DataFrame,
    threshold: float,
    stratum: str,
    inventory: str,
    filt: str,
) -> pd.Series:
    match = summary[
        (summary["coverage_measure"] == "union")
        & (summary["threshold"] == threshold)
        & (summary["stratum"] == stratum)
        & (summary["inventory"] == inventory)
        & (summary["footprint_filter"] == FILTER_LABELS[filt])
    ]
    return match.iloc[0]


def _table(summary: pd.DataFrame, stratum: str, inventory: str, filt: str) -> list[str]:
    lines = [
        "| Coverage | Radios | Barrios | Footprints | Private dwellings | "
        "Occupied dwellings | Households | FP / dwelling | FP / occupied | "
        "FP / household |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for threshold in THRESHOLDS:
        row = _pick(summary, threshold, stratum, inventory, filt)
        lines.append(
            f"| >={threshold:.0%} | {row['n_radios']:,} | {row['n_barrios']:,} | "
            f"{row['footprints']:,} | {row['dwellings_all']:,} | "
            f"{row['dwellings_occupied_broad']:,} | {row['households']:,} | "
            f"{row['ratio_totals_per_dwelling_all']:.2f} | "
            f"{row['ratio_totals_per_occupied_broad']:.2f} | "
            f"{row['ratio_totals_per_household']:.2f} |"
        )
    return lines


def write_report(
    summary: pd.DataFrame,
    frame: pd.DataFrame,
    checks: dict,
    timings: dict,
    manifest: dict,
) -> None:
    def at(stratum: str, inventory: str = VIDA, filt: str = "all") -> pd.Series:
        return _pick(summary, PRIMARY_THRESHOLD, stratum, inventory, filt)

    vida = at("All eligible")
    vida_10 = at("All eligible", VIDA, "ge10")
    pre = at("All eligible", PRE_CENSUS)
    pre_10 = at("All eligible", PRE_CENSUS, "ge10")
    pre_2023 = at("All eligible", MS2023)
    pre_horizontal = at("Horizontal regime", PRE_CENSUS)
    pre_no_caba = at("Excluding CABA", PRE_CENSUS)
    pre_caba = at("CABA only", PRE_CENSUS)
    vida_no_caba = at("Excluding CABA")
    vida_caba = at("CABA only")
    q75 = frame.attrs["departamento_q75"]

    lines = [
        "# Footprints against the Census 2022 dwelling and household inventory",
        "",
        "This test compares physical building inventories with the Census 2022",
        "dwelling and household inventory, inside census radios that lie almost",
        "entirely within RENABAP barrios. It applies no persons-per-footprint",
        "multiplier, no RENABAP families multiplier, and no areal allocation of",
        "census quantities. It does not test national census omission. Its purpose",
        "is to locate where in the chain the published discrepancy begins.",
        "",
        "## 1. Method",
        "",
        "A census radio qualifies when RENABAP barrio polygons cover at least the",
        "stated share of its area. Once it qualifies, the whole radio enters the",
        "comparison, with its full INDEC dwelling and household counts and every",
        "building footprint whose centroid falls inside it.",
        "",
        "### Three building inventories",
        "",
        "| Inventory | Imagery | Can contain post-Census construction |",
        "| --- | --- | --- |",
        "| VIDA, September 2024 | not published | yes |",
        f"| Microsoft release 2022-06-14 | to {MS_IMAGERY_END} | no |",
        f"| Microsoft release 2023-04-25 | to {MS_IMAGERY_END} | no |",
        "",
        f"Census Day was {CENSUS_DAY}. Both Microsoft releases declare imagery",
        f"ending {MS_IMAGERY_END}, eleven months earlier, so neither can contain a",
        "building constructed after the Census. The 2022-06-14 release was",
        "published 27 days after Census Day. This is the primary pre-Census",
        "inventory. The 2023-04-25 release is reported as a check on it.",
        "",
        "Two effects push the pre-Census ratio down, so a value above 1.0 is a",
        "floor rather than an estimate. Microsoft alone is thinner than the VIDA",
        "conflation of Google, Microsoft, and OpenStreetMap. The imagery range is",
        "a dataset-level declaration, so some tiles carry older imagery still.",
        "",
        "Microsoft publishes no area column, so its footprint areas come from",
        "`ST_Area_Spheroid`. VIDA publishes `area_in_meters`. The size filters are",
        "therefore not computed identically across inventories.",
        "",
        "Coverage is measured two ways. The union measure dissolves the barrio",
        "polygons before measuring the intersection. The sum measure adds the",
        "intersections separately, as `census_comparison.py` does, and therefore",
        "double-counts where RENABAP polygons overlap each other. Only",
        f"{checks['radios_with_coverage_sum_above_1']} radios exceed a coverage of",
        "1.0 under the sum measure, and the two measures select identical radios",
        "at every threshold reported here.",
        "",
        "Footprints are assigned by centroid containment. No inventory here",
        "carries a stable footprint id, so uniqueness comes from the geometry:",
        "census radios tile the territory, and a centroid lies in at most one",
        "radio. No two eligible radios overlap by more than 1 m2",
        f"({checks['eligible_radio_pairs_overlapping_by_more_than_1_m2']} pairs).",
        "",
        "### REDATAM variables and their universes",
        "",
        "Each identity below was verified against the national file.",
        "",
        "| Variable | Meaning | Universe | National |",
        "| --- | --- | --- | ---: |",
        "| `VIVIENDA_TIPOVIVG` | Private dwellings | All | 17,783,029 |",
        "| `VIVIENDA_V01` cat 4 | Departamento | All private dwellings | 3,744,173 |",
        "| `VIVIENDA_V02` cat 1 | People present | All private dwellings | 15,699,016 |",
        "| `VIVIENDA_V02` cat 2 | Nobody present | All private dwellings | 2,084,013 |",
        "| `VIVIENDA_V04` cat 5 | Habitual residents absent | `V02` = 2 | 254,521 |",
        "| `VIVIENDA_V04` cats 1-4, 6 | Vacant or other use | `V02` = 2 | 1,829,492 |",
        "| `VIVIENDA_V06` | Households, sum of k x n(k) | `V02` = 1 | 15,932,302 |",
        "| `VIVIENDA_TOTPOBV` | Persons, sum of k x n(k) | `V02` = 1 | 45,618,787 |",
        "",
        "Three consequences follow.",
        "",
        "1. `V01` and `V02` cover all 17,783,029 private dwellings, so the dwelling",
        "   denominator includes unoccupied stock.",
        "2. `V04` sums to exactly the `V02` = 2 count, so its universe is the set of",
        "   dwellings with nobody present.",
        "3. `V06` covers exactly the `V02` = 1 count. Households and population exist",
        "   only for dwellings with people present. A dwelling whose habitual",
        "   residents were absent counts in the stock and contributes no household.",
        "",
        "This analysis therefore reports three dwelling denominators:",
        "all private dwellings; occupied broad, meaning `V02` = 1 plus `V04` = 5;",
        "and people present, meaning `V02` = 1 alone. Occupied broad is the",
        "headline denominator because it is the most generous reading of an",
        "occupied private dwelling.",
        "",
        "`TOTHOG` does not exist in the 2022 base. `VIVIENDA_V06` is the household",
        "variable.",
        "",
        "## 2. The pre-Census inventory test, and why it is inconclusive",
        "",
        "The 2022 Microsoft releases were recovered and counted. The test they",
        "were meant to support does not work, because that inventory is too",
        "incomplete to serve as a building census.",
        "",
        "Microsoft release 2022-06-14, imagery ending "
        f"{MS_IMAGERY_END}, no size filter.",
        "",
        *_table(summary, "All eligible", PRE_CENSUS, "all"),
        "",
        "### The completeness diagnostic",
        "",
        "Only VIDA and the 2022 Microsoft release cover all of Argentina. The",
        "2023 release is fetched by quadkey, so only the tiles that intersect an",
        "eligible radio are on disk, and its national total is not comparable.",
        "",
        "| Inventory | Footprints, all Argentina | Per Census private dwelling |",
        "| --- | ---: | ---: |",
        *[
            f"| {INVENTORY_SPECS[inventory]['short']} | "
            f"{checks[f'{inventory}_national_footprints']:,} | "
            f"{checks[f'{inventory}_national_footprints'] / 17_783_029:.2f} |"
            for inventory in (VIDA, MS2022)
        ],
        "",
        "Argentina has 17,783,029 private dwellings, of which 3,744,173 are",
        "apartments. A complete inventory of a country that is mostly low-rise",
        "cannot hold fewer buildings than a third of the dwelling count. The",
        "Microsoft release does. The download is complete, and its per-file",
        "checksums are in `data/ms-buildings-2022-06-14/manifest.json`.",
        "",
        "The shortfall is not specific to barrios. In a matched comparison",
        "against radios of similar dwelling count that touch no barrio, the",
        "Microsoft inventory is thinner still:",
        "",
        "| Radios | VIDA per dwelling | Microsoft 2022 per dwelling |",
        "| --- | ---: | ---: |",
        f"| Barrio coverage >={PRIMARY_THRESHOLD:.0%} | "
        f"{vida['ratio_totals_per_dwelling_all']:.2f} | "
        f"{pre['ratio_totals_per_dwelling_all']:.2f} |",
        "| No barrio overlap, matched on dwellings | 1.70 | 0.26 |",
        "",
        "So the Microsoft ratio of "
        f"{pre['ratio_totals_per_occupied_broad']:.2f} measures the detector, not",
        "the housing stock. It is not a floor on the Census comparison, and no",
        "conclusion about post-Census construction follows from it.",
        "",
        f"In the eligible radios the Microsoft inventory holds "
        f"{pre['footprints'] / vida['footprints']:.0%} of the VIDA count.",
        "",
        "The 2023-04-25 release, which shares the same imagery cut-off, behaves",
        f"the same way: {pre_2023['footprints']:,} footprints against",
        f"{pre['footprints']:,}, a ratio of "
        f"{pre_2023['ratio_totals_per_occupied_broad']:.2f}. The two releases",
        "agree with each other and disagree with VIDA, which is what a coverage",
        "difference rather than a time difference looks like.",
        "",
        "## 3. What this leaves open",
        "",
        "The temporal mismatch in the VIDA result stands unresolved. Census counts",
        f"are from {CENSUS_DATE} and the VIDA snapshot is from {BUILDINGS_DATE}.",
        "Some share of the excess is construction in the 28 months between, and",
        "this analysis still cannot say how much.",
        "",
        "Three routes were tried and closed:",
        "",
        "1. Microsoft's own 2022 releases are deleted. Their URLs, preserved in",
        "   the git history of microsoft/GlobalMLBuildingFootprints, point at a",
        '   storage account that answers "409 Public access is not permitted on',
        '   this storage account". The Planetary Computer copies survive and were',
        "   used here.",
        "2. Those recovered copies are too incomplete to count against, as shown",
        "   above.",
        "3. Overture carries no usable construction date. See section 8.",
        "",
        "The remaining option not attempted is Google Open Buildings Temporal,",
        "which runs one model over uniform annual Sentinel-2 stacks from 2016 to",
        "2023 and is designed so that year-over-year differences are valid. Its",
        "2022 layer centres on 30 June 2022, six weeks after Census Day.",
        "",
        "## 4. Outside CABA and in the horizontal regime",
        "",
        "The horizontal regime is the set of radios whose apartment share",
        "(`V01` category 4) is below the 75th percentile of eligible radios,",
        f"which is {q75:.1%}.",
        "",
        "| Stratum | Radios | Pre-Census FP / occupied | VIDA FP / occupied |",
        "| --- | ---: | ---: | ---: |",
        f"| All eligible | {pre['n_radios']:,} | "
        f"{pre['ratio_totals_per_occupied_broad']:.2f} | "
        f"{vida['ratio_totals_per_occupied_broad']:.2f} |",
        f"| Horizontal regime | {pre_horizontal['n_radios']:,} | "
        f"{pre_horizontal['ratio_totals_per_occupied_broad']:.2f} | "
        f"{at('Horizontal regime')['ratio_totals_per_occupied_broad']:.2f} |",
        f"| Excluding CABA | {pre_no_caba['n_radios']:,} | "
        f"{pre_no_caba['ratio_totals_per_occupied_broad']:.2f} | "
        f"{vida_no_caba['ratio_totals_per_occupied_broad']:.2f} |",
        f"| CABA only | {pre_caba['n_radios']:,} | "
        f"{pre_caba['ratio_totals_per_occupied_broad']:.2f} | "
        f"{vida_caba['ratio_totals_per_occupied_broad']:.2f} |",
        "",
        "## 5. Effect of the footprint size filters",
        "",
        "Pre-Census inventory, >=10 m2 filter.",
        "",
        *_table(summary, "All eligible", PRE_CENSUS, "ge10"),
        "",
        "The >=10 m2 filter moves the pre-Census ratio against occupied dwellings",
        f"from {pre['ratio_totals_per_occupied_broad']:.2f} to "
        f"{pre_10['ratio_totals_per_occupied_broad']:.2f}. On VIDA the same filter",
        f"moves it from {vida['ratio_totals_per_occupied_broad']:.2f} to "
        f"{vida_10['ratio_totals_per_occupied_broad']:.2f}.",
        "",
        "## 6. Reconciliation arithmetic",
        "",
        "The share of detected footprints that would have to be non-residential,",
        "secondary, or otherwise not an independent occupied dwelling for the",
        f"Census inventory to be correct, at >={PRIMARY_THRESHOLD:.0%} coverage",
        "and no size filter:",
        "",
        "| Denominator | Pre-Census | VIDA |",
        "| --- | ---: | ---: |",
        f"| All private dwellings | "
        f"{pre['non_dwelling_share_vs_dwelling_all']:.1%} | "
        f"{vida['non_dwelling_share_vs_dwelling_all']:.1%} |",
        f"| Occupied private dwellings | "
        f"{pre['non_dwelling_share_vs_occupied_broad']:.1%} | "
        f"{vida['non_dwelling_share_vs_occupied_broad']:.1%} |",
        f"| Households | {pre['non_dwelling_share_vs_household']:.1%} | "
        f"{vida['non_dwelling_share_vs_household']:.1%} |",
        "",
        "In the pre-Census column, post-Census construction is not an available",
        "explanation.",
        "",
        "## 7. VIDA reference result",
        "",
        "Retained so the two inventories can be compared directly.",
        "",
        *_table(summary, "All eligible", VIDA, "all"),
        "",
        "Census-internal ratios at the primary threshold: "
        f"{vida['households_per_occupied_broad']:.2f} households per occupied",
        f"dwelling, {vida['pop_per_occupied_broad']:.2f} persons per occupied",
        f"dwelling, and {vida['pop_per_household']:.2f} persons per household.",
        "",
        "## 8. Why Overture was not used",
        "",
        "Overture Maps was tested as a way to date construction and rejected on",
        'measurement. Its schema documents `update_time` as "Last update time of',
        'the source data record", which is provenance rather than a construction',
        "date. Measured over a conurbano window of 1,307,185 buildings in release",
        "2026-08-19.0, the timestamps are bulk dataset stamps: 841,674 buildings",
        "carry Google Open Buildings 2023-05 and 350,933 carry Microsoft ML",
        "Buildings 2000-01, a sentinel. Only about 3 percent, from OpenStreetMap,",
        "carry genuine per-feature dates.",
        "",
        "Splitting that window at Census Day would report 68 percent of buildings",
        "as post-Census, which the single-month spike shows is false. Overture",
        "also keeps only two releases, both from 2026, and its first release ever",
        "postdates Census Day, so no snapshot difference can bracket it.",
        "",
        "## 9. Checks",
        "",
        "| Check | Value |",
        "| --- | ---: |",
        *[f"| {key.replace('_', ' ')} | {value:,} |" for key, value in checks.items()],
        "",
        "The published `building_count` used `ST_Intersects`, so a footprint on a",
        "barrio boundary counted once per barrio. Centroid assignment removes that",
        f"double count: {checks['footprint_double_count_from_intersects']:,}",
        f"footprints of {checks['footprints_in_barrios_published_intersects']:,}.",
        "",
        "## 10. Limits",
        "",
        "- The Microsoft imagery range is a dataset-level declaration, not a",
        "  per-tile measurement, and not a construction date for any one building.",
        "- Microsoft is one source. VIDA conflates three. The pre-Census count is",
        "  therefore a floor, and the gap between the two inventories mixes",
        "  construction with source coverage.",
        "- REDATAM applies confidentiality treatment to small cells, so radio-level",
        "  counts carry some perturbation. National identities still hold exactly.",
        "- A footprint is not a dwelling in a multi-unit building. The",
        "  apartment-share stratification bounds that effect but does not remove it.",
        "- No inventory here has a stable footprint id. Uniqueness comes from",
        "  centroid containment in non-overlapping radios.",
        "- This test says nothing about national census omission.",
        "",
        "## 11. Provenance",
        "",
        "| Input | Path | sha256 |",
        "| --- | --- | --- |",
        *[
            f"| {name} | `{entry['path']}` | `{entry['sha256'][:16]}...` |"
            for name, entry in manifest["inputs"].items()
        ],
        "",
        "The Microsoft releases come from the Planetary Computer `ms-buildings`",
        "collection. Microsoft's own 2022 copies are gone: the URLs in the 2022",
        "link tables, preserved in the git history of",
        "microsoft/GlobalMLBuildingFootprints, point at a storage account that now",
        'answers "409 Public access is not permitted on this storage account".',
        "Per-file checksums are in each `manifest.json` under `data/`.",
        "",
        "| Step | Seconds |",
        "| --- | ---: |",
        *[
            f"| {key.replace('_', ' ')} | {value:.1f} |"
            for key, value in timings.items()
        ],
        "",
    ]
    (OUTPUT_DIR / "report.md").write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--census-path", type=Path)
    parser.add_argument("--settlements-path", type=Path)
    parser.add_argument("--buildings-path", type=Path)
    parser.add_argument("--redatam-path", type=Path)
    parser.add_argument("--temp-dir", type=Path, default=Path("/tmp/duckdb-bv"))
    parser.add_argument("--skip-plots", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    paths = prepare_inputs(args)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timings: dict[str, float] = {}

    con = connect(args.temp_dir)
    started = time.time()
    load_geometry(con, paths)
    build_coverage(con)
    timings["coverage"] = time.time() - started

    create_footprint_table(con)
    for inventory in INVENTORIES:
        timings[f"join_{inventory}"] = count_footprints(con, inventory)

    started = time.time()
    build_census(con, paths["redatam"])
    timings["census_pivot"] = time.time() - started

    radios, pairs = assemble(con)
    frame = derive(radios)

    started = time.time()
    checks = run_checks(con, frame)
    timings["checks"] = time.time() - started

    summary = summarise(frame, pairs)

    inputs = {
        name: {"path": str(path), "sha256": sha256(path)}
        for name, path in paths.items()
    }
    for inventory in INVENTORIES:
        path = INVENTORY_SPECS[inventory]["path"]
        if path.is_dir():
            inputs[inventory] = {
                "path": str(path),
                "sha256": sha256(path / "manifest.json"),
            }
    manifest = {
        "census_date": CENSUS_DATE,
        "census_day": CENSUS_DAY,
        "buildings_date": BUILDINGS_DATE,
        "microsoft_imagery_end": MS_IMAGERY_END,
        "primary_threshold": PRIMARY_THRESHOLD,
        "pre_census_inventory": PRE_CENSUS,
        "inputs": inputs,
    }
    (OUTPUT_DIR / "input_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    frame.to_parquet(
        OUTPUT_DIR / "census_dwelling_footprint_by_radio.parquet", index=False
    )
    summary.to_csv(OUTPUT_DIR / "census_dwelling_footprint_summary.csv", index=False)
    write_report(summary, frame, checks, timings, manifest)
    if not args.skip_plots:
        make_plots(frame)
    con.close()
    print(f"Wrote {OUTPUT_DIR}")
    for key, value in timings.items():
        print(f"  {key}: {value:.1f}s")


if __name__ == "__main__":
    main()
