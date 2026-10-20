# SpecControl — positive git control failure: isolated fixture recipe, exact token, exit

Lane: tameshi r15 w1, seat `TameshiR15.SpecControl` (executor). Target: historical
`.ufo/evidence/round-14/capture-context.py`; advice for `TameshiR15.ContextGate` / active
`tools/context-capture.py`. **No source edit, no gate/selftest execution.** Every statement below
is derived statically from the cited source lines and the retained round-14 receipt; nothing here
is an executed result.

## 1. Answer first

| Question | Answer |
|---|---|
| Which branch fails? | `positive_control.effective is not True` → `decide()` appends the reason at `capture-context.py:571`. |
| Exact **existing** stable token | Literal reason string **`git poison positive control is ineffective`** (`capture-context.py:571`). |
| Secondary existing tokens | status token `mismatch` (`:579`); stdout field `poison-control=False` and `exit=1` on the `CONTEXT: MISMATCH (…)` line (`:637-642`). |
| Expected exit | **1** (`return "mismatch", 1, reasons`, `:579`). |
| Existing finding-ID token? | **None.** The historical tool has no finding-ID/code field; `reasons` is a list of plain strings (`:563-579`) and the receipt schema carries no identifier. Do not pin an invented ID. If the promoted tool introduces IDs, this reason's ID must be declared in source and pinned next to the literal above; no broader taxonomy is required by this seat. |
| Receipt still written on this path? | Yes. `main()` writes the receipt for both branches (`:629-635`) before printing and returning the code. |
| Repro without a stub git? | Not at exit 1. An existing `GIT_DIR` target is rejected earlier with `InvalidContext("poison_path_exists")` → exit 2 (`:469-472`); real git against the absent poison path always yields exit 128, i.e. `effective=True`. See §3. |

## 2. What the control actually checks (`positive_control_block`, `:395-412`)

- argv: `[git_path, "-C", LANE_ROOT, "rev-parse", "--git-dir"]`, run twice with
  `CONTROL_ENV_ADDITIONS` (`:46-51`), cwd `LANE_ROOT`, timeout 30 s.
- `baseline_ok = baseline.exit == 0 and baseline.stdout.strip() != ""` (`:403`).
- `reflects = poison in injected.stdout or poison in injected.stderr or injected.exit != baseline.exit` (`:404-406`).
- `effective = baseline_ok and injected.exit != 0 and reflects` (`:407-409`).

Therefore `effective=False` has exactly three shapes:

1. baseline does not produce a non-empty success (broken/unavailable git);
2. injected exits 0 like baseline **and** poison is not echoed (git ignores `GIT_DIR`);
3. injected exits 0 with output identical to baseline.

Only shape 2 gives an unambiguous "poison is not observable to git" verdict while keeping the rest
of the gate in its pass state. Shape 1 conflates a broken git executable with an ineffective
injection and is offered only as an optional variant (§5).

## 3. Why a stub `git` is the only route to exit 1

The fixture cannot use real git:

- The injected value is the fixed literal `GIT_DIR=<poison>` (`:45-46`). Real git on a nonexistent
  directory exits 128 and prints `fatal: not a git repository: '<poison>'`; that is
  `effective=True` (retained round-14 receipt: baseline `exit 0`, stdout `.git\n`; injected
  `exit 128`, stderr with the poison path).
- Pointing `GIT_DIR` at an existing repository would make real git exit 0 and not echo the path
  (shape 2) — but `evaluate()` rejects any fixture whose declared poison path exists *before* the
  control runs: `os.path.lexists(POISON_PATH)` → `InvalidContext("poison_path_exists")` → exit 2
  (`:469-472`). That route is closed by design.
- Creating a repository at the literal poison path is an external write and is forbidden.

So the exit-1 control fixture must place a synthetic `git` earlier on `PATH` that deliberately does
not observe `GIT_DIR`. This is the non-vacuous negative control for the gate's own control logic: it
proves the gate reports an ineffective injection with the pinned token, not that real git behaves
this way. Real-git behaviour remains evidence in the prospective capture, not in `--selftest`.

