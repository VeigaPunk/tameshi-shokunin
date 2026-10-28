# code -> emission site -> selftest case -> sweep verdict (measured)

Subject: /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/receipt-revision-gate.py
sha256 1d80f8a665f83508a05a33827de66ffd53c986e8de25f8f77937707cac78fbd2
lane HEAD c3e2ca9f020776b3d66c7af854fb82c834674fcf
Baseline selftest: GATE_SELFTEST: 14/14 pass, exit 0 (01-baseline-selftest.txt)

| code | emission line | selftest case | sweep site | verdict |
|---|---|---|---|---|
| RECEIPT_MISSING | 97 | missing-refused | E01 | KILLED |
| RECEIPT_EMPTY | 100 | empty-refused | E02 | KILLED |
| RECEIPT_NOT_BLOB | NONE | NONE | — | no emission site, no case |
| RECEIPT_REV_ABSENT | 118 | absent-refused | E03 | KILLED |
| RECEIPT_REV_UNRESOLVABLE | 124 | unresolvable-refused | E04 | KILLED |
| RECEIPT_REV_AMBIGUOUS | 132 | ambiguous-refused | E05 | KILLED |
| RECEIPT_REV_MISMATCH | 137 | strict-mismatch-refused | E06 | KILLED |
| RECEIPT_REV_CONTENT_DRIFT | 142 | content-drift-refused | E07 | KILLED |
| RECEIPT_CONTROL_NOT_ANCESTOR | 149 | control-not-ancestor-refused | E08 | KILLED |
| RECEIPT_DIGEST_MISMATCH | 112 | digest-mismatch-refused | E09 | KILLED |
| RECEIPT_REQUIRED_LINE_MISSING | 115 | required-line-refused | E10 | KILLED |

Ten of eleven declared codes are 1:1 with a named selftest case and each emission
line is load-bearing (disabling it fails exactly that case). RECEIPT_NOT_BLOB is
declared in the docstring (line 26) and in CODES (line 46) and is never emitted.

Required mutant set (8) -> failing case:
M1 drop RECEIPT_REV_ABSENT return -> absent-refused (child exits 1 on IndexError, not 3)
M2 drifted_paths -> []            -> content-drift-refused
M3 is_ancestor -> True            -> control-not-ancestor-refused
M4 skip digest check              -> digest-mismatch-refused
M5 accept multi-rev positive      -> ambiguous-refused
M6 skip required-line check       -> required-line-refused
M7 empty file treated as present  -> empty-refused
M8 drop RECEIPT_CONTROL_NOT_ANCESTOR -> control-not-ancestor-refused
