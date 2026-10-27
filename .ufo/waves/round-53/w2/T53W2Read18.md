# T53W2Read18 — re-read of `### The six-leg regression — usage and this round's receipt`

Seat T53W2Read18 (lane repo `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, wave 2 of round 53).
Section read at content commit **C\*\* = `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e`** via git objects only
(`git -C <lane> cat-file -p C**:SKILL.md`); the working tree was never the source of the bytes.

- heading: `### The six-leg regression — usage and this round's receipt`
- section span at C\*\*: 1-based lines **1317–1380** (63 lines); previous heading
  `### The operator's runbook — `corpus/knowledge/operator-runbook.md`` ends at 1316; next heading
  `## Final pointers — the standing map at the arc's close (round 11, measured)` starts at 1381
- last body line (trailing whitespace-only lines stripped): ``  measured at `r10-2`, and no ledger cell is edited from here.`
- `section_sha256` = **`17e7a20c11cfba208ae2f89165020fe0e6760dd8898e42bdddff62cff0748829`** (4 566 bytes; 64 sections at C\*\*)

## Split verification (before hashing)

| # | check | outcome |
|---|---|---|
| 1 | frozen splitter `.ufo/evidence/round-18/measure.py:sectionize`, loaded with `importlib` and `sys.dont_write_bytecode = True` (never reimplemented for the recorded hash) | unique match `start=1317 end=1380`, `sha256=17e7a20c…`; 64 sections |
| 2 | independent reimplementation of the same rule (`^#{1,3}(\s\|$)` outside `line.strip().startswith('```')` fences, strip trailing whitespace-only lines, join `\n`, no trailing newline, `surrogateescape`) | same span 1317–1380, same `17e7a20c…`; the two agree |

## Wave-1 fix verification (run first)

Wave-1 reader `T53W1Read25` filed two findings at C\* (`45fe934f…`): the round-7 cross-quote
("Four legs at this revision" + the assertion "the section now reads \"that revision\"") described bytes
that no longer existed, and the round-9 caveat was quoted/cited at lines that no longer carried it.
The item says the applied fix was "Four-legs cross-quote updated to the section current wording".

| fix | verification at C\*\* | outcome |
|---|---|---|
| F1 wording: the quote is now the section's current wording | `Round 7 recorded four legs at` + `r7-1 (dated milestones: …)` is present verbatim at C\*\* lines **928–929**; the phrase "that revision" no longer appears in this bullet | **wording VERIFIED**, but the parenthetical's anchor regressed with the fix → **F1 below** |
| F1 anchor: `:925-929` → `:923-927` | `sed -n '923,927p'` prints a blank, the round-7 heading, a blank, and the unrelated "Round 7 turns … / fleet's **leg ledger** …" sentence; the quoted words are at 928–930 | **FAILS** → **F1 below** |
| F2: caveat quote `"still not embedded — named debt"` + anchor `:1226-1228` replaced by `"named debt"` + prose pointer | `"named debt"` is present at C\*\* line 1235 (`line at this boundary — named debt, not smoothed`); no false anchor is attached to it; `ER-4` caveat (a) exists at `fleet-kill-rate-ledger.md:350` and says the tool "embeds **4** legs — cases 5/6 … carry no `REGRESSION` line at `cf41efaa…`" | **VERIFIED** |
| F2 residual: the surviving `cases=4` anchor `:1218-1222` | `cases=4` is at C\*\* line **1227**; 1218–1222 is blank / `### The receipt at this boundary` / blank / the receipt preamble | **FAILS** → **F2 below** |

## Checks run

| # | check | outcome |
|---|---|---|
| 1 | frozen split + independent split (above) | span 1317–1380, `17e7a20c…`, 64 sections |
| 2 | `git ls-tree` of `tools/mutate-and-run.sh` at CAND0 `bcba8924`, C\* `a41195d`, C\*\* | all three: mode `100755`, blob `51fa5bc8ac2c863ec754ac87a1e3227a18c79d67`; extracted bytes 2 159 lines, sha256 `977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda` — the tool anchors are the same bytes at every revision the section names |
| 3 | `git diff --stat C* C** -- tools/` | the 7 C2-patched tools only; `mutate-and-run.sh` untouched |
| 4 | every tool anchor the section carries, read at C\*\* | `:88-97` ten leg lines · `:98-121` sources + `@old` notes · `:614-643` `PIN_*`/`REV_*` (614–633) and `TABLE_*` (634–643) · `:850` leg-5 spec head · `:925` leg-6 spec head · `:128-130` + `:1281-1302` exec-bit mirror · `:139-143` exit map · `:1446` `REGRESSION_EXPECT` printf · `:1459-1507` ten `regression_case_git` dispatches · `:2024` "embedded leg specs: ten files written" — **all resolve** |
| 5 | recount the six-row table against `PIN_*`/`REV_*`/`TABLE_*` at C\*\* | 8/10 (js-kimi, `175de6ba`), 8/10 (surface, `fecee874`), 6/10 (tsukuroi, `165307fe`), 4/10 (mado, `eead56b2`), 7/15 (checklist, `fecee874`), 7/10 (claims, `175de6ba`) — every rev and rate agrees |
| 6 | command / scratch / lifecycle | `:1432` `root=$(mktemp -d "${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX")`; `--workdir` sets `auto=0` (`:1434-1436`); PASS+auto+no-`--keep` removes (`:1542-1544`), FAIL keeps (`:1522`), SETUP keeps (`:1528`); usage `:206` |
| 7 | `@old` count claim ("their 25 `@old` strings") | leg-5 heredoc (854–924) 15 `@old` + leg-6 heredoc (929–972) 10 `@old` = **25**; the 16th grep hit inside 929–972 is line 931, a comment naming `@old`, not a directive |
| 8 | ledger anchors at C\*\* (`corpus/knowledge/fleet-kill-rate-ledger.md`, 441 L) | `:85-88` "Embedding status … **cases 1 and 2 only**"; `:272` ER-2 heading, `:281` "carries **four** materialized legs"; `grep -nE 'six-leg\|ten-leg\|ten legs\|leg registry'` over the ledger returns **nothing** (no registry row) |
| 9 | runbook at C\*\* | `## 7. The regression mode — replaying the recorded legs` at `:345`; `:374-375` "four legs at this revision (cases 1–4); cases 5/6 are **not embedded** — named debt, tool owner's call" |
| 10 | dated-receipt corroboration | `plans/round-10-record-draft.md:339-340` names `/tmp/w10-t10-4-ev/` with `selftest.log` 80/80 · `regression.log` 21:02:39Z · `tool-at-run.txt`; `:90-92` the closing `PASS (cases=6 passed=6; ledger legs exact: killed-delta<=0 flips<=0)` with T10-2 21:00:24Z; `corpus/knowledge/closeout-r11.md:69` `75ed934dc86360f5…` (r10-2, 1 642 L; committed at `606716f`), `:309` "`--selftest` 80/80 — T10-2 21:00:24Z" |
| 11 | `:965-1008` ("Reading a receipt stays the round-7 discipline") | the discipline section `### Reading a receipt — the discipline` starts at 970 and its items 1–7 run 972–1013; the cited range lands inside it (read the block / PASS exact / FAIL rows / SETUP not a verdict) |
| 12 | `:923-927` and `:1218-1222` at C\*\* (the two cited anchors) | both **miss their quoted content** — see findings; the same two anchors resolve at C\* (925-926, 1222) and at CAND0 (925, 1220), so both are drift, not invention |

## Holds (C\*\* bytes)

- **"`--regression` replays six in r10-2 (ten since round 51)"** — the tool comment `:84` reads
  `--regression (r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven; r18 eight; r26 nine; r51 ten)`; the leg list
  `:88-97` carries ten lines; the dispatch block `:1459-1507` carries ten calls; `nlegs=10` at `:1510`.
- **Header anchors** — `list :88-97`, `sources :98-121`, `pins/tables :614-643`, `specs :850`/`:925`,
  `registry :1459-1507` all land on the objects described; "line anchors re-read at CAND0 `bcba8924…`, the sha
  governs" is true for the same reason as check 2 (identical blob at CAND0/C\*/C\*\*).
- **Six-row table** — all six recorded revisions and rates match the pinned constants and the tables (check 5);
  `match=15/15` holds because `TABLE_CHECKLIST` has 15 entries while the other five tables have 10.
- **Command / default scratch / exit map** — section text matches the tool byte-for-byte (check 6); "TMPDIR
  honoured since r51" is the comment block's own annotation at `:148-150` (`` Scratch root: mktemp -d `` /
  `# "${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX" by default (r51 honours` / `# TMPDIR)`) and the code at
  `:1432`.
