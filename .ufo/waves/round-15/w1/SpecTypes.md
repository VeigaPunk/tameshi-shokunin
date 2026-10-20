# SpecTypes — bool-vs-integer and container types: fixture recipe, tokens, exits

Seat: `TameshiR15.SpecTypes` (executor, leaf). Assignment: read the historical
`capture-context.py`, draft only a concrete isolated fixture recipe for
**bool versus integer exits** and **container types**, state the exact existing
stable token and expected exit where supported, invent no required broad
validation feature, no source edits. This report advises `ContextGate`
(owner of `tools/context-capture.py`) through `TameshiR15`.

Method: source reads only at lane root `tameshi-shokunin`, 2026-10-20. I
executed no gate, no selftest, no historical script, no fixture, no target, no
sibling gate, no build/lint/test/formatter. The only process I ran was a
throwaway `python3` heredoc proving Python language semantics (`True == 1`,
`0 is False`, `isinstance(True, int)`, `json.loads` types, `list.get`,
`list.extend(str)`); it imported no lane file and touched no repository path.
`tools/context-capture.py` did not exist at read time (`ls` → No such file),
so every promoted-tool statement below is a contract recommendation, not an
observation of implemented behavior. No tool was installed or updated.

Overlap boundary with sibling seats: malformed/duplicate JSON is `SpecJSON`,
missing receipt/input is `SpecUnavailable`, snapshot digest mismatch is
`SpecTamper`, equal-valued REV name swap is `SpecNames`, mapping-false is
`SpecMapping`, control-failure is `SpecControl`, hermeticity is `SpecHermetic`.
This report owns only **JSON-type discrimination** (bool vs int, container
vs scalar) and the **selftest's own exit-code typing**.

---

## 1. Verdict

| Question | Answer |
|---|---|
| Does the historical public CLI accept a receipt, so a bool/int field can be fed to `decide()`? | **No.** `main(argv)` (`capture-context.py:605-613`) accepts only `-h/--help` (exit 0) and otherwise exits **64**. `decide()` runs only on the receipt the script itself computed in `evaluate()`. |
| Is any bool-vs-int literal exit pair therefore supported by the historical entry point? | **No.** The four strict `is not True` checks and the inverted `is not False` check are unreachable from outside; the values are produced internally as real bools (`base_text == inj_text`, comparisons, `baseline_ok`). |
| Is a container-type literal exit pair supported by the historical entry point? | **Partly, on the capture path only:** `parse_json` root-not-object → exit 2 `invalid_json`; manifest shape → exit 2 `invalid_manifest`; expected `inputs`/manifest `derived_from` shape → exit 2. Probe-document/section container defects are **not** classified: they either coalesce silently or raise an uncaught `AttributeError`/`TypeError` and exit **1** with a traceback and no `CONTEXT:` line. |
| What is the exact existing stable token for the reachable classes? | exit 2 → `CONTEXT: INVALID (kind=<kind> receipt=<path> exit=2)`; exit 0/1 → `CONTEXT: OK|MISMATCH (receipt=<path> exit=<n> probe-equal=<v> poison-control=<v> runner-mapping=<v>)`; exit 64 → **no `CONTEXT:` line**, stderr `capture-context.py: unexpected argument(s): <argv>` plus USAGE, no receipt. |
| Does the historical source emit stable per-predicate finding IDs? | **No.** `decide()` appends eight **prose** reasons (`:560-578`); there is no ID field. Status words `ok`/`mismatch`/`invalid_input` are the only stable machine tokens. Any per-predicate ID vocabulary is a round-15 addition and must be pinned explicitly, not assumed. |
| Is the bool/int pair supported after ContextGate adds `--check-receipt`? | **Yes, conditionally.** The ContextGate target already requires "retained receipt checking using actual decide predicates plus required structure"; under that mode a stored `1` in a field that `decide()` tests with `is True`, or a stored `0` in the field tested with `is not False`, has a deterministic, source-exact outcome: **exit 1, status `mismatch`, one exact reason string per predicate**. Section 4 gives the matrix. |

