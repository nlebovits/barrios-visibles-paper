---
key: indec2013ad35
status: retained
lang: es
verification: verified_secondary
strength: high
source_type: primary_official
method: demographic_reconciliation
evidence_type: [direct_analogue]
unit_of_analysis: [resident, national]
geographies: [Argentina]
tags: [INDEC, AD35, census-2010, omission, official]
cited_in_manuscript: false
retrieved: 2026-09-15
follow_up: >-
  Locate the 1.99 percent result and the sex and age breakdown in the
  publication.
evidence:
  - id: E1
    label: "Reported 40,117,096 people and corrected the total to 40,930,448, implying 813,352 omitted or 1.99 percent"
    kind: unlocated
    quote: |
      INDEC reported 40,117,096 people and demographically corrected the
      total to 40,930,448, implying 813,352 omitted people or 1.99%.
    reference_kind: modeled_estimate
    origin: litreview-docx
  - id: E2
    label: "Correction was larger for men at 2.44 percent than women at 1.55 percent, and largest for ages 0 to 14 at 3.8 percent"
    kind: unlocated
    quote: |
      The correction was larger for men (2.44%) than women (1.55%), and
      largest for ages 0-14 (3.8%).
    reference_kind: modeled_estimate
    origin: litreview-docx
claims:
  - claim: census-net-omission-small-but-nonzero
    relationship: supports
    strength: high
    evidence: [E1]
    note: >-
      The official 2010 figure.
  - claim: subgroup-errors-cancel-nationally
    relationship: supports
    strength: high
    evidence: [E2]
    note: >-
      The same pattern as 2022 appears in 2010: men and children
      undercounted more than women and working-age adults. The age-sex
      shape is demographically plausible, which is part of why the
      national figure is credible.
does_not_establish:
  - "It is a reconciliation, so it estimates a total rather than measuring coverage."
  - "No independent national post-enumeration survey accompanied the 2010 round, so the official figure cannot be checked against a direct measurement."
  - "It shares inputs with the independent estimates that agree with it, so their convergence is not full corroboration."
---

INDEC's Análisis Demográfico 35 corrects the 2010 census total from
40,117,096 to 40,930,448, implying 813,352 omitted people, or 1.99
percent. The correction runs larger for men than women and largest for
children under 15.

The age and sex shape is the same one that appears in 2022. That
consistency is evidence the reconciliation is capturing something real,
and it is also why the national total cannot vouch for subgroup
accuracy.
