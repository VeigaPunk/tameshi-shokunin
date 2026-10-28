# T56W3ScribeLessonFinal — final lesson text, tameshi round 56 attempt 3

Seat: `T56W3ScribeLessonFinal` (leaf scribe, wave 3). Milestone: final lesson text. Judged on: calibration.
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. PIN read: `2f5512a8ab0771fb2eee463ec16db359174f5edd`. C0: `c0137451f5b7f22d65f748fc69f1b181f55e1378`.

## What this seat did

- Read the wave-1, wave-2 and integration receipts on disk, and the wave-3 controls receipts.
- Re-read both source pages from the raw URLs with the `read` tool on 2026-10-28 (S281 and S282; DSSE was not re-read, the L1's record is cited for it).
- Ran read-only commands only: `git status --porcelain`, `git diff --stat`, `git show`, `git ls-files`, `git ls-tree`, `git cat-file -e`, `git log`, and the census validator `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` (exit 0, output in scratch, scratch removed after writing).
- No counter, control, binder or deciding script was run. No lane file, frozen instrument, bound ledger or git state was changed. No tool was installed or upgraded (none needed; pacman untouched).
- The lesson text below is not yet committed. `corpus/lessons/round-56.md` at HEAD still carries four `<L1 fills>` markers; the working-tree copy differs from HEAD by five lines. The L1 commits the text below verbatim, after reconciling the tree (finding 1).

## Findings (calibrated; receipts named)

1. **Blocker for the deciding run: the lane tree is not clean at PIN.** `git status --porcelain` at `2f5512a` = 30 entries: 20 tracked modifications and 10 untracked. The modifications are `.ufo/evidence/round-21/coldread/ledger.json` (36 lines), `.ufo/evidence/round-21/coldread/rekey-r56-c0137451f5b7/traces/section-01..18.json` (argv rewritten from relative to `/home/vgpnk/Projects/shokunin/tameshi-shokunin/...`), and `corpus/lessons/round-56.md`. In the ledger, 18 `L1 TameshiR56a3 re-key` labels read `L1 TameshiR56 re-key` in the tree; HEAD has 18 `a3` and 0 plain. `deciding-run.sh` lines 129–132 and 164–165 refuse any status line not under the run's OUT directory, so this tree would refuse. The counters read committed bytes at `--rev`, so this does not change a PIN verdict; it blocks the deciding run. Reconcile before the deciding run; I did not touch anything.
2. **Controls at PIN are running, with no verdict on disk yet.** Processes `controls.sh <lane> 981c5e8b… 2f5512a… 21eb3c63… …/T56W3ExecControlsA/out` and `…B/out` were running when read; `T56W3ExecControlsA-receipts/controls-a.stdout` and `…B-receipts/controls-b.stdout` each contain only the header line `# phase A: do-nothing and mutation controls (expected false unless stated)`. The C1 run at PIN (`T56W3ExecC1Run`) was also in progress. The lesson therefore states no control or deciding verdict.
3. **Bootstrap**: the first phase-B run is expected to report `own-receipts-missing` / `CTL_POS_c2=false` (as the contract's bootstrap note says); the L1 commits that actual output, then reruns the frozen script at the resulting PIN. Not done here.
4. **Wave-3 bound-ledger verifiers (`T56W3Led01`–`Led18`) and the post-bind falsifiers have no result files on disk** (`.ufo/waves/round-56/w3/` holds only the two controls directories and `swarm-registry.json`). Nothing in this report or the lesson is attributed to them.
5. **Sources re-verified.** S281 quote matches the raw page at `### subject` ("IMPORTANT: Subject artifacts are matched purely by digest, regardless of content type.", 11 words). S282's corrected `## Model` sentence matches the raw page (20 words). The attempt-2 S282 quote is absent from the page (`T56W2RevSources-receipts/01-lesson-s282-quote-vs-source.txt`, `grep_exit=1`). The lesson uses the corrected quote.
6. **Census**: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0; `tameshi ok …/corpus/SOURCES.md`; 1 `ok`, 1 `W01`, 15 `W04`; `grep -cE '^ {0,3}\| S[0-9]{3,} \|' corpus/SOURCES.md` → 142. S281 mined, S282 rejected and retained.
7. **HEAD lesson placeholders**: `git show HEAD:corpus/lessons/round-56.md | grep -c 'L1 fills'` → 4. Fixed in the text below: no unfilled marker remains; the string appears only in two descriptive lines of the Mistakes entry (checked after writing this file: 2 matches in the lesson text, both descriptive).
8. **Counter attacks recorded in the lesson** (no new attack run by this seat): C1 fabricated-hash bind `total=0 C1_R56_PASS=true` (`T56W1CritC1-receipts/fabricate.txt`); C2 rewritten-`rev=` real receipt `own=PASS docs=4/4 total=0 C2_R56_PASS=true` (`T56W2CritDoNothingC2-receipts/v3-rewritten-slice.stdout`); C2 null-tree `own-receipts-missing … total=1 C2_R56_PASS=false` (`v1-c0-baseline.stdout`). The C2 do-nothing control reaches its target (claim-sizing failure): the target is not admitted as improvement evidence.

## Items this seat did not verify

- The deciding-run verdicts for C1 and C2 and the controls verdicts (not on disk).
- Whether `deciding-run.sh` gate 0b/0c refuses at PIN (not run).
- The R55.7 claim that the 14 deleted `T55W1MutC2-receipts` files are restored by name (the spotcheck does not list them).

## Command evidence (this seat)

- `git status --porcelain | wc -l` → 30 (at PIN, read at drafting).
- `git diff --stat` → 20 files changed, 92 insertions, 93 deletions (tracked).
- `git ls-files .ufo/evidence/round-56/before` → three paths (`before/c1.stdout`, `before/c2.stdout`, `before/c2-at-base.stdout`).
- `git cat-file -e 981c5e8b:<path>` → yes for all seven R55.6 files listed in the lesson.
- `git show 981c5e8b:.ufo/evidence/round-55/after/c2.stdout | grep -n C2_R55` → no lines (base copy carries no green C2_R55 line).
- `git ls-tree -r --name-only 981c5e8b -- .ufo/waves/round-55/w1/ | grep -c T55W1MutC2-receipts` → 101.
- Census validator, as above: exit 0.

## Lesson text (commit verbatim as `corpus/lessons/round-56.md`)

=== BEGIN corpus/lessons/round-56.md ===

# tameshi round 56 — lesson (hyaku run 11, 2026-10-28)

Attempt 3, L1 `TameshiR56a3`. Base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`
(`.ufo/evidence/round-56/contract.json`). The contract, both counters,
`tools/receipt-revision-gate.py`, `controls.sh`, `no-harm.sh` and `deciding-run.sh`
are frozen at the original freeze `c3e2ca9f020776b3d66c7af854fb82c834674fcf`;
`.ufo/evidence/round-56/freeze.json` records one pre-scoring amendment at operative
freeze `21eb3c63cd0f3190c0deeb8953c6c91c7742cd68` (amendment 1; targets, denominators
and arms unchanged). Content commit C0 `c0137451f5b7f22d65f748fc69f1b181f55e1378`;
content-final revision PIN `2f5512a8ab0771fb2eee463ec16db359174f5edd` (the C1 bind and
the restated calibration row). Deciding receipts go under `.ufo/evidence/round-56/after/`.
This lesson records what was on disk when it was written; it does not restate their
verdict lines.

The round answers round 55's non-author closure (`corpus/lessons/round-55-verifier-spotcheck.md`,
verdict `rejected-harmed`). It has two claims. C1 (R55.3): the eighteen headings round 55's
edits cost the cold-read monitor (64/64 score 8 → 46/64 score 6) are re-read at C0, bound
under one re-key directory, and the standing calibration row is restated to the score the
monitor reads at the commit it names. C2 (R55.5): the deciding gate must compare the revision
a receipt names with the revision it certifies. R55.1–R55.7 are dispositioned below.

## Gate (sources opened this round)

| S | URL | opened | quote (≤25 words, located) | verdict |
|---|---|---|---|---|
| S281 | https://github.com/in-toto/attestation/blob/v1.2.0/spec/v1/statement.md | 2026-10-28 | §Fields, `subject`, IMPORTANT paragraph: "Subject artifacts are matched purely by digest, regardless of content type." (11 words) | **admit, mined** — `corpus/knowledge/receipt-revision-binding.md` cites it for the receipt-to-revision binding: an attestation is evidence only for the artifact whose digest it names, so a receipt that names another revision is not evidence for this one. Tier A for the Statement v1 layer only; it says nothing about git receipts or DSSE. |
| S282 | https://github.com/slsa-framework/slsa/blob/main/spec/build-provenance.md | 2026-10-28 | §Model, first paragraph: "Provenance is an attestation that a particular build platform produced a set of software artifacts through execution of the `buildDefinition`." (20 words) | **rejected, kept as row S282** — the predicate says which build platform produced which artifacts; it does not say which revision a receipt certifies. Flip: the lane publishes signed build provenance for its own artifacts and needs `builder.id` and `buildType`. |

Snapshot and extraction: `.ufo/evidence/round-56/assimilation/in-toto-statement-v1.md`
(sha256 `cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea`, 2492 B; tag
`v1.2.0`, identical at `main` `50bf0171`). Both located quotes were re-read from the raw
pages on 2026-10-28. The first S282 draft quoted "Provenance is a predicate that describes how
a software build was executed."; that sentence is not on the page, and the row above replaces
it (see Mistakes, sourced quotation). A DSSE protocol candidate was screened out before a row
existed: its `SERIALIZED_BODY` row reads "Arbitrary byte sequence to be signed." and nothing in
DSSE requires the payload to name its subject digest (`.ufo/waves/round-56/integration/l1-source-reopen.txt`).

Census at PIN: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
exits 0: 142 rows, one `ok`, 16 warnings (15 W04 duplicate-URL notices, one W01 S101 tier-C
notice), no errors.

`considerthese/2026-10-28.md` proposal 1 (receipt-existence linter) is mined into `corpus/QUALITY.md`
criterion 107 for its revision half. Its quote half is declared unmined in that criterion's scope
paragraph; `.ufo/waves/round-56/w1/T56W1ScribeQuality-receipts/107-scope-gap-fabricated-line.txt`
shows the gap (a hand-written counter line with fabricated numbers passes the gate). Proposals 2–5
remain unmined.

## Mistakes

- **class: landing — the lane tree is not clean at the content-final PIN (the R55.6 class, recurring).**
  evidence: `git status --porcelain` at `2f5512a` (committed 17:52:41 local) lists 30 entries: 20 tracked
  modifications — `.ufo/evidence/round-21/coldread/ledger.json` (36 lines; the 18 seat labels `L1 TameshiR56a3 re-key`
  committed at HEAD read `L1 TameshiR56 re-key` in the tree) and `.ufo/evidence/round-21/coldread/rekey-r56-c0137451f5b7/traces/section-01..18.json`
  (each trace's `argv` path rewritten from relative to an absolute `/home/vgpnk/…` path) — plus
  `corpus/lessons/round-56.md`; and 10 untracked — `.ufo/waves/round-56/spec-w3.json`, `w3-dispatch.json`, `w3.ready`,
  `w3.ready.dispatched`, `w3/`, and five receipts under `w1/` and `w2/`.
  captured-by: `deciding-run.sh` lines 129–132 and 164–165 (`clean-tree-before/after`), which refuse any status line not under the
  run's OUT directory. Those gates have not fired; against this tree they would.
  fix: **open.** Before the deciding run the tree must equal PIN bytes, or a new PIN must commit the intended bytes. The counters read committed bytes, so this does not change a PIN verdict.
  red-before: the status listing above (`grep -vc` over it is non-zero, so the gate refuses).

- **class: closure contamination — bytes in the lane tree written by a process other than the lane's committing seat (the R55.7 class, recurring).**
  evidence: the `argv` path rewrite and the seat-label rewrite in the item above are both absent from the committed traces and ledger at `c1dd23b`/`2f5512a`
  (`git show --stat c1dd23b` lists the committed trace files). The writer is not recorded. `[INFERENCE]`: a re-run of the binder from another working directory, since
  the edits change only a path prefix and a label.
  captured-by: none at round time. Seen by `git status` and `git diff --stat` (20 files, 92 insertions, 93 deletions) when this lesson was drafted.
  fix: none this round. As with R55.7, the lane cannot fence a non-lane process inside its tree; the clean-tree gate is the only refusal, and the record is the diff.
  red-before: not applicable (no fix claimed). `git diff -- .ufo/evidence/round-21/coldread/rekey-r56-c0137451f5b7/traces/section-01.json` is the record.

- **class: landing — placeholder text committed.**
  evidence: HEAD's `corpus/lessons/round-56.md` contains four `<L1 fills>` markers (Gate header, census line, and the R55.1, R55.3 and R55.4 rows of the routed-defect table).
  captured-by: none; no gate reads lesson markers.
  fix: this text leaves no unfilled marker; each verdict-dependent cell names the receipt path instead of stating a verdict.
  red-before: `git show HEAD:corpus/lessons/round-56.md | grep -c 'L1 fills'` → 4. After: no unfilled marker; the three remaining matches in this text are the description above.

- **class: disposition before its receipt existed (the R55.4 class, repeated in the HEAD draft).**
  evidence: the HEAD draft says R55.4 "FIXED by construction" and R55.1 "FIXED by C2's deciding gate" while the receipts those rows lean on were not yet written. The wave-3 phase receipts `.ufo/waves/round-56/w3/T56W3ExecControlsA-receipts/controls-a.stdout` and `…ControlsB-receipts/controls-b.stdout` held only their header line when read at PIN.
  captured-by: the wave-2 critic and the claim-sizing rule; no gate.
  fix: the dispositions below claim mechanisms and name the receipt that will carry the verdict.
  red-before: the two header-only controls receipts (above).

- **class: attribution — `before/` receipts cited while untracked (caught inside the round).**
  evidence: `.ufo/waves/round-56/w1/T56W1ScribeLog-receipts/cited-paths.txt` reads `base=no freeze=no` for `.ufo/evidence/round-56/before/c1.stdout`, `before/c2.stdout` and `before/c2-at-base.stdout`, which the frozen contract's `before` fields cite.
  captured-by: wave-1 seat `T56W1ScribeLog` (finding 1).
  fix: C0 commits the three files. `git ls-files .ufo/evidence/round-56/before` now lists all three.
  red-before: `cited-paths.txt` (`freeze=no`). Green: the `git ls-files` listing.

- **class: sourced quotation — a located quote that is not in its source (S282), and a spliced sentence in the knowledge note (S281).**
  evidence: the attempt-2 `## Gate` row quoted "Provenance is a predicate that describes how a software build was executed." Its exact-string search against the fetched page returns `grep_exit=1` (`.ufo/waves/round-56/w2/T56W2RevSources-receipts/01-lesson-s282-quote-vs-source.txt`); the page's `## Model` first paragraph reads "Provenance is an attestation that a particular build platform produced a set of software artifacts …". The knowledge note's S281 sentence joins two passages with a splice (errata in `corpus/knowledge/receipt-revision-binding.md`, `## Errata — round 56 wave-2 re-open`).
  captured-by: wave-2 seat `T56W2RevSources` (findings F1–F3); the L1's source re-open (`.ufo/waves/round-56/integration/l1-source-reopen.txt`). QUALITY criterion 91 requires a located quote to be compared byte-exact; the check was not run on the drafted quote before writing.
  fix: corrected in the Gate above (the 20-word located quote, re-read 2026-10-28); the knowledge note carries an appended erratum rather than a rewrite.
  red-before: `grep_exit=1` on the false sentence. Green: the corrected sentence is the `## Model` paragraph of the raw page.

- **class: citation drift — page-local `:NNN` anchors in `SKILL.md` moved by this round's own +13-line insertion (and round 55's +4).**
  evidence: `.ufo/waves/round-56/w2/T56W2Read17-receipts/page-wide-sweep.txt`: 57 of 61 distinct line ranges no longer name the bytes they cite; the offset is +17, from hunks `@@ -44,0 +45,13 @@` (round-56 C0) and round 55's insertion. `.ufo/waves/round-56/w2/T56W2RevSkillScope.md` §3a counts 125 of 155 `:NNN` anchors moved by +13.
  captured-by: QUALITY criterion 34 (a citation into a moving file is anchored by a stable heading). No gate enforces it.
  fix: **not fixed this round.** A `SKILL.md` edit after C0 changes section hashes and invalidates the eighteen bound reader reports. Measured: one post-C0 line takes the monitor 47/64 → 46/64 (`T56W2RevSkillScope.md`). Round 57's first item.
  red-before: the sweep output (no fix claimed).

- **class: standing-rule table — a wrong refusal code in this round's own `## Standing rules` table.**
  evidence: row 1 maps `role=verdict` with a declared surface to `RECEIPT_REV_MISMATCH`. The gate selects the code by `--paths` and drift, not by role: on one receipt, `role=verdict` with `--paths` gives `RECEIPT_REV_CONTENT_DRIFT` (`.ufo/waves/round-56/w2/T56W2Read07-receipts/r10-F2-receipt-code-cells.txt`). The table also names 4 of the gate's 11 codes.
  captured-by: reader seat `T56W2Read07`, finding F2 (`.ufo/waves/round-56/w2/T56W2Read07.json`).
  fix: deferred to round 57 with the anchor repairs (a text edit now breaks C0 byte identity).
  red-before: the four invocations in `r10-F2-receipt-code-cells.txt`.

- **class: incomplete seat output — two wave-2 readers stopped before their Markdown reports.**
  evidence: `.ufo/waves/round-56/w2-results.json` rows `T56W2Read04` and `T56W2Read15` carry partial outputs; `.ufo/waves/round-56/integration/w2-resume-completions.txt`.
  captured-by: L1 at result intake (no `.md` beside the `.json`).
  fix: same-identity continuation, no replacement seat. Both now have `.json`, `.md` and receipts. The attempt-2 blocker (seven of eighteen reader reports absent at C0) is closed: eighteen root-level `w2/T56W2Read??.json` files exist and `integration/binder.stdout` ends `REFRESH rekeyed=18 skipped=0 headings=18`.
  red-before: the partial strings in `w2-results.json`; the seven-absent state recorded in the attempt-2 draft.

- **class: counter defects, fixed before any score — in `c2/measure.py` and `controls.sh`.**
  evidence: `.ufo/evidence/round-56/freeze.json` amendment 1: (a) C2 arm 6 read SOURCES' status column at index 8 (the opened date), so the knowledge-note cell could never score and C2 was unreachable; (b) `controls.sh` emitted clone-local commit SHAs as `rev=` tokens the gate cannot resolve, relabelled `clone_rev=`.
  captured-by: wave-1 seats, before any control score (stated in amendment 1).
  fix: amendment 1 (`cells[7]`; `clone_rev=`).
  red-before: for (a), `.ufo/waves/round-56/w2/T56W2CritDoNothingC2.md` F5 (the freeze-era counter scores the v2 tree `docs=3/4` and `C2_R56_PASS=false`). For (b), the amendment text is the only record on disk; no separate red receipt.

- **class: claim sizing — C2's target is reached by a tree that performs none of C2's work.**
  evidence: `.ufo/waves/round-56/w2/T56W2CritDoNothingC2-receipts/v2-stub-receipts.stdout` (line 16): two 79-byte stub control receipts naming C0 give `own=PASS docs=4/4 total=0 C2_R56_PASS=true`. `v3-rewritten-slice.stdout`: a real round-54 receipt with its `rev=077d431e6996` rewritten to C0 gives the same. The null tree fails (`v1-c0-baseline.stdout`: `own-receipts-missing docs=4/4 total=1 C2_R56_PASS=false`).
  captured-by: the claim-sizing rule (§9 do-nothing discriminator), and the counter's declared provenance blind spot (`contract.json` C2 `cannot_see`).
  fix: none this round. The counter and target are frozen after data; the measured C2 line is recorded and is not admission evidence for an improvement. A future claim needs a discriminator for control provenance.
  red-before: `v1-c0-baseline.stdout` (the null tree fails).

## Round-55 routed defects — dispositions (this round)

| id | disposition | evidence |
|---|---|---|
| R55.1 | **Fixed at the tool; the deciding-run path awaits its receipt.** Round 55 scored `4c04c1d3` with no C2 verdict at that revision, and its committed `after/c2.stdout` is truncated mid-run. `tools/receipt-revision-gate.py` refuses that receipt, and `deciding-run.sh` gate 0c applies the gate to the verdicts the run itself produces. | red: `.ufo/evidence/round-56/before/c2.stdout` `arm4-red55 exit=3 codes=RECEIPT_REV_ABSENT` on `.ufo/evidence/round-55/after/c2.stdout` (the file at base `981c5e8b` has no `C2_R55:` line). Green on the deciding run: pending `.ufo/evidence/round-56/after/receipt-gate-verdicts.stdout`. |
| R55.2 | **Carried; no instrument can fail it.** Quotes are checked by convention. QUALITY criterion 107's scope paragraph declares the byte-for-byte quote half unmined. | `.ufo/waves/round-55/w1/T55W1ScribeSkill-receipts/c2-integrated.out` (`total=1 C2_R55_PASS=false`, quoted as `total=0`); `corpus/QUALITY.md` `### Criterion 107` scope paragraph; `.ufo/waves/round-56/w1/T56W1ScribeQuality-receipts/107-scope-gap-fabricated-line.txt` (`GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS` on a fabricated line). |
| R55.3 | **Repaired at the bind; the monitor verdict is the deciding receipt's.** The eighteen lost headings are read at C0, bound under one `rekey-r56-c0137451f5b7` directory, and `SCORECARD.md` (`## Round 56 - calibration re-key…`, standing axis table) restates calibration at the commit it names (`c1dd23b`). | red: `.ufo/evidence/round-56/before/c1.stdout` `credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false`. Green at the bind: `.ufo/waves/round-56/integration/bind-precheck.stdout` `cand=c1dd23b3f83f cand_credited=64 lost=0 ok`; `binder.stdout` `REFRESH rekeyed=18 skipped=0 headings=18`. Verdict: pending `.ufo/evidence/round-56/after/c1.stdout`. |
| R55.4 | **Mechanism in place; the phase verdicts are not yet on disk.** Controls run from the frozen `controls.sh` (base, PIN and freeze as arguments); `deciding-run.sh` refuses without `CONTROLS_A:` and `CONTROLS_B:` verdict lines. | red: `.ufo/evidence/round-55/control/controls-a.stdout` was committed before the round-55 report that called `CTL_SKIP_c2` "still running", and reads `CONTROLS_A: 5/5`. At PIN the phase receipts were header-only when read (Mistakes). Verdict: pending `.ufo/evidence/round-56/control/controls-{a,b}.stdout` at PIN. |
| R55.5 | **Fixed in the tool and in QUALITY 107; the deciding path applies it to the round's control receipts (gate 0b).** Round 55's deciding gate never compared a `CTL` line's `rev=` with the revision under test. C2's gate now compares each receipt's `rev=` and digest sidecar with the certified revision, and `deciding-run.sh` gate 0b runs it over the control receipts. | red: `.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout` is refused with `RECEIPT_REV_CONTENT_DRIFT` and `.ufo/evidence/round-56/before/c2.stdout` records `red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE`. Gate selftest at C0: `selftest=19/19` (`.ufo/waves/round-56/w2/T56W2CritDoNothingC2-receipts/v1-c0-baseline.stdout`). Deciding receipt pending. |
| R55.6 | **Inherited files fixed and verified; the going-forward gate would refuse the PIN tree, so this is open.** The seven round-55 receipts exist at `981c5e8b`, and the sweep is in `6efd2a1`. The clean-tree gates now refuse a dirty tree, and the PIN tree is dirty (first Mistake). | red: the round-55 closure's `git status` (83 entries, seven round-55 files created before the 14:54:02 tip; `corpus/lessons/round-55-verifier-spotcheck.md` item 6). Green: `git cat-file -e 981c5e8b:<path>` succeeds for `w1/T55W1ExecRekeyPrep-receipts/{base,cand,floor,rekey}.json`, `w1/T55W1ExecNoHarm-receipts/coldread-at-base.json`, `w1/T55W1CritClaimShape-receipts/coldread-HEAD.json` and `w2/T55W2ScoutColdread-receipts/inputs.json`. Open: the first Mistake. |
| R55.7 | **Partly fixed on the lane side; the harness side is not fixed.** Base `981c5e8b` carries no green `C2_R55:` line in `after/c2.stdout`, and the tracked `T55W1MutC2-receipts` set is present (101 paths at base). `6efd2a1` changes 235 files, all insertions. The fourteen deleted files the spotcheck describes are not named there, so their restoration is not verified by name. The harness-side class recurs at PIN (second Mistake). | red: `corpus/lessons/round-55-verifier-spotcheck.md` item 7 (`C2_R55 … total=0 C2_R55_PASS=true` uncommitted; 14 tracked files deleted mid-closure). Green: `git show 981c5e8b:.ufo/evidence/round-55/after/c2.stdout` has no `C2_R55:` line. |

## What the counters cannot see

- **C1 — a tree-computed hash passes arm 4.** Arm 4 requires each reader report's `section_sha256` to equal the section's bytes at REV. Those bytes are computable from the tree without reading anything. Demonstrated by wave-1 seat `T56W1CritC1`: `.ufo/waves/round-56/w1/T56W1CritC1-receipts/fabricate.txt` prints `EXPLAIN arm4-readers 18/18` and `C1_R56: rev=d6fe899da135 c0=981c5e8b20a2 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true`. The hashes came from `round18.sectionize(SKILL_at_REV)` (`.ufo/waves/round-56/w1/T56W1CritC1.md` §3). The guard that remains is that the readers are honest, as the contract's `cannot_see` concedes. The strongest non-fabricated bind does not pass: wave-2 seat `T56W2CritDoNothingC1` reached `rekeyed=2/18 … total=6` (`.ufo/waves/round-56/w2/T56W2CritDoNothingC1.md`, row ctrl5).
- **C2 — a copied `rev=` token passes.** The gate binds the token to the certified revision, and the digest sidecar narrows it for the receipts that carry one. A real receipt with its token rewritten is still accepted: `.ufo/waves/round-56/w2/T56W2CritDoNothingC2-receipts/v3-rewritten-slice.stdout` gives `own=PASS docs=4/4 total=0 C2_R56_PASS=true` for a round-54 slice whose `rev=077d431e6996` was rewritten to C0. A hand-written line naming `rev=077d431e6996` with fabricated numbers passes the same way (`.ufo/waves/round-56/w1/T56W1ScribeQuality-receipts/107-scope-gap-fabricated-line.txt`, `verdict=PASS`). The contract's `cannot_see` says so, and QUALITY criterion 107 says so in its own terms.
- Neither counter sees whether a re-key entry's pinned-input surface is the surface the section's bytes depend on. The drift map (`.ufo/waves/round-56/w1/drift-map.json`) is wave-1 reconnaissance, not a gate.

## Round-57 deferrals

- **F1 — anchors.** Page-local `:NNN` anchors in `SKILL.md` (Mistakes: citation drift). Repair by heading anchor, then re-read.
- **F2 — standing-rule table.** Row 1's code (Mistakes: standing-rule table). Repair with F1, since both change the same section.
- **Standing-rules text, two more items from `T56W2Read07`:** the scratch-namespace dash-form clause, and the `<tool>: could-not-evaluate:` byte shape (three of nine modes print `WITNESS_STUDY:` or `ENVDIFF_SETUP:`). Both are round-55-era text. One re-read covers all three.
- **R1 — `SKILL.md` byte identity between C0 and the deciding revision is unenforced.** `SKILL.md` is not in `contract.json` `frozen_paths` and is in the binder's drop list. Measured: one post-C0 line moves the monitor 47/64 → 46/64. `validate-readers.py` already computes `READER_HASH_XREV_DRIFT`; the deciding path should run it at the candidate revision before the bind.
- **Reader findings adjudicated `gap-minor`, not repaired** (`.ufo/waves/round-56/integration/reader-adjudication.md`): `SOURCES.md` pointer at line 503 (now 508); the env-diff invocation missing `--fleet-root`; active-row count 50, not 49; two non-clean round-26 registry examples; the shared JS `off-by-one` class omitted from one summary.
- **Coverage index.** `corpus/knowledge/receipt-revision-binding.md` is not indexed in `corpus/README.md`; that file is a pinned re-key input, so the change waits for the next round.
- `considerthese` proposals 2–5 remain unmined.

=== END corpus/lessons/round-56.md ===
