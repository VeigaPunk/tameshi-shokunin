# ProbeIntegrations — does the non-hermetic `--integrations` group kill any round-26 survivor?

**Verdict: NO. The `--integrations` group kills none of the five survivors
(`S_OOR_EDGE`, `S_STRICT`, `S_EMPTY_GUARD`, `S_USAGE`, `S_PIN_INCLUDES`).**
Over today's live trees, every one of the five mutant copies produces **byte-identical
`--integrations` stdout and the same exit status** as the pristine pin. One of them
(`S_OOR_EDGE`) even changes the group's informational live-error list — 572 error
findings become 571 — and still flips no assertion.

**Second verdict (the one that matters for the ledger): the `--integrations` group
cannot serve as a mutation oracle for the ninth leg at all.** It is *red at the
pristine pin* on today's live trees (6 of 9 cases pass, exit status 1), so exit
status has zero discriminating power; and with no live tree present it is a *green
no-op* (0 of 0 cases run, `VERDICT: PASS`, exit status 0). The ninth recorded
mutation leg must therefore stay hermetic-only, exactly as the runner and the
interop judge already have it.

This is an **observation**, not a re-measurement: the recorded sweep at
`.ufo/evidence/round-26/cite-check/sweep/results.tsv` remains the measurement of
record, and the ledger leg still uses the hermetic group only.

---

## 0. Axes (godspeed naming)

Round 26's owned axis is **depth**. For this probe the frontier that actually moves
is three axes, and all three were measured:

| axis | question | outcome |
|---|---|---|
| **kill power** | does the integration group flip any case for any of the five survivors? | no, on all five |
| **oracle usability** | is the group green, stable and discriminating at the pristine pin? | no: red at baseline, green no-op without a live tree |
| **coupling cost** | what does running it couple the runner to? | live src tree (1145 files), live self tree, fleet root, git repos behind pins, 4.0 s per run versus 0.15 s for the hermetic group |

Moves kept: the five-mutant per-case comparison, the two-batch reproducibility
check, the `--strict` supplementary probe, and the no-live-tree skip probe. All
are in the evidence below. No production file was touched.

---

## 1. Materialization of the pin and of the five mutants

Both the pristine pin and the five mutants were built in the `/tmp` scratch dir
`/tmp/r26-probe`. Nothing was executed inside
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`.

```
$ mkdir -p /tmp/r26-probe && cd /tmp/r26-probe
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show \
    1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs > pristine.mjs
$ sha256sum pristine.mjs
40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f  pristine.mjs
$ wc -l pristine.mjs
2537 pristine.mjs
```

The digest matches the frozen pin recorded in
`.ufo/evidence/round-26/cite-check/predictions.json` (`"pin_sha256":
"40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f"`) and the
spec header line 2 of
`.ufo/evidence/round-26/cite-check/cite-check.defects.spec`; the line count
matches the spec's `2537 lines`.

Each mutant is a copy of the pinned file with exactly one replacement, taken
verbatim from the spec's `@old` / `@new` pairs, and each `@old` was asserted to
occur **exactly once** in the pinned bytes. The generator is
`/tmp/r26-probe/mkmutants.py`; its observed output:

```
$ cd /tmp/r26-probe && python3 mkmutants.py
S_OOR_EDGE	occurrences=1	bytes=126486	sha256=f1b41c7f59c030111a134c85433b238eab03214ada4746dd7c3b9ac156efb093
S_STRICT	occurrences=1	bytes=126478	sha256=caf4d03911d7cc0ef301612f96c3f2c8d0083fab7cc5921017ebf061525fb921
S_EMPTY_GUARD	occurrences=1	bytes=126451	sha256=949c29035366702b3e93ca9d8ed5a6df25275f104ebe72490a7cc11893bea5d5
S_USAGE	occurrences=1	bytes=126478	sha256=0ec5fff61e3c91e13a3b87b71106921633ebdf107e2e6fbb33a018cddfe3afcd
S_PIN_INCLUDES	occurrences=1	bytes=126476	sha256=206a7f94a948dd98c8f92c3e77b50a47aba20d1356d2e6b7c3ae6efe8387c0bc
pristine	sha256=40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f
```

**These five digests are identical to the `mutant-sha256` column of the recorded
sweep** `.ufo/evidence/round-26/cite-check/sweep/results.tsv` (rows
`S_OOR_EDGE`, `S_STRICT`, `S_EMPTY_GUARD`, `S_USAGE`, `S_PIN_INCLUDES`). The
bytes probed here are therefore the *same* mutant bytes that the hermetic sweep
ran — this probe adds no new mutation.

---

## 2. The probe command, and what it reads

```
node <copy> --integrations \
     --src  /home/vgpnk/Projects/ufo-fsd-alpha \
     --self /home/vgpnk/Projects/shokunin/kumitate-shokunin
