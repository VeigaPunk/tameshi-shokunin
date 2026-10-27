# T53W2ScribeSCORECARD — round-53 SCORECARD section draft (calibration)

Seat T53W2ScribeSCORECARD, round 53 wave 2, hyaku run 10, L1 TameshiR53a2. Item: draft the
round-53 `SCORECARD.md` section — the frozen-claims table (C1/C2, before/target from
`.ufo/evidence/round-53/before` + `contract.json`), the deciding-results table shape of rounds
49–51, and the Planned (round 54) paragraph from the lesson's open items. `SCORECARD.md` was
**not** written (seat bounds). Read-only over the lane; no git/jj mutation; no counter run; no
fixtures; no installs; no scratch tree (nothing needed, nothing left behind).

Everything below reads the lane through git objects at the freeze
`7d8aaac676cbcb6379f57659e7c3c4c12150a815` and the content commits `a41195dfc13a73958e4c5228ec196b28d03ded03`
(C\*), `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e` (C\*\*) and `6db1d220b337c35ff1e25bf9cfd74abc9db1498d`
(base), plus the committed receipts. Values I did not observe are marked `[INFERENCE]` or left as
placeholders; no value is copied from contract prose into a cell without the receipt that prints it.

## Checks run

| # | Command (lane root) | Observed | Used for |
|---|---|---|---|
| 1 | `python3` dump of `.ufo/evidence/round-53/contract.json` (claims, controls, kill_rule) | C1/C2 predicates, before cells, targets, 7 pre-registered controls, `cannot_see`, kill rule | table prose |
| 2 | `cat .ufo/evidence/round-53/before/coldread-precheck-at-tip.stdout`; `cat …exit` | last line `COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=6db1d220b337 cand_credited=45 lost=19 RED`; exit `1` | C1 before |
| 3 | `ls -la .ufo/evidence/round-53/{before,c1,c2,control,integrate}` | `before/` = one receipt pair; `control/` = `controls.py`, `break-fixtures.py`, `controls.stdout`, `.stderr`, `.exit`; `integrate/` = `rekey.py`; no `after/` | controls state |
| 4 | `cat .ufo/evidence/round-53/control/controls.stdout`; `.exit` | `CONTROL CTL_C1_BASE verdict=false PROBLEM lost-headings-missing-at-rev expected=false pass`; `CONTROL CTL_C2_BASE verdict=false T: 9/9 pass] cr47=rc=0 docs=stale-patterns=4 total=4 C2_R53_PASS=false expected=false pass`; `CONTROLS: total=2 pass=2`; exit `0` | do-nothing controls |
| 5 | `git grep -n -E 'dir\s*=\s*["'"'"']/tmp' 6db1d220 -- tools/` | nine matching lines across seven files (`bash-witness-study.py:1241`, `context-capture.py:27,1625`, `env-diff.py:61`, `evidence-disposition.py:2351`, `pin-disposition.py:706`, `registry-check.py:766,917`, `repeat-control.py:597`) | C2 before |
| 6 | `git grep -c -E 'dir\s*=\s*["'"'"']/tmp' 5b703c6f -- tools/` | exit 1, no match | C2 target surface at C\*\* |
| 7 | `git show 5b703c6f:SKILL.md \| grep -n 'registry-check\|env-diff' \| grep -i tmp` | rows at 1993, 2163, 2172 now name `$TMPDIR`; 2172 carries the round-53 CR47 clause | C2 docs state |
| 8 | `git show 5b703c6f:tools/env-diff.py \| sed -n '25,130p'` | `strict_scratch_root()` raises on a set-but-unusable TMPDIR; `profile_env` `/tmp/w/*` are bwrap-namespace paths (`--tmpfs /tmp`, `--bind tmp /tmp/w`) | rules out a false `/tmp` finding |
| 9 | `git show 5b703c6f:tools/registry-check.py \| grep -n 'gettempdir\|cannot create scratch\|TMPDIR'` | helper at 758–768, message `cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: %r (could-not-evaluate)` | C2 CR47 surface |
| 10 | `git show 7d8aaac6:.ufo/evidence/round-53/c1/lost-headings.json \| python3 -c 'import json,sys; print(len(json.load(sys.stdin)))'` | `30` headings; first two are `## Context gate classification and explicit exit classes — round 15`, `## Effective expectation reconciliation — round 14` | heading count |
| 11 | `git show 7d8aaac6:.ufo/evidence/round-53/c1/measure.py \| sed -n '1,30p'` | docstring step 2 says `the unique … directory 'rekey-r53-<c0>'`; verdict-line template says `rekeyed=K/19 readers=R/19` | item F5 |
| 12 | python re-hash of every `files` entry in `freeze.json` against `git show 7d8aaac6:` bytes | 8/8 OK (`contract.json 5fb52e4d2522`, `c1/measure.py da89149195b8`, `c1/lost-headings.json 069a680e8d93`, `c2/measure.py 1942cd8f9850`, `no-harm.sh e4e6b7ad803f`, `deciding-run.sh 585e166d4ab7`, `control/controls.py c5a37ca1ecd6`, `control/break-fixtures.py c80f5a8ca676`) | freeze integrity (my own check) |
| 13 | `git log -1 --format='%H %ci %s' 7d8aaac6 -- .ufo/evidence/round-53/control/controls.stdout` | `a36d3e514d6565f6dbcb14bf0f70ecc379521ecb 2026-10-27 10:10:29 -0300 round-53: phase-A controls scored at freeze bytes (2/2 as pre-registered), before wave 1`; `git merge-base --is-ancestor a36d3e5 7d8aaac6` → true | controls commit |
| 14 | `git log --format='%h %ci %s' -1` for `a41195d`, `5b703c6`, `7d8aaac`, `218bc6b`, `e62d997`; `git merge-base --is-ancestor 218bc6b5 e62d997` | `10:24:16` / `10:49:22` / `10:50:28` / `10:15:50` / `10:18:54`; ancestry exit 0 | item F1 |
| 15 | `git show 7d8aaac6:.ufo/evidence/round-53/freeze.json` (python) | `frozen_at` = `before any seat ran and before the fix pass`; `files` 8; amendments `[1,2,3,4,5,6]` | item F1 |
| 16 | python dump of `corpus/routed-defects.json` | 49 rows; `round: 50`; note `one row per item routed by the round-40..49 closure spot-checks…`; no `R52.*`/`R53.*` row; `git log -3 -- corpus/routed-defects.json` → newest `b28a978` (round 50) | item F7 / Planned |
| 17 | `git grep -n "round 52\|round 53" 5b703c6f -- LOG.md` | `LOG.md:2444 ## 2026-10-27 — round 52 (honest stop, run wrap-up)`, `LOG.md:2465 ## 2026-10-27 — round 53, attempt 2 (this round)` | R52.2 closed |
| 18 | `git ls-tree -r --name-only 5b703c6f -- .ufo/waves/round-52 .ufo/evidence/round-52/integrate \| grep -E 'w3.ready\|w3/\|build-readers'` | the four untracked items R52.4 named are committed | R52.4 closed |
| 19 | `for s in 'mkdtemp under /tmp' 'context-capture-selftest' 'tameshi-r12-repeat-control-selftest' 'bash-witness-selftest-private'; do git show 5b703c6f:SKILL.md \| grep -n "$s"; done` | first string absent; the other three now read `$TMPDIR` (2162, 2174, 1521) | critic C2-C fixed at C\*\* |
| 20 | `git status --porcelain`; re-read `git status --porcelain -- SKILL.md`; `git hash-object SKILL.md` vs `git rev-parse HEAD:SKILL.md` | a transient ` M SKILL.md` on the first read; on re-read no entry, `diff --quiet` exit 0, both blobs `d75af3ffbe5261a67bde46bd891128b8eb1b4c6d` | clean-tree gate |
| 21 | read `.ufo/waves/round-53/w1/T53W1CritClaims.md` (§C1-B, C1-C, C2-C) and `.ufo/waves/round-53/w2/T53W2RevContract.md` | wave-1 critic routes the 218bc6b5 receipt gap and the freeze-timing note; wave-2 review prints `KILL-RULE-HOLE` for the C1 provenance gate | prior art / draft limits |

