# QualityReview — QUALITY.md criteria 18–20 at `c699c8c`

Seat: `TameshiR16.QualityReview` (leaf, read-only; no subagents).
Lane root: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Reviewed commit:
`c699c8c36d6e4eca4b796b81a8247904aa145ec8` (HEAD, pushed).
Scratch: `/tmp/tameshi-r16w2-QualityReview-f2imNW`.
Tool installs/upgrades: **none**; no pacman transaction; no host service touched.
Read at `c699c8c` via `git show`/`git archive` per the lane contract; every lane tool was
executed from a `/tmp` copy of its committed bytes.

## Axes

- **Depth** — does each new criterion carry a falsifier that actually fires?
- **Calibration** — does the prose claim exactly what the retained evidence measures, no more?

## 0. Verdict on what I attacked

Criteria 18–20 are **partial**: each cites a real `## Mistakes` row and each named fix is
re-executable and fires as claimed (18 and 19 fully; 20's staging/install half fully), but
criterion 20's universal *“every receipt names the instrument sha it ran”* is contradicted by the
round's own `--selftest` receipt, and criterion 18's *“keeps any prior structured branch (JSON)
unchanged”* is false as a code property (true only on the retained JSON rows). No blocking gap.

## 1. Criteria 1–17 untouched

```
$ git diff --numstat e69b488 c699c8c -- corpus/QUALITY.md
21	0	corpus/QUALITY.md
```

The only hunk is `@@ -82,3 +82,24 @@` — appended after criterion 17
(`corpus/QUALITY.md:77-84`, ending `Routed defects5)`). 21 added lines, 0 removed, 0 modified.
No criterion 1–17 line changed. **Holds.**

## 2. Citation to real `## Mistakes` rows

`corpus/lessons/round-16.md` `## Mistakes` (line 49) has exactly four data rows:

| Line | Class | Criterion citing it |
|---|---|---|
| 53 | `attribution` (round-15 receipt parser) | 18 |
| 54 | `attribution` (this round's AttrFix draft rule) | 18 |
| 55 | `landing` (misroot `TameshiR15`) | 19 |
| 56 | `scope` (in-place edit of `tools/mutate-and-run.sh`) | 20 |

`grep -n '^18\.\|^19\.\|^20\.' corpus/QUALITY.md` → 88, 97, 102. Citation forms match the
house rule at `corpus/QUALITY.md:8` (“Each criterion cites the mistake it learns from”). **Holds.**

## 3. Criterion 18 — attribution (`corpus/QUALITY.md:88-96`)

### 3.1 The named falsifier fires, exactly as stated

```
$ python3 <scratch>/.ufo/evidence/round-16/attribution/reattribute.py --selftest
/tmp/.../.ufo/evidence/round-15/verification-3.json sha256=3c419055723319f50611eb7d2fa3de46e4d4c37fb405267609eee80aecc7d8ce
usage-proof-new: oracle=usage_error old='context_consistent' FAIL new='usage_error' PASS
gate-usage: oracle=usage_error old='context_consistent' FAIL new='usage_error' PASS
usage-proof-old: oracle=receipt_missing old='receipt_missing' PASS new='receipt_missing' PASS
forged-first-line: oracle=usage_error old='context_consistent' FAIL new='usage_error' PASS
SELFTEST: PASS (new rule 4/4; old rule fails 3/4; same fixtures and oracles)
rc=0
```

Matches the lesson row (`corpus/lessons/round-16.md:53`: “old rule fails 3/4 fixtures … repaired
rule passes 4/4”) and the criterion's sha prefix `3c419055…d8ce`.

Fixture provenance (`reattribute.py:256-276`): three fixtures are the retained receipt rows
(`usage-proof-new`, `gate-usage`, `usage-proof-old`); the fourth is
`usage-proof-new`'s retained stderr with `CONTEXT: OK (id=context_consistent exit=0)` prepended
(`:274`), and its oracle is `usage_error` while `observed_exit=64`. That is the exit cross-check
the criterion demands: the forged line carries `exit=0`, so the repaired rule rejects it.

### 3.2 “The faulty receipt is corrected by an appended record, never rewritten”

```
$ git log --oneline -- .ufo/evidence/round-15/verification-3.json
9f2c86f round-15: land verified context capability and calibrated evidence
$ git rev-parse e69b488:.ufo/evidence/round-15/verification-3.json   # 87987fb8…193
$ git rev-parse c699c8c:.ufo/evidence/round-15/verification-3.json   # 87987fb8…193  (same blob)
$ git show c699c8c:...verification-3.json | sha256sum                # 3c419055…d8ce
```

Same blob before and after round 16; one commit ever touched it. Correction mode re-run:

```
$ python3 reattribute.py
... sha256=3c419055…d8ce
correction.json already exists with identical bytes; left unchanged
corrections: usage-proof-new context_consistent->usage_error, gate-usage context_consistent->usage_error
old rule reproduced every recorded observed_id (14 command rows)
rc=0
```

`correction.json` names exactly the two usage rows, `coverage_changes: []`,
`old_rule_fidelity_failures: []`, `source_receipt.mutated: false`. Its sha is unchanged
(`1caf1237…cea1`). **Holds.**

### 3.3 Minor gap — “keeps any prior structured branch (JSON) unchanged”

The branch is *kept*, but its null-id fallback changed. Imported the committed module and
compared:

```
$ python3 -c "… ra.old_rule('{"id": null, "note": "id=context_consistent"}', '', True)"
  old = 'context_consistent'
$ … ra.new_rule(<same>, exit_code=64)
  new = None
```

Old rule (`reattribute.py:80-87`): dict with `id: null` → falls through to the first-`id=` token
search. New rule (`:121-127`): dict with `id: None` → falls through to the terminal-verdict scan.
Divergence demonstrated on a constructed JSON doc.

Scope of the imprecision: no selftest fixture exercises the JSON branch — all four fixtures have
`_stdout_is_result_json == False` (measured). Six retained rows *do* use the branch
(`gate-frozen-builtin`, `gate-clean`, `gate-missing-env`, `gate-tampered-snapshot`,
`mapping-oracle-old`, `mapping-oracle-new`), and all six map old→new identically (no entry in
`corrections` or `coverage_changes`). So **“unchanged on every retained JSON row” is verified;
“unchanged” as a code property is not.** Accurate wording: *“the repair keeps the JSON branch and
its ids are unchanged on every retained JSON row.”*

Secondary note: the selftest's PASS condition (`reattribute.py:288`) is
`failures == 0 and old_fails >= 1`, not `old_fails == 3`. The criterion's “must reject the old
attribution” is therefore gated at ≥1 fixture; the 3/4 figure is an observation, not a bound.

## 4. Criterion 19 — landing (`corpus/QUALITY.md:97-101`)

### 4.1 “Every per-seat prompt names the L1 as `agent://<id>`”

Measured over the committed round-16 dispatch payload, per task (not whole-file substring count):

```
$ python3 … .ufo/waves/round-16/dispatch1.json
tasks 68
per-task count of agent://TameshiR16: {1: 68}
bare occurrences of TameshiR16 not preceded by "agent://": 0
tasks with "Message only TameshiR16": 0
```

Each of the 68 tasks carries the URI exactly once, e.g. from CR01's task:
`Message agent://TameshiR16 only for blockers …`. **Holds.**

The round-15 mechanism was re-measured from its committed payload:
`dispatch1.json` → 66 tasks, `0/66` containing `agent://`, `66/66` containing
`Message only TameshiR15`; `spec1.json` context (2,503 B) *does* contain `agent://TameshiR15`.
This reproduces the lesson row's census (`corpus/lessons/round-16.md:55`). **Holds.**

### 4.2 “The round's misroot sweep … must flag the archived round-15 bytes”

Reproduced on a fresh mirror (`/tmp/…/mirror`, init + one tracked commit) carrying the real
archived bytes — `sha256 b413df98…6469`, 605 B at
`/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/TameshiR15`:

```
$ git status --porcelain
?? TameshiR15                                   # rc 0  — no pathspec, flags the artifact
$ git status --porcelain -- .ufo/
                                                # rc 0, empty — the historic miss
$ ./guard2.sh <mirror>                           # verbatim prototype from Misroot.md §4
STRAY [TameshiR15] (file, LANE-NOTE)             # rc 1
$ ./guard2.sh <mirror>  (artifact removed)
                                                # rc 0
$ grep -qiE 'shokunin|tameshi|agent://' <mirror>/TameshiR15 ; echo $?
1                                                # content-only guard is blind on the real bytes
```

All four arms match `w1/Misroot.md` §4 (arms 1, 2, 3, 5). **Holds.**

### 4.3 Minor gap — falsifier is prose-retained, not in-repo executable

```
$ git ls-tree -r --name-only c699c8c | grep -i 'misroot\|guard\|fleet-root'
.ufo/waves/round-16/w1/Misroot.md        # only hit in round 16
```

`.ufo/evidence/round-16/` contains `attribution/`, `coldread/`, `round-gate/` — no misroot
directory, no guard script, no fixtures/expected.json. The guard existed only in the seat's `/tmp`
scratch and as a code block in the report. I re-executed it from that block and it behaves as
claimed, so the claim is *reproducible*, but criterion 9's “evidence a claim rests on is copied
into the repo” is satisfied at report level only. Misroot's own R3 recommends landing
`.ufo/gates/fleet-root.py`; that is not done at this HEAD.

Precision note on the same sentence: the no-pathspec `git status` *flags by output line* and exits
**0**; the rc 1 quoted in the lesson row (`corpus/lessons/round-16.md:55`) belongs to the
root-entry guard. Reading “flag” as “nonzero exit” would make the criterion false; reading it as
“surface the artifact” makes it true.

Not re-executed (lane bounds): writing a bare-id path through the live harness to confirm “a bare
id is a file path”, because that write lands at the fleet root. Evidence used instead: the archived
605 B file and the round-15 66/66 bare-id census. [INFERENCE on the mechanism, observed on the
artifact.]

## 5. Criterion 20 — scope (`corpus/QUALITY.md:102-104`)

### 5.1 Staging path and the race it answers

- `w1/RGLeg.md:11-12` — deliverable copied to
  `.ufo/waves/round-16/w1/RGLeg.mutate-and-run.sh`, sha `f91f7fa8…4736`, 79,479 B;
  `:14` restore via `git show HEAD:tools/mutate-and-run.sh`; `:36` “L1 installs the deliverable
  after cold-reads finish.”
- `w1/CRSentinel.md:139` — 10:27:20 `sha256sum` → `2e810b5d…a7c6`, 1,668 L, worktree ` M`,
  with `@@R16_ROUNDGATE_TABLE@@` and `@@R16_ROUNDGATE_SPEC@@` live; `:141` — 10:27:45 back to
  `75ed934d…adc5` = HEAD blob; `:142` — staging copy at 10:28:43.
- `w1/CR23.md:113` — first regression at `2026-10-20T13:27:04Z` read `2e810b5d…` and ended
  `REGRESSION: SETUP (cases=7 passed=6 cannot-verify=1)` / rc 2; the 13:29Z re-run is the PASS.
  (Caveat: that PASS is the six-leg `75ed934d`, not the committed seven-leg `89722ddb`.)

So “shown able to fail” is documented by two independent seats with commands and hashes — but as
observation, not as a retained detector.

### 5.2 “Installed after the readers finish” — consistent, by inference from two receipts

```
e69b488 committer  2026-10-20T10:39:59-03:00  (= 13:39:59Z)  wave-1 reports land
sweep.log:2        MUTATE_DATE 13:40:15Z, MUTATE_TOOL sha256=75ed934d… (pre-install)
runner-regression.txt:2  REGRESSION_DATE 13:41:49Z, REGRESSION_TOOL sha256=89722ddb…
```

Install is bounded in (13:40:15Z, 13:41:49Z), i.e. after the wave-1 landing. No direct install
log exists; this is [INFERENCE] from the two receipts, and it is the only gap in that half.

### 5.3 “Every receipt names the instrument sha it ran” — **fails at this HEAD** (minor)

Classifying every file under `.ufo/evidence/round-16/round-gate/`:

| Receipt | Names instrument sha? |
|---|---|
| `sweep/sweep.log:1` | yes — `sha256=75ed934d…` (the tool that ran the sweep) |
| `runner-regression.txt:1` + per-case `REGRESSION_PIN` | yes — `sha256=89722ddb…` |
| `runner-selftest.txt` (84 lines) | **no** — no `sha256=` anywhere |
| `runner-sha256.txt` | sha only, no verdict (companion, not a receipt) |
| `sweep/evidence/*.out`, `results.tsv`, `defects.tsv` | target outputs/derived tables — not instrument receipts |
| `survivor-probes/*.log` | produced by `probes.mjs`; it never invokes `mutate-and-run.sh` |

Structural cause: the instrument prints `MUTATE_TOOL` only in the sweep path
(`tools/mutate-and-run.sh:442`); `selftest()` (`:1259`) prints none. Re-ran the committed
instrument in scratch:

```
$ bash tools/mutate-and-run.sh --selftest
… MUTATE_SELFTEST: 81/81 pass / VERDICT: PASS      rc=0
$ grep -cE 'sha256=[0-9a-f]{64}' out.txt
0
$ diff out.txt runner-selftest.txt
83a84
> rc=0                                               # only the harness-appended rc line differs
```

The retained receipt is authentic and reproduces, but a `--selftest` receipt *cannot* satisfy the
criterion's universal under the current instrument. Accurate wording: *“every sweep and regression
receipt names the instrument sha it ran; a `--selftest` receipt is bound by the adjacent
`runner-sha256.txt`.”*

Adjacent fact (context, not a criterion-20 violation): 12 of the 31 w1 reports that mention
`tools/mutate-and-run.sh` do not name `75ed934d` (CR14, CRMeasure, CRRevenger, FrontierMap,
Overlap1, Overlap2, PITSource, ProvinceBox4, RGControl, RGSentinel, RGSpecB, RGSpecD). I sampled
CRMeasure, RGSentinel, RGControl and ProvinceBox4 — each *reads* the tool, none runs it, so they
are not instrument receipts. Only CR23/CRSentinel/RGLeg ran it and all three name the sha.

### 5.4 Record precision — the installed bytes are not the staged bytes

```
$ diff staged.sh installed.sh      # 5 hunks, 8 removed / 55 added
@@ -88,7 +88,7 @@   -@@RG_KILLED@@/10 (@@RG_PCT@@ %)   +5/10 (50 %)
@@ -567,7 +567,7 @@  -TABLE_ROUNDGATE='@@R16_ROUNDGATE_TABLE@@'
@@ -898,11 +898,68 @@ pre-registered spec body substitution (57 lines)
@@ -1161,7 +1218,7 @@
  - "$specs/js-round-gate.spec" 'node "$MUTANT" --selftest' "$TABLE_ROUNDGATE"
  + "$specs/js-round-gate.spec" 'h="$WORKDIR/sandbox-$DEFECT_ID"; … exec env -i …' "$TABLE_ROUNDGATE"
@@ -1607,7 +1664,7 @@ -…:10:@@RG_KILLED@@'   +…:10:5'
```

Four hunks are the declared placeholder substitutions. The fifth is a **non-marker suite change**
at install time: the staged copy's bare `node "$MUTANT" --selftest` becomes the guarded `env -i`
sandbox — consistent with gate decision G5 (`corpus/lessons/round-16.md:22`), but nowhere recorded
as an install-time change. The lesson row's “the staged copy was installed”
(`corpus/lessons/round-16.md:56`) is therefore loose: the *staged design* was installed after a
suite-string repair plus substitution. The criterion does not claim byte identity, so this is a
record-precision note, not a criterion defect.

## 6. Findings by severity

1. **Minor (wording, criterion 20).** “Every receipt names the instrument sha it ran” is false for
   the round's own selftest receipt and is structurally unsatisfiable by `--selftest`
   (`tools/mutate-and-run.sh:442` vs `:1259`; `.ufo/evidence/round-16/round-gate/runner-selftest.txt`).
   Fix: scope the universal to sweep/regression receipts, or emit `MUTATE_TOOL` from `selftest()`.
2. **Minor (wording, criterion 18).** “Keeps any prior structured branch (JSON) unchanged” is true
   of the branch's id extraction and of all six retained JSON rows, but not of the null-id fallback
   (`reattribute.py:80-87` vs `:121-127`; constructed input shown in §3.3). No fixture covers the
   JSON branch.
3. **Minor (retention, criterion 19).** The guard that makes the sweep able to fail exists only as
   a code block in `w1/Misroot.md §4`; nothing under `.ufo/evidence/round-16/` is executable. It
   reproduces, but a future round must retype it.
4. **Note (record, not criterion).** `corpus/lessons/round-16.md:56` says the staged copy was
   installed; the installed `89722ddb…` differs by a non-marker suite change (§5.4).

Nothing blocking: no criterion is false in the sense in which it would be applied, criteria 1–17
are untouched, and every named falsifier was re-executed here and fired.

## 7. Residual risk and verification gaps

- `agent://` vs bare-id write behavior was not replayed (lane bounds); the archived 605 B file plus
  the 66/66 round-15 census are the evidence.
- Criterion 20's “installed after the readers finish” is an inference from two timestamps; no
  install command/timestamp is retained.
- Criterion 18's JSON-branch clause is code-asserted, not fixture-tested; I tested it by importing
  the module and constructing the null-id input.
- The `.ufo/waves/round-16/w1/` reports are wave-1 seat outputs; I used them as evidence pointers
  only and re-derived every measurement independently where the tool allowed.

## 8. Command log (observed; all from committed bytes in `/tmp`)

| Command | rc | Key line |
|---|---|---|
| `git diff --numstat e69b488 c699c8c -- corpus/QUALITY.md` | 0 | `21 0`; single append hunk at `-82,3` |
| `python3 reattribute.py --selftest` | 0 | `new rule 4/4; old rule fails 3/4`; sha `3c419055…` |
| `python3 reattribute.py` | 0 | `already exists with identical bytes; left unchanged`; 2 corrections |
| `git rev-parse e69b488:c699c8c` blob of `verification-3.json` | 0 | both `87987fb8…193`; content `3c419055…` |
| import `reattribute` + null-id JSON comparison | 0 | old `'context_consistent'` vs new `None` |
| `json` count over `dispatch1.json` (round 16) | 0 | 68 tasks, `{1: 68}` URI, 0 bare |
| `json` count over `dispatch1.json` (round 15) | 0 | 66 tasks, 0 URI, 66 bare |
| `git status --porcelain` on mirror + archived bytes | 0 | `?? TameshiR15` |
| `git status --porcelain -- .ufo/` on same mirror | 0 | empty |
| `./guard2.sh <mirror>` (artifact / clean) | 1 / 0 | `STRAY [TameshiR15] (file, LANE-NOTE)` / empty |
| `grep -qiE 'shokunin\|tameshi\|agent://' <archived>` | 1 | no match |
| `sha256sum /home/.../misroots/TameshiR15` | 0 | `b413df98…6469`, 605 B |
| `diff staged.sh installed.sh` | 1 | 5 hunks; suite string + 4 substitutions |
| `bash tools/mutate-and-run.sh --selftest` (committed bytes) | 0 | `81/81 pass`, `VERDICT: PASS`, 0 sha lines |
| `diff out.txt runner-selftest.txt` | 1 | `83a84 > rc=0` only |

**One-line verdict:** criteria 18 and 19 hold end-to-end and criterion 20 holds on staging and
install ordering, but criterion 20's “every receipt” universal and criterion 18's JSON “unchanged”
clause overstate their evidence — **partial**, no blocking gap.
