# ConnectorSibling — Sibling overlap (axis: adjacency)

## Axes

- adjacency (this seat): sibling-gate overlap vs tameshi ownership
- depth (C1): `tools/write-path-census-v2.py` sha pin `4022853295882c5a11e192274e9215ea5a008e54eb0a2f77a8a2365f522d878b`
- freshness (C2): untouched
- province: `PROVINCE.md` adjacent rule, report never absorb

## Evidence

Command (read-only, depth covers `<lane>/<dir>/<file>`):

```
find /home/vgpnk/Projects/shokunin -maxdepth 3 -name 'write-path-census*' -not -path '*/__pycache__/*' -print
```

Output, only the tameshi pair:

```
/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/write-path-census.py
/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/write-path-census-v2.py
```

Same two paths from a name walk that also checked `.tower/worktrees` and `tameshi-shokukin` (empty). No sibling lane has a tool named `write-path-census`.

`sha256sum tools/write-path-census-v2.py` = `4022853295882c5a11e192274e9215ea5a008e54eb0a2f77a8a2365f522d878b` (matches frozen `contract.json` `claims.C1.tool_sha256`). Live v2 not edited.

String scan of sibling `tools/`, `scripts/`, `verifiers/`, and kagi `corpus/` for `write-path-census|os\.replace|expected\.json|WRITE_CENSUS|update_goldens` returned one hit, not a write-form census:

`souji-shokunin/tools/souji-landing-gate.py:133`

```
EXPECTED_JSON_RE = re.compile(r"tests/fixtures/[^/]+-frozen/expected\.json$")
```

That is souji's frozen-pin path rule (`:128-133`), owned by souji (`souji-shokunin/PROVINCE.md:6-17`, hygiene). v2's `WRITE_RE` (`tools/write-path-census-v2.py:16-22`) does not match that assignment line, so the line is not a v2 write site. v2's `EXPECTED_RE` (`:23-25`) looks for a quoted `expected.json` on the same line as `open` / `.write_bytes` / `os.replace` / `os.rename`. Different predicate. Not overlap.

## Province

Absorbing a sibling gate would violate tameshi `PROVINCE.md`:

- `:14-17` — every lane's gate remains its own; never edit a sibling's gate code; recommendations travel in round reports
- `:20` — **Out of province → report, never absorb.**
- `:44-45` — **Adjacent** — report, never absorb: every sibling gate's code (owner lane)

## Proposed move

Do not import `souji-landing-gate.py:133` (or any sibling gate) into `tools/write-path-census-v2.py`. Leave v2 bytes at the C1 pin. The near-miss is a report, not a merge.

That improves adjacency (false overlap stays closed; souji keeps its gate) and harms neither depth (sha pin holds) nor freshness (C2 snapshot untouched).

## Risks

A later seat that treats souji's `expected.json` suffix as the missing C1 pattern and edits v2 breaks `tool_sha256` (C1 fail) and crosses province in one change. v1 pin `bc8c660c…` is a different file and was not the sibling scan target.

## Verification

Re-run the `find` above. Re-read `PROVINCE.md:14-20` and `:44-45`, and `souji-landing-gate.py:128-133`. Do not run the C1/C2 counters in default mode.

No tools installed.
