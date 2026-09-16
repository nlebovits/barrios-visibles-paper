---
key: kuffer2019
status: retained
lang: en
verification: verified_secondary
strength: medium
source_type: peer_reviewed
method: remote_sensing
evidence_type: [direct_analogue, mechanism_evidence]
unit_of_analysis: [settlement, roof, resident]
geographies: [Tanzania]
tags: [direct-analogue, roof-area, census-comparison, Dar-es-Salaam, subletting, priority]
cited_in_manuscript: false
retrieved: 2026-09-15
follow_up: >-
  Obtain the full JURSE paper and locate the 3 million and 5 million
  figures on the page.
evidence:
  - id: E1
    label: "A census-based estimate implied approximately 3 million Dar es Salaam residents living in slum-like conditions."
    kind: data
    loc: "pp. 1–3"
    quote: |
      A census-based estimate implied approximately 3 million Dar es Salaam
      residents living in slum-like conditions.
    origin: annotated-review
  - id: E2
    label: "A bottom-up estimate combining OSM/UAV-derived rooftop outlines, a household survey in five settlements, Slum Dwellers International data, and land-use exclusions produced approximately 5 millio…"
    kind: data
    loc: "pp. 1–3"
    quote: |
      A bottom-up estimate combining OSM/UAV-derived rooftop outlines, a
      household survey in five settlements, Slum Dwellers International
      data, and land-use exclusions produced approximately 5 million.
    origin: annotated-review
  - id: E3
    label: "Roof-area calibration was 9.8 m² per person in the household survey and 10.6 m² per person in SDI data."
    kind: data
    loc: "pp. 1–3"
    quote: |
      Roof-area calibration was 9.8 m² per person in the household survey
      and 10.6 m² per person in SDI data.
    origin: annotated-review
  - id: E4
    label: "The inferred total city population exceeded 6 million, with roughly 80% living in slum-like conditions."
    kind: data
    loc: "pp. 1–3"
    quote: |
      The inferred total city population exceeded 6 million, with roughly
      80% living in slum-like conditions.
    origin: annotated-review
  - id: E5
    label: "The analysis mapped concentrations of residents described as possibly uncounted."
    kind: paraphrase
    loc: "pp. 1–3"
    quote: |
      The analysis mapped concentrations of residents described as possibly
      uncounted.
    origin: annotated-review
  - id: E6
    label: "Houses were commonly single-storey, but portions of houses were often sublet."
    kind: paraphrase
    loc: "pp. 1–3"
    quote: |
      Houses were commonly single-storey, but portions of houses were often
      sublet.
    origin: annotated-review
claims:
  - claim: imagery-reveals-more-dwellings
    relationship: supports
    strength: high
    evidence: [E1, E2, E4]
    note: >-
      Closest published roof-based versus census-based comparison in the
      registry. The gap is about two million people in one city.
  - claim: informal-population-underrepresentation
    relationship: supports
    strength: high
    evidence: [E1, E2]
  - claim: footprint-not-one-household
    relationship: supports
    strength: medium
    evidence: [E6]
    note: >-
      Single-storey houses with sublet portions, so the household count
      exceeds the structure count without any verticality.
does_not_establish:
  - "The paper explicitly does not claim a “final truth.”"
  - "Roof area per person is transferred across the city and could differ between central and peripheral settlements."
  - "Census, survey, and imagery inputs came from different years."
  - "Mixed-use buildings can inflate residential roof area despite land-use exclusions."
---

Kuffer and colleagues compare a census-based estimate of Dar es Salaam
residents in slum-like conditions against a bottom-up estimate built
from rooftop outlines, a household survey in five settlements, Slum
Dwellers International data, and land-use exclusions.

This is the closest design analogue to Barrios Visibles in the
registry. It runs the same comparison, roof evidence against official
population, and finds the roof evidence far larger. The published
version is a four-page conference paper, so the methodological detail
is thin.
