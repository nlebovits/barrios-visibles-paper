---
key: sanchezcespedes2024
status: retained
lang: en
verification: verified_full_text
strength: high
source_type: peer_reviewed
method: remote_sensing
evidence_type: [direct_analogue, method_validation]
unit_of_analysis: [census_area, building, resident]
geographies: [Colombia]
tags: [Colombia, DANE, census-gap, unvisited-areas, community-mapping, satellite-buildings, priority]
cited_in_manuscript: false
retrieved: 2026-09-15
evidence:
  - id: E1
    label: "Of 1,302 special-route census enumeration areas, 508 had at least 90% of expected properties enumerated, 628 were partially enumerated, and 166 were not visited."
    kind: data
    loc: "Data pp. 2–4; results pp. 8–11; Figure 5"
    quote: |
      Of 1,302 special-route census enumeration areas, 508 had at least 90%
      of expected properties enumerated, 628 were partially enumerated, and
      166 were not visited.
    origin: annotated-review
  - id: E2
    label: "Models were trained using 489 sufficiently enumerated areas."
    kind: data
    loc: "Data pp. 2–4; results pp. 8–11; Figure 5"
    quote: |
      Models were trained using 489 sufficiently enumerated areas.
    origin: annotated-review
  - id: E3
    label: "Satellite building coverage alone explained 56.8% of out-of-sample population variance."
    kind: data
    loc: "Data pp. 2–4; results pp. 8–11; Figure 5"
    quote: |
      Satellite building coverage alone explained 56.8% of out-of-sample
      population variance.
    origin: annotated-review
  - id: E4
    label: "Community estimates explained 66.2%."
    kind: data
    loc: "Data pp. 2–4; results pp. 8–11; Figure 5"
    quote: |
      Community estimates explained 66.2%.
    origin: annotated-review
  - id: E5
    label: "The combined satellite and community model explained 67.9% of population variance and 65.1% of building-count variance, with the best overall accuracy."
    kind: data
    loc: "Data pp. 2–4; results pp. 8–11; Figure 5"
    quote: |
      The combined satellite and community model explained 67.9% of
      population variance and 65.1% of building-count variance, with the
      best overall accuracy.
    origin: annotated-review
  - id: E6
    label: "Validation of World Settlement Footprint building area in Cartagena produced mean error of 0.29%, MAE of 6.52%, and RMSE of 8.98%."
    kind: data
    loc: "Data pp. 2–4; results pp. 8–11; Figure 5"
    quote: |
      Validation of World Settlement Footprint building area in Cartagena
      produced mean error of 0.29%, MAE of 6.52%, and RMSE of 8.98%.
    origin: annotated-review
claims:
  - claim: official-enumeration-omits-areas
    relationship: supports
    strength: high
    evidence: [E1]
    note: >-
      The closest Latin American precedent in the registry, and the national
      statistical office coauthored it. 628 of 1,302 enumeration areas
      partially enumerated and 166 never visited.
  - claim: footprints-contain-population-information
    relationship: supports
    strength: high
    evidence: [E3, E4, E5, E6]
    note: >-
      Satellite building coverage alone explained 56.8 percent of
      out-of-sample population variance, and the combined model reached 67.9
      percent.
does_not_establish:
  - "The omitted Colombian areas were remote, conflict-affected, and often home to minority communities, not urban informal settlements."
  - "The method models building coverage, not one footprint per dwelling."
  - "The study does not report a national missing-population total."
  - "Treating 90% property coverage as “full” leaves some residual enumeration error."
---

Sánchez-Céspedes and colleagues estimate population for
difficult-to-access regions of Colombia after the census, combining
social cartography with satellite-derived building coverage. DANE, the
national statistical office, coauthored the study.

This is the strongest census-gap precedent in the registry for two
reasons. A national statistical office documents its own enumeration
failure in numbers, and it then uses building evidence to repair the
gap. Both moves are what Barrios Visibles argues for in Argentina.
