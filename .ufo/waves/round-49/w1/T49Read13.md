# T49Read13 — C1 reader: `## Promotion-evidence calibration` pointer ordinals 0–4

Base `8ca67421111fa354b47b803358391d0b07fc6db9`. Section `## Promotion-evidence calibration —
fleet round-1`, `section_start` 1464, frozen `section_sha256`
`76c6929815b2b84ed977d315674125d4c70ffc46de9d5b280134ede03fbdf6fe` — recomputed from the base blob
with the monitor's own `sectionize` (`.ufo/evidence/round-18/measure.py`) and found equal, one
section with this heading (receipt line 5).

The five pointers are the rows of `.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json`
with this heading and `ordinal` 0–4: one `external` line pointer (`../PROTOCOL.md:63–68`) and one
`line` pointer (`corpus/knowledge/executor-test-sufficiency.md:160–184`) at `skill_line` 1469 and
1472, then three `path` pointers (`SHONEN.md`, `reports/round-1-calibration.md`,
`corpus/lessons/round-1.md`) at `skill_line` 1466, 1467, 1477. The extractor finds exactly these
five in the section (`list_pointers` → `selected=5`, `missing_headings=[]`), which equals the
contract's frozen floor for this section (`promotion: 5`).

The counter script was **never executed** (no `--selftest`, no `--list`, no lane run). Its module was
imported read-only and its own pure helpers `norm()` / `pointed_text()` (`measure.py:202-208`) and
`check_reads()` (`measure.py:259-320`) were applied to these rows at BASE. That is a probe, not a
verdict, and it prints no label.

## Verdicts

| ord | raw | base_verdict | one-line reasoning |
|---|---|---|---|
| 0 | `../PROTOCOL.md:63–68` | **holds** | At fleet HEAD `d1e70ce6`, `PROTOCOL.md:63–68` is the `shonen → shokunin` gate bullet: `:64-65` "a subagent the lane dispatched is still the lane" carries "Tameshi-dispatched reviewers remain part of tameshi", and `:66-68` "only a non-author `<id>` may write `[x]` … any `[x]` carrying no named non-author verifier is author attestation" carries "a different agent name does not justify `[x]`"; the range lands on the bullet exactly, and the working-tree fleet file is byte-identical to HEAD (`git diff --stat HEAD -- PROTOCOL.md` → empty). |
| 1 | `executor-test-sufficiency.md:160–184` | **holds** | `corpus/knowledge/executor-test-sufficiency.md:160-162` is "one killed mutant of the JS case, control + gate + restore — **confirmed**" and `:165-166` is "Not tested by this run: the full 10-mutant sweep … any second executor (n = 1 reader)" — the two halves of "historical single-JS-mutant exercise, not a current full cold-read" both sit inside the range, which starts at the first bullet of §5 (`:155`), so it has not drifted. |
| 2 | `SHONEN.md` | **holds** | `SHONEN.md` at base is the lane's live 4-box promotion checklist (765 bytes, 12 lines; box marks `:5,:7,:9,:11` each with an in-repo evidence link at `:6,:8,:10,:12`, all `[~]` "no independent promotion verifier") — a checklist, not the historical training closeout; whole-blob pointer, so no line range to drift. |
| 3 | `reports/round-1-calibration.md` | **holds** | The file is `# Fleet round-1 calibration audit — tameshi-shokunin` (26 kB, 450 lines) and `## box-1` is at `:71`, so the section's `…#box-1` fragment resolves to a real heading; box-1 (`:71-104`) audits decision table / error taxonomy / checklist and its own opening (`:3-4`) cites `PROTOCOL.md:63–68` for the same reading. |
| 4 | `corpus/lessons/round-1.md` | **holds** | Whole-file read (40 kB, 490 lines): `- **Admitted (corrections):**` at `:106` and `- **Rejected, with reasons (kept per `corpus/QUALITY.md:8`):**` at `:114` with four numbered rejections at `:115-131` — the admitted correction and the rejected claims are both in this file, separately. |

