seat: CritC3Control
item: attacked the frozen round-46 C3 coverage counter for a cheapest pass — 22 cheat variants built in one scratch Git repo and scored with the frozen counter at their own commits

# CritC3Control — cheapest-pass attack on `.ufo/evidence/round-46/coverage/measure.py`

Scope: critic only. I did not edit the counter, the contract, the registry, any
entry or any snapshot. The deciding run is the L1's; every run below is a scratch
score, never a verdict.

Counter under attack, sha256 (lane and scratch identical):

```
$ sha256sum .ufo/evidence/round-46/coverage/measure.py
f8bfefdf6c08ce880c3f329018d946168dd022c50391d24551853326dbcfb5f5  .ufo/evidence/round-46/coverage/measure.py
```

Counter selftest, run from the scratch checkout (24 cases, all pass):

```
$ python3 .ufo/evidence/round-46/coverage/measure.py --selftest | tail -2
C3_R46_SELFTEST: cases=24 failed=0
VERDICT: PASS            # exit 0
```

None of the 22 variants below is killed by a selftest case. The relabel-plus-one-
fresh-quote shape is accepted by design: T22 (`measure.py:296`) expects
`C3_R46_PASS=true` for an entry that keeps the package's quoted claim and adds one
fresh quote, and Vd extends that to the whole package body.

## Method (reproducible)

One scratch repo, one commit per variant, the frozen counter run at that commit:

```
D=/tmp/tameshi-r46-CritC3Control/repo
git -C "$D" init -q -b m
# attack.py asserts: git -C "$D" rev-parse --show-toplevel == os.path.realpath(D)
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin archive 745a583181648cfc7f9c1b476cd1be7dc68f7433 | tar -x -C "$D"
# commit the freeze tree with a throwaway identity in $D only; tag it `freeze`
# per variant: write rows/entries/README (+ snapshot overrides), commit, then
python3 "$D/.ufo/evidence/round-46/coverage/measure.py" --lane "$D" --rev HEAD
```

Driver: `/tmp/tameshi-r46-CritC3Control/attack.py`; raw output:
`/tmp/tameshi-r46-CritC3Control/out7.txt`. Scratch freeze commit `cecac85eb95b`,
23 commits total (freeze + 22 variants). No git command touched the lane.

Do-nothing control reproduced at the freeze commit of the same scratch repo:

```
$ python3 .ufo/evidence/round-46/coverage/measure.py --lane "$D" --rev freeze
C3_R46: self_pin=1 rows=0 entries=0 indexed=0 covered=0 row_ids=- rev=freeze C3_R46_PASS=false
```

## Results

All lines are the counter's own summary at the variant commit (`HEAD`).
Accepted = `C3_R46_PASS=true` and rc=0.

| # | cheat (item letter) | counter line | accepted? |
|---|---|---|---|
| V0 | legit baseline: 3 rows, 3 entries at the package basenames, claim + fresh quote, README index | `rows=3 entries=3 indexed=3 covered=3 … PASS=true` | yes (control) |
| Va | (a) entries quote only arXiv/TUM **navigation** text (`Skip to main content Search Submit Donate …`, `Skip to main navigation …`); claims unrelated; the S260 entry cites `S258, S260` and quotes arXiv nav | `rows=3 entries=3 indexed=3 covered=3 … PASS=true` | **yes** |
| Vb | (b) line 1 cites `S258, S259, S260`; body asserts figures the snapshots contradict (92 % detected, 0.3 % escape, no environment effect; 1,200 of 1.1 bn; 2 % false-red) with one genuine located quote each | `rows=3 entries=3 indexed=3 covered=3 … PASS=true` | **yes** |
| Vc | (c) three entries quote the **identical** arXiv sentence, each citing all three rows | `rows=3 entries=3 indexed=3 covered=3 … PASS=true` | **yes** |
| Vd | (d) package body relabelled (trio rewritten) + one fresh sentence bolted on | `… PASS=true` | **yes** (by design, T22) |
| Vd2a | package body relabelled, only the package's own (verbatim-locatable) quote — the CTL_B shape at the package basename | `rows=3 entries=0 … PASS=false` | no (`no quote fresh against the package copy`) |
| Vd3 | **same bytes as Vd2a**, written to `corpus/knowledge/r46-flaky-s25x.md` instead | `rows=3 entries=3 indexed=3 covered=3 … PASS=true` | **yes — bypass** |
| Vd4 | (d) package body + fresh quote parked in a "Quotes considered and rejected" list | `… PASS=true` | **yes** |
| Vd5 | package body + package's own quote, with the three `assimilation/package/*.md` copies deleted at REV | `… PASS=true` | **yes — bypass** |
| Ve1 | (e) source URL with a trailing slash (`…/2504.16777/`) | `… PASS=true` | **yes** |
| Ve2a | (e) uppercase host, no `www.` (`https://ARXIV.ORG/…`, `https://Portal.FIS.TUM.de/…`) | `… PASS=true` | **yes** |
| Ve2b | uppercase `WWW.` (`https://WWW.ArXiv.org/…`) | `rows=2 … row_ids=S259,S260 PASS=false` | no |
| Ve3 | (e) fragment appended to the URL (`…#abstract`, `…#publications`, `…#feed`) | `rows=0 … PASS=false` | no (silent: no per-row diagnostic) |
| Ve4 | (e) query appended (`…?context=cs`, `…?lang=en`, `…&x=1`) | `rows=0 … PASS=false` | no (silent) |
| Ve8 | (e) fragment/query hidden behind a cell separator (`…#` → `;#abstract`, `;?lang=en`) plus a second contradictory URL in the S260 cell | `rows=3 entries=3 … PASS=true` | **yes** |
| Ve5 | (e) cross-document anchor: source cell keeps the frozen URL, anchor pins **another** document's snapshot and digest (S258→TUM, S259→feed, S260→arXiv) | `… PASS=true` | **yes — false provenance** |
| Ve6 | all three rows anchored to the single arXiv snapshot; all three entries quote arXiv nav | `… PASS=true` | **yes — false provenance** |
| Ve7 | the three snapshots overwritten with hand-authored one-sentence files, anchor digests updated to the new bytes | `… PASS=true` | **yes — false provenance** |
| Vf | (f) README lists the three paths in backticks **inside a fenced block** that says "Do not treat this as the index" | `indexed=3 … PASS=true` | **yes** |
| Vh | rows at ids `S900/S901/S902` (guard-admitted ids never checked) | `rows=3 … row_ids=S900,S901,S902 PASS=true` | **yes** |
| Vi | `verified-at: 2099-01-01` | `… PASS=true` | **yes** |
| Vg | `verified-at: 2026-10-25-not-really-checked` | `… PASS=true` | **yes** |

