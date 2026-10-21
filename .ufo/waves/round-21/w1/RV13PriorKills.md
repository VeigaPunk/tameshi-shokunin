done

# Findings

**No C1 survivor was already closed by the frozen round-20 baseline.** All 18 frozen IDs are `SURVIVED` at `08175c62d661fddf052ed10abc91313dec8eb77d`: killed=0, survived=18, inconclusive=0, and all four pristine selftests exit 0. The stored ruler exit is 1 because its contract returns 1 when any mutant is not killed; it is a complete measurement, not an inconclusive/setup failure.

| ID | Owning tool | Status at baseline | Evidence |
|---|---|---|---|
| MB03 | `tools/bash-witness-study.py` | SURVIVED | `c1-before.stderr:1` |
| MB04 | `tools/bash-witness-study.py` | SURVIVED | `c1-before.stderr:2` |
| MB05 | `tools/bash-witness-study.py` | SURVIVED | `c1-before.stderr:3` |
| MB06 | `tools/bash-witness-study.py` | SURVIVED | `c1-before.stderr:4` |
| MB07 | `tools/bash-witness-study.py` | SURVIVED | `c1-before.stderr:5` |
| MB08 | `tools/bash-witness-study.py` | SURVIVED | `c1-before.stderr:6` |
| MB09 | `tools/bash-witness-study.py` | SURVIVED | `c1-before.stderr:7` |
| MB10 | `tools/bash-witness-study.py` | SURVIVED | `c1-before.stderr:8` |
| MB11 | `tools/bash-witness-study.py` | SURVIVED | `c1-before.stderr:9` |
| MB12 | `tools/bash-witness-study.py` | SURVIVED | `c1-before.stderr:10` |
| D02 | `tools/evidence-disposition.py` | SURVIVED | `c1-before.stderr:11` |
| D11 | `tools/evidence-disposition.py` | SURVIVED | `c1-before.stderr:12` |
| D12 | `tools/evidence-disposition.py` | SURVIVED | `c1-before.stderr:13` |
| R02 | `tools/registry-check.py` | SURVIVED | `c1-before.stderr:14` |
| R05 | `tools/registry-check.py` | SURVIVED | `c1-before.stderr:15` |
| R07 | `tools/registry-check.py` | SURVIVED | `c1-before.stderr:16` |
| T04 | `tools/trace-inputs.py` | SURVIVED | `c1-before.stderr:17` |
| T12 | `tools/trace-inputs.py` | SURVIVED | `c1-before.stderr:18` |

Each receipt row also has `anchor_count: 1` (`.ufo/evidence/round-21/c1-before.json:45-353`); per the ruler's contract, `SURVIVED` means the pristine selftest was green and the mutant selftest also exited 0 (`.ufo/evidence/round-21/c1-survivors.py:9-14,109-130`). The four pristine-control summaries are PASS / 63-of-63 / 48 cases / 30-of-30 in `c1-before.json`; no control was red.

## History and disposition

- The requested path-filtered history (`58e5d53..33d03b7`) contains exactly one commit touching these four tools: `9ee1c80` (2026-10-20 18:09:03, round-18 wave-2 corrections). Its only owning-tool change is `tools/registry-check.py` (+14/-2): add `MAX_TIMEOUT_S = 86400`, cap the finite timeout, and add too-large timeout selftest cases. There is no change in that commit to the other three owning tools.
- R02 is the sole survivor whose anchor was rewritten. The frozen spec records the exact reanchor: old `math.isfinite(ts) and ts > 0` became `math.isfinite(ts) and 0 < ts <= MAX_TIMEOUT_S`; the mutant still changes that to `0 <= ts <= MAX_TIMEOUT_S` (accept zero). The round-21 baseline still measures R02 as `SURVIVED`. Thus the timeout upper-bound fix is real but does not kill the R02 mutant; it is not a partial kill or equivalence disposition. Evidence: `.ufo/evidence/round-21/c1-mutants.json:91-95`, `SCORECARD.md:874-875`, and the 9ee1c80 hunk in `tools/registry-check.py`.
- There are no owner-tool changes between the round-20 baseline and the round-21 frozen revision: `git diff 08175c6 33d03b7 -- <the four owning tools>` emitted zero lines. The all-files diff for that interval lists only round-21 evidence, `SCORECARD.md`, and `tools/wave-route-mix.py`; it does not list any of the four owners. Therefore no later owner-tool edit closed a survivor before dispatch.
- Round 19 explicitly rejects closing these 18 through metadata repair because the fixes exercise none of the distinct behavioral gaps (`corpus/lessons/round-19.md:24`). Round 20 says all 18 remain open, names their per-tool counts, and says its receipt-metadata work does not exercise them (`corpus/lessons/round-20.md:31`); its separate new-guard probe also exercises/closes none of the 18 (`:151-157`). The round-18 SCORECARD had already marked the same 18 as next-round work (`SCORECARD.md:680-681`).
- No per-ID or population-level routed-equivalence rationale was found in the requested round-19/20 lessons/SCORECARD evidence. Round 19's “no current-page equivalence” wording (`corpus/lessons/round-19.md:112-113`) concerns a different input-keyed-credit claim, not these mutants.

## Commands and observed results

- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --format='%h %ad %s' --date=iso 58e5d53..33d03b716d3edcf1d8656d46d6df61801d232c52 -- tools/bash-witness-study.py tools/evidence-disposition.py tools/registry-check.py tools/trace-inputs.py` — exit 0; sole output: `9ee1c80 2026-10-20 18:09:03 -0300 round-18: wave-2 corrections ... registry timeout cap + scratch exit 2 ...`.
- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show -s --format='%h %ad %s' 58e5d53` — exit 0; `58e5d53 Tue Oct 20 17:20:09 2026 -0300 round-18: build landing ...`.
- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --stat 58e5d53 9ee1c80 -- tools/bash-witness-study.py tools/evidence-disposition.py tools/registry-check.py tools/trace-inputs.py` — exit 0; only `tools/registry-check.py | 16 ++++++++++++++--`.
- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff 08175c6 33d03b716d3edcf1d8656d46d6df61801d232c52 -- tools/bash-witness-study.py tools/evidence-disposition.py tools/registry-check.py tools/trace-inputs.py | wc -l` — exit 0; output `0`.
- Recorded baseline command (not rerun for this review): `python3 .ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 08175c62d661fddf052ed10abc91313dec8eb77d --json`. Stored evidence: `.ufo/evidence/round-21/c1-before.exit` says `exit=1`; `.ufo/evidence/round-21/c1-before.stderr:1-19` records every ID `SURVIVED` and `killed=0 survived=18 inconclusive=0 total=18`; `.ufo/evidence/round-21/c1-before.json:42-45,354-358` agrees.

## Residual risk / verification gap

I did not rerun the mutation ruler: this is an audit of the retained round-20 baseline plus the exact owner-file history/diff, not a new runtime admission. No disagreement was found between the per-ID receipt, round-19/20 lessons, and SCORECARD. No tools were installed or updated.