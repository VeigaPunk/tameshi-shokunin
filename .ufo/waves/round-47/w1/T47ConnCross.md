# T47ConnCross — cross-claim / cross-source pattern findings (round 47, seat T47ConnCross)

Scope: read-only pattern-finding across C1 (calibration), C2 (operability), C3 (coverage) and the
four frozen C3 sources. Every inference is labelled `[I]`; every observation is `[O]`. Nothing in
the lane was edited except this report; all measurements ran in `/tmp/tameshi-r47-T47ConnCross/`
against the frozen commit `9acfbe21435e1976636a276448dee1d5e7155915` and the content revision
`8b0e15d25ea598c0bf908d183fb410a085bf3a18`.

Tooling: no installs were needed (python3 3.14, git, xfs `df`/`findmnt` were all present). No
pacman/uv/npm transaction was performed.

## Axes named

- **C1 / calibration** — the standing SCORECARD rows must state each statement's live-host
  `(line, exit, tool sha256)` **and** a `deps` clause equal to the dependence set observed by
  comparing `(line, exit)` across six profiles.
- **C2 / operability** — v2 counters must kill ≥150 of 183 real pool mutants, one selftest run each.
- **C3 / coverage** — three registry rows + three re-grounded, indexed knowledge entries citing them.

## Source-to-claim map used below

| id | document | what it states (as used here) |
|---|---|---|
| S261 | arxiv 2302.09330 (staged S155) | flaky-test prediction is possible from recorded history — outcomes + durations, no extra reruns |
| S262 | Lam et al. camera-ready (staged S158) | ≤5 reruns classify ≥82% of failures correctly; the cheaper axis is **order diversity**, not more repeats of one order |
| S263 | arxiv 2607.09345 (staged S206) | flakiness is **not a static property** of test code; benchmarks reward shortcuts and inflate F1 |
| S264 | Semantic Scholar DOI 10.1109/ICST60714.2024.00037 (staged S207) | a rerun costs 0.02 cents; a red pipeline costs $5.67 of human investigation |
| S258 (held, round-46) | arxiv 2504.16777 | flaky failures cluster; shared root cause ⇒ several observations are fewer independent observations |
| S156 (held) | pitest.org/faq | a mutant may be **timed out on one run, but killed or surviving on another** — verdict classes are run-dependent |

---

## Pattern 1 — C1's dependence observation is one run per profile, and the lane's own tool says N≥3
before it will believe agreement

**Claim it would change:** C1 (calibration).

**Evidence pointers.**
- `.ufo/evidence/round-47/calibration/measure.py:296-300` — one `observe()` call per
  `(statement, profile)`; `futs[(s['id'], prof)] = pool.submit(observe, s, prof, ctxs[prof])`, one
  submission each ⇒ **132 runs for 22 statements × 6 profiles**, N=1 per cell.
- `corpus/knowledge/repeated-control-precondition.md:36-39` and `tools/repeat-control.py:262`
  (`--runs must be >= 3`) — the lane's own repeated-control gate takes **N≥3** before it will say
  `controls_match`; the floor is lane policy, explicitly *not* source-prescribed
  (`repeated-control-precondition.md:39`).
- `corpus/README.md:80` (F3 row) — the standing frontier move is "one control per sweep → N ≥ 3
  byte-identical controls, **or a named mismatch**".
- S262 supplies the *published* budget for the classification task: "≤ 5 reruns … still check
  correctly ≥ 82 % of the time" (`lam-2020-reruns.txt`, quoted in
  `.ufo/evidence/round-47/assimilation/package/flaky-aware-verdict-evidence.md:13-16`).
- S156 (held lane row) supplies the reason a single run is not enough: "a mutant may be detected
  as timed out on one run, but killed or surviving on another".

**What the counter does that the F3 row forbids.** A `deps` clause is a *difference* between two
single runs. If the statement's command is not deterministic, a one-run difference is
indistinguishable from a real dependence. The lane already owns the instrument
(`tools/repeat-control.py`), and the F3 row's own escape hatch is "**or a named mismatch**" — C1
has no channel to name a mismatch: `deps` is a set of names (`measure.py:51`,
`CLAIM_CAP` at `:36`), so an unstable cell must be misreported as either a dependence or as `none`.

