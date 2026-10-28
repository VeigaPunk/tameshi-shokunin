# T54W2Read08 — cold read at C1

- **Section:** `### The service's limits — what tameshi refuses to mutation-test`
- **Revision (C1):** `99c3bc88d704566197783f66b211ee0a830e0330` (2026-10-28 11:38:37 -0300)
- **Section bytes:** SKILL.md lines **1265–1293** inclusive (reader `start=1265 end=1294`; line 1294 is the blank before `## The operator's runbook…` at 1295) — 29 lines, 2 597 bytes
- **`section_sha256`:** `7e240e714c6e6fa75a01061ef171238401b3a91fdd69cc86c13f97b151b848f6`
  (reproduced independently: sha256 of `'\n'.join(lines[1264:1293])`, no trailing newline, matching the round-18 sectionizer's "heading through the line before the next heading, trailing blanks stripped" rule)
- **findings:** none — `[]`

## Result

No defensible defect. Every in-page anchor, every cross-file anchor and every bound note name in
this section resolves at C1 to the clause the cell asserts; the table's rows match the detail of
record in `corpus/knowledge/service-limits.md` row-for-row; no sentence contradicts another in the
section; the QUALITY-104 mechanical scan (double space, glued sentence punctuation, repeated word,
adjacent/double parenthetical, odd backtick count) is clean.

## Anchor resolution (each checked against the C1 blob, byte-for-byte at both range ends)

Method: `git show 99c3bc8:SKILL.md` / `git show 99c3bc8:<note>` split on `\n`; the printed
line `n` is `lines[n-1]`, compared for equality with the expected boundary text.

| Cell / sentence | Anchor | C1 first line | C1 last line | Verdict |
|---|---|---|---|---|
| intro, "no cadence or ledger text names it" | `:1023-1169` (this page) | `## The re-sweep cadence and the six-case confidence statement (round 8, measured)` | `` (blank; next heading `## The cadence's first scheduled tick…` is 1170) | resolves to exactly the cadence section |
| note's role quote | `service-limits.md:4-5` | `` `plans/round-9.plan.md:47-69`). Role: the **refusal table the re-sweep cadence `` | `applies at intake** — what this service will not sweep, the trigger that fires` | quote is byte-exact (modulo the note's own `**` emphasis) |
| "no cadence or ledger text names it" | `fleet-kill-rate-ledger.md:285` | ER-3 heading (the re-sweep cadence policy) | — | holds |
| "no cadence or ledger text names it" | `fleet-kill-rate-ledger.md:318` | ER-4 heading (first scheduled tick) | — | holds |
| row a | `service-optin-protocol.md:25-30` | `only; results are per-revision and per-host. The queue` | `` (`plans/round-7.plan.md:16-20`).`` | holds ("offer, not a schedule … no-opt-in line") |
| row a | `fleet-suite-census.md:277-286` | `Queue (projection, ordered by expected yield — most static protection last):` | kimi-census row | holds (the queue is a projection) |
| row b | `:824-828` | `2. **A one-command hermetic suite** invocable against a copy — mado's gate` | `` (`mutation-case-mado-verify.md:44-49`).`` | holds (the request shape requires the suite) |
| row b | `:851-855` | `2. **Spec parse + uniqueness.** … asserted` | `   (kills could not be attributed).` | holds (spec → `MUTATE: SETUP`, exit 2, no headline; red control exits 2) |
| row c | `:834-836` | `4. Nothing else. The service never edits, repairs or re-pins the gate; a` | `` `plans/round-6.plan.md:23-25`).`` | holds |
| row d | `service-optin-protocol.md:129-132` | `- **No live substrate read.** …` | `  local stub, never the session", …` | holds |
| row e | `PROVINCE.md:14-18`, `PROVINCE.md:20` | `**Refuses:** product domains …` / `**Out of province → report, never absorb.**` | `Credential material (→ kagi), endpoint health (→ kama).` | holds (both refusal subjects named) |
| row f | `:890-892` | `- **Sensitivity, not truth** — a sweep measures what the suite can detect,` | `` (`mutation-case-mado-verify.md:229-230`).`` | holds |
| row f | `fleet-kill-rate-ledger.md:156-158` | `… suite sensitivity ≠ gate truth (nothing` | `  live-substrate drift (suites are hermetic by construction).` | holds |
| row g | `fleet-kill-rate-ledger.md:220` | `- **U2** — coordinated multi-edit rewrites unmeasured everywhere (matrix §7).` | — | holds |
| row h | `service-optin-protocol.md:267-269` | `- **U4** — a harness that adjudicates by exit code alone cannot kill the` | `` … a named future, not a measurement`` | holds |
| row i | `fleet-kill-rate-ledger.md:35-36` | `… A post-hardening re-run of the same spec` | `  is a **directed repair**, not an independent rate; it is recorded as such.` | holds |
| row j | `service-optin-protocol.md:86-91` | `- **Scratch namespace per lane.** …` | ``  (`corpus/knowledge/mutation-case-mado-verify.md:24-29`).`` | holds ("kept exactly its own 8, and removed exactly those paths") |

