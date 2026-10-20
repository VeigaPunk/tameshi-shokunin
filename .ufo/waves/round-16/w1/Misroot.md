# Misroot — round-15 `TameshiR15` fleet-root landing: mechanism, detection, failure-demonstrated guard

Seat: `TameshiR16.Misroot` (leaf, read-only; no subagents, no lane or fleet edits).
Lane root: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Fleet root: `/home/vgpnk/Projects/shokunin`.
Fleet checkout HEAD at read time: `0fb66cb26fa3083f8eef3d68680dea17f01fc8f7`.
Scratch: `/tmp/tameshi-r16-Misroot-demo` (mirror repos, guard prototypes, mutant arms).
No tool installs or upgrades were performed; no pacman transaction was run.
Date: 2026-10-20.

## 0. Summary

The round-15 `Frontier` seat (`TameshiR15.Frontier`, scribe) finished its report at
`.ufo/waves/round-15/w1/Frontier.md`, then emitted a short note addressed to its lead. The note was
written with `write` and a **bare id path `TameshiR15`** rather than the agent URL
`agent://TameshiR15`. A non-URL path is filesystem-relative, so the note became a plain 605-byte file
named `TameshiR15` at the fleet root. It was caught only post-hoc, archived byte-for-byte at
`.ufo/waves/hyaku/misroots/TameshiR15` (`HANDOFF.md:142-145`). This was not a one-off: the same
archiver records three agent-to-L1 notes written as plain fleet-root files in one campaign
(`MoriR16.Lesson`, `SoujiR15`, `TameshiR15`, `HANDOFF.md:142-143`).

The instruction defect is now pinned exactly: the round-15 wave composed **66/66 seat tasks** with
`Message only TameshiR15 …` and **0/66** with the `agent://` scheme. The shared `# Contract` that did
carry `Coordinate only agent://TameshiR15; never Main or agent://all.` (`spec1.json:3`, 2,503 B) exists
in the spec envelope and in `dispatch1.json`, but was dropped from every per-seat task string.

The recommended sweep command, `git -C <fleet> status --porcelain` with no pathspec, does catch this
artifact's shape (mirror: `?? TameshiR15`). It is **not sufficient**: a second, live fleet-root stray
(`bash: `, 2026-10-18) is invisible to it because `.gitignore`'s `*-shokunin/` ignores the only file
inside, and it shows only under `--ignored` as `!! "bash: …"`. A root-entry allowlist guard (prototype
in §4) is red on both artifacts and green after removal; the naive content predicate suggested in the
ticket ("content names tameshi") is demonstrated **not** to fire on the real 605-byte bytes.

## 1. The artifact and its provenance

| Fact | Value | Source |
|---|---|---|
| Archived path | `.ufo/waves/hyaku/misroots/TameshiR15` | `ls -la .ufo/waves/hyaku/misroots/` |
| Size / sha256 | 605 B / `b413df980b7781b8c4b904770e968391c2664c908e327d4231c4727f7f236469` | `sha256sum`, `stat` |
| Birth / mtime | 2026-10-20 05:06:36.339042586 -0300 (both) | `stat -c '%n %s %y %w'` |
| Source report | `tameshi-shokunin/.ufo/waves/round-15/w1/Frontier.md`, 16,871 B, sha256 `685e430c95a27d6853bd546cdade60deb5f80ea57d0bc217e0a989f4e9ce32e3` | `sha256sum`, `wc -c`, `stat` |
| Report mtime | 2026-10-20 05:06:34.155045426 -0300 | `stat` |
| Note-to-report delta | **2.184 s** | subtraction of the two `stat` values |
| Trailing byte | no newline; file ends `… No checks run.` at byte 605 | `xxd` tail |

The content is a handoff note, not a report body: it opens
`Frontier report written: .ufo/waves/round-15/w1/Frontier.md. Implementation-critical for L1: (1) S051 has one allocator — decide …`
and closes `No checks run.` The **file name is the recipient id** (`TameshiR15`, the round-15 lead),
not the sender id (`TameshiR15.Frontier`). That asymmetry is the first discriminator between “a note
sent to the lead” and “a report written to a wrong path”.

## 2. Mechanism (evidence chain)

### 2.1 Which seat

