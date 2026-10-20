# SpecTimestamp — observed_at volatile-exclusion fixture recipe

Seat: `TameshiR15.SpecTimestamp` (executor, leaf). Scope: report only; no source edits, no gate/selftest execution.
Lane root: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Historical source is read-only evidence.

## Verdict in one paragraph

The historical comparison *does* have one exact volatile-exclusion rule: parse both probe
stdout documents, remove **only the top-level `observed_at`** key, canonicalize with
`json.dumps(..., sort_keys=True, separators=(",", ":"))`, and compare the resulting strings
(`.ufo/evidence/round-14/capture-context.py:350-393`). There is **no existing per-predicate
finding ID** for this rule; the observable stable tokens are the literal
`comparison.exclusions`/`comparison.normalization` values, the `probe-equal=` stdout token,
`comparison.equal`, and the decide-time reason string on failure. In a fully passing fixture
the exact expected exit is **0**. The retained round-14 receipt does **not** exercise the
exclusion: both runs printed the same `observed_at` (`2026-10-20T06:35:01Z`) and
`raw_stdout_equal` is `true`, so a fixture must force differing timestamps. A concrete,
hermetic, CLI-subprocess fixture is given below; it requires no new validation surface, only
a lane-root seam that the promoted `tools/context-capture.py` needs anyway because its
location is two directories below the repo root, not four.

## 1. Historical source anchors (read-only)

| Fact | Anchor |
|---|---|
| Comparison removes only top-level `observed_at` from both parsed documents | `capture-context.py:385-391` |
| `exclusions` literal `["observed_at"]` | `capture-context.py:364` |
| `normalization` literal `"top-level observed_at removed; canonical JSON compared"` | `capture-context.py:365` |
| Baseline doc must be `pin-disposition-v1`, status `ok`, six legs, each `content_status != "unavailable"` and `pinned.status == "verified"`, and carry top-level `observed_at` | `capture-context.py:351-362` |
| `raw_stdout_equal` compares the two raw stdout strings | `capture-context.py:367` |
| Equal normalized payload is `comparison.equal`; digests of the normalized payload are recorded | `capture-context.py:389-391` |
| `payload_tool_sha256_matches_disk` requires both docs' `tool_sha256` to equal the probe file digest | `capture-context.py:380-383` |
| Decide requires equal + probe digest + exact env delta + no baseline `GIT_DIR` + effective poison control + both source digests + full mapping | `capture-context.py:553-579` |
| Success token line is `CONTEXT: OK (receipt=<OUTPUT_REL> exit=0 probe-equal=True poison-control=True runner-mapping=True)` | `capture-context.py:637-641` |
| Mismatch reason prefix: `injected observation differs from baseline after excluding observed_at: ...` | `capture-context.py:560-563` |
| Exit map: 0 equal, 1 mismatch, 2 could-not-evaluate, 64 usage (no receipt) | `capture-context.py:26-29`, `605-607` |
| Fixed probe/runner/manifest/expected/output rela-tive paths | `capture-context.py:54-58` |
| Injection literal `{"GIT_DIR": "/nonexistent/tameshi-round14-poison"}` | `capture-context.py:60-61` |
| Root derivation: `LANE_ROOT = dirname(dirname(dirname(dirname(SELF))))` | `capture-context.py:45-47` |

Retained receipt facts: `.ufo/evidence/round-14/context-receipt.json` has
`comparison.exclusions == ["observed_at"]`, `equal == true`, `raw_stdout_equal == true`,
`observed_at.baseline == observed_at.injected`, and identical comparable digests. Therefore the
retained evidence records the *rule*, not a *discriminating run* of it. That is why the
selftest must not rely on wall-clock drift or on re-running the historical capture.

## 2. Exact existing stable tokens and expected exit

A passing observed-at fixture must pin all of these; any failure makes decide() return exit 1,
so they are jointly the fixture's oracle. No new finding ID is required or present.

| Token | Exact value in the successful fixture | Kind |
|---|---|---|
| process exit | `0` | literal |
| stdout line (for the promoted round-15 output rel) | `CONTEXT: OK (receipt=.ufo/evidence/round-15/context-receipt.json exit=0 probe-equal=True poison-control=True runner-mapping=True)\n` | literal |
| `status` / `exit` / `reasons` | `"ok"` / `0` / `[]` | literal |
| `comparison.exclusions` | `["observed_at"]` | literal |
| `comparison.normalization` | `top-level observed_at removed; canonical JSON compared` | literal |
| `comparison.equal` | `true` | literal |
| `comparison.raw_stdout_equal` | `false` (fixture forces this; `true` only when timestamps coincide) | literal |
| `comparison.error` | `null` | literal |
| `comparison.payload_tool_sha256_matches_disk` | `true` | literal |
| `comparison.observed_at.baseline` / `.injected` | `2000-01-01T00:00:01Z` / `2000-01-01T00:00:02Z` | literal (fixture-chosen) |
| `comparison.baseline_comparable_sha256` and `.injected_comparable_sha256` | equal to each other and to `sha256(canonical(PROBE_PAYLOAD without observed_at))` | derived from fixture literals |
| `environment.injected_env` / `env_delta_keys` | exactly the tool's declared `INJECTED_ENV` mapping / its sorted key list | literal (use the tool constant) |
| `environment.baseline_has_GIT_DIR` | `false` | literal |
| `positive_control.effective` | `true` | literal |
| `mapping.all_match` | `true` | literal |

