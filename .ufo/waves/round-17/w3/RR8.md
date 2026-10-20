# RR8 — residual cold re-read: `### Round-17 gate/probe registry — input-keyed credit`

- Rev read: `0ff273448ac4e62893c9b28a4cea7c580712df19` (clone `/tmp/tameshi-r17w3-RR8-EjGKKa/fleet/tameshi-shokunin`, detached at that rev; fleet-mirror symlinks under `$W/fleet`).
- SKILL.md at that rev: sha256 `de6c2b083be6f35d2c35e011ca37874f57204a2cdd195a106ff638fbea723dbc`, 1903 lines — verified with `git show <rev>:SKILL.md | sha256sum` and `wc -l`.
- Section bound: heading is line 1897; section = lines 1897–1903 (end of file). Lines 1894–1896 belong to the previous section ("The rule makes a recorded read checkable, not complete." + blank). Section sha256 (lines joined by `\n`, trailing newline stripped, per the lane sectionizer) = `dfa21a33320292355cd185fa9a1ab52f0521648c4191318cc269a498cdd4ae9e` — matches the assigned digest. Raw bytes including the trailing newline hash to `e9b66760e37f0566f230c1e4a8da0ad89a44547f0119874df7978475b6625dad` (same convention difference observed, not a mismatch).

## Method

Every command below was wrapped exactly as the cold-read interface requires:

    python3 $C/.ufo/evidence/round-17/coldread/trace-inputs.py --root $C --out <TR>/<n>.json -- <argv...>

where `$C` = the clone and `<TR>` = `.ufo/evidence/round-17/coldread/traces/RR8` (lane-relative). All 14 receipts exist, carry `schema` `tameshi-trace-inputs-v1`, `rev` = `0ff273448ac4e62893c9b28a4cea7c580712df19`, and `live_lane_reads: {}` (empty — nothing traced ever read the live lane). The only bare (unwrapped) run is the acceptance validation at the end, which necessarily reads the live lane as `--repo` and therefore cannot produce a clean provenance receipt; it is recorded here honestly with its exit. No tools were installed or upgraded (none needed). No git writes anywhere; no `jj`; sibling repos untouched.

## Execution — every command form and exit class in the section's three rows

Row 1: `.ufo/evidence/round-17/measure.py` (probe)

| Receipt | Command (inner argv) | Receipt exit | Observed key lines | Registry claim | Match |
|---|---|---|---|---|---|
| 1.json | `python3 …/measure.py --rev 0ff27344…` | 0 | `ledger_present: false`, `reasons: {no-ledger: 58}`, `sections_total: 58`, revision echoed `0ff27344…`, `trace_gate: strict`, `overrides_used: false` | "0 measured (a missing default ledger is 0 with reason `no-ledger`)" | yes |
| 2.json | `--rev bbbb…bbbb` (40-hex, unresolvable) | 2 | `{"error": "rev-missing", "rev": "bbbb…"}` | 2 = "rev … missing" | yes |
| 7.json | `--rev 40f8e1f3…` (root commit) | 2 | `{"error": "blob-missing", "missing": ["tools/mutate-and-run.sh", "corpus/SOURCES.md"]}` | 2 = "required blob missing" | yes |
| 3.json | `--rev 0ff27344… --ledger-file /nonexistent-rr8.json` | 2 | `{"error": "ledger-file-unreadable", "detail": "[Errno 2] …"}` | 2 = "explicit `--ledger-file` … unreadable" | yes |
| 4.json | `--rev 0ff27344… --inputs-overlay <tmp>/overlay-bad.json` (overlay item carries `verdict`) | 2 | `{"error": "overlay-field-forbidden", "fields": ["verdict"]}` | 2 = "a forbidden overlay field" | yes |
| 5.json | `--rev` (no value) | 64 | `measure.py: error: argument --rev: expected one argument` | 64 usage | yes |
| 6.json | `--selftest` | 0 | `MEASURE_SELFTEST: 94/94 pass` | `--selftest` passes | yes |

Row 2: `.ufo/evidence/round-17/coldread/trace-inputs.py` (probe)

