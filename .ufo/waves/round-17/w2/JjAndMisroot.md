# JjAndMisroot — lane sync, lane tree, fleet-root misroot sweep (read-only)

Seat: `TameshiR17.JjAndMisroot-2` (leaf, no dispatch). All probes read-only; nothing moved, deleted, committed, or installed.

## 1. Lane sync — `jj-lane.sh state`

Command: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/tameshi-shokunin`
Exit 0. Output at 13:03 and again at 13:04:35 (identical except the live untracked count):

```
state branch=master local=eb7838b16490ca7ba17ea3242ade76a61f744af2 remote=eb7838b16490ca7ba17ea3242ade76a61f744af2 ahead=0 behind=0 head=detached tracked=0 untracked=8
...
state branch=master local=eb7838b16490ca7ba17ea3242ade76a61f744af2 remote=eb7838b16490ca7ba17ea3242ade76a61f744af2 ahead=0 behind=0 head=detached tracked=0 untracked=14
```

Cross-checks (all exit 0 unless noted):

- `git -C <lane> rev-parse HEAD master` → `eb7838b16490ca7ba17ea3242ade76a61f744af2` twice. **HEAD == master == landing rev.**
- `git -C <lane> ls-remote origin refs/heads/master` → `eb7838b16490ca7ba17ea3242ade76a61f744af2	refs/heads/master`. The remote tip is the landing rev, not just a stale tracking ref; `refs/remotes/origin/master` also resolves to it.
- `git -C <lane> symbolic-ref -q HEAD` → exit **1** (detached, as `state` says).
- `jj --ignore-working-copy -R <lane> log -r '@|@-' --no-graph -T 'commit_id.short() ++ " " ++ bookmarks ++ "\n"'` →
  ```
  8703773b9143
  eb7838b16490 master
  ```
  `@` is an empty working-copy commit with no bookmark; the master bookmark sits on `@-`, which is exactly the commit git HEAD is detached at. So `head=detached` is the normal jj-colocation projection (git HEAD parked on `@`'s parent), **not** a lane sitting off-branch. `ahead=0 behind=0` confirms the push landed.

Verdict on axis 1: **holds** — branch master, local == remote == HEAD == eb7838b16490ca7ba17ea3242ade76a61f744af2, 0/0.

## 2. Lane tree — `git status --porcelain`

`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --porcelain` exit 0. First probe, 8 lines, all untracked:

```
?? .ufo/evidence/round-17/c2-after-eb7838b.json
?? .ufo/evidence/round-17/c2-after-eb7838b.txt
?? .ufo/evidence/round-17/registry-full-eb7838b.json
?? .ufo/evidence/round-17/registry-full-eb7838b.txt
?? .ufo/waves/round-17/dispatch2.json
?? .ufo/waves/round-17/spawn2.json
?? .ufo/waves/round-17/spec2.json
?? .ufo/waves/round-17/w2/
```

`-uall` expanded the same snapshot to 16 files. At close (13:04:35) the default listing had grown to 14 entries; `-uall` showed roughly 50 files (`c1-measure-98bea7d.json`, `c1-measure-eb7838b.json`, `coldread/traces/CR02…CR56/…`, `w2/swarm-registry.json`, …). Every entry was `??`; `awk '{print $1}' | sort | uniq -c` → `14 ??` and **zero** tracked modifications.

All of it lives under `.ufo/evidence/round-17/` or `.ufo/waves/round-17/`, i.e. driver runtime that the lane tool refuses to commit by construction: `scripts/hyaku/jj-lane.sh:532-534` rejects `.ufo`, `.ufo/state*`, and `.ufo/watchdog.log` paths with "driver runtime is never committed by a lane". The count drift is live seat writing during the wave, not lane drift.

Verdict on axis 2: **holds** — clean tracked tree; untracked content is round-17 evidence/wave runtime in the directory the runner forbids committing.

## 3. Misroot sweep — fleet root untracked files naming tameshi round 17

`git -C /home/vgpnk/Projects/shokunin status --porcelain` exit 0 at 13:03 (11 lines) and 13:04:26 (12 lines, snapshot sha256 `14f766ef3dd6f4cf9e28f2448402a9aa89b9bee418414092ff971994e2ed795b`):

```
 M .ufo/watchdog.log
 M scripts/hyaku/inline.sh
 M scripts/hyaku/jj-lane-selftest.sh
 M scripts/hyaku/jj-lane.sh
