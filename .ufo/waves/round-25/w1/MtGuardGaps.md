# MtGuardGaps — round 25, wave 1

**Verdict:** the gate's own selftest (44 cases, `tools/command-binding.py --selftest`
staged with the round-23 and round-24 fixture files) kills the eight recorded
guard mutants of `.ufo/evidence/round-25/guard-mutants.spec` **8/8**, but it
does **not** pin the guard *semantics* around them. Of 64 additional
single-edit weakenings of `tools/command-binding.py evaluate()` (lines 65–113)
that I ran through the same bounded detector, **41 SURVIVED** and 23 were
KILLED. Seventeen of the 41 survivors are genuine guard weakenings — there is a
bundle the pristine gate rejects (exit 1 or 2, a finding ID) that the mutated
gate accepts silently (exit 0, `finding_ids: []`). Twelve more survivors
downgrade a *shape* refusal (`INVALID_RECEIPT` / `INVALID_REQUIREMENT`) into a
*semantic* mismatch, three survivors make the gate stricter, and nine survivors
are semantically equivalent to the pristine code (no bundle distinguishes them;
they are recorded so the kill-rate is not read as coverage).

This is a coverage finding about the gate's selftest, not a defect in the
production check and not permission to change the contract.

---

## 1. Setup and restoration evidence

| item | value |
|---|---|
| private clone | `/tmp/MtGuardGaps-r25` |
| clone revision | `c9ff09fb41fb8aac5fc335faf10858ff606bd5df` (detached) |
| lane repo | read-only; never entered for writes |
| target under test | `tools/command-binding.py` (220 lines) |
| target sha256 (pristine, before every sweep) | `9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d` |
| target sha256 (after all six sweeps, clone) | `9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d` |
| target sha256 (after all six sweeps, lane) | `9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d` (byte-identical to the clone) |
| suite bytes | `.ufo/evidence/round-25/c1-suite.py` sha256 `ae33a04bd0a3646ec6a879b786024861de2af1a83b1a914369f4b720e75b15f9` (clone copy == lane copy) |
| runner bytes | `tools/mutate-and-run.sh` sha256 `d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b` (clone copy == lane copy) |
| fixture bytes | `.ufo/evidence/round-23/extra-cases.json` and `.ufo/evidence/round-24/extra-cases.json` copied by the suite itself, unchanged |

**The target file was never written.** Every mutant is a separate byte copy
under `/tmp/mtguardgaps/work*/`; `tools/mutate-and-run.sh` never writes the
target (it pins a pristine copy and asserts `count==1` for every `@old`
string before any run). All six sweeps ended with
`MUTATE_RESTORE: OK (target-sha256 before=9230c68e… after=9230c68e… pristine-sha256=9230c68e…)`.
The lane working tree shows no change from this item
(`git status --porcelain` in the lane lists only other peers' files:
`M corpus/SOURCES.md` and the untracked `.ufo/waves/round-25/*`).

## 2. Detector and its semantics

The bounded behavioural detector is exactly the one the assignment names:

```
cd /tmp/MtGuardGaps-r25
python3 .ufo/evidence/round-25/c1-suite.py selftest <mutant copy>
```

Suite semantics (`c1-suite.py:76-93`): the mutant is staged into a private tree
as `tools/command-binding.py` together with the round-23 and round-24
`extra-cases.json` files, then run as `--selftest`. Exit `0` = every case
passed, exit `1` = an explicit `CASE <name> FAIL` witness line, exit `3` =
setup error. So:

* suite exit 0 → the mutant **SURVIVED**;
* suite exit 1 with a `CASE … FAIL` line → **KILLED**;
* suite exit 3 → INCONCLUSIVE (never observed in the six sweeps below).

**Baseline (pristine bytes):** `COMMAND_BINDING_SELFTEST: 44/44 pass`, exit 0,
in every one of the six sweeps. The detector is green before any mutation, so
every kill below is attributable and no survivor is a red-baseline artefact.

## 3. Baseline: the eight recorded guard mutants still kill

