# SpecSourcePins — source digest and expected input digests: fixture recipe, tokens, exits

Seat: `TameshiR15.SpecSourcePins` (executor, leaf). Assignment: read the
historical `capture-context.py` relevant functions and draft only a concrete
isolated fixture recipe for the **source digest** predicates and the
**expected input digests**, with the exact existing stable token and expected
exit where the historical source supports one. No new broad validation
feature; no source edits; no verification execution.

Evidence basis: static reads only, 2026-10-20, lane HEAD
`a9cf4da78f2514c7bedd91a850a88590009d7df0`. **Nothing was executed** — no
gate, selftest, fixture, probe, git control, build, lint or formatter was run.
No tool was installed or updated. Historical bytes are unchanged:
`git status --porcelain -- .ufo/evidence/round-14 tools` is empty.

## 1. Verdict (bounded)

The historical tool has exactly **three source-file digest predicates** that
can produce a verdict, all computed once during `evaluate()` and frozen as
booleans in the receipt:

1. probe file digest vs `expected.json.inputs["tools/pin-disposition.py"]`
   (`sources.probe.matches_declared`);
2. runner file digest vs `manifest.derived_from.sha256` **and**
   `derived_from.path.endswith("tools/mutate-and-run.sh")`
   (`sources.runner.matches_manifest_declaration`);
3. probe-reported `tool_sha256` vs the probe file digest on disk
   (`comparison.payload_tool_sha256_matches_disk`).

Every well-formed disagreement in those three is exit **1**, status
`mismatch`, with one exact literal reason string. A **malformed digest shape**
(`manifest.legs[].expected_sha256` not 64 lowercase hex, or `pinned_commit` not
40 lowercase hex) is a different class: exit **2**, status `invalid_input`,
kind `invalid_manifest`. A missing/non-object `inputs` in `expected.json` is
exit **2**, kind `invalid_expected`. An `inputs` object that simply lacks the
probe key is **not** invalid input: it is the probe-digest mismatch (exit 1).

The fixture recipe below makes a hermetic temp lane whose probe is
self-digesting at run time (a literal self-digest is a hash fixed point and is
impossible), whose expected digests are computed after the input bytes are
written, and whose runner/manifest constants are mutually consistent so that
exactly one digest predicate is false per negative case.

## 2. Exact anchors read

| Claim | Anchor (`.ufo/evidence/round-14/capture-context.py`, 647 lines) |
|---|---|
| Exit map `0/1/2/64` | `:26-29` |
| Input paths `tools/pin-disposition.py`, `tools/mutate-and-run.sh`, `.ufo/evidence/round-13/{pin-manifest,expected}.json` | `:54-57`; historical output `:58` |
| Six declared variable suffixes `JS/BASH/TSUKUROI/MADO/CHECKLIST/CLAIMS` | `:74-81` |
| Runner header / `PIN_` / `REV_` / call / function-body parsers | `:83-107` |
| Five mapping check names | `:109-115`; failure composition `:261-333` |
| Baseline probe acceptance (six legs, no `unavailable`, `pinned.status == "verified"`, top-level `observed_at`) | `:350-361` |
| `payload_tool_sha256_matches_disk` = both runs' `tool_sha256` equal the disk digest | `:380-383` |
| Normalization removes **only** top-level `observed_at`; canonical JSON compared | `:384-390` |
| Sources recorded: four `path`+`sha256` entries | `:480-487` |
| `probe_declared = inputs.get(PROBE_REL)`; `matches_declared` requires a `str` equal to the disk digest | `:496-503` |
| `matches_manifest_declaration` requires `str` digest, `str` path ending in `tools/mutate-and-run.sh`, and equal digest | `:497-511` |
| Manifest digest **shape** validation (40/64 lowercase hex) | `:456-461` |
| Missing/non-object `inputs` raises `invalid_expected` | `:490-493` |
| Probe subprocess argv is `[python3, "tools/pin-disposition.py", "--manifest", ..., "--root", FLEET_ROOT]`, cwd = lane | `:517-540` |
| Reason literals and `is True` / `is False` identity tests in `decide()` | `:553-581` |
| Exit1 receipt written, then `CONTEXT: MISMATCH` printed | `:632-645` |
| Exit2 receipt written with `status=invalid_input`, `error.kind`, reason `kind + ": " + message` | `:617-630` |
| No standalone selftest exists in the historical script | `grep -c -- '--selftest'` = **0** |
| Retained receipt agrees | `.ufo/evidence/round-14/context-receipt.json`: `schema=tameshi-round14-context-receipt-v1`, `status=ok`, `exit=0`, both `matches_*` true, `payload_tool_sha256_matches_disk=true` |