**Intra-section anchor drift check (C1 vs C0).** C1 re-anchored this section's five in-page
ranges. I verified both directions: at C0 the old numbers do **not** land on the asserted clauses
and at C1 the new ones do.

```
C0 1010-1154: first='   rate is never implied to hold at a later revision than its sweep pin.'  last='  — the checklist note classifies `C1` …'
C0  813-817 : first='the run below is the worked instance this section formalizes…'             last='### The opt-in contract — what the lane brings'
C0  840-844 : first='All writes in scratch, through the pinned harness `tools/mutate-and-run.sh`' last='```bash'
C0  823-825 : first='   moved substrate needs a re-pin, never a re-interpretation of the old…'   last='   takes `bash "$MUTANT" --selftest`; it must exercise the copy it is'
C0  879-881 : first='  a low kill rate is a report, not a service failure (SKILL.md:335).'       last='  + 6 out-of-surface, measured 4/4 and 0/6), not as a suite regression'
C1 1023-1169: first='## The re-sweep cadence and the six-case confidence statement (round 8…'  last=''   (next heading 1170)
C1  824-828 : first="2. **A one-command hermetic suite** …"                                      last='   (`mutation-case-mado-verify.md:44-49`).'
C1  851-855 : first='2. **Spec parse + uniqueness.** … asserted'                               last='   (kills could not be attributed).'
C1  834-836 : first='4. Nothing else. The service never edits, repairs or re-pins the gate; a'  last='   `plans/round-6.plan.md:23-25`).'
C1  890-892 : first='- **Sensitivity, not truth** — a sweep measures what the suite can detect,' last='  (`mutation-case-mado-verify.md:229-230`).'
```

No in-page `:…` reference in the section was left un-shifted, and no cross-file anchor it cites
points into a file C1 edited (C1 touched `SKILL.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`,
`corpus/knowledge/change-aware-resweep-cadence.md`, `corpus/lessons/round-54.md`,
`tools/env-diff.py`; none of the section's cited notes is among them).

## Cross-checks behind the table cells

- **"no cadence or ledger text names it"** — `git grep -n 'service-limits' <C1> -- SKILL.md corpus/knowledge/change-aware-resweep-cadence.md corpus/knowledge/fleet-kill-rate-ledger.md corpus/knowledge/service-optin-protocol.md` returns only `SKILL.md:1268,1274` (this section), `:1319`, `:1410`, `:1483` — no cadence or ledger hit. The cadence section `:1023-1169` contains no mention, and the ledger has no `service-limits` string at all (its only `refus` hit is `:123`, about claim-ledger refusal paths).
- **"carries the same rows as the detail of record — verbatim anchor quotes, the trigger column and the intake-precondition check"** — `service-limits.md` §1 table header at `:44` is `| # | Refused — no sweep runs against … | Trigger at intake | What happens instead | Measured reason (anchor) |`; row ids `a`–`j` at `:46-55` are the same ten refusals as this section's a–j; §2 (`:57-170`) is the verbatim-quote detail; §3 (`:172`) is `## 3. The intake precondition — the re-pin rule (checked: present, cited)`. All three named components exist.
- **row b, "spec/control failures are `MUTATE: SETUP`, exit 2, no headline"** — verified against the artifact the harness runs: `tools/mutate-and-run.sh:253-256` (`die_setup` → `MUTATE: SETUP (%s)` on stderr, `exit 2`) and `:536-543` (red control → `CONTROL: RED`, then `die_setup "control run on the pristine copy is red …"`), i.e. a control failure is in fact a SETUP/exit-2/no-headline outcome.
- **row a, "the queue is an offer, not a schedule … no-opt-in line"** — `service-optin-protocol.md:26-30` carries the sentence verbatim; `fleet-suite-census.md:277` labels the queue a "projection".
- **row j, "never removed"** — `service-optin-protocol.md:88-90`: "the mado run saw ≥37 foreign … directories, kept exactly its own 8, and removed exactly those paths" (i.e. foreign scratch is left in place).

## Candidates examined and rejected (recorded, not reported as findings)

