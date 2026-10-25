# Residual seat — C1 replay at the measured commit and the tip

Seat: `L1Tameshi41.ResidualReplayC1`. Read-only: this file is the only write. No tool installs, no
lane/record/fleet/jj/index edits. All commands ran from
`/home/vgpnk/Projects/shokunin/tameshi-shokunin` unless stated.

Lane tip `812ee0d11d267e131be3dc8db0b71253cbae9234`; measured commit
`2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6`; base `a3d6c690bcbf8914551d4f4e8e1612784c1c2046`;
deciding-run revision named by the records `baa18b7bdd637ff175255e82b6bee3c85df0881e`.

Executed counter (worktree copy; identical bytes to the blob at every revised commit below):

```
$ sha256sum .ufo/evidence/round-41/calibration/measure.py
9aaa99ac5a5abd16a42123fba4bf5c90151b3d043aa2d92ee99116e5789d92cd
$ for r in b37ce974 baa18b7b 2ae00eb 812ee0d; do git show $r:.ufo/evidence/round-41/calibration/measure.py | sha256sum; done
9aaa99ac… (each of the four)      # base a3d6c690: path absent (round-41 artifact)
```

`9aaa99ac…92cd` is `claims.C1.counter_sha256` in `.ufo/evidence/round-41/contract.json`, so the bytes
executed here are the contract-pinned bytes. My runs are labelled replays, per the seat's terms.

## Runs

Command (exact): `python3 .ufo/evidence/round-41/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV`

| REV | exit | stdout (predicate line) |
|---|---|---|
| `a3d6c690bcbf8914551d4f4e8e1612784c1c2046` (base, reference) | **1** | `C1_R41: m6=1 m7=0 m8=0 m9=1 total=2 records=0 sources_rows=107 rev=a3d6c690bcbf8914551d4f4e8e1612784c1c2046 C1_R41_PASS=false` |
| `baa18b7bdd637ff175255e82b6bee3c85df0881e` | **0** | `C1_R41: m6=0 m7=0 m8=0 m9=0 total=0 records=3 sources_rows=109 rev=baa18b7bdd637ff175255e82b6bee3c85df0881e C1_R41_PASS=true` |
| `2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6` | **0** | `C1_R41: m6=0 m7=0 m8=0 m9=0 total=0 records=3 sources_rows=109 rev=2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6 C1_R41_PASS=true` |
| `812ee0d11d267e131be3dc8db0b71253cbae9234` | **0** | `C1_R41: m6=0 m7=0 m8=0 m9=0 total=0 records=3 sources_rows=109 rev=812ee0d11d267e131be3dc8db0b71253cbae9234 C1_R41_PASS=true` |

Reproducibility of the committed receipts: my `--rev 2ae00eb…` stdout is byte-identical to
`.ufo/evidence/round-41/after/c1-at-2ae00eb7.stdout` and my `--rev baa18b7b…` stdout is byte-identical
to `after/c1-at-baa18b7b.stdout` (`diff` empty for both, single 125-byte line including `\n`). The base
stdout matches `before/c1-at-base.stdout` line for line. Committed exit files: `before/c1-at-base.exit`
= `1`, `after/c1-at-baa18b7b.exit` = `0`, `after/c1-at-2ae00eb7.exit` = `0` — all reproduce.

Cwd independence (the counter resolves `--rev` with `git rev-parse` and reads with `git show` /
`git cat-file -e`, so nothing is read from the worktree in non-`work` mode):

```
$ cd /tmp && python3 …/calibration/measure.py --lane …/tameshi-shokunin --rev 812ee0d11d267e131be3dc8db0b71253cbae9234
C1_R41: … sources_rows=109 rev=812ee0d11d267e131be3dc8db0b71253cbae9234 C1_R41_PASS=true     EXIT=0
```

`--control` and `--selftest` do not exist on this counter (CLI is `--lane --rev [--fleet]`); both flags
are rejected with argparse exit 2 (`error: unrecognized arguments: --selftest`), so the seat's permission
to run them has no target on C1. C1's negative control is its base run, which still prints `m6=1 m9=1`.

## Character-for-character comparisons

Pasted line in `SCORECARD.md`:1971 / `### Round 41 — after the deciding run` (124 bytes):

```
C1_R41: m6=0 m7=0 m8=0 m9=0 total=0 records=3 sources_rows=109 rev=baa18b7bdd637ff175255e82b6bee3c85df0881e C1_R41_PASS=true
```

