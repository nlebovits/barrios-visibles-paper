# Reproducing INDEC's 2022 demographic reconciliation identity

Compiled 9 September 2026. All figures traced to primary published documents; every
PDF cited was downloaded and text-extracted locally (copies in this directory).

The identity under test:

    P(18 May 2022) = P(1 Jan 2001, revised) + births(2001-2022) - deaths(2001-2022)
                     + net international migration(2001-2022)

INDEC's own answer: **46,122,853** at 18 May 2022.

---

## Headline findings

1. **Every published term of the identity was located and verified against the primary
   documents.** The 2001 base (37,530,617 at 1 Jan 2001), net migration (+375,802), and
   the result (46,122,853 at 18 May 2022) are all confirmed verbatim, with table and page.

2. **A complete, double-sourced DEIS births and deaths series 2001-2022 was assembled**
   (`births_deaths_2001_2022.csv`). Published Serie 5 annual totals and independently
   summed DEIS microdata agree **exactly** for all 18 years where both exist.

3. **The identity, computed with raw DEIS registration counts, gives 45,907,494** —
   leaving a residual of **+215,359 (0.47%)** against INDEC's 46,122,853.

4. **That residual is almost exactly the census undercount INDEC claims.** The same
   computation lands within **15,209 persons (0.03%)** of the *actual 2022 census count*
   of 45,892,285. The balancing equation, fed with INDEC's revised base and *uncorrected*
   flows, reproduces the census count; the entire 230,568-person gap INDEC reports as
   undercount is produced by its unpublished upward corrections to births and deaths.
   **Caveat:** this depends on accepting INDEC's 2001 base revision — with the original
   2004 base the same flows give 45,346,904, i.e. 545,381 *below* the census. See §3.3.

5. **The corrected series are not published**, in AD 39, AD 40, or any data annex found —
   so the identity is **not reproducible to zero from public sources**. But the
   *magnitude* partly is: AD 39 states its births "incluyen los nacimientos anotados como
   'tardíos'", and **AD 40 §4.1 (p. 19) quantifies the fertility correction — six
   provinces adjusted, national TGF impact "inferior a 2%" in 2001, the year of maximum
   adjustment, smaller thereafter.** That published ceiling of <2%, declining, brackets
   the **1.44%** uniform birth uplift that closes my residual almost exactly (§3.3).

6. **The "+1.6%" adjustment to the 2001 base does not reproduce 37,530,617 exactly.**
   Interpolating the 2004 series to 1 Jan 2001 and applying 1.016 overshoots by ~31,000
   (0.08%); the implied *net* uplift is **1.52%**, and it is not uniform by sex
   (men +1.40%, women +1.63%). AD 39's 1.6% is an *ajuste total* — a summed-absolute
   measure — referenced to **30 June** 2001, not a flat scaling at 1 January.

7. **Proof that the DEIS series excludes late registrations, with its exact size, across
   a decade.** Cuadro 19 gives `occ(Y) + occ(Y-1) = published total` **exactly** in 2013,
   2015 and 2022. Excluded late registrations were **1.55% (2013), 1.60% (2015), 0.34%
   (2022)** — a real collapse, consistent with DEIS's documented registration
   improvements. The 2022 figure is still probably understated: seven jurisdictions
   including Buenos Aires and Santa Fe report *exactly zero*, having reported non-zero
   counts in 2015.

8. **Birth under-registration is provincial, not national.** DEIS's census-anchored
   studies give 6% against both the 2001 and 2010 censuses, falling to ~3.0% and 3.8%
   once late registrations are credited — but only 8 of 24 jurisdictions are significant
   at 95%, five show *over*-registration (CABA −10.7%), and the deficit concentrates in
   Santiago del Estero 13.0%, Santa Fe 11.1%, Tierra del Fuego 10.1%. Hospital
   record-matching found 20-28% birth omission and up to 78% infant-death omission in
   specific northern establishments. Full provincial tables in §2.4b.

8b. **External benchmarks contradict any large national under-registration claim.** UNSD
   codes Argentina "C" (≥90% complete); MICS 2019-2020 puts birth registration at 99.7%;
   PAHO puts death sub-registration at 0.5-2.6% since 2012; Mathers et al. and WHO GHE
   put death completeness at 100; Sacco's death-distribution estimates give 100-105%.
   **Death registration is the weakest place to argue incompleteness** — the documented
   mortality problems are fetal deaths, infant deaths in Santiago del Estero, maternal
   deaths (14.2% omission in 2014), and cause-of-death *coding quality* (a different
   claim). See §2.4c.

9. **INDEC benchmarked the census against RENAPER and the COVID vaccination registry at
   the census date itself** (AD 39 §2.4.1.3) and published neither the registry totals nor
   the gap. No published RENAPER national headline total exists at all.

---

## 0. The two 2025 INDEC sources (retrieved in full)

