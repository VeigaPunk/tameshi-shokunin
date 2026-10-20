# ReopenS066 — independent re-open of source row S066 (RFC 8259 §6)

Seat: TameshiR18.ReopenS066 (wave 2, source-row re-open).
Read rev: `01d586ddbc5fcd78659557c4e93a6ee8517b87d1` (lane `HEAD` at this seat's start; `git rev-parse HEAD` exit 0).
Opened: 2026-10-20 (`date -Iseconds` → `2026-10-20T17:29:14-03:00`).

Target row: `corpus/SOURCES.md:75` at the read rev — id S066, RFC 8259, kind `spec`, tier `A`,
status `mined`, used-by `corpus/knowledge/guard-kill-closure.md`.
Target quote: `.ufo/waves/round-18/staged/lesson-round-18-gate.md:18` at the read rev.

## Verdict

**Holds.** Every check in the ticket passes: the quote is verbatim at the anchor, is 18 words
(≤25), the teaches cell does not overstate the page, kind/tier fit the frozen contract, and the
used-by path exists and cites S066. Two non-blocking wording notes are recorded below; neither
changes the verdict.

## Evidence opened

| source | bytes / lines | sha256 |
|---|---|---|
| `corpus/SOURCES.md` @ rev (git show) | 13 columns for S066; row at line 75 | `1d4b5910d2ef3e4acbf09a0dfaab61f5ba0e979fb8bc1c99d7241eee5d274e37` |
| `.ufo/waves/round-18/staged/lesson-round-18-gate.md` @ rev | quote at line 18 | `a4f94cd79c08564aad7e3fb59d74235a9450a39dcfae508af29ddd2fbfd9a6d8` |
| `corpus/knowledge/guard-kill-closure.md` @ rev (used-by) | 136 lines, 21712 B | `9312bdebd4e93d427ea32d3db8652f95530237477b49ffecffdf4e4ac49991fb` |
| `https://www.rfc-editor.org/rfc/rfc8259.txt` (fetched 2026-10-20) | 899 lines | `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7` |
| `https://www.rfc-editor.org/rfc/rfc8259.html` (canonical URL, fetched 2026-10-20) | 37946 B | `5302d6ccb6cf221817bdd1f8cd7221661d4519372e0ac0b4cf641e11e8037de7` |
| RFC 8259 errata search (`errata_search.php?rfc=8259`, fetched 2026-10-20) | 93417 B | `a39b43751fc2be571adb00005df89cd97393275f8707ba4cef9b16a2b513302e` |
| fleet `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` (frozen contract) | 81 lines | `6c674a2281afb75b2de11790ebfe34fdcf7ddde61a6734d2eca302f023966119` |

## Checks

### 1. Quote verbatim at the stated anchor — PASS

Registry quote (line 75) and Gate quote (line 18) are the same string:

> "Numeric values that cannot be represented in the grammar below (such as Infinity and NaN) are not permitted."

- `sed -n '362,380p'` of the RFC .txt shows heading `6.  Numbers` (line 362), the sentence at
  lines 377–378, and `number = [ minus ] int [ frac ] [ exp ]` at line 380 — the sentence is
  exactly the one immediately before the `number` grammar, as the anchor cell states.
- .txt whitespace-flattened match: `verbatim_txt_flat: True`.
- Served HTML, tags stripped and whitespace normalised: `verbatim_html: True`; the context reads
  `...are not permitted. number = [ minus ] int [ frac ] [ exp ]`; the last heading before the
  quote in the HTML text is `6. Numbers` (proximity regex over the stripped page).
- The Gate's parenthetical location `(§6 Numbers)` and the row's more precise
  `§6 Numbers, sentence before the \`number\` grammar` agree with the page.
- `/tmp` scratch note: fetches were first written to bare `/tmp`, then moved to the sanctioned
  `mktemp -d /tmp/tameshi-r18w2-ReopenS066-lIP9mL`; bare `/tmp/rfc8259*` no longer exists
  (`ls` exit 2). No lane file other than this report was written.

### 2. Length ≤25 words — PASS

`len(q.split())` = **18** (same string from both the row and the Gate table). Contract
`.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:47` requires a ≤25-word quote.

### 3. Anchor metadata — PASS

RFC header (`sed -n '1,12p'`): `Request for Comments: 8259`, `Obsoletes: 7159`,
`December 2017`, `Category: Standards Track`, `T. Bray, Ed.`; title line: `The JavaScript
Object Notation (JSON) Data Interchange Format`; Status of This Memo: "This is an Internet
Standards Track document." This matches the row's `source` cell (title, T. Bray Ed., IETF
Standards Track) and anchor revision (`December 2017 (obsoletes RFC 7159)`).
The row's `fetched 2026-10-20` matches the system date and this seat's fetch.

