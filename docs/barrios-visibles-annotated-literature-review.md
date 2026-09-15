# Barrios Visibles: Annotated Literature Review

**Working evidence index**  
**Prepared:** 2026-09-15  
**Scope:** Informal-settlement population undercount; geographic omission and misallocation; building-footprint population methods; dwelling and household yield; verticality and internal subdivision; building-dataset completeness.

## How to use this review

This document is a claim-oriented evidence index, not a narrative literature review. Each entry records:

- what the source directly establishes;
- which Barrios Visibles claim it can support;
- what it does **not** establish;
- relevant pages, sections, or tables;
- evidence strength and follow-up status;
- stable identifiers and links.

Evidence labels:

- **Direct analogue:** closely matches the Barrios Visibles inference or comparison.
- **Method validation:** validates a component of the method but not the Argentine result.
- **Mechanism evidence:** demonstrates how an undercount or conservative estimate can arise.
- **Context:** establishes the broader problem or geographic setting.
- **Caution:** identifies uncertainty, bias, or a claim that should not be repeated uncritically.

Verification labels:

- **Verified full text:** findings checked in the original paper.
- **Verified secondary:** finding checked in a review but not the original source.
- **Needs follow-up:** obtain or inspect the original before relying heavily on the claim.

---

## Claim index

| Claim or section | Strongest sources | What they establish |
|---|---|---|
| Informal-settlement populations are systematically underrepresented | `thomson2021`, `breuer2024`, `kuffer2019` | Large recurring deficits between field/literature estimates and census-derived population products; a roof-based estimate exceeding a census-based estimate by roughly two million in Dar es Salaam. |
| A plausible national total can conceal severe geographic error | `kuffer2022`, `thomson2021` | Population is systematically shifted away from dense informal areas and into lower-density or non-residential cells. |
| Official enumeration can omit entire areas | `sanchez-cespedes2024`, `kuffer2020`, `angeles2009` | Census areas can be partially enumerated or not visited; missing settlement maps increase the probability of census and survey omission. |
| Independent imagery can reveal more dwellings than official records | `gunter2009`, `kuffer2019`, `kit2013` | Image-derived dwelling or population estimates can substantially exceed administrative estimates in particular settlements. |
| Building footprints contain validated population information | `boo2022`, `galeon2008` | Survey-calibrated footprints predict population well; VHR imagery can identify informal-settlement structures with field-validated accuracy. |
| One footprint need not equal one household | `marx2019`, `ono2020`, `thomson2021`, `vanhuysse2024` | One roof object can contain many households or rental units; contiguous roofs can be merged; buildings can contain rows of rooms and several floors. |
| Two-dimensional footprint counts are conservative in vertical settlements | `ono2020`, `galeon2008`, `almeida2011` | Planar roofs omit residential floor space and weaken population relationships where structures are multilevel. |
| Missing footprints generally push estimates downward | `boo2022`, `gevaert2024` | Cloud, imagery, geometry, and model omissions produce false negatives and population underprediction. |
| No single footprint provider should be treated as complete | `chamberlain2024`, `gevaert2024`, `herfort2023` | Products differ sharply across places; OSM is especially incomplete and geographically clustered. |
| Argentina's informal settlements are dispersed and growing outside large metros | `samper2025` | RENABAP area is large in small urban areas, and measured settlement-area growth is faster there than in major metropolitan areas. |
| Post-2022 construction should be tested rather than assumed | `quinn2024` | Temporal building data provide an independent way to date construction; the dataset alone says nothing about occupancy. |

---

## Priority reading list

If time is limited, read these first:

1. `sanchez-cespedes2024` — closest Latin American census-gap precedent.
2. `kuffer2019` — closest roof-based versus census-based population analogue.
3. `thomson2021` — strongest multi-settlement empirical evidence of systematic underrepresentation.
4. `boo2022` — strongest validation of population estimation from household data and building footprints.
5. `kuffer2022` — strongest source for geographic misallocation despite shared aggregate totals.
6. `marx2019` — strongest direct evidence that one remotely delineated roof object can contain many households.
7. `ono2020` — strongest field evidence for verticality and internal rental subdivision.
8. `gunter2009` — closest reported dwelling-count discrepancy, but original requires retrieval.

---

# I. Direct analogues and population underrepresentation

## `thomson2021`

**Citation**  
Thomson, Dana R., Andrea E. Gaughan, Forrest R. Stevens, Gregory Yetman, Peter Elias, and Robert Chen. 2021. “Evaluating the Accuracy of Gridded Population Estimates in Slums: A Case Study in Nigeria and Kenya.” *Urban Science* 5 (2): 48.

**Links**  
DOI and full text: https://doi.org/10.3390/urbansci5020048

**Evidence type:** Direct empirical analogue; method precedent.  
**Evidence strength:** High for gridded-product underrepresentation; indirect for census enumeration.  
**Verification:** Verified full text.

### Direct findings

- Compares nine gridded population products with community field-referenced boundaries and population estimates for 118 settlements: 26 in Lagos, 39 in Port Harcourt, and 53 in Nairobi.
- Every product substantially underestimated the reference populations.
- Bias ranged from −2,853 to −7,638 people per settlement; RMSE ranged from 4,958 to 14,422.
- The best-performing product, HRSL, captured only 39% of the community-derived population on average.
- In Lagos, gridded products placed only 1.02–2.96% of the population in mapped slum areas, versus 56% using UN-Habitat’s survey-based method.
- The Know Your City workflow counted front doors, sampled households for average household size, multiplied these quantities, and community-validated the results.
- The paper identifies slum-specific variation in household size, households per building, and residential-building share as major sources of model error.
- It notes that contiguous roofs can be extracted as a single building and that multiple one-room dwellings within a building are common.
- Its footprint-based WorldPop “Peanut Butter” models used a default of 1.1 households per building in both Nigeria and Kenya.

### Useful for Barrios Visibles

- Establishing strong international precedent for population products missing most residents of dense informal settlements.
- Demonstrating that a building-specific household multiplier of 1.1 is used outside RENABAP and was not invented for Barrios Visibles.
- Explaining why citywide household-size or building-occupancy averages fail in informal settlements.
- Supporting the claim that one extracted footprint can conceal several dwellings.

### Does not establish

- It does not directly audit a national census. The products are census-derived, but the tested error includes spatial allocation and model error.
- It does not validate Argentina’s effect size or the 1.1 multiplier in Argentina.
- Know Your City estimates were not independently verified; sampling procedures were incompletely documented, and some questionable large estimates were excluded.

**Locations:** Methods and product descriptions around p. 9; results pp. 12–14; discussion and limitations pp. 14–18.

**Tags:** `undercount`, `gridded-population`, `households-per-building`, `community-enumeration`, `Nigeria`, `Kenya`, `priority`

---

## `kuffer2019`

**Citation**  
Kuffer, Monika, Claudio Persello, Karin Pfeffer, Richard Sliuzas, and Vinodkumar Rao. 2019. “Do We Underestimate the Global Slum Population?” In *2019 Joint Urban Remote Sensing Event (JURSE)*, 1–4.