Consequence for acceptance: do **not** register bool/int literal pairs against
`.ufo/evidence/round-14/capture-context.py`; it cannot produce them. Register
them against the new `--check-receipt` mode only if that mode exists in the
delivered `tools/context-capture.py`. If it does not exist, record the pair as
unsupported rather than fabricating an expectation.

---

## 2. Source facts the recipe depends on

All paths below are `.ufo/evidence/round-14/capture-context.py` (historical,
must stay byte-identical).

### 2.1 Strict identity predicates (`decide()`, :553-580)

| Line | Predicate | Accepts | Rejects (→ reason) |
|---:|---|---|---|
| 560 | `comparison.get("equal") is not True` | JSON `true` only | `1`, `"true"`, `null`, missing |
| 564 | `comparison.get("payload_tool_sha256_matches_disk") is not True` | `true` only | `1`, `"true"`, `null`, missing |
| 566 | `environment.get("env_delta_matches_declared") is not True` | `true` only | `1`, `"true"`, `null`, missing |
| 568 | `environment.get("baseline_has_GIT_DIR") is not False` | JSON `false` only | `0`, `1`, `true`, `null`, missing — **inverted**: the familiar `0` is a mismatch |
| 570 | `positive_control.get("effective") is not True` | `true` only | `1`, `"true"`, `null`, missing |
| 572 | `not (sources.get("probe") or {}).get("matches_declared")` | **truthiness**: `true`, `1`, `"yes"` all pass | `false`, `0`, `""`, `null`, missing |
| 574 | `not (sources.get("runner") or {}).get("matches_manifest_declaration")` | truthiness | as above |
| 576 | `not mapping.get("all_match")` | truthiness | as above |

The asymmetry is real and load-bearing: five fields are strict identity, three
are truthiness. A selftest that assumes "all receipt booleans are strict" will
pin a wrong candidate contract; one that assumes "all are truthy" will miss the
five strict ones.

### 2.2 Source-exact reason strings (`:560-578`), concatenations resolved

1. `injected observation differs from baseline after excluding observed_at: normalized JSON mismatch`
   (the tail becomes `comparison.get("error")` when that is a truthy string)
2. `probe payload tool_sha256 does not match the disk digest`
3. `environment delta is not exactly the declared GIT_DIR injection`
4. `baseline still carries GIT_DIR`
5. `git poison positive control is ineffective`
6. `probe source digest does not match its r13 declared digest`
7. `runner source digest does not match the manifest declaration`
8. `mapping.reasons` entries, or `runner mapping mismatch` when that list is absent/empty

They are appended in exactly that order and returned as
`("mismatch", 1, reasons)`; all-pass returns `("ok", 0, [])` (`:579-580`).

### 2.3 Container handling

| Site | Source behavior |
|---|---|
| `parse_json` (:167-181) | root must be `dict` (`isinstance`); otherwise `InvalidContext("invalid_json", "<label> root is not an object")` → exit 2. Duplicate keys → `invalid_json`. |
| `parse_probe_document` (:340-347) | probe stdout must parse to a **dict**; list/scalar → `None`. Baseline `None` → `probe_baseline_unusable` exit 2 (`:350-360`). Injected `None` → comparison error `injected probe run produced no JSON document (exit=<n>)` → **exit 1**, not 2. |
| `comparison_block` (:350-360) | `legs` must be `list` of length 6; each row is used as `row.get(...)` with **no dict check** → a non-dict row raises `AttributeError` (`:354`). |
| `decide` section locals (:554-558) | `receipt.get("<section>") or {}`. A **falsy** container (`[]`, `0`, `""`) coalesces to `{}` and yields ordinary mismatch reasons; a **non-empty non-dict** (`[1]`, `1`, `"x"`) survives and the next `.get(...)` raises `AttributeError`. |
| `mapping.reasons` (:577) | `reasons.extend(mapping.get("reasons") or [...])`: a string is accepted and **char-extended** (no error); an int raises `TypeError`. |
| `validate_manifest` (:439-463) | `legs` must be `list`, length 6; each entry must be `dict`; message forms `manifest must carry exactly six legs`, `leg <n> is not an object`, `leg <n> has no string <key>`. All → `invalid_manifest` exit 2. |
| `evaluate` (:491-495) | `expected.inputs` must be `dict` → `invalid_expected`; `manifest.derived_from` must be `dict` → `invalid_manifest`. |
| `main` (:605-643) | Uncaught exceptions are **not** caught: an `AttributeError`/`TypeError` from the sites above escapes, so the interpreter exits **1** with a traceback, no `CONTEXT:` line and no receipt. Exit 2 is used for `InvalidContext` and receipt-write failure only. |