Verified errata do not disturb the anchor: the errata search reports 5 verified errata; the only
one touching §6 (Errata-ID 7600) rewrites the "Leading zeros are not allowed" sentence, not the
quoted Infinity/NaN sentence. No erratum's replacement text contains `Infinity`/`NaN`/`not
permitted` as a correction (the only `Infinity` hit is inside 7600's quoted "Section 6 says"
original).

### 4. Teaches cell does not overstate the page — PASS

Cell text (`corpus/SOURCES.md:75`): "numeric values the number grammar cannot represent, such as
Infinity and NaN, are not permitted in JSON, so a registry timeout_s that is NaN or Infinity is
outside the grammar; §6 does not say what a parser must do with them [INFERENCE: refusing it is a
design choice]".

- Clause 1 mirrors the quoted sentence (the only addition is the contextual "in JSON", warranted
  by RFC title/§6).
- Clause 2 ("a registry timeout_s ... outside the grammar") is a direct instantiation for the
  literal spellings `NaN`/`Infinity`; the lane's probe feeds exactly those literals
  (`.ufo/evidence/round-18/defect-probes.py:581`: `for literal in ("NaN", "Infinity")`).
- Clause 3 ("§6 does not say what a parser must do with them") is true of §6, and the quoted
  sentence carries no RFC 2119 keyword (`keywords: []`; §1.1 at .txt lines 183–186 is the RFC's
  2119/8174 boilerplate, so the absence is meaningful). RFC §9 (.txt lines 543–545) is the
  page's parser clause — `MUST accept all texts that conform to the JSON grammar`, `MAY accept
  non-JSON forms or extensions` — which supports, rather than contradicts, the bracketed
  inference that refusing is a design choice. The inference is therefore conservative, not an
  overstatement.
- The page's own §6 range paragraph (.txt lines 407–421) allows implementations to set
  range/precision limits and calls `1E400` a JSON number with "potential interoperability
  problems". See note O1 for the only imprecision this creates.

### 5. Kind/tier fit — PASS

Contract `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:24` enumerates `spec`; an RFC is a
specification, so `kind=spec` fits. `:26–30` defines tier A as "primary or authoritative for
that scope (spec, official docs, source code, original paper, maintainer statement …)"; the scope
cell is "JSON number grammar: whether NaN and Infinity are valid JSON numbers", for which RFC
8259 is the IETF Standards Track document (header text above). Tier A is not inflation; the
`community`-never-A rule does not apply. `scope` is the claim the tier is scoped to, and the
`anchor` gives section + revision date, satisfying `:31–33`.

### 6. Used-by path exists and cites S066 — PASS

`used-by` names exactly one path, `corpus/knowledge/guard-kill-closure.md`.
`git cat-file -s 01d586dd…:corpus/knowledge/guard-kill-closure.md` → `21712` (exists).
The file cites S066 twice:

- line 1 (`source:` header): `S066 — RFC 8259 §6 Numbers, https://www.rfc-editor.org/rfc/rfc8259`;
- line 57: "RFC 8259 §6 states that numeric values not representable in the grammar, such as
  Infinity and NaN, are not permitted [src: S066, quote]. That sentence has no RFC 2119 keyword.
  Rejecting a non-finite `timeout_s` with exit 2 is a design choice, not a quoted requirement
  [src: S066, Gate note]."

The derived use is substantive (the knowledge entry's §3 rests on the S066 prohibition and on
its non-normative wording), so `status=mined` is supported under the contract's `mined` = cited
by ≥1 used-by path (`:34`). No missing used-by path.

## Minor observations (non-blocking)

