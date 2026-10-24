# Round 35 verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_kfc)
date: 2026-10-24
lane-round: tameshi 35 · base `51d3f08073be65d3475cf0286042fc0dbe4c4a7d` · deciding `34fa5b0cfe909f3cde644676ead723256281dd05` · tip `5df962b32fec2c341df9757245a51a14176eb905`
report: `.ufo/reports/round-35/tameshi.md` @ fleet `712049b282479899d5af0280a02f0d3dbb1d4d56` (author `tameshi-shokunin`)

## Step-1 conformance

| Check | Result |
|---|---|
| Report committed by lane identity | pass — `git log --format='%an %H' -- .ufo/reports/round-35/tameshi.md` → `tameshi-shokunin 712049b282479899d5af0280a02f0d3dbb1d4d56`; pushed (`merge-base --is-ancestor 712049b origin/main`) |
| SHONEN heading, one line per box | pass — `## SHONEN`, 4 boxes, all `[~]` with resolvable pointers |
| Cited lane commits exist + ancestor of branch | pass — 12/12 cited hashes (`5df962b`, `34fa5b0`, `d16f9b5a`, `43aea03`, `7267738`, `f9df589`, `23bd903`, `7da6e07`, `691bb51`, `1fc6cb7`, `5829676`, `51d3f08`) all `git cat-file -e` OK and `git merge-base --is-ancestor <hash> master` OK |
| Lane repo clean + pushed | pass — `jj-lane.sh state` → `ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` empty |
| Prompt carries template contract | pass — dispatched `.ufo/prompts/tameshi-round-35.md` carries §§1–6 (MISSION/AXES binding, 1–3 claims, frontier, L2 floor, report contract, commit scope, hyaku addendum) |
| Marker test | real report, not a marker |

Defects named (status-neutral): none at step 1.

## Per-claim re-check

Which claims were re-measured vs evidence-verified: per PROTOCOL §Gate standard (Closure consequence) the two lane-owned counters (`c1-measure.py`, `c2-measure.py`) were **not executed**; their committed evidence was verified and plain independent measurements over committed bytes were run by this closure.

### C1 — capability acquisition `tools/tally-audit-v3.py` (depth surface, operability)

- Plain measurements (closure-run):
  - `git cat-file -e 51d3f08:tools/tally-audit-v3.py` → absent at base; present at `34fa5b0`. Matches before receipt `tool_present=0` / after `tool_present=1`.
  - `git show 34fa5b0:tools/tally-audit-v3.py | sha256sum` → `6188db16de045f29…` = receipt `tool_sha` and capability-row pin.
  - Runner identity: `git show {51d3f08,5df962b}:tools/mutate-and-run.sh | sha256sum` both `a7d3f2dd7d47511a…` — byte-identical base↔tip, matches counter `PIN_RUNNER`.
  - Self-test tally: `grep -c '^CASE ' .ufo/evidence/round-35/lessons/selftest-33.out` → 33; trailer `TALLY_AUDIT_V3_SELFTEST: 33/33 pass`.
  - Closure pin re-check re-derived: all six pinned paths at tip hash to the receipt's digests (`pins.stdout` agrees).
- Evidence-verified (committed receipts, verbatim against report): before `C1_R35: mode=before tool_present=0 runner_sha_ok=1 … PASS=false` exit 1; do-nothing v2 control `pub_kill=0/6 pub_accept=0/3 … PASS=false` exit 1 at `5829676d`; deciding run `pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 … PASS=true` exit 0 at `34fa5b0`. Deciding receipt carries 16 COPY lines = 9 public + 7 holdout, matching the tallies. Frozen inputs: sealed manifest + per-copy sha256 committed; revision measured is named in every receipt line.
- Verdict: **verifies** (capability admitted; evidence-verified gate + closure re-measurement of every pin).

### C2 — self-assessment conformance, six classes (calibration)

- Receipts verified verbatim: before `m1=8 m2=3 m3=1 m4=1 m5=1 m6=1 total=15 entries=40 sources_rows=98 … PASS=false` exit 1 (per-class MISMATCH lines all present); after `m1=0 … total=0 … sources_rows=99 … PASS=true` exit 0 at `34fa5b0`.
- Hand re-derivation by this closure at tip `5df962b` (plain greps over committed bytes):
  - m1: all three knowledge files carry `source:`/`verified-at:`/`recheck:` (closeout-r11, survivor-fixture-minimization, witness-equivalence-rule).
  - m2: `corpus/README.md` rows exist (lines 48, 482, 483).
  - m3: `.ufo/waves/round-34/w1/ReviewDevReceipts.md` in lane tree (blob `5006bb7…`); no fleet-root copy (`ls` fails; fleet `git status` clean of it).
  - m4: `.ufo/evidence/round-35/pin-reconciliation.json` records the `9dbbce62…→7b11ba25…` re-pin of the round-33 contract.
  - m5: `# ROUND-35 ADJUDICATION` block present in `.ufo/evidence/round-34/dev/authoring.stdout` (records PanelSeed4 F1, JSON_IS_RIGHT).
  - m6: standing sources-registry cell replaced by re-derivable command (SCORECARD line 1609: `grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md` → 99).
