# RevengerV1Frozen — was the round-35 v1 counter REALLY left frozen?

Round 36, wave 1, leaf seat (read-only). Attacked: **`.ufo/evidence/round-35/c1/c1-measure.py`** (v1 C1 counter, claimed frozen at round-35 A8) and the **v1 → v2 delta** (`/.ufo/evidence/round-36/c1/c1-measure-v2.py`, claimed = docstring + constants + predicate only).

Repo: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (jj-colocated; HEAD detached at `d9c496b19371b779ce0eec6dfee1b049b27a3a2d`, "round-36: receipts …", 2026-10-24 03:21:45 -0300).

**VERDICT: FREEZE CONFIRMED — the v1 counter is byte-identical to the last round-35 commit (blob `ede608ea`), no commit on any ref touched it after `5829676` (round-35 A8, 2026-10-23 19:33:49 -0300 committer date), and v2 differs from v1 in exactly 6 hunks, all inside the documented delta (docstring, constants, predicate + its mandatory identifier rename). No unexplained hunk. High confidence — object-level evidence, not names.**

## 1. Every historical blob of the v1 counter

Enumerated with `git rev-list --all --objects -- .ufo/evidence/round-35/c1/c1-measure.py` (covers every tree reachable from every ref: master, origin/\*, refs/jj/keep/\* — several hundred refs). Exactly **6 distinct blobs** ever committed at this path:

| # | blob (git sha1) | sha256(content) | lines | first committed | commit | subject (round-35 re-pin) | what changed vs previous blob |
|---|---|---|---|---|---|---|---|
| 1 | `625025c2eb26…` | `78bb43ebf3d2a313…` | 397 | 10-23 17:31:25 | `d16f9b5` | "round-35: tally-audit-v3 … + C1/C2 counters frozen" | (initial freeze) |
| 2 | `2252e0892104…` | `50398b3d13ea1131…` | 464 | 10-23 18:23:36 | `7267738` | A4/A5 amendments | `CONFIGS` gained real-auto-root slots (`None`, `auto_root()`); `atexit`/`tempfile` imports |
| 3 | `fd899eca91a3…` | `515b0b1b00b970f3…` | 464 | 10-23 18:25:48 | `23bd903` | "counter A5 fix — real auto-root interpolation in run_block" | `root_s, auto_s, keep_s = cfg_root(cfg), cfg[1], cfg[2]` |
| 4 | `e35024ed85c4…` | `d27e6769c0def379…` | 464 | 10-23 18:30:28 | `f9df589` | A6 re-pin | `TOOL_SHA256`: `da23d3a2…` → `ef98fc53…` ("v3 after A4") |
| 5 | `124b67b96925…` | `44f05be2deb7958a5…` | 536 | 10-23 18:56:12 | `691bb51` | A4–A7 re-pin | A7 locator head-rule notes, `/tmp/tally-audit-explicit` config, mktemp-shape-matching loop |
| 6 | `ede608ea229b…` | `d360a159a1ad320e…` | 535 | 10-23 19:33:48 | `5829676` | **A8 re-pin (final round-35 version)** | `TOOL_SHA256`: `ef98fc53…` → `6188db16…` ("v3 after A7 (final bytes)"); vestigial `FREEZE_REV = '__FREEZE_REV__'` line removed |

The pre-data evolution (blobs 1→6) is round-35's own documented A5/A6/A8 re-pin sequence — each has a matching commit message; nothing in it postdates round 35.

## 2. Working copy == committed round-35 version

