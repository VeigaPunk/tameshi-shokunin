# MtGuardGapsRecheck — round 26, wave 1 (routed item 4, first part)

**Verdict: all seventeen weakenings still SURVIVE at revision
`a08e85c5d7f899e8a5992e20517edb1a380d79eb`. 0/17 killed, 17/17 survived,
0 inconclusive — a 0 % kill rate, identical to the round-25 measurement.**

The survivors are not stale bookkeeping: a differential probe re-confirms, for
each of the seventeen, that the pristine gate **refuses** the recorded
discriminating bundle while the mutant **accepts it silently** (exit 0,
`finding_ids: []`). Every one of the seventeen is therefore still a live
undetected guard weakening at this revision.

Two calibration notes that the round-25 record did not state:

* **A13 and D06 are the same byte-level edit.** Their mutant files are
  byte-identical (both sha256 `85a052b1c48cc4dd9415ea9a177a29398cb1ec5fd0bf08e93d15e43b4c469f41`).
  The round-25 report described them as "the same edit family"; they are in fact
  the *same single edit*, applied twice under two ids. So "seventeen
  weakenings" is **sixteen distinct edits**. The round-25 report's own §5 table
  lists A13 and D06 with identical `@old`/`@new` text.
* **The seventeen span two distinct failure modes, not one.** Twelve of them
  turn a *semantic* refusal (exit 1, `CWD_MISMATCH` / `EXIT_MISMATCH` /
  `STDOUT_MISMATCH` / `REVISION_MISMATCH` / `MEMBERSHIP_MISMATCH` /
  `ARGV_MISMATCH`) into a silent pass; five turn a *shape* refusal (exit 2,
  `INVALID_REQUIREMENT` / `INVALID_RECEIPT` / `INVALID_BUNDLE`) into a silent
  pass. A shape refusal becoming a pass is the more dangerous of the two,
  because it removes the "could not evaluate" signal as well as the guard.

**No fix was made and none is implied.** The pristine bytes behave correctly on
every bundle below; each weakening requires an edit to
`tools/command-binding.py` to exist at all. This is a coverage finding about
the gate's selftest corpus, and the corpus was not changed between the round-25
revision and this one.

---

## 1. Scope and provenance

| item | value |
|---|---|
| routed item | round-25 wave-1 item 4, first part (`.ufo/waves/round-25/w1/MtGuardGaps.md` §5) |
| private clone | `/tmp/MtGuardGapsRecheck-r26` |
| clone revision | `a08e85c5d7f899e8a5992e20517edb1a380d79eb` (detached) |
| target under test | `tools/command-binding.py` (220 lines) |
| target sha256 (pristine) | `9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d` |
| suite | `.ufo/evidence/round-25/c1-suite.py` sha256 `ae33a04bd0a3646ec6a879b786024861de2af1a83b1a914369f4b720e75b15f9` |
| runner | `tools/mutate-and-run.sh` sha256 `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de` |
| round-23 fixture | `.ufo/evidence/round-23/extra-cases.json` sha256 `87bffdc829ad705c9fad6c4c0495e50e1bc5c6d2af3fec04da2294fda43c1c00` (19 cases) |
| round-24 fixture | `.ufo/evidence/round-24/extra-cases.json` sha256 `6ad7842fa01fc205bb92f0989f87fcaa88a3b79078a9c4302647a321f359cb35` (6 cases) |
| mutation spec (this item) | `/tmp/mtguardgaps-r26/r26-gaps.spec` sha256 `9d67a45d63359acfe41bcc2fdb79db8af18aed1139386369c10554c3213dda5a` |
| differential prober | `/tmp/mtguardgaps-r26/weaken_probe.py` sha256 `8109a5b6740fc997ab4f3a47cdff9effaef468954eb86872b190417680f49f65` |

### 1.1 Why the result is expected — and why that is still a measurement

The target file, the suite, and both fixture corpora are **byte-identical** to
the round-25 revision `c9ff09fb41fb8aac5fc335faf10858ff606bd5df`:

```
$ cd /tmp/MtGuardGapsRecheck-r26
$ git diff --stat c9ff09fb41fb8aac5fc335faf10858ff606bd5df \
      a08e85c5d7f899e8a5992e20517edb1a380d79eb \
      -- tools/command-binding.py .ufo/evidence/round-25/c1-suite.py \
            .ufo/evidence/round-23/extra-cases.json \
            .ufo/evidence/round-24/extra-cases.json
(no output — no drift)

$ git diff --stat c9ff09fb... a08e85c5... -- .ufo/evidence/round-23 .ufo/evidence/round-24
(no output — no drift)
```

The lane working copy of the target is byte-identical to the pinned revision
(`diff <(git show a08e85c5...:tools/command-binding.py) <lane copy>` → no
output; both sha256 `9230c68e…`). The selftest's fixture loader
(`tools/command-binding.py:166`) still reads exactly two files —
`round-23/extra-cases.json` and `round-24/extra-cases.json` — and the corpus is
still **44 cases** (17 built-in `changed(...)` cases + 19 round-23 + 6 round-24
+ 2 appended).

So the corpus that failed to kill the seventeen in round 25 is the same corpus
today. That makes "still survive" the expected outcome; the point of re-running
is to *measure* it rather than inherit it, and to confirm the mutants are still
genuine weakenings against the current bytes. Both were done.

**No new fixture file exists that the selftest could pick up.**
`.ufo/evidence/round-26/` contains `cite-check/`, `contract.json`,
`c1-measure.py`, `c2-measure.py` and `before-rev.txt` — no `extra-cases.json`,
and the loader hard-codes the round-23/round-24 paths, so nothing in round 26
can reach the corpus without a production edit.

---

## 2. Detector

Exactly the one the assignment names:

```
cd /tmp/MtGuardGapsRecheck-r26
python3 .ufo/evidence/round-25/c1-suite.py selftest <mutant copy>
```

`c1-suite.py` stages the mutant into a private temp tree as
`tools/command-binding.py` together with the round-23 and round-24
`extra-cases.json` files, then runs `--selftest`. Exit `0` = every case passed
(SURVIVED), exit `1` with a `CASE … FAIL` witness line = KILLED, exit `3` =
setup error (INCONCLUSIVE, never observed here).

**Baseline is green.** Control run on the pristine copy:
`COMMAND_BINDING_SELFTEST: 44/44 pass`, exit 0, in both sweeps. Every kill
would therefore be attributable; there are none.

---

## 3. Command and result

```
$ cd /tmp/MtGuardGapsRecheck-r26
$ rm -rf /tmp/mtguardgaps-r26/work-r26
$ bash tools/mutate-and-run.sh \
    --target tools/command-binding.py \
    --defects /tmp/mtguardgaps-r26/r26-gaps.spec \
    --suite 'python3 /tmp/MtGuardGapsRecheck-r26/.ufo/evidence/round-25/c1-suite.py selftest "$MUTANT"' \
    --workdir /tmp/mtguardgaps-r26/work-r26 \
    --label r26-guardgaps-recheck --timeout 300
```

