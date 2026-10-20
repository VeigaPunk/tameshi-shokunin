# CRCritic2 — falsifying the C2 cold-read protocol (round 16, wave 1)

Seat: TameshiR16.CRCritic2 (critic). Scope: the C2 protocol only: the partition, the verdict vocabulary, the contamination rule, the strictest-wins ledger and the sha-matching rule in `measure.py`. I judged no seat and edited no file. My only write is this report. Scratch: `/tmp/tameshi-r16-CRCritic2-PGmF/` (`snap.md` and `sim.py`). Installs: none.

Evidence base:
- I hashed and parsed the snapshot.
- I read the wave spec `.ufo/waves/round-16/spec1.json` (the seat prompts).
- I parsed the JSON blocks in the 16 CR reports that had landed at about 10:30.
- I searched the CR seat transcripts (`history://TameshiR16.CR*`) for the paths that seats actually touched with tool calls.

Times are from this wave. Reports were still landing while I worked.

## Axes
- **A1 coverage.** Every partition unit gets a credited verdict that means what box 3 says.
- **A2 independence and contamination.** No seat sees expected answers, sibling output or oral context.
- **A3 verdict soundness.** The verdict follows from the evidence, and replicas merge soundly.
- **A4 carry-over soundness.** The sha rule credits only bytes that were actually read, in the context where they now sit.
- **A5 truthfulness of the claim text.**

## Baseline facts (observed)
- `sha256sum SKILL.md .ufo/evidence/round-16/coldread/SKILL.snapshot.md` printed `97cf436b…3580` for both files, and `cmp` exited 0. `git show HEAD:SKILL.md | sha256sum` gives the same hash, at HEAD `28aeef4`.
- The file does not end with a newline. `wc -l` reports 1704, but `split('\n')` gives 1705 lines. The last line is `exits0/1/2 for pass/case failure/setup inability and64 for invalid invocation.`
- `grep -n '^#'` returns 54 lines. Four of them (549, 552, 618, 621) sit inside fences 542–555 and 610–624. That leaves **50 headings** at levels 1–3. There are no `####` headings, no tilde or indented fences, no duplicate headings and no carriage returns or tabs.
- **There are 51 partition units: the preamble (lines 1–5) plus 50 headings.** All 51 section sha256 values are distinct (golden table at the end). CR05 computed its own section hash `4d8dd8db…`, which matches my table.
- Seat ranges from `spec1.json` cover lines 1–1705 contiguously with no holes: 30 seats over 27 ranges. Only three ranges have a replica seat: (131–245), (527–593) and (594–667).

## Findings — counterexample · evidence · axes · smallest safe correction

**F1. "50 sections" in the claim does not match the 51 units the tooling counts.** (A5; fixable)
- C2 says "50 sections". The CR01 prompt asks for a preamble entry (start 1, heading `""`), and the CRMeasure spec says "preamble + every #/##/### heading", which gives 51.
- A ledger with 50 entries fails `box3_full_page`. A claim reading "50/50" misstates what was measured.
- Correction: state the claim as 51 units (50 headings plus the preamble), and make the measure print `total=51`.

**F2. The contamination rule contradicts itself on page-named forbidden paths, and the contradiction is already live.** (A2, A3; fixable)
- The rule allows "any file … your range explicitly names" and also says "Never open … plans/, reports/, corpus/lessons/, SHONEN.md, LOG.md, SCORECARD.md".
- The snapshot names forbidden paths 28 times across 15 sections: lines 19, 49, 331, 340, 411, 462, 684, 763, 803, 825, 1001, 1262, 1367–1394, 1440, 1466–1477, 1512–1513, 1521, 1565 and 1612–1613.
- Transcripts show seats resolving the conflict towards opening the file:
  - `history://TameshiR16.CR08:77` ran `sed -n '1,16p' plans/round-3.plan.md`.
  - `CR06:73` read `plans/round-2.plan.md:1-12`.
  - `CR14:59,69,113` read `plans/round-6.plan.md`.
  - `CR17:94` read `plans/round-7.plan.md:1-25`, and `CR17:60` ran `grep … -r tools/ corpus/ plans/`.
  - `CR27:95` ran `ls … corpus/lessons/`.
  - `CR02:92-99,116` opened `kaidoku-shokunin/SCORECARD.md` and `.ufo/waves/kaidoku-r5/…`. The rule does not say whether its path list covers only this lane or sibling and fleet trees too.
