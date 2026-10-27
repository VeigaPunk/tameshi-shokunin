# T53W1LabLint — QUALITY-104 receipt (round 53, wave 1)

Seat: `T53W1LabLint` (executor, wave-1 labrat; axes: operability).
Subject: the 30 SKILL.md sections frozen in `.ufo/evidence/round-53/c1/lost-headings.json`,
re-read at **C\* = `a41195dfc13a73958e4c5228ec196b28d03ded03`**.
All reads are `git show <rev>:SKILL.md` (git objects only). The working tree was never read
for section bytes. No file under `SKILL.md`, `tools/`, `corpus/`, `.ufo/evidence/` or
`MANIFEST.json` was modified; no git/jj mutating command was run.

---

## 0. Verdict

| QUALITY-104 check | result | un-fixed hits |
|---|---|---|
| C1 duplicate parentheticals (`(…since round 51) (…since round 51)`-class) | **clean** | **0** |
| C2 immediate word repetitions (prose) | **clean** | **0** |
| C3 known pattern P1 `'(ten since round 51) (ten since round 51)'` | **gone at C\*** | **0** |
| C4 known pattern P2 `'still not embedded at this boundary (both are legs 5–6 since round 10-2'` | **gone at C\*** | **0** |
| C5 `/tmp/` occurrences in the 30 sections | **NOT clean** | **8** |

**Overall: the QUALITY-104 lint does not return a clean PASS.** The four text-lint classes
(C1–C4) are clean — the fix pass introduced no duplicate parenthetical and no word
repetition, and both known round-52 patterns are demonstrably gone. The `/tmp/` arm is
**not** clean: **8 registry rows in the two gate/probe-registry sections still describe the
patched tools' selftest scratch as living under `/tmp` with "TMPDIR ignored"/"hardcoded"**,
which the C\* tool bytes contradict. Those 8 rows are the only un-fixed hits and they are
all of one class (§4, F1–F8).

Two **decisive-run blockers** outside the QUALITY-104 checks were found while executing the
scan and are reported in §6 (A1–A3). They are evidence-backed and reproducible.

---

## 1. Method (what was actually run)

### 1.1 Section split — the frozen monitor's, not a reimplementation

`git show a41195df:.ufo/evidence/round-18/measure.py` was extracted to scratch and its
`sectionize()` imported directly, so the section boundaries are the cold-read monitor's own
(`HEADING_RE = ^#{1,3}(?:\s|$)`, fences excluded, trailing whitespace-only lines stripped,
joined with `\n`, no trailing newline, sha256 over UTF-8 bytes with `surrogateescape`).

* 30/30 frozen headings resolved **exactly once** each in the C\* sectionize output (no
  duplicated headings among the 30).
* For every one of the 30 sections I re-derived the body from the C\* line range and
  re-hashed it: **30/30 sha256 self-checks passed** against the module's own `sha256`
  field, i.e. my line-range split reproduces the monitor's split byte-for-byte.
