# T48A2SentinelFixtures — fixture-commit leak audit (no fixture commit may leave a scratch clone)

Seat: T48A2SentinelFixtures (round 48, attempt 2, wave a2w1). Lane `tameshi-shokunin`, base
`473336d9d789f6081195e7376d17836a24666bc3`, content revision
`c7586b9a10effc63b4bd327f976edc094c1bdc17`. Lane HEAD during the audit `17cc5ce141868454d05bf75ef5cd230e35f0cdf4`.
Read-only on the lane checkout; the only files written are under
`.ufo/waves/round-48/a2w1/T48A2SentinelFixtures/`. Scratch root
`/fast/scratch/hyaku/tameshi-r48/T48A2SentinelFixtures` (deleted at end of seat). No tool was
installed or upgraded (nothing was needed).

Evidence files kept next to this report (`T48A2SentinelFixtures/`):
`identity-census.txt`, `fixture-commit-leak.txt`, `control-commit-provenance.txt`,
`c2-controls-reuse-demo.txt`, `c2-controls-gitdir-demo.txt`.

## Verdict

No round-48 control commit leaked into the lane or the fleet repo: every throwaway-identity
commit the two control harnesses made in this round landed in a clone under
`/fast/scratch/hyaku/tameshi-r48/L1/` and is absent from the lane object store (evidence
`control-commit-provenance.txt`). Two defects in `c2-controls.py` are, however, live
reproductions of the mechanism that *did* leak fixture commits into the lane on 2026-10-20
(lane HEAD reflog `HEAD@{307}: round-17 L1 repair: restore HEAD after R04 seat fixture commits
(GIT_DIR leak)`): the harness commits into any pre-existing repo named `<work>/lane`, and its
git calls are not environment-hermetic. Those three pre-existing `tameshi <tameshi@selftest>`
fixture commits are still in the lane store today and are invisible to the `git log --all`
command this item prescribes.

Severity key: **High** = can land a throwaway identity in the lane or destroy lane content;
**Medium** = hides or contaminates audit evidence; **Low** = hygiene / operability.

---

## 1. Identity census (item command, both repos)

Lane, exactly the item's command:

```
$ git -C tameshi-shokunin log --all --format='%H %an <%ae> %s' | awk '{print $2,$3}' | sort | uniq -c
   1161 tameshi-shokunin
    139 protocol-shokunin
      9 João Pedro
      4 Joao Pedro
```

The `awk` drops `%ae` (name + email is three fields for a two-word name), so it cannot see the
`@selftest` identity below; with `%an <%ae>` kept, the lane's reachable history has 5
author/committer identities: `tameshi-shokunin <tameshi@shokunin.local>` (1161 authors),
`protocol-shokunin <protocol@shokunin.local>` (139), `João Pedro Veiga <jpveigao10@gmail.com>`
(9), `Joao Pedro Veiga <jpveigao10@gmail.com>` (4) — the owner's personal reflection/README
commits — and nothing else. Full scan of **every commit object in the lane store** (1321
commits, reachable + unreachable) adds only `tameshi <tameshi@selftest>` ×3 (§2). No commit by
`tameshi-ctl <ctl@tameshi.invalid>` (run-controls.py) or `c2 control <c2@tameshi.invalid>`
(c2-controls.py) exists anywhere in the lane store.

