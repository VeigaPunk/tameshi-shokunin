# Registry completeness — round 17 / wave 2

Seat: `TameshiR17.RegistryCompleteness-2` (reviewer, leaf). Target: does
`tools/registry.json` at `eb7838b16490ca7ba17ea3242ade76a61f744af2` carry every
**active** registered entry command from the round-12/13/15/16 registries and
the SCORECARD Capabilities table at `98bea7da5801f4bc58e4187690ee1687c8a5061f`,
with the same argv — or did a row get silently dropped or re-pointed?

Environment: required fleet-mirror clone at
`/tmp/tameshi-r17w2-RegistryCompleteness-Rg9BRO/fleet/tameshi-shokunin`,
`git checkout --detach eb7838…`, siblings symlinked beside it. Every run below
executed in that clone; the live lane was never used as a tool root.
`tools/registry.json` sha256 `98bdc23ce4880fc3d23d169c38e36c2a9f2c69c273b936e868a7ddfd459e0630`
(29 rows: 28 active, 1 superseded; 24 rows tagged `baseline`). Nothing was
installed or upgraded for this seat; no pacman transaction was attempted.

## Baseline enumerated

10 registry rows (20 command forms) across the four tables plus 8 SCORECARD
evidence commands:

| # | Source (at 98bea7d) | Registered entry command | registry.json row | Verdict |
|---|---|---|---|---|
| 1 | `SKILL.md:1503` (round 12) | `repeat-control.py --runs 3 --out DIR -- COMMAND ARG...` (also recipe `:1492`) | **none** | **silent drop** |
| 2 | `SKILL.md:1503` | `repeat-control.py --snapshot DIR` | `repeat-control-snapshot-clean` (:5), `-mismatch` (:24) | covered, 2 instances (exit 0 / 1) |
| 3 | `SKILL.md:1503` | `repeat-control.py --selftest` | `repeat-control-selftest` (:43) | exact |
| 4 | `SKILL.md:1504` | `bash-witness-study.py count` | `bash-witness-count` (:64) | exact |
| 5 | `SKILL.md:1504` | `bash-witness-study.py selftest` | `bash-witness-selftest` (:85) | exact |
| 6 | `SKILL.md:1552` (round 13) | `pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` | `pin-disposition-read` (:106) | exact |
| 7 | `SKILL.md:1552` | `pin-disposition.py --selftest` | `pin-disposition-selftest` (:132) | exact |
| 8 | `SKILL.md:1553` | `witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` | `witness-metadata-check` (:153) | exact |
| 9 | `SKILL.md:1553` | `witness-metadata.py --selftest` | `witness-metadata-selftest` (:176) | exact |
| 10 | `SKILL.md:1680` (round 15) | `context-capture.py --check` (frozen clean receipt) | `context-capture-frozen` (:294) | present, argv `--check --json` |
| 11 | `SKILL.md:1680` | `context-capture.py --check --receipt FILE --expected FILE` | `context-capture-missing-env` (:316), `-mapping-suffix` (:341) | present; row 14 fixture path differs, bytes identical |
| 12 | `SKILL.md:1680` | `context-capture.py --selftest` | `context-capture-selftest` (:363) | exact |
| 13 | `SKILL.md:1681` | `evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json` | `evidence-disposition-round14-superseded` (:250) | same argv, **superseded**, `expect.exit=0` false (observed 2) |
| 14 | `SKILL.md:1681` | `evidence-disposition.py --selftest` | `evidence-disposition-selftest` (:273) | exact |
| 15 | `SKILL.md:1810` (round 16) | `bash tools/mutate-and-run.sh --selftest` | `mutate-and-run-selftest` (:384) | exact |
| 16 | `SKILL.md:1810` | `bash tools/mutate-and-run.sh --regression` | `mutate-and-run-regression` (:406) | exact |
| 17 | `SKILL.md:1811` | `measure.py --rev REV` | `measure-round16-rev` (:427) | present, argv `--rev HEAD --repo .` |
| 18 | `SKILL.md:1811` | `measure.py --selftest` | `measure-round16-selftest` (:452) | exact |
| 19 | `SKILL.md:1812` | `assemble.py --selftest` | `assemble-round16-selftest` (:473) | exact |
| 20 | `SKILL.md:1813` | `reattribute.py --selftest` | `reattribute-round16-selftest` (:494) | exact |

SCORECARD Capabilities at `98bea7d` (`SCORECARD.md:238-247`):

| Source line | Command | registry.json row |
|---|---|---|
| `SCORECARD.md:240` | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` | `sources-census` (:515) exact |
| `SCORECARD.md:241`/`:242` | `bash tools/mutate-and-run.sh --selftest` / `--regression` | rows 17/18, exact |
| `SCORECARD.md:243` | `python3 tools/repeat-control.py --selftest` | row 2, exact |
| `SCORECARD.md:244` | `python3 tools/pin-disposition.py --selftest` | row 6, exact |
| `SCORECARD.md:245` | "metadata selftest39/39" (no literal command; the null-only-companion and producer same-oracle cases are described without argv) | row 8 covers the selftest |
| `SCORECARD.md:246` | `python3 tools/evidence-disposition.py --selftest` | row 12, exact |
| `SCORECARD.md:247` | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4d…` | `verify-round15` (:535) exact |

