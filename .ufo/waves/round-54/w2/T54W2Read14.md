# T54W2Read14 — cold read of `### Round-13 gate/probe registry` at C1

- Heading: `### Round-13 gate/probe registry`
- Candidate revision: `99c3bc88d704566197783f66b211ee0a830e0330` (C1)
- `section_sha256` (printed by reader-section.py): `896722c4941841f228810678befe82e9910cc66eb67c3de45d7561ce4668566d`
- Section bytes: SKILL.md lines 1573–1588 at C1 (1588 is the blank line before `## Effective expectation reconciliation — round 14` at 1589)

## Findings

None. `findings: []`.

The section ships clean at C1 under the reader criteria: every named anchor resolves, the two table rows are accurate against the artifacts they cite, no sentence contradicts another, and no run-together token / missing space / duplicate parenthetical was found. Every candidate defect below was investigated and rejected on evidence, recorded so the empty list is auditable rather than assumed.

## Artifacts opened (lane paths absolute, read-only)

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md` at C1 (section lines 1573–1588; heading target at 1-based line 1780; neighbouring boundaries 1570–1572, 1585–1594)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/pin-disposition.py` (docstring exit map 70–90 and 150–165; `LEGS` 139–144; `strict_scratch_root` 161–174; selftest scratch creation 725; `main`/`selftest` exits ~1340–1405)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/witness-metadata.py` (header 1–140: `PINNED_INPUTS`, `RERUN_SUMMARY_REL`, `EXPECTED_KIND`, `EXPECTED_DISCLOSURE`, `PRODUCER_TOOL_PATH/SHA256`, `HISTORICAL_RUNNER_PATH/SHA256`; `run_check` 400–530; CLI 1220–1300)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/pin-manifest.json` (6 legs, `pinned_source` line refs, `derived_from` sha)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/witness-metadata.json` (`frozen_declaration` = 3 inputs; `scope` covered/uncovered null observations; `expected` = `{id: metadata_consistent, exit: 0}`)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-13/expected.json` (exists; not read by this gate)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-12/BashWitness/{summary.json,declaration.json,declared.tsv,rerun-20261020T035435Z/summary.json}`
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md` (rows S047 line 56, S048 line 57, S266 line 141; 139 `| S…` rows)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/incremental-pin-disposition.md` (S047/S048 text at 1, 5, 67, 346–349)
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/fleet-kill-rate-ledger.md` (line 272: fifth/sixth cases landed by round 8)

No SKILL.md, tool, counter, contract, freeze, ledger, or wave-spec file was edited. Nothing was installed (pacman paused; no tool needed). No mutating git/jj command was run anywhere.

## Commands run and what they showed

1. Section locator (TMPDIR under `/fast/scratch/hyaku/tameshi-r54/T54W2Read14`):
   `python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin 99c3bc88d704566197783f66b211ee0a830e0330 "### Round-13 gate/probe registry"`
   → `start 1573 end 1588 section_sha256 896722c4…`.

2. Bytes:
   `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 99c3bc88d704566197783f66b211ee0a830e0330:SKILL.md | sed -n '1573,1588p'`
   → heading, 8-column header, two data rows, blank, then prose lines 1580–1587; boundaries confirmed (1589 is the next `##` heading).

3. Entry command row 1:
   `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin`
   → exit 0; `counts {legs: 6, unchanged: 1, changed: 5, unavailable: 0}`; 6 legs exactly. Confirms the cell "0 observations, including changed/unavailable" and "six-leg".

4. Entry command row 2:
   `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json`
   → `WITNESS_METADATA: metadata_consistent reason=ok exit=0 … inputs=summary,declaration,declared,rerun_summary`, exit 0. Confirms "0 metadata_consistent/clean" and that exactly the companion plus four frozen files are the read set.

5. Hidden-input sweep for row 2's "the four frozen round-12 files" / "this gate never reads":
   - `grep -n "PRODUCER_TOOL_PATH\|HISTORICAL_RUNNER_PATH\|checked_live" tools/witness-metadata.py` → live tool hash is carried as a literal with `checked_live` required to be `false` (lines 168–181, 452–476); the gate never opens `tools/*` on disk.
   - `grep -rln "expected.json" tools/` → witness-metadata.py absent (readers are repeat-control, evidence-disposition, context-capture, registry.json, wave-accounting, command-binding, registry-replay, write-path-census v2/v3). The "never reads expected.json" clause holds.

