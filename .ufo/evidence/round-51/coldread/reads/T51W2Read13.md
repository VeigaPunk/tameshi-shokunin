# T51W2Read13 — cold-read re-key

Candidate: `6d8c11e378aa90b12650808e1b79270742935f15`; base: `9962033fd7a75aa2f2847e979dd687a5d28505a1`.

Re-resolved at candidate: `### The map — where a reader enters, artifact by artifact` begins at `SKILL.md:1380`; the next heading, `### Boundary readings, executed by this lane`, is at `:1396`. I read the complete section (`:1380-1395`) and checked its cited surfaces against candidate blobs. The map section itself is byte-identical to base.

## `reads.json` row

```json
{
  "heading": "### The map — where a reader enters, artifact by artifact",
  "heading_range": "SKILL.md:1380-1395 (next heading :1396)",
  "candidate": "6d8c11e378aa90b12650808e1b79270742935f15",
  "seat": "T51W2Read13",
  "pointers": [
    {"raw_text":"corpus/knowledge/operator-runbook.md","file":"corpus/knowledge/operator-runbook.md","ranges":null,"verdict":"holds","located_excerpt":"§3 six-row table at :131-175; §7 replay/default-scratch text at :345-353. The file exists and contains the sections named by the map. Stale claims: map says the lane held nine cases since round 26, while candidate runner records ten at round 51 (:84, :1504-1508, :2087); runbook §7 says default scratch is `mktemp -d /tmp/...` (:349-351), while candidate runner explicitly honors TMPDIR (:149-150). Runbook's six-case presentation is historical, not a current ten-leg roster."},
    {"raw_text":"SKILL.md:1294-1297","file":"SKILL.md","ranges":["1294-1297"],"verdict":"holds","located_excerpt":":1294-1296 says the runbook is a pointer, not a second home, and the anchored source governs divergence; :1297 begins the next bullet and is extraneous to the cited proposition."},
    {"raw_text":"corpus/knowledge/fleet-kill-rate-ledger.md","file":"corpus/knowledge/fleet-kill-rate-ledger.md","ranges":null,"verdict":"holds","located_excerpt":"Candidate :117-123 includes queue row :119: `drift-pins ... unmeasured by sweep; hermetic`. Candidate C2 `c2/sweep/sweep.txt` records the sweep, 10 defects, 2 killed, restore OK, and DONE (:1-31); candidate runner wires `bash-drift-pins` at :1504-1508. Ledger is byte-identical to base and has no appended drift-pins measurement row. Thus the map's `one row per gate measured so far` premise is false at CAND; its parenthetical only discloses the round-26 ninth case, not this measured tenth case."},
    {"raw_text":"corpus/knowledge/service-limits.md","file":"corpus/knowledge/service-limits.md","ranges":null,"verdict":"holds","located_excerpt":"Decision table exists at :42-55 with refusal rows a-j; this is the standalone detail-of-record named by the map."},
    {"raw_text":"SKILL.md:1246-1270","file":"SKILL.md","ranges":["1246-1270"],"verdict":"holds","located_excerpt":":1246 begins the service-limits section; the compact rendering and refusal table occupy the cited range and end with the re-resolve instruction at :1269-1270."},
    {"raw_text":"corpus/knowledge/service-optin-protocol.md","file":"corpus/knowledge/service-optin-protocol.md","ranges":null,"verdict":"holds","located_excerpt":"§1 request shape and re-pin at :54-77 (moved substrate requires re-pin at :61-62); §2 read-only at :109+; §3 owner-hardens at :142+; §4 report shape at :182+. These match the map's descriptions."},
    {"raw_text":"corpus/knowledge/fleet-suite-census.md","file":"corpus/knowledge/fleet-suite-census.md","ranges":null,"verdict":"holds","located_excerpt":"Standing offer :269-275 and queue :277-287 are present. The queue is a projection, not the drift-pins record; drift-pins is not listed in this census queue. The stale unmeasured label is specifically in the cited ledger at :119."},
    {"raw_text":"corpus/knowledge/service-standing-state.md","file":"corpus/knowledge/service-standing-state.md","ranges":null,"verdict":"holds","located_excerpt":"Boundary note describes fleet-visible/lane-owned and handoff at :3-9; SC1, SC2, SC3 are present at :159, :174, :181."},
    {"raw_text":"corpus/knowledge/mutation-case-*.md (six at round 11; seven since round 16; eight since round 18; nine since round 26)","file":"corpus/knowledge/mutation-case-*.md","ranges":null,"verdict":"holds","located_excerpt":"Candidate glob has 10 matching files, including new `mutation-case-kagi-drift-pins.md`; that note identifies itself as case 10 at :6-12 and contains pin/suite, sweep, verdict table, witnesses and reproduce material. The map's `nine since round 26` count is stale at CAND (case 10 was added in round 51)."},
    {"raw_text":"tools/mutate-and-run.sh (six-leg registry at round 11, seven since round 16, eight since round 18, nine since round 26; git-materialized replay)","file":"tools/mutate-and-run.sh","ranges":null,"verdict":"holds","located_excerpt":"CAND :84 says `r26 nine; r51 ten`; `bash-drift-pins` is wired at :1504-1508; ten-leg tally is asserted at :2087-2088. `--selftest`, `--regression`, git-materialized replay and workdir options remain present. TMPDIR behavior is now explicitly honored at :149-150. The map's nine-leg endpoint is false at CAND."},
    {"raw_text":"corpus/README.md (the coverage map — a row per note carried, holds + sources; round addenda append further tables of the same shape)","file":"corpus/README.md","ranges":null,"verdict":"holds","located_excerpt":"Coverage map header `Note | Holds | Sources` at :3-6 and rows follow; candidate round-51 tenth-case admission is separately recorded at :630-634. That new row is not in the same three-column shape, so the universal `addenda ... same shape` gloss is not demonstrated by this new entry (but the note is indexed by that separate row)."},
    {"raw_text":"plans/round-N.plan.md (latest plans/round-11.plan.md)","file":"plans/round-N.plan.md; plans/round-11.plan.md","ranges":null,"verdict":"holds","located_excerpt":"Candidate plans directory contains `round-11.plan.md`; its :13-25 supports the final-round frame and :290-300 includes the round-11 seat/write-scope plan. Concrete round-4 through round-10 plan files exist. `round-2.plan.md` and `round-3.plan.md` also exist, but are not part of the stated record-draft pairs."},
    {"raw_text":"plans/round-N-record-draft.md (concrete round-4 through round-10 plan and record-draft pairs)","file":"plans/round-N-record-draft.md","ranges":null,"verdict":"holds","located_excerpt":"Candidate plans listing has record drafts for each round 4-10; no round-11 record-draft file. This matches the stated pair range and the map's next clause that round 11 has no separate record file."},
    {"raw_text":"LOG.md:316-317","file":"LOG.md","ranges":["316-317"],"verdict":"holds","located_excerpt":"CAND blob :316-317: `Same dispatch shape as rounds 1–10 — the lane deliverables in this repo ARE the wave record (no .ufo/waves/tameshi-r11-* directory)`; supports the map's round-11 record pointer."},
    {"raw_text":"corpus/knowledge/closeout-r11.md","file":"corpus/knowledge/closeout-r11.md","ranges":null,"verdict":"holds","located_excerpt":"Candidate :34-40 distinguishes the round record from the corpus-side closeout and identifies the completion pack; :46-63 has the ten-round restatement and links to round rows/record drafts."},
    {"raw_text":"plans/completion-evidence.md","file":"plans/completion-evidence.md","ranges":null,"verdict":"holds","located_excerpt":"Candidate :1-8 says completion pack covers rounds 2-11, one line per round, SHONEN status and debts, with headlines pointing into landed records; its body contains the per-round table and debts."},
    {"raw_text":"LOG.md","file":"LOG.md","ranges":null,"verdict":"holds","located_excerpt":"CAND record blob contains the round entries, including the round-11 passage at :316-320."},
    {"raw_text":"SCORECARD.md","file":"SCORECARD.md","ranges":null,"verdict":"holds","located_excerpt":"CAND record blob has `## Move log` and its round rows/counting commands (:7-13; round 11 at :24)."}
  ],
  "strongest_possible_falsifier_checked": "Candidate runner itself states nine legs through round 26 and ten at round 51 (tools/mutate-and-run.sh:84), wires bash-drift-pins (:1504-1508), and selftests a 10/10 tally (:2087-2088). Candidate sweep receipt records the tenth case measured (2/10, restore OK, DONE). Yet the unchanged map says nine, and the unchanged ledger queue row still calls drift-pins unmeasured (:119) with no measurement row. Also checked TMPDIR: runner :149-150 honors TMPDIR, contradicting the runbook's bare /tmp-only default at :349-351. The four updated panel tools (tally-audit.py, v2, v3, mte-interop.py) are not named by this section, so they create no missing pointer or independent claim here.",
  "findings": [
    "False at CAND: map's runbook/runner/mutation-case prose says nine cases since round 26; runner and matching corpus files now contain ten (round 51).",
    "False at CAND: the map describes one row per measured gate but the tenth drift-pins sweep is present while ledger :119 still says unmeasured and no measurement row was appended.",
    "Stale cited detail: runbook §7's default `/tmp` scratch statement does not account for runner's CAND TMPDIR honoring.",
    "Qualified unsupported premise: README's tenth-note row is under a different table schema from the map/addenda `Note | Holds | Sources` shape; the note is present, so not an absent-note finding."
  ],
  "verification_gap": "No LSP device is mounted (`read xd://lsp` returned no such tool); candidate reads were direct git-show/git-cat-file byte reads and text ranges, not semantic LSP proof."
}
```

## Review notes

- The four panel-tool updates (three tally-audit versions and `mte-interop.py`) are present in the candidate diff, but none is a pointer in this section. The runner and all cited paths were verified at CAND; no panel-tool claim was attributed to the map.
- The table's direct pointers resolve. The actionable defects are false/stale content at those resolved targets, not absent files or moved section boundaries.
- No builds, tests, or linters were run. No repository code was edited.