**Links**  
DOI: https://doi.org/10.1109/JURSE.2019.8809066  
Open PDF: https://ris.utwente.nl/ws/files/284398855/Kuffer_2019_Do_we_underestimate_the_global_slum.pdf

**Evidence type:** Direct methodological analogue.  
**Evidence strength:** Medium-high; very close design but a short conference paper.  
**Verification:** Verified full text.

### Direct findings

- A census-based estimate implied approximately 3 million Dar es Salaam residents living in slum-like conditions.
- A bottom-up estimate combining OSM/UAV-derived rooftop outlines, a household survey in five settlements, Slum Dwellers International data, and land-use exclusions produced approximately 5 million.
- Roof-area calibration was 9.8 m² per person in the household survey and 10.6 m² per person in SDI data.
- The inferred total city population exceeded 6 million, with roughly 80% living in slum-like conditions.
- The analysis mapped concentrations of residents described as possibly uncounted.
- Houses were commonly single-storey, but portions of houses were often sublet.

### Useful for Barrios Visibles

- This is the closest published analogue to the core inference: satellite-observed roofs plus locally grounded occupancy information substantially exceed a census-based informal-settlement estimate.
- The approximate two-million-person discrepancy provides precedent for a national or metropolitan gap of the same order as Barrios Visibles.
- Subletting supports the possibility of more than one family or household per visible structure.

### Does not establish

- The paper explicitly does not claim a “final truth.”
- Roof area per person is transferred across the city and could differ between central and peripheral settlements.
- Census, survey, and imagery inputs came from different years.
- Mixed-use buildings can inflate residential roof area despite land-use exclusions.

**Locations:** pp. 1–3.

**Tags:** `direct-analogue`, `roof-area`, `census-comparison`, `Dar-es-Salaam`, `subletting`, `priority`

---

## `gunter2009`

**Citation**  
Gunter, Ashley W. 2009. “Getting It for Free: Using Google Earth and ILWIS to Map Squatter Settlements in Johannesburg.” In *2009 IEEE International Geoscience and Remote Sensing Symposium*, III-388–III-391.

**Links**  
DOI: https://doi.org/10.1109/IGARSS.2009.5417784

**Evidence type:** Direct dwelling-count analogue.  
**Evidence strength:** Potentially high relevance; current evidence is secondary.  
**Verification:** Verified secondary through `kuffer2016`; original full text still needed.

### Reported finding

- Kuffer et al. report that image mapping identified approximately 10,000 more dwellings in one Johannesburg settlement than government estimates recorded.

### Useful for Barrios Visibles

- This is the closest like-for-like precedent for visible dwelling counts greatly exceeding an administrative dwelling estimate.

### Does not establish

- The government comparator and its collection method have not yet been checked in the original paper.
- Kuffer et al. warn that part of the discrepancy could reflect different definitions of “slum dwelling.”

### Follow-up

- Obtain the original four-page paper.
- Record the settlement name, government estimate, image-derived estimate, imagery date, and dwelling definition.
- Until then, write “Kuffer et al. report that Gunter found…” rather than citing the number as directly verified.

**Tags:** `dwelling-count`, `government-estimate`, `Johannesburg`, `needs-original`, `priority`

---

## `breuer2024`

**Citation**  
Breuer, Julius H. P., John Friesen, Hannes Taubenböck, Michael Wurm, and Peter F. Pelz. 2024. “The Unseen Population: Do We Underestimate Slum Dwellers in Cities of the Global South?” *Habitat International* 148: 103056.

**Links**  
Open PDF: https://elib.dlr.de/203674/1/Friesen_et_al_%282024%29_Unseen_Population_HABITAT.pdf

**Evidence type:** Multi-city comparative precedent.  
**Evidence strength:** Medium; broad coverage but heterogeneous comparison estimates.  
**Verification:** Verified full text.

### Direct findings

- Compares WorldPop clipped to Earth-observation-mapped morphological slums against 80 literature estimates across eight cities and three continents.
- Recurring large deficits include:
  - Dharavi: 53,194 modeled residents versus a 350,000 comparison estimate; other model versions remained far below estimates of 300,000–1 million.
  - Petare: 42,534 versus approximately 600,000–1 million.
  - Baseco: 12,512 versus 51,060.
  - Cape Town: modeled estimates captured roughly 68% of comparison populations in townships but only about 24% in informal settlements.

### Useful for Barrios Visibles

- Demonstrates that underrepresentation of informal-settlement populations recurs across cities and continents.
- Shows that the problem is most severe in informal settlements rather than all low-income settlement types equally.

### Does not establish

- WorldPop is census-derived, so the discrepancy combines census-input limitations, modeled-boundary error, and allocation-model failure.
- Literature comparison figures differ considerably in quality and date.
- Do not repeat the paper’s statement that censuses themselves underestimate slum populations by about 46% as though Thomson et al. directly established that. Thomson evaluated gridded products, not census enumeration.
- The Bangladesh “7.5 times” example concerns differing slum definitions and thresholds, not proof that seven-eighths of residents were omitted.

**Tags:** `multi-city`, `WorldPop`, `underrepresentation`, `informal-settlements`, `caution`

---

## `kit2013`

**Citation**  
Kit, Oleksandr, Matthias Lüdeke, and Diana Reckien. 2013. “Defining the Bull’s Eye: Satellite Imagery-Assisted Slum Population Assessment in Hyderabad, India.” *Urban Geography* 34 (3): 413–424.

**Links**  
DOI: https://doi.org/10.1080/02723638.2013.778665  
Author manuscript: https://www.mkb-l.de/lit/Slums_Hyderabad_Urban_Geography_final_manuscript.pdf

**Evidence type:** Spatial misclassification and stale-list evidence.  
**Evidence strength:** Medium.  
**Verification:** Verified full text.

### Direct findings

- Field visits found severely deprived informal areas that were not known or recognized by local government.
- Some officially listed slums no longer appeared morphologically slum-like.
- Image-derived estimates differed from official estimates in most city circles.
- In Circle VII, the conservative core-slum estimate exceeded census data by 10%.
- Citywide, however, the image-derived slum share was 29%, below the official 35%.

### Useful for Barrios Visibles

- Establishes that official settlement lists can be geographically wrong in both directions.
- Supports a distinction between a roughly plausible aggregate and incorrect local allocation.
- Helps explain how recognition rules and stale boundaries exclude poor areas without necessarily lowering every aggregate.

### Does not establish

- It does not support a universal or citywide census undercount.
- Absolute estimates depend on assumed population-density ranges rather than a dwelling census.
- Agarwal’s reported finding that 76% of Hyderabad’s poorest residents lived outside census-designated slums concerns classification, not population omission.

**Tags:** `official-boundaries`, `spatial-misclassification`, `Hyderabad`, `counterevidence`

---

# II. Census gaps and official invisibility

## `sanchez-cespedes2024`

