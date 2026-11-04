# tameshi round 80 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-04
Reviewed lane tip: `9d5422bd3414b0dd1c6fa1a1c45fd9da51dee692` (base
`dd2b9e2c44df680174a829901829fe86a2185185`). Fleet report
`.ufo/reports/round-80/tameshi.md` at `e8591ba2501958818c72e6a7cee175a46a2d3bf2`.
I did not author the round. Lane gates were not executed; their committed
evidence (self-test tallies, frozen-run receipts, measured revisions) was
verified, and independent plain measurements were run where they do not
re-execute a lane gate.

## 1. Step-1 conformance

| Check | Result | Evidence |
|---|---|---|
| Report committed by the lane identity | PASS | `git log --format='%an\|%ae\|%H' -- .ufo/reports/round-80/tameshi.md` → `tameshi-shokunin\|tameshi@shokunin.local\|e8591ba2…`; in `origin/master` |
| Report lands after the lane work | PASS | lane tip committer `2026-11-04 05:14:04 -0300`; report committer `05:14:28 -0300` |
| `SHONEN` heading, one line per box | PASS | `## SHONEN`, 4 `[~]` lines = 4 `SHONEN.md` boxes; pointers resolve (`reports/round-1-calibration.md` `## box-1`/`## box-2`/`## box-4`, `.ufo/evidence/round-21/coldread/ledger.json`); no `[x]` written |
| Cited lane commits exist and are ancestors of `refs/heads/master` | PASS | `dd2b9e2c`, `ae591d5a`, `01ca77cd`, `f45c1332`, `3e310e2b`, `93991f1a`, `9d5422bd`: `git merge-base --is-ancestor` → YES each |
| Lane pushed, branch not ahead | PASS | `jj-lane.sh state` → `branch=master local=9d5422bd… remote=9d5422bd… ahead=0 behind=0 head=detached tracked=1 untracked=7`; `git ls-remote origin refs/heads/master` → `9d5422bd…` |
| No uncommitted round work | **FAIL — defect D1** | `git status --porcelain`: ` M .ufo/evidence/round-80/design/coldread-before.txt` plus 7 untracked paths (list in §6) |
| Prompt carries the template contract | PASS | `diff` of `templates/round-prompt.md:1-140` against `.ufo/prompts/tameshi-round-80.md:1-140` differs only in substitutions (fleet root, axes, lane); five round-level items and five child-lane items present; §6 carries the run-15 route/size map (supersedes run-13/11 maps quoted above it) |
| Wave size / attack share | PASS | `w1-spec.json` 13 seats, policy band 8–16; reviewer 2 + critic 1 + mutation-tester 1 = 4/13 = 30.8 %; `w1-results.json` 13 results, 0 dead; `w1.ready` + `.dispatched` present |

The fleet-side driver digest used by this closure (copied from
`.ufo/watchdog.log`): `2026-11-04T04:11:54-03:00 launch tameshi round=80
pgid=2540392 driver=hyaku-inline attempt=1`; `2026-11-04T05:15:04-03:00
complete tameshi round=80; hyaku-inline attempt=1`.

## 2. Per-claim re-check

### R80-C1 — calibration, capability: registry-home figures equal live figures

Commands run against the archived tip tree (`git archive 9d5422bd` into a
scratch root; no lane gate executed):

```sh
python3 -c "import json;print(len(json.load(open('tools/registry-figure-bind.json'))['rows']))"
# 7
grep -c '@defect' tools/selfstate-freshness-mutants.spec tools/wave-reconcile-mutants.spec
# 4 / 13
```

Observed committed evidence:

- `c1-before-sweep.txt` (committed at `ae591d5a`): `REGISTRY_BIND: rows=7
  match=0 stale=5 absent=2 error=0 unexpected=7`, exit 1; per-row live tokens
  `24/24`, `17/17`, `22/20`.
- `c1-after-sweep.txt` (committed at `01ca77cd`): `rows=7 match=7 stale=0
  absent=0 error=0 unexpected=0`; declared tokens `24/24`, `17/17`,
  `rows=23 match=21 stale=2`, `13/13`.