Notes:
- Use the promoted tool's own `INJECTED_ENV`, `OUTPUT_REL` and `RECEIPT_SCHEMA` constants; do
  not hardcode round-14 values into the selftest expectation. The *keys and boolean tokens*
  above are the stable contract. The receipt schema string is round-scoped and not an
  observed-at token.
- Exit `64` is usage-only (`argv` non-empty and not `-h/--help`) and is unreachable by this
  fixture; exit `2` is could-not-evaluate (including `poison_path_exists`,
  `runner_unparsed`, missing inputs) and indicates a broken fixture, not a mismatch.
- The failure reason string is quoted for boundary reference only; the mismatch fixture is
  `TameshiR15.SpecMismatch`'s scope.

## 3. Fixture recipe (isolated, CLI subprocess, temp-root only)

### 3.1 Placement and the one implementation-critical constraint

Historical `LANE_ROOT` is four `dirname()` levels above `SELF`, which is correct for
`.ufo/evidence/round-14/capture-context.py` but would resolve to `<repo>/..` for
`tools/context-capture.py`. The promoted command must either (a) derive the lane root as
`dirname(dirname(realpath(__file__)))` for a `tools/` placement, or (b) accept one explicit
lane-root override. Either is a path seam, not a new validation feature. The recipe below uses
(a) with a byte-identical copy in a temp lane, so the shipped CLI is the process under test and
nothing is read or written outside the temp root. If ContextGate implements (b), skip the copy
and invoke the real file with the fixture root argument; the fixture content is unchanged.

### 3.2 Tree (all under one `mkdtemp`, e.g. `T`)

```text
T/
├── bin/git                          # fixture stub, executable (see 3.5)
├── lane/
│   ├── tools/
│   │   ├── context-capture.py       # byte copy of the promoted tool (recipe A only)
│   │   ├── pin-disposition.py       # synthetic probe (3.4)
│   │   └── mutate-and-run.sh        # synthetic six-leg mapping stub (3.6)
│   └── .ufo/evidence/
│       ├── round-13/
│       │   ├── pin-manifest.json    # synthetic six legs + derived_from (3.7)
│       │   └── expected.json        # {"inputs": {"tools/pin-disposition.py": <probe sha256>}}
│       └── round-15/                # created by the tool; receives context-receipt.json
└── home/, tmp/                      # HOME/TMPDIR targets, empty
```

`FLEET_ROOT` is `T` (parent of `lane`); the fixture never uses the real repo, real round-13
files, network, or the real round-15 receipt.

### 3.3 Invocation and environment

```sh
env -i \
  PATH="$T/bin:/usr/bin:/bin:/usr/local/bin" \
  HOME="$T/home" TMPDIR="$T/tmp" \
  python3 "$T/lane/tools/context-capture.py"
```

- No `GIT_*` keys in the fixture environment (decide requires `baseline_has_GIT_DIR=false`).
- `T/bin` first so `shutil.which("git")` resolves the stub; `python3` falls through to the real
  interpreter. If ContextGate prefers real git, `git init -q "$T/lane"` replaces the stub and
  the invocation is otherwise identical.
- Exactly one capture process; no retry and no second invocation (the historical run pair is
  baseline then injected inside one process).

### 3.4 Synthetic probe (`T/lane/tools/pin-disposition.py`)

It is invoked by the tool as `python3 tools/pin-disposition.py --manifest
.ufo/evidence/round-13/pin-manifest.json --root <FLEET_ROOT>` with cwd `LANE_ROOT`; it ignores
the arguments. It must emit one JSON object, exit 0, and satisfy the baseline precondition at
`capture-context.py:351-362`:

```python
import hashlib, json, os, sys

SELF = os.path.realpath(__file__)
LEGS = ("js-kimi-census", "bash-surface-census", "bash-tsukuroi-census",
        "bash-mado-verify", "bash-checklist-run", "js-claims-check")
payload = {
    "schema": "pin-disposition-v1",
    "tool_sha256": hashlib.sha256(open(SELF, "rb").read()).hexdigest(),
    "status": "ok",
    "legs": [{"leg": leg, "content_status": "unchanged",
              "pinned": {"status": "verified"}} for leg in LEGS],
}
# The ONLY run-to-run volatile value, forced deterministically instead of clock-based.
payload["observed_at"] = ("2000-01-01T00:00:02Z" if "GIT_DIR" in os.environ
                          else "2000-01-01T00:00:01Z")
json.dump(payload, sys.stdout, indent=2, sort_keys=True)
sys.stdout.write("\n")
```

