# SentinelScope — round 40 w1 (scope + adjacency, `r40-write-form-misses.md`)

Axes: (1) quantification precision of the entry's claim, (2) province containment / refusal of
sibling absorption, (3) the two named live sites are real and match the frozen C1 wording.

## Verdict

**Only two named sites. The entry does not claim a universal write census, and it says so in
its own words.** No sibling-domain absorption found. One LOW scope ambiguity remains: the
denominator behind "live hits" is two hard-coded files, not the tree, and the entry never
states that boundary.

## Evidence

Entry, quoted at the load-bearing lines:

- `corpus/knowledge/r40-write-form-misses.md:6` — title is bounded: "**Two** write forms the
  frozen census pattern does not see" (a count of two forms, not of all forms).
- `corpus/knowledge/r40-write-form-misses.md:10` — scope is the tool delta plus five planted
  fixtures: "classifies **two forms** that `tools/write-path-census.py` … misses"; the fixture
  set is "the discriminating set".
- `corpus/knowledge/r40-write-form-misses.md:18` — explicit non-universal clause: "The live
  hits are two named sites … **They are not a claim that every write in the tree is
  classified**, and not a claim that the `os.replace` site writes an expected value. The
  destination there is a variable."

Site verification (both true, and both v1 misses):

```
$ sha256sum tools/write-path-census-v2.py tools/write-path-census.py
4022853295882c5a11e192274e9215ea5a008e54eb0a2f77a8a2365f522d878b  tools/write-path-census-v2.py
bc8c660c56f871f85dad8912be28446293fd63f62b4fd1c16eb153f7a27edc62  tools/write-path-census.py
```
Both match `contract.json` C1 `tool_sha256` / `v1_sha256` at the frozen rev `5641ed8`.

```
$ sed -n '123p' tools/registry-replay.py
    (out / 'expected.json').write_bytes(encode({'schema': 'command-binding-expected-v1',
$ sed -n '778p' tools/bash-witness-study.py
    os.replace(tmp, path)
```

v1 misses both, by regex difference: `tools/write-path-census.py:51-53` EXPECTED_RE has
`.expected|expected.txt|golden|snapshot` but not `expected.json`; `:46-50` WRITE_RE has no
`os.replace`. v2 adds both (`tools/write-path-census-v2.py:18-22`). Neither file contains a
`FLAG_RE` token (`grep -nE -- '--update_goldens|--update-goldens|--update\b|update_goldens'`
→ NONE for both), so v2's file-wide suppression does not zero either hit.

Scratch-copy selftest (tool copied to `/tmp/tameshi-r40-SentinelScope/`, live lane untouched):

```
$ python3 v2.py --selftest --fixtures …/census/fixtures.json
WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0
exit=0
```

## Adjacency — no absorption

- The entry names no sibling lane, gate, or product clause:
  `grep -nE 'kagi|kumitate|tsukuroi|mado|kaidoku|kama|shokuknow|sibling' corpus/knowledge/r40-write-form-misses.md` → `NONE`.
  Both named tools are this lane's own instruments (`tools/`).
- `PROVINCE.md:14-16` admits a pattern as *general* only from two independent lanes. The entry
  never claims generality — it pins to one v1 tool blob and two sites — so the two-lane gate is
  not triggered and not dodged.
- `PROVINCE.md:44-47` marks screenshot/UI diffing adjacent (S030) and every sibling gate's code
  owner-held. The entry touches neither: it cites S152 only for the abstract's fragility
  sentence (`:14`), and S152 is an already-mined tier-B row, `corpus/SOURCES.md:122`, with prior
  admission at `corpus/knowledge/r6-snapshot-practice-corpus.md:1`. `:14` explicitly narrows the
  citation to that sentence "not a count of the lane's gates".

## Residual defect (LOW) — "live hits" has an unstated denominator

`corpus/knowledge/r40-write-form-misses.md:18` says "The live hits are two named sites", but the
counter's live check reads exactly two files, not the tree:

```
$ grep -n "git_show(args.lane, args.rev" .ufo/evidence/round-40/census/measure.py
189:    replay = git_show(args.lane, args.rev, 'tools/registry-replay.py')
190:    witness = git_show(args.lane, args.rev, 'tools/bash-witness-study.py')
```

The same expected-token class has a **third** unflagged in-lane instance the counter never
examines. Classifier output from the scratch copy over read-only lane files:

```
registry-replay.py: write_sites=5 unflagged=1
bash-witness-study.py: write_sites=24 unflagged=0
wave-accounting.py: write_sites=2 unflagged=1
wave-accounting:165: (work / 'expected.json').write_text(json.dumps({
line EXPECTED_RE: True WRITE_RE: True SCRATCH: False file FLAG: False
```

`tools/wave-accounting.py:165` is a v2-class hit (expected token + write call + no scratch token
+ no flag token in the file), and v1 would also miss it, since v1's EXPECTED_RE lacks
`expected.json`. Also, v2 classifies `os.rename` (`tools/write-path-census-v2.py:21`) while
entry `:10` names only `os.replace`; six live `os.rename` sites exist
(`tools/pin-disposition.py:1163,1183,1186,1206`, `tools/evidence-disposition.py:2266,2330`), two
of which target sibling paths.

Impact: none on the predicate — C1's wording names exactly these two files, so entry and counter
agree. The risk is citation: a later seat can read `:18` as a tree-wide enumeration ("the lane
has exactly two unflagged expected writes") and be wrong by one on the very class the round
added. That is a scope-adjacency risk, not a universal claim.

Smallest remediation (doc-only; not applied — report path only, live checkout untouched): add
one clause to `:18` naming the population, e.g. "live hits" = the counter's two hard-coded
paths at `.ufo/evidence/round-40/census/measure.py:189-190`; `tools/wave-accounting.py:165` is
the same class outside that population. No predicate change, no tool change.

Boundary: no counter was run in default mode; `--control`/`--selftest` only, plus a scratch copy
in `/tmp/tameshi-r40-SentinelScope/`. Lane Git index, `.ufo/state`, jj state and domain trees
were not written; base `304e3355…` is untouched.
