# B15Lesson17Corrections — append-only correction for `corpus/lessons/round-17.md`

Seat: TameshiR18.B15Lesson17Corrections (scribe-class, leaf; no dispatch). Base pinned at `183f87b899e6cae46be98d251cbc87fb5118f6ca`.
Owned write: `.ufo/waves/round-18/staged/corpus/lessons/round-17.md` (staged full file = base + appended block).
Tools installed or updated: none.

## Behaviour

Appended one block after the base's last line (base 96 lines, staged 106 lines). No earlier line was edited.

Verification of the staged bytes:

```
cmp -n 12705 <base-r17.md> <staged>            -> PREFIX-CMP-OK (12705 bytes)
diff <base-r17.md> <staged>                    -> "96a97,106" (one addition, zero "<" lines)
head -n 96 <staged> | cmp -s - <base-r17.md>   -> HEAD96-EQ
wc -l <staged>                                 -> 106; final byte \n
```

The three corrections, each checked against bytes at the base rev:

1. **G5 (line 22) "K02 holes 1–4 … closed … (89/89 selftest)" overstates the closure.**
   - Holes 3 and 4 are closed: `OVERLAY_FIELDS` (measure.py:134), `overlay-field-forbidden` selftest (measure.py:1358), `cat_file_blob` via `git cat-file blob` (measure.py:182–184).
   - The zero-command part of hole 2 is closed: `commands-unrecorded` (measure.py:517).
   - The input-to-trace part of hole 1 is closed: `trace_reason` (measure.py:368–426) raises `trace-input-unrecorded`, `trace-input-drift`, `live-lane-read`.
   - Still open (command binding, K02 fix items 1 and 2): `trace_reason` never reads a receipt's `argv` or `rev`. `grep -n "'argv'"` on measure.py at base gives only the selftest fixture (line 773). No `commands-unbound` or `class-mismatch` reason exists. `coldread/bucket-commands.json` is read by neither measure.py nor assemble.py.
   - Corroborated by spot-check §5 G5 row (`corpus/lessons/round-17-verifier-spotcheck.md:324`) and §7 item 2 (lines 423–427).
   - The "record with commands>0 still credits" consequence is [INFERENCE from the code path, not run]; the block marks it so.
2. **G7 (line 24) pointer "K02 hole 5" should read "K02 hole 7".** Confirmed in `.ufo/waves/round-17/w1/K02InputCreditHoles.md`: hole 5 = reads of the live lane from a clone run; hole 7 = over-invalidation by the page itself (SKILL.md in every seat's inputs). Spot-check §5 G7 row (line 327) agrees.
3. **G5 (line 22) tally "89/89".** 89 is the W2 receipt at eb7838b: `.ufo/waves/round-17/w2/NoHarmSelftests.md:57` (`MEASURE_SELFTEST: 89/89 pass`); `git show eb7838b:.ufo/evidence/round-17/measure.py | sha256sum` → `f348adc3…`, matching the receipt's NEW row. The final measure at 183f87b has sha256 prefix `d25d3d04`, and its selftest was run in a clone (below) → `MEASURE_SELFTEST: 94/94 pass`, exit 0. Spot-check §4 table (line 306) records `round-17 measure | 94/94 | d25d3d04`. Versioned receipts for different bytes; not interchangeable.

## Commands run (all in scratch; lane never written)

| Command (abbrev.) | Exit | Key output |
|---|---|---|
| `git show 183f87b:corpus/lessons/round-17.md \| wc -c` | 0 | 12705 |
| `git show 183f87b:.ufo/evidence/round-17/measure.py \| sha256sum` | 0 | `d25d3d04…` |
| `git show eb7838b:.ufo/evidence/round-17/measure.py \| sha256sum` | 0 | `f348adc3…` |
| `git clone -q <lane> $W/fleet/tameshi-shokunin` with GIT_* unset; `git checkout -q 183f87b…` (read of lane, clone is /tmp) | 0 | HEAD = 183f87b |
| `env -u GIT_* GIT_CONFIG_GLOBAL=/dev/null python3 .ufo/evidence/round-17/measure.py --selftest` (in the clone) | 0 | `MEASURE_SELFTEST: 94/94 pass` |
| `grep -n` on measure.py / assemble.py for argv, bucket-commands, commands-unbound, class-mismatch | 0 / 1 (no matches for last four) | see item 1 |

Scratch: `/tmp/tameshi-r18w1-B15Lesson17Corrections-cgm5gD/` (clone under `fleet/`, copies of base and measure.py). Git writes: none in the lane or any sibling. Symlinks created only inside the scratch fleet mirror.

## Gate and scope notes

- The G5 row's decision (admit) is not rewritten; the block narrows its stated reason only, and says so in its last line.
- Earlier lines were not touched. The spot-check's own "not a mechanical proof" bound (§3 "Bound", §5) is cited, not re-argued.
- The block cites only observed bytes. Nothing was re-run for the corrections other than the one selftest above.

## Routed to L1

- The staged file is ready to install. L1 owns installation; the seat did not edit the live `corpus/lessons/round-17.md`.
- R17-CMD-BIND remains open in code (see item 1). This block records it; it does not close it.

## Verdict

built — staged file = base + one appended 10-line block (`96a97,106`), with three exact-line corrections verified at 183f87b.
