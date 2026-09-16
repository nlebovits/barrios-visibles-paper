---
key: breuer2024
status: retained
lang: en
verification: verified_full_text
strength: medium
source_type: peer_reviewed
method: modeled_population_product
evidence_type: [direct_analogue, caution]
unit_of_analysis: [settlement, resident]
geographies: [India, Venezuela, Philippines, South Africa]
tags: [multi-city, WorldPop, underrepresentation, informal-settlements, caution]
cited_in_manuscript: true
retrieved: 2026-09-15
follow_up: >-
  No page locators recorded. Locate the Dharavi, Petare, Baseco, and Cape Town
  figures in the published article.
evidence:
  - id: E1
    label: WorldPop clipped to Earth-observation-mapped morphological slums compared against 80 literature estimates across eight cities and three continents
    kind: unlocated
    quote: |
      Compares WorldPop clipped to Earth-observation-mapped morphological
      slums against 80 literature estimates across eight cities and three
      continents.
    sample_size: eight cities, 80 literature estimates
    reference_kind: undocumented_literature_value
    origin: annotated-review
  - id: E2
    label: Dharavi modelled at 53,194 residents against a 350,000 comparison estimate
    kind: unlocated
    quote: |
      Dharavi: 53,194 modeled residents versus a 350,000 comparison
      estimate; other model versions remained far below estimates of
      300,000-1 million.
    reference_kind: undocumented_literature_value
    origin: annotated-review
  - id: E3
    label: Petare modelled at 42,534 against roughly 600,000 to 1 million
    kind: unlocated
    quote: |
      Petare: 42,534 versus approximately 600,000-1 million.
    reference_kind: undocumented_literature_value
    origin: annotated-review
  - id: E4
    label: Baseco modelled at 12,512 against 51,060
    kind: unlocated
    quote: |
      Baseco: 12,512 versus 51,060.
    reference_kind: undocumented_literature_value
    origin: annotated-review
  - id: E5
    label: Cape Town models captured about 68 percent of comparison populations in townships but only about 24 percent in informal settlements
    kind: unlocated
    quote: |
      Cape Town: modeled estimates captured roughly 68% of comparison
      populations in townships but only about 24% in informal settlements.
    reference_kind: undocumented_literature_value
    origin: annotated-review
claims:
  - claim: informal-population-underrepresentation
    relationship: supports
    strength: medium
    evidence: [E1, E2, E3, E4, E5]
    note: >-
      Broadest geographic coverage in the registry for this claim. Strength is
      capped at medium because the comparison estimates come from
      heterogeneous literature rather than field enumeration.
  - claim: national-total-conceals-geographic-error
    relationship: supports
    strength: medium
    evidence: [E5]
    note: >-
      The township versus informal-settlement split inside one city shows the
      error is not uniform across low-income settlement types.
does_not_establish:
  - "WorldPop is census-derived, so the discrepancy combines census-input limitations, modelled-boundary error, and allocation-model failure. It does not isolate census undercount."
  - "The literature comparison figures differ considerably in quality and date."
  - "Do not repeat the paper's statement that censuses themselves underestimate slum populations by about 46 percent as though thomson2021 established it. Thomson evaluated gridded products, not census enumeration."
  - "The Bangladesh 7.5 times example concerns differing slum definitions and thresholds, not proof that seven-eighths of residents were omitted."
---

Breuer and colleagues compare WorldPop, clipped to morphological slum
boundaries mapped from Earth observation, against 80 literature population
estimates across eight cities on three continents. The deficits are large and
recurring.

The Cape Town result is the most informative. Models captured about 68 percent
of comparison populations in townships and only about 24 percent in informal
settlements, so the problem concentrates in informal settlements rather than
affecting all low-income settlement types equally.

Handle the paper's own citations carefully. It restates a 46 percent census
underestimate as though thomson2021 had established it, and thomson2021
evaluated gridded products instead. Cite the originals.
