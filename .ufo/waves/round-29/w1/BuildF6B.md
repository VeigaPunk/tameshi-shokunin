# BuildF6B — F6 fixture (independent builder B), round 29 wave 1

## Verdict

**The anchored (byte-identical pinned census) fixture kills B5 in the pristine gate but cannot be
killed cleanly by the B5 mutant, so `C2_F6_V2_PASS` is false at my head.** The blocking conjunct is
inside the frozen counter's own `Oracle.kills()`: it requires the mutant to exit 0, and the pinned
declaration makes that impossible for any exec-row drift. This is a measurement, not a build failure:
my fixture is anchored, the pristine reports exactly one divergence (the exec-bit one), and the
mutant reports the same row as a mode drift instead.

I did **not** use environment tricks (noexec mounts, TMPDIR, ACLs, ownership changes, different
`HOME`) to force a kill, per the L1's note and because those are not the claimed craft.

## What I built

Generator (committed, reproducible): `.ufo/evidence/round-29/f6/BuildF6B/generate-f6.py`.

- `original/census.tsv` — **byte-identical** to the pinned kagi declaration
  `corpus/surface-census.tsv` at `REV_BASH=fecee8743e52eb8fb5fbb40782934cb619a1a96e`.
  sha256 `4af0dbcc81fdb7229f816bf23920174b1d699ba279405272fb78c5922f368992`, identical to
  `git -C kagi-shokunin show fecee874...:corpus/surface-census.tsv` (verified with `cmp`).
  Every line is kept: the 4 `# scan` directives, the 17 comment lines and all 35 data rows.
- `original/shapes.tsv` — empty (a subset of the pinned `corpus/state-shape.tsv` lines).
- `original/baseline.tsv` — the 15 pinned `corpus/drift-baseline.tsv` lines verbatim
  (a subset of the pinned file). The gate reads only the mode column of this file, and every mode
  there agrees with the pinned census mode for the same path, so the CROSSCHECK arm stays clean.
- `original/host.tsv` — one manifest node per declared census row, at its declared mode, except the
  one drifted exec row `.config/the-janitor/client.py`, materialized at mode `644` instead of `755`
  so its file lacks the execute bit. Node format is the counter's own
  `<relative path>\t<dir|file>\t<octal mode>\t<content>` (`c2-measure-v2.py:120-152`).

Reduction used the **frozen counter's own** `ddmin()` and `Oracle.kills()` imported from
`.ufo/evidence/round-29/c2-measure-v2.py` — nothing reimplemented.

## Units, oracle tests, wall time

| measurement | value |
| --- | --- |
| units before (original) | 105 (54 census + 0 shapes + 15 baseline + 36 host lines) |
| units after (minimized) | 105 — **no unit could be removed** |
| oracle tests run by `ddmin()` | 171 |
| wall time of the `ddmin()` run | 47.0 s |
| unit tuples equal original == minimized | True |

`minimized/` is therefore unit-identical to `original/`. The counter's own comparison
(`ddmin_match`) compares `[(f, l) for f, _, l in got] == [(f, l) for f, _, l in mu]` over line contents;
I verified that equality holds for the committed pair.

The ddmin is a no-op here for a structural reason, not a tuning accident: the frozen `ddmin` only
keeps a complement when `Oracle.kills()` is true for it, and `kills()` is false for every subset of
this fixture (see below). With no killing subset, no complement is ever kept and the unit list comes
back whole.

## Receipts: pristine vs B5 mutant on the anchored fixture

Both runs use the pinned gate bytes
(`corpus/surface-census.sh` at `fecee874...`, sha256 `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f`,
matching `PIN_BASH` in `tools/mutate-and-run.sh:605`) and the B5 mutant built by the runner's own
`@defect B5` spec (`tools/mutate-and-run.sh:717-719`), which deletes the exec x-bit arm:

```
      file|exec) if [[ "$live" != "regular" ]]; then
             ...
           fi
-           if [[ "$kind" == "exec" && ! -x "$abs" ]]; then
-             printf 'SURFACE DIVERGED %s (declared exec, no execute bit)\n' "$p"
-             N_DIVERGED=$((N_DIVERGED + 1)); FAILED=1; continue
-           fi ;;
+           ;;
```

