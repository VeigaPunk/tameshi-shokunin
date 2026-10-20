# SpecMapping — mapping-false exit 1: isolated fixture recipe, exact token, expected exit

Seat: `TameshiR15.SpecMapping` (executor, leaf). Target: historical
`.ufo/evidence/round-14/capture-context.py`, read only; advice for
`TameshiR15.ContextGate` and the promoted `tools/context-capture.py`.
**No source edit, no gate/selftest/test execution, no build, no formatter, no commit,
no tool install or update.** Every source claim below is bounded to the cited
historical lines. LSP is not mounted — `read xd://lsp` returned `No such tool`;
navigation used direct reads and `grep`, recorded as actual unavailability rather
than an empty semantic result.

## 1. Answer first

| Question | Answer |
|---|---|
| Which branch produces mapping false? | One or more of the five per-leg checks, or the set/order flags, is false, so `mapping.all_match` is false (`capture-context.py:313-335`). `decide()` then extends the reason list from `mapping.reasons` and returns mismatch (`:576-579`). |
| Is exit 1 supported by the historical source? | **Yes.** `return "mismatch", 1, reasons` (`:578-579`). The fixture must make every *other* `decide()` predicate true so the exit is attributable to mapping alone (`:553-577`). |
| Exact existing stable token — machine-readable | **`pin_name_and_value_match_manifest`**. Frozen member of the `CHECKS` tuple (`:109-115`), row key in `mapping.legs[].checks` (`:270, :283-288, :300-312`). |
| Exact existing stable token — message | **`leg js-kimi-census: pin_name_and_value_match_manifest`**. Literal produced by `"leg {}: {}".format(row["leg"], ", ".join(failed))` (`:320-323`); appears both in top-level `reasons` and in `mapping.reasons`. |
| Exact existing stable token — CLI line | The `CONTEXT: MISMATCH (…)` line (`:637-642`). For this fixture its invariant substrings are **`exit=1`** and **`runner-mapping=False`**, with `probe-equal=True poison-control=True`; the receipt path renders from the tool's constant. |
| Expected exit | **1** (evaluated mismatch). |
| Existing finding-ID field? | **No.** No finding identifier field (`id`, `code`, `finding_id`) exists; `reasons` is a list of plain strings (`:559-579`) and no receipt schema key carries an identifier. Do not pin an invented ID as if it were historical. If the promoted CLI adds `findings[].id`, the mapping-false ID must be declared in source and pinned next to these literals; no broader taxonomy is required by this seat. |
| Minimal fixture | One synthetic lane root. Baseline: all six mappings agree → exit 0. Negative: rewrite exactly one manifest leg's `expected_sha256` and rerun the same public CLI → exit 1 with exactly one reason, `leg js-kimi-census: pin_name_and_value_match_manifest`. Runner bytes, probe bytes, expected.json and every other manifest field stay identical. |
| Does this need snapshot mode? | **No.** All four inputs are generated inside the temp fixture and their digests are written into the synthetic manifest/expected. A digest-bound snapshot of real lane bytes would break isolation and add a second cause of mismatch. |

The pair to pin is therefore `(exit 1, "leg js-kimi-census: pin_name_and_value_match_manifest")`
with the machine key `mapping.legs[0].checks.pin_name_and_value_match_manifest == false`.
That is the "literal exit and stable finding pair" the round-15 lesson requires,
expressed with tokens that exist in the historical bytes today.

## 2. Read revision and evidence anchors

Read revision: working tree at the round-15 lane root, 2026-10-20. Historical file:
`.ufo/evidence/round-14/capture-context.py`, 647 lines, sha not re-attested by this
seat (no execution). Relevant ranges:

