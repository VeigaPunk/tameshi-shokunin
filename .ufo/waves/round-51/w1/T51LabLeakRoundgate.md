# T51LabLeakRoundgate — C2 sandbox-id leak audit of recorded leg `js-round-gate`

Seat: T51LabLeakRoundgate · round 51, wave 1 · lane `tameshi-shokunin` @ base `9962033fd7a75aa2f2847e979dd687a5d28505a1`
Item: audit the recorded leg `js-round-gate` for the same sandbox-id leak as C2 (drift-pins gate).
Hypothesis to falsify: **none of the recorded verdicts (TABLE_ROUNDGATE) depends on the defect id appearing in the sandbox path.**
Method: single-variable probe — identical suite, sandbox named `sandbox-<DEFECT_ID>` (recorded) vs `sandbox-n<ordinal>` (neutral).
Receipts: `.ufo/waves/round-51/w1/T51LabLeakRoundgate/` (22 run logs, `exits.tsv`, `driver.sh`, `defects.tsv`, `js-round-gate.spec`, `spec_helper.py`, `target-and-mutant-sha256.txt`).

## 1. Pinned target materialization (verified)

| item | value | source |
|---|---|---|
| REV_ROUNDGATE | `364f1d5954158ef8844bca4a5fef57b05d2f2ca5` | `tools/mutate-and-run.sh:618` |
| PIN_ROUNDGATE | `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9` | `tools/mutate-and-run.sh:617` |
| blob mode | `100755` | `git -C kumitate-shokunin ls-tree 364f1d5 scripts/round-gate.mjs` |
| materialized | `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs` → 1511 lines | — |
| sha256(materialized) | `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9` = PIN ✓ | `sha256sum` |
| chmod | `755` (per mode 100755) | — |

## 2. Embedded spec extraction, exact

The runner writes the spec via a quoted heredoc `cat >"$d/js-round-gate.spec" <<'EOT'` (`tools/mutate-and-run.sh:966-1024`); body extracted verbatim (lines 967–1023) → `js-round-gate.spec` (57 lines).
Parsed with the runner's own spec helper, extracted verbatim from the runner (`tools/mutate-and-run.sh:314-448`, `py_helper` PYEOF body lines 316–446) → `python3 spec_helper.py list js-round-gate.spec`:
10 defects, ids exactly the TABLE_ROUNDGATE keys (`tools/mutate-and-run.sh:629`), 5 kill-aimed (A1, A3, B1, E3, C1060), 5 hole-aimed (C1059, A2, B2, CKIND, E1).

Each mutant built by the helper's byte-exact single `@old→@new` replace (count==1 asserted before write):

```
APPLY OK id=A1 old-count=1 bytes-before=80415 bytes-after=80415   … (all 10: old-count=1)
```

## 3. Probe design

Suite string copied verbatim from the runner (`tools/mutate-and-run.sh:1418`), only the sandbox name changed:

- variant A (recorded): `h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" node "$MUTANT" --selftest`
- variant B (neutral, one variable): identical except `sandbox-$ORDINAL` (`sandbox-n0` for control, `sandbox-n1..n10` for defects in spec order).

Environment per run mirrors `run_one` (`tools/mutate-and-run.sh:452-460`): `MUTANT`, `WORKDIR`, `DEFECT_ID` (A) / `ORDINAL` (B), `timeout 300 bash -c "$SUITE"` with output to evidence file; exit recorded. Verdict map per the runner (`tools/mutate-and-run.sh:545-551`): 0 → SURVIVED, 124/126/127 → INCONCLUSIVE, else KILLED.
Runs: control + 10 mutants × 2 variants = 22; all completed, no timeout/inconclusive.
Sandbox dirs actually created: `sandbox-CONTROL`, `sandbox-A1…E3`, `sandbox-n0…n10` (22 dirs) — confirms both variants executed under their intended names.

## 4. Results: exit and verdict per artifact

| artifact | exit A (id sandbox) | exit B (neutral sandbox) | verdict A | verdict B | match TAB |
|---|---|---|---|---|---|
| pristine control | 0 | 0 | SURVIVED (control green) | SURVIVED | — |
| A1 | 1 | 1 | KILLED | KILLED | ✓ |
| A3 | 1 | 1 | KILLED | KILLED | ✓ |
| B1 | 1 | 1 | KILLED | KILLED | ✓ |
| E3 | 1 | 1 | KILLED | KILLED | ✓ |
| C1060 | 1 | 1 | KILLED | KILLED | ✓ |
| C1059 | 0 | 0 | SURVIVED | SURVIVED | ✓ |
| A2 | 0 | 0 | SURVIVED | SURVIVED | ✓ |
| B2 | 0 | 0 | SURVIVED | SURVIVED | ✓ |
| CKIND | 0 | 0 | SURVIVED | SURVIVED | ✓ |
| E1 | 0 | 0 | SURVIVED | SURVIVED | ✓ |