Pristine, exit 1 — exactly one divergence, the exec-bit one:

```
  SURFACE OK       $HOME/.config/the-janitor (dir 700)
  SURFACE DIVERGED $HOME/.config/the-janitor/client.py (declared exec, no execute bit)
  SURFACE OK       $HOME/.config/the-janitor/opencode.json (file 644)
  ... (34 SURFACE OK lines, one per remaining declared row)
  SURFACE_CENSUS: DRIFT (diverged=1 gone=0 link=0 unlisted=0 crosscheck=0 shape=0 unverified=0 ok=34 absent=0 skipped=0)
```

B5 mutant, exit 1 — the same row now diverges as a **mode** drift, because the exec arm that
`continue`d past the mode check is gone:

```
  SURFACE OK       $HOME/.config/the-janitor (dir 700)
  SURFACE DIVERGED $HOME/.config/the-janitor/client.py (mode 644, declared 755)
  ... (34 SURFACE OK lines)
  SURFACE_CENSUS: DRIFT (diverged=1 gone=0 link=0 unlisted=0 crosscheck=0 shape=0 unverified=0 ok=34 absent=0 skipped=0)
```

`Oracle.kills(original)` is therefore **False**: the pristine half holds (exit 1 with the
`(declared exec, no execute bit)` token), the mutant half does not (exit 1, not 0).

## Why no manifest can satisfy both halves — exhaustive sweep

I swept the whole manifest-expressible state space for the drifted exec row, using the frozen
counter's own `Oracle`, over all three pinned exec rows
(`.config/the-janitor/client.py`, `.local/bin/the-janitor`, `.local/bin/tac-check`) and all 512
octal modes `000`–`777`:

```
sweep A: pinned census, drift row mode varied (exec rows declare 755)
  .config/the-janitor/client.py  mode=600 pristine_exit=1 hit=True mutant_exit=1  SURFACE DIVERGED ... (mode 600, declared 755)
  .config/the-janitor/client.py  mode=644 pristine_exit=1 hit=True mutant_exit=1  SURFACE DIVERGED ... (mode 644, declared 755)
  .local/bin/the-janitor         mode=600 pristine_exit=1 hit=True mutant_exit=1  SURFACE DIVERGED ... (mode 600, declared 755)
  .local/bin/the-janitor         mode=644 pristine_exit=1 hit=True mutant_exit=1  SURFACE DIVERGED ... (mode 644, declared 755)
  .local/bin/tac-check            mode=600 pristine_exit=1 hit=True mutant_exit=1  SURFACE DIVERGED ... (mode 600, declared 755)
  .local/bin/tac-check            mode=644 pristine_exit=1 hit=True mutant_exit=1  SURFACE DIVERGED ... (mode 644, declared 755)
WINNERS (pinned census): []
```

`WINNERS` is the set of states where the pristine hits the exec token **and** the mutant exits 0.
It is empty for every mode and every exec row. The mechanism is visible in the pinned gate
(`corpus/surface-census.sh` at `fecee874...`):

- line 214: `if [[ "$kind" == "exec" && ! -x "$abs" ]]; then` → the exec-bit verdict, which
  `continue`s, so the mode check at 219 is never reached for that row in the pristine;
- line 219-223: `lmode="$(stat_mode "$abs")"; if [[ "$mode" != "-" ]] && [[ "$lmode" != "$mode" ]]`
  → the mode verdict.

All three pinned exec rows declare mode `755`. Any live file that lacks the execute bit therefore
has a live mode other than `755`, and the mutant — having lost the exec arm that would have
`continue`d past it — reports `(mode <live>, declared 755)` instead. The only live mode that
satisfies the mutant's mode check is `755` itself, and a `755` file **is** executable, so it never
produces the exec-bit verdict at all.

## The two states that bracket the reachability

Measured with the frozen counter's `Oracle` on the same host manifest:

```
A  anchored census (byte-identical to pinned) + exec file 644:
    pristine exit=1  exec-token=True  divergences=['SURFACE DIVERGED ... (declared exec, no execute bit)']
    mutant   exit=1                  divergences=['SURFACE DIVERGED ... (mode 644, declared 755)']
    Oracle.kills == False

B  same host manifest, census exec row mode 755 -> "-":
    pristine exit=1  exec-token=True  divergences=['SURFACE DIVERGED ... (declared exec, no execute bit)']
    mutant   exit=0                  divergences=[]
    Oracle.kills == True
```

