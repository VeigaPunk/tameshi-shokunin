# Read20: cold read of SKILL.md :1272-1280 (round 27, C1)

Verdict: gap-minor (class: record). Blocking gaps: none. Four minor gaps, each with a correction below.

Pin: 2227d8338c02aa9a5fd7d95c1a41b76865ad7647. SKILL.md sha256 386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95. The clone is /tmp/Read20-XqVO/fleet/tameshi-shokunin, detached at the pin, and its HEAD equals the pin.

## Boundary used

The item's rule ends a section before the next #, ##, or ### heading. The heading is at :1272. The next heading is the ### at :1281. So this verdict covers :1272-1280 only: the heading and a nine-line intro. The intro names no lane file. It cites `:1226-1228` on this page and the labels T10-1 and T10-2.

The next ## heading is at :1365, so the ## span runs :1272-1364. Its ### subsections at :1281 and :1302 (and any other ### in :1302-1364) cite the five files the monitor lists as input drift. I opened those five under the collector, so each has an inputs entry at the pin. I did not verdict those subsections. See the routing notes.

## Claim checks

1. "Round 7 made `--regression` the ledger's replay gate." Supported. SKILL.md :921-925 says round 7 turns `--regression` into the fleet's leg ledger, where each recorded case is a leg replayed at its pinned revision. The words "replay gate" first appear at :2074, after this section. The paraphrase is fair.
2. "rounds 8-9 left ... cases 5-6 ... still not embedded — named debt (`:1226-1228`)." The substance is supported. SKILL.md :1219 says `--regression` ran 4 legs. :1227-1228 says cases 5-6 are still not embedded and calls that named debt. Ledger :281-282 agrees (receipt Read20-1). The quoted words are not verbatim (minor gap 1).
3. "the registry ran four legs." The count is supported (SKILL.md :1219; ledger :281, "four materialized legs"). The naming is off (minor gap 3).
4. "the operator the arc was built for had no single entry point", which rounds 8-9 named as a gap. The closure is pointed. SKILL.md :1384 calls the runbook "the operator's entry point (T10-1)", and runbook line 4 calls it "the single operator-facing document" (receipt Read20-4). The "named in rounds 8-9" part is not supported. A case-insensitive search of SKILL.md :900-1271 for operator, entry point, runbook, single entry, and oral context returned no matches. A positive control on :1270-1300 matched "OPERATOR", so the search works (minor gap 2).
5. "Round 10 closes both — the runbook lands (T10-1, this round)." Supported. corpus/knowledge/operator-runbook.md at the pin has 517 lines, 33515 bytes, sha256 8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859. Line 1 reads "(round 10, T10-1)" and line 3 reads "Written 2026-10-14 by lane T10-1 (tameshi round 10)" (receipt Read20-4). The file is in the committed tree at the pin.
6. "the leg cut resolves as an embedding of cases 5-6 (T10-2), never a re-cut." The embedding is supported by the tool itself, tools/mutate-and-run.sh (receipts Read20-2, Read20-6, Read20-7):
   - :83 reads "r10-2 six legs", and :175 sets VERSION to `mutate-and-run.sh r10-2`.
   - :87-92 list six legs with recorded rates 8/10, 8/10, 6/10, 4/10, 7/15, and 7/10. These match SKILL.md :1312-1317 and ledger :279.
   - Spec files for case 5 (bash-checklist-run) and case 6 (js-claims-check) are written at :840 and :915.
   - The gate at :1141-1146 requires both spec files. Both run through regression_case_git at :1404-1413, and both are listed at :1951-1952.
   "Never a re-cut" holds, since the recorded rates are unchanged. The label T10-2 is not defined on the page or in the runbook (minor gap 4).

## Findings by severity

Blocking: none.

Minor, each with the smallest safe correction:

- Minor 1, misquote. :1275-1276 put "still not embedded — named debt" in quotation marks. That phrase does not appear in :1226-1228. The source reads "Cases 5–6 are still not embedded: their rows carry no `REGRESSION` line — named debt, not smoothed" (:1227-1228). The same phrase recurs at :1348 with the same pointer. Correction: quote the source words exactly, or mark the cut with an ellipsis.
- Minor 2, unsupported "named". :1276-1277 say rounds 8-9 named the missing operator entry point. Rounds 7-9 on this page never name it (the search above). Correction: point to where it is named, or say the gap was identified in round 10.
- Minor 3, naming. :1275 says "the registry ran four legs." The legs are not in tools/registry.json. That file has 56 rows (schema tameshi-entry-registry-v1). Its only regression row is row 20, `mutate-and-run-regression`, with argv `bash tools/mutate-and-run.sh --regression`. No row names bash-checklist-run or claims-check (receipt Read20-3). The legs live in tools/mutate-and-run.sh. Correction: "the `--regression` gate ran four legs."
- Minor 4, undefined label. :1278 uses "(T10-2)". The page uses that label only at :1278. The tool calls the same edit r10-2 (:175 and :83), and the runbook uses r10-2 at its ER-R1 and ER-R2 entries. Correction: state the mapping once, for example "T10-2 is the r10-2 edit of tools/mutate-and-run.sh."

## Observed, not verdicted (outside :1272-1280, for routing)

- :1306 cites `tools/mutate-and-run.sh:85-89` as the leg list. At the pin, lines 85-89 hold the comment header and three legs; the leg list runs :87-92. :1304 says the file is 1 642 L, but it is 2017 L at the pin (receipt Read20-2). Both anchors are dated to tool revision 75ed934d, so they are stale anchors rather than errors in the section.
- The :1302 heading "six-leg" is dated to round 10. At the pin the tool comment says "r26 nine" (:83), and the gate lists nine spec files (:1141-1145). This is correct as dated. It would mislead a reader who takes the page as current.

## Residual risk and verification gaps

- Boundary. If the monitor's section is the ## span (:1272-1364), this read does not verdict :1281-1364. Those lines need a second read.
- Commands outside the collector. The clone, the checkout, the symlinks, the rev-parse, the sha256 of the clone's bytes, and a read-only git ls-tree on the clone (to confirm the runbook and the tool are committed at the pin) ran outside the collector, as step 1 prescribes. The clone reads the live lane repository, and the collector would flag that as a live-lane read, so the clone cannot be traced. I also ran `ls -ld` on the lane's traces and waves directories (metadata only, outside any trace), and I read my own receipt files back as JSON. Page searches of SKILL.md were by hand; that page is excluded from inputs. I also searched the runbook and the registry by hand; those are the same bytes as the receipts. I read the godspeed skill file for posture only; it is not an input to any claim here.
- The runbook's ER-R1 and ER-R2 entries describe an uncommitted tool edit in progress when they were written. I read only the committed bytes at the pin.
- Not run: `tools/trace-inputs.py --selftest`. A record read does not need it.

## Tools

No tool was installed or upgraded. Present on the host: strace 7.2 (`strace -V`) and Python 3.14.8 (`python3 --version`).

## Receipts

