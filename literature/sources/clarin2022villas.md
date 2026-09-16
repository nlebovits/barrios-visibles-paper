---
key: clarin2022villas
status: retained
lang: es
verification: verified_secondary
strength: medium
source_type: journalism
method: journalism
evidence_type: [mechanism_evidence, caution]
unit_of_analysis: [household, settlement]
geographies: [Argentina]
tags: [CABA, census-operation, referentes, journalism, citation-incomplete]
cited_in_manuscript: false
retrieved: 2026-09-15
follow_up: >-
  Recover a stable archived URL. The article URL now redirects to the Clarín
  homepage. Confirm the author rather than retaining the provisional "Gómez,
  2022" shorthand; the saved record does not preserve enough metadata to
  support that byline.
evidence:
  - id: E1
    label: Census enumeration in the city's villas was assigned to the Ministerio de Desarrollo Humano y Hábitat
    kind: paraphrase
    loc: "6 May 2022 article"
    quote: |
      Census enumeration in the city's villas was assigned to the Ministerio
      de Desarrollo Humano y Hábitat.
    origin: audit-notes
  - id: E2
    label: The operation was coordinated through barrio referentes, delegates, recognized residents, and social organizations
    kind: verbatim
    loc: "6 May 2022 article"
    quote: |
      Estamos coordinando con los referentes barriales, con los delegados y
      los vecinos más reconocidos; también con las organizaciones sociales.
    lang: es
    origin: audit-notes
  - id: E3
    label: Preparatory population projections began with the 2010 Census and were updated with subsequent local information
    kind: paraphrase
    loc: "6 May 2022 article"
    quote: |
      Preparatory population projections began with the 2010 Census and were
      updated using subsequent local information.
    reference_kind: census
    origin: audit-notes
claims:
  - claim: renabap-indec-not-independent
    relationship: supports
    strength: medium
    evidence: [E1, E2]
    note: >-
      The other half of the claim, and the only direct evidence for it. The
      CABA census operation used the same categories of territorial
      intermediary that sisu2023 shows RENABAP using formally. Strength is
      capped at medium because the source is a contemporary news report with
      an unconfirmed byline and no stable URL.
  - claim: census-net-omission-small-but-nonzero
    relationship: qualifies
    strength: medium
    evidence: [E3]
    note: >-
      Preparatory estimates for the villas were anchored to the 2010 census
      baseline. In a settlement type that grew over the intervening twelve
      years, a stale prior biases the operational target downward.
does_not_establish:
  - "It reports CABA only. No nationwide documentation of the same operational arrangement has been located, so the arrangement cannot be assumed for other provinces."
  - "It does not show that INDEC copied RENABAP's published family totals, nor that the two used the same questionnaire or database."
  - "Operational overlap alone does not prove a national population undercount of roughly three million people."
  - "It is journalism, so it carries a single official's account of the operation rather than an audited description of it."
---

A Clarín report from May 6, 2022 describes how the 2022 Census would enumerate
the population of the villas in the Ciudad Autónoma de Buenos Aires.
Enumeration there went to the Ministerio de Desarrollo Humano y Hábitat, and
the operation was coordinated through barrio referentes, delegates, recognized
residents, and social organizations.

This is the only direct evidence that the census operation used the same
territorial intermediaries RENABAP formally relies on. That makes it load
bearing for the independence claim and simultaneously the weakest link in it.
The byline is unconfirmed, the URL no longer resolves, and the account covers
one jurisdiction.
