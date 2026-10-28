# T54W1Crit01 — C1 input-sufficiency attack

**Axes:** calibration (discernment/sufficiency of the re-read bind).
**Verdict:** the frozen C1 counter **passes** on a vacuous re-read tree; `cannot_see` **covers** this construction; the blind spot is real and live.

## Construction (strongest tree that is not a re-read)

Fixture: `git clone --shared` of the lane under `$HYAKU_SCRATCH/tameshi-r54/T54W1Crit01/fixture` (toplevel asserted before every mutating git call). Base = `d33053f7552d` (57/64). No `SKILL.md` edit.

1. Empty marker commit **c0** = `2f0d695654f108f38452417ced7f4536a57d1842`.
2. Content commit then collateral commit → **rev** = `c79ef005c0986a7d7b00f0a38afeafed34390b1c`.
3. For each of the seven frozen base-lost headings: one ledger entry + one `tameshi-trace-inputs-v1` receipt under `rekey-r54-2f0d695654f1/traces/`, plus one `T54W1Crit01ReadNN.json` with `findings: []` and a hollow `.md` that records `(no checks performed)`.
4. Every forged entry’s **only** recorded input is `.gitignore` (sha `0f699af0…`) — unrelated to section text, citations, or tools the section names.
5. Collateral: editing `ledger.json` drifted the previously-credited `### Round-21 gate/probe registry — finite environment differential`; one eighth vacuous `.gitignore` entry restored 64/64 without reading that section either.

Diff vs base touches only ledger, rekey traces, reader JSON/MD, and the c0 marker — **zero** `SKILL.md` bytes (receipt `forge-diffstat.txt`).

## Would the counter pass?

**YES.** Live run of the frozen counter (`c1/measure.py` sha `63f5f881…` per freeze):

```
$ python3 .ufo/evidence/round-54/c1/measure.py \
    --lane $S/fixture --rev c79ef005c0986a7d7b00f0a38afeafed34390b1c \
    --work $S/work-final --explain
EXPLAIN arm1-precheck exit=0 ... cand_credited=64 lost=0 ok
EXPLAIN arm2-monitor exit=0 covered=64 score=8
EXPLAIN arm3-rekey dirs=['rekey-r54-2f0d695654f1'] c0=2f0d695654f108f38452417ced7f4536a57d1842
EXPLAIN arm4-readers 7/7
C1_R54: rev=c79ef005c098 c0=2f0d695654f1 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
```

Base control (same counter, same fixture at `d33053f7552d`):

```
C1_R54: rev=d33053f7552d c0=none credited=57 lost=7 rekeyed=0/7 readers=0/7 monitor=6/57 unstable=0 total=4 C1_R54_PASS=false
```

Receipts: `T54W1Crit01-receipts/c1-counter-forged.stdout`, `c1-counter-base.stdout`.

## What the frozen contract cannot see

Quoted from `contract.json` claims.C1.`cannot_see`:

> whether a reader's judgment of a section is fair, and whether a re-keyed entry's inputs are the ones the reader actually needed; the wave's adversarial re-reads and the L1's disclosed adjudications stand in for that

**Does it cover this construction? YES — both clauses.**

| Blind spot in the construction | Covered by `cannot_see`? | What the counter actually checks |
| --- | --- | --- |
| Reader JSON has `findings: []`; hollow MD performs no opens/checks | yes — "reader's judgment … fair" | arm4: `heading` + `cand==c0` + `section_sha256` only (`measure.py:214-238`). Word `findings` never appears in the counter. |
| Entry inputs = one unrelated `.gitignore` blob | yes — "inputs are the ones the reader actually needed" | arm3: `entry_reason` verifies pin integrity (blob exists, sha matches, trace ⊆ inputs); never that the pin set is a re-read of the section. arm5 only bans `LOG.md`/`SCORECARD.md`. |

This is not a counter bug; it is the declared procedural remainder. The counter’s job is mechanical bind+credit. Sufficiency is delegated to wave adversarial re-reads and L1 adjudication — if those seats accept empty-findings / unrelated-input binds, C1 lights green on a non-re-read.

## Evidence that this is not a re-read

Sample forged entry (`## Standing rules`) — receipt `sample-forged-artifacts.txt`:

- `inputs: {".gitignore": "0f699af0…"}` only
- `class/verdict: record / verified-record`, `commands_executed_count: 1`
- trace argv `python3 -c pass` (no section open)
- reader: `{"findings": []}` + MD body `(no checks performed)`
- `SKILL.md` unchanged from base → section bytes never re-examined by a reader

Arm harness (mirrors amended measure.py directory-component discovery): `rekeyed=7/7 readers=7/7 unstable=0 ARMS_3_4_5_PASS True` — receipt `arm3-arm4-arm5-final.txt`.

## Smallest safe correction (do not touch the frozen counter)

Leave `c1/measure.py` alone (`cannot_see` already names this). Require, before closure admit:

1. L1/non-author reject of any rekey entry whose `inputs` view does not cite at least one path the section’s prose names (or an explicit "inputs-insufficient" adjudication), and
2. reject of reader reports whose MD shows no opened artifact when `findings` is empty.

Those are wave/adjudication duties the contract already points at; this seat shows they are load-bearing, not decorative.

## Tooling

No installs. Used existing `python3`, `git`. pacman paused — nothing filed.

## Scratch

Work tree `$HYAKU_SCRATCH/tameshi-r54/T54W1Crit01/` removed after receipt copy (see cleanup). Deliverables only under `.ufo/waves/round-54/w1/T54W1Crit01.md` and `T54W1Crit01-receipts/`.
