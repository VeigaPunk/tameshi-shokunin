# RegistryCheck — round 26 wave 1 (axis: operability)

Seat: `TameshiR26.RegistryCheck` (executor). Report written 2026-10-22.
Scope: run the registry monitor against the round-26 integration commit and report
the `REGISTRY_CHECK` line, every row that is not `held`, the two new `mte-interop-*`
rows, and the wall time. **No production file was edited**; the only file written by
this seat is this report.

## Verdict

**The target command does not evaluate the registry at all.** It exits `2`
(`could-not-evaluate`) on a schema violation, so **zero of the 49 active rows ran**
and **no row reached a `held`/`differs` verdict**. The two rows added by the round-26
integration (`mte-interop-selftest`, `mte-interop-check`) are the cause: their
`source` strings do not satisfy the registry schema that `tools/registry-check.py`
enforces on every row. The defect is introduced by the round-26 integration commit
`a08e85c5d7f899e8a5992e20517edb1a380d79eb` itself; the frozen pre-integration commit
`622d31d9` and the base `d4140796` are both clean.

The smallest safe correction is one field per row (append `@<rev>` and drop the
parenthetical). With only that change applied to a scratch copy, the same command
runs the full registry: **47/49 held, 7 superseded, exit 1**, wall **202.2 s**, and
both new rows hold. The two rows that then differ are **pre-existing** — they fail
identically at base `d4140796`, so they are not a round-26 regression.

## Axes named (godspeed)

| Axis | Question | Result |
|---|---|---|
| operability | Does the target command evaluate and produce per-row verdicts? | **No** — exit 2, `could-not-evaluate`, 0 rows run |
| operability | Is the tool itself sound? | Yes — `registry-check.py --selftest` → `SELFTEST: PASS (51 cases)`, exit 0 |
| regression isolation | Did round-26 introduce the failure? | Yes — schema-clean at `d4140796`/`622d31d9`, 2 errors at `a08e85c5` |
| counter fidelity | Did the round-26 counters see it? | No — C2 item 1 reads `RESOLVED`; C1 passes `depth_score=9` |
| hermeticity | Is the new gate row reproducible under `--rev`? | Invocation-dependent (see F3) |

## Evidence

### E1 — clone identity (as prescribed)

```
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/RegistryCheck-reg
git -C /tmp/RegistryCheck-reg rev-parse master   → a08e85c5d7f899e8a5992e20517edb1a380d79eb
git -C /tmp/RegistryCheck-reg rev-parse HEAD     → a08e85c5d7f899e8a5992e20517edb1a380d79eb
sha256sum /tmp/RegistryCheck-reg/tools/registry.json \
          /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/registry.json
→ e795532f6bf686fb69da53f8dd84a3d159be2b080314ce9f49bf7dd57ed96eca  (both, identical)
```

### E2 — the target command, verbatim

```
cd /tmp/RegistryCheck-reg
python3 tools/registry-check.py --rev a08e85c5d7f899e8a5992e20517edb1a380d79eb
```

stdout (one line, byte-for-byte, `repr()`):

```
"REGISTRY_CHECK: could-not-evaluate (registry invalid: rows[54].source must be <file>@<7-40 hex rev>:<line>, got 'corpus/lessons/round-25-verifier-spotcheck.md:189-192 (routed item 1)'; rows[55].source must be <file>@<7-40 hex rev>:<line>, got 'corpus/lessons/round-25-verifier-spotcheck.md:189-192 (routed item 1)')\n"
```

stderr: empty. Exit code: **2**.

### E3 — wall time of the target command

Three consecutive runs, timed with `time.monotonic()` around `subprocess.run`:

```
run1 wall=0.526s exit=2 stdout_lines=1 stderr=''
run2 wall=0.576s exit=2 stdout_lines=1 stderr=''
run3 wall=0.509s exit=2 stdout_lines=1 stderr=''
```

**Wall time of the target command: ~0.5 s** — and this is *not* a working run. The
0.5 s is the cost of parsing and rejecting the registry; the monitor aborts before
any row executes. A registry that actually runs takes **202.2 s** (E6).

### E4 — rows that are not `held`

**None — because no row ran.** The monitor validates the whole registry before
selecting or executing anything (`tools/registry-check.py:180` `registry_errors`,
called from `evaluate()` at `tools/registry-check.py:846-848`), so the invalid
registry aborts the entire evaluation. Consequences:

* `held=0/49`, `superseded=0` — no trailer with counts is printed at all; the
  `REGISTRY_CHECK:` line is the `could-not-evaluate` form instead.
* Even a single-row selection is blocked, so neither new row can be exercised in
  isolation:

```
python3 tools/registry-check.py --rev a08e85c5d7f899e8a5992e20517edb1a380d79eb --only mte-interop-selftest
→ REGISTRY_CHECK: could-not-evaluate (registry invalid: rows[54].source ...; rows[55].source ...)
→ exit=2
```

* The two rows that *are* defective, as named by the tool's own validator:

| index | row name | status | defect |
|---|---|---|---|
| `rows[54]` | `mte-interop-selftest` | active | `source` = `corpus/lessons/round-25-verifier-spotcheck.md:189-192 (routed item 1)` — no `@<rev>`, trailing parenthetical |
| `rows[55]` | `mte-interop-check` | active | same `source` string |

Enforcing rule: `tools/registry-check.py:108`
`SOURCE_RE = re.compile(r"^[^@]+@[0-9a-f]{7,40}:[0-9]+(-[0-9]+)?$")`, applied at
`tools/registry-check.py:257-262`; the required form is documented at
`tools/registry-check.py:24` (`"source": "<file>@<7-40 hex rev>:<line>[-<line>]"`).

### E5 — the two new rows, verbatim from `tools/registry.json`

`tools/registry.json:1000-1009`:

```json
    {
      "name": "mte-interop-selftest",
      "kind": "selftest",
      "argv": ["uv", "run", "--no-project", "--with", "jsonschema==4.25.1", "python3", "tools/mte-interop.py", "--selftest"],
      "expect": {"exit": 0, "stdout_contains": ["MTE_SELFTEST: 17/17 pass"]},
      "timeout_s": 300,
      "status": "active",
      "tags": ["new-r26"],
      "source": "corpus/lessons/round-25-verifier-spotcheck.md:189-192 (routed item 1)"
    },
```

`tools/registry.json:1010-1019`:

```json
    {
      "name": "mte-interop-check",
      "kind": "gate",
      "argv": ["uv", "run", "--no-project", "--with", "jsonschema==4.25.1", "python3", "tools/mte-interop.py", "--check", "--fleet-root", "/home/vgpnk/Projects/shokunin"],
      "expect": {"exit": 0, "stdout_contains": ["MTE_INTEROP: PASS legs_conforming=9/9"]},
      "timeout_s": 900,
      "status": "active",
      "tags": ["new-r26"],
      "source": "corpus/lessons/round-25-verifier-spotcheck.md:189-192 (routed item 1)"
    },
```

Both are the **last two rows** of the registry (index 54 and 55 of 56; 49 active,
7 superseded). They are the only two rows in the file whose `source` points into
`corpus/`; the other 54 all use the `<file>@<hexrev>:<line>` form (e.g.
`tools/registry.json:1005`
`".ufo/waves/round-23/fresh-adjudication.json@6a1821a8897eea6e7d9669292160ec9593669409:74-93"`).

### E6 — minimal correction, then the full run (scratch only)

The correction is one field per row: insert the revision and drop the parenthetical.

```
"corpus/lessons/round-25-verifier-spotcheck.md:189-192 (routed item 1)"
→ "corpus/lessons/round-25-verifier-spotcheck.md@a08e85c5d7f899e8a5992e20517edb1a380d79eb:189-192"
```

Applied **only** to a scratch copy (`/tmp/RegistryCheck-scratch/registry-fixed.json`)
and graded with the tool's own `--registry` flag (no repository file touched):

```
python3 tools/registry-check.py --rev a08e85c5d7f899e8a5992e20517edb1a380d79eb \
        --registry /tmp/RegistryCheck-scratch/registry-fixed.json --json
```

Result: **WALL=202.2 s, EXIT=1**, trailer

```
REGISTRY_CHECK: held=47/49 superseded=7
```

`rev_resolved=a08e85c5d7f899e8a5992e20517edb1a380d79eb`, `registry_sha256` of the
patched file recorded in the JSON report. Both new rows **hold**:

```
ROW mte-interop-selftest expect=0 got=0 held
ROW mte-interop-check expect=0 got=0 held
```

The two rows that are **not** `held` under the corrected registry:

| row | expect | got | kind of failure |
|---|---|---|---|
| `mutate-and-run-regression` | 0 | 2 | `SETUP (repo_identity_mismatch: .../fleet/kumitate-shokunin is not its own repository; ...)` — the `--rev` fleet mirror holds sibling lanes as symlinks, which the runner's repo-identity guard rejects |
| `round21-measure-selftest` | 0 | 1 | uncaught `subprocess.CalledProcessError` — `git -C .../fleet/tameshi-shokunin show 08175c62…:tools/mutate-and-run.sh` exits 128 (same symlinked-sibling cause) |

