#!/usr/bin/env python3
"""
Argentina Informal Settlement Population Estimation — end-to-end.

Runs the full pipeline in one shot, with per-phase timing:

    download  ->  geoparquet-io optimization  ->  spatial-join query  ->  export

Estimates household counts in informal settlements by joining satellite-derived
building footprints to official RENABAP settlement boundaries.

Logic: max(building_count × occupation_rate × 1.1, renabap_families) per settlement.
- 1.1 = RENABAP's families-per-dwelling multiplier (SISU 2023a pp. 14-15)
- Occupation rate discounts building counts only (familias_aproximadas is enumerated)

Includes sensitivity analysis across:
- Building size filters (none, ≥6m², ≥10m²)
- Occupation rates (85%, 90%, 95%, 100%)
- Population multipliers (2.8, 3.35)

Data sources:
- RENABAP boundaries: argentina.gob.ar GeoJSON (downloaded, then gpio-optimized)
- Buildings: Google/MS/OSM Open Buildings via VIDA on Source Cooperative
  (downloaded, then gpio-optimized: bbox column + Hilbert order + ideal row groups)
- Urban areas: IGN Planta Urbana polygons (local file; see URBAN_AREAS_PATH)

Optimization rationale: the raw VIDA national file is not spatially organized for a
join like this. gpio re-writes it with a bbox column, Hilbert-curve row ordering, and
ideal row-group sizes so DuckDB can prune row groups during the spatial join.

Output:
- Per-settlement GeoJSON: ~/Documents/settlement_estimates.geojson
- Summary markdown: ~/Documents/settlement_analysis_summary.md

Run with: pixi run python estimate.py
"""

import time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

import duckdb
import geoparquet_io as gpio
import requests

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
DATA_DIR = Path(__file__).resolve().parent / "data"
DOWNLOADS = Path.home() / "Downloads"

# RENABAP: downloaded GeoJSON, then gpio-optimized parquet
RENABAP_GEOJSON = DATA_DIR / "renabap-2023-12-06.geojson"
RENABAP_PATH = DATA_DIR / "renabap.parquet"

# Buildings: raw VIDA national file (cached download), then gpio-optimized parquet
BUILDINGS_RAW = DOWNLOADS / "ARG.parquet"
BUILDINGS_PATH = DATA_DIR / "buildings_arg.parquet"

# Urban areas: local-only (no public URL wired). if-not-exists guard below.
URBAN_AREAS_PATH = DOWNLOADS / "areas_de_asentamientos_y_edificios_020105.parquet"

OUTPUT_GEOJSON = Path.home() / "Documents/settlement_estimates.geojson"
OUTPUT_MD = Path.home() / "Documents/settlement_analysis_summary.md"

# --------------------------------------------------------------------------- #
# Download sources
# --------------------------------------------------------------------------- #
RENABAP_URL = (
    "https://www.argentina.gob.ar/sites/default/files/renabap-2023-12-06.geojson"
)
VIDA_URL = (
    "https://data.source.coop/vida/google-microsoft-open-buildings/"
    "geoparquet/by_country/country_iso=ARG/ARG.parquet"
)

# --------------------------------------------------------------------------- #
# Sensitivity analysis parameters
# --------------------------------------------------------------------------- #
BUILDING_SIZE_FILTERS = [
    (None, "No filter"),
    (6, "≥6 m²"),
    (10, "≥10 m²"),
]
OCCUPATION_RATES = [0.85, 0.90, 0.95, 1.00]
POP_MULTIPLIERS = [2.8, 3.35]

# Argentina total population (2022 census)
ARGENTINA_POP = 46_700_000

# --------------------------------------------------------------------------- #
# Timing
# --------------------------------------------------------------------------- #
TIMINGS: dict[str, float] = {}


@contextmanager
def timed(label: str):
    """Time a pipeline phase, record it, and report start/finish."""
    print(f"\n▶ {label} ...")
    t0 = time.perf_counter()
    yield
    dt = time.perf_counter() - t0
    TIMINGS[label] = dt
    print(f"✓ {label} — {dt:,.1f}s")


