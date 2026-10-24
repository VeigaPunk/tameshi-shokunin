# W2MTLogAppend — mutation probe: QUALITY criterion 72 (LOG evidence citations must resolve in git history)

Seat: mutation tester (leaf). Wave round-36 / w2. No production edits; scratch-only mutation.
Lane tip under attack: `fbb01cf46f8437fd1264c1a3acc053c882fa2164` (lane `HEAD` before and after this seat).
Scratch clone: `/fast/scratch/hyaku/tameshi-r36-seats/W2MTLogAppend/repo` (`git clone --no-hardlinks` of the lane;
lane `.git` never written). Only lane write: this report.

## Attack surface

QUALITY criterion 72 (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/QUALITY.md:846-857`):

> A LOG.md entry that names a file as evidence must name a file that exists at write time: the citation is
> re-resolved (path or `git log --all -- <path>`) before the entry commits …

The behavioral detector is the emptiness test on the cited path:

```
git -C <repo> log --all --format=%H -- '<path>'
```

non-empty history = citation resolves; empty history = violation. Because `git log` exits 0 even when the path has
no history, the test must read stdout, not the exit status (see calibration finding 1). The one-command wrapper used
for every run below is `/fast/scratch/hyaku/tameshi-r36-seats/W2MTLogAppend/cite-check.sh`
(sha256 `daa1b83a60dd0800a105a9e46b4a27fd7928ef1dc7007d42f1afc7c96b5c366e`):

```sh
#!/bin/sh
r=$1; p=$2
h=$(git -C "$r" log --all --format=%H -- "$p")
if [ -n "$h" ]; then
  printf 'CITE_RESOLVED commits=%s path=%s\n' "$(printf '%s\n' "$h" | wc -l)" "$p"
  exit 0
else
  printf 'CITE_UNRESOLVED commits=0 path=%s\n' "$p"
  exit 3
fi
```

## Mutant applied

Appended to the scratch clone's `LOG.md` (append-only shape; last 3 lines of the file, nothing else changed):

```
- 2026-10-24 — round 36 (w2 log-citation probe): evidence
  `.ufo/waves/round-36/w2/LogCitationProbeReceipt.md` records the probe's raw
  output.
```

The cited path `.ufo/waves/round-36/w2/LogCitationProbeReceipt.md` was never committed and does not exist in the
working tree; the string `LogCitationProbeReceipt` occurs 0 times in the pristine `LOG.md`. This is the exact defect
class criterion 72 was opened for (r35's `ResidualSentinelClosure.md` dead pointer).

- Pristine `LOG.md` sha256 `a2223dc239aaa37ca9347e274084dc51426d741a1d2398eafa93c420d9340534` (blob at `fbb01cf`; identical
  to the lane file, `sha256sum` cross-checked).
- Mutant `LOG.md` sha256 `0514aed67432b49e0921748f873631b3042e95019f427342304eca82598e7666`.
- Mutant commit `c3100cabe6ec03439a3e06fbe2a7786c3b2d0c6f`; `git diff --numstat fbb01cf..c3100ca` = `3	0	LOG.md`
  (three added lines, zero removed).
- The citation is present in the mutant commit: `git show c3100ca:LOG.md | grep -n LogCitationProbeReceipt` →
  `1944:  `.ufo/waves/round-36/w2/LogCitationProbeReceipt.md` records the probe's raw`.

## Commands, revisions, outputs

Repo root for all commands: `/fast/scratch/hyaku/tameshi-r36-seats/W2MTLogAppend/repo`.

1. Baseline, pristine `fbb01cf46f8437fd1264c1a3acc053c882fa2164`. The five evidence paths the round-36 correction
   actually names (the real residual reports):
   ```
   ./cite-check.sh repo .ufo/waves/round-35/residual/ResidualCriticPredicate.md   # CITE_RESOLVED commits=1 exit 0
   ./cite-check.sh repo .ufo/waves/round-35/residual/ResidualReviewC2.md          # CITE_RESOLVED commits=1 exit 0
   ./cite-check.sh repo .ufo/waves/round-35/residual/ResidualReviewReceipt.md     # CITE_RESOLVED commits=1 exit 0
   ./cite-check.sh repo .ufo/waves/round-35/residual/ResidualReviewSealed.md      # CITE_RESOLVED commits=1 exit 0
   ./cite-check.sh repo .ufo/waves/round-35/residual/ResidualScoutRecords.md      # CITE_RESOLVED commits=1 exit 0
   ```
   Baseline PASSES: every path the LOG cites resolves. Control on the never-committed name before it is cited:
   `./cite-check.sh repo .ufo/waves/round-36/w2/LogCitationProbeReceipt.md` → `CITE_UNRESOLVED commits=0`, exit 3 —
   but `grep -c LogCitationProbeReceipt LOG.md` = 0, so no violation exists yet (calibration finding 2).
   Historical falsifier of criterion 72: `git log --all --format=%H -- '*ResidualSentinelClosure*'` → 0 lines
   (the r35 dead pointer), and the literal path `.ufo/waves/round-35/residual/ResidualSentinelClosure.md` →
   `stdout_bytes=0 exit=0` (calibration finding 1).
2. Mutant `c3100cabe6ec03439a3e06fbe2a7786c3b2d0c6f` (`master`; `--all` covers `master` + the clone's other refs).
   ```
   ./cite-check.sh repo .ufo/waves/round-36/w2/LogCitationProbeReceipt.md
   → CITE_UNRESOLVED commits=0 path=.ufo/waves/round-36/w2/LogCitationProbeReceipt.md
   → exit 3
   ```
   The entry cited the path (line 1944, grep above) and the path has zero commits → **violation caught**.
   Precision control at the same commit: the five real cited paths still print `CITE_RESOLVED commits=1` / exit 0
   (`mutant-realpaths-all.stdout`), so the check is not globally failing under the mutant.
3. Restore: `git checkout fbb01cf46f8437fd1264c1a3acc053c882fa2164 -- LOG.md`, committed as
   `11838b91e220ac8a1b9dd8d7ce7e29194ef15664` (restore-on-top, history not rewritten).
   - `git diff --name-only fbb01cf..11838b9` → empty (restored tree byte-identical to pristine).
   - `sha256sum LOG.md` → `a2223dc239aaa37ca9347e274084dc51426d741a1d2398eafa93c420d9340534` = pristine.
   - `git show 11838b9:LOG.md | grep -c LogCitationProbeReceipt` → 0 (citation gone).
   - Five-path check rerun at `11838b9` → 5 × `CITE_RESOLVED commits=1` / exit 0; the output file is byte-identical
     to the baseline file (`cmp base-real-paths.stdout restore-realpaths-all.stdout` silent; both sha256
     `0ef61e9ed8acd08aebfd559f379f75d5e78565df7162cb7f7c56c59d010a48cb`).

## Calibration findings (bounded to what was observed)

1. **Exit status alone would miss the violation.** For the never-committed path, the raw criterion command
   `git -C repo log --all --format=%H -- .ufo/waves/round-36/w2/LogCitationProbeReceipt.md` prints 0 bytes and
   **exits 0** (`stdout_bytes=0 exit=0`), same for the literal r35 dead pointer. The emptiness test must assert on
   stdout content (`[ -n "$(...)" ]`), not on the command's exit code. criterion 72's phrasing ("re-resolved") is
   compatible with this, but a checker that treats `git log` exit status as the verdict is vacuous.
2. **The emptiness test is state-blind; the citation is the state-bearing part.** The check's output for the
   never-committed path at pristine (`not yet cited`) and at the mutant (`cited`) is byte-identical
   (`4819723a2019bd71dbddd1cc26413c47017c62a03310d5b62c4c1a041e09e6fc` both runs). Only the pairing
   "LOG line names the path" (absent at baseline/restore, present at mutant) makes the empty history a violation.
   criterion 72 is correctly written as a per-citation step ("the citation is re-resolved"), not as a global sweep
   over every backticked token; a global sweep would flag uncited names as violations and needs a citation
   extractor.
3. **The criterion's own falsifier reproduces under the check.** The r35 dead pointer
   (`*ResidualSentinelClosure*`, glob and literal form) yields 0 commits at the lane tip, exactly as
   `corpus/QUALITY.md:855-857` records — the same one-command check that catches the synthetic mutant also catches
   the real historical defect class.

## Evidence files (all under `/fast/scratch/hyaku/tameshi-r36-seats/W2MTLogAppend/`)

| file | sha256 |
|---|---|
| `cite-check.sh` (detector) | `daa1b83a60dd0800a105a9e46b4a27fd7928ef1dc7007d42f1afc7c96b5c366e` |
| `base-real-paths.stdout` (pristine, 5 real paths) | `0ef61e9ed8acd08aebfd559f379f75d5e78565df7162cb7f7c56c59d010a48cb` |
| `base-bogus-uncited.stdout` (pristine, bogus name uncited) | `4819723a2019bd71dbddd1cc26413c47017c62a03310d5b62c4c1a041e09e6fc` |
| `base-falsifier.stdout` (r35 dead pointer empty, exit 0) | `36c8c728f31081064876fcd2e5298c5c07cebc717dac0fc4223eaa7de6c8c325` |
| `mutant-check.stdout` (mutant, cited path → exit 3) | `4819723a2019bd71dbddd1cc26413c47017c62a03310d5b62c4c1a041e09e6fc` |
| `mutant-realpaths-all.stdout` (mutant, 5 real paths resolve) | `0ef61e9ed8acd08aebfd559f379f75d5e78565df7162cb7f7c56c59d010a48cb` |
| `restore-realpaths-all.stdout` (restore, 5 real paths resolve) | `0ef61e9ed8acd08aebfd559f379f75d5e78565df7162cb7f7c56c59d010a48cb` |
| `restore-check.stdout` (restore, single control path) | `5e9d2b89a3e81e982539e8f50a308a8a0ea62003e7a041e2f43910e86b386496` |
| `raw-criterion-command.stdout` (`stdout_bytes=0 exit=0`) | see report text; captured inline |
| `mutant-meta.txt` / `mutant-numstat.txt` / `restore-meta.txt` | rev + `3	0	LOG.md` |

Scratch worktree clean at the restore commit (`git status --porcelain` empty). Lane untouched:
`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --porcelain` shows only the wave reports' untracked
directories; lane `HEAD` is still `fbb01cf46f8437fd1264c1a3acc053c882fa2164` and the lane `LOG.md` still hashes to
`a2223dc239aaa37ca9347e274084dc51426d741a1d2398eafa93c420d9340534`. No tool installs (none needed).

## Verdict

**KILLED.** The criterion-72 mutant — a LOG entry citing the never-committed
`.ufo/waves/round-36/w2/LogCitationProbeReceipt.md` — is caught by the one-command check: at mutant commit
`c3100cab` the entry's cited path yields `CITE_UNRESOLVED commits=0` (exit 3) from
`git log --all --format=%H -- '<path>'`, while the five paths the pristine LOG really cites resolve with one commit
each at baseline, mutant, and restore. Restoring the pristine `LOG.md` bytes (`11838b91`, tree diff empty, sha256
back to `a2223dc2…`) removes the citation and returns the check to its baseline output byte-for-byte.
