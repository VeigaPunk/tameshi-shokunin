# SpecHistorical — round14 script and receipts immutable (round15 w1)

Seat: `TameshiR15.SpecHistorical` (leaf executor). Report only; no source edit,
no gate/selftest/script execution, no tool install or update.

## Scope and method

Read-only inspection of committed working-tree bytes: the historical
`.ufo/evidence/round-14/capture-context.py` (647 lines, 27,781 B, mode 755),
retained `.ufo/evidence/round-14/context-receipt.json` (424 lines, 29,492 B,
mode 644), `round-14/guardrails.json`, `round-14/context-missing-env.json`,
current `SKILL.md` round-14 registry rows (1596–1607), the round-14 verifier
spot-check Routed defect 5, and `.ufo/evidence/round-15/claims.json`.
Commands used were only `sha256sum`, `stat`, `find|sha256sum`, and file reads.
No gate, probe, runner, selftest or historical script was invoked. New tool
`tools/context-capture.py` did not exist at read time, so no review of it is
possible here.

## Observed anchors (2026-10-20 read; timestamped, not standing claims)

| Object | sha256 | Size |
|---|---|---:|
| `.ufo/evidence/round-14/capture-context.py` | `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89` | 27,781 B |
| `.ufo/evidence/round-14/context-receipt.json` | `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` | 29,492 B |
| `.ufo/evidence/round-14/guardrails.json` | `cca670b54f5da70873daec8d1bd54749ea63be99582f21138d43c8c715eaf784` | — |
| `.ufo/evidence/round-14/context-missing-env.json` | `1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208` | — |

Directory manifests (sorted path+digest listing hashed once): round-12
`562` files `97b0ec155dc0912f3915338e17c5012cf4034e0ba62123cc61c91d2d6640e918`;
round-13 `16` files `92dfe2e032cee8dcb31780c34aba635800be9cdf67d87b7c674f65d3cdbfa3bc`;
round-14 `21` files `3458f5b0b48dbb662132183b69eb0535176b34798008437baddba1449281891b`.

The retained receipt records `"tool_sha256": "7313e9a2…7d89"`, identical to the
current on-disk script digest. Within this read, the bytes that produced the
retained receipt are the bytes now on disk; the receipt is self-bound to its
producer. Receipt terminal keys are `"status": "ok"`, `"exit": 0`,
`"reasons": []`.

## Source facts that bound the immutability claim

Line anchors in the historical script:

- `44–52` — `VERSION`, `SELF = os.path.realpath(__file__)`,
  `LANE_ROOT = dirname(dirname(dirname(dirname(SELF))))`, `FLEET_ROOT`,
  receipt/mapping/probe/manifest schema literals. `RECEIPT_SCHEMA` is
  `"tameshi-round14-context-receipt-v1"`.
- `53–58` — fixed input paths plus `OUTPUT_REL =
  ".ufo/evidence/round-14/context-receipt.json"`.
- `141–155` — `lane_path`/`read_lane_bytes`: reads resolve under `LANE_ROOT`;
  missing file raises `InvalidContext("missing_input", …)`.
- `414–417` — `base_receipt` opens `SELF` read-only solely to record
  `tool_sha256`.
- `583–603` — **sole write path**: `write_receipt` uses exactly `OUTPUT_REL`,
  `os.makedirs` on its parent, `mkstemp` in that directory, fsync,
  `chmod(0o644)`, `os.replace`, temporary unlink on failure. No other function
  opens a path for writing.
- `605–613` — any argv except `-h/--help` writes
  `capture-context.py: unexpected argument(s): …` plus `USAGE` to stderr and
  returns `64` **before** `base_receipt`/`write_receipt`; no receipt exists.
- `614–628` — `InvalidContext` writes a receipt with `status:"invalid_input"`,
  `exit:2`, `error.kind`; if that write fails, exit `2` with stderr only.
- `629–643` — `decide` returns `("mismatch",1,reasons)` on any failed
  predicate else `("ok",0,[])`; the success line is
  `CONTEXT: OK (receipt=<path> exit=0 probe-equal=True poison-control=True runner-mapping=True)`.

The retained receipt confirms every `decide()` conjunct passed: `comparison.equal
= true`, `payload_tool_sha256_matches_disk = true`,
`environment.env_delta_matches_declared = true`, `baseline_has_GIT_DIR = false`,
`positive_control.effective = true` (baseline git exit 0 `.git`; injected git
exit 128 `fatal: not a git repository: '/nonexistent/tameshi-round14-poison'`),
both `sources.*.matches_* = true`, `mapping.all_match = true`, six legs each
with five true checks.

Historical immutability is therefore **structural**: one fixed output path,
read-only inputs, no argv-selected target, and a 64 path that cannot write.
`guardrails.json` supplies the existing external integrity check
`historical_integrity` (`git diff --exit-code d6809df… -- .ufo/evidence/round-12
.ufo/evidence/round-13 tools/…`), observed exit 0 at round-14; it does not yet
cover `.ufo/evidence/round-14`.

