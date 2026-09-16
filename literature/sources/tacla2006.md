---
key: tacla2006
status: retained
lang: es
verification: verified_secondary
strength: medium
source_type: review
method: demographic_reconciliation
evidence_type: [context]
unit_of_analysis: [national]
geographies: [Colombia, Guatemala, Venezuela]
tags: [CEPAL, CELADE, historical, omission, regional-review]
cited_in_manuscript: false
retrieved: 2026-09-15
follow_up: >-
  Confirm the Cuadro 1 row for Argentina against the rendered page. pdftotext
  scrambles the table columns, so the values were read by position.
evidence:
  - id: E1
    label: "Repeated national omission estimates above 7 to 15 percent across Latin America between 1950 and 2000"
    kind: unlocated
    quote: |
      Documents repeated national omission estimates above 7-15% and
      emphasizes that national averages conceal much larger geographic
      differences.
    origin: audit-notes
  - id: E2
    label: "Colombia 13.9 percent in 1970 and 11.3 percent in 1990, Guatemala 15.6 percent in 1980 and 14.5 percent in 1990, Venezuela 8.9 percent in 1990 and 7.5 percent in 2001"
    kind: unlocated
    quote: |
      Colombia 13.9% in 1970 and 11.3% in 1990; Guatemala 15.6% in 1980
      and 14.5% in 1990; Venezuela 8.9% in 1990 and 7.5% in 2001.
    origin: audit-notes
  - id: E3
    label: "Every omission figure in Cuadro 1 is an indirect evaluation, not a post-enumeration survey"
    kind: verbatim
    loc: "Cuadro 1 source line, p. 20"
    quote: |
      Fuente: Área Demografía, CELADE - División de Población de la CEPAL,
      evaluaciones indirectas. Revisión 2004 - 2005, realizadas por Giomar
      Bay.
    lang: es
    reference_kind: modeled_estimate
    origin: manual
  - id: E4
    label: "Argentina's recorded omission runs 1.4, 3.3, 2.8, 1.1, 1.1, and 2.8 percent across the 1950 to 2000 rounds"
    kind: data
    loc: "Cuadro 1, p. 20"
    quote: |
      Argentina: 1950 1,4; 1960 3,3; 1970 2,8; 1980 1,1; 1990 1,1; 2000 2,8.
      The asterisk on the 1980 and 1990 values marks "Nuevas proyecciones con
      censo de la ronda del 2000", not a change of method.
    reference_kind: modeled_estimate
    origin: manual
  - id: E5
    label: "Argentina's 1980 census was apparently not evaluated for omission by a direct method"
    kind: verbatim
    loc: "COTA 1980 round section"
    quote: |
      Al parecer, no se evaluó la omisión censal por método directo.
    lang: es
    origin: manual
  - id: E6
    label: "An earlier Argentine coverage evaluation was attempted and abandoned before the record matching finished"
    kind: verbatim
    loc: "COTA 1970 round section"
    quote: |
      Argentina intentó evaluar la cobertura del censo mediante la utilización
      de la Encuesta del Empleo cuyo levantamiento era cercana al censo,
      combinada con listas de nacidos vivos en el año anterior al censo, más
      una muestra de la población masculina que debía presentarse para cumplir
      el Servicio Militar Obligatorio. Sin embargo, no se llegó a completar
      las tareas de cotejo, por lo que no se pudo disponer de las conclusiones
      de dicha labor.
    lang: es
    origin: manual
claims:
  - claim: latin-american-omission-range-includes-six-percent
    relationship: qualifies
    strength: medium
    evidence: [E1, E2]
    note: >-
      Labelled by method. These are principally indirect demographic
      estimates and historical comparisons, not post-enumeration
      surveys, so they set historical context rather than a measured
      benchmark.
  - claim: net-accuracy-differs-from-complete-enumeration
    relationship: supports
    strength: medium
    evidence: [E1]
    note: >-
      The review's own emphasis is that national averages conceal much
      larger geographic differences.
  - claim: no-independent-pes-limits-verification
    relationship: supports
    strength: high
    evidence: [E3, E4, E5, E6]
    note: >-
      The decisive source for the Argentine case. Every figure in the
      regional table is an indirect evaluation, the 1980 round was
      apparently never evaluated by a direct method, and an earlier attempt
      was abandoned before the record matching finished. Together with the
      2001 survey being withheld and no survey run for 2010 or 2022, no
      published Argentine post-enumeration survey result exists in the
      modern series. Saying results have not been published "since 1991"
      overstates what was ever published.
does_not_establish:
  - "These are principally indirect demographic estimates and historical comparisons, not all direct post-enumeration surveys."
  - "The record covers 1950 to 2000, so it predates every census Barrios Visibles examines."
  - "It does not state that Argentina never ran a post-enumeration survey. It states that the figures in its own table are indirect, and that the 1980 round appears to lack a direct evaluation."
  - "Cuadro 1 was read through pdftotext, which scrambles the column order. The Argentine values should be confirmed against the rendered page before publication."
  - "The publication year and series number are not recorded."
---

Tacla Chamy's CEPAL and CELADE review documents census omission across
Latin America from 1950 to 2000, with repeated national estimates above
7 to 15 percent. Colombia reached 13.9 percent in 1970, Guatemala 15.6
percent in 1980, and Venezuela 8.9 percent in 1990.

The review's own emphasis matters as much as the figures. National
averages conceal much larger geographic differences, which is the
argument Barrios Visibles makes for Argentina at barrio scale.
