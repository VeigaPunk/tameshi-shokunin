# T55W3RevReportSections — report contract (round 55, w3)

Axis: **calibration**. Attacked surface: the round's fleet report contract —
`/home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-55.md` §4 (report contract)
and §6 item 6 (report extras) — against what the lane actually holds at
`9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` (C0) and at the tip `4f7a7040`.

Everything below was read-only in the lane. The two runnable probes (deciding gate,
binder) ran on `git clone --shared` copies under
`/fast/scratch/hyaku/tameshi-r55/T55W3RevReportSections/lane-clone`; every receipt is in
`.ufo/waves/round-55/w3/T55W3RevReportSections-receipts/` and names its command.

**Verdict.** The section list is fully derivable from the prompt, and the round already
holds what three of the six required sections and both extras need (`Sources & frontier`,
`SHONEN`, `Stale-lane`, tool installs); `Work performed` and `Landed changes` can be drafted
but not landed (A3, A4, A6); `Before → after` cannot be written at all: **no `after/`
deciding receipt exists** (the deciding run refuses at its control-receipt gate, receipt A2)
and **the binder cannot run** on the committed adjudication file (receipt A1), so the
re-key half of C1 has no receipt either. The round's own `LOG.md` entry also quotes four
values its committed receipts contradict (A3), and the wave-2/3 artefacts the report must
cite are untracked (A6).
Writing the report today would produce a `before → after` table with an empty after
column — which the marker rule reads as a contentless report only if the rest is empty
too, but which is an honest-stop, not a pass.

---

## 1. The contract, restated from the prompt (so the skeleton is not invented)

Source lines, verified by reading
`/home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-55.md:104-125` and `:502-515`:

- **path**: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-55/tameshi.md` on the fleet repo
  (directory exists — `ls -d /home/vgpnk/Projects/shokunin/.ufo/reports/round-55` → present).
- **required sections, in order**: `## Work performed`, `## Landed changes`,
  `## Before → after measurements`, `## Sources & frontier`, `## Trend verdicts`, `## SHONEN`.
- **extras (§6.6)**: the canonical `## Trend verdicts`; a **Stale-lane** line; **any tool installs**.
- **marker rule**: placeholder text, a missing required section, or no evidence pointers ⇒
  the round is read as **failed**; `Sources & frontier` and `Trend verdicts` are logged, not
  marker predicates.
- **pre-commit checks**: `grep -c '^## SHONEN' <report>` must print **1** followed by one
  `[~]`/`[ ]` line per `SHONEN.md` box; the report lands **last**, through
  `fleet-commit.sh --as tameshi`, and cites the pushed lane hash
  (`git -C <lane> ls-remote origin refs/heads/master` must print it — today
  `4f7a7040a57e7aed17db941be9c27b300aafb783`, verified).

## 2. Section inventory — evidence present vs missing at C0 / tip

