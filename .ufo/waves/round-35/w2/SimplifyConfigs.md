# Round-35 w2 — SimplifyConfigs

Seat: `tameshi-r35-w2-SimplifyConfigs` (leaf simplifier, godspeed). Lane pin at dispatch:
`7da6e076c2e25936a3b60dde2a4080d8f05b7e5b` (between A5-fix `23bd903a` and A6 `f9df5898`;
A6 already landed at tip `68f25573` — see HYGIENE-2). Scratch:
`/fast/scratch/hyaku/tameshi-r35-seats/SimplifyConfigs/` (clone read-only, no git mutations;
the only lane-path write is this report). No installs (pacman untouched).

Slice: measure which of the four `(auto,KEEP)` configs each public specimen actually needs —
a copy × config divergence matrix under the counter's own behavior oracle — then answer
whether TWO configs could suffice under full-stdout comparison and what that would lose.

Frozen bytes (clone-verified sha256 at the pin): runner `tools/mutate-and-run.sh`
`a7d3f2dd…912eb9`; tool `tools/tally-audit-v3.py` `ef98fc53…5885`; counter
`.ufo/evidence/round-35/c1/c1-measure.py` `515b0b1b…f9cc`; c2 counter `67bb7118…f9cc`.
All match the contract pins. Panel = 8 committed JSONs (5 kill + 3 accept,
`pub_distinct=8` — verified via `distinct_bodies`).

## Method

The counter's oracle is imported read-only (`c1-measure.py`: `tally_block` → `leg_names` →
`run_block` over `CONFIGS = ((None,'1','0'), (None,'1','1'), ('tally-audit','0','1'),
('tally-audit-explicit','0','0'))`, `None` = a real `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`
per A4, 267 vectors per config, compared tuple = (exit, FULL stdout)). For each panel copy,
edits are applied to the pinned runner and `diverge(pristine, copy)` computed. Two scripts:
`matrix.py` (sha256 `60261e00…30cb`, also runs the real frozen tool per copy) and
`demos.py` (`d924f93b…154b`, adds first-line-vs-full-stdout comparison and three synthetic
mutants). Commands:

```
timeout 3000 python3 matrix.py        # exit 0 — 8/8 counter_pass=true
timeout  900 python3 demos.py         # exit 0
timeout  600 python3 vec_counts.py    # exit 0 — per-config divergent-vector counts
python3 lane/tools/tally-audit-v3.py --runner demo{A,B,C}.sh
```

## Measured matrix — public panel (copy × config → divergent; N/267 = divergent vectors)

| copy | set | (1,0) REAL-AUTO | (1,1) REAL-AUTO | (0,1) `tally-audit` | (0,0) `tally-audit-explicit` | tool rc / failed checks |
|---|---|---|---|---|---|---|
| cfg00-accept-swap | kill | — | — | — | **YES** (6/267, first @vec2 `st0=1`: FAIL→SETUP counted=8) | 1 / runtime |
| cfg11-pass-mask | kill | — | **YES** (265/267) | — | — | 1 / runtime |
| workdir-branch-swap | kill | **YES** (1/267*, all-zero vec) | — | — | **YES** (1/267*) | 1 / runtime |
| root-keyed-auto-mask | kill | **YES** (267/267) | **YES** (267/267) | — | — | 1 / runtime |
| root-keyed-auto-zero | kill | **YES** (6/267) | **YES** (6/267) | — | — | 1 / runtime |
| comment-brace | accept | — | — | — | — | 0 / — |
| comment-esac | accept | — | — | — | — | 0 / — |
| comment-names-leg | accept | — | — | — | — | 0 / — |

*indices [0,1] are both the all-zero vector — `vectors_for` emits it twice (minor hygiene,
noted, does not affect validity).

All three accepts are identical under every config and vector; the real tool accepts them.
All five kills are killed by `runtime` alone (rc=1, `failed=['runtime']` — the contract's
kill shape). The panel is self-consistent under the post-A4 oracle: 8/8 `pass=true`.

**First-line-only comparison** (v2 semantics, measured on the same tuples):
`workdir-branch-swap` diverges NOWHERE (its only divergence is the REGRESSION_WORKDIR line —
kept-vs-removed wording, exit stays 0). Under first-line+rc it would be an invalid kill.
Full-stdout is load-bearing for that specimen.

## Could two configs suffice?

**For this exact panel, exactly one 2-subset suffices: {(0,0),(1,1)}.** cfg00-accept-swap
requires (0,0) and cfg11-pass-mask requires (1,1) — each diverges under its config and
NOWHERE else — and the anti-diagonal happens to cover the remaining three kills
(workdir-branch-swap also under (0,0); both root-keyed copies also under (1,1)). No single
config covers all five (best single = (1,0): 3/5).

