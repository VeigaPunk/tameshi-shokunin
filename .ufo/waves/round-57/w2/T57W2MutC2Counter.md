# T57W2MutC2Counter — round 57 wave 2, seat report

**Scope.** Mutation-test the round-57 C2 counter (operability) at
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/c2/measure.py`
(sha256 `7d49e3c493b3096f3375bc19ba960049faf6ef76590c4ed2674dbb69a5d2b9cd`) with 12 single-edit
mutants, and repair the selftest's coverage gaps the mutants expose.

**Verdict.** 6 of 12 mutants KILLED, 6 SURVIVED. All 6 survivors are coverage gaps in the
counter's own `--selftest`, not in the counter's measurement logic. A staged amended counter
carrying 6 proposed selftest cases passes **20/20** and kills **all 6 survivors** (each then
fails exactly its own proposed case, 19/20, exit 1).

Machine-readable: `.ufo/waves/round-57/w2/T57W2MutC2Counter.json`.
Receipts: `.ufo/waves/round-57/w2/T57W2MutC2Counter-receipts/`.
Staged instrument: `.ufo/waves/round-57/w2/T57W2MutC2Counter/stage/.ufo/evidence/round-57/c2/measure.py`
(sha256 `a5138acb2248dbf2d05a575ffd66f1eb685b518843649e5129bb03b8040c5a79`).

---

## 1. Method

**Detector.** The counter's own selftest, run against the lane at C0:

```
python3 <mutant-dir>/measure.py --selftest \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev   ca75c2674645ab6bdadeecb8584007c74342bfa9
```

**KILL rule.** A mutant is KILLED when the counter's selftest reports a FAIL (exit != 0, fewer
than 14/14 pass); SURVIVED when the selftest still passes 14/14.

**Isolation.** Each mutant is a fresh copy of `measure.py` plus a byte-identical `mutants.json`
in its own scratch directory under `/fast/scratch/hyaku/tameshi-r57/T57W2MutC2Counter/mut/<id>/`.
The counter's `__file__`-relative `mutants.json` lookup and its sha256 pin are therefore
satisfied by construction, so the mutants differ from the baseline in exactly the one edited
string. **The lane's `measure.py` and `mutants.json` were never edited** — sha256 verified
identical before and after (`7d49e3c4…` / `d51f558c…`, receipts `lane-integrity.txt`).

**Uniqueness.** Each mutant's `old` string was asserted to occur **exactly once** in the pristine
counter; the build aborts otherwise (`build_mutants.py`, `FATAL …: old string occurs N times`).

**Parallelism.** 4 concurrent selftests; `TMPDIR` under the scratch root. Baseline 127 s wall,
mutants ~200 s each.

**Second, independent probe (real verdict at C0).** Each mutant was also run in *measurement*
mode against a scratch clone at C0 + the round-57 evidence dir (the shape `dry-c2.sh` uses), to
see whether a mutant changes the counter's real verdict, not just the selftest:

```
C2_R57: self=7d49e3c493b3 rev=7db275a89059 gate_rows=3 exits=0,2,3 held=3/3 mutants=3/3 \
         skill_row=1 codes_known=4/4 standing_cell=ok total=0 C2_R57_PASS=true   # BASELINE
