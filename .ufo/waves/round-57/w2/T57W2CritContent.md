# T57W2CritContent — attack on C0 `ca75c2674645ab6bdadeecb8584007c74342bfa9`

Seat: T57W2CritContent (wave 2, critic, content). Lane base `5e3569969b532310d2b8a3d130901757a3df356b`.
Scope: the 13 files of C0 (SKILL.md rows 53 and 1547; QUALITY criteria 108–110; SOURCES S283–S285;
`corpus/knowledge/gate-row-exit-map.md`; the receipt-revision-binding errata; the README coverage row;
the round-57 lesson corrections R53.8, R55.2, R56.7). Judged on calibration.
Machine-readable: `T57W2CritContent.json`. Receipts: `T57W2CritContent-receipts/`. Staged fix:
`T57W2CritContent/stage/T57W2CritContent.diff` (`git apply --check` passes at C0).

Tooling: no tool installed or upgraded. Used `git`, `python3`, `curl` (already present), `diff`.

## Verdict

C0 is mostly sound. The gate does what the SKILL rows and the registry rows say, the three new gate
rows execute and hold, the S283/S284 quotes are verbatim, and the ledger-label counts in the referent
record are right. Eight defects: five are errors in new prose (D1 a misquote the round-57 lesson
presents as a finding; D2 a self-contradiction on exit 2; D3 a routed item closed by C0 but still
open in the text; D4 a revision-free claim that is false at the round tip; D5 a rule file the lane
does not contain); two are in QUALITY (D6 a criterion the landing round cannot satisfy; D7 a wrong
source for the exit map); one cites an untracked receipt (D8).
All proposed text fixes except the QUALITY pair are in unmonitored files (lesson, new knowledge entry),
so they cost no cold-read credit. The two QUALITY edits add no lost heading (measured below), but
they must land before the wave-3 re-read binds, or they cost a re-read.

## Defects (path:line, evidence, staged fix)

### D1 — R55.2 quotes a string the report does not contain (lesson, unmonitored; fix staged)
- `corpus/lessons/round-57.md` R55.2 bullet (C0 lines 19–24). It says the round-55 report quotes the
  C2 run as `grammar=9/9 … note=9/9 skill=1/1 total=0`.