## Holds (used by the draft, receipt-backed)

- The freeze manifest is self-consistent at `7d8aaac6`: every one of its eight recorded sha256 values
  re-derives from the committed bytes (check 12). `verify-freeze.stdout` in the evidence directory is the
  **earlier** run (`FREEZE e62d99711a0d files=8 amendments=5`), superseded by amendment 6. The deciding run does
  not run that script: it requires the frozen file set to be byte-identical between freeze and revision
  (`git diff --quiet "$FREEZE" "$REV" -- $FROZEN` → `FROZEN_UNCHANGED=1`), and the freeze-integrity re-run at
  `7d8aaac6` is a separate wave-2 check.
- Base is RED on the frozen floor: `cand_credited=45 lost=19 RED`, exit 1 (check 2).
- Both do-nothing controls behave as pre-registered: `verdict=false`, `expected=false pass`,
  `CONTROLS: total=2 pass=2`, exit 0 (check 4).
- The C2 target surface is empty at C\*\* (`git grep` for the predicate regex over `tools/` exits 1 with no
  match, check 6), and the two tools' SKILL rows plus the helper code carry the round-53 scratch-root semantics
  (checks 7–9). The `/tmp/w/*` literals in `env-diff.py` are sandbox-internal names, not host scratch (check 8) —
  they are **not** a finding.