```
MUTATE_TOOL: /tmp/MtGuardGapsRecheck-r26/tools/mutate-and-run.sh sha256=fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de
MUTATE_DATE: 2026-10-22T10:55:02Z
MUTATE_TARGET: /tmp/MtGuardGapsRecheck-r26/tools/command-binding.py sha256=9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d bytes=11799
MUTATE_SPEC: /tmp/mtguardgaps-r26/r26-gaps.spec defects=17
CONTROL: GREEN (exit=0 duration-ms=1511 pristine-sha256=9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d)
DEFECT A01: SURVIVED (exit=0 duration-ms=1491) cwd compared by prefix instead of equality
DEFECT A03: SURVIVED (exit=0 duration-ms=1454) cwd compared by basename only
DEFECT A04: SURVIVED (exit=0 duration-ms=1455) exit compared with abs() (sign-blind)
DEFECT A05: SURVIVED (exit=0 duration-ms=1449) exit compared modulo 256 (sign-blind)
DEFECT A06: SURVIVED (exit=0 duration-ms=1480) stdout token matched case-insensitively
DEFECT A07: SURVIVED (exit=0 duration-ms=1529) stdout token matched after strip
DEFECT A10: SURVIVED (exit=0 duration-ms=1476) requirement row may carry unknown keys
DEFECT A13: SURVIVED (exit=0 duration-ms=1558) stdout_contains tokens need not be nonempty strings
DEFECT A19: SURVIVED (exit=0 duration-ms=1485) receipt stderr type unchecked
DEFECT A20: SURVIVED (exit=0 duration-ms=1501) bundle schema not checked
DEFECT A22: SURVIVED (exit=0 duration-ms=1462) revision compared by 8-char prefix
DEFECT A23: SURVIVED (exit=0 duration-ms=1477) revision compared by 8-char suffix
DEFECT A26: SURVIVED (exit=0 duration-ms=1482) stdout_contains may be a bare string
DEFECT A29: SURVIVED (exit=0 duration-ms=1460) membership compared case-insensitively
DEFECT B12: SURVIVED (exit=0 duration-ms=1412) cwd compared with commonprefix
DEFECT C04: SURVIVED (exit=0 duration-ms=1442) argv compared joined by newline
DEFECT D06: SURVIVED (exit=0 duration-ms=1422) stdout_contains entries need not be strings
MUTATE_RESTORE: OK (target-sha256 before=9230c68e… after=9230c68e… pristine-sha256=9230c68e…)
MUTATE_EVIDENCE: /tmp/mtguardgaps-r26/work-r26
MUTATE: DONE (target=r26-guardgaps-recheck defects=17 killed=0 survived=17 inconclusive=0 kill-rate=0%)
```

**Determinism check** — a second, independent sweep into a fresh workdir
(`/tmp/mtguardgaps-r26/work-r26b`) produced the identical table (17 SURVIVED,
0 KILLED, 0 INCONCLUSIVE, control GREEN, `MUTATE_RESTORE: OK`).

**Per-mutant witness** — every evidence log ends `COMMAND_BINDING_SELFTEST:
44/44 pass`, and `grep -h " FAIL" *.out | wc -l` over the 17 mutant logs plus
the control returns **0**: no mutant produced a `CASE … FAIL` line, so none was
killed.

### 3.1 Restoration evidence

The target was never written. The runner copies it to a pinned pristine and
builds every mutant as a separate byte copy under the workdir; the target's
sha256 is re-checked after the sweep.

| file | sha256 |
|---|---|
| clone target, before sweep | `9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d` |
| clone target, after sweep | `9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d` |
| lane target, after all work | `9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d` |
| pinned pristine copy | `9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d` |

`MUTATE_RESTORE: OK (target-sha256 before=9230c68e… after=9230c68e… pristine-sha256=9230c68e…)`
in both sweeps. Lane `git status --porcelain` lists only other peers' files
(`M corpus/knowledge/mte-report-interop.md`, untracked `.ufo/evidence/round-26/after/`,
untracked `.ufo/waves/round-26/`) — nothing from this item.

Each mutant differs from the pristine by exactly one line (`diff` per mutant:
one hunk, one changed line). Full mutant digests are in
`/tmp/mtguardgaps-r26/work-r26/results.tsv`.

---

## 4. Are they still real weakenings? Differential probe

Survival alone only says the corpus does not see the mutant. A survivor that
had become semantically equivalent to the pristine would be a different
finding. So each mutant was run against its recorded discriminating bundle,
and the pristine against the same bundle, through the public CLI
(`--bundle … --expected … --json`):

```
$ python3 /tmp/mtguardgaps-r26/weaken_probe.py /tmp/mtguardgaps-r26/work-r26
```

