# Replica1499 — cold-read re-read: SKILL.md lines 1499-1516 (`### Gate/probe registry`)

Seat: TameshiR16.Replica1499 · wave 2 falsify · lane commit c699c8c36d6e4eca4b796b81a8247904aa145ec8
Page SHA-256 verified: `git show c699c8c3:SKILL.md | sha256sum` → `3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4` (matches pinned page sha; page 1795 lines).
Scratch: `/tmp/tameshi-r16w2-Replica1499-jQzoSz` (committed bytes exported via `git show`; nothing written outside scratch except this report).

**Verdict: HOLDS.** The registry is an accurate record: both instruments exist at the pinned revision, both named commands and self-tests run as documented, every pinned evidence file verifies, and the calibration correction is factually right. One minor literal mismatch (see gaps).

## Section class

Record (registry table + scope notes + calibration correction; the row cells document entry/self-test commands rather than instructing the reader). Per target, every named command was executed anyway.

## Executed commands

All runs from a /tmp mirror of the committed tree (`EVIDENCE_ROOT`/`REPO` resolve via `__file__`, so `.ufo/evidence/round-12/` and `tools/mutate-and-run.sh` were exported alongside the tools).

| Command | Exit | Key output |
|---|---|---|
| `python3 tools/repeat-control.py --selftest` | 0 | `SELFTEST: PASS (29 cases)` — all 29 `SELFTEST_CASE … PASS` |
| `python3 tools/repeat-control.py --runs 3 --out out-demo -- printf 'hello\n'` | 0 | `REPEAT_COMPARE identical=yes runs=3` / `REPEAT_CONTROL: controls_match`; wrote only `out-demo/` (command.txt, finding.txt, run-1..3.{stdout,stderr,exit}) |
| `python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate` | 0 | `SNAPSHOT_INPUTS 9 verified` / `controls_match` expected=observed |
| `python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate/mismatch` | 1 | `SNAPSHOT_INPUTS 9 verified` / `controls_mismatch` expected=observed |
| `python3 tools/bash-witness-study.py selftest` | 0 | `WITNESS_SELFTEST: 41/41 pass` / `VERDICT: PASS` |
| `python3 tools/bash-witness-study.py count` | 0 | `counts killed_on_witness=8 accidental=0 survived=2 inconclusive=0 total=10`; `unresolved none`; declared.tsv sha `0def0d3b…` reported |

Verdict maps confirmed in-code: `EXIT_BY_ID` at repeat-control.py:122-130 (controls_match 0 / controls_mismatch 1 / baseline_nonzero,command_unavailable,snapshot_tampered,setup_error 2 / invalid_usage 64); `EXIT_OK, EXIT_FAIL, EXIT_CANNOT, EXIT_USAGE = 0, 1, 2, 64` at bash-witness-study.py:118. Matches both rows' verdict-map cells (the gate cell's "2 could-not-evaluate" is the family union — accurate, if coarse).

## Re-checked anchors (record claims)

- `.ufo/evidence/round-12/ControlGate/expected.json` — exists; `expected_id controls_match / expected_exit 0`; all 9 `inputs` sha256s recompute over the run-* files (True).
- `.ufo/evidence/round-12/ControlGate/mismatch/expected.json` — `controls_mismatch / 1`; all 9 inputs verify; the only differing hash vs stable is `run-3.stdout` — a genuine single-run divergence.
- `.ufo/evidence/round-12/BashWitness/{declaration.json,declared.tsv,manifest.json}` — exist; `sha256sum declared.tsv` = `0def0d3b…41d3` matches `declaration.json.declared.sha256`; `count` verified the same linkage and frozen row set.
- "integrity-frozen, not blind" — `declaration.json.kind` = "declared-witness mapping (not a blind preregistration)"; its `disclosure` enumerates the prior source/spec/outcome exposure. Consistent with the registry prose.
- Write-scope cells — `cmd_count` (bash-witness-study.py:1041) is read-only over the evidence dir; `--runs --out` writes only the caller DIR; `--snapshot` writes nothing. `run`/`rerun` write under the own evidence dir, `sweep/`/`rerun-*`, as claimed.
- `SHONEN.md` box 3 (third checklist box, "Instructions executable by an agent without oral context") carries `[~]`, not `[ ]` — confirmed.
- `corpus/lessons/round-1-verifier-spotcheck.md` — Adjudication states "the box-3 increment is not credited (cold-read covered Appendix A+B only…)" — confirmed; consistent with the registry's "excludes it from the score" and "does not extend the earlier Appendix A/B cold-read".

## Gaps

- Minor (literal): bash-study row's Write-scope cell claims selftest scratch under "isolated `/tmp/tameshi-r12-*`", but `bash-witness-study.py:1230` uses `tempfile.mkdtemp(prefix="bash-witness-selftest.")`. The isolated-/tmp property holds; the literal glob does not. (`repeat-control` selftest does use `/tmp/tameshi-r12-repeat-control-selftest.*`, matching its own cell.)
- Not a gap, recorded for honesty: first `selftest` run in a partial copy failed `FileNotFoundError: tools/mutate-and-run.sh`; the file exists at revision (`tools/` blob 021f4918) and `RUNNER = REPO/"tools"/"mutate-and-run.sh"` (bash-witness-study.py:95) requires it for digest pinning. With it mirrored, selftest passes 41/41.

No installs performed; stdlib `python3` and `bash` sufficed.

```json
{"seat":"Replica1499","skill_sha256":"3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4","sections":[{"start":1499,"heading":"### Gate/probe registry","class":"record","verdict":"gap-minor","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["bash-witness-study Write-scope cell claims isolated /tmp/tameshi-r12-* but bash-witness-study.py:1230 uses mkdtemp prefix 'bash-witness-selftest.' (isolated /tmp property holds; literal glob does not)"],"commands_executed":["git show c699c8c36d6e4eca4b796b81a8247904aa145ec8:SKILL.md | sha256sum","git show c699c8c36d6e4eca4b796b81a8247904aa145ec8:SKILL.md | sed -n '1499,1516p'","git ls-tree -r --name-only c699c8c36d6e4eca4b796b81a8247904aa145ec8","python3 tools/repeat-control.py --selftest (exit 0, 29/29 PASS)","python3 tools/repeat-control.py --runs 3 --out DIR -- printf 'hello\\n' (exit 0, controls_match)","python3 tools/repeat-control.py --snapshot ControlGate (exit 0) and --snapshot ControlGate/mismatch (exit 1)","python3 tools/bash-witness-study.py selftest (exit 0, 41/41 PASS)","python3 tools/bash-witness-study.py count (exit 0, killed_on_witness=8 survived=2 unresolved none)","sha256sum declared.tsv + expected.json input-hash recomputation (all verify)"],"opened":["tools/repeat-control.py","tools/bash-witness-study.py","tools/mutate-and-run.sh",".ufo/evidence/round-12/ControlGate/expected.json",".ufo/evidence/round-12/ControlGate/mismatch/expected.json",".ufo/evidence/round-12/BashWitness/declaration.json",".ufo/evidence/round-12/BashWitness/declared.tsv",".ufo/evidence/round-12/BashWitness/manifest.json","SHONEN.md","corpus/lessons/round-1-verifier-spotcheck.md"],"scratch":"/tmp/tameshi-r16w2-Replica1499-jQzoSz"}]}
```