6. Anchor resolution:
   - `ls` on `tools/pin-disposition.py`, `tools/witness-metadata.py`, `.ufo/evidence/round-13/{pin-manifest,witness-metadata,expected}.json` → all present.
   - `find . -name declared.tsv -o -name declaration.json` → `.ufo/evidence/round-12/BashWitness/{declared.tsv,declaration.json}` (the four frozen inputs live under `…/round-12/BashWitness/`, not directly under `…/round-12/`).
   - Exact-line match for the quoted heading: `grep`-equivalent search produced `exact-line hits: [1780]`, unique.
   - `grep -n "S047\|S048\|S266" corpus/SOURCES.md` → S047:56, S048:57 ("supersedes S047 — item 4 is prioritisation rather than a reuse skip"), S266:141.

7. Self-test command arms (static, since running the selftests would create temp git fixtures and the reader criteria do not require it):
   - `tools/pin-disposition.py`: `argv == ["--selftest"]` is accepted (main), selftest returns 0 PASS, 1 FAIL, 2 COULD_NOT_EVALUATE (ScratchRootUnusable caught at main → exit 2, stderr, no traceback). Matches "selftest 1 failed" plus the row's 2 arm.
   - `tools/witness-metadata.py`: `--selftest` is a required mutually-exclusive mode flag (build_parser 1228–1231); argparse usage errors exit 2, matching "including usage".

8. Quality sweep over the 16 section lines:
   - backtick parity: 6 on 1577, 16 on 1578, 2 on 1581 (all even, no unclosed code span);
   - no trailing whitespace, no tabs, no double spaces outside code paths;
   - duplicate-word scan: none;
   - the only "space before punctuation" hits are the literal relative paths `.ufo/…` inside backticks (not prose defects).

9. Census (context only): `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0; SOURCES.md carries 139 `| S…` rows, so the S047/S048 anchors are live rows.

## Candidate defects considered and rejected

- **"four frozen round-12 files" names basenames, not full paths** (`summary.json`, … , `rerun-20261020T035435Z/summary.json`). Rejected: the same cell's first clause sends the reader to the tool for the "literal frozen input digests", and `witness-metadata.py` pins the full paths (`.ufo/evidence/round-12/BashWitness/…`, `RERUN_SUMMARY_REL`); every basename is unique under `round-12/BashWitness/` and all four exist. The count four = 3 `PINNED_INPUTS` + rerun summary is exactly what `--check` consumed (`inputs=summary,declaration,declared,rerun_summary`).
- **`S048 supersedes S047` vs `S266 supersedes S048`** (SOURCES.md:141). Rejected: S266's row supersedes "S048's anchor and quote only" and re-pins the same bytes (`sha256 e9cbc3e1ab7c…`, the sha S041/S047 already carried); the section's retained distinction ("item 4 is prioritisation, not a reuse skip") is S048's substantive claim and survives. The sentence is a historical clarification, and it does not contradict any sentence in the section.
- **"the six recorded cases at this write"**. Rejected: the ledger records the fifth and sixth cases as landed by round 8 (`fleet-kill-rate-ledger.md:272`), so six is right for a round-13 write, and the parenthetical's "seventh … since round 16" is explicitly forward-looking.
- **"The historical summary's producer SHA names the producer that actually ran, not the repaired current producer."** Rejected as a defect: `summary.json#/tool.sha256 = 249d9dcd…` while the current `tools/bash-witness-study.py` hashes `f2bb50c7…`; the statement is true and the tool enforces `checked_live is False`.
- **Row 1's omission of a normal-mode exit 1**. Rejected: the tool's exit map has no normal-mode 1 (0 observations, 2 could-not-evaluate only); "selftest 1 failed" is the only 1 arm, exactly as written.
- **Row 2's "1 metadata_inconsistent/failed" not literally emitted**. Rejected: `metadata_inconsistent` is the emitted id (line 261); "failed" is the same arm's English gloss, and the parallel registry row (`SKILL.md:2193`) uses the identical "1 failed" gloss.

## Provenance / limits

- C1 bytes only; wave-1 reader JSONs were not opened.
- All commands ran read-only against the lane; the only writes are this MD and `T54W2Read14.json` under `.ufo/waves/round-54/w2/`.
- The two tools' `--selftest` verbs were verified by source (accepted argv, exit arms), not executed, to avoid creating git fixtures; the C2 claim separately owns their executed self-test arms.
