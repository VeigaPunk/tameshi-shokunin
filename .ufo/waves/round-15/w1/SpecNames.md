# SpecNames — equal-valued REV variable-name mismatch: isolated fixture recipe

Seat: `TameshiR15.SpecNames` (leaf executor, advisory only). Scope: report only.
Report: `.ufo/waves/round-15/w1/SpecNames.md`.
No source edit, no gate/selftest/probe/runner execution, no sibling execution, no
commits. The recipe below is read from committed bytes and is **not** an executed
result; the L1 owns the single post-integration run.

Read revision and evidence (all observed by direct read and `sha256sum`):

| Item | Observed |
|---|---|
| Lane HEAD | `a9cf4da78f2514c7bedd91a850a88590009d7df0` |
| `.ufo/evidence/round-14/capture-context.py` | 647 lines, sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89` |
| `.ufo/evidence/round-14/context-receipt.json` | sha256 `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` |
| `.ufo/evidence/round-14/guardrails.json` | sha256 `cca670b54f5da70873daec8d1bd54749ea63be99582f21138d43c8c715eaf784` |
| `.ufo/evidence/round-13/pin-manifest.json` | sha256 `64eaa43e3f7a928472efa32c7230ca78358235716db04947a93edb0202920af6` |
| `tools/mutate-and-run.sh` | sha256 `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` |
| `tools/context-capture.py` at read | absent |

Tool installs/updates: none. LSP: no LSP device is exposed in this seat's tool
inventory, so symbol navigation was unavailable; the evidence below is direct
line-addressed source reading.

---

## 1. Why this case exists in the historical source

`REV_BASH` and `REV_CHECKLIST` resolve to the same commit, and so do `REV_JS` and
`REV_CLAIMS`:

- `tools/mutate-and-run.sh:545` `REV_BASH=fecee8743e52eb8fb5fbb40782934cb619a1a96e`
- `tools/mutate-and-run.sh:551` `REV_CHECKLIST=fecee8743e52eb8fb5fbb40782934cb619a1a96e`
- `tools/mutate-and-run.sh:543` / `:553` the JS pair, both
  `175de6ba2e9e904010411b19cab27e0af9aad3d4`

The historical checker therefore compares the variable **name** as well as the
resolved value. `EXPECTED_SUFFIX` (`capture-context.py:74-81`) is code-resident and
maps `bash-surface-census -> BASH`, `bash-checklist-run -> CHECKLIST`, etc. The
comment at `:71-73` states the reason directly: equal values mean a value-only
comparison would not catch a wrong binding.

For leg `bash-surface-census`, `mapping_block` computes
(`capture-context.py:287-294`):

```python
checks["rev_name_and_value_match_manifest"] = (
    suffix is not None and rev_name == "REV_" + suffix
    and rev_value == manifest["pinned_commit"]
)
checks["constant_names_match_leg"] = (
    suffix is not None
    and call["pin_suffix"] == call["rev_suffix"] == call["table_suffix"] == suffix
)
```

Replacing the one call-site token `"$REV_BASH"` with `"$REV_CHECKLIST"` leaves
`rev_value == manifest["pinned_commit"]` **true** (the values are equal) while both
name predicates above become false. `reasons` gets
`"leg bash-surface-census: <failed checks in CHECKS order>"` (`:321-323`), and
`decide()` returns `("mismatch", 1, reasons)` (`:576-579`).

### Observable vs source-derived

- **Observed (round-14 retained):** the guardrail
  `runner_variable_swap_discriminator` (`guardrails.json:36-48`, recorded exit 0)
  executed the in-process mutation and asserted
  `not out["all_match"] and not row["checks"]["constant_names_match_leg"]` for
  `bash-surface-census`, printing
  `runner_variable_swap_rejected: equal REV values do not hide wrong binding`.
  That is a helper-level execution, **not** a public-CLI invocation.
- **Source-derived, not executed:** the CLI exit 1, the exact `reasons` string, and
  the receipt fields below. `decide()` at `:576-579` and `main()` at `:630-642`
  determine them, but no round-14 run exercised this case through the CLI.
- **Not claimed:** anything about bash expansion, `git show`, leg execution, or the
  real pins. The check is static text parsing; the runner is never run
  (`capture-context.py:11-14`).

---

## 2. Exact existing tokens and expected exit

Do **not** invent a new predicate or a new taxonomy for this class. The historical
source already emits all three of the following.

| Kind | Exact existing token / value | Authority |
|---|---|---|
| Machine check key (primary) | `constant_names_match_leg` | `capture-context.py:114`, `:291-294` |
| Machine check key (co-fires) | `rev_name_and_value_match_manifest` | `capture-context.py:112`, `:287-290` |
| Exact receipt reason | `leg bash-surface-census: rev_name_and_value_match_manifest, constant_names_match_leg` | `:321-323`, `:576-577` |
| CLI status token | `CONTEXT: MISMATCH` and trailing `runner-mapping=False` | `:636-641` |
| Exit | **1** (`status` = `"mismatch"`) | `:579` |
| Round-14 helper case label (not a CLI ID) | `runner_variable_swap_discriminator` | `guardrails.json:36` |
| Round-14 helper success text (not CLI output) | `runner_variable_swap_rejected: equal REV values do not hide wrong binding` | `guardrails.json:46` |

The two check keys fire in `CHECKS` order, which is why the reason string lists
`rev_name_and_value_match_manifest` before `constant_names_match_leg`. With the
fixture in §3, `set_equal` and `order_equal` are true, so the reason list contains
**exactly one** element. If the promoted gate introduces a finding ID, the
least-invention choice is the existing check key (`constant_names_match_leg`),
optionally namespaced; the exact reason string above should remain the durable
receipt assertion. A rename that drops both existing keys is a semantic change, not
a formatting choice.

---

## 3. Isolated fixture recipe

### 3.1 Placement and containment

Build under one `tempfile.mkdtemp(prefix="tameshi-r15-names-")`, removed in
`finally`:

```text
<tmp>/r/                                  # FLEET_ROOT
<tmp>/r/lane/                             # LANE_ROOT (git init -q here)
<tmp>/r/lane/tools/context-capture.py     # copy of the maintained tool
<tmp>/r/lane/tools/pin-disposition.py     # synthetic probe (below)
<tmp>/r/lane/tools/mutate-and-run.sh      # synthetic runner (below)
<tmp>/r/lane/.ufo/evidence/round-13/pin-manifest.json
<tmp>/r/lane/.ufo/evidence/round-13/expected.json
```

The tool copy at `lane/tools/` makes the corrected `LANE_ROOT =
dirname(dirname(SELF))` resolve to `lane`. If the promoted CLI exposes an explicit
root/output flag (the `evidence-disposition.py --root` precedent), that flag is an
equivalent alternative; the paths and semantics do not change. This placement is
the same containment used by the sibling usage spec (`<tmp>/r/lane/tools/...`).

`git init -q lane` is required: `positive_control_block` runs
`git -C LANE_ROOT rev-parse --git-dir` under baseline and injected env
(`capture-context.py:395-411`). Without a work tree the baseline control fails and
`decide()` adds `git poison positive control is ineffective`, which would destroy
the single-cause assertion. Strip ambient `GIT_*` from the selftest's own setup
environment before `git init`.

Invoke the public CLI as a subprocess with `cwd=lane` (no arguments in the
historical contract; adapt only to the selected CLI contract). The receipt is
written to `lane/.ufo/evidence/round-15/context-receipt.json`, inside the temp root.
No live lane path, no sibling repository, no network, and no write outside `<tmp>`
is needed.

### 3.2 Synthetic runner `tools/mutate-and-run.sh`

Literal pristine fixture (all values synthetic; no real pin is claimed):

```bash
# js-kimi-census        sib-a/scripts/a.mjs      1/1 (100 %)
# bash-surface-census   sib-b/corpus/b.sh        1/1 (100 %)
# bash-tsukuroi-census  sib-c/tools/c.sh         1/1 (100 %)
# bash-mado-verify      sib-d/tools/d.sh         1/1 (100 %)
# bash-checklist-run    sib-b/corpus/e.sh        1/1 (100 %)
# js-claims-check       sib-a/scripts/f.mjs      1/1 (100 %)