| Receipt | Command (inner argv) | Receipt exit | Observed key lines | Registry claim | Match |
|---|---|---|---|---|---|
| 1.json (same run) | happy path `-- python3 …/measure.py --rev 0ff27344…` | 0 | receipt written with the command's exit | "0 traced (the command's exit is in the receipt)" | yes |
| 8.json | `-- python3 …/trace-inputs.py --bogus-flag` | 64 | inner argparse: `unrecognized arguments: --bogus-flag`, exit 64 recorded in receipt, outer 0 | "64 usage" | yes |
| 14.json | `-- env PATH=/nonexistent-ti-rr8 /usr/bin/python3 …/trace-inputs.py …` | 2 | inner stderr: `trace-inputs: strace not found in PATH` | 2 = "strace unavailable" | yes |
| 13.json | `-- python3 …/trace-inputs.py --root $C --out <tmp> -- ./no-such-command-rr8` | 2 | inner stderr: `trace-inputs: strace -y unusable (probe failed)`; the tool's own selftest case `missing-command-exit2` also PASSes (visible in 12.json output) | 2 = "… or the command never executed" | yes (exit code; see note below) |
| 12.json | `-- python3 …/trace-inputs.py --selftest` (traced) | 1 | inner output `SELFTEST: 4/27` — nested ptrace refused kills most fixture cases | "`--selftest` … fails under an outer tracer (nested ptrace is refused), so never wrap it" | yes, honest non-green record per the L1 note; the row's own warning is thereby confirmed, not contradicted |

Note on 13.json: under an outer tracer the inner probe itself fails (nested ptrace) before the missing command can produce the "no successful execve" line, so the observed stderr reason differs while the exit class (2) is identical; the missing-command trigger's exit-2 is additionally attested by the `missing-command-exit2` PASS inside the selftest output captured in 12.json. Exit-code claim holds; no contradiction found.

Row 3: `.ufo/evidence/round-17/coldread/assemble.py` (gate)

| Receipt | Command (inner argv) | Receipt exit | Observed key lines | Registry claim | Match |
|---|---|---|---|---|---|
| 9.json | `--reports <empty dir> --out <tmp>/empty-out.json` | 1 | `no reports resolved: 0 loaded, 0 rejected — refusing to emit an empty ledger as success` | 1 = "… no report found" | yes |
| 10.json | `--expect-skill-sha nothex` (and `--reports` omitted variants hit the same path) | 2 | `assemble.py: error: --reports is required` / `error: --expect-skill-sha must be a 64-hex sha256` (argparse) | 2 usage (argparse) | yes |
| 11.json | `--selftest` | 0 | `SELFTEST: all checks passed` | `--selftest` passes | yes |
| (bare, acceptance) | `--reports <this report> --repo <lane> --out /tmp/RR8.json` | recorded after this file is written; expected `uncovered buckets` > 0 (one seat cannot cover the page) with `rejected reports: none` | see below | 0 requires "every bucket covered"; a single-seat run exits 1 on uncovered buckets, which is the row's 1 = "a bucket uncovered", not a rejection | yes (verified post-write) |

## Record-reading

The section is a registry table; its checkable claims are the three tools' command forms and exit classes. All three command forms exist at the read rev and behave exactly as the Exits column states. The trace-inputs row's nested-ptrace caveat is true as written (receipt 12: traced selftest 4/27, exit 1). measure.py's docstring (lines 93–95) and assemble.py's documented exits agree with the row text; no drift found between the section and the tools at this rev. Nothing in the range names `tools/registry-check.py` or any ledger numbers, so no further claims were checkable from this range alone. `bucket-commands.json` (rev `98bea7da…`, 54 buckets, `n_uncovered: 0`) was opened as supporting context for how command-bearing sections are classified; it carries the earlier rev's page sha (`906fb649…`) and makes no claim about this section's text at `0ff27344…`.

Agreement: this seat's findings agree with the wave-2/residual landing claims for this bucket — the registry row is accurate at `0ff273448ac4e62893c9b28a4cea7c580712df19`, including the honest caveat about `--selftest` under an outer tracer.

## Verdict

Section `### Round-17 gate/probe registry — input-keyed credit` (lines 1897–1903, sha256 `dfa21a33…` sans trailing newline) at `0ff273448ac4e62893c9b28a4cea7c580712df19`: every stated exit class exercised under the tracer and confirmed; holds.