```

Only **M4** changes that verdict (total 0 → 3, PASS → FAIL). The other 11 mutants are latent
at C0: they would matter only if the lane's registry/SKILL drifted into the shape the mutant
blind to. That is the point of the exercise — the counter must be able to *see* those shapes, and
for 6 of the 12 shapes it cannot.

---

## 2. Baseline

```
C2_R57_SELFTEST: 14/14 pass        exit=0
```

Receipts: `baseline-selftest.stdout`, `baseline-selftest.exit`.

---

## 3. Results

| id | arm | mutant | selftest | verdict | real verdict at C0 changed? |
|----|-----|--------|----------|---------|------------------------------|
| M1 | rows | rows arm admits `--selftest` rows | 13/14 | **KILLED** | no |
| M2 | rows | exit set check dropped | 13/14 | **KILLED** | no |
| M3 | rows | refusal-needle check dropped | 14/14 | SURVIVED | no |
| M4 | executed | executed arm skips rows | 12/14 | **KILLED** | **yes (total 0→3)** |
| M5 | mutants | mutant arm kills credit from non-admitted rows | 14/14 | SURVIVED | no |
| M6 | mutants | mutant pin check removed | 14/14 | SURVIVED | no |
| M7 | skill | skill_row arm accepts any `0` token | 13/14 | **KILLED** | no |
| M8 | codes | codes arm vacuous-pass when zero tokens | 14/14 | SURVIVED | no |
| M9 | cell | cell arm compares with `in` instead of equality | 14/14 | SURVIVED | no |
| M10 | cell | cell arm reads the committed table instead of running the gate | 10/14 | **KILLED** | no |
| M11 | fixture | base fixture builder drops the drifting path | 12/14 | **KILLED** | no |
| M12 | verdict | verdict line prints PASS on total>0 | 14/14 | SURVIVED | no |

Per-mutant diffs: `receipts/mutant-<id>.diff`. Per-mutant stdout/exit:
`receipts/mutant-<id>-selftest.stdout|.exit`. Real-verdict probe:
`receipts/realverdict-<id>.stdout`.

### What killed each mutant

- **M1** — `rows arm (forgery): selftest-argv rows are not gate rows FAIL gate_rows=3`
- **M2** — `rows arm: no exit-2 row -> rows shortfall FAIL short={'rows': 1, …}`
- **M4** — `good fixture: every arm 0 FAIL … held=0/3 … total=3` and
  `executed arm: a row expecting the wrong exit does not hold FAIL held=0/3`
- **M7** — `skill_row arm: verdict map without the 2 -> 0 FAIL`
- **M10** — all four cell-arm cases FAIL (the arm stops running the gate, so the cell is graded
  against itself)
- **M11** — `good fixture: every arm 0 FAIL … held=2/3 … total=3` and
  `mutants arm: a mutant whose old string is absent is not killed (uniqueness assert) FAIL mutants=1/3`

### Why each survivor survived (the coverage gap)

- **M3 (refusal-needle check dropped).** `unnamed` — the list of exit-2/3 rows whose
  `stdout_contains` names a code the gate does not define — is always empty in every fixture.
  The `bogus` fixture puts the unknown token in **SKILL.md standing rules** (the *codes* arm),
  never in a **registry row's needle** (the *rows* arm). The two arms are untested against each
  other.
- **M5 (mutant arm kills credit from non-admitted rows).** The kill-credit loop's
  `if r['name'] not in baseline: continue` is only observable when some admitted row *fails* at
  baseline. The fixtures that exercise the mutants arm (`nodrift`, `onlyok`) keep every row
  holding; the fixture that has a non-holding row (`unheld`) is never asserted on the mutants
  arm. Measured effect (fixture `unheld`): baseline `mutants=1/3`, M5 `mutants=3/3` — a row
  that never held supplies kill credit, so an unrelated row's drift silently "kills" a mutant
  and the arm reports a stronger guarantee than it measured.
- **M6 (mutant pin check removed).** The sha256 pin lives in `main_measure`, which `--selftest`
  never calls. The selftest reads `mutants.json` from its own directory and never exercises the
  lane-at-REV pin path, so no fixture can see the removal. Measured effect: with the pin
  removed, a lane whose committed `.ufo/evidence/round-57/c2/mutants.json` differs from the
  pinned sha256 is graded on the unpinned file instead of being refused — the counter's
  "the three mutants are the pinned three" claim becomes unenforceable.
- **M8 (codes arm vacuous-pass when zero tokens).** Every fixture's Standing-rules section
  names at least one `RECEIPT_*` token, so the `+ (1 if not tokens else 0)` branch is never
  reached. Measured effect: a SKILL whose Standing rules name no code scores `codes` shortfall
  0 instead of 1 — the arm passes vacuously on an empty section.
- **M9 (cell arm compares with `in` instead of equality).** Every fixture's verdict cell carries
  exactly the one code the gate emits, so subset and equality agree. The `cellwrong` fixture
  *swaps* the code but never *adds* a second one. Measured effect: a cell carrying the emitted
  code plus another code is scored `ok` although the table names more codes than the gate emits.
- **M12 (verdict line prints PASS on total>0).** No fixture asserts on the verdict **line**'s
  rendered `C2_R57_PASS` field; the cases assert on `res['total']` and the arm tallies, so a
  lying PASS field is invisible. Measured effect: the rendered line says `C2_R57_PASS=true`
  whenever `total>0` (the process exit code still follows `res['total']`, so only the line lies).

---

## 4. Repair — 6 proposed selftest cases, staged

The staged file
`.ufo/waves/round-57/w2/T57W2MutC2Counter/stage/.ufo/evidence/round-57/c2/measure.py`
(sha256 `a5138acb2248dbf2d05a575ffd66f1eb685b518843649e5129bb03b8040c5a79`) is the pristine
counter plus the six proposed cases and the three fixture knobs they need
(`fx_registry(..., needle_override=)`, `build_lane(..., skill_text=, mutants_text=)`).
Full diff: `receipts/amended-counter.diff`.

| # | proposed case | kills | assertion |
|---|---------------|-------|-----------|
| P1 | rows arm: a refusal row naming an undefined code is counted | M3 | `r['short']['rows'] >= 1` on a fixture whose exit-3 row's needle is `RECEIPT_REV_NOT_A_CODE` |
| P2 | mutants arm: a row that did not hold at baseline supplies no kill credit | M5 | `r['mutants'] == 1` on the `unheld` fixture (a row whose expected exit is wrong) |
| P3 | mutants pin: a lane whose committed mutants.json fails the sha256 pin is refused | M6 | `main_measure()` on that lane returns non-zero, prints `mutants.json unavailable or pin mismatch`, reports `mutants=0/3` |
| P4 | codes arm: a standing-rules section naming no code is a shortfall | M8 | `r['codes_total'] == 0 and r['short']['codes'] >= 1` on a SKILL whose Standing rules name no `RECEIPT_*` token |
| P5 | cell arm: a cell carrying the emitted code plus another code is WRONG | M9 | `r['standing_cell'] != 'ok' and r['short']['cell'] == 1` on a cell naming `RECEIPT_REV_CONTENT_DRIFT` **and** `RECEIPT_REV_ABSENT` |
| P6 | verdict line: C2_R57_PASS=false whenever the total is non-zero | M12 | `'C2_R57_PASS=false' in verdict_line('-', 'x'*12, dict(r, total=1))` |

### Verification of the repair

```
AMENDED   exit=0   C2_R57_SELFTEST: 20/20 pass
M3        exit=1   C2_R57_SELFTEST: 19/20 pass
M5        exit=1   C2_R57_SELFTEST: 19/20 pass
M6        exit=1   C2_R57_SELFTEST: 19/20 pass
M8        exit=1   C2_R57_SELFTEST: 19/20 pass
M9        exit=1   C2_R57_SELFTEST: 19/20 pass
M12       exit=1   C2_R57_SELFTEST: 19/20 pass
```

Each survivor was re-applied **on top of the amended counter**; each then failed **exactly its
own** proposed case and no other:

```
M3  → rows arm: a refusal row naming an undefined code is counted FAIL short={'rows': 0, …}
M5  → mutants arm: a row that did not hold at baseline supplies no kill credit FAIL mutants=3/3
M6  → mutants pin: a lane whose committed mutants.json fails the sha256 pin is refused FAIL
      (the counter graded the unpinned file: mutants=3/3, C2_R57_PASS=true)
