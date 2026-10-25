# ScoutC3Package — staged package document census (round 43, w1)

Item: classify the 103 staged rows in `merge/tameshi/SOURCES.append.md` by document address,
count within-set duplicate documents, and count what the lane registry already holds.
Read-only; scratch under `/tmp` (deleted). No installs needed (python3 stdlib only).

## Basis (bytes, not the live path)

| file | rows | id span | bytes | sha256 | mtime |
|---|---|---|---|---|---|
| `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md` | 103 (lines 7–109) | S153…S255, contiguous | 154031 | `020fbeaa048fc6727e08c0e91e242cd8b1b15ea9dc8853837c4548b1cf394807` | 2026-10-24T23:33:20-0300 |
| `corpus/SOURCES.md` at base `487b8f0`, freeze `17f6ef0` and HEAD | 113 | S001…S158 | — | `afb6e5cb014be1a1a4a3621f10d34fe7afa6f9df241517ddf869896c709c38da` | committed |
| `corpus/SOURCES.md` working tree | 114 | S001…S159 | 98079 | `c50ca1fbce6b1afb769735793d2ca520d05e5e8a830fd3ea88a7c48fb4c961fd` | 2026-10-25T07:58:48-0300 |

The three measurement revisions carry the **same** registry bytes (`afb6e5cb…`, 113 rows); the
working tree is +1 row — another seat's round-43 append of `S159` (Wikipedia, Mutation testing) plus
trailing-text edits on S089/S155/S158 and a round-43 note — uncommitted. The registry was also being
written during the first read (~10:53Z returned 115 rows, collisions through `S160`); the snapshot
used for the counts below is the working-tree state `c50ca1fb…`, re-read stable at 10:58:04Z and
10:59:19Z. Re-run `python3 -I tools/staged-id-guard.py --registry <COMMITTED BYTES>` to see the
REV-state numbers quoted in §4.

## 1. Classification of the 103 staged rows

Method: source cell (column 2), plus the anchor cell (column 6) only to disambiguate; a document
address = an `http(s)` URL or a DOI. A bare `<repo root>` URL counts as the document **only** when
the row names no repo-internal path.

| class | count | ids |
|---|---|---|
| carries a document URL/DOI | **59** | 87 rows carry ≥1 http URL, of which these 59 are document addresses; 8 rows also carry a DOI token: S157 S161 S171 S182 S190 S207 S237 S248 |
| only a repo path | **44** | 16 with no URL at all: S172 S173 S174 S178 S179 S180 S184 S185 S186 S187 S188 S189 S191 S193 S194 S201 · 28 with a bare repo-root URL + a path: S208 S213 S214 S215 S217 S218 S219 S220 S221 S222 S223 S226 S227 S228 S230 S231 S232 S233 S234 S236 S238 S239 S245 S246 S247 S249 S250 S251 |
| neither → `unmapped` | **0** | — |

Boundary row: **S176** (line 30) — its only address is a third-party repo root
`https://github.com/VictorGazzinelli/snapshot-testing` and it names no path; counted as URL. If a
bare repo root is instead read as "repo path", the split is 58 / 45 / 0. Nothing changes for
`unmapped`: still 0.

Cross-check with the C3 tool's own notion: `staged-id-guard.py:document_key` searches cells 2–6,
so the anchor's `repository https://github.com/VeigaPunk/tameshi-shokunin` satisfies it for every
own-work row. Result: **0 empty keys, 103 URL keys, 58 distinct keys** — 43 rows share
`https://github.com/VeigaPunk/tameshi-shokunin` (45 rows key to some bare repo root, incl. S176 and
S226). `unmapped` therefore cannot fire for this package, and a by-document map built on that key
collapses 43 distinct documents onto one target.

## 2. Documents duplicated WITHIN the staged set

**By exact normalized address/DOI — 7 duplicated documents, 22 rows, 15 redundant rows:**

| document | rows (file line) |
|---|---|
| `tools/repeat-control.py` | S172 (26), S180 (34), S186 (40) |
| `tools/env-diff.py` | S173 (27), S184 (38), S188 (42) |
| `tools/mutate-and-run.sh` | S179 (33), S185 (39), S187 (41), S189 (43), S191 (45) |
| `lanes/tameshi/round13/evidence/f5-port-measurement.txt` | S233 (87), S234 (88) |
| `https://www.t.kyoto-u.ac.jp/lib/ja/support/ieice` | S177 (31), S192 (46) |
| `https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json` | S216 (70), S225 (79), S229 (83), S235 (89) |
| DOI `10.1109/TSE.2026.3685588` (arXiv 2602.09311) | S171 (25), S237 (91), S248 (102) |

**Including same-document/different-address variants — 8 documents, 25 rows, 17 redundant:**

* + **S212** (66) is the same blog post as the per-post feed record — it names the rendered page
  `…/2016/05/flaky-tests-at-google-and-how-we.html`; the table above carries that post through
  three address forms (page, index feed, per-post feed). Group becomes S212 S216 S225 S229 S235.
* + **S209** (63) / **S210** (64) are the English `docs/golden_tests.md` pin and its official
  zh-cn rendition of the same page; no shared URL string, same document, different rendition.

Not duplicates: S202 / S204 (different googletest files at one commit); S196 / S198 (thesis vs JSS
paper); S240 is a *different document about* the TSE paper in the DOI group (a faculty record) —
a publication-level repeat, not a document repeat.

## 3. Documents the lane registry already holds

**11 distinct lane-held documents covering 19 of the 103 staged rows** (lane = `corpus/SOURCES.md`,
line cited in the last column; every lane id listed is ≤ S158, so the mapping holds identically in
the committed registry at base/freeze and in the working tree):

