# T49W2RevQuality — round-49 QUALITY.md additions (criterion 99)

Seat: wave-2 reviewer, round 49 (tameshi). Item: review the round's `corpus/QUALITY.md` additions at
`f181a961ae44061af486f600e5ea257d2baf78f8` — each new criterion (a) cites its lesson, (b) is not a
duplicate of criteria 1-98, (c) carries a falsifier that can fail. Probe only; I decide no claim; no
counter was invoked at any revision (one gate-0 refusal re-run only, which starts no counter).

Scope observed:

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff 8ca67421111fa354b47b803358391d0b07fc6db9 f181a961ae44061af486f600e5ea257d2baf78f8 -- corpus/QUALITY.md
# -> 1 file changed, 22 insertions(+) — exactly one new criterion:
#    "### Criterion 99 — a control is scored and committed before the deciding run it discriminates,
#     and the script refuses otherwise" (corpus/QUALITY.md:1444-1464 at f181a96)
```

No other QUALITY.md line changed; criteria 1-98 untouched. All line numbers below are at `f181a96`
(read from a scratch shared clone checked out at it; scratch deleted before yield — every command is
reproducible against the lane with `git show f181a961…:<path>`).

## Check 1 — the criterion cites its lesson: verified

- `corpus/lessons/round-48-verifier-spotcheck.md:27` — Conformance defect 2, "**C1 controls scored
  after the deciding run.** … CTL_B to CTL_E were scored by attempt 3 from 16:21:02Z to 19:35:25Z …
  after the C1 deciding run (15:34:20Z to 16:20:54Z …)". Matches the criterion's "round 48 stated the
  order in prose and scored CTL_B-CTL_E after its deciding run" (QUALITY.md:1457-1458).
  `grep -n "C1 controls scored after" corpus/lessons/round-48-verifier-spotcheck.md` → line 27.
- `corpus/lessons/round-48-verifier-spotcheck.md:28` — defect 3, undisclosed `--only` previews at the
  content revision; matches the criterion's disclosure clause "Any other invocation of a claim counter
  at the deciding revision (a partial or probe mode, a seat preview) is listed in the report with its
  revision and verdict line" (QUALITY.md:1452-1453); also routed as `:116`.
- `corpus/lessons/round-49.md:86` — `## Mistakes` row 1: "round 48's pre-registered control order was
  kept only in prose; CTL_B-CTL_E were scored eight seconds after the C1 deciding run ended, and
  partial counter invocations at the deciding revision were not named in the report", fix = the
  deciding-run gate. The 8-second arithmetic checks out against the timestamps quoted in defect 2
  (16:20:54Z end → 16:21:02Z start). Row 1's captured-by note — "none (QUALITY 69 and 88 do not reach
  a claim counter's control order)" — also checks out: criterion 69 (QUALITY.md:784-787) binds
  data-wave binding conditions frozen as code, not a claim counter's control order.

## Check 2 — not a duplicate of criteria 1-98: verified

`grep -nE "deciding|receipt|scored (with|after|before)|before the|refus" corpus/QUALITY.md` and
`grep -n "invocation|second deciding|start receipt" corpus/QUALITY.md` surface every order/receipt
criterion in 1-98. The closest adjacents, read in full:

- 58 (QUALITY.md:653-663) — a required control whose seat dies blocks the **data wave**; control
  availability, not order, not the deciding run.
- 59 (QUALITY.md:665-676) — control receipts committed in a lane commit that precedes the **data-wave
  spec commit**; commit-order proof, no script gate, no deciding run.
- 86 (QUALITY.md:1156-1182) — the deciding receipt binds the **revision measured**; receipts after C;
  drift listing. Nothing about control-receipt order.
- 88 (QUALITY.md:1291-1315) — no-harm monitors run at the base **before the freeze**; different
  receipts, different event.
- 98 (QUALITY.md:1436-1442) — cold-read precheck on the candidate **before the freeze**; different
  gate.

No criterion 1-98 states "controls scored before the deciding run" or a script-enforced refusal for
it; criterion 99's subject (claim-counter control order, enforced by the deciding script's gate 0) is
new. Adjacent to 59 in subject family but distinct in event, proof and enforcement — recorded below so
a future reader does not collapse them.

## Check 3 — the falsifier can fail: verified (three committed receipts; case (a) re-run observed)

The falsifier (QUALITY.md:1460-1464) names `.ufo/evidence/round-49/deciding-run.sh` at the freeze
`14d03ea4` and three refusal conditions. All verified:

- Script identity: `sha256sum .ufo/evidence/round-49/deciding-run.sh` at f181a96 →
  `31e9838e735b27a9aa6ac3ee5ccc3e8f2d39432a32e3dd6a80ab456125dd10f5` = the `freeze.json:15` pin;
  `git diff 14d03ea4… f181a96… -- .ufo/evidence/round-49/deciding-run.sh` is empty (identical bytes at
  freeze and candidate).
- Premise of case (a): `git ls-tree --name-only 14d03ea4270c6904064022b62b6faf467e5c0968 -- .ufo/evidence/round-49/control/`
  lists harnesses and selftests only — no `c1-controls.stdout`/`.exit`, no `c2-controls.stdout`/`.exit`.
- Committed receipts match the claimed lines exactly:
  `.ufo/waves/round-49/w1/T49ExecMistakeGate/case-a.stdout` = `DECIDING_REFUSED control-receipt-missing .ufo/evidence/round-49/control/c1-controls.stdout`;
  `case-b.stdout` = `DECIDING_REFUSED second-invocation c1`;
  `case-c.stdout` and `case-c-literal.stdout` = `DECIDING_REFUSED control-receipt-not-after-freeze .ufo/evidence/round-49/control/c1-controls.stdout`
  (case-c fixture: receipt commit `ebd2e64` predating a rewritten freeze `e5eb093`, plus the literal
  ancestor-of-`14d03ea` shape via a replace ref; `commands.txt`, `gate0-subchecks.txt`, `fixture.txt`).
- My own re-run of case (a) in scratch (clone at `14d03ea`, `HYAKU_SCRATCH=$S`, existing empty OUT):

  ```
  HYAKU_SCRATCH=$S bash "$S/clone/.ufo/evidence/round-49/deciding-run.sh" "$S/clone" 14d03ea4… 14d03ea4… "$S/out-a"
  # stdout: DECIDING_REFUSED control-receipt-missing .ufo/evidence/round-49/control/c1-controls.stdout
  # exit=3 ; OUT still empty ; $S/tameshi-r49 (the script's work root) never created
  ```

  Confirms "exits 3 having started no counter": every refusal exits at deciding-run.sh:22-29, before
  the first side effect outside OUT (`mkdir -p "$SCR"`, :30) and before any counter (:43-48).
- Practice complies at the candidate: all four gated receipts are last touched by `6885adb4`
  ("round-49: controls scored at freeze bytes …"), and
  `git merge-base --is-ancestor 14d03ea4… 6885adb4…` → 0.
- Pointers resolve at f181a96 (criterion 97 shape): `git cat-file -e f181a961…:<path>` OK for
  `.ufo/evidence/round-49/deciding-run.sh`, `.ufo/waves/round-49/w1/T49ExecMistakeGate.md`,
  `.ufo/waves/round-49/w1/T49ExecMistakeGate`, `corpus/lessons/round-48-verifier-spotcheck.md`,
  `corpus/lessons/round-49.md`.

## Findings

**F1 (minor) — the criterion's "descends from the counter freeze" is enforced as "at or after", and
neither the criterion's limit list nor its falsifier covers the freeze-commit-itself case.**
Criterion 99 states the receipt is "committed in a commit that descends from the counter freeze"
(corpus/QUALITY.md:1448-1449); the script implements
`git merge-base --is-ancestor "$FREEZE" "$c"` (`.ufo/evidence/round-49/deciding-run.sh:27`), which is
reflexive — `git merge-base --is-ancestor 14d03ea4270c6904064022b62b6faf467e5c0968 14d03ea4270c6904064022b62b6faf467e5c0968; echo $?`
→ 0 (also recorded in `.ufo/waves/round-49/w1/T49ExecMistakeGate/fixture.txt`, "is-ancestor
reflexivity boundary: exit=0", and T49ExecMistakeGate.md gate-strength finding 2). A control receipt
committed inside the freeze commit itself therefore passes gate 0 while violating the criterion's
plain-English rule; the falsifier set (QUALITY.md:1460-1464) exercises only the strictly-before case.
The criterion names two limits — order-not-values (:1453-1454) and probes outside the receipt
directory (:1455) — but not this third one, although wave 1 had already surfaced it. Fix: an
append-only clause naming the at-or-after semantics beside the other two limits.

**F2 (minor) — "(one deciding invocation)" overstates the start-receipt gate: it is per-OUTDIR.**
Criterion 99 glosses the third refusal as "when its receipt directory already holds a start receipt
(one deciding invocation)" (QUALITY.md:1451-1452). The script checks only `$OUT/$k.start` for the
OUTDIR handed to it (deciding-run.sh:29); a second invocation with a fresh empty OUTDIR passes gate 0
— the real backstop is the criterion's own disclosure clause (:1452-1453), not the gate. Wave 1
recorded the same limit (T49ExecMistakeGate.md finding 3, "not exercised"). The criterion should carry
the per-OUTDIR qualifier rather than equate the check with one-deciding-invocation outright.

**F3 (minor) — the gate's receipt list is the two harness summaries, not each pre-registered
control's receipt.** The rule says "Every pre-registered control of a claim counter … its receipt is
committed" (QUALITY.md:1448-1449); the gate checks exactly four paths — `c1-controls.stdout/.exit`,
`c2-controls.stdout/.exit` (deciding-run.sh:23-25). The per-control receipts (`c1-CTL_0/J/K/K2.stdout`,
`c2-CTL_ABSENT/CTL_FIX/WITNESS.stdout`) are committed at f181a96
(`git ls-tree --name-only f181a961… -- .ufo/evidence/round-49/control/` → all present), so the round's
practice satisfies the stronger reading, but a tree committing only the two summaries would pass the
gate with the per-control receipts absent. "Binds the order, not the values" (:1453-1454) covers
values, not per-control receipt presence.

**N1 (nit) — falsifier case (a) has an unstated precondition.** `control-receipt-missing` fires only
when OUTDIR exists; with a nonexistent OUTDIR the script prints `DECIDING_REFUSED outdir-missing`
first (deciding-run.sh:22 vs :25). The falsifier text (QUALITY.md:1460-1462) omits this; the script's
usage header (:4) states it. A reproducer following the falsifier text alone could see a different
refusal line and call it a mismatch.

**N2 (nit) — context-relative shorthand in the falsifier's receipt pointer.** QUALITY.md:1464 cites
"receipts in `T49ExecMistakeGate/`" — not a repo-root path; it resolves only relative to the citing
file's directory (`.ufo/waves/round-49/w1/`). Same established convention as criterion 94's
`quality/c94-96-falsifiers.stdout` (:1398). A mechanical criterion-97 pointer check must expand
context-relative shorthands or it will flag this line MISSING.

**N3 (nit) — hyphen line-wrap inside a token.** The lesson line wraps "CTL_B-" / "CTL_E" across
QUALITY.md:1457-1458; after a criterion-91-style whitespace collapse the token reads "CTL_B- CTL_E".
Cosmetic today; matters only if a future byte-exact-after-fold check quotes this line.

## Residual risk / verification gaps

- Gate 0's pass-side behavior was never exercised by me (a passing gate runs the counters); F1's
  freeze-commit acceptance is derived from the reflexivity fact plus code reading of :27, not from a
  full passing run. Wave 1's sub-check table (`gate0-subchecks.txt`) is the committed evidence that
  the four sub-checks pass for after-freeze receipts.
- Whether the round report will list every counter invocation at the deciding revision (the criterion's
  disclosure clause, :1452-1453) is checkable only at closure.
- I did not audit the real control receipts' contents (`c1-controls.stdout`, `c2-controls.stdout`) —
  other seats' scope; this review needs only their committed presence and commit order, both verified.
- The hidden C2 panel and `~/.local/state/` were never read; `c2-WITNESS.stdout`, `c2-CTL_FIX.stdout`,
  `c2-CTL_ABSENT.stdout` were never opened (not named by my item).

Tooling: nothing installed or upgraded (git, bash, python3, GNU coreutils as present); no pacman
transaction. Scratch `/fast/scratch/hyaku/tameshi-r49/T49W2RevQuality` (shared clone at f181a96, one
gate-0 refusal re-run) deleted before yield; no cited evidence lives in scratch.

Report: .ufo/waves/round-49/w2/T49W2RevQuality.md

## Summary

- Scope: `git diff 8ca67421..f181a96 -- corpus/QUALITY.md` adds exactly one criterion — 99
  (corpus/QUALITY.md:1444-1464); criteria 1-98 untouched.
- Lesson citations verified: round-48-verifier-spotcheck.md:27-28 (defects 2-3) and round-49.md:86
  (Mistakes row 1) both say what the criterion claims; the 8-second gap arithmetic checks out.
- Not a duplicate: greps surface 58/59/86/88/98 as the only order/receipt adjacents; none reaches a
  claim counter's control order at the deciding run (69 checked too, per the lesson's captured-by).
- Falsifier can fail: three committed refusal receipts match the claimed `DECIDING_REFUSED` lines; my
  own case-a re-run observed the line, exit 3, empty OUT, no work root — no counter started.
- Script identity verified: sha256 `31e9838e…` = freeze.json:15 pin; identical bytes at 14d03ea and
  f181a96; no control receipts committed at the freeze (case-a premise); practice complies at the
  candidate (receipts last touched by after-freeze commit 6885adb4).
- F1-F3 (minor): criterion/falsifier gaps — freeze-commit receipts pass the reflexive is-ancestor
  check (:27); the one-invocation gate is per-OUTDIR (:29); the gate lists two harness summaries, not
  each per-control receipt (:23-25). N1-N3: unstated OUTDIR precondition, shorthand pointer, hyphen
  wrap. All append-only fixes; nothing rewritten.
- No verdict taken; no counter invoked at any revision; hidden panel untouched.
