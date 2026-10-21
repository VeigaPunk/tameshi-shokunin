# D07 — Round-19 instrument wording erratum

## Finding

The requested append-only erratum is already present at the end of `corpus/lessons/round-19.md` (lines 348–374) under **“Round-20 erratum — distinct instrument identities and date bases (2026-10-21)”**. This seat did not add or alter lesson text; the lane contract permits writing only this report trailer.

The erratum explicitly supersedes line 299's singular wording **“the frozen SHA”** and separately names the five instrument identities:

| Instrument | SHA-256 |
|---|---|
| Round-19 wave-1 ruler | `96a68b60538504a8a1b5ead9d5811a2c7bcbf8b427c5934b07e22e16c38585ef` |
| Witness tool | `8dfaa25aa2713635e7363f60effb442a474ba3656d6cf2bb171c0c22432e3a12` |
| Witness runner | `d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b` |
| Round-18 measure | `7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37` |
| Separate round-19 wave-2 frozen ruler | `bb651eefdbe0f85b2d01408ec61e9accebeca8041c20b70982ae698634ff5053` |

It also says the three probes did not all pin the wave-2 ruler and preserves the original round-19 history/verdict. The adjoining S049 note makes the date basis explicit: `2026-10-20` is the original round-14 opening date in local BRT (UTC−03:00), while `2026-10-21` UTC is the round-19 reopening; it states that the source row stays unchanged.

## Commands and observed outputs

- `functions.grep(pattern="frozen SHA|bb651eef|wave-2|round-19 wave-1|96a68b60|8dfaa25a|d22c4025|7ca87a7c", path="/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-19.md", case=false)` — matched the original singular phrase at line 299, the supersession at line 350, and the full instrument identities at lines 356–362.
- `functions.read(path="/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-19.md:275-365")` — showed the existing erratum heading at line 348, its scope statement at lines 350–352, and the five separately identified hashes at lines 356–362.
- `functions.read(path="/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/lessons/round-19.md:367-374")` — showed the S049 date-basis note and unchanged-row statement; the file ends at line 374.
- `functions.read(path="/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-20/w1/D07WordingErratum.md")` — returned `Path ... not found` before this report was written.

No code, build, test, lint, formatter, or final suite was run. No tool was installed.

## Agree / disagree / defects

**Agree:** The current lesson text meets the requested wording correction: it identifies the precise singular phrase being superseded, names each instrument SHA separately, distinguishes the wave-2 ruler from the three probe instruments, and does not state that the historical probes all used that ruler.

**Disagree / defects:** No wording defect in this scoped erratum was observed. The current file places the erratum at EOF, but no comparison against a prior lesson blob was performed; therefore this report does not independently attest that every prior byte was preserved. The erratum itself states that the original bytes remain history.

## Touched surfaces and limits

- Written: only `.ufo/waves/round-20/w1/D07WordingErratum.md`.
- Not written: `corpus/lessons/round-19.md` or any production/tool/corpus file; no Git/JJ state was mutated.
- Out of scope: independent historical-byte comparison and verification of evidence not cited above.