**Análisis Demográfico N° 39** — INDEC (2025), *Estimaciones y proyecciones de
población, por sexo y edad. Total del país. Años 2022-2040*, Serie Análisis
Demográfico N° 39, Buenos Aires, octubre de 2025.
URL: https://www.indec.gob.ar/ftp/cuadros/publicaciones/proyecciones_nacionales_2022_2040.pdf
(mirror: https://censo.gob.ar/wp-content/uploads/2025/10/proyecciones_nacionales_2022_2040.pdf)
Local copy: `ad39.pdf` / `ad39.txt`.

**Análisis Demográfico N° 40** — INDEC (2025), *Estimaciones y proyecciones de
población, por sexo y grupos de edad. Jurisdicciones. Años 2022-2040*, Serie Análisis
Demográfico N° 40, Buenos Aires, octubre de 2025.
URL: https://www.indec.gob.ar/ftp/cuadros/publicaciones/proyecciones_jurisdicciones_2022_2040.pdf
Local copy: `ad40.pdf` / `ad40.txt`.

### The method, in INDEC's words (AD 39, §3.1 "Conciliación demográfica", p. 16)

> "Este método vincula los resultados de dos o más censos de población con la
> fecundidad, la mortalidad y la migración neta de los años intercensales. De esta
> forma, se realiza un ejercicio de consistencia demográfica en el que, partiendo de
> una población inicial se suman nacimientos, se restan defunciones y se adiciona el
> saldo migratorio internacional neto para obtener la estimación de población por edad
> y sexo a la fecha censal, y la población base para las proyecciones."

### Terms of the identity, as published

| Term | Value | Source |
|---|---|---|
| P(1 Jan 2001), revised, both sexes | **37,530,617** | AD 40, Tabla 3, "Población revisada, por sexo, según jurisdicción. 1 de enero de 2001", row "Total del país" (p. 13; ToC entry confirms p. 13) |
| — men | 18,364,239 | AD 40, Tabla 3 |
| — women | 19,166,378 | AD 40, Tabla 3 |
| Immigrants 2001-2022 | **1,289,103** | AD 39, Tabla 11 (p. 31) |
| Emigrants 2001-2022 | **913,301** | AD 39, Tabla 11 |
| Net migration 2001-2022 | **+375,802** | AD 39, Tabla 11 |
| P(18 May 2022) estimated at census date | **46,122,853** | AD 39, Tabla 4 (p. 19) |
| Census 2022 count (definitive), used by INDEC | **45,892,285** | AD 39, Tabla 1, "Indicadores seleccionados de la estructura de la población. Total del país. Años 1947/2022", column "2022" (p. 12) |
| Census 2022 count excl. 5,705 homeless with missing age | 45,886,580 | AD 39, Tabla 4 + footnote (1) |
| Net differential (estimated vs counted) | **-0.5%** | AD 39, Tabla 4 |

AD 39 Tabla 11 decomposes migration further:

| Period | Immigrants | Emigrants | Net |
|---|---|---|---|
| 2001-2009 | 525,736 | 374,931 | +150,805 |
| 2010-2022 | 763,219 | 538,370 | +224,849 |
| **2001-2022** | **1,289,103** | **913,301** | **+375,802** |

(Non-natives 2001-2022: +900,623. Natives: -524,821.)

Note: AD 39 body text (§6.1, p. 30) says the 2010-2022 balance is "224.996"; Tabla 11 on the
same page says 224,849. 150,805 + 224,849 = 375,654, not 375,802; 150,805 + 224,996 =
375,801. **The published components of Tabla 11 do not sum to the published total.**
This is an unresolved internal inconsistency of ~148-153 persons in AD 39, immaterial
to the identity but worth flagging.

### The four different "2022 population" numbers — keep them straight

| Number | What it is | Source |
|---:|---|---|
| 46,234,830 | INDEC projection for **1 July 2022** on the 2010-census base (the pre-census expectation; also the denominator printed in DEIS Serie 5 N° 66 Tabla 1) | INDEC Serie Análisis Demográfico N° 35 series, as carried in DEIS Serie 5 N° 66 |
| 46,044,703 | Censo 2022 **provisional** count (published 31 Jan 2023) = 45,767,858 in viviendas particulares + 273,883 in viviendas colectivas + 2,962 en situación de calle (vía pública) | INDEC, *Censo 2022. Resultados provisionales*, Cuadro 1, "Total" row. https://www.indec.gob.ar/ftp/cuadros/poblacion/cnphv2022_resultados_provisionales.pdf (local copy `censo2022_prov.pdf`) |
| **45,892,285** | Censo 2022 **definitive** count (published Nov 2023) — 152,418 *below* the provisional figure, after deduplication of the digital census | AD 39, Tabla 1, column "2022" (p. 12) |
| **46,122,853** | **Reconciled estimate** at the census date, 18 May 2022 — the base for the 2022-2040 projections | AD 39, Tabla 4 (p. 19) |

The gap that AD 39 calls a 0.5% net undercount is therefore
46,122,853 - 45,892,285 = **230,568 persons**, measured against the *definitive*
count. Note that the *provisional* count (46,044,703) was already within 78,150 of the
reconciled estimate; the deduplication step that produced the definitive count moved
the census figure *away* from the reconciled estimate by 152,418.

### A caution about "1.6%"

Two distinct 1.6% figures appear in AD 39 and are easily conflated:

1. **The 2001 base adjustment** (AD 39, §3.1.1, pp. 16-17; quote on p. 17):
   > "El ajuste total a la población al 30 de junio del 2001 publicada por el INDEC
   > (2004) fue del 1,6%, cuya distribución por edad puede verse en el gráfico 4."

   This is the *total* (i.e. summed-absolute, age-specific) adjustment to the
   **30 June 2001** figure, not a net uplift and not referenced to 1 January.

2. **The 2022 gross census differential** (AD 39, §3.1.2, p. 18):
   > "el Censo 2022 cuenta con un diferencial de población bruto del 1,6%. Este es el
   > resultado de la suma ponderada de los valores absolutos de la sobrenumeración de
   > mujeres (1,1%) y la subnumeración de varones (-2,1%)."

The second has nothing to do with the 2001 base. Arithmetic below shows the *net*
uplift of the 2001 base is ~1.52%, consistent with (1) being a gross measure.

---

## 1. The INDEC (2004) base for 2001, and census omission rates

### Source document

INDEC-CELADE (2004), *Estimaciones y proyecciones de población. Total del país.
1950-2015*, **Serie Análisis Demográfico N° 30** (CELADE Serie OI N° 212), INDEC,
Buenos Aires. Prepared by the Programa de Análisis Demográfico (PAD), Dirección de
Estadísticas Poblacionales; team credited on the title page under the direction of
Gladys Massé and Alejandro Giusti, with CELADE technical advice (José Pujol, Susana
Sckholnik, Guiomar Bay).

**Canonical URL** (INDEC's own library, and the URL AD 39 itself cites):
https://biblioteca.indec.gob.ar/bases/minde/4si20_30.pdf
Mirror given in the brief:
https://ipiec.tierradelfuego.gob.ar/wp-content/uploads/2013/11/Estimaciones_Proyecciones_Pa%C3%ADs_1950_2015.pdf
Both were downloaded and are **byte-identical** (md5 `be76a9dcff48ab457ca37def86dacec2`,
197,702 bytes, 33 pp.), so the mirror is safe to cite from.
Local copies: `proy_1950_2015.pdf` (mirror) and `ad30_official.pdf` (INDEC).

AD 39's bibliography confirms this is the document it means by "INDEC (2004)":
> "Programa de Análisis Demográfico (PAD) de la Dirección de Estadísticas Poblacionales
> (2004). Estimaciones y proyecciones de población. Total del país. 1950-2015 [Análisis
> Demográfico N° 30]. Instituto Nacional de Estadística y Censos (INDEC).
> https://biblioteca.indec.gob.ar/bases/minde/4si20_30.pdf"

### 1.1 Mid-2001 (30 June 2001) estimate — CONFIRMED

Annex "Cuadro 1. Poblacion por sexo y ano calendario" (ToC: begins p. 25; the
1992-2015 continuation carrying 2001 is on p. 26):

| Year | Total | Men | Women |
|---|---|---|---|
| 2000 | 36,783,859 | 18,021,900 | 18,761,959 |
| **2001** | **37,156,195** | **18,201,249** | **18,954,946** |
| 2002 | 37,515,632 | 18,374,920 | 19,140,712 |

Note to the table: *"los resultados que se presentan derivan de la aplicación de la
hipótesis media de evolución de la fecundidad (variante recomendada)."*
The 37,156,195 figure quoted in the brief is therefore **confirmed** as the mid-year
(30 June) 2001 estimate.

### 1.2 Census-date reconciled population for 2001 — CONFIRMED

Cuadro 3, *"Población censada y población corregida por conciliación censal al
17-11-2001, por sexo y grandes grupos de edad"* (p. 10):

| Age group | Counted (17-11-01) | Corrected (17-11-01) | Diff % |
|---|---|---|---|
| **Total** | **36,260,130** | **37,282,971** | **2.7** |
| 0-14 | 10,247,695 | 10,274,920 | 0.4 |
| 15-64 | 22,424,815 | 23,331,837 | 3.9 |
| 65+ | 3,587,620 | 3,676,214 | 2.4 |
| Men, total | 17,659,072 | 18,263,846 | 3.3 |
| Women, total | 18,601,058 | 19,019,125 | 2.2 |

Source line: *"INDEC, Censo Nacional de Población, Hogares y Viviendas 2001; Bankirer
y Raimondi (2003)."*

So the 2001 census count of **36,260,130 on 17 November 2001** is confirmed, and the
2004-vintage census-date reconciled population was **37,282,971**.

### 1.3 Published 2001 census omission rate — CONFIRMED

AD 30 §2.1 (p. 6):
> "Como resultado del análisis por conciliación censal realizado con el asesoramiento
> técnico del Centro Latinoamericano de Demografía (CELADE) surge que la omisión del
> Censo 2001 para el total del país fue del **2,75%**."

Cuadro 1 (p. 7), *"Porcentajes de omisión por sexo. Censos de 1991 y 2001"*
(source: INDEC-CELADE (1995)):

| Census | Both sexes | Men | Women |
|---|---|---|---|
| 1991 | 0.8 | 1.3 | 0.4 |
| 2001 | 2.7 | 3.3 | 2.2 |

(AD 35 later restates these to two decimals: 2001 = 2.75 / 3.31 / 2.20.)

### 1.4 Published 2010 census omission rate — CONFIRMED

INDEC (2013), *Estimaciones y proyecciones de población 2010-2040. Total del país*,
**Serie Análisis Demográfico N° 35**.
URL: https://www.indec.gob.ar/ftp/cuadros/publicaciones/proyeccionesyestimaciones_nac_2010_2040.pdf
Local copy: `ad35_2010_2040.pdf` / `.txt`.

§2.1 (p. 9):
> "Como resultado de este análisis se obtuvo un valor de omisión de **1,99%** para el
> total del país."

Cuadro 1 (p. 9), *"Porcentajes de omisión por sexo. Censos 2001 y 2010"*
(source: INDEC (2013); INDEC-CELADE (2004)):

| Census | Both sexes | Men | Women |
|---|---|---|---|
| 2001 | 2.75 | 3.31 | 2.20 |
| 2010 | **1.99** | **2.44** | **1.55** |

Cuadro 3 (p. 12), *"Población censada y corregida por evaluación demográfica al
27-10-2010"*:

| Age group | Counted (27-10-10) | Corrected | Diff % |
|---|---|---|---|
| **Total** | **40,117,096** | **40,930,448** | **2.0** |
| 0-14 | 10,222,317 | 10,622,674 | 3.8 |
| 15-64 | 25,790,131 | 26,153,003 | 1.4 |
| 65+ | 4,104,648 | 4,154,771 | 1.2 |
| Men, total | 19,523,766 | 20,012,478 | 2.5 |
| Women, total | 20,593,330 | 20,917,970 | 1.6 |

The **2010 census count of 40,117,096** is confirmed.

AD 35 §2.1 (pp. 7-8) also states the same balancing equation explicitly:
> "N(t) = N(0) + B (0,t) – D(0,t) + I (0,t) - E(0,t) ... Población base 2001 +
> Nacimientos período intercensal – Defunciones período intercensal + Inmigrantes
> período intercensal – Emigrantes período intercensal."

### 1.5 CHECK: does 37,156,195 × 1.016, interpolated back to 1 Jan 2001, give 37,530,617?

**Short answer: no — it overshoots by ~31,000 (0.08%). The implied net uplift is
1.52%, not 1.6%.**

Step 1 — interpolate the INDEC (2004) series to 1 January 2001. The published series
is mid-year (30 June). 1 Jan 2001 lies between mid-2000 and mid-2001.

    Linear:     (36,783,859 + 37,156,195) / 2            = 36,970,027
    Geometric:  r = ln(37,156,195 / 36,783,859) = 0.0100711
                t = 184/365 = 0.5068 yr from 30-Jun-2000
                36,783,859 x exp(0.0100711 x 0.5068)     = 36,972,109

Step 2 — apply +1.6%:

    Linear:     36,970,027 x 1.016 = 37,561,547
    Geometric:  36,972,109 x 1.016 = 37,563,662

Step 3 — compare to AD 40 Tabla 3:

    37,561,547 - 37,530,617 = +30,930   (+0.082%)
    37,563,662 - 37,530,617 = +33,045   (+0.088%)

Step 4 — invert to get the *actual* implied factor:

    37,530,617 / 36,970,027 = 1.015163  ->  net uplift +1.5163%
    37,530,617 / 36,972,109 = 1.015106  ->  net uplift +1.5106%

By sex (linear interpolation of the 2004 series to 1 Jan 2001):

    Men:    18,364,239 / 18,111,574.5 = 1.013950  ->  +1.395%
    Women:  19,166,378 / 18,858,452.5 = 1.016328  ->  +1.633%

**Interpretation.** The uplift is *not* uniform by sex — men were raised 1.40% and
women 1.63% — which is inconsistent with a flat +1.6% scaling and consistent with AD
39's description of an age- and sex-specific revision (Beers disaggregation, spline
smoothing of the sex ratio, re-estimated under-15s from re-estimated fertility
including late-registered births, and extinct-generations for 80+). The published
"1,6%" is an *ajuste total* — a summed-absolute measure of how much mass moved — and
the *net* effect on the total is +1.52%. Two further caveats: (a) AD 39 states the
1.6% refers to the **30 June 2001** population, whereas AD 40 Tabla 3 reports **1
January 2001**, so any check must interpolate across that half-year gap; (b) AD 40
§2.1.1 says the *provincial* base was taken from **INDEC (2005)** (the provincial
2001-2015 projections, Serie Análisis Demográfico N° 31), not from AD 30 — so the
national and provincial revisions started from slightly different published vintages.

Note that the mid-year/1-January distinction cannot rescue the discrepancy: because
scaling by a constant commutes with linear interpolation, applying 1.016 at 30 June
2001 (37,156,195 x 1.016 = 37,750,694) and then interpolating back to 1 January returns
the same 37,561,547. The gap is real, and it is the definition of the "1,6%" — gross,
not net — that explains it.

Consistency check on the compounded 2001 omission:

    1.0275 (AD 30 omission) x 1.016 (AD 39 uplift) = 1.04394

i.e. the effective total 2001 census omission implied by the 2025 revision is **~4.4%**,
up from the 2.75% published in 2004. Cross-check from the other direction: growing
37,530,617 from 1 Jan 2001 to the 17 Nov 2001 census date at ~1.0%/yr gives ~37.86m
against a count of 36,260,130, i.e. ~4.4%. The two agree.

---

## 2. DEIS annual live births and deaths, Argentina, 2001-2022

### 2.1 Sources and construction

Two fully independent extractions, which agree **exactly** in every overlapping year:

**(a) Published annual totals.** DEIS, *Estadísticas Vitales - Información Básica*,
Serie 5. One volume per year; the volume number is `year - 1956` (N° 45 = 2001 ...
N° 66 = 2022). National totals read from **Tabla/Cuadro 1**, *"Indicadores de
natalidad, nupcialidad, mortalidad general, infantil y materna por división político
territorial / jurisdicción de residencia"*, row "REPÚBLICA ARGENTINA", columns
"NACIDOS VIVOS" and "DEFUNCIONES TOTALES". All 22 volumes downloaded to `serie5/`.

URL pattern (all verified live): `https://www.argentina.gob.ar/sites/default/files/serie5nro<NN>.pdf`
for N° 45-58 and 60-62; `.../serie5numero<NN>.pdf` for N° 59, 63, 64;
`.../serie_5_nro_65_anuario_vitales_2021_-_web.pdf` (2021);
`.../serie_5_nro_66_anuario_vitales_2022_3.pdf` (2022).
Landing page: https://www.argentina.gob.ar/salud/deis/publicaciones

**(b) DEIS aggregated microdata.** Sum of the `CUENTA` column over the full national
files `nacweb<YY>.csv` and `defweb<YY>.csv`, 2005-2022 (2005-2019 plus `nacweb20_0`,
`nacweb21_0`, `nacweb22_0` and death equivalents), from
https://www.argentina.gob.ar/salud/deis/datos/nacidosvivos and
https://www.argentina.gob.ar/salud/deis/datos/defunciones
Files in `deis/`; summation script `sum.py`. Totals include `PROVRES` codes 98
("otro país") and 99 ("sin especificar"), which is what reproduces the published
national totals.

Result: **(a) and (b) match to the unit for all 18 years 2005-2022.** Years 2001-2004
rest on (a) alone (no microdata CSVs are published before 2005).

### 2.2 The series

Written to **`births_deaths_2001_2022.csv`** (columns: year, births, deaths, source).

| Year | Live births | Deaths |
|---:|---:|---:|
| 2001 | 683,495 | 285,941 |
| 2002 | 694,684 | 291,190 |
| 2003 | 697,952 | 302,064 |
| 2004 | 736,261 | 294,051 |
| 2005 | 712,220 | 293,529 |
| 2006 | 696,451 | 292,313 |
| 2007 | 700,792 | 315,852 |
| 2008 | 746,460 | 302,133 |
| 2009 | 745,336 | 304,525 |
| 2010 | 756,176 | 318,602 |
| 2011 | 758,042 | 319,059 |
| 2012 | 738,318 | 319,539 |
| 2013 | 754,603 | 326,197 |
| 2014 | 777,012 | 325,539 |
| 2015 | 770,040 | 333,407 |
| 2016 | 728,035 | 352,992 |
| 2017 | 704,609 | 341,688 |
| 2018 | 685,394 | 336,823 |
| 2019 | 625,441 | 341,728 |
| 2020 | 533,299 | 376,219 |
| 2021 | 529,794 | 436,799 |
| 2022 | 495,295 | 397,115 |

**Sum 2001-2022 (22 full calendar years): births 15,269,709; deaths 7,207,305.**
Sum 2001-2021 (21 full years): births 14,774,414; deaths 6,810,190.

Incidental but useful: the population denominators printed in Serie 5 Tabla 1 are
INDEC projections of the vintage current at publication. The 2022 volume uses
**46,234,830** (the 2010-census-based projection for 1 July 2022) — 341,977 above the
2022 reconciled figure of 46,122,853 that superseded it.

### 2.3 Occurrence vs registration, and late registrations

This is the single most important caveat on the series above.

DEIS, Serie 5 N° 66 (*Estadísticas vitales - Argentina Año 2022*), section
**"INSCRIPCION TARDIA DE HECHOS VITALES"** (p. 14):

> "Se consideran como 'tardías' a aquellas inscripciones de hechos vitales ocurridos
> **dos o más años antes al año de registro**. Las defunciones de inscripción tardía
> representan un porcentaje ínfimo en la Argentina, **cercano al 1,0 por mil**. A
> partir del año 2006, en consonancia con lo que estipulan los 'Principios y
> Recomendaciones para un Sistema de Estadísticas Vitales' de la División de
> Estadísticas de Naciones Unidas, se tomó la decisión de **excluir de los archivos
> nacionales las defunciones inscriptas tardíamente**.
>
> En el caso de los nacidos vivos, debe tenerse presente que por 'nacidos vivos
> registrados' se entiende y contabiliza a aquellos nacimientos ocurridos tanto en el
> año de registro como a aquellos ocurridos en el año inmediato anterior y registrados
> en el año de referencia."

Restated in the same volume as a table footnote (p. ~26):
> "Se consideran nacidos vivos registrados a los ocurridos en el año de registro y a
> los ocurridos en el año inmediato anterior y registrados en el año de referencia."

**Therefore the series in §2.2 is neither pure year-of-occurrence nor pure
year-of-registration.** It is a hybrid: births occurring in year Y or Y-1 and
registered in Y. Births registered two or more years after occurrence — i.e. exactly
the *nacimientos tardíos* — are **excluded**, and so are late-registered deaths (from
2006 onward, by explicit policy). Year-of-occurrence series are not what DEIS
publishes annually.

DEIS also flags a data-quality wrinkle affecting 2016-2017: after new registration
systems came in, births with unknown date of occurrence jumped from ~100/yr to 659
(2016, La Pampa) and ~2,500 (2017, Buenos Aires); DEIS verified >90% of the Buenos
Aires cases were compatible with timely registration and decided to include them in
the published totals for those years.

### 2.3b Direct proof of the exclusion, and the size of the late-registration flow

DEIS Serie 5 N° 66, **Cuadro 19**, *"Nacidos vivos inscriptos según año de ocurrencia,
por jurisdicción de registro. República Argentina - Año 2022"* (index of tables: p. 59;
printed folio on the page itself: 60), decomposes
every birth *inscribed* during 2022 by the year the birth actually occurred:

| Year of occurrence | Births inscribed in 2022 |
|---|---:|
| **Total inscribed 2022** | **497,001** |
| 2022 | 466,237 |
| 2021 | 29,058 |
| 2020 | 584 |
| 2019 | 176 |
| 2018 | 101 |
| 2017 | 102 |
| 2016 | 101 |
| 2015 | 59 |
| 2014 | 56 |
| 2013 | 45 |
| 2012 | 39 |
| 2011 | 38 |
| Before 2011 | 374 |
| Unspecified | 31 |

The arithmetic settles the question exactly:

    466,237 (occurred 2022) + 29,058 (occurred 2021) = 495,295

which is **precisely the published national total** for 2022 (§2.2). And

    497,001 (all inscriptions) - 495,295 = 1,706
              = 1,675 (occurred 2020 or earlier) + 31 (year unspecified)

**So the series in §2.2 provably excludes late registrations**, and in 2022 that
exclusion removed 1,706 births, or **0.34% of all inscriptions**.

**The same check across years shows the flow was 5x larger a decade ago.** I repeated the
Cuadro 19 extraction for 2013 (Serie 5 N° 57, Tabla 19) and 2015 (N° 59, Cuadro 19):

| Year | Total inscribed | Occurred in ref. year | Occurred prior year | = Published total | Late (≥2 yr), excluded | Late as % of published |
|---|---:|---:|---:|---:|---:|---:|
| 2013 | 766,294 | 704,516 | 50,087 | **754,603** ✓ | 11,691 | **1.55%** |
| 2015 | 782,333 | 709,267 | 60,773 | **770,040** ✓ | 12,293 | **1.60%** |
| 2022 | 497,001 | 466,237 | 29,058 | **495,295** ✓ | 1,706 | **0.34%** |

The identity `occ(Y) + occ(Y-1) = published total` holds **exactly** in all three years,
confirming the definition beyond doubt across a decade.

**How much of the 1.60% → 0.34% fall is real?** Probably most of it. DEIS documents a
genuine collapse in late registration — free DNI at birth from Decreto 262/03 onward,
and by the 2016-2017 study *"más del 95%"* of births registered within three months in
every jurisdiction. The ~1.6%/yr flow observed in 2013-2015 is also consistent in
magnitude with the 2010-census study's finding that late registrations arriving over
2011-2014 accounted for **2.2 percentage points** of a 6% gap.