Measured static identities (read, not executed): script sha256
`7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`;
receipt sha256
`05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a`;
last commit touching either path `64314783836bb0d05ad06a774d7310fd3a23b5bd`;
working tree clean for those paths.

## 3. What each digest is bound to (and what is *not* checked)

| Digest | Producer | Compared to | Predicate | Class if false |
|---|---|---|---|---|
| Probe file sha256 `P` | `evaluate()` over `lane/tools/pin-disposition.py` | `expected.json.inputs["tools/pin-disposition.py"]` | `matches_declared` | 1 `mismatch` |
| Runner file sha256 `R` | `evaluate()` over `lane/tools/mutate-and-run.sh` | `manifest.derived_from.sha256`, path suffix `tools/mutate-and-run.sh` | `matches_manifest_declaration` | 1 `mismatch` |
| Probe payload `tool_sha256` | both probe runs | disk digest `P` (from `evaluate()`) | `payload_tool_sha256_matches_disk` | 1 `mismatch` |
| Manifest leg `expected_sha256` | fixture constant | runner `PIN_<SUFFIX>` constant **only** | `pin_name_and_value_match_manifest` | 1 `mismatch` (mapping lane) |
| Manifest leg `pinned_commit` | fixture constant | runner `REV_<SUFFIX>` constant **only** | `rev_name_and_value_match_manifest` | 1 `mismatch` (mapping lane) |

Non-checks, stated so no fixture invents them:

- `sources.manifest.sha256` and `sources.expected_r13.sha256` are **recorded
  only**; `decide()` has no predicate over them.
- Only the single probe key of `expected.json.inputs` is consumed. The real
  round-13 `expected.json` carries thirteen input digests; the other twelve are
  not read by this tool. Do not turn the fixture into a loop over all keys.
- `manifest.legs[].expected_sha256` is a *declared content pin* compared to the
  runner constant; it is not the hash of any fixture-local file, and the
  sibling targets do not need to exist. The runner is never executed.
- The historical script never re-hashes the live lane during `decide()`. Any
  retained-receipt check must replay the recorded booleans, not re-read live
  sources.

## 4. Hermetic fixture recipe

### 4.1 Layout and invariants

```text
<tmp>/                                  # FLEET_ROOT: must exist (os.path.isdir)
  lane/                                 # LANE_ROOT
    .git/                               # git init -q: positive-control baseline needs a repo
    tools/
      context-capture.py                # byte copy of the active gate (LANE_ROOT derivation under test)
      pin-disposition.py                # synthetic probe; digest P
      mutate-and-run.sh                 # synthetic runner; digest R
    .ufo/evidence/round-13/
      pin-manifest.json                 # six legs; derived_from.sha256 == R
      expected.json                     # inputs["tools/pin-disposition.py"] == P
    .ufo/evidence/round-15/             # capture output (created by the tool)
```

Invariants that make the fixture hermetic and the digests meaningful:

1. `<tmp>` is `tempfile.mkdtemp(prefix="tameshi-r15-context-")`; nothing is
   written outside it. The probe is a regular file, never a symlink.
2. The active tool is copied to the **same lane-relative path** it occupies in
   production (`tools/context-capture.py`), so the lane-root derivation runs
   unchanged: two parent levels from `tools/context-capture.py` give
   `<lane>`, and `<lane>`'s parent gives `FLEET_ROOT` (the historical four
   levels were an artifact of the archived
   `.ufo/evidence/round-14/` location and must not be reused).
3. The synthetic probe computes its **own** sha256 at run time by reading its
   own bytes. A literal digest embedded in the probe is a fixed point and
   cannot equal the sha256 of a file that contains it.
4. `P` and `R` are computed **after** the probe/runner bytes are written, then
   embedded in `expected.json` / `pin-manifest.json`. There is no cycle:
   expected/manifest bytes are not themselves hashed by any predicate.
5. The fixture lane is `git init -q`-ed so the injected `GIT_DIR` positive
   control has a baseline exit 0 with nonempty stdout (`.git`). This is local
   and temp-only; no network and no host repository read.
