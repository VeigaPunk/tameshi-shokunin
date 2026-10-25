seat: ConnSeparability

# Round-45 C1/C2 claim separability + integration no-harm cross-check (ad5942c6e9858af19d00000b58439b321ddfa62b)

## (a) Causal separability of C1 (freshness) and C2 (coverage)

The two claims are causally separable in both directions: neither counter reads the other's artifacts, and C2's rows are excluded from C1's population by id bound.

C1 population code — `.ufo/evidence/round-45/freshness/measure.py`:
- line 61: `MAX_ID = 160`
- lines 95-97:
```python
def population(rows):
    return {rid: r for rid, r in rows.items()
            if r['status'] == 'mined' and int(rid[1:]) <= MAX_ID and r['url']}
```
- C1 measure() inputs (lines 218-252): `corpus/SOURCES.md`, `ledger.json`, `reviews.json`, `.ufo/waves/round-45/w2-results.json`, and snapshot blobs under `.ufo/evidence/round-45/freshness/sources/`. None of these paths are written by C2.

Replication of population at ad5942 (read-only `git show`):
```
total_rows=117 population=73 max_pop_id=S160 above160_in_pop=[]
```
- C2 rows S256/S257 (present in SOURCES.md at ad5942, lines 131-132) have ids 256/257 > 160, so they are excluded from C1's population regardless of status/url. C1's population is byte-identical in size (73) to base.
- C1 ledger at ad5942: `entries=73 max_id=S160 above_160=[]` — no C2 id could even enter the ledger.

C2 counter inputs — `.ufo/evidence/round-45/coverage/measure.py` (`gt_rows` lines 67-90, `measure` lines 115-139): `corpus/SOURCES.md` (GoogleTest rows only), `corpus/knowledge/*.md`, `corpus/README.md`, `.ufo/evidence/round-45/coverage/sources/`. None of these are written by C1.

