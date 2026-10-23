# ResidualReviewSealed — independent re-derivation of the 7 sealed specimens' behavior class

Lane tip observed: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse master` → `34fa5b0cfe909f3cde644676ead723256281dd05`. `git status --porcelain` on sealed/, runner, tool, counter: empty — working tree == rev for all inputs.

## Method

Harness `/tmp/tameshi-r35-res-sealed/rederive.py` imports `.ufo/evidence/round-35/c1/c1-measure.py` via `importlib.util` (never `main()`, never deciding mode; no `--before`/`--tool` invocation at all) and calls its oracle functions on committed bytes at rev (`git show 34fa5b0:<path>`). Per copy: `apply_edits` → `tally_block` → `unsafe_block` gate → `behavior()` under all 4 configs × 267 vectors → `diverge(pristine, copy)`. Pristine behavior re-run in a fresh dir per copy as a determinism check. Counter verdicts were never read before classification.

```
$ time python3 rederive.py
runner sha256@rev : a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
PIN_RUNNER        : a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
runner match      : True
vector set size   : 267 (n=9 legs)
configs           : ((None, '1', '0'), (None, '1', '1'), ('tally-audit', '0', '1'), ('/tmp/tally-audit-explicit', '0', '0'))
done accept-trailing-comments.json              identical
done cfg00-setup-as-pass.json                   divergent(min-configs)
done cfg11-workdir-wording.json                 divergent(min-configs)
done comment-head-comment-quoted-legnames.json  identical
done inert-heredoc-apostrophe-comment.json      identical
done workdir-branch-keep-swap.json              divergent(min-configs)
done workdir-keep-cleanup-nested-config.json    divergent(min-configs)
real	0m5.764s
```

No `PRISTINE-UNSTABLE` flag printed on any copy: re-running `behavior(runner_text)` in a fresh dir was identical for all 7 (deterministic oracle).

## Provenance: committed bytes == manifest

`sha256sum .ufo/evidence/round-35/c1/sealed/*.json` matched `manifest.json`'s `sha256` for all 7 (sha_ok=True in table). `git ls-tree -r --name-only 34fa5b0 -- sealed` lists exactly these 7 .json + manifest.json.

## Per-copy results (div labels `(auto,KEEP)` per receipt format; cfg tuple is (root,auto,KEEP))

| copy | declared (set) | observed div configs | receipt div | verdict |
|---|---|---|---|---|
| accept-trailing-comments.json | accept | identical | `-` | CONFIRM |
| cfg00-setup-as-pass.json | kill | `(0,0)` | `(0,0)` | CONFIRM |
| cfg11-workdir-wording.json | kill | `(1,1)` | `(1,1)` | CONFIRM |
| comment-head-comment-quoted-legnames.json | accept | identical | `-` | CONFIRM |
| inert-heredoc-apostrophe-comment.json | accept | identical | `-` | CONFIRM |
| workdir-branch-keep-swap.json | kill | `(1,0),(1,1)` | `(1,0),(1,1)` | CONFIRM |
| workdir-keep-cleanup-nested-config.json | kill | `(1,1)` | `(1,1)` | CONFIRM |

Receipt lines (`.ufo/evidence/round-35/after/c1-at-34fa5b0c…05.stdout`, sealed block):

```
COPY accept accept-trailing-comments           accept-trailing-comments.json div=- rc=0 checks=- pass=True
COPY kill  cfg00-setup-as-pass                cfg00-setup-as-pass.json div=(0,0) rc=1 checks=runtime pass=True
COPY kill  cfg11-workdir-wording              cfg11-workdir-wording.json div=(1,1) rc=1 checks=runtime pass=True
COPY accept comment-head-comment-quoted-legnames comment-head-comment-quoted-legnames.json div=- rc=0 checks=- pass=True
COPY accept inert-heredoc-apostrophe-comment   inert-heredoc-apostrophe-comment.json div=- rc=0 checks=- pass=True
COPY kill  workdir-branch-keep-swap           workdir-branch-keep-swap.json div=(1,0),(1,1) rc=1 checks=runtime pass=True
COPY kill  workdir-keep-cleanup-nested-config workdir-keep-cleanup-nested-config.json div=(1,1) rc=1 checks=runtime pass=True
```

Every observed divergence-set is an exact match to the receipt (no subset/extra-config discrepancy → no NOTE). Kill copies all diverge; accept copies all identical.

## Non-circularity of the oracle (counter's ground truth is runner-code execution, not tool output)

c1-measure.py (line numbers from `grep -n`):
- `run_block` embeds the **extracted runner block text** in bash source and executes it: `200:             block.rstrip('\n'), '}']` and `208:    p = subprocess.run(['bash', path], cwd=tmp, env=env, capture_output=True, timeout=300)`.
- `behavior` → `243:        out[cfg] = run_block(block, names, vs, cfg, tmp)`; `diverge` `248:    return [cfg for cfg in CONFIGS if a[cfg] != b[cfg]]` compares only bash-executed `(exit, stdout)` records.
- In `score_copies`: `369:        div = diverge(pristine_beh, copy_beh)` precedes `374:        rc, failed, last, _ = run_tool(tool_path, rpath, tmp)`; `377:            row['valid'] = bool(div)` / `380:            row['valid'] = not div` — class validity depends solely on `div`; the tool's `rc`/`failed` feed only `pass` (378/381).
- Block provenance: `tally_block` cuts `run_regression`/`local nlegs=` from the copy text derived from `git show 34fa5b0:tools/mutate-and-run.sh` (runner has `local nlegs=9 npass=0 nfail=0 nsetup=0 st` at line 1432); `auto_root()` builds the runner's real root shape — runner `root=$(mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX)` (line 1359 in `git show 34fa5b0:tools/mutate-and-run.sh | sed -n '1350,1370p'`).

Non-circularity CONFIRMED: ground truth = bash execution of the runner's own tally code; the audited tool is never imported by or read into the oracle.

## Residual risk / verification gaps

- Divergence is bounded by the frozen 267-vector set and 4 configs; a mutation outside their reach would read `identical` — a coverage limit, not a defect.
- `workdir-branch-swap.json` (public panel, `div=(1,0),(0,0)`) is a different specimen from sealed `workdir-branch-keep-swap.json` (`(1,0),(1,1)`); both matched their own receipt lines.
- Tool-side `rc=1, checks=runtime` legs not re-derived (outside this seat's behavioral scope); behavior class is what was verified.
- Tooling installs: none (python3/git/bash host tools sufficed; pacman paused per directive).

VERDICT: CONFIRMED — all 7 sealed copies: observed behavior class agrees with manifest-declared set AND receipt div lines, exact config sets matching.

SEAT: ResidualReviewSealed model=devin/swe-2
