# T53W2ExecDupLint — duplicate-phrase lint over SKILL.md at C\*\*

**Seat:** T53W2ExecDupLint (wave-2 executor, axis `operability`)
**Lane:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
**Measured revision (cand):** `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e` (= C\*\*)
**Comparators:** `a41195dfc13a73958e4c5228ec196b28d03ded03` (C\*), `6db1d220b337c35ff1e25bf9cfd74abc9db1498d` (base)
**SKILL.md sha256 at C\*\*:** `4b4a05251208beb61b0ad70ff8f26fef42dd9d3187317c4286b06c42b06b3d6d` (2189 lines, 197 139 B)
**Sections split (frozen monitor rule):** 64 sections
**Verdict: PASS — zero un-fixed duplicate-phrase hits, and zero un-fixed `/tmp/` claims presented as current in the 21 re-fixed sections.**

Every command in this report is reproducible from the lane root; the lint script and its raw output are listed under *Deliverables*.

---

## 1. Method

The lint reads SKILL.md **only** from git objects (`git -C <lane> show <rev>:SKILL.md`) — never the working tree — so the measured bytes are the commit bytes.

Section splitting mirrors the frozen monitor exactly
(`.ufo/evidence/round-18/coldread/assemble.py:159` `sectionize()`, `HEADING_RE = ^#{1,3}(?:\s|$)`,
`FENCE_RE = ^(`{3,}|~{3,})`): split into lines, a heading is a `#{1,3}` line **outside** ``` fences,
a section runs from its heading line through the line before the next heading, trailing
whitespace-only lines stripped, joined with `\n`, sha256 over the UTF-8 bytes.

### Axes

| axis | what it detects | why it is a defect class |
|---|---|---|
| **K1** | the two known fixed patterns named by the seat item | the item's named targets |
| **D1** | doubled word in prose (`the the`) | classic copy-paste typo |
| **D6** | the **same qualifier twice on one item** — two equivalent parentheticals attached to a single phrase, separated only by whitespace/punctuation | the exact shape of known fixed pattern 1 |
| **D2** | two identical parentheticals on one line | duplicate qualifier |
| **D3** | duplicate parenthetical, same line, non-adjacent | duplicate qualifier |
| **D4** | duplicate parenthetical across two lines of one section | weaker — usually a shared attribute of two list items |
| **D5** | repeated ≥6-word n-gram across two lines of one section, fenced blocks excluded | weakest — table headers and deliberate mutant-pair tables repeat |
| **T1** | every `/tmp/` occurrence inside the 21 re-fixed sections, with history markers detected | the item's second half |

### Exclusions applied to D1 (each is a false positive, not a defect)

1. **CLI metavariable pairs** — `--rev REV`, `--tag TAG`, `--sha SHA`, `--map MAP`, `--bundle BUNDLE`, `--expected EXPECTED`, `--repo REPO`, `--pristine PRISTINE`, `--mutant MUTANT`, `--case CASE`, `--out OUT`, `--staged STAGED`, `--config CONFIG`, `--spec SPEC`, `--receipt RECEIPT`, `--file FILE`. The second token is the placeholder the flag names.
2. **Code-table column boundaries** — `pin==live live==HEADblob` (SKILL.md:1179) is two *columns* of a fixed-width table inside a ``` fence, glued by `=`. Not a repeated word.

Both exclusions are documented in the script and each is exercised by a self-test case (T6).

### Negative control (the lint is proven live)

The lint must **fire** on a defect and **stay silent** on clean bytes. `selftest_duplint.py` — 7/7 pass:

```
[PASS] T1 known-fixed pattern 1: findings=[('K1', '(**ten** since round 51) (ten since round 51)'), ('D6', '**ten** since round 51')]
[PASS] T2 known-fixed pattern 2: findings=[('K1', 'still not embedded at this boundary (both are legs 5-6 since round 10-2'), ('K1', ...)]
[PASS] T3 doubled word: findings=[('D1', 'The the')]
[PASS] T4 adjacent duplicate parenthetical: findings=[('K1', ...), ('D2', 'ten since round 51'), ('D6', 'ten since round 51')]
[PASS] T4b duplicate qualifier on one item (emphasis variant): findings=[('K1', ...), ('D6', '**ten** since round 51')]
[PASS] T5 clean text: findings=[]
[PASS] T6 CLI metavariable pair is not a doubled word: findings=[]
selftest: 7/7 pass
```

The strongest end-to-end control: run the **same** lint against the base revision, where both known patterns were present. It fires twice there and zero times at C\*\*:

```
=== K1 (the two known fixed patterns) ===
  base 6db1d220: line 1305 '(**ten** since round 51) (ten since round 51)'
  base 6db1d220: line 1227 'still not embedded at this boundary (both are legs 5-6 since round 10-2'
