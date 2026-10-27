# T53W2RevLesson — round-53 lesson audit

Audited `corpus/lessons/round-53.md` from C** (`5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e`) against that commit's tree. Gate and Mistakes checks are structural; citation statuses below are per cited path (quotes are quoted verbatim from the lesson).

## Findings

- **MISMATCH — pass-2/strict-helper history is under-described and stale at C**.** The lesson calls its claims frozen at `e62d9971` with amendments 1–5 (lines 5–6), says wave 1 reads all 30 sections and then describes only those re-reads (123–126), and does not identify C* (`a41195dfc13a73958e4c5228ec196b28d03ded03`), C** (`5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e`), the 40 wave-1 findings, the second fix pass over the 21 dirty sections, or the strict TMPDIR scratch-root helper work in seven tools. The frozen manifest is amended through amendment 6; C** is explicitly the second content/fix commit. Thus the lesson does not describe the actual pass-2 work or this re-read wave. No edits made (review-only scope).
- **MISMATCH — cited receipt paths**: `.ufo/evidence/round-53/assimilation/S161-camera-ready.pdf`, `.ufo/evidence/round-53/assimilation/S162-arxiv.html`, and `.ufo/evidence/round-53/verify-freeze.sh` do not resolve as paths in C**. Their citations are presented as snapshots/receipt, not explicitly as historical/reaped paths. The lesson's HTTP status/hash claims therefore are not verifiable from these C** tree paths.

## Citation/path audit

- VERIFIED — `corpus/lessons/round-52-verifier-spotcheck.md` (lines 8–9).
- VERIFIED — `.ufo/evidence/round-53/contract.json`, `freeze.json` (lines 5–6).
- MISMATCH — `.ufo/evidence/round-53/assimilation/S161-camera-ready.pdf` (lines 21–22).
- MISMATCH — `.ufo/evidence/round-53/assimilation/S162-arxiv.html` (lines 29–30).
- VERIFIED — `corpus/README.md` (line 43).
- VERIFIED — `.ufo/waves/round-52/w3/` (line 86).
- MISMATCH — `.ufo/evidence/round-53/verify-freeze.sh` (lines 71–73).
- VERIFIED — `considerthese/2026-10-26.md` (line 70).
- VERIFIED — `.ufo/waves/round-53/` (lines 123–126; directory exists).
- VERIFIED — `T52W2Fix06.selftest.out` (line 84: named as a receipt; whether its specific assertion is supported is part of the MISMATCH above about the receipt citation).

## Structural checks

- Gate: **PASS** — at least one admit (`change-aware-resweep-cadence.md`) and at least one reject (the 85 staged entries; also staged row as-is).
- Mistakes: **PASS** — all three entries state class, evidence, captured-by, and fix.
- Phrase checks: the wave-1 40-finding pass and strict-helper fix are **not named**; pass 2 is not described. The lesson's wave-1-only account is insufficient at C**.

## Verification basis / residual risk

Used `git show` from C** to extract the lesson and `git cat-file -e C**:<path>` for path status; freeze manifest bytes identify amendments 1–6. I did not verify external URLs, PDF quote locations, or HTTP/hash receipts. No tests run; this was a content audit.
