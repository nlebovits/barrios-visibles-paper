#!/usr/bin/env python3
"""Render example maps of census radios that lie inside RENABAP barrios.

Each map shows one radio, the barrio polygons it falls inside, and every VIDA
building footprint whose centroid lies in the radio. The footprint count and
the INDEC household count are printed together, so the gap between the physical
inventory and the census inventory is visible in a single frame.

Styling follows the settlement maps in the published article: Esri World
Imagery under an orange footprint outline, a white dashed radio boundary, a
scale bar, and a north arrow. The barrio boundary is drawn in a third colour.

Footprint selection repeats census_dwelling_footprint.py exactly. A footprint
belongs to the radio that contains its centroid.

Usage:

    pixi run tract-examples
"""

from __future__ import annotations

import argparse
from pathlib import Path

import contextily as cx
import duckdb
import geopandas as gpd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib_map_utils import north_arrow, scale_bar

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs" / "tract-examples"

CENSUS_PATH = Path("/home/nissim/Documents/dev/arg-bp-map/radios-hilbert.parquet")
SETTLEMENTS_PATH = Path("/home/nissim/Documents/dev/arg-bp-map/barrios-hilbert.parquet")
BUILDINGS_PATH = DATA_DIR / "buildings_arg.parquet"
RADIO_TABLE = (
    ROOT
    / "outputs"
    / "census-dwelling-footprint"
    / ("census_dwelling_footprint_by_radio.parquet")
)

WEB_MERCATOR_CRS = "EPSG:3857"
DEFAULT_FIGSIZE = (12, 10)
MARGIN_M = 50

# Same plasma stops the article uses. 0.8 is the orange the footprints carry.
PLASMA = plt.cm.plasma
FOOTPRINT_COLOR = PLASMA(0.8)
RADIO_COLOR = "white"
BARRIO_COLOR = "#00e5ff"

ATTRIBUTION = (
    "Datos: RENABAP (2023), INDEC (2022), VIDA (2024) | Mapa base: Esri (2025)"
)

# Four radios at or above 99% RENABAP coverage, each inside a single barrio,
# drawn from four provinces. See outputs/census-dwelling-footprint/report.md
# for the full set of 738 radios at the 95% threshold.
EXAMPLES = ("221402006", "620070622", "900844212", "064970507")


def load_frames(codes: tuple[str, ...]) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
    radios = gpd.read_parquet(CENSUS_PATH)
    radios = radios[radios["COD_2022"].isin(codes)].to_crs(WEB_MERCATOR_CRS)
    if len(radios) != len(codes):
        missing = set(codes) - set(radios["COD_2022"])
        raise RuntimeError(f"Radios not found: {sorted(missing)}")
    barrios = gpd.read_parquet(SETTLEMENTS_PATH).to_crs(WEB_MERCATOR_CRS)
    return radios, barrios