M8  → codes arm: a standing-rules section naming no code is a shortfall FAIL codes_known=0/0 short=0
M9  → cell arm: a cell carrying the emitted code plus another code is WRONG FAIL ok
M12 → verdict line: C2_R57_PASS=false whenever the total is non-zero FAIL
```

Receipts: `receipts/amended-<id>-selftest.stdout|.exit` for `AMENDED`, `M3`, `M5`, `M6`, `M8`,
`M9`, `M12`. The amended counter keeps the 14 original cases (all still PASS) and adds 6.

**Not changed:** the counter's measurement logic. The amendment adds *cases and fixture knobs
only*; every arm, threshold and verdict field is byte-identical to the pristine counter. The
amended counter's own measurement at C0 is unchanged (`total=0 C2_R57_PASS=true`, same as
baseline).

**Install note for the L1.** `stage-collect.py --install` **skips a target that already exists**
(`EXISTS-skip`), and `.ufo/evidence/round-57/c2/measure.py` is already present in the lane
(untracked). The staged file therefore will **not** be auto-installed; it must be copied over the
lane's counter deliberately. The staged path collides with no other seat's staged path (the C1
seat stages `.ufo/evidence/round-57/c1/measure.py`), so `stage-collect.py` reports no `DUP`
flag for it.

---

## 5. Lane integrity

| file | sha256 before | sha256 after |
|------|---------------|--------------|
| `.ufo/evidence/round-57/c2/measure.py` | `7d49e3c493b3096f3375bc19ba960049faf6ef76590c4ed2674dbb69a5d2b9cd` | `7d49e3c493b3096f3375bc19ba960049faf6ef76590c4ed2674dbb69a5d2b9cd` |
| `.ufo/evidence/round-57/c2/mutants.json` | `d51f558ca7a4f32c301eccd3bc5ce0814b11da8e16dac539058fbb843448e6de` | `d51f558ca7a4f32c301eccd3bc5ce0814b11da8e16dac539058fbb843448e6de` |

No mutating git/jj command was run in the lane or the fleet repo. The scratch clone used by the
real-verdict probe is `git clone --shared` of the lane into `/fast/scratch/…/probe/clone`, with
its own fixture commits (`-c user.name=fixture -c user.email=fixture@example.invalid`).

---

## 6. Commands (the sweep, verbatim)

```bash
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tameshi-r57/T57W2MutC2Counter; mkdir -p "$S/tmp"