```
A01 pristine=exit1 ['CWD_MISMATCH'] | mutant=exit0 [] | STILL-A-WEAKENING | receipt cwd extends bundle cwd
A03 pristine=exit1 ['CWD_MISMATCH'] | mutant=exit0 [] | STILL-A-WEAKENING | receipt cwd shares only basename
A04 pristine=exit1 ['EXIT_MISMATCH'] | mutant=exit0 [] | STILL-A-WEAKENING | expected exit 9 vs receipt exit -9
A05 pristine=exit1 ['EXIT_MISMATCH'] | mutant=exit0 [] | STILL-A-WEAKENING | expected exit 1 vs receipt exit -255
A06 pristine=exit1 ['STDOUT_MISMATCH'] | mutant=exit0 [] | STILL-A-WEAKENING | token "clean" vs stdout "CLEAN\n"
A07 pristine=exit1 ['STDOUT_MISMATCH'] | mutant=exit0 [] | STILL-A-WEAKENING | token " CLE " vs stdout "CLEAN\n"
A10 pristine=exit2 ['INVALID_REQUIREMENT'] | mutant=exit0 [] | STILL-A-WEAKENING | requirement row carries an extra key
A13 pristine=exit2 ['INVALID_REQUIREMENT'] | mutant=exit0 [] | STILL-A-WEAKENING | stdout_contains = [""]
A19 pristine=exit2 ['INVALID_RECEIPT'] | mutant=exit0 [] | STILL-A-WEAKENING | receipt stderr = 123
A20 pristine=exit2 ['INVALID_BUNDLE'] | mutant=exit0 [] | STILL-A-WEAKENING | bundle schema = command-binding-v2
A22 pristine=exit1 ['REVISION_MISMATCH'] | mutant=exit0 [] | STILL-A-WEAKENING | receipt revision differs in last hex digit
A23 pristine=exit1 ['REVISION_MISMATCH'] | mutant=exit0 [] | STILL-A-WEAKENING | receipt revision differs in first hex digit
A26 pristine=exit2 ['INVALID_REQUIREMENT'] | mutant=exit0 [] | STILL-A-WEAKENING | stdout_contains = "CLEAN" (bare string)
A29 pristine=exit1 ['MEMBERSHIP_MISMATCH'] | mutant=exit0 [] | STILL-A-WEAKENING | requirement "Clean" vs receipt "clean"
B12 pristine=exit1 ['CWD_MISMATCH'] | mutant=exit0 [] | STILL-A-WEAKENING | receipt cwd extends bundle cwd
C04 pristine=exit1 ['ARGV_MISMATCH'] | mutant=exit0 [] | STILL-A-WEAKENING | required argv ["a\nb"] vs receipt argv ["a","b"]
D06 pristine=exit2 ['INVALID_REQUIREMENT'] | mutant=exit0 [] | STILL-A-WEAKENING | stdout_contains = [""]
```

**17/17 are still genuine weakenings**: the pristine gate refuses every
bundle, the mutant accepts it silently with `finding_ids: []`.

### 4.1 The crash sub-case still holds

The A13/D06 edit (`stdout_contains` need not be a list of nonempty strings)
also admits a non-string token, and the gate then crashes instead of
verdicting. Re-measured at this revision:

```
stdout_contains=[1]    | pristine (2, ['INVALID_REQUIREMENT']) | D06-mutant (1, ["CRASH:TypeError: 'in <string>' requires string as left operand, not int"])
stdout_contains=[None] | pristine (2, ['INVALID_REQUIREMENT']) | D06-mutant (1, ["CRASH:TypeError: 'in <string>' requires string as left operand, not NoneType"])
```

A clean `exit=2` shape refusal becomes an exit-1 traceback. Same root cause as
round 25, unchanged.

### 4.2 A13 and D06 are one edit, not two

```
$ cmp work-r26/mutant-A13.command-binding.py work-r26/mutant-D06.command-binding.py
(identical)

$ sha256sum work-r26/mutant-A13.command-binding.py work-r26/mutant-D06.command-binding.py
85a052b1c48cc4dd9415ea9a177a29398cb1ec5fd0bf08e93d15e43b4c469f41  mutant-A13.command-binding.py
85a052b1c48cc4dd9415ea9a177a29398cb1ec5fd0bf08e93d15e43b4c469f41  mutant-D06.command-binding.py
```

Both spec entries carry the identical `@old`/`@new` pair:

```
@defect A13 | stdout_contains tokens need not be nonempty strings
@old or not strings(row['expect'].get('stdout_contains', []))
@new or not isinstance(row['expect'].get('stdout_contains', []), list)

@defect D06 | stdout_contains entries need not be strings
@old or not strings(row['expect'].get('stdout_contains', []))
@new or not isinstance(row['expect'].get('stdout_contains', []), list)
```

**Correction to the round-25 count: 17 ids = 16 distinct edits.** The round-25
report's §5 already notes "Same edit family as A13" for D06; they are the same
single edit, so the seventeen cover sixteen distinct byte-level weakenings.

---

## 5. Table: verdict per mutant at this revision

| id | line | edit (target → mutant) | detector verdict | still a weakening? |
|---|---|---|---|---|
| A01 | 105 | `receipt['cwd'] != bundle['cwd']` → `not receipt['cwd'].startswith(bundle['cwd'])` | SURVIVED | yes — pristine `CWD_MISMATCH`, mutant exit 0 |
| A03 | 105 | → `os.path.basename(receipt['cwd']) != os.path.basename(bundle['cwd'])` | SURVIVED | yes — pristine `CWD_MISMATCH`, mutant exit 0 |
| A04 | 109 | `receipt['exit'] != required['expect']['exit']` → `abs(...) != abs(...)` | SURVIVED | yes — pristine `EXIT_MISMATCH`, mutant exit 0 |
| A05 | 109 | → `receipt['exit'] % 256 != required['expect']['exit'] % 256` | SURVIVED | yes — pristine `EXIT_MISMATCH`, mutant exit 0 |
| A06 | 111 | `token not in receipt['stdout']` → `token.lower() not in receipt['stdout'].lower()` | SURVIVED | yes — pristine `STDOUT_MISMATCH`, mutant exit 0 |
| A07 | 111 | → `token.strip() not in receipt['stdout'].strip()` | SURVIVED | yes — pristine `STDOUT_MISMATCH`, mutant exit 0 |
| A10 | 76 | `set(row) != {'name','argv','expect'}` → `not {'name','argv','expect'} <= set(row)` | SURVIVED | yes — pristine `INVALID_REQUIREMENT`, mutant exit 0 |
| A13 | 80 | `not strings(...stdout_contains...)` → `not isinstance(..., list)` | SURVIVED | yes — pristine `INVALID_REQUIREMENT`, mutant exit 0 (**same edit as D06**) |
| A19 | 91 | `or not isinstance(row.get('stdout'), str) or not isinstance(row.get('stderr'), str)):` → drops the stderr check | SURVIVED | yes — pristine `INVALID_RECEIPT`, mutant exit 0 |
| A20 | 67 | `or bundle.get('schema') != SCHEMA` → `or False` | SURVIVED | yes — pristine `INVALID_BUNDLE`, mutant exit 0 |
| A22 | 107 | `receipt['revision'] != bundle['revision']` → `receipt['revision'][:8] != bundle['revision'][:8]` | SURVIVED | yes — pristine `REVISION_MISMATCH`, mutant exit 0 |
| A23 | 107 | → `receipt['revision'][-8:] != bundle['revision'][-8:]` | SURVIVED | yes — pristine `REVISION_MISMATCH`, mutant exit 0 |
| A26 | 80 | `not strings(...)` → `not isinstance(..., (list, str))` | SURVIVED | yes — pristine `INVALID_REQUIREMENT`, mutant exit 0 |
| A29 | 99 | `set(receipts) != set(requirements)` → `{k.lower() …} != {k.lower() …}` | SURVIVED | yes — pristine `MEMBERSHIP_MISMATCH`, mutant exit 0 |
| B12 | 105 | → `os.path.commonprefix([receipt['cwd'], bundle['cwd']]) != bundle['cwd']` | SURVIVED | yes — pristine `CWD_MISMATCH`, mutant exit 0 |
| C04 | 103 | `receipt['argv'] != required['argv']` → `chr(10).join(receipt['argv']) != chr(10).join(required['argv'])` | SURVIVED | yes — pristine `ARGV_MISMATCH`, mutant exit 0 |
| D06 | 80 | same edit as A13 | SURVIVED | yes — pristine `INVALID_REQUIREMENT`, mutant exit 0 (**duplicate of A13**) |