```

`--fleet` was left at the tool's default, `dirname(--self)` =
`/home/vgpnk/Projects/shokunin` (the fleet root); the group's fleet-rung case
resolved `kasegi-shokunin/corpus/knowledge/program-quirks.md`. All reads are
read-only: the group copies the live self tree into a temp dir for its mutation
case (`copyDocs(realSelf, copy)`, pinned line 2374) and never writes to
the live trees. Node `v24.21.0`.

All six runs (pristine + five mutants) were launched concurrently; a second
independent batch was run later as a reproducibility check (§6).

---

## 3. Pristine baseline: the nine integration cases

```
$ cd /tmp/r26-probe && time node pristine.mjs --integrations \
    --src /home/vgpnk/Projects/ufo-fsd-alpha \
    --self /home/vgpnk/Projects/shokunin/kumitate-shokunin
kumitate cite-check --integrations
group: integration
PASS  real docs repaired: no F1-class finding (GateDecision off-line) — 0 SYMBOL_OFF_LINE for GateDecision
FAIL  real docs repaired: no F4-class finding (primeagent-assimilation.json ref) — corpus/knowledge/queue-summary.md:144 UNRESOLVED, corpus/knowledge/queue-summary.md:223 UNRESOLVED, corpus/knowledge/queue-summary.md:234 UNRESOLVED
PASS  real symbol machinery fires on a repaired site (mutation copy) — SKILL.md:355 GateDecision not on crates/ufo-core-runtime/src/gate.rs:11 — occurs at line(s) 15, 70, 76, 93, 98, 155, …
FAIL  real F2 omp_role_chains.rs → generated, informational — not reported
FAIL  real F3 content pin ba5e02be resolves-by-content (never REV_UNKNOWN) — content=0 revUnknown=1
PASS  real pin staleness: b18e0274d reports commits-behind-HEAD — pin b18e0274d (git pin) resolved-by-git:src (42 commits behind HEAD)
PASS  real fleet doc rung: sibling-lane program-quirks.md resolves under --fleet — fleet kasegi-shokunin/corpus/knowledge/program-quirks.md
PASS  real good samples stay clean (no error-level finding) — 0 error-level findings on the 16 samples
PASS  real index size matches a pruned live find — indexSize=1145 live-find=1145
6/9 cases passed (integration)
live error findings under /home/vgpnk/Projects/shokunin/kumitate-shokunin:
  … 572 error lines …
VERDICT: FAIL
exit status 1
real 0m4.024s
```

**The pristine pin is already RED on today's live trees: 6/9 cases, exit status 1.**
Three cases fail because the pinned expectations were written against an older
live tree and today's content has moved past them:

- F4 (`primeagent-assimilation.json`): today's
  `corpus/knowledge/queue-summary.md:144,223,234` cite `config/primeagent-assimilation.json`,
  which does not exist under the src tree, so it grades `UNRESOLVED` (error).
- F2 (`omp_role_chains.rs` → generated): the file is no longer classified
  `generated` on today's tree, so the note is "not reported".
- F3 (`ba5e02be`): today's `scripts/fleet-dispatcher.mjs` no longer hashes to
  `ba5e02be…`, so the pin resolves to `REV_UNKNOWN` (`content=0 revUnknown=1`).

A baseline that is already failing cannot certify a kill: the exit status is 1 for
every variant, pristine and mutant alike.

---

## 4. The measurement: pristine versus each of the five survivors

Kill criterion used (stated before reading the results): a mutant is *killed* by
the group if, over the same live trees, the mutant's exit status or any of the
nine case outcomes (the `PASS`/`FAIL`/`SKIP` flag **or** the detail text) differs
from the pristine pin's.

| mutant | exit | case outcomes vs pristine | full stdout diff vs pristine |
|---|---|---|---|
| `S_OOR_EDGE` | 1 (same) | identical: same 6 passes, same 3 failures, same detail strings | **1 line removed** (one live error finding) |
| `S_STRICT` | 1 (same) | identical | 0 lines |
| `S_EMPTY_GUARD` | 1 (same) | identical | 0 lines |
| `S_USAGE` | 1 (same) | identical | 0 lines |
| `S_PIN_INCLUDES` | 1 (same) | identical | 0 lines |

Observed diffs, verbatim:

```
$ cd /tmp/r26-probe/runs
$ for f in S_OOR_EDGE S_STRICT S_EMPTY_GUARD S_USAGE S_PIN_INCLUDES; do
    diff pristine.txt $f.txt | grep -c '^[<>]'
  done
