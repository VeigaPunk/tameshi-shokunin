# RevLiveRows — which replay rows actually read live fleet paths (round-24 C1)

Lane: TameshiR24-2.RevLiveRows (revenger, leaf — no subagents, read-only except this file).
Replay audited: `.ufo/evidence/round-24/replay/` (43 rows, rev `d2eaecd443bf5f4e387e7e5331282e3d11dea047`, ran 2026-10-21T15:56:41Z–16:01:02Z per `../replay-command.json`).

## Axes (godspeed)

- **A1 classification fidelity** — `live_dependent` vs live reads derivable from the executed sources.
- **A2 evidence grounding** — every claim carries `path:line` or a command with observed output.
- **A3 correction blast radius** — smallest safe change that removes the divergence.

## Verdict

1. **The two reported `live_dependent` rows are correct** — both genuinely read live fleet paths, each through a different detection channel. No over-classification found.
2. **The list is incomplete: `round21-measure-selftest` also reads live fleet paths but is classified `revision_pinned` (external:false).** Its selftest resolves 8 of 9 frozen surface pins by running `git -C <clone>/../<sibling-repo> show <pinned-rev>:<path>` against the **live sibling repositories** reached through the replay's fleet-mirror symlinks. Concrete counterexample below: the kagi surface pin resolved at replay time and is **gone from the live sibling now**, so an identical rerun today crashes this "revision-pinned" row. `live_dependent.json` therefore under-reports by one row.
3. Boundary note (no reclassification): the round-17/18 `measure.py`/`assemble.py` selftests `os.path.realpath()` live-lane paths recorded in committed fixtures — metadata (lstat) contact only; all content comparisons run against fixture/clone rev blobs.

Fresh falsification result: **1 defect found** (item 2), with a reproducible-in-principle failure mode; items checked and clean are listed under "Checked, no defect".

## Evidence

### Classification mechanism (both channels)

- `tools/registry-replay.py:99-100` — a row is `live_dependent` iff `row.external is True` **or** the runner reported `non_hermetic_argv`; everyone else is counted `revision_pinned` (`:103-108`).
- `tools/registry-check.py:632-645` `_argv_outside_fleet` — the runner only inspects **literal argv tokens** for absolute paths under the live fleet root; `:648-671` `run_row` refuses undeclared non-hermetic rows and otherwise runs them with `cwd=clone`.
- `tools/registry-replay.py:152-161` — the private clone is `<tmp>/fleet/tameshi-shokunin`, and every sibling lane becomes a **symlink to the live sibling repo**: `(fleet / os.path.basename(sibling)).symlink_to(sibling, ...)`. Consequence: any row that traverses `../<sibling>` from the clone silently reaches live fleet state — invisible to the argv-only detector.

### Row 1 — `pin-disposition-read`: live-dependent, correctly flagged (both channels)

- Argv (`observations.json`): `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin`; runner flagged `non_hermetic: ["/home/vgpnk/Projects/shokunin"]`, registry `external:true` (`.ufo/evidence/round-23/registry-baseline.json`, one of exactly two `external:true` rows).
- Source: `tools/pin-disposition.py` — `run_mode` (`:667-670`) takes the live fleet root; `repo_identity` (`:245-275`) and `git_run` (`:224-242`) run read-only git (`rev-parse`, `cat-file`, `symbolic-ref`, `show-ref`) **inside live sibling repos**; `head_observation` (`:374-450`) resolves the live branch tip and hashes blobs at it; `worktree_observation` (`:453-505`) opens live worktree files (lstat + O_NOFOLLOW). The manifest itself resolves against cwd = clone (pinned bytes).
- Verdict: genuinely live; external flag and runner flag both justified.

### Row 2 — `verify-round15`: live-dependent, correctly flagged (registry channel only)

- Argv is clean (`python3 .ufo/evidence/round-15/verify.py --rev 7650fe4…`), so the runner's argv detector is silent; `external:true` in the registry is the sole flag.
- Source: `.ufo/evidence/round-15/verify.py` — `ROOT = Path(__file__).resolve().parents[3]` (`:89`) = the clone; all `git()` calls are `git -C ROOT` (`:130-137`), i.e. clone history at pinned revs; receipts/frozen inputs are written under clone `EVIDENCE` or `SCRATCH` temp (`:473-495`, `:524-529`); `gate-frozen-builtin` runs the clone's `tools/context-capture.py` (`:655-663`), and `measure-before/after` run the clone's `round-15/measure.py` verified byte-equal to the rev blob (`:793-806`).
- The single live channel: `CENSUS_TOOL = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"` (`:105`) executed at `:835-837` as `[CENSUS_TOOL, "validate", "--root", "/home/vgpnk/Projects/shokunin", "tameshi"]` — a fleet-root script **outside the lane repo**, reading the live fleet. This is exactly what `external` must cover.
- Verdict: genuinely live; flag justified, detection only possible via the registry declaration.

### Row 3 — DEFECT: `round21-measure-selftest` reads live sibling repos, classified pinned

- Classification: `external:false`, `non_hermetic:null` in `observations.json`; counted in `revision_pinned: 41`.
- Source: `tools/round21-measure.py` — `ROOT = Path(__file__).resolve().parents[1]` (`:24`) = the clone lane; in `selftest()` (`:28-146`), for every surface of the frozen contract `.ufo/evidence/round-21/c2-contract.json`:

  ```python
  data = subprocess.run(["git", "-C", str(ROOT.parent / surface["repo"]),
                         "show", surface["rev"] + ":" + surface["path"]],
                        env=env, capture_output=True, check=True).stdout   # :73-77
  ```

  `ROOT.parent` = `<tmp>/fleet` (registry-replay.py:152), so `ROOT.parent / "kagi-shokunin"` (etc.) is the **symlink to the live sibling repo** (`registry-replay.py:160-161`). `check=True` with no error handling: any missing live object crashes the selftest with a traceback. Only the first surface (`repo: "tameshi-shokunin"`) resolves inside the clone; the other 8 (kumitate ×3, kagi ×2, tsukuroi, mado) are live-sibling object-store reads of pinned revs.
