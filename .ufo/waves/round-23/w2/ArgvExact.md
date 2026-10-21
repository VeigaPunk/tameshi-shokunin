**Verdict:** I found no defect in the gate's argv comparison. Order, extra flags, joined strings and per-name swaps are all rejected by the exact list comparison at `tools/command-binding.py:103`. The real gap is calibration: no fixture swaps argv between two named requirements, so a regression to "matches any requirement's argv" would pass every test. I wrote nothing, as this wave forbids writes, so the requested `.ufo/waves/round-23/w2/ArgvExact.md` report does not exist; L1 can persist these findings. I ran no builds, tests or gate invocations, only read-only parsing of the JSON artifacts. Nothing was installed.

**What I checked, all at revision 336565f:**
- **Exact comparison.** `receipt['argv'] != required['argv']` compares lists by order, length and every string, with no normalization. Receipts are looked up by name. A receipt whose argv is a string instead of a list is caught by the shape check as `INVALID_RECEIPT` (exit 2).
- **Order, extra flags, joined strings.** The fixtures `argv-order`, `argv-missing`, `argv-extra`, `argv-joined-collision` (`'gate.py --selftest'` as one token), `argv-normalized` (`./gate.py`) and `argv-shell-string` would each catch a weaker comparison. That includes sorted or set comparison, prefix matching, `' '.join` and whitespace-split comparison, `shlex.join`, and path normalization.
- **No joined-string identity elsewhere.** Nothing in `tools/` or the round-23 scripts joins argv into a key. The 43-row replay bundle has no duplicate argv lists, no duplicate joined strings, no tokens containing spaces and no empty tokens.
- **Unicode.** Two different strings can map to the same exec bytes (for example `é` versus surrogate-escaped `\udcc3\udca9`). The gate then reports `ARGV_MISMATCH`, which is the safe direction. I found no case where unequal argv compares equal.

**Counterexample (the gap):** Replace the check with a name-insensitive one, such as `receipt['argv'] not in [r['argv'] for r in requirements.values()]`. That mutant survives all 38 selftest cases and the 10-case `measure.py` counter:
- I scanned every fixture: no receipt ever carries another requirement's argv under its own name.
- Every argv fixture uses an argv that matches no requirement at all (`['cat','gate']`, reordered, extended).
- `mutate.py` only tests `if False:` for the argv guard, so this mutation was never tried.

Take the selftest base and swap only the argv of `clean` and `red`, keeping exits and stdout. The real gate gives exit 1 with `ARGV_MISMATCH`; the mutant gives exit 0, clean. The same blind spot covers case-only differences (`--Selftest`), whitespace-padded tokens and repeated flags (`--selftest --selftest`): no fixture would catch a lowercasing, stripping or de-duplicating comparison. That is lower priority, because those regressions are less plausible.

**Smaller findings:**
1. **The replay can't fail on argv.** `replay.py:62` sets receipt argv to `list(row['argv'])`, the same registry row that `requirements` comes from. That list is what gets spawned (`run_row` calls `Popen(row["argv"])` without rewriting), so the claim is faithful, but the replay's clean result says nothing about argv. The only real-world `ARGV_MISMATCH` evidence is the source-read pair (`cat tools/registry.json` against `receipt-measure-selftest`), which is a different program, not a near-miss. The knowledge doc says "retain actual argv", but what is retained is the declared list given to `Popen`, not one read back from the process. If `run_row` ever rewrites argv (for example to `sys.executable`), the replay would silently keep reporting the registry argv. This is a tradeoff, not a false claim today.
2. **Exact argv doesn't fix which program ran.** `python3` is found on the inherited `PATH`, and the receipt doesn't record the resolved interpreter. This falls inside the doc's stated "no producer/execution authentication" limit, so it's not overclaimed.
3. **Empty-string arguments are rejected.** `strings()` refuses `''` elements, so a legitimate command with an empty argument can't be declared and returns `INVALID_REQUIREMENT` (exit 2). No current row is affected; it fails safe.

**Axes affected:** calibration, through how much the mutation and fixture suite proves. Correctness of the gate itself is unaffected, and nothing here needs the Rust judge to reject a tradeoff.

**Smallest safe correction (no production code change):**
- Add an `argv-swapped-between-names` case to `extra-cases.json`: base requirements, with the receipts' argv swapped between the two names and exits and stdout unchanged. Expected result: exit 1, `["ARGV_MISMATCH"]`.
- Optionally add case-only and padded-token variants.
- Add a name-insensitive mutant to `mutate.py`'s `MUTANTS` list.
- Update the selftest pass count in the `command-binding-selftest` row's token in `tools/registry.json` (currently `38/38 pass`), since it moves with the fixture count. Then re-freeze the replay digest if L1 rebuilds it.

If L1 chooses to record the spawned argv in finding 1, the fix is to keep `proc.args` from `run_row` and use it for the receipt instead of the row copy.
