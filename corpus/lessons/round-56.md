# tameshi round 56 — lesson (hyaku run 11, 2026-10-28)

L1 TameshiR56. The round repairs what the round-55 non-author closure rejected
(`corpus/lessons/round-55-verifier-spotcheck.md`, verdict `rejected-harmed`):
R55.3 — the round's own edits cost the cold-read monitor 18 of 64 credited
sections (64/64 score 8 → 46/64 score 6) and the re-key never landed — is C1;
R55.5 — the deciding gate cannot compare the revision it certifies — is C2.
R55.1, R55.2, R55.4, R55.6 and R55.7 are disposed below. Base `981c5e8b`
(`.ufo/evidence/round-56/contract.json`); the contract, both counters,
`tools/receipt-revision-gate.py`, `controls.sh`, `no-harm.sh` and
`deciding-run.sh` are frozen at the original freeze `c3e2ca9f020776b3d66c7af854fb82c834674fcf`; `freeze.json` records one pre-scoring amendment at operative freeze `21eb3c63cd0f3190c0deeb8953c6c91c7742cd68` (amendment 1; the contract, targets, counters and arms are unchanged). Content commit C0 `c0137451f5b7f22d65f748fc69f1b181f55e1378`; deciding receipts
under `.ufo/evidence/round-56/after/`.

## Gate (sources opened this round)

| S | URL | opened | quote (<=25 words, located) | verdict |
|---|---|---|---|---|
| S281 | https://github.com/in-toto/attestation/blob/v1.2.0/spec/v1/statement.md | 2026-10-28 | §Fields, field `subject`, the IMPORTANT paragraph (snapshot lines 54–55, `> ` stripped): "Subject artifacts are matched purely by digest, regardless of content type." (11 words) | **admit, mined** — `corpus/knowledge/receipt-revision-binding.md` cites it for the receipt-to-subject binding: an attestation is evidence only for the artifact its `subject.digest` names, so a verdict naming another revision is not evidence for this one; the spec is tier A for its own Statement shape |
| (no row) | https://github.com/secure-systems-lab/dsse/blob/master/protocol.md | 2026-10-28 | §Signature Definition, line 27: "SERIALIZED_BODY: Arbitrary byte sequence to be signed." (6 words) | **reject before append** — DSSE signs an arbitrary payload; nothing in the envelope requires the payload to name the artifact it attests, so it cannot ground a receipt-must-name-its-revision rule. Flip: a lane rule that adopts DSSE as the wire format and layers a subject-digest requirement on the payload |
| S282 | https://github.com/slsa-framework/slsa/blob/main/spec/build-provenance.md | 2026-10-28 | §Model, first paragraph (reader extraction, 11 words): "Provenance is a predicate that describes how a software build was executed." | **rejected, kept as row S282** — the predicate binds a build to the artifacts it produced, not a receipt to the revision it certifies; the subject binding the rule needs lives in S281's Statement layer. Flip: the lane publishes signed build provenance for its own artifacts and needs `builder.id`/`buildType` |

Snapshot/extraction receipts: `.ufo/evidence/round-56/assimilation/in-toto-statement-v1.md`
(sha256 `cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea`, 2492 B;
pinned tag `v1.2.0` `df02077b`, byte-identical at `main` `50bf0171`), extraction metadata
`in-toto-statement-v1.json`, full text `in-toto-statement-v1.extract.txt`. Census at round
end: exit 0, 142 rows, 16 warnings (15 W04 duplicate-URL notices and one W01 S101 tier-C notice), no errors (`integration/census-pre-pin.{stdout,stderr,exit}`); command `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`.

considerthese mining: `considerthese/2026-10-28.md` proposal 1 (the
receipt-existence linter for records) is mined into `corpus/QUALITY.md`
criterion 107 — its revision half (the receipt names the revision it measured;
existence checked as `RECEIPT_MISSING`/`RECEIPT_REV_UNRESOLVABLE`) lands; its
quote half (byte-for-byte match of a quoted counter line) is declared unmined
in the criterion's own scope sentence, demonstrated by
`.ufo/waves/round-56/w1/T56W1ScribeQuality-receipts/107-scope-gap-fabricated-line.txt`.
Proposals 2–5 remain unmined (at most one per round).

