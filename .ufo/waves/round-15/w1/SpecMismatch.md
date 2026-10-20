# SpecMismatch — comparison mismatch exit 1: existing token and isolated fixture

Lane: tameshi-shokunin. Seat: TameshiR15.SpecMismatch (leaf executor, advisory only).
Report path is lane-relative; no source file was created or edited. No lane gate,
selftest, or promoted tool was executed. The only command that did anything beyond
reading was one bounded local `git` observation in a `mktemp -d` directory under
`/tmp`, disclosed with its exact transcript in §5.1 and §8 as a no-mid-flight-check
exception; it was removed afterwards. Read revision:
`a9cf4da78f2514c7bedd91a850a88590009d7df0`.

## 1. Historical source pinned for this report

`.ufo/evidence/round-14/capture-context.py` is tracked at that revision:

- mode `100755`, git blob `3601d26327cc633443d425bb3eaef5d93edc0b77`,
  sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`
  (equals the retained `context-receipt.json.tool_sha256`), introduced by
  `0c6e36d`; 647 lines.
- Anchors read: docstring/exit map `:1-31`; constants `:50-107` (`EXPECTED_SUFFIX`
  `:74-81`, header/regexes `:83-107`); `safe_env` `:184-188`; `run_bounded`
  `:190-210`; `parse_runner_mapping` `:213-256`; `mapping_block` `:259-337`;
  `parse_probe_document` `:340-347`; `comparison_block` `:350-392`;
  `positive_control_block` `:395-411`; `validate_manifest` `:439-463`;
  `evaluate` `:465-551`; `decide` `:553-580`; `write_receipt` `:583-603`;
  `main` `:605-643`.
- Retained positive run read for grounding: `.ufo/evidence/round-14/context-receipt.json`
  (`status=ok`, `exit=0`, `comparison.equal=true`, `comparison.error=null`,
  `positive_control`: baseline exit 0 / stdout `.git\n`, injected exit 128 /
  stderr `fatal: not a git repository: '/nonexistent/tameshi-round14-poison'\n`,
  `effective=true`).

## 2. Exact comparison-mismatch contract in the historical source

`comparison_block()` builds `result` with `equal=false` by default, then:

- sets `error` and returns early when the **injected** probe run produced no JSON
  document (`exit != 0` or non-object JSON): `:372`
  `injected probe run produced no JSON document (exit=<n>)`;
- sets `error` when the injected document lacks top-level `observed_at`: `:378`
  `injected document has no top-level observed_at`;
- otherwise removes only top-level `observed_at` from both documents, re-serializes
  canonical JSON (`sort_keys`, compact separators), records both digests and sets
  `equal = base_text == inj_text` (`:382-391`). On a pure payload difference the
  result is `equal=false` **and** `error=null`.

`decide()` `:553-580` turns that into exit 1, first reason branch `:560-563`:

```python
if comparison.get("equal") is not True:
    reasons.append("injected observation differs from baseline after "
                   "excluding observed_at: {}".format(
                       comparison.get("error") or "normalized JSON mismatch"))
