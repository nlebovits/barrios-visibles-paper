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

| Archive filename | Purpose | Expected SHA-256 |
| --- | --- | --- |
| census_2022_radios.parquet | INDEC population and private-dwelling totals joined to corrected radio geometry | ade36a340854bf3e616ff28f34527ba193aa515274c503929877f831276a4936 |
| census_settlement_counts.parquet | Settlement polygons and footprint counts used in the validated Census comparison | a90503b0ef3ad5e9359cb93fba7363cf7bb872ecbb9be84fc446ea40da5ac012 |

After publishing the version, replace
REPLACE_WITH_VERSION_RECORD_ID in census_comparison.py and both manuscript
DOI placeholders with the exact version DOI. Do not use the concept DOI.

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

## Known gaps requiring resolution

1. **Paper I output mismatch.** The manuscript and recovered Paper II input
   contain 1,969,975 footprints. The frozen version-1.0.0 Zenodo-derived
   settlement_estimates.parquet contains 1,967,013. Counts differ in 302
   settlements by 2,962 footprints in total. The current archived national
   footprint input reproduces 1,967,013. The exact raw footprint input or
   processing step that produced 1,969,975 has not been recovered. The
   manuscript numbers have not been silently changed.
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
