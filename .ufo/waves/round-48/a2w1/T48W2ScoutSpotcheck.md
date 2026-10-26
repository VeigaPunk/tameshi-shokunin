# T48W2ScoutSpotcheck — closure-style dry run (read-only; HEAD 17cc5ce, content c7586b9a)

All fetches live 2026-10-26 into scratch (since deleted). Nothing in the lane was written except this file.

## Spot-check 1 — ADMIT S266 (supersedes S048), plus S265 (S026) as a second admit
- Source re-opened live: https://pitest.org/quickstart/incremental_analysis/ → HTTP 200, 8892 B, sha256 `e9cbc3e1ab7c…` = the snapshot `freshness/sources/S048.html` and the receipt digest (byte-identical). `last-modified: Wed, 03 Jun 2026` matches the lesson's `2026-06-03`.
- Gate line `C2-QUOTE S266 S048` (21 tokens ≤25): after amendment-2 extraction (script/style dropped, tags stripped, unescape, whitespace collapsed) it is found exactly once, at offset 1013, in both the live fetch and the snapshot. It is the 4th `<li>` (raw line 86) of the `<ol>`, ending "(since 1.14.4)". Item 5 carries "(not yet implemented)", as the S266 row says.
- **AGREE (admit).** Reason: bytes unchanged, quote located whole, and it supplies the consequent ("prioritised above others") that round-45's dispute said the old quote dropped. The row does not resolve the "still kill it" pronoun, which matches the quote.
- S265/S026 (https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html): live HTTP 200, 236387 B, same size as the receipt but sha256 `dfea6b9b…` ≠ snapshot `a4c5c46b…`. `cmp -l` shows 97 differing bytes, all rotating Blogger tokens (`authorization.css?zx=…`, `widgets.js` build id, `__wavt`). The 15-token quote is found once at offset 2136 in both extractions; raw line 1132 holds "about 84% of the transitions we observe from pass to fail involve a flaky test!" and raw line 1082 holds "Friday, May 27, 2016". **AGREE**, with the caveat that a byte-identical live re-fetch is not available for this page; only the snapshot-plus-quote check can be reproduced.
- S267 (bwrap.xml v0.13.1): live raw bytes 33289 B, sha256 `2cb77df2f4be…` = snapshot. The quote is exactly 25 tokens, so it is at the limit and passes `<=25`. (I did not re-run the located-offset check for it.)

## Spot-check 2 — REJECT `r8-predictive-test-selection-cost.md` (re-stated)
- Reason claimed: the entry cites staged row S205 (arXiv 1810.05286), which the lane never opened.
- Re-check: `grep -c 1810.05286 corpus/SOURCES.md` → 0, and no `S205` row. The staged copy is `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/r8-predictive-test-selection-cost.md`, `source: S205 — https://arxiv.org/abs/1810.05286 … verified-at: 2026-10-24`. `merge/tameshi/SOURCES.append.md:59` carries S205 as a staged row.
- Live: https://arxiv.org/abs/1810.05286 → HTTP 200, title "[1810.05286] Predictive Test Selection"; the entry's recheck string ("reduces the total infrastructure cost of testing code changes by a factor of two") → count 1. The claim itself is true on the source.
- **AGREE (reject), narrowly.** The refusal is on QUALITY 10/2 (no lane-opened row, no committed snapshot), not on source truth. The flip condition ("a row opened mined in the writing round with a committed snapshot") is checkable. A judge may note that the live string is present, so the rejection is about provenance and not content. The lesson says so and withdraws the weaker `PROVINCE.md:14-18` reason (C1-R48-2).

## Pointer check (report-to-be)
| pointer | state at HEAD 17cc5ce |
|---|---|
| `freeze-2.json` | present. `calibration/measure.py` sha256 `572a5670…` and `freshness/measure.py` `faefe9b4…` both match my `sha256sum`; `control/run-controls.py` `f5732f18…` and `control/c2-controls.py` `46b8c039…` match; `contract.json` `4fff75db…` and `statements.json` `924102dc…` match |
| `.ufo/evidence/round-48/after/` | **absent** (the L1's deciding run has not landed; expected in a receipts-only commit) |
| `control/c2-controls.*` | present. `CONTROLS: F=0 G=0 H=2 expected=F0,G0,H<=2 ok=true`, exit 0 |
| `control/c1-controls.stdout` (CTL_A-E) | **absent**. QUALITY 95 (`corpus/QUALITY.md:1418`) and `quality/falsifiers.sh:33` cite it, and `quality/pointer-check-red-15b1521.stdout` shows it missing |
| `quality/c94-96-falsifiers.stdout` | **absent** (cited by criterion 94; same red file) |
| `selftest/c{1,2}-r48-selftest.*` | present |
| `calibration/emit-15b1521.*` | present, but it is the attempt-1 salvage revision: `unparsed=22 … fleet_drift=1 … C1_R48_PASS=false`, exit 1. It is not the attempt-2 emit |
| SOURCES rows | S265-S268 at `corpus/SOURCES.md:140-143`; S026/S048/S093/S108 rows unchanged (lines 37, 57, 102, 120), as the lesson says ("rows touched: none") |
| citing entries | `repeated-control-precondition.md`, `incremental-pin-disposition.md`, `regression-tally-completeness.md`, `r8-golden-update-flag.md` carry the new ids and `verified-at: 2026-10-26` on line 2 |

## What a closure judge would flag first
1. **The C1 control receipt is missing.** `control/c1-controls.stdout` is cited by QUALITY 95 and by the falsifier script but is not in the tree, and `quality/c94-96-falsifiers.stdout` is missing too. This repeats the "receipts cited before they existed" defect the lesson records as a mistake. Only the C2 controls (CTL_F/G/H) are committed. Until C1 CTL_A-E and the falsifier receipt land, the pre-registered C1 `cheapest_controls` have no receipt.
2. **`after/` is absent.** Neither `C1_R48_PASS` nor `C2_R48_PASS` has a deciding receipt at the content revision, so any "pass" in the report must come from the later receipts-only commit. The only C1 emit on disk is the attempt-1 `15b1521` one (`fleet_drift=1`, exit 1).
3. **Weaker byte reproducibility for S026.** A live re-fetch differs in sha256 (rotating tokens) though the size matches and the quote is located. This is disclosed for S108, not for S026. The quote check passes; the digest check does not.
4. The S267 quote is exactly 25 tokens. It passes, but it leaves no margin if the counter's tokenizer differs from `str.split`.

Installs/updates: none. Scratch dir `/fast/scratch/hyaku/tameshi-r48/T48W2ScoutSpotcheck` removed (see below).
