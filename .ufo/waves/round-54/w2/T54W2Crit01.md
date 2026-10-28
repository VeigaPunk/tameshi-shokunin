# T54W2Crit01 — C1 reader-arm attack (unchanged-section C0 read)

**Axes:** calibration / discernment (what arm4 actually proves).
**Verdict:** the frozen reader arm **cannot tell** a C0-only read from a read of the shipped C1 bytes when the section is byte-identical C0↔C1. Both arm4 predicates hold; `cannot_see` covers the fairness half of the gap.

## Axes named

1. **Arm4 bind strength** — does `cand == c0 ∧ section_sha256 == sha(section@REV)` prove the reader opened the shipped REV bytes?
2. **Counter observability** — can `c1/measure.py` distinguish that construction from a genuine REV read?
3. **Contract coverage** — does `claims.C1.cannot_see` already name this remainder?

## Construction (cheapest tree)

Fixture: `git clone --shared` → `$HYAKU_SCRATCH/tameshi-r54/T54W2Crit01/fixture`, checked out at **C1** `99c3bc88d704566197783f66b211ee0a830e0330`. No `SKILL.md` edit (receipt `forge-vs-c1.diffstat.txt`: only rekey marker + 7 reader JSON/MD).

1. Minimal `rekey-r54-59c38109bf11/traces/marker.json` so arm3 discovery resolves `c0 = 59c38109bf119d0e9d4f878644a82babc937bc1e` (ancestor of REV).
2. Seven `T54W2Crit01ReadNN.json` with `cand = C0` and `section_sha256 = sha at C1` (= sha at REV after the forge commit).
3. Forge commit **REV** = `b631ec7f0963f70000be9ee75e15f30ebc5f19f2`.

Of the seven frozen base-lost headings, **two are byte-identical C0↔C1** (receipt `section-shas-c0-vs-c1.txt`, `unchanged-byte-cmp.txt`):

| identical | heading | sha |
| --- | --- | --- |
| True | `### Round-14 historical registry — superseded by round 15` | `06a6864fb05f…` |
| True | `### Round-26 gate/probe registry — report interop` | `cc23587b353f…` |

Those two reports' MD state an open of C0 only and **never** C1 `SKILL.md` (`sample-read06-round14.md`). Their `section_sha256` is the hash of the C0 read; because the bytes did not change, it equals sha at REV.

## Assertion 1 — section bytes unchanged

```
$ python3 … # sectionize C0 vs C1 for the seven frozen headings
True  06a6864fb05f…  06a6864fb05f…  ### Round-14 historical registry — superseded by round 15
True  cc23587b353f…  cc23587b353f…  ### Round-26 gate/probe registry — report interop
# BYTE_EQ both True (len 1643 and 23083)
```

Receipt: `T54W2Crit01-receipts/section-shas-c0-vs-c1.txt`, `unchanged-byte-cmp.txt`.

## Assertion 2 — both arm4 predicates hold on a non-REV read

```
rekey_dirs=['rekey-r54-59c38109bf11']
c0=59c38109bf119d0e9d4f878644a82babc937bc1e
c0==C0_truth: True

HEADING ### Round-14 historical registry — superseded by round 15
  PREDICATE cand==c0: True
  PREDICATE section_sha256==sha_at_REV: True
  BOTH_ARMS: True
  md_claims_c0_only: True

HEADING ### Round-26 gate/probe registry — report interop
  PREDICATE cand==c0: True
  PREDICATE section_sha256==sha_at_REV: True
  BOTH_ARMS: True
  md_claims_c0_only: True

COUNTER_CAN_TELL: false
```

Receipt: `T54W2Crit01-receipts/arm4-unchanged-predicate.txt`.

Arm4 code (frozen `measure.py` sha256 `63f5f881…`):

```
if d.get('cand') == c0 and d.get('section_sha256') == sec['sha256']:
    reader_ok += 1
```

No open of REV is observed; `findings` is never consulted.

## Assertion 3 — frozen counter reports arm4-readers 7/7

```
$ python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-54/c1/measure.py \
    --lane $FIX --rev b631ec7f0963f70000be9ee75e15f30ebc5f19f2 \
    --work $S/work-measure --explain
EXPLAIN arm1-precheck exit=1 … cand_credited=41 lost=23 RED
EXPLAIN arm2-monitor exit=0 covered=41 score=6
EXPLAIN arm3-rekey dirs=['rekey-r54-59c38109bf11'] c0=59c38109bf119d0e9d4f878644a82babc937bc1e
EXPLAIN arm4-readers 7/7
C1_R54: rev=b631ec7f0963 c0=59c38109bf11 credited=41 lost=23 rekeyed=0/7 readers=7/7 monitor=6/41 unstable=0 total=3 C1_R54_PASS=false
```

Receipt: `T54W2Crit01-receipts/c1-counter-forge.stdout`.

Bare C1 control (no readers): `arm4-readers 0/7` — `c1-counter-c1-bare.stdout`.

Overall PASS is false (precheck/rekey not forged); **reader arm alone is green** on a tree whose unchanged-section reports never opened C1.

## Assertion 4 — live wave-1 readers already bind the same gap

Working-tree `T54W1Read16.json` / `T54W1Read23.json` (cand=`C0`, sha = C1 sha, findings non-empty) already satisfy both arm4 predicates at C1 for the two unchanged sections. Arm4 ignores findings. Receipt: `live-w1-unchanged-also-binds.txt`.

## Can the frozen counter tell?

**No.** Arm4 accepts any JSON with matching `cand`/`section_sha256`. When section bytes are stable C0→REV, a C0 read is observationally identical to a REV read under that predicate. The counter never checks that the reader opened `REV:SKILL.md`.

## Contract `cannot_see` (quoted)

> whether a reader's judgment of a section is fair, and whether a re-keyed entry's inputs are the ones the reader actually needed; the wave's adversarial re-reads and the L1's disclosed adjudications stand in for that

**Coverage:** YES for the fairness clause (hollow C0-only MD / no REV open is a judgment-fairness remainder the wave must catch). The identical-byte provenance gap is the mechanical form of that remainder for arm4: hash continuity ≠ proof of a shipped-byte read. Not a counter bug — declared procedural remainder.

## Smallest safe correction (do not edit the frozen counter)

Leave `c1/measure.py` alone. Before closure admit, L1/wave must reject (or explicitly adjudicate as hash-continuity-only) any empty-findings reader whose MD does not show an open of the deciding section bytes when the claim is that the shipped tree was re-read. For unchanged C0→C1 sections, disclose that arm4 only proves sha continuity, not a fresh C1 cold-read.

## Tooling

No installs. Used existing `python3`, `git`. pacman paused — nothing filed.

## Scratch

Work under `$HYAKU_SCRATCH/tameshi-r54/T54W2Crit01/` (fixture + receipts). Deliverables only under `.ufo/waves/round-54/w2/T54W2Crit01.md` and `T54W2Crit01-receipts/`.