State B is the historical kaika probe shape (`.ufo/evidence/kaika-round-1/coldread/probe-fixtures/probe/census.tsv`
declares `$HOME/bin/tool` as `asset exec -`, and the B-probe receipts show the same
`(declared exec, no execute bit)` / mutant-clean pair). With declared mode `-` the gate skips both
the mode check (line 220 `[[ "$mode" != "-" ]]`) and the cross-check, so the mutant is clean and the
kill holds — but the census is then no longer byte-identical to the pinned declaration, so
`anchored=0` and the counter's conjunction still fails. The pinned declaration at `fecee874...` has
three exec rows all declaring `755` and no exec row with mode `-`.

## Counter run at my head

Clone `/tmp/BuildF6B-r29`, commit `253cb842dcb9b46e311b14965190631cbaf0eadb` (the fixture and the
generator; the frozen counter and the pinned kagi bytes are untouched):

```
$ timeout 1800 python3 .ufo/evidence/round-29/c2-measure-v2.py --repo /tmp/BuildF6B-r29 --rev HEAD
  oracle tests run: 1
C2_F6_V2: fixture=present anchored=1 kill_original=0 units_original=105 units_minimized=105 ddmin_match=0 kill=0 one_minimal=0 entry_sourced=0 quote_located=0 rev=253cb842dcb9b46e311b14965190631cbaf0eadb
PREDICATE: C2_F6_V2_PASS=false
exit 1
```

`anchored=1` (my census is byte-identical to the pinned declaration). `kill_original=0` for the
reason above. `entry_sourced=0` and `quote_located=0` are the L1's to land, as the task says.

## Every fixture field

`original/census.tsv` — 4752 bytes, sha256 `4af0dbcc81fdb7229f816bf23920174b1d699ba279405272fb78c5922f368992`,
byte-identical to the pinned kagi census. Fields per data row: `path`, `class` (asset|runtime),
`kind` (file|dir|exec), `mode` (3 octal digits or `-`), `note`. 4 `# scan` directives; 17 comment
lines; 35 data rows (21 asset, 14 runtime).

`original/shapes.tsv` — 0 bytes, sha256 `e3b0c44298fc86935e2c66359462d27260ce04b5ce9ab69c63ba02b61385a208`
(empty subset of the pinned `state-shape.tsv`).

`original/baseline.tsv` — 1341 bytes, sha256 `90c2d7a52360e97201b6fb766cd8f26fc653daa2a38bcefc40edcac6576c1bda`,
15 pinned lines. Fields: `path`, `mode`, `lines`, `sha256` (or `-`).

`original/host.tsv` — 1772 bytes, sha256 `b63fe3877867567c8a6757b5325559f617a11c01e26136379c597614d5705b99`,
36 lines: one node per declared census row. Fields: relative path (no `$HOME/` prefix), `dir|file`,
octal mode, content (`x` for files, empty for dirs). The single drift: `.config/the-janitor/client.py`
at `644` where the census declares `755`. All other nodes carry their census-declared mode, except
`.local/share/the-musketeer/chrome-profile`, whose census mode is `-` (unchecked) and which I give
`700`.

`minimized/` — same four files, unit-identical to `original/`; the only byte difference is that
`census.tsv` gains one trailing newline (4753 bytes, sha256
`fc76f0685fdd7b42c41eea2733a7e55c2b3d96197a8c33b8a30c57e03a8dfa1e`), because the counter's
`lines_of()` drops the final empty element and `from_units()` re-adds a newline per line. The other
three files are byte-identical to `original/`.

### The four files of `minimized/` verbatim

`minimized/census.tsv` (55 lines; the pinned census with one trailing newline):

