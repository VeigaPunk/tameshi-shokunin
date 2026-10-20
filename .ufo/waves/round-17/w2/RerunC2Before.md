# RerunC2Before — independent re-run of the C2 before measurement

Scope: re-run the C2 before-state command from a throwaway clone and report every
differing row with its cause. Lane root `/home/vgpnk/Projects/shokunin/tameshi-shokunin`;
graded clone at `eb7838b16490ca7ba17ea3242ade76a61f744af2` in the required fleet-mirror
layout. No delegation, no background jobs, no lane writes beyond this report.

Setup:

```
W=/tmp/tameshi-r17w2-RerunC2Before-2-wGcxiQ            # fleet-mirror workspace
C=$W/fleet/tameshi-shokunin                            # clone, detached at eb7838b
S=/tmp/tameshi-r17w2-RerunC2Before-2-scratch-HeWWiV    # scratch
git -C $C show eb7838b16490ca7ba17ea3242ade76a61f744af2:tools/registry.json \
  > $S/registry-eb7838b.json
sha256sum $S/registry-eb7838b.json $C/tools/registry.json
# 98bdc23ce4880fc3d23d169c38e36c2a9f2c69c273b936e868a7ddfd459e0630  (both)
```

`git -C $C rev-parse HEAD` = `eb7838b16490ca7ba17ea3242ade76a61f744af2`.

## Command and exit

```
cd $C
python3 tools/registry-check.py \
  --rev 98bea7da5801f4bc58e4187690ee1687c8a5061f \
  --registry $S/registry-eb7838b.json --tag baseline --json
```

Exit **1**, wall 209.87 s. JSON on stdout, human rows on stderr:

```
ROW evidence-disposition-round17 expect=0 got=2 differs
ROW evidence-disposition-round14-superseded superseded expect=0 got=2
REGISTRY_CHECK: held=22/23 superseded=1
```

JSON report fields (schema `tameshi-registry-check-report-v1`):

```
rev            98bea7da5801f4bc58e4187690ee1687c8a5061f
rev_resolved   98bea7da5801f4bc58e4187690ee1687c8a5061f
registry_sha256 98bdc23ce4880fc3d23d169c38e36c2a9f2c69c273b936e868a7ddfd459e0630
live           false      tags ["baseline"]
held 22 / total 23 / superseded 1 / exit 1
```

Selection and count semantics: `--tag baseline` selects 24 rows (23 active + 1
superseded) at `tools/registry-check.py:524-527`; only active rows enter `held/total`
and the exit code is `0 if held == len(active) else 1` at `tools/registry-check.py:541-551`;
the fixed trailer is printed at `tools/registry-check.py:573`. The graded rev was resolved
in the clone and executed in a temp clone (`root` in the report was
`/tmp/tameshi-registry-check-iphc01y6/fleet/tameshi-shokunin`), never the live lane.

## Differing rows (all of them)

### 1. `evidence-disposition-round17` — active, expect 0, got 2 (the disposition-capability row)

Row: `tools/registry.json:197-222`; expects `exit: 0` plus needles
`"status": "clean"`, `"effective": 11`, `"superseded": 1` (`:208-215`).
Observed fragment: `got=2`, `held=false`, `stdout_missing` = all three needles; the row's
own JSON:

```
error.kind    dispositions_missing
error.message .ufo/evidence/round-17/dispositions.json
status        could_not_evaluate
tool          evidence-disposition.py r14
tool_sha256   1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95
```

