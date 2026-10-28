# tameshi round 56 — lesson (hyaku run 11, 2026-10-28)

L1 TameshiR56. The round repairs what the round-55 non-author closure rejected
(`corpus/lessons/round-55-verifier-spotcheck.md`, verdict `rejected-harmed`):
R55.3 — the round's own edits cost the cold-read monitor 18 of 64 credited
sections (64/64 score 8 → 46/64 score 6) and the re-key never landed — is C1;
R55.5 — the deciding gate cannot compare the revision it certifies — is C2.
R55.1, R55.2, R55.4, R55.6 and R55.7 are disposed below. Base `981c5e8b`
(`.ufo/evidence/round-56/contract.json`); the contract, both counters,
`tools/receipt-revision-gate.py`, `controls.sh`, `no-harm.sh` and
`deciding-run.sh` are frozen at `c3e2ca9f` (`.ufo/evidence/round-56/freeze.json`,
`amendments` `<L1 fills>`). Content commit C0 `<L1 fills>`; deciding receipts
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
end: `<L1 fills>` (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`).

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

## Round-55 routed defects — dispositions (this round)

| id | disposition | evidence |
|---|---|---|
| R55.1 | FIXED by C2's deciding gate: `deciding-run.sh` gate 0c runs `tools/receipt-revision-gate.py --certified REV` on the verdicts the run just produced (`receipt-gate-verdicts.stdout`), so a committed `c1.stdout`/`c2.stdout` that does not name the certified revision is refused (`RECEIPT_REV_ABSENT` or `RECEIPT_REV_MISMATCH`) and `DECIDING_RUN_EXIT` cannot read 0 without it | `.ufo/evidence/round-56/deciding-run.sh`; red-before: `.ufo/evidence/round-55/after/c2.stdout` refused `RECEIPT_REV_ABSENT` in `.ufo/evidence/round-56/before/c2.stdout` (`red55=`); after: `.ufo/evidence/round-56/after/{c2.stdout,receipt-gate-verdicts.stdout}` `<L1 fills>` |
| R55.2 | CARRIED — stated as a rule and exercised as a convention, but no instrument can fail it: every value this round's records quote names the committed receipt that carries it, and verdicts are quoted from the counter's own line, never a seat paraphrase (the ScribeLog draft's rule; the report skeleton's `<fill: receipt path>` slots). QUALITY 107 binds the receipt's `rev=`; its scope sentence declares the byte-for-byte quote half unmined — claiming R55.2 instrumented-fixed would repeat the defect | the rule: `corpus/QUALITY.md` criterion 107 scope paragraph; the round-55 receipt: `.ufo/waves/round-55/w1/T55W1ScribeSkill-receipts/c2-integrated.out` (`total=1 C2_R55_PASS=false` where the report quoted `total=0`) |
| R55.3 | FIXED by C1: the 18 lost headings are re-read at one content commit C0 and bound under one `rekey-r56-<c0>` directory, the precheck must read `lost=0` (64 credited), the monitor `64/64 score=8 box3=true`, and the standing calibration row is restated to the score the monitor reads at the commit the row names (arm 6 `restate`) | `.ufo/evidence/round-56/contract.json` C1 target; red-before: `.ufo/evidence/round-56/before/c1.stdout` (`credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 restate=8`); after: `.ufo/evidence/round-56/after/{coldread-precheck.stdout,c1.stdout}` `<L1 fills>` |
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
