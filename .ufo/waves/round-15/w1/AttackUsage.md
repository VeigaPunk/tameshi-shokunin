# AttackUsage — critic, round 15 w1

Assignment: try to break planned C1 on the exit-64 usage class and its stable finding. Build a concrete counterexample that a helper-only test would miss. Separate the required routed fix from optional hardening.

Read revision: lane HEAD `a9cf4da78f2514c7bedd91a850a88590009d7df0`. `tools/context-capture.py` **did not exist** when I read the tree, so every point below concerns the *planned* contract. None of it describes behaviour I observed in new code. Nothing was executed: no gate, no selftest, no harness. The only things run were read-only `git rev-parse`, `sha256sum` and `git status`. Tool installs: none.

Digests I read (historical bytes, which must stay unchanged):

| Path | sha256 |
|---|---|
| `.ufo/evidence/round-14/capture-context.py` | `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89` |
| `tools/evidence-disposition.py` | `1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95` (matches the round-14 lesson's checker hash) |
| `.ufo/evidence/round-14/context-receipt.json` | `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` (`status ok`, `exit 0`, argv `['.ufo/evidence/round-14/capture-context.py']`) |

## Axes

What the claim needs:
- The 64 class is registry-explicit for both tools.
- The 64 path is reached through the real CLI.
- The 64 finding is stable and discriminating.
- The 64 path has no side effects (no receipt, no live read or write).
- 64 stays distinct from 2 and 0.

## Source evidence

- **Historical context script, usage path** (`capture-context.py:605-613`). Any non-empty argv other than exactly `-h` or `--help` writes `capture-context.py: unexpected argument(s): …` plus `USAGE` to stderr and returns 64. This happens before `base_receipt()` (`:614`), so no receipt is written. The docstring (`:29`) says "64 usage error, no receipt". The usage path has no stable finding token; it is free text.
- **`USAGE` text contains the words a weak test would look for.** The `USAGE` string (`:117-124`) contains `usage:` and the literal `exit 64 usage.` `-h`/`--help` prints the same text to **stdout** and exits **0** (`:607-609`). Under PROTOCOL §Gate standard, 0 means `clean`.
- **Exit-2 paths write a receipt.** On `InvalidContext`, `main` still calls `write_receipt()` (`:617-628`) at `LANE_ROOT/OUTPUT_REL`. `LANE_ROOT` is `dirname×4(SELF)` (`:46`), which is correct only at the historical `.ufo/evidence/round-14/` depth.
- **No arguments means a live capture.** `main([])` runs the full capture: it runs the live `pin-disposition.py`, runs live `git rev-parse`, and writes the round-14 receipt.
- **The child probe uses 2 for usage, not 64.** `pin-disposition.py:69-71,147,1196-1238` maps `invalid_usage` to exit 2. So the context gate's own 64 can only come from its own argv. The historical code never propagates the child's exit code: baseline exit ≠ 0 becomes `probe_baseline_unusable`, which becomes 2 (`:340-361`).
- **Round-14 C1 checker.** `evidence-disposition.py:1927-1941` returns 64 for no arguments and for any `UsageError`, with no finding token. Its selftest (`:1828-1837`) asserts exit only (`usage-no-arguments`, `usage-selftest-extra`). The retained output shows `SELFTEST_CASE usage-no-arguments PASS (exit=64 expects=64)` (`verification-final.json:24`). Registry row `SKILL.md:1601` says "64 usage" with no class mapping. Registry row `:1602` (context, labelled `probe`) omits 64 entirely.
- **PROTOCOL.md:380-389.**
  - Every other exit code is declared and mapped to `clean | failed | could-not-evaluate`; an undeclared nonzero code reads as could-not-evaluate.
  - The self-test must assert both an exit code and a stable finding ID.
  - "a helper-only or model-only self-check does not satisfy this clause."
- **No retained evidence of a 64 run exists** for the context harness anywhere under `.ufo/evidence/round-14/`. A grep for `"exit": 64`, `exit=64` and `unexpected argument` matched only the source lines.

## Primary counterexample (a helper-only test passes, the CLI is wrong)

Mutant M1 is a one-line entry-point bug in the new tool:

```python
if __name__ == "__main__":
    raise SystemExit(main(sys.argv))      # argv[0] not stripped
```

M1 keeps historical `main` semantics: non-empty argv other than `-h`/`--help` returns 64. So **every** real CLI invocation, including the registry entry command `python3 tools/context-capture.py` and any `--check FILE`/`--selftest` path, returns 64 with `unexpected argument(s): tools/context-capture.py …` on stderr.

A nominal helper-only selftest **passes** against M1:
- `main(["--bogus"]) == 64`
- `main(["--check", fixture]) == 0` in-process
- `decide(fixture) == ("ok", 0, [])`
- the missing-field and variable-swap helper controls from round 14

Even one subprocess usage case `[sys.executable, SELF, "--bogus"]` that asserts `returncode == 64` and `"usage" in stderr` **passes** against M1. Both the exit and the substring are satisfied by the broken entry point.

What fails M1: a subprocess case through the *same* entry point (`[sys.executable, SELF, …]`) that pins a literal **non-64** outcome. For example, `--check <clean temp fixture>` → exit 0 plus a stable clean ID, or a mismatch fixture → exit 1 plus a stable mismatch ID. Pair that with a usage case whose token is distinct from the `USAGE` text.

Impacted axis: calibration (the C1 claim "standalone isolated exit+finding selftest"). Without the pairing, a 64 case is consistent with a gate that can never measure.

## Secondary counterexamples (these also defeat a single-case CLI usage test)

| ID | Mutant | Helper test | One subprocess `--bogus`→64 case | What discriminates |
|---|---|---|---|---|
| M2 | `argparse` with the default `error()`, so usage exits **2** | passes if it tests a `classify`/wrapper returning 64 | fails: exit 2 (literal 64 catches it) | the literal 64 subprocess case; required |
| M3 | Operand validation during parsing (e.g. `argparse.FileType`, or `open()` inside the parser raising `UsageError`): `--check /tmp/X/missing.json` → **64** instead of 2 `missing_input` | passes | **passes** (it only tests an unknown flag) | the pair `--check` (no operand) → 64 `usage_error` and `--check <absent temp path>` → 2 with the existing `missing_input` kind |
| M4 | Usage check after side effects (e.g. `base_receipt()`, a live read, or the receipt write happens before the extra argv is rejected) | passes (it cannot observe files) | passes on exit | assert no receipt or out-file in the temp root and no `CONTEXT:` verdict line on stdout |
| M5 | `-h` printing `USAGE`, or any path that dumps `USAGE`, satisfies a substring finding check, because `USAGE` contains `usage` and `exit 64 usage` | passes | passes | the token must not occur in `USAGE` (e.g. `finding=usage_error`), checked by exact line match |
| M6 | A new capture path propagates a child exit (`return baseline_run["exit"]`) | passes | passes | only relevant if implemented. The child `pin-disposition.py` uses 2 for usage, so propagation corrupts 1 and 2, not 64 directly. Keep the historical "child nonzero → `probe_baseline_unusable`/2" mapping |

## Hermeticity trap, specific to promoting the historical script

If the new tool keeps "no arguments means live capture" and its selftest copies the disposition gate's `usage-no-arguments` case, that case would run live `pin-disposition.py` against sibling trees, run live git, and write `.ufo/evidence/round-15/context-receipt.json`. Running with `cwd=scratch` does not isolate it, because `LANE_ROOT` comes from `__file__`, not from cwd. That breaks the integration interface ("no live reads/network/writes outside temp roots") and PROTOCOL's "no live-tree write". The exit check fails, but only after the side effects have happened.

Copying the historical `dirname×4` unchanged into `tools/context-capture.py` gives `LANE_ROOT=/home/vgpnk/Projects`. Every live capture then becomes exit 2 `missing_input`, and the receipt is written to `/home/vgpnk/Projects/.ufo/evidence/round-15/context-receipt.json`, outside the lane, because `main` writes receipts on `InvalidContext` too. I sent this to `agent://TameshiR15` as implementation-critical, since a check-mode selftest would not exercise it.

## Required routed fix vs optional hardening

### Required: routed defect 5 and PROTOCOL §Gate standard

1. **R1. Registry, both rows.** These go in the `SKILL.md` active registry.
   - Context gate row: `gate` (not `probe`), and its verdict map declares `64 usage → could-not-evaluate`.
   - Disposition gate row: `64 usage` becomes `64 usage → could-not-evaluate`.

   This is text only. Disposition 64 behaviour is unchanged and already backed by the retained `usage-no-arguments`/`usage-selftest-extra` exit-64 PASS lines.
2. **R2. A usage case through the real CLI.** The context gate's `--selftest` runs at least one `subprocess.run([sys.executable, SELF, <bad argv>], cwd=<temp>)` that asserts a **literal `== 64`**. An in-process `main([...])` does not count, per PROTOCOL `:389`.
3. **R3. A discriminating pair through the same entry.** The same selftest has at least one subprocess case with a literal non-64 exit (0 or 1) and a stable ID. This defeats M1. The integration interface already plans clean/mismatch fixtures; the requirement is that they go through `[sys.executable, SELF, …]`, not an import.
4. **R4. No side effects on usage.** No case invokes no-argument or live-capture argv unless that argv deterministically exits 64 before any I/O. The usage case asserts that no file appeared in its temp root.

### Required only if C1 or the registry claims a stable 64 finding

5. **R5. A distinct finding token.** The claim text "explicit class and stable finding" for 64 needs a CLI-emitted token not contained in `USAGE`. Example: one stderr line `CONTEXT: USAGE (finding=usage_error exit=64)`, asserted by exact match. Neither historical tool has such a token, so `usage_error` would be **new vocabulary**. Do not present it as an existing historical token, and do not retro-attribute it to the round-14 disposition gate. If no token is added, the claim must say "64 asserted by exit only; gate finding IDs asserted on 0/1/2 cases". PROTOCOL requires *a* stable finding ID per self-test, and round-14 closure `:162` says "not every emitted finding ID needs a separate fixture".

### Optional hardening (status-neutral; do not route as a defect if absent)

- **H1.** Add the M3 pair (`--check` with no operand → 64; `--check <absent temp path>` → 2 `missing_input`). Outer classes are equal (both could-not-evaluate), so swapping them is not a protocol violation. It does prove the two declared codes mean different things.
- **H2.** `--selftest` combined with another argument → 64, mirroring the disposition gate.
- **H3.** Make no-argument → 64 and give capture an explicit mode flag. This removes the hermeticity trap, at the cost of changing the historical no-argument entry command. Record the new entry command in the registry.
- **H4.** `-h`/`--help` exits 0 with no measurement. Fleet-wide 0 means clean, so a help invocation reads as clean. This is conventional, and the registry entry command is fixed, so disclose it rather than change it.
- **H5.** Keep child exit codes out of the gate's own exit map (M6).

## Claims to reject at closure

- "64 path tested", when the only evidence is an in-process `main()` call or a helper (M1).
- "Stable 64 finding", when the assertion is a substring of `USAGE` (`usage`, `64`) (M5).
- "Round-14 disposition gate had a stable usage finding". Its retained selftest asserts exit only.
- Any 64 behaviour for the context harness described as *observed historically*. No retained 64 run exists. The source mapping `:605-613` is the only basis, and it is a source reading, not an execution.

No scalar or axis movement beyond C1 calibration (6→6) is supported by these points.
