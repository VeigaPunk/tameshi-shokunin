## Mistakes

Seven rows, one per mistake, classed by the `mistakes.md` §5 vocabulary. Row 1 is the round-47 C1 miss the
round-47 closure routed, and it is the premise this round's C1 counter is built against; rows 2–7 are the
round-47 conformance defects 1–5 plus the scratch incident, which the round-47 lesson did not record as
mistakes. Every row names the rule that should have caught it (`none` where no rule exists) and a fix whose
red state is shown by a command, not by prose. Readings are taken at the round-48 pre-data tree
(`f1cfaad3`, base `473336d9`); the round-47 receipts they compare against are committed at `edd4ca44` /
`663e0682`.

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| `stale-premise` — the round-47 C1 miss: a one-shot flaky observation restated as a standing value | `.ufo/evidence/round-47/after/c1.stdout:5` — `six-leg regression ledger` claimed `REGRESSION: FAIL (cases=9 passed=7` exit 1, observed `REGRESSION: PASS (cases=9 passed=9` exit 0, `declared_deps=env,fleet-root,node` vs `observed_deps=fleet-root,node`; the paragraph naming the wrong row is `SCORECARD.md:2318` (`663e0682`); the instability was disclosed before the deciding run at `SCORECARD.md:2314` | `none` — the criterion governing these rows, QUALITY 92 (`corpus/QUALITY.md:1365-1369`), requires the value, its exit, the tool sha256 and a `deps` clause, and says nothing about how many times the value was observed; the round-47 contract's C1 statement (`.ufo/evidence/round-47/contract.json`, `claims.C1.statement`) asks only for the line "under the live host profile P0", i.e. one observation. Disclosure (SQ 2314) was not a gate | the standing row carries `runs 3 stable` or `runs 3 nondeterministic`, and the value set is scored against R=3 observation rounds with every declared member attested (`.ufo/evidence/round-48/contract.json:26`); counter `.ufo/evidence/round-48/calibration/measure.py`. Shown able to fail by the pre-registered relabel control CTL_B (`contract.json:33`): the round-47 rows re-appended verbatim with `runs 3 stable` must print false, and the six-leg row is the input that must be refused, because the deciding run's own P0 line does not reproduce its member (`after/c1.stdout:6`: `P0=REGRESSION: PASS (cases=9 passed=9`). Limits: CTL_B and the counter receipts are freeze-step-2 artifacts and were not executed for this draft (`d1`) |
| `scope` — a wave of the declared round shape was built, validated and never dispatched; the round closed below its floor | `.ufo/waves/round-47/spec-w2.json` carries 32 items (`jq '.items\|length'` → 32) and `.ufo/waves/round-47/w2/` holds only `swarm-registry.json`, so 0 seat reports; report `:52` states "planned and not dispatched" and "40 seats, below the 64–100 floor" | `none` — QUALITY 78 (`corpus/QUALITY.md:931-943`) settles a *dispatched* wave whose parent exits before seat terminals and says in terms "Prepared specs are not dispatched seats"; no criterion refuses a round that closes with a declared wave unrun, and none compares the counted seat total against the floor | the round prints a counted shape line before any claim is scored — seat reports found per wave directory against the declared total — and a wave with a spec, a dispatch file and no seat report is reported as not dispatched, never as run (`d2`). Red state: the same count over round 47 reads `w2` = 0 seat reports against 32 spec items and 64 declared |
| `landing` — selftest tallies are cited as evidence but no receipt for any of them is committed | `.ufo/evidence/round-47/selftest/` holds 0 files (`find … -type f \| wc -l` → 0) while the report `:12` cites `C1 35/35, C2 pool 14/14, C3 24/24` and `SCORECARD.md:2308-2310` cites `addition-lint.py --selftest` → `cases=7 failed=0`; round 46 committed the same shape as `.ufo/evidence/round-46/selftest/c{1,2,3}-selftest.{stdout,exit}` (6 files) | `none` — criterion 88 (`corpus/QUALITY.md:1291-1315`) makes a committed receipt mandatory for the no-harm falsifier script only; criteria 92 and 93 name a `--selftest` command as their evidence and require no committed output for it | every selftest a claim or the frontier step cites commits `<name>-selftest.stdout` and its exit under `.ufo/evidence/round-48/selftest/` before the freeze, the round-46 layout reused. Red state: `d3` reads 0 for round 47 against three cited tallies and 6 for round 46 |
| `landing` — the falsifier of a shipped criterion has no receipt, and the receipt that exists contradicts the report's account of when it was taken | `.ufo/evidence/round-47/quality/c91-92-falsifiers.stdout` is 7 lines and ends `CRITERION-92-FALSIFIER-OK`; block 93 exists at `.ufo/evidence/round-47/quality/falsifiers.sh:26-36`; the report `:15` says the receipt was taken before 91 was added to the script, yet the same receipt carries `CRITERION-91-FALSIFIER-OK` | `none` — criterion 93 (`corpus/QUALITY.md:1371-1377`) names block 93 as its falsifier and requires no committed output; the round-46 precedent commits one (`QUALITY.md:1312-1315`: `c88-90-falsifiers.stdout`), so the omission is a regression, not an unwritten rule | one receipt per criterion block (`quality/c<N>-falsifier.stdout`), written after the block's last edit and naming the criteria it covers. Red state: `d4` counts 2 `CRITERION-…-FALSIFIER-OK` lines in a receipt cited for three criteria, so a block-per-criterion check exits 1 on the round-47 tree |
| `reference-drift` — the lesson restates a run-to-run unstable observation and the value it prints is not the one in the committed receipt | `corpus/lessons/round-47.md:118` states `hermetic env-differential probe` `{env, node}`; the content-revision receipt prints `observed_deps=bwrap,node` (`.ufo/evidence/round-47/after/c1.stdout:17`), and the two-run difference is disclosed at `SCORECARD.md:2314` (`{env, node}` in one run, `{bwrap, node}` in another) | `none` — criterion 91 (`corpus/QUALITY.md:1355-1361`) binds only located *quotes* to snapshots; criterion 92 binds a SCORECARD *row* to observed deps and leaves the lesson restatement unread | every number a lesson restates from a counter names the receipt line it came from, and the comparison runs. Red state: `d5` prints `1c1 / < env,node / --- / > bwrap,node` and exits 1 on the round-47 lesson against its own deciding receipt |
| `provider` — scratch placement on the shared `/tmp` volume filled it mid-wave, and no counter could see it | report `:17` (`/tmp` to 100%; each C1 counter pass clones the lane twelve times, ~2.3 GB; one seat held ~20 GB; two probes died on ENOSPC) and `.ufo/waves/round-47/w1/T47ExecObsD.md:30,199` (`C1_R47: clone/checkout failed` when the counter's clone hit ENOSPC at profile P2) | `none` — QUALITY 9 (`corpus/QUALITY.md:24`) is the rule that puts scratch in `/tmp`, and nothing bounds a counter's per-pass clone fan-out; QUALITY 92 (`QUALITY.md:1367`) states in terms that "free disk in `/tmp`" is a variable the profiles do not vary, so no monitor could go red before the volume filled; QUALITY 67 (`QUALITY.md:762-768`) binds a seat's `--regression --workdir` to its own scratch but not the counter's internal clones. Misroot itself did not occur (no seat file at the fleet root; QUALITY 77 clean) — the scratch half did | every seat and the L1 take a scratch root on a volume apart from `/tmp` (`/fast/scratch/hyaku/tameshi-r48/<Seat>`) with `trap 'rm -rf' EXIT`, a leftover tree is counted as that seat's defect, and the counter's work dir defaults outside `/tmp`. Red state: `d6` — `du -sh` and a directory count bound the wave's footprint (18 directories, 13 GB at this reading, live seats included), and any tree surviving the round is the failing state |
| `landing` — the report names a lane HEAD that is one commit behind the tree it delivered, and that commit rewrites a landed seat report* | report `:5` states lane HEAD `663e0682…`; `git rev-list --count 663e0682..03facb22` → 1, "run 7 wrap-up: straggler seat reports written after the landing (orchestrator commit, not a landing)", and `git diff --name-only 663e0682 03facb22` → `.ufo/waves/round-47/w1/T47ConnCross.md` only (+228/−214) | `none` — QUALITY 86 (`corpus/QUALITY.md:1156-1222`) binds a deciding receipt to the revision it measured, not the HEAD line a report prints; QUALITY 77 binds a seat report to the lane repo, not to the revision that carries it | the report's closing act reads the HEAD it names and the number of commits after the last cited one, and either the wrap-up commit lands before the report is written or it is named in the report. Red state: `d7` — the same count on the round-47 tree is 1, so a "cited tip is HEAD" check exits 1 |

\* The silent rewrite of an already-landed seat report is the same commit; the class is `landing` because the
delivered tree is not the tree the report cites, not because a counted surface moved (the rewritten file is
cited by no claim).

Red states, each a command run against the lane tree above (outputs as observed):

```
d1  git show edd4ca44:.ufo/evidence/round-47/after/c1.stdout | sed -n '5,6p'
    # claimed FAIL passed=7 | observed PASS passed=9 ; P0=PASS passed=9  (the input CTL_B must refuse)
d2  jq '.items|length' .ufo/waves/round-47/spec-w2.json ; ls .ufo/waves/round-47/w2/*.md 2>/dev/null | wc -l
    # 32 ; 0
d3  find .ufo/evidence/round-47/selftest -type f | wc -l ; find .ufo/evidence/round-46/selftest -type f | wc -l
    # 0 ; 6
d4  grep -c '^CRITERION-' .ufo/evidence/round-47/quality/c91-92-falsifiers.stdout
    # 2   (three criteria shipped: 91, 92, 93; block 93 at falsifiers.sh:26-36)
d5  diff <(grep -oP 'hermetic env-differential probe` \{\K[^}]*' corpus/lessons/round-47.md | tr -d ' ') \
          <(grep 'STATEMENT cap/hermetic' .ufo/evidence/round-47/after/c1.stdout | grep -oP 'observed_deps=\K[a-z,]+')
    # 1c1 / < env,node / --- / > bwrap,node   (exit 1)
d6  find /fast/scratch/hyaku/tameshi-r48 -mindepth 1 -maxdepth 1 -type d | wc -l ; du -sh /fast/scratch/hyaku/tameshi-r48
    # 18 ; 13G   (mid-wave; any tree left after the round is the defect)
d7  git rev-list --count 663e0682..03facb22
    # 1
```

Sweep that found no further mistake to restate: `corpus/lessons/round-47.md` `## Mistakes` carries five data
rows (`grep -n '^| ' corpus/lessons/round-47.md` → rows at `:105-109`), and its three rounds-46 rows (quote
fold, embedded oracle, self-referential pins) already ship red-before receipts (QUALITY 91 and 93, and the
deciding script's widened `FROZEN`), so restating them here would be a duplicate, not a new row. The five
round-47 conformance defects map onto rows 2–5 and 7 (defect 2 = row 7); defect 4's chronology contradiction
is carried inside row 4.

Provenance and limits of these rows: every `.ufo/evidence/round-47` path, commit, command and count above was
read on this seat's tree; the round-47 spot-check is cited only where it is the observation (the report's
account of when the receipt was taken). Row 1's fix is pre-registered, not executed: CTL_B and the C1 counter
receipts are freeze-step-2 artifacts, and this section claims none of them. Rows 2–7 are detectors only — the
fixes they name are the round-48 protocol's, and none is scored here.
