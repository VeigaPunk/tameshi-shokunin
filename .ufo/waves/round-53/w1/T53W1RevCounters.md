# T53W1RevCounters — independent mid-state counters

## Checks and receipts

- Read the frozen round-53 contract and the c1/c2 measure scripts; ran both frozen commands against lane git objects at `a41195dfc13a73958e4c5228ec196b28d03ded03`. No checkout or git mutation was used. Python: 3.14.8. `lost-headings.json` at the lane contained 30 entries.
- Scratch: `/fast/scratch/hyaku/tameshi-r53/w1/T53W1RevCounters`; `TMPDIR` was explicitly bound to its `tmp/` directory for both measure invocations. Each `--work` was an initially empty directory under that scratch. Both counters emitted no stderr.
- C1 command: `TMPDIR=/fast/scratch/hyaku/tameshi-r53/w1/T53W1RevCounters/tmp python3 .ufo/evidence/round-53/c1/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev a41195dfc13a73958e4c5228ec196b28d03ded03 --work /fast/scratch/hyaku/tameshi-r53/w1/T53W1RevCounters/work-c1`; exit 1.

  `C1_R53: rev=a41195dfc13a credited=34 lost=30 rekeyed=0/30 readers=0/30 total=32 C1_R53_PASS=false`

- C2 command: `TMPDIR=/fast/scratch/hyaku/tameshi-r53/w1/T53W1RevCounters/tmp python3 .ufo/evidence/round-53/c2/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev a41195dfc13a73958e4c5228ec196b28d03ded03 --work /fast/scratch/hyaku/tameshi-r53/w1/T53W1RevCounters/work-c2`; exit 1.

  `C2_R53: rev=a41195dfc13a tmp_hits=0 registry_selftest=[rc=0 SELFTEST: PASS (51 cases)] envdiff_selftest=[rc=0 ENVDIFF_SELFTEST: 9/9 pass] cr47=rc=0 docs=ok total=2 C2_R53_PASS=false`

- Scratch receipts (SHA-256): `c1.stdout` `df6305aceab6aff0b024fa8bd24ed5f82ea7e2a17ef03a33e6f2b277932f5b75`; `c1.stderr` `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; `c2.stdout` `14f9536079f2476a11ea17fd471dd40ed16e45d0f4d089d3760b9413e2172af5`; `c2.stderr` `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Counter-script SHA-256: c1 `067c1685eeda8177a47fec5806a8367ebde4b99737394dd4a68068fe5d949955`; c2 `1942cd8f9850727066439d317acaf5eb0a8e44458b0355ea4dceaf90e8c82c27`.
- C2 manual reproduction: extracted `tools/registry-check.py` from C* to scratch (`f394f6221e4f9288041fc6efe7afc47f2f2b96f36601ff25a7501b73a669909b`); with `TMPDIR=/fast/scratch/hyaku/tameshi-r53/w1/T53W1RevCounters/cr47probe/missing-nonexistent`, `python3 registry-check.py --selftest` exited 0, printed `SELFTEST: PASS (51 cases)`, and emitted no stderr. A separate Python `tempfile.gettempdir()` probe with nonexistent TMPDIR printed `/tmp`; explicit `tempfile.mkdtemp(dir='/nonexistent-r53-c2-missing')` raised `FileNotFoundError`.
- Work residue observed before cleanup: c1 extracted `precheck.sh`, `r18measure.py`, and `__pycache__/r18measure.cpython-314.pyc`; c2 extracted its `tmp/`, `registry-check.py`, and `env-diff.py`. The lane already had unrelated round activity at initial status capture (e.g. reader files and integration artifacts); I did not alter it.

## Finding — C2 CR47 guard does not reject missing TMPDIR

At C*, `tools/registry-check.py` lines 766–768 use `tempfile.mkdtemp(..., dir=tempfile.gettempdir())` and catch `OSError` to raise `RuntimeError("cannot create clone scratch ...")`. But `tempfile.gettempdir()` silently falls back to `/tmp` when `TMPDIR` points to a nonexistent directory. I reproduced this using the extracted C* script: missing TMPDIR still yielded a successful 51-case selftest, and the counter's CR47 run reported `rc=0`. The frozen counter requires that path to fail nonzero and name scratch creation (its `measure.py` lines 97–110); instead the counter reports `cr47=rc=0`, `total=2`, and `C2_R53_PASS=false`. This contradicts the assigned expected C2 pass and the CR47 contract: invalid TMPDIR is not treated as could-not-evaluate; execution falls back to `/tmp`.

**C1:** expected mid-state confirmed; no finding. **C2:** unexpected counter verdict; finding above. Scratch was removed before handoff. No tools installed or updated.
