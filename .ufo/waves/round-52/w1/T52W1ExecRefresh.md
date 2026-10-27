# T52W1ExecRefresh

Axes: calibration (C2 m6), instrument operability.

## Deliverables

- `refresh.py`: `.ufo/waves/round-52/w1/T52W1ExecRefresh/refresh.py`
- Adapted from `.ufo/evidence/round-51/coldread/refresh.py`; BASE is `ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4`; receipt location and scratch are round 52; reader JSON carries seats, reader_files and findings; ledger wrong_expectations is `len(findings)`; quotes must occur verbatim in reader files.

## Scratch experiment (all artifacts under `/fast/scratch/hyaku/tameshi-r52/T52W1ExecRefresh`)

Clone command:

```sh
git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/clone"
git -C "$S/clone" checkout -q --detach ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4
test "$(git -C "$S/clone" rev-parse --show-toplevel)" = "$S/clone"
```

Synthetic edit appended `Synthetic calibration edit. tools/mte-interop.py` to SKILL.md. Reader file contained `Synthetic reader quote from fixture. This exact sentence supports the finding.` The instrument output:

```text
TARGETS 1 BASE ef19d8e1 (64/64 score 8) CAND f6fe0f82 (63/64 score 6)
```

Generated ledger data observed in scratch: one entry for `### Round-26 gate/probe registry — report interop`, `wrong_expectations=1`, `reader_files=["reader.md"]`, one matching finding. Frozen C2 `--explain` output for the scratch candidate included `m6 ok t52_entries=1 bad=[]` and `m6=0`. Other C2 predicates were expectedly mismatched because this fixture contains only the synthetic edit and not the round's other repairs; this is not a verdict.

The round-21 monitor at the first candidate read `covered=63 total=64`, with the modified section `no-ledger-entry`. After the generated ledger was committed into the scratch clone, the monitor read the appended entry but marked `wrong-expectations:1`; that monitor's score uses wrong_expectations and thus the generated fixture is not a valid monitor-credit demonstration. C2 m6 specifically did accept the reader-file/finding structure. This is a test fixture limitation, not a deciding run.

Forged-quote test, against a candidate with its prior generated ledger:

```text
rc=1
finding quote is not a verbatim substring of its reader files for ### Round-26 gate/probe registry — report interop: 'forged quote is not really in reader file'
```

The initial attempt to test monitor credit therefore did not demonstrate credit-after-rekey. No claim is made that the monitor credited the synthetic target. The instrument's corresponding prior-round flow assigns zero wrong_expectations; the round-52 schema correctly derives it from provided findings as required by C2 m6.

## Diff evidence

Command used to inspect version delta:

```sh
diff -u /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-51/coldread/refresh.py \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-52/w1/T52W1ExecRefresh/refresh.py
```

The file is adapted rather than copied byte-for-byte: BASE, round-specific destination/scratch, structured reader input, quote validation and findings/count persistence changed; tracing and monitor-target computation were retained.

## Findings with locations and reproducing commands

- `.ufo/evidence/round-52/c2/measure.py:166-176` checks each T52 entry's reader_files, findings quote substrings, and exact wrong_expectations count. Command: `python3 .ufo/evidence/round-52/c2/measure.py --lane LANE --rev REV --explain`.
- `.ufo/waves/round-52/w1/T52W1ExecRefresh/refresh.py:112-141` validates reader schema and verbatim quote inclusion. Reproducer: run the instrument with a finding quote absent from its referenced reader file; observed refusal above.
- `.ufo/waves/round-52/w1/T52W1ExecRefresh/refresh.py:213-224` appends reader_files/findings and derives wrong_expectations from their count.

## Risks / blocker

The specified end-to-end acceptance requires a synthetic changed section to become credited by the cold-read monitor after the generated entry is appended. The inherited monitor algorithm treats any positive wrong_expectations count as an uncredited entry; because this round requires wrong_expectations equal to findings length and C2 requires findings for m6, the synthetic fixture with a nonempty finding remains uncredited. The observed scratch monitor output is 63/64, not 64/64. The delivery does not claim that acceptance criterion passed. The successful finding-schema observation (`m6=0`) is not a substitute for monitor credit.

## Summary
- Delivered round-52 refresh instrument.
- Synthetic run generated one finding-bearing entry; observed C2 m6=0.
- Forged quote rejected.
- Monitor credit-after-rekey not demonstrated (63/64 in scratch); no deciding claim.