| Lines | Content used |
|---|---|
| `:2-31` | Module contract: one prospective GIT_DIR-injection comparison, top-level `observed_at` exclusion, six runner-leg mappings, exit map. |
| `:44-58` | Version, `SELF`, `LANE_ROOT`/`FLEET_ROOT` derivation, schemas, four input paths, round-14 output path. |
| `:60-68` | `INJECTED_ENV` = exactly `GIT_DIR=/nonexistent/tameshi-round14-poison`, control env additions, timeouts. |
| `:74-81` | Frozen `EXPECTED_SUFFIX` table for the six real leg names. |
| `:83-105` | `HEADER_ROW_RE`, `PIN_CONST_RE`, `REV_CONST_RE`, `CALL_RE`, `CALL_LINE_RE`, `RUN_REGRESSION_RE`. |
| `:109-115` | Frozen `CHECKS` tuple (five per-leg check names). |
| `:117-125` | Usage and the exit map: 0 equal, 1 mismatch, 2 could-not-evaluate, 64 usage. |
| `:184-210` | `safe_env()` (all `GIT_*` removed, `LC_ALL=C`) and `run_bounded()`. |
| `:213-256` | Runner parse and its structural `InvalidContext("runner_unparsed", …)` raises. |
| `:259-337` | `mapping_block`: per-leg checks, row/check recording, reasons, `all_match`. |
| `:350-392` | `comparison_block`: baseline must be a six-leg ok `pin-disposition-v1` document with `pinned.status == "verified"` and no `content_status == "unavailable"`; normalized JSON equality. |
| `:395-412` | Positive control; `effective` requires baseline git exit 0, non-empty stdout, injected nonzero exit, and reflection. |
| `:439-462` | `validate_manifest`: schema, exactly six legs, unique names, string fields, 40-hex commit, 64-hex digest. |
| `:476-515` | Reads/parses all four inputs; probe digest must equal `expected.json.inputs["tools/pin-disposition.py"]`; runner digest must equal `manifest.derived_from.sha256` with path ending `tools/mutate-and-run.sh`; then `mapping_block(...)`. |
| `:524-545` | Environment delta and the two probe subprocess runs. |
| `:553-580` | `decide()`: eight predicates, mapping last, exit 1 / exit 0. |
| `:605-643` | `main()`: `--help` 0, unexpected argv 64 without receipt, `InvalidContext` 2 with receipt, evaluated result printed and returned. |

Retained round-14 receipt corroboration (read-only): `status "ok"`, `exit 0`,
`reasons []`, `mapping.all_match true`, `mapping.reasons []`, all five checks true on
every leg, `comparison.equal true`, `positive_control.effective true`. This is the
shape the fixture's baseline must reproduce.

## 3. Why the mutation must be in the manifest, not the runner

`decide()` admits exit 1 from eight independent predicates (`:560-577`). A nominal
"exit 1" assertion therefore proves nothing by itself; a broken fixture can exit 1 for
a neighbouring reason. Two source facts dictate the design:

1. **The runner file is digest-checked.** `sources.runner.matches_manifest_declaration`
   compares the actual runner bytes with `manifest.derived_from.sha256` (`:504-509`),
   and `decide()` fails on a mismatch with the reason
   `runner source digest does not match the manifest declaration` (`:574-575`).
   Editing the runner without also rewriting the manifest's `derived_from` produces the
   **wrong** exit-1 reason.
2. **A manifest leg's `expected_sha256` is not checked against any file.** It is only
   compared with the parsed `PIN_` value in `mapping_block` (`:283-288`). Therefore
   changing one manifest leg's digest changes exactly one mapping check while leaving
   the runner digest, the probe digest, the environment delta and the control untouched.

The negative fixture is consequently a **one-field manifest mutation** with identical
runner/probe/expected bytes. That is the differential that makes exit 1 attributable to
mapping, not to a source-pin or control failure.

A second requirement follows from the frozen name table: the fixture must reuse the six
literal leg names from `EXPECTED_SUFFIX` (`:74-81`). A synthetic leg name yields
`suffix = None`, which makes the pin, rev and constant-name checks all false and adds
set/order reasons (`:279-312, :313-323`); the single-check token in §1 is then lost.

## 4. Required invocation seam (implementation-critical for ContextGate)

The historical `LANE_ROOT` is `dirname(dirname(dirname(dirname(SELF))))` (`:46-47`).
That is correct only because the historical file lives at
`.ufo/evidence/round-14/capture-context.py`. A real file at
`tools/context-capture.py` has a different depth: the same expression resolves the lane
root to an ancestor **above the repository** (`…/Projects`), so the four input reads and
the output write would leave the intended tree. The promoted tool must therefore either
derive the repository root from its `tools/` location, or accept an explicit root.