PIN_JS=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
REV_JS=1111111111111111111111111111111111111111
PIN_BASH=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
REV_BASH=2222222222222222222222222222222222222222
PIN_TSUKUROI=cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
REV_TSUKUROI=3333333333333333333333333333333333333333
PIN_MADO=dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
REV_MADO=4444444444444444444444444444444444444444
PIN_CHECKLIST=eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
REV_CHECKLIST=2222222222222222222222222222222222222222
PIN_CLAIMS=ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
REV_CLAIMS=1111111111111111111111111111111111111111

run_regression() {
  regression_case_git js-kimi-census 'sib-a/scripts/a.mjs' "$PIN_JS" "$REV_JS" "spec.js" 'node --selftest' "$TABLE_JS"
  regression_case_git bash-surface-census 'sib-b/corpus/b.sh' "$PIN_BASH" "$REV_BASH" "spec.sh" 'bash --selftest' "$TABLE_BASH"
  regression_case_git bash-tsukuroi-census 'sib-c/tools/c.sh' "$PIN_TSUKUROI" "$REV_TSUKUROI" "spec.sh" 'bash --selftest' "$TABLE_TSUKUROI"
  regression_case_git bash-mado-verify 'sib-d/tools/d.sh' "$PIN_MADO" "$REV_MADO" "spec.sh" 'bash --selftest' "$TABLE_MADO"
  regression_case_git bash-checklist-run 'sib-b/corpus/e.sh' "$PIN_CHECKLIST" "$REV_CHECKLIST" "spec.sh" 'bash --selftest' "$TABLE_CHECKLIST"
  regression_case_git js-claims-check 'sib-a/scripts/f.mjs' "$PIN_CLAIMS" "$REV_CLAIMS" "spec.js" 'node --selftest' "$TABLE_CLAIMS"
}
```

Why this shape satisfies the historical parsers:

- `HEADER_ROW_RE` (`:83-88`): six matching `# leg repo/path n/n (n %)` lines.
- `PIN_CONST_RE` / `REV_CONST_RE` (`:89-90`): six unique line-anchored 64-hex and
  40-hex constants. Equal **values** on `REV_BASH`/`REV_CHECKLIST` and
  `REV_JS`/`REV_CLAIMS` do not collapse the dict, because the keys differ.
