# SpecUnavailable — missing source input / missing receipt: the exit-2 could-not-evaluate class

Seat: executor, leaf, report-only. No source edits, no gate/selftest execution, no builds, no commits. LSP is not mounted (`read xd://lsp` returned `No such tool: xd://lsp`); navigation used direct file reads and `grep`, recorded as actual unavailability rather than an empty semantic result. Every source claim below is bounded to the committed historical bytes named in the evidence anchors.

## Verdict (bounded pair)

| Case | Existing stable token | Envelope | Expected exit | Grounding |
|---|---|---|---|---|
| Required **source input absent** (capture mode) | `missing_input` | receipt `status: "invalid_input"`, `exit: 2`, `error.kind: "missing_input"` | **2** | historical source |
| Required **retained receipt absent** (check mode) | `missing_input` (reuse; historical source has no check mode) | same `invalid_input`/`error.kind` finding channel | **2** | interface-required; token reused |

The historical source has exactly one token for an absent required file: `InvalidContext("missing_input", "missing lane file: " + rel)` at `.ufo/evidence/round-14/capture-context.py:150`, raised from `read_lane_bytes` (`:145-155`). `main()` maps every `InvalidContext` to status `"invalid_input"`, receipt field `"exit": 2`, `error.kind`, `reasons[0] = kind + ": " + message`; it writes the receipt, prints `CONTEXT: INVALID (kind=<kind> receipt=<path> exit=2)`, and returns 2 (`:615-629`). The module docstring (`:26-30`) and USAGE (`:123`) both define exit 2 as could-not-evaluate for missing/unparsable input. So `missing_input` + exit 2 is the **existing** stable pair; no new token is needed for an absent source.

For a missing checked receipt the new gate has no historical precedent, but the same absence semantics apply: it is a missing required input, not a mismatch. Reuse `missing_input`; do **not** invent `missing_receipt`. A second token for the same class must be registry-declared and pinned and buys no discrimination the exit map does not already carry. A wrong digest on an *existing* snapshot is the distinct `snapshot_tampered` token (exit 2) owned by SpecTamper; an existing but malformed input is `invalid_json` (SpecJSON); an existing but OS-unreadable input is `unreadable_input` (`:152-155`).

## Fixture F1 — missing source input (capture mode)

Isolated construction, one `mkdtemp` root `T`; fleet root is `T`, lane root is `T/lane`:

```python
T = tempfile.mkdtemp(prefix="cc-r15-selftest-missing-input-")
lane = Path(T) / "lane"
(lane / "tools").mkdir(parents=True)
(lane / ".ufo/evidence/round-13").mkdir(parents=True)
# Present every input the gate reads BEFORE the omitted one. Bytes need not be
# valid: the first missing read aborts before parsing.
(lane / "tools/mutate-and-run.sh").write_bytes(b"")
(lane / ".ufo/evidence/round-13/pin-manifest.json").write_bytes(b"{}\n")
(lane / ".ufo/evidence/round-13/expected.json").write_bytes(b"{}\n")
# tools/pin-disposition.py deliberately absent
```

Invocation (public CLI, child process, fixture cwd, minimal env, stdin closed, bounded timeout):

```python
p = subprocess.run(
    [sys.executable, "-I", str(Path(__file__).resolve()),  # the copy under test
     "--lane-root", str(lane)],                            # gate's documented root flag
    cwd=lane, env={"PATH": "/usr/bin:/bin", "LC_ALL": "C", "HOME": str(Path(T) / "home")},
    stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30,
)
```

Literal assertions (pin the token and exit, not a prefix or substring alone):