- R52.2 and R52.4 are closed at C\*\* (checks 17, 18); R52.1 and R52.5 are this round's two claims.
- The transient ` M SKILL.md` was a stat-dirty entry, not content: the re-read shows a clean status and
  identical blobs (check 20). Recorded here so nobody re-reports it.

## Calibration items (statements that do not hold as written at the freeze)

Every item below is a non-hold with a command-backed reason; none changes a predicate, target or control.
Classes follow the cold-read vocabulary (stale-as-current, receipt/pointer mismatch, unsupported premise).

**F1 — stale-as-current provenance note in the operative freeze.**
Quote (`git show 7d8aaac6:.ufo/evidence/round-53/freeze.json`): `"frozen_at": "before any seat ran and before the fix pass"`.
Reason: that describes the first freeze, not this one. The operative amendment 6 (`7d8aaac`, 10:50:28) postdates
both content commits (`a41195d` C\*, 10:24:16 → `5b703c6` fix pass 2, 10:49:22), and amendment 5 (`e62d997`,
10:18:54) already descends from the first fix pass (`218bc6b`, 10:15:50;
`git merge-base --is-ancestor 218bc6b5 e62d997` → true). Both re-freezes were therefore taken with the fix
passes' damage visible, so "before the fix pass" is wrong for the current freeze in two ways: the 30-heading
scope postdates the first fix pass and the counter change postdates the second. The wave-1 critic reached the
same conclusion independently (`.ufo/waves/round-53/w1/T53W1CritClaims.md`, §C1-C defect 1). Fix: the draft
header states the amendment timing instead of repeating the string; the string itself is frozen bytes and needs
the next re-freeze.

**F2 — receipt/pointer mismatch in the C1 `before` cell.**
Quote (`.ufo/evidence/round-53/contract.json`, claims.C1.before): `cand_credited=34 lost=30 RED at the post-fix-pass candidate 218bc6b5 (the round's own edits, repaired by the same re-key) (before/coldread-precheck-at-tip.stdout, exit 1)`.
Reason: the cited receipt's bytes end at the base run (`cand=6db1d220b337 cand_credited=45 lost=19 RED`) and
`grep -rn 'lost=30' .ufo/evidence/round-53/` matches only `contract.json`; no committed receipt records the
218bc6b5 run. The value is receipted at C\* by a seat-report verdict line —
`C1_R53: rev=a41195dfc13a credited=34 lost=30 rekeyed=0/30 readers=0/30 total=32 C1_R53_PASS=false`
(`.ufo/waves/round-53/w1/T53W1RevCounters.md:9`) — not at 218bc6b5 and not as raw stdout. The draft therefore
cites the two states with their own paths and carries the attribution gap as errata; predicate and target unchanged.

