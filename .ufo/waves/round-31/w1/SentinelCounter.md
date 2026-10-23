VERDICT — MEDIUM: the frozen regression runner does not itself write to real sibling repositories, the lane, or fleet root, but C1 is not a filesystem containment boundary. Its child tests write outside `--work`; inherited `TMPDIR` can redirect a regression fixture into a real repo, and a symlinked `--work` can redirect the counter's persistent staging tree there.

Axes: live-repository integrity; `--work` containment; temporary-file containment.

## Exploit paths and write paths

1. **Persistent writes through `--work` alias.** C1 applies `os.path.abspath()` to `--work` but does not resolve or reject symlinks (`c1-measure.py:176-180`). `exists()` and `listdir()` follow a symlink, so a symlink to an empty directory passes the emptiness check; `os.makedirs(work + '/fleet')` then writes through it. Pointing that symlink at an empty directory inside a sibling repo or the lane causes the clone/staging tree to be created in that real repo. Subsequent writes include `fleet/`, `fleet/tameshi-shokunin`, `clone`, `obs-*.stdout`, and the regression workdir. This is a code-path finding; I did not execute the counter.

2. **Regression writes through inherited `TMPDIR`.** C1's `env()` preserves every non-`GIT_*` variable, and `observe()` passes that environment to subprocesses (`c1-measure.py:68-71, 136-147`). The regression leg `js-kimi-census` runs `node "$MUTANT" --selftest` (`mutate-and-run.sh:1386-1390`); its pinned script creates fixture trees under `os.tmpdir()` (`pinned-sources/kimi-census.mjs:471-485`) and removes them in `finally` (`:843-845`). Thus, with `TMPDIR` set to a writable real sibling/lane directory, this normal selftest writes a temporary fixture directory there; successful completion removes it, but interruption can leave it behind. The runner does not override `TMPDIR` for this leg. The last three JS legs explicitly set `TMPDIR` beneath their case workdirs (`mutate-and-run.sh:1416-1429`), unlike the first six.

3. **Other writes outside `--work` on ordinary counter paths.** C1 separately runs `mutate-and-run.sh --selftest` (`c1-measure.py:41-45`); that selftest creates `/tmp/tameshi-r4-2-selftest.*`, removes it on PASS, and retains it on failure (`mutate-and-run.sh:1475-1493, 2046-2053`). Within regression, pinned `tsukuroi-census.sh --selftest` creates `/tmp/tsukuroi-r3-2-selftest.*` (`pinned-sources/tsukuroi-census.sh:628-633`) and pinned `mado-verify.sh --selftest` creates `/tmp/w5-mado-m52-selftest.*`, retaining it on failure (`pinned-sources/mado-verify.sh:338-342, 421-429`). The surface-census and checklist selftests also use `mktemp` without an explicit workdir (`pinned-sources/surface-census.sh:694-698`; `pinned-sources/checklist-run.sh:339-342`). These are outside the supplied `--work` when run with the usual temp configuration; some clean up normally, but they are not confined to it.

4. **Writes confined to the intended work tree.** With a canonical, dedicated `--work`, C1 writes the lane clones/checkouts at `<work>/clone` and `<work>/fleet/tameshi-shokunin`, creates sibling symlinks under `<work>/fleet`, and records outputs under `<work>` (`c1-measure.py:180-204`). Regression writes embedded specs under `<work>/regression-wd/specs`; each leg writes its materialized target, `git-show.err`, `sweep.log`, mutation copies, evidence, and results under its `<work>/regression-wd/<leg>` (`mutate-and-run.sh:1171-1173, 1203-1227, 1247-1251; 481-516, 539-555`). The final three legs also put `sandbox-<defect>/{home,tmp}` there (`:1416-1429`).

## Sibling-repository Git behavior

C1 creates absolute symlinks from `<work>/fleet/<sibling>` to the real siblings (`c1-measure.py:186-189`). Since the runner's `SELF` is in the staged lane, it derives `FLEET_ROOT` as that stage's grandparent (`mutate-and-run.sh:1357-1368`); `regression_case_git()` then resolves each repo through those sibling symlinks (`:1332-1343`). The runner's actual repo operations are reads: `rev-parse`, `cat-file -e`, `show`, and `ls-tree` (`:1187-1204, 1213`). `git show` redirects bytes to the per-leg workdir, and `chmod` applies only to that copied target (`:1203-1227`). No checkout, worktree creation, index/ref update, or Git write is performed in a real sibling. C1's `git clone`/`checkout` operations target only its two staged lane clones (`c1-measure.py:191-195`), not the lane source.

The symlinks are nevertheless writable path aliases, and the subprocesses are not OS-sandboxed. Therefore the read-only behavior above is a property of these pinned commands, not an enforced boundary; code at an untrusted `--rev` can access other writable paths as the caller.

## Evidence / commands

Static review only; no counter, regression, gate, or selftest was executed. These read-only hash commands confirmed the inspected runner and counter are the frozen lane blobs, and that the Kimi source is the runner's pinned target:

```text
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c111dab58b0a8d55e991bbd2efe3aad56717b95a:tools/mutate-and-run.sh | sha256sum
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  -
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c111dab58b0a8d55e991bbd2efe3aad56717b95a:.ufo/evidence/round-31/c1-measure.py | sha256sum
657fcc1291d781577c20f4f0c4dc55feb84aadb38bce846bfdb296c7ef1e7584  -
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs | sha256sum
83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426  -
```

## Smallest safe correction

Reject symlinked `--work` and require its resolved path to be inside the authorized scratch root. Set every child `TMPDIR` to a private directory under that canonical work root (and remove hard-coded `/tmp` use from the invoked fixtures). To guarantee sibling/lane integrity even for an untrusted `--rev`, execute child commands in a filesystem sandbox where only the canonical work root is writable; staging sibling copies instead of symlinks alone does not prevent absolute-path writes.