| Section | Evidence the round already holds (all committed unless marked) | Evidence still missing | Command the section will cite |
|---|---|---|---|
| **Work performed** | `contract.json` (2 claims, before/target/counter/kill/controls); `.ufo/evidence/round-55/before/{c1,c2}.stdout` (committed at `4f7a704`); `freeze.json` (`files=7 amendments=9`); `spec-w1.json` + `w1-dispatch.json` (tracked, 75 seats); 1260 tracked files under `.ufo/waves/round-55/`; C0 `9cf0146b`, F4 `c31cdd9`, F5 `4f7a704` | wave-2/3 `spec-*.json`, `w2-dispatch.json`, `w3/swarm-registry.json` are **untracked** (A6); `integrate/resolutions.json` is tracked but being rewritten (21 rows, `M` in `git status`); no committed reader inventory | `git ls-files .ufo/waves/round-55/ \| wc -l`; `git log --oneline 0a2010ac..4f7a704`; `python3 -c 'len(json.load(open(".ufo/evidence/round-55/freeze.json"))["amendments"])'` |
| **Landed changes** | six commits since base (`631cd64` freeze, `e2979f2` amendments 1–7, `9cf0146b` C0, `133b2ce` am. 8, `c31cdd9` F4, `4f7a704` F5); one `LOG.md` round-55 entry (`LOG.md:2519-2560`); `## Round 55 - round-54 record corrections` with **10** `**ER-R54-n` rows (`grep -cE '^\*\*ER-R54-[0-9]+ ' SCORECARD.md` → 10) | the LOG entry's measured numbers do not match the receipts (A3); the claimed `QUALITY 106` does not exist in the tree (A4); no LOG close paragraph for waves/deciding yet | `git log --oneline 0a2010ac..<REV>`; `grep -cE '^\*\*ER-R54-[0-9]+ ' SCORECARD.md`; `sed -n '2519,2560p' LOG.md` |
| **Before → after** | before receipts **committed at the tip**: `C1_R55: … premise=9/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false`; `C2_R55: … grammar=6/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/9 skill=0/1 total=20 C2_R55_PASS=false`; the C0 green C1 line appears in 47 wave receipts, the C0 green C2 line in 10 (and a pre-amendment-8 `total=1` twin in 7 — A3b) | **no `.ufo/evidence/round-55/after/` at all**; the deciding run refuses before the counters (A2); the cold-read floor is `cand_credited=46 lost=18 RED` at C0 and the receipt carrying it is untracked | §4 below (one command per row) |
| **Sources & frontier** | census exit **0**, 140 rows; `| S### |` count **139 → 140** at C0; S280 (spec, A) added; S281 refused as a duplicate of S090 with the reason in `corpus/lessons/round-55.md` `## Gate`; `corpus/SOURCES.md:517` carries the round-55 ledger bullet | a committed **round-start** census receipt (value is derivable: `git show 0a2010ac:corpus/SOURCES.md` → 139); an explicit "no frontier row advanced" sentence for round 55 (`:517` does not say it; the only such lines are rounds old, `:365`, `:372`, `:397`) | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`; `git show <REV>:corpus/SOURCES.md \| grep -cE '^ {0,3}\| S[0-9]{3,} \|'` |
| **Trend verdicts** | expansion: rows 139→140, one tier-A row, zero frontier rows; quality: the counters move at C0 (`C1 10 → 0`, `C2 total=20 → 0`, `docs 0/7 → 7/7`, `note 0/9 → 9/9`, `skill 0/1 → 1/1` in wave receipts); discernment: 10 ER rows + 21 adjudication rows in `integrate/resolutions.json` | the deciding-run receipts (the deltas above are wave-run, not the deciding invocation); the **independent non-author verification** an `improved` verdict would rest on (round-54's lesson: no self-granted verdict); the binder's re-key receipt, which is part of this section's "quality" and is blocked (A1) | the three receipts named in §4 |
| **SHONEN** | `SHONEN.md` has exactly **4** boxes, all `[~]` today with resolvable pointers (`reports/round-1-calibration.md#box-1/2/4`, `.ufo/evidence/round-21/coldread/ledger.json`) | nothing to add; `[x]` is unavailable (it needs a named non-author promotion verifier, which this round does not have) | `grep -c '^\- \[' SHONEN.md` → 4; `grep -c '^## SHONEN' <report>` → must print 1 |
| **Stale-lane** (extra) | respawn-per-round driver; lane state `.ufo/state/tameshi.mission` = `2684639`, `.ufo/state/tameshi.round` = `1`; run number 11 recorded in the prompt | a checked sentence that **no other mission of this lane is open** — the check is reading that state pair at report time | `cat /home/vgpnk/Projects/shokunin/.ufo/state/tameshi.mission /home/vgpnk/Projects/shokunin/.ufo/state/tameshi.round` |
| **Tool installs** (extra) | sweep is empty: no seat in `.ufo/waves/round-55/` installed or upgraded anything (only the RULES pointer sentence matches) | none | see A8 |

---

## 3. The skeleton the report should follow

Literal text for `/home/vgpnk/Projects/shokunin/.ufo/reports/round-55/tameshi.md`.
`<REV>` is the deciding revision (a commit after `4f7a704`, carrying the committed
control receipts); `<FREEZE>` must be `4f7a7040…` (9 amendments) or a later re-freeze —
**not** `133b2ce`, see A5.