**F3 — unsupported premise if the section claimed the full control set scored.**
Quote (`control/controls.stdout`): `CONTROLS: total=2 pass=2`; the frozen contract pre-registers seven controls
(claims.C1.controls four, claims.C2.controls three), and `control/controls.py` documents the other five as
phase B — `CR47) are phase B: they run against scratch fixtures built from the POST-FIX` and
`candidate bytes in integrate/break-fixtures.py, before wave 2.`
Reason: `control/` holds no phase-B receipt at my read time, and `deciding-run.sh` gate 0 checks only
`control/controls.stdout` and `control/controls.exit`, while the kill rule says "every pre-registered control
receipt". The draft names the phase-A receipt precisely and leaves the phase-B receipt as a placeholder; the
section must not print a "controls scored" count until that receipt is committed.

**F4 — the `CTL_C1_BASE` receipt does not display `lost=19`.**
Quote: `CONTROL CTL_C1_BASE verdict=false PROBLEM lost-headings-missing-at-rev expected=false pass`.
Reason: `controls.py` records `'verdict=%s %s' % (verdict, last)` with `last` = the counter's last stdout line,
and the c1 counter with `--explain` prints its `PROBLEM` lines **after** the verdict line, so the slice shows
the problem code, not the verdict fields. The counter itself does run the precheck arm at base (that arm is
first in `main()`), so `lost=19` is what the counter printed — it is the receipt that cannot show it. Class:
receipt display limitation, not a false contract statement; disclosed so the section does not lean on the
truncated line for a number it cannot print.

**F5 — stale-as-current docstring in the frozen C1 counter.**
Quotes (`git show 7d8aaac6:.ufo/evidence/round-53/c1/measure.py`): `Verdict line: 'C1_R53: rev=... credited=... lost=... rekeyed=K/19 readers=R/19 total=N C1_R53_PASS=true|false'` and `2. rekey   — at REV, find the unique .ufo/evidence/round-21/coldread/`.
Reason: the frozen heading file holds 30 headings (check 10), the code prints `rekeyed=%d/%d` over
`len(headings)`, and amendment 6 accepts one-or-more `rekey-r53-<rev>` directories — three ways the docstring
misdescribes the file's own behavior. Frozen bytes cannot be repaired without `FROZEN_UNCHANGED=0`; the draft
discloses it and routes it to the next re-freeze.

**F6 — C2's doc arm is narrower than its claim's wording.**
Quote (`git show 7d8aaac6:.ufo/evidence/round-53/c2/measure.py`): `FLEET_DOC_PATTERNS = [` with exactly
`re.compile(r'/tmp/tameshi-f5\.json')`, `re.compile(r'/tmp/tameshi-r21-envdiff')`,
`re.compile(r'mkdir -p /tmp/<lane>-r<round>')`, plus a sweep-recipe needle whose pattern text begins
`Scratch for a sweep:`.
Reason: the predicate says "SKILL.md names no /tmp scratch path for either tool", but the arm decides that on
four literal legacy needles; a stale row in any other form passes. At C\*\* the two tools' rows read `$TMPDIR`
(checks 7, 19), so the gap is latent this round, not active — it belongs in the section's limits, not as a
claim failure.

**F7 — the routed-defect ledger is last current at round 50.**
Quote (`corpus/routed-defects.json`): `"note": "one row per item routed by the round-40..49 closure spot-checks; statuses judged against the tree, evidence rules in .ufo/evidence/round-50/c1/measure.py"`, `"round": 50`.
Reason: newest commit touching the file is `b28a978` (round 50); there is no `R52.*` row, so the six items
`corpus/lessons/round-52-verifier-spotcheck.md` routes (R52.1–R52.6) exist only in that lesson. The Planned
paragraph cites the lesson file, and ledger currency becomes a round-54 item.

