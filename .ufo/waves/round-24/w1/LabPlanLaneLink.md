# LabPlanLaneLink — `registry-replay.py --plan` when the lane directory is a symlink

Item: TameshiR24-2.LabPlanLaneLink · round-24 C1 calibration · pinned revision `c8c5b88c8e961a929cdc351b95a7074c76958909` (`round-24: append fifteen actual traced source reanchors preserving prior ledger`).

## Verdict

**Hypothesis holds.** When the lane directory is itself a symlink, `--plan --json` never lists the lane among its own siblings. Ten of ten lane-is-symlink variants excluded it: relative, absolute, two-hop chain, trailing slash, cwd-relative, a symlink whose name does not match `*-shokunin`, a symlinked fleet plus a symlinked lane, a `..` path after a symlinked fleet, a symlink whose target lies outside the invoking fleet, and a symlink to a physical lane not named `*-shokunin`. A symlinked fleet directory alone (lane real) also excluded it. Exclusion is realpath equality on both sides (`tools/registry-replay.py:67-68`), not a name match.

Caveats, all observed, none a failure of the exclusion itself:

1. **Target outside the invoking fleet (L2).** `fleet_root` and `siblings` describe the target's physical parent, not the invoking fleet. The invoking fleet's peer is dropped, and the sibling relation is one-way.
2. **Missing or dangling lane (L3).** Exclusion is vacuous there, and `--plan` exits 0 on a path that is not a lane. The header documents exit 2 for invalid or unavailable input (`tools/registry-replay.py:27-28`).

Adjacent defect, outside the hypothesis: `siblings` lists the same directory twice when two `*-shokunin` names resolve to one sibling (L4).

## Scope and method

- Under test: `tools/registry-replay.py` `plan()` (lines 63-69) and its `--plan` dispatch (lines 267-272). I ran `--plan --json` only. I did not run `--selftest`, the round-24 ruler, or `--run`.
- Clone: `/tmp/LabPlanLaneLink-r24`, created with `GIT_OPTIONAL_LOCKS=0 git clone -q --no-hardlinks` from the main repo and detached at `c8c5b88`. Confirmed by `git rev-parse HEAD`.
- Fixture: `/tmp/LabPlanLaneLink-fixture`. `realpath(/tmp)` = `/tmp`, so the fixture has no alias skew. Built with `os.symlink`; the layout is below.
- Invocation, every case: `python3 /tmp/LabPlanLaneLink-r24/tools/registry-replay.py --plan --repo <path> --json`, python3 3.14.8 (pre-existing on this host). Every run returned exit 0 and empty stderr.
- Main repo access: read-only only — the clone source, a grep of `tools/`, and listings of `.ufo/waves` and `.ufo/waves/round-24/w1`. This report is the single write.
- Subagent dispatch: none. This seat has no spawn tool, and the direct observation did not need a labrat.
- Tools installed or upgraded: none.

## Code under test

```
63 def plan(repo):
64     """Realpath-normalised lane, fleet root and sibling lanes (no cloning)."""
65     real = os.path.realpath(repo)
66     fleet = os.path.dirname(real)
67     siblings = sorted(os.path.realpath(p) for p in Path(fleet).glob('*-shokunin')
68                       if p.is_dir() and os.path.realpath(p) != real)
69     return {'repo': real, 'fleet_root': fleet, 'siblings': siblings}
```

Coverage gap: `.ufo/evidence/round-24/measure.py:185-200` (K11) and the selftest `plan-realpath` (`tools/registry-replay.py:227-242`) both reach the lane through a symlinked fleet (`alias -> fleet`) while `lane-shokunin` is a real directory. Neither exercises a symlinked lane directory. This probe covers that gap.

## Fixture (`os.walk`; `l` = symlink with target, `d` = directory)

```
L1/alias                  l -> /tmp/LabPlanLaneLink-fixture/L1/fleet
L1/fleet/lane-shokunin    d
L1/fleet/peer-shokunin    d
L1/fleet/lane-abs-shokunin  l -> /tmp/LabPlanLaneLink-fixture/L1/fleet/lane-shokunin
L1/fleet/lane-link-shokunin l -> lane-shokunin
L1/fleet/lane-plain       l -> lane-shokunin
L2/fleet/peer-shokunin    d
L2/fleet/lane-link-shokunin l -> ../store/lane-shokunin
L2/store/lane-shokunin    d
L2/store/other-shokunin   d
L3/fleet/peer-shokunin    d
L3/fleet/lane-dangling-shokunin l -> ../nowhere/lane-shokunin     (../nowhere absent)
L4/fleet/lane-shokunin    d
L4/fleet/peer-shokunin    d
L4/fleet/peer-two-shokunin  l -> peer-shokunin
L5/fleet/lane-shokunin    d
L5/fleet/peer-shokunin    d
L5/fleet/lane-link-shokunin l -> lane-shokunin
L5/fleet/chain-shokunin   l -> lane-link-shokunin
L5/fleet/loop-shokunin    l -> loop-shokunin                       (self-loop)
L6/fleet/lane             d
L6/fleet/peer-shokunin    d
L6/fleet/lane-link-shokunin l -> lane
```