But that coverage is a coincidence of this panel, and what it loses is the substance:

- **The class requiring (0,0):** `cfg00-accept-swap` — an accept-side swap gated on
  `auto=0 && KEEP=0` (`explicit --workdir DIR` without `--keep`). This is exactly
  Mutkillvectorarmswap F3, the one r34 accept-side hole that was not fail-closed.
- **The class requiring (1,1):** `cfg11-pass-mask` — a `npass` reset gated on
  `auto=1 && KEEP=1` (`--regression --keep`, the keep mode the runner's own line
  "(removed on PASS; --keep retains)" advertises).
- **Dropping (1,0) drops the runner's DEFAULT config** (`--regression` with no flags —
  the only mode that rm's the workdir, and the mode every real kill-rate figure comes
  from). Proof: DEMO-A, one line `if [[ $auto -eq 1 && $KEEP -eq 0 ]]; then nfail=0; fi`
  inserted before the FAIL guard (sha256 `a21f7e8a…fad89`), diverges ONLY under (1,0)
  (oracle: `cfg(1,0) @vec2`, FAIL→SETUP counted=8). A {(0,0),(1,1)} sweep ACCEPTS it while
  the live tool kills it via cfg(1,0): `TALLY_AUDIT: FAIL … runtime=fail`, exit 1.
- **Dropping (0,1) drops the hermetic explicit+keep config.** Proof: DEMO-B
  (`auto=0 && KEEP=1` gate, sha256 `b6a98b36…3a14e`), divergent ONLY under (0,1);
  the 4-config tool kills it via cfg(0,1), exit 1 — invisible to {(0,0),(1,1)}.
- Dropping (0,1) and (1,0) also destroys all redundancy: each remaining kill becomes
  single-config-visible, and (1,1) becomes the only config exercising the real auto root
  (`/tmp/tameshi-r4-2-regression.*`) — the A4 witness would survive only there.
- Note the old v2 diagonal {(0,1),(1,0)} does NOT cover this panel at all (it misses
  cfg00 and cfg11 outright; under first-line it misses workdir-branch-swap too).

Sealed-draft cross-check (uncommitted working-tree drafts at tip `68f25573`, measured with
the tip counter `d27e6769…2052c2` oracle — same CONFIGS): 4 kill + 3 accept;
`cfg00-setup-as-pass` diverges only under (0,0); `cfg11-workdir-wording`,
`workdir-branch-keep-swap`, `workdir-keep-cleanup-nested-config` only under (1,1) or
{(1,0),(1,1)} — ALL divergences are **full-stdout-only** (first-line+rc sees nothing).
The {(0,0),(1,1)} pair covers this draft set too, and **no landed or drafted specimen
ever diverges uniquely under (0,1) or (1,0)** — yet both directions are reachable kills
(DEMO-A/B), so the gap is panel-shaped, not impossible.

## Findings (ranked)

