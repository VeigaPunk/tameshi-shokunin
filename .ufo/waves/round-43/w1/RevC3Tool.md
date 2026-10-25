# RevC3Tool — guard logic review (round 43, wave 1)

Seat: `L1Tameshi43.RevC3Tool`. Assignment: line-by-line review of
`tools/staged-id-guard.py` — `parse_rows`, `document_key`, `analyse`, `validate_map`, the
selftest — reporting every place code and docstring differ and every refusal path that cannot
fire. Read-only; no edits to the lane.

## Pins and what was actually measured

Reviewed bytes (my declared freeze, per the contract):

| thing | value |
|---|---|
| `tools/staged-id-guard.py` | sha256 `8140945a816873562eee8bcc6862d5e098f95b8083b4760b087812568f97b762`, 374 lines |
| freeze rev | `17f6ef0c72ec27e1aea305b5c95806b43bb2caef` |
| C3 counter | `.ufo/evidence/round-43/guard/measure.py` sha256 `6278edcd691e230b32383a8b2ac25f38910e17f3041e4082271a5863a8d78601` (read from the freeze blob; the on-disk copy was rewritten mid-wave, see *Drift*) |
| state at base `487b8f0` | tool absent → `tool_absent=1`, `C3_R43_PASS=false` (correct direction) |

Behaviour was probed by executing the tool (no `lsp` device is mounted and no Python language
server answers this repo — semantic checks are direct execution, not text grep).

**Headline.** At the declared freeze `C3_R43_PASS=false`, and the single failing predicate is
`safe_map_admitted=0`:

```
C3_R43: self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=0 selftest_cases=13 selftest_failed=0
staged_rows=103 live_collisions=6 live_collisions_agree=1 live_held=2 live_held_agree=1
live_unmapped=0 live_cascade=1 live_verdict=refused naive_map_refused=1 safe_map_admitted=0
map_dedupe_live=1 safe_floor=S256 C3_R43_PASS=false
```

The cause is one line. It is also the largest docstring divergence in the file: the docstring
says the map is validated for shape; the code validates the *concatenation* of the targets.

---

## Findings by severity

### F1 (critical, operability; claim-falsifying) — `validate_map:172` rejects every map with two or more entries

```python
169    targets = list(mapping.values())
170    if len(targets) != len(set(targets)):
171        reasons.append('map is not injective (two staged rows share a target)')
172    if not re.fullmatch(r'S\d{3,}', ''.join(targets) or 'S0'):
173        reasons.append('map has a target that is not an S-id')
```

`''.join(['S010','S011']) == 'S010S011'`, which can never fullmatch `S\d{3,}`. Therefore
**any** map with ≥2 entries gets `'map has a target that is not an S-id'` and is
`inadmissible` with rc=1. Only single-entry maps can be admitted. The empty map is refused too
(`''.join([]) or 'S0'` → `'S0'`, which needs three digits).

Evidence — the counter's own 6-entry by-document safe map
(`{S153:S105, S154:S106, S155:S256 … S158:S259}`), run on the real registry + staged package:

```
"map_below_floor": [], "map_clash": [], "map_dedupe": {"S153": "S105", "S154": "S106"},
"map_entries": 6, "map_floor": "S256", "map_ok": false,
"map_reasons": ["map has a target that is not an S-id"],
"map_staged_clash": [], "map_targets": 6, "map_uncovered": [],   → EXIT=1
```

Every rule the map does satisfy is empty; the only reason is the join. Isolated:

| map | collisions | verdict |
|---|---|---|
| `{S002:S050}` | 1 | `(True, [])` |
| `{S002:S050, S003:S051}` | 2 | `(False, ['map has a target that is not an S-id'])` |
| `{}` (package has no collisions) | 0 | `(False, ['map has a target that is not an S-id'])` |

One-line per-target repair, scored through the frozen counter at the allowed revs with the
allowed `--tool-file` control:

```
pinned_fixed  self_pin=1 selftest_failed=0 safe_map_admitted=1 C3_R43_PASS=true
```