**Citation**  
Sánchez-Céspedes, Lina M., et al. 2024. “Social Cartography and Satellite-Derived Building Coverage for Post-Census Population Estimates in Difficult-to-Access Regions of Colombia.” *Population Studies* 78 (1): 3–20.

**Links**  
DOI: https://doi.org/10.1080/00324728.2023.2190151  
Open manuscript: https://www.researchgate.net/publication/369608716_Social_cartography_and_satellite-derived_building_coverage_for_post-census_population_estimates_in_difficult-to-access_regions_of_Colombia

**Evidence type:** Official census-gap precedent; method validation.  
**Evidence strength:** High. DANE coauthored the study.  
**Verification:** Verified full text.

### Direct findings

- Of 1,302 special-route census enumeration areas, 508 had at least 90% of expected properties enumerated, 628 were partially enumerated, and 166 were not visited.
- Models were trained using 489 sufficiently enumerated areas.
- Satellite building coverage alone explained 56.8% of out-of-sample population variance.
- Community estimates explained 66.2%.
- The combined satellite and community model explained 67.9% of population variance and 65.1% of building-count variance, with the best overall accuracy.
- Validation of World Settlement Footprint building area in Cartagena produced mean error of 0.29%, MAE of 6.52%, and RMSE of 8.98%.

### Useful for Barrios Visibles

- Strong Latin American precedent in which a national statistical office recognized incomplete census geography.
- Demonstrates that community reports of dwellings, families, and residents can be combined with satellite-observed building coverage to reconstruct missing population.
- Supports treating community mechanisms and satellite evidence as complementary rather than independent systems that must agree automatically.

### Does not establish

- The omitted Colombian areas were remote, conflict-affected, and often home to minority communities, not urban informal settlements.
- The method models building coverage, not one footprint per dwelling.
- The study does not report a national missing-population total.
- Treating 90% property coverage as “full” leaves some residual enumeration error.

**Locations:** Data pp. 2–4; results pp. 8–11; Figure 5.

**Tags:** `Colombia`, `DANE`, `census-gap`, `unvisited-areas`, `community-mapping`, `satellite-buildings`, `priority`

---

## `kuffer2020`

**Citation**  
Kuffer, Monika, Dana R. Thomson, Gianluca Boo, et al. 2020. “The Role of Earth Observation in an Integrated Deprived Area Mapping ‘System’ for Low-to-Middle Income Countries.” *Remote Sensing* 12 (6): 982.

**Links**  
DOI and full text: https://doi.org/10.3390/rs12060982

**Evidence type:** Mechanism and official-geography precedent.  
**Evidence strength:** Medium-high for the mapping mechanism; mixed sources for individual city comparisons.  
**Verification:** Verified full text.

### Direct findings

- Describes a circular problem: where deprived-area maps are absent, census and household-survey sampling and field collection are more likely to underreport those communities.
- Notes that approximately 60% of Nairobi’s population occupies about 4% of its built-up area; ordinary sampling can therefore exclude large shares of the population implicitly.
- In Bangalore, the 2011 census reported an 8% slum-population share, the Karnataka Slum Development Board counted 597 slums and approximately 23%, and a local organization mapped more than 1,500 settlements.
- Small, temporary, unrecognized, and especially deprived areas were the most likely to be omitted.

### Useful for Barrios Visibles

- Establishes a mechanism by which missing or outdated settlement maps propagate into census and survey omission.
- Supports the argument that peripheral, small, or recently formed barrios are the most vulnerable to exclusion.
- Provides precedent for large disagreements among census, administrative, and community settlement systems.

### Does not establish

- The Bangalore figures come from different institutions, definitions, and possibly dates; do not interpret their differences as a clean census coverage rate.
- This is not an Argentina-specific enumeration audit.

**Tags:** `mapping-frame`, `census-mechanism`, `Bangalore`, `Nairobi`, `unrecognized-settlements`

---

## `carr-hill2013`

**Citation**  
Carr-Hill, Roy. 2013. “Missing Millions and Measuring Development Progress.” *World Development* 46: 30–44.

**Links**  
DOI: https://doi.org/10.1016/j.worlddev.2012.12.017

**Evidence type:** Broad methodological context.  
**Evidence strength:** Medium for general exclusion; low for any Argentina-specific effect size.  
**Verification:** Verified through target papers and source summaries; original should be retained in the repository.

### Direct findings

- Argues that household-survey frames, and in some settings censuses, systematically exclude mobile, homeless, institutionalized, conflict-affected, and other difficult-to-reach groups.
- Estimates approximately 250 million people missing globally from common development-measurement systems.
- Includes informal-settlement residents among populations at elevated risk of exclusion.

### Useful for Barrios Visibles

- Establishes that exclusion from statistical frames is a recognized structural problem rather than an extraordinary Argentine allegation.

### Does not establish

- The slum component relies on assumed undercount scenarios of roughly one in ten or one in five, described as approximate and probably conservative.
- It provides no footprint validation and no Argentine estimate.

**Tags:** `sampling-frame`, `missing-populations`, `global-context`, `caution`

---

## `angeles2009`

**Citation**  
Angeles, Gustavo, Peter Lance, Janine Barden-O’Fallon, Nazrul Islam, A. Q. M. Mahbub, and Nurul Islam Nazem. 2009. “The 2005 Census and Mapping of Slums in Bangladesh: Design, Select Results and Application.” *International Journal of Health Geographics* 8: 32.

**Links**  
Full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC2701942/

**Evidence type:** Census-cartography precedent and imagery limitation.  
**Evidence strength:** High for the combined imagery-and-field workflow.  
**Verification:** Verified full text.

### Direct findings

- Government base maps frequently omitted recent development and sometimes omitted established areas.
- Satellite imagery supplied the first reliable citywide framework and identified likely concentrations of slums.
- Imagery interpretation alone nevertheless missed approximately 30% of slums because of foliage, terrain, morphological variation, or recent development.
- The combined imagery and field census identified 9,048 slum communities across six cities.

### Useful for Barrios Visibles

- Shows that official cartography can miss entire established areas.
- Supports a combined approach using imagery, administrative sources, and field/community information.
- Provides an honest caveat: imagery improves enumeration but does not eliminate omission.

### Does not establish

- The 30% figure is the share of slum communities missed by image interpretation, not a modern building-footprint false-negative rate or population undercount.

**Tags:** `Bangladesh`, `census-mapping`, `satellite-imagery`, `field-validation`, `limitations`

---

# III. Building footprints as population evidence

## `boo2022`

**Citation**  
Boo, Gianluca, et al. 2022. “High-Resolution Population Estimation Using Household Survey Data and Building Footprints.” *Nature Communications* 13: 1330.

**Links**  
DOI and full text: https://doi.org/10.1038/s41467-022-29094-x

**Evidence type:** Strong method validation.  
**Evidence strength:** High.  
**Verification:** Verified full text.

### Direct findings

