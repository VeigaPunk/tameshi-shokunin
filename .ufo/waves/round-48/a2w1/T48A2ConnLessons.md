# T48A2ConnLessons — cross-round scan of `## Mistakes`, rounds 44–48

seat: T48A2ConnLessons (connector, lane leaf) · wave: a2w1 · item: cross-round mistake-class scan
attacks: `corpus/lessons/round-44.md` .. `round-48.md` `## Mistakes` + `round-44..47-verifier-spotcheck.md`
method: read-only corpus scan; two cheap re-derivations (`jq`, `git rev-list`); one scratch fixture
repo (created per bounds, verified root, throwaway identity, deleted after use). No lane counter
executed (this item attacks no claim). No tools installed or upgraded.

## 1. Axes (named)

Round-48 declared axes (`.ufo/evidence/round-48/contract.json` `axes`): depth 9, **calibration 6**
(lowest non-retired, carried by C1), freshness 9; operability and coverage unnumbered. This seat is
judged on calibration, and the scan below is calibrated to it: every row cites file:line and the
command that shows it.

## 2. Mistake classes per round (tabulated)

The `class` column is the lesson's own label. Round 46 wrote free-text sentences instead of the
`mistakes.md` §5 vocabulary; the bracketed class is my normalization, used only for the recurrence
matrix. Row counts: `grep -c '^| '` over each `## Mistakes` table (44:4, 45:7, 46:9, 47:5, 48:7+2 mined).

| round | rows (file:line) | class | gist | captured-by named |
|---|---|---|---|---|
| 44 | :83 | scope | assignment-form value `safe_floor=S256` not masked; counter reports `m7=1` | none (grammar gap) |
| 44 | :84 | scope | wave plan assumed staged ids < S160; staged S160 exists | `tools/staged-id-guard.py` |
| 44 | :85 | landing | modified tracked worktree file at base, routed by r43 spot-check | none |
| 44 | :86 | number-drift | newest standing row states 114, census-valid 115 (`m6=1`) | frozen m6 class |
| 45 | :158 | number-drift | quote label "20 words"; counter measures 28 tokens | none (routed by r44 spot-check:73, which itself wrote "24") |
| 45 | :159 | landing | round-bound counter named as no-harm monitor in frozen contract; can never be green | none |
| 45 | :160 | landing | persistent-shell `set -e` aborts receipt batch mid-write | none |
| 45 | :161 | scope | entry draft misstates `env-diff.py` (reviewer HIGH-1) | per-entry QUALITY claim-vs-source bar (wave-1 reviewer) |
| 45 | :162 | vacuous | forged 5-file ledger passes the whole counter offline; S048/S093 disputed later | counter itself (blind to provenance); wave-2 non-author re-fetch |
| 45 | :163 | vacuous | 8 C2-counter selftest survivors, no killing case | none |
| 45 | :164 | provider | mori round-47 output mapped into tameshi w2 under `ScribeScorecard` | none |
| 46 | :121 | landing [landing] | no-harm monitor named in frozen contract never run at base | none → QUALITY 88 + `no-harm-gate.py` |
| 46 | :122 | provider [provider] | seat-name collision across lanes recurs in `w1-results.json` | none (r45 proposed prefix, unenforced) → QUALITY 90 |
| 46 | :123 | landing [landing] | one-line counter edit prints `C1_R46_PASS=true` over 21 failing statements | the r44 `--freeze` pin this round's counters lacked → `FROZEN_UNCHANGED` |
| 46 | :124 | landing [landing] | `no-harm.sh` prints three `RED` lines, exit 0 | QUALITY 17 adjacent only → deciding-run greps `RED` |
| 46 | :125 | vacuous [vacuous] | 4/22 mutants survive selftest; 18/22 cheat variants pass the counter | criterion 89 covers declared-survivor shape only |
| 46 | :126 | attribution [attribution] | README/lesson say the rendered page "hides the post body"; it does not | QUALITY 2; wave-1 scribe reported, L1 landed anyway |
| 46 | :127 | scope [scope] | `PROVINCE.md` append drops coldread sub-measure 60→55; monitor checks score only | none → deciding-run requires `COLDREAD_SECTIONS_CREDITED >= 60` |
| 46 | :128 | attribution [attribution] | entries state lane-facing inference as `Observation` (F1 BLOCKING + cluster) | QUALITY 2 and 3; counter cannot see prose |
| 46 | :129 | number-drift [number-drift] | freshness score 1→9 is a formula change | none → count cited beside score |
| 47 | :105 | reference-drift + vacuous | lesson prints `-`, snapshot holds U+2013; fold hid it | none (QUALITY 79/87 fold U+2013→`-`) → QUALITY 91 |
| 47 | :106 | scope + vacuous | packed differential oracle in mutation pool scores `killed=160` | none (neutral set refuses pins, not oracles) → QUALITY 93 + addition-lint |
| 47 | :107 | landing | edit counter + its hash constant together: `self_pin` passes; `tools/` outside frozen diff | `FROZEN_UNCHANGED` (counters only) → FROZEN widened to `tools/` + evidence dirs |
| 47 | :108 | attribution | package copy attributes arXiv 2607.09345 to Baltes, McKim, Zaidman, Wagner; snapshot: Gültekin, Berndt, Bell, Bach, Baltes | CORPUS.md rule 1 (manual re-open), not any counter |
| 47 | :109 | provider/scope | `/tmp` fills to 100% mid-wave; two probes die on ENOSPC | none → `/var/tmp` relocation |
| 48 | :303 | stale-premise | one-shot flaky observation (six-leg `FAIL passed=7`) restated as standing value | none — QUALITY 92 silent on observation count → R=3 counter + criterion 95 |
| 48 | :304 | scope | wave-2 spec built, validated, never dispatched; round closes below floor | none — QUALITY 78 settles *dispatched* waves only |
| 48 | :305 | landing | selftest tallies cited (`35/35, 14/14, 24/24`), zero committed receipts | none — criterion 88 binds falsifier script only |
| 48 | :306 | landing | criterion-93 falsifier uncommitted; existing receipt contradicts the report's chronology | none → one receipt per criterion block |
| 48 | :307 | reference-drift | lesson restates `{env, node}`; deciding receipt prints `observed_deps=bwrap,node` | none — 91 binds quotes only, 92 binds SCORECARD rows only |
| 48 | :308 | provider | `/tmp` fill recurs; no counter can see it | none — **QUALITY 9 is the rule that puts scratch in `/tmp`** → `/fast/scratch` protocol |
| 48 | :309 | landing | report names HEAD `663e0682`; delivered tip `03facb22` is one commit later and rewrites a landed seat report | none — 86 binds deciding receipts, 77 binds reports to the repo, neither binds a report's cited tip |
| 48 | :352 (mined) | attribution | `hermetic env-differential probe` P1 `2/9` called "host-load nondeterminism"; cause is tmpfs-on-`/tmp` masking the PATH shim | none — QUALITY 92 asks for deps, not cause → counter refuses `--work` under `/tmp`; criterion 96 |
| 48 | :358 (mined) | landing | attempt-1 L1 cites receipts that do not exist at the carrying revision | none → `pointer-check.py`, criterion 97 |

