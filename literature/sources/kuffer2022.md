---
key: kuffer2022
status: retained
lang: en
verification: verified_full_text
strength: high
source_type: peer_reviewed
method: modeled_population_product
evidence_type: [mechanism_evidence, direct_analogue]
unit_of_analysis: [grid_cell, settlement]
geographies: [Ghana, Indonesia, Egypt, Afghanistan, Brazil, United States]
tags: [geographic-misallocation, GHS-POP, national-total, informal-density, priority]
cited_in_manuscript: true
retrieved: 2026-09-15
evidence:
  - id: E1
    label: GHS-POP compared with the finest available local population data aggregated to 1 km across seven cities
    kind: paraphrase
    loc: "Abstract; §4.3 pp. 10-11"
    quote: |
      Compares GHS-POP with the finest available local population data,
      aggregated to 1 km, across seven cities.
    sample_size: seven cities
    reference_kind: census
    origin: annotated-review
  - id: E2
    label: Only about 25 percent of urban cells fell within 10 percent of local reference counts
    kind: data
    loc: "Table 7 pp. 11-12"
    quote: |
      Only approximately 25% of urban cells were within ±10% of local
      reference counts; roughly 75% were wrongly estimated under that
      criterion.
    reference_kind: census
    origin: annotated-review
  - id: E3
    label: Correctly estimated residential cells ranged from 8.9 percent in Kumasi to 68.2 percent in New York
    kind: data
    loc: "Table 7 pp. 11-12"
    quote: |
      Correctly estimated residential cells included 8.9% in Kumasi, 16.2% in
      Jakarta, 13.4% in Cairo, 27.8% in Kabul, 26.7% in São Paulo, and 68.2%
      in New York.
    reference_kind: census
    origin: annotated-review
  - id: E4
    label: Dense residential, informal, and high-rise areas tended to be underestimated
    kind: paraphrase
    loc: "§4.3 pp. 10-11"
    quote: |
      Dense residential, informal, and high-rise areas tended to be
      underestimated.
    origin: annotated-review
  - id: E5
    label: Mixed or non-residential central areas and some low-density outskirts tended to be overestimated
    kind: paraphrase
    loc: "§4.3 pp. 10-11"
    quote: |
      Mixed or non-residential central areas and some low-density outskirts
      tended to be overestimated.
    origin: annotated-review
  - id: E6
    label: Mechanism is binary distribution of population across built-up pixels without land-use or height information
    kind: paraphrase
    loc: "discussion and conclusion pp. 12-15"
    quote: |
      The mechanism is partly the binary distribution of population across
      built-up pixels without sufficient land-use or height information.
    origin: annotated-review
  - id: E7
    label: Top-down disaggregation assumes admin-unit average densities hold at fine scale
    kind: unlocated
    quote: |
      Top-down disaggregation assumes admin-unit average densities hold at
      fine scale, collapsing precisely where density is most extreme. Most
      products also lack a building-density auxiliary that would let the
      model resolve intra-urban heterogeneity.
    origin: manuscript
claims:
  - claim: national-total-conceals-geographic-error
    relationship: supports
    strength: high
    evidence: [E2, E3, E4, E5, E6]
    note: >-
      The registry's best source for this claim. Roughly 75 percent of urban
      cells are wrong by more than 10 percent while the city totals stay
      plausible, and the error is directional: people move out of dense
      informal areas and into non-residential or low-density cells.
  - claim: informal-population-underrepresentation
    relationship: supports
    strength: high
    evidence: [E4]
    note: >-
      Underestimation concentrates in exactly the morphology RENABAP
      settlements have.
  - claim: footprints-contain-population-information
    relationship: qualifies
    strength: medium
    evidence: [E6, E7]
    note: >-
      Built-up area without land use or height is not enough. This is the
      argument for a building-density auxiliary rather than area alone.
does_not_establish:
  - "It does not independently test the completeness of national censuses."
  - "São Paulo's informal-settlement category was excluded from part of the analysis because most settlements were smaller than one 1-km cell."
  - "Some of the measured error reflects temporal and source mismatches rather than model failure."
  - "The paper warns that Google Open Buildings can contain large omissions in high-density informal areas. That warning supports conservatism but is not Argentina-specific."
---

Kuffer and colleagues compare GHS-POP against the finest available local
population data across seven cities, aggregated to a common 1 km grid. Roughly
three quarters of urban cells fall outside 10 percent of the local reference.

The direction of the error is what matters for this project. Population moves
statistically out of dense informal and high-rise areas and into mixed,
non-residential, or low-density cells. A nationally reconciled total validates
nothing about where the people were placed. This is the mechanism
behind the shortfall thomson2021 measures.
