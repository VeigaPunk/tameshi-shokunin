# ResidualScoutRecords — round-35 record inventory

Tip `34fa5b0cfe909f3cde644676ead723256281dd05` (`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse master`). `d16f9b5^` = `51d3f08073be65d3475cf0286042fc0dbe4c4a7d`. `git log --format='%h' 51d3f08..master | wc -l` → 12. No tools installed.

## Commits

`git log --name-status --format='COMMIT %h %s' 51d3f08..master` (newest first). One line each:

| commit | carries |
|---|---|
| 34fa5b0 | A8 receipt re-run only: replaces `control/c1-v2-control.stdout`, adds `control/c1-v3-public-rehearsal.stdout`. Not the deciding receipt. |
| 5829676 | A8 pins: `c1-measure.py` `TOOL_SHA256` → A7 tool bytes, `FREEZE_REV` removed, `contract.json`; plus 54 `w2/*.md` (diff-tree 56 paths). |
| 3168749 | pre-A8 control stdout + `lessons/selftest-33.out`. |
| 691bb51 | A7 batch + sealed set + lesson: tool, counter, contract, `c1/sealed/` (8 paths), `panel/root-keyed-shape6.json`, `corpus/lessons/round-35.md`. |
| 68f2557 | A6-bytes control stdout only. |
| f9df589 | A6: counter `TOOL_SHA256` re-pin + contract pins. |
| 1fc6cb7 | wave-2 machinery (5 files): `dispatch-w2.json`, `spec-w2.json`, `validate-w2.stdout`, `validate-w2.stderr`, `w2/swarm-registry.json`. |
| 7da6e07 | A4/A5 receipt re-run: contract + control stdout. |
| 23bd903 | A5: counter `run_block` auto-root interpolation + contract re-pin. |
| 7267738 | A4/A5 tool+counter, two panel copies, both census receipts, 6 inherited `w1/` reports. |
| 43aea03 | v1 wave (spec/dispatch/validate/registry) + `after/c2-at-d16f9b5a.stdout` + inherited r34 `PanelSeed4.md`. |
| d16f9b5 | adds `tools/tally-audit-v3.py`, `contract.json`, both counters, panel, before receipts, S102 snapshot, SOURCES row, C2 repairs. |

Named carriers: v3 tool added `d16f9b5`, modified `7267738`, final A7 bytes `691bb51` (A8 does not touch the tool). Contract added `d16f9b5`, amended `7267738` `23bd903` `7da6e07` `f9df589` `691bb51` `5829676`. Sealed set `691bb51` only (`git ls-tree --name-only 691bb51 .ufo/evidence/round-35/c1/sealed/` → 7 json + `manifest.json`). Wave-2 evidence split: machinery `1fc6cb7`, 54 seat reports `5829676`. A7 batches = `691bb51` (one commit; `grep -n batch .ufo/evidence/round-35/contract.json` → `contract batch: no matches`; lesson A7 text `corpus/lessons/round-35.md:64-71`). A8 = `5829676` (pins) + `34fa5b0` (re-run receipts).

VERDICT: 12 commits; carriers named above.

## Untracked

`git status --porcelain` (re-run just before this file; `residual/` was empty):

| path | column |
|---|---|
| `.ufo/evidence/round-35/after/c1-at-34fa5b0cfe909f3cde644676ead723256281dd05.stdout` | MUST-COMMIT |
| `.ufo/evidence/round-35/after/c1-at-34fa5b0cfe909f3cde644676ead723256281dd05.stderr` | MUST-COMMIT |
| `.ufo/evidence/round-35/after/c1-at-34fa5b0cfe909f3cde644676ead723256281dd05.exit` | MUST-COMMIT |

`cat` of `.exit` → `0` (2 bytes). stderr 0 bytes. stdout 2075 bytes; last line `C1_R35: mode=deciding tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=34fa5b0cfe909f3cde644676ead723256281dd05 C1_R35_PASS=true`. No other porcelain entry. This report is written after that status.

VERDICT: three MUST-COMMIT deciding-run receipts; zero NOT-MINE.

## Bookkeeping

