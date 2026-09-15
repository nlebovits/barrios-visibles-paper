---
key: indec2005ad32
status: retained
lang: es
verification: verified_secondary
strength: high
source_type: primary_official
method: demographic_reconciliation
evidence_type: [direct_analogue]
unit_of_analysis: [resident, national]
geographies: [Argentina]
tags: [INDEC, AD32, census-2001, omission, reconciliation]
cited_in_manuscript: false
retrieved: 2026-09-15
follow_up: >-
  Read the operational and demographic components off pp. 4-9 and 16-18
  and confirm the 1.90 and 0.85 percentage-point split.
evidence:
  - id: E1
    label: "Published 2001 count of 36,260,130 raised to 36,944,597 by targeted operational reconstruction"
    kind: data
    loc: "pp. 4-9"
    quote: |
      The published count was 36,260,130. INDEC's targeted operational
      reconstruction added 684,467 people, producing 36,944,597.
    reference_kind: census
    origin: litreview-docx
  - id: E2
    label: "INDEC-CELADE reconciliation produced 37,282,970, or 2.75 percent omission"
    kind: data
    loc: "pp. 16-18"
    quote: |
      A subsequent INDEC-CELADE demographic reconciliation produced
      37,282,970, 1,022,840 above the raw count, or 2.75% omission.
    reference_kind: modeled_estimate
    origin: litreview-docx
  - id: E3
    label: "Of the 2.75 percent, 1.90 points came from operational evidence and 0.85 points were a residual demographic adjustment"
    kind: data
    loc: "pp. 16-18"
    quote: |
      Of this, 1.90 percentage points came from operational evidence and
      0.85 points were a residual demographic adjustment.
    reference_kind: modeled_estimate
    origin: litreview-docx
  - id: E4
    label: "The operational method was geographically differentiated and found the largest difficulties in major urban centres"
    kind: paraphrase
    loc: "pp. 4-9"
    quote: |
      The operational component used precensus dwelling counts,
      supervisors' summary forms, incomplete interviews and assumed
      household size. It was geographically differentiated and
      identified the largest difficulties in major urban centers,
      including Greater Buenos Aires, La Plata, Córdoba and Rosario.
    origin: litreview-docx
  - id: E5
    label: "The targeted dwelling method was not applied in rural areas because the rural frame had not been updated"
    kind: paraphrase
    loc: "pp. 4-9"
    quote: |
      The targeted dwelling method was not applied in rural areas
      because the rural frame had not been adequately updated. Low rural
      adjustment is therefore not proof of high rural completeness.
    origin: litreview-docx
claims:
  - claim: census-net-omission-small-but-nonzero
    relationship: supports
    strength: high
    evidence: [E1, E2, E3]
    note: >-
      The official 2001 figure, and the only Argentine round where
      operational field evidence carries most of the adjustment rather
      than a demographic residual.
  - claim: official-enumeration-omits-areas
    relationship: supports
    strength: medium
    evidence: [E4, E5]
    note: >-
      INDEC's own method found the largest difficulties in major urban
      centres and skipped rural areas for want of an updated frame.
does_not_establish:
  - "It is a reconciliation, not a post-enumeration survey, so it estimates a total rather than measuring coverage person by person."
  - "The 0.85 percentage-point residual was allocated proportionally because INDEC lacked evidence for differential allocation. The national adjustment is more defensible than the resulting local corrections."
  - "Low rural adjustment reflects the method not being applied there, not high rural completeness."
---

INDEC's Análisis Demográfico 32 documents how population coverage was
estimated for the 2001 census. A targeted operational reconstruction
added 684,467 people to the published 36,260,130, and an INDEC-CELADE
reconciliation then produced 37,282,970, implying 2.75 percent omission.

Of those 2.75 percentage points, 1.90 rest on operational field evidence
and 0.85 are a residual demographic adjustment allocated proportionally. That makes the national figure better supported than any
local correction derived from it.