**One-command test** (the lane's own N≥3 instrument, against the flaky statement under a clean
profile — no lane write; `--out` under `/tmp`):

```bash
env -i PATH=/usr/bin:/bin HOME=/tmp/t47-home TMPDIR=/tmp/t47-tmp LANG=C LC_ALL=C TZ=UTC \
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/repeat-control.py \
  --runs 3 --out /tmp/t47-repeat-control -- python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/env-diff.py --selftest
```

Expected on this host: `REPEAT_COMPARE identical=yes runs=3` with `REPEAT_CONTROL: baseline_nonzero`
(exit 2 — the selftest exits 1 under the clean profile), i.e. the N≥3 channel reaches a *named*
class where C1 currently has only `deps`.

---

## Pattern 1b — DECISIVE: C1's `deps` clauses are not a function of the tree. Two of the 22 landed
rows already disagree with the counter, and the disagreement has a *filesystem* cause the contract
never mentions

**Claim it would change:** C1 (calibration). This is a live defect at the revision that carries the
records, not a hypothetical.

**Evidence pointers.**
- Landed `SCORECARD.md:2268-2289` now carries a `deps` clause on all 22 rows (`grep -c 'deps \`'`
  = 0 at the freeze `9acfbe2`, 22 at the content revision `8b0e15d`).
- `.ufo/evidence/round-47/control/emit-observed-pre-freeze.out` is the **counter's own emitted**
  dependency sets at the freeze (22 `EMIT_*` rows) — the authoritative observation.
- `.ufo/evidence/round-47/calibration/measure.py:301-315` compares `observed_deps` to `claim[1]`;
  a difference increments `depm` and prints `DEPS-MISMATCH`.
- `.ufo/evidence/round-47/deciding-run.sh` — the deciding run's work root is
  `WORK=${4:-/var/tmp/tameshi-r47-deciding}`.

**[O] Comparing the counter's emitted deps (freeze receipt) with the landed clauses: 20 of 22
agree, two do not.**

| statement | counter-emitted (freeze) | landed in SCORECARD | agree? |
|---|---|---|---|
| `hermetic env-differential probe` | `env,node` | `bwrap,node` | **NO** |
| `six-leg regression ledger` | `fleet-root,node` | `env,fleet-root,node` | **NO** |

**[O] And the counter already reports the mismatch, at the content revision.** From the L1's own
deciding receipt `.ufo/evidence/round-47/after/c1.stdout` (rev
`8b0e15d25ea598c0bf908d183fb410a085bf3a18`):

```
STATEMENT cap/six-leg regression ledger: claimed=REGRESSION: FAIL (cases=9 passed=7|1|a7d3f2dd7d47
  observed=REGRESSION: PASS (cases=9 passed=9|0|a7d3f2dd7d47 (exit=0) MISMATCH
  declared_deps=env,fleet-root,node observed_deps=fleet-root,node DEPS-MISMATCH
STATEMENT cap/hermetic env-differential probe: … declared_deps=bwrap,node observed_deps=bwrap,node DEPS-OK
C1_R47: … mismatches=1 unparsed=0 unobservable=0 dep_mismatch=1 unpinned=0 append_only=1 total=2
  rev=8b0e15d… C1_R47_PASS=false
```

**[O] I reproduced both mismatches independently**, and — this is the part that matters — the
*same tree at the same revision* produces **different** observed deps depending on where the
counter's scratch root lives:

| counter run | work root | `hermetic env-differential probe` observed deps | `six-leg regression ledger` observed deps |
|---|---|---|---|
| freeze `--only` probe A | `/tmp/tameshi-r47-T47ConnCross/c1a` | `env,node` | `fleet-root,node` |
| freeze `--only` probe B | `/tmp/tameshi-r47-T47ConnCross/c1b` | `bwrap,env,node` | `fleet-root,node` |
| content-rev probe | `/tmp/tameshi-r47-T47ConnCross/rev_b` | `env,node` | `fleet-root,node` |
| content-rev probe | `/var/tmp/t47-vt` | `bwrap,node` | `fleet-root,node` |