1. **Closing provenance line** — `Anchors re-resolved 2026-10-14 on the live bytes; a reader on a differing revision re-resolves rather than trusts.`
   Rejected: it is a dated historical statement plus an instruction, and its second clause explicitly
   tells a reader at another revision to re-resolve — which is exactly what C1 did for the five in-page
   ranges. At C1 every anchor resolves, so no executor is misled and no enumerated read criterion fails
   (not a rule whose anchor fails, not a table cell, not an intra-section contradiction).
2. **Row b, "spec/control failures are `MUTATE: SETUP`"** — the cited `:851-855` spells out the
   `MUTATE: SETUP` token for spec failures and only "exits 2" for a red control.
   Rejected as a defect: the statement is true at the artifact (`tools/mutate-and-run.sh:536-543` +
   `:253-256`), so the cell is a compact aggregate, not a stale or false claim; the anchor does carry
   the exit-2 half for control.

## Artifacts opened (all at `99c3bc88d704566197783f66b211ee0a830e0330` unless noted)

- `SKILL.md` — section 1265–1293; context ranges 1019–1032, 1165–1172, 1170–1264, 820–860, 815–900, 1005–1020
- `corpus/knowledge/service-limits.md` (281 lines) — 1–45, 45–140, 140–281 (rows a–j, §2, §3, §6, §7)
- `corpus/knowledge/service-optin-protocol.md` (286 lines) — 22–32, 80–95, 125–135, 260–275
- `corpus/knowledge/fleet-kill-rate-ledger.md` (441 lines) — 30–40, 150–165, 214–226, 278–325
- `corpus/knowledge/fleet-suite-census.md` (675 lines) — 270–295
- `PROVINCE.md` (118 lines) — 1–26
- `corpus/QUALITY.md` — criterion 104 (`:1574`)
- `tools/mutate-and-run.sh` — 250–258, 534–546 (control/SETUP path)
- `.ufo/waves/round-54/reader-section.py` (the instrument, read to learn the hash convention)
- `.ufo/evidence/round-18/measure.py` at C1 (sectionizer only, lines 1–80)
- `SKILL.md` and `corpus/knowledge/change-aware-resweep-cadence.md` at `59c38109bf11` (C0) for the drift comparison; `git diff 59c3810 99c3bc8 -- SKILL.md`

## Commands run

```
export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read08
python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  99c3bc88d704566197783f66b211ee0a830e0330 "### The service's limits — what tameshi refuses to mutation-test"
  -> {"heading": ..., "start": 1265, "end": 1294, "section_sha256": "7e240e71…b848f6"}

git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 99c3bc8:SKILL.md > $TMPDIR/SKILL.md
python3 -   # sha256('\n'.join(lines[1264:1293])) == 7e240e71…b848f6 ; 29 lines / 2597 bytes
git -C … show 99c3bc8:SKILL.md | sed -n '1265,1293p'            # section verbatim
git -C … show 99c3bc8:SKILL.md | sed -n '820,860p;1005,1020p;1165,1172p'
git -C … show 99c3bc8:corpus/knowledge/service-limits.md | sed -n '1,45p;45,140p;140,281p'
git -C … show 99c3bc8:corpus/knowledge/service-optin-protocol.md | sed -n '22,32p;80,95p;125,135p;260,275p'
git -C … show 99c3bc8:corpus/knowledge/fleet-kill-rate-ledger.md | sed -n '30,40p;150,165p;214,226p;278,325p'
git -C … show 99c3bc8:corpus/knowledge/fleet-suite-census.md | sed -n '270,295p'
git -C … show 99c3bc8:PROVINCE.md | sed -n '1,26p'
git -C … show 99c3bc8:tools/mutate-and-run.sh | sed -n '250,258p;534,546p'
git -C … show 99c3bc8:corpus/QUALITY.md | sed -n '1574p'
git -C … grep -n 'service-limits' 99c3bc8 -- SKILL.md corpus/knowledge/change-aware-resweep-cadence.md \
   corpus/knowledge/fleet-kill-rate-ledger.md corpus/knowledge/service-optin-protocol.md
git -C … diff 59c3810 99c3bc8 -- SKILL.md corpus/knowledge/change-aware-resweep-cadence.md
python3 -   # boundary-equality assertion for every reference (all MATCH) + QUALITY-104 lint scan (clean)
```

No mutating git/jj command was run in the lane; the lane tree was read through `git show`/`git grep`
and `git diff` only. Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W2Read08`. No tool installed or
upgraded this seat (host `pacman` transactions paused; nothing needed).

## Limits of this read

- Read is at the C1 commit only; the note artifacts were read through `git show` at that same
  revision, not on the worktree.
- Anchor verification is boundary-line equality against expected text plus a full read of each cited
  range; it does not re-run any cited command (the section claims no command output of its own).
- Nothing under `.ufo/waves/round-54/w1/` (wave-1 reader JSONs) or any adjudication record was opened.
