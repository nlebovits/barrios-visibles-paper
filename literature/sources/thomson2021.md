---
key: thomson2021
status: retained
lang: en
verification: verified_full_text
strength: high
source_type: peer_reviewed
method: modeled_population_product
evidence_type: [direct_analogue, method_precedent]
unit_of_analysis: [settlement, grid_cell, building]
geographies: [Nigeria, Kenya]
tags: [undercount, gridded-population, households-per-building, community-enumeration, priority]
cited_in_manuscript: true
retrieved: 2026-09-15
follow_up: >-
  Check the 39 percent figure against the exact table and performance metric,
  as the census-coverage notes require. The citation conflict is resolved: the
  Zotero record gives Urban Science 5(2):48, and the IJGI 10(6):381 link in
  those notes is an error.
evidence:
  - id: E1
    label: Nine gridded population products compared with community field-referenced boundaries and population estimates
    kind: data
    loc: "Methods and product descriptions around p. 9"
    quote: |
      118 settlements: 26 in Lagos, 39 in Port Harcourt, and 53 in Nairobi.
    sample_size: 118 settlements across three cities
    reference_kind: community_estimate
    origin: annotated-review
  - id: E2
    label: Every product substantially underestimated the reference populations
    kind: data
    loc: "pp. 12-14"
    quote: |
      Bias ranged from -2,853 to -7,638 people per settlement. RMSE ranged
      from 4,958 to 14,422.
    reference_kind: community_estimate
    origin: annotated-review
  - id: E3
    label: Best-performing product HRSL captured only 39 percent of the community-derived population on average
    kind: data
    loc: "pp. 12-14"
    quote: |
      The best-performing product, HRSL, captured only 39% of the
      community-derived population on average.
    reference_kind: community_estimate
    origin: annotated-review
  - id: E4
    label: In Lagos gridded products placed 1.02 to 2.96 percent of population in mapped slum areas against 56 percent by survey method
    kind: data
    loc: "pp. 12-14"
    quote: |
      In Lagos, gridded products placed only 1.02-2.96% of the population in
      mapped slum areas, versus 56% using UN-Habitat's survey-based method.
    reference_kind: community_estimate
    origin: annotated-review
  - id: E5
    label: Slum-specific variation in household size, households per building, and residential-building share are major model error sources
    kind: paraphrase
    loc: "discussion and limitations pp. 14-18"
    quote: |
      The paper identifies slum-specific variation in household size,
      households per building, and residential-building share as major
      sources of model error.
    origin: annotated-review
  - id: E6
    label: Contiguous roofs can be extracted as a single building and multiple one-room dwellings within a building are common
    kind: paraphrase
    loc: "discussion and limitations pp. 14-18"
    quote: |
      It notes that contiguous roofs can be extracted as a single building
      and that multiple one-room dwellings within a building are common.
    origin: annotated-review
  - id: E7
    label: WorldPop Peanut Butter footprint models used a default of 1.1 households per building in Nigeria and Kenya
    kind: data
    loc: "Methods and product descriptions around p. 9"
    quote: |
      Its footprint-based WorldPop "Peanut Butter" models used a default of
      1.1 households per building in both Nigeria and Kenya.
    reference_kind: modeled_estimate
    origin: annotated-review
  - id: E8
    label: Know Your City workflow counted front doors, sampled household size, multiplied, and community-validated
    kind: paraphrase
    loc: "Methods and product descriptions around p. 9"
    quote: |
      The Know Your City workflow counted front doors, sampled households for
      average household size, multiplied these quantities, and
      community-validated the results.
    reference_kind: community_estimate
    origin: annotated-review
  - id: E9
    label: Gridded products used urban defaults of 63 to 71 percent residential buildings, unverified against slum data
    kind: unlocated
    quote: |
      Gridded population products have used urban defaults of 63% to 71%
      residential buildings in Kenya and Nigeria, although those defaults
      were never verified against slum data.
    origin: manuscript
claims:
  - claim: informal-population-underrepresentation
    relationship: supports
    strength: high
    evidence: [E1, E2, E3, E4]
    note: >
      Strongest multi-settlement empirical evidence in the registry. The
      deficit holds across all nine products and all three cities.
  - claim: national-total-conceals-geographic-error
    relationship: supports
    strength: high
    evidence: [E4]
    note: >
      Lagos is the sharpest case. The products place almost no population in
      mapped slum areas while the city total stays plausible.
  - claim: footprint-not-one-household
    relationship: supports
    strength: high
    evidence: [E6, E7]
    note: >
      Also establishes that a 1.1 households-per-building multiplier is in
      use outside RENABAP and was not invented for this analysis.
  - claim: footprints-contain-population-information
    relationship: qualifies
    strength: medium
    evidence: [E5, E9]
    note: >
      Citywide household-size and building-occupancy averages fail inside
      informal settlements, so footprint methods need local calibration.
does_not_establish:
  - It does not directly audit a national census. The tested products are census-derived, so the measured error mixes census input error with spatial allocation and model error.
  - It does not validate an Argentine effect size, nor the 1.1 multiplier in Argentina.
  - Know Your City reference estimates were not independently verified. Sampling procedures were incompletely documented and some questionable large estimates were excluded.
---

Thomson and colleagues compare nine widely used gridded population products
against community field-referenced boundaries and population estimates for 118
settlements in Lagos, Port Harcourt, and Nairobi. The products include
LandScan, WorldPop, HRSL, GRID3, and GHS-POP. Every one underestimates the
reference population, and the shortfall is worst in the densest settlements.

This is the strongest published analogue for the Barrios Visibles comparison.
The mechanism differs, because RENABAP is a field registry rather than a
gridded product. The structural vulnerability is the same. One enumeration
approach cannot resolve the density heterogeneity that defines informal
settlements.

Read it with kuffer2022, which supplies the allocation mechanism, and with
boo2022, which validates the footprint-to-population step the products get
wrong.

One citation caution. The census-coverage working notes link this paper to
ISPRS IJGI 10(6):381. That is a different article. The Zotero record and the
annotated review both place it in Urban Science 5(2):48.
