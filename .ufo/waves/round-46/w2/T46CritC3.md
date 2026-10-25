seat: T46CritC3
item: attacked C3 as declared in the round-46 contract vs as delivered at content revision 6f2168e0 — expansion-credit honesty (is the third row coverage or re-covering?), sourced-claim and Gate-quote reality, package-copy re-grounding vs relabel, the id map and the S225/S229/S235 dedupe, the quarantine slice, `F3 stays open`, and the before/after cells.

# T46CritC3 — C3 (coverage) attack

Scope: critic only. I am not an author of any artifact below. Read-only on the lane
except this report. Scratch: `/tmp/tameshi-r46-T46CritC3/` (counter runs, extractor
outputs, one scratch adoption map, live fetches). No git/jj write command was run in
the lane; no fleet, package or sibling-lane file was touched; no tool was installed or
upgraded (nothing was needed); no pacman transaction.

Revisions: content revision under attack `6f2168e028ce7ff6e82ac92093ac05dd1f147c32`
(lane HEAD is `eada0b3`, which adds only `.ufo/waves/round-46/{spec-w2.json,w2-dispatch.json,w2/swarm-registry.json}` —
`git diff --name-status 6f2168e0..HEAD`). Freeze `745a5831…`, base `683eedd…`.

## 1. Counter runs I took (observed, not verdicts)

```
$ python3 .ufo/evidence/round-46/coverage/measure.py --selftest | tail -2
C3_R46_SELFTEST: cases=24 failed=0
VERDICT: PASS                      # exit 0

$ python3 .ufo/evidence/round-46/coverage/measure.py --lane . --rev 6f2168e028ce7ff6e82ac92093ac05dd1f147c32 | tail -1
C3_R46: self_pin=1 rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260 rev=6f2168e028ce7ff6e82ac92093ac05dd1f147c32 C3_R46_PASS=true
                                   # exit 0

$ python3 .ufo/evidence/round-46/coverage/measure.py --lane . --rev 683eedde3a50441c34d85a22f5fd5346f8b1ec6d | tail -1
C3_R46: self_pin=0 rows=0 entries=0 indexed=0 covered=0 row_ids=- rev=683eedde3a50441c34d85a22f5fd5346f8b1ec6d C3_R46_PASS=false
                                   # self_pin=0 because the counter file does not exist at base; rows=0 is the claim's before state

$ tail -1 .ufo/evidence/round-46/before/c3-at-freeze.stdout
C3_R46: self_pin=1 rows=0 entries=0 indexed=0 covered=0 row_ids=- rev=745a583181648cfc7f9c1b476cd1be7dc68f7433 C3_R46_PASS=false
```

Frozen bytes are the frozen bytes at the content revision:

```
$ git diff --stat 745a5831..6f2168e0 -- .ufo/evidence/round-46/assimilation/package/ .ufo/evidence/round-46/coverage/sources/
(empty; rc=0)
$ sha256sum .ufo/evidence/round-46/coverage/sources/*
28d2954d22ea45af7bd0454f1a8b01bb5db40e8e5cc235eed176a1621aa26a14  arxiv-2504.16777-abs.html
434d86586ecf3ea03f57d4342c6e8575576eef6a9fd452a5c0a9e67bd8889929  google-flaky-feed-6277555988217606236.json
5eb59adf099304a07059530b0857f7b517eaa72c832049f46952915a77e71a6f  tum-portal-flaky-failures.html
$ sha256sum .ufo/evidence/round-46/coverage/measure.py
f8bfefdf6c08ce880c3f329018d946168dd022c50391d24551853326dbcfb5f5   (unchanged since the freeze)
```

So the counter, snapshots and package copies are byte-identical to the freeze, and the
declared C3 predicate is met at the content revision. The attacks below are about what
the record *claims*, not about the predicate.

## 2. Findings

### F1 — HIGH — the stated reason for the third row is false against the lane's own committed bytes

**Attacks:** `corpus/README.md:577` (round-46 section), the justification for row S260 /
entry `r9-false-red-rate.md` — the third row the C3 target `rows>=3` needs.

The sentence:

> The rendered Google blog page is already held as S026; S260 is the publisher's
> per-post feed record of the same post, **adopted because the rendered page's body sits
> in a script template that the lane's HTML extraction discards.**

