# T56W3ConnectorFinal — final separability and overlap

Scope: final bytes at PIN `2f5512a8ab0771fb2eee463ec16db359174f5edd` (HEAD of the lane at the time of this seat). Read-only against the lane. The lane's working tree is dirty (L1/sibling edits to `ledger.json`, `rekey-r56-*/traces`, `corpus/lessons/round-56.md`); both counters read git objects at `--rev` and never the working tree, so the dirty tree does not affect any verdict below. No lane production file, frozen instrument, or bound ledger entry was edited. Scratch: `/fast/scratch/hyaku/tameshi-r56/T56W3ConnectorFinal` (removed at the end of the seat). No tools installed or updated.

## (a) Counters on the separability trees

Commands (all `--work` = a fresh empty dir under scratch; `--explain` on):

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-56/c1/measure.py --lane <TREE> --rev <REV> --work <EMPTY_DIR> --explain
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-56/c2/measure.py --lane <TREE> --rev <REV> --work <EMPTY_DIR> --explain
```

Trees. Wave-2 trees are re-run in their original scratch clones (their REVs reproduce the wave-2 REVs). PIN-rooted trees are fresh `git clone --shared` of the lane checked out at PIN, then committed in the scratch clone only.

| Tree | Construction | REV | C1 verdict line | C2 verdict line |
|---|---|---|---|---|
| PIN (final bytes, as committed) | none | `2f5512a8ab07` | `C1_R56: rev=2f5512a8ab07 c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=1 C1_R56_PASS=false` | `C2_R56: rev=2f5512a8ab07 selftest=19/19 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=4/4 total=1 C2_R56_PASS=false` |
| **C1-only, final bytes (PIN + SCORECARD case fix, below)** | `treeC1` = PIN + one commit `37113788ade1` changing SCORECARD.md:2718 `Round-21` → `round-21` | `37113788ade1` | `C1_R56: rev=37113788ade1 c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true` | `C2_R56: rev=37113788ade1 selftest=19/19 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=4/4 total=1 C2_R56_PASS=false` |
| **C2-only, final bytes** | `treeC2` = PIN minus the `rekey-r56-c0137451f5b7` directory, plus synthetic `control/controls-a/b.stdout` (+ sha256 sidecars) rebound to PIN; commits `3498a73`, `56fcb79` | `56fcb7944759` | `C1_R56: rev=56fcb7944759 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false` | `C2_R56: rev=56fcb7944759 selftest=19/19 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=PASS docs=4/4 total=0 C2_R56_PASS=true` |
| Wave-2 C1-only tree (re-run, `cloneC`) | docs absent at C0, re-keyed fixture readers at `0e237811`, restated row | `9507862f54c2` | `C1_R56: rev=9507862f54c2 c0=0e237811bf2f credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true` | `C2_R56: rev=9507862f54c2 selftest=19/19 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=0/4 total=2 C2_R56_PASS=false` |
| Wave-2 C2-only tree (re-run, `cloneB`) | C0 docs present, no re-key, fixture own receipts | `9a2f3967d2ec` | `C1_R56: rev=9a2f3967d2ec c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false` | `C2_R56: rev=9a2f3967d2ec selftest=19/19 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=PASS docs=4/4 total=0 C2_R56_PASS=true` |

All wave-2 verdict lines reproduce byte-for-byte (`wave-2 separability-counters.txt` for Trees B and C).

Observed, not a verdict: the first PIN-rooted C2-only attempt (commit `3498a73`) with fixture controls that named the C0 revision `c0137451` returned `own=REFUSED` (`EXPLAIN arm5-own exit=3 verdict=REFUSED`). The frozen surface (`SKILL.md`, `QUALITY.md`, `SOURCES.md`, `knowledge/`, `registry.json`, the gate, `ledger.json`, counters) differs between C0 and PIN, so a positive control naming C0 is not content-identical at PIN. Rebinding the fixture to PIN (`56fcb79`) gave `own=PASS`. The gate's refusal of the C0-named fixture is the correct behaviour and is the reason the fixture was rebound.

### What the PIN results show

1. **PIN is not C1-true. The one failing C1 arm is arm 6 (restate), and the cause is a capital letter.** The frozen counter tests `'round-21' in cells[2]` (SCORECARD.md calibration row, evidence cell). The committed row at 2f5512a:2718 reads `Round-21 cold-read monitor …`. Arms 1–5 pass at PIN: precheck `cand_credited=64 lost=0 ok`, monitor `covered=64 score=8 box3=True`, one `rekey-r56-c0137451f5b7`, readers `18/18`, and no LOG/SCORECARD pin in the bound entries (the `total` stays at 1).

2. **The fix is one character, verified in a scratch commit.** Diff applied only in the scratch clone (`37113788ade1`):

```
-| calibration | 8 | Round-21 cold-read monitor `calibration_restraint_score`; …
+| calibration | 8 | round-21 cold-read monitor `calibration_restraint_score`; …
```

   With it, C1 reads `total=0 C1_R56_PASS=true`. SCORECARD is not a bound input (arm 5 forbids LOG/SCORECARD pins, and no entry pins them), so editing it does not invalidate the 18-heading bind. But the fix changes the content-final REV: the L1 must commit it, choose the new REV, and re-run both counters and the controls at that REV. The deciding run cannot use `2f5512a`.

3. **C2 at PIN fails only on arm 5** (`own=own-receipts-missing`). No `controls-a/b.stdout` is committed at PIN, which is the expected bootstrap state. The docs arm is 4/4 and the selftest is 19/19.

4. **C1 and C2 are separable in both directions at the final bytes.** Tree `treeC1` (C1 true, C2 false) and `treeC2` (C1 false, C2 true) differ from PIN only in the one arm each claim owns: the case fix, or the re-key directory plus the own receipts. The separability holds with the counters, not only in the wave-2 construction.

5. **Caveat on the C2-only verdict.** `own=PASS` in `treeC2` rests on synthetic fixture control receipts that name the certified revision. That is the frozen counter's declared provenance blind spot (wave-2 `T56W2CritDoNothingC2`). The verdict shows the counters separate; it is not admission evidence for C2.

## (b) Sibling overlap on final bytes

Overall verdict: **`overlap=complement`** (no `contest`, no duplicate owner of equality between a receipt and the revision a deciding gate certifies).

Method. Two sweeps. (1) `git -C <lane> grep -n -I -E 'RECEIPT_REV_[A-Z]+|receipt-revision-gate|receipt-revision-binding|certified revision|receipt_rev|revision-binding|receipt-check' HEAD -- tools corpus SKILL.md scripts` over every sibling at its HEAD (reads git objects only). (2) Blob identity: `git -C <lane> rev-parse --short=12 HEAD:<path>` for every path the wave-2 report named. Lane HEADs changed for `souji-shokunin` (`994de3b4` → `4280fed`, three commits) and `tsukuroi-shokunin` (`fb5a1d86` → `c0ad548a`). Tool blobs are unchanged except `souji`'s `corpus/knowledge/git-strict-descendant-relation-r40.md` (`0bc3075509b8` → `00ce8f952a4b`; the rule is still in QUALITY Q90 at HEAD).

| # | Lane | Path (HEAD blob) | Owned rule | Relation to C2 (receipt rev == certified rev) | Verdict |
|---|---|---|---|---|---|
| 1 | chousa | `corpus/evidence/round51/receipt-check.py` (`75a171b9ce39`) | `tool-rev` ancestor + tool-blob-at-rev + digest | binds the tool revision, not the certified revision | complement |
| 2 | chousa | `corpus/QUALITY.md:899-908` (documents #1) | same tool, criterion text | same as #1 | complement |
| 3 | chousa | `corpus/knowledge/receipt-binding-r38.md` (`67c073a9566c`) | counter/gate digest pins, invocation identity | not a revision-equality rule | complement |
| 4 | chousa | `corpus/knowledge/revision-binding-r31.md` (`475697b11989`) | SHA-256 pin of a claim's source bytes | not a receipt/certified-revision rule | complement |
| 5 | kotodama | `tools/check-receipt-seq.py` (`b46e77eb7348`) | stamped = evaluated = measured revision; tree and counter digests | equality among a receipt's own fields, not against the deciding revision | complement |
| 6 | souji | `tools/souji-receipt-run.py` (`8f78ec1beef3`) | receipt binds `rev`, tool path/SHA, command, exit; verify checks tool blob at named rev | carrier/tool binding | complement |
| 7 | souji | `corpus/QUALITY.md:218` Q88 (HEAD `4280fed`) — **new since wave 2** | self-assessed value binds to a 40-hex commit that resolves, is an **ancestor** of the audited revision, and carries the value | ancestor relation (weaker than C2's equality; equality implies ancestry, so every receipt C2 accepts is accepted by Q88) | complement |
| 8 | souji | `corpus/QUALITY.md:237` Q90 + `corpus/knowledge/git-strict-descendant-relation-r40.md` (`00ce8f952a4b`, was `0bc3075509b8`) | register row `commit` must be a STRICT descendant of `receipt_rev` | a register-row relation, not a deciding-gate certification | complement |
| 9 | kama | `tools/round33-gate-receipts.py` (`900154d7af55`) | separates evaluated revision from receipt-carrier commit | does not gate a receipt against the deciding revision | complement |
| 10 | tsukuroi | `tools/run-receipt.py` (`9944bd1899d3`) and `tools/check-report-receipts.py` (`5ea796e2dc57`) | report-cited revision/tool pair must have a committed receipt | citation coverage | complement |
| 11 | tsukuroi | `tools/_revision.py` (`24f398a6b981`) and `tools/check-revision-binding.py` (`86ef0ad09602`); SKILL.md `revision-binding` probe rows (e.g. :1902, :2464) | a tool's `--revision` bound to a landed branch revision | no receipt read | complement |
| 12 | kake | `corpus/knowledge/receipt-integrity.md` (`351afd3bb71b`) | `counterSha256`/`toolSha256` bound to the writing invocation | run identity | complement |
| 13 | kumitate | `scripts/receipt-attest.mjs` (`3ff972d4fbb5`) | canonical-record digest, sidecar, nonce | no revision axis | complement |
| 14 | kaidoku | `tools/round-46/attest.py` (`7aaa9b72a5c8`) | `--rev` resolves; artifact's own SHA-256 pin | artifact attestation | complement |
| 15 | revenger | `corpus/knowledge/digest-scope-versus-provenance.md` (`a459db90da35`) | scope of digest equality | semantic guardrail | complement |
| 16 | mori | `tools/mori-retention-reconcile.py` (`78c676e665d2`) — **new since wave 2**; setup token `receipt_revision` in SKILL.md:584 | receipt's `measured_revision` must resolve to a commit, be an **ancestor** of the audited `--rev`, equal the argv `--rev` and the receipt's `commit`; policy/allowlist unchanged since the measured revision | ancestor relation plus self-consistency; equality implies the ancestor test, so no C2-accepted receipt is refused | complement |
| 17 | mado | `SKILL.md:710` `mado-receipt-check` probe → `.ufo/waves/round-18/receipt-check.py` — **new since wave 2** | receipt and tool bytes read via `git show` at the named revisions; `pending rev` = could-not-evaluate | reads the bytes at the revision the receipt names; no certified-revision gate | complement |
| 18 | kotoba | `.ufo/waves/round-21/scouts/C1.md:110` and `corpus/lessons/round-62-verifier-spotcheck.md:47-48,166` | not a rule: the first records a round-21 separability sentence later found true only pre-landing; the second records a mis-cited `receipt_rev` as a defect | not a rule owner | none (evidence of the failure class, not an owner) |

Excluded as non-hits: `kengaku`/`lane3` `recovery_receipt_reviewers` (substring false positive); `kasegi` wave-2 scout list (a read list, not a rule).

Contest check. C2's relation is equality (the receipt names the revision the deciding gate certifies, or a content-identical one on the frozen surface). The closest sibling relations (rows 7, 8, 16) are ancestor or strict-descendant tests on a different field, and each is weaker than or orthogonal to equality. None refuses a receipt that C2 accepts, and none accepts a receipt that C2 refuses on the same field. Verdict: **complement**. Caveat for the lesson: the fleet uses three different relations (equality, ancestor, strict descendant) for "receipt names a revision". That is documented disagreement, not a contradiction.

## (c) Independence of the two landings

Commits that carry each claim (ancestry verified with `git merge-base --is-ancestor`; both C0 and the bind are ancestors of PIN):

- `c013745` (C0 content, `c0137451f5b7`): C2 docs (SKILL.md `## Standing rules` +13, QUALITY criterion 107 +62, SOURCES S281/S282 +4, `knowledge/receipt-revision-binding.md` +206, registry cell +33); also the C1 frozen-heading text the bind reads.
- `877eede`: C2 docs edited after C0 and before the bind (QUALITY +31, SOURCES +2, knowledge note +39). `SKILL.md`, `registry.json`, and the gate are not touched.
- `c1dd23b`: C1 bind (`ledger.json`, `rekey-r56-c0137451f5b7/*`, integration binder output).
- `2f5512a` (PIN): C1 restate (SCORECARD.md +35: the calibration row and the round-56 section; integration bind files).

