# Reproducibility and data provenance

## Publication paths

The repository separates exact publication reproduction from live upstream
rebuilds.

- **pixi run estimate** defaults to Zenodo record 22656880 and verifies the md5
  values returned by that version-specific record.
- **pixi run census-comparison** will default to the new version-specific
  Zenodo record after its record id is inserted in census_comparison.py.
- **pixi run reproduce** runs both analyses.
- **python estimate.py --source live** and
  **python census_comparison.py --source live** retrieve current upstream data.
  They need not reproduce submitted values.

The Census comparison can be checked before publication with:

    pixi run census-comparison --       --census-path /path/to/radios-hilbert.parquet       --settlements-path /path/to/barrios-hilbert.parquet

## Files required in the new Zenodo version

Retain the files already in version 1.0.0 and add:

| Archive filename                 | Purpose                                                                          | Expected SHA-256                                                 |
| -------------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| census_2022_radios.parquet       | INDEC population and private-dwelling totals joined to corrected radio geometry  | ade36a340854bf3e616ff28f34527ba193aa515274c503929877f831276a4936 |
| census_settlement_counts.parquet | Settlement polygons and footprint counts used in the validated Census comparison | a90503b0ef3ad5e9359cb93fba7363cf7bb872ecbb9be84fc446ea40da5ac012 |

After publishing the version, replace
REPLACE_WITH_VERSION_RECORD_ID in census_comparison.py and both manuscript
DOI placeholders with the exact version DOI. Do not use the concept DOI.

## Household floor and dwelling-yield sweep

**pixi run estimate** computes, per settlement, H = max(R, F × y × 1.1),
where R is the RENABAP family count, F is the eligible footprint count, and y
is the assumed number of occupied dwellings per mapped footprint. The yield is
one net factor for every mechanism between a mapped polygon and an occupied
household. The sweep runs 30 scenarios: five yields from 0.60 to 1.15, three
size filters, and two population multipliers. It also reports the aggregate
parity yield (R / 1.1 / F) per size filter. Results are written to
outputs/sensitivity_dwelling_yield.csv and outputs/settlement_analysis_summary.md.
The supplement's table S1 is copied from the CSV.

**pixi run diagnostic-multiplier** overlays the same y × 1.1 factor on the
Census dwelling-inventory comparison at the 95 percent coverage threshold and
reports the break-even yield at which implied households equal Census
households. It reads outputs/census-dwelling-footprint/ and writes
diagnostic_household_multiplier.csv and .md there.

## Census calculation

The analysis intersects 6,467 RENABAP polygons with 66,502 Census 2022 radios.
For each radio, it computes the share of its area covered by all barrio
polygons. Population is allocated to each barrio in proportion to its
intersection area. Threshold runs keep radios with coverage of at least 0,
10, 25, 50, 75, 90, or 95 percent, and retain barrios for which eligible
radios cover at least half the barrio. The program verifies the published
counts and ratios before writing CSV and Markdown results under
outputs/census-comparison/.

VIV_TOT_P is the number of private dwellings, not households. The resulting
persons-per-private-dwelling ratios are occupancy diagnostics.

## Dwelling and household inventory comparison

**pixi run dwelling-footprint** runs a second, independent test that removes
both assumptions standing between the physical evidence and the published
result. It applies no persons-per-footprint multiplier and no areal allocation.

    pixi run dwelling-footprint -- \
      --census-path /path/to/radios-hilbert.parquet \
      --settlements-path /path/to/barrios-hilbert.parquet

A census radio qualifies when RENABAP polygons cover at least 50, 75, 90, or 95
percent of its area. Once it qualifies, the whole radio enters the comparison,
with its full INDEC dwelling and household counts and every building footprint
whose centroid falls inside it. Coverage is measured both by dissolving the barrio polygons
and by summing the intersections separately, as census_comparison.py does. The
two measures select identical radios at every threshold.

Footprints are assigned by centroid containment. The VIDA schema has no stable
footprint id, so uniqueness comes from the geometry: census radios tile the
territory without overlap, and a centroid lies in at most one radio. This also
removes the boundary double-count in the published `building_count`, which used
`ST_Intersects`.

