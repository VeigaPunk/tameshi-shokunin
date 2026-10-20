# CriticMistakes — attack on `.ufo/waves/round-18/staged/lesson-round-18-mistakes.md` (5 rows)

Read rev `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`; clone `$C` at that rev.
Axes attacked: (a) honesty of each `Captured-by`; (b) whether each fix is
shown able to fail by a **committed artifact**, not prose; (c) accuracy of
every quoted fragment and `path:line` anchor.

## F0 — decisive counterexample: `Captured-by` is evaluated at the admission rev, not the read rev

Four of five rows claim `none` (row 1 `partial`) for capture, but the same
build landing (`58e5d53`) that staged this doc added QUALITY criteria that
capture these exact mistakes — and name them:

- Row 1 (breadth overclaim): `corpus/QUALITY.md:236-250` criterion 33 —
  "A claim that holes or commands are 'covered', 'closed' or 'all run' binds
  each declared command to an argv in a committed trace receipt"; its own
  Captured-by names "the round-17 K02 claim that holes 1–4 were all closed"
  (R17-CMD-BIND). The row's "no criterion ties the breadth of a gate reason
  to the command coverage it claims" is **false at the read rev** — QUALITY
  33 is exactly that tie.
- Row 2 (7 surviving guards): `corpus/QUALITY.md:176-189` criterion 29 —
  "a surviving mutant; the owner either adds a killing selftest case in its
  next round or names the mutant equivalent"; its Captured-by names the same
  seven survivors (G3 tag-object, G5 symlink-mode, detached-checkout,
  short-rev regex, O_RDWR, pycache-prefix, execve) — the identical list in
  the row's evidence pointer. "none for the kill requirement" is **false at
  the read rev**; QUALITY 29 is the standing kill requirement, and its
  "check that can fail" is the row's own falsifier.
- Row 5 (stale count): `corpus/QUALITY.md:262-279` criterion 35 — "a
  correction to a landed entry (an exit sentence, **a count**, a citation…)
  is an appended, dated erratum… This extends criterion 26 from receipts to
  corpus prose". The row's "QUALITY 26 covers stale receipts, not lesson
  prose" is stale: 35 closes exactly that gap.
- Row 4 (wrong cross-reference): also covered by 35's citation/correction
  mechanics, though 34 (anchor fragility) does not prevent wrong *targets*;
  "none" is the most defensible of the four.

Verification that 29–35 postdate the mistakes' admission:
`git show 183f87b…:corpus/QUALITY.md | grep -c 'killing selftest'` → 0;
QUALITY.md last modified at base is criterion 28 (tail of base file ends
with the criterion-27 note). Fixable defect, not a reject: each row's
Captured-by should read "none at admission; now QUALITY 29/33/35" — which
incidentally makes the doc stronger, since the criterion *is* the fix's
standing guard. As written, the column is systematically dishonest-by-omission
in the same commit that introduced the capturing criteria.

## Row-by-row

### Row 1 — breadth overclaim (K02 holes 1–4). WEAKEST.
- Evidence pointers verified: `corpus/lessons/round-17.md:22` quote exact;
  `K02InputCreditHoles.md:24` hole-1 text exact ("no binding to traces or to
  the section's commands"); `measure.py` argv grep → only `:773` (fixture),
  `:1462` (`main(argv)`), `:1483` (`parse_args`) — claim that `trace_reason`
  (`:368`) never reads receipt argv/page commands is **true**. Closed holes
  verified: `:517` `commands-unrecorded`, `:82-84` overlay whitelist,
  `:184` `cat-file blob`. Spot-check G5 row is at line 324 ✓.
- Captured-by `partial`: wave-2 catch verified (`round-17.md:81` "G5 claimed
  K02 hole 2 closed — wrong"); QUALITY 24 (`:136-140`) sweep clause confirmed
  — but see F0: at read rev the breadth tie is captured by QUALITY 33.
- Fix demonstrability: **weak**. The erratum half landed
  (`round-17.md:100-105` correction item 1 narrows :22 — verified). The argv
  binding half has **not landed**: `.ufo/evidence/round-18/measure.py` still
  has argv only at `:789`/`:1516`/`:1539`; `trace_reason` (`:373`) unchanged.
  The falsifier's red-before needs a fixture (receipt inputs ⊆ trace, argv
  unrelated to entry commands) that is **not a committed artifact** — it is
  constructible and cheap, but nothing committed embodies it. The row is
  honest that "until that check exists, the `:22` wording stays wrong" —
  which is itself the admission that the fix is shown-able-to-fail only in
  prose.

### Row 2 — 7 survivors, no killing test. STRONGEST on the fix axis.
- All seven survivor citations verified at exact lines:
  `MutateDispositionV2.md:54` G3Commit "survived; non-equivalent", `:58`
  G5Mode "survived; non-equivalent"; `MutateRegistryCheck.md:52` M06
  "**survived**", `:53` M07 "**survived**"; `MutateTraceInputs.md:52` M01
  "**Survived**", `:54` M03, `:55` M04; `round-17.md:87` "Open, named, not
  closed by prose" ✓.
- Captured-by: QUALITY 17 (`:77`) and 22 (`:116`) characterized correctly —
  but "none" is false at read rev per F0 (QUALITY 29).
- Fix demonstrability: **best in the doc**. `defect-probes.py` P01–P07 map
  one-to-one onto the seven survivors (`:54-98` guard specs verified). Both
  falsifier directions are committed receipts:
  `c2-probes-v2-183f87b.txt:1-7` all `open` (mutant_exit=0, pristine 0 —
  "seven open is the red-before" ✓) and `c2-probes-v2-e08271a.txt:1-7` all
  `closed` (mutant_exit=1; `DEFECT_PROBES: open=0 closed=11 total=11`).
  Minor blemish: row 2 does not cite QUALITY 29 or the probe receipts as the
  capturing artifact — its own falsifier was already executed.

### Row 3 — unexecuted exit contract. STRONGEST overall (honest + demonstrated).
- Pointers verified: `input-keyed-coldread-credit.md:75` "2 rev/blob/ledger
  missing" exact; `measure.py:546-552` `no-ledger` branch ✓; selftest
  `exit0-no-ledger` at `:940` ✓ (not :941 — line 940 holds the `check`
  call); `KnowledgeEntryReview.md:54` documents both exits; `round-17.md:94`
  admission ✓.
- Captured-by `none`: QUALITY 1 (`:3`), 7 (`:18`), 10 (`:27`)
  characterizations all accurate; no criterion requires executing a claim's
  exit line before admission. **Honest** even under the F0 lens — 35 covers
  the erratum, not pre-admission execution, which is what the row claims.
- Fix demonstrated live (my runs in clone):
  `python3 .ufo/evidence/round-17/measure.py --repo $C --rev eb7838b…` →
  **exit 0**, `ledger_present:false`, `no-ledger:58` (admitted sentence false);
  `… --ledger-file /tmp/does-not-exist-ledger.json` → **exit 2** (erratum
  sentence true). The erratum itself is committed at
  `input-keyed-coldread-credit.md:77-95` ("Lines 1–75 are unchanged" — verified
  via diff). Both halves of "FAIL on admitted / PASS on erratum" shown able
  to fail by committed artifacts.

### Row 4 — wrong cross-reference.
- Verified: `round-17.md:24` "K02 hole 5: one edit would uncredit the whole
  page" exact; `K02InputCreditHoles.md:28` hole 5 = live-lane reads, `:30`
  hole 7 = over-invalidation by the page; spot-check G7 row at line 327 says
  the same ("Lesson's pointer to K02 hole 5 is wrong… the cited reasoning is
  hole 7") ✓.
- Captured-by `none`: defensible (see F0; 35 covers the correction, not the
  admission).
- Fix: committed at `round-17.md:103` (correction item 2, "pointer should
  read K02 hole 7"). Falsifier (cited hole's text names page/SHA → fail on
  hole 5, pass on hole 7) is demonstrable on committed bytes — hole 7's text
  names SKILL.md, hole 5's does not.

### Row 5 — stale count.
- Verified: `round-17.md:22` "(89/89 selftest)" exact; spot-check `:306`
  "round-17 measure | 94/94 | d25d3d04" and `:311-312` "earlier measure
  tally is 89, not the final 94" exact.
- Captured-by `none`: stale at read rev — QUALITY 35 (`:262-279`) extends 26
  to corpus prose and names "a count" (F0).
- Fix demonstrated live: `python3 .ufo/evidence/round-17/measure.py
  --selftest` → `MEASURE_SELFTEST: 94/94 pass`, exit 0, on bytes whose
  sha256 `d25d3d04cb26ca7c20ef…` matches the correction's pin
  (`round-17.md:100,104`); the "89 as final" claim fails against both the
  committed tally and this re-execution. The dated correction naming 89 (at
  eb7838b, sha f348adc3…) and 94 (at 183f87b, sha d25d3d04…) is committed
  at `round-17.md:104` — verified. This closes the row's own admission that
  94 was "not re-executed for this draft".

## Ranking
- **Strongest: row 3** — only row whose captured-by is honest at the read
  rev AND whose fix is shown able to fail by committed artifacts in both
  directions (executed above). Row 2 is strongest on the fix axis alone but
  damaged by the F0 captured-by falsehood.
- **Weakest: row 1** — captured-by claims "no criterion ties breadth to
  command coverage" while QUALITY 33 exists as that criterion; and its fix's
  falsifier needs an uncommitted fixture, making it the only fix not shown
  able to fail by a committed artifact today.

## Smallest safe correction
Append (never rewrite) a per-row clause: "Captured at admission: none/partial
as stated; captured now by QUALITY 33 (row 1), 29 (row 2), 35 (rows 4–5)" —
which also converts the doc from naming fixes to naming the criteria that
enforce them. Optionally commit row 1's red-before fixture so its falsifier
stops being prose.

## Commands run (all in `/tmp` clone at 01d586d…, `env -u GIT_*`)
- `sha256sum .ufo/evidence/round-17/measure.py` → `d25d3d04cb26ca7c20ef…`
  (matches `round-17.md:104` pin)
- `python3 .ufo/evidence/round-17/measure.py --selftest` → exit 0,
  `MEASURE_SELFTEST: 94/94 pass`
- `python3 .ufo/evidence/round-17/measure.py --repo $C --rev eb7838b…` →
  exit 0, `ledger_present:false`, `no-ledger:58`
- `… --ledger-file /tmp/does-not-exist-ledger.json` → exit 2
- `git show 183f87b…:corpus/QUALITY.md | grep -c 'killing selftest'` → 0
- `git diff 183f87b… HEAD -- .ufo/waves/round-17/
  .ufo/evidence/round-17/measure.py corpus/lessons/round-17-verifier-spotcheck.md`
  → no changes (all wave-17/base anchors valid at read rev)

Verdict: **partial** — evidence pointers and fixes are accurate and mostly
demonstrated by committed artifacts (rows 2, 3, 4, 5), but the `Captured-by`
column is systematically stale: it measures capture at the admission rev
while QUALITY 29/33/35 — committed alongside this doc — now capture rows 1,
2 and 5 verbatim, and row 1's fix additionally lacks a committed
failure-witness.
