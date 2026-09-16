# Sources from the dwelling-yield conversation

This note consolidates every identifiable external source discussed in the conversation about converting building footprints into occupied dwellings, the sensitivity parameter \(y\), and the interpretation of Census and RENABAP discrepancies.

## Interpretation established in the conversation

The revised model is:

\[
H_i = \max(R_i, F_i \times y \times 1.1)
\]

where:

- \(H_i\) is the estimated household floor for settlement \(i\);
- \(R_i\) is RENABAP's recorded family count;
- \(F_i\) is the number of eligible mapped building footprints;
- \(y\) is the **net occupied-dwelling yield per detected footprint**; and
- 1.1 is RENABAP's assumed families per inhabited dwelling.

The literature does not establish a universal one-to-one relationship between footprints and occupied dwellings. It documents mechanisms in both directions:

- **Downward pressure on \(y\):** non-residential buildings, ancillary structures, vacancy, unfinished buildings, and false-positive or fragmented footprints.
- **Upward pressure on \(y\):** missed buildings, merged or connected roofs, multiple dwellings within one footprint, and vertical construction.

Accordingly, \(y=0.85\) is best described as a **plausible or cautious central specification**, not a proven lower bound. The \(y=0.70\) scenario approximates the deliberately stringent combination \(0.85 \times 0.85 = 0.7225\), while \(y=0.60\) is a severe stress test near aggregate parity.

---

## 1. IBGE (2024): Brazil's 2022 favela census

### Citation

