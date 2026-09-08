# Barrios Visibles

Analysis code and manuscript source for the Barrios Visibles paper.

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

## License

[Apache-2.0](LICENSE) covers the code in this repository.

Nissim Lebovits holds the copyright to the paper text, figures, and tables,
and reserves all rights to them. Read the manuscript on
[SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6588819).