- `GIT_DIR` is present only in the injected run under the preserved historical env policy
  (`safe_env()` removes all `GIT_*`, then exactly `INJECTED_ENV` is added). This makes the two
  stdout strings differ **only** in `observed_at`, with no clock dependence, no retry
  sensitivity, and no file writes.
- Fallback if the promoted tool normalizes the probe env: have the probe read/increment a
  counter file at `os.path.join(<--root value>, ".observed-at-seq")` and emit `...01Z`/`...02Z`.
  Both variants stay inside `T`.
- The probe hashes itself, so the fixture builder must write the probe first and then compute
  the same sha256 for `expected.json` and for the payload's `tool_sha256` oracle. Do not
  hand-write a digest.

Expected canonical digest, computed by the fixture builder from the same literal payload (not
from tool output):

```python
expected_comparable = json.dumps({k: v for k, v in payload.items() if k != "observed_at"},
                                 sort_keys=True, separators=(",", ":"))
EXPECTED_SHA256 = hashlib.sha256(expected_comparable.encode()).hexdigest()
```

Pin this value literally after construction, or recompute it from the literal payload inside
the selftest. It is the guard that the tool removed *only* `observed_at`: if the tool also
dropped or rewrote any other field, the receipt digests will not match even though `equal`
could still be true.

### 3.5 Git stub (`T/bin/git`, mode 0755)

```sh
#!/bin/sh
if [ -n "$GIT_DIR" ]; then
  echo "fatal: not a git repository: '$GIT_DIR'" >&2
  exit 128
fi
echo .git
exit 0
```

The tool calls `git -C <LANE_ROOT> rev-parse --git-dir` under the control env. This yields
baseline exit 0 with non-empty stdout, and injected exit 128 with the poison path in stderr,
so `positive_control.effective` is `true` deterministically and without reading a real repo.
This stubs only the external control binary; the observed-at comparison remains the code under
test.

### 3.6 Synthetic runner (`T/lane/tools/mutate-and-run.sh`)

The mapping parser is unchanged, so it must contain exactly six header rows, exactly six
`PIN_*=` and six `REV_*=` line-anchored constants, and exactly six calls inside
`run_regression() { ... }` with the syntax at `capture-context.py:82-107`. Minimal literal
template (fixture repo/path `fx/target.txt`, unique suffixes from `EXPECTED_SUFFIX`):

```sh
# js-kimi-census fx/target.txt 1/1 (100%)
# bash-surface-census fx/target.txt 1/1 (100%)
# bash-tsukuroi-census fx/target.txt 1/1 (100%)
# bash-mado-verify fx/target.txt 1/1 (100%)
# bash-checklist-run fx/target.txt 1/1 (100%)
# js-claims-check fx/target.txt 1/1 (100%)

PIN_JS=<64 lowercase hex, leg 1>          # ... one per leg, six distinct values
REV_JS=<40 lowercase hex, leg 1>          # ... one per leg, six distinct values

run_regression() {
  regression_case_git js-kimi-census 'fx/target.txt' "$PIN_JS" "$REV_JS" "x" 'y' "$TABLE_JS"
  regression_case_git bash-surface-census 'fx/target.txt' "$PIN_BASH" "$REV_BASH" "x" 'y' "$TABLE_BASH"
  regression_case_git bash-tsukuroi-census 'fx/target.txt' "$PIN_TSUKUROI" "$REV_TSUKUROI" "x" 'y' "$TABLE_TSUKUROI"
  regression_case_git bash-mado-verify 'fx/target.txt' "$PIN_MADO" "$REV_MADO" "x" 'y' "$TABLE_MADO"
  regression_case_git bash-checklist-run 'fx/target.txt' "$PIN_CHECKLIST" "$REV_CHECKLIST" "x" 'y' "$TABLE_CHECKLIST"
  regression_case_git js-claims-check 'fx/target.txt' "$PIN_CLAIMS" "$REV_CLAIMS" "x" 'y' "$TABLE_CLAIMS"
}
```

`TABLE_*` need not be defined; only the call suffix is checked. Any extra header, constant,
call, duplicate leg, or a seventh case yields exit 2 `runner_unparsed`, not the exit 0 reserved
for this fixture.

### 3.7 Manifest and expected inputs

`T/lane/.ufo/evidence/round-13/pin-manifest.json`:

```json
{
  "schema": "pin-manifest-v1",
  "legs": [
    {"leg": "js-kimi-census", "repo": "fx", "path": "target.txt",
     "pinned_commit": "<40 hex matching REV_JS>", "expected_sha256": "<64 hex matching PIN_JS>"}
  ],
  "derived_from": {"path": "fixture/tools/mutate-and-run.sh", "sha256": "<sha256 of the runner file>"}
}
```

Six legs, in call order, with `repo`/`path` equal to every header/call. `derived_from.path` must
end with `tools/mutate-and-run.sh` (the historical suffix check at `capture-context.py:505-513`).

`T/lane/.ufo/evidence/round-13/expected.json`:

```json
{"inputs": {"tools/pin-disposition.py": "<sha256 of the synthetic probe file>"}}
```

The probe digest appears in three places and must be the same value: `expected.json.inputs`,
the probe's emitted `tool_sha256`, and `comparison.payload_tool_sha256_matches_disk`'s premise.
The fixture builder computes it once from the written probe bytes.

### 3.8 Assertions after the subprocess returns

1. Process exit is exactly `0`.
2. stdout is exactly the `CONTEXT: OK (...)` line in §2, ending in the four literal tokens
   `exit=0 probe-equal=True poison-control=True runner-mapping=True)`.
3. Load `T/lane/.ufo/evidence/round-15/context-receipt.json` and pin every row in §2,
   including `comparison.exclusions == ["observed_at"]` and the exact normalization string.
4. Re-read `runs.baseline.stdout` and `runs.injected.stdout`; assert they are unequal as raw
   strings, equal after popping only `observed_at`, and that the popped values are exactly the
   two literal timestamps. This proves the fixture varied only the intended key.
5. Assert both comparable digests equal `EXPECTED_SHA256` from §3.4.
6. Assert the real repo paths were never touched: the fixture only ever references `T/...`;
   no real round-14 or round-15 file is read or written. The promoted tool's normal capture
   remains the only writer of the real round-15 receipt.

## 4. Boundaries and pitfalls (bounded, no broad claims)

- **No finding ID exists in the historical source.** The rule is represented by the literals
  above and by `equal`/exit. Do not add a mandatory `observed_at_excluded`-style ID as a
  selftest requirement; if the promoted check mode introduces stable finding IDs for other
  reasons, this fixture still pins the existing tokens and exit 0.
- **`raw_stdout_equal` must be `false` in this fixture.** The retained round-14 receipt's
  `true` value is evidence that timestamps coincided, not that the exclusion is broken.
- **Do not rely on the wall clock.** Two sequential probe runs can land in the same second;
  the round-14 receipt demonstrates exactly that. Forcing the value from `GIT_DIR` presence (or
  a temp counter) is required for a deterministic fixture.
- **Do not weaken `decide()` to isolate the comparison.** A positive fixture must pass the
  control, env-delta, source-digest and mapping predicates; otherwise the expected exit is 1
  and the fixture is invalid. The observed-at rule is only exercised end-to-end when everything
  else is deliberately satisfied.
- **Only top-level `observed_at` is excluded.** The fixture's digest pin detects accidental
  exclusion of any other field; a negative payload-difference case belongs to
  `TameshiR15.SpecMismatch` and is not duplicated here.
- **Isolation is placement-based.** With the historical four-level derivation, a copy placed at
  `T/lane/.ufo/evidence/round-14/capture-context.py` would also work, but the promoted tool
  lives at `tools/`, so the derivation or a lane-root seam must be adapted. This is the only
  implementation-critical detail I am routing to L1.
- **No installs, no network, no host writes.** Nothing outside `T` is written; `python3` and
  the git stub are the only executables used. This report installed or updated no tools.

## 5. Recommendation to ContextGate (via TameshiR15)

1. Preserve the comparison block's literals and mechanics exactly: pop only top-level
   `observed_at` from each parsed document, canonicalize with `sort_keys=True` and
   `separators=(",", ":")`, record both digests and `equal`. Do not generalize the exclusion.
2. Make the lane root explicit/testable: either `dirname(dirname(realpath(__file__)))` for the
   `tools/` location or a single fixture-root override. Do not derive it from cwd or git.
3. Ship the §3 fixture in `--selftest` as a real CLI subprocess under a temp root, with the
   literal exit `0`, the literal `CONTEXT: OK`/`probe-equal=True` tokens, the §2 receipt fields,
   and the §3.4 canonical digest as the "only observed_at removed" guard.
4. Do not add a new broad validation feature or a new finding-ID contract for this predicate;
   the exact existing tokens are sufficient and bounded.
5. Leave `.ufo/evidence/round-14/capture-context.py` and every round-12/13/14 artifact
   byte-identical; the fixture and the promoted command write only under the temp root, and
   normal capture writes only the round-15 receipt.
