---
key: indec2025ad39
status: retained
lang: es
verification: verified_secondary
strength: high
source_type: primary_official
method: demographic_reconciliation
evidence_type: [direct_analogue]
unit_of_analysis: [resident, national]
geographies: [Argentina]
tags: [INDEC, AD39, census-2022, net-differential, subgroup, priority]
cited_in_manuscript: false
retrieved: 2026-09-15
evidence:
  - id: E1
    label: "Reconciliation estimated 46,122,853 residents at census date against 45,886,580 enumerated in the age-sex base, a signed difference of -0.5 percent"
    kind: data
    loc: "table 4"
    quote: |
      INDEC's 2025 cohort-component reconciliation estimated 46,122,853
      residents at census date, compared with 45,886,580 enumerated
      people in the age-sex analytical base. The signed difference was
      -0.5%, or 236,273.
    reference_kind: modeled_estimate
    origin: litreview-docx
  - id: E2
    label: "Including the 5,705 people counted in street situations without age gives a gap of about 230,568"
    kind: data
    loc: "table 4"
    quote: |
      Once the 5,705 people counted in street situations without age are
      included, the gap is approximately 230,568.
    reference_kind: modeled_estimate
    origin: litreview-docx
  - id: E3
    label: "Men were 2.1 percent below the demographic estimate and women 1.1 percent above it"
    kind: data
    loc: "table 4"
    quote: |
      Men were 2.1% below the demographic estimate, women 1.1% above it.
    reference_kind: modeled_estimate
    origin: litreview-docx
  - id: E4
    label: "Ages 0 to 14 were 3.5 percent below and ages 15 to 64 were 0.6 percent above"
    kind: data
    loc: "table 4"
    quote: |
      Ages 0-14 were 3.5% below the demographic estimate, and ages 15-64
      were 0.6% above.
    reference_kind: modeled_estimate
    origin: litreview-docx
  - id: E5
    label: "The sex-based gross differential was 1.6 percent against a net differential of 0.5 percent"
    kind: data
    loc: "table 4"
    quote: |
      The sex-based gross differential was 1.6%.
    reference_kind: modeled_estimate
    origin: litreview-docx
claims:
  - claim: census-net-omission-small-but-nonzero
    relationship: supports
    strength: high
    evidence: [E1, E2]
    note: >-
      The source of the 0.5 percent figure that anchors every claim
      about 2022 accuracy.
  - claim: subgroup-errors-cancel-nationally
    relationship: supports
    strength: high
    evidence: [E3, E4, E5]
    note: >-
      The decisive numbers. A 0.5 percent net differential sits on top
      of a 1.6 percent gross differential by sex alone, with men 2.1
      percent low and women 1.1 percent high. The national fit is
      produced partly by cancellation.
  - claim: net-accuracy-differs-from-complete-enumeration
    relationship: supports
    strength: high
    evidence: [E1, E5]
    note: >-
      0.5 percent is a signed difference against a demographic estimate.
      It is not a count of people missed.
does_not_establish:
  - "The 0.5 percent is a net differential against a model, not a direct estimate of every missed person."
  - "A cohort-component reconciliation tests aggregate demographic consistency. It does not show that each person was enumerated or correctly located."
  - "It carries no subnational coverage estimate, so it says nothing about any barrio."
---

INDEC's Análisis Demográfico 39 reconciles the 2022 census against a
cohort-component projection. It estimates 46,122,853 residents at census
date against 45,886,580 enumerated in the age-sex analytical base, a
signed difference of 0.5 percent, or about 230,568 people once street
residents without age are included.

The subgroup table is what matters. Men run 2.1 percent below the
demographic estimate and women 1.1 percent above. Ages 0 to 14 run 3.5
percent below and ages 15 to 64 run 0.6 percent above. The sex-based
gross differential is 1.6 percent against a net differential of 0.5
percent.

So the close national fit is produced partly by errors that cancel.
Citing 0.5 percent as the census omission rate misstates what the table
reports.