* Section line ranges and sha256 at C\* (for the readers' cross-check):

```
## Context gate classification and explicit exit classes — round 15   1616-1682  132cfb9ef1aa07111af42389e4fe862152e3118b3a8bb66f1d84a6a332e7edf6
## Effective expectation reconciliation — round 14                     1570-1603  664a9dfb18fc4318feb4321cc23ad69ffd742e5e37c1477b7b63abd8d05827e1
## Live-tree re-pin and entry-command monitor — round 17                1821-1852  037c9df3076fc7ada495b906b9bf458e9d06099bfaf9d1270b88de0acb4151f3
## Mutation-sweep recipe — numbered steps; bounded cold-read evidence  131-245   71ee856c8bc844468850aee317ad0dd09c6ad425653a415f6ede907dd12f712a
## Pin disposition and provenance correction — round 13                  1524-1554  ad8d6c4010f2c584a8fd34795625d66ab1a7ffcc91463a49e6d122ca06e4bf15
## Repeated controls and gate registry — round 12                       1486-1505  532bebc8fad6dadff4ef3581677a15230b994cbbac56dbdaa571e59204cf0d74
## Standing rules                                                        17-29     374964f40ab5ff71fd4713282867b360506d23c1918eb1c627645cdb03639053
## The leg ledger — replay, receipt, and how it is read (round 7, measured) 921-934  8bc5b3f5b95c26a9aac8aa05d7ba4c203fe2d2dde3885f9afc3d105996f04f77
## The operator's runbook and the six-leg regression (round 10, measured) 1278-1286  e52321d2152b65c88894a72fd91b594dc7aabfb1c5bea9ed283cbdd81ec1664d
## The re-sweep cadence and the six-case confidence statement (round 8, measured) 1012-1022  bab481fd3488f9c38656856f93b054b897d7acad5923abcb5bb0fe6b4ac63eed
### Gate/probe registry                                                 1506-1523  c1aabe900e6fbc46288d2ff241348a5fba8481388979ed62d7720dff0b244c65
### Reading a receipt — the discipline                                  967-1011   09151f506e87add7fcf41ad5bff76c92c371e870b53b2cc1eec26d9db14431c5
### Round-13 gate/probe registry                                         1555-1569  cfe1211232579bcfe7195d81b3932f2bc08109b30d58a3c853f2aff608514e50
### Round-14 historical registry — superseded by round 15               1604-1615  06a6864fb05fd63df168597696407397c7d3f4d47337556c25ab60393fb959af
### Round-15 gate/probe registry                                         1683-1713  b814e0afbad4c270b5d2d973639df287e982be1dbfac9deae8d9444fb57c1620
### Round-17 gate/probe registry — re-pin and monitor                    1853-1861  ad2320cb7770e47aa5fa628f0a0aa96e751e42c821cff4fe9d0c9fe03af0dcd9
### Round-18 gate/probe registry — routed-defect closure                1932-1944  1f0a60ec99834f64de35d40b845f2c71381b15e8b24310eaf8ffa8028379e439
### Round-21 gate/probe registry — finite environment differential       1971-2110  eccd3ec82207fa69cee544f8f4ebfc0f9a473fe7254b8041ae2f5924f8d00a06
### Round-26 gate/probe registry — report interop                       2139-2178  5399e46663220dea7df1c4ae9dc1b2871150e73aabe007d1371aa2a80e1a8e93
### Six-case confidence statement (round 8, measured)                   1094-1156  71c46c773e7f80782caee328f9f1e8bdb35e6f87ce5f498c703a0e2da849a206
### The map — where a reader enters, artifact by artifact                1387-1402  56faf129bad7bfce6649c19e99b4cc9981019a322e828c09fb74c21d52fd5333
### The re-pin semantics, as executed                                    1232-1247  0767d32fa85ab5591b3c170d27be7cb69a40e04be5859c52a992fa88a7bf73f5
### The receipt at this boundary                                          1214-1231  a44eec946e9adcfcb8f864f89b2f4de3925614ace891edea212dca7d951ca90e
### The service's limits — what tameshi refuses to mutation-test        1248-1277  37d63abf882e89d8103fb2618d8622c78da60eacfac75352851687e42eea7590
### The six-leg regression — usage and this round's receipt              1308-1371  45fe934f6254c9f95e20f8444f4a6a435d1c818e07f84290e1a4a0de8b119232
### The tick and the pin read                                             1023-1070  0221fc822c87f3aff940aa6ed46e7b06cd649b37165f64d3400641c1d2256cda
### The tick, executed                                                    1166-1213  d58978b5611e65939b188704ce32de562ddce854885aee7a85cb24858707b2f0
### Triggers T1–T3 and the re-pin rule                                   1071-1093  2350210704efcc3becfbcd40a63775ad591910039744ac6d072881b3deef7801
### Using the ledger                                                       935-966   1a6d9681bd90321ff6e66fa9887ed7e31026e40942aa02d2bbed11a74d2390fe
### What stays open — named, never closed by prose                        1456-1470  6716afc89e85379975438fe58a3ac23288a393fdd0d4058139cf9b1fafb352ff
```

### 1.2 Base for the delta

Base = `6db1d220b337c35ff1e25bf9cfd74abc9db1498d` (the round-53 base; the round's own fix
pass is `218bc6b5`, whose content commit is C\*). Section bodies were extracted at base with
the *same* frozen `sectionize()` and compared to C\*. **12 of the 30 bodies changed**
base→C\*, 18 are byte-identical:

* edited: Mutation-sweep recipe; Standing rules; The leg ledger; Reading a receipt;
  Round-21 gate/probe registry; **Round-26 gate/probe registry — report interop**;
  The map; The receipt at this boundary; The service's limits; The six-leg regression;
  The tick, executed; Triggers T1–T3.
* not edited: the other 18 (Context gate classification; Effective expectation reconciliation;
  Live-tree re-pin monitor; Pin disposition; Repeated controls (round 12); Operator's runbook;
  Re-sweep cadence; **Gate/probe registry**; Round-13/14/15/17/18 registries; Six-case
  confidence statement; The re-pin semantics; The tick and the pin read; Using the ledger;
  What stays open.

This matters for §4: the two registry sections that carry the 8 stale rows are
"### Round-26 gate/probe registry — report interop" (**edited** by the fix pass) and
"### Gate/probe registry" (not edited).

---

## 2. C1 — duplicate parentheticals: CLEAN (0 un-fixed hits)

Three independent detectors, all over the 30 C\* section bodies:

| detector | base | C\* | notes |
|---|---|---|---|
| adjacent-identical parenthetical, same line, markup stripped | 1 | **0** | over the whole file |
| adjacent-identical parenthetical, section body joined across line breaks | — | **0** | whole file also 0 |
| repeated `since round NN` parenthetical, exact, within a section | — | **0** | 11 such parentheticals at C\*, all distinct |
| repeated `since round NN` parenthetical, near-dup (ratio ≥ 0.75) within a section | — | 1 | see below |

The single base hit was at base L1305 and is the known pattern P1 (§3).

The one C\* near-dup pair is **not** a duplicate parenthetical: C\* L1311
`**ten** since round 51` (the leg count in the six-leg-regression usage) and C\* L1368
`ten-leg since round 51` (a ledger-row description). Different sentences, different facts,
57 lines apart — a legitimate re-mention, not a repeat of one clause. Not a finding.

A broader sweep (any parenthetical text repeated ≥ 2× within a section) produced 6 hits, all
present identically at base and all structural table-cell artefacts, not clause repeats:

* `(mutation-case-kagi-census.md:50-53)` ×2 — Mutation-sweep recipe, L213 (round-3 result)
  and L243 (cost profile). Two different facts citing the same note.
* `(round 18)` ×3 — Round-18 registry, L1937/1938/1939, one provenance tag per tool row.
* `(same registry section; same-ground calibration)` ×2 — Round-21 registry, L2017 (round-23
  addition) and L2050 (round-24 addition).
* `(usage)` ×13 across the Round-26 registry — the verdict-map cell of each row.
* `(r8)` ×2 — The tick and the pin read, L1050/1051, a table column value.

All are byte-identical at base and C\*; the fix pass changed none of them.

---

## 3. C2/C3/C4 — word repetitions and the two known patterns: CLEAN (0 un-fixed hits)

### 3.1 Immediate word repetitions — 0 un-fixed

A fence-aware prose scan (``` fences skipped, stop-words excluded) over the 30 C\* sections
returns **41** immediate word repetitions; the same scan over the base 30 returns **41**, and
the `(heading, word)` multisets are **equal** — the fix pass introduced **none** and removed
none. Every one is a markdown pipe-table cell boundary (e.g. `… | json | json | …` at
C\* L1590, `… could-not-evaluate could-not-evaluate …` at C\* L2151) or a single-letter
table column separator, not prose repetition. Zero are fix-pass artifacts.

The one same-line hit in the whole file, `live live` at C\* L1174, lies **inside** a fenced
code block (fence at L1173–L1181) and is a fixed-width table header —
`case recorded-rev live-HEAD anc pin==live live==HEADblob worktree reading` — two adjacent
column headers. It is byte-identical at base (base L1172) and is not prose.

### 3.2 Known pattern P1 — gone

Literal byte string `(ten since round 51) (ten since round 51)`:

```
base 6db1d220 : 0 occurrences
C*  a41195df  : 0 occurrences
```

**Byte-level caveat the wave-2 falsifier must know.** At base the duplicate exists in a
*markup-decorated* form — base L1305 reads:

> `uncommitted worktree file at this write), \`--regression\` replays **six** in r10-2 (**ten** since round 51) (ten since round 51)`

so the first parenthesis is `(**ten** since round 51)`, not `(ten since round 51)`. A literal
`git show … | grep -c '(ten since round 51) (ten since round 51)'` returns **0 at base** for
this pattern; only the markup-stripped form matches:

```
base, markup stripped (`sed 's/\*//g'`): 1
C* , markup stripped                     : 0
```

The adjacent-duplicate detector (markup-normalised) sees it at base and **not** at C\*.
For the wave-2 base-shows arm to be sound it must grep `since round 51) (ten since round 51)`
or strip markup — the plain literal as written in the wave-2 spec item will read 0 at base
and could masquerade as "pattern never existed".

At C\* the sentence now reads (C\* L1309–L1310):

> `uncommitted worktree file at this write), \`--regression\` replays **six** in r10-2 (**ten** since round 51)`
> `embedded legs (list \`tools/mutate-and-run.sh:88-97\`; sources \`:98-121\`;`

— one parenthetical, no repeat.

### 3.3 Known pattern P2 — gone

Literal byte string `still not embedded at this boundary (both are legs 5–6 since round 10-2`:

```
base 6db1d220 : 1 occurrence
C*  a41195df  : 0 occurrences
```

Base L1226 read `Cases 5–6 were still not embedded at this boundary (both are legs 5–6 since
round 10-2 — \`tools/mutate-and-run.sh:92-93\`)`. At C\* (L1228–L1229) it reads:

> `read \`stale\`. Cases 5–6 were not yet embedded at this boundary (they became legs 5–6 at r10-2; the current tool carries them at \`tools/mutate-and-run.sh:88-97\`): their rows carried no \`REGRESSION\``
> `line at this boundary — named debt, not smoothed (\`fleet-kill-rate-ledger.md:282\`; the debt was retired when the legs embedded).`

The replacement's pointer `tools/mutate-and-run.sh:88-97` was checked against C\*: those ten
lines are the leg registry (`js-kimi-census` … `bash-drift-pins`), and base `:92-93` is the
same list two lines earlier — so the re-pin is consistent with the C\* runner bytes.

---

## 4. C5 — `/tmp/` in the 30 sections: **8 un-fixed hits** (the only un-fixed class)

### 4.1 Inventory at C\* (29 `/tmp` mentions, base 34)

| class | count | lines |
|---|---|---|
| historical ER-4 quote (expected) | 1 | 1169 |
| scratch-directive mentions (expected) | 6 | 25, 939, 1327, 1391, 2156 (×2) |
| dated historical receipt paths (HOLD) | 12 | 988, 1042, 1068, 1111 (×2), 1169, 1193, 1217, 1218, 1224, 1341, 1499 |
| truthful rows for un-patched tools (HOLD) | 2 | 2167, 2168 |
| **stale rows contradicting the C\* tool bytes (FINDING)** | **8** | **1510, 1511, 2149, 2151, 2153, 2158, 2161, 2163** |

Per-section `/tmp` counts (base → C\*), for the L1's cross-check:

```
## Mutation-sweep recipe                                2 -> 0   (EDITED)
## Standing rules                                       1 -> 1   (EDITED)
### Round-21 gate/probe registry                        2 -> 0   (EDITED)
### Round-26 gate/probe registry                       11 -> 10  (EDITED)
### Reading a receipt — the discipline                 1 -> 1   (EDITED)
### The map                                             1 -> 1   (EDITED)
### The receipt at this boundary                        3 -> 3   (EDITED)
### The service's limits                                0 -> 0   (EDITED)
### The six-leg regression                              2 -> 2   (EDITED)
### The tick, executed                                  3 -> 3   (EDITED)
### Triggers T1–T3                                      0 -> 0   (EDITED)
## The leg ledger                                       0 -> 0   (EDITED)
## Repeated controls and gate registry — round 12       1 -> 1
### Gate/probe registry                                 2 -> 2
### Six-case confidence statement (round 8, measured)   2 -> 2
### The tick and the pin read                           2 -> 2
### Using the ledger                                    1 -> 1
(all other 14 sections: 0 -> 0)
```

### 4.2 Why the 8 rows are findings

The round-53 fix pass (`218bc6b5`) patched **7 tools** to honour `TMPDIR`, replacing
`dir="/tmp"` with `dir=tempfile.gettempdir()`. Verified at C\*:

```
tools/registry-check.py:766      work = tempfile.mkdtemp(prefix="tameshi-registry-check-", dir=tempfile.gettempdir())
tools/registry-check.py:917      prefix="tameshi-r17-registry-check-selftest.", dir=tempfile.gettempdir()
tools/repeat-control.py:597      tempfile.mkdtemp(prefix="tameshi-r12-repeat-control-selftest.", dir=tempfile.gettempdir())
tools/bash-witness-study.py:1241 prefix="bash-witness-selftest-private.", dir=tempfile.gettempdir()))
tools/context-capture.py:1625    tempfile.mkdtemp(prefix="context-capture-selftest-", dir=tempfile.gettempdir())
tools/evidence-disposition.py:2351 tempfile.mkdtemp(prefix="tameshi-r14-evidence-disposition-selftest.", dir=tempfile.gettempdir())
tools/pin-disposition.py:706      tempfile.mkdtemp(prefix="tameshi-r13-pin-disposition-selftest.", dir=tempfile.gettempdir())
```

`git grep -E 'dir\s*=\s*["'\'']/tmp'` over `tools/` at C\* returns **0** hits, so the C2
counter's grep arm is green — but SKILL.md's *prose* about those tools still says `/tmp`.
The fix pass updated only the two **env-diff** rows (C\* L1982 now
`--out "$HYAKU_SCRATCH/tameshi-f5.json"`, C\* L2152 now
`sandboxes under \`$TMPDIR\` (\`tameshi-r21-envdiff.*\`)`); the other six tools' rows were
left describing the pre-patch behaviour. Each finding below is a statement in a scanned
section that **does not hold at C\***.

The counter's own docs arm does not reach these rows: its four patterns are
`/tmp/tameshi-f5.json`, `/tmp/tameshi-r21-envdiff`, `mkdir -p /tmp/<lane>-r<round>` and
``Scratch for a sweep: `/tmp/`` — all 0 hits at C\* — while **none** of the 8 stale rows
matches any of them (checked programmatically: `counter would catch … : False` for every
one). So C2's docs check passes while the contradiction stands.

**F1** — `### Round-26 gate/probe registry — report interop`, C\* L2161 (row
`tools/registry-check.py`):

> `selftest and --rev fixture trees via mkdtemp under /tmp (hardcoded, TMPDIR ignored), removed afterwards`

Fails: at C\* `tools/registry-check.py` uses `dir=tempfile.gettempdir()` at **both** sites
(:766 clone scratch, :917 selftest scratch), so TMPDIR is honoured and the path is not
hardcoded. This is the strongest of the eight — the row asserts the exact opposite of the
patched bytes. The same section's env-diff row was rewritten to `$TMPDIR` in the same fix
pass, so the table now contradicts itself.

**F2** — `### Round-26 gate/probe registry — report interop`, C\* L2149 (row
`tools/bash-witness-study.py`):

> `selftest writes a private fixture tree under a hardcoded /tmp (TMPDIR ignored)`

Fails: `tools/bash-witness-study.py:1241` at C\* is
`prefix="bash-witness-selftest-private.", dir=tempfile.gettempdir())`. "TMPDIR ignored" is
false at C\*. (The tool's own docstring no longer says /tmp — the row outlived the patch.)

**F3** — `### Round-26 gate/probe registry — report interop`, C\* L2151 (row
`tools/context-capture.py`):

> `selftest fixtures under /tmp/context-capture-selftest-*, removed in finally`

Fails: `tools/context-capture.py:1625` at C\* is `dir=tempfile.gettempdir()`; the fixture
root follows TMPDIR, not `/tmp`.

**F4** — `### Round-26 gate/probe registry — report interop`, C\* L2153 (row
`tools/evidence-disposition.py`):

> `selftest fixtures under /tmp/tameshi-r14-evidence-disposition-selftest.* removed on pass, kept on failure`

Fails: `tools/evidence-disposition.py:2351` at C\* is `dir=tempfile.gettempdir()`; the root
follows TMPDIR, not `/tmp`.

**F5** — `### Round-26 gate/probe registry — report interop`, C\* L2158 (row
`tools/pin-disposition.py`):

> `selftest writes isolated /tmp/tameshi-r13-pin-disposition-selftest.* fixtures, removed on PASS`

Fails: `tools/pin-disposition.py:706` at C\* is `dir=tempfile.gettempdir()`; the root follows
TMPDIR, not `/tmp`.

**F6** — `### Round-26 gate/probe registry — report interop`, C\* L2163 (row
`tools/repeat-control.py`):

> `selftest scratch under /tmp/tameshi-r12-repeat-control-selftest.* (removed on pass)`

Fails: `tools/repeat-control.py:597` at C\* is `dir=tempfile.gettempdir()`; the root follows
TMPDIR, not `/tmp`.

**F7** — `### Gate/probe registry`, C\* L1510 (row `repeated pristine controls`):

> `isolated \`/tmp/tameshi-r12-*\` selftest`

Fails: same tool as F6 — `tools/repeat-control.py:597` at C\* honours TMPDIR, so the
selftest scratch is not confined to `/tmp`.

**F8** — `### Gate/probe registry`, C\* L1511 (row `bash declared-witness study`):

> `isolated \`/tmp/bash-witness-selftest-private.*\` (selftest only)`

Fails: same tool as F2 — `tools/bash-witness-study.py:1241` at C\* honours TMPDIR.

Two further stale-tool claims sit **outside** the 30 frozen headings and are therefore not
scored as QUALITY-104 findings, but are the same defect and are listed for the L1:
`tools/pin-disposition.py` docstring `:36` (`pin-disposition.py --selftest  isolated /tmp git
fixtures`) and `:705` (`Hermetic fixtures under /tmp: …`),
`tools/evidence-disposition.py` `:181`/`:2350` (`Isolated /tmp fixtures`),
`tools/repeat-control.py` `:67` (``/tmp/tameshi-r12-repeat-control-selftest.*``) and
`tools/registry-check.py` `:767` (comment `an unusable /tmp is could-not-evaluate`).

### 4.3 The 21 non-finding `/tmp` mentions — why each holds

* **ER-4 quote** (C\* L1169) — the expected one:
  `ER-4's record of this tick names \`/tmp/w9-tameshi-t91/\` — fleet-kill-rate-ledger.md:320`,
  a dated quotation of the round-9 tick's own scratch path. HOLD.
* **Scratch-directive mentions** — C\* L25 (`/tmp` is for files under 50 MB only — the
  host scratch directive), L939 and L1327 (``${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX``,
  the runner's own default, which honours TMPDIR since r51), L2156 (twice,
  `auto mktemp under ${TMPDIR:-/tmp}`), and L1391 (the map row's ``mktemp -d /tmp/…`` note,
  which explicitly dates itself `[round 52]` and says the runner governs). Verified against
  C\* bytes: `tools/mutate-and-run.sh:149-150` reads
  `# "${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX" by default (r51 honours` /
  `# TMPDIR); removed on PASS unless --keep,` and
  `corpus/knowledge/operator-runbook.md:350` reads
  ``mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`` — the SKILL.md map row's anchors are
  accurate. HOLD.
* **Dated historical receipts** — L988 (round-7 negative run, self-annotated
  `[round 52: that volatile path is gone; the mechanism is corroborated at …]`), L1042 and
  L1068 (round-8 tick read), L1111 ×2 (round-8 six-case), L1169 (round-9 tick scratch),
  L1193 (round-9 falsifier), L1217/L1218/L1224 (round-9 regression logs,
  `REGRESSION_DATE 2026-10-14T19:58:59Z`), L1341 (round-10 workdir). Dated historical
  milestones → HOLD.
* **L1499** — `## Repeated controls and gate registry — round 12`:
  `run \`python3 tools/repeat-control.py --runs 3 --out /tmp/tameshi-r12-controls-UNIQUE -- COMMAND ARG...\`;`
  — a round-12-dated recipe (the section states `Registry scope is these round-12
  instruments`), path round-12-tagged. Treated as a dated historical hold, with the note
  that a reader copying it today writes into `/tmp` under the new scratch regime.
* **L2167 / L2168** — truthful rows for tools the round did **not** patch:
  `/tmp/tally-audit-work` and `/tmp/tameshi-r4-2-regression.XXXXXX` match the literal
  strings still present in `tools/tally-audit-v2.py:265` and `tools/tally-audit-v3.py:422`
  at C\*, so the SKILL.md text is accurate as written. HOLD. (Adjacent observation for the
  L1: those two tools still create directories under `/tmp` by literal path — outside C2's
  declared `dir="/tmp"` surface and outside the QUALITY-104 scope, but not covered by the
  C2 grep either.)

---

## 5. Holds carried by this receipt (pointers verified against C\* bytes)

* The 30 frozen headings resolve uniquely and the frozen `sectionize()` split is reproduced
  for all 30 (§1.1, 30/30 sha256 self-checks).
* The `### The map` row's anchors are accurate at C\*: `corpus/knowledge/operator-runbook.md`
  still reads ``mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`` at L350 (cited as
  `:349-351`), and `tools/mutate-and-run.sh:149-150` reads the `${TMPDIR:-/tmp}` default.
* The rewritten P2 pointer `tools/mutate-and-run.sh:88-97` is the ten-leg registry at C\*;
  the base pointer `:92-93` was the same list two lines earlier.
* `tools/registry.json` at C\* carries 56 rows and **none** contains `/tmp`, so no registry
  row JSON-side contradicts the SKILL.md prose.
* The round-53 fix pass is a single commit (`218bc6b5`) for both `SKILL.md` and the 7
  `tools/` files; the 12 changed section bodies and the 8 stale rows are all attributable
  to it.

---

## 6. Adjacent operability blockers found while executing the scan (outside QUALITY-104)

These are **not** QUALITY-104 findings (different subject), but they are decisive-run
blockers, are reproducible, and the L1 needs them before the deciding run. Each is
evidence-backed; all commands are read-only against git objects.

### A1 — The C2 counter is RED at C\*: `C2_R53_PASS=false`, exit 1

```
$ python3 .ufo/evidence/round-53/c2/measure.py --lane …/tameshi-shokunin \
      --rev a41195dfc13a73958e4c5228ec196b28d03ded03 --work <scratch> --explain
C2_R53: rev=a41195dfc13a tmp_hits=0 registry_selftest=[rc=0 SELFTEST: PASS (51 cases)]
        envdiff_selftest=[rc=0 ENVDIFF_SELFTEST: 9/9 pass] cr47=rc=0 docs=ok total=2
        C2_R53_PASS=false
PROBLEM cr47-zero-exit
PROBLEM cr47-no-scratch-message
EXIT=1
```

Root cause, isolated: the CR47 arm runs `registry-check.py --selftest` with
`TMPDIR=<work>/missing-dir` (absent) and requires a non-zero exit naming scratch creation.
But the fix pass changed `dir="/tmp"` → `dir=tempfile.gettempdir()`, and Python's
`tempfile.gettempdir()` **silently falls back to `/tmp`** when `TMPDIR` names a missing
directory — it does not raise. Measured directly:

```
$ TMPDIR=/nonexistent-xyz python3 -c "import tempfile;print(tempfile.gettempdir())"
/tmp
```

so the selftest succeeds (rc 0, `SELFTEST: PASS (51 cases)`) and never names scratch
creation. The base has the same two CR47 problems (base counter: `cr47=rc=0`,
`PROBLEM cr47-zero-exit`, `PROBLEM cr47-no-scratch-message`), so the CR47 arm is not
reachable by either revision's `registry-check.py`.

A remedy that satisfies the frozen CR47 arm exists (probed in scratch, not applied): resolve
`TMPDIR` explicitly and fail closed, e.g. `dir=os.environ.get("TMPDIR", "/tmp")` wrapped in
`except OSError` raising `RuntimeError("cannot create clone scratch under the scratch root: …")`.
Probe result — exit 1, `cannot create clone scratch` present twice on stderr, **0**
`REGISTRY_CHECK` lines on stdout, and the same file still passes `SELFTEST: PASS (51 cases)`
under a valid `TMPDIR`. `registry-check.py:768` already carries that message shape.

### A2 — The frozen `no-harm.sh` has a bash syntax error and dies before its 12th monitor

```
$ bash -n .ufo/evidence/round-53/no-harm.sh
…/no-harm.sh: line 40: unexpected EOF while looking for matching `''
EXIT=2
```

Line 40 is

> `Q=$(git grep -c -E 'dir\s*=\s*["\']/tmp' "$REV" -- tools/ 2>/dev/null | awk -F: '{s+=$NF} END {print s+0}')`

The `\'` inside a single-quoted string does not escape the quote, so the pattern's quoting
terminates early and the rest of the file is unparsable. Consequences: the script exits 2
after printing only **11** of the 12 `NOHARM` lines, so the `r53-scratch-hygiene` monitor
(the C2-surface monitor) **never runs**, and the deciding run's
`[ "$(grep -c '^NOHARM .* ok$'" …)" = 12 ]` check can never be satisfied. The error is
present in the round-53 freeze commit `cf87276` and is byte-identical at the amendment-5
freeze `e62d997` and at C\* (sha256 `e4e6b7ad803f5f591ceb5f83b3540bc46b0be0de958d17dc74064485ea1e9e6b`);
round 52's `no-harm.sh` parses cleanly (`bash -n` exit 0), so the defect is new in round 53.
A scratch copy with the quoting repaired parses and runs all 12 monitors.

### A3 — `NOHARM tools-scope` is RED at C\*: the fix pass edited 7 tools, the frozen allow-list permits 2

```
NOHARM tools-scope [M:tools/bash-witness-study.py M:tools/context-capture.py
  M:tools/env-diff.py M:tools/evidence-disposition.py M:tools/pin-disposition.py
  M:tools/registry-check.py M:tools/registry.json M:tools/repeat-control.py
  M:tools/round21-measure.py ] RED
```

`no-harm.sh` compares **floor `ef19d8e1`** → REV and allows only
`M:tools/registry.json|M:tools/round21-measure.py|M:tools/registry-check.py|M:tools/env-diff.py`
(anything else RED); its own header says the round-53 C2 allowance is
`M:tools/registry-check.py + M:tools/env-diff.py`. The fix pass patched **seven** tools
(adding `bash-witness-study.py`, `context-capture.py`, `evidence-disposition.py`,
`pin-disposition.py`, `repeat-control.py`), so five files fall outside the allow-list and the
monitor prints RED. Since `no-harm.sh` is in the deciding run's `FROZEN` file list, the
round must either amend/re-freeze the monitor to declare the actual C2 tool set, or narrow
the patch set. (At floor→base the tools diff was only `registry.json` +
`round21-measure.py`, i.e. green; the RED is created by this round's patch set.)

### A4 — informational: `NOHARM coldread-floor` is RED at C\*

`NOHARM coldread-floor score=6 credited=34 RED` — the C1 re-key and the committed
round-53 reader JSONs are not in C\* yet. Expected at this stage (wave-1 readers are still
being written), not a defect; recorded so the L1 is not surprised by it in the deciding run.

---

## 7. What the L1 is asked to do

1. **C5 / F1–F8 (the only QUALITY-104 un-fixed hits):** update the eight registry-row
   scratch descriptions to match the patched tools (e.g. `selftest scratch under $TMPDIR
   (tameshi-r12-repeat-control-selftest.*)`, `… via mkdtemp under $TMPDIR …`), or restore
   the tools' behaviour if the `/tmp` prose is to be kept. Note the two env-diff rows were
   already rewritten in the same fix pass, so the table is currently self-inconsistent.
   If the counter's docs arm is meant to police this class, its four patterns must be
   widened — as written they cannot see any of the eight rows.
2. **A1:** decide how the frozen CR47 arm is to be satisfied — `tempfile.gettempdir()`
   cannot produce the required non-zero exit for a missing `TMPDIR`; an explicit
   `os.environ.get("TMPDIR", "/tmp")` plus a fail-closed `except OSError` does (probed).
3. **A2:** repair the `no-harm.sh` line-40 quoting (or re-freeze the monitor) — as committed
   it cannot run its 12th monitor and cannot reach 12/12 ok.
4. **A3:** reconcile the frozen `tools-scope` allow-list with the seven-tool C2 patch set.
5. **Wave-2 falsifier recipe:** for P1, grep `since round 51) (ten since round 51)` or
   strip markup — the plain literal reads 0 at base (§3.2).

## 8. Provenance and hygiene

* Reads: `git show` of git objects in `/home/vgpnk/Projects/shokunin/tameshi-shokunin` only.
* Scratch: `/fast/scratch/hyaku/tameshi-r53/w1/T53W1LabLint/` (created with `mkdir -p`,
  removed on exit; no inherited `TMPDIR` relied upon, all probes bound `TMPDIR` explicitly).
* No git/jj mutating command was run anywhere; no commit, push, fetch or prune; no file
  under `SKILL.md`, `tools/`, `corpus/`, `MANIFEST.json` or `.ufo/evidence/` was touched.
* The only file this seat wrote is this report.
* Tooling: no package was installed or upgraded (Python 3.14 + `git` already present; no
  pacman transaction).
