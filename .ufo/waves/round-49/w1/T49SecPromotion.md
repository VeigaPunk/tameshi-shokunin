# T49SecPromotion — C1 section audit: `## Promotion-evidence calibration — fleet round-1`

Seat: section critic for C1 target 4 of 7 (`contract.json` `c1.targets_frozen[3]`, FLOORS 5). Read-only on the
lane; every command below is `git show`/`grep`/`sha256sum`/`python3`, plus one scratch clone for the fix proof.
Deliverable: `.ufo/waves/round-49/w1/T49SecPromotion.findings.json` (12 statements: **1 false, 1 unverifiable,
10 true**). Receipts with full observed output: `.ufo/waves/round-49/w1/T49SecPromotion.receipts.txt`.
I decide no claim and run no deciding counter.

Section at base `8ca67421111fa354b47b803358391d0b07fc6db9`: SKILL.md:1464–1477 (heading :1464, body 14 lines).
Body sha256 `76c6929815b2b84ed977d315674125d4c70ffc46de9d5b280134ede03fbdf6fe` — reproduced under the round-17
sectionizer convention and byte-identical to the round-21 ledger bucket for this section
(`receipts R1b/R1c`).

## Headline: this section lapsed on the file it names as its audit, not on a record append

The section body has not changed since round 21. Of the five inputs the ledger keys it to, exactly one moved:

```
$ for f in reports/round-1-calibration.md corpus/knowledge/executor-test-sufficiency.md \
        corpus/lessons/round-1.md .ufo/evidence/fleet-round-1/cli-smoke-canonical.json \
        .ufo/evidence/fleet-round-1/selftest.json; do git show 8ca67421:$f | sha256sum; done
a2afa5f7f8a916…  reports/round-1-calibration.md          <- ledger says fc46d59db204…
b26021292d69b3…  corpus/knowledge/executor-test-sufficiency.md   same
568609fcd0071e…  corpus/lessons/round-1.md                       same
19296d8332371e…  .ufo/evidence/fleet-round-1/cli-smoke-canonical.json  same
8492de881056fa…  .ufo/evidence/fleet-round-1/selftest.json       same
$ git log --format='%h %ad %s' --date=short 370f2df..8ca67421 -- reports/round-1-calibration.md
583909a 2026-10-24 round-37: w1 seat reports (27/33), S104 citation correction, box-3 erratum, …
$ git log -p --format='%h' 370f2df..8ca67421 -- reports/round-1-calibration.md | grep -E '^@@|^\+.*Erratum'
583909a
@@ -164,6 +164,15 @@
+> **Erratum (round 37, append-only).** This box-3 disposition was written at the fleet round-1 …
```

So the section's cold-read credit lapsed because a **non-record** tracked file it cites was appended to
(`reports/round-1-calibration.md:167-174`, the box-3 erratum). The contract's durability probe appends only to
the five `volatile_records`; it cannot exercise this class, and re-keying this section at REV will key it to a
file that has already drifted once. **Flag for the L1, not a defect I can fix from this seat**: a `[~]` section
whose evidence is a mutable audit is append-fragile by construction. The lane's own input-drift model already
names the effect (SKILL.md:1874, "A section whose bytes did not change still loses credit"); what it does not
carry is a probe that appends to a cited non-record file. The monitor agrees on the state, not the
cause: `calibration_restraint_score 6`, `coldread.box3_full_page false`
(`.ufo/evidence/round-49/control/monitor-at-base-8ca67421.json`, `receipts R7`).

## False

### F1 — SKILL.md:1467: "Its supporting audit is `reports/round-1-calibration.md#box-1`."

**Verdict: false (scope).** `#box-1` disposes box 1 only and cannot be "the checklist's supporting audit".

```
$ git show 8ca67421:reports/round-1-calibration.md | grep -n '^## '   # condensed; exact output R2
71:## box-1   105:## box-2   132:## box-3   176:## box-4
211:## lane-local dispositions (calibration target)  224:## executed verification
$ git show 8ca67421:SHONEN.md           # four boxes -> four different pointers (summarized; exact output R3)
  box1 reports/round-1-calibration.md#box-1 | box2 #box-2
  box3 .ufo/evidence/round-21/coldread/ledger.json | box4 #box-4
```

The checklist-level audit is the dispositions table at `:211-218`; box 3's disposition is at `:132-174`. The
cited anchor is also the one block that cannot support this section's own box-3 sentences — box-3's rejection
sits at `:160-163` and its reconciling round-37 erratum at `:167-174`, both past the anchor (`receipts R4`).
Materiality: `reports/round-1-calibration.md` is precisely the input whose drift lapsed this section (Headline),
so a cold reader who takes the pointer at 1467 literally lands before both the contradiction and its repair.

