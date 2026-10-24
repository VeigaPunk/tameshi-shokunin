# RevengerSealedSet — sealed-set usage in the v2 deciding run (round-36 w1)

Attacked: how the C2 v2 deciding run (`C1_R36V2`, receipt `.ufo/evidence/round-36/after/c1v2-at-b455001e.{exit,stderr,stdout}`) uses `--sealed`. Three assertions from the dispatch:

1. the `--sealed` directory at run time is the committed `.ufo/evidence/round-35/c1/sealed` (7 files, 4 kill + 3 accept);
2. each sealed file's last-modifying commit descends from the round-35 freeze `d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc`;
3. the v2 receipt's `ho_distinct` (7) matches an independent distinct-body count.

Everything below is read-only over committed bytes at the deciding rev `b455001e2589b3f4f471d94a3de7e5e549b9f54c` and at HEAD `d9c496b19371b779ce0eec6dfee1b049b27a3a2d`. No counters, tools, or receipts were edited; no mutating git/jj command was run; no tools installed (system `git` + `python3` only; `pacman` untouched). Scratch: `/fast/scratch/hyaku/tameshi-r36-seats/RevengerSealedSet/verify_sealed.py`.

## How the counter actually uses `--sealed` (reconstructed from `.ufo/evidence/round-36/c1/c1-measure-v2.py`, sha256 `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53` at b455001e == disk == contract `counter_sha256`)

