# T51W2CritSourceEntry — source-row falsification (round 51)

Axes: calibration, depth, operability. Scope: S272/S273, C2 entry provenance, census diagnostics. Read-only review; no lane or fleet mutation.

## Findings

### F1 — S272 pin, anchors, quote, scope and C2 relevance corroborate

**Evidence / commands:**

```sh
git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show e64e81b8eb96f3682b00c1e7a291e84420b280fa:corpus/drift-pins.sh | sha256sum
```

Observed SHA-256 `c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb`, matching S272 and the target in the registered and neutral sweep receipts. S272 row in candidate `corpus/SOURCES.md:147` pins that rev, full hash, 451 lines, mode 100755 and unchanged kagi HEAD. Its cited regions cover exit map (:19), verify (:118-259), and selftest (:374-446), including the exit-plus-unanchored-grep assertion (:400-405). The knowledge entry independently identifies the same pin and explains the relevant assertion at `.ufo/evidence/round-51` entry `corpus/knowledge/mutation-case-kagi-drift-pins.md:24-50`; source row/entry SHA command:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 6d8c11e378aa90b12650808e1b79270742935f15:corpus/SOURCES.md | sha256sum
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 6d8c11e378aa90b12650808e1b79270742935f15:corpus/knowledge/mutation-case-kagi-drift-pins.md | sha256sum
```

Observed candidate hashes `c35c33044dc958102b542ba4b6669c637af950e3afe16ca21a3e0b2e2283ee6e` and `251ad9ee431e4aa676bf382a8854c920078699fe5a2c116f3ef15b8a5a4992a7`.

**Assessment:** No source-row claim defect found for S272. The entry accurately preserves the measured 2/10 as suite-plus-harness and explicitly identifies three harness-masked kills; neutral receipt `.ufo/waves/round-51/w1/T51ScribeEntry/sweep-neutral.txt:7-34` shows K_GONE_ARM, K_AMBIG_GT, K_SHAPE_OPTIN KILLED and final 5/10, versus registered `.../c2/sweep/sweep.txt:7-31` at 2/10. These are probe measurements, not a replacement recorded table. Keep that distinction.

### F2 — S273 source is supported, but row's opened date is locally dated, not fetch date

S273's source is the captured Chet Ramey author copy, not the unreachable GNU node URL; this is stated in candidate row `corpus/SOURCES.md:148` and substantiated by W1 snapshot metadata (`.ufo/waves/round-51/w1/T51ScribeRowBash/draft-S273.md:8-10,44-73`). Snapshot named `chet-bashref.html`, exact byte count and sha are recorded there; quoted `-e`, exceptions, pipefail, and assignment-status fragments have anchors and counterpart Savannah texi anchors in the row. The entry's explanatory composition is appropriately qualified and backed by measured probe cited at `corpus/knowledge/mutation-case-kagi-drift-pins.md:1,14-22,92-120`; its own line 1 says the S273 semantic content is not a personal page re-read, but is from the named row and observed run.

**Softening:** the row says opened `2026-10-26` although both fetches are recorded at `2026-10-27T00:22Z` UTC. The draft explicitly explains that 2026-10-26 is the lane-local round date and that UTC day-boundary difference is disclosed (`T51ScribeRowBash/draft-S273.md:16-20,44-53`). This is transparent, not false provenance, but date should be described as round-local opened date wherever paraphrased; avoid saying fetched/opened on 2026-10-26 without that qualifier. The row itself contains the fetch timestamp, so no source cell correction warranted.

### F3 — C2 `source:` linkage and sourced predicate fields match

Candidate entry `corpus/knowledge/mutation-case-kagi-drift-pins.md:1-4` starts at column zero with `source:`, names `corpus/drift-pins.sh`, S272 and S273, calls out read-only source, has `verified-at` and `recheck`, and labels the ground Core. SOURCES row S272/S273 used-by cells name exactly this entry; both statuses are mined and opened date is 2026-10-26, matching the frozen C2 sourced-entry requirement (contract `claims.C2`, raw line 35; `.ufo/evidence/round-51/c2/measure.py` rule referenced in W1 Scribe draft §4 at `T51ScribeRowBash/draft-S273.md:76-89`). README inclusion is evidenced by the draft validation record (`draft-S273.md:87-89,114-132`); entry itself describes the expected-after-base state rather than claiming a finalized counter verdict.

**Softening:** entry `:3` states the future `--regression` expectation (“expected once the C2 edit wires the leg”); it is correctly conditional, not evidence of a completed regression. The neutral/registered sweep discrepancy must remain explicit: only the 2/10 result is the registered TABLE measurement; 5/10 is a probe and cannot be narrated as the committed leg result. The entry does so (`:14-22,111-131,161-170,217-222`).

### F4 — Registry schema and census: no new S272/S273 errors; historic warnings remain

Candidate rows `corpus/SOURCES.md:147-148` are pipe-delimited 11-column rows (header `:10`, separator `:11`); row texts contain no literal field-separating pipe beyond delimiters. Dates, IDs, status, tier/kind, and used-by are as above. The stored end census `.ufo/evidence/round-51/census-end.stdout:1-16` has no W04/E04 for S272 or S273; it reports 14 pre-existing W04 duplicate-URL warnings elsewhere and one W01 S101 issue, then `ok`. Thus “no W04/E04” is substantiated only for these two additions; do not call the entire census warning-free. W1 source-row draft records clone validation and 11-column check (`T51ScribeRowBash/draft-S273.md:91-132`), while contract says census command is the fleet-root `scripts/sources-census.sh` (`contract.json:73-76`).

**Smallest safe correction:** none to the rows indicated by this review. Preserve the explicit local-date qualifier and scoped census wording; do not convert the neutral 5/10 probe into the registered 2/10 measurement.