1
0
0
0
0
```

```
$ diff pristine.txt S_OOR_EDGE.txt
146d145
<   corpus/knowledge/native-admission-detail.md:43  ERROR LINE_OOR          native_seats.rs:218-230
```

and for the four others, `diff` printed nothing at all.

The per-case comparison, explicitly:

```
$ for f in S_OOR_EDGE S_STRICT S_EMPTY_GUARD S_USAGE S_PIN_INCLUDES; do
    diff <(grep -E '^(PASS|FAIL|SKIP)  ' pristine.txt) \
         <(grep -E '^(PASS|FAIL|SKIP)  ' $f.txt) && echo "$f: case outcomes IDENTICAL"
  done
S_OOR_EDGE: case outcomes IDENTICAL
S_STRICT: case outcomes IDENTICAL
S_EMPTY_GUARD: case outcomes IDENTICAL
S_USAGE: case outcomes IDENTICAL
S_PIN_INCLUDES: case outcomes IDENTICAL
```

Live-error counts (the informational block printed under the group):

```
pristine: 572 error findings, VERDICT: FAIL, 6/9 cases passed (integration)
S_OOR_EDGE: 571 error findings, VERDICT: FAIL, 6/9 cases passed (integration)
S_STRICT: 572 error findings, VERDICT: FAIL, 6/9 cases passed (integration)
S_EMPTY_GUARD: 572 error findings, VERDICT: FAIL, 6/9 cases passed (integration)
S_USAGE: 572 error findings, VERDICT: FAIL, 6/9 cases passed (integration)
S_PIN_INCLUDES: 572 error findings, VERDICT: FAIL, 6/9 cases passed (integration)
```

---

## 5. The one observable effect, and why it is not a kill

`S_OOR_EDGE` widens the line-range predicate by exactly one line (pinned line
1312: `const bad = ref.start > n || ref.end > n;` → `... > n + 1 ...`). Exactly one
live citation in today's tree sits on that boundary:
`corpus/knowledge/native-admission-detail.md:43` cites `native_seats.rs:218-230`,
and the file
`/home/vgpnk/Projects/ufo-fsd-alpha/crates/ufo-core-runtime/src/native_seats.rs`
has 229 lines (`wc -l` → 229; `countLines` at pinned line 336-340 gives 229), so the
cited end line 230 is `n + 1`. Pristine flags it `LINE_OOR`; the mutant does not.

That difference is **printed but never asserted**. The group's verdict comes from
the nine cases only — pinned line 2471 (`verdict: failed ? 'FAIL' : 'PASS'`) and
line 2474 — and the `liveErrors` array is carried alongside without feeding any
case (pinned lines 2360-2362 build it; it is reported, never checked). The nine
assertions are all "no bad finding" (absence) or "this specific finding is
present" (presence) shapes, and none of them counts live errors, so one fewer
`LINE_OOR` in the informational list changes nothing.

Note also that the group *did* have a chance to catch this mutant and did not: the
"real good samples stay clean" case asserts that the 16 curated samples carry no
error-level finding — an absence assertion, which a *relaxing* mutant can only
help, never break.

---

## 6. Reproducibility (two independent batches)

The live trees are mutable, so a single batch could in principle have raced a
concurrent edit. Two full batches (six runs each) were executed and compared
byte for byte:

```
$ for f in pristine S_OOR_EDGE S_STRICT S_EMPTY_GUARD S_USAGE S_PIN_INCLUDES; do
    if diff -q runs/$f.txt runs2/$f.txt >/dev/null; then echo "$f: IDENTICAL"; else echo "$f: DIFFERS"; fi
  done
