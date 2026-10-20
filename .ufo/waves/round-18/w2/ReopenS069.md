# Reopen S069 — Linux man-pages: setsid(2) (round 18, wave 2)

Seat: `TameshiR18.ReopenS069` (leaf; no dispatch). Lane:
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Read rev: `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`.

**Verdict: holds.** The quote is verbatim at the stated anchor, 18 words; the
`teaches` cell is page-grounded (its one non-page claim is explicitly flagged
`[INFERENCE]`); `docs`/`A` fits the frozen contract; the single `used-by` path
exists at the read rev and cites S069. Two non-blocking precision notes (G1, G2).

## Inputs

| input | sha256 | anchor used |
|---|---|---|
| `corpus/SOURCES.md` @ read rev | `1d4b5910d2ef3e4acbf09a0dfaab61f5ba0e979fb8bc1c99d7241eee5d274e37` | S069 row = line 78 (72 rows total) |
| `.ufo/waves/round-18/staged/lesson-round-18-gate.md` @ read rev | `a4f94cd79c08564aad7e3fb59d74235a9450a39dcfae508af29ddd2fbfd9a6d8` | S069 quote row = line 21; mapping = lines 51–53; wording note = lines 68–69; totals = line 88; checks = lines 92–93 |
| `corpus/knowledge/guard-kill-closure.md` @ read rev | `9312bdebd4e93d427ea32d3db8652f95530237477b49ffecffdf4e4ac49991fb` | S069 citations = lines 1 and 71 |
| `https://man7.org/linux/man-pages/man2/setsid.2.html` | `52cbc1904742df69556104f71d3279f93581756579881c85cee8e37be37c7f30`, 11555 B | HTTP 200, fetched 2026-10-20 |
| `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` (fleet root, outside lane) | `6c674a2281afb75b2de11790ebfe34fdcf7ddde61a6734d2eca302f023966119` | kind l.24–25; tier l.26–31; anchor l.32–33; teaches l.34; status l.36; recheck l.38; used-by l.40; rule 1 l.45–47 |
| `.ufo/waves/round-18/sources/S070-B06SrcSetsid.md` (auxiliary: the draft this row came from) | `7e477032f6727e92fc6a3f9a44a8fae207575d674435b544d9e752b1b7636cac` | §Duplicate sweep, §Registry row, §Gate |

Live-tree parity: `sha256sum` of the three lane inputs equals the read-rev
values above, and `git status --porcelain` on them printed nothing (exit 0).
The contract is **not** in the lane repo: `git show <rev>:SOURCES-CONTRACT-v1.md`
→ exit 128; it lives at the fleet path above, as earlier reopen seats recorded.

## 1. Quote gate — PASS

Lesson line 21, verbatim:

```
| S069 | https://man7.org/linux/man-pages/man2/setsid.2.html | 2026-10-20 | "The calling process will be the only process in the new process group and in the new session." (§DESCRIPTION ¶2) |
```

- **Verbatim.** Tag-stripped, whitespace-normalized page text contains the
  quote `occurrences: 1`, `exact_in_page: True`. Raw HTML has the two-line break
  after "process" (`...in the new process\n       group...`); normalizing to one
  space reproduces the quote exactly. No non-ASCII characters in the quote.
- **Word count.** `printf '%s\n' "$Q" | wc -w` → `18` (exit 0). 18 ≤ 25.
- **Anchor.** Paragraph enumeration of the stripped DESCRIPTION block:
  ¶1 "setsid() creates a new session if the calling process is not a process
  group leader. …"; ¶2 the quoted sentence; ¶3 "Initially, the new session has no
  controlling terminal. …". The stated `§DESCRIPTION ¶2` is correct.
- **Revision.** COLOPHON text: `Linux man-pages 6.19 2026-06-05`. The row's
  "man-pages 6.19 (footer date 2026-06-05)" is exact. The page also shows
  "HTML rendering created 2026-09-09" — not claimed by the row, so no conflict.
- **Stability.** The draft Gate recorded the same HTML sha256 `52cbc190…` and
  the same 18-word count on 2026-10-20; today's fetch is byte-identical, so the
  quote has not drifted between the opening and this re-open.

## 2. `teaches` cell vs the page — PASS (no overstatement found)

Row cell (field 8, line 78):

> the caller becomes the only process in a new process group and a new session,
> distinct from its old group; a group-directed signal sent to the old group does
> not reach it [INFERENCE: follows from the distinct group ID; killpg is not
> named on this page]; setsid fails with EPERM for a process group leader, so the
> escaping process must fork and let the child call setsid