Prior grading, for calibration: round-17 seat CR43 graded this claim "holds"
(`.ufo/waves/round-17/w2/CR43.md:60-61`) by checking that the anchor *resolves*; resolution is not scope.
Round-16 seat RR15 called the same thing "minor pointer imprecision" while still grading holds
(`.ufo/waves/round-16/w2/RR15.md:34-40`, "No statement in the range is false"). I differ on the verdict, not on
the facts: resolution passes, scope fails, and the scope failure is the documented cause of the lapse.

## Unverifiable

### F2 — SKILL.md:1466–1467: "not the historical training\ncloseout"

**Verdict: unverifiable.** The phrase names no artifact and resolves to two different things in the lane's own
records.

```
$ git grep -n -F 'training closeout' 8ca67421 -- SKILL.md .ufo/waves .ufo/evidence
SKILL.md:1466-1467 (+ derived snapshots .ufo/evidence/round-16/coldread/SKILL.snapshot.md:1466, skill-versions/SKILL.*.md:1466)
.ufo/waves/round-16/w2/RR15.md:18   "… which the range does not name by path"
.ufo/waves/round-16/w2/RR09.md:23   "Unresolved (gap). … Existence is not a pass."
.ufo/waves/round-35/w2/CriticC2.md:78  "284ab0f0 is the October 14 training closeout"   <- a commit, not a file
$ git show 8ca67421:corpus/knowledge/closeout-r11.md | grep -c '\[~\]\|\[x\]\|\[ \]'
0
```

RR15 resolved the referent to `corpus/knowledge/closeout-r11.md` and had to over-read to do it; CriticC2
resolved it to commit `284ab0f0`. The nearest candidate carries zero box marks, so the contrast is at best
vacuously true. Minor, but it is exactly the "file name without a line number" class the seat was asked to
attack — here with no file name at all.

## True (with the caveats that matter)

| line | statement (short) | command → observed |
|---|---|---|
| 1464 | heading "— fleet round-1" | `git log -S'Promotion-evidence calibration — fleet round-1' -- SKILL.md` → `cd31c6b 2026-10-15 fleet round 1: reconcile calibration evidence; dispatch blocked` |
| 1466 | "current checklist is `SHONEN.md`" | `git show 8ca67421:SHONEN.md \| head -1` → `# tameshi-shokunin — Promotion checklist`; PROTOCOL.md:432 defines the file |
| 1468–69 | dispatched reviewers are the lane; a new agent name is not `[x]` | `sed -n '63,68p'` of the fleet PROTOCOL.md → :64-65 "a subagent the lane dispatched is still the lane", :66-67 "only a non-author `<id>` may write `[x]`"; byte-identical range in the kimi copy (`diff` → IDENTICAL_RANGE); fleet copy sha256 `886e459b…`, the digest the ledger pins |
| 1470 | lane assertions use `[~]` with durable evidence, not temp logs | 4/4 marks `[~]`, 0 `[x]` in SHONEN.md/MINT.md/PROVINCE.md/README.md; no `/tmp` in SHONEN.md; all four pointer targets exist at base (round-21 ledger present). Round-16's dangling box-3 pointer (RR15 F1) is cured at base. Caveat: the durability rule is uncited inside the section (RR09:26 "partial citation"); it lives at fleet PROTOCOL.md:345-359 |
| 1472 | "Box 3 was `[ ]` at this write" | `git show cd31c6b:SHONEN.md \| sed -n '9p'` → `- [ ] Instructions executable by an agent without oral context` |
| 1472 | "(`[~]` since; Errata — round 16)" | mark is `[~]` at base and continuously from `c7986cd` (2026-10-19) — commit-by-commit loop, no revert; errata heading exists once at SKILL.md:1707, its row at :1736 says "`[~]` since". Caveat: neither the section nor the errata row carries the since-point; the transition commit is `c7986cdf051cbe9d047f02f76f2e1da0b36a84e3`. Credit (not the mark) is lapsed at base (`box3_full_page false`) |
| 1472–73 | `executor-test-sufficiency.md:160–184` shows a historical single-JS-mutant exercise, not a current full cold-read | `sed -n '160,166p'` → :160-162 "(O) For the executed scope — one killed mutant of the JS case … confirmed"; :164-166 "(U) Not tested by this run: the full 10-mutant sweep, survivor probes (step 8), Appendix B entirely …". Both halves hold inside the range |
| 1474–75 | the CLI receipt verifies kill/survivor/restore and is neither a cold read nor an outside review | `.ufo/evidence/fleet-round-1/cli-smoke-canonical.json` (committed): `exitCode 0`, `CONTROL: GREEN`, `DEFECT wrong-value: KILLED`, `DEFECT unread-value: SURVIVED`, `MUTATE_RESTORE: OK`, `SMOKE_ASSERTIONS: PASS (control, kill, survivor, restore, …)`, and its own `scope`: "… not a new fleet rate, outside review, current full cold-read …". "Fresh" is undated in the section; the receipt's `MUTATE_DATE` is 2026-10-15T05:14:49Z |
| 1476 | the audit rejects the broader claim rather than upgrading its confidence | audit `:160-163` "cannot support a broad current assertion … does not qualify even for `[~]`"; dispositions row box 3 "`[ ]` (assertion rejected)". The section omits that the same file's erratum (:167-174) records the mark later standing `[~]` — the broad claim is still rejected, so the sentence is not false |
| 1477 | `corpus/lessons/round-1.md` holds the admitted correction and rejected claims | `sed -n '106,120p'` → "**Admitted (corrections):** independence … canonical wording … durability … scope bounding"; "**Rejected, with reasons:** 1. **Box-3 blanket claim** …" |