For the selftest, an explicit public seam is required: the fixture needs all four inputs
and the receipt to resolve under a `mkdtemp` root while the **same maintained file** is
invoked as a real subprocess. Recommended minimal seam:

```text
tools/context-capture.py --root <lane-root>     # capture/check against that root
tools/context-capture.py --selftest             # spawns the CLI on temp fixtures
```

`--root` must scope `LANE_ROOT`, `FLEET_ROOT = dirname(LANE_ROOT)`, all four relative
inputs and the receipt path. It is one argument, not a new validation feature. A copied
tool under a four-level-deep temp path is the only no-flag alternative, but it conflicts
with the promoted `tools/` location and makes the receipt's tool identity a copy; not
recommended. An environment variable would also work but is less auditable than an
explicit argv entry in the retained receipt.

Selftest mechanics: `--selftest` must spawn `sys.executable <tool> --root <fixture>` as
a subprocess and assert the process exit plus the receipt. Calling `mapping_block()` or
`decide()` in-process does **not** meet the routed requirement
(`corpus/lessons/round-15.md`, admit criteria: public CLI selftest over isolated
fixtures asserting literal exit and stable finding pairs).

## 5. Fixture recipe

### 5.1 Layout and preconditions

```text
T/                                  # tempfile.mkdtemp(prefix="cc-r15-selftest-mapping-")
└── lane/                           # the --root value; a git repository
    ├── tools/
    │   ├── pin-disposition.py      # synthetic probe stub (below)
    │   └── mutate-and-run.sh       # synthetic runner stub (below)
    └── .ufo/evidence/round-13/
        ├── pin-manifest.json       # synthetic, six legs
        └── expected.json           # synthetic, pins the probe digest
```

- `T/lane` must be a git repository (`git init -q T/lane`). Otherwise the positive
  control's baseline exit is nonzero and the run exits 1 with the **wrong** reason
  `git poison positive control is ineffective` (`:570-571, :395-412`).
- `python3` and `git` must be on `PATH`; the tool looks both up and raises exit 2
  `missing_executable` otherwise (`:517-522`).
- `os.path.lexists("/nonexistent/tameshi-round14-poison")` must be false; otherwise the
  tool exits 2 `poison_path_exists` before mapping (`:469-472`). Preflight this in the
  selftest and report a setup outcome rather than misclassifying it as mapping false.
  This single fixed-path `stat`, the two `which` lookups (`:517-518`) and the tool's own
  source-digest read (`:414-417`) are the only non-temp observations on this path; no
  other bytes are read or written outside the temp root.
- No network. No real lane, round-14, sibling or fleet file is read.

### 5.2 Exact fixture bytes

The six leg tuples are the real identities from the round-13 manifest, paired with
synthetic digests so nothing looks like a live pin. Values are lowercase hex and satisfy
`validate_manifest` (`:439-462`).

```python
LEGS = [
    ("js-kimi-census",       "kumitate-shokunin", "scripts/kimi-census.mjs",   "JS",        "a"*64, "1"*40),
    ("bash-surface-census",  "kagi-shokunin",     "corpus/surface-census.sh",  "BASH",      "b"*64, "2"*40),
    ("bash-tsukuroi-census", "tsukuroi-shokunin", "tools/tsukuroi-census.sh",  "TSUKUROI",  "c"*64, "3"*40),
    ("bash-mado-verify",     "mado-shokunin",     "tools/mado-verify.sh",      "MADO",      "d"*64, "4"*40),
    ("bash-checklist-run",   "kagi-shokunin",     "corpus/checklist-run.sh",   "CHECKLIST", "e"*64, "5"*40),
    ("js-claims-check",      "kumitate-shokunin", "scripts/claims-check.mjs",  "CLAIMS",    "f"*64, "6"*40),
]
```

Runner stub — text only; the gate parses and hashes it, never executes it. It must
satisfy `HEADER_ROW_RE` six times, `PIN_CONST_RE`/`REV_CONST_RE` exactly six times each
over the whole file, and `CALL_RE` six times inside the `run_regression` body
(`:83-105, :213-256`). Do not add any other `# leg repo/path n/n (n%)` line or any
extra `PIN_…=`/`REV_…=` assignment, including in comments; each would push a count past
six and turn the run into exit 2 `runner_unparsed`.

