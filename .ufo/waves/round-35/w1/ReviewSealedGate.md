# ReviewSealedGate — audit of the C1 sealed-provenance gate (round 35 w1)

Seat: `tameshi-r35-w1-ReviewSealedGate` (leaf). Pin: `d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc` (lane tip at dispatch; the round-35 freeze commit).
Scope: the sealed-provenance gate in `.ufo/evidence/round-35/c1/c1-measure.py` (sha256 `78bb43ebf3d2a313951d9d89f470f2543023b1605326fe676eef3cdb7a947ef9` at the pin), checked against the round-34 PanelSeed4 F2 routing (last-modify, not first-add; round-34.md append item 2). Frozen artifacts read-only; all scratch under `/fast/scratch/hyaku/tameshi-r35-seats/ReviewSealedGate/`.

## The gate as implemented (c1-measure.py:345-363)

- Manifest-declared freeze: `freeze_rev = manifest.get('freeze_rev','')` (line 352); global check `git merge-base --is-ancestor <freeze_rev> <rev>` (line 353).
- Per sealed copy file: `fpath = '.ufo/evidence/round-35/c1/sealed/<file>'` (line 355, hardcoded); `last = git log -1 --format=%H -- <fpath>` (lines 356-357, no `--follow`); fail unless `git merge-base --is-ancestor <freeze_rev> <last>` (line 358).
- No `git status`/worktree-cleanliness check, no blob-binding of `last`→`rev`→disk anywhere in the counter (verified by full read; grep for `follow|git status|--porcelain` returns only the lines above).

**What the gate actually proves:** for each sealed JSON file, the commit selected by `git log -1` at the checkout HEAD (default traversal order, path-limited, rename-blind) that touches that path is at-or-after the *manifest-declared* `freeze_rev` in the ancestry of `rev`. It does not prove the file's bytes were authored after the freeze; it only certifies that a post-freeze commit touched the path (or that the declared freeze is old enough).

## Findings (ranked)

### BOUND-1 (FAIL-OPEN) — freeze identity is unauthenticated; the gate is vacuous under adversarial manifest
`freeze_rev` comes from the L1-authored `manifest.json`; nothing binds it to the actual freeze commit (`d16f9b5`, where contract.json and the counters landed — `git log --oneline -- .ufo/evidence/round-35/contract.json` = only `d16f9b5`). Any ancestor works, including the copies' own commit.
Reproduction (scratch `w4`):
```
$ git init -q w4 && cd w4
$ mkdir -p .ufo/evidence/round-35/c1/sealed
$ echo ADAPTED_TO_COUNTER > .ufo/evidence/round-35/c1/sealed/copy.json
$ git add -A && git commit -qm copy_authored_BEFORE_real_freeze
$ C=$(git rev-parse HEAD)                 # copy commit (pre-freeze)
$ git commit --allow-empty -qm the_real_freeze_lands_later
$ git merge-base --is-ancestor $C $C; echo $?    # -> 0 (equality accepted)
$ git merge-base --is-ancestor $C HEAD; echo $?  # -> 0 (copy is ancestor of rev)
$ git merge-base --is-ancestor $(git rev-list --max-parents=0 HEAD) $C; echo $?  # -> 0 (root-as-freeze)
```
All three exit 0 → the gate passes for a copy committed BEFORE the real freeze if the manifest declares `freeze_rev` = that copy's commit (or any of its ancestors). The per-file branch (line 358) has the same shape. The claim clause "sealed set authored after this freeze" (contract.json:28) is therefore not enforced; it relies entirely on the L1 not lying in its own manifest.