**But the 2022 figure is still likely understated.** Reading Cuadro 19 by jurisdiction
for 2022, seven jurisdictions — CABA, Buenos Aires, Córdoba, Santa Fe, Chubut, Neuquén
and Santa Cruz — report **exactly zero** late registrations in every year from 2011 back,
while reporting tens of thousands of timely ones. Buenos Aires inscribed 156,298 births
in 2022 and records not one occurring before 2021. In **2015 the same provinces did
report late registrations** — Buenos Aires alone returned 2,491 births occurring before
2005, and CABA, Córdoba and Santa Fe all returned non-zero counts. A fall to exactly
zero across seven jurisdictions at once looks like a change in what is transmitted, not
a change in what happens; and Santa Fe is one of the three provinces the 2016-2017 study
singled out for omission above 10%. In 2022 essentially all recorded late registrations
come from a handful of northern provinces: Chaco 511, Salta 370, Formosa 188, Misiones
163, Santiago del Estero 124, Tucumán 109, Entre Ríos 49, Jujuy 41, San Luis 32, La
Rioja 21 (these ten account for 1,608 of the 1,675).

**Practical implication.** Correcting the §2.2 series for late registration using Cuadro
19 would add ~1.5-1.6% per year in the early 2010s but only ~0.3-0.5% at the end of the
period — and would still miss whatever the non-reporting jurisdictions hold. It recovers
part, not all, of the shortfall the census-anchored studies identify (§2.4).

### 2.4 Published estimates of birth under-registration

Serie 5 N° 66, section **"COBERTURA DE LOS DATOS"** (pp. 15-17), reports two
census-anchored studies. These are the key published magnitudes:

**Against Censo 2001** (multicentre study, DEIS/OPS):
> "La omisión de nacidos vivos que surge de comparar los datos que brinda el Censo
> Nacional de Población y Viviendas 2001 con los nacidos vivos registrados en el
> Subsistema de Estadísticas Vitales es el **6% para el total del país**, si se toman
> como referencia los datos publicados para el mismo año, y **se reduce a menos del
> 3%** si se consideran las inscripciones tardías que se produjeron a lo largo de los
> años 2002 a 2005."

Also from that study:
- Registrations beyond the year of birth (2003), 14 provinces studied: **1.9%**
  (2.2% in the hospitals/departments analysed).
- After the decree making the DNI free at birth: registrations beyond 365 days fell
  from **2.9% (1st half 2003) to 0.8% (2nd half 2003)**.

**Against Censo 2010** (DEIS with UNICEF and CENEP, fieldwork 2016-2017):
> "La omisión de nacidos vivos que surge de comparar los datos que brinda el Censo 2010
> con los nacidos vivos registrados por el Subsistema de Estadísticas Vitales es del
> **6% para el total del país**, si se toman como referencia los datos publicados para
> el mismo año, y **se reduce al 3,8%** si se consideran las inscripciones tardías que
> se produjeron a lo largo de los años 2011 a 2014."
> "Sin embargo, las diferencias entre los valores provinciales son elevadas, provincias
> como **Santiago del Estero, Santa Fe y Tierra del Fuego tienen valores por encima de
> 10%**."
> "Dentro de los 3 meses de acaecido el nacimiento, en todas las jurisdicciones se
> observa que más del **95%** de ellos fueron registrados."
> Hospital fieldwork omission/late-registration rates: **Buenos Aires 5.3%,
> Santa Fe 2.1%, La Rioja 0.6%**.

A third study (2010-2012, DEIS/UNICEF, CABA + Conurbano Bonaerense + Gran Rosario)
found *"en los establecimientos relevados en el estudio la cobertura de registro de
nacimientos es cercana al 100%"*, with residual problems attributed to data quality
rather than coverage.

Cited source document for the earlier study, per Serie 5 N° 66:
> MINISTERIO DE SALUD Y DESARROLLO SOCIAL – ORGANIZACIÓN PANAMERICANA DE LA SALUD,
> *"Omisión de registro de nacimientos y muertes infantiles. Magnitud, desigualdades y
> causas."*, ISBN 978-950-710-110-6, Ciudad Autónoma de Buenos Aires, marzo 2008.

**Bottom line for the identity.** The published DEIS annual births series is short of
census-implied births by ~6% on published figures, or **~3-3.8%** once late registrations
arriving over the following four years are credited (3.0% against the 2001 census, 3.8%
against 2010). Late-registered *deaths* are negligible (~1 per 1,000) and excluded by
policy from 2006.

Two important qualifications, developed in §2.4b and §2.4c. First, **the shortfall is
provincial, not national in character**: only 8 of 24 jurisdictions show a statistically
significant omission against the 2010 census, five show *over*-registration, and the
deficit concentrates in Santiago del Estero (13.0%), Santa Fe (11.1%) and Tierra del
Fuego (10.1%). Second, **every external assessment of Argentine registration
completeness is far more favourable** than these census-comparison figures — UNSD codes
Argentina "C" (≥90%), MICS 2019-2020 puts birth registration at 99.7%, and independent
death-distribution estimates put death completeness at 100-105%. The census-comparison
gap depends on accepting the census *fecundidad actual* question as the truth, which the
2008 report itself flags (*"siempre que se acepte como válida la información censal sobre
fecundidad actual"*). Treat 3-4% as an upper bound on the national birth deficit, not a
settled value.

### 2.4b The primary reports, and the provincial omission tables

The two studies summarised in Serie 5 N° 66 were traced to their primary reports. **I did
not personally re-extract these two documents** (they were retrieved in a parallel
research pass); the figures below are reproduced from them and, where checkable, verified
arithmetically — noted at each point.

**Study 1 — the 2001-census study.** Fernández MM, Guevel C, Krupitzki H, Marconi É,
Massa C, *"Omisión de registro de nacimientos y muertes infantiles. Magnitud,
desigualdades y causas"*, 1a ed., Buenos Aires: OPS – Ministerio de Salud, 2008, 196 pp.,
ISBN 978-950-710-110-6. Working PDF:
https://iin.oea.org/boletines/boletin6/publicaciones-recibidas-ing/OPS-Omision-de-registro.pdf

Method (p. 31): direct record-matching (*pareo*), **not** capture-recapture —
*"registros hospitalarios (libros de partos, libros de defunciones, libros de morgue,
historias clínicas, etc.), registros civiles … y documentación estadística (Informe
Estadístico de Nacido Vivo e Informe Estadístico de Defunción). Se trata de un método
directo de evaluación del grado de cobertura del registro civil…"* — plus two
census-based comparisons using the 2001 census *fecundidad actual* question.

National result (Cuadro 1, p. 39; text p. 40):
> "la omisión de nacimientos en las Estadísticas Vitales del 'año 2001' se ubicaría entre
> el **-6,1 (Omisión A)** y **-3,0 % (Omisión B)** para el Total del País, siempre que se
> acepte como válida la información censal sobre fecundidad actual."

Omisión A = vs births as published for 2001; Omisión B = vs births occurring in 2001 and
registered 2001-2005, i.e. crediting late registrations. A third method (Cuadro 2, p. 45,
population aged 0) gave **-0.7%** nationally. Selected provinces, Omisión B: **Santiago
del Estero -17.7%**, Córdoba -11.1, Corrientes -8.4, La Rioja -5.3, Santa Fe -5.2,
Catamarca -5.2, Entre Ríos -5.1, Tucumán -4.9, Salta -3.8, Buenos Aires -2.5; CABA
**+12.0** (over-registration, i.e. births to non-resident mothers registered in CABA).

Hospital record-matching, births not registered one year after birth — **1999 → 2003**
(pp. 126-129): Chaco 38% → 21%; Formosa 20% → 3%; La Rioja 27% → 10%; Salta 16% → 7%;
Santiago del Estero 38% → 20%; Tucumán 38% → 15%. Infant deaths: Salta 1.5% → 0.0%;
Formosa 5.0% → 2.0%; La Rioja 16.9% → 9.3%; Chaco 6.6% → 5.9%; Tucumán 8.0% → 12.3%;
**Santiago del Estero 71.8% → 77.6%** (worsening).

**Study 2 — the 2010-census study.** Bomben E. et al., *"Registro de nacimientos en
Argentina"*, Ministerio de Salud (DEIS) / UNICEF / CENEP, 2017. The UNICEF landing page
blocks automated clients; retrievable mirror:
https://web.archive.org/web/20220124132305id_/https://www.unicef.org/argentina/media/751/file/Registro%20de%20nacimientos.pdf

> "…es del 6% para el total del país si se toman como referencia los datos publicados por
> DEIS para el mismo año. Y se reduce al 3,8 % si se consideran las inscripciones tardías
> que se produjeron a lo largo de los años 2011 a 2014. **En términos absolutos se
> trataría de 30 mil niños y niñas.**"

Cuadro 1 (Anexo), full provincial table — births occurring in 2010:

| Jurisdicción | Reg. in 2010 | Reg. 2011-14 | Total (a) | Census est. (b) | Omission (b−a)/b | Sig. 95% |
|---|---:|---:|---:|---:|---:|:--:|
| **TOTAL PAÍS** | 756,731 | 16,304 | **773,035** | **803,669** | **3.8%** | Sí |
| CABA | 45,509 | 234 | 45,743 | 40,936 | −10.7% | Sí |
| Buenos Aires | 290,781 | 8,157 | 298,938 | 317,502 | 6.0% | Sí |
| Catamarca | 6,861 | 70 | 6,931 | 7,584 | 9.2% | Sí |
| Córdoba | 58,621 | 1,005 | 59,626 | 60,672 | 1.6% | No |
| Corrientes | 20,440 | 87 | 20,527 | 21,581 | 4.9% | Sí |
| Chaco | 22,826 | 1,156 | 23,982 | 23,916 | −0.5% | No |
| Chubut | 10,104 | 80 | 10,184 | 10,816 | 6.0% | No |
| Entre Ríos | 22,068 | 179 | 22,247 | 23,056 | 3.4% | No |
| Formosa | 11,718 | 242 | 11,960 | 11,745 | −2.0% | No |
| Jujuy | 13,353 | 518 | 13,871 | 13,793 | −0.7% | No |
| La Pampa | 5,528 | 12 | 5,540 | 5,526 | −0.4% | No |
| La Rioja | 6,111 | 75 | 6,186 | 6,622 | 6.9% | No |
| Mendoza | 34,185 | 630 | 34,815 | 34,833 | −0.1% | No |
| Misiones | 24,780 | 510 | 25,290 | 27,147 | 7.1% | Sí |
| Neuquén | 11,934 | 241 | 12,175 | 11,507 | −5.7% | No |
| Río Negro | 11,925 | 168 | 12,093 | 12,092 | −0.2% | No |
| Salta | 27,999 | 979 | 28,978 | 30,626 | 5.5% | Sí |
| San Juan | 14,234 | 203 | 14,437 | 14,542 | 0.5% | No |
| San Luis | 7,921 | 75 | 7,996 | 8,274 | 3.3% | No |
| Santa Cruz | 6,014 | 95 | 6,109 | 6,210 | 1.5% | No |
| **Santa Fe** | 53,483 | 321 | 53,804 | 59,895 | **11.1%** | Sí |
| **Sgo. del Estero** | 17,691 | 546 | 18,237 | 20,647 | **13.0%** | Sí |
| Tucumán | 30,137 | 716 | 30,853 | 31,376 | 1.5% | No |
| **Tierra del Fuego** | 2,508 | 5 | 2,513 | 2,771 | **10.1%** | No |