So the frozen tool cannot claim the capability it was frozen for, and the whole failure is
`validate_map:172`. This is now recorded in the lane as amendment **A4** at HEAD `5cd2154`
(tool pin moved to `efa5f129…`), together with a `T4_multi_entry_map_admitted` selftest case.
`A4` is outside my declared freeze; I judged `17f6ef0` and mark below which findings survive
the A4 repair.

### F2 (high) — `--map` accepts the exact renumber the tool exists to refuse

Docstring L17–20 and L32–33: a colliding row with no document is *refused* because "a renumber
decision that is not tied to a document is arithmetic", and `exit 1 = the map is not
admissible (or a collision has no document)`. `validate_map` never consults
`base['unmapped']` (L162 computes `base`, L178–192 only use `staged`/`registry`/`floor`).

```
analyse:            unmapped=['S002'] refused=True
validate {S002:S050} → (True, [])        exit 0
```

A documentless collision is silently renumbered by any fresh-id map. Separately, `main`
(L344–353) overwrites `verdict` with `admitted`/`inadmissible` and drops the `analyse`
refusal, so a single `--json` payload can carry both:

```
{'refused': True, 'verdict': 'admitted', 'map_ok': True, 'map_reasons': []}   exit 0
```

`refused` and `verdict` contradict each other; the docstring lists both fields as the answer.
Survives A4 (verified on the `5cd2154` blob).

### F3 (high) — the held-dedupe answer is unrepresentable: `analyse:117-122` vs `validate_map:205-207`

`analyse` reports a collision whose document the registry already carries as `held`, i.e.
"dedupe to the registry id, do not append". When the held registry id *is the staged id*, the
only faithful map is the identity, which `validate_map` refuses:

```
analyse                 held={'S002': 'S002'}
validate {S002:S002}    (False, ['map leaves a colliding id on itself: S002'])
```

The self-map rule fires after the dedupe branch has already accepted the target as a
by-document dedupe (L181–184), so the tool contradicts itself on its own stated remedy. Not
reachable on today's live pair (the two live `held` entries map S153→S105 and S154→S106, not
to themselves), so this is latent rather than live. Survives A4.

### F4 (high) — `document_key:94` strips hex runs from path heads → false `held` (silent non-append)

```python
57  HEXISH = re.compile(r'[0-9a-f]{7,40}')
93  head = re.split(r'\s+[—–]\s+', source)[0].strip()
94  head = HEXISH.sub('', head).strip()
```

Nothing in the docstring mentions SHA stripping. Consequences, measured:

| source head | key produced |
|---|---|
| `deadbeefcafe/notes.md` | `/notes.md` |
| `abc1234.md` | `''` (→ false `unmapped` refusal) |
| `/data/deadbeef/notes.md` | `/data//notes.md` |
| `/data/feedface/notes.md` | `/data//notes.md`  ← same key |
| `corpus/deadbeefcafe/notes.md` | `corpus//notes.md` |

Two *different* documents therefore share one key, and `held` reports the registry already
carrying the staged document:

```
document_key("/data/deadbeef/notes.md") == document_key("/data/feedface/notes.md") == '/data//notes.md'
analyse → collisions=['S002'] held={'S002': 'S040'} unmapped=[] refused=False
```

That is the tool's own failure mode inverted: it tells the operator "dedupe, do not append"
for a genuinely new source, and nothing downstream re-checks. `abc1234.md` is the mirror case —
a real document key deleted, so the row is refused as `unmapped`.

Exposure today: the staged package has 0 rows without a URL, so no live false `held`; but the
registry has **14** rows that carry no URL and rely on the path fallback (S031–S034 among
them), so any future staged row with a hex-looking path segment will false-match. Survives A4;
per `MutC3Selftest` it is repaired in the tree after A4 (`normalise_document`, `HEXISH` gone),
which is beyond both my declared freeze and the A4 pin.

### F5 (medium) — `validate_map:188,191` exempts whole-set maps from both rules the docstring states