## Mistakes

- **class: landing — round evidence left uncommitted at closure.** evidence:
  round 55's `git status --porcelain` at closure read 83 entries, seven of them
  round-55 evidence files created before the lane tip (`corpus/lessons/round-55-verifier-spotcheck.md`
  item R55.6, `## Step-1 conformance` row "uncommitted round work"): the wave-1
  re-key prep receipts `w1/T55W1ExecRekeyPrep-receipts/{base,cand,floor}.json`
  (13:55:47) and `rekey.json` (13:58:42), the cold-read monitors
  `w1/T55W1ExecNoHarm-receipts/coldread-at-base.json` (14:02:24) and
  `w1/T55W1CritClaimShape-receipts/coldread-HEAD.json` (14:31:03), and
  `w2/T55W2ScoutColdread-receipts/inputs.json` (14:34:53) — all before the tip
  14:54:02, all uncommitted at close. captured-by: none at round 55 — the
  deciding run checked receipt existence at REV, never the working tree after
  the tip. fix: the R55.6 files were swept into the base at `6efd2a1` and
  `981c5e8b` before this round's contract froze; and the frozen
  `deciding-run.sh` refuses a dirty tree both before (`clean-tree-before.txt`,
  `DECIDING_REFUSED dirty-tree`) and after (`clean-tree-after.txt`) the
  deciding run — a receipt the tree did not commit is a refusal, not a note.
  Red-before: the round-55 closure's own `git status` output (83 `??` lines),
  quoted in the spotcheck; shown able to fail again by this round's own row
  below.

- **class: attribution — a non-lane seat wrote inside the lane tree.**
  evidence: during the round-55 closure, `.ufo/evidence/round-55/after/c2.stdout`
  was rewritten after the tip with `C2_R55: rev=4c04c1d33377 … total=0
  C2_R55_PASS=true` (uncommitted — a green line the lane never produced) and 14
  tracked `T55W1MutC2-receipts` files were deleted from the working tree
  mid-closure (`corpus/lessons/round-55-verifier-spotcheck.md` item R55.7;
  `## Step-1 conformance` "uncommitted round work" row). captured-by: none —
  the closure flagged it as not lane debt but nothing kept a concurrent seat
  out of the lane's working tree. fix: the post-tip closure rewrites were
  reverted to branch bytes at `6efd2a1` before the base (contract `base_note`:
  content files byte-identical to `fa48c06c` for every claim path), and this
  round's deliverables discipline sends every seat's writes to `.ufo/waves/…`
  and scratch clones — the deciding run's clean-tree gates catch any residue.
  Residual, not closed: the lane cannot fence a closure harness's own seats;
  the receipt is the spotcheck's list plus the base commits.

- **class: landing — this round's before-receipts cited while untracked.**
  evidence: the frozen contract's `before` fields and the C1/C2 claim text
  cite `.ufo/evidence/round-56/before/c1.stdout` and `…/c2.stdout`, but
  `git status --porcelain` at wave-1 drafting reads `??
  .ufo/evidence/round-56/before/` — the receipts the claims' before-values
  restate are not in any commit (T56W1ScribeQuality F107-5; T56W1ScribeLog
  finding 1; `git cat-file -e c3e2ca9f:.ufo/evidence/round-56/before/c1.stdout`
  → absent). captured-by: this round's own `## Mistakes` — the same class as
  R55.6, caught by wave-1 seats inside the round, not by a later closure.
  fix: C0 commits `before/{c1,c2,c2-at-base}.stdout` (and the wave-1 reports
  and receipts) so every before-pointer resolves at the commit that cites it
  (QUALITY 97). Red-before: the `git cat-file -e` refusals recorded in
  `T56W1ScribeLog-receipts/cited-paths.txt` (three `before/*.stdout` absent
  at the freeze).

