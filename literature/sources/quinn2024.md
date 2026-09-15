---
key: quinn2024
status: queued
lang: en
verification: needs_follow_up
strength: medium
source_type: dataset
method: remote_sensing
evidence_type: [method_precedent]
unit_of_analysis: [building]
geographies: []
tags: [Argentina-analysis, temporal-buildings, post-2022, needs-metadata]
cited_in_manuscript: false
retrieved: 2026-09-15
follow_up: >-
  INCOMPLETE CITATION. Normalise the venue, DOI, and author list against
  the exact dataset version used in the analysis, as the annotated
  review requires. Add exact authors, DOI/arXiv identifier, dataset
  version, temporal coverage, and access date. Link the source to the
  analysis artifact that produced the ≤20% result.
evidence:
  - id: E1
    label: "Provides an independent way to test whether footprint excess is explained by post-census construction."
    kind: unlocated
    quote: |
      Provides an independent way to test whether footprint excess is
      explained by post-census construction.
    origin: annotated-review
  - id: E2
    label: "In the current Barrios Visibles clean low-rise tests, post-2022 construction explains no more than roughly 20% of the excess."
    kind: unlocated
    quote: |
      In the current Barrios Visibles clean low-rise tests, post-2022
      construction explains no more than roughly 20% of the excess.
    origin: annotated-review
claims:
  - claim: post-2022-construction-must-be-tested
    relationship: method_validates
    strength: medium
    evidence: [E1]
    note: >-
      Provides an independent way to date detected construction. It says
      nothing about occupancy, which stays a separate assumption.
does_not_establish:
  - "Building date does not establish occupancy, residential use, household count, or census coverage."
  - "Temporal detection errors and confidence thresholds must remain documented with the project results."
---

Quinn and colleagues describe the Open Buildings 2.5D Temporal
dataset, which tracks building changes across the Global South. The
project uses it to test whether structures counted in the footprint
snapshot postdate the 2022 census.

The citation is incomplete and the annotated review flags it for
normalisation. The dataset dates construction and nothing else.
Occupancy remains an independent assumption, so temporal evidence can
rule out a post-census-construction explanation without establishing
that the buildings are occupied.