Census quantities come from the REDATAM long table at
https://data.source.coop/nlebovits/censo-argentino/2022/census-data.parquet.
The script asserts eight national identities before it computes anything, which
pins the universe of every variable it reads. `TOTHOG` does not exist in the
2022 base. `VIVIENDA_V06` is the household variable, and its universe is
dwellings with people present.

Temporal mismatch, labelled but not corrected:

| Quantity                                          | Date           |
| ------------------------------------------------- | -------------- |
| Census dwelling, household, and population counts | May 2022       |
| VIDA building footprint snapshot                  | September 2024 |

Results are written to outputs/census-dwelling-footprint/. The analysis does
not support any inference about national census omission.

### Building inventories predating the census

**pixi run fetch-ms-buildings** downloads two Microsoft releases from the
Planetary Computer ms-buildings collection, so the same radios can be counted
against a building inventory that predates Census Day.

    pixi run fetch-ms-buildings -- \
      --census-path /path/to/radios-hilbert.parquet \
      --settlements-path /path/to/barrios-hilbert.parquet

| Release    | Layout                                | Declared imagery         |
| ---------- | ------------------------------------- | ------------------------ |
| 2022-06-14 | one whole-country partition, 22 parts | 2014-04-15 to 2021-06-06 |
| 2023-04-25 | Bing level-9 quadkeys                 | 2014-04-15 to 2021-06-06 |

Microsoft's own copies of the 2022 releases are gone. Both 2022 link tables
survive in the git history of microsoft/GlobalMLBuildingFootprints, at commits
4d0848095f and 5e2bf4d8d3, and every URL in them points at
minedbuildings.blob.core.windows.net, which now answers "409 Public access is
not permitted on this storage account". The project README explains that older
versions were not migrated. The Planetary Computer copies survive.

Microsoft publishes no area column, so footprint areas come from
ST_Area_Spheroid rather than from a published field. Its parquet also fails
DuckDB's GeoParquet type check, so it is read as WKB with
enable_geoparquet_conversion disabled.

**The resulting test is inconclusive, and the report says so.** The 2022
Microsoft release holds 5,678,708 buildings for all of Argentina against VIDA's
33,754,731, in a country with 17,783,029 private dwellings. It is thin in
radios that touch no barrio as well, so the shortfall is a detector limit
rather than a barrio-specific failure. The script reports the completeness
diagnostic and draws no conclusion about post-Census construction from it.

Overture Maps was tested for the same purpose and rejected. Its `update_time`
is documented as the last update of the source data record, and in practice it
is a bulk dataset stamp: over a conurbano window of 1,307,185 buildings,
841,674 carry Google Open Buildings 2023-05 and 350,933 carry a Microsoft
sentinel of 2000-01. No Overture release predates Census Day.

## Known gaps requiring resolution

1. **Footprint series.** The manuscript and supplement now
   report the series that the frozen version-1.0.0 Zenodo input reproduces:
   1,967,013 footprints. The recovered Census-comparison input
   (census_settlement_counts.parquet) holds an earlier join with 1,969,975
   footprints. Counts differ in 302 settlements by 2,962 footprints in total,
   and the difference is confined to the 0% coverage row of the Census sweep.
   The exact raw input or processing step that produced 1,969,975 has not
   been recovered. Both manuscripts state the difference next to the Census
   table. Adopted on September 10, 2026 when the dwelling-yield sensitivity
   sweep was added, because the new scenarios can only be computed from the
   archived input.
2. **Adjacent-radio implementation.** The validation report preserved the
   result and the 1-percent coverage rule, but not the exact two-kilometre
   distance query. The executable workflow does not yet reproduce that
   diagnostic.
3. **Raw Census rebuild.** The processed radio file is public on Source
   Cooperative and will be frozen on Zenodo. The separate raw-REDATAM
   processing repository does not currently contain every documented geometry
   conversion step. Exact article reproduction begins from the frozen
   processed radio file and does not claim a fully automated raw-source build.

These items must be resolved or explicitly accepted by the author before
submission. No data deposit is published by this repository workflow.