```markdown
# tameshi — round 55 (hyaku run 11, attempt 1)

L1 `TameshiR55`. Lane repo `tameshi-shokunin`; base `0a2010ac`; counter freeze
`<FREEZE>` (9 amendments, `.ufo/evidence/round-55/freeze.json`); content commit C0
`9cf0146b`; deciding revision `<REV>`.

Round shape: one v2 wave of **75** seats (band 64-128; 28 attack roles = 37.3 %,
`spec-w1.json`/`w1-dispatch.json`) + one v1 wave of **34** seats (24 attack = 70.6 %) + a
v1 falsify wave of **32** seats (10 attack = 31.2 %; `spec-w2.json`/`spec-w3.json`,
committed at `<REV>`). Attack roles are reviewer + critic + mutation-tester, the round-54
definition; every count above is `role` tallied from the spec file named beside it.

---

## Work performed

Claims (2, distinct axes; the lowest non-retired axis is calibration at 8):

- **C1 — calibration (8).** The lane's record must agree with the tree on the ten routed
  defects of the round-54 non-author spot-check (R54.1-R54.10). At base the counter reads
  `premise=9/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false`
  (`.ufo/evidence/round-55/before/c1.stdout`). Target: `total=0`, every corrected value
  derived from a receipt. [one bullet per work item, each with path:line / commit /
  command output]
- **C2 — operability.** One stderr line and one exit class across the **nine** documented
  allocating modes (not the self-test only). At base `grammar=6/9 … docs=0/7 note=0/9
  skill=0/1 total=20 C2_R55_PASS=false` (`before/c2.stdout`). Target: `total=0`.

[work-item bullets: contract/counters/monitors/controls frozen at `631cd64` + amendments
1-9 in `freeze.json`; phase A `<CONTROLS_A>`; wave 1 (75 seats) with its tracked receipts;
adjudication (`integrate/resolutions.json`, N findings); wave 2 (34 seats); the 18 cold-read
readers at C0 (18/18 headings, `w3/T55W3R*.json`); the bind (`REFRESH rekeyed=18
skipped=0`); the deciding run.]

## Landed changes

| Change | LOG.md entry | Commit |
|---|---|---|
| contract, both counters, 15 no-harm monitors, controls harness, deciding script, freeze manifest | round-55 §claims/freeze | `631cd64` + amendments 1-9 |
| C0 content — three tools' one stderr line, seven `scratch_root` registry cells, the note, the SKILL.md scratch rule, the 10 `ER-R54` corrections, QUALITY 105 falsifier re-derived, lessons, S280 | round-55 §C0 | `9cf0146b` |
| F4/F5 instrument bookkeeping (contract before-value, FROZEN list, per-row stale pass) | round-55 §freeze | `c31cdd9`, `4f7a704` |
| waves 1-3 + adjudication + bind | round-55 §waves/re-key | `<REV>` |
| round record (LOG close, SCORECARD, lessons) | round-55 §record | `<REV>` |

## Before → after measurements

| # | Before (base `0a2010ac`, at `4f7a704`) | After (deciding rev `<REV>`) |
|---|---|---|
| C1 | `C1_R55: rev=0a2010acd1e9 classes=10 premise=9/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false` (`.ufo/evidence/round-55/before/c1.stdout`) | `… total=0 C1_R55_PASS=true` (`.ufo/evidence/round-55/after/c1.stdout`) |
| C2 | `C2_R55: rev=0a2010acd1e9 grammar=6/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/9 skill=0/1 total=20 C2_R55_PASS=false` (`.ufo/evidence/round-55/before/c2.stdout`) | `C2_R55: … grammar=9/9 … docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true` (`.ufo/evidence/round-55/after/c2.stdout`) |
| cold-read floor (supporting) | `COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=9cf0146b94dd cand_credited=46 lost=18 RED` | `… cand_credited=64 lost=0 ok` (`.ufo/evidence/round-55/after/coldread-precheck.stdout`) |

Counting commands (each run at the commit named, never at the working tree):
[c1, c2, precheck, controls a/b, no-harm, census — verbatim block from §4]

Instrument amendments 1-9 (all pre-control, all disclosed in `freeze.json`): [one line
each, with the seat that found it].

## Sources & frontier

[`sources-census.sh validate` → exit 0, 140 rows; `| S### |` 139 → 140; S280 (spec, A);
S281 refused (duplicate of S090, reason in the lesson's `## Gate`); rows touched
old→new: the round-54 bullet's "Next unused id" cell only; frontier rows advanced:
none (state the reason; `:517` records the round, not a frontier move); Assimilation:
one theme, one row, one refusal.]

## Trend verdicts

