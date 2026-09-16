---
key: okyere2025
status: retained
lang: en
verification: verified_full_text
strength: low
source_type: preprint
method: remote_sensing
evidence_type: [caution]
unit_of_analysis: [building]
geographies: []
tags: [arXiv, weak-evidence, OSM-reference, provider-disagreement, do-not-overclaim]
cited_in_manuscript: true
retrieved: 2026-09-15
follow_up: >-
  Locate the polygon counts and overlap percentages on the page.
evidence:
  - id: E1
    label: "Compares Google, Microsoft/VIDA, and OSM footprint geometry across Accra, Nairobi, Caracas, Berlin, and Houston."
    kind: unlocated
    quote: |
      Compares Google, Microsoft/VIDA, and OSM footprint geometry across
      Accra, Nairobi, Caracas, Berlin, and Houston.
    origin: annotated-review
  - id: E2
    label: "Accra: 2,619,136 Google polygons versus 292,038 OSM polygons."
    kind: unlocated
    quote: |
      Accra: 2,619,136 Google polygons versus 292,038 OSM polygons.
    origin: annotated-review
  - id: E3
    label: "Caracas: 387,049 Google polygons versus 12,395 OSM polygons."
    kind: unlocated
    quote: |
      Caracas: 387,049 Google polygons versus 12,395 OSM polygons.
    origin: annotated-review
  - id: E4
    label: "Only 8.19% of Google polygons overlapped OSM in Accra and 3.97% in Caracas, while 61% and 57% of OSM polygons overlapped Google, respectively."
    kind: unlocated
    quote: |
      Only 8.19% of Google polygons overlapped OSM in Accra and 3.97% in
      Caracas, while 61% and 57% of OSM polygons overlapped Google,
      respectively.
    origin: annotated-review
  - id: E5
    label: "Geometric agreement was poorer in Caracas than in the formal Global North comparison cities."
    kind: unlocated
    quote: |
      Geometric agreement was poorer in Caracas than in the formal Global
      North comparison cities.
    origin: annotated-review
claims:
  - claim: no-single-provider-complete
    relationship: qualifies
    strength: low
    evidence: [E1, E4, E5]
    note: >-
      Usable only for the weak claim that providers disagree and that
      complex urban morphology reduces polygon alignment. Its bibliography
      leads to gevaert2024, chamberlain2024, and herfort2023, which are
      stronger.
does_not_establish:
  - "that Google systematically omits Caracas or Accra buildings;"
  - "that OSM represents ground truth;"
  - "that low polygon overlap measures real-world building completeness;"
  - "anything about population, dwellings, households, or census accuracy."
  - "The analysis explicitly assumes OSM is closer to ground truth despite its own counts showing that OSM is dramatically sparser. Non-overlap therefore cannot distinguish missing Google buildings from missing OSM buildings, segmentation differences, dates, or geometry mismatch. Some discussion language conflates disagreement with omission."
---

Okyere, Lu, and Brunn compare Google, Microsoft/VIDA, and
OpenStreetMap footprint geometry across Accra, Nairobi, Caracas,
Berlin, and Houston. It is an unreviewed preprint with no population
ground truth.

The analysis assumes OpenStreetMap is closer to ground truth while its
own counts show OSM is far sparser: 292,038 OSM polygons against
2,619,136 Google polygons in Accra. Non-overlap cannot
separate a missing Google building from a missing OSM building, a
segmentation difference, or a date mismatch. Some of its discussion
conflates disagreement with omission.