That last row is the defect class: without a shape check, a *container type*
error is indistinguishable by exit code from an *evaluated mismatch* (both 1),
and the round-14 lesson already rejects exit agreement alone. The lane has a
written precedent for the fix: `tools/repeat-control.py:43-48` says
`setup_error` "exists so that no uncaught Python exception can exit 1 and be
read as `controls_mismatch`". The context gate should adopt the same rule.

### 2.4 Existing lane precedent for int-not-bool (`tools/repeat-control.py`)

```python
if not isinstance(runs, int) or isinstance(runs, bool) or runs < 3:   # :379-380
if (expected_id not in SNAPSHOT_IDS
    or not isinstance(expected_exit, int)
    or isinstance(expected_exit, bool)                             # :384-386
    or expected_exit != EXIT_BY_ID[expected_id]):
```

This is the exact idiom to reuse. It proves the lane already treats
`true`/`false` as **not** acceptable where an integer exit is declared, and it
cross-checks the declared exit against the ID's table entry so the pair cannot
drift. No new framework is needed.

### 2.5 Python semantics (observed, language-level only)

```
True == 1        -> True        0 == False       -> True
1 is True        -> False       0 is False       -> False
isinstance(True, int) -> True   type(True) is int -> False
json.loads('{"a":true,"b":1,"c":false,"d":0}') -> bool,int,bool,int
true == 1        -> True        false == 0       -> True
[1].get("x")     -> AttributeError
["a"].extend("xyz") -> ['a','x','y','z']
```

Two independent consequences:
1. **Receipt semantics:** JSON `1`/`0` are `int` and fail `is True`/`is not False`.
2. **Selftest semantics:** an expected-exit table entry written as `True`/`False`
   compares equal to a process exit of `1`/`0`. Existing lane selftests compare
   with `==` only (`tools/evidence-disposition.py:1573`,
   `tools/witness-metadata.py:1165-1166`, `:1170`), so a CLI that emitted
   `"exit": true` would pass a case expecting `1` unless the type is checked.

---

## 3. Hermetic fixture recipe

### 3.1 Scratch layout and invocation

```python
scratch = tempfile.mkdtemp(prefix="tameshi-r15-context-types.", dir="/tmp")
lane = scratch / "<case>"          # one lane per case, never shared
# retained-receipt cases need only: lane/.ufo/evidence/round-15/receipt.json
# capture-mode cases also need the full synthetic lane listed in §3.6
```

Retained-receipt cases (the subject of §4.1–§4.2):

```sh
python3 tools/context-capture.py --check-receipt <lane>/.ufo/evidence/round-15/receipt.json \
    --lane-root <lane>
# acceptable spelling variants: --root; positional receipt path
```

Rules that make this hermetic:

- **Lane root must be explicit.** `capture-context.py:46` derives `LANE_ROOT`
  from four `dirname` calls on `SELF`, which is correct only at
  `.ufo/evidence/round-14/capture-context.py`; at `tools/context-capture.py` it
  resolves one level too high (also reported by `ReviewNames`). If the promoted
  tool does not add `--lane-root`/`--root`, the selftest must copy the tool to
  `<lane>/tools/context-capture.py` and run that copy. Do not rely on cwd.
- Pass `sys.executable` and `-I` to the child (existing convention,
  `witness-metadata.py:1135-1143`): no user site, no `PYTHON*` influence.
- The `--check-receipt` mode must be **read-only**: no receipt write, no probe,
  no git, no live lane/sibling read. Assert that the only files under `<lane>`
  afterwards are the fixture files the case authored.