=== D6 (duplicate qualifier on one item) ===
  base 6db1d220: line 1305 col 83 '(**ten** since round 51) (ten since round 51)' gap=' '
```

---

## 2. Checks run — the named fixes FIRST

### 2.1 Known fixed pattern 1 — `(ten since round 51) (ten since round 51)` — **FIXED, holds**

Base (`6db1d220`) SKILL.md:1305 read:

> uncommitted worktree file at this write), `--regression` replays **six** in r10-2 (**ten** since round 51) (ten since round 51)

C\*\* SKILL.md:1320 reads:

> uncommitted worktree file at this write), `--regression` replays **six** in r10-2 (**ten** since round 51)

The duplicate qualifier is gone; the sentence keeps one qualifier. **Verified by the K1 and D6 axes at base (fire) and at C\*\* (silent).**

### 2.2 Known fixed pattern 2 — `still not embedded at this boundary (both are legs 5-6 since round 10-2` — **FIXED, holds**

Base (`6db1d220`) SKILL.md:1227 read:

> read `stale`. Cases 5–6 were still not embedded at this boundary (both are legs 5–6 since round 10-2 — `tools/mutate-and-run.sh:92-93`): their rows carry no `REGRESSION`

C\*\* SKILL.md:1234 reads:

> read `stale`. Cases 5–6 were not yet embedded at this boundary (they became legs 5–6 at r10-2; the current tool carries them at `tools/mutate-and-run.sh:88-97`): their rows carried no `REGRESSION`

The phrase `still not embedded at this boundary` is absent at C\*\*; the replacement carries an explicit date qualifier and a pointer to the current tool's leg list. **Verified: the replacement's anchor resolves** — `tools/mutate-and-run.sh:88-97` at C\*\* lists exactly 10 leg lines (`grep -c '^#'` = 10), matching the anchor's claim. The K1 axis fires at base and is silent at C\*\*.

### 2.3 Known fixed pattern 1 was already fixed at C\* (wave-1 scribe M1a agrees)

Wave-1's scribe recorded the same conclusion (`T53W1ScribeLesson.md:84`, "VERIFIED (as base-state)"): base `6db1d220:SKILL.md:1305` reads exactly the doubled form; at `218bc6b5` and C\* it reads "… (**ten** since round 51)" — single. This seat's independent measurement reproduces it byte-for-byte; the two seats agree.

### 2.4 The fix pass introduced **no** new duplicate

Diffing the lint's finding sets C\* → C\*\*:

```
=== NEW at C** (introduced by fix pass 2) ===
(none)
=== GONE at C** (removed by fix pass 2) ===
   D5 cross-line-duplicate-ngram '### Reading a receipt — the discipline' lines 1005 and 1006 | pass VERDICT PASS rc 0 at
        (this D5 quote is a normalized n-gram — the lint tokenizes and joins with spaces;
         the verbatim C* bytes it came from are:
            --selftest` → `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0 at tool
            sha256 `cf41efaa…` (a content sha, not a git revision) (round 52: the same command prints …)
```

One duplicate was **removed** (the `--selftest` receipt line was reworded at C\*\*:1006 to "at the pinned r7-1 tool printed … the tally is the pinned tool's, not the current command's"). None was added. Axis census:

| revision | findings | by axis |
|---|---|---|
| base `6db1d220` | 89 | K1:2 · D6:1 · D2:1 · D3:1 · D4:24 · D5:60 |
| C\* `a41195df` | 73 | D2:1 · D3:1 · D4:24 · D5:47 |
| **C\*\* `5b703c6f`** | **72** | D2:1 · D3:1 · D4:24 · D5:46 |

**K1 = 0 and D6 = 0 at C\*\*.**

---

## 3. Holds (not findings)

Every remaining hit was adjudicated against the finding discipline ("a finding is a statement that does **not** hold at C\*\*"). All 72 are **holds**.

### 3.1 D1 doubled words — **0 real hits at C\*\***

A raw, unfiltered regex sweep (`\b([A-Za-z][A-Za-z'-]*)\s+\1\b`, IGNORECASE, no exclusions) over all 2189 lines yields **32** matches at C\*\*. Every one is either a CLI metavariable pair (30 of them, listed in §1) or the `pin==live live==HEADblob` code-table column boundary at SKILL.md:1179 (inside a ``` fence). **Zero prose doubled words** — no `the the`, no `of of`, no `and and`.

C\* has the identical 32; the fix pass neither added nor removed one.

### 3.2 D6 duplicate qualifier on one item — **0 at C\*\***

The precise discriminator (two *equivalent* parentheticals — compared after stripping markdown emphasis, so `(**ten** since round 51)` ≡ `(ten since round 51)` — attached to **one** item with only whitespace/punctuation between):

```
=== base: equivalent qualifier repeated on ONE item ===
  L1305 gap=' ' -> (**ten** since round 51) / (ten since round 51)
  total: 1
=== C*: ===
  total: 0
=== C**: ===
  total: 0
```

This is the axis that isolates the real defect from its harmless neighbours.

### 3.3 D2/D3 — one hit, at SKILL.md:769 — HOLD

> asserted-stem-vs-remainder (3 gates); asserted counts and floors (3 gates);

Two **different** list items each carrying the qualifier `(3 gates)`. The gap is a substantive clause (`; asserted counts and floors `), so this is a shared attribute of two items, not a duplicated qualifier on one item. Contrast the base defect, where the gap was a single space. **HOLD.**

### 3.4 D4/D5 — 70 hits, all holds

Adjudicated by category:

- **Registry table headers** (`| Name | Kind | Entry | Verdict map | Self-invocation | Persisted values | Write scope | Owner |`, 18 hits at SKILL.md:1991/2013/2035/2068): four *separate* registry tables in one section each open with the same column header. Structural, not duplication.
- **Verdict-map boilerplate** (`0 clean; 1 failed; 2 could-not-evaluate`, 9 hits): the shared verdict-map shape every registry row states.
- **`(usage)`** (11 hits at SKILL.md:2160-2187): the `64 usage` exit class repeated in each row's verdict map.
- **`(80 %)`** (SKILL.md:47/50, 321/325): the same kill-rate band stated in two different bands' rows.
- **`(16 cases)`** (SKILL.md:600/618/655/658/662): the suite size restated at each step of the Appendix B recipe.
- **`(round 18)`** (SKILL.md:1948/1949/1950): three different tools, each row labelled with its own round.
- **`(exit 1)`** (SKILL.md:1806/1814): two different tools' exit codes.
- **`(same registry section; same-ground calibration)`** (SKILL.md:2028/2061): the same qualifier opening each round's addition paragraph.
- **`(mutation-case-kagi-census.md:50-53)`** (SKILL.md:216/246): the same citation used for two different facts (kill rate, then runtime). Anchor checked — `corpus/knowledge/mutation-case-kagi-census.md:50-53` at C\*\* does carry both the `8/10 (80 %)` kill rate and the `11.0 s` runtime. **Anchor resolves; HOLD.**
- **Deliberate mutant-pair tables** (SKILL.md:584, 643-649, 780-816 region): the Appendix A/B worked examples show pristine and mutant code side by side. The n-gram repeats *because* the mutant is a one-token edit of the pristine. Fenced blocks are excluded from D5, but these two are outside the fences. **Structural; HOLD.**
- **`second raw pass 20:00:29Z`** (SKILL.md:1206): the phrase appears twice in one sentence — once as prose, once inside the ER-4 quotation it cites. Verbatim: `reproduced in its second raw pass 20:00:29Z (ER-4: "second raw pass 20:00:29Z, same readings")`. **HOLD.**
- **`nine cases since round 26, ten since round 51`** (SKILL.md:1400) and **`nine since round 26, ten since round 51`** (SKILL.md:1407): the map table's two rows (the runbook row and the `tools/mutate-and-run.sh` row) each state the case-count history in their own cell. **HOLD.**

---

## 4. `/tmp/` claims in the 21 re-fixed sections

The 21 headings wave-1 found dirty were derived from the wave-1 reader JSONs (each JSON with a non-empty `findings` array):

```
## Effective expectation reconciliation — round 14
## Mutation-sweep recipe — numbered steps; bounded cold-read evidence
## Repeated controls and gate registry — round 12
## Standing rules
## The leg ledger — replay, receipt, and how it is read (round 7, measured)
## The operator's runbook and the six-leg regression (round 10, measured)
## The re-sweep cadence and the six-case confidence statement (round 8, measured)
### Gate/probe registry
### Reading a receipt — the discipline
### Round-13 gate/probe registry
### Round-14 historical registry — superseded by round 15
### Round-15 gate/probe registry
### Round-17 gate/probe registry — re-pin and monitor
### Round-26 gate/probe registry — report interop
### Six-case confidence statement (round 8, measured)
### The map — where a reader enters, artifact by artifact
### The re-pin semantics, as executed
### The six-leg regression — usage and this round's receipt
### The tick and the pin read
### Using the ledger
### What stays open — named, never closed by prose
```

**Eight `/tmp/` lines fall inside those 21 sections at C\*\*. Every one is either explicitly marked as history/reaped, or is a dated historical milestone. Zero are presented as a current scratch location.**

| line | section | quote (verbatim) | adjudication |
|---|---|---|---|
| 991 | `### Reading a receipt — the discipline` | `flips=1)` (negative run, `/tmp/w7-tameshi-1/flip-run.out` — [round 52: that volatile path is gone; the mechanism is corroborated at `reports/r7-aud-t7.md` §3 F4 and `tools/mutate-and-run.sh:2010`]). Quote the rows,` | **HOLD** — explicitly marked gone (round 52), with the corroborating receipt named (`reports/r7-aud-t7.md` §3 F4, `tools/mutate-and-run.sh:2010`) |
| 1045 | `### The tick and the pin read` | ``/tmp/w8-tameshi-t84/pin-read.txt`:` | **HOLD** — dated historical milestone: the sentence is "Executed instance — this lane, tick 2026-10-14T19:15:14Z, host `plazir27`, tool `cf41efaa…`" |
| 1072 | `### The tick and the pin read` | `appended reads `drift` (`/tmp/w8-tameshi-t84/drift-demo.txt`; substrate 0` | **HOLD** — same dated round-8 tick instance as the line above |
| 1115 | `### Six-case confidence statement (round 8, measured)` | ``/tmp/w8-tameshi-t81/sweep/` and `/tmp/w8-t8-2-claims/work/` — scratch paths long since reaped under the host scratch rule, named here as history only; the evidence of record is the case notes `corpus/knowledge/mutation-case-kagi-checklist.md` and` | **HOLD** — this is wave-1 finding Read20, and C\*\* is the **fix**: the paths are now explicitly marked "long since reaped … named here as history only" and the evidence of record is redirected to the case notes. Both case-note blobs exist at C\*\* (`git ls-tree` → `mutation-case-kagi-checklist.md` = `a267cbe0…`, `mutation-case-kumitate-claims.md` = `3b5c3109…`) |
| 1350 | `### The six-leg regression — usage and this round's receipt` | ``/tmp/w10-t10-4-ev/` (regression workdir kept):` | **HOLD** — dated historical milestone: "Receipt, executed by this lane … 2026-10-14T21:02:39Z, tool `75ed934d…` before and after" |
| 1400 | `### The map — where a reader enters, artifact by artifact` | `§7's default scratch still reads `mktemp -d /tmp/…` (`corpus/knowledge/operator-runbook.md:349-351`) while the runner honours `TMPDIR` (`tools/mutate-and-run.sh:149-150`) — by that rule the runner governs [round 52] \|` | **HOLD** — a cross-document *description* of the runbook's own text, dated `[round 52]`, and it names the governing rule (the runner's `TMPDIR` wins). **Both anchors verified at C\*\***: `corpus/knowledge/operator-runbook.md:349-351` does read `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`, and `tools/mutate-and-run.sh:149-150` does read `"${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX" by default (r51 honours` / `# TMPDIR)` |
| 2178 | `### Round-26 gate/probe registry — report interop` | `the runtime sweep additionally removes the fixed literal /tmp/tally-audit-work whenever a PASS vector fires` | **HOLD** — a factual description of a *test fixture* the tool simulates and removes, verified by execution (see below) |
| 2179 | `### Round-26 gate/probe registry — report interop` | `plus one auto-root dir /tmp/tameshi-r4-2-regression.XXXXXX allocated to witness the runner shape and removed at exit` | **HOLD** — same shape; verified by execution (see below) |

### 4.1 The two registry-row `/tmp/` claims were verified by **execution**, not by reading

The rows claim specific runtime behaviour. Both were measured against the C\*\* tool bytes.

**SKILL.md:2178 — "removes the fixed literal /tmp/tally-audit-work whenever a PASS vector fires".** A sentinel directory was planted at `/tmp/tally-audit-work`, then the C\*\* `tally-audit-v2.py` `check_runtime()` was run:

```
before: sentinel exists = True
check_runtime -> (True, 'vectors=18288 mismatched=0')
after: sentinel exists = False
```

The claim holds: the literal is removed on a PASS vector. (`tools/tally-audit-v2.py:265` `CONFIGS = (('tally-audit', '0', '1'), ('/tmp/tally-audit-work', '1', '0'))` — it is a simulated config value the audit drives, not a live scratch location the lane writes into.)

**SKILL.md:2179 — "one auto-root dir /tmp/tameshi-r4-2-regression.XXXXXX … removed at exit".** The C\*\* `tally-audit-v3.py` `auto_root()` was invoked with and without a `TMPDIR`:

```
auto_root() -> /tmp/tameshi-r4-2-regression.wU7Dhj
under TMPDIR? /fast/scratch/.../tmp
--- with TMPDIR set ---
auto_root() -> /tmp/tameshi-r4-2-regression.kF2ecV
under TMPDIR? /fast/scratch/.../mytmp
IS UNDER TMPDIR? False
```

The tool's `auto_root()` deliberately allocates a `/tmp/…` directory (`tools/tally-audit-v3.py:422`, `os.makedirs(cand)`) and removes it at exit via `atexit.register(lambda: shutil.rmtree(cand, …))` — `tools/tally-audit-v3.py:428`. The row describes that faithfully. **This directory is the audit tool's own witness of the runner's shape, not a lane scratch path**, and the row is a write-scope description of the tool, not a directive to a seat. **HOLD.**

### 4.2 The round's own C2 counter agrees, and its docs arm is green

The frozen C2 counter, run against C\*\* with an absolute `--work` (a *relative* `--work` makes `TMPDIR` relative and the registry-check selftest's git-clone cases fail — an artifact of the counter's `work / 'tmp'` path handling, not of the lane):

```
C2_R53: rev=5b703c6ff tmp_hits=0 registry_selftest=[rc=0 SELFTEST: PASS (51 cases)] envdiff_selftest=[rc=0 ENVDIFF_SELFTEST: 9/9 pass] cr47=rc=1 docs=ok total=0 C2_R53_PASS=true
```

`tmp_hits=0` (no `dir = "/tmp"` under `tools/` at C\*\*), `docs=ok` (SKILL.md names no stale `/tmp` scratch path for either tool), `cr47=rc=1` (a set-but-unusable `TMPDIR` is refused, not silently fallen back).

Independently, the C\*\* `registry-check.py --selftest` was reproduced from a `git clone --shared` fixture with `TMPDIR` bound inside it:

```
SELFTEST: PASS (51 cases)
SELFTEST_EXIT=0
```

### 4.3 The 7 wave-1 findings in the Round-26 registry section are all fixed at C\*\*

Read19's 7 findings, each re-checked byte-exactly against the C\*\* blob:

```
  PRESENT@C*   FIXED@C**  | 'selftest writes a private fixture tree under a hardcoded /tmp (TMPDIR ignored)'
  PRESENT@C*   FIXED@C**  | 'selftest fixtures under /tmp/context-capture-selftest-*, removed in finally'
  PRESENT@C*   FIXED@C**  | 'SELFTEST: PASS (49/49 cases)'
  PRESENT@C*   FIXED@C**  | 'selftest fixtures under /tmp/tameshi-r14-evidence-disposition-selftest.* removed on pass, kept on failure'
  PRESENT@C*   FIXED@C**  | 'selftest writes isolated /tmp/tameshi-r13-pin-disposition-selftest.* fixtures'
  PRESENT@C*   FIXED@C**  | 'selftest and --rev fixture trees via mkdtemp under /tmp (hardcoded, TMPDIR ignored)'
  PRESENT@C*   FIXED@C**  | 'selftest scratch under /tmp/tameshi-r12-repeat-control-selftest.* (removed on pass)'
```

Every one of the 7 stale `/tmp` scratch pointers in that section is gone at C\*\*. The two surviving `/tmp` mentions (2178, 2179) are the *test-fixture* and *witness* literals described above — different strings, not among Read19's findings, and both verified accurate by execution.

---

## 5. Files changed

**None in the lane.** This seat is read-and-report; it made no edit to SKILL.md, `corpus/`, `tools/`, `.ufo/evidence/`, `MANIFEST.json`, or any tracked file. The only lane write is this report and its machine-readable companion.

Written under the seat's declared write scope:

| path | what |
|---|---|
| `.ufo/waves/round-53/w2/T53W2ExecDupLint.md` | this report |
| `.ufo/waves/round-53/w2/T53W2ExecDupLint.json` | machine-readable result (axes, hits, holds, `/tmp/` adjudication) |
| `.ufo/waves/round-53/w2/T53W2ExecDupLint.duplint.py` | **the lint script** (deliverable) |
| `.ufo/waves/round-53/w2/T53W2ExecDupLint.selftest.py` | **the 7-case self-test** (deliverable) |
| `.ufo/waves/round-53/w2/T53W2ExecDupLint.refixed_sections.json` | the 21 headings derived from the wave-1 reader JSONs |
| `.ufo/waves/round-53/w2/T53W2ExecDupLint.output-Cdbl.txt` | lint output at C\*\* (authoritative) |
| `.ufo/waves/round-53/w2/T53W2ExecDupLint.output-Cstar.txt` | lint output at C\* |
| `.ufo/waves/round-53/w2/T53W2ExecDupLint.output-base.txt` | lint output at base (the negative control: K1 fires twice) |

Scratch (deleted before yield — see *Scratch hygiene* below):

The deliverable scripts and outputs are also copied into the lane under this seat's own
`.ufo/waves/round-53/w2/` prefix (see *Files changed*), so the L1 can re-run the lint from the lane
without the scratch tree:

```
python3 .ufo/waves/round-53/w2/T53W2ExecDupLint.selftest.py                    # 7/7 pass
python3 .ufo/waves/round-53/w2/T53W2ExecDupLint.duplint.py \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e \
    --sections .ufo/waves/round-53/w2/T53W2ExecDupLint.refixed_sections.json
```

The scratch tree also held the three raw JSON lint runs (`run_*.json`) used for the axis census in §2.4.

---

## 6. Deliverables — the lint script + its output

**Script:** `duplint2.py` (self-contained, stdlib only, reads via `git show`, never the working tree).

```
python3 duplint2.py --lane <LANE> --rev <REV> --sections refixed_sections.json \
                    --json-out OUT.json --text-out OUT.txt
```

Output at C\*\* (head):

```
DUPLINT rev=5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e path=SKILL.md
skill_sha256=4b4a05251208beb61b0ad70ff8f26fef42dd9d3187317c4286b06c42b06b3d6d
sections_total=64
findings=72
```

Findings by axis at C\*\*: `D2:1 · D3:1 · D4:24 · D5:46` — **K1: 0, D1: 0, D6: 0** (the defect axes). The 72 are the shared-attribute / structural-repeat holds adjudicated in §3.

`run_5b703c6.txt` carries the full per-hit dump; `run_6db1d22.txt` and `run_a41195d.txt` carry the base and C\* dumps for comparison.

---

## 7. Risks and blockers

**Risks**

1. **The lint's weakest axis is D5.** It deliberately flags repeated ≥6-word n-grams across a section, which in a registry-table-heavy document yields many structural repeats (table headers, verdict maps). 46 of the 72 C\*\* hits are D5. D5 is *reported* but must be adjudicated by hand; it is not a defect signal on its own. The defect-bearing axes (K1, D1, D6) are narrow and unambiguous.
2. **The D6 discriminator relies on a heuristic** — that two parentheticals separated only by whitespace/punctuation belong to one item. A duplicated qualifier split across a line break would escape it. I checked for that shape explicitly (adjacent-line duplicate parentheticals within one section): the only hits are `(3 gates)` at SKILL.md:769 and `(round 18)` at SKILL.md:1948-1950, both shared attributes of *different* items (verified by reading each).
3. **Two `/tmp/` literals in the Round-26 registry rows describe tool behaviour that ignores `TMPDIR`** (`tools/tally-audit-v3.py:422` allocates under `/tmp` even with `TMPDIR` set — measured). The SKILL.md rows describe this accurately, so they are not findings. But if the L1 intends the C2 scratch-hygiene axis to extend to *every* tool (not just `registry-check.py` and `env-diff.py`), those two tools would be in scope and their rows would need rewording. That is a scope decision for the L1, not a defect at C\*\*.
4. **The C2 counter is sensitive to a relative `--work`** (its `work / 'tmp'` becomes a relative `TMPDIR`, and the registry-check selftest's git-clone cases then fail: `SELFTEST: FAIL (6 of 51 cases: gitdir-scrub-rev, rev-clone-detached, …)`). With an absolute `--work` it prints `C2_R53_PASS=true`. The counter is a frozen file and must not be edited; the deciding run should pass an absolute `--work`.

**Blockers**

None. Every check ran; every command output is quoted above.

---

## 8. Scratch hygiene

Everything lived under `/fast/scratch/hyaku/tameshi-r53/w2/T53W2ExecDupLint/` (plus two `git clone --shared` fixtures and a `mktemp -d` work dir, all inside it). `pacman` was not run (host-wide pause). No tool was installed — the lint uses only the Python standard library. The scratch tree was **deleted before yield**; `ls /fast/scratch/hyaku/tameshi-r53/w2/` shows no residue from this seat.

The fixture rule was honoured: the clone was created with `git clone --shared`, and `git rev-parse --show-toplevel` was asserted to print the fixture dir before any use.

---

## 9. Summary

| item | result |
|---|---|
| known fixed pattern 1 `(ten since round 51) (ten since round 51)` | **absent at C\*\*** — present at base, fixed; K1+D6 fire at base, silent at C\*\* |
| known fixed pattern 2 `still not embedded at this boundary (both are legs 5-6 since round 10-2` | **absent at C\*\*** — present at base, fixed; replacement anchor `tools/mutate-and-run.sh:88-97` resolves (10 legs) |
| doubled words (`the the`) | **0** in prose at C\*\* (32 raw regex hits, all CLI metavariable pairs or one code-table column boundary) |
| repeated parentheticals | **0** duplicate-qualifier-on-one-item at C\*\* (D6=0). The 72 remaining hits are shared attributes of different items and structural table repeats — all holds, each adjudicated in §3 |
| `/tmp/` claims presented as current in the 21 re-fixed sections | **0** — 8 hits, all dated historical milestones or explicitly history-marked; the two registry-row claims were verified by execution |
| fix pass 2 introduced a duplicate? | **No** — 0 new findings C\* → C\*\*; 1 removed |
| **overall** | **PASS — zero un-fixed hits** |
