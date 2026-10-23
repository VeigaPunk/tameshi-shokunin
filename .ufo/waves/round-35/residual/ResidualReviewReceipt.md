# ResidualReviewReceipt — round-35 C1 deciding receipt audit

Lane tip observed: `34fa5b0cfe909f3cde644676ead723256281dd05`
(`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse master` → `34fa5b0cfe909f3cde644676ead723256281dd05`), equal to the tip named in the round contract.

## Item 1 — pin frozen artifacts at tip
```
$ sha256sum tools/tally-audit-v3.py tools/mutate-and-run.sh .ufo/evidence/round-35/c1/c1-measure.py
6188db16de045f2927df2a0e667bc1539f4acfce5a1ac116e6de3107bf15d354  tools/tally-audit-v3.py
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  tools/mutate-and-run.sh
d360a159a1ad320e8726eed51256146a90025ce5e5fc97840a488f3a2ad4bbe3  .ufo/evidence/round-35/c1/c1-measure.py
$ git status --porcelain -- tools/tally-audit-v3.py tools/mutate-and-run.sh .ufo/evidence/round-35/c1/c1-measure.py
(empty)
```
All three equal contract.json `frozen_artifacts` (tool `6188db16…`, runner `a7d3f2dd…`, c1 counter `d360a159…`); worktree clean on the pinned paths.
VERDICT: CONFIRMED

## Item 2 — receipt line, exit, stderr
```
$ cat .ufo/evidence/round-35/after/c1-at-34fa5b0cfe909f3cde644676ead723256281dd05.stdout
COPY kill  cfg00-accept-swap                  cfg00-accept-swap.json div=(0,0) rc=1 checks=runtime pass=True
COPY kill  cfg11-pass-mask                    cfg11-pass-mask.json div=(1,1) rc=1 checks=runtime pass=True
COPY accept comment-brace                      comment-brace.json div=- rc=0 checks=- pass=True
COPY accept comment-esac                       comment-esac.json div=- rc=0 checks=- pass=True
COPY accept comment-names-leg                  comment-names-leg.json div=- rc=0 checks=- pass=True
COPY kill  root-keyed-auto-mask               root-keyed-auto-mask.json div=(1,0),(1,1) rc=1 checks=runtime pass=True
COPY kill  root-keyed-auto-zero               root-keyed-auto-zero.json div=(1,0),(1,1) rc=1 checks=runtime pass=True
COPY kill  root-keyed-shape6                  root-keyed-shape6.json div=(1,0),(1,1) rc=1 checks=runtime pass=True
COPY kill  workdir-branch-swap                workdir-branch-swap.json div=(1,0),(0,0) rc=1 checks=runtime pass=True
COPY accept accept-trailing-comments           accept-trailing-comments.json div=- rc=0 checks=- pass=True
COPY kill  cfg00-setup-as-pass                cfg00-setup-as-pass.json div=(0,0) rc=1 checks=runtime pass=True
COPY kill  cfg11-workdir-wording              cfg11-workdir-wording.json div=(1,1) rc=1 checks=runtime pass=True
COPY accept comment-head-comment-quoted-legnames comment-head-comment-quoted-legnames.json div=- rc=0 checks=- pass=True
COPY accept inert-heredoc-apostrophe-comment   inert-heredoc-apostrophe-comment.json div=- rc=0 checks=- pass=True
COPY kill  workdir-branch-keep-swap           workdir-branch-keep-swap.json div=(1,0),(1,1) rc=1 checks=runtime pass=True
COPY kill  workdir-keep-cleanup-nested-config workdir-keep-cleanup-nested-config.json div=(1,1) rc=1 checks=runtime pass=True
C1_R35: mode=deciding tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=34fa5b0cfe909f3cde644676ead723256281dd05 C1_R35_PASS=true
$ cat .../.exit
0
$ wc -c .../.stderr
0 .ufo/evidence/round-35/after/c1-at-34fa5b0cfe909f3cde644676ead723256281dd05.stderr
```
`rev=` equals the observed tip; `tool_sha` is the truncated prefix of `6188db16de045f2927df2a0e667bc1539f4acfce5a1ac116e6de3107bf15d354`; all summary fields match the required values; exit `0`; stderr 0 bytes. Line-level arithmetic: 16 COPY lines = 9 panel + 7 sealed = pub_slots + ho_distinct; kill lines 6+4, accept lines 3+3.
VERDICT: CONFIRMED

## Item 3 — sealed provenance (no deciding mode)
```
$ git log --diff-filter=A --format='%H %an %s' -- .ufo/evidence/round-35/contract.json
d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc tameshi-shokunin round-35: tally-audit-v3 (four-config sweep, ...) + S102
$ sha256sum sealed/*.json      # all 7 match manifest.json 'sha256' fields exactly
a46a30f7…  accept-trailing-comments.json  (manifest: a46a30f7158f78b2023bda24af70c3cadf7ec304638cc33024670ea108d55251) MATCH
a77486d9…  cfg00-setup-as-pass.json        MATCH  |  daa53fcf… cfg11-workdir-wording.json  MATCH
b9e0aaad…  comment-head-comment-quoted-legnames.json  MATCH  |  33d15541… inert-heredoc-apostrophe-comment.json  MATCH
0d46e7cf…  workdir-branch-keep-swap.json  MATCH  |  f2e1501d… workdir-keep-cleanup-nested-config.json  MATCH
$ for f in $(git ls-tree -r master --name-only -- .ufo/evidence/round-35/c1/sealed/); do
    last=$(git log -n1 --format=%H -- "$f"); git merge-base --is-ancestor d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc "$last" && anc=yes || anc=NO; echo "$f last=$last ancestor=$anc"; done
# all 8 paths (7 copies + manifest.json): last=691bb5128e98ff0b827f5eb1e8cd8f86f8ce2757 ancestor=yes
$ git merge-base --is-ancestor d16f9b5a… master && echo yes
yes
```
Contract first added at `d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc` (the manifest's `freeze_rev`); every sealed copy's last-touching commit `691bb5128e98ff0b827f5eb1e8cd8f86f8ce2757` descends from it. Each manifest `author_report` exists under `.ufo/waves/round-35/w2/`: SealAcceptTrailing.md, SealCfg00Guard.md, SealCfg11Mask.md, SealAcceptCommentHead.md, SealAcceptHeredoc.md, SealStdoutWorkdir.md, SealStdoutDetail.md (verified via `ls .ufo/waves/round-35/w2/` — all present).
VERDICT: CONFIRMED

## Item 4 — per-copy lines vs committed bytes
The 7 sealed names and 9 panel names in the receipt are exactly the committed files (excluding `manifest.json`): `ls` of `c1/sealed/` and `c1/panel/` equals the receipt's COPY-line filenames verbatim. Each committed copy JSON (`copies[0]`) declares `class` and `set` (`kill`/`accept`); an automated cross-check (python3, json only — the c1 counter module was not run in deciding mode) matched every line: receipt class-name column == JSON `class`, receipt kill/accept word == JSON `set`, kill lines have ≥1 `div=(i,j)` tuple + `rc=1` + `checks=runtime`, accept lines `div=-` + `rc=0` + `checks=-`, all `pass=True`. Output: 16× `OK`, `ALL_CONSISTENT`; summary sets panel (6 kill,3 accept), sealed (4 kill,3 accept) — matching `pub_kill=6/6 pub_accept=3/3`, `ho_kill=4/4 ho_accept=3/3`, `pub_slots=9 pub_distinct=9 ho_distinct=7`.
VERDICT: CONFIRMED

## Item 5 — evidence status
```
$ git status --porcelain -- .ufo/evidence/round-35/after/
?? .ufo/evidence/round-35/after/c1-at-34fa5b0cfe909f3cde644676ead723256281dd05.exit
?? .ufo/evidence/round-35/after/c1-at-34fa5b0cfe909f3cde644676ead723256281dd05.stderr
?? .ufo/evidence/round-35/after/c1-at-34fa5b0cfe909f3cde644676ead723256281dd05.stdout
$ git ls-tree -r master --name-only | grep 'round-35/after'
.ufo/evidence/round-35/after/c2-at-d16f9b5a.stdout   (last touch 43aea0305ba4af19b634ee115e769a91ea99fbc9)
.ufo/evidence/round-35/after/census-at-round-end.stdout
```
The C1 deciding receipt trio is untracked; no commit carries it. Evidence-status only, not a defect per this seat's contract.
VERDICT: CONFIRMED

## Residual risk / gaps
- `div=` tuple semantics (which config pair each index names) not re-derived; only non-emptiness/consistency against declared class was checked. The excluded-specimen claims (SealKillHeadRead `div=-` on the 266-vector oracle) were not re-run — out of this audit's scope.
- The untracked receipt cannot be anchored to a commit; integrity rests on working-tree bytes alone.

Tooling installs: none. No counter deciding-mode run; only `cat`/`sha256sum`/`git log|ls-tree|merge-base` and a read-only python3 JSON comparison.
VERDICT: all five items CONFIRMED (no DEFECT found).
SEAT: ResidualReviewReceipt model=devin/swe-2