## Exact existing stable token and expected exit

| Observable | Existing exact token | Where | Expected exit | Supported? |
|---|---|---|---|---|
| Retained round14 receipt identity | `"schema":"tameshi-round14-context-receipt-v1"` + `"status":"ok"` + `"exit":0` | script 49; receipt tail | `0` | Yes — historical, exact |
| Historical byte integrity | check name `historical_integrity` | `round-14/guardrails.json` | `0` (`git diff --exit-code`) | Yes, but external and live-root; not tool-emitted |
| Usage cannot select another output | stderr substring `unexpected argument(s)`; no receipt | script 605–613 | `64` | Yes — historical, exact |
| Immutability-violation finding | **none exists** | — | — | **No** — do not invent one |

No historical production finding ID covers "historical bytes changed". The
historical tool never reads the round-14 script or receipt, so changing them
cannot produce a gate verdict. The immutability fixture must therefore assert
**byte-digest equality inside the selftest harness**, not a new gate finding.
The only stable production tokens this lane can pin are the receipt
schema/status/exit and the 64 stderr substring above.

## Concrete isolated fixture recipe — `historical-bytes-immutable`

Purpose: prove the promoted `tools/context-capture.py`, in both its retained
check and prospective capture modes, never rewrites or executes the round-14
script/receipt and writes only under `.ufo/evidence/round-15/`.

Isolation and literal fixture bytes (stdlib only; no live lane read, no
network, no sibling tree):

```python
scratch = tempfile.mkdtemp(prefix="tameshi-r15-context-capture-selftest.", dir="/tmp")
lane = os.path.join(scratch, "lane")
hist = os.path.join(lane, ".ufo", "evidence", "round-14")
os.makedirs(hist)

SCRIPT_BYTES = (b"#!/usr/bin/env python3\n"
                b"# round-14 historical script fixture: never executed\n"
                b"open('EXECUTED','w').write('executed')\n")
RECEIPT_BYTES = json.dumps({
    "schema": "tameshi-round14-context-receipt-v1",
    "tool": "capture-context.py r14 (fixture)",
    "tool_sha256": hashlib.sha256(SCRIPT_BYTES).hexdigest(),
    "observed_at": "2026-01-01T00:00:00Z",
    "status": "ok", "exit": 0, "reasons": [],
    "environment": {"injected_env": {"GIT_DIR": "/nonexistent/tameshi-round14-poison"},
                    "env_delta_keys": ["GIT_DIR"],
                    "env_delta_matches_declared": True,
                    "baseline_has_GIT_DIR": False,
                    "poison_path_exists": False, "ambient_env_dumped": False},
    "comparison": {"equal": True, "payload_tool_sha256_matches_disk": True,
                   "raw_stdout_equal": True},
    "positive_control": {"effective": True},
    "sources": {"probe": {"matches_declared": True},
                "runner": {"matches_manifest_declaration": True}},
    "mapping": {"all_match": True},
    "result_reuse": "not_established",
}, indent=2, sort_keys=True).encode() + b"\n"
```

Write both files, then take `seal = {rel: sha256(bytes)}` over every file under
`hist`. The synthetic receipt binds `tool_sha256` to the synthetic script,
mirroring the real historical binding without copying live bytes.

Cases (each invokes the public CLI as a subprocess with `sys.executable`, `SELF`,
`cwd=scratch`, `capture_output=True`, `timeout=60`; never import internals):

1. **`historical-bytes-immutable` (retained check)** —
   `[SELF, "--check-receipt", receipt_path, "--root", lane]` (use the promoted
   check flag exactly as registered). Expected literal exit **`0`**; parsed
   stdout, if JSON, must report the receipt's own `schema`/`status:"ok"`/`exit:0`
   unchanged. Then assert all of:
   - `sha256(script_bytes) == seal[script]` and same for the receipt;
   - `not os.path.exists(os.path.join(lane, "EXECUTED"))` (historical script
     never executed);
   - the file set under `lane` is byte-for-byte the two sealed files — the
     check mode adds nothing and rewrites nothing.
2. **`historical-bytes-immutable-capture` (composed with SpecClean's clean
   fixture)** — build the clean synthetic lane from the clean-capture recipe,
   add the same two sealed round-14 files, run the default prospective capture
   with `--root lane`. Expected literal exit **`0`**; assert both seals
   unchanged, no `EXECUTED` marker, and exactly one new file:
   `lane/.ufo/evidence/round-15/context-receipt.json`. No path under
   `.ufo/evidence/round-14/` may appear in the before/after delta.
3. **`historical-bytes-usage`** — `[SELF, "--overwrite", receipt_path]`.
   Expected literal exit **`64`**; stderr contains `unexpected argument(s)`;
   both seals unchanged and no new file anywhere under `lane`. This pins the
   existing 64 semantics from script 605–613, not a new feature.
4. **Not required by this lane** — a byte-flipped *copy* of the sealed receipt
   expecting exit `2` and a snapshot-tamper ID belongs to SpecTamper and only
   if ContextGate implements a digest-pinned snapshot mode. Historical source
   has no such token; do not make it a mandatory admission case here.

Failure detail must state the case name and the observed/expected exit and
digest role, following the existing `SELFTEST_CASE <name> PASS|FAIL (<detail>)`
convention (`tools/evidence-disposition.py:1518–1524`). The case's expected
exit is a literal, and the immutability assertion is the digest comparison, not
a production finding ID.

## Bounded recommendations to ContextGate (via TameshiR15)

1. **Correct the lane-root derivation before copying path constants.**
   Historical `LANE_ROOT = dirname⁴(SELF)` is correct only at
   `.ufo/evidence/round-14/capture-context.py` (script 45–47). At
   `tools/context-capture.py`, four dirnames resolve to
   `/home/vgpnk/Projects` and `FLEET_ROOT` to `/home/vgpnk`; every
   `lane_path` read then misses and `write_receipt`'s `makedirs` could create
   paths outside the lane. Two dirnames (`parents[1]`) are correct for
   `tools/`, but the hermetic selftest still needs an explicit synthetic root.
   Therefore: add explicit `--root` for check and capture, default to
   `Path(__file__).resolve().parents[1]`, require `os.path.isdir(root)`, and
   build the output strictly as
   `root/.ufo/evidence/round-15/context-receipt.json`. Never accept an output
   path argument.
2. **Keep the round-14 files read-only data.** The retained-receipt check must
   not compare `receipt.tool_sha256` (a historical producer digest,
   `7313e9a2…7d89`) against the new tool's digest, must not require historical
   `lane_root`/`fleet_root` absolute strings to equal the current root, and must
   not execute or re-derive embedded `runs.*.argv`/`stdout`. Check the recorded
   `decide()` booleans, structure and `status ↔ exit` consistency only.
3. **Preserve `decide`/`comparison`/`mapping` semantics exactly.** Exit 0 still
   requires `comparison.equal`, `payload_tool_sha256_matches_disk` (of the probe
   payload in a fresh capture), exact `env_delta_keys == ["GIT_DIR"]`,
   `baseline_has_GIT_DIR == false`, `positive_control.effective`, both source
   digest matches and `mapping.all_match`; any failure is exit 1 with the
   existing free-text reasons. Exit 2 remains `InvalidContext`/input problems;
   exit 64 remains argv rejection with no receipt. Do not convert these into a
   new generic finding framework.
4. **Selftest must never invoke `.ufo/evidence/round-14/capture-context.py`.**
   That script performs live reads, runs the probe and git, and writes a
   round-14 receipt. Embedding literal fixture bytes (above) is the only
   hermetic form.
5. **Do not add a production "history changed" finding.** The minimum fix is
   the sealed-fixture case plus the existing `historical_integrity` runbook
   check; anything broader is unearned by this round's evidence.

## L1 runbook check for the real lane (not part of selftest)

Extend the existing `historical_integrity` pattern to the round-14 directory
under the round-15 baseline `a9cf4da78f2514c7bedd91a850a88590009d7df0`:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --exit-code \
  a9cf4da78f2514c7bedd91a850a88590009d7df0 -- \
  .ufo/evidence/round-12 .ufo/evidence/round-13 .ufo/evidence/round-14
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --porcelain -- \
  .ufo/evidence/round-12 .ufo/evidence/round-13 .ufo/evidence/round-14
```

Expected: exit `0` and empty porcelain (the second covers untracked files the
first cannot see). The observed 2026-10-20 anchors at top are the byte-level
reference if a digest mismatch appears.

## Risks, limits, blockers

- `tools/context-capture.py` did not exist when read, so its actual flags,
  output schema and check predicates are unobservable here; the recipe names
  `--check-receipt`/`--root` as shape, not as an established contract. Registry
  must pin the final names.
- The synthetic fixture cannot detect a write **outside** `scratch`; that is
  why the root-containment defect in recommendation 1 must be fixed
  structurally. The selftest can only assert synthetic-root containment and
  recorded `lane_root`.
- The retained round14 receipt contains absolute live paths; the fixture must
  use synthetic bytes and not copy it, or the selftest reads the live lane.
- `historical_integrity` in `guardrails.json` predates round-14 creation and
  does not cover `.ufo/evidence/round-14`; the runbook command above is the
  bounded extension, not a claim that the old check already covered it.
- No source edit was made and no check was executed by this seat. No tool was
  installed or updated.
