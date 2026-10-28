# T54W1Read07 — cold read at C0: `### Triggers T1–T3 and the re-pin rule`

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Content commit read (`cand` / C0): `59c38109bf119d0e9d4f878644a82babc937bc1e`
- Section: heading at line 1083, text = lines 1083–1104 of `SKILL.md` at C0
  (22 lines; `reader-section.py` reports `end` 1105, the line before the next
  heading, and the trailing blank at 1105 is stripped before hashing — computed
  below)
- `section_sha256`: `2350210704efcc3becfbcd40a63775ad591910039744ac6d072881b3deef7801`
- Deliverable JSON: `.ufo/waves/round-54/w1/T54W1Read07.json` (`findings: []`)

## Verdict

**No findings.** Every file:line anchor the section names resolves at C0 to the
content the clause attributes to it; the section holds no table, so it has no
table cell to be stale; and I could not establish a self-contradiction between two
sentences of the section. The checks that support this, the artifacts opened, and
the candidates I examined and deliberately did not report are below.

## Identity of the read (commands and observed output)

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
$ python3 .ufo/waves/round-54/reader-section.py <lane> \
    59c38109bf119d0e9d4f878644a82babc937bc1e "### Triggers T1–T3 and the re-pin rule"
{"heading": "### Triggers T1\u2013T3 and the re-pin rule", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e",
 "start": 1083, "end": 1105, "section_sha256": "2350210704efcc3becfbcd40a63775ad591910039744ac6d072881b3deef7801"}
```

Cross-check with the frozen round-18 sectionizer, run over the C0 bytes of
`SKILL.md` (import of `.ufo/evidence/round-18/measure.py` at C0, no
reimplementation):

```
{'start': 1083, 'end': 1105, 'heading': '### Triggers T1–T3 and the re-pin rule',
 'sha256': '2350210704efcc3becfbcd40a63775ad591910039744ac6d072881b3deef7801'}
```

Identical start/end/sha. The sectionizer's own definition (docstring of
`.ufo/evidence/round-18/measure.py`): "section text = heading line through the line
before the next heading with trailing blank (whitespace-only) lines stripped,
joined by \n, no trailing newline". Recomputed by hand from the C0 blob:

```
lines 1083..1104 joined with "\n", no trailing newline, sha256:
2350210704efcc3becfbcd40a63775ad591910039744ac6d072881b3deef7801   (22 lines)  <- matches
lines 1083..1105 (blank line 1105 kept):
067d85ff07c93bea5654ecced1a1335a6628a7a4aa85795474ce8faa66d4e906   (23 lines)  <- not the section text
```

The section bytes were read with
`git -C <lane> show 59c38109…:SKILL.md`; no working-tree read of `SKILL.md` was made.

Section facts: 22 lines (heading `1083`, blank `1084`, text `1085–1104`), 4 bullets
(T1, T2, T3, the re-pin rule), **0 table rows** and 0 `|` characters in the section,
9 file:line references
(`fleet-kill-rate-ledger.md:170-173`, `fleet-kill-rate-ledger.md:281`,
`fleet-kill-rate-ledger.md:310`, the bare `:318` continuation,
`service-optin-protocol.md:232`, `mutation-case-mado-verify.md:17-23`,
`RerunSweep.md:19-23`, `RerunSweep.md:93`, `plans/round-8.plan.md:69-74`).

## Anchor resolution, one by one

Every line number below is in the file the section names, at C0
(`git show C0:<path>`), and the quoted text is the observed line content.

1. **T3 — `§1–§4 are never edited` (`fleet-kill-rate-ledger.md:170-173`).**
   `:173` reads `row, not an edit of §1–§4.` and `:170-172` carry the embedding /
   case-count sentence about the tsukuroi and mado cases. The ledger at C0 has
   `## 1.`, `## 2.`, `## 3.`, `## 4.` headings (`:41`, `:90`, `:98`, `:132`), so
   "§1–§4" names real sections. Resolves.

2. **Re-pin rule — `:310`, ER-3.** `:310` is trigger 3 of the ER-3 block:
   `A moved substrate needs a **re-pin**, never a re-interpretation of the old table`.
   The ER-3 heading is at `:285`, so `:310, ER-3` is line 310 inside erratum ER-3.

3. **Re-pin rule — `:318`, ER-4.** `:318` is the ER-4 heading itself, whose body
   says no §1–§4 cell is edited and `a moved pin is never re-interpreted`.