| check | result | command and output |
|---|---|---|
| (a) `Round 35` section | ABSENT | `grep -n 'Round 35' SCORECARD.md` → `SCORECARD Round 35: no matches` |
| (a) move-log row | ABSENT; not a closeout write | `grep -nE '^\| 35 \|' SCORECARD.md` → no matches. `## Move log` is lines 7–24 and the last row is round 11. Line 60: "The historical move log above predates this fleet round." Rounds 12–34 are `## Round N` sections. |
| (b) LOG.md entry | ABSENT | `grep -nE 'Round 35\|round-35' LOG.md` → `LOG round-35: no matches`. Last heading `## Round 34` at line 1820. |
| (c) lesson | PRESENT | `grep -n '^##' corpus/lessons/round-35.md` → `11:## What this round attacked, and why`; `30:## The change — tools/tally-audit-v3.py (new file; v2 untouched)`; `48:## C1 counter and its controls (frozen before data)`; `73:## C2 — self-assessment conformance (measured)`; `89:## Gate`; `100:## Mistakes`; `133:## Holds (routed to round 36)`. |
| (d) census receipt | PRESENT, `exit=0` | `tail -n 2 .ufo/evidence/round-35/after/census-at-round-end.stdout` → `tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md` then `exit=0`. File added in `7267738`. |

`grep -n 'round 35' SCORECARD.md` hits only line 1609 (sources-registry cell, "99 rows at round 35") and line 1666 (`**Planned (round 35):**` inside `## Round 34`). `grep -n tally-audit-v3 SCORECARD.md` → no matches.

VERDICT: section and LOG entry are the missing closeout writes. Lesson and census receipt are present. Do not add a move-log row.

## S102

Full row `corpus/SOURCES.md:110`:

`| S102 | POSIX.1-2024 Shell Command Language, §2.3 Token Recognition — https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html | spec | A | the normative rule that makes a `#` start a comment and where the comment ends | §2.3 Token Recognition, the `#` sentence @ page fetched 2026-10-23 UTC (357,953 bytes; SHA-256 0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd; committed snapshot .ufo/evidence/round-35/src/s102-posix-chap02.html) | a `#` at the point a token begins discards that character and all up to (excluding) the next newline as a comment, so comment text is never code — the ground for blanking comments before structural scans | mined | 2026-10-23 | 365d | tools/tally-audit-v3.py, corpus/lessons/round-35.md |`

URL matches lesson Gate `:92`. Snapshot `:25-26` is Issue 8 / IEEE Std 1003.1-2024, title `Shell Command Language`. `grep` of the absolute URL inside the snapshot → no matches (relative nav only). Live HTTP fetch: not run. Access date: anchor `page fetched 2026-10-23 UTC`, opened column `2026-10-23`. `sha256` of the snapshot = `0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd`, 357953 bytes (matches the row). Located quote (lesson `:94-96`, 25 whitespace tokens): `If the current character is a '#', it and all subsequent characters up to, but excluding, the next <newline> shall be discarded as a comment.` One hit, byte offset 20770, span through `comment.` ends 20925 (HTML has `<tt>'#'</tt>` and `&lt;newline&gt;`). used-by names `tools/tally-audit-v3.py` (and the lesson). Tool docstring `:29` cites S102.

VERDICT: S102 row conformant; quote at offset 20770; used-by names the v3 tool.

## Census

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi; echo EXIT=$?`

```
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S048 duplicate url pitest.org/quickstart/incremental_analysis across scopes
tameshi	W04	S075 duplicate url man7.org/linux/man-pages/man1/strace.1.html across scopes
tameshi	W04	S076 duplicate url docs.jj-vcs.dev/latest/git-compatibility across scopes
tameshi	W04	S077 duplicate url man7.org/linux/man-pages/man2/PR_SET_CHILD_SUBREAPER.2const.html across scopes
tameshi	W04	S078 duplicate url man7.org/linux/man-pages/man2/open.2.html across scopes
tameshi	W04	S081 duplicate url bazel.build/reference/test-encyclopedia across scopes
tameshi	W04	S092 duplicate url bazel.build/remote/caching across scopes
tameshi	W01	S101 tierC mined used-by=corpus/knowledge/witness-equivalence-rule.md
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
EXIT=0
```

Same ten script lines as `census-at-round-end.stdout`; that file's extra last line `exit=0` is the recorded status.

VERDICT: census EXIT=0.

GAPS: commit `.ufo/evidence/round-35/after/c1-at-34fa5b0cfe909f3cde644676ead723256281dd05.{stdout,stderr,exit}`; write SCORECARD `## Round 35` (no `tally-audit-v3` string exists in SCORECARD.md); write the LOG.md round-35 entry. Do not add a move-log row.

SEAT: ResidualScoutRecords model=xai-oauth/grok-4.7-build-fast
