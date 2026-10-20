# MisrootSweep — fleet-root misroot sweep for tameshi round-16 seats

Seat: TameshiR16.MisrootSweep (wave 2, falsify lane). Assigned question: do untracked/ignored
fleet-root entries exist whose **name or content** points at tameshi round-16 seats
(`TameshiR16*`, fleet-root `.ufo/waves/round-16`, `CR*/RG*/RR*.md`)? Read-only; nothing deleted.

## Verdict

**Falls (hypothesis falsified):** no tameshi round-16 seat artifact exists at the fleet root.
Zero `TameshiR16*` names, zero `CR*/RG/RR*.md` outside lane repos, zero wave-1/wave-2 seat
basenames outside `tameshi-shokunin/`. Three adjacent notes are recorded below: the one untracked
entry whose *content* encodes tameshi round 16 is expected watchdog state; a mid-sweep jj trial
wave names tameshi only as a subject repo (`JjTrialTameshi`, no R16 seat); and the sweep recipe
quoted at `HANDOFF.md:145` (`git status --porcelain`, no `--ignored`) provably misses ignored
strays.

## Commands and exits

All from `/home/vgpnk/Projects/shokunin`.

| command | exit | key output |
|---|---|---|
| `git -C . status --porcelain` | 0 | 13 lines at 10:55:19 (12 at 10:52): 1 `M .ufo/watchdog.log`, 12 `??` (9 `.ufo/state/*.report-baseline`, 2 `scripts/hyaku/jj-lane*.sh`, `.ufo/waves/hyaku/jj-w1/`) |
| `git -C . status --porcelain --ignored -- .` | 0 | 50 entries: the same 13 + 37 `!!` (`.tower/`, `bash: /`, 14 `*-scratch/`, 21 `*-shokunin/`) |
| `git status --porcelain \| grep -c 'bash'` | 1 | `0` — the stray is **invisible** without `--ignored` |
| `git status --porcelain --ignored \| grep bash` | 0 | `!! "bash: /"` |
| `git check-ignore -v -- 'bash: /…/No such file or directory'` | 0 | `.gitignore:1:*-shokunin/` (rule match proved) |
| `git status --porcelain --ignored -- .ufo/waves/round-16` | 0 | empty (dir is tracked and clean) |
| `find . -name '*TameshiR16*'` (lane repos + `.git` pruned) | 0 | empty |
| `find . \( -name 'CR*.md' -o -name 'RG*.md' -o -name 'RR*.md' \)` (lane repos + `.git` pruned) | 0 | empty |
| `grep -rl 'TameshiR16'` (lane repos + `.git` excluded) | 1 | empty; positive control `TameshiR15` → `.ufo/waves/hyaku/HANDOFF.md` (grep is sensitive) |
| `find . -name Overlap1.md / Frontier.md / RoutedDefects.md / MisrootSweep.md` outside `tameshi-shokunin/` | 0 | only `souji-shokunin/.ufo/waves/round-15/w1/RoutedDefects.md` (other lane, prior round, inside its lane) |

## Entries whose name/content points at tameshi round 16

Exactly **one** entry in the untracked set qualifies, and it is tooling state, not a leaked seat file:

### `.ufo/state/tameshi.report-baseline` — untracked, 68 bytes
- sha256 `096c86cb77732f5fd6c969cbcb67addc696702bf72fd0b12a82170c84be9c23a`
- first line: `16 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Format is `<round> <report-sha256>`, per `scripts/shokunin-watchdog.sh:31` ("holds \"round SHA256\"
  for the report bytes captured immediately before launch"). `e3b0c442…b855` is sha256 of empty
  input (verified: `printf '' | sha256sum`), which `report_digest` returns when the report file is
  absent (`scripts/shokunin-watchdog.sh:112-118`), written by `record_report_baseline`
  (`:121-137`) *before* launch.
- mtime `2026-10-20 10:14:08.425514781 -0300`; `.ufo/watchdog.log:476` records
  `2026-10-20T10:14:09-03:00 launch tameshi round=16 pgid=11738 driver=hyaku-inline attempt=1`.
- Classification: **expected fleet-root state keyed by lane** (same shape as the other eight
  baselines; e.g. `kaidoku.report-baseline` reads `17 …`, matching its round-17 dispatch). Not a
  misroot.

The prompt-designated report path `/home/vgpnk/Projects/shokunin/.ufo/reports/round-16/tameshi.md`
(`.ufo/prompts/tameshi-round-16.md:101,242,258`) **does not exist** (round still in flight); it is a
tracked-dir target, not an untracked entry.

## `.ufo/waves/round-16` at the fleet root — tracked, name collision, not tameshi

Clean to git (`git status --ignored -- .ufo/waves/round-16` → empty), all six files tracked:

| path | bytes | sha256 | first line |
|---|---|---|---|
| `before.md` | 8142 | `7464f5860fa76e2c8ea4978e4450a2ae76f6602b0d36b25ddf6891ac6d001ccd` | `# Round 16 — BEFORE measurements (protocol lane)` |
| `dispatch.md` | 2768 | `955cae0bf4bb2f570e9020f81bc4cdc15701ab67622e9346e26dc7de954ded42` | `# Protocol round 16 — L2 dispatch receipt` |
| `clobber/classify.sh` | 5323 | `ef4ac7fd538282388436a376c717af4c6769c0ac8e71fedbe13b6eafc5144438` | `#!/bin/sh` |
| `clobber/classify.out` | 8864 | `23d299238580864c0566716059e65ebc908839e6164b7a2edb97768ddb0e5019` | `====…====` |
| `gate/mutate.sh` | 3084 | `ae7f7a95c6575ca243298d51784e0ac864f6ce4e61b268a6e326586cd1cdbd88` | `#!/bin/sh` |
| `gate/runs.md` | 4029 | `b6a41e0971c44cdb62bdecab312e0cded0339a492831f8f0d0af44bdcf3c65bd` | `# root-ledgers gate — round-16 runs (protocol lane)` |

Content disambiguates the collision: this is the **protocol lane's** round 16, tracked since
2026-10-19 20:10. A name-keyed sweep must not flag it.

## Adjacent real stray (out of tameshi scope) and why the recommended sweep misses it

`bash: ` — a directory at the fleet root whose basename is `bash:` + one trailing space (6 bytes:
`printf '%s' 'bash: ' | wc -c` → `6`; the `8` in `find`'s `d|bash: |8` is the directory's size, not
its name), holding a literal path tree
`home/vgpnk/Projects/shokunin/souji-shokunin/tests/tools/souji-verify.sh: No such file or directory`
(10139 bytes, one file).

- file sha256 `3a127f03b9afbfef76d8cfb4274e0cb16aa7d59b915ce19e70a236321e9b3c33`; first line `{`
- payload is invalid JSON (`jq` fails at byte 999: missing values such as `"live_ledger_lines_before": ,`);
  it is a souji-shokunin adversarial-run result, `"seat":"S54"`, `"round":4`,
  `"verdict":"false-SAFE/contract failures present: 7"` — it points at **souji**, not tameshi R16.
- It is ignored **only incidentally**: the literal path embeds `souji-shokunin/`, which matches
  `.gitignore:1:*-shokunin/`. Hence `git status --porcelain` returns 0 matching lines for `bash`
  (grep exit 1); the entry appears only with `--ignored`.
- Consequence for R16: `HANDOFF.md:145` says "Future misroot sweeps should check
  `git -C <fleet> status --porcelain` with no pathspec." That recipe is **necessary but not
  sufficient** — a literal-path stray that happens to embed a `*-shokunin/` component is masked by
  the same rule that hides the lane repos. A sweep needs `--ignored` (as this seat's Target
  specifies) or a separate `find` census.

## Second untracked pointer, added mid-sweep: `.ufo/waves/hyaku/jj-w1/`

