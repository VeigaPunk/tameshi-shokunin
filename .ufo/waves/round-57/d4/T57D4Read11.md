# T57D4Read11 — documentary audit

Scope: T57W3Read11.md/.json and retained receipts, compared with committed C0b `adf87899c70d616140a81185a8f9acbbdfb30392`. Axes: receipt consistency, committed-byte identity, claim boundaries, provenance completeness. Recommendation only: **bounded documentary agreement, with a provenance gap; integration remains UNVERIFIED.**

## Findings by severity

### Low — execution identity and scratch environment are asserted, not retained

`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read11.md:10` says every command ran from a detached C0b clone with seat-local TMPDIR. Each of its seven numbered receipt files contains only `command`, `cwd`, `exit`, `stdout`, and `stderr`; none retains clone HEAD, checkout/status output, or TMPDIR. A cwd string does not establish executed bytes or environment. The top-level JSON's `cand` and command-5 section hash identify the intended revision and committed section, not the execution revision of commands 2–4, 6–7. Command 1 additionally retains a tool SHA matching C0b, which partially narrows this gap.

Read-only documentary sweep (Python Eval, no imported candidate modules):

```python
for c in report['commands']:
    d = json.loads(pathlib.Path(c['receipt']).read_text())
    print(sorted(d))
    print(sorted(set(d) & {'cand','rev','revision','head','tool_sha256','environment','TMPDIR'}))
```

Observed keys for all seven: `['command', 'cwd', 'exit', 'stderr', 'stdout']`; provenance-field intersections: `[[], [], [], [], [], [], []]`. The report's original retained receipts are under `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read11-receipts/`.

Further, retained `pointer-sweep.py:5–6` imports the frozen sectionizer from the live lane, not the clone. This is another live input beyond the disposition root acknowledged in JSON note 12. Its present bytes equal C0b, so no contradictory hash was observed; that present comparison does not prove its historical execution bytes. Treat the record as unsigned observations, not independently authenticated C0b execution. Qualify the clone/TMPDIR assertion or provide already-existing contemporaneous identity evidence; do not retrofill observations.

## Bounded agreement and documentary sweep

Only source/data reads were performed. The SKILL content was obtained using:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md
```

Observed heading: `### Round-13 gate/probe registry`, lines 1590–1605; next heading at 1606: `## Effective expectation reconciliation — round 14`. Source-read the committed round-18 sectionizer, then reproduced its documented trailing-blank trimming and newline joining as data processing, without importing/executing it. Result: `SECTION_HASH_MATCH True 896722c4941841f228810678befe82e9910cc66eb67c3de45d7561ce4668566d`. A raw newline-inclusive slice has a different hash; this is expected normalization, not a defect.

Python data comparison of each main JSON command with its numbered receipt, across `command,cwd,exit,stdout,stderr`, yielded all five fields equal for each of 7/7 receipts. Retained outputs substantiate the narrative summaries:

- Command 1: exit 0; `counts={legs:6, unchanged:1, changed:5, unavailable:0}`; `result_reuse=not_established`. Committed tool SHA: `c917bc41c3f40dae3eacea492d861211c2a4fe1e530cb9f22c5f8d6ff47d2988`, matching receipt stdout.
- Command 2: exit 0; 19 retained `SELFTEST_CASE` lines; terminal `SELFTEST: PASS (19/19)`.
- Command 3: exit 0; `metadata_consistent reason=ok`, inputs `summary,declaration,declared,rerun_summary`.
- Command 4: exit 0; 39 retained `SELFTEST_CASE` lines; terminal `SELFTEST: PASS 39/39`.
- Command 5: exit 0; terminal `POINTER_AND_CLAIM_SWEEP_PASS`; includes the isolated without-expected command and its recorded exit 0. The retained script constructs this fixture and asserts that expected.json is absent.
- Commands 6–7: exit 2, respectively `invalid_usage` and required-mode argparse error. Expected-red observations are not mislabeled successful gate runs.

For frozen identities, the sweep used `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show REV:PATH` at C0b and assigned base `5e3569969b532310d2b8a3d130901757a3df356b`, then compared bytes and SHA256. All four comparisons returned `True`:

| Round-12 BashWitness input | C0b SHA256, matching base and retained command 5 |
|---|---|
| summary.json | acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9 |
| declaration.json | e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901 |
| declared.tsv | 0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3 |
| rerun-20261020T035435Z/summary.json | 6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0 |

Committed summary/companion producer hashes agree: `249d9dcd2dfb410f7e6847989da2cb3ab6ef7dd693b87ec2b9b4d6b193d43f1a`. Committed current producer hash is `f2bb50c77a6b6ffc53fd4e31d06c729f9cface7c1684f232c060f6a4978bf261`. These support the historical/current distinction, not authentication of the historical producer. Committed SOURCES rows S047/S048/S266 match command 5's printed rows and the stated anchor-only supersession.

## Residual risk and verification gaps

No contradictory retained exit, output summary, candidate label, normalized section hash, or frozen input identity was found. Agreement is documentary, not a replay pass. Disposition observations concern live fleet state at their recorded time, explicitly not a C0b fleet snapshot or reuse proof. The selftest counts are retained claims, not newly exercised tests or universal correctness evidence. This seat does not establish 64/64 NO-HARM, runtime continuity, same-identity rerouting, saturation, or admission; those are outside this item.

LSP device documentation request returned `No such tool: xd://lsp`; semantic status/references/definitions/diagnostics were unavailable. Source and byte comparisons are not semantic-reference proof. No candidate gates, tests, builds, exploits, credentials, external targets, alternate runtimes, or production edits were used. No tools installed/upgraded.

Self-evaluation: accuracy 4/5 (historical execution provenance unavailable); completeness 4/5 (documentary scope complete, no replay permitted); clarity 4/5 (long hashes retained for auditability); actionability 4/5 (qualify provenance assertion, without retrospective fabrication); conciseness 4/5 (selected evidence duplicated for independent review). Overall 4.0/5. Highest-impact improvement: contemporaneous per-command revision/environment evidence. User-agreement check: this bounded recommendation deliberately grants no admission.