- **expansion — [verdict].** [rows 139→140, one row, no frontier row, one refusal]
- **quality — [verdict].** [C2 20→0 on nine modes, docs 0/7→7/7, note 0/9→9/9, skill 0/1→1/1;
  C1 10→0; the bind]
- **discernment — [verdict].** [10 ER rows, 21 adjudications, the readers' findings fixed;
  name whether an independent non-author verifier exists — if not, `unprovable-but-better`
  and say so]

## Stale-lane

Respawn-per-round driver: this report closes round 55 only; no other mission of this lane
is open (`/home/vgpnk/Projects/shokunin/.ufo/state/tameshi.mission` = `2684639`,
`.ufo/state/tameshi.round` = `1`). Round 56's planned list is in `SCORECARD.md`.

## SHONEN

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — lane assertion, no independent promotion verifier (`reports/round-1-calibration.md#box-1`)
- [~] At least one end-to-end domain task executed and logged in LOG.md — lane assertion, no independent promotion verifier (`reports/round-1-calibration.md#box-2`)
- [~] Instructions executable by an agent without oral context — input-keyed monitor only; no independent promotion verifier (`.ufo/evidence/round-21/coldread/ledger.json`)
- [~] No cross-domain bleed (PROVINCE.md still accurate) — lane assertion, no independent promotion verifier (`reports/round-1-calibration.md#box-4`)

Tool installs: none. Sweep: `grep -rn "uv tool install\|pip install\|npm install -g\|pacman -S\|cargo install" .ufo/waves/round-55/` (no hit outside the RULES-pointer sentence).
```

Pre-commit, verbatim:

```sh
grep -c '^## SHONEN' /home/vgpnk/Projects/shokunin/.ufo/reports/round-55/tameshi.md   # must print 1
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-remote origin refs/heads/master  # must print <REV>
/home/vgpnk/Projects/shokunin/scripts/hyaku/fleet-commit.sh --as tameshi -m "round-55: tameshi report" \
  -- .ufo/reports/round-55/tameshi.md
```

---

## 4. The exact commands each `before → after` line cites

Every command below reads committed bytes at the revision named; none reads the working
tree. `<EMPTY>` must be an existing empty directory (each counter refuses a non-empty
`--work`: `c1/measure.py:301`, `c2/measure.py:166`).

```sh
# C1 — before (already committed, re-measured at F5 with the amended bytes)
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-55/c1/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 0a2010acd1e92e4e332774050825e21bcfc7e079 \
  --work <EMPTY> --explain          # → .ufo/evidence/round-55/before/c1.stdout
# C1 — after (does not exist): the deciding run prints it at the deciding revision
python3 .ufo/evidence/round-55/c1/measure.py --lane LANE --rev <REV> --work <EMPTY> --explain
                                  # → .ufo/evidence/round-55/after/c1.stdout

# C2 — before (already committed) and after (absent), same shape
python3 .ufo/evidence/round-55/c2/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 0a2010acd1e92e4e332774050825e21bcfc7e079 \
  --work <EMPTY> --explain          # → .ufo/evidence/round-55/before/c2.stdout
python3 .ufo/evidence/round-55/c2/measure.py --lane LANE --rev <REV> --work <EMPTY> --explain
                                  # → .ufo/evidence/round-55/after/c2.stdout

# cold-read floor — the leading indicator the 18 readers exist to close
bash .ufo/evidence/round-48/quality/coldread-precheck.sh LANE \
  0a2010acd1e92e4e332774050825e21bcfc7e079 <REV>
                                  # 46/18 RED at C0 → must print cand_credited=64 lost=0 ok

# no-harm — 15 monitors, the deciding run requires exactly 15 `ok` and no RED
bash .ufo/evidence/round-55/no-harm.sh LANE <REV>        # → after/no-harm.stdout

# controls — phase A at the freeze bytes, phase B at the revision it certifies
bash .ufo/evidence/round-55/controls.sh a LANE <FREEZE> 0a2010ac… <OUT>   # → CONTROLS_A: 5/5
bash .ufo/evidence/round-55/controls.sh b LANE <FREEZE> <REV>    <OUT>    # → CONTROLS_B: 3/3

