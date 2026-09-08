---
layout: post.njk
title: "Barrios Visibles: Building-footprint evidence of a systematic population undercount in Argentina's informal settlements"
author: Nissim Lebovits
affiliation: Independent Researcher
email: nlebovits@pm.me
orcid: 0009-0001-5083-9838
date: 2026-04-16
tags: ["writing", "research", "geospatial"]
bibliography: paper/references.bib
csl: paper/cambridge-a.csl
link-citations: true
---

## Abstract

Argentina's Registro Nacional de Barrios Populares (RENABAP) lists approximately 1.24 million families across 6,467 registered informal settlements. I compare this enumeration with 1.97 million building footprints spatially joined to the same settlement polygons. Detected footprints exceed recorded families by 59% in raw counts. A per-settlement household floor, defined as the larger of the recorded family count and the footprint count scaled by RENABAP's 1.1 families-per-dwelling ratio, exceeds the national RENABAP total by 83%. Population inference remains conditional on occupancy and demographic assumptions: the resulting range is 6.3 to 7.6 million residents, approximately 2.9 to 3.4 million above RENABAP's implied figure. The range indicates approximate magnitude. Results differ by settlement form. RENABAP exceeds footprint-derived estimates in consolidated, vertically developed settlements in the Ciudad Autónoma de Buenos Aires, while footprints predominate in horizontal settlements elsewhere. A separate comparison with allocated Census 2022 population declines from a ratio of 2.62 to 1.88 as the analysis is restricted to tracts increasingly covered by registered settlements. The Census comparison provides robustness evidence whose independence is limited by shared inputs and institutional context. Open building data also provide a reproducible view of the built environment against which administrative population records can be audited.

## Policy Significance Statement

Open building-footprint datasets now provide sufficiently complete coverage to provide an independent view of the built environment for public agencies, community organizations, researchers, and other users. They can help identify where administrative population records may be stale or incomplete and where field verification or updated enumeration should be prioritized. In Argentina's registered informal settlements, visible structures substantially exceed official family estimates in most places, although translating structures into population still requires explicit occupancy and demographic assumptions. Building footprints measure the built environment; population remains inferred. Used carefully, they are a low-cost audit and planning tool that can make gaps in public data visible before those gaps distort infrastructure, service-delivery, and risk-management decisions.

**Keywords:** informal settlements; building footprints; population estimation; administrative data quality; Argentina

---

## 1. Motivation

In 2025, I worked with the municipality of La Plata, Argentina to assess flood risk in informal settlements. The city's GIS team had been relying on RENABAP (Registro Nacional de Barrios Populares), Argentina's national registry of informal settlements, and I set out to supplement it with building footprint data for more precise household estimates [@smith2019]. The counts diverged sharply. Across La Plata's informal settlements, roughly 72,000 building footprints intersect polygons for which RENABAP lists only 34,000 families [@lebovits2025laplata] — and in one Los Hornos settlement, RENABAP's 330 families sit against more than 4,200 footprints clearly visible in satellite imagery.

