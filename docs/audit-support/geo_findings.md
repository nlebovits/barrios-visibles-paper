# Geography of INDEC's demographic reconciliation vs. the RENABAP/footprint discrepancy

Read-only research note. Sources: INDEC *Análisis Demográfico* 39 (national), 40 (jurisdictions,
October 2025), 42 (departments, February 2026); INDEC Census 2022 definitive and provisional
results; repo files `data/renabap.parquet` and `outputs/settlement_estimates.parquet`.

Page numbers below are the printed page numbers in the PDF footers.

---

## A. How AD40 builds the 2022 jurisdiction populations

### A.1 The method is a cohort balance equation per jurisdiction, not a census benchmark

AD40 §2 *Metodología* (p. 12):

> "Las proyecciones subnacionales por sexo y edad fueron elaboradas mediante el método de los
> componentes, que consiste en la proyección independiente de cada uno de los tres componentes del
> cambio demográfico –mortalidad, fecundidad y migraciones– para cada una de las 24 jurisdicciones
> del país. Para su aplicación se requiere partir de una población base por sexo y edad, mediante la
> evaluación y el ajuste de la información básica."

> "La primera etapa consistió en la revisión de la población inicial de 2001 y, a partir de esta y los
> nacimientos y defunciones por año de ocurrencia, sexo y edad, y la estimación del saldo migratorio
> (internacional e interno) por año, sexo y edad, se efectuó la ecuación de balance por cohorte
> (Swanson & Siegel, 2004), con la que se determinó la población base al 2022, punto de partida de la
> proyección."

AD40 §2.1.2 *Estimación de la población al 18 de mayo de 2022* (p. 14):

> "A partir de la población estimada al 1/1/2001 en cada provincia, los nacimientos y las defunciones
> por año de ocurrencia, sexo y edad, la estimación de saldo migratorio por año, sexo y edad, y
> teniendo en cuenta el procedimiento de conciliación censal realizado a nivel nacional, se realizó la
> ecuación de balance por cohorte (Swanson & Siegel, 2004), y se obtuvo la población corregida por
> provincia a la fecha censal (18/5/2022)."

**Answer to "is each jurisdiction reconciled with its own balance equation?"** Yes. Each of the 24
jurisdictions is carried forward independently from a revised 1 January 2001 population by its own
births, deaths and net migration to 18 May 2022. The jurisdiction's *own* censused 2022 count is
**not** the target of that equation. The only stated national tie-in is the phrase "teniendo en cuenta
el procedimiento de conciliación censal realizado a nivel nacional".

### A.2 The 2001 starting population

AD40 §2.1.1 *Revisión de la población inicial 2001* (p. 13):

> "Se ajustó la población base por provincia publicada por el INDEC (2005) a la población base de la
> proyección nacional para incorporar las correcciones realizadas en la conciliación demográfica
> nacional. Se desagregaron los grupos quinquenales de 15 a 79 años mediante el empleo de los
> multiplicadores matemáticos de Beers (Neupert, 2018). Se ajustó la cantidad de menores de 15 años a
> partir de la estimación de la fecundidad en años previos, considerando nueva información de los
> registros mencionados, y estimaciones indirectas de la fecundidad mediante la aplicación de
> diferentes procedimientos demográficos. La población de 80 años y más se estimó utilizando el método
> de generaciones extintas a partir de las defunciones de estadísticas vitales (Vincent, 1951)."

So the 2001 provincial starting values are the 2005-published provincial base **rescaled to the
national 2001 base of the new national reconciliation** — again a national, not provincial, anchor.

### A.3 Administrative records: evaluation and comparison, not benchmarks

AD40 §1.2.2 *Otros registros administrativos nacionales con desagregación provincial* (p. 12):

> "Otros registros administrativos fueron utilizados tanto en la etapa de evaluación de los datos
> censales provinciales como en la conciliación censal correspondiente a cada jurisdicción para
> comparar los resultados de las estimaciones respecto de agregados de población y estructuras por
> sexo y edad generados a partir de las fuentes administrativas."

The six sources listed (p. 12): *Relevamiento anual* school enrolment (Secretaría de Educación, April
2022); ARCA tax padrón; RENAPER documented-persons base by province, sex, age and country of birth at
May 2022; the COVID-19 vaccination database ("se seleccionan las personas por edad y sexo que
hubieran recibido al menos una dosis de la vacuna al 18/05/2022"); ANSES benefit recipients (province
= the bank branch where the benefit is deposited); and SIPA employer declarations.