def _fmt_bytes(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return f"{n:,.1f} {unit}"
        n /= 1024


def _stream_download(url: str, dest: Path) -> None:
    """Stream a (possibly large) file to disk with light progress reporting."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(dest.suffix + ".part")
    with requests.get(
        url, headers={"User-Agent": "Mozilla/5.0"}, stream=True, timeout=300
    ) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        done = 0
        next_mark = 0.10
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(chunk_size=8 * 1024 * 1024):
                if not chunk:
                    continue
                f.write(chunk)
                done += len(chunk)
                if total and done / total >= next_mark:
                    print(f"    {done / total:5.0%}  ({_fmt_bytes(done)})")
                    next_mark += 0.10
    tmp.rename(dest)
    print(f"    saved {_fmt_bytes(dest.stat().st_size)} -> {dest}")


# --------------------------------------------------------------------------- #
# Phase 1+2: download + gpio optimization
# --------------------------------------------------------------------------- #
def prepare_renabap() -> None:
    """Download RENABAP GeoJSON (cached) and write an optimized GeoParquet."""
    with timed("Download RENABAP boundaries"):
        if RENABAP_GEOJSON.exists():
            print(f"    cached: {RENABAP_GEOJSON}")
        else:
            _stream_download(RENABAP_URL, RENABAP_GEOJSON)

    with timed("Optimize RENABAP (gpio: bbox + Hilbert)"):
        if RENABAP_PATH.exists():
            print(f"    cached: {RENABAP_PATH}")
        else:
            (
                gpio.convert(str(RENABAP_GEOJSON))
                .add_bbox()
                .sort_hilbert()
                .write(str(RENABAP_PATH), geoparquet_version="1.1", overwrite=True)
            )


def prepare_buildings() -> None:
    """Download the national VIDA buildings file (cached) and gpio-optimize it."""
    with timed("Download VIDA national buildings"):
        if BUILDINGS_RAW.exists():
            print(
                f"    cached: {BUILDINGS_RAW} ({_fmt_bytes(BUILDINGS_RAW.stat().st_size)})"
            )
        else:
            print("    not found locally — downloading from VIDA (Source Cooperative)")
            _stream_download(VIDA_URL, BUILDINGS_RAW)

    with timed("Optimize buildings (gpio: bbox + Hilbert + row groups)"):
        if BUILDINGS_PATH.exists():
            print(f"    cached: {BUILDINGS_PATH}")
        else:
            (
                gpio.read(str(BUILDINGS_RAW))
                .add_bbox()
                .sort_hilbert()
                .write(str(BUILDINGS_PATH), geoparquet_version="1.1", overwrite=True)
            )


def check_urban_areas() -> None:
    """Urban-areas layer has no wired download URL; guard for the local file."""
    if not URBAN_AREAS_PATH.exists():
        raise FileNotFoundError(
            f"Urban-areas file not found: {URBAN_AREAS_PATH}\n"
            "No public download URL is wired for this layer. Place the IGN "
            "Planta Urbana parquet at the path above (or update URBAN_AREAS_PATH)."
        )
    print(f"    urban areas: {URBAN_AREAS_PATH}")


# --------------------------------------------------------------------------- #
# Phase 3: spatial-join query + sensitivity analysis
# --------------------------------------------------------------------------- #
def run_analysis() -> dict:
    """Run the spatial joins, sensitivity sweep, and breakdowns. Returns results."""
    con = duckdb.connect()
    con.execute("INSTALL spatial; LOAD spatial;")

    print("    spatial joins (settlements × urban areas × buildings)...")

    # Step 1: Flag settlements that intersect urban areas
    con.execute(f"""
        CREATE TABLE settlements_with_urban AS
        SELECT
            s.id_renabap,
            s.nombre_barrio as nombre,
            s.provincia,
            s.departamento,
            s.localidad,
            s.familias_aproximadas,
            s.geometry,
            CASE WHEN COUNT(u.geometry) > 0 THEN TRUE ELSE FALSE END as is_urban
        FROM '{RENABAP_PATH}' s
        LEFT JOIN '{URBAN_AREAS_PATH}' u
            ON ST_Intersects(
                ST_SetCRS(s.geometry, 'EPSG:4326'),
                ST_SetCRS(u.geometry, 'EPSG:4326')
            )
        GROUP BY
            s.id_renabap, s.nombre_barrio, s.provincia, s.departamento,
            s.localidad, s.familias_aproximadas, s.geometry
    """)

    # Step 2: Spatial join with buildings (all buildings, no filter yet)
    # We'll filter by size later for sensitivity analysis
    con.execute(f"""
        CREATE TABLE settlement_buildings_raw AS
        SELECT
            s.id_renabap,
            s.nombre,
            s.provincia,
            s.departamento,
            s.localidad,
            s.familias_aproximadas,
            s.geometry,
            s.is_urban,
            b.area_in_meters as building_area
        FROM settlements_with_urban s
        LEFT JOIN '{BUILDINGS_PATH}' b
            ON ST_Intersects(
                ST_SetCRS(b.geometry, 'EPSG:4326'),
                ST_SetCRS(s.geometry, 'EPSG:4326')
            )
    """)

    print("    sensitivity sweep across building-size filters...")

    # Step 3: Build aggregated table for each size filter
    # Logic: max(buildings, renabap_families) per settlement
    sensitivity_results = []

    for min_area, filter_label in BUILDING_SIZE_FILTERS:
        area_filter = f"AND building_area >= {min_area}" if min_area else ""

        # Aggregate building counts per settlement with this filter
        con.execute(f"""
            CREATE OR REPLACE TABLE settlement_buildings AS
            SELECT
                id_renabap,
                nombre,
                provincia,
                departamento,
                localidad,
                familias_aproximadas,
                geometry,
                is_urban,
                COUNT(building_area) as building_count
            FROM settlement_buildings_raw
            WHERE 1=1 {area_filter}
            GROUP BY
                id_renabap, nombre, provincia, departamento, localidad,
                familias_aproximadas, geometry, is_urban
        """)

        # For each occupation rate and pop multiplier, calculate estimates
        # estimated_families depends on occupation_rate, so computed per scenario
        for occ_rate in OCCUPATION_RATES:
            total_buildings = int(
                con.execute(
                    "SELECT SUM(building_count) FROM settlement_buildings"
                ).fetchone()[0]
            )
            renabap_households = int(
                con.execute(
                    "SELECT SUM(familias_aproximadas) FROM settlement_buildings"
                ).fetchone()[0]
            )

            # Apply methodology fix:
            # - building_count * occ_rate * 1.1 (occupancy + families-per-dwelling multiplier)
            # - familias_aproximadas unchanged (already enumerated families, no discount)
            # - max() selects higher of the two per settlement
            est_households = float(
                con.execute(f"""
                SELECT SUM(
                    CASE
                        WHEN building_count * {occ_rate} * 1.1 > familias_aproximadas
                        THEN building_count * {occ_rate} * 1.1
                        ELSE familias_aproximadas
                    END
                )
                FROM settlement_buildings
            """).fetchone()[0]
            )

            for pop_mult in POP_MULTIPLIERS:
                est_pop = est_households * pop_mult
                renabap_pop = renabap_households * pop_mult

                sensitivity_results.append(
                    {
                        "size_filter": filter_label,
                        "min_area": min_area,
                        "occupation": occ_rate,
                        "pop_multiplier": pop_mult,
                        "total_buildings": total_buildings,
                        "est_households": int(est_households),
                        "renabap_households": renabap_households,
                        "est_population": int(est_pop),
                        "renabap_population": int(renabap_pop),
                        "pct_of_argentina": est_pop / ARGENTINA_POP * 100,
                    }
                )

    print(f"    completed {len(sensitivity_results)} sensitivity scenarios")

    # Step 4: Rebuild final table with no filter for exports and validation
    con.execute("""
        CREATE OR REPLACE TABLE settlement_buildings AS
        SELECT
            id_renabap,
            nombre,
            provincia,
            departamento,
            localidad,
            familias_aproximadas,
            geometry,
            is_urban,
            COUNT(building_area) as building_count
        FROM settlement_buildings_raw
        GROUP BY
            id_renabap, nombre, provincia, departamento, localidad,
            familias_aproximadas, geometry, is_urban
    """)

    # Apply 1.1 multiplier (baseline: 100% occupation for exports)
    # DOUBLE because building_count * 1.1 is no longer whole-number
    con.execute("""
        ALTER TABLE settlement_buildings ADD COLUMN estimated_families DOUBLE;
        UPDATE settlement_buildings
        SET estimated_families = CASE
            WHEN building_count * 1.1 > familias_aproximadas THEN building_count * 1.1
            ELSE familias_aproximadas
        END
    """)

    # Validation: % where buildings vs RENABAP was used, by urban intersection
    # Uses multiplier-adjusted comparison (building_count * 1.1)
    print("    source breakdown by urban intersection...")

    validation_by_urban = con.execute("""
        SELECT
            is_urban,
            COUNT(*) as n_settlements,
            SUM(CASE WHEN building_count * 1.1 > familias_aproximadas THEN 1 ELSE 0 END) as used_buildings,
            SUM(CASE WHEN building_count * 1.1 <= familias_aproximadas THEN 1 ELSE 0 END) as used_renabap,
            ROUND(SUM(CASE WHEN building_count * 1.1 > familias_aproximadas THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as pct_used_buildings,
            ROUND(SUM(CASE WHEN building_count * 1.1 <= familias_aproximadas THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as pct_used_renabap
        FROM settlement_buildings
        WHERE building_count > 0
        GROUP BY is_urban
        ORDER BY is_urban DESC
    """).fetchdf()

    print("\nSource breakdown by urban intersection:")
    print(validation_by_urban.to_string(index=False))

    # Aglomerado tier analysis
    print("\n    aglomerado tier breakdown...")

    # Define conurbano partidos
    CONURBANO_PARTIDOS = [
        "La Matanza",
        "Lomas de Zamora",
        "Quilmes",
        "Moreno",
        "Merlo",
        "General San Martín",
        "Esteban Echeverría",
        "Almirante Brown",
        "Florencio Varela",
        "Lanús",
        "José C. Paz",
        "Tigre",
        "Avellaneda",
        "San Miguel",
        "Malvinas Argentinas",
        "San Isidro",
        "Berazategui",
        "Hurlingham",
        "Ituzaingó",
        "Morón",
        "Tres de Febrero",
        "Vicente López",
        "San Fernando",
        "Pilar",
        "Escobar",
        "Presidente Perón",
        "José M. Ezeiza",
    ]

    con.execute(f"""
        ALTER TABLE settlement_buildings ADD COLUMN aglomerado_tier VARCHAR;
        UPDATE settlement_buildings
        SET aglomerado_tier = CASE
            WHEN provincia = 'Ciudad Autónoma de Buenos Aires' THEN 'CABA'
            WHEN provincia = 'Buenos Aires' AND departamento IN ({",".join(f"'{p}'" for p in CONURBANO_PARTIDOS)})
                THEN 'Conurbano-AMBA'
            WHEN (provincia = 'Buenos Aires' AND departamento = 'La Plata')
                OR (provincia = 'Buenos Aires' AND departamento = 'General Pueyrredón')
                OR (provincia = 'Santa Fe' AND departamento = 'Rosario')
                OR (provincia = 'Córdoba' AND departamento = 'Capital')
                OR (provincia = 'Mendoza' AND departamento IN ('Capital', 'Godoy Cruz', 'Guaymallén', 'Las Heras', 'Maipú'))
                OR (provincia = 'Tucumán' AND departamento = 'Capital')
                THEN 'Other Gran Aglomerados'
            ELSE 'Outside Aglomerados'
        END
    """)

    by_aglomerado = con.execute("""
        SELECT
            aglomerado_tier,
            COUNT(*) as n_settlements,
            SUM(CASE WHEN familias_aproximadas > building_count * 1.1 THEN 1 ELSE 0 END) as renabap_higher,
            SUM(CASE WHEN building_count * 1.1 > familias_aproximadas THEN 1 ELSE 0 END) as footprints_higher,
            ROUND(MEDIAN(building_count * 1.1 / NULLIF(familias_aproximadas, 0)), 2) as median_ratio
        FROM settlement_buildings
        WHERE building_count > 0
        GROUP BY aglomerado_tier
        ORDER BY
            CASE aglomerado_tier
                WHEN 'CABA' THEN 1
                WHEN 'Conurbano-AMBA' THEN 2
                WHEN 'Other Gran Aglomerados' THEN 3
                ELSE 4
            END
    """).fetchdf()

    print("\nAglomerado tier breakdown:")
    print(by_aglomerado.to_string(index=False))

    # Conurbano partido breakdown (vertical density gradient)
    print("\n    conurbano partido breakdown...")

    conurbano_partidos = con.execute(f"""
        SELECT
            departamento,
            COUNT(*) as n_settlements,
            SUM(CASE WHEN familias_aproximadas > building_count * 1.1 THEN 1 ELSE 0 END) as renabap_higher,
            ROUND(SUM(CASE WHEN familias_aproximadas > building_count * 1.1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as pct_vertical
        FROM settlement_buildings
        WHERE building_count > 0
          AND provincia = 'Buenos Aires'
          AND departamento IN ({",".join(f"'{p}'" for p in CONURBANO_PARTIDOS)})
        GROUP BY departamento
        ORDER BY pct_vertical DESC
    """).fetchdf()

    print("\nConurbano vertical density by partido:")
    print(conurbano_partidos.to_string(index=False))

    # National totals (baseline: no filter, 100% occupation)
    national = con.execute("""
        SELECT
            COUNT(*) as n_settlements,
            SUM(familias_aproximadas) as total_renabap_families,
            SUM(building_count) as total_buildings,
            SUM(estimated_families) as total_estimated_families
        FROM settlement_buildings
    """).fetchone()

    # By province (uses multiplier-adjusted comparison)
    by_province = con.execute("""
        SELECT
            provincia,
            COUNT(*) as n_settlements,
            SUM(familias_aproximadas) as renabap_families,
            SUM(building_count) as building_count,
            SUM(estimated_families) as estimated_families,
            SUM(CASE WHEN building_count * 1.1 > familias_aproximadas THEN 1 ELSE 0 END) as used_buildings,
            SUM(CASE WHEN building_count * 1.1 <= familias_aproximadas THEN 1 ELSE 0 END) as used_renabap
        FROM settlement_buildings
        GROUP BY provincia
        ORDER BY estimated_families DESC
    """).fetchdf()

    return {
        "con": con,
        "sensitivity_results": sensitivity_results,
        "validation_by_urban": validation_by_urban,
        "by_aglomerado": by_aglomerado,
        "conurbano_partidos": conurbano_partidos,
        "national": national,
        "by_province": by_province,
    }


# --------------------------------------------------------------------------- #
# Phase 4: export + summary
# --------------------------------------------------------------------------- #
def export_outputs(results: dict) -> None:
    con = results["con"]
    sensitivity_results = results["sensitivity_results"]
    validation_by_urban = results["validation_by_urban"]
    by_aglomerado = results["by_aglomerado"]
    conurbano_partidos = results["conurbano_partidos"]
    national = results["national"]
    by_province = results["by_province"]

    n_settlements, renabap_fam, total_bldg, est_fam = national

    # Export per-settlement GeoJSON
    print(f"    writing {OUTPUT_GEOJSON}...")
    OUTPUT_GEOJSON.parent.mkdir(parents=True, exist_ok=True)
    con.execute(f"""
        COPY (
            SELECT
                id_renabap,
                nombre,
                provincia,
                departamento,
                localidad,
                is_urban,
                familias_aproximadas as renabap_families,
                building_count,
                estimated_families,
                CASE WHEN building_count * 1.1 > familias_aproximadas THEN 'buildings' ELSE 'renabap' END as estimate_source,
                geometry
            FROM settlement_buildings
            ORDER BY provincia, departamento, nombre
        ) TO '{OUTPUT_GEOJSON}'
        WITH (FORMAT GDAL, DRIVER 'GeoJSON')
    """)

    # Write markdown summary
    print(f"    writing {OUTPUT_MD}...")
    with open(OUTPUT_MD, "w") as f:
        f.write("# Argentina Informal Settlement Population Estimates\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("---\n\n")

        # Sensitivity Analysis Table (the main deliverable)
        f.write("## Sensitivity Analysis\n\n")
        f.write(
            "Estimated households and population across building size filters, occupation rates, and population multipliers.\n\n"
        )
        f.write(
            "| Size Filter | Occupation | Pop Mult | Buildings | Est. Households | Est. Population | % of Argentina |\n"
        )
        f.write(
            "|-------------|------------|----------|-----------|-----------------|-----------------|----------------|\n"
        )
        for r in sensitivity_results:
            f.write(
                f"| {r['size_filter']} | {r['occupation']:.0%} | {r['pop_multiplier']} | {r['total_buildings']:,} | {r['est_households']:,} | {r['est_population']:,} | {r['pct_of_argentina']:.2f}% |\n"
            )
        f.write("\n")

        # Summary range
        min_pop = min(r["est_population"] for r in sensitivity_results)
        max_pop = max(r["est_population"] for r in sensitivity_results)
        min_hh = min(r["est_households"] for r in sensitivity_results)
        max_hh = max(r["est_households"] for r in sensitivity_results)
        f.write(
            f"**Range:** {min_hh:,} – {max_hh:,} households | {min_pop:,} – {max_pop:,} population\n\n"
        )

        # Source breakdown by Urban Intersection
        f.write("## Estimate Source by Urban Intersection\n\n")
        f.write(
            "Shows which source (buildings vs RENABAP) was used per settlement, split by urban area intersection.\n\n"
        )
        f.write(
            "| Urban? | Settlements | Used Buildings | Used RENABAP | % Buildings | % RENABAP |\n"
        )
        f.write(
            "|--------|-------------|----------------|--------------|-------------|----------|\n"
        )
        for _, row in validation_by_urban.iterrows():
            urban_label = "Yes" if row["is_urban"] else "No"
            f.write(
                f"| {urban_label} | {int(row['n_settlements']):,} | {int(row['used_buildings']):,} | {int(row['used_renabap']):,} | {row['pct_used_buildings']:.1f}% | {row['pct_used_renabap']:.1f}% |\n"
            )
        f.write("\n")
        f.write(
            "*Logic: max(building_count × occ_rate × 1.1, renabap_families) per settlement*\n\n"
        )

        # Aglomerado tier analysis
        f.write("## Aglomerado Tier Analysis\n\n")
        f.write(
            "| Aglomerado Tier | N Settlements | RENABAP Higher | Footprints Higher | Median Ratio |\n"
        )
        f.write(
            "|-----------------|---------------|----------------|-------------------|-------------|\n"
        )
        for _, row in by_aglomerado.iterrows():
            f.write(
                f"| {row['aglomerado_tier']} | {int(row['n_settlements']):,} | {int(row['renabap_higher']):,} | {int(row['footprints_higher']):,} | {row['median_ratio']:.2f} |\n"
            )
        f.write("\n")
        f.write(
            "*Median ratio = footprints / RENABAP families. <1 means RENABAP captures more (vertical density).*\n\n"
        )

        # Conurbano vertical density gradient
        f.write("## Conurbano Vertical Density Gradient\n\n")
        f.write(
            "Vertical density (RENABAP > footprints) concentrates in inner-ring partidos adjacent to CABA.\n\n"
        )

        # Split into inner ring (high vertical) and outer ring (low vertical)
        inner_ring = conurbano_partidos[conurbano_partidos["pct_vertical"] >= 25].head(
            7
        )
        outer_ring = conurbano_partidos[conurbano_partidos["pct_vertical"] < 10].head(4)

        f.write("**Inner ring (adjacent to CABA):**\n\n")
        f.write("| Partido | N | RENABAP Higher | % Vertical |\n")
        f.write("|---------|---|----------------|------------|\n")
        for _, row in inner_ring.iterrows():
            f.write(
                f"| {row['departamento']} | {int(row['n_settlements'])} | {int(row['renabap_higher'])} | {row['pct_vertical']:.0f}% |\n"
            )
        f.write("\n")

        f.write("**Outer ring:**\n\n")
        f.write("| Partido | N | RENABAP Higher | % Vertical |\n")
        f.write("|---------|---|----------------|------------|\n")
        for _, row in outer_ring.iterrows():
            f.write(
                f"| {row['departamento']} | {int(row['n_settlements'])} | {int(row['renabap_higher'])} | {row['pct_vertical']:.0f}% |\n"
            )
        f.write("\n")

        f.write(
            "*Clear gradient: vertical density decays with distance from CABA. Inner-ring partidos show 40-60% vertical (nearly CABA-like), outer ring drops to <10%.*\n\n"
        )

        # National summary (baseline scenario)
        f.write("## Baseline National Summary\n\n")
        f.write("*Baseline: No building filter, 100% occupation*\n\n")
        f.write(
            "| Metric | RENABAP Official | Building-Based Estimate | Difference |\n"
        )
        f.write("|--------|------------------|------------------------|------------|\n")
        f.write(f"| Settlements | {n_settlements:,} | {n_settlements:,} | — |\n")
        f.write(f"| Building Footprints | — | {int(total_bldg):,} | — |\n")
        f.write(
            f"| Families/Households | {int(renabap_fam):,} | {int(est_fam):,} | +{int(est_fam - renabap_fam):,} (+{(est_fam / renabap_fam - 1) * 100:.1f}%) |\n"
        )

        for mult in POP_MULTIPLIERS:
            renabap_pop = renabap_fam * mult
            est_pop = est_fam * mult
            diff = est_pop - renabap_pop
            pct_arg = est_pop / ARGENTINA_POP * 100
            f.write(
                f"| Population (×{mult}) | {int(renabap_pop):,} | {int(est_pop):,} | +{int(diff):,} ({pct_arg:.1f}% of Argentina) |\n"
            )

        f.write("\n")

        # Province breakdown
        f.write("## Province Breakdown\n\n")
        f.write(
            "| Provincia | Settlements | RENABAP | Buildings | Est. Families | Used Bldg | Used RENABAP |\n"
        )
        f.write(
            "|-----------|-------------|---------|-----------|---------------|-----------|-------------|\n"
        )
        for _, row in by_province.iterrows():
            f.write(
                f"| {row['provincia']} | {int(row['n_settlements']):,} | {int(row['renabap_families']):,} | {int(row['building_count']):,} | {row['estimated_families']:,.1f} | {int(row['used_buildings']):,} | {int(row['used_renabap']):,} |\n"
            )
        f.write("\n")

        # Methodology
        f.write("## Methodology\n\n")
        f.write(
            "**Per-settlement logic:** `max(building_count × occupation_rate × 1.1, renabap_families)`\n\n"
        )
        f.write(
            "- **1.1 multiplier**: RENABAP documents ~1.1 families per dwelling (SISU 2023a pp. 14-15)\n"
        )
        f.write(
            "- **Occupation rate**: Applied only to building-derived counts, not RENABAP\n"
        )
        f.write(
            "- `familias_aproximadas` is already enumerated families, needs no discount\n"
        )
        f.write(
            "- If adjusted buildings > RENABAP → use building estimate (RENABAP undercounted)\n"
        )
        f.write(
            "- If RENABAP > adjusted buildings → use RENABAP (vertical density / multi-family)\n\n"
        )

        # Data sources
        f.write("## Data Sources\n\n")
        f.write("- **RENABAP:** Argentina Ministry of Habitat, 2023 release\n")
        f.write(
            "- **Building Footprints:** Google/Microsoft/OSM Open Buildings (VIDA, Source Cooperative)\n"
        )
        f.write("- **Urban Areas:** IGN Planta Urbana polygons\n")
        f.write(
            "- **Population multipliers:** INDEC 2022 Census (2.8), Barrios-specific estimate (3.35)\n"
        )
        f.write("\n---\n")
        f.write("\n*Analysis code: arg-informal-settlements-analysis*\n")

    con.close()


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #
def main():
    pipeline_start = time.perf_counter()

    # Phase 1+2: download + optimize
    prepare_renabap()
    prepare_buildings()
    with timed("Check urban-areas layer"):
        check_urban_areas()

    # Phase 3: query
    with timed("Spatial-join query + sensitivity analysis"):
        results = run_analysis()

    # Phase 4: export
    with timed("Export GeoJSON + markdown summary"):
        export_outputs(results)

    total = time.perf_counter() - pipeline_start

    # Timing report
    print("\n" + "=" * 60)
    print("TIMING BREAKDOWN")
    print("=" * 60)
    width = max(len(k) for k in TIMINGS)
    for label, dt in TIMINGS.items():
        print(f"  {label:<{width}}  {dt:8,.1f}s  ({dt / total:4.0%})")
    print("-" * 60)
    print(f"  {'TOTAL':<{width}}  {total:8,.1f}s")
    print("=" * 60)

    print("\nDone! Output files:")
    print(f"  - {OUTPUT_GEOJSON}")
    print(f"  - {OUTPUT_MD}")


if __name__ == "__main__":
    main()
