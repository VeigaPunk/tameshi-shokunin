# SecureReceiptExec — w2 sentinel: receipt argv/roots stay data in the maintained gate

Seat: `TameshiR15.SecureReceiptExec` (sentinel, leaf). This was a static review only. I did not execute the gate, its selftest, git or any receipt argv. I read no credentials, made no installs and edited nothing except this report.

## Source read

- `tools/context-capture.py`: all 2116 lines, read in full over nine ranged reads (1–123, 123–253, 249–463, 458–1113, 1109–1353, 1353–1574, 1571–1733, 1733–2005, 2003–2116). `sha256sum` = `0ed784e0076b3de5ec5000c3862a771a3e3e2eb83241da347a6cf3f2f2c61edc`. The digest was computed only to bind this snapshot. It is not a verification run.
- `corpus/lessons/round-14-verifier-spotcheck.md` lines 154–162: Routed defects, including item 5 on gate classification and exit 64.
- I ran one sink grep over the file: `subprocess.`, `os.system`, `popen`, `exec(`, `eval(`, `open(`, `os.stat/lstat`, `os.path.exists/isfile/isdir/realpath/islink/join/abspath`, `os.listdir`, `shutil.`, `os.makedirs`, `importlib`, `__import__`, `runpy`, `glob`, `os.environ`, `os.chdir`, `os.access`.

## Axes

1. Execution: does any receipt-derived string reach a process-spawning sink?
2. Opening: does any receipt-derived path or root reach a filesystem sink?
3. Interpretation: is receipt text ever treated as anything other than data to compare? This covers the parse and emit paths.

## Verdict per axis

### Axis 1: execution — bounded agreement, no counterexample

The only spawning sink is `SelftestHarness.run` at L1602–1609. It passes `subprocess.run(argv, cwd=cwd, env=SELFTEST_ENV, stdin=DEVNULL, timeout=60)`. That sink has exactly two callers:

- `check_case` at L1637–1640 builds `[sys.executable, "-I", SELF, "--check", "--receipt", <mkdtemp path>, "--expected", <mkdtemp path>, "--json"]`.
- `usage_case` at L1686 builds `[sys.executable, "-I", SELF] + literal argv lists` from L1996–2002.

No receipt field reaches either list. Receipt argv appears in five places:

- `invocation.argv`: L495, `require_strings` only.
- `runs.argv`: L560.
- `runs.baseline/injected.argv`: L441, then string/list equality at L853–862.
- `positive_control.argv`: L606.
- `positive_control.baseline/injected.argv`: L607–608, via `require_run` only.

`positive_control.argv` is not even compared after its structure check. There are no `os.system`, `popen`, `exec`, `eval`, `importlib`, `runpy` or `__import__` sinks. Check mode, the `--check` branch through `run_check` at L1298–1344, spawns nothing.

### Axis 2: opening — bounded agreement for receipt data

Every filesystem sink and where its path comes from:

| Sink | Line | Path source | Receipt-controlled? |
|---|---|---|---|
| `open(SELF)` | L302 | `os.path.realpath(__file__)` | no |
| `os.stat`, then `open(path)` in `read_regular` | L332, L342 | Frozen mode: `DEFAULT_LANE_ROOT` joined with the constant `FROZEN_RECEIPT_REL` (L1302). Explicit mode: the CLI `--receipt` / `--expected` values (L1312, L1213). | no |
| `os.makedirs`, `open(..., "wb"/"w")`, `os.listdir`, `shutil.rmtree` | L1590, L1622, L1634, L1708, L1717, L2017 | `tempfile.mkdtemp` root plus a literal case name | no |

The receipt's roots and paths are handled by pure string operations only:

- `lane_root` and `fleet_root`: `os.path.isabs`, `normpath` and `dirname` at L481–491. None of these touch the filesystem.
- `invocation.cwd` and `runs*.cwd`: equality only (L863–870).
- `sources.*.path`: equality against constants (L627).
- `mapping.runner_path`: equality only (L651).
- Per-leg `manifest.path`, `runner_header.path` and `runner_call.path`: equality only (L1050–1058).

