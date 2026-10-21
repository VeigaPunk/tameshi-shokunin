# RevRunnerHash — runner_sha256_clone_copy vs replay-revision blob

## Verdict

**HOLDS.** `observations.json:runner_sha256_clone_copy` = `cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad` is byte-identical to sha256 of the `tools/registry-check.py` blob at the replay revision `d2eaecd443bf5f4e387e7e5331282e3d11dea047`. The copy that ran is the **fresh clone working-tree copy** at `/tmp/tameshi-registry-replay-dzo3ypiq/fleet/tameshi-shokunin/tools/registry-check.py`, checked out detached at that revision inside the replay's tempdir — not the main checkout copy.

## Which copy ran

`tools/registry-replay.py:152-166` (observed): `run_replay` clones `args.repo` into `TemporaryDirectory(prefix='tameshi-registry-replay-')`, does `git checkout --quiet --detach <revision>` in the clone, hard-fails if clone HEAD ≠ revision (`registry-replay.py:158-160`), then:

- `registry-replay.py:162-163`: `runner_path = clone / 'tools/registry-check.py'`; `runner_sha = sha256(runner_path.read_bytes())` — recorded as `runner_sha256_clone_copy` at line 177.
- `registry-replay.py:164-166`: the **same** `runner_path` is loaded via `importlib.util.spec_from_file_location` + `exec_module`, and `module.run_row(...)` is invoked per requirement (lines 168-174). Hash and execution read the identical path with no gap, so the recorded digest describes exactly the executed bytes.

Replay clone is the tempdir path in `observations.json:cwd` (`/tmp/tameshi-registry-replay-dzo3ypiq/fleet/tameshi-shokunin`); that tempdir has since been removed by `TemporaryDirectory` cleanup (direct re-hash impossible), but the recorded hash was captured from the live clone file immediately before loading it.

## Evidence

Replay revision: `observations.json:revision` = `d2eaecd443bf5f4e387e7e5331282e3d11dea047` = `--rev` in the same file's `argv`; `replay-command.json` (context listing) records the same. Current repo HEAD = `c8c5b88c8e961a929cdc351b95a7074c76958909` (post-delivery).

Commands (all read-only, `GIT_OPTIONAL_LOCKS=0`, run in `/home/vgpnk/Projects/shokunin/tameshi-shokunin`):

```
git cat-file -t d2eaecd443bf5f4e387e7e5331282e3d11dea047
→ commit
git ls-tree d2eaecd443bf... -- tools/registry-check.py
→ 100755 blob 08ac9cd14c3aa63cb2f50c3b8f3de1f08b7e3e3e
git show d2eaecd443bf...:tools/registry-check.py | sha256sum
→ cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad
git show HEAD:tools/registry-check.py | sha256sum
→ cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad
sha256sum tools/registry-check.py            # working tree
→ cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad
```

`runner_sha256_clone_copy` (observations.json) = `cba16646…944ad` — matches all three. Git blob oid is the same at replay rev and HEAD (`08ac9cd14c3a…`), i.e. the runner file did not change between the replayed revision and the delivered revision; working tree is clean for this path (`git status --porcelain` empty). Hash-and-execute use the same `runner_path` string sequentially, so no race/aliasing gap. A checkout filter that mutated bytes would have shown up as hash inequality against the blob; equality is therefore direct byte proof, not name coincidence.

## Falsification notes (counterexample hunt)

- Tried: rev other than the one replayed — no; `revision`, `argv[].rev`, and clone-HEAD assert agree.
- Tried: hash of a different copy standing in (repo working tree instead of clone) — code path hashes `clone/tools/registry-check.py` only (`registry-replay.py:162`); the equality is against the clone copy by construction.
- Tried: clone cleanup making the claim unverifiable — the field is recorded at run time from the executed file; re-hashing the removed tempdir is unnecessary for the claim.
- No defect found. Checked: observations.json fields, registry-replay.py:135-180, blob/exe hashes at three levels.

## Correction

None required. Note for the record: the round-24 replay directory contains `observations.json`, `bundle.json`, `expected.json`, `live-dependent.json` — files named `replay-command.json` / `replay-gate.json` in the wave context are not present at that path (out of my item's scope; flagged for whoever owns those paths).

Tooling directive: no tools installed or upgraded for this item.
