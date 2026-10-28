# T55W2RevCorrections — the corrections section against base and against the receipts

seat `T55W2RevCorrections` (reviewer, wave 2) — lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
object under attack: `SCORECARD.md` `## Round 55 - round-54 record corrections` **at C0**
`9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` (lines 2621-2702), the ten rows ER-R54-1..10
base `0a2010acd1e92e4e332774050825e21bcfc7e079`; round-54 freeze `077d431e69965fa4673cd006ab64f6fc387f9e15`
read-only: no lane production file, no frozen file, no wave spec was written. This report plus
`T55W2RevCorrections-receipts/` (five files) are the only writes, both under `.ufo/waves/round-55/w2/`.

## Verdict

**10/10 rows agree. No blocking finding for C1.** Every quoted old value exists in the artifact the row
names, at base, with the meaning the row attributes to it; every corrected value is what the named
receipt prints (or what the derivation the row describes yields); every named receipt exists at C0 and
carries that fact. *Five non-blocking findings* follow — one medium (a false preamble claim about
uniqueness) and four traceability gaps — plus one reading hazard.

Method: two independent derivations of the same ten facts, then a cross-check.
1. the lane's frozen C1 counter at C0 (`.ufo/evidence/round-55/c1/measure.py`, byte-frozen) —
   `premise=10/10 stale=0 classes_corrected=10/10 total=0 C1_R55_PASS=true`
   (`T55W2RevCorrections-receipts/frozen-c1-counter-at-c0.out`);
2. my own ten-row re-derivation (`T55W2RevCorrections-receipts/verify-ten-rows.py`, output
   `.../verify-ten-rows.out`), which shares no code with the counter and re-derives ER-R54-5's counts,
   ER-R54-9's registry numbers, ER-R54-7's section-sha negatives, and ER-R54-8's host facts from the
   artifacts themselves.
Both agree on all ten, and they agree with each other's *values*, not merely with the section's prose.

## The ten rows

Every check below is in `verify-ten-rows.py`; the command that reproduces the whole matrix is

```
python3 .ufo/waves/round-55/w2/T55W2RevCorrections-receipts/verify-ten-rows.py   # exit 0 = 10/10 agree
```

`R` below = `.ufo/evidence/round-54/` at C0; `REP` = `/home/vgpnk/Projects/shokunin` `fcb8d8db:.ufo/reports/round-54/tameshi.md`
(the fleet commit that last wrote the round-54 report; working tree clean on that path).