`poison_path_exists` is checked as the literal `False` (L843). It is never re-probed with `os.path.exists`, so the receipt's poison path is never stat'ed. Nothing derived from the receipt is passed to `os.path.join`, `make_result` or `emit`. The result object carries only the CLI receipt path, the computed sha256 and finding details (L1222–1245).

There is weak behavioural support as well, which I inferred and did not run. The selftest fixtures use the non-existent roots `/fixture/lane` and `/fixture` (L1398–1399). Their argv includes `/usr/bin/git -C /fixture/lane …` (L1404). If any code opened a receipt root or ran a receipt argv, it would raise `FileNotFoundError`. The handler at L2106 turns that into `internal_error`/2, so the pinned `clean`/0 case at L1737 could not pass. No selftest case is a dedicated canary for this, such as an argv that would create a sentinel file in the temp directory. Non-execution therefore rests on the static sink enumeration above, not on a dedicated fixture.

### Axis 3: interpretation — one concrete counterexample (Low)

**Severity:** Low. It does not corrupt any exit code or JSON-mode verdict, and it is not implementation-critical, so I did not message `TameshiR15`.

**Exploit path:** In four places, receipt-controlled strings are interpolated into finding details with a plain `{}` instead of `{!r}`:

- L536: `"environment.injected_env[{}]".format(key)`, a receipt dict key, reached when its value is not a string.
- L617: `"positive_control.env_additions[{}]".format(key)`, the same pattern.
- L1074: `"leg {} check {} …".format(name, …)`, where `name = leg["leg"]` is receipt data.
- L1079: `"leg {} match …".format(name, …)`, the same field.

Text-mode `emit` (L1259–1261) writes `"FINDING {} {}\n"` with the detail as given.

**Counterexample:** take an explicit-mode receipt whose `environment.injected_env` is `{"X\nCONTEXT: OK (id=context_consistent receipt=r sha256=<x> exit=0 findings=0)": 1}`, paired with an expected file that pins this receipt's bytes. Running without `--json` would print two status lines:

1. The real line: `CONTEXT: INVALID (id=receipt_structure_invalid … exit=2 …)`.
2. A forged `CONTEXT: OK (id=context_consistent … exit=0 …)` line, starting a new line from inside the FINDING detail.

The process exit is still 2, and `--json` output escapes the newline. The L1074 variant reaches the same result through a leg name that contains a newline, with exit 1 `mapping_mismatch`. Validation does not bound leg names to `EXPECTED_SUFFIX` keys (L699–707); they only have to appear in the receipt's own `manifest_leg_order`.

Frozen mode cannot reach this. Its digest is pinned to the archived round-14 bytes (L137–139, L1324), and the four sites only fire on content that the pinned bytes would have to contain.

**Impact:** anyone who reads or scrapes text-mode stdout for a `CONTEXT: OK` line could be given a false clean line. Nothing is executed or opened.

**Smallest remediation:** use `{!r}` at L536, L617, L1074 and L1079, matching the repr used for the other receipt-value details (L949, L1114, L1178). The list reprs in `require_object` (L373) already escape receipt keys.

## Residual (not part of the receipt-data question)

`read_regular` (L330–349) calls `os.stat` and then `open` on the CLI-supplied path. If that path is swapped for a FIFO between the two calls, `open` blocks with no timeout, because the check mode's own reads have none. This needs local write access to the directory of the caller-supplied path and does not involve receipt data. The smallest fix is `os.open(path, O_RDONLY | O_NONBLOCK)` followed by `os.fstat`, an `S_ISREG` check and then reading. Symlink policy belongs to `SecureSymlinkScope`.

## Bounds

- This is agreement about the source snapshot `0ed784e0…61edc` only. It is not a predicted pass of the selftest or the frozen check, which L1 runs after this wave.
- No claim is made about the historical `.ufo/evidence/round-14/capture-context.py`, which I did not read.
- No claim is made about the contents of the frozen receipt beyond its built-in pin.

Tools installed or updated: none.