- Uses complete household enumeration in 926 microcensus clusters across five provinces of the Democratic Republic of Congo.
- The source enumeration included 79,126 responding households; nonresponses were imputed.
- Population totals were modeled using population density and total satellite-derived footprint area.
- Across 905 usable clusters, out-of-sample population-total performance reached R² = 0.79.
- Approximately 90% of observations fell inside nominal 95% credible intervals.
- Smaller average footprints were associated with higher population density, interpreted partly as small and overcrowded buildings.
- Missing, outdated, cloud-obscured, or smoke-obscured footprints inflated modeled densities and contributed to population underprediction.

### Useful for Barrios Visibles

- Provides strong independent evidence that building footprints carry substantial information about population.
- Validates the general architecture of combining building evidence with locally grounded household or occupancy information.
- Shows that missed footprints normally bias the resulting population estimate downward.

### Does not establish

- It does not equate footprint polygons with dwellings.
- It depends on microcensus calibration and includes non-residential buildings.
- Results from the DRC cannot supply an Argentine dwelling-yield parameter directly.

**Locations:** Results and Table 1; discussion of footprint errors and building morphology.

**Tags:** `method-validation`, `microcensus`, `building-footprints`, `population-model`, `DRC`, `priority`

---

## `galeon2008`

**Citation**  
Galeon, Florence A. 2008. “Estimation of Population in Informal Settlement Communities Using High Resolution Satellite Image.” *International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences* XXXVII-B4: 1377–1382.

**Links**  
Full paper: https://www.isprs.org/proceedings/xxxvii/congress/4_pdf/242.pdf

**Evidence type:** Field-validated structure detection; verticality mechanism.  
**Evidence strength:** Medium.  
**Verification:** Verified full text.

### Direct findings

- QuickBird mapping achieved 95% identification accuracy against stratified field validation.
- Researchers collected 160 building-level field samples covering roof area, resident count, settlement type, and whether structures were single- or multilevel.
- Multilevel structures contained many residents despite small visible roof areas and substantially weakened the planar roof-area/population relationship.
- The authors excluded multilevel houses before fitting final equations.
- In a small seven-building validation cluster, one model predicted 71 residents versus 70 observed.

### Useful for Barrios Visibles

- Demonstrates that sub-meter imagery can independently enumerate informal-settlement structures with high field-validated accuracy.
- Shows directly why two-dimensional population estimates are conservative or unstable in multilevel housing.

### Does not establish

- This is one Philippine setting with small validation samples.
- It models residents, not households.
- The prevalence of multilevel buildings should not be transferred to Argentina.

**Locations:** Abstract; §§5.4 and 6.1–6.2.

**Tags:** `field-validation`, `QuickBird`, `verticality`, `Philippines`, `structure-detection`

---

## `gevaert2024`

**Citation**  
Gevaert, Caroline M., T. Buunk, and Marc J. van den Homberg. 2024. “Auditing Geospatial Datasets for Biases: Using Global Building Datasets for Disaster Risk Management.” *IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing* 17: 12579–12590.

**Links**  
DOI: https://doi.org/10.1109/JSTARS.2024.3422503

**Evidence type:** Manual footprint-product audit.  
**Evidence strength:** High for dataset bias and false negatives; not an occupancy study.  
**Verification:** Verified full text.

### Direct findings

- Manually digitized reference buildings in 100 stratified 250 m tiles in Tanzania and 106 in the Philippines.
- Across tested products, false-negative rates using an IoU ≥ 0.5 criterion ranged from 0.55 to 0.85 in Tanzania and 0.70 to 0.83 in the Philippines.
- OSM ranged from high-quality targeted coverage to no buildings at all in some rural tiles.
- Google sometimes counted more buildings than the manual reference because the reference generalized adjacent buildings into one polygon while Google separated the structures.

### Useful for Barrios Visibles

- Establishes that global building datasets contain substantial and geographically uneven omissions.
- Shows that reference polygons themselves can merge several real structures, making lower reference counts ambiguous.
- Supports presenting the VIDA union as evidence that still has a downward false-negative risk, not a complete census of all structures.

### Does not establish

- The false-negative rate includes geometry mismatches at the IoU threshold, not only buildings missing entirely.
- Samples exclude some low-building and low-provider-coverage areas.
- No households or residents were observed.
- Results cover two countries, not Argentina.

**Locations:** Methods pp. 12583–12584; Table II; discussion pp. 12587–12588.

**Tags:** `dataset-bias`, `manual-validation`, `false-negatives`, `Google`, `OSM`, `limitations`

---

## `chamberlain2024`

**Citation**  
Chamberlain, Hannah R., et al. 2024. “Building Footprint Data for Countries in Africa: To What Extent Are Existing Data Products Comparable?” *Computers, Environment and Urban Systems* 110: 102104.

**Links**  
DOI: https://doi.org/10.1016/j.compenvurbsys.2024.102104

**Evidence type:** Multi-provider comparability.  
**Evidence strength:** High for product disagreement; no authoritative ground truth.  
**Verification:** Verified full text/preprint.

### Direct findings

- Across 879 first-level administrative units, mean footprint counts were approximately 556,615 for Ecopia, 534,676 for Google, 241,978 for Microsoft, and 110,616 for OSM.
- Google and Ecopia generally had the highest counts and strongest spatial similarity.
- Microsoft showed visible missing-imagery tiles and major-city gaps in some countries.
- OSM was geographically widespread but had the lowest footprint counts and areas.
- The authors conclude there is no universally best or interchangeable product.

### Useful for Barrios Visibles

- Supports combining several independent providers and checking imagery directly.
- Shows that convergence among independent satellite-derived sources is more informative than agreement with sparse OSM.
- Helps frame source-specific omissions as a robustness issue rather than a reason to discard all footprint evidence.

### Does not establish

- Agreement between Google and Ecopia does not prove either is complete.
- The analysis lacks authoritative ground truth and covers Africa rather than Argentina.
- Image acquisition dates differ.

**Locations:** Results pp. 11–12 and Figure 1; discussion pp. 21–23.

**Tags:** `provider-comparison`, `Google`, `Microsoft`, `Ecopia`, `OSM`, `Africa`

---

## `herfort2023`

**Citation**  
Herfort, Benjamin, Sven Lautenbach, João Porto de Albuquerque, et al. 2023. “A Spatio-Temporal Analysis Investigating Completeness and Inequalities of Global Urban Building Data in OpenStreetMap.” *Nature Communications* 14: 3985.

**Links**  
DOI and full text: https://doi.org/10.1038/s41467-023-39698-6

**Evidence type:** OSM completeness and geographic inequality.  
**Evidence strength:** High for OSM caution.  
**Verification:** Verified full text.

### Direct findings

- Assesses 13,189 urban centers.
- Only 1,848 exceeded 80% estimated building completeness.
- 9,163 urban centers—69% of the sample, containing 48% of the studied urban population—had less than 20% estimated completeness.
- Mean estimated completeness for Latin America and the Caribbean was approximately 20%.
- Within cities, entire neighborhoods could be absent even where adjacent neighborhoods were relatively complete.