```python
RUNNER_SRC = (
    "# tameshi round-15 selftest fixture runner (synthetic; parsed, never executed)\n"
    + "".join(f"# {leg} {repo}/{path} 10/10 (100%)\n" for leg, repo, path, *_ in LEGS)
    + "\n"
    + "".join(f"PIN_{suffix}={pin}\n" for _leg, _repo, _path, suffix, pin, _rev in LEGS)
    + "".join(f"REV_{suffix}={rev}\n" for _leg, _repo, _path, suffix, _pin, rev in LEGS)
    + "\nrun_regression() {\n"
    + "".join(
        f"  regression_case_git {leg} '{repo}/{path}' \"$PIN_{suffix}\" \"$REV_{suffix}\" "
        f"\"fixture-{leg}\" 'synthetic case' \"$TABLE_{suffix}\"\n"
        for leg, repo, path, suffix, _pin, _rev in LEGS)
    + "}\n"
)
```

Probe stub — executed as `python3 tools/pin-disposition.py` with `cwd = LANE_ROOT`. It
must emit a six-leg `pin-disposition-v1` document with `status "ok"`, a top-level
`observed_at`, every `content_status != "unavailable"`, every `pinned.status ==
"verified"`, and a `tool_sha256` equal to its own on-disk digest (`:350-359`). The
timestamp is fixed so baseline and injected stdout are byte-identical; `raw_stdout_equal`
and `equal` are then both true and no comparison predicate can confound the mapping
verdict. (Exercising the `observed_at` exclusion is a different fixture; do not mix it
into this one.)

```python
PROBE_SRC = '''#!/usr/bin/env python3
import hashlib, json, os

digest = hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest()
legs = [{"leg": name, "content_status": "present", "pinned": {"status": "verified"}}
        for name in ("js-kimi-census", "bash-surface-census", "bash-tsukuroi-census",
                     "bash-mado-verify", "bash-checklist-run", "js-claims-check")]
print(json.dumps({"schema": "pin-disposition-v1", "status": "ok",
                  "observed_at": "2026-10-20T00:00:00Z",
                  "tool_sha256": digest, "legs": legs}, sort_keys=True))
'''
```

Oracles — generated after the two source files exist, so the digests bind the exact
fixture bytes. The runner digest goes in `derived_from.sha256`; the probe digest goes in
`expected.json.inputs` under the exact key `tools/pin-disposition.py`
(`:476-509`).

```python
def write_oracles(lane, mutate):
    lane = Path(lane)
    probe_sha = hashlib.sha256((lane / "tools/pin-disposition.py").read_bytes()).hexdigest()
    runner_sha = hashlib.sha256((lane / "tools/mutate-and-run.sh").read_bytes()).hexdigest()
    legs = []
    for leg, repo, path, suffix, pin, rev in LEGS:
        expected = "0" * 64 if mutate and leg == "js-kimi-census" else pin
        legs.append({"leg": leg, "repo": repo, "path": path,
                     "pinned_commit": rev, "expected_sha256": expected,
                     "pinned_source": "synthetic round-15 selftest fixture"})
    (lane / ".ufo/evidence/round-13/pin-manifest.json").write_text(
        json.dumps({"schema": "pin-manifest-v1",
                    "derived_from": {
                        "path": "tameshi-shokunin/tools/mutate-and-run.sh",
                        "sha256": runner_sha},
                    "legs": legs}, indent=1) + "\n", encoding="utf-8")
    (lane / ".ufo/evidence/round-13/expected.json").write_text(
        json.dumps({"schema": "tameshi-expected-v1",
                    "inputs": {"tools/pin-disposition.py": probe_sha}}, indent=1) + "\n",
        encoding="utf-8")
```

`mutate=False` sets every manifest digest to the matching `PIN_` value, so all five
checks pass on every leg and `leg_set_equal`/`leg_order_equal` are true. `mutate=True`
changes only `js-kimi-census.expected_sha256` to `"0"*64`; it does not touch the runner,
the probe, `derived_from`, or any other leg.

