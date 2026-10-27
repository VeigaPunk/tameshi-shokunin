# T51W2ExecTool24 — C3 row audit: `tools/wave-parent-settle.py` (SKILL.md:2165)

Seat T51W2ExecTool24, round 51 wave 2 (falsify). Candidate
`6d8c11e378aa90b12650808e1b79270742935f15`. All runs in `git clone --shared` at CAND under
`/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool24/cand` (`git rev-parse --show-toplevel` =
that clone, HEAD = CAND), `TMPDIR` in scratch, stdin `/dev/null`. Raw receipts:
`T51W2ExecTool24/receipts.txt`. Nothing in the lane was written; no tool installed.

Row audited (verbatim cells, parsed to exactly 8 by the frozen counter's own `cells()`):

> `| wave parent settlement | gate | python3 tools/wave-parent-settle.py --receipt RECEIPT.json | 0 clean (SETTLED); 1 failed (UNSETTLED); 2 could-not-evaluate (usage, or --receipt not supplied) | python3 tools/wave-parent-settle.py --selftest → WAVE_PARENT_SELFTEST: 3/3 pass, exit 0 | .ufo/waves/round-40/settlement-receipt.json records SETTLED exit 0; .ufo/waves/round-41/settlement-receipt.json records UNSETTLED exit 1; red and green receipt literals live in the tool selftest | caller-chosen receipt is read only; verdict on stdout; nothing written, no TMPDIR use | tameshi |`

**Verdict: operative; no false claim in four of five checked fields.** Two mismatches
(F1, F2-F3 precision, F4) and one kind judgement (F5). The row is counter-coverable — I ran the
frozen counter's own parser on it, not a reimplementation.

## Measured: every positive field of the row is true

| Row field | Measurement | Result |
|---|---|---|
| self-test command (exact backticked bytes) | `python3 tools/wave-parent-settle.py --selftest` | exit 0, last line `WAVE_PARENT_SELFTEST: 3/3 pass`, 25-29 ms |
| usage probe | `… --r51-no-such-flag` | exit 2, stderr `error: unrecognized arguments: --r51-no-such-flag`; `2` is a standalone verdict-map token |
| exit 2 meaning "usage, or --receipt not supplied" | no args at all | exit 2, `usage:` on stderr (`tools/wave-parent-settle.py:72-74`) |
| pin round-40 "records SETTLED exit 0" | `--receipt .ufo/waves/round-40/settlement-receipt.json` | `WAVE_PARENT: verdict=SETTLED detail=parent exit >= last seat terminal`, exit 0; byte-identical to its committed sibling `.ufo/waves/round-40/settlement-receipt.stdout` |
| pin round-41 "records UNSETTLED exit 1" | `--receipt .ufo/waves/round-41/settlement-receipt.json` | `WAVE_PARENT: verdict=UNSETTLED detail=parent_exit_unix missing`, exit 1; identical to committed `.ufo/waves/round-41/settlement-receipt.stdout` (`… exit=1`) |
| "red and green receipt literals live in the tool selftest" | `tools/wave-parent-settle.py:37-47` | true (`red` 10/20, `green` 30/20+25, `none` 30/no-terminal) |
| write scope "nothing written, no TMPDIR use" | one `open()` in the whole tool. The only `open()` is the read at `:75`; `print` ×3; `sys.exit` ×1. After every run: `TMPDIR entries=0`, `git status --porcelain` empty | true |
| owner `tameshi` | row cell 8 | true |
| kind `gate` (not probe) | run mode exits 1 on a substantive condition (`:79`) | defensible, see F5 |

**The last-line marker is a real diagnostic, not author-chosen help text.** `:59` prints the
tally from the failed-comparison count, `:61` prints `FAIL …` per case, `:62` returns 1. Disabling
the rule at `:31` in a scratch copy yields `WAVE_PARENT_SELFTEST: 2/3 pass`,
`FAIL red: want UNSETTLED got SETTLED`, exit 1 — the marker moves with behaviour.

**The pinned values are load-bearing.** The round-40 receipt sits exactly on the inequality
boundary: `parent_exit_unix == max(terminal_unix) == 1792890156`, slack 0 seconds (64 seats). The
`<` → `<=` mutant of `tools/wave-parent-settle.py:31` keeps the selftest **green** (`3/3 pass`,
exit 0) and flips that pin to `UNSETTLED … parent exited before last seat terminal`, exit 1. So
the pin covers a hole the selftest cannot, and the row's `SETTLED` claim is a boundary claim, not
a slack claim. This tool is not the known clone-context red row (that is `round21-measure.py`); it
has no fixture dependency and its selftest is green straight from a `--shared` clone at CAND.

**Counter acceptance (its own code, not a reimplementation).** Importing
`.ufo/evidence/round-51/c3/measure.py` from the clone and calling `registry_rows` → 32 rows;
`row_reason(lane, CAND, 'tools/wave-parent-settle.py', <row at 2165>)` → `None` (no static
failure), returning argv `['python3','tools/wave-parent-settle.py','--selftest']` and usage argv
`[...,'--r51-no-such-flag']`; `tool_set` includes the tool, `deleted=[]`. Combined with the exits
above (`0` last line `WAVE_PARENT_SELFTEST: 3/3 pass`, usage `2` ∈ map) the row is covered.

## F1 — MISMATCH: exit 1 carries both `failed` and `could-not-evaluate`

The row maps `1` to `failed (UNSETTLED)`. The tool also exits 1 through uncaught tracebacks before
any verdict is printed (`:75-77`, the `:79` return never runs):

```
$ python3 tools/wave-parent-settle.py --receipt /nonexistent/x.json
FileNotFoundError: [Errno 2] No such file or directory: '/nonexistent/x.json'      exit=1
$ python3 tools/wave-parent-settle.py --receipt bad.json        # 'not json'
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)            exit=1
$ python3 tools/wave-parent-settle.py --receipt list.json       # '[1,2]'
AttributeError: 'list' object has no attribute 'get'                               exit=1
```

`PROTOCOL.md` §Gate standard (§Gate standard, Verdict bullet): *"`0` = `clean` and `1` = `failed`
fleet-wide; every other code a gate exits … is declared in its registry entry and mapped onto
`clean | failed | could-not-evaluate`."* An absent, unreadable or malformed receipt is not a graded
`failed`; it is `could-not-evaluate`. The row therefore declares the code but assigns the wrong
class to three reachable paths, and the standard's own fallback ("an undeclared nonzero code reads
as `could-not-evaluate`") cannot help because the code **is** declared. The lane's own precedent
splits them: `evidence-disposition` (SKILL.md:2146) maps *"missing, unreadable, malformed,
tampered or path-invalid input"* to `2 could-not-evaluate`, and `frozen registry replay`
(SKILL.md:2155) explicitly writes *"an uncaught traceback also exits 1"* rather than leaving the
reader to infer it. This row does neither.

Operability consequence: a settlement wrapper that grades `1` as `failed` records "the wave parent
did not settle" (a substantive round defect routed to an owner) when in fact the receipt was
missing or corrupt. There is no observable way to tell the two apart from the exit code, and the
`WAVE_PARENT:` stdout line is absent in the traceback case only by accident, not by contract.

## F2 — MISMATCH (precision): the row's own failure pin is an incomplete-record shape, not the round-38 shape

`tools/wave-parent-settle.py:2-6` says the tool exists to catch *"a parent that exits while seats
are still running … the round-38 failure shape"*. The row's failure pin does not exercise that
shape: the round-41 receipt has 40 seats with 40 **integer** `terminal_unix` values and
`parent_exit_unix: null`, so the replay takes the `not isinstance(parent_exit, int)` branch at
`:21-22` and reports `detail=parent_exit_unix missing`. The early-exit rule at `:31-32` is
evidenced only by the selftest's `red` literal. The row's sentence "records UNSETTLED exit 1" is
literally true (and matches the committed `.stdout`), so this is not a false claim — but the
two-evidence pair demonstrates *SETTLED* plus *record incomplete*, and the receipt it calls
`UNSETTLED` is precisely the `could-not-evaluate`-shaped input that F1 mislabels as `failed`.

## F3 — RESIDUAL: pinned values are undigested, and the lane already carries the drift this causes

Both pinned paths exist at CAND and replay to the stated verdicts, but the row pins no sha256 for
either. §Gate standard, Two evidences: *"A frozen baseline's `expected.json` MUST pin the digest of
every snapshot input file … an edited snapshot is `snapshot_tampered` (could-not-evaluate), not a
compared verdict."* Measured digests: `659e39bb7fba6d381ee3af27daec8b74a6542d861b8b4666b4d46d4ad44f89a3`
(round-40), `c9527fef19cb489670b4b632ad4909e0db1324f15e29975bb259f7ea8386c731` (round-41).
`659e39bb…` is pinned only outside this row, in `.ufo/evidence/round-50/integrate/overrides.json:12`;
`c9527fef…` appears nowhere in the lane. A hand-edit of either receipt silently falsifies the row's
"records SETTLED / UNSETTLED" text without any gate noticing, and the lane shows exactly this drift
already: `.ufo/waves/round-41/residual/ResidualReceipts.md:268` still quotes the round-41 run as
`WAVE_PARENT: verdict=UNSETTLED detail=no seats`, which the current receipt cannot produce — commit
`b14ff11` replaced the `no seats` shape with 40 seats and a null `parent_exit_unix`. The committed
sibling `.stdout` files are the stronger evidence the row could cite, and both agree with today's
replay.

## F4 — LOW: mixed arguments silently grade nothing

`--selftest --receipt <round-40 pin>` prints `WAVE_PARENT_SELFTEST: 3/3 pass` and exits 0, ignoring
the receipt (`:70-71`). The row does not mention it; `round-20 receipt-window measure`
(SKILL.md:2152) declares the mixed case as `2 could-not-evaluate`. A wrapper that passes both sees
exit 0 with no `WAVE_PARENT:` line — "clean" for a settlement that was never classified.

## F5 — JUDGEMENT: `gate` is defensible, but only on the "can fail" half of the standard

§Gate standard opens: *"A **gate** is a committed, re-runnable verdict script a lane owns: it reads
surfaces, compares them against expected values persisted in its own repo … A tool that cannot fail
is a **probe**."* Run mode can exit 1 on a substantive condition, so the tool is not disqualified
from `gate`; but nothing inside the tool compares against persisted expectations — the tool grades
the caller's receipt against its own fields, and the "expected values persisted in its own repo"
role is carried entirely by the row's two committed receipts. A reviewer applying the strict
reading could register it `probe` (the lane does exactly that for `pin-disposition`, whose exit 1
fires only in selftest). No observed behaviour contradicts `gate`; recorded so the L1 can rule on
it rather than inherit the label.

## Non-findings I checked and cleared

- Self-test cell: exactly one backticked command, no shell metacharacters (`;&|<>`$(){}\n` absent);
  first token of the last stdout line (`WAVE_PARENT_SELFTEST:`) appears in the cell.
- Pinned cell parses; every backticked path exists at CAND (`git cat-file -e` via the counter's
  `exists`); cell is not `none`.
- `-h` exits 0 (generic argparse; no settlement graded) — inherent to every row in this registry,
  not row-specific.
- The tool spawns nothing, reads no environment, opens no network, and does not mutate the clone.
- Blocker status: none. No shim or row repair performed, per the item.

## What the L1 should do

1. F1 is the only defect worth a row edit: split the exit-1 paths — either make input errors exit 2
   in the tool (out of wave-2 seat scope) or state in the verdict map that an unreadable or
   malformed receipt exits 1 via traceback and reads as `could-not-evaluate`. 2. Add the sha256 of
   both pinned receipts to the pinned cell (F3). 3. Declare the mixed `--selftest --receipt` case
   (F4). 4. Record F5's kind ruling. Row remains counter-coverable as written: `C3_R51_PASS` does
   not depend on any of these edits.
