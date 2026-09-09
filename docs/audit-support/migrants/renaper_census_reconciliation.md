# RENAPER vs Census 2022: reconciling the foreign-born totals

Date: 2026-09-09. Companion to `docs/indec-reconciliation-audit.md`. Detail and every citation are in `census_foreign_born_findings.md` and `renaper_findings.md` in this folder.

## Question

RENAPER reported 3,033,786 foreign-born persons with a digital DNI and residence in Argentina in August 2022. Census 2022 counted 1,933,463 foreign-born in private dwellings on 18 May 2022. The gap is 1,100,323. How much of it is people the census missed?

## Answer

Little of it. Between about 0.74 and 1.5 million of the RENAPER records were for people not resident in Argentina. The plausible census-side undercount of the foreign-born is 10,000 to 250,000, central value about 100,000. The gap is a register-residence problem, not a census-coverage measurement.

## The two universes

| | RENAPER, Aug 2022 | Census, 18 May 2022 |
|---|---|---|
| Unit | Record of a living person with a digital-process DNI, an Argentine domicile, and no DNM record of absence over six months | Habitual resident enumerated in a private dwelling |
| Excludes | Holders of pre-2009 paper documents; persons with precaria, transitoria, or temporaria status awaiting a DNI; persons without any DNI | Collective dwellings (267,793 persons, foreign-born share unpublished); street population (5,705) |
| Country of birth | Recorded for all | Unknown for 179,239 (9.3%) |
| Death removal | Civil-registry notification; no channel for deaths abroad of non-nationals | Not applicable |
| Emigration removal | Only if DNM recorded an exit and no return within six months; exits on foreign passports are not matched; a foreign national's DNI cannot carry a foreign address | Not applicable |

## Comparison by country of birth

Census counts adjusted by redistributing the 179,239 unknown-country cases proportionally (factor 1.1022).

| Country | RENAPER | Census | Ratio | Census adjusted | Ratio adjusted |
|---|---:|---:|---:|---:|---:|
| Ecuador | 27,350 | 8,879 | 3.08 | 9,786 | 2.79 |
| China | 51,361 | 18,629 | 2.76 | 20,533 | 2.50 |
| Colombia | 111,969 | 46,482 | 2.41 | 51,232 | 2.19 |
| Bolivia | 658,559 | 338,299 | 1.95 | 372,872 | 1.77 |
| Brazil | 94,897 | 49,943 | 1.90 | 55,047 | 1.72 |
| Peru | 289,430 | 156,251 | 1.85 | 172,219 | 1.68 |
| Paraguay | 900,238 | 522,598 | 1.72 | 576,005 | 1.56 |
| Spain | 71,064 | 48,492 | 1.47 | 53,448 | 1.33 |
| Chile | 211,662 | 149,082 | 1.42 | 164,318 | 1.29 |
| Venezuela | 220,595 | 161,495 | 1.37 | 177,999 | 1.24 |
| Uruguay | 128,333 | 95,384 | 1.35 | 105,132 | 1.22 |
| Italy | 88,799 | 68,169 | 1.30 | 75,136 | 1.18 |
| Total | 3,033,786 | 1,933,463 | 1.57 | | 1.57 |

Paraguay, Bolivia, and Peru hold 831,079 of the raw gap. Italy, the oldest and least mobile stock, has the lowest ratio.

## Comparison by age

RENAPER age structure digitized from the report's population pyramid, validated against its sex totals within 0.02 points.

| Age | Ratio RENAPER / census |
|---|---:|
| 0-4 | 0.38 |
| 15-19 | 1.31 |
| 25-29 | 1.97 |
| 30-34 | 2.00 |
| 35-39 | 1.82 |
| 45-49 | 1.50 |
| 60-64 | 1.43 |
| 75-79 | 1.35 |
| 85-89 | 1.25 |
| 95-99 | 1.14 |
| All ages | 1.57 |

The excess peaks at working ages and falls with age. Unpurged deaths would produce the opposite shape. The register's share aged 65+ is 17.5% against the census's 20.4%.

## What each definitional difference can explain

Sign convention: + inflates RENAPER relative to the census and helps explain the gap; − deflates RENAPER and makes the true gap larger.