- **Exec-bit mirror** — `:128-130` states the rule, `:1281-1302` implements it and `:1302` prints `mode=` on
  every `REGRESSION_PIN`; the selftest arms at `:1860-1896` exercise the mirror and its 100644 control.
- **`REGRESSION_EXPECT` / "ten at CAND0, `:1446`"** — `:1446` is the printf with ten rate arguments; "six at
  r10-2" is the dated leg count, reconciled inline with "(ten at CAND0)".
- **`"named debt"` bullet** — quote resolves at 1235; `ER-4` caveat (a) (`ledger:350`) and the absense of any
  ledger registry row (check 8) both support "a ledger row recording the … registry is the ledger owner's
  follow-on"; `fleet-kill-rate-ledger.md:85-88` and `:281` read exactly as quoted.
- **25 `@old` strings** — 15 + 10 (check 7), matching the tool's own note at `:114-121`.
- **The 2026-10-14T21:02:39Z receipt** (`80/80`, six legs, `cases=6 passed=6`, `mode=` pins, scratch
  `/tmp/w10-t10-4-ev/`) is a **dated** execution record, corroborated by the round-10 record draft and the
  round-11 closeout (check 10). Dated historical receipt → HOLD, not a scratch-directive violation (the
  host directive is dated 2026-10-25; the receipt is 2026-10-14 and the workdir is named as kept evidence).
- **"uncommitted worktree file at this write" / "1 642 L"** describes the r10-2 revision `75ed934d…` at the
  time this section was written (`closeout-r11.md:69` records the same 1 642 L and the later commit
  `606716f`); it is a date-bound parenthetical, not a claim about the C\*\* tree (where the tool is the
  committed blob `51fa5bc8`, 2 159 L).
- **Runbook §7 rendered "as of round 10 (four legs then; the tool embeds ten since round 51)"** — runbook `:374`
  still reads four legs, and the section labels it as the round-10 rendering.

## Findings (2)

### F1 — the round-7 cross-quote's anchor does not contain the quoted sentence at C\*\*

Verbatim from the section at C\*\*:

```
recorded four legs at r7-1" (`:923-927`; dated milestones there since round 16)
```

**What the skill asserts.** The round-7 quotation "Round 7 recorded four legs at r7-1" — and the dated
milestones "there since round 16" — are at SKILL.md:923-927.

**Why it fails at C\*\*.** `sed -n '923,927p'` on the C\*\* blob prints, verbatim:

```
## The leg ledger — replay, receipt, and how it is read (round 7, measured)

Round 7 turns `--regression` from the tool's two-case self-check into the
fleet's **leg ledger**: every recorded mutation case is a leg of this ledger,
```

(surrounded by blank lines 923 and 925). The quoted sentence is at **928–930**:

```
replayed at its pinned original revision. Round 7 recorded four legs at
r7-1 (dated milestones: seven from round 16, eight from round 18, nine from
round 26, ten from round 51) — `js-kimi-census`
```

`grep -n 'Round 7 recorded four legs'` at C\*\* returns only line 928; `grep -n 'dated milestones: seven from
round 16'` returns only 929. The anchor therefore cites lines whose quoted content is absent.