- `--sealed` is normalized, never read directly as bytes: absolute kept, else joined to `--lane`; `srel = relpath(abspath(sdir), lane)` (:484-486).
- Sealed copies are loaded from COMMITTED bytes at REV: `git ls-tree -r --name-only REV -- <srel>`, keep `*.json` except `manifest.json`, then `git show REV:<name>` per file (`load_copies_rev`, :292-310; docstring cites round-35 seat ReviewSealedGate BOUND-4 — v1 scored the working tree while the gate read history, now both read the commit).
- The freeze is not self-declared: derived from history as the commit that first ADDED `.ufo/evidence/round-35/contract.json` at REV; `sealed_ok` requires `manifest.freeze_rev == derived`, `rev != derived`, `derived` ancestor of `rev` (:488-497).
- Per file: `last = git log REV -1 --format=%H -- <fpath>`; `origin = git log REV --follow --diff-filter=A -1 -- <fpath>`; rejects empty `last`, `last == freeze` (BOUND-3 strict descent), freeze not ancestor of `last`, `last` not ancestor of `rev`, empty `origin`, freeze not ancestor of `origin`; any failure prints `SEALED-PROVENANCE-FAIL` (:498-510). Empty set prints `SEALED-SET-EMPTY`.
- `ho_kill_total`/`ho_accept_total` come from the committed `set` fields; `ho_distinct = distinct_bodies(...)` = |{ sha256(full runner text after applying the copy's `edits`) }|, with a `sha256(filename)` fallback when an edit does not apply exactly `cnt` times (:513-521, :255-260).
- Predicate: `runner_ok and tool_sha_ok and pub 6/6+3/3+9 and ho_kill_total >= 4 and ho_accept_total >= 2 and ho_kill==ho_kill_total and ho_accept==ho_accept_total and ho_invalid==0 and sealed_ok`.

## Verification 1 — runtime `--sealed` dir is the committed set

Commands (cwd = lane; rev `b455001e…`):

```
sha256sum .ufo/evidence/round-35/c1/sealed/<f>
git show b455001e2589b3f4f471d94a3de7e5e549b9f54c:.ufo/evidence/round-35/c1/sealed/<f> | sha256sum
git show HEAD:.ufo/evidence/round-35/c1/sealed/<f> | sha256sum
git status --porcelain -- .ufo/evidence/round-35/c1/sealed/
git ls-tree -r --name-only b455001e2589b3f4f471d94a3de7e5e549b9f54c | grep -i sealed
```

Result: 8/8 files (7 specimens + `manifest.json`) byte-identical disk == b455001e == HEAD. All seven specimen sha256 equal the manifest's `copies` entries exactly (`a46a30f7…`, `a77486d9…`, `daa53fcf…`, `b9e0aaad…`, `33d15541…`, `0d46e7cf…`, `f2e1501d…`). `git status --porcelain` on the dir: empty (clean). The only other committed `sealed`-named artifacts at b455001e are `.ufo/evidence/round-30/v4/c1-sealed.json` (a single round-30 file, not a manifest directory) and wave reports — no alternate `--sealed` candidate path exists at that rev.

Depth note: because the scorer reads committed bytes (BOUND-4), the receipt is decided by the commit, not the runtime directory; the receipt numbers themselves pin the set it saw — `ho_kill=4/4 ho_accept=3/3 ho_distinct=7` — and I confirm below that exactly the committed set at `b455001e:.ufo/evidence/round-35/c1/sealed` yields 4 kill + 3 accept + 7 distinct bodies. Runtime disk equality (verified above) corroborates that the on-disk dir is that set.

## Verification 2 — per-file last-modifying commit descends from the freeze

```
git log b455001e2589b3f4f471d94a3de7e5e549b9f54c -1 --format=%H -- .ufo/evidence/round-35/c1/sealed/<f>
git merge-base --is-ancestor d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc 691bb5128e98ff0b827f5eb1e8cd8f86f8ce2757
git merge-base --is-ancestor 691bb5128e98ff0b827f5eb1e8cd8f86f8ce2757 b455001e2589b3f4f471d94a3de7e5e549b9f54c
git log b455001e2589b3f4f471d94a3de7e5e549b9f54c --diff-filter=A -1 --format=%H -- .ufo/evidence/round-35/contract.json
git ls-tree d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc -- .ufo/evidence/round-35/c1/sealed/
git show -M --name-status --format=%H 691bb5128e98ff0b827f5eb1e8cd8f86f8ce2757 -- .ufo/evidence/round-35/c1/sealed/
```

Result: for **all 7** specimens the last-modifying commit at the deciding rev is `691bb5128e98ff0b827f5eb1e8cd8f86f8ce2757` ("round-35: A4-A7 pre-data apparatus … sealed set 4 kill + 3 accept with manifest …", 2026-10-23T18:56:12-03:00). `d16f9b5a` is an ancestor of `691bb51` (rc 0), `691bb51 != d16f9b5a` (strict descent), and `691bb51` is an ancestor of both `b455001e` and HEAD `d9c496b`. The whole-dir history up to the deciding rev is exactly one creation commit: at the freeze `d16f9b5a` the sealed directory does not exist (empty ls-tree); `691bb51` adds all 8 files as pure `A` entries (155 insertions, no renames). The counter's self-derived freeze (`git log REV --diff-filter=A -1 -- .ufo/evidence/round-35/contract.json` at b455001e) is `d16f9b5a…` exactly, equal to the manifest's `freeze_rev` — so `sealed_after_freeze=1` in the receipt is exactly this gate passing.

Divergence note (D1, by design, no violation): `git log REV --follow --diff-filter=A` reports origin `d16f9b5a` for `workdir-branch-keep-swap.json` (other six: `691bb51`). That is `--follow` rename-similarity lineage to the panel copy `panel/workdir-branch-swap.json` (added at the freeze), NOT creation — plain `--diff-filter=A` attributes creation of all 8 files to `691bb51`. The gate accepts `origin == freeze` (`merge-base --is-ancestor X X` → 0); my independent run computes the same origin values, so the receipt's gate semantics and mine agree exactly. The task's assertion concerns last-modifying commits, which hold strictly for all 7.

## Verification 3 — independent `ho_distinct`

Independent script (scratch; does NOT import the counter): read each committed specimen at `b455001e`, apply its `edits` to `git show b455001e:tools/mutate-and-run.sh` (sha256 `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` == `PIN_RUNNER`), assert every edit applies exactly `cnt` times (all pass — the counter's filename-fallback path never fires), and count distinct sha256 of the full applied text (same definition as `distinct_bodies`).

Result:

```
independent ho_distinct = 7   (one digest per specimen, zero collisions)
sealed slots: kill=4 accept=3 total=7
  kill   cfg00-setup-as-pass / cfg11-workdir-wording / workdir-branch-keep-swap / workdir-keep-cleanup-nested-config
  accept accept-trailing-comments / comment-head-comment-quoted-legnames / inert-heredoc-apostrophe-comment
```

Matches the receipt `ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7`. Surplus depth: the same independent method over the public panel gives `pub_distinct = 9` (matches receipt), and the public∩sealed body-digest overlap is **0** — the sealed set is also novel relative to the panel at the applied-body level, which the v2 predicate does not require (recorded as surplus strength, not a frozen requirement).

Receipt integrity cross-checks: `.exit` contains `EXIT=0`; `.stderr` is 0 bytes; `.stdout` is 2079 bytes, disk sha256 `5e2b4e15c0a24face50273f3200da7ce7747f96908410ce61eaec22f85393efb` == HEAD blob; predicate line ends `rev=b455001e2589b3f4f471d94a3de7e5e549b9f54c C1_R36V2_PASS=true`. The round-35 deciding receipt (`.ufo/evidence/round-35/after/c1-at-34fa5b0c….stdout`) shows the identical sealed numbers (`ho_kill=4/4 ho_accept=3/3 ho_distinct=7 sealed_after_freeze=1`) at its own rev — consistent with a frozen set reused across rounds.

## Divergences / observations

- D1: `--follow` origin equality-to-freeze is accepted by the gate (above); actual creation of every sealed file is post-freeze (`691bb51`). Provenance clarity only.
- D2: the receipt line does not print `srel`, so the receipt alone does not identify *which* `--sealed` argument was passed. What it does prove: the passed path resolved at `b455001e` to a committed directory containing exactly 4 kill + 3 accept copies with 7 distinct bodies and clean lineage. The contract's `counting_command` pins the canonical path `.ufo/evidence/round-35/c1/sealed`, and no other committed candidate directory exists at that rev (checked).
- D3: runtime tampering of the on-disk sealed directory cannot affect the deciding receipt (committed-bytes reads, BOUND-4); disk == HEAD verified regardless.

## Verdict

All three assertions hold: (1) runtime `--sealed` directory is byte-identical to the committed `.ufo/evidence/round-35/c1/sealed` — 7 specimen files + manifest, 4 kill + 3 accept, clean working tree, no alternate committed candidate; (2) every sealed file's last-modifying commit at the deciding rev is `691bb5128e98ff0b827f5eb1e8cd8f86f8ce2757`, a strict descendant of freeze `d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc` and an ancestor of `b455001e`; (3) independent distinct-body count = 7 == receipt `ho_distinct=7` (and `pub_distinct=9`, sealed∩public overlap 0).

VERDICT: CONFIRMED — no defect found in the v2 deciding run's sealed-set usage.