| # | clause | page evidence | verdict |
|---|---|---|---|
| 1 | caller becomes the only process in a new process group and a new session, distinct from its old group | ¶2 verbatim: "The calling process will be the only process in the new process group and in the new session." ¶1: new session, session ID = PID, new process group with PGID = PID | holds. "distinct from its old group" is an entailment of "new process group", not a page sentence (see G2) |
| 2 | a group-directed signal sent to the old group does not reach it, flagged `[INFERENCE: … killpg is not named on this page]` | `killpg` → 0 hits; `kill(` → 0 hits. The page's only signal-delivery text is the controlling-terminal SIGHUP rule in §NOTES; the third `signal` hit is the SEE ALSO entry `signal-safety(7)` | holds. The claim is correctly marked as inference; the page states no group-signal delivery rule, and nothing on it contradicts the inference |
| 3 | setsid fails with EPERM for a process group leader, so the escaping process must fork and let the child call setsid | §ERRORS: "EPERM The process group ID of any process equals the PID of the calling process. Thus, in particular, setsid() fails if the calling process is already a process group leader." §NOTES: "In order to be sure that setsid() will succeed, call fork(2) and have the parent _exit(3), while the child (which by definition can't be a process group leader) calls setsid()." | holds; see G1 on "must" |

The page's only signal sentences are in §NOTES: "If a session has a controlling
terminal, and the CLOCAL flag for that terminal is not set, and a terminal
hangup occurs, then the session leader is sent a SIGHUP signal. If a process that
is a session leader terminates, then a SIGHUP signal is sent to each process in
the foreground process group of the controlling terminal." Those concern the
session leader / foreground group, not a signal sent to the old process group;
they neither support nor contradict clause 2. (The third `signal` occurrence on
the page is `signal-safety(7)` in SEE ALSO.)

No clause asserts a second, stronger claim than the page carries. The one clause
that the page does not state (signal non-delivery) carries the `[INFERENCE]`
marker and names why (`killpg` absent).

## 3. Tier / kind fit — PASS

Contract (`SOURCES-CONTRACT-v1.md`, sha `6c674a22…`):

- **kind `docs`** — the enum is `spec · docs · paper · code · tool · dataset ·
  talk · book · community · own-work` (l.24–25). A manual page is documentation;
  `docs` is in-enum and accurate.
- **tier `A`** — "primary or authoritative for that scope (spec, official docs,
  source code, original paper, maintainer statement, the lane's own re-runnable
  gate output)" (l.26–31). The row scopes the tier to "Linux setsid(2) session
  and process-group semantics"; the Linux man-pages project page is the
  authoritative rendering of that interface. A fits; B would under-tier it, C
  would be wrong, and `community` is not involved.
- **anchor** (l.32–33: exact section plus revision) — `§DESCRIPTION ¶2 and
  §ERRORS EPERM @ man-pages 6.19 (footer date 2026-06-05), fetched 2026-10-20`
  names the sections, the release, the footer date and the access date.
- **scope** — scoped, not global: "for a caller that leaves its group".
- **status `mined`** (l.36: cited by ≥1 path in `used-by`) — satisfied (§4).
- **opened / recheck** — `2026-10-20` is the access date; `180d` is an allowed
  cadence (l.38), consistent with the neighbouring man-page rows S067/S068.

No duplicate row: `grep -iE 'setsid|setpgid'` over `corpus/SOURCES.md` returns
only line 78 and the line-207 id-allocation footer note. The draft's duplicate
sweep (`S070-B06SrcSetsid.md:7-8`) reached the same result.

## 4. `used-by` path — PASS

`corpus/knowledge/guard-kill-closure.md` exists at the read rev
(`git cat-file -e 01d586d…:corpus/knowledge/guard-kill-closure.md` → exit 0).
It cites S069 in two places:

- `:1` (source front matter): `S069 — setsid(2) §DESCRIPTION ¶2 and §ERRORS
  EPERM, https://man7.org/linux/man-pages/man2/setsid.2.html`.
- `:71` (§4 "Process escape: setsid and setpgid leave the group"), verbatim:

  ```
  Fact. `setsid()` makes the caller the only process in a new process group and a new session [src: S069, quote "The calling process will be the only process in the new process group and in the new session."]. A group-directed signal to the old group therefore does not reach it. That consequence is inference from the new group ID; `killpg` is not named on the man page [src: S069, Gate note]. `setsid` fails with EPERM for a process group leader, so an escaping process must fork first [src: S069, §ERRORS].
  ```

The quoted sentence at `:71` is byte-identical to the Gate quote; the paragraph
also reproduces the row's `[INFERENCE]` scoping and its EPERM clause, so the
citation is not a bare ID mention.

## 5. Row shape and registry census — PASS

- S069 split on `|`: `NF=13` (11 cells; contract census expects NF=13).
- Read-rev/staged `corpus/SOURCES.md` (identical shas): `rows=72`,
  `malformed=0`, tier `A=63 B=7 C=2`, status `mined=44 queued=23 rejected=5`,
  duplicate ids none, enum violations none.