- `git hash-object .ufo/evidence/round-35/c1/c1-measure.py` = `ede608ea229bd84c1e8e85b72671b637120c0490` = `git rev-parse HEAD:.ufo/evidence/round-35/c1/c1-measure.py` — working copy, index, and HEAD blob are the same object.
- `git cat-file blob HEAD:.ufo/evidence/round-35/c1/c1-measure.py | cmp - .ufo/evidence/round-35/c1/c1-measure.py` → **byte-identical**.
- `GIT_OPTIONAL_LOCKS=0 git status --porcelain -- .ufo/evidence/round-35 .ufo/evidence/round-36 tools` → **empty** (clean; no uncommitted drift).
- `sha256sum` of the working file = `d360a159a1ad320e8726eed51256146a90025ce5e5fc97840a488f3a2ad4bbe3` = blob 6's content hash.
- The two same-timestamp empty-subject commits (`2cdd89c5`, `d25e05cf`, 19:33:48) carry the identical blob `ede608ea` — jj-side working-copy/merge artifacts, zero content delta.

## 3. No later commit touched it

- `git log --all --format='%H|%cd|%s' --date=iso -- <path>` ordered by **committer** date (rebase check): newest = `5829676` at 2026-10-23 **19:33:49 -0300**; committer ≈ author dates throughout, no post-dated/rebased commits.
- Per-ref last-toucher scan: `git for-each-ref --format='%(refname)'` → `git log -1 <ref> -- <path>` over **all 800+ refs** (master, origin/\* incl. cursor/\* and devin/\* branches, all `refs/jj/keep/*`, both extra worktrees' branches `hyaku/s3-ready66-tameshi` @ `09a3a30` and `hyaku/s3-tameshi-r25-author` @ `1f73157`). Result: every ref's last toucher is one of the eight round-35 commits above (all 2026-10-23); **zero refs contain any commit dated 2026-10-24+ touching the path** (grep for `2026-10-2[4-9]` over the full scan output: no matches).
- Consequence: the round-36 L1 commits — `e423c41b` (content, 02:50:40), `d9c496b` (receipts, HEAD), `3cbd7646`/`ef37d726` — carry blob `ede608ea` forward **unchanged**.

## 4. v1 → v2 delta: every hunk classified

`diff -u round-35/c1/c1-measure.py round-36/c1/c1-measure-v2.py` → 1 file, **37 insertions(+), 13 deletions(−), 6 hunks** (line counts below fully reconcile with that stat — no hidden lines):

| hunk | old→new | −/+ | classification |
|---|---|---|---|
| 1 | `@@ -1,9 +1,21 @@` | −5/+17 | **docstring**: v2 title, freeze record (contract.json), v1-vacuous-accept narrative, `C1_R36V2_PASS` name. Shebang is context (unchanged). |
| 2 | `@@ -30,7 +42,7 @@` | −1/+1 | **docstring** (usage text): counting-command example path → `.ufo/evidence/round-36/c1/c1-measure-v2.py` |
| 3 | `@@ -51,6 +63,11 @@` | +5 | **constants**: `PUB_KILL_SLOTS_TARGET = 6`, `PUB_ACCEPT_SLOTS_TARGET = 3`, `PUB_DISTINCT_TARGET = 9` + 2 comment lines — values match contract `frozen_targets` exactly |
| 4 | `@@ -412,16 +429,16 @@` | −3/+3 | **predicate-identifier rename (labels only)**: three SETUP error prints `C1_R35:` → `C1_R36V2:` |
| 5 | `@@ -429,13 +446,13 @@` | −3/+3 | **predicate-identifier rename**: before-mode print `C1_R35_PASS=false` → `C1_R36V2_PASS=false`; `label = 'C1_R35'` → `'C1_R36V2'`; `'C1_R35_CONTROL'` → `'C1_R36V2_CONTROL'` |
| 6 | `@@ -513,8 +530,15 @@` | −1/+8 | **predicate**: v1's `and pub_kill == pub_kill_slots and pub_accept == pub_accept_slots` replaced by `pub_kill_slots == 6 and pub_accept_slots == 3 and pub_kill == 6 and pub_accept == 3 and pub_distinct == 9` (via the constants) + 5 comment lines |

**Hunks outside the documented delta: none.** No hunk touches `CONFIGS`, panel/manifest/sealed handling, the `ho_*` oracle counts, argument parsing, or exit codes. The embedded pins are context lines identical in both files — `PIN_RUNNER = 'a7d3f2dd…'` and `TOOL_SHA256 = '6188db16…'` — and both match the on-disk frozen artifacts I hashed (`mutate-and-run.sh` → `a7d3f2dd…` ✓, `tally-audit-v3.py` → `6188db16…` ✓, both equal the dispatch pins).

**Strict-reading note (transparency):** hunks 4–5 are string labels, not logic — technically outside the literal triad "docstring, constants, predicate". They are, however, the mechanical consequence of the predicate's own rename: the contract specifies the deciding line as `C1_R36V2_PASS=true`, so every print/label carrying the old name must change for the counter's output to match the contract. Semantically identical modulo the identifier.

**Predicate semantics:** v2 *removes* v1's two self-consistency clauses but asserts strictly stronger frozen-target clauses that jointly imply them (if `pub_kill == 6` and `pub_kill_slots == 6` then `pub_kill == pub_kill_slots`). No weakening; closes the documented vacuous-accept (`0 == 0`) hole. `pub_distinct` is consumed but not computed anew — the quantity already existed in v1 (the diff contains no computation changes).

## 5. v2 committed identity (bonus pin check)

v2 was introduced by round-36 content commit `e423c41ba253357ab8c8513f0376dad9d38ab248` ("round-36: content — … frozen v2 counter + contract, wave specs w1/w2", 2026-10-24 02:50:40 -0300) and carried unchanged by `3cbd7646`/`ef37d726`. Working copy `git hash-object` = HEAD blob = `5f1c2047ce533182a8938cb2b44d73938a54c153`; `sha256sum` = `9eb8944c…` = contract `counter_sha256` ✓. Clean.

## 6. Exact commands run

All read-only git plumbing (no mutation; no jj command executed at all — jj auto-snapshot avoidance; `GIT_OPTIONAL_LOCKS=0` used for `status`):

```
git -C <repo> rev-parse --show-toplevel; git worktree list; git remote -v; git log -1 --format='%H %ad %s' --date=iso
sha256sum tools/tally-audit-v3.py tools/mutate-and-run.sh .ufo/evidence/round-35/c1/c1-measure.py .ufo/evidence/round-36/c1/c1-measure-v2.py
git log --all --format='%H|%ad|%s' --date=iso --follow -- .ufo/evidence/round-35/c1/c1-measure.py
git rev-list --all --objects -- .ufo/evidence/round-35/c1/c1-measure.py
for c in $(git log --all --format=%H -- <path>); do git rev-parse "$c:<path>"; done          # commit→blob map
git hash-object <v1>; git rev-parse HEAD:<v1>; git cat-file blob HEAD:<v1> | cmp - <v1>
GIT_OPTIONAL_LOCKS=0 git status --porcelain -- .ufo/evidence/round-35 .ufo/evidence/round-36 tools
for b in <6 blobs>; do git cat-file -p $b | sha256sum; done                                  # per-blob content
git log --all --format='%H|%cd|%s' --date=iso -- <path>                                      # committer-date order
git for-each-ref | while read r; do git log -1 --format='%h %ad %s' "$r" -- <path>; done     # per-ref last toucher
diff -u .ufo/evidence/round-35/c1/c1-measure.py .ufo/evidence/round-36/c1/c1-measure-v2.py   # 6 hunks, classified above
git log --all -- .ufo/evidence/round-36/c1/c1-measure-v2.py; git hash-object <v2>; git rev-parse HEAD:<v2>
for pairs of consecutive blobs: diff <(git cat-file -p $prev) <(git cat-file -p $b)          # re-pin deltas
```

Tools installed: none (git/diff/sha256sum sufficed). No pacman. Scratch: none needed outside session artifacts.

## 7. Confidence & residual surface

- **High confidence** on both sub-claims: every statement above is object-level (blob hashes, `cmp`, per-ref commit walks), not name/comment inference.
- Residual (out of scope, unattacked): packed-but-unreachable objects (dangling blobs can't make a committed file "unfrozen"); `.ufo/state/` and other lanes untouched per lane bounds.