# census — the Sources & frontier marker
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
```

The eight controls the harness scores (`grep -oE "check CTL_[A-Za-z0-9_]+" controls.sh`):
`CTL_0_c1 CTL_0_c2 CTL_SKIP_c1 CTL_FAB_c1 CTL_SKIP_c2 CTL_POS_c1 CTL_POS_c2 CTL_BREAK_c2`
— phase A 5, phase B 3. None of phase B exists yet.

---

## 5. Findings (calibration), severity order

### A1 — BLOCKER: the binder cannot run on the committed adjudication file; the re-key receipt therefore cannot exist

`.ufo/evidence/round-55/integrate/binder.py:50-54` (tracked at `c31cdd9`, absent at C0)
reads the adjudication file as `RES[item['heading']] = int(item['n'])`. The committed
`integrate/resolutions.json` has **21 rows and neither key**:

```
# command: python3 - <<'PY' (binder lines 50-54 over the committed file)
entries 21 keys ['decision', 'evidence', 'finding', 'from', 'id']
binder RES parse: KeyError 'heading'
# round-54 file for comparison:
r54 entries 12 keys ['findings', 'heading', 'kind', 'n', 'reader', 'routed']
```

Run for real on a `git clone --shared` at the tip, the binder dies before doing anything
(exit 1, nothing written, no `rekey-r55-*` directory):

```
# command: python3 .ufo/evidence/round-55/integrate/binder.py CLONE 9cf0146b 4f7a7040 EMPTYDIR
Traceback (most recent call last):
  File ".../integrate/binder.py", line 54, in <module>
    RES[item['heading']] = int(item['n'])
KeyError: 'n'
rc=1
# command: ls -d .ufo/evidence/round-21/coldread/rekey-r55-*
no rekey-r55-* directory
```

This is not cosmetic: the binder is the only route to the 18 re-key entries, and without
them the precheck cannot reach `lost=0`, so the C1 after-line and the `Trend verdicts`
quality row cannot be written. Second half of the same finding — even with a heading-keyed
file, the bind refuses readers that carry findings (`allowed = RES.get(h, 0)`): at capture
**13 of 18** headings had a C0-pinned reader and **10 of those 13 carried findings**, so
those ten headings need a per-heading `n` before they can bind
(`reader-coverage.txt`). Receipts: `binder-blocker.txt`, `reader-coverage.txt`.

**Fix before the deciding run** (neither file is in `contract.frozen_paths`, so no amendment
is required): make the adjudication file heading-keyed (`heading`, `n`) or point the binder
at a second file via an explicit path, then require `REFRESH rekeyed=18 skipped=0` as the
report's bind line.

### A2 — BLOCKER: no deciding receipt exists, and the deciding gate already refuses

```
# command: bash .ufo/evidence/round-55/deciding-run.sh CLONE 9cf0146b 4f7a7040 EMPTYDIR
FREEZE_INTEGRITY: OK files=7 amendments=9
DECIDING_REFUSED control-receipt-missing .ufo/evidence/round-55/control/controls-a.stdout
rc=3
```

`ls -A .ufo/evidence/round-55/control/` holds one **untracked** file; it grew while this
seat read it (4 of 5 phase-A `CTL` lines at capture, **no** `CONTROLS_A: n/n` verdict line),
and `.ufo/evidence/round-55/after/` does not exist. Phase B (`controls-b.stdout/.exit`) does
not exist at all. So each of these report lines is currently unwritable:
`after/c1.stdout`, `after/c2.stdout`, `after/coldread-precheck.stdout`, `after/no-harm.stdout`
(15 `ok`), `after/frozen.stdout`, `after/census.stdout`, `DECIDING_RUN_EXIT`.
Receipt: `deciding-readiness.txt`.

### A3 — MAJOR: the round's own `LOG.md` entry quotes values its committed receipts contradict

```
# command: sed -n '2526p;2531p;2543,2546p' LOG.md
`631cd645`, amended four times before any control was scored or any deciding
... at base `premise=10/10 stale=4
... the eight allocating modes plus the five lazy ones
# command: git show 4f7a704:.ufo/evidence/round-55/before/c1.stdout | tail -1
C1_R55: rev=0a2010acd1e9 classes=10 premise=9/10 stale=4 classes_corrected=0/10 total=10 C1_R55_PASS=false
# command: git show 4f7a704:.ufo/evidence/round-55/before/c2.stdout | tail -2
C2_R55: rev=0a2010acd1e9 grammar=6/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/9 skill=0/1 total=20 C2_R55_PASS=false
# command: len(freeze.json['amendments'])
9
```

