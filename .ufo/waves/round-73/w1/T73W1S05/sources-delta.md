# corpus/SOURCES.md delta — round 73 (seat T73W1S05, scribe)

Draft only. This seat did not edit `corpus/SOURCES.md`; the L1 lands every
production byte. Observation time: 2026-11-04T01:05Z (2026-11-03 22:05 -03).

## 0. State observed — one repair finding and two premise checks

The delta is already committed at `be1199d3` ("round-73: C1 record edits
(SOURCES S066 re-open, QUALITY criteria 121-123, pointer-recheck note count)")
and is present at `origin/master` `3e0ef1c8`. **Its S066 row is malformed**:
10 pipe-fields (8 columns) instead of 13 fields (11 columns). The used-by
append collapsed the row — it dropped the `teaches` tail
`[INFERENCE: refusing it is a design choice]` and the `status` / `opened` /
`recheck` cells (`mined`, `2026-10-20`, `365d`).

Measured:

```
$ python3 - <<'EOF'   # per-rev S066 row structure
... cells=len(row.split('|')) ...
EOF
be1199d3 cells= 10 fields= 8 usedby= MISSING
2e89e539 cells= 10 fields= 8 usedby= MISSING
7982619f cells= 10 fields= 8 usedby= MISSING
4ebf7a1e cells= 10 fields= 8 usedby= MISSING
3e0ef1c8 cells= 10 fields= 8 usedby= MISSING

$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
1

$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
...
tameshi	E01	S066 fields=8
...
census_exit=1
```

The paste-ready repair is §1: replace the whole S066 line with the corrected
row. Do **not** splice the used-by cell into the 8-field line — the line has
already lost three cells and the teaches tail.

**Resolution (observed at 2026-11-04T01:06Z):** the L1 committed the repair at
`1d118c14cce63fc78bac7d3095056d60a11ed8f5` ("round-73: S066 row repair
(restore the four cells the used-by append collapsed; census exit 0)").
Re-check on the repaired tree: S066 = 13 fields with the teaches
`[INFERENCE: …]` tail and `mined | 2026-10-20 | 365d`, `NF!=13` → 0,
`sources-census.sh validate` → `tameshi ok`, exit 0, and the §1 row below is
byte-identical to `HEAD`'s row. The finding, its class and the repair are in
this seat's report (`.ufo/waves/round-73/w1/T73W1S05.md`).

Premise checks:

- **There is no Round 72 tail note.** `git show a3dd3574:corpus/SOURCES.md |
  grep -c 'Round 72'` → `0`; the last bullet is Round 71. Round 72 appended row
  S303 (commit `d618518a`) without a tail bullet. This round's note therefore
  follows the Round 71 bullet, not a Round 72 one.
- **`origin/master` is now `3e0ef1c8`**, not the frozen base
  `a3dd35742eee608d1205843dacebc461b4242b9e`. The frozen base is an ancestor
  (`git merge-base --is-ancestor a3dd3574 origin/master` → exit 0); the
  plan's "base = origin/master" held at freeze, not at this observation.

## 1. S066 `used-by` cell (old → new)

Contract: `CORPUS.md` rule 2 — only `status`, `recheck` and `used-by` change
in place. Every other cell stays byte-identical, including the `teaches`
cell's trailing `[INFERENCE: refusing it is a design choice]`.

Old (trimmed):
`corpus/knowledge/guard-kill-closure.md`

New (trimmed):
`corpus/knowledge/guard-kill-closure.md, corpus/lessons/round-73.md`

Exact cell bytes in the table:

- old: `| corpus/knowledge/guard-kill-closure.md |`
- new: `| corpus/knowledge/guard-kill-closure.md, corpus/lessons/round-73.md |`

No `status`/`recheck` change: `mined` / `365d` (opened `2026-10-20`) stay as
written; the re-open appends the round-73 lesson only.

### Paste-ready replacement for line 75 (full 11-column row)

```markdown
| S066 | RFC 8259: The JavaScript Object Notation (JSON) Data Interchange Format (T. Bray, Ed.; IETF Standards Track) — https://www.rfc-editor.org/rfc/rfc8259 | spec | A | JSON number grammar: whether NaN and Infinity are valid JSON numbers | §6 Numbers, sentence before the `number` grammar @ RFC 8259, December 2017 (obsoletes RFC 7159), fetched 2026-10-20 | numeric values the number grammar cannot represent, such as Infinity and NaN, are not permitted in JSON, so a registry timeout_s that is NaN or Infinity is outside the grammar; §6 does not say what a parser must do with them [INFERENCE: refusing it is a design choice] | mined | 2026-10-20 | 365d | corpus/knowledge/guard-kill-closure.md, corpus/lessons/round-73.md |
```

This line is the base row at `a3dd3574` with only cell 11 (`used-by`) changed:
old length 700 chars / 13 fields, new length 728 chars / 13 fields (the
appended `, corpus/lessons/round-73.md` is 28 chars).

Repair verification, on a scratch lane whose only changed bytes are the S066
row (`corpus/knowledge`, `corpus/lessons` and `tools` are symlinks to the real
lane):

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' .../corpus/SOURCES.md
163

$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' .../corpus/SOURCES.md
0

$ bash scripts/sources-census.sh validate /fast/scratch/hyaku/tameshi-r73/T73W1S05/censusroot/tameshi-shokunin
tameshi-shokunin	W04	S047 duplicate url pitest.org/quickstart/incremental_analysis across scopes
... (18 W04 + 1 W01 lines, the pre-existing warning set, S303's expected duplicate-URL warning included)
tameshi-shokunin	ok	/fast/scratch/hyaku/tameshi-r73/T73W1S05/censusroot/tameshi-shokunin/corpus/SOURCES.md
exit=0
```

Zero E codes on the repaired row; the committed row reads `E01 S066 fields=8`
(§0).

## 2. Re-open anchor / quote material

### Fetch record

| field | value |
|---|---|
| source | RFC 8259, *The JavaScript Object Notation (JSON) Data Interchange Format* (T. Bray, Ed.) |
| canonical URL (row) | https://www.rfc-editor.org/rfc/rfc8259 |
| text form fetched | https://www.rfc-editor.org/rfc/rfc8259.txt |
| HTTP date | `Wed, 04 Nov 2026 00:58:08 GMT` (2026-11-03 21:58 -03 local) |
| Content-Length | **absent** from the receipt — `grep -ic 'content-length' rfc8259-headers.txt` → `0` (exit 1). The response is `HTTP/2 200` (`cf-r2-served: 1`), where the header is optional. The observed body size is 28360 B (`wc -c`); do not write a Content-Length value the receipt does not carry. |
| observed size | 28360 B; 899 lines; 16 form feeds (16 pages); ends `[Page 16]`; no BOM |
| sha256 | `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7` |
| extract | `.ufo/evidence/round-73/sources/rfc8259.txt` |
| headers | `.ufo/evidence/round-73/sources/rfc8259-headers.txt` (sha256 `7826ea14f7faaf10662b481d78c499d1794922a8655e28f167e4e1e8a2f80a4d`, 694 B) |
| ETag | `W/"effcde61d580b8bb9e8eb8fdca283c5f"` |
| canonical link header | `<https://www.rfc-editor.org/info/rfc8259/>; rel="canonical"` |

Commands and outputs:

```
$ sha256sum .ufo/evidence/round-73/sources/*
7826ea14f7faaf10662b481d78c499d1794922a8655e28f167e4e1e8a2f80a4d  rfc8259-headers.txt
61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7  rfc8259.txt

$ wc -c rfc8259.txt
28360 rfc8259.txt

$ grep -ic 'content-length' rfc8259-headers.txt
0
   (exit 1)

$ grep -i '^date:\|^etag:\|^content-type:\|^link:' rfc8259-headers.txt
date: Wed, 04 Nov 2026 00:58:08 GMT
content-type: text/plain;charset=utf-8
etag: W/"effcde61d580b8bb9e8eb8fdca283c5f"
link: <https://www.rfc-editor.org/info/rfc8259/>; rel="canonical"

$ python3 -c "b=open('rfc8259.txt','rb').read(); print('bytes',len(b),'formfeeds',b.count(b'\x0c'),'bom',b[:3]==b'\xef\xbb\xbf')"
bytes 28360 formfeeds 16 bom False
```

### The three located quotes (§8.1 Character Encoding, page lines 483–499)

| # | page lines | words | quote (verbatim) |
|---|---|---|---|
| Q1 | 485–486 | 18 | "JSON text exchanged between systems that are not part of a closed ecosystem MUST be encoded using UTF-8" |
| Q2 | 494–495 | 17 | "Implementations MUST NOT add a byte order mark (U+FEFF) to the beginning of a networked-transmitted JSON text." |
| Q3 | 496–498 | 21 | "implementations that parse JSON texts MAY ignore the presence of a byte order mark rather than treating it as an error" |

Count method: whitespace-separated tokens of the quoted span
(`python3` `len(q.split())`; `wc -w` agrees). Outputs:

```
$ wc -w q1.txt q1full.txt q2.txt q3.txt q3full.txt
 18 q1.txt
 19 q1full.txt
 17 q2.txt
 21 q3.txt
 26 q3full.txt
101 total
```

Quote-boundary caveats (both counts are still ≤ 25 as listed):

- Q1 as quoted stops before the bracketed citation. The page line reads
  `... MUST be encoded using UTF-8 [RFC3629].`; including the citation makes
  **19** words on the same lines 485–486. Use 18 if the span stops at
  `UTF-8`, 19 if the whole sentence including `[RFC3629].` is quoted.
- Q3 is a mid-sentence fragment. The full sentence starts
  `In the interests of interoperability,` and is **26** words (lines
  495–498), over the ≤25 cap; the 21-word fragment (lines 496–498) is the
  conforming span. Mark the elision outside the quoted span if house style
  requires it.

Verbatim check: each quoted span is a substring of the extract after
collapsing the RFC's line wrapping, at these page lines and normalized-text
offsets:

```
q1-18  words= 18 lines= (485, 486) norm_off= 15757
q1-full words= 19 lines= (485, 486) norm_off= 15757
q2     words= 17 lines= (494, 495) norm_off= 16150
q3-21  words= 21 lines= (496, 498) norm_off= 16300
q3-full words= 26 lines= (495, 498) norm_off= 16262
```

The section's raw lines (page numbering as printed in the extract):

```
483:8.1.  Character Encoding
485:   JSON text exchanged between systems that are not part of a closed
486:   ecosystem MUST be encoded using UTF-8 [RFC3629].
494:   Implementations MUST NOT add a byte order mark (U+FEFF) to the
495:   beginning of a networked-transmitted JSON text.  In the interests of
496:   interoperability, implementations that parse JSON texts MAY ignore
497:   the presence of a byte order mark rather than treating it as an
498:   error.
```

Grounding for the re-open: `tools/wave-reconcile.py:36-37` — "artifact bytes
decode as UTF-8; a UTF-8 BOM is refused as setup exit 2 naming the artifact
(S066 §8.1: a BOM is not part of a JSON text, and this reader refuses it
rather than silently stripping bytes the emitter said are not JSON)" — and
`:75` — "Strict: UTF-8 only, a BOM is refused and never stripped (S066
§8.1)". The `bom-present` setup exit 2 is the RFC's MAY-ignore alternative
declined: §8.1 permits either, so the fail-closed choice is a design choice,
not a requirement of the RFC.

## 3. Round-73 tail note (paste-ready)

Append after the Round 71 bullet, separated by one blank line (the
r54–r57/r61 convention). Do not modify any earlier bullet.

```markdown
- Round 73: NO new row — the sourced C1 claim rests on S066, **RE-OPENED** this round for §8.1's encoding ground (a JSON text's UTF-8 encoding and the byte-order-mark rule) while S066's §6 number-grammar scope stands as written; the re-open is the curation delta, not a row. Fetch 2026-11-04 (HTTP date `Wed, 04 Nov 2026 00:58:08 GMT`): `https://www.rfc-editor.org/rfc/rfc8259.txt`, 28360 B (`wc -c`; the receipt carries no `content-length` header — HTTP/2, `cf-r2-served: 1`), sha256 `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7`, extract `.ufo/evidence/round-73/sources/rfc8259.txt` (+ `rfc8259-headers.txt`); the three located quotes (18, 17 and 21 words, page lines 485–486, 494–495, 496–498) are in `corpus/lessons/round-73.md` `## Gate`. S066 `used-by` old → new: `corpus/knowledge/guard-kill-closure.md` → `corpus/knowledge/guard-kill-closure.md, corpus/lessons/round-73.md` (logged in the same Gate; `status` `mined`, opened `2026-10-20`, recheck `365d` unchanged). A new row on the held URL was refused **before staging** as a within-scope duplicate for the same document (CORPUS.md rule 2; the S289/S293 precedent, re-sampled by the round-72 non-author closure at `corpus/lessons/round-72-verifier-spotcheck.md:169`) — flip: the §6 scope is retired, or the document is superseded by a new RFC, whose successor is then a new document with a new row. Registry rows 163 → 163. Next unused id: S304 (staged ids S161–S255 stay reserved by document for the package).
```

Note on the committed copy: `be1199d3`'s tail note already says substantially
this; the two deltas in this draft are (a) the size provenance `28360 B
(wc -c; no content-length header)` and (b) the explicit "the re-open is the
curation delta". Neither changes a claim. The committed note's quote counts
(18/17/21) and page lines (485–486, 494–495, 496–498) are verified correct.

## 4. Gate material (LEARNING.md Gate duty: candidates, admits, rejects with reasons)

The committed `corpus/lessons/round-73.md` `## Gate` already carries this
pair accurately (verified against §2). This is the paste-ready restatement.

### ADMIT — S066 §8.1 re-open (the curation delta)

RFC 8259 is already held as S066 for §6's number grammar; this round opens
the same document at §8.1 for the C1 instrument's BOM/UTF-8 decision. The
three located quotes are Q1 (UTF-8 MUST, 485–486, 18 words; 19 with the
bracketed citation), Q2 (BOM MUST NOT be added, 494–495, 17 words) and Q3
(the MAY-ignore alternative the instrument declines, 496–498, 21 words).
`tools/wave-reconcile.py` grounds its strict decode and its `bom-present`
setup exit 2 on this section (`:36-37`, `:75`).

- **Reason:** the claim — a BOM is a setup failure, never silently stripped —
  is only as good as the RFC sentences it cites; the fresh fetch re-locates
  them at 485–486, 494–495 and 496–498 and pins the bytes
  (`61a5378f…`, 28360 B). §6's scope and the row's `status`/`opened`/`recheck`
  are unchanged.
- **Flip:** a revision of RFC 8259 that changes §8.1's UTF-8/BOM text, or a
  successor RFC that obsoletes this one, makes these spans stale; the row is
  then re-opened again or superseded by a new row (CORPUS.md rule 2's
  correction mechanism).

### REJECT — a new row for the held RFC 8259 URL

- **Reason:** the URL is already held as S066 (tier A, spec, `mined`); a
  second row for the §8.1 ground would be a within-scope duplicate for the
  same document, adding no new document and no new tier judgement. CORPUS.md
  rule 2 allows only `status`/`recheck`/`used-by` to change in place; the
  lane's precedent is the S289/S293 standing rejection (S293 refused as a
  within-scope duplicate of S289's `git-cat-file` URL; re-sampled and agreed
  by the round-72 non-author closure at
  `corpus/lessons/round-72-verifier-spotcheck.md:169`). The curation delta is
  the re-open, not a row.
- **Flip:** the §6 scope is retired, or RFC 8259 is superseded by a new RFC —
  the successor is a new document and gets a new row.

### Price-outs (this seat, drafting; NOT opened this round)

Only RFC 8259 was opened this round (the evidence dir holds only
`rfc8259.txt` and `rfc8259-headers.txt`). These are price-outs, kept only if
the L1 wants them in the Gate; none is a row.

Held-page greps at base (`git show a3dd3574:corpus/SOURCES.md`):

```
rfc3629          0
RFC 3629         0
unicode.org      0
utf-8-sig        0
byte order mark  0
UTF-8            0
BOM              0
```

- **RFC 3629 (UTF-8)** — unheld; §8.1's normative sentence already carries
  the UTF-8 requirement and cites RFC 3629 for the encoding itself. No claim
  in this round needs RFC 3629's own well-formedness/ABNF. Flip: a future
  claim about overlong encodings or surrogate ranges opens it as its own row.
- **The Unicode Standard's U+FEFF/BOM definition** — unheld; §8.1 names
  U+FEFF, and the instrument's rule is "refuse", not "interpret" the
  character. Flip: a claim that must classify a BOM as a character rather
  than bytes opens the relevant Unicode chapter.
- **Python `codecs` / `utf-8-sig` documentation** — unheld; the tool uses
  strict UTF-8 and refuses the BOM, and the codec docs would ground only a
  strip-BOM design, which the lane rejects. Flip: if `utf-8-sig` is ever
  adopted, the codec documentation becomes the ground and needs a row.

## 5. Landing checklist

1. Line 75 is already repaired at `1d118c14`; the §1 row matches it
   byte-for-byte. If any later edit re-touches the row, replace the whole
   line — do not splice the used-by cell into a collapsed line.
2. Append the §3 tail note after the Round 71 bullet, one blank line before
   it; no earlier bullet changes.
3. Run the frozen census: `grep -cE '^\|…'` → 163 and the `NF!=13` awk → 0;
   then `bash scripts/sources-census.sh validate --root
   /home/vgpnk/Projects/shokunin tameshi` → exit 0, the 18 W04 + 1 W01
   pre-existing set, no E codes.
4. Keep the lesson's `## Gate` pair (§4); the committed text already matches
   the verified counts and lines.

Out of scope for this seat: no edit to `corpus/SOURCES.md`,
`corpus/lessons/round-73.md`, or any tracked file; no counter run for C1/C2;
no git mutation.