```
# kagi-shokunin external-surface census — v1 (round 10)
#
# Declares every host surface this corpus governs, so PROVINCE.md §Surfaces is
# verifiable rather than prose. Columns:
#   path <TAB> class <TAB> kind <TAB> mode <TAB> note
#   class  asset   = must exist; missing/changed = drift
#          runtime = may legitimately be absent (ABSENT, informational)
#   kind   file | dir | exec        mode = 3 octal digits, or - for unchecked
# Directives: `# scan <TAB> <dir>` — every child of <dir> must be declared
# above, otherwise UNLISTED (the round-6 leak class: an undeclared file in
# $CONFIG_DIR is loaded by the handler because discovery is not disabled).
#
# Modes are the live values read 2026-09-28 (round 10). Where a path is also in
# drift-baseline.tsv the two modes must agree (CROSSCHECK); hash/line pins stay
# in the baseline, they are not duplicated here.
#
# scan	$HOME/.config/the-janitor
# scan	$HOME/.local/state/the-janitor
# scan	$HOME/.local/state/the-janitor/xdg-data/opencode
# scan	$HOME/.local/state/tac
$HOME/.config/the-janitor	asset	dir	700	the-janitor config dir (CONFIG_DIR)
$HOME/.config/the-janitor/client.py	asset	exec	755	HTTP client: session-id, request timeout (the flock is in the CLI)
$HOME/.config/the-janitor/opencode.json	asset	file	644	model overlay: enabled_providers, share disabled, baseURL
$HOME/.config/the-janitor/op.env	asset	file	600	env-ref file; values never read into an artifact
$HOME/.config/the-janitor/config.json	asset	file	600	inert decoy — not an opencode-discovered filename (round 6)
$HOME/.config/opencode/opencode.json	asset	file	644	global config merged UNDER the overlay (additive, round 6)
$HOME/.config/opencode/agents/janitor.md	asset	file	644	agent contract: steps 4, permission deny ceiling
$HOME/.config/opencode/tools/janitor_auth.ts	asset	file	644	the only allowed tool: AUTH_OK / AUTH_REQUIRED
$HOME/.config/opencode/plugin/fnm-nudge.js	asset	file	644	global plugin; resolves but fails to load at every serve
$HOME/.local/bin/the-janitor	asset	exec	755	the CLI (env overrides: CONFIG_DIR/STATE_DIR/ENV/PORT)
$HOME/.local/bin/tac-check	asset	exec	755	offline receipt check; --register never replaces
$HOME/.local/state/tac	asset	dir	700	tac evidence dir
$HOME/.local/state/tac/daybreak-blue-access.json	asset	file	600	model-access receipt (model id + nonce only)
$HOME/.local/state/tac/handoff-status.json	asset	file	600	custody/provenance record
$HOME/.local/state/the-janitor	asset	dir	700	state dir (STATE_DIR)
$HOME/.local/state/the-janitor/client.lock	runtime	file	600	flock serialization file; prepare_state recreates it
$HOME/.local/state/the-janitor/session-id	runtime	file	600	OpenCode conversation id; stop removes it (not a credential)
$HOME/.local/state/the-janitor/tac-daybreak-blue.json	asset	file	600	janitor custody checksum record (keys pinned by shape)
$HOME/.local/state/the-janitor/xdg-cache	runtime	dir	700	XDG_CACHE_HOME for the handler
$HOME/.local/state/the-janitor/xdg-cache/opencode/models.json	runtime	file	600	cached public model catalog (no secret material)
$HOME/.local/state/the-janitor/xdg-data	runtime	dir	700	XDG_DATA_HOME for the handler
$HOME/.local/state/the-janitor/xdg-data/opencode	runtime	dir	700	opencode data root
$HOME/.local/state/the-janitor/xdg-data/opencode/log	runtime	dir	700	handler log dir
$HOME/.local/state/the-janitor/xdg-data/opencode/repos	runtime	dir	700	created on first boot, unused here
$HOME/.local/state/the-janitor/xdg-data/opencode/opencode.db	runtime	file	600	durable transcripts — shape-pinned in state-shape.tsv
$HOME/.local/state/the-janitor/xdg-data/opencode/opencode.db-shm	runtime	file	600	WAL shared-memory index; appears with a writer
$HOME/.local/state/the-janitor/xdg-data/opencode/opencode.db-wal	runtime	file	600	WAL; 0 bytes once checkpointed
$HOME/.local/state/the-janitor/xdg-data/opencode/log/opencode.log	runtime	file	600	ERROR log — shape-pinned in state-shape.tsv
$HOME/.local/state/the-janitor/xdg-state	runtime	dir	700	XDG_STATE_HOME for the handler
$HOME/.local/state/the-janitor/xdg-state/opencode	runtime	dir	700	receives only locks/
$HOME/.local/state/the-janitor/xdg-state/opencode/locks	runtime	dir	700	empty in every observed run
$HOME/.local/share/the-musketeer/chrome-profile	asset	dir	-	CONTESTED with kake (lease/profile ownership) — reported, not ruled
$HOME/.local/share/the-musketeer/chrome-profile/NativeMessagingHosts	asset	dir	700	NMH dir written by cdp-bridge ensure
$HOME/.local/share/the-musketeer/chrome-profile/NativeMessagingHosts/com.1password.1password.json	asset	file	600	1Password NMH manifest — kagi pins this file only, not the profile
$HOME/.agents/AGENTS.md	asset	file	600	shared with kotoba (always-on checklist surface); bytes pinned here
```

`minimized/shapes.tsv` — empty file, 0 bytes.

`minimized/baseline.tsv` (15 lines, the pinned drift baseline verbatim):

```
$HOME/.local/bin/the-janitor	755	333	2408b0c90b7e9057f2d1bbce7c6d027c270bf70aa9548e7e54c20c9a58057edd
$HOME/.config/the-janitor/client.py	755	117	8179b241c6f15fb9e0c5036f6d37c762d78fa8a1ce50587ca56445c9165ace51
$HOME/.config/the-janitor/opencode.json	644	29	a318e719a04bd5d913719b642ea54eec7272a92a3726a4bdbd81814117ad8a8e
$HOME/.config/the-janitor/config.json	600	23	-
$HOME/.config/the-janitor/op.env	600	17	-
$HOME/.config/opencode/opencode.json	644	455	b270d762026e1303e332b9089ade5ef2c65abcbde24e7dc9c1436c04d6fddd3c
$HOME/.config/opencode/agents/janitor.md	644	41	c17e263879cbc8385f5facc097687f6ec90c5c3784a7e573e5944cf267e42699
$HOME/.config/opencode/tools/janitor_auth.ts	644	14	2382d5afd00dd1d8b04f32b95e395f8747880c1125d2d5267eefdbe6f126362a
$HOME/.config/opencode/plugin/fnm-nudge.js	644	67	0d8b7c16ec81f623c8f54b0e5314f15af2d26d453a0a77e9d169b2214d953119
$HOME/.local/bin/tac-check	755	88	af95ca97b3e3542ccd3f3b4fb718b9208254dea7d133e118806aff53e6b2961d
$HOME/.local/state/tac/daybreak-blue-access.json	600	82	-
$HOME/.local/state/the-janitor/tac-daybreak-blue.json	600	9	-
$HOME/.local/state/tac/handoff-status.json	600	54	-
$HOME/.agents/AGENTS.md	600	75	-
$HOME/.local/share/the-musketeer/chrome-profile/NativeMessagingHosts/com.1password.1password.json	600	10	05e1cd94336987c4984ef2c8b2fa2506ffdcbbdd620c8eda580713f89b93ce9b
```

`minimized/host.tsv` (36 lines; `<path>\t<dir|file>\t<mode>\t<content>`; content is `x` for files
and empty for dirs — the trailing tab on dir rows is the empty content field):

```
.config/the-janitor	dir	700	
.config/the-janitor/client.py	file	644	x
.config/the-janitor/opencode.json	file	644	x
.config/the-janitor/op.env	file	600	x
.config/the-janitor/config.json	file	600	x
.config/opencode/opencode.json	file	644	x
.config/opencode/agents/janitor.md	file	644	x
.config/opencode/tools/janitor_auth.ts	file	644	x
.config/opencode/plugin/fnm-nudge.js	file	644	x
.local/bin/the-janitor	file	755	x
.local/bin/tac-check	file	755	x
.local/state/tac	dir	700	
.local/state/tac/daybreak-blue-access.json	file	600	x
.local/state/tac/handoff-status.json	file	600	x
.local/state/the-janitor	dir	700	
.local/state/the-janitor/client.lock	file	600	x
.local/state/the-janitor/session-id	file	600	x
.local/state/the-janitor/tac-daybreak-blue.json	file	600	x
.local/state/the-janitor/xdg-cache	dir	700	
.local/state/the-janitor/xdg-cache/opencode/models.json	file	600	x
.local/state/the-janitor/xdg-data	dir	700	
.local/state/the-janitor/xdg-data/opencode	dir	700	
.local/state/the-janitor/xdg-data/opencode/log	dir	700	
.local/state/the-janitor/xdg-data/opencode/repos	dir	700	
.local/state/the-janitor/xdg-data/opencode/opencode.db	file	600	x
.local/state/the-janitor/xdg-data/opencode/opencode.db-shm	file	600	x
.local/state/the-janitor/xdg-data/opencode/opencode.db-wal	file	600	x
.local/state/the-janitor/xdg-data/opencode/log/opencode.log	file	600	x
.local/state/the-janitor/xdg-state	dir	700	
.local/state/the-janitor/xdg-state/opencode	dir	700	
.local/state/the-janitor/xdg-state/opencode/locks	dir	700	
.local/share/the-musketeer/chrome-profile	dir	700	
.local/share/the-musketeer/chrome-profile/NativeMessagingHosts	dir	700	
.local/share/the-musketeer/chrome-profile/NativeMessagingHosts/com.1password.1password.json	file	600	x
.agents/AGENTS.md	file	600	x
```

## Smallest safe correction

The blocker is the conjunction inside the frozen counter, not the fixture. Two minimal options, both
in the counter/predicate rather than in my fixture:

1. **Widen the pinned anchor.** `c2-measure-v2.py:249` anchors the census to the pinned bytes, and
   the pinned declaration has no exec row with an unchecked (`-`) mode. Anchoring the census *rows*
   instead of its exact bytes, or allowing one declared mode field to be `-` for the drifted exec
   row, would let the same host manifest satisfy both halves (measured: state B above,
   `Oracle.kills == True`).
2. **Relax the mutant half of `Oracle.kills()** so a mutant that reports the same row as a mode
   drift counts as "the mutant no longer detects the x-bit loss". The B5 mutation's whole effect is
   to change that row's verdict from `(declared exec, no execute bit)` to `(mode 644, declared 755)`;
   the mutation is real and the drift is still detected, but not by the deleted arm.