### Additional round-56 mistakes (attempt 3; 2026-10-28)

- **class: citation drift — current SKILL.md page-local anchors.** Evidence: `T56W2Read17-receipts/page-wide-sweep.txt` finds 57 of 61 ranges no longer resolve to the bytes they named; the offset is +17 from the round-54 repair (+4 at round-55 C0, +13 at round-56 C0). The service-limits reader's ranges `:824-828`, `:834-836`, `:851-855`, `:890-892`, and `:1023-1169` land on unrelated text. **captured-by:** QUALITY criterion 34 (a citation into a moving file must be anchored by a stable symbol/heading; a line range is secondary). **fix:** no same-round SKILL edit; it would change C0 section hashes and invalidate bound reports. Round 57 must replace these ranges with heading/function anchors and re-read after the change. Red-before: the `git show C0:SKILL.md` ranges and corrected ranges in Read17's receipts; this fix is not credited as landed.

- **class: sourced quotation and recheck drift.** Evidence: W2 `T56W2RevSources.md` F1–F3 shows the S282 sentence is absent from its source, the S281 note splices two passages, and its `14/14` selftest expectation disagrees with the amended C0 gate's `19/19`; the L1's source re-open is retained in `integration/l1-source-reopen.txt`. **captured-by:** CORPUS.md SOURCES rule 1 and QUALITY criteria 35/51/91. **fix:** append-only errata in the knowledge note and this lesson; the replacement quote is present in the re-open record, and the recheck is explicitly superseded. Red-before: exact-string searches for the claimed S282 quote return 0; the C0 gate selftest returns `GATE_SELFTEST: 19/19 pass`.

- **class: claim sizing — C2's no-op control reaches its target.** Evidence: `T56W2CritDoNothingC2.md` v2/v3 scratch trees yield `C2_R56_PASS=true` using two stub controls or a borrowed round-54 receipt with its `rev=` token rewritten; no controls run produced those bytes. **captured-by:** the round prompt's claim-sizing rule (§9), which requires a do-nothing control below target before freeze. **fix:** none this round; the claim/counter are frozen after data. The final C2 counter result is recorded, but C2 is not admitted as a measured improvement; a future claim must preregister a discriminator for control provenance.

## Round-55 routed defects — dispositions (this round)

