# B04SrcRfc8259 — report

Lane tip: 183f87b899e6cae46be98d251cbc87fb5118f6ca. Access date 2026-10-20. Scope: C2 P09 (JSON numbers exclude NaN and Infinity, RFC 8259 §6).

## Decision

**New row, provisional id S068, status `mined`.** Draft: `.ufo/waves/round-18/sources/S068-B04SrcRfc8259.md`.

Duplicate check (no duplicate, no reject):
- Command: `grep -n 'rfc8259\|rfc-editor\|RFC 8259' corpus/SOURCES.md` → no output, exit 1.
- Result: no existing row carries this URL or this RFC; the draft is not `DUPLICATE`.

Source open:
- `read https://www.rfc-editor.org/rfc/rfc8259` → full text returned (Metadata: Published December 2017, Obsoletes RFC 7159, errata https://www.rfc-editor.org/errata/rfc8259). No mirror needed.

## Gate evidence

- §6 Numbers, the sentence before the `number` grammar, verbatim (18 words, `wc -w` = 18; the plain-text RFC wraps after "(such"):
  "Numeric values that cannot be represented in the grammar below (such as Infinity and NaN) are not permitted."
- Corroboration: `grep` over the whole fetched RFC text for `NaN|Infinity` returns exactly that one line (RFC text line 315-316).

## Row shape check

- 11 cells; piped with leading/trailing `|` gives NF=13 as the CORPUS census requires.
- Kind `spec`, tier `A` scoped to "JSON number grammar", opened 2026-10-20, recheck `365d`.
- `used-by` = `.ufo/evidence/round-18/` (provisional; exists, so census `[ -e ]` passes). L1 must replace it with the concrete citing file once it exists, because `mined` requires a real citing path.

## Findings / caveats

1. Id conflict: `corpus/SOURCES.md` says "Next unused id: S065", but sibling drafts S065 (B01, Stryker states, duplicate of S001) and S076 (B12, subprocess) already exist in `.ufo/waves/round-18/sources/`. L1 must assign the id at merge; S068 is provisional as the Target says.
2. Teaches wording: the RFC sentence says such values "are not permitted" and carries no RFC 2119 keyword. The row's "must refuse" phrasing for `timeout_s` is a consequence [INFERENCE], not a literal §6 requirement; the Gate notes this.
3. No tools installed or updated. No file writes outside the owned draft and this report. No git commands run. No subagents spawned.

## Verdict

built
