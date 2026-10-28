# T54W2Read07 — cold read at C1: `### Triggers T1–T3 and the re-pin rule`

- Seat: `T54W2Read07` (scribe/reader, wave 2 of tameshi round 54; L1 `TameshiR54a2`)
- Section: `### Triggers T1–T3 and the re-pin rule`
- Revision read: `99c3bc88d704566197783f66b211ee0a830e0330` (C1)
- Span: start 1083, end 1105 (section body = lines 1083–1104; the trailing blank line 1105 is stripped by the sectionizer)
- `section_sha256`: `2350210704efcc3becfbcd40a63775ad591910039744ac6d072881b3deef7801`
- Findings: **1**
- Writes: only `.ufo/waves/round-54/w2/T54W2Read07.{json,md}`. No lane file, counter, contract, freeze, ledger or wave spec touched; no mutating git/jj command anywhere.

## Findings

### 1. The day's harness-move count and the chain it annotates name different sets of revisions

**Quote (byte-exact, section lines 1092–1093):**

```
the harness itself moved four times in
  one day (`597e1419…` → `b56c6e57…` → `4dc69ef9…` → `e3f838d4…` → `cf41efaa…`) [round 52: `4dc69ef9…` and `e3f838d4…` were working-tree writes, not commits (`plans/round-8.plan.md:69-74`, 15:27:40 and 15:28:38); the day's committed chain is `d8abee52…` (created 13:01) → `597e1419…` (13:57) → `b56c6e57…` (15:17) → `cf41efaa…` (16:06) → `75ed934d…` (18:28, r10-2 — `RerunSweep.md:93`) — four moves]
```

**Why:** the count and the chain it annotates cannot both be the day's tally — the parenthetical lists four transitions over `597e1419…`→`cf41efaa…`, but two of its five members (`4dc69ef9…`, `e3f838d4…`) are, by the same bracket, non-commits, while the bracket's own four-move committed chain runs `d8abee52…`→`75ed934d…` and shares neither endpoint; git shows seven distinct harness states on 2026-10-14 (five committed, two no-commit writes), so "moved four times" does not describe the list printed beside it.

**Receipt (the sweep that decides it):**

```
$ git -C tameshi-shokunin log --format='%cI %h' --since=2026-10-14T00:00:00-03:00 \
    --until=2026-10-15T00:00:00-03:00 -- tools/mutate-and-run.sh
2026-10-14T18:28:23-03:00 606716f
2026-10-14T16:06:31-03:00 9f1d3c3
2026-10-14T15:17:26-03:00 4494715
2026-10-14T13:57:18-03:00 b58b26f
2026-10-14T13:01:03-03:00 53e74a8

# distinct committed blob sha256 of tools/mutate-and-run.sh that day
4a5bf430… 75ed934d
935adec3… cf41efaa
a8d3c981… b56c6e57
fc4e9ff8… 597e1419
ff9cc1f9… d8abee52
```

Full-history sweep over every commit that carries `tools/mutate-and-run.sh` (37 commits, 13 distinct blobs) yields the same five 2026-10-14 entries and **no** commit carrying `4dc69ef9…` or `e3f838d4…` — so the bracket's "working-tree writes, not commits" is right, and the base chain's "four moves" counts two of them as moves while omitting `d8abee52…` (13:01) and `75ed934d…` (18:28), which the same bullet calls committed moves. The bullet's two enumerations are mutually exclusive; a cold reader cannot tell which chain is "the day".

Note: this section's bytes are **identical at C0 and C1** (`diff` of `SKILL.md` lines 1060–1110 between `59c38109bf11` and `99c3bc88d704566197783f66b211ee0a830e0330` is empty), i.e. the C1 fix pass did not touch this section and this defect predates it.

## Anchors checked (all of them) and where they resolve at C1