### 5.3 Invocation and literal assertions

```python
def invoke(tool, lane, cwd):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run([sys.executable, str(tool), "--root", str(lane)],
                          cwd=str(cwd), env=env, capture_output=True, text=True)

BASELINE_LINE = ("CONTEXT: OK (receipt=.ufo/evidence/round-15/context-receipt.json "
                 "exit=0 probe-equal=True poison-control=True runner-mapping=True)\n")
MISMATCH_LINE = ("CONTEXT: MISMATCH (receipt=.ufo/evidence/round-15/context-receipt.json "
                 "exit=1 probe-equal=True poison-control=True runner-mapping=False)\n")
REASON = "leg js-kimi-census: pin_name_and_value_match_manifest"
```

Baseline run (`mutate=False`):

```python
assert base.returncode == 0
assert base.stdout == BASELINE_LINE
r = json.loads((lane / ".ufo/evidence/round-15/context-receipt.json").read_text())
assert (r["status"], r["exit"], r["reasons"]) == ("ok", 0, [])
assert r["mapping"]["all_match"] is True and r["mapping"]["reasons"] == []
assert r["comparison"]["equal"] is True
assert r["positive_control"]["effective"] is True
assert r["sources"]["probe"]["matches_declared"] is True
assert r["sources"]["runner"]["matches_manifest_declaration"] is True
assert not (lane / ".ufo/evidence/round-14/context-receipt.json").exists()
```

Negative run (`mutate=True`, after asserting the runner bytes are unchanged):

```python
assert neg.returncode == 1
assert neg.stdout == MISMATCH_LINE
r = json.loads((lane / ".ufo/evidence/round-15/context-receipt.json").read_text())
assert (r["status"], r["exit"]) == ("mismatch", 1)
assert r["reasons"] == [REASON]
assert r["mapping"]["reasons"] == [REASON]
assert r["mapping"]["all_match"] is False
assert r["mapping"]["leg_set_equal"] is True
assert r["mapping"]["leg_order_equal"] is True
assert r["mapping"]["legs"][0]["checks"] == {
    "header_matches_manifest": True,
    "pin_name_and_value_match_manifest": False,
    "rev_name_and_value_match_manifest": True,
    "leg_call_matches_manifest": True,
    "constant_names_match_leg": True,
}
assert all(row["match"] for row in r["mapping"]["legs"][1:])
assert r["comparison"]["equal"] is True
assert r["positive_control"]["effective"] is True
assert r["sources"]["probe"]["matches_declared"] is True
assert r["sources"]["runner"]["matches_manifest_declaration"] is True
```

Pinning the whole stdout line is possible only if the promoted CLI keeps the historical
print format (`:637-642`) and the round-15 receipt path. If either is parameterized,
pin the invariant substrings `exit=1`, `probe-equal=True`, `poison-control=True`,
`runner-mapping=False`, and assert `receipt` equals the declared path.

Cleanup: `shutil.rmtree(T)` in `finally`. All fixture writes and the receipt are under
`T`; the historical round-14 receipt and source are never opened for write.

## 6. Confounds that would fake "mapping false, exit 1"

| Mutation or omission | Actual outcome | Source |
|---|---|---|
| Runner bytes edited without updating `derived_from.sha256` | exit 1, wrong reason `runner source digest does not match the manifest declaration` | `:504-509, :574-575` |
| Header/call/PIN/REV count changed, duplicate or unparsable body | exit 2 `invalid_input`, `error.kind=runner_unparsed`, `CONTEXT: INVALID (kind=runner_unparsed … exit=2)` | `:218-253, :617-628` |
| Synthetic leg name not in `EXPECTED_SUFFIX` | exit 1, but three checks fail plus set/order reasons; single-check token lost | `:74-81, :279-312, :313-323` |
| Manifest schema, leg count, uniqueness or hex format wrong | exit 2 `invalid_manifest` | `:439-462` |
| `expected.json` lacks `inputs` or the probe key | exit 2 `invalid_expected`; wrong digest key → exit 1 `probe source digest does not match its r13 declared digest` | `:490-502, :572-573` |
| Probe output lacks six legs, `status "ok"`, `observed_at`, verified pins, or correct `tool_sha256` | exit 2 `probe_baseline_unusable` | `:350-359` |
| Lane not a git repository | exit 1, wrong reason `git poison positive control is ineffective` | `:570-571, :395-412` |
| `/nonexistent/tameshi-round14-poison` exists | exit 2 `poison_path_exists` before mapping | `:469-472` |
| `git` or `python3` absent from PATH | exit 2 `missing_executable` | `:517-522` |
| Real `tools/pin-disposition.py` reused as the fixture probe | reads the temp `--root` fleet path, likely nonzero → exit 2 or unusable baseline; not hermetic | `:538-540` |