```

`main()` `:629-643` stores `status="mismatch"`, `exit=1`, `reasons` in the receipt,
writes it, prints one line, and returns 1. The line format is `:637-641`:

```text
CONTEXT: MISMATCH (receipt=<OUTPUT_REL> exit=1 probe-equal=False poison-control=True runner-mapping=True)
```

`<OUTPUT_REL>` is the relative constant returned by `write_receipt` (`:583-603`),
not an absolute temp path, so the stdout line is deterministic in a fixture once
the promoted output constant is fixed. The exit map is declared at `:26-30` and
`:123`: 0 equal, 1 mismatch, 2 could-not-evaluate, 64 usage. A comparison mismatch
is therefore **exit 1, not 2**; exit 2 is reserved for setup/input failure.

## 3. Stable-token answer (what exists, what does not)

| Level | Existing token | Source | Status |
|---|---|---|---|
| Process | exit `1` | `:26-30`, `:579`, `:641` | exists |
| Receipt status | `"mismatch"` | `:579`, `:630` | exists |
| Stdout prefix | `CONTEXT: MISMATCH ` | `:637-641` | exists |
| Branch reason (exact) | `injected observation differs from baseline after excluding observed_at: normalized JSON mismatch` | `:560-563` (implicit concatenation + `or` default) | exists |
| Narrow literal | `normalized JSON mismatch` | `:563` | exists |
| Opaque per-finding ID (e.g. `CTX-...`) | — | none in the file | **does not exist** |

So the requested "stable ID and expected exit" are supported only as the literal
pair **`(exit=1, reasons == [<exact branch line>])`** plus `status="mismatch"`.
There is no standalone stable finding ID for this branch anywhere in the
historical tool; `reasons` is free text built from literals, and all opaque
machine tokens in the file are `InvalidContext.kind` values on the exit-2 path
(`missing_input`, `invalid_json`, `invalid_utf8`, `missing_executable`, `timeout`,
`exec_failed`, `non_utf8_output`, `runner_unparsed`, `probe_baseline_unusable`,
`invalid_manifest`, `invalid_expected`, `invalid_fleet_root`,
`poison_path_exists`).

Recommendation: the historical file supplies only the literal pair, so pin that.
The advisory fixture does **not** require frozen historical IDs: if the active
`tools/context-capture.py` declares a stable finding ID for this branch, pin the
declared ID together with exit 1, retaining the literal line as the anchor. What
must not happen is a claim that the historical tool already emitted such an ID, or
a case that fails merely because the active gate declares none.

The comparator's two error variants are distinguishable from the pure mismatch by
`comparison.error`: `null` means normalized mismatch; non-null carries one of the
two literal messages above. Pin `comparison.error == null` so a fixture cannot
silently drift into the "unusable injected run" variant.

## 4. Isolated fixture recipe — case `comparison-normalized-mismatch`

Design: a temp lane tree that satisfies every pre-comparison predicate, with a
**synthetic probe stub** whose only difference between the two runs is a payload
field read from `GIT_DIR`. No live lane input, probe, runner, or receipt is read.
The tool under test is copied byte-for-byte into the temp tree, so the fixture
also exercises SELF-relative lane discovery exactly as production does.

### 4.1 Tree (all under `tempfile.mkdtemp(prefix="tameshi-r15-ctx-mismatch-")`)

```text
T/                                  # FLEET_ROOT = dirname(lane)
└── tameshi-shokunin/               # LANE_ROOT, the temp git repo
    ├── .git/                       # from `git init -q` (control baseline)
    ├── tools/
    │   ├── context-capture.py      # copy2 of the promoted tool (bytes identical)
    │   ├── pin-disposition.py      # synthetic probe stub below
    │   └── mutate-and-run.sh       # synthetic six-leg runner below
    └── .ufo/evidence/round-13/
        ├── pin-manifest.json
        └── expected.json
```

`git init -q <lane>` must run with every `GIT_*` key removed from the harness
environment (otherwise an ambient `GIT_DIR` redirects the init). `tempfile` root,
one lane-shaped child, no other writes; nothing outside `T` is touched.

### 4.2 Probe stub `tools/pin-disposition.py` (exact)

```python
#!/usr/bin/env python3
import hashlib, json, os
SELF = os.path.abspath(__file__)
with open(SELF, "rb") as handle:
    digest = hashlib.sha256(handle.read()).hexdigest()
document = {
    "schema": "pin-disposition-v1",
    "status": "ok",
    "observed_at": "2026-10-20T00:00:00Z",
    "tool_sha256": digest,
    "injected_git_dir": os.environ.get("GIT_DIR"),
    "legs": [
        {"leg": "fixture-leg-{}".format(index), "content_status": "present",
         "pinned": {"status": "verified"}}
        for index in range(6)
    ],
}
print(json.dumps(document, sort_keys=True))
```

Why this satisfies `comparison_block` `:350-370`: a dict, `schema` and `status`
exact, six legs, no `content_status == "unavailable"`, every `pinned.status ==
"verified"`, top-level `observed_at` present, and `tool_sha256` equals the sha256
of its own bytes as read from disk (source digest captured at `:477-480`; both
documents checked against it at `:380-383`). Both runs exit 0; only
`injected_git_dir` differs — `null` in the baseline (because `safe_env` `:184-188`
strips every `GIT_*`) and `/nonexistent/tameshi-round14-poison` in the injected
run. The stub ignores its `--manifest/--root` argv.

### 4.3 Runner fixture `tools/mutate-and-run.sh` (exact skeleton)

Leg names and suffixes are hard-coded by `EXPECTED_SUFFIX` `:74-81`, so use exactly
these six. Constants are fabricated hex; the runner is parsed as text and never
executed (`:213-256`). Values repeat the digit per leg for readability.

```sh
#!/usr/bin/env bash
PIN_JS=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
PIN_BASH=bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
PIN_TSUKUROI=cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
PIN_MADO=dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd
PIN_CHECKLIST=eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
PIN_CLAIMS=ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
REV_JS=1111111111111111111111111111111111111111
REV_BASH=2222222222222222222222222222222222222222
REV_TSUKUROI=3333333333333333333333333333333333333333
REV_MADO=4444444444444444444444444444444444444444
REV_CHECKLIST=5555555555555555555555555555555555555555
REV_CLAIMS=6666666666666666666666666666666666666666