4. **The old table stays, and the moved case lands at its newest revision with both
   shas and the delta, appended** (section lines 1098–1099; the sentence wraps, so I
   cite lines rather than quote across the wrap). Ledger support: `both revisions
   stay in the record` (`:310`), `old tables stand at their revisions` (`:318`), and
   `:312` — the outcome lands `as an appended row or errata block in this ledger`.
   The section's compression is faithful.

4b. **`moved=0 stale=0` is a complete outcome** (section lines 1099–1100, wrapped).
   Both halves resolve: `fleet-kill-rate-ledger.md:312` carries
   `` `moved=0` is recorded, never manufactured. `` and `:352` carries
   `` a tick that read `stale=0` would be as complete. `` (`:312` is inside ER-3,
   heading `:285`; `:352` is inside ER-4, heading `:318`).

5. **Round-8 replay receipt — `fleet-kill-rate-ledger.md:281`.** `:281` reads in
   full: `- **§5 / ER-1 supersession (embedding + tool).** … the harness at
   `cf41efaa8be5f52d…` (r7-1; 1 341 L / 61 632 B) carries **four** materialized legs
   and passes them at the exact band — `REGRESSION: PASS (cases=4 passed=4; ledger
   legs exact: killed-delta<=0 flips<=0)`, every leg `match=10/10 flips=0`
   (O: T8-2's run 2026-10-14T19:14:16Z, `mutation-case-kumitate-claims.md` §6; …)`.
   So tool `cf41efaa…`, four legs and 19:14:16Z all resolve on the cited line.
   The `rc 0` in the section's parenthetical is not on `:281`; it is on the note
   the cited line points at — `corpus/knowledge/mutation-case-kumitate-claims.md:316-317`
   reads `at 19:14:16Z, tool `cf41efaa…` → `REGRESSION: PASS (cases=4 passed=4; ledger
   legs exact: killed-delta<=0 flips<=0)`, rc 0`. The citation chain closes.

6. **T2 precedent — `RerunSweep.md:19-23`.** The file is
   `.ufo/waves/round-16/w2/RerunSweep.md` (unique basename in the C0 tree).
   `:19-20` read `Tool: worktree/tools/mutate-and-run.sh at c699c8c → sha256
   89722ddb3082abd63136d025e0dfb08dcea9ffd91d58878beb230241b61f5594`, `:22-23`
   `this re-run used the committed landing revision 89722ddb (r16, leg 7 embedded)`.
   That is exactly the clause the pointer is attached to ("under runner `89722ddb…`").
   `reproduced case 7` resolves too: `:1` is the round-gate falsification, `:3-5`
   the HOLDS verdict, `:36` the `--label js-round-gate` invocation, and commit
   `c699c8c36d6e` carries the subject `round-16: land js-round-gate case 7`.

7. **`0673d2e5…` is the later regression/selftest runner.** Verified at C0:
   `.ufo/evidence/round-16/round-gate/runner-sha256.txt:1` = `89722ddb…` for the
   c699c8c runner; `:2-4` state that `05a2247` moved the runner and that
   `runner-regression.txt` and `runner-selftest.txt` were re-run on it; `:5` gives
   `0673d2e5374b94c651238e7497cbebaffb6483348400747b08f9d27cdc8118aa`. Direct
   recomputation: `git show 05a224754db3…:tools/mutate-and-run.sh | sha256sum` =
   `0673d2e5…`, and `git log -1 --format=%ci 05a22475` = `2026-10-20 11:18:08 -0300`,
   later than `c699c8c` (`2026-10-20 10:49:37 -0300`). Both runner shas also appear
   in the round-16 receipts (`runner-regression.txt:1-2`, `runner-selftest.txt:87`,
   `runner-sha256.txt:5`). "Later" holds in both orderings (commit time and
   receipt provenance).

8. **mado re-run by SCR-T6 — `service-optin-protocol.md:232`.** `:232` (the
   "second seat" row of the mado table) reads `SCR-T6 re-ran the spec under
   `b56c6e57…`: 4/10, all ten mutant shas identical`. The section's `4/10` is on the
   line. `scratch not retained` is a disclosure, not a ledger quote, and the plan
   that records the run names the scratch as an uncommitted `/tmp` path:
   `plans/round-6-record-draft.md:204-209` — `Scribe verification (this draft,
   TAMESHI-SCR-T6, re-run 2026-10-14; scratch` / `/tmp/w6-scr-t6-*): … independent
   mado re-sweep against the pinned` / `d7edaab4` bytes … `→ 4/10, verdicts and all
   ten mutant shas identical to T6-1's table`. A `git grep` for `w6-scr-t6` / `scr-t6`
   at C0 returns only that draft's path strings (plus traces and wave reports quoting
   it); no retained receipt exists. The disclosure is consistent with the record, and
   the round-52 audit adjudicated it the same way.