### BOUND-2 (FAIL-OPEN) — last-modify measures *touch*, not *authorship*: move/copy defeats
Because `git log` runs without `--follow`, a rename counts as a modify of the new path, and a copy from any sibling branch produces a fresh post-freeze commit. Pre-freeze content passes through both.
Move reproduction (scratch, rerun in /tmp due to /fast exhaustion; see note):
```
$ mkdir -p .ufo/evidence/round-35/c1/{elsewhere,sealed}
$ echo PREDATES_FREEZE > .ufo/evidence/round-35/c1/elsewhere/copy.json
$ git add -A && git commit -qm prefreeze_content_at_other_path
$ F=$(git rev-parse HEAD)                   # freeze
$ git mv .ufo/evidence/round-35/c1/elsewhere/copy.json .ufo/evidence/round-35/c1/sealed/copy.json
$ git commit -qm moved_into_sealed_after_freeze
$ last=$(git log -1 --format=%H -- .ufo/evidence/round-35/c1/sealed/copy.json)
$ git merge-base --is-ancestor $F $last; echo $?    # -> 0: GATE PASSES (content predates freeze)
$ git rev-parse $last:.ufo/evidence/round-35/c1/sealed/copy.json   # b190c246a4ec6b8d39a1a5c92fa3eebd5074a165
$ git rev-parse $F:.ufo/evidence/round-35/c1/elsewhere/copy.json   # b190c246a4ec6b8d39a1a5c92fa3eebd5074a165 (identical blob)
```
Copy reproduction (scratch `w2`): content committed on a sibling forked before the freeze (`e3c2eed…`); copied in post-freeze via `git checkout sib -- <path>` + commit; `last=240fd0ab…`, `git merge-base --is-ancestor $F $last` → exit 0 (gate passes).
Contrast — the lineage-first-add check closes both: `git log --follow --diff-filter=A -1 --format=%H -- <path>` returns the original creation commit (pre-freeze in both cases); with a distinct freeze commit, `git merge-base --is-ancestor $F $origin` → exit 1 (FAIL, correctly) — verified with freeze=`cef067be…`, origin=`9cfea25a…`, move=`fdaeb1fb…`.

### BOUND-3 (FAIL-OPEN) — same-commit equality accepted
`git merge-base --is-ancestor X X` exits 0, so a sealed copy committed *inside the freeze commit itself* passes.
Reproduction (scratch `w3`): one commit containing both `counter.py` and `sealed/copy.json`; `last == freeze == 5f3e0aa…`; `git merge-base --is-ancestor $F $last; echo $?` → `0`.

### BOUND-4 (FAIL-OPEN) — dirty worktree / disk-vs-rev unbound
Provenance reads history; scoring (`load_copies` → `score_copies`) reads the working-tree files. An uncommitted edit to a sealed copy passes the gate while the scorer uses the edited bytes.
Reproduction (scratch `w6`): commit benign post-freeze copy → gate exit 0; overwrite the working-tree file with attack content → gate still exit 0 (`git merge-base --is-ancestor $F $last` = 0) while `git status --porcelain -- <path>` prints ` M …`.

### BOUND-5 (FAIL-CLOSED) — `git log -1` ordering is date-based across merge frontiers
In a linear history, topology forces the genuine post-freeze touch to be selected (verified: forged future committer date on a pre-freeze commit did not shadow the post-freeze touch; `git log -1` selected the post-freeze commit). Across merged branches the frontier is walked by commit date, so an anachronistically-dated pre-freeze touch (clock skew or `GIT_COMMITTER_DATE`) can be selected, making the gate fail despite a genuine post-freeze touch. This direction cannot manufacture a false PASS: any selected commit that descends from the declared freeze is genuinely post-freeze; anything else fails the gate (fail-closed).

### HYGIENE-1 — manifest.json is parsed as a specimen
`load_copies` (lines 195-211) treats every `*.json` in the sealed dir as a copy. A natural manifest `{"freeze_rev": …}` (no `copies` key) becomes a specimen and crashes the counter at `distinct_bodies` (`KeyError: 'edits'`, line 272) — reproduced by importing the counter and running `load_copies`/`distinct_bodies` on a temp dir containing only `manifest.json`. Only a manifest carrying a `copies` key is skipped safely. This aborts the measurement after the provenance block, so the gate itself still runs first — but the run dies.