| # | old text — where it actually is at base | corrected value — the named receipt prints | old@base / value@receipt / pointer | verdict |
|---|---|---|---|---|
| ER-R54-1 | `CTL_POS_c1 true` — base `SCORECARD.md:2583`; `rekeyed=7/7` on its positive control — base `corpus/QUALITY.md:1590`; `proven live by the positive control (CTL_POS_c1, which prints rekeyed=7/7)` — base `corpus/lessons/round-54.md:101` | `Rcontrol/controls-b.stdout`: `CTL CTL_POS_c1 … rekeyed=3/7 … C1_R54_PASS=false`, `CTL_MISMATCH CTL_POS_c1 expected=true actual=false`, `CONTROLS_B: 2/3 as pre-registered`, exit 1; control cloned `rev=077d431e6996` | ok / ok / ok | **agree** |
| ER-R54-2 | `7883e0e5` "is the freeze pointer the deciding run uses" — base `SCORECARD.md:2564-2567`; "freeze `fe70474d` (amendments 1-5)" — base `SCORECARD.md:2608`, inside `### Round 54 — measured close`; "the freeze pointer `097985c1`" — `REP:155` | `Rafter/frozen.stdout`: `FROZEN_UNCHANGED=1 freeze=077d431e69965fa4673cd006ab64f6fc387f9e15 rev=c2108100…`; `Rfreeze.json` has 5 amendments | ok / ok / ok | **agree** |
| ER-R54-3 | `total=14` — base `SCORECARD.md:2584` (C2 claim row), whose own parenthetical claimed the receipt carried 14 | `Rbefore/c2.stdout` last line: `… sources=0 total=13 C2_R54_PASS=false`; contract `claims.C2.before` also `total=13`; receipt bytes identical base..C0 | ok / ok / ok | **agree** |
| ER-R54-4 | `49280fe5` for c2 — `REP:122` ("the freeze-manifest digest `d7749f84…` (c1) and `49280fe5…` (c2)") | `Rfreeze.json` key `c2/measure.py` = `8528ee85…`; the deciding blob `c2108100:Rc2/measure.py` **hashes to exactly that**; `49280fe5` is the pre-amendment-4 blob (commit `19c7558`), `8528ee85` arrives with the amendment-4 commit `fe70474` | ok / ok / ok | **agree** |
| ER-R54-5 | "returned **25 findings**" (w1) `REP:62`; "22 findings in 9 of the 23 sections" (w2) `REP:79` | re-derived with the counter's exact rule (`T54W\d+[A-Za-z]*Read\d+\.json`, `len(findings)`): **w1=28 over 23 reader files; w2=25 over 12 of 23** — identical at base, at deciding rev `c2108100`, and at C0 | ok / ok / ok | **agree** |
| ER-R54-6 | "three seat deliverables untracked when the round filed" — proved by `Rafter/clean-tree-after.txt`, whose three `??` lines are exactly `T54W2Sent03.md` + the two receipts | `ff2a821` adds exactly those three files (309 insertions, no other path), is an ancestor of base, and all three exist at C0 | ok / ok / ok | **agree** |
| ER-R54-7 | "the deletion lands in `7fa9a5e0`" — `REP:116` | `git show --name-status -M 7fa9a5e` contains `R100 … T54W2Sent01-forged-reader.json → T54W2Sent01-receipts/forged-reader.json`; old path absent, new path present at C0; its path fails the reader regex; its `section_sha256` `b90c1f79…` matches **0 of 64** sections at c0 `99c3bc88d704…` (round-18 `sectionize`, frozen) while the genuine reader's `61736dce…` is `## Standing rules` | ok / ok / ok | **agree** |
| ER-R54-8 | base `corpus/lessons/round-54.md` mentions `config.yml` **0 times**; base `T54W1ExecStraceNoise.md:324` asserts the edit was "on the operator's direct instruction in-session, which is the higher authority"; `REP:105-112` names the incident | C0 seat file carries `**SUPERSEDED (round 55, ER-R54-8).**` (line 332) withdrawing both the "fabricated" characterisation **and** the licence claim; C0 `corpus/lessons/round-55.md:62` records it; `history.db` id 690 = `2026-10-28 15:12:15`, prompt `use m_glm53 instead of m_grok`; `~/.omp/agent/config.yml:418` reads `scout: "@m_grok"`; the 5 m 33 s gap is receipted (`…w1/T55W1Rev10-receipts/r548-premises.stdout`: `15:06:42.101Z -> 15:12:15.736Z = 5m33.6s`) | ok / ok / ok | **agree** |
| ER-R54-9 | `REP:8` "attack-role share 26.3 % in w1"; `REP:58-59` "4 critics, 4 reviewers"; base `corpus/lessons/round-54.md:51` "The other 84 staged `merge/tameshi` entries" | `R…/w1-registry.json`: `reviewer=5`, `attack_seats=21`, `seats=76`, role_mix sums to 76 ⇒ 21/76 = 27.6 %; `staged-at-freeze.txt` prints `output=81` (live read-only count today also 81); in-place lesson now reads "The other **80** staged" = 81 − the one named entry, which is arithmetically consistent | ok / ok / ok | **agree** |
| ER-R54-10 | `REP:50-52` quotes "`CTL_R53` (the round-53 final tree, 58/64, `rekeyed=0/30`)" under `control/controls-a.stdout` | `Rcontrol/controls-a.stdout` `CTL CTL_R53` line: `… credited=58 lost=6 rekeyed=0/7 …`; `Rcontrol/r53-counter-at-88afa941.stdout`: `rev=88afa9415454 … rekeyed=0/30 …` | ok / ok / ok | **agree** |

Rows that carry a *second* claim were checked too: ER-R54-1's "phase B cloned the FREEZE commit, which
predates the re-key" (`git merge-base --is-ancestor 077d431e 7fa9a5e0` → yes; controls-b line prints
`rev=077d431e6996`), and its closing promise that round 55 re-scores its own positive control at the
certified revision — `.ufo/evidence/round-55/controls.sh` phase B does exactly that (`clone_at "$LANE"
"$REV"`, then `score` passes `--rev "$(git -C "$d" rev-parse HEAD)"`), so R54.1 is not merely re-narrated,
it is structurally excluded from round 55's own control.