Pasted fragment in `LOG.md`:2179, the deciding-runs bullet (the bullet names the revision in prose —
"Deciding runs, both at `baa18b7b…`" — and quotes the line without the `C1_R41: ` prefix and without
the `rev=` field):

```
m6=0 m7=0 m8=0 m9=0 total=0 records=3 sources_rows=109 C1_R41_PASS=true   (exit 0)
```

| # | comparison | result |
|---|---|---|
| A | replay@`2ae00eb` line vs SCORECARD pasted line | **DEFECT** — not identical; first difference at index 67, differing substring `2ae00eb750…fd8a6` vs `baa18b7bdd…881e`; lengths 124/124; field-diff set is exactly `{rev}` |
| B | replay@`812ee0d` line vs SCORECARD pasted line | **DEFECT** — same shape; first difference at index 67; field-diff set exactly `{rev}` |
| C | replay@`baa18b7b` line vs SCORECARD pasted line | **PASS** — byte-identical, 124 chars, single line |
| D | replay@`2ae00eb` line vs LOG deciding bullet | **PASS on fields** — the quoted token equals the run line minus `C1_R41: ` and minus ` rev=…`; `stripped == fragment` is true; exit claim `(exit 0)` matches |
| E | replay@`812ee0d` line vs LOG deciding bullet | **PASS on fields**, same reconstruction, same exit claim |
| F | replay@`baa18b7b` line vs LOG deciding bullet | **PASS on fields** (+ the prose revision equals the line's `rev=`) |
| G | exit codes vs the records ("Both exit 0" / "(exit 0)" / base "exit 1") | **PASS** — 0/0/0 measured, 1 at base; committed `.exit` files agree |
| H | `rev=` field names a revision whose counter bytes match the contract pin | **PASS** — `baa18b7b`'s blob hash is `9aaa99ac…92cd` = `claims.C1.counter_sha256`; likewise `2ae00eb` and `812ee0d`. The pasted `rev=` is a revision, not a tree, so no pin question arises for it beyond this |

## Findings

**D1 — DEFECT (record precision, medium). The pasted after-line is not the line the counter prints at
the measured commit or at the tip, and the round's artifacts paste two different lines while claiming
they are the same.**

Evidence, same pinned counter, two revisions:

```
$ python3 …/measure.py --lane …/tameshi-shokunin --rev 2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6
C1_R41: … sources_rows=109 rev=2ae00eb750b86eba6c9b54b36b1a6e875e9fd8a6 C1_R41_PASS=true   exit 0
$ python3 …/measure.py --lane …/tameshi-shokunin --rev 812ee0d11d267e131be3dc8db0b71253cbae9234
C1_R41: … sources_rows=109 rev=812ee0d11d267e131be3dc8db0b71253cbae9234 C1_R41_PASS=true   exit 0
```

Both differ from the pasted line only in the 40-hex `rev=` field (index 67, equal length 124), because
`rev` is echoed from the normalized `--rev` argument. The divergence is internal to the round, not an
artifact of my choice of revision:

- `SCORECARD.md` and `LOG.md` paste/quote the `rev=baa18b7b…` variant;
- `.ufo/reports/round-41/tameshi.md:89` pastes the `rev=2ae00eb…` variant as the "After, at
  `2ae00eb…`" line, and that line is byte-identical to my replay at `2ae00eb`;
- the report's line and the scorecard's line differ from each other at the same index 67, both 124
  bytes;
- `SCORECARD.md` says "the same two commands were executed again at the commit that carries this
  section and printed the same two lines", `LOG.md`:2183 says "The same two commands re-ran at the
  commit carrying this entry and printed the same lines", yet the lane's own committed confirmation
  receipt at that commit (`.ufo/evidence/round-41/after/c1-at-2ae00eb7.stdout`, added by `0c8e1be`)
  prints a **different** line from the one pasted above it.

Impact is confined to provenance: every declared predicate field (`m6 m7 m8 m9 total records
sources_rows C1_R41_PASS`) is identical at `baa18b7b`, `2ae00eb` and `812ee0d`, so no measured value is
overclaimed; what fails is the identity/consistency claim about the pasted text. Note the shape: this
is an m9-shaped self-contradiction (a summary contradicting its own table) reappearing one level up —
prose "same lines" versus the round's own receipts — and no C1 class can see it, because m9 is scoped
to the round-40 lesson. The honest phrasing is "re-ran with the same `--rev` and printed the same
line; a run at the carrying commit prints the same counts with `rev=` set to that commit".

**D2 — DEFECT (precision, low). "Re-ran at the commit carrying this entry and printed the same lines"
is unfalsifiable as constructed.** `read()` uses `git show <rev>:<path>` and `resolves()` uses
`git cat-file -e <rev>:<path>`, and `rev` is normalized by `git rev-parse`; the counter never reads the
invoking tree. With `--rev baa18b7b…` the line is a pure function of that revision, so the re-run cannot
differ unless the counter is nondeterministic (it is not — my replay hours later is byte-identical to
the committed receipt) or the `--rev` argument changes — which is exactly what D1 shows happened. The
sentence therefore evidences determinism only, not that the measurement was re-executed over the
carried records.

**D3 — DEFECT (wording, low). "the counters … write only a temporary directory" is false for C1.**
`grep -nE "tempfile|mkdtemp|open\(.*['\"]w|os\.write|write_text" .ufo/evidence/round-41/calibration/measure.py`
→ no matches: the C1 counter writes nothing. The claim is stronger than needed rather than weaker, and
C2 (which does use a temp dir) is where the sentence belongs.

## Checks that passed (no actionable defect)

- **Exit codes**: 0 at `baa18b7b`, `2ae00eb`, `812ee0d`; 1 at base; matches `after/*.exit`,
  `before/c1-at-base.exit` and both prose claims.
- **Contract pin on the pasted `rev=`**: `9aaa99ac…92cd` at `baa18b7b` (and at both later revisions); no
  amendment drift after A5.
- **Registry count (m6) is independently true, and m6 is live, not vacuous**: the standing row's own
  command `grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md` gives **109** at `812ee0d`/`2ae00eb`/`baa18b7b`
  and **107** at base; unique ids 109, zero duplicate ids; the counter's `standing[-1]` parse of
  `SCORECARD.md`:1851 yields `109` against `observed=109` (at base `103` vs `107` → m6 fires, as receipted).
- **m7 index and liveness**: registry rows have 13 `|`-split cells with status at index 8 (`S153` →
  `cells[8]='mined'`); the round-41 records cite exactly `S001, S153, S154`, all `mined` in the 109-row
  registry. Non-vacuity proved by recomputing with the counter's own functions at all three revisions:
  `cited_sids=3`, all mined.
- **m8 liveness and coverage drift**: 27 backticked lane-relative tokens in the round-41 records at the
  tip, 0 unresolvable; 25 at `baa18b7b`, 0 unresolvable (the extra 2 are the receipt paths added with
  the after sections). I also probed outside m8's read surface — every `corpus/ tools/ .ufo/evidence/round-41/
  .ufo/waves/round-41/` occurrence in the three records **outside** inline code — and found 0 candidates,
  so no live miss this round.
- **m9 liveness and derived words**: round-40 lesson `table=(1, 6, 10)`, `summary=(1, 7, 9)`; derived
  words `(six, ten)` both present in `corpus/lessons/round-41.md`:55 ("one adopted, six refused, ten
  present-but-not-appended"), so m9 is satisfied by round-41 text derived from the table, not by the
  retired literals.
- **Record stability across the tip**: `812ee0d` touches only `.ufo/evidence/round-41/census/end.exit`
  and `.ufo/waves/round-41/w1/ScribeScorecard.md` (`git show --stat 812ee0d`), and `0c8e1be` adds only
  the four confirmation receipts plus `census/end.stdout`; neither edits `SCORECARD.md` or `LOG.md`, so
  the text compared above is the text measured at `2ae00eb`.

## Residual risk and verification gaps

- A replay proves the numbers, never the execution time or authorship of the original run; nothing here
  can distinguish "the deciding run happened at `baa18b7b`" from "the receipts were produced later and
  labelled that way". The receipts' own `rev=` echo is not evidence of when they were made.
- C1 has no self-pin clause and no `records >= 1` gate (disclosed in the round's own limits); I verified
  the pin by hand above, and `records=3` at every revised commit, but a future runner gets no such
  guarantee from the counter.
- No measured class compares a round's prose claim to its own receipts, which is the class D1/D2 sit in;
  the counter will keep scoring `m6..m9 = 0` while this kind of contradiction recurs.
- m8 remains backtick- and prefix-scoped (`corpus/`, `tools/`, `.ufo/evidence/round-41/`,
  `.ufo/waves/round-41/`, plus seven exact root files): a path written in plain prose or under another
  prefix escapes. No instance this round (0 unbackticked candidates), so this is a standing gap, not a
  live miss.
- `--fleet` is accepted and never read (dead argument); harmless, but it advertises a cross-repo mode the
  counter does not implement.