- `c1-selftest.txt`: `REGISTRY_BIND_SELFTEST: 11/11 pass` (11 named arms).
- Registry surfaces at the tip: last `SKILL.md` row of each name prints
  `WAVE_RECONCILE_SELFTEST: 24/24 pass`, `SELFSTATE_SELFTEST: 17/17 pass`,
  `RECEIPT_BIND_SELFTEST: 13/13 pass`; `tools/registry.json` rows
  `wave-reconcile-selftest` 24/24, `selfstate-freshness-selftest` 17/17,
  `selfstate-freshness-sweep` `rows=23 match=21 stale=2`, `receipt-bytes-selftest`
  13/13.

**Verdict for the claim: verifies — calibration improved.** The before→after
predicate (`match=0` → `match=7`) matches the committed receipts, and the
kill rule's population bound (exactly 7 declared rows) is independently
re-counted. **Record defect D2:** the report and the frozen plan state the
before-state live tokens as `23/23` and `14/14`; the cited receipt shows
`24/24` and `17/17`. The `23/23` / `14/14` figures belong to the *base tool
bytes* (verified below via the C2 control receipts, shas `ca8acdd9…` /
`d9336fcd…`), while the declaration instrument ran against the candidate
tools in the declaration worktree. The stale verdict is unaffected (19/19
and 11/11 are stale against either), but the record's numbers are not the
ones its receipt carries.

### R80-C2 — coverage: the four named survivors become fixture coverage

Commands and observed values:

```sh
sha256sum tools/selfstate-freshness.py tools/wave-reconcile.py
# 0c4ac5e4… / 2dfeda82…  (tip)
git cat-file blob dd2b9e2c:tools/selfstate-freshness.py | sha256sum
# ca8acdd9…   (base; matches the control receipts' MUTATE_TARGET)
git cat-file blob dd2b9e2c:tools/wave-reconcile.py | sha256sum
# d9336fcd…   (base; matches)
grep -n 'SELFTEST_ARMS =' tools/selfstate-freshness.py tools/wave-reconcile.py
# 17 / 24
grep -c '@defect' tools/selfstate-freshness-mutants.spec tools/wave-reconcile-mutants.spec
# 4 / 13
cat .ufo/evidence/round-80/design/noharm-ss-arms.diff   # 14a15,17 (three ARM15-17 PASS lines)
cat .ufo/evidence/round-80/design/noharm-wr-arms.diff   # 23a24 (one arm24 line)
wc -c .ufo/evidence/round-80/design/noharm-rb-arms.diff # 0 (empty)
```

Committed receipts (evidence-verified; batteries not re-executed):
`c2-control-selfstate.txt` `defects=3 killed=0 survived=3`, target sha
`ca8acdd9…`; `c2-control-wave.txt` `defects=1 killed=0 survived=1`, target
sha `d9336fcd…`; landed `c2-landed-selfstate.txt` `defects=4 killed=4
survived=0`, `CONTROL: GREEN`, restore `byte-identical`; landed
`c2-landed-wave.txt` `defects=13 killed=13 survived=0`, `CONTROL: GREEN`,
restore byte-identical; `c2-landed-*-selftest.txt` `17/17` and `24/24`.
Each new mutant's FAIL set is exactly its named arm (`ss-bom-strip`→arm15,
`ss-cache-key-drops-argv`→arm16, `python-utf8-dropped`→arm17,
`record-unknown-root-check-removed`→arm24). **Verdict: verifies — coverage
improved.**

### R80-C3 — operability: the declared tree covers the design class

Independent population census over the archived tip tree (plain grep, not the
lane gate):

```sh
grep -rlE '^# measured_rev:' .ufo/evidence | wc -l        # 22
grep -rlE '^# design_base:' .ufo/evidence | wc -l         # 7
grep -rlE '^# design_base:' .ufo/evidence | sort
# exactly the seven .ufo/evidence/round-79/* receipts
sha256sum tools/receipt-bytes-bind.py                     # 6118c755… (tip)
git cat-file blob dd2b9e2c:tools/receipt-bytes-bind.py | sha256sum  # 8d9f9d76… (base instrument)
```

