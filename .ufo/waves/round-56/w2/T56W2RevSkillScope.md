# T56W2RevSkillScope — SKILL.md drift scope (round 56, wave 2)

**Seat:** `T56W2RevSkillScope` (reviewer) · **Lane:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
**Base:** `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1` · **C0:** `c0137451f5b7f22d65f748fc69f1b181f55e1378`
**Axis judged:** calibration · **Milestone:** SKILL.md drift scope

> **Handoff — attempt 2 (`TameshiR56a2`) owns the round.** This report is the SKILL.md drift-scope
> deliverable. Two items need a decision before the bind:
> **(1) F1 (§3a)** — the round's own +13 edit breaks the page-local anchor surface inside the
> eighteen headings being re-read; two readers have reported it as true findings, and the frozen
> binder refuses to bind a reader with findings (`REFRESH rekeyed=6 skipped=12 headings=18`, where
> `rekeyed=18 skipped=0` is required). A text fix costs eighteen re-reads, so F1 must be **deferred
> to round 57 and named in the lesson**; the bind still needs to complete, which needs a
> `resolutions` file naming the two headings with `n >= 1` (`bind.sh`'s `RESOLUTIONS=` flag exists
> for exactly this) — or the L1's explicit adjudication.
> **(2) R1 (§5)** — `SKILL.md` must be byte-identical at C0 and at the deciding revision; nothing in
> `bind.sh`, `deciding-run.sh`, `contract.json`'s `frozen_paths`, or round-18's `IGNORED_INPUTS`
> enforces it. Run `validate-readers.py` at the candidate deciding revision before the bind
> (it already computes `READER_HASH_XREV_DRIFT`).

**Verdict: the round's SKILL.md edit is confined to exactly ONE section, `## Standing rules`, and that
section is already one of the eighteen frozen headings — so the edit creates no *new* reader
obligation. The other seventeen frozen headings are byte-identical at base and at C0.**

**One finding (F1):** the edit's 13 inserted lines shift the target of **125 of the 155** page-local
`:NNN` anchors in `SKILL.md` by exactly +13 — **29 of them inside the eighteen headings being
re-read**. Two readers have already reported it as true findings, and the frozen binder refuses to
bind a reader with findings, so **the bind cannot currently complete 18/18**. This is the R55.3
harm class ("the round's own edits cost cold-read credit") on a surface the round's instruments do
not measure. See §3a.

**One self-correction (F2, §6a):** this seat's first pass claimed "no false statement in the changed
section". That was an **overclaim** — it checked only that the four refusal codes *exist*, not the
table's role→code *mapping*, which is false. `T56W2Read07`'s finding is correct and this seat
verifies it independently against the C0 gate. The corrected statement: the changed section's table
mis-states the gate's role→code mapping in row 1 and omits seven of the gate's refusal codes.
Rows 3 and 4 are true as written. The attempt-2 L1 has adjudicated this (`resolutions.json`,
`## Standing rules`, n=3, `gap-minor`) and deferred the repair to round 57; this seat's
verification confirms that adjudication.

---

## 1. The hunk — exactly one, inside `## Standing rules`, nothing else

```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff \
    981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1 \
    c0137451f5b7f22d65f748fc69f1b181f55e1378 -- SKILL.md
```

```diff
@@ -42,6 +42,19 @@ Appendix A/B mutants (`.ufo/evidence/kaika-round-1/coldread/`); round 16 adds a
   corpus/knowledge/scratch-root-contract.md; the seven registry `scratch_root`
   cells).
 
+- **A receipt is evidence only for the revision it names.** A verdict or a
+  positive-control receipt is bound to the revision it certifies by
+  `tools/receipt-revision-gate.py --lane LANE --certified REV`: a receipt that
+  names another revision is refused with a named code, never re-read as if it
+  had been measured at the certified one (round-56 C2; ER-R54-1, R55.5).
+
+  | situation | rule | code |
+  |---|---|---|
+  | a verdict receipt names another revision | refused unless its bytes equal the certified revision on the declared `--paths` surface | `RECEIPT_REV_MISMATCH` |
+  | a positive control was scored at the freeze | refused: the freeze predates the work it certifies and drifts on the frozen surface | `RECEIPT_REV_CONTENT_DRIFT` (no `--paths`: `RECEIPT_REV_MISMATCH`) |
+  | a control set's CTL lines name a revision absent from the repo | refused: the revision cannot be resolved, so nothing is certified | `RECEIPT_REV_UNRESOLVABLE` |
+  | a receipt names no revision at all | refused: nothing is bound | `RECEIPT_REV_ABSENT` |
+
 ## Source notes
```

| assertion | evidence | result |
|---|---|---|
| exactly one hunk | `grep -c '^@@' verbatim.diff` → `1` | **CONFIRMED** |
| pure insertion, no deletion | `git diff --numstat` → `13	0	SKILL.md` | **CONFIRMED** |
| the 13 added lines sit at C0 lines 45–57 | located by exact-match of the added lines in the C0 file | **CONFIRMED** |
| `## Standing rules` spans C0 lines 17–57 | frozen round-18 `sectionize` at C0 | **CONFIRMED** |
| added block ⊂ section bounds | `17 ≤ 45` and `57 ≤ 57` | **CONFIRMED** |
| the section's next heading is untouched | C0 line 58 = `## Source notes`; base line 45 = `## Source notes` | **CONFIRMED** |
| the section body is a prefix-preserving insert (no rewrite) | `difflib` opcodes = `[equal base[17..43], insert c0[44..56]]`; base body is a prefix of C0 body | **CONFIRMED** |

