# Round 35 W2 — ExecReplayC2Before

## Scope

Replayed the frozen C2 counter against the recorded before revision (`51d3f08073be65d3475cf0286042fc0dbe4c4a7d`) and the dispatch pin (`7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`), using the current fleet root `/home/vgpnk/Projects/shokunin`. No source, lane, fleet, or sibling files were changed; only this report was written in the repository. No tools installed.

The counter SHA-256 is `67bb71188cde259088646f960b6fda8e0a217fad5d8260e379054b381018f9cc` (current file and `git show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:.ufo/evidence/round-35/c2/c2-measure.py` agree). This is the frozen counter hash in `contract.json:16-17`. The counter was not present in commit `51d3f080...` (`git show 51d3f08073be65d3475cf0286042fc0dbe4c4a7d:.ufo/evidence/round-35/c2/c2-measure.py` exited 128); the receipt's `rev=` is the data revision, so I ran the frozen counter bytes at the dispatch pin while evaluating that historical tree.

## Commands and evidence

1. Historical receipt revision, current fleet working tree:

   ```sh
   python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/c2/c2-measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 51d3f08073be65d3475cf0286042fc0dbe4c4a7d --fleet /home/vgpnk/Projects/shokunin
   ```

   Exit **1**. Output saved at `/fast/scratch/hyaku/tameshi-r35-w2/ExecReplayC2Before/c2-at-51d3-current-fleet.stdout`, SHA-256 `1dcfb1b4cd36e01daade1127fa8292cd67009e566817263839700b4a628bd126`. Receipt `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/before/c2-at-base.stdout` SHA-256 `c366753db8778dc9289bda1b0ec2d5251cc6cd91b7aefaac3e25e2de4074fb8c`.

   `cmp -s /fast/scratch/hyaku/tameshi-r35-w2/ExecReplayC2Before/c2-at-51d3-current-fleet.stdout /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/before/c2-at-base.stdout` exited **1**. `diff -u` exited **1** and showed only two changed lines: the receipt's `MISMATCH m3 .ufo/waves/round-34/w1/ReviewDevReceipts.md (untracked seat file: ??)` is absent from the replay, and the final total changes from `m3=1 total=15` to `m3=0 total=14`. All other mismatch lines and counts match exactly (`m1=8 m2=3 m4=1 m5=1 m6=1`, `entries=40`, `sources_rows=98`, same `rev=51d3...`). See the receipt and replay output paths above.

   Cause: the fleet file has since been removed. `test -e /home/vgpnk/Projects/shokunin/.ufo/waves/round-34/w1/ReviewDevReceipts.md` exited **1** (absent); `git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all -- .ufo/waves/round-34/w1/ReviewDevReceipts.md` exited **0** with no output. The corresponding file is present in the lane at dispatch pin `7da6...`; `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:.ufo/waves/round-34/w1/ReviewDevReceipts.md | sha256sum` exited **0**, SHA-256 `ff532da39c28846c3d0ff832340312cdb97a457e68843ddc8e8642898267b3c2`. I did not copy the fleet repository; the exact line-level alternative requested is established by the diff and missing-path checks.

2. Dispatch pin, current fleet working tree:

   ```sh
   python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/c2/c2-measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b --fleet /home/vgpnk/Projects/shokunin
   ```

   Exit **0**. Output `/fast/scratch/hyaku/tameshi-r35-w2/ExecReplayC2Before/c2-at-7da6-current-fleet.stdout`, SHA-256 `611277c8e7153ee36733dd9dd108b3ec7ba1654e152f798d655397c4802302ba`; exact line: `C2_R35: m1=0 m2=0 m3=0 m4=0 m5=0 m6=0 total=0 entries=40 sources_rows=99 rev=7da6e076c2e25936a3b60dde2a4080d8f05b7e5b C2_R35_PASS=true`.

## Findings (ranked)

- **BOUND — historical m3 depends on fleet working-tree state.** The recorded before receipt is not byte-replayable against today's fleet because the specifically named untracked file is absent. The diff proves this changes exactly the m3 line and final total; the other five mismatch classes reproduce at the receipt revision. This is a bounded historical-state difference, not a counter discrepancy.
- **No CRITICAL finding.** At the dispatched lane pin, the exact frozen counter reports all six classes zero and exits 0; evidence and hash are above.

## What I could not break

- **C2 at dispatch pin:** could not produce a mismatch; the counter returned `m1=m2=m3=m4=m5=m6=0`, `C2_R35_PASS=true`, exit 0 (output hash above).
- **Five non-m3 historical mismatches:** could not produce a difference from the receipt; `diff -u` identifies only the deleted fleet-file line and dependent total as changed.

## Files and risks

- Repository file changed: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/ExecReplayC2Before.md` (this report only).
- Scratch evidence: the two stdout files under `/fast/scratch/hyaku/tameshi-r35-w2/ExecReplayC2Before/`.
- Risk/blocker: exact historical reproduction of m3 requires the old external fleet working-tree file; current fleet state lacks it. No other blocker observed.
