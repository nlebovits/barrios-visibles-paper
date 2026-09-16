---
key: idecba2026
status: retained
lang: es
verification: verified_secondary
strength: high
source_type: primary_official
method: direct_enumeration
evidence_type: [direct_analogue]
unit_of_analysis: [dwelling, resident, census_area]
geographies: [Argentina]
tags: [IDECBA, Padre-Ricciardelli, Villa-1-11-14, processing-loss, CABA, priority]
cited_in_manuscript: false
retrieved: 2026-09-15
follow_up: >-
  Extract the complete Annex II tables and the geographic definitions.
  Resolve the geographic-unit differences between IDECBA's 3,640, Tejido
  Urbano's 6,868, and broader Padre Ricciardelli totals that include
  housing complexes.
evidence:
  - id: E1
    label: "INDEC F2 operational sheets recorded 4,906 visited dwellings and 23,213 people"
    kind: unlocated
    quote: |
      Operational sheets: 4,906 visited dwellings and 23,213 people.
    origin: audit-notes
  - id: E2
    label: "Published Redatam data for the same radios show 1,118 dwellings and 3,640 people"
    kind: unlocated
    quote: |
      Published Redatam data: 1,118 dwellings and 3,640 people.
    origin: audit-notes
  - id: E3
    label: "The difference is 3,788 dwellings and 19,573 people"
    kind: unlocated
    quote: |
      Difference: 3,788 dwellings and 19,573 people.
    origin: audit-notes
  - id: E4
    label: "IDECBA describes the difference as subenumeracion u omision censal"
    kind: unlocated
    quote: |
      subenumeración u omisión censal
    lang: es
    origin: audit-notes
claims:
  - claim: local-processing-loss-documented
    relationship: supports
    strength: high
    evidence: [E1, E2, E3, E4]
    note: >-
      The strongest Argentine evidence in the registry, and it needs no
      footprints. People present in INDEC's own field-summary records
      are absent from the published small-area data, so the loss falls
      between field collection and publication.
  - claim: net-accuracy-differs-from-complete-enumeration
    relationship: supports
    strength: high
    evidence: [E3]
    note: >-
      19,573 people in one barrio is devastating locally and about 0.04
      percent of the national total, which is why a close national
      figure cannot vouch for small-area data.
does_not_establish:
  - "The figures concern the villa-sector radios analysed in the annex, not necessarily every housing complex included in broader definitions of Barrio Padre Ricciardelli."
  - "It documents one barrio. It does not establish a national omission rate or that the same loss occurred elsewhere."
  - "It compares operational sheets with published results. It does not explain which processing step lost the records."
---

IDECBA, the statistical office of the City of Buenos Aires, compares
INDEC's own F2 Resumen de Fracción operational sheets against INDEC's
published Redatam results for the same radios in Barrio Padre
Ricciardelli. The sheets record 4,906 visited dwellings and 23,213
people. The published data show 1,118 dwellings and 3,640 people.

The gap of 19,573 people is nearly direct evidence that records
collected in the field did not reach the published small-area tables. It
uses only INDEC's own paperwork, independent of building footprints,
occupancy assumptions, and Barrios Visibles. IDECBA calls it
subenumeración u omisión censal.
