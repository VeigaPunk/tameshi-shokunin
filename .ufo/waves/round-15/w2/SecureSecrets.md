# SecureSecrets — round-15 wave2 sentinel: env/auth/agent-DB and subprocess secret capture

Seat: `TameshiR15.SecureSecrets` (sentinel, leaf). Static review only. I executed nothing: no
`--check`, no `--selftest`, no interpreter. I read no credential, auth, env, or `agent.db*` file.
I installed no tools.

## Exact source read

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/context-capture.py`, snapshot tag `#472A`
(2116 lines). Ranges read: 1-123 (docstring and imports), 252-281 (USAGE), 296-512 (read/parse
helpers, `require_*`, `validate_top`), 515-555 (`validate_environment`, via grep context),
805-846 (`recompute_environment`, via grep), 1186-1346 (expected pin, `make_result`, `emit`,
`apply_expected`, `run_check`), 1572-1733 (`SELFTEST_ENV`, `SelftestHarness`), 1736-2002 (selftest case list,
via grep), 2005-2116 (`run_selftest`, `parse_argv`, `main`). I grepped the whole file for
`environ|getenv|open(|subprocess.|os.stat|listdir|expanduser|HOME|agent.db|.omp|token|secret|credential|auth`.
I also grepped lines 556-1182 for every `.format`/`repr`/`exc` echo site.

Context also read: `corpus/lessons/round-14-verifier-spotcheck.md`, "Routed defects and
residuals" (lines 154-157).

## Axes

A1: ambient env read. A2: auth/agent-DB access. A3: subprocess env/secret capture. A4: content
echoed from files read on a caller-named path. A5: honesty of the "no credentials" claim.

## Bounded agreement (A1, A2 default path, A3)

- **A1 — the tool never reads env itself.** The file has no `os.environ`, `os.getenv`,
  `expanduser`, or `HOME` reference. Every `GIT_DIR` mention is a literal constant compared
  against receipt fields (`INJECTED_ENV` L146, `recompute_environment` L805-846).
  `validate_environment` L549-554 rejects any receipt that declares `ambient_env_dumped` other
  than literal `False`. The only implicit env use is `tempfile.mkdtemp` in the selftest parent,
  which honours `TMPDIR`. That is benign and outside check mode.
- **A2 on the default path.** Frozen mode builds exactly one path:
  `DEFAULT_LANE_ROOT/.ufo/evidence/round-14/context-receipt.json` (L1301-1302).
  `tool_sha256()` reads only `SELF` (L300-305). Nothing references `~/.omp` or `agent.db`.
  Every `open` is read-only `"rb"`, except the selftest fixture writes under `mkdtemp`
  (L1622, L1634). Check mode does not mutate anything.
- **A3 — subprocess isolation holds.** `SelftestHarness.run` L1602-1609 is the file's only
  `subprocess.run`. It passes `env=SELFTEST_ENV`, a full replacement holding only `PATH`,
  `LC_ALL` and a poison `GIT_DIR` (L1572-1576), so no ambient API key or token reaches a child.
  It also passes `sys.executable -I` (ignores `PYTHON*` env and user site),
  `stdin=DEVNULL`, a temp `cwd`, and `timeout=60`.
  - The children are only this tool. Each case passes an explicit temp `--receipt`/`--expected`
    (L1637-1640), and the usage cases fail during argv parsing (L1996-2002).
  - No selftest case runs frozen mode or names a lane or home path.
  - Captured child stdout/stderr stays in memory. It is printed only on a failed case, capped at
    400 characters (L1674-1682, L1695-1698), and comes from synthetic fixtures.
  - `run_selftest` removes the temp root in a `finally` (L2016-2017).
- **No-traceback guarantee.** `main` L2106-2112 turns unexpected exceptions into
  `internal_error`. Its detail is `type(exc).__name__: str(exc)`. For the JSON paths reachable
  from an arbitrary file, the realistic exceptions are `RecursionError` and `MemoryError`; their
  messages carry no file content.

## Counterexample (A2 explicit mode, A4, A5) — severity LOW, not implementation-critical

**Where.** Explicit mode does not confine paths. `parse_argv` L2050-2064 accepts any non-empty
string. `read_regular` L330-349 follows symlinks (`os.stat`), accepts any `S_ISREG`, and reads it
whole and unbounded. `run_check` L1313 loads `--expected` before it touches the receipt.

Concrete invocations, shown as static derivation only (I did not run them):

1. `context-capture.py --check --receipt X --expected <any caller-named JSON file, e.g. under ~/.omp/agent/> --json`
   - `load_expected` → `validate_expected` L1190-1196 raises `expected_invalid`.
   - The detail is `"<path> keys mismatch (missing=[...], extra=[<every top-level key name>])"`.
   - `main` L2101-2105 emits it on stdout, exit 2.
   - **Effect:** a one-step disclosure of the file's top-level key names. String values are
     never echoed: `require_string`, `require_hex`, and the schema and `FINDING_ID` messages are
     all fixed text. A duplicated key is echoed by `repr` (L312). An integer `exit` value is
     echoed (L401) only when all four keys are present.
2. `--receipt ~/.omp/agent/agent.db` (or `/proc/self/environ`) `--expected <any valid pin>`
   - `/proc/self/environ` passes `S_ISREG`. Its bytes are the process's own ambient env,
     secrets included.
   - The digest misses the pin, so the result is `snapshot_tampered`. L1324-1332 prints the
     file's full sha256, a digest oracle for the secret file.
   - Content stops there. A caller who then pins that digest reaches `parse_json_strict`, and
     `JSONDecodeError` messages carry no content.
   - `validate_top` L463-467 rejects any root without `status ∈ {ok, mismatch, invalid_input}`,
     using a fixed message. So a credential file never reaches the stages that echo key names
     or values.
   - The value-echo sites (L937-1118: `{!r}` of `error`, `observed_at`, booleans) are reachable
     only for documents that already satisfy the full receipt schema.

**Impact.** These are not privilege escalations: the tool runs as the caller, with the caller's
read authority. But the gate can be pointed at agent-DB, auth, or env files. It will read them,
print a digest of any such file, and print the top-level key names of any such JSON file. A
lane runner that retains `--json` output would put those into evidence.

The docstring line 105, "No credentials are read.", is unconditional. It holds only for frozen
mode and `--selftest`. USAGE L262-264 ("does not … read live lane inputs") has the same gap in
explicit mode. That is an A5 overclaim, not a fabricated result.

**Smallest remediation (no new broad claim).** Two options:

- Reword docstring L105 to: "No credentials are read by default; explicit --receipt/--expected
  read exactly the caller-named paths, with no confinement." Mirror that in USAGE.
- Optionally, drop the key-name lists from the `expected_invalid` detail (L1195) and from
  `require_object`, and report counts only. Neither is needed for the stable-id or exit
  contract.

Path deny-lists (`~/.omp`, `/proc`) are brittle and not recommended.

## Disposition

- No implementation-critical defect on this surface, so I did not message `TameshiR15`.
- A1 and A3: bounded agreement with the source as read.
- A2, A4, A5: one LOW finding. It is caller-directed explicit-mode reach plus an unconditional
  docstring claim. The remediation is wording-level.
- Runtime confirmation of the selftest isolation and of the expected-file key echo is left to L1
  verification. I claim no executed result.