The verbs are "comparar", "validar, contrastar y ajustar … y fortalecer su coherencia interna y
externa" (§1 *Datos básicos*, p. 9). AD40 never states a rule by which any of these records sets a
jurisdiction total.

### A.4 International migration by province (§5.1, p. 24)

> "La distribución por provincia del saldo migratorio internacional 2001-2040 estimado en las
> proyecciones nacionales (INDEC, 2025b) consideró varias alternativas, y se adoptó la opción que
> distribuye el saldo migratorio internacional total, sin considerar los componentes inmigratorios y
> emigratorios entre las provincias. Esta distribución contempló dos criterios: para los años en los
> que el saldo migratorio internacional fue negativo, se consideró para su distribución la proporción
> de nativos que residían fuera del país hacía 5 años, mientras que para los años con saldo migratorio
> positivo, se utilizó la distribución tanto de las personas nativas como no nativas que residían
> hacía 5 años en el exterior."

> "Por último, se realizó la distribución del saldo migratorio internacional en cada provincia por edad
> simple y sexo en base a la estructura por edad y sexo estimada en el saldo migratorio internacional,
> aplicando la estructura observada a nivel nacional para todas las provincias, dado el escaso impacto
> que tiene por su magnitud."

The **national** international balance is fixed first and then split across provinces. The census
variable used is **residence five years ago** (residía en el exterior hacía 5 años) — not place of
birth. Table 14 (p. 25) is sourced to "Censos Nacionales de Población, Hogares y Viviendas 2001, 2010
y 2022" plus foreign registers (Padrón Municipal de España, ACS 5-Year, ISTAT, INE Paraguay, ONU
2024c, OCDE 2024). Table 14 annual averages: CABA +1,819 (2001-2010) and +3,897 (2011-2022); Buenos
Aires +5,928 and +4,444; Córdoba +1,928 and +900; Santa Fe +1,383 and +613. Magnitudes are a few
thousand per year at most.

### A.5 Internal migration by province (§5.2, pp. 25-26)

> "Para la estimación del saldo migratorio interno se consideró la información de las matrices
> migratorias de los censos 2001, 2010 y 2022 correspondientes a la migración interna del quinquenio
> anterior a cada censo. Se interpolaron las tasas migratorias estimadas por sexo y edad usando esos
> años como pivotes para el resto de los años del período."

> "Se suavizaron las tasas obtenidas para todos los años con la estructura derivada del modelo de
> Rogers y Castro (1982)."

> "Los movimientos interprovinciales se han reducido o estancado a lo largo de las últimas décadas y
> perdieron importancia relativa respecto de los movimientos intraprovinciales. A nivel del total país,
> entre 2001 y 2022, la población que cambió su provincia de residencia durante los 5 años previos al
> censo disminuyó 30%, mientras que la que cambió de residencia dentro de la provincia se incrementó
> 78%."

> "Teniendo en cuenta este cambio en las tendencias de la migración interna, se proyectaron linealmente
> los saldos observados en la matriz migratoria del Censo 2022, suponiendo que estos se reducirán a la
> mitad hacia 2050 (tabla 15)."

**Census variables used for internal migration: the migration matrices of "residencia 5 años antes"
from the 2001, 2010 and 2022 censuses — the five-year-prior-residence question only.** Place of birth
(*lugar de nacimiento*) is never mentioned as an input; the only "país de nacimiento" reference in
AD40 is the RENAPER register field (p. 12). Rates are interpolated between the three census pivots,
so the entire 2001-2022 internal-migration series rests on three five-year windows: 1996-2001,
2005-2010 and 2017-2022.

Table 15 (p. 26) annual averages, 2011-2022: Buenos Aires +5,790, Córdoba +7,426, CABA −4,395,
Chaco −7,036, Misiones −3,583, Formosa −2,575, Salta −1,790, Santiago del Estero −1,205,
Corrientes −1,322, Tucumán −796, Santa Fe −65, Jujuy −596.

### A.6 Every place Census 2022 data enters the jurisdiction estimates

Exhaustively, from the AD40 text:

1. **§1.1.1, Table 1 (pp. 9-10)** — Whipple and Myers indices by jurisdiction, Census 2022 vs 2001 and
   2010. Diagnostic only; no quantity is derived from it.