Four mismatches in one paragraph: `premise=10/10` (receipt `9/10`), `grammar=6/8`/`note=0/8`/
`total=18` (receipt `6/9`, `0/9`, `20`), "amended four times" (manifest `9`), "eight
allocating modes" (the counter's table and the note carry **nine**). If the report copies
this paragraph its `Before → after` before column is false in the same way round 54's was
(ER-R54-3). Receipt: `record-vs-receipt.txt`.

### A3b — MAJOR: the C0 C2 verdict exists in two values in the wave receipts; only one of them is the frozen counter's

```
# command: grep -rl "C2_R55: rev=9cf0146b94dd.*total=0 C2_R55_PASS=true" .ufo/waves/round-55/ | wc -l
10
# command: grep -rl "C2_R55: rev=9cf0146b94dd.*total=1 C2_R55_PASS=false" .ufo/waves/round-55/ | wc -l
7
# command: grep -rl "C1_R55: rev=9cf0146b94dd.*C1_R55_PASS=true" .ufo/waves/round-55/ | wc -l
47
```

Seventeen wave files print a C0 C2 verdict; seven of them (`T55W1ScribeLog-receipts/c2-c0-amendment7.stdout`,
`w2/T55W2Read01-receipts/r03-c2-run-at-c0.stdout`, `w2/T55W2RevDocsArms-receipts/c2-both-revisions.txt`,
…) were produced by the **pre-amendment-8** bookkeeping bytes and print `total=1 C2_R55_PASS=false`
at an all-green tree — the exact defect amendment 8 repaired. A report that cites "a wave receipt"
inherits whichever of the two it happened to open. The `Before → after` after-column must cite
`after/c2.stdout` from the deciding run (frozen bytes at `<FREEZE>`), never a wave receipt, and the
`Work performed` section may cite the pair only as *"10 receipts at total=0, 7 at total=1 (pre-amendment-8)"*
with amendment 8 named.



```
# command: git show 9cf0146b:corpus/QUALITY.md | grep -c '^### Criterion 106'
0
# command: git diff 0a2010ac..9cf0146b -- corpus/QUALITY.md | grep -c '^-Falsifier'
1
```

`LOG.md:2547-2548` states "QUALITY 106 (a control is scored at the revision it certifies)
with an erratum on 105". The tree appends no criterion 106 and no `## Criteria appended — round
55` section; the single change is criterion 105's falsifier line rewritten in place
(`rekeyed=7/7 on its positive control` → `… at its deciding revision and rekeyed=3/7 …
[ER-R54-1]`). That directly contradicts this file's own criterion 4 ("Errata are append-only
blocks") and the criterion at `corpus/QUALITY.md:1430` ("corrected by an appended erratum,
never by rewriting the record"). Either append the missing criterion and the erratum, or
restate the `Landed changes` row as a falsifier re-derivation — do not let the report claim
a criterion the tree cannot show.

### A5 — MAJOR: the freeze pointer in the wave spec is stale; a deciding run at that pointer prints `FROZEN_UNCHANGED=0`

The wave-3 context says "counter freeze `133b2ce` (7 amendments)". The manifest re-derives
at five candidates and the tip is the only one with nine amendments:

```
FREEZE_CAND 631cd6455e58 OK files=6 amendments=0
FREEZE_CAND e2979f277138 OK files=7 amendments=7
FREEZE_CAND 133b2ce6d4d8 OK files=7 amendments=8
FREEZE_CAND c31cdd92345a OK files=7 amendments=8
FREEZE_CAND 4f7a7040a57e OK files=7 amendments=9
# command: git diff 133b2ce..4f7a704 -- <deciding-run FROZEN list>
 .ufo/evidence/round-55/c1/measure.py   | 14 +++++++++++---
 .ufo/evidence/round-55/contract.json   |  8 ++++++--
 .ufo/evidence/round-55/deciding-run.sh |  2 +-
 .ufo/evidence/round-55/freeze.json     | 12 ++++++++----
