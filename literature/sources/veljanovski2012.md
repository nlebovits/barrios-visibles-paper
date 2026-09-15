---
key: veljanovski2012
status: retained
lang: en
verification: verified_full_text
strength: medium
source_type: peer_reviewed
method: remote_sensing
evidence_type: [caution, mechanism_evidence]
unit_of_analysis: [building, roof, resident]
geographies: [Kenya]
tags: [sensitivity-analysis, Kibera, occupancy, merged-roofs, caution]
cited_in_manuscript: false
retrieved: 2026-09-15
follow_up: >-
  Locate the residential-area estimate and the density scenarios on the
  page.
evidence:
  - id: E1
    label: "Estimated approximately 1.647 million m² of residential area in Kibera."
    kind: unlocated
    quote: |
      Estimated approximately 1.647 million m² of residential area in
      Kibera.
    origin: annotated-review
  - id: E2
    label: "Population scenarios based on published density assumptions ranged from 156,652 to 642,284, compared with a reported 2009 census population of 170,070."
    kind: unlocated
    quote: |
      Population scenarios based on published density assumptions ranged
      from 156,652 to 642,284, compared with a reported 2009 census
      population of 170,070.
    origin: annotated-review
  - id: E3
    label: "In Raila, the same typical 32 m² structure corresponded to assumptions ranging from 3.04 to 12.48 people."
    kind: unlocated
    quote: |
      In Raila, the same typical 32 m² structure corresponded to assumptions
      ranging from 3.04 to 12.48 people.
    origin: annotated-review
  - id: E4
    label: "Dense and merged roofs prevented reliable extraction of individual buildings even with VHR imagery."
    kind: unlocated
    quote: |
      Dense and merged roofs prevented reliable extraction of individual
      buildings even with VHR imagery.
    origin: annotated-review
claims:
  - claim: footprint-not-one-household
    relationship: supports
    strength: medium
    evidence: [E3]
    note: >-
      The same typical 32 square metre structure corresponds to between 3.04
      and 12.48 people depending on which published density assumption is
      used.
  - claim: missing-footprints-push-estimates-down
    relationship: supports
    strength: medium
    evidence: [E4]
    note: >-
      Dense and merged roofs prevented reliable extraction of individual
      buildings even from very high resolution imagery.
  - claim: footprints-contain-population-information
    relationship: qualifies
    strength: high
    evidence: [E2]
    note: >-
      The decisive caution for this project. Population scenarios from
      published density assumptions span 156,652 to 642,284 for Kibera
      against a reported census population of 170,070. The multiplier, not
      the imagery, dominates the answer.
does_not_establish:
  - "The paper does not validate a preferred occupancy assumption."
  - "Residential-use assumptions can be wrong, and the total range is intentionally broad."
---

Veljanovski and colleagues estimate population in Kibera from very
high resolution imagery using object-based image analysis, then apply
a range of published density assumptions.

The four-fold spread in the resulting scenarios is the reason the
registry retains this source. It shows that the occupancy multiplier
dominates a footprint-derived population estimate, which is exactly
why Barrios Visibles reports a dwelling-yield range rather than a
point estimate.
