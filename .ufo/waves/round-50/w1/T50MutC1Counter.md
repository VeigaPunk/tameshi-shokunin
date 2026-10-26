# T50MutC1Counter — mutation testing of the frozen C1 counter's selftest

Seat: T50MutC1Counter (L1 TameshiR50, wave w1). Target: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-50/c1/measure.py` (lane bytes untouched; sha256 `ceee320c9ad84c89a7846fd746a072a60758a465d25ff80343fb95e0bd88ae29`, re-verified at end — see Restoration). All work in scratch `/fast/scratch/hyaku/tameshi-r50/T50MutC1Counter/` (deleted before yield). Detector: the counter's own `--selftest` (builds a fixture repo and runs `measure()` end to end, 25 cases), run per the scratch directive: `TMPDIR=$S/w python3 measure.py --selftest --work $S/w/<tag>`.

## Method

1. Baseline: pristine copy passes `--selftest`: `cases=25 failed=0`, exit 0 (`T50MutC1Counter/baseline.txt`).
2. Phase 1 — 29 single-edit mutants (`T50MutC1Counter/mutant-diffs.txt`), each applied to a scratch copy and run against the unmodified selftest.
3. Phase 2 — for every phase-1 survivor, one killing case was appended to the selftest (extension `T50MutC1Counter/ext-measure.py`); the extended selftest passes 43/43 on pristine (exit 0), and each survivor run against it fails exactly its killing case (`T50MutC1Counter/ext_results.json`). So: 29/29 mutants killed by a selftest that reaches `measure()`; 18/29 killed only after the extension.

## Phase 1 results (mutant → selftest verdict)

Killed = existing case failed (case named). Survived = 25/25 ok. Lines refer to the frozen counter.

| Mutant | Area (line) | Verdict | Failing case |
|---|---|---|---|
| M03 ack check off | ACK_WORDS use, measure.py:246 | KILLED | ack line is not a fix |
| M08 key case-sensitive | key match, :117 | KILLED | good ledger passes (+11) |
| M10 routed_at `not` dropped | ancestry, :231 | KILLED | fix commit before routing refused (+7) |
| M12 touched-files off | :239 | KILLED | commit not touching evidence refused |
| M13 new-since-routing off | :242 | KILLED | excerpt present at routing refused |
| M20 extra counted as missing | :183 | KILLED | extra row counted |
| M22 spot-check hash `!=`→`==` | :165 | KILLED | good ledger passes (+6) |
| M23 STATUSES 'open'→'opens' | :49 | KILLED | good ledger passes (+9) |
| M24 decline length 40→4 | :262 | KILLED | short decline reason refused |
| M25 open/Planned check off | :257 | KILLED | open not in Planned refused |
| M26 key-miss check off | :223 | KILLED | unkeyed evidence refused |
| M01 drop 'planned' from ACK_WORDS | :54 | SURVIVED | — |
| M02 drop 'still open' from ACK_WORDS | :54 | SURVIVED | — |
| M04 HARD prefix check off | :128 | SURVIVED | — |
| M05 SOFT prefix check off | :130 | SURVIVED | — |
| M06 excerpt min length 15→1 | :137 | SURVIVED | — |
| M07 excerpt max length 400→4000 | :137 | SURVIVED | — |
| M09 key path-suffix match dropped | :117 | SURVIVED | — |
| M11 commit-ancestor-of-REV dropped | :231 | SURVIVED | — |
| M14 Planned pattern loosened | :102 | SURVIVED | — |
| M15 Planned paragraph bleed (break→pass) | :108 | SURVIVED | — |
| M16 FIXED_FLOOR 20→0 | :50 | SURVIVED | — |
| M17 DECLINED_CAP 12→99 | :52 | SURVIVED | — |
| M18 THIS_ROUND_FLOOR 5→0 | :51 | SURVIVED | — |
| M19 total sum→max | :268 | SURVIVED | — |
| M21 duplicate row not skipped | :188 | SURVIVED | — |
| M27 lines-range b<=len dropped | :146 | SURVIVED | — |
| M28 line() PASS token always 'true' | :284 | SURVIVED | — |
| M29 BASE constant corrupted | :272 | SURVIVED | — |

## Phase 2 — killing cases (all 18 survivors killed, extension pristine-clean)

Extension = pristine + 18 cases, inserted before selftest's `finally` (43 cases total). Pristine run: `C1_R50_SELFTEST: cases=43 failed=0` exit 0. Per survivor, `killed_by` is the case that fails (`ext_results.json`):

| Survivor | Killing case (new) | What it pins |
|---|---|---|
| M01 | planned-only ack is not a fix | an ACK span whose only acknowledgement word is 'planned' must refuse a fixed row |
| M02 | still-open-only ack is not a fix | same for 'still open' alone |
| M04 | existing instrument-path evidence refused | HARD path that EXISTS at REV with keyed excerpt is refused (old case only hit path-absent) |
| M05 | existing wave-path evidence refused | SOFT path without key-suffix refused even when file exists and excerpt keys |
| M06 | tiny excerpt refused | 9-char keyed excerpt refused |
| M07 | oversized excerpt refused | 457-char keyed excerpt refused |
| M09 | path-suffix key match accepted | a row keyed ONLY via `path.endswith(key)` must pass on pristine (mutant gives key_miss) |
| M11 | fix commit off REV history refused | fix commit on a side branch (valid object, touches path, not ancestor of REV) refused |
| M14 | stale planned line after paragraph refused | a later line containing 'Planned' and naming the id must not satisfy `open` |
| M15 | stale planned line… + trailing note past paragraph refused | blank line must end the Planned paragraph (id after it must not count) |
| M16 | default fixed floor enforced | `measure()` with default floors: fixed_short == 19 (fixed=1) — selftest never exercised the constants |
| M17 | default declined cap enforced at 13 declines | second fixture, 13 declined rows: default cap yields declined_over == 1 |
| M18 | default this-round floor enforced | default trf=5 with one post-base fix: this_round_short == 4 |
| M19 | two simultaneous terms sum into total | missing + pin: total == 2 (max() would say 1) |
| M21 | duplicate row never validated | duplicate row with status 'done' must stay unvalidated (mutant validates it: bad_status + fixed_short) |
| M27 | range past end with span 17 refused | b=20 > len=5 with b-a=17: must refuse (old case only hit span 38 > 30) |
| M28 | line() reports false when total>0 | output line must contain `C1_R50_PASS=false` when total>0 |
| M29 | BASE constant intact | structural: `BASE == 'e3729de862f73ae080d98fcf522a7081ce16e40a'` (a fixture repo cannot contain the real base commit, so the default-base path is not behaviorally distinguishable in-repo) |

Note: M19 is also caught incidentally by the new M11 case (pristine total=2 vs max=1); the dedicated case keeps it pinned independently.

## Findings

1. The frozen selftest reaches `measure()` end to end and kills gross mutations (status set, key check, evidence resolution, spot-check hash, decline/open thresholds), but 18/29 realistic single-edit mutants survive it — `show:` `grep -c SURVIVED T50MutC1Counter/run.log` → 18.
2. Gap classes the extension closes: (a) refusal cases that pass for the wrong reason — path-absent instead of excluded-path (:128/:130), span>30 instead of range-past-end (:146), 'carried' masking a dropped sibling ACK word (:54); (b) constants used only as defaults (FIXED_FLOOR/THIS_ROUND_FLOOR/DECLINED_CAP/BASE, :50-52/:272) — every selftest run passes floors explicitly, so tampering with the frozen floors is invisible; (c) aggregation/paragraph-parsing edge cases (sum vs max :268, paragraph boundary :102/:108); (d) the decision output line itself (:284) was never asserted.
3. This substantiates the round's mined mistake: a selftest can reach `measure()` and still miss ~62% of single-edit mutants; the same instrument with the 18 added cases kills 29/29.
4. Boundary finding, no action taken: one mid-run assertion needed correcting (side-branch case expected total=1; refusing the only fix also trips the run's trf=1 floor, total=2) — fixed in the extension before scoring; pristine now passes 43/43.

## Restoration

Lane counter never edited: `sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-50/c1/measure.py` → `ceee320c9ad84c89a7846fd746a072a60758a465d25ff80343fb95e0bd88ae29`, identical to the pre-task copy (`T50MutC1Counter/pristine-measure.py`); all mutants lived in scratch copies only. `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --porcelain -- .ufo/evidence/round-50/c1/` is empty. No lane git/jj state touched; no tool installed or upgraded (none needed); pacman unused. Scratch dir removed before yield.

Receipts (this directory): `baseline.txt`, `run.log` (phase 1 console), `results.json` (phase 1 machine), `mutant-diffs.txt` (all 29 edits), `pristine-measure.py`, `ext-measure.py` (43-case selftest), `ext_run.log`, `ext_results.json` (phase 2 machine).

## Summary
- 29 single-edit mutants of the frozen C1 counter, detector = its own `--selftest` (reaches measure() on a fixture repo).
- Phase 1: 11 killed, 18 survived — survivors span ACK words, HARD/SOFT prefixes, excerpt length, key path-suffix, REV ancestry, Planned parsing, all four constants, total arithmetic, duplicate handling, range end, the PASS token.
- Built a 43-case extended selftest (pristine: 43/43, exit 0); every killing case demonstrated: 18/18 survivors now fail exactly their case.
- Net: 29/29 killed; the frozen selftest alone kills 11/29 (38%), confirming and sharpening the round-49 finding (selftests can reach measure() and still miss most mutants).
- Lane bytes unchanged (sha256 ceee320c… before and after); receipts in `.ufo/waves/round-50/w1/T50MutC1Counter/`; scratch deleted.