The round-14 table (`SKILL.md:1597-1602`) is marked "superseded by round 15"
and "not active"; the archived `capture-context.py` row is correctly absent.
No round-12/13/15/16 command is missing **except** #1.

## Findings

### F1 (silent drop, low) — the live `--runs` form has no registry row

`SKILL.md:1503` registers two entry forms joined by "or": the live comparison
`python3 tools/repeat-control.py --runs 3 --out DIR -- COMMAND ARG...` and the
snapshot replay `--snapshot DIR`. `tools/registry.json` has rows only for
`--snapshot` (clean and mismatch, :5-42); `grep -c -- '--runs' tools/registry.json`
returns `0`. The form is live, not historical: running
`python3 tools/repeat-control.py --runs 3 --out <fresh> -- true` exited 0 with
`REPEAT_CONTROL: controls_match` (3 runs, identical). No registry note says the
form is intentionally unregistered.

The omission is *defensible*: `registry-check.py` rows are `exec`'d directly
(no shell), `expect.exit` is fixed per row, and the output DIR must not exist,
so a static row cannot allocate a unique DIR or carry a caller command. But
"defensible" is not "documented": the registry's coverage story is silent about
the one active entry form it cannot express, and the snapshot rows exercise
only the comparison half of the round-12 gate.

### F2 (false expectation on a superseded row, low) — expect 0 where the page says 2

`evidence-disposition-round14-superseded` (`registry.json:250-266`) registers
the round-15 table's exact argv
(`--root . --dispositions .ufo/evidence/round-14/dispositions.json --json`) with
`expect.exit = 0`. The same page line (`SKILL.md:1681`, both revs) says
`--root .` returns 2 `expected_input_digest_mismatch` "by design" and that the
0-clean outcome is restored only by re-pinning. Observed at landing:

```
ROW evidence-disposition-round14-superseded superseded expect=0 got=2
```

Status `superseded` keeps it out of `held=N/M` (registry-check counts it in
`superseded=K` only), so no active baseline row breaks — but the registry
records an expectation the page itself calls unreachable, and the landing page
warns that relabelling does not restore 0. A row-level reader sees `expect: 0`
and no counter-evidence; the human line is the only place the contradiction
surfaces. Either pin the observed 2 or drop the expectation field for
superseded rows.

### F3 (present with a different argv — benign) — three deviations, none semantic

1. `context-capture-frozen` uses `--check --json` (`registry.json:296-309`)
   where `SKILL.md:1680` names `--check`. Verified both: bare `--check` →
   exit 0 `CONTEXT: OK (id=context_consistent …)`; `--check --json` → exit 0
   with `"id": "context_consistent"`. Output mode only; the registered needle
   `context_consistent` matches in both. Not a drop.
2. `measure-round16-rev` uses `--rev HEAD --repo .` (`registry.json:427-445`)
   where `SKILL.md:1811` names `--rev REV`. `measure.py --help` shows `--repo`
   is supported, defaulting to `/home/vgpnk/Projects/shokunin/tameshi-shokunin`;
   `--repo .` is *required* so a `--rev` clone measures its own checkout rather
   than the live lane. `HEAD` is the detached checkout of the graded rev. This
   is a legitimate instantiation, not drift.
3. `context-capture-missing-env` uses
   `.ufo/evidence/round-15/frozen/context-missing-env/receipt.json` where
   `SKILL.md:1680` pins the negative fixture
   `.ufo/evidence/round-14/context-missing-env.json`. `sha256sum` on both gives
   `1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2a2852aa208` — same
   bytes, same pinned id/exit via `expected.json`. Path substitution only.

### F4 (provenance, low) — six `source` refs do not point at their command

`registry-check.py` validates `source` only against
`^[^@]+@[0-9a-f]{7,40}:\d+` (SOURCE_RE) and never opens the cited file, so a
wrong ref passes silently. Checked each ref against the cited line:

- Rows 10, 25, 26, 27, 28 cite `SKILL.md@98bea7d:1806`. At `98bea7d` (and at
  landing) line 1806 is `### Round-16 gate/probe registry`; it contains none of
  `dispositions-before.json`, `registry-check.py`, `measure.py`,
  `trace-inputs.py` or `assemble.py`. Their commands are defined at landing
  `SKILL.md:1846-1857` / `:1897-1905`.
