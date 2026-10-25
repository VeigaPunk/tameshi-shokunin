seat: ScribeRows
item: drafted the three round-46 C3 registry rows S258/S259/S260 (arXiv 2504.16777, the TUM portal record of the IEEE TSE 2026 paper, the Google Testing Blog per-post feed) in the 11-column `corpus/SOURCES.md` schema, each grounded on its committed snapshot and each naming the single knowledge entry it feeds

# ScribeRows — round-46 C3 rows (S258, S259, S260)

Read-only on the lane. I wrote exactly two files, both under
`.ufo/waves/round-46/w1/`: this report and the deliverable `ScribeRows.rows.md`.
Scratch lives in `/tmp/tameshi-r46-ScribeRows/`. No git or jj command was run in the
lane; no pacman, no tool install.

Sources of truth read: `.ufo/evidence/round-46/contract.json` (C3 surface),
`/home/vgpnk/Projects/shokunin/CORPUS.md` §SOURCES.md (11 columns, `NF=13`, no `|` in a
cell), `corpus/SOURCES.md:12` (header) and `:131-132` (S256/S257 style),
`.ufo/evidence/round-46/coverage/measure.py` (the counter's own row and entry predicates),
`.ufo/evidence/round-46/assimilation/{adoption-map.json,guard-map.json}`,
`.ufo/evidence/round-46/control/run-controls.py:33-39` (the fixture's exact document
triples), and the three snapshots under `.ufo/evidence/round-46/coverage/sources/`.

## Rows (delivered verbatim in `ScribeRows.rows.md`)

| S258 | Systemic Flakiness: An Empirical Analysis of Co-Occurring Flaky Test Failures (Parry, Kapfhammer, Hilton, McMinn; arXiv 2504.16777) — https://arxiv.org/abs/2504.16777 | paper | A | F3's determinism precondition — flaky failures co-occur in clusters that share root causes, so a set of flaky or surviving cases is not a set of independent observations | §Abstract @ arXiv:2504.16777v1 (submitted 23 Apr 2025), snapshot .ufo/evidence/round-46/coverage/sources/arxiv-2504.16777-abs.html sha256 28d2954d | Flaky tests co-occur in clusters: 75% of the 810 flaky tests found in 10,000 test suite runs across 24 Java projects belong to a cluster of mean size 13.5, so one green rerun says nothing about the cluster's other members | mined | 2026-10-25 | 365d | corpus/knowledge/r6-flaky-failures-cluster.md |
| S259 | An Empirical Study of Detected and Undetected Flaky Test Failures in Real-World CI Pipelines (Leinen, Gruber, Erdogan, Stahlbauer, Pretschner; IEEE TSE 2026) — https://portal.fis.tum.de/en/publications/an-empirical-study-of-detected-and-undetected-flaky-test-failures/ | paper | A | F3's flaky-aware verdict — a rerun inside the same job is both the detection mechanism and its blind spot; DOI 10.1109/TSE.2026.3729363 | §Abstract on the TUM portal record @ IEEE Transactions on Software Engineering, accepted/in press 2026, snapshot .ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html sha256 5eb59adf | Rerunning a failed test inside the same job both detects flakiness and hides it: undetected flaky failures are 9.8%-16.3% of failed pipeline runs across 8.8 billion test executions in four industry-scale projects, spiking on code changes and test reordering | mined | 2026-10-25 | 365d | corpus/knowledge/r5-undetected-flaky-failures.md |
| S260 | Flaky Tests at Google and How We Mitigate Them (Micco; Google Testing Blog, published 2016-05-27; the publisher's per-post JSON record of the post) — https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json | docs | A | F3's flaky-aware precondition and the false-red rate a verdict is priced against — most observed pass-to-fail transitions involve a flaky test | entry.content body of the per-post record, post id tag:blogger.com,1999:blog-15045980.post-6277555988217606236, published 2016-05-27T17:31:00-07:00, snapshot .ufo/evidence/round-46/coverage/sources/google-flaky-feed-6277555988217606236.json sha256 434d8658 | Google reports that about 84% of the pass-to-fail transitions it observes involve a flaky test, so legitimate failures get dismissed as false positives and a red build is more likely a flake than a defect | mined | 2026-10-25 | 365d | corpus/knowledge/r9-false-red-rate.md |

## Gate block lines (one per row: ≤25-word located quote, URL, access date)

- **S258** — quote “finding that 75% of flaky tests across all projects belong to a
  cluster, with a mean cluster size of 13.5 flaky tests” (22 whitespace tokens; §Abstract,
  first occurrence at character offset 1752 of the extracted text and byte offset 3642 of
  the raw snapshot; `grep -cF` on the snapshot → 3 lines) — URL
  https://arxiv.org/abs/2504.16777 — accessed 2026-10-25.
- **S259** — quote “undetected flaky failures account for 9.8 %-16.3 % of failed pipeline
  runs” (12 tokens; §Abstract on the portal record, character offset 1691 of the extracted
  text; the raw HTML holds the range with an en dash, `9.8 %–16.3 %`, which the extractor
  folds to `-`, so a literal ASCII grep on the raw file does not match while the folded
  comparison does) — URL
  https://portal.fis.tum.de/en/publications/an-empirical-study-of-detected-and-undetected-flaky-test-failures/
  — accessed 2026-10-25.
- **S260** — quote “about 84% of the transitions we observe from pass to fail involve a
  flaky test” (15 tokens; the `entry.content` body of the per-post record, byte offset 2904
  of the snapshot; `grep -cF` → 1) — URL
  https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json —
  accessed 2026-10-25.
  Snapshot structure, verified locally: 8353 bytes, **0 newlines** (single-line JSON),
  body in `entry.content.$t` with `entry.content.type = html`, and
  `entry.link[rel=alternate].href` = `https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html`,
  i.e. the rendered page the lane holds as S026.

### Alternate located quotes, with the freshness flag the entry seat needs

The C3 counter requires each entry to carry at least one located quote that is **absent
from the package copy** of the same basename. Measured with the counter's own
`norm_text`/`fold` (imported from `.ufo/evidence/round-46/coverage/measure.py`), against
`.ufo/evidence/round-46/assimilation/package/`:

| row | quote (tokens) | located | fresh vs package copy |
|---|---|---|---|
| S258 | “We discovered that flaky tests often exist in clusters, with co-occurring failures that share the same root causes, which we call systemic flakiness” (23) | yes, offset 870 | **yes** |
| S258 | “We used an established dataset of 10,000 test suite runs from 24 Java projects on GitHub” (16) | yes, offset 1333 | **yes** |
| S258 | “finding that 75% of flaky tests … mean cluster size of 13.5 flaky tests” (22) | yes, offset 1752 | no (`r6-flaky-failures-cluster.md` already quotes it) |
| S259 | “Modern CI systems commonly rerun failed tests within the same job to identify flaky failures” (15) | yes, offset 1116 | **yes** |
| S259 | “We analyzed 8.8 billion test executions from four industry-scale projects over two-month periods” (13) | yes, offset 1365 | no |
| S259 | “These flaky failure rates spike temporarily, triggered primarily by code changes and test reordering” (14) | yes, offset 1767 | no |
| S259 | “the most disruptive test cases with undetected flaky failures remain largely invisible to tools relying on current detection mechanisms” (19) | yes, offset 1932 | **yes** |
| S260 | “Almost 16% of our tests have some level of flakiness associated with them” (13) | yes, offset 2380 | **yes** |
| S260 | “we see a continual rate of about 1.5% of all test runs reporting a” (14) | yes, offset 1658 | **yes** |
| S260 | “about 84% of the transitions we observe from pass to fail involve a flaky test” (15) | yes, offset 2904 | no |
| S260 | “It is quite common to ignore legitimate failures in flaky tests due to the high number of false-positives” (18) | yes, offset 3096 | no |

## Verification (commands and outputs)

Row shape and the counter's own row predicate — the three delivered lines were fed to
`flaky_rows()` from `.ufo/evidence/round-46/coverage/measure.py` through an in-process
stub `Tree` (snapshot bytes read from the lane, registry text from the draft; **no**
`--lane/--rev` run, so this is a syntax/semantics check of the draft, not a verdict):

```
row lines found: 3
  cells=13 id=S258 status=mined pipefree=True
  cells=13 id=S259 status=mined pipefree=True
  cells=13 id=S260 status=mined pipefree=True
S258 doc= arxiv.org/abs/2504.16777 used= {'corpus/knowledge/r6-flaky-failures-cluster.md'}
S259 doc= portal.fis.tum.de/en/publications/an-empirical-study-of-detected-and-undetected-flaky-test-failures used= {'corpus/knowledge/r5-undetected-flaky-failures.md'}
S260 doc= testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json used= {'corpus/knowledge/r9-false-red-rate.md'}
ROWS_ACCEPTED=3
```

The frozen census from `CORPUS.md`, run on the draft file
(`D=.ufo/waves/round-46/w1/ScribeRows.rows.md`):

```
rows: 3
malformed: 0
dup ids: 
enum/tier: (end)
used-by missing: missing: corpus/knowledge/r6-flaky-failures-cluster.md
missing: corpus/knowledge/r5-undetected-flaky-failures.md
missing: corpus/knowledge/r9-false-red-rate.md
```

The `used-by missing:` prefix is my own `echo -n` label; the three `missing:` lines are
the census's output, one per `mined` row whose `used-by` path is absent.

Snapshot identity — `sha256sum .ufo/evidence/round-46/coverage/sources/*`:

```
28d2954d22ea45af7bd0454f1a8b01bb5db40e8e5cc235eed176a1621aa26a14  arxiv-2504.16777-abs.html   (43376 bytes)
434d86586ecf3ea03f57d4342c6e8575576eef6a9fd452a5c0a9e67bd8889929  google-flaky-feed-6277555988217606236.json   (8353 bytes)
5eb59adf099304a07059530b0857f7b517eaa72c832049f46952915a77e71a6f  tum-portal-flaky-failures.html   (51850 bytes)
```

The three 8-hex prefixes in the anchors (`28d2954d`, `5eb59adf`, `434d8658`) are the
first eight hex digits of those digests; the counter re-hashes the snapshot at REV and
matches any 8+-hex token in the anchor cell, so each anchor pins exactly one snapshot.

Id availability — `grep -cE '^\| S(258|259|260) ' corpus/SOURCES.md` → `0`;
`grep -cE '^\| S(258|259|260) ' /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md`
→ `0`. The guard's `safe_floor`/`next_free` is S258
(`.ufo/evidence/round-46/assimilation/guard-map.json`, verdict `admitted`), the lane's
registry max is S257, and the staged package max is S255 — no id is reused.

Document keys — the counter's `doc_key()` on the first URL of each source cell prints
exactly the three frozen document strings from `measure.py` `DOCS`
(`arxiv.org/abs/2504.16777`;
`portal.fis.tum.de/en/publications/an-empirical-study-of-detected-and-undetected-flaky-test-failures`;
`testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json`), as the
`doc=` lines above show. The S259 URL carries a trailing slash, which `doc_key` strips;
the same trailing-slash form is what `control/run-controls.py:35` and the counter's own
selftest use.

Snapshot text, extracted with the item's prescribed command
(`python3 .ufo/evidence/round-45/freshness/measure.py --extract <snapshot>`): arXiv
extract 5169 bytes, TUM extract 12011 bytes, feed extract 8353 bytes (the feed extract
is the raw JSON — the text lives in `entry.content.$t`, which I decoded with `json` +
tag-strip to read the prose).

## Dedupe notes

- **S216 = S225 = S229 = S235** are the same document in the read-only package: all four
  staged rows carry the per-post record
  `https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json`
  (`grep -c "6277555988217606236" /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md`
  → `4`). They collapse to the one adopted row S260; S225/S229/S235 are not adopted.
  `adoption-map.json` records the same thing (`S216 → S260`, note “S225/S229/S235 are the
  same feed document and dedupe to S260”).
- **S212** is the rendered post page’s text carried by the **blog-level** feed
  (`/feeds/posts/default?alt=json&max-results=200`, a different document key from the
  per-post record); the lane already holds the rendered page as **S026**
  (`corpus/SOURCES.md:37`, URL
  `https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html`). S212 is
  therefore neither a duplicate of S260 nor adoptable — it is the same underlying post
  under a third carrier, and the lane’s S026 already covers the page.
- `grep -n "2504.16777\|portal.fis.tum.de\|googleblog" corpus/SOURCES.md` returns only
  line 37 (S026): the lane holds no row for the arXiv paper or the portal record, so S258
  and S259 are new documents and S260 is new by carrier.

## Known gap at draft time (not a defect of the rows)

The three `used-by` paths do not exist in the lane yet — `corpus/knowledge/` holds no
`r6-flaky-failures-cluster.md`, `r5-undetected-flaky-failures.md` or
`r9-false-red-rate.md` (only the package copies under
`.ufo/evidence/round-46/assimilation/package/`). Consequences, stated plainly:

- the frozen census “mined rows whose used-by paths do not exist” prints the three
  `missing:` lines above until the entry seat lands the entries;
- the C3 counter refuses a row-free entry and an entry-free row: `covered == rows`
  requires each of S258/S259/S260 to be cited on line 1 of an admitted entry, and
  `entries` requires `verified-at: >= 2026-10-25` plus a quote fresh against the package
  copy (the table above lists the fresh quotes available per row);
- `corpus/README.md` must gain the three index rows (`| \`knowledge/<name>.md\` | … | S25x |`)
  or `indexed == entries` fails.

I wrote no entry, no README line and no `corpus/SOURCES.md` line: the rows are delivered
as a draft beside this report, per the item.

Status of the entry side at the time of this report (read-only check, not my deliverable):
the S260 entry exists as a draft at `.ufo/waves/round-46/w1/ScribeEntryFalseRed.entry.md`
(7584 bytes; line 1 `source: S260 — …` naming the same snapshot and `sha256 434d8658…`,
line 2 `verified-at: 2026-10-25`, line 3 `recheck: 365d — …`), and it is **not** yet at
`corpus/knowledge/r9-false-red-rate.md` (`[ -e corpus/knowledge/r9-false-red-rate.md ]` →
ABSENT). The peer reports `self_pin=1 rows=1 entries=1 indexed=1 covered=1` on a scratch
harness with a synthesized S260 row; I did not re-run that harness. Remaining C3
dependencies, in order: land the three entries at the `used-by` paths, then add the three
`corpus/README.md` index lines, then the L1's deciding run.

## Not run (unrun checks, reported as unrun)

- `python3 .ufo/evidence/round-46/coverage/measure.py --lane … --rev …` — not run by me at
  any revision; the deciding run is the L1's (measurement bounds).
- `--selftest` for any of the three counters — not run by me (not my item).
- No fetch of any URL: every quote and number here comes from the committed snapshots.
- No tool was installed or upgraded, so there is no tool/version/channel line to record.
