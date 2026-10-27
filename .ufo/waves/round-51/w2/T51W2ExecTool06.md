# T51W2ExecTool06 — independent audit of the C3 registry row for `tools/golden-verdict.py`

Candidate `6d8c11e378aa90b12650808e1b79270742935f15`. Row audited: SKILL.md **line 2147**, the
`golden verdict classes` row of the canonical section `#### Gate/probe registry — round 51`
(heading at SKILL.md:2138). Read-only on the lane; clone `git clone --shared --no-checkout` at CAND
in `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool06/clone`, `TMPDIR=$S/tmp`, stdin `/dev/null`.
Raw receipts: `.ufo/waves/round-51/w2/@P@ExecTool06/receipts.txt`.

## Verdict

**The row is operably true at CAND but four of its cells are imprecise, and one of them is a real
falsification of the row's own evidence claim.** The self-test passes 0, the last line carries the
recorded finding id, the usage probe exits a code the verdict map declares, the pinned paths all
exist, and the write scope is accurate. What does not hold up is (i) the verdict map's silent
conflation of "could not evaluate" into exit 1, (ii) the "Pinned values" cell naming a counter that
does not pin anything, (iii) the self-test cell recording a marker prefix with no expected tally, and
(iv) the entry command being un-runnable as written because `PATH` is a literal placeholder with no
resolved value in the row. **None of these makes the C3 predicate fail for this row**; each is a
row-fidelity defect that the counter's checks cannot see (exactly the C3 `cannot_see` clause).

## 1. The row and the tool

Row (SKILL.md:2147, verbatim, 8 cells parsed by the counter's own `cells()`):

| cell | value |
|---|---|
| Name | `golden verdict classes` |
| Kind | `gate` |
| Entry command | `python3 tools/golden-verdict.py --check-entry PATH` |
| Verdict map | `0 clean; 1 failed; 2 could-not-evaluate (usage)` |
| Self-test command | `python3 tools/golden-verdict.py --selftest` → `GOLDEN_VERDICT_SELFTEST:` |
| Pinned values | `corpus/knowledge/golden-comparison-verdict.md`, `tools/golden-verdict.py`, `.ufo/evidence/round-38/golden/measure.py`; class names and the update-flag rule are literals in the tool |
| Write scope | `no lane write: the named entry is read-only and the selftest writes only inside a TMPDIR temp dir` |
| Owner | `tameshi` |

Tool at CAND: `tools/golden-verdict.py`, 111 lines, sha256 `c5f9616be719fdce99e8aaa9d8c9b1cde5c4c2d4d4db0b517ec16c1a26d15f87`
— **matches** the round-38 pin at `.ufo/evidence/round-38/contract.json:46`. Modes:
`--selftest` (`selftest()`), `--check-entry PATH` (`check_entry()`), `--classify-exit N`
(`classify_exit()`), else usage on stderr + exit 2 (`tools/golden-verdict.py:93-107`).

## 2. Measured runs (the row's exact backticked commands)

| probe | exit | last stdout line | wall |
|---|---|---|---|
| `python3 tools/golden-verdict.py --selftest` | **0** | `GOLDEN_VERDICT_SELFTEST: 3/3 pass` | 38–45 ms over 5 runs |
| `python3 tools/golden-verdict.py --r51-no-such-flag` | **2** | (stdout empty; argparse usage on stderr) | 38–45 ms over 5 runs |
| `… --check-entry corpus/knowledge/golden-comparison-verdict.md` | **0** | `GOLDEN_VERDICT_ENTRY: classes=3/3 update_rule=present path=…` | ~45 ms |

Both required behaviours hold: exit 0 with the row's marker on the last line for the self-test, and
the usage probe exiting 2, a code the verdict map declares ("2 could-not-evaluate (usage)").

The marker is a **meaningful diagnostic, not help text**: `GOLDEN_VERDICT_SELFTEST:` is emitted by
`tools/golden-verdict.py:66` from the case table (`3/3 pass`), and it changes with the verdict. It is
not an argparse heading or a hand-written string in the row.

## 3. Row fields checked against the source

**Kind = `gate` — TRUE, the tool genuinely fails.** PROTOCOL §Gate standard (line 388) separates a
gate ("cannot fail ⇒ probe") from a probe. The entry command fails on a real surface:

```
$ python3 tools/golden-verdict.py --check-entry entry-no-error.md     # '| error |' class row removed
GOLDEN_VERDICT_ENTRY: classes=2/3 update_rule=present path=…
MISSING outcome class: error
exit=1
$ python3 tools/golden-verdict.py --check-entry entry-no-flag2.md     # all update/flag text removed
GOLDEN_VERDICT_ENTRY: classes=3/3 update_rule=absent path=…
MISSING explicit update-flag rule
exit=1
```

So `gate` is right and the tool is not merely a probe.

**Exit codes — the map is complete but semantically lossy.** Enumerated every reachable code:

```
--selftest 0 | (no args) 2 | --classify-exit {0,1,2,127} 0 | --classify-exit abc 2
--check-entry (no value) 2 | --r51-no-such-flag 2 | --help 0
```

No code outside {0, 1, 2} is reachable, so nothing is *undeclared*. But **exit 1 carries two
different meanings**, and the row's map records only one of them:

```
$ python3 tools/golden-verdict.py --check-entry genuine-fail.md   # non-conforming entry
exit=1
$ python3 tools/golden-verdict.py --check-entry no-such-file.md   # absent input
GOLDEN_VERDICT_ENTRY: unreadable no-such-file.md ([Errno 2] No such file or directory)
exit=1
$ python3 tools/golden-verdict.py --check-entry corpus/knowledge  # a directory
GOLDEN_VERDICT_ENTRY: unreadable corpus/knowledge ([Errno 21] Is a directory)
exit=1
```

`check_entry()` returns 1 from both the unreadable branch (`tools/golden-verdict.py:77-79`) and the
non-conforming branch (`:90`), so **"could not evaluate" is reported as "failed"**. That contradicts
the lane's own doctrine in the entry the row pins —
`corpus/knowledge/golden-comparison-verdict.md:34`, "**A comparison that could not be made is not a
failure of the code under test**", and its table row for `error`, "nothing was compared; the fixture
proved nothing and must not be recorded as a red". A sibling row in the same table does draw the
line the lane's convention requires: SKILL.md:2146 declares "2 could-not-evaluate (missing,
unreadable, malformed, tampered or path-invalid input …)". **The golden row declares 2 for usage
only.** Measured consequence: a missing/unreadable entry is graded red.