- `assignments1.json:65` — `"Frontier": "TameshiR15.Frontier"`.
- `record1.json:387-391` — `"kind": "spawn"`, `"agentId": "TameshiR15.Frontier"`, `"role": "scribe"`.
- `dispatch1.json:751-753` — `"name": "Frontier"` and its task string.
- `w1/Frontier.md:3` — `Seat: \`TameshiR15.Frontier\` (leaf, report-only)`.

### 2.2 The instruction the seat actually received

The runtime task in `spawn1.json:1086` is 2,017 chars and decomposes exactly:

```
2,017 = 33  ("Complete assignment thoroughly:\n\n")
      + 1,004 (dispatch1.json taskCall.tasks[Frontier].task)
      +   980 ("\n\n# Tooling directive — operator, 2026-10-19 …")
```

Verified with `startswith` (`True`) and the exact prefix/suffix lengths. The 1,004-char dispatch task
is itself the 880-char `spec1.json` item prompt plus 124 chars:

```
\n\nLane bounds: leaf member — no subagent dispatch.\n\nReport: write your scoped findings to .ufo/waves/round-15/w1/Frontier.md
```

Measured counts across the wave:

| Corpus | tasks | containing `agent://` | containing `# Contract` | containing `Message only TameshiR15` |
|---|---|---|---|---|
| `dispatch1.json` `taskCall.tasks` | 66 | **0** | **0** | **66** |
| `spawn1.json` all spawned `task` strings | 66 | **0** | — | **66** |

The only `agent://` occurrences in `spawn1.json` (2) are in the orchestrator's task-tool result prose
(`have them message each other via \`write agent://<id>\``), i.e. not in any seat prompt. By contrast
`spec1.json:3` (`context`, 2,503 chars) contains `# Contract` and the line

> Coordinate only agent://TameshiR15; never Main or agent://all.

`dispatch1.json` retains that contract in its envelope (2 raw occurrences), but no per-seat task string
contains it. **So the seat obeyed the only messaging sentence it was given, which named a bare id.**

### 2.3 Why a bare id produced a file

`write` resolves `agent://…` as an agent URL; any path without that scheme is a filesystem path, and
relative paths resolve against the process cwd — the fleet root for every seat. The product's name is
therefore exactly the path string the seat passed: `TameshiR15`.

Corroboration that this is the known harness behavior and not a guess: the round-16 seat contract
records it verbatim — “a bare name like `TameshiR16` creates a stray file at the fleet root; that
misroot happened in round 15” — and the hyaku archiver names the same cause for all three notes
(`HANDOFF.md:92-95`, `:142-145`).

### 2.4 What is observed vs inferred

| Claim | Status |
|---|---|
| Frontier wrote the report, then produced a 605 B L1-addressed note 2.184 s later | **observed** (mtimes, content) |
| The only messaging instruction in its prompt was `Message only TameshiR15` | **observed** (1,004/2,017-char strings) |
| It called `write` with path `TameshiR15` (no scheme) | **inference**, uniquely consistent with: file name = recipient id; content = the note to that id; creation 2.184 s after the report; no `agent://` in any seat prompt. The exact call is unrecoverable: `history://TameshiR15.Frontier` → `Unknown agent` (round-15 sessions are unregistered), and `spawn1.json` is a pre-run registry snapshot (`status: "pending"`, `toolCount: 0`, `recentTools: []`). |
| The shared contract was dropped at composition, not at spawn | **observed** (0/66 tasks in *both* dispatch and spawn; spec context present) |

Alternative “wrong report path” is excluded: the name is the recipient, the bytes are not the report,
and the report exists separately at its contract path with a different size and digest.

## 3. Detection

### 3.1 Command and what it shows

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain
 M .ufo/watchdog.log
?? .ufo/state/kaidoku.report-baseline
… (9 baseline files)
?? .ufo/waves/round-16/build/
```

10 lines at the last read, all under `.ufo/`; the driver churns them between reads. The decisive
check is the root-only filter:

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain -uall | grep -v /
$ echo $?
1
```

No root-level untracked entry today. The historical artifact is gone from the root; its archived copy
is what §4 replays.

On a mirror with the real `.gitignore`, the same command catches the misroot:

