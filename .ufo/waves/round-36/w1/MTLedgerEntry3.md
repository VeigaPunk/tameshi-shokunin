# MTLedgerEntry3 — mutation probe: cold-read ledger refresh entry 3 (`corpus/README.md` drift)

Seat: mutation tester (leaf). Target claim: **C1** — the cold-read monitor refresh of the four
round-35-drifted SKILL headings restores calibration credit 6 → 8.
Probe authorised: scratch-copy the lane, edit ONE byte of the traced `corpus/README.md` content the
entry's inputs cite (after the trace was recorded), re-run the monitor; the entry must fail with
`input-drift:corpus/README.md`.

Lane state at probe time: `d9c496b19371b779ce0eec6dfee1b049b27a3a2d` (round-36 receipts).
Refresh commit `b455001e2589b3f4f471d94a3de7e5e549b9f54c`; its parent / every refreshed entry's
`read_rev` `e423c41ba253357ab8c8513f0376dad9d38ab248` (round-36 content commit).

Frozen inputs re-hashed before and after the probe; none was written:
`tools/tally-audit-v3.py` `6188db16de045f2927df2a0e667bc1539f4acfce5a1ac116e6de3107bf15d354`,
`tools/mutate-and-run.sh` `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`,
`round-36/c1/c1-measure-v2.py` `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53`,
`round-21/coldread/ledger.json` `29bddc03f957ef962a6e8d6192e96527e017d86d294d1944b07cb3263ba3bbbf`
(unchanged; also the blob at lane tip), `corpus/README.md` `7c0fe513ac1999d1c489d0c0e6b0aa57c648c8b2855d0e4a28fd617dcbc2619f`
(unchanged at lane tip).

## The entry under attack

Ledger entry **index 495** of 497 (`start` 1380–1395, heading
`### The map — where a reader enters, artifact by artifact`, section sha
`d4600d2f69f97bfd0e936fec1a15df0f82002fcc2138fa43ce2846c0eaee5517`), the third of the four L1
source re-anchor entries added in `b455001`. `read_rev` `e423c41b…`, `class` record,
`verdict` gap-minor, `commands_executed_count` 1, trace
`.ufo/evidence/round-36/coldread/traces/L1/source-3.json` (receipt schema
`tameshi-trace-inputs-v1`, README digest `7c0fe513…`). Recorded inputs (after the ignored
`SKILL.md`): `corpus/README.md` `7c0fe513…`, `corpus/knowledge/closeout-r11.md` `f0894bf6…`,
`tools/mutate-and-run.sh` `a7d3f2dd…`. It is the **sole crediting entry** for this section at the
pristine rev: the 12 older entries that carry the same section sha record older README digests and
already fail the input gate (they neither credit nor veto).

## Mutant

One byte, one file, post-trace, in an isolated clone — plausibility: the corpus README was edited
after the entry's trace receipt froze its digest, so the recorded binding no longer describes the
measured bytes.

- Location: `corpus/README.md`, byte offset **12644**, line
  `Fleet round-1 status: **local calibration correction retained; formal` — the byte `l` of
  `local` → `L`
  (`0x6c` → `0x4c`).
- Uniqueness: same length 46380 B before/after; exactly one differing offset asserted; README
  sha256 `7c0fe513…` → `51e6dfdf33bda045bda5ac9fcaa77682b590289e448dfb954fd47d54d4c86e43`;
  git blob `7c0fe5…`(= `9f1e4a944a5ae204478ce3a8349f531738828c9d` at `d9c496b`) →
  `02439700fbf12a2224396798d974cfa7df04ee2e` at the mutant rev. `git diff --numstat` = `1 1`.
- Commit (scratch clone only): `2d19a88aac90d3ba249e58f4631b5638f5aec246` on top of
  `d9c496b…`; `SKILL.md` untouched, so the measured section sha stays `d4600d2f…`.
- No mutating git command ran in the lane, fleet repo or any sibling; only the throwaway clone.

## Detector (frozen, unmodified)

`python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py`
— the round-21 selector over the frozen round-18 credit algorithm. Strict: no
`--ledger-file`/`--ledger-rev`/`--inputs-overlay` (the selector refuses those with exit 64), so
`overrides_used=false` and the claim-bearing input gate runs. The mutant bytes are supplied the
only way the claim reads them: as the blob at `REV`.

## Commands and outputs

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py \
  --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev d9c496b     # PRISTINE (cited command)
  exit 0 · revision d9c496b… · calibration 8 · 64/64 · reasons {"credited": 64}
  strict · overrides_used false · ledger_source rev · ledger_committed true
  JSON sha256 b2f493e0d9dbce3d22206f8e16090f58a3729268529c6ddbc637d1ef9feb925a