?? .ufo/state/kaidoku.report-baseline
?? .ufo/state/kake.report-baseline
?? .ufo/state/kama.report-baseline
?? .ufo/state/mado.report-baseline
?? .ufo/state/mori.report-baseline
?? .ufo/state/souji.report-baseline
?? .ufo/state/tabi.report-baseline
?? .ufo/state/tameshi.report-baseline
?? .ufo/state/tsukuroi.report-baseline
```

(`M scripts/hyaku/inline.sh` — 8 insertions/5 deletions — appeared only in the 13:04 snapshot; the fleet-root scripts tree is being edited by other work while this sweep runs.)

Content check over every currently untracked non-ignored fleet-root file:

```
while IFS= read -r p; do [ -f "$p" ] && grep -l 'tameshi' "$p"; done < <(git status --porcelain -uall | awk '$1=="??"{print $2}')
→ no output, exit 1
```

Exactly one untracked fleet-root file names tameshi round 17 at the path level; listed per instruction, **not** moved or deleted:

| path | first line |
|---|---|
| `.ufo/state/tameshi.report-baseline` | `17 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Classification: canonical driver state, not a seat stray. `scripts/shokunin-watchdog.sh:31` documents `.ufo/state/<lane>.report-baseline` as `"round SHA256"`; `record_report_baseline` (`:120-138`) writes it atomically, and its only launch-path call (`:203`, inside `launch_lane`, before spawning) refuses to spawn when the baseline cannot be written. The file's mtime `2026-10-20 12:07:32.084 -0300` matches the watchdog launch record `2026-10-20T12:07:33-03:00 launch tameshi round=17 …` (`.ufo/watchdog.log:485`). `e3b0c442…` is the SHA-256 of the empty string, so the line means "tameshi round 17 launched, report not yet written" — the expected launch-time value, consistent with `report_of`'s same-round digest suppression (`:155-160`). The other eight baselines are the same format for their own lanes and none names tameshi.

Ignored untracked entries at fleet root (197): name filter `tameshi|round-?17` hits only `tameshi-shokunin/` — the lane repo itself, ignored by `.gitignore:1` (`*-shokunin/`), so lane files can never leak into fleet-root tracking. The rest are `.tower` runtime (139) and old `shokunin-train-2026…` scratch (36). Ignored content was not content-scanned (157 MB of tower runtime); the stated sweep is over non-ignored untracked files plus name filtering of ignored ones.

Two out-of-scope strays observed, left untouched:

1. `.ufo/waves/round-18/w2/reports/ReopenS089.md` — untracked at 13:03, **gone by 13:04**; first line `# S089 — non-author re-open (round 18, wave 2 / FALSIFY)`; `grep -inE 'tameshi|round[ -]?17|R17'` → no match (exit 1). A sibling lane writing at the fleet root; it never named tameshi round 17. Confirms the fleet root must be swept against a timestamped snapshot.
2. `bash: /home/vgpnk/Projects/shokunin/souji-shokunin/tests/tools/souji-verify.sh: No such file or directory` — a literal directory tree (dated Oct 18, 10139-byte JSON file) created by a bad redirect, content `{"seat":"S54",… "lane":"souji-shokunin","round":4 …}`; `grep -rlE 'tameshi|round[ -]?17'` → exit 1. Pre-existing, ignored, unrelated to this round.

Verdict on axis 3: **holds** — zero untracked fleet-root files whose *content* names tameshi round 17; the single path-level hit is launch-time watchdog state at its canonical location.

## Verdict

Holds: the lane is exactly at eb7838b16490ca7ba17ea3242ade76a61f744af2 on local master, remote master and HEAD (detached only in the normal jj-colocation sense, with `@` empty on top of the bookmarked commit), its tracked tree is clean with only uncommittable `.ufo/` runtime untracked, and the fleet-root misroot sweep found no tameshi round-17 strays — only the canonical `tameshi.report-baseline` launch record.