### Useful for Barrios Visibles

- Establishes that OSM absence is not evidence of building absence.
- Directly undermines analyses that treat OSM as universal ground truth.
- Shows that mapping omissions are spatially clustered within cities rather than random.

### Does not establish

- Completeness is model-estimated rather than established through a worldwide field census.
- Microsoft-derived reference/training data can introduce bias.
- The paper does not examine household occupancy or census population.

**Tags:** `OSM`, `completeness`, `Latin-America`, `geographic-bias`, `priority-caveat`

---

# IV. Multiple households, internal subdivision, and verticality

## `marx2019`

**Citation**  
Marx, Benjamin, Thomas M. Stoker, and Tavneet Suri. 2019. “There Is No Free House: Ethnic Patronage in a Kenyan Slum.” *American Economic Journal: Applied Economics* 11 (4): 36–70.

**Links**  
DOI: https://doi.org/10.1257/app.20160484  
Open manuscript: https://sciencespo.hal.science/hal-03873744/file/2019_marx_stoker_suri_there_is_no_free_house_ethnic_patronage_in_a_kenyan_slum.pdf

**Evidence type:** Direct household-to-roof-object evidence.  
**Evidence strength:** High, with an important object-definition caveat.  
**Verification:** Verified full text.

### Direct findings

- Combines household/GPS survey data with very-high-resolution image segmentation in Kibera.
- The mean remotely delineated roof object covered 466 m².
- Each roof object contained an average of 11.2 households.
- The authors describe the segmented objects as “roofs or blocks of roofs” and manually corrected them.

### Useful for Barrios Visibles

- Strong existence proof that one remotely visible polygon can correspond to many households.
- Demonstrates why a one-footprint/one-household assumption is conservative in dense, conjoined-roof environments.

### Does not establish

- Do not state that the average detached building contained 11.2 households.
- The remotely delineated object could combine a roof block rather than a single freestanding structure.
- The quantity cannot be transferred as an Argentine multiplier.

**Locations:** Article pp. 47–48.

**Tags:** `households-per-roof`, `Kibera`, `contiguous-roofs`, `direct-evidence`, `priority`

---

## `ono2020`

**Citation**  
Ono, Hiroshi, and Tetsuo Kidokoro. 2020. “Understanding the Development Patterns of Informal Settlements in Nairobi.” *Japan Architectural Review* 3: 384–393.

**Links**  
DOI and full text: https://doi.org/10.1002/2475-8876.12161

**Evidence type:** Field evidence for verticality and rental subdivision.  
**Evidence strength:** High for mechanism; no household-per-footprint parameter.  
**Verification:** Verified full text.

### Direct findings

- Fieldwork in three villages in Mukuru Kwa Njenga documented rows of standard 10-by-12-foot rental rooms arranged around aisles.
- Housing included single rooms, bedsitters, and one-bedroom units.
- In MCC, 45.8% of buildings had one or two stories, 27.2% had three to five stories, and 11.5% had six or seven stories; the maximum was seven.
- Gross building coverage was 64.7%, while gross floor-area ratio was 196.7%.
- Surveyed plots contained tenants or owners plus tenants; no surveyed plot was occupied only by the structure owner.

### Useful for Barrios Visibles

- Shows that overhead footprint area can omit most residential floor space in vertically consolidated informal settlements.
- Establishes internal rental subdivision within structures.
- Supports accepting RENABAP/INDEC counts over raw footprints in consolidated vertical villas while treating one-household-per-footprint assumptions elsewhere as a floor.

### Does not establish

- Rental rooms are not explicitly enumerated as households.
- One Nairobi settlement cannot define Argentine occupancy rates.

**Locations:** §§5.2–5.4 and §7.

**Tags:** `verticality`, `rental-units`, `floor-area-ratio`, `Nairobi`, `priority`

---

## `vanhuysse2024`

**Citation**  
Vanhuysse, Sabine, Monika Kuffer, Stefanos Georganos, Jiong Wang, Angela Abascal, Taïs Grippa, and Eléonore Wolff. 2024. “Putting the Invisible on the Map: Low-Cost Earth Observation for Mapping and Characterizing Deprived Urban Areas (Slums).” In *Urban Inequalities from Space*, 119–137.

**Links**  
DOI: https://doi.org/10.1007/978-3-031-49183-2_7  
Open manuscript: https://dipot.ulb.ac.be/dspace/bitstream/2013/384381/3/Vanhuysse_et_al_2024-Putting_the_invisible_AAM.pdf

**Evidence type:** Mechanism and EO-method context.  
**Evidence strength:** Medium.  
**Verification:** Verified full text/manuscript.

### Direct findings

- Describes Nairobi housing ranging to multi-story tenements divided into multiple rental units.
- Describes Kisumu compounds composed of multiple residential units occupying a single plot, with plot coverage reaching approximately 80% near the center.
- Shows that open building footprints, while imperfect in deprived areas, add substantial morphological information beyond Sentinel-1/2 imagery.
- Its overall premise is that EO can meet some spatial-data needs without relying on censuses or socioeconomic surveys.

### Useful for Barrios Visibles

- Supports internal subdivision and verticality as real mechanisms.
- Supports treating visible built form as evidence partly independent of census population.

### Does not establish

- It does not estimate population, occupancy, dwellings per footprint, or census undercount.
- A plot is not necessarily equivalent to one detected footprint.

**Locations:** Case studies in §3, manuscript pp. 6–7; EO results in §4; synthesis in §5.

**Tags:** `Springer-chapter`, `verticality`, `multi-unit`, `EO`, `context`

---

## `almeida2011`

**Citation**  
Almeida, Cláudia M., Cléber G. Oliveira, Camilo D. Rennó, and Raul Q. Feitosa. 2011. “Population Estimates in Informal Settlements Using Object-Based Image Analysis and 3D Modeling.” *IEEE Earthzine*, August 16.

**Links**  
Full article: https://earthzine.org/population-estimates-in-informal-settlements-using-object-based-image-analysis-and-3d-modeling/

**Evidence type:** Verticality mechanism.  
**Evidence strength:** Medium-low; useful mechanism, weaker publication and validation.  
**Verification:** Verified full text.

### Direct findings

- Rio das Pedras had developed multistory favela structures.
- The population model applied a height factor corresponding to a 30% increase over orthogonally projected residential area.
- The resulting 3D estimate was 43,295 residents, close to a census-projected reference of 43,342.
- The authors argue that population estimation must include the third dimension where multistory informal housing exists.

### Useful for Barrios Visibles

- Provides a Brazilian example in which planar footprint area omitted approximately 30% of modeled residential area.

### Does not establish

- IEEE Earthzine is not a conventional peer-reviewed journal.
- The reference was the 2000 census projected to 2006 using a citywide growth rate, not independent field truth.
- Classification and elevation models were not fully validated.

**Tags:** `Brazil`, `Rio-das-Pedras`, `3D`, `verticality`, `secondary`

---

## `veljanovski2012`

**Citation**  
Veljanovski, Tatjana, Urša Kanjir, Peter Pehani, Krištof Oštir, and Primož Kovačič. 2012. “Object-Based Image Analysis of VHR Satellite Imagery for Population Estimation in Informal Settlement Kibera-Nairobi, Kenya.” In *Remote Sensing—Applications*, 407–434.

**Links**  
DOI and full text: https://doi.org/10.5772/37869

**Evidence type:** Sensitivity and calibration evidence.  
**Evidence strength:** Medium.  
**Verification:** Verified full text.

### Direct findings

- Estimated approximately 1.647 million m² of residential area in Kibera.
- Population scenarios based on published density assumptions ranged from 156,652 to 642,284, compared with a reported 2009 census population of 170,070.
- In Raila, the same typical 32 m² structure corresponded to assumptions ranging from 3.04 to 12.48 people.
- Dense and merged roofs prevented reliable extraction of individual buildings even with VHR imagery.

### Useful for Barrios Visibles

- Demonstrates why sensitivity analysis is essential.
- Shows that occupancy calibration, not only footprint detection, dominates population uncertainty.
- Supports avoiding a single universal dwelling-yield parameter.

### Does not establish

- The paper does not validate a preferred occupancy assumption.
- Residential-use assumptions can be wrong, and the total range is intentionally broad.

**Tags:** `sensitivity-analysis`, `Kibera`, `occupancy`, `merged-roofs`, `caution`

---

# V. Population geography and model misallocation

## `kuffer2022`

**Citation**  
Kuffer, Monika, Maxwell Owusu, Lorraine Oliveira, Richard Sliuzas, and Frank van Rijn. 2022. “The Missing Millions in Maps: Exploring Causes of Uncertainties in Global Gridded Population Datasets.” *ISPRS International Journal of Geo-Information* 11 (7): 403.

**Links**  
DOI: https://doi.org/10.3390/ijgi11070403  
Open PDF: https://ris.utwente.nl/ws/files/283468040/ijgi_11_00403.pdf

**Evidence type:** Geographic-misallocation evidence.  
**Evidence strength:** High for distributional error; indirect for census completeness.  
**Verification:** Verified full text.

### Direct findings

- Compares GHS-POP with the finest available local population data, aggregated to 1 km, across seven cities.
- Only approximately 25% of urban cells were within ±10% of local reference counts; roughly 75% were wrongly estimated under that criterion.
- Correctly estimated residential cells included 8.9% in Kumasi, 16.2% in Jakarta, 13.4% in Cairo, 27.8% in Kabul, 26.7% in São Paulo, and 68.2% in New York.
- Dense residential, informal, and high-rise areas tended to be underestimated.
- Mixed or non-residential central areas and some low-density outskirts tended to be overestimated.
- The mechanism is partly the binary distribution of population across built-up pixels without sufficient land-use or height information.

### Useful for Barrios Visibles

- Best source for explaining why a nationally reconciled population total does not validate its geographic allocation.
- Establishes a mechanism by which people are moved statistically out of high-density residential areas and into implausible non-residential or low-density locations.
- Supports distinguishing national-total accuracy from correct enumeration and assignment of informal-settlement residents.

### Does not establish

- It does not independently test the completeness of national censuses.
- São Paulo’s informal-settlement category was excluded from part of the analysis because most settlements were smaller than one 1-km cell.
- Some error reflects temporal and source mismatches.
- The paper warns that Google Open Buildings can contain large omissions in high-density informal areas; that warning supports conservatism but is not Argentina-specific.

**Locations:** Abstract; §4.3 pp. 10–11; Table 7 pp. 11–12; discussion and conclusion pp. 12–15.

**Tags:** `geographic-misallocation`, `GHS-POP`, `national-total`, `informal-density`, `priority`

---

## `darin2022`

**Citation**  
Darin, E., et al. 2022. “The Population Seen from Space: When Satellite Images Come to the Rescue of the Census.” *Population* 77 (3): 437–464.

**Links**  
DOI: https://doi.org/10.3917/popu.2203.0467  
Repository record: https://eprints.soton.ac.uk/473749/

**Evidence type:** Official census-reconstruction precedent.  
**Evidence strength:** Medium-high for method precedent.  
**Verification:** Verified through source record and citation trail; retain full text when organizing repository.

### Direct findings

- Burkina Faso’s 2019 census could not fully enumerate areas affected by insecurity.
- Partial enumeration and satellite-derived settlement/building data were incorporated into hierarchical Bayesian estimation and 100 m population grids.

### Useful for Barrios Visibles

- Another official precedent for treating satellite-observed settlement as evidence about populations missed by census field operations.

### Does not establish

- The omission mechanism was armed-conflict inaccessibility, not informal-urban enumeration.
- It does not validate one footprint per dwelling.

**Tags:** `Burkina-Faso`, `census-reconstruction`, `satellite`, `Bayesian-model`

---

# VI. Argentina-specific settlement geography and temporal evidence

## `samper2025`

**Citation**  
Samper, Jota, Julio Pedrassoli, Malena Jaramillo Espinosa, Juan Manuel D’Attoli, Anthony Boanada-Fuchs, and Monika Kuffer. 2025. “Spatiotemporal Dynamics of Informal Settlements Across Argentine Cities: A National-Scale Analysis.” SSRN Working Paper.

**Links**  
SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5588589  
DOI: https://doi.org/10.2139/ssrn.5588589

**Evidence type:** Argentina-specific geographic context.  
**Evidence strength:** Medium; national-scale empirical work but an unreviewed preprint.  
**Verification:** Bibliography and reported findings checked; SSRN PDF access was intermittently blocked.

### Direct findings

- RENABAP settlement polygons cover approximately 683.92 km² in Argentine urban areas with more than 2,000 residents.
- Extra-small urban areas contain approximately 266.99 km² of informal-settlement area, compared with 216.23 km² in large metropolitan areas.
- Estimated settlement-area growth from 2016 to 2023 averaged 1.78% annually.
- Growth was faster in small urban areas, approximately 2.78% annually, than in large metropolitan areas, approximately 1.44%.

### Useful for Barrios Visibles

- Strong independent support for the argument that Argentina’s informal-settlement geography is dispersed beyond Greater Buenos Aires.
- Supports expecting larger registry staleness and monitoring gaps in small and peripheral urban areas.
- Helps explain why nationally averaged verticality assumptions derived from central Buenos Aires are inappropriate elsewhere.

### Does not establish

- It does not validate RENABAP’s family counts or Barrios Visibles’ population estimate.
- Its statement that roughly 1.2 million RENABAP families were “surveyed in their homes” should not be repeated without qualification. RENABAP documents a mixed estimation system using community-leader declarations, enumerator observation, satellite dwelling counts, and later house-to-house updates.
- Its “several orders” language is not supported by the magnitude of the reported differences.

**Tags:** `Argentina`, `RENABAP`, `small-cities`, `periphery`, `settlement-growth`, `SSRN`

---

## `quinn2024`

**Citation**  
Quinn, John A., et al. 2024. “Open Buildings 2.5D Temporal Dataset Tracks Building Changes Across the Global South.” Google Research/Open Buildings temporal dataset paper.

**Links**  
Project and exact bibliographic record should be added from the version used in the Barrios Visibles analysis.

**Evidence type:** Temporal control.  
**Evidence strength:** High for dating detected construction within dataset limits; irrelevant to occupancy by itself.  
**Verification:** Dataset already used in the project; exact citation metadata needs normalization.

### Useful for Barrios Visibles

- Provides an independent way to test whether footprint excess is explained by post-census construction.
- In the current Barrios Visibles clean low-rise tests, post-2022 construction explains no more than roughly 20% of the excess.

### Does not establish

- Building date does not establish occupancy, residential use, household count, or census coverage.
- Temporal detection errors and confidence thresholds must remain documented with the project results.

### Follow-up

- Add exact authors, DOI/arXiv identifier, dataset version, temporal coverage, and access date.
- Link the source to the analysis artifact that produced the ≤20% result.

**Tags:** `Argentina-analysis`, `temporal-buildings`, `post-2022`, `needs-metadata`

---

# VII. Reviews and conceptual sources

## `kuffer2016`

**Citation**  
Kuffer, Monika, Karin Pfeffer, and Richard Sliuzas. 2016. “Slums from Space—15 Years of Slum Mapping Using Remote Sensing.” *Remote Sensing* 8 (6): 455.

**Links**  
DOI and full text: https://doi.org/10.3390/rs8060455

**Evidence type:** Review and citation bridge.  
**Evidence strength:** High as a review; not direct undercount evidence.  
**Verification:** Verified full text.

### Direct contributions

- Reviews 87 slum-mapping case studies published from 2000 through 2015.
- Establishes that official information on settlement extent, population, buildings, and boundaries is frequently missing or inconsistent.
- Reviews evidence that VHR imagery can extract roof- or dwelling-level information for settlement mapping and population estimation.
- Identifies small buildings, extreme roof density, overlapping roofs, verticality, contextual diversity, and weak reference data as recurring limitations.
- Leads to the Gunter, Galeon, Kit, and Kibera studies annotated above.

### Useful for Barrios Visibles

- Literature-level support that remote sensing is an established way to map informal urban form where administrative information is incomplete.
- Provides the citation trail for more direct empirical sources.

### Does not establish

- The review’s statements are not new population-undercoverage measurements.
- Cite original studies wherever a specific number is important.

**Tags:** `review`, `remote-sensing`, `slum-mapping`, `citation-bridge`

---

## `thomson2020`

**Citation**  
Thomson, Dana R., Monika Kuffer, Gianluca Boo, et al. 2020. “Need for an Integrated Deprived Area ‘Slum’ Mapping System (IDEAMAPS) in Low- and Middle-Income Countries.” *Social Sciences* 9 (5): 80.

**Links**  
DOI: https://doi.org/10.3390/socsci9050080  
Open manuscript: https://eprints.gla.ac.uk/256040/

**Evidence type:** Conceptual framework.  
**Evidence strength:** High for multi-source design; not quantitative undercount evidence.  
**Verification:** Verified full text.

### Direct contributions

- Explains why four common deprivation-mapping approaches remain siloed.
- Census and household-survey aggregation measures household deprivation but often lacks current neighborhood geography.
- Community mapping is locally precise but difficult to scale.
- Image interpretation and machine learning capture morphology but cannot observe every social condition.
- Proposes integrating official, community, field, and Earth-observation evidence.

### Useful for Barrios Visibles

- Strong conceptual support for triangulating RENABAP, INDEC, community information, and visible buildings rather than treating any single source as complete.

### Does not establish

- It supplies no direct population-undercoverage rate.

**Tags:** `IDEAMAPS`, `multi-source`, `conceptual`, `community-data`, `official-data`

---

## `kuffer2021`

**Citation**  
Kuffer, Monika, Jiong Wang, Dana R. Thomson, et al. 2021. “Spatial Information Gaps on Deprived Urban Areas (Slums) in Low-and-Middle-Income Countries: A User-Centered Approach.” *Urban Science* 5 (4): 72.

**Links**  
DOI and full text: https://doi.org/10.3390/urbansci5040072

**Evidence type:** Stakeholder and information-needs context.  
**Evidence strength:** Medium-high for documented information gaps.  
**Verification:** Verified full text.

### Direct findings

- Synthesizes surveys and workshops with governments, community organizations, NGOs, and researchers.
- Base maps were commonly outdated, incomplete, limited to part of a city, and especially sparse in dynamic peri-urban areas.
- Building data were identified as important inputs to population models.
- Deprived-area residents were described as among those least likely to be counted and served.

### Useful for Barrios Visibles

- Supports the connection between peripheral settlement growth, missing spatial information, and service exclusion.
- Provides user-centered evidence that official users themselves need building-level information and uncertainty metadata.

### Does not establish

- It is not an enumeration audit and supplies no independently measured undercount rate.

**Tags:** `stakeholders`, `spatial-data-gaps`, `peri-urban`, `service-delivery`

---

## `wang2022`

**Citation**  
Wang, Jiong, Stefanos Georganos, Monika Kuffer, et al. 2022. “On the Knowledge Gain of Urban Morphology from Space.” *Computers, Environment and Urban Systems* 95: 101831.

**Links**  
DOI: https://doi.org/10.1016/j.compenvurbsys.2022.101831

**Evidence type:** Footprint-utility context.  
**Evidence strength:** Medium.  
**Verification:** Verified through the Springer chapter and source record.

### Direct contribution

- Finds that incomplete or suboptimal open building maps can still provide substantial knowledge about urban morphology.
- Warns that footprint omissions and errors propagate into downstream metrics.

### Useful for Barrios Visibles

- Supports treating footprint layers as meaningful evidence without presenting them as exhaustive ground truth.

### Does not establish

- It does not validate building counts as dwelling counts or estimate population.

**Tags:** `urban-morphology`, `footprint-quality`, `knowledge-gain`, `caution`

---

# VIII. Sources to treat cautiously

## `okyere2025`

**Citation**  
Okyere, Franz, Meng Lu, and Ansgar Brunn. 2025. “Evaluating the Quality of Open Building Datasets for Mapping Urban Inequality: A Comparative Analysis Across 5 Cities.” arXiv:2508.12872.

**Links**  
Abstract: https://arxiv.org/abs/2508.12872  
DOI: https://doi.org/10.48550/arXiv.2508.12872

**Evidence type:** Caution; cross-provider disagreement.  
**Evidence strength:** Low as affirmative validation. It is an unreviewed preprint with no population ground truth.  
**Verification:** Verified full text.

### Direct findings

- Compares Google, Microsoft/VIDA, and OSM footprint geometry across Accra, Nairobi, Caracas, Berlin, and Houston.
- Reported counts include:
  - Accra: 2,619,136 Google polygons versus 292,038 OSM polygons.
  - Caracas: 387,049 Google polygons versus 12,395 OSM polygons.
