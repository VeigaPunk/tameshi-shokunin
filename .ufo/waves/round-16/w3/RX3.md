# RX3 — cold-read re-read, SKILL.md:1302–1364

Page: `git show 05a224754db3c6fce18f5ec1816a6873bffe3d0e:SKILL.md`, sha256
`e289acec4e90c994d303b2dd6c844d907dc1bf48330ecd2fd253ac7379f794b3` (verified, exit 0).
Range: heading line 1302 (`### The six-leg regression — usage and this round's receipt`)
through the section body ending 1363; line 1364 is the blank before `## Final pointers`
(1365). Class chosen: **record** (a receipt), with its usage/reading-discipline statements
executed and re-checked as instructions.

## Revision resolution — the named pin is retrievable

`75ed934d…` is not a git object in the lane (`git cat-file -t 75ed934d` → "Not a valid
object name"), but it is the **sha256 of the tool blob later committed in `606716f`**:

```
git cat-file -p 606716f703f7699af458476a31fc78ddc9bf552c:tools/mutate-and-run.sh | sha256sum
→ 75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5
wc -l → 1642; line 157: VERSION='mutate-and-run.sh r10-2 (tameshi-shokunin, 2026-10-14)'
```

So every anchor and both receipts below were checked against the **exact revision the
section names**, not a surrogate. The governing page revision `05a224754` carries a later
tool with the *same* VERSION string: 1739 L, sha256 `0673d2e5…`, header line 81
"`--regression (r4-2; r7-1 leg ledger; r10-2 six legs; r16 seven)`", 7 registry entries.
The section's last bullet ("on a differing revision the tool bytes and the run you
executed govern") is the correct escape hatch for this; see the observations below.

Tools were run from /tmp copies staged at the depth `FLEET_ROOT` expects (`SELF`'s three
`dirname`s, line 1087 at this revision), with sibling repos symlinked read-only. No install
performed.

## Executions (commands, exits, key lines)

1. **Selftest at the named revision** — `bash /tmp/…/fleet2/tameshi-shokunin/tools/mutate-and-run.sh --selftest`
   → **rc 0**; `MUTATE_SELFTEST: 80/80 pass` / `VERDICT: PASS`. Exact receipt match.
   Its arms include the two the receipt cites:
   `PASS embedded leg specs: six files written`, six × `PASS embedded leg <name>: spec and
   recorded table agree`, and the exec-bit mirror trio
   (`PASS ledger leg: exec bit mirrored (self-exec gate runs)`,
   `PASS exec-bit leg pin line carries mode=100755`, `PASS exec-bit leg PASSes at the exact
   tolerance`) plus the red control `PASS no-exec leg refusal names the red control (exit=126)`.
2. **Regression at the named revision** — `--regression --workdir …/reg75` → **rc 0**;
   `REGRESSION: PASS (cases=6 passed=6; ledger legs exact: killed-delta<=0 flips<=0)`.
   Per leg: `match=10/10` for legs 1–4 and 6, `match=15/15` for leg 5; every leg
   `flips=0 inconclusive=0`; measured rates 8/10, 8/10, 6/10, 4/10, 7/15, 7/10 — exactly the
   section's table. `REGRESSION_EXPECT` lists the six rates; each of the six
   `REGRESSION_PIN` lines carries `mode=` beside repo/rev/path/sha256.
3. **Default scratch semantics** — regression with no `--workdir` → **rc 0**;
   `REGRESSION_WORKDIR: /tmp/tameshi-r4-2-regression.QWZhhd (removed on PASS; --keep
   retains)` and `test -d` → absent. With `--workdir` given the same run printed `(kept)`.
4. **Pins, independently** — six × `git show <rev>:<path> | sha256sum` at
   `175de6ba`, `fecee874`, `165307fe`, `eead56b2` (kagi twice, kumitate twice) all equal the
   recorded pins; modes `100644` (kimi), `100755` (surface, tsukuroi, mado, checklist, claims).
5. **The 25 `@old` claim** — spec strings decoded with the tool's own `unescape` grammar
   (`\n \t \r \\`): checklist 15 + claims 10 = **25**, every decoded string `count==1` in the
   materialized pinned bytes (TOTAL=25 bad=0).
6. **Supersessions / ledger** — at `cf41efaa` (blob in `9f1d3c3`) the tool is r7-1, 1341 L,
   4 registry calls, `nlegs=4`: the "four legs at this revision" state holds.
   `corpus/knowledge/fleet-kill-rate-ledger.md` at `05a224754`: lines 85–88 still read
   `**cases 1 and 2 only**` (pointing at `tools/mutate-and-run.sh:482-483`); ER-2 starts at
   272 and line 281 states the harness "carries **four** materialized legs"; there is no
   six-leg registry row. "No ledger cell is edited from here" holds at this revision.
7. **Runbook §7** (`corpus/knowledge/operator-runbook.md:345-407`, the only part read):
   it does render this command — same flags, same scratch/keep rules, same exit map,
   git-object-store bytes, receipt-reading discipline. It is the **four-leg** rendering
   (`cases=4`, `67/67` selftest at `cf41efaa`), i.e. a differing revision the section's own
   clause covers.
8. **Governing revision sanity** — at `05a224754`'s bytes: `--selftest` → rc 0,
   `MUTATE_SELFTEST: 83/83 pass` / `VERDICT: PASS`; `--regression --workdir` → rc 0,
   `REGRESSION: PASS (cases=7 passed=7; …)`, and the six legs the section names still replay
   exactly with the same rates. Leg 7 (`js-round-gate`) is additive; no named leg moved.

## Claim-cluster verdicts

| Cluster | Check | Result |
|---|---|---|
| tool pin / VERSION / length 1 642 L | sha256 + `wc -l` + line 164 | exact |
| six legs, table revs and rates | registry + six pin reads + replay | exact |
| `--regression` usage, scratch, exit map | help/code 115–119, 1089, 1166–1170; live runs | exact (0 observed, 2 arm in selftest) |
| git object store, pin equality, SETUP refusal | code 932–960; selftest arms | exact |
| mode mirror + checklist re-exec | code 939–959; selftest arms 1488+ | exact |
| receipt: selftest 80/80, rc 0 | re-run at 75ed934d | exact |
| receipt: six legs all exact, `cases=6`, rc 0 | re-run at 75ed934d | exact |
| `mode=` in PIN, six rates in EXPECT | re-run log | exact |
| 25 `@old` count==1 | decoded count check | exact |
| four legs at `cf41efaa`; ledger still stale; no cell edited | blob + ledger read | exact |
| runbook §7 renders the command | §7 read | exact (at its own revision) |
| line anchors `:90-97`, `:104-106`, `:115-119`, `:932-960`, `:766`, `:841`, `:1132-1141`, `:1488-1527` | line-by-line at 75ed934d | mostly exact; see minor gaps |

## Findings

**Blocking: none.** The behavioral receipt is reproduced exactly; no wrong expectation was
found at the revision the section names.

**Minor (4) — line-anchor precision at `75ed934d`, not behavioral error:**

1. `list tools/mutate-and-run.sh:85-89` — the six leg rows are **84–89**; line 85 is
   `bash-surface-census`, so the quoted range omits row 1, `js-kimi-census` (line 84), while
   the sentence says "six".
2. `pins/tables :550-559` — that range holds `PIN_CHECKLIST`/`REV_CHECKLIST`/
   `PIN_CLAIMS`/`REV_CLAIMS` (550–553) and all six `TABLE_*` lines (554–559). The other four
   pins are **542–549** (`PIN_JS` 542, `REV_JS` 543, `PIN_BASH` 544, `REV_BASH` 545,
   `PIN_TSUKUROI` 546, `REV_TSUKUROI` 547, `PIN_MADO` 548, `REV_MADO` 549). A reader sent to
   :550 for "pins" sees only 2 of 6.
3. `registry :1132-1141` — that range holds only the `bash-checklist-run` (1132) and
   `js-claims-check` (1137) registrations through `st_claims` (1141); the six-entry registry
   begins at **1112**.
4. `added selftest arms at :1488-1527 cover the mirror` — 1488–1527 is the positive self-exec
   arm and its three assertions; the `100644` counter-arm begins at **1529**. Both arms pass
   in the 80/80 run, but the cited range names half of the stated coverage.

**Observation (not a gap):** at the governing revision `05a224754` the present-tense
"`REGRESSION_EXPECT` lists six recorded rates" is superseded by seven, and selftest is
83/83; at the named revision it is exactly six/80. The section's differing-revision clause
and the tool's own `r16 seven` header make this honest rather than misleading.

## Residual risk / verification gaps

- The named revision survives only as the `606716f` blob (sha256-verified). The receipt's
  historical scratch `/tmp/w10-t10-4-ev` is gone, so the lane's 21:02:39Z run and the owner's
  21:00:24Z run are verified by **reproduction**, not by their original logs.
- `SKILL.md:925-1008` cross-references (round-7 "four legs", round-9 `cases=4` and the
  caveat, the reading discipline) were **not opened**, per the cold-read interface; the
  round-11 heading after 1365 was not opened either.
- Exit 1 (FAIL) was not exercised live; the comparator arms of `--selftest` cover the FAIL
  band, and the code prints `REGRESSION_DEFECT` rows for differences.
- No tools installed or upgraded during this seat.

**One-line verdict:** at the named revision the receipt reproduces exactly — `80/80` selftest
and `cases=6 passed=6`, every match row exact, rc 0 — with only four narrow line-anchor
imprecisions in the section itself; minor.

```json
{"seat":"RX3","skill_sha256":"e289acec4e90c994d303b2dd6c844d907dc1bf48330ecd2fd253ac7379f794b3","sections":[{"start":1302,"heading":"### The six-leg regression — usage and this round's receipt","class":"record","verdict":"gap-minor","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["list anchor :85-89 omits the first of six leg rows: the rows are 84-89 at 75ed934d; line 85 is bash-surface-census","pins/tables anchor :550-559 starts mid-block: it holds PIN_CHECKLIST..REV_CLAIMS (550-553) plus the six TABLE_* lines; PIN_JS..REV_MADO are at 542-549","registry anchor :1132-1141 holds only the last two registrations (bash-checklist-run 1132, js-claims-check 1137) through st_claims 1141; the registry begins at 1112","selftest-arms anchor :1488-1527 covers the positive self-exec arm and assertions; the 100644 counter-arm begins at 1529"],"commands_executed":["git show 05a224754:SKILL.md | sha256sum -> e289acec4e90c9... (exit 0)","git cat-file -p 606716f:tools/mutate-and-run.sh | sha256sum -> 75ed934dc863... , 1642 L, VERSION r10-2","six x git show <rev>:<path> | sha256sum -> all six pins match; modes 100644/100755","staged /tmp copy at <scratch>/fleet/tameshi-shokunin/tools/ for FLEET_ROOT depth","--selftest at 75ed934d -> rc 0, MUTATE_SELFTEST: 80/80 pass, VERDICT: PASS","--regression --workdir at 75ed934d -> rc 0, cases=6 passed=6, match=10/10 x5 + 15/15, flips=0 inconclusive=0","--regression default scratch at 75ed934d -> rc 0, /tmp/tameshi-r4-2-regression.QWZhhd (removed on PASS; --keep retains), dir absent","--selftest at governing 05a224754 -> rc 0, 83/83 pass","--regression --workdir at 05a224754 -> rc 0, cases=7 passed=7; six named legs still exact","python3 decoded @old check against materialized pinned blobs -> TOTAL=25 bad=0","git show 05a224754:corpus/knowledge/fleet-kill-rate-ledger.md (lines 80-95, 272-290, ER headings)","git show 05a224754:corpus/knowledge/operator-runbook.md:345-407 (section 7 only)","git cat-file -p 9f1d3c3:tools/mutate-and-run.sh -> sha256 cf41efaa..., nlegs=4"],"opened":["05a224754:SKILL.md:1302-1364","05a224754:tools/mutate-and-run.sh (1739 L; run)","606716f:tools/mutate-and-run.sh = 75ed934d (1642 L; anchors + run)","9f1d3c3:tools/mutate-and-run.sh = cf41efaa (four-leg check)","05a224754:corpus/knowledge/fleet-kill-rate-ledger.md:80-95,272-290 and ER headings","05a224754:corpus/knowledge/operator-runbook.md:345-407 (section 7)","six pinned sibling blobs at their recorded revisions (pin/mode check)"],"scratch":"/tmp/tameshi-r16w2-RX3-48jlQk"}]}
```
