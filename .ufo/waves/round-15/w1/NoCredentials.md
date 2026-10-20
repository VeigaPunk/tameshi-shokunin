# NoCredentials — credential / non-secret environment boundary (round 15, w1)

Seat: sentinel, leaf. Scope: historical harness `.ufo/evidence/round-14/capture-context.py`
(sha256 recorded in its receipt as `7313e9a2…7d89`, bytes not modified), retained
`context-receipt.json` / `context-missing-env.json`, the shared plan (ContextGate task text in
`.ufo/waves/round-15/dispatch1.json`, integration interface in `spec1.json:3`), and the probe it
executes (`tools/pin-disposition.py`). The new `tools/context-capture.py` was **absent at read
time** (glob: "Skipped missing paths"), so the recommendations below are design constraints, not a
review of landed code.

Nothing was executed: no gates, selftests, CLIs or environment dumps. No credential/auth file,
`~/.omp/agent/agent.db*`, or environment variable value was read. Tool installs/updates: none.
`RULES.md` was not needed because nothing was installed.

## Axes

A1 secret values never serialized · A2 secret-bearing paths never read or hashed · A3 child
processes don't receive ambient secrets they don't need · A4 the receipt claims only what the tool
checks.

## Observed boundary (historical source)

| Fact | Evidence | Status |
|---|---|---|
| The tool opens only five fixed lane-relative files plus itself (`PROBE_REL`, `RUNNER_REL`, `MANIFEST_REL`, `EXPECTED_R13_REL`, `SELF`). It writes only `OUTPUT_REL`. | `:54-58`, `:476-479`, `:414-416`, `:583-602` | A2 holds for the tool's own reads |
| Child env = the whole ambient environment minus `GIT_*`, plus `LC_ALL=C` | `safe_env` `:184-187`; used for both probe runs `:539-540` and the git control `:547` | A3 **not** held: non-`GIT_*` ambient values pass through (tokens, `SSH_AUTH_SOCK`, `PYTHON*`, `LD_*`) |
| Removed ambient `GIT_*` are recorded **by name only** | `:466-468` | A1 holds (values like `GIT_CONFIG_PARAMETERS` / `GIT_ASKPASS` are never written) |
| Receipt serializes `argv`, `cwd`, `exit` and **verbatim child stdout/stderr**, never an env mapping | `run_bounded` `:209-210`, `invocation` `:420` | A1 holds for tool-authored fields; child output is retained unfiltered |
| `"ambient_env_dumped": False` is a literal constant, never computed | `:427` | A4 risk: it's true only "by construction", and only for tool-authored fields |
| JSON parse errors report label + line/column only, never content | `:167-181` (`:177`) | A1 holds on error paths |
| Probe digest is compared **after** reading but the probe is executed regardless of the result. A mismatch only surfaces later in `decide` as exit 1. | `matches_declared` `:500-502`; unconditional runs `:538-540`; `decide` `:571-572` | A3/A4 gap (R1) |
| Receipt is `0644` | `:594` | Retained child output is world-readable |
| Probe pins leg repo/path to the six canonical constants, so a tampered manifest can't redirect hashing to credential material | `tools/pin-disposition.py:128-134`, `:527-541` | A2 holds for an **unmodified** probe |
| Probe git env scrubs `GIT_*` and bypasses global/system config. It also sets `GIT_TERMINAL_PROMPT=0` and `GIT_NO_LAZY_FETCH=1`, and uses only `rev-parse`/`cat-file`. | `tools/pin-disposition.py:73-78`, `:197-210` | No credential-helper or network path observed. `[INFERENCE]` from documented git env semantics; not executed |
| Harness positive control adds `GIT_CONFIG_NOSYSTEM`, `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_TERMINAL_PROMPT=0`, and runs only `rev-parse --git-dir` | `:62-67`, `:395-411` | No fetch/credential path |
| Retained receipts contain no secret-shaped strings | Shape-only regex grep (token/api-key/password/secret/`ghp_`/`github_pat_`/`sk-`/`AKIA`/`SSH_AUTH`/PRIVATE KEY/Authorization) over both round-14 receipts → **0 matches** | Observed clean; bounded to those patterns |
| Policy | `AGENTS.md:5` "Secrets are shape-only, never content-read"; `PROVINCE.md:18`; `corpus/knowledge/service-limits.md:50` row (e) | Contract the new tool must keep |

## Findings (supported risk only)

### R1 — Low: an unverified probe still runs with the ambient environment, and its output is kept verbatim
- **Exploit path:** an actor who can modify `tools/pin-disposition.py` (any writer to the lane tree) makes it print `os.environ` or other secret material to stdout. The harness hashes the file, sees `matches_declared=false` (`:500-502`), and still runs it twice with the full non-`GIT_*` ambient env (`:539-540`). It then stores both stdouts verbatim in `runs.*.stdout` (`:209-210`) and writes the receipt `0644` (`:594`). That receipt is an evidence artifact intended to be committed. Exit 1 flags the mismatch, but the secret is already on disk. There is also a hash→exec TOCTOU: bytes are hashed at `:476`, then the path is re-opened by `python3` at `:538`. The payload's self-reported `tool_sha256` (`:375-378`) can be forged by the modified probe, so it is not a defence.
- **Bounding:** the same writer could modify the harness itself, so the extra capability is small. That is why this is Low. No secret leak was observed: the 0-match shape scan is above.
- **Smallest remediation (new tool, normal capture mode):** run no child until `sources.probe.matches_declared` and `sources.runner.matches_manifest_declaration` are true. On failure, write the receipt with `runs`/`comparison` marked not executed, plus the existing digest reason. Keep the `decide` reason strings and exit class unchanged (exit 1 for digest mismatch), so the decide semantics are reused rather than redefined. Optionally re-hash the probe after both runs and treat a change as a mismatch; this is cheap and closes the TOCTOU window for detection only.