| Factor | Direction | Low | High | Central | Basis |
|---|---|---:|---:|---:|---|
| a. Deaths not purged | + | 0 | 120,000 | 40,000 | Expected deaths in the stock 37,809 per year; 53% at 80+, where the register/census ratio is only 1.29. More than 120,000 unpurged deaths would push the true 80+ ratio below 0.71. |
| b. Non-residents retained (emigrated, circular, exit unrecorded) | + | 780,000 | 1,483,000 | 1,155,000 | Residual of the identity. Independent checks: excess over the elderly reference ratio of 1.30-1.35 gives 460,000-547,000 as a floor; RENAPER itself removed 563,333 records by Aug 2024 and 683,970 by Jun 2025 with no published note. |
| c. Digital-DNI-only exclusion | − | 0 | 100,000 | 40,000 | Would bite on elderly Europeans; Europe ratio 1.46 vs all-origin 1.57 shows only a mild deficit. DNI renewal is compulsory, so few paper documents remain. |
| d. Date, 18 May to 31 Aug 2022 | ~0 | −15,000 | 15,000 | 0 | Net non-native inflow about +9,741 over the interval; deaths in the stock about −10,870. |
| e. Persons without a DNI, counted by census only | − | 130,000 | 300,000 | 190,000 | ENMA 2020: 11% of migrants without DNI; ENMA 2023: 7%. About half of them are legally regular and awaiting the document. Concentrated in NOA (24%) and NEA (23%) vs AMBA (5.8%). |
| f. Country-of-birth coding | ± | −20,000 | 50,000 | 10,000 | Both sources use place of birth. Small residual for Argentines born abroad to Argentine parents holding a DNI while living abroad. |
| g. Census universe excludes collective dwellings | + | 12,000 | 45,000 | 25,000 | 273,498 persons outside the census universe; foreign-born share unpublished; prisons and geriatric homes dominate. |
| h. Census under-enumeration of the foreign-born | + | 10,000 | 250,000 | 100,000 | National net differential −0.5%, men −2.1%. Sex ratio: census 121.7 women per 100 men vs RENAPER 107.0; imposing the register ratio on the census female count implies about 120,000 men missing. No migrant-specific omission rate published. |
| Observed gap | | | | 1,100,323 | Identity: gap = (a + b + f + g + h) − (c + e). |

## Reading

1. Factor b dominates. The register kept people who left. RENAPER's later series confirms it: the same definition gives 2,470,453 in August 2024 and 2,349,816 in June 2025, a fall of 684,000 with no methodological note. UN DESA cut its Argentina migrant stock by 16.2% in its 2024 revision on the strength of the census, and R4V replaced RENAPER with the census as its source for Venezuelans.
2. Factor h is the only part of the gap that is census undercount. Its range is 10,000 to 250,000. The upper end rests on the sex-ratio argument and on AD39's finding that men were undercounted by 2.1% nationally. INDEC's own demographer (Ameijeiras 2025, AEPA) reports the same country pattern and calls the register "francas distancias" from the census, without a magnitude.
3. Factors c and e run the other way. The register cannot see 130,000 to 300,000 migrants without a DNI, concentrated among precarious and recent arrivals in the NOA and NEA. For work on informal settlements this is the exclusion that matters. The register cannot correct it.
4. The best single figure for resident foreign-born at mid-2022 is the census figure raised for the collective-dwelling universe and for probable undercount of migrant men: about 1.96 to 2.23 million. This brackets UN DESA's revised 1,912,294 for mid-2020 and 1,958,039 for mid-2024.

## Consequence for the audit memo

The migration row in Section 3 of `docs/indec-reconciliation-audit.md` had used the full 1.1 million RENAPER gap as an upper bound on the census-dependence channel. That bound is now 250,000, central 100,000. The combined worst case for a 3 million national undercount falls back to about 2.65 million, below the 2.77 million required, even with every other component at its extreme.

Early in this session I told the user the country pattern pointed at Paraguayan, Bolivian, and Peruvian migrants as undercounted at a scale of a few hundred thousand. That read used the Italy and Spain ratios as a register-inflation baseline. The age profile shows the inflation is concentrated at working ages, so the baseline from elderly stocks understates it. The corrected reading is the one above.

## Not established

- Foreign-born count in collective dwellings (asked in the census, never published).
- Any migrant-specific 2022 omission rate from INDEC.
- RENAPER's purge rules for deaths abroad and for unmatched exits, and the method behind the 2022-2025 decline in its series.
- The share of the census "country unknown" group by true origin.
- Any radio-level or settlement-level foreign-born comparison.
