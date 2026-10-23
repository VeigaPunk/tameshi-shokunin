# Round-35 W2 — ScribeLesson

Axes: calibration and provenance. This was a read-only review of the round-35 C1/C2 counters, the current `## Mistakes` draft, and available W2 scratch evidence. I did not edit product files or run either deciding counter.

## Finding — HYGIENE: A4's C1 patch initially missed the counter

This is a real, lesson-worthy pre-data mistake, already drafted as Mistake 3 in `corpus/lessons/round-35.md`. The draft has the required class/evidence/captured-by/fix structure. Evidence and limits:

- Exact source reproduction command (read-only), exit 0:
  ```sh
  env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7267738:.ufo/evidence/round-35/c1/c1-measure.py
  ```
  The historical blob SHA-256 is `50398b3d13ea11312b83446e0b0204b1d023c923f81c23e05eae73b89bca21b9`; its `run_block` line 165 is `root_s, auto_s, keep_s = cfg`, so an auto-root `None` was passed literally instead of resolved with `cfg_root`.
- The exact search used to expose that line also exited 0:
  ```sh
  env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7267738:.ufo/evidence/round-35/c1/c1-measure.py | grep -n -A2 -B2 'root_s, auto_s, keep_s'
  ```
  It printed lines 163–169, including the faulty assignment. The source is the A4 commit (`72677381eb8f24456f03ea9cee0af374688eb6b6`).
- The later counter blob in commit `68f25573d075d04189158e7eac76408b0e0a981f` hashes to `d27e6769c0def37900eea4d860f9b23bf2ce4e7c876a49eb0a1e92b7bf2052c2`; its line 165 uses `cfg_root(cfg)`. The committed control stdout at that commit hashes to `28bc3529b88879cf4f64251c16deb304140c50849909a070b6a4dacd62044e5d` and records both root-keyed copies as `div=(1,0),(1,1)`. The receipt ends `pub_kill=0/5 pub_accept=0/3 ... C1_R35_CONTROL_PASS=false`; the commit summary records control exit 1. This is the expected v2 control failure, not a claim that v2 detected the specimens.
- Hash commands and exits:
  ```sh
  set -o pipefail && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7267738:.ufo/evidence/round-35/c1/c1-measure.py | sha256sum
  # exit 0; 50398b3d13ea11312b83446e0b0204b1d023c923f81c23e05eae73b89bca21b9
  set -o pipefail && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 68f2557:.ufo/evidence/round-35/c1/c1-measure.py | sha256sum
  # exit 0; d27e6769c0def37900eea4d860f9b23bf2ce4e7c876a49eb0a1e92b7bf2052c2
  env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 68f2557:.ufo/evidence/round-35/control/c1-v2-control.stdout
  # exit 0; output SHA-256 above
  ```

**Draft lesson line:** **class:** a pre-data two-file amendment silently failed to update the C1 counter's auto-root input. **evidence:** A4 commit `7267738`, C1 counter line 165 (`root_s, auto_s, keep_s = cfg`), plus the corrected control receipt at `68f2557`, where both root-keyed kills have `div=(1,0),(1,1)`. **captured-by:** C1's per-copy behavioral `div=` column and the v2 control receipt. **fix:** resolve the root with `cfg_root(cfg)` in `run_block`, then re-pin and rerun before/control from the corrected counter bytes. **shown able to fail:** the source-level reproducer above returns the A4 counter with the faulty assignment; the later receipt demonstrates that the corrected counter observes divergence under both auto triples.

Limit: the original failing post-A4 runtime receipt was superseded; I found no durable exact invocation/output for that first run. The historical source command is a reproducible source-level witness, while the later control receipt is evidence of the corrected behavior. Do not describe the lost first run as an independently re-executed result.

## Parser-mistake draft: mechanism verified, full historical run not

The current lesson's Mistake 4 says the original parser produced `30316/30316` phantom mismatches. The present C1 source (SHA-256 `d27e6769c0def37900eea4d860f9b23bf2ce4e7c876a49eb0a1e92b7bf2052c2`) now writes U+001F and parses with `split('\n')` at lines 171–182. The two committed lesson stdout files are `c1-splitlines-mutation.stdout` (SHA-256 `42a5a56668d090438f162b471290cd36b63ffff6a813038b8dff12e05efdded4`) and `c1-separator-mutation.stdout` (SHA-256 `bb92e7227dee51f74c5777429ef9ba1c4dbd13ed4a4408abac66920ad4ab5dec`). Their recorded `workdir-branch-swap` rows differ (`div=(1,0),(0,0)` versus `div=-`/invalid), consistent with the parser sensitivity.

A narrow mechanism reproduction was run (exit 0):
```sh
/usr/bin/python3 -c 'wire = "R\t0\tFAIL\x1eREGRESSION_WORKDIR: removed\n"; legacy = [line for line in wire.splitlines() if line.startswith("R\t")]; fixed = [line for line in wire.split("\n") if line.startswith("R\t")]; print("legacy_records=%r" % legacy); print("fixed_records=%r" % fixed); print("legacy_second_line_lost=%s" % ("REGRESSION_WORKDIR" not in "\n".join(legacy))); print("fixed_embedded_line_preserved=%s" % ("REGRESSION_WORKDIR" in fixed[0]))'
```
It printed `legacy_records=['R\t0\tFAIL']`, the fixed record retaining `REGRESSION_WORKDIR`, and both expected booleans `True`. This proves the delimiter mechanism only; it is **not** a reproduction of the full 30,316-vector original run. The stdout artifacts do not preserve that run's command or the mutated counter bytes/hash, so Mistake 4 should not claim a fully auditable end-to-end reproduction from these pointers alone.

## Gates, touched surfaces, and limits

- Read and hashed the counters: current observed C1 `d27e6769…2052c2`, C2 `67bb7118…018f9cc`; current contract `ef878db7…97d3041`. C2 source lines 88–104 derive m3 from `git status` on the live fleet worktree, not solely from `REV`; a historical m3 count therefore depends on the contemporaneous fleet state.
- The scratch copy at `/fast/scratch/hyaku/tameshi-r35-seats/ScribeLesson/lane/.ufo/evidence/round-35/c1/c1-measure.py` hashes to `78bb43ebf3d2a313951d9d89f470f2543023b1605326fe676eef3cdb7a947ef9`, not the dispatch-pinned C1 bytes `515b0b1b…0559e8`. I treated that copy as stale and did not use it to claim dispatch behavior. The current contract records the later A6 counter pin `d27e…2052c2`.
- The W2 `CriticPredicate` scratch receipt explicitly labels its probe as AST/metadata-only and says no counter/tool/shell runner was executed; I did not upgrade it to execution evidence.
- No C1 default-mode run, C2 head run, build, test, install, git mutation, or product edit was performed. In particular, this report does not claim C1 PASS or current-head C2 PASS; the main agent should perform the contract-mandated C2 recount after wave records land and preserve the deciding C1 run rule.
- What could not be broken from existing executed evidence: the corrected counter's root-keyed panel behavior is non-identical under both auto triples, as shown by the committed `68f2557` receipt. This is bounded to those specimens/configs, not a general claim about v3.

Touched surface: this report only. No installs or updates.

Artifact: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/ScribeLesson.md`