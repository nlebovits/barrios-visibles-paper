---
key: kuffer2016
status: retained
lang: en
verification: verified_full_text
strength: high
source_type: review
method: literature_review
evidence_type: [context, method_validation]
unit_of_analysis: [settlement, roof, building]
geographies: []
tags: [review, slum-mapping, morphology, VHR-imagery, gateway-source]
cited_in_manuscript: true
retrieved: 2026-09-15
follow_up: >-
  Locate the recurring-limitations passage, the 87 case-study count, and the
  slum morphological signature on the page.
evidence:
  - id: E1
    label: Reviews 87 slum-mapping case studies published from 2000 through 2015
    kind: unlocated
    quote: |
      Reviews 87 slum-mapping case studies published from 2000 through 2015.
    sample_size: 87 case studies
    origin: annotated-review
  - id: E2
    label: Official information on settlement extent, population, buildings, and boundaries is frequently missing or inconsistent
    kind: unlocated
    quote: |
      Establishes that official information on settlement extent, population,
      buildings, and boundaries is frequently missing or inconsistent.
    origin: annotated-review
  - id: E3
    label: Very high resolution imagery can extract roof or dwelling level information for settlement mapping and population estimation
    kind: unlocated
    quote: |
      Reviews evidence that VHR imagery can extract roof- or dwelling-level
      information for settlement mapping and population estimation.
    origin: annotated-review
  - id: E4
    label: Recurring limitations are small buildings, extreme roof density, overlapping roofs, verticality, contextual diversity, and weak reference data
    kind: unlocated
    quote: |
      Identifies small buildings, extreme roof density, overlapping roofs,
      verticality, contextual diversity, and weak reference data as recurring
      limitations.
    origin: annotated-review
  - id: E5
    label: Diagnostic slum signature is higher roof coverage density, organic patterns, and small building sizes
    kind: unlocated
    quote: |
      The diagnostic slum signature is higher roof coverage density, organic
      patterns, and small building sizes.
    origin: manuscript
  - id: E6
    label: Slum mapping reviews report dwellings below 20 square metres
    kind: unlocated
    quote: |
      Slum mapping reviews report dwellings below 20 m² and note that
      extraction algorithms both delete small dwellings as noise and merge
      adjacent ones.
    origin: manuscript
claims:
  - claim: footprints-contain-population-information
    relationship: context_only
    strength: high
    evidence: [E3]
    note: >-
      Reviews the evidence rather than producing it. Cite the primary studies
      for any number.
  - claim: informal-population-underrepresentation
    relationship: supports
    strength: medium
    evidence: [E2]
    note: >-
      Official settlement information is frequently missing or inconsistent,
      which is the precondition for undercount.
  - claim: missing-footprints-push-estimates-down
    relationship: supports
    strength: medium
    evidence: [E4, E6]
    note: >-
      Small buildings, extreme roof density, overlapping roofs, and
      verticality all suppress detected counts.
  - claim: planar-counts-conservative-when-vertical
    relationship: supports
    strength: medium
    evidence: [E5]
    note: >-
      The morphology used to detect slums is a dwelling stock at occupational
      saturation, with the built fraction approaching the parcel fraction.
      That independently supports a dwelling yield near one.
does_not_establish:
  - "It is a review and not a direct undercount measurement."
  - "It does not calibrate an area threshold for filtering footprints. The 6 and 10 square metre cuts in the manuscript stay uncalibrated."
  - "It leads to the Gunter, Galeon, Kit, and Kibera studies, so maintenance rule 2 applies: cite those originals for their numbers rather than this review."
---

Kuffer, Pfeffer, and Sliuzas review fifteen years of slum mapping from remote
sensing, covering 87 case studies. The review establishes both that official
settlement information is frequently missing and that very high resolution
imagery can recover roof or dwelling level detail.

The morphological signature matters twice for this project. It describes a
built fraction approaching the parcel fraction, with circulation reduced to
footpaths, which is what a dwelling yield near one assumes. It also fixes the
scale of real dwellings, which constrains how aggressively footprints can be
filtered by area.

This is also the registry's gateway to several primary sources. Gunter,
Galeon, Kit, and the Kibera studies all reach the project through it.