2. **§1.1.2, Table 2 (p. 11)** — sex ratio (índice de masculinidad) by jurisdiction, Census 2022.
   Diagnostic: "permite identificar eventuales omisiones censales o sesgos".
3. **§1.2.2 (p. 12)** — administrative records used "en la etapa de evaluación de los **datos censales
   provinciales**" and in "la conciliación censal correspondiente a cada jurisdicción para **comparar**
   los resultados". Comparison, not benchmarking.
4. **§5.1 (p. 24)** — Census 2022 (with 2001 and 2010) supplies the distribution of persons who resided
   abroad five years earlier, used to split the nationally fixed international balance across
   provinces.
5. **§5.2 (pp. 25-26)** — Census 2022 supplies one of three internal-migration matrices (residence five
   years earlier), and the 2022 matrix alone is the basis for the forward projection.
6. Every table in AD40 carries the source line "INDEC, estimaciones elaboradas con base en el Censo
   Nacional de Población, Hogares y Viviendas 2022", but that is a provenance label, not a statement
   that jurisdiction counts were benchmarked to jurisdiction census counts.

**The jurisdiction-level censused population of 2022 is nowhere used as a level target.** It enters
only through (a) migration distributions and (b) diagnostics. This is the crux: a jurisdiction's
reconciled population can and does depart from its censused population by several percent in either
direction, with no per-jurisdiction omission rate published.

### A.7 Are jurisdiction totals forced to sum to 46,122,853?

AD40 never states an explicit prorating or raking step for jurisdiction totals. The evidence is
arithmetic and indirect:

- AD40 Table 4 (p. 14) prints "Total del país 46.122.853". The 24 jurisdiction rows as printed sum to
  **46,122,851** — two persons short, consistent with independent rounding rather than an exact
  constraint applied to the printed values.
