# Coverage concepts

Census-coverage arguments routinely conflate the quantities below. The
definitions come from `docs/barrios-visibles-census-coverage-sources-and-notes.md`.
The `method` field on a source note and the `requires_direct_measurement` flag
on a claim keep them apart.

## Direct enumeration

People actually recorded from household responses or field enumeration.

## Imputation

Statistical assignment of people or characteristics where a dwelling is known
or inferred but no complete interview was obtained. Imputation improves
completeness without reaching residents. It is weakest where the underlying
dwelling or household was never identified. That is the failure mode of dense
informal settlements.

## Gross omission

People who should have been included and were not correctly enumerated. This
can be large even when the final national total sits close to an independent
population estimate.

## Erroneous inclusion

Duplicated people, people counted in the wrong place or at the wrong
residence, and other records that should not appear in the count.

## Net coverage error

The balance left after omissions and erroneous inclusions offset each other. A
small net error does not imply a small number of omissions.

## Demographic reconciliation or population projection

A calculation over prior population stocks, births, deaths, migration, census
results, and sometimes coverage-study evidence, producing a plausible
population total. It tests aggregate demographic consistency. Whether each
person was enumerated or correctly located stays untested.

## Net accuracy against complete enumeration

Argentina's 2022 figure of 0.5 percent is a net differential against a
demographic estimate, not a measured omission rate. The United States 2020
census shows the size of that gap. Its post-enumeration survey estimated 18.8
million omissions while national net coverage error stayed statistically
indistinguishable from zero, because roughly 18 million erroneous
enumerations offset them.

Brazil reports three quantities for one census. About 195.1 million people
were directly enumerated, the published total reached 203.1 million after
imputation, and a later demographic estimate for July 1, 2022 gave 210.9
million.