**Arithmetic verified by me:** all 24 provincial rows satisfy
`Reg.2010 + Reg.2011-14 = Total (a)`; the columns sum to exactly 773,035 and 803,669; and
803,669 − 773,035 = **30,634**, matching the report's "30 mil niños y niñas" and the 3.81%
headline. **One correction:** the total-row "Reg. in 2010" value is sometimes transcribed
as 758,398; the column actually sums to **756,731**, and that is what is shown above.
Note that only **8 of 24** jurisdictions have a statistically significant omission at 95%,
and five jurisdictions show *negative* omission (over-registration relative to the census
estimate), CABA most strongly at −10.7% — the mirror image of mothers travelling to CABA
to give birth.

Also in that report: SEV vs RENAPER for 2014 births showed **−2.4%** (766,096 of 784,506
registered children had obtained a DNI).

### 2.4c External assessments of registration completeness

These matter because they are the benchmark a reviewer will reach for, and they run
**against** a story of large national under-registration.

| Source | Measure for Argentina | Value |
|---|---|---|
| UN Demographic Yearbook 2024, Tables 9/15/18 | completeness code for live births, deaths, infant deaths | **"C"** = *"estimated to be virtually complete, that is, representing at least 90 per cent"* |
| UNSD CRVS completeness table (Apr 2023) | births / deaths | births **90-99%** (2010); deaths **≥90%** (2008) |
| PAHO Core Indicators, ind. 224 *Subregistro de mortalidad (%)* | death under-registration | 2012 = 2.55; 2013 = 2.40; 2014 = 0.85; 2018 = 0.53; 2019 = 1.02; 2020 = 1.48; **2021 = 0.87** |
| PAHO *Indicadores Básicos 2016* | subregistro de mortalidad (~2014) | **1.0%** (ill-defined causes 7.1%) |
| Mathers et al. 2005, *Bull WHO* 83(3), Table 2 | completeness / coverage / ill-defined / quality | **100 / 100 / 22% / "Low"** — the "Low" is driven entirely by ill-defined causes, not completeness |
| WHO GHE 2000-2016, Annex Table D | completeness / usability (2015) | **100 / 67** |
| World Bank SP.REG.BRTH.ZS (UNICEF MICS) | birth registration | 2004 = 91; 2012 = 99.5; **2020 = 99.7** (MICS6, n = 6,157) |
| World Bank SP.REG.DTHS.ZS | death registration with cause | 2011 = 100; **2016 = 100** |
| Sacco N. (2016), *Población y Salud en Mesoamérica* 14(1), DOI 10.15517/psm.v14i1.25306 | death-distribution methods, intercensal 2001-2010, ages 5-84 | GGB **105% (m) / 104% (f)**; SEG (Bennett-Horiuchi) **100% both sexes** |
| Karlinsky (2024), *Demographic Research* 50(38) | `death_comp` | 2015 = 100; 2017 = 99.91; 2018 = 98.97; 2019 = 98.59 |
| CEPAL/CELADE ST/ECLA/CONF.19/L.3 (1964), Recchini de Lattes | birth omission 1942-60 | **0.9% national** (Tierra del Fuego 6.8%, La Rioja 3.4%) |

**Reading.** Death registration is the *weakest* place to argue incompleteness: every
external assessment puts Argentina at or near 100%, and Sacco's death-distribution
estimates actually exceed 100%. What *is* documented for mortality is narrower and
specific: fetal deaths (*"poseen un subregistro importante"*), infant deaths in Santiago
del Estero, **maternal deaths (14.2% omission in 2014**, Serie 5 N° 67 p. 18), and
cause-of-death coding quality (22% ill-defined in 2003; ~24.6% garbage codes in 2021).
Coding quality is a different claim from completeness and must not be conflated with it.

For births the picture is the same shape: high national completeness (MICS 2019-2020 puts
birth registration at 99.7%), with the real deficit concentrated in a few provinces and,
historically, in late registration.

### 2.5 What INDEC actually fed into the equation (and it is not §2.2)

AD 39 makes clear that it did **not** use the published DEIS annual totals as-is:

- **Deaths** (AD 39, §4.1, p. 20):
  > "Para la conciliación se utilizaron las defunciones por **sexo, edad y año de
  > ocurrencia**, con un **ajuste en la mortalidad infantil** en determinados años y
  > provincias, como se ha descripto en INDEC (2025b)."
- **Births — late registrations are explicitly added back** (AD 39, §2.4.1.2, p. 13,
  listing the inputs):
  > "Nacimientos por sexo del nacido vivo, edad y lugar de residencia de la madre según
  > año de ocurrencia (**incluyen los nacimientos anotados como "tardíos"**)⁹."

  with footnote 9 (p. 14) giving exactly the DEIS definition of §2.3:
  > "Se define nacimiento con registro oportuno al ocurrido en el año de registro o al
  > ocurrido en el año inmediato anterior y registrado en el año de referencia. Todos los
  > nacimientos que se registran posteriormente a los dos años o más de la fecha de
  > ocurrencia se consideran tardíos."

  So INDEC's births are, at minimum, the §2.2 series **plus** the Cuadro 19 late
  registrations of §2.3b — a difference of ~1.6%/yr in the early 2010s falling to
  ~0.3-0.5%/yr at the end of the period.
- **Fertility further corrected in six provinces, and the size IS published** (AD 40,
  §4.1, p. 19). This is the one place any correction magnitude is quantified:
  > "La información básica de nacimientos totales se reconstruyó mediante la incorporación
  > de los registros tardíos de nacimientos. … En particular, en algunas provincias se
  > ajustó el nivel de la fecundidad para el período 2001-2022 … Para ello se utilizó un
  > factor de corrección que surge del cociente entre el nivel de la tasa global de
  > fecundidad (TGF) estimado a partir del método de sobrevivencia inversa y el estimado
  > con datos de las estadísticas vitales. **Las jurisdicciones que se ajustaron fueron
  > Chaco, Corrientes, Formosa, Jujuy, Misiones y Santiago del Estero. El impacto de la
  > corrección en la TGF del total del país es inferior a 2% en el 2001, que lo hace el
  > año de mayor ajuste.**"
- **The 2001 base under-15s** (AD 39, §3.1.1, p. 16):
  > "También se ajustó la cantidad de menores de 15 años a partir de la reestimación de
  > la fecundidad en años previos, considerando la **nueva información (nacimientos
  > tardíos)** y estimaciones indirectas del nivel de la fecundidad."
- **Provenance** (AD 39, §2, p. ~10): the vital records used cover **1991-2022** and
  come from *"bases de datos provistas por la Dirección de Estadísticas e Información
  en Salud (DEIS) del Ministerio de Salud de la Nación"* — i.e. supplied databases,
  not (only) the published annuals. AD 39's bibliography nonetheless lists exactly the
  volumes used in §2.2 above:
  > "Dirección de Estadísticas e Información en Salud (DEIS) (1993-2023). Estadísticas
  > Vitales. Información Básica. **Años 1991 a 2022 (Serie 5 N° 35-66)**."

  So the *published* series INDEC cites is the same one reconstructed in §2.2
  (N° 45-66 = 2001-2022); the corrections were applied on top of supplied microdata.

**The corrected annual series themselves are still not published.** AD 39 contains
13 tables (list of tables, pp. 163-203 of the text extraction); none is a table of
annual births or deaths counts. What it publishes are *derived* quantities: life
expectancy at birth by sex for each year 2001-2022 (Tabla 5), total fertility rate,
and the migration aggregates (Tabla 11). The underlying corrected B and D series, and
the size of the correction, are not released in AD 39 or AD 40.

---

## 3. The implied identity, computed

### 3.1 Timing

    1 Jan 2001 -> 18 May 2022 = 7,807 days = 21.3744 years (365.25 d/yr)

The 2022 calendar year is only partly covered: 1 Jan 2022 -> 18 May 2022 = **137 days**,
i.e. **137/365 = 0.3753** of the year. The 2022 births and deaths must be prorated by
that factor (this assumes events are uniform within the year, which for births is a
mild approximation and for deaths understates the share slightly, since Argentine
deaths peak in the southern winter, June-August — so the true share of 2022 deaths
falling before 18 May is a little *below* 0.3753, if anything).

### 3.2 The computation (raw DEIS registration counts)

    Base (AD 40 Tabla 3)                      37,530,617
    + births 2001-2021                      + 14,774,414
    + 0.3753 x 495,295 (2022)               +    185,905
    - deaths 2001-2021                      -  6,810,190
    - 0.3753 x 397,115 (2022)               -    149,054
    + net migration 2001-2022 (AD 39 T.11)  +    375,802
                                            ------------
                                     TOTAL  = 45,907,494

    INDEC's published figure                  46,122,853
                                            ------------
    RESIDUAL (unexplained shortfall)         +   215,359   (+0.47% of the total)