**Provenance.** Wave 1 already flagged the *wording* and the L1 fixed it, but the fix also moved the anchor
`925-929` → `923-927`, i.e. five lines above the words the fix put there. The value 923-927 is exactly the
"Snapshot line" cell of this page's own round-16 repair row (`SKILL.md:1751`:
`| 923-927 | "Round 7 recorded four legs at r7-1" | dated: four at r7-1, seven since round 16 | CR16 |`), so
the snapshot anchor was reused as a live one. At C\* the old anchor `:925-929` did contain the sentence
(925-926); at CAND0 `:923-927` did contain the older wording (line 925: `pinned original revision. Four legs
at that revision (r7-1; …)`). The page's own rule at `SKILL.md:1736-1737` is that "every `SKILL.md:<line>`
self-anchor still resolves". Class: stale anchor (introduced by the wave-1 fix).

### F2 — the round-9 receipt's `cases=4` is cited five lines before it sits at C\*\*

Verbatim from the section at C\*\*:

```
the round-9 receipt's `cases=4`
  (`:1218-1222`)
```

**Why it fails at C\*\*.** Those lines present the range as the home of the round-9 receipt's closing
`REGRESSION: PASS (cases=4 passed=4; …)`. At C\*\*, `sed -n '1218,1222p'` prints:

```
### The receipt at this boundary

Run at the tick (this lane; `--selftest` 19:58:49Z, `--regression`
`REGRESSION_DATE 2026-10-14T19:58:59Z`; logs `/tmp/w9-tameshi-t93/selftest.txt`,
```

— a blank, the heading, a blank, and the receipt preamble. `cases=4` at C\*\* is at line **1227**
(`  closing \`REGRESSION: PASS (cases=4 passed=4; ledger legs exact:`), with the leg counts at 1226 and the
rest of the closing line at 1228-1229. `grep -n 'cases=4'` at C\*\* returns 983, 1094, 1227, 1361 (this
section's own citation line) and 1752 (the round-16 repair row `| 949-950 | receipt literal \`cases=4\` |`);
none is inside 1218-1222.

**Provenance.** This anchor was correct at CAND0 (`cases=4` at 1220) and at C\* (`cases=4` at 1222) and
drifted by +5 lines when this round's fix pass inserted five lines above it, without a rebase. The
neighbouring caveat citation was repaired to a prose pointer (verified above), but this one was left as an
absolute line range. Class: stale anchor (drift left by the fix pass).

## Calibration notes

- Both findings are anchor-only: the section's quarantine-period prose, its six-row table, its tool anchors,
  its counts and its dated receipt all hold at C\*\* (checks 4–12). Neither finding disputes a historical
  record; both concern pointers presented as live.
- I did not raise a finding against the heading's "six-leg" title, the "six in r10-2 (ten since round 51)"
  reconciliation, the "uncommitted worktree file at this write" parenthetical, or the `/tmp/w10-t10-4-ev/`
  scratch: all four are date-bound history, and the page reconciles the count inline.
- The round-16 repair row at `SKILL.md:1751` carries the same 923-927 value as a *snapshot* line; that row is
  outside this section and is named here only as the likely source of F1, not filed as a finding of this seat.

## Not claimed / out of scope

- The dated receipt (2026-10-14T21:02:39Z, `80/80`, `cases=6 passed=6`, `mode=` pins, the owner's 21:00:24Z
  run) was **not re-executed**; it is corroborated by committed records (check 10) and contradicted by no
  C\*\* byte. No present-tense numeric claim depends on a re-run.
- Nothing under `tools/`, `corpus/`, `SKILL.md` or `.ufo/evidence/` was edited; no mutant was cut (this seat
  is a re-read seat). No git/jj mutating command ran anywhere — only `cat-file`, `ls-tree`, `diff --stat`,
  `show`-equivalents through `cat-file`.
- The C1 credit decision belongs to the L1 counter; this report claims only the section bytes, the hash, and
  two evidenced anchor findings.

## Tooling and scratch

- No tool installed or upgraded (nothing needed; git + python3 sufficed). No `pacman` invocation.
- Scratch: `/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read18/` (SKILL.md at C\*/C\*\*/CAND0, section bytes,
  split script, `tools/mutate-and-run.sh` at C\*\*, ledger/runbook/closeout/plan copies) — deleted before
  yielding. No file written outside `.ufo/waves/round-53/w2/` and that scratch dir; `/tmp` unused.