Worse, a non-UTF-8 entry does not even fail closed *as* a verdict — it dies on an uncaught
`UnicodeDecodeError` and lands on the same exit 1:

```
$ python3 tools/golden-verdict.py --check-entry binary.bin
<stdout empty>
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xc4 in position 128
exit=1
```

**Pinned values — the round-38 counter cited as a pin pins nothing.** All three paths exist at CAND
(`git cat-file -e` confirms each). But `--check-entry` takes the entry path *from the caller*
(`:96`), so the pinned corpus entry is a **default subject, not a dependency of the tool**: deleting
both the corpus entry and the whole `.ufo/evidence/round-38/` tree from a scratch copy still gives

```
$ python3 tools/golden-verdict.py --selftest
GOLDEN_VERDICT_SELFTEST: 3/3 pass
exit=0
```

so the self-test's expected behaviour is independent of two of the three "pinned values". And the
third — `.ufo/evidence/round-38/golden/measure.py` — is not a pin either: it *prints* `tool_sha256`
and never compares it to the contract's literal (no comparison, no `contract.json` read; verified by
`grep`). Demonstrated on a fixture repo whose tool differs only by a leading comment line:

```
$ python3 .ufo/evidence/round-38/golden/measure.py --lane FIX1 --rev HEAD
GOLDEN_R38: cases=3/3 mutant_killed=true entry_ok=true tool_sha256=1346c93b… C2_R38_PASS=true
exit=0
```

The pin is `c5f9616b…`; the counter reported **PASS on a different sha256**. So the "Pinned values"
cell names a file that does not pin the bytes it is cited for — a violation of PROTOCOL's §Drift pins
(line 383: a fingerprint *printer* with no stored baseline "cannot detect drift"), and a hole the C3
counter explicitly does not see (`c3/measure.py` only checks that a pinned path *exists*).

Second, sharper probe: gutting the entry command's fail arm
(`:90` `return 0 if not missing and update_rule else 1` → `return 0`) leaves the self-test green
**and** the cited r38 counter green:

```
$ python3 tools/golden-verdict.py --selftest                      # M2 mutant
GOLDEN_VERDICT_SELFTEST: 3/3 pass
exit=0
$ python3 tools/golden-verdict.py --check-entry nothing.md        # gate that can no longer fail
GOLDEN_VERDICT_ENTRY: classes=0/3 update_rule=absent …   (MISSING ×4)
exit=0
$ python3 .ufo/evidence/round-38/golden/measure.py --lane FIX-M2 --rev HEAD
GOLDEN_R38: cases=3/3 mutant_killed=true entry_ok=true … C2_R38_PASS=true
exit=0
```

So neither the row's self-test nor the row's own pinned counter detects that the gate has stopped
failing. The gate's *failability* rests on an argument the row never records.