Cause A — the artifact is absent at the before rev. `git cat-file -e
98bea7d:.ufo/evidence/round-17/dispositions.json` fails ("exists on disk, but not in
'98bea7d…'"); the file was added only in `2a22ade` (`git log --diff-filter=A`). The r14
tool raises `dispositions_missing` from `read_dispositions`
(`tools/evidence-disposition.py@98bea7d:300-304`). `tool_sha256` 1609a9… equals
`sha256(tools/evidence-disposition.py@98bea7d)`, so the before tree ran its own tool
(unmodified by the landing).

Cause B — capability, not just the missing file. I cloned `98bea7d` a second time,
copied `eb7838b:.ufo/evidence/round-17/dispositions.json` into it, and ran the old tool
directly:

```
cd $W2/c   # W2=/tmp/tameshi-r17w2-RerunC2Before-2-v2-UJFYsy, detached at 98bea7d
python3 tools/evidence-disposition.py --root . \
  --dispositions .ufo/evidence/round-17/dispositions.json --json
```

Exit **2**:

```
error.kind    schema_mismatch
error.message dispositions schema must be 'evidence-dispositions-v1'
tool_sha256   1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95
```

The before tool supports only `evidence-dispositions-v1`
(`tools/evidence-disposition.py@98bea7d:94`, enforced at `:1133-1137`); the round-17
artifact declares `evidence-dispositions-v2`
(`.ufo/evidence/round-17/dispositions.json@eb7838b:2`). So the capability difference is
real and twofold: no v2 artifact at the before rev, and no v2 support in the before tool.
No other cause contributes to this row.

### 2. `evidence-disposition-round14-superseded` — superseded, expect 0, got 2 (reported, excluded from 22/23)

Row: `tools/registry.json:250-271`, `superseded_by: evidence-disposition-round17`.
Observed: `ROW … superseded expect=0 got=2`; JSON error:

```
error.kind    expected_input_digest_mismatch
error.message tools/mutate-and-run.sh: observed 0673d2e5374b94c651238e7497cbebaffb6483348400747b08f9d27cdc8118aa
              expects 75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5
status        could_not_evaluate, exit 2
```

Cause — historical input drift inside the superseded recipe. The round-14 dispositions
pin `.ufo/evidence/round-13/expected.json` (sha `a0160794…`) as their expected file
(`.ufo/evidence/round-14/dispositions.json:2-5`), and that expected file pins
`tools/mutate-and-run.sh` to `75ed934d…` at line 12
(`.ufo/evidence/round-13/expected.json@98bea7d:12`). At `98bea7d` the file hashes
`0673d2e5…`. The r14 tool verifies every `expected.inputs` digest in full before any
predicate (`tools/evidence-disposition.py@98bea7d:1184-1192`), so it exits 2 as
could-not-evaluate. Drift timeline from `git show <rev>:tools/mutate-and-run.sh | sha256sum`:

```
606716f (pre-round-16)  75ed934d…   <- the pinned bytes
c699c8c (round-16)      89722ddb…
05a2247 (round-16)      0673d2e5…   <- observed at 98bea7d
2a22ade (round-17)      fb6d86d5…   <- observed at eb7838b (after run)
```

The row's `expect: 0` is not invented: re-running the same row at the round-14 tip
`0c6e36d` (`--rev 0c6e36d --only evidence-disposition-round14-superseded --json`)
gives exit **0**, `ROW … superseded expect=0 got=0`, `status: clean`, and
`tools/mutate-and-run.sh@0c6e36d` hashes exactly `75ed934d…`. So the expectation was true
when authored and the row drifted through round-16 edits; it predates the round-17
landing, is correctly marked superseded, and is correctly excluded from `held/total`.
The v2 artifact itself records this drift as a first-class fact
(`.ufo/evidence/round-17/dispositions.json@eb7838b:11-19` names the 75ed934d bytes and the
round-16/17 commits that moved them), and at `eb7838b` the superseded row still reports
`got=2` with observed `fb6d86d5…`, still excluded from 23/23.

## Rows that did not differ, and the one external dependency

22 other active rows held; no other differing row exists in the report (verified by
filtering every fragment with `held == false`: exactly the two above). One held row is
not hermetic: `pin-disposition-read` (`tools/registry.json:106-130`) holds `exit 0` with
`"unavailable": 0`, but its argv passes `--root /home/vgpnk/Projects/shokunin` (`:114`)
and declares `external: true` / tag `fleet-live` (`:125-129`). `pin-disposition.py --root`
is a fleet root (super-repo + siblings), so this row reads live fleet state. It held in
my run (elapsed 0.062 s). Because I graded from a fleet-mirror clone, the monitor's
`_argv_outside_fleet` compared tokens against the temp mirror
(`tools/registry-check.py:326-339`), so it did not emit `non_hermetic_argv` for this row;
when the same tool is invoked with the live lane as `--root`, the token equals the live
fleet root and would be flagged (still allowed because `external` is declared). The
landed before receipt was produced from a temp clone too and also carries no
`non_hermetic_argv` for this row.

## Independent corroboration

- Landed receipt equality. Normalizing my JSON against
  `.ufo/evidence/round-17/c2-before-98bea7da5801f4bc58e4187690ee1687c8a5061f.json`
  (`rev_resolved`, `registry_sha256`, `live`, `tags`, `held`, `total`, `superseded`,
  `exit`, and all 24 `(name, status, expect, got, held, tags)` tuples) yields **all equal,
  zero row diffs**. The landed `.txt` differs from my human output only by its appended
  `exit=1` line.
- After-side contrast (extra check, same command family):
  `--rev eb7838b --registry $S/registry-eb7838b.json --tag baseline --json` → exit **0**,
  `REGISTRY_CHECK: held=23/23 superseded=1`; `evidence-disposition-round17` held (needles
  present), and `evidence-disposition-selftest` held in 3.669 s — the row that was red at
  `2a22ade` (`c2-after-2a22ade.txt`) before the hermetic-git-env fix. The superseded row
  still reported `got=2` and stayed outside the count.
- Timing: before 209.87 s, after 208.01 s; `mutate-and-run-regression` dominates both
  runs (192.04 s before, 184.49 s after) against its 900 s `timeout_s`
  (`tools/registry.json:419`); the next largest is 5.38 s before / 6.55 s after, so every
  row finished far inside its bound.

## Residual risks / notes

1. The raw before-row error is `dispositions_missing`, not `schema_mismatch`. A reader
   looking only at the receipt could think the v2 schema was rejected at that invocation;
   the injected-artifact probe above separates the two. Claim wording should read "the
   round-17 v2 dispositions artifact and v2-aware tool are both absent at 98bea7d".
2. `pin-disposition-read` returned `held` by reading the live fleet root; that one row of
   the 22 is not reproducible from a clone alone. The dependency is declared in the
   registry (`external: true`, tag `fleet-live`), so this is a visibility limitation of
   the `non_hermetic_argv` audit when grading from a fleet-mirror clone, not an unmet
   registry claim. No other row names an absolute path.
3. Two layers are distinct and intended: the *driver* was `eb7838b`'s
   `tools/registry-check.py` (the file invoked from `$C`), while every *row* executed
   inside the `98bea7d` temp clone. The graded registry was a /tmp copy of
   `eb7838b:tools/registry.json` (sha 98bdc23…), identical to the clone's own
   `tools/registry.json`. This matches the landed receipt's construction (same
   `registry_sha256`, same row outcomes).
4. Lane untouched: `git -C <lane> rev-parse HEAD` remained `eb7838b…`; the only write from
   this seat is this report. No tool installs or upgrades were needed or performed.

## Verdict

C2 before half **holds**: exit 1, `held=22/23 superseded=1`, exactly one active row
differs and it is the disposition-capability gate (missing v2 artifact at the before rev;
old tool rejects v2 with `schema_mismatch` when the artifact is injected), while the only
other differing row is the superseded round-14 recipe reported and excluded, differing
solely from historical `tools/mutate-and-run.sh` drift that predates the round-17 landing
and was green at its own rev `0c6e36d`.

One line: attacked the C2 before measurement end-to-end — it reproduces the landed receipt row-for-row (all 24 fragments equal after normalizing root, registry path and elapsed time), with both differing rows caused and explained; holds.