| id | disposition | evidence |
|---|---|---|
| R55.1 | FIXED by C2's deciding gate: `deciding-run.sh` gate 0c runs `tools/receipt-revision-gate.py --certified REV` on the verdicts the run just produced (`receipt-gate-verdicts.stdout`), so a committed `c1.stdout`/`c2.stdout` that does not name the certified revision is refused (`RECEIPT_REV_ABSENT` or `RECEIPT_REV_MISMATCH`) and `DECIDING_RUN_EXIT` cannot read 0 without it | `.ufo/evidence/round-56/deciding-run.sh`; red-before: `.ufo/evidence/round-55/after/c2.stdout` refused `RECEIPT_REV_ABSENT` in `.ufo/evidence/round-56/before/c2.stdout` (`red55=`); after: `.ufo/evidence/round-56/after/receipt-gate-verdicts.stdout` reads `GATE: receipts=2 ok=2 refused=0 codes=none verdict=PASS` at REV `1b44bace0974` and `.ufo/evidence/round-56/after/deciding-run.exit` reads `DECIDING_RUN_EXIT=0` |
| R55.2 | CARRIED — stated as a rule and exercised as a convention, but no instrument can fail it: every value this round's records quote names the committed receipt that carries it, and verdicts are quoted from the counter's own line, never a seat paraphrase (the ScribeLog draft's rule; the report skeleton's `<fill: receipt path>` slots). QUALITY 107 binds the receipt's `rev=`; its scope sentence declares the byte-for-byte quote half unmined — claiming R55.2 instrumented-fixed would repeat the defect | the rule: `corpus/QUALITY.md` criterion 107 scope paragraph; the round-55 receipt: `.ufo/waves/round-55/w1/T55W1ScribeSkill-receipts/c2-integrated.out` (`total=1 C2_R55_PASS=false` where the report quoted `total=0`) |
| R55.3 | FIXED by C1: the 18 lost headings are re-read at one content commit C0 and bound under one `rekey-r56-<c0>` directory, the precheck must read `lost=0` (64 credited), the monitor `64/64 score=8 box3=true`, and the standing calibration row is restated to the score the monitor reads at the commit the row names (arm 6 `restate`) | `.ufo/evidence/round-56/contract.json` C1 target; red-before: `.ufo/evidence/round-56/before/c1.stdout` (`credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 restate=8`); after: `.ufo/evidence/round-56/after/c1.stdout` reads `C1_R56: rev=1b44bace0974 c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true` and `after/coldread-precheck.stdout` reads `lost=0 ok`. Residual: 13 of the 18 bound entries label `external_inputs` `tameshi@C0:corpus/SOURCES.md` (13) / `corpus/QUALITY.md` (6) with the PIN digest, not the C0 blob digest (L1 re-derived with `git show C0:<path>` sha256; seat `T56W3Led13`): the frozen counter does not read `external_inputs`, so the pass does not certify those labels. |
| R55.4 | FIXED by construction: the control set is the frozen `.ufo/evidence/round-56/controls.sh`, phase B scores the positive controls at the revision they certify (PIN), both phase receipts are committed before the deciding run which refuses without their `CONTROLS_A:`/`CONTROLS_B:` verdict lines — nothing is described from memory before the receipts exist | `.ufo/evidence/round-56/controls.sh`, `deciding-run.sh` (control-receipt-missing / controls-*-verdict-missing refusals); the round-55 receipt: `.ufo/evidence/round-55/control/controls-a.stdout` (`CTL_SKIP_c2 … total=4`, `CONTROLS_A: 5/5` — committed before the report claimed it "still running") |
| R55.5 | FIXED by C2: `tools/receipt-revision-gate.py` binds each receipt's `rev=` to the certified revision (drift on the declared surface → `RECEIPT_REV_CONTENT_DRIFT`; unresolvable → `RECEIPT_REV_UNRESOLVABLE`; absent → `RECEIPT_REV_ABSENT`), and `deciding-run.sh` applies it to the round's own control receipts (gate 0b) and to the verdicts it produces (gate 0c); QUALITY 107 states the rule and its falsifier is the gate's refusal of the real round-54 receipt | `tools/receipt-revision-gate.py`; red-before: `.ufo/evidence/round-56/before/c2.stdout` (`red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE`, `docs=0/4`) on `.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout` and `.ufo/evidence/round-54/control/controls-b.stdout`, which the old path accepted (`.ufo/evidence/round-54/after/deciding-run.exit` `DECIDING_RUN_EXIT=0`) |
| R55.6 | FIXED for the inherited files and gated going forward: the seven uncommitted round-55 receipts were swept into the base at `981c5e8b` (round-56 start, contract `base_note`) and `6efd2a1`; the frozen `deciding-run.sh` refuses a dirty tree before and after the deciding run (`clean-tree-before.txt` / `clean-tree-after.txt`); the class recurred this round and is caught in `## Mistakes` (the untracked `before/` receipts) | `git log 981c5e8b` (`6efd2a1`, `981c5e8` messages name R55.6/R55.7); `.ufo/evidence/round-56/deciding-run.sh`; the round-55 receipt: `corpus/lessons/round-55-verifier-spotcheck.md` item R55.6 and its seven-file list |
| R55.7 | PARTIALLY DISPOSED — lane side repaired, harness side residual: the post-tip closure rewrites (the uncommitted green `C2_R55` line in `after/c2.stdout`, the 14 deleted `T55W1MutC2-receipts` files) were reverted to branch bytes at `6efd2a1` before the base; this round's discipline keeps seat writes in `.ufo/waves/…` and scratch clones and the clean-tree gates expose any residue at close, but a non-lane seat writing in the lane tree is outside the lane's write scope — the receipt is the record, not a fence | `corpus/lessons/round-55-verifier-spotcheck.md` item R55.7; `git show 6efd2a1 --stat` (reverted files); contract `base_note` (content bytes identical to `fa48c06c` on every claim path) |