Absent at 10:52, present at 10:55 (live peers). 296,608 B; a **jj-colocation trial wave**, not an
R16 seat wave:

| path | bytes | sha256 | first line |
|---|---|---|---|
| `spec.json` | 132638 | `a5b0fdde7e8b0ed5463576525a0b545f62e09b8becd135e8bd184eb10623d5a7` | `{` |
| `dispatch.json` | 155610 | `5c4f2bd05127c9b2f442183678e398d1b4d52a1dbfcbed0d5b9910ca06e42d0c` | `{` |
| `reports/swarm-registry.json` | 8360 | `894b8a4c7db57dd01d410cadefd3f1d6c132fc48c1de18862f028259e335cf09` | `{` |

Its seat names are `JjTrialTameshi` / `JjAuditTameshi` (`spec.json:102,212`), and it treats
`tameshi-shokunin` as the **subject repo** of an empirical trial/audit, with reports routed to
`.ufo/waves/hyaku/jj-w1/reports/` at the fleet root by design. It contains no `TameshiR16` string
(grep of the directory → only "Tameshi" as part of those two trial seat names). A sweep keyed on
the loose token `Tameshi` would false-positive here; the precise `TameshiR16` token does not.

## Coverage of seat-name signatures (the actual misroot test)

Lane commit `c699c8c` wave 1 contains `CR01…CR27`, `CRCritic1/2`, `CRLedger`, `RG*`, `Overlap1/2`,
`FrontierMap`, `Misroot`, `QualityAudit`, `swarm-registry.json` under lane
`.ufo/waves/round-16/w1/`; current wave 2 holds `swarm-registry.json`, `ToolsNoHarm.md`,
`WaveCounts.md`, `RR01.md`, `Replica1548.md` under the lane root only. A fleet-root `find` for each
seat basename (and `swarm-registry.json`) outside `tameshi-shokunin/` found **no** round-16 copy; the
only hit was another lane's in-lane file (`souji-shokunin/.ufo/waves/round-15/w1/RoutedDefects.md`).
Wave evidence therefore lives only where the prompt says (`tameshi-round-16.md:191-192`, lane-relative
`reportDir`).

## Limits of this sweep

- The untracked set is live: it grew from 48 to 50 porcelain entries during the sweep and the
  `.ufo/waves/hyaku/jj-w1/` directory appeared between two reads. All counts above are pinned to
  `2026-10-20T10:55:19-03:00`; a later sweep must re-run the censuses rather than reuse them.
- Git is blind to empty directories: `local/` (contains empty `local/fleet-analysis/`) and
  `reports/` (empty) produce zero porcelain lines and zero tracked files, so an empty or
  never-written directed misroot is undetectable by status alone.
- `scripts/hyaku/jj-lane*.sh` are untracked and **live-mutated** during the sweep by a peer:
  `jj-lane.sh` stable at 10872 B / `ce518e25add51f1da1310cc58da48348d4df9e1c46f2447ca2ede709730c1fe2`
  (mtime 10:49:24); `jj-lane-selftest.sh` changed 12465 → 12545 B between reads, final
  `502273204a738fec7e0e1a6a7af6910e2d22cd369ed04d9b627684436c0ab54b` (mtime 10:53:45). Neither
  contains `tameshi`/`round-16`/`R16` (grep exit 1), so neither is a seat artifact.
- `.ufo/watchdog.log` (tracked, `M`, 34247 B) is the only modified tracked file and is the anchor
  for the baseline timestamp (`:476`); it is not an untracked/ignored entry.
- Lane-repo contents (21 ignored `*-shokunin/` trees, sizes recorded by `du -sb`, e.g.
  `tameshi-shokunin/` 24,104,833 B, `.tower/` 129,000,874 B) were inspected only for the named
  basenames above, not exhaustively.

## Tooling

No installs or upgrades performed; pacman is paused host-wide per the lane contract. `jq`, `git`,
GNU findutils and coreutils were already present. Scratch: none created (all probes read-only,
in-process); no files deleted.