### HYGIENE-2 — hardcoded fpath ignores `--sealed`
Line 355 hardcodes `.ufo/evidence/round-35/c1/sealed/<file>` regardless of the `--sealed` argument (resolved at line 346). Running with a non-canonical `--sealed` scores different bytes than the provenance check inspects (fail-closed if the canonical path lacks the files, blind if it contains different ones).

### HYGIENE-3 — provenance walks the checkout HEAD, not `--rev`
`git log` (line 356) runs against the lane checkout's HEAD; the resolved `rev` is only used for content and for the manifest-level ancestor check. If the checkout is not exactly at `rev`, the per-file gate inspects a different history.

## What I could NOT break (proofs)

- **Pinned byte integrity at `d16f9b5`:** `git show HEAD:tools/tally-audit-v3.py | sha256sum` = `da23d3a25271072cae4cfd977cf3aeca531ef97e0abcd913890b3710cfa9a16f`; `git show HEAD:tools/mutate-and-run.sh | sha256sum` = `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`; counter blob = `78bb43ebf3d2a313951d9d89f470f2543023b1605326fe676eef3cdb7a947ef9`. All match the frozen pins.
- **Fail-closed paths:** an untracked sealed copy → `git log -1` empty → `not last` triggers (exit 128/flag; reproduced); a missing manifest → `sealed_ok=False` (lines 361-363); an unresolvable `freeze_rev` → `git_ok` false → fail. These are the only ways the gate can currently fail, and they are all conservative.
- **Current claim status:** no claim is false today — no measurement has run; the sealed dir is ABSENT at the pin (`git ls-tree -r --name-only HEAD -- .ufo/evidence/round-35/c1/` lists only the counter + 6 panel jsons; `.ufo/evidence/round-35/c1/sealed/` does not exist). Panel files' last-modify = `d16f9b5` (the freeze commit itself). All weakness reproductions are synthetic.
- **No date-forgery false-PASS** (see BOUND-5).

## What round 36 should tighten

1. **Bind freeze identity:** resolve the freeze from repo metadata (e.g. `git log -1 --format=%H -- .ufo/evidence/round-35/contract.json`) and require the manifest's `freeze_rev` to equal it; reject mismatch.
2. **Strict descent:** require `git merge-base --is-ancestor $FREEZE $last && [ "$FREEZE" != "$last" ]` (or `git rev-list --count $FREEZE..$last` > 0) to close same-commit.
3. **Authorship anchor:** gate on lineage first-add `git log --follow --diff-filter=A -1 --format=%H -- <fpath>` against that freeze (this is what PanelSeed4 F2's first-add intent actually requires — compared with the *final* counter-bytes commit, not the first commit), keeping last-modify as a secondary guard.
4. **Content binding:** require `git rev-parse $rev:<fpath>` blob == the hash of the bytes `load_copies` reads, and reject a dirty worktree (`git status --porcelain` non-empty) before scoring.
5. **De-couple path:** derive `fpath` from the resolved `sdir` (and validate `--sealed` against the canonical location).
6. **Manifest schema check:** skip `manifest.json` in `load_copies` explicitly (or require the `copies` key) so a plain manifest cannot crash the run.

## Notes
- `/fast` reached 100% (804G/804G, <100KB free, inodes 99.9%) mid-audit; two reproduction commands (W1 move, strict contrast) were rerun in `/tmp` (92G free) and deleted after capture. Scripts retained at `/fast/scratch/hyaku/tameshi-r35-seats/ReviewSealedGate/scratch/wk.sh` (W2-W7) and `wk2.sh` (W1/W5-merge; superseded by the /tmp reruns).
- No installs performed; no `pacman`; no mutations of any pinned artifact, the lane, or the fleet repo.
