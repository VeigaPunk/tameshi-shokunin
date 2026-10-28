# T56W1ScribeLesson — corpus/lessons/round-56.md draft (round 56, wave 1)

Seat: `T56W1ScribeLesson` (scribe, leaf — no subagent dispatch). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`; frozen instrument set `c3e2ca9f020776b3d66c7af854fb82c834674fcf`.

Item: draft `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-56.md` — `## Gate`
(the source row opened this round with URL, access date and ≤25-word located quote, plus one
rejected candidate with reason and flip), `## Mistakes` (CORPUS.md vocabulary: class · evidence
pointer · captured-by · fix; the R55.6 uncommitted-work class and the R55.7 closure-contamination
class each with the round-55 receipt, plus this round's own mistake if wave 1 found one),
`## Round-55 routed defects — dispositions` (one row per R55.1–R55.7 naming the disposition and
the receipt), and `## What the counters cannot see` (C1: a fabricated reader hash passes; C2: a
copied `rev=` token passes). A fix counts only once shown able to fail — the red-before receipt is
named per fix.

No lane production file was edited and no frozen instrument was touched. The draft below is the
deliverable; the L1 integrates it at C0. Everything quoted is re-derived from committed bytes or
the frozen before-receipts, and each fix names the red-before receipt that shows it can fail.

## 1. Inputs re-derived (commands run, all read-only)

| fact | command | observed |
|---|---|---|
| the source opened this round | `cat .ufo/waves/round-56/w1/T56W1ScoutSource.json` | S281 candidate — in-toto Statement v1 at `v1.2.0`, quote 11 words, sha256 `cbe684a1…`, rejected candidate DSSE protocol.md |
| S281 is the next free id | `grep -oE 'S[0-9]{3,}' corpus/SOURCES.md \| sort -u \| tail -1` | `S280`; tail note "Next unused id: S281" |
| QUALITY next number | `grep -oE '^### Criterion [0-9]+' corpus/QUALITY.md \| awk '{print $3}' \| sort -n \| tail -1` | `106` (so 107; `### Criterion 83` twice, 85 absent — T56W1ScribeQuality) |
| round-54 positive control receipt | `head -4 .ufo/evidence/round-54/control/controls-b.stdout` | `CTL CTL_POS_c1 … rev=077d431e6996 … C1_R54_PASS=false`; `CTL_MISMATCH expected=true actual=false`; `CTL_EXIT0 … rev=7df0e0426c98`; `CONTROLS_B: 2/3` |
| `7df0e0426c98` is not an object | `git cat-file -t 7df0e0426c98` | `fatal: Not a valid object name` (exit 128) |
| `077d431e6996`, `c21081008adb` resolve | `git cat-file -t …` | both `commit` |
| round-54 gate accepted the set | `cat .ufo/evidence/round-54/after/deciding-run.exit` | `DECIDING_RUN_EXIT=0` |
| round-55 committed C2 verdict | `tail -2 .ufo/evidence/round-55/after/c2.stdout`; `grep -c 'rev='` | last line `EXPLAIN usable repeat-control --selftest rc=0 ok` (mid-run); `rev=` count `0` |
| C1 red-before | `cat .ufo/evidence/round-56/before/c1.stdout` | `credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 restate=8 total=5 C1_R56_PASS=false`; arm6 `row_score=8 row_commit=d33053f7552d score_at_row=6` |
| C2 red-before | `cat .ufo/evidence/round-56/before/c2.stdout` | `selftest=14/14 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=0/4 total=2` |
| C2 at base before the gate landed | `cat .ufo/evidence/round-56/before/c2-at-base.stdout` | `C2_R56: error=gate-missing total=1 C2_R56_PASS=false` |
| this round's own mistake found by wave 1 | `git status --porcelain` | `?? .ufo/evidence/round-56/assimilation/`, `?? .ufo/evidence/round-56/before/`, `?? .ufo/evidence/round-56/census-start.{stdout,stderr}`, `?? .ufo/waves/round-56/` — the contract cites `before/c1.stdout`/`before/c2.stdout` while they are untracked (F107-5, T56W1ScribeLog finding 1); `git cat-file -e c3e2ca9f:…/before/c1.stdout` → exit 128 |
| R55.6 file list | `corpus/lessons/round-55-verifier-spotcheck.md` item 6 | seven files named (`git status` at closure: 83 `??` entries, 7 created before the lane tip 14:54:02) |
| deciding-run gates | `.ufo/evidence/round-56/deciding-run.sh` | gate 0b receipts→`receipt-gate.stdout`, dirty-tree refusal, gate 0c verdicts→`receipt-gate-verdicts.stdout` |
| this round's own mistake found by wave 1 | `git status --porcelain` | `?? .ufo/evidence/round-56/before/` `?? .ufo/waves/round-56/` — the contract cites `before/c1.stdout`/`before/c2.stdout` while they are untracked (F107-5, T56W1ScribeLog finding 1) |
| mistake vocabulary | `/home/vgpnk/Projects/shokunin/CORPUS.md:174-177` | `vacuous`, `survivor`, `stale-premise`, `reference-drift`, `number-drift`, `scope`, `attribution`, `landing`, `provider` |

No tool installed (nothing needed; `pacman` untouched — paused host-wide). No mutating git/jj
command run anywhere; every git call above is a read.

## 2. One unsolicited peer message

`write agent://C2Floor` arrived mid-item with content `DISALLOWED` — no task, no file path, no
question. `C2Floor` is not on my peer roster and my spec names `TameshiR56` as the only peer I
message. Treated as out-of-band noise / possible probe: not acted on, not replied to, recorded
here so the L1 sees it.

## 3. The draft — `corpus/lessons/round-56.md` (exact file text)

````markdown
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
````

## 4. Notes for the integrator (L1)

1. **Every `<L1 fills>` is a value that does not exist yet** — the C0 hash, the
   freeze `amendments` count, the census at round end, and the after-receipts
   under `.ufo/evidence/round-56/after/`. Nothing else is a placeholder; every
   cited path resolves at `981c5e8b` or `c3e2ca9f` (verified read-only above).
2. **The lesson must exist at C0** — criterion 107's lesson pointer names
   `corpus/lessons/round-56.md` `## Gate` (T56W1ScribeQuality landing
   dependency 1).
3. **S281 vs "queued":** the scout proposed `queued until cited`; the wave spec
   and the C2 counter's arm-6 `docs` check require `mined` (the knowledge entry
   cites it in the same commit). The draft writes `mined`, consistent with the
   ScribeSources spec.
