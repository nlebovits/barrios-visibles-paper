---
key: sirko2021
status: retained
lang: en
verification: verified_secondary
strength: medium
source_type: preprint
method: remote_sensing
evidence_type: [method_validation]
unit_of_analysis: [building]
geographies: [Africa]
tags: [open-buildings, deep-learning, provenance, google]
cited_in_manuscript: true
retrieved: 2026-09-15
follow_up: >-
  Locate the reported detection performance and the confidence-score
  definition in the preprint, and record the section.
evidence:
  - id: E1
    label: Continental-scale building detection applies a deep learning model to high-resolution satellite imagery
    kind: unlocated
    quote: |
      The Google V3 Open Buildings footprints are derived from deep learning
      models applied to high-resolution satellite imagery.
    origin: manuscript
  - id: E2
    label: VIDA distributes Google output already filtered to footprints with confidence at or above 0.65
    kind: unlocated
    quote: |
      The VIDA dataset already represents Google's quality-filtered output,
      footprints with confidence >= 0.65.
    origin: manuscript
claims:
  - claim: no-single-provider-complete
    relationship: supports
    strength: medium
    evidence: [E1, E2]
    note: >-
      Model-derived footprints fail in correlated ways across similar
      morphology, so a detection shortfall in one dense settlement predicts a
      shortfall in the next. Provenance is why the errors are not independent.
  - claim: missing-footprints-push-estimates-down
    relationship: supports
    strength: medium
    evidence: [E2]
    note: >-
      A confidence threshold removes false positives and cannot recover false
      negatives, so the filter the data ships with biases counts downward.
does_not_establish:
  - "It reports model performance, not dwelling or household counts."
  - "It does not report Argentine detection accuracy, nor accuracy stratified by informal versus formal morphology."
  - "It is an arXiv preprint describing one of three inputs to the VIDA union, so it does not characterise the union this project actually uses."
---

Sirko and colleagues describe the model behind Google Open Buildings, which
detects building footprints across continental extents from high-resolution
satellite imagery. It is one of three inputs to the VIDA combined layer used
here, alongside Microsoft GlobalMLBuildingFootprints and OpenStreetMap.

Provenance matters for the error structure. Model-derived footprints fail in
correlated ways across similar morphology, so detection shortfalls cluster in
exactly the settlements the analysis is about. The confidence filter VIDA
inherits removes false positives and cannot recover false negatives.