## 4. Concrete hermetic fixture recipe

### 4.1 Tree (everything under one `tempfile.mkdtemp()`; no real lane file is read)

Assume the promoted tool keeps the historical semantic slots `PROBE_REL=tools/pin-disposition.py`,
`RUNNER_REL=tools/mutate-and-run.sh`, and the round-13 manifest/expected inputs (`:36-40`). If the
promoted constants move, move the same fixture files to the promoted relative paths; do **not**
change the tool to match the fixture.

```
<tmp>/                                  # FLEET_ROOT (parent of lane root)
├── bin/
│   └── git                             # stub, mode 0755
└── lane/                               # LANE_ROOT
    ├── tools/
    │   ├── context-capture.py          # byte copy of the tool under test (SELF)
    │   ├── pin-disposition.py          # synthetic deterministic probe
    │   └── mutate-and-run.sh           # synthetic six-leg mapping text
    └── .ufo/evidence/
        ├── round-13/
        │   ├── pin-manifest.json       # synthetic manifest, six legs + derived_from
        │   └── expected.json           # {"inputs": {"tools/pin-disposition.py": <probe sha>}}
        └── round-15/                   # created by write_receipt on the mismatch path
```

**Root-depth requirement (implementation-critical):** `LANE_ROOT` is derived from
`os.path.realpath(__file__)` with **four** `dirname` calls historically (`:32-34`), correct only
because the historical file sits at `.ufo/evidence/round-14/capture-context.py`. At
`tools/context-capture.py` the correct derivation is **two** `dirname` calls. Copying the historical
constant verbatim makes the fixture (and the real capture) read `<parent-of-lane>`: the fixture then
returns exit 2 `missing_input`, not the pinned 1. The fixture copy must be placed at whatever depth
the promoted derivation expects, and that derivation must be correct for `tools/`.

### 4.2 Synthetic probe — `lane/tools/pin-disposition.py`

Must satisfy `comparison_block` (`:350-392`): exit 0, stdout parses to one dict, `schema ==
"pin-disposition-v1"`, `status == "ok"`, exactly six legs, every row `content_status !=
"unavailable"` and `pinned.status == "verified"`, top-level `observed_at` present, and
`tool_sha256` equal to the file's own digest (`payload_tool_sha256_matches_disk`).

```python
#!/usr/bin/env python3
import datetime, hashlib, json, os

LEGS = ["js-kimi-census", "bash-surface-census", "bash-tsukuroi-census",
        "bash-mado-verify", "bash-checklist-run", "js-claims-check"]
with open(os.path.realpath(__file__), "rb") as handle:
    digest = hashlib.sha256(handle.read()).hexdigest()
document = {
    "schema": "pin-disposition-v1",
    "tool": "fixture-probe",
    "tool_sha256": digest,
    "status": "ok",
    "observed_at": datetime.datetime.now(datetime.timezone.utc)
                    .strftime("%Y-%m-%dT%H:%M:%SZ"),
    "legs": [{"leg": leg, "content_status": "unchanged",
              "pinned": {"status": "verified"}} for leg in LEGS],
}
print(json.dumps(document, sort_keys=True, separators=(",", ":")))
```

Argv is ignored on purpose: the tool passes `--manifest … --root …` (`:534-536`) and the fixture
must be insensitive to invocation details. Both runs emit the same document except `observed_at`,
which `comparison_block` removes before canonical comparison (`:383-391`); `raw_stdout_equal` is
recorded but is not a `decide()` input.

### 4.3 `lane/.ufo/evidence/round-13/expected.json`

```json
{"inputs": {"tools/pin-disposition.py": "<sha256 of the probe bytes written above>"}}
```

`evaluate()` requires only that `inputs` is an object and that `inputs[PROBE_REL]` equals the disk
digest (`:488-501`). The digest must be computed by the fixture generator **after** writing the
probe.

### 4.4 Synthetic runner — `lane/tools/mutate-and-run.sh`

