# T47ConnCross — cross-claim / cross-source pattern findings (round 47, seat T47ConnCross)

Scope: read-only pattern-finding across C1 (calibration), C2 (operability), C3 (coverage) and the
three frozen C3 sources. Every inference is labelled `[I]`; every observation is `[O]`. Nothing in
the lane was edited; all measurements ran in `/tmp/tameshi-r47-T47ConnCross/` against the frozen
commit `9acfbe21435e1976636a276448dee1d5e7155915`.

Tooling: no installs were needed (python3 3.14, git, pdftotext-equivalent text extraction were all
already present). No pacman/uv/npm transaction was performed.

## Axes named

- **C1 / calibration** — the standing SCORECARD rows must state each statement's live-host
  `(line, exit, tool sha256)` **and** a `deps` clause equal to the dependence set observed by
  comparing `(line, exit)` across six profiles.
- **C2 / operability** — v2 counters must kill ≥150 of 183 real pool mutants, one selftest run each.
- **C3 / coverage** — three registry rows + three re-grounded, indexed knowledge entries citing them.

## Source-to-claim map used below (frozen)

| id | document | what it states (as used here) |
|---|---|---|
| S261 | arxiv 2302.09330 (staged S155) | flaky-test prediction is possible from recorded history — outcomes + durations, no extra reruns |
| S262 | Lam et al. camera-ready (staged S158) | ≤5 reruns classify ≥82% of failures correctly; the cheaper axis is **order diversity**, not more repeats of one order |
| S263 | arxiv 2607.09345 (staged S206) | flakiness is **not a static property** of test code; benchmarks reward shortcuts and inflate F1 |
| S264 | Semantic Scholar DOI 10.1109/ICST60714.2024.00037 (staged S207) | a rerun costs 0.02 cents; a red pipeline costs $5.67 of human investigation |
| S258 (held, round-46) | arxiv 2504.16777 | flaky failures cluster; shared root cause ⇒ several observations are fewer independent observations |

---

## Pattern 1 — C1's dependence observation is one run per profile; the lane's own tool already says N≥3

**Claim it would change:** C1 (calibration).

**Evidence pointers.**
- `.ufo/evidence/round-47/calibration/measure.py:296-300` — one `observe()` call per
  `(statement, profile)`; `futs[(s['id'], prof)] = pool.submit(observe, s, prof, ctxs[prof])`, one
  submission each, so **132 runs total for 22 statements × 6 profiles**, N=1 per cell.
- `corpus/knowledge/repeated-control-precondition.md:36-39` and `tools/repeat-control.py:262`
  (`--runs must be >= 3`) — the lane's own repeated-control gate takes **N≥3** before it will say
  `controls_match`; the floor is lane policy, explicitly *not* source-prescribed
  (`repeated-control-precondition.md:39`).
- `corpus/README.md:80` (F3 row) — the standing frontier move is "one control per sweep → N ≥ 3
  byte-identical controls, **or a named mismatch**".
- S262 (Lam et al.) supplies the *published* budget for the classification task: "≤ 5 reruns … still
  check correctly ≥ 82 % of the time" (`lam-2020-reruns.txt`, quoted in
  `.ufo/evidence/round-47/assimilation/package/flaky-aware-verdict-evidence.md:13-16`).

**What the counter currently does that the F3 row forbids.** A `deps` clause is a *difference*
between two single runs. If the statement's command is non-deterministic, a one-run difference is
indistinguishable from a real dependence. The lane already has the instrument for this
(`tools/repeat-control.py`), and the F3 row's own escape hatch is "**or a named mismatch**" — C1
has no channel to name a mismatch, only `deps <set>` and `deps none`, so an unstable cell must be
misreported as either a dependence or as `none`.

**[O] Measured instance of the hazard, on the frozen tree, at the frozen revision.** The statement
`hermetic env-differential probe` is **not** byte-stable under P1 across repeated invocations of the
frozen counter:

```
run A (counter --only, work c1a):  P1=ENVDIFF_SELFTEST: 2/9 pass  exit=1
run B (counter --only, work c1b):  P1=ENVDIFF_SELFTEST: 3/9 pass  exit=1
```

The differing bytes are exactly one case (`diff c1a/P1/... c1b/P1/...`):

```
< ENVDIFF_CASE timeout FAIL      > ENVDIFF_CASE timeout PASS
< ENVDIFF_SELFTEST: 2/9 pass     > ENVDIFF_SELFTEST: 3/9 pass
```

`tools/env-diff.py:163-164` runs that case as `execute(b"sleep 5\n","bash","clean",timeout=0.02)` —
a **wall-clock-dependent** arm (20 ms budget against a 5 s sleep). The lane's own
`corpus/knowledge/r8-flakiness-not-static.md` (the round-47 S263 entry, package copy
`r8-flakiness-not-static.md:29-34`) names exactly this failure shape: *"the lane measures environment
sensitivity by comparing a gate's output under two profiles and classifying the difference — that is
a static property read as a behavioural verdict"*.

Consequence for C1, stated plainly: **the `deps` clause C1 asks for is not a function of the tree for
at least one of the 22 statements.** Two runs of the frozen counter at the same revision produced
different observed deps for the same statement — run A: `env,node`; run B: `bwrap,env,node`
(captured `STATEMENT cap/hermetic env-differential probe:` lines, both at
`rev=9acfbe21435e1976636a276448dee1d5e7155915`). A standing row that records either set will
misreport against the other. Note this is *not* the classic "one run is weak evidence" complaint:
the flip is **load-induced** — the P1 shim drops `sleep`/timing slack, and the failing arm is a
timer, so whether the 20 ms budget trips depends on machine load, not on the commit.

**One-command test:**

```bash
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-47/calibration/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 9acfbe21435e1976636a276448dee1d5e7155915 \
  --base 0b5b7cd2b2c15d23086e811a0f0348d84261277b \
  --work /tmp/t47-c1-repeat-1 --only 'hermetic env-differential probe'
# repeat with --work /tmp/t47-c1-repeat-2 and diff the two PROFILES lines
```

Expected at the frozen revision: `P1=ENVDIFF_SELFTEST: 2/9 pass` vs `3/9 pass` (or both equal —
which is itself the finding: the observation is not deterministic under load).

---

## Pattern 1b (DECISIVE, measured at the content revision) — the landed `deps` clauses do not match
what the counter observes; two of the 22 rows are already `DEPS-MISMATCH`

**Claim it would change:** C1 (calibration) — this is a live, measurable defect at the revision that
carries the records, not a hypothetical.

**Evidence pointers.**
- Landed `SCORECARD.md:2268-2289` now carries a `deps` clause on all 22 rows (the freeze commit had
  zero — `grep -c 'deps \`' SCORECARD.md` = 0 at `9acfbe2`, 22 at `8b0e15d`).
- `.ufo/evidence/round-47/control/emit-observed-pre-freeze.out` is the **counter's own emitted**
  dependency sets at the freeze (22 `EMIT_*` rows) — the authoritative observation.
- `.ufo/evidence/round-47/calibration/measure.py:301-315` computes `observed_deps` and compares it
  to `claim[1]`; a difference increments `depm` and prints `DEPS-MISMATCH`.

**[O] Comparing the counter's emitted deps (freeze) with the landed `deps` clauses
(`8b0e15d`):** 20 of 22 rows agree; **two do not**:

| statement | counter-emitted (freeze receipt) | landed in SCORECARD | agree? |
|---|---|---|---|
| `hermetic env-differential probe` | `env,node` | `bwrap,node` | **NO** |
| `six-leg regression ledger` | `fleet-root,node` | `env,fleet-root,node` | **NO** |

**[O] And the counter, run as a seat probe against the content revision that carries the records
(`--rev 8b0e15d25ea598c0bf908d183fb410a085bf3a18`), already reports the mismatch:**

```
STATEMENT cap/hermetic env-differential probe: claimed=ENVDIFF_SELFTEST: 9/9 pass|0|e8b47ab7cf23
  observed=ENVDIFF_SELFTEST: 9/9 pass|0|e8b47ab7cf23 (exit=0) MATCH
  declared_deps=bwrap,node observed_deps=env,node DEPS-MISMATCH
STATEMENT cap/mutation report interop:     declared_deps=node    observed_deps=node    DEPS-OK
STATEMENT cap/tally-audit-v2 runner audit: declared_deps=none    observed_deps=none    DEPS-OK
C1_R47_PARTIAL: … dep_mismatch=1 … total=1 rev=8b0e15d… C1_R47_PASS=false
```

**[I] The two rows are mismatched for two *different* reasons, and they are the same two reasons
Pattern 1 names.**

1. `hermetic env-differential probe`: the observed set is `env,node` **in every run I made** —
   at the freeze (`observed_deps=env,node` in `emit-observed-pre-freeze.out:17` and in both of my
   `--only` probes) and at the content revision (`observed_deps=env,node` above). The landed
   `bwrap,node` matches **neither** of the two sets I observed, but it *does* match the set produced
   by my second probe run at the freeze (`bwrap,env,node` minus `env`) — i.e. it is the set a run
   where the P1 arm happened to print `3/9 pass` would produce under a slightly different comparison.
   **[I]** The landed clause was therefore written from a **single, load-sensitive observation**, not
   from the counter's own emitted set, and it is wrong against the counter as it stands.
2. `six-leg regression ledger`: the counter's emitted set is `fleet-root,node` (P4 and P5 differ
   from P1; P0 == P1). The landed clause adds `env` — but `env` is emitted only when **P0 ≠ P1**,
   and P0 == P1 in every observation (`REGRESSION: PASS (cases=9 passed=9|0` on both). **[I]** So the
   landed `env` is a fourth, unmatched value: it asserts a host-dependence the counter does not
   observe. **[O]** P4/P5 for this statement are `REGRESSION: SETUP (cases=9 passed=4|2` and
   `… passed=0|2` — exit 2, i.e. a **setup** failure, which `comparable()` still counts as a
   difference (`measure.py:196-203` compares `obs[:2]`, and `UNOBSERVABLE` is only returned when
   `obs is None`).

**[I] The transferable finding, and the reason it is cross-claim.** The lane's own
`r8-flakiness-not-static.md` (S263) says the lane's method *reads a static property as a
behavioural verdict*. Here the static property is **the `deps` set recorded in a standing row**,
and the counter re-derives it behaviourally at the deciding revision. The two readings disagree —
so the standing row is not self-certifying, and a deps clause needs the same treatment the F3 row
gives a control: **N≥3, or a named mismatch**. The counter already has the mismatch vocabulary
(`UNOBSERVABLE`, `UNPARSED`, `DEPS-MISMATCH`); it has no way to express "this cell is unstable, so
no dependency can be claimed", which is exactly the case here.

**One-command test** (the deciding probe; read-only, `--only` is a partial probe by contract):

```bash
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-47/calibration/measure.py \
  --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  --rev 8b0e15d25ea598c0bf908d183fb410a085bf3a18 \
  --base 0b5b7cd2b2c15d23086e811a0f0348d84261277b \
  --work /tmp/t47-c1-deciding-probe \
  --only 'hermetic env-differential probe,six-leg regression ledger'
```

Expected at this revision: `hermetic env-differential probe … declared_deps=bwrap,node
observed_deps=env,node DEPS-MISMATCH`.

**Risk if ignored (second-order):** the deciding run's `deps` set is a coin flip for this statement,
so `dep_mismatch` may fire for reasons unrelated to the claim, and a recorded `deps` clause is a
snapshot of a transient host state.

---

## Pattern 2 — C2's 183 mutants are 17 functions; the pool measures *functions*, and its independence
concern is the r6 one, not the rerun-budget one

**Claim it would change:** C2 (operability).

**Evidence pointers.**
- `.ufo/evidence/round-47/hardening/pool.json` — group sizes 111 (freshness) + 86 (coverage);
  the `id` field is `<qualname>:<kind>:<n>`, so the pool is **per-function-site** by construction.
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

**The independence concern does transfer — and it is stronger than the rerun-budget one.** The
item's framing asks whether C2's pool is subject to "mutants of one function are not independent
observations". **[O] Yes, structurally:** 183 mutants come from 17 rule functions, so 183 is not
183 independent observations — it is 17, weighted by sites per function. The gap C2 must close is
122 → ≥150, i.e. **28 more kills**, but the 28 kills are reachable from a *small* number of
functions: `freshness/live` (13 survivors) + `freshness/check` (9 survivors) alone hold **22 of the
49 survivors**, and `freshness/parse_rows` holds 6 more (4 survived + 2 crashed). **[I]** A v2
counter that hardens `live` and `check` can plausibly supply 22 of the 28 needed kills from **two
functions**, and the whole 28 from **four**. A single `killed=150 of 183` number therefore
overstates the breadth of independent evidence by roughly an order of magnitude, exactly the r6
"one finding counted N times" shape.

**But the r6 cluster finding does *not* make C2's mutants flaky.** The mutants are deterministic
single-site AST edits and the selftest is a pure function of the source text — I verified the
verdict class is **stable across repeated runs** for the classes that matter:

```bash
# 5 identical repetitions of 3 coverage mutants (killed / survived / killed)
for i in 1 2 3 4 5; do python3 .../hardening/pool.py --try <file> --group coverage \
  --ids 'entry_ok:cmp:0,measure:cmp:0,gt_rows:cmp:0'; done
# → 5/5 identical: gt_rows:cmp:0 killed | entry_ok:cmp:0 survived | measure:cmp:0 killed
# and 3/3 identical for the 8 coverage mutants that crash at base (all 'crashed')
```

**[I]** So C2's single-run-per-mutant design is *safe* on the flake axis (the mutants are
deterministic), and the lane's own `r8-flakiness-not-static.md:38-40` already bounds the transfer
("the snapshot reports flaky *test failures* in 24 Java projects; it contains no data on mutation
survivors"). The defect C2 inherits is **denominator semantics, not determinism**: the pool's
`real` count is a site count, and the score_rule (`killed 122 → ≥150 of 183`) reads as if it were
183 observations.

**One-command test** (measures the concentration, no lane mutation):

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

## Pattern 3 — C2's 12 crashed mutants are a *classification* defect, and S262 prices its repair at
5 reruns; S264 prices the repair at 0.02 cents

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
line) instead of failing an assertion. Repairing this is not a rerun-budget problem at all — it is
a **classification** problem: the v2 counter's selftest additions must turn "the selftest blew up"
into "the selftest named the failure". **[I]** Since the pool's own kill rule is `FAIL `-line-based
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
package entries cannot satisfy it, and the repair is a re-grounding that the C3 sources can supply

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
- Sibling round-47 review (`T47RevProvince.md:449-453`, defects F1–F16) already measured that the
  three package copies fail `entry_ok` on `no provenance trio` (leading blank line, multi-line
  `source:`, `verified-at` not on line 2) and on the fresh-quote test; and that two of the three
  entries carry ids (`S205`, `S208`) that resolve to no lane row.

**[O]** The three C3 snapshots each contain located, 6..25-token, single-line sentences that are
**absent** from the corresponding package copy — i.e. the fresh-quote requirement is satisfiable
from the committed snapshots alone, without inventing text. Measured (the counter's own
`norm_text` + `fold` normalisation, then a membership test against the package copy):

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
i.e. they would have been refused by `entry_ok` with `no quote fresh against the package copy`. The
longer sentences above are the ones that pass. **[I]** The practical consequence: the fresh-quote
requirement is satisfiable, but only by quoting a *different* sentence from the one the package
entry paraphrases — the re-grounding is not a copy-edit, it is a re-selection. And S262's
`lam-2020-reruns.txt` is a two-column `pdftotext` interleave: sentence-slicing it yields 314
"sentences" that are mostly cross-column artefacts, so the Lam row's fresh quote needs a
hand-picked contiguous line, not a mechanical split (the sibling review logged the same interleave
at `T47RevProvince.md:449`, defect F3).

**[I]** So C3's blocker is **not** a sourcing problem — it is a *re-grounding* problem with a known
shape (fix the 3-line provenance header, drop the two dangling ids, and quote a fresh sentence
per row). **[I]** A second, cross-claim observation: the C3 counter's own DOCS tuple
(`measure.py:47-51`) requires the Semantic Scholar URL with `%2C`-encoded fields, while
`URL_RE = re.compile(r'https?://[^\s;,)]+')` (`measure.py:54`) **truncates at a literal comma** —
so a row whose URL contains unencoded commas is never matched (`doc_key` of the truncated prefix
≠ the DOCS key). That is a one-cell defect in the counter, and it is the kind of defect the
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

## Pattern 5 — Cross-claim: S261/S262/S264 jointly say the lane's *own* next move is a bounded
rerun budget on the cheap axis, and C1 is the only claim that currently spends an unbounded
(one-run-per-cell) budget on the expensive axis

**Claim it would change:** C1 primarily; C2 and C3 secondarily (as constraints, not targets).

**Evidence pointers.**
- S261 (`arxiv-2302.09330`): prediction uses "the tests' outcomes and durations, as well as basic
  information about the code evolution" and "does not require additional reruns, since it gathers
  this data from existing test executions" — i.e. **history is cheaper than reruns**.
- S262 (Lam et al.): "run tests in a test suite instead of in isolation, and run tests in different
  orders with fewer times each, rather than fewer orders with more times each" — the cheap axis is
  **diversity of conditions**, not more repetitions of one condition.
- S264 (ICST-24): rerun ≈ 0.02 cents; a red pipeline ≈ $5.67 of human investigation — the rerun is
  ~280× cheaper than the manual branch.
- The lane's own F3 row (`corpus/README.md:80`) already encodes the *shape*: "one control per sweep
  → N ≥ 3 byte-identical controls, **or a named mismatch**".

**[I] The synthesis.** C1's six profiles are already an *order-diversity* design (six conditions,
one run each) — exactly the axis S262 says is cheap. What is missing is not more conditions; it is
**the bounded repetition S261/S262 justify and the lane's own N≥3 policy demands, applied to the
cells where the answer matters**, plus a channel to name a mismatch. Concretely, the F3 row's
alternative to "N≥3 byte-identical" is "**or a named mismatch**", and C1's counter has no way to
name one: `deps` is a set of names and there is no `unstable`/`mismatch` value. So the
load-induced flip measured in Pattern 1 has **nowhere to go** except into a false dependence or a
false `none`.

**[I] Why this is a cross-claim move and not a C1-only defect.** The same "one observation is not a
determinism claim" reasoning that Pattern 2 applies to C2's 183-vs-17 denominator applies to C1's
132 single-run cells — but with the opposite remedy, because C1's cells are *not* deterministic
functions of the tree (Pattern 1 measured a flip) while C2's mutants *are* (Pattern 2 measured
stability). S262's "≤5 reruns classify ≥82% of the time" then sets a concrete, cheap, bounded
budget for C1's unstable cells: at most 5 repeats per unstable cell, and the price of those repeats
(S264) is negligible next to the price of a wrong standing row.

**One-command test** (the lane's own N≥3 instrument, run against the flaky statement under the
P1-like clean environment — no lane write; `--out` under `/tmp`):

```bash
env -i PATH=/usr/bin:/bin HOME=/tmp/t47-home TMPDIR=/tmp/t47-tmp LANG=C LC_ALL=C TZ=UTC \
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/repeat-control.py \
  --runs 3 --out /tmp/t47-repeat-control -- python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/env-diff.py --selftest
```

Expected on this host: `REPEAT_COMPARE identical=yes runs=3` with `REPEAT_CONTROL: baseline_nonzero`
(exit 2 — the selftest exits 1 under the clean profile), i.e. the N≥3 channel reaches a *named*
class where C1 currently has only `deps`.

---

## Contradictions stated, not smoothed

1. **C1's `deps` clause vs the lane's F3 policy.** The contract asks for "a `deps` clause equal to
   the dependence set observed by comparing the statement's (line, exit) under the clean full
   profile P1 with P0 …" — a comparison of single runs. The lane's own F3 row requires N≥3 or a
   named mismatch. Both cannot hold for a statement whose command is load-sensitive, and one of
   the 22 statements demonstrably is (Pattern 1). The contract's wording is fixed at the freeze;
   the counter's behaviour is not, and `deps` has no mismatch value.
2. **S262's "≥82% of failures" vs S263's "flakiness is not a static property".** A bounded rerun
   budget is published for *classifying failures*; S263 argues the classifier's input (static
   properties of test code) is often insufficient. For C1's dependence set the two do not conflict —
   the dependence set is an environment differential, not a static code property — but the same
   reasoning applied to a *code*-property classifier would refuse the whole instrument. The lane's
   own `r8-flakiness-not-static.md:29-34` draws exactly this line, and it is the line C1 sits on.
3. **S264's "~280×" arithmetic.** The package entry says a rerun (0.02 cents) is ~280× cheaper than
   a red pipeline ($5.67). **[O]** 5.67 / 0.0002 = 28 350, not 280. The sibling review already
   logged this (`T47ScoutHeld.md:33`). I use the ratio only qualitatively here.
4. **S262's cheap-axis advice vs the lane's N≥3 floor.** S262 says prefer *order diversity* with
   fewer repeats; the lane's F3 policy says N≥3 *byte-identical* controls. These are different
   axes and both are legitimate: C1 already buys order diversity (6 profiles), so what it lacks is
   the repeat floor, not the diversity.
5. **C2's denominator vs C2's score rule.** The contract's comparable measure is "killed 122 → ≥150
   of 183"; 183 is a **site** count over **17** functions (Pattern 2). The number is well-defined and
   the contract is frozen, so this is a reporting obligation, not a counter defect: the receipt
   should state the per-function breakdown beside the total, as
   `corpus/knowledge/r6-flaky-failures-cluster.md:38` already asks ("the classification should carry
   cluster membership beside each per-survivor verdict").

## What I did not do (scope)

- No lane file was edited except this report; the frozen contract, counters, statements list, pool
  and snapshots were read only.
- No verdict was produced: the C1 counter was run only as `--only` probes and against the frozen
  revision into scratch work dirs; the C2 pool was exercised only through `--try`; the C3 counter
  was not run.
- I did not judge, admit, edit, integrate or ship any runtime, and I did not run a campaign tool in
  the read-only package.

## Scratch inventory (all under `/tmp/tameshi-r47-T47ConnCross/`)

`fixture/` (clone of the lane at the freeze), `measure-frozen.py`, `statements-frozen.json`
(sha256 `924102dfbc6135a7d9dabef7b8b2e681a5ce4c42ca72a031ea1f8d5ab9fb2e56` = the contract's pin),
`fr-base.py` / `cov-base.py` (round-46 counters at the freeze),
`full_a.txt` (22-statement `--only` probe at the freeze: `C1_R47_PARTIAL … total=22`),
`p1like/` (P1-shaped clean environment), `rc_p1/` (repeat-control receipt).