```
$ git -C /tmp/tameshi-r16-Misroot-demo/mirror status --porcelain
?? TameshiR15
$ git -C /tmp/tameshi-r16-Misroot-demo/mirror status --porcelain -- .ufo/
$                       # empty — this is why the hyaku sweep missed it
```

`HANDOFF.md:143` records that the three notes were “outside the `.ufo/` sweep pathspec”;
`HANDOFF.md:145` prescribes the no-pathspec command. That is correct for this artifact shape.

### 3.2 The command's proven blind spot (live artifact today)

There is a second fleet-root stray, predating the campaign:

```
$ ls -d '/home/vgpnk/Projects/shokunin/bash: '
bash:                        # name bytes: 62 61 73 68 3a 20 — trailing space
$ find 'bash: ' -type f -printf '%p\t%s\t%TY-%Tm-%Td %TH:%TM:%TS\n'
bash: /home/vgpnk/Projects/shokunin/souji-shokunin/tests/tools/souji-verify.sh: No such file or directory
        10139 bytes     2026-10-18 14:01:47.326772594
```

- The single file's sha256 is `3a127f03b9afbfef76d8cfb4274e0cb16aa7d59b915ce19e70a236321e9b3c33`,
  byte-identical (`cmp`) to
  `souji-shokunin/census/operator-sweep-20261019/stray-bash-tree-file.preserved.json`. It is a
  **known, preserved** operator-sweep artifact whose root copy was never removed — not an
  unacknowledged new misroot.
- `git status --porcelain -uall` does **not** list it. The only file's path contains a
  `souji-shokunin/` component, ignored by `.gitignore:1` (`*-shokunin/`). Only
  `git status --porcelain -uall --ignored -- 'bash: '` reveals it:

  ```
  !! "bash: /home/vgpnk/Projects/shokunin/souji-shokunin/tests/tools/souji-verify.sh: No such file or directory"
  ```

- [INFERENCE] The parent directories (`bash: /home/…/tests/tools/`) did not pre-exist and a shell
  `>` redirect cannot create them, so the writer created parents from a path string that was itself a
  captured `bash: …: No such file or directory` message. Content is an S54 adversarial JSON report
  (`{"seat":"S54","kind":"adversarial","round":4,"lane":"souji-shokunin",…}`). Same class: a
  non-URI/mistaken `write` path landed at the fleet root; the ignore rule then hid it.

## 4. Prevention, shown able to fail

Two predicates matter and only one is load-bearing:

1. **Path allowlist (primary).** Every top-level entry of the fleet checkout must be tracked at `HEAD`,
   a lane repo `*-shokunin`, or a declared scratch dir (`.git`, `.tower`, `local`, `reports`).
   This is content-independent, so it catches both artifacts.
2. **Content classifier (triage only).** Labels a stray file `LANE-NOTE` vs `UNKNOWN`. The ticket's
   example predicate `grep -qiE 'shokunin|tameshi|agent://'` **returns 1 on the real 605 bytes** — the
   note's body never names the lane. Content alone would have reported clean.

Prototype actually executed (`/tmp/tameshi-r16-Misroot-demo/guard2.sh`):

```sh
#!/usr/bin/env bash
# fleet-root misroot guard v2 (report draft)
set -u
root=${1:?usage: misroot-guard.sh <fleet-root>}
tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
git -C "$root" ls-tree --name-only HEAD | LC_ALL=C sort > "$tmp/tracked"
find "$root" -mindepth 1 -maxdepth 1 -printf '%f\n' | LC_ALL=C sort > "$tmp/entries"
LC_ALL=C comm -23 "$tmp/entries" "$tmp/tracked" |
  grep -vE '^(\.git|\.tower|local|reports|.*-shokunin)$' > "$tmp/stray" || true
n=0
while IFS= read -r e; do
  n=$((n+1))
  if [ -f "$root/$e" ]; then
    if grep -qiE 'agent://|\.ufo/waves/|corpus/|SKILL\.md|SCORECARD\.md|Report:|round-[0-9]+' "$root/$e"; then
      printf 'STRAY [%s] (file, LANE-NOTE)\n' "$e"
    else
      printf 'STRAY [%s] (file, UNKNOWN)\n' "$e"
    fi
  else
    printf 'STRAY [%s] (dir)\n' "$e"
  fi
done < "$tmp/stray"
[ "$n" -eq 0 ] || exit 1
exit 0
```

