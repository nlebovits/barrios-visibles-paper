---
key: checchi2013
status: retained
lang: en
verification: verified_secondary
strength: medium
source_type: peer_reviewed
method: remote_sensing
evidence_type: [mechanism_evidence, method_validation]
unit_of_analysis: [building, dwelling, resident]
geographies: [Haiti, Mozambique]
tags: [imagery-population, residential-share, shelters-per-structure, displacement]
cited_in_manuscript: true
retrieved: 2026-09-15
follow_up: >-
  All findings are recorded from the manuscript rather than the source. Locate
  the Port-au-Prince ratios, the residential-share range, and the Bairro
  Esturro figures in the original article.
evidence:
  - id: E1
    label: Field teams counted 1.9 to 2.2 shelters per structure identified from imagery in two dense Port-au-Prince neighbourhoods
    kind: unlocated
    quote: |
      In two dense Port-au-Prince neighbourhoods, ground teams counted 1.9
      and 2.2 shelters per residential structure identified in imagery.
    sample_size: two neighbourhoods
    reference_kind: complete_enumeration
    origin: manuscript
  - id: E2
    label: Analyst-derived population estimates ran 46 to 48 percent below the census in those neighbourhoods
    kind: unlocated
    quote: |
      Analyst-derived population estimates ran 46% to 48% below the census.
    reference_kind: census
    origin: manuscript
  - id: E3
    label: Analysts judged 77 to 100 percent of structures residential across eleven camp and urban sites
    kind: unlocated
    quote: |
      Imagery analysts classifying structures in eleven camp and urban sites
      judged between 77% and 100% of them residential.
    sample_size: eleven sites
    origin: manuscript
  - id: E4
    label: In Bairro Esturro 84 to 87 percent were residential and the imagery count reached 84 percent of a field estimate
    kind: unlocated
    quote: |
      84% to 87% in the one ordinary low-rise neighbourhood, Bairro Esturro
      in Mozambique, where the imagery count also reached 84% of a field
      estimate.
    reference_kind: complete_enumeration
    origin: manuscript
claims:
  - claim: footprint-not-one-household
    relationship: supports
    strength: high
    evidence: [E1, E2]
    note: >-
      In dense low-rise settlements a mapped structure held about two
      shelters. This is the clearest case for a dwelling yield above one in
      horizontal morphology, where verticality cannot be the explanation.
  - claim: missing-footprints-push-estimates-down
    relationship: qualifies
    strength: medium
    evidence: [E3, E4]
    note: >-
      Cuts the other way. If 13 to 16 percent of mapped structures in an
      ordinary low-rise neighbourhood are not residential, some footprints
      are not dwellings. This anchors the 0.85 dwelling-yield scenario.
does_not_establish:
  - "The Port-au-Prince sites are post-earthquake displacement settings, so the shelter density is not a stable residential morphology."
  - "It does not supply an Argentine footprint-to-dwelling ratio. Bairro Esturro is the only ordinary low-rise neighbourhood in the study."
  - "The residential-share figures are analyst judgements from imagery, not field verification of use."
---

Checchi and colleagues test whether satellite imagery can estimate displaced
populations quickly, and validate against ground counts across eleven camp and
urban sites. The sites include two dense post-earthquake Port-au-Prince
neighbourhoods and one ordinary low-rise neighbourhood, Bairro Esturro in
Mozambique.

This is the only source in the registry with evidence running both directions
on the footprint-to-dwelling ratio. The Port-au-Prince figures argue the ratio
exceeds one. The residential-share figures argue some mapped structures are
not dwellings at all. The dwelling-yield range in the manuscript spans both,
which is the honest use of this source.