Must satisfy `parse_runner_mapping` (`:213-257`) and `mapping_block` (`:259-337`): six header rows,
six unique `PIN_` 64-hex constants, six unique `REV_` 40-hex constants, and six `regression_case_git`
calls inside a literal `run_regression() {` … `}` body, in manifest order. Leg names and variable
suffixes are fixed by `EXPECTED_SUFFIX` (`:74-81`): `JS`, `BASH`, `TSUKUROI`, `MADO`, `CHECKLIST`,
`CLAIMS`. Each manifest row's `repo`/`path` must equal both the header and the call (`:276-290`).

```sh
# js-kimi-census synth/legs/js-kimi-census.txt 1/1 (100%)
# bash-surface-census synth/legs/bash-surface-census.txt 1/1 (100%)
# bash-tsukuroi-census synth/legs/bash-tsukuroi-census.txt 1/1 (100%)
# bash-mado-verify synth/legs/bash-mado-verify.txt 1/1 (100%)
# bash-checklist-run synth/legs/bash-checklist-run.txt 1/1 (100%)
# js-claims-check synth/legs/js-claims-check.txt 1/1 (100%)

PIN_JS=42d1aec8554ed11e9a9de409168d963c8de9773cd982cf84f65889de1334a612
PIN_BASH=c31222e856594f9b548e15dc7150307665b717448847f71c7270554fecba7319
PIN_TSUKUROI=1a233d3b59a9a8bb86a3f5afe391eb860e33030f1d40d0ef519ab459a0e1ee19
PIN_MADO=50b400c47b2a38aec88d26a4c271b96dbced8ca1a1170e73f5cd17985ca67a8b
PIN_CHECKLIST=c52b0ef931139a1b8e72f69883b4f527e62786fdc0caa3b3b63b6fcebcfb8c39
PIN_CLAIMS=73d9dc50faa60037e37c6728be4af10dfeb64fd6e7cfc90c9253ed691efde977

REV_JS=de1764cd535e94b591fd30340c2d2521b2b0c964
REV_BASH=99137cd4e9acf643175c8e455c05035b1d78c3ef
REV_TSUKUROI=ba7e944d114ad12836aa8e08095eb174748c3d11
REV_MADO=831807a33a4c35288f0299ca022b8bd0dea5e458
REV_CHECKLIST=db9a944f41da25f9e26903cdc9794094bc11eb2b
REV_CLAIMS=41ee4d979b1d355e58bc2d0d5cef8a6986b37d40

run_regression() {
  regression_case_git js-kimi-census 'synth/legs/js-kimi-census.txt' "$PIN_JS" "$REV_JS" "fixture digest" 'fixture note' "$TABLE_JS"
  regression_case_git bash-surface-census 'synth/legs/bash-surface-census.txt' "$PIN_BASH" "$REV_BASH" "fixture digest" 'fixture note' "$TABLE_BASH"
  regression_case_git bash-tsukuroi-census 'synth/legs/bash-tsukuroi-census.txt' "$PIN_TSUKUROI" "$REV_TSUKUROI" "fixture digest" 'fixture note' "$TABLE_TSUKUROI"
  regression_case_git bash-mado-verify 'synth/legs/bash-mado-verify.txt' "$PIN_MADO" "$REV_MADO" "fixture digest" 'fixture note' "$TABLE_MADO"
  regression_case_git bash-checklist-run 'synth/legs/bash-checklist-run.txt' "$PIN_CHECKLIST" "$REV_CHECKLIST" "fixture digest" 'fixture note' "$TABLE_CHECKLIST"
  regression_case_git js-claims-check 'synth/legs/js-claims-check.txt' "$PIN_CLAIMS" "$REV_CLAIMS" "fixture digest" 'fixture note' "$TABLE_CLAIMS"
}
```

The hex values shown are illustrative fixture constants (sha256/sha1 of each leg name), not repo
digests; they must be copied verbatim into the manifest `expected_sha256` / `pinned_commit` fields.
Do not add any other line matching the header or constant regexes. The runner is parsed as text and
is never executed (`:9-10`).

### 4.5 Synthetic manifest — `lane/.ufo/evidence/round-13/pin-manifest.json`