- AD40 Table 5 (p. 15) prints "Total del país 46.135.579", and the 24 rows sum to exactly 46,135,579.
- 46,122,853 is exactly the national reconciled figure of AD39 (Table 4, p. 19: "Población censada
  45.886.580 / Población estimada a la fecha censal 46.122.853 / Diferencia relativa −0,5%"; the
  censused figure excludes "población en situación en calle por faltantes de declaración del dato de
  edad (5.705 personas)").

So: coherence with the national total is achieved **upstream**, by rescaling the 2001 provincial base
to the national 2001 base (§2.1.1) and by distributing the *nationally determined* migration balances
across provinces (§5.1, and §5.2's zero-sum internal matrix). Given a common national mortality and
fertility reconciliation, the balance equations then add up to the national figure by construction.
AD40 does **not** describe a terminal proportional adjustment of jurisdiction totals, and does not use
the phrase "prorrateo" anywhere. That distinction matters: the national total is not imposed on the
provinces at the end — the provinces are built from nationally reconciled ingredients.

AD40 glossary (p. 153) defines the concept but publishes no jurisdiction values:

> "Omisión censal: permite medir el error de cobertura en un operativo censal. Se calcula con la
> población corregida menos la población censada, y a ese resultado se lo divide por la población
> censada. Se expresa como porcentaje."

---

## B. How AD42 builds the department estimates

AD42 §1 *Datos básicos* (p. 8):

> "Población por sexo de cada departamento al 1° de julio de 2010 (INDEC, 2015): corresponde a la
> población base de las proyecciones elaboradas a partir del Censo 2010, la cual incorpora una
> corrección por omisión censal. Sobre esta base, se aplicó un ajuste adicional derivado del análisis
> de evaluación demográfica realizado para las proyecciones nacionales y por jurisdicción vigentes
> (INDEC, 2025a; 2025b), de modo de asegurar la coherencia con los totales provinciales estimados como
> población base al 1° de julio de 2022, desagregados por sexo."

> "Población por sexo de cada departamento al 1° de julio de 2022: se obtuvo mediante el **ajuste
> proporcional de la población censada**, de manera tal que la suma de las poblaciones departamentales
> resulte consistente con la población de la jurisdicción (INDEC, 2025b) estimada para la misma fecha y
> sexo."

> "En ambos casos, el procedimiento consistió en la aplicación de un **factor de corrección calculado
> como el cociente entre la población provincial objetivo y la suma de las poblaciones departamentales
> observadas**, para cada sexo. Este factor se aplicó de **forma uniforme a todos los departamentos,
> preservando el peso relativo de cada uno en el total de la población provincial**, con excepción de
> aquellos casos en los que se realizaron ajustes específicos analizados en conjunto con las
> direcciones provinciales de estadística (DPE) y con base en evidencia asociada al operativo censal."

> "Población por sexo de la jurisdicción 2023-2035 (INDEC, 2025b): se tuvo en cuenta que la suma de la
> población estimada de los departamentos en cada año es igual a la población proyectada a nivel de la
> jurisdicción."

**This confirms the framing in the task.** The 2022 department population is the **censused**
department population multiplied by a single province-wide, sex-specific scalar that makes the
departments sum to the AD40 jurisdiction total. The 2010 department population is the 2010-based
department projection base, likewise rescaled to be coherent with AD40. Every department in a province
therefore receives the *same* percentage correction — the province's aggregate reconciliation gap is
spread uniformly, so **the within-province relative distribution is exactly the Census 2022 relative
distribution**, and the 2010→2022 department growth rates are exactly the censused intercensal growth
rates up to the two province-level scalars.

The only exceptions are the "ajustes específicos" agreed with the provincial statistical offices.

### B.1 Independent department-level demographic input?

None that sets a level. AD42 §1 (p. 8) lists further sources, but explicitly as contrasts:

> "En el proceso de elaboración de las estimaciones también se utilizó información proveniente de
> registros administrativos con el propósito de **contrastar** los totales de población obtenidos en las
> poblaciones base … a fin de evaluar la consistencia de los resultados obtenidos para el período
> intercensal:"
> — "Estadísticas vitales de nacimientos y defunciones: base de eventos por departamento para el
> período 2010-2022, provista por la DEIS (MINSAL)."
> — "Registro Nacional de las Personas (RENAPER): a. Base de personas documentadas … b. Procesamiento
> especial de movilidad residencial interdepartamental, con base en el universo de personas residentes
> en Argentina que, entre 2012 y 2022, tramitaron cambios de domicilio que implicaron actualizaciones
> en el departamento de residencia."

So department births, deaths and RENAPER address-change flows exist and were computed, but they are
used to *check* the ratio-derived figures, not to run a department balance equation. **There is no
department-level cohort-component estimate.**

### B.2 Projection method 2023-2035

AD42 §3 *Metodología* (p. 9):

> "Las estimaciones departamentales por sexo se realizaron utilizando el método de los incrementos
> relativos para 23 de las 24 jurisdicciones. En el caso de las comunas de la Ciudad Autónoma de Buenos
> Aires, se utilizó el método de función logística de proporciones y se tuvo en cuenta la tendencia al
> decrecimiento de la población en la jurisdicción y la heterogeneidad entre comunas durante el período
> que abarcan las estimaciones."

§3.1 *Incrementos relativos* (pp. 9-10):

> "El método de los incrementos relativos o de participación en el crecimiento es uno de los métodos de
> razón (Smith, Tayman & Swanson, 2013) que expresan la población de un área menor como la proporción
> de un área mayor. Se utilizan cuando existe una estructura jerárquica perfecta entre entidades, y las
> áreas menores son mutuamente excluyentes. Además, la sumatoria de todas las áreas menores (en este
> caso, los departamentos) debe corresponderse con un área mayor. El método requiere de la proyección
> independiente de las áreas mayores para el período de la proyección. Se fundamenta en la
> participación del crecimiento absoluto del área mayor (jurisdicción) que le corresponde a cada área
> menor (departamento) en un determinado período de referencia (Madeira y Simões, 1972)."

> "Para la determinación de estos coeficientes se utiliza el **período delimitado por dos censos**."

> "Generalmente, cuando el crecimiento de las áreas mayores no presenta cambios bruscos para el período
> estimado, el uso de esta metodología implica aceptar para el largo plazo una disminución de las
> diferencias en los ritmos de crecimiento de las áreas componentes."

§3.2 *Función logística para proyectar proporciones* (pp. 10-11), used only for the CABA comunas:

> "Este método consiste en la extrapolación de relaciones existentes entre la población del área menor
> y la población del área mayor, por lo que su aplicación requiere disponer de una proyección de la
> población del área mayor para el período considerado (Arriaga, 2001)."

> "La relación que se utiliza generalmente es la proporción que representa la población del área menor
> con respecto a la población del área mayor. Estas proporciones se extrapolan con la función logística,
> dado que en esta versión del método solo se requiere contar como dato básico con la población en dos
> momentos. … Las proporciones proyectadas luego se ajustan de manera tal que se respete la
> distribución relativa con el fin de que su suma sea igual a 1. Por último, se multiplican las
> proporciones ajustadas por la población proyectada del área mayor …"

**Statement for the paper: AD42's department figures are derived from Census 2010→2022 intercensal
growth ratios, uniformly rescaled ("prorrateados") to the AD40 jurisdiction totals, and projected
forward as shares of the AD40 jurisdiction projection. This is exactly what the text says.** Both
methods take the jurisdiction trajectory as given and only redistribute it; the department layer
contributes shape, never level. And because the redistribution factor is uniform within a province,
the shape is Census 2022's shape.

### B.3 The provincial-office consultation (§2, p. 9)

> "Durante noviembre y diciembre de 2025, se desarrolló un proceso de consultas e intercambios con las
> DPE. Este proceso contempló la presentación de los principales resultados vinculados a la conciliación
> demográfica, la metodología empleada para las estimaciones de población 2022-2035, las poblaciones
> base por departamento y las tasas de crecimiento. Asimismo, se expusieron los índices de masculinidad
> resultantes, la comparación entre la variación intercensal observada y las tasas implícitas calculadas
> a partir de las poblaciones base 2010 y 2022, junto con los valores estimados para cada año
> calendario."

> "Este intercambio tuvo como objetivo principal someter a revisión experta los supuestos y resultados
> preliminares de las estimaciones departamentales e incorporar la perspectiva territorial y
> sociodemográfica de los equipos provinciales. Esta retroalimentación resultó fundamental para
> garantizar la coherencia de los resultados y la adecuación de los insumos que se utilizan en las
> estimaciones."

**What it changed:** the only concrete consequence AD42 attributes to the consultation is the carve-out
in §1 — "con excepción de aquellos casos en los que se realizaron ajustes específicos analizados en
conjunto con las direcciones provinciales de estadística (DPE) y con base en evidencia asociada al
operativo censal". AD42 does **not** name which departments received such adjustments, how large they
were, or what the "evidencia asociada al operativo censal" was. Everything else described is
presentation and review, not modification.

---

## C + D. Jurisdiction comparison, joined to RENABAP

| Jurisdiction | Census 2022 definitive | AD40 reconciled 18 May 2022 | Recon − census | Recon − census % | RENABAP families | Footprint families | RENABAP pop ×2.8 | Footprint pop ×2.8 | Footprint gap % of census |
|---|---|---|---|---|---|---|---|---|---|
| Chaco | 1,129,606 | 1,189,884 | 60,278 | +5.34 | 55,821 | 118,817 | 156,299 | 332,687 | 15.62 |
| La Rioja | 383,865 | 398,296 | 14,431 | +3.76 | 2,476 | 7,386 | 6,933 | 20,682 | 3.58 |
| Santa Fe | 3,544,908 | 3,669,573 | 124,665 | +3.52 | 92,776 | 153,171 | 259,773 | 428,879 | 4.77 |
| Río Negro | 750,768 | 775,839 | 25,071 | +3.34 | 36,239 | 61,858 | 101,469 | 173,202 | 9.55 |
| La Pampa | 361,859 | 373,802 | 11,943 | +3.30 | 409 | 1,156 | 1,145 | 3,237 | 0.58 |
| Misiones | 1,278,873 | 1,312,397 | 33,524 | +2.62 | 58,322 | 99,990 | 163,302 | 279,973 | 9.12 |
| Córdoba | 3,840,905 | 3,921,832 | 80,927 | +2.11 | 37,039 | 63,097 | 103,709 | 176,670 | 1.90 |
| Formosa | 607,419 | 620,097 | 12,678 | +2.09 | 27,942 | 54,533 | 78,238 | 152,692 | 12.26 |
| Salta | 1,441,351 | 1,466,305 | 24,954 | +1.73 | 39,319 | 74,777 | 110,093 | 209,375 | 6.89 |
| San Juan | 822,853 | 836,714 | 13,861 | +1.68 | 5,563 | 10,508 | 15,576 | 29,424 | 1.68 |
| Entre Ríos | 1,425,578 | 1,449,417 | 23,839 | +1.67 | 26,276 | 46,799 | 73,573 | 131,038 | 4.03 |
| Tucumán | 1,731,820 | 1,757,461 | 25,641 | +1.48 | 48,003 | 92,044 | 134,408 | 257,724 | 7.12 |
| Catamarca | 429,562 | 434,528 | 4,966 | +1.16 | 3,936 | 7,350 | 11,021 | 20,579 | 2.23 |
| Chubut | 592,621 | 597,148 | 4,527 | +0.76 | 10,660 | 22,219 | 29,848 | 62,214 | 5.46 |
| Ciudad Autónoma de Buenos Aires | 3,121,707 | 3,122,464 | 757 | +0.02 | 80,517 | 80,960 | 225,448 | 226,688 | 0.04 |
| Mendoza | 2,043,540 | 2,032,130 | -11,410 | -0.56 | 26,432 | 52,618 | 74,010 | 147,330 | 3.59 |
| Buenos Aires | 17,523,996 | 17,407,546 | -116,450 | -0.66 | 588,779 | 1,119,569 | 1,648,581 | 3,134,792 | 8.48 |
| Santa Cruz | 337,226 | 334,310 | -2,916 | -0.86 | 2,863 | 7,193 | 8,016 | 20,140 | 3.60 |
| Santiago del Estero | 1,060,906 | 1,044,587 | -16,319 | -1.54 | 20,947 | 49,660 | 58,652 | 139,049 | 7.58 |
| Corrientes | 1,212,696 | 1,188,384 | -24,312 | -2.00 | 29,136 | 56,227 | 81,581 | 157,435 | 6.25 |
| Jujuy | 811,611 | 795,110 | -16,501 | -2.03 | 18,938 | 31,356 | 53,026 | 87,797 | 4.28 |
| San Luis | 542,069 | 527,034 | -15,035 | -2.77 | 4,442 | 8,714 | 12,438 | 24,399 | 2.21 |
| Neuquén | 710,814 | 688,557 | -22,257 | -3.13 | 14,813 | 30,074 | 41,476 | 84,208 | 6.01 |
| Tierra del Fuego, Antártida e Islas del Atlántico Sur | 185,732 | 179,436 | -6,296 | -3.39 | 6,147 | 12,722 | 17,212 | 35,621 | 9.91 |
| **Total (24 jurisdictions)** | 45,892,285 | 46,122,851 | 230,566 | +0.50 | 1,237,795 | 2,262,798 | 3,465,827 | 6,335,835 | 4.13 |

Sorted by "Recon − census %", descending. Full machine-readable versions:
`geo/jurisdiction_comparison.csv` (census + AD40 columns) and `geo/renabap_by_province.csv`
(the same, joined to RENABAP and footprint aggregates, plus derived shares).

Notes on the table:

- **Census 2022 definitive** is INDEC's definitive censused population by jurisdiction, from
  *CNPHV 2022 — Indicadores por sexo y edad. Resultados definitivos*
  (`https://www.indec.gob.ar/ftp/cuadros/poblacion/censo2022_indicadores_demograficos.pdf`), table
  "Población total, por jurisdicción, sexo registrado al nacer y edad mediana". The 24 rows sum to
  **45,892,285**, matching the published national definitive total exactly.
- **AD40 reconciled** is AD40 Table 4 (18 May 2022, census date). Its 24 rows sum to 46,122,851 against
  a printed national total of 46,122,853 (a 2-person rounding residue).
- The national reconciled-minus-censused gap computed here is **+230,566 (+0.50%)**. AD39's own national
  comparison is 46,122,853 − 45,886,580 = **+236,273 (+0.51%)**; the 5,707 difference is the 5,705
  street-population persons lacking an age declaration (excluded from AD39's censused figure but
  included in the definitive jurisdiction totals) plus the 2-person rounding residue.
- **Footprint families** is `estimated_families` from `outputs/settlement_estimates.parquet`, i.e.
  `max(building_count × 1.1, renabap_families)` per settlement at 100% assumed occupancy (5,803 of
  6,467 settlements take the buildings branch, 664 keep the RENABAP value).
- Population multipliers 2.8 (INDEC 2022 census persons per household) and 3.35 (settlement-specific).
  `renabap_by_province.csv` carries both; the markdown table shows ×2.8 only.

### Provisional (2023) vs definitive, for context

Definitive minus provisional, largest movers: **Córdoba −138,079**, Buenos Aires −45,057,
Neuquén −15,776, Chaco −13,357, Santa Fe −11,614, Río Negro −11,299, Chubut −10,499; and upward
**Mendoza +29,007**, **Tucumán +28,634**, Corrientes +15,143, Jujuy +13,656, Santiago del Estero
+6,878. Córdoba's revision is by far the largest and moves in the *opposite* direction to its
reconciliation gap: the definitive count cut 138,079 people from the provisional figure, and AD40 then
adds 80,927 back on top of the definitive count. Full column in both CSVs.

---

## E. Analysis

### E.1 The reconciliation gap has a real geography, and it is large

The national +0.50% average conceals a range of nearly nine percentage points. Reconciled exceeds
censused by **+5.34% in Chaco** (+60,278 people), +3.76% in La Rioja, +3.52% in Santa Fe (+124,665
people — the largest absolute upward adjustment of any jurisdiction), +3.34% in Río Negro, +3.30% in
La Pampa, +2.62% in Misiones and +2.11% in Córdoba. It falls *below* censused by −3.39% in Tierra del
Fuego, −3.13% in Neuquén, −2.77% in San Luis, −2.03% in Jujuy, −2.00% in Corrientes and −1.54% in
Santiago del Estero. Buenos Aires province is **−0.66% (−116,450 people)** and CABA is essentially
neutral at +0.02% (+757).

This is a strong result on its own: because AD40 never uses the jurisdiction censused count as a
level target (§A.6), these differences are not "measured census undercount by province". They are the
residual between a 21-year cohort balance equation and the census, and INDEC does not decompose or
publish them as omission rates by jurisdiction.

### E.2 The two geographies do not line up

Ranking the 24 jurisdictions by reconciled-minus-censused (%) against the footprint-minus-RENABAP gap
as a share of censused population:

| Pair | Pearson | Spearman |
|---|---|---|
| recon − census % ~ footprint gap % of census | 0.176 | 0.036 |
| recon − census % ~ RENABAP pop (×2.8) as % of census | 0.216 | 0.129 |
| recon − census % ~ footprint pop (×2.8) as % of census | 0.203 | 0.096 |
| recon − census (persons) ~ footprint − RENABAP pop (persons) | −0.524 | 0.256 |

Essentially no rank association. The negative Pearson on the absolute-persons pair is driven entirely
by Buenos Aires province, which is the single largest negative on one axis and the single largest
positive on the other.

The mismatch is concrete and easy to state:

- **Buenos Aires province** holds **47.6%** of all RENABAP families and **51.8%** of the entire
  national footprint-minus-RENABAP gap (1,486,211 of 2,870,008 people at ×2.8). Its footprint-implied
  settlement population is 17.9% of its censused population against RENABAP's 9.4%, an 8.5-point gap —
  the third largest in the country. Yet AD40 *subtracts* 116,450 people from Buenos Aires relative to
  the census. If the footprint evidence pointed at undercounted informal population, Buenos Aires is
  where INDEC's reconciliation should have gone furthest up. It goes down.
- **CABA** has the second-largest RENABAP settlement share of population (7.2%) and a footprint gap of
  essentially zero (+0.04 points; the villas are vertical, so footprints under-read them). AD40 moves
  CABA by +757 people. Here the two methods agree — but only because both find nothing.
- **Chaco** is the one clean coincidence: the largest reconciliation gap (+5.34%) *and* the largest
  footprint gap (+15.62 points, 13.8% RENABAP → 29.5% footprint). Misiones (+2.62% / +9.12 points) and
  Formosa (+2.09% / +12.26 points) are weaker versions of the same pattern.
- **Santa Fe** takes the biggest absolute upward adjustment (+124,665) but has a middling footprint gap
  (+4.77 points), and **Córdoba** (+80,927) has one of the smallest (+1.90 points). Both are large
  provinces where the adjustment tracks province size, not settlement incidence.
- The clearest counter-examples: **Santiago del Estero** (footprint gap +7.58 points, reconciliation
  −1.54%), **Corrientes** (+6.25, −2.00%), **Jujuy** (+4.28, −2.03%), **Neuquén** (+6.01, −3.13%),
  **Tierra del Fuego** (+9.91, −3.39%). All five have substantial footprint-implied undercounts of
  settlement population and all five are revised *downward* by INDEC.
- **Tucumán** (+1.48% / +7.12 points) and **Salta** (+1.73% / +6.89 points) sit in between: modest
  upward reconciliation against a large footprint gap.

### E.3 Magnitudes are not comparable either

The whole national reconciliation moves 230,566 people, 0.50% of the population. The national
footprint-minus-RENABAP gap alone is 2,870,008 people at ×2.8 (3,433,438 at ×3.35) — 12.5 times
larger. Even in Chaco, the best-aligned province, the reconciliation adds 60,278 people against a
footprint gap of 176,388. The reconciliation is a demographic-accounting correction of an order of
magnitude that simply cannot absorb the settlement-population discrepancy.

### E.4 What this means for the paper's argument

The chain is: AD42 department figures = Census 2022 department shares × a uniform provincial scalar,
projected forward on Census 2010→2022 intercensal growth, benchmarked to AD40 jurisdiction totals
(§B). AD40 jurisdiction totals = per-jurisdiction cohort balance equations from a 2001 base, using
Census 2022 only for migration distributions and diagnostics (§A). So **no INDEC product at any
geography incorporates an independent measurement of settlement population**, and at the department
level — the level at which informal settlements are actually located — the relative distribution is
the raw census distribution by construction. A department-level census undercount concentrated in
*barrios populares* survives the entire INDEC pipeline untouched, because the only correction applied
below the province is a scalar that is identical for every department in the province.

The province-level geography confirms this from the other direction: whatever the reconciliation gap
measures, its spatial pattern is uncorrelated with settlement incidence, and it is an order of
magnitude too small to be the same phenomenon.

---

## F. What could not be established

1. **Whether AD40 applies a terminal raking of jurisdiction totals to 46,122,853.** The text never says
   so and never uses "prorrateo" or equivalent for jurisdictions. The 2-person shortfall in Table 4's
   row sum is consistent with no exact constraint on the printed values, but is not proof. The
   coherence is most plausibly upstream (rescaled 2001 base, nationally fixed migration balances), as
   argued in §A.7 — but AD40 does not state a rule.
2. **Jurisdiction-level census omission rates.** INDEC defines *omisión censal* (AD40 glossary p. 153,
   AD39 glossary) but publishes no by-jurisdiction values. The reconciled-minus-censused column in the
   table is my own computation and INDEC does not label it as omission.
3. **Which departments received the "ajustes específicos" agreed with the DPEs** (AD42 §1, p. 8), how
   large they were, or what evidence justified them. AD42 names none.
4. **The exact 2010 and 2022 department populations underlying AD42.** Establishing that AD42's
   department shares equal Census 2022 shares empirically would require the department-level census
   tables and AD42's Cuadros 1-24 parsed out; I read the method text, not the numbers.
5. **The allocation of the 5,705 street-population persons across jurisdictions.** They are in the
   definitive jurisdiction totals but INDEC's national reconciliation table excludes them; the
   per-jurisdiction split is not published, so 5,705 of the 236,273 national gap cannot be assigned.
6. **Whether the RENAPER interdepartmental address-change processing (AD42 §1, p. 8) contradicted or
   confirmed the ratio-derived department figures.** AD42 says it was used "para contrastar" and reports
   no outcome.
7. **A settlement-level or department-level census undercount estimate from INDEC.** None exists in
   AD39, AD40 or AD42.
8. **CABA's comuna-level treatment under the logistic method** may impose asymptote adjustments
   ("ajustes específicos sobre las asíntotas superior e inferior", §3.2, p. 11); AD42 does not say
   whether any were applied to CABA in practice.

---

## G. Files written

All under `docs/audit-support/` (PDF and raw text files were not copied):

| File | Contents |
|---|---|
| `geo_findings.md` | This note |
| `jurisdiction_comparison.csv` | 24 jurisdictions: census definitive, census provisional, AD40 Table 4, AD40 Table 5, reconciled − censused (persons and %), definitive − provisional |
| `renabap_by_province.csv` | The above joined to RENABAP families, building counts, footprint families, ×2.8 and ×3.35 populations, footprint/RENABAP ratio, and shares of censused population |
| `ad40_table4_reconciled_18may2022.csv` | AD40 Table 4 verbatim (both sexes, men, women) |
| `ad40_table5_base_1jul2022.csv` | AD40 Table 5 verbatim |
| `census2022_definitive_by_jurisdiction.csv` | Definitive censused population by jurisdiction (sum 45,892,285, verified) |
| `census2022_provisional_by_jurisdiction.csv` | Provisional population by jurisdiction (sum 46,044,703, verified) |