---

## 6. What the corpus still does not pin

Unchanged from round 25, and re-confirmed here by the seventeen survivors:

* **cwd** must be exact canonical-path equality — prefix, basename and
  `commonprefix` forms all pass (A01, A03, B12);
* **exit** must be signed integer equality — `abs()` and modulo-256 forms both
  pass (A04, A05);
* **stdout token** compare must be case- and whitespace-sensitive (A06, A07);
* **revision** must be full 40-hex equality — 8-char prefix and suffix forms
  both pass (A22, A23);
* **membership** must be case-sensitive set equality (A29);
* **argv** elements may not contain a newline (C04);
* the **bundle `schema`** field must be compared (A20);
* a **requirement row** may not carry unknown keys (A10);
* `stdout_contains` must be a list of nonempty strings (A13, A26, D06 — one
  edit, two ids);
* the **receipt `stderr`** field must be a string (A19).

The corpus that would close these is a fixture list, not a production change:
the round-25 report's §8 already enumerates the seventeen one-bundle
perturbations needed (receipt cwd `/fixture/repo-evil` and `/other/repo`; exit
`9`/`-9` and `1`/`-255`; token `"clean"` vs `"CLEAN\n"`; token `" CLE "` vs
`"CLEAN\n"`; a requirement row with an extra key; `stdout_contains = [""]`;
receipt `stderr = 123`; `schema = "command-binding-v2"`; receipt revision
differing in the first and in the last hex digit; `stdout_contains = "CLEAN"`;
requirement `"Clean"` vs receipt `"clean"`; required argv `["a\nb"]` vs receipt
`["a","b"]`). **This item makes no such change** — no fix was in scope and
none was made.

---

## 7. Bounds observed

* Private clone `/tmp/MtGuardGapsRecheck-r26`; every command ran inside it or
  inside `/tmp/mtguardgaps-r26/`. No gate, selftest or sweep ran in the lane
  repo.
* No production file was edited. The lane target is byte-identical to the
  pinned revision.
* No git write command was issued in the lane repo (no add/commit/checkout/
  reset/stash/push/fetch/pull). Read-only `git status` / `git diff` were run
  with `GIT_OPTIONAL_LOCKS=0`.
* **No `jj` command was run anywhere.**
* No sibling lane was touched; `kumitate-shokunin` was not read.
* No subagent was dispatched.

---

## 8. Tooling

No tools were installed or upgraded for this item — everything used was already
present: `git` 2.56.0, `bash` 5.3.20, `python3` 3.14.8, plus the lane's own
`tools/mutate-and-run.sh` and `.ufo/evidence/round-25/c1-suite.py`. The pacman
guard (all pacman transactions paused host-wide) was respected: no package
transaction was attempted, and no host service was restarted. No network access
was needed.

---

## 9. Reproduction

```
rm -rf /tmp/MtGuardGapsRecheck-r26 /tmp/mtguardgaps-r26
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    /tmp/MtGuardGapsRecheck-r26
git -C /tmp/MtGuardGapsRecheck-r26 checkout -q --detach \
    a08e85c5d7f899e8a5992e20517edb1a380d79eb
cd /tmp/MtGuardGapsRecheck-r26
bash tools/mutate-and-run.sh --target tools/command-binding.py \
    --defects /tmp/mtguardgaps-r26/r26-gaps.spec \
    --suite 'python3 /tmp/MtGuardGapsRecheck-r26/.ufo/evidence/round-25/c1-suite.py selftest "$MUTANT"' \
    --workdir /tmp/mtguardgaps-r26/work-r26 --label r26-guardgaps-recheck --timeout 300
python3 /tmp/mtguardgaps-r26/weaken_probe.py /tmp/mtguardgaps-r26/work-r26
```

Report: .ufo/waves/round-26/w1/MtGuardGapsRecheck.md