9. **mado note keeps it U — `mutation-case-mado-verify.md:17-23`.** `:17-21` are
   the "Incident I1" paragraph ending `Re-pin at 17:46:15Z: sha256 b56c6e57…2bcb,
   46850 B, mtime 14:46:08 -0300`; `:22-23` read `**Every number in this note is tied
   to `597e1419…`**; whether the new revision reproduces this table is **U** (§7)`.
   The U reading resolves on the cited lines.

10. **`plans/round-8.plan.md:69-74` for the two working-tree writes.** `:69` carries
    `4dc69ef9… (15:27:40, 1247 L / 56518 B: header`, `:72-73` carry
    `→ e3f838d4… (15:28:38,` / `61305 B: the headline count parameterized, :965)`.
    Both timestamps in the section's bracket resolve exactly.

11. **T1 instances, round 8 (2026-10-14).** ER-3's executed pin read
    (`fleet-kill-rate-ledger.md:297-304`, run `2026-10-14T19:21:00Z`) records
    `| 3 | tsukuroi-census | 084951be… | bba6cdf6… (1 472 L) | bba6cdf6… | clean | stale |`
    and
    `| 4 | mado-verify | d7edaab4… | dc864c6a… (2 186 L) | 90d50cdd… | dirty | stale + drift |`.
    The section's `084951be… → bba6cdf6…` and `d7edaab4… → 90d50cdd…` are the
    recorded pin and HEAD-blob cells verbatim; the 6/10 (60 %) and 4/10 (40 %) rates
    are §4's rate sequence (`:279`). The third mado link `7da4ec50…` is confirmed
    twice: ER-3's row 4 live cell (`:329`, `` `7da4ec50…` (2 887 L / 131 612 B) ``) and
    ER-3's chain paragraph (`:338`): `d7edaab4` (`eead56b2`) → `c4c1afb7` (`c8f6667`,
    round 6, 18:17:26Z) → `90d50cdd` (`0c20a76`, round 7, 19:06:31Z) → `7da4ec50`
    (`12c8f08`, round-8 commit). Read-only on the sibling lane:
    `git -C mado-shokunin show -s --format='%h %ci' 12c8f08` →
    `12c8f08a 2026-10-14 16:55:09 -0300` (same day as the round-8 tick), and
    `git -C mado-shokunin show 12c8f08:tools/mado-verify.sh | sha256sum` →
    `7da4ec5013583c91942538986b05e7243b3edeb8e3dd37b54f6b65a9225f2f4f`. All three
    chains resolve.

12. **The round-52 bracket's committed chain.** Recomputed from git history and
    per-commit blob sha256 of `tools/mutate-and-run.sh`:

    | commit | commit time (`git log -1 --format=%ci`) | blob sha256 (first 8) |
    |---|---|---|
    | `53e74a890c70…` | 2026-10-14 13:01:03 -0300 | `d8abee52` |
    | `b58b26fbeba8…` | 2026-10-14 13:57:18 -0300 | `597e1419` |
    | `44947154c237…` | 2026-10-14 15:17:26 -0300 | `b56c6e57` |
    | `9f1d3c339a70…` | 2026-10-14 16:06:31 -0300 | `cf41efaa` |
    | `606716f703f7…` | 2026-10-14 18:28:23 -0300 | `75ed934d` |

    Four moves across five commits, and the times 13:01 / 13:57 / 15:17 / 16:06 /
    18:28 are exact. No 2026-10-14 commit on that path has blob `4dc69ef9` or
    `e3f838d4` — consistent with the bracket's "working-tree writes, not commits".
    `RerunSweep.md:93` reads `durations, and the tool sha (75ed934d → 89722ddb, the
    commit-expected r16 tool —`, so the `75ed934d` sha in that parenthetical resolves
    at the cited line.

