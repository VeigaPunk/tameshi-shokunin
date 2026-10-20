# V02 — R16 ToolsNoHarm monitor: exactly what it ran, and what a registered-entry-command run would have caught

**Verdict: partial (reconstruction holds; the monitor's "holds" was a selftest-only verdict, not an operability verdict).**
The R16 monitor executed **nine selftest commands and nothing else**. At the same rev (`c699c8c`) a registered-entry-command run over the lane's own gate/probe registries yields **held = 10/11**, exit 1: the row `effective expectation disposition` declares `0 clean` and returned `2 expected_input_digest_mismatch`. That is the operability harm the round's non-author spot-check later routed as R16-OP1/R16-MON1.

## 1. What the seat ran — reconstructed, not inferred

Sources: the dispatch payload, the seat transcript, the landed report, and a reproduction of every command.

- Dispatch (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-16/dispatch2.json`, `taskCall.tasks[58]`): the Target is one sentence — "No-harm monitor for operability: from a /tmp worktree of `c699c8c…`, run every lane tool selftest:" followed by a nine-item `--selftest` / `selftest` list. It names no `--root`, `--check`, `--manifest`, `--rev`, `--runs`, `--snapshot`, `--regression` or `count` form. Acceptance asks only for "each exit and summary line".
- Transcript `history://TameshiR16.ToolsNoHarm`: one `bash` call that creates `/tmp/tameshi-r16w2-ToolsNoHarm-3092` and extracts `git archive c699c8c`; then nine parallel `bash` calls, each exactly one selftest with `echo "EXIT=$?"`; then one `write` of the report; then the final message. No other tool call, and no entry command anywhere in the transcript.
- Landed report `.ufo/waves/round-16/w2/ToolsNoHarm.md`: verdict line `:3` ("All nine lane-tool selftests … pass"); method `:7-13` (`git archive`, no `.git`); results table `:18-28`; aggregate `:30`; "Files changed" `:44-46` (report only).
- Timing: `c699c8c` committed 10:49:37; `ToolsNoHarm.md` written 10:52:31. The monitor measured the very commit that introduced the drift below.

Reproduction from a fleet-mirror clone at the same rev (`git clone` + `git checkout c699c8c`, siblings symlinked beside it), all nine commands, all exit 0, summary lines identical to the report:

| # | Command (cwd = clone root) | Exit | Summary line |
|---|---|---|---|
| 1 | `python3 tools/repeat-control.py --selftest` | 0 | `SELFTEST: PASS (29 cases)` |
| 2 | `python3 tools/pin-disposition.py --selftest` | 0 | `SELFTEST: PASS (18/18)` |
| 3 | `python3 tools/witness-metadata.py --selftest` | 0 | `SELFTEST: PASS 39/39` |
| 4 | `python3 tools/evidence-disposition.py --selftest` | 0 | `SELFTEST: PASS (34/34)` |
| 5 | `python3 tools/context-capture.py --selftest` | 0 | `SELFTEST: PASS (49/49)` |
| 6 | `python3 tools/bash-witness-study.py selftest` | 0 | `WITNESS_SELFTEST: 41/41 pass` / `VERDICT: PASS` |
| 7 | `python3 .ufo/evidence/round-16/measure.py --selftest` | 0 | `MEASURE_SELFTEST: 33/33 pass` |
| 8 | `python3 .ufo/evidence/round-16/coldread/assemble.py --selftest` | 0 | `SELFTEST: all checks passed` |
| 9 | `python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest` | 0 | `SELFTEST: PASS (new rule 4/4; old rule fails 3/4; …)` |

So the report is truthful about what it ran; the defect is the scope, and the scope was written by the dispatch.

## 2. The registered entry commands at the same rev — expected vs observed

Rows are the lane's own registries at `c699c8c` (`git show c699c8c:SKILL.md`): round-12 `:1499-1504`, round-13 `:1548-1553`, round-15 `:1676-1681`, round-16 `:1789-1796`. The round-14 table `:1597-1602` is marked historical/superseded; its archived `capture-context.py` row is "not active" and correctly excluded. Accounting: the mutate-and-run row's two mandatory commands (`--selftest` · `--regression`) split into two rows; the repeat-control row's two alternative forms (`--runs` *or* `--snapshot`) stay one row, evaluated in its pinned `--snapshot` form. All run from the clone at `c699c8c`, cwd = clone root.

| Row (registry anchor at c699c8c) | Entry command | Registered outcome | Observed | Result |
|---|---|---|---|---|
| repeated pristine controls `:1503` | `python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate` | 0 clean | 0 `controls_match` | held |
| bash declared-witness study `:1504` | `python3 tools/bash-witness-study.py count` | 0 complete sample | 0 `witness_classified=10` | held |
| six-leg content disposition `:1552` | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` | 0 observations | 0 `status=ok`, 6 legs (3 changed/3 unchanged) | held |
| exposed witness provenance companion `:1553` | `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` | 0 `metadata_consistent` | 0 `metadata_consistent reason=ok` | held |
| retained invocation-context gate `:1680` | `python3 tools/context-capture.py --check` | 0 `context_consistent` | 0 `CONTEXT: OK … findings=0` | held |
| **effective expectation disposition `:1681`** | **`python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json`** | **0 clean** | **2 `expected_input_digest_mismatch`** | **DIFFERS** |
| `tools/mutate-and-run.sh` selftest `:1793` | `bash tools/mutate-and-run.sh --selftest` | 0 pass | 0 `MUTATE_SELFTEST: 81/81 pass` | held |
| `tools/mutate-and-run.sh` regression `:1793` | `bash tools/mutate-and-run.sh --regression` | 0 PASS | 0 `REGRESSION: PASS (cases=7 passed=7 …)`, 123.7 s | held |
| `measure.py` `:1794` | `python3 .ufo/evidence/round-16/measure.py --rev c699c8c` | 0 measured | 0 measured (mid-wave: `ledger_present=false`, restraint 6) | held |
| `coldread/assemble.py` `:1795` | `python3 .ufo/evidence/round-16/coldread/assemble.py --selftest` | 0 all checks pass | 0 `SELFTEST: all checks passed` | held |
| `attribution/reattribute.py` `:1796` | `python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest` | 0 rule passes oracle | 0 | held |

The repeat-control **run form** (`--runs 3 --out DIR -- printf 'stable-out\n'`, DIR not pre-created — a pre-created `--out` is refused exit 64 by design) was also executed and held: exit 0, `controls_match`, `identical=yes runs=3`.

**held = 10/11; differs = 1/11.**

The failing row's full finding (c699c8c, `--root .`):

```
status=could_not_evaluate  id=expected_input_digest_mismatch  exit=2
tools/mutate-and-run.sh: observed 89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594
                         expects  75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5
```

Root-cause chain, all committed evidence:
1. `.ufo/evidence/round-13/expected.json:12` (frozen round-13 evidence) pins `tools/mutate-and-run.sh` at `75ed934d…adc5`.
2. `c699c8c` — the rev the monitor measured — edited that tool (`git diff 7650fe4..c699c8c --stat -- tools/mutate-and-run.sh`: `+108/−24`, adding leg 7), producing `89722ddb…5594`. `git show c699c8c:tools/mutate-and-run.sh | sha256sum` confirms it.
3. `tools/evidence-disposition.py:1182-1192` verifies **every** `expected.inputs` digest before any predicate runs, so the run cannot reach a disposition verdict at all.
4. `05a2247` moved the tool again (`0673d2e5…`); the registered command still exits 2 at the lane tip `98bea7d` (`observed 0673d2e5… expects 75ed934d…`) — the R16-OP1 repair has not landed at this dispatch tip.

The round-14 recipe step 2 (`SKILL.md:1581-1583`) also regressed, and this report executed it (the R16 spot-check marked it `[INFERENCE]`):

| Root | `dispositions.json` (step 3) | `dispositions-before.json` (step 2) |
|---|---|---|
| `e69b488` (pre-landing) | exit 0 `clean`, `passed=11 failed=0` | exit 1 `failed`, `expected_contains_missing` |
| `c699c8c` (measured rev) | exit **2** `expected_input_digest_mismatch` | exit **2**, same finding |
| `28aeef4` (`git archive` → /tmp, documented workaround) | exit 0 `clean` | exit 1 `failed` |

So the two commands that the recipe depends on to discriminate "supersession effective" (0) from "producer_before unresolved" (1) both collapse to the same could-not-evaluate class (2) on the tree the lane actually ships — and the only green path grades a frozen commit.

## 3. The monitor rule that would have failed

**MON-1 — registered-outcome conformance per registry row at the measured rev.**

> For every active gate/probe registry row of the lane at rev `REV`, execute the row's exact entry argv once from a checkout of `REV` (cwd = lane root, own pinned inputs, no shell), and require the observed exit to **equal the row's registered clean outcome** (`expect.exit`). Report one line per row (`ROW <name> expect=<exit> got=<exit> held|differs`) and a summary `REGISTRY_CHECK: held=N/M`; exit 1 if any row differs, 2 if the rev/registry cannot be evaluated.

At `c699c8c` this rule emits, among ten `held` lines:

```
ROW effective-expectation-disposition expect=0 got=2 differs    # expected_input_digest_mismatch: tools/mutate-and-run.sh 89722ddb… vs 75ed934d…
REGISTRY_CHECK: held=10/11                                       # exit 1
```

and the monitor's overall verdict could not have been "holds". Two weaker rules are *not* sufficient and are worth naming so they are not adopted:
- **"exit is inside the published verdict map"** — the row's own map lists `2 … could-not-evaluate`, so a `2` passes. The row must carry one registered outcome, because a gate that can never be clean has stopped being the capability it registers.
- **"selftest is green"** — the selftest of this gate is 34/34 at the same rev (§4). A selftest proves the instrument's branches, never the lane's pinned inputs.

This is exactly the semantics interface B gives `tools/registry-check.py` (`rows[].expect.exit`, `--rev` clone, `REGISTRY_CHECK: held=N/M`). The reconstruction supplies the missing numbers for the R16 rev: 11 command-rows, one differs.

## 4. Why the nine selftests structurally could not see it

The disposition tool's selftest is hermetic by construction: `tools/evidence-disposition.py:1512` creates `/tmp/tameshi-r14-evidence-disposition-selftest.*` and every case runs against a synthetic lane; the drift case at `:1753` (`expected-input-digest-mismatch`) deliberately mutates a **fixture** file and asserts exit 2. The real-pin check (`:1182-1192`) is only reachable in normal mode against `--root`. The same shape holds for the other eight instruments: their selftests use temp fixtures or frozen receipts; none hashes the lane's committed pin set against the live instruments. Selftest green and live-gate red are therefore consistent, not contradictory.

## 5. Method / caveats

- All runs used a fleet-mirror clone (`git clone` of the lane at `c699c8c`, sibling repos symlinked beside it) so `FLEET_ROOT`-derived and absolute-root entry commands both worked; scratch confined to `/tmp/tameshi-r17w1-V02ToolsNoHarmScope-*`.
- The monitor's `git archive` snapshot is adequate for the nine selftests but not for the entry set: `.ufo/evidence/round-16/measure.py` hard-codes `DEFAULT_REPO` to the live lane (`measure.py:53`), so from an archive it silently measures the live lane unless `--repo .` is passed — and `--repo .` exits 2 `rev-missing` because the archive has no `.git` (verified). An entry-command monitor needs a rev checkout/clone, which is what interface B's `--rev` mode provides.
- The `measure --rev c699c8c` row is `held` on exit, but its output at that rev is `ledger_present=false` (the R16 ledger landed later, at `3490708`); the row registers only exit 0, so no ledger expectation is implied.
- Only lane write: this report. Lane `git status --porcelain` before the write showed only the L1's pre-existing round-17 state (`M .gitignore`, `M runner-sha256.txt`, untracked round-17/round-15 evidence); nothing of mine.
- No tools installed or updated.

## 6. Cross-checks against committed reports

- `corpus/lessons/round-16-verifier-spotcheck.md` §3 already states the operability harm and "The ToolsNoHarm monitor ran selftests only, so it could not see this"; §6 item 6 (R16-MON1) asks for the registered entry commands. This report reproduces both with executed commands and quantifies the run: 10/11.
- `RR10` (`.ufo/waves/round-16/w2/RR10.md:6-9`, written 10:57:25, five minutes after the monitor) independently ran the same disposition row and recorded exit 2 `expected_input_digest_mismatch`; `RX5` repeats it at `05a2247`. The evidence existed inside the wave; the monitor's rule did not ask for it.
- `CR26` (`.ufo/waves/round-16/w1/CR26.md:27-28`) recorded step 3 = exit 0 at `e69b488`, before the runner moved — which is why the sha-only bucket credit stayed green (the R16-C2b hole, separate item).

**Verdict: partial — the monitor ran exactly the nine selftests the dispatch enumerated (all reproducible, all green), and a registered-entry-command run at the same rev would have failed on 1 of 11 rows (`evidence-disposition --root .`: 0 expected, 2 `expected_input_digest_mismatch`), i.e. `held=10/11`, exit 1; the rule that fails is registered-outcome conformance (`expect.exit`), not verdict-map membership and not selftest green.**
