# T58W2RevThis — this-round fixes

C0: `8063d0a551fc5b3cb5a2d397da7353af53444534`; base: `2a32aa8228d5f86a85c81a923a3148bf792a9538`.

Axes: calibration, measurement reproducibility, provenance.

## Findings by severity

No new actionable finding in the assigned this-round-floor check. This is a review recommendation, not admission.

The requested frozen C1 command completed with exit 0:

```text
C1_R58_TERMS: fixed=37 open=13 declined=1 fixed_this_round=8 missing=0 extra=0 duplicate=0 old49=0 spotcheck_changed=0 defects_pin=0 bad_status=0 evidence_bad=0 key_miss=0 fixed_bad=0 open_unplanned=0 declined_bad=0 fixed_short=0 declined_over=0 this_round_short=0 panel_pin=0 panel_over=0 base_status_bad=0 panel_prov=0
C1_R58: self=9b7c01673912 rev=8063d0a551fc rows=51/51 agree=51/51 old49=ok fixed=37 declined=1 thisround=8 panel=4/5 spot=ok total=0 C1_R58_PASS=true
```

Command: `python3 -I /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-58/c1/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 8063d0a551fc5b3cb5a2d397da7353af53444534 --work /fast/scratch/hyaku/tameshi-r58/T58W2RevThis/c1-work --explain`.

Independent git-object enumeration found eight fixed rows whose fixing commits descend from base and precede C0. Each fixing commit names its row IDs; every row declares `status_at_base=open`:

| IDs | Fix commit |
|---|---|
| R51.5, R51.6 | `38e4e3aff7cf0da9032761acd1548e49ba49d9fe` |
| R53.2, R53.4, R55.1 | `7d5ae605eb6f07b91e836fd5afe822db5e00ecd3` |
| R53.5 | `764f87bc8a9f4354ab9dec3ff77f995176063cc7` |
| R55.4 | `6024c8fcc9b01950b9bff11b59cab257eea87333` |
| R56.3 | `1d1f70d89acf4e07ee7326707878455c0f5b3c19` |

For each row, `git -C LANE merge-base --is-ancestor FIX C0` returned 0, `FIX BASE` returned 1, and `BASE FIX` returned 0. Full messages and outputs are in the receipts. The canonical eligibility/increment logic is `.ufo/evidence/round-58/c1/measure.py:309–355`; shortfall is calculated at lines 447–449. Eight clears the required six without counting base-era fixes.

## Two independently reproduced fixing measurements

Counters were extracted from C0 and confirmed byte-identical to their historical `88afa941545469457c78c7f4014bcda1afdee52c` versions. Runs used a shared scratch clone detached at C0 and separate empty work directories. Both stdout blobs matched their C0 committed receipts exactly:

- Round-53 C1, exit 1: `credited=58 lost=6 rekeyed=0/30 readers=25/30 total=37 C1_R53_PASS=false`; all 38 lines match `.ufo/evidence/round-53/after/c1.stdout`.
- Round-53 C2, exit 0: `tmp_hits=0 registry_selftest=[rc=0 SELFTEST: PASS (51 cases)] envdiff_selftest=[rc=0 ENVDIFF_SELFTEST: 9/9 pass] cr47=rc=2 docs=ok total=0 C2_R53_PASS=true`; matches `.ufo/evidence/round-53/after/c2.stdout`.

These support R53.2's missing-receipt repair and R53.4's replacement receipt binding. Historical C1 RED is expected, not suppressed, and does not mean the record repair failed.

## Known falsifier reproduced

Using literal `CHEAT_GATE`/`BENT_RC` constants from the committed wave-1 attack (without executing its hardcoded driver), the unchanged frozen round-58 C2 measurement accepted the nonexecuting runner: `held=3/3 mutants=3/3 total=0 C2_R58_PASS=true`. A corresponding real-runner fixture refused: `held=2/3 mutants=1/3 total=3 C2_R58_PASS=false`.

This confirms the known executor-forgery vulnerability, not a new finding. The prior report's real-runner `held=1/3` was not reproduced; this run observed `2/3`. Numerical PASS is not evidence of C2 admission. Neither counter nor target was weakened.

## Residual risk and verification gaps

- This seat independently reproduced two measurements, not semantic saturation of every fixed row. Other ledger seats own full per-row semantic adjudication.
- C1 has four panel disagreements against an allowance of five; mechanical acceptance does not adjudicate those disagreements.
- Round-55 C2 was not rerun by this seat.
- `xd://lsp` returned `No such tool`; git-object/text inspection is not semantic reference proof.
- Runtime/rerouting/resume-continuity implementations are not changed by these ledger repairs and were not invoked or assessed here.

Receipts (absolute directory): `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w2/T58W2RevThis-receipts/`. `commands.json` includes actual commands/output; `ancestry.json`, `post-base-rows.json`, both `round53-*-comparison.json`, and `forgery-replay.json` carry detailed evidence.

Scratch `/fast/scratch/hyaku/tameshi-r58/T58W2RevThis` was deleted before delivery; `os.path.exists` returned `False`. No tools installed. No lane implementation or prior-round evidence edited.