```python
assert p.returncode == 2
assert p.stdout.decode() == (
    "CONTEXT: INVALID (kind=missing_input receipt="
    ".ufo/evidence/round-15/context-receipt.json exit=2)\n")
r = json.loads((lane / ".ufo/evidence/round-15/context-receipt.json").read_text())
assert r["status"] == "invalid_input"
assert type(r["exit"]) is int and r["exit"] == 2
assert r["error"]["kind"] == "missing_input"
assert r["error"]["message"] == "missing lane file: tools/pin-disposition.py"
assert r["reasons"] == ["missing_input: missing lane file: tools/pin-disposition.py"]
assert "Traceback" not in p.stderr.decode()
assert os.path.commonpath([T, os.path.realpath(lane / ".ufo/evidence/round-15")]) == T
```

Adapter points, not relaxations: substitute the gate's declared round-15 receipt path and schema in the equality assertion; use the gate's documented root flag name. Keep the `missing_input` + exit-2 pair exact. The message path (`tools/pin-disposition.py`) is an **optional second pin** valid only if the promoted gate keeps the historical read order `probe, runner, manifest, expected` (`:476-479`); if it reorders, pin whichever input its contract documents first. Do not weaken the message assertion to a bare `missing_input` prefix while claiming determinism.

Why this isolates the class: `evaluate()` reads the four inputs in fixed order and raises on the first absent one, before JSON parsing, mapping, `shutil.which`, probe subprocesses, or any Git/network action (`:476-517`). A missing input therefore needs no valid manifest/runner/expected bytes and stays hermetic.

### Ordering trap that breaks token determinism

`evaluate()` checks the poison path (`:469-472`) and the fleet-root directory (`:473-474`) **before** reading inputs. If the promoted gate keeps a host-absolute poison path (historical `/nonexistent/tameshi-round14-poison`), a contaminated host makes the first failure `poison_path_exists` — still exit 2, but the wrong token, so the literal pair fails. Make F1's first failure reproducible by construction, cheapest first:

1. derive the round-15 poison path inside the fixture root (guaranteed absent), or
2. check required-input existence before the poison/fleet-root preconditions.

Do not "fix" this by accepting any exit-2 token: that would flatten `missing_input`, `poison_path_exists`, `invalid_fleet_root`, `snapshot_tampered`, and `invalid_json` into one class and defeat the routed requirement for literal expected exits and IDs.

### Non-substitutes for "missing"

