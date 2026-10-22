# Read04: cold read of SKILL.md:314-373 (Kill-rate bands)

Verdict: **gap-minor**. Class: **record**. Read point 2227d8338c02aa9a5fd7d95c1a41b76865ad7647, detached fleet-mirror clone. Page sha256 386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95 (checked at the clone and at the rev).

The measured figures hold at the revisions their notes pin. The gaps are an unpinned artifact path, one count the cited lines do not support, an unstated boundary reading, and three pointer slips. None blocks the section.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read04", "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95", "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
 "sections": [{"start": 314, "heading": "## Kill-rate bands \u2014 admission readings (rounds 2\u20133, measured)", "class": "record", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": [
   "Unpinned artifacts (SKILL.md:316-317 and 320-321): kumitate-shokunin/scripts/kimi-census.mjs and kagi-shokunin/corpus/surface-census.sh are named with no revision or sha256. The 43/43 control holds at kumitate 175de6ba (sha256 83016d45...4f426; mutation-case-kimi-census.md:13-16). The same path at HEAD f69817ed prints KIMI_CENSUS_SELFTEST: 48/48 pass (receipt Read04-2). The 16-case control holds at kagi fecee874 (sha256 275d8294...53009f; mutation-case-kagi-census.md:13-17) and at HEAD 899c50b4 (receipt Read04-3). Pin the revision wherever the figures are stated.",
   "Unsupported count (SKILL.md:361): 'D1/D3 die on 16 cases each, 14 shared (mutation-case-kimi-census.md:74-76)'. Lines 74-76 give one 16-case group for both defects (exact green baseline, two --json cases, 13 more) and no 14. The only '14' strings in the note are dates. Per-case lists are not in the lane.",
   "Boundary reading unstated (SKILL.md:324-325): the section says 'that boundary reading is the worked one' without saying which row 80 % takes. The table's strict '>80 %' puts 8/10 in the 50-80 % row, and mutation-case-kagi-census.md:57-60 applies that row by attaching the survivors table. The section should say so.",
   "Pointer to a non-supporting line (SKILL.md:331): the <50 % row cites mutation-case-kimi-census.md:29-33, which reports an 80 % run. Its admission rule rests on the pre-registered anti-claim (plans/round-2.plan.md:8-9); no <50 % case was measured. The plan says the round admits 'that IS the finding' with 'the bar table recording the gap'; the section says 'the survivors table IS the finding'.",
   "PROVINCE pointer one line off (SKILL.md:340): cites PROVINCE.md:16-17 for the at-least-two-lane bar. The bar sentence ('admitted from evidence in TWO independent lanes') is PROVINCE.md:15-16, which the divergence section cites (SKILL.md:462).",
   "Bands-convention pointer (SKILL.md:335-337): cites mutation-case-kimi-census.md:185-191, which records the E1 calibration miss on D7. It supports 'gap recorded, not softened' but not 'a report convention, not a pass/fail gate'."
  ],
  "commands_executed": [
   "python3 tools/trace-inputs.py --root /tmp/Read04-hkTI/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read04-1.json -- python3 -c '<printer: for each path:lo-hi spec print numbered lines>' PROVINCE.md:1-25 corpus/knowledge/mutation-case-kimi-census.md:3-8 corpus/knowledge/mutation-case-kimi-census.md:21-38 corpus/knowledge/mutation-case-kimi-census.md:43-54 corpus/knowledge/mutation-case-kimi-census.md:58-77 corpus/knowledge/mutation-case-kimi-census.md:100-145 corpus/knowledge/mutation-case-kimi-census.md:147-167 corpus/knowledge/mutation-case-kimi-census.md:184-208 corpus/knowledge/mutation-case-kagi-census.md:26-39 corpus/knowledge/mutation-case-kagi-census.md:41-61 corpus/knowledge/mutation-case-kagi-census.md:104-127 corpus/knowledge/mutation-case-kagi-census.md:194-205 plans/round-2.plan.md:7-10 corpus/knowledge/gates-survey-kumitate.md:49-60 (exit 0; printed the cited passages)",
   "python3 tools/trace-inputs.py --root /tmp/Read04-hkTI/fleet/tameshi-shokunin --out .../traces/Read04-2.json -- node /tmp/Read04-hkTI/sib/kumitate/scripts/kimi-census.mjs --selftest (kumitate f69817ed exported by git archive into scratch; exit 0; 'KIMI_CENSUS_SELFTEST: 48/48 pass', 'VERDICT: PASS')",
   "python3 tools/trace-inputs.py --root /tmp/Read04-hkTI/fleet/tameshi-shokunin --out .../traces/Read04-3.json -- bash /tmp/Read04-hkTI/sib/kagi/corpus/surface-census.sh --selftest (kagi 899c50b4 exported into scratch; exit 0; 'SELFTEST: PASS (16 cases)'; skip-case 15 and 16 'substrate-absent (handler not on PATH)')",
   "python3 tools/trace-inputs.py --root /tmp/Read04-hkTI/fleet/tameshi-shokunin --out .../traces/Read04-4.json -- python3 -c '<printer>' corpus/knowledge/mutation-case-kimi-census.md:1-2 corpus/knowledge/mutation-case-kimi-census.md:77-80 corpus/knowledge/mutation-case-kagi-census.md:1-25 (exit 0)",
   "python3 tools/trace-inputs.py --root /tmp/Read04-hkTI/fleet/tameshi-shokunin --out .../traces/Read04-5.json -- python3 -c '<printer>' corpus/knowledge/mutation-case-kimi-census.md:9-20 corpus/knowledge/mutation-case-kimi-census.md:80-100 plans/round-2.plan.md:1-13 (exit 0)",
   "python3 tools/trace-inputs.py --root /tmp/Read04-hkTI/fleet/tameshi-shokunin --out .../traces/Read04-6.json -- node /tmp/Read04-hkTI/pinned/kimi/scripts/kimi-census.mjs --selftest (kumitate 175de6ba, sha256 83016d45...4f426; exit 0; 'KIMI_CENSUS_SELFTEST: 43/43 pass', 'VERDICT: PASS')",
   "python3 tools/trace-inputs.py --root /tmp/Read04-hkTI/fleet/tameshi-shokunin --out .../traces/Read04-7.json -- bash /tmp/Read04-hkTI/pinned/kagi/corpus/surface-census.sh --selftest (kagi fecee874, sha256 275d8294...53009f; exit 0; 'SELFTEST: PASS (16 cases)')",
   "python3 tools/trace-inputs.py --root /tmp/Read04-hkTI/fleet/tameshi-shokunin --out .../traces/Read04-8.json -- python3 -c '<printer>' .ufo/evidence/kaika-round-1/witness/js-kimi-census.defects.tsv:1-40 .ufo/evidence/kaika-round-1/witness/js-kimi-census.results.tsv:1-40 (exit 0)",
   "python3 tools/trace-inputs.py --root /tmp/Read04-hkTI/fleet/tameshi-shokunin --out .../traces/Read04-9.json -- bash -c 'git show 2227d8338c02aa9a5fd7d95c1a41b76865ad7647:<8 lane paths> | sha256sum; GIT_OPTIONAL_LOCKS=0 git -C <sibling mirror> show <40-hex rev>:<path> | sha256sum for 5 sibling paths' (exit 0)",
   "python3 tools/trace-inputs.py --root /tmp/Read04-hkTI/fleet/tameshi-shokunin --out .../traces/Read04-10.json -- bash -c 'git show 2227d8338c02aa9a5fd7d95c1a41b76865ad7647:SKILL.md | sha256sum; git show ...:.ufo/waves/round-26/w1/ColdreadPilot.md | sha256sum; git show ...:SKILL.md | wc -l' (exit 0)"
  ],
  "opened": ["SKILL.md", "tools/trace-inputs.py", ".ufo/waves/round-26/w1/ColdreadPilot.md", "corpus/knowledge/mutation-case-kimi-census.md"],
  "inputs": {
   "PROVINCE.md": "b2875fe21f381d98551d5a4946af4fb547ceb6244ce6bef35885dbdf034c28be",
   "corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548",
   "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0",
   "corpus/knowledge/gates-survey-kumitate.md": "3dca7a1a5c621bf0ec75948d0836839dec98651673bb2987861d9aa122579b0e",
   "plans/round-2.plan.md": "8eccbbfdf0d8c2bd76ced8c9d58c40c17ea48dfeb564f598c315ea835360ccec",
   "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4",
   ".ufo/evidence/kaika-round-1/witness/js-kimi-census.defects.tsv": "6949035cba1ec8ff88e824321b8dd8e9fa6a0bfe961b8323da712191c90e0612",
   ".ufo/evidence/kaika-round-1/witness/js-kimi-census.results.tsv": "e859d7159abd9cdeec8f0bc4520bbd73da80885be15d7d9bcea4a541e9838b1f",
   ".ufo/waves/round-26/w1/ColdreadPilot.md": "428a61a30ff8cf9e02f5a2a0923f916cf5f4c98596d2ace022f9d982fc25ceb7"
  },
  "external_inputs": {
   "kumitate-shokunin@f69817edf687c8ce4f87ed7953a353399232f69e:scripts/kimi-census.mjs": "7818970b80d4951b8edf15dcc8c5a16efe57f457f956a5ce019f049068538156",
   "kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs": "83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426",
   "kumitate-shokunin@f69817edf687c8ce4f87ed7953a353399232f69e:scripts/cite-check.mjs": "40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f",
   "kagi-shokunin@899c50b42634a3a4ad0b28ab7509786315e2fc2b:corpus/surface-census.sh": "1e697b0179547a869b73fcf966ce05dd60b07adbe7094a95d3d0a2d4102de11d",
   "kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh": "275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f"
  },
  "traces": [
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read04-1.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read04-2.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read04-3.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read04-4.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read04-5.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read04-6.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read04-7.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read04-8.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read04-9.json",
   "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read04-10.json"
  ]
 }]}