- If the mode requires a pins/digest manifest, the fixture builder must
  generate that manifest **from the fixture bytes it just wrote** (or reuse one
  fixed `tool_sha256` constant declared in both the receipt and the pins
  record). Otherwise every type case is rejected as `snapshot_tampered` before
  `decide()` runs. The only deliberately stale digest is `SpecTamper`'s case.
- `--selftest` itself must not depend on `/nonexistent/tameshi-round14-poison`
  being absent by luck. Either keep the fixed path and have the selftest emit a
  distinct unable-to-run result (exit 2, no silent skip) if `os.path.lexists`
  is true, or make the poison path fixture-internal only under `--selftest`.
  Do not add a production flag that changes the declared injection.

### 3.2 Canonical green receipt `G`

Literal fixture bytes; the reason matrix in §4 mutates exactly one field.
`decide()` ignores `status`/`exit`/`reasons`; the promoted shape check reads
them, so they must be present and consistent.

```json
{
  "schema": "tameshi-round14-context-receipt-v1",
  "tool": "context-capture.py r15 fixture",
  "tool_sha256": "<64 lowercase hex: sha256 of the tool bytes, or the constant declared in the pins record>",
  "status": "ok",
  "exit": 0,
  "reasons": [],
  "comparison": {
    "equal": true,
    "payload_tool_sha256_matches_disk": true
  },
  "positive_control": {"effective": true},
  "environment": {
    "env_delta_matches_declared": true,
    "baseline_has_GIT_DIR": false
  },
  "sources": {
    "probe": {"matches_declared": true},
    "runner": {"matches_manifest_declaration": true}
  },
  "mapping": {"all_match": true, "reasons": []}
}
```

`G` → `decide()` returns `("ok", 0, [])`. Expected observables: exit **0**,
status `ok`, receipt `exit` **0** (JSON int, not `true`), reasons `[]`.

### 3.3 Green-control discriminator (selftest-level bool/int)

Two negative controls prove the table itself is not conflating bool and int:

- Run `G` and assert `proc.returncode == 0` **and** `type(payload["exit"]) is int`
  **and** `payload["status"] == "ok"`.
- Run the `T1` case (below) and assert `proc.returncode == 1`; if any harness
  row encodes `expected_exit` as `True`, the `G` case would also pass
  (`0 == False`), which the type assertion forbids.

---

## 4. Expected exits and tokens

### 4.1 Bool-vs-integer matrix (retained-receipt mode)

Every row is `G` with exactly **one** field replaced. `comparison.error` must
stay absent/null so reason 1 uses the canonical default tail. "Reason list" is
exact and ordered; all eight strings are existing source text.

| # | One-field mutation | Exit | Status | Exact reason list |
|---|---|---:|---|---|
| T0 | none (`G`) | 0 | `ok` | `[]` |
| T1 | `comparison.equal = 1` | 1 | `mismatch` | `["injected observation differs from baseline after excluding observed_at: normalized JSON mismatch"]` |
| T2 | `comparison.equal = "true"` | 1 | `mismatch` | same as T1 |
| T3 | `comparison.payload_tool_sha256_matches_disk = 1` | 1 | `mismatch` | `["probe payload tool_sha256 does not match the disk digest"]` |
| T4 | `environment.env_delta_matches_declared = 1` | 1 | `mismatch` | `["environment delta is not exactly the declared GIT_DIR injection"]` |
| T5 | `environment.baseline_has_GIT_DIR = 0` | 1 | `mismatch` | `["baseline still carries GIT_DIR"]` |
| T6 | `environment.baseline_has_GIT_DIR = true` | 1 | `mismatch` | same as T5 |
| T7 | `positive_control.effective = 1` | 1 | `mismatch` | `["git poison positive control is ineffective"]` |
| T8 | `sources.probe.matches_declared = 1` | **0** | `ok` | `[]` — truthiness, **contract pin of the historical asymmetry**, not an endorsement |
| T9 | `mapping.all_match = 1` | **0** | `ok` | `[]` — same asymmetry |
| T10 | top-level `"exit": true` (status `ok`) | 2 | `invalid_input` | kind `receipt_shape_invalid` (new, §5.R2) |