| Anchor in the section | Resolves? | Evidence |
|---|---|---|
| `fleet-kill-rate-ledger.md:170-173` (T3: appended row, §1–§4 never edited) | yes | lines 170–173 end "change as an appended row, not an edit of §1–§4." |
| `fleet-kill-rate-ledger.md:310`, ER-3 (moved pin never re-interpreted) | yes | line 310 is ER-3 trigger 3: "A moved substrate needs a **re-pin**, never a re-interpretation of the old table" |
| `fleet-kill-rate-ledger.md:318`, ER-4 | yes | line 318 is the ER-4 heading, ending "…and a moved pin is never re-interpreted." |
| `fleet-kill-rate-ledger.md:281` (round-8 replay receipt) | yes | line 281 carries tool `cf41efaa8be5f52d…`, four materialized legs, `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)`, run `2026-10-14T19:14:16Z` |
| `RerunSweep.md:19-23` (round-16 runner `89722ddb…`) | yes | lines 19–23: "Tool … → sha256 `89722ddb3082…b61f5594`" |
| `RerunSweep.md:93` (`75ed934d → 89722ddb`) | yes | line 93: "durations, and the tool sha (75ed934d → 89722ddb, the commit-expected r16 tool —" |
| `plans/round-8.plan.md:69-74` (the two working-tree writes, 15:27:40 / 15:28:38) | yes | lines 69–74: `4dc69ef9…` (15:27:40, 1247 L) → `e3f838d4…` (15:28:38) → `cf41efaa…` (15:29:01) |
| `service-optin-protocol.md:232` (SCR-T6 re-ran mado spec under `b56c6e57…`, 4/10) | yes | line 232: "SCR-T6 re-ran the spec under `b56c6e57…`: 4/10, all ten mutant shas identical" |
| `mutation-case-mado-verify.md:17-23` ("the mado note keeps it U") | yes | lines 17–23 are Incident I1: "**Every number in this note is tied to `597e1419…`**; whether the new revision reproduces this table is **U**" |

Cross-checks cleared (no finding recorded):

- T1's figures match the ledger: tsukuroi `084951be…` 6/10 at r5; mado `d7edaab4…` 4/10 at r6 (ledger §1 rows 3/4); `bba6cdf6…` and `7da4ec50…` are the round-8 HEAD blobs (ER-4 table rows 3/4, ledger `:333-338`), and ER-4's addendum ("worktree-dirty again, minutes after the tick") supports "both have moved again since".
- `0673d2e5…` is indeed later than `89722ddb…`: committed 2026-10-20T10:49:37-03 (`89722ddb`) vs 2026-10-20T11:18:08-03 (`0673d2e5`).
- "reproduced case 7" matches the ledger's "'## Round 16 — seventh row appended'" (`:403`) and RerunSweep's verdict ("re-running §1-§2 of `mutation-case-kumitate-round-gate.md` … reproduces every verdict … 5/10 killed, 10/10 predictions").
- "scratch not retained" is an absence claim, not contradicted: `git grep -n "SCR-T6"` over the lane finds it only at `service-optin-protocol.md:232`; round-27 `ReRead07.md:59` records the same absence ("their scratch directory is not in the repo"). Not counted as a defect (unverifiable-in-repo ≠ false).
- "rc 0" on the replay receipt is not printed on ledger `:281`, but `REGRESSION: PASS` ⇒ exit 0 is the tool's documented arm (`SKILL.md:952-953`: "Exits 0/1/2: PASS/FAIL/SETUP"). Not counted.
- Typography sweep of the 22 body lines: no mid-line double spaces, no `)(`, no `))`, no missing space after a period, no NBSP/zero-width bytes.