Selftest PASS/FAIL assertion counts identical per defect across variants
(A1 49/11, A3 57/3, B1 57/3, E3 58/2, C1060 58/2, C1059 60/0, A2 60/0, B2 60/0, CKIND 60/0, E1 60/0; control 60/0).

**No defect's verdict differs between the two sandbox namings.** The recorded table (5 KILLED / 5 SURVIVED) is reproduced exactly under both.

## 5. Why no dependence exists (mechanism)

- Verdict oracle for this leg is **exit status only** (`js-round-gate.spec` header, `tools/mutate-and-run.sh:969-970`; runner map at :545-551). There is no grep-over-output verdict step in the suite whose outcome a defect id inside a scratch path could satisfy — the C2 leak mechanism (unanchored `grep -q` over output that prints scratch paths) is absent here.
- The target's `--selftest` is a hermetic 60-assertion harness (`ROUND_GATE_SELFTEST: 60/60 pass` / `VERDICT: PASS`); its fixtures build their own `mkdtemp` scratch dirs under `$h/tmp`. The defect id appears in outputs only inside the sandbox path string (variant A), and not at all in variant B outputs (`grep -E 'sandbox-(A1|…)'` matches only `mut_A_*.out`).
- Normalized output diff (sandbox name anonymized): residual A-vs-B differences are only the random `mkdtemp` suffixes (e.g. `kumitate-round-gate-selftest-x5KCvP/` vs `…oE7uzj/`), matching the spec's own note that stdout is not byte-deterministic (mkdtemp names). Exit codes are nonetheless identical.

## 6. Verdict on hypothesis

Hypothesis **not falsified**: none of the recorded verdicts (TABLE_ROUNDGATE, `tools/mutate-and-run.sh:629`) depends on the defect id appearing in the sandbox path.
No defect has a differing verdict, therefore no "selftest assertion that matched the id" exists to list.

## Commands that show the findings

```
git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs | sha256sum   # f890e277… = PIN
python3 spec_helper.py list js-round-gate.spec                          # 10 defects, ids = TABLE_ROUNDGATE keys
python3 spec_helper.py apply js-round-gate.spec round-gate.mjs mutant-<id>.mjs <id>   # count==1 per defect
bash driver.sh                                                          # 22 runs; exits.tsv
diff <(sed -E 's#sandbox-(A1|A3|B1|E3|C1060|C1059|A2|B2|CKIND|E1)#sandbox-X#g' mut_A_<id>.out) \
    <(sed -E 's#sandbox-n[0-9]+#sandbox-X#g' mut_B_<id>.out)    # only mkdtemp suffixes differ
grep -lE 'sandbox-(A1|A3|B1|E3|C1060|C1059|A2|B2|CKIND|E1)' work/*.out   # only mut_A_* outputs carry the id
```

The derived per-defect comparison is `verdict-compare.tsv` in the receipts dir (exits A/B, verdicts, same=YES for all).

No tools installed/changed during this seat (none required; `node v24.21.0` used).

## Summary
- js-round-gate leg (`tools/mutate-and-run.sh:1416-1419`) audited for the C2-style sandbox-id leak; pinned target verified (sha256 `f890e277…` = PIN_ROUNDGATE, mode 100755).
- Embedded spec extracted verbatim and applied by the runner's own helper: 10 mutants, one exact `@old→@new` edit each (count==1).
- 22 runs (control + 10 mutants × 2 sandbox namings); exits identical between `sandbox-<DEFECT_ID>` and `sandbox-n<ordinal>` for every artifact.
- Recorded TABLE_ROUNDGATE (5 KILLED / 5 SURVIVED) reproduced exactly under both namings; PASS/FAIL counts identical per defect.
- Normalized outputs differ only in random mkdtemp suffixes, never in verdict-relevant content; the id appears in outputs only as a path string.
- Hypothesis survives: no recorded verdict depends on the defect id in the sandbox path; no differing verdict, so no matching assertion to report.
- Mechanism: verdict oracle is exit-status-only; the suite contains no grep-over-output step, unlike the C2 drift-pins gate.
- Lane untouched except this report and receipts (read-only audit; no edits to tools, SKILL.md, or other sections).
