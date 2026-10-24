# SimplifierSCORECARDRow — round-36 SCORECARD citation audit (read-only)

Seat: SimplifierSCORECARDRow (godspeed w1, leaf; no subagents spawned). Attack surface: every
numeric/hash/filename citation in `SCORECARD.md` lines 1731–1776 (`## Round 36 — cold-read refresh
(calibration 6 → 8) + counter cardinality successor (depth surface) (2026-10-24)`), checked against
its receipt at the refresh commit. No files edited; read-only git only (`rev-parse`, `log`,
`show`, `status`).

## Revisions
- working tip (receipts commit): `d9c496b19371b779ce0eec6dfee1b049b27a3a2d` (clean)
- refresh commit (C1/C2 measurement commit): `b455001e2589b3f4f471d94a3de7e5e549b9f54c`
- round-36 content commit (do-nothing control): `e423c41ba253357ab8c8513f0376dad9d38ab248`
- r35 tip / C1 base: `796e08b888849308d0c4d5e932e56833600a139f`

## Verdict line
**VERDICT: citations resolve with 2 literal-citation failures (both receipt-naming/quote-level, no
numeric conflict), 1 cosmetic quote truncation. All scores, hashes, row counts and exit codes in the
Round 36 block match their receipts.**

## Citations that do NOT resolve (or quote-level mismatch)

1. **C1 evidence cell — control receipt filename `control/monitor-at-content-commit.*` does not
   exist.** The block (line ~1746, parenthetical inside the Evidence cell) cites
   `.ufo/evidence/round-36/control/monitor-at-content-commit.*`; the committed receipts are
   `control/monitor-at-e423c41b.{stdout,stderr,exit}`. `e423c41b` IS the round-36 content commit
   (subject "round-36: content — …"), so the citation resolves semantically but the literal filename
   is a word-substituted placeholder (the same block uses explicit `<rev>` placeholders elsewhere).
   `LOG.md:1918` repeats the same generic name. Substance verified: that receipt prints
   `calibration_restraint_score: 6`, `sections_covered 60/64`, exit 0.
2. **C2 after cell — quoted token `pub_kill_slots=0` appears in no receipt.** The block quotes
   `C1_R36V2: … pub_kill_slots=0 … C1_R36V2_PASS=false` against
   `control/v2-at-emptypanel.stdout`; that receipt contains zero occurrences of `pub_kill_slots`
   (grep count 0). Its actual line is `C1_R36V2: … pub_kill=0/0 pub_accept=0/0 pub_slots=0
   pub_distinct=0 … C1_R36V2_PASS=false` (exit 1). `pub_kill_slots` exists only as a variable in
   `c1-measure-v2.py` (`:470`, never printed; format string `:547` prints `pub_slots=%d`). The
   zero-slot substance is true via `pub_slots=0`, but the quoted fragment does not resolve against
   its cited receipt — a misquote.
3. **Cosmetic (quote truncation, not a conflict):** the numeric-axes paragraph quotes the protocol
   scope line starting at "input-keyed source reads only; …", dropping the leading `L1-author `
   prefix without ellipsis. The "carried verbatim" claim itself holds: the full line
   `L1-author input-keyed source reads only; not independent/blind cold-read, recipe re-execution or
   required-command coverage` appears verbatim in `round-36/coldread/refresh-receipts.json`
   (`:3` and per-receipt) and `refresh-specs.json:3`, matching the round-21 protocol spec
   (`round-21/coldread/refresh-specs.json:3`).

## Citations verified (all resolve at the refresh commit)