- `RUN_REGRESSION_RE` (`:104-106`): `run_regression() {` at column 0 and a closing
  `}` at column 0; no nested line begins with `}`.
- `CALL_RE` (`:92-101`): each call is one line with the exact quoted sequence
  `'path' "$PIN_X" "$REV_X" "..." '...' "$TABLE_X"`. Continuations are unnecessary.
- `TABLE_*` need not be defined; the parser only reads the name suffix. `spec.*`
  and command strings are opaque.

### 3.3 Synthetic probe `tools/pin-disposition.py`

The mapping verdict is reached only after a usable probe baseline
(`comparison_block`, `:350-361`), so the fixture probe must emit a valid
`pin-disposition-v1` document and must be deterministic under both environments.
A self-contained fake is sufficient; **no sibling repository, commit, or real file
is needed**:

```python
#!/usr/bin/env python3
import hashlib, json, pathlib

legs = ["js-kimi-census", "bash-surface-census", "bash-tsukuroi-census",
        "bash-mado-verify", "bash-checklist-run", "js-claims-check"]
digest = hashlib.sha256(pathlib.Path(__file__).resolve().read_bytes()).hexdigest()
print(json.dumps({
    "schema": "pin-disposition-v1",
    "status": "ok",
    "observed_at": "2026-10-20T00:00:00Z",
    "tool_sha256": digest,
    "legs": [{"leg": leg, "content_status": "present",
              "pinned": {"status": "verified"}} for leg in legs],
}, sort_keys=True))
```