T5 is the discriminating case that a naive "0 means false" test misses:
`0 is not False` is true, so the gate must report a mismatch. T8/T9 are
optional but recommended: choosing them forces the contract to state that
these three fields are truthy, not strict, and prevents a later silent
"strictness upgrade" from changing documented behavior. If ContextGate instead
decides to type-check those three fields as bool, T8/T9 move to exit 2 and
**must be documented as a deliberate deviation from `decide()`**.

Token for exit 1 rows: the promoted line must carry the status word and
`exit=1` (historical form `CONTEXT: MISMATCH (... exit=1 ...)`), and the
receipt/JSON must expose `"status": "mismatch"`, `"exit": 1` (int), and the
exact reason list above. Pinning exit alone is explicitly insufficient per
`corpus/lessons/round-14-verifier-spotcheck.md` (exit agreement with the wrong
mechanism was rejected).

### 4.2 Container-type matrix (retained-receipt mode)

Historical behavior is listed so the promoted contract cannot be confused with
it. Recommended promoted outcomes assume the minimal shape precheck in §5.R1/R2.

| # | One-field mutation | Historical trace | Recommended | Exact token |
|---|---|---|---|---|
| C1 | file root = `[]` | `parse_json` → exit 2 | 2 | `invalid_json`; message suffix ` root is not an object` |
| C2 | `comparison = []` | falsy → `{}` → exit 1, reasons 1+2 | 2 | `receipt_shape_invalid` |
| C3 | `comparison = [1]` | `AttributeError` uncaught → exit 1, traceback, **no `CONTEXT:` line, no receipt** | 2 | `receipt_shape_invalid` |
| C4 | `comparison = 0` | falsy → `{}` → exit 1, reasons 1+2 | 2 | `receipt_shape_invalid` |
| C5 | `comparison = 1` | `AttributeError` → exit 1 traceback | 2 | `receipt_shape_invalid` |
| C6 | `mapping = {"all_match": false, "reasons": 7}` | `TypeError` on `extend` → exit 1 traceback | 2 | `receipt_shape_invalid` |
| C7 | `mapping.reasons = "xyz"` | char-extended → exit 1, reasons `["x","y","z"]` | 2 | `receipt_shape_invalid` |
| C8 | `sources.probe = [1]` | `AttributeError` → exit 1 traceback | 2 | `receipt_shape_invalid` |
| C9 | `sources.probe = []` | falsy → `{}` → exit 1, reason 6 | 2 | `receipt_shape_invalid` |
| C10 | `"status": "mismatch", "exit": 0` | ignored by `decide` → exit 0 `ok` | 2 | `receipt_shape_invalid` |
| C11 | delete `"comparison"` | missing → exit 1, reasons 1+2 | 2 | `receipt_shape_invalid` |

C2/C3 (and C4/C5, C8/C9) are the important pairs: **same JSON kind, different
truthiness** produces opposite historical behavior — silent mismatch versus an
uncaught crash. A gate that classifies by exit code alone cannot tell them
apart. The precheck must collapse each pair to one stable exit 2 without a
traceback.

The checks apply to every decision section, not just the examples:
`comparison`, `positive_control`, `environment`, `sources`, `mapping` must each
be a JSON object; `mapping.reasons`, when present, must be an array of strings;
`exit` must be an int (not bool); `status` must be a string consistent with the
exit. Nothing else in the receipt needs typing for this mode.

### 4.3 Container matrix on the capture path (`evaluate()`)

These need the full synthetic lane (§3.6); they are listed because the
container position changes the exit class and the selftest must not assume
"bad container ⇒ exit 2".

