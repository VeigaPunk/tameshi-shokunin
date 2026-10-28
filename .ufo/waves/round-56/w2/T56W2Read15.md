# T56W2Read15 — cold-read report

Heading: `### Round-21 gate/probe registry — finite environment differential`

Candidate: `c0137451f5b7f22d65f748fc69f1b181f55e1378`

Section range at C0 (frozen round-18 `sectionize`): lines 2007–2146; SHA-256 `eccd3ec82207fa69cee544f8f4ebfc0f9a473fe7254b8041ae2f5924f8d00a06`.

## Findings

1. **The documented env-diff entry fails in the required scratch clone.** Command:
   ```text
   cd /fast/scratch/hyaku/tameshi-r56/T56W2Read15/clone && python3 tools/env-diff.py --contract .ufo/evidence/round-21/c2-contract.json --out /fast/scratch/hyaku/tameshi-r56/T56W2Read15/tameshi-f5-clone-recheck.json
   ```
   Output:
   ```text
   ENVDIFF: classified=0/9 out=/fast/scratch/hyaku/tameshi-r56/T56W2Read15/tameshi-f5-clone-recheck.json
   EXIT=1
   tameshi-runner unavailable PIN_UNREADABLE: tameshi-runner
   js-kimi-census unavailable PIN_UNREADABLE: js-kimi-census
   ```
   Its default `--fleet-root` is derived from the tool path; in the scratch clone that is not the fleet root. Supplying `--fleet-root /home/vgpnk/Projects/shokunin` yields 9/9, exit 0. The listed entry omits this required override for the mandated clone context.

2. **Stale active-row count at C0.** SKILL.md:2120 says “49 active rows from round 26 on”; `tools/registry.json` at C0 has 50 active rows. Command/output:
   ```text
   $ python3 - <<'PY'
   import json, subprocess
   raw = subprocess.run(['git','show','c0137451f5b7f22d65f748fc69f1b181f55e1378:tools/registry.json'], capture_output=True, text=True).stdout
   rows = json.loads(raw)['rows']
   print('total', len(rows), 'active', sum(r.get('status') == 'active' for r in rows))
   PY
   total 57 active 50
   ```
   Round-26 and round-55 registries each had 49 active rows; C0 adds active `receipt-revision-gate-selftest`, so the unqualified “from round 26 on” count is stale at C0. The round-24 count of 47 and frozen replay count of 43 are historical populations and remain correct.

## Notes

- A rerun of the retained round-20 route-mix spec is now accepted (exit 0), while `.ufo/evidence/round-21/routemix-r20-spec1.json` records refusal (exit 1). The section's Round-28 correction already warns that live route-table reruns can differ from retained receipts.
- The C1 mutant set includes hooks-off MB08/MB09 and pidfd-ownership R07. The “not demonstrated malicious hooks or PID reuse” wording is consistent with the round-21 lesson's scope limitation, though it could be read ambiguously.

## Commands run

- Imported `.ufo/evidence/round-18/measure.py` and used its `sectionize()` on `git show c0137451f5b7f22d65f748fc69f1b181f55e1378:SKILL.md`; got start=2007, end=2146, and the SHA-256 above.
- Created a `git clone --shared` scratch clone and checked out C0 detached.
- Ran the section's self-invocations in the C0 clone: env-diff 9/9; wave-route-mix 8/8; round21-measure 13/13; coldread selector 12/12; wave-accounting 8/8 frozen + 16/16 supplemental; command-binding 44/44; registry-replay 10/10. All exited 0.
- Ran the env-diff entry from the live lane root (9/9, exit 0) and from the scratch clone without `--fleet-root` (0/9, exit 1); reran from the clone with `--fleet-root /home/vgpnk/Projects/shokunin` (9/9, exit 0).
- Ran wave-route-mix on the round-21 and round-20 specs; also ran synthetic concentration and unrouted-role specs (both exit 1).
- Ran round21-measure `--claim c1` and `--claim c2`, coldread measure `--explain`, wave-accounting clean and wrong-count pairs, command-binding clean and source-read pairs, registry-replay `--plan`, and registry-replay `--run` with a missing repo (uncaught traceback, exit 1).
- Counted active registry rows at C0, round 26, and round 55.
- Ran `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` (exit 0).

Receipts: `T56W2Read15-receipts/`.
