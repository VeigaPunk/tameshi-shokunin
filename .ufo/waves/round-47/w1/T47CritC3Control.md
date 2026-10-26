# T47CritC3Control — C3 (coverage) cheapest-pass attack

Seat: T47CritC3Control, critic (leaf, no dispatch). Assigned item: attack
`.ufo/evidence/round-47/coverage/measure.py` for a cheap pass — items (a)–(f) — on scratch clones at
freeze `9acfbe21435e1976636a276448dee1d5e7155915`, and name for each the check that would close it.

**Verdict: all six assigned attacks pass the frozen counter.** Nine independent variants produce a full
`C3_R47_PASS=true` (three more beyond the six, one of them a hole not in my item). The counter's own
`--selftest` is green (24/24, `VERDICT: PASS`) and all seven no-harm monitors are `ok` on the cheapest
variant, so nothing in the freeze detects any of this. The counter refuses exactly two things: a quote
that is absent from the snapshot, and non-fresh text *at the three declared basenames*.

Nothing was edited in the lane except this file. Scratch: `/tmp/tameshi-r47-T47CritC3Control/`
(clone `clone.a2Dr`, driver `gen.py`/`drive{,2,3,4,5}.py`, one branch per variant). No package
install or update was made (no pacman transaction, no uv/npx/binary install); no model was passed.
No writes to `/home/vgpnk/Projects/shokuknow`, the fleet repo, or the lane's Git/jj state.

## Method

```
D=/tmp/tameshi-r47-T47CritC3Control/clone.a2Dr
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin "$D"
git -C "$D" rev-parse --show-toplevel   # == $D
git -C "$D" checkout -q 9acfbe21435e1976636a276448dee1d5e7155915
# per variant, throwaway identity inside $D only:
git -C "$D" checkout -q -B <vN> 9acfbe...
python3 "$D/.ufo/evidence/round-47/coverage/measure.py" --lane "$D" --rev <vN>
```

Each variant starts from the freeze tree, appends the three rows (`| S261 |`, `| S263 |`, `| S264 |`,
13 cells, status `mined`, anchor `.ufo/evidence/round-47/coverage/sources/<snap> <8-hex>`), writes the
entries, appends three backticked paths to `corpus/README.md`, and commits. Row snapshots/prefixes are
the real committed bytes, so `rows=3` in every run below.

Quotes used (token counts are what the counter measures, after its own fold):

| token | length | text |
|---|---|---|
| `NAV` | 15 | "Skip to main content Search Submit Donate Log in Search arXiv Press Enter to search" |
| `LABS` | 18 | "arXivLabs is a framework that allows collaborators to develop and share new arXiv features directly on our website" |
| `CHROME_SPAN` | 15 | "Search arXiv Press Enter to search · Advanced search --> Computer Science > Software Engineering" |
| `CHROME_LINK` | 9 | "About · Help · Contact · Subscribe · Copyright" |
| `VENUE` | 8 | "International Conference on Information Control Systems & Technologies" |
| titles | 12/14/11 | the three documents' own titles |

## Results

| # | variant (branch) | attack | rc | counter line |
|---|---|---|---|---|
| (a) | `vA2_nav_boilerplate` | quotes taken from page chrome | 0 | `rows=3 entries=3 indexed=3 covered=3 C3_R47_PASS=true` |
| (b) | `vB2_body_contradicts` | body states what the snapshot denies | 0 | `entries=3 … C3_R47_PASS=true` |
| (c) | `vC_same_sentence_x3` | three entries quote the same sentence | 0 | `entries=3 … C3_R47_PASS=true` |
| (d) | `vD_relabel_one_fresh` | relabel + exactly one fresh quote | 0 | `entries=3 … C3_R47_PASS=true` |
| (e) | `vE4_title_only_novel` | entries at basenames with no package copy | 0 | `entries=3 … C3_R47_PASS=true` |
| (f) | `vF_venue_field_only` | S2 quote in `venue`, a field the entry does not cite | 0 | `entries=3 … C3_R47_PASS=true` |
| + | `vI2_stripped_chrome_span` | quotes that exist only after tag-stripping | 0 | `entries=3 … C3_R47_PASS=true` |
| + | `vG_cheapest_combined` | (e)+(c)+(b) combined | 0 | `entries=3 … C3_R47_PASS=true` |
| + | `vJ2_row_snapshot_mismatch` | each row's snapshot belongs to another document | 0 | `entries=3 … C3_R47_PASS=true` |
| – | `vE5_title_only_declared` | (e)'s exact bytes at the declared basenames | 1 | `entries=1` — `REFUSED r8-flakiness-not-static.md` and `REFUSED r8-flaky-cost-baseline.md`, both `no quote fresh against the package copy` |
| – | `vZ_quote_absent` | quote absent from every snapshot | 1 | `entries=1` — `REFUSED … no located quote` |
| – | (frozen) `CTL_A..D` | package byte-exact / relabel / rows-only / wrong digest | 1 | `entries=0` / `entries=0` / `entries=0` / `rows=0` |