**Method.** Every sha and every line range in this report comes from the **frozen round-18
sectionize**, imported from `.ufo/evidence/round-18/measure.py` — never reimplemented. That blob is
byte-identical at base and at C0 (`git rev-parse <base>:.ufo/evidence/round-18/measure.py` and
`<C0>:...` both → `9643f7032ae6fde843464d4ef6bc0c5919518528`), and unchanged across the round.

---

## 2. Per-heading equality table — the seventeen

Frozen list: `.ufo/evidence/round-56/c1/lost-headings-at-base.json` (18 headings, all in `SKILL.md`).
`base==C0` is decided twice: by the frozen `sectionize` sha, and by a **raw byte comparison** of the
section body (line slice, trailing blanks stripped) — both agree on all eighteen.

| # | heading | base lines | C0 lines | base==C0 (bytes) | `section_sha256` at C0 |
|---|---|---|---|---|---|
| 1 | `## Context gate classification and explicit exit classes — round 15` | 1639–1705 | 1652–1718 | **EQUAL** | `132cfb9ef1aa07111af42389e4fe862152e3118b3a8bb66f1d84a6a332e7edf6` |
| 2 | `## Effective expectation reconciliation — round 14` | 1593–1626 | 1606–1639 | **EQUAL** | `6110606ea4a977c70f0fa67ef8bdc97b4a4d2e51e9e8c2a96e984c7886376cbe` |
| 3 | `## Live-tree re-pin and entry-command monitor — round 17` | 1844–1875 | 1857–1888 | **EQUAL** | `6395900104ed76b6f9dbfae1bb33384197982447e1db7dbaf89bf2b6b1b9beac` |
| 4 | `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` | 146–260 | 159–273 | **EQUAL** | `77d88c0226463dfc97f0074a5cafedc1044be0a2a16c85fbb6237ac06a5140da` |
| 5 | `## Pin disposition and provenance correction — round 13` | 1546–1576 | 1559–1589 | **EQUAL** | `1fa3130bc6d4bc46124a1c0e234583657bb6c7623256dfa85f4db2a7fb91da31` |
| 6 | `## Repeated controls and gate registry — round 12` | 1508–1527 | 1521–1540 | **EQUAL** | `3a78cbfcef65ada68c09342e5cbc71dc067d2b5258c3afbff6ea94e37a82b831` |
| **7** | **`## Standing rules`** | **17–44** | **17–57** | **CHANGED** | **`28bde4663c463ad40eba050dc9e5a97c6ed68148414cdfaf6d36789db5160bcc`** |
| 8 | `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` | 936–949 | 949–962 | **EQUAL** | `430dd86f25b6ce3d5ed51012d54de7cdad7213c6353eb7701323de762b9fb993` |
| 9 | `## The operator's runbook and the six-leg regression (round 10, measured)` | 1299–1307 | 1312–1320 | **EQUAL** | `636e850f885cb39904d100f67446e1039aa48c6510c2a66ea6e6d5aaa089faf7` |
| 10 | `### Gate/probe registry` | 1528–1545 | 1541–1558 | **EQUAL** | `99285e24a71a8d2a0ea3fd6bcafe7e080acb23bfd653e7cbb3b71dfdc5144c77` |
| 11 | `### Round-13 gate/probe registry` | 1577–1592 | 1590–1605 | **EQUAL** | `896722c4941841f228810678befe82e9910cc66eb67c3de45d7561ce4668566d` |
| 12 | `### Round-15 gate/probe registry` | 1706–1736 | 1719–1749 | **EQUAL** | `78edbb693cdddcab61902811985918087529c444d3fb01da7bcaf4a674daf4ea` |
| 13 | `### Round-17 gate/probe registry — re-pin and monitor` | 1876–1884 | 1889–1897 | **EQUAL** | `309f83283e7518eb00cf7ce4296daf4bf5e80843ff2b3046755eb55d3ba8fb8c` |
| 14 | `### Round-18 gate/probe registry — routed-defect closure` | 1955–1967 | 1968–1980 | **EQUAL** | `661f63518af62b198f68ec5400778d9662df725d84744ad428dacc08823e6d7e` |
| 15 | `### Round-21 gate/probe registry — finite environment differential` | 1994–2133 | 2007–2146 | **EQUAL** | `eccd3ec82207fa69cee544f8f4ebfc0f9a473fe7254b8041ae2f5924f8d00a06` |
| 16 | `### Round-26 gate/probe registry — report interop` | 2162–2201 | 2175–2214 | **EQUAL** | `cc23587b353fb780d4310aebc7277e4030729ae767850e2e826d2ff151bdea52` |
| 17 | `### The service's limits — what tameshi refuses to mutation-test` | 1269–1298 | 1282–1311 | **EQUAL** | `7e240e714c6e6fa75a01061ef171238401b3a91fdd69cc86c13f97b151b848f6` |
| 18 | `### Triggers T1–T3 and the re-pin rule` | 1087–1109 | 1100–1122 | **EQUAL** | `2350210704efcc3becfbcd40a63775ad591910039744ac6d072881b3deef7801` |

