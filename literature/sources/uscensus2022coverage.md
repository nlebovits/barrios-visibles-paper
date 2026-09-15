---
key: uscensus2022coverage
status: retained
lang: en
verification: verified_secondary
strength: high
source_type: primary_official
method: post_enumeration_survey
evidence_type: [mechanism_evidence]
unit_of_analysis: [resident, national]
geographies: [United States]
tags: [gross-versus-net, PES, coverage-estimates, priority]
cited_in_manuscript: false
retrieved: 2026-09-15
follow_up: >-
  Record the specific coverage-estimate table behind the 18.8 million
  omissions figure, and the Census Bureau's definition of an omission.
evidence:
  - id: E1
    label: "Post-enumeration survey estimated 18.8 million omissions while national net coverage error was not statistically significant"
    kind: unlocated
    quote: |
      The post-enumeration survey estimated 18.8 million omissions even
      though national net coverage error was not statistically
      significant.
    origin: audit-notes
claims:
  - claim: net-accuracy-differs-from-complete-enumeration
    relationship: supports
    strength: high
    evidence: [E1]
    note: >-
      The clearest single demonstration in the registry that a close
      national total and a complete count are different claims. 18.8
      million omissions coexist with no statistically significant net
      error.
  - claim: imputation-is-not-enumeration
    relationship: context_only
    strength: medium
    evidence: [E1]
does_not_establish:
  - "The United States is outside the Latin American comparison set."
  - "It establishes the conceptual distinction and gives no Argentine figure."
  - "The offsetting erroneous enumerations are what make net error small, so the case cannot be used to argue that omissions were hidden rather than offset."
---

The 2020 United States census post-enumeration survey estimated 18.8
million omissions while the national net coverage error stayed
statistically indistinguishable from zero.

This is the clearest available separation of gross omission from net
coverage error. Roughly 18 million erroneous enumerations offset the
omissions, and the net undercount came to about 782,000. A national
total can be close while millions of people were never reached.
