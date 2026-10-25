# ConnOverlap — sibling overlap scan for the two round-43 capabilities

Seat `L1Tameshi43.ConnOverlap`, round 43 attempt 1, item **sibling overlap scan**.
Judged on: adjacency. Read-only on every sibling; nothing under
`/home/vgpnk/Projects/shokunin/<other lane>`, `/home/vgpnk/Projects/shokuknow`, the
lane's jj state or Git index was written. Scratch only at
`/tmp/tameshi-r43-ConnOverlap-fixture/` (deleted before return). No tool installed
or upgraded, so there is no tool/version/channel entry to record.

Questions asked of each lane:
**A** — "which staged/imported ids collide with a registry?"
**B** — "classify a mutant survivor?"

## Method (reproducible)

```bash
cd /home/vgpnk/Projects/shokunin
ls -1 {kumitate,kagi,kaidoku,chousa,kotodama,kake}-shokunin/{tools,scripts,corpus}
grep -rliE 'staged|collid|dedupe|duplicate|survivor|dead[_ -]?code|equivalent mutant' \
  {kumitate,kagi,kaidoku,chousa,kotodama,kake}-shokunin \
  --include='*.py' --include='*.sh' --include='*.mjs' --include='*.js' --include='*.ts'
grep -rniE 'comm -12|id collision|staged id' {kumitate,kagi,kaidoku,chousa,kotodama,kake}-shokunin
```

The `.mjs` pass was **not** optional: kumitate is a Node lane and its only lane-level
registry and mutant instruments are `.mjs` (`scripts/*.mjs`, 24 files). Kagi, kaidoku,
chousa and kotodama have no `.mjs`; kake has 3 — `scripts/{corpus-contract,freshness-sweep,probe-delta}.mjs`,
of which `corpus-contract.mjs` gates knowledge-metadata trios and lesson `## Gate` sections, not registry ids.

Lane shapes: **kumitate** has no `tools/` (gates live in `scripts/`, `.mjs`);
**kagi** keeps gates in `corpus/*.sh`; **kaidoku** `tools/round-NN/*` + `.ufo/gates/*`;
**chousa** `tools/*` + `corpus/evidence/roundNN/*`; **kotodama** `tools/*` +
`tools/gates/*` + `reports/round-NN/*`; **kake** `scripts/*` + `.ufo/waves/round-NN/*`.

## A — "which staged/imported ids collide with a registry"