Count: 18 of 22 variants accepted (including the V0 legit control); 4 refused
(Vd2a, Ve2b, Ve3, Ve4 — Vd2a is the only refusal the claim depends on).

## What the counter actually refuses

1. A quote that is only in the package copy, when the entry sits at the package
   basename (Vd2a; matches CTL_B's `entries=0` in `controls-at-freeze.stdout`).
2. Fragment/query **inside** the parsed URL (Ve3/Ve4: `doc_key` keeps them, so the
   key stops matching) — and it refuses silently: rows drop out before entries are
   examined, so the only symptom is `rows=0` and the entries' suppressed
   `cites no flaky row`.
3. Uppercase `WWW.` (Ve2b): `doc_key` strips `www.` case-sensitively
   (`measure.py:67-69`), so `WWW.ArXiv.org` keeps its `www.` prefix and misses.

Correction to the item's premise for (e): `doc_key` does **not** accept a trailing
fragment or query on the parsed URL. What it does accept is a trailing slash and an
uppercase host without `www.`; and because `URL_RE` stops at `;`, a fragment/query
placed after a semicolon is never parsed and the row is accepted (Ve8).

## Accepted cheats, and the Gate check that closes each

The Gate block must carry the act's evidence; the counter's output strings are all
forgeable without performing the act.

**A. Quote is boilerplate / claim is fabricated / one sentence reused (Va, Vb, Vc).**
Gate check: per entry, (i) the located quote's character offset in the extracted
snapshot falls inside the document's evidence region — after `Abstract:` for the
arXiv and TUM snapshots, inside `entry.content.$t` for the feed — not in chrome
(`Skip to main …`, cookie/licence footers, `Submission history`, feed envelope);
(ii) every numeric/factual claim in the entry is mapped to a located quote in the
same entry, and a non-author re-derives the number from the snapshot;
(iii) the three entries carry three distinct located quotes, each from the row's
own document. Va/Vb/Vc fail (i) or (ii)/(iii).

**B. Anti-relabel check is basename-scoped (Vd, Vd3, Vd4, Vd5).**
Gate check: show a real body diff of each new entry against
`.ufo/evidence/round-46/assimilation/package/<same basename>` and state what was
re-derived; reject a body that is the package body modulo the provenance trio and
one appended sentence. Reviewers must also check the entry basename is the frozen
one (`r6-flaky-failures-cluster.md` for S258, `r5-undetected-flaky-failures.md` for
S259, `r9-false-red-rate.md` for S260) and that the three package copies are
byte-identical to the freeze commit (`git diff 745a5831..REV --
.ufo/evidence/round-46/assimilation/package/` empty). Vd3/Vd5 die on the basename /
package-copy check; Vd and Vd4 need the body-diff + load-bearing-quote check (the
fresh quote must be the sentence the claim rests on, not a parked "rejected" line).

**C. Anchor is decoupled from the source cell; snapshots can be replaced (Ve5, Ve6,
Ve7).** Gate check: a per-row mapping table — row id → exact source URL → snapshot
filename → sha256 — where the snapshot filename is the one committed for that URL
at freeze, plus `git diff 745a5831..REV -- .ufo/evidence/round-46/coverage/sources/`
empty (so the bytes are the frozen bytes) and a live-fetch receipt
(`curl -fsSL <URL> | sha256sum`) if any snapshot is re-pinned. The counter never
ties `cells[2]` to `cells[6]`; only this table does.

**D. README "index" can be a fenced example (Vf).** Gate check: show the three
README index **table rows** verbatim (`| \`knowledge/<name>.md\` | … | S25x |`) and
confirm each path's first occurrence is inside a table line, not a fenced block or
an HTML comment. The counter is a plain substring test (`measure.py:170`).

**E. Ids and dates are unconstrained (Vh, Vi, Vg).** Gate check: the counter line's
`row_ids` must read exactly `S258,S259,S260`, backed by
`.ufo/evidence/round-46/assimilation/{guard-map.json,adoption-map.json}`; each
entry's `verified-at` must be an access date actually used this round (≤ today) and
the `recheck:` command must have been run. The counter accepts any `S\d{3,}` id,
any date ≥ 2026-10-25 (including future), and any text after `verified-at:`.

**F. Cell can carry extra URL-ish tokens (Ve8, Ve1, Ve2a).** Gate check: quote the
source cell verbatim and confirm it contains exactly one `http` occurrence and no
`;#`/`;?` tail; confirm the URL's canonical form against the frozen `DOCS` tuple
(`measure.py:37-41`). Only the first URL is parsed, so a second, contradictory
source in the same cell is invisible.

## Smallest safe correction (recommendation only — the counter is frozen)

Ordered by leverage; each is a few lines and none changes the frozen predicate's
intent:

1. Bind anchor → document: a frozen `SNAP_OF = {'arxiv.org/abs/2504.16777':
   'arxiv-2504.16777-abs.html', …}` and require `cells[6]`'s snapshot basename to be
   the one for `doc_key(cells[2])`. Kills Ve5/Ve6 at zero cost.
2. Pin the snapshot bytes: require the three snapshots' sha256 to equal constants
   committed at freeze. Kills Ve7.
3. Locate the package copy by the row's document map, not by the entry basename, and
   compare against every package copy whose basename the entry's name contains.
   Kills Vd3/Vd5.
4. Require the fresh quote to be the **first** quote in the entry body and outside
   fenced blocks and lines containing `reject`/`not used`. Kills Vd4.
5. Require each admitted entry to cite exactly the row whose `doc` it quotes, and
   require the three admitted entries' located quotes to be distinct. Kills Vc and
   Va's cross-row citation.
6. Restrict quotes to the evidence region: for HTML snapshots, take the text after
   the first `Abstract:` marker (or a frozen byte span); for the feed, the decoded
   `entry.content.$t`. Kills Va.
7. README index must match a table-row regex, e.g.

   ```
   ^\|\s*`?((corpus/)?knowledge/[A-Za-z0-9._-]+\.md)`?\s*\|
   ```

   Kills Vf.
8. Id allow-list `{S258,S259,S260}`, exact canonical URL strings (no
   slash/case normalization), `verified-at` exact-line match and ≤ today. Kills
   Vh/Vi/Vg/Ve1/Ve2a/Ve8.

Items 1–3 are defects relative to the claim's own wording ("committed snapshots"
for the frozen documents; "the package copy of the same entry"), not merely
tradeoffs — though note the counter's docstring already narrows the last one to
"same basename", so the docstring is the text that should be tightened. Items 4–8
are tradeoffs of a cheap textual predicate; the canonical Rust judge must decide
whether the claim's words "re-grounded" and "indexed" are meant mechanically.
Until then the Gate block is the only closing check.