## Findings

### F1 — medium: the section's preamble claim of uniqueness is false at C0 (not an ER row)

> "this section is the only place where the old values are quoted, which is why the round-55 counter
> (`.ufo/evidence/round-55/c1/measure.py`) counts every stale token outside it."

The census (`verify-ten-rows.out`, PREAMBLE-CENSUS block) shows `corpus/lessons/round-54-verifier-spotcheck.md`
— the routing document — still quotes **every** old value: `CTL_POS_c1 true`, `total=14`, `49280fe5`,
`7fa9a5e0`, `84 staged`, `7883e0e5`, `fe70474d`, `097985c1`. `rekeyed=0/30` additionally stands in
`corpus/QUALITY.md`, `corpus/lessons/round-54.md`, `corpus/lessons/round-53-verifier-spotcheck.md` and the
round-54 spotcheck (legitimately there — it is the round-53 arm's true value, correctly attributed).
The counter's `RECORD` set is `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/lessons/round-54.md`, `LOG.md`
(`measure.py:38-43`), which excludes the routing document; so "counts every stale token outside it" is
true only *within that four-file set*, and the unqualified "only place" is contradicted by the tree.
Consequence: a reader who verifies the claim the way it is written (`grep -rn`) finds eight hits and
concludes the correction failed. This is a calibration artifact making an imprecise record claim — the
class the section exists to repair. Not blocking for C1 under this seat's criterion (no ER row's old text
or value is wrong); the honest phrasing is "the only place where the old values stand as the lane's own
assertion" or "the only place in the counter's record set".

### F2 — minor: ER-R54-4's `Old` names no artifact

`Old: `49280fe5` for `c2/measure.py`` gives no file and no line, so "is this what the file said at base"
cannot be checked from the row (the value lives at `REP:122`). ER-R54-3 does this correctly ("in the C2
claim row"). Same for ER-R54-6, whose `Old` is a tree state with no receipt named — the receipt it rests on
is `Rafter/clean-tree-after.txt`, which the row does not cite.

### F3 — minor: ER-R54-7 names no command, and renders one commit two ways

The rename is verifiable (`git -C LANE show --name-status -M 7fa9a5e`) but the row names no command and no
receipt for it, unlike every other row. It also prints the *same* commit as 7-char `7fa9a5e` in the
correction while quoting the old 8-char `7fa9a5e0`; both resolve to `7fa9a5e0104bc…` (the old text's error
was "deletion", not the sha), so the two spellings read as two commits in a section whose subject is
pointer hygiene.

### F4 — minor: ER-R54-8's 5 m 33 s and row-690 locator are unpointered / mutable

The gap number has no pointer in the row; it is receipted at
`.ufo/waves/round-55/w1/T55W1Rev10-receipts/r548-premises.stdout` (`gap 15:06:42.101Z -> 15:12:15.736Z =
5m33.6s`). And `history.db` row 690 is an `AUTOINCREMENT` id in a live table: reproducible today
(`select id, datetime(created_at,'unixepoch') … where id=690`), not stable for a later reader. A prompt-text
locator (`prompt = 'use m_glm53 instead of m_grok'`, `UNIQUE`) would survive.

### F5 — minor: ER-R54-5's literal command covers only half the count

`git ls-tree -r --name-only <rev> -- .ufo/waves/round-54/w1` yields the w1 half; `w2=25 sections=12` needs
the `w2` path as well. The row's second clause ("the round-55 c1 counter does exactly this at every
revision") does cover both, so the row is reproducible via the counter — but not via the command as
written.

### F6 — informational: a corrected token is split inside its own code span

ER-R54-1's corrected value is hard-wrapped as `` `CONTROLS_B: `` / `` 2/3` `` (lines 16-17 of the section),
so a byte grep for `CONTROLS_B: 2/3` misses the section's own statement of it. The counter's arm tests
`"2/3" in corr`, which passes; a human grep does not. (My own first pass failed on exactly this — the
checks now normalize whitespace, the lesson round-54's amendment 2 taught.)

## What I did not find

- No row's *old* text is a fabrication: all ten are verbatim (modulo markdown backticks and the documents'
  ~78-column wrapping) in the artifact the row names, at base.
- No row's *corrected* value contradicts its receipt: each is either the literal token the receipt prints
  or the value the stated derivation yields, and I re-derived the derivable ones (4, 5, 7, 9, 10) from
  first principles rather than trusting the section.
- No receipt pointer is wrong: every named path exists at C0, is byte-identical base..C0
  (`git diff --stat 0a2010a..C0 -- .ufo/evidence/round-54/` empty), and carries the cited fact.
- The in-place fixes outside the section are consistent with the section's corrected values where I
  sampled them: `QUALITY.md:1590` now prints `rekeyed=7/7` at the deciding revision and `rekeyed=3/7` with
  `CTL_MISMATCH` on the control cloned at the freeze commit; `lessons/round-54.md` now reads "the other 80
  staged" (81 total − the one named entry); no stale token (`CTL_POS_c1 true`, `total=14`, `7883e0e5`,
  `fe70474d`, `097985c1`, `7fa9a5e0`) survives in `SCORECARD.md` outside the section, in `LOG.md`, or in
  `lessons/round-54.md`.

