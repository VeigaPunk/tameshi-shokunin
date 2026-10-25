# CriticR40Discharge — round-40 routed defects, disposed against round-41 artefacts

Seat: `L1Tameshi41.CriticR40Discharge` (critic, read-only). The lane checkout, the fleet repo, the
sibling lanes, the lane jj state and the Git index were not touched; the only file written is this
report. No installs (nothing needed; `python3`, `git`, `awk`, `wc`, `sha256sum` sufficed; the host
pacman pause was not exercised).

State read: freeze `d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937`, then the round commit
`b37ce974b6efb8c465626d7346149549a3300a4b` (records + after receipts) and its uncommitted successors
(`contract.json` amendment A5, `after/`, `.ufo/waves/round-41/w1/`). One counter run only, at the
allowed base revision; never at the tip.

## Verdicts — one line per routed defect

1. **discharge** — the appended correction is committed and the class is measured closed: `corpus/lessons/round-41.md:51-58` states "one adopted, six refused, ten present-but-not-appended" and names `round-40`, my independent count of the table (`git show d4ee4e6:corpus/lessons/round-40.md | awk '/^### Quarantine/…'` → `rows=17 adopted=1 refused=6 present=10`) shows the correction is numerically true rather than string-satisfying, the receipt `.ufo/evidence/round-41/after/c1-at-b37ce974b6efb8c465626d7346149549a3300a4b.stdout` prints `m9=0` at the round commit, and the same class fires at base (`m9=1 … its table counts (1, 6, 10)`), so m9 can fail; `round-40.md` was not rewritten (`git log -1 -- corpus/lessons/round-40.md` → `4678127`).
2. **route again** — round 41 retires the transient pointer only by making no grant/timing claim, and never cites the durable replacement its routing names: `git show b37ce97:LOG.md | grep -c wave-slots` → `0` with the wave bullet citing only `spec-w1.json`/`dispatch-w1.json`/`swarm-registry.json` (`LOG.md:2145-2149`), `ScribeLog.md:84-85` says "Settlement is not observable at draft time … claims no settlement", and `.ufo/waves/round-41/settlement-receipt.json` does not exist and no item creates or validates it; smallest correction: one report line — `wave timing: .ufo/waves/round-41/settlement-receipt.json + python3 tools/wave-parent-settle.py --receipt … stdout + OMP log; no wave-slots citation`.
3. **route again** — nothing pastes the lists and the briefed checker says so itself: `ReviewIdLists.md:8` reads "the lists are MISSING everywhere; the report does not exist", the lesson (`corpus/lessons/round-41.md:42`) and LOG (`LOG.md:2138`) carry counts/ranges only, the lists sit untracked at `.ufo/waves/round-41/assimilation/{reg-ids:109,staged-ids:103,collisions:2}`, and `prompt:427` requires the paste in the report; smallest correction: paste `ReviewIdLists.md`'s block into the report only — never the lesson/LOG, where 109/103 ids add 28 m7 mismatches (`ReviewIdLists.md:41-47`).
4. **discharge** — the erratum is committed with both numbers and the class did not repeat: `corpus/lessons/round-41.md:75` records "a quote labelled \"11 words\" that has 13 tokens" against `corpus/lessons/round-40.md:14` (`printf '%s' 'drawbacks such as fragility and lack of context can lead to false positives' | wc -w` → `13`), the round's own labels verify at `round-41.md:17,:21` and `corpus/knowledge/r41-variable-destination-writes.md:12,:19` (`wc -w` → `15` and `16`), and the closed round-40 file is untouched (`git log -1 -- corpus/lessons/round-40.md` → `4678127`).
5. **discharge** — the vacuous contract guard is retired and the record cites the operative guard that can fail, which is the alternative the round-38 routing allowed: `git show d4ee4e6:tools/mutate-and-run.sh | grep -cE '^\s*leg'` → `0`, the round-41 contract carries no `no_harm_guard` key (`'no_harm_guard' in json.dumps(contract)` → `False`), `SCORECARD.md:1919-1925` states "depth 9 → 9 (command D prints `recorded_cases=9 depth_score=9` at base and at the round commit …)" against `SCORECARD.md:73`'s can-fail command, and `git diff --stat a3d6c69 b37ce97 -- tools/mutate-and-run.sh` is empty; residual: retirement by omission — re-adding `depth_command_d` with `^\s*leg` re-breaks it.

