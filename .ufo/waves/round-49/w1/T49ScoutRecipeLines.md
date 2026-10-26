# T49ScoutRecipeLines — line-shift map for the recipe/restore pointers into the two census notes

Base `8ca67421111fa354b47b803358391d0b07fc6db9`. Pointer source: `.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json` (90 pointers; the recipe heading has 34, the restore heading 10; 40 of those are `line` pointers into the two notes, 13 distinct kimi ranges + 14 distinct kagi ranges, tabled below). Read-only recon; no counter run.

## 1. Commits that touched each note

Commands: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --follow --format='%h %ad %s' --date=short -- corpus/knowledge/mutation-case-kimi-census.md` (and kagi); round-11 boundary = `284ab0f` ("probation round 11 (training r10, FINAL)", 2026-10-14).

| note | commit | date | effect | shifts a line before any cited line? |
|---|---|---|---|---|
| kimi | `2587e0a` | 2026-10-14 (round 2) | creates note, 207 lines | n/a (origin) |
| kimi | `e0c453e` | 2026-10-14 (round 5) | appends `## Errata (round 5)` after old last line; hunk `@@ -204,4 +204,35 @@`; old line 207 (`  reads the live tree by construction.`) is fused with the new `## Errata` heading (no newline at EOF) | no: only lines >= 207 touched |
| kagi | `53e74a8` | 2026-10-14 (round 3) | creates note, 259 lines | n/a (origin) |
| kagi | `8eaae28` | 2026-10-21 (round 21) | appends `## Erratum R21` after old line 259; hunk `@@ -256,4 +256,20 @@` (only the final line's missing newline and 16 appended lines) | no: only lines >= 259 touched |

Since round 11 (`284ab0f`): kimi has NO commit; kagi has exactly one (`8eaae28`, EOF append). `git diff --stat 284ab0f 8ca67421 -- <both notes>` shows only the kagi file, 17 insertions / 1 deletion. Base lengths: kimi 237 lines, kagi 274 lines (`wc -l`).

Verification of "no shift": line-by-line comparison of `git show <rev>:corpus/knowledge/<note>` for every historical revision against the base blob. kimi `2587e0a` equals base for lines 1-206 (first differing line 207, the fused-heading line); kimi `e0c453e`/`284ab0f` equal base entirely; kagi `53e74a8` and `284ab0f` equal base for lines 1-259; kagi `8eaae28` equals base entirely.

## 2. Line-shift map

The map is the identity: for every cited range, old line = base line (shift 0), across every revision in section 1. The highest cited line is kimi 191 (note has 237) and kagi 253 (note has 274), both far below the first edited line of any commit (kimi 207, kagi 259). Consequence for the readers: a cited range in either note that does not match its claim at base is a WRONG pointer (authored off), never a DRIFTED one. The only question left is whether it was authored wrongly or the claim is wrong.

One sub-caveat: the pointers could have been authored against some revision other than these (the SKILL recipe was written in round 3, `53e74a8`/`dd2f4dee`, before kimi's round-5 append). That does not matter: both appends sit after every cited line, so any authoring revision after `2587e0a` (kimi) / `53e74a8` (kagi) yields the same line numbers.


### mutation-case-kimi-census.md

| cited range | old -> base | cited by (section#ordinal@SKILL line) | base text, first line | base text, last line |
|---|---|---|---|---|
| 4-7 | 4-7 -> 4-7 (shift 0) | recipe#0@SKILL:141, restore#2@SKILL:384 | `axis: depth). Substrate: kumitate-shokunin **read-only** — every mutant is a cop` | `pointed at an empty dir under `/tmp`.` |
| 13-16 | 13-16 -> 13-16 (shift 0) | recipe#5@SKILL:152, restore#0@SKILL:382 | `Artifact under test (O: `sha256sum`, `stat`, `git rev-parse`): sha256` | ``git status --porcelain -- scripts/kimi-census.mjs` empty.` |
| 20-21 | 20-21 -> 20-21 (shift 0) | recipe#3@SKILL:147, recipe#28@SKILL:241 | `- O: control run, unmutated copy — `node pristine.mjs --selftest` →` | `  `KIMI_CENSUS_SELFTEST: 43/43 pass` / `VERDICT: PASS`, exit 0 (node v24.21.0).` |
| 22-25 | 22-25 -> 22-25 (shift 0) | recipe#11@SKILL:174 | `- O: each defect = ONE exact-string replacement applied to a fresh copy of the p` | `  compounds with another.` |
| 26-28 | 26-28 -> 26-28 (shift 0) | recipe#13@SKILL:186 | `- O: per-defect evidence: `node mutant-<id>.mjs --selftest` full stdout →` | `  aggregate → `evidence/results.json`.` |
| 29-31 | 29-31 -> 29-31 (shift 0) | recipe#21@SKILL:212, recipe#28@SKILL:241 | `- O: **kill rate 8/10 (80 %)**; survivors D2, D10. No inconclusive run — each of` | `  wall against the 300 s timeout.` |
| 30-33 | 30-33 -> 30-33 (shift 0) | recipe#15@SKILL:194 | `  11 runs (control + 10) produced a definitive suite verdict; the whole sweep to` | `  all three green runs printed exactly `KIMI_CENSUS_SELFTEST: 43/43 pass`.` |
| 34-35 | 34-35 -> 34-35 (shift 0) | recipe#25@SKILL:226, restore#4@SKILL:388 | `- O: restore proof — original sha256 before `83016d45…4f426` and after `83016d45` | `  size 43273 B and mtime unchanged; kumitate working tree clean for that path.` |
| 41-53 | 41-53 -> 41-53 (shift 0) | recipe#8@SKILL:166 | `\| # \| Defect class \| Injected defect (ref = edit site) \| Exit \| Suite line \| Ver` | `\| D10 \| wrong reported constant \| `FROZEN.K2 25` → `24` (kimi-census.mjs:145) \| ` |
| 44-53 | 44-53 -> 44-53 (shift 0) | recipe#20@SKILL:207 | `\| D1 \| off-by-one count \| K2 counted dir `counted: 18` → `17` (kimi-census.mjs:1` | `\| D10 \| wrong reported constant \| `FROZEN.K2 25` → `24` (kimi-census.mjs:145) \| ` |
| 59-76 | 59-76 -> 59-76 (shift 0) | recipe#17@SKILL:196 | `Failing-case labels of the narrow kills (O: `evidence/<id>.selftest.txt`):` | `  remaining CLEAN/exact-line cases plus the count-string (`'19 children, 18 decl` |
| 82-99 | 82-99 -> 82-99 (shift 0) | recipe#23@SKILL:218 | `**D2 — render truncation off-by-one (kimi-census.mjs:378).** O: 43/43 PASS.` | `frozen=25`; D10 `… frozen=24`.` |
| 155-166 | 155-166 -> 155-166 (shift 0) | recipe#8@SKILL:166 | ````` | ````` |
| 183-191 | 183-191 -> 183-191 (shift 0) | recipe#9@SKILL:169 | `## 5. Calibration and errata (append-only)` | ``!== floor` rejects them (§3, D7). Recorded as a calibration miss.` |

### mutation-case-kagi-census.md

| cited range | old -> base | cited by (section#ordinal@SKILL line) | base text, first line | base text, last line |
|---|---|---|---|---|
| 13-17 | 13-17 -> 13-17 (shift 0) | recipe#6@SKILL:153, restore#1@SKILL:382 | `Artifact under test (O: `sha256sum`, `stat`, `git`): sha256` | ``git status --porcelain -- corpus/surface-census.sh` empty.` |
| 24-38 | 24-38 -> 24-38 (shift 0) | recipe#1@SKILL:141 | `- O: the selftest builds every fixture under `mktemp -d` and re-invokes the gate` | `  edit verify/shapes logic, so this does not touch the measured table; kept as U` |
| 27-35 | 27-35 -> 27-35 (shift 0) | recipe#4@SKILL:148, recipe#16@SKILL:194 | `- O: the two trailing verb cases are substrate-gated: `command -v "$JANITOR"` (`` | `  substrate-gated cases that performed no execution.` |
| 42-43 | 42-43 -> 42-43 (shift 0) | recipe#4@SKILL:148 | `- O: control run, unmutated byte copy — `bash control.sh --selftest` →` | `  `SELFTEST: PASS (16 cases)`, exit 0, 1.0 s wall.` |
| 44-45 | 44-45 -> 44-45 (shift 0) | recipe#7@SKILL:160, restore#3@SKILL:385 | `- O: each defect = ONE exact-string replacement applied to a fresh copy of `pris` | `  `cp -p` byte copy, `cmp`-verified); the driver asserts the old string occurs e` |
| 44-47 | 44-47 -> 44-47 (shift 0) | recipe#12@SKILL:175 | `- O: each defect = ONE exact-string replacement applied to a fresh copy of `pris` | `  the kagi original was never written, and no live host surface was read by any ` |
| 48-49 | 48-49 -> 48-49 (shift 0) | recipe#14@SKILL:187 | `- O: per-defect evidence: full combined output → `evidence/<id>.selftest.txt`; e` | `  sha256 + wall time + case summary → `evidence/<id>.meta.json`; aggregate → `ev` |
| 50-53 | 50-53 -> 50-53 (shift 0) | recipe#16@SKILL:194, recipe#22@SKILL:213, recipe#29@SKILL:243 | `- O: **kill rate 8/10 (80 %)**; survivors B5, B10. No inconclusive run — each of` | `  (~1.0 s each) against the 280 s per-run bound.` |
| 54-56 | 54-56 -> 54-56 (shift 0) | recipe#26@SKILL:227, restore#5@SKILL:390 | `- O: restore proof — kagi sha256 before `275d8294…53009f` and after `275d8294…53` | `  `cmp`-identical to the kagi original after the sweep.` |
| 82-103 | 82-103 -> 82-103 (shift 0) | recipe#18@SKILL:199 | `Failing-case labels (O: `evidence/<id>.selftest.txt`, exact bad-case lines):` | `  runtime reported GONE, exit 1) — the two classes swap.` |
| 88-91 | 88-91 -> 88-91 (shift 0) | recipe#19@SKILL:203 | `- B4 (1): `bad-case 07 symlink-swap want exit=1 token=SURFACE LINK got exit=1` —` | `  passed this deletion.` |
| 111-114 | 111-114 -> 111-114 (shift 0) | recipe#24@SKILL:221 | ``grep -n -- '-x ' surface-census.sh` → `214`). O (non-equivalence): on a probe r` | ``SURFACE OK       … (exec 644)` exit 0 (`evidence/probe-B5-non-equivalence.txt`)` |
| 118-122 | 118-122 -> 118-122 (shift 0) | recipe#24@SKILL:221 | `**B10 — CLEAN-summary count (`surface-census.sh:862`).** O: 16/16 PASS. O: no ca` | ``… ok=0 …`; both exit 0 (`evidence/probe-B10-non-equivalence.txt`). Same class a` |
| 184-191 | 184-191 -> 184-191 (shift 0) | recipe#10@SKILL:170 | `## 5. Calibration and errata (append-only)` | `about the fixtures, not the edits (same shape as round-2 E1).` |
| 251-253 | 251-253 -> 251-253 (shift 0) | recipe#24@SKILL:221 | `` | `exit 0 (pristine prints `SURFACE DIVERGED … no execute bit`, exit 1); B10's summ` |

(`recipe#N`/`restore#N` = ordinal in the pointer JSON; `@SKILL:L` = SKILL.md line of the citation at base. The two rows citing kimi 155-166 and kagi 251-253 start/end on fence/blank lines; see section 3.)

## 3. Boundary check of each cited range at base (anchors read, `sed -n` over the note)

Because no shift exists, I read the line before the first and after the last of every range. Findings:

- **kagi 251-253 is off by one (wrong pointer, not drift).** Cited by recipe#24 (`SKILL.md:221`, text `mutation-case-kagi-census.md:111-114, :118-122, :251-253`). Line 250 is the closing code fence, 251 is blank, 252 `Sensitivity checks expected from the note alone: B5's run must print `SURFACE OK … (exec`, 253 `exit 0 (pristine prints `SURFACE DIVERGED … no execute bit`, exit 1); B10's summary must`, 254 `` `ok=0` (pristine `ok=1`), both exit 0.``. The sentence the SKILL claim ("B5 prints SURFACE OK … exec 644 exit 0 where pristine prints SURFACE DIVERGED … no execute bit exit 1; B10: ok=0 where pristine prints ok=1") rests on is 252-254. Command: `sed -n '250,254p' corpus/knowledge/mutation-case-kagi-census.md`. The citation at 251-253 is a blank line plus two lines of a three-line sentence and omits the `ok=0` clause (254).
- **kagi 111-114 starts mid-paragraph (boundary note, not an error).** The B5 paragraph starts at 107 (`**B5 — deleted exec x-bit arm (`surface-census.sh:214-217`).**`); 111 is the `grep -n -- '-x '` clause, 112 `whose file is not executable, pristine prints`, 113 the `SURFACE DIVERGED …` output, 114 the `SURFACE OK … (exec 644)` output. The SKILL claim (B5 prints SURFACE OK exec 644) is fully inside 111-114. Command: `sed -n '107,115p' corpus/knowledge/mutation-case-kagi-census.md`.
- **kimi 155-166 and kimi 183-191 / kagi 184-191** are exact units: 155 and 166 are the opening/closing ``` fences of the D1..D10 driver-spec block; 183/184 are the `## 5. Calibration and errata (append-only)` headings. Kimi §5 heading at 183, kagi §5 heading at 184; kimi 183-191 ends at the last §5 line ("Recorded as a calibration miss"); kagi 184-191 ends "(same shape as round-2 E1)".
- All other ranges start on a bullet/paragraph first line and end on a paragraph last line (13-16/13-17 artifact paragraphs, 20-21 control run, 22-25 + 44-47 mutation-injection bullet [kimi 22-25, kagi 44-47], 26-28 / 48-49 evidence bullet, 29-31 / 50-53 kill-rate bullet, 34-35 / 54-56 restore proof, 4-7 hermeticity sentence). kimi 30-33 and kimi 29-31 overlap the kill-rate bullet (29-31) plus continuation (30-33 starts mid-bullet by design: "11 runs … all three green runs"); kagi 44-45 is a prefix of the 44-47 bullet (cites the cp -p byte copy part, fine).
- **kagi 24-38**: bullets 24-38 are the hermeticity/selftest-fixture bullets; fine at both ends.

Restore-section line pointers into the notes: kimi 13-16, kagi 13-17, kimi 4-7, kagi 44-45, kimi 34-35, kagi 54-56: all exact, no drift.

## 4. Non-note line pointers present in the same two sections (for completeness, not scoped to shift)

recipe#2 `gates-survey-kumitate.md:19-31` (SKILL:143), recipe#27 `SKILL.md:377-378` (SKILL:228), restore#6 `SCORECARD.md:13` (SKILL:397). Not examined here: the item names only the two census notes.

## Summary
- Neither census note shifted any cited line: kimi last changed `e0c453e` (r5, EOF append at 207); kagi `8eaae28` (r21, EOF append at 259). The old->base map is identity for all cited ranges (kimi max cited 191, kagi max 253).
- Since round 11 (`284ab0f`): kimi untouched; kagi one commit, `8eaae28`, EOF-only.
- So any mismatch between a cited range and its claim at base is a wrong pointer, not drift.
- One off-by-one found: kagi `:251-253` (recipe#24, `SKILL.md:221`) should be `:252-254`; 251 is blank, 254 holds the B10 `ok=0` clause.
- All other kimi/kagi line ranges read at base matched their claim and had clean paragraph boundaries; kagi `:111-114` starts mid-paragraph but contains the cited text.
- Not examined: gates-survey-kumitate.md:19-31, SKILL.md:377-378, SCORECARD.md:13.