## Proposed fixes (4), all proven pointer-neutral

Each `skill_old` is exact and occurs once in the section; each `skill_new` adds no `.md`/`:N` token. Proof in a
scratch clone (`receipts R15`): with all four applied and committed,
`measure.py --list` yields the section's pointer set **identical** to base — `base=5 after=5 identical=True`
(same `ordinal`/`raw`/`kind`/`file`/`ranges`/`skill_line`; `../PROTOCOL.md:63–68`, `executor-test-sufficiency.md:160–184`,
`SHONEN.md`, `reports/round-1-calibration.md`, `corpus/lessons/round-1.md`), whole-page pointers `90 → 90`,
`missing_headings=[]`, and the section's line count is unchanged, so every later `SKILL.md:<line>` self-anchor
still resolves and the C1 row key (heading+ordinal+raw) is untouched.

1. **1467 (F1)** — keep the pointer, add its scope: skill_new
   `` Its supporting audit is `reports/round-1-calibration.md#box-1`, box 1's block only; this checklist's per-box dispositions are that file's `## lane-local dispositions` table, which still records box 3's audit as rejected. ``
2. **1472** — pin the `[~]` transition: skill_new `` (`[~]` since `c7986cd`; Errata — round 16) ``, `skill_old`
   being the verbatim `` (`[~]` since; Errata — round 16) ``. Cost: none (a bare sha is not a pointer token).
3. **1474** — date the status word: skill_new
   `` The fresh (2026-10-15) CLI receipt in the audit verifies kill/survivor/restore behavior; ``
4. **1476** — record the reconciliation the cited file already carries: skill_new
   `` The source audit rejects the broader claim rather than upgrading its confidence; its appended round-37 erratum records the `[~]` without rewriting that rejection. ``

**Withdrawn deliberately:** a fix for F2. Both available corrections cost more than the defect — naming the
artifact adds one path pointer and therefore one mandatory `holds` read row at REV, and deleting the clause
shrinks the section by a line and shifts every later `SKILL.md:<line>` self-anchor (the round-16 repair rule
kept edited sections' line counts unchanged so self-anchors keep resolving, SKILL.md:1718 — the lane records
that the claim itself missed one section, SKILL.md:1867). That scheduling decision belongs to the L1, so
`proposed_fix` is null there.

## Bounds observed / tooling

No lane writes (only `.ufo/waves/round-49/w1/T49SecPromotion.{md,json,receipts.txt}`); no git or jj mutation in
the lane or the fleet repo; the one scratch clone lived under `/fast/scratch/hyaku/tameshi-r49/T49SecPromotion`
with `rev-parse --show-toplevel` asserted before its first commit and was removed in a `finally`
(`receipts R15`). Nothing under `~/.local/state/` read; no `c2-*.stdout` control receipt opened; no model passed.
**Tooling: nothing installed or upgraded** — no pacman (host-wide paused), no uv/npx; only system git, python3
stdlib, and one `git clone --shared`.

## Summary

1. Section body at base is unchanged since round 21; its lapse came from one input: `reports/round-1-calibration.md` (round-37 erratum append, commit 583909a), the very file it calls its supporting audit.
2. **False (1):** SKILL.md:1467 names box 1's block as the checklist's audit — the checklist cites four pointers and the checklist-level table is `:211-218`; box 3's disposition and erratum sit at `:132-174`.
3. **Unverifiable (1):** "the historical training closeout" (SKILL.md:1466–1467) names no artifact; RR15, RR09 and CriticC2 resolved it to different referents.
4. **True (10):** the checklist claim, the PROTOCOL:63–68 authority rule, the `[~]`/durability rule, "`[ ]` at this write", the continuous `[~]` from c7986cd, the executor-doc scope, the CLI receipt (kill/survivor/restore, not cold-read/outside), the audit's rejection, the lesson pointer, the fleet round-1 attribution.
5. Caveats worth carrying: the `[~]` "since" has no since-point in text or errata row; the audit's erratum (which reconciles `[~]` with the table's `[ ]`) is never mentioned; box 3's mark stands but its credit is lapsed (`box3_full_page false`, score 6).
6. Four fixes proposed, all proven pointer-neutral by `measure.py --list` in a scratch clone (5 pointers, identical raws/ordinals, whole page 90, line count unchanged).
7. One fix withdrawn (F2) because both corrections cost a new read row or a line-count shift — the L1's call.
8. Structural flag for the L1: this section's evidence is a mutable non-record audit, so C1's record-append durability probe cannot cover the class that actually lapsed it.