To rebuild by hand: `mkdir -p` each `d` entry, then `ln -s <target> <link>` for each `l` entry, using the printed target verbatim.

## Observed results

`ALL exit=0, stderr empty`. Path prefix is `/tmp/LabPlanLaneLink-fixture/`. "Same" means stdout identical to the family's first row (L1-a for L1-*, L5-a for L5-*): checked programmatically for L1-b to L1-g and L2-b, by inspection for L5-b to L5-d.

| Case | `--repo` (relative to fixture) | `siblings` | lane listed? |
|---|---|---|---|
| L1-a control | `L1/fleet/lane-shokunin` | `[L1/fleet/peer-shokunin]` | no |
| L1-b | `L1/fleet/lane-link-shokunin` (relative symlink) | same (L1-b to L1-g: byte-identical to L1-a, checked programmatically) | no |
| L1-c | `L1/fleet/lane-abs-shokunin` (absolute symlink) | same | no |
| L1-d | `L1/fleet/lane-plain` (not `*-shokunin`) | same | no |
| L1-e | `L1/alias/lane-shokunin` (symlinked fleet) | same | no |
| L1-f | `L1/alias/lane-link-shokunin` | same | no |
| L1-g | `L1/alias/peer-shokunin/../lane-link-shokunin` | same | no |
| L2-a | `L2/fleet/lane-link-shokunin` (target outside fleet) | `[L2/store/other-shokunin]`, `fleet_root` = `L2/store` | no |
| L2-b control | `L2/store/lane-shokunin` | same as L2-a (byte-identical, checked programmatically) | no |
| L2-c control | `L2/fleet/peer-shokunin` | `[L2/store/lane-shokunin]` | n/a |
| L3-a | `L3/fleet/lane-dangling-shokunin` (dangling) | `[]` | vacuous |
| L3-b | `L3/fleet/missing-shokunin` (nonexistent) | `[L3/fleet/peer-shokunin]` | n/a |
| L4-a | `L4/fleet/lane-shokunin` (sibling by second name) | `[peer, peer]` (duplicate) | no |
| L5-a | `L5/fleet/chain-shokunin` (two-hop chain) | `[L5/fleet/peer-shokunin]` | no |
| L5-b | `L5/fleet/lane-link-shokunin/` (trailing slash) | same | no |
| L5-c | `lane-link-shokunin`, cwd = `L5/fleet` (relative) | same | no |
| L5-d | `L5/fleet/lane-shokunin` (direct, self-loop sibling present) | same; loop skipped, no crash | no |
| L6-a | `L6/fleet/lane-link-shokunin` (physical name `lane`) | `[L6/fleet/peer-shokunin]` | no |

Verbatim stdout for the cases that differ from the control:

```
L1-a  {"fleet_root": "/tmp/LabPlanLaneLink-fixture/L1/fleet", "repo": "/tmp/LabPlanLaneLink-fixture/L1/fleet/lane-shokunin", "siblings": ["/tmp/LabPlanLaneLink-fixture/L1/fleet/peer-shokunin"]}
L2-a  {"fleet_root": "/tmp/LabPlanLaneLink-fixture/L2/store", "repo": "/tmp/LabPlanLaneLink-fixture/L2/store/lane-shokunin", "siblings": ["/tmp/LabPlanLaneLink-fixture/L2/store/other-shokunin"]}
L2-c  {"fleet_root": "/tmp/LabPlanLaneLink-fixture/L2/fleet", "repo": "/tmp/LabPlanLaneLink-fixture/L2/fleet/peer-shokunin", "siblings": ["/tmp/LabPlanLaneLink-fixture/L2/store/lane-shokunin"]}
L3-a  {"fleet_root": "/tmp/LabPlanLaneLink-fixture/L3/nowhere", "repo": "/tmp/LabPlanLaneLink-fixture/L3/nowhere/lane-shokunin", "siblings": []}
L3-b  {"fleet_root": "/tmp/LabPlanLaneLink-fixture/L3/fleet", "repo": "/tmp/LabPlanLaneLink-fixture/L3/fleet/missing-shokunin", "siblings": ["/tmp/LabPlanLaneLink-fixture/L3/fleet/peer-shokunin"]}
L4-a  {"fleet_root": "/tmp/LabPlanLaneLink-fixture/L4/fleet", "repo": "/tmp/LabPlanLaneLink-fixture/L4/fleet/lane-shokunin", "siblings": ["/tmp/LabPlanLaneLink-fixture/L4/fleet/peer-shokunin", "/tmp/LabPlanLaneLink-fixture/L4/fleet/peer-shokunin"]}
L5-a  {"fleet_root": "/tmp/LabPlanLaneLink-fixture/L5/fleet", "repo": "/tmp/LabPlanLaneLink-fixture/L5/fleet/lane-shokunin", "siblings": ["/tmp/LabPlanLaneLink-fixture/L5/fleet/peer-shokunin"]}
L6-a  {"fleet_root": "/tmp/LabPlanLaneLink-fixture/L6/fleet", "repo": "/tmp/LabPlanLaneLink-fixture/L6/fleet/lane", "siblings": ["/tmp/LabPlanLaneLink-fixture/L6/fleet/peer-shokunin"]}
```