- CR08 did list the plan file in `opened`, so it was honest. The problem is the rule, not the seats.
- Correction (one sentence in the wave-2 context): "The never-open list wins. A claim cluster whose only anchors are on that list is recorded in `minor_gaps` as `anchor-barred:<path:line>`, without opening the file. The list applies to tameshi paths only, and sibling-lane anchors named by the page may be opened."

**F3. A record section can pass vacuously when its central claim is barred or superseded.** (A1, A3; fixable)
- Counterexample: section 1464, `## Promotion-evidence calibration — fleet round-1`.
  - Line 1472 says "Box 3 remains `[ ]`".
  - Line 1512, in the next section, says "box 3 currently carries a scope-bounded `[~]`, not `[ ]`".
  - At HEAD, `SHONEN.md:9` reads `- [~] Instructions executable by an agent without oral context`. I read it as a critic, not as a seat.
- CR24 had both lines in range and returned `1464 record verified-record we=0`. It verified only the allowed anchors (`PROTOCOL.md`, `executor-test-sufficiency.md`). Its single minor gap says the box state "cannot be re-checked from the page alone".
- So the in-page contradiction (1472 vs 1512) earns credit for 1464 and is never flagged.
- Correction:
  - `verified-record` requires that the section's *headline* claim was checked. If that claim is barred, the verdict is `gap-minor` with `anchor-barred`.
  - Any claim contradicted elsewhere on the page is `wrong-expectation` unless the page itself marks it as superseded. Line 1511 does mark it: "Calibration correction to the historical promotion paragraph above". In that case the seat records `superseded-by:<line>` in `minor_gaps`.

**F4. The vocabulary does not say at which revision a record is checked, so seats will diverge.** (A3; fixable)
- Many records carry measurements at old revisions. For example, line 1412 reads "4 × `current` · 2 × `stale`".
- Today CR22 observed "current=3 stale=3" (`history://TameshiR16.CR22:85`) and chose to read the drift as "the reading map working as documented, not a defect".
- Another seat could just as easily mark the same drift `wrong-expectation`. With strictest-wins, that one seat's choice decides box 3.
- Correction (one rule): "Check a record at its recorded revision via `git show <rev>:<path>`. Drift since then goes in `minor_gaps`. Use `wrong-expectation` only when the page asserts a *current* outcome or the recorded-revision check fails."

**F5. Seats choose the instruction/record label themselves, and mixed sections get the easier label.** (A1, A3; fixable)
- CR08's minor gap says: "section is mixed record+imperative-rules; classified record".
- CR24 labelled `### Gate/probe registry` (1499) as `record`, although every row of that table has an Entry command and a Self-test command.
- A `record` label needs only one anchor per "claim cluster", a term the context never defines. So the label lowers the bar the seat has to clear.
- Correction:
  - In the assembler: if any seat, or a mechanical signal, marks a section `instruction`, the class is instruction. Signals: a code fence, a backticked command starting `bash `/`node `/`python3 `, or numbered imperative steps.
  - A section in the instruction class whose verdict is `verified-record` becomes `not-executed`.
  - Define "claim cluster" as one bullet, table row or paragraph.

**F6. Verdicts are not derived from the gap lists.** (A3; fixable)
- In the 24 landed entries, 14 carry an `executed-ok` or `verified-record` verdict alongside a non-empty `minor_gaps` list: CR07, 08, 09, 11a, 11b, 17, 19, 20×3, 21, 24×2 and 25. CR11a's minor gap says "inferred FAIL-prefixed case lines", which by definition makes it `gap-minor`.
- In a replica merge, gap-minor outranks verified-record and executed-ok, so a seat's self-chosen label decides the merged result.
- Correction (in the assembler): effective verdict = the strictest of the declared verdict and the verdict derived from the lists, where a non-empty `wrong_expectations` derives `wrong-expectation`, a non-empty `blocking_gaps` derives `gap-blocking`, and a non-empty `minor_gaps` derives `gap-minor`.
  - Set `blocking_gaps` and `wrong_expectations` to the union of counts across seats, not the counts from the winning seat alone.

