# RENAPER administrative-register count of the foreign-born population of Argentina

**Audit support note.** Extraction, definitional audit, time series, and reconciliation against the
2022 census.

Primary source under audit:

> Dirección Nacional de Población (DNP), *Caracterización de la migración internacional en Argentina
> a partir de los registros administrativos del RENAPER*. Registro Nacional de las Personas
> (RENAPER), Ministerio del Interior. **Diciembre 2022**, 31 numbered pages.
> PDF used: `https://www.argentina.gob.ar/sites/default/files/2022/12/08_-_caracterizacion_de_la_migracion_internacional.pdf`
> (sha-checked local copy in the session scratchpad; 32 PDF pages, 31 with printed folios).
> Landing page: https://www.argentina.gob.ar/interior/renaper/estadistica-de-poblacion/caracterizacion-de-la-migracion-internacional-en-argentina

**Page-citation convention.** The PDF has an unnumbered cover and an unnumbered authorities page,
after which every page carries a printed folio at the foot. **PDF page = printed folio + 1.**
The report's own *Índice* is off by one against those folios (it lists "Introducción 2" for the page
whose folio reads 3); all citations below use the **printed folio**, with the PDF page in
parentheses. The report's own table of contents should not be used for citation.

Headline figure under audit:

> "La cantidad de personas nacidas en el exterior con DNI con proceso digital y residencia en
> Argentina al mes de agosto de 2022 es de **3.033.786**." — p. 8 (PDF 9), repeated p. 24 (PDF 25)
> and p. 27 (PDF 28).

Counter-figure:

> INDEC, *Censo Nacional de Población, Hogares y Viviendas 2022. Resultados definitivos.
> Migraciones internacionales e internas. Edición ampliada, abril de 2024*: **1.933.463** persons
> in private dwellings born in another country, reference date **18 May 2022**; 1.061.421 women and
> 872.042 men; 4,2% of the population in private dwellings.

---

## 0. Files produced

All in `docs/audit-support/migrants/`.

| File | Content | Provenance |
|---|---|---|
| `renaper_tabla1_pais_de_origen.csv` | Tabla 1 — count and % by country of birth | Transcribed, p. 9 (PDF 10) |
| `renaper_tabla2_region_residencia.csv` | Tabla 2 — % by region of DNI domicile × country | Transcribed, p. 17 (PDF 18) |
| `renaper_sexo_total.csv` | Totals by DNI gender | Narrative, p. 9 (PDF 10) and p. 27 (PDF 28) |
| `renaper_grafico2_piramide_edad_sexo_DIGITALIZADO.csv` | Age × sex structure, 21 five-year groups | **Digitized from the chart image**, Gráfico 2, p. 11 (PDF 12) |
| `renaper_grafico14_15_top20_censo2010_vs_renaper2022.csv` | Top-20 countries, 2010 census vs 2022 register (%) | Data labels read from chart images, Gráficos 14–15, p. 26 (PDF 27) |
| `renaper_grafico13_amba_caba_vs_partidos.csv` | CABA vs 40 AMBA *partidos* split by country | Narrative, pp. 21–22 and 28–29 |
| `renaper_conteos_narrativos_por_pais.csv` | Country counts stated only in prose (Ecuador, China, South America total, 2010 comparators) | pp. 23–25 (PDF 24–26) |
| `renaper_serie_stock_2022_2026.csv` | Stock by country, Aug 2022 → Jun 2026 | RENAPER open data, recomputed here from source CSVs |
| `renaper_vs_censo2022_por_pais.csv` | Register vs census by country, raw and adjusted | Derived |
| `renaper_vs_censo2022_estructura_por_edad.csv` | Register vs census by five-year age group | Derived |
| `renaper_reconciliacion_factores.csv` | The quantification table of §4 | Derived |

Companion census extractions (`census2022_*.csv`) in the same directory were produced by a parallel
workstream and are used here as the census-side input.

---

## 1. Every table in the report

### 1.1 What the report actually publishes

**The report contains exactly two numeric tables.** Everything else is a chart image. Specifically:

| Exhibit | Folio (PDF) | Numeric table? |
|---|---|---|
| Tabla 1 — count and % by country of birth | 9 (10) | **Yes** |
| Tabla 2 — % by region of DNI domicile × country | 17 (18) | **Yes** |
| Gráfico 1 — femininity index by five-year age group | 10 (11) | No — raster image, no data labels |
| Gráfico 2 — population pyramid, all foreign-born | 11 (12) | No — raster image, no data labels |
| Gráficos 3–12 — pyramids for 10 individual countries | 13–15 (14–16) | No — raster images, no data labels |
| Mapas 1–8 — % by jurisdiction, 8 countries | 18–21 (19–22) | No — raster choropleths, no printed values |
| Gráfico 13 — CABA vs AMBA *partidos* by country | 22 (23) | No — raster image; some values given in prose |
| Gráficos 14–15 — top-20 countries, 2010 census and 2022 register | 26 (27) | No — **but the bars carry printed data labels**, which are recoverable |

Consequences for the brief as written:

- **There is no table by sex.** The sex totals appear only as a sentence.
- **There is no table by age group.** Only pyramids as images. The age distribution in
  `renaper_grafico2_piramide_edad_sexo_DIGITALIZADO.csv` was **recovered by pixel measurement**
  (see §1.5); it is not published by the DNP.
- **There is no table by province of residence.** Tabla 2 is at *region* level only (six regions),
  and only as row percentages, with no counts. The eight maps are the only province-level exhibit
  and carry no legible values.
- **There is no table by year of DNI issue and no table by year of arrival.** The report does not
  report either variable anywhere. The DNP's *previous* report (2021) covers residence-permit flows
  instead; see §3.4.

### 1.2 Tabla 1 — country of birth, August 2022

Source line, verbatim: *"Elaborado por la DNP a partir de las personas vivas con DNI con proceso
digital (Decreto N°1501/2009), libreta celeste o tarjeta, residentes en Argentina y nacidas en el
exterior al mes de agosto del 2022 de la Base de Datos del RENAPER."*

| País de origen | Cantidad | Porcentaje |
|---|---:|---:|
| Paraguay | 900.238 | 29,67 |
| Bolivia | 658.559 | 21,71 |
| Perú | 289.430 | 9,54 |
| Venezuela | 220.595 | 7,27 |
| Chile | 211.662 | 6,98 |
| Uruguay | 128.333 | 4,23 |
| Colombia | 111.969 | 3,69 |
| Brasil | 94.897 | 3,13 |
| Italia | 88.799 | 2,93 |
| España | 71.064 | 2,34 |
| Otro país | 258.240 | 8,51 |
| **Total** | **3.033.786** | **100,00** |

Arithmetic check: the eleven rows sum to 3.033.786 exactly, and the percentages to 100,00.
"Otro país" is a residual over named countries, **not** an unknown-birthplace category; the register
has no missing-country cases. (This matters for §4: the census, by contrast, has 179.239 cases —
9,3% — with country of birth unknown.)

### 1.3 Tabla 2 — region of residence recorded on the DNI

Row percentages, by country of birth. Folio 17 (PDF 18). Every row sums to 100,0 ±0,1.

| País de origen | AMBA | Centro | Cuyo | NEA | NOA | Patagonia |
|---|---:|---:|---:|---:|---:|---:|
| Bolivia | 61,5 | 11,7 | 7,0 | 0,4 | 13,0 | 6,4 |
| Brasil | 56,8 | 19,5 | 1,6 | 16,7 | 2,5 | 2,9 |
| Chile | 19,9 | 14,3 | 11,6 | 0,5 | 1,6 | 52,2 |
| Colombia | 72,0 | 12,8 | 3,2 | 5,2 | 3,4 | 3,5 |
| España | 61,7 | 22,5 | 7,3 | 1,3 | 2,7 | 4,5 |
| Italia | 71,0 | 21,6 | 3,3 | 0,6 | 1,1 | 2,4 |
| Otro país | 67,8 | 17,4 | 3,8 | 2,2 | 3,1 | 5,6 |
| Paraguay | 74,2 | 13,5 | 0,2 | 10,3 | 0,3 | 1,6 |
| Perú | 78,7 | 14,7 | 3,4 | 0,4 | 1,3 | 1,5 |
| Uruguay | 73,7 | 20,3 | 1,1 | 1,4 | 1,0 | 2,5 |
| Venezuela | 81,9 | 10,6 | 2,0 | 0,5 | 1,0 | 4,1 |
| **Total** | **67,1** | **14,3** | **3,7** | **4,3** | **3,8** | **6,9** |

The column heading is *"según región de residencia en el DNI"* — the domicile printed on the
document, not an independently observed place of residence. See §2.6.

AMBA is defined in footnote 8, folio 15 (PDF 16), as CABA plus 40 named Buenos Aires municipalities
— **not** the 24-partido Gran Buenos Aires used by INDEC. Any join to census geography must respect
this; the census `census2022_population_by_jurisdiction_birthplace.csv` reports "24 partidos del
Gran Buenos Aires", a different area.

