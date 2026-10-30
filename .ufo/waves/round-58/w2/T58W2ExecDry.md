# T58W2ExecDry — C1 committed replay

Detached clone at `8063d0a551fc5b3cb5a2d397da7353af53444534`; asserted `git rev-parse --show-toplevel` was `/fast/scratch/hyaku/tameshi-r58/T58W2ExecDry/clone`. Ran the frozen counter against that clone and revision with a newly empty `--work` directory and `--explain`.

Command:

```sh
python3 "$S/clone/.ufo/evidence/round-58/c1/measure.py" --lane "$S/clone" --rev 8063d0a551fc5b3cb5a2d397da7353af53444534 --work "$S/empty-work" --explain
```

Exit status: **0**. Full stdout is preserved in `T58W2ExecDry-receipts/frozen-counter.stdout`; exit status in `T58W2ExecDry-receipts/frozen-counter.exit`.

Observed explanatory lines: `panel-disagree R54.5`, `panel-disagree R54.6`, `panel-disagree R56.2`, `panel-disagree R56.3`.

Observed every printed counter term: `fixed=37`, `open=13`, `declined=1`, `fixed_this_round=8`; `missing=0`, `extra=0`, `duplicate=0`, `old49=0`, `spotcheck_changed=0`, `defects_pin=0`, `bad_status=0`, `evidence_bad=0`, `key_miss=0`, `fixed_bad=0`, `open_unplanned=0`, `declined_bad=0`, `fixed_short=0`, `declined_over=0`, `this_round_short=0`, `panel_pin=0`, `panel_over=0`, `base_status_bad=0`, `panel_prov=0`.

Final line: `C1_R58: self=9b7c01673912 rev=8063d0a551fc rows=51/51 agree=51/51 old49=ok fixed=37 declined=1 thisround=8 panel=4/5 spot=ok total=0 C1_R58_PASS=true`.

This confirms the frozen counter's numerical committed replay with an empty work directory; it does not independently validate the executor-forgery attack's separate admission concern. Scratch was removed by the command's EXIT trap before yielding.