- Row 9 cites `SKILL.md@98bea7d:1681`, which names the **round-14**
  `dispositions.json`; `round-17` does not appear on that line at `98bea7d`.
  The live entry only appears at landing `:1681` ("Live entry: `--dispositions
  .ufo/evidence/round-17/dispositions.json`"). The rev pin is stale.

Rows 0-8, 11-24 all resolve to a line that names the row's tool (and its
distinctive file where one exists). Held counts are unaffected; the defect is
that the registry's traceability field cannot be trusted for the round-17
additions.

### F5 (informational) — extra instance and out-of-baseline rows

- `context-capture-mapping-suffix` (:341) is an extra second negative fixture
  of the documented `--receipt/--expected` form. The 98bea7d page names only
  the missing-env fixture; the fixture exists at that rev
  (`.ufo/evidence/round-15/frozen/mapping-suffix/`). Extra coverage, not a drop.
- The landing round-17 registry (`SKILL.md:1846-1857`, `:1897-1905`) lists live
  entry commands for `registry-check.py`, round-17 `measure.py --rev`,
  `trace-inputs.py --root … --out …` and `assemble.py --reports … --out …`.
  `registry.json` registers only their `--selftest` rows (25-28), unlike the
  round-16 measure precedent (row 19, live). The registry-check live form
  cannot self-register without recursion, but the round-17 measure `--rev` form
  could. This is outside the requested 98bea7d baseline; flagged only so the
  asymmetry is not mistaken for a baseline drop.

## Observed runs

All from the clone, `cwd = …/fleet/tameshi-shokunin`, rev pinned as noted:

| Command | Exit | Key output |
|---|---|---|
| `python3 tools/registry-check.py --rev eb7838… --registry tools/registry.json --tag baseline --json` | 0 | `REGISTRY_CHECK: held=23/23 superseded=1` |
| `python3 tools/registry-check.py --rev eb7838… --registry tools/registry.json --json` (all rows) | 0 | `REGISTRY_CHECK: held=28/28 superseded=1`; one `superseded expect=0 got=2` line (F2) |
| `python3 tools/registry-check.py --rev 98bea7d… --registry tools/registry.json --tag baseline --json` | 1 | `ROW evidence-disposition-round17 expect=0 got=2 differs`; `held=22/23 superseded=1` |
| `python3 tools/registry-check.py --rev 98bea7d… --registry tools/registry.json --only evidence-disposition-round17-before` | 1 | `ROW … expect=1 got=2 differs` |
| `python3 tools/context-capture.py --check` | 0 | `CONTEXT: OK (id=context_consistent … exit=0 findings=0)` |
| `python3 tools/context-capture.py --check --json` | 0 | `"id": "context_consistent"`, `"verdict_matches_expected": true` |
| `python3 tools/repeat-control.py --runs 3 --out <fresh> -- true` | 0 | `REPEAT_RUN 1/2/3 exit=0 … REPEAT_CONTROL: controls_match` |
| `grep -c -- '--runs' tools/registry.json` | 1 (grep: 0 matches) | `0` — no `--runs` row |
| `sha256sum .ufo/evidence/round-14/context-missing-env.json .ufo/evidence/round-15/frozen/context-missing-env/receipt.json` | 0 | both `1ee9d09b…` |
| `python3 .ufo/evidence/round-16/measure.py --help` | 0 | `--repo REPO  repository path (default: /home/vgpnk/Projects/shokunin/tameshi-shokunin)` |
| `git diff 2a22ade..eb7838 -- tools/registry.json` | 0 | empty — registry unchanged within the wave |
| `git show 98bea7d:tools/registry.json` | 128 | file absent before landing (so `--registry` is required for the before run) |

Relation to claim C2: the baseline registry holds **23/23 at landing** and
**22/23 at 98bea7d**. The single before-state difference is the newly
registered round-17 disposition row, which exits 2 with
`"kind": "dispositions_missing"`, `.ufo/evidence/round-17/dispositions.json`;
the whole round-17 evidence tree is absent at `98bea7d` (empty
`git ls-tree -r 98bea7d .ufo/evidence/round-17/`). The round-17 `before` row
fails identically (expect 1, got 2, `dispositions_missing` for
`dispositions-before.json`).
No round-12/13/15/16 baseline command changed outcome between the two revs —
the old round-15 disposition command is exit 2 at both, and the registry says
so (in the `superseded` line only, F2). "Every baseline row holds" is true for
**active** rows; it is not true if a reader counts the superseded row's
registered `expect=0`.

## Residual risk

- The drop in F1 is invisible to `registry-check.py` by construction: the
  monitor grades rows, it does not cross-check the SKILL page's command cells.
  A future round could add a coverage manifest (SKILL source-cell → row name)
  and fail closed on an unmapped active cell.
- F4 shows the same monitor cannot detect a stale `source` ref; any claim of
  "every row is traceable to its page line" is currently unverified.
- The `external: true` rows (`pin-disposition-read`, `verify-round15`) still
  read live-fleet state under `--rev`; their `held` at the old rev measures the
  clone's tool logic against today's fleet, not the old rev's fleet. This is
  declared, but it means the before/after runs are not a fully hermetic replay.

## Verdict

Registry completeness at the landing rev **holds for every fixed-outcome active
entry command** (23/23 baseline, 28/28 with round-17 rows) but is **partial**
overall: the live `--runs` form of the round-12 gate is silently unregistered,
three argv deviations are benign/necessary, one superseded row registers a
false `expect=0`, and six round-17 `source` refs point at lines that do not
contain their commands — none of which changes a baseline held count.