[An author-produced overlay shows the building footprints and satellite basemap for this La Plata settlement](https://nlebovits.github.io/ciut-riesgo/renabap_files/figure-html/fig-ejemplos-barrios-adicionales-output-3.png). It is linked rather than reproduced pending confirmation of the underlying basemap's publication permissions.

RENABAP's official documentation provides several plausible explanations for this large gap. RENABAP grew through a sequence of normatively-bounded survey waves: an initial 2015 to 2016 mass survey by TECHO, Cáritas, and UTEP-affiliated movements covering localities above 10,000 inhabitants, formalized as 4,100 barrios via Decreto 358/2017 (cutoff 31 December 2016); a 2017 update to 4,228 barrios via AABE Resolution 275/2017; a 2021 extension to localities of 2,000 to 10,000 inhabitants, formalized as 4,561 barrios via Decreto 880/2021 (cutoff 31 December 2018); and a further update via Decreto 573/2023 (cutoff 31 December 2021) [@sisu2023, pp. 3–6]. Family counts are not derived from a household census but from a three-source estimation combining referente declarations, field enumerator counts, and satellite-image dwelling counts, multiplied by a national average of 1.1 families per inhabited dwelling (pp. 14–15, 24). For many settlements, the underlying dwelling estimates are 5 to 10 years old as of this writing. The registry also explicitly excludes dispersed rural population (p. 6). Settlement boundaries are also frozen at registration cutoffs (2016, 2018, 2021), so settlements that emerged or were reconfigured after these dates aren't in the registry. New settlements formed during the post-2023 economic deterioration are entirely missing, as the last available data were posted in December of 2023.

Academic and policy literature also affirms broad precedent for systemic population undercounts in informal settlements [@breuer2024; @kuffer2022; @thomson2021], and offers reasons for difficulties in keeping census data in sync with the actual population of informal settlements, including infrequent census cycles and budgetary constraints on national statistical offices, particularly in resource-constrained contexts [@leete2001], and government non-recognition of informal settlements themselves [@avis2016].

In La Plata, I was able to present my findings to the municipal government, which has now incorporated the data into their first-ever master plan [@resa2025]. Yet the scale of the discrepancy in La Plata — a city of only 800,000 people — made me wonder what this gap looked like nationally.

Recent national-scale work has begun to surface the geographic bias in informal-settlement monitoring. @samper2025 use RENABAP to show that the largest total informal-settlement area in Argentina is not in Greater Buenos Aires (216 km²) but in extra-small urban areas of 2,000 to 50,000 residents (267 km²), and that smaller cities expanded faster between 2016 and 2023 — up to 2.78% annually in small urban areas versus 1.44% in large metropolitan areas. Their analysis takes RENABAP's polygons and family counts as given. This paper is complementary. Their question is where the registered area is concentrated and how fast it grows. Mine is whether the recorded household count inside RENABAP's own polygons matches the built evidence. These critiques operate on orthogonal axes — geographic coverage and internal enumeration — and, as discussed in §5, their implications compound.

---

## 2. Data Sources

This analysis uses four datasets.

**Settlement boundaries and family counts** come from RENABAP (Registro Nacional de Barrios Populares), the official Argentine registry of barrios populares. Following national-government restructuring, formal responsibility for RENABAP administration and evaluation, including follow-up, rests with the Secretaría de Obras Públicas; the relevant functions did not disappear with changes to the former Secretaría de Integración Socio-Urbana [@decreto764; @decreto70]. This formal continuity is distinct from the age of the public data. The dataset used here contains 6,467 settlement polygons with associated names and estimated family counts, totaling 1,237,795 families nationally. According to the registry's official methodology manual [@sisu2023], its sources include declarations by community referentes and on-the-ground enumerator counts. Satellite-image dwelling counts provide a third source [@sisu2023, p. 24]. Family counts are estimated by applying a national multiplier of 1.1 families per inhabited dwelling, a ratio derived from subsequent house-by-house surveys across registered barrios (pp. 14–15). The snapshot used here, dated 6 December 2023, is the most recent publicly available release and was obtained via the Mapa de Barrios Populares [@renabap2023].

RENABAP was created by Decreto 358/2017 and given its operational mandate by Ley 27.453 (2018), which declares the integración socio urbana of registered barrios to be of public interest. That law defines integración socio urbana as a suite of actions — expansion of social infrastructure, service access, treatment of public spaces, environmental sanitation and mitigation, strengthening of family economic activities, parcelary redimensioning, tenure security, and dominial regularization — of which titling is one component among many. The registry's own baja criteria follow from this. A barrio leaves the registry only after it gains both dominial regularity and formal service access, never on titling alone [@sisu2023]. Municipal and provincial governments use RENABAP to target infrastructure investment (water, sewer, electrification, stormwater); national programs including the Fondo de Integración Socio Urbana allocate resources against the registry; and — as in La Plata's recent master plan — it is the de facto population basis for planning in the absence of any alternative settlement-level census product.

**Building footprints** come from the combined Google-Microsoft-OpenStreetMap dataset assembled by VIDA, which merges Google's V3 Open Buildings, Microsoft's GlobalMLFootprints, and OpenStreetMap into one global dataset of approximately 2.7 billion footprints, distributed via Source Cooperative as country-partitioned GeoParquet files [@vida2024]. The Google [@sirko2021] and Microsoft [@microsoft2022] footprints are derived from deep learning models applied to high-resolution satellite imagery; OSM footprints are human-contributed. VIDA was selected for its ease of access at the time the original La Plata analysis was conducted in August 2025; alternative sources such as Overture Maps, which offers a similar combined building layer with more frequent updates, would be reasonable substitutes for future iterations. These datasets have been validated as reliable inputs for high-resolution population estimation [@boo2022].

Building-footprint derivation from satellite imagery is imperfect, particularly in dense urban contexts, where detection accuracy is somewhat lower in informal settlements than in formally-planned neighborhoods [@okyere2025]. The VIDA snapshot used here was last updated in September 2024, predating any subsequent construction in actively growing settlements. I do not apply confidence filtering: the VIDA dataset already represents Google's quality-filtered output (footprints with confidence ≥ 0.65), and the relevant source of uncertainty in informal-settlement detection is false negatives — structures missed by the model — which no confidence threshold can address. I do apply area filtering as a sensitivity test, reporting results across lower thresholds of 0, 6, and 10 m². These thresholds are calibrated to exclude clearly non-residential micro-structures (latrines, sheds, animal enclosures) while retaining all footprints plausibly inhabitable as one-room dwellings. I do not apply an upper threshold. Large structures in informal settlements are predominantly multi-family residential, so filtering them would undercount rather than overcount. Full sensitivity tables are reported in the supplementary material.

**Urban-extent classification** uses the Planta Urbana layer published by Argentina's Instituto Geográfico Nacional [@ign2021], which delineates each Planta Urbana polygon as an approximate urban area covering the contiguous zone of built blocks with recognizable limits. The layer belongs to IGN's Hábitat e Infraestructura Social dataset. It covers Argentina and arrives as a monthly shapefile in WGS 1984 (EPSG:4326). It is used here to classify each RENABAP settlement as intersecting or not intersecting an IGN-recognized urban area, supporting the urban/non-urban split reported in the supplementary material.

**Census population and private-dwelling totals** come from INDEC's 2022 Census REDATAM release, joined to a corrected version of the official census-radio cartography [@indec2023; @indec2024; @lebovits2025census; @rodriguez2024]. The processed tract file contains 66,502 radios with 45,618,784 people and 17,783,028 private dwellings. The smaller total than INDEC's later revised national population reflects the variables and geographic records available in the tract-level processing file; the comparison below uses the same file throughout and does not substitute the later national total. The analysis uses VIV_TOT_P as a count of private dwellings, which may be occupied or unoccupied and may contain more than one household. Ratios formed with this field are described as persons per private dwelling. Household size is a different measure.

---

## 3. Results

Across 6,467 registered settlements, 1,969,975 building footprints intersect settlement polygons — 59% more than RENABAP's 1,237,795 recorded families. Applying RENABAP's own 1.1 families-per-dwelling ratio to footprint counts and taking the per-settlement household floor defined in §4.2 yields an estimated 2,265,499 households, or 83% above the official figure. Under conservative population multipliers, this implies a total informal-settlement population of roughly 6.3 to 7.6 million, against an official total of 3.5 to 4.1 million.

**Table 1. National summary.**

| Metric | RENABAP Official | Building-Based Estimate | Difference |
| --- | --- | --- | --- |
| Settlements | 6,467 | 6,467 | — |
| Building footprints (within polygons) | — | 1,969,975 | — |
| Families / households | 1,237,795 | 2,265,499 | +1,027,704 (+83.0%) |
| Population (×2.8) | 3,465,826 | 6,343,398 | +2,877,572 |
| Population (×3.35) | 4,146,613 | 7,589,423 | +3,442,810 |
| Undercount as share of Argentina's population | — | — | 6.2% – 7.4% |

**Table 2. Settlements by aglomerado tier.**

| Aglomerado tier | Settlements | RENABAP higher | Footprints higher | Median ratio (footprints / families) |
| --- | --- | --- | --- | --- |
| CABA | 49 | 43 | 6 | 0.53 |
| Conurbano-AMBA | 1,307 | 176 | 1,127 | 1.76 |
| Other Gran Aglomerados | 850 | 108 | 739 | 1.73 |
| Outside Aglomerados | 4,259 | 302 | 3,938 | 1.88 |

In CABA, building footprints undercount families due to vertical multi-story construction in consolidated villas. Everywhere else, the pattern reverses: building counts substantially exceed official family estimates, even after applying RENABAP's own 1.1 families-per-dwelling multiplier.

### 3.1 Census 2022 robustness comparison

Census 2022 provides a useful second official comparison, although not an independent population ground truth. INDEC publishes population at census-radio rather than building level. I initially allocated each radio's population to intersecting barrios in proportion to intersection area. This assumes uniform population density within each radio and can assign too little population to a dense barrio occupying a small portion of a large radio. The unfiltered result is biased upward.

To reduce this problem, I calculated the fraction of each radio covered by all intersecting RENABAP polygons and progressively excluded radios below specified coverage thresholds. At every threshold, a barrio remains in the comparison only if eligible radios cover at least half its area. If the discrepancy were only an areal-allocation artifact, the ratio would approach parity as the threshold increased. It declines, but remains substantial.

**Table 3. Footprint-based population relative to Census 2022 allocated population.**

| Minimum barrio coverage of eligible radios | Barrios | Footprints | Allocated Census population | Footprint-based population (×3.35) | Ratio |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0% | 6,467 | 1,969,975 | 2,518,282 | 6,599,416 | 2.62 |
| 25% | 2,151 | 1,364,480 | 2,010,840 | 4,571,008 | 2.27 |
| 50% | 1,089 | 959,971 | 1,479,959 | 3,215,903 | 2.17 |
| 75% | 544 | 607,405 | 990,041 | 2,034,807 | 2.06 |
| 90% | 304 | 405,682 | 687,672 | 1,359,035 | 1.98 |
| 95% | 223 | 305,226 | 542,938 | 1,022,507 | 1.88 |

At the 75% threshold, the ratio is 1.72 using 2.80 persons per footprint, 1.91 using 3.12, and 2.06 using 3.35. The 3.12 value is the observed ratio of people to private dwellings across all barrio-intersecting radios. It is an intermediate sensitivity value. The private-dwelling denominator prevents a direct household-size interpretation. Radios with at least 75% barrio coverage contain 3.25 people per enumerated private dwelling, compared with 2.57 nationally in the processed radio file.

A further diagnostic classified radios with at least 1% barrio coverage, radios within 2 km but without that coverage, and more distant radios, then restricted the comparison to urban radios. Adjacent radios did not show the elevated persons-per-private-dwelling ratio that systematic reassignment of barrio residents would predict. Adjacent radios contained 2.55 people per private dwelling, close to the national 2.57 value, so the diagnostic provides no strong evidence of spillover. Its design cannot independently determine whether residents absent inside barrios are also absent from the national total.

The Census comparison uses different population totals from RENABAP, but it shares the building-footprint baseline and cannot be described as fully statistically or institutionally independent. Census enumeration in informal settlements and RENABAP have also used overlapping territorial organizations and earlier census baselines. The result supplies additional robustness evidence: the discrepancy falls under safer spatial comparisons but does not collapse toward parity. No second national estimate of missing residents is produced from this comparison.

---

## 4. Methodology

In this analysis, I aggregated building footprints to settlement boundaries using a spatial join. The use of building footprints as a proxy for household counts is an established methodology in high-resolution population estimation [@boo2022]. This approach is also consistent with RENABAP's own methodology, which uses satellite imagery to manually count dwellings as one of three converging sources for its population estimates [@sisu2023, p. 24].

### 4.1 Counting Building Footprints

The analysis itself proceeded in three steps. First, both datasets were downloaded for the sake of query speed, rather than sourced remotely. The data were then converted to optimized GeoParquet files, including ZSTD compression, Hilbert spatial sorting, optimized row group sizes, and bounding box covering metadata, all to enable efficient spatial queries on large datasets. This was done using geoparquet-io (https://geoparquet.io/). The third step processed the data in DuckDB with simple spatial queries. Building footprints were joined to settlement boundaries using spatial intersection. This query counts the number of building footprints that intersect each settlement polygon. With spatial indexing from the optimization step, the join across 6,467 settlement boundaries and 33.8 million national building footprints completes in approximately 3 seconds. A second spatial join against IGN's Planta Urbana layer flags each settlement as intersecting or not intersecting an IGN-recognized urban area. This flag is descriptive, not generative — it does not enter the household-floor calculation in §4.2 — and supports the urban/non-urban split reported in Appendix A.2.

### 4.2 Assessing Household Undercount

For each settlement, I take the household floor as the maximum of (a) RENABAP's recorded family count and (b) the detected building-footprint count scaled by RENABAP's own 1.1 families-per-dwelling ratio [@sisu2023, pp. 14–15], optionally discounted by an occupation rate in sensitivity analysis. The occupation rate is applied only to the building-derived side; RENABAP already provided an enumerated family count that requires no further discount. The floor's components capture different mechanisms of undercount, and which one is larger depends on how the settlement is built. In low-rise settlements, each footprint corresponds to at least one dwelling, so the footprint-derived count establishes the floor. In multi-story settlements, one footprint contains stacked dwellings, so the footprint count understates households, and RENABAP's field walk-through enumeration establishes the floor instead. I am not estimating the household count in each settlement; I am establishing a floor below which it cannot reasonably fall.

Summed nationally, raw building footprints exceed official RENABAP family estimates by 59%, and the per-settlement household floor exceeds RENABAP's total by 83%. Footprints (scaled by 1.1) are the larger value in 5,810 of 6,467 settlements; RENABAP is larger in 655 (the remainder are ties). Because CABA's reverse pattern partially offsets the peripheral undercount in the national aggregate, the true peripheral undercount is larger than the national headline suggests.

The regimes are geographically distinct. In the Ciudad Autónoma de Buenos Aires, RENABAP records 80,517 families across 27,987 footprints: a median ratio of 0.53, or roughly 1.9 families per footprint, consistent with the consolidated multi-story villas that characterize the city (comparable to the approximately three families per structure documented in Mexico City's Isidro Fabela; @reyes2021). Outside CABA the pattern reverses: building counts substantially exceed official family estimates. This is consistent with a broad international literature showing that conventional population products systematically undercount informal settlements. @thomson2021 offer the clearest benchmark: comparing nine widely-used gridded population datasets (LandScan, WorldPop, HRSL, GRID3, GHS-POP, and others) against resident-enumerated counts across 118 slum settlements in Lagos, Port Harcourt, and Nairobi, they found that every product severely underestimated slum populations, with the best performer (HRSL) capturing only 39% of field-referenced residents. The undercount was worst in the densest settlements. They attribute this to two structural problems that apply directly to RENABAP: top-down disaggregation assumes admin-unit average densities hold at fine scale (collapsing precisely where density is most extreme), and most products lack a building-density auxiliary that would let the model resolve intra-urban heterogeneity. Related work reaches similar conclusions across other contexts [@breuer2024; @carrhill2013; @kuffer2022; @lucci2018]. That these regimes are geographically distinct is what justifies settlement-level maxima over one national multiplier — different settlements undercount through different mechanisms, and a uniform correction would obscure rather than reveal the pattern.

Within Conurbano-AMBA, vertical density decays sharply with distance from the urban core. Eighty-eight percent of CABA settlements show vertical density, with a median ratio of 0.53. The inner ring of partidos adjacent to CABA approaches this; the outer ring drops to single digits.

**Table 4. Vertical density gradient across Conurbano partidos.**

| Partido | Ring | N settlements | RENABAP higher | % vertical |
| --- | --- | --- | --- | --- |
| Vicente López | Inner | 15 | 8 | 53% |
| San Isidro | Inner | 17 | 9 | 53% |
| General San Martín | Inner | 45 | 22 | 49% |
| Lanús | Inner | 26 | 11 | 42% |
| Tres de Febrero | Inner | 20 | 8 | 40% |
| Malvinas Argentinas | Outer | 53 | 5 | 9% |
| Tigre | Outer | 67 | 5 | 8% |
| Almirante Brown | Outer | 74 | 5 | 7% |
| Merlo | Outer | 90 | 6 | 7% |

Vertical-density rates fall further outside AMBA. Among Other Gran Aglomerados, 108 of 850 settlements (13%) have RENABAP counts above the footprint-derived estimate. Outside any aglomerado, only 302 of 4,259 (7%) do. The gradient tracks informal-settlement consolidation theory: older core-adjacent settlements have had longer to densify vertically, while newer peripheral settlements remain horizontal.

### 4.3 Estimating Total Population

Total population estimates use two persons-per-household multipliers: 2.8, the 2022 INDEC national average [@indec2023], and 3.35, derived from RENABAP's own 2016–2017 enumeration of 526,686 families and 1,763,248 persons across 4,428 settlements [@siempro2021, p. 7]. The lower figure provides a conservative floor against the national distribution; the higher figure reflects the larger household sizes documented in barrios populares.

Applied to the 2,265,499 household floor (no size filter, 100% occupation), these multipliers yield a baseline national estimate of 6,343,398 to 7,589,423 informal-settlement residents. Under the most conservative sensitivity specification (≥10 m² footprint filter, 85% occupation rate, 2.8 persons per household), the estimate remains at 5,340,576 residents — still well above RENABAP's implied total of roughly 3.5 million. Full sensitivity analysis is reported in the supplementary material.

#### 4.3.1 On occupation rates

The sensitivity analysis in §4.3 treats occupation rates of 85%, 90%, 95%, and 100%, but the lower end of that range is almost certainly too conservative for informal settlements. Evidence from ethnography, remote sensing, and the structural literature converges on the claim that habitable dwellings in informal settlements are effectively always occupied.

First, ethnographic and urban-studies work on Buenos Aires villas documents that once a settlement has no more horizontal space, it densifies vertically and develops an internal informal rental market. @rodriguez2018, following @cravino2006, document this transition directly. From the mid-1990s onward, agotamiento de los predios vacantes — exhaustion of vacant lots — drove vertical growth in the traditional villas. Informal mechanisms for sale-purchase of dwellings and room rental accompanied it, and intensified in the following decade. They note that the informal "secondary" market has grown sharply because "in many cities it is no longer possible to occupy more land — there is none left" [@rodriguez2018, p. 127; my translation]. According to @rodriguez2018, citing @cravino2008, villa population in CABA grew 52.3 percent between the 2001 and 2010 censuses (from 107,422 to 163,587 inhabitants) while villas occupied only 1.46 percent of CABA's territory. @benitez2022 extends the observation: informal residents in central CABA grew from 52,000 in 1991 to contested current estimates of approximately 227,000 even as few new settlements emerged and existing ones expanded little horizontally, with estimates suggesting that 30 to 50 percent of residents of CABA informal settlements now rent rooms. The mechanism — population growth without footprint growth — is exactly the geometry that makes a footprint-based population floor under-count in CABA specifically.

Second, the remote-sensing literature converges on the same conclusion from morphology. @kuffer2016 identify the diagnostic slum signature as higher roof coverage density, organic patterns, and small building sizes. This is, in effect, the morphology of a dwelling stock at occupational saturation — circulation reduced to footpaths, the built fraction approaching the parcel fraction. @mahabir2018 describe the standard slum life-cycle as infancy → consolidation → maturity, with vertical densification possible at the maturity stage. The morphology used to detect informal settlements from satellite imagery is, in effect, the physical signature of a stock at or approaching occupational saturation.

Third, the structural literature frames informal settlements as the persistent housing outcome of a binding supply shortage. @unhabitat2003 identifies the drivers of slum formation as rapid rural-to-urban migration, urban poverty and inequality, inability of the urban poor to access affordable land, and insufficient investment in low-income housing. @unhabitat2016 documents the resulting trajectory. Public housing declined in the late twentieth century and informal settlements burgeoned. Absolute slum population grew from 689 million in 1990 to 880 million in 2014, even as the proportion of the urban population in slums fell from 46.2 to 29.7 per cent over the same period. Informal stock in this framing is not residual temporary overflow; it is the standing housing solution for a large and growing population unable to access formal alternatives. UN-Habitat's operational slum definition incorporates overcrowding — more than three people sharing the same habitable room — as one of five core deprivations [@unhabitat2018]; a stock defined by overcrowding cannot by construction contain much vacancy.

Formal resettlement housing built to replace informal settlements often stands empty, or intended residents reject it. That apparent counterexample deserves preemption. @unhabitat2003 documents that forced relocation destroys affordable stock while replacement housing frequently turns out to be unaffordable, with relocated households moving back into slum accommodation. @benitez2022 describes the same pattern in the Playón de Chacarita relocation programme in Buenos Aires, where community organizers and residents express serious reservations about the planned move to adjacent social-housing apartment buildings. This is a distinct phenomenon — formal-sector supply failing to match demand characteristics — and does not bear on whether the informal stock itself clears. If anything it strengthens the argument: residents prefer staying in fully-occupied informal dwellings to moving to formal alternatives.

The 85% floor in the sensitivity table is a deliberately permissive lower bound rather than a central estimate. It absorbs a second source of uncertainty not captured by the vacancy literature — the fraction of detected footprints that are habitable dwellings rather than sheds, latrines, kitchen outbuildings, or partial construction. Vacancy of habitable dwellings itself is best treated as near zero.

### 4.4 Census comparison method

For every census radio intersecting a RENABAP polygon, I calculate its spheroidal area, the area intersecting each barrio, and the share of the radio covered by all barrios. Population is allocated to a barrio as the radio total multiplied by the barrio-radio intersection area divided by radio area. Threshold scenarios retain only radios whose total barrio coverage is at least 0%, 10%, 25%, 50%, 75%, 90%, or 95%. A barrio is included in a scenario when those eligible radios cover at least 50% of the barrio. Building counts are then summed once per barrio and multiplied by the stated persons-per-footprint sensitivity value. The 3.35 scenario is reported in Table 3 so that the demographic assumption matches the RENABAP-based upper scenario; 2.80 and 3.12 are reported as sensitivity checks.

The recovered adjacent-radio diagnostic first classifies radios with at least 1% barrio coverage. Among the remainder, it separates radios within 2 km of a barrio from more distant radios. The comparison is restricted to radios intersecting IGN Planta Urbana polygons to reduce urban-rural confounding. The original validation report preserved its output but not the exact distance-query implementation. The coverage sweep, occupancy diagnostics, and multiplier tests are executable in this repository; the precise adjacent-radio classification remains a documented reproducibility limitation.

### 4.5 Ground-truthing and direct inspection

These findings have not been formally ground-truthed. Systematic field enumeration remains a need this paper motivates rather than satisfies. Published accounts document Census 2022 coverage and revision problems [@marin2023; @ocar2023]. The Census comparison supplies an additional consistency check, but it does not replace field validation and is not fully independent of RENABAP.

The CABA operation illustrates the qualification. Enumeration in the city's villas was delegated to the Ministerio de Desarrollo Humano y Hábitat and coordinated through barrio referentes, delegados, and social organizations, the same community infrastructure that RENABAP relies on for its family-count estimates [@gomez2022]. The projections going in were drawn from the 2010 census, and the city's own Dirección General de Estadísticas y Censos anticipated that the resulting figures might undercount informal-settlement population. RENABAP and Census 2022 are distinct official products, but they are not wholly separate measurements of the same underlying reality.

During earlier research in La Plata, I examined the most recently available high-resolution satellite basemaps for most of the area's informal settlements and visually confirmed that footprint polygons generally match existing buildings. In several cases the discrepancies were acute. RENABAP lists a newer settlement in the Los Hornos neighborhood at 330 families, whereas the area currently contains more than 4,200 building footprints. Applying the 1.1 families-per-dwelling and 2.8–3.35 persons-per-household multipliers to La Plata yielded an estimated 221,000 to 265,000 informal-settlement residents, against an official figure of approximately 112,000, a discrepancy consistent with the national pattern documented above.

The supplementary material provides illustrative imagery. An interactive web map at [https://barriosvisibles.org](https://barriosvisibles.org) displays every settlement boundary and every building footprint in Argentina against current high-resolution basemap imagery, allowing readers to inspect detection quality across the study area.

### 4.6 Use of generative AI

Anthropic Claude and OpenAI Codex were used during 2025–2026 across multiple model versions; exact historical version identifiers are not recoverable. They supported literature discovery and review. Their technical use covered analysis-code drafting and debugging as well as implementation of parts of the workflow. They also provided methodological, research, drafting, restructuring, and editing assistance.

The author designed and directed the research. The author also reviewed generated code, outputs, and methodological choices. Every reported result and the final manuscript received author review and approval.

The author takes full responsibility for the scientific content, interpretation, and conclusions. No AI system is an author.

---

## 5. Discussion

The core finding of this paper is that RENABAP's enumeration of Argentina's informal-settlement population is systematically low. Summed nationally, raw building footprints exceed RENABAP's recorded family counts by 59%, and the per-settlement household floor — applying RENABAP's own 1.1 families-per-dwelling ratio to footprint counts — exceeds RENABAP's total by 83%. Under conservative assumptions this implies an undercount on the order of 2.9 to 3.4 million people, and likely more: the national aggregate averages across the two regimes documented in §4.2, so the peripheral gap is larger than the 83% headline suggests.

This pattern replicates the systematic undercount documented across gridded population products in @thomson2021, who found that none of nine widely-used products captured more than 39% of field-enumerated slum residents across 118 settlements in Lagos, Port Harcourt, and Nairobi. RENABAP is a field registry rather than a gridded product, and it inherits the same structural vulnerability. Without a building-level floor, one enumeration approach cannot resolve the density heterogeneity that defines informal settlements. Related work reaches similar conclusions across other contexts [@breuer2024; @carrhill2013; @kuffer2022; @lucci2018].

### 5.1 Relationship to prior national-scale work

These findings compound with recent area-based work. @samper2025 document that Argentina's informal-settlement area is geographically more dispersed than global monitoring assumes: extra-small urban areas hold 267 km² against 216 km² in Greater Buenos Aires, and small cities grew at 2.78% annually between 2016 and 2023 against 1.44% in large metropolitan areas. My results indicate that, within those same polygons, registered household counts are a low floor on actual household counts — and that the gap between building evidence and family counts is largest precisely in the peripheral, horizontally-developed settlements that dominate the smaller-city categories. The vertical-density regime documented in §4.2, which keeps CABA's household floor bounded by RENABAP rather than by footprint count, decays sharply with distance from the urban core; outside CABA, roughly 90% of settlements sit in the horizontal regime where footprint counts substantially exceed registered families. The geographic bias identified by Samper et al. and the enumeration gap identified here reinforce one another: the cities that global monitoring already neglects are also the cities where the national registry most substantially undercounts.

The 2016–2023 area-based growth rates reported by @samper2025 should be read with attention to RENABAP's registration waves. The 2016 baseline covered only localities above 10,000 inhabitants (Decreto 358/2017); the extension to localities of 2,000 to 10,000 was formalized only in 2021 (Decreto 880/2021), with a registration cutoff of 31 December 2018. The 2018 growth peak — 991 new settlements nationally, with the highest proportional increases (6.18%, 5.06%, 4.17%) concentrated in medium, small, and extra-small urban areas — falls at the cutoff for the later-added locality-size tier. The mechanism is explicitly acknowledged by RENABAP itself. In a 2023 Infobae interview discussing the most recent registry update, Juan Manuel D'Attoli — coordinator of RENABAP and a co-author of @samper2025 — explained that new entries added during a registration wave do not necessarily indicate new settlements, but rather include "barrios — muchos de ellos antiguos — que no se habían registrado previamente" [settlements, many of them old, that had not been previously registered] [@infobae2023]. Samper's team retro-mapped growth from satellite imagery, but the settlements in question had first to be field-identified through the later survey waves. Some fraction of the apparent 2016–2023 growth in the smaller-city categories is retrospective registration catch-up rather than contemporaneous physical expansion. The correction leaves the cross-sectional finding about where informal area concentrates intact; if anything it strengthens the case that the static total is more peripherally weighted than the year-by-year growth curve alone suggests.

### 5.2 Limitations

Several sources of error remain unaddressed by this analysis. Settlement boundaries change over time relative to those recorded by RENABAP, and the relationship between buildings, households, and persons per household is itself uncertain. Settlement-level variation in that relationship, especially vertical density as documented in §4.2, is only partially captured by the max-of-two approach; settlements with mixed vertical and horizontal construction may be understated by either component of the floor. Nonresidential or vacant footprints can bias building-derived estimates upward. Missed structures, construction after the September 2024 footprint snapshot, vertical or mixed construction, settlements absent from RENABAP, and polygon boundaries that omit later expansion generally bias the national estimate downward.

The Census comparison adds separate limitations. Census population refers to 2022, the public RENABAP snapshot is dated December 2023, and the VIDA footprint snapshot was updated in September 2024. Areal allocation assumes uniform population density within radios, which is least plausible when a dense barrio occupies a small part of a large radio. The coverage restriction reduces that bias by selecting a smaller and nonrepresentative subset; it does not remove it or establish a national Census undercount. The Census and RENABAP products are distinct but share some territorial infrastructure and historical baselines, while the Census comparison and primary analysis share the same footprint counts.

A more structural limitation is coverage. RENABAP only registered settlements meeting size minima for the surrounding locality — initially >10,000 inhabitants, later relaxed to >2,000 — so settlements in smaller localities are absent from the registry entirely. This analysis cannot detect them, because there is no polygon against which to spatially join building footprints. Whatever population lives in sub-threshold-locality informal settlements is missing from both RENABAP's count and mine, and the true national informal-settlement population is correspondingly higher than either figure.

A reader might object that RENABAP was never designed to enumerate all occupants, only titleable households. As noted in §2, however, Ley 27.453 gives the registry a mandate that extends well beyond titling, and in practice it is the population basis for infrastructure planning, resource allocation, and service delivery. That downstream use — not any narrower original purpose — is what this paper critiques.

### 5.3 On the staleness objection

One obvious objection to the finding warrants direct attention: that the gap merely reflects registry staleness, with RENABAP's figures accurate when enumerated but lagging subsequent growth. RENABAP's published methodology provides for continuous updating through territorial visits, satellite analysis, and external submission forms [@sisu2023]. Its quality-control protocol also requires estimated family counts to be consistent with dwellings visible in satellite imagery: "Verificar que la cantidad de familias estimada sea consistente con la cantidad de viviendas que se ven desde la imagen satelital" [@sisu2023]. The age of the public snapshot remains a limitation. Formal responsibility for RENABAP continues within the Secretaría de Obras Públicas, but the latest public dataset used here is dated 6 December 2023, and this study cannot establish how consistently the update protocol has operated since then. Subsequent settlement growth can explain part of the present gap. The methodological concern remains because building-level evidence was already part of RENABAP's stated enumeration and quality-control process.

---

## 6. Conclusion

RENABAP's family totals imply approximately 3.5 to 4.1 million people in Argentina's registered informal settlements under the two demographic multipliers used here. The building-based household floor implies 6.3 to 7.6 million, a difference of approximately 2.9 to 3.4 million people. This range describes the magnitude implied by explicit assumptions, not an exact count of unenumerated residents. Census 2022 provides an additional robustness check: the footprint-based comparison remains 1.88 to 2.06 times the allocated Census population in the safer high-coverage subsets, but it does not independently establish the national total. Flood risk assessment, infrastructure planning, and service delivery all depend on recognizing this uncertainty rather than treating an aging administrative estimate as complete.

The method needs only a spatial join between settlement boundaries and building footprints, plus a per-settlement max-of-two household floor — using RENABAP's own 1.1 families-per-dwelling ratio on the building-derived side — applied as a conservative lower bound. It runs in seconds on a standard laptop using open data and open-source tools.

The analysis does not replace census operations or treat footprints as population ground truth. It shows that open global footprint data can independently characterize the built environment and identify administrative figures that warrant updated enumeration. The inferred national discrepancy is on the order of 6 to 7% of Argentina's population under the assumptions reported here. Local governments without current settlement-level population data can use the comparison to identify where visible development and official records diverge. Those discrepancies can direct field verification before infrastructure or risk-management resources are allocated from stale counts alone.

---

## Acknowledgements

Anthropic Claude and OpenAI Codex provided drafting, restructuring, and editing assistance as described in §4.6. The author reviewed and approved all resulting text and accepts full responsibility for the manuscript.

---

## Author Contributions

Nissim Lebovits: Conceptualization; methodology; software; validation; formal analysis; investigation; data curation; visualization; writing — original draft; writing — review and editing; project administration.

---

## Funding Statement

This work received support from the Fulbright U.S. Student Program, sponsored by the U.S. Department of State and the Comisión Fulbright Argentina. The contents and conclusions are solely the responsibility of the author and do not necessarily represent the official views of the Fulbright Program, the Government of the United States, or the Comisión Fulbright Argentina. The sponsors had no role in study design; data collection, analysis, or interpretation; the decision to submit the work for publication; or manuscript preparation.

---

## Competing Interests

Competing interests: The author declares none.

---

## Data Availability Statement

The code and manuscript-generation workflow are available at [https://github.com/nlebovits/barrios-visibles-paper](https://github.com/nlebovits/barrios-visibles-paper). The version-specific Zenodo archive contains the frozen inputs and derived files for the RENABAP analysis [@lebovits2026data]. A new version of that record, to be cited here as **[INSERT EXACT CENSUS-ENABLED ZENODO VERSION DOI BEFORE SUBMISSION]**, will add the processed Census 2022 radio file and the settlement-count file used for the Census comparison. The Census robustness calculations can then be reproduced with **pixi run census-comparison** from the frozen files, with checksums verified before analysis. Before submission, the archived Paper I output must also be reconciled with the reported footprint total; the current archived output contains 1,967,013 footprints while the manuscript and recovered Census input contain 1,969,975.

The workflow also has live-source modes that retrieve the current public RENABAP, VIDA, IGN, and processed Census inputs. Those runs answer the same analytical questions against changing upstream sources and need not reproduce the publication values. The frozen Zenodo version, rather than a live rerun or the Zenodo concept DOI, defines exact publication reproducibility. Census radio data are also available from [Source Cooperative](https://source.coop/nlebovits/censo-argentino), and the interactive map at [https://barriosvisibles.org](https://barriosvisibles.org) supports settlement-level inspection.

---

## Supplementary Material

The supplementary PDF contains the full building sensitivity analysis, urban and provincial breakdowns, additional Census diagnostics, and illustrative satellite imagery. The article's results and interpretation do not depend on the imagery.

---

## References

::: {#refs}
:::