Sweep of the recorded spec, unmodified, same detector:

```
bash tools/mutate-and-run.sh --target tools/command-binding.py \
  --defects .ufo/evidence/round-25/guard-mutants.spec \
  --suite 'python3 /tmp/MtGuardGaps-r25/.ufo/evidence/round-25/c1-suite.py selftest "$MUTANT"' \
  --workdir /tmp/mtguardgaps/work-g --label r25-guardbaseline
```

```
CONTROL: GREEN (exit=0 duration-ms=1405 pristine-sha256=9230c68e…)
DEFECT G1: KILLED (exit=1) argv guard disabled
DEFECT G2: KILLED (exit=1) cwd guard disabled
DEFECT G3: KILLED (exit=1) revision guard disabled
DEFECT G4: KILLED (exit=1) exit guard disabled
DEFECT G5: KILLED (exit=1) stdout finding dropped
DEFECT G6: KILLED (exit=1) membership finding dropped
DEFECT G7: KILLED (exit=1) duplicate-command refusal dropped
DEFECT G8: KILLED (exit=1) duplicate-requirement refusal dropped
MUTATE_RESTORE: OK (target-sha256 before=9230c68e… after=9230c68e… pristine-sha256=9230c68e…)
MUTATE: DONE (target=r25-guardbaseline defects=8 killed=8 survived=0 inconclusive=0 kill-rate=100%)
```

Each kill log holds explicit `CASE … FAIL` witness lines (e.g. `G1.out`:
`CASE source-read-not-command FAIL`, `CASE argv-order FAIL`, `CASE argv-missing FAIL`, …).
So R23-ROUTED-2's recorded re-run is reproducible: 8/8 killed with witnesses,
control green, restore OK. **The gaps reported below are gaps in the selftest's
*corpus*, not in the eight recorded mutants** — the eight are genuinely killed.

## 4. Mutants tried

64 new single-edit mutants of `tools/command-binding.py evaluate()`
(lines 65–113), in five spec files, none repeating the eight of
`guard-mutants.spec`. Every mutant replaces exactly one byte-exact string;
the runner asserts `count==1` for each `@old` before any suite run.

| sweep | spec file | defects | KILLED | SURVIVED | INCONCLUSIVE | kill-rate |
|---|---|---|---|---|---|---|
| wave 1 | `/tmp/mtguardgaps/gap-mutants.spec` | 23 | 4 | 19 | 0 | 17 % |
| wave 2 | `/tmp/mtguardgaps/gap-mutants2.spec` | 12 | 6 | 6 | 0 | 50 % |
| wave 3 | `/tmp/mtguardgaps/gap-mutants3.spec` | 13 | 6 | 7 | 0 | 46 % |
| wave 4 | `/tmp/mtguardgaps/gap-mutants4.spec` | 6 | 3 | 3 | 0 | 50 % |
| wave 5 | `/tmp/mtguardgaps/gap-mutants5.spec` | 10 | 4 | 6 | 0 | 40 % |
| **total** | | **64** | **23** | **41** | **0** | **36 %** |

Two wave-4 entries (C02, C04) were first written with malformed replacements
that produced a Python `SyntaxError`; the runner's first pass reported them
KILLED with exit 3. That was a false kill — a crash is not a behavioural
detection. Both were re-specified with syntax-valid replacements and re-run
from scratch (`work4` was deleted and rebuilt); the numbers above are the
corrected sweep. C04 survives with a valid replacement and is reported as a
genuine gap below.

### 4.1 The 23 KILLED mutants (detector works)