### 1.4 Sex

Folio 9 (PDF 10), narrative only:

> "Del total de personas nacidas en el exterior, **1.568.350 son mujeres y 1.465.430 varones**
> (solo 6 personas tienen su DNI con género no binario)."

1.568.350 + 1.465.430 + 6 = 3.033.786 exactly. Femininity index 107,0 women per 100 men.
Note the variable is the **gender recorded on the DNI**, not sex at birth — the report says
"género no binario", reflecting Decreto 476/2021. The census variable is *sexo registrado al
nacer*, and INDEC redistributes its category X. The two are not the same variable.

### 1.5 Age × sex — recovered by digitization, not published

Gráfico 2 (folio 11, PDF 12) is a 2048×1536 raster pyramid with no data labels. Bar extents were
measured in pixels against the zero axis and normalized so that both sexes sum to 100%.

**Validation.** The method reproduces the two quantities the report states independently:

| Quantity | Digitized | Report | Error |
|---|---:|---:|---:|
| Male share | 48,28% | 48,30% | 0,02 pp |
| Female share | 51,72% | 51,70% | 0,02 pp |
| Max femininity index, ages 0–44 | 101,7 (20–24) | "101,63" (folio 10) | 0,1 |

Resolution is 1 px ≈ 0,017 pp, so each bar carries roughly ±0,04 pp of edge uncertainty. Groups
below ~0,5 pp (0–4, 95–99, 100+) are unreliable in relative terms; the mid-range groups are good to
about ±1% relative. Full table in the CSV. Summary:

- 25–44 years: **43,8%** of the stock.
- 65 years and over: **17,5%**.
- 80 years and over: **4,6%**.

**A second, external check.** RENAPER's later open data publishes the same variable directly. The
August 2024 file's age distribution tracks the digitized 2022 shape closely — every group agrees
within 0,7 pp except 25–29 (+2,15 pp) and 30–34 (+1,87 pp). Those two exceptions are not
digitization error: they are precisely where the intervening revision removed people (§3.3), so the
check corroborates both the digitization *and* the revision's age profile.

| Group | Digitized 2022 % | Open data Aug 2024 % |
|---|---:|---:|
| 25–29 | 10,13 | 7,98 |
| 30–34 | 12,84 | 10,97 |
| 65+ (total) | 17,51 | 19,19 |
| all other groups | — | within 0,7 pp |

### 1.6 Gráficos 14–15 — top-20 countries, 2010 census vs 2022 register

These bars *do* carry printed data labels, read from the image. The 2022 column is validated
against Tabla 1 (Paraguay 29,7 / Bolivia 21,7 / Perú 9,5 / Venezuela 7,3 / Chile 7,0 / Uruguay 4,2 /
Colombia 3,7 / Brasil 3,1 / Italia 2,9 / España 2,3 — all consistent with Tabla 1 rounded). The 2010
column reproduces the published 2010 census counts to the decimal (Paraguay 550.713/1.805.957 =
30,5%; Bolivia 19,1%; Chile 10,6%; Perú 8,7%; Italia 8,2%; Uruguay 6,5%; España 5,2%; Brasil 2,3%).
Both columns can therefore be used with confidence. Values are in
`renaper_grafico14_15_top20_censo2010_vs_renaper2022.csv`.

### 1.7 Two internal inconsistencies in the report

Recorded in `renaper_grafico13_amba_caba_vs_partidos.csv`:

- **Bolivia, share resident in the 40 AMBA *partidos*:** "59,9%" at folio 22 (PDF 23) vs "56,9%"
  at folio 29 (PDF 30, *Síntesis*).
- **Brasil, share resident in CABA:** "70,0%" at folio 22 vs "70,7%" at folio 29.

The report gives no reconciliation. Neither figure can be preferred on internal evidence.

---

## 2. The definitional rules, verbatim

### 2.1 Universe: digitally processed DNI only

Folio 7 (PDF 8), *Metodología*, verbatim and complete:

> "La base de datos elaborada por la Dirección Nacional de Población se nutre del registro
> administrativo digital del RENAPER creado en el año 2009. A partir del Decreto N°1501/2009, se
> inició la digitalización en el proceso de identificación de los ciudadanos nacionales y
> extranjeros, como así también en la emisión del DNI. En este sentido, para este estudio **solo se
> contabilizan las personas que cuentan con DNI digital** (Resolución 1800/2009, Resolución
> 585/2012), mientras que **quedan afuera todas aquellas personas que cuentan con versiones
> confeccionadas manualmente (Libreta Cívica, Libreta de Enrolamiento y DNI tapa verde o bordo)**."

The unit of analysis is stated at folio 6 (PDF 7):

> "Unidad de análisis: Personas identificadas con DNI con proceso digital (Decreto N°1501/2009),
> **libreta celeste o tarjeta**, de origen extranjero y que residen en el país al mes de agosto de
> 2022."

So both digital formats are in scope — the 2009–2012 *libreta celeste* booklet and the later card.
Only the three pre-2009 manually produced documents are excluded. Legal instruments named:
**Decreto 1501/2009**, **Resolución RENAPER 1800/2009**, **Resolución RENAPER 585/2012**.

The same exclusion is restated in a later DNP publication co-issued with IOM and ECLAC
(DNP/CEPAL/OIM, *La movilidad interna de las personas migrantes en la República Argentina*,
December 2023): *"…se contabilizan las personas que tienen DNI digital, y quedan afuera aquellas
que cuentan con versiones confeccionadas manualmente (Libreta Cívica, Libreta de Enrolamiento y DNI
tapa verde o bordo)."*
https://argentina.iom.int/sites/g/files/tmzbdl901/files/documents/2023-12/la-movilidad-interna-de-las-personas-migrantes-en-la-republica-argentina.pdf

### 2.2 The six-month DNM absence filter

Folio 7 (PDF 8), immediately following, verbatim and complete:

> "La BdDR, también cuenta con información provista por la Dirección Nacional de Migraciones (DNM)
> que permite estimar la cantidad de personas que residen actualmente en la Argentina. Para ello,
> **se solicitó a la DNM la cantidad de personas que no se encuentran en el país desde, al menos,
> hace más de 6 meses, pero que en su DNI cuentan con residencia en el país**, a los fines de
> eliminar del cómputo aquellas personas que no estarían residiendo actualmente en Argentina."

**How it works, and its four structural holes.** The rule is a subtraction, not a residence test.
DNM supplies a list of people whose border records show them out of the country for more than six
months; those people are deleted. A person is therefore **retained by default**. That means:

1. **Only recorded absences count.** A departure that generated no usable DNM record leaves the
   person in the count.
2. **The person must have been matched on the DNI.** The most authoritative published statement of
   this problem comes from an INDEC–CONICET demographer (Ameijeiras 2025, §5): *"señalaron la
   dificultad de contabilizar a las personas a partir del registro de egresos e ingresos ya que
   justamente los extranjeros cuentan con múltiples documentos de identidad y podrían haber salido
   del país con un documento distinto al DNI."* A Paraguayan who leaves on a Paraguayan passport or
   cédula is not matched, and so is not removed.
3. **Six months is a long threshold.** Circular and seasonal migrants who return inside six months
   are retained regardless of where their centre of life is.
4. **It is a point-in-time query, not a longitudinal one.** Someone absent for years who happened to
   re-enter shortly before the extract resets the clock.

No sensitivity analysis, no count of how many people the filter removed, and no match rate are
published. The report does not state how many records the filter deleted.

### 2.3 Deceased persons

**What the report says.** The word "purge" never appears. The only statement is in the source line
of every table, chart and map: the base is

> "las personas **vivas** con DNI con proceso digital…"

That is an assertion, not a method. Unlike the six-month absence filter, which is described, the
report names no death-notification process, no civil-registry linkage and no cut-off date. This is
the largest documentation gap in the methodology. Everything below comes from outside the report.

**The statutory circuit is passive.** Ley 17.671 art. 17 inc. b) makes RENAPER a recipient, not an
investigator:

> "b) Registrar la inscripción de los nacimientos, matrimonios y fallecimientos, **de acuerdo con
> las comunicaciones recibidas** de las oficinas seccionales o consulares correspondientes;"

The "oficinas seccionales" are the 24 provincial and CABA civil registries (art. 62). Art. 46 places
the duty on the certifying doctor to record the deceased's DNI number on the death certificate.
**There is no article of Ley 17.671 requiring surrender or annotation of the DNI on death** — arts.
47 and 48 concern domicile and time limits, not *defunción*.

**"Persona viva" operationally means "no death notice on file".** RENAPER's own *Convenio Único de
Servicio de Aviso de Fallecimiento* (Disposición 3132) enumerates five death states, of which the
fifth is:

> "5) SIN AVISO DE FALLECIMIENTO: la persona no registra aviso de fallecimiento registrado en
> 'RENAPER'."

and attaches this disclaimer:

> "El 'RENAPER' **no garantiza el cumplimiento por parte de las Direcciones Generales** mencionadas
> en la remisión tempestiva de los avisos de fallecimiento correspondientes."