The deciding run uses `/var/tmp/tameshi-r47-deciding` (`deciding-run.sh`), which is why the landed
`bwrap,node` matches the deciding run and **not** the counter's own emitted `env,node`.

**[O] Root cause, isolated.** `tools/env-diff.py` runs its nine selftest cases through `bwrap`
(`tools/env-diff.py:57-95`), and `bwrap` needs `bash` on the `PATH` it inherits. C1's P1 profile
sets `PATH` to a **shim directory** (`measure.py:186-199`, `build_shim`) built under the counter's
scratch root. Isolated experiment:

| shim location | PATH | env-diff selftest |
|---|---|---|
| under `/tmp` | shim only | `2/9 pass`, exit 1 (7 cases FAIL) |
| under `/tmp` | shim **+ `/usr/bin`** | `9/9 pass`, exit 0 |
| under `/var/tmp` | shim only | `9/9 pass`, exit 0 |

**[I]** The shim's `bash` symlink lives under the scratch root; when that root is on `/tmp`, `bwrap`
cannot use it and the selftest degrades to `2/9`. So the P1 profile's outcome depends on the
**filesystem the scratch root happens to sit on**, and `/tmp` (xfs, `findmnt` → `xfs
/dev/nvme1n1p1`) and `/var/tmp` (the root filesystem) behave differently. The contract says
"comparing the statement's (line, exit) under the clean full profile P1" — it does not say *where
the scratch lives*, but the scratch location is part of the observation. **[I]** This is exactly the
S263 hazard the lane's own `r8-flakiness-not-static.md:29-34` names — *"the lane measures
environment sensitivity by comparing a gate's output under two profiles and classifying the
difference"* — except here the undeclared input is the counter's own scratch filesystem.

**[O] The second mismatch has a different, non-filesystem cause.** `six-leg regression ledger`'s
claimed value `REGRESSION: FAIL (cases=9 passed=7` is a **string from the tool's own mutation
fixture table**, not an observation: `tools/mutate-and-run.sh:2024-2026` lists
`'1 1 0 0 0 0 0 0 0:1:REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)'` and two siblings.
**[O]** The live command prints `REGRESSION: PASS (cases=9 passed=9)` in every run I made (3 direct
runs and 3 counter runs, at both revisions). **[I]** So the landed row states a value the command
does not print under the live host profile P0 — a **wrong value**, not merely a wrong deps clause —
and it is wrong in the specific way of quoting a fixture expectation instead of an observation.
**[O]** The landed `env` in that row's deps clause is likewise unobserved: `env` is emitted only
when P0 ≠ P1 (`measure.py:305-306`), and P0 == P1 == `REGRESSION: PASS (cases=9 passed=9|0` in every
observation I made. **[I]** The `env` label looks like a hand-assignment from "this command reads
the fleet" rather than a comparison the counter performed.

**One-command test** (read-only `--only` probes; the deciding probe is a partial probe by
contract):

```bash
# (a) the deciding-revision probe, from /tmp — reproduces the mismatches
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-47/calibration/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 8b0e15d25ea598c0bf908d183fb410a085bf3a18 \
  --base 0b5b7cd2b2c15d23086e811a0f0348d84261277b \
  --work /tmp/t47-c1-probe \
  --only 'hermetic env-differential probe,six-leg regression ledger'

# (b) the same probe from /var/tmp — the deciding run's filesystem
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-47/calibration/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 8b0e15d25ea598c0bf908d183fb410a085bf3a18 \
  --base 0b5b7cd2b2c15d23086e811a0f0348d84261277b \
  --work /var/tmp/t47-c1-probe \
  --only 'hermetic env-differential probe,six-leg regression ledger'
```

Expected: (a) `hermetic env-differential probe … observed_deps=env,node` and
`six-leg regression ledger … MISMATCH`; (b) `observed_deps=bwrap,node` — **the same tree, the same
revision, two different answers**, differing only in the scratch filesystem.

**Risk if ignored (second-order):** C1's standing `deps` clauses are not reproducible by a third
party, and the deciding run's answer depends on an undeclared host input. A row that says
`bwrap,node` is true on `/var/tmp` and false on `/tmp`; a row that says `env,node` is the opposite.
The "standing self-assessment" the claim is about is therefore a snapshot of the deciding
machine's scratch filesystem, not of the tree.

