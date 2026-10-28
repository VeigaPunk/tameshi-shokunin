# T56W2Read17 — cold read: `### The service's limits — what tameshi refuses to mutation-test`

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (absolute paths only; no lane production file, frozen instrument or wave spec was edited; no mutating git command was run anywhere).
- Content commit (`cand`): `c0137451f5b7f22d65f748fc69f1b181f55e1378`
- Section at C0: `SKILL.md` lines **1282-1311** (body 1282-1310, 29 lines), `section_sha256` **`7e240e714c6e6fa75a01061ef171238401b3a91fdd69cc86c13f97b151b848f6`**
- Item: 17 of 18 frozen headings (`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-56/c1/lost-headings-at-base.json`).
- Verdict: **gap-minor** — 4 findings, all one defect class (page-local `:NNN` anchors that no longer resolve). **No `SKILL.md` edit was made**; the findings are for the L1 to adjudicate and defer to round 57.

## Reader command and output

```
git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin clone && git -C clone checkout --detach c0137451f5b7f22d65f748fc69f1b181f55e1378
```

```
git -C clone show c0137451f5b7f22d65f748fc69f1b181f55e1378:SKILL.md
```

The section sha was computed with the **frozen** round-18 `sectionize()` (loaded via `importlib` from
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py`, never reimplemented),
over the C0 `SKILL.md` blob:

```
start=1282 end=1311 sha256=7e240e714c6e6fa75a01061ef171238401b3a91fdd69cc86c13f97b151b848f6
```

Cross-checked with the lane's own helper, which returns the identical start/end/sha:

```
python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin c0137451f5b7f22d65f748fc69f1b181f55e1378 "### The service's limits — what tameshi refuses to mutation-test"
```

```
{"heading": "### The service's limits \u2014 what tameshi refuses to mutation-test", "cand": "c0137451f5b7f22d65f748fc69f1b181f55e1378", "start": 1282, "end": 1311, "section_sha256": "7e240e714c6e6fa75a01061ef171238401b3a91fdd69cc86c13f97b151b848f6"}
```

Receipts: `.ufo/waves/round-56/w2/T56W2Read17-receipts/` —
`anchor-resolution-at-c0.txt`, `drift-provenance.txt`, `tool-behaviour-row-b.txt`, `claims-that-resolve.txt`.

## The section (verbatim, C0)

```
### The service's limits — what tameshi refuses to mutation-test

The note states its own role as "the refusal table the re-sweep cadence
applies at intake" (`service-limits.md:4-5`); no cadence or ledger text names
it (`:1023-1169`, `fleet-kill-rate-ledger.md:285`, `fleet-kill-rate-ledger.md:318`) — the
intake application is the note's claim, quoted as stated, not a cadence fact
this page asserts. Each refusal carries a measured anchor —
a refusal without an anchor is not written; the table states refusals, it does not
adjudicate them. (Anchors `:…` are this page; `PROVINCE.md` is repo-relative; other bare note names are under `corpus/knowledge/`.) The
standalone note `corpus/knowledge/service-limits.md` (T9-2, round 9) carries
the same rows as the detail of record — verbatim anchor quotes, the trigger column
and the intake-precondition check; this page is the compact rendering, and a
divergence between the two is the finding, never smoothed.

| # | Refusal | What it means | Anchor |
|---|---|---|---|
| a | No pinned revision / no opted-in lane | no sweep — the queue is an offer, not a schedule; a round with no opt-in records the no-opt-in line | `service-optin-protocol.md:25-30`; `fleet-suite-census.md:277-286` |
| b | No one-command hermetic suite | refused before any suite runs — the request shape requires it; spec/control failures are `MUTATE: SETUP`, exit 2, no headline | `:824-828`; `:851-855` |
| c | A moved substrate without a re-pin | a recommendation, never an edit — the service never edits, repairs or re-pins a gate | `:834-836` |
| d | Live substrates / sessions | never read; a live-plane probe is a PATH-level stub, never the session | `service-optin-protocol.md:129-132` |
| e | Credential material / endpoint health | out of province — report, never absorb | `PROVINCE.md:14-18`, `PROVINCE.md:20` |
| f | Product semantics — whether a gate's verdicts are right | never measured — sensitivity ≠ truth | `:890-892`; `fleet-kill-rate-ledger.md:156-158` |
| g | Coordinated multi-edit rewrites | outside the defect vocabulary — no rate claimed | `fleet-kill-rate-ledger.md:220` (U2) |
| h | The exit-flatten family | a harness boundary — named, not fixed | `service-optin-protocol.md:267-269` |
| i | A directed-repair re-run presented as a rate | recorded as directed repair, not an independent rate | `fleet-kill-rate-ledger.md:35-36` |
| j | Foreign scratch | never removed | `service-optin-protocol.md:86-91` |

Anchors re-resolved 2026-10-14 on the live bytes; a reader on a differing revision
re-resolves rather than trusts.
```

## Summary

One defect class, four findings, one cause: **every page-local (`:…`) anchor in this section is
17 lines early at C0 and lands on unrelated text.** Every row's own refusal claim (a-j) is true of
the tree at C0, and every note-side anchor resolves. The defect is that the page-local pointers do
not resolve to the sentences they name.

Provenance is exact and the drift is a **regression**: these same anchors were adjudicated a
finding and repaired once already, in the round-54 C1 fix pass `99c3bc8`, whose commit message
lists *"stale SKILL anchors at C0"* among its fixes. Two later content commits moved the page again
and undid that repair — round-55's C0 (`9cf0146`) inserted 4 lines at `SKILL.md:37` (+4) and
round-56's C0 (`c013745`) inserted 13 lines at `SKILL.md:45` (+13) — so C0 sits **+17** from the
revision where the repair was byte-exact.

```
git diff -U0 99c3bc8 9cf0146 -- SKILL.md
```

```
@@ -37,3 +37,7 @@ Appendix A/B mutants (`.ufo/evidence/kaika-round-1/coldread/`); round 16 adds a
```

```
git diff -U0 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1 c0137451f5b7f22d65f748fc69f1b181f55e1378 -- SKILL.md
```

```
@@ -44,0 +45,13 @@ Appendix A/B mutants (`.ufo/evidence/kaika-round-1/coldread/`); round 16 adds a
```

Drift table (target sentence line number per revision):

| cited range | text it was written for | at `99c3bc8` (repair) | at base `981c5e8b` | at C0 `c013745` | correct C0 range |
|---|---|---|---|---|---|
| `:824-828` | opt-in contract item 2, "A one-command hermetic suite…" | 824-828 | 828 | 841 | **`:841-845`** |
| `:851-855` | protocol items 2-3, "`MUTATE: SETUP (<reason>)`, exit 2 — no headline" + red control | 851-855 | 857 | 870 | **`:868-872`** |
| `:834-836` | opt-in contract item 4, "The service never edits, repairs or re-pins the gate…" | 834-836 | 838 | 851 | **`:851-853`** |
| `:890-892` | "**Sensitivity, not truth** — a sweep measures what the suite can detect…" | 890-892 | 894 | 907 | **`:907-909`** |
| `:1023-1169` | round-8 cadence section (heading line → line before the next `##`) | 1023-1169 | 1027 | 1040 | **`:1040-1186`** |

## Findings (4)

### F1 — row (b): both page anchors land 17 lines early

Quote (byte-exact in the section):

```
| b | No one-command hermetic suite | refused before any suite runs — the request shape requires it; spec/control failures are `MUTATE: SETUP`, exit 2, no headline | `:824-828`; `:851-855` |
```

Why: the section fixes the convention itself — *"(Anchors `:…` are this page…)"* — so `:824-828`
means `SKILL.md:824-828` at the reading revision.

```
sed -n '824,828p' SKILL.md
```

```
   824	Rounds 2–5 measured three fleet gates at tameshi's hand; round 6 turns the
   825	method outward as the service the fleet census offered
   826	(`fleet-suite-census.md:249-291`): an opting-in lane brings its own gate, the
   827	service sweeps it hermetically and read-only, and returns a kill-rate table
   828	plus recommendations — absorption stays with the owner lane. The first
```

That is the round-6 service paragraph. It carries neither the opt-in contract item the first half of
the cell paraphrases, nor the failure rule the second half paraphrases. The target is:

```
sed -n '841,845p' SKILL.md
```

```
   841	2. **A one-command hermetic suite** invocable against a copy — mado's gate
   842	   takes `bash "$MUTANT" --selftest`; it must exercise the copy it is handed
   843	   (mado's selftest re-enters `$0`), print its own executed count and verdict
   844	   (`MADO_SELFTEST: 28/28 assertions passed` on green), and read no live path
   845	   (`mutation-case-mado-verify.md:44-49`).
```

The second anchor lands on a different row's text entirely:

```
sed -n '851,855p' SKILL.md
```

```
   851	4. Nothing else. The service never edits, repairs or re-pins the gate; a
   852	   needed change is a recommendation to the owner (round-6 anti-claim,
   853	   `plans/round-6.plan.md:23-25`).
   854	
   855	### The protocol — ordered, fail-closed
```

The `MUTATE: SETUP` / exit-2 / red-control rule it points at is at:

```
sed -n '868,872p' SKILL.md
```

```
   868	2. **Spec parse + uniqueness.** Every `@old` must occur exactly once (non-overlapping count), asserted
   869	   **before any suite run**; `@new == @old` is refused. Any spec failure is
   870	   `MUTATE: SETUP (<reason>)`, exit 2 — no headline.
   871	3. **Control first.** The unmutated copy must run green; a red control exits 2
   872	   (kills could not be attributed).
```

**The row's substance is TRUE at C0** — exercised, not assumed (receipt `tool-behaviour-row-b.txt`):

```
bash tools/mutate-and-run.sh --selftest
```

```
MUTATE_SELFTEST: 107/107 pass
VERDICT: PASS
rc=0
```

```
bash tools/mutate-and-run.sh --target <w>/target.sh --defects <w>/spec.txt --suite 'bash "$MUTANT"' --workdir <w>/wd
```

```
spec: line 1: unrecognized line: 'notpresent old string'
MUTATE: SETUP (spec parse failed)
rc=2   (no 'MUTATE: DONE' headline printed)
```

```
bash tools/mutate-and-run.sh --target <w>/target.sh --defects <w>/spec.txt --suite 'exit 1' --workdir <w>/wd
```

```
CONTROL: RED (exit=1 duration-ms=2 pristine-sha256=5dbad7dd0b9b122dcd9956884390f4aac4738caba8ff53498a7ab6718b176c30)
  | (no output)
MUTATE: SETUP (control run on the pristine copy is red (exit=1); cannot attribute kills; log: …/evidence/control.out)
rc=2
```

So the defect is precisely that the two cited ranges no longer resolve to the sentences the cell
names. Provenance: at `99c3bc8` both ranges were byte-exactly the cited text.

```
git show 99c3bc8:SKILL.md
```

```
   824	2. **A one-command hermetic suite** invocable against a copy — mado's gate
   …
   851	2. **Spec parse + uniqueness.** Every `@old` must occur exactly once (non-overlapping count), asserted
   852	   **before any suite run**; `@new == @old` is refused. Any spec failure is
   853	   `MUTATE: SETUP (<reason>)`, exit 2 — no headline.
   854	3. **Control first.** The unmutated copy must run green; a red control exits 2
   855	   (kills could not be attributed).
```

### F2 — row (c): the paraphrase's sentence moved 17 lines down

```
| c | A moved substrate without a re-pin | a recommendation, never an edit — the service never edits, repairs or re-pins a gate | `:834-836` |
```

```
sed -n '834,836p' SKILL.md
```

```
   834	### The opt-in contract — what the lane brings
   835	
   836	1. **A pinned revision** — committed bytes of the gate with sha256, size, line
```

The cited range is a heading, a blank line and the **pinned-revision** item — the row's refusal is
not about pinning. The meaning-cell is a near-verbatim rendering of the sentence now at `:851-853`
("4. Nothing else. The service never edits, repairs or re-pins the gate; a needed change is a
recommendation to the owner…"). At `99c3bc8`, `:834-836` was byte-exactly that item. Correct C0
range: **`:851-853`**.

### F3 — row (f): the page half of the anchor is 17 lines early

```
| f | Product semantics — whether a gate's verdicts are right | never measured — sensitivity ≠ truth | `:890-892`; `fleet-kill-rate-ledger.md:156-158` |
```

```
sed -n '890,892p' SKILL.md
```

```
   890	- **Hermetic suites only** — no substrate-drift claim; results are
   891	  per-revision and per-host (census §5 scope, `fleet-suite-census.md:288-291`).
   892	- **Read-only** — target sha before = after (`MUTATE_RESTORE`); the tool emits no tree-clean check, so porcelain-clean is an opt-in precondition at open (SKILL.md:819-820).
```

Two other bullets, not the one the row renders. The target is:

```
sed -n '907,909p' SKILL.md
```

```
   907	- **Sensitivity, not truth** — a sweep measures what the suite can detect,
   908	  never whether the gate's verdicts are right
   909	  (`mutation-case-mado-verify.md:229-230`).
```

The ledger half `fleet-kill-rate-ledger.md:156-158` still resolves ("suite sensitivity ≠ gate
truth"), so only the page half is stale. Correct C0 range: **`:907-909`**.

### F4 — the "no cadence … names it" locator no longer matches the cadence section

```
no cadence or ledger text names it (`:1023-1169`, `fleet-kill-rate-ledger.md:285`, `fleet-kill-rate-ledger.md:318`)
```

```
grep -n '^## The re-sweep cadence' SKILL.md
```

```
1040:## The re-sweep cadence and the six-case confidence statement (round 8, measured)
```

```
awk 'NR>1040 && /^## /{print NR; exit}' SKILL.md
```

```
1187
```

So at C0 the round-8 cadence section spans `:1040-1186`; the cited `:1023-1169` opens 17 lines
early inside the round-7 ledger-leg list (`:1023` reads "5. **The ledger proves the instrument, not
the gates.**…") and stops 17 lines before the section ends, omitting the six-case bullets at
`:1170-1186`. At `99c3bc8` the range was exactly the section's span (heading 1023, next `##` 1170).

**The negative claim itself is TRUE at C0 and was measured:**

```
grep -n 'service-limits' corpus/knowledge/fleet-kill-rate-ledger.md
```

```
(no output — the ledger never names it)
```

```
sed -n '1040,1186p' SKILL.md | grep -c "service-limits"
```

```
0
```

Only the page locator is stale. Correct C0 span: **`:1040-1186`**.

## Checked and resolving (no finding)

Every note-side anchor in the table resolves at C0 (receipt `claims-that-resolve.txt`):

- **row (a)** `service-optin-protocol.md:25-30` — "The queue (`fleet-suite-census.md:277-286`) is an offer, not a schedule… a round with no opt-in records the no-opt-in line as its complete outcome"; `fleet-suite-census.md:277-286` — the queue projection table.
- **row (b)** the *behaviour* — exercised above: `MUTATE: SETUP`, exit 2, no headline, for both the spec-parse and the red-control arm.
- **row (c)** the *sentence* — at `SKILL.md:851-853` (only the anchor is stale).
- **row (d)** `service-optin-protocol.md:129-132` — "**No live substrate read.** … a PATH-level stub, never the session".
- **row (e)** `PROVINCE.md:14-18` — "Never edits a sibling's gate code… Credential material (→ kagi), endpoint health (→ kama)."; `PROVINCE.md:20` — "**Out of province → report, never absorb.**".
- **row (f)** ledger half `fleet-kill-rate-ledger.md:156-158` — "suite sensitivity ≠ gate truth (nothing here measures whether a gate's verdicts about the real world are right)".
- **row (g)** `fleet-kill-rate-ledger.md:220` — "**U2** — coordinated multi-edit rewrites unmeasured everywhere (matrix §7)".
- **row (h)** `service-optin-protocol.md:267-269` — "**U4** — a harness that adjudicates by exit code alone cannot kill the exit-flatten family…".
- **row (i)** `fleet-kill-rate-ledger.md:35-36` — "A post-hardening re-run of the same spec is a **directed repair**, not an independent rate; it is recorded as such."
- **row (j)** `service-optin-protocol.md:86-91` — "**Scratch namespace per lane.** … kept exactly its own 8, and removed exactly those paths".
- **the note's own role statement** `service-limits.md:4-5` — "Role: the **refusal table the re-sweep cadence / applies at intake**" (the quote crosses the note's line break); the attribution "(T9-2, round 9)" matches the note header.
- **"carries the same rows as the detail of record"** — the note's §1 table (line 44) has rows a-j with the "Trigger at intake" column, §2 carries the ten verbatim anchor quotes, §3 is "The intake precondition — the re-pin rule (checked: present, cited)" (line 172). The letters a-j align one-to-one with the page's rows and no page cell contradicts its note counterpart, so the section's own "a divergence between the two is the finding" rule fires nothing.
- **table integrity** — header `| # | Refusal | What it means | Anchor |`, separator, ten rows a-j, four cells each, no duplicate or missing letter; every row carries at least one anchor, consistent with "a refusal without an anchor is not written".
- **closing line** — "Anchors re-resolved 2026-10-14 on the live bytes; a reader on a differing revision re-resolves rather than trusts" is a dated statement about the round-9 write, not a contradiction. It does not downgrade F1-F4: the section's page-local anchors were already adjudicated a finding and repaired once, in round-54's C1 fix pass `99c3bc8` ("stale SKILL anchors at C0"), and two later content commits moved the page again and undid that repair. The note's own §7 ER-1 records the same hazard ("The round-9 section was **edited in place**, not merely appended: its internal lines shifted… Cite the round-9 SKILL section by heading, not by line").

## Calibration mechanism (measured — this is the axis the round is judged on)

This heading's **SKILL.md text is byte-identical at base and at C0**. The frozen round-18 `sectionize`
gives `sha256 = 7e240e714c6e6fa75a01061ef171238401b3a91fdd69cc86c13f97b151b848f6` at **both**
`981c5e8b` (span 1269-1298) and `c013745` (span 1282-1311).

So this heading is in `lost-headings-at-base.json` **not** because the round edited its text, but
through the round-21 monitor's **input gate**. Running the frozen monitor
(`.ufo/evidence/round-21/coldread/measure.py --repo LANE --rev REV`) gives **46 credited of 64 at both
base and C0**, and this heading's own reason string at C0 is:

```
input-drift:tools/context-capture.py;input-drift:tools/registry-check.py;input-drift:tools/registry.json;input-drift:tools/repeat-control.py
```

The ledger entry read at `99c3bc8` pins those four tools at their round-54 digests; round-55's C0
changed all four. Measured against the blobs at C0: 35 of 39 recorded inputs MATCH, and exactly those
four DRIFT. The recovery is therefore a **re-read that re-pins those inputs at C0**, not a text edit.

Two consequences the L1 needs before adjudicating:

1. **An in-section `SKILL.md` edit breaks this report's binding.** C1 arm 4 compares the report's
   `section_sha256` to the section's sha **at REV**. A re-pin edit inside this section changes the sha
   (measured: `bf9e0f4dd0587894…`), which is `READER_HASH_XREV_DRIFT`. **The +17 drift must be fixed in
   a later round, never before the bind** — this is exactly the round-55 harm pattern.
2. **An insertion *above* the section does not change its sha.** Measured: 13-line inserts at lines 44,
   200 and 1200 all leave `7e240e71…` unchanged and only move the span. So the +17 drift is a pure
   offset and the re-key is unaffected by it.

## Notes for the L1 (improvements, stale-but-true, routing)

1. **The note-side anchors of the standalone detail of record are stale in the same way** and are *not* this section's defect, so they are a note, not a finding: `corpus/knowledge/service-limits.md` §2 still cites `SKILL.md:811-812` for "A moved substrate needs a re-pin", `SKILL.md:879-880` for "Sensitivity, not truth" and `SKILL.md:860-861` for "Single-edit mutants only"; at C0 those ranges land on the defect-taxonomy list, the evidence-dir list and a blank/bash-fence line respectively. The note discloses this itself (its §7 ER-1 supersedes its write-time cites and directs citing the round-9 SKILL section by heading), and its §6 pins are dated 2026-10-14.
2. **Cheapest durable fix.** This is a pointer class, not a behaviour class — no row's refusal changes meaning and no command in the section fails. Another +17 re-pin would be a fifth edit to the same cells and would be re-broken by the next insertion above them; the note's ER-1 already prescribes the durable form ("Cite the round-9 SKILL section by heading, not by line"). The round-54 repair's own lesson is that line-anchored page-local cites are fragile against insertions above them.
3. **Cross-section pointer into this section, same +17 shift** — the round-10 runbook section says "the same rendering/divergence rule this page applies to `service-limits.md` (`:1276-1277`)" (`SKILL.md:1334-1336`); the divergence rule is at `:1293-1294` at C0, and `:1276-1277` now reads the tail of the preceding re-pin-semantics paragraph. Another seat's item; recorded here for routing.
4. **Census (not this seat's claim, recorded for the round's census-after item).** `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` exits 0 (`tameshi ok …/corpus/SOURCES.md`; duplicate-URL W04 warnings only, no failures). Measured row count is **142** registry rows (S001…S282), not the 141 the round brief states: base `981c5e8b` had 140 and C0 `c013745` added **two** rows (S281 statement-layer specification, S282 build-provenance), not one. Flagged for the L1; it does not affect this heading's verdict.
5. **No tool was installed or upgraded** (pacman is paused host-wide; nothing was needed for this read). No lane file, frozen instrument or wave spec was edited. Scratch `/fast/scratch/hyaku/tameshi-r56/T56W2Read17` (clone, tmp, work dirs) was removed at exit; nothing was written under `/tmp` outside the read-only git object reads.

## Sweep and method

- Section bytes and every cited artifact were read from **git objects** at C0 via `git show <rev>:<path>`; the working tree was never the source of section bytes. The clone was created with `git clone --shared` and checked out `--detach` at C0 (`c0137451f5b7f22d65f748fc69f1b181f55e1378`); `git rev-parse --show-toplevel` was asserted to be the fixture dir before any commit there, and **no mutating git command was run anywhere**.
- Full anchor enumeration of the 29-line body: page-local `:1023-1169`, `:824-828`, `:851-855`, `:834-836`, `:890-892`; note-side `service-limits.md:4-5`, `service-optin-protocol.md:25-30`, `fleet-suite-census.md:277-286`, `service-optin-protocol.md:129-132`, `PROVINCE.md:14-18`, `PROVINCE.md:20`, `fleet-kill-rate-ledger.md:156-158`, `:220`, `:35-36`, `service-optin-protocol.md:267-269`, `:86-91`, plus the prose `fleet-kill-rate-ledger.md:285` and `:318`.
- Anchor-resolution sweep: every page-local `:NNN` range in the section was opened at C0 and at `99c3bc8` and compared byte-for-byte, giving the drift table above; the whole-file sweep over **all 61** page-local `:NNN` ranges in SKILL.md shows that **57 of the 61 no longer hold the bytes they cited at `99c3bc8`**, the cited text having moved down by exactly **+17 lines**. The 4 unaffected anchors are `:11`, `:14`, `:318` and `:2-31` (all at or above the insertion points). A naive byte-search reports +18 for 8 anchors only because their range begins on a blank line, and a spurious offset for the two blank-bodied ranges `:2024`/`:318`; the true offset is +17 throughout. So the +17 shift is a **page-wide property of this commit pair, not local to this heading** — worth the L1's attention when it routes the other seventeen headings, and the fix should be decided once for the page (heading-anchored cites) rather than per-heading re-pins.
- Provenance: `git log --format=... -L 1282,1294:SKILL.md` names `99c3bc8` as the last writer of this section; `git diff -U0` between `99c3bc8`/`9cf0146` and `981c5e8b`/`c013745` locates the two insertions that broke the anchors.
- Tool behaviour was **exercised at C0**, not read: the selftest (107/107, rc 0), the spec-parse refusal arm and the red-control refusal arm, all under `TMPDIR` inside the seat's scratch.

COLDREAD T56W2Read17: gap-minor (4 findings, one class: page-local anchors no longer resolve at C0)