```

A deciding run with `FREEZE=133b2ce` (or `c31cdd9`) against any `REV` after `4f7a704` prints
`FROZEN_UNCHANGED=0` and sets `rc=1` — the round would fail its own gate for a bookkeeping
reason, which is ER-R54-2's class re-entered. The report must name the pointer the deciding
receipt actually prints. Receipt: `freeze-pointer.txt`.

### A6 — MAJOR: the artefacts the report must cite are untracked, and the clean-tree gate would refuse

```
# command: git cat-file -e master:<path>
.ufo/waves/round-55/spec-w2.json -> UNTRACKED
.ufo/waves/round-55/spec-w3.json -> UNTRACKED
.ufo/waves/round-55/w2/T55W2ScoutColdread-receipts/precheck.stdout -> UNTRACKED
.ufo/waves/round-55/w3/swarm-registry.json -> UNTRACKED
# command: git status --porcelain | grep -vc '^??'  /  | grep -c '^??'
52
183
```

Consequences: (i) the report cannot cite wave-2/3 shape or the `46/18` precheck by path at
the landing tip, and `corpus/QUALITY.md:1430` calls a backticked path that does not exist at
the tip a landing defect; (ii) `deciding-run.sh` writes `clean-tree-before.txt` and refuses
`dirty-tree` with 52 modified tracked files (three of them are the very `tools/*.py`,
`registry.json` and note the round edited) plus 183 untracked. The 52 modified files are
peer/in-flight state at this read; they must be committed (or reverted) before the gate.
Receipt: `untracked-evidence.txt`.

### A7 — MINOR: the frozen C2 counter's own description still carries the pre-amendment denominators

```
# command: sed -n '28,34p;279,283p' .ufo/evidence/round-55/c2/measure.py
           names all eight allocating modes;
`C2_R55: rev=... grammar=N/8 … docs=N/7 note=N/8 skill=N/1 …`
      print("C2_R55: rev=%s grammar=%d/%d … tmp_mkdirs=%d docs=%d/7 note=%d/9 skill=%d/1 …"
```

The docstring says eight allocating modes and `note=N/8`; the code emits `len(allocating)`
= 9 and hardcodes `note=%d/9`. Amendment 6/8 changed the code and not the text. This is a
disclosure item for the report (a frozen file cannot be edited without amendment 10, and the
freeze is closed); a reader of the counter is otherwise misled about the predicate it scores.

### A8 — INFO: tool-install line

```
# command: grep -rn "uv tool install\|pip install\|npm install -g\|pacman -S\|cargo install" .ufo/waves/round-55/
(no output)
```

The report's `Tool installs: none` is evidenced by that empty sweep; no pacman transaction
was attempted (host pause respected).

---

## 6. Residual risk and verification gaps

- **No language server covers this surface.** The findings are about markdown records and
  shell/python driver semantics; `.md` has no server and the `.py` claims were settled by
  *executing the committed bytes* (binder traceback) rather than by reference lookup, which
  is stronger evidence than an `lsp` answer would be. Two claims are text-derived and are
  labelled as such: A3's "eight allocating modes" (a grep of `LOG.md:2545`) and A4's
  "no criterion 106" (a grep of the committed blob; a heading written as `### Criterion 106
  —` is the only shape the file uses — checked against 103/104/105).
- **Live-tree reading.** The lane's working tree moved under this seat: `control/controls-a.stdout`
  grew from 1 to 4 lines, `integrate/resolutions.json` changed (`M`), the reader count went
  12/18 → 13/18, and the untracked count 178 → 183. Every finding above cites a commit
  (`9cf0146b`, `4f7a704`) or a scratch-clone run, never those moving files, except where a
  file is explicitly marked untracked/in flight (A2, A6).
- **Not in scope, and not checked**: whether the round can still reach 18/18 readers and a
  green bind within its seat budget (5 headings had no reader at capture) — that is the
  simplifier's and the L1's call; and whether `unprovable-but-better` or `improved` is the
  honest discernment verdict, which needs the independent non-author verifier the round does
  not yet have. The skeleton deliberately leaves the three verdict words as placeholders so
  the L1 cannot inherit this seat's guess.
- **One structural risk the skeleton cannot fix**: the marker rule reads a report whose
  `Before → after` after-column is empty as *failed* only when the rest is contentless; here
  the rest is rich, so an honest stop is writable. What is **not** writable today is a report
  that claims `C1_R55_PASS=true` or `C2_R55_PASS=true` at a deciding revision — no receipt
  says so, and A1/A2 are why.
