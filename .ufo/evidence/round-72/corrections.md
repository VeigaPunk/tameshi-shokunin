# Round-72 corrections of record

Two routed defects from the round-71 non-author closure are corrected this
round. The pointers below are the tokens the standing pointer-recheck rows
resolve; this file is the *record* those rows read (it is not a corpus file).

1. **S302's §-label and page span.** The round-71 closure routed defect 1: the
   S302 row cites "§4.3's numeric-address form" while the sentence lives under
   **§4.2 Selecting lines by numbers** (fetched page line 2246; the sentence at
   page line 2255), and the primary §4.4 range quote sits at page lines
   **2446–2449**, not 2445–2448 (both re-measured this round on the live page,
   sha256 `511edd60a6f5034d4f28ca1dbe0772bbfd4c9865aaf6c0f85e2f05d4294b6bac`,
   byte-identical to the r71 snapshot). Corrected by supersession, CORPUS.md
   rule 2: **corpus/SOURCES.md:178** carries `| S303 |` with the §4.2 label
   and the measured page lines (needle: `§4.2 Selecting lines by numbers`).

2. **The PROVINCE round-16 append's span.** `PROVINCE.md` line 57 says "the
   seven-leg list now sits at `:85-91`"; at the base revision lines 85-91 are
   the ledger narrative plus legs 1-4 (the header is line 84). The corrected
   spans, appended at the round-72 correction block: `:88-94` (legs 1-7, leg 7
   `js-round-gate` at line 94) and `:88-97` (legs 1-10, leg 10
   `bash-drift-pins` at line 97). The stale cell stands append-only and stays
   measured by the red arm `province-r16-sevenleg-85-91`.
