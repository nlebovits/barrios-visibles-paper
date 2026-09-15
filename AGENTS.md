# Literature registry

Read `literature/README.md` before touching sources, claims, or citations.

Order of operations, every time:

1. Add the item in Zotero and pin the citation key.
2. Export to `paper/references.bib`.
3. Create `literature/sources/<key>.md` from the template in the README.
4. Record findings with locators before writing any claim link.
5. Cite `[@key]` in prose.
6. Run `pixi run sources-index`, then `pixi run sources-check`.

Hard rules:

- Never hand-edit `paper/references.bib`. Fix the item in Zotero and re-export.
- Never hand-edit `literature/index.md`, `literature/evidence-matrix.csv`,
  `literature/schema.json`, or the parquet tables in `outputs/`. Run
  `pixi run sources-index`.
- Never write a claim link without at least one evidence ID.
- Never leave `does_not_establish` empty.
- Never give a `kind: unlocated` finding a `loc`. If you have the page, change
  the kind.
- Never invent a page number. Use `kind: unlocated` and set `follow_up`.
- Never delete an annotated-review finding to make a note shorter. The reviews
  are the audit record.
- Never add a key to `literature/pending.txt` to silence an error you could
  fix by writing the note. The list is for deferred work, not for skipped
  work.
- Remove a key from `literature/pending.txt` in the same commit that adds its
  note.