# js-kimi-census shokunin/fixture-kimi 1/1 (100 %)
# bash-surface-census shokunin/fixture-surface 1/1 (100 %)
# bash-tsukuroi-census shokunin/fixture-tsukuroi 1/1 (100 %)
# bash-mado-verify shokunin/fixture-mado 1/1 (100 %)
# bash-checklist-run shokunin/fixture-checklist 1/1 (100 %)
# js-claims-check shokunin/fixture-claims 1/1 (100 %)

run_regression() {
  regression_case_git js-kimi-census 'shokunin/fixture-kimi' "$PIN_JS" "$REV_JS" "fixture" 'fixture' "$TABLE_JS"
  regression_case_git bash-surface-census 'shokunin/fixture-surface' "$PIN_BASH" "$REV_BASH" "fixture" 'fixture' "$TABLE_BASH"
  regression_case_git bash-tsukuroi-census 'shokunin/fixture-tsukuroi' "$PIN_TSUKUROI" "$REV_TSUKUROI" "fixture" 'fixture' "$TABLE_TSUKUROI"
  regression_case_git bash-mado-verify 'shokunin/fixture-mado' "$PIN_MADO" "$REV_MADO" "fixture" 'fixture' "$TABLE_MADO"
  regression_case_git bash-checklist-run 'shokunin/fixture-checklist' "$PIN_CHECKLIST" "$REV_CHECKLIST" "fixture" 'fixture' "$TABLE_CHECKLIST"
  regression_case_git js-claims-check 'shokunin/fixture-claims' "$PIN_CLAIMS" "$REV_CLAIMS" "fixture" 'fixture' "$TABLE_CLAIMS"
}
```

This matches `HEADER_ROW_RE` `:83-88`, `PIN_CONST_RE`/`REV_CONST_RE` `:89-90`,
`CALL_RE` `:92-101`, `CALL_LINE_RE` `:102`, and `RUN_REGRESSION_RE` `:103-105`.
Keep calls one line each (the historical parser supports continuation joins, but a
single line removes an avoidable fixture variable). `TABLE_*` names need not exist
because the body is never executed.

### 4.4 `pin-manifest.json` and `expected.json`

Manifest: schema `pin-manifest-v1`; six legs in the same order as the runner
calls, each `repo="shokunin"`, matching `path`, `pinned_commit` equal to the
leg's `REV_*` value, `expected_sha256` equal to the leg's `PIN_*` value; plus
`"derived_from": {"path": "tools/mutate-and-run.sh", "sha256": "<sha256 of the
runner bytes>"}`. The file is written **after** the runner so the digest is real.

```json
{
  "schema": "pin-manifest-v1",
  "derived_from": {"path": "tools/mutate-and-run.sh", "sha256": "<runner-sha256>"},
  "legs": [
    {"leg": "js-kimi-census", "repo": "shokunin", "path": "fixture-kimi",
     "pinned_commit": "1111111111111111111111111111111111111111",
     "expected_sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"},
    {"leg": "bash-surface-census", "repo": "shokunin", "path": "fixture-surface",
     "pinned_commit": "2222222222222222222222222222222222222222",
     "expected_sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"},
    {"leg": "bash-tsukuroi-census", "repo": "shokunin", "path": "fixture-tsukuroi",
     "pinned_commit": "3333333333333333333333333333333333333333",
     "expected_sha256": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"},
    {"leg": "bash-mado-verify", "repo": "shokunin", "path": "fixture-mado",
     "pinned_commit": "4444444444444444444444444444444444444444",
     "expected_sha256": "dddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"},
    {"leg": "bash-checklist-run", "repo": "shokunin", "path": "fixture-checklist",
     "pinned_commit": "5555555555555555555555555555555555555555",
     "expected_sha256": "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"},
    {"leg": "js-claims-check", "repo": "shokunin", "path": "fixture-claims",
     "pinned_commit": "6666666666666666666666666666666666666666",
     "expected_sha256": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"}
  ]
}
```

`expected.json` only needs `inputs` to exist as an object with the probe digest at
`tools/pin-disposition.py` (read at `:477-508`); add the runner digest too if the
promoted reader requires it (harmless to the historical reader):

```json
{"inputs": {
   "tools/pin-disposition.py": "<probe-sha256>",
   "tools/mutate-and-run.sh": "<runner-sha256>"
 }}
```

Do not reuse the live `.ufo/evidence/round-13/` manifest, expected file, real
probe, or real runner: that is a live lane/sibling read and would make the fixture
non-hermetic (and the selftest would depend on production pins).

### 4.5 Invocation

```text
cwd:  <T>/tameshi-shokunin
argv: [sys.executable, "<T>/tameshi-shokunin/tools/context-capture.py"]   # public capture CLI
env:  ambient with all GIT_* removed (the tool strips them again in safe_env)
```

If the promoted interface adds an explicit subcommand (e.g. `capture`) or a
fixture-root option, pass it here; the assertions below are invariant. What must
not be required is any read of the real lane. Copying the tool with
`shutil.copy2` keeps the SELF-relative root arithmetic honest: at
`<lane>/tools/context-capture.py`, the promoted lane root must resolve to
`<lane>` (two `dirname`s, not the historical four), so this fixture also catches a
naive `dirname ×4` port by ending up with the wrong `LANE_ROOT`, wrong output path,
and an ineffective control (see TameshiR15.ReviewControl H1, consistent finding).

### 4.6 Expected result (analytic from source; not executed)

Process: **exit 1**, stderr empty, stdout exactly

```text
CONTEXT: MISMATCH (receipt=.ufo/evidence/round-15/context-receipt.json exit=1 probe-equal=False poison-control=True runner-mapping=True)
```

with `receipt=` set to the promoted round-15 constant (historical string carried
`.ufo/evidence/round-14/context-receipt.json`; it must never remain round-14).
If the promoted tool prints an absolute path or reshapes the line, pin
`prefix == "CONTEXT: MISMATCH "` plus the literal field suffixes
`exit=1 probe-equal=False poison-control=True runner-mapping=True` instead; do not
pin a temp path.

Receipt at `<lane>/.ufo/evidence/round-15/context-receipt.json`:

| JSON path | Expected | Basis |
|---|---|---|
| `status` | `"mismatch"` | `:579`, `:630` |
| `exit` | `1` | `:579`, `:630` |
| `reasons` | exactly `["injected observation differs from baseline after excluding observed_at: normalized JSON mismatch"]` | `:560-563` |
| `comparison.equal` | `false` | probe payload differs after `observed_at` removal |
| `comparison.error` | `null` | pure normalized difference, `:382-391` |
| `comparison.raw_stdout_equal` | `false` | consequence of the same difference |
| `comparison.payload_tool_sha256_matches_disk` | `true` | stub self-hash |
| `positive_control.effective` | `true` | baseline repo exists; see §5 |
| `positive_control.baseline.exit` / `.injected.exit` | `0` / `128` | §5 |
| `environment.env_delta_keys` | `["GIT_DIR"]` | `:526-535` by construction |
| `environment.baseline_has_GIT_DIR` | `false` | `safe_env` |
| `mapping.all_match` | `true` | fixture runner/manifest parity |
| `sources.probe.matches_declared` | `true` | expected.json pin |
| `sources.runner.matches_manifest_declaration` | `true` | manifest `derived_from` |

Do **not** pin `observed_at`, `invocation.argv`, `invocation.cwd`, `lane_root`,
`fleet_root`, `tool_sha256`, the comparable digests, or the receipt file digest:
they are temp-path- or time-dependent. Pin the exit/status/reason triple and the
boolean structure above.

Failure isolation: if any other `decide()` predicate fails, the reasons list grows,
so the exact one-element list is a strong per-fixture isolation assertion. The
likely failure signatures are `probe payload tool_sha256 does not match the disk
digest` (stub self-hash wrong), `git poison positive control is ineffective`
(repo not initialized / root arithmetic), `runner source digest does not match the
manifest declaration` (manifest written before runner), and
`leg …: header_matches_manifest, …` (fixture drift from `EXPECTED_SUFFIX`).

### 4.7 Clean twin (non-vacuity, not a new case)

Reuse the identical builder and runner/manifest; delete only the
`"injected_git_dir": os.environ.get("GIT_DIR"),` line from the probe source,
recompute the probe digest in `expected.json`, and rerun. The normalized documents
are then equal; expected **exit 0**, `status="ok"`, `reasons=[]`,
`comparison.equal=true`, `comparison.error=null`, and stdout
`CONTEXT: OK (receipt=… exit=0 probe-equal=True poison-control=True runner-mapping=True)`.
The pair differs by one payload field, which proves the exit-1 case is caused by
the comparison predicate and not by a broken fixture. Do not expand this into a
new coverage claim or a seventh mutation case.

## 5. Control substrate and why `git init` is part of the recipe

`positive_control_block` `:395-411` runs exactly
`git -C <LANE_ROOT> rev-parse --git-dir` twice (control env = stripped env plus
`GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_OPTIONAL_LOCKS=0`,
`GIT_TERMINAL_PROMPT=0`; injected env adds only `GIT_DIR=<poison>`). Without a repo
at the temp lane, `baseline_ok` is false and `decide()` appends the second reason
`git poison positive control is ineffective`, so the one-element reasons assertion
would fail for the wrong reason. Hence `git init -q <lane>`.

Grounding for the expected control pair:

- `[READ]` the retained round-14 receipt records baseline exit 0 / stdout
  `.git\n`, injected exit 128 / stderr with the poison path, `effective=true`.
- `[MEASURED]` a bounded local `git` observation on this host (git `2.55.0`); the
  exact command, output, abort behavior and cleanup are retained in §5.1. It is
  the only executed item in this report and is disclosed there as a
  no-mid-flight-check exception; L1 runtime proof will not rely on it.

### 5.1 Exact temp-git transcript and exception disclosure

Run once, in a temporary shell (the session shell was busy; no variables persisted),
with this exact command:

```sh
set -e; T=$(mktemp -d /tmp/tameshi-r15-specmismatch.XXXXXX); env -u GIT_DIR -u GIT_WORK_TREE git -C "$T" init -q; echo "baseline:"; env -u GIT_DIR GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0 GIT_TERMINAL_PROMPT=0 git -C "$T" rev-parse --git-dir; echo "exit=$?"; echo "injected:"; GIT_DIR=/nonexistent/tameshi-round14-poison GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_OPTIONAL_LOCKS=0 GIT_TERMINAL_PROMPT=0 git -C "$T" rev-parse --git-dir; echo "exit=$?"; rm -rf "$T"
```

Exact observed output:

```text
baseline:
.git
exit=0
injected:
fatal: not a git repository: '/nonexistent/tameshi-round14-poison'
```

Harness framing, quoted verbatim (not program output): `Ran in a temporary shell
while the session shell is busy with another command: session variables and
functions were unavailable, and nothing set here persisted.` The harness also
reported `Command exited with code 128`. Because `set -e` was in
force, the injected `git` exit 128 terminated the harness before the second
`echo "exit=$?"` and before the inline `rm -rf "$T"` ran; the 128 is the harness's
process exit, not an echoed value. The created directory was
`/tmp/tameshi-r15-specmismatch.X6XRvq`; cleanup was a separate read-only listing
plus removal, with this exact command and output:

```sh
ls -d /tmp/tameshi-r15-specmismatch.* 2>/dev/null && rm -rf /tmp/tameshi-r15-specmismatch.* && echo cleaned; ls -d /tmp/tameshi-r15-specmismatch.* 2>/dev/null || true
```

```text
/tmp/tameshi-r15-specmismatch.X6XRvq
cleaned
```

The final `ls` printed nothing, so no temp directory remained.

**No-mid-flight-check exception (explicit).** This seat was instructed to skip
build/lint/tests/formatters, perform no verification execution, and not run checks
mid-flight. The single `git` observation above is disclosed as an exception to
that instruction: it executed the real `git` binary solely to ground the expected
fixture control pair. It did **not** run the historical or promoted
`capture-context.py`, did not touch the repository, sibling trees, or any lane gate
or receipt, and wrote only under the `mktemp -d` root that was removed. It is not a
lane check, selftest, or verification of any deliverable; **L1 runtime proof will
not rely on it**, and the fixture's expected values must be established by the
promoted tool's own selftest at gate time.

If the planner prefers no repo-dependent fixture, the fallback is the same tree
**without** `git init`, where the expected result is still exit 1 but with
`reasons == ["injected observation differs from baseline after excluding
observed_at: normalized JSON mismatch", "git poison positive control is
ineffective"]`. That fallback pins two literals and is strictly less isolated; the
repo-initialized variant above is recommended.

## 6. Bounded recommendations to TameshiR15.ContextGate

1. **Preserve the four `decide()` comparison predicates and the reason literals**
   (`:560-563`) in the promoted `tools/context-capture.py`; the checked-in fixture
   literal must be the promoted literal. If the wording is changed, the fixture
   must change in the same commit and the claim must not imply old/new equivalence.
2. **CLI shape:** implement `--selftest` (before the historical "any argv is
   usage" branch at `:605-613`, or it returns 64) as a real subprocess pilot of the
   public capture command over temp fixtures, in the repo's existing style
   (`SELFTEST_CASES` with `expected_exit`/`expected_reason`, `SELFTEST_CASE …
   expected=… observed=…`, final `SELFTEST: PASS n/n`). Helper-level unit calls do
   not satisfy the routed requirement; the case must observe the process exit and
   the written receipt, and may import constants only for the expected literals.
3. **Case row suggestion (literal+exit; add the declared ID if provided):**
   `{"case": "comparison-normalized-mismatch", "expected_status": "mismatch",
   "expected_exit": 1, "expected_reason": "<exact branch line>",
   "expected_id": "<active-tool ID, only if declared>",
   "setup": "probe-payload-sensitive"}`.
4. **Root/output contract:** lane root for `tools/context-capture.py` is
   `dirname(dirname(SELF))`; output constant is
   `.ufo/evidence/round-15/context-receipt.json`. The temp-tree copy in §4.1 tests
   both. Never write round-14's path.
5. **Selftest must use the synthetic stub**, not the live probe/runner/manifest;
   and must scrub `GIT_*` for its own `git init` only. No network, no live lane
   reads, no writes outside the temp root.
6. **Stable IDs are optional active-tool vocabulary.** If the promoted gate
   declares a stable finding ID for the `comparison.equal is not True` branch
   (consistent with a `finding_ids` array for other branches), the fixture pins
   that declared ID with exit 1 and the literal line; the assertion is then about
   the active tool's own vocabulary, not a historical one. If no ID is declared,
   the literal+exit pair alone satisfies the case; do not invent an ID solely to
   fill the row.
7. If a retained-receipt `--check` mode is added, keep it separate from this
   fixture: `decide()` on a stored receipt reads stored booleans, so a check mode
   must be described as configured-expectation replay, not re-execution. This
   report makes no recommendation for that mode beyond not conflating it with the
   capture fixture.

## 7. Bounds and non-claims

- No historical byte was edited; `.ufo/evidence/round-12`, `round-13`, and
  `round-14` are untouched.
- The fixture is synthetic: it does not test the real `pin-disposition.py`, the
  real six-leg runner, round-14's receipt, sibling trees, or actual regression
  execution. It establishes only that the promoted CLI returns exit 1 with the
  pinned literal when the two probe observations differ after `observed_at`
  removal, and exit 0 when they do not.
- No environment-independence, result-reuse, suite/dependency identity,
  kill-rate, mutation-rate, or broad hermeticity claim follows from this case.
- The analytic expected values in §4.6 are derived by reading the cited source
  (`[INFERENCE]` for the actual execution, since no run of the historical or
  promoted tool was performed); the control pair is `[READ]`/`[MEASURED]` as
  marked in §5. No sibling gate was executed and this report is not an admission
  authority.
- LSP was not used: no LSP device is mounted for this seat; navigation was by
  `grep`/`read` with exact line anchors.

## 8. Tooling and coordination

- Tools installed or updated: none (`pacman`, `uv`, `cargo`, `npm` untouched).
- Read-only commands: `ls`, `grep`, `read`, `sha256sum`, `git ls-files -s`,
  `git hash-object`, `git log`, `git --version`, `python3 -c` JSON reads of
  retained receipts.
- Bounded local observation (exception, disclosed in full in §5.1): one `git`
  command in a `mktemp -d` repo, run once in a temporary shell, then removed
  (`/tmp/tameshi-r15-specmismatch.X6XRvq`; cleanup verified). This is the only
  executed item in this seat's work and is an explicit exception to the lane's
  no-mid-flight-check / no-verification-execution instruction. It is not a lane
  gate, selftest, or verification of any deliverable, and L1 runtime proof will
  not rely on it.
- Messages sent: two concise notes to `agent://TameshiR15` — the initial
  implementation-critical detail (exact literal, no-ID finding, temp-copy fixture,
  root/output constants) and a follow-up confirming the retained transcript and the
  active-tool ID latitude. No broadcast, no Main message, no sibling contact.
