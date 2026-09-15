---
key: ibge2024projmetodo
status: retained
lang: pt
verification: verified_secondary
strength: high
source_type: official_documentation
method: demographic_reconciliation
evidence_type: [mechanism_evidence]
unit_of_analysis: [national, jurisdiction]
geographies: [Brazil]
tags: [Brazil, projection, reconciliation, PES, small-area]
cited_in_manuscript: false
retrieved: 2026-09-15
follow_up: >-
  Preserve the projection methodology statement showing that the
  revision includes the post-enumeration survey.
evidence:
  - id: E1
    label: "Revised estimate for 1 July 2022 of 210,862,983, which is 7,782,227 above the published census total"
    kind: unlocated
    quote: |
      Revised estimate for 1 July 2022: 210,862,983. Difference from the
      final Census population: 7,782,227, or about 3.8%.
    origin: audit-notes
  - id: E2
    label: "The 2024 revision incorporates the 2022 Census, post-enumeration survey data, and demographic reconciliation for the 27 states"
    kind: unlocated
    quote: |
      The presentation states that the revision includes the 2022
      Census, post-enumeration survey data, and demographic
      reconciliation for the 27 states.
    origin: audit-notes
claims:
  - claim: reconciliation-does-not-repair-small-area-geography
    relationship: supports
    strength: high
    evidence: [E1, E2]
    note: >-
      Brazil produced a revised national baseline of 210.9 million using
      the census, the post-enumeration survey, and reconciliation, and
      left the published census tables intact. The later national
      estimate does not repair the original small-area geography.
  - claim: net-accuracy-differs-from-complete-enumeration
    relationship: supports
    strength: high
    evidence: [E1]
    note: >-
      Three legitimate population quantities coexist: people reached,
      the published total after imputation, and a later demographic
      estimate.
does_not_establish:
  - "It does not rewrite or correct the published census tables, which is the point rather than a limitation."
  - "It is a methodology presentation rather than a full technical report."
  - "An earlier working answer wrongly claimed the 210.9 million projection excluded the post-enumeration survey. This source states the opposite, and the corrected formulation is that Brazil used the census, post-enumeration evidence, and reconciliation to revise the projection while leaving the census geography alone."
---

IBGE's presentation on the 2024 projection revision states that the
revision incorporates the 2022 Census, post-enumeration survey data, and
demographic reconciliation for all 27 states. The resulting estimate for
July 1, 2022 is 210,862,983, or 7,782,227 above the published census
population.

The revision changed the demographic baseline and left the published
census tables where they were. A national reconciliation is not
evidence that small-area figures were repaired.