6. The selftest runs the **public CLI in a subprocess** with cwd = `lane` and
   an env that keeps `PATH` (for `python3`/`git`) and sets
   `LC_ALL=C`, `HOME=<tmp>`, `GIT_CONFIG_NOSYSTEM=1`,
   `GIT_CONFIG_GLOBAL=/dev/null`. The tool itself strips all `GIT_*` ambient
   keys; the fixture must not pre-strip the injection it is testing.

### 4.2 Fixture builder (stdlib only; recipe, not executed)

```python
import hashlib, json, os, subprocess, sys

LEGS = [
    ("js-kimi-census",       "JS",        "kimi",      "census.py"),
    ("bash-surface-census",  "BASH",      "surface",   "census.sh"),
    ("bash-tsukuroi-census", "TSUKUROI",  "tsukuroi",  "census.sh"),
    ("bash-mado-verify",     "MADO",      "mado",      "verify.sh"),
    ("bash-checklist-run",   "CHECKLIST", "checklist", "run.sh"),
    ("js-claims-check",      "CLAIMS",    "claims",    "check.mjs"),
]

PROBE_SELF = '''#!/usr/bin/env python3
import hashlib, json, os
own = hashlib.sha256(open(os.path.realpath(__file__), "rb").read()).hexdigest()
legs = [{"leg": "fixture-%d" % i, "content_status": "verified",
         "pinned": {"status": "verified"}} for i in range(6)]
print(json.dumps({"schema": "pin-disposition-v1", "status": "ok",
                  "tool_sha256": own,
                  "observed_at": "2026-10-20T00:00:00Z",
                  "legs": legs}, sort_keys=True))
'''

PROBE_LITERAL = '''#!/usr/bin/env python3
import json
legs = [{"leg": "fixture-%d" % i, "content_status": "verified",
         "pinned": {"status": "verified"}} for i in range(6)]
print(json.dumps({"schema": "pin-disposition-v1", "status": "ok",
                  "tool_sha256": "__DIGEST__",
                  "observed_at": "2026-10-20T00:00:00Z",
                  "legs": legs}, sort_keys=True))
'''

def _write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data if isinstance(data, bytes) else data.encode())

def fixture_env(root):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update({"LC_ALL": "C", "HOME": root,
                "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull})
    return env

def build(root, *, declared_probe=None, declared_runner=None,
          runner_path="tameshi-shokunin/tools/mutate-and-run.sh",
          payload_literal=None, pin_digest=None, inputs=None):
    lane = os.path.join(root, "lane")
    if payload_literal is None:
        probe = PROBE_SELF.encode()
    else:
        probe = PROBE_LITERAL.replace("__DIGEST__", payload_literal).encode()
    _write(os.path.join(lane, "tools/pin-disposition.py"), probe)
    probe_sha = hashlib.sha256(probe).hexdigest()

    pin = {leg: hashlib.sha256(("pin:" + leg).encode()).hexdigest()
           for leg, _s, _r, _p in LEGS}
    rev = {leg: hashlib.sha1(("rev:" + leg).encode()).hexdigest()
           for leg, _s, _r, _p in LEGS}
    manifest_pin = dict(pin)
    if pin_digest is not None:
        manifest_pin[LEGS[0][0]] = pin_digest

    lines = ["# {} {}/{} 3/4 (75%)".format(leg, repo, path)
             for leg, _s, repo, path in LEGS]
    lines += ["PIN_{}={}".format(s, pin[leg]) for leg, s, _r, _p in LEGS]
    lines += ["REV_{}={}".format(s, rev[leg]) for leg, s, _r, _p in LEGS]
    lines += ["", "run_regression() {"]
    lines += ["  regression_case_git {l} '{r}/{p}' \"$PIN_{s}\" \"$REV_{s}\" "
              "\"census\" 'kat' \"$TABLE_{s}\"".format(l=leg, r=repo, p=path, s=s)
              for leg, s, repo, path in LEGS]
    lines += ["}", ""]
    runner = "\n".join(lines)
    _write(os.path.join(lane, "tools/mutate-and-run.sh"), runner)
    runner_sha = hashlib.sha256(runner.encode()).hexdigest()

    manifest = {
        "schema": "pin-manifest-v1",
        "derived_from": {"path": runner_path,
                         "sha256": runner_sha if declared_runner is None else declared_runner},
        "legs": [{"leg": leg, "repo": repo, "path": path,
                  "pinned_commit": rev[leg], "expected_sha256": manifest_pin[leg]}
                 for leg, _s, repo, path in LEGS],
    }
    _write(os.path.join(lane, ".ufo/evidence/round-13/pin-manifest.json"),
           json.dumps(manifest, indent=2) + "\n")

    expected_inputs = {"tools/pin-disposition.py":
                       probe_sha if declared_probe is None else declared_probe}
    if inputs is not None:
        expected_inputs = inputs
    _write(os.path.join(lane, ".ufo/evidence/round-13/expected.json"),
           json.dumps({"inputs": expected_inputs}, indent=2) + "\n")

    _write(os.path.join(lane, "tools/context-capture.py"),
           open(os.path.realpath(__file__), "rb").read())
    subprocess.run(["git", "-C", lane, "init", "-q"], env=fixture_env(root),
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return lane, probe_sha, runner_sha

def run_capture(root, lane):
    return subprocess.run(
        [sys.executable, os.path.join(lane, "tools/context-capture.py")],
        cwd=lane, env=fixture_env(root), stdin=subprocess.DEVNULL,
        capture_output=True, text=True, timeout=120)
```