- Directory at the input path → `IsADirectoryError` (an `OSError`) → `unreadable_input`, not `missing_input`.
- `chmod 000` → `EACCES` → `unreadable_input`, and is ineffective under root.
- Empty file → read succeeds; parse fails later as `invalid_json` (SpecJSON's class).
- Broken/dangling symlink → `ENOENT` → `missing_input`, but a plainly absent path is clearer evidence.
- Missing CLI argument → exit 64 with no receipt (`:606-613`), SpecUsage's class, not this one.

Capture mode writes the invalid receipt even on failure (`:620`), so the fixture root override is mandatory; without it a selftest invoking the real `tools/context-capture.py` would write into the live lane.

## Fixture F2 — missing retained receipt (check mode)

The historical bytes have no receipt-check mode; the round-15 interface requires one. Implementation-critical ordering: the check path must resolve/read the retained receipt **first**, before lane inputs or digest/predicate validation, so this fixture needs no synthetic lane tree and its token cannot be masked by an earlier `invalid_*` error.

```python
T = tempfile.mkdtemp(prefix="cc-r15-selftest-missing-receipt-")
absent = Path(T) / "absent-context-receipt.json"   # never created
p = subprocess.run(
    [sys.executable, "-I", str(Path(__file__).resolve()),
     "--check", str(absent)],                      # gate's documented check flag/positional
    cwd=T, env={"PATH": "/usr/bin:/bin", "LC_ALL": "C", "HOME": str(Path(T) / "home")},
    stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30,
)
```

Assertions:

```python
assert p.returncode == 2
payload = json.loads(p.stdout)          # if the check CLI emits JSON; otherwise use the line token
assert payload["status"] == "invalid_input"
assert payload["exit"] == 2 and type(payload["exit"]) is int
assert payload["error"]["kind"] == "missing_input"
assert "Traceback" not in p.stderr.decode()
assert not absent.exists()
# pre/post walk of T: check mode is read-only, no new files
```

If the check CLI's finding channel is a single text line, assert the literal `missing_input` token there instead of JSON. Either way the pair is `missing_input` + exit 2; process exit alone is exit-only adjudication and is insufficient. A missing *argument* remains 64 (SpecUsage), so F2 must pass an explicit absent path. A wrong digest on an existing receipt is `snapshot_tampered` (SpecTamper) and must not be able to satisfy F2.

## Boundary with the adjacent exit-2 and exit-64 classes

| Class | Token | Fixture owner | Distinguishing fact |
|---|---|---|---|
| Absent source input | `missing_input` | this seat | required file does not exist |
| Absent retained receipt | `missing_input` (reused) | this seat | receipt path does not exist |
| Existing snapshot, wrong digest | `snapshot_tampered` | SpecTamper | file exists, bytes differ |
| Existing malformed JSON / duplicate key | `invalid_json` | SpecJSON | file exists, parse fails |
| Existing unreadable file | `unreadable_input` | (unassigned by name; keep distinct) | file exists, open fails |
| Poison path present | `poison_path_exists` | SpecControl adjacency | GIT_DIR target exists |
| Missing/unexpected CLI argument | usage, 64 | SpecUsage | no receipt written |

## What not to build (scope restraint)

No generic preflight that enumerates and validates every declared input, no new `missing_receipt`/`missing_source` taxonomy, no fixture per receipt field, and no broader environment/validation claim. This defect needs two public-CLI cases, one reused historical token (`missing_input`), and exact exit 2. The round-14 routed item explicitly excludes requiring a fixture for every emitted ID.

## Evidence anchors (committed bytes, read-only)

- `.ufo/evidence/round-14/capture-context.py:26-30` — exit map: 2 = could-not-evaluate (missing/unparsable input).
- `.ufo/evidence/round-14/capture-context.py:123` — USAGE: exit 2 could-not-evaluate; exit 64 usage.
- `.ufo/evidence/round-14/capture-context.py:145-155` — `read_lane_bytes`: `FileNotFoundError` → `missing_input`; other `OSError` → `unreadable_input`.
- `.ufo/evidence/round-14/capture-context.py:469-479` — poison path and fleet-root preconditions precede the fixed-order input reads.
- `.ufo/evidence/round-14/capture-context.py:605-613` — help 0; any other argument exits 64 without a receipt.
- `.ufo/evidence/round-14/capture-context.py:615-629` — `InvalidContext` → `status=invalid_input`, `exit=2`, `error.kind`, `reasons`, receipt write, literal `CONTEXT: INVALID (kind=… receipt=… exit=2)`, return 2.
- `.ufo/evidence/round-14/capture-context.py:583-600` — atomic receipt write at the lane-relative output path.
- `corpus/lessons/round-14-verifier-spotcheck.md`, Routed defects item 5 — gate classification, standalone isolated self-invocation with literal exits and stable IDs, explicit 64; scope excludes a fixture per emitted ID.

## Method, limits, and checks for L1

No script, selftest, gate, build, or formatter was executed; the literal stdout line is computed from the format string at `:627` plus the token at `:150` and is labeled `[INFERENCE]` as an executed observation (the format itself is read directly). Tool installs/updates: none. The check-mode contract is the round-15 interface requirement, not historical behavior; ContextGate owns the final flag names and output schema. This report is advisory source reconstruction, not an independent admission decision.

After the gate lands, L1 should run once:

1. `python3 tools/context-capture.py --selftest` — exit 0; the summary enumerates both missing-input cases, each asserting the literal `missing_input` token and exit 2 (plus the receipt `status`/`error.kind` for capture mode).
2. The selftest must create only under its temp roots; no fixture may point the lane root at the real checkout (SpecHermetic owns the wider no-live-roots check).
3. One manual public-CLI check against a fresh absent receipt path — exit 2 and `missing_input`, no file created.
