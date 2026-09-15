---
key: chamberlain2024
status: retained
lang: en
verification: verified_full_text
strength: high
source_type: peer_reviewed
method: remote_sensing
evidence_type: [caution, method_validation]
unit_of_analysis: [building, jurisdiction]
geographies: []
tags: [provider-comparison, Google, Microsoft, Ecopia, OSM, Africa]
cited_in_manuscript: false
retrieved: 2026-09-15
follow_up: >-
  Locate the mean footprint counts in the results tables.
evidence:
  - id: E1
    label: "Across 879 first-level administrative units, mean footprint counts were approximately 556,615 for Ecopia, 534,676 for Google, 241,978 for Microsoft, and 110,616 for OSM."
    kind: data
    loc: "Results pp. 11–12 and Figure 1; discussion pp. 21–23"
    quote: |
      Across 879 first-level administrative units, mean footprint counts
      were approximately 556,615 for Ecopia, 534,676 for Google, 241,978 for
      Microsoft, and 110,616 for OSM.
    origin: annotated-review
  - id: E2
    label: "Google and Ecopia generally had the highest counts and strongest spatial similarity."
    kind: paraphrase
    loc: "Results pp. 11–12 and Figure 1; discussion pp. 21–23"
    quote: |
      Google and Ecopia generally had the highest counts and strongest
      spatial similarity.
    origin: annotated-review
  - id: E3
    label: "Microsoft showed visible missing-imagery tiles and major-city gaps in some countries."
    kind: paraphrase
    loc: "Results pp. 11–12 and Figure 1; discussion pp. 21–23"
    quote: |
      Microsoft showed visible missing-imagery tiles and major-city gaps in
      some countries.
    origin: annotated-review
  - id: E4
    label: "OSM was geographically widespread but had the lowest footprint counts and areas."
    kind: paraphrase
    loc: "Results pp. 11–12 and Figure 1; discussion pp. 21–23"
    quote: |
      OSM was geographically widespread but had the lowest footprint counts
      and areas.
    origin: annotated-review
  - id: E5
    label: "The authors conclude there is no universally best or interchangeable product."
    kind: paraphrase
    loc: "Results pp. 11–12 and Figure 1; discussion pp. 21–23"
    quote: |
      The authors conclude there is no universally best or interchangeable
      product.
    origin: annotated-review
claims:
  - claim: no-single-provider-complete
    relationship: supports
    strength: high
    evidence: [E1, E2, E3, E4, E5]
    note: >-
      Across 879 administrative units the mean counts run from about 556,615
      for Ecopia to 110,616 for OSM. The authors conclude no product is
      universally best or interchangeable.
does_not_establish:
  - "Agreement between Google and Ecopia does not prove either is complete."
  - "The analysis lacks authoritative ground truth and covers Africa rather than Argentina."
  - "Image acquisition dates differ."
---

Chamberlain and colleagues compare building footprint products across
countries in Africa, covering 879 first-level administrative units and
four providers: Ecopia, Google, Microsoft, and OpenStreetMap.

The spread between providers is the finding. It is large enough that a
footprint count is a property of the product as much as of the ground.
The spread is the argument for the VIDA union used in Barrios
Visibles, and the reason that union cannot be called complete.