- Evidence: `git grep "skill=1/1 total=0"` at tip `06e9849` hits only `T55W1CritC2` (a different
  seat's run at `rev=252742953e0c`) and `w1-results.json:76`. The report `T55W1ScribeSkill.md` has:
  line 148 `total=1 C2_R55_PASS=false` (the 9-mode run, correct) and line 157
  `grammar=8/8 … total=0 C2_R55_PASS=true`, explicitly labelled the earlier 8-mode run
  (`9de7dea`). The string `grammar=9/9 … total=0` does not occur in the report.
- So the R55.2 finding is a verifier misquote, not a report that contradicts its receipt. The C0
  correction repeats the misquote and also says the report "is fleet-side"; it is lane-side
  (`.ufo/waves/round-55/w1/`). The routed item should be answered as a misquote.
- Fix: the staged diff rewrites the R55.2 bullet with the three line references.

### D2 — gate-row-exit-map contradicts itself on exit 2 (knowledge, new and unpinned; fix staged)
- `corpus/knowledge/gate-row-exit-map.md:92-93` says "The header's could-not-evaluate class is exit 2".
- Same file line 29 says the header documents exit 0, exit 3 and the eleven codes, and exit 2 appears
  only in the code. The gate header (`tools/receipt-revision-gate.py:25, :32`) documents only
  "Codes … exit 3" and "Exit 0 iff PASS". Exit 2 is at `:194` only.
- Measured: `grep -n -i "exit\|could" tools/receipt-revision-gate.py` (receipt in `T57W2CritContent-receipts/`
  is the sweep; header lines quoted above).
- Fix: staged (the entry now says exit 2 is in the code at `:194` and the SKILL row, not the header).
  Cost: the entry is `NEW` to the forecast tool and no ledger entry pins it (`grep` over
  `.ufo/evidence/round-21` is empty), so 0 readers.

### D3 — gate-row-exit-map routed item 2 is closed by C0 but still reads as open (knowledge; fix staged)
- `corpus/knowledge/gate-row-exit-map.md:95-96`: "`SKILL.md` `## Standing rules`, row one, names
  `RECEIPT_REV_MISMATCH` … Routed, not fixed here".
- C0 changed SKILL.md line 53 to `RECEIPT_REV_CONTENT_DRIFT` (`git show ca75c26 -- SKILL.md`). The
  entry is written at base, so the wording is not false about base, but the routed item now reads as
  an open defect at C0.
- Fix: staged, a one-line "Fixed at C0 `ca75c26` (SKILL.md:53)" note.

### D4 — R56.7 names no revisions, and read at round-57 tip it is false (lesson, unmonitored; fix staged)
- `corpus/lessons/round-57.md` R56.7: "the sentence holds for the interval from the pinned bind
  revision to the round's final tip".
- Evidence: `git diff --stat 877eedee3ddb7fe25d7a6a09922b04ba13e5a99b 5e3569969b532310d2b8a3d130901757a3df356b -- SKILL.md corpus/QUALITY.md corpus/SOURCES.md corpus/knowledge tools` prints nothing (the sentence holds from `877eedee` to base). Repeating the diff to C0 `ca75c26` shows 11 files changed, so the sentence is false for any tip after C0.
- The lesson's own stat numbers are correct: `c0137451f5b7 877eedee3ddb -- corpus SKILL.md tools`
  gives `QUALITY.md +31`, `SOURCES.md +2`, `receipt-revision-binding.md +39`.
- Fix: staged, names `877eedee..5e35699`.

### D5 — R53.8 cites a rule file this lane does not contain (lesson, unmonitored; fix staged)
- `corpus/lessons/round-57.md:17`: "the 25-word bound of CORPUS.md SOURCES rule 1". The lane has no
  `CORPUS.md` (`ls` of the lane root; `corpus/` has none). The rule is the fleet-root `CORPUS.md`
  `### Rules` item 1 (`/home/vgpnk/Projects/shokunin/CORPUS.md:112-114`, "a ≤25-word quote"). The lane's
  SOURCES.md header names a third file, `SOURCES-CONTRACT-v1.md`.
- The counts are right: the two quotes are 20 and 20 words (`python3 -c 'print(len(q.split()))'`).
- Fix: staged, names the fleet-root file.

### D6 — QUALITY criterion 110 cannot be satisfied by round 57, the round that lands it (monitored; fix staged, must bind before wave-3)
- `corpus/QUALITY.md:1727`: "The round's contract carries a `coldread_forecast` key, committed before
  the round's first content edit".
- Evidence: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/contract.json` is
  untracked (`git status --short` shows `??`), and its keys are `lane round attempt l1 base base_note
  shape lowest_axis claims no_harm frontier routed_defects_from_round_56 frozen_paths`. No
  `coldread_forecast` key. The criterion's falsifier checks round 52 only, so it passes the falsifier
  test while failing round 57.
- Fix: staged, "From round 58 on, …".
- Cost, measured: `python3 tools/cold-read-forecast.py --lane <C0> --rev ca75c26 --paths corpus/QUALITY.md`
  → `FORECAST: paths=1 headings=0 readers=0 of 64`, `18 heading(s) already uncovered`. C0 already
  loses 18 headings (`--rev 5e35699 --diff-to ca75c26` → `headings=18 readers=18 of 64`), so a further
  QUALITY edit adds no reader, provided the wave-3 re-read binds after the final bytes.

### D7 — QUALITY criterion 109 names the header as the exit-map source; the header documents only 0 and 3 (monitored; fix staged, same cost as D6)
- `corpus/QUALITY.md:1719`: "names each exit code the tool's header documents with its class. … the map
  is 0 = PASS, 2 = certified revision unresolvable, 3 = refused". The header (`receipt-revision-gate.py:25,
  :32`) has no exit 2, so the criterion's own map cannot be derived from its named source.
- Fix: staged, "its SKILL.md exit-map row documents".

### D8 — the S285 receipt is untracked, so the row's anchor resolves at no commit (SOURCES; no text change staged)
- `corpus/SOURCES.md:160`: receipt `.ufo/waves/round-57/w1/T57W1ScoutSourceB-receipts/atlassian-postmortems.html`,
  "receipt line 42055".
- Evidence: `git status` shows `??`; `git cat-file -e 06e9849:<path>` fails; the file is absent from C0
  and from the wave-1 commit. Its bytes match the row: sha256 `2644d1c9…a87369`, 2313661 B
  (`T57W2CritContent-receipts/sources-rederive.txt`). Line 42055 contains the quoted text.
- The quote is true: the page reads "We practice <a>blameless postmortems at Atlassian</a> to ensure…".
- The row is not a criterion-97 breach as written (97 lists SCORECARD, LOG, QUALITY and lessons), but
  nothing committed can reproduce the anchor. Round 56 landed `888d342e` with ">1 MiB receipts named as
  files"; if that is the practice for this file, the row should say so.
- Fix: commit the receipt (preferred; no SOURCES byte changes, so no cold-read cost) or add the
  named-file note. No SOURCES diff staged, because any SOURCES byte costs the Registry heading's credit.

## Checked and clean (with the command and its output)

- SKILL.md rows 53 and 1547 vs the gate. `python3 tools/receipt-revision-gate.py --selftest` → `GATE_SELFTEST: 19/19 pass`.
  Row 53 (`--paths` drift → `RECEIPT_REV_CONTENT_DRIFT`, rc 3; no `--paths` → `RECEIPT_REV_MISMATCH`) matches
  the gate's branches at `:139-155`. Row 3's "exit 3" for an unresolvable CTL line: a control receipt with
  `rev=deadbeefdeadbeef` gives `code=RECEIPT_REV_UNRESOLVABLE`, rc 3. "Unresolvable `--certified` exits 2":
  `GATE: error=unresolvable-certified … verdict=REFUSED` rc 2 (`:194`).
- SKILL line count: `git show 5e3569969b53:SKILL.md | wc -l` → 2214; C0 → 2214.
- Page-local anchors: parsed every `SKILL.md:N[-M]` in `corpus/ tools/ SKILL.md README.md AGENTS.md` at C0
  for overlap with line 53 or 1544–1552 → 0 hits. (The historical waves cite `SKILL.md:1548-1562` for an older
  layout; those are records and were not edited.)
- Registry rows: `python3 tools/registry-check.py --rev <scratch commit> --tag new-r57` → `ROW … held` ×3,
  `REGISTRY_CHECK: held=3/3 superseded=0`, rc 0; `--only` per row held 1/1 each; the base tag selects nothing
  (`could-not-evaluate`, rc 2).
- Gate sweep (`gate-sweep.sh` at tip, `T57W2CritContent-receipts/gate-sweep.stdout`): the 13 rc-3 cases
  (12 fixtures plus `json-drift`), rc 2 for `certified-unresolvable`, rc 1 for `usage-no-receipt` and
  `paths-file-missing` (`FileNotFoundError` at `:197`), all match the knowledge truth table.
- Lane-demo (`T57W2CritContent-receipts/lane-demo.stdout`): `codes defined: 11 | emitted by the sweep: 11`,
  `emitted by a staged row: 2`, `emitted by no registry row: 9`. The knowledge's numbers match.
  The base claim (`RECEIPT_MISSING` rc 3 from the lane before the fixtures land) is in the wave-1 receipt
  `lane-demo.stdout` at tip (not re-run at base; the lane now has the fixtures).
- QUALITY 108: `git show 5e35699…:corpus/routed-defects.json | python3 -c …` → `rows 49 rows_r50_56 0`; `git ls-tree
  --name-only 5e35699… .ufo/evidence/round-53/after/` → empty; lesson `round-56-verifier-spotcheck.md` §6 lists
  R56.1–R56.7; `considerthese/2026-10-28.md` exists. Falsifier fails at base as intended.
- QUALITY 109: `gate-rows-naming-gate 0` at base; `gate-rows-at-C0 3`; `D-CF3` exists in the cited lesson §1.
- QUALITY 110: round-52 `contract.json` keys match the criterion text (no `coldread_forecast`); its
  `no_harm.coldread_note` quote matches; `lost=19 RED` is in `round-52-verifier-spotcheck.md:53`.
  The receipt `precheck-quality-2line.txt` (at tip) reads `COLDREAD_PRECHECK … cand_credited=58 lost=6 RED`.
- S283: fetched `https://www.gnu.org/software/grep/manual/grep.html` → 248692 B, sha256 `517177d0…675f37` (matches the
  row). §2.3 text: "Normally the exit status is 0 if a line is selected, 1 if no lines were selected, and 2 if an
  error occurred. However, if the -q or --quiet or --silent option is used … Other grep implementations may exit
  with status greater than 2 on error." Row quote verbatim. Receipt lines 1208–1209 contain it.