**Headings whose bytes changed base→C0: 1 (`## Standing rules`). Headings byte-identical: 17.**
The one changed heading **is** in the frozen list, so the round's edit is already inside the priced
scope — no reader obligation was created outside the eighteen.

### The sha256 the readers must read

> **`## Standing rules` at C0 → `28bde4663c463ad40eba050dc9e5a97c6ed68148414cdfaf6d36789db5160bcc`**
> (`start=17`, `end=57`; `cand` = `c0137451f5b7f22d65f748fc69f1b181f55e1378`)

Whole-file `SKILL.md` sha256 at C0 = `63f13766e9ea7d8f9cf7ae1b82bfe2fb5159b9d77d5aa72fd6a938702940015d`
(base = `e0ce89f7866062062f4987358e353c8626c18f56d2eb1589225af99f44d695a6`).

**Independent recomputation.** Each of the eighteen shas was recomputed by hand (raw line slice,
trailing blanks stripped, `\n`-joined, no trailing newline, sha256) and compared with the frozen
`sectionize` value: **18/18 agree**. The numbers do not depend on one function's behaviour.

**Cross-check against sibling readers.** Eight wave-2 reader reports are already on disk
(`T56W2Read05/06/09/10/11/12/17/18.json`); every one carries `cand=c0137451f5b…` and a
`section_sha256` **identical** to this seat's table. The readers and this seat do not disagree.

---

## 3. What the 13-line shift does and does not do

The insertion moves the **start line of 61 of 64 sections by exactly +13**, and changes **1**
section's sha (`## Standing rules`).

Credit binds by **sha256, never by line**: `coldread()` builds `by_sha = {entry['sha256']: [...]}`
then `matches = by_sha.get(sec['sha256'], [])`. A line shift therefore cannot invalidate a reader
report or an existing credit. Only a section-**body** edit can. Confirmed in a fixture: editing one
line inside `## Standing rules` moved **0** start lines and changed exactly **1** sha.

---

## 3a. **FINDING — the +13 shift breaks the page-local anchors, and the round did not price it**

This is the one substantive finding of the seat, and it is a consequence of the round's own edit.

`SKILL.md` states the convention itself (C0 line 1290): *"Anchors `:…` are this page"*. The
document carries **155 page-local anchors** of the form `:NNN` / `:NNN-MMM`. The round's 13-line
insertion at line 45 shifts every anchor's target **+13 lines**.

Measured by locating the content each anchor names (script `anchor_stale.py`, over the floor/base/C0
blobs):

| | anchors | resolving correctly | staleness of the rest |
|---|---|---|---|
| at **floor** `0a2010ac` | 155 | 155/155 | 0 |
| at **base** `981c5e8b` | 155 | **27/155** | **+4 lines** (109 anchors) — round-55's debt |
| at **C0** `c0137451f5b7` | 155 | **27/155** | **+17 lines** (109 anchors) |

**The round-56 edit adds exactly 13 to the staleness of all 109 already-stale anchors**
(`delta distribution: {13: 109}`) and **breaks none that was correct at base**. So:

* the anchors were **already broken by round-55** (+4) — inherited debt, not this round's;
* **this round's edit makes 109 of them 13 lines further wrong**, and **29 of those anchors sit
  inside the eighteen frozen headings** — including **12 in `### The service's limits`** and
  **6 in `### Triggers T1–T3 and the re-pin rule`**;
* the round's own lesson file records the R55.3 harm as *"the round's own edits cost the cold-read
  monitor 18 of 64 credited sections"* — but the same class of harm is being repeated on the
  **page-local anchor surface**, and this time it lands **inside the very sections being re-read**.

**This is why two readers reported findings, and it is why the bind will fail.** The two readers
that carry findings are reporting *true* statements about the tree at C0:

| reader | heading | findings | what the finding is |
|---|---|---|---|
| `T56W2Read17` | `### The service's limits…` | 4 | page-local anchors `:824-828`, `:834-836`, `:851-855`, `:890-892`, `:1023-1169` are **17 lines early at C0** and land on unrelated text |
| `T56W2Read06` | `## Repeated controls and gate registry — round 12` | 1 | `corpus/SOURCES.md:503` no longer records the S026→S265 supersession |

