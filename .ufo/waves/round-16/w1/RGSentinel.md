# RGSentinel — C1 safety review: round-gate.mjs `--selftest` under tools/mutate-and-run.sh

Seat: TameshiR16.RGSentinel (sentinel, read-only review; no lane/sibling file edited; no mutant run).
Target: kumitate-shokunin `scripts/round-gate.mjs` @ `364f1d5954158ef8844bca4a5fef57b05d2f2ca5`
(blob mode 100755, 1511 lines), runner `tameshi-shokunin/tools/mutate-and-run.sh` (working tree, 1642 lines)
plus the wave-1 draft `.ufo/waves/round-16/w1/RGLeg.mutate-and-run.sh` (js-round-gate leg).
Scratch: `/tmp/tameshi-r16-RGSentinel-52LR/` (all experiments below ran the **pristine** blob only).
Tools installed/updated: none (strace, bwrap, unshare, git 2.56.0, node v24.21.0 already present).

## Materialization (verified)

```
git -C kumitate-shokunin show 364f1d59…:scripts/round-gate.mjs > /tmp/tameshi-r16-RGSentinel-52LR/round-gate.mjs
sha256sum → f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9   (= recorded pin)
git ls-tree 364f1d59 scripts/round-gate.mjs → 100755 blob 1f7d623e…
```

Baseline (pristine, `TMPDIR=<scratch>`, cwd=<scratch>, under `strace -f -e trace=%file,%network,execve`):
exit 0, `ROUND_GATE_SELFTEST: 60/60 pass`, `VERDICT: PASS`, ~7 s traced (~2–4 s untraced); TMPDIR left empty.

## Answers to the four questions

| Question | Answer (pristine) | Evidence |
|---|---|---|
| Writes outside its temp dir? | **No** in a normal env; **YES if `GIT_DIR` is inherited** (S1) | strace: 0 writes outside scratch; E1b below |
| Reads live fleet trees (`~/Projects/ufo-fsd-alpha` via UFO_SRC/default)? | **stat only** (26× `access(F_OK)`), never a git probe; mutants can escalate (S4) | strace classification; `round-gate.mjs:161-166,293-297` |
| Touches the network? | **No** | 0 `socket`/`connect` in three traces; imports `:130-137` only `child_process`,`fs`,`os`,`path`,`url`; pushes are local-path transports (`/bin/sh -c git-receive-pack '/tmp/…'`) |
| Depends on HOME / cwd? | cwd: **no**; HOME: only via the derived-origin stat and host git config of gate children; TMPDIR and several env vars **change the verdict** (S3) | E2, E3, strace |

## Findings

### S1 — HIGH (conditional): inherited `GIT_DIR` makes the *control run* commit into a foreign repo

- Exploit path: `run_one` hands the suite the runner's full environment (`mutate-and-run.sh:394-395`,
  `MUTANT=… … timeout "$TIMEOUT_S" bash -c "$SUITE"` — no env filtering anywhere; `grep -nE 'unset|GIT_DIR|GIT_INDEX|GIT_WORK|env -i|TMPDIR|HOME'`
  over the runner matched only two unrelated spec-heredoc lines, 747-748). The selftest builds its fixture git env as
  `GIT_ENV = { ...process.env, GIT_CONFIG_GLOBAL: '/dev/null', … }` (`round-gate.mjs:704-710`) and every fixture
  `git init/add/commit/push` uses it (`:717-720`). `git -C <fixture>` does not override an exported `GIT_DIR`.
  Any invocation of `mutate-and-run.sh` from a context that exports `GIT_DIR` (a git hook, a shell that exported it)
  therefore commits fixture commits into that repository — on the **pristine control run**, before any verdict.
- Evidence E1b (canary repo under scratch, pristine blob):
  ```
  GIT_DIR=/tmp/…/e1b/live/.git TMPDIR=/tmp/…/e1b/tmp node <pristine> --selftest  → exit=1
  Error: fixture lane commit failed: exit 1
  HEAD before=fa797421e53034998fa5e49428d8e9d2dce4b9cf
  HEAD after =b8ed57b826cc76caf72d7b1bf0d5de012bf4afc6
  log: b8ed57b round-5 fixture seed / 940704f round-5 fixture report / 31b1041 round-5 fixture seed / …
  git ls-files → LOG.md, SCORECARD.md   (the canary's own LIVE.txt is gone from its index)
  ```
  E1 (bare canary as GIT_DIR): exit 1, `fatal: this operation must be run in a work tree`, canary commits 0.
