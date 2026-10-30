# T58W1Verify12 — row verification

Base: `2a32aa8228d5f86a85c81a923a3148bf792a9538`. No scratch directory was created; no checks were run.

Commands used (all reads against the lane repository/base):

- `git -C "$L" show <base>:corpus/lessons/round-56-verifier-spotcheck.md | tail -n 30` — recovered the routed R56.1–R56.4 item descriptions.
- `git -C "$L" show <base>:SKILL.md | grep -nE 'QUALITY 34|page-local|heading anchors|## Standing rules|RECEIPT_REV_CONTENT_DRIFT|role=verdict|--paths'` — standing rules at lines 53–54 associate verdict receipt + declared `--paths` drift with `RECEIPT_REV_CONTENT_DRIFT`; page-local `:925-929` remains in the cited SKILL index excerpt at line 1782.
- `git -C "$L" show <base>:corpus/knowledge/receipt-revision-binding.md | grep -nE 'ER-R57-K1|19/19|recheck:'` — line 3 retains the `14/14` frontmatter; lines 224 onward document round-57 errata, but do not replace that frontmatter line.
- `git -C "$L" show <base>:corpus/README.md | grep -n 'receipt-revision-binding.md'` — line 653 indexes the entry, but does not resolve the stale frontmatter.
- `git -C "$L" show <base>:.ufo/evidence/round-57/coldread-referent-r56.md` — the record names the `external_inputs` labels, the exact intermediate referent and its digests.
- `git -C "$L" rev-parse 3a05d706` returned `3a05d706fe434ee8450a144546226e44750f1993`; `git -C "$L" show --stat --oneline 3a05d706` lists the R56.2 changes to SKILL. This full hash is an ancestor of base as demonstrated by `git show <base>:SKILL.md` containing the resulting standing-rules mapping.

| ID | Result at base | Proposed status | Evidence-grounded finding |
|---|---|---|---|
| R56.1 | open | open | The SKILL page-local reference `:925-929` remains, so use a round-58 fix intent; cited line 1782. |
| R56.2 | fixed | fixed | SKILL lines 53–54 carry the correct `RECEIPT_REV_CONTENT_DRIFT` mapping for verdict with `--paths`; resolving commit `3a05d706fe434ee8450a144546226e44750f1993`. |
| R56.3 | open | open | README index exists and errata gives 19/19, but frontmatter line 3 still says 14/14 rather than pointing to the superseding value. |
| R56.4 | fixed | fixed | `.ufo/evidence/round-57/coldread-referent-r56.md` records the intermediate referent and both source digests; resolving commit `3a05d706fe434ee8450a144546226e44750f1993`. |

The JSON beside this report contains one row per assigned ID. Fixed-row evidence excerpts are grounded in the checked base tree. Scratch cleanup: not applicable (no scratch created).