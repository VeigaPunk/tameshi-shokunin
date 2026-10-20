# S05 — run the retained invocation-context gate at the tip

Seat: `TameshiR17.S05RunContext` (scout, leaf; no delegation, no background jobs).
Round: 17 (hyaku phase 2), wave 1. Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Lane HEAD at both runs: `98bea7da5801f4bc58e4187690ee1687c8a5061f` (branch `master`).
Live-run timestamp: `2026-10-20T12:22:56-03:00`. Tool under test:
`tools/context-capture.py` sha256 `c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726`
at HEAD and live tree (identical), unchanged by any commit since the r16 baseline
`28aeef4` (`git log 28aeef4..HEAD -- tools/context-capture.py` → empty).

Registry source for the registered outcome: SKILL.md `### Round-15 gate/probe registry`,
line 1680 (`retained invocation-context gate | gate`), plus the discriminating-pin
sentence at SKILL.md:1650-1656.

## 1. Registered commands — outcome table

Every command was executed from the lane root (`cwd` = lane root), twice (first pass and
a repeat 12:22:56), and once in a clean clone; all three executions agreed.

| # | Command (as registered) | Registered outcome | Observed (both live runs) | Held? |
|---|---|---|---|---|
| C1 | `python3 tools/context-capture.py --check` | 0 clean, `context_consistent` (frozen round-14 receipt, built-in pin) | exit 0; `CONTEXT: OK (id=context_consistent receipt=.ufo/evidence/round-14/context-receipt.json sha256=05cb55b8…9c1a exit=0 findings=0)` | **held** |
| C2 | `python3 tools/context-capture.py --check --receipt .ufo/evidence/round-14/context-missing-env.json --expected .ufo/evidence/round-15/frozen/context-missing-env/expected.json` | negative retained fixture with a committed pin naming `missing_injected_environment`/exit1 must fail at exit 1 (SKILL.md:1650-1656; verdict map "1 failed stable finding ID") | exit 1; `CONTEXT: MISMATCH (id=missing_injected_environment … exit=1 findings=2)`; findings `missing_injected_environment` (injected_env absent) and `receipt_verdict_mismatch` | **held** |
| C3 | `python3 tools/context-capture.py --selftest` | self-test green, all literal cases pass (pinned values: "literal isolated selftest expectations in tool") | exit 0; 49 `SELFTEST_CASE … OK` lines; `SELFTEST: PASS (49/49)`; hermetic cases `hermetic-no-lane-path OK`, `hermetic-temp-only OK` | **held** |

Pin binding actually exercised by C1/C2 (observed, not assumed):

- C1: live receipt sha256 `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` =
  SKILL.md:1680 built-in pin and `FROZEN_RECEIPT_SHA256` (`tools/context-capture.py:153-155`).
- C2: committed expected pin `.ufo/evidence/round-15/frozen/context-missing-env/expected.json`
  (`git cat-file -e HEAD:<path>` → present) has schema `tameshi-context-expected-v1`,
  `receipt_sha256=1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208`,
  `id=missing_injected_environment`, `exit=1`. The live negative receipt and the frozen
  copy share that sha (`sha256sum` of both → `1ee9d09b…a208`).

## 2. Committed-bytes replication (branch tip, not just live tree)

Because the live tree carried untracked round-17 directories during the wave, the same
three commands were re-run in a clean clone at the tip using the contract's fleet-mirror
layout:

```
W=$(mktemp -d /tmp/tameshi-r17w1-S05RunContext-XXXXXX); mkdir $W/fleet
for s in /home/vgpnk/Projects/shokunin/*-shokunin; do [ "$s" = …/tameshi-shokunin ] || ln -s "$s" $W/fleet/; done
git clone -q …/tameshi-shokunin $W/fleet/tameshi-shokunin
git -C $W/fleet/tameshi-shokunin checkout -q 98bea7da5801f4bc58e4187690ee1687c8a5061f
```

Clone state: `rev=98bea7da5801f4bc58e4187690ee1687c8a5061f`, `git status --porcelain` empty
before and after the runs. Observed: C1 exit 0 `context_consistent`; C2 exit 1
`missing_injected_environment` (same two findings); C3 exit 0 `SELFTEST: PASS (49/49)`
(49 `OK` case lines). **3/3 held on committed bytes.**

Why this is a true committed-bytes run, not a live-tree read: frozen mode resolves the
receipt under `DEFAULT_LANE_ROOT = dirname(dirname(realpath(__file__)))`
(`tools/context-capture.py:137-138`, used at `:1342-1344`), so the clone's own copy is the
one read; explicit mode reads the `--receipt`/`--expected` paths relative to the caller's
cwd, which was the clone root.

## 3. Auxiliary probes (NOT registered rows; verdict-map classes only)

Run in scratch `/tmp/tameshi-r17w1-S05RunContext-Jj71mM` to confirm the registry's exit
classes are live on retained fixtures rather than selftest-only claims. These do not
alter the table above.

| Probe | Command shape | Observed | Registry class it exercises |
|---|---|---|---|
| A | negative receipt + `/tmp` pin claiming `context_consistent`/0 | exit 1, extra finding `expected_verdict_mismatch` ("expected id=context_consistent exit=0 but recomputed id=missing_injected_environment exit=1") | pinned-verdict precedence (clean→1) |
| B | byte-appended copy of the negative receipt + original pin | exit 2, `snapshot_tampered` (sha `13e5828b…` ≠ pinned `1ee9d09b…`) | 2 tampered input |
| C | no arguments | exit 64, `CONTEXT: USAGE_ERROR (id=usage_error exit=64)` | 64 `usage_error` |
| D | `--expected /dev/null` | exit 2, `expected_unreadable` ("expected file is not a regular file") | 2 malformed/unusable expected |
| E | `--receipt <missing path>` | exit 2, `receipt_missing` | 2 missing receipt |

## 4. Side effects and lane hygiene

- Check/frozen/selftest paths are read-only: `run_check` (`tools/context-capture.py:1341-1394`)
  only calls `read_regular`; the write-mode opens at `:1667`, `:1682`, `:1685` are inside
  `SelftestHarness.check_case` fixture construction under `mkdtemp`. Observed corroboration:
  the clone's `git status` was clean after all three commands.
- No lane file was written by this seat. Only this report is mine.
- Tracked modifications appeared in the live tree **during** the wave window — `.gitignore`
  (+`.ufo/state/`, `+.ufo/watchdog.log`) and `.ufo/evidence/round-16/round-gate/runner-sha256.txt`
  (+4-line R16-EV1 correction), both mtime `2026-10-20 12:21:34 -0300`; untracked
  `.ufo/evidence/round-15/attempt-4/` and `verification-4.json` also appeared. None are
  mine, none are read by this gate, and both runs before/after them agreed. Flagged only
  so the integrator does not attribute them here.
- Tool installs/upgrades: none (no pacman, no uv, no downloads). Stdlib `python3`/`git` only.

## 5. What this does and does not establish (C2 scope)

- Establishes: the round-15 registry's entry commands for the retained invocation-context
  gate return their registered exit/id at the round-17 branch tip, on live and committed
  bytes, repeat-stable, with the discriminating negative pin failing as registered. This is
  the row-1 slice of C2's "registered entry commands return their registered outcome at the
  branch tip".
- Does not establish: the disposition gate row (SKILL.md:1681), the new `tools/registry.json`
  monitor, or any sibling gate — out of this seat's target and not executed. A green check
  here is a retained-replay capability result, not an outside admission or proof the
  historical probe was re-executed (tool's own bounded-scope text, `tools/context-capture.py:105-112`).
- Residual risk [INFERENCE]: frozen `--check` reads the live lane copy of
  `.ufo/evidence/round-14/context-receipt.json`; if a future commit edits it the gate turns
  exit 2 `snapshot_tampered` rather than silently passing — demonstrated by probe B. The
  gate is input-keyed by construction (digest pin compared against the same bytes parsed,
  `tools/context-capture.py:1349-1375`).

## 6. Remaining unknowns

- None blocking this item. Registered-outcome wording for C3 comes from the registry's
  "Self-test command" cell plus "literal isolated selftest expectations in tool"; the table
  does not print a separate verdict-map entry for selftest, so "green" is the tool's own
  declared expectation (exit 0, all cases pass), observed exactly.

**Verdict: holds — 3/3 registered `tools/context-capture.py` commands returned their
registered outcome at `98bea7d` (live lane and clean clone, two live runs), exit/id exact,
no writes.**