- S284: fetched `https://sre.google/workbook/postmortem-culture/` → 103251 B, sha256 `25b55c64…0bd22` (matches the
  row). "A postmortem is a factual artifact that should be free from personal judgments and subjective language" is
  verbatim under "Animated language". Receipt line 666 contains it. Status `queued` is in the registry vocabulary (22 rows).
- Ledger labels (`T57W2CritContent-receipts/ledger-labels.txt`): entries 591–608 (0-based) carry 13 SOURCES and
  6 QUALITY labels. Against `c0137451` (the labelled commit) all 13 and all 6 mismatch. Against `877eedee` 0
  mismatch. The referent record's 13/6 and digests `11c56829…` (SOURCES, c0137451), `6c2096d8…` (SOURCES,
  877eedee), `80792b7d…`, `54c49d38…` are correct. (A first probe with a mistyped hash found no `877eedee`;
  the committed full hash `877eedee3ddb7fe25d7a6a09922b04ba13e5a99b` is correct, so no edit is proposed.)
- Errata ER-R57-K1: frontmatter `recheck:` says `14/14`; `GATE_SELFTEST: 19/19 pass`; gate sha256 `c60772ce…0569ac9`
  matches the tip file.
- README coverage row: table header matches the other coverage tables (`| Note | Holds | Sources |`); its numbers
  (2 of 11 codes, 19/19, exit map) match the checks above. No change.