## Evidence notes

- Snapshot digests used by every accepted row (freeze bytes, unchanged):
  `28d2954d…` arXiv, `5eb59adf…` TUM, `434d8658…` feed — the same prefixes ScribeRows
  reports; the counter re-hashes the blob at REV and matches any 8+-hex token in the
  anchor cell (`measure.py:110-118`).
- Each run prints `REFUSED … no provenance trio` for 23 of the 52 pre-existing
  `corpus/knowledge/*.md` entries; the other 29 start with `source:` and cite no
  flaky row, so they are skipped silently. That noise does not affect the verdict,
  but it means the entry census scans the whole directory (a nested subdirectory
  entry would not be listed by `git ls-tree --name-only corpus/knowledge/`).
- `git show` refuses `..` path components, so an anchor cannot escape `sources/` by
  traversal (probe: `fatal: path '…/sources/../../assimilation/package/…' exists on
  disk, but not in 'HEAD'`). The provenance hole is the sibling-document anchor
  (Ve5/Ve6), not traversal.

## Not run / tooling

- No deciding run: the L1 owns `--rev 745a5831…`. My runs are scratch-only and
  reported as such; no run is a verdict.
- No counter, contract, registry, entry, snapshot, lane git/jj state or fleet file
  was edited. Only this report was written in the lane.
- No tool installed or upgraded (nothing was needed); no pacman transaction.
- Not exercised: C1/C2 counters, the census, the no-harm script — outside this
  item.