```

## Evidence

Every receipt (Read04-1 to Read04-10) has rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647, exit 0, and empty `live_lane_reads` and `external`. The two sibling-side runs used scratch copies exported with `git archive` or `git show` at pinned revisions. Nothing was written to a sibling or to the lane except this report and the receipts.

1. Bounds. The section is SKILL.md:314-373. Line 314 is the only heading in that span, the next heading is SKILL.md:375, and line 374 is blank. Two fence lines precede line 314, so the heading is outside a fence.
2. Page identity. `git show 2227d…:SKILL.md | sha256sum` gives 386de44b…e95 (Read04-10).
3. Kimi control at its pin. Kimi note :13-16 pins kumitate 175de6ba…, sha256 83016d45…4f426, 896 lines, 43273 B. Running `node kimi-census.mjs --selftest` from that exact file prints `KIMI_CENSUS_SELFTEST: 43/43 pass` and `VERDICT: PASS` (Read04-6). The note's line 21 says the same.
4. Kimi control at HEAD. The same command at f69817ed (sha256 7818970b…, 957 lines, 46638 B) prints `KIMI_CENSUS_SELFTEST: 48/48 pass` (Read04-2).
5. Kagi control at its pin. Kagi note :13-17 pins fecee874…, sha256 275d8294…53009f, 44212 B. `bash surface-census.sh --selftest` prints `SELFTEST: PASS (16 cases)` with skip-case 15 and 16 `substrate-absent (handler not on PATH)` (Read04-7). Notes :42-43 and :50-53 say the same.
6. Kagi control at HEAD. Same output at 899c50b4 (sha256 1e697b01…, 44220 B; Read04-3).
7. Survivors. Witness results.tsv line 3 is `D2 SURVIVED`, line 11 is `D10 SURVIVED`, and the other eight are KILLED (Read04-8). Kimi note :29 and kagi note :50 both report 8/10, and the notes name the survivors.
8. Restore hashes. Kimi note :34-35 and kagi note :54-56 quote the same sha256 values as the pinned files in items 3 and 5.
9. Host-gated skips. SKILL.md:369-371 says the bash verb cases skip on this host. The live run at both revisions prints the skip-case lines above, so the claim holds today.
10. cite-check (SKILL.md:363-365; gates-survey-kumitate.md:51-58). At kumitate f69817ed, scripts/cite-check.mjs line 267 sets only `opts.selfTest` for `--selftest`, line 2354 is the skip arm `if (!opts.integrations)`, 2357 is the guard, 2372-2384 is the mutation copy with `gate.rs:15` to `gate.rs:11` at 2377, and line 2515 dispatches `--selftest` to `selfTest`, where the skip arm then applies because `integrations` is false. The blob sha256 40573448…c10c9f matches the round-26 pilot record (ColdreadPilot.md:259-260).
11. Plan and PROVINCE. plans/round-2.plan.md:8-9: 'Anti-claim: if the suite kills <50% of injected defects, the round still admits (that IS the finding) with the bar table recording the gap.' PROVINCE.md:15-16: 'a pattern is admitted from evidence in TWO independent lanes before it is claimed general'. The divergence section (SKILL.md:460-462) cites PROVINCE.md:15-16.
12. Search for the 14. A case-sensitive `grep` of the kimi note for `shared|\b14\b` finds no shared-count line and only digit-14 dates (for example 2026-10-14). A case-insensitive `grep` for `shared|fourteen` finds only the 'Shared class' heading at line 101. `git ls-files` lists no tracked `.ufo/evidence/round-2/` files.

Claims that hold at the pinned revisions: 8/10 and 80 % for both controls; the survivor sets (kimi D2 and D10; kagi B5 and B10, from the note); the 43/43 and 16-case controls; the suite count held; no inconclusive run; the restore hashes; the no-live-tree runs (kimi note :4-7); the host-gated skips; the cite-check lines; the plan's anti-claim wording; the PROVINCE bar sentence; the (U) and (I) markers.

Claims that do not hold as written or cannot be checked: the 43-case count at the named HEAD path (SKILL.md:316-317); the 14 shared count (SKILL.md:361); the unstated boundary reading (SKILL.md:324-325); and the pointers at SKILL.md:331, 335-337 and 340.

## Smallest safe correction

1. At SKILL.md:316-321, add the pins: 'kumitate-shokunin/scripts/kimi-census.mjs at 175de6ba (sha256 83016d45...4f426)' and 'kagi-shokunin/corpus/surface-census.sh at fecee874 (sha256 275d8294...53009f)'.
2. At SKILL.md:361, drop '14 shared' and say the two defects each die on 16 cases (mutation-case-kimi-census.md:74-76).
3. At SKILL.md:324-325, add: '80 % is not above 80 %, so both points read in the 50-80 % row and are cited only with the survivors table attached (mutation-case-kagi-census.md:57-60).'

Optional pointer fixes: move the kimi :29-33 pointer out of the <50 % row (331) and mark that row as pre-registered (plans/round-2.plan.md:8-9); change PROVINCE.md:16-17 to 15-16 (340); and re-point or drop :185-191 (337).

## Residual risk and verification gaps

- Time scope. The verdict assumes the heading 'rounds 2-3, measured' scopes the 43-case and 8/10 figures to the measured revisions. If the L1 reads the first paragraph as a present-tense claim about HEAD, the 48/48 result makes it a wrong-expectation. I did not mark it that way, because each figure matches its pinned revision.
- '14 shared' cannot be checked. Per-case lists are not in the lane, and the note's own composition gives one 16-case group. If the L1 wants this kept, it needs the round-2 results file.
- I re-ran the two controls at their pins and at HEAD, not the mutant sweeps. The 8/10 figures rest on the notes plus the kaika round-1 verdict table, which agrees only on D2 and D10.
- Timings from the traced runs (about 1.2 s kimi, about 3.3 s kagi, under strace) are not comparable with the historical sweep times and are not used. SKILL.md:372 already marks timing host-local (U).
- Setup and search steps ran outside the collector: the prescribed clone, `git ls-files` and `cat-file` checks, and grep and read tool calls over .ufo/evidence for orientation. Every fact in this report that depends on them is re-derived under the collector (Read04-9, Read04-10), and no discovery result is used as evidence. The round-25 MTE report was not used.

## Tools and writes

- Tools installed or upgraded: none. Used the already-present git, bash, node v24.21.0, python3 3.14.8 and strace. No pacman, uv or npm transaction ran.
- Writes: this report and receipts Read04-1 to Read04-10 under .ufo/evidence/round-27/coldread/traces/. Scratch copies live under /tmp/Read04-hkTI.

COLDREAD Read04: gap-minor
