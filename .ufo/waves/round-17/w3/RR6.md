# RR6-2 — cold-read re-read: SKILL.md:1806-1813 `### Round-16 gate/probe registry`

Seat RR6 (wave 3 residual re-read). Read rev `0ff273448ac4e62893c9b28a4cea7c580712df19` (fresh clone
`/tmp/tameshi-r17w3-RR6-vlVVcK/fleet/tameshi-shokunin`, fleet-mirror layout, detached at the read rev).

## Page and section identity

- `git show 0ff273448ac4e62893c9b28a4cea7c580712df19:SKILL.md | sha256sum` →
  `de6c2b083be6f35d2c35e011ca37874f57204a2cdd195a106ff638fbea723dbc` (matches the assigned page).
- Lines 1806-1813 (8 lines, trailing newline stripped) hash to
  `2642efc5147715676537ab35e1489742f4183b39c8a6ff0e51e25213695be843` — exactly the assigned section
  sha. (With the trailing newline the span hashes `ea3f9859…`; the canonical section hash strips it,
  consistent with assemble.py's documented "joined with \n AFTER stripping trailing blank lines; no
  trailing newline".) Heading `### Round-16 gate/probe registry` confirmed at start 1806 also by
  round-16 measure.py's section map (receipt 5: `"start": 1806`).

## What the section claims (record table, 4 rows)

| Row | Command(s) | Documented exits |
|---|---|---|
| `tools/mutate-and-run.sh` (gate) | `--selftest` · `--regression` | selftest 0 pass / 1 fail; regression 0 PASS · 1 FAIL · 2 SETUP · 64 usage |
| `.ufo/evidence/round-16/measure.py` (probe) | `--rev REV` · `--selftest` | 0 measured · 2 rev/blob missing · 64 usage |
| `.ufo/evidence/round-16/coldread/assemble.py` (gate) | `--selftest` | 0 every bucket covered (a rejected report is printed, not counted) · 1 a bucket uncovered · 2 usage (argparse), an invalid override or a heading mismatch (round 17) |
| `.ufo/evidence/round-16/attribution/reattribute.py` (probe) | `--selftest` | 0 corrected rule passes the oracle · 1 it fails |

## Commands executed (all under trace-inputs.py, cwd = clone)

All wrapper exits are 0 by design (inner exit lives in the receipt JSON). Receipts:
`.ufo/evidence/round-17/coldread/traces/RR6/<n>.json`; every receipt: `rev=0ff2734…`,
`tracked_filter=true`, `live_lane_reads=0`.

| # | Command (cwd = $C unless noted) | Receipt exit | Key output |
|---|---|---|---|
| 1 | `bash tools/mutate-and-run.sh --selftest` | 0 | `MUTATE_SELFTEST: 95/95 pass` / `VERDICT: PASS`; arms assert 1-fail ("inconclusive run exits 1"), SETUP 2 (duplicate/escape/no-op refusals, pin mismatch, missing target, repo_identity_mismatch, no-exec blob), usage 64 ("missing --target exits 64", "--regression refuses --target") |
| 2 | `bash tools/mutate-and-run.sh --regression` (264 s) | 0 | 7/7 legs exact: `REGRESSION: PASS (cases=7 passed=7; ledger legs exact: killed-delta<=0 flips<=0)`; per-leg `match=10/10` (checklist-run 15/15), flips=0, inconclusive=0 |
| 3 | `bash tools/mutate-and-run.sh --bogus` | 64 | `mutate-and-run: unknown argument: --bogus` + usage |
| 4 | `python3 .ufo/evidence/round-16/measure.py --selftest` | 0 | `MEASURE_SELFTEST: 38/38 pass`; arms cover exit2-bad-rev, exit2-blob-missing, exit64-no-rev, exit64-unknown-arg, exit2-no-repo |
| 5 | `python3 .ufo/evidence/round-16/measure.py --rev 0ff2734… --repo $C` | 0 | measured JSON (`revision`, depth_score 7, 58 sections) — "0 measured" |
| 6 | `python3 .ufo/evidence/round-16/measure.py --rev 000…0 --repo $C` | 2 | `{"error": "rev-missing", ...}` — "2 rev missing" |
| 7 | `python3 .ufo/evidence/round-16/measure.py --repo $C` (no --rev) | 64 | `measure.py: error: --rev is required` |
| 8 | `python3 .ufo/evidence/round-16/coldread/assemble.py --selftest` | 0 | `SELFTEST: all checks passed`; `REJECTED … seatBad.md` printed and not counted; arms assert "incomplete coverage exits 1 got 1", "heading mismatch exits 2 got 2", relaxing/equal-rank override rejected exit 2 |
| 9 | `python3 .ufo/evidence/round-16/coldread/assemble.py --nonexistent-flag` | 2 | `assemble.py: error: unrecognized arguments: --nonexistent-flag` (argparse) |
| 10 | `python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest` | 0 | `SELFTEST: PASS (new rule 8/8; old rule fails 5/8; old-rule fidelity 14/14)` |
| 11 (auxiliary, **not** part of the credited entry — root = `/tmp/tameshi-r17w3-RR6-vlVVcK/failcopy`, a shared clone detached at the same rev with `.ufo/evidence/round-15/verification-3.json` tampered: 4 `observed_id` values changed) | `python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest` | 1 | `SELFTEST: FAIL (new rule failed 1 of 8; old rule failed 6; fidelity failures 4)` — the documented "1 it fails" arm, exercised directly without touching any lane file. Receipt `.ufo/evidence/round-17/coldread/traces/RR6/11.json` (rev `0ff2734…`, exit 1) is deliberately excluded from the JSON block's `traces`: its input surface records the corrupted receipt blob, which by construction conflicts with the pristine `verification-3.json` declared in `inputs`. |

Note on row 2: measure.py's `DEFAULT_REPO` is the live lane
(`/home/vgpnk/Projects/shokunin/tameshi-shokunin`, measure.py:53), so the seat passed `--repo $C`
explicitly per the seat contract (never aim lane tools at the live lane). The tool accepts `--repo`;
the record's command column omits it — not treated as a defect. No nested-ptrace trap applies here:
none of the four tools invokes trace-inputs.py or tools/registry-check.py (grep over
`.ufo/evidence/round-16` for `trace-inputs|registry-check|ptrace`: no matches).

## Verdict per claim

- Row 1: selftest 0 observed directly (95/95); the 1/2/64 arms are asserted inside that same selftest
  run. Regression 0 observed directly (7/7 PASS at exact tolerance, 264 s); 64 observed directly
  (--bogus); 1 FAIL / 2 SETUP arms are asserted inside the selftest's regression-engine cases
  (doctored table → exit 1; pin mismatch / missing target → exit 2). Holds.
- Row 2: 0 measured, 2 (rev missing directly; blob-missing arm in selftest), 64 directly. Holds.
- Row 3: 0 with rejected-report-printed-not-counted, 1 (selftest-asserted exit 1), 2 (argparse
  directly; heading-mismatch and invalid-override arms exit 2). Holds.
- Row 4: 0 directly (8/8, old-rule fidelity 14/14); 1 directly via tampered-copy run (receipt 11).
  Holds.

No wrong expectations found; no blocking gaps. The section is a record and every documented exit was
observed as a real process exit (directly or via an asserted selftest arm of the same tool at this
rev). `verified-record`.

```json
{"schema":"tameshi-coldread-report-v2","seat":"RR6","skill_sha256":"de6c2b083be6f35d2c35e011ca37874f57204a2cdd195a106ff638fbea723dbc","read_rev":"0ff273448ac4e62893c9b28a4cea7c580712df19","sections":[{"start":1806,"heading":"### Round-16 gate/probe registry","class":"record","verdict":"verified-record","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":[],"commands_executed":["bash tools/mutate-and-run.sh --selftest","bash tools/mutate-and-run.sh --regression","bash tools/mutate-and-run.sh --bogus","python3 .ufo/evidence/round-16/measure.py --selftest","python3 .ufo/evidence/round-16/measure.py --rev 0ff273448ac4e62893c9b28a4cea7c580712df19 --repo <clone>","python3 .ufo/evidence/round-16/measure.py --rev 0000000000000000000000000000000000000000 --repo <clone>","python3 .ufo/evidence/round-16/measure.py --repo <clone>","python3 .ufo/evidence/round-16/coldread/assemble.py --selftest","python3 .ufo/evidence/round-16/coldread/assemble.py --nonexistent-flag","python3 .ufo/evidence/round-16/attribution/reattribute.py --selftest"],"opened":["tools/mutate-and-run.sh",".ufo/evidence/round-16/measure.py",".ufo/evidence/round-16/coldread/assemble.py",".ufo/evidence/round-16/attribution/reattribute.py",".ufo/evidence/round-15/verification-3.json",".ufo/evidence/round-17/coldread/trace-inputs.py"],"inputs":{"tools/mutate-and-run.sh":"fb6d86d59b5c9285864c9ebfa19d5a6f8938e91c47877a6d25b451a1da03001a",".ufo/evidence/round-16/measure.py":"03b67f58742a95e8c28ba1bffd06bd487fdc8d4c2c3130c43b487e7768c8ffbb",".ufo/evidence/round-16/coldread/assemble.py":"9ee9264aabe9f474b4ecf7cfa52b4d50274ee4a6b82d06df36812a006eb0a156",".ufo/evidence/round-16/attribution/reattribute.py":"eaf564e42629634e21bc2ee1aa70932a1024d721eba664f8ed892640590015c1",".ufo/evidence/round-15/verification-3.json":"3c419055723319f50611eb7d2fa3de46e4d4c37fb405267609eee80aecc7d8ce"},"external_inputs":{"kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs":"83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426","kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh":"275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f","tsukuroi-shokunin@165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh":"084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5","mado-shokunin@eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh":"d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13","kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/checklist-run.sh":"7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf","kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/claims-check.mjs":"e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b","kumitate-shokunin@364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs":"f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9"},"traces":[".ufo/evidence/round-17/coldread/traces/RR6/1.json",".ufo/evidence/round-17/coldread/traces/RR6/2.json",".ufo/evidence/round-17/coldread/traces/RR6/3.json",".ufo/evidence/round-17/coldread/traces/RR6/4.json",".ufo/evidence/round-17/coldread/traces/RR6/5.json",".ufo/evidence/round-17/coldread/traces/RR6/6.json",".ufo/evidence/round-17/coldread/traces/RR6/7.json",".ufo/evidence/round-17/coldread/traces/RR6/8.json",".ufo/evidence/round-17/coldread/traces/RR6/9.json",".ufo/evidence/round-17/coldread/traces/RR6/10.json"]}]}
```