---

## Pattern 2 — C2's 183 mutants are 17 functions; the independence concern transfers, and it is a
denominator-semantics defect, not a determinism defect

**Claim it would change:** C2 (operability).

**Evidence pointers.**
- `.ufo/evidence/round-47/hardening/pool.json` — group sizes 111 (freshness) + 86 (coverage); the
  `id` field is `<qualname>:<kind>:<n>`, so the pool is **per-function-site** by construction.
  Distinct functions: **5** in coverage (`entry_ok` 31, `measure` 25, `gt_rows` 21, `Tree.read` 5,
  `Tree.ls` 4) and **12** in freshness (`measure` 23, `grade` 21, `live` 14, `review_sets` 12,
  `parse_rows` 11, `check` 9, `git` 5, `population` 4, `words` 4, `extract` 3, `wave_seats` 3,
  `load_snapshot` 2) — **17 functions for 183 mutants**.
- `.ufo/evidence/round-47/before/pool-base.stdout` (base run, `--targets base`) —
  `killed=122 survived=49 crashed=12`. Broken out by function (measured from that stdout):
  `freshness/live` 0 killed / 13 survived, `freshness/check` 0 killed / 9 survived,
  `freshness/parse_rows` 5 killed / 4 survived / 2 crashed, `coverage/gt_rows` 18 killed / 3 crashed,
  `coverage/entry_ok` 23 killed / 5 survived / 3 crashed.
- `corpus/knowledge/r6-flaky-failures-cluster.md:38-39` — *"Survivor lists are not independent
  observations … several of them are fewer independent observations than their number"* and
  *"the classification should carry cluster membership beside each per-survivor verdict."*

**The independence concern does transfer — and the measured shape is stronger than the item's
framing.** The item asks whether C2's pool is subject to "mutants of one function are not
independent observations". **[O] Yes, structurally:** 183 mutants come from 17 rule functions, so
183 is not 183 independent observations — it is 17, weighted by sites per function. The gap C2
must close is 122 → ≥150, i.e. **28 more kills**, but those 28 are reachable from a *small* number
of functions: `freshness/live` (13 survivors) + `freshness/check` (9 survivors) hold **22 of the 49
survivors**, and `freshness/parse_rows` holds 6 more (4 survived + 2 crashed). **[I]** A v2 counter
that hardens `live` and `check` can plausibly supply 22 of the 28 needed kills from **two
functions**, and the whole 28 from **four**. A single `killed=150 of 183` number therefore
overstates the breadth of independent evidence by roughly an order of magnitude — exactly the r6
"one finding counted N times" shape.

**But the r6 cluster finding does *not* make C2's mutants flaky**, and this is the part that
distinguishes C2 from C1. The mutants are deterministic single-site AST edits and the selftest is
a pure function of the source text — I verified the verdict class is **stable across repeated
runs**:

```bash
# 5 identical repetitions of 3 coverage mutants (killed / survived / killed)
for i in 1 2 3 4 5; do python3 .../hardening/pool.py --try <file> --group coverage \
  --ids 'entry_ok:cmp:0,measure:cmp:0,gt_rows:cmp:0'; done
# → 5/5 identical: gt_rows:cmp:0 killed | entry_ok:cmp:0 survived | measure:cmp:0 killed
# and 3/3 identical for the 8 coverage mutants that crash at base (all 'crashed')
```

