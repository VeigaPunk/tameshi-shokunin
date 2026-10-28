# T54W1Read17 — cold read: `## Context gate classification and explicit exit classes — round 15`

- heading: `## Context gate classification and explicit exit classes — round 15`
- cand (content commit C0): `59c38109bf119d0e9d4f878644a82babc937bc1e`
- section_sha256: `132cfb9ef1aa07111af42389e4fe862152e3118b3a8bb66f1d84a6a332e7edf6` (span `start=1635 end=1701`, as printed by `.ufo/waves/round-54/reader-section.py`; recomputation shows it is the sha256 of lines 1635-1700 joined by newline, i.e. the section text with its trailing blank line/newline stripped — same value the round-21 ledger carries for this heading)
- findings: **none**. No rule anchor failed to resolve, no table cell contradicted the artifact it cites, and no sentence contradicted another in the same section, under every check below.

## Bounds command and its output

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin && python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin 59c38109bf119d0e9d4f878644a82babc937bc1e "## Context gate classification and explicit exit classes — round 15"
{"heading": "## Context gate classification and explicit exit classes \u2014 round 15", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "start": 1635, "end": 1701, "section_sha256": "132cfb9ef1aa07111af42389e4fe862152e3118b3a8bb66f1d84a6a332e7edf6"}
```

The section bytes were read only with `git -C ... show 59c38109bf11:SKILL.md` (lines 1635-1701); no working-tree read was used for the section or for any cited object.

## What I opened, and what each check found

### Sources line (section line 1637-1640)

- `corpus/SOURCES.md` at C0: row `S049` exists (Python subprocess environment mapping, grade A, mined, opened 2026-10-20) and row `S051` exists (Retained context-receipt gate — `tools/context-capture.py`, grade A, mined, opened 2026-10-20, used-by `corpus/lessons/round-15.md`). Both cited rows still resolve, and C0's S277-S279 append did not disturb them.
- `corpus/lessons/round-15.md` at C0: headings `## Gate` (line 11) and `## Mistakes` (line 46) exist.
- `corpus/lessons/round-14-verifier-spotcheck.md` at C0: `## Routed defects and residuals` (line 154) carries item 5 (line 159-161), which is exactly the probe/gate mislabel and the missing exit-64 mapping this section corrects, including the `/tmp` literal-pair caveat.
- `../PROTOCOL.md` resolves at the fleet root (`/home/vgpnk/Projects/shokunin/PROTOCOL.md`), and `## Gate standard` exists there (line 375). Its text supports the section's inference: a gate compares surfaces against expected values persisted in its own repo and returns a verdict; codes other than 0/1 are declared in the registry entry and mapped onto `clean | failed | could-not-evaluate`; an undeclared nonzero code reads as could-not-evaluate. The round-16 errata repair of this anchor (`../PROTOCOL.md` rather than bare `PROTOCOL.md`) is present at C0.

### Effective runtime evidence and the two failed receipts (section lines 1642-1643)

- `.ufo/evidence/round-15/verification-3.json` exists at C0: `attempt 3`, `passed: true`, 44 checks, no failed check.
- The two earlier receipts exist and both are failed harness runs: `verification.json` (44 checks, failed `selftest-new`, `selftest-new-full-count`) and `verification-2.json` (`attempt 2`, failed `runner-internal-error`).
- A later `verification-4.json` (added in round 53, `attempt 4`, `passed: false`) also exists in the same directory, but it is not "earlier" and it is not a harness failure (failed checks are `tool-source-pin`, `integrity-tools/mutate-and-run.sh`, `integrity-SHONEN.md`, `runner-published-digest`, `measure-after-fields`), so the sentence's count is precise, not stale.

### Classification correction and archive status (section lines 1648-1666)

- `.ufo/evidence/round-14/capture-context.py` exists at C0 and its own bytes hash to the value the section pins, which reads in the section: bytes stay at sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`
- The instrument description checks out in the source: its module docstring (lines 2-31) documents the two-document probe comparison, the exact environment delta, the positive git control, the round-13 `expected.json`/`pin-manifest.json` digest binding and the six-leg mapping; `comparison_block()` pops only the top-level `observed_at` (`exclusions: ["observed_at"]`); `evaluate()` persists probe/runner/manifest/expected digests; `parse_runner_mapping()` requires six unique shared legs; `decide()` spans exactly 553-580 and returns only `("ok", 0, [])` or `("mismatch", 1, reasons)`; `main()` spans exactly 605-643. All three cited line ranges (`:2-31`, `:553-580`, `:605-643`) resolve in the 647-line file.
- Archive labels: the round-14 registry row above the section is `archived invocation context capture | historical gate, not active | do not run; retained source ... only`, and round-14 recipe step 5 is headed `Archived experiment, not an entry point` — so the section's claim that both are marked archive-only resolves.
- `tools/context-capture.py` contains no invocation of the archived script: the only occurrence of `capture-context` in the maintained tool is its docstring line 10 naming the archived file as replaced.

### Retained-check semantics and the two retained fixtures (section lines 1668-1684)

- `.ufo/evidence/round-14/context-receipt.json` hashes to `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a`, which is also the tool's literal `FROZEN_RECEIPT_REL`/digest default (`tools/context-capture.py:151-153`).
- `.ufo/evidence/round-14/context-missing-env.json` hashes to `1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208`, exactly as pinned in the section, and its recorded status is `ok`/exit 0 against raw fields that recompute mismatch — the discriminating counterpart the section describes.
- The retained receipt's `mapping.legs` holds six legs with `all_match`/`leg_set_equal`/`leg_order_equal` true, and `environment.injected_env` is the single declared `GIT_DIR` injection.
- The maintained tool re-derives rather than trusts: `positive_control.effective` is recomputed (`baseline_ok and injected["exit"] != 0 and reflects`) and compared (`effective recorded ... but raw runs recompute`), `comparison.raw_stdout_equal`/`payload_tool_sha256_matches_disk` are recomputed and compared, and stored `status`/`exit`/`reasons` are compared with the recomputed verdict. So `trust the receipt's stored summary booleans` being refused is true of the artifact, not just of the prose.