Fleet repo, last 300 commits in both readings of "same": `git log --all -300` gives 11
identities (protocol 135, kasegi 30, tabi 24, kama 19, souji/kengaku 18, kaidoku 16, tsukuroi 15,
mado 9, tameshi/mori 8; window 2026-10-26 02:55 – 10:15), and plain `git log -300` (HEAD, which
trails `main`) gives 17 identities, all `*-shokunin <…@shokunin.local>`. No throwaway identity
in either.
Out of the item's 300-commit window but visible in full history, for the record only (predates
round 48, not fixture commits): `probe <probe@example.invalid>` (3 commits on `main`, e.g.
`9d9f181e41fe2a5d26ce7946d48769b61f816c19`) and `r20 <r20@example.invalid>` (19 commits, e.g.
`23753dbfa0aac72eb2f27d528dbd5db6667d5126`) — real orchestrator/lane content landed under
placeholder `example.invalid` identities (provenance defect, another round's surface).

## 2. FINDING S-1 (Medium) — three fixture commits by a throwaway identity sit in the lane object store, outside any scratch clone

```
$ git -C tameshi-shokunin reflog show HEAD | grep -E 'selftest-fixture|GIT_DIR leak'
98bea7d HEAD@{307}: round-17 L1 repair: restore HEAD after R04 seat fixture commits (GIT_DIR leak)
e16adb7 HEAD@{308}: commit: selftest-fixture-noexec
0559c60 HEAD@{309}: commit: selftest-fixture-exec
f8832ef HEAD@{310}: commit: selftest-fixture
$ git -C tameshi-shokunin fsck --unreachable --no-reflogs | awk '$2=="commit"'
… 0559c60abbed30367d620f1057face4644db1d3c (tameshi <tameshi@selftest>), e16adb7d8f4f…, f8832ef3…
```

- `f8832ef` (tree: `target.sh`), `0559c60` (adds `exec.sh`), `e16adb7` (adds `noexec.sh`), all
  dated 2026-10-20 12:29:33 -0300, identity `tameshi <tameshi@selftest>` — the fixture identity
  of `tools/mutate-and-run.sh:297`.
- `f8832ef`'s parent is `98bea7d`, a real lane commit: the three commits were made **on the lane
  branch** and excised; the reflog entry at `HEAD@{307}` names the cause (a seat's GIT_DIR leak,
  round-17 R04), so this is the exact defect class this seat audits, not a round-48 product.
- Observable consequence today:
  - the item's own check misses them — `git log --all` shows none of the three;
  - `git clone --shared` of the lane (the clone form this wave's bounds tell every seat to
    prefer) resolves them through `.git/objects/info/alternates`, so any seat's fixture audit of
    a shared clone sees fixture commits it never made (`fixture-commit-leak.txt`);
  - a `--no-local file://` clone does not carry them (`fixture-commit-leak.txt`).
- Remediation (owner action, not seat action): `git -C tameshi-shokunin reflog expire
  --expire-unreachable=now --all && git -C tameshi-shokunin gc --prune=now`; and change the
  audit recipe from `git log --all` to `git log -g --all` **plus** `git fsck --unreachable
  --no-reflogs` (objects only reachable from a reflog, or from no ref at all, are otherwise
  invisible).

Store-stability caveat measured during the audit: `pack-afa9552c…pack` was rewritten under me
(mtime 10:46:58 → 10:49:18) and resolution of `e16adb7` flipped between `commit` and `Not a
valid object name` between 10:44:33 and 10:50:41 while `fsck` and the reflog kept naming it.
Present at end of audit: `f8832ef`, `0559c60` readable; `e16adb7` named by reflog and fsck,
intermittently resolvable. The lane store is being repacked concurrently with the waves;
object-level fixture checks must be timestamped and retried (`fixture-commit-leak.txt`).

## 3. FINDING S-2 (High) — `c2-controls.py` commits into whatever repo already sits at `<work>/lane`

`c2-controls.py:157-164` (`clone_lane`) creates `<work>/lane` only `if not os.path.isdir(path)`
— no `--work` emptiness check, no `rev-parse --show-toplevel` check — and `c2-controls.py:174-182`
(`commit`) then runs `git checkout -q --detach BASE`, `git clean -qfd`, `git add -A`,
`git commit` in that repo with the throwaway identity `c2 control <c2@tameshi.invalid>`
(`c2-controls.py:52`).

Reproduced on a scratch repo that was not a clone of the lane (`c2-controls-reuse-demo.txt`):

```
$ mkdir -p <S>/reuse3/lane && git -C <S>/reuse3/lane init -q && … commit -m init   # dummy <dummy@invalid>
$ mkdir -p <S>/reuse3/lane/keepme && echo never-staged > <S>/reuse3/lane/keepme/untracked.txt
$ python3 .ufo/evidence/round-48/control/c2-controls.py --work <S>/reuse3 \
      --lane tameshi-shokunin --measure .ufo/evidence/round-48/freshness/measure.py
CTL_H refreshed=0
CONTROLS: F=0 G=0 H=0 expected=F0,G0,H<=2 ok=true
$ git -C <S>/reuse3/lane log --format='%h %an <%ae> %s'
4cfb7e9 c2 control <c2@tameshi.invalid> round-48 C2 control
24f71d0 c2 control <c2@tameshi.invalid> round-48 C2 control
706dd0b dummy <dummy@invalid> init
$ ls <S>/reuse3/lane/keepme/untracked.txt
ls: cannot access '…/keepme/untracked.txt': No such file or directory
```

Two fixture commits landed in a foreign repo, its untracked files were deleted by `git clean
-qfd`, and the harness exited 0 with `ok=true`. Exploit path against the lane:
`mkdir -p "$S" && ln -s "$LANE" "$S/lane"` then run the harness with `--work "$S"` —
`os.path.isdir` follows the symlink, so `commit()` detaches the lane's HEAD at BASE, deletes
untracked lane files (`clean -qfd`), and commits `c2 control` into the lane. `run-controls.py`
already contains the two defences this file is missing: it refuses a non-empty `--work`
(`run-controls.py:308-309`), refuses an existing destination (`run-controls.py:185-186`) and
verifies `rev-parse --show-toplevel` before the first commit (`run-controls.py:190-192`).
Smallest remediation: copy those three guards into `clone_lane`/`commit`.

## 4. FINDING S-3 (High) — `c2-controls.py` git calls are not environment-hermetic, so `-C` does not bind

`c2-controls.py:55-56` runs `subprocess.run(['git', '-C', repo] + args)` with the caller's
environment unchanged; there is no `child_env()` equivalent. `run-controls.py:60-66` strips every
`GIT_*` variable before spawning git — the fix that was added after the round-17 leak precisely
because `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` override `-C`.

Reproduced (`c2-controls-gitdir-demo.txt`), all scratch:

```
$ env GIT_DIR=<S>/hijack/.git python3 .ufo/evidence/round-48/control/c2-controls.py \
      --work <S>/ctl_gd2 --lane tameshi-shokunin --measure .ufo/evidence/round-48/freshness/measure.py
CTL_H refreshed=2
CONTROLS: F=0 G=0 H=2 expected=F0,G0,H<=2 ok=true
$ git -C <S>/hijack log -2
0e055d7 c2 control <c2@tameshi.invalid> round-48 C2 control
473336d protocol-shokunin <protocol@shokunin.local> round-47 verifier spot-check …
$ git -C <S>/ctl_gd2/lane log -2      # the harness's own clone
17cc5ce …  c7586b9 …
$ git -C <S>/ctl_gd2/lane status --porcelain | head -2
 D .ufo/evidence/round-48/before/coldread-sections-at-base.stdout
 D .ufo/evidence/round-48/calibration/emit-15b1521.end
```

With `GIT_DIR` exported, the CTL_G/CTL_H fixture commits landed in the `GIT_DIR` repo instead of
`<work>/lane`, the clone's worktree was checked out/cleaned against the `GIT_DIR` repo's index,
and the harness still printed `ok=true`. Pointing `GIT_DIR` at `tameshi-shokunin/.git` would
therefore detach the lane's HEAD, rewrite its index and land `c2 control` commits in the lane —
the round-17 failure named at `HEAD@{307}` — with a passing control verdict. `GIT_INDEX_FILE` and
`GIT_WORK_TREE` have the same reach (`env GIT_DIR=… git -C tameshi-shokunin rev-parse
--absolute-git-dir` returned the `GIT_DIR` path, not the lane's).

## 5. FINDING S-4 (Low) — scratch-bound guards are advisory, and absent on one harness

- `c2-controls.py:208-209` (`os.makedirs(work, exist_ok=True)`) has no `/fast/scratch` check and
  no emptiness check; `--work` inside the lane would create/populate a clone inside the lane
  checkout.
- `run-controls.py:306-307` only prints a note when `--work` is outside `/fast/scratch`; it does
  not refuse, and it does not check that `--work` is outside the lane. Its clone destination at
  `run-controls.py:187` is otherwise safe (fresh path, `rev-parse` guard, `GIT_*` scrub).
- Leftover trees from the recorded round-48 control runs are still on disk:
  `/fast/scratch/hyaku/tameshi-r48/L1/ctl/CTL_A…E` and `L1/c2ctl/lane` (3.0 G under `L1`; 21.5 G
  for the whole round-48 scratch root at audit time). Not a repo leak (all six heads are absent
  from the lane store), but a leftover-tree defect under this wave's bounds.

## 6. Clean bill — `run-controls.py` (C1 controls)

Every git call names its clone: `git(tree, …)` → `['git','-C',tree,…]` (`run-controls.py:89-90`),
`git_show` (`:96-97`), `add -A` (`:219`), commit with inline `-c user.name=tameshi-ctl -c
user.email=ctl@tameshi.invalid -c commit.gpgsign=false` (`:220-222`). The one call without `-C`
is `git clone -q --shared LANE dest` (`:187`), which is the correct form for a clone — `dest` is
`<work>/CTL_X`, the source is only read, and `child_env()` (`:60-66`) scrubs `GIT_*` first. All
writes are under `--work`: `append_scorecard` (`:198-201`), `install_counter` (`:210-215`),
`run_counter` stdout/stderr (`:243-256`), `shutil.rmtree(rundir)` (`:247`). Both the clone-time
`rev-parse --show-toplevel` check (`:190-192`) and the fresh-destination check (`:185-186`)
precede any mutation. Reading its only results-bearing artefact, the recorded runs committed
`tameshi-ctl` heads `a1b266e/c0389ca/a8bacc8/a6516c5/c6c94c2` inside `L1/ctl/CTL_*`, each
`toplevel` equal to its own directory, each absent from the lane store.

Recorded C2 control run (`control/c2-controls.stdout`, `control/c2-controls.meta`): work
`/fast/scratch/hyaku/tameshi-r48/L1/c2ctl`, revs `a865909b…` (CTL_G) and `b83f2424…` (CTL_H) —
both absent from the lane store; `L1/c2ctl/lane` toplevel is itself, so that invocation was safe.
The defects in §3–§4 are latent in the hire, not exercised by the receipt.

## Reproduce

```
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
git -C "$L" log --all --format='%H %an <%ae> %s' | awk '{print $2,$3}' | sort | uniq -c
git -C "$L" reflog show HEAD | grep -E 'selftest-fixture|GIT_DIR leak'
git -C "$L" fsck --unreachable --no-reflogs | awk '$2=="commit"{print $3}'
git -C /home/vgpnk/Projects/shokunin log --all -300 --format='%H %an <%ae> %s' | awk '{print $2,$3}' | sort | uniq -c
# S-2 / S-3: run .ufo/evidence/round-48/control/c2-controls.py with --work on a scratch dir whose
# <work>/lane is a foreign/symlinked repo, and once with GIT_DIR exported (see the two demo files).
```