pristine: IDENTICAL (exit 1 vs 1)
S_OOR_EDGE: IDENTICAL (exit 1 vs 1)
S_STRICT: IDENTICAL (exit 1 vs 1)
S_EMPTY_GUARD: IDENTICAL (exit 1 vs 1)
S_USAGE: IDENTICAL (exit 1 vs 1)
S_PIN_INCLUDES: IDENTICAL (exit 1 vs 1)
```

Both batches ran in about 4.4 s and 5.0 s of wall clock, six runs in parallel.

---

## 7. Supplementary probes (two, both cheap)

### 7.1 With `--strict`

`S_STRICT` changes `opts.strict && totals.warn > 0` to `> 1` (pinned line 1589).
Since `--integrations` alone never sets `--strict`, the group was also run with
it, to check whether the strict arm is reachable from the group at all:

```
$ node pristine.mjs --integrations --strict --src … --self …    # exit 1
$ node mut/S_STRICT.mjs --integrations --strict --src … --self … # exit 1
$ diff <(grep -E '^(PASS|FAIL|SKIP)  ' strict/pristine.txt) \
       <(grep -E '^(PASS|FAIL|SKIP)  ' strict/S_STRICT.txt) && echo IDENTICAL
IDENTICAL case outcomes under --strict
$ diff strict/pristine.txt strict/S_STRICT.txt
   (no output)
```

Structurally this is expected: `drift` is consumed only at pinned line 1590 to
build `runCheck`'s `verdict` string, and the integration group never reads
`report.verdict` — it builds its own verdict from the nine cases (pinned lines
2466-2474). The strict arm is therefore unreachable from the group on any input.

### 7.2 Without a live tree (the skip path)

The group only runs when both `crates/ufo-core-runtime/src/gate.rs` under
`--src` and `SKILL.md` under `--self` exist (pinned line 2357). Pointing `--src`
at an empty directory:

```
$ node pristine.mjs --integrations --src /tmp/r26-probe/emptysrc \
    --self /home/vgpnk/Projects/shokunin/kumitate-shokunin
kumitate cite-check --integrations
group: integration
SKIP  real-tree F1–F4 + good samples — SKIP (no live tree at /tmp/r26-probe/emptysrc / /home/vgpnk/Projects/shokunin/kumitate-shokunin)
0/0 cases passed (integration)
VERDICT: PASS
exit status 0
```

**A green no-op.** In any environment without the live trees — a CI container, a
sandbox, a clone of the wrong repo — the group reports `VERDICT: PASS` with zero
cases run. A mutation oracle that passes when it cannot see anything is worse
than no oracle.

---

## 8. Structural argument: the nine assertions cannot kill these five

This is why the negative result above is not an accident of today's tree state.

| # | integration case (pinned lines) | shape | what it depends on | can it kill one of the five? |
|---|---|---|---|---|
| 1 | F1 absence, `SYMBOL_OFF_LINE` for `GateDecision` (2363-2366) | absence | symbol machinery | no |
| 2 | F4 absence, `primeagent-assimilation.json` (2367-2371) | absence | path resolution | no |
| 3 | mutation copy fires `SYMBOL_OFF_LINE` (2372-2384) | presence | symbol machinery, ref line 11 of a 203-line file (in range) | no |
| 4 | F2 `omp_role_chains.rs` generated note (2385-2388) | presence | file classification | no |
| 5 | F3 content pin `ba5e02be` (2389-2394) | presence + counts | the sha256-kind content-pin compare at pinned line 1195 | **only** `S_PIN_INCLUDES`, and only as a *mask*: if the cited file's sha256 contained `ba5e02be` anywhere but at its head, the mutant would turn a `PIN_MISMATCH` into an `OK` and change the counts. Today's digest contains it nowhere (identical output, measured). Note the git-pin path at line 1219 is untouched. |
| 6 | pin staleness `b18e0274d` (2395-2398) | presence | git resolution | no |
| 7 | fleet rung `program-quirks.md` (2399-2403) | presence | name resolution | no |
| 8 | 16 good samples clean (2404-2445) | absence | absence of findings | no — a *relaxing* mutant can only remove findings |
| 9 | index size equals a pruned live `find` (2446-2450) | equality | file count | no |

The four mutants that touch `runCheck`'s verdict expression (`S_STRICT` at line
1589, `S_EMPTY_GUARD` at line 1590) and the usage exit (`S_USAGE` at line 2512,
reachable only from `main()`'s `parseArgs` failure path) are **outside the
group's read set entirely**: the group computes its verdict from the nine cases
(pinned lines 2466-2474) and never consults `report.verdict`; and the group
never passes an unknown flag, so the usage arm is never taken. `S_OOR_EDGE`
(pinned line 1312) touches a predicate the nine assertions only consume through
absence-shaped checks, which a relaxation can only help.

So: on any live-tree state, the only assertion whose inputs any of the five
mutants can change is case 5, and the change it could produce is a *false green*
(a `PIN_MISMATCH` hidden), not a kill — and only when the baseline is green,
which today it is not.

---

## 9. Smallest safe correction implied (for the lane's integrator; NOT applied here)

Nothing in the production tree needs correcting because of this probe — the probe
found no defect. The correction is to the **ledger design**, and it is the one the
runner already implements:

1. **Keep the ninth leg (`js-cite-check`) hermetic-only.** Do not wire
   `--integrations` into `tools/mutate-and-run.sh` or into the interop judge. The
   reasons, measured above: it is red at the pristine pin on today's live trees
   (6/9, exit 1), it is a green no-op without a live tree (0/0, exit 0), it reads
   1145 live src files plus the self tree, the fleet root and the git repos behind
   pins, and it costs 4.0 s per run against 0.15 s for the hermetic group. A
   baseline-red oracle cannot certify a kill.
2. **If the lane wants off-suite falsifiers for these five survivors, use the
   public CLI over a synthetic tree**, which the sibling probes in this wave
   (`ProbeSOOREDGE.md`, `ProbeSUSAGE.md`) already do: the public CLI is
   hermetic-able, needs no live tree, and does separate `S_OOR_EDGE` (exit 1 vs 0
   on a citation of line n+1). This group adds nothing to that and costs the
   hermeticity the ninth leg depends on.
3. **No change to the recorded sweep.** `.ufo/evidence/round-26/cite-check/sweep/results.tsv`
   remains the measurement of record (5 of 10 killed, 5 survivors); this report is
   an observation about a second, non-hermetic group, and it changes no verdict.

---

## 10. Environment, tooling, bounds

- Node `v24.21.0`; Python 3 (standard library only); `git` for a read-only
  `show` of the pinned blob.
- **No packages were installed or upgraded by this seat**, so there is no install
  record to report.
- Scratch space: `/tmp/r26-probe` (pristine copy, five mutants, generator script,
  two run batches, strict batch, skip probe). Nothing was executed inside
  `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