Blob identities, C0 (`c013745`) vs PIN:

| Input | C0 | PIN | Read by |
|---|---|---|---|
| `SKILL.md` | `8200329abc6c` | same | C1 (frozen `## Standing rules` and 17 other frozen headings), C2 docs arm |
| `tools/registry.json` | `003b2b28dacb` | same | C2 docs arm |
| `tools/receipt-revision-gate.py` | `c77e91a2296c` | same | C2 arms 1–5 |
| `corpus/QUALITY.md` | `7799a8a4bd91` | `2af19a48b875` | C2 docs arm; monitor credit |
| `corpus/SOURCES.md` | `78df11a911a5` | `643474e5dde4` | C2 docs arm |
| `corpus/knowledge/receipt-revision-binding.md` | `38862d716440` | `94dd12e48e13` | C2 docs arm |
| `SCORECARD.md` | `54faed384783` | `4aac3baecd9d` | C1 arm 6 (restate row) only |
| `LOG.md` | `834aac53abb5` | same | not read by either counter (C1 arm 5 forbids it as a pin) |
| `c1/measure.py`, `c2/measure.py` | unchanged | unchanged | — |

Verdict on (c):

- **C2 does not depend on C1's commits.** Its counter reads SKILL, QUALITY, SOURCES, the knowledge note, the registry, the gate, and the control receipts. None is changed by `c1dd23b` or `2f5512a`. Its docs commits (`c013745`, `877eede`) predate the bind. The only C2 input still missing at PIN is the controls run (arm 5), which lands after the final REV and does not involve C1.
- **C1 depends on C2's commits.** The bind at `c1dd23b` froze SKILL.md's `## Standing rules` section, whose text `c013745` wrote, and it ran after `877eede` edited QUALITY, SOURCES and the knowledge note. Wave-2 Tree D showed a QUALITY edit after the bind drops credit to 58/64, so any later edit to SKILL, QUALITY, SOURCES, or the knowledge note breaks C1 unless the bind is re-keyed. Also, the bind's `read_rev` is `C0`, while QUALITY/SOURCES/knowledge bytes at the bind's parent differ from C0 (`877eede`). The counter still credits 64/64 at PIN, so this is not a current failure, but the lesson should record that the bind's `read_rev` is not the revision where every credited byte was fixed.
- **C1's current failure is in its own commit (`2f5512a`), not in C2's chain.** The restate row's `Round-21` capital letter is the only C1 failure at PIN.
- **Landing order for the deciding run:** C2 docs (`c013745`, `877eede`) → C1 bind (`c1dd23b`) → C1 restate fix (`2f5512a` plus the case fix, not yet committed) → C2 controls at the final REV. Any commit to SKILL, QUALITY, SOURCES, or the knowledge note after `c1dd23b` requires a new bind before the counters are re-run.

