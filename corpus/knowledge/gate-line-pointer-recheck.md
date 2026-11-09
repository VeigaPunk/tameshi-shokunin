# Gate line-pointer recheck — a cited `line N` is re-derived from the snapshot it names

source: S327 — Jergas, Baethge, "Quotation accuracy in medical journal articles — a systematic
review and meta-analysis", PeerJ 2015 (e1364), Europe PMC REST record (abstract) fetched
2026-11-08, snapshot `.ufo/evidence/round-100/sources/s327.json` 4722 B sha256
`bbd5b0fbb8bafe42b6dbc8a43fcf64b49ba6060f5fbd8f834020a66e2c310c5f`
verified-at: 2026-11-08; receipts `.ufo/evidence/round-100/records/c2-population.out`,
`c2-red-r95-only.out`, `c2-green-r97-only.out`, `c2-green-r99-only.out`, `c2-selftest.out`,
`c2-control-quote-presence.out`, `c2-forgery-r96-pointer.out`, `c2-r95-stated-renderer.out`
(tool bytes executed from the round-100 records revision named in
`.ufo/waves/round-100/records-rev.txt`); instrument `tools/gate-line-recheck.py` sha256
`dae90e50d8d5d447c7a85d77df8e973114355d8ce96e5b78f522b82e88ad3bb9` (unchanged since the
instruments revision `f8f912df`)
recheck: 365d; reopen S327 and re-run the recheck over the newest five lessons
ground: calibration — the lane's own Gate records (rounds 95-99) and the snapshots they cite;
not a frontier row, no coverage-map ground is claimed by this entry

## 1. The question

A lesson's `## Gate` block records where a source says what the lane relies on: a snapshot
path, a `line N` (or `lines N-M`) under the lane renderer, and the quote with its word count.
The lane's existing source checks (`C1_SOURCE … quote:1`, the round-93..99 quote-location
receipts) ask one question: is the quote present in the snapshot? They never ask whether the
line number the Gate prints is the line the quote starts on. Both are self-assessment; the
rendered snapshot is the observed state.

The round-95 non-author closure found the gap by reading (D1,
`corpus/lessons/round-95-verifier-spotcheck.md:172-183`): six round-95 Gate pointers were off
by 2-4 lines under the lane renderer while every quote was verbatim, so every presence check
stayed green.

## 2. What the outside practice says

S327 pooled 28 studies of quotation accuracy in medical articles and states the class plainly:
"Studies indicate, however, that quotations not serving their purpose-quotation errors-may be
prevalent." (12 words, `abstractText`). Its ascertainment distinguishes a citation that
supports the claim from one that merely names a real source; the lane's analogue is a Gate
whose quote is real but whose pointer does not locate it. The lesson taken: a pointer is a
separate claim from the quote and needs its own mechanical check. S328 (Mogull 2017) was
opened and rejected: it re-weights the same error rate per quotation rather than per
reference, and the lane reports no rate (flip in `corpus/SOURCES.md` S328).

## 3. The instrument

`tools/gate-line-recheck.py` (round 100) reads each record and each snapshot as a blob at one
40-hex revision, renders the snapshot with the lane's canonical renderer
(`.ufo/waves/round-93/w1/R93S1-tagstrip.py`: `strip_tags`, `norm_text`, `_bare`, `locate`,
compiled from the blob at that revision), and grades every pointer of every `## Gate` block:

| verdict | meaning |
|---|---|
| `hit` | `line N`: some located span of the quote starts on N; `lines N-M`: some span is exactly (N, M) |
| `miss` | the quote is located, not at the cited line(s); the observed spans are printed |
| `absent` | `locate()` finds no word-sequence match for the extracted quote in the rendered snapshot |
| `unbound` | no extractable quote, no resolvable snapshot, a JSON snapshot, or a non-UTF-8 snapshot |

Exit 0 only when every pointer hits; `unbound` exits 1 (silence is not agreement, round-99
routed item 2). The declared grammar (block, sid, pointer, three-step quote rule, four-step
snapshot binding) is the tool docstring.

## 4. Measurement (round 100)

Over the five round-95..99 lessons at the records revision:
`GATE_LINE_RECHECK records=5 pointers=21 hit=12 miss=6 absent=0 unbound=3`, exit 1. The six
misses are exactly round-95 lines 17-22 (cited 84, 4399, 4393, 4493, 2615, 2355; observed
88, 4403, 4395-4397, 4496-4497, 2618-2619, 2358-2359) — the six D1 pointers. Round 95 alone
exits 1 (`miss=6`); round 97 alone and round 99 alone exit 0 (`hit=2`); `--selftest` 24/24.

The do-nothing control — quote presence anywhere in the rendered snapshot, over the same 21
pointers — prints `flagged_d1=0`: it sees none of the six. A one-pointer forgery (round-96
`4403`→`4399` in a scratch child commit) flips that pointer to `miss`. Under the round-95
Gate's own stated convention (no script/style removal) all six still miss
(`hit_under_stated=0`); the wave's revenger seat tried ten further line renderings and none
reproduces the cited numbers, which were written at `16cf0d58` with no receipt
(`.ufo/waves/round-100/w1/R100RV1.md` F1). An independent re-implementation of renderer and
locate rule agreed on all 21 verdicts and spans (`w1/R100E2.md` F2).

## 5. Limits (declared, and narrowed by the wave)

- A `line N` hit means some occurrence starts on N; a quote occurring twice can hit on an
  occurrence the Gate did not mean. The observed start is the line of the quote's first word
  (`a single header row` starts on 4395, where the round-95 closure wrote 4396 — `w1/R100RV1.md` F3).
- `absent` is `locate()`'s verdict, not presence in the bytes: a lone punctuation token left
  by a tag boundary reduces to an empty word and breaks the match, so a verbatim quote can be
  `absent` (round-77:70, round-88:46; `w1/R100E3.md` F4).
- A markdown table is one block: one sid and one explicit-snapshot fallback serve every row,
  and a quote written before its pointer is not extracted; out-of-set round 89 mis-binds five
  pointers this way (`w1/R100E3.md` F5). A backticked snapshot name inside a quote can become
  the explicit binding (`w1/R100SN1-F7-backtick-in-quote.out`).
- The renderer is code from the lane's own committed file: compiling its four definitions
  runs their decorator and default-argument expressions (`w1/R100R2-receipt-renderer-default-arg.out`,
  `w1/R100SN1-F1-renderer-exec.out`). The trust boundary is the lane blob at `--rev`.
- Only lesson `## Gate` sections are read (an exact `## Gate` header; `## Gate (round 7)` is
  not one — `w1/R100R2-receipt-gate-heading-suffix.out`); plans, SOURCES anchors and reports
  are not.

## 6. Rule

QUALITY criterion 180: a Gate `line N` pointer is written from a receipt that printed the
rendered line, and the round re-runs the recheck over its own lesson before filing.