| id | edit | killed by |
|---|---|---|
| A09 | stdout token may be supplied by stderr | `stderr-cannot-supply-token` |
| A11 | bundle may carry unknown keys | `unknown-bundle-key` |
| A12 | expect may hold unknown keys | `unknown-expect-key` |
| A14 | requirement argv may be empty | `blank-argv` |
| A24 | argv compared by first element only | `source-read-not-command` + 8 argv fixtures |
| A25 | argv compared as joined string | `argv-joined-collision` |
| A27 | expected exit type via `isinstance` (bool admitted) | `bool-expected-exit` |
| A28 | receipt exit type via `isinstance` (bool admitted) | `bool-exit` |
| A30 | `canonical_cwd` relaxed to absolute-path only | `noncanonical-cwd` |
| A33 | stdout token matched ignoring case on token side only | 26 corpus cases |
| B01 | membership checked as subset (`receipts ⊆ requirements`) | `missing` |
| B02 | membership checked as superset (`requirements ⊆ receipts`) | `unknown-added` |
| B03 | membership checked by cardinality only | `unknown` |
| B04 | argv compared by length only | 6 argv fixtures |
| B05 | bundle revision shape unchecked | `short-revision` |
| B06 | bundle requirements list may be empty | `empty-requirements` |
| C10 | exit guard compares only truthiness of difference | `wrong-exit` |
| C11 | cwd guard compares only truthiness of difference | `wrong-cwd` |
| C12 | membership guard compares only truthiness of difference | `missing` |
| D02 | receipt row may carry unknown keys | `unknown-receipt-key` |
| D07 | argv entries need not be strings | `argv-shell-string` |
| D09 | bundle revision type unchecked (non-str admitted) | `short-revision` |
| D10 | bundle cwd type unchecked (non-str admitted) | `noncanonical-cwd` |

### 4.2 The 41 SURVIVED mutants, classified

Classification is by a differential probe: for each mutant I compared
`mutant.evaluate()` against `pristine.evaluate()` on the full 44-case corpus
(17 built-in selftest cases + 19 round-23 fixtures + 6 round-24 fixtures +
the base bundle) **and** on 41 hand-built discriminating bundles. Four classes:

* **WEAKENING** (17) — pristine rejects a bundle, the mutant accepts it
  (exit 0, `finding_ids: []`). A real, undetected guard weakening.
* **SHIFT** (12) — both reject, but the mutant turns a *shape* refusal
  (`INVALID_RECEIPT` / `INVALID_REQUIREMENT`, exit 2) into a *semantic*
  mismatch (exit 1), or changes which finding ID is reported. The gate still
  refuses the bundle, so the acceptance contract holds, but the reason changes.
* **STRICTER** (3) — the mutant rejects a bundle the pristine accepts
  (`A08` stdout token matched on word boundaries only; `C09` stdout token
  matched on whitespace-split words; `B10` stdout tokens joined into one
  string before the search). The selftest cannot see the tightening.
* **EQUIVALENT** (9) — no bundle I could construct distinguishes the mutant
  from the pristine code: `A02` (cwd compared after `normpath` — but
  `canonical_cwd` already guarantees `normpath(value) == value`, so the two
  comparisons coincide), `A21` (full-length revision prefix compare is
  equality because `REVISION` is a 40-hex fullmatch), `A34`
  (`os.path.realpath` — `canonical_cwd` already forbids `..`), `A35`
  (revision case-folded — the regex is lowercase-only), `B07`/`B08`
  (`setdefault` instead of assignment — unreachable because the duplicate
  check returns first), `B11` (exit compared as string — both sides are
  `int`), `B13` (`commonprefix` on two equal-length hex strings), `C02`
  (receipts tuple admitted — `decode()` only ever produces `list`). These
  nine are recorded so the survivor count is not mis-read as coverage.

## 5. The seventeen undetected guard weakenings (WEAKENING)

Each row: the single edit, and the bundle the pristine gate rejects but the
mutant accepts. Both columns are the real CLI output
(`command-binding.py --bundle … --expected … --json`).

**A01 — cwd compared by prefix instead of equality**
`tools/command-binding.py:105`
```python
if receipt['cwd'] != bundle['cwd']:          →   if not receipt['cwd'].startswith(bundle['cwd']):
```
Bundle: `cwd = /fixture/repo`, receipt `cwd = /fixture/repo-evil`.
```
pristine exit=1 finding_ids=["CWD_MISMATCH"]
mutant  exit=0 finding_ids=[]
```