This table is the AttackMapping counterexample surface: an assertion on exit 1 alone
is satisfiable by at least three wrong paths. The recipe therefore pins the
`(status, exit, reasons, checks)` tuple, not just the code.

## 7. Bounded recommendations to ContextGate (via TameshiR15)

1. **Add the root seam and derive the default root from the promoted location.** Preserve
   the historical comparison, mapping and decision semantics; only the path resolution
   changes because `tools/` is two levels shallower than `.ufo/evidence/round-14/`
   (`:46-47`). Without this, the selftest cannot invoke the maintained file against a
   temp root.
2. **Ship the differential pair above as one selftest case.** Baseline exit 0 with zero
   reasons, negative exit 1 with exactly `REASON`, invoked as public CLI subprocesses.
   Pin the literal exit numbers, the reason literal, the check key, and the `runner-mapping`
   field. This satisfies the routed "literal exit and stable finding pair" without a
   fixture for every receipt field.
3. **Keep the receipt round-15-only.** The promoted constant must be
   `.ufo/evidence/round-15/context-receipt.json`; the fixture asserts the round-14 path
   does not exist under the root. The historical round-14 file is read-only history.
4. **If the promoted CLI exposes `findings[].id`, derive it mechanically** from the
   already-computed failed `(leg, check)` pairs and set/order flags (for example
   `mapping.pin_name_and_value_match_manifest`, with the leg carried as data). Declare it
   in source, pin it in this one case, and leave the existing `reasons` strings unchanged.
   Do not invent IDs as required historical tokens; the historical tool has none. If no
   ID field is added, the tokens in §1 are the stable finding pair.
5. **Do not add** snapshot mode, a broad environment comparison, a real probe/runner
   execution, network fixtures, or one fixture per emitted reason for this case. They are
   outside this defect and would import new claims (round-15 lesson: no successor sweep,
   no seventh case, no broad environment independence).

## 8. Evidence executed for this report, and limits

Executed: read-only file reads and `grep`; `python3 -c` JSON reads of
`.ufo/evidence/round-13/pin-manifest.json`, `.ufo/evidence/round-14/context-receipt.json`
and the wave spec; one **in-memory** `re` check of the drafted fixture strings using
regexes transcribed verbatim from `capture-context.py:83-105`, plus the direct five-check
predicate arithmetic on the extracted groups. Result of that draft check:

```text
headers 6  pin pairs 6  rev pairs 6  calls 6
unique legs: headers 6, calls 6, sets equal True
baseline: all five checks true on all six rows
mutated js: header True, pin False, rev True, leg_call True, constant_names True
mutated failed: ['pin_name_and_value_match_manifest']
reason: leg js-kimi-census: pin_name_and_value_match_manifest
other five rows: all true
```

Not executed: no repo script, gate, selftest, fixture subprocess, historical command,
build, lint or formatter. The draft check above validates the fixture text against the
source regexes; it is **not** runtime evidence that the promoted tool exits 0/1, and it
does not attest the historical file's digest. This report is advisory source
reconstruction, not an independent admission decision and not C1 credit.

Limits: the recipe proves only the mapping-false verdict path and its tokens. It does not
prove leg execution, kill rates, suite/dependency/fixture identity, the `observed_at`
exclusion, the exit-64 class, or that configured pins authenticate an author. If the
promoted tool changes `CHECKS` names, the per-leg check structure, the `reason` format, or
the stdout fields, the pinned literals must be re-declared in source and re-pinned; the
exit-1 mapping outcome itself is the stable behavior.