## What the counters cannot see

- C1: whether a reader actually read the section. A reader report's
  `section_sha256` is computable from the tree without opening the section, so
  a fabricated report satisfies arm 4 (`contract.json` C1 `cannot_see`); the
  wave's adversarial seats — and CTL_FAB_c1, which fabricates exactly one hash
  and must read `C1_R56_PASS=false` — are the only guards.
- C2: whether a receipt that names the certified revision was produced by the
  run it claims. A copied `rev=` token passes the gate
  (`contract.json` C2 `cannot_see`); the digest sidecar
  (`RECEIPT_DIGEST_MISMATCH`, `--receipt PATH:ROLE` with a `.sha256` sibling)
  narrows it for the receipts that carry one, but a hand-written line naming
  the right sha still passes — demonstrated this wave by
  `T56W1ScribeQuality-receipts/107-scope-gap-fabricated-line.txt`
  (`rev=077d431e6996 credited=99 lost=0` → `verdict=PASS`), and QUALITY 107
  says so in terms rather than letting the criterion read as a byte check.
- Neither counter sees whether the pinned-input surface a re-key entry carries
  is the surface the section's bytes actually depend on; the drift map
  (`.ufo/waves/round-56/w1/drift-map.json`) is the wave-1 recon, not a gate.

## Round-57 deferrals (named here because they cannot be repaired this round)

- **F1 — the round's +13-line insertion moved 125 of SKILL.md's 155 page-local `:NNN`
  anchors by +13** (109 were already stale by +4 from round 55). Twenty-nine of the
  shifted anchors sit inside the eighteen headings being re-read, and two readers
  reported it as a true finding (`T56W2Read17` 4 findings in `### The service's limits`,
  `T56W2Read06` 1 finding in `## Repeated controls and gate registry — round 12`, whose
  `corpus/SOURCES.md:503` cite is 2 off because this round added S281/S282 at lines
  156-157). **Adjudicated gap-minor, not repaired**: a text fix would cost eighteen
  re-reads, so the repairs are round 57's first item. Receipts:
  `.ufo/waves/round-56/w2/T56W2RevSkillScope.md` §3a,
  `.ufo/evidence/round-56/integrate/resolutions.json`.
- **R1 — SKILL.md byte-identity between C0 and the deciding revision is unenforced.**
  `SKILL.md` is not in `contract.json` `frozen_paths`, is in the binder's DROP list (so
  bind step 3c cannot see it) and is in round-18's `IGNORED_INPUTS`. Measured with the
  frozen binder: one post-C0 line takes the monitor 47/64 -> 46/64 and makes arm 4
  refuse the reader report. `validate-readers.py` already computes this as
  `READER_HASH_XREV_DRIFT`; the deciding path must run it at the candidate revision
  before the bind. Not closed this round — recorded so round 57 instruments it.
- **Blocker, not a deferral: seven of eighteen reader reports do not exist at C0.**
  `T56W2Read02`, `Read03`, `Read04`, `Read13`, `Read14`, `Read15`, `Read16` left
  receipts directories but no `.json` (Read04/15/16 left nothing). The binder therefore
  cannot reach `rekeyed=18 skipped=0` and C1 is an honest miss this attempt; the seven
  headings stay unbound and the monitor stays at 46/64.