**F8 — the C2 `before` cell undercounts its own surface.**
Quote (contract, claims.C2.before): `dir="/tmp" hardcodes at tools/registry-check.py:766 and tools/env-diff.py:61 (plus SKILL.md /tmp invocations for env-diff and the sweep recipe)`.
Reason: at base, `tools/` matches the predicate regex at nine lines across seven files (check 5) — the sentence
is true but names two of the nine sites. The phase-A harness repeats the undercount —
`(do-nothing control: the two inherited dir="/tmp" hardcodes)` (`control/controls.py`) — so a reader of the
control receipt alone would also size the surface at two. The predicate's scope (all committed files under
`tools/`) is the stronger, correct one; only the before prose is partial, so the draft's cell quotes the grep
surface with its own path.

**F9 — the amendment note claims a record the frozen counter does not keep.**
Quote (`git show 7d8aaac6:.ufo/evidence/round-53/freeze.json`, amendment 6): `reader arm binds on section_sha256 at the measured rev only (cand recorded, not gated)`.
Reason: `git show 7d8aaac6:.ufo/evidence/round-53/c1/measure.py | grep -n cand` returns only the precheck's
`cand_credited` matches and the `cands` filename list; the reader loop reads `heading` and `section_sha256` and
nothing else, and prints no candidate. "Not gated" holds; "recorded" does not. Frozen bytes, so it is disclosed
here and in the draft header, and the note is corrected at the next re-freeze.

## Draft — round-53 SCORECARD section

<!-- Paste into SCORECARD.md after the round-52 section. Slots in <angle brackets> are filled by the L1 from -->
<!-- .ufo/evidence/round-53/after/ after the deciding run; nothing in those slots is to be typed from memory. -->

## Round 53 — cold-read re-key repair (calibration) + `tools/` scratch hygiene (operability) (2026-10-27)