Variants, for transparency:

| Treatment of 2022 | Identity result | Residual vs 46,122,853 |
|---|---:|---:|
| A. All 22 calendar years in full | 45,968,823 | +154,030 (+0.33%) |
| **B. 21 full years + 0.3753 x 2022** (correct) | **45,907,494** | **+215,359 (+0.47%)** |
| C. 21 full years only (2001-2021) | 45,870,643 | +252,210 (+0.55%) |

Script: `calc.py`; sensitivity: `sens.py`.

### 3.3 What the residual means — the important result

The residual of +215,359 is **1.44% of the prorated birth total** and 3.09% of the
prorated death total. Uplifting births alone by 1.44% (leaving deaths and migration
untouched) closes it exactly.

But the more revealing comparison is against the **census count**, not the reconciled
estimate:

    Identity with raw DEIS counts            45,907,494
    Censo 2022 definitive count (AD 39 T.1)  45,892,285
                                            ------------
    Difference                                  +15,209   (+0.03%)

**The balancing equation, fed entirely with uncorrected DEIS registration counts and
INDEC's own published base and migration figures, reproduces the 2022 census count to
within 0.03% — about fifteen thousand people out of forty-six million.** The whole of
INDEC's claimed 2022 census under-count (46,122,853 - 45,892,285 = **230,568**, the
"-0.5%" of AD 39 Tabla 4) is therefore generated by INDEC's *upward corrections to the
components* — chiefly the late-registered births folded into the fertility
re-estimation, plus the infant-mortality adjustment — and not by anything visible in
the published registration data.

**Two caveats that stop this being over-read.** First, the computation is *not* a
pure "uncorrected" reconstruction: it uses INDEC's **corrected** 2001 base
(37,530,617), which already embeds the +1.52% revision, alongside uncorrected flows.
Substituting the original INDEC (2004) base interpolated to 1 Jan 2001 (36,970,027) and
holding the raw flows fixed gives

    36,970,027 + 8,376,877 (net raw flows) = 45,346,904

which falls **545,381 below** the census count and 775,949 below the reconciled
estimate. So the near-agreement in the box above depends entirely on INDEC's 2001 base
revision being accepted; the base revision contributes 560,590 of the total. Second,
the agreement is to some degree a coincidence of offsetting errors — under-counted
births pushing down, an unadjusted infant-mortality series and the whole
under-registration of deaths pushing the death total down too, and migration modelled
rather than counted. The right reading is not "the raw data prove the census was
right", but "the published inputs cannot distinguish between the census count and
INDEC's reconciled estimate, because the corrections that separate them are exactly the
ones INDEC did not publish."

**The 1.44% needed is strikingly close to the one correction magnitude INDEC does
publish.** AD 40 §4.1 (p. 19) states that its provincial fertility correction — applied
in Chaco, Corrientes, Formosa, Jujuy, Misiones and Santiago del Estero — had a national
TGF impact *"inferior a 2% en el 2001, que lo hace el año de mayor ajuste"*, i.e. under
2% at the maximum and smaller in every later year. Adding the Cuadro 19 late
registrations on top (~1.6%/yr in the early 2010s, ~0.3-0.5%/yr by 2022, §2.3b), INDEC's
total upward correction to births plausibly averages somewhere near 1.5% over the
period. That is the 1.44% the residual requires. The identity is therefore **internally
consistent with INDEC's published description of its own method**, even though the
corrected series are withheld.

By contrast, the *census-anchored* omission estimates (§2.4) are larger: 3.8% against
the 2010 census after crediting late registrations. A uniform 3.8% birth uplift would
overshoot 46,122,853 by ~353,000. So INDEC did **not** apply the full census-implied
omission to births nationally — consistent with its own account, which restricts the
fertility correction to six provinces and caps the national effect below 2%. Offsetting
adjustments elsewhere (the sex-ratio smoothing lowered the male base; the
infant-mortality adjustment raises deaths) absorb the rest. Beyond this the
decomposition cannot be pushed with public data.

### 3.4 Which inputs are uncorrected, explicitly

| Input | Status |
|---|---|
| 37,530,617 (1 Jan 2001 base) | **INDEC's corrected figure**, published (AD 40 Tabla 3). Its derivation from INDEC (2004)/(2005) is described but the age-sex correction vector is published only as a graph (AD 39 gráfico 4), not as numbers. |
| Births 2001-2022 (§2.2) | **Uncorrected registration counts** (DEIS published "nacidos vivos registrados"; excludes late registrations 2+ years out). NOT what INDEC used — AD 39 §2.4.1.2 says its births "incluyen los nacimientos anotados como 'tardíos'", and AD 40 §4.1 adds a fertility correction in six provinces. |
| Deaths 2001-2022 (§2.2) | **Uncorrected registration counts** (excludes late-registered deaths from 2006 by policy; no infant-mortality adjustment). NOT what INDEC used. |
| +375,802 net migration | **INDEC's estimate**, published (AD 39 Tabla 11), itself modelled from census "año de llegada" / "residencia 5 años antes" plus foreign registers, not an administrative flow count. Its own components do not sum to the published total (see §0). |
| 46,122,853 | **INDEC's reconciled result**, published (AD 39 Tabla 4). |

**INDEC's corrected births and deaths series are not published.** They exist (AD 39
§4.1 refers to annual life tables built from them for 2001-2022) but neither AD 39 nor
AD 40 contains them, and no accompanying data annex releasing them was located (§6
item 1 documents the annex check). The residual in §3.2 is therefore *not* reproducible
to zero from published sources, and the +215,359 gap should be read as "the aggregate
size of INDEC's unpublished component corrections", not as an error in either INDEC's or
DEIS's work.

**What is published is enough to bound them.** Two of the three corrections are described
with a magnitude: late registrations are added back in full (measurable from Cuadro 19 —
~1.6%/yr early in the period, ~0.3-0.5%/yr at the end, §2.3b), and the extra provincial
fertility correction is capped at *"inferior a 2%"* on the national TGF in 2001 and
smaller thereafter (AD 40 §4.1). Only the infant-mortality adjustment is wholly
unquantified. Those bounds are consistent with the 1.44% uniform birth uplift that closes
the residual — see §3.3.

---

## 4. Administrative totals for 2022 (plausibility comparison only)

These are **not** inputs to the identity. They are order-of-magnitude cross-checks, and
every one of them counts a different universe from "resident population on 18 May 2022".

### 4.0 INDEC used two of these itself

This is the most important finding in this section. AD 39 §2.4.1.3, *"Otros registros
administrativos nacionales"* (p. 14), names its registry inputs verbatim:

> "**Registro Nacional de las Personas (Renaper)**: base de personas documentadas de
> acuerdo con el registro administrativo del organismo por provincia de residencia,
> sexo, edad y país de nacimiento **al mes de mayo de 2022**."
>
> "**Base de datos Vacunas COVID-19** (Ministerio de Salud de la Nación): base de datos
> nominalizada correspondiente a las vacunas COVID-19 por orden de dosis, sexo, rango de
> edad, provincia de aplicación, provincia de residencia y fecha de aplicación. A partir
> de ella **se seleccionan las personas por edad y sexo que hayan recibido al menos una
> dosis de la vacuna al 18 de mayo 2022**."

And earlier (§2.4.1, p. 13):
> "Los registros administrativos se utilizaron tanto en la etapa de evaluación de los
> datos censales como en la conciliación censal. También se emplearon para la
> comparación entre distintas fuentes de agregados de población y de las estructuras por
> sexo y edad."

Other registries named (AD 39, p. 8 and §2.4.1.3): school enrolment (Relevamiento Anual
Educativo, April 2022), the ARCA (ex-AFIP) padrón, SIPA social-security records, ANSES
special processings, and Migraciones entry/exit records 2010-2022.

**INDEC therefore already benchmarked the census against RENAPER and the vaccination
registry, at the exact census date, and published neither the registry totals nor the
gap.** What it published is the outcome: the -0.5% net differential of Tabla 4. Any
external registry-vs-census comparison is, in effect, re-running an exercise INDEC did
internally and did not disclose.

### 4.1 RENAPER — persons with digital DNI resident in Argentina