Result: **0 stale, 0 unresolved, 0 absent** among ordinals 0–4. No `proposed_fix` rows are produced:
nothing in this section needs a pointer edit, a re-anchor or a qualification, and no pointer is
proposed for deletion (all five are required to keep the section's count at its floor of 5).

## Commands that show each verdict

```
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin; B=8ca67421111fa354b47b803358391d0b07fc6db9
git -C $LANE show $B:SKILL.md | awk 'NR>=1464 && NR<=1477'                 # the clauses, with line numbers
git -C /home/vgpnk/Projects/shokunin show d1e70ce6:PROTOCOL.md | awk 'NR>=63 && NR<=68'
git -C /home/vgpnk/Projects/shokunin diff --stat HEAD -- PROTOCOL.md      # empty: tree == HEAD
git -C $LANE show $B:corpus/knowledge/executor-test-sufficiency.md | awk 'NR>=158 && NR<=186'
git -C $LANE show $B:SHONEN.md                                            # whole file, 12 lines
git -C $LANE show $B:reports/round-1-calibration.md | grep -n '^#'        # '## box-1' at 71
git -C $LANE show $B:reports/round-1-calibration.md | sed -n '1,30p;71,110p'
git -C $LANE show $B:corpus/lessons/round-1.md | grep -n -i 'admitted\|rejected'
git -C $LANE show $B:corpus/lessons/round-1.md | awk 'NR>=60 && NR<=150'
```

Excerpt/claim containment, per row, plus the counter's own `check_reads()` aggregate over these five
rows at BASE: `.ufo/waves/round-49/w1/T49Read13.excerpt-check.txt` (all five `excerpt_in_pointed
True`, lengths 274/186/177/139/261 inside the 24–400 bound, all five `claim_verbatim True`,
aggregate `{"absent":0,"excerpt_miss":0,"not_holds":0,"unresolved":0,"unverified":0}`).

## Findings

1. **No staleness in ordinals 0–4.** Each target still carries exactly the evidence its clause
   needs — including the external pointer, which is the only one that could have drifted with the
   fleet repo: `PROTOCOL.md:63–68` at fleet HEAD `d1e70ce6` is still the promotion-gate bullet, and
   the working tree matches HEAD. Evidence: table above; receipt lines 10–14.
2. **Ordinal 0's clause needs the whole range, not one line.** `:64-65` gives "still the lane";
   `:66-68` gives the `[x]`-authority rule. If the integration rewords the sentence it must keep
   both halves pointed at `PROTOCOL.md:63–68`; splitting the pointer would drop one half. Same range
   is used independently by `reports/round-1-calibration.md:3-4` and
   `corpus/lessons/round-1.md:107`, so the three files agree on the citation — no conflict to report
   for the Rust judge.
3. **Ordinal 1 sits on a stable boundary.** The pointed range begins at the first bullet of
   `## 5. The SKILL's core claim, assessed` (`:155`) and ends at the last line of the (U3) bullet
   (`:184`); an insertion above `:160` would shift it. That is a re-key risk for a later edit, not a
   base defect: at base the range contains the (O) single-mutant sentence and the (U) n=1 limitation.
4. **Ordinals 2–4 are path pointers whose targets are small/large blobs, not line ranges.** Drift can
   only appear as a missing file or a missing heading: `SHONEN.md` exists (12 lines), `## box-1`
   exists at `reports/round-1-calibration.md:71`, and both the `Admitted (corrections)` and
   `Rejected, with reasons` blocks exist in `corpus/lessons/round-1.md` (`:106`, `:114`).
5. **Spot-check only, outside my pointer scope:** the audit's own inner SKILL cites —
   `reports/round-1-calibration.md:81` `SKILL.md:58–92`, `:83` `:497–525`, `:85` `:466–495` — still
   land on the gate-shape table (`SKILL.md:58`), the fail-closed arm taxonomy (`:497`) and the
   no-permissiveness recipe (`:466`) at base, so the audit is not silently pointing at moved text.
   This is not part of any verdict above.
6. **Floor note for integration:** the section's five pointers are exactly its frozen floor (5). All
   five already produce `holds` rows with located excerpts, so this section needs no text change to
   be credited by read rows; any rewrite, however, must keep at least five extractable pointers or
   the section drops below its floor.

## Out of scope / not done

- No counter invocation at any revision; no control was scored; no deciding behaviour is claimed.
  The label `C1_R49_PASS` was never produced or observed by this seat.
- Ordinals 5+ of this section (there are none: extraction yields 0–4) and the other six lapsed
  sections are other seats' items; the other 85 pointers of the base set were not read here.
- No edits to SKILL.md, the five targets, `PROTOCOL.md`, the contract, the pointer control file,
  `reads.json`, the lane's jj state or Git index. Read-only on the lane apart from the two wave-1
  deliverables.
- No tools installed or upgraded; no package manager touched.
- No `/home/vgpnk/.local/state/`, hidden C2 panel, or `control/c2-*.stdout` file opened.
- Scratch `/fast/scratch/hyaku/tameshi-r49/T49Read13/` (used only as `TMPDIR` for the in-process
  checks) removed before yield; nothing cited from it.

## Artifacts

- `.ufo/waves/round-49/w1/T49Read13.rows.json` — 5 rows, sha256
  `ebec3bafca4a80bac4a39153596f1b2084da4a4587b4b8ccaf9bce5b5375a106`.
- `.ufo/waves/round-49/w1/T49Read13.excerpt-check.txt` — receipt: pointers-file sha256
  `92a2e532fb323bee556e44b0877107339f7faa9e1c8f9636a8a6b1a8de6d4d3c`, per-row excerpt length /
  containment / claim-verbatim flags, section-sha equality (`equal=True`), `fleet_commit`
  `d1e70ce65352cf95866842eb81e470eda7988e8e`, and the `check_reads` aggregate.

## Summary

Section `## Promotion-evidence calibration — fleet round-1` (start 1464, sha `76c69298…`), pointers
0–4 read at base against their targets: all five **hold** — 0 stale, 0 unresolved, 0 absent.
Ord 0 (`../PROTOCOL.md:63–68`, fleet HEAD) carries "dispatched is still the lane" + "only a
non-author may write `[x]`"; the whole range is needed, and two lane files cite the same range.
Ord 1 (`executor-test-sufficiency.md:160–184`) has the one-mutant sentence at `:160-162` and the
n=1 "not a full cold-read" limitation at `:165-166`, all inside the range.
Ord 2 `SHONEN.md` is the live 4-box checklist; ord 3's `#box-1` anchor exists at `:71`; ord 4's
`Admitted (corrections)` `:106` and `Rejected, with reasons` `:114` are both present.
All five excerpts pass the counter's own `norm()`/`pointed_text()` test (24–400 chars) and its
`check_reads()` aggregate is zero on every miss counter (receipt `T49Read13.excerpt-check.txt`).
No proposed fixes; the section's 5 pointers are exactly its frozen floor, so keep all five.
No counter run, no probe verdict, no tooling installed; scratch removed.
Artifacts: `T49Read13.rows.json`, `T49Read13.excerpt-check.txt`, this file.