## Artifacts opened (absolute paths; all read via `git show <C1>:<path>`)

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md` — lines 1060–1110 (section 1083–1105 with context), plus 952–953, 1248 (`(`### Triggers T1–T3 and the re-pin rule`)` cross-reference), and the C0↔C1 unified diff.
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/fleet-kill-rate-ledger.md` — lines 160–180, 272–284, 305–340 (441 lines total).
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/service-optin-protocol.md` — lines 225–240 (286 lines total).
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/mutation-case-mado-verify.md` — lines 1–30, 150–180, 224–240 (323 lines total).
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-16/w2/RerunSweep.md` — lines 1–26, 88–105 (105 lines total).
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/plans/round-8.plan.md` — lines 60–80 (172 lines total).
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/operator-runbook.md` — lines 283–300 (adjacent cross-reference, see below).
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/reader-section.py` — read to confirm the span/sha semantics.
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py` (`sectionize`) — read to confirm heading-to-heading span and trailing-blank stripping.
- Lane git object store (`git log`, `git rev-list`, `git cat-file blob | sha256sum`) for `tools/mutate-and-run.sh`.

## Commands run (chronological, scratch `TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read07`)

1. `python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin 99c3bc88d704566197783f66b211ee0a830e0330 "### Triggers T1–T3 and the re-pin rule"`
   → `{"heading": "### Triggers T1–T3 and the re-pin rule", "cand": "99c3bc88d704566197783f66b211ee0a830e0330", "start": 1083, "end": 1105, "section_sha256": "2350210704efcc3becfbcd40a63775ad591910039744ac6d072881b3deef7801"}`
2. `git -C … show 99c3bc88…:SKILL.md | awk 'NR>=1083 && NR<=1105'` → the 23-line section (body 1083–1104).
3. Independent re-implementation of the round-18 `sectionize` over the same blob → same body, same sha `2350210704ef…` (confirms the printed `section_sha256` is the bytes' sha, not an artefact of trailing newline).
4. `git -C … show 99c3bc88…:{corpus/knowledge/fleet-kill-rate-ledger.md, corpus/knowledge/service-optin-protocol.md, corpus/knowledge/mutation-case-mado-verify.md, .ufo/waves/round-16/w2/RerunSweep.md, plans/round-8.plan.md} | awk 'NR>=a && NR<=b'` for every anchor range above.
5. `git -C … rev-list --all -- tools/mutate-and-run.sh | while read c; do git rev-parse "$c:tools/mutate-and-run.sh"; done | sort -u` → 13 distinct blobs; `git cat-file blob <b> | sha256sum | cut -c1-8` → the prefix list; joined with `git show -s --format=%cI` per blob's newest commit.
6. `git -C … log --format='%cI %h' --since=2026-10-14T00:00:00-03:00 --until=2026-10-15T00:00:00-03:00 -- tools/mutate-and-run.sh` → five commits, 13:01:03 / 13:57:18 / 15:17:26 / 16:06:31 / 18:28:23 (-03).
7. `git -C … diff -U0 59c38109bf11 99c3bc88d704566197783f66b211ee0a830e0330 -- SKILL.md` and `diff <(show C0 | sed -n '1060,1110p') <(show C1 | sed -n '1060,1110p')` → "SECTION REGION IDENTICAL".
8. `git grep -n "SCR-T6|moved=|not retained|retained" 99c3bc88…` → the sweep behind the "scratch not retained" and `moved=0 stale=0` checks.
9. Typography sweep over the section bytes (`grep -nE '[^ ]  [^ ]|\)\(|\)\)|\.[A-Za-z(]| ;|;  '` and a non-breaking/zero-width character scan) → nothing.

## Adjacent observation — NOT a finding for this section

The runbook cites **into** this section with two ranges that no longer contain the blocks they name at C1: `corpus/knowledge/operator-runbook.md:286` says "**Triggers — what to do** (`SKILL.md:1069-1090`)" and `:299` cites `SKILL.md:1083-1086` for the re-pin rule, while at C1 the triggers block is 1083–1104 (T1 1085–1088, T2 1089–1094, T3 1095–1096, re-pin 1097–1104) — 1069–1082 is the preceding ER-4/falsifiers text. Recorded here only so the L1 can route it to whichever seat reads the runbook; the bytes are in the runbook file, not in my section, so it is not counted above.

## Limits

- Cold read of committed bytes only; I did not execute `.ufo/evidence/round-54/c1|c2/measure.py`, the controls harness or any gate tool (not this item's scope), and I ran no gate suite.
- All git calls were read-only (`show`, `log`, `rev-list`, `rev-parse`, `cat-file`, `grep`, `diff`); no fixture clone was needed, so nothing under `D=$(mktemp -d)` was created.
- No tool installs: nothing was needed, and pacman transactions are paused host-wide anyway.
- `reader-section.py` wrote its temporary `measure.py` under my `TMPDIR` (`/fast/scratch/hyaku/tameshi-r54/T54W2Read07`), as the seat spec requires; nothing was written under `/tmp`.