**Both are pre-existing, not round-26 regressions.** Re-run at the base revision
with the base (schema-valid) registry:

```
python3 tools/registry-check.py --rev d4140796f4e48e8ec81b793facba73fbd03b4443 --only mutate-and-run-regression
→ ROW mutate-and-run-regression expect=0 got=2 differs
python3 tools/registry-check.py --rev d4140796f4e48e8ec81b793facba73fbd03b4443 --only round21-measure-selftest
→ ROW round21-measure-selftest expect=0 got=1 differs
```

Identical failures at base. They are an environment/layout gap in the `--rev`
fleet-mirror layout, not something round 26 introduced.

### E7 — the regression is local to the round-26 integration commit

Schema validation of `tools/registry.json` at each revision, using the tool's own
`registry_errors()` (imported read-only; no row executed):

```
d4140796 rows=54 errors=0
622d31d9 rows=54 errors=0
a08e85c5 rows=56 errors=2
    rows[54].source must be <file>@<7-40 hex rev>:<line>, got 'corpus/lessons/round-25-verifier-spotcheck.md:189-192 (routed item 1)'
    rows[55].source must be <file>@<7-40 hex rev>:<line>, got 'corpus/lessons/round-25-verifier-spotcheck.md:189-192 (routed item 1)'
```

The frozen pre-integration contract commit `622d31d9` is clean; the round-26
integration `a08e85c5` is the commit that adds the two rows and the two schema
violations.

### E8 — the round-26 counters do not see this

```
python3 .ufo/evidence/round-26/c2-measure.py --repo /tmp/RegistryCheck-reg
C2_ITEM R25-SPOT-1: RESOLVED
C2_ITEM R25-SPOT-2: MISMATCH (...)
C2_ITEM R25-SPOT-3: MISMATCH (...)
C2_RECORD: mismatches=2/3          exit=1

python3 .ufo/evidence/round-26/c1-measure.py --repo /tmp/RegistryCheck-reg
C1_LEG js-kimi-census: WIRED … (9 legs WIRED)
C1_DEPTH: recorded_cases=9 wired_legs=9 depth_score=9   exit=0
```

C2 item 1 accepts the row because its criterion is only "an active registry row
whose argv names `tools/mte-interop.py`" — a weaker test than the registry schema
the monitor enforces. That is how a registry-invalidating row was recorded as
`RESOLVED`.

### E9 — the tool itself is operable

```
cd /tmp/RegistryCheck-reg && python3 tools/registry-check.py --selftest
… SELFTEST_CASE only-missing PASS (exit=2) … SELFTEST_CASE json-report PASS (exit=1)
SELFTEST: PASS (51 cases)      exit=0      (11.24 s)
```

## Findings

**F1 — blocking: the two new rows violate the registry schema, so the registry
monitor cannot evaluate the registry at `a08e85c5`.** Evidence: E2, E4, E7.
Smallest safe correction: rewrite the `source` of `mte-interop-selftest`
(`tools/registry.json:1008`) and `mte-interop-check` (`tools/registry.json:1018`)
to the enforced form, e.g.
`corpus/lessons/round-25-verifier-spotcheck.md@a08e85c5d7f899e8a5992e20517edb1a380d79eb:189-192`.
With that change the monitor runs the whole registry (E6). No other field of either
row is wrong; only `source`.

**F2 — the registry is the monitor's only gate for the new tool, and the round-26
counter that "fixed" the routed item never validated it against the schema.** The
C2 item-1 criterion (`c2-measure.py`, `item1()`) should also require the row to
satisfy `registry_errors()`, otherwise "RESOLVED" can coexist with
"could-not-evaluate". The same `source` string appears in both the registry and
the wave evidence, so the fix must be applied in the registry file itself; the
integrator (L1) owns that edit.

**F3 — the new gate row is not hermetic under `--rev`, and its verdict depends on
where the monitor is invoked.** `mte-interop-check` argv carries the absolute
`/home/vgpnk/Projects/shokunin` (`tools/registry.json:1015`). The monitor's
fleet-root is `os.path.dirname(os.path.realpath(root_requested))`
(`tools/registry-check.py:1907`), and `_argv_outside_fleet()`
(`tools/registry-check.py:632-649`) marks such a row `non-hermetic` → `differs`
unless the row declares `"external": true` (`tools/registry-check.py:662-671`).
Measured with the tool's own function:

```
fleet_root=/home/vgpnk/Projects/shokunin  mte-interop-check   outside=['/home/vgpnk/Projects/shokunin'] external=None
fleet_root=/tmp                           mte-interop-check   outside=[]                                 external=None
```

