# Argentina Census 2022 — foreign-born population by country of birth

Reference note for comparing the census count of the foreign-born with an
administrative register (RENAPER / DNM residence permits). Everything below is
sourced from INDEC's definitive-results publications; page numbers refer to the
printed page numbers on the PDF pages, and file names refer to the copies listed
under "Sources and local copies" at the end.

Census reference date: **18 May 2022** (Decreto 42/22 declared that day a national
holiday and the Census day). The digital self-enumeration window opened 16 March
2022; the collective-dwelling operation ran 17 May 2022; the street-population
operation ran the night of 16 May 2022.

---

## 1. Headline numbers and the three universes

The 2022 census enumerated three separate populations. Place of birth is
**published only for the private-dwelling population**.

| Universe | Persons | Women | Men | Place of birth published? |
|---|---:|---:|---:|---|
| Total population | 45,892,285 | 23,705,494 | 22,186,791 | no |
| Population in private dwellings (*viviendas particulares*) | 45,618,787 | 23,607,906 | 22,010,881 | **yes** |
| Population in collective dwellings (*viviendas colectivas*) (¹) | 267,793 | 96,357 | 171,436 | **no** |
| Population in street situation (*situación de calle*) (²) | 5,705 | 1,231 | 4,474 | **no** |

(¹) Excludes people enumerated in shelters/*paradores*, who are counted with the
street population. (²) Includes people in shelters/*paradores*.

Source: *Base de datos REDATAM — Control de universos*, "Cuadro control de
universos 3", p. 5 (`Redatam_control_de_universos.pdf`); identical figures in
`c2022_tp_c_resumen.xlsx`, sheet `cuadro_resumen`, and in
`censo2022_viviendas_colectivas.pdf` pp. 11 and 13.

**Foreign-born, private dwellings only:**

| | Persons |
|---|---:|
| Born in another country | **1,933,463** |
| — women/female | 1,061,421 |
| — men/male | 872,042 |
| Share of private-dwelling population | 4.2% |
| Of which country of birth *Ignorado* (not stated) | 179,239 (9.27%) |

Source: `censo2022_migraciones.pdf` p. 9 (infographic) and p. 27 (Cuadro
"Población en viviendas particulares por lugar de nacimiento, según
jurisdicción"); web table `c2022_tp_migraciones_c10.xlsx`, Cuadro 10.

Complementary counts in the same universe (p. 27): born in the province of
enumeration 36,772,721; born in another Argentine province 6,912,603.

### Is there a foreign-born total including collective dwellings?

**No — INDEC does not publish one.** Checked and not found in:

* `censo2022_migraciones.pdf` (Edición ampliada, April 2024) — every table and
  graph is explicitly restricted to *población en viviendas particulares*.
* `censo2022_viviendas_colectivas.pdf` (*Viviendas colectivas y personas en
  situación de calle*) — the only breakdowns are by type of collective dwelling,
  five-year age group, sex and jurisdiction. No place-of-birth table.
* The 15 open-format national web tables `c2022_tp_migraciones_c1..c15.xlsx` —
  all in the private-dwelling universe.
* The `censo.gob.ar` collective-dwellings section — no downloadable tables.

The data nevertheless **exists in the microdata**: the collective-dwelling
questionnaire asked place of birth (Q12/Q14) and year of arrival (Q15), and the
REDATAM database carries the collective-dwelling and street populations (at
department level only, for statistical-secrecy reasons — Ley 17.622). So a
foreign-born count including collective dwellings is derivable from REDATAM
(`redatam.indec.gob.ar`, BASE=CPV2022) but has never been published by INDEC.

For the street population, INDEC states that "dado el nivel de respuesta del
operativo especial realizado sobre la población en situación de calle, solo se
expone la información de la variable sexo registrado al nacer"
(`Redatam_aspectos_metodologicos.pdf`, p. 10) — i.e. place of birth is not
disseminated for that group at all.

**Practical upper bound.** If the 273,498 people outside private dwellings had
the same 4.24% foreign-born rate as the private-dwelling population, the total
foreign-born would be about 1,945,000 — a difference of roughly 0.6%. Prisons and
geriatric homes (70.6% of the collective-dwelling population) plausibly deviate
from that rate, so treat this only as an order-of-magnitude adjustment.

---

## 2. Foreign-born by country of birth

Full machine-readable list (205 categories, summing exactly to 1,933,463) in
`census2022_foreign_born_by_country.csv`.

* **Universe:** population in private dwellings.
* **Source table:** Cuadro 10. *Total del país. Población en viviendas
  particulares nacida en otro país, por lugar de nacimiento, según sexo
  registrado al nacer y jurisdicción. Año 2022* — web table
  `c2022_tp_migraciones_c10.xlsx` (this full country list is **not** printed in
  the PDF; the PDF prints only the top 30 on p. 13).
* National sex split is not a column of Cuadro 10; it is the sum of the 24
  jurisdiction columns, and it reproduces the published 1,061,421 / 872,042
  exactly (column `check_sum_jurisdictions` in the CSV verifies the row totals).

Top 36 of 205 categories:

| Country of birth | Continent | Persons | Women | Men | % of foreign-born |
|---|---|---:|---:|---:|---:|
| Paraguay | América | 522,598 | 298,850 | 223,748 | 27.03 |
| Bolivia | América | 338,299 | 177,186 | 161,113 | 17.50 |
| *IGNORADO (not stated)* | Otros | 179,239 | 97,275 | 81,964 | 9.27 |
| Venezuela | América | 161,495 | 85,118 | 76,377 | 8.35 |
| Perú | América | 156,251 | 85,768 | 70,483 | 8.08 |
| Chile | América | 149,082 | 83,659 | 65,423 | 7.71 |
| Uruguay | América | 95,384 | 51,409 | 43,975 | 4.93 |
| Italia | Europa | 68,169 | 39,474 | 28,695 | 3.53 |
| Brasil | América | 49,943 | 30,520 | 19,423 | 2.58 |
| España | Europa | 48,492 | 27,550 | 20,942 | 2.51 |
| Colombia | América | 46,482 | 24,399 | 22,083 | 2.40 |
| China | Asia | 18,629 | 8,543 | 10,086 | 0.96 |
| Estados Unidos | América | 13,986 | 6,846 | 7,140 | 0.72 |
| Ecuador | América | 8,879 | 4,862 | 4,017 | 0.46 |
| República Dominicana | América | 7,817 | 5,031 | 2,786 | 0.40 |
| México | América | 5,833 | 3,116 | 2,717 | 0.30 |
| Corea | Asia | 5,337 | 2,743 | 2,594 | 0.28 |
| Alemania | Europa | 4,087 | 2,179 | 1,908 | 0.21 |
| Francia | Europa | 3,960 | 1,945 | 2,015 | 0.20 |
| Cuba | América | 3,921 | 1,744 | 2,177 | 0.20 |
| Ucrania | Europa | 3,486 | 2,034 | 1,452 | 0.18 |
| Portugal | Europa | 3,281 | 1,778 | 1,503 | 0.17 |
| Taiwán | Asia | 3,018 | 1,551 | 1,467 | 0.16 |
| Japón | Asia | 2,703 | 1,436 | 1,267 | 0.14 |
| Rusia | Europa | 2,169 | 1,306 | 863 | 0.11 |
| Reino Unido de Gran Bretaña e Irlanda del Norte | Europa | 1,840 | 790 | 1,050 | 0.10 |
| Haití | América | 1,524 | 643 | 881 | 0.08 |
| Polonia | Europa | 1,408 | 927 | 481 | 0.07 |
| Israel | Asia | 1,394 | 695 | 699 | 0.07 |
| Canadá | América | 1,377 | 708 | 669 | 0.07 |
| Siria | Asia | 1,324 | 558 | 766 | 0.07 |
| Suiza | Europa | 1,139 | 559 | 580 | 0.06 |
| Senegal | África | 1,120 | 79 | 1,041 | 0.06 |
| Armenia | Asia | 862 | 435 | 427 | 0.04 |
| El Salvador | América | 830 | 433 | 397 | 0.04 |
| Costa Rica | América | 706 | 365 | 341 | 0.04 |

The country list also carries five residual codes that matter when reconciling
with a register: `Indeterminado (América)` 171, `Indeterminado (África)` 127,
`Indeterminado (Europa)` 100, `Indeterminado ( Asia )` 23,
`Indeterminado (Oceanía)` 2, plus `Ex Unión Soviética` 32 and the large
`IGNORADO` 179,239.

### Aggregated groupings ("resto" categories)

The published aggregates, which is the level at which the PDF and most tables
report (Cuadro 3, `c2022_tp_migraciones_c3.xlsx`, and PDF p. 28):

| Group | Persons | % of foreign-born |
|---|---:|---:|
| América — total | 1,567,110 | 81.05 |
| — Países limítrofes (BO, BR, CL, PY, UY) | 1,155,306 | 59.75 |
| — Países no limítrofes de América | 411,804 | 21.30 |
| — — Resto de América | 47,576 | 2.46 |
| Europa — total | 145,808 | 7.54 |
| — Resto de Europa | 29,147 | 1.51 |
| Asia | 37,342 | 1.93 |
| África | 3,243 | 0.17 |
| Oceanía | 721 | 0.04 |
| Ignorado | 179,239 | 9.27 |

Printed percentage distribution (PDF p. 13, Gráfico 6): Paraguay 27.0, Bolivia
17.5, Venezuela 8.4, Perú 8.1, Chile 7.7, Uruguay 4.9, Brasil 2.6, Colombia 2.4,
Resto de América 2.5, Italia 3.5, España 2.5, Resto de Europa 1.5, Asia 1.9,
África y Oceanía 0.2, Ignorado 9.3.

---

## 3. Other breakdowns (separate CSVs)

| File | Content | Source table |
|---|---|---|
| `census2022_foreign_born_by_country.csv` | 205 countries × persons/women/men, national | Cuadro 10 (`c10.xlsx`) |
| `census2022_foreign_born_by_country_jurisdiction.csv.gz` | 205 countries × 24 jurisdictions × total/women/men (long format, 4,944 rows) | Cuadro 10 (`c10.xlsx`) |
| `census2022_foreign_born_by_country_age.csv` | 205 countries × 19 five-year age groups | Cuadro 11 (`c11.xlsx`) |
| `census2022_foreign_born_by_sex_and_agegroup.csv` | 21 country groups × sex × broad age (0-14, 15-24, 25-64, 65+) | Cuadro 3 (`c3.xlsx`) |
| `census2022_foreign_born_by_year_of_arrival.csv` | 21 country groups × 8 arrival periods | Cuadro 13 (`c13.xlsx`) |
| `census2022_population_by_jurisdiction_birthplace.csv` | 24 jurisdictions + GBA split × birthplace (this province / other province / other country) | Cuadro 1 (`c1.xlsx`), PDF p. 27 |

### Year of arrival, national (Cuadro 13, finer than the printed version)

The PDF (p. 28) prints only five periods (Hasta 1999 / 2000-2009 / 2010-2019 /
2020-2022 / Ignorado). The web table gives eight:

| Lugar de nacimiento | Total | Hasta 1989 | 1990-1999 | 2000-2004 | 2005-2009 | 2010-2014 | 2015-2019 | 2020-2022 | Ignorado |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Total** | 1,933,463 | 476,082 | 184,776 | 120,297 | 214,705 | 175,909 | 255,262 | 62,667 | 443,765 |
| Bolivia | 338,299 | 62,993 | 50,196 | 31,388 | 51,391 | 36,627 | 26,301 | 6,433 | 72,970 |
| Brasil | 49,943 | 9,699 | 3,680 | 1,931 | 2,588 | 4,297 | 12,478 | 7,435 | 7,835 |
| Chile | 149,082 | 101,454 | 9,759 | 2,129 | 3,198 | 3,271 | 3,513 | 2,205 | 23,553 |
| Paraguay | 522,598 | 108,631 | 59,981 | 49,779 | 97,167 | 60,809 | 34,035 | 8,058 | 104,138 |
| Uruguay | 95,384 | 57,528 | 6,713 | 2,912 | 3,407 | 2,826 | 2,932 | 1,098 | 17,968 |
| Colombia | 46,482 | 883 | 746 | 744 | 3,211 | 11,478 | 15,422 | 4,525 | 9,473 |
| Perú | 156,251 | 7,176 | 33,526 | 18,459 | 28,993 | 23,336 | 13,978 | 4,192 | 26,591 |
| Venezuela | 161,495 | 1,280 | 586 | 412 | 1,340 | 5,627 | 118,421 | 17,982 | 15,847 |
| España | 48,492 | 31,151 | 1,193 | 670 | 2,864 | 4,851 | 1,642 | 688 | 5,433 |
| Italia | 68,169 | 54,722 | 1,288 | 347 | 1,034 | 1,237 | 662 | 264 | 8,615 |
| Ignorado | 179,239 | 13,535 | 5,648 | 3,585 | 5,951 | 6,618 | 7,007 | 2,285 | 134,610 |

**Caveat carried by INDEC on the year-of-arrival tables** (PDF p. 28, and every
jurisdiction table X.2), verbatim:

> Nota: No incluye hogares donde la única persona migrante es servicio doméstico
> o sus familiares

(The row totals nevertheless reproduce the published country totals exactly, so
the exclusion appears to affect only the arrival-year distribution's provenance,
not the count. Flag this if the arrival-year distribution is load-bearing.)

Note also the very large **Ignorado year of arrival: 443,765 (23.0%)**, of which
134,610 also have unknown country of birth.

### By jurisdiction of residence (PDF p. 27, Cuadro 1)

| Jurisdiction | Pop. in private dwellings | Born abroad | % foreign-born | % of all foreign-born |
|---|---:|---:|---:|---:|
| Total del país | 45,618,787 | 1,933,463 | 4.24 | 100.0 |
| Buenos Aires | 17,408,906 | 994,653 | 5.71 | 51.4 |
| — 24 partidos del Gran Buenos Aires | 10,801,336 | 740,355 | 6.85 | 38.3 |
| — Resto de Buenos Aires | 6,607,570 | 254,298 | 3.85 | 13.2 |
| Ciudad Autónoma de Buenos Aires | 3,095,454 | 419,091 | 13.54 | 21.7 |
| Mendoza | 2,030,773 | 66,590 | 3.28 | 3.4 |
| Córdoba | 3,812,064 | 65,703 | 1.72 | 3.4 |
| Santa Fe | 3,519,059 | 48,862 | 1.39 | 2.5 |
| Río Negro | 747,697 | 40,826 | 5.46 | 2.1 |
| Neuquén | 708,578 | 39,367 | 5.56 | 2.0 |
| Misiones | 1,273,347 | 39,027 | 3.06 | 2.0 |
| Jujuy | 809,364 | 30,317 | 3.75 | 1.6 |
| Salta | 1,434,225 | 29,497 | 2.06 | 1.5 |
| Chubut | 589,454 | 28,976 | 4.92 | 1.5 |
| Santa Cruz | 335,677 | 22,111 | 6.59 | 1.1 |
| Formosa | 605,507 | 17,108 | 2.83 | 0.9 |
| Entre Ríos | 1,415,097 | 14,354 | 1.01 | 0.7 |
| Corrientes | 1,209,671 | 13,153 | 1.09 | 0.7 |
| Tucumán | 1,727,337 | 12,325 | 0.71 | 0.6 |
| Tierra del Fuego, Antártida e Islas del Atlántico Sur | 184,958 | 12,251 | 6.62 | 0.6 |
| San Juan | 819,445 | 8,260 | 1.01 | 0.4 |
| San Luis | 540,548 | 8,219 | 1.52 | 0.4 |
| Chaco | 1,124,603 | 5,989 | 0.53 | 0.3 |
| La Rioja | 382,453 | 5,772 | 1.51 | 0.3 |
| Santiago del Estero | 1,057,752 | 5,280 | 0.50 | 0.3 |
| La Pampa | 359,193 | 3,501 | 0.97 | 0.2 |
| Catamarca | 427,625 | 2,231 | 0.52 | 0.1 |

Country × jurisdiction detail (the register comparison's most useful cut) is in
`census2022_foreign_born_by_country_jurisdiction.csv.gz`.

---

## 4. Census definitions, verbatim

### 4.1 De jure census / habitual residence

> Finalmente, cabe recordar que el Censo 2022, por primera vez en la historia de
> los censos de población argentinos, empleó la metodología de censo de derecho,
> por la cual las personas se contabilizaron en su lugar de residencia habitual,
> es decir, en el que pasan la mayor parte del tiempo durante la semana.

— `censo2022_migraciones.pdf`, p. 7 (Introducción).

> Por primera vez en la historia de los censos argentinos, el Censo Nacional de
> Población, Hogares y Viviendas 2022 (Censo 2022) se llevó a cabo de acuerdo con
> la definición de censo de derecho; esto es, contó a las personas según su lugar
> de residencia habitual, donde viven la mayor parte del tiempo.
>
> Censar a la población bajo esta definición contribuye a precisar el diseño de
> las políticas públicas en relación con la demanda de servicios, la atención de
> la salud y la educación, entre otras. Además, proporciona una mayor oportunidad
> de integración con las encuestas a hogares y su asimilación con los registros
> administrativos que utilizan también el criterio de residencia habitual de la
> población.

— `Redatam_aspectos_metodologicos.pdf`, section 3 "Metodología", p. 5.

Glossary definition:

> **Residencia habitual**
> Lugar donde el censado reside habitualmente la mayor parte del tiempo, o el
> lugar donde esté decidido a fijar su residencia.

— `censo2022_migraciones.pdf`, p. 104 (Glosario).

Operationalised on the form as questions 3 and 8 of the private-dwelling
questionnaire:

> 3 ¿Cuántas personas viven la mayor parte del tiempo en esta vivienda?
> 8 ¿Cuáles son los nombres de las personas de este hogar que viven la mayor
> parte del tiempo en esta vivienda?

— `Censo2022_cuestionario_viviendas_particulares_impresion.pdf`.

### 4.2 Treatment of persons abroad

There is **no question about absent household members living abroad**, and no
emigration module. The census enumerates only people whose habitual residence is
in Argentina on 18 May 2022; Argentine residents (native or foreign-born) who had
moved abroad are simply out of scope, and the census produces no emigrant count.
The only proxy is Q17 *¿Hace 5 años vivía en… otro país?* (variable P17), which
identifies people **now** resident in Argentina who lived abroad in 2017 — this
includes returning Argentines as well as recent immigrants.

Two consequences for a register comparison:
* Foreign nationals who hold a valid Argentine residence permit but had left the
  country by May 2022 are in the register and absent from the census.
* Foreign nationals present in Argentina only temporarily (tourists, short stays,
  people not living "la mayor parte del tiempo" at the address) are excluded by
  design, even where they appear in an entry/permit register.

### 4.3 Nationality / naturalisation — NOT ASKED

Neither questionnaire contains a nationality, citizenship or naturalisation
question. `grep -i nacionalidad` and `grep -i naturaliz` return zero hits in
`Censo2022_cuestionario_viviendas_particulares_impresion.pdf`,
`Censo2022_cuestionario_viviendas_colectivas.pdf` and
`censo2022_migraciones.pdf`. The census measures **country of birth only**.

This is the single largest conceptual gap against an administrative register:
* Foreign-born people who have naturalised as Argentine are counted as
  foreign-born by the census but are (usually) no longer in a foreigners'
  residence register.
* Argentine-born children of immigrants are natives for the census and absent
  from a foreigners' register — and vice versa, foreign nationals born in
  Argentina do not exist as a census category.

### 4.4 "Lugar de nacimiento" — exact question wording

Private-dwelling questionnaire, questions 13-16 (reproduced in
`censo2022_migraciones.pdf`, p. 8):

> **13 ¿Nació en…**
> esta provincia? 1 → *Pase a 17*
> otra provincia argentina? 2
> otro país? 3 → *Pase a 15*
>
> **14 ¿En qué provincia?** CABA refiere a Ciudad Autónoma de Buenos Aires y
> Tierra del Fuego refiere a Tierra del Fuego, Antártida e Islas del Atlántico
> Sur. [24 pre-coded jurisdictions] → *Pase a 17*
>
> **15 ¿En qué país?**
> Bolivia 1 · Brasil 2 · Chile 3 · Colombia 4 · Paraguay 5 · Perú 6 · Uruguay 7 ·
> Venezuela 8 · Otro país 9
> *Si responde Otro país, escriba el nombre del país.*
>
> **16 ¿En qué año llegó a la Argentina?**
> Año: ____   Ignorado 9999
>
> **17 ¿Hace 5 años vivía en…**
> esta localidad o paraje? 1 → *Pase a 19*
> otra localidad o paraje de esta provincia? 2
> otra provincia argentina? 3
> otro país? 4
> No había nacido 5 → *Pase a 19*

Note the design: only **8 countries are pre-coded**; everything else is an open
write-in that had to be coded office-side. That, plus the digital
self-enumeration mode, is the mechanical origin of the 179,239 (9.27%)
*Ignorado* country of birth.

The collective-dwelling questionnaire asks the same items, renumbered: Q12
(*¿Nació en…*), Q13 (province), Q14 (*¿En qué país?*, same 8 pre-codes), Q15
(*¿En qué año llegó a la Argentina?*), Q16 (residence 5 years ago).

### 4.5 Conceptual definitions (glossary, `censo2022_migraciones.pdf` pp. 103-105)

> **Lugar de nacimiento**
> Lugar en el que el censado nació (la provincia en el caso de los nacidos en
> Argentina y el país en el caso de los extranjeros).

> **Migración internacional**
> Cambio de jurisdicción de un país a otro para adoptar una residencia
> definitiva.

> **Migración internacional de toda la vida**
> Cambio de jurisdicción de un país a otro para adoptar una residencia permanente
> en una fecha anterior a 2017.

> **Migración internacional del período**
> Cambio de jurisdicción de un país a otro para adoptar una residencia permanente
> en una fecha posterior a 2017.

> **Condición migratoria**
> Permite clasificar a la población entre no migrante y migrante,
> indistintamente de si es migrante internacional o interno y diferenciar entre
> migración del período o de toda la vida.

Note that INDEC's *condición migratoria* is a demographic classification, **not**
a legal-status classification. The census records nothing about residence
permits, visa category or regularity of stay.

Sex variable caveat, repeated on every table:

> Nota: de acuerdo con la evaluación de calidad y consistencia de los resultados
> definitivos, y para cumplir con los estándares de calidad estadística
> requeridos por el INDEC, la categoría X de las respuestas a la pregunta por
> sexo registrado al nacer se distribuye entre las categorías Mujer/femenino y
> Varón/masculino.

### 4.6 REDATAM variable names (CPV2022)

From *Base de datos REDATAM — Definiciones de la base de datos*
(`Redatam_Definiciones_de_la_base_de_datos.pdf`), section 3 "Variables de
Población", pp. 33-34. Entity: `PERSONA`.

| Variable | Label | Definition (verbatim) |
|---|---|---|
| `P13` | Lugar de nacimiento (p. 33) | "lugar donde vivía habitualmente la persona censada al nacer, y no el lugar físico del establecimiento (hospital, vivienda, etc.) en el que nació." Codes: 1 Esta provincia, 2 Otra provincia argentina, 3 Otro país |
| `P14` | Provincia de nacimiento (p. 33) | "provincia donde, al nacer, vivía habitualmente la persona censada que respondió haber nacido en otra provincia argentina…" |
| `P15` | País de nacimiento (p. 34) | "país en el que vivía habitualmente la persona censada al nacer, y no el lugar físico del establecimiento (hospital, vivienda, etc.) en el que nació." |
| `P16` | Año de llegada a la Argentina (p. 34) | "para la persona que declara haber nacido en otro país, refiere al año en que llegó a la Argentina para establecer residencia definitiva. En caso de que hubiese más de un ingreso, se refiere al último a partir del cual la persona nacida en otro país llegó para establecer residencia definitiva. El código 9999 corresponde a las respuestas que se agrupan bajo la categoría Ignorado." |
| `P17` | Lugar de residencia hace 5 años (p. 34) | "país, provincia, localidad o paraje en donde la persona censada residía habitualmente 5 años antes del momento del Censo." Codes 1-5 as on the form |
| `P18` | Provincia de residencia hace 5 años (p. 34) | — |

**Important:** `P13`/`P15` record *where the person habitually lived at birth*,
not the physical place of the birth event. A register keyed to the birth
certificate's place of issue is therefore not measuring exactly the same thing.

Related derived variables at household (`HOGAR`) level, same document p. 22:
`HOGMIG` (Hogar con al menos un migrante) and `HTOTMIG` (Hogar con migrantes).
Other person variables referenced above: `P02` sexo registrado al nacer, `EDAD`,
`EDADQUI`, `EDADGRU`, `P19` cobertura de salud, `CONDACT` condición de actividad.

### 4.7 Universe definitions (verbatim, `Redatam_Definiciones_de_la_base_de_datos.pdf` p. 4)

> **Viviendas particulares:** viviendas destinadas al alojamiento de uno o más
> hogares en donde las personas viven bajo un régimen de tipo familiar (sean o no
> parientes). Estas viviendas pueden haber sido construidas con fines
> habitacionales o estar adaptadas para alojar personas. Pueden estar habitadas o
> deshabitadas.
>
> **Viviendas colectivas:** viviendas de alojamiento construidas o adaptadas para
> albergar personas de un modo permanente o temporario, sujetas a reglamentos de
> convivencia y comportamiento […] y que al momento del Censo estén ocupadas por
> al menos una persona que resida allí la mayor parte de la semana. Se excluyen
> las viviendas colectivas que estén deshabitadas al momento del Censo.
>
> **Situación de calle:** persona o personas que utilizan un espacio de la vía
> pública (calle, estación de ferrocarril, estación del subterráneo, portal de un
> edificio, plaza, etc.) como lugar de habitación o pernocte, y a las que residen
> en paradores y refugios y fueron relevadas en el operativo de viviendas
> colectivas.

Composition of the collective-dwelling population (`censo2022_viviendas_colectivas.pdf`, p. 9):
prisons 40.0%, geriatric homes 30.6%, health establishments/hospitals 10.7% —
81% of the total between the three.

---

## 5. Comparison with Census 2010

Machine-readable comparison: `census_foreign_born_2010_vs_2022.csv`.

### 5.1 The 2010 headline is NOT the same universe as the 2022 headline

This is the most consequential finding of the comparison, and it is easy to get
wrong (most secondary sources do).

| | 2010 | 2022 |
|---|---:|---:|
| Published foreign-born headline | **1,805,957** | **1,933,463** |
| Universe of that headline | **total population** (private + collective dwellings + street) | **private dwellings only** |
| Census methodology | *censo de hecho* (de facto) | *censo de derecho* (de jure) |
| Foreign-born in collective dwellings | **45,716** (10.4% of the 441,191 there) | not published |
| Approx. like-for-like foreign-born | 1,760,241 (= 1,805,957 − 45,716) | 1,933,463 |

2010 sources: *Censo Nacional de Población, Hogares y Viviendas 2010. Censo del
Bicentenario. Resultados definitivos, Serie B Nº 2*, Tomo 1, Cuadro 1 (PDF p. 91)
and Cuadro 2 (PDF p. 94); Tomo 1 Chapter 9 "Viviendas colectivas", printed p. 266:

> Del total de 441.191 personas censadas en viviendas colectivas, 395.475 son
> argentinos y 45.716 son extranjeros, lo que representa el 10,4%.

Note the 2010 collective-dwelling foreign-born share (10.4%) is inflated by the
de-facto methodology, which counted tourists in hotels and other tourist
accommodation as collective-dwelling residents on census night. The 2022 de-jure
collective-dwelling population (267,793) is a different, much more institutional
population (prisons 40.0%, geriatric homes 30.6%, hospitals 10.7%), so its
foreign-born share is very unlikely to be 10.4%. Do not project the 2010 rate
onto 2022.

The 2010 total-population tables also carry the note:

> Nota: la población total incluye a las personas viviendo en situación de calle.

### 5.2 Change by country, 2010 → 2022

Comparing the two published headlines directly overstates growth by roughly 45,700
(the collective-dwelling term). The per-country deltas below are on the published
figures as issued and inherit that bias; it is small relative to the country-level
movements except for the aggregate total.

| Country / group | 2010 | 2022 | Change | % |
|---|---:|---:|---:|---:|
| **Total** | 1,805,957 | 1,933,463 | +127,506 | +7.1 |
| *Total, like-for-like approx.* | *1,760,241* | *1,933,463* | *+173,222* | *+9.8* |
| Paraguay | 550,713 | 522,598 | −28,115 | −5.1 |
| Bolivia | 345,272 | 338,299 | −6,973 | −2.0 |
| Chile | 191,147 | 149,082 | −42,065 | −22.0 |
| Perú | 157,514 | 156,251 | −1,263 | −0.8 |
| Italia | 147,499 | 68,169 | −79,330 | −53.8 |
| Uruguay | 116,592 | 95,384 | −21,208 | −18.2 |
| España | 94,030 | 48,492 | −45,538 | −48.4 |
| Brasil | 41,330 | 49,943 | +8,613 | +20.8 |
| Alemania | 8,416 | 4,087 | −4,329 | −51.4 |
| China | 8,929 | 18,629 | +9,700 | +108.6 |
| Corea | 7,321 | 5,337 | −1,984 | −27.1 |
| Francia | 6,995 | 3,960 | −3,035 | −43.4 |
| Japón | 4,036 | 2,703 | −1,333 | −33.0 |
| Taiwán | 2,875 | 3,018 | +143 | +5.0 |
| Siria | 1,337 | 1,324 | −13 | −1.0 |
| **Venezuela** | *not published separately* | 161,495 | — | — |
| **Colombia** | *not published separately* | 46,482 | — | — |
| **Ecuador** | *not published separately* | 8,879 | — | — |
| **Ignorado** | *no such category* | 179,239 | — | — |
| América — total | 1,471,399 | 1,567,110 | +95,711 | +6.5 |
| — Países limítrofes | 1,245,054 | 1,155,306 | −89,748 | −7.2 |
| — Países no limítrofes | 226,345 | 411,804 | +185,459 | +81.9 |
| — Resto de América (2010 basis, i.e. incl. VE + CO) | 68,831 | 255,553 | +186,722 | +271.3 |
| Europa — total | 299,394 | 145,808 | −153,586 | −51.3 |
| — Resto de Europa | 42,454 | 29,147 | −13,307 | −31.3 |
| Asia | 31,001 | 37,342 | +6,341 | +20.5 |
| África | 2,738 | 3,243 | +505 | +18.4 |
| Oceanía | 1,425 | 721 | −704 | −49.4 |
| Women | 974,261 (53.9%) | 1,061,421 (54.9%) | +87,160 | +8.9 |
| Men | 831,696 | 872,042 | +40,346 | +4.9 |

### 5.3 Three non-comparabilities that will bite

1. **Venezuela, Colombia and Ecuador have no 2010 baseline.** INDEC's 2010
   country list for the Americas stops at Perú; all three sit inside
   *Resto de América* = 68,831. Verified in both `censo2010_tomo2.pdf`
   (Cuadro P6, PDF pp. 168-169) and the official XLS. Widely circulated figures
   (Colombia 17,576; Venezuela 6,379; Ecuador 4,820) come from third-party
   processing of the 2010 REDATAM microdata, **not** from a published INDEC
   table — do not cite them as INDEC.
2. **2010 has no *Ignorado* category.** The five continents sum exactly to
   1,805,957. Unknown country of birth was absorbed into the "Resto de …"
   residuals. In 2022, *Ignorado* is 179,239 (9.27%) and is reported explicitly.
   Any 2010→2022 country delta is therefore contaminated by up to ~9% of the 2022
   stock that has no country assigned.
3. **De facto → de jure.** 2022 is the first Argentine de-jure census. In 2010,
   people were counted where they spent census night; in 2022, where they live
   most of the time. For a mobile, partly circular migrant population this is a
   real break, not a rounding difference.

Historical series for context (`censo2022_migraciones.pdf` p. 11, Gráfico 2 —
foreign-born as % of the private-dwelling population): 1869 12.1 · 1895 25.4 ·
1914 29.9 · 1947 15.3 · 1960 13.0 · 1970 9.5 · 1980 6.8 · 1991 5.0 · 2001 4.2 ·
2010 4.5 · 2022 4.2.

Total foreign-born by census (2010 Tomo 1, Cuadro 2, PDF p. 94): 1991 1,615,473 ·
2001 1,531,940 · 2010 1,805,957. Same table's country series 1991/2001/2010:
Paraguay 240,450 / 325,046 / 550,713 · Bolivia 143,569 / 233,464 / 345,272 ·
Chile 244,410 / 212,429 / 191,147 · Perú 15,939 / 88,260 / 157,514 ·
Italia 328,113 / 216,718 / 147,499 · Uruguay 133,453 / 117,564 / 116,592 ·
España 224,500 / 134,417 / 94,030 · Brasil 33,476 / 34,712 / 41,330 ·
Resto 251,563 / 169,330 / 161,860.

---

## 6. What this means for comparison against an administrative register

Ordered by expected size of the discrepancy.

1. **Country of birth vs. nationality.** The census has no nationality question at
   all (§4.3). A residence register counts foreign *nationals*; the census counts
   foreign-*born*. Naturalised Argentines stay in the census numerator and drop
   out of the register; Argentine-born foreign nationals do the reverse.
2. **179,239 (9.27%) with country of birth unknown.** Almost half the size of the
   Bolivian stock. Any per-country census-vs-register ratio is biased downward
   unless the *Ignorado* mass is redistributed, and INDEC gives no redistribution.
   A further 443,765 (23.0%) have unknown year of arrival.
3. **Universe.** The census figure excludes 273,498 people in collective dwellings
   and street situations, for whom place of birth was collected but never
   published. Prisons alone are 40% of the collective-dwelling population — a
   group where a register/census gap is substantively interesting and unmeasurable
   from published tables.
4. **De jure residence, not presence and not legal status.** People must live at
   the address "la mayor parte del tiempo". Short-stay foreigners are out; permit
   holders who had emigrated by May 2022 are in the register but not the census.
5. **Only 8 pre-coded countries** on the form; everything else was a hand-written
   country name coded office-side. Expect coding noise in the smaller countries
   and in the *Ignorado* residual.
6. **Reference date 18 May 2022** — a register snapshot must be aligned to it, and
   the 62,667 arrivals recorded for 2020-2022 show the tail is thin and sensitive
   to the exact cut.

---

## 7. Could not be found

* **Foreign-born population in collective dwellings, 2022 (any total or by
  country).** Not published in the migrations dossier, the collective-dwellings
  dossier, the 15 national migration web tables, or the `censo.gob.ar`
  collective-dwellings section. Collected on the form and present in REDATAM, so
  derivable — but only by driving the REDATAM web engine or the microdata.
* **A published foreign-born total including collective dwellings and street
  population for 2022.** Consequently the only published national total is the
  private-dwelling one, 1,933,463.
* **Place of birth for the 5,705 people in street situation, 2022.** INDEC
  explicitly disseminates only *sexo registrado al nacer* for that operation
  (`Redatam_aspectos_metodologicos.pdf`, p. 10).
* **The January 2024 first edition of the migrations dossier.** The
  `2024/01/censo2022_migraciones.pdf` URL now serves the April 2024 *Edición
  ampliada* (verified: `censo.gob.ar` and `indec.gob.ar` copies are byte-identical,
  md5 `df186c52addf9b4709ee64b6fad1303d`, 109 pp., PDF title "…Edición ampliada.
  Abril de 2024"). The first edition is not retrievable from either site. What
  changed is documented in the credits page and the press release: graphs 8, 9,
  13 and 17 plus the year-of-arrival tables were added, and **data on pages 23-25,
  27 and 32-35 were corrected** — i.e. the p. 27 jurisdiction table used here was
  one of the corrected ones. Do not cite January 2024 figures.
* **Venezuela / Colombia / Ecuador in any official 2010 INDEC table** (see §5.3).
* **An absolute private-dwellings-only foreign-born total for 2010.** Only
  derivable (1,760,241 = total − collective) or approximated by Cuadro P35's
  age-3+ private-dwelling figure of 1,745,351.
* **REDATAM online query output.** `redatam.indec.gob.ar` is a JavaScript
  application; the `RpWebEngine.exe` CGI returns only a shell page to a plain HTTP
  client. Producing the collective-dwelling foreign-born count needs a browser
  session or the downloadable microdata.
* **A REDATAM country-of-birth code list.** `P15` refers to "la tabla incluida en
  el apartado específico" of the definitions document; the geographic code tables
  were not extracted here.

---

## 8. Sources and local copies

Downloaded copies are in the session scratchpad, **not** in the repository:
`/tmp/user/1000/claude-1000/-home-nissim-Documents-dev-radiant-earth-barrios-visibles-paper/65c09a9f-d027-4ea8-8554-ad93505be3d9/scratchpad/migrants_census/`

| Local file | Title | URL |
|---|---|---|
| `censo2022_migraciones_indec.pdf` (= `..._jan.pdf`, identical) | CNPHV 2022. Resultados definitivos. Migraciones internacionales e internas. **Edición ampliada, abril de 2024**. 109 pp. ISBN 978-950-896-671-1 | `https://www.indec.gob.ar/ftp/cuadros/poblacion/censo2022_migraciones.pdf` and `https://censo.gob.ar/wp-content/uploads/2024/01/censo2022_migraciones.pdf` |
| `censo2022_viviendas_colectivas.pdf` | CNPHV 2022. Viviendas colectivas y personas en situación de calle | `https://censo.gob.ar/wp-content/uploads/2023/11/censo2022_viviendas_colectivas.pdf` |
| `xlsx/c2022_tp_migraciones_c1..c11.xlsx` | Web tables, Cuadros 1-11 (Jan 2024) | `https://censo.gob.ar/wp-content/uploads/2024/01/c2022_tp_migraciones_cN.xlsx` |
| `xlsx/c2022_tp_migraciones_c12..c15.xlsx` | Web tables, Cuadros 12-15 (Apr 2024, *edición ampliada*) | `https://censo.gob.ar/wp-content/uploads/2024/04/c2022_tp_migraciones_cN.xlsx` (c12 is `...c12.xlsx.xlsx`) |
| `xlsx/c2022_tp_c_resumen.xlsx` | Cuadro resumen: population by universe and jurisdiction | `https://censo.gob.ar/wp-content/uploads/2024/01/c2022_tp_c_resumen.xlsx` |
| `redatam_metodologia.pdf` | Base de datos REDATAM — Aspectos metodológicos | `https://redatam.indec.gob.ar/redarg/CENSOS/CPV2022/Docs/Redatam_aspectos_metodologicos.pdf` |
| `redatam_definiciones.pdf` | Base de datos REDATAM — Definiciones de la base de datos (variable dictionary) | `https://redatam.indec.gob.ar/redarg/CENSOS/CPV2022/Docs/Redatam_Definiciones_de_la_base_de_datos.pdf` |
| `redatam_universos.pdf` | Base de datos REDATAM — Control de universos (octubre 2024) | `https://redatam.indec.gob.ar/redarg/CENSOS/CPV2022/Docs/Redatam_control_de_universos.pdf` |
| `redatam_introduccion.pdf` | Base de datos REDATAM — Introducción | `https://redatam.indec.gob.ar/redarg/CENSOS/CPV2022/Docs/Redatam_introduccion.pdf` |
| `cuest_viviendas_particulares.pdf` | Cuestionario Censo 2022, viviendas particulares | `https://www.censo.gob.ar/wp-content/uploads/2022/03/Censo2022_cuestionario_viviendas_particulares_impresion.pdf` |
| `cuest_viviendas_colectivas.pdf` | Cuestionario Censo 2022, viviendas colectivas | `https://www.censo.gob.ar/wp-content/uploads/2022/02/Censo2022_cuestionario_viviendas_colectivas.pdf` |
| `press_paraguay_bolivia_venezuela.html` | Press release "Paraguay, Bolivia y Venezuela son los países con mayor representación inmigrante en la Argentina" | `https://censo.gob.ar/index.php/paraguay-bolivia-y-venezuela-son-los-paises-con-mayor-representacion-inmigrante-en-la-argentina/` |
| `press_nueva_version_ampliada.html` | Press release "Nueva versión ampliada sobre la publicación de Migraciones" | `https://censo.gob.ar/index.php/nueva-version-ampliada-sobre-la-publicacion-de-migraciones/` |
| `censo2010_tomo1.pdf`, `censo2010_tomo2.pdf` | Censo 2010, Serie B Nº 2, Tomos 1 y 2 | `https://www.indec.gob.ar/ftp/cuadros/poblacion/censo2010_tomo1.pdf`, `..._tomo2.pdf` |
| `c2010_P6.xls` / `.csv` | Cuadro P6. Población total nacida en el extranjero por lugar de nacimiento, según sexo y grupo de edad. Año 2010 | `https://sitioanterior.indec.gob.ar/definitivos_bajarArchivoNacionales.asp?idc=13&arch=x&c=2010` |

Note: `censo.gob.ar` serves an incomplete TLS chain; downloads used `curl -k`.

### Scope of the web tables

The *edición ampliada* front matter (p. 4) states the accompanying web tables
comprise **15 indicators / 4,521 tables** disaggregated to department, *partido*
or *comuna* level: 3 indicators on population by place of birth (604 tables),
3 on place of habitual residence (578 tables), and 9 on the foreign-born
population (3,339 tables). Only the 15 national ("total del país") files were
pulled here; per-jurisdiction and per-department equivalents exist on the
`censo.gob.ar` jurisdiction pages under the same `c2022_<jur>_migraciones_cN.xlsx`
naming.