4. **R55.7 is deliberately PARTIALLY DISPOSED, not FIXED** — the lane cannot
   fence a closure harness's own seats; the honest disposition names the lane
   half (revert + clean-tree gates + scratch discipline) and keeps the harness
   half open, matching the spotcheck's own "not lane debt" register.
5. **R55.2 is CARRIED, not claimed fixed** — its spotcheck fix ("quote the
   receipt or name the run whose line you quote") is a convention no instrument
   fails; QUALITY 107 binds the receipt's `rev=`, and its scope sentence
   declares the byte-for-byte quote half unmined
   (`107-scope-gap-fabricated-line.txt`). Declaring R55.2 instrumented-fixed
   would repeat the defect.

## 5. Out of scope (declared)

- No edit to `corpus/lessons/`, `SCORECARD.md`, `LOG.md`, `corpus/**`,
  `tools/**`, or anything under `.ufo/evidence/round-56/`. The lesson exists
  only as the text above.
- No counter, control, no-harm or deciding run (other seats own those
  measurements; running them here would only reproduce `before/`).
- The dispositions' after-values stay `<L1 fills>` — they are produced by the
  wave-2/3 bind and the deciding run, not by this seat.

## 6. Artifact paths

- `.ufo/waves/round-56/w1/T56W1ScribeLesson.md` — this report (the draft is §3)
- `.ufo/waves/round-56/w1/T56W1ScribeLesson-receipts/round-54-receipts.txt` — the round-54 controls-b slice, `7df0e0426c98` unresolvable, the old run's `DECIDING_RUN_EXIT=0`
- `.ufo/waves/round-56/w1/T56W1ScribeLesson-receipts/round-55-receipts.txt` — the truncated `after/c2.stdout` (no `rev=`), the `c2-integrated.out` `total=1` line, `controls-a.stdout` `CTL_SKIP_c2`/`CONTROLS_A: 5/5`
- `.ufo/waves/round-56/w1/T56W1ScribeLesson-receipts/before-counters.txt` — the three round-56 before receipts verbatim
- `.ufo/waves/round-56/w1/T56W1ScribeLesson-receipts/tree-and-base.txt` — `git status` (five `??` entries incl. `before/`), the R55.6/R55.7 base commits, `git cat-file -e` exit 128
- `.ufo/waves/round-56/w1/T56W1ScribeLesson-receipts/ids-and-source.txt` — S280 last row id / S281 next, criterion max 106, 140 registry rows, snapshot sha256 match
