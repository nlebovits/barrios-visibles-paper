# Barrios Visibles

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22656880.svg)](https://doi.org/10.5281/zenodo.22656880)

Argentina's Registro Nacional de Barrios Populares (RENABAP) records about
1.24 million families across 6,467 registered informal settlements. This
analysis compares that enumeration against 1.97 million building footprints
from the combined Google, Microsoft, and OpenStreetMap dataset, joined to the
same polygons.

Inside registered boundaries, detected footprints exceed recorded families by
59%. A per-settlement household floor exceeds RENABAP's national total by 83%.
Under conservative population multipliers that implies 6.3 to 7.6 million
residents, or 2.9 to 3.4 million above the official figure.

The gap splits by geography. In the consolidated vertical villas of CABA,
RENABAP records residents whom footprints miss. Everywhere else, building
counts run well above the recorded family estimates.

This repository contains the analysis code and the manuscript source. The data
snapshot behind every number is archived at
[10.5281/zenodo.22656880](https://doi.org/10.5281/zenodo.22656880).

## Environment

[pixi](https://pixi.sh) manages the dependencies. `pixi.lock` pins every
version. Install the environment once:

```bash
pixi install
```

## Analysis

`estimate.py` estimates household counts in the informal settlements of
Argentina. It joins satellite-derived building footprints to the RENABAP
settlement boundaries, then sweeps three building-size filters, four
occupation rates, and two population multipliers.

```bash
pixi run estimate
```

The script downloads the RENABAP boundaries and the VIDA building footprints
into `data/`, which `.gitignore` excludes. It also reads an IGN Planta Urbana
parquet file. That layer has no public download URL, so point
`URBAN_AREAS_PATH` at a local copy before the first run.

## Papers

The manuscript source is in `paper/`. Render both papers to PDF:

```bash
pixi run pdf
```

That writes `outputs/barrios-visibles-part-i.pdf` and
`outputs/barrios-visibles-part-ii.pdf`. pandoc comes from pixi. The xelatex
engine comes from a system TeX installation, because a full TeX distribution
would dwarf the rest of this environment. On Debian or Ubuntu, install
`texlive-xetex` and `fonts-dejavu`.

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

Vale needs its pinned style packages before the first run. `vale sync` fetches
them into `styles/`, and `.gitignore` keeps them out of the repository:

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

## Commits

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