- Base `183f87b` (the lesson's comparison base): `rows=62`, `malformed=0`,
  `mined=35 queued=24 rejected=3`.
- Lesson totals (`lesson-round-18-gate.md:88`): "rows 62 → 72. Status `mined`
  35 → 44, `queued` 24 → 23, `rejected` 3 → 5" — all four deltas reproduce
  exactly. Line 92–93's `rows=72 bad=0` / base `rows=62` also reproduces.
- Appended rows occupy lines 74–83; S069 is line 78, as the lesson's mapping
  (lines 45–46) implies.

## 6. Minor, non-blocking notes

**G1 — `must fork` is stronger than the page's frame, and §NOTES is not in the
anchor.** The row anchors `§DESCRIPTION ¶2 and §ERRORS EPERM`, but the fork
recipe is stated in §NOTES ("In order to be sure that setsid() will succeed,
call fork(2) and have the parent _exit(3), while the child … calls setsid()").
The row renders this as "must fork". That necessity is exact for a process group
leader (the row's stated antecedent: EPERM otherwise); for a non-leader the
page's own note says the child "by definition can't be a process group leader",
so a direct `setsid()` can succeed. Adding `§NOTES` to the anchor, or reading
"must fork" as "must fork to be sure", would remove the only sharp edge. Not
blocking: the derivation follows from §ERRORS and the page's §NOTES corroborates
the recipe.

**G2 — "distinct from its old group" is an unflagged entailment.** It is not a
page sentence; it follows from "new process group" (new PGID = caller PID, which
cannot equal a live group leader's PGID because that would make the caller that
leader and setsid would fail with EPERM). No operational risk; noted only for
calibration.

**O1 — not a contract gap.** The staged Gate table carries one quote per row
(the ¶2 sentence); the EPERM/fork half is anchored (§ERRORS) but not quoted
there. Rule 1 (l.45–47) asks for "a ≤25-word quote with its location grounding
`teaches`" (singular), so this is compliant. The draft Gate retains a second,
12-word §ERRORS quote ("setsid() fails if the calling process is already a
process group leader.") if the L1 wants it in the lesson.

## 7. Commands executed

All exited 0 unless noted.

Method note: every lane read used `git show <rev>:<path>`, `git cat-file`,
`git grep` or `git status` (read-only); no clone, no lane write, no `GIT_*`
override. Scratch lived at `/tmp/setsid2.html` (fetched page),
`/tmp/staged-sources.md` and `/tmp/base-sources.md` (census inputs) — outside
the lane; written directly under `/tmp` rather than a `mktemp -d` (deviation
noted, no lane/sibling file touched). The only lane write is this report.

| command | key output |
|---|---|
| `git show <rev>:corpus/SOURCES.md \| grep -n "S069"` | line 78 (row); line 207 (id-allocation footer) |
| `git show <rev>:.ufo/waves/round-18/staged/lesson-round-18-gate.md \| grep -n "S069"` | lines 21, 49, 52, 53, 68 |
| `curl -sS -L --max-time 60 https://man7.org/linux/man-pages/man2/setsid.2.html -o /tmp/setsid2.html` | exit 0; 11555 B |
| `curl -sS -o /dev/null -w '%{http_code} %{size_download}' …` | `http=200 size=11555` |
| `sha256sum /tmp/setsid2.html` | `52cbc1904742df69556104f71d3279f93581756579881c85cee8e37be37c7f30` |
| `printf '%s\n' "$Q" \| wc -w` | `18` |
| Python verbatim check over tag-stripped page | `occurrences: 1`, `exact_in_page: True`; `q == page_para` → `True` |
| Python DESCRIPTION paragraph split | ¶2 = the quote; ¶1 and ¶3 as quoted in §2 |
| Python COLOPHON check | `man-pages 6.19` present; `2026-06-05` present |
| Python signal sweep | `killpg` 0; `kill(` 0; `signal` 3 (two SIGHUP sentences in §NOTES, one SEE ALSO entry `signal-safety(7)`) |
| `git cat-file -e <rev>:corpus/knowledge/guard-kill-closure.md` | exit 0 |
| `git show <rev>:corpus/knowledge/guard-kill-closure.md \| awk 'index($0,"S069")'` | lines 1 and 71 |
| `awk -F'\|'` field split on line 78 | `NF=13`; kind `docs`; tier `A`; status `mined`; used-by `corpus/knowledge/guard-kill-closure.md` |
| contract census on read-rev/staged file | `rows=72`, `malformed=0`, `A=63 B=7 C=2`, `mined=44 queued=23 rejected=5` |
| contract census on base `183f87b` | `rows=62`, `malformed=0`, `mined=35 queued=24 rejected=3` |
| `grep -iE 'setsid\|setpgid' corpus/SOURCES.md` | lines 78 and 207 only |
| `sha256sum` lane inputs (live tree) vs read-rev values | all equal |
| `git status --porcelain -- <three lane inputs>` | empty, exit 0 |

## Verdict

**holds** — at `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`, S069's Gate quote is
verbatim, 18/25 words, at `§DESCRIPTION ¶2` of man-pages 6.19; the `teaches`
cell is page-grounded with its one non-page claim explicitly marked
`[INFERENCE]`; `docs`/`A` is the contract-correct kind/tier; and
`corpus/knowledge/guard-kill-closure.md` exists and cites S069 at `:1` and `:71`.
Two wording-precision notes (G1, G2), neither blocking.

**holds** — S069 holds at `01d586d`; G1/G2 are non-blocking wording notes.