- **F2 — this round's own `## Standing rules` table states the wrong code for row 1,
  verified by the L1 against the C0 gate** (four invocations on the same receipt bytes,
  `rev=077d431e6996` certified `c21081008adb`):
  `role=verdict paths=1 -> RECEIPT_REV_CONTENT_DRIFT`,
  `role=verdict paths=0 -> RECEIPT_REV_MISMATCH`,
  `role=positive paths=1 -> RECEIPT_REV_CONTENT_DRIFT`,
  `role=positive paths=0 -> RECEIPT_REV_MISMATCH`.
  The gate selects the code by `--paths` and drift, never by role, so row 1's
  `RECEIPT_REV_MISMATCH` cell is false in the case it most matters (a verdict receipt
  gated on the declared surface); row 2's parenthetical is the only true statement of
  the rule. The table also names four of eleven codes; it never names
  `RECEIPT_CONTROL_NOT_ANCESTOR`, `RECEIPT_REV_AMBIGUOUS`, `RECEIPT_MISSING`,
  `RECEIPT_EMPTY`, `RECEIPT_NOT_BLOB`, `RECEIPT_REQUIRED_LINE_MISSING` or
  `RECEIPT_DIGEST_MISMATCH`. **Deferred to round 57 with the anchor repairs** — fixing
  it now would break C0 byte-identity (R1) and invalidate the reader reports bound at
  C0. Receipt: `.ufo/waves/round-56/w2/T56W2RevSkillScope.md` §6a (which withdraws that
  report's earlier "no false statement" claim) and `T56W2Read07.json` finding F2.
- **Scope of the round-57 `## Standing rules` repair list — three items, one of them
  this round's.** Read07's F2 (the role->code mapping above) is the only finding about
  round-56 text; its F1 (the scratch-namespace "dash form survives only in run
  artifacts" clause) and F3 (the `<tool>: could-not-evaluate:` byte shape, where three
  of nine modes print `WITNESS_STUDY:`/`ENVDIFF_SETUP:`) are pre-existing round-55-era
  text. Repairs are scheduled together because one re-read covers all three.

## Attempt 3 integration and adjudication notes (2026-10-28)

### Source re-open and additive corrections

The L1 re-opened S281, S282 and the screened-out DSSE candidate on 2026-10-28; exact URLs,
anchors and quotes are in `.ufo/waves/round-56/integration/l1-source-reopen.txt`. S281's
located quote remains “Subject artifacts are matched purely by digest, regardless of content
type.” (11 words, `## Fields` / `subject`, lines 54-55). S282 remains a rejected row; the
source's actual `## Model` first sentence is “Provenance is an attestation that a particular
build platform produced a set of software artifacts through execution of the `buildDefinition`.”
The earlier Gate quote “Provenance is a predicate that describes how a software build was
executed” is not in that source. The DSSE candidate remains an excluded search result without a
registry row: its `SERIALIZED_BODY` quote says “Arbitrary byte sequence to be signed.” (7 words,
`## Signature Definition`, parameters row), and it does not require a subject digest.

The L1 appended errata, without rewriting the C0 evidence: `knowledge/receipt-revision-binding.md`
records the S281 quote splice, the freeze-era 14/14 versus amended 19/19 gate count, and the
fixture-demo environment/cwd requirement; `corpus/QUALITY.md` records the corrected criterion-107
lesson anchor and scope-gap receipt bytes. The source search log records 3 identified/screened,
1 included (S281), 2 excluded (S282 retained rejected row; DSSE excluded without a row). Rows
added remain S281 mined and S282 rejected; S283 remains the next unused id.

### Wave-2 findings and dispositions

All 18 C0 reader reports are now present under `w2/` after same-identity completion of Read04 and
Read15; no seat was replaced. `integration/resolutions.json` carries the explicit minor-gap counts
for the six headings with findings (13 total). The exact findings and L1 dispositions are in
`integration/reader-adjudication.md`; the C0 section hashes and reader outputs remain unchanged.
No `SKILL.md` edit is made before the re-key.

Read17 and the page-wide sweep establish that 57 of 61 distinct page-local line ranges no longer
resolve to the bytes they cite; the offset is +17 from the round-54 line-anchor repair (+4 in the
round-55 C0, then +13 in this C0). This is a depth/quality harm outside the frozen no-harm monitor.
It is deferred to round 57: a same-section edit now would change a C0 section hash and invalidate
its reader report. The occurrence-count sweep (125/155 shifted by +13) and the distinct-range sweep
(57/61 stale at C0) count different populations; neither figure replaces the other.

Read04 also records the undercount in the shared JS defect classes; Read06 the S026→S265
`SOURCES.md` pointer (at the current working tree after the appended search log, the target is
line 508); Read07 the dash-form boundary, receipt-code mapping and stderr-token shape; Read15 the
clone `env-diff` invocation's missing `--fleet-root` and the 49→50 active-row count; Read16 two
non-clean round-26 registry/gate examples. These SKILL page findings remain deferred; no line or
content fix is claimed.

The C2 do-nothing attack also reached `C2_R56_PASS=true` with two synthetic 79-byte control
receipts (W2 critic v2); a borrowed round-54 receipt with its revision token rewritten did so too
(v3). The actual gate correctly binds revision tokens and refuses the retained old receipts, but
the frozen counter cannot establish that its “own receipts” came from a real controls run. This
invalidates C2's do-nothing-control admission predicate; no frozen target or counter is changed
after data. Report the measured C2 line separately from this claim-sizing failure.

## Errata — attempt 3 source and claim adjudication (2026-10-28)

### S282 quote re-opened by L1

The `## Gate` S282 quote at line 21 above is not in the cited SLSA page. The L1 re-opened
`https://github.com/slsa-framework/slsa/blob/main/spec/build-provenance.md` on 2026-10-28;
at `## Model`, first paragraph, the exact sentence is “Provenance is an attestation that a
particular build platform produced a set of software artifacts through execution of the
`buildDefinition`.” The false quote is superseded by this located passage; the S282 rejection
and flip remain unchanged. DSSE was also re-opened at its pinned protocol commit and excluded
without a row. Evidence: `.ufo/waves/round-56/integration/l1-source-reopen.txt`.

### Reader finding dispositions and same-seat completion

The W2 `T56W2Read04` and `T56W2Read15` result strings initially ended before their required
Markdown/JSON reports. The same two identities were resumed; both reports and receipts are now
present. No replacement seat was spawned. The frozen reader findings are adjudicated as
`gap-minor` with the exact per-heading counts in `.ufo/waves/round-56/integration/resolutions.json`;
the supporting dispositions are in `reader-adjudication.md`. No `SKILL.md` section was edited.

### C2's no-op control reaches the frozen target

`T56W2CritDoNothingC2.md` demonstrates that two 79-byte stub receipts naming the certified
revision make the frozen C2 counter print `C2_R56_PASS=true`; a borrowed round-54 receipt with
only its `rev=` token rewritten does so as well. The gate is correctly binding those bytes, but
the counter cannot show that the receipts came from an actual controls run. This is the
pre-registered provenance blind spot; it also means the frozen C2 target fails the claim-sizing
do-nothing discriminator. No counter or target is changed after data. The final measured line is
reported separately and is not claimed as an admitted improvement.

### Coverage-index debt

`corpus/knowledge/receipt-revision-binding.md` is not indexed in `corpus/README.md`. The C0
reader-input census shows `corpus/README.md` is a pinned input for the re-key; changing it after
C0 would invalidate the readers. No frontier expansion is claimed. Owner: tameshi, round 57,
after the current re-key is safely landed.

## Attempt 4 — landing record and mistakes (L1 TameshiR56a4, 2026-10-28)

Attempt 4 inherited three finished waves (w1 37, w2 34, w3 37 = 108 seats, no seat replaced), C0, the
bind and three uncommitted pieces; it swept them, ran the controls and the deciding run, and wrote
the record. Landed sequence: `caf6742a` (wave-3 deliverables, bootstrap control receipts),
`888d342e` (five >1 MiB receipts named as files, PIN2), `1b44bace` (final control receipts, REV),
`18bbdab7` (deciding-run receipts). Deciding run: `.ufo/evidence/round-56/after/deciding-run.exit`
`DECIDING_RUN_EXIT=0`, `C1_R56 … total=0 C1_R56_PASS=true`, `C2_R56 … total=0 C2_R56_PASS=true`, all
at `rev=1b44bace0974`; `no-harm.stdout` 15 of 15 `NOHARM … ok`; census exit 0 (`after/census.stdout`).

- **class: control design — the C2 positive control cannot pass on the first controls run.**
  evidence: `integration/controls-bootstrap-8c20d5.stdout` (`CTL_POS_c2 … own=own-receipts-missing
  total=1`, `CONTROLS_B: 1/2`). C2 arm 5 reads the round's committed `controls-a/b.stdout` at the
  certified revision; those cannot exist before the first controls run, so a single-generation
  `controls.sh` can never print `CONTROLS_B: 2/2` and `deciding-run.sh` refuses `CTL_MISMATCH`.
  captured-by: none — the pre-registration never ran the controls end to end before wave 3.
  fix: two generations without touching a frozen byte. Generation 1 (bootstrap, `CONTROLS_B 1/2`) is
  committed at `caf6742a`; generation 2 is scored at `888d342e`, the commit that carries
  generation 1 (`integration/controls-final-888d34.stdout`, `CONTROLS_A: 7/7`, `CONTROLS_B: 2/2`),
  and is what `control/controls-{a,b}.stdout` holds; the gate accepts generation-1 receipts there
  because the declared surface has not changed since `8c20d5c3`
  (`GATE OK … role=positive revs=888d342e1080` in `after/receipt-gate.stdout`). Shown able to fail:
  the bootstrap receipts themselves (`own-receipts-missing`). Round 57: pre-register the two
  generations in `controls.sh`'s header.

- **class: predicate/text mismatch — a frozen counter predicate read a prose cell case-sensitively.**
  evidence: `T56W3ExecControlsA.md` finding: `c1/measure.py:275` tests `'round-21' in cells[2]`; the
  standing row spelled `Round-21`, so `CTL_POS_c1` read `restate` false at `2f5512a8`
  (`w3/T56W3ExecControlsB-receipts/controls-b.stdout`). captured-by: none (the restate arm had no
  fixture with the capitalised cell). fix: the row text was corrected at `8c20d5c3`; the counter stays
  frozen. The `CTL_RESTATE_c1` control (row asserts 9) remains the arm's only discriminator.

- **class: deliverable absent — seats reported a report path that was never written.** evidence:
  `T56W3Led13` wrote its report at the fleet root (misroot, copied byte-exact into
  `.ufo/waves/round-56/w3/T56W3Led13.md`, `cmp` clean, the fleet copy deleted); `T56W3ExecC1Run`
  named `.ufo/waves/round-56/w3/T56W3ExecC1Run.md` and no such file exists in the lane (its result
  string in `w3-results.json` is the only record; a session-log copy exists under the omp sessions
  directory and is not citable). captured-by: wave-context path rules (absolute paths, seat prompts)
  — they failed for two seats of 37. fix: the result strings are retained as the record; neither seat
  is a claim input.

- **class: label drift the frozen counter cannot see — `external_inputs` digests.** evidence: for 13
  of the 18 bound `rekey-r56` entries (ledger indices 591–598, 601, 603–605, 608) 19 `external_inputs`
  labels `tameshi@<C0>:corpus/SOURCES.md` (13) and `corpus/QUALITY.md` (6) carry a digest that is not
  the sha256 of `git show C0:<path>` (L1 re-derived; seat `T56W3Led13`). The counter and the cold-read
  monitor credit the entries by their `inputs`, so `C1_R56_PASS=true` stands, but the labels are
  false statements in the committed ledger. captured-by: none. fix: not repaired — the ledger is a
  frozen surface path and a rewrite would invalidate the bind; round 57 records the PIN as the
  digest's referent or re-binds.

### What attempt 4 did not do

No `SKILL.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/knowledge/`, `tools/` or ledger byte
changed after C0/PIN (the deciding run's `FROZEN_UNCHANGED=1` and the monitor's 64/64 at the final
tip both depend on it). The round-57 repair list stays: F1 anchors, R1 SKILL byte-identity, F2/Read07
standing-rules table, the `corpus/README.md` index entry for `receipt-revision-binding.md`, and the
`external_inputs` labels above.