**Write scope — TRUE, verified.** `tempfile.TemporaryDirectory(prefix='golden-verdict-')`
(`:47`) honours TMPDIR: `tempfile.gettempdir()` resolves to the scratch dir, TMPDIR is empty after
each run, `git status --porcelain` in the clone is clean after all probes, and `--check-entry` opens
the entry read-only (`:75`, no mode argument). Nothing else is written.

**Self-test cell — marker prefix only, no expected tally.** The row says `→ GOLDEN_VERDICT_SELFTEST:`;
the tool prints `GOLDEN_VERDICT_SELFTEST: 3/3 pass`. Every sibling row in this table records the
tally (`mte-interop` "17/17 pass", `pbt-staged-id` "cases=35 failed=0", `receipt-window`
"20/20 pass", `tally-audit-v2` "22/22 pass"). The counter's check is `last.split()[0] in st`, so it
accepts the bare prefix — a tool that printed `GOLDEN_VERDICT_SELFTEST: 0/3 pass` with exit 0 would
still be credited. Demonstrated: a mutant that hard-codes the print and returns 0 always

```
GOLDEN_VERDICT_SELFTEST: 3/3 pass
exit=0
```

satisfies the counter's row check. (The round-38 counter does kill this one via `mutant_killed=false`,
so it is not unguarded overall — but the row's own self-test cell does not carry the guard.)

**Entry command — not runnable as written.** Run verbatim, `PATH` is a literal argument:

```
$ python3 tools/golden-verdict.py --check-entry PATH
GOLDEN_VERDICT_ENTRY: unreadable PATH ([Errno 2] No such file or directory: 'PATH')
exit=1
```

The row names the tool and the mode, but the concrete entry is only recoverable from the "Pinned
values" cell. This is the same shape as several siblings (`--repo REPO`, `--receipt RECEIPT.json`),
so it is a table-wide convention, not a defect unique to this row — recorded for completeness.

**Kind/owner**: `gate` ✓, `tameshi` ✓. **A judge finding id is recorded** and the tool is
`tools/golden-verdict.py`, so the row's "entry naming the tool" requirement holds.

## 4. Counter consequence

The C3 counter credits this row at CAND (its own `row_reason` and `run_row`, run from a fresh shared
clone in scratch):

```
row line 2147 cells 8
row_reason -> None
argv      -> (['python3','tools/golden-verdict.py','--selftest'],
              ['python3','tools/golden-verdict.py','--r51-no-such-flag'], …)
run_row   -> None | last='GOLDEN_VERDICT_SELFTEST: 3/3 pass'
```

**No mismatch blocks C3 for this row.** The row is operably true; the defects above are fidelity
defects the counter is blind to by construction, and they are disclosed here rather than repaired
(this seat does not edit the row or the tool).

## 5. Notes on scope

- This is **not** the row16 / `round21-measure.py` clone-context failure; my tool's self-test has no
  sibling-repo dependency and passes from a bare shared clone. It does depend on the external `diff`
  binary (`tools/golden-verdict.py:40`): with `diff` absent from PATH the self-test dies on an
  uncaught `FileNotFoundError` (`exit=1`, stdout empty). That dependency is unrecorded in the row
  and is invisible to the counter (which inherits a PATH containing `diff`).
- The tool is not the row16 blocker; the known row16 clone-context failure does not apply.

## 6. Findings, ranked

1. **Exit-1 conflation (real, cited).** `:77-79` and `:90` both return 1, so an absent/unreadable
   entry is graded `failed`; the row declares `2` for usage only, diverging from the lane's own
   `error` class doctrine (`corpus/knowledge/golden-comparison-verdict.md:34`) and from sibling row
   SKILL.md:2146. A binary entry additionally raises an uncaught `UnicodeDecodeError` on the same
   code.
2. **"Pinned values" overstates (real, demonstrated).** `.ufo/evidence/round-38/golden/measure.py`
   prints the sha and compares it to nothing: a comment-drifted tool yields `C2_R38_PASS=true` with
   `tool_sha256=1346c93b…` against the frozen `c5f9616b…`. Two of the three pinned paths do not
   affect the self-test at all (deleted → still 3/3, exit 0).
3. **No paired failability evidence in the row (real, demonstrated).** Gutting `:90` leaves the
   row's self-test green and the row's cited counter green — the entry command becomes a gate that
   cannot fail while both evidences report PASS.
4. **Self-test cell lacks the expected tally (minor).** Marker prefix only, vs. full tally in every
   sibling row; the counter's `last.split()[0] in st` accepts a hard-coded marker.
5. **Entry command has an unresolved `PATH` (minor, table-wide convention).**
6. **Undeclared external dependency `diff` (minor).** Absent `diff` → uncaught traceback, exit 1.

Nothing here is a C3 predicate failure; items 1–3 are the row-fidelity gaps the contract's
`cannot_see` clause names, and they should be routed as row defects, not as counter failures.