| # | Mutation | Historical | Recommended | Token |
|---|---|---|---|---|
| P1 | baseline probe stdout root = `[]` | exit 2 | 2 | `probe_baseline_unusable` |
| P2 | baseline `legs` = six non-object rows | `AttributeError` at `:354` → exit 1 traceback | 2 | `probe_baseline_unusable` |
| P3 | baseline `legs = {}` | exit 2 | 2 | `probe_baseline_unusable` |
| P4 | manifest `legs = {}` | exit 2 | 2 | `invalid_manifest`, `manifest must carry exactly six legs` |
| P5 | manifest `legs[0] = []` | exit 2 | 2 | `invalid_manifest`, `leg 1 is not an object` |
| P6 | `expected.inputs = []` | exit 2 | 2 | `invalid_expected`, `expected.json has no inputs object` |
| P7 | manifest `derived_from = []` | exit 2 | 2 | `invalid_manifest`, `manifest has no derived_from object` |
| P8 | **injected** probe stdout root = `[]` (baseline valid) | exit 1 | 1 | exact reasons `["injected observation differs from baseline after excluding observed_at: injected probe run produced no JSON document (exit=0)", "probe payload tool_sha256 does not match the disk digest"]` |

P8 is the mirror of P1 and proves the asymmetry is intentional in `decide()`
(`comparison_block` sets `equal=false` and an error string for the injected
side, while the baseline side raises). Do not "fix" it by promoting P8 to exit
2 without changing `comparison_block`; pin whichever contract is implemented.

### 4.4 Capture-mode lane prerequisites (for P1–P8 only)

`tools/pin-disposition.py` (deterministic probe emitting a six-leg
`pin-disposition-v1` ok document with a stable `tool_sha256`),
`tools/mutate-and-run.sh` (six header rows, six `PIN_`/`REV_` constants, six
`regression_case_git` calls inside `run_regression`),
`.ufo/evidence/round-13/pin-manifest.json` (six legs, `derived_from.sha256` =
runner digest), `.ufo/evidence/round-13/expected.json`
(`inputs["tools/pin-disposition.py"]` = probe digest), and a `git init` at the
fixture lane root so the positive control baseline is ok. Without the `git
init`, every capture case also emits `git poison positive control is
ineffective` (also reported by `ReviewNames` FP3), which would contaminate the
reason lists above.

---

## 5. Bounded recommendations for ContextGate

**R1 — Keep `decide()` as the sole verdict authority.** The retained-receipt
mode should: (a) parse with the historical `parse_json` (root object, duplicate
keys rejected, exact `invalid_json` token); (b) check *presence* of the five
decision sections and the eight decision keys, and *container* types (sections
are objects, `mapping.reasons` is an array of strings); (c) check
`status`/`exit`/`schema` are present and typed (`exit` int-not-bool, status
consistent with exit); (d) pass the decision values to the **actual**
`decide()`. Do not boolean-coerce, and do not type-check the eight decision
values as bool — that would make the historical strict/truthiness distinction
untestable and would contradict "reuse decide semantics". This is a narrow
shape check, not a general receipt validator.

**R2 — One new token only: `receipt_shape_invalid`, exit 2, status
`invalid_input`.** It covers C2–C11; C1 reuses `invalid_json`. Both are
could-not-evaluate, never a verdict. Rationale: the historical behavior for
these inputs is either a silent mismatch or an uncaught exception that exits 1
and is indistinguishable from a real mismatch; `repeat-control.py:43-48`
already states the lane rule that no uncaught exception may exit 1. If
ContextGate declines the precheck, it must still pin the historical traces
above **and** assert `"Traceback" not in stderr`, which will fail the tool —
proving the precheck is required rather than optional polish.

**R3 — Selftest rows must type-check exits.** Use the `repeat-control.py`
int-not-bool idiom:

```python
assert type(row["expected_exit"]) is int          # not isinstance: True is an int
assert proc.returncode == row["expected_exit"]
payload = json.loads(last_stdout_line)
assert type(payload["exit"]) is int and payload["exit"] == proc.returncode
assert payload["status"] == {0: "ok", 1: "mismatch", 2: "invalid_input"}[row["expected_exit"]]
assert "Traceback" not in proc.stderr
```

The existing `==`-only comparisons (`evidence-disposition.py:1573`,
`witness-metadata.py:1165-1166`) would accept JSON `true` for exit 1 and
`false` for exit 0; do not copy that hole into the new gate. If the receipt
mode emits JSON, add one fixture (`T10`) whose `exit` is `true` and expect
exit 2 / `receipt_shape_invalid`; that fixture is the discriminator that fails
loudly under an `==`-only harness.

