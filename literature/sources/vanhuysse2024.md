---
key: vanhuysse2024
status: retained
lang: en
verification: verified_full_text
strength: medium
source_type: peer_reviewed
method: remote_sensing
evidence_type: [mechanism_evidence, method_validation]
unit_of_analysis: [building, dwelling]
geographies: [Kenya]
tags: [Springer-chapter, verticality, multi-unit, EO, context]
cited_in_manuscript: false
retrieved: 2026-09-15
evidence:
  - id: E1
    label: "Describes Nairobi housing ranging to multi-story tenements divided into multiple rental units."
    kind: paraphrase
    loc: "Case studies in §3, manuscript pp. 6–7; EO results in §4; synthesis in §5"
    quote: |
      Describes Nairobi housing ranging to multi-story tenements divided
      into multiple rental units.
    origin: annotated-review
  - id: E2
    label: "Describes Kisumu compounds composed of multiple residential units occupying a single plot, with plot coverage reaching approximately 80% near the center."
    kind: data
    loc: "Case studies in §3, manuscript pp. 6–7; EO results in §4; synthesis in §5"
    quote: |
      Describes Kisumu compounds composed of multiple residential units
      occupying a single plot, with plot coverage reaching approximately 80%
      near the center.
    origin: annotated-review
  - id: E3
    label: "Shows that open building footprints, while imperfect in deprived areas, add substantial morphological information beyond Sentinel-1/2 imagery."
    kind: data
    loc: "Case studies in §3, manuscript pp. 6–7; EO results in §4; synthesis in §5"
    quote: |
      Shows that open building footprints, while imperfect in deprived
      areas, add substantial morphological information beyond Sentinel-1/2
      imagery.
    origin: annotated-review
  - id: E4
    label: "Its overall premise is that EO can meet some spatial-data needs without relying on censuses or socioeconomic surveys."
    kind: paraphrase
    loc: "Case studies in §3, manuscript pp. 6–7; EO results in §4; synthesis in §5"
    quote: |
      Its overall premise is that EO can meet some spatial-data needs
      without relying on censuses or socioeconomic surveys.
    origin: annotated-review
claims:
  - claim: footprint-not-one-household
    relationship: supports
    strength: medium
    evidence: [E1, E2]
    note: >-
      Multi-story tenements divided into rental units, and Kisumu compounds
      of multiple residential units on one plot with coverage near 80
      percent.
  - claim: footprints-contain-population-information
    relationship: supports
    strength: medium
    evidence: [E3]
    note: >-
      Open footprints add substantial morphological information beyond
      Sentinel imagery even where they are imperfect.
does_not_establish:
  - "It does not estimate population, occupancy, dwellings per footprint, or census undercount."
  - "A plot is not necessarily equivalent to one detected footprint."
---

Vanhuysse and colleagues survey low-cost Earth observation for mapping
and characterising deprived urban areas, with Nairobi and Kisumu case
studies.

The Kisumu compound description is the useful part for Argentina.
Multiple residential units on one plot, at plot coverage near 80
percent, is a morphology that a footprint count reads as fewer
dwellings than exist.