## Commands that produced the above

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/calibration/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev a3d6c690bcbf8914551d4f4e8e1612784c1c2046
MISMATCH m6 SCORECARD standing row says 103 rows, SOURCES.md has 107
MISMATCH m9 round-40 quarantine summary says (1, 7, 9), its table counts (1, 6, 10) (no round-41 correction)
C1_R41: m6=1 m7=0 m8=0 m9=1 total=2 records=0 sources_rows=107 rev=a3d6c690… C1_R41_PASS=false   (exit 1)

git show d4ee4e6:corpus/lessons/round-40.md > /tmp/tameshi-r41-criticr40-r40lesson.md
awk '/^### Quarantine/{f=1} f&&/^\| S[0-9]/{t++; …}' /tmp/…r40lesson.md
rows=17 adopted=1 refused=6 present=10

git show b37ce97:SCORECARD.md | awk '/^## Round 41 —/,0' | sed -n '22,26p'
Numeric axes: **depth 9 → 9** (command D prints `recorded_cases=9 depth_score=9` at base and at the
round commit — the runner is not edited and no ledger leg is added); **calibration 8 → 8** …

git show b37ce97:LOG.md | awk '/^## 2026-10-25 — round 41/,0' | grep -c "wave-slots\|settlement" → 0
grep -c "wave-slots" corpus/lessons/round-41.md                                                  → 0
grep -c "wave-slots" .ufo/evidence/round-41/contract.json                                        → 0
git show b37ce97:LOG.md | sed -n '2150p'  → - Command D at the measured commit: `recorded_cases=9 depth_score=9`. No axis harmed.
wc -l .ufo/waves/round-41/assimilation/{reg-ids,staged-ids,collisions}                              → 109 / 103 / 2
```

State of the round's own receipts (read, not produced): `.ufo/evidence/round-41/after/` holds
`c1-at-b37ce974…stdout` = `MISMATCH m8 .ufo/waves/round-41/w1/swarm-registry.json cited but does not
resolve at b37ce974…` + `m6=0 m7=0 m8=1 m9=0 total=1 records=3 sources_rows=109 C1_R41_PASS=false`
(exit 1) and `c2-at-b37ce974…stdout` = `C2_R41_PASS=true` (exit 0). C1 is therefore **not** green at
the revision those receipts name — the m8 miss is the uncommitted wave directory (`git status
--porcelain` → `?? .ufo/waves/round-41/w1/`), which is a commit-ordering item, not a routed defect.
Verdict 1 rests on `m9=0` in that receipt, not on a green C1.

## Counterexample the routed list does not cover (impacts C1's calibration claim)

The declared C1 pin does not identify the counter at the revision the deciding receipt names, and no
class can notice:

```
git show b37ce97:.ufo/evidence/round-41/calibration/measure.py | sha256sum
9aaa99ac5a5abd16a42123fba4bf5c90151b3d043aa2d92ee99116e5789d92cd
git show b37ce97:.ufo/evidence/round-41/contract.json  → claims.C1.counter_sha256
8bc9b4221c59c7b380892b7f97885e9b8ada1f5d82b0703effa166f0519ce11c
```

`measure.py` declares no self-sha class (contrast C2's `tool_sha_ok` at `census/measure.py`), so a
stale pin cannot turn `C1_R41_PASS` false — the pin is asserted in the contract and enforced nowhere.
The worktree already fixes it (A5, uncommitted: pin `9aaa99ac…` equals the live file,
`contract.json` is `M`), so the smallest safe correction is to commit that pin with the round-41
commit **and** add a `counter_sha_ok` field to C1's predicate so the pin can fail; otherwise the next
post-freeze counter edit re-creates the same false record.

## Bounds

- No default-mode counter run at the tip or at any measurement revision; the single C1 run was
  `--rev a3d6c690…` (the allowed base). `--control`/`--selftest` were not needed for these items.
- The lane moved under this read: `measure.py` sha256 `f00917dd…` at the freeze, `8bc9b422…` after
  A1/A4, `9aaa99ac…` after A5. Record line numbers are pinned to the round commit `b37ce97`
  (lesson `:42`, `:51-58`, `:75`; `SCORECARD.md:1851`, `:1919-1925`; `LOG.md:2138`, `:2145-2149`,
  `:2150`). The worktree was being appended to again at 03:50 (`count-label-drift` had moved
  `:75` → `:104`), so re-anchor by content, not by offset, if the records are re-committed.
- No routed item was dropped; none is discharged by silence — defect 2's and 3's prescriptions are
  simply not implemented, and both corrections are one-block edits.

Report: .ufo/waves/round-41/w1/CriticR40Discharge.md