- R53.8: lesson lines 23 and 31–32 quote 22 and 19 words; the quoted strings count 20 and 20.
- R56.7: lesson lines 316–318 match the quote; the diff numbers match (see D4).

## Not attacked

- `tools/cold-read-forecast.py` (805 lines, C0): outside the item list. Ran its retrospective and
  marginal modes (above); its code was not reviewed.
- The uncommitted ledger working-tree edit (`corpus/routed-defects.json`, `M` in the lane): outside C0.

## Staged files

- `T57W2CritContent/stage/T57W2CritContent.diff` — `diff -u` for `corpus/QUALITY.md` (D6, D7),
  `corpus/knowledge/gate-row-exit-map.md` (D2, D3), `corpus/lessons/round-57.md` (D1, D4, D5).
  Apply at C0: `git apply --check` passed in a scratch clone.
- No SOURCES, SKILL or README diff: no defect there is worth a re-read (D8 is a commit, not a byte change).

## Cost note for the L1

- C0 already loses 18 headings (retrospective forecast). A further monitored edit inside an already-lost
  file adds 0 readers (measured for QUALITY.md, `headings=0`), so D6/D7 are free only if they land before the
  wave-3 re-read binds the 18 headings.
- The unmonitored edits (D1–D5) cost nothing.
- Commands to re-run after the L1 installs the stage: `bash .ufo/waves/round-57/dry-c1.sh` and
  `bash .ufo/waves/round-57/dry-c2.sh` (the dry runs in the wave specs), plus the gate selftest and
  `registry-check.py --rev <content commit> --tag new-r57`.