### Table cells executed against the artifact at C0

Run from a `git clone --shared` copy of the lane at C0 (`lane54`, toplevel asserted), with `TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1Read17`; no lane file was touched.

| Row (section wording) | Command | Observed | Cell holds |
|---|---|---|---|
| clean, exit0 | `python3 tools/context-capture.py --check` | `CONTEXT: OK (id=context_consistent receipt=.ufo/evidence/round-14/context-receipt.json sha256=05cb55b8... exit=0 findings=0)`, exit 0 | yes |
| "A re-derived predicate, source digest, control or mapping disagrees" | `--check --receipt .ufo/evidence/round-14/context-missing-env.json --expected <pin id=missing_injected_environment exit=1>` | `CONTEXT: MISMATCH (id=missing_injected_environment ... exit=1 findings=2)`, exit 1, findings `missing_injected_environment` and `receipt_verdict_mismatch` | yes |
| exit2 could-not-evaluate, "exit2 with a stable kind" | frozen receipt bytes edited in place in the clone, then `--check` | `CONTEXT: INVALID (id=snapshot_tampered ... exit=2 findings=2)`, exit 2 | yes |
| duplicate-key input is a finding unless clean | `--check --receipt ... --expected <expected JSON with duplicate 'receipt_sha256' key>` | `CONTEXT: INVALID (id=expected_invalid ... exit=2 findings=1)`, `duplicate JSON key 'receipt_sha256'` | yes |
| "Could not evaluate, exit64 for usage, no receipt written" | `--check --receipt <file>` (receipt without expected) | stderr usage text, `CONTEXT: USAGE_ERROR (id=usage_error exit=64)`, exit 64 | yes |
| six static mappings / one declared `GIT_DIR` injection | receipt at C0 | 6 `mapping.legs`, all_match true; `environment.injected_env` = the declared `GIT_DIR` | yes |
| selftest inputs synthetic, distinct from retained files | `python3 tools/context-capture.py --selftest` | `SELFTEST: PASS (49/49)`, including `hermetic-no-lane-path OK default lane root absent from subprocess output` and `hermetic-temp-only OK` | yes |

### Exit classes paragraph (section lines 1694-1700)

- Both gates named by the round-15 registry rows that follow the section declare the same four codes and the same class mapping: `0` clean, `1` failed, `2`/`64` could-not-evaluate, `64` usage. `tools/context-capture.py` returns 0/1/2/64 (verified by the runs above); `tools/evidence-disposition.py` at C0 still documents `exit 1 failed semantic expectation`, `exit 2 could-not-evaluate bad/missing/tampered input`, `exit 64 usage error`, and C0's new `ScratchRootUnusable` arm is itself mapped to exit 2 with a `could-not-evaluate` line, so this round's input drift did not break the section's mapping.
- The corrected rows resolve: the round-15 registry's disposition row reads `2 and 64 could-not-evaluate (invalid, missing or tampered inputs; 64 usage)`, and its context row reads `0 clean (...); 1 failed stable finding ID ...; 2 and 64 could-not-evaluate (... 64 \`usage_error\`)`.
- The no-harm sentence's `C1` referent resolves to the round-14 claim record: `.ufo/evidence/round-14/claims.json` carries the `C1` calibration claim with `scalar_before: 6`, `scalar_after: 6`; C0's content commit changes neither that file nor SCORECARD.md.

## Limits of this read

- `tools/context-capture.py` bytes have drifted since round 15 (round-15 pin `c4a1d165...`, C0 bytes `be539b4c...`). The section pins no digest for that tool, so this is not a stale cell; every behavioural claim about it above was re-executed at C0 rather than inferred from the round-15 pin.
- `verification-4.json` (round 53) is a later failing receipt in the round-15 directory; the section sentence scopes itself to "the two earlier failed harness receipts" and remains true, but the directory now holds a third failing receipt that this section does not mention. I did not treat that as a defect of this section, and I report it here as an observation only.
- No tool was installed or upgraded; no lane file was edited; the scratch clone and fixtures under `/fast/scratch/hyaku/tameshi-r54/T54W1Read17/` were removed at exit (see the cleanup note below).

## Scratch cleanup

`rm -rf -- /fast/scratch/hyaku/tameshi-r54/T54W1Read17` was run after the deliverables were written; `ls /fast/scratch/hyaku/tameshi-r54/` shows no `T54W1Read17` tree left by this seat.
