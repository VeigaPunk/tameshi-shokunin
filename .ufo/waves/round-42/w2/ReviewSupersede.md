# ReviewSupersede — round 42 wave 2 (FALSIFY): the two supersede receipts

Seat: `L1Tameshi42.ReviewSupersede` (reviewer, read-only). Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`,
tip `a21845f523b75adbd3e3f7a62af91294db224ad9`. Only lane write: this file. Scratch file
`/tmp/r42w2-ReviewSupersede-draft.json` (deleted). No tool installs or updates. `lsp` is not
relevant: every target is JSON/Markdown read through git objects.

Attacked: `.ufo/waves/round-42/supersede/round-41-residual-receipt.json` (the C1 repair) and
`.ufo/waves/round-42/supersede/round-20-outcomes.json` (an out-of-claim correction).

## Findings (by severity)

### F1 — low: `round-20-outcomes.json` `reason` says something the record does not support
`git show a21845f…:.ufo/waves/round-42/supersede/round-20-outcomes.json` `reason` says:
"original-outcomes.json, the original dispatch record, already agrees." But
`.ufo/waves/round-20/original-outcomes.json` has **no `report_exists` or `present` field and no report
path** (its schema is `tameshi-r20-original-seat-outcomes-v1`, with seat keys `name, role, status, model, error,
timestamp`). For this seat it records `{'name': 'A01ProvRound19Ruler', … 'status': 'failed', … 'code=turn_rate_limit_exceeded'}`
(`seats[0]`), and lists A01 in `unsolicited_peer_wakeups` (`['A01ProvRound19Ruler', 'B10HistRound19', 'D07WordingErratum']`).
So "agrees" is vacuous at best: the original record makes no claim about whether the report exists. Read
alongside `outcomes.json:735` ("no dead seat is rehabilitated by this later snapshot"), it reads as though the
original record backs a report from a seat it marks dead. The claim came from `.ufo/waves/round-42/w1/ScoutReceiptSweep.md:25-26`
("original-outcomes.json has 0 mismatches vs base (all 72 seats match)"), and that zero comes from a field that
does not exist. The assertion itself, `present: true` for the A01 report, is correct (see F3). Only the
prose justification is wrong. This does not affect C1: the m10 count is unaffected and the file is out of claim.
Command: `python3` walk over `git show a21845f…:.ufo/waves/round-20/original-outcomes.json` (top keys `schema, basis,
total, completed, dead, seats, unsolicited_peer_wakeups, no_replacements`; zero `report_exists`/`present` entries).

### Checks that held

- **Hash, and byte-exact to the draft.** `sha256sum .ufo/waves/round-42/supersede/round-41-residual-receipt.json`
  gives `987f82b4ce749787068d5845208382f930422d84126c94a7b2431e8d08334979`. The tip blob
  (`git show a21845f…:<path> | sha256sum`) gives the same value, and the working tree is unchanged
  (`git status --short` is empty). I extracted the ```` ```json ```` block of
  `.ufo/waves/round-42/w1/ExecSupersedeDraft.md` with awk to a scratch file: 1382 bytes, the same sha256,
  and `cmp` against the landed file reported `BYTE_EQUAL`.
- **Every asserted path exists, is non-empty, and is the right seat.** `git cat-file -t/-s a21845f…:<path>`:
  ResidualReplayC1 blob 12373 (`Seat: L1Tameshi41.ResidualReplayC1`), ResidualReplayC2 16089
  (`Seat: L1Tameshi41.ResidualReplayC2`), ResidualReceipts 24386 ("every citation in the round-41 report, checked
  at the tip"), ResidualScope 24839 ("path scope of the landed round-41 diff"), ResidualIds 14995 ("item-10 id
  lists vs the assimilation evidence"), ResidualCounts 16434 (`seat: L1Tameshi41.ResidualCounts`),
  ResidualAppendOnly 14002 ("append-only attack on the landed round 41"), ResidualClaims 28497
  (`Seat: L1Tameshi41.ResidualClaims`). Each title matches its item in `.ufo/waves/round-41/residual/spec.json`
  (8 items, same names). A01ProvRound19Ruler is a blob of 9917 bytes whose line 3 reads `Seat: TameshiR20-3.A01ProvRound19Ruler`,
  which matches `agent_id` in `round-20/outcomes.json`. All 9 asserted paths resolve at both the freeze `322b5cd…`
  and the tip (`resolves=9/9`), so the phrase "at the round-42 freeze commit" in both `reason` fields is true.
- **The round-41 receipt covers everything it supersedes.** `.ufo/waves/round-41/residual/receipt.json` asserts
  8 `report` paths, with ResidualReceipts `present: false` as the only stale one. The supersede re-asserts all 8 with
  `present: true` and has no stale assertions of its own, so `theirs ⊆ mine` holds and `measure.py:206-213`
  marks it covered.
- **The round-20 receipt's facts.** `outcomes.json` has 72 seats. Mapping each `name` to
  `.ufo/waves/round-20/w1/<name>.md` gives 71 agreeing and 1 mismatching (`A01ProvRound19Ruler False True completed`).
  That matches "other 71 … agree". The claim "not counted" also holds: `walk_present` (`measure.py:175-179`)
  keys on `present` with a string `report`, so `outcomes.json` yields no entries and is not a receipt. The
  supersede is audited as an ordinary receipt and has 0 stale assertions.
- **The superseded receipts were not edited.**
  `git -C …/tameshi-shokunin diff c77c2b7e64d2e356381441ecf94abac03e984606 a21845f523b75adbd3e3f7a62af91294db224ad9 -- .ufo/waves/round-41 .ufo/waves/round-20`
  gave empty output (`--stat` empty, `--name-status | wc -l` gives `0`).
  `git log --oneline c77c2b7..a21845f -- .ufo/waves/round-41 .ufo/waves/round-20 | wc -l` gives `0`.
  Last touches: round-41 at `b14ff11`, round-20 at `dc046fa`, both before the base. `.ufo/waves/round-42/supersede/`
  holds exactly 2 files at the tip.
- **Counter.** Pre-run (labelled) at base `c77c2b7…`:
  `MISMATCH m10 .ufo/waves/round-41/residual/receipt.json asserts present=false for …/ResidualReceipts.md; tree says true`,
  giving `m10=1 … C1_R42_PASS=false`. Pre-run (labelled) at tip `a21845f…`:
  `C1_R42: self_pin=1 m6=0 m7=0 m8=0 m10=0 m11=0 total=0 records=6 sources_rows=113 … C1_R42_PASS=true`.
  `--selftest` gives `C1_R42_SELFTEST: cases=9 failed=0` (it includes `T2_junk_supersede_still_counts` and
  `T2_partial_supersede_still_counts`). This is not the deciding run; that belongs to the L1. The
  `exit=0` echoes in my shell were the exit codes of `tail`, so I recorded no exit code for the counter.

## Residual risk and verification gaps

- The checks are about whether the files exist and are the right seat. I did not re-audit the content
  quality of the 9 reports.
- The meaning of `present` is still "the file exists in the tree". A01 is `failed` in the original record yet has
  a report that came from a later peer wakeup, so `present: true` does not mean the seat succeeded. Neither
  receipt claims that it does, apart from the wording in F1.

Verdict: SURVIVES. Both receipts hold, and the superseded receipts were not edited. F1 is a low-severity
wording defect in the `reason` field of `round-20-outcomes.json` and does not affect the claim.