Observed matrix (all commands run; exit codes are the script's):

| # | Arm | rc | Key output |
|---|---|---|---|
| 1 | clean mirror (tracked entries only) | 0 | — |
| 2 | replay archived `TameshiR15` bytes at mirror root | **1** | `STRAY [TameshiR15] (file, LANE-NOTE)` |
| 3 | naive content-only on the same bytes | grep **1** | no match — a content-only guard reports clean |
| 4 | `git status --porcelain` on the same mirror | 0 | `?? TameshiR15` |
| 5 | same, `-- .ufo/` pathspec | 0 | empty (the round-15 sweep shape) |
| 6 | mirror + live `bash: ` tree, plain `git status -uall` | 0 | tree absent |
| 7 | same, `--ignored` | 0 | `!! "bash: …/souji-verify.sh: No such file or directory"` |
| 8 | guard on the same mirror | **1** | `STRAY [TameshiR15] (file, LANE-NOTE)` / `STRAY [bash: ] (dir)` |
| 9 | remove the stray file, keep the tree | **1** | `STRAY [bash: ] (dir)` |
| 10 | remove both | 0 | — |
| 11 | guard on the **live fleet root** | **1** | `STRAY [bash: ] (dir)` |
| 12 | mutant: allowlist without `local`,`reports` (live) | **1** | `STRAY [bash: ]`, `STRAY [local]`, `STRAY [reports]` |
| 13 | mutant: tracked list emptied (live) | **1** | 21 lines, e.g. `STRAY [.devin] (dir)`, `STRAY [AXIS…]` |

Reading: arms 2–3 show the content predicate is not load-bearing; arms 4–5 reproduce the historic
sweep miss; arms 6–7 show the recommended command's blind spot on live data; arms 8–11 show the
allowlist detects both shapes and goes green when the artifact is removed; arms 12–13 show the
allowlist is calibrated, not inert (removing rows changes the verdict).

## Mistakes

Draft row for `corpus/lessons/round-16.md` (CORPUS.md:171-177 shape; class from the `mistakes.md` §5
vocabulary at CORPUS.md:174):

| Class | Evidence pointer | Captured-by | Fix and falsification |
|---|---|---|---|
| landing | `.ufo/waves/hyaku/misroots/TameshiR15` — 605 B, sha256 `b413df98…`, born 2026-10-20 05:06:36.339, 2.184 s after `round-15/w1/Frontier.md` (16,871 B, `685e430c…`); content is the Frontier→L1 note. Prompt chain: `spec1.json:3` 2,503 B carries `Coordinate only agent://TameshiR15`, but `dispatch1.json:751-753` Frontier task = 1,004 B and `spawn1.json:1086` = 2,017 B, with **0/66** tasks carrying `agent://` and **66/66** carrying `Message only TameshiR15` | `none` mechanically: no QUALITY criterion covers write-path landing (`corpus/QUALITY.md` ends at criterion 17, line 84); criterion 9 (scratch in `/tmp`, evidence copied into the repo) is adjacent but does not cover an agent-addressed note, and the nearest rule `PROTOCOL.md:468` (“Lanes write only inside their own child repo and their lane report”) is commit-framed and unmechanized; detection happened post-hoc in the hyaku archive (`HANDOFF.md:142-145`) | Emit the lead as `agent://<id>` in every per-seat prompt (round-15 dropped the shared `# Contract`; round-16’s contract now states the prefix is mandatory) and land a root-entry allowlist gate (`.ufo/gates/fleet-root.py`, prototype §4). Red-before: replay of the archived bytes → rc 1 `STRAY [TameshiR15] (file, LANE-NOTE)`; live `bash: ` tree → rc 1, invisible to `git status`; green after removal → rc 0. Kept falsifications: the content-only predicate returns 1 on the real bytes, and the `.ufo/` pathspec arm returns 0 on the same replay. |

Class note: `landing` (C09 “Evidence landing”) is the visible failure; `attribution` (C10
“Write-scope / attribution”) is the sibling mechanism — the fleet checkout acquired an
agent-named artifact with no lane ownership. One class per row, so `landing`.

## 5. Bounded recommendations

- **R1 — instruction (owner: round owner / L1).** Every dispatched seat prompt must carry the lead as
  `agent://<id>` verbatim, and the messaging interface must be one of the items checked by the
  prompt-fidelity rule (`PROTOCOL.md:101-102`). Falsifier already available: scan a wave's
  `spawn1.json` for `agent://` in `task` strings; round-15 w1 measures 0/66, round-16’s contract
  measures present-by-construction.
- **R2 — write-path lint (owner: harness/operator side).** Refuse a `write` path matching a bare agent
  id (`^[A-Z][A-Za-z0-9]*R[0-9]+(\.[A-Za-z0-9]+)?$`) unless it starts `agent://`. This is the exact
  shape that produced `TameshiR15`. Not demonstrated here: replaying it through the live harness would
  create a second fleet-root file, which this read-only seat must not do.
- **R3 — fleet gate (owner: protocol lane).** Land `.ufo/gates/fleet-root.py` following the registered
  `root-ledgers` convention (`root-ledgers.py:1-30`: deterministic findings, fixtures, exit map
  0 clean / 1 failed / 2 could-not-evaluate). Fixtures should include arms 2, 5, 6, 8, 10 and 12 of
  §4; expected.json should pin `STRAY [TameshiR15] (file, LANE-NOTE)` and `STRAY [bash: ] (dir)`.
- **R4 — live residue (owner: operator).** `bash: ` is byte-identical to the souji preserved copy
  (`3a127f03…`). Relocate it under `.ufo/waves/hyaku/misroots/` (as the three agent notes were) or add
  an explicit allowlist entry with that digest; then R3’s gate exits 0. Do not delete without the
  preserved copy being confirmed — it is, by `cmp`.
- **R5 — sweep procedure.** Keep `git -C <fleet> status --porcelain` **with no pathspec** as the
  cheap check, but pair it with the root-entry allowlist: the no-pathspec command is blind to strays
  whose only content sits under an ignored path (`bash: ` today). Run after the round’s integration
  commit so legitimate untracked evidence is not flagged as a misroot.

## 6. Command log (observed)

| Command | rc | Key line |
|---|---|---|
| `git -C <fleet> status --porcelain` | 0 | 10 lines, all `.ufo/…`; no root entry |
| `git -C <fleet> status --porcelain -uall \| grep -v /` | 1 | empty |
| `git -C <fleet> status --porcelain -uall --ignored -- 'bash: '` | 0 | `!! "bash: …/souji-verify.sh: No such file or directory"` |
| `sha256sum .ufo/waves/hyaku/misroots/TameshiR15` | 0 | `b413df98…` |
| `sha256sum tameshi-shokunin/.ufo/waves/round-15/w1/Frontier.md` | 0 | `685e430c…` |
| `stat -c '%n %s %y %w' <archived> <report>` | 0 | mtimes 05:06:36.339 / 05:06:34.155 |
| `python3` prompt decomposition (`spec1`/`dispatch1`/`spawn1`) | 0 | 880 → 1,004 → 2,017; 66/66 bare id; 0/66 `agent://` |
| `git -C <fleet> rev-parse HEAD` | 0 | `0fb66cb2…` |
| `sha256sum` live `bash: ` file vs souji preserved JSON | 0 | both `3a127f03…`; `cmp` → `IDENTICAL` |
| `guard2.sh` arms 1–13 (§4) | 0/1 as tabled | see matrix |

## 7. Limits

- No tool call transcript exists for round 15 (`history://TameshiR15.Frontier` → `Unknown agent`); the
  `write` call itself is reconstructed, marked [INFERENCE] in §2.4, and bounded by four independent
  observations (name, content, 2.184 s delta, 0/66 prompt scheme).
- The harness `write` behavior was not replayed (it would create a new misroot at the fleet root);
  the guard demo used filesystem mirrors, and the harness statement is cited from the round-16
  contract plus the archived instance.
- `bash: ` provenance (parent-dir creation by the writer) is [INFERENCE]; its identity and bytes are
  observed and hash-matched.
- No commits, no git add, no edits outside this report; scratch only under
  `/tmp/tameshi-r16-Misroot-demo`.
