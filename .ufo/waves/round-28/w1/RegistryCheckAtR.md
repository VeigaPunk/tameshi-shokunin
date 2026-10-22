# Registry no-harm at the landed head — executor report (registry-check at base and head)

Seat `TameshiR28.RegistryCheckAtR`, routed item 2 of
`corpus/lessons/round-27-verifier-spotcheck.md` ("Registry no-harm at the landed
head: commit a full `registry-check.py` run at the head from a fleet mirror").
Axes: operability. I wrote none of the content under test and read no private
author tree.

## Verdict

**No harm. The runnable registry holds at the landed head, row for row, exactly
as at the base.**

| Rev | Command | Summary line | Exit |
|---|---|---|---|
| `b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a` (head) | `python3 tools/registry-check.py --rev b05d2ee…` from a fleet mirror | `REGISTRY_CHECK: held=49/49 superseded=7` | **0** |
| `06b59b93697c9b0a8795ac2d0fe3d0bd7e18572c` (base) | same, `--rev 06b59b93…` | `REGISTRY_CHECK: held=49/49 superseded=7` | **0** |

The two stdouts are byte-identical (`md5sum` `cc1d8d292d5fea28d35ac41f4ae52046`
for both, 2934 bytes, 57 lines, empty stderr on both). **Zero active rows
differ.** No row changes state between base and head.

That is the intended result, and the reason is checkable, not assumed:
`tools/registry.json` is byte-identical at base, at the round-27 receipt rev
`2227d83`, and at the head (`sha256 c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c`
in all three), and `git diff 06b59b93 b05d2ee -- tools/ .ufo/evidence/` is empty
apart from three new `round-28/` evidence files. The head's 18 added SKILL.md
lines and the SOURCES.md edit move no runnable row.

Also not a new fact about the rows: the head output is byte-identical to the
already-committed round-27 receipt `.ufo/evidence/round-27/after/registry-2227d83.stderr`
(`diff` empty). What the head run adds is that this holds **after** the SKILL
registry-row edits in `b1cc95e` / `af7b70d` / `b05d2ee` — the specific thing
round-27 routed item 2 asked to close.

## Scope boundary the verdict depends on (read this before quoting "49/49")

`registry-check.py` grades the **command surface** in `tools/registry.json`. It
does not read `SKILL.md`: no row's `argv` and no row's `stdout_contains`
needle names `SKILL.md` (checked by parsing `tools/registry.json`). So this
receipt proves the 49 registered entry commands still return their registered
outcomes; it **cannot** and does not prove the correctness of any SKILL.md
registry-table prose cell. Round-27's wording ("SKILL registry rows … were
edited later") mixed the two surfaces; the tools/rows surface is what
`registry-check.py` can speak to, and on that surface there is nothing to
repair.

## Fleet mirror — required, and shown to be load-bearing

Setup (verbatim, my scratch `W=/tmp/RegistryCheckAtR-vBgS`):

```bash
W=$(mktemp -d /tmp/RegistryCheckAtR-XXXX); mkdir $W/fleet
for d in /home/vgpnk/Projects/shokunin/*-shokunin; do b=$(basename $d)
  [ $b = tameshi-shokunin ] || ln -s $d $W/fleet/$b; done
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin
git -C $W/fleet/tameshi-shokunin checkout -q --detach b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a
R=$W/fleet/tameshi-shokunin
cd $R && python3 tools/registry-check.py --rev b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a
```

`--rev` made the tool build its own nested mirror (`/tmp/tameshi-registry-check-*/fleet/tameshi-shokunin`,
21 sibling entries) whose siblings resolve through my mirror to the live lanes.
Both runs: head 326.98 s, base 311.40 s wall.

Negative control that the mirror is not decoration — same head rev, a clone
seated alone in a directory with no `*-shokunin` siblings:

```
ROW mutate-and-run-regression expect=0 got=2 differs
ROW round21-measure-selftest expect=0 got=1 differs
ROW mte-interop-check expect=0 got=2 differs
```

Exactly the three rows the round-27 no-mirror receipt
(`.ufo/evidence/round-27/after/registry-2227d83-no-mirror.stderr`, 46/49)
reported. These three are the rows that read live sibling object stores, so
"49/49" is a statement about the fleet with its siblings present, never about
the lane in isolation. Consistent with `SKILL.md:1932` and the round-24
correction at `SKILL.md:2074-2075`, which already declare those two rows live.

## Rows that are not held

Active rows: **none**. All 49 active rows returned `held` at both revs.

Superseded rows (7) are excluded from `N/M` by the contract but still execute.
Four meet their recorded expectation; three do not, identically at both revs:

| Row | Recorded expect | Observed exit |
|---|---|---|
| `evidence-disposition-round17` | 0 | 2 |
| `evidence-disposition-round17-before` | 1 | 2 |
| `evidence-disposition-round14-superseded` | 0 | 2 |

Why, measured directly (`python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions.json --json`
and the round-14 counterpart, both in the clone):

```
"kind": "expected_input_digest_mismatch"
"message": "tools/bash-witness-study.py: observed 60575e62a5301bd31c8c84a4039af69fe8f845abf035b8d072975cd9ef685be9
            expects 49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80"
```

`tools/bash-witness-study.py` moved by design at `370f2df` (round 21, an
ancestor of the base). The round-17 and round-14 manifests pin only
`tools/mutate-and-run.sh` and `tools/pin-disposition.py` in `historical_inputs`;
only the round-18 manifest adds `tools/bash-witness-study.py`, which is why the
active `evidence-disposition-round18` row exits 0 and holds. So this is the
documented, intended superseded state — `SKILL.md:1601` already reads "round
17's now exits 2, bash-witness moved" — not drift, and not a round-28
regression (identical at base and head).

## Full stdout — head `b05d2ee8e7f80b18428e8f38b9ad535cf9d99a1a` (exit 0)

```
ROW repeat-control-snapshot-clean expect=0 got=0 held
ROW repeat-control-snapshot-mismatch expect=1 got=1 held
ROW repeat-control-selftest expect=0 got=0 held
ROW bash-witness-count expect=0 got=0 held
ROW bash-witness-selftest expect=0 got=0 held
ROW pin-disposition-read expect=0 got=0 held
ROW pin-disposition-selftest expect=0 got=0 held
ROW witness-metadata-check expect=0 got=0 held
ROW witness-metadata-selftest expect=0 got=0 held
ROW evidence-disposition-round17 superseded expect=0 got=2
ROW evidence-disposition-round17-before superseded expect=1 got=2
ROW evidence-disposition-round18 expect=0 got=0 held
ROW evidence-disposition-round18-before expect=1 got=1 held
ROW evidence-disposition-round14-superseded superseded expect=0 got=2
ROW evidence-disposition-selftest expect=0 got=0 held
ROW context-capture-frozen expect=0 got=0 held
ROW context-capture-missing-env expect=1 got=1 held
ROW context-capture-mapping-suffix expect=1 got=1 held
ROW context-capture-selftest expect=0 got=0 held
ROW mutate-and-run-selftest expect=0 got=0 held
ROW mutate-and-run-regression expect=0 got=0 held
ROW measure-round16-rev expect=0 got=0 held
ROW measure-round16-selftest expect=0 got=0 held
ROW assemble-round16-selftest expect=0 got=0 held
ROW reattribute-round16-selftest expect=0 got=0 held
ROW sources-census expect=0 got=0 held
ROW verify-round15 expect=0 got=0 held
ROW registry-check-selftest expect=0 got=0 held
ROW measure-round17-selftest expect=0 got=0 held
ROW trace-inputs-round17-selftest superseded expect=0 got=0
ROW assemble-round17-selftest expect=0 got=0 held
ROW trace-inputs-selftest expect=0 got=0 held
ROW measure-round18-selftest expect=0 got=0 held
ROW assemble-round18-selftest expect=0 got=0 held
ROW defect-probes-selftest expect=0 got=0 held
ROW round19-correction-ruler-selftest expect=0 got=0 held
ROW round19-coldread-selector-selftest expect=0 got=0 held
ROW receipt-window-selftest expect=0 got=0 held
ROW receipt-measure-selftest expect=0 got=0 held
ROW round20-coldread-selector-selftest expect=0 got=0 held
ROW env-diff-selftest expect=0 got=0 held
ROW wave-route-mix-selftest expect=0 got=0 held
ROW round21-measure-selftest expect=0 got=0 held
ROW round21-coldread-selector-selftest expect=0 got=0 held
ROW wave-accounting-frozen-entry expect=0 got=0 held
ROW wave-accounting-selftest expect=0 got=0 held
ROW wave-accounting-wrong-count-entry expect=1 got=1 held
ROW command-binding-selftest superseded expect=0 got=0
ROW command-binding-frozen-clean superseded expect=0 got=0
ROW command-binding-source-read-red superseded expect=1 got=1
ROW command-binding-selftest-r24 expect=0 got=0 held
ROW command-binding-frozen-clean-pinned expect=0 got=0 held
ROW command-binding-source-read-red-pinned expect=1 got=1 held
ROW registry-replay-selftest expect=0 got=0 held
ROW mte-interop-selftest expect=0 got=0 held
ROW mte-interop-check expect=0 got=0 held
REGISTRY_CHECK: held=49/49 superseded=7
```

stderr: empty.

## Full stdout — base `06b59b93697c9b0a8795ac2d0fe3d0bd7e18572c` (exit 0)

```
ROW repeat-control-snapshot-clean expect=0 got=0 held
ROW repeat-control-snapshot-mismatch expect=1 got=1 held
ROW repeat-control-selftest expect=0 got=0 held
ROW bash-witness-count expect=0 got=0 held
ROW bash-witness-selftest expect=0 got=0 held
ROW pin-disposition-read expect=0 got=0 held
ROW pin-disposition-selftest expect=0 got=0 held
ROW witness-metadata-check expect=0 got=0 held
ROW witness-metadata-selftest expect=0 got=0 held
ROW evidence-disposition-round17 superseded expect=0 got=2
ROW evidence-disposition-round17-before superseded expect=1 got=2
ROW evidence-disposition-round18 expect=0 got=0 held
ROW evidence-disposition-round18-before expect=1 got=1 held
ROW evidence-disposition-round14-superseded superseded expect=0 got=2
ROW evidence-disposition-selftest expect=0 got=0 held
ROW context-capture-frozen expect=0 got=0 held
ROW context-capture-missing-env expect=1 got=1 held
ROW context-capture-mapping-suffix expect=1 got=1 held
ROW context-capture-selftest expect=0 got=0 held
ROW mutate-and-run-selftest expect=0 got=0 held
ROW mutate-and-run-regression expect=0 got=0 held
ROW measure-round16-rev expect=0 got=0 held
ROW measure-round16-selftest expect=0 got=0 held
ROW assemble-round16-selftest expect=0 got=0 held
ROW reattribute-round16-selftest expect=0 got=0 held
ROW sources-census expect=0 got=0 held
ROW verify-round15 expect=0 got=0 held
ROW registry-check-selftest expect=0 got=0 held
ROW measure-round17-selftest expect=0 got=0 held
ROW trace-inputs-round17-selftest superseded expect=0 got=0
ROW assemble-round17-selftest expect=0 got=0 held
ROW trace-inputs-selftest expect=0 got=0 held
ROW measure-round18-selftest expect=0 got=0 held
ROW assemble-round18-selftest expect=0 got=0 held
ROW defect-probes-selftest expect=0 got=0 held
ROW round19-correction-ruler-selftest expect=0 got=0 held
ROW round19-coldread-selector-selftest expect=0 got=0 held
ROW receipt-window-selftest expect=0 got=0 held
ROW receipt-measure-selftest expect=0 got=0 held
ROW round20-coldread-selector-selftest expect=0 got=0 held
ROW env-diff-selftest expect=0 got=0 held
ROW wave-route-mix-selftest expect=0 got=0 held
ROW round21-measure-selftest expect=0 got=0 held
ROW round21-coldread-selector-selftest expect=0 got=0 held
ROW wave-accounting-frozen-entry expect=0 got=0 held
ROW wave-accounting-selftest expect=0 got=0 held
ROW wave-accounting-wrong-count-entry expect=1 got=1 held
ROW command-binding-selftest superseded expect=0 got=0
ROW command-binding-frozen-clean superseded expect=0 got=0
ROW command-binding-source-read-red superseded expect=1 got=1
ROW command-binding-selftest-r24 expect=0 got=0 held
ROW command-binding-frozen-clean-pinned expect=0 got=0 held
ROW command-binding-source-read-red-pinned expect=1 got=1 held
ROW registry-replay-selftest expect=0 got=0 held
ROW mte-interop-selftest expect=0 got=0 held
ROW mte-interop-check expect=0 got=0 held
REGISTRY_CHECK: held=49/49 superseded=7
```

stderr: empty.

## Row-by-row comparison

Alignment: the two stdouts are line-aligned by construction (same 56 row names
in the same order at both revs, from the same registry file), and `diff -u
base.stdout head.stdout` prints nothing. Rows whose result differs: **none**.
Consequently no "why" is owed; the nearest thing to a difference is wall time
(head 326.98 s, base 311.40 s, both dominated by
`mutate-and-run-regression` and `mte-interop-check`).

Two corroborating single-row probes, run separately rather than inferred, also
came out equal at both revs: `--only sources-census` → `held=1/1`, and the
census script run directly in the clone at both revs produced identical output
(`diff` empty, exit 0 both).

## Smallest safe correction

**None needed in the lane.** The routed item's deliverable is a full run at the
head from a fleet mirror; it is above, exit 0, and it is the only artifact this
seat produced.

For the integrator, two things this report does not do and one it suggests:

1. The receipt is **not committed** by me — bounds forbid it. The exact stdout
   above is what would go to something like
   `.ufo/evidence/round-28/after/registry-b05d2ee.stdout` if the round wants a
   retained receipt; the round-27 pair
   (`registry-2227d83.json` / `.stderr`) is the format precedent. Note that a
   `--json` run was not taken; add `--json` if the round wants the structured
   form, at the cost of a second ~5.5 min run.
2. `verify-round15` carries `external: true` and an absolute `--rev` argument,
   and `pin-disposition-read` carries the absolute live-fleet path
   `--root /home/vgpnk/Projects/shokunin`. The `non_hermetic_argv` guard fires
   for the second only when the grading root sits in the live fleet: measured
   `non_hermetic_argv: ['/home/vgpnk/Projects/shokunin']` with
   `--root /home/vgpnk/Projects/shokunin/tameshi-shokunin`, and `None` from my
   mirror clone (`fleet_root` = `/tmp/.../fleet`, so the live path is outside
   it). Both still hold, because both declarants set `external: true`; worth
   knowing that the mirror shape weakens that particular guard's observation
   without changing any row's verdict.
3. No registry row reads `SKILL.md`, so if a future round wants prose-cell
   drift caught mechanically rather than by a cold read, that is a new row,
   not a repair of this one. Naming it as an observation only — out of scope
   here, and I am not proposing a change.

## Environment / tooling

Nothing installed: no pacman, no `uv tool install`, no release binary. Present
and used as-is — Python 3.14.8, git 2.56.0, uv 0.13.0 (the
`mte-interop-check` row runs `uv run --no-project --with jsonschema==4.25.1`;
it resolved from the warm `~/.cache/uv` and held). All runs read-only with
`GIT_OPTIONAL_LOCKS=0`; no `jj` command was run anywhere; no git write command
was run in the lane. Scratch: `/tmp/RegistryCheckAtR-vBgS/`
(`head.stdout`, `base.stdout`, `head.exit`, `base.exit`, `nomirror/` control).
The lane's live working tree was left untouched — its one dirty file
(`corpus/lessons/round-28.md`, another seat's edit) already differed before my
first command and I never wrote to it.