13. **Provenance tags.** `(corrected round 18)` — located: `.ufo/waves/round-18/w2/CR21.md`
    W1 corrects this section's T2 precedent sentence (round gate re-read; the ledger's
    entry for this heading records `wrong_expectations: 1` at `01d586dd…` and `0` at
    `4acdeac9…`, the re-read). `(corrected round 27, seat Read15)` —
    `.ufo/waves/round-27/w1/Read15.md:15-22` is the F1 finding that the RerunSweep
    runner was `89722ddb`, not `0673d2e5`, exactly the correction the section carries.
    `seat ReRead07` — `.ufo/waves/round-27/residual/ReRead07.md` is that seat's read
    of this heading (page sha `fce54977…`), and its recommended wording is what the
    section now uses for the SCR-T6 re-run and the 19:14:16Z receipt.

## Self-contradiction sweep

I walked the four bullets pairwise and looked for pairs that cannot both be true.
T1 (lines 1085–1086) forbids `never an edit of the recorded table`; T3 (1095–1096)
says a re-run lands as an appended row and §1–§4 are never edited; the re-pin rule
(1097–1100) says `The old table stays` and the moved case lands appended. All three
prescribe the same append-only path; none offers an edit path. T2's quote `record both pins`
(line 1090) matches the re-pin rule's `with both shas and the delta, appended.`
(line 1099) — record the old and the new pin. The `moved=0 stale=0`
completeness clause (lines 1099–1100) does not conflict with T1's option to record a
STALE cell: one describes a reading with nothing moved, the other a case that did
read stale. The receipt's closing clause (line 1104,
`their own pinned blobs regardless of the live drift above`) is a claim about
pin-vs-live replay, not a claim that the drift did not happen, and the receipt's four
legs are stated as replayed `at their recorded pins` (`fleet-kill-rate-ledger.md:281`).
No pair is contradictory.

## Opened artifacts

All read at C0 with `git show`; sha256 measured on the C0 blob unless noted.

| artifact | what I checked |
|---|---|
| `SKILL.md` @ C0, `:1083-1104` (`:1105` blank) | section bytes, anchor list, table absence |
| `corpus/knowledge/fleet-kill-rate-ledger.md` (`d345ae3e…`, 441 L) | `:41,90,98,132` (§ headings), `:170-173`, `:279`, `:281`, `:287-291` (pin-read command set), `:297-304` (ER-3 rows), `:310`, `:312`, `:318`, `:329`, `:338`, `:352` |
| `corpus/knowledge/service-optin-protocol.md` (`84d0c154…`) | `:232` (SCR-T6 re-run row) |
| `corpus/knowledge/mutation-case-mado-verify.md` (`f2d53d49…`) | `:14-26` (I1, re-pin, the U sentence) |
| `.ufo/waves/round-16/w2/RerunSweep.md` (`8b03036e…`) | `:1-30` (setup, runner sha, case 7 target), `:88-96` (deltas, `:93`) |
| `plans/round-8.plan.md` (`7e53c9d8…`) | `:66-76` (working-tree writes and their timestamps) |
| `plans/round-6-record-draft.md` | `:202-210` (the SCR-T6 re-run, its `/tmp` scratch and the 4/10 table) |
| `.ufo/evidence/round-16/round-gate/runner-sha256.txt`, `runner-regression.txt`, `runner-selftest.txt` | `89722ddb` at `:1`, correction at `:2-4`, `0673d2e5` at `:5`; receipts carrying `0673d2e5` |
| `corpus/knowledge/mutation-case-kumitate-claims.md` | `:316-317` (19:14:16Z, `cf41efaa`, `rc 0`) |
| `.ufo/waves/round-18/w2/CR21.md`; `.ufo/evidence/round-18/coldread/ledger.json` | round-18 correction of this heading; `wrong_expectations` 1 → 0 |
| `.ufo/waves/round-27/w1/Read15.md`; `.ufo/waves/round-27/residual/ReRead07.md` | the two seat citations the section carries |
| `.ufo/waves/round-53/w1/T53W1Read28.md` | round 53's read of this same heading (0 findings) — reconciliation only |
| `.ufo/evidence/round-21/coldread/ledger.json` | 11 entries for this heading (last: `executed-ok`, `wrong_expectations: 0`) |
| `git log --all -- tools/mutate-and-run.sh` + per-commit `sha256sum`; `mado-shokunin` read-only `show` | the 2026-10-14 commit/blob chain, the 2026-10-20 runner order, `12c8f08`/`7da4ec50` |

## Examined and deliberately not reported (with the reason)