22 measured + 7 design = 29 receipts at the tip; the base instrument
recognised only the measured triple, so `receipts=22` with no design field is
the correct before-state. Two bind rows re-derived byte-exactly from git
objects: `.ufo/evidence/round-78/c1-base-sweep.txt` `measured_rev=5bcb13ea…`
→ `sha256(cat-file 5bcb13ea:tools/selfstate-freshness.py) = c6e81e1c…` =
recorded (bound); `.ufo/evidence/round-78/c1-cache-kill.txt`
`measured_rev=6f532752…` → blob sha `cb891173…` ≠ recorded `7edecba8…`,
`measured_bytes_rev=091d50e4…` → blob sha `7edecba8…` = recorded
(corrected). The after receipt reads `receipts=29 bound=14 corrected=8
design=7 unbound=0`; selftest `13/13` (13 named arms). **Verdict: verifies —
operability improved.**

**Defect D3 (standing sweep pin):** `tools/selfstate-freshness.json` pins the
two new round-80 rows at the declaration commit `ae591d5a` for tools that
changed after it — `receipt-bytes-bind.py` `14b3e015…` at `ae591d5a` vs
`6118c755…` at the tip, and `registry-figure-bind.py` `8ddf0a1b…` vs
`a97171ed…`. The rows' figures match at both revisions today, but the sweep
measures pre-settlement bytes; re-pin at the landing/records revision and
re-measure next round.

## 3. Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| calibration | **improved** | C1 `match=0`→`7` and `11/11` selftest; capability row `registry-home figure binding` in `SCORECARD.md`; cold-read monitor `66/66`, score 8, box3 true at `93991f1a` (committed `coldread-after-rekey.json`) |
| coverage | **improved** | C2 four survivors → arms 15–17 (selfstate) and 24 (wave-reconcile); `SELFTEST_ARMS` 17/24; batteries `4/4` and `13/13` killed |
| operability | **improved** | C3 population 22 → 29 with `design=7`; selftest 10 → 13 named arms; `receipt-bytes-tree` registry row |
| depth | **unchanged** | no claim; `tools/mutate-and-run.sh` untouched base→tip; SCORECARD depth 10 not restated |
| freshness | **unchanged** | no claim; SCORECARD freshness 9 not restated; S289 re-open is an input, not a re-verification claim |
| adjacency | **unchanged** | `PROVINCE.md` unchanged; the reported kama overlap is a distinct cross-surface population, reported not absorbed |

No axis is harmed: the tools' base arms are line-identical additions only
(`noharm-*.diff`), `registry.json` deletions are the replaced expected tokens
of refreshed rows (no row removed), and no SCORECARD score was lowered.

