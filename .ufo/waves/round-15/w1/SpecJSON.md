# SpecJSON — malformed JSON and duplicate keys: fixture recipe, token, expected exit

Seat: `TameshiR15.SpecJSON` (executor, leaf). Assignment: read the historical
`capture-context.py` JSON functions and draft **only** a concrete isolated
fixture recipe for malformed JSON and duplicate keys, naming the exact existing
stable token and expected exit where the source supports it. No source edits.

Evidence basis: source reads of `.ufo/evidence/round-14/capture-context.py`
(647 lines; sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`,
matching the retained receipt's `tool_sha256`), the round-14 routed defect 5
(`corpus/lessons/round-14-verifier-spotcheck.md:160`), the round-15 spec
(`.ufo/waves/round-15/spec1.json`), and the sibling-established check-mode
spelling in `.ufo/waves/round-15/w1/SpecTamper.md:53-57`. **Nothing was
executed**: no gate, selftest, fixture, historical script or runner. No tool
installed or updated. LSP was unavailable — `read xd://lsp` is not mounted in
this session — so all claims are text-anchored source reads, not semantic LSP
evidence. `tools/context-capture.py` does not exist yet at this revision; the
recipe below is a contract for it.

## 1. Verdict

**Supported, with one shared existing token and exit: `invalid_json` → exit 2.**

Both assigned classes already exist in the historical source and land in the
same stable kind:

| Input class | Kind token | Detail string | Process exit |
|---|---|---|---|
| syntactically malformed JSON | `invalid_json` | `<label> is not valid JSON: line L column C` | 2 |
| duplicate key, any depth | `invalid_json` | `duplicate JSON key '<key>'` | 2 |
| root not an object | `invalid_json` | `<label> root is not an object` | 2 (SpecTypes' class, see §7) |

Malformed and duplicate-key inputs are therefore **not distinguishable by
token**. The historical source never distinguishes them and there is no second
token to reuse; inventing `duplicate_json_key` would be a new vocabulary and is
not required by the routed defect. The fixture pair still discriminates real
implementation faults (§5), because in the historical source `invalid_json` is
reachable *only* through `parse_json` (`:162`, `:177`, `:180`); every other
invalid-input class — manifest and expected structure included — uses its own
kind (`invalid_manifest`, `invalid_expected`, …). The promoted check mode must
preserve that separation by not collapsing a parse failure into a
structure/schema kind.

Exit 2 is the source's own could-not-evaluate class (`:123`), and the historical
invalid-input path returns 2 (`:628`). Exit 1 is **not** correct here: `decide()`
reserves 1 for an evaluated observation mismatch (`:553-580`), and unparsable
bytes are not an observation.

Target surface: the **retained-receipt check mode** of the promoted
`tools/context-capture.py`, never the historical capture path. Capture mode
reads the round-13 expected file and pin manifest, needs the six-leg runner,
probe and live git control, and its invalid-input branch writes
`.ufo/evidence/round-14/context-receipt.json` (`:58`, `:583-601`, `:621-626`) —
not isolatable and not allowed to overwrite round-14 evidence.

## 2. Exact anchors

| Claim | Anchor |
|---|---|
| Stable kind constructor: `InvalidContext(kind, message)` | `capture-context.py:127-131` |
| Duplicate-key hook raises `InvalidContext("invalid_json", "duplicate JSON key " + repr(key))` | `capture-context.py:158-165` (raise at `:162`) |
| Hook is installed on the parser: `json.loads(text, object_pairs_hook=_no_duplicate_keys)` | `capture-context.py:173` |
| Malformed JSON → `InvalidContext("invalid_json", "<label> is not valid JSON: line L column C")` | `capture-context.py:174-178` |
| Root-not-object → `invalid_json` | `capture-context.py:179-180` |
| `parse_json` catches only `json.JSONDecodeError`; the hook's `InvalidContext` propagates unchanged | `capture-context.py:172-178` |
| Historical parse call sites (manifest, expected) — no receipt parse exists yet | `capture-context.py:487-488` |
| Invalid input → status `invalid_input`, `error.kind`, exit 2; stdout `CONTEXT: INVALID (kind=<kind> ... exit=2)` | `capture-context.py:617-628` (print at `:627`) |
| Declared exit map: `0 equal; 1 mismatch; 2 could-not-evaluate; 64 usage` | `capture-context.py:123`, `:2-31` |
| `decide()` owns exit 1 for failed comparison/control/source-pin/mapping predicates | `capture-context.py:553-580` |
| Historical receipt pins the historical tool digest `7313e9a2…` | `.ufo/evidence/round-14/context-receipt.json` `tool_sha256` |
| Check-mode spelling precedent | `.ufo/waves/round-15/w1/SpecTamper.md:53-57` (`--check-receipt RECEIPT --pins PINS` or `--check-snapshot DIR`) |

Consequence for ordering: a malformed receipt can only produce `invalid_json`
if the check mode **parses caller-supplied bytes before** any pin/containment/
structure comparison. If the tool validates the receipt path, the digest pin, or
required keys first, the fixture would yield `path_rejected`,
`input_digest_mismatch` or an `invalid_manifest`-class kind instead, and this
class would be untestable. Parse order is part of the contract.

## 3. Fixture recipe

Scratch root (hermetic, temp-only; removed on pass, kept on failure — the
`tools/repeat-control.py:597,859` and `tools/evidence-disposition.py:1512,1855`
convention):

```python
scratch = tempfile.mkdtemp(prefix="tameshi-r15-context-selftest.", dir="/tmp")
```

Fixtures are **raw bytes written by the selftest**, not committed files. Never
place a malformed fixture under a tracked evidence directory, and never point
the check at `.ufo/evidence/round-14/context-receipt.json`.

### 3.1 Literal fixture bytes

```python
FIXTURES = {
    # J1: truncated object — syntactic failure at EOF (JSONDecodeError path)
    "receipt-json-malformed-truncated": (
        b'{"schema": "tameshi-round14-context-receipt-v1",\n'
    ),
    # J2: complete object plus trailing bytes — "Extra data" (strict-parser arm)
    "receipt-json-malformed-trailing-data": (
        b'{"schema": "tameshi-round14-context-receipt-v1"}\n}\n'
    ),
    # J3: top-level duplicate of the real schema key (hook arm)
    "receipt-json-duplicate-key-top": (
        b'{"schema": "tameshi-round14-context-receipt-v1", '
        b'"schema": "tameshi-round14-context-receipt-v1"}\n'
    ),
    # J4: duplicate nested under comparison (recursion arm)
    "receipt-json-duplicate-key-nested": (
        b'{"schema": "tameshi-round14-context-receipt-v1", '
        b'"comparison": {"equal": false, "equal": true}}\n'
    ),
}
```

All four are valid UTF-8 and contain no BOM, so they exercise the JSON path and
not `invalid_utf8` (`:169-171`). Keys are the real receipt keys where possible,
so a lenient parser reaches *plausible* structure and the token difference is
meaningful.

Optional minimal arm, only if the check CLI exposes the detail string:
`b'{"a": 1, "a": 2}\n'` with expected detail `duplicate JSON key 'a'`
(`repr` of a string key yields single quotes).

### 3.2 Invocation

Preferred pair mode (matches `SpecTamper`'s recommendation):

```
[sys.executable, SELF, "--check-receipt", fixture_path]
```

Omit `--pins`; the receipt is the only input under test. If ContextGate instead
implements `--check-snapshot DIR`, place each fixture at
`<snapshot>/receipt.json` and compute the snapshot manifest's listed digest
**over the exact malformed bytes**. The digest must match so that the digest
gate passes and the JSON parse is the failing predicate; a stale digest would
surface `snapshot_tampered`/exit 2 and silently mask this class.

If the check mode enforces lane containment on the receipt path, use a temp
lane instead of an absolute path — still hermetic:

```
[sys.executable, SELF, "--root", str(scratch / "lane"),
 "--check-receipt", ".ufo/evidence/round-15/context-receipt.json"]
```

with the fixture written at
`scratch/lane/.ufo/evidence/round-15/context-receipt.json`. Parse still precedes
containment, so both placements produce the same token; the containment-first
variant would not.

### 3.3 Literal expectations

| Arm | Expected exit | Required stdout token | Optional (only if detail is emitted) |
|---|---:|---|---|
| js-malformed-truncated | 2 | `invalid_json` | none |
| js-malformed-trailing-data | 2 | `invalid_json` | none |
| js-duplicate-key-top | 2 | `invalid_json` | `duplicate JSON key 'schema'` |
| js-duplicate-key-nested | 2 | `invalid_json` | `duplicate JSON key 'equal'` |

The check CLI must place the token on **stdout** for this class, in either the
historical shape (`kind=invalid_json`, `:627`) or the gate shape
(`id=invalid_json` / `"kind": "invalid_json"`, cf.
`tools/evidence-disposition.py:1066-1082`). One spelling, reused from history;
no second token.

### 3.4 Reference selftest shape

Follows the established `record()`/`SELFTEST_CASE`/`SELFTEST: PASS (N/N)`
convention (`tools/evidence-disposition.py:1510-1545, 1828-1856`):

```python
def run_check(path):
    return subprocess.run(
        [sys.executable, SELF, "--check-receipt", str(path)],
        capture_output=True, text=True, timeout=60, cwd=str(scratch),
    )

for name, raw in FIXTURES.items():
    path = scratch / (name + ".json")
    path.write_bytes(raw)
    proc = run_check(path)
    record(
        name,
        proc.returncode == 2 and "invalid_json" in proc.stdout,
        "exit={} expects=2 token={} expects=invalid_json".format(
            proc.returncode, "invalid_json" in proc.stdout),
    )
```

Subprocess only: calling `parse_json` or `decide()` in-process does not meet the
routed "standalone self-invocation" clause (`corpus/lessons/round-14-verifier-spotcheck.md:160`).

## 4. Additional check-mode invariants these fixtures depend on

1. **Read-only check.** `--check-receipt` must not write any receipt, temporary
   or final, and must not create files outside the scratch root. The historical
   INVALID branch writes `OUTPUT_REL` (`:621-626`); that behavior must not be
   carried into check mode, or the fixture run could write into lane evidence.
2. **Same parser, not a re-implementation.** The check path must call the
   promoted `parse_json`/`_no_duplicate_keys` pair verbatim (`:158-182`). A
   refactor to `json.load(open(path))` drops the hook and J3/J4 change class.
3. **Parse before structure, digest pin and path containment** (§2).
4. **Failure routing.** Any `InvalidContext` from parsing maps to exit 2 with its
   `kind` on stdout; it must not be flattened into `mismatch`/1 or `usage`/64.

## 5. Non-vacuity: what each arm would catch

| Arm | Fault it detects |
|---|---|
| J1 truncated | A check mode that lets a parse error escape as an uncaught traceback (exit 1/other) or that reports a schema/decide verdict instead of a parse failure. |
| J2 trailing data | A parser using `raw_decode`/first-document-only and silently ignoring trailing bytes; strict `json.loads` is the historical behavior (`:173`). |
| J3 top duplicate | A missing `object_pairs_hook`. Without the hook these bytes parse to a dict with `schema` set, and the same input then yields a *different* kind (structure/schema class) or an exit-1 decide mismatch — so asserting `invalid_json` specifically fails. This is the discriminating arm; asserting only "exit 2" would be vacuous because a schema-invalid receipt also exits 2. |
| J4 nested duplicate | A shallow pre-scan that de-duplicates only top-level keys. Nested duplicates are the real hazard for `comparison`/`mapping`/`environment` objects, because a later key silently overwrites the earlier one. |

Together J3+J4 pin that rejection is recursive over every object, which is the
actual guarantee `object_pairs_hook` provides.

## 6. What must not be pinned

- **The `JSONDecodeError` message text, line and column** (`:176-178`). It comes
  from CPython and contains the label; pinning it would make the selftest
  interpreter-version- and temp-path-dependent. Pin the kind only. (The
  duplicate-key detail is the lane's own literal at `:162` and is safe to pin —
  but only if the CLI exposes detail.)
- **The wrapper prefix.** Historical `CONTEXT: INVALID (…)` also carries a
  `receipt=<path>` field (`:627`) that has no meaning in a read-only check.
- **Absolute fixture paths.**
- **Which of J3/J4 is reported first** if an implementation scans ahead; each arm
  is a separate invocation, so ordering never matters.

## 7. Boundaries — what this class does not cover

- `invalid_utf8` (`:169-171`) is a distinct kind for non-UTF-8 bytes; not this
  fixture.
- Root-not-object (`:179-180`) also yields `invalid_json`, but is assigned to
  `SpecTypes` (container types); do not double-count it here.
- **Non-finite constants** (`NaN`, `Infinity`): historical `parse_json` passes no
  `parse_constant`, so Python's parser accepts them. Do not claim this class
  rejects them, and do not add a fixture expecting `invalid_json` for them. (The
  round-14 `evidence-disposition.py:176-177` gate does reject them; that is a
  different tool's contract.)
- BOM-prefixed files, duplicate keys with identical values, and very deep
  nesting are not required by the routed defect.
- These fixtures never reach the digest pin, structure validation or `decide()`;
  they prove the parse-error routing and nothing about the receipt semantics
  (those are `SpecClean`/`SpecMismatch`/`SpecTamper`).

## 8. Registry/exit-class line (for the Registry seat, bounded)

```
| invocation context capture | gate | python3 tools/context-capture.py --check-receipt RECEIPT | 0 retained receipt agrees; 1 evaluated mismatch; 2 could-not-evaluate invalid/malformed receipt JSON (invalid_json) or unavailable inputs; 64 usage/could-not-evaluate | python3 tools/context-capture.py --selftest | historical round-14 receipt and pins read-only; literal isolated selftest expectations in tool | normal capture writes round15 only; selftest isolated /tmp fixtures | tameshi |
```

Exit 64 remains usage/could-not-evaluate, per `:123` and the routed defect; it is
not a pass and not an evaluated mismatch.

## 9. Method and confidence

High confidence for the token/exit pair: `invalid_json` is written literally at
`:162`, `:177` and `:180`; the exit-2 routing is literal at `:628`; the declared
map is literal at `:123`; and the hook's exception bypasses the `JSONDecodeError`
handler by construction (`:172-178`). Medium confidence only on the check-mode
flag spelling, which is ContextGate's to fix; the recipe is parameterized on it
in §3.2 and the token/exit pair is invariant across the spellings.

No check, build, test, formatter, gate or selftest was executed while drafting
this report. This is advisory source reconstruction for the executor, not an
independent admission decision, and it adds no calibration credit by itself.