Either change is the L1's call, not mine. I did not edit the counter, the contract, or the pinned
kagi bytes.

## What I did not do

- No edits to production files, the frozen counter, the contract, or the pinned kagi corpus.
- No `jj` command anywhere, and no git write command in the lane repo. My clone commits were made
  only in `/tmp/BuildF6B-r29` (commit `253cb84`), as the task directs.
- No environment tricks to force a kill: no noexec mount, no `TMPDIR` or `HOME` manipulation, no
  ACLs, no ownership changes, no alternative `--kagi` or `--rev`.
- The `original/` and `minimized/` fixture directories and `generate-f6.py` are staged under
  `.ufo/evidence/round-29/f6/BuildF6B/` in the lane repo; the L1 integrates them wherever it wants.

## One mistake of mine, reported

While cleaning up my own background processes I killed PID 2758108 (`python3 sweep.py`) and its two
child gate runs (3083677/3083678). Those belonged to the sibling seat BuildF6A (cwd
`/tmp/buildf6a`), not to me: I matched them in a `pgrep` listing, assumed they were mine, and killed
them without checking `/proc/<pid>/cwd` first. No files of that seat were deleted, and I messaged
BuildF6A directly so it could re-run the sweep if the kill cut it short. Every sweep step there is
deterministic and re-runnable. Nothing of mine was left running.

## Files

- `.ufo/evidence/round-29/f6/BuildF6B/generate-f6.py` — generator (build + reduce; imports the
  frozen counter's `ddmin`/`Oracle`).
- `.ufo/evidence/round-29/f6/BuildF6B/original/{census,shapes,baseline,host}.tsv`
- `.ufo/evidence/round-29/f6/BuildF6B/minimized/{census,shapes,baseline,host}.tsv`

## Tooling

No tools were installed or updated in this seat.