Traces are Read20-1 through Read20-7 in /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/. Each receipt has rev 2227d8338c02aa9a5fd7d95c1a41b76865ad7647, rev_reason null, exit 0, and tracked_filter true. Each has empty untracked, external, and live_lane_reads maps, and dropped_home_count 0. Read20-7 replaced an earlier version of itself, so no stray receipt from this seat remains.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read20", "skill_sha256": "386de44be69de85ab90f3c0b1890f4e5f2b400ea52ff6ffe1d4dd65097c51e95", "read_rev": "2227d8338c02aa9a5fd7d95c1a41b76865ad7647",
 "sections": [{"start": 1272, "heading": "## The operator's runbook and the six-leg regression (round 10, measured)", "class": "record", "verdict": "gap-minor", "blocking_gaps": [], "wrong_expectations": [],
 "minor_gaps": [
  "Quotation is not verbatim: the phrase 'still not embedded — named debt' at :1275-1276 does not appear in :1226-1228. The source reads 'Cases 5–6 are still not embedded: their rows carry no REGRESSION line — named debt, not smoothed' (:1227-1228). The same phrase recurs at :1348 with the same pointer. Correction: quote exactly, or mark the cut with an ellipsis.",
  "Second named gap is unsupported as 'named': :1276-1277 say rounds 8-9 named the missing operator entry point, but SKILL.md :900-1271 has no operator, entry point, runbook, single entry, or oral context wording (case-insensitive search). The closure is pointed (:1384; runbook line 4). Correction: point to where it is named, or say the gap was identified in round 10.",
  "Naming: 'the registry ran four legs' (:1275). The legs live in tools/mutate-and-run.sh (:83-100 comment, :840 and :915 specs, :1141-1146 gate, :1404-1413 calls). tools/registry.json has 56 rows, one regression row (row 20, mutate-and-run-regression) and no rows for cases 5-6. Correction: 'the --regression gate ran four legs'.",
  "Undefined label: 'T10-2' (:1278) appears only at :1278 on the page and not in operator-runbook.md. The tool labels the same edit r10-2 (mutate-and-run.sh :175, :83). Correction: state the mapping once."
 ],
 "commands_executed": [
  "python3 tools/trace-inputs.py --root /tmp/Read20-XqVO/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read20-1.json -- python3 /tmp/Read20-XqVO/rd.py corpus/knowledge/fleet-kill-rate-ledger.md L281-282 G:Named",
  "python3 tools/trace-inputs.py --root /tmp/Read20-XqVO/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read20-2.json -- python3 /tmp/Read20-XqVO/rd.py tools/mutate-and-run.sh L83-100 L175-175",
  "python3 tools/trace-inputs.py --root /tmp/Read20-XqVO/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read20-3.json -- python3 /tmp/Read20-XqVO/rd.py tools/registry.json JROWS K:checklist-run|claims-check|mutate-and-run-regression",
  "python3 tools/trace-inputs.py --root /tmp/Read20-XqVO/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read20-4.json -- python3 /tmp/Read20-XqVO/rd.py corpus/knowledge/operator-runbook.md L1-4 L35-35 G:^#",
  "python3 tools/trace-inputs.py --root /tmp/Read20-XqVO/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read20-5.json -- python3 /tmp/Read20-XqVO/rd.py tools/trace-inputs.py L1-3 G:^SCHEMA G:^DEFAULT_LANE",
  "python3 tools/trace-inputs.py --root /tmp/Read20-XqVO/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read20-6.json -- python3 /tmp/Read20-XqVO/rd.py tools/mutate-and-run.sh L838-841 L913-916 L1141-1146 L1403-1413 L1948-1953",
  "python3 tools/trace-inputs.py --root /tmp/Read20-XqVO/fleet/tameshi-shokunin --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read20-7.json -- python3 /tmp/Read20-XqVO/rd.py tools/mutate-and-run.sh G:js-claims-check|bash-checklist-run"
 ],
 "opened": ["SKILL.md", "corpus/knowledge/fleet-kill-rate-ledger.md", "corpus/knowledge/operator-runbook.md", "tools/mutate-and-run.sh", "tools/registry.json", "tools/trace-inputs.py"],
 "inputs": {
  "corpus/knowledge/fleet-kill-rate-ledger.md": "13a11e468dbf26972bb9734c2f0bedec859386f6729225c367c61ba056d7499e",
  "corpus/knowledge/operator-runbook.md": "8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859",
  "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de",
  "tools/registry.json": "c1b75366f1789121e6d5a4c8f6587f7519fef3bad60569ed274df8c7a681b73c",
  "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4"
 },
 "external_inputs": {},
 "traces": [
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read20-1.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read20-2.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read20-3.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read20-4.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read20-5.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read20-6.json",
  "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-27/coldread/traces/Read20-7.json"
 ]}]}
```

What I checked, in plain terms: I built the pinned clone, confirmed its HEAD and the SKILL.md sha256, and read the section. It is a record, not an instruction. It states round history and points at this page's :1226-1228, the runbook, and the tool. Seven receipts were produced under the collector, and each one checks out at the pin. The runbook exists at the pin and is labelled round 10. The tool embeds cases 5 and 6, and the recorded rates are unchanged. The registry has one regression row and no case rows. The weak part is the account of rounds 8-9: the quotation is not verbatim, and rounds 7-9 on this page never name the entry-point gap.

COLDREAD Read20: gap-minor
