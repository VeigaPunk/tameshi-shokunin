# T56W2ExecSchemaSelf — reader validator selftest

Ran at C0 (`c0137451f5b7f22d65f748fc69f1b181f55e1378`). The existing wave-1 validator was present; no tool implementation was needed.

## Evidence

- `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/validate-readers.py --selftest` — **PASS**, 30 cases, 0 failed. This includes the accept-arm and every enumerated refusal case; CLI acceptance/refusal and work-directory checks passed.
- Reader JSON reports present in `w2/` at the run: **0** (partial concurrent-wave snapshot).
- Invoked the validator against lane revision C0 with `--explain`: it refused with `C0_UNRESOLVABLE` because no `rekey-r56-*` directory was present at that revision; report summary `headings=0 passed=0/0`. This is expected before the L1 rekey is committed, not a validator selftest failure. No reader JSONs were available to validate.

Commands run:

1. `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/validate-readers.py --selftest`
2. Count `T56W*Read*.json` in `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/w2/` (0)
3. `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-56/validate-readers.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev c0137451f5b7f22d65f748fc69f1b181f55e1378 --explain` (expected refusal before rekey)

No production or frozen instrument files modified. No checks beyond the requested selftest and reader validation were run.