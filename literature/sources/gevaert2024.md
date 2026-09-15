---
key: gevaert2024
status: retained
lang: en
verification: verified_full_text
strength: high
source_type: peer_reviewed
method: remote_sensing
evidence_type: [method_validation, caution]
unit_of_analysis: [building]
geographies: [Tanzania, Philippines]
tags: [dataset-bias, manual-validation, false-negatives, Google, OSM, limitations]
cited_in_manuscript: false
retrieved: 2026-09-15
evidence:
  - id: E1
    label: "Manually digitized reference buildings in 100 stratified 250 m tiles in Tanzania and 106 in the Philippines."
    kind: data
    loc: "Methods pp. 12583–12584; Table II; discussion pp. 12587–12588"
    quote: |
      Manually digitized reference buildings in 100 stratified 250 m tiles
      in Tanzania and 106 in the Philippines.
    origin: annotated-review
  - id: E2
    label: "Across tested products, false-negative rates using an IoU ≥ 0.5 criterion ranged from 0.55 to 0.85 in Tanzania and 0.70 to 0.83 in the Philippines."
    kind: data
    loc: "Methods pp. 12583–12584; Table II; discussion pp. 12587–12588"
    quote: |
      Across tested products, false-negative rates using an IoU ≥ 0.5
      criterion ranged from 0.55 to 0.85 in Tanzania and 0.70 to 0.83 in the
      Philippines.
    origin: annotated-review
  - id: E3
    label: "OSM ranged from high-quality targeted coverage to no buildings at all in some rural tiles."
    kind: paraphrase
    loc: "Methods pp. 12583–12584; Table II; discussion pp. 12587–12588"
    quote: |
      OSM ranged from high-quality targeted coverage to no buildings at all
      in some rural tiles.
    origin: annotated-review
  - id: E4
    label: "Google sometimes counted more buildings than the manual reference because the reference generalized adjacent buildings into one polygon while Google separated the structures."
    kind: paraphrase
    loc: "Methods pp. 12583–12584; Table II; discussion pp. 12587–12588"
    quote: |
      Google sometimes counted more buildings than the manual reference
      because the reference generalized adjacent buildings into one polygon
      while Google separated the structures.
    origin: annotated-review
claims:
  - claim: missing-footprints-push-estimates-down
    relationship: supports
    strength: high
    evidence: [E1, E2]
    note: >-
      False-negative rates of 0.55 to 0.85 in Tanzania and 0.70 to 0.83 in
      the Philippines against manually digitised reference tiles.
  - claim: no-single-provider-complete
    relationship: supports
    strength: high
    evidence: [E3, E4]
    note: >-
      OSM ranged from targeted high quality to no buildings at all. Google
      sometimes exceeded the reference because the reference generalised
      adjacent buildings into one polygon.
does_not_establish:
  - "The false-negative rate includes geometry mismatches at the IoU threshold, not only buildings missing entirely."
  - "Samples exclude some low-building and low-provider-coverage areas."
  - "No households or residents were observed."
  - "Results cover two countries, not Argentina."
---

Gevaert, Buunk, and van den Homberg audit global building datasets for
bias against manually digitised reference buildings in 100 stratified
tiles in Tanzania and 106 in the Philippines.

The false-negative rates are the load-bearing result for Barrios
Visibles. They establish that the dominant error in open footprint
data is missing buildings, which biases any footprint-derived
population estimate downward. The fourth finding is the necessary
caveat: polygon disagreement is sometimes a segmentation difference
rather than an omission.
