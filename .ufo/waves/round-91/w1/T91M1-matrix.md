# T91M1 mutation matrix

target sha256: `37e5b3b480d8e4f8f9efec2f24c95e38f4b8afdb2e60fb0200f507ed4dab902e`

## Defect outcomes

| defect | weakened check | prediction | outcome | killed by (must-not-pass control -> PASS=true) | pos_ok |
|---|---|---|---|---|---|
| D01 | replace-list gate (lane) refuses non-empty git replace -l | SURVIVED (V4-replace still refused by sealed reads / source=false) | **SURVIVED** | — | yes |
| D02 | sealed git env carries GIT_NO_REPLACE_OBJECTS=1 | SURVIVED (replace-list gate still refuses V4-replace) | **SURVIVED** | — | yes |
| D03 | pristine gate is green on two runs | SURVIVED (no control state exercises green) | **SURVIVED** | — | yes |
| D04 | exit-97 canary gate | SURVIVED (canary is constant across control states) | **SURVIVED** | — | yes |
| D05 | figure: compare both K and N of measured: K/N killed | KILLED by CTL3-figure | **KILLED** | CTL3-figure | yes |
| D06 | figure: compare K only | SURVIVED (CTL3-figure also changes K) | **SURVIVED** | — | yes |
| D07 | note verdicts must match derived verdicts | KILLED by CTL2-flip | **KILLED** | CTL2-flip | yes |
| D08 | duplicate id row refuses the note | KILLED by VOV1-dup-row, VOV3-draft-column | **KILLED** | VOV1-dup-row | yes |
| D09 | out-of-vocabulary verdict cell refuses the note | KILLED by VOV3-draft-column | **KILLED** | VOV3-draft-column | yes |
| D10 | note id set must equal the spec id set | SURVIVED (CTL4-ids also flips mismatched0) | **SURVIVED** | — | yes |
| D11 | mutant spec bytes pinned to SPEC_SHA | KILLED by CTL5-spec | **KILLED** | CTL5-spec | yes |
| D12 | gate blob pinned to the spec sha256 | SURVIVED (CTL12-pin also flips spec=false) | **SURVIVED** | — | yes |
| D13 | mutant edit must be unique and non-noop (invalid0) | SURVIVED (invalid-flipping controls also edit the spec) | **SURVIVED** | — | yes |
| D14 | mutant validate run must not fail trivially (trivial0) | SURVIVED (trivial-flipping controls also edit the spec) | **SURVIVED** | — | yes |
| D15 | no-op mutant counts as invalid | SURVIVED (CTL6-noop also edits the spec) | **SURVIVED** | — | yes |
| D16 | witness must actually differ | SURVIVED (CTL9-equiv also edits the spec) | **SURVIVED** | — | yes |
| D17 | timeout derives INCONCLUSIVE, not SURVIVED | SURVIVED (no control produces a timeout) | **SURVIVED** | — | yes |
| D18 | fenced code blocks are skipped by the note parser | SURVIVED (no control note carries fenced rows) | **SURVIVED** | — | yes |
| D19 | at least 12 mutants (n_min) | SURVIVED (no control shrinks the mutant list without editing the spec) | **SURVIVED** | — | yes |
| D20 | note cites a mined S318 registry row naming the note | KILLED by CTL10-source, CTL16-oldsource | **KILLED** | CTL10-source, CTL16-oldsource, CTL1b-nowork-A | yes |
| D21 | README carries a row naming the note | KILLED by CTL15-coverage | **KILLED** | CTL15-coverage | yes |

## Per-control matrix

T = `C1_R91_PASS=true`, f = `C1_R91_PASS=false`, E = receipt missing, 2 = exit 2 refusal.