So from the prescribed clone path (`/tmp/RegistryCheck-reg`, fleet root `/tmp`) the
row is *not* flagged and it grades the live fleet's sibling lanes; run from the lane
itself (fleet root `/home/vgpnk/Projects/shokunin`) the same row is flagged
`non-hermetic` and can never hold. The `held` verdict for the new gate therefore
depends on the invocation directory. Either declare `"external": true` on the row
or point the row at a fleet root inside the `--rev` mirror.

**F4 — pre-existing `--rev` fleet-mirror breakage (not round-26).** Two rows fail
under `--rev` both at base and at `a08e85c5` because the mirror represents sibling
lanes as symlinks: `mutate-and-run-regression` (exit 2,
`repo_identity_mismatch` on `kumitate-shokunin`) and `round21-measure-selftest`
(uncaught `CalledProcessError`, `git -C …/fleet/tameshi-shokunin show` → 128).
Recorded for the next round; out of scope for a round-26 fix.

**F5 — the round-25 lesson's own routed item 1 wording now understates the defect.**
`corpus/lessons/round-25-verifier-spotcheck.md:189-192` says the tool has "no
registry row"; after `a08e85c5` it has two rows, but the registry is invalid, so
"has a row" and "the monitor can evaluate" have diverged. The lesson text is the
C2 draft's territory, not this seat's.

## Commands run (all read-only or inside `/tmp`)

```
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/RegistryCheck-reg
cd /tmp/RegistryCheck-reg && python3 tools/registry-check.py --rev a08e85c5d7f899e8a5992e20517edb1a380d79eb
cd /tmp/RegistryCheck-reg && python3 tools/registry-check.py --rev a08e85c5d7f899e8a5992e20517edb1a380d79eb --only mte-interop-selftest
cd /tmp/RegistryCheck-reg && python3 tools/registry-check.py --rev a08e85c5d7f899e8a5992e20517edb1a380d79eb --registry /tmp/RegistryCheck-scratch/registry-fixed.json --json
cd /tmp/RegistryCheck-reg && python3 tools/registry-check.py --rev d4140796f4e48e8ec81b793facba73fbd03b4443 --only mutate-and-run-regression
cd /tmp/RegistryCheck-reg && python3 tools/registry-check.py --rev d4140796f4e48e8ec81b793facba73fbd03b4443 --only round21-measure-selftest
cd /tmp/RegistryCheck-reg && python3 tools/registry-check.py --selftest
cd /tmp/RegistryCheck-reg && python3 .ufo/evidence/round-26/c1-measure.py --repo /tmp/RegistryCheck-reg
cd /tmp/RegistryCheck-reg && python3 .ufo/evidence/round-26/c2-measure.py --repo /tmp/RegistryCheck-reg
```

## Bounds honoured

* No `jj` command was run anywhere (not `jj log`, not `jj st`, not in any clone).
* No git write command (`add`/`commit`/`checkout`/`reset`/`stash`/`push`/`fetch`/`pull`)
  was run in the lane or the fleet repo; the clone was created read-only from the lane.
* The lane and the fleet repo were **read** only; the single file written by this seat
  is this report. The registry correction in E6 exists only as a scratch copy at
  `/tmp/RegistryCheck-scratch/registry-fixed.json` and was passed with `--registry`.
* No gate, selftest or sweep was run inside `/home/vgpnk/Projects/shokunin/tameshi-shokunin`;
  every execution above ran inside `/tmp/RegistryCheck-reg` or a `/tmp` scratch dir.
  `registry-check.py --rev` itself grades a throwaway `mkdtemp` clone, not the lane.
* Sibling lane `kumitate-shokunin` was not modified; only the registry monitor's own
  error text about it was read.
* Tool installs/updates: **none**. `uv 0.13.0` was already present and was used as-is
  (via the two `uv run --no-project --with jsonschema==4.25.1` rows); `python3` and
  `git` are system tools; no `pacman` transaction was performed.

## Risks and blockers

* **Blocker for the round-26 gate**: until `tools/registry.json:1008` and `:1018`
  carry schema-valid `source` strings, `tools/registry-check.py --rev a08e85c5…`
  exits 2 with no row verdicts, and no registry-based operability claim about
  round 26 can be evidenced. This is an L1 (integrator) edit.
* After that edit the registry is not green: 47/49 with `mutate-and-run-regression`
  and `round21-measure-selftest` differing (F4, pre-existing at base). A
  "registry held 47/49" claim is the honest ceiling for this revision.
* F3 makes the new gate row's `held` verdict dependent on the invocation directory;
  it should be settled before the row is relied upon as a hermetic gate.