- **O1 — literal vs parsed value.** The row's "a registry timeout_s that is NaN or Infinity is
  outside the grammar" is exact for the literal tokens `NaN`/`Infinity`. A grammar-valid token
  such as `1e400` also parses to `+inf` in Python (`json.loads` check: `1e400 inf finite=False`)
  and is rejected by the lane's `math.isfinite` gate (`tools/registry-check.py:240`), but that
  token is inside the grammar; its rejection rests on §6's allowed range/precision limits
  (.txt lines 407–421), not on the quoted prohibition. The lane's actual probe uses only the
  literals, so no live misuse; adding "literal" would remove the ambiguity.
- **O2 — §9 pointer.** The row's "§6 does not say what a parser must do" is literally true, but
  RFC §9 is the clause that actually grounds "refusing is a design choice" (`MAY accept non-JSON
  forms or extensions`). Citing §9 alongside §6 would strengthen the same inference; its absence
  is not an overstatement.
- **O3 — Gate change-note phrasing.** `.ufo/waves/round-18/staged/lesson-round-18-gate.md:65`
  says the draft's "a registry timeout_s … must refuse them" "is marked
  `[INFERENCE: refusing it is a design choice]`". The installed row does not retain "must refuse
  them": the draft (`.ufo/waves/round-18/sources/S068-B04SrcRfc8259.md:11`) said "must refuse them
  rather than accept them", and the installed row replaces that with "§6 does not say what a
  parser must do with them [INFERENCE: refusing it is a design choice]". The note is loose about
  whether the draft wording survived; the row itself is correct. Documentation nit only.

## Commands run (key lines, exits)

```
git -C <lane> show 01d586dd…:corpus/SOURCES.md | grep -n S066                  # exit 0 → :75; also :207
git -C <lane> show 01d586dd…:corpus/SOURCES.md | awk -F'|' '… S066 …'          # exit 0 → NF=13
git -C <lane> show 01d586dd…:.ufo/waves/round-18/staged/lesson-round-18-gate.md | grep -n S066   # exit 0 → :18,:48,:65,:72
curl -sS https://www.rfc-editor.org/rfc/rfc8259.txt -o <scratch>/rfc8259.txt     # exit 0, 899 lines
curl -sS https://www.rfc-editor.org/rfc/rfc8259.html -o <scratch>/rfc8259.html   # exit 0, 37946 B
python3 … whitespace/tag-normalised match                                        # verbatim_txt_flat True; verbatim_html True
python3 -c 'len(q.split())'                                                      # 18
sed -n '362,380p' <scratch>/rfc8259.txt                                          # §6 heading, sentence, number grammar
grep -n 'Obsoletes: 7159|December 2017|Category: Standards Track' <scratch>/rfc8259.txt  # exit 0 → :9,:10
sed -n '543,545p' <scratch>/rfc8259.txt                                          # parser MUST/MAY clause
curl -sSL 'https://www.rfc-editor.org/errata_search.php?rfc=8259'                # exit 0, 93417 B; 5 verified
git -C <lane> cat-file -s 01d586dd…:corpus/knowledge/guard-kill-closure.md       # exit 0 → 21712
git -C <lane> show 01d586dd…:corpus/knowledge/guard-kill-closure.md | grep -n S066  # exit 0 → :1,:57
git -C <lane> grep -n 'must refuse them' 01d586dd… -- .                          # exit 0 → sources/S068-B04SrcRfc8259.md:11
date -Iseconds                                                                   # 2026-10-20T17:29:14-03:00
```

## Residual unknowns

- None blocking. The page was fetched once from rfc-editor.org on 2026-10-20 and matched in both
  .txt and HTML renderings; no independent mirror was compared (not needed for the quote/anchor
  checks). Errata were checked and do not alter the quoted sentence.
- Contract file location caveat is pre-existing (lane `corpus/SOURCES.md:4` names
  `SOURCES-CONTRACT-v1.md` by bare name; the frozen copy is at fleet
  `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`, as round-12/15 noted); this re-open used the fleet
  copy for the tier/kind rubric.

VERDICT: holds — S066's quote is verbatim (18 words) at RFC 8259 §6 immediately before the `number` grammar, teaches does not overstate the page, spec/A fit the frozen contract, and `corpus/knowledge/guard-kill-closure.md` exists at 01d586dd… and cites S066 at :1 and :57.