- Impact: live repo history and index rewritten by fixture content (same mechanism applies to
  `GIT_WORK_TREE`/`GIT_INDEX_FILE` — **[INFERENCE]**, not separately executed). Mutants inherit the same env.
- Smallest remediation: `env -i` in the suite string (guard G1 below). E6 proves the guard neutralizes it.

### S2 — MEDIUM (mutant-borne): `rm -rf` reach of `rmSync(tmp)` is the shared `/tmp`

- `selfTest` scratch is `mkdtempSync(join(tmpdir(), 'kumitate-round-gate-selftest-'))` (`:690`) — under
  `os.tmpdir()` (= `$TMPDIR` else `/tmp`), **not** under the runner's `$WORKDIR`; cleanup is
  `rmSync(tmp, { recursive: true, force: true })` (`:1495`). A single-edit mutant on either path expression
  (e.g. `rmSync(join(tmp, '..'), …)`) recursively deletes the shared tmp root: other seats' `/tmp/tameshi-r16-*`
  scratch and the runner's own `$WORKDIR` (pristine + remaining mutants → later rows 127/INCONCLUSIVE,
  `MUTATE_RESTORE` drift). Not present in the drafts visible to me (RGSpecB B1–B3 edit fail-closed tokens;
  RGLeg D10 swaps `SRC_CANDIDATES` `:151-152`) — this is a spec-review rule, not an observed defect.
- Remediation: G1's private `TMPDIR` bounds a one-level `..` to the sandbox; plus spec-review rule G3.

### S3 — MEDIUM (reproducibility): the measured verdict depends on runner env

- `KUMITATE_ROUND_GATE_NESTED=1` inherited → hermeticity check [51] is SKIPped and counted as pass
  (`:1381-1382`, `results.push({… ok: true, skipped: true …})`). E3: `exit=0`, `SKIP [51/60] hermeticity: nested --selftest …`,
  `60/60 pass`. A mutant killed only by the nested re-run would flip KILLED→SURVIVED on such a host.
- `TMPDIR` inside any git work tree → git discovery from the "non-git" fixture dirs walks up into that tree.
  E2 (TMPDIR inside a scratch work tree): `exit=1`, `57/60`, FAIL [37] `MAIN_REPO_NOT_GIT` (`:1215-1220`),
  FAIL [56] `--tracked … MAIN_REPO_NOT_GIT` (`:1445-1452`), FAIL [51] nested; the scratch tree's HEAD unchanged
  (read-only). Under the runner this turns the control RED → SETUP. Baseline trace shows the walk-up
  (`newfstatat("/tmp/.git") = -1 ENOENT`, 4×).
- Gate children (`runGate`, `:725-726`) get `cleanEnv()` = `process.env` minus 4 keys (`:711-716`) and no
  `GIT_CONFIG_GLOBAL` override, so they read host git config: baseline trace `/home/vgpnk/.gitconfig` 706 opens,
  `/home/vgpnk/.config/git/config` 1608, `/etc/gitconfig` 804 (absent). Host-config-sensitive mutants
  (e.g. on `GIT_ENV` `:704-710`) become host-dependent. 271 inherited env vars observed on spawned children
  (strace `/* 271 vars */`).
- Remediation: G1 (also pins `LC_ALL=C` so git stderr matched by e.g. `:1212` `/no upstream|exit 128/` is not
  locale-translated — **[INFERENCE]**, not executed under another locale).

### S4 — LOW: live `~/Projects/ufo-fsd-alpha` is stat'ed; mutants can turn it into a git read

- `~/Projects/ufo-fsd-alpha` exists on this host. `parseArgs` resolves the origin default for every non-selftest
  child without `--origin` (`:293-297` → `resolveSrcDefault` `:161-166`, candidates `:150-153` from `homedir()`).
  Calls without `--origin`/HOME override: fcA `:1186`, fcB `:1191`, fcC `:1196`, r44 `:1291`, `--tracked` arms
  `:1408-1477`. Baseline strace: `26 access("/home/vgpnk/Projects/ufo-fsd-alpha", F_OK) = 0` and **no** git
  execve with `-C` outside scratch (all `git -C /tmp/tameshi-r16-RGSentinel-52LR…`).
