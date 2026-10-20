# SpecNoReuse — the `result_reuse=not_established` invariant in the promoted context gate

Round 15, wave 1. Read-only source reconstruction. **No script, gate, selftest, fixture
or subprocess was executed.** No installs or updates. Every claim below is anchored to
bytes read in this workspace; the recipe is a specification, not an observed run.

## Axes moved (godspeed)

| Axis | Move | Bound |
|---|---|---|
| calibration | none | The fixture guards an existing claim-limit invariant; it adds no new claim or case. |
| operability | small, bounded | Supplies one literal token/exit pair and a hermetic fixture for the gate's `--selftest`. |
| depth / coverage / freshness / adjacency | unchanged | No seventh mutation case, no new target surface, no successor sweep, no province change. |

The kept move is deliberately one fixture's assertion set plus retention advice. It is not
a new CLI mode, a new finding class, or a broader environment test.

## Source facts that constrain the answer

Historical file `.ufo/evidence/round-14/capture-context.py`
(SHA-256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`, 647 lines,
unmodified by this seat).

1. `base_receipt()` `:414-436` seeds the receipt with three literal claim-limit fields
   before any observation:
   - `result_reuse = "not_established"`
   - `result_reuse_reason = "content observation + static mapping do not establish environment, dependency, fixture or suite identity"`
   - `not_compared = ["leg execution and kill-rate outcomes", "suite environment and dependencies", "concurrent sibling movement"]`
2. Nothing later writes them. `evaluate()` `:465-551` fills `sources`, `runs`,
   `comparison`, `positive_control`, `mapping`, and `environment`; `decide()` `:553-580`
   reads only `comparison`, `positive_control`, `mapping`, `sources`, `environment`.
   There is **no** predicate, reason string, exit code, or finding ID coupled to
   `result_reuse`.
3. `main()` `:605-643` writes the receipt on every evaluated path whose write
   succeeds: `ok` (exit 0),
   `mismatch` (exit 1), and `invalid_input` (exit 2). `--help` returns 0 at `:607-609`
   without writing a receipt; unexpected arguments return **64** at `:610-613` without a
   receipt. Therefore exit 64 and help cannot observe this field at all.
4. Exit map, `USAGE` `:123`: `exit 0 equal; exit 1 mismatch; exit 2 could-not-evaluate; exit 64 usage.`
5. The printed summary `:637-642` carries `CONTEXT: OK|MISMATCH|INVALID`, `exit=`, and
   `probe-equal=`, `poison-control=`, `runner-mapping=` — **no reuse token is printed**.
6. The historical receipt confirms the values, not just the source
   (`.ufo/evidence/round-14/context-receipt.json`, read via `json.load`):
   `status=ok`, `exit=0`, `result_reuse='not_established'`, the reason above, and the
   three-element `not_compared` list.

### The exact supported pair — and what is not supported

- **Supported stable token:** the receipt field pair
  `"result_reuse": "not_established"` (with the exact reason and list above), observed on a
  passing capture receipt. **Expected exit: `0`** (status `"ok"`), which is the historical
  exit class for a receipt whose declared checks agree.
- **Not supported by the historical source:** any dedicated finding ID, nonzero exit, or
  stdout marker for `result_reuse`. `decide()` never consults it, so a receipt whose field
  was flipped to `"established"` would still exit 0. A fixture that asserts only exit 0
  therefore proves **nothing** about this invariant; the assertion must read the persisted
  receipt.
- **No new ID is to be minted.** Names such as `result_reuse_claimed`,
  `reuse_not_established`, or a `--check-reuse` mode have no basis in the source and are
  outside this correction. The routed defect asks for the context gate's own exits and
  stable IDs; it does not ask for a per-field validation feature. GateClassification.md
  independently says not to add “an expected fixture for every receipt field/finding”.
- Boundedly available secondary anchor (optional, not required): every `invalid_input`
  receipt also carries the three literals because `base_receipt()` runs first. The
  existing stable pair there is `CONTEXT: INVALID (kind=missing_input ...)` + exit **2**
  (kind from `read_lane_bytes` `:145-156`). Duplicating a could-not-evaluate case for this
  field is unnecessary and would widen the selftest for no calibration gain.

## Concrete isolated fixture recipe (one case: ok-path receipt retention)

The recipe exercises the **actual public CLI as a subprocess** on a synthetic lane tree.
It adds no network access, no live-lane read, and no write outside the temporary root.
It assumes the promoted gate keeps the historical six-leg/schema/path contract; wherever
the maintained tool declares a schema constant or input path differently, the fixture
must mirror the tool's own constants rather than fork them.

### Tree (all under `tempfile.TemporaryDirectory()`)

```text
<tmp>/lane/tools/context-capture.py          # byte copy of the maintained tool under test
<tmp>/lane/tools/pin-disposition.py          # synthetic contract stub (below)
<tmp>/lane/tools/mutate-and-run.sh           # synthetic six-leg runner text (below)
<tmp>/lane/.ufo/evidence/round-13/pin-manifest.json
<tmp>/lane/.ufo/evidence/round-13/expected.json
<tmp>/lane/.git/                             # created by `git init <tmp>/lane`
# expected output after the run:
<tmp>/lane/.ufo/evidence/round-15/context-receipt.json
```

The copy-in placement is the zero-new-option route: the tool must resolve
`LANE_ROOT = dirname(dirname(realpath(__file__)))` and
`FLEET_ROOT = dirname(LANE_ROOT)`. The historical four-`dirname` expression at `:45-47`
was correct only for its `.ufo/evidence/round-14/` location; carrying it verbatim to
`tools/context-capture.py` resolves the wrong root and makes every fixture case fail with
`missing_input`/exit 2. If the maintained tool instead exposes one explicit root selector
(e.g. `--root <dir>`), invoke that against `<tmp>/lane` and keep the same tree. One seam
is enough; do not add both plus a separate fixture framework.

### `tools/pin-disposition.py` — hermetic contract stub

The real probe must not run: it reads live repositories. The stub emits a deterministic
six-leg `pin-disposition-v1` document twice, with identical comparable payloads. The
`tool_sha256` self-digest is the value `comparison_block()` cross-checks against the bytes
on disk (`:380-383`); reading its own file inside the temp tree is still hermetic.

```python
#!/usr/bin/env python3
import hashlib, json, os, sys

LEGS = ("js-kimi-census", "bash-surface-census", "bash-tsukuroi-census",
        "bash-mado-verify", "bash-checklist-run", "js-claims-check")

def main(argv):
    with open(os.path.realpath(__file__), "rb") as handle:
        tool_sha = hashlib.sha256(handle.read()).hexdigest()
    document = {
        "schema": "pin-disposition-v1",
        "status": "ok",
        "observed_at": "2000-01-01T00:00:00Z",
        "tool_sha256": tool_sha,
        "legs": [
            {"leg": leg, "content_status": "verified",
             "pinned": {"status": "verified", "sha256": "0" * 64}}
            for leg in LEGS
        ],
    }
    json.dump(document, sys.stdout, sort_keys=True, separators=(",", ":"))
    sys.stdout.write("\n")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

This satisfies every check `comparison_block()` applies at `:352-362`: schema, `status=ok`,
exactly six legs, no `content_status="unavailable"` row, every `pinned.status="verified"`,
and a top-level `observed_at`. Optional strengthening (not required): make `observed_at`
read `os.environ.get("GIT_DIR", "")` so the two runs differ only in the excluded field;
that demonstrates the exclusion is doing work. The base recipe keeps it fixed.

### `tools/mutate-and-run.sh` — synthetic runner text

Leg identities and suffixes must match `EXPECTED_SUFFIX` `:74-81`; values are derived once
and reused verbatim by the manifest, so fixture drift is impossible by construction:

```python
import hashlib
LEGS = [("js-kimi-census", "kumitate-shokunin", "scripts/kimi-census.mjs", "JS"),
        ("bash-surface-census", "shokunin", "tools/surface-census.sh", "BASH"),
        ("bash-tsukuroi-census", "tsukuroi-shokunin", "tools/tsukuroi-census.sh", "TSUKUROI"),
        ("bash-mado-verify", "mado-shokunin", "tools/mado-verify.sh", "MADO"),
        ("bash-checklist-run", "kagi-shokunin", "corpus/checklist-run.sh", "CHECKLIST"),
        ("js-claims-check", "kagi-shokunin", "scripts/claims-check.mjs", "CLAIMS")]
def pin(leg): return hashlib.sha256(("pin:" + leg).encode()).hexdigest()
def rev(leg): return hashlib.sha256(("rev:" + leg).encode()).hexdigest()[:40]
```

Rendered text (blank lines optional). Each `<…>` is a build-time substitution: the
fixture builder writes the computed hex string into the file, never the angle-bracket
expression or quote characters.

```text
# js-kimi-census kumitate-shokunin/scripts/kimi-census.mjs 1/1 (100%)
# bash-surface-census shokunin/tools/surface-census.sh 1/1 (100%)
# bash-tsukuroi-census tsukuroi-shokunin/tools/tsukuroi-census.sh 1/1 (100%)
# bash-mado-verify mado-shokunin/tools/mado-verify.sh 1/1 (100%)
# bash-checklist-run kagi-shokunin/corpus/checklist-run.sh 1/1 (100%)
# js-claims-check kagi-shokunin/scripts/claims-check.mjs 1/1 (100%)

PIN_JS=<sha256("pin:js-kimi-census")>
PIN_BASH=<sha256("pin:bash-surface-census")>
PIN_TSUKUROI=<sha256("pin:bash-tsukuroi-census")>
PIN_MADO=<sha256("pin:bash-mado-verify")>
PIN_CHECKLIST=<sha256("pin:bash-checklist-run")>
PIN_CLAIMS=<sha256("pin:js-claims-check")>

REV_JS=<sha256("rev:js-kimi-census")[:40]>
REV_BASH=<sha256("rev:bash-surface-census")[:40]>
REV_TSUKUROI=<sha256("rev:bash-tsukuroi-census")[:40]>
REV_MADO=<sha256("rev:bash-mado-verify")[:40]>
REV_CHECKLIST=<sha256("rev:bash-checklist-run")[:40]>
REV_CLAIMS=<sha256("rev:js-claims-check")[:40]>

run_regression() {
  regression_case_git js-kimi-census 'kumitate-shokunin/scripts/kimi-census.mjs' "$PIN_JS" "$REV_JS" "case-JS" 'js-kimi-census' "$TABLE_JS"
  regression_case_git bash-surface-census 'shokunin/tools/surface-census.sh' "$PIN_BASH" "$REV_BASH" "case-BASH" 'bash-surface-census' "$TABLE_BASH"
  regression_case_git bash-tsukuroi-census 'tsukuroi-shokunin/tools/tsukuroi-census.sh' "$PIN_TSUKUROI" "$REV_TSUKUROI" "case-TSUKUROI" 'bash-tsukuroi-census' "$TABLE_TSUKUROI"
  regression_case_git bash-mado-verify 'mado-shokunin/tools/mado-verify.sh' "$PIN_MADO" "$REV_MADO" "case-MADO" 'bash-mado-verify' "$TABLE_MADO"
  regression_case_git bash-checklist-run 'kagi-shokunin/corpus/checklist-run.sh' "$PIN_CHECKLIST" "$REV_CHECKLIST" "case-CHECKLIST" 'bash-checklist-run' "$TABLE_CHECKLIST"
  regression_case_git js-claims-check 'kagi-shokunin/scripts/claims-check.mjs' "$PIN_CLAIMS" "$REV_CLAIMS" "case-CLAIMS" 'js-claims-check' "$TABLE_CLAIMS"
}
```

This parses under the maintained mapping semantics: six `HEADER_ROW_RE` rows (`:83-88`),
six unique `PIN_` (64 hex) and `REV_` (40 hex) constants (`:89-90`), and six calls inside a
`run_regression() {` body closed by a line starting `}` (`:103-105`, `:213-257`). Constant
names, manifest values, and manifest order agree, so `mapping.all_match` can be true
(`:259-338`). No other line may match those anchors.

### `.ufo/evidence/round-13/pin-manifest.json`

```json
{
  "schema": "pin-manifest-v1",
  "derived_from": {"path": "tools/mutate-and-run.sh", "sha256": "<sha256 of the runner text above>"},
  "legs": [
    {"leg": "js-kimi-census", "repo": "kumitate-shokunin", "path": "scripts/kimi-census.mjs",
     "pinned_commit": "<REV_JS>", "expected_sha256": "<PIN_JS>"},
    {"leg": "bash-surface-census", "repo": "shokunin", "path": "tools/surface-census.sh",
     "pinned_commit": "<REV_BASH>", "expected_sha256": "<PIN_BASH>"},
    {"leg": "bash-tsukuroi-census", "repo": "tsukuroi-shokunin", "path": "tools/tsukuroi-census.sh",
     "pinned_commit": "<REV_TSUKUROI>", "expected_sha256": "<PIN_TSUKUROI>"},
    {"leg": "bash-mado-verify", "repo": "mado-shokunin", "path": "tools/mado-verify.sh",
     "pinned_commit": "<REV_MADO>", "expected_sha256": "<PIN_MADO>"},
    {"leg": "bash-checklist-run", "repo": "kagi-shokunin", "path": "corpus/checklist-run.sh",
     "pinned_commit": "<REV_CHECKLIST>", "expected_sha256": "<PIN_CHECKLIST>"},
    {"leg": "js-claims-check", "repo": "kagi-shokunin", "path": "scripts/claims-check.mjs",
     "pinned_commit": "<REV_CLAIMS>", "expected_sha256": "<PIN_CLAIMS>"}
  ]
}
```

`validate_manifest()` `:439-462` requires exactly six unique legs with those five nonempty
string fields, 40-hex commits, and 64-hex digests; leg order equals call order.

### `.ufo/evidence/round-13/expected.json`

```json
{"inputs": {"tools/pin-disposition.py": "<sha256 of the written stub bytes>"}}
```

Only this entry is consumed by `evaluate()` (`:465-551`; `inputs` must be an object). If the
promoted tool retains the round-13 paths, this is sufficient; if it moves its declared
input constants, mirror them under the fixture lane.

### Run and assertions

1. `git init <tmp>/lane` with a `GIT_*`-free environment (the tool’s positive control at
   `:395-411` requires `git -C LANE_ROOT rev-parse --git-dir` to work). Writing `.git`
   under the temp root keeps hermeticity.
2. Invoke the **public CLI** as a subprocess, e.g.
   `subprocess.run([sys.executable, "<tmp>/lane/tools/context-capture.py"], cwd="<tmp>/lane", env=child_env)`
   where `child_env` is `os.environ` with every `GIT_*` key removed (the tool’s own
   baseline policy at `:184-187`; an ambient `GIT_DIR` legitimately makes the run exit 1
   with “baseline still carries GIT_DIR” at `:568-569`, which is not the case under test).
   Keep `PATH` so `python3` and `git` resolve. Do not create the tool’s declared poison
   path (`:60-61`); if it exists the tool correctly exits 2 with kind `poison_path_exists`.
3. Assert the literal expected process pair: **exit `0`** and stdout matching the existing
   `CONTEXT: OK (` prefix from `:637-642`. The receipt path inside that line is
   temp-dependent, so assert the prefix/status token, not the full path.
4. Load `<tmp>/lane/.ufo/evidence/round-15/context-receipt.json` and assert literally:
   - `receipt["status"] == "ok"` and `receipt["exit"] == 0`
   - `receipt["result_reuse"] == "not_established"`
   - `receipt["result_reuse_reason"] == "content observation + static mapping do not establish environment, dependency, fixture or suite identity"`
   - `receipt["not_compared"] == ["leg execution and kill-rate outcomes", "suite environment and dependencies", "concurrent sibling movement"]`
5. Assert containment: `receipt["lane_root"] == str(Path("<tmp>/lane").resolve())` and
   `receipt["fleet_root"] == str(Path("<tmp>").resolve())`. This catches the historical
   four-`dirname` root error immediately and confirms the fixture tree, not the live lane,
   is the resolved root for the source's `lane_path()`-relative reads (`:141-143`).
6. Let `TemporaryDirectory` delete the root. No persistent writes, no network, no sibling
   or live-repository reads.

If the selftest prints a line for this case, it is a selftest label, not a gate finding.
A literal phrasing such as `PASS result_reuse=not_established (exit=0)` carries the pair
greppably. **Do not** register `result_reuse` as one of the gate’s finding IDs.

## Advice to ContextGate (bounded)

1. **Retain the three literals verbatim** in the promoted receipt, under whatever round-15
   schema name is chosen: key `result_reuse`, value `"not_established"`, the exact reason
   sentence, and the exact three-element `not_compared` list. A schema-name bump is fine;
   changing the payload token would erase the claim limit the outside review relied on.
2. **Do not derive `result_reuse` from `comparison.equal`.** Equality of the probe’s
   normalized JSON under one `GIT_DIR` injection is not suite, dependency, fixture or
   environment identity; round 14 rejected exactly that inference
   (`corpus/lessons/round-14-verifier-spotcheck.md`, outside item “Infer broad environment
   independence or safe reuse from one GIT_DIR injection” → reject). Flipping the field on
   a green comparison would be a substantive regression, not an implementation choice.
3. **Assert it inside the ok-path fixture that already exists**, not as a new selftest
   case and not as a new CLI mode. It costs four receipt-field comparisons.
4. **If the planned retained-receipt check includes required structure**, these four
   fields belong in that structure because the historical receipt carries them. A mutated
   field may be rejected with the checker’s generic mismatch class, but this seat
   recommends **not** making such a negative fixture mandatory and **not** minting a
   `result_reuse`-specific finding ID. No historical ID or nonzero exit exists to inherit.
5. **Root resolution is implementation-critical.** Use
   `LANE_ROOT = dirname(dirname(realpath(__file__)))` for `tools/context-capture.py` (or
   one explicit root option) and route every read, the positive-control cwd, and the output
   path through it. Otherwise the fixture copy resolves the wrong lane root, and the
   standalone selftest can never be hermetic.
6. **Keep prospective output round-15-only.** The fixture expects
   `.ufo/evidence/round-15/context-receipt.json`; the historical round-14 receipt and script
   bytes stay untouched.

## Explicit non-goals (rejections)

- No claim that the fixture establishes environment independence, dependency identity, or
  safe reuse. It asserts a recorded limit, not its truth.
- No new broad validation feature, no `--verify-reuse`, no seventh mutation case, no extra
  exit code, no new finding token.
- No negative fixture that flips `result_reuse` and requires a bespoke ID.
- No execution, rerun, or repair of the historical round-14 artifact or receipt.
- No successor sweep, source acquisition, or axis promotion claim.

## Risks and limits

- The recipe is source-derived, not executed. Its correctness depends on the promoted tool
  retaining the six-leg parser, schema constants, and receipt field names documented here;
  if ContextGate changes them, the fixture must follow the tool’s declared constants, and
  the literal `result_reuse` payload values must still remain identical.
- `git` and `python3` are host prerequisites of the historical tool (`:517-525`); the
  fixture does not sandbox them, only its data. That is within the existing command’s
  contract and is not an environment-identity claim.
- The declared poison path must remain absent on the host. Creating it would turn the ok
  fixture into a legitimate exit-2 `poison_path_exists` case, not a fixture failure.
- Assertion 5 depends on `lane_root`/`fleet_root` being persisted; the historical receipt
  records both (`base_receipt()` `:419`), so this is an existing structural field, not
  a new requirement.

## Evidence used

- Read (unmodified): `.ufo/evidence/round-14/capture-context.py` (full relevant functions:
  constants `:45-108`, parser `:213-257`, mapping `:259-338`, comparison `:350-393`,
  control `:395-411`, `base_receipt` `:414-436`, `evaluate` `:465-551`, `decide`
  `:553-580`, `write_receipt` `:583-602`, `main` `:605-643`), SHA-256
  `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`.
- Read: `.ufo/evidence/round-14/context-receipt.json` via `json.load`; confirmed
  `status=ok`, `exit=0`, and the exact three claim-limit values.
- Read: `corpus/lessons/round-14-verifier-spotcheck.md` (Routed defects 5 and the reuse
  rejection row); `corpus/lessons/round-15.md` (Gate admit/reject criteria);
  `.ufo/waves/round-15/w1/GateClassification.md`; `.ufo/waves/round-15/w1/ReconEnvironment.md`.
- Tool installs/updates: none. No pacman, uv, npm, cargo, or binary install was run.
- No LSP device is mounted in this session; source-level text was the fallback, as in the
  sibling gate report.