- The sibling lane `/home/vgpnk/Projects/shokunin/kumitate-shokunin` was read
  with read-only git (`git show <rev>:scripts/cite-check.mjs`) and read-only file
  reads; the live src tree `/home/vgpnk/Projects/ufo-fsd-alpha` and the fleet
  root were read only, by the tool under test.
- **No git write command** (`add`, `commit`, `checkout`, `reset`, `stash`,
  `push`, `fetch`, `pull`) was run in the lane, and **no `jj` command was run
  anywhere** — not at the fleet root, not in the lane, not in a clone.
- No seat was spawned; the single permitted labrat probe was not needed.
- Files written by this seat: this report only.

### Sources opened this session

- `/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/cite-check.mjs` at
  rev `1205c6621a2eccbb8ffceae86d9e7b79a7990b3a` (read 2026-10-22, via
  `git show` into `/tmp/r26-probe/pristine.mjs`; sha256
  `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`, 2537 lines).
  Quote, pinned line 1312: `const bad = ref.start > n || ref.end > n;`
- `/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/cite-check.mjs`,
  pinned lines 2466-2474. Quote: `verdict: failed ? 'FAIL' : 'PASS',`
- `/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/cite-check.mjs`,
  pinned line 2357. Quote: `existsSync(join(realSrc, 'crates', 'ufo-core-runtime', 'src', 'gate.rs'))`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-26/cite-check/cite-check.defects.spec`
  (read 2026-10-22). Quote, the header line 2: `blob sha256 40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f, 2537 lines`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-26/cite-check/sweep/results.tsv`
  (read 2026-10-22). Header quote: `id	verdict	exit	duration-ms	mutant-sha256	desc`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-26/cite-check/predictions.json`
  (read 2026-10-22). Quote: `"pin_sha256": "40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f"`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-26/contract.json`
  (read 2026-10-22). Quote: `"name": "js-cite-check"`

---

## 11. Files changed

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-26/w1/ProbeIntegrations.md`
  (this report) — the only lane file touched by this seat.

PROBE INTEGRATIONS: NO SURVIVOR KILLED; GROUP IS RED AT BASELINE AND A GREEN NO-OP WITHOUT A LIVE TREE
