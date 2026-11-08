# SC1 — `LOG.md` append draft (round 95)

**Seat:** R95SC1 (scribe). **Lane:** tameshi. **Mode:** read-only — nothing under
`corpus/` or at the lane's `LOG.md` was written; this file is a draft for the L1 to
integrate.

The entry goes at the end of the lane's `LOG.md` (the round-94 entry ends at line
`5092`, the last line of the file). It follows the round-93/round-94 shape: **Shape.**
/ **claims** / **Motivating evidence.** / **Frontier.** / **Routed.** — the shape the
lane's own LOG entries use.

Every number below was read from a file at the revision named; nothing is projected.
Where the round has not yet produced a receipt, the draft says so rather than
guessing.

---

## Round 95 (2026-11-08) — two claims: the reader's literal classes (coverage) and the audit's receipt bytes (calibration)

- **Shape.** One v1 wave `w1`, 13 seats: executor 4, reviewer 2, scribe 1, scout 1,
  critic 1, mutation-tester 1, sentinel 1, connector 1, revenger 1 — the seat count is
  printed by `.ufo/waves/round-95/w1-dispatch.json` `counts.total` (13) and its 13
  registry members, not written by hand. Base `02ff6290945dde18062a366799a774abb50fb365`;
  freeze commit `0d3fc99b36a8ea1f18356066425ecdb56fdad748` ("round-95: freeze
  declarations — plan, w1 spec (13 seats), dispatch, census before"); instruments
  `0685c3586805a2f2aed07e0038239cf384c38c4c`; lesson Gate reflow `20fabad4` (R95R1's
  finding); claims freeze `3ca1981a2265880ae3ce9b88d316e71741b02426`
  (`.ufo/waves/round-95/freeze-rev.txt`). **The plan's §Wave says "12 seats"**
  (`plans/round-95.plan.md:172`) while the dispatch it points at commits 13 — the 13th
  is the L1's own `revenger` seat; recorded as `lessons/round-95.md` M5 and routed below.
- **R95-C1 (coverage) — the note reader governs five presentation states it did not
  govern.** The successor reader adds the indented-code class (S323), the escaped
  backslash before a pipe, the one/two-hyphen delimiter (S321's rule, re-read), and a
  second self-pin line. The five added states are `indent-code-row`, `indent-token`,
  `escaped-backslash-pipe`, `two-hyphen-delimiter` and `double-pin`; the first three
  are measured against the round-94 reader in
  `.ufo/waves/round-95/w1/R95E1-five-states-discriminate.out` (`indent-code-row` v94
  `verdict_tables=2 badrows=12 ids_ok=False` → v95 `verdict_tables=1 badrows=0
  ids_ok=True`; `indent-token` v94 `badrows=1 stray-verdict:365` → v95 clean;
  `two-hyphen-delimiter` v94 `verdict_tables=0 badrows=12` → v95 clean) and the
  backslash arms in `R95E1-backslash-discriminate.out` (v94 mis-splits
  `| C01 | fixture arm\\| KILLED | differs |` into `['C01', 'fixture arm\\| KILLED',
  'differs']`, v95 into `['C01', 'fixture arm\\', 'KILLED', 'differs']`). The
  double-pin arm refuses at setup with `C1_SETUP self-pin-line-count` (exit 2,
  `R95E1-refusals.out`). At the current HEAD the counter prints
  `C1_SOURCE S320=row:1,quote:1 S321=row:1,quote:1 S322=row:1,quote:1 S323=row:1,quote:1`
  and `C1_R95_PASS=true` (exit 0) — the `source` conjunct reads a located quote per row
  out of `corpus/lessons/round-95.md`, and the round's own reviewer (`R95R1`) found that
  the first landed lesson's Gate quotes sat on lines that did not name their sid, which
  made the counter read zero quotes and `source=false`; the L1 reflowed the Gate at
  `20fabad4`. **What the reflow did not reach is the numbers inside the quotes' own
  lines**: at HEAD, five of the six Gate lines mis-state their quote's word count and
  four cite a line that carries different text, and the `S323` registry row repeats both
  errors (`(15 words)` for a 16-token span; `line 2355` for a sentence that begins at
  line 2358) — recorded as `lessons/round-95.md` M4 and QUALITY 172.
- **R95-C2 (calibration) — the disposition audit reads receipt bytes from the object
  store.** The checker reads each receipt at `--rev` from the object store and refuses
  one that is absent there or whose `counter_sha=` differs from the counter blob's
  digest; the selftest carries 11 cases and prints `DISPOSITION_SELFTEST: 11/11 pass`
  (exit 0, `.ufo/waves/round-95/w1/R95E3-selftest.out`). The three forged receipt sets
  are measured in `.ufo/waves/round-95/w1/R95E3-forge/forge-matrix.txt` (8 checks, 0
  failed): `forge-handwritten` → exit 1 `receipt-absent-at-rev`; `forge-counter-sha` →
  exit 1 `receipt-counter-sha-mismatch`; `forge-replace-ref` → exit 2
  `DISPOSITION_SETUP replace-refs-present` — while the round-94 checker at `6a2a1fdd`
  prints `findings=0` on the first two and reads the substituted blob on the third.
- **Motivating evidence.** The round-94 non-author spot-check
  (`corpus/lessons/round-94-verifier-spotcheck.md`) routed eight record and instrument
  defects; this round answers them (`plans/round-95.plan.md` §Round-94 defects) and
  its routed item 1 — the C2 selftest tally `8/8` versus the operative `9/9` — is
  reconciled by the append-only erratum in `corpus/lessons/round-95.md` § Erratum, which
  names the superseded sentence and edits none of the three frozen files
  (`plans/round-94.plan.md:165`, `LOG.md:5085`, `corpus/lessons/round-94.md:66`).
- **Frontier.** S320, S321 and S322 re-opened (all three snapshots byte-identical to
  round 94's) and S323 admitted new (CommonMark 0.31.2 §4.4 Indented code blocks,
  sha256 `c85f56cc…60f0d`, the same page bytes as S322); registry rows 182 → 183.
  QUALITY 169–172. Mistakes M1–M5 in `corpus/lessons/round-95.md`.
- **Routed.** Four items for round 96: (1) the plan's §Wave seat count against the
  dispatch's member count — the round-94 closure's routed item 4 again, one round
  later (`lessons/round-95.md` M5); (2) the `S323` registry row's hand-written word
  count and anchor line, and the Gate's hand-written counts and line numbers — QUALITY
  172 and the corrections drafted in `.ufo/waves/round-95/w1/SC1-sources.append.md` and
  `SC1-lesson.md`; (3) the round-94 plan's `§Wave`/`§Controls` seat and state lists,
  whose counts disagree with the artifacts they name in more than one place — a check
  that re-derives a count from the table it names, printed by a command; (4) the twelve
  round-94 rule-level survivors (E04, E05, E09, E10, E13, E15, E16, E20, E26, E29, E30,
  E32), re-registered against the round-95 reader in
  `.ufo/waves/round-95/w1/R95E4-defects.txt` and measured by R95E4 — one discriminating
  state per survivor, which the round-94 wave showed the round-94 reader lacks.

---

## Drafting notes for the L1 (not part of the entry)

- **Where the entry goes.** At the end of the lane's `LOG.md` (after the round-94 entry
  that ends at line 5092). The fleet-root `LOG.md` is a different file (1294 lines) and
  is not this lane's log.
- **Numbers to re-verify before landing.** The `C1_CONTROLS states=50 …` aggregate and
  the round-95 census-after histogram on the lane are the round report's to print, from
  committed receipts, at the records commit. The census **before** figures quoted above
  (rows 182, tiers A=164 B=14 C=4, status mined=148 queued=23 rejected=11) are from the
  committed `.ufo/waves/round-95/census-before.txt` and re-measured by R95SC1 against
  the lane at `0685c358` (exit 0). The census **after** is expected to read rows 183,
  tier A 165, status mined 149, with one additional `W04` duplicate-URL warning (S322
  and S323 are two rows on `https://spec.commonmark.org/0.31.2/` with different
  scopes) — measured on a scratch mirror, see `SC1-sources.append.md` §Census check.
- **The `C1_R95_PASS` line.** The draft reports the counter's current value at HEAD
  (`true`, re-measured) and names the failure that preceded it (`source=false`,
  `quote:0` at `0685c358`), because the entry is a record of the round as it stands and
  the fix is part of the round's history. If the L1 prefers, the failure sentence can be
  dropped — but it must not keep both without saying which revision each belongs to.
- **`R95-C1` is not a verdict.** This entry reports the five states' measured
  discrimination and the counter's reading of the lesson; the round's per-axis verdict
  is the round report's, after the wave closes.