**F7. Replicas can disagree about which experiment they ran, and the merge cannot see it.** (A3; fixable)
- CR04a materialized the pinned blob `git show 175de6ba` (43/43). It re-registered D1–D10 from the note's manifest, marked those predictions "informed" (`CR04a:98`), and added blind mutants X1 and X2.
- CR04b ran `cp -p` on the *working-tree* `kimi-census.mjs` and got 45/45 ("suite grew 43→45", `CR04b:87`). It ran 11 new mutants and got 10/11 killed (`CR04b:120`).
- Strictest-wins then merges two incomparable experiments. Nothing in the ledger schema records the target.
- A recipe replica that only replays a recorded manifest is also not a test of whether the page can be executed blind.
- Correction:
  - Add `target` (`repo@rev:path`, blob sha) and `informed_by` (paths opened before the predictions were registered) to each seat's section entry.
  - The assembler flags a replica pair whose targets differ as `replica-incomparable`, and L1 must resolve it in writing.

**F8. Only 3 of 51 sections have a replica, so seat reliability is not measured anywhere else.** (A3; tradeoff)
- 48 sections rest on a single seat. With one seat, strictest-wins is the identity, and a lenient seat cannot be caught.
- The largest single-seat section is 668–793 (9,407 B, CR13).
- Correction: wave 2 adds one independent seat to a sample of k ≥ 5 credited sections.
  - Choose the sample *after* the wave-1 ledger is frozen, by the lowest values of sha256(section_sha ∥ ledger_sha). L1 cannot steer that choice.
  - Report agreement as x/k.

**F9. A partition by sections cannot see incoherence across the page.** (A1; fixable, and it bears directly on the "full-page" claim)
- Lines 9–15 still say "Two mutation cases are now measured … complete reproduce specs for both cases". The page now records six cases, and C1 adds a seventh.
- CR01's range is 1–57, so CR01 cannot see this. The same applies to the 1472/1512 contradiction (F3) and to the overloaded `:NNN` anchors (F11).
- A union of 27 range-bounded reads is not a cold-read of the full page.
- Correction: wave 2 adds one whole-page coherence seat.
  - It reads all 1705 lines, executes nothing and returns one entry per section, plus a `page` entry listing contradictions, stale summaries, superseded claims and broken anchors.
  - It must have no wave-1 exposure.

**F10. Contamination routes that `opened` cannot catch.** (A2; fixable)
1. **Sibling scratch directories.** I counted 63 directories matching `/tmp/tameshi-r16-*`, all owned by the same uid (`vgpnk`), so mode 700 does not protect them. `/tmp/tameshi-r16-CR11b/` contains `pinned.mjs` and `work/`, and `/tmp/tameshi-r16-CR04a-1/work` exists too. Replica pairs can read each other's results. I saw no evidence that any seat did.
2. **Wave reports while they land.** Several seats listed the forbidden directory with `ls -la .ufo/waves/round-16/w1/`: `CR02:45`, `CR10:45`, `CR21:45`, `CR05:89`, `CR22:86` and `CR17:126`. Listing exposes sibling report names and sizes. Wave-2 seats would see the very wave-1 verdicts they are meant to re-check.
3. **Git bypasses the path rule.** `git show HEAD:SCORECARD.md`, `git log -p` and `git grep` read barred content without "opening" the path. CR14:61,71 already ran `git log --all` in the lane repo. Commit subjects such as `28aeef4 round-15 verifier spot-check … admit/reject` are verdict text.
4. **Oral context in the prompts themselves.**
   - The shared Goal tells every CR seat the outcome that is wanted ("so SHONEN box 3 … is earned").
   - Per-seat prompts embed method hints: CR11a's "(pin, uniqueness, control, all defects, verdict table, survivor probes, restore proof)", CR16's "(e.g. run the regression it names)" and CR24's "(e.g. selftests)".
   - For a test of "executable without oral context", that hint text *is* oral context.