L5-b, L5-c, and L5-d print the same text as L5-a.

## Analysis

- **Why exclusion holds (observed).** Line 65 resolves the lane. Line 68 compares the realpath of every glob entry against it. Glob entries that resolve to the lane are dropped: `lane-link-shokunin` (L1-b), `lane-abs-shokunin` (L1-c), `chain-shokunin` (L5-a), and the physical `lane-shokunin`. The `repo` field is always the physical path, so consumers cannot recover the alias from the output.
- **Why the realpath comparison matters [INFERENCE, not run as a mutant].** In L1-b and L1-c the physical `lane-shokunin` is also a glob entry. Comparing against the typed `--repo` string would fail to drop it and would list the lane.
- **Outside-fleet identity (L2, observed).** `fleet_root = dirname(realpath)` (line 66). L2-a and L2-b are byte-identical, so the documented invariant holds: a symlinked alias does not change identity (`corpus/knowledge/replay-projection-hardening.md:20`). The cost is that a lane's fleet is its physical location. From the lane (L2-a) the peer is absent. From the peer (L2-c) the lane appears as a sibling at its physical path. I found no document that settles which relation is intended.
- **Replay consequence [INFERENCE, not run].** `run_replay` mirrors `layout['siblings']` into the clone's fleet (lines 160-161). For L2-a that mirror contains only the target's siblings, not the invoking fleet's peers.

## Adjacent findings (observed unless marked)

- **A1 — duplicate siblings (L4-a, observed).** `siblings` is not deduplicated (line 67). [INFERENCE, not run] `run_replay` line 161 then calls `symlink_to` twice on `peer-shokunin`, raising `FileExistsError`. That is an unhandled exception, which exits 1, the same code the docstring assigns to "refused".
- **A2 — missing lane accepted (L3-a, L3-b, observed).** `--plan` exits 0 and prints a plan for a path that is not a directory. The header assigns exit 2 to invalid or unavailable input (`tools/registry-replay.py:27-28`). [INFERENCE, not run] `run_replay` line 135 (`git -C <path> rev-parse ... check=True`) would raise `CalledProcessError`, an unhandled exit 1.
- **A3 — physical lane name not checked (L6-a, observed).** The `*-shokunin` suffix filters siblings only. The lane itself may have any name. I found no document stating whether that is intended.

## Not tested / limits

- Retargeting a symlink between `realpath` and `glob` (TOCTOU) — not testable deterministically here.
- The live fleet at `/home/vgpnk/Projects/shokunin` — not inspected for second-name symlinks, so the live exposure of A1 is unknown. The target asked for commands to run only in the clone.
- `--selftest`, the round-24 ruler, `--run` — not executed (outside the item's `--plan --json` scope).
- Case-insensitive filesystems, bind mounts, and a symlink whose target is an ancestor or descendant of the fleet — not tested.

## Smallest safe correction (for the integrator; not applied — production file outside my write scope)

1. `tools/registry-replay.py:67` — wrap the generator in a set: `sorted({os.path.realpath(p) for p in ...})`. Add a selftest case with `peer-two-shokunin -> peer-shokunin` expecting one entry (fixes A1).
2. `tools/registry-replay.py` `--plan` branch (lines 267-272) — before printing, refuse when `not os.path.isdir(os.path.realpath(a.repo))` with exit 2 and a stderr line, matching the header (fixes A2). Add selftest cases for a missing path and a dangling symlink.
3. Document the outside-fleet semantics (L2) in the `plan()` docstring and in `corpus/knowledge/replay-projection-hardening.md`, and pin them with a selftest. Switching to the invoking path would break alias independence (L2-a ≠ L2-b).
4. Add a symlinked-lane-directory case (L1-b equivalent) to the ruler or selftest. K11 and `plan-realpath` do not exercise it. Ruler edits belong to the integrator.

## Checks for the main agent (not run by me)

- After any change, run `python3 tools/registry-replay.py --selftest` and the round-24 ruler in a fresh `/tmp` clone, not in the main repo.
- Rebuild this fixture from the tree above and rerun the 18 `--plan --json` invocations. Expected output matches the table.

## Non-claims

No producer authentication, promotion, historical R17-CMD-BIND closure, or numeric score uplift is claimed. Direct observations are labelled as observed; code-derived consequences are marked [INFERENCE].
