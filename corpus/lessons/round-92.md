# Round 92 — lesson (tameshi)

Base `63172b9889475103aeca976d37389d204010dd11` (round-91 verifier spot-check tip).
One claim this round: R92-C1, coverage — the third attempt at certifying the
round-90 fleet-gate mutation case, under a sealed counter that pins its own
sha256 and refuses any verdict-shaped row outside the spec's id set.

## Gate

| Item | Decision | Source opened this round | Reason |
|---|---|---|---|
| S320 sha256sum(1), Arch manual pages (GNU coreutils 9.12) | admit (A, `mined`) | https://man.archlinux.org/man/sha256sum.1.en, fetched 2026-11-08, HTTP date `Sun, 08 Nov 2026 05:27:37 GMT`, 12 127 B, sha256 `b968bc09839877f9b0bf892b8a37fce0f72f4fa0ff0f17208824161b8547277b` (`.ufo/evidence/round-92/sources/s320.html`, headers in `s320.headers`) | "Print or check SHA256 (256-bit) checksums." (7 words, `sources/s320.txt:19`) and "The sums are computed as described in FIPS-180-2." (10 words, `:53`). Grounds the counter's `SELF_SHA256` pin: the pin is a sha256 digest of the instrument's own bytes, and `--check`/`--strict` are the semantics a reader uses to re-verify it. |
| Claim candidate: reuse round-91's frozen counter and re-point its `source:` conjunct at S320 | reject | round-91 `measure-v91.py` `parse_note` and its receipts | round 91's counter was killed by its own wave (a hidden `C001`-`C012` table is invisible to `^\|\s*(C\d\d)`) and its receipts certify post-freeze bytes; a re-pointed copy would inherit both defects. A successor is required, and it must pin its own bytes (QUALITY 143-144). |