- Escalation by mutant **[INFERENCE from code]**: dropping the `HOME:` override at `:1347`/`:1354`/`:1369`, or
  `--origin` from `auditArgs` (`:853-854`), sends a child to the live origin; for tokens unresolved in lane/main it
  runs read-only `git cat-file -e`/`merge-base` there (header `:110-112`). Read-only, but a live-tree read.
- Remediation: G1's `HOME="$h/home"` (E4/E6: zero `/home/vgpnk/Projects/*` paths touched by the gate).

### S5 — LOW: timeout leaks the selftest scratch

- `timeout` SIGTERM skips the `finally` at `:1494-1496`. E5: `TMPDIR=<scratch> timeout 1 bash -c 'node … --selftest'`
  → `exit=124`, leftover `kumitate-round-gate-selftest-Eg7jDY` (1 dir), orphans 0 (process group killed).
- Remediation: G1 puts it under `$WORKDIR/sandbox-<id>/tmp`, removed with the case root on PASS.

### S6 — INFO: cwd and HERE-derived defaults

- cwd: the gate never reads `process.cwd()` (contract `:52-55`; no `cwd(` call in code); runs from two different
  cwds were identical. `run_one` does not `cd` (`:391-399`).
- `DEFAULT_REPO = realpath(HERE/..)` (`:193`), `DEFAULT_MAIN_REPO = HERE/../..` (`:142`), reports default `:143`.
  The mutant lives at `$WORKDIR/mutant-<id>.target.round-gate.mjs` (`mutate-and-run.sh:454`), so with the default
  `/tmp/tameshi-r4-2-regression.*/js-round-gate` workdir these resolve to `/tmp/tameshi-r4-2-regression.*` and `/tmp`
  (`/tmp/.ufo` absent; `/tmp` not a work tree). In the pristine run every default-using child fail-closes before a
  git probe. If `--workdir` were placed inside the lane tree, the defaults would name live lane dirs → keep G2.
- Materialization side (`mutate-and-run.sh:932-937`, `git -C "$repo" show`) is read-only on sibling repos.

## Guards for L1 (bounded)

**G1 — suite string (use the identical literal for the measuring sweep AND the RGLeg ledger leg, replacing
`'node "$MUTANT" --selftest'` at RGLeg draft `:1163`):**

```
'h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" node "$MUTANT" --selftest'
```

`$WORKDIR`/`$DEFECT_ID` are exported by `run_one` (`:394`); in the ledger the sub-sweep's workdir is the case dir
(`--workdir "$cwd"`, `:978`), so sandboxes are removed with the root on PASS. `PATH="$PATH"` expands before `env -i`
so node/git resolution is unchanged (node here comes from a per-session fnm path).

E6 — G1 executed as the CONTROL row exactly as `run_one` would (pristine blob, poisoned env:
`GIT_DIR=<canary>/.git KUMITATE_ROUND_GATE_NESTED=1 UFO_SRC=$HOME/Projects/ufo-fsd-alpha TMPDIR=<inside canary work tree>`):
```
E6 guarded-suite exit=0
ROUND_GATE_SELFTEST: 60/60 pass        (no SKIP line)
VERDICT: PASS
live HEAD unchanged: yes ; canary status clean
/home/vgpnk/Projects/* touched: 1 (newfstatat by the outer `bash -c` on inherited PWD, before env -i)
net: 0 ; sandbox tmp leftover: 0
```
E4 (plain `env -i` run, same shape): exit 0, 60/60, only `/home/…/fnm/…/node` touched, net 0.

Interface consequence: the verdict table is a function of the suite string, so pre-registered predictions and the
recorded `TABLE_ROUNDGATE` must be measured under G1, and the ledger leg must carry the same literal; a sweep
measured with the bare suite and replayed with G1 (or vice versa) is not the same experiment.

**G2 — workdir:** keep the default `mktemp -d /tmp/…` workdir (no `--workdir` inside the lane or any repo).

**G3 — spec review rule:** reject any `@old` touching the scratch/cleanup path expressions at `:690` / `:1495`
(G1 contains a one-level `..`, not `../..` which reaches `$WORKDIR`). Untested stronger option if such a mutant is
wanted: wrap in `bwrap --ro-bind / / --tmpfs /tmp --bind "$h" "$h" --unshare-net` (bwrap present at
`/usr/bin/bwrap`; **not executed**).

Not checked: the six existing legs' suites share the same unfiltered-env exposure in `run_one` (**[INFERENCE]**,
same code path; their targets were not reviewed).
