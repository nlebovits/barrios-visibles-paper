---
key: ibge2024ppe
status: retained
lang: pt
verification: verified_secondary
strength: high
source_type: primary_official
method: post_enumeration_survey
evidence_type: [direct_analogue]
unit_of_analysis: [resident, household]
geographies: [Brazil]
tags: [PES, coverage-measurement, Brazil, favelas, priority]
cited_in_manuscript: false
retrieved: 2026-09-15
follow_up: >-
  Retrieve the final technical tables and the exact definitions of the
  denominators used for gross omission and net coverage error. The
  landing page alone is not enough to quote from.
evidence:
  - id: E1
    label: "Person omission of 12.2 percent measured by post-enumeration survey"
    kind: unlocated
    quote: |
      12.2% person omission; 3.3% erroneous inclusion; 8.3% net coverage
      error.
    origin: audit-notes
  - id: E2
    label: "Access problems in favelas include multiple dwellings on one plot where only the front dwelling is discovered"
    kind: unlocated
    quote: |
      IBGE materials and reporting identify access problems in favelas
      and dense communities, including multiple dwellings on a single
      plot where only the front dwelling is discovered.
    origin: audit-notes
claims:
  - claim: latin-american-omission-range-includes-six-percent
    relationship: supports
    strength: high
    evidence: [E1]
    note: >-
      Direct coverage measurement, not a disagreement with projections.
      The proportional omission is substantially larger than a
      three-million-person discrepancy against Argentina's 2022
      population, which is the strongest available answer to the claim
      that a roughly 6 percent Argentine gap is intrinsically
      impossible.
  - claim: net-accuracy-differs-from-complete-enumeration
    relationship: supports
    strength: high
    evidence: [E1]
    note: >-
      One survey reports gross omission, erroneous inclusion, and net
      coverage error as three separate quantities. 12.2 percent omission
      against 8.3 percent net error is the distinction in a single
      number set.
  - claim: footprint-not-one-household
    relationship: supports
    strength: medium
    evidence: [E2]
    note: >-
      The documented access failure is the mechanism: only the front
      dwelling on a plot gets found.
does_not_establish:
  - "It measures Brazilian coverage. It does not show that INDEC committed the same error."
  - "The figures are recorded from the landing page and secondary reporting, so the denominators behind each percentage are not yet verified."
  - "A post-enumeration survey measures coverage of the census as fielded. It does not attribute the omission to any particular settlement type without the subgroup tables."
---

IBGE's post-enumeration survey for the 2022 Brazilian census measured
12.2 percent person omission, 3.3 percent erroneous inclusion, and 8.3
percent net coverage error.

This is the strongest regional precedent in the registry. It is direct
coverage measurement rather than a disagreement between a census and a
projection, and the proportional omission exceeds the Argentine
discrepancy Barrios Visibles reports. IBGE materials attribute part of
the access problem to favelas and dense communities, where several
dwellings share a plot and only the front one is found.