So the DNP's "personas vivas" is *persons against whom no death notice has arrived* — not persons
verified alive. The universe is defined by the absence of an incoming record.

**RENAPER concedes the notifications run late.** Disposición RENAPER 1804/2018 (B.O. 20/04/2018)
exists because of the delays, and says so in its own *considerandos*:

> "Que esta DIRECCIÓN NACIONAL DEL REGISTRO NACIONAL DE LAS PERSONAS ha tomado conocimiento de **los
> atrasos que tienen los Registros Civiles Provinciales en informar los Avisos de Fallecimiento**,
> luego del labrado de la respectiva Acta de defunción."

It imposes a 20-day loading deadline (art. 1). Note the territorial scope stated in the same
*considerandos*: the digital F24D notice covers *"las defunciones acontecidas y registradas **en
territorio argentino**"*.

**Foreigners were explicitly deprioritised in death processing.** Auditoría General de la Nación,
Informe 216/2013, §4.4.3:

> "Del relevamiento efectuado surge que una vez ingresados los formularios de fallecimiento a la
> División Fallecidos **existe una demora de aproximadamente 6 meses para su procesamiento e ingreso
> a la base de datos del ReNaPer.** […] Asimismo cabe destacar que **previo a los períodos
> eleccionarios sólo se procesan los datos correspondientes a las personas en condiciones de emitir
> su voto (mayores nacionales) dejando para su posterior procesamiento los extranjeros y menores de
> edad**."

This describes the pre-F24D paper circuit and should be cited as evidence of historical accumulation
in the base, not of its 2022 state. But the population it deprioritised is exactly the population
this report counts.