5. **The working-tree instrument moves during the wave.** My first `git status --short` showed ` M tools/mutate-and-run.sh`. Later checks found the content sha equal to HEAD (`75ed934d…`) and `git status` clean, so the modification was transient.
   - RGLeg owns that file this wave, and seats read and run lane tools from the working tree (`CR17:61` read `tools/mutate-and-run.sh:60-215`; CR24 ran `python3 tools/repeat-control.py …` from the lane root).
   - A wave-2 `--regression` run against the working tree after the `js-round-gate` leg lands would run round-gate mutants. That could break C1's rule that predictions are registered before any mutant runs. [INFERENCE: depends on timing.]

Correction for F10 (all of it goes in the wave-2 prompt; no new tooling):
- Use a byte-identical generic prompt for every seat, with no Goal or claim text and no per-seat hints. Only the range and the report path differ.
- Forbid `ls`/`find` over `/tmp/tameshi-r16-*` except the seat's own directory, and over `.ufo/waves/`.
- Run lane tools only from `git show 28aeef4:tools/<f>` materialized into the seat's scratch.
- Forbid `git log -p`, `git grep` and `git show <rev>:` against the barred paths.
- After the wave, L1 searches each `history://TameshiR16.<seat>` for tool calls that touch barred paths or sibling scratch. Transcripts are readable: `history://` lists every seat, and a search of `TameshiR16.CR08` returned line 77. Contaminated entries are tagged `contaminated:<line>` and excluded from credit. Self-reported `opened` is not enough: CR11a's `opened` lists 2 paths even though it authored `mutate_driver.py`, while CR11b's `opened` lists its authored files.

**F11. The sha rule keeps credit for sections whose line anchors went stale.** (A4; this is a defect the judge must reject)
- The page uses `:NNN` to point at its own lines. Line 1296 states the convention: "(Anchors `:…` are this page; the others are repo-relative)".
- A crude scan counts 85 `:NNN` references in 27 sections. The scan over-counts: line 166 uses `:155-166` to continue a note citation, and lines 1307, 1328, 1331 and 1628 cite tool lines. So the convention is also ambiguous, which is a cold-read gap of its own.
- I checked 12 references where the target content confirms they point at this page: 1384→`:1294-1297`, 1386→`:1246-1270`, 1400→`:1021-1053`, 1415/1232→`:1069-1090`, 1419→`:1230-1244`, 1443→`:131`, 1445→`:965-1008`, 1453→`:1017-1019`, 1456→`:1359-1363`, 1162→`:1019` and 1025→`:14`.
- Counterexample (`python3 /tmp/tameshi-r16-CRCritic2-PGmF/sim.py`, exit 0): insert 2 lines in place at line 240 to repair the recipe.
  - Only one section sha changes (131). The other **50 keep their credit**.
  - **10 of the 12 confirmed self-anchors now resolve to the wrong text.** For example, `:1246` used to point at `### The service's limits — …` and now points at `  assumed.`. `:965` used to point at `### Reading a receipt — the discipline` and now points at `  case set is tameshi-carried at this revisio…`. Only `:131` and `:14`, which come before the edit, still match.
- So in-place repairs keep stale verdicts credited on sections whose bytes did not change but whose instructions now point at the wrong lines.
- Correction (choose one):
  - (a) After any repair, a mechanical anchor check: for every page-referencing `:N[-M]` in the new SKILL.md, compare the target's first line with the snapshot's target at the shifted position. Any section with a mismatch drops to `needs-reread`.
  - (b) Repairs must keep line counts unchanged above line 1464, the first line after the last confirmed self-anchor target.

**F12. Append-only errata can never clear a blocking gap under the sha rule.** (A4, A5; a tradeoff L1 must pick explicitly)
- The page's own rules are "Errata append-only" (line 24) and "nothing above this section was edited by this write" (line 1460).
- Simulation: append `## Errata — round 16` at the end of the file.
  - The recipe section's sha does not change (`recipe sha unchanged: True`), so a `gap-blocking` entry keyed to that sha blocks `box3_full_page` for ever.
  - The last section (1676) *does* change sha, because the file has no trailing newline and any append adds a blank line to it. Its credit is lost too.