It ignores the `--manifest` / `--root` arguments, reads only its own file, writes
nothing, calls no git, and produces byte-identical output in baseline and injected
runs. `comparison_block` checks exactly these fields (`:349-377`):
`schema == "pin-disposition-v1"`, `status == "ok"`, six leg rows, no
`content_status == "unavailable"`, every `pinned.status == "verified"`, a top-level
`observed_at`, and `tool_sha256` equal to the probe's on-disk digest.

### 3.4 Manifest and expected input

`lane/.ufo/evidence/round-13/pin-manifest.json`:

```json
{
  "schema": "pin-manifest-v1",
  "derived_from": {
    "path": "tools/mutate-and-run.sh",
    "sha256": "<sha256 of the runner bytes written for this variant>"
  },
  "legs": [
    {"leg": "js-kimi-census", "repo": "sib-a", "path": "scripts/a.mjs",
     "pinned_commit": "1111111111111111111111111111111111111111",
     "expected_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
    {"leg": "bash-surface-census", "repo": "sib-b", "path": "corpus/b.sh",
     "pinned_commit": "2222222222222222222222222222222222222222",
     "expected_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},
    {"leg": "bash-tsukuroi-census", "repo": "sib-c", "path": "tools/c.sh",
     "pinned_commit": "3333333333333333333333333333333333333333",
     "expected_sha256": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"},
    {"leg": "bash-mado-verify", "repo": "sib-d", "path": "tools/d.sh",
     "pinned_commit": "4444444444444444444444444444444444444444",
     "expected_sha256": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"},
    {"leg": "bash-checklist-run", "repo": "sib-b", "path": "corpus/e.sh",
     "pinned_commit": "2222222222222222222222222222222222222222",
     "expected_sha256": "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"},
    {"leg": "js-claims-check", "repo": "sib-a", "path": "scripts/f.mjs",
     "pinned_commit": "1111111111111111111111111111111111111111",
     "expected_sha256": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"}
  ]
}
```

The bash legs share `pinned_commit` exactly as the real runner does; the manifest
carries no variable names, so the name table remains code-side.

`lane/.ufo/evidence/round-13/expected.json`:

```json
{
  "schema": "tameshi-round13-evidence-v1",
  "baseline": "0000000000000000000000000000000000000000",
  "inputs": {
    "tools/pin-disposition.py": "<sha256 of the probe bytes written>"
  },
  "expected_checks": {}
}
```

`evaluate()` reads only `inputs[PROBE_REL]` (`:490-497`); the manifest is read from
`MANIFEST_REL`, and the runner digest is compared to `derived_from.sha256`
(`:504-509`). If the promoted tool relocates or renames these relative inputs,
place the same fixtures at its declared relatives; do not point at the live lane.

### 3.5 Digest policy for the variants

Write each runner variant first, then compute and write
`derived_from.sha256` from **that variant's** bytes; likewise compute the probe
digest after writing the probe. This produces a self-consistent synthetic baseline
and means the runner-source digest check passes. That is deliberate: it isolates
the name check as the **only** remaining detector.

If the manifest digest is instead left at the pristine runner's digest, `decide()`
adds `runner source digest does not match the manifest declaration` **before** the
leg reason, and the expected reason list becomes:

```text
["runner source digest does not match the manifest declaration",
 "leg bash-surface-census: rev_name_and_value_match_manifest, constant_names_match_leg"]
```

That variant is optional and only useful to pin reason ordering; it is not the
single-cause fixture and must not be used to claim the name check fired alone.

---

## 4. The two cases