**A03 — cwd compared by basename only** — `tools/command-binding.py:105`
```python
if receipt['cwd'] != bundle['cwd']:          →   if os.path.basename(receipt['cwd']) != os.path.basename(bundle['cwd']):
```
Bundle: `cwd = /fixture/repo`, receipt `cwd = /other/repo`.
```
pristine exit=1 finding_ids=["CWD_MISMATCH"]
mutant  exit=0 finding_ids=[]
```

**A04 — exit compared with `abs()`** — `tools/command-binding.py:109`
```python
if receipt['exit'] != required['expect']['exit']:   →   if abs(receipt['exit']) != abs(required['expect']['exit']):
```
Bundle: expected `exit = 9`, receipt `exit = -9`.
```
pristine exit=1 finding_ids=["EXIT_MISMATCH"]
mutant  exit=0 finding_ids=[]
```

**A05 — exit compared modulo 256** — `tools/command-binding.py:109`
```python
if receipt['exit'] != required['expect']['exit']:   →   if receipt['exit'] % 256 != required['expect']['exit'] % 256:
```
Bundle: expected `exit = 1`, receipt `exit = -255`.
```
pristine exit=1 finding_ids=["EXIT_MISMATCH"]
mutant  exit=0 finding_ids=[]
```

**A06 — stdout token matched case-insensitively** — `tools/command-binding.py:111`
```python
if any(token not in receipt['stdout'] for token in required['expect'].get('stdout_contains', [])):   →   … token.lower() not in receipt['stdout'].lower() …
```
Bundle: `stdout_contains = ["clean"]`, receipt `stdout = "CLEAN\n"`.
```
pristine exit=1 finding_ids=["STDOUT_MISMATCH"]
mutant  exit=0 finding_ids=[]
```

**A07 — stdout token matched after `strip()`** — `tools/command-binding.py:111`
```python
… token not in receipt['stdout'] …   →   … token.strip() not in receipt['stdout'].strip() …
```
Bundle: `stdout_contains = [" CLE "]`, receipt `stdout = "CLEAN\n"`.
```
pristine exit=1 finding_ids=["STDOUT_MISMATCH"]
mutant  exit=0 finding_ids=[]
```

**A10 — requirement row may carry unknown keys** — `tools/command-binding.py:76`
```python
or set(row) != {'name', 'argv', 'expect'}   →   or not {'name', 'argv', 'expect'} <= set(row)
```
Bundle: requirement carries an extra `extra: 1` key.
```
pristine exit=2 finding_ids=["INVALID_REQUIREMENT"]
mutant  exit=0 finding_ids=[]
```

**A13 — `stdout_contains` tokens need not be nonempty strings** — `tools/command-binding.py:80`
```python
or not strings(row['expect'].get('stdout_contains', []))   →   or not isinstance(row['expect'].get('stdout_contains', []), list)
```
Bundle: `stdout_contains = [""]`.
```
pristine exit=2 finding_ids=["INVALID_REQUIREMENT"]
mutant  exit=0 finding_ids=[]
```
(The same edit with a non-string entry `stdout_contains = [1]` makes the gate
crash with `TypeError: 'in <string>' requires string as left operand, not int`
— exit 1 with a traceback instead of a verdict. Same root cause, different symptom.)

**A19 — receipt `stderr` type unchecked** — `tools/command-binding.py:91`
```python
or not isinstance(row.get('stdout'), str) or not isinstance(row.get('stderr'), str)):   →   or not isinstance(row.get('stdout'), str)):
```
Bundle: receipt `stderr = 123`.
```
pristine exit=2 finding_ids=["INVALID_RECEIPT"]
mutant  exit=0 finding_ids=[]
```

**A20 — bundle `schema` not checked** — `tools/command-binding.py:67`
```python
or bundle.get('schema') != SCHEMA   →   or False
```
Bundle: `schema = "command-binding-v2"`.
```
pristine exit=2 finding_ids=["INVALID_BUNDLE"]
mutant  exit=0 finding_ids=[]
```