- So the protocol forces an in-place repair. That breaks the page's own append-only rule and triggers F11.
- Correction: decide this in writing before wave 2. Either
  - allow in-place repair as a declared exception to line 24, with F11(a) required; or
  - let the ledger key a section's credit on (section sha, erratum sha) via a `repaired_by` field, with the re-read seat reading both.

**F13. The ledger can be trusted without checking the reports behind it.** (A4, A3; fixable)
- `measure.py` takes `box3_full_page` from `ledger.json` at REV. The `--override FILE` option lets L1, the claimant, replace the strictest-wins verdict by giving free-text reasons.
- The seat reports under `.ufo/waves/round-16/` are untracked: `git status` shows `?? .ufo/waves/round-16/`. At REV the provenance cannot be checked.
- The `seat` field is self-declared and inconsistent: `TameshiR16.CR08` sits next to `CR05`.
- Correction:
  - Commit the reports with the ledger.
  - `measure.py` re-derives each entry's verdict from the cited reports' JSON at REV, using the F6 rule, and fails if the result does not match.
  - An override may only lower `gap-blocking` or `wrong-expectation` when it cites a wave-2 entry on the *new* section sha. Free-text overrides are counted, never credited.
  - Normalize seat names to the roster id.

**F14. Most of the credit can come from records.** (A5; tradeoff)
- Landed so far: 12 instruction entries (7 `executed-ok`, 2 `gap-minor`, 3 `wrong-expectation`) and 12 record entries (10 `verified-record`, 2 `gap-minor`).
- Box 3 is about *instructions*. A pass in which about half the units were anchor-checked records is not "the full page executed".
- Correction: phrase the box-3 evidence as "I instruction units executed (gap-minor g) + R record units anchor-verified, 0 blocking". Do not write "full page executed".

## Minimal wave-2 changes (ordered by leverage)
1. Write the claim text as 51 units (F1).
2. Make the never-open list win and add an `anchor-barred` minor-gap tag (F2). Specify that records are checked at their recorded revision (F4).
3. Add the derived verdict, class dominance and union counts to `assemble.py`; add `target` and `informed_by` fields to the seat JSON (F5–F7).
4. Use one generic, byte-identical seat prompt: no Goal, claim or hints; the instrument comes from `git show 28aeef4:`; no listing of `/tmp/tameshi-r16-*` or `.ufo/waves`; L1 searches the transcripts afterwards (F10).
5. Re-read seats are fresh agents with no wave-1 exposure, and the brief must not describe the gap or the fix. If CRSentinel's /tmp substitutions are needed, they go into the generic contract, not into section-specific hints.
6. Add one whole-page coherence seat (F9) and a k ≥ 5 replica sample chosen after the ledger is frozen (F8).
7. Choose between in-place repair with the mechanical anchor check and erratum-keyed credit, and do it in writing (F11, F12).
8. Commit the reports, have `measure.py` re-derive verdicts from them, and limit overrides to wave-2 evidence (F13).

## Weaknesses of the sha-matching rule (summary)
- **Context blindness (F11).** Credit for unchanged bytes survives even when their self-anchors shift.
- **Append-only incompatibility (F12).** Errata cannot clear a gap, and any append resets the last section's credit because the file has no trailing newline.
- **Parser divergence.** On this snapshot, a parser that toggles fences only on exact lines equal to `` ``` `` (so `` ```bash `` openers are ignored) finds **23** sections. A parser with no fence handling finds **55**. A parser matching any `^#` finds the same **51** shas today, but would diverge on the first `####` heading a repair adds.
  - `measure.py` (CRMeasure) and `assemble.py` (CRLedger) are written independently. Both must reproduce the golden table below on the snapshot. Without that check, a mismatch looks like "missing coverage".
- **Matching on the section sha alone** ignores `skill_sha256`, `start` and `heading`. An entry from any SKILL revision credits identical bytes anywhere. Today that is harmless because all 51 shas are distinct. It becomes unsafe if a repair duplicates a block such as a registry table.
- **No proof of what a seat read.** Seats copy `skill_sha256` from the prompt. Require each seat to report `section_sha256` computed from the bytes it read, and have the assembler reject mismatches. CR05 already did this voluntarily: `4d8dd8db…` matches.