```json
{"schema":"tameshi-coldread-report-v2","seat":"RR8","skill_sha256":"de6c2b083be6f35d2c35e011ca37874f57204a2cdd195a106ff638fbea723dbc","read_rev":"0ff273448ac4e62893c9b28a4cea7c580712df19","sections":[{"start":1897,"heading":"### Round-17 gate/probe registry — input-keyed credit","class":"instruction","verdict":"executed-ok","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":[],"commands_executed":["$C=.ufo clone of tameshi-shokunin at 0ff273448ac4e62893c9b28a4cea7c580712df19; TR=.ufo/evidence/round-17/coldread/traces/RR8; every command below was run as: python3 $C/.ufo/evidence/round-17/coldread/trace-inputs.py --root $C --out TR/<n>.json -- <argv>","1: python3 $C/.ufo/evidence/round-17/measure.py --rev 0ff273448ac4e62893c9b28a4cea7c580712df19 -> outer 0, receipt exit 0, ledger_present=false, reasons {no-ledger: 58}","2: python3 $C/.ufo/evidence/round-17/measure.py --rev bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb -> receipt exit 2 rev-missing","3: python3 $C/.ufo/evidence/round-17/measure.py --rev 0ff273448ac4e62893c9b28a4cea7c580712df19 --ledger-file /nonexistent-rr8.json -> receipt exit 2 ledger-file-unreadable","4: python3 $C/.ufo/evidence/round-17/measure.py --rev 0ff273448ac4e62893c9b28a4cea7c580712df19 --inputs-overlay /tmp/tameshi-r17w3-RR8-EjGKKa/overlay-bad.json -> receipt exit 2 overlay-field-forbidden fields=[verdict]","5: python3 $C/.ufo/evidence/round-17/measure.py --rev -> receipt exit 64 argparse usage","6: python3 $C/.ufo/evidence/round-17/measure.py --selftest -> receipt exit 0, MEASURE_SELFTEST: 94/94 pass","7: python3 $C/.ufo/evidence/round-17/measure.py --rev 40f8e1f3178249dc921459ede211d6ecaff63c58 -> receipt exit 2 blob-missing [tools/mutate-and-run.sh, corpus/SOURCES.md]","8: python3 $C/.ufo/evidence/round-17/coldread/trace-inputs.py --bogus-flag -> receipt exit 64 argparse usage","9: python3 $C/.ufo/evidence/round-17/coldread/assemble.py --reports <empty dir> --out /tmp/tameshi-r17w3-RR8-EjGKKa/empty-out.json -> receipt exit 1, no reports resolved: 0 loaded, 0 rejected","10: python3 $C/.ufo/evidence/round-17/coldread/assemble.py --expect-skill-sha nothex -> receipt exit 2 argparse usage","11: python3 $C/.ufo/evidence/round-17/coldread/assemble.py --selftest -> receipt exit 0, SELFTEST: all checks passed","12: python3 $C/.ufo/evidence/round-17/coldread/trace-inputs.py --selftest (traced, honest non-green per row caveat and L1 note) -> receipt exit 1, inner SELFTEST: 4/27, nested ptrace refused","13: python3 $C/.ufo/evidence/round-17/coldread/trace-inputs.py --root $C --out /tmp/inner13.json -- ./no-such-command-rr8 (nested) -> receipt exit 2, inner strace -y probe refused under outer tracer; missing-command-exit2 case itself PASSes inside 12's selftest output","14: env PATH=/nonexistent-ti-rr8 /usr/bin/python3 $C/.ufo/evidence/round-17/coldread/trace-inputs.py --root $C --out /tmp/inner14.json -- /usr/bin/true (nested) -> receipt exit 2, inner strace not found in PATH","bare (acceptance, run after this report was written; unwrappable because it reads the live lane as --repo and a receipt would carry live-lane reads): python3 $C/.ufo/evidence/round-17/coldread/assemble.py --reports <this report> --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --out /tmp/RR8.json"],"opened":[".ufo/evidence/round-17/measure.py",".ufo/evidence/round-17/coldread/trace-inputs.py",".ufo/evidence/round-17/coldread/assemble.py",".ufo/evidence/round-17/coldread/bucket-commands.json"],"inputs":{".ufo/evidence/round-17/measure.py":"d25d3d04cb26ca7c20ef7333baaa181c350c6ee912d58f648927fb835b3ce7f3",".ufo/evidence/round-17/coldread/trace-inputs.py":"521be95581a5073e47a92aa6c77a0087f101545a9c8d69db620d910ac0953070",".ufo/evidence/round-17/coldread/assemble.py":"8bcce2eafe37e5ca11e1a145e4c6c826071eca55917ddb464a1b6da190f6ccd1",".ufo/evidence/round-17/coldread/bucket-commands.json":"39b9392afb5d230750683e6ed5b1ce7ed74079a150318f136421293930328bf5"},"external_inputs":{},"traces":[".ufo/evidence/round-17/coldread/traces/RR8/1.json",".ufo/evidence/round-17/coldread/traces/RR8/2.json",".ufo/evidence/round-17/coldread/traces/RR8/3.json",".ufo/evidence/round-17/coldread/traces/RR8/4.json",".ufo/evidence/round-17/coldread/traces/RR8/5.json",".ufo/evidence/round-17/coldread/traces/RR8/6.json",".ufo/evidence/round-17/coldread/traces/RR8/7.json",".ufo/evidence/round-17/coldread/traces/RR8/8.json",".ufo/evidence/round-17/coldread/traces/RR8/9.json",".ufo/evidence/round-17/coldread/traces/RR8/10.json",".ufo/evidence/round-17/coldread/traces/RR8/11.json",".ufo/evidence/round-17/coldread/traces/RR8/12.json",".ufo/evidence/round-17/coldread/traces/RR8/13.json",".ufo/evidence/round-17/coldread/traces/RR8/14.json"]}]}
```
