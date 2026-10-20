# ToolsNoHarm — wave-2 no-harm monitor (operability)

**Verdict: holds.** All nine lane-tool selftests at commit `c699c8c36d6e4eca4b796b81a8247904aa145ec8` pass with exit 0 when executed from a pristine `/tmp` snapshot of the commit bytes.

## Method

Snapshot taken via `git archive` (no `git worktree`, no `.git` state mutation on the lane repo):

```
mkdir -p /tmp/tameshi-r16w2-ToolsNoHarm-3092
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin archive c699c8c36d6e4eca4b796b81a8247904aa145ec8 | tar -x -C /tmp/tameshi-r16w2-ToolsNoHarm-3092
```

Each tool invoked with `python3` from cwd `/tmp/tameshi-r16w2-ToolsNoHarm-3092`. Exits captured via `echo "EXIT=$?"`.

## Results

| # | Command | Exit | Summary line |
|---|---------|------|--------------|
| 1 | `python3 tools/repeat-control.py --selftest` | 0 | `SELFTEST: PASS (29 cases)` |
| 2 | `python3 tools/pin-disposition.py --selftest` | 0 | `SELFTEST: PASS (18/18)` |
| 3 | `python3 tools/witness-metadata.py --selftest` | 0 | `SELFTEST: PASS 39/39` |
| 4 | `python3 tools/evidence-disposition.py --selftest` | 0 | `SELFTEST: PASS (34/34)` |
| 5 | `python3 tools/context-capture.py --selftest` | 0 | `SELFTEST: PASS (49/49)` |
| 6 | `python3 tools/bash-witness-study.py selftest` | 0 | `WITNESS_SELFTEST: 41/41 pass` / `VERDICT: PASS` |
| 7 | `python3 .ufo/evidence/round-16/measure.py --selftest` | 0 | `MEASURE_SELFTEST: 33/33 pass (scratch /tmp/tameshi-r16-CRMeasure-5q6dgppk)` |
| 8 | `python3 .ufo/evidence/round-16/coldread/assemble.py --selftest` | 0 | `SELFTEST: all checks passed` |
| 9 | `python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest` | 0 | `SELFTEST: PASS (new rule 4/4; old rule fails 3/4; same fixtures and oracles)` |

Aggregate: 9/9 selftests pass; zero non-zero exits; every per-case line reported PASS/ok.

## Key observations

- `repeat-control.py`: 29 cases all PASS, including tamper-detection family (`snapshot-tamper-byte`, `snapshot-tamper-manifest-symlink`, etc.) → `snapshot_tampered/2`.
- `pin-disposition.py`: 18/18; green cases exit 0, malformed/duplicate/missing-manifest cases exit 2 as expected.
- `witness-metadata.py`: 39/39; green `metadata_consistent/ok/0`, red classes exit 1, tamper/input classes exit 2.
- `evidence-disposition.py`: 34/34, incl. `argv-never-executed` and `usage-no-arguments exit=64`.
- `context-capture.py`: 49/49, incl. hermetic checks (`hermetic-no-lane-path`, `hermetic-temp-only`) and usage-error family exit 64.
- `bash-witness-study.py selftest`: 41/41; verdict-line text is `VERDICT: PASS`.
- `measure.py`: 33/33; negative-path cases (`exit2-blob-missing`, `exit64-no-rev`, `exit2-no-repo`) all PASS. Selftest leaves scratch at `/tmp/tameshi-r16-CRMeasure-*` (reported in its own summary line).
- `assemble.py`: all `[ok]` checks pass; expected-rejection diagnostics (`REJECTED`, `SKIPPED`, `WARNING`, `ERROR` lines) are selftest-authored fixtures, not failures.
- `reattribute.py`: reads fixture `…/round-15/verification-3.json` from the worktree (present in the commit snapshot); prints its sha256 `3c419055…d8ce` and confirms the new rule passes 4/4 where the old rule fails 3/4 on identical fixtures/oracles.

## Files changed

- `.ufo/waves/round-16/w2/ToolsNoHarm.md` (this report) — the only lane write.

## Environment / tooling

- `python3` on PATH used for all invocations; no installs needed; no tools installed or updated.

## Risks / blockers

None. Snapshot method did not touch lane `.git`; scratch confined to `/tmp/tameshi-r16w2-ToolsNoHarm-3092` (plus the measure.py selftest's own `/tmp/tameshi-r16-CRMeasure-*` scratch).