**A22 — revision compared by 8-char prefix** — `tools/command-binding.py:107`
```python
if receipt['revision'] != bundle['revision']:   →   if receipt['revision'][:8] != bundle['revision'][:8]:
```
Bundle: bundle revision `1111…`, receipt revision `1111…2` (last hex digit differs).
```
pristine exit=1 finding_ids=["REVISION_MISMATCH"]
mutant  exit=0 finding_ids=[]
```

**A23 — revision compared by 8-char suffix** — `tools/command-binding.py:107`
```python
if receipt['revision'] != bundle['revision']:   →   if receipt['revision'][-8:] != bundle['revision'][-8:]:
```
Bundle: bundle revision `1111…`, receipt revision `2111…` (first hex digit differs).
```
pristine exit=1 finding_ids=["REVISION_MISMATCH"]
mutant  exit=0 finding_ids=[]
```

**A26 — `stdout_contains` may be a bare string** — `tools/command-binding.py:80`
```python
or not strings(row['expect'].get('stdout_contains', []))   →   or not isinstance(row['expect'].get('stdout_contains', []), (list, str))
```
Bundle: `stdout_contains = "CLEAN"`.
```
pristine exit=2 finding_ids=["INVALID_REQUIREMENT"]
mutant  exit=0 finding_ids=[]
```

**A29 — membership compared case-insensitively** — `tools/command-binding.py:99`
```python
if set(receipts) != set(requirements):   →   if {k.lower() for k in receipts} != {k.lower() for k in requirements}:
```
Bundle: requirement `name = "Clean"`, receipt `name = "clean"`.
```
pristine exit=1 finding_ids=["MEMBERSHIP_MISMATCH"]
mutant  exit=0 finding_ids=[]
```

**B12 — cwd compared with `os.path.commonprefix`** — `tools/command-binding.py:105`
```python
if receipt['cwd'] != bundle['cwd']:   →   if os.path.commonprefix([receipt['cwd'], bundle['cwd']]) != bundle['cwd']:
```
Bundle: `cwd = /fixture/repo`, receipt `cwd = /fixture/repo-evil`.
```
pristine exit=1 finding_ids=["CWD_MISMATCH"]
mutant  exit=0 finding_ids=[]
```

**C04 — argv compared joined by newline** — `tools/command-binding.py:103`
```python
if receipt['argv'] != required['argv']:   →   if chr(10).join(receipt['argv']) != chr(10).join(required['argv']):
```
Bundle: required `argv = ["a\nb"]`, receipt `argv = ["a", "b"]`.
```
pristine exit=1 finding_ids=["ARGV_MISMATCH"]
mutant  exit=0 finding_ids=[]
```

**D06 — `stdout_contains` entries need not be strings** — `tools/command-binding.py:80`
```python
or not strings(row['expect'].get('stdout_contains', []))   →   or not isinstance(row['expect'].get('stdout_contains', []), list)
```
Same edit family as A13; it also admits `stdout_contains = [1]` and the gate
then crashes with `TypeError: 'in <string>' requires string as left operand, not int`.

## 6. The twelve undetected SHIFT survivors

These still reject the bundle (exit 1), so the acceptance contract is intact,
but the *reason* the gate gives changes from a shape refusal to a semantic
mismatch, or a different finding ID is reported.

