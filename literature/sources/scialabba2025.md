---
key: scialabba2025
status: retained
lang: es
verification: verified_secondary
strength: high
source_type: peer_reviewed
method: independent_analysis
evidence_type: [mechanism_evidence, direct_analogue]
unit_of_analysis: [dwelling, household, family]
geographies: [Argentina]
tags: [piezas-de-alquiler, inquilinato, CABA, household-definition, census-criteria, priority]
cited_in_manuscript: false
retrieved: 2026-09-15
follow_up: >-
  Quotes arrived through a page summary with a 125-character cap, so they are
  fragments rather than full sentences. Open the article, confirm each one in
  context, and transcribe Cuadro 2, which tabulates the enumeration criteria
  for rental rooms across the 1970 to 2022 censuses.
evidence:
  - id: E1
    label: Informal room rentals in dwellings and tenements are concealed by landlords during the census operation
    kind: verbatim
    loc: "Results, subsection Empadronamiento de hogares"
    quote: |
      generalmente ocultados por sus 'dueños' durante el operativo censal
    lang: es
    origin: manual
  - id: E2
    label: Difficulties identifying rental-room dwellings result in an underestimation of households
    kind: verbatim
    loc: "Results, subsection Empadronamiento de hogares"
    quote: |
      redundan en la subestimación de hogares
    lang: es
    origin: manual
  - id: E3
    label: In later censuses the problem became the hidden informal room-rental market in the densest villas
    kind: verbatim
    loc: "Results, subsection Empadronamiento de hogares"
    quote: |
      el mercado de alquiler informal de piezas oculto en las villas más
      densas
    lang: es
    origin: manual
  - id: E4
    label: Related household members occupy adjoining rooms with independent street exits while sharing food expenses
    kind: verbatim
    loc: "Results, subsection Empadronamiento de hogares, citing Marcos 2023"
    quote: |
      que residen en habitaciones contiguas con salida a la calle
      independiente, pero que comparten los gastos de alimentación
    lang: es
    origin: manual
  - id: E5
    label: Dwellings have more than one street access, and accesses that can hardly be treated as separate
    kind: verbatim
    loc: "Results, subsection Empadronamiento de hogares, citing Marcos 2023"
    quote: |
      viviendas con más de un acceso a la calle, accesos a la calle que
      difícilmente pueden ser considerados separados
    lang: es
    origin: manual
  - id: E6
    label: Enumeration criteria for rental rooms differed across the 1970 to 2022 censuses
    kind: data
    loc: "Cuadro 2"
    quote: |
      Criterios de empadronamiento de las piezas de alquiler. Argentina,
      censos 1970-2022.
    reference_kind: census
    lang: es
    origin: manual
  - id: E7
    label: Consequences are hard to quantify and concentrated mainly in CABA
    kind: paraphrase
    loc: "Results, subsection Empadronamiento de hogares"
    quote: |
      The authors state that the consequences of these enumeration
      difficulties are hard to quantify and are concentrated mainly in the
      Ciudad Autónoma de Buenos Aires.
    origin: manual
claims:
  - claim: footprint-not-one-household
    relationship: supports
    strength: high
    evidence: [E1, E3, E4, E5]
    note: >-
      The Argentine source for this claim, and the only one. Everything else
      supporting it comes from Kibera, Nairobi, or Port-au-Prince. Adjoining
      rooms with independent street exits that share food expenses is the
      footprint-to-household problem stated in Argentine census terms.
  - claim: census-net-omission-small-but-nonzero
    relationship: qualifies
    strength: high
    evidence: [E1, E2, E3]
    note: >-
      Names a specific, documented mechanism by which Argentine census
      household counts run low, and locates it in the densest villas. The
      authors decline to quantify it, so it qualifies the national figure
      rather than contradicting it.
  - claim: renabap-indec-not-independent
    relationship: qualifies
    strength: medium
    evidence: [E6]
    note: >-
      The household definition itself moved between censuses, so a
      RENABAP-to-INDEC comparison is comparing against a criterion that has
      not been stable.
  - claim: territorial-coverage-is-not-population-coverage
    relationship: supports
    strength: medium
    evidence: [E1]
    note: >-
      A dwelling an enumerator reaches can still hide households inside it, so
      completing a segment is not the same as counting its residents.
does_not_establish:
  - "It quantifies nothing. The authors state explicitly that the consequences are hard to quantify."
  - "It concerns the identification of households within dwellings, not the omission of whole dwellings or buildings from the census frame."
  - "The effect is concentrated in CABA, which is the one jurisdiction where footprint counts fall below the RENABAP registry. It does not transfer to horizontal settlements elsewhere."
  - "The quotes are recorded from a page summary rather than from the article, so none should be printed in the manuscript before someone opens it."
---

Scialabba and Marcos trace how Argentine censuses have counted households
from 1970 to 2022, and devote part of their results to rental rooms. Informal
room rental spread through dwellings and tenements as villas densified and
grew vertically, and landlords conceal those arrangements from enumerators.
The authors conclude that the resulting difficulty in identifying
rental-room dwellings underestimates households.

This is the Argentine evidence the registry was missing. Until now the claim that one
footprint can contain several households rested entirely on Kibera, Nairobi,
and Port-au-Prince. Here the same mechanism appears in a demography
journal, in Argentine census terms, with the effect placed in the densest
villas and concentrated in CABA.

Their Cuadro 2 is worth transcribing in full. It tabulates how each census
from 1970 onward decided whether a rented room counted as a separate dwelling,
which means the household denominator this project compares against has not
been defined the same way across rounds.