`vE5` vs `vE4` is the clean differential for (e): **identical entry bytes, the verdict flips on the
basename alone.** `bash .ufo/evidence/round-47/no-harm.sh "$D" vE4_title_only_novel` → all seven `ok`
(`commandD 9`, `coldread 6`, `r45-freshness 71`, `r45-coverage 2/2`, `S160 1`, `registry 123`,
`r46-coverage 3/3`).

## Per item: counterexample, evidence, closing check

Impacted axis for all six: **coverage only** (C3's own claim). None touches calibration or operability;
none changes a route or an id.

### (a) Chrome quoted as ground — PASSES

Counterexample: entry 1 cites `S261`, body `Claim: flakiness is a language-specific artifact of
instrumentation; the paper contributes a search box and a donate button.`, and its only located quote is
`NAV` — the `ds-skip-link` anchor of every arXiv page. Accepted (`located=True`, and the package copy
does not contain it, so `fresh=True`).

Sharper: `vI2`'s `CHROME_LINK` ("About · Help · Contact · Subscribe · Copyright") is the footer's five
separate `<a>` links, and `CHROME_SPAN` spans the search box, the `-->` of an HTML comment and the
breadcrumb. **Neither string exists in the raw snapshot** (`in_raw_html=False`; verified by substring
search on both `.html` files) — both are artifacts of `re.sub(r'(?s)<[^>]*>', ' ', text)` in `norm_text`
(lines 74-80). The counter's "located quote" can therefore be a string no reader of the page can point at.

Evidence: `vA2` and `vI2` both `C3_R47_PASS=true`. The genuine abstract sentences are contiguous in the
raw HTML (`in_raw_html=True`), so tightening does not cost the intended quotes.

Smallest safe correction: locate quotes in a content window, not in the stripped whole page. One
function, one call site (`flaky_rows` line 119):

```python
def content_text(data):
    t = data.decode('utf-8', 'replace')
    if re.search(r'<(html|body|div|p|head)\b', t, re.I):          # one occurrence each, verified
        parts  = re.findall(r'(?is)<blockquote[^>]*class="[^"]*\babstract\b[^"]*".*?</blockquote>', t)
        parts += re.findall(r'(?is)<h1[^>]*class="[^"]*\btitle\b[^"]*".*?</h1>', t)
        t = ' '.join(parts)
    else:
        try: t = ' '.join(str(json.loads(t).get(k, '')) for k in ('title', 'abstract'))
        except ValueError: pass
    t = re.sub(r'(?is)<(script|style)\b.*?</\1\s*>', ' ', t)
    return fold(html.unescape(re.sub(r'(?s)<[^>]*>', ' ', t)))
...
rows[cells[1]] = dict(text=content_text(data), used=used, doc=doc_key(url.group(0)))
```
and a selftest case `T25_chrome_quote_refused` (row snapshot = the real head of an arXiv page, entry
quoting `NAV` → `entries=0`).

### (b) Body contradicts the snapshot — PASSES

Counterexample: `vB2` entry 1 quotes the abstract's real first sentence, then asserts
"The authors report that flakiness affects 0% of test runs and that reruns are independent observations;
no prediction is proposed and the industrial deployment succeeded without instrumentation." The
snapshot says the opposite on every clause ("Non-deterministically behaving test cases cause developers
to lose trust … Detecting flaky tests is therefore a crucial task … we therefore investigate the
prediction of flaky tests"). The counter never reads the body beyond its double-quoted spans.

This is not mechanically closable by an entailment check, and I will not pretend otherwise; the
smallest correction converts it from silent to visible: every declarative body sentence must either
contain a located quote or be tagged `[INFERENCE]`.

```python
for sent in re.split(r'(?<=[.!?])\s+', body):
    if len(sent.split()) >= 6 and '[INFERENCE]' not in sent \
       and not any(q in fold(sent) for q in located_quotes):
        return False, 'unsupported claim sentence', []
```
plus `T26_contradicting_body_refused`. A false paraphrase of a real quote stays a reviewer obligation —
say so in the counter docstring rather than implying the counter reads the claim.

### (c) Three entries, one sentence — PASSES

Counterexample: `vC` — all three entries' only quote is `LABS`, the arXivLabs paragraph present in both
arXiv snapshots. The third entry's line 1 is `source: S261, S264 — two rows, one quote`, so the cost
claim about the S2 record rests on a sentence from a different web page; `vG` repeats this with novel
basenames.

Smallest safe correction: make the located quote an exclusive resource across admitted entries (one
accumulator in `measure`, three lines):

```python
claimed = set()
# entry_ok returns its located quotes; in measure():
if not (ent[lq] - claimed):
    refused = 'every located quote already claimed by another entry'
claimed |= ent[lq]
```
plus `T27_same_sentence_three_entries_refused`.

### (d) Relabel + one fresh quote — PASSES

Counterexample: `vD` — each entry is the package copy with only the header rewritten
(`source: … relabelled package entry` / `verified-at: 2026-10-25` / `recheck: 365d`) plus one appended
sentence quoting chrome (`NAV`, `LABS`, `VENUE`). Everything else is byte-identical to the package entry,
including its stale `verified-at: 2026-10-23` body prose. `fresh` is a boolean over *any* one quote
(lines 140-148), so a single 8-token `venue` string buys an entire entry.

Smallest safe correction: price the freshness, don't gate it on one quote.

```python
fresh_q = {q for q in located_q if package_text is None or q not in fold(package_text)}
if len(fresh_q) < 2 or len(' '.join(fresh_q).split()) < 25:
    return False, 'fresh ground too thin', []
```
plus `T28_relabel_one_fresh_quote_refused`.

### (e) Basenames the counter does not check — PASSES

The deciding script (`control/run-controls.py`) and the contract both name the three basenames; the
counter accepts *any* `corpus/knowledge/*.md`, and `measure` line 164 reads the package copy by
basename, so a novel basename yields `package_text is None` and line 144 then sets `fresh = True`
**unconditionally**. Fail-open.

Counterexample: `vE4` — `corpus/knowledge/r47-{a,b,c}.md`, each body nothing but the document's title in
quotes and a claim; `rows=3 entries=3 indexed=3 covered=3 C3_R47_PASS=true`, with **zero** text absent
from the package copy (the S263 and S264 titles are present in the package copies' own source line —
verified). Same bytes at `vE5` = `entries=1`.

Deletion is the same hole: `vH4` removes the three package copies in the commit and the declared-basename
title-only entries pass (`entries=3`, PASS); no-harm does not monitor the package directory, so the
freeze receipts stay green.

Smallest safe correction — two lines, fail-closed plus the pinned names:

```python
BASENAMES = ('flaky-aware-verdict-evidence.md', 'r8-flakiness-not-static.md',
             'r8-flaky-cost-baseline.md')
...
if os.path.basename(path) not in BASENAMES:      # measure(), line 161
    continue
if package_text is None:                          # entry_ok(), line 144
    return False, 'no package copy', []
```
plus `T29_novel_basename_refused`, `T30_package_copy_deleted_refused`.

### (f) S2 quote from an uncited field — PASSES

Counterexample: `vF` — the S264 entry's only quote is the `venue` value, while the entry's claim is about
the abstract's cost findings. `norm_text` does no field segmentation; a JSON snapshot is one flat string,
so `venue`, `externalIds`, `openAccessPdf.disclaimer` and `paperId` are all quotable ground.

The payload is worse than the form: the committed record's `venue` is
`"International Conference on Information Control Systems & Technologies"`, while the DOI's DBLP key in
the same record is `conf/icst/LeinenEPSSJ24` — the ICST series is Software Testing, not Information
Control Systems [INFERENCE from the DBLP key; the record's own `venue` field is mislabelled]. So the
counter admits a quote that is both off-field and false.

Smallest safe correction: the same `content_text` as (a) — for JSON, only `title` and `abstract` values —
plus a refusal of any quote found only in `venue`/`externalIds`/`openAccessPdf`. `T31_venue_quote_refused`.

## Extra hole found while testing (not in my item, cheapest pass of all)

`vJ2`: a row's source URL and its snapshot anchor are independent — `flaky_rows` checks only that the
URL is one of the three (`doc_key`) and that *some* snapshot exists with a matching digest. With
S261→`s2-icst24-cost-of-flaky.json`, S263→`arxiv-2302.09330-abs.html`, S264→`lam-2020-reruns.txt`, three
entries each grounded in the *wrong document* pass: `rows=3 entries=3 … C3_R47_PASS=true`.
Closure: a per-document expected-snapshot map and one comparison.

```python
DOC_SNAP = {doc_key('https://arxiv.org/abs/2302.09330'): 'arxiv-2302.09330-abs.html', ...}
if os.path.basename(snap.group(0)) != DOC_SNAP[doc_key(url.group(0))]:
    continue
```
plus `T32_row_snapshot_mismatch_refused`.

## Cost of the cheapest pass (what the lane must not be able to do)

Three rows (free-form cells, status `mined`, real digest), three entries whose entire body is one title
quote each at basenames with no package copy, three backticks in `corpus/README.md`: **no part of any of
the three documents is read, no package entry is re-grounded, and every claim in every body is
unconstrained.** `vE4` and `vH4` are that pass, and both are invisible to all seven no-harm monitors and
to the counter's 24-case selftest.

The strongest counterexample from local evidence is `vI2` + `vJ2`: quotes that exist only as
tag-stripped concatenations (`in_raw_html=False`) attached to rows whose snapshots belong to a different
paper. A canonical judge reading only the receipt line cannot distinguish that from the intended pass;
only the six checks above (content window, sentence support, exclusive quotes, fresh budget, pinned
basenames + fail-closed freshness, row↔snapshot binding) make the distinguishing fact appear in the
receipt.