# build the 12 mutant copies (asserts each old string is unique in the pristine counter)
python3 "$S/build_mutants.py" "$S/mut"

# baseline
TMPDIR="$S/tmp" python3 "$S/mut/BASELINE/measure.py" --selftest \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev   ca75c2674645ab6bdadeecb8584007c74342bfa9
# -> C2_R57_SELFTEST: 14/14 pass   exit=0

# the 12 mutants, 4 at a time
bash "$S/run_mutants.sh"          # -> out/M<id>.stdout, out/M<id>.exit

# real-verdict probe at C0 (clone + round-57 evidence dir, like dry-c2.sh)
bash "$S/probe_real.sh"           # -> probe/<id>.stdout

# build the amended counter with the 6 proposed cases and re-apply each survivor on top
python3 "$S/build_amended.py" "$S/amended"
bash "$S/run_amended.sh"          # -> aout/<id>.stdout, aout/<id>.exit
```

Scripts are preserved in `receipts/` (`build_mutants.py`, `build_amended.py`, `run_mutants.sh`,
`run_amended.sh`, `probe_real.sh`, `probe_fixture.py`).

---

## 7. Tools

No package was installed or upgraded for this seat — everything used was already on the host:
system `python3` (stdlib only) and system `git` (`clone --shared` into scratch). No tool was
added to or removed from any PATH directory.

## 8. Judgement notes (operability)

- The counter's **measurement** logic was not falsified by any mutant at C0: every mutant leaves
  the C0 verdict at `total=0 C2_R57_PASS=true` except M4, which the selftest already catches.
  The falsification landed on the counter's **selftest**: 6 of 12 single-point defects are
  invisible to it, and three of those six (M5, M6, M9) can make the counter report a *stronger*
  guarantee than it measured.
- The staged amendment is coverage-only. If the L1 prefers not to change the counter in wave 2,
  the six proposed cases can be carried into wave 3 unchanged — they are additive and each one
  is verified to fail on exactly its mutant.
- M4 is the one mutant with a live effect at C0 and it is already killed by the existing
  selftest, so no repair is owed for it.