### R2 — Low (claim accuracy, A4): `ambient_env_dumped: false` over-reads
- **Evidence:** it is a constant (`:427`). Meanwhile child stdout/stderr are retained unfiltered (`:209-210`), so the receipt can contain environment-derived bytes whenever a child prints them.
- **Smallest remediation:** in the round-15 receipt, either keep the field but document it as "tool-authored fields contain no environment values; child stdout/stderr retained verbatim", or rename it to that scope. A retained-receipt check must **not** treat this field as evidence of anything. Don't add a broad "no secrets in receipt" claim; it isn't measured.

### R3 — Medium for the selftest only: ambient pass-through would make `--selftest` non-hermetic
- **Evidence:** if the selftest launches the public CLI with `env=None` (inherit), or with an ambient-derived env like `safe_env`, every synthetic fixture child receives the operator's ambient secrets and `PYTHON*`/`LD_*`/`PATH` influences. The fixture outcome then depends on the host. The isolated-selftest contract (`spec1.json:3`: "no live reads/network/writes outside temp roots") is not met. The lane already has the right pattern in `tools/pin-disposition.py:648-680`: scrub `GIT_*`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `HOME=<scratch>`, fixed author identity, empty templates/hooks dirs, `commit.gpgsign=false`.
- **Smallest remediation:** each selftest CLI subprocess gets an **explicit allowlist mapping**, not ambient-minus-denylist. Python `subprocess` docs (S049, already admitted at `round-14-verifier-spotcheck.md:130`): "If env is not None, it must be a mapping that defines the environment variables for the new process". The mapping contains exactly:
  - `PATH` — the parent's PATH, needed so the CLI's `shutil.which("python3"/"git")` resolves;
  - `LC_ALL=C`;
  - `HOME=<tmp>` and `TMPDIR=<tmp>`;
  - `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=/dev/null`.

  Optionally launch the CLI as `[sys.executable, "-I", cli, …]`, so `PYTHON*` variables and user site-packages can't run code inside it. Fixture `git init` reuses the pin-disposition pattern above. Expected exits and finding IDs are unaffected: the CLI's own `safe_env` derives from this mapping, and the receipt never serializes env values.

### R4 — Low (A1/A2): the new retained-receipt check reads a caller-chosen path
- **Exploit path:** if `--check PATH` accepts any path, a mistaken or hostile invocation can point it at credential material. If the tool then echoes bytes in errors, or prints a digest before validating, it "content-reads/hashes" a secret-bearing path, which violates `AGENTS.md:5` and `service-limits.md:50`.
- **Smallest remediation:** reuse the historical `parse_json` (`:167-181`) unchanged, so errors carry only label + line/column. Emit any digest of the checked file only after it parses as a JSON object with the expected round-14/round-15 receipt `schema`; a key or token file can't pass that. Never print the receipt's retained `runs.*.stdout/stderr` to the terminal. Lane path containment for `PATH` belongs to PathContainment's surface; it is not restated here.

## Non-risks confirmed (don't spend fixes here)
- A tampered manifest can't redirect the probe to secret-bearing files: the canonical repo/path pins are at `pin-disposition.py:527-541`.
- `ambient_git_keys_removed` is names-only. Keep it that way; never add values.
- `lane_root`/`fleet_root`/home-directory paths in the receipt are non-secret and already retained in round 14. Selftest stable IDs must not embed temp paths. That is a stability concern, not a credential one.
- The git positive control and probe git calls are local plumbing with prompts disabled. `[INFERENCE]`: no credential helper is reachable. Not executed this round.

## Optional, only if ContextGate wants a non-vacuous A1 fixture (not required by the gate standard)
These are fixture-advice suggestions, not executed results:
- **Canary pair.** Put the literal `TAMESHI_R15_SELFTEST_CANARY=r15-canary-7f3c` in the selftest allowlist env.
  - **Negative case:** a synthetic probe that doesn't print it. Assert the literal is absent from the CLI's stdout, stderr and receipt bytes.
  - **Positive control:** a synthetic probe that prints it inside its JSON. Assert the literal **is** present in `runs.baseline.stdout`. This documents verbatim child retention (R2) and proves the absence check can fail.
- **Claim boundary.** The canary is synthetic, not a secret. The pair supports only "tool-authored fields carry no env values". It does not support any broad no-secret or environment-independence claim (rejected row, `round-14-verifier-spotcheck.md:127`).

## Read revision
Historical harness bytes per receipt `tool_sha256` 7313e9a2…7d89 (not re-hashed: no execution). `tools/pin-disposition.py` read revision corresponds to receipt `sources.probe.sha256` 29725397…1f11 [INFERENCE: not re-hashed]. `tools/context-capture.py` absent at read time.