**[I]** So C2's single-run-per-mutant design is *safe* on the flake axis, and the lane's own
`r8-flakiness-not-static.md:38-40` already bounds the transfer ("the snapshot reports flaky *test
failures* in 24 Java projects; it contains no data on mutation survivors"). The defect C2 inherits
is **denominator semantics, not determinism**: the pool's `real` count is a site count, and the
score_rule (`killed 122 → ≥150 of 183`) reads as if it were 183 observations.

**One-command test** (measures the concentration; no lane mutation):

```bash
python3 - <<'EOF'
import json, collections
d = json.load(open('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-47/hardening/pool.json'))
for g, lst in d['groups'].items():
    real = [m for m in lst if not m['neutral']]
    c = collections.Counter(m['id'].split(':')[0] for m in real)
    print(g, 'real mutants', len(real), 'distinct functions', len(c))
    print('  ', c.most_common())
EOF
```

Expected: `coverage real mutants 82 distinct functions 5`; `freshness real mutants 101 distinct
functions 12` — 183 mutants, 17 functions.

---

## Pattern 3 — C2's 12 crashed mutants are a *classification* defect; converting them to named
`FAIL`s is worth up to 12 of the 28 kills needed, from 6 functions

**Claim it would change:** C2 (operability).

**Evidence pointers.**
- `.ufo/evidence/round-47/before/pool-base.stdout` — `GROUP coverage: … crashed=8`,
  `GROUP freshness: … crashed=4`. The 12 crashing ids (measured from that stdout):
  `coverage/Tree.read:const:0`, `coverage/gt_rows:int:3`, `coverage/gt_rows:const:0`,
  `coverage/gt_rows:int:6`, `coverage/entry_ok:bool:3`, `coverage/entry_ok:int:2`,
  `coverage/entry_ok:int:6`, `coverage/measure:const:0`, `freshness/parse_rows:int:1`,
  `freshness/parse_rows:int:8`, `freshness/review_sets:bool:1`, `freshness/review_sets:not:2`.
- `.ufo/evidence/round-47/hardening/pool.py:171-183` — a mutant is `killed` only when the selftest
  exits nonzero **and** prints a line starting `FAIL `; a crash is explicitly *not* a kill
  (`crashed` is a separate bucket). So the 12 crashes are 12 mutants the pool currently scores as
  neither kill nor survivor.
- S262 (Lam et al.) and S264 (ICST-24) give the published budget and price for re-classifying
  failures: ≤5 reruns classify ≥82% correctly; a rerun costs 0.02 cents against $5.67 for a human
  investigating a red build (`r8-flaky-cost-baseline.md:19-24`).

**[O] The crashes are deterministic, not flaky** — the 8 coverage crashing ids returned `crashed`
on 3/3 repetitions (same ids, same result). **[I]** So each crash is a *stable* fact about that
mutant: the mutant breaks the counter's own selftest (a raised exception rather than a `FAIL `
line) instead of failing an assertion. **[I]** Repairing this is not a rerun-budget problem at all —
it is a **classification** problem: the v2 counter's selftest additions must turn "the selftest
blew up" into "the selftest named the failure". Since the pool's kill rule is `FAIL `-line-based
(`pool.py:171-183`), a v2 selftest that wraps each case in try/except and prints `FAIL <case>` on
exception would convert up to 12 crashes into kills at once — from 6 functions (`gt_rows`,
`entry_ok`, `Tree.read`, `measure`, `parse_rows`, `review_sets`), which is **12 of the 28 kills C2
needs**. Combined with Pattern 2, the 28-kill gap looks reachable from a handful of functions, not
from 28 independent findings.

**One-command test** (probes a crashing mutant against the base counter — read-only, `--try` writes
only to `/tmp`):

```bash
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-47/hardening/pool.py \
  --try <base-freshness-counter.py> --group freshness --ids 'parse_rows:int:1,review_sets:not:2'
```

Expected at base: `MUT freshness/parse_rows:int:1 crashed` and `MUT freshness/review_sets:not:2
crashed` — stable across repetitions.

---

## Pattern 4 — C3's own counter demands a *fresh* quote absent from the package copy; the three
snapshots satisfy it, but only by quoting a different sentence than the package paraphrases

**Claim it would change:** C3 (coverage).

**Evidence pointers.**
- `.ufo/evidence/round-47/coverage/measure.py:140-150` (`entry_ok`) — an entry must carry a
  located quote of 6..25 whitespace tokens found in the cited row's snapshot **and** at least one
  such located quote that does **not** occur in the committed package copy
  `.ufo/evidence/round-47/assimilation/package/<basename>`; otherwise
  `no quote fresh against the package copy`.
- `.ufo/evidence/round-47/coverage/measure.py:129-145` (`flaky_rows`) — a row counts only if its
  anchor cell names a snapshot present at REV with an 8+-hex sha256 prefix that recomputes over
  the snapshot bytes; the row's first URL must equal one of the three frozen `DOCS`.
- The snapshots exist and hash: `arxiv-2302.09330-abs.html`, `arxiv-2607.09345-abs.html`,
  `lam-2020-reruns.pdf` + `.txt`, `s2-icst24-cost-of-flaky.json` under
  `.ufo/evidence/round-47/coverage/sources/`.
- Sibling round-47 review (`T47RevProvince.md:449-453`, defects F1–F16) measured that the three
  package copies fail `entry_ok` on `no provenance trio` (leading blank line, multi-line
  `source:`, `verified-at` not on line 2) and on the fresh-quote test, and that two entries carry
  ids (`S205`, `S208`) that resolve to no lane row.

**[O]** The three C3 snapshots each contain located, 6..25-token, single-line sentences that are
**absent** from the corresponding package copy — the fresh-quote requirement is satisfiable from
the committed snapshots alone, without inventing text. Measured with the counter's own
`norm_text` + `fold`:

| row | verified fresh candidate (token count) | located | absent from pkg |
|---|---|---|---|
| S261 (`arxiv-2302.09330-abs.html`) | "Furthermore, our approach does not require additional reruns, since it gathers this data from existing test executions." (17 t) | yes | yes |
| S261 (alt) | "Non-deterministically behaving test cases cause developers to lose trust in their regression test suites and to eventually ignore failures." (19 t) | yes | yes |
| S263 (`arxiv-2607.09345-abs.html`) | "Flaky tests pass and fail on the same code version, weakening the signal of test results and disrupting continuous integration (CI) pipelines." (22 t) | yes | yes |
| S263 (alt) | "We argue that the field is studying the wrong problem:" (10 t) | yes | yes |
| S264 (`s2-icst24-cost-of-flaky.json`) | "However, it is yet unclear where and to what extent the costs of flaky tests manifest in industrial Continuous Integration (CI) development processes." (23 t) | yes | yes |

**[O] Correction to my own first reading.** I initially proposed shorter candidates
("prediction of flaky tests without such requirements …", "Flakiness is not a static property of
test code …", "Automatically rerunning a test costs 0.02 cents"). Measured against the counter's
own normalisation, **two of those three are already present in the package copy** (`fresh=False`),
i.e. they would have been refused by `entry_ok` with `no quote fresh against the package copy`.
The longer sentences above are the ones that pass. **[I]** The practical consequence: the
fresh-quote requirement is satisfiable, but only by quoting a *different* sentence from the one the
package entry paraphrases — the re-grounding is not a copy-edit, it is a re-selection. And S262's
`lam-2020-reruns.txt` is a two-column `pdftotext` interleave: sentence-slicing it yields 314
"sentences" that are mostly cross-column artefacts, so the Lam row's fresh quote needs a
hand-picked contiguous line, not a mechanical split (the sibling review logged the same interleave
at `T47RevProvince.md:449`, defect F3).

**[I] A second, cross-claim observation on C3's counter.** The DOCS tuple
(`measure.py:47-51`) requires the Semantic Scholar URL with `%2C`-encoded fields, while
`URL_RE = re.compile(r'https?://[^\s;,)]+')` (`measure.py:54`) **truncates at a literal comma** — so
a row whose URL contains unencoded commas is never matched (`doc_key` of the truncated prefix ≠
the DOCS key). That is a one-cell defect in the counter, and it is the kind of defect the
"coverage" axis is supposed to catch, not be caught by.

**One-command test** (read-only; prints each candidate's token count, whether it is located in the
snapshot, and whether it is absent from the package copy — using the counter's own
`norm_text`/`fold` so the verdict matches `entry_ok`):

```bash
python3 - <<'EOF'
import re, html, unicodedata, pathlib
SRC = pathlib.Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-47/coverage/sources')
PKG = pathlib.Path('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-47/assimilation/package')
def fold(t):
    t = unicodedata.normalize('NFKC', t)
    for a,b in ((u'‘',"'"),(u'’',"'"),(u'“','"'),(u'”','"'),(u'–','-'),(u'—','-'),(u'­',''),(u' ',' '),(u'','')):
        t=t.replace(a,b)
    return ' '.join(t.split())
def norm(raw):
    t=raw.decode('utf-8','replace')
    if re.search(r'<(html|body|div|p|head)\b', t, re.I):
        t=re.sub(r'(?is)<(script|style)\b.*?</\1\s*>',' ',t)
        t=re.sub(r'(?s)<[^>]*>',' ',t); t=html.unescape(t)
    return fold(t)
checks=[
 ('S261','arxiv-2302.09330-abs.html','flaky-aware-verdict-evidence.md',
  'Furthermore, our approach does not require additional reruns, since it gathers this data from existing test executions.'),
 ('S263','arxiv-2607.09345-abs.html','r8-flakiness-not-static.md',
  'Flaky tests pass and fail on the same code version, weakening the signal of test results and disrupting continuous integration (CI) pipelines.'),
 ('S264','s2-icst24-cost-of-flaky.json','r8-flaky-cost-baseline.md',
  'However, it is yet unclear where and to what extent the costs of flaky tests manifest in industrial Continuous Integration (CI) development processes.'),
]
for rid,snap,pkg,q in checks:
    st=norm((SRC/snap).read_bytes()); pt=fold((PKG/pkg).read_text(errors='replace'))
    print('%-5s tok=%-3d located=%-5s fresh=%-5s | %s' % (rid, len(q.split()), q in st, q not in pt, q[:80]))
EOF
```

Expected: `S261 tok=17 located=True fresh=True`; `S263 tok=22 located=True fresh=True`;
`S264 tok=23 located=True fresh=True`.

---

## Pattern 5 — Cross-claim synthesis: the lane's own F3 row already names the fix for all three
claims ("N ≥ 3 byte-identical controls, **or a named mismatch**"), and C1 is the only claim that
spends an unbounded, un-named budget where the evidence is weakest

**Claim it would change:** C1 primarily; C2 and C3 secondarily (as constraints, not targets).

**Evidence pointers.**
- S261: prediction uses "the tests' outcomes and durations, as well as basic information about the
  code evolution" and "does not require additional reruns, since it gathers this data from existing
  test executions" — **history is cheaper than reruns**.
- S262: "run tests in a test suite instead of in isolation, and run tests in different orders with
  fewer times each, rather than fewer orders with more times each" — the cheap axis is **diversity
  of conditions**, not more repetitions of one condition.
- S264: rerun ≈ 0.02 cents; a red pipeline ≈ $5.67 of human investigation — the rerun is ~280×*
  cheaper than the manual branch (*the package's own "~280×" arithmetic is wrong: 5.67 / 0.0002 =
  28 350; the sibling review logged this at `T47ScoutHeld.md:33`; I use the ratio only
  qualitatively).
- `corpus/README.md:80` (F3 row) already encodes the shape: "one control per sweep → N ≥ 3
  byte-identical controls, **or a named mismatch**".
- `corpus/knowledge/repeated-control-precondition.md:31-39` — the lane's own reading: stream
  agreement is stronger than pass/fail stability and still weaker than determinism; retries do not
  repair; the floor of 3 is lane policy, not a sourced threshold.

**[I] The synthesis.** C1's six profiles are already an *order-diversity* design (six conditions,
one run each) — exactly the axis S262 says is cheap. What is missing is (a) the **bounded
repetition** S261/S262 justify and the lane's own N≥3 policy demands, applied to the cells where
the answer matters, and (b) a **channel to name a mismatch** so an unstable cell does not have to
be misreported as a dependence or as `none`. The F3 row's own alternative to "N≥3 byte-identical"
is "**or a named mismatch**", and C1's counter has no way to express one.

**[I] Why this is cross-claim, not C1-only.** The same "one observation is not a determinism
claim" reasoning that Pattern 2 applies to C2's 183-vs-17 denominator applies to C1's 132
single-run cells — but with the **opposite** remedy, because C1's cells are *not* deterministic
functions of the tree (Pattern 1b measured a flip: same tree, same revision, two answers) while
C2's mutants *are* (Pattern 2 measured stability). S262's "≤5 reruns classify ≥82% of the time"
then sets a concrete, cheap, bounded budget for C1's unstable cells; S264 prices those repeats as
negligible next to the price of a wrong standing row; and S261 says the cheapest input is the
history the lane already keeps, not new runs.

**One-command test** (the lane's own N≥3 instrument against the flaky statement under the clean
profile — no lane write):

```bash
env -i PATH=/usr/bin:/bin HOME=/tmp/t47-home TMPDIR=/tmp/t47-tmp LANG=C LC_ALL=C TZ=UTC \
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/repeat-control.py \
  --runs 3 --out /tmp/t47-repeat-control -- python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/env-diff.py --selftest
```

Expected on this host: `REPEAT_COMPARE identical=yes runs=3` with `REPEAT_CONTROL: baseline_nonzero`
(exit 2), i.e. the N≥3 channel reaches a *named* class where C1 currently has only `deps`.

---

## Contradictions stated, not smoothed

1. **C1's `deps` clause vs the lane's F3 policy.** The contract asks for "a `deps` clause equal to
   the dependence set observed by comparing the statement's (line, exit) under the clean full
   profile P1 with P0 …" — a comparison of single runs, on a scratch root whose **filesystem** is
   an undeclared input (Pattern 1b). The lane's own F3 row requires N≥3 or a named mismatch. Both
   cannot hold for the two rows that already mismatch.
2. **The counter's own emitted deps vs the landed clauses.** `emit-observed-pre-freeze.out` says
   `env,node` and `fleet-root,node`; `SCORECARD.md` says `bwrap,node` and
   `env,fleet-root,node`. **[I]** The landed clauses are not the counter's output. One of them
   (`six-leg regression ledger`) quotes a **mutation-fixture string** from
   `tools/mutate-and-run.sh:2024-2026` rather than an observation — that is a value error, not
   only a deps error.
3. **S262's "≥82% of failures" vs S263's "flakiness is not a static property".** A bounded rerun
   budget is published for *classifying failures*; S263 argues the classifier's input (static
   properties of test code) is often insufficient. For C1's dependence set the two do not conflict
   — the dependence set is an environment differential, not a static code property — but the same
   reasoning applied to a *code*-property classifier would refuse the whole instrument. The
   lane's own `r8-flakiness-not-static.md:29-34` draws exactly this line, and it is the line C1
   sits on.
4. **S264's "~280×" arithmetic.** 5.67 / 0.0002 = 28 350, not 280. The package entry's figure is
   wrong; I use the ratio only qualitatively.
5. **S262's cheap-axis advice vs the lane's N≥3 floor.** S262 says prefer *order diversity* with
   fewer repeats; the lane's F3 policy says N≥3 *byte-identical* controls. Different axes, both
   legitimate: C1 already buys order diversity (6 profiles), so what it lacks is the repeat floor
   and the mismatch channel, not the diversity.
6. **C2's denominator vs C2's score rule.** The contract's comparable measure is "killed 122 →
   ≥150 of 183"; 183 is a **site** count over **17** functions (Pattern 2). The number is
   well-defined and the contract is frozen, so this is a reporting obligation, not a counter
   defect: the receipt should state the per-function breakdown beside the total, as
   `corpus/knowledge/r6-flaky-failures-cluster.md:38` already asks ("the classification should
   carry cluster membership beside each per-survivor verdict").

## What I did not do (scope)

- No lane file was edited except this report; the frozen contract, counters, statements list, pool
  and snapshots were read only.
- No verdict was produced: the C1 counter was run only as `--only` probes and against the frozen
  and content revisions into scratch work dirs; the C2 pool was exercised only through `--try`; the
  C3 counter was not run.
- I did not judge, admit, edit, integrate or ship any runtime, and I did not run a campaign tool in
  the read-only package.

## Scratch inventory (all under `/tmp/tameshi-r47-T47ConnCross/`)

`measure-frozen.py`, `statements-frozen.json` (sha256
`924102dfbc6135a7d9dabef7b8b2e681a5ce4c42ca72a031ea1f8d5ab9fb2e56` = the contract's pin),
`fr-base.py` / `cov-base.py` (round-46 counters at the freeze), `full_a.txt` (22-statement `--only`
probe at the freeze: `C1_R47_PARTIAL … total=22`), `rc_p1/` (repeat-control receipt),
`p1like/` (P1-shaped clean environment), `t47-shimtest/` (shim-location experiment).