## 3. Recurrence matrix (vocab-normalized)

| class | 44 | 45 | 46 | 47 | 48 | recurring? |
|---|---|---|---|---|---|---|
| landing | 1 | 3 | 4 | 1 | 4 | every round; largest class every round since 45 |
| scope | 2 | 1 | 2 | 2 | 1 | every round |
| provider | 0 | 1 | 1 | 1 | 1 | 45→46 same seat-collision shape; 47→48 same `/tmp` incident |
| vacuous | 0 | 2 | 1 | 2 | 0 | 45–47 chain (forged ledger → selftest gaps → embedded oracle) |
| number-drift | 2 | 1 | 1 | 0 | 0 | 44–46, relabeled reference-drift after criterion 91 |
| reference-drift | 0 | 0 | 0 | 1 | 1 | new label, same drift family |
| attribution | 0 | 0 | 2 (unlabeled) | 1 | 1 (mined) | see §5 |
| stale-premise | 0 | 0 | 0 | 0 | 1 | new label for the r47 C1 miss restated |

## 4. Was each named captured-by later shown able to fail?

| captured-by (introduced) | later evidence | verdict |
|---|---|---|
| r44:84 `staged-id-guard.py` | r47 lesson cites it working (`corpus/lessons/round-47.md:67` `verdict=answered`); no failure row in 45–48 | not shown to fail |
| r44:86 frozen m6 class (newest row states census count) | the *monitor family* fails 4× later: r45:159 (round-bound monitor red by construction), r46:121 (never run at base), r46:124 (`RED` exit 0), r46:127 (untracked sub-measure 60→55; criterion 88's text at `corpus/QUALITY.md:1314-1315` was extended because of it) | shown at family level; the m6 count itself held in both spot-checks |
| r45:161 wave-1 reviewer claim-vs-source bar | r46:126 (scribe refuted the README line; L1 landed it anyway) and r46:128 (inference-as-observation passed wave-1 review) | shown able to fail (human gate overruled) |
| r45:162 counter itself + wave-2 re-fetch | r46:125 (18/22 cheat variants pass), r46:123 (one-line edit prints PASS) | shown able to fail again |
| r46:121 → QUALITY 88 + `no-harm-gate.py` | r47 `after/no-harm.stdout` and r48 `before/no-harm-at-base.stdout` all `ok`; no red slipped through 47–48 | not shown to fail in 47–48 (but pre-extension form weakened same-round, see above) |
| r46:122 → QUALITY 90 `seat-name-check.py` | r47/r48 wave specs all carry lane-round prefixes (`T46`/`T47`/`T48`; r48 `spec-w1.json` and `spec-a2w1.json`, 32/64 items, all `T48`-prefixed) | not shown to fail |
| r46:123 → `FROZEN_UNCHANGED` (counters only) | **r47:107 directly shows it failing**: counter + its hash constant edited together pass `self_pin`; rewritten tool under unchanged `sha_file` passes because `tools/` was outside the frozen diff | shown able to fail; fix widened same round |
| r47:105 → QUALITY 91 `lesson-quote-check.py` | **r48:307 shows the scope gap**: 91 byte-binds located *quotes*; numbers a lesson restates from a counter (`{env, node}` vs `{bwrap, node}`) are unread | shown incomplete |
| r47:107 → widened FROZEN (`tools/` + pinned evidence dirs) | no failure row in r48; contract amendment 8 binds it into the deciding run | not shown to fail through r48 |
| r47:108 → CORPUS.md rule 1 (manual re-open) | the automation was routed (`SCORECARD.md:2312` Planned: "a located-name check for entry authorship") and **not found built**: no author/name check in `.ufo/evidence/round-48/freshness/measure.py`; r48 rows S265–S268 rest on snapshots + fetch receipts | not shown to fail; still manual — recurrence risk carried open |

Net: of 11 named capture rules, 4 were later shown able to fail (monitor family, reviewer bar,
counter-as-gate, FROZEN-counters-only) and 1 shown incomplete (QUALITY 91); 5 hold; 1 (manual
re-open) was never institutionalized despite being routed twice.

## 5. Round 48's mined attribution mistake: new or recurrence?

**Recurrence — third instance of the class, first under this subclass, and one incident recorded
under two faces.**

1. Class level: `attribution` mistakes exist since round 46 — r46:126 (a false *reason* for a
   registry row: "the rendered page hides the post body", refuted by `w2/T46CritEntryFalseRed` F12)
   and r46:128 (an `Observation` line that was lane inference, F1 BLOCKING) — both unlabeled
   free-text, then r47:108 (provenance: wrong paper authors, caught by manual re-open).
2. Subclass: r48:352 is the first *causal* attribution: `SCORECARD.md:2314` called the P1 `2/9`
   "not stable across runs under host load"; `.ufo/waves/round-48/w1/T48RevenEnvDiff.md` §1–§3
   shows it is deterministic — the round-47 counter builds the P1 PATH shim inside `--work` and
   `tools/env-diff.py:68-71` mounts a tmpfs on `/tmp`, so a `--work` under `/tmp` masks the
   interpreter. Red-before pair: `.ufo/evidence/round-47/before/c1-at-freeze.stdout:18` (`/tmp`,
   P1 `2/9`) vs `.ufo/evidence/round-47/after/c1.stdout:18` (`/var/tmp`, P1 `9/9`).
3. Same incident, two faces: the env-diff instability is recorded twice in the round-48 lesson —
   as reference-drift (:307, the value `{env,node}` vs `{bwrap,node}`) and as the mined
   attribution (:352, the *cause* misnamed). Round 47 disclosed it (`SCORECARD.md:2314`) but
   recorded no mistake for it; round 48 mines it with a red-before receipt and institutionalizes
   it immediately (counter `under_tmp` selftest case `T63_work_under_tmp_refused`; QUALITY 96;
   contract amendment 10 records the declined F2 alternative).
4. Structural identity with r46:128: "host load" was an inference; the `/tmp`-vs-`/var/tmp` pair
   is the observation. Criterion 96 (`corpus/QUALITY.md:1420-1427`) now forbids exactly this shape.

So: not new as a class, new as a subclass, and notable as the first attribution mistake the lane
mined with a red-before receipt rather than a spot-check routed defect.

## 6. One pattern no current QUALITY criterion captures — falsifier sketch

**Pattern: a record's cited revision-identity is unbound to the tree that carries it.**
Face in r48:309 / d7: the round-47 report names lane HEAD `663e0682`; the delivered tip `03facb22`
is one commit later and rewrites a landed seat report (`git rev-list --count 663e0682..03facb22` →
1; `git diff --name-only 663e0682 03facb22` → `.ufo/waves/round-47/w1/T47ConnCross.md` only —
re-derived read-only on this seat's tree). Why nothing catches it today:

- criterion 97 (`corpus/QUALITY.md:1428+`) resolves **backticked lane paths** at the landing tip
  (`git cat-file -e TIP:path`); a bare commit hash cited as "lane HEAD" is not a lane path;
- criterion 86 (`:1156+`) binds a **deciding receipt** to the revision it measured, not the HEAD
  line a **report** prints;
- criterion 77 binds a seat report to the lane repo, not to the revision that carries it.

Adjacent uncaught faces of the same pattern: r48:305 (tallies with no resolving receipt) and
r48:306 (a receipt that contradicts the record's account of when it was taken). The r48 fixes for
rows 2, 3, 7 are protocol sentences in the lesson, not standing criteria.

**Falsifier sketch (`cited-tip-check`, demonstrated in a scratch fixture):** for a record R with
cited commit T and carrying tip H: (a) no cited commit → `CITED-TIP-UNCITED REFUSE`, exit 2
(vacuous pass refused); (b) any path R quotes as landed that differs T..H
(`git diff --quiet T H -- path`) → `CITED-TIP-FALSIFIER-OK`, exit 1; (c) else `CITED-TIP-CLEAN`,
exit 0, printing `commits-after-cited` (a receipts-only tail is tolerated; criterion 86's shape).
Refinement not exercised in the demo: confirm a cited token is a commit (`git cat-file -t`) before
counting it, so sha256 prefixes are not mistaken for commits.

Observed fixture outputs (throwaway repo under `/fast/scratch/hyaku/tameshi-r48/T48A2ConnLessons`,
root verified, deleted after use):

```
honest control (cited tip carries the quoted work; receipts-only tail after):
  CITED-TIP-CLEAN commits-after-cited=2 (receipts-only tail, cited paths unchanged)   exit 0
planted (wrap-up commit rewrites a landed, quoted seat report):
  CITED-TIP-FALSIFIER-OK {'rewritten_cited_paths': ['seat.md']}                      exit 1
vacuous (record cites no commit):
  CITED-TIP-UNCITED REFUSE                                                           exit 2
```

Proposed move (one, bounded): land this as a criterion-98 gate run by the closure at the landing
tip (in-seat use would be self-certifying), merging it with `pointer-check.py`'s path mode so one
gate covers both faces of revision-identity. Red-before input already exists: the round-47 tree
(d7 above). Affects calibration directly (a record that mis-states its own revision basis is the
purest calibration defect) and freshness adjacently (C2 receipts are revision-bound).

## 7. Explicit contradiction (stated, not smoothed)

`corpus/QUALITY.md:24` criterion 9 still reads "Scratch stays in `/tmp`", while the round-48
lesson row :308 fixes scratch to a volume apart from `/tmp` (`/fast/scratch/hyaku/tameshi-r48/<Seat>`)
and this round's operative bounds do the same. The provider mistake recurred 45→47→48 (r45:164,
r47:109, r48:308 — the latter two the same `/tmp` fill family) while the standing criterion that
seeded it was never amended (corrections exist for criteria 18 and 23; none for 9). A criterion
that contradicts its own lesson fix is itself a calibration defect: it certifies the practice the
lesson records as a mistake.

## 8. Risks

- The sketch's cited-path extraction is line-shaped (`quoted …: path`); real reports need a
  cited-path inventory (claims cite seat reports, receipts, rows) or the check degrades to
  HEAD-counting only. Named as a refinement, not exercised.
- Distinguishing "cited as landed" from "cited as pending" needs the record's own wording; a
  pending citation legitimately resolves later (criterion 97's answer is the erratum route — the
  same must apply here).
- Criteria 94–96 reached `corpus/QUALITY.md` via the attempt-1 salvage commit `15b1521e` and are
  reused under attempt-2's re-verify rule; criterion 97 (`pointer-check.py`) is the mechanism that
  re-verifies pointer claims. A criterion-98 should be landed with its red-before receipt at the
  same tip, or it repeats the prospective-record shape the round just mined (:358).

## 9. Verification (all read-only; outputs as observed)

- `jq '.items|length' .ufo/waves/round-47/spec-w2.json` → 32; `ls .ufo/waves/round-47/w2/` →
  `swarm-registry.json` only (r48:304 / d2 confirmed).
- `git rev-list --count 663e0682..03facb22` → 1; `git diff --name-only 663e0682 03facb22` →
  `.ufo/waves/round-47/w1/T47ConnCross.md` only (r48:309 / d7 confirmed).
- `grep -c '^### Criterion' corpus/QUALITY.md` → 22 at HEAD `17cc5ce` (criteria through 97;
  21 at `15b1521e`); criterion 9 text at `corpus/QUALITY.md:24`.
- No located-name/author check in `.ufo/evidence/round-48/freshness/measure.py`; the check remains
  on the Planned list (`SCORECARD.md:2312`).
- r47/r48 no-harm receipts green (`round-47/after/no-harm.stdout`, `round-48/before/no-harm-at-base.stdout`);
  r48 wave specs fully `T48`-prefixed (collision rule holding).
- Fixture demo outputs quoted in §6; scratch tree deleted (`test ! -e` → removed).
- No installs/upgrades this seat; nothing written outside this report file.
