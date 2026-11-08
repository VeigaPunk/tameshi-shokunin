# Round 92 — lesson (tameshi)

Base `63172b9889475103aeca976d37389d204010dd11` (round-91 verifier spot-check tip).
One claim this round: R92-C1, coverage — the third attempt at certifying the
round-90 fleet-gate mutation case, under a sealed counter that pins its own
sha256 and refuses any verdict-shaped row outside the spec's id set.

## Gate

| Item | Decision | Source opened this round | Reason |
|---|---|---|---|
| S320 sha256sum(1), Arch manual pages (GNU coreutils 9.12) | admit (A, `mined`) | https://man.archlinux.org/man/sha256sum.1.en, fetched 2026-11-08, HTTP date `Sun, 08 Nov 2026 05:27:37 GMT`, 12 127 B, sha256 `b968bc09839877f9b0bf892b8a37fce0f72f4fa0ff0f17208824161b8547277b` (`.ufo/evidence/round-92/sources/s320.html`, headers in `s320.headers`) | "Print or check SHA256 (256-bit) checksums." (6 words, `sources/s320.txt:19`) and "The sums are computed as described in FIPS-180-2." (8 words, `:53`). Grounds the counter's `SELF_SHA256` pin: the pin is a sha256 digest of the instrument's own bytes, and `--check`/`--strict` are the semantics a reader uses to re-verify it. |
| Claim candidate: reuse round-91's frozen counter and re-point its `source:` conjunct at S320 | reject | round-91 `measure-v91.py` `parse_note` and its receipts | round 91's counter was killed by its own wave (a hidden `C001`-`C012` table is invisible to `^\|\s*(C\d\d)`) and its receipts certify post-freeze bytes; a re-pointed copy would inherit both defects. A successor is required, and it must pin its own bytes (QUALITY 143-144). |

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M1 | **the battery counted what it selected, not what it declared.** The first full driver run printed `C1_CONTROLS states=20 matched=20` while the three removal mutants (D01, D01D02, D03) and the do-nothing base were never selected: `sel = list(C)` held only the repo states, and the mutant loop iterated that same list. The summary was computed from the in-memory results, so it could not disagree with the run set. | driver repairs `7da303df` (A4), `33b90d48` (A5), `f0ece7a3` (A6): `git diff 84904d41 f0ece7a3 -- .ufo/evidence/round-92/c1/controls-v92.py`; the committed run prints `states=25 matched=25` (`.ufo/evidence/round-92/pre-freeze/controls/C1-summary.txt`) | none — no rule required the summary's state count to equal the pre-registered expectation table | QUALITY 152: the summary is derived from the receipts on disk and a state the run did not select is a missing row. Able to fail: the A5 driver on the same battery printed `states=19` with three mutant receipts absent |
| M2 | **a conjunct printed as a literal.** `measure-v92.py` at `884a4dc1` printed `selfpin=True` from a constant in the conjunct dict; the check ran and refused, but the receipt's value could not be false, so the figure carried no information about the check that produced it. | `git show 84904d41 -- .ufo/evidence/round-92/c1/measure-v92.py` (the A3 hunk: `selfpin = self_pin_ok()` and `dict(selfpin=selfpin, ...)`); `selfpin-edit.out` is the receipt the check now governs | QUALITY 138's "no figure is a literal in the counter's own output", read as applying to selftest totals only, not to every conjunct | QUALITY 150. Able to fail: the edited-counter control `selfpin-edit.out` (`C1_SETUP self-pin-mismatch`, exit 2) |
| M3 | **an incomplete removal control proves nothing about the defences it did not remove.** D03's first construction dropped the self-pin assert, narrowed the id shape and removed the unkeyed rule, but left the `headers == 1` rule in place: the hidden-table state was still refused (`exit=1`, `badrows=0 headers=2`), so D03 could not show that the parser change alone was a cheat. The header-count rule is an independent second defence against the exact round-91 attack. | driver repair `f144da2b` (A7: `.replace(hdr, "ids_ok = (not bad) and headers >= 1 and", 1)`); final `D03.out` (`exit=0`, `C1_R92_PASS=true` only after the rule was relaxed). The first refusal's receipt was overwritten by the corrected run — see M4 | none — QUALITY 149 names the removal control but not that the removal must be complete | the D03 mutant now removes all four rules; the surviving evidence is the A7 diff and the final receipt. QUALITY 151 records the header count as a defence in its own right |
| M4 | **a receipt was overwritten in place.** Re-running a control wrote `D03.out` over the failed D03 run, so the first failure's receipt no longer exists; the driver opens every receipt with `"w"` and has no existence guard. | the driver's receipt writes (`open(os.path.join(a.outdir, name + ".out"), "w")`), unchanged from the A6 blob; the overwritten content is not citable (transcript only) | none — no rule required a superseded receipt to be preserved; considerthese `2026-11-07.md` idea 5 names the write-safety class | routed to round 93: a re-run writes `<name>.rerun-<n>.out` and never overwrites a committed receipt; the driver is not changed after the freeze in this round |

## Claim and kill

