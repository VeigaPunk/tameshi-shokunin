# Round-55 C1 counter mutation matrix (counter sha256 5e8f50d1...)

`*` marks a tree where the PRISTINE counter already deviates from the correct
expectation: a mutant that happens to match there is coincidence, not a kill.

sound trees: base, C0, dirty, noprem, corronly, tailsec, m1, m2, m7, m9, m10, m12, m13, m14, m15, m16, p8

blind trees: f1, f2, f3, p7, p9, p5, p10

| counter | base | C0 | dirty | noprem | corronly | tailsec | m1 | m2 | m7 | m9 | m10 | m12 | m13 | m14 | m15 | m16 | f1 | f2 | f3 | p7 | p9 | p5 | p10 | p8 | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (expected) | F | P | F | F | F | F | F | P | F | P | P | P | P | F | F | F | F | F | F | F | F | F | F | F | baseline |
| pristine | F/1 | P/0 | F/1 | F/1 | F/1 | F/1 | F/1 | P/0 | F/1 | P/0 | P/0 | P/0 | P/0 | F/1 | F/1 | F/1 | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | F/1 | BASELINE-BLIND:f1,f2,f3,p7,p9,p5,p10 |
| N1-drop-R54.1-stale-scan | F/1 | P/0 | F/1 | F/1 | F/1 | F/1 | P/0 | P/0 | F/1 | P/0 | P/0 | P/0 | P/0 | F/1 | P/0 | F/1 | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | F/1 | KILLED@m1,m15 |
| N10-hardcode-R54.4-digest | F/1 | P/0 | F/1 | F/1 | F/1 | F/1 | F/1 | P/0 | F/1 | P/0 | F/1 | P/0 | P/0 | F/1 | F/1 | F/1 | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | F/1 | KILLED@m10 |
| N11-total-from-corrected-only | F/1 | P/0 | F/1 | P/0 | F/1 | P/0 | P/0 | P/0 | F/1 | P/0 | P/0 | P/0 | P/0 | P/0 | P/0 | F/1 | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | F/1 | KILLED@noprem,tailsec,m1,m14,m15 |
| N12-staged-constant-81 | F/1 | P/0 | F/1 | F/1 | F/1 | F/1 | F/1 | P/0 | F/1 | P/0 | P/0 | F/1 | P/0 | F/1 | F/1 | F/1 | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | F/1 | KILLED@m12 |
| N13-hardcode-freeze-pointer | F/1 | P/0 | F/1 | F/1 | F/1 | F/1 | F/1 | P/0 | F/1 | P/0 | P/0 | P/0 | F/1 | F/1 | F/1 | F/1 | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | F/1 | KILLED@m13 |
| N14-drop-scan_span | F/1 | P/0 | F/1 | F/1 | F/1 | F/1 | F/1 | P/0 | F/1 | P/0 | P/0 | P/0 | P/0 | P/0 | F/1 | F/1 | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | F/1 | KILLED@m14 |
| N15-drop-LOG-from-RECORD | F/1 | P/0 | F/1 | F/1 | F/1 | F/1 | F/1 | P/0 | F/1 | P/0 | P/0 | P/0 | P/0 | F/1 | P/0 | F/1 | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | F/1 | KILLED@m15 |
| N16-R54.8-any-superseded | F/1 | P/0 | F/1 | F/1 | F/1 | F/1 | F/1 | P/0 | F/1 | P/0 | P/0 | P/0 | P/0 | F/1 | F/1 | P/0 | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | F/1 | KILLED@m16 |
| N17-corrections-heading-any | F/1 | P/0 | F/1 | F/1 | F/1 | F/1 | F/1 | P/0 | F/1 | P/0 | P/0 | P/0 | P/0 | F/1 | F/1 | F/1 | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | F/1 | SURVIVED |
| N18-no-corrections-exclusion | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1* | F/1* | F/1* | F/1* | F/1* | F/1* | F/1* | F/1 | KILLED@C0,m2,m9,m10,m12,m13 |
| N19-scan_span-no-exclusion | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1* | F/1* | F/1* | F/1* | F/1* | F/1* | F/1* | F/1 | KILLED@C0,m2,m9,m10,m12,m13 |
| N2-hardcode-R54.3-derived | F/1 | P/0 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | F/1 | P/0 | P/0 | P/0 | P/0 | F/1 | F/1 | F/1 | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | F/1 | KILLED@m2 |
| N3-premise-not-in-ok | F/1 | P/0 | F/1 | P/0 | F/1 | F/1 | F/1 | P/0 | F/1 | P/0 | P/0 | P/0 | P/0 | F/1 | F/1 | F/1 | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | F/1 | KILLED@noprem |
| N4-corrections-to-eof | F/1 | P/0 | F/1 | F/1 | F/1 | P/0 | F/1 | P/0 | F/1 | P/0 | P/0 | P/0 | P/0 | F/1 | F/1 | F/1 | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | F/1 | KILLED@tailsec |
| N5-worktree-not-rev | F/1 | P/0 | P/0 | F/1 | F/1 | F/1 | F/1 | P/0 | F/1 | P/0 | P/0 | P/0 | P/0 | F/1 | F/1 | F/1 | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | F/1 | KILLED@dirty |
| N6-skip-R54.8 | F/1 | P/0 | F/1 | F/1 | F/1 | F/1 | F/1 | P/0 | F/1 | P/0 | P/0 | P/0 | P/0 | F/1 | F/1 | P/0 | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | P/0 | KILLED@base,m16,p8 |
| N7-weak-R54.5 | F/1 | P/0 | F/1 | F/1 | F/1 | F/1 | F/1 | P/0 | P/0 | P/0 | P/0 | P/0 | P/0 | F/1 | F/1 | F/1 | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | F/1 | KILLED@m7 |
| N9-last-commit | F/1 | P/0 | F/1 | F/1 | F/1 | F/1 | F/1 | P/0 | F/1 | F/1 | P/0 | P/0 | P/0 | F/1 | F/1 | F/1 | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | P/0* | F/1 | KILLED@m9 |

killed=17 survived=1