**Read17's arithmetic is correct.** Its `:1023-1169` anchor named the round-8 cadence section's
span at floor (heading at 1023, next `##` at 1170). At base the heading is at 1027 (the anchor is
4 lines early — round-55's drift); at C0 it is at 1040, so the anchor is **17 lines early**.
4 + 13 = 17. Each of Read17's five cited anchors resolves 17 lines off at C0, and the content it
names now lives at C0 + 17 (verified anchor by anchor: `:824`→841, `:834`→851, `:851`→868,
`:890`→907, `:1023`→1040).

**Read06's finding is also true, and it is induced by the round's `corpus/SOURCES.md` edit.**
The round-56 commit added two S-rows (`S281`, `S282`) at SOURCES.md lines 156–157, shifting every
later line by 2. `corpus/SOURCES.md:503` at base reads *"- Next unused id: S265 (staged ids
S161–S255 stay reserved by document for the package)."*; at C0 line 503 reads *"- Next unused id:
S265 (S261–S264 are map-only reserved; …)"* and the cited base content has moved to line 505. The
S026→S265 supersession is recorded at line 140 (row `S265`) and in the round-48 note at line 506 —
not at 503.

**Consequence for the bind.** `bind.sh` passes `--resolutions` at a non-existent path, so
`allowed == 0` for every heading and any reader with a non-empty `findings` list is skipped
(`reader-has-findings:N>0`). Running the **frozen binder** against the **real** wave-2 reports:

```
binder rc: 1
REKEY ## Pin disposition and provenance correction — round 13 start=1559 inputs=33 dropped=0 reader=T56W2Read05
REKEY ## The operator's runbook and the six-leg regression (round  start=1312 inputs=11 dropped=0 reader=T56W2Read09
REKEY ### Gate/probe registry start=1541 inputs=124 dropped=0 reader=T56W2Read10
REKEY ### Round-13 gate/probe registry start=1590 inputs=24 dropped=0 reader=T56W2Read11
REKEY ### Round-15 gate/probe registry start=1719 inputs=38 dropped=0 reader=T56W2Read12
REKEY ### Triggers T1–T3 and the re-pin rule start=1100 inputs=89 dropped=0 reader=T56W2Read18
SKIP ## Context gate classification and explicit exit classes — r no-clean-reader
SKIP ## Effective expectation reconciliation — round 14 no-clean-reader
SKIP ## Live-tree re-pin and entry-command monitor — round 17 no-clean-reader
SKIP ## Mutation-sweep recipe — numbered steps; bounded cold-read no-clean-reader
SKIP ## Repeated controls and gate registry — round 12 reader-has-findings:1>0
SKIP ## Standing rules no-clean-reader
SKIP ## The leg ledger — replay, receipt, and how it is read (rou reader-md-missing
SKIP ### Round-17 gate/probe registry — re-pin and monitor no-clean-reader
SKIP ### Round-18 gate/probe registry — routed-defect closure no-clean-reader
SKIP ### Round-21 gate/probe registry — finite environment differ no-clean-reader
SKIP ### Round-26 gate/probe registry — report interop no-clean-reader
SKIP ### The service's limits — what tameshi refuses to mutation- reader-has-findings:4>0
REFRESH rekeyed=6 skipped=12 headings=18
```

`bind.sh` requires `REFRESH rekeyed=18 skipped=0 headings=18`; the actual line is
`rekeyed=6 skipped=12 headings=18` → **the bind aborts** (`BIND error=binder-exit-1`). The six
`no-clean-reader` skips are the nine readers not yet delivered; `reader-md-missing` is
`T56W2Read08` (its `.md` is absent — only the `.json` is on disk); the two
`reader-has-findings:N>0` skips are Read06 and Read17.

