---
key: gonzalez2013
status: retained
lang: es
verification: verified_secondary
strength: medium
source_type: peer_reviewed
method: demographic_reconciliation
evidence_type: [direct_analogue]
unit_of_analysis: [resident, national]
geographies: [Argentina]
tags: [AEPA, census-2010, independent-estimate, omission]
cited_in_manuscript: false
retrieved: 2026-09-15
follow_up: >-
  Locate the 2.44 percent estimate and the 1,000,778 figure in the
  proceedings. The title is recorded from a truncated citation.
evidence:
  - id: E1
    label: "Independent projection put the 2010 gap at 2.44 percent, about 1,000,778 people"
    kind: unlocated
    quote: |
      González, Ribotta and Torres projected a 2.44% gap, about
      1,000,778 people.
    reference_kind: modeled_estimate
    origin: litreview-docx
claims:
  - claim: census-net-omission-small-but-nonzero
    relationship: qualifies
    strength: medium
    evidence: [E1]
    note: >-
      An independent estimate above INDEC's own 1.99 percent. Labelled
      by method: it is a projection, not a coverage measurement, and it
      shares inputs with the official figure.
  - claim: no-independent-pes-limits-verification
    relationship: supports
    strength: medium
    evidence: [E1]
    note: >-
      Independence here is partial. The projection inherits the adjusted
      2001 base, births, deaths, and uncertain migration, so agreement
      with INDEC is informative rather than independent.
does_not_establish:
  - "It is an indirect demographic projection, not a dual-system or post-enumeration estimate."
  - "It shares the adjusted 2001 base and vital statistics with the official estimate, so it is not fully independent of it."
  - "The published record is a conference paper and the title in the bib entry is truncated."
---

González, Ribotta, and Torres estimate the omission of Argentina's 2010
census indirectly, arriving at 2.44 percent, or roughly 1,000,778
people. That sits above INDEC's own 1.99 percent.

The convergence across studies near 1 to 2.5 percent is the useful
result. The disagreement within that band is smaller than the
shared-input problem, so none of them answers the question alone.