- Verdict: **verifies** (15 → 0 re-measured by hand; receipts verbatim).

### Numeric guardrails

- depth: command D re-run by closure at base/tip/final — `recorded_cases=9 depth_score=9` at `51d3f08`, `34fa5b0`, `5df962b` → **unchanged** as declared.
- calibration: strict cold-read monitor `.ufo/evidence/round-21/coldread/measure.py` re-run by closure: `calibration_restraint_score: 8, sections_covered 64/64` at base; `6, 60/64` at tip → matches report; decline is the instrument's input-drift rule applied to four headings this round's own repairs rewrote; disclosed in SCORECARD + lesson Holds; refresh routed to round 36. Not a harm: it is a measured, disclosed, mechanical withholding, and C2's verified 15→0 is the calibration axis move.

### No axis harmed

`git diff 51d3f08 5df962b --stat` over SCORECARD/LOG/SOURCES/README/QUALITY/SKILL/PROVINCE: LOG +50, SCORECARD +61/−1 (the −1 is the declared m6 standing-cell repair), README +13, SOURCES +11; SKILL.md, PROVINCE.md, QUALITY.md untouched. The single SCORECARD deletion is the m6 repair the declared claim requires (cell records the correction provenance inline).

## Discernment spot-check (LEARNING.md — checked from outside)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S102 admit (POSIX.1-2024 §2.3 Token Recognition) | admit | committed snapshot `.ufo/evidence/round-35/src/s102-posix-chap02.html` + SOURCES row 110 | agree | sha256 `0889867a…` and 357,953 bytes match the Gate record; located quote found verbatim at snapshot line 303 (`<tt>` stripped); quote is 25 words; row well-formed, status `mined`, used-by names the tool + lesson |
| gnu.org Bash manual Comments page | reject (no row) | `curl -m 60 https://www.gnu.org/software/bash/manual/html_node/Comments.html` | agree | curl exit 28, connection timed out at 60.00 s — the recorded timeout reproduces; writing no row was correct |
| Census | — | `scripts/sources-census.sh validate --root … tameshi` | agree | exit 0, final line `tameshi ok …/corpus/SOURCES.md` (W04 duplicate-url warnings + W01 tier notice are warnings, not failures) |

Misroot sweep (closure-run): `git -C fleet status --porcelain` untracked set (`bm.json live.html live_s228.html nama.html s395.txt tf_bavelas.html unblob.log wb2.html write AGENTS.md xc.xml .omp/mcp.json` + script backups) — `grep -il tameshi` over all of them exit 1; only `.ufo/state/tameshi.report-baseline` matches (driver state file, untouched). Agrees with the report.

## Trend verdicts (closure assessment)

- **expansion: improved** — SOURCES rows 98 → 99 re-measured (`git show {51d3f08,34fa5b0}:corpus/SOURCES.md | grep -c '^| S[0-9][0-9][0-9] |'`); S102 tier A, status mined, snapshot pinned; `tools/tally-audit-v3.py` docstring lines 29–31 cite S102 + S097 (sourced-claim requirement met); capabilities-table row admitted.
- **quality: improved** — deciding receipt (evidence-verified): 6/6 public must-kill + 4/4 sealed must-kill failing exactly `runtime`, 3/3 + 3/3 accepts, 0 invalid; v2 do-nothing control 0/6 + 0/3 cannot reach the target; the two r34 structural classes (unswept `(0,0)`/`(1,1)` configs; comment text seizing head/brace/`esac` locators) are covered by named panel + sealed copies.
- **discernment: improved** — C2 15 → 0 verified by receipts and by this closure's hand re-derivation of all six classes; five mistakes mined with captured-by criteria; the sixth catch (census-invariance prose vs receipts, LOG "unchanged (99)" → corrected "98 → 99") is disclosed as a seventh undeclared class with the LOG correction landed in-round.

## Routed defects for round 36 (lane must fix)

1. **Dead evidence pointer (closure-found):** LOG.md round-35 entry cites `ResidualSentinelClosure.md` ("the residual sentinel seat … was respawned by the closure") — no such file exists anywhere in the lane (`git log --all -- '*ResidualSentinel*'` empty; residual dir holds only the 5 committed reports). Commit the file or append a correction naming the real artifact.
2. **Counter PASS cardinality** (`c1-measure.py:517`): PASS does not assert slot totals 6/3 or `pub_distinct==9`; receipt meets the stronger target; successor counter with public-slot cardinality + distinctness asserts, frozen pre-data (already routed by the lane's own residual critic — confirmed disclosed in SCORECARD + lesson Holds).
3. **`code_view` not universal after ANSI-C `$'…'` quotes** (residual critic MAJOR; wave-2 AttackQuotedHash): claim stays scoped to the 16 enumerated copies; real lexer or supported-form list routed (already in lesson Holds).

No SHONEN box is independently checkable by a non-author beyond the lane assertions recorded (`[~]` rows carry pointers; boxes remain operator-owned for promotion).