Both cases use identical bytes except for (a) the one call-site token and (b) the
manifest's `derived_from.sha256`, which is recomputed for the variant.

### Case `names-equal-value-swap` (required)

Mutation applied to the fixture runner, exactly once:

```text
"$REV_BASH"  ->  "$REV_CHECKLIST"
```

on the `bash-surface-census` call. This mirrors the retained guardrail mutation
(`guardrails.json:36-48`) and leaves the declared `REV_BASH` constant present but
unreferenced. `REV_BASH` and `REV_CHECKLIST` remain value-equal.

Expected public-CLI pair:

| Observable | Literal expected value |
|---|---|
| Process exit | `1` |
| Receipt `status` | `"mismatch"` |
| Receipt `exit` | `1` |
| Receipt `mapping.all_match` | `false` |
| Receipt `mapping.leg_set_equal` | `true` |
| Receipt `mapping.leg_order_equal` | `true` |
| Receipt `mapping.reasons` | `["leg bash-surface-census: rev_name_and_value_match_manifest, constant_names_match_leg"]` |
| Receipt `sources.runner.matches_manifest_declaration` | `true` (proves the digest did not fire) |
| Receipt `comparison.equal` | `true` |
| Receipt `positive_control.effective` | `true` |
| Row `bash-surface-census` `runner_call.rev_constant` | `"REV_CHECKLIST"` |
| Row `bash-surface-census` `declared_variable_suffix` | `"BASH"` |
| Row `bash-surface-census` `rev_value` | `"2222222222222222222222222222222222222222"` |
| Row `bash-surface-census` `manifest.pinned_commit` | `"2222222222222222222222222222222222222222"` (equal-value premise) |
| Row `bash-surface-census` `checks.constant_names_match_leg` | `false` |
| Row `bash-surface-census` `checks.rev_name_and_value_match_manifest` | `false` |
| Row `bash-surface-census` `checks.header_matches_manifest` | `true` |
| Row `bash-surface-census` `checks.pin_name_and_value_match_manifest` | `true` |
| Row `bash-surface-census` `checks.leg_call_matches_manifest` | `true` |
| Row `bash-surface-census` `match` | `false` |
| Row `bash-checklist-run` `checks` (all five), `match` | all `true` |
| stdout | contains `CONTEXT: MISMATCH` and the substring `exit=1 probe-equal=True poison-control=True runner-mapping=False)` |

The stdout substring is the historical format (`:636-641`); pin only the stable
portion if the promoted line is reworded, and treat the receipt fields as the
durable contract.

### Case `names-pristine-control` (required companion)

Same fixture with the original `"$REV_BASH"` call token and the corresponding
manifest digest. Expected: exit `0`, `status == "ok"`, `reasons == []`,
`mapping.all_match == true`, all six rows `match == true`. This is not a new
predicate; it proves the swap case fails because of the name swap, not because the
synthetic fixture is malformed. The round-14 guardrail also asserted the pristine
mapping passed before mutating (`guardrails.json:40-41`).

---

## 5. What is deliberately not required

- **No new validation feature.** The two existing checks catch this case. Do not add
  a general variable-reference linter, an unused-constant rule, a shell-expansion
  resolver, or a manifest variable-name field for this fixture. `REV_BASH` being
  declared but unreferenced after the swap is **expected** and must not be treated
  as an error.
- **No runner execution.** No `bash`, `node`, `git show`, or sibling repository is
  needed. The check is static parsing (`capture-context.py:11-14`).
- **No real pins.** The synthetic constants are fixture values, not claims about
  `kagi-shokunin`, `kumitate-shokunin`, or any recorded revision.
- **No claim of whole-class coverage.** This recipe pins one direction:
  `bash-surface-census` misbound to `REV_CHECKLIST`. The reverse direction and the
  `REV_JS`/`REV_CLAIMS` pair are the same mechanism; adding them is cheap but
  optional and is not required by this ticket. Do not describe one direction as
  proof for all four.
- **No exit-2 case here.** An unquoted or otherwise unparseable REV spelling is a
  different class (`runner_unparsed`, exit 2) and belongs to the JSON/parse seat,
  not this fixture.

---

## 6. Implementation-critical notes for the gate executor

1. **Root depth.** The historical `LANE_ROOT = dirname^4(SELF)`
   (`capture-context.py:46`) is correct only at
   `.ufo/evidence/round-14/capture-context.py`. At `tools/context-capture.py` it
   resolves one level too high. The promoted tool must use
   `dirname(dirname(SELF))` or an explicit `--root`, and its selftest must run the
   copy at `<tmp>/r/lane/tools/context-capture.py` (or pass the temp root) so no
   live path is read.
2. **Preserve the two check keys and the reason composition.** The fixture pins
   `constant_names_match_leg` and `rev_name_and_value_match_manifest` and the exact
   `"leg <leg>: <checks in CHECKS order>"` string. If the selected CLI contract
   emits a new finding ID, pin the mapping from the existing key rather than
   silently renaming the check.
3. **Recompute the manifest digest per variant.** Without it, the runner-source
   digest reason appears first and the fixture no longer isolates the name check.
   Do not weaken the digest check itself; only the synthetic baseline's declared
   digest is recomputed.
4. **Keep round-14 bytes untouched.** The fixture copies or generates its own
   `tools/mutate-and-run.sh`, probe, manifest, and expected file under `<tmp>`. Do
   not read `.ufo/evidence/round-14/*` from the selftest and do not write the
   round-14 receipt. Normal capture writes only the round-15 output path.
5. **The fake probe must self-hash.** `payload_tool_sha256_matches_disk` compares
   the probe document's `tool_sha256` to the on-disk probe digest. A constant or
   absent field turns the case into a probe mismatch and masks the mapping verdict.
6. **Exit 1 must come from `decide()`.** If the promoted `main()` adds a catch-all,
   map unexpected exceptions to the could-not-evaluate class, not to 1; otherwise a
   fixture crash could be misread as the mapping finding. This is a general exit
   hygiene note already owned by the control critics; it is listed here only
   because the fixture's literal `(exit 1, token)` pair depends on it.

---

## 7. Residual risks

- The promoted tool's schema/flag names are not yet fixed at this read. The
  assertions above use the historical receipt keys (`mapping.legs[].checks`,
  `mapping.reasons`, `sources.runner...`). If the selected contract changes them,
  the fixture must be re-read against the final tool and the literal pairs updated;
  the **semantics** (equal values do not hide a wrong name; exit 1; those two
  checks false) must not change.
- The fixture assumes the baseline probe can be satisfied by a six-leg synthetic
  document. If the promoted tool tightens probe validation beyond the historical
  predicates, the fake probe may need additional fixed fields; that would be a new
  contract and must be stated by the gate executor, not inferred here.
- `git` is required for the positive control in the fixture. If it is absent, the
  historical code exits 2 before a mapping verdict; the selftest should report that
  as a fixture precondition failure, not as the expected swap result.
- `RUN_REGRESSION_RE` stops at the first column-0 `}`; the fixture's single
  function body is deliberately minimal so that boundary cannot be confused with a
  second function.
- This seat executed nothing: no gate, selftest, probe, runner, git gate, or
  sibling check. The expected pairs are source-derived and are explicitly labeled
  as such.

---

## 8. One-line handoff

For the promoted `tools/context-capture.py --selftest`, pin the case
`names-equal-value-swap` at exit **1** with the existing token
`constant_names_match_leg` (co-firing `rev_name_and_value_match_manifest`) and the
exact reason
`leg bash-surface-census: rev_name_and_value_match_manifest, constant_names_match_leg`,
using the synthetic six-leg fixture above, a self-hashing fake probe, a `git init`
temp lane, and a manifest digest recomputed for the mutated runner. Pair it with
the pristine exit-0 control. No new predicate is required.