def load_footprints(radio: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Every VIDA footprint whose centroid falls inside the radio."""
    wgs84 = radio.to_crs("EPSG:4326")
    wkt = wgs84.geometry.iloc[0].wkt
    minx, miny, maxx, maxy = wgs84.total_bounds
    con = duckdb.connect()
    con.execute("INSTALL spatial; LOAD spatial;")
    frame = con.execute(
        f"""
        SELECT ST_AsWKB(geometry) AS geometry
        FROM read_parquet('{BUILDINGS_PATH}')
        WHERE bbox.xmin BETWEEN {minx} AND {maxx}
          AND bbox.ymin BETWEEN {miny} AND {maxy}
          AND ST_Within(ST_Centroid(geometry), ST_GeomFromText('{wkt}'));
        """
    ).df()
    con.close()
    return gpd.GeoDataFrame(
        geometry=gpd.GeoSeries.from_wkb(frame["geometry"].map(bytes)),
        crs="EPSG:4326",
    ).to_crs(WEB_MERCATOR_CRS)


def scalebar_max(width_m: float) -> int:
    """Round bar length: about a fifth of the frame, on a 1-2-5 ladder."""
    target = width_m / 5.0
    for step in (50, 100, 200, 250, 500, 1000, 2000):
        if target <= step:
            return step
    return 2000


def draw(
    radio: gpd.GeoDataFrame,
    barrios: gpd.GeoDataFrame,
    footprints: gpd.GeoDataFrame,
    households: int,
    coverage: float,
    path: Path,
) -> None:
    figure, axes = plt.subplots(figsize=DEFAULT_FIGSIZE)

    bounds = radio.total_bounds
    axes.set_xlim(bounds[0] - MARGIN_M, bounds[2] + MARGIN_M)
    axes.set_ylim(bounds[1] - MARGIN_M, bounds[3] + MARGIN_M)

    cx.add_basemap(
        axes,
        crs=WEB_MERCATOR_CRS,
        source=cx.providers.Esri.WorldImagery,
        attribution=ATTRIBUTION,
    )

    footprints.plot(ax=axes, facecolor="none", edgecolor=FOOTPRINT_COLOR, linewidth=1)
    barrios.plot(
        ax=axes,
        facecolor="none",
        edgecolor=BARRIO_COLOR,
        linewidth=2.5,
        zorder=9,
    )
    radio.plot(
        ax=axes,
        facecolor="none",
        edgecolor=RADIO_COLOR,
        linewidth=3,
        linestyle="--",
        zorder=10,
    )

    cx.add_basemap(
        axes,
        crs=WEB_MERCATOR_CRS,
        source=cx.providers.CartoDB.PositronOnlyLabels,
        attribution="",
    )

    scale_bar(
        ax=axes,
        location="upper left",
        style="ticks",
        bar={
            "projection": "axis",
            "minor_type": "none",
            "tickcolors": "white",
            "basecolors": "white",
            "max": scalebar_max(bounds[2] - bounds[0]),
        },
        labels={"style": "first_last", "textcolors": ["white"], "stroke_width": 0},
        units={"label": "m", "textcolor": "white", "stroke_width": 0},
    )
    north_arrow(
        axes,
        location="upper right",
        scale=0.3,
        rotation={"degrees": 0},
        base={"facecolor": "none", "edgecolor": "white", "linewidth": 1},
        fancy=True,
        shadow=True,
        label=False,
    )

    name = barrios["nombre_barrio"].iloc[0]
    place = f"{barrios['departamento'].iloc[0]}, {barrios['provincia'].iloc[0]}"
    figure.suptitle(f"Barrio {name} - {place}", fontsize=16, fontweight="bold", y=0.98)
    axes.set_title(
        f"Census radio {radio['COD_2022'].iloc[0]}, "
        f"{coverage * 100:.0f}% inside RENABAP\n"
        f"INDEC households: {households:,} | "
        f"Building footprints: {len(footprints):,} | "
        f"{households / len(footprints):.2f} households per footprint",
        fontsize=12,
        style="italic",
        pad=30,
    )

    axes.set_xticks([])
    axes.set_yticks([])
    axes.set_xlabel("")
    axes.set_ylabel("")
    for side in ("top", "right", "bottom", "left"):
        axes.spines[side].set_visible(False)

    handles = [
        Line2D(
            [0],
            [0],
            color=RADIO_COLOR,
            linewidth=3,
            linestyle="--",
            label="Census radio",
        ),
        Line2D([0], [0], color=BARRIO_COLOR, linewidth=2.5, label="RENABAP barrio"),
        Line2D(
            [0], [0], color=FOOTPRINT_COLOR, linewidth=1, label="Building footprint"
        ),
    ]
    axes.legend(handles=handles, loc="lower right", bbox_to_anchor=(1.0, 0.02))

    figure.tight_layout()
    figure.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codes", nargs="*", default=list(EXAMPLES))
    args = parser.parse_args()
    codes = tuple(args.codes)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    table = gpd.pd.read_parquet(RADIO_TABLE).set_index("COD_2022")
    radios, barrios = load_frames(codes)

    for code in codes:
        radio = radios[radios["COD_2022"] == code]
        row = table.loc[code]
        touching = barrios[barrios.intersects(radio.geometry.iloc[0])]
        footprints = load_footprints(radio)
        path = OUTPUT_DIR / f"fig_tract_{code}.png"
        draw(
            radio=radio,
            barrios=touching,
            footprints=footprints,
            households=int(row["households"]),
            coverage=float(row["coverage_union"]),
            path=path,
        )
        print(
            f"{code}: {len(footprints):,} footprints, "
            f"{int(row['households']):,} households -> {path}"
        )


if __name__ == "__main__":
    main()
