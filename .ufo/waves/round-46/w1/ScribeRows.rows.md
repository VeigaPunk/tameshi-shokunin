seat: ScribeRows
item: drafted the three C3 registry rows S258/S259/S260 (arXiv 2504.16777, TUM portal record of the IEEE TSE 2026 paper, Google Testing Blog per-post feed) in the 11-column `corpus/SOURCES.md` schema, each grounded on its round-46 snapshot and each naming the knowledge entry it feeds

# Round-46 C3 rows — draft (append verbatim, in this order, after S257)

Contract: `/home/vgpnk/Projects/shokunin/CORPUS.md` §SOURCES.md (11 columns, `NF=13`,
no `|` in any cell, append-only). Style copies the lane's last rows `corpus/SOURCES.md:131`
(S256) and `:132` (S257). Ids are the guard-admitted whole-collision map
(`.ufo/evidence/round-46/assimilation/adoption-map.json`: staged S195 → S258,
S190 → S259, S216 → S260; `.ufo/evidence/round-46/assimilation/guard-map.json` verdict
`admitted`, `safe_floor` S258).

## Rows

| S258 | Systemic Flakiness: An Empirical Analysis of Co-Occurring Flaky Test Failures (Parry, Kapfhammer, Hilton, McMinn; arXiv 2504.16777) — https://arxiv.org/abs/2504.16777 | paper | A | F3's determinism precondition — flaky failures co-occur in clusters that share root causes, so a set of flaky or surviving cases is not a set of independent observations | §Abstract @ arXiv:2504.16777v1 (submitted 23 Apr 2025), snapshot .ufo/evidence/round-46/coverage/sources/arxiv-2504.16777-abs.html sha256 28d2954d | Flaky tests co-occur in clusters: 75% of the 810 flaky tests found in 10,000 test suite runs across 24 Java projects belong to a cluster of mean size 13.5, so one green rerun says nothing about the cluster's other members | mined | 2026-10-25 | 365d | corpus/knowledge/r6-flaky-failures-cluster.md |
| S259 | An Empirical Study of Detected and Undetected Flaky Test Failures in Real-World CI Pipelines (Leinen, Gruber, Erdogan, Stahlbauer, Pretschner; IEEE TSE 2026) — https://portal.fis.tum.de/en/publications/an-empirical-study-of-detected-and-undetected-flaky-test-failures/ | paper | A | F3's flaky-aware verdict — a rerun inside the same job is both the detection mechanism and its blind spot; DOI 10.1109/TSE.2026.3729363 | §Abstract on the TUM portal record @ IEEE Transactions on Software Engineering, accepted/in press 2026, snapshot .ufo/evidence/round-46/coverage/sources/tum-portal-flaky-failures.html sha256 5eb59adf | Rerunning a failed test inside the same job both detects flakiness and hides it: undetected flaky failures are 9.8%-16.3% of failed pipeline runs across 8.8 billion test executions in four industry-scale projects, spiking on code changes and test reordering | mined | 2026-10-25 | 365d | corpus/knowledge/r5-undetected-flaky-failures.md |
| S260 | Flaky Tests at Google and How We Mitigate Them (Micco; Google Testing Blog, published 2016-05-27; the publisher's per-post JSON record of the post) — https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json | docs | A | F3's flaky-aware precondition and the false-red rate a verdict is priced against — most observed pass-to-fail transitions involve a flaky test | entry.content body of the per-post record, post id tag:blogger.com,1999:blog-15045980.post-6277555988217606236, published 2016-05-27T17:31:00-07:00, snapshot .ufo/evidence/round-46/coverage/sources/google-flaky-feed-6277555988217606236.json sha256 434d8658 | Google reports that about 84% of the pass-to-fail transitions it observes involve a flaky test, so legitimate failures get dismissed as false positives and a red build is more likely a flake than a defect | mined | 2026-10-25 | 365d | corpus/knowledge/r9-false-red-rate.md |

## Column-by-column intent

- `source` — title, authors, venue, then the exact URL. S259's URL is the portal record
  (`og:url` in the snapshot), not the DOI; the DOI sits in `scope`.
- `kind` — `paper` (S258, S259), `docs` (S260, a vendor blog post, not a paper).
- `tier` — `A`: original paper (S258, S259) and the publisher's own statement (S260).
- `scope` — names the F3 claim each row grounds, and nothing wider.
- `anchor` — section (`§Abstract`, or the record's `entry.content` body), the publication
  date/revision, the round-46 snapshot path and its 8-hex sha256 prefix.
- `teaches` — one sentence, every number from the snapshot abstract.
- `status` `mined`, `opened` 2026-10-25, `recheck` 365d, `used-by` the single entry path.

## Dedupe notes

- The package's staged S216, S225, S229 and S235 all carry the same document — the
  per-post record `https://testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json`
  (`grep -c "6277555988217606236" SOURCES.append.md` → 4). They dedupe to one adopted row,
  S260; the other three ids are not adopted.
- Staged S212 is the rendered post page's text carried by the *blog-level* feed
  (`/feeds/posts/default?alt=json&max-results=200`), a different document key from the
  per-post record; the lane already holds the rendered page as S026
  (`corpus/SOURCES.md:37`). S212 is therefore neither a duplicate of S260 nor adoptable.
- The lane holds no row for arxiv.org/abs/2504.16777 or for the portal.fis.tum.de record
  (`grep -n "2504.16777\|portal.fis.tum.de\|googleblog" corpus/SOURCES.md` returns only
  S026), so S258/S259 are new documents and S260 is new by carrier.
