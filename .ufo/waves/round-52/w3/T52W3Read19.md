# T52W3Read19 — cold-read: `### What stays open — named, never closed by prose`

CAND1 `7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135`, SKILL.md. Section = lines 1449–1463
(heading `:1449`; next heading of level 1–3 is `## Promotion-evidence calibration — fleet round-1`
at `:1464`; line 1463 is the blank separator line, included in the section span). The
section closes the round-8…11 cadence arc (`## The re-sweep cadence…` `:1010`, `## The
cadence's first scheduled tick…` `:1155`, `## The operator's runbook…` `:1272`, `## Final
pointers…` `:1365`). All checks below were run against CAND1 bytes via
`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:<path>`.

## Findings

None. No statement in this section failed at CAND1: every pointer lands on the bytes it
names, every recorded `[U]` is still open at its home, and the dated claims are accurate
for their writes. `findings` is `[]` in the JSON.

## Holds

11 pointers/statements checked, all hold:

1. **"The interval — the operator's `[U]` (above)"** — SKILL.md:1441 (in the four-readers
   entry whose seat is "The operator", `:1437-1440`): "No lane declares a clock interval —
   the ticks so far are boundary-bound, and the interval is that seat's `[U]`."
   Corroborated by `corpus/knowledge/closeout-r11.md:210` ("The interval is `[U]` — set and
   kept by the seat the handoff names"). Command: `git -C … show CAND1:SKILL.md | sed -n '1441p'`.
2. **"round 8's own `[U]` (`:1017-1019`)"** — SKILL.md:1017-1019 carries exactly that
   unknown ("…whether any fleet driver would ever invoke the command with no lane acting
   stays [U].") inside the round-8 section (`:1010`). Command: `git -C … show CAND1:SKILL.md | sed -n '1010,1019p'`.
3. **"`…unchanged`"** — the sentence is byte-identical to what round 8 landed: at `c611d5d`
   (commit "probation round 8") the same lines read identically. Commands:
   `git -C … show c611d5d:SKILL.md | sed -n '1018,1019p'` vs
   `git -C … show CAND1:SKILL.md | sed -n '1018,1019p'`.
4. **"Whether the operator adopts the schedule — `[U]`, recorded as such"** — recorded as
   `[U]`: `plans/round-11.plan.md:288` ("the operator adopts — `[U]`"),
   `corpus/knowledge/closeout-r11.md:347` ("the interval `[U]`, adoption `[U]`") and
   `closeout-r11.md:408-409` ("[U] the standing future itself: … whether the operator
   adopts the schedule/runbook"). Commands: `git -C … show CAND1:plans/round-11.plan.md | sed -n '288p'`;
   `git -C … show CAND1:corpus/knowledge/closeout-r11.md | sed -n '347p;408,409p'`.
5. **"The two successor rows (T1 fired again at this read)"** — at the round-11 read both
   stale cells are committed HEAD blobs, "so T1 fired" (SKILL.md:1414-1415); T1 had fired
   at the earlier ticks too (SKILL.md:1232; closeout-r11.md §2.5 tick series, ticks 2–4 all
   "2 stale"), so "again" is accurate. Commands: `git -C … show CAND1:SKILL.md | sed -n '1414,1419p'`.
6. **"successor rows … open at this write"** — SKILL.md:1418-1419 states it for the same
   write ("successor rows land appended in the ledger (`:1230-1244`) — open at this write").
7. **"the ledger row for the six-leg registry (`:1359-1363`)"** — SKILL.md:1359-1363 is the
   "Named debt, not smoothed" bullet recording that "a ledger row recording the six-leg
   (ten-leg since round 51) registry is the ledger owner's follow-on" — i.e. open. The
   range is exact both at CAND1 and at the round-11 write commit `284ab0f` (same lines).
   Command: `git -C … show CAND1:SKILL.md | sed -n '1359,1363p'`.
8. **"the ledger's U-list"** — `corpus/knowledge/fleet-kill-rate-ledger.md:216` `## 8. Unknowns`,
   items U1–U9 at `:218-240`. Command: `git -C … show CAND1:corpus/knowledge/fleet-kill-rate-ledger.md | sed -n '216,240p'`.
9. **"the protocol's U1–U6"** — `corpus/knowledge/service-optin-protocol.md:257` `## 7. Unknowns`,
   items U1–U6 at `:259-274`. Command: `git -C … show CAND1:corpus/knowledge/service-optin-protocol.md | sed -n '257,274p'`.
10. **"`service-limits.md` §5"** — `corpus/knowledge/service-limits.md:218` `## 5. Unknowns`
    (U1–U5 plus a "Carried" line, `:220-239`). Command: `git -C … show CAND1:corpus/knowledge/service-limits.md | sed -n '218,240p'`.
11. **"Append-only to the last line: nothing above this section was edited by this write"** —
    the round-11 write is commit `284ab0f`; its SKILL.md diff is a single hunk
    `@@ -1360,4 +1360,103 @@`, a pure EOF append (the old file ended at line 1362 with
    "\ No newline at end of file"; the append re-terminated that last line and added the
    round-11 block). Nothing above the append point was touched. Commands:
    `git -C … diff 284ab0f^ 284ab0f -- SKILL.md | grep '^@@'`;
    `git -C … show 284ab0f:SKILL.md | wc -l` (=1461; section at `:1449`).

Section integrity: heading `:1449`; no level-1-3 heading between it and `:1464`; the dated
clauses ("at this write", "at this read", "by this write") all scope to the round-11 write,
which the `284ab0f` diff confirms. Section sha256 (lines 1449–1463 joined by `\n`, i.e. the
text ends `…trusts.\n`): `50bd6cc09773a2850a3fd4828d64a2659df29d7f59925062e1b7ebef2139a211`.
(Alternative reading that also keeps the file's own newline terminating line 1463 —
`sed -n '1449,1463p'` output verbatim — hashes to
`3b83c572096413bf13347a7391a655134fd276065bd4b86172bd10607baaf53f`; the JSON carries the
lines-joined value.)

Tooling: no installs this seat (read-only git + coreutils only).

## Summary

- Cold-read SKILL.md:1449-1463 at CAND1; 6 statements, every pointer opened at CAND1 bytes.
- 0 findings: `:1017-1019`, `:1359-1363`, `:1441` all land exactly; "unchanged" verified against round 8's `c611d5d`.
- Adoption-of-schedule `[U]` is recorded as such (plan `:288`, closeout-r11 `:347,:408-409`).
- Unknowns' homes all exist: ledger U-list (U1-U9), protocol U1-U6, service-limits.md §5.
- Append-only claim verified against the round-11 write commit `284ab0f`: single-hunk pure EOF append.
- section_sha256 (lines 1449-1463, `\n`-joined) = `50bd6cc09773a2850a3fd4828d64a2659df29d7f59925062e1b7ebef2139a211`.
- holds_checked = 11; findings = [].