- Only 8.19% of Google polygons overlapped OSM in Accra and 3.97% in Caracas, while 61% and 57% of OSM polygons overlapped Google, respectively.
- Geometric agreement was poorer in Caracas than in the formal Global North comparison cities.

### Useful for Barrios Visibles

- Only for acknowledging that providers disagree and complex urban morphology reduces polygon alignment.
- Its bibliography leads to stronger sources including `gevaert2024`, `chamberlain2024`, `herfort2023`, and `boo2022`.

### Do not use it to claim

- that Google systematically omits Caracas or Accra buildings;
- that OSM represents ground truth;
- that low polygon overlap measures real-world building completeness;
- anything about population, dwellings, households, or census accuracy.

### Methodological problem

The analysis explicitly assumes OSM is closer to ground truth despite its own counts showing that OSM is dramatically sparser. Non-overlap therefore cannot distinguish missing Google buildings from missing OSM buildings, segmentation differences, dates, or geometry mismatch. Some discussion language conflates disagreement with omission.

**Tags:** `arXiv`, `weak-evidence`, `OSM-reference`, `provider-disagreement`, `do-not-overclaim`

---

# IX. Evidence synthesis for the blog

## What the literature now supports strongly

1. **Building evidence is a legitimate independent constraint.** Complete or representative household enumeration combined with building footprints can predict population at fine resolution (`boo2022`). Informal structures can be detected with high field-validated accuracy in suitable imagery (`galeon2008`).

2. **Large official-versus-visible discrepancies have precedent.** Roof-based population estimation exceeded a census-based Dar es Salaam estimate by roughly two million (`kuffer2019`). Image mapping reportedly found 10,000 more dwellings than a Johannesburg government estimate (`gunter2009`).

3. **Informal residents routinely disappear geographically.** Census-derived gridded products recovered no more than 39% of community-derived populations in 118 settlements (`thomson2021`). GHS-POP systematically moved residents away from dense informal and high-rise areas (`kuffer2022`).

4. **Enumeration gaps can be literal, not merely statistical.** Colombia documented census areas that were partially enumerated or never visited and used community plus satellite evidence to estimate their population (`sanchez-cespedes2024`).

5. **One visible roof is not a safe upper bound on households.** A remotely delineated roof or roof block averaged 11.2 households in Kibera (`marx2019`); fieldwork documents multi-story tenements and internally subdivided rental structures (`ono2020`, `vanhuysse2024`).

6. **The main footprint errors make Barrios Visibles conservative.** Missed buildings and merged roofs reduce visible structure counts; verticality and subdivision increase households relative to footprints (`boo2022`, `gevaert2024`, `marx2019`, `ono2020`). False positives and non-residential buildings operate in the opposite direction and must remain controlled through size filtering, imagery inspection, and sensitivity analysis.

7. **Multiple sources are stronger than any one provider.** Google, Microsoft, Ecopia, and OSM differ sharply (`chamberlain2024`). OSM is too incomplete to function as universal ground truth (`herfort2023`). The VIDA union plus direct imagery inspection is therefore defensible, but should not be called complete.

## What the literature does not independently prove

- It does not independently validate an Argentine gap of exactly 2.9–3.4 million people.
- It does not provide a universal footprint-to-dwelling or footprint-to-household multiplier.
- It does not prove that Argentina’s national census total is wrong solely because local allocation is wrong.
- It does not allow African or Asian occupancy ratios to be transferred directly to Argentina.
- It does not eliminate false positives, non-residential buildings, temporal mismatch, or settlement-boundary error.

## Strongest defensible inference

The international literature independently validates the components of the Barrios Visibles argument: building footprints contain population information; official and census-derived systems often underrepresent dense informal areas; missing settlement geography contributes to enumeration gaps; planar roof counts omit subdivision and vertical occupancy; and closely analogous roof-based analyses have produced much larger populations than official estimates. Combined with the Argentine comparisons against both RENABAP and INDEC, this makes systematic underestimation substantially more plausible than an explanation based only on footprint overcount.

---

# X. Repository handoff instructions

An organizing agent should preserve this file as the source audit and create structured derivatives rather than rewriting it destructively.

## Recommended repository structure

```text
literature/
  README.md
  evidence-matrix.csv
  sources/
    thomson2021.md
    kuffer2019.md
    ...
  claims/
    geographic-misallocation.md
    footprint-validity.md
    households-per-footprint.md
    official-enumeration-gaps.md
    footprint-limitations.md
  bibliography/
    references.bib
  originals/
    README.md
```

Do not commit copyrighted PDFs unless their licenses permit redistribution. Store stable URLs, DOI links, Zotero keys, and local attachment paths instead.

## Suggested per-source front matter

```yaml
---
citation_key: thomson2021
title: "Evaluating the Accuracy of Gridded Population Estimates in Slums"
year: 2021
evidence_type:
  - direct_analogue
  - method_precedent
strength: high
verification: verified_full_text
geographies:
  - Nigeria
  - Kenya
claims:
  - informal_population_underrepresentation
  - households_per_building
  - contiguous_roof_merging
doi: 10.3390/urbansci5020048
zotero_key: null
status: retained
---
```

## Suggested evidence-matrix columns

```text
citation_key
claim_id
relationship
evidence_type
geography
unit_of_analysis
sample_size
direct_result
page_or_section
supports
does_not_establish
strength
verification
doi
url
zotero_key
follow_up
```

Allowed `relationship` values should be:

- `supports`
- `qualifies`
- `contradicts`
- `method_validates`
- `context_only`

## Maintenance rules

1. Every quantitative claim must include a page, section, figure, or table.
2. Reviews should point to original sources for important numbers.
3. “Does not establish” must remain mandatory, not optional.
4. Separate census-enumeration error from gridded-population allocation error.
5. Separate buildings, roofs, roof blocks, dwellings, households, families, and residents.
6. Record whether a reference population is a census, complete enumeration, sample-based community estimate, modeled estimate, or undocumented literature value.
7. Treat geographic transfer as a limitation unless a source includes Argentina or a clearly comparable Latin American context.
8. Retain counterevidence such as `kit2013` and the imagery omissions in `angeles2009`.
9. Connect every blog claim to an evidence-matrix row, not directly to prose notes.
10. Add a CI check that rejects evidence rows lacking `citation_key`, `claim_id`, `relationship`, `page_or_section`, and `verification`.

## Immediate follow-ups

- Retrieve and inspect the original `gunter2009` paper.
- Normalize the exact citation and version for `quinn2024`.
- Add Zotero keys for every retained source.
- Import citations into a single BibTeX export generated from Zotero rather than maintaining two independent bibliographies.
- Link each Argentina-specific numerical finding to its reproducible output artifact.
- Add separate entries for the INDEC reconciliation, IDECBA Padre Ricciardelli evidence, RENABAP methodology, and the 95%-contained-tract analysis. Those sources are central to the blog but outside the international bibliography audited here.