These are the candidates a reader could raise; none is a rule whose anchor fails, a
stale table cell, or a contradiction I can defend, so none is in the JSON.

- **Undated `(both have moved again since; re-read, never carry)` (T1).** The clause
  forbids carrying the observation, so it is not a fact a later reader must resolve;
  the claim holds as of 2026-10-22 (round-27 ReRead07: tsukuroi `d17d32a3`, mado
  `050efc72`). Undated, not false. Round-27 recorded it as an optional minor gap.
- **T1's mado arrow names the HEAD blob (`90d50cdd…`) while the round-8 worktree was
  dirty (`dc864c6a…`).** The ledger row labels the columns (`live` vs `HEAD blob`,
  `:297`) and the page's own preceding bullet (`SKILL.md:1069-1074`) states the
  dirty-worktree drift explicitly. The arrow is a committed-blob chain and is not
  false; disclosing the dirt inside T1 would duplicate the paragraph above it.
- **`RerunSweep.md:93` and the `r10-2` label.** The cited line resolves the
  `75ed934d` sha the parenthetical names; the `r10-2` label is at `:21` and the 18:28
  time is commit `606716f7`'s own timestamp (git log). A cold reader following `:93`
  gets the sha; the other two tokens are independently verifiable. No wrong pointer.
- **`moved four times in one day` vs the bracket's four committed moves.** The two
  four-move chains name different windows (four states 597→…→cf; four commits
  d8→…→75); the sentence says the harness moved four times, not that it moved only
  four times, and both counts are true. The union of the two chains is seven blobs /
  six moves, which is an understatement, not a contradiction. Not reported.
- **Bare basenames for the five corpus/wave files.** Other sections use full
  `corpus/knowledge/…` paths; this section uses the base name. Each basename is
  unique at C0 for the wave files, and `git ls-tree -r` at C0 shows exactly three
  copies of the ledger: the `corpus/knowledge/` one the section means, plus two dated
  copies under `.ufo/` (`.ufo/evidence/round-53/assimilation/validate/…` and
  `.ufo/waves/round-18/staged/…`). Resolution costs one `git ls-files`, not an
  ambiguity in content. Not a failing anchor.
- **`(corrected round 18)` carries no pointer.** I located the correction anyway
  (round-18 CR21 W1 on the T2 precedent). The label names a real, findable event, so
  it is not a dangling citation; adding a pointer would be an improvement, not a fix
  for a false statement.

## Bounds and disclosures

- Wrote only `.ufo/waves/round-54/w1/T54W1Read07.json` and
  `.ufo/waves/round-54/w1/T54W1Read07.md`. No lane file, no counter, contract,
  freeze, ledger or wave-spec write. No `git add/commit/push/fetch/reset`; no `jj`;
  no fixture repo was created (nothing was mutated, so no fixture was needed).
- Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W1Read07/` was created (`mkdir -p`,
  `TMPDIR` pointed at its `tmp/`) and is removed before this seat yields; one
  helper file `/tmp/r18m.py` (the C0 copy of the frozen round-18 sectionizer) was
  removed after the sha cross-check. No other scratch is left behind.
- Prior-wave reports: I opened `.ufo/waves/round-27/w1/Read15.md` and
  `.ufo/waves/round-27/residual/ReRead07.md` because the section cites those seats
  (anchor verification), `.ufo/waves/round-52/w2/T52W2Fix05.md`/`.json` to test my
  own reading of the round-52 bracket, and — after my own checks had run —
  `.ufo/waves/round-53/w1/T53W1Read28.md`, round 53's read of this same heading
  (which also returned 0 findings), as a reconciliation check. No claim above rests
  on them: every check is against C0 bytes or `git log`, and the prior documents
  agree with the checks rather than supply them.
- Runs: read-only git plumbing (`show`, `log`, `cat-file -e`, `grep`, `ls-tree`,
  `rev-parse`) and `sha256sum`. I did not execute the harness, a sweep or a
  regression run.
- Census (conformance, read-only): `scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin tameshi` → exit 0 (W-codes only);
  `scripts/sources-census.sh census --root … tameshi` → `tameshi rows 139`
  (`status.mined 112`, `queued 21`, `rejected 6`; `FLEET.invalid 0`,
  `FLEET.missing 0`).
- Tooling: nothing installed or upgraded (host pacman transactions are paused; no
  `uv`/`npm`/binary install was needed).