**No published national headline total exists.** RENAPER's Sistema Estadístico de
Población (https://estadisticas.renaper.gob.ar/app_poblacion/) renders the total over a
websocket in a Shiny app, so it is neither crawlable nor archived, and no DNP report or
press release states it. Only the disaggregated open data is published, at
https://datos.gob.ar/dataset/renaper-estructura-de-poblacion-argentina (files served
from https://datosabiertos.renaper.gob.ar/).

Totals below are **sums computed from those official files — derived, not published.
Label them as such in any citation.**

| Reference date | Total "población identificada" | File |
|---|---:|---|
| January 2023 | 46,897,335 | `poblacion_identificada_provincia_enero_2023.csv` |
| August 2023 | 47,121,321 | `poblacion_identificada_departamento_agosto_2023.csv` |
| August 2024 | 46,888,798 | `poblacion_identificada_provincia_agosto_2024.csv` |
| January 2025 | 47,010,761 | `poblacion_identificada_provincia_enero_2025.csv` |
| June 2025 | 46,735,004 | `poblacion_identificada_provincia_junio_2025.csv` |

Caveats, which are severe:
- The 2023 files have been **removed from the live portal** (only Aug-2024 onward are
  listed today) and were recovered from the Internet Archive.
- The Aug-2023 departmental file is a **broken export**: every logical row is duplicated
  (84,497 rows → 50,251 unique keys); naive summation gives 106,199,987. The figure above
  is post-deduplication and should be trusted less than the Jan-2023 one.
- **Universe** (DNP methodology, *Caracterización de la migración internacional en
  Argentina a partir de los registros administrativos del RENAPER*, Nov 2022, pp. 5-6):
  *"Personas identificadas con DNI con proceso digital (Decreto N°1501/2009), libreta
  celeste o tarjeta… y que residen en el país"*. It **excludes** holders of the old
  manual documents — *"quedan afuera todas aquellas personas que cuentan con versiones
  confeccionadas manualmente (Libreta Cívica, Libreta de Enrolamiento y DNI tapa verde o
  bordo)"* — a downward bias concentrated in the oldest cohorts.
- Non-residents are purged using Migraciones data (absent >6 months), so Argentines
  abroad are excluded — the opposite convention from the electoral roll.
- Deceased persons are meant to be purged, but only as fast as death registration reaches
  RENAPER. **No published quantification of the un-purged residual was found.**
- Note that the nearest RENAPER total (Jan 2023, 46.90m) sits **~780,000 above** INDEC's
  reconciled 46,122,853 for eight months earlier. Given the caveats above this is not
  evidence of census undercount; it is what a cumulative identity register looks like.
- One genuinely published RENAPER headline, for contrast: **3,033,786** foreign-born
  persons with digital DNI resident in Argentina, **August 2022** (same report, p. 15:
  *"1.568.350 son mujeres y 1.465.430 varones (solo 6 personas tienen su DNI con género
  no binario)"*). Do not compare this with the later `poblacion_extranjera_*` files,
  which count foreign *nationality* (2,470,453 in Aug 2024), a different universe.

### 4.2 Padrón electoral 2023

Source: Cámara Nacional Electoral, "Total de electores por distrito",
https://www.electoral.gob.ar/nuevo/paginas/datos/total_electores_2023.php
(zip: `.../total_electores_2023.zip`; file `Totales Padron 2023 21OCT23.xlsx`, sheet
`Hoja1`; sheet `referencias` states *"Actualizado: 21/10/2023 (12hs)"* and
*"La cantidad de electores no incluye electores agregados ni tachas"*).

| | Electors |
|---|---:|
| In-country (24 districts) | **35,394,425** |
| Argentines abroad | 449,909 |
| **Total general** | **35,844,334** |

By age group, from `PASO 2023 Electores por genero y edad 2023.xlsx` in the same zip
(domestic roll only; groups sum exactly to 35,394,425):

- **16-17 year olds (clases 2006-2007): 1,045,034** (clase 2006 = 615,232;
  clase 2007 = 429,802, partial because eligibility requires turning 16 by election day)
- 1994-2005: 8,453,534 · 1984-1993: 6,843,691 · 1974-1983: 6,312,001 ·
  1964-1973: 4,699,872 · 1954-1963: 3,808,648 · 1953 and earlier: 4,228,201 · S/D: 3,444
- By gender: F 18,005,180 · M 17,388,170 · X 1,075

Caveats: electors ≠ population (excludes under-16s and resident foreign nationals, who
vote only in some sub-national elections; *includes* ~450k Argentines abroad). The roll
is built from RENAPER with a ~180-day cut-off, so post-cut-off deaths remain. The
*provisional* roll (5 May 2023) was 35,815,436, i.e. ~421k above the definitive one
after depuration — a useful indication of churn magnitude. A figure of 35,463,946 that
circulates in press (La Nación Data) equals 35,394,425 + 69,520 *privados de la
libertad*, who sit on a separate roll excluded from the CNE headline.

### 4.3 COVID-19 vaccination — persons with at least one dose

**No official figure for exactly 18 May 2022 is published in retrievable form.** The
Monitor Público de Vacunación was an embedded Grafana dashboard whose values were never
captured as text by the Wayback Machine, and the surviving open-data aggregate
(`Covid19VacunasAgrupadas.csv`) carries no date dimension.

What is published: Ministerio de Salud press releases quoting the Monitor, each using
the wording *"X personas iniciaron su esquema y Y lo completaron"* — **persons, not
doses**:

| Date | Persons with ≥1 dose | Schedule complete | Doses applied |
|---|---:|---:|---:|
| 23 Apr 2022 | **40,695,477** | 37,186,671 | 98,129,937 |
| **27 May 2022** | **40,779,344** | 37,446,810 | 102,161,920 |
| 6 Jun 2022 | 40,802,733 | 37,503,794 | 103,507,017 |
| 17 Jun 2022 | 40,824,848 | 37,559,032 | 104,879,079 |

URLs: 23 Apr — https://www.argentina.gob.ar/noticias/argentina-recibio-mas-de-dos-millones-de-vacunas-de-moderna ;
27 May — https://www.argentina.gob.ar/noticias/llego-hoy-al-pais-un-cargamento-con-1681500-vacunas-de-moderna ;
6 Jun — https://www.argentina.gob.ar/noticias/argentina-recibio-el-sabado-318000-vacunas-de-moderna ;
17 Jun — https://www.argentina.gob.ar/noticias/salud-distribuyo-741340-vacunas-de-moderna-todo-el-pais

**The census-date value is therefore bracketed: 40,695,477 (23 Apr) to 40,779,344
(27 May) — about 40.75 million. Cite the bracket, not an interpolated point.**

Do **not** substitute Our World in Data, which gives `people_vaccinated` = 41,154,134 on
2022-05-18 (https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/country_data/Argentina.csv).
That series is sourced from covidstats.com.ar, not the Ministry, and runs 375-460k
**above** the Ministry's own "esquema iniciado" figures on adjacent dates — probably a
different treatment of single-dose (CanSino) or component-1 records. The two series must
not be mixed.

Caveats: NOMIVAC counts persons vaccinated *in Argentina*, including non-residents and
people who have since died or emigrated; under-3s were ineligible; uptake was voluntary.
It is a lower bound on population, not an estimate of it. Against a reconciled
46,122,853 it implies ~88% of all ages with ≥1 dose, which is unremarkable.

### 4.4 ANSES — AUH coverage, May 2022

Source: ANSES, *Boletín mensual AUH — Junio 2022*,
https://www.anses.gob.ar/sites/default/files/2022-09/Boletin%20mensual%20AUH%20Junio%202022.pdf

| | May 2022 | (Apr 2022) | (Jun 2022) |
|---|---:|---:|---:|
| Beneficiaries (children receiving AUH) | **4,364,669** | 4,369,206 | 4,360,033 |
| Titulares (adults collecting) | **2,473,980** | 2,475,188 | 2,472,440 |

Cuadro 1.1 splits May beneficiaries by sex: 2,142,366 + 2,222,303. Titulares: 2,305,663
women + 168,317 men. Beneficiaries and titulares must not be conflated.

Inconsistency to flag: ANSES's *Informe de Estadísticas de la Seguridad Social — I
Trimestre 2022* headlines 4,397,391 beneficiarios / 2,494,272 titulares / 83,077
titulares AUE. That beneficiary figure matches **January** 2022 in the monthly series,
not March (4,480,811), though secondary summaries attribute it to March. The monthly
bulletin is the better source.

**More useful than AUH itself:** the same bulletin, Cuadro 1.6, *"Población total menor
de 18 años en el Administrador de Datos de Personas (ADP)"* — ANSES's own registry of
under-18s:

| | Under-18s in ADP |
|---|---:|
| April 2022 | 13,170,081 |
| **May 2022** | **13,155,899** |
| June 2022 | 13,139,009 |
| (Dec 2019) | 13,493,330 |

Against the census: 0-14 censused 10,079,357, estimated 10,445,663. The ADP figure is
for under-**18s**, so it is not directly comparable, but it is materially larger than any
census-consistent under-18 total. ADP is a cumulative identity register (deceased,
emigrated and duplicate records not necessarily purged), so it is an upper bound, not a
competing estimate — the same caveat as RENAPER, and the reason INDEC used registries
for *structure* comparison rather than as a level benchmark.

### 4.5 Not found

- **CUIL/CUIT registration totals.** AD 39 names the ARCA padrón as an input but
  publishes no aggregate, and no ARCA/AFIP publication giving a national count was
  located.
- **SISA / PUCO padrón de salud record counts.** PUCO is documented
  (https://sisa.msal.gov.ar/sisadoc/docs/0204/puco_intro.jsp) as covering persons with
  *obra social* only — excluding prepagas and the uninsured — so it could not serve as a
  population denominator even if a total were published. None was.
- **SINTyS totals.** None published.
- **Academic quantification of a registry-vs-census gap for 2022.** No published
  statement by AEPA/Red AEPA, the Grupo de Estudios de Población, or individual
  demographers quantifying such a discrepancy was found. The demographer commentary that
  exists (El Economista, May 2022,
  https://eleconomista.com.ar/actualidad/censo-2022-opinion-demografos-resultados-provisorios-n53357)
  responded to the *preliminary* 47,327,407 figure and ran in the **opposite** direction:
  Victoria Mazzeo raised the possibility of *over*-registration arising from the new
  digital modality. Nicolás Sacco (Penn State) criticised the census design pre-fieldwork
  (https://observatoriocensal.org/2021/11/04/). The AEPA Jornadas 2023/2025 proceedings
  are the likeliest place for a quantified treatment; nothing surfaced in web search.

### 4.6 Summary

| Registry | Figure | Date | Nature |
|---|---:|---|---|
| Census, counted (definitive) | 45,892,285 | 18 May 2022 | published (INDEC) |
| Census, reconciled estimate | 46,122,853 | 18 May 2022 | published (AD 39 Tabla 4) |
| RENAPER identified resident population | 46,897,335 | Jan 2023 | **derived** (sum of official CSV) |
| RENAPER identified resident population | 47,121,321 | Aug 2023 | **derived** (deduplicated) |
| Padrón definitivo, in-country | 35,394,425 | 21 Oct 2023 | published (CNE) |
| Padrón definitivo, incl. abroad | 35,844,334 | 21 Oct 2023 | published (CNE) |
| — of which 16-17 | 1,045,034 | PASO 2023 | published (CNE) |
| Persons with ≥1 COVID dose | 40,695,477 → 40,779,344 | 23 Apr → 27 May 2022 | published (MSal) |
| AUH beneficiaries | 4,364,669 | May 2022 | published (ANSES) |
| AUH titulares | 2,473,980 | May 2022 | published (ANSES) |
| ANSES ADP under-18s | 13,155,899 | May 2022 | published (ANSES) |

Supporting downloads for this section are in `admin/`.


## 5. Files in this directory

| File | What it is |
|---|---|
| `vitals_findings.md` | This document |
| `births_deaths_2001_2022.csv` | **Deliverable.** year, births, deaths, source — 22 rows, 2001-2022 |
| `ad39.pdf` / `.txt` | INDEC Serie Análisis Demográfico N° 39 (2025), national projections 2022-2040 |
| `ad40.pdf` / `.txt` | INDEC Serie Análisis Demográfico N° 40 (2025), jurisdictional projections |
| `ad30_official.pdf`, `proy_1950_2015.pdf` / `.txt` | INDEC AD N° 30 (2004), 1950-2015 — official and mirror, byte-identical |
| `ad35_2010_2040.pdf` / `.txt` | INDEC AD N° 35 (2013), 2010-2040 |
| `censo2022_prov.pdf` / `.txt` | Censo 2022 provisional results |
| `serie5/s5_45..s5_66.pdf` / `.txt` | DEIS Estadísticas Vitales Serie 5, all 22 annuals 2001-2022 |
| `deis/nacweb*.csv`, `deis/defweb*.csv` | DEIS aggregated vital microdata 2005-2022 |
| `deis/descnac.xlsx`, `deis/descdef1.xlsx` | DEIS record layouts for the above |
| `sum.py` | Sums DEIS microdata `CUENTA` by year |
| `calc.py` | Builds the CSV and computes the identity under three timing treatments |
| `sens.py` | Residual sensitivity |
| `annex/` | INDEC's published projection data annexes (c1, c2, c3_6 xlsx + base csv) — checked and found to contain no 2001-2022 births/deaths |
| `admin/` | Downloads supporting §4 (RENAPER CSVs, CNE padrón xlsx, ANSES bulletins) |
| `underreg/` | Downloads supporting §2.4b and §2.4c (2008 MSAL/OPS volume, 2017 DEIS/UNICEF/CENEP report, UNSD/PAHO/WHO tables) |
| `deis/deis_datos.html`, `nacidosvivos.html`, `defunciones.html`, `pubs.html` | Saved DEIS landing pages (link provenance) |

## 6. What could NOT be found

Listed explicitly, as requested. These are genuine gaps, not items I stopped short on.

**Central to the identity:**

1. **INDEC's corrected annual births series 2001-2022.** Not published in AD 39 or AD 40
   (neither contains a table of annual birth counts; AD 39's 13 tables are listed in its
   ToC and none is such a table). AD 39 publishes only derived quantities — total
   fertility rate, life expectancy — from which the counts cannot be inverted without
   the corrected population exposures, which are also unpublished for intercensal years.

   **This was checked against the data annexes, not just the PDFs.** INDEC's projections
   hub (https://censo.gob.ar/index.php/proyecciones/) publishes machine-readable annexes:
   `proyecciones_nacionales_2022_2040_base.csv`, `..._c1.xlsx` (Cuadro 1, population by
   year), `..._c2.xlsx` (Cuadros 2.1-2.3, by age and sex), `..._c3_6.xlsx` (Cuadros 3-6),
   plus jurisdictional equivalents, metadata PDFs, a dossier, and the 2019 and 2020-2022
   life tables. Inspecting their contents:
   - `_c3_6.xlsx` Cuadro 3 gives *rates* only ("Tasa anual de crecimiento total,
     crecimiento vegetativo, natalidad, mortalidad y migración neta") and **only for
     2025, 2030, 2035 and 2040** — projection years, not the 2001-2022 reconciliation
     period. Cuadros 4-6 are projected migration, life expectancy and TFR.
   - `..._base.csv` (Edad; Sexo; Poblacion; Fecha) covers **`Fecha` 2022-2040 only**
     (19 years; 2022 total = 46,135,579, the 1 July 2022 figure, against 46,122,853 at
     the 18 May census date).

   So no annex releases the corrected counts.

1b. **The reconstructed annual intercensal population 2001-2021.** AD 39 states its aim
   in its introductory section (§1, "Introducción"): *"se busca reconstruir anualmente la población nacional por edad y sexo entre
   2001 y 2022"*. That reconstruction is the backbone of the reconciliation, but the
   published series — PDF and annex alike — **begins at 2022**. The intercensal years are
   not released in any form located.
2. **INDEC's corrected annual deaths series 2001-2022.** Same. AD 39 §4.1 confirms these
   exist ("se construyeron tablas de mortalidad nacionales por sexo para cada año
   calendario del período 2001-2022") but publishes only the resulting life expectancies
   (Tabla 5).
3. **The size of the infant-mortality adjustment**, by year and province — still not
   found. AD 40 §3.1 (p. 15) confirms it happened: *"se ajustaron, específicamente, las
   defunciones correspondientes a los menores de 1 año, dada la evidencia de problemas de
   omisión en el registro de esos hechos vitales en algunas provincias"* — but gives no
   magnitude, unlike the fertility correction. AD 39 §4.1 defers to a reference it calls
   **INDEC (2025b)**, which I could not resolve: the in-text citation exists (p. 20) but
   no matching "2025b" entry appears in AD 39's reference list, which carries only an
   unlettered "INDEC (2025). Censo Nacional de Población, Hogares y Viviendas 2022.
   República Argentina. Síntesis de resultados." This looks like an editorial slip.
   **Note that the fertility-correction magnitude, by contrast, IS published** (AD 40
   §4.1, p. 19: six provinces, national TGF impact <2% in 2001) — see §2.5 and §3.3.
4. **The age-sex vector of the +1.6% adjustment to the 2001 base.** AD 39 presents it
   only as gráfico 4 (a chart), never as numbers. This is why the check in §1.5 can be
   done only in aggregate.
5. **A published year-of-occurrence births or deaths series for Argentina.** DEIS
   publishes only the hybrid "registrados" definition (§2.3). Cuadro 19 exists for single
   years but, as §2.3b shows, its late-registration counts are structurally incomplete
   (seven jurisdictions report zero). No DEIS or INDEC publication reconstructs
   occurrence-year totals for 2001-2022.
6. **Reconciliation of AD 39 Tabla 11's internal inconsistency.** The migration
   components (150,805 + 224,849) sum to 375,654, and the body text's alternative
   (224,996) gives 375,801, against a published total of 375,802. No erratum was located.

**On birth under-registration (§2.4):**

7. ~~The full by-province omission table from the 2016-2017 study.~~ **FOUND** — see the
   new §2.4b. Both the 2001-census and 2010-census provincial tables were located in the
   primary reports.
8. **The brief's "Serie 8 / Serie 10" lead is a dead end.** The 2008 omission study is a
   standalone ISBN volume (MSAL/OPS), not part of a numbered DEIS Serie; only the annual
   yearbooks are Serie 5. Its full text was obtained — see §2.4b.

**Method notes / minor:**

9. **INDEC (2005)**, the provincial base cited by AD 40 §2.1.1 (Serie Análisis
   Demográfico N° 31, provincial projections 2001-2015), was not downloaded; only the
   national AD N° 30 was needed for §1.
10. **Deaths before 2005 could not be cross-validated** against microdata, since DEIS
    publishes aggregated CSVs only from 2005. The 2001-2004 figures rest on the Serie 5
    annuals alone (single-sourced, though these are the official publications and the
    same ones AD 39 cites).

11. ~~Independent assessments of vital-registration completeness.~~ **MOSTLY FOUND** —
    see §2.4c. Still missing: any **IHME/GBD numeric completeness estimate for
    Argentina** (GBD 2019 appendix Table S9 is access-blocked and Argentina is absent
    from secondary reproductions); any **UNSD point percentage** (only the letter code
    "C" and the band "90-99%" are published); and a working source for **Bay & Orellana
    (2007, CEPAL/CELADE)**, commonly cited for the claim that Argentine vital statistics
    are satisfactory.

11b. **Documentation-drive counts.** No official RENAPER or Ministerio del Interior count
    of people newly registered under **Decreto 90/2009** or **Decreto 278/2011** has been
    published; the decrees invoke *"la información estadística sobre los resultados de la
    aplicación del Decreto Nº 90/09"* without releasing it. (Extension chain: 92/2010,
    278/2011, 294/2012, 339/2013, 297/2014, 406/2015, 459/2016, 160/2017, 222/2018,
    185/2019, 285/2020.) The only stock estimates are non-official: UCA Observatorio de la
    Deuda Social + IADEPP, on 2011 data, found **1.6% of children 0-17 born in Argentina,
    in urban Argentina, had no DNI ≈ 168,000 children** (2.3% among 0-4; 2.2% in
    villas vs 1.0% in formal areas) — cited by the Defensoría del Pueblo de la Nación
    (https://dpn.gob.ar/articulo.php?id=31815), which notes these "are the only available
    data, coming from private sources."

    **Terminology correction for the record:** *Ley 26.774* is the 2012 *voto joven* law
    (voting at 16), **not** a documentation law. The relevant statutes are **Ley 26.413/08**
    (Registro Civil) and **Ley 26.061/05 + Decreto 415/06** (free first DNI); the fee-waiver
    chain DEIS credits for the improvement in timely registration is Decretos 262/03,
    832/04, 819/05, then Ley 26.061/05.

12. **No independent count series exists for 2001-2004.** The long historical series
    tables carried in the Serie 5 annuals ("Años 1980-2004", "Años 1990-2022") are
    **rates** — infant mortality, maternal mortality — not counts of births or deaths.
    So the 2001-2004 rows of `births_deaths_2001_2022.csv` cannot be cross-validated
    within the DEIS corpus; they rest on each year's own Tabla 1.