- Observed at replay time (16:01Z): row held, `ROUND21_MEASURE_SELFTEST: 13/13 pass` (`observations.json`, row `round21-measure-selftest`; bundle receipt exit 0, cwd `/tmp/tameshi-registry-replay-dzo3ypiq/fleet/tameshi-shokunin`). The 9 surface reads happen **before** any check prints (`:69-83` precedes the first `invoke()`), so 13/13 PASS proves all 8 live-sibling reads succeeded then.
- Observed now (post-replay): the kagi surface pin no longer exists in the live sibling —

  ```
  $ git -C /home/vgpnk/Projects/shokunin/kagi-shokunin cat-file -t feece8743e52eb8fb5fbb40782934cb619a1a96e
  fatal: git cat-file: could not get object info
  $ git -C /home/vgpnk/Projects/shokunin/kagi-shokunin cat-file -t feece8743…:corpus/surface-census.sh
  fatal: path 'corpus/surface-census.sh' exists on disk, but not in 'feece8743…'
  ```

  while the sibling pins that still resolve do (`kumitate 175de6ba/0acb7752/364f1d59`, `tsukuroi 165307fe`, `mado eead56b2` → all `blob`; `0acb7752:scripts/sources-check.mjs` hashes to `6a293a72800123a2…`, matching the contract's declared `blob_sha256`).
- kagi lane timeline: reflog shows `export from jj` at 13:29:03 -0300 (= 16:29:03 UTC), **after** the replay ended (16:01:02Z); the pinned commit object `feece8743…` is now unreachable entirely.
- Conclusion: a row counted as `revision_pinned` whose heldness depends on live sibling repos retaining pinned historical objects — precisely the `live_dependent` condition, missed because neither detector sees it (argv is relative; registry row not marked `external`). This is a concrete counterexample to "`live_dependent` == rows actually reading live fleet paths".

### Boundary — metadata-only live contact in round-17/18 selftests (no reclassification)

- `.ufo/evidence/round-17/measure.py:355-365, 430-448`; `.ufo/evidence/round-18/measure.py:359-370, 437-446`; `round-17/coldread/assemble.py:569-583`; `round-18/coldread/assemble.py:569-583` — `under_live_lane`/`live_read_bound` call `os.path.realpath(path)` on fixture-recorded live paths (e.g. `/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md`, `…/.git/HEAD`): lstat metadata on live paths, then **`.git/` prefixes are accepted without any read**, and everything else is compared to `ls_tree_mode`/`cat_file_blob` of the **fixture/clone repo at rev** — no live bytes are read. Not live-dependent under a content-read definition; noted as the only other live contact among pinned rows.

### Checked, no defect (remaining 39 pinned rows)

- Argv sweep of all 43 rows (`observations.json`): no `..` traversal, no absolute fleet paths except `pin-disposition-read`.
- `tools/*.py`, `tools/*.sh`, `.ufo/evidence/**/*.py|sh` grep for `/home/vgpnk/Projects/shokunin`: only trace-inputs (argparse defaults unused in selftest — `tools/trace-inputs.py:702-775` builds everything under a mkdtemp), round-19 measure (live-lane strings are recorded receipt data, never executed — `round-19/measure.py:81-90, 215-218, 265-286`; its only subprocess is `sys.executable __file__` on temp fixtures `:384`), round-17/18 (above), and non-row evidence scripts (`round-12/ExitReview/cases/run-cases.sh`, round-16/18 survivor-probe shells, `round-23/final-measure.py`, `round-21/c1-survivors.py|c2-count.py` — none is an active row entrypoint).
- `sources-census` row: `.ufo/evidence/kaika-round-1/sources-census-v2.sh` operates on `corpus/SOURCES.md` and mined used-by paths relative to cwd = clone; `corpus/SOURCES.md` contains no `/home/…` or `../` tokens (grep: no matches). Pinned.
- Coldread/round19-20-21 selftests invoke wrappers with `--repo <temp fixture>` (`round-19/coldread/measure.py:59-63`, round-20 `:67-71`, round-21 `:67-71`) — hermetic.
- All audited sources are byte-identical between the live tree and the replay rev (`git show d2eaecd…:<path> | sha256sum` vs `sha256sum <path>` → SAME for all 24 audited files, with `GIT_OPTIONAL_LOCKS=0`, read-only).

## Smallest safe correction

1. Registry (`.ufo/evidence/round-23/registry-baseline.json` → successor registry): mark `round21-measure-selftest` `external: true` with a note ("selftest resolves sibling surface pins from the live fleet mirror; kagi pin feece8743… already unresolvable post-2026-10-21T16:29Z jj export"). `registry-replay.py:99-100` then projects it into `live_dependent` with no instrument change; the row will legitimately report the live read instead of silently passing/failing on sibling state.
2. (Optional, deeper) Make the selftest hermetic instead: seed the fixture fleet with the 8 pinned blobs from the contract (they are already recorded as `blob_sha256` in `c2-contract.json`) rather than reading sibling object stores; or have `registry-replay.py` clone siblings at pinned revs instead of symlinking them live. Either removes the live read; both are larger changes than (1).
3. No instrument change required for rows 1–2; their flags match their sources.

Bounds compliance: read-only inspection only; no commands executed in the lane beyond read-only git with `GIT_OPTIONAL_LOCKS=0`; no tool installs (tooling directive: nothing installed this session); only this report file written.
