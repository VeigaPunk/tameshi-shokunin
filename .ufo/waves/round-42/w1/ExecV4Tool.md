# ExecV4Tool findings

- Created and committed `/tmp/tameshi-r42-ExecV4Tool-clone/tools/write-path-census-v4.py` (commit `f4e9e52`, SHA-256 `eaf67995010c353302c596228e132e237455dea7fc2db30459257b88491cebbd`). The live lane was not edited.
- Counter command: `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-42/census/measure.py --lane /tmp/tameshi-r42-ExecV4Tool-clone --rev HEAD --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f`
- Exact output: `C2_R42: self_pin=1 tool_absent=0 tool_sha256=eaf67995010c353302c596228e132e237455dea7fc2db30459257b88491cebbd v3_sha_ok=1 v2_sha_ok=1 selftest_exit=0 fixtures_pass=3/10 run_errors=0 live_1682_ok=0 live_1685_ok=0 live_123_ok=0 live_unflagged_v3=3 live_unflagged_v4=24 live_tool_errors_v4=0 mutants_declared=0 mutants_killed=0 mutant_classes_killed= rev=f4e9e525d17134d13bb3232a97e2d529f9c65695 freeze=322b5cd32b4319a05340d249ae752d12a9e6b19f C2_R42_PASS=false` (exit 1).
- Counter also reported duplicate write-site records: F01–F06 and F10 as 2 expected sites, live context-capture lines 1682/1685 as 8 sites, registry-replay line 123 as 2. The v4 attempt is incomplete; required fixture/live target was not achieved. Selftest is only a minimal existence check, not the required ten-shape coverage.
- No checks beyond the specified counter were run. No tools installed or updated.