```python
174    whole_set = len(mapping) == len(staged)
188        if target in staged and not whole_set:      # staged-clash
191        if not whole_set and id_number(target) < id_number(floor):   # safe floor
```

Docstring L159–160 states both rules unconditionally ("above the safe floor for a partial map,
and never an id another staged row still holds"). Demonstrated, one-row package,
`safe_floor=S011`:

```
validate {S002:S003}  (True, [])                                  # below floor, admitted
same target, partial map (2 staged rows)
validate {S002:S003}  (False, ['partial map targets are below the safe floor S011: S003'])
```

Pre-A4 the exemption was unobservable for packages with ≥2 rows, because every such map died at
L172 first. After A4 it is live. The staged-clash exemption is sound only because an injective
map over *all* staged keys vacates them — a property nothing in the code checks or asserts; a
whole-set map that targets a staged-only id is admitted on the strength of it. Survives A4.

`MutC3Selftest`'s M4 removes **both** exemptions and survives every selftest that exists —
13/13 at `17f6ef0`, 14/14 at `5cd2154`, 23/23 on the tree after that — while changing behaviour
(a whole-set `S011→S004` under `floor=S012` is admitted today and refused with "partial map
targets are below the safe floor S012: S004" by M4). So the whole-set rule is unpinned in both
directions: the exemption is load-bearing for the current admission semantics, and no case
asserts it either way. The contract should state the whole-set rule before any case encodes it.

### F6 (medium) — several of the tool's rules are measured by neither the selftest nor the counter

Built from the pinned blob, scored through the frozen counter at the allowed revs with
`--tool-file` (all with the F1 repair applied, so admission is reachable):

| mutant (from pinned bytes) | selftest | counter |
|---|---|---|
| `validate_map` floor check deleted (L191–192) | 13/13 pass | **`C3_R43_PASS=true`** |
| duplicate-id refusal deleted (L76–77) | 13/13 pass | **`C3_R43_PASS=true`** |
| self-map rule deleted (L205–207) | 13/13 pass | **`C3_R43_PASS=true`** |
| staged-clash reason deleted (L196–198) | fails 1 | `naive_map_refused=1` (frozen bytes) |
| dedupe document comparison replaced by bare accept | fails 1 | — |
| `ROW_RE` replaced by column-zero (L54) | fails 7 | all live checks unchanged |
| both `not whole_set` exemptions removed (L188/L191) — M4, measured by `MutC3Selftest` | **13/13 pass**; 14/14 at `5cd2154` | **`C3_R43_PASS=true`** |

Read: the claim's "new documents take ids at or above the safe floor" is **not measured at all**
— the counter goes green with the floor rule absent. The "refuses its own naive arithmetic map"
target is satisfied **vacuously** at the freeze: the naive map has 6 entries, so F1 refuses it
whether or not the staged-clash rule exists. And on the live pair the census-valid 0-3-space
pattern is not load-bearing either — both texts are entirely column-0 (`indent_hist={0:113}`
registry, `{0:103}` staged), so a column-zero extractor scores identically on the live run and
only the fixture (T1) distinguishes them.

### F7 (medium) — selftest structure

13 cases at the freeze (`selftest:256-316`). Every case that asserts admission uses a
**one-entry** map (`T4_valid_map_admitted`, `T5_dedupe_map_admitted`), which is why F1 was
invisible. No case exists for: `below_floor`, `selfmap`, duplicate-id refusal, whole-set maps,
documentless-under-`--map`, the empty map, path-head documents (`HEXISH`), or row shapes other
than column-0 and 2-space. `T6` exercises the malformed threshold only at 2 cells, so the
`<5` boundary is never probed. Survives A4 except that one multi-entry case was added.

### F8 (medium) — bad `--map` input crashes instead of a setup refusal

Docstring L34: `exit 2 = setup refusal (missing file, malformed row, bad map file)`.

```
{'map': {'row-2': 'S050'}}      → ValueError: invalid literal for int() with base 10: 'ow-2'   (via L177 sort key)
{'map': {'S002': 10}}           → TypeError: sequence item 0: expected str instance, int found (L172, pre-A4)
```

Both are uncaught tracebacks with no JSON and rc=1, indistinguishable by return code from
"inadmissible". Survives A4 (the sort key at L177 is untouched; a non-str target now raises
inside `re.fullmatch`).

### F9 (low) — the documented map-file envelope is not implemented

Docstring L27–29: the map file is `{"map": …, "staged": path, "registry": path}`. `validate_map`
reads only `map` (L165); `staged`/`registry` are never consulted. A map built against different
inputs is silently accepted:

```
{'map': {'S002': 'S050'}, 'staged': '/nonexistent', 'registry': '/nonexistent'} → (True, [])
```

Survives A4.

### F10 (low) — `next_free` names an id the same run declares occupied

`analyse:142` sets `next_free = S(registry_max+1)`, which is exactly `naive_map`'s first target
and is in `cascade`. Live output: `next_free='S159'`, `cascade` contains `S159`; fixture:
`next_free='S003'`, `cascade=['S003']`. The truthful answer, `safe_floor='S256'`, is computed
(L145) but never printed in the human mode (L362–365). Docstring L43–44 lists `next_free`
without a caveat. Survives A4.

### F11 (low) — docstring ↔ code divergences (each verified)

| docstring | code |
|---|---|
| L45 `column0_extract` is a `--json` key | no such key; actual keys are `column0_collisions`, `column0_miss` (L147–148). The listed key set also omits `registry_max`, `staged_max`, `safe_floor`, `registry_docs`, and every `map_*` key |
| L17–18 "no URL/DOI **and an empty source cell**" | a *non-empty prose* source cell is unmapped too (L98): the selftest's own T2 fixture is `nothing here` |
| L8, L87 "URL/**DOI**" | `URL_RE` is `https?://` only; a DOI outside the source cell yields `''` (`['S001','Some prose title','docs','A','10.1000/xyz123']` → `''`). A DOI in the source cell only works by falling through to the path heuristic |
| L30 "injective, **disjoint from the registry**, and covering every collision" | L181–184 admits a registry target for by-document dedupe, as L157–158 correctly says. The two docstrings contradict each other |
| L65 rows carry `document`, `cells`, `lineno` | `cells` and `lineno` are stored and never read (0 occurrences) |
| L73 "malformed row" | threshold is `len(cells) < 5` while the schema (and every fixture) has 11 columns; a 5–10 cell row is accepted silently. Verified: 5 cells `ACCEPTED`, 4 cells refused |
| L50 `import os` | unused (0 uses) |
| L156–160 "never an id another staged row still holds" | skipped for whole-set maps (F5) |

### F12 (low) — rows that look like rows are silently skipped, with no refusal

`ROW_RE:54` requires `S` + ≥3 digits + spaces then `|` in the id cell. A registry row annotated
in its id cell, e.g. `| S002* | … |`, is not parsed at all:

```
'| S002* | … |'        → staged_rows=0, collisions=[]
'    | S002 | … |'     → staged_rows=0   (4 spaces; out of corpus, but silent)
'\t| S002 | … |'       → staged_rows=0   (tab-indented; silent)
```

For the marked-id case this is a collision false-green: the id exists in both files and the
tool reports none. There is no "unparsed row" counter or refusal. Also `column0_*` (L109–111)
is computed from the staged text only, so the indented-row proof never covers the registry
side. Survives A4.

---

## Refusal paths / branches that cannot fire

1. **`document_key:92`** `cells[1] if len(cells) > 1 else ''` — the `''` branch is unreachable:
   `parse_rows:73` refuses `<5` cells *before* calling `document_key` (single call site, L79),
   so `len(cells) > 1` always holds. Dead code.
2. **`validate_map:188` (`staged_clash`) and `:191` (`below_floor`)** — both are gated on
   `not whole_set`, so they can never fire for a whole-set map. Pre-A4 that was unobservable
   (F1 blocked every ≥2-entry map); post-A4 a whole-set map may target a staged-only id or a
   below-floor id and be admitted (F5).
3. **`validate_map:170` (non-injectivity) could not be the deciding reason at the freeze** — a
   1-entry map is trivially injective, and every ≥2-entry map already failed L172. It only ever
   co-fired; the selftest asserted `any('injective' in r …)` and so passed on a map refused for
   the unrelated reason. A4 removes the cause.
4. **Injective dedupe is unrepresentable** — two staged rows carrying the same document that
   the registry holds must both dedupe to one registry id, which L170 rejects as
   non-injective although dedupe appends nothing:
   `{S002:S001, S003:S001}` → `['map is not injective …']`.
5. **`parse_rows:76-77` (duplicate id)** fires correctly but has no selftest case and no live
   instance, so it is an entirely unmeasured guarantee (F6).

---

## Drift observed while reviewing (not a defect of the tool; affects decidability)

- The lane re-froze while I worked: HEAD is now `5cd2154` ("freeze A4/A5") with amendments
  **A4** (guard map-shape repair — exactly F1 — tool pin `8140945a`→`efa5f129`) and **A5**
  (C1 reachability gate + tool-pin source; C3 counter pin `6278edcd`→`fbc8ad3c`). Both record
  `rule_changed: false`. Note the contract's own `amendments_note` says amendments change
  "citations and disclosures only"; A4/A5 also move `tool_sha256`, `frozen_tools` and
  `claims.C3.counter_sha256`. That is a provenance call for the L1 and `RevProvenance`, not a
  code defect; I only record it because my ticket still names `17f6ef0`.
- Consequence: the on-disk counter now self-pins to `fbc8ad3c`, so running it with
  `--freeze 17f6ef0` yields `self_pin=0` (pin mismatch). The `17f6ef0` measurement above was
  taken with the counter bytes from the freeze blob (`git show 17f6ef0:…/measure.py`,
  `self_pin=1`). Any 17f6ef0 receipt must use those bytes.
- `RevProvenance` reports the on-disk tool has since moved to a third version (`2484da72…`)
  pinned by neither freeze. The counter reads `git show REV:tools/staged-id-guard.py`, so
  measurements are unaffected; a tool that read the worktree instead would score
  `tool_sha_ok=0`.

## Residual risk and verification gaps

- **The tool's core promise is still unenforced after A4**: F2 (documentless renumber under
  `--map`), F3 (self-dedupe unrepresentable), F4 (hex-collapsed documents produce a false
  "already held" — present at the freeze and at A4, reported fixed later in the tree), F5
  (whole-set maps escape the floor, and the whole-set rule itself is asserted by no case —
  M4 survives everywhere), and F6 (the floor is not measured). F4 is the one that can lose
  data silently — the tool tells the operator not to append.
- I did **not** measure at `5cd2154` (not an allowed measurement rev); the A4 blob was probed
  as code only, to mark which findings survive.
- `safe_map_admitted=1` with `--tool-file` at `17f6ef0` is a **control**, not a measurement. The
  deciding run must be made against whatever freeze rev the L1 declares.
- The counter's own blind spots, for the report's calibration section: `dedupe_live`
  (`measure.py:223`) reads `safe_doc` even when the map was refused, so it reports
  `map_dedupe_live=1` on an inadmissible map (the freeze output does exactly that) — its
  docstring L30 says "the admitted safe map". `live_cascade` (L203) reads the tool's own
  `cascade` field rather than an independent computation, and `own_held` (L189–193) joins on
  URLs only while the tool joins on URL-or-path, so a path-keyed document would disagree
  spuriously.
- `MIN_CASES=13` is a floor, not a check on what the cases assert: deleting the floor,
  duplicate-id and self-map rules leaves the selftest at 13/13 (F6).

## Tools installed

None. No package manager transaction, no `uv`/`npx`/binary install was performed or needed.
Scratch: `/tmp/tameshi-r43-RevC3Tool-run/` (removed before return; the mutants are 3-line
diffs reproduced by the table in F6, and every decisive output is quoted above verbatim).

Assimilation: none (read-only package; nothing adopted).
