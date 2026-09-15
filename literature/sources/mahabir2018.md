---
key: mahabir2018
status: retained
lang: en
verification: verified_secondary
strength: medium
source_type: review
method: literature_review
evidence_type: [context, mechanism_evidence]
unit_of_analysis: [building, dwelling, settlement]
geographies: []
tags: [review, slum-mapping, extraction-error, settlement-life-cycle]
cited_in_manuscript: true
retrieved: 2026-09-15
follow_up: >-
  Locate the extraction-error discussion and the life-cycle framing in the
  published review.
evidence:
  - id: E1
    label: Extraction algorithms delete small dwellings as noise and merge adjacent ones
    kind: unlocated
    quote: |
      Extraction algorithms both delete small dwellings as noise and merge
      adjacent ones.
    origin: manuscript
  - id: E2
    label: Slum life cycle runs infancy to consolidation to maturity, with vertical densification possible at maturity
    kind: unlocated
    quote: |
      The standard slum life-cycle runs infancy, consolidation, maturity,
      with vertical densification possible at the maturity stage.
    origin: manuscript
claims:
  - claim: missing-footprints-push-estimates-down
    relationship: qualifies
    strength: medium
    evidence: [E1]
    note: >-
      Automated extraction errs in both directions at once, deleting small
      dwellings and merging adjacent ones, so a single correction factor
      cannot repair it.
  - claim: planar-counts-conservative-when-vertical
    relationship: supports
    strength: medium
    evidence: [E2]
    note: >-
      Explains why footprint counts fall below the registry in consolidated
      settlements such as those in the Ciudad Autónoma de Buenos Aires, and
      exceed it in horizontal ones.
does_not_establish:
  - "It is a review, so it does not itself measure an extraction error rate. Cite the primary studies for rates."
  - "It does not establish how many Argentine settlements have reached the maturity stage."
  - "The life-cycle model is a framing rather than a validated temporal sequence for any specific settlement."
---

Mahabir and colleagues review high and very high resolution remote sensing
approaches for detecting and mapping slums.

Extraction algorithms drop small dwellings as noise and merge adjacent ones,
so the error is bidirectional and resists one correction factor. Settlements
also follow a life cycle from infancy through consolidation to maturity, where
vertical growth becomes possible. Vertical growth at maturity is why the
analysis reports CABA separately from the rest of the country.