## Residual risk and verification gaps

- I did not re-run round-54's counters. Not needed: the receipts are frozen bytes, and the whole
  `.ufo/evidence/round-54/` tree is identical at base and C0, so "the receipt prints X" is time-invariant.
- `sections=12` is "reader files with ≥1 finding", not `SKILL.md` sections; the label follows the report's
  own usage and the ledger's `minor_gaps` entries. A reader expecting heading counts will misread it.
- `merge/tameshi` live count (81) reproduced read-only today; the counter reads the frozen receipt, not the
  worktree, so the claim cannot drift (amendment 7) — but the receipt itself is a one-shot observation of a
  sibling lane's package.
- ER-R54-8's `5 m 33 s` rests on a wave-1 seat's transcript-line timestamps; I did not open the transcript
  itself (read-only, outside the lane's records) beyond confirming the receipt that quotes it.
- Not attempted: whether each row's *prose fairness* to the harmed reader is right, and whether the named
  receipt is the only receipt that could carry the fact — both are the contract's declared `cannot_see`
  and are argued by other seats, not measured here.

## Artifacts opened

lane @ C0 unless noted: `SCORECARD.md` (2621-2702 and pre-section grep), `corpus/QUALITY.md` (criterion 105,
base + C0), `corpus/lessons/round-54.md` (base + C0), `corpus/lessons/round-55.md` (R54.8 row),
`corpus/lessons/round-54-verifier-spotcheck.md` (base, R54.1-R54.10 + erratum),
`LOG.md` (token grep), `.ufo/evidence/round-54/{before/c2.stdout, after/frozen.stdout,
after/clean-tree-after.txt, after/clean-tree-before.txt, after/deciding-run.exit, control/controls-a.stdout,
control/controls-b.stdout, control/r53-counter-at-88afa941.stdout, freeze.json at 077d431e and at
7883e0e5/fe70474d/097985c1/441c26be, contract.json (base + C0), c2/measure.py at C0/c2108100/19c7558,
c1/measure.py}`, `.ufo/evidence/round-55/{contract.json, c1/measure.py, c1/staged-at-freeze.txt,
controls.sh}`, `.ufo/evidence/round-18/measure.py` (`sectionize`), `.ufo/waves/round-54/{w1-registry.json,
w1/T54W1ExecStraceNoise.md (base + C0), w2/T54W2Sent01-receipts/forged-reader.json,
w1|w2/T54W*Read*.json (46 files, by derivation)}`, `.ufo/waves/round-55/w1/T55W1ScribeSeat-receipts/*`,
`.ufo/waves/round-55/w1/T55W1Rev10-receipts/r548-premises.stdout`; fleet root (read-only):
`fcb8d8db:.ufo/reports/round-54/tameshi.md`; host (read-only): `~/.omp/agent/history.db` (SELECT-only),
`~/.omp/agent/config.yml`, `find /home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge -name '*.md' | wc -l`.

Tooling: no installs or upgrades; `pacman` transactions are paused host-wide and nothing needed one.
Scratch: `/fast/scratch/hyaku/tameshi-r55/T55W2RevCorrections` (removed after the receipts were copied into
the lane; the shared parent was never touched).
