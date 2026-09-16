---
key: lanacion2022villa2124
status: retained
lang: es
verification: verified_secondary
strength: medium
source_type: journalism
method: journalism
evidence_type: [mechanism_evidence]
unit_of_analysis: [household, dwelling, building]
geographies: [Argentina]
tags: [La-Nacion, Villa-21-24, enumeration-conditions, verticality, inquilinato]
cited_in_manuscript: false
retrieved: 2026-09-15
follow_up: >-
  Preserve the exact enumerator quotations and speaker names. The byline
  is not recorded.
evidence:
  - id: E1
    label: "Buildings up to five stories with narrow internal passages"
    kind: unlocated
    quote: |
      Buildings up to five stories; narrow internal passages.
    origin: audit-notes
  - id: E2
    label: "Several households behind a single apparent entrance, and an inquilinato containing as many as ten households"
    kind: unlocated
    quote: |
      Several households behind a single apparent entrance; an
      inquilinato containing as many as ten households.
    origin: audit-notes
  - id: E3
    label: "Enumerators reported difficulty tracking which dwellings had been visited"
    kind: unlocated
    quote: |
      Enumerators reporting difficulty tracking which dwellings had been
      visited.
    origin: audit-notes
claims:
  - claim: footprint-not-one-household
    relationship: supports
    strength: medium
    evidence: [E1, E2]
    note: >-
      Argentine field evidence for the mechanism marx2019 and ono2020
      measure elsewhere. An inquilinato with ten households behind one
      entrance is one footprint.
  - claim: building-method-is-conservative-in-vertical-settlements
    relationship: supports
    strength: high
    evidence: [E1, E2]
    note: >-
      Barrios Visibles does not infer these households. Where INDEC
      reports more people than the building-based floor, the analysis
      keeps INDEC's value, so hidden vertical and subdivided households
      push the estimate down.
  - claim: official-enumeration-omits-areas
    relationship: supports
    strength: medium
    evidence: [E3]
    note: >-
      Enumerators losing track of which dwellings were visited is an
      operational omission mechanism reported as it happened.
does_not_establish:
  - "It is journalism from one settlement on Census Day, not a measurement."
  - "It documents conditions that make omission likely. It does not establish that omission occurred or its size."
  - "The byline and the exact quotations are not yet recorded."
---

La Nación reported from Villa 21-24 on Census Day 2022. Enumerators
described buildings up to five stories, narrow internal passages,
several households behind one apparent entrance, an inquilinato holding
as many as ten households, and difficulty tracking which dwellings they
had already visited.

The report documents the mechanism by which both a conventional census
and a one-footprint-one-household model miss residents. For Barrios
Visibles the direction matters: the analysis never infers these extra
households, so they make the published floor conservative.