The lane already holds a committed snapshot of that rendered page — taken and committed
in round 45 for the held-row freshness ledger:

```
$ gunzip -c .ufo/evidence/round-45/freshness/sources/S026.raw.gz > /tmp/tameshi-r46-T46CritC3/s026/S026.html
$ ls -l /tmp/tameshi-r46-T46CritC3/s026/S026.html
-rw-r--r-- 1 vgpnk vgpnk 236387 … S026.html
$ python3 .ufo/evidence/round-45/freshness/measure.py --extract /tmp/tameshi-r46-T46CritC3/s026/S026.html | wc -c
26626
$ grep -c '84% of the transitions we observe from pass to fail' /tmp/tameshi-r46-T46CritC3/s026/extract.txt
1
$ grep -c 'Almost 16% of our tests' /tmp/tameshi-r46-T46CritC3/s026/extract.txt
1
```

The round-46 counter's own normaliser gives the same result, and **all 19 of the r9
entry's located quotes are locatable in the held S026 snapshot**:

```
$ # norm_text from .ufo/evidence/round-46/coverage/measure.py applied to S026.html
norm_text len 26246
1 | about 84% of the transitions we observe from pass to fail involve a flaky test
1 | Almost 16% of our tests have some level of flakiness associated with them
1 | It is quite common to ignore legitimate failures in flaky tests due to the high number of false-positives
1 | causing it to report a failure only if it fails 3 times in a row
1 | The breakage will not be discovered until 3 executions of the test complete, or 45 minutes
1 | A tool that monitors the flakiness of tests and if the flakiness is too high, it automatically quarantines the test
r9 quotes=19 located_in_S026_norm_text=19
```

The held entry itself already records that the body is served twice, not discarded
(`corpus/knowledge/repeated-control-precondition.md:16`):

> S026 post body (`S026.html:1130-1137`; the same bytes are served again in a
> `text/template` copy at `:1095-1102`):

**Impacted:** coverage axis credit (the third row exists to reach `rows>=3`); the
round-46 README record. **Not impacted:** the counter's predicate, the row's URL, the
snapshot, or the entry's quotes — the feed record is a genuine second carrier and the
r9 entry's quotes are real.

**Smallest safe correction:** replace the reason with the true one (the publisher's
per-post record is directly machine-readable and counter-gradable, and it is a stable
publisher-side carrier), and state that the held S026 snapshot already supplies the
same quotes. One sentence; no artifact re-runs.

Note on severity: sibling seat `w2/T46RevGate.md` rates the lesson's weaker parenthetical
("keeps it in a script template") LOW after a live fetch.
I escalate to HIGH because the README says *discards*, and the refutation is not a live
fetch but the lane's own committed round-45 snapshot plus the held entry's own note that
the bytes are duplicated — and because this sentence is the only stated reason for the
row the target needs.

### F2 — LOW — "three documents / three measurements" is one more than the round's own Gate allows