| id | edit (line) | pristine | mutant |
|---|---|---|---|
| A15 | receipt argv may be empty (`:89`) | `(2, ['INVALID_RECEIPT'])` | `(1, ['ARGV_MISMATCH'])` |
| A16 | receipt cwd need not be canonical (`:89`) | `(2, ['INVALID_RECEIPT'])` | `(1, ['CWD_MISMATCH'])` |
| A17 | receipt revision shape unchecked (`:90`) | `(2, ['INVALID_RECEIPT'])` | `(1, ['REVISION_MISMATCH'])` |
| A18 | requirement name may be empty (`:75`) | `(2, ['INVALID_REQUIREMENT'])` | `(1, ['MEMBERSHIP_MISMATCH'])` |
| A31 | duplicate-command refusal narrowed to exact-row duplicates (`:95`) | `(1, ['DUPLICATE_COMMAND'])` | `(1, ['ARGV_MISMATCH'])` |
| A32 | duplicate-requirement refusal narrowed to exact-row duplicates (`:82`) | `(2, ['DUPLICATE_REQUIREMENT'])` | `(1, ['ARGV_MISMATCH'])` |
| B09 | receipt cwd unchecked entirely (`:89`) | `(2, ['INVALID_RECEIPT'])` | `(1, ['CWD_MISMATCH'])` |
| D01 | receipt name may be empty (`:87`) | `(2, ['INVALID_RECEIPT'])` | `(1, ['MEMBERSHIP_MISMATCH'])` |
| D03 | receipt stdout type unchecked (`:91`) | `(2, ['INVALID_RECEIPT'])` | crash: `TypeError: argument of type 'int' is not a container or iterable` |
| D04 | requirement name type unchecked, non-str admitted (`:75`) | `(2, ['INVALID_REQUIREMENT'])` | `(1, ['MEMBERSHIP_MISMATCH'])` |
| D05 | receipt name type unchecked, non-str admitted (`:87`) | `(2, ['INVALID_RECEIPT'])` | `(1, ['MEMBERSHIP_MISMATCH'])` |
| D08 | receipt argv entries need not be strings (`:89`) | `(2, ['INVALID_RECEIPT'])` | `(1, ['ARGV_MISMATCH'])` |

Two of these are worth singling out because the gate stops refusing rather
than merely re-labelling: **D03** (receipt `stdout` not a string) and **D06**
(`stdout_contains` entry not a string) both turn a clean `exit=2` refusal into
an uncaught `TypeError` and an exit-1 traceback — a crash, not a verdict.

## 7. What the selftest corpus does and does not pin

The gate's 44-case corpus (17 built-in `changed(...)` cases + 19 round-23
fixtures + 6 round-24 fixtures) pins:

* argv compared element-wise and in order, byte-exact, with no case folding,
  no whitespace normalisation, no path normalisation, no length-only compare,
  and no joined-string compare — `argv-order`, `argv-missing`, `argv-extra`,
  `argv-joined-collision`, `argv-normalized`, `argv-second-only`,
  `argv-swapped-between-names`, `argv-case-only`, `argv-padded-token`,
  `argv-repeated-flag`, `argv-shell-string` all kill;
* membership as **set equality** — `missing`, `unknown`, `unknown-added` kill
  subset, superset, and cardinality-only forms;
* the exit compare as **signed integer equality** — `wrong-exit`,
  `negative-exit-mismatch`, `negative-exit-declared-match` kill `abs()` and
  modulo forms;
* the revision compare as **full 40-hex equality** — `stale-revision`,
  `all-stale` kill prefix and suffix forms;
* the cwd compare as **exact canonical-path equality** — `wrong-cwd`,
  `second-cwd`, `noncanonical-cwd` kill prefix, basename, `realpath`,
  `commonprefix`, and `normpath` forms;
* the stdout check as **byte-exact substring of stdout only** —
  `stderr-cannot-supply-token`, `stdout-surround-clean`, `all-of-tokens` kill
  the stderr-supply form.

It does **not** pin:

* that the stdout token compare is case-sensitive and whitespace-sensitive
  (A06, A07 survive);
* that the stdout token compare is a *substring* compare rather than a word
  compare (A08 and C09 survive — the corpus cannot see either direction);
* that an argv element may not contain a newline (C04 survives);
* that the bundle `schema` field is compared (A20 survives);
* that a requirement row may not carry unknown keys (A10 survives — the
  corpus covers the *receipt* row and the *bundle*, not the requirement row);
* that `stdout_contains` entries are nonempty strings (A13, A26, D06 survive);
* that the requirement and receipt `stderr`/`stdout` fields are strings
  (A19, D03 survive);
