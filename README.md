# Barrios Visibles

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22656880.svg)](https://doi.org/10.5281/zenodo.22656880)

This repository contains the canonical manuscript, supplement, and analysis
code for submission of *Barrios Visibles* to Cambridge University Press's
*Data & Policy*. Paper I is the submission manuscript. The former Paper II
remains as a historical working paper; its Census 2022 evidence is integrated
into Paper I as a compact robustness comparison.

Argentina's Registro Nacional de Barrios Populares (RENABAP) records about
1.24 million families across 6,467 registered informal settlements. The
article compares that enumeration against 1.97 million building footprints
from the combined Google, Microsoft, and OpenStreetMap dataset, joined to the
same polygons.

The version 1.0.0 data snapshot is archived at
[10.5281/zenodo.22656880](https://doi.org/10.5281/zenodo.22656880).
A recovered mismatch between its derived footprint total and the manuscript is
documented in REPRODUCIBILITY.md and must be resolved before submission.

## Findings

Inside registered boundaries, detected footprints exceed recorded families by
59%. A per-settlement household floor exceeds RENABAP's national total by 83%.
Under conservative population multipliers that implies 6.3 to 7.6 million
residents, or 2.9 to 3.4 million above the official figure.

The gap splits by geography. In the consolidated vertical villas of CABA,
RENABAP records residents whom footprints miss. Everywhere else, building
counts run well above the recorded family estimates. A Census 2022 robustness
comparison declines from 2.62 to 1.88 as the analysis is restricted to radios
increasingly covered by registered settlements. It is a consistency check, not
an independent population count.

## Reproduce the analysis

### Install the environment

[pixi](https://pixi.sh) manages the dependencies. `pixi.lock` pins every
version. Install the environment once:

```bash
pixi install
```

### Run the frozen analyses

The default RENABAP analysis uses the version-specific Zenodo snapshot:

    pixi run estimate

The Census comparison requires a new Zenodo version containing the processed
radio and recovered settlement-count files. Until the author publishes that
version and inserts its record id, run it against the recovered inputs:

    pixi run census-comparison -- \
      --census-path /path/to/radios-hilbert.parquet \
      --settlements-path /path/to/barrios-hilbert.parquet

After the archive update:

    pixi run reproduce

Live modes retrieve changing upstream sources and need not reproduce publication
values. See REPRODUCIBILITY.md for file hashes, data lineage, and unresolved
provenance issues.

## Build the submission files

The canonical article and supplement are in paper/. Render both with:

    pixi run pdf

This writes outputs/barrios-visibles-data-and-policy.pdf and
outputs/barrios-visibles-supplement.pdf. The historical Paper II can still be
rendered with pixi run pdf-part-ii. Pandoc comes from pixi. The xelatex engine
comes from a system TeX installation; on Debian or Ubuntu, install
texlive-xetex and fonts-dejavu.

## Prose checks

Vale and proselint run through [prek](https://github.com/j178/prek), which
pixi provides. Install the git hooks once:

```bash
pixi run prek install \
  --hook-type pre-commit \
  --hook-type commit-msg
```

Run every check against the whole tree:

```bash
pixi run lint
```

To run Vale directly, first fetch its pinned style packages. `vale sync` puts
them in `styles/`, which `.gitignore` excludes:

```bash
vale sync
vale --output=line .
```

The local rules live in `styles/`, and `.vale.ini` configures them. Each rule
explains its purpose in its `message` field. To suppress a rule for one
heading, wrap the heading in a comment toggle:

```markdown
<!-- vale Paper-Mechanics.Headings = NO -->
## A Heading That Must Keep Its Case
<!-- vale Paper-Mechanics.Headings = YES -->
```

A comment toggle works on a local style only. Vale ignores it for a rule from
a package such as `ai-tells` or `Google`. Suppress one of those with a path
section in `.vale.ini`.

## Commit messages

Commit messages follow the Conventional Commits format. The commitizen hook
checks each message at commit time.

## Funding

Nissim Lebovits gratefully acknowledges financial support for this research by
the Fulbright U.S. Student Program, which is sponsored by the U.S. Department
of State and the Comisión Fulbright Argentina. Its contents are solely the
responsibility of the author and do not necessarily represent the official
views of the Fulbright Program, the Government of the United States, or the
Comisión Fulbright Argentina.

## License

[Apache-2.0](LICENSE) covers the code in this repository.

Nissim Lebovits holds the copyright to the paper text, figures, and tables,
and reserves all rights to them. Read the manuscript on
[SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6588819).