L1 TameshiR53a2, hyaku run 10, attempt 2 (attempt 1 died at its first model call on a provider quota limit —
nothing to inherit; `.ufo/evidence/round-53/contract.json`, `corpus/lessons/round-53.md`). Two claims on
distinct axes, pre-registered with both counters, the control harnesses, the no-harm monitors and the deciding
script in `.ufo/evidence/round-53/contract.json`, frozen at
`7d8aaac676cbcb6379f57659e7c3c4c12150a815` (`.ufo/evidence/round-53/freeze.json`, amendments 1–6; every
recorded manifest hash re-derives at that commit —
`.ufo/waves/round-53/w2/T53W2ScribeSCORECARD.md` §Checks row 12). Base
`6db1d220b337c35ff1e25bf9cfd74abc9db1498d`. Calibration (8, the lowest non-retired numeric axis;
`contract.json` claims.C1.axis_score) carries C1; C2 repairs routed defect R52.5 (the scratch directive's
`/tmp` rule, `corpus/lessons/round-52-verifier-spotcheck.md`). The freeze is not one moment: amendment 5 (the
re-key scope extended to the frozen heading set)
froze before wave 1, and amendment 6 (`7d8aaac676cb`) changed the C1 counter to accept more than one
`rekey-r53-<rev>` directory and to bind reader JSONs by `section_sha256` alone — frozen after C\* `a41195dfc13a`
and C\*\* `5b703c6ff3ff`, before wave 2. (The amendment's note also says the reader candidate is "recorded, not
gated"; the frozen counter does not read a candidate — see `.ufo/waves/round-53/w2/T53W2ScribeSCORECARD.md` F9.)
The manifest's `"frozen_at"` string still reads `"before any seat ran and before the fix pass"`, which describes the first
freeze: amendment 5 already descends from the first fix pass (`218bc6b`), and amendment 6 postdates the second
(`.ufo/evidence/round-53/freeze.json`; the content order is `a41195d` → `5b703c6` → `7d8aaac`). Phase-A
controls were scored at the freeze bytes and committed at `a36d3e514d65`
(`.ufo/evidence/round-53/control/controls.stdout`, `.exit`: `CONTROLS: total=2 pass=2`); the five break-one
controls live in `control/break-fixtures.py` and their scored receipt is `<phase-B controls receipt>`.

| Claim | Axis | Before (CTL_0, freeze bytes) | Target | Counting command | Controls (freeze bytes) |
|---|---|---|---|---|---|
| **C1** the round-21 cold-read monitor credits every section at the measured revision against floor `ef19d8e1e7ba` (`cand_credited=64 lost=0 ok`, exit 0), and every heading frozen in `.ufo/evidence/round-53/c1/lost-headings.json` has at that revision a ledger entry in `.ufo/evidence/round-21/coldread/ledger.json` whose traces lie under `rekey-r53-<C0>/`, whose `read_rev` names `<C0>`, whose `wrong_expectations` and `blocking_gaps` are zero, plus a committed `.ufo/waves/round-53/` reader JSON whose `heading` matches and whose `section_sha256` equals the section bytes at that revision: `C1_R53_PASS=true` | calibration (8; surface: the frozen heading set — the contract's 19 round-52 inherited losses plus the 11 sections the round's own C2 and scratch-rule edits drifted; `contract.json` claims.C1) | `COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=6db1d220b337 cand_credited=45 lost=19 RED`, exit 1 (`.ufo/evidence/round-53/before/coldread-precheck-at-tip.stdout`, `.exit`); mid-state at C\* `credited=34 lost=30` with `C1_R53_PASS=false` (`.ufo/waves/round-53/w1/T53W1RevCounters.md`); do-nothing control prints `verdict=false` and passes as pre-registered (`.ufo/evidence/round-53/control/controls.stdout`) | `C1_R53_PASS=true` | `python3 .ufo/evidence/round-53/c1/measure.py --lane LANE --rev REV --work EMPTY_DIR` | `CTL_C1_BASE` false at base (`control/controls.stdout`); `CTL_C1_NOTRACE`, `CTL_C1_BADREADER`, `CTL_C1_WRONGREV` pre-registered against the candidate in `control/break-fixtures.py`, scored receipt `<phase-B controls receipt>` |
| **C2** no committed file under `tools/` at the measured revision matches `dir\s*=\s*["']/tmp`; `registry-check.py --selftest` and `env-diff.py --selftest` both exit 0 with `TMPDIR` bound to the counter's scratch; `registry-check.py --selftest` with a missing `TMPDIR` directory exits non-zero naming scratch creation and prints no verdict-bearing line; SKILL.md names no `/tmp` scratch path for either tool: `C2_R53_PASS=true` | operability (no numeric score; surface: the runnable tools under `tools/` and their documented invocations; `contract.json` claims.C2) | at base `6db1d220`, the predicate regex matches nine lines across seven files under `tools/` (`.ufo/waves/round-53/w2/T53W2ScribeSCORECARD.md` §Checks row 5); at C\*\* `5b703c6f` the same grep exits 1 with no match (same report, row 6); do-nothing control prints `docs=stale-patterns=4 total=4` and `C2_R53_PASS=false`, passing as pre-registered (`.ufo/evidence/round-53/control/controls.stdout`) | `C2_R53_PASS=true` | `python3 .ufo/evidence/round-53/c2/measure.py --lane LANE --rev REV --work EMPTY_DIR` | `CTL_C2_BASE` false at base (`control/controls.stdout`); `CTL_C2_TMP`, `CTL_C2_CR47` pre-registered against the candidate in `control/break-fixtures.py`, scored receipt `<phase-B controls receipt>` |

Errata to the frozen `before` prose and to the freeze note (predicates, targets and the kill rule unchanged).
The C1 `before` line attributes `cand_credited=34 lost=30` to the post-fix candidate `218bc6b5` but cites
`before/coldread-precheck-at-tip.stdout`, whose bytes carry the base run only; the value is receipted as a C\*
verdict line by `.ufo/waves/round-53/w1/T53W1RevCounters.md`, and no committed receipt records the 218bc6b5
run. The C2 `before` line names two of the nine `dir="/tmp"` sites the base tree carries under `tools/`
(`.ufo/waves/round-53/w2/T53W2ScribeSCORECARD.md` §Checks row 5). The phase-A receipt covers the two do-nothing
controls; the five break-one controls are phase B (`contract.json` claims.C1.controls and claims.C2.controls;
`control/break-fixtures.py`) and must be scored and committed before the deciding run, because the kill rule
requires every pre-registered control receipt.

What the counters cannot see (contract `cannot_see`, plus what the wave seats measured this round): C1 — whether
a fresh reader's finding is semantically fair (the wave-2 re-read and the non-author closure attack it), whether
the recorded inputs are the right citation set, and whether the fixed SKILL statements are true beyond the
frozen checks; the frozen counter's own docstring still declares the heading count as `19` and a **unique**
re-key directory while the frozen heading file holds 30 headings
(`.ufo/evidence/round-53/c1/lost-headings.json`) and amendment 6 accepts many
(`git show 7d8aaac6:.ufo/evidence/round-53/c1/measure.py`). The frozen provenance gate is also weaker than the
contract's wording — `rekey_prefix()` accepts an entry on one in-directory trace, and `read_rev` is checked by
string prefix, not commit identity (`.ufo/waves/round-53/w2/T53W2RevContract.md`: `KILL-RULE-HOLE`). C2 — whether
TMPDIR redirection truly isolates a run, tools and counters outside `tools/` (frozen `.ufo/evidence` counters
with `/tmp` are routed, not claimed), and hosts where TMPDIR itself is ignored; the docs arm decides "no /tmp
scratch path" from four literal legacy needles (`.ufo/evidence/round-53/c2/measure.py`), so a stale row in
another form would pass. The after values are
read from the deciding receipts under `.ufo/evidence/round-53/after/`, never from this table.

### Round 53 — deciding results (appended after the deciding run)

L1 TameshiR53a2, attempt 2 (attempt 1 died at its first model call on a provider quota limit).

- **Deciding run.** One invocation of `.ufo/evidence/round-53/deciding-run.sh` at content revision `<REV>`
  (freeze `7d8aaac6`), receipts `.ufo/evidence/round-53/after/`. The gate's requirements, not results: the
  frozen file set byte-identical between freeze and revision (`FROZEN_UNCHANGED=1`, `<after/frozen.stdout>`),
  every no-harm monitor `ok` with the gate's own count (`deciding-run.sh`:
  `[ "$(grep -c '^NOHARM .* ok$' "$OUT/no-harm.stdout")" = 12 ]`, `<after/no-harm.stdout>`), the frozen
  precheck's last line and exit (`<after/coldread-precheck.stdout>`, `<after/coldread-precheck.exit>`), census
  exit (`<after/census.exit>`), and the one-invocation and clean-tree witnesses
  (`<after/deciding-run.exit>` carries `DECIDING_RUN_EXIT=<rc>`).