## 4. Discernment spot-check (`corpus/lessons/round-80.md` `## Gate`)

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S308 — PEP 540 | admit (`spec`, tier A, `mined`) | `https://peps.python.org/pep-0540/` fetched 2026-11-04, HTTP 200, 32,969 B, sha256 `c6ed7151…` = committed snapshot; quote at page line 220 | **agree** | Quote is verbatim at line 220 ("This mode is disabled by default and enabled by the POSIX locale.", 12 words ≤25); a spec page is authoritative for `-X utf8`; it grounds arm17's fixture. Live bytes are byte-identical to the snapshot. |
| S309 — Python 3.15 `sys` | reject (`rejected`, reason + flip on the row) | `https://docs.python.org/3.15/library/sys.html` fetched 2026-11-04, HTTP 200, 280,617 B; live sha differs from the snapshot only at line 3061 ("Last updated": 03:27 → 07:56 UTC); quote at page line 999 | **agree** | The page maps `isolated` to `-I` in 11 words and states no isolation semantics; the reject reason and flip stand; the content paragraph is unchanged, so a timestamp-only rebuild does not disturb the verdict. |
| S289 — `git-cat-file` re-open | re-open claimed, `used-by` old→new claimed | `corpus/SOURCES.md` cells at `dd2b9e2c` vs `9d5422bd`: identical (`… round-61.md, round-64.md, round-79.md`), no `round-80.md`; SOURCES diff adds only S308/S309 | **disagree with the record** | The row content agrees with "byte-identical", but the claimed `used-by` edit did not land (defect D4); the report's "rows touched old→new: S289" line is false at the tip. |
| Census (required run) | gate `ok` | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`; exit 0; 169 rows; `mined=136 queued=22 rejected=11`; `A=151 B=14 C=4` | **agree** | Exit 0 matches the report; the row count and both histograms match exactly; W01/S101's tier-C mined warning is pre-existing (row untouched this round). |

## 5. Trend verdicts

- **expansion — improved.** A capability row enters `SCORECARD.md`
  (`registry-home figure binding`, first-working round 80) and the registry
  adds two opened tier-A rows on ground the lane did not hold (S308 `mined`,
  S309 `rejected`). No frontier row moved and no admitted entry claims a bar
  it failed.
- **quality — improved.** The receipt-bind verifier gained the declared
  design class and three selftest arms (10 → 13), the registry-figure binder
  is new (11 arms), and both counters were measured before→after with base
  arms byte-identical; `QUALITY.md` criteria 76–77 each cite the lesson that
  produced them.
- **discernment — improved.** Both new gate decisions agree under an outside
  re-open (see §4), rejected material is on record with a flip, and the
  QUALITY criteria are grounded in the round's own mined mistakes. The two
  record defects below are routed, not absorbed; no criterion was added
  without a lesson.

## 6. Routed defects for the lane (status-neutral; next round)

1. **D1 — uncommitted round evidence.** The lane tip carries one modified
   tracked path and seven untracked paths after the final commit
   (`git status --porcelain`): ` M .ufo/evidence/round-80/design/coldread-before.txt`
   (committed as an empty blob, 7.1 MB in the worktree) and
   `?? .ufo/evidence/round-80/coldread-at-f45.json` (7.2 MB, cited by the
   report's cold-read paragraph), `?? .ufo/evidence/round-80/design/census-before.txt`
   (cited by the report's Sources & frontier), plus five
   `?? .ufo/evidence/round-80/rekey/work-analyze/rev-f45c13323042/chunk-000{0..4}.json`.
   Fix: commit the cited receipts or replace the citations with committed
   summaries; a fresh clone cannot reach the current pointers.
2. **D2 — C1 before-state tokens are not the receipt's.** The report and
   `plans/round-80.plan.md` state `19/19→23/23` and `11/11→14/14`; the
   committed `c1-before-sweep.txt` shows live `24/24` and `17/17` (the
   declaration worktree's candidate tools). The `23/23` / `14/14` pair is the
   base-tool figure (`c2-base-*`/`c2-control-*` receipts, shas `ca8acdd9…` /
   `d9336fcd…`). Fix: restate the before row against the receipt, or re-run
   the binder with the base tool worktree and commit that receipt.
3. **D3 — the standing sweep pins pre-settlement tool bytes.** The two
   round-80 rows in `tools/selfstate-freshness.json` pin `ae591d5a`
   (`receipt-bytes-bind.py` `14b3e015…`, `registry-figure-bind.py`
   `8ddf0a1b…`) while the tip carries `6118c755…` and `a97171ed…`. Re-pin at
   the landing/records revision and re-measure (the figures happen to agree
   today; the pin does not).
4. **D4 — S289 `used-by` change claimed, not landed.** The report and lesson
   Gate log the S289 `used-by` old→new ending `… round-64.md, round-79.md,
   round-80.md`; the tip cell ends `… round-64.md, round-79.md`, and the
   SOURCES diff contains only the S308/S309 additions. Fix: append the cell
   change (and log it old→new) next round, or append a correction naming the
   superseded sentence.
5. **D5 — S289's re-open has no committed fetch receipt.** S308/S309 carry
   snapshots and headers under `.ufo/evidence/round-80/sources/`; S289's
   re-open is prose (`cmp` exit 0, cache-busted refetch) with no committed
   bytes or digest. Fix: commit the re-open extract + headers (or a digest
   file) with the row.
6. **D6 — no round-80 Search log note.** The SOURCES `## Search log`'s last
   dated notes are round-57 (the round-78 note is undated prose); the round-80
   source work is recorded only in the lesson `## Gate`. Add the bounded-search
   note per `CORPUS.md` rule 5.

## 7. Closure

`CLOSURE tameshi r80 status=ok admitted=true` — every claim verifies
(C1/C2/C3 measured, with gate tallies evidence-verified), no axis is harmed,
and the six defects above are routed for the lane's next round.