Instituto Brasileiro de Geografia e Estatística (IBGE). 2024. *Censo Demográfico 2022: Favelas e Comunidades Urbanas: Resultados do universo*. Rio de Janeiro: IBGE. [Official catalog record](https://biblioteca.ibge.gov.br/index.php/biblioteca-catalogo?id=2102134&view=detalhes). [PDF](https://biblioteca.ibge.gov.br/visualizacao/livros/liv102134.pdf). [Current IBGE results page](https://www.ibge.gov.br/geociencias/organizacao-do-territorio/tipologias-do-territorio/15788-favelas-e-comunidades-urbanas.html).

### What it contributes

- The 2022 census provides an official national inventory of dwellings in Brazilian *Favelas e Comunidades Urbanas*.
- The figures discussed in the conversation imply that approximately **84.8% of enumerated dwellings were occupied permanent private dwellings**.
- The report also distinguishes houses, apartments, collective dwellings, vacant dwellings, occasional-use dwellings, establishments, and buildings under construction.
- Its state breakdown documents meaningful vertical housing in some favela contexts, especially Rio de Janeiro.

### Correct use in the paper

Use this as an **occupancy benchmark among units already classified as dwellings**. It supports the plausibility of an occupancy factor near 0.85 at that stage of the conversion.

### Important limitation

The IBGE denominator is not remotely detected building footprints. Therefore, the finding does **not** show that 84.8% of all footprints are occupied dwellings. It does not independently account for shops, sheds, ancillary structures, footprint errors, merged roofs, or multiple dwellings per footprint. It cannot by itself validate \(y=0.85\) as a full footprint-to-occupied-dwelling conversion.

---

## 2. Checchi et al. (2013): satellite structure counts and displaced populations

### Citation

Checchi, Francesco, Barclay T. Stewart, Jennifer J. Palmer, and Chris Grundy. 2013. “Validity and Feasibility of a Satellite Imagery-Based Method for Rapid Estimation of Displaced Populations.” *International Journal of Health Geographics* 12: 4. [https://doi.org/10.1186/1476-072X-12-4](https://doi.org/10.1186/1476-072X-12-4). [Open full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC3558435/).

### What it contributes

This is the most directly useful empirical source in the conversation because it compares image-interpreted structures with independent population or shelter counts across 11 sites.

#### Bairro Esturro, Mozambique

- Analyst 1 counted 1,643 residential and 242 other structures: **87.2% residential** among 1,885 total structures.
- Analyst 2 counted 1,194 residential and 222 other structures: **84.3% residential** among 1,416 total structures.
- The mean image count used for estimation was 1,419 residential structures.
- Independent field methods estimated 1,685 residential structures; an earlier government census counted 1,828.
- The imagery analysis therefore **undercounted residential structures**, but a higher assumed occupancy partly offset that error.
- The final imagery-based population estimate was 8,940, compared with a reference estimate of 9,523: **6.1% low**.

These figures place an 85% residential share within an observed range, while also showing that image interpretation can omit residential structures.

#### Haiti

- Champs-de-Mars: 2,361 mean imagery structures versus 4,542 census shelters. The imagery-based population estimate was **46.1% below** the reference population.
- Delmas 24, Sollino, and Fort National: 3,889 mean imagery structures versus 8,565 census shelters. The imagery-based population estimate was **47.6% below** the reference population.
- The paper attributes the difficulty to dense, complex layouts, connected roofs, tree cover, collapsed structures, and the inability to identify what constituted one household dwelling from above.

These cases show that one visible imagery structure can correspond to roughly two field-enumerated shelters in dense settings.

### Correct use in the paper

Use Checchi et al. for three claims:

1. Around 85% of mapped structures were classified as residential by two analysts in the Mozambique case.
2. Remote interpretation can miss residential structures even where the final population estimate is close.
3. In dense or connected-roof environments, imagery structure counts can materially understate the number of shelters or dwellings.

### Important limitations

- The study concerns displaced-person settings and one urban Mozambican neighborhood, not Argentine informal settlements.
- The 84.3% and 87.2% values are ratios calculated from the paper's Table 3 counts; they are not a universal parameter proposed by the authors.
- The study multiplies structures by an external occupancy estimate. Its full estimation error combines errors in structure counts and people-per-structure assumptions.

---

## 3. Thomson et al. (2021): gridded population products miss slum populations

### Citation

Thomson, Dana R., Andrea E. Gaughan, Forrest R. Stevens, Gregory Yetman, Peter Elias, and Robert Chen. 2021. “Evaluating the Accuracy of Gridded Population Estimates in Slums: A Case Study in Nigeria and Kenya.” *Urban Science* 5 (2): 48. [https://doi.org/10.3390/urbansci5020048](https://doi.org/10.3390/urbansci5020048). [Reproducibility repository](https://github.com/danathomson/Accuracy_of_GridPops_in_Slums).

### What it contributes

- The paper compares nine gridded population products with field-referenced population estimates for 118 slum areas in Lagos, Port Harcourt, and Nairobi.
- Even the best-performing product in the discussion, HRSL, captured only about **39%** of the field-referenced population in Port Harcourt.
- The paper demonstrates that population models can severely underrepresent people in deprived and informal urban areas, even when the settlements are physically present.

### Correct use in the paper

Use this as evidence that conventional gridded population products are unreliable validators of population totals inside informal settlements. It supports the broader mechanism of systematic underrepresentation in modelled population data.

### Important limitation

This paper evaluates gridded population estimates, not national censuses and not building-footprint-to-dwelling conversion rates. It supports the general omission mechanism but does not identify an Argentine value for \(y\).

---

## 4. Mahabir et al. (2018): review of remote detection and mapping of slums

### Citation

Mahabir, Ron, Arie Croitoru, Andrew T. Crooks, Peggy Agouris, and Anthony Stefanidis. 2018. “A Critical Review of High and Very High-Resolution Remote Sensing Approaches for Detecting and Mapping Slums: Trends, Challenges and Emerging Opportunities.” *Urban Science* 2 (1): 8. [https://doi.org/10.3390/urbansci2010008](https://doi.org/10.3390/urbansci2010008).

### What it contributes

- Reviews high- and very-high-resolution remote-sensing approaches used to detect and map slums.
- Documents substantial variation in settlement morphology, roofing materials, density, texture, geography, and mapping methods.
- Emphasizes that methods trained or validated in one locality do not automatically generalize to another.
- Supports the need to combine imagery with other geospatial and local information.

### Correct use in the paper

Use this to justify treating footprint accuracy and footprint-to-dwelling conversion as context-dependent rather than universal. It supports sensitivity analysis and cautious interpretation of any single yield value.

### Important limitation

This is a methodological review, not a direct empirical estimate of occupancy, residential share, or dwellings per footprint.

---

## 5. Kuffer, Pfeffer, and Sliuzas (2016): fifteen years of slum mapping from space

### Citation

Kuffer, Monika, Karin Pfeffer, and Richard Sliuzas. 2016. “Slums from Space—15 Years of Slum Mapping Using Remote Sensing.” *Remote Sensing* 8 (6): 455. [https://doi.org/10.3390/rs8060455](https://doi.org/10.3390/rs8060455).

### What it contributes

- Reviews remote-sensing studies of slums published from 2000 through 2015.
- Shows that informal-settlement morphology is heterogeneous and strongly context-dependent.
- Identifies recurring obstacles including roof-material variation, high density, small structures, spectral confusion, shadows, and inconsistent definitions.
- Supports the argument that errors can occur through both omission and commission and that no single global mapping rule is sufficient.

### Correct use in the paper

Use this as general methodological support for uncertainty in footprint detection and for testing multiple size filters and dwelling yields.

### Important limitation

The review does not provide an empirical dwelling yield for Argentina and should not be cited as direct validation of \(y=0.85\).

---

## 6. Gaugris et al. (2007): multiple structures and ancillary buildings within rural households

### Citation

Gaugris, J. Y., M. W. van Rooyen, J. du P. Bothma, and M. J. Van der Linde. 2007. “Hardwood Utilization in Rural Households of the Mankakulane Community, Maputaland, South Africa.” *Ethnobotany Research and Applications* 5: 97–114. [https://doi.org/10.17348/era.5.0.97-114](https://doi.org/10.17348/era.5.0.97-114). [Repository copy](https://scholarspace.manoa.hawaii.edu/items/3c3fab59-d865-4f7c-a651-d10f388ff831).

### What it contributes

- The study inventories **226 buildings used for habitation or other purposes** in rural South African households.
- The household compounds contained multiple structures serving different functions.
- It provides direct evidence for a mechanism that can make raw building counts exceed dwelling or household counts: several structures can belong to one household, and not every structure is residential.

### Correct use in the paper

Use this as evidence for **downward pressure on the net yield** from ancillary and non-residential structures. It helps justify testing \(y<1\).

### Important limitations and correction

- This is rural Maputaland, South Africa, not Mozambique and not an urban informal settlement.
- It does not supply the 84.3–87.2% residential shares. Those values come from Checchi et al.'s Bairro Esturro counts.
- Its 226-building sample should not be converted directly into an Argentine yield parameter without a comparable household-compound analysis.

---

## 7. De Grande (2023): replicated records in Argentina's 2010 Census

### Citation

De Grande, Pablo. 2023. “Viviendas repetidas en el censo de 2010 de la Argentina: una exploración empírica.” *Notas de Población* 50 (117): 119–144. [https://doi.org/10.18356/16810333-50-117-6](https://doi.org/10.18356/16810333-50-117-6). [CEPAL publication page](https://www.cepal.org/es/publicaciones/69004-viviendas-repetidas-censo-2010-la-argentina-exploracion-empirica). [PDF](https://www.aacademica.org/acta.academica/box/pablo.de.grande/79.pdf).

### What it contributes

- Uses Argentina's 2010 REDATAM census data to identify implausibly identical sequences of dwelling, household, and person records.
- Estimates **96,086 replicated dwelling records**, approximately **0.85%** of census dwellings.
- Those records contain an estimated **312,229 replicated person records**, approximately **0.78%** of the national population.
- Some local areas show extreme concentrations of replicated records, supporting concern about local geographic reliability.

### Correct use in the paper

Use this as evidence of documented **duplication and geographic reassignment or misallocation** in the 2010 Census. It demonstrates that internally coherent census totals can contain serious local data-quality failures.

### Important limitation and direction of evidence

- This is not evidence of population omission. It is direct evidence of duplicated records and possible inflation or geographic misallocation.
- Replication could have been used to compensate for failed enumeration, but the study does not establish the true net population error.
- It concerns the 2010 Census, not the 2022 Census.
- If duplicated records inflated counts in relevant comparison areas, they would make a footprint-versus-Census deficit harder, not easier, to produce.

---

## Claim-to-source map

| Claim or mechanism | Best source | Direction | Main caution |
|---|---|---|---|
| Roughly 85% of image-counted structures were classified as residential in one low-rise African urban case | Checchi et al. 2013, Bairro Esturro | Supports \(y\) near 0.85 | One site; values are calculated from analyst counts |
| About 85% of already-classified favela dwellings were occupied permanent dwellings | IBGE 2024 | Supports an occupancy factor near 0.85 | Denominator is dwellings, not footprints |
| Connected roofs and dense layouts can make image structure counts understate shelters by about half | Checchi et al. 2013, Haiti cases | Upward pressure on \(y\) | Displacement settings; not directly Argentina |
| Image interpretation can miss residential structures even in a low-rise neighborhood | Checchi et al. 2013, Bairro Esturro | Upward pressure on \(y\) | Final population error also depends on occupancy assumptions |
| One household can contain several structures with different uses | Gaugris et al. 2007 | Downward pressure on \(y\) | Rural South African compound settlement |
| Population grids substantially undercount slum populations | Thomson et al. 2021 | Supports broader omission mechanism | Not a census or footprint-yield validation |
| Informal-settlement mapping is heterogeneous and context-dependent | Mahabir et al. 2018; Kuffer et al. 2016 | Supports sensitivity analysis | Reviews, not direct yield estimates |
| Argentina's census data have contained duplicated and geographically misplaced records | De Grande 2023 | Duplication/misallocation, not omission | 2010 rather than 2022 |

## Recommended language for the manuscript

### For \(y=0.85\)

> The \(y=0.85\) specification is a cautious net occupied-dwelling yield: every 100 detected footprints are assumed to represent 85 occupied dwellings after errors in both directions. This value is consistent with observed residential shares in one Mozambican image-counting exercise and with the occupied share of already-classified favela dwellings in Brazil, but neither source directly estimates the net footprint-to-occupied-dwelling yield in Argentina.

### For the low-yield stress tests

> The \(y=0.70\) scenario approximates separately retaining 85% of footprints as dwellings and 85% of those dwellings as occupied. The \(y=0.60\) scenario is a severe stress test near aggregate parity, not a literature-derived estimate.

### For the parity result

> Matching RENABAP's national total requires a net yield of 0.572 occupied dwellings per raw detected footprint, or 0.593 after excluding footprints below 10 m². Under a binary one-dwelling-per-footprint interpretation, approximately 43% of raw footprints would have to be vacant, non-residential, ancillary, erroneous, or otherwise fail to represent an occupied dwelling.

### For the Argentina duplication paper

> De Grande's analysis is evidence of duplicated census records and geographic misallocation, not population omission. It should be used to question the local reliability of census distributions, not to claim that the national Census necessarily missed the duplicated people.

## Notes for Zotero/repository ingestion

- Prefer the DOI URL as the canonical item URL for all journal articles.
- Store the IBGE book as a report or book with `IBGE` as the institutional author and attach the official PDF.
- Suggested tags: `dwelling-yield`, `building-footprints`, `occupancy`, `informal-settlements`, `remote-sensing`, `census-quality`, `duplication`, `geographic-misallocation`, `Argentina`, `Brazil`, `Mozambique`, `Haiti`, `South-Africa`.
- Do not merge the Checchi and Gaugris notes. They support distinct mechanisms and concern different study sites.
- The numerical Barrios Visibles results discussed in the conversation—RENABAP totals, footprint totals, parity yields, and sensitivity outputs—are project outputs rather than external sources and therefore are not bibliographic entries here.

