# Round 53 frozen counter mutation probe

Source bytes were obtained with `git show 7d8aaac676cbcb6379f57659e7c3c4c12150a815:<path>`; hashes matched `freeze.json`: C1 `da89149195b863ad5982dd50c072d0aecffd8eb11593db3d931a409c355fd391`, C2 `1942cd8f9850727066439d317acaf5eb0a8e44458b0355ea4dceaf90e8c82c27`. Fixture was a shared clone checked out at C** `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e`; its `rev-parse --show-toplevel` matched its designated scratch path.

## Bounded detector results

The detector invocation was each counter with `--lane <fixture> --rev 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e --work <seat scratch>` (C1 additionally had its frozen `lost-headings.json` beside the script). Pristine C1 output: `C1_R53: rev=5b703c6ff3ff credited=33 lost=31 rekeyed=0/30 readers=0/30 total=62 C1_R53_PASS=false`. Pristine C2 output: `C2_R53: rev=5b703c6ff3ff tmp_hits=0 registry_selftest=[rc=0 SELFTEST: PASS (51 cases)] envdiff_selftest=[rc=0 ENVDIFF_SELFTEST: 9/9 pass] cr47=rc=1 docs=ok total=0 C2_R53_PASS=true`.

| Single-edit mutant | Observed output (C1/C2 verdict) | Verdict |
|---|---|---|
| C1 `rekey-dir-count=0` check disabled | `credited=33 lost=31 rekeyed=0/30 readers=0/30 total=61 C1_R53_PASS=false` | INCONCLUSIVE: pristine already fails (no rekey directory); mutant merely removes one diagnosed problem. |
| C1 `wrong_expectations == 0` changed to `>= 1` | `credited=33 lost=31 rekeyed=0/30 readers=0/30 total=62 C1_R53_PASS=false` | INCONCLUSIVE: pristine already fails before predicate-specific behavior can be isolated. |
| C1 reader SHA comparison replaced with unconditional true | `credited=33 lost=31 rekeyed=0/30 readers=0/30 total=62 C1_R53_PASS=false` | INCONCLUSIVE: pristine already fails; reader count remains 0 because no reader records qualify at fixture revision. |
| C2 CR47 verdict-line rejection disabled | `tmp_hits=0 ... cr47=rc=1 docs=ok total=0 C2_R53_PASS=true` | SURVIVED on this valid C** fixture; need a CR47-breaking fixture to challenge this predicate. |
| C2 TMP regex narrowed from `/tmp` to `/tmpx` | `tmp_hits=0 ... cr47=rc=1 docs=ok total=0 C2_R53_PASS=true` | SURVIVED on this valid C** fixture; no planted committed tools hit was present. |
| C2 documentation-pattern list emptied | `tmp_hits=0 ... cr47=rc=1 docs=ok total=0 C2_R53_PASS=true` | SURVIVED on this valid C** fixture; the current docs pass the pristine patterns, so a stale-doc fixture is needed. |

No mutant was falsely labeled killed: the available C** revision is not a positive C1 fixture (its frozen counter reports 31 lost, zero rekeys/readers), and no C2 negative-control fixture was constructed in this probe. Thus these observations do not establish C1 mutant sensitivity or C2 negative-control sensitivity. The evidence establishes that the requested six code mutations were exercised against the same bounded C** detector and records the baseline limitation explicitly.

## Restoration / scratch

Mutants existed only as separate scratch copies; the extracted pristine counter files remained byte-identical to the freeze hashes. Scratch tree `/fast/scratch/hyaku/tameshi-r53/w2/T53W2MutCounter` was removed after the probe. No tool installation was needed.