| path | scope | vs `tools/staged-id-guard.py` |
|---|---|---|
| `kumitate-shokunin/scripts/source-dupes.mjs` | **lane-level, maintained, selftest, FAIL-CLOSED.** Intra-registry duplicate *document* groups: normalised URL + differing `scope`, pinned `known` set in `.ufo/pins/source-dupes.json`, DRIFT on new/stale/mismatched group. Parses the Registry section with **0–3 leading spaces** (`:44`, `:142`, `:158`, `:165`) and applies the census normalisation (scheme + trailing `/` + `#fragment` stripped, host lowercased; `:33-40`). | **Closest neighbour.** Same section/extractor idea and same document-identity idea, but registry-vs-registry (never registry-vs-staged), and normalised. The guard is staged-side and un-normalised. |
| `kumitate-shokunin/scripts/sources-check.mjs` | lane-level validator, contract `kumitate-sources-v1`; `ID_DUPLICATE` = E03 intra-registry id repeat (`:7-25`), `ROW_MALFORMED` = E01. | Adjacent only: intra-registry id duplicates, no staged side. **Its row regexes are column-zero only** (`:864-866`: `^\|[[:space:]]*S…`), so it would not see an indented collision — the exact blind spot the guard's `column0_miss` exists to expose, while the file claims "fleet `sources-census.sh validate` correspondence" (`:8`). |
| `kagi-shokunin/corpus/sources-census.sh` | lane-level registry gate (contract v1, 11 columns). `SC_DUP` = "an id used by more than one row" (`:32`, awk `:187-189`). | Adjacent: intra-registry dup only. Its grammar is the **opposite** of the fleet census on indentation — a leading space is `SC_MALFORMED`, "not silently uncounted" (`:26-31`), vs fleet/4-numeral `^ {0,3}\|` acceptance. The guard's 0-3-space extractor is correct for tameshi and the fleet census, **not** portable to kagi's contract. |
| `chousa-shokunin/corpus/evidence/round26-registry-oracle.py` + `.ufo/waves/round-26/falsify/FRegistryDuplicateId.md` | independent oracle for `verify-metadata --registry`; adjudicates "first row of a duplicated id wins" (`:12-16`) | Adjacent: intra-registry duplicate *resolution* semantics, no staged side. |
| `kaidoku-shokunin/tools/round-28/preseen-overlap.py` | test-selector pre-seen overlap against an evidence freeze (`:1-9`) | Different population (selectors vs registry ids). Names the same *shape* of question. |
| `kake-shokunin` `.ufo/waves/round-48..51/assimilation/*`, `corpus/lessons/round-51.md:67-73`, `.ufo/waves/round-51/w1/CriticIds.md` | **procedure + committed fixtures, no tool.** `reg-ids`/`staged-ids`/`collisions`; `guard/guard-registry.md` has an indented row, `guard/guard-collisions` = `S137` (round 48) and the round-51 `guard-col0` / `guard-col0-ids` are **empty** — the column-zero-blindness proof, committed. Lesson: "with the census parser's own 0-to-3-leading-space pattern (a column-zero-only pattern misses an indented collision)" (`round-51.md:69-70`). Round-48 seat item `make_spec.py:187` is the same reproduction verbatim. | **Nearest prior art for the whole capability**, but it stops at the intersection: shell `comm -12` over hand-kept lists. It has no `held`/`unmapped` split, no map admission, no injectivity or cascade. Its own critic asks for the two things the guard still lacks (`CriticIds.md:102-103`): URL as well as id, reported separately, and a pinned, revision-anchored staged read. |
| `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/renumber-staged.py` *(assimilation package, out of the six lanes — read-only, recorded because three lanes including tameshi are named in it)* | campaign renumberer. `:2-7` names the collisions ("kama 12, kotoba 1, **tameshi 1**"); `ROW_RE = ^\|\s*(S\d{3,})` is **column-zero only** (`:36`); assigns `nxt = max(reg)+1` then sequential (`:81-101`) with `used = set(reg)` only; remap is keyed by **round**, not id (`:85-90`). | Not a duplicate and not a guard: it *writes*. But it is the live instance of the arithmetic map the guard refuses, and its round key is the orthogonal scope to the guard's document key. |

Fleet-level, outside the six lanes: `scripts/sources-census.sh` accepts `^ {0,3}\|`
(`:541`, `:615`), `E03` duplicate id (`:641`), `E04` duplicate URL+scope (`:649`),
and owns the one URL normalisation in the fleet (`url_of`, `:600-608`).

## B — "classify a mutant survivor"

| path | scope | vs C1's K/D/E/U |
|---|---|---|
| `kumitate-shokunin/scripts/gate-mutants.mjs` | **lane-level**, contract `kumitate-gate-mutants-v2`, "round 43: kill predicate **K43**" (`:3`). Vocabulary: `KILLED` / `SURVIVED` / `UNSTABLE` / `drifted` (`:5-8`, `:149`). Survivors are resolved by **nomination**: the id is frozen into `FROZEN_IDS` with a `survivor/` label (`:203-245`, entries `:222-230`). | Adjacent and materially different: no `dead_code_only`, no `equivalent`; classification is binary and the survivor's disposition is an allowlist entry, not a rule. **It does test double-run stability** ("an immediate second run … same sorted FAIL case names", `:5-7`) — a hazard C1's K does not check. Note the name clash: kumitate's `K43` is not tameshi's `K`. |
| `kumitate-shokunin/.ufo/waves/round-61/build/MutDispatchGate/probe.py` | **wave-local, `/tmp`-bound, one target** (`dispatch-evidence.mjs`). "Survivor characterization": build a fixture the selftest does not contain, run pristine vs mutant, a behaviour difference proves **COVERAGE GAP (non-equivalent)**, else equivalent (`:2-8`, `:61-63`). | The only survivor *classifier* in the six lanes. Two classes only; **no dead-code construct anywhere in the fleet's six lanes**. Reachable by no lane entry point (it asserts `/tmp/kumitate-r61/MutDispatchGate`). |
| `kake-shokunin/.ufo/waves/round-37/c2_mutkill.py` | frozen counter, `killed >= 32 of 32`, jail-isolated fixtures, blind independent implementation. Emits `survivors` as an id list (`:288-293`). | Adjacent: counts kills, names survivors, classifies none. |
| `kagi-shokunin/.ufo/waves/round-24/tools/identity-swap.py` | count-preserving identity swap; prints `survived=<n> killed=<n> invalid=<n>` (`:27`, `:300`) | Adjacent: a survivor count, not a class. |
| kotodama `tools/check-draft-ids.py`; chousa `tools/quote-reopen.py`; kaidoku `.ufo/gates/c1-census-v10.py` | checked, different populations: draft-id *fragments* that name no registry row (`check-draft-ids.py:1-18`); quote truth fetched from the URL a `source_id` resolves to (`quote-reopen.py:1-12` — reads the registry, never compares id sets); scope/undeclared census counts (`c1-census-v10.py:1-12`). | no overlap |

## Verdict on `tools/staged-id-guard.py`

**No duplicate, and no sibling lane can answer it today.** Nothing in kumitate, kagi,
kaidoku, chousa, kotodama or kake takes two documents (lane registry + staged package)
and reports id collisions; every lane-level registry instrument is single-registry.
The nearest neighbours are kumitate `source-dupes.mjs` (same extractor + document
identity, intra-registry, normalised, pinned) and kake rounds 48–51 (same procedure,
committed fixtures, intersection only). The guard's three deltas — document-keyed
`held`/`unmapped` split, refusal of the naive arithmetic map with the cascade witness,
and map admission (injective, disjoint, covering) — appear in none of them.
The guard's `naive_map` refusal is not a strawman: `renumber-staged.py:81-101` is the
live arithmetic map it describes, and its `ROW_RE` (`:36`) is column-zero only.

## One verified divergence (found, not inferred)

The guard's document key is not the fleet census's document identity.
`document_key` returns the raw matched URL (`tools/staged-id-guard.py:86-98`:
`return found.group(0).rstrip('.,;)]')`). The census `url_of`
(`scripts/sources-census.sh:600-608`) strips `#fragment`, the trailing `/`, the
scheme, and lowercases the host; kumitate's gate applies exactly that normalisation
(`scripts/source-dupes.mjs:33-40`). Fixtures under `/tmp/tameshi-r43-ConnOverlap-fixture/`:

```
# registry S001 https://example.com/x ; staged S001 http://Example.com/x/ + S005
$ python3 -I tameshi-shokunin/tools/staged-id-guard.py --registry reg.md --staged staged2.md --json
{"collision_count":1,"collisions":["S001"],"cascade":[],"held":{},"unmapped":[],
 "refused":false,"verdict":"answered", ...}          rc=0

# same staged file with the URL spelled https://example.com/x
$ ... --staged staged3.md --json
{..., "held":{"S001":"S001"}, "refused":false,"verdict":"answered"}   rc=0

# the fleet census on the two spellings
$ bash scripts/sources-census.sh validate --file /tmp/.../cen.md
file	E04	S002 duplicate url example.com/x within scope s1
file	E11	S001 missing used-by p
rc=1
```