| Citation in Round 36 block | Receipt / check | Result |
|---|---|---|
| contract `.ufo/evidence/round-36/contract.json`, frozen pre-data; C2 counter sha `9eb8944c…` recorded there | file exists; `contract.json` records `9eb8944c2541…`; `sha256sum` of `round-36/c1/c1-measure-v2.py` = `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53` | MATCH |
| C1 before `calibration_restraint_score: 6, sections_covered 60/64` at r35 tip `796e08b`, receipt `after/monitor-at-796e08b.stdout` | receipt JSON: score 6, `sections_covered: 60`, `sections_total: 64`, `"revision": "796e08b8888…"`; `exit=0`; `796e08b` is the commit before the round-36 content commit | MATCH |
| C1 after target `8, 64/64` at the refresh commit, hash named in `monitor-at-<rev>.stdout` filename | `after/monitor-at-b455001e.stdout`: score 8, 60→64 covered of 64, `"revision": "b455001e2589…"`; `exit=0` | MATCH |
| Evidence: `coldread/` traces `traces/L1/` (four), `refresh-specs.json`, `refresh-receipts.json`; four new ledger entries in `round-21/coldread/ledger.json`; lesson `corpus/lessons/round-36.md` | all present (`traces/L1/source-{1..4}.json`); ledger entries 493 @ `e423c41b` → 497 @ `b455001e`/tip (exactly +4; `refresh-receipts.json` self-reports `entries_added: 4`, `original_entries_retained: 493`); lesson exists | MATCH |
| Do-nothing control still prints 6 at the content commit | `control/monitor-at-e423c41b.stdout`: score 6, 60/64, `"revision": "e423c41ba2…"`; `exit=0` | MATCH (filename issue ⇒ item 1) |
| C2 before: v1 on emptied panel `C1_R35: … pub_kill=0/0 pub_accept=0/0 … C1_R35_PASS=true`, exit 0, `control/v1-at-emptypanel.stdout` | receipt line exactly as quoted; `V1_EXIT=0` | MATCH |
| C2 mutant: v2 fails it (`C1_R36V2_PASS=false`, exit 1), `control/v2-at-emptypanel.stdout` | `C1_R36V2_PASS=false`, `V2_EXIT=1` | MATCH except quoted `pub_kill_slots=0` token (item 2) |
| C2 deciding: `pub_kill=6/6 pub_accept=3/3 pub_distinct=9 … C1_R36V2_PASS=true`, exit 0, `after/c1v2-at-<rev>.stdout` | `after/c1v2-at-b455001e.stdout:17`: `pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 … rev=b455001e2589… C1_R36V2_PASS=true`; `EXIT=0`; 6+3+4+3 = 16/16 verdicts (Delta cell "16/16 re-confirmed" holds) | MATCH |
| Counter frozen targets 6/3/9 | `c1-measure-v2.py` `PUB_KILL_SLOTS_TARGET/PUB_ACCEPT_SLOTS_TARGET/PUB_DISTINCT_TARGET` asserted in the PASS expression (`:539-541`) | MATCH |
| Parent v1 counter unchanged | `git show b455001e:.ufo/evidence/round-35/c1/c1-measure.py` sha = `d360a159a1ad…` = worktree = r35 capability-table citation | MATCH |
| Pre-data controls committed under `control/` | 5 stdout/stderr/exit triples present | MATCH |
| depth 9 → 9; command D prints `recorded_cases=9 depth_score=9` at the refresh commit | `after/depthD-at-b455001e.stdout` = `recorded_cases=9 depth_score=9` | MATCH |
| runner byte-identical `a7d3f2dd…` | `git show b455001e:tools/mutate-and-run.sh` sha = worktree sha = `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` (also equals the frozen-artifacts pin) | MATCH |
| calibration pinned 6 at round 35 (lowest axis) | r35 block measures `calibration 8 → 6` at tip `34fa5b0`; consistent | MATCH |
| Routed repair: LOG round-36 correction names the five real residual reports | LOG names `ResidualCriticPredicate.md`, `ResidualReviewC2.md`, `ResidualReviewReceipt.md`, `ResidualReviewSealed.md`, `ResidualScoutRecords.md` — all five exist under `.ufo/waves/round-35/residual/`; `ResidualSentinelClosure.md` confirmed absent repo-wide | MATCH |
| S103 opened and mined | `corpus/SOURCES.md:112` row S103; snapshot `.ufo/evidence/round-36/src/s103-git-hash-object.html` sha `dd826daeeacaea01858ab1330e6f014ed1a0741652e5a710c578d137711f6100` = contract `new_source_row` = SOURCES/LOG claims; size 29,933 bytes as stated | MATCH |
| Measured commit "hash named in the … receipt filename and the round-36 report" | `monitor-at-b455001e.stdout` / `c1v2-at-b455001e.stdout` filenames and the w1 seat reports (`ExecMonitorAfter.md`, `ExecControlCensus.md`, `ScoutCitedInputs.md`, …) all name `b455001e2589…` | MATCH |

## Exact commands run (read-only)
```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --oneline -6
git -C … rev-parse 796e08b e423c41b b455001e d9c496b
git -C … status --short                                   # clean
sha256sum tools/tally-audit-v3.py tools/mutate-and-run.sh \
  .ufo/evidence/round-36/c1/c1-measure-v2.py .ufo/evidence/round-35/c1/c1-measure.py
git -C … show b455001e:tools/mutate-and-run.sh | sha256sum
git -C … show b455001e:.ufo/evidence/round-35/c1/c1-measure.py | sha256sum
git -C … show <rev>:.ufo/evidence/round-21/coldread/ledger.json | python3 -c
    'import json,sys;print(len(json.load(sys.stdin)["entries"]))'   # revs: e423c41b b455001e d9c496b
grep -o 'sections_covered[^,}]*' /"sections_total"/revision fields of the three monitor receipts
grep -c 'pub_kill_slots' .ufo/evidence/round-36/control/v2-at-emptypanel.stdout \
                          .ufo/evidence/round-36/after/c1v2-at-b455001e.stdout      # both 0
grep -n 'pub_kill_slots\|pub_slots\|pub_distinct' .ufo/evidence/round-36/c1/c1-measure-v2.py
find . -name 'Residual*.md' -not -path './.git/*'
stat -c %s .ufo/evidence/round-36/src/s103-git-hash-object.html          # 29933
cat of the 7 exit receipts under after/ and control/
read of SCORECARD.md:1731-1776 (:raw), contract.json, refresh-receipts/refresh-specs JSON,
  affected-sections.json, corpus/SOURCES.md S103 row, LOG.md round-36 entry, monitor/c1v2/v1/v2
  receipt stdouts, depthD/census/sources-rows receipts
```
No monitor or counter was re-executed (committed receipts used as ground truth); no tools
installed or updated; `pacman` not used; no subagents; the only file written is this report.