```json
{
  "schema": "pin-manifest-v1",
  "derived_from": {"path": "tools/mutate-and-run.sh", "sha256": "<sha256 of the runner bytes>"},
  "legs": [
    {"leg": "js-kimi-census", "repo": "synth", "path": "legs/js-kimi-census.txt",
     "pinned_commit": "de1764cd535e94b591fd30340c2d2521b2b0c964",
     "expected_sha256": "42d1aec8554ed11e9a9de409168d963c8de9773cd982cf84f65889de1334a612"},
    {"leg": "bash-surface-census", "repo": "synth", "path": "legs/bash-surface-census.txt",
     "pinned_commit": "99137cd4e9acf643175c8e455c05035b1d78c3ef",
     "expected_sha256": "c31222e856594f9b548e15dc7150307665b717448847f71c7270554fecba7319"},
    {"leg": "bash-tsukuroi-census", "repo": "synth", "path": "legs/bash-tsukuroi-census.txt",
     "pinned_commit": "ba7e944d114ad12836aa8e08095eb174748c3d11",
     "expected_sha256": "1a233d3b59a9a8bb86a3f5afe391eb860e33030f1d40d0ef519ab459a0e1ee19"},
    {"leg": "bash-mado-verify", "repo": "synth", "path": "legs/bash-mado-verify.txt",
     "pinned_commit": "831807a33a4c35288f0299ca022b8bd0dea5e458",
     "expected_sha256": "50b400c47b2a38aec88d26a4c271b96dbced8ca1a1170e73f5cd17985ca67a8b"},
    {"leg": "bash-checklist-run", "repo": "synth", "path": "legs/bash-checklist-run.txt",
     "pinned_commit": "db9a944f41da25f9e26903cdc9794094bc11eb2b",
     "expected_sha256": "c52b0ef931139a1b8e72f69883b4f527e62786fdc0caa3b3b63b6fcebcfb8c39"},
    {"leg": "js-claims-check", "repo": "synth", "path": "legs/js-claims-check.txt",
     "pinned_commit": "41ee4d979b1d355e58bc2d0d5cef8a6986b37d40",
     "expected_sha256": "73d9dc50faa60037e37c6728be4af10dfeb64fd6e7cfc90c9253ed691efde977"}
  ]
}
```

`validate_manifest` (`:439-463`) enforces six unique legs, non-empty strings, 40-hex commit and
64-hex digest; `derived_from.path` must `endswith("tools/mutate-and-run.sh")` and its `sha256` must
equal the synthetic runner's disk digest (`:506-515`).

### 4.6 Stub `git` — `<tmp>/bin/git`, mode `0755`

```sh
#!/bin/sh
# Fixture control: deliberately ignores GIT_DIR / GIT_CONFIG_*; never opens a repository.
printf '.git\n'
exit 0
```

It must (a) exit 0 in both runs, (b) write a non-empty stdout in both, (c) never echo the poison
path, (d) produce identical output/exit in both runs. That makes `baseline_ok=True` and
`reflects=False` → `effective=False`.

### 4.7 Invocation and fixture-generation order

1. `mkdir` the tree above.
2. Write synthetic probe → compute its sha256 → write `expected.json`.
3. Write synthetic runner → compute its sha256 → write `pin-manifest.json`.
4. Write stub `git`; `chmod 0o755`.
5. Copy the active tool bytes to `lane/tools/context-capture.py` (byte copy; this is the public CLI
   under test).
6. Assert the declared poison path does not exist (`os.path.lexists(POISON_PATH) == False`); if it
   exists, the fixture is unrunnable and must fail loudly rather than emit exit 2.
7. Run the **public CLI** as a subprocess with no arguments:
   `env = {**os.environ, "PATH": f"{tmp}/bin:{os.environ['PATH']}"}`, `cwd=tmp`,
   `stdin=DEVNULL`, capture stdout/stderr, `python3 <tmp>/lane/tools/context-capture.py`.
   The stub must be first on `PATH` so `shutil.which("git")` (`:527-531`) resolves it; real
   `python3` must remain resolvable after it.