**Attacks:** `SCORECARD.md:2208` ("C3 **three flaky-failure documents** enter as rows
S258/S259/S260 …"), `corpus/README.md:577` ("Frontier F3 … gains **three published
measurements**"), `PROVINCE.md:123` ("gains **three published measurements** through
admitted, source-headed entries citing mined rows S258, S259 and S260"), against
`corpus/lessons/round-46.md` (`## Gate`, S260 admit): "Two of the three entries are on
unheld ground …; this one is not, and the round does not claim it as expansion."

What the third row/entry actually covers, measured:

- Document identity: the feed record's `entry.link[rel=alternate].href` is
  `https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html`
  (`python3` decode of the committed snapshot), i.e. the document the lane already holds
  as **S026** (`corpus/SOURCES.md:37`, status `mined`, used-by
  `corpus/knowledge/repeated-control-precondition.md`).
- Held claims: of r9's 19 located quotes, **5 are already verbatim in the held entry**
  and several more are held in paraphrase —

```
r9 quotes=19 already_in_held_entry=5
HELD  a test that exhibits both a passing and a failing result with the same code
HELD  Almost 16% of our tests have some level of flakiness associated with them
HELD  about 84% of the transitions we observe from pass to fail involve a flaky test
HELD  This reduces false positives, but encourages developers to ignore flakiness in their own tests
HELD  The breakage will not be discovered until 3 executions of the test complete, or 45 minutes
```

  and the held entry states the 1.5 % rate, the 16 % reach, the 84 % transitions, the
  wait-for-CI-cycles mitigation and the 45-minute latency at
  `repeated-control-precondition.md:19-22`.
- CORPUS rule 4 (`CORPUS.md:123`, "Expansion is knowledge, not rows") counts admitted
  `knowledge/` entries citing a mined row on uncovered ground. r9's ground is F3, the
  same ground the held F3 entry already covers with the same document.

Honest count: **two new documents (S258 arXiv clustering, S259 same-job-rerun blind
spot) + one carrier repair (S260 = S026's document)**. The r9 entry is not empty — it
adds ~14 newly located sentences from the held document, of which the materially new
claims are the masking habit, the alarm analogy, the quarantine risk, the steady-state
insertion rate and the project-scale arithmetic — but it is not new-document coverage,
and the lesson says so while the three records above do not qualify it.

**Impacted:** coverage axis credit framing. **Smallest safe correction:** state "two new
documents + one carrier repair (S260 = S026's post under the publisher's per-post
record); coverage credit 2 documents / 3 rows" in the C3 SCORECARD cell and the README
section. The declared C3 predicate (`rows>=3 entries>=3 indexed==entries covered==rows`)
is unaffected and remains met.

### F3 — LOW — the adoption map's key choice defeats the guard's own document check

**Attacks:** `.ufo/evidence/round-46/assimilation/adoption-map.json` and the contract's
phrase "adopted at guard-admitted ids S258/S259/S260".

The guard validates a *candidate* map and treats a target that already exists in the
registry as a document dedupe only when the staged row's document key equals the
registry row's. Re-running the frozen guard at the content revision:

```
$ python3 -I tools/staged-id-guard.py --registry corpus/SOURCES.md \
    --staged /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md \
    --map .ufo/evidence/round-46/assimilation/adoption-map.json --json
verdict inadmissible
map_reasons ['map targets collide with registry ids: S259,S260']
map_clash ['S259','S260']   map_dedupe {'S153':'S105','S154':'S106','S159':'S155','S160':'S156','S195':'S258'}
registry_rows 120   registry_max S260   safe_floor S261   collision_count 8
```

Cause, from the guard's own normaliser:

```
registry S258 -> arxiv.org/abs/2504.16777
registry S259 -> portal.fis.tum.de/en/publications/an-empirical-study-of-detected-and-undetected-flaky-test-failures
registry S260 -> testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json
staged   S195 -> arxiv.org/abs/2504.16777
staged   S190 -> doi.org/10.1109/tse.2026.3729363
staged   S216 -> testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json**
staged   S225/S229/S235 -> testing.googleblog.com/feeds/posts/default/6277555988217606236?alt=json
```

S195→S258 dedupes cleanly (same key). S190→S259 is a carrier substitution (DOI vs the
institutional record) and cannot dedupe by construction — the lesson states the DOI
serves an empty body, so this is disclosed, not hidden. S216→S260 fails only because the
chosen staged key carries Blogger's bold markers (`…?alt=json**`); the same feed document
is staged three more times with clean keys. Keying the map by **S225** instead makes the
guard record the dedupe and leaves only the disclosed S259 substitution:

```
$ # scratch map: S216 replaced by S225, /tmp/tameshi-r46-T46CritC3/adoption-map-S225.json
verdict inadmissible   map_reasons ['map targets collide with registry ids: S259']
map_dedupe {'S153':'S105','S154':'S106','S159':'S155','S160':'S156','S195':'S258','S225':'S260'}
```

**What this does and does not mean.** `guard-map.json` (verdict `admitted`, `registry_rows
117`, `registry_max S257`, `safe_floor S258`) is a *pre-append* id-availability receipt and
is true of its moment; it is not a standing document-identity check. The deciding run does
not invoke the guard (`grep -n 'staged-id-guard' .ufo/evidence/round-46/deciding-run.sh` →
no match), so there is no interaction with a verdict. **Smallest safe correction:** key the
map by S225 and record S190→S259 explicitly as a carrier substitution in the map's note
(the note currently says only "S190->S259 (TUM portal record of the TSE 2026 paper)").

### F4 — INFO — the SCORECARD's after receipt does not exist at the content revision (expected)

`SCORECARD.md:2208` names `.ufo/evidence/round-46/after/c3.stdout` as the deciding
receipt; `ls .ufo/evidence/round-46/after/` → the directory is empty. This matches the
declared landing rule (deciding runs at the content revision, then a receipts-only
commit), so it is not a defect at this point; it is unverifiable until the L1's run. My
independent run at the content revision reproduces the after cell character for
character (section 1), including `row_ids=S258,S259,S260`.

### F5 — INFO — none of the accepted cheat shapes from the wave-1 cheapest-pass attack is present

`w1/CritC3Control.md` lists 22 variants; 18 were accepted by the counter. Checked against
the delivered artifacts, none of the accepted shapes is present:

| shape | check I ran | result |
|---|---|---|
| Va boilerplate/nav quotes | located quotes of each entry read and located in its own document | 15/15 (r6), 19/19 (r9); r5 13 snapshot quotes located, the other 12 are lane-file quotes (`corpus/README.md:80,127`, `tools/repeat-control.py:18,94`) or quotes of package claims being corrected — verified against those files |
| Vb fabricated figures | every number in the three entries matched to its snapshot | all located, e.g. `75%`, `810`, `10,000`, `24`, `13.5`, `1.28%`, `$2,250` (arXiv, count 1 each); `8.8 billion`, `9.8 %-16.3 %`, `3×`, `154,000`, `1.7 million` (TUM, 4/3/3/4/4); `1.5%`, `1000`, `15 tests`, `45 minutes`, `3 times in a row` (feed) |
| Vc one quote reused | distinct quotes per entry | distinct; no cross-row citation (r6 cites S258 only, r5 S259, r9 S260) |
| Vd/Vd3/Vd4/Vd5 relabel or parked quote or deleted package | entry basenames are the frozen ones; package copies byte-identical to the freeze (`git diff` empty); fresh quotes sit in the body | 8-word shingle overlap with the package copy, quotes removed: r6 `0.020`, r5 `0.005`, r9 `0.006` — rewrites, not relabels; r6's own count "14 of the 15 located quotes do not occur in the package copy" reproduces exactly (`quotes=15 located=15 fresh_vs_package=14`); r9 `19/19 located, 16 fresh`; r5 `11 fresh` |
| Ve5/Ve6 cross-document anchor | row → snapshot mapping | S258→`arxiv-2504.16777-abs.html` `28d2954d`, S259→`tum-portal-flaky-failures.html` `5eb59adf`, S260→`google-flaky-feed-…json` `434d8658`; each anchor names its own document's snapshot and digest |
| Ve7 replaced snapshots | `sha256sum` at the content revision | matches the freeze digests (section 1) |
| Vf fenced "index" | `corpus/README.md:573-575` context | three index **table rows** inside the `## Round 46` table (`\| Note \| Holds \| Sources \|`), not a fenced block |
| Vh ids / Vi,Vg dates | counter line + entry headers | `row_ids=S258,S259,S260`; `verified-at: 2026-10-25` in all three entries (today) |
| Ve1/Ve2a/Ve8 URL forms | row source cells | each source cell holds exactly one `http` occurrence and no `;#`/`;?` tail; anchors hold none; 13 fields per row, status `mined`, opened `2026-10-25`, `recheck 365d`, used-by exactly the entry path |

Registry census at the content revision: `rows=120`, malformed `0`, duplicate ids none,
mined used-by paths all exist (CORPUS census block).

## 3. The item's specific checks, each with its evidence

### 3.1 Expansion credit — what was already held

- arXiv 2504.16777 (clustering): **unheld**. `grep -rln 'mean cluster size\|co-occurring failures' corpus/knowledge/`
  → only `corpus/knowledge/r6-flaky-failures-cluster.md`. The round-43/46 held sweep
  agrees. This is real expansion.
- TUM portal record (same-job rerun blind spot, 9.8 %–16.3 %): **unheld**.
  `grep -rln '9\.8 %\|9\.8%' corpus/knowledge/` → only `r5-undetected-flaky-failures.md`.
  The package's "S140, round 5" cross-reference does not resolve to a lane row: S140 is a
  retired shokuknow id remapped to **S184**, which the package itself defines as the
  lane's own F5 env-diff receipt, not the paper (`SOURCES.append.md:38`,
  `ID-REMAP.md:84`). This is real expansion.
- Google post: **held at the claim level**. S026 (`SOURCES.md:37`) already teaches "about
  1.5% … about 84% of pass-to-fail transitions … a fail-3-in-a-row flaky mark cuts false
  positives but teaches people to ignore flakiness", and
  `repeated-control-precondition.md:19-22` quotes the same post at `S026.html:1130-1137`.
  So `coverage` moves on two documents and is re-covered on the third; the lesson says
  so, F1's README sentence says otherwise with a false reason, and F2's three records
  state the gain unqualified.

### 3.2 Sourced claim: each entry cites its row opened this round, with a located Gate quote

Rows: S258/S259/S260 appended this round, `mined`, opened `2026-10-25`, each with one
snapshot + 8-hex digest in the anchor and exactly one entry in used-by. Gate quotes
re-located with the counter's own `fold`/`norm_text`:

| row | lesson Gate quote | tokens | occurrences in the folded snapshot |
|---|---|---|---|
| S258 | "finding that 75% of flaky tests across all projects belong to a cluster, with a mean cluster size of 13.5 flaky tests" | 22 | 1 (matches the lesson's "found once") |
| S259 | "We found that, across all projects, undetected flaky failures account for 9.8 %-16.3 % of failed pipeline runs." | 18 | 3 (matches "three times") |
| S260 | "about 84% of the transitions we observe from pass to fail involve a flaky test" | 15 | 1 (matches "found once") |

Entry headers cite exactly their own row; no cross-row citation; `verified-at:
2026-10-25` on all three. The S258 Gate quote is not fresh against the package copy
(`w1/ScribeRows.md` flags it "no") — that is allowed: the Gate needs a located quote, and
the *entry* carries 14 fresh ones.

### 3.3 Re-grounded, not relabelled

Beyond F5's shingle/quote evidence, the re-grounding is visible in content: r6 drops the
package's `ground: F8` primacy and its "S140, round 5" attribution; r5 corrects the
package's "online date 2026-09-19" (snapshot count `0`), its "open access per the
institutional record" (markup marker only, `open-access` class count `1`), and its
"S107" misattribution (S107 is the TensorFlow Federated golden-tests row,
`SOURCES.md:119`); r9 drops the package's rerun-price arithmetic and its "S156" detection
floor (no held row carries them: `grep -rn '5\.67'` over `corpus/` hits only the package
copy and the lesson). The r5 lane-file citations reproduce at the stated lines
(`README.md:80,127`; `tools/repeat-control.py:18,94`;
`hermetic-env-differential.md:2,4` "nine pinned surfaces … seven profiles"; `S107` at
`SOURCES.md:119`).

Live recheck honesty (fetched 2026-10-25 into scratch, read-only):

```
feed  434d86586ecf3ea03f57d4342c6e8575576eef6a9fd452a5c0a9e67bd8889929   == committed snapshot
arXiv 28d2954d22ea45af7bd0454f1a8b01bb5db40e8e5cc235eed176a1621aa26a14   == committed snapshot
TUM   a6c246ed0fbe0732066ca1b39beabe0a2dae97063216a2501e7c48470511c44c   != snapshot (volatile page)
      extract: live words 1668, snapshot words 1668, identical=True; quote count 4
```

The feed's two grep counts are `1` and `1`, exactly as the r9 recheck states; the TUM
page is a third distinct digest but its normalized text is still word-for-word the
snapshot's, exactly as the r5 recheck says ("the drift signal is the count falling to 0,
not a digest mismatch"). No recheck claim is overstated.

### 3.4 Id map and the S225/S229/S235 dedupe

`adoption-map.json` maps 11 staged rows; the feed document is staged four times
(`grep -c '6277555988217606236' /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md`
→ `4`; rows S216/S225/S229/S235, all the per-post feed), and S225/S229/S235 carry the
clean document key. The dedupe is therefore real; only the map's *key choice* weakens the
guard's ability to show it (F3). S153/S154/S159/S160 → held S105/S106/S155/S156,
S155-S158 → S261-S264 map-only (no `S261`-`S264` row exists: registry max is S260), and
nothing was appended under the round-45 map-only targets. See F3 for the post-append
guard reading.

### 3.5 Quarantine slice

```
$ diff .ufo/evidence/round-45/assimilation/quarantine-slice .ufo/evidence/round-46/assimilation/quarantine-slice
IDENTICAL
$ wc -l < .ufo/evidence/round-46/assimilation/quarantine-slice
17
$ grep -cE 'S(190|195|216)' .ufo/evidence/round-46/assimilation/quarantine-slice
0
```

No adopted document is in the slice; the slice's ids are campaign ids S105–S143, and the
package's "S140" reference is a retired id (F3.1), not an adopted document. No new
verdict is claimed for any slice row.

### 3.6 `F3 stays open`

```
$ git diff 683eedd..6f2168e0 -- corpus/README.md | grep -E '^[-+]\| F3|^[-+]\| F5|^[-+]\| F7'
(no output — the frontier rows are unchanged)
```

`README.md:80` still reads F3 `open`; the round-46 section and `PROVINCE.md:123-127` both
say F3 stays `open` and that the entries state literature measurements, not the lane's
controls; the three entries say the same (`r9`: "F3 stays open"; `r6` §2 and `r5`
"the lane's own F3 verdict on its fleet legs remains unmade"). Honest.

### 3.7 Before/after cells

| cell | stated | observed |
|---|---|---|
| C3 before | `rows=0 entries=0 C3_R46_PASS=false` at `745a5831` | reproduced exactly (`before/c3-at-freeze.stdout`, section 1) |
| C3 after | `rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260 C3_R46_PASS=true` at `a6892b1` | reproduced exactly at `6f2168e0` (section 1) |

The after value was measured at a wave-1 commit and holds at the content revision; the
deciding receipt itself is not yet written (F4).

## 4. The strongest argument that C3 is not coverage expansion — and whether it holds

**Argument.** C3's coverage movement is two documents, not three. The third row (S260) is
a second carrier of a document the lane already holds as S026: the feed's own
`entry.link[rel=alternate].href` points at the S026 URL; the lane's committed round-45
snapshot of S026 supplies every one of the r9 entry's 19 located quotes under both the
round-45 extractor and the round-46 counter's own `norm_text`; the held F3 entry already
states the post's principal claims (1.5 %, 16 %, 84 %, fail-3-in-a-row, 45-minute
latency) at `repeated-control-precondition.md:19-22`; and the round justifies the row
with a technical premise ("the lane's HTML extraction discards" the body) that the lane's
own committed bytes refute. Under CORPUS rule 4 ("expansion is knowledge, not rows"), the
third entry lands on F3 ground the same document already covers. The honest expansion
count is therefore 2 documents / 3 rows, which is what the lesson's Gate says and what the
SCORECARD cell, the README section and the PROVINCE append do not.

**Does it hold?** It holds as far as *document* coverage and the stated rationale go, and
it does not touch the declared claim. The declared C3 surface is keyed by URL and says so
("0 rows and 0 entries citing arxiv.org/abs/2504.16777, the TUM portal record … or the
Google … feed at base"); the three URLs are exactly those; the rows, snapshots, entries
and index are real; the counter passes at the content revision; and the lesson discloses
the carrier nature of the third. What fails is narrower and fixable in prose: (i) the
README's reason for the third row is false (F1, HIGH); (ii) three records state the gain
as three documents/measurements without the lesson's qualifier (F2, LOW); (iii) the id
map's key choice leaves the guard unable to show the feed dedupe it claims (F3, LOW). The
claim survives; the record's coverage credit should read 2 documents + 1 carrier repair.

## 5. Unreproduced / not run

- **Unreproduced:** nothing. Every finding above was reproduced from committed bytes; the
  three live recheck claims (feed digest, arXiv digest, TUM word-for-word text) were
  re-fetched and matched or matched in text.
- **Not run:** C1 and C2 counters, the no-harm script, the census-end receipt and the
  deciding run — outside this item and owned by the L1. No deciding run was taken; my
  counter runs are scratch observations, not verdicts.
- **Tooling:** no tool installed or upgraded; no pacman transaction; bash + python3
  stdlib only. Scratch: `/tmp/tameshi-r46-T46CritC3/`.