**The DNP itself still reports lag and under-registration.** Its own mortality monitor
(*Monitoreo de Mortalidad en Argentina 2020–2024*, https://estadisticas.renaper.gob.ar/app_momo/):

> "**El tiempo entre ocurrencia y registro varía según la jurisdicción, pudiendo generar déficits
> aparentes por demoras en la carga.**" … "**Puede existir subregistro de defunciones en determinados
> períodos.**" … "Se excluyó a la provincia de Santiago del Estero del análisis debido a
> inconsistencias detectadas en el registro de defunciones."

**Deaths abroad are structurally invisible — and this is the finding that matters most.** The F24D
system covers only deaths occurring and registered in Argentine territory. The consular channel that
handles Argentine deaths abroad (Ley 17.671 art. 17 inc. b, second limb) **explicitly excludes
foreigners**. Consulado General en Madrid, *Inscripción consular de la partida de defunción*, §5:

> "**Extranjeros con DNI argentino**: lo indicado en este apartado **no resulta de aplicación para
> el fallecimiento de un ciudadano extranjero titular de DNI argentino para residentes extranjeros.
> No se efectúan inscripciones consulares de defunciones de personas que no hayan tenido la
> nacionalidad argentina.**"

Identical wording appears at the Embajada en Austria and, affirmatively, at the Consulado en
Tenerife: *"No aplica a ciudadanos extranjeros que hubieran residido en Argentina y tuvieran un DNI
argentino para extranjeros."*

**Consequence.** A Bolivian- or Paraguayan-born holder of an Argentine DNI who returns home and dies
there has **no channel by which RENAPER can learn of it**. Such a record stays in state 5 forever.
Note, however, that this does not add a term to the reconciliation beyond factor (b) in §4: that
person had already emigrated, and if DNM had recorded the exit the absence filter would have removed
them regardless of whether they were alive. What it does mean is that the over-count is
**irreversible by any mechanism the register possesses** — no future process can ever clear it.

**Not established, and do not assert it:** no RENAPER or Cámara Nacional Electoral document states
that deaths abroad cannot be known; the conclusion above rests on the two converging texts. **No
published audit or official figure quantifies how many deceased persons remain in the RENAPER base
or the electoral roll.** Do not attribute a number to anyone. INDEC's Programa de Análisis
Demográfico reports "algunas inconsistencias para eliminar personas fallecidas" from exercises it
explicitly describes as **unpublished** (Ameijeiras 2025), with no magnitude.

For the empirical ceiling the data themselves place on this factor, see §4.2.

### 2.4 Persons with *precaria*, *transitoria* or *temporaria* residence

**Not addressed in the report at all** — its universe is defined by document type plus the absence
filter, never by immigration status. The rule can nonetheless be established from statute.

**Ley 25.871 art. 30** (original 2004 text, still in force; not amended by DNU 70/2017 or DNU
366/2025) is exhaustive:

> "ARTICULO 30. — Podrán obtener el Documento Nacional de Identidad, **los extranjeros con residencia
> permanente o temporaria**."

> "ARTICULO 31. — Los solicitantes de refugio o asilo, con autorización de residencia precaria,
> podrán obtener su Documento Nacional de Identidad **una vez reconocidos** como 'refugiados' o
> 'asilados' por la autoridad competente."

> "ARTICULO 32. — Cuando se trate de extranjeros autorizados en calidad de 'residentes temporarios'
> el Documento Nacional de Identidad se expedirá por el mismo plazo que corresponda a la
> subcategoría migratoria otorgada…"

**DNM states it plainly** (https://www.argentina.gob.ar/migraciones/residencias):

> "Residencias **Transitorias**: […] **no habilitan la obtención de DNI**."
> "Residencias **Temporarias**: […] **Habilitan la obtención de DNI temporario**."
> "Residencias **Permanentes**: […] **Habilitan la obtención de DNI permanente**."

**The pipeline that actually populates the register** is Decreto 616/2010 art. 30, and it carries a
threshold worth noting:

> "La DIRECCION NACIONAL DE MIGRACIONES comunicará inmediatamente a la DIRECCION NACIONAL DEL
> REGISTRO NACIONAL DE LAS PERSONAS **toda residencia permanente, o temporaria que sea otorgada por
> un plazo de UN (1) año o más**."

**Answers.** *Temporary residents are inside the universe* — they hold a DNI, and it is in the
digital format, so they appear in the 3.033.786. Their DNI expires with the residence (art. 32),
which incidentally bounds how stale their recorded domicile can be. *Transitory residents are
outside it.* *Precaria holders are outside it* — a *precaria* is a certificate, not an identity
document; Decreto 616/2010 art. 20 inc. d) calls it *"el certificado que emita la autoridad de
aplicación otorgando una residencia precaria"*, and DNM's own travel guidance has *precarios*
crossing borders on a passport plus the certificate, not a DNI. Even refugee and asylum applicants
holding a *precaria* must wait for recognition (art. 31).

**Caveats.** No official page says in so many words that a *precaria* does not yield a DNI; the
exclusion is an inference from four converging texts. Two official documents are internally
inconsistent and should not be relied on: RENAPER's `requisitos_dni.pdf` says "residencia permanente
**o transitoria**", contradicting art. 30 and DNM's own page (evidently a slip for *temporaria*); and
Disposición 1255/2023 uses "transitoria" where the DNI's own field admits only TEMPORARIA or
PERMANENTE. Also note that **there is no art. 20 bis in force** — it existed only 2017–2021 (DNU
70/2017, abrogated by Decreto 138/2021) — and DNU 366/2025 substituted art. 20 without touching DNI
issuance. Do not cite 366/2025 for a DNI rule.

### 2.5 Naturalized Argentines born abroad

**The record can answer the question; the report does not say whether it was asked.**

*What is established.* The RENAPER record retains the foreign country of birth and links the
naturalized person's file to their former foreigner matrícula. Disposición RENAPER 1255/2023,
Anexo I (the spec in force when the report was written):

> "En los DNI de personas naturalizadas figuran el número de Juzgado y la fecha de naturalización."
> "En los DNI de personas naturalizadas, que previamente poseían un DNI argentino para personas
> extranjeras, figuran el número de Juzgado, la fecha de naturalización y **la respectiva asociación
> con la matrícula anterior**."

Its successor, Disposición 55/2026, makes birthplace explicit: *"En los DNI de personas
naturalizadas figuran **el país de nacimiento**, número de Juzgado y la fecha de naturalización."*
(By contrast, a native Argentine's DNI records only the province.) Ley 17.671 art. 20 obliges federal
judges to notify RENAPER of every *carta de ciudadanía*, and Decreto 616/2010 art. 30 has RENAPER
notify DNM in return.

The DNP itself describes this population as *"personas **nacidas en el extranjero** nacionalizadas
por naturalización"* and profiles it *"según **país de nacimiento**"* in a companion study
(*Caracterización sociodemográfica de la población nacionalizada argentina … 2013-2023*, Oct 2023).
Scale: **46.026** first-DNI transactions via *carta de ciudadanía* plus **42.928** via *opción* over
2013–2023 — roughly 1,5–3% of 3,03 million. Small, but not nil.

The successor open data settles the direction for the current series: the June 2026 file publishes
`pais_nacimiento` and `nacionalidad` as **separate fields** and reports 2.367.573 persons born abroad
against 2.147.086 of foreign nationality — a gap of ~220.000 that is precisely the naturalized
foreign-born. The register plainly distinguishes the two, and the migration series keys on birth.

*What is not established.* **The December 2022 report never uses the words "naturalizado",
"nacionalizado" or "ciudadanía" — zero occurrences in the full text.** And the report equivocates
between two criteria in adjacent paragraphs: the *Introducción* and every source line say
**"personas nacidas en el exterior"** (birthplace), while the *Diseño de investigación* says
**"de origen extranjero"** and every table header says **"País de origen"**. RENAPER's live dashboard
is separately titled "Población **Extranjera** identificada con residencia en Argentina", and
RENAPER runs a *separate* naturalizados dashboard. So the record could answer a birthplace query and
the report's dominant wording is birthplace-based, but **which query was actually run cannot be
documented**. Treat this as an unresolved ambiguity in the source.

*For the reconciliation this matters little either way*, because the census also classifies by place
of birth: if the DNP ran a birthplace query the two are aligned, and if it ran a nationality query
the register is understated by ~1,5–3%, which pushes in the same direction as factors (c) and (e).

### 2.6 What "residencia" means

Two different things, and the report uses both without flagging the difference.

**(a) In the headline count**, residence is the DNM six-month absence test of §2.2, applied to people
who *"en su DNI cuentan con residencia en el país"* — i.e. whose DNI carries an Argentine domicile.
The criterion is therefore: *an Argentine domicile is printed on the document* **and** *DNM has no
record of an absence longer than six months*. That phrase does mean the DNI shows an Argentine
address; it describes exactly the people the filter removes.

**(b) In every geographic breakdown**, residence is purely the **domicile printed on the DNI**.
Tabla 2 says *"según región de residencia en el DNI"*; all eight maps say *"según jurisdicción de
residencia en el DNI"*.

**That domicile is self-declared and never verified.** Ley 17.671 art. 47:

> "Todas las personas de existencia visible o sus representantes legales […] están obligados a
> comunicar en las oficinas secciónales, consulares o que se habiliten como tales, el cambio de
> domicilio, **dentro de los treinta días** de haberse producido la novedad."

Art. 38 prices non-compliance at **one tasa** — the cost of the trámite itself:

> "Será sancionado con una multa cuyo importe será equivalente a una (1) tasa vigente a la fecha en
> que se realice el trámite, la persona mayor de dieciséis (16) años que no denuncie dentro de los
> noventa (90) días de producido su cambio de domicilio…"

RENAPER asks for no evidence of address anywhere in the country; its published requisitos for a
change-of-domicile DNI list only the previous DNI ("recomendado, no excluyente"). Consular guidance
states the rule outright: *"**El domicilio a asentar es estrictamente declarativo. No es requisito
presentar empadronamiento ni prueba documental alguna del mismo.**"*

**Nothing in the renewal cycle forces an address update.** Correcting a common misreading: the
"5 and 8" in Decreto 1501/2009 art. 5 are **ages, not intervals**. The stages are an update between
ages 5 and 8, another at 16, and thereafter:

> "C - A partir de los DIECISEIS (16) años, cualquiera sea la edad del identificado, todo ejemplar
> de los nuevos Documentos Nacionales de Identidad (D.N.I.) […] **tendrán una validez de QUINCE (15)
> años** a partir de la fecha de su emisión. Las actualizaciones serán obligatorias hasta cumplidos
> los SETENTA (70) años de edad."

So the jurisdiction recorded in Tabla 2 and the eight maps can be **up to 15 years stale for an adult
permanent resident, and unbounded above age 70** — and it was never verified when first declared. It
is a different variable from the census's *residencia habitual*, and it is why the DNP had to
commission a separate study of internal residential mobility (DNP/CEPAL/OIM 2023).

**A foreigner's DNI can only carry an Argentine address, and no consulate will change it.** This is
the structural asymmetry that makes the register's geography self-fulfilling. Disposición 1255/2023,
Anexo I, "B. DORSO / III. Personas extranjeras":

> "01. Domicilio: declarado según 'calle y número, ciudad, partido/departamento, provincia' […]
> **Correspondiente a su lugar de residencia en Argentina.**"

An Argentine national living abroad declares a foreign domicile and *may not* declare an Argentine
one. A foreign national has no such option — and the consulates refuse the trámite entirely:

> "**Los Consulados no tramitan renovación de DNI argentinos para extranjeros. El trámite se realiza
> exclusivamente en la Argentina.**" — Consulado General en Madrid

So a foreign-born person who emigrates keeps an Argentine domicile on their DNI **by construction**,
permanently, no matter where they live. The only thing that can remove them from the count is a DNM
exit record — which is precisely the mechanism §2.2 shows to be leaky. This is the mechanical reason
factor (b) in §4 is as large as it is.

### 2.7 The report's own caveats

Two, both important, both easy to miss.

**Footnote 9, folio 24 (PDF 25)** — the canonical statement of why the register and the census are
not the same quantity:

> "La base de RENAPER contabiliza personas identificadas con DNI argentino mientras que el censo
> contabiliza personas residiendo en Argentina en un momento determinado, sin importar su estatus
> legal de residencia."

**Folio 23 (PDF 24)** — the DNP's own claim for the register, made *before* the census results
existed:

> "A más de una década del censo 2010 y a la espera de los resultados del censo 2022, la información
> provista por RENAPER permite dar cuenta de las modificaciones ocurridas en los últimos años.
> Teniendo en cuenta la política migratoria en Argentina que facilita el acceso a la residencia, se
> podría afirmar que los registros administrativos cuantifican gran parte del fenómeno migratorio."

This claim has not been revisited by the DNP since the census landed.

---

## 3. The series over time

### 3.1 There is no second edition of this report

The December 2022 report is the **only** edition. No 2023, 2024, 2025 or 2026 "Caracterización de la
migración internacional" exists. Checked: the DNP studies index
(`argentina.gob.ar/interior/renaper/estadistica-de-poblacion/estudios`, 19 studies), its Migración
section (11 studies), the DNP landing page, and the report's own landing page. No
"Radiografía de la migración" or "Radiografía migratoria" exists from RENAPER, the DNP or the DNM.

Two versions of the 2022 report itself circulate — **Noviembre 2022** and **Diciembre 2022** —
identical but for the added authorities page. Cite the December one.

The DNP was **not** dissolved after the December 2023 change of government, but it moved: the
current chain is Jefatura de Gabinete de Ministros → Vicejefatura de Gabinete del Interior →
RENAPER → Dirección Nacional de Población. Mariano Fagalde remains Director Nacional de Población.
The DNM moved separately, to the Ministerio de Seguridad Nacional. **The PDF series was replaced by
dashboards plus open data**, not continued.

### 3.2 The open-data successor, recomputed here

RENAPER publishes the same universe as flat CSVs at `datosabiertos.renaper.gob.ar`, catalogued on
`datos.gob.ar` as *"Estructura de población de origen extranjero"*
(https://datos.gob.ar/dataset/estructura-de-poblacion-de-origen-extranjero), disaggregated by
country of birth × province × department × sex × five-year age group. Four editions exist.
**The totals below were recomputed independently from the source CSVs for this note**, not taken
from any summary:

| Reference date | Foreign-born, digital DNI, resident | Basis |
|---|---:|---|
| **Agosto 2022** | **3.033.786** | Stated in the DNP report |
| Enero 2023 | 3.007.251 | Secondary source only (CIC-PBA citing RENAPER); no primary document found — **use with caution or drop** |
| **Agosto 2024** | **2.470.453** | Recomputed from `poblacion_extranjera_identificada_provincia_agosto_2024.csv` |
| **Enero 2025** | **2.458.191** | Recomputed from `…_enero_2025.csv` |
| **Junio 2025** | **2.349.816** | Recomputed from `…_junio_2025.csv`; corroborated verbatim by *Infobae* (4 Jan 2026) quoting RENAPER |
| **Junio 2026** | **2.367.573** | Recomputed from `…_junio_206.csv` (the `206` typo is in the official URL) |

By country, in `renaper_serie_stock_2022_2026.csv`:

| País | 2022-08 | 2024-08 | 2025-01 | 2025-06 | 2026-06 |
|---|---:|---:|---:|---:|---:|
| Paraguay | 900.238 | 744.306 | 754.673 | 721.735 | 711.122 |
| Bolivia | 658.559 | 542.872 | 535.370 | 528.177 | 551.789 |
| Perú | 289.430 | 227.179 | 213.767 | 207.647 | 207.428 |
| Venezuela | 220.595 | 197.395 | 196.573 | 185.245 | 197.682 |
| Chile | 211.662 | 182.173 | 183.045 | 175.836 | 171.086 |
| Uruguay | 128.333 | 111.814 | 113.475 | 107.933 | 105.983 |
| Colombia | 111.969 | 68.057 | 62.766 | 57.639 | 57.670 |
| Brasil | 94.897 | 76.323 | 79.448 | 69.538 | 67.248 |
| Italia | 88.799 | 74.311 | 70.728 | 68.236 | 64.134 |
| España | 71.064 | 55.028 | 54.422 | 51.039 | *(dropped)* |
| China | 51.361 | 31.946 | 31.924 | 30.111 | 32.283 |
| **Total** | **3.033.786** | **2.470.453** | **2.458.191** | **2.349.816** | **2.367.573** |

*España* is absent from the June 2026 file because that edition publishes only 20 country categories
and folds Spain into "Otro país" — which rises from 53.049 to 103.533, a difference of 50.484
against Spain's 51.039 in June 2025. This is a published-category change, not a data anomaly.

### 3.3 The series is not stable and not growing — it falls by 18,6%

**This is the most consequential finding for the audit.** The stock does not behave like a register
of a growing migrant population. It falls from 3.033.786 (Aug 2022) to 2.470.453 (Aug 2024) — a drop
of **563.333, or 18,6%** — and then flattens at 2,35–2,47 million.

The drop cannot be demographic:

- **Not mortality.** Expected deaths in a population of this size and age structure are about 38.000
  a year (§4a); two years is ~76.000, one seventh of the drop.
- **Not naturalization.** The universe is place of birth, which naturalization does not change; and
  total naturalizations 2013–2025 are only ~118.600 on RENAPER's own figures.
- **Not a change of universe.** The open-data files use the identical definition — living persons
  born abroad, digital DNI, resident in Argentina.
- **Not net emigration.** No plausible outflow removes half a million people in 24 months.

The drop is also **not age-neutral**, which points at the residence filter. Comparing the 2022
report's digitized structure with the recomputed Aug 2024 file:

| | Aug 2022 | Aug 2024 | Change |
|---|---:|---:|---:|
| Aged 65+ | ~531.000 (17,5%) | 474.153 (19,2%) | −11% |
| Aged under 65 | ~2.503.000 (82,5%) | 1.996.300 (80,8%) | −20% |

The revision removed working-age people at roughly twice the rate of the elderly. That is the
signature of a **tightened or corrected residence/absence rule**, not of deaths or emigration.

**No published methodological note documents this revision.** RENAPER has not explained it, and
neither has the DNP. Two implications for the paper:

1. **The 2022 and 2024+ figures are not one series.** They must not be plotted as a trend.
2. **RENAPER's own later figures repudiate 3.033.786 as a residence count.** By June 2025 the
   register itself reports 2.349.816 — 684.000 below the August 2022 figure and only 22% above the
   census. Whatever the correct number, the register's publisher no longer stands behind 3,03
   million as a count of residents.

### 3.4 The predecessor report is a flow study, not a stock

DNP, *Migración Internacional Reciente en Argentina entre 2012 y 2020*, November 2021.
https://www.argentina.gob.ar/sites/default/files/2021/11/migracion_internacional_reciente_en_la_argentina_entre_2012_y_2020.pdf
Its unit is *radicaciones resueltas* (resolved residence permits), not persons: *"Entre 2012 y 2020,
se otorgaron en total 1.916.884 radicaciones y en promedio se realizaron 212.987 por año."* Permits
are transactions; one person can generate several (temporary, then permanent). It cannot be
differenced against a stock. IOM makes the same point:
*"lo que se cuenta son trámites y no individuos."*

### 3.5 Other open data located

- *"Estructura de población Argentina"* — https://datos.gob.ar/dataset/estructura-de-poblacion-argentina
  — the whole identified population with both `pais_nacimiento` and `nacionalidad`; reproduces the
  foreign-born totals above exactly.
- *"Población Nacionalizada en Argentina"* — https://datos.gob.ar/dataset/poblacion-nacionalizada-en-argentina
- Dashboards at `estadisticas.renaper.gob.ar` (`app_extranjeros`, `app_poblacion`,
  `app_naturalizados`, `app_idt`). These are R/Shiny apps rendering over websocket; values cannot be
  scraped statically. `app_migracion` is **internal** residential mobility, not international
  migration.
- **No DNM data on datos.gob.ar.** A `radicaciones` query returns zero datasets and DNM has no
  organization page on the portal. DNM's old `/interior/migraciones/estadisticas` path did not
  survive its move to the Ministerio de Seguridad.

---

## 4. Quantifying the gap

**The gap.** 3.033.786 − 1.933.463 = **1.100.323**, i.e. the register is **56,9% above** the census.

### 4.0 Two diagnostics that constrain everything else

Before assigning magnitudes it is worth establishing where in the population the excess sits,
because that rules several explanations in and out. Both diagnostics compare the register against
the census on the same axis.

**By age** (`renaper_vs_censo2022_estructura_por_edad.csv`; RENAPER structure digitized from
Gráfico 2, census from `census2022_foreign_born_by_country_age.csv`):

| Age group | RENAPER % | Census % | RENAPER n | Census n | Ratio |
|---|---:|---:|---:|---:|---:|
| 0–4 | 0,26 | 1,06 | 7.888 | 20.579 | **0,38** |
| 5–9 | 1,58 | 2,08 | 47.934 | 40.130 | 1,19 |
| 10–14 | 2,51 | 2,87 | 76.148 | 55.525 | 1,37 |
| 15–19 | 3,71 | 4,44 | 112.553 | 85.843 | 1,31 |
| 20–24 | 5,80 | 5,75 | 175.960 | 111.219 | 1,58 |
| 25–29 | 10,13 | 8,06 | 307.323 | 155.745 | **1,97** |
| 30–34 | 12,84 | 10,08 | 389.538 | 194.930 | **2,00** |
| 35–39 | 11,64 | 10,02 | 353.133 | 193.685 | **1,82** |
| 40–44 | 9,18 | 8,56 | 278.502 | 165.504 | 1,68 |
| 45–49 | 7,19 | 7,50 | 218.129 | 145.046 | 1,50 |
| 50–54 | 6,70 | 7,17 | 203.264 | 138.706 | 1,47 |
| 55–59 | 5,98 | 6,52 | 181.420 | 126.000 | 1,44 |
| 60–64 | 4,99 | 5,47 | 151.386 | 105.851 | 1,43 |
| 65–69 | 4,56 | 5,11 | 138.341 | 98.792 | 1,40 |
| 70–74 | 4,52 | 5,25 | 137.127 | 101.522 | 1,35 |
| 75–79 | 3,85 | 4,47 | 116.801 | 86.460 | 1,35 |
| 80–84 | 2,39 | 2,83 | 72.507 | 54.623 | 1,33 |
| 85–89 | 1,32 | 1,65 | 40.046 | 31.911 | 1,25 |
| 90–94 | 0,66 | 0,81 | 20.023 | 15.693 | 1,28 |
| 95–99 | 0,19 | 0,26 | 5.764 | 5.059 | 1,14 |
| 100+ | 0,02 | 0,03 | 607 | 640 | 0,95 |
| **Total** | 100,00 | 100,00 | **3.033.786** | **1.933.463** | **1,57** |

The ratio is a clean inverted-U: it peaks at **2,00 at ages 30–34** and falls monotonically above
age 45 to **1,14 at 95–99**. The register's 65+ share is **17,5%**, *below* the census's **20,4%**.

**This is the opposite of the signature of unpurged deaths**, which would pile up at the oldest ages
and make the register look older than the census. The excess is concentrated in exactly the ages
that migrate, re-migrate and circulate.

**By country** (`renaper_vs_censo2022_por_pais.csv`). The census has 179.239 cases (9,3%) with
country of birth unknown; the adjusted column redistributes them proportionally over named countries
(factor 1,1022), which is the like-for-like comparison.

| País | RENAPER Aug 2022 | Censo 18 May 2022 | Ratio | Censo ajustado | Ratio ajustado |
|---|---:|---:|---:|---:|---:|
| Ecuador | 27.350 | 8.879 | 3,08 | 9.786 | **2,79** |
| China | 51.361 | 18.629 | 2,76 | 20.533 | **2,50** |
| Colombia | 111.969 | 46.482 | 2,41 | 51.232 | **2,19** |
| Bolivia | 658.559 | 338.299 | 1,95 | 372.872 | 1,77 |
| Brasil | 94.897 | 49.943 | 1,90 | 55.047 | 1,72 |
| Perú | 289.430 | 156.251 | 1,85 | 172.219 | 1,68 |
| Paraguay | 900.238 | 522.598 | 1,72 | 576.005 | 1,56 |
| España | 71.064 | 48.492 | 1,47 | 53.448 | 1,33 |
| Chile | 211.662 | 149.082 | 1,42 | 164.318 | 1,29 |
| Venezuela | 220.595 | 161.495 | 1,37 | 177.999 | 1,24 |
| Uruguay | 128.333 | 95.384 | 1,35 | 105.132 | 1,22 |
| Italia | 88.799 | 68.169 | 1,30 | 75.136 | **1,18** |
| **Total** | **3.033.786** | **1.933.463** | **1,57** | — | 1,57 |

The lowest ratio in the table belongs to **Italy** — the oldest, longest-settled, least mobile
population in it, and precisely the one that unpurged deaths and the digital-DNI exclusion would
distort most. The highest belong to recent, highly mobile flows. Venezuela's low ratio (1,24) fits
the same logic in reverse: arrivals too recent to have accumulated exits or deaths.

Both diagnostics point the same way: **the gap is a residence problem, not a mortality problem.**

### 4.1 The quantification table

Full text of the bases is in `renaper_reconciliacion_factores.csv`. Sign convention: **+** means the
factor pushes the register above the census; **−** means it pushes the register *below* the census,
so the remaining + factors must be correspondingly larger.

| Factor | Direction | Low | High | Central | Basis (abridged) |
|---|---|---:|---:|---:|---|
| **a.** Deaths of DNI holders not purged | + | 0 | 120.000 | 40.000 | 37.809 expected deaths/yr at 2022 Argentine age-sex rates on the digitized structure (crude 12,46‰), 53% of them at 80+. Ceiling with *zero* purging would be 270k–418k; capped at ~120.000 by the 80+ cell (§4.2) |
| **b.** Emigration / non-residence missed by the 6-month DNM filter | + | **780.000** | **1.483.000** | **1.155.000** | Residual, plus two independent checks: age-excess method gives ≥460k–547k; RENAPER's own later revision removed 563.333 by Aug 2024 and 683.970 by Jun 2025 |
| **c.** Digital-DNI-only exclusion (pre-2009 documents) | − | 0 | 100.000 | 40.000 | Real in direction, invisible in the data: RENAPER Europe/census Europe = 1,46 vs 1,57 all-origin. Bounded by compulsory DNI renewal at 5/8/14 years |
| **d.** Date difference 18 May → 31 Aug 2022 | ≈0 | −15.000 | +15.000 | 0 | +9.741 net non-native migration vs −10.870 deaths over 3,45 months. Net **−1.129** |
| **e.** Migrants with no DNI (counted by census, not by RENAPER) | − | 130.000 | 300.000 | 190.000 | ENMA: **11%** without a DNI in 2020, **7%** in 2023. 7–11% of ~2,0M = 137.000–226.000. About half of that group is legally *regular* — precarios and temporarios awaiting a DNI |
| **f.** Country-of-birth coding | ± | −20.000 | +50.000 | +10.000 | Both sources key on place of birth; naturalization is not a divergence. Residual risk is consular registrations of Argentines born abroad |
| **g.** Census universe = private dwellings only | + | 12.000 | 45.000 | 25.000 | **273.498** people outside the universe (267.793 collective + 5.705 street); foreign-born at 1×–3× the 4,24% share, or bottom-up from geriátricos and prisons |
| **h.** Census under-enumeration of the foreign-born | + | 10.000 | 250.000 | 100.000 | AD39 net differential −0,5% overall, −2,1% for men. High end from the sex-ratio gap: 119.725 foreign-born men implied missing |
| **Observed gap** | | | | **1.100.323** | Identity: gap = (a+b+d+f+g+h) − (c+e) |

The identity closes: all three assignments reconstruct 1.100.000 against an observed 1.100.323.

### 4.2 Reading the table

**(a) Deaths cannot carry this, and the 80+ cell proves it.** The arithmetic ceiling — 13 years of
accumulated deaths with no purging at all — is 270.000–418.000, at most 38% of the gap. The data cut
that down much further. In this population 53% of expected deaths fall at ages 80 and over, where
the register holds 138.947 people against the census's 107.926, a ratio of 1,29. An unpurged mass of
*U* implies a true live-and-resident ratio at 80+ of (138.947 − 0,53·*U*) / 107.926:

| Unpurged deaths *U* | Implied true ratio at 80+ |
|---:|---:|
| 0 | 1,29 |
| 20.000 | 1,19 |
| 60.000 | 0,99 |
| 100.000 | 0,80 |
| 120.000 | 0,71 |

Against an all-origin ratio of 1,57 and an Italian ratio of 1,30, a true 80+ ratio of 0,71 would
require the digital-DNI exclusion to be several times larger than anything else in the evidence
supports. **120.000 is a hard ceiling; the central value is nearer 40.000.**

The mechanism evidence genuinely cuts both ways and should be reported as such. For a larger value:
the AGN found a six-month processing delay and the explicit deprioritisation of *extranjeros* before
elections (§2.3); RENAPER concedes provincial *atrasos* and disclaims timeliness; and deaths abroad
of foreign nationals have no notification channel whatsoever. For a smaller value: every source line
says "personas vivas", the register is *younger* than the census rather than older, and its Italian
population is its least inflated of all. What INDEC's demographers report is "algunas
inconsistencias" (Ameijeiras 2025), from exercises they describe as unpublished, with no magnitude
attached. Treat any claim that unpurged deaths explain the gap as unsupported.

**(b) Non-residence is the answer, and the register's publisher now agrees.** Between one quarter
and one half of the August 2022 records were for people not resident in Argentina. The strongest
evidence is not any calculation here but RENAPER's own subsequent behaviour: the same series, on the
same definition, reports 2.470.453 by August 2024 and 2.349.816 by June 2025 (§3.3). The register
deleted 684.000 records in under three years, disproportionately of working-age people, without
publishing a methodological note. That is a residence correction.

**(c) and (e) run the other way and are usually forgotten.** Together they mean the register
*understates* the resident foreign-born population by something like 130.000–400.000 people at the
same time as it *overstates* it by roughly a million. These are not offsetting errors in any useful
sense — they fall on different people. The digital-DNI rule drops elderly long-settled Europeans;
the no-DNI gap drops recent and precarious arrivals.

Note what (e) actually measures. ENMA's "sin DNI" group is **not** the irregular population: it
reports that roughly half of it is legally regular — 31,7% hold a *precaria*, 16,8% a *temporaria*
awaiting the document, 5,9% a provisional paper. That is precisely the population Ley 25.871 art. 30
excludes from a DNI (§2.4). So the register's blind spot is not confined to people breaking the law;
it includes everyone in the documentation pipeline. It is heavily concentrated: 13,5% of
extra-MERCOSUR non-European migrants lack a DNI, and 24,0% in the NOA and 23,3% in the NEA against
5,8% in AMBA. For any analysis of informal settlement or of vulnerable migrant populations, **(e) is
the error that matters**, and it is the error the register cannot fix.

**(d) is genuinely negligible.** The two components cancel to −1.129 people. Anyone attributing
material weight to the 3½-month reference-date difference is wrong by two orders of magnitude.

**(h) deserves more weight than the census-side literature gives it.** The sex-ratio discrepancy is
hard to explain away: the census foreign-born population is 121,7 women per 100 men, the register
107,0. AD39 independently reports the 2022 census under-counted men by 2,1% and over-counted women
by 1,1%. Calvelo (2011) is the standard Argentine statement that non-native omission exceeds native
omission and has risen since 1960. But no migrant-specific 2022 omission rate has ever been
published, so this factor cannot be pinned down.

### 4.3 A caution about INDEC AD39 Tabla 11

INDEC's estimate of emigration of non-natives, **181.779 for 2010–2022** (AD39, Tabla 11, p. 30,
against 622.234 immigrants and a net balance of +440.455), is tempting to use for factor (b) and
should not be. AD39 states its own method:

> "en el caso de emigración de no nativos se utilizó como método indirecto la estimación de la
> diferencia entre el stock censal de inmigrantes extranjeros, los sobrevivientes del stock de
> inmigrantes del censo anterior y la cantidad de inmigrantes llegados al país en el período
> intercensal."

It is a **residual computed from the census stock itself**. Using it to explain a register-versus-
census gap assumes the census is right, which is the thing in question. It is reported here for
completeness, not as an input.

### 4.4 Mortality inputs used, and their validation

Deaths: **DEIS microdata `defweb22_0.csv`** (Estadísticas Vitales 2022), 397.115 deaths, tabulated
here by five-year age group and sex. Denominator: **INDEC's 2022-census-based national projection**
(`proyecciones_nacionales_2022_2040_base.csv`, 46.135.579 at 1 July 2022). Note that DEIS's *own*
published rates use the superseded 2010-based AD36 denominator (46.234.830), so the two differ
slightly by construction.

The rates computed here reproduce DEIS's published *tasas específicas* to about 1%:

| Group | Mine, M | DEIS, M | Mine, F | DEIS, F |
|---|---:|---:|---:|---:|
| 65–69 | 28,52 | 28,15 | 15,23 | 15,25 |
| 70–74 | 42,49 | 42,99 | 24,38 | 24,49 |
| 75–79 | 65,96 | 66,12 | 39,75 | 39,98 |

For work needing a proper life table rather than period rates, INDEC published census-2022-anchored
abridged tables in machine-readable form on 15 October 2025 —
`https://censo.gob.ar/wp-content/uploads/2025/10/tabla_mortalidad_2020_2022_base_csv.csv`, with
columns `m, q (nqx), l, d, L, T, P, e`. They confirm e₀ 2022 = **73,42** (men) / **79,05** (women) /
76,16 (both).

**There is no direct measurement of foreign-born mortality in Argentina, and there cannot be.** The
Argentine death certificate has no place-of-birth field. CEPAL/CELADE, verbatim:

> "las estadísticas vitales, tienen una limitación esencial: los certificados ya sea de nacimiento o
> de defunción **no incluyen preguntas sobre lugar de nacimiento** (ni del difunto, ni de la madre
> del recién nacido o del nacido muerto). De este modo **no es posible establecer tasas de mortalidad
> específicas** ni tampoco un análisis de las causas de muerte de los inmigrantes en la frontera."
> — Courtis, Liguori & Cerrutti, *Migración y salud en zonas fronterizas*, CEPAL Serie Población y
> Desarrollo N° 93, 2010, p. 12

Factor (a) is therefore necessarily a model applied to a national schedule, with no way to test the
usual healthy-migrant discount. That is a reason to prefer the empirical 80+ ceiling of §4.2 over
the actuarial estimate.

### 4.5 A correction worth recording

An earlier working version of this note put 425.916 people outside the census's private-dwelling
universe. **That figure came from the *provisional* January 2023 count (46.044.703) and is
superseded.** The definitive census total is **45.892.285** = 45.618.787 private dwellings +
267.793 collective dwellings + 5.705 *en situación de calle*. The correct figure is **273.498**, and
factor (g) is scaled accordingly.

Note also a universe mismatch in the report's own 2010-vs-2022 comparison: the 2010 census figure of
1.805.957 is over the **total** population including collective dwellings, whereas 1.933.463 is
private dwellings only. The report compares the two without flagging it.

---

## 5. Published comparisons of the two figures

### 5.1 The one direct comparison

**Ameijeiras, Analía (2025). "Estimación del saldo migratorio internacional 2001–2022 en la
Argentina: alcances y desafíos."** XVIII Jornadas Argentinas de Estudios de Población / V Congreso
Internacional de Población del Cono Sur, AEPA, Córdoba, 23–26 September 2025. Author affiliation
**INDEC – CONICET**, Programa de Análisis Demográfico. https://www.aacademica.org/xviii.jornadas.aepa/17.pdf

This is the conference version of the work behind INDEC's official AD39 projections, and it is the
best available citation. The key sentence:

> "La cantidad de inmigrantes declarados en el Censo 2022 no coincide, y tiene francas distancias,
> con la estimación realizada por RENAPER en base a la emisión de DNI a personas extranjeras
> (DNP, 2022)."

On why the register may over-count — the passage quoted in §2.2 and §2.3 about death-removal
inconsistencies and foreigners exiting on non-DNI documents.

On the pattern, which matches §4.0 exactly:

> "Los países de origen con mayores diferencias relativas son Bolivia, Colombia y Brasil, con casi
> el doble o más de registros en la base de RENAPER. Países como Chile, Uruguay, Italia y Venezuela
> presenta las menores diferencias. En el caso de Venezuela puede responder a una llegada reciente
> de extranjeros de esa nacionalidad al país, lo cual podría estar evadiendo el problema de
> registros de salida del país o fallecimiento. En el caso de los otros países, a diferencia del
> caso venezolano, es una inmigración antigua, por lo que los registros puede que hayan tenido pocos
> cambios en los últimos años."

And the conclusion, which is that the two sources agree on *structure* while disagreeing on *level*:

> "A pesar de las diferencias significativas en términos cuantitativos, se observaron algunas
> similitudes en las tendencias migratorias. Esto también ocurre en términos de estructura por edad
> y sexo de la población migrante."

**Two cautions on citing her Cuadro 1.** First, its totals (Censo 1.815.434 / RENAPER 2.723.045) are
**selected countries only**, not the national totals — do not quote them as 1.933.463 and 3.033.786.
Second, its RENAPER row for **Perú reads 236.929**, whereas Tabla 1 of the source report gives
**289.430**; the discrepancy is unexplained and the DNP figure should be preferred.

### 5.2 The peer-reviewed methodological treatment

**Ameijeiras, Analía (2024). "Los registros administrativos en la medición de las migraciones en la
Argentina: desafíos y limitaciones de los métodos y fuentes disponibles."** *SaberEs* 16(2):211–228.
https://saberes.unr.edu.ar/index.php/revista/article/view/292

Restates the DNP method precisely, and supplies the ENMA anchor used in factor (e):

> "solo incluye a las personas que tienen su situación de residencia regularizada. Sobre esto, la
> Encuesta Nacional Migrante de Argentina (ENMA) en su Anuario Migratorio Argentino 2020 […]
> registra que **un 11% de las personas migrantes encuestadas no cuentan con DNI**. Este porcentaje
> se incrementa entre las personas de origen extra Mercosur no europeo, con una fuerte concentración
> en personas provenientes de Haití y Senegal."

### 5.3 ENMA chose the register over the census — for sampling, not for level

The ENMA team (RIOSP-DDHH / CONICET) compared RENAPER 2022, EPH and the censuses when designing
their 2023 sample, and picked the register for quotas while flagging exactly the two biases in
§4.1:

> "las estimaciones del RENAPER para el año 2022 se realizaron a partir de las solicitudes de DNI,
> por lo tanto, las comunidades que tengan una mayor propensión a realizar la solicitud podrían
> estar sobreestimadas, mientras que no se cuenta con información de la población migrante en
> situación documentaria irregular o que aún no cuenta con DNI con trámite digital."
> — *Documento metodológico ENMA 2023*, June 2023

Their *Anuario Estadístico Migratorio de la Argentina 2023* carries a four-source comparison chart
(Gráfico A.1: RENAPER 2022 / EPH 2017–2022 / EPH 2022 / Censo 2022). Their final calibration used
**the census for nationality weights and RENAPER for sex, age and territory** — an implicit
verdict that the register's *level* is not trustworthy but its *structure* is.

### 5.4 The census-side silence

- **INDEC, *CNPHV 2022. Migraciones internacionales e internas* (April 2024)** — the definitive
  migration volume, 109 pages. It mentions RENAPER **zero times**, and contains no discussion of
  administrative records, omission or under-registration. It reports 1.933.463 with no external
  comparison.
- **INDEC, AD39 (October 2025)** confirms it *ingested* a RENAPER extract — *"Registro Nacional de
  las Personas (Renaper): base de personas documentadas … por provincia de residencia, sexo, edad y
  país de nacimiento al mes de mayo de 2022"*, and that administrative records were used "para la
  estimación de migrantes" — but publishes no resulting migrant coverage figure.
- **The DNP has never revisited its figure.** Its later publications still cite the 2022 register
  report as the migrant benchmark. No post-census statement addresses the discrepancy.
- **OIM Argentina**, *Migraciones Internacionales. Reflexiones desde Argentina* N° 10 (Dec 2024), a
  110-page special issue devoted to reading the 2022 census with a migration lens, does **not**
  compare the totals.
- **Chequeado**, "Censo 2022: qué datos se informaron sobre las migraciones" (17 Jan 2024, updated
  16 Mar 2024) — verified in full: RENAPER is never mentioned and 3.033.786 does not appear. The
  only trace of the question is an unanswered reader comment asking what share of foreigners go
  unregistered.
- **CEPAL/CELADE** flags a 2022 census data-quality problem, but for *internal* migration only.

### 5.5 The only press treatment

*Infobae*, 4 January 2026 (Sandra Crucianelli), places the two side by side without reconciling
them:

> "Según el RENAPER en Argentina hay 2.349.816 extranjeros residiendo en el país, con datos a junio
> pasado. […] La cifra de este año es ligeramente superior a la reportada por el INDEC para 2022,
> cuando el censo de ese año contabilizó 1.933.463 personas en viviendas particulares de la
> Argentina nacidas en otro país."

Note what has happened by then: the register's own figure has fallen close enough to the census that
a journalist can call it "ligeramente superior". The August 2022 figure of 3.033.786 is the outlier
in RENAPER's own series.

### 5.6 Two international bodies have already switched sides

Neither is framed as a comparison, but both are one in substance.

**UN DESA revised Argentina down to the census.** Its *International Migrant Stock 2020* revision put
Argentina at **2.281.728** at mid-2020, a value extrapolated off the 2010 census. The **2024
revision** (released January 2025) reassessed Argentina in full — it is one of only 60 countries
given a full reassessment rather than an extrapolation, driven by the 2022 census — and restated the
same mid-2020 figure as **1.912.294**, a downward revision of **369.434 (−16,2%)**, with mid-2024 at
**1.958.039**. The international benchmark now sits beside the census, not the register.

**R4V dropped the RENAPER figure for Venezuelans and said so.** Its end-2022 Argentina stock of
**220.595** was not an independent estimate: it *was* the RENAPER number, adopted verbatim —
*"La cifra refiere a personas venezolanas con DNI conforme al Decreto Nº 1501/2009, que residían en
el país al mes de agosto 2022"*, with the rider *"no incluye a personas sin DNI"*. In May 2024 R4V
replaced it:

> "Based on census data and official data on entries to and exits from the country, it is estimated
> that **as of September 2023, the Venezuelan population in the country amounted to 164,230
> persons**. Following the publication of census data, **it supersedes the previously used source**
> for the determination of the 'stock' of Venezuelan refugees and migrants (RENAPER)… Reasons for
> the difference between the number of Venezuelan individuals reflected in the census, versus the
> figure that was previously published by RENAPER (**−59,000**), are being explored."

So an agency that had adopted the register as its own source formally superseded it with the census,
and recorded the −59.000 discrepancy as unexplained. Venezuela is the *least* inflated large origin
in §4.0 (adjusted ratio 1,24); the same operation on Paraguay or Bolivia would be far larger.

---

## 6. What could not be established

Listed so that nothing here is mistaken for a settled fact.

**In the report itself**

1. **How, or whether, deceased persons are removed.** The report asserts "personas vivas" and
   describes no method, no linkage and no cut-off. §2.3 reconstructs the statutory circuit from
   outside sources; the report supports none of it.
2. **How many records the six-month DNM filter removed.** 3.033.786 is the post-filter figure only.
   No before-and-after count, no match rate, no sensitivity analysis is published.
3. **Whether naturalized Argentines born abroad are in the count.** The words "naturalizado",
   "nacionalizado" and "ciudadanía" appear zero times, and the report equivocates between
   "nacidas en el exterior" (birthplace) and "de origen extranjero" / "País de origen" (§2.5).
4. **Any province-level counts.** Tabla 2 is regional and percentage-only; the maps carry no legible
   values; the underlying jurisdiction table is not published in the report. (Province-level data
   *are* available in the later open data — §3.2.)
5. **Any age-group table, sex-by-age table, year of DNI issue or year of arrival.** None exists. The
   age structure in this note was recovered by digitizing a chart image (§1.5).
6. **The two internal inconsistencies** at §1.7 (Bolivia 59,9% vs 56,9%; Brasil 70,0% vs 70,7%)
   cannot be resolved on internal evidence.

**In the wider record**

7. **The reason for the 18,6% fall in the series between August 2022 and August 2024.** No
   methodological note exists from RENAPER or the DNP. The age pattern of the drop points at a
   residence-filter revision (§3.3), but that is inference.
8. **Any count of deceased persons remaining in the RENAPER base or the electoral roll.** No audit,
   no official figure, no published estimate. The Cámara Nacional Electoral has spoken only
   qualitatively to the press. **Do not attribute a number to anyone.**
9. **Any migrant-specific census omission rate for 2022.** None has ever been published. INDEC
   explicitly declines to compute a comparable omission rate at all for 2022 and substitutes net
   population differentials. Calvelo (2011) supplies the direction, not a number.
10. **Whether *precaria* holders receive a DNI.** No official page says in so many words that they
    do not; §2.4's conclusion is an inference from four converging texts, and two official RENAPER
    documents are internally inconsistent on the point.
11. **How stale DNI domiciles actually are.** No study, audit or official estimate exists. §2.6
    establishes only the legal ceiling (15 years for an adult, unbounded above 70) and that the
    datum is never verified.
12. **How DNM's exit records handle unrecorded land departures** to Bolivia, Paraguay and Brazil,
    or departures predating mature biometric exit control. This is a live question for the two
    largest origin groups (Paraguay 29,67%, Bolivia 21,71%) and no source addresses it.
13. **The primary source for the January 2023 figure of 3.007.251.** Found only in a secondary
    citation (CIC-PBA). Use with caution or drop it.
14. **Any DNM statistical publication or open data for 2024–2025.** DNM has no presence on
    datos.gob.ar and its old statistics path did not survive the move to the Ministerio de Seguridad.
15. **Live dashboard totals at `estadisticas.renaper.gob.ar`.** These are R/Shiny apps rendering
    over websocket and cannot be read as text; the open-data CSVs were used instead.
16. **The foreign-born count in the 2022 census's collective dwellings.** INDEC asked place of birth
    on the collective-dwelling questionnaire (qq. 12 and 14) but never published the result, and the
    public Redatam collective base exposes only sex and age. So 1.933.463 is a lower bound whose
    deficit is bounded above by 273.498 and otherwise unmeasured — and 30,6% of collective residents
    are in geriatric homes, where the foreign-born are likely over-represented.
17. **Mortality of the foreign-born.** Not measured and not measurable: the Argentine death
    certificate carries no place-of-birth field (§4.4). Factor (a) is necessarily modelled.
18. **DNM resident vs non-resident entry/exit split for 2019–2024.** Discontinued after 2018, so the
    published balances (e.g. +519.214 for foreigners in 2022) count *movements*, not persons, and
    cannot be netted into a stock.
19. **Annual values for INDEC's modelled foreign-born emigration.** Ameijeiras (2025) estimates the
    series by survival ratios off successive censuses but publishes it only as an unlabelled bar
    chart; the axis implies low tens of thousands per year at its 2015–2019 peak. Do not quote a year.
20. **Beneficiary counts for the recent regularization regimes** — Disp. DNM 1891/2021 (Venezuelan
    minors), 940/2022 (Senegal), 941/2022 (CARICOM, Dominican Republic, Cuba), 388/2024. None
    published. Two citation corrections: there is no "Disposición DNM 520/2021" of the kind
    sometimes cited (520/2019 is the Venezuelan assistance programme), and the Senegalese regime is
    **940**/2022, not 941.

**One error found in a secondary source.** Ameijeiras (2025) Cuadro 1 gives RENAPER's Peru figure as
**236.929**; the source report's Tabla 1 gives **289.430**. Prefer the DNP figure. Her Cuadro 1
totals are also selected-countries-only and must not be quoted as national totals (§5.1).

**One premise correction.** The DNI renewal schedule is not "5 and 8 years" or "14 years" as
intervals. Decreto 1501/2009 art. 5 sets updates *at ages* 5–8 and 16, then a 15-year document
validity, obligatory only to age 70 (75 in RENAPER's guidance for foreigners). See §2.6.

---

## 7. Bottom line

1. **The report publishes two tables, not the six the brief assumed.** Age, sex, province and
   arrival-date breakdowns do not exist in it. What could be recovered has been, by digitizing chart
   images with stated and validated error (§1.5, §1.6).

2. **The 3.033.786 figure is a count of digital-DNI records not known to be dead and not known to
   have been abroad for six months.** Each of those three clauses is a record-keeping state, not an
   observation about a person. §2 documents every one of them verbatim.

3. **The gap with the census is a residence problem, not a mortality problem.** The excess is
   concentrated at ages 25–44 (ratio up to 2,00) and thinnest among the old (1,14–1,35 above 75) and
   among Italians (1,18 adjusted). Unpurged deaths would produce the exact opposite pattern, and the
   80+ cell caps them at about 120.000 — at most 11% of the 1.100.323 gap.

4. **Between roughly 740.000 and 1.540.000 of the August 2022 records were for people not resident
   in Argentina**, most plausibly ~1.155.000. The mechanism is documented: the DNM filter deletes
   only recorded absences; foreigners frequently exit on non-Argentine documents and go unmatched;
   and a foreign national's DNI cannot carry a foreign address and cannot be updated from abroad, so
   emigrants remain geolocated in Argentina by construction.

5. **RENAPER's own later figures no longer support 3.033.786.** The same series on the same
   definition reports 2.470.453 (Aug 2024) and 2.349.816 (Jun 2025) — 684.000 fewer, removed
   disproportionately from working ages, with no published explanation. **Do not plot 2022 and 2024+
   as one series.**

6. **Two factors run the other way and are routinely forgotten.** The digital-DNI-only rule drops
   elderly holders of pre-2009 documents, and the register cannot see migrants without a DNI at all
   — 11% of ENMA respondents in 2020, 7% in 2023, and about half of them legally *regular*
   (precarios and temporarios awaiting the document). It reaches 13,5% among extra-MERCOSUR
   non-Europeans and 24% in the NOA. For work on informal settlement or on precarious migrant
   populations, this exclusion is the one that bites, and the register cannot correct it.

7. **The reference-date difference is worth −1.129 people.** It explains nothing.

8. **Two international bodies have already chosen the census over the register.** UN DESA's 2024
   revision cut its Argentina series by 16,2% — restating mid-2020 from 2.281.728 to 1.912.294 — on
   the strength of the 2022 census, and R4V formally superseded RENAPER as its source for
   Venezuelans, recording the −59.000 difference as unexplained (§5.6).

9. **If a single foreign-born figure for mid-2022 is needed, the census figure is the better
   starting point**, adjusted upward for the collective-dwelling universe (+12.000 to +45.000) and
   for probable under-enumeration of migrant men (+10.000 to +250.000) — i.e. roughly **1,96–2,23
   million**. That brackets UN DESA's revised 1.912.294 for mid-2020 and 1.958.039 for mid-2024. The
   register's value is its *structure* — by country, age, sex and territory — which ENMA's
   calibration choice independently endorses, and which agrees with the census even where the levels
   do not.
