---
layout: post.njk
title: "Barrios Visibles, Part II: Open Building Footprint Evidence of Substantial Population Undercount in Argentina's 2022 Census"
date: 2026-05-06
tags: ["writing", "research", "geospatial"]
---

*Argentina's 2022 national census appears to undercount the population of registered informal settlements by roughly half, a finding that converges with what I documented earlier this month in a [working paper](/posts/writing/informal-settlements-argentina/) on the country's informal-settlement registry, RENABAP. These findings show how open global datasets like building footprints can now surface coverage problems that traditional methods cannot, and that this capacity matters most precisely where official data is weakest.*

---

## Background

A few weeks ago I published *[Barrios Visibles](https://barriosvisibles.org)*, a working paper showing that Argentina's national registry of informal settlements (RENABAP) appears to undercount the population of its own registered settlements by roughly three million people. The methodology was simple: I spatially joined open global building-footprint data to the 6,467 polygons RENABAP itself maintains, and compared the number of detected structures against the number of families officially recorded. Across the country, building footprints exceed recorded family counts by 59 percent in raw terms, and by 83 percent after applying RENABAP's own families-per-dwelling ratio. Under conservative population multipliers, the implied informal-settlement population is 6.3 to 7.6 million, against an official total closer to 4 million.

The original paper deliberately did not compare its findings against INDEC's 2022 national census, for one specific reason: the two sources aren't independent. INDEC's enumeration in informal settlements relied on the same community *referentes* and barrio organizations that RENABAP itself uses for its family estimates, and both products trace back to the same 2010 baseline projections. INDEC's own statisticians anticipated coverage problems in informal areas before fieldwork began. Comparing the two directly would have meant comparing two outputs of overlapping operational machinery, not two independent measurements.

So I asked a different question: how many of the people INDEC counted actually fall inside RENABAP's settlement boundaries? INDEC publishes population in small census tracts. For each barrio, I added up the population of the tracts it overlaps, weighted by how much of each tract is actually inside the barrio. Then I compared that number to the population implied by the building footprints in the same barrio. After correcting for the obvious methodological objection (more on that below), the finding is clear: like RENABAP, INDEC accounts for roughly half the people that satellite-visible buildings suggest live there. The same three million people missing from RENABAP appear to be missing from the national census too.

---

## Implications beyond Argentina

INDEC is one of Latin America's better-resourced national statistical institutes, and Argentina is, by regional standards, a country with reasonably mature administrative data systems. If the country's primary demographic instrument is missing roughly half the residents of its informal settlements, the implications for the rest of the region, and for the Global South more broadly, are larger, not smaller. Whatever the gap looks like in Argentina, it's almost certainly worse in countries with thinner statistical capacity, less political pressure to enumerate marginal populations, and fewer alternative data sources to fall back on.

The deeper point is about what's now possible. Five years ago, an analysis of this kind would have required a research team with proprietary data and months of field operations. The infrastructure that makes it tractable today, open continental-scale building footprints from VIDA, Source Cooperative as a hosting layer, GeoParquet as an analytic format, DuckDB as a query engine, barely existed. Now the entire pipeline runs on a laptop in seconds.

This is what cloud-native geospatial actually changes. Anyone with basic technical literacy can now run an analysis that previously required institutional resources. A municipal GIS staffer in La Plata can run the same queries I ran. So can a journalist in Bogotá or an analyst at a community organization in Lima. So can a researcher at a small university in Lagos.

In Argentina specifically, this matters more than it did a few years ago. SISU, the institution that maintained RENABAP, was [effectively closed](https://www.pagina12.com.ar/2026/02/11/cierre-de-subsecretaria-de-integracion-sociourbana-fuerte-golpe-a-la-politica-publica-de-vivienda/) earlier this year. Whatever one's view of that decision, the question of how the country counts the residents of its informal settlements doesn't pause with it. Open global data offers something the national infrastructure no longer reliably provides: a baseline that any municipality, NGO, journalist, or researcher can use to check official counts in their own jurisdiction. It isn't a replacement for state statistical capacity, and shouldn't be framed as one. But it's a real complement, and right now in Argentina, it's among the few options available.

---

## Objections and validation

Comparing census tract populations to building counts inside barrio polygons requires an assumption about how each tract's residents are distributed in space. INDEC publishes population at the tract level, not at finer resolution, so when a barrio sits partly inside a tract, you have to estimate how much of that tract's population lives within the barrio specifically. The simplest approach, and the one I used above, is to assume the population is spread evenly across the tract. If a barrio covers 10 percent of a tract's area, it gets credited with 10 percent of that tract's people.

This works reasonably well when the area inside the barrio looks similar to the area outside it. It breaks down when the barrio is much denser than its surroundings, which informal settlements almost always are. A small dense barrio sitting inside a much larger, mostly empty rural tract will have most of the tract's residents living inside it, but the math will assign it only a small fraction by area and distribute the rest across the empty surroundings. The result is an inflated undercount that mostly reflects the geometry of the calculation rather than any real coverage gap in the census.

The provincial breakdown shows this clearly. In the unfiltered analysis, San Juan came out at 7x, La Pampa and Santa Cruz at 4x, far higher than anything reported in *[Barrios Visibles](https://barriosvisibles.org)*. These are the provinces where census tracts are largest and barrios occupy the smallest, densest fractions of them. INDEC didn't suddenly miss seven times more people in San Juan than RENABAP did; the calculation produced an inflated number, and the analysis has to correct for it.

The correction is to limit the analysis to tracts where the area-weighting assumption is close to true: tracts that are mostly or entirely covered by one barrio. In those cases, the population of the tract and the population of the barrio are nearly the same number, and the geometry stops distorting the comparison. If the apparent undercount were entirely an artifact of area-weighting, the ratio should collapse toward 1 as the coverage threshold rises. If a real undercount is present underneath the artifact, the ratio should fall partway and then stabilize.

| Tract barrio-coverage | Barrios in subset | Pop. undercount ratio |
|-----------------------|-------------------|-----------------------|
| 0% (all tracts)       | 6,467             | 2.62x                 |
| ≥25%                  | 2,151             | 2.27x                 |
| ≥50%                  | 1,089             | 2.17x                 |
| ≥75%                  | 544               | 2.06x                 |
| ≥90%                  | 304               | 1.98x                 |
| ≥95%                  | 223               | 1.88x                 |

The ratio drops from 2.62x to 1.88x as the filter tightens, then flattens. About a quarter of the apparent undercount was the geometry problem; the remaining three-quarters is a real signal. In tracts that are almost entirely barrio, where the comparison is most defensible, INDEC's allocated population is roughly half what the building footprint count suggests should be there.

Further tests do not change the finding. Re-running the analysis with different household-size assumptions, including INDEC's own conservative national average of 2.8 persons per household, still produces ratios between 1.7x and 2.1x. A separate test compared population density and household sizes in tracts that border barrios but contain none of their area; if INDEC enumerators had been counting barrio residents at adjacent formal addresses, those border tracts should show inflated household sizes. They don't. The household-size signal in border tracts sits at the national average, which is consistent with the missing residents being absent from the count rather than reallocated elsewhere.

The two-fold residual gap also matches the central finding from *[Barrios Visibles](https://barriosvisibles.org)*, which compared building footprints to RENABAP's family counts inside the same polygons and found a household-level undercount of about 1.83x. The analyses used different official sources, methods, and inputs, and produced the same range. That convergence is what makes the gap hard to dismiss as a methodological quirk of either approach.

---

## What's at stake

The census matters far beyond its own published tables. National statistical offices produce the population figures that downstream surveys, resource allocation formulas, and policy models rely on. When the census misses people, those errors propagate. If INDEC undercounts barrio residents at the rate this analysis suggests, every estimate that uses the census as its frame inherits the same coverage problem.

Three million is probably conservative. RENABAP only registers settlements in localities above 2,000 inhabitants, so smaller settlements aren't in the registry at all and aren't in this analysis. The household-floor methodology in *[Barrios Visibles](https://barriosvisibles.org)* also doesn't account for vertical density, which means consolidated multi-story villas (especially in CABA) get undercounted further. The real gap is almost certainly larger than what either analysis captures.

This is where open global data matters most. Informal settlements are exactly the kind of blind spot national statistical offices have the hardest time reaching, and open global building footprints fill that gap directly. The data is open, the tools are open, and the whole pipeline runs on a laptop. The infrastructure already exists; what's missing is the awareness that it does.

---

## Acknowledgements

Nissim Lebovits gratefully acknowledges financial support for this research by the Fulbright U.S. Student Program, which is sponsored by the U.S. Department of State and the Comisión Fulbright Argentina. Its contents are solely the responsibility of the author and do not necessarily represent the official views of the Fulbright Program, the Government of the United States, or the Comisión Fulbright Argentina.

---

*All code and data for the analysis available upon request. Contact at nlebovits [at] pm [dot] me.*