* that membership is compared case-sensitively (A29 survives);
* that a receipt `cwd` is canonical (A16, B09 survive);
* that a receipt `name` is a nonempty string (D01, D04, D05 survive);
* that a duplicate receipt/requirement with the *same name but different
  content* is refused rather than reported as a mismatch (A31, A32 survive —
  the corpus's `duplicate` fixture appends a byte-identical row).

## 8. Smallest safe correction

The finding is about the *fixture corpus*, so the correction belongs there,
not in `tools/command-binding.py`: **add fixture cases** to
`.ufo/evidence/round-23/extra-cases.json` (or a round-26 equivalent) that
distinguish each surviving class, and re-run the guard sweep. Concretely, the
corpus needs, at minimum, one case each for:

1. receipt cwd that *extends* the bundle cwd (`/fixture/repo-evil`) and one
   that shares only its basename (`/other/repo`) — kills A01, A03, B12;
2. expected exit `9` with receipt exit `-9` — kills A04;
3. expected exit `1` with receipt exit `-255` — kills A05;
4. `stdout_contains = ["clean"]` against `stdout = "CLEAN\n"` — kills A06;
5. `stdout_contains = [" CLE "]` against `stdout = "CLEAN\n"` — kills A07;
6. a requirement row with an extra key — kills A10;
7. `stdout_contains = [""]` — kills A13, D06;
8. receipt `stderr = 123` — kills A19;
9. `schema = "command-binding-v2"` — kills A20;
10. receipt revision differing in its last hex digit — kills A22;
11. receipt revision differing in its first hex digit — kills A23;
12. `stdout_contains = "CLEAN"` — kills A26;
13. requirement `name = "Clean"` against receipt `name = "clean"` — kills A29;
14. required `argv = ["a\nb"]` against receipt `argv = ["a", "b"]` — kills C04;
15. a duplicate receipt with the same name but different `argv` — kills A31;
16. a duplicate requirement with the same name but different `argv` — kills A32;
17. a receipt whose `name` is `""` and whose `stdout` is not a string — kills
    D01/D03/D05.

Cases 1–5 and 10–14 are also the natural companions to the round-25
multi-token stdout fixtures: they are single-field perturbations of a bundle
that is otherwise clean, so each is one bundle, two lines of JSON.

**No production change is implied.** Every one of the seventeen weakenings
requires an edit to `tools/command-binding.py` to occur at all; the pristine
bytes behave correctly on every bundle above. The correct reading is: the
gate's selftest is calibrated for *whether* each guard fires (the eight
recorded mutants, 8/8 killed), not for *how* it fires.

## 9. Reproduction

```
rm -rf /tmp/MtGuardGaps-r25
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/MtGuardGaps-r25
git -C /tmp/MtGuardGaps-r25 checkout -q --detach c9ff09fb41fb8aac5fc335faf10858ff606bd5df
cd /tmp/MtGuardGaps-r25
for spec in /tmp/mtguardgaps/gap-mutants{,2,3,4,5}.spec; do
  bash tools/mutate-and-run.sh --target tools/command-binding.py --defects "$spec" \
    --suite 'python3 /tmp/MtGuardGaps-r25/.ufo/evidence/round-25/c1-suite.py selftest "$MUTANT"' \
    --workdir "/tmp/mtguardgaps/work-$(basename "$spec" .spec)" --timeout 300
done
```

The five spec files, the differential probe, the direction classifier and the
end-to-end CLI verifier live under `/tmp/mtguardgaps/` (`gap-mutants*.spec`,
`probe.py`, `direction.py`, `classify.py`, `cli_verify.py`); per-defect
evidence logs and `results.tsv` are under `/tmp/mtguardgaps/work*/evidence/`
and `/tmp/mtguardgaps/work*/results.tsv`.

## 10. Tooling

No tools were installed or upgraded for this item. Everything used was already
present: `git`, `bash`, `python3` (3.13), `coreutils`, and the lane's own
`tools/mutate-and-run.sh` plus `.ufo/evidence/round-25/c1-suite.py`. No
network access was needed and no host service was restarted.

Report: .ufo/waves/round-25/w1/MtGuardGaps.md