## Golden partition (snapshot `97cf436b…3580`; sha = section text joined with `\n`, no trailing newline)
| start | end | sha256 |
|---|---|---|
| 1 | 5 | 955cabcd17dfc19221531a2b2c45528d2594c30426c81f9fedc5cb5e91ef7885 |
| 6 | 16 | 1beb22ed3fd1644961ae905b0c1de1b1dd61db41b7b4f7fa2d045f0394eaced1 |
| 17 | 29 | 5e15f9fba40102f04d479f3d802338991a066d1fc27dc4658cb51c15498662d6 |
| 30 | 57 | a4b0d789df3f817338d085dca6c50c0ccff9cebcc25cbe95a046fd2e5fac00f4 |
| 58 | 93 | 7f67dde7b169a15d3b4d89baa1ac4a4d8b6c211a271ba9cc8ee0aabe5810b675 |
| 94 | 130 | 6cd8ff289fcb4ee072c9f991ef7cd090384c7cb9bcaf90393281d07b67bcb70e |
| 131 | 245 | ef7a8469b49984615e6308bdcc92a3258f9aaf222241093ef88aa3e31670bccc |
| 246 | 313 | 4d8dd8db1bb3c05175a22a94a95ba151fb35a6b4a3f50c3cb88ed1fdf2a77df0 |
| 314 | 374 | c529131f8689f437d135a1bda71cd03e9519519485114c48e70f8755c4964ec1 |
| 375 | 404 | 9425ce5f1f860a0094906dd3b022aaec657316abdd51fee324ffe2d8424b992d |
| 405 | 465 | bfb5db4fcdcf8ef7b0de00bac29d743b3627ebf1d8f12589d86182f51db9c1f6 |
| 466 | 496 | 335fb62193390692f4bfc4c96560d4332c3dc3cf6f4ba2caf6ccf975a078a90b |
| 497 | 526 | df288197365105924026f297724cc0bc5e4aade05a0d2e4e980249ed26fa4e31 |
| 527 | 593 | 838ea53d5a9ead4889a1e5d8269e32dee1d98ec83e149e1433e4de776b7c8cd3 |
| 594 | 667 | a5816f8ddebe02ae2a6dcf66cd7a17d8cced4276f56f53e227fab073abaf4ac6 |
| 668 | 793 | db541dd3b625e0acb2e2632c1b3c2879c6ed9148b395e3f0c19f13d8bc84eccb |
| 794 | 805 | e328005d028625acdaadfed11de75d53bcf926c5b455d38d3def67d698a021e8 |
| 806 | 826 | 92e007065c449c20293f6aa57bbf0fb5ed85375f54fb5e248481cb1da4f8698e |
| 827 | 857 | 679ef7dec80c3a89358a006ef59baec3875dcd53f62b0c24c376b1e2eed18dc3 |
| 858 | 882 | f10dc05de0cbb6180f83008d6c100cf65645bbb14ec2cb1db823e85f86d41ce5 |
| 883 | 898 | b4188f00e377af7339f30feb440a99bf8b5ad8f2cb92becfe6faf0a669b32d2e |
| 899 | 920 | bfb5742faf7f0bc9029f5e74a1be65e494013b0f3e0d91a6bfd304cfb42ed14d |
| 921 | 932 | 2dca8a047b3797eb6d8ae81a731643204a2b58e8151baf2661c1915faeaf0089 |
| 933 | 964 | e787150a962c011a617763f337c9d23951188c390e568dda3c5c5c865dc50b4f |
| 965 | 1009 | 2da3ff3c20925a71653ee35ffca7fd3ff41479c04dd986694ec04a510a03f077 |
| 1010 | 1020 | 6a974ef991fac80f229537aedb03581e6668a1d8d650d45efc1c3f6809b3963b |
| 1021 | 1068 | b56dda9841162826aab96f6f28b429d01b3bc3ecae7cae2f57539c79ebe1458e |
| 1069 | 1091 | 04ca4d84cf4d4e05e91a0ba6dd39a4f217e94de86a10c24af111fd4a1242eba1 |
| 1092 | 1154 | 4d1ce01475895139271d5bb7d114c3100132aeb9ba2f1f7c46d6c1d4c57aae0e |
| 1155 | 1163 | 7d198f592df3ad14c2983a952937f63ae2223757c6796c23619599af3e29283d |
| 1164 | 1211 | daf609693bba1f7ea290ac44650a0f88d5e269aa9c75045b50d4f73004583784 |
| 1212 | 1229 | 39b3147bee4c820f94d259566e043ff0a8195d9b3c0053b42d87c7aa2dab12b8 |
| 1230 | 1245 | 22e828f50b3e3ce92e9e500a3ead897308e8ad99e5f3bf3d6747784f59c71c15 |
| 1246 | 1271 | 78c388d56f93442faf97f7aeec136aac9c35cfa6ca4d1488c77ea6450e4cb7b9 |
| 1272 | 1280 | 1e567a17aa6c7198c12f1a92749dc20f59ee65426d4e3aeb8e39b666dc7cf296 |
| 1281 | 1301 | 371b21b5044810d2d2b71e393dc050d34bcb26a625d5b5691548e1f574360e97 |
| 1302 | 1364 | d97640cfbff5719c966128e7c97ad1a9c4f23a6dd707f7dc77b6681b6eb031c2 |
| 1365 | 1379 | de5d5d14fc374dbba2a01bd549e966b0201b41f47542556cce701c0ee9a0d075 |
| 1380 | 1395 | fe758fad7663ec47056824d321f8f241b433f9210d01fc1012d5ebdba446d9d9 |
| 1396 | 1435 | 21ea5b1c77646e4d00bdc8a597565786e69718573cfb0fe76151aa80e9429247 |
| 1436 | 1448 | 2ba412c85cc5524f1588ca9e9520ff018837998042e6bbd6f13ad27b0cd06a6c |
| 1449 | 1463 | 13eff75a60c3c5a3091ba5232d803343c81cb63e57345a0b4fa0ff22ab26de8b |
| 1464 | 1478 | 2f26fc4888ab813d79bce4aed3cea7f1659ea134d1278fb152a11b0618be2452 |
| 1479 | 1498 | 986090c11485970b4789b10dc5e13b1202ebbd324446b8be71239d94c500e08d |
| 1499 | 1516 | 546acd6964fe2feeb243bc2cc5102de57a9806099b7b50c7e5cf0d50d75be7b8 |
| 1517 | 1547 | 0fc644b0c1613c873b9debd0749d7bcd37758939ef452d6a03e4096098189ccc |
| 1548 | 1562 | 169f0e28b9a5939f3fd09722d2de31cd8e5be26b9804050bb7838448f71fb6e4 |
| 1563 | 1596 | 32ff8ebc99e310b58ac014302a1e1e6cf51ad7f12c357cc9b902eab6b6c6e038 |
| 1597 | 1608 | 96d72d9fb9a55e963b73161d2dafb2fa1055f1eafd7b20f1d9c9b951d267a657 |
| 1609 | 1675 | baa873df7cfb686bc6886a30cdcfb2702ce2357cf4c4c68a5cbd8a6d9583922d |
| 1676 | 1705 | 7544ca6940553ecd2adca2d1d9d6571b4a55f0ad191013507ff4d7bd14b32dde |

## Commands (exit 0 unless noted)
- `sha256sum SKILL.md …/SKILL.snapshot.md`, `cmp` (exit 0), `git show HEAD:SKILL.md | sha256sum` and `git status --short`, run in the lane root.
- `grep -n '^#'` and `grep -n '^```'` on the snapshot. Parse plus sha scripts in Python, using the stdlib only.
- `/tmp/tameshi-r16-CRCritic2-PGmF/sim.py`: variant parsers, the in-place repair simulation and the erratum simulation.
- Python scans of `spec1.json` and of the landed `w1/CR*.md` JSON blocks (16 reports; 23 of 51 sections covered at the time).
- `grep` over the `history://TameshiR16.CR*` transcripts with the pattern `^→ .*(LOG\.md|SCORECARD\.md|SHONEN\.md|plans/|reports/|corpus/lessons|\.ufo/waves)`.
- `stat -c '%A'` on the replica scratch directories, and `grep -n '^- \[' SHONEN.md` (critic read only).

Not run: any mutant, `assemble.py`, `measure.py`, or any lane tool.