**The two `reader-has-findings` skips are the round's own doing, and they are TRUE findings.** The
readers correctly reported that the round's edit broke anchors inside the sections being re-read.
The L1's options are (a) adjudicate the two findings as accepted (a `resolutions` file naming
those two headings with `n >= 1`, which the binder's `--resolutions` flag exists to permit), or
(b) defer them to round 57 and accept that this round's bind cannot reach 18/18. Either way the
round must **name this in the lesson**: the R55.3 class ("the round's own edits cost cold-read
credit") has a second surface — the page-local anchor surface — and the +13 shift lands **inside
the eighteen headings the round is paying eighteen re-reads to fix**.

---

## 4. Attribution: the SKILL.md edit is NOT what costs the eighteen

This is the load-bearing result of the seat. Monitor sweep along the commit chain
(`python3 .ufo/evidence/round-21/coldread/measure.py --repo LANE --rev REV`, the frozen monitor):

| rev | covered | score | box3 | uncovered |
|---|---|---|---|---|
| floor `0a2010acd1e9` | **64/64** | 8 | True | 0 |
| base `981c5e8b20a2` | 46/64 | 6 | False | 18 |
| C0's parent `21eb3c6` | 46/64 | 6 | False | 18 |
| C0 `c0137451f5b7` | 46/64 | 6 | False | 18 |

**Newly uncovered by the C0 commit: ∅. Restored by the C0 commit: ∅.** The C0 commit changed the
*identity* of one loss (`## Standing rules`: sha `acfb671a…` → `28bde466…`) but changed no
section's credit status.

The eighteen lost sections split as:

| cause | count | detail |
|---|---|---|
| **input drift on files the round changed** | 3 | `## Pin disposition…` (SOURCES.md), `## The leg ledger…` (SOURCES.md), `## The operator's runbook…` (registry.json) |
| **input drift already present at base (inherited R55 debt)** | 14 | drift on `tools/context-capture.py`, `tools/registry-check.py`, `tools/repeat-control.py`, `tools/bash-witness-study.py`, `tools/pin-disposition.py`, `tools/evidence-disposition.py`, `tools/mutate-and-run.sh`, `corpus/knowledge/service-limits.md`, `.ufo/evidence/round-15/verify.py` — none of these changed base→C0 |
| **both** (drift on a round-56-changed file *and* on inherited files) | 2 | — |
| **no sha-keyed ledger entry at all** | 1 | `## Standing rules` |

**So the SKILL.md hunk costs exactly one of the eighteen — and that one (`## Standing rules`) is
already on the re-read list.** The other seventeen are lost to input drift on `corpus/SOURCES.md`,
`corpus/QUALITY.md`, `tools/registry.json` and friends — the round-55 damage the re-key exists to
repair. The round's SKILL.md edit adds **no** unpriced reader obligation.

---

## 5. Residual risks the L1 must price before the bind

### R1 (highest) — a post-C0 `SKILL.md` edit orphans the re-key entry, and nothing in the chain catches it before the bind

The binder writes the section's sha **as computed at C0** into the ledger entry
(`binder-r55.py`: `skill = show(c0, 'SKILL.md')` → `sections` → `'sha256': sec['sha256']`), while
the monitor computes sections **at the revision it measures**. If `SKILL.md` changes between C0 and
the bound revision, the entry no longer matches and the section is uncovered again.

**End-to-end proof with the FROZEN binder** (clone `--shared`, `checkout --detach C0`,
`git rev-parse --show-toplevel` asserted equal to the fixture dir, no mutation in the lane):

```
binder rc: 0
REKEY ## Standing rules start=17 inputs=2497 dropped=0 reader=T56W2Read99
REFRESH rekeyed=1 skipped=0 headings=1

== (a) monitor at the bound rev (SKILL.md unchanged since C0) ==
  covered 47/64 score 6 box3 False
  '## Standing rules' uncovered? False -> None

== (b) monitor at a rev whose SKILL.md was edited after C0 ==
  section sha at C0   : 28bde4663c463ad40eba050dc9e5a97c6ed68148414cdfaf6d36789db5160bcc
  section sha at rev2 : 9d6f37afc48c5e649304f13d2fcb04814d918d4877d9ac6d05c82aeed9ed3502
  covered 46/64 score 6 box3 False
  '## Standing rules' uncovered? True -> no-ledger-entry
  arm-4 accepts the reader report: False
  (validator code: READER_HASH_XREV_DRIFT)
```

One line added to `SKILL.md` **after C0** takes the monitor from 47/64 back to 46/64, and makes the
C1 counter's arm 4 refuse the reader report.

**Why no existing guard catches it:**
- `SKILL.md` is **not** in `contract.json`'s `frozen_paths` (verified by reading the list), so the
  deciding run's `FROZEN_UNCHANGED` check cannot see it.
- `SKILL.md` is in the binder's `DROP` list, so it is never a pinned input; `bind.sh` step 3c
  ("no pinned input may move between PIN and the bound revision") cannot see it either.
- `SKILL.md` **is** in round-18's `IGNORED_INPUTS`, so pinning it in a re-key entry's `inputs`
  causes no drift and no alarm (verified: `IGNORED_INPUTS = ['.ufo/evidence/round-17/coldread/ledger.json', '.ufo/evidence/round-18/coldread/ledger.json', 'SKILL.md']`).

**Consequence for the L1:** the re-key is valid only if `SKILL.md` is byte-identical at C0 and at the
deciding revision. The binder is invoked as `C0=… PIN=…` and the C1 counter measures at `REV`.
**C0 and PIN must carry the same `SKILL.md` bytes.** If the L1 makes any `SKILL.md` edit after
reading the readers, it must re-read `## Standing rules` at the new revision too — that is exactly
the "text fix costs eighteen re-reads" rule in the reader contract, and it is currently
unenforced by the tooling rather than by the rule.

*Mitigation available now:* `validate-readers.py` already implements the check
(`READER_HASH_XREV_DRIFT`, comparing the section sha at C0 against the sha at REV). Running it at
the candidate deciding revision before the bind closes this gap; the deciding run does not
currently invoke it.

### R2 — the re-key directory must be named exactly `rekey-r56-c0137451f5b7`

The counter's `REKEY_RE = ^rekey-r56-([0-9a-f]{12})$` and `bind.sh` step 1b both require the
directory basename to be `rekey-r56-${C0:0:12}`. `git rev-parse c0137451f5b^{commit}` resolves to
`c0137451f5b7f22d65f748fc69f1b181f55e1378` and the resolved commit starts with the 12-hex prefix,
so the name is well-formed. A directory named with the **full 40-hex** would fail `REKEY_RE` and
arm 3 would find zero re-key directories.

### R3 — no old entry can veto the re-key

`coldread()` vetoes a section when an old entry has `entry_failure(...) is not None` **and** is not
stale. Analysis at C0 over all entries whose sha matches each of the eighteen: **no old entry can
veto any of the eighteen** (every failing old entry is stale — its inputs no longer verify — so it
cannot veto). The re-key's own entry is sufficient to restore each heading's credit.

### R4 — the binder's `old`-entry lookup is by `heading`, and `## Standing rules` has 8 old entries

The binder sources each re-key entry's `inputs` from the old ledger entries **with the same
heading** (not the same sha). `## Standing rules` has **8** such old entries, yielding **2497**
resolvable inputs at C0 — so it is **not** skipped as `no-stable-inputs`. All eighteen headings
resolve a non-empty input set (minimum 11, maximum 7702). The re-key is mechanically able to bind
all eighteen.

### R5 — the binder writes `gap-minor` for sixteen of the eighteen (unavoidable, and not a loss)

The binder takes `class`/`verdict` from each heading's newest old entry. Sixteen of the eighteen
are `gap-minor` (two are `wrong-expectation`, which the binder maps to `verified-record`/`executed-ok`).
`gap-minor` is in `REC_VERDICTS` and in `VALID_VERDICTS`, and `entry_failure` treats it as
non-failing, so it **credits**. A reader report that carries findings also sets `verdict=gap-minor`
and `minor_gaps=<n>`; `bind.sh` passes `--resolutions` at a non-existent path, so **zero findings
are allowed per heading** — a reader report with findings is skipped as
`reader-has-findings:N>0` and the round stops. This is the designed fail-closed behaviour, but it
means **every one of the eighteen readers must land with an empty `findings` list** for the bind to
complete in one pass. (`T56W2Read06.json` currently carries `verdict=gap-minor`; its `findings`
count should be checked against that heading's `findings` list before the bind.)

---

## 6. The changed section's own claims — checked against the tree at C0

| claim in `## Standing rules` | check | result |
|---|---|---|
| `tools/receipt-revision-gate.py --lane LANE --certified REV` exists | `git cat-file -e <C0>:tools/receipt-revision-gate.py` | **TRUE** (16 741 bytes) |
| the tool accepts `--lane` / `--certified` / `--paths` / `--receipt` | CLI parse of the C0 blob | **TRUE** (all four) |
| the codes `RECEIPT_REV_MISMATCH`, `RECEIPT_REV_CONTENT_DRIFT`, `RECEIPT_REV_UNRESOLVABLE`, `RECEIPT_REV_ABSENT` are the ones the tool defines | the four codes appear in both the section table and the gate source | **TRUE** (all four, both sides) |
| the gate actually works | `python3 <C0 blob> --selftest` | **TRUE** — `GATE_SELFTEST: 19/19 pass`, exit 0 |
| the citations `ER-R54-1` and `R55.5` exist in the corpus at C0 | grep over `corpus/QUALITY.md`, `corpus/lessons/round-56.md`, `corpus/knowledge/receipt-revision-binding.md` at C0 | **TRUE** (both found) |

### 6a. CORRECTION to this seat's own earlier claim — the table's role→code mapping is wrong

**This seat's first pass checked only that the four codes exist on both sides. That was an
overclaim: it did not check the table's role→code *mapping*, which is false. `T56W2Read07`'s
finding F2 is correct and this seat verifies it independently.**

The section's table keys a refusal code to the receipt's **ROLE**:

> \| a verdict receipt names another revision \| … \| `RECEIPT_REV_MISMATCH` \|<br>
> \| a positive control was scored at the freeze \| … \| `RECEIPT_REV_CONTENT_DRIFT` (no `--paths`: `RECEIPT_REV_MISMATCH`) \|

The gate keys it to **`--paths` + drift**, not to the role (`tools/receipt-revision-gate.py`
`check()`, lines 139–154): for `role_name in ('positive','verdict')`, `full != certified` gives
`RECEIPT_REV_MISMATCH` when `paths is None`, else `RECEIPT_REV_CONTENT_DRIFT` when the declared
surface drifted — **identically for both roles**.

Measured on the **same receipt bytes** (the round's own red-before round-54 receipt, `rev=077d431e6996`,
certified `c21081008adb`), at a clone at C0:

```
role=verdict   --paths=True  exit=3 codes=['RECEIPT_REV_CONTENT_DRIFT']
role=verdict   --paths=False exit=3 codes=['RECEIPT_REV_MISMATCH']
role=positive  --paths=True  exit=3 codes=['RECEIPT_REV_CONTENT_DRIFT']
role=positive  --paths=False exit=3 codes=['RECEIPT_REV_MISMATCH']
```

**Both roles give byte-identical codes.** So the table's row 1 is wrong in the case it most
matters: a **verdict** receipt naming another revision, checked on the declared `--paths` surface,
is refused with **`RECEIPT_REV_CONTENT_DRIFT`**, not `RECEIPT_REV_MISMATCH`. Row 2's parenthetical
("no `--paths`: `RECEIPT_REV_MISMATCH`") is the only part of the table that describes the real
selection rule.

The other two rows **are** true as written, verified by running the gate:

| table row | measured |
|---|---|
| row 3 — a control's CTL lines name an absent revision → `RECEIPT_REV_UNRESOLVABLE` | **TRUE** (role=control, absent rev → `codes=['RECEIPT_REV_UNRESOLVABLE']`) |
| row 4 — a receipt names no revision at all → `RECEIPT_REV_ABSENT` | **TRUE** (all three roles → `codes=['RECEIPT_REV_ABSENT']`) |

**Also incomplete (not false):** the gate can emit **seven codes the table never names** —
`RECEIPT_CONTROL_NOT_ANCESTOR`, `RECEIPT_REV_AMBIGUOUS`, `RECEIPT_MISSING`, `RECEIPT_EMPTY`,
`RECEIPT_NOT_BLOB`, `RECEIPT_REQUIRED_LINE_MISSING`, `RECEIPT_DIGEST_MISMATCH`. A reader who
treats the table as the gate's code list will not recognise those refusals.

**Consequence.** `T56W2Read07` (the reader for the section this round edited) reported this as a
true finding; the attempt-2 L1 has adjudicated it (`resolutions.json`, `## Standing rules`, n=3,
verdict `gap-minor`) and deferred the repair to round 57, because a SKILL.md text fix costs
eighteen re-reads. **This seat's earlier "no false statement found in the changed section" was
wrong and is withdrawn**; the corrected statement is: *the changed section's table mis-states the
gate's role→code mapping in row 1 and omits seven of the gate's refusal codes.*

---

## 7. Census

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --root /home/vgpnk/Projects/shokunin tameshi
tameshi	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
… (16 advisory lines, identical to the frozen .ufo/evidence/round-56/census-start.stdout) …
tameshi	ok	/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
EXIT=0
```

**Exit 0 — PASS.** The census output is byte-identical to the round's frozen start-of-round
evidence (`.ufo/evidence/round-56/census-start.stdout`).

**Note on the row count (a discrepancy in the assignment brief, not a defect in the tree):**
the brief says "141 rows after this round's one new row". The census parser reports
`tameshi rows 142`, and the arithmetic is `floor 139 → base 140 → C0 142`: this round added **two**
rows (`S281` in-toto Statement spec, `S282` SLSA build-provenance predicate), not one. Both new rows
are present in the C0 blob and the census exits 0, so the *requirement* ("must exit 0") is met; only
the brief's parenthetical count is off by one row and off by one new row.

---

## 8. Findings

**F1 — the round's own SKILL.md edit breaks the page-local anchor surface, including inside the
eighteen headings being re-read.** (Full evidence in §3a.)

The edit inserts 13 lines at line 45 and shifts the target of **125 of the 155** page-local anchors
in `SKILL.md` by exactly +13. **109** of them were already stale by +4 (round-55's debt); the round
makes them **17 lines** off. **29** of the shifted anchors sit inside the eighteen frozen
headings — 12 in `### The service's limits`, 6 in `### Triggers T1–T3 and the re-pin rule`,
2 each in `## Context gate classification…`, `## Mutation-sweep recipe…`, `## Pin disposition…`,
`## The leg ledger…`, and 1 each in `## Live-tree re-pin…`, `## Repeated controls…`,
`### Round-18 gate/probe registry…`.

This is the **same harm class as R55.3** ("the round's own edits cost the cold-read monitor 18 of
64 credited sections"), on a surface the round's instruments do not measure, landing **inside the
sections the round is paying eighteen re-reads to repair**. Two readers have already reported it,
and their findings are **true** — which the frozen binder refuses to bind
(`reader-has-findings:1>0`, `reader-has-findings:4>0`).

The round's own lesson file (`corpus/lessons/round-56.md`) must name this, and the L1 must decide
how the two findings are adjudicated. **A text fix costs eighteen re-reads**, so per the reader
contract this must be **deferred to round 57, not fixed here** — but the deferral must be
recorded, and the bind must be made to complete despite the two readers' findings (a
`resolutions` file naming those two headings with `n >= 1`, which is exactly what
`bind.sh`'s `--resolutions` flag exists for).

**No other finding of my own.** The SKILL.md edit is confined to one section, that section is already
among the eighteen frozen headings, the other seventeen are byte-identical base↔C0, and the changed
section's *existence* claims are all true of the tree at C0.

**F2 — this seat's own earlier claim was an overclaim, withdrawn.** §6 originally read "no false
statement and no failing command found in the changed section". That checked only that the four
refusal codes **exist** on both sides; it did not check the table's role→code **mapping**, which
is **false**. `T56W2Read07`'s finding F2 is correct, and this seat verifies it independently by
running the C0 gate on identical receipt bytes across both roles with and without `--paths`:
`role=verdict` and `role=positive` give **byte-identical codes** in all four combinations. The
table's row 1 ("a verdict receipt names another revision → `RECEIPT_REV_MISMATCH`") is wrong for
the case it most matters — a verdict receipt checked on the declared `--paths` surface is refused
with **`RECEIPT_REV_CONTENT_DRIFT`**. The table also omits **seven** codes the gate can emit
(`RECEIPT_CONTROL_NOT_ANCESTOR`, `RECEIPT_REV_AMBIGUOUS`, `RECEIPT_MISSING`, `RECEIPT_EMPTY`,
`RECEIPT_NOT_BLOB`, `RECEIPT_REQUIRED_LINE_MISSING`, `RECEIPT_DIGEST_MISMATCH`). Rows 3 and 4
**are** true as written. Full evidence and the corrected statement: §6a. The attempt-2 L1 has
already adjudicated F2 (`resolutions.json`, `## Standing rules`, n=3, `gap-minor`) and deferred the
repair to round 57; this seat's independent verification confirms that adjudication.

**Items for the L1 to price (not findings against the round — no command failed):**

1. **R1** — `SKILL.md` must be byte-identical at C0 and at the deciding revision. Nothing in
   `bind.sh`, `deciding-run.sh`, `contract.json`'s `frozen_paths`, or round-18's `IGNORED_INPUTS`
   currently enforces this; a one-line post-C0 edit silently takes the monitor 47/64 → 46/64 and
   makes arm 4 refuse the reader report. `validate-readers.py` already computes the check
   (`READER_HASH_XREV_DRIFT`); run it at the candidate deciding revision before the bind, or add
   `SKILL.md` to `frozen_paths`.
2. **R5** — `bind.sh` passes `--resolutions` at a non-existent path, so **zero findings are
   allowed** on every one of the eighteen readers; any reader with a non-empty `findings` list is
   skipped as `reader-has-findings:N>0` and the bind aborts. Measured against the real reports:
   `REFRESH rekeyed=6 skipped=12 headings=18` where `rekeyed=18 skipped=0` is required. Two of the
   twelve skips are F1's readers; `T56W2Read08` is additionally missing its `.md`
   (`reader-md-missing`).
3. **R2** — name the re-key directory exactly `rekey-r56-c0137451f5b7` (12 hex, not 40).
4. **Census count** — 142 rows after **two** new rows (`S281`, `S282`), not 141 after one; the
   census exits 0 as required.

---

## 9. Commands run

```bash
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff \
    981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1 \
    c0137451f5b7f22d65f748fc69f1b181f55e1378 -- SKILL.md
git -C … diff --numstat 981c5e8b… c0137451f5b… -- SKILL.md          # 13  0  SKILL.md
git -C … diff -U0 981c5e8b… c0137451f5b… -- SKILL.md               # @@ -44,0 +45,13 @@
git -C … rev-parse 981c5e8b…:.ufo/evidence/round-18/measure.py \
                   c0137451f5b…:.ufo/evidence/round-18/measure.py  # 9643f703… (identical)
git -C … show c0137451f5b…:SKILL.md | (frozen round-18 sectionize)  # 64 sections
git -C … show c0137451f5b…:corpus/SOURCES.md | grep -cE '^\| *S[0-9]+ '   # 142
git -C … show c0137451f5b…:tools/receipt-revision-gate.py | python3 - --selftest  # 19/19
git -C … rev-parse --verify --quiet 'c0137451f5b^{commit}'          # c0137451f5b7f22d…
python3 .ufo/evidence/round-21/coldread/measure.py --repo LANE --rev {0a2010ac,981c5e8b,21eb3c6,c0137451f5b}
bash .ufo/evidence/round-48/quality/coldread-precheck.sh LANE 0a2010ac… c0137451f5b…
python3 .ufo/evidence/round-56/c1/measure.py --lane LANE --rev c0137451f5b… --work EMPTY --explain
python3 .ufo/waves/round-56/validate-readers.py --lane . --rev c0137451f5b… --c0 c0137451f5b… --work EMPTY --explain
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin   # rows 142
# F1 anchor analysis (read-only, over the three SKILL.md blobs):
#   anchor_stale.py    staleness of each of the 155 anchors at floor / base / C0
#   anchor_split.py    the +4 (round-55) / +13 (round-56) split, and reach into the eighteen
#   anchor_decide.py   Read17's "17 lines early" arithmetic
#   findings_induced.py  Read06's corpus/SOURCES.md:503 finding, and Read17's five anchors
#   verify_f2.py          F2: the C0 gate on identical receipt bytes, both roles, +/- --paths
#   verify_table_rows.py  every row of the added table against the C0 gate
# fixtures (all in scratch, all `git rev-parse --show-toplevel` asserted == the fixture dir):
#   fixture_drift.py    one post-C0 SKILL.md edit vs arm-4's sha comparison
#   fixture_pos2.py     positive control: a crediting re-key entry lifts coverage 46 -> 47
#   fixture_binder.py   end-to-end with the FROZEN binder: bind, then a post-C0 edit
#   fixture_r5.py       the FROZEN binder against the REAL wave-2 reader reports (the 12 skips)
```

**Tools:** none installed. No `pacman`, no `uv tool`, no `npx`, no binary in `~/.local/bin` —
the task needed only `git`, `python3` (stdlib), and `bash`, all already present.
`/home/vgpnk/.omp/agent/RULES.md` was not consulted because no install was performed.

**Scratch:** `/fast/scratch/hyaku/tameshi-r56/T56W2RevSkillScope` (fixtures under
`fixture-*/`, all `git clone --shared` + `checkout --detach`; no lane file was modified; no
mutating git command was run against the lane).

**Lane production files edited by this seat: none.**
