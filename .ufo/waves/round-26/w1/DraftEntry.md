# C1 — draft knowledge entry `corpus/knowledge/mutation-case-kumitate-cite-check.md`

## Verdict

**The draft is complete and ready for the L1 to land.** It is in the shape of
`corpus/knowledge/mutation-case-kumitate-sources-check.md` (case 8): frontmatter keys
`source` / `verified-at` / `recheck` / `ground` first, then sections. Every number in it is
grounded in a file under `.ufo/evidence/round-26/cite-check/`, and each ground is quoted at
`path:line`. The full draft text is in the single fenced block at the end of this report.

Two findings the L1 must decide on before landing, both raised from evidence, not invented:

1. **S089 would duplicate S052's subject.** `corpus/SOURCES.md:61` already holds S052
   ("Supported mutators (Stryker Mutator docs)", `mined`, used-by the case-7 and case-8
   entries). The brief asks the frontmatter to name S089 as the Stryker supported-mutators
   page. I wrote S089 in as instructed and flagged it here; the L1 either opens a distinct
   S089 row or cites S052 instead.
2. **S088 and S089 do not exist as registry rows yet.** `corpus/SOURCES.md:323` reads
   `Next unused id: S088.` — the frontmatter ids are placeholders, as the brief says.

I wrote nothing except this report file. No production file, registry row, ledger or
`SKILL.md` was touched; no git write command and no `jj` command was run; no gate, selftest
or sweep was executed inside the lane.

## What I opened (all read-only)

| artifact | identity | how read |
|---|---|---|
| `.ufo/evidence/round-26/cite-check/cite-check.defects.spec` | sha256 `969f50d6a28121e02b091337c2267ec92bdc47a279124c6b7e73d4939576b208` | `read` |
| `.ufo/evidence/round-26/cite-check/predictions.json` | sha256 `f1d26201ffac81fdd7415ac325165807c0f721f841ec5608636ba415879c938e` | `read` |
| `.ufo/evidence/round-26/cite-check/sweep/sweep.txt` | sha256 `957952b8f4e3cb413b73af8830c17705b480b702807c269eda7a1bc148ad1893` | `read` |
| `.ufo/evidence/round-26/cite-check/sweep/results.tsv` | sha256 `daa25ff90a7982db74f9dd8d1fbde79265b17f4e829ded05b0b621f00a81112d` | `read` |
| `.ufo/evidence/round-26/cite-check/sweep/defects.tsv` | sha256 `ddbfa4f932527afc98ec4f4c86e5789247f3fc0d5fa52a84089b51761fbb812c` | `read` |
| `.ufo/evidence/round-26/cite-check/sweep/evidence/*.out` | 11 files (control + 10 mutants) | `read` + `grep` |
| `.ufo/evidence/round-26/cite-check/regression-worktree.stdout` | regression receipt, 2026-10-22T10:04:24Z | `read` |
| `.ufo/evidence/round-26/contract.json` | `tameshi-r26-contract-v1` | `read` |
| kumitate `scripts/cite-check.mjs` @ `1205c6621a2eccbb8ffceae86d9e7b79a7990b3a` | blob sha256 `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`, 2537 lines, 126735 B | `git show` into `/tmp/r26c1/cite-check.mjs` |
| `tools/mutate-and-run.sh` (landed) | sha256 `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de` | `sha256sum`, `read` |
| `tools/mte-interop.py` | `js-cite-check` → `TABLE_CITECHECK` at `:78` | `read` |
| `corpus/knowledge/mutation-case-kumitate-sources-check.md` (shape) | case 8 | `read` |
| `corpus/knowledge/mutation-case-kumitate-round-gate.md` (shape) | case 7 | `read` |
| `corpus/SOURCES.md` | rows S001/S052 + `:323` | `grep` |
| `SKILL.md:2078-2100` | the ninth-case section | `read` |
| `corpus/knowledge/fleet-kill-rate-ledger.md` | §2 cite-check probe row, §3 queue row, §4 classes | `read` |

## Commands run (all read-only, all observed)

```
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs > /tmp/r26c1/cite-check.mjs
$ sha256sum /tmp/r26c1/cite-check.mjs
40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f  /tmp/r26c1/cite-check.mjs
$ wc -l -c /tmp/r26c1/cite-check.mjs
  2537 126735 /tmp/r26c1/cite-check.mjs
```

Anchor location in the pinned bytes (a Python count of each spec `@old` line, run against
the same `/tmp` copy — every anchor occurred exactly once):