- **BOUND-1 — absolute-explicit-root blind spot survived A4 (fail-closed for the claim,
  fail-open for the tool's stated capability).** A4 replaced only the AUTO roots with the
  real `mktemp` shape; the two explicit roots became the RELATIVE literals
  `tally-audit`/`tally-audit-explicit`, so NO swept config carries an absolute `--workdir`
  path. DEMO-C (sha256 `774d08c8…a02a`): after the tally loop,
  `if [[ $auto -eq 0 && "$root" == /* ]]; then nfail=0; npass=$((npass+1)); fi`.
  Under the counter's own oracle plus an extra absolute-explicit config
  `('/tmp/tameshi-r35-absworkdir','0','0')` it diverges at vector 0 (pristine
  PASS passed=9 → copy SETUP counted=10) — i.e. under a REAL
  `bash mutate-and-run.sh --regression --workdir /tmp/…` run — while all four swept
  configs and the real frozen tool see zero divergence:
  `python3 lane/tools/tally-audit-v3.py --runner demoC.sh` →
  `CHECK runtime PASS vectors=30316 mismatched=0 … TALLY_AUDIT: PASS`, **exit 0**
  (a false-accept of the same root-shape class as wave-1 RevengerRootShape CRITICAL,
  moved to the explicit side). It stays BOUND, not CRITICAL: the counter's ground truth
  shares the blind spot, so a specimen exploiting it would score `invalid` (an accept
  that diverges is impossible under the frozen configs; a kill without divergence is
  rejected) — the claim's literal predicate cannot be falsified by it, and the falsifier
  wording is auto-root-specific. W1's BOUND ("explicit side admits no independent
  evasion") was wrong post-A4: the literals are now BOTH relative. The tool's comment
  "the explicit triples keep representative caller-supplied --workdir values, relative
  and absolute" (v3:347-348) is also stale — there is no absolute explicit triple.
  Fix direction: one absolute explicit literal (e.g. `/tmp/tameshi-r35-audit-work`)
  for (0,0) or (0,1), lockstep in tool and counter.
- **BOUND-2 — two-config sufficiency is a panel artifact (proved above).** Adopting
  {(0,0),(1,1)} would silently drop the runner's default config and the hermetic config;
  single-config kills exist (DEMO-A/B). The four-config sweep is the minimum that covers
  all single-config classes; even that misses the absolute-explicit root (BOUND-1).
- **HYGIENE-1 — dead constant.** `FREEZE_REV = '__FREEZE_REV__'` at c1-measure.py:47 is
  never referenced post-A5 (the freeze is derived from `contract.json` first-add history
  at :404-406). Harmless leftover; the `__FREEZE_REV__` placeholder suggests a templating
  step that no longer exists.
- **HYGIENE-2 — at-pin stale `TOOL_SHA256` (already fixed at tip).** At my dispatch pin
  `7da6e076`, c1-measure.py:46 pins `da23d3a2…` (pre-A4 tool) while the tree carries
  `ef98fc53…`; `tool_sha_ok=0` would have forced `C1_R35_PASS=false` (line 374 + 445).
  Resolved by A6 `f9df5898` ("caught pre-data by wave-2 seat CriticPredicate") before any
  deciding run; recorded here only because the pin I was dispatched at contained the defect.
- **HYGIENE-3 — duplicate all-zero vector** in `vectors_for` (vs[0] and vs[1]); the
  divergent-vector counts above reflect it. Cosmetic.

## What I could NOT break (proofs)

- **The four-config sweep itself**: every swept config is load-bearing — (0,0) for
  cfg00-accept-swap and cfg00-setup-as-pass, (1,1) for cfg11-pass-mask and two sealed
  workdir kills, (1,0) for DEMO-A and (with (1,1)) both root-keyed copies,
  (0,1) for DEMO-B. Removing any one admits a demonstrated kill class.
- **Full-stdout comparison**: removing it makes workdir-branch-swap non-divergent
  (invalid kill) and renders all four sealed workdir-wording kills invisible.
- **The panel's ground truth and the tool agree at the pin**: 5/5 kills diverge and are
  killed by `runtime` alone (rc=1); 3/3 accepts are identical on 267 vectors × 4 configs
  and accepted (rc=0). All edits applied exactly `count` times.
- **The A4 auto-root fix holds**: both auto configs share the REAL
  `/tmp/tameshi-r4-2-regression.*` root, and both root-keyed copies diverge under it
  (267/267 and 6/267 vectors). The RevengerRootShape mutant class is closed on the
  auto side; only the absolute-explicit side remains open (BOUND-1).
- **Runner is byte-identical** (`a7d3f2dd…912eb9` at pin and tip); no runner-mediated
  path was touched.

## Answers to the assigned question

1. **Per-copy need** — matrix above: cfg00→(0,0) only; cfg11→(1,1) only;
   workdir-branch-swap→{(1,0),(0,0)} full-stdout-only; root-keyed→{(1,0),(1,1)} both
   (shared real auto root); the three accepts→none.
2. **Could two configs suffice?** For this panel, {(0,0),(1,1)} alone does — the unique
   covering pair, forced by cfg00-accept-swap (requires (0,0)) and cfg11-pass-mask
   (requires (1,1)). What it loses: coverage of the runner's DEFAULT (1,0) config
   (DEMO-A survives) and the hermetic (0,1) config (DEMO-B survives), plus all
   single-config redundancy; and even four configs still miss an absolute `--workdir`
   root (DEMO-C is ACCEPTED, rc=0 — BOUND-1).

## Artifacts

`/fast/scratch/hyaku/tameshi-r35-seats/SimplifyConfigs/` — `matrix.py` `60261e00…30cb`,
`demos.py` `d924f93b…154b`, `vec_counts.py`, `matrix.out` (full per-copy JSON detail),
`demoA.sh` `a21f7e8a…fad89`, `demoB.sh` `b6a98b36…3a14e`, `demoC.sh` `774d08c8…a02a`,
`c1-measure-tip.py` `d27e6769…2052c2` (tip counter for sealed-draft cross-check).
Lane checkout at `7da6e076` untouched; no mutating git command ran.
