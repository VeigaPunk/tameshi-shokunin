# T56W2Read16 — cold-read report

Heading: `### Round-26 gate/probe registry — report interop`  
Candidate: `c0137451f5b7f22d65f748fc69f1b181f55e1378`  
Section: lines 2175–2214; SHA-256: `cc23587b353fb780d4310aebc7277e4030729ae767850e2e826d2ff151bdea52`

## Findings

- **Minor — `python3 tools/bash-witness-study.py check` fails at C0.** Exit 1:
  `WITNESS_CHECK: DRIFT tools/mutate-and-run.sh sha256=977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda committed=75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`
  `WITNESS_CHECK: FAIL (1 problems; 96 files covered)`
  The exit map does include digest drift as an exit-1 class; the frozen round-12 runner pin is nevertheless stale against C0 (also recorded in round-15 verification-4).
- **Minor — `python3 tools/registry-check.py --rev HEAD --json` is non-clean at C0.** Run from the live lane: exit 1, `REGISTRY_CHECK: held=48/50 superseded=7`; the active differing rows were `sources-census` (S280 id-or-path-cite violation) and `verify-round15`. The row documents exit 1 as “failed”; this records the current registry state rather than a false exit-map claim.

## Residual notes

- The Round-26 mte-interop command, run from a C0 clone with `--fleet-root /home/vgpnk/Projects/shokunin`, passed with `MTE_INTEROP: PASS legs_conforming=10/10`; both named registry expectations exist. Its selftest passed `17/17`.
- `env-diff` classified `0/9` when launched from the scratch clone because its default fleet root was outside the fleet. The same entry command from the live lane path passed `9/9`; this is checkout-location dependent.
- The fleet census required by the assignment (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`) exited 0. The separate legacy lane-local kaika census is the `sources-census` registry row noted above.
- All other round-51 selftest counters/output markers checked matched their table entries, and referenced pinned paths resolved. Placeholder commands requiring caller-supplied bundles/cases were not run literally.

## Commands run

- Loaded the frozen round-18 `sectionize`, read C0 `SKILL.md` lines 2175–2214, and computed the section SHA-256 above.
- Ran the Round-26 mte-interop `--check` and `--selftest`; checked usage exits.
- Ran the round-51 selftests for bash-witness-study, command-binding, context-capture, env-diff, evidence-disposition, golden-verdict, mte-interop, mutate-and-run, pbt-staged-id, pin-disposition, receipt-measure, receipt-window, registry-check, registry-replay, repeat-control, round21-measure, shrink-case, staged-id-guard, tally-audit v2/v3, tally-audit, trace-inputs, wave-accounting, wave-parent-settle, wave-route-mix, witness-metadata, and write-path-census v2/v3/v4.
- Ran applicable entry commands for bash-witness-study, context-capture, env-diff (clone and live lane), evidence-disposition, golden-verdict, mte-interop, pin-disposition, pbt-staged-id, receipt-measure, registry-check, repeat-control, round21-measure, trace-inputs, staged-id-guard, wave-parent-settle, witness-metadata, write-path-census, and the census validation.