The receipt is read from `<lane>/.ufo/evidence/round-15/context-receipt.json`
(historical `OUTPUT_REL` is the round-14 path and must not be the promoted
tool's normal write target). Every assertion below is over that parsed JSON,
not over stdout prose.

### 4.3 Case matrix (literal exits and exact stable finding tokens)

All cases use the same builder; overrides are the only difference. Each
negative case leaves every other predicate clean, so `decide()` emits exactly
one reason in its fixed order.

| # | Builder override | Exit | `status` | Exact `reasons` (existing literal) |
|---|---|---:|---|---|
| D0 | none | 0 | `ok` | `[]` |
| D1 | `declared_probe="0" * 64` | 1 | `mismatch` | `["probe source digest does not match its r13 declared digest"]` |
| D2 | `declared_runner="1" * 64` | 1 | `mismatch` | `["runner source digest does not match the manifest declaration"]` |
| D2b | `runner_path="tameshi-shokunin/tools/mutate-and-run.sh.bak"` (digest correct) | 1 | `mismatch` | same as D2 |
| D3 | `payload_literal="2" * 64` | 1 | `mismatch` | `["probe payload tool_sha256 does not match the disk digest"]` |
| D4 | `inputs={}` | 1 | `mismatch` | `["probe source digest does not match its r13 declared digest"]` |
| D5 | `pin_digest="xyz"` | 2 | `invalid_input` | `["invalid_manifest: leg js-kimi-census sha256 not 64 hex"]` |
| D6 | `inputs=[]` | 2 | `invalid_input` | `["invalid_expected: expected.json has no inputs object"]` |

D0 field pins:

```python
assert proc.returncode == 0
assert receipt["status"] == "ok" and receipt["exit"] == 0 and receipt["reasons"] == []
assert receipt["sources"]["probe"]["sha256"] == probe_sha          # exact bytes hashed
assert receipt["sources"]["probe"]["declared_sha256"] == probe_sha
assert receipt["sources"]["probe"]["matches_declared"] is True
assert receipt["sources"]["runner"]["sha256"] == runner_sha
assert receipt["sources"]["runner"]["manifest_declared_sha256"] == runner_sha
assert receipt["sources"]["runner"]["matches_manifest_declaration"] is True
assert receipt["comparison"]["payload_tool_sha256_matches_disk"] is True
assert receipt["mapping"]["all_match"] is True
```

D1 field pins (the declaration is the only false thing):

```python
assert proc.returncode == 1 and receipt["status"] == "mismatch"
assert receipt["reasons"] == ["probe source digest does not match its r13 declared digest"]
assert receipt["sources"]["probe"]["sha256"] == probe_sha
assert receipt["sources"]["probe"]["declared_sha256"] == "0" * 64
assert receipt["sources"]["probe"]["matches_declared"] is False
assert receipt["comparison"]["payload_tool_sha256_matches_disk"] is True
assert receipt["mapping"]["all_match"] is True
```

D2 / D2b field pins:

```python
assert proc.returncode == 1
assert receipt["reasons"] == ["runner source digest does not match the manifest declaration"]
assert receipt["sources"]["runner"]["matches_manifest_declaration"] is False
# D2:  manifest_declared_sha256 == "1" * 64, sha256 == runner_sha
# D2b: manifest_declared_sha256 == runner_sha, derived_from.path has the wrong suffix
```

D3 field pins (comparison stays equal; only the payload digest is false):

```python
assert proc.returncode == 1
assert receipt["comparison"]["equal"] is True
assert receipt["comparison"]["payload_tool_sha256_matches_disk"] is False
assert receipt["reasons"] == ["probe payload tool_sha256 does not match the disk digest"]
```

D4 field pins (absent key is *not* invalid input):

```python
assert proc.returncode == 1 and receipt["status"] == "mismatch"
assert receipt["sources"]["probe"]["declared_sha256"] is None
assert receipt["sources"]["probe"]["matches_declared"] is False
assert receipt["reasons"] == ["probe source digest does not match its r13 declared digest"]
```

D5 / D6 field pins (could-not-evaluate class):

```python
assert proc.returncode == 2
assert receipt["status"] == "invalid_input" and receipt["exit"] == 2
assert receipt["error"]["kind"] == "invalid_manifest"      # D5, or "invalid_expected" D6
```

## 5. Exact stable token inventory (existing literals only)

| Token | Kind | Exit | Source |
|---|---|---:|---|
| `ok` / `mismatch` / `invalid_input` | receipt `status` | 0 / 1 / 2 | `:553-581`, `:617-630` |
| `probe source digest does not match its r13 declared digest` | `reasons[]` literal | 1 | `:572-573` |
| `runner source digest does not match the manifest declaration` | `reasons[]` literal | 1 | `:574-575` |
| `probe payload tool_sha256 does not match the disk digest` | `reasons[]` literal | 1 | `:564-565` |
| `leg {leg}: {check_names}` | `reasons[]` composition | 1 | `:323` |
| `pin_name_and_value_match_manifest`, `rev_name_and_value_match_manifest`, `header_matches_manifest`, `leg_call_matches_manifest`, `constant_names_match_leg` | per-leg `checks` keys | 1 when false | `:109-115` |
| `invalid_manifest`, `invalid_expected`, `missing_input`, `invalid_json` | `error.kind` and `reasons[0]` prefix | 2 | `:439-462`, `:490-495`, `:145-180` |
| `matches_declared`, `matches_manifest_declaration`, `payload_tool_sha256_matches_disk` | boolean field names | — | `:496-511`, `:380` |
| `pin-disposition-v1`, `pin-manifest-v1`, `tameshi-round14-context-receipt-v1` | schema strings | — | `:49-52` |

There is no separate finding-ID namespace in the historical tool. The reason
strings and `error.kind` values **are** the stable finding vocabulary; every
mapping failure is `leg <leg>: <check-name>`. If the promoted gate introduces
short IDs, they must be bound one-to-one to these literals and the literals must
remain byte-identical (a retained round-14 receipt records them, and a replay
of `decide()` over it must reproduce them).

## 6. Classification boundaries (do not fold into each other)

- **Well-formed but unequal digest** → exit 1 `mismatch` (D1/D2/D2b/D3).
- **Malformed digest shape** (manifest `expected_sha256`/`pinned_commit`) →
  exit 2 `invalid_manifest` (D5). Validation runs before any comparison.
- **`expected.json.inputs` absent or not an object** → exit 2
  `invalid_expected` (D6). Present object missing the probe key → exit 1 (D4).
- **Per-leg `expected_sha256` unequal to the runner PIN but well-formed** →
  exit 1 `leg <leg>: pin_name_and_value_match_manifest`. This is the mapping
  lane's assigned case (`SpecMapping`); this seat only fixes the digest-binding
  fact so the two fixtures cannot contradict each other.
- **Pinned receipt/snapshot digest disagreement** → `SpecTamper`'s assigned
  class (`snapshot_tampered`, exit 2, per `repeat-control.py:42-44`). It is a
  *promoted* mode; the historical script has zero `snapshot`/`tamper`
  occurrences. Do not reuse the three source-digest reason strings for it.
  Source-digest fixtures pin exits and reason tokens, not receipt bytes: a
  capture receipt carries run-specific `observed_at`, `lane_root`, `fleet_root`
  and `invocation`, so literal receipt-byte pinning belongs to a frozen
  snapshot, not to these cases.
- **Usage** → exit 64, stderr `capture-context.py: unexpected argument(s): ...`
  plus the usage block, no receipt (`SpecUsage`'s assigned class). No
  source-digest case maps to 64.

## 7. Recommendations to ContextGate (bounded, implementable)

1. **Implement the three digest cases as CLI subprocess fixtures** exactly as
   in §4.3 (D1, D2, D2b, D3), plus D0 and the two shape/parse exit-2 cases.
   Each test asserts the literal exit, `status`, the exact `reasons` list and
   the named boolean fields. Do not assert stdout prose as the primary token;
   stdout prefixes `CONTEXT: OK`, `CONTEXT: MISMATCH`, `CONTEXT: INVALID` are
   historical display strings.
2. **Compute the probe's payload digest at probe run time** from its own bytes
   (`open(os.path.realpath(__file__), "rb")`). Never embed a literal in the
   self-digest probe; that is an unsatisfiable fixed point.
3. **Compute `P`/`R` after writing the bytes**, then write
   `expected.json.inputs["tools/pin-disposition.py"] = P` and
   `pin-manifest.derived_from = {"path": ".../tools/mutate-and-run.sh",
   "sha256": R}`. Use a lane-relative or fleet-relative path whose string
   really ends with `tools/mutate-and-run.sh`; `endswith` is part of the
   predicate, so D2b is a distinct arm.
4. **Place the tool copy at `<lane>/tools/context-capture.py`** and run it with
   cwd `<lane>`. Derive the lane root as two parent levels of the realpath of
   `__file__` (that is the promoted analogue of the historical four-level
   derivation), so the fixture exercises production root discovery without a
   test-only flag. If the promoted tool already needs an explicit root for
   round-15 output selection, passing that root is the acceptable alternative.
5. **`git init -q` the fixture lane** for the positive-control baseline. Keep
   the historical `GIT_DIR` injection constant and treat
   `/nonexistent/tameshi-round14-poison` absence as a documented fixture
   precondition; do not create that path (outside the temp root). If the
   promoted tool renames the poison path, apply the same precondition to the
   new literal.
6. **Keep every `decide()`/mapping reason literal and the five `CHECKS` names
   byte-identical.** A retained round-14 receipt records them; a check mode
   that replays `decide()` and compares to the recorded finding would otherwise
   declare the historical receipt false.
7. **In a retained-receipt check mode, treat recorded booleans as verdict
   inputs, not structure.** `matches_declared: false` and
   `payload_tool_sha256_matches_disk: false` are well-formed receipts that must
   replay to exit 1; rejecting them as invalid structure would erase the very
   digest verdicts this gate exists to report. Use identity (`is True` /
   `is False`) on parsed JSON, matching `decide()`.
8. **Do not add digest predicates over `sources.manifest.sha256` or
   `sources.expected_r13.sha256`, and do not iterate all `expected.json`
   inputs.** The historical tool records but never compares them. A fixture
   cannot honestly support an exit for a predicate that does not exist.
9. **Do not re-hash live lane inputs in check mode.** The digest predicates are
   computed during capture and frozen as booleans; re-hashing would broaden the
   claim beyond the recorded experiment.

## 8. Risks and limits

- **Host precondition:** `/nonexistent/tameshi-round14-poison` must not exist.
  If it does, clean fixtures exit 2 `poison_path_exists` before any digest
  predicate. This is inherited from the historical constant, not a fixture
  degree of freedom.
- **Executables:** `python3` and `git` must be on `PATH`; otherwise exit 2
  `missing_executable` (`:517-522`).
- **Probe file type:** the probe must be a regular file in the lane; a symlink
  to bytes outside the lane makes the payload self-digest differ from the
  tool's lane-path digest.
- **Runner parser strictness:** extra `PIN_`/`REV_` definition lines, or a
  missing/repeated leg, exit 2 `runner_unparsed` before any digest comparison.
  Keep exactly six of each, at column 0.
- **This fixture proves the gate's predicates with a synthetic probe.** It does
  not re-verify the real `tools/pin-disposition.py` content observations; that
  remains the real probe's own `--selftest` scope.
- **No executed evidence is claimed here.** Every expected exit/token above is
  read from the historical source and the committed round-14 receipt; no
  fixture, subprocess, git control or selftest was run by this seat.

## 9. Tooling and write scope

No tool installed or updated (`pacman`/`uv`/`cargo`/`npm` unused; no binary
fetched). No source file edited. The only write is this report under
`.ufo/waves/round-15/w1/`.