| Claim | Axis | Before (CTL_0) | After (REV `<REV>`) | Delta | Verdict | Evidence |
|---|---|---|---|---|---|---|
| C1 | calibration (8) | `cand_credited=45 lost=19 RED` (`before/coldread-precheck-at-tip.stdout`) | `<after/c1.stdout verdict line, byte-exact>` | `<axis score from the deciding no-harm coldread-floor line; the surface moved or did not>` | `<verifies (measured) / does not verify (honest stop)>` | `after/c1.stdout`; `after/no-harm.stdout` coldread-floor |
| C2 | operability (no numeric score) | `docs=stale-patterns=4 total=4` (`control/controls.stdout`) | `<after/c2.stdout verdict line, byte-exact>` | `<the surface at C\*\*: tmp_hits, both selftests, cr47, docs — from the same line>` | `<verifies (measured) / does not verify (honest stop)>` | `after/c2.stdout` |

Numeric axes after: the deciding no-harm receipt `<after/no-harm.stdout>` (command D, coldread-floor and
r45-freshness lines, byte-exact); no axis value is typed here. Capabilities: none claimed this round — both
claims are axis moves (`contract.json` claims.C1.kind, claims.C2.kind). Limits: the items listed under "What the
counters cannot see" above, the frozen C1 docstring and `freeze.json` `"frozen_at"` string (frozen bytes, next
re-freeze), and the phase-B control receipt, which the kill rule requires but `deciding-run.sh` does not gate on.

