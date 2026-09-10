#!/usr/bin/env python3
"""Diagnostic: footprints against Census households under y x 1.1 factors.

This reads the summary that census_dwelling_footprint.py already wrote. It
recomputes nothing, changes no methodology, and leaves every existing output
in place. It adds two files of its own.

The headline analysis deliberately applies no multiplier, because its purpose
is to compare physical inventories directly. This diagnostic overlays the
paper's footprint branch: footprints are scaled by y x 1.1 for each tested
dwelling yield y (occupied dwellings per mapped footprint) before the
comparison with Census households. Both factors come from outside this
analysis and are taken as given. Treat the result as a sensitivity, not as a
second estimate. The break-even yield, at which implied households equal
Census households, is reported per stratum.

Scope: the >=95 percent RENABAP coverage sample, VIDA footprints at the
>=10 m2 filter, in two strata reported separately. The strata overlap, because
most CABA radios are already outside the horizontal regime. They are not
additive.

    pixi run diagnostic-multiplier
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
SOURCE = (
    ROOT
    / "outputs"
    / "census-dwelling-footprint"
    / "census_dwelling_footprint_summary.csv"
)
OUTPUT_DIR = ROOT / "outputs" / "census-dwelling-footprint"
STEM = "diagnostic_household_multiplier"

THRESHOLD = 0.95
FILTER = ">=10 m2"
INVENTORY = "vida"
STRATA = ("Horizontal regime", "Excluding CABA")

# Same grid as estimate.py: occupied dwellings per mapped footprint.
DWELLING_YIELDS = (0.60, 0.70, 0.85, 1.00, 1.15)
FAMILIES_PER_DWELLING = 1.1


def build() -> pd.DataFrame:
    summary = pd.read_csv(SOURCE)
    selected = summary[
        (summary["coverage_measure"] == "union")
        & (summary["threshold"] == THRESHOLD)
        & (summary["inventory"] == INVENTORY)
        & (summary["footprint_filter"] == FILTER)
        & (summary["stratum"].isin(STRATA))
    ]
    missing = set(STRATA) - set(selected["stratum"])
    if missing:
        raise RuntimeError(f"Strata absent from {SOURCE.name}: {sorted(missing)}")

    rows = []
    for name in STRATA:
        row = selected[selected["stratum"] == name].iloc[0]
        footprints = int(row["footprints"])
        dwellings = int(row["dwellings_occupied_broad"])
        households = int(row["households"])
        break_even = households / (footprints * FAMILIES_PER_DWELLING)
        for dwelling_yield in DWELLING_YIELDS:
            combined = dwelling_yield * FAMILIES_PER_DWELLING
            implied = footprints * combined
            rows.append(
                {
                    "stratum": name,
                    "n_radios": int(row["n_radios"]),
                    "n_barrios": int(row["n_barrios"]),
                    "vida_footprints_ge10": footprints,
                    "census_occupied_dwellings": dwellings,
                    "census_households": households,
                    "raw_fp_per_occupied_dwelling": footprints / dwellings,
                    "raw_fp_per_household": footprints / households,
                    "dwelling_yield": dwelling_yield,
                    "combined_factor": combined,
                    "break_even_yield": break_even,
                    "implied_households": implied,
                    "implied_household_ratio": implied / households,
                    "excess_over_census_households": implied - households,
                    "excess_over_census_households_pct": implied / households - 1,
                }
            )
    return pd.DataFrame(rows)


def write_markdown(table: pd.DataFrame) -> None:
    lines = [
        "# Diagnostic: footprints against Census households under y x 1.1 factors",
        "",
        f"Sample: census radios with RENABAP coverage at or above {THRESHOLD:.0%}.",
        f"Footprints: VIDA, September 2024, {FILTER} filter.",
        "Census: May 2022.",
        "",
        "The headline analysis applies no multiplier. This table overlays the",
        f"paper's footprint branch: footprints are scaled by y x {FAMILIES_PER_DWELLING}",
        "for each tested dwelling yield y (occupied dwellings per mapped",
        "footprint) before the comparison with Census households. Both factors",
        "come from outside this analysis and are taken as given here. It is a",
        "sensitivity, not a second estimate, and it does not change any existing",
        "output.",
        "",
        "The two strata are reported separately and overlap. Most CABA radios are",
        "already outside the horizontal regime, so the rows are not additive.",
        "",
        "| Stratum | Radios | Barrios | Footprints >=10 m2 | Occupied dwellings | "
        "Households | FP / dwelling | FP / household |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    first = table.drop_duplicates("stratum")
    for row in first.itertuples():
        lines.append(
            f"| {row.stratum} | {row.n_radios:,} | {row.n_barrios:,} | "
            f"{row.vida_footprints_ge10:,} | {row.census_occupied_dwellings:,} | "
            f"{row.census_households:,} | "
            f"{row.raw_fp_per_occupied_dwelling:.2f} | "
            f"{row.raw_fp_per_household:.2f} |"
        )
    lines += [
        "",
        "Break-even yield, at which footprints x y x 1.1 equals Census households:",
        "",
    ]
    for row in first.itertuples():
        lines.append(f"- {row.stratum}: y = {row.break_even_yield:.3f}")
    lines += [
        "",
        f"After the y x {FAMILIES_PER_DWELLING} factor:",
        "",
        "| Stratum | y | Implied households | Census households | Ratio | "
        "Excess | Excess % |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in table.itertuples():
        lines.append(
            f"| {row.stratum} | {row.dwelling_yield:.2f} | "
            f"{row.implied_households:,.0f} | "
            f"{row.census_households:,} | {row.implied_household_ratio:.2f} | "
            f"{row.excess_over_census_households:+,.0f} | "
            f"{row.excess_over_census_households_pct:+.1%} |"
        )
    lines += [
        "",
        "The 2022 to 2024 temporal mismatch is not corrected here. The growth",
        "analysis in outputs/openbuildings-growth/ attributes about 20 percent of",
        "the excess above parity to construction after Census Day.",
        "",
    ]
    (OUTPUT_DIR / f"{STEM}.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(
            f"{SOURCE} is missing. Run census_dwelling_footprint.py first."
        )
    table = build()
    table.to_csv(OUTPUT_DIR / f"{STEM}.csv", index=False)
    write_markdown(table)
    print(table.to_string(index=False))
    print(f"\nWrote {OUTPUT_DIR / STEM}.csv and .md")


if __name__ == "__main__":
    main()