Consequence: a colliding staged row whose document the registry already holds, written
under any spelling the census normalises (`http`/`https`, host case, trailing `/`,
`#fragment`), is **neither `held` nor `unmapped`** and the tool exits 0 `answered` —
the third state its docstring does not admit. `refused` is `False` because
`refused = bool(unmapped) or bool(cascade)` (`:130`) and neither fires. Documents are
compared only for colliding ids (`:113-121`), so a fresh-id staged row carrying an
already-mined URL is invisible to the guard entirely, though the census calls it `E04`.

This does **not** falsify C3's counter: `.ufo/evidence/round-43/guard/measure.py`
re-derives `own_held` with the same exact-string join (`:94-95`, `:188-195`) and
compares to the tool's `held` (`:201`), so `live_held_agree=1` holds by shared
assumption. That is precisely the "internally consistent, externally unanchored"
defect kake's own critic names (`CriticIds.md:38`). C3's sentence "dedupes a staged
row whose document the registry already holds" is broader than the bytes.

## Affected axes, proposed move, risks, verification

**Axes.** C3 operability (the claim's scope), C2 calibration (the document-identity
notion is a calibration record: "same document" must mean the census's, or the record
is lane-private). C1 unaffected.

**Move (bounded, this round, report-only — no frozen byte touched).** Record the limit
in the round-43 C3 report as a named limitation, in the census's own vocabulary:
`held` is exact-string document equality, not `url_of` normalisation, and
staged-vs-registry *document* collisions for non-colliding ids are out of scope
(`E04` family). Queue as the next round's delta: adopt `url_of`
(`scripts/sources-census.sh:600-608`, mirrored at `source-dupes.mjs:33-40`) as
`document_key`, and report the two joins separately — id collisions and document
groups — which is kake `CriticIds.md:102-103` and fleet `E04` asking for the same
thing from two directions. A compatible synthesis, not an import: the guard keeps
its `held`/`unmapped`/map-admission structure; only the key's derivation and one
extra reported join change, and it stays a guard (never writes) unlike
`renumber-staged.py`.

**Risks.** (1) Editing `tools/staged-id-guard.py` now would break the freeze
(`17f6ef0…` includes the guard) and the C3 counter's `tool_sha_ok`; hence report-only
this round. (2) If the guard later normalises, the frozen counter would have to
normalise too or `live_held_agree` flips to 0 — the counter must gain the independent
join kake's critic demands. (3) A widening of `held` changes `refused` for live
packages: a row previously "answered" could become a dedupe, which is the intended
direction but must be re-measured, not asserted. (4) Do not port the 0-3-space
extractor into kagi: its contract makes an indented row malformed by design.

**Verification** (read-only, run by whoever takes the next round; not run here):
`python3 -I tools/staged-id-guard.py --registry <lane>/corpus/SOURCES.md --staged
/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md --json` before and after
the key change, plus `bash scripts/sources-census.sh validate` on the same registry,
diffing the document joins. The fixture pair above is the regression case.

## Limits

- I ran no sibling tool: `source-dupes.mjs`, `sources-check.mjs`, `gate-mutants.mjs`,
  `c2_mutkill.py` and `identity-swap.py` are characterised from their headers, contracts
  and code, not from execution. Their selftests were not run.
- I did not run the guard's `--selftest` or any round-43 counter (the deciding run is
  the L1's); only the three ad-hoc fixture invocations quoted above.
- The inventory is a repository grep over the named lanes at their working trees, not a
  revision-pinned survey; parked or deleted waves are not covered. Prose-only hits
  (`.md`) were read only where they carried a procedure (kake rounds 48–51).
- `/home/vgpnk/Projects/shokuknow` was read (headers, data files) and never written,
  fetched or pushed; no campaign tool was run.
- Scratch `/tmp/tameshi-r43-ConnOverlap-fixture/` deleted after the report was written.