Directional conclusions:
- C1 verifies without C2 landing: fresh>=50 requires only <=S160 mined rows with URLs, C1's own ledger/reviews, and w2-results seat names; nothing C2 produces feeds those. Also C1's score/` population is unaffected by S256/S257 existing.
- C2 verifies without C1 landing: rows S256/S257, the two re-grounded knowledge entries, and the README index are self-contained; C2 never reads C1's ledger/reviews/results.
- No shared mutable artifact between the counters (only the shared read of SOURCES.md, and C2's additions to it are excluded from C1 by id).

## (b) Integration commit ad5942c6e9858af19d00000b58439b321ddfa62b

Commit stat (its own diff): only `corpus/knowledge/r8-gtest-order-and-seed.md` and `corpus/knowledge/r8-gtest-primer-independence.md`, 1 line each (entry errata: env-diff normalization claim corrected; primer wording softened). It touches no counter input of C1 or the round-44 counter.

Command D (depth axis):
```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show ad5942c6e9858af19d00000b58439b321ddfa62b:tools/mutate-and-run.sh | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
recorded_cases=9 depth_score=9
```
Depth axis intact (9 = base value).

Round-44 record-agreement counter (calibration no-harm monitor):
```
$ python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-44/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev ad5942c6e9858af19d00000b58439b321ddfa62b --freeze ba01973c73ad7de60e5bd19ae08255a1b7ef917e
C2_R44: self_pin=1 classes=7 m6=1 m7=0 m8=0 m10=0 m11=0 m12=0 m13=0 total=1 records=4 sources_rows=117 standing=115 receipts=17 revisions=4 m13_probe=standing=8_column0=116_valid=117 rev=ad5942c6e9858af19d00000b58439b321ddfa62b freeze=ba01973c73ad7de60e5bd19ae08255a1b7ef917e C2_R44_PASS=false first=m6:standing=115_actual=117
exit 1
```
At the same freeze, at base 5891bdb77aba8489683533ae4cdd3b49b5e2626b:
```
C2_R44: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=0 m12=0 m13=0 total=0 records=4 sources_rows=115 standing=115 receipts=17 revisions=4 m13_probe=standing=8_column0=114_valid=115 rev=5891bdb77aba8489683533ae4cdd3b49b5e2626b freeze=ba01973c73ad7de60e5bd19ae08255a1b7ef917e C2_R44_PASS=true
exit 0
```
So ad5942 fails the contract's no_harm `total=0` predicate (m6=1, total=1). Root cause: the wave-1 assimilation commit `3bf8bcd` ("integrate wave-1 C1 ledger ... and C2 adoption (S256/S257 rows ...)") grew the census-valid registry from 115 to 117 rows, while the newest standing `| sources-registry |` row (`SCORECARD.md` line 2146, the last such row) still states "115 rows at round 44". The m6 check (`measure.py` line 503-504, `row_count_claim(standing[-1])` vs `valid_count`) flags the stale claim. ad5942's own diff (knowledge-only) neither caused nor fixed this; the break entered with `3bf8bcd`.

S160 count monitor:
```
$ grep -cE '^ {0,3}\| S160 ' /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
1
```
Monitor stays 1 at the working tree (and 1 at ad5942 per the counter run / SOURCES.md state).

Summary of no-harm at ad5942: command D depth 9 ✓; S160 count 1 ✓; C1 population unchanged (73) ✓; round-44 record-agreement total=0 ✗ (m6=1, stale standing row) — the calibration no-harm monitor is NOT clean at the integration point and needs the later record edits below to reach total=0 at the deciding revision.

## Classes the round's later record edits (SCORECARD, LOG, lesson) must satisfy for the round-44 counter to stay total=0

Classes and their exact triggers (from `.ufo/evidence/round-44/calibration/measure.py`; contract round-44 `classes` field):

- m6 (`measure.py:501-504`): the NEWEST standing `| sources-registry |` row must state the census-valid row count. Currently `SCORECARD.md` line 2146 says "115 rows at round 44" while actual census-valid = 117 (S256/S257 adopted), so a new standing row must be appended stating `117 rows at round 45` (the counter reads only `standing[-1]`). This is the only class failing at ad5942.
- m7 (`measure.py:92-115`): every S-id cited by the round's records (round-45 SCORECARD block, LOG tail from the "round 45" marker, lessons round-42/43) must be a mined registry row. Masked-as-value forms: `staged:S###` (colon), `Next unused id: S###`, `next unused id` phrase, `safe floor` phrase, `register:S###`, assignment `key=S###` (incl. spaces). Pitfall: `staged S202` with a SPACE is NOT masked (`MASK_IDS`/`VALUE_ID_AFTER` only cover the colon form), so any lesson/scorecard mention of the staged ids S202/S203 (which are not registry rows) must use the colon/assignment forms or avoid citing them; any new unmined/unknown id flags.
- m8 (`measure.py:263-273`): every backtick path cite in records must resolve at REV after `:NN` normalization and brace expansion; directory cites resolve by prefix.
- m10 (`measure.py:276-345`): presence receipts under `.ufo/waves` must agree with the tree; only a receipt named in another receipt's `supersedes` is skipped, and the superseding receipt is graded. Any new receipt JSON carrying `present` bool claims (report/path target) must match tree reality.
- m11 (`measure.py:348-358`): every 40-hex object cited in records must resolve via `git cat-file -e` (object existence). Hex prefixes < 40 chars (e.g. sha256 `05546ed6`) are not checked; full 40-hex shas must exist.
- m12 (`measure.py:163-179`): the newest `## Round N` block must carry the field `**Planned (round N+1):**` with non-empty content (prose mention is not the field). At ad5942 the newest block is Round 44 (which has `**Planned (round 45):**` at `SCORECARD.md` line 2145). When the round-45 block is added it must declare the round-46 planned FIELD, and its heading must be `## Round 45` (a wrong round number appends a `BLOCK_ROUND_MISMATCH` m12 hit, `measure.py:520-522`).
- m13 (`measure.py:215-234`): the newest standing row's backticked counting command must contain `grep` and the census-valid `0,3` pattern, and the indent-mirror probe must stay load-bearing (column0 = valid − 1). The restated round-45 standing row must keep a backticked `grep -cE '^ {0,3}\| S[0-9]{3,} \|' corpus/SOURCES.md`-style command.
- self_pin: the round-44 `measure.py` blob must stay byte-identical to the freeze pin (`self_pin=1` confirmed at both revs); record edits must not touch `.ufo/evidence/round-44/calibration/measure.py`.

The round-44 lesson (`.ufo/evidence/round-44/after/...` / `corpus/lessons/round-44.md`) documents the identical class: its first landing `83beaf9` had `m6=1 standing=114 actual=115` and was fixed by appending a new census-valid standing row and re-running the predicate unchanged — the same fix shape applies here.

## Evidence / risks

Evidence: counter source code cited above; reproduction commands and outputs pasted verbatim; commit stats via `git show --stat`. No tools installed (no pacman/uv/npx action needed; `python3`/`git`/`grep` pre-existing).

Risks:
- If the round lands without the m6 restatement (117 rows at round 45), the deciding-run round-44 counter stays total=1 and the round violates its own no_harm clause — the one currently-open no-harm defect.
- The `staged S202`-space-form pitfall is the easiest way to trip m7 while writing the round-45 lesson/scorecard around the id map.
- The planned-round-46 field and the `## Round 45` heading must both be present in the new block to keep m12=0.