| staged rows | lane id (line) | how the key matches |
|---|---|---|
| S153 | S105 (117) | same URL `pubs.opengroup.org/…/diff.html` |
| S154 | S106 (118) | same URL `raw.githubusercontent.com/google/golden/master/golden.go` |
| S159 | S155 (125) | same URL `pitest.org/quickstart/basic_concepts/` |
| S160 | S156 (126) | same URL `pitest.org/faq/` |
| S196 | S152 (122) | same URL `repositorio.ufmg.br/bitstreams/271f8a97…/download` |
| S209 | S107 (119) | same URL `raw.githubusercontent.com/tensorflow/federated/4d3a89c9…/docs/golden_tests.md` |
| S210 | S108 (120) | same URL `www.tensorflow.org/federated/golden_tests?hl=zh-cn` |
| S211 | S002 (13) | same URL `raw.githubusercontent.com/stryker-mutator/…/mutation-testing-report-schema.json` |
| S179 S185 S187 S189 S191 | S031 (42) | same own-work document `tools/mutate-and-run.sh` |
| S212 S216 S225 S229 S235 | S026 (37) | same post, carrier variants (page vs feed record) |
| S176 | S132 (121) | same README, address-form variant (repo root vs `raw…/master/README.md`) |

Cited as an *input*, not the row's own document (not counted above): S180→S031, S194→S031,
S185/S189→S032 S037 S053 S088 (kumitate gate blobs), S213→S033 (`corpus/surface-census.sh`),
S224→S032 (`scripts/kimi-census.mjs`).

## 4. Id collisions and the guard — two different answers from two byte sources

```
# A. registry at base 487b8f0 / freeze 17f6ef0 / HEAD  (113 rows, sha afb6e5cb…)
$ git show 17f6ef0c72ec27e1aea305b5c95806b43bb2caef:corpus/SOURCES.md > /tmp/lane.md
$ python3 -I tools/staged-id-guard.py --registry /tmp/lane.md --staged <staged> --json  # exit 1
registry_rows=113  registry_max=S158  collision_count=6
collisions = S153 S154 S155 S156 S157 S158
held       = {S153→S105, S154→S106}          next_free=S159  cascade_count=6  verdict="refused"

# B. registry working tree  (114 rows, sha c50ca1fb…, uncommitted S159)
$ python3 -I tools/staged-id-guard.py --registry corpus/SOURCES.md --staged <staged> --json  # exit 1
registry_rows=114  registry_docs=100  registry_max=S159  staged_rows=103  staged_max=S255
verdict="refused"  refused=true  unmapped=[]  next_free=S160  safe_floor=S256
collisions = S153 S154 S155 S156 S157 S158 S159                    (7; column0 also 7, miss [])
held       = {S153→S105, S154→S106, S159→S155}                     (3)
cascade    = S160…S166  cascade_count=7   naive_map={S153→S160 … S159→S166}
```

* **6 vs 7 collisions is a byte-source question, not a finding about the package.** The staged
  file's own hazard note (`SOURCES.append.md:109`, "six lane rows — S153…S158") is correct for the
  committed registry at both measurement revisions and stale only against the uncommitted working
  tree, where S159 was appended this round.
* Of the 6 committed-state collisions, 2 are held documents (S153, S154) and **4 are numeric-only**,
  needing renumbering by document: S155 (arXiv 2302.09330) vs lane S155 (PIT basic concepts); S156
  (arXiv 2406.09843) vs lane S156 (PIT FAQ); S157 (JOSS 01891) vs lane S157 (argparse); S158 (UIUC
  flaky PDF) vs lane S158 (DetectionStatus.java). In the working tree the same 4 plus S159 (PIT
  basic concepts) collide, and S159's document *is* held (lane S155), so it is held rather than
  numeric-only.
* `held` is computed only over colliding ids, so **in both byte states** the guard misses staged rows
  whose document the lane already holds: at REV, S159 (PIT basic concepts, id free), S160 (PIT FAQ),
  S196, S209, S210, S211, S179/S185/S187/S189/S191 (S031), the five blog rows (S026) and S176
  (S132) — 17 rows; 16 of those are still missed in the working tree after S159 starts colliding.
  They would be appended as duplicates.

## Confidence

Observed (command output, snapshot-pinned): row counts, class counts, ids, duplicate groups,
lane-held mapping, guard JSON. [INFERENCE]: that S212 and S209/S210 are "the same document" as
their carrier/rendition counterparts — evidenced by the rows' own text (same title/date/post id;
S210's source names the upstream pin), not by byte-identical fetch.

## Remaining unknowns

1. Whether the L1 treats carrier/address/rendition variants as one document when renumbering — both
   the strict (7 docs / 15 redundant rows) and loose (8 / 17) counts are given.
2. Which byte source the C3 counter will read for the registry (committed REV bytes → 6 collisions,
   2 held; working tree → 7 collisions, 3 held). The working-tree diff is another seat's round-43
   append (S159 + note), not a change to any of the 11 held documents. Any counter that reads
   `corpus/SOURCES.md` should pin a sha first (as done here); an unpinned read can also land
   mid-write (one read here saw 115 rows).
3. `document_key` puts 45 rows on a bare repo root (43 on `…/VeigaPunk/tameshi-shokunin`), so the
   tool's by-document map cannot separate those 43 documents. Whether that matters depends on
   whether adoption ever reads a map instead of the per-row `held` list; not exercised here.

## Tooling

None installed or upgraded. `python3` (system), stdlib only; scratch under
`/tmp/tameshi-r43-ScoutC3Package/` and `/tmp/tameshi-r43-ScoutC3Package2/`, both removed. Lane and
staging trees untouched (`git status` shows only other seats' pre-existing modifications).