## Verification and handoff

- Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0.
- Counter commands and verdict lines are reproducible: quoted above. The PIN verdicts are the ones the deciding run will see if nothing else moves; the L1 must commit the case fix and then re-run at the new REV.
- Limitations: `treeC1` and `treeC2` are scratch commits; their C2 own receipts are synthetic. Neither the C1-only nor the C2-only verdict is admission evidence. The official `controls.sh` run (bootstrap, then the second run) is outside this seat.
- Recommended for L1: (1) commit the one-character SCORECARD.md:2718 fix; (2) re-run both counters at the new REV from the clean tree; (3) run the controls at that REV in the bootstrap sequence; (4) the do-nothing C2 attack remains recorded as the counter's declared provenance limit.

## Addendum — the lane moved after PIN

While this seat ran, the lane advanced to `8c20d5c351b3` (`round-56: correct scorecard evidence predicates`). Its only C1-relevant change is SCORECARD.md:2718, `Round-21` → `round-21`, byte-identical to the scratch patch in `treeC1` above; it also rewrites the C2 `before` cell of the frozen-claims table (not a counter input). Both counters were measured at PIN `2f5512a` as the seat specified; the C1 verdict at PIN is therefore `total=1` (arm 6 only), and the case fix that the L1 has since landed is the one verified in `treeC1` (`total=0`). The deciding run must re-run both counters at the final REV (≥ `8c20d5c`) and re-run the controls there.
