seat: ExecJudge01

# Round-45 w2 — C1 falsify review of S012, S062, S157

Inputs read: `.ufo/evidence/round-45/contract.json` (frozen, unedited), `.ufo/evidence/round-45/freshness/ledger.json` at commit
ad5942c6e9858af19d00000b58439b321ddfa62b (73 entries, no duplicate ids), the three committed snapshots under
`.ufo/evidence/round-45/freshness/sources/`, the registry rows in `corpus/SOURCES.md:23,71,127`, and the author reports
`.ufo/waves/round-45/w1/ExecRows03.md`, `ExecRows09.md`, `ExecRows24.md`. I am not the author of any of the three entries.

## Verdicts

S012 agree — reviewer ExecJudge01 — sha equal (today's live fetch, the entry's raw_sha256 and the gunzipped snapshot are all fb6f384d…), the quote is Abstract body text on the arXiv abs page (submitted 17 Aug 2026) naming specification- vs state-anchored expectations that flow from the code under mutation, which is the row's teaches claim, and the same abstract still carries "recover… 8 of 46" and "366 mutants".
S062 agree — reviewer ExecJudge01 — sha equal (9b8f63b6…), the quote is the `--show-toplevel` definition entry inside the "Options for Files" section (section starts at offset 10581, quote at 12274), body content at the row's own anchor, followed by "If there is no working tree, report an error", so it supports both the discovered-top-level and the no-work-tree failure the row claims.
S157 agree — reviewer ExecJudge01 — sha equal (421e3891…), the quote sits in the §dest section (heading "dest ¶" immediately precedes it) and the adjacent text still gives the dash→underscore conversion and "attribute of the object returned by parse_args()", so it supports dest inference, underscore conversion and parse_args attribute assignment.

No dispute. Each quote is 6-25 whitespace tokens (25 / 15 / 15), occurs in the counter's normalized snapshot text, shares ≥2 content
words with scope+anchor+teaches (7 / 6 / 7 distinct), and is not copied from the row's own source/scope/anchor/teaches cells
(checked as substring against each folded cell: all False).

## Commands and output

```
$ mkdir -p /tmp/tameshi-r45-ExecJudge01
$ for id in S012 S062 S157; do gunzip -c …/.ufo/evidence/round-45/freshness/sources/$id.raw.gz > $id.snap; \
    echo "$id $(sha256sum $id.snap|cut -d' ' -f1) bytes=$(stat -c%s $id.snap)"; done
S012 fb6f384d294898d2a154c248261b518e77a3363a4e40ed92f4bf17b35fea2a80 bytes=42588
S062 9b8f63b653029da49bce87f6b292f099dc8f1b3667a85515c92f66a6f5eb2978 bytes=122331
S157 421e389138e80a47df36df8501df89e68fe55ee03dc04816b85cd15c955352e4 bytes=328434
```

```
$ for id in S012 S062 S157; do url=<entry.url>; curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o $id.live "$url"; \
    echo "$id url=$url rc=$? sha=$(sha256sum $id.live|cut -d' ' -f1) bytes=$(stat -c%s $id.live)"; done
S012 url=https://arxiv.org/abs/2608.17214 rc=0 sha=fb6f384d294898d2a154c248261b518e77a3363a4e40ed92f4bf17b35fea2a80 bytes=42588
S062 url=https://git-scm.com/docs/git-rev-parse rc=0 sha=9b8f63b653029da49bce87f6b292f099dc8f1b3667a85515c92f66a6f5eb2978 bytes=122331
S157 url=https://docs.python.org/3/library/argparse.html rc=0 sha=421e389138e80a47df36df8501df89e68fe55ee03dc04816b85cd15c955352e4 bytes=328434
```

sha256 comparison lines (live vs entry.raw_sha256 vs gunzip snapshot):

```
S012 live==entry==snapshot : fb6f384d294898d2a154c248261b518e77a3363a4e40ed92f4bf17b35fea2a80  (equal, 42588 B)
S062 live==entry==snapshot : 9b8f63b653029da49bce87f6b292f099dc8f1b3667a85515c92f66a6f5eb2978  (equal, 122331 B)
S157 live==entry==snapshot : 421e389138e80a47df36df8501df89e68fe55ee03dc04816b85cd15c955352e4  (equal, 328434 B)
```

All three are byte-identical to today's live fetch, so provenance is confirmed without needing the dynamic-chrome fallback; no
`--member` is set on any of the three entries. Entry fields: opened 2026-10-25, verdict `holds`, authors ExecRows03 / ExecRows09 /
ExecRows24, each URL exactly the first http(s) URL of its row's source cell.

```
$ python3 …/.ufo/evidence/round-45/freshness/measure.py --extract /tmp/tameshi-r45-ExecJudge01/$id.snap
S012 rc=0 textbytes=5061
S062 rc=0 textbytes=34014
S157 rc=0 textbytes=85724
```

Located context (a few words either side of the quote):

- S012, quote at offset 881 of 5052: `… We call this oracle anchoring. [An expectation is specification-anchored when composed from values fixed outside the code under mutation, and state-anchored when it flows, directly or transitively, from that code.] The expected-value form is named in the test-smell literature but not measured in any study we retrieved. …`
  Abstract block confirmed: `[2608.17214] … [Submitted on 17 Aug 2026] … Authors: Arquimedes Canedo … Abstract: A test oracle that obtains its expected value from the system it is judging cannot fail. …`; teaches corroborated at `… Re-anchoring one holding oracle on published procedure, changing no production code, recovers 8 of 46; …` and `Across 4 modules and 366 mutants …`.
- S062, quote at offset 12274 of 33933: `… "git rev-parse --git-path objects/abc" returns /foo/bar/abc. [--show-toplevel Show the (by default, absolute) path of the top-level directory of the working tree.] If there is no working tree, report an error. --show-superproject-working-tree …`
  Section: heading `Options for Files` at offset 10581, quote at 12274 inside it (next option entries `--show-cdup`, `--show-prefix`, `--show-object-format` follow in the same section); page body, not nav/footer.
- S157, quote at offset 48117 of 85631: `… >>> parser . parse_args ([ 'XXX' ]) Namespace(bar='XXX') [For optional argument actions, the value of dest is normally inferred from the option strings.] ArgumentParser generates the value of dest by taking the first double-dash long option string and stripping away the initial - characters. … Any internal - characters will be converted to _ characters to make sure the string is a valid attribute name. …`
  Section: heading `dest ¶` precedes the quote; the same section opens with `Most ArgumentParser actions add some value as an attribute of the object returned by parse_args() .`; the `The parse_args() method` section exists at offset 548 of the TOC/navigation and its body is present later in the text.

## Notes / risks

- No pacman, no installs, no network writes beyond `curl` GETs to the three registry URLs; no git/jj command was run in the lane and nothing in the lane was modified except this report file (plus creating the `.ufo/waves/round-45/w2/` directory it lives in).
- Scratch: `/tmp/tameshi-r45-ExecJudge01/` (`S0*.snap`, `S0*.live`, `S0*.txt`, `reviews.json`).
- `reviews.json` for merging into `.ufo/evidence/round-45/freshness/reviews.json` was written to `/tmp/tameshi-r45-ExecJudge01/reviews.json` (lane is read-only for me); its `report` field is `.ufo/waves/round-45/w2/ExecJudge01.md`.
- All three rows would be `verified` on the counter's own predicate; my independent judgment does not downgrade any of them. Nothing here changes the population or the target.