No fixture file is read from the real lane, no network is used, and the only writes are under
`<tmp>` (receipt at `lane/.ufo/evidence/round-15/context-receipt.json`). The one absolute metadata
probe is `lexists(POISON_PATH)`; prefer a single narrow poison-path override (defaulting to the
historical literal) so the fixture can point at an absent `<tmp>` subpath and be independent of host
state. That override changes no gate semantics — the receipt's own delta check derives from the same
constant.

## 5. Literal expectations to pin

Pinned in the selftest (derived from `:553-579`, `:583-643`; **not executed here**):

| Observable | Literal expected value |
|---|---|
| process exit | `1` |
| stdout substring | `exit=1 probe-equal=True poison-control=False runner-mapping=True` |
| stdout line (full, when the promoted receipt path is declared) | `CONTEXT: MISMATCH (receipt=.ufo/evidence/round-15/context-receipt.json exit=1 probe-equal=True poison-control=False runner-mapping=True)` |
| receipt `status` | `"mismatch"` |
| receipt `exit` | `1` |
| receipt `reasons` | exactly `["git poison positive control is ineffective"]` (length 1 — proves the control is the sole failing branch) |
| receipt `positive_control.effective` | `false` |
| receipt `positive_control.baseline_ok` | `true` |
| receipt `positive_control.injected_reflects_poison` | `false` |
| receipt `positive_control.baseline.exit` / `.injected.exit` | `0` / `0` |
| supporting pass fields | `comparison.equal == true`, `mapping.all_match == true`, `environment.env_delta_matches_declared == true`, `environment.baseline_has_GIT_DIR == false` |
| receipt file | exists at the promoted round-15 output path (mismatch path still writes, `:629-635`) |

Pin the reason **list** rather than checking "contains": a substring assertion would hide an
additional accidentally-failing branch and would not prove fixture isolation. The full stdout line
may be pinned only after the promoted `OUTPUT_REL` is fixed; otherwise pin the stable
`exit=1 … poison-control=False` segment plus the receipt JSON.

Optional variant (same token, same exit, not required): stub exiting 128 in both runs makes
`baseline_ok=False`; `reflects` stays False (equal exits, no poison text), so `effective=False` and
the reason list is again exactly one entry. It exercises the other disjunct but conflates "git
unusable" with "poison unobservable", so it must not replace the primary fixture.

## 6. Explicit non-goals and bounds

- This fixture proves the gate's decision wiring for an ineffective positive control and its exact
  retained token/exit. It is **not** evidence about real git, real probe authenticity, real manifest
  contents, leg execution, suite environment, dependency identity, or result reuse.
- It does not validate the other `decide()` branches; those belong to the sibling specs. It does not
  create or require a finding-ID taxonomy, A-B-A/retry, snapshot modes, or environment claims.
- The synthetic probe/runner/manifest bind only their own fixture bytes; the source-digest checks
  are exercised as pass-throughs so the control branch is isolated, not as provenance evidence.
- No real round-12/13/14 file is read, written, or referenced by the fixture; no round-14 receipt
  is overwritten.

## 7. Implementation-critical notes for ContextGate (also sent to L1)

1. Keep the literal `git poison positive control is ineffective` as the retained token for this
   branch; if IDs are added, declare one for this reason in source and pin it next to the literal.
2. Add this stub-git fixture to `--selftest` with the exit-1 and receipt assertions in §5.
3. Correct `LANE_ROOT` derivation for `tools/` placement (two `dirname`s, or an explicit fixture
   root); a verbatim copy of `:32-34` breaks both the fixture and the real capture root.
4. Normal capture must write round 15 only; the fixture relies on the mismatch path still writing a
   receipt inside the temp lane.
5. If strict temp containment is wanted, one narrow poison-path override with the historical
   literal default is sufficient; do not add broader environment validation.

## 8. Tooling record

No install or update was performed. Facts used: Python 3.14.7 and git 2.55.0 already present;
`/nonexistent` absent on the host at read time. Report write only; no gate, selftest, build, test,
or formatter was run by this seat.
