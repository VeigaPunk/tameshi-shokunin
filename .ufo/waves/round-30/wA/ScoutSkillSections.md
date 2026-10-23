| Item | Value |
|---|---|
| Commit | `f09d3425258403a51422c9959e25340807982947` `SKILL.md` (2136 lines, 22602 words) |
| Section | heading plus following lines, until the next heading. A `#` inside a code fence is not a heading. |
| `corpus/SOURCES.md` | file exists (9522 words). No section cites that path. |
| `corpus/QUALITY.md` | file exists (5546 words). No section cites that path. QUALITY41-style tokens are not the path. |
| Citing sections | 18. The runner path is in 16. `corpus/README.md` is in 3 (recipe, restore, map). |
| Must run | 9 sections, modes in the detail table. The other 9 cite a line, a checksum, or a past receipt. |
| Over 45 minutes | none of the 18. Longest citing section is the recipe, 1043 words, 115 lines. |
| Whole page | 22602 words is not a 45-minute read. The errata says that job was 51 buckets and 30 seats. |
| Tools installed | none |

| Run | Command and observed result |
|---|---|
| `--selftest` | Clone at that commit, git env vars unset. `timeout 600 bash tools/mutate-and-run.sh --selftest`. Exit 0. 12.500 s. `MUTATE_SELFTEST: 97/97 pass`. `VERDICT: PASS`. |
| `--regression` | Same commit, clone moved to `fleet/tameshi-shokunin`, sibling repos symlinked beside it. `timeout 480 bash tools/mutate-and-run.sh --regression --workdir <seat>/regression-work`. Exit 0. 459.835 s (7 min 40 s). `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)`. Tool sha256 `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de`. |
| Per-leg suite time | control line plus `results.tsv`, sum 453.4 s. bash-surface-census 125.1 s. bash-checklist-run 119.0 s. js-round-gate 92.0 s. bash-tsukuroi-census 40.5 s. js-kimi-census 28.7 s. bash-mado-verify 20.7 s. js-sources-check 13.1 s. js-claims-check 11.7 s. js-cite-check 2.7 s. Per-run cap is 300 s. It was not hit. |

| Start | Heading | Cites | Run? | Mode | Rough time | Over 45 min |
|---|---|---|---|---|---|---|
| 131 | ## Mutation-sweep recipe — numbered steps; bounded cold-read evidence | `corpus/README.md` (156, G-R2-1 row) | No. Hand recipe, not this runner. Page's own sweeps: 7.0 s and 11.0 s. | none | 1043 words | no |
| 375 | ## Restore discipline — before/after identity, not continuous non-write proof | runner (399), `corpus/README.md` (403) | Yes. Step 6 says use the maintained replay when the old driver is gone. | `--regression` | 7 min 40 s | no |
| 827 | ### The protocol — ordered, fail-closed | runner (829, 831, 834) | Fence is a sweep, but `<gate>`, `<spec>`, and `<scratch>` are placeholders, so it is not runnable as written. | sweep (`--target --defects --suite`) | mado leg here: 20.7 s. Page's mado figure: 5.26 s for 11 runs. | no |
| 858 | ### The boundaries — what a service run is not | runner (865, lines 36-38, a quote) | No. Read those lines. | none | 242 words | no |
| 921 | ## The leg ledger — replay, receipt, and how it is read (round 7, measured) | runner (929, old pin `@9f1d3c3`) | No. Anchor only. The command is the next heading. | none | 130 words, through line 932 | no |
| 933 | ### Using the ledger | runner (935, 940, 943, 960) | Yes. The first bullet is the replay command. | `--regression` | 7 min 40 s | no |
| 965 | ### Reading a receipt — the discipline | runner (1002) | Yes, item 7 only. It says not to re-sweep a FAIL by hand. | `--selftest` | 12.5 s. Page expects `67/67` at `cf41efaa…`. This commit printed `97/97`. | no |
| 1021 | ### The tick and the pin read | runner (1039) | No. That line is `sha256sum` of the file, not a mode. | none | 531 words | no |
| 1164 | ### The tick, executed | runner (1169, 1182) | No. Line anchor plus `sha256sum`. | none | 376 words | no |
| 1212 | ### The receipt at this boundary | runner (1225, lines 733-791) | No. Past run (`67/67`, four legs), not an instruction to run again. | none | 108 words | no |
| 1302 | ### The six-leg regression — usage and this round's receipt | runner (1306, 1319, 1323) | Yes. "Command, unchanged" is the replay. The `80/80` self-test is a past receipt at `75ed934d…`. | `--regression` | 7 min 40 s. Live result is `cases=9`, not the six this heading records. | no |
| 1380 | ### The map — where a reader enters, artifact by artifact | runner (1391), `corpus/README.md` (1392) | No. Pointer: read the tool when you already have a sweep or a replay. | none | 369 words. Whole `corpus/README.md` is 5555 words, about 37 min at 150 words per minute. | no |
| 1707 | ## Errata — round 16 full-page cold-read | runner (1750, anchor shape) | No. | none | 689 words. The page it recounts is the overflow, not this heading. | no |
| 1754 | ## Seventh recorded case and full-page cold-read — round 16 | runner (1762, 1771, 1789) | Yes. The fenced block is one sweep. The `--regression` arrow is a recorded result (`cases=7` then, `cases=9` since round 26). | sweep of `round-gate.mjs` | that leg: 92.0 s, 5/10 killed, PASS | no |
| 1806 | ### Round-16 gate/probe registry | runner (1810) | Yes. The row is the command. | `--selftest` and `--regression` | 12.5 s, then 7 min 40 s. Both exited 0. | no |
| 1846 | ### Round-17 gate/probe registry — re-pin and monitor | runner (1852) | Yes. Same two commands. | `--selftest` and `--regression` | 12.5 s, then 7 min 40 s | no |
| 1905 | ## Eighth recorded case — round 18 | runner (1914) | Yes. The replay line is the full command, not the one leg. | `--regression` | 7 min 40 s. `js-sources-check` alone: 13.1 s, PASS, 5/10. | no |
| 2104 | ## Ninth recorded case — round 26 | runner (2112) | Yes. The replay line is the full command. | `--regression` | 7 min 40 s. `js-cite-check` alone: 2.7 s, PASS, 5/10. | no |

| Question | Answer |
|---|---|
| Sections that cannot be read in 45 minutes | None of the 18. Running every required mode in the detail table is about 8 minutes. |