| defect | CTL1-nowork-base | CTL1b-nowork-A | V4-replace | CTL2-flip | CTL3-figure | CTL4-ids | CTL5-spec | CTL6-noop | CTL7-syntax | CTL8-absent | CTL9-equiv | CTL10-source | CTL11-trivial | CTL12-pin | CTL14-pos | CTL15-coverage | CTL16-oldsource | VOV1-dup-row | VOV3-draft-column |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D01 | 2 | f | f | f | f | f | f | f | f | f | f | f | f | f | T | f | f | f | f |
| D02 | 2 | f | 2 | f | f | f | f | f | f | f | f | f | f | f | T | f | f | f | f |
| D03 | 2 | f | 2 | f | f | f | f | f | f | f | f | f | f | f | T | f | f | f | f |
| D04 | 2 | f | 2 | f | f | f | f | f | f | f | f | f | f | f | T | f | f | f | f |
| D05 | 2 | f | 2 | f | T | f | f | f | f | f | f | f | f | f | T | f | f | f | f |
| D06 | 2 | f | 2 | f | f | f | f | f | f | f | f | f | f | f | T | f | f | f | f |
| D07 | 2 | f | 2 | T | f | f | f | f | f | f | f | f | f | f | T | f | f | f | f |
| D08 | 2 | f | 2 | f | f | f | f | f | f | f | f | f | f | f | T | f | f | T | f |
| D09 | 2 | f | 2 | f | f | f | f | f | f | f | f | f | f | f | T | f | f | f | T |
| D10 | 2 | f | 2 | f | f | f | f | f | f | f | f | f | f | f | T | f | f | f | f |
| D11 | 2 | f | 2 | f | f | f | T | f | f | f | f | f | f | f | T | f | f | f | f |
| D12 | 2 | f | 2 | f | f | f | f | f | f | f | f | f | f | f | T | f | f | f | f |
| D13 | 2 | f | 2 | f | f | f | f | f | f | f | f | f | f | f | T | f | f | f | f |
| D14 | 2 | f | 2 | f | f | f | f | f | f | f | f | f | f | f | T | f | f | f | f |
| D15 | 2 | f | 2 | f | f | f | f | f | f | f | f | f | f | f | T | f | f | f | f |
| D16 | 2 | f | 2 | f | f | f | f | f | f | f | f | f | f | f | T | f | f | f | f |
| D17 | 2 | f | 2 | f | f | f | f | f | f | f | f | f | f | f | T | f | f | f | f |
| D18 | 2 | f | 2 | f | f | f | f | f | f | f | f | f | f | f | T | f | f | f | f |
| D19 | 2 | f | 2 | f | f | f | f | f | f | f | f | f | f | f | T | f | f | f | f |
| D20 | 2 | T | 2 | f | f | f | f | f | f | f | f | T | f | f | T | f | T | f | f |
| D21 | 2 | f | 2 | f | f | f | f | f | f | f | f | f | f | f | T | T | f | f | f |

## Kill attribution per committed control

| control | frozen receipt | defects it kills |
|---|---|---|
| CTL1-nowork-base | false | — |
| CTL1b-nowork-A | false | D20 |
| V4-replace | false | — |
| CTL2-flip | false | D07 |
| CTL3-figure | false | D05 |
| CTL4-ids | false | — |
| CTL5-spec | false | D11 |
| CTL6-noop | false | — |
| CTL7-syntax | false | — |
| CTL8-absent | false | — |
| CTL9-equiv | false | — |
| CTL10-source | false | D20 |
| CTL11-trivial | false | — |
| CTL12-pin | false | — |
| CTL14-pos | true | — |
| CTL15-coverage | false | D21 |
| CTL16-oldsource | false | D20 |
| VOV1-dup-row | false | D08 |
| VOV3-draft-column | false | D09 |

## Verdict

killed=7 survived=14 of 21

VERDICT: survivors:D01,D02,D03,D04,D06,D10,D12,D13,D14,D15,D16,D17,D18,D19

lane snapshot HEAD 584bbe3ca78fdb9188214b0a3de22caf6ffeb2e4; frozen driver sha256 21607bf89e039a71bcd07c17c1b3771d59a833c487dd6585a9d5e8c3e1b84fa4; patched driver sha256 f94088b016b8666f4821c467fe9358dd4f4ea49b20ef9c7351a47e230d5b9401