**Planned (round 54):** the two routed items this round does not work — R52.3 (re-derive the round-52 over-count
verdict under one written counting rule, and decide whether a reviewer-seat quote-truncation criterion is
needed) and R52.6 (the report-contract repairs: per-box SHONEN lines, Landed changes and Before → after
sections, the false "not committed/pushed" sentence, trend vocabulary) — both in
`corpus/lessons/round-52-verifier-spotcheck.md`, and neither in `corpus/routed-defects.json`, whose newest
commit is round 50's, so bringing that ledger current is itself an item. The round's own records put further
items on the table: the frozen C1 docstring's `19` and "unique" wording and the `freeze.json` `"frozen_at"`
string, both fixed at the next re-freeze and not before (they are frozen bytes here;
`.ufo/evidence/round-53/c1/measure.py`, `.ufo/evidence/round-53/freeze.json`); the provenance hole the wave-2
contract review names — all traces of an
entry beneath exactly one accepted directory, `read_rev` compared to the resolved commit rather than a prefix,
and a break-one control for mixed trace sets (`KILL-RULE-HOLE`,
`.ufo/waves/round-53/w2/T53W2RevContract.md`) — which needs a re-freeze and a control, so it cannot land inside
this freeze; and the phase-B control receipt, if it is still missing when the deciding run is attempted. C1's
semantic half stays open by declaration: whether a fresh reader's finding is fair and whether the recorded
inputs are the right citation set (`contract.json` claims.C1.cannot_see). C2's successor should read each
tool's scratch helper instead of four literal needles and extend the doc sweep past the two tools, and still
cannot see TMPDIR-isolation or a host that ignores TMPDIR (`contract.json` claims.C2.cannot_see). §10 takes one
theme and its ranked entries per round (`corpus/lessons/round-53.md` §Gate): the next fit against the open
frontier rows is `r8-predictive-test-selection-cost.md`, then
`delta-debugging-minimization-contract.md`, and one `considerthese/2026-10-26.md` proposal may be mined. F7
stays `open`: the per-leg reuse classification is still unmeasured (`corpus/README.md`, round-53 addendum).

## Out of scope / not done

- **Handoff state of this file.** The wave-2 integration commit `ac52387` captured an intermediate copy of this
  report while it was still being edited (HEAD at handoff is `ac52387`). The final bytes are the working-tree
  version of `.ufo/waves/round-53/w2/T53W2ScribeSCORECARD.md`; this report is the only path this seat wrote.
  This seat makes no git mutation, so the L1 must commit these bytes; until then the tree is dirty and the
  deciding run's clean-tree gate will refuse (other dirty paths in `git status` at handoff belong to peer seats,
  not to this one).
- `SCORECARD.md` was not written or touched; the draft above is the deliverable. No lane file was edited besides
  this report, no git or jj mutation was made, no counter was executed, no tool was installed, no fixture or
  scratch tree was created (nothing under `/fast/scratch/hyaku/tameshi-r53/w2/T53W2ScribeSCORECARD` exists).
- I did not score any control or run either counter: the phase-B receipt, the deciding revision and the after
  cells are the L1's and the deciding run's to fill, and every such slot is left as a placeholder rather than a
  plausible number.
- The draft's `12/12` no-harm requirement is the frozen gate's own count (`deciding-run.sh`:
  `[ "$(grep -c '^NOHARM .* ok$' "$OUT/no-harm.stdout")" = 12 ]`), not an observation of this round.
- Not audited here: whether the 30-heading set is the semantically right re-key scope, the fairness of the
  wave-1 reader findings (wave-2 re-read seats), and the C2 selftest coverage claims (the deciding receipt is the
  evidence).