**R92-C1 (coverage) — predicate met, killed by its own rule (a) branch 2.** The sealed
counter's honest receipt at the freeze is `C1_R92_PASS=true`, exit 0, all seventeen
conjuncts true, `badrows=0 headers=1`
(`.ufo/evidence/round-92/pre-freeze/measure-at-freeze.txt`); the 25-state battery prints
`C1_CONTROLS states=25 matched=25 mismatches=0`, and the two new refusals hold on their own
states (a hidden `C001`-`C012` table: `ids=false`, `badrows=12`; a post-freeze instrument
edit: `C1_SETUP self-pin-mismatch`, exit 2). The do-nothing receipt is
`pre-freeze/controls/nowork-base.out` (`C1_SETUP spec-absent-at-rev`, exit 2).

Then the wave killed it, in the same class the counter was built to close. T92C1 `A13` is
the committed note with its §2b impact table reformatted so the id is its own cell — no
verdict changed; the counter refuses it (`ids=false`, `badrows=5`). That is an honest note
refused by a rule stated in the claim: because `parse_note` refuses **any** id-shaped row
that does not carry exactly one verdict token, not only verdict-bearing rows. T92R1 SF-2
adds the same class for a `verdict`-word cell and bold ids. T92R1 SF-1 adds the opposite
defect in the *text*: the kill rule lists "a fenced table" while the declared limits say
fenced tables are not keyed; a fenced inverted table (T92C1 A1) and an HTML table (A2) and
a prose presentation (A3) all PASS because the keyed table is still true. T92M1's mutation
matrix scores 25/30: M19 (no timeout state) is killable and missing, M20/M24/M25/M28 are
not falsifiable under the pinned gate. A10/A11 are decoys the `coverage`/`source` conjuncts
admit: a README row that says the note is **not admitted** satisfies coverage, and the
lesson's bare `S320 <URL>` satisfies source.

The claim is therefore not admitted; the round is an honest stop whose deliverable is the
narrowing below.

## Wave

One v1 wave `r92-w1`, 11 seats, all eleven settled with reports: executor 3 (T92E1
`reproduced-12/12`, T92E2 `no-regression`, T92E3 `reproduced`), scribe 1 (T92SC1 draft +
four measured probes), scout 2 (T92S1 `agree`; T92S2 `premise-holds`), reviewer 2 (T92R1
`findings:2`, T92R2 `defects:4`), critic 1 (T92C1 `killed:A13-id-keyed-2b-reformat`),
mutation-tester 1 (T92M1 `killed:25/30`), sentinel 1 (T92SN1 `findings:8`). Attack seats
5/11 = 45 %. No seat died; no residual call.

| M5 | **the wave spec's constants were one revision stale.** `.ufo/waves/round-92/make-spec.py` still carried `INSTR_REV = 884a4dc1`, `COUNTER_SHA = a6adf4a6…` and `DRIVER_REV = 3119c0ea` after the instrument moved to A3/A7: nine seats were briefed with the wrong counter sha, T92E3 was told to run `--rev 884a4dc1`, and it killed a battery run mid-flight on the correction. | the dispatch text (`w1-dispatch.json`) vs `plans/round-92.plan.md`; the corrected generator (records commit) and T92E3 §0 / T92R2 Note S1 | none — the spec generator copied constants by hand, and no check compared them with the plan before dispatch | the generator must derive the sha256 from `git cat-file blob <rev>:<path>` and refuse when it disagrees with the plan; routed to round 93. Able to fail: the stale dispatch carries `a6adf4a6` while `git cat-file` says `be5a9221` |
| M6 | **the kill: the reader refused honest rows by id shape.** `parse_note` made every id-shaped table row a verdict row, so an id-keyed impact table with no verdict token refused the note (T92C1 A13, `ids=false badrows=5`) and a `verdict`-word cell created a second header (T92R1 SF-2). Honest-note refusal is kill rule (a) branch 2. | `.ufo/waves/round-92/w1/T92C1-A13-id-keyed-2b-reformat-note.md` + `T92C1-A13-id-keyed-2b-reformat.out`; `T92R1-probe.out` | the plan's own wording ("whose first cell is id-shaped **or** that carries a verdict token must ... carry exactly one verdict token") — it required a token of non-verdict rows | QUALITY 154/155. Able to fail: the A13 receipt (honest note, `ids=false`, exit 1) |
| M7 | **the kill rule and the limits contradicted each other.** Rule (a) listed "a fenced table" among the presentations that kill; the declared limits said fenced blocks are not keyed. A fenced inverted table PASSes, so the claim could be killed from the rule text alone. | `plans/round-92.plan.md` rule (a) vs declared limits; `.ufo/waves/round-92/w1/T92C1-A1-fenced-second-table.out`; T92R1 SF-1 | none — no check compared the kill rule's presentation list with the limits before the freeze | QUALITY 156. Able to fail: `T92C1` A1 PASS with the inverted fenced table |
| M8 | **the battery's conjunct coverage was incomplete and unstated.** 30 single-edit mutants: 25 killed, 5 survived. M19 (inconclusive0 forced true) is killable with a `timeout_s` state the battery does not have; M20/M24/M25/M28 cannot be falsified under the pinned gate at all. | `.ufo/waves/round-92/w1/T92M1.md` §5 (`SURVIVORS:` line, `T92M1-mutants.out`) | QUALITY 146 ("every conjunct fails at least once") read as satisfied by the state set that existed, not by a mutation matrix over the shipped bytes | QUALITY 158; the timeout state and the unfalsifiable declarations route to round 93. Able to fail: the matrix's five SURVIVED rows |