**R4 — Distinguish help/usage/verdict.** `-h/--help` returns 0 with no receipt
(`:606-608`); a 0-exit selftest case must assert the `ok` status and receipt
contract, not just the code. Exit 64 (`--selftest --json`, unknown flag) has no
`CONTEXT:` line, writes nothing, and stderr contains
`capture-context.py: unexpected argument(s):`; assert that exact line and the
absence of output files. Never describe 64 as a mismatch. Mirror the
`evidence-disposition.py:1828-1832` usage-case shape.

**R5 — Pin reason lists, not substrings, for the eight decision predicates.**
The order is source order; T1/T3/T4/T5/T7 each isolate exactly one reason, so a
regression that drops or reorders a predicate is visible. If ContextGate adopts
a per-predicate ID vocabulary (e.g. the `SiblingOverlap` suggestions), map the
five strict predicates to five distinct IDs; do **not** collapse them into one
generic `mismatch`, or the type matrix cannot distinguish "rejected `1`" from
"rejected digest".

**R6 — Digest binding is orthogonal to the type matrix.** Generate each
fixture's pins record from the bytes just written, and use one fixed
`tool_sha256` constant across receipt and pins so no type case is pre-empted
by `snapshot_tampered`. The mode should record, not silently assume, which
digest it enforced (pinned value vs live tool bytes).

**R7 — Add only these rows.** 11 retained-receipt type rows (T0–T10, T8/T9
optional-as-contract-pins), 11 container rows (C1–C11), and the 8 capture-row
container cases if the capture path is exercised hermetically (P1–P8; P8 is the
only exit-1 row). Do not add a fixture for every emitted reason or every
receipt field; the lesson explicitly excludes that.

**R8 — Registry text.** In the new gate row, state the retained-receipt mode's
authority limit: it re-evaluates stored declarations with `decide()`; it does
not re-execute stored argv, does not authenticate the author of the pins, and
does not establish environment independence. Exit 64 is could-not-evaluate.

---

## 6. What this report does **not** require

- No bool/int fixtures against the historical script; it cannot receive a
  receipt, and its internal values are already real bools.
- No bool type enforcement on the eight decision values (that would replace
  `decide()` semantics with a schema validator).
- No fixture per reason string, per receipt field, or per manifest key.
- No new environment claim, no GIT_* matrix, no dependency/suite identity.
- No change to `.ufo/evidence/round-14/capture-context.py`,
  `context-receipt.json`, or any round-12/13/14 byte.
- No execution by this seat; every expected value above is source-derived.

---

## 7. Risks and limits

1. **The promoted tool was absent at read time.** All `--check-receipt`,
   `--lane-root`, and `receipt_shape_invalid` statements are contract advice.
   If ContextGate's selected CLI differs, the *values* in §4.1/§4.2 still hold
   (they come from `decide()`), but the argv and the exit-2 kind must be
   re-pinned to the delivered contract. Do not treat this report as a test log.
2. **Truthiness asymmetry (T8/T9/`:572-576`).** A future "strictness cleanup"
   would change documented behavior; pin whichever choice is made. Marking it
   as an unstated assumption is the actual risk.
3. **Historical exit-1 traceback.** If the delivered tool keeps the uncaught
   exception path, a container fixture will exit 1 with a traceback and no
   `CONTEXT:` line; any selftest comparing exit only will pass it. The
   `Traceback`-absence assertion is the guard.
4. **`LANE_ROOT` derivation.** At `tools/context-capture.py` the historical
   four-`dirname` rule resolves above the lane; fixtures must use an explicit
   root flag or a copied tool. This is a prerequisite for every recipe here.
5. **`comparison.error` text.** Reason 1's tail is input-controlled. Fixtures
   must omit `error`; a fixture that sets it silently pins a different string.
6. **No independent admission.** This is advisory source reconstruction by a
   non-author seat, not an admission decision; L1 runs all checks once.