| id | `@old` line | occurrences | pinned line |
|---|---|---|---|
| K_UNRESOLVED_SEV | `SYMBOL_MISS: 'warn', … UNRESOLVED: 'error',` | 1 | 221 |
| K_PIN_KIND | `if (/sha256/i.test(marker) || /sha256/i.test(gap)) kind = 'sha256';` | 1 | 1127 |
| K_FENCE_TILDE | `` (`{3,}|~{3,})/; `` | 1 | 471 |
| K_MISSING_WORD | `kind = e.code === 'ENOENT' ? 'missing' : 'unreadable';` | 1 | 2519 |
| K_EMPTY_VERDICT / S_EMPTY_GUARD | `const verdict = totals.filesScanned > 0 && totals.resolved > 0 && !drift ? 'PASS' : 'FAIL';` | 1 | 1590 |
| S_OOR_EDGE | `const bad = ref.start > n \|\| ref.end > n;` | 1 | 1312 |
| S_STRICT | `const drift = totals.error > 0 \|\| (opts.strict && totals.warn > 0);` | 1 | 1589 |
| S_USAGE | `return 64;` | 1 | 2512 |
| S_PIN_INCLUDES | `} else if (digest.startsWith(pin.hex)) {` | 1 | 1195 |

```
$ diff .ufo/evidence/round-26/cite-check/cite-check.defects.spec .ufo/evidence/round-26/cite-check/sweep/spec.copy
(no output — byte-identical; both sha256 969f50d6…)
$ sha256sum tools/mutate-and-run.sh
fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de
$ git show 622d31d:tools/mutate-and-run.sh | sha256sum   # the runner that ran the sweep
d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b
$ git show -s --format='%H %cI %s' 622d31d
622d31d90b1fbc55c56e91a2b012bc18d6f1421a 2026-10-22T07:01:47-03:00 round-26: pre-register claims C1 …
$ git show -s --format='%H %cI %s' a08e85c
a08e85c5d7f899e8a5992e20517edb1a380d79eb 2026-10-22T07:06:40-03:00 round-26: ninth ledger leg js-cite-check …
$ node --version
v24.21.0
```

## Measured result (read from the committed receipts, not re-executed by this seat)

Control: `CONTROL: GREEN (exit=0 duration-ms=147 pristine-sha256=40573448…)`, `62/62 cases
passed (hermetic)`, `VERDICT: PASS` (`sweep/sweep.txt:2-11`, `sweep/evidence/control.out:65-66`).
Restore proof: `MUTATE_RESTORE: OK (target-sha256 before=… after=… pristine-sha256=…)`.
Summary: `MUTATE: DONE (target=cite-check.mjs defects=10 killed=5 survived=5 inconclusive=0
kill-rate=50%)`.

Kill rate **5/10 = 50 %**. Verdict predictions **10/10 held** (`predictions.json` vs
`sweep/results.tsv`). Attribution (which case killed which mutant) is a **separate**
reading: **4/5**, because K_FENCE_TILDE died on two cases other than its predicted one.

### Per-defect table with witness cases

`cases` is the suite's own counter in the mutant's `evidence/*.out`; `witness` is the FAIL
line, quoted from that file with its line number.

| id | edit (cite-check.mjs line) | predicted | measured | exit | cases | witness case (evidence file:line) |
|---|---|---|---|---|---|---|
| K_UNRESOLVED_SEV | severity table `UNRESOLVED: 'error'` → `'warn'` (:221) | KILLED | KILLED | 1 | 55/62 | `bogus-path → UNRESOLVED error` — FAIL `UNRESOLVED/warn @SKILL.md:3` (`K_UNRESOLVED_SEV.out:3`); plus 6 collateral FAILs at `:23, :45, :46, :47, :48, :61` |
| K_PIN_KIND | `kind = 'sha256'` → `'rev'` (:1127) | KILLED | KILLED | 1 | 61/62 | `content pin match → OK; mismatch → PIN_MISMATCH` — FAIL `match=yes mismatch=no` (`K_PIN_KIND.out:8`) |
| K_FENCE_TILDE | fence regex `~{3,}` → `~{4,}` (:471) | KILLED | KILLED | 1 | 60/62 | `fence content is never tokenized (by design, kept)` — FAIL `insideFence=1 afterFence=OK` (`:27`); `R16 regression: fence content is never tokenized under line-local pairing` — FAIL `fenceSpans=1 afterFence=OK` (`:39`) |
| K_MISSING_WORD | fail-closed word `'missing'` → `'absent'` (:2519) | KILLED | KILLED | 1 | 61/62 | `bare run (no --src): both candidates absent keeps the --src fail-closed arm (exit 2)` — FAIL, stderr `… is absent` (`:64`) |
| K_EMPTY_VERDICT | verdict drops both guards (:1590) | KILLED | KILLED | 1 | 61/62 | `fail-closed: empty scan set → exit-2 condition` — FAIL `filesScanned=0 verdict=PASS` (`:22`) |
| S_OOR_EDGE | `ref.start > n \|\| ref.end > n` → `> n + 1` (:1312) | SURVIVED | SURVIVED | 0 | 62/62 | none — every case PASS |
| S_STRICT | `opts.strict && totals.warn > 0` → `> 1` (:1589) | SURVIVED | SURVIVED | 0 | 62/62 | none |
| S_EMPTY_GUARD | verdict drops only the `filesScanned` guard (:1590) | SURVIVED | SURVIVED | 0 | 62/62 | none |
| S_USAGE | usage `return 64;` → `return 65;` (:2512) | SURVIVED | SURVIVED | 0 | 62/62 | none |
| S_PIN_INCLUDES | `digest.startsWith(pin.hex)` → `digest.includes(pin.hex)` (:1195) | SURVIVED | SURVIVED | 0 | 62/62 | none |

Total failing cases across the five kills: 7 + 1 + 2 + 1 + 1 = **12**.

### Prediction-witness mismatches

**M1 — K_FENCE_TILDE: verdict held, killing case differed (the only attribution
mismatch).** The predicted case was `R16 repro: ~~~ fence gives the same result as ```
(marker-symmetric)` (`predictions.json`, `K_FENCE_TILDE`). Under the mutant that case
**PASSED**, with the same detail as the pristine run:
`backtick=UNRESOLVED/error@line7 tilde=UNRESOLVED/error@line7`
(`K_FENCE_TILDE.out:24`; pristine `control.out:23`). The check asserts *equality* between
the backtick fixture and the tilde fixture. The mutation only removes the **opening** of a
three-tilde fence; the citation the tilde fence used to mask becomes visible at the same
line with the same kind and severity, so the two fixtures still agree — for the wrong
reason. The mutant died instead on the two "fence content is never tokenized" checks, whose
`insideFence` / `fenceSpans` counters go from 0 to 1 (`:27`, `:39`). A symmetric-equality
assert cannot see a one-sided grammar regression that makes the two sides agree; it needs
an absolute assert on the masked region.

**M2 — K_PIN_KIND: the predicted case failed, but the predicted *reason* is half wrong.**
`predictions.json` says rev-classified pins "come back REV_UNKNOWN, not OK or
PIN_MISMATCH". Measured: the matching pin came back **OK** (`match=yes`), because the rev
branch carries its own content fallback at `cite-check.mjs:1219` —
`if (digest && digest.startsWith(pin.hex)) resolvedBy = { how: 'content', … }` — which emits
`pin <hex> (<marker>) resolved-by-content`, and the check's regex accepts
`/resolved-by-content/` (`cite-check.mjs:1896`). Only the mismatching half behaved as
predicted: `0123456789ab` came back REV_UNKNOWN, so no PIN_MISMATCH finding existed and the
check read `mismatch=no` (`cite-check.mjs:1897`; `K_PIN_KIND.out:8`).

**M3 — K_UNRESOLVED_SEV: predicted case correct, breadth wider than predicted.** The
predicted case `bogus-path → UNRESOLVED error` did fail (`:3`), and six further cases failed
with it, because the suite asserts severity `error` for UNRESOLVED in seven places. The
prediction named one witness; the mutation killed seven.

**M4 — a second, unpinned `startsWith(pin.hex)` site.** `S_PIN_INCLUDES` edited the
sha256-branch compare at `:1195`. The rev-branch content compare at `:1219` carries the same
prefix semantics and was not edited — and the only check that would notice it
(`real F3 content pin ba5e02be resolves-by-content (never REV_UNKNOWN)`,
`cite-check.mjs:2389-2391`) is a `checkI(` **integration**-group case, which `--selftest`
does not execute. The gate holds 9 `checkI(` call sites (`cite-check.mjs:2363-2446`;
`gates-survey-kumitate.md:48`); none ran.

### Survivor classes (measured, none proved equivalent)

| id | class | why the suite cannot see it |
|---|---|---|
| S_OOR_EDGE | boundary at an untested granularity | the only LINE_OOR fixture cites `:999` in a 20-line file (`control.out:4`); the predicate's far-out branch is asserted, its edge (`n+1`) never is |
| S_STRICT | a CLI mode no hermetic case enables | `--strict` appears only in the usage text (`:10`, `:236`), the parser (`:264`), the drift predicate (`:1589`) and the renderer (`:1604`); no hermetic case passes it, so `warn > 0` vs `warn > 1` moves nothing |
| S_EMPTY_GUARD | a co-extensive guard | the empty-scan-set fixture has `filesScanned=0` **and** `resolved=0`, so dropping the first conjunct changes no fixture's outcome — the remaining conjunct still yields FAIL |
| S_USAGE | an out-of-band exit map | `parseArgs` throws on an unknown flag; `main` catches it, writes the message and USAGE to stderr and returns 64 (`:2509-2512`). The suite runs only `--selftest`, so no case exercises the arm |
| S_PIN_INCLUDES | a compare-direction asymmetry | the mismatch fixture hex `0123456789ab` is not a substring of the real digest, so a substring compare still reports PIN_MISMATCH; the *direction* of the compare (prefix vs anywhere) is unpinned |

All five are **PENDING** wave-2 off-suite probes. No survivor is declared equivalent and
none is probed here: equivalence is undecidable in general, and a survivor needs an
off-suite witness or an explicit equivalence argument.

### What the suite does not pin

1. The `--strict` promotion threshold (`:1589`).
2. The usage exit code and the whole unknown-flag arm (`:2512`).
3. The LINE_OOR edge at exactly `n+1` (`:1312`).
4. The `filesScanned` conjunct of the verdict (`:1590`), because the `resolved` conjunct is
   co-extensive on every fixture the suite builds.
5. The prefix-vs-substring direction of the content-pin compare (`:1195`) — and, separately,
   the rev-branch content compare at `:1219`, whose only check is in the integration group.
6. The whole integration group: 9 `checkI(` sites do not run under `--selftest`. The 62
   cases are the hermetic group only (`cite-check.mjs:81`, `gates-survey-kumitate.md:322`).
7. The verdict oracle is the process exit status only; the runner grades on exit status and
   nothing downstream reads the report body.
8. Byte-determinism of the run: one control per sweep, no repeated controls (F3 stays open).

### Method note (a step beyond case 8)

Case 8 recorded only the tail of each mutant run, so its per-check attribution was
impossible for 4 of its 5 kills. This case keeps the **full** per-mutant stdout
(`sweep/evidence/*.out`, 66 lines each) in the lane, which is why the witness column and
mismatch M1 can be stated at all. That is the difference between "the verdict was right" and
"this case killed it".

## Conflicts for the canonical judge (verbatim)

1. `predictions.json`, `K_FENCE_TILDE.reason`: "a three-tilde line stops opening a fence, so
   the tilde fixture tokenizes differently from the backtick fixture." — **contradicted by the
   measurement**: `K_FENCE_TILDE.out:24` shows the tilde fixture tokenizing *identically*
   (`backtick=UNRESOLVED/error@line7 tilde=UNRESOLVED/error@line7`), which is why the
   predicted case passed and the mutant died elsewhere.
2. `predictions.json`, `K_PIN_KIND.reason`: "rev-classified pins go to git resolution and come
   back REV_UNKNOWN, not OK or PIN_MISMATCH." — **half contradicted**: the matching pin came
   back OK via the rev-branch content fallback at `cite-check.mjs:1219`
   (`K_PIN_KIND.out:8`, `match=yes`).
3. The brief's instruction to name S089 as "Stryker supported-mutators page" — **overlaps
   S052**, which already is that row (`corpus/SOURCES.md:61`, `mined`).
4. `fleet-kill-rate-ledger.md` §2 records cite-check as a "PREP-T6 **probe**: 4 defects —
   **1 killed** … a probe, **not a sweep**" and §3's queue row says "**probe only, 1/4** …
   full sweep open". This case is that full sweep. The ledger cells are stale and need an
   append-only erratum (the ledger's own ER-3 update rule, `fleet-kill-rate-ledger.md` §8 U9).

## L1 obligations (not done by this seat — I wrote only my report)

Smallest safe corrections, in order:

1. Land `corpus/knowledge/mutation-case-kumitate-cite-check.md` from the block below.
2. Open S088 (the pinned kumitate file, kind `code`, tier A, anchor = rev + blob sha256 +
   `scripts/cite-check.mjs`, used-by = this entry) and S089, or point `source:` at the
   existing S052 row instead. `corpus/SOURCES.md:323` still reads `Next unused id: S088.`
3. Add a `corpus/README.md` row for the new entry (case 8's row is at
   `corpus/README.md:265`).
4. Append an erratum to `corpus/knowledge/fleet-kill-rate-ledger.md` superseding the §2
   cite-check probe row and the §3 "probe only, 1/4" queue cell with this sweep's 5/10,
   its 62-case hermetic suite, the five survivor classes, and the pin.
5. Add the `LOG.md` entry and the coverage-map row (the round-18 precedent named in case 8's
   §6).
6. Verify the counter after landing: `python3 .ufo/evidence/round-26/c1-measure.py --repo
   <clone at the landed rev>` → `C1_DEPTH: recorded_cases=9 wired_legs=9 depth_score=9`,
   exit 0. The counter reads the runner only; whether the recorded table equals a real sweep
   is the regression companion's check (contract C1 `bound`).

## Tools

No tool was installed or upgraded by this seat; the task needed none. Everything above used
what the host already had (`git`, `python3`, `node` v24.21.0, `sha256sum`, `grep`, `read`).

---

## Full draft text of `corpus/knowledge/mutation-case-kumitate-cite-check.md`

````markdown
source: S088 kumitate `scripts/cite-check.mjs` @ 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a (blob sha256 40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f, 2537 lines, 126735 bytes, mode 100755), read-only; S089 Stryker supported mutators (docs) — PLACEHOLDER ids, the L1 confirms (S052 already carries that subject); procedure: `corpus/knowledge/mutation-case-kumitate-round-gate.md` (case 7) and `corpus/knowledge/mutation-case-kumitate-sources-check.md` (case 8)
verified-at: 2026-10-22; pre-registration `622d31d90b1fbc55c56e91a2b012bc18d6f1421a` (2026-10-22T07:01:47-03:00 = 10:01:47Z), sweep 2026-10-22T10:02:07Z, regression replay 2026-10-22T10:04:24Z; receipts under `.ufo/evidence/round-26/cite-check/`
recheck: `git -C kumitate-shokunin show 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs | sha256sum` → `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`; `bash tools/mutate-and-run.sh --regression` → `REGRESSION_CASE js-cite-check: PASS` and `REGRESSION: PASS (cases=9 passed=9)`; hermetic suite string `env -i PATH HOME TMPDIR LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES node "$MUTANT" --selftest` → `62/62 cases passed (hermetic)`, `VERDICT: PASS`, exit 0
ground: none — the ninth recorded mutation case on a kumitate gate; no `corpus/README.md` frontier row moves. F3 (determinism precondition) stays open: this case ran one control per mutant, not N ≥ 3 byte-identical controls

# Mutation case 9 — kumitate `scripts/cite-check.mjs` (round 26)

The ninth recorded case and the fourth kumitate gate. Like cases 7 and 8, the
target is a kumitate `scripts/*` primary surface (tameshi's `PROVINCE.md:7-11`).
Kumitate's tree stayed read-only: the target is a byte copy materialized from its
git object store, and no owner opt-in was needed (kumitate `PROVINCE.md:15` names
the lane's own `scripts/*.mjs` as a member-level governed surface). Ownership is
split: kumitate owns the gate, tameshi owns the method and this measurement only.
This is not a service run and does not drain the service queue
(`service-optin-protocol.md` §0).

## 0. Pin and suite

- Target: rev `1205c6621a2eccbb8ffceae86d9e7b79a7990b3a`, blob sha256
  `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`,
  126,735 bytes, 2,537 lines, mode 100755. Sweep line:
  `MUTATE_TARGET: … cite-check.mjs sha256=40573448… bytes=126735`.
- Suite: `node "$MUTANT" --selftest`, hermetic group only, 62 cases,
  `62/62 cases passed (hermetic)`, `VERDICT: PASS`, exit 0
  (`sweep/evidence/control.out:65-66`). The run string is the same `env -i`
  shape as cases 7 and 8: `h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home"
  "$h/tmp" && cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp"
  LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" node "$MUTANT"
  --selftest`, with a per-defect private `HOME` and `TMPDIR`. Fixtures are
  temporary; the gate's own header records that `--selftest` "stats no live path"
  (`cite-check.mjs:114`).
- The gate holds two groups. `--selftest` runs hermetic only; `--integrations`
  alone runs the integration group (`cite-check.mjs:81`), and that group holds 9
  `checkI(` call sites (`cite-check.mjs:2363-2446`; `gates-survey-kumitate.md:48`).
  **None of them ran here.** Every number in this entry is hermetic-scoped.
- Control determinism: one pristine control per sweep, GREEN (exit 0, 147 ms),
  `MUTATE_RESTORE: OK` with the target sha unchanged before and after
  (`sweep/sweep.txt:2`, `:104`). Unlike case 8, no repeated-control measurement
  was taken for this leg, so byte-determinism of the hermetic run is not
  established here; verdicts are graded on exit status only. F3 stays open.

## 1. Pre-registration

Ten defects and their predictions were committed in `622d31d`
(2026-10-22T07:01:47-03:00 = 10:01:47Z) before any mutant ran; the sweep is
stamped `MUTATE_DATE: 2026-10-22T10:02:07Z` — twenty seconds later. The
committed files are `cite-check.defects.spec` (sha256 `969f50d6…b208`) and
`predictions.json` (schema `tameshi-r26-preregistration-v1`, sha256
`f1d26201…938e`). The sweep's own copy of the spec (`sweep/spec.copy`) is
byte-identical to the committed spec (same sha256; `diff` empty).

Each `@old` anchor is unique in the pinned bytes under the runner's rule. A count
on the pinned blob gives one occurrence for all ten, at these lines:
K_UNRESOLVED_SEV :221, K_PIN_KIND :1127, K_FENCE_TILDE :471, K_MISSING_WORD
:2519, K_EMPTY_VERDICT :1590, S_OOR_EDGE :1312, S_STRICT :1589, S_EMPTY_GUARD
:1590, S_USAGE :2512, S_PIN_INCLUDES :1195. K_EMPTY_VERDICT and S_EMPTY_GUARD
share the anchor line by construction: one edit removes both verdict guards, the
other removes the `filesScanned` guard alone.

Composition: 5 kill-aimed (predicted KILLED: K_UNRESOLVED_SEV, K_PIN_KIND,
K_FENCE_TILDE, K_MISSING_WORD, K_EMPTY_VERDICT) and 5 hole-aimed (predicted
SURVIVED: S_OOR_EDGE, S_STRICT, S_EMPTY_GUARD, S_USAGE, S_PIN_INCLUDES). Each
prediction names one selftest case and gives a reason (`predictions.json`). The
spec header names the matrix axes: severity table, pin classification, fence
grammar, fail-closed wording, verdict guards, line-range boundary, strict
promotion, usage exit, content-pin compare.

Operator families. By S089's (Stryker supported-mutators) named JS single-edit
classes, three edits are string-literal class (K_UNRESOLVED_SEV, K_PIN_KIND,
K_MISSING_WORD) and three are conditional-expression class (K_EMPTY_VERDICT,
S_EMPTY_GUARD, S_STRICT). Four are outside those named classes: S_OOR_EDGE and
S_USAGE shift a numeric literal, K_FENCE_TILDE changes a regex quantifier
(`~{3,}` → `~{4,}`), and S_PIN_INCLUDES swaps a method name
(`digest.startsWith` → `digest.includes`). This entry does not call any of them a
Stryker operator; the ten edits were chosen by hand from the suite's predicates.
No historical-performance selection (S008) was used.

## 2. Result — 5/10 killed (50 %), 10/10 verdict predictions held

Tool: `tools/mutate-and-run.sh`, sha256
`d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b`
(`MUTATE_TOOL` in `sweep/sweep.txt:1`) — the runner as it stood at the
pre-registration commit, before the leg was wired. The control was GREEN, exit 0,
`MUTATE_RESTORE: OK`, and the target sha was unchanged before and after
(`SWEEP_TARGET_RECHECK: PASS`). The runner reports killed, survived and
inconclusive only (inconclusive 0), so valid = 10 and kill rate = killed / 10.

| id | class | edit (cite-check.mjs line) | predicted | measured | exit | cases | witness case (evidence/*.out) |
|---|---|---|---|---|---|---|---|
| K_UNRESOLVED_SEV | severity table | `UNRESOLVED: 'error'` → `'warn'` (:221) | KILLED | KILLED | 1 | 55/62 | `bogus-path → UNRESOLVED error` — FAIL `UNRESOLVED/warn @SKILL.md:3` (`K_UNRESOLVED_SEV.out:3`); six more FAILs at `:23, :45, :46, :47, :48, :61` |
| K_PIN_KIND | pin classification | `kind = 'sha256'` → `'rev'` (:1127) | KILLED | KILLED | 1 | 61/62 | `content pin match → OK; mismatch → PIN_MISMATCH` — FAIL `match=yes mismatch=no` (`K_PIN_KIND.out:8`) |
| K_FENCE_TILDE | fence grammar | `~{3,}` → `~{4,}` in the fence-line regex (:471) | KILLED | KILLED | 1 | 60/62 | `fence content is never tokenized (by design, kept)` — FAIL `insideFence=1 afterFence=OK` (`:27`); `R16 regression: fence content is never tokenized under line-local pairing` — FAIL `fenceSpans=1 afterFence=OK` (`:39`) |
| K_MISSING_WORD | fail-closed wording | `'missing'` → `'absent'` (:2519) | KILLED | KILLED | 1 | 61/62 | `bare run (no --src): both candidates absent keeps the --src fail-closed arm (exit 2)` — FAIL, stderr `… is absent` (`:64`) |
| K_EMPTY_VERDICT | verdict guards | both guards dropped (:1590) | KILLED | KILLED | 1 | 61/62 | `fail-closed: empty scan set → exit-2 condition` — FAIL `filesScanned=0 verdict=PASS` (`:22`) |
| S_OOR_EDGE | line-range boundary | `ref.start > n \|\| ref.end > n` → `> n + 1` (:1312) | SURVIVED | SURVIVED | 0 | 62/62 | none — every case PASS |
| S_STRICT | strict promotion | `opts.strict && totals.warn > 0` → `> 1` (:1589) | SURVIVED | SURVIVED | 0 | 62/62 | none |
| S_EMPTY_GUARD | verdict guards | only the `filesScanned` guard dropped (:1590) | SURVIVED | SURVIVED | 0 | 62/62 | none |
| S_USAGE | usage exit | `return 64;` → `return 65;` (:2512) | SURVIVED | SURVIVED | 0 | 62/62 | none |
| S_PIN_INCLUDES | content-pin compare | `digest.startsWith(pin.hex)` → `digest.includes(pin.hex)` (:1195) | SURVIVED | SURVIVED | 0 | 62/62 | none |

Twelve cases failed across the five kills (7 + 1 + 2 + 1 + 1). Every survivor's
suite ends `62/62 cases passed (hermetic)`, `VERDICT: PASS`, exit 0.

Prediction accuracy and attribution are separate readings. The 10/10 compares
KILLED/SURVIVED against the prediction; it does not say *which case* killed a
mutant. On attribution this case reads **4/5**, for the reason in §3.

## 3. Prediction versus witness — where the named case was not the killing case

- **K_FENCE_TILDE — verdict held, killing case differed (the one attribution
  mismatch).** The predicted case was `R16 repro: ~~~ fence gives the same result
  as ``` (marker-symmetric)`. Under the mutant that case **PASSED**, with the same
  detail as the pristine run: `backtick=UNRESOLVED/error@line7
  tilde=UNRESOLVED/error@line7` (`K_FENCE_TILDE.out:24`; pristine
  `control.out:23`). The check asserts *equality* between the backtick fixture and
  the tilde fixture. The mutation removes only the **opening** of a three-tilde
  fence; the citation the tilde fence used to mask becomes visible at the same
  line with the same kind and severity, so the two fixtures still agree — for the
  wrong reason. The mutant died instead on the two "fence content is never
  tokenized" checks, whose `insideFence` / `fenceSpans` counters go from 0 to 1
  (`:27`, `:39`). A symmetric-equality assert cannot see a one-sided grammar
  regression that makes the two sides agree; it needs an absolute assert on the
  masked region. The prediction's stated reason ("the tilde fixture tokenizes
  differently from the backtick fixture") is contradicted by the measurement.
- **K_PIN_KIND — the predicted case failed, but the predicted reason is half
  wrong.** `predictions.json` says rev-classified pins "come back REV_UNKNOWN, not
  OK or PIN_MISMATCH". Measured: the matching pin came back **OK** (`match=yes`),
  because the rev branch carries its own content fallback at `cite-check.mjs:1219`
  — `if (digest && digest.startsWith(pin.hex)) resolvedBy = { how: 'content', … }`
  — which emits `pin <hex> (<marker>) resolved-by-content`, and the check's
  regex accepts `/resolved-by-content/` (`cite-check.mjs:1896`). Only the
  mismatching half behaved as predicted: `0123456789ab` came back REV_UNKNOWN,
  so no PIN_MISMATCH finding existed and the check read `mismatch=no`
  (`cite-check.mjs:1897`).
- **K_UNRESOLVED_SEV — predicted case correct, breadth wider than predicted.** The
  predicted case `bogus-path → UNRESOLVED error` did fail (`:3`), and six further
  cases failed with it, because the suite asserts UNRESOLVED severity `error` in
  seven places. One predicted witness, seven killed cases.
- **A second unpinned compare.** `S_PIN_INCLUDES` edited the sha256-branch compare
  at `:1195`. The rev-branch content compare at `:1219` carries the same prefix
  semantics and was not edited, and the only check that would notice it
  (`real F3 content pin ba5e02be resolves-by-content (never REV_UNKNOWN)`,
  `cite-check.mjs:2389-2391`) is a `checkI(` integration-group case, which
  `--selftest` does not run.

## 4. Survivors — non-equivalence PENDING

No survivor is declared equivalent and none is probed here. A survivor needs an
off-suite witness or an explicit equivalence argument; equivalence is not
measured.

| survivor | spec line | why the suite cannot see it | witness needed | status |
|---|---|---|---|---|
| S_OOR_EDGE | :1312 | the only LINE_OOR fixture cites `:999` in a 20-line file (`control.out:4`); the predicate's far-out branch is asserted, its edge (`n+1`) never is | a ref to exactly line `n+1` of a target file | PENDING |
| S_STRICT | :1589 | `--strict` appears only in the usage text (`:10`, `:236`), the parser (`:264`), the drift predicate (`:1589`) and the renderer (`:1604`); no hermetic case passes it | a warn-level finding under `--strict` | PENDING |
| S_EMPTY_GUARD | :1590 | the empty-scan-set fixture has `filesScanned=0` **and** `resolved=0`, so dropping the first conjunct changes no fixture's outcome — the remaining conjunct still yields FAIL (co-extensive guard) | a scan set with files scanned but zero resolved citations, or vice versa | PENDING |
| S_USAGE | :2512 | `parseArgs` throws on an unknown flag; `main` catches it, writes the message and USAGE to stderr and returns 64 (`:2509-2512`). The suite runs only `--selftest`, so the arm is never exercised | an unknown flag, asserting exit 64 | PENDING |
| S_PIN_INCLUDES | :1195 | the mismatch fixture hex `0123456789ab` is not a substring of the real digest, so a substring compare still reports PIN_MISMATCH; the compare's *direction* is unpinned | a content pin whose hex is an interior substring of the target digest | PENDING |

## 5. What the suite does not pin

1. The `--strict` promotion threshold (`:1589`).
2. The usage exit code and the whole unknown-flag arm (`:2512`).
3. The LINE_OOR edge at exactly `n+1` (`:1312`).
4. The `filesScanned` conjunct of the verdict (`:1590`), because the `resolved`
   conjunct is co-extensive on every fixture the suite builds.
5. The prefix-vs-substring direction of the content-pin compare (`:1195`) and,
   separately, the rev-branch content compare at `:1219`, whose only check is in
   the integration group.
6. The whole integration group: 9 `checkI(` sites do not run under `--selftest`.
   The 62 cases are the hermetic group only.
7. The verdict oracle is the process exit status only; the runner grades on exit
   status and nothing downstream reads the report body.
8. Byte-determinism of the run: one control per sweep, no repeated controls.

## 6. Ledger leg

`js-cite-check` is the ninth leg and the fourth kumitate gate in the ledger. It
holds the pin (git source, rev `1205c6621a2eccbb8ffceae86d9e7b79a7990b3a`, path
`scripts/cite-check.mjs`, mode 100755, sha `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`),
the spec, the recorded table and the guarded suite.

In the landed runner (`tools/mutate-and-run.sh` at sha256
`fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de`, revision
`a08e85c`): the ledger comment at `:95`, the spec heredoc at `:1082`, the
regression replay call at `:1424-1427`, the leg-check entry at `:1955`
(`'js-cite-check:js-cite-check.spec:TABLE_CITECHECK:10:5'`), and the table at
`:629`:

    TABLE_CITECHECK='K_UNRESOLVED_SEV:KILLED,K_PIN_KIND:KILLED,K_FENCE_TILDE:KILLED,K_MISSING_WORD:KILLED,K_EMPTY_VERDICT:KILLED,S_OOR_EDGE:SURVIVED,S_STRICT:SURVIVED,S_EMPTY_GUARD:SURVIVED,S_USAGE:SURVIVED,S_PIN_INCLUDES:SURVIVED'

Its suite string is the `env -i` form quoted in §0.
`tools/mte-interop.py:78` maps `'js-cite-check'` to `TABLE_CITECHECK`, so the
report-interop gate judges nine legs.

Replay receipt (`.ufo/evidence/round-26/cite-check/regression-worktree.stdout`,
2026-10-22T10:04:24Z, tool sha `fb91ef76…`):
`REGRESSION_CASE js-cite-check: PASS (band: killed-delta<=0 flips<=0 inconclusive=0 defects=10)`,
`REGRESSION_TABLE js-cite-check: match=10/10 recorded-killed=5 measured-killed=5 survived=5 inconclusive=0 flips=0`,
`REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)`.

The sweep itself ran with the *pre-wiring* runner (sha `d22c4025…`, the runner at
the pre-registration revision) against the standalone spec file; the leg's wiring
landed afterwards. The landed runner replays leg 9 from its own embedded spec and
reproduces the same 5/10 with `match=10/10` — that replay is the receipt tying
the landed bytes to the sweep.

The round-26 counter `.ufo/evidence/round-26/c1-measure.py` reads the runner
only: it counts the ledger comment lines and, per leg, checks the spec heredoc,
the regression call, the leg-check entry and the table's defect and KILLED counts.
It does not check that the recorded table equals a real sweep; that is the
regression companion's check (contract C1 `bound`).

## 7. Limits

- One revision (`1205c662`), one host (node v24.21.0, Linux), one control run per
  sweep. The 50 % is a property of this suite at this pin, not of kumitate's
  gates in general. It shares composition (5/5 by design) with cases 7 and 8's
  50 %, but the three suites and the three defect sets differ; do not compare
  them without the composition note.
- Scope: hermetic group only. The integration group (9 `checkI(` sites) did not
  run, so the measured rate is a lower bound on what the gate's own full suite
  would kill, not a rate for the gate's whole suite.
- The oracle is the process exit status. A mutant that keeps exit 0 while
  changing a finding's severity, kind or line is a survivor by this measurement.
- Survivors are not proved equivalent (§4). All five are PENDING wave-2
  off-suite probes.
- The four numeric, regex-quantifier and method-name edits sit outside the named
  JS single-edit operator classes (§1).
- Ownership: kumitate owns the gate and this entry measures its suite. No kill is
  attributed to any other gate. The pre-registration carries no
  fleet-versus-kumitate label and this entry does not add one.
- Suite sensitivity ≠ gate truth: nothing here measures whether cite-check's
  verdicts about the real world are right.
- The lane's standing ledger still carries cite-check as a four-defect probe
  (1/4, no composition, no full table) and as a queue row ("probe only, 1/4");
  this case is that full sweep, and the ledger's cells need an append-only
  erratum (the ledger's own update rule, `fleet-kill-rate-ledger.md` §8 U9).
- Corpus and registry obligations (L1, not done by this seat): S088 and S089 are
  placeholder ids — neither row exists yet (`corpus/SOURCES.md:323` reads
  `Next unused id: S088.`), and S089's subject (Stryker supported mutators) is
  already carried by S052 (`corpus/SOURCES.md:61`, `mined`, used-by the case-7 and
  case-8 entries). This entry needs a `corpus/README.md` row, a
  `fleet-kill-rate-ledger.md` erratum, a LOG.md entry and the coverage-map row.
````
