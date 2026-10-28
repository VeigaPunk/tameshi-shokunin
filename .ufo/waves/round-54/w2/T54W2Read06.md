# T54W2Read06 — cold read of `### The tick and the pin read` at C1

- **Heading:** `### The tick and the pin read`
- **Candidate:** `99c3bc88d704566197783f66b211ee0a830e0330` (C1)
- **Span:** start 1034, end 1082 (exclusive; section text = SKILL.md lines 1034–1081, trailing blank line 1082 stripped by the round-18 `sectionize`)
- **`section_sha256`:** `ca86e98de294306fca4f2cbc060555b05eb036967ad333d907b761e09fb70805`
- **Reader mode:** cold read as an executor with no wave-1 context; read-only on the lane; no lane file edited.

Byte identity note (context, not a finding): the section bytes are **identical at C0 `59c38109bf11` and C1** (`sha256 dc5152…` under my own extraction, `ca86e98d…` under `sectionize`; a Python byte compare of both revisions' section text printed `identical`). The C1 fix pass did not touch this section.

## Artifacts opened

| Artifact (absolute path) | Revision / lines | Purpose |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md` | `99c3bc88d704566197783f66b211ee0a830e0330`, lines 1010–1082 | the section and its immediate predecessor context |
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/reader-section.py` | C1 worktree | confirms the span/sha are taken from git objects via the round-18 `sectionize` |
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py` | `99c3bc88…:.ufo/evidence/round-18/measure.py`, `def sectionize` (lines 209–239) | exact section-boundary and sha rule (trailing whitespace-only lines stripped, no trailing newline) |
| `/home/vgpnk/Projects/shokunin/scripts/shokunin-watchdog.sh` | fleet `17c1fad`, lines 1–20 | anchor "round 8: `scripts/shokunin-watchdog.sh:3-5` at fleet `17c1fad`" and "`:14`" |
| `/home/vgpnk/Projects/shokunin/shokunin.conf` | fleet `5efb4114`, lines 1–20 and 55 | anchor "since `5efb4114` (2026-10-19) the lanes live in `shokunin.conf`, which names tameshi" |
| `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh` | C1 worktree, lines 92–183, 839 | anchor "`<branch>` = the `branch=` field of `… jj-lane.sh state <repo>` (git config `lane.branch` first, else function `detect_branch()`)" |
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/fleet-kill-rate-ledger.md` | `99c3bc88…`, lines 276–282, 320, 333, 360, 410–423 | anchor "the branch-tip rule in force is ER-jj, `fleet-kill-rate-ledger.md:420`"; corroboration of the tool pin and of the 4/2/0 headline |
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh` | C1 worktree (sha256 `977de470…`) | anchor "`sha256sum tools/mutate-and-run.sh`" and the round-52 `MUTATE_SELFTEST` claim |
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-52/w2/T52W2Fix06.selftest.out` | round-52 receipt | the round-52 selftest claim's recorded receipt |

## Commands run

```console
$ mkdir -p /fast/scratch/hyaku/tameshi-r54/T54W2Read06 && export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read06
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
$ python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin 99c3bc88d704566197783f66b211ee0a830e0330 "### The tick and the pin read"
{"heading": "### The tick and the pin read", "cand": "99c3bc88d704566197783f66b211ee0a830e0330", "start": 1034, "end": 1082, "section_sha256": "ca86e98de294306fca4f2cbc060555b05eb036967ad333d907b761e09fb70805"}
$ python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin 59c38109bf11 "### The tick and the pin read"
{"heading": "### The tick and the pin read", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "start": 1034, "end": 1082, "section_sha256": "ca86e98de294306fca4f2cbc060555b05eb036967ad333d907b761e09fb70805"}
$ git show 99c3bc88…:SKILL.md | awk 'NR>=1034 && NR<=1082'        # read the bytes
$ git show 17c1fad:scripts/shokunin-watchdog.sh | awk 'NR<=20'
$ git show 5efb4114:shokunin.conf | grep -n "tameshi"
55:tameshi|tameshi-shokunin|depth + calibration (verification-fixture craft)
$ awk 'NR>=140 && NR<=200' /home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh
$ git show 99c3bc88…:corpus/knowledge/fleet-kill-rate-ledger.md | awk 'NR>=410 && NR<=428'
$ sha256sum tools/mutate-and-run.sh
977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda  tools/mutate-and-run.sh
$ bash tools/mutate-and-run.sh --selftest   # TMPDIR set to the seat scratch
MUTATE_SELFTEST: 107/107 pass
VERDICT: PASS
rc=0
```

## Anchor sweep (cold-executor reading)

| Anchor in the section | Resolves at C1? | Evidence |
|---|---|---|
| `scripts/shokunin-watchdog.sh:3-5` at fleet `17c1fad` | **yes** | `git cat-file -t 17c1fad` → `commit`; lines 3–5 are exactly "A lane's round ends when .ufo/reports/round-<N>/<lane>.md lands; … Cap 1024/lane. Tick 450s." — the report-file round end and the 450 s tick |
| its lane map then did not name tameshi (`:14`) | **yes** | `17c1fad:scripts/shokunin-watchdog.sh:14` = `LANES="protocol aggregator kasegi kengaku kake kumitate kotoba kagi kama"` — no tameshi |
| since `5efb4114` (2026-10-19) the lanes live in `shokunin.conf`, which names tameshi | **yes** | `git cat-file -t 5efb4114` → `commit`, date `Mon Oct 19 20:00:37 2026 -0300`; `5efb4114:shokunin.conf:55` = `tameshi|tameshi-shokunin|…` |
| `../scripts/hyaku/jj-lane.sh state <repo>` and its `branch=` field | **yes** | `cmd_state()` requires exactly one argument (`[ $# -eq 1 ] \|\| usage`), resolves `$(lane_realdir "$1")`, and prints `state branch=… local=… remote=… ahead=… behind=… head=… tracked=… untracked=…` |
| `git config lane.branch` first, else function `detect_branch()` | **yes** | `cmd_state` line 165: `branch=$(lane_branch_git "$dir") \|\| branch=$(detect_branch "$dir")`; `lane_branch_git` reads `git -C "$1" config --get lane.branch` |
| the branch-tip rule in force is ER-jj, `fleet-kill-rate-ledger.md:420` | **yes** | `:420` is the `**ER-jj — jj-era reading of "HEAD" (round 17 …)**` block (branch tip `refs/heads/<branch>`, cite the resolver by function name); `:422` ER-jj2 confirms the by-name citation practice the section repeats |
| tool `cf41efaa…` (`sha256sum tools/mutate-and-run.sh`) and tool `held` | **yes** | ledger `:281`/`:320` record `cf41efaa8be5f52d…` at this tick and `held` vs ER-2's pin; ledger `:333` headline matches the section's counts exactly |
| `MUTATE_SELFTEST: 67/67` at round 8; `MUTATE_SELFTEST: 107/107 pass` at round 52 | **yes** | running the tool at C1 prints exactly `MUTATE_SELFTEST: 107/107 pass` / `VERDICT: PASS` (rc 0); the round-52 receipt `.ufo/waves/round-52/w2/T52W2Fix06.selftest.out` ends with the same two lines; SKILL.md:1016 records the 67/67 sequence |
| `4 × current · 2 × stale · 0 × drift` vs the executed-instance table | **yes** | the table has 4 `current` rows (js-kimi-census, bash-surface-census, kagi checklist-run, kumitate claims-check) and 2 `stale` rows (bash-tsukuroi-census, bash-mado-verify); ledger `:333` carries the same `current=4 stale=2 drift=0` |
| re-read gap `19:15:14Z → 19:20:29Z` = "a 5 min 15 s gap" | **yes** | arithmetic holds |

No stale line anchor, no stale table cell, no run-together token / missing space / duplicated parenthetical found in the section text.

## Finding 1 — the round-52 parenthetical's conditions do not entail "all three read no"

**Quote (byte-exact, single occurrence in the section; SKILL.md line 1042):**

> the three labels are not exhaustive — when the recorded revision is not an ancestor of the branch tip and the live file equals the tip blob, all three read no

**Why:** Those two conditions are insufficient. The `current` row of the table decides on the equality "`git show <tip>:<path>` sha256 == the recorded pin" alone — no ancestry requirement — so a case whose file bytes are unchanged between a non-ancestor recorded revision and the tip reads `current`, not "no" (fixture A). The `drift` row decides on "live sha ≠ tip blob **or** `git status --porcelain -- <path>` non-empty", so a case with the live file equal to the tip blob but a detached HEAD holding other bytes reads `drift`, not "no" (fixture B). Both fixtures hold exactly the note's two stated conditions, so the note contradicts the table rows above it and would mislabel real cases for an executor.

### Receipt A — stated conditions hold, `current` reads YES

```console
$ D=/fast/scratch/hyaku/tameshi-r54/T54W2Read06/fix-A   # mktemp -d under the seat scratch
$ git -C "$D" init -q -b main
$ printf 'alpha\n' > "$D/f"; printf 'base\n' > "$D/g"; git -C "$D" add f g; git -C "$D" commit -qm A
$ git -C "$D" checkout -q -b side; printf 'side\n' > "$D/h"; git -C "$D" add h; git -C "$D" commit -qm S
$ SREV=$(git -C "$D" rev-parse side)
$ git -C "$D" checkout -q main; printf 'base2\n' > "$D/g"; git -C "$D" commit -qam T
$ TIP=$(git -C "$D" rev-parse refs/heads/main)
recorded rev S=d8272b01b1da8e4904e70dc8a08a8892d7eb2fe1 tip=e2378e3421f7e2fd6318e48dfae3d22f0e765513
--- row1 predicate: recorded pin vs tip blob ---
pin(S:f)=b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060
tip(main:f)=b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060
live f=b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060
--- row2 predicate: ancestry ---
is-ancestor rc=1
--- row3 predicate: porcelain ---
porcelain=[]
--- verdicts by the section's table ---
current: YES (tip blob == recorded pin)
stale: no (ancestry rc=1)
drift: no
--- the two stated conditions ---
recorded revision not an ancestor of the branch tip: rc=1 => TRUE
live file equals the tip blob: b6a98d9c… = b6a98d9c… => TRUE
```

Verdict: the note's antecedent is satisfied and the table reads `current`; "all three read no" is false.

### Receipt B — stated conditions hold, `drift` reads YES

```console
$ D=/fast/scratch/hyaku/tameshi-r54/T54W2Read06/fix-B
$ git -C "$D" init -q -b main
$ printf 'beta\n' > "$D/f"; git -C "$D" add f; git -C "$D" commit -qm T1
$ T1=$(git -C "$D" rev-parse main); printf 'alpha\n' > "$D/f"; git -C "$D" commit -qam T2
$ TIP=$(git -C "$D" rev-parse refs/heads/main)
$ git -C "$D" checkout -q -b side "$T1"; printf 'divergent\n' > "$D/x"; git -C "$D" add x; git -C "$D" commit -qm D1
$ REC=$(git -C "$D" rev-parse side); git -C "$D" checkout -q --detach "$T1"; printf 'alpha\n' > "$D/f"
recorded rev=8955eac39ae0ae7cf9832727b448a91d99f54126  HEAD(detached)=df32be4c9efbfe5ed0c7511a0fe7f010ec275390  refs/heads/main=36dbcdc2743e5c3ea0a930efe4358902043d1b1f
pin(recorded rev blob)=f2c82decdd7181cf98945929a62598db7e6b477e11f6e0eb0ae97020eff151ad
live=b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060
tip blob=b6a98d9ce9a2d9149288fa3df42d377c3e42737afdcdaf714e33c0a100b51060
--- stated condition 1: recorded rev not an ancestor of tip ---
is-ancestor rc=1 (1 = not an ancestor)
--- stated condition 2: live file equals the tip blob ---
live == tip blob: YES
--- table verdicts ---
current: no
stale: no (ancestry rc=1)
porcelain=[ M f]
drift: YES
```

Verdict: the note's antecedent is satisfied and the table reads `drift`; "all three read no" is false again, this time on the `drift` row's porcelain arm.

## Candidates considered and not reported

- `fleet-kill-rate-ledger.md:420` cited by bare filename (the file lives at `corpus/knowledge/fleet-kill-rate-ledger.md`): **not reported** — bare filename is SKILL.md's established citation style for this document (lines 1096, 1098, 1101, 1131, 1213, 1243, 1257, 1286–1289 all do it), so it is not a per-section defect.
- The ER-jj block's own pointer `Canonical rule: SKILL.md:1027-1035`, which at C1 lands on the cadence preamble rather than the branch-tip rule (that rule is at 1040–1049): **not reported against this section** — the section cites `fleet-kill-rate-ledger.md:420`, which resolves correctly, and the stale pointer is the append-only ledger's dated round-17 byte, not this section's.
- `/tmp/w8-tameshi-t84/pin-read.txt` and `/tmp/w8-tameshi-t84/drift-demo.txt`: **not reported** — the section itself labels the pin read "a timestamped observation … never carried as a standing claim" and the falsifier block "scratch, read-only"; these are ephemeral round-8 demonstration paths, not rule anchors.
- "six case paths across four worktrees": **not reported** — the section does not name the worktrees and the observation is dated; no artifact at C1 falsifies the count.

## Scope

Wrote only `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w2/T54W2Read06.json` and `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w2/T54W2Read06.md`. Fixtures live under `/fast/scratch/hyaku/tameshi-r54/T54W2Read06/`. No lane file, counter, contract, freeze, ledger or wave spec edited; no git mutation in the lane; every fixture git call named `-C "$D"` with `D` under the seat scratch. No tools installed.
