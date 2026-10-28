# T55W2SentStrayWrites — fleet-root misroot / stray-write sweep

Seat `T55W2SentStrayWrites`, tameshi round 55, wave 2 (falsify wave), item: *sweep the fleet root for
round-55 misroots and `/tmp` for `tameshi-r55` scratch; report each candidate with its first line and
say whether it must be moved into the lane (byte-exact `cmp`) or left alone.*

- Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`; content commit C0 `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`.
- Read-only on the fleet root, on sibling lanes and on `/tmp`. **Nothing was moved, deleted or edited outside
  `.ufo/waves/round-55/w2/`.**
- Fixtures/reproduction ran only inside `S=/fast/scratch/hyaku/tameshi-r55/T55W2SentStrayWrites`, removed by
  `trap 'rm -rf -- "$S"' EXIT`.
- No tool installs or upgrades were needed (nothing older than the shipped `git`/`find`/`grep`/`md5sum`/`python3`).

Driver, reruns every receipt below verbatim:
`.ufo/waves/round-55/w2/T55W2SentStrayWrites-receipts/sweep.sh`
Receipts: `01-fleet-root-porcelain.txt`, `02-untracked-content-markers.txt`, `03-misroot-dir-scan.txt`,
`04-tmp-sweep.txt`, `05-byte-equality-verdict.txt`, `06-mechanism-reproduction.txt`,
`07-sibling-lanes-and-home.txt`, `08-census.txt`, `09-closure-r54-clone.txt`.

> `02-untracked-content-markers.txt` truncates the `.scratch/closure-r54` hit list at 10 (`head -10`) — it is a
> 28415-file clone of the lane, so listing its hits is meaningless; the question that matters (does it hold a
> round-55 deliverable?) is answered without truncation in `09-closure-r54-clone.txt`: **0** `T55W*` files, no
> `.ufo/waves/round-55`.

## Verdict in one line

**No file anywhere outside the lane names tameshi round 55, so nothing must be moved in.** The sweep did find
one real misroot — a **git-invisible, zero-file directory tree `/home/vgpnk/Projects/shokunin/D=/…`** left at the
fleet root by a *round-54* seat's documented command re-run without variable expansion. It holds no bytes, so it
is not a move candidate; it is debris the L1 may remove (or leave) — I did not touch it.

## What I attacked

Three write surfaces a round-55 seat can hit by accident, each checked by content, not by name:

1. the fleet root's untracked set, `git -C /home/vgpnk/Projects/shokunin status --porcelain` (no pathspec);
2. the untracked set's blind spot — directories git cannot see (empty dirs), and any `NAME=`-shaped
   path-leak directory;
3. `/tmp` (all depths ≤ 4, plus "created today" filtering), the sibling-lane repos at the fleet root, and `$HOME`
   at depth 2.

## F1 — Misroot at the fleet root: `D=/fast/scratch/hyaku/tameshi-r54/T54W2Sent02/pinned.7U6Avg/w-base2` (Low)

Evidence (`03-misroot-dir-scan.txt`, `06-mechanism-reproduction.txt`):

```
$ find /home/vgpnk/Projects/shokunin -maxdepth 2 -type d -name '*=*'
/home/vgpnk/Projects/shokunin/D=
$ find '/home/vgpnk/Projects/shokunin/D='
D=  D=/fast  D=/fast/scratch  D=/fast/scratch/hyaku  D=/fast/scratch/hyaku/tameshi-r54
D=/fast/scratch/hyaku/tameshi-r54/T54W2Sent02  …/T54W2Sent02/pinned.7U6Avg  …/pinned.7U6Avg/w-base2
dirs=8 files=0
top: mode=drwxr-xr-x size=8 mtime=2026-10-28 12:07:44.082520575 -0300   # all 8 dirs created in one call (12:07:44.08/.083)
```

Why the assigned sweep would have missed it: `git status --porcelain` and `git ls-files -o` report **0** entries —
git has no record for empty directories, and `git check-ignore -v D=` exits 1 (no ignore rule). A porcelain-only
sweep is structurally blind to this class; the `find -name '*=*'` leg is what caught it.

Mechanism, reproduced (cwd = a scratch dir, never the fleet root):

```
$ mkdir -p "D=/fast/scratch/hyaku/tameshi-r54/T54W2Sent02/pinned.7U6Avg/w-base2"
dirs=8 files=0 leaf=D=/fast/scratch/hyaku/tameshi-r54/T54W2Sent02/pinned.7U6Avg/w-base2
```

That is the leftover's shape exactly (8 dirs, 0 files, same leaf). The plain `mktemp -d "D=…"` form does *not*
reproduce it (`mktemp` never builds parents) — so the producer ran `mkdir -p` on a string whose `$NAME=` prefix
survived into the path, with process cwd = the fleet root. Attribution is pinned by the *round-54* report, which
documents both halves of the literal path:

- `.ufo/waves/round-54/w2/T54W2Sent02.md:41` — `Built only inside `D=$(mktemp -d /fast/scratch/hyaku/tameshi-r54/T54W2Sent02/pinned.XXXXXX)`:`
- `.ufo/waves/round-54/w2/T54W2Sent02.md:63` — `… --lane "$D/clone" --rev e26cd9304a6a94decbbdbd881aeaafb64d6074eb --work "$D/w-base2" --explain`

i.e. `pinned.7U6Avg` is that seat's pinned scratch dir and `w-base2` is its `--work` dir; re-running the documented
line with `D=$D`/`$D` left unexpanded yields the literal argument `D=/fast/…/pinned.7U6Avg/w-base2`.

Verdict: **leave alone / L1's call to remove.** Zero files → nothing to recover, nothing to `cmp`-move, no evidence
lost. Note it dates from *round 54* (12:07 today, i.e. after the r54 C0 11:23 and before this wave), so it is not one
of this wave's writes; the r55 analogue of the command is far weaker — the r55 reports use bare `S=/fast/…`
assignments (valid shell lines), and `find` over the lane at depth 2 shows **0** `D=`/`S=` directories.

Impact if left: a future `git add -A`/tarball at the fleet root could commit 8 empty dirs named after a foreign
lane's scratch path (git would then track a fabricated path component `D=`); a future `rm -rf /fast/scratch/...`
sweep is unaffected. Smallest remediation: `rmdir -p`/`rm -rf` the empty tree (I did not).

## F2 — Fleet-root untracked set: 8 entries, **0** tameshi-round-55 candidates (`01`,`02`)

`git -C /home/vgpnk/Projects/shokunin status --porcelain` → `entries=8`, byte-identical to the listing taken at
the start of this seat (post-sweep porcelain md5 `0bbfb3d780375cc8ebbbeca84b29f92f`, `01-fleet-root-porcelain.txt`). Marker counts from `02-untracked-content-markers.txt`
(`tameshi` / `round-55|round 55|\br55\b` / `T55W[123]` / C0 sha):

| entry | first line (cut) | tameshi | r55 | T55W | C0 sha | verdict |
|---|---|---|---|---|---|---|
| `o.bin` | `<!DOCTYPE html><html lang="en-US"><head><title>Just a moment...` (Cloudflare interstitial, 5867 B, mtime 10-27 16:58) | 0 | 0 | 0 | 0 | leave — fetch artifact, no lane content |
| `oldrep1.out` | `PASS healthy: all planes pass (exit 0, HEALTHY)` (15314 B, 10-28 09:10) | 0 | 0 | 0 | 0 | leave — tsukuroi health-sample output |
| `oldrep2.out` | same first line, 15314 B, 10-28 09:11, md5 `2d22c691…619d` | 0 | 0 | 0 | 0 | leave — byte-identical twin of `oldrep1.out` |
| `.scratch/closure-mado-r50.json` | `{"round": 50, …, "lane": "mado", "verdict": "rejected-honest-stop"` | 0 | 0 (r50) | 0 | 0 | leave — `.scratch/` is out of scope by bounds |
| `.scratch/source-routing-queue.md` | `# Source-routing queue — operator directives 2026-10-27 (hyaku run 10)` | 0 | 0 | 0 | 0 | leave — `.scratch/`, run 10 |
| `.ufo/reports/round-49/tsukuroi.md` | `# tsukuroi — round 49 (hyaku run 11, attempt 1)` | 0 | 0 | 0 | 0 | leave — another lane's round-49 report |
| `.scratch/closure-r54/` (dir) | a `lane/` clone at r54 close `0263c71` (12:25:51 today); 45848 files | 28415 (clone's own lane files) | 16 files mention `round-55` as a forward reference; **0** `T55W*` artifacts; no `.ufo/waves/round-55` (`09-closure-r54-clone.txt`) | 0 | 0 | leave — `.scratch/`, a clone of the r54 close, holds no round-55 deliverable |
| `.scratch/goal-20261028-hyaku-run11.md` (**M**, tracked) | run-11 goal note | — | — | — | — | leave — tracked, not a stray write |

No entry names round 55 or tameshi; therefore **no fleet-root file is a move candidate** and nothing needs a
byte-exact `cmp` against the lane.

## F3 — `/tmp`: no `tameshi-r55` scratch; every r55-named file is a duplicate or reproducible (`04`,`05`)

```
$ ls -d /tmp/tameshi-r55*        →  no such file or directory
$ find /tmp -maxdepth 4 -name '*tameshi*' -o -name '*r55*' -o -name '*round-55*' -o -name '*T55W*'
   → no T55W*/T55W2* anywhere; no /tmp/tameshi-r55*
$ find /tmp -maxdepth 1 -newermt '2026-10-28 00:00' -name '*{tameshi,r55,round-55}*'
   → census-r55.txt, census-r55-rev01.txt, census-r55-mut.txt
```

`/tmp` today holds 547 top-level files; the ones whose content names tameshi/round-55 resolve as follows
(`05-byte-equality-verdict.txt`):

| /tmp file | first line (cut) | lane relation (proved) | verdict |
|---|---|---|---|
| `census-r55.txt`, `census-r55-rev01.txt`, `census-r55-mut.txt`, `census-val.out`, `census-now.txt` | `tameshi\tW04\tS047 duplicate url pitest.org/…` | `cmp` **IDENTICAL** to `.ufo/waves/round-55/w1/T55W1ExecCensus-receipts/base-validate.tsv` (md5 `242459bd…2067`; 32 files under `.ufo/` carry that same byte string) | leave — redundant copy of a landed receipt |
| `fl.json` (3022874 B) | `{"calibration_restraint_score": 8, "coldread": {…` rev_input `0a2010ac…` | `cmp` **IDENTICAL** to `T55W1ExecNoHarm-receipts/coldread-at-base.json` **and** `T55W1ExecRekeyPrep-receipts/floor.json` (md5 `1cbeb467…59`) | leave — same bytes already in the lane |
| `t55stat.txt` (78373 B) | ` .../round-55/assimilation/S280-gnu-errors.txt      \|   11 +` | `cmp` **IDENTICAL** to `git diff --stat 0a2010ac…..9cf0146…` (regenerated, 1286 lines both sides) | leave — reproducible diffstat |
| `skill_c0_923625.md` (198186 B) | `---\nname: tameshi-shokunin` | sha256 `e0e0b4d0…ff9` = **blob `95ae52bb`** = `SKILL.md` at r54 C0 `59c38109bf11`; ≠ C0 `e0ce89f7…` (199384 B), ≠ base `b5ff9727…` | leave — stale r54 SKILL snapshot, `git show 59c3810:SKILL.md` reproduces it |
| `c0.json` (3038961 B) | `{"calibration_restraint_score": 6, "coldread": {…` rev_input `9cf0146…` | **no** lane twin (`find -size 3038961c` → only `T55W1CritClaimShape-receipts/coldread-HEAD.json`, md5 `8cebe208…` ≠ `2274dbe4…`; that one differs only in `rev_input`/`revision`, is at HEAD); no round-55 document references `c0.json` | leave — unreferenced transient coldread capture at C0; re-runnable into a seat's receipts if ever cited (the lane already holds the HEAD-rev twin) |
| `l54.md`, `sc60.md`, `specdump.txt`, `sentscope_frozen.txt`, `t55stat.txt` | round-54 report copy / mori SCORECARD copy / spec dump / frozen-path list | no lane twin, all regenerable from lane/either-lane sources | leave — scratch dumps, no lane evidence role |

`tameshi-r55` scratch in the sanctioned place is intact: `/fast/scratch/hyaku/tameshi-r55/` holds 64 seat dirs
(wave-1 and wave-2 seats' own trees); nothing there is a deliverable and nothing there names a lane receipt path.
Left unchecked as out-of-scope-by-bounds but noted: `tameshi-r55-final` and loose `base-*.py`/`fid*.json` files in
`/fast/scratch/hyaku/` — scratch root, not the fleet root, not mine to move.

Bounds observation (not a misroot, no move): five leftover lane/sibling clones sit in `/tmp` and exceed the
"`/tmp` only for files under 50 MB" guidance — `k57` 421 M, `k57b` 411 M, `r57a8d` 305 M, `s05dbg` 197 M (all
mtime 10-27, contain `corpus/lessons/round-55*.md` from an earlier round's clone), and
`tameshi-registry-check-u9ffi_ub` 107 M (**mtime 2026-10-28 14:01**, i.e. created inside this wave's window,
holding `fleet/tameshi-shokunin`). Each is a throwaway clone, not a deliverable: leave alone; the 107 M one is the
only piece of this wave's `/tmp` footprint worth the L1 knowing about. Empty leftovers
`/tmp/r55-lab-mutant.{4b2i0t4h,pct1l9eq,p4ba44si,lj31nhey}` (0 bytes, today) and
`/tmp/tameshi-r4-2-regression.Fa6S8t` (0 bytes) hold no files at all.

## F4 — Sibling lanes and `$HOME`: clean (`07`)

```
top-level dirs=26 git-repos=21  lanes-with-tameshi-r55-strays=0
$ find /home/vgpnk -maxdepth 2 -newermt today \( -name '*T55W*' -o -name '*r55*' -o -name '*tameshi*' \)   → (empty)
```

All 21 git repos under the fleet root (other than the lane) report no `tameshi|T55W|r55|round-55` porcelain
entry; the tameshi lane itself is clean of `D=`/`S=` misroot dirs at depth 2.

## F5 — Census (`08-census.txt`)

```
$ scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
… tameshi  W04  S274 duplicate url bazel.build/basics/hermeticity across scopes
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
exit=0
```

`exit=0` as required (the 17 output lines are the duplicate-url warnings plus the terminal `ok` row; the census
row count is unchanged by this sweep — I wrote nothing under `corpus/`).

## Artifacts opened

Fleet root: `git status --porcelain` (8 entries), `o.bin`, `oldrep1.out`, `oldrep2.out`,
`.scratch/closure-mado-r50.json`, `.scratch/source-routing-queue.md`, `.scratch/closure-r54/` (tree),
`.ufo/reports/round-49/tsukuroi.md`, `D=/…` (full tree, 8 dirs).
Lane: `SKILL.md` (worktree + `git show` at C0, base, and `59c3810`), `.ufo/waves/round-55/` (wave dirs, `spec-w2.json`),
`.ufo/waves/round-55/w1/T55W1ExecCensus-receipts/*`, `T55W1ExecNoHarm-receipts/coldread-at-base.json`,
`T55W1ExecRekeyPrep-receipts/floor.json`, `T55W1CritClaimShape-receipts/coldread-HEAD.json`,
`.ufo/waves/round-55/w2/*` (listing), `T55W2ScoutColdread-receipts/*` (listing),
`.ufo/waves/round-54/w2/T54W2Sent02.md`, `T54W2Sent02-receipts/` (listing),
`.ufo/evidence/round-55/` (listing), `corpus/SOURCES.md` (via the census validator).
`/tmp`: `census-r55*.txt`, `census-val.out`, `census-now.txt`, `fl.json`, `c0.json`, `t55stat.txt`,
`specdump.txt`, `skill_c0_923625.md`, `sentscope_frozen.txt`, `l54.md`, `sc60.md`, `ct.txt`, the `r55-lab-mutant.*`
and clone leftovers (names/sizes/mtimes only).

## What a reader should be able to falsify here

- `git -C /home/vgpnk/Projects/shokunin status --porcelain | wc -l` = 8 and none of the 8 grep-matches
  `tameshi|round-55|T55W[123]|9cf0146…` — if any does, my "nothing to move" line is wrong.
- `find /home/vgpnk/Projects/shokunin -maxdepth 2 -type d -name '*=*'` = exactly `/…/D=` — if more exist, the
  sweep under-counted.
- `ls -d /tmp/tameshi-r55*` fails — if it succeeds in your shell, that dir was created after 14:41.