git clone --no-hardlinks <lane> /fast/scratch/hyaku/tameshi-r36-seats/MTLedgerEntry3/lane
  HEAD d9c496b… · clean · corpus/README.md 7c0fe513… (clone baseline JSON byte-equal to the above)

python3 <clone>/…/coldread/measure.py --repo /fast/…/MTLedgerEntry3/lane \
  --rev 2d19a88aac90d3ba249e58f4631b5638f5aec246                     # MUTANT
  exit 0 · revision 2d19a88… · calibration 6 · 61/64 · box3_full_page false
  reasons {"credited": 61, <three input-drift unions>: 3}
  missing: start 131, start 375, start 1380
  start 1380 reason includes input-drift:corpus/README.md

python3 <clone>/…/coldread/measure.py --repo /fast/…/MTLedgerEntry3/lane \
  --rev 2d19a88aac90d3ba249e58f4631b5638f5aec246 --explain            # MUTANT, per-entry
  section 1380: credited=false · vetoed=false ·
    explanation reasons (13 matched entries, ledger order, last = entry 495):
      input-drift:corpus/README.md
      input-drift:corpus/README.md;input-drift:corpus/knowledge/closeout-r11.md
      input-drift:corpus/README.md;input-drift:corpus/knowledge/closeout-r11.md;input-drift:tools/mutate-and-run.sh

python3 <same measure module>  # direct per-entry attribution of entry 495 (read-only)
  entry_reason(pristine d9c496b) = None            input_failures = []
  entry_reason(mutant 2d19a88)   = input-drift:corpus/README.md
  input_failures(mutant)         = ['input-drift:corpus/README.md']   (other 3 inputs still hold)

cp -p README.pristine lane/corpus/README.md ; git -C lane reset --hard -q d9c496b   # RESTORE
  HEAD d9c496b… · status clean · corpus/README.md sha256 7c0fe513… (exact pre-probe bytes)

python3 <clone>/…/coldread/measure.py --repo /fast/…/MTLedgerEntry3/lane --rev d9c496b   # RESTORED
  exit 0 · calibration 8 · 64/64 · reasons {"credited": 64}
  JSON byte-identical to pristine: sha256 b2f493e0…
```

Raw captures: `/fast/scratch/hyaku/tameshi-r36-seats/MTLedgerEntry3/{real-lane-pristine.json,
baseline.json,mutant.json,mutant-explain.json,restored.json,README.pristine}`.

## Verdict

**VERDICT: KILLED** — the assigned entry fails exactly as the claim requires. With one byte of
`corpus/README.md` changed after the trace was recorded, `entry_reason` for entry 495 flips
`None → input-drift:corpus/README.md` (single reason; its other three inputs still verify), the
section 1380 record becomes `credited=false`, and the monitor drops `calibration_restraint_score`
8 → 6 with coverage 64/64 → 61/64. Expected-under-dispatch, observed: **`input-drift:corpus/README.md`**.

Collateral, not a defect: the other two refreshed sections citing the same README digest
(`## Mutation-sweep recipe`, start 131; `## Restore discipline`, start 375) also lose their sole
crediting entry, which is why the score falls 8 → 6 rather than 8 → 7 — the monitor revokes box-3
full-page credit whenever any section is uncovered. The drift is attributed to the assigned entry
by exact per-entry `entry_reason`, not by reading the aggregated section string.

The probe confirms the C1 mechanism is real for entry 3: credit is input-keyed, not
trace-existence-keyed; a post-trace byte change in a cited input uncredits the section. It does not
test (and must not be read as testing) the truthfulness of `read_rev`, which the sibling entry-4
probe covers.

## Restoration evidence

- `corpus/README.md` restored from the pre-probe byte copy and re-verified at
  `7c0fe513ac1999d1c489d0c0e6b0aa57c648c8b2855d0e4a28fd617dcbc2619f` (46380 B), equal to the lane
  tip blob `9f1e4a94…`; `git reset --hard d9c496b` returned the clone to the pristine tip with a
  clean `git status --porcelain`.
- Restored detector run is byte-identical to the pristine run (same JSON sha256 `b2f493e0…`):
  calibration 8, 64/64, `{"credited": 64}`.
- Lane untouched throughout: HEAD still `d9c496b…`, ledger and README hashes unchanged, lane
  `git status` still only the pre-existing untracked `.ufo/waves/round-36/w1/`. The mutant commit
  lives only in the scratch clone. The only lane path created by this seat is this report.

## Tooling

None installed or upgraded; no `pacman`. Probe used the host `python3` and `git` already present.
Scratch root: `/fast/scratch/hyaku/tameshi-r36-seats/MTLedgerEntry3/` (clone + 5 JSON captures +
pristine README backup).

VERDICT: KILLED (entry-3 `corpus/README.md` one-byte drift → `input-drift:corpus/README.md`,
section uncredited, calibration 8 → 6; exact bytes restored)
