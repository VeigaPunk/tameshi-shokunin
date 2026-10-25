# tameshi-shokunin — Scorecard

Lane axes per AXES.md (six-axis vocabulary; primary verdicts per
LEARNING.md trends). Probation rounds 1-3 build the initial measurements.
Axes will be pinned with their counting commands as rounds land.

## Move log

| Round | Axis | Before | After | Evidence |
|---|---|---|---|
| 1 | depth | seed `SKILL.md`: 22 lines, 0 tables, 0 cited sources, corpus empty | 171 lines: gate-shape decision table (3 rows), fail-closed arm taxonomy (5 rows), 7 mutation-bar rules, 8-step no-permissiveness audit recipe — every rule citing a survey-note line; 3 source notes admitted under it (556+335+105 lines) | `git show 40f8e1f:SKILL.md \| wc -l` → 22; `wc -l SKILL.md corpus/knowledge/*.md` → 171 / 556 / 335 / 105; `grep -cE '^\| ' SKILL.md` → 10 (8 rule rows + 2 header rows); `grep -c 'corpus/knowledge/' SKILL.md` → 3. Re-run 2026-10-14 (TAMESHI-SCRIBE) |
| 1 | calibration | no observation/inference/unknown separation measured anywhere (corpus empty, no notes) | all three notes label every claim and keep the classes apart (kumitate O:33/I:7, kagi [OBS]28/[INF]18/[UNK]7, fleet OBSERVATION×11/INFERENCE×4); unknowns named as unknowns, never green (kumitate §9 ×4; kagi [UNK] ×7; fleet U1–U7); self-caught errors kept as append-only errata, not silently fixed (kagi ER-1 = 16 wrong-line cites + generator analysis); counts quoted from executed counters, never source greps (kumitate 62/42/60/102/39/43 executed vs 62/42/60/71/35/41 literal sites; kagi 250 from suite counters vs static 6/1/0/1/6/2) | `grep -oE '(^|[[:space:]])O:' corpus/knowledge/gates-survey-kumitate.md \| wc -l` → 33 (same for `I:` → 7); `grep -oE '\[OBS\]' corpus/knowledge/gates-survey-kagi.md \| wc -l` → 28 (`[INF]` → 18, `[UNK]` → 7); `grep -cE '^\| §' corpus/knowledge/gates-survey-kagi.md` → 16; `grep -cE '^- U[0-9]' corpus/knowledge/verification-patterns-fleet.md` → 9 (U1–U7 + 2 prediction bullets). Re-run 2026-10-14 (TAMESHI-SCRIBE) |
| 2 | depth | corpus carried no kill-rate measurement on any gate (round-1 census: "no kill-rate harness or self-code fault injection anywhere in the corpus"; SKILL's mutation bar was nominal-vs-load-bearing by argument only) | first measured kill-rate: `kimi-census.mjs`'s 43-case hermetic suite vs 10 single-edit mutants (fresh /tmp copies, one exact edit each, driver asserts old-string unique; original byte-identical, sha256 before=after `83016d45…`) → **8/10 killed (80 %)**, no inconclusive run (control 43/43; every mutant run still enumerated 43), 7.0 s sweep; survivors D2 `findings.slice(0,6)`→`(0,5)` + D10 `FROZEN.K2 25`→`24` = reported-but-unasserted surfaces (max findings in any suite run = 2 vs cap 6 + prefix-only DRIFT asserts; only `frozen.K5` asserted); per-kill failing-case labels + full reproduce spec in the new 206-line note; distilled into SKILL.md's measured mutation-bar table (kill-rate bands >80 / 50-80 / <50 with admission readings — bands are a report convention, 8/10 admits) + defect taxonomy + when-not-worth-it rules | `node kumitate-shokunin/scripts/kimi-census.mjs --selftest` → `KIMI_CENSUS_SELFTEST: 43/43 pass` / `VERDICT: PASS`, exit 0 (denominator held); `sha256sum kumitate-shokunin/scripts/kimi-census.mjs` → `83016d45049b009a…4f426` (pin held; kumitate HEAD `175de6ba`, path clean); `wc -l corpus/knowledge/mutation-case-kimi-census.md` → 206; `grep -cF '**killed**'` → 8, `grep -cF '**survived**'` → 2 (the 8/10); sensitivity re-runs from the lane's retained scratch: `node /tmp/tameshi-r2-1-work/mutant-D2.mjs --root /tmp/tameshi-r2-1-work/empty-root \| tail -1` → 5 ids + `+23 more`, `node /tmp/tameshi-r2-1-work/mutant-D10.mjs --root … \| grep 'FAMILY K2'` → `frozen=24` (both survivors observably different off-suite, as claimed); `grep -cE '^\| ' SKILL.md` → 14 (round-1 10 + 1 header + 3 band rows), `wc -l SKILL.md` → 244. Re-run 2026-10-14 (TAMESHI-SCR) |
| 2 | calibration | wave-1 record: kagi ER-1 ×16 the only errata; kumitate + fleet errata blocks "(none yet)"; three carried gaps recorded as recommendations | wave-1 review trail applied append-only to all three notes — 15 errata entries (K-R2 ×4, G-R2 ×6, V-R2 ×4) + E1 in the new mutation note (author's D7-survivor expectation wrong, kept as a calibration miss); 4 substantive corrections: K-R2-2 meta-check anchors → `claims-check.mjs:851-852` / `kimi-census.mjs:841-842`; G-R2-1 claim-ledger pin → 79301 B / `93c5827202b9cdec` (surveyed 79294/`357fb245` never committed; kagi's own round-18 `fecee87` re-pinned stamps.tsv); G-R2-2 §9 citation :53-56 → :26-28; G-R2-3 denied verbs 22→23; the rest holds/dispositions (six kumitate executed counts + pins held; kagi 250 selftest cases + `--falsify` 16/18 held; kaidoku 72 files / 468 vs 467 held; w6-w8 AGREE tallies held; kagi §8.1 [UNK] discharged = own round-18 [INF]; sibling-owned items stay recorded-not-absorbed; U1/U2 open); nothing above any errata block edited | `grep -c '^\*\*K-R2' corpus/knowledge/gates-survey-kumitate.md` → 4; `'^\*\*G-R2'` → 6; `'^\*\*V-R2'` → 4; `grep -c '^E1 —' corpus/knowledge/mutation-case-kimi-census.md` → 1; `grep -n "every finding kind fired by the suite" kumitate-shokunin/scripts/claims-check.mjs scripts/kimi-census.mjs` → :851/:841 and "…fail-closed arm…" → :852/:842 (K-R2-2 exact); `sha256sum kagi-shokunin/corpus/claim-ledger.sh` → `93c5827202b9cdec…` + `stat -c %s` → 79301 + `git -C kagi-shokunin log -1 --format='%h %ci %s'` → `fecee87` round-18 10:05:10; DENY pipeline `grep '^DENY_WORD_RE=' … \| grep -oE … \| tr '\|' '\n' \| wc -l` → 23; `sed -n '26,28p'` = the final-line rule, `'53,56p'` = the usage paragraph (G-R2-2 exact); claim-ledger selftest → `SELFTEST: PASS (97 cases)` exit 0, scope-gate → `SCOPE_SELFTEST: PASS (61 cases)` exit 0, `--falsify` exit 1 → `SCOPE_FALSIFY: FAIL (caught=16/18 failed=2)` with 2× `SCOPE BREADTH-EXCEEDS`, kagi tree porcelain-empty before/after, `corpus/README.md:43` still `18/18`; kaidoku `ls … \| wc -l` → 72, `verify:` → 468, `verified-at:` → 467; w6/w7/w8 closeout AGREE grep → 3×5/5, 3×5/5, 2×6/6+1×5/5. Re-run 2026-10-14 (TAMESHI-SCR) |
| 3 | depth | one measured kill-rate, one language, one gate (round 2: JS `kimi-census.mjs` 8/10) — PROVINCE's ≥2-lane rule blocked calling the method general, the 50 % crossover and both band interiors were unprobed, and the bash side had no measurement at all | second measured kill-rate on a bash gate, same headline: kagi `surface-census.sh`'s 16-case selftest vs 10 single-edit mutants → **8/10 killed (80 %)**, no inconclusive run, suite count held on every run, 11.0 s for 11 runs; survivors B5 (**fixture-absent arm** — deleted exec x-bit arm reachable by no case, a survivor class round 2 did not have) + B10 (CLEAN-summary `ok=` swapped — reported-never-read, same family as D10); kill widths measured per case (widest bash kill 3/16 vs JS up to 16/43 — per-case fresh fixtures + exit+token asserts vs shared fixtures + exact-line asserts; B4 killed on the token assert alone with the expected exit code); cross-language divergence distilled: same rate, different kill width, shared class reported-but-unasserted data (D2/D10, B10) + bash-only unreached-arm class (B5) — SKILL.md gained the 10-step executable sweep recipe, defect-class catalog with per-class JS+bash evidence columns, restore-discipline checklist, divergence section, and full reproduce appendices for both cases (244 → 665 lines); the plan's anti-claim resolved: the rates do not diverge wildly, the language-class differences sit in kill width and survivor composition, recorded as the finding | `bash kagi-shokunin/corpus/surface-census.sh --selftest` → `SELFTEST: PASS (16 cases)`, exit 0, skip-cases 15/16 `substrate-absent`, kagi tree porcelain-empty before/after (denominator held); `sha256sum kagi-shokunin/corpus/surface-census.sh` → `275d8294…53009f` (pin held; kagi HEAD `fecee87`); `wc -l corpus/knowledge/mutation-case-kagi-census.md` → 258 (final line unterminated); `grep -cF '**killed**'` → 8, `grep -cF '**survived**'` → 2, table rows `grep -cE '^\| (—\|B[0-9]+) \|'` → 11; anchors re-read on the pinned bytes (`sed -n '241p;214p;862p;85p'` = the guard inversion / exec-x-bit arm / summary args / die exit-2 lines, all four matching the note's edits); full independent re-sweep through the shipped tool from a spec cut from the pinned artifact → `CONTROL: GREEN`, B1–B9 per-kill failing counts 1/2/3/1/2/1/2/2 of 16 exactly as the note's table, B5+B10 `PASS (16 cases)`, `MUTATE_RESTORE: OK` before=after, `MUTATE: DONE (… killed=8 survived=2 inconclusive=0 kill-rate=80 %)`. Re-run 2026-10-14 (TAMESHI-B4) |
| 3 | operability | the mutation method existed only as prose + a per-lane ad-hoc driver left in /tmp (round 2's `mutate_driver.py` was one-off, unversioned, not in-tree); no tameshi-owned runnable instrument existed | first tool: `tools/mutate-and-run.sh` (611 lines, r3-2) — generic inject→run→restore runner: spec v1 with fail-closed parsing (count==1 asserted before any suite run, no-op edit refused, escape allowlist `\n \t \r \\`, CR refused), pinned pristine + fresh byte-copy mutants, green-control gate before any mutant run, per-defect KILLED / SURVIVED / INCONCLUSIVE (timeout 124, 126/127 = not runnable), byte-identity restore proof (`MUTATE_RESTORE: OK\|DRIFT`), evidence workdir (control + per-defect full logs, results.tsv, spec.copy), exit map 0/1/2/64; hermetic selftest builds its own fixture + mini-suite and checks control-green, kill, survivor, exact kill-rate line, restore, DEGRADED and all refusal paths — 24/24; the tool re-ran both fleet cases end-to-end: audit lane B3's dual sweep (`MUTATE: DONE … killed=8 survived=2 … kill-rate=80 %` on BOTH targets, verdict-per-defect identical to both notes, restore OK ×2) and B2's D5 re-run (same kill, same mutant sha as the executor's run) — the round-2 note's manual method now reproduces from one versioned instrument | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 24/24 pass` / `VERDICT: PASS`, exit 0; `sha256sum tools/mutate-and-run.sh` → `d8abee52…eda68` (the revision the audits replayed); scribe re-sweep in own scratch: `bash tools/mutate-and-run.sh --target kagi-shokunin/corpus/surface-census.sh --defects <spec cut from pinned bytes> --suite 'bash "$MUTANT" --selftest'` → `CONTROL: GREEN`, 8× `DEFECT B<n>: KILLED (exit=1 …)`, `DEFECT B5: SURVIVED (exit=0 …)`, `DEFECT B10: SURVIVED (exit=0 …)`, `MUTATE_RESTORE: OK`, `MUTATE: DONE (target=surface-census-b4 defects=10 killed=8 survived=2 inconclusive=0 kill-rate=80 %)`, exit 0; audit evidence re-checked: B3 `results.tsv` ×2 (10 rows each, verdicts identical to the notes) + `MUTATE_RESTORE: OK` lines, B2 `results.tsv` D5 KILLED mutant-sha `b0dfe1a7…` = the executor note's recorded sha; `wc -l tools/mutate-and-run.sh` → 611. Re-run 2026-10-14 (TAMESHI-B4) |
| 4 | calibration | round-3 state | arm-class matrix (JS+bash cases) + round-gate static projection (§13) | wave-4 32-lane; VER-T1 |
| 5 | depth | round-4 state | 3rd mutation case (tsukuroi gate, cross-author): 6/10 killed, matrix amended per arm-class evidence (not smoothed) | wave-5 32-lane |
| 6 | adjacency + operability | round-5 state | the service round on mado's gate: 4/10 killed, in-surface 4/4 vs out-of-surface 0/6 — the co-extensive assertion/kill finding | wave-6 32-lane (2 lanes rerouted alibaba->hyper) |
| 7 | operability | round-6 state | the leg ledger: --regression replays ALL 4 recorded cases at pinned git blobs (drift-immune | wave-7 32-lane (3 rerouted alibaba->hyper) |
| 8 | coverage | round-7 state | cases 5+6: kagi checklist-run (47%, third co-extensive instance, 15/15 pre-registered predictions) + kumitate claims-check | wave-8 32-lane (2 rerouted alibaba->hyper) |
| 9 | operability | round-8 state | the cadence tick fired: 4/4 legs PASS | wave-9 32-lane (2 rerouted alibaba->hyper) |
| 10 | operability | round-9 state | the operator runbook (511 lines, cold-readable, exercised receipts) | wave-10 32-lane (1 rerouted alibaba->hyper) |
| 11 | operability (terminal — the close) | round-10 state: the operator runbook landed with executed receipts, but the cadence was "a convention, not a mechanism" (ledger U9) — no firing had been announced in advance; both moved gates read `stale` with no successor rows; the ten rounds had no single restatement and the runbook's leg lines still read four | **the close:** the pre-announced tick fired — announcement `068578f1…` @ `606716f` (21:28:23Z) → first firing 21:32:35Z (**Δ +4 m 12 s**), five independent firings; pin read **4 current · 2 stale · 0 drift** (tsukuroi `084951be…` → live `10452443…` @ `af8adf1`; mado `d7edaab4…` → `93e43f8f…` @ `f7bfc9f`); tool pulse `--selftest` 80/80 + six-leg `--regression` `PASS (cases=6 passed=6; ledger legs exact…)` at `75ed934d…` (**held**), independent leg-check 6/6 clean + 65/65 mutants re-applied byte-identical; the schedule + tick series 1–4 + gap series (45 m 20 s · 51 m 45 s · 40 m 16 s) + interval `[U]` land (`closeout-r11.md` §2.5); the ten rounds restated + the service as it stands + the named debts (§1–§4 of the same note); `plans/completion-evidence.md` (PACK-T); SKILL final-pointers section (+100/−1 → 1 461 L); `corpus/lessons/round-10.md` (T11-2); `reports/r11-aud-t11.md` (12-row verdict table, CONFIRMED ×12); **open at close:** the two stale-gate successor rows (ledger byte-identical `2f25c51e…`, no appended rows), the six-leg registry row, the runbook's four-leg lines (ER-R3), the census §5 re-pin errata, the coverage rows, the r10 fresh-executor table, tsukuroi's 9 clause sites (owner's), the attestation leg + the queue | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 80/80 pass` rc 0; `--regression --workdir /tmp/w11-scr-t11/regr` → `REGRESSION: PASS (cases=6 passed=6; ledger legs exact: killed-delta<=0 flips<=0)`, rc 0, `REGRESSION_DATE 2026-10-14T21:34:27Z`, tool `75ed934d…`; six-case pin read 21:36:27Z → 4 current · 2 stale · 0 drift (`/tmp/w11-scr-t11/pin-read-open.txt`; four lanes' reads agreeing cell-for-cell); ledger `2f25c51e…` unchanged all window; poll `poll.log` (60 s × 30). Re-run 2026-10-14 (SCR-T11) |

## The ten training rounds — verdict table (rounds 2–11 = training r1–r10)

Completed at the arc's close (round 11 = training r10; the arc has no
successor — `plans/round-11.plan.md:13-25`). One row per training round, every
cell anchored to the round's landed record; nothing is re-measured and no
verdict is re-adjudicated — this table restates the move-log rows above and
`closeout-r11.md` §1 (`:42-59`; its own round-11 row was `in flight` at its
write, completed here from the round's own receipts). Verdicts as the records
land them: r1–r2 carry the rounds' recorded `improved` sentences
(`LOG.md:156-162`, `:278-289`); r3–r10 land an axis move — the records' own
language ("Axis moved: …", `LOG.md:303`) — and no landed row records a
`harmed` / `unchanged` / `unprovable-but-better` verdict. A cell with no
landed verdict renders `—`, never manufactured. Mirror: the parent's one-line
pack, `plans/completion-evidence.md:27-41`.

| Training | Round | Axis | The move (one line) | Verdict, as recorded | Receipt |
|---|---|---|---|---|---|
| r1 | 2 | depth + calibration | first measured kill-rate (kimi-census 8/10, 80 %); wave-1 errata append-only; fleet 4th pattern | improved | `SCORECARD.md:13-14` · `LOG.md:68` · `2587e0a` |
| r2 | 3 | depth + operability | second kill-rate, first bash gate (surface-census 8/10, 80 %); first tool (selftest 24/24); no-oral-context executor test | improved | `SCORECARD.md:15-16` · `LOG.md:173` · `53e74a8` |
| r3 | 4 | calibration | arm-class matrix + `--regression` mode + round-gate §13 projection | axis moved (landed) | `SCORECARD.md:17` · `LOG.md:303` · `b58b26f` |
| r4 | 5 | depth | third kill-rate, cross-author (tsukuroi 6/10, 60 %); incident I1 recorded; six-gate suite/arm census | axis moved (landed) | `SCORECARD.md:18` · `LOG.md:304` · `e0c453e` |
| r5 | 6 | adjacency + operability | first service engagement (mado 4/10, 40 %): in-surface 4/4 vs out-of-surface 0/6; own-tool meta-hardening | axis moved (landed) | `SCORECARD.md:19` · `LOG.md:305` · `4494715` |
| r6 | 7 | operability | the leg ledger (4 cases replayed at pinned git blobs); standing ledger + opt-in protocol land | axis moved (landed) | `SCORECARD.md:20` · `LOG.md:306` · `9f1d3c3` |
| r7 | 8 | coverage | cases 5+6 (47 % · 70 %) → six gates measured; cadence policy + first pin read | axis moved (landed) | `SCORECARD.md:21` · `LOG.md:307` · `c611d5d` |
| r8 | 9 | operability | first scheduled tick (4 current · 2 stale · 0 drift); the limits note | axis moved (landed) | `SCORECARD.md:22` · `LOG.md:308` · `b8eb96e` |
| r9 | 10 | operability | the operator runbook; the leg cut resolved (six legs); the boundary note | axis moved (landed) | `SCORECARD.md:23` · `LOG.md:309` · `606716f` |
| r10 | 11 | operability (terminal) | the close: the pre-announced tick fired; the schedule + the service as it stands; the ten-round record — open items named in the round-11 row above | axis moved (landed) | `SCORECARD.md:24` · `LOG.md:310` · wave-11 landing (this commit) |

Round-11's own commit is the landing that carries this file (no hash exists at
this write; HEAD `606716f`); the round's receipts ride the record above, and
its open items are named in the round-11 row — never closed by prose.

## Current axes — fleet round-1 baseline

The historical move log above predates this fleet round. It contains no
0–10 axis scores; these bounded, reproducible local rubrics establish them
without retrospectively grading the training arc.

| Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
|---|---|---|---|---|
| depth | 6 | One point per recorded mutation case listed in the tool's pinned replay ledger, capped at 10. `tools/mutate-and-run.sh:84-89`; command D below. This measures documented case depth, not newly executed cases. | `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d` | fleet round-1 baseline |
| calibration | 0 | Two points per correctly restrained, durable-evidence-linked promotion assertion (`[~]`), capped at 8; the remaining 2 require independent promotion review of all boxes. Baseline has four `[x]` marks attributed to tameshi's own dispatched agents, not independent verifiers. `SHONEN.md:5-34`; command C below. | `284ab0f0b8b989ee73d9c00c0c0df0a59757af8d` | fleet round-1 baseline |

Commands, run from this repo with `REV` set to the measured commit:

```sh
# D: recorded ledger case count = depth score (cap 10).
git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
# C: mark census only; this upper bound awards no evidence/authority credit.
git show "$REV:SHONEN.md" | python3 -c 'import re,sys; m=re.findall(r"^- \[([x~ ])\] ",sys.stdin.read(),re.M); print("boxes="+str(len(m))+" checked="+str(m.count("x"))+" asserted="+str(m.count("~"))+" untouched="+str(m.count(" "))+" asserted_mark_upper_bound="+str(min(8,2*m.count("~"))))'
```

**Planned:** calibration — replace unsupported completion claims with the
canonical four-box checklist and durable, explicitly lane-authored evidence.
Falsification: any retained `[x]` without independent provenance, any changed
box wording, or any unresolved evidence pointer defeats the claim.

**Retired:** none. Other axes in the historical log remain historical
observations, not newly assigned axes or new round moves.

## Fleet round-1 interactive continuation — local delta, admission blocked

The baseline table above remains the reproducible **pre-round** record.
The historical training arc remains intact. The driver's launch counter
does not advance a verified-round count. This attempt continues the
unfinished fleet round 1; it is not historical round 12 or fleet round 2.
No numeric score is awarded as a substitute for the verdicts below.

Measurement: `.ufo/evidence/fleet-round-1/calibration-acceptance.json`
contains the exact command/program, baseline object
`284ab0f0b8b989ee73d9c00c0c0df0a59757af8d`, candidate-file check and
complete output. Baseline canonical rows false / four `[x]` / zero
durable checklist links; candidate canonical rows true /
`[~], [~], [ ], [~]` / four resolving links, comparison exit 0.
Semantic source support was read separately and is retained in
`reports/round-1-calibration.md#interactive-continuation--blocked-dispatch-local-correction-retained`.
The content commit measured is cited by hash in the post-content local
report `.ufo/reports/round-1/tameshi.md`, not guessed in this file.

| Axis | Local candidate verdict | Evidence / bound |
|---|---|---|
| calibration (LIVE target) | improved | Unsupported independent marks withdrawn; source-linked assertions retained only within their actual scope; full cold-read box remains unchecked. Mechanical comparison plus bounded source review above. |
| depth (LIVE guardrail) | unchanged | Runner and six recorded mutation cases unchanged; no newly measured gate. |
| coverage | unchanged | No new domain surface admitted; the 32 audit scopes are a plan, not coverage. |
| operability | unchanged | Existing runner passes own 80-case selftest and actual two-defect CLI scenario; no tool change or new capability claimed. |
| freshness | unchanged | Local source rereads only; no re-pin, sibling live census or historical replay claimed. |
| adjacency | unchanged | Existing method/product boundary retained; out-of-scope routing/config defects reported, not absorbed. |

| Learning trend | Local verdict | Evidence / missing authority |
|---|---|---|
| expansion | unchanged | Corrections, not new knowledge on previously uncovered ground. |
| quality | improved | Broad cold-read and independent-authority claims explicitly superseded by narrower durable evidence; historical bytes retained. |
| discernment | unprovable-but-better | Admits/rejects documented, but no non-author spot-check of at least one admit and one reject. Lane-owned checks do not satisfy that criterion. |

**Round admission: BLOCKED.** Existing live role aliases and connector
fallback do not realize the operator contract. Exact evidence:
`.ufo/evidence/fleet-round-1/route-bindings.json` and
`live-seat-bindings.txt`. Canonical wave `plan` validated 32 distinct
tasks, exit 0; neither `run` nor native `task` was invoked under wrong
bindings. The inherited nine-seat batch cannot substitute. No completed
or verified-round increment, promotion, native verdict or saturation is
claimed; one observed blocked attempt is not three consecutive blocks.

**Planned / concrete unblock:** preserve calibration as the lowest LIVE
axis while this round is incomplete. Authorized route owner supplies
content -> `@m_composer`, audits -> `@m_grok`, connector ->
`@m_antigravity` with `@m_zfl` fallback; a fresh L1 session then
reconciles this handoff and dispatches exactly the complete canonical
32-scope payload before claiming a sound round. Independent admit/reject
review and current full cold-read proof remain separate evidence debts.
Receipt applicability must be bound to real dispatch metadata, never an
invented task key or arbitrary configuration digest.

**Retired:** none. The at-least-100 verified-round target is unchanged;
neither a launch count nor this blocked local correction counts toward
it without the required applicable evidence.

Verification erratum for the local candidate: the initial 05:10:40Z
CLI evidence used repo-local scratch and is rejected as nonconforming
to `SKILL.md:25-28`, despite its valid output. The corrected actual CLI
run at 05:14:49Z uses a fresh `/tmp/tameshi-r1-…` namespace; full
command/program/output, runner exit 0, driver exit 0 and independent
byte-identity assertion are retained in
`.ufo/evidence/fleet-round-1/cli-smoke-canonical.json`. The audit's
scratch erratum and lesson ER-I2 preserve this self-caught failure.
That corrected run is the operative smoke evidence for the table above;
the valid selftest is unchanged. Admission remains blocked.

## Fleet round 1 — kaika continuation (2026-10-19): claims and measurements

This closes the open fleet round 1 above (steered round 1,
orchestrator steer table). Its declared calibration claim comes first
and is adjudicated **once**: the `0 → 6` part landed in `cd31c6b`
(the blocked attempt of this same round) and is inherited, not
re-landed; this round adds box 3. The blocked-section prerequisites
are superseded by the kaika binding (route table assigns models by
role; non-author verification is the orchestrator's after landing).
Self-verdicts below are **pending non-author verification**; no score
is pinned on self-attestation.

| # | Claim | Type | Axis | Before | After | Counting command | Measured commit |
|---|---|---|---|---|---|---|---|
| K1 | SHONEN restraint + box 3 by a full cold-read of Appendix A + B | axis move (lowest axis) | calibration | pinned 0 at `284ab0f` (`checked=4 asserted=0` → bound 0); `4eb4cf3` bound 6 | `checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8` — candidate 8 (lane cap); final 2 need independent promotion review | command C above, `REV=<round commit>` | round-1 kaika commit (hash in `.ufo/reports/round-1/tameshi.md`, fleet ledger) |
| K2 | `sources-registry`: opened, tiered, rechecked source rows that mine into admitted entries | capability acquisition | — (per-axis verdicts below) | no `corpus/SOURCES.md`; 0 external URLs in `SKILL.md PROVINCE.md corpus` (ART §1.2 sweep) | 44 rows (A 37 · B 5 · C 2; mined 12 · queued 29 · rejected 3); every contract census check clean; 2 admitted entries cite 5 mined external rows | `bash .ufo/evidence/kaika-round-1/sources-census.sh` | same |

K1 evidence: `reports/round-1-kaika-coldread.md` (`COLDREAD: SUFFICIENT
(appendixA=8/10 recorded=8/10 appendixB=8/10 recorded=8/10
blocking-gaps=0 wrong-expectations=0 survivors-probed=4/4)`, `SKILL.md`
sha256 `33e3009c…0f81`, unchanged by this round); lesson `## Mistakes`
and `QUALITY.md` 6–10. K2 evidence: `corpus/SOURCES.md`,
`.ufo/evidence/kaika-round-1/sources-opened.tsv` (37 fetch records),
`sources-census-final.txt`. A third claim (coverage via frontier
entries) was withdrawn before landing — see `corpus/lessons/round-1.md`
`## Gate — kaika continuation`.

| Axis | Self-verdict (pending non-author) | Evidence / bound |
|---|---|---|
| calibration | improved (candidate) | K1 |
| depth | unchanged | command D → `recorded_cases=6 depth_score=6`; no new ledger leg |
| coverage | unchanged (unpinned) | F1/F2 entries admitted as knowledge; no coverage claim |
| operability | unchanged | runner unchanged; re-demonstrated (`.ufo/evidence/kaika-round-1/capability-demo/`) |
| freshness | unchanged (unpinned) | 37 sources re-opened live with recheck cadences; no rubric pinned |
| adjacency | unchanged | `PROVINCE.md` Adjacent appended; nothing absorbed |

Phase-2 corrections (same round, after the lane's Reviewer and Critic
seats re-ran every command on `c7986cd`; `corpus/lessons/round-1.md`
ER-K5…ER-K8): K1's numbers re-ran identical; the box-3 line is now
scope-bounded (Appendix A + B sweep recipe only, via the runner, B
probe fixtures reconstructed) and the Critic seat rates the `8` a
scope-incomplete candidate. K2's "contract census clean" holds for
contract v1 only; the run's extra H4 id-cite block printed 25 links
for own/gate rows S031–S037 (path-cited by pre-registry entries) and
those rows lacked Gate quotes. Fixed by the Gate addendum and census
v2: `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → exit 0,
`SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`, strict id-cite
25 (informational); mutation-tested (a planted violation →
`SOURCES_CENSUS: VIOLATIONS`). The capability row's census is v2.

Post-review corrections (same round, orchestrator adjudication
2026-10-19 — non-author; reviewer: admit with conditions; critic: K2
admit, K1 reject as measured). Append-only; the rows above stay as
written and are superseded here:

- **K1 re-pinned without the box-3 increment.** The cold-read covered
  only Appendix A + B, with Appendix B survivor-probe fixtures
  reconstructed by the seat; the box-3 `[ ]`→`[~]` move is **not
  earned** and scores 0. Box 3 stays `[~]` as a scope-noted lane
  assertion (`SHONEN.md:9-10`), carried as an unscored mark. Verified
  calibration work this round: `QUALITY.md` criteria 5 → 10 (each
  citing its `## Mistakes` row) and the box-4 overreach fix
  (`PROVINCE.md` appended Core/Frontier/Adjacent). **Calibration
  pinned 6** = boxes 1, 2, 4 restrained `[~]` × 2 (rubric of command C,
  box 3 excluded), measured on `121696b`; the inherited `0 → 6` from
  `cd31c6b` is the part admitted, counted once. Saturation note above
  ("calibration pinned 0, candidate 8 pending") is superseded: pinned 6.
- **Measured-commit cells corrected.** K1 and K2 were measured on
  `121696bf92db813f75f792be8590cf2c2c98edb1` (not "hash in the
  report" / "same"). K1 command: command C with `REV=121696b` →
  `boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8`
  (mark census only; the pin is 6 per the bullet above).
- **K2 pointer corrected.** K2's counting command is
  `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` (exit 0,
  `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`), not the v1
  `sources-census.sh` named in the K2 row. Fleet census:
  `TZ=UTC bash …/fleet-census/scripts/sources-census.sh validate <worktree>`
  → `tameshi-shokunin ok`, exit 0. K2 admitted.
- Axis verdicts: calibration improved (0 → 6 pinned); all others
  unchanged. Trends: expansion improved; **quality unchanged** (not
  improved); discernment per the orchestrator's adjudication.

## Capabilities

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | curate where the lane learns: opened, tiered, rechecked source rows, mined into admitted entries, census-gated | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → exit 0, 44 rows, `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`; `corpus/SOURCES.md` | fleet round 1 (kaika) |
| mutation sweep runner | inject → run → restore single-edit mutants with a green-control gate, verdict lines and byte-identity proof | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 80/80 pass`, exit 0 (`.ufo/evidence/kaika-round-1/capability-demo/h1a-selftest-host.stdout`) | historical round 3 (`SCORECARD.md:16`); re-demonstrated fleet round 1 |
| six-leg regression ledger | replay every recorded mutation case at its pinned blob; exact expectation | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=6 passed=6 …)`, exit 0 (`…/capability-demo/h1b-regression.stdout`) | historical round 7 (four legs) / round 10 (six); re-demonstrated fleet round 1 |
| repeated pristine-control gate | observe N≥3 exact exit/stdout/stderr tuples, distinguish mismatch from unavailable/uniform-nonzero baseline, validate digest-pinned observation snapshots | `python3 tools/repeat-control.py --selftest` → PASS (29 cases), exit 0; real bash controls match; red-before loop mutant fails the same mismatch oracle, restored loop passes; `.ufo/evidence/round-12/verification-final.json`, `oracle-repair.json`; measured `9df9212d33dc2dbda133e88f28ad47bb08839a5b` | round 12; lane demonstrated, outside admission pending |
| six-leg content-disposition probe | emit configured-pin, committed-HEAD and worktree SHA observations for every recorded leg, while explicitly withholding verdict reuse | `python3 tools/pin-disposition.py --selftest` → 18/18 PASS0; real read changed3/unchanged3/unavailable0; `.ufo/evidence/round-13/verification.json`, `pin-dispositions.json`; measured `4acc607dfd79f19d508bd50cdd06b77269fccd1d` | round 13; lane demonstrated, outside admission pending |
| exposed witness provenance correction | validate a new digest-anchored non-blind companion without rewriting frozen observations; prevent wrong-nesting in future producer output | metadata selftest39/39 PASS0; null-only companion FAIL1/corrected PASS0; producer same-oracle40/41 FAIL1→41/41 PASS0; `.ufo/evidence/round-13/producer-oracle-repair.json`, `verification-verdict.json`; measured `4acc607dfd79f19d508bd50cdd06b77269fccd1d` | round 13; lane demonstrated, outside admission pending |
| effective expectation reconciliation | account for every historical expected row, reject an exit-only setup crash, and preserve that raw failure under a checked explicit oracle supersession | `python3 tools/evidence-disposition.py --selftest` → PASS34/34 exit0; same checker before FAIL1/contains_missing→after CLEAN0, eleven effective+one superseded; `.ufo/evidence/round-14/verification-final.json`, S050; executable measurement6431478 | round14; lane demonstrated, separate outside admission pending |
| retained invocation-context gate | re-derive bounded raw receipt predicates, check byte-pinned frozen receipts, and distinguish semantic mismatch from unavailable/tampered input through a standalone public-CLI selftest | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72` → exit0, copied-source CLI selftest49/49, registered frozen0, missing-env1, tamper2, usage64; `.ufo/evidence/round-15/verification-3.json`; S051 | round15; lane demonstrated, separate non-author admission pending |
| hermetic env-differential probe | classify the raw exit/stdout/stderr tuple of nine pinned selftests under seven explicit profiles, separating repeat variation from environmental sensitivity | `python3 tools/env-diff.py --selftest` first actual9/9; real receipt `f5/receipt-initial.json` under `.ufo/evidence/round-21/` classifies9/9 (eight invariant, one raw-output-variable); `corpus/knowledge/hermetic-env-differential.md`, S079/S081 | round21; lane demonstrated, separate non-author admission pending |
| callback-authoritative wave accounting | reconcile exact registered identities and terminal states while preserving failed seats' partial artifacts; reject mismatched totals and digest tampering | at11f55d64968778aaed07b001fc8b2480c38e1896: frozen counter8/8, actual146-seat replay66 completed/80 failed, wrong-count1/TOTAL_MISMATCH; `.ufo/evidence/round-22/final/verification.json`, S082 | round22; lane demonstrated, separate non-author admission pending |

Rows enter only through a round that demonstrates the capability running (`AXES.md` §Capabilities); none enter through this rollout.

## Saturation

The lane's saturation line + stagnation window N are to be declared by the lane on its next round per `AXES.md` §The stagnation nudge; not asserted by this conformance change.

Declared fleet round 1 (kaika): **saturation line 8/10** on each owned
axis — calibration's lane-attainable cap is 8, the last 2 need
independent review; depth is capped at 10 recorded cases. **Stagnation
window N = 2** completed rounds without a capability entering the
table. Policy choices, not observations; the nudge does not fire now
(depth 6 < 8; calibration pinned 0, candidate 8 pending).

## Planned

Populated by the lane at each round start per the `SCORECARD.md` contract (`AXES.md` §SCORECARD.md contract); no entries declared by this rollout.

Round 2 (declared fleet round 1, kaika):

1. **freshness** — re-sweep the two `stale` ledger legs (tsukuroi,
   mado) at live revisions and pin a freshness rubric. Before: pin
   read 4 current · 2 stale · 0 drift → after 6 · 0 · 0. Count:
   `grep -c 'stale' corpus/knowledge/fleet-kill-rate-ledger.md` plus the
   tool's pin read.
2. **capability (frontier F3)** — repeated-control determinism gate:
   one control per sweep (`…/capability-demo/README.md` H2) → N ≥ 3
   byte-identical controls or a named mismatch.
3. **depth** — witness-scoped split on a bash leg (surface-census)
   recorded as a ledger case. Before: command D 6 → after 7.

## Retired

- none retired; record with justification when an axis is retired.


## Round 12 — measured claims (steered round 12, 2026-10-20)

The old round-2 plan above supplied F3/F2 starting points, not permission
to add a seventh ledger leg. Freshness successor re-sweeps are not claimed.
The “6 → 7” prediction is rejected and superseded: reanalysis of the same
bash target is depth within a case, not a new independent case.

Counting command, run from this repo on both revisions:
`python3 .ufo/evidence/round-12/measure.py --rev REV`.
Before: `18ad5d050ef4bcd830fe513825baed878f025024`;
after/measured content: `9df9212d33dc2dbda133e88f28ad47bb08839a5b`.
Exact outputs: `.ufo/evidence/round-12/resumed-before.json` and
`after-committed.json`. This metadata commit records that already
measured content; it does not pretend to measure itself.

| Claim | Axis / type | Falsifiable before → after | Score delta | Verdict / evidence | Measured commit |
|---|---|---|---|---|---|
| C1 repeated pristine controls | calibration; capability acquisition (F3) | repeat-control artifact 0 → 1, accompanied by executed 29-case CLI selftest, frozen match/mismatch, three actual matching bash controls and failing single-control mutant | calibration 6 → 6, delta 0; capability gained, no promotion points | improved, lane-measured; `verification-final.json`, `oracle-repair.json`, `SKILL.md` gate registry | `9df9212d33dc2dbda133e88f28ad47bb08839a5b` |
| C2 bash witness detail | depth; axis move on existing case (F2) | bash summary absent / classified defects 0 → 10, 8 witness hits / 0 accidental / 2 survived / 0 inconclusive; 14 exercised + 2 skipped case slots | depth 6 → 6, delta 0; six independent ledger cases remain six | improved, bounded case-label attribution; six specific hits, two generic-only, one extra B3 failure; `BashWitness/summary.json`, main `check`/`count` in final verification receipt | `9df9212d33dc2dbda133e88f28ad47bb08839a5b` |

Both owned axes tie at 6; C2 works the lowest depth axis. C1 may be
read as capability acquisition without forcing the historical
promotion-restraint score to count a tool. Their runtime commands are
independent; C2 does not import or invoke C1. Neither is a blind
prediction test or a proof of assertion-level causality.

Scalar commands D and C remain historical: D prints recorded_cases=6;
C prints asserted_mark_upper_bound=8, not the pinned score. The outside
round-1 adjudication excludes box 3; measure.py reports scored boxes
1/2/4 and calibration_restraint_score=6. Marks are not a fresh authority
or source-support check. The unique-gate count is a reported guardrail,
not automatic duplicate-proofing of command D.

| Axis | Round-12 lane verdict | Bound |
|---|---|---|
| depth | improved (detail), scalar unchanged 6 | C2; no new recorded case |
| calibration | improved (capability), scalar unchanged 6 | C1 and learned criterion13; no independent promotion credit |
| coverage | unchanged | new F3 knowledge indexed, no numerical coverage claim |
| operability | unchanged | runner unchanged; 80-case selftest and six-leg regression PASS |
| freshness | unchanged | no stale-successor re-pin claimed |
| adjacency | unchanged | sibling target/object store read-only; no province takeover |

Admission remains pending separate non-author closure and admit/reject
sampling. All four SHONEN marks stay `[~]`; box 3 stays scope-limited
and unscored. Saturation 8 and stagnation window 2 remain; no retirement.

Next intended claim: freshness — measure and disposition the existing
stale-successor ledger debt at actual pinned revisions. This is a plan,
not a round-13 execution or pre-claimed outcome.

## Round 13 — measured claims (2026-10-20)

The previous intended freshness sweep is not reported as executed.
C1 works tied-lowest **depth6** through a capability acquisition and
source-backed technical detail; C2 independently works **calibration6**
through the outside-routed provenance fix. No scalar changes or retirement.

Same counting command on both revisions:
`python3 .ufo/evidence/round-13/measure.py --rev REV`.
Before `546b371a48a2f6bd1e7dca6ae8aee2a6dc1b0a50`, output
`before-final.json`; after/measured content
`4acc607dfd79f19d508bd50cdd06b77269fccd1d`, output
`after-committed.json`. The earlier `before.json` used the initial,
smaller output schema; `before-final.json` is the comparable measurement.

| Claim | Axis / type | Measured before → after | Score delta | Lane verdict / proof | Measured commit |
|---|---|---|---|---|---|
| C1 structured content disposition | depth; capability acquisition, F7 prerequisite | pin_probe_artifact0→1; current record absent→six re-derivable observations, unchanged3/changed3/unavailable0 | 6→6, delta0; detail is not another independent case | improved; selftest18/18 PASS0, six actual pins verified; S003/S048 knowledge and ledger ER-5 | `4acc607dfd79f19d508bd50cdd06b77269fccd1d` |
| C2 provenance repair | calibration; capability plus root-cause correction | checker0→1, companion absent→present; canonical normalized kind null→exact exposed top-level string in new companion; original frozen summary SHA unchanged | 6→6, delta0; box3 excluded, no promotion credit | improved; selftest39/39 PASS0; same checker old-null FAIL1→corrected PASS0; identical producer oracle40/41 FAIL1→41/41 PASS0 | `4acc607dfd79f19d508bd50cdd06b77269fccd1d` |

C1's initial date-named absence was not a substantive before-state:
`claims.json` preserves the measurement refinement. Historical manual
six-row content readings already existed (last carried4current/2stale).
The acquisition is the runnable structured method and sourced F7 detail,
not six observations falsely claimed new or the constant reuse label.
The observed content states cannot establish safe verdict reuse; the
manifest is configured authority, not adversarial baseline authentication.

C2 repairs future summary generation and normalizes only the canonical
historical summary by addition. The rerun null remains named raw history
and is digest-checked, not normalized. The original tool SHA in frozen
evidence is intentionally not the repaired current tool's SHA.
The initial misplaced-producer crash is retained and excluded from proof;
only `producer-oracle-repair.json` shows the named assertion failing.

Guardrails from both count outputs: recorded_cases6, unique_recorded_gates6,
calibration_restraint_score6 (boxes1/2/4, excluding3), frozen canonical
summary SHA `acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9`.
These scalar/mark counts are not a fresh outside promotion review.

Sources: rows44→46; A37→39/B5→5/C2→2;
mined15→19/queued26→24/rejected3→3, malformed0→0 — same counting
command/revisions above. Two opened URLs, not four new sources:
S003/S041 mined and S047/S048 append-only corrections to that same PIT
URL. End census0 carries disclosed W04 duplicate-URL warnings.

| Axis | Round-13 lane verdict | Bound |
|---|---|---|
| depth | improved; scalar6 unchanged | C1 source-backed six-leg detail and demonstrated capability |
| calibration | improved; scalar6 unchanged | C2, QUALITY14, outside-routed mistake; no promotion points |
| coverage | unchanged | F7 prerequisite knowledge indexed; full reuse frontier stays open |
| operability | unchanged | old runner unchanged; new capability serves C1/C2 rather than separate axis claim |
| freshness | unchanged | no successor mutation-sweep verdict; three changed targets now named |
| adjacency | unchanged | siblings read-only; no product-gate ownership absorbed |

Admission and current admit/reject sampling remain separate non-author
closure duties. All SHONEN marks remain `[~]`, box3 scope-limited and
unscored. Saturation8/window2 unchanged; a capability enters this round,
so no stagnation waiver is claimed.

Next intended claim: freshness — prepare one owner-opted-in successor
sweep at an actual current pinned revision (kimi now joins tsukuroi/mado
debt), including explicit spec remapping and a retained run, or an honest
intake refusal. This is a plan, not an execution or future round claim.

## Round 14 — measured calibration capability (2026-10-20)

C1 works **calibration6**, tied with depth6 for lowest non-retired axis.
No stagnation waiver, retirement, scalar inflation or additional axis claim.
The intended freshness successor sweep instead receives the contract's
honest intake refusal: `.ufo/waves/round-14/w1/FreshnessIntake.md`,
sections7.1–7.4. Its bounded scans found no current service request, kimi's
old D10 anchor absent, mado's old anchors duplicated, and tsukuroi in flight.
That observed intake state is not a statement that siblings cannot advance.
Clean committed target bytes, an owner request and current unique mapped
spec remain prerequisites; successor sweep debt is not closed.

| Claim | Axis / type | Falsifiable before → after | Score delta | Evidence and measured revision |
|---|---|---|---|---|
| C1 effective expectation reconciliation | calibration; capability acquisition | no complete disposition tool/ledger → gate and twelve accounted rows; constructed all-effective ledger11 pass+1 fail → eleven effective pass+one explicit valid supersession; one raw contains mismatch remains visible | 6→6, delta0; no promotion points | same checker `--root . --dispositions FILE --json`, before exit1/expected_contains_missing and after exit0; selftest34/34 PASS0; S050 and `verification-final.json`; executable/content measured6431478 |

Executable measurement commit:
`6431478` (full hash in `expected-runtime-final.json` and
`verification-final.json`). Same static counting command for baseline and
delivered tree: `python3 .ufo/evidence/round-14/measure.py --rev REV`;
`before.json` is the actual historical baseline. `dispositions-before.json`
is constructed this round to expose the unresolved row, not a historical
file or a new producer-fix experiment. Baseline and delivered static counts
are appended after the committed-tree measurement below.

Initial code at `0c6e36d0bd2fd98077de4cff4c90c6f467c2e1fb` already
reconciled the real frozen rows but failed18 of34 own selftest fixtures.
`verification.json` retains that failure. Two fixture construction repairs
(the missing GAMMA_OK marker and JSON-brace formatting) leave production
predicates and literal expected IDs unchanged; the same selftest then passes
34/34. No failed output was erased or silently called a pass.

Prospective context capture at0c6e36d exits0: explicit bounded GIT_DIR
override, plain-git control0→128, equal raw JSON including the timestamp,
normalization excluding only observed_at, six header/PIN/REV/call mappings
all true. It is not C1's counting oracle, a retrospective r13 setup proof
or evidence of broad environment independence. `context-receipt.json`.

| Axis | Round14 lane verdict | Bound |
|---|---|---|
| depth | unchanged, scalar6 | no new target detail or seventh recorded mutation case |
| calibration | improved, scalar6 | C1 verified capability; QUALITY15–16 learn prior outside-routed defects |
| coverage | unchanged | no new covered target surface or whole-frontier completion |
| operability | unchanged | C1 capability credited once, not another independent axis move |
| freshness | unchanged | intake refusal, not a successor execution or new rate |
| adjacency | unchanged | sibling reads only; product gate ownership remains with owners |

Trend verdicts: expansion unchanged (existing ground, not new admitted
knowledge); quality improved (stale expectation and deferred empirical
account corrected by addition); discernment improved (prior outside
disagreement becomes grounded QUALITY15–16 and a failure-backed checker).
Current-round non-author admit/reject sampling and admission remain pending
separate closure. All SHONEN boxes stay `[~]`; box3 stays unscored.
Saturation8/window2 unchanged.

Next intended claim remains freshness: accept one owner-opted-in,
clean-current-revision successor spec and execute a bounded sweep, or retain
an honest intake refusal. No next round or outcome is preclaimed.

### Round14 committed-tree counting receipt

Same command:
`python3 .ufo/evidence/round-14/measure.py --rev REV`, exit0 each.
Before `d6809df7775338f000e44c8a916067b8866867fb` (`before.json`);
after `4d409d796ad8f9bf2aa8d380489da9e7d6cb9ca1`
(`after-committed.json`). This appended metadata is not claimed to measure
its own later commit.

Gate artifact0→1; disposition name coverage0→12;
effective rows0→11/superseded0→1; original expected rows12→12.
Recorded cases6→6, calibration restraint6→6; original setup exit1 and
missing mechanism assertion remain unchanged. Frozen summary and runner
SHA256 values in both outputs match exactly. Scalar delta remains0.

Source rows46→48; tiers A39→41/B5→5/C2→2;
statuses mined19→21/queued24→24/rejected3→3. Added by tier: A2 (docs1,
own-work1), B0/C0. No existing mutable field changed; S049's same-round
used-by expansion and S050's draft cadence correction are logged in lesson
Gate. End census0, disclosed S047/S048 W04 warnings unchanged.

These counts demonstrate complete retained account and capability artifact,
not authority or a proof from file existence alone. Actual discriminating
runtime proof is separately pinned at6431478 in `verification-final.json`.

## Round 15 — context gate classification and failure-backed replay

C1 works calibration6, tied with depth6 for lowest among this lane's owned
numeric axes. Other axes below are no-harm monitors, not newly assigned
scores. No stagnation waiver, retirement or promotion credit.

| Claim | Axis / type | Falsifiable before → after | Score delta | Measured evidence |
|---|---|---|---|---|
| C1 retained context gate | calibration; capability | active maintained gate0→1; standalone selftest artifact0→1; explicit64 classes0→2; unsupported old same-path selftest64→new0 with49/49; frozen clean0 and missing-env1 remain discriminated | 6→6, delta0 | S051, QUALITY17; `verification-3.json`, `attempt-3/{before,after,expected}.json`; measured7650fe4 below |

Counting command for both revisions:
`python3 .ufo/evidence/round-15/measure.py --rev REV`, exit0 each.
Before `a9cf4da78f2514c7bedd91a850a88590009d7df0`;
after `7650fe4db89f3a706aed63d048ac47e02289cc72`.
The script's text-presence counters are structural, not selftest proof;
the multiline self-invocation-line heuristic remains0 and is not credited.
Actual subprocess proof is retained separately.

Integrated command:
`python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72`,
exit0, all44 retained checks pass. The selftest is run from byte-identical
source copied to `<scratch>/lane/tools/candidate.py`, not falsely described
as the registered-path argv. Its summary is `SELFTEST: PASS (49/49)`.
The registered `tools/context-capture.py --check --json` command is separately
executed in the same run and returns0/context_consistent.

Same-path/same-argv flag-as-value proof: pre-repair maintained source
`bca5deb2f61f4235d7f5baac71219c55459f29b5` returns2/receipt_missing;
final source returns64/usage_error. Same frozen mapping fixture and CLI:
old id expected_verdict_mismatch/1 fails the literal mapping_mismatch/1
oracle; new id mapping_mismatch/1 satisfies it. Oracle FAIL1→PASS0, not
an exit-only proof. No retained argv, sibling gate or historical capture ran.

Failed integration is retained, not amended away: `verification.json` at
0494c244 has42/44 checks passing and the bad copied-tool layout triggers
hermetic-no-lane-path; `verification-2.json` at b2550559 records the
accidentally dropped ID_TOKEN_RE declaration. Only the harness layout and
diagnostic declaration were repaired; production gate SHA stays
`c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726`.
The third run's expectations/count/census live under `attempt-3/`.

Guardrails from the same counting command: recorded cases6→6, calibration
restraint6→6 (boxes1/2/4, box3 excluded); all599 historical evidence paths
preserved, changed0/added0. Runner and frozen summary retain their published
SHA values. SHONEN and prior outside lesson remain byte-identical.
Sources48→49, A41→42/B5→5/C2→2, mined21→22/queued24→24/rejected3→3;
S051 is A/own-work, not uncovered knowledge. Census before0/end0 with
unchanged disclosed S047/S048 W04 warnings.

| Axis | Round15 lane verdict | Bound |
|---|---|---|
| calibration | improved; scalar6 unchanged | C1, grounded QUALITY17 and failure-backed retained replay |
| depth | unchanged; scalar6 | no seventh recorded case or new target depth |
| coverage | unchanged | no new uncovered knowledge or whole-F7 completion |
| operability | unchanged | C1 credited once to calibration; runner unchanged |
| freshness | unchanged | no owner-approved current successor sweep executed |
| adjacency | unchanged | own retained-receipt craft only; no sibling execution or ownership |

Trends: expansion unchanged; quality improved; discernment improved via the
prior outside disagreement becoming a grounded criterion and failure-backed
fix. Current-round independent admit/reject sampling and admission remain
the separate non-author closure duty. All SHONEN boxes stay restrained;
box3 is unscored. The prior round14 outside closure already admitted its
bounded C1; dated pending wording in its old table row is historical.
Saturation8/window2 unchanged; no waiver claimed.

Next intended claim remains freshness: one owner-approved clean-current
successor spec and bounded sweep, or an explicit intake refusal. No next
round number, future capability or new rate is preclaimed.

## Round 16 — seventh recorded case and full-page cold-read (2026-10-20)

Two claims on the two tied-lowest owned axes (depth 6, calibration 6). No
stagnation waiver, retirement or new capability row. Both claims are axis
moves measured by one counting command; each verifies without the other
(C1 changes the runner ledger; C2 changes SKILL.md, SHONEN box 3's link and
the cold-read ledger).

Counting command, same on both revisions:
`python3 .ufo/evidence/round-16/measure.py --rev REV` (exit 0 each).
Before `28aeef498cc070c3183271b709bc79d344ff547a`; measured `09ee1d099190918ec388019bb79afbb6b93f1ff2`. Outputs:
`.ufo/evidence/round-16/measure-28aeef4.json`, `measure-09ee1d0.json`
(and the intermediate `measure-3490708.json`: 53/54 buckets before the
errata re-read). Command D (`SCORECARD.md:73`) gives the same depth numbers.

| Claim | Axis / type | Falsifiable before → after | Score delta | Evidence | Measured commit |
|---|---|---|---|---|---|
| C1 seventh recorded case `js-round-gate` | depth; axis move | recorded ledger cases 6 → 7 (kumitate `round-gate.mjs` @364f1d5, 5/10 killed, 10/10 predictions committed in `e69b488` before the sweep); `--regression` cases 6 → 7 PASS; header/calls/tuples agree 7/7/7, unique gates 7 | depth 6 → 7 | `corpus/knowledge/mutation-case-kumitate-round-gate.md`; `.ufo/evidence/round-16/round-gate/`; S052, S053, S056, S057 | `09ee1d099190918ec388019bb79afbb6b93f1ff2` |
| C2 full-page SKILL cold-read | calibration; axis move | box-3 full-page coverage 0/51 (no ledger) → 54/54 buckets at the measured page sha `906fb649…`; SHONEN box-3 link to the ledger false → true | calibration 6 → 8 (lane cap; the last 2 need independent promotion review) | `.ufo/evidence/round-16/coldread/ledger.json` (75 entries over 4 page versions); `w1/CR*`, `w2/RR*`, `w2/Replica*`, `w3/RX*`; S054, S055 | `09ee1d099190918ec388019bb79afbb6b93f1ff2` |

Box 3 stays `[~]` (lane assertion). Lane-dispatched seats are the lane, so
this earns the box-3 lane-assertion points only, never an `[x]`. The 8 is a
lane measurement pending the separate non-author closure; it is not pinned
on self-attestation.

Guardrails from the same command: SHONEN marks `~ ~ ~ ~` unchanged; sources
49 → 55 (A 42→47, B 5→6, C 2→2; mined 22→28, queued 24, rejected 3,
malformed 0). Census start/end exit 0, with the same disclosed S047/S048
W04 warnings.

| Axis | Round-16 lane verdict | Bound |
|---|---|---|
| depth | improved, 6 → 7 | C1 |
| calibration | improved, 6 → 8 (pending non-author) | C2; QUALITY 18–22 from mined mistakes |
| coverage | unchanged | case 7 is on Core ground (kumitate `scripts/*`); no frontier move |
| operability | unchanged | all nine lane selftests green (ToolsNoHarm). Runner selftest 80 → 83 (leg tuple + leg-count checks). The round-14 disposition gate now exits 2 at `--root .` by design, because its pinned runner input moved; its archived-root form exits 0 (RR10, RX5) |
| freshness | unchanged | no successor sweep of the stale legs |
| adjacency | unchanged | kumitate read-only (C1Overlap); owner recommendations reported, not absorbed |

Next intended claim: none pre-claimed. Open debts are named in
`corpus/lessons/round-16.md` (six older legs not env-scrubbed; `bwrap`
confinement; successor sweeps).

## Round 17 — live-tree re-pin, entry-command monitor, input-keyed cold-read (2026-10-20)

Repair-first round after round 16 closed rejected-harmed
(`corpus/lessons/round-16-verifier-spotcheck.md`). Two claims on two axes.
C1 works **calibration 6**, the lowest owned numeric axis (the closure ruled
round 16's 6→8 not earned). C2 works **operability**, which the closure graded
harmed; this lane keeps no 0–10 operability score, so C2's unit is
"registered baseline rows held / total", never converted into a score. No
stagnation waiver, retirement or new axis.

| Claim | Axis / type | Falsifiable before → after | Score delta | Evidence | Measured commit |
|---|---|---|---|---|---|
| C1 input-keyed full-page cold-read | calibration; axis move | under the input-keyed rule (`.ufo/evidence/round-17/measure.py --rev REV`, no overrides, strict trace gate): `98bea7d` 0/54 credited, `box3_full_page` false, restraint 6 → `e3827ee` 58/58, true, restraint 8; red-before on the round-14 bucket: credited at `e69b488`, `input-drift:tools/mutate-and-run.sh` at `09ee1d0` (overlay demonstration) | calibration 6 → 8 (lane cap; pending non-author) | `.ufo/evidence/round-17/coldread/ledger.json` (68 entries; 58 w2 + 8 w3 seat reports, every credited entry bound to committed trace receipts); `c1-measure-98bea7d.json`, `c1-measure-e3827ee.json`; `redbefore/`; S058, S059, S060, S064 | `e3827ee67d58673e1e9a1141ba1c8333125f4de8` |
| C2 registered outcomes restored + monitor | operability; axis move (restoration of the round-16 harm plus a new monitor) | `python3 tools/registry-check.py --rev REV --registry <round-17 registry> --tag baseline`: `98bea7d` held 22/23 (the disposition capability differs: no live-clean-capable command) → `eb7838b` 23/23 (superseded old round-14 row reported, expect 0 got 2); full registry 28/28 | n/a (unit: rows held) | `tools/registry-check.py`, `tools/registry.json`; `.ufo/evidence/round-17/c2-before-98bea7d….json`, `c2-after-eb7838b.json`; OP1 red-before `op1-redbefore-98bea7d.txt` → green `op1-green-*` | `eb7838b16490ca7ba17ea3242ade76a61f744af2` |

Separability: C2's counting command reads no cold-read ledger and C1's reads
no registry. C1's receipts record the tool bytes they ran against, so a C1 read
taken without C2's tool changes would have keyed to the old bytes and still
verified; C2's rows hold without any ledger. Sourced claim: C1 (S058, S059,
S060, S064); C2's jj fixes rest on S061–S063.

Box 3 stays `[~]` (lane assertion). SHONEN box 3 carries an appended
correction of the round-16 overclaim (R16-C2c) and links the round-17 ledger.
The 8 is a lane measurement pending the separate non-author closure.

| Axis | Round-17 lane verdict | Bound |
|---|---|---|
| calibration | improved, 6 → 8 (pending non-author) | C1; QUALITY 23–28 |
| operability | improved (restored + monitor) | C2; registry baseline 22/23 → 23/23; no-harm rerun 16/16 entry points green (w2 NoHarmSelftests) |
| depth | unchanged, 7 | command D `recorded_cases=7`; legs/calls/tuples 7/7/7; `--regression` cases=7 PASS |
| coverage | unchanged | no frontier ground moved (F7 stays open) |
| freshness | unchanged | no successor sweep; S058–S064 newly opened, not a freshness rubric move |
| adjacency | unchanged | siblings read-only; no sibling gate pins the moved bytes (w2 SiblingImpact) |

Capability counts in the table above are dated literals. At round 17:
mutation sweep runner selftest 95/95 (row says 80/80); six-leg regression is
seven legs, `cases=7` (row says 6); pin-disposition 19/19 (18/18);
evidence-disposition 56/56 (34/34). The rows stay as written; this line
supersedes their counts.

Corrections, appended (round-16 rows above stay as written): `:571` and
`:586` (calibration 6 → 8, 54/54) did not hold — the non-author closure
returned 6, and under the input-keyed rule the round-16 ledger credits 0/54;
`:588` ("operability unchanged") — the closure graded operability harmed;
round 17's C2 is the repair.

Next intended claim: none pre-claimed. Open debts: `corpus/lessons/round-17.md`
(selftest survivors, `bash-witness-study.py` env scrub behind a waiver,
registry-check timeout hardening, evidence-disposition G2/G3 HEAD vs branch
tip, knowledge entry §5 exit sentence).

## Round 18 — eighth recorded case and bounded routed-defect closure (2026-10-20)

Two claims, distinct axes. Depth 7 was the lowest owned numeric axis;
calibration 8 is a no-harm monitor, not an additional claim or promotion.

| Claim | Axis / type | Before → after | Score delta | Evidence / counting command | Measured revision |
|---|---|---|---|---|---|
| C1 eighth recorded case `js-sources-check` | depth; axis move | recorded cases 7 → 8; header/calls/tuples 8/8/8; regression cases=8 passed=8; new case 5/10 killed, 10/10 predictions held | 7 → 8, pending non-author closure | command D at :73; `python3 .ufo/evidence/round-18/measure.py --rev REV`; `.ufo/evidence/round-18/final/regression.stdout`; `corpus/knowledge/mutation-case-kumitate-sources-check.md` and its errata | before `183f87b899e6cae46be98d251cbc87fb5118f6ca`; strict after `a85f7107c4167cd9968248722256fcaf617fc30c` |
| C2 eleven named routed defects | operability; unscored axis move | ruler v2 base open=11/11 → open=0 closed=11; seven exact guard-removal mutants killed with green pristine controls, jj G2/G3 mismatch, timeout NaN/Infinity and setsid/setpgid, bash-witness repository-env leak | n/a; unit is named defect probes, not a scalar | `python3 .ufo/evidence/round-18/defect-probes.py --rev REV`; `c2-probes-v2-183f87b.txt`, `c2-probes-v2-e08271a.txt`, `final/probes.stdout` | before `183f87b`; after `e08271a`; final tools `921ef8077440f90d092aab4b9fdc750a45de1224` |

Final registry: 31/31 active held, four superseded, using
`python3 tools/registry-check.py --rev 5923d89ac491ec3d296905561a8ab0faf3fda65a --json`
in a branch-aligned scratch mirror (`final/registry-branch-aligned.stdout`).
The earlier 32/32 with three superseded rows was before the historical
round-17 trace collector row was explicitly superseded by the promoted tool.
Raw failed final attempts remain: the missing S076 citation, then a stale
scratch branch whose refs did not contain the graded commit.

Strict no-harm count at `a85f7107c4167cd9968248722256fcaf617fc30c`:
`python3 .ufo/evidence/round-18/measure.py --rev REV --explain`, exit 0,
60/60, box3 full page, restraint 8, `overrides_used=false`
(`final/measure-final-60.json`). The intermediate 59/60 is retained.
Seventeen final sections were completed by the L1 after provider
cancellations; this is not an independent or entirely blind cold-read.
It verifies the narrower input-keyed predicate, not required-command coverage.

| Axis / trend | Lane verdict | Bound |
|---|---|---|
| depth / quality | improved, depth 8 | C1 and bounded tool fixes; historical receipts unchanged |
| calibration / discernment | unchanged score 8; discernment improved | surviving mutants, false prose and intermediate failures disclosed and corrected |
| coverage / expansion | expansion improved; coverage unchanged | two knowledge notes and S008 mined; no F1–F10 ground moved |
| freshness / adjacency | unchanged | no successor sweep; kumitate gates read-only; owner recommendations only |

Open next-round work: 18 newly surviving mutations (3 registry, 3 disposition,
2 trace, 10 bash-witness); P08 non-master and P11 object-directory canaries;
round-16 measure GIT_* leak through direct invocation (registered wrapper
scrubs); registry adopted-orphan ownership and same-tick PID reuse;
unconfined git-env-canary tool; load-sensitive tsukuroi regression leg;
unimplemented required-command binding and duplicated measurement helpers.
Helper-owned live-Git recovery is fleet scope, routed in L0 (fleet `36500aa`).
No capability or promotion is pre-claimed; planned next claim is failure-backed
coverage on these named residuals, with the saturation nudge evaluated afresh.

## Round 19 — five routed calibration defects (2026-10-21)

One declared claim C1, calibration (tied lowest numeric owned axis at 8;
depth also 8). Population frozen in `.ufo/evidence/round-19/contract.json`
before corrections, landed `78b99ddcbf46f06246b978c8f5d4b6720dc5f59e`.
Unit: five named defects durably corrected, not a numerical expertise
increase. Calibration remains **8**, a dated historical score; independent
promotion and a current-page cold-read are not claimed.

Counting command:
`python3 .ufo/evidence/round-19/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV --check`
with the same ruler for both revisions. At baseline
`7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`: corrected=0, open=5,
total=5, exit1 (`.ufo/evidence/round-19/before.json`, input digests included).
Target: corrected=5, open=0, total=5, exit0; the revision-specific after
receipt is recorded separately after the corrections land.

The five items are exactly round-18 verifier §5: header PENDING, header S008
queued, four-vs-five source lines, failed witness invocation mislabeled final,
and the missing exact4b7c682 measurement receipt. QUALITY37–39 mine them;
source S049 was reopened. Append-only metadata corrections preserve original
bytes; the raw exit64 witness row stays failed and is explicitly superseded.
Actual historical replays now observe witness43/43 and input-keyed60/60,
restraint8, at4b7c682, not the round19 tip.

No new capability or frontier entry. Depth8, coverage, operability, freshness
and adjacency are unchanged; tool bytes and eight-leg mutation ledger are
unchanged. No current-page full-read/command-completeness inference follows
from these historical receipts. The 18 guard survivors, P08/P11 breadth
canaries and other round18 residuals remain open, not silently retired.

Measured C1 result at delivered correction revision
`21e79329f8bdcf01a62be63b3e46db4a7de6b6f9`: corrected=5, open=0, total=5,
exit0 (`.ufo/evidence/round-19/after-21e7932.json`, including every input
digest and ruler SHA-256). Same ruler on baseline7243e7f: corrected0/open5,
exit1. C1 lane verdict: **improved**, unit named defects, numeric calibration
8→8. This does not re-score the independent-promotion ceiling or grant
current-page cold-read credit. No axis retirement or saturation waiver.

Current no-harm correction (w1 AxisBound): at21e7932 the old round18
ledger actually measured49/60 and restraint6 (`current-ledger-monitor-21e7932.json`).
Thus the preceding historical8 sentence alone did **not** establish current
unchanged calibration. That intermediate is marked harmed until repaired,
not relabeled green. C1's five-item denominator stays unchanged.

Maintenance uses the unchanged round18 algorithm through
`.ufo/evidence/round-19/coldread/measure.py`, with a round19 default ledger
and strict trace gate, no override/legacy flags. Original ledger entries
are retained; the eleven invalidated buckets receive provenance-labeled
L1-author input-keyed source re-reads. This is neither independent/blind
cold-read evidence nor required-command coverage. The final no-harm
receipt must name its delivered revision and reproduce restraint8;
historical4b7c682 counts cannot stand in for it. QUALITY40 / lesson
`## No-harm repair` capture the failed intermediate.

### Round19 final measured verdict

C1 **improved**: baseline `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`
corrected0/open5, exit1 → measured
`32838a505fc9e15be5e7f6ad4335b0548d263dcd` corrected5/open0, exit0.
Same final ruler SHA256
`7af3e951bf67f7671954dee33aaa4dc183a642fce85cbc2d9d782085f856cf72`
on both endpoints; counting command remains the round19 measure `--rev REV --check`.
Receipts: `.ufo/evidence/round-19/final/checks.json`,
`c1-before.stdout`, `c1-final.stdout`, `expectations.json`.

Numeric calibration **8→8**, current no-harm measured at32838a5:
strict input-keyed60/60, restraint8, no overrides (`monitor-final.stdout`);
not blind/independent cold-read or command coverage. Ledger184 entries:
159 unchanged carried +25 L1-author source entries on16 distinct buckets.
Historical11/13/15 counts above describe earlier stages, not the final cohort.
Full registered suite at `d7caf86110e6c6fdcc14ee7a797bda93d32e89cb`:
33/33 active outcomes held, four superseded; new selftests43/43 and3/3,
frozen algorithm98/98 separately. Failed setup/suite attempts are retained.

Sources76→76, A67/B7/C2, mined48/queued23/rejected5, malformed0;
only four used-by cells changed, no immutable cells/removed rows/non-row loss.
Expansion unchanged; quality improved (bounded); discernment improved.
No promotion, axis retirement or new capability-table claim. Existing18
guard survivors and marked source-anchor/backlink debts remain open.

## Round 20 — frozen receipt-window enforcement (2026-10-21)

One declared claim C1, **calibration**, tied lowest owned numeric axis
(depth8/calibration8). The repeat QUALITY20 failure is routed by the
ADMITTED round19 outside review; round19 is not redone. Numeric
calibration stays8: this round counts six named receipt-hygiene predicates,
not expertise points or independent promotion. No new capability-table
row, axis retirement, frontier admission or guard-survivor closure.

| Claim | Axis / unit | Frozen before → target | Counting command / evidence | Measured revision |
|---|---|---|---|---|
| C1 frozen-before-dispatch and receipt-window predicates | calibration; corrected items, score8→8 | baseline `c144dcd807166dfc275c1ac2936fd2fa4b678bda`:0/6 → target6/6 | `python3 tools/receipt-measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV --json`; frozen stage ruler SHA `f34dc233eee33f4fea9a82c391bfb57ebfef8983f5c7146b4d2dc0b6b3be4e2d`; `.ufo/evidence/round-20/contract.json` and final receipts | baseline above; delivered measurement recorded in the observed-outcome addendum below |

The maintained wrapper supplies public isolated CLI selftests and scrubs
inherited Git overrides; it does not alter the frozen six predicates.
The inherited contract's `--check` command is unsupported and is
superseded only as an invocation: use the command above, not a shim.
Stage bytes were committed at `6fd220bce3705498d1d1054e99e3cae73c203751`
before this replacement coordinator's dispatch. Their unchanged
post-wave installation and new wrapper landed at
`c51eb32f3c8588cd391907db774af0f1d3c355c6`.

Current no-harm calibration will be measured with the unchanged round18
algorithm through the round20 default-ledger selector, with no overrides;
the historical round19 60/60 is not substituted for current evidence.
All184 original entries are carried unchanged. New source-read entries,
if needed, are labeled L1-author input-keyed re-anchoring, never blind or
independent cold-read, recipe re-execution or required-command coverage.

Stagnation: the dated fleet-round1 “nudge does not fire now” parenthetical
is historical, not a current judgment (H03). This round works a tied-lowest
axis regardless of whether the capability nudge is available; no waiver
is needed or claimed. All eighteen round18 guard survivors remain open.
Planned after this round: no claim pre-awarded; retain those behavioral
gaps, successor sweeps and required-command binding as unclosed work.

### Intermediate no-harm correction — before source re-anchoring

The earlier “calibration stays8” sentence is a target/historical-score
statement, **not** an observed current no-harm result. Actual default,
strict invocation at `d0ec3c8106aeb89b8df4054250585609ad68c26e` reports
46/61 sections, restraint6, `overrides_used=false`; retained
`.ufo/evidence/round-20/final/monitor-red-before.stdout`. That intermediate
is harmed until repaired. New receipts cannot borrow round19's60/60.

The carried184 entries are exactly159 round18 entries plus25 round19
L1-author source entries, all preserved as data, not184 independent reads.
The default selector initially accepted diagnostic override flags
(`selector-override-red-before.stdout`: exit0, overrides true, legacy
trace mode,46/61, restraint6). The new selector now refuses all three
override options, including abbreviations and equals forms, with exit64
and SELECTOR_OVERRIDE_FORBIDDEN; the frozen credit algorithm is unchanged.
Delivered strict no-harm results belong in the final receipt, not this
failed intermediate. This bounded enforcement repair is maintenance
within C1/no-harm, not a new axis claim or changed six-item denominator.

### Observed C1 outcome

Using one unchanged frozen ruler SHA
`f34dc233eee33f4fea9a82c391bfb57ebfef8983f5c7146b4d2dc0b6b3be4e2d`
and wrapper SHA
`a67bffa9c562ee1c22e8fbd580668379b452e63df82ee6141fe54623d5931afa`,
the published command above actually measured baseline
`c144dcd807166dfc275c1ac2936fd2fa4b678bda`: corrected0/open6/total6,
exit1 → `2f1f855975a98a59a73577a594db9abd4393cfc4`:
corrected6/open0/total6, exit0. Receipts:
`.ufo/evidence/round-20/final/c1-before-current.json`, `c1-after.json`,
and their stdout/stderr files. C1's bounded lane verdict is **improved**,
unit six named predicates. Numeric expertise is not increased.

Registered verification is deliberately not misrepresented as one green
full battery: the full run at `dc046fac5c05dda0a3d067afd25d7435c92b582a`
held35/36, with one new selector assertion TypeError. The repaired row
alone held1/1 at `2f1f855975a98a59a73577a594db9abd4393cfc4`,
public selector12/12. Other new public selftests were gate20/20 and
maintained ruler10/10; independent CLI controls20/20. The effective
mixed-revision registry receipt names each row's observed revision.

Source rows76→76, A67/B7/C2 and mined48/queued23/rejected5; only S049's
used-by cell changed. Source/census commands and outputs are retained in
`final/source-invariants.json`, `census-start.json` and `final/census-end.stdout`.
All original entries and failed observations remain. The final current
strict no-harm observation is separately retained as `final/monitor-final.stdout`
with its measured revision; no historical60/60 is a substitute for it.

## Round 21 — declared claims, frozen before dispatch (2026-10-21)

**Stagnation nudge fires (first use).** Both owned numeric axes sit at the
declared saturation line (depth 8, calibration 8; `## Saturation`, line 8/10)
and no capability row has entered `## Capabilities` since round 15 — five
completed rounds against window N = 2. Per `AXES.md` §The stagnation nudge
the lowest-axis obligation is waived; this round is a frontier/capability
round. Depth 8 and calibration 8 are no-harm monitors, not claimed.

| Claim | Axis / type | Frozen before → target | Counting command | Baseline receipt |
|---|---|---|---|---|
| C1 kill the 18 round-18 guard survivors | operability (own gates' selftests discriminate their guards); unit named mutants, unscored | killed 0/18 (survived 18, inconclusive 0, all four pristine controls green) → each mutant killed by a named discriminating selftest case, or named equivalent with reasons | `python3 .ufo/evidence/round-21/c1-survivors.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV --json` | `.ufo/evidence/round-21/c1-before.{json,stderr,exit}` at `08175c62d661fddf052ed10abc91313dec8eb77d` |
| C2 F5 hermetic env-differential → Core | coverage (frontier F5 → Core) + capability `tools/env-diff.py`; sourced claim | classified 0/9, tool selftest absent, F5 entry absent → 9/9 frozen surfaces classified from executed profile tuples, tool selftest pass, admitted entry citing a mined S### opened this round | `python3 .ufo/evidence/round-21/c2-count.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV --json` | `.ufo/evidence/round-21/c2-before.{json,stderr,exit}` at `08175c6` |

Separability: C1 edits only the four owning tools' selftests
(`tools/{bash-witness-study,evidence-disposition,registry-check,trace-inputs}.py`);
C2 adds `tools/env-diff.py`, its receipt, one knowledge entry, SOURCES rows
and README/PROVINCE appends. Neither ruler reads the other's files. One
R02 anchor was re-anchored before dispatch (the round-18 `ts > 0` line was
rewritten by `9ee1c80`); the same semantic edit is recorded in
`c1-mutants.json`. Mined-mistake fix (frontier step, not a claim):
`tools/wave-route-mix.py` refuses the round-20 wave (openai-codex 35/72 >
0.40, exactly the 35 Codex deaths) — `.ufo/evidence/round-21/routemix-r20-spec1.*`.

### Round21 implementation observation and no-harm boundary

Private implementation actually discriminates all18 mutants, with
green owning controls (disposition66/66, registry51 cases, trace30/30,
witnessVERDICT:PASS): `.ufo/evidence/round-21/c1-private-first.json`.
This is explicitly private execution evidence, not a landed-revision
measurement. Final committed-revision receipts are separate.

C2's actual initial profile run is9/9 classified, all clean exits0:
eight raw-tuple invariant and one repeated-output-variable (round-gate
random temporary directories, not flaky pass/fail). The intended six
are the fleet-ledger gates; the H3 runner and two later ledger gates
are explicit additions. The distinct kumitate six-suite survey is
not fully covered. F5 finite method moves to Core, not all possible
environmental surfaces or universal hermeticity.

The SKILL registry gains one current entry section for the new tool,
measurement facade and selector; SHONEN only changes its evidence
pointer to the round21 ledger. That is protocol registry maintenance,
not a third claim. Source re-anchoring must follow current-input
drift; neither the old61/61 nor the retained historical score8 proves
current no-harm. Corpus/source metadata is frozen before that repair.

Wave1:71 validated/dispatched seats,28 completed/43 provider deaths;
no replacement. Two whole-payload job-cap refusals preceded the
successful third identical dispatch. Evidence:
`.ufo/waves/round-21/{original-outcomes1.json,dispatch-refusal-01.json,
dispatch-attempt-02.json,dispatch-attempt-03.json}`.

### Landed implementation measurement and harmed intermediate

C1 measured at helper-landed
`370f2dffe66f00c3c7412c962bf3e8fcbe75dfdb`: killed18/survived0/
inconclusive0, exit0, same frozen ruler/population as0/18 baseline.
`.ufo/evidence/round-21/c1-after-A.json` retains exact instrument SHA,
argv, aware interval and complete streams. C1 lane verdict improved;
operability has no numeric expertise score.

At that same revision the current strict calibration monitor actually
reports32/62, restraint6, no overrides; depth remains8. This intermediate
is harmed, not a claim of unchanged8. The new registry-home section
increased the old61-section denominator to62; thirty actual sections
are uncredited. Evidence: `monitor/current-red-A.json` under round21.
The original199-entry prefix and historical failures stay retained;
final no-harm requires actual provenance-labelled source re-reads and
a separate committed-revision observation.

### Observed C2 outcome and final observation lookup

C2 measured at helper-landed
`790abd2129f153c13b471e381d454186edbde65e`: classified9/9, tool
selftestpass, F5 entrytrue, exit0, versus baseline0/9/absent/false exit1.
Same frozen counter/contract; `.ufo/evidence/round-21/c2-after-B.json`
retains exact argv, actual instrument SHA, ordered interval and streams.
C2 coverage/capability lane verdict improved; no numeric expertise increase.

At B the historical current monitor was31/62, restraint6; that is not
the final observation. Current-source credit and its actual measured
commit are read from `.ufo/evidence/round-21/final/monitor-current.json`;
the complete registered battery and its measured commit are in
`final/registry.json`. Original harmed observations remain preserved.
This keeps monitor provenance separate from C1's18-mutant denominator
and C2's9-surface denominator. No promotion/independent-read credit.

Wave2:75 seats,40 completed/35 provider deaths; round total146 unique
seats,68 completed/78 dead. No dead seat was replaced. Original outcomes
and fresh attack inventory are in `.ufo/waves/round-21/`.

### Original-outcome correction (round21)

The preceding40-completed/35-dead wave2 and68/78 round totals are superseded.
Two partial reports came from failed seats: original callback status wins.
Wave2 actually **38 completed/37 dead**; total146 unique seats,
**66 completed/80 dead**, no replacement. Exact terminal results:
`.ufo/waves/round-21/original-outcomes2-corrected.json`.

At measured commit `40508a120ee13e6088a594decc66d2da759bd0cc`,
the integrated battery held40/40 active (four superseded), exit0;
current strict source-credit62/62, restraint8, depth8, no overrides.
Evidence: `final/registry.json` and the preserved revision-specific monitor.
This is the observed restoration8, not a new calibration claim or promotion.
Accounting-append input drift receives a separately recorded source refresh;
the canonical final monitor carries its actual measured revision.

## Round 22 — declared callback-authoritative accounting (2026-10-21)

C1 calibration, tied lowest owned numeric axis (depth8/calibration8).
Frozen unit: eight named rejection predicates in
`.ufo/evidence/round-22/contract.json`; numeric expertise stays8, not a
fixture-count score. Before at `51d49d58ac81a1b4ea17607c4f2c4757ed6189ad`:
tool absent, discriminated0/8, exit1 (`before.json`). Target8/8 through
the same frozen `python3 .ufo/evidence/round-22/measure.py --repo REPO`.
Also replay the complete retained round21 population146 against exact
registry identities, and reject the historical report-count inference.
This is one calibration claim plus a runnable capability; no second axis
claim, promotion or provider-authenticity claim. Retained callback inputs
are declared evidence, not cryptographically authenticated telemetry.
L1 holds planner. Wave1 audits all146 original identities in52 nonoverlapping
groups plus12 concrete source/design/count attacks; no dead seat replacement.
Measured final commits and actual no-harm outputs are recorded separately.

### Round22 intermediate observation

At11f55d64968778aaed07b001fc8b2480c38e1896 C1 actually discriminates8/8
against0/8 tool-absent baseline; full declared146-seat replay is66 completed/
80 failed, wrong-count input exits1/TOTAL_MISMATCH. Registry43/43 active,
4 superseded. Numeric expertise is not increased.

The same revision's actual current strict source monitor is47/62, restraint6,
depth8, overridesfalse. This intermediate is harmed until source re-anchoring
and a separately observed current committed-revision result; old62/62 is not
borrowed. Initial new-gate guard mutations killed14/16, survivorsM10/M15
are nondiscriminating supplemental fixtures and receive a retained repair.
Canonical executed outcomes and instrument identities are in round22 final/.

### Round22 final measured verdict

At211838e3d1df48cc03316dc119ed0ec908b0eab3 the unchanged frozen counting
command `python3 .ufo/evidence/round-22/measure.py --repo REPO_AT_REV`
actually reports discriminated8/8, exit0. Before51d49d5 tool-absent0/8,
exit1, is absence of a runnable capability, not eight executed failing tests.
Final gateSHA96b3038a77f895c119b6e88d8b1278effffd1cebcc7dc18e6bd7a080a1bafd8e.
`final/verification-final.json` retains full argv, actual revision, intervals,
instrument hashes and streams. C1 calibration verdict **improved**,
numeric8→8/delta0; no independent promotion credit.

Same measured revision: current strict source coverage62/62, restraint8,
depth8, overridesfalse; full registered battery43/43 active,4 superseded,
exit0. The original234 ledger entries compare equal to the249-entry prefix;
15 new entries are actual traced L1-author source reads, not blind or
independent cold-reads, recipe execution or required-command coverage.
The prior47/62/score6 intermediate and invalid registry-source observation
remain visible. Guard sweep at6b6a3ead kills16/16 with restored0, identical
gate bytes to211838e; initial14/16 and repaired two-case receipts retained.
The actual146-seat replay remains66 completed/80 failed, two failed seats
with reports; wrong claimed totals fail1/TOTAL_MISMATCH, digest tampering2.

No other axis is claimed or harmed in the measured monitors. Same-ground
calibration repair means expansion unchanged; quality improved through the
failure-backed accounting rule; discernment unchanged pending outside
admit/reject sampling. No retirement, scalar inflation, promotion or frontier
crossing. Next intended work remains unclosed required-command binding,
frontier F1/F4/F6/F7/F8/F9/F10 and owner-approved successor sweeps; this row
awards no later round or capability.

## Round 23 — declared required-command receipt binding (2026-10-21)

C1 calibration, tied lowest owned numeric axis (depth8/calibration8):
the ten frozen public-CLI predicates in
`.ufo/evidence/round-23/contract.json` move tool-absent0/10 at
28cae179e4dc2c1fa7f032a79cdddf0b5d862d76 to target10/10.
Counting command: `python3 .ufo/evidence/round-23/measure.py --repo REPO_AT_REV`.
The capability binds explicit registered command names, exact argv, cwd,
revision and retained outcomes to requirements; positive source-read counts
cannot substitute. Numeric expertise stays8, delta0, subject to actual
current no-harm measurements. This is not full-page command coverage,
independent cold-read, producer authentication or promotion.
Frozen before receipt: `.ufo/evidence/round-23/before.json`, exit1.
The real demonstration population is the43 active baseline registry rows,
separate from ten synthetic discrimination predicates. L1 holds planner;
one64-seat batch audits43 command contracts plus21 concrete design/count
items, read-only, with no concurrent production writers or replacements.

### Round23 executed capability and intermediate boundary

At496d212bc46789cdf8cafab72978bdb7f4182963 the unchanged frozen
counter actually discriminates10/10, exit0; public selftest38/38, guard
mutations killed10/survived0/inconclusive0 with pristine/restored0.
Actual frozen43-command clone replay holds43/43; the binding gate validates
that full-stream bundle0/[] (`replay-command-A.json`, `replay-gate-A.json`).
The actual source-read command returns the expected stdout tokens but the
new gate rejects1/ARGV_MISMATCH; an actual correct command is clean0.

| capabilities addition | What it can now do | Evidence | First-working round |
|---|---|---|---|
| required-command-receipt-binding | validate a finite trusted bundle's exact named command/context/outcome declarations, with a frozen registry compiler/replay demonstration | `tools/command-binding.py`; `.ufo/evidence/round-23/{c1-after-A,replay-gate-A,source-read-gate-A}.json` | 23 |

Numeric expertise stays8/delta0, not a fixture-derived score. At that same
revision the strict current-source monitor actually drops62/62→48/62,
restraint8→6, depth8, overridesfalse. This is a harmed intermediate;
final no-harm requires actual source re-anchors and a separately recorded
strict committed-revision result. The historical249-entry prefix is retained.
No historical R17-CMD-BIND closure, full-page command coverage, independent
cold-read, execution authentication or promotion is claimed.

### Round23 restored current no-harm observation

At336565fc2e70e034307ef267aaa2018572c200d3 the actual strict
default-ledger measurement restores62/62 source support, restraint8,
depth8, overridesfalse, exit0 (`monitor-current-C.json`). The complete
registered battery holds46/46 active with4 superseded, exit0
(`registry-C.json`). Previous48/62 and47/62 harmed observations are
preserved. Fifteen actual source reads were appended to the unchanged
249-entry prefix; these do not change the command-binding denominator.
C1 calibration verdict improved; numeric8→8/delta0. The current final
revision receipt, if later, names its own revision rather than borrowing C.

### Round23 fresh falsification, corrections and final measured verdict

The authoring L1 TameshiR23 died on a Codex `cyber_policy` refusal. Its
fallback, gpt-6.1-sol, was the provider that refused. The round was
reassigned to CloseTameshi22 under the same claim, tameshi23/attempt1.
Wave2 had 64 validated seats: 30 completed and 34 dead. The dead seats have
no callback, and each transcript ends with `Request was aborted` when the
parent ended. The round total is 128 seats: 93 completed, 35 dead, no
replacements. Our own gate `tools/wave-accounting.py` reconciles both waves
to 0/[], with Replay16 the only failed-with-report seat
(`.ufo/evidence/round-23/accounting/receipt.json`).

Fresh findings were adjudicated in `.ufo/waves/round-23/fresh-adjudication.json`.
Three changes were appended as corrections, not code (corpus lesson
Errata A–D, QUALITY47, a SKILL.md correction and a knowledge-entry erratum):
- The 43-row replay's receipt argv/cwd/revision are instrument-supplied, so
  it tests only exit and stdout.
- The replay is 41 revision-pinned rows plus 2 live-dependent rows, not an
  isolated clone.
- The gate binds bundle-declared requirements.

Eight code/registry repairs are routed, not claimed. These corrections
temporarily drifted the monitor to 59/62 with restraint 6
(`monitor-intermediate-D.json`, harmed intermediate). Three actual traced
source re-anchors then appended to the unchanged 264-entry prefix.

The final measured revision is `549ede24aa9b2a6746d3973cf55dc4ceb07a5413`
(`.ufo/evidence/round-23/final-verification.json`):
- The frozen counter discriminates 10/10, exit 0, gate SHA d533dc1e.
- Selftest 38/38.
- Replay binding 0/[]; source-read 1/ARGV_MISMATCH; correct command 0.
- Strict monitor 62/62, restraint 8, depth 8, overrides false.
- Registry battery 46/46 active with 4 superseded, exit 0.
- Source census exit 0.

C1 calibration **improved**, numeric 8→8, delta 0; no other axis harmed.
The ten-anchor mutation sweep (`mutations-A.json`) was not re-run because
the tool bytes are unchanged.

Planned successor work, routed rather than awarded:
- an argv swapped-name case plus a name-insensitive mutant
- a negative-exit mutant
- bundle_sha256 pins in the two frozen registry rows
- carrying the runner's held/cleanup/external fields in the replay
- hashing the clone copy of the runner
- realpath fleet root
- bounded streams

## Round 24 — declared command-binding hardening (2026-10-21)

C1 calibration, tied lowest owned numeric axis (depth 8, calibration 8). The
claim covers eleven frozen predicates in `.ufo/evidence/round-24/contract.json`,
landed at e338f1bd0749a1786d95d3d3cd9572bb10757667 before any build seat:
- K1–K3: argv swapped-between-names, case-fold and negative-exit mutants
  killed by the public selftest;
- K4: the any-token control;
- K5–K6: bundle-digest pins on the two frozen registry rows;
- K7–K11: projection refusal for not-held, cleanup-failed and over-limit
  rows, the live-dependent listing and realpath identity.

Before, at 6a1821a8897eea6e7d9669292160ec9593669409: 1/11, exit 1
(`before.json`). K4 is already killed at base by round23's `all-of-tokens`
case and is kept as a control.

Counting command: `python3 .ufo/evidence/round-24/measure.py --repo CLONE_AT_REV`.
Numeric expertise stays 8 (delta 0), not a fixture-count score. Source rows
S084 and S085 are opened. Measured results are recorded below only after
execution.

| capabilities addition | What it can now do | Evidence | First-working round |
|---|---|---|---|
| refusing-registry-replay | replay frozen registry requirements, refuse to publish a binding bundle from rejected/cleanup-failed/over-limit rows, list live-dependent rows, realpath fleet identity | `tools/registry-replay.py`; `.ufo/evidence/round-24/` final receipts | 24 |

### Round 24 — measured result and fresh-wave errata (replacement L1 TameshiR24-2)

| Claim | Axis | Before | After | Delta | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|---|
| C1 command-binding hardening | calibration | 1/11, exit 1 at 6a1821a | 11/11, exit 0 at c8c5b88 | +10 predicates (K4 a control); numeric 8→8, delta 0 | `python3 .ufo/evidence/round-24/measure.py --repo CLONE_AT_REV` | c8c5b88c8e961a929cdc351b95a7074c76958909 | `.ufo/evidence/round-24/before.json`, `after.json`; seats RunRulerAfter, RunRulerBase | improved (measured), bounded by lesson Errata E–L |

No-harm at c8c5b88 (`noharm-c8c5b88.json`):
- the strict monitor gives 62/62, restraint 8, depth 8, overrides false;
- registry 47/47 held, 7 superseded, exit 0;
- census exit 0 (81 → 83 rows).

The ten moved predicates cover seven mechanisms. K7–K11 measure the new
`registry-replay.py` capability: its base failures are tool-absent, not
repairs. The fresh 64-seat wave found weaker implementations that pass the
frozen ruler (single-fixture predicates) and validation gaps in `--project`.
Both are recorded as errata and QUALITY49 and routed to round25. The tool,
fixtures and ruler were not changed after the wave. The capabilities row
above is bounded by Errata E (publication-only stream bound) and G (input
validation).

Residual-review correction (round24): the C1 verdict is bounded by all lesson
Errata E–P and the residual corrections, not just E–L. Explicit mechanism
taxonomy: argv K1/K2, exit K3, digest pins K5/K6, runner-held/cleanup K7/K8,
stream-size K9, live listing K10, identity K11 are seven moved groups;
including unchanged stdout K4 makes eight groups. Grouping all three refusal
predicates K7–K9 instead gives six moved/seven total. Neither grouping is a
new measured claim; the stable unit remains eleven named predicates.

The capabilities row is a bounded synthetic demonstration, not end-to-end
replay hardening: real replay refused 0/43; rejection is shown synthetically.
Evidence is `after.json`, `replay-command.json`, `replay-gate.json` and
`final-verification.json` under `.ufo/evidence/round-24/`. In particular L,
M and O qualify the row: ambient pin inputs, live receipts certified as
ordinary receipts, and stale clean pairs surviving refusal. The consumer
warning now appears directly in SKILL.md.

Harmed intermediates are retained: bd38c02 had 47/62 and restraint 6
(`monitor-intermediate-A.json`); 250069f had 60/62 and restraint 6
(`monitor-intermediate-B.json`). Source re-anchors restored the bounded
monitor; at measured 4903959, `final-verification.json` records 62/62,
restraint 8, depth 8, overrides false, registry 47/47, census exit 0.
Those numerical checks do not detect misleading prose; the appended
consumer warnings and the open defects must be read alongside them.

A third harmed intermediate C is retained at c6e827a: 59/62, restraint 6
after the consumer-warning correction. Its three actual traced source
reads and preserved 284-entry prefix are recorded in the C-series files.
The post-C landing measurement is retained separately in
`.ufo/evidence/round-24/landing-verification.json`.

## Round 25 — routed-item dispositions and report interop (2026-10-22)

Attempt 2, L1 TameshiR25 (fresh identity; attempt 1 was not resumed). Two
claims on distinct axes, frozen in `.ufo/evidence/round-25/contract.json` at
`2a97ec1782424f5fc0281e3ed08f89a2ee3dbdb9` before the wave; amendments 1
(`c9ff09f`) and 2 (`09dc114`) only add checks or make the counter runnable
from a clone, and come before any after measurement.

- **C1 calibration (repair-first).** Lowest owned numeric axis, tied with
  depth at 8. It counts mismatches between the lane's own record and the
  routed state: round-23 closure items with no SCORECARD disposition backed by
  an executed check. Counter `python3 .ufo/evidence/round-25/c1-measure.py
  --repo CLONE_AT_REV`; before `C1_ROUTED: dispositioned=0/3`, exit 1, at
  `1f73157`; target 3/3, exit 0. Companion input-pin check
  `python3 .ufo/evidence/round-25/c1-pins.py --repo CLONE_AT_REV`. Numeric
  calibration stays 8: this is a record repair, and the R1/R2 kills are
  controls on an unchanged gate (QUALITY48), not gate repairs.
- **C2 coverage, capability (frontier F1 report interop).** Counter
  `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py
  --check --fleet-root /home/vgpnk/Projects/shokunin`; before: tool absent at
  `1f73157` (0/8); target `MTE_INTEROP: PASS legs_conforming=8/8`, exit 0.

Routed-item disposition rows (one per item; read by both counters):

| Label | State | Item (MANIFEST `rounds[421].notes`) | Executed check | Evidence |
|---|---|---|---|---|
| R23-ROUTED-1 | dispositioned | multi-token stdout fixture in the ruler | eleven ruler-owned fixtures (seven multi-token) through the gate's public CLI kill all ten stdout and iteration mutants M1–M10, each with an explicit `FIXTURE … FAIL` witness; control green, restore OK | `.ufo/evidence/round-25/multitoken-cases.json`, `multitoken-mutants.spec`, `c1-suite.py` |
| R23-ROUTED-2 | dispositioned | re-run guard sweep | all ten round-23 guard anchors re-run verbatim (G1–G4, G9–G14) plus three finding-drop variants (G5–G7) and one lane-added guard (G8): 14/14 killed by the gate selftest, each with a `CASE … FAIL` witness | `.ufo/evidence/round-25/guard-mutants.spec` |
| R23-ROUTED-3 | dispositioned | dead-falsifier coverage gap | every one of the 34 round-23 wave-2 seats that died was re-attacked by a fresh round-25 seat: 34 completed, 20 AGREE, 14 FINDING, 0 died; doctored ledgers (one row dropped, one status flipped) fail as required | `.ufo/evidence/round-25/dead-falsifier-disposition.json`; `.ufo/waves/round-25/w1/Re*.md` |

| capabilities addition | What it can now do | Evidence | First-working round |
|---|---|---|---|
| mutation report interop | emit each recorded ledger leg as a mutation-testing-elements report, validate it with the official schema 3.9.0, score it with the official metrics library 3.9.0, and check counts and per-defect statuses against the runner's own tables | `tools/mte-interop.py --selftest`, `--check`; `corpus/knowledge/mte-report-interop.md`; S086, S087 | 25 |

Measured results are appended below only after execution.

### Round 25 — measured results (TameshiR25)

| Claim | Axis | Before | After | Delta | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|---|
| C1 routed-item dispositions | calibration | 0/3, exit 1 at 1f73157 | 3/3, exit 0 | +3 records; numeric 8→8 | `python3 .ufo/evidence/round-25/c1-measure.py --repo CLONE_AT_REV` | 77302fa8f79144d06c1d2d2e2d2898c44b459bda | `.ufo/evidence/round-25/c1-before.json`, `after/c1-measure.stdout`; companion `c1-pins.py` HOLD 0 failures (`after/c1-pins.stdout`) | improved (measured, record repair) |
| C2 mutation report interop | coverage | tool absent at 1f73157 (0/8) | `MTE_INTEROP: PASS legs_conforming=8/8`, exit 0; selftest 17/17 | +8 legs; capability added | `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin` | 77302fa8f79144d06c1d2d2e2d2898c44b459bda | `.ufo/evidence/round-25/c2-before.json`, `after/c2-check.stdout`, `after/c2-selftest.stdout`, `mte-reports/` | improved (measured) |

Bounds: the C1 counter's population is three fixed labels; a SCORECARD row
reading "NOT dispositioned" still passes the frozen counter (only `c1-pins.py`
P5 refuses it; executed in a scratch clone, see the lesson). C2's score
equality holds by construction; `ledger` and `per_mutant` carry the
information.

No-harm: at 77302fa the strict cold-read monitor fell from 62/62 (restraint 8)
to 45/62 (restraint 6) because this round's edits to corpus files drifted the
traced inputs of 17 SKILL.md sections (`after/monitor-harmed-77302fa.json`).
That harmed intermediate is retained. The restoration and the final monitor,
registry and census receipts are recorded in the lesson's `## After
measurement`.

### Round 25 — correction (appended in round 26)

Routed by `corpus/lessons/round-25-verifier-spotcheck.md:193-196`; nothing
above is rewritten. The round-25 header names amendments 1 (`c9ff09f`) and 2
(`09dc114`) only. **Amendment 3** (`.ufo/evidence/round-25/contract-amendment-3.json`)
landed in `77302fa`, the C1 and C2 measured commit, and also precedes the
recorded after-measurement (receipts in `154bf4d`). It only adds refusals and
one selftest case: `c1-pins.py` P5 requires the exact row shape; the interop
leg set must equal the ledger legs; tar members are contained; a node timeout
is SETUP; `narrow-score-delta` makes the selftest 17 cases. Its JSON flag
`before_any_after_measurement: true` is true for the L1's recorded receipts,
not for seat probes: wave seats had already run the C2 counter at PASS 8/8 at
`c9ff09f` and `09dc114`, under the weaker ruler
(`round-25-verifier-spotcheck.md:88-95`). No target or population moved.

## Round 26 — ninth recorded case and round-25 record repair (2026-10-22)

L1 TameshiR26, attempt 1. Two claims, frozen in
`.ufo/evidence/round-26/contract.json` at
`622d31d90b1fbc55c56e91a2b012bc18d6f1421a` before any mutant ran and before
any edit the C2 counter reads.

- **C1 depth (learning claim).** Depth and calibration tie at 8 as the
  lowest owned numeric axes; depth has headroom to 10. Ninth recorded ledger
  leg `js-cite-check` = kumitate `scripts/cite-check.mjs` at `1205c66`.
  Counter `python3 .ufo/evidence/round-26/c1-measure.py --repo CLONE_AT_REV`:
  before `C1_DEPTH: recorded_cases=8 wired_legs=8 depth_score=8`, exit 1, at
  base `d4140796` (`.ufo/evidence/round-26/c1-before.stdout`); target
  `recorded_cases=9 wired_legs=9 depth_score=9`, exit 0. Command D (above)
  gives the same depth score. Sourced: the entry cites S088 and S089, opened
  this round.
- **C2 calibration (record repair).** Mismatches between the lane's own
  record and repo bytes for the round-25 spot-check routed items 1–3
  (registry row for `tools/mte-interop.py`; this SCORECARD and the lesson
  omitting amendment 3; the stale `verified-at` line). Counter
  `python3 .ufo/evidence/round-26/c2-measure.py --repo CLONE_AT_REV`: before
  `C2_RECORD: mismatches=3/3`, exit 1, at base
  (`.ufo/evidence/round-26/c2-before.stdout`); target `mismatches=0/3`,
  exit 0. Numeric calibration stays 8 (lane cap). Only item 2 is a
  SCORECARD self-assessment row in the strict sense; items 1 and 3 are the
  lane's SKILL registry and knowledge-entry records (seat CriticC2).

Capabilities: no new row. `tools/mte-interop.py` (round 25) now has registry
rows `mte-interop-selftest` and `mte-interop-check` and judges nine legs.
Measured results are appended below only after execution.

### Round 26 — measured results (TameshiR26)

| Claim | Axis | Before | After | Delta | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|---|
| C1 ninth recorded case | depth | `recorded_cases=8 wired_legs=8 depth_score=8`, exit 1 at d4140796 | `recorded_cases=9 wired_legs=9 depth_score=9`, exit 0; command D `recorded_cases=9 depth_score=9` | depth 8 → 9 | `python3 .ufo/evidence/round-26/c1-measure.py --repo CLONE_AT_REV` | 40a12bf34f34977a5789e81b930303b97c4038d1 | `.ufo/evidence/round-26/c1-before.stdout`, `after/c1-measure-40a12bf.stdout`, `after/commandD-40a12bf.stdout`; regression 9/9 `cite-check/regression-worktree.stdout`; interop 9/9 `after/mte-check-a08e85c.stdout` | improved (measured) |
| C2 round-25 record mismatches | calibration | `mismatches=3/3`, exit 1 at d4140796 | `mismatches=0/3`, exit 0 | 3 → 0 records; numeric 8 → 8 | `python3 .ufo/evidence/round-26/c2-measure.py --repo CLONE_AT_REV` | 40a12bf34f34977a5789e81b930303b97c4038d1 | `.ufo/evidence/round-26/c2-before.stdout`, `after/c2-measure-40a12bf.stdout` | improved (measured, record repair) |

Bounds: C1's counter checks that the ninth leg is recorded and wired; the
regression replay (`match=10/10`) ties its table to the pinned bytes, and a
leg copied from another leg would pass both (seat CriticC1). C2's counter can
be gamed by token-bearing prose and stale receipts (seat MutateC2Counter);
its after-value stands with the seat reviews of the actual correction text.
No-harm readings (monitor, registry, census) are recorded in
`corpus/lessons/round-26.md` `## After measurement`.

### Round 26 — correction (appended in round 27)

The round-26 measured table above, row C2, says calibration "numeric 8 → 8".
That is wrong for the same revisions. The lane's strict cold-read monitor
(`.ufo/evidence/round-21/coldread/measure.py`), which computes the
calibration score of this SCORECARD's "Current axes", read restraint 8 at
base `d4140796` and restraint 6 at `40a12bf`, `d2206cd`, `2b064cf` and the
landed head `e08444d3` (committed receipts
`.ufo/evidence/round-26/after/monitor-harmed-*.json`; round-26 closure
`corpus/lessons/round-26-verifier-spotcheck.md:120-123`). Calibration was
harmed in round 26, 8 → 6, not held at 8. The row is left as written; this
entry supersedes its delta cell. Re-measured at round-27 base `91edf9cd`:
`C1_MONITOR: covered=25/64 restraint=6 box3_mismatch=1`
(`.ufo/evidence/round-27/c1-before.stdout`).

## Round 27 — monitor repair and frontier F8 (2026-10-22)

L1 TameshiR27, attempt 1. Two claims, frozen in
`.ufo/evidence/round-27/contract.json` with both counters before any
content edit of this round.

- **C1 calibration (harm repair, routed by the round-26 closure item 1).**
  Self-assessment against repo state: SHONEN box 3 is `[~]` and cites the
  cold-read ledger, but the strict monitor credits 25 of 64 sections, so
  that box and the repo disagree. Counter
  `python3 .ufo/evidence/round-27/c1-measure.py --repo CLONE --rev REV`:
  before `C1_MONITOR: covered=25/64 restraint=6 box3_mismatch=1`, exit 1,
  at base `91edf9cd`; target `covered=T/T restraint=8 box3_mismatch=0`,
  exit 0, at the landed lane head, where T is that head's section total.
  Repair method: independent cold reads by fresh seats that did not write
  the sections, at the content revision; no author re-anchor.
- **C2 coverage, frontier F8 (learning claim, sourced).** Oracle anchoring
  as a survivor class. The four round-26 cite-check survivors called suite
  holes were judged by a pristine-versus-mutant differential, an
  expectation that flows from the code under mutation. Each is re-judged
  against an expectation composed outside that code, by an executed probe
  whose receipt is bound to the probe and anchor bytes. Counter
  `python3 .ufo/evidence/round-27/c2-measure.py --repo CLONE --rev REV`:
  before `C2_F8: survivors=4 classified=0 anchored_holes=0`, exit 1, at
  base; target `classified=4`, exit 0. The anchored-hole count is reported
  as observed. Sourced: S012 re-opened and mined this round, plus new rows
  for the outside anchors.

Not claimed: the `--regression` leg-sum check (round-26 closure item 5)
stays open, because `tools/mutate-and-run.sh` is a traced input of most
cold-read entries and an edit would re-drift the sections C1 restores.
Measured results are appended below only after execution.

### Round 27 — measured results (TameshiR27)

| Claim | Axis | Before | After | Delta | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|---|
| C1 cold-read monitor repair | calibration | `covered=25/64 restraint=6 box3_mismatch=1`, exit 1 at 91edf9cd | `covered=60/64 restraint=6 box3_mismatch=1`, exit 1 | sections 25 → 60 of 64; numeric calibration 6 → 6 (base of round 26 was 8) | `python3 .ufo/evidence/round-27/c1-measure.py --repo CLONE --rev REV` | af7b70daf7754f1d9363669cf9bc97ec01f61f9c | `.ufo/evidence/round-27/c1-before.stdout`, `after/c1-measure-af7b70d.stdout`, ledger append receipts `coldread/append-receipt-{w1,residual}.json` | **missed target (honest stop); calibration still harmed** |
| C2 F8 oracle-anchored survivors | coverage (frontier F8) | `classified=0`, exit 1 at 91edf9cd (frozen and amended counter) | `classified=4 anchored_holes=4`, exit 0 | 0 → 4 classified; F8 open → partly held | `python3 .ufo/evidence/round-27/c2-measure.py --repo CLONE --rev REV` (contract amendment 1, `2227d83`: S012 check reads `used-by`, not `opened`) | af7b70daf7754f1d9363669cf9bc97ec01f61f9c | `after/c2-measure-af7b70d.stdout`, `f8/receipt.json`, `f8/probe-negative-control.stdout` | improved (measured; counter necessary, not sufficient — 3 header-anchored holes, 1 convention-only) |

C1 detail: 51 wave seats cold-read the 39 uncovered sections at `2227d83`;
27 credited and 12 failed with real defects in the page. The L1 corrected
those 12 sections (line counts kept) and 8 residual seats re-read them at
`b1cc95e`: 8 credited, 3 `wrong-expectation` (new wording errors, two of
them introduced by the L1's corrections), 1 `gap-blocking` after the seat
excluded receipts that read the live lane. The 4 uncovered at the head:
"The report shape", "Triggers T1–T3", "Gate/probe registry" (all three
corrected again in `af7b70d`, not re-read) and "Round-21 gate/probe
registry". SHONEN box 3 `[~]` therefore still disagrees with the repo
(mismatch 1). Correction to the round-26 correction above: the
`40a12bf` reading now has its own receipt (`after/c1-measure-40a12bf.stdout`).
Registry at `2227d83` in a fleet mirror: `held=49/49 superseded=7`
(`after/registry-2227d83.stderr`). Census end exit 0.

## Round 28 — cold-read monitor repair, second attempt (2026-10-22)

L1 TameshiR28, attempt 1. One claim.

- **C1 calibration (harm repair, routed by the round-27 closure item 1).**
  Counter `python3 .ufo/evidence/round-27/c1-measure.py --repo CLONE --rev REV`
  (frozen, byte-identical since round 27). Before at base `06b59b93`:
  `covered=60/64 restraint=6 box3_mismatch=1`, exit 1. Target at the landed
  head: `covered=64/64 restraint=8 box3_mismatch=0`, exit 0.

| Claim | Axis | Before | After | Delta | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|---|
| C1 cold-read monitor repair | calibration | `covered=60/64 restraint=6 box3_mismatch=1`, exit 1 at 06b59b93 | `covered=60/64 restraint=6 box3_mismatch=1`, exit 1 | 0 sections; score 6 → 6 | `python3 .ufo/evidence/round-27/c1-measure.py --repo . --rev REV` | a20e2ba00e6903283faf7462993a3898d70f3853 | `.ufo/evidence/round-28/c1-after-ledger.stdout`, `monitor-a20e2ba-explain.json` | missed (honest stop) |

Detail: the round's own `corpus/SOURCES.md` edit (S059 re-open) drifted 10
credited sections, so the content revision `b05d2ee` read 50/64. 38 seats
were dispatched (two fresh readers per uncovered section, plus falsifiers);
12 died on a provider rate limit and 6 were still running at the 19:24Z
cut. 12 cold-read entries were appended (ledger 354 → 366, prefix equal as
data, `git diff --numstat` 668 added / 0 removed). The head reads 60/64:
uncovered "Repeated controls … round 12" (one reader dead, one late),
"Effective expectation … round 14" (the one landed entry records an input
digest that does not match the revision), "Round-18 gate/probe registry"
(both readers dead) and "Round-21 gate/probe registry" (one dead, one
late). Calibration stays harmed against the pre-harm round-26 base
(62/62, restraint 8). SHONEN marks unchanged, all `[~]`.
No other axis claimed; no scalar changes; no retirement.

Round 28 — final reading (appended; the table row above stays as measured at
`a20e2ba`). Three late reports (Read04B, Read05A, Read06A) finished at
19:24Z and were assembled with the first 12 (ledger 354 → 369, appended
from the `b05d2ee` ledger, prefix equal as data). At `c30926e38bc6204f33f33cb84248b7caf27e8324`:
`covered=61/64 restraint=6 box3_mismatch=1`, exit 1
(`.ufo/evidence/round-28/c1-after-final.stdout`). Net over base: 60 → 61
sections, score 6 → 6. Target missed; honest stop.

Round 28 — final reading, second pass (appended). Read09B finished at
19:26Z and was assembled with the other 15 (ledger 354 → 370, appended from
the `b05d2ee` ledger). At `bdf0aa5e4f74273df33db62f7426a685347edb9a`:
`covered=62/64 restraint=6 box3_mismatch=1`, exit 1
(`.ufo/evidence/round-28/c1-after-final2.stdout`). Uncovered: "Round-18
gate/probe registry" (both readers dead) and "Round-21 gate/probe
registry" (one dead, one late). Net over base 60 → 62 sections; score 6 → 6.
Target missed; honest stop.

Round 28 — final reading, third pass (appended). Read14B finished at
19:28Z and was assembled with the other 16 (ledger 354 → 371, appended from
the `b05d2ee` ledger). At `41da22a3d85bf6b8d766ba1e4d3bc5042e205ee6`:
`covered=63/64 restraint=6 box3_mismatch=1`, exit 1
(`.ufo/evidence/round-28/c1-after-final3.stdout`). The Round-21 section,
corrected this round, is now credited. Still uncovered: "Round-18 gate/probe
registry" (both readers dead). Net over base 60 → 63; score 6 → 6. Target
missed; honest stop.

## Round 29 — calibration repair and frontier F6 (2026-10-23)

L1 TameshiR29, attempt 1 (repair-first round). Two claims, frozen in
`.ufo/evidence/round-29/contract.json` (`9f3084bc`) and re-frozen before any data
seat after the control wave: C2 in `contract-amendment-1.json` (`6ab11a62`), C1 in
`contract-amendment-2.json` (`09e4f273`). Every widely read input edit (SOURCES
S024, README Round-29 section, QUALITY 55-57) landed in `9f3084bc`, before the cold
reads (QUALITY 56).

| Claim | Axis | Before | After | Delta | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|---|
| C1 cold-read monitor repair with seat binding | calibration | `covered=63/64 restraint=6 box3_mismatch=1`, PASS false at 367ec0f1 | `covered=64/64 restraint=8 box3_mismatch=0 appended=22 bound=22 prefix_equal=1`, `C1_R29_V2_PASS=true`, exit 0 | restraint 6 → 8; box3_mismatch 1 → 0 | `python3 .ufo/evidence/round-29/c1-measure-v2.py --repo CLONE --rev REV` | 7a45f7b9d6a2542a553276330c8b02ac2e28c7ef | `.ufo/evidence/round-29/c1-at-E.stdout`, `c1-at-D.stdout`, `coldread/select-receipt-w1.json`, `coldread/c1-dry-all32.txt` | improved (measured; one post-data integration step disclosed: 10 passing entries not appended because they fail the frozen binding) |
| C2 F6 survivor fixture minimization (B5) | coverage (frontier F6) | `fixture=absent`, PASS false at 367ec0f1 | `fixture=present anchored=1 kill_original=0 units_original=105 units_minimized=105`, `C2_F6_V2_PASS=false`, exit 1 | none | `python3 .ufo/evidence/round-29/c2-measure-v2.py --repo CLONE --rev REV` | 7a45f7b9d6a2542a553276330c8b02ac2e28c7ef | `.ufo/evidence/round-29/c2-at-E.stdout`, `.ufo/waves/round-29/w1/BuildF6B.md`, `.ufo/waves/round-29/ctl/CriticC2v2.md` | **missed (honest stop)**: target unreachable under the pinned declaration (exec rows declare 755) |

Detail: 36 cold readers (three per drifted section) at `9f3084bc`, no failing
read; ledger 371 → 393 as an append. C2's anchored fixture shows survivor B5 is
masked by the gate's exact-mode check under the pinned declaration
(`corpus/knowledge/survivor-fixture-minimization.md`). Calibration is restored to
the pre-round-26 level (restraint 8). Other axes: depth 9 → 9 (command D),
operability, freshness, adjacency unchanged; no capability row; no retirement.
SHONEN marks unchanged (all `[~]`); box 3 now agrees with the monitor.

## Round 30 — exploratory tally guard, binding v3, credit restored (2026-10-23)

Three attempts (TameshiR30, TameshiR30A2 died with the orchestrator; TameshiR30A3 files). One claim,
exploratory before data (`.ufo/evidence/round-30/contract-amendment-4.json`, `713dee6a`): four counter
versions were each met by a control before data (K7, K8, CtlS2SymEval), so C1 carries no counting
command. Every widely read input edit landed in the content revision `bb681566`.

| Claim | Axis | Before | After | Delta | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|---|
| C1 `--regression` case-tally completeness guard + behavioral selftest (exploratory) | operability | base `9ed6db84`: a tally with one leg dropped prints `REGRESSION: PASS (cases=9 passed=8 …)`, exit 0; selftest 97/97 does not notice | `bb681566`: the same mutant prints `REGRESSION: SETUP (case-tally mismatch: cases=9 counted=8)`, exit 2, and its selftest fails 98/106 | none (exploratory) | none (exploratory; v4 receipt `C1_R30_PASS=true` at `bb681566` is supporting only) | `bb681566b18211adf8ae9c28df91e17678e3f545` (judged object) | `.ufo/waves/round-30/wC/JudgeC1.md`; `corpus/lessons/round-30.md` "After measurement" | `unprovable-but-better` by named non-author seat JudgeC1 (reviewer), reasons on record |

Detail: calibration no-harm monitor `covered=64/64 restraint=8 box3_mismatch=0` at base → 33/64 at
`bb681566` (input drift by design) → 64/64, restraint 8, box3_mismatch 0 at `4df5107f` after 22 fresh
cold readers (63 entries, ledger 393 → 456, binding v3 63/63, audit 211/211 traces). Calibration 8 → 8,
depth 9 → 9 (command D), coverage, freshness, adjacency unchanged; operability carries C1's exploratory
verdict, not a number. No capability row; no retirement. SHONEN marks unchanged (all `[~]`). Eight
selftest survivors of the new guard (MutateHead) and binding v4 are routed to round 31.

## Round 31 — standing self-assessment re-stated (calibration claim C1, 2026-10-23)

L1 TameshiR31, attempt 1. One measured claim, frozen with its counter, predicate, target and
kill rule in `.ufo/evidence/round-31/contract.json` at `c111dab5` before any data seat.

- **C1 calibration.** Surface: the standing rows of this file's `| Capability |` and
  `| Axis | Score (0–10) |` tables. Predicate (label `C1_R31_PASS`): for each of the 12 frozen
  statements, the last row of its table type states the values its frozen command prints at
  REV, and the base `SCORECARD.md` stays a byte prefix. Counter
  `python3 .ufo/evidence/round-31/c1-measure.py --rev REV --work EMPTY_DIR`. Before at base
  `36c1d393`: `mismatches=7` of 12, `C1_R31_PASS=false`, exit 1
  (`.ufo/evidence/round-31/before/c1-at-base.stdout`). Target: `mismatches=0`, PASS true.
  Measurement protocol (stated before the after-run): the after-value is the first full counter
  run at the measurement revision; every other run, by the L1 or a seat, is reported as observed.

Erratum to the round-30 block above (append-only; the block stays as written): its C1 row calls
JudgeC1 a "named non-author seat". JudgeC1 was dispatched by the lane's L1 and is still the lane
(LEARNING.md §Discernment; AXES.md). The non-author `unprovable-but-better` ruling on round-30 C1
is the hyaku closure's own (`corpus/lessons/round-30-verifier-spotcheck.md:47-84`); JudgeC1's
report is supporting evidence only.

### Current standing capabilities — re-stated at round 31

This table is the current statement for every capability named in it. It supersedes the counts
of the `| Capability |` table above (whose rows stay as written, as dated literals), the round-17
supersession line ("At round 17: … 95/95 … `cases=7` … 56/56"), which was itself stale at base,
and the three `| capabilities addition |` rows of rounds 23–25 for the values it states. Values
are what each command prints at the round-31 measurement revision named in the measured-result
row below; the first-working rounds are unchanged.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | curate where the lane learns: opened, tiered, rechecked source rows, mined into admitted entries, census-gated | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → exit 0, 94 rows, `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`; `corpus/SOURCES.md` | fleet round 1 (kaika) |
| mutation sweep runner | inject → run → restore single-edit mutants with a green-control gate, verdict lines and byte-identity proof; `--regression` refuses a miscounted tally (round 30) | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 106/106 pass`, exit 0 | historical round 3; re-demonstrated round 31 |
| six-leg regression ledger | replay every recorded mutation case (nine legs since round 26; the name is kept as the row id) at its pinned blob; exact expectation | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=9 passed=9 …)`, exit 0 | historical round 7 (four legs) / round 10 (six) / round 26 (nine) |
| repeated pristine-control gate | observe N≥3 exact exit/stdout/stderr tuples, distinguish mismatch from unavailable/uniform-nonzero baseline, validate digest-pinned observation snapshots | `python3 tools/repeat-control.py --selftest` → PASS (29 cases), exit 0 | round 12 |
| six-leg content-disposition probe | emit configured-pin, committed-HEAD and worktree SHA observations for every recorded leg, while explicitly withholding verdict reuse | `python3 tools/pin-disposition.py --selftest` → 19/19 PASS0 | round 13 |
| exposed witness provenance correction | validate a new digest-anchored non-blind companion without rewriting frozen observations | `python3 tools/witness-metadata.py --selftest`: metadata selftest39/39 PASS0 | round 13 |
| effective expectation reconciliation | account for every historical expected row, reject an exit-only setup crash, and preserve that raw failure under a checked explicit oracle supersession | `python3 tools/evidence-disposition.py --selftest` → PASS66/66 exit0 | round 14 |
| retained invocation-context gate | re-derive bounded raw receipt predicates, check byte-pinned frozen receipts, and distinguish semantic mismatch from unavailable/tampered input through a standalone public-CLI selftest | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72` → exit0, copied-source CLI selftest49/49 | round 15 |
| hermetic env-differential probe | classify the raw exit/stdout/stderr tuple of nine pinned selftests under seven explicit profiles; the committed receipt `.ufo/evidence/round-21/f5/receipt-initial.json` classes eight `invariant` and one `nondeterministic` (`js-round-gate`), not "raw-output-variable" as the row above says | `python3 tools/env-diff.py --selftest` actual9/9 (`ENVDIFF_SELFTEST: 9/9 pass`) | round 21 |
| callback-authoritative wave accounting | reconcile exact registered identities and terminal states while preserving failed seats' partial artifacts; reject mismatched totals and digest tampering | `python3 tools/wave-accounting.py --selftest` → frozen counter8/8 (`ACCOUNTING_SELFTEST: 8/8 pass`; extra cases `ACCOUNTING_EXTRA_SELFTEST: 16/16 pass`) | round 22 |
| required-command-receipt-binding | validate a finite trusted bundle's exact named command/context/outcome declarations | `python3 tools/command-binding.py --selftest` → `COMMAND_BINDING_SELFTEST: 44/44 pass`, exit 0 (not a C1 statement) | round 23 |
| refusing-registry-replay | replay frozen registry requirements and refuse to publish a binding bundle from rejected rows | `python3 tools/registry-replay.py --selftest` → `REGISTRY_REPLAY_SELFTEST: 10/10 pass`, exit 0 (not a C1 statement) | round 24 |
| mutation report interop | emit each recorded leg as a mutation-testing-elements report and check it with the official schema and metrics library | `python3 tools/mte-interop.py --selftest` → `MTE_SELFTEST: 17/17 pass`, exit 0 at round 33 (jsonschema 4.25.1 installed via uv; `.ufo/evidence/round-33/repair/mte-selftest.{stdout,exit}`); supersedes the round-31 'not runnable here' clause | round 25 |

### Current axes — re-stated at round 31

Supersedes the fleet round-1 baseline table above for current values (that table stays as the
pre-round record of `284ab0f`) and the Saturation sentence "the nudge does not fire now (depth 6 <
8; …)": depth is 9 and calibration 8, both at or above the declared saturation line 8/10.

| Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
|---|---|---|---|---|
| depth | 9 | One point per recorded mutation case in the runner's ledger comment (`tools/mutate-and-run.sh:87-95`, nine legs), capped at 10; command D above prints `recorded_cases=9 depth_score=9` | round-31 measurement revision (measured-result row below) | 26 |
| calibration | 8 | Restraint score of the strict cold-read monitor `python3 .ufo/evidence/round-21/coldread/measure.py --repo R --rev REV` (`calibration_restraint_score`): two points per restrained, evidence-linked `[~]` SHONEN box (`SHONEN.md:5-12`), box 3 only when the monitor credits the full page; the last 2 points need independent promotion review | round-31 measurement revision (measured-result row below) | 29 (restored 6 → 8); held 30 |

Measured results are appended below only after execution.

### Round 31 — measured result (TameshiR31)

| Claim | Axis | Before | After | Delta | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|---|
| C1 standing SCORECARD rows agree with their own commands | calibration | `C1_R31: statements=12 mismatches=7 … append_only=1 C1_R31_PASS=false`, exit 1 at 36c1d393 | `C1_R31: statements=12 mismatches=0 unparsed=0 unobservable=0 append_only=1 C1_R31_PASS=true`, exit 0 | mismatches 7 → 0 of 12; numeric calibration 8 → 8 | `python3 .ufo/evidence/round-31/c1-measure.py --rev REV --work EMPTY_DIR` | 83c001a5d95f33a78a9e2d51f5ec1c9a6ddf2217 (first full run; re-measured at the round's last SCORECARD commit, receipt `.ufo/evidence/round-31/after/c1-at-final.stdout`) | `.ufo/evidence/round-31/before/c1-at-base.stdout`, `after/c1-at-83c001a5.stdout`, `ctl/c1-controls-summary.txt`, `.ufo/waves/round-31/w1/`, `w2/` | improved (measured; route controls that copy correct committed values also meet the counter, as the contract declared; of the 7 base mismatches, 3 were stale current statements and 4 dated literals without a current restatement) |

The "round-31 measurement revision" cells of the re-stated tables above mean `83c001a5`. No-harm at
`83c001a5`: `C1_MONITOR: covered=64/64 restraint=8 box3_mismatch=0 depth_score=9` (content revision
`2da841bd`: 55/64, restraint 6, by design; 24 fresh cold-read entries bound by binding v5 and appended,
ledger 456 → 480). Depth 9 → 9 (command D); coverage: one new lane entry
(`corpus/knowledge/executable-self-assessment.md`, not a frontier move); operability, freshness,
adjacency unchanged (tools unchanged). No capability row; no retirement. SHONEN marks unchanged (all
`[~]`). Lesson: `corpus/lessons/round-31.md`.

## Round 32 — runner tally audit (operability, capability acquisition C1, 2026-10-23)

L1 TameshiR32, attempt 1. Stagnation nudge: depth 9 and calibration 8 sit at or above the saturation
line 8, and no capability row has entered since round 25 (window 2), so the lowest-axis obligation is
waived and the round is a capability move. One measured claim:

- **C1 operability, capability acquisition.** Surface: a new versioned tool `tools/tally-audit.py`
  that audits `tools/mutate-and-run.sh` without editing it (per-leg presence of the `--regression`
  tally, the tally block against an oracle over every status 0–255 with stress, and the runner's own
  tally harness against a panel of faulty blocks). It closes the runner items deferred since round 30
  (per-leg tally check; the eight MutateHead selftest survivors). The runner stays byte-identical
  (sha256 `a7d3f2dd…2eb9`). Counter v1 (`.ufo/evidence/round-32/c1-measure.py`, frozen `c3181497`)
  was met before data by control seat CriticC1's allowlist, so the claim was re-designed before data:
  counter v2 (`.ufo/evidence/round-32/v2/c1-measure-v2.py`, amendment 1 `b50a18f0`, amendment 2
  `528f8dee`) runs the tool in a sandbox, pins the tool bytes (sha256 `9639c458…99ef`) and adds a
  sealed held-out set written by seats after the freeze. Predicate label `C1_R32V2_PASS`. Before at
  base `e24688b2`: no tool (v1 receipt `before/c1-at-base.stdout`, `kill=0/18 accept=0/8`, false).
  Target: `C1_R32V2_PASS=true` with every valid held-out copy right and at least 6 of each kind.

Repairs routed by `corpus/lessons/round-31-verifier-spotcheck.md`: counter v2 of the round-31 C1
counter with the exact `Score (0–10)` header and a byte-prefix append-only test
(`.ufo/evidence/round-32/repair/c1-r31-measure-v2.py`; the frozen round-31 counter is unchanged); a
round-31 base monitor receipt (`repair/c1monitor-at-r31-base-36c1d393.*`, `covered=64/64 restraint=8`);
command D receipts with exit files at `67c0e013` and `08125328` (`repair/commandD-at-r31-*`; the
round-31 receipt without an exit stays as written). Measured results are appended below only after
execution.

### Round 32 — measured result (TameshiR32)

| Claim | Axis | Before | After | Delta | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|---|
| C1 runner tally audit (`tools/tally-audit.py`, sha256 `9639c458…99ef`) | operability (capability acquisition) | no tool at base `e24688b2` (v1 receipt `kill=0/18 accept=0/8`, false) | `C1_R32V2: v1_kill=18/18 v1_accept=8/8 ho_kill=1/10 ho_accept=8/12 ho_invalid=0 tool_sha_ok=1 runner_sha_ok=1 heldout_after_freeze=1 seed=63d2e2e95a1e35c5 … C1_R32V2_PASS=false`, exit 1 | sealed held-out set: 9 of 10 must-kill copies passed by the tool, 4 of 12 must-accept copies rejected | `python3 .ufo/evidence/round-32/v2/c1-measure-v2.py --lane LANE --rev REV --work EMPTY_DIR` | 24a5a5bb598ae919546715267d76f814efaf8912 (first full v2 run) | `.ufo/evidence/round-32/after/c1v2-at-measurement.{stdout,exit}`, `heldout/`, `.ufo/waves/round-32/w2/HeldOut*.md` | **miss** (kill rule: the first full run decides; not re-scaled, re-seeded or amended) |

No capability row enters the table: the tool does not meet its own frozen predicate. It meets the public
v1 fixtures (18/18, 8/8) and fails the sealed copies written after its freeze, which is the gap the v1
control finding predicted. Causes named by the held-out authors: the runtime sweep never produces 3–8
failing or setup legs (HeldOutPrintf, HeldOutGuard, HeldOutTallyArms), per-position statuses stop at
`1 2 3 4 126 127 255` (HeldOutRefactor k1), the stress rewrites the first leg-status loop rather than the
tally loop (HeldOutRefactor a4, HeldOutLoop), and harness extraction refuses a second extraction line
(HeldOutRefactor a3). No harm: runner sha256 unchanged at `24a5a5bb`; strict monitor
`C1_MONITOR: covered=64/64 restraint=8 box3_mismatch=0 depth_score=9` there
(`after/c1monitor-at-24a5a5bb.stdout`; content revision `a4f71813` read 59/64 by design, 13 fresh bound
cold reads appended, ledger 480 → 493); command D `recorded_cases=9 depth_score=9`. Numeric scores:
depth 9 → 9, calibration 8 → 8. SHONEN marks unchanged (all `[~]`).

Errata (append-only): the round-32 block above and `contract.json` say the runner is an input of 270 of
480 ledger entries; at `a4f71813` it is 282 of 480 (seats ReviewEntry, ReviewScorecardLog; 270 of 456 was
the round-31 count). The amendment-1 control re-score with counter v2 was not run before the L1's first v2
run; it was run afterwards as an observation (`.ufo/waves/round-32/res/CtlV2Controls.md`).

### Current standing capabilities — changed row re-stated at round 32

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | curate where the lane learns: opened, tiered, rechecked source rows, mined into admitted entries, census-gated | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → exit 0, `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`; row count from the re-derivable command `grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md` → 99 rows at round 35 (the "96 rows" this cell carried was a round-32 observation; corrected 2026-10-23, round 35, per r34 AllFourScorecard F1); `corpus/SOURCES.md` | fleet round 1 (kaika) |

## Round 33 — C2 freshness repair (measured) + C1 tool hardening frozen unmeasured (2026-10-23)

L1 TameshiR33, attempt 2 (attempt 1 died with the phase-4 orchestrator; nothing inherited).
Stagnation nudge still applies (no capability since round 25). Two claims frozen at `f6d8a891`
(contract `.ufo/evidence/round-33/contract.json`); five pre-data amendments followed the wave-1
falsification seats (`27902a16`, `e6a5f4b`, `49876298`, `ee398492`; all disclosed in
`corpus/lessons/round-33.md`; no default-mode counter run occurred before them).

| Claim | Axis | Before | After | Delta | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|---|
| C2 S055 supersedes-row with versioned pin | freshness | `C2_R33: row=none versioned_url=0 snapshot_sha_ok=0 gate_sha_ok=0 quote_ok=0 C2_R33_PASS=false`, exit 1 at base `66e1fb44` (`.ufo/evidence/round-33/before/c2-at-base-v2.*`) | `C2_R33: row=S100 versioned_url=1 snapshot_sha_ok=1 gate_sha_ok=1 quote_ok=1 C2_R33_PASS=true`, exit 0 | row none → S100; the moving /3/ pin is replaced by committed bytes (216574 B, sha256 217edd57…4899) that no live footer churn can break | `python3 .ufo/evidence/round-33/c2/c2-measure.py --lane LANE --rev REV` | see `.ufo/evidence/round-33/after/c2-at-head.stdout` (this commit) | `corpus/SOURCES.md` row S100; snapshot `.ufo/evidence/round-33/c2/doctest-snapshot.html`; fetch receipt; lesson Gate | **improved (measured)** |
| C1 runner tally audit v2 (capability acquisition) | operability | no `tools/tally-audit-v2.py` at base; frozen counter before-state `tool_present=0 … C1_R33_PASS=false`, exit 1 | measurement NOT RUN: the sealed held-out set (>=8 must-kill + >=6 must-accept authored after the freeze) was never authored — the orchestrator's 2 h freeze redirected the round to an honest landing. Tool hardened pre-data by nine seat findings (config sweep, co-occurrence vectors x 15158, nesting-aware extraction, loop dataflow, harness panel +5, twice-only head rule, boundary repair); routed residue named in the lesson | none — no verdict consumed | `python3 .ufo/evidence/round-33/c1/c1-measure.py --lane LANE --rev REV --work EMPTY_DIR` | n/a (not run against the predicate) | `.ufo/evidence/round-33/after/c1-at-head-notrun.stdout` (structural false: ho 0/0), lesson `## Gate` rejection row | **unverified this round (honest stop; routed to round 34)** |

C1 detail: wave 1 (33 seats, zero dead) ran only pre-data attacks. All four control shortcuts were
caught by the frozen counter (receipt planned at the round-34 measurement; the four seat ctl.py
files and their scratch receipts are named in the lesson). No capability row enters the standing
table for C1 (the tool never ran against its predicate); the existing rows are untouched. Numeric
axes: depth 9 → 9 (command D, runner byte-identical), calibration monitor at the freeze baseline
64/64 restraint 8; this round's records (lesson, SCORECARD, LOG, SOURCES row) drift monitor sections
— re-crediting is routed to round 34's first wave (LedgerAudit sized ~19 SOURCES-citing sections +
3 all-four); the drifted-section reading at the head is recorded in the report. mte-interop SETUP
repaired (jsonschema 4.25.1 via uv, `MTE_SELFTEST: 17/17 pass`, receipt
`.ufo/evidence/round-33/repair/`); the round-31 re-stated row's 'not runnable here' clause is
superseded by this round's row below. Freshness carries the round's only score move.

## Round 34 — C1 tally-audit-v2 measured true (capability admitted) + frontier (2026-10-23)

L1 TameshiR34, attempt 1. Single claim, routed from the round-33 honest-stop closure; the
stagnation nudge is discharged by this capability admission (no capability since round 25).

| Claim | Axis | Before | After | Delta | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|---|
| C1 runner tally audit v2 (capability acquisition, routed measurement) | operability | `tool_present=1 … controls_ok=0(receipt-missing) v1_kill=0/0 v1_accept=0/0 ho_kill=0/0 ho_accept=0/0 ho_invalid=0 heldout_after_freeze=0 C1_R33_PASS=false`, exit 1 at `732b6860` (r33 head, not-run structural false, `.ufo/evidence/round-33/after/c1-at-head-notrun.*`) | `tool_present=1 tool_sha_ok=1 runner_sha_ok=1 controls_ok=1(ok) v1_kill=18/18 v1_accept=8/8 ho_kill=8/8 ho_accept=6/6 ho_invalid=0 heldout_after_freeze=1 seed=685f63bd25263908 rev=c17e593b51802dd4ed568da3265f21c6d00c4273 C1_R33_PASS=true`, exit 0 | the capability now runs and verifies: tool at the frozen pin 7b11ba25…8d10 kills 18/18 public + 8/8 sealed must-kill and accepts 8/8 public + 6/6 sealed must-accept with zero invalid sealed copies, controls receipt attesting the amended counter committed pre-data | `python3 .ufo/evidence/round-33/c1/c1-measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev c17e593b51802dd4ed568da3265f21c6d00c4273 --work EMPTY_DIR` | `c17e593b51802dd4ed568da3265f21c6d00c4273` (measurement revision) | `.ufo/evidence/round-34/measure/c1-deciding-run.{stdout,exit}`; sealed set `.ufo/evidence/round-33/heldout/` (8 kill + 6 accept, per-copy authoring receipts `round-34/dev/authoring-receipts.json`); controls receipt `.ufo/evidence/round-33/c1/controls-receipt.json` minted at `6aaad5b3`; amendment 6 disclosed in `contract-amendments.json` | **improved (measured)** |

Pre-data amendment 6 (`6aaad5b3`): the counter's sealed-copy witness gate made set-aware BEFORE
any sealed authoring (routed RevengerWitness rule; the frozen set-blind rule was voidable in both
directions by cosmetic clones — kill+head accepted inert head edits, accept+vector demanded a!=b
from equivalence copies). Probe battery 8/8 exact; panel 18/18 + 8/8 re-confirmed; tool selftest
22/22. Kill rule honored: exactly one full default-mode run at the measurement revision; no
re-seed, no re-scale, no post-data rule change. The deciding run receipt is the only
`C1_R33_PASS=true` counter output on record.

Capabilities table — row admitted this round:

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| tally-audit-v2 runner audit | audit the mutation runner's regression tally without editing it: head/static/runtime/harness checks kill all 18 public + 8 sealed must-kill copies and accept all 8 public + 6 sealed must-accept copies, zero invalid sealed copies, controls-gated counter | deciding-run receipt `C1_R33: … v1_kill=18/18 v1_accept=8/8 ho_kill=8/8 ho_accept=6/6 ho_invalid=0 … C1_R33_PASS=true` at `c17e593b`, counter `.ufo/evidence/round-33/c1/c1-measure.py`, tool `tools/tally-audit-v2.py` @ `7b11ba25…8d10` | round 34 (tool landed round 33, predicate honestly not decided there) |

Numeric axes: depth 9 → 9 (command D, runner byte-identical at the pinned sha); calibration
monitor sections (this block, LOG, lesson) — re-crediting rides in the r34 wave per the r33
closure routing. Freshness carries S101 (Major Mutation Framework — equivalent mutants
first-class; row + committed snapshot in round-34 evidence; the gnu.org/TLDP bash-exit-status
duplicates of S097's scope rejected, recorded in the round-34 lesson Gate). No owned axis score
lowered; no axis harmed.

**Planned (round 35):** the v3 residue classes ride in `corpus/lessons/round-34.md` Holds
(Guard-2 divisibility, TallyArms-02 coexistence, quoted case subject, helper-function refactors,
per-index record parsing, preamble seeding, nonzero-leg stress, all-pairs nlegs recompute) —
each adoptable only under the freeze-before-data discipline; tool re-pin and counter re-attest
required if any lands pre-data.

## Round 35 — tally-audit-v3 measured true (four configs, whole stdout, comment-blind) + C2 six-class record repair (2026-10-23)

L1 TameshiR35, attempt 3. Attempts 1-2 died with the orchestrator session before the report; their
apparatus (A4-A8), the 64-seat wave-1 spec, the 58-seat wave-2 wave and the deciding receipt are
inherited, re-verified and cited. Contract `.ufo/evidence/round-35/contract.json`; every amendment
A1-A8 is pre-data (no default-mode C1 run before A8). Two claims, each with its own counter; no
stagnation waiver is claimed (calibration carries the round, and a capability entered the table at
round 34). Axis names follow the surface the round changed, not the number it prints. The round
report is landed by the fresh-claim respawn (hyaku run-5, after the stale-claim reset; watchdog
`lane-dead-no-report tameshi round=35` ×8 on 2026-10-23), which re-ran the census gate and both
counters at write time against the inherited commits and folded this record.

| Claim | Axis | Before | After | Delta | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|---|
| C1 capability acquisition: `tools/tally-audit-v3.py` audits the runner tally over all four `(root,auto,KEEP)` triples, compares the FULL stdout plus exit, and scans a comment-blinded code view | depth (declared surface), operability (runnable artifact) | `C1_R35: mode=before tool_present=0 runner_sha_ok=1 rev=51d3f08073be65d3475cf0286042fc0dbe4c4a7d C1_R35_PASS=false`, exit 1 — no v3 tool at base (`.ufo/evidence/round-35/before/c1-at-base.stdout`) | `C1_R35: mode=deciding tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=34fa5b0cfe909f3cde644676ead723256281dd05 C1_R35_PASS=true`, exit 0 | 16/16 copies scored as declared where the do-nothing control scores 0/6 kill and 0/3 accept; the capability runs and verifies | `python3 .ufo/evidence/round-35/c1/c1-measure.py --lane LANE --rev REV --work EMPTY_DIR --sealed .ufo/evidence/round-35/c1/sealed` | `34fa5b0cfe909f3cde644676ead723256281dd05` (deciding receipt, one run, `after/c1-at-34fa5b0…stdout` committed by this round's landing commit) | `after/c1-at-34fa5b0…stdout`, `control/c1-v2-control.stdout` (v2 on the same nine copies: `pub_kill=0/6 pub_accept=0/3 … C1_R35_CONTROL_PASS=false`, exit 1), `control/c1-v3-public-rehearsal.stdout`, `lessons/selftest-33.out` (`TALLY_AUDIT_V3_SELFTEST: 33/33 pass`), sealed manifest with 7 copies (4 kill / 3 accept) authored after the freeze `d16f9b5a` | **improved (measured)**; two disclosed predicate defects routed (below) |
| C2 six declared self-assessment mismatch classes (m1 header trio, m2 README index, m3 stranded seat file, m4 frozen-contract pin, m5 round-34 authoring adjudication, m6 standing sources-registry row count) | calibration | `C2_R35: m1=8 m2=3 m3=1 m4=1 m5=1 m6=1 total=15 entries=40 sources_rows=98 rev=51d3f080… C2_R35_PASS=false`, exit 1 (`.ufo/evidence/round-35/before/c2-at-base.stdout`) | `C2_R35: m1=0 m2=0 m3=0 m4=0 m5=0 m6=0 total=0 entries=40 sources_rows=99 rev=34fa5b0c… C2_R35_PASS=true`, exit 0, and independently re-derived by hand class-by-class in the residual wave (`ResidualReviewC2.md`, six-row table, all agree) | 15 → 0 mismatches across six classes | `python3 .ufo/evidence/round-35/c2/c2-measure.py --lane LANE --rev REV --fleet FLEET` | `34fa5b0cfe909f3cde644676ead723256281dd05` (first after at `d16f9b5a`, re-run at the tip; `after/c2-at-d16f9b5a.stdout`, `after/c2-at-34fa5b0…stdout`) | `before/c2-at-base.stdout`, `after/c2-at-d16f9b5a.stdout`, `.ufo/waves/round-35/residual/ResidualReviewC2.md`, lesson `## Mistakes` 1-2 | **improved (measured)** |

Pre-data controls. C1: the do-nothing control (keep v2, same nine copies) is `0/6` kill and `0/3`
accept, exit 1 — it cannot reach the target. C2: the base state is its own control (every class
non-zero). Both receipts are committed. Kill rule honored: exactly ONE default-mode C1 run, at
`34fa5b0` after the sealed set landed; every other receipt is `mode=before` or `mode=control`.

Capabilities table — row admitted this round:

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| tally-audit-v3 runner audit | audit the runner's regression tally without editing it, across all four `(root,auto,KEEP)` triples, comparing the FULL stdout plus exit and scanning a comment-blinded code view; kills 6/6 public + 4/4 sealed must-kill copies (failing check exactly `runtime`), accepts 3/3 public + 3/3 sealed must-accept copies, zero invalid sealed copies, under a pinned sha256 | deciding receipt `C1_R35: … pub_kill=6/6 … ho_kill=4/4 ho_accept=3/3 ho_invalid=0 … C1_R35_PASS=true` at `34fa5b0`, counter `.ufo/evidence/round-35/c1/c1-measure.py` @ `d360a159…`, tool `tools/tally-audit-v3.py` @ `6188db16…` | round 35 |

Numeric axes, measured. **depth 9 → 9**: command D at the tip prints `recorded_cases=9 depth_score=9`
(the rubric counts recorded ledger legs; the runner is byte-identical `a7d3f2dd…` at base and tip, so
no tenth leg and no numeric move — the C1 gain is a capability and a wider audit surface, not a ledger
count). **calibration 8 → 6**: the strict cold-read monitor
`python3 .ufo/evidence/round-21/coldread/measure.py --repo . --rev REV` prints
`calibration_restraint_score: 8, sections_covered 64/64` at the round base `51d3f08` and
`calibration_restraint_score: 6, sections_covered 60/64` at the tip `34fa5b0`; four SKILL headings
("Mutation-sweep recipe", "Restore discipline", "### The map", "### Where to enter") have cited
inputs that this round's record repairs rewrote (`corpus/SOURCES.md`, `corpus/README.md`, the
knowledge headers, `SCORECARD.md`, `corpus/QUALITY.md`), so the frozen ledger withholds their credit
by its input-drift rule (the monitor working as designed — the exception is recorded in the lesson
`## Holds`). The stale `8` this file carried from round 29-34 is superseded by the measured `6`; a
cold-read refresh is routed to round 36. C2's own counter is independent of that instrument and reads
`total=0`.

Disclosed predicate defects (no rule was changed after data; both routed, not patched):
1. The counter's PASS expression (`c1-measure.py:517`) requires `pub_kill == pub_kill_slots` and
   `pub_accept == pub_accept_slots` but not the slot totals 6/3 nor `pub_distinct == 9`, so an empty
   panel would satisfy the code; the receipt meets the stronger declared target
   (`pub_kill=6/6 pub_accept=3/3 pub_distinct=9`), and the divergence is a counter defect for round 36
   (residual seat `ResidualCriticPredicate` §1, MAJOR).
2. Clause (3) of C1's surface ("every structural scan runs on a comment-blinded code view") is not
   universal: `code_view` fails to blank a comment that follows an ANSI-C `$'…'` quote (same seat §4,
   MAJOR; already an open class in the lesson `## Holds`, first filed by wave-2 seat AttackQuotedHash).
   The claim stays scoped to the enumerated 16 copies; no universal lexical claim is made or admitted.

**Planned (round 36):** cold-read refresh for the four drifted headings (restores calibration credit
against the rewritten inputs); public-slot cardinality and distinctness asserts in a successor counter
(frozen pre-data, then one deciding run); a real shell lexer or an enumerated supported-form list for
`code_view`; the open recall classes in the lesson `## Holds`.

## Round 36 — cold-read refresh (calibration 6 → 8) + counter cardinality successor (depth surface) (2026-10-24)

L1 TameshiR36, attempt 1. Two claims, distinct axes; calibration is the lane's lowest
non-retired axis (pinned 6 at round 35) and carries C1. Contract
`.ufo/evidence/round-36/contract.json`, frozen before any data run (C2 counter sha256
`9eb8944c…` recorded there). Both claims are the round-35 closure's routed defects
(dead-pointer correction lands in LOG.md this round; `code_view` routed defect 3 is
explicitly NOT taken — editing `tools/tally-audit-v3.py` would void the round-35 capability
pin; planned for round 37).

| Claim | Axis | Before | After | Delta | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|---|
| C1 cold-read monitor refresh of the four round-35-drifted headings (recipe, restore discipline, the map, where to enter) | calibration (lowest axis) | `calibration_restraint_score: 6, sections_covered 60/64` at r35 tip `796e08b` (`.ufo/evidence/round-36/after/monitor-at-796e08b.stdout`) | target `calibration_restraint_score: 8, sections_covered 64/64` at the round-36 refresh commit | 6 → 8; 60/64 → 64/64 | `python3 .ufo/evidence/round-21/coldread/measure.py --repo . --rev REV` | the round-36 refresh commit — hash named in the `monitor-at-<rev>.stdout` receipt filename and the round-36 report | `.ufo/evidence/round-36/coldread/` (traces `traces/L1/`, four new ledger entries in `.ufo/evidence/round-21/coldread/ledger.json`, `refresh-specs.json`, `refresh-receipts.json`); do-nothing control `control/monitor-at-content-commit.*` (record edits without the ledger refresh still print 6); lesson `corpus/lessons/round-36.md` | measured (receipt at the refresh commit) |
| C2 successor counter `c1-measure-v2.py`: frozen public-slot cardinality + distinctness asserts over the round-35 tally-audit panel | depth (surface: the tally-audit counter's predicate completeness) | the frozen v1 counter accepts an emptied (zero-slot) public panel vacuously: `C1_R35: … pub_kill=0/0 pub_accept=0/0 … C1_R35_PASS=true`, exit 0 (`.ufo/evidence/round-36/control/v1-at-emptypanel.stdout` — the r35-closure-disclosed predicate defect, now demonstrated) | v2 fails the same emptied panel (`C1_R36V2: … pub_kill_slots=0 … C1_R36V2_PASS=false`, exit 1, `control/v2-at-emptypanel.stdout`) and passes the full deciding re-run at the refresh commit (`pub_kill=6/6 pub_accept=3/3 pub_distinct=9 … C1_R36V2_PASS=true`, exit 0, `after/c1v2-at-<rev>.stdout`) | the vacuous-accept class is closed; the round-35 16/16 verdicts re-confirmed under the stronger predicate | `python3 .ufo/evidence/round-36/c1/c1-measure-v2.py --lane LANE --rev REV --work EMPTY_DIR --sealed .ufo/evidence/round-35/c1/sealed` | the round-36 refresh commit (hash in the `c1v2-at-<rev>.stdout` receipt filename and the report) | `.ufo/evidence/round-36/c1/c1-measure-v2.py` @ `9eb8944c…` (frozen in `contract.json`); parent v1 counter unchanged; lesson `corpus/lessons/round-36.md` | measured (one deciding run, kill rule honored) |

Pre-data controls. C1: the do-nothing control is the same monitor command at the round-36
content commit (every record edit landed, the ledger refresh did not): it must still print
6 — record edits alone cannot restore credit. C2: the do-nothing control is the frozen v1
counter on the emptied-panel mutant: it prints PASS=true, proving a no-fix path "meets" a
vacuous target while v2 fails it. Both receipts are committed under
`.ufo/evidence/round-36/control/`. Kill rule honored: exactly ONE default-mode v2 deciding
run, at the refresh commit; every other v2/v1 run is a control or the before demonstration.

Numeric axes, measured. **depth 9 → 9**: command D at the refresh commit prints
`recorded_cases=9 depth_score=9` (the runner is byte-identical `a7d3f2dd…`; C2's gain is
predicate completeness, not a ledger count). **calibration 6 → 8**: the strict cold-read
monitor prints `calibration_restraint_score: 6, sections_covered 60/64` at base `796e08b`
and `8, 64/64` at the refresh commit — the four round-35-drifted headings are re-anchored by
L1 author source reads (trace receipts + ledger entries), the round-21 refresh protocol;
the scope line of that protocol ("input-keyed source reads only; not independent/blind
cold-read, recipe re-execution or required-command coverage") is carried verbatim in the
round-36 refresh receipts. The r35 numeric block's measured `6` is superseded by this
measured `8` at the refresh commit; record-keeping commits after the refresh commit that
touch the four headings' cited inputs re-trigger the instrument's input-drift rule by
design (as at round 35), so the pinned measurement commit is the refresh commit itself.

Routed repair (r35 closure defect 1): LOG.md round-35 entry's `ResidualSentinelClosure.md`
pointer — no such file ever committed; corrected by an append-only round-36 entry naming
the five real residual reports. Frontier: S103 opened and mined (see LOG + lesson Gate).
Capabilities table: no new row (the v2 counter is a successor audit predicate, not a new
repertoire capability).

**Planned (round 37):** the `code_view` ANSI-C `$'…'` quote class (routed defect 3) under
the freeze-before-data discipline with a tool re-pin and counter re-attest (real shell
lexer or enumerated supported-form list); the open recall classes in the round-35 lesson
`## Holds`; the two prepared round-36 waves' findings once the orchestrator dispatches them.

### Round 36 control-input erratum (round 37)

The round-36 empty-panel stdout files remain historical outputs, but their `rev=91373d55557fe26c431e9e3dd9e8fa4a00d7b57f` input is not an object in this lane (`git cat-file -e` fails at the r36 tip `d9c496b19371b779ce0eec6dfee1b049b27a3a2d`). The closure-routed control is now reconstructed from the committed tree/spec at `.ufo/evidence/round-37/control/empty-panel/manifest.json`: source panel tree `4f3d8af5b62ba04a5ff825bfdaec6c9193f8489e`, nine committed specimens, deterministic empty-panel input. The replay receipt `.ufo/evidence/round-37/control/replay-at-final-fixed.stdout` runs the frozen v1/v2 counters at the resolvable counter revision and reads the committed panel tree at its resolvable panel revision. This correction does not rewrite the r36 receipts.

### Round 36 control-mode erratum (round 37)

The historical r36 empty-panel receipts (`.ufo/evidence/round-36/control/v1-at-emptypanel.stdout:8` and `.ufo/evidence/round-36/control/v2-at-emptypanel.stdout:8`) use the default `mode=deciding` label although they are mutant controls. The frozen counters support `--tool` control mode; the r37 replay now passes the identical committed tool bytes explicitly, verifies the frozen SHA-256, and requires `mode=control` with `C1_R35_CONTROL_PASS=true` / `C1_R36V2_CONTROL_PASS=false`. `.ufo/evidence/round-37/control/replay-at-final-control.stdout` is the authoritative explicit-mode receipt; the earlier r37 attempt remains historical.

### Round 36 scorecard/control-pointer errata (round 37)

The round-36 C1 table's `control/monitor-at-content-commit.*` shorthand does not name a committed file; the actual control receipts are `.ufo/evidence/round-36/control/monitor-at-e423c41b.{stdout,stderr,exit}`. The r36 `Numeric axes, measured` prose was already present at content revision `e423c41ba253357ab8c8513f0376dad9d38ab248`, before the after run. Read its `8, 64/64` sentence at that revision as a pre-registered target, not an observed result; the measured result is the committed `.ufo/evidence/round-36/after/monitor-at-b455001e.stdout` at `b455001e2589b3f4f471d94a3de7e5e549b9f54c`, reproduced at the r36 tip in the non-author spot-check. This corrects evidence timing and path wording only; the verified 6 → 8 result is unchanged.



## Round 37 — control-input calibration + ANSI-C code-view capability (2026-10-24)

L1 TameshiR37, attempt 1. Two distinct claims. Calibration (score 8) is the
lowest non-retired axis and carries C1. The stagnation nudge applies: depth 9 and
calibration 8 are at/above saturation 8, with no capability added in rounds 35–36;
C2 admits one bounded capability. Neither claim is exploratory. Contract:
`.ufo/evidence/round-37/contract.json`.

| Claim | Axis / type | Before | After | Delta | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|---|
| C1 r36 empty-panel control-input resolvability | calibration (lowest axis) | `C1_R37_PASS=false unresolved_control_inputs=1` at `d9c496b19371b779ce0eec6dfee1b049b27a3a2d` | `C1_R37_PASS=true unresolved_control_inputs=0` at `32826f37eb40afa6b2497425eecc95e23dacc5ee` | one unsuperseded control-input mismatch → zero; no numeric restraint-score move claimed | `python3 .ufo/evidence/round-37/calibration/measure.py --lane LANE --rev REV` | `32826f37eb40afa6b2497425eecc95e23dacc5ee` | `.ufo/evidence/round-37/calibration/before-final-control.stdout`, `after-control-final.stdout`, `.ufo/evidence/round-37/control/replay-at-final-control.stdout` | improved |
| C2 ANSI-C `$'...'` comment boundary | depth (capability acquisition) | code_view fixtures `1/2` at `d9c496b19371b779ce0eec6dfee1b049b27a3a2d` | fixtures `2/2`, selftest `35/35`, frozen r36 predicate re-attested PASS at `ae9b771ab795fb5b4a6302165d8abdc0a2c6b229` | one bounded quote form added; numeric depth remains 9 under command D | `python3 .ufo/evidence/round-37/code-view/measure.py --lane LANE --rev REV` | `ae9b771ab795fb5b4a6302165d8abdc0a2c6b229` | `.ufo/evidence/round-37/code-view/{before,after}.stdout`, `tool-selftest-after.stdout`, `c2-repin-after.stdout`, S104 | improved (capability) |

Capabilities table — row admitted this round:

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| bounded ANSI-C code_view | Keep Bash `$'...'` quoted text intact across escaped single quotes, blank a following comment, and preserve a literal `#` inside the quote; nested substitutions and unquoted backslash-newline remain unsupported | `.ufo/evidence/round-37/code-view/after.stdout` (2/2), `.ufo/evidence/round-37/tool-selftest-after.stdout` (35/35), `.ufo/evidence/round-37/c2-repin-after.stdout` (frozen r36 predicate PASS), S104 | round 37 |

Numeric guardrails: command D is `recorded_cases=9 depth_score=9` at both
`d9c496b` and `ae9b771`; no runner ledger case was added. The C1 counter measures
the named evidence/input mismatch, not the SHONEN restraint rubric. The r36 numeric
calibration score remains the last measured 8; the round-37 strict no-harm monitor
result is reported separately.

**Planned (round 38):** nested command-substitution quoting and unquoted
backslash-newline remain explicit holds from `corpus/lessons/round-35.md`
`## Holds`; do not generalize the bounded ANSI-C capability to a full Bash lexer.

## Round 38 — self-assessment reconciliation (calibration) + golden-comparison three-outcome verdict (depth) (2026-10-24)

L1 TameshiR38, attempt 1. Two claims, distinct axes; calibration (8) is the lowest non-retired
axis and carries C1. The stagnation nudge does not apply: round 37 added a capability row
inside the stagnation window. Neither claim is exploratory. Contract
`.ufo/evidence/round-38/contract.json`, frozen before any data run (base rev `ea8f14aa`).

| Claim | Axis | Before | After | Delta | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|---|
| C1 the lane's self-assessment records agree with the observed repo state (six declared mismatch classes m1..m6) | calibration (lowest axis) | `C2_R35: m1=0 m2=0 m3=1 m4=0 m5=0 m6=1 total=2 entries=40 sources_rows=101 rev=ea8f14aa5780084dc96a0fb0d2a50fd35eb93c8a C2_R35_PASS=false`, exit 1 (`.ufo/evidence/round-38/calibration/before-at-base.stdout`) | `total=0 ... C2_R35_PASS=true`, exit 0 at the round commit (`.ufo/evidence/round-38/calibration/after-at-<rev>.stdout`) | two live self-assessment mismatches -> zero (m3 the misrooted fleet-root seat file; m6 the standing sources-registry row count) | `python3 .ufo/evidence/round-35/c2/c2-measure.py --lane LANE --rev REV --fleet /home/vgpnk/Projects/shokunin` | the round-38 content commit (hash named in the receipt filename and the report) | `.ufo/waves/round-38/calibration/`, the misroot copy `.ufo/waves/round-37/residual/ResCorrections.md` (sha256 `46ff0665…`), lesson `corpus/lessons/round-38.md` `## Mistakes` | improved (measured) |
| C2 golden-comparison three-outcome verdict discipline (frontier F4) with a behavioural fixture | depth | `GOLDEN_R38: cases=0/3 mutant_killed=false entry_ok=false tool_absent=1 rev=ea8f14aa5780084dc96a0fb0d2a50fd35eb93c8a C2_R38_PASS=false`, exit 1 (`.ufo/evidence/round-38/golden/before-at-base.stdout`) | `cases=3/3 mutant_killed=true entry_ok=true ... C2_R38_PASS=true`, exit 0 at the round commit (`.ufo/evidence/round-38/golden/after-at-<rev>.stdout`) | one bounded decision table + fixture; the numeric depth score stays 9 (no new ledger leg) | `python3 .ufo/evidence/round-38/golden/measure.py --lane LANE --rev REV` | the round-38 content commit (hash named in the receipt filename and the report) | `tools/golden-verdict.py` (sha256 `c5f9616b…`, frozen in the contract), `corpus/knowledge/golden-comparison-verdict.md`, S105 + S106, lesson `corpus/lessons/round-38.md` `## Gate` | improved (measured) |

Numeric axes, measured. **depth 9 -> 9**: command D prints `recorded_cases=9 depth_score=9` at
the base rev and at the round commit (no ledger leg added; C2's gain is the decision table
and the fixture, not a case count). **calibration 8 -> 8**: C1's counter measures the named
self-assessment divergences, not the SHONEN restraint rubric; the restraint score is
unchanged because no SHONEN box moved. The lane's lowest axis is worked, and no axis is
harmed.

Capabilities table: no new row this round (the golden-verdict fixture is a verification
instrument for C2, not a new repertoire capability).

Routed repair: the round-37 closure's routed defect 1 (the lane claimed six residual reports,
five were committed) is discharged here -- the sixth seat report was located in the fleet root,
copied byte-exact into the lane repo (cmp verified) and the fleet-root copy deleted.

**Planned (round 39):** the F4 write-path census over the surveyed gates (the measurement
this round deliberately did not take); the comparator lattice beyond POSIX `diff`
(`cmp`, `git diff --exit-code`); the two named holds in the round-38 lesson.

| sources-registry | curate where the lane learns: opened, tiered, rechecked source rows, mined into admitted entries, census-gated | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → exit 0, `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`; row count from the re-derivable command `grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md` → 103 rows at round 35 (the "103 rows" this cell carried was a round-32 observation; corrected 2026-10-23, round 35, per r34 AllFourScorecard F1); `corpus/SOURCES.md` | fleet round 1 (kaika) |

## Round 39 — depth-guard agreement (calibration) + F4 write-path census (depth) (2026-10-24)

L1 Kimi fresh L1, attempt 1. Two claims, distinct axes. Calibration 8 is the lowest non-retired axis and carries C1. The stagnation nudge does not apply: round 37 added a capability inside the window. Neither claim is exploratory. Contract `.ufo/evidence/round-39/contract.json`, frozen before the deciding run (base `50aadd1bbd94e43cd3fcfb81459414394db2dc35`). The round-38 contract is not edited. Numeric depth stays 9; no ledger leg was added.

| Claim | Axis | Before | After | Delta | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|---|
| C1 the round-39 depth no-harm guard agrees with canonical command D on the live runner and on a ledger-stripped copy; the round-38 regex `^\s*leg` still matches 0 lines | calibration (lowest axis) | `C1_R39: guard_absent=1 ... mismatches=1 ... C1_R39_PASS=false` at `50aadd1bbd94e43cd3fcfb81459414394db2dc35` | `C1_R39: ... live_agree=1 stripped_agree=1 r38_regex_hits=0 mismatches=0 ... C1_R39_PASS=true` at `233077f88d7a8d142eff329202a120457a5d5258` | one vacuous guard replaced by a successor that agrees on both probes; the r38 file is unchanged | `python3 .ufo/evidence/round-39/guard/measure.py --lane LANE --rev REV` | `233077f88d7a8d142eff329202a120457a5d5258` | `.ufo/evidence/round-39/before/c1-at-base.stdout`, `.ufo/evidence/round-39/after/c1-at-233077f.stdout`, `.ufo/evidence/round-39/control/vacuous-and-constant.stdout` | improved (measured); numeric calibration stays 8 |
| C2 F4 write-path census of the 21 lane gate tools, with planted controls and a fixture that writes an expected file only behind an explicit flag | depth | `C2_R39: tool_absent=1 gates=0/21 ... C2_R39_PASS=false` at `50aadd1bbd94e43cd3fcfb81459414394db2dc35` | `C2_R39: tool_sha_ok=1 gates=21/21 live_write_sites=99 live_unflagged=0 planted_unflagged=1 planted_flagged=0 planted_scratch=0 fixture_wrote=1 mutant_killed=1 ... C2_R39_PASS=true` at `233077f88d7a8d142eff329202a120457a5d5258` | the census runs and discriminates; numeric depth stays 9 | `python3 .ufo/evidence/round-39/census/measure.py --lane LANE --rev REV` | `233077f88d7a8d142eff329202a120457a5d5258` | `.ufo/evidence/round-39/before/c2-at-base.stdout`, `.ufo/evidence/round-39/after/c2-at-233077f.stdout`, `tools/write-path-census.py` pin `bc8c660c56f871f85dad8912be28446293fd63f62b4fd1c16eb153f7a27edc62` | improved (measured); the 0 unflagged count is the frozen pattern's count, not a universal claim |

Do-nothing controls, committed before the deciding run: C1 at the base rev is `guard_absent=1` and cannot pass; a `^\s*leg` guard disagrees 0 vs 9 on the live runner; a constant 9 disagrees with command D's 0 on the stripped runner (`.ufo/evidence/round-39/control/vacuous-and-constant.stdout`). C2 at the base rev is `tool_absent=1`. A constant-0 classifier fails `planted_unflagged=1`. A constant-1 classifier fails `planted_scratch=0`. Removing `FLAG_GATE` makes the selftest fail (`mutant_killed=1`).

Numeric axes, measured at `233077f88d7a8d142eff329202a120457a5d5258`. **depth 9 → 9**: command D prints `recorded_cases=9 depth_score=9`. **calibration 8 → 8**: C1 counts the guard-versus-command-D mismatch, not the SHONEN restraint rubric. No SHONEN box moved. No axis harmed. `tools/golden-verdict.py` sha256 remains `c5f9616be719fdce99e8aaa9d8c9b1cde5c4c2d4d4db0b517ec16c1a26d15f87`.

Capabilities table: no new row. The census tool is the C2 instrument, not a new repertoire capability. The settlement classifier `tools/wave-parent-settle.py` is the round-38 parent-exit repair; it is not a capability-table claim.

**Planned (round 40):** the write forms the frozen pattern misses (`expected.json` via `.write_bytes`, `os.replace`), still under freeze-before-data; `cmp` and `git diff --exit-code` lattices stay unmeasured.

## Round 40 — write-form census v2 (capability) + S108 snapshot pin (freshness) (2026-10-24)

L1 Kimi fresh L1, attempt 1. Stagnation nudge fires: depth 9 and calibration 8 are at or above the saturation line 8, and no capability entered in rounds 38–39 (window N=2). The lowest-axis obligation is waived. The round is a capability move plus the routed S108 pin. Neither claim is exploratory. Contract `.ufo/evidence/round-40/contract.json`, frozen before any seat scored and before the deciding run (base `304e3355705640af2879c772fc9a5c2902c61763`). Numeric depth stays 9. Numeric calibration stays 8. The v1 census pin was not moved.

| Claim | Axis | Before | After | Delta | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|---|
| C1 write-path-census-v2 sees `expected.json` on `.write_bytes` and `os.replace`, which v1 misses | depth (capability) | `C1_R40: tool_absent=1 ... C1_R40_PASS=false` at `304e3355705640af2879c772fc9a5c2902c61763` | `C1_R40: tool_sha_ok=1 v1_sha_ok=1 bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0 v1_bytes_unflagged=0 v1_replace_writes=0 live_json_v2=1 live_json_v1=0 live_replace_v2=1 live_replace_v1=0 mutant_replace_killed=1 mutant_json_killed=1 ... C1_R40_PASS=true` at `5641ed84c8dc148c34c8dd83f062279ddf06b4af` | the two missed forms are classified; v1 cannot meet the target | `python3 .ufo/evidence/round-40/census/measure.py --lane LANE --rev REV` | `5641ed84c8dc148c34c8dd83f062279ddf06b4af` | `.ufo/evidence/round-40/before/c1-at-base.stdout`, `.ufo/evidence/round-40/after/c1-at-5641ed84.stdout`, `.ufo/evidence/round-40/control/v1-on-fixtures.stdout`, tool pin `4022853295882c5a11e192274e9215ea5a008e54eb0a2f77a8a2365f522d878b` | improved (measured); numeric depth stays 9 |
| C2 S108 quote pinned to a committed snapshot | freshness | `C2_R40: snapshot_absent=1 quote_in_snapshot=0 sha_ok=0 ... C2_R40_PASS=false` at `304e3355705640af2879c772fc9a5c2902c61763` | `C2_R40: snapshot_absent=0 quote_in_snapshot=1 sha_ok=1 stripped_quote_fails=1 ... C2_R40_PASS=true` at `5641ed84c8dc148c34c8dd83f062279ddf06b4af` | the quote the closure could not re-open is now in committed tag-stripped bytes | `python3 .ufo/evidence/round-40/s108/measure.py --lane LANE --rev REV` | `5641ed84c8dc148c34c8dd83f062279ddf06b4af` | `.ufo/evidence/round-40/before/c2-at-base.stdout`, `.ufo/evidence/round-40/after/c2-at-5641ed84.stdout`, snapshot sha256 `f27cf274b5dd7c28122dcb5a137971b401dad7910f7702eb4cbd3c28cd782bf0` | improved (measured); not a numeric owned-axis move |

Do-nothing controls, committed before the deciding run: C1 at the base rev is `tool_absent=1`. The v1 control on the planted fixtures is `v1_bytes_unflagged=0 v1_replace_writes=0 C1_R40_CONTROL_PASS=false`. C2 at the base rev is `snapshot_absent=1`. A copy of the snapshot with the prefix `可以通过使用参数` removed fails the quote check (`stripped_quote_fails=1` on the green run proves the check is load-bearing).

One deciding run of each counter, at `5641ed84c8dc148c34c8dd83f062279ddf06b4af`. The counter is deterministic and read-only (it reads the tree at a revision and writes only a temporary directory); the resumed L1 re-ran both counters and got the same lines and the same exit codes that the receipts below hold. The before and control receipts were re-run the same way.

Disclosed limit, not a predicate change: the live-site fields match the tool's regex objects on prefiltered lines. They do not call `classify_text` on the live file. A tool that hardcoded the five fixtures would still fail `tool_sha_ok` unless its bytes were the pinned blob. Seat `CriticHardcode` named this. The rule was not changed after that seat scored. Seat `CriticUniversal` found that `os.symlink`, `os.link`, `Path.symlink_to`, `Path.rename`, `shutil.*`, `os.remove/unlink` and `handle.write` are outside v2's `WRITE_RE`, and that `tools/repeat-control.py:807-823` writes `expected.json` through a variable path and through `os.symlink`. The frozen predicate names two planted classes and two live sites and claims no universality, so the pass bit stands; the gap is recorded in `corpus/lessons/round-40.md` Holds and is not counted anywhere.

Capabilities table — row admitted this round:

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| write-path-census-v2 | classify a string-literal `expected.json` on `.write_bytes` and an `os.replace` / `os.rename` write, which the round-39 census misses, with planted flagged and scratch controls | deciding receipt `C1_R40: ... C1_R40_PASS=true` at `5641ed84`, counter `.ufo/evidence/round-40/census/measure.py`, tool `tools/write-path-census-v2.py` @ `4022853295882c5a11e192274e9215ea5a008e54eb0a2f77a8a2365f522d878b` | round 40 |

Numeric axes, measured at `5641ed84c8dc148c34c8dd83f062279ddf06b4af`. **depth 9 → 9**: command D prints `recorded_cases=9 depth_score=9`. **calibration 8 → 8**: no SHONEN box moved (`boxes=4 checked=0 asserted=4`). No axis harmed. `tools/write-path-census.py` sha256 remains `bc8c660c56f871f85dad8912be28446293fd63f62b4fd1c16eb153f7a27edc62`.

**Planned (round 41):** `cmp` and `git diff --exit-code` lattices stay unmeasured; the v2 pattern still misses a variable destination on `os.replace`.

## Round 41 — self-assessment reconciliation (calibration) + variable-destination write census v3 (depth) (2026-10-25)

L1 tameshi, hyaku run 6, attempt 2. Attempt 1 died with the orchestrator
(`lane-dead-no-report tameshi round=41`, 2026-10-25T03:23:08-03:00); nothing was inherited:
`git status --porcelain` was empty and `.ufo/waves/round-41/` did not exist at attempt-2 start.
Two claims on distinct axes. Calibration (6, measured by the round-21 coldread monitor) is the
lane's lowest non-retired axis and carries C1;
the stagnation nudge does not fire because round 40 added a capability inside the window N=2.
Contract `.ufo/evidence/round-41/contract.json`, frozen at `d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937`
before any seat scored and before the first deciding run; five pre-data amendments are recorded
there (A1 the m7 status column index, A2 the symlink fixture root plus a third mutant, A3 a record
rephrasing, A4 directory-path resolution in m8, A5 the m9 correction words derived from the table).
A2 and A5 are declared `rule_changed: true` because they add a required conjunct to the C2 predicate
and a field to its target, and replace m9's two hardcoded correction strings with words derived from
the round-40 table — both stricter, neither relaxing a target or the kill rule.

| Claim | Axis | Before | After | Delta | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|---|
| C1 the lane's self-assessment records agree with observed repo state (classes m6, m7, m8, m9) | calibration (lowest axis) | `m6=1 m9=1 total=2 records=0 sources_rows=107 C1_R41_PASS=false`, exit 1 at base `a3d6c690bcbf8914551d4f4e8e1612784c1c2046` (`m6` the standing registry cell said 103; `m9` the round-40 quarantine summary said 7 refused / 9 present against its own table's 6 / 10) | target `m6=0 m7=0 m8=0 m9=0 total=0 C1_R41_PASS=true`, exit 0 | two live mismatches → zero, plus the two record-audit classes (m7 cited unmined S-ids, m8 unresolvable cited paths) measured at zero on this round's records | `python3 .ufo/evidence/round-41/calibration/measure.py --lane LANE --rev REV` | see the after subsection below | `corpus/lessons/round-41.md`, the round-40 correction appended there, the restated standing row | improved (measured) |
| C2 destination resolution in the write-path census (`tools/write-path-census-v3.py`) | depth (surface: `corpus/knowledge/r41-variable-destination-writes.md` — two cited sources S153/S154, the two-live-site table, the depth-4 fold threshold; capability instrument: `tools/write-path-census-v3.py`). Coverage is noted, not claimed separately: the tool and the two destination edge classes v2 cannot see (variable-held, `os.symlink`); the unmoved command is `grep -c 'os\.symlink' tools/write-path-census-v2.py` → 0 | `tool_absent=1 var_expected=0 symlink_expected=0 C2_R41_PASS=false`, exit 1 at base `a3d6c690` | target `tool_absent=0 tool_sha_ok=1 v2_sha_ok=1 selftest_exit=0 var_unflagged=1 var_expected=1 symlink_unflagged=1 symlink_expected=1 literal_unflagged=1 scratch_var_unflagged=0 v2_var_expected=0 v2_symlink_sites=0 live_var_resolved_v3=1 live_var_scratch_v3=1 live_var_expected_v2=0 live_symlink_resolved_v3=1 live_symlink_scratch_v3=1 live_symlink_sites_v2=0 mutant_resolve_killed=1 mutant_symlink_killed=1 mutant_symlink_arg_killed=1 C2_R41_PASS=true`, exit 0 | the two live sites `tools/repeat-control.py:811` and `:820` move from v2-unresolvable to v3-resolved; the v2 pin does not move; numeric depth stays 9 (no ledger leg added) | `python3 .ufo/evidence/round-41/census/measure.py --lane LANE --rev REV` | see the after subsection below | `tools/write-path-census-v3.py`, `.ufo/evidence/round-41/census/fixtures.json`, `corpus/knowledge/r41-variable-destination-writes.md` | improved (capability) |

Capabilities table — row admitted this round:

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| write-path census destination resolution | resolve a write destination held in a variable through up to four assignments/`os.path.join`/`+`/`/`/f-string hops and classify it as expected-value, scratch or update-flagged, for `open`, `write_text`/`write_bytes`, `os.replace`/`os.rename` and `os.symlink`; v2 cannot connect a destination to a token that is not on the same line | deciding receipt `C2_R41: … C2_R41_PASS=true` at the round-41 measured commit, counter `.ufo/evidence/round-41/census/measure.py`, tool `tools/write-path-census-v3.py` @ `095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279` | round 41 |

Numeric axes, measured: **depth 9 → 9** (command D prints `recorded_cases=9 depth_score=9` at the base
and at the round commit — the runner is not edited and no ledger leg is added). **calibration 6 → 6**:
the round-21 coldread monitor prints `calibration_restraint_score: 6` at both revisions, so the
carried `8` in earlier blocks is superseded as an upper bound (command C's `asserted_mark_upper_bound`
awards no credit, `corpus/knowledge/input-keyed-coldread-credit.md`), and no SHONEN box moved
(`boxes=4 checked=0 asserted=4`). Calibration remains the lowest axis at 6, which is where C1 works.
The C1 gain is record agreement, not a restraint-score move, and the C2 gain is a capability, not a
ledger count. No axis is harmed. Receipts: `.ufo/evidence/round-41/census/command-d.stdout`.

Guardrail on the label: numeric depth stays 9 → 9 under command D, and `C2_R41_PASS` is the
capability instrument's predicate, not the depth measure — the depth surface the label names is the
knowledge entry (two sources, the site table, the fold threshold), which the counter does not read.
C2's own instrument limits, disclosed rather than repaired after data: the counter imports the
measured tool **in-process** (`exec_module`) before running the selftest and mutants, so a hostile
tool could supply the fixture counts and patch `subprocess.run`; the tool pin is read from the same
revision's contract, so it proves the freeze commit agrees with itself, not that the bytes were
authored before the seats; the live half reads `expected`/`scratch`/`kind`/`lineno` and never the
`resolved` text, so a constant `{811: open, 820: symlink}` table would satisfy it; `killed` is
`returncode != 0`, so a traceback would count as a kill (all three real mutants die on their own
fixture class, receipted); `--control` is a negative control by construction (a `CONTROL_PASS=true` would mean v2 reached the
target), it reads the fixtures from the working tree rather than from `--rev`, and `fixtures_sha256`
is pinned but never verified.
The successor counter — out-of-process tool execution, a counter-side digest constant, `resolved`
text inspection and an exit-plus-FAIL-line kill oracle — is routed to round 42.
C1's own instrument limits, disclosed rather than repaired after data: neither counter has a
self-pin clause (C1 does not hash its own bytes against `claims.C1.counter_sha256`; C2 pins the tool
it audits and its `V2_SHA` constant, not itself), so a reader must compare each counter's bytes to
the contract pin by hand; m7 and m8 are vacuous when a
round's records are absent (the run prints `records=` and this round's is 3); m8 covers four path
prefixes and a root-file list, and it resolves directories as well as files; m9 reads the whole
lesson rather than the round-41 section. A successor counter with a self-pin and a `records >= 1`
gate is routed to round 42. None of these defects was used to reach the target — the two live
mismatches (m6, m9) and the two record-audit classes were all measured on this round's records,
and the base and deciding receipts are committed.
Pre-data controls, receipted before the deciding run: C1's base run is its own do-nothing control
(`m6=1 m9=1` survive any edit that does not touch them). C2's base run is `tool_absent=1`, and
`--control` scores the same fixtures with the embedded v2 patterns →
`v2_var_expected=0 v2_symlink_sites=0 C2_R41_CONTROL_PASS=false`, exit 1.

Disclosed limit (not a predicate change): v3 labels `tools/context-capture.py:1682` and `:1685`
`unflagged` although both are scratch — their base is `self.case_dir(name)`, a non-folding call over an
unbound `self.root`. The tool's `unflagged` column must be read against the base expression; the fix
(dotted-attribute binding plus a completeness flag) is routed to round 42. `tools/registry-replay.py:123`
writes `expected.json` under an explicit `--out` directory, which the census counts as unflagged because
an explicit output flag is not in its update-flag pattern; that is a classification gap, not a hidden update.


### Round 41 — after the deciding run

Both counters ran at `baa18b7bdd637ff175255e82b6bee3c85df0881e`, the revision that carries the wave
evidence and the corrected records. Both passed:

```
C1_R41: m6=0 m7=0 m8=0 m9=0 total=0 records=3 sources_rows=109 rev=baa18b7bdd637ff175255e82b6bee3c85df0881e C1_R41_PASS=true
C2_R41: tool_absent=0 tool_sha_ok=1 v2_sha_ok=1 selftest_exit=0 var_unflagged=1 var_expected=1 symlink_unflagged=1 symlink_expected=1 literal_unflagged=1 scratch_var_unflagged=0 v2_var_expected=0 v2_symlink_sites=0 live_var_lineno=811 live_var_resolved_v3=1 live_var_scratch_v3=1 live_var_sites_v2=1 live_var_expected_v2=0 live_symlink_lineno=820 live_symlink_resolved_v3=1 live_symlink_scratch_v3=1 live_symlink_sites_v2=0 mutant_resolve_killed=1 mutant_symlink_killed=1 mutant_symlink_arg_killed=1 rev=baa18b7bdd637ff175255e82b6bee3c85df0881e C2_R41_PASS=true
```

Both exit 0. Receipts: `.ufo/evidence/round-41/after/c1-at-baa18b7b.stdout` (exit file alongside),
`.ufo/evidence/round-41/after/c2-at-baa18b7b.stdout`. The two runs are the deciding runs; the same
two commands were executed again at the commit that carries this section and printed the same counts
and the same pass bit — the `rev=` field differs by design, because it echoes the revision the run
read. The counters read a revision and write nothing to the lane (C1 writes nothing at all; C2 writes
only a temporary directory), so a re-run is the same measurement. The earlier run at `b37ce974` is retained as history: C2 passed there and C1 failed
`m8` on a cited wave path that had not yet been committed — the landing-order defect the wave seats
named.

Verdicts as measured: C1 **improved** (two live mismatches → zero, with the two record-audit classes
measured at zero on this round's records); C2 **improved** (capability acquisition, five of five
declared pin/fixture/live/mutant conditions met). Numeric depth 9 → 9, numeric calibration 6 → 6; no
axis harmed.

| sources-registry | curate where the lane learns: opened, tiered, rechecked source rows, mined into admitted entries, census-gated | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → exit 0, `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`; row count from the re-derivable command `grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md` → 109 rows at round 41 (restated by appending this row, the round-35 row above is unchanged; the counter reads the last standing row) ; `corpus/SOURCES.md` | fleet round 1 (kaika) |

## Round 42 — receipt reconciliation (calibration) + attribute/output-flag write census v4 (depth) (2026-10-25)

L1 tameshi, hyaku run 6, attempt 1. Nothing was inherited. Two claims on distinct axes. Calibration
(6, measured by the round-21 coldread monitor) is the lowest non-retired axis and carries C1. The
stagnation nudge does not fire: round 41 added a capability inside the window N=2. Contract
`.ufo/evidence/round-42/contract.json`, frozen at `322b5cd32b4319a05340d249ae752d12a9e6b19f`
before any seat ran. Post-freeze amendments P1–P4 change citations and disclosures only.

| Claim | Axis | Before | After | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|
| C1 self-assessment records agree with the tree: no unsuperseded stale presence receipt; round-41/42 records cite no unmined S-id (round 42), no unresolvable path, no unreachable revision | calibration (lowest axis) | `m10=1 total=1 records=3 C1_R42_PASS=false`, exit 1, at base `c77c2b7e64d2e356381441ecf94abac03e984606` | target `self_pin=1 m6=0 m7=0 m8=0 m10=0 m11=0 total=0 records=6 C1_R42_PASS=true`, exit 0 | `python3 .ufo/evidence/round-42/calibration/measure.py --lane LANE --rev REV --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f` | see the after subsection | `corpus/lessons/round-42.md`, `.ufo/evidence/round-42/before/c1-at-base.stdout`, `.ufo/evidence/round-42/control/c1-do-nothing.stdout` | see the after subsection |
| C2 `tools/write-path-census-v4.py` binds attribute and output-flag destinations: the three live v3 false positives resolve with `mkdtemp` / `--out` in the resolved text, ten fixtures keep their classes, lane-wide unflagged 0, every declared mutant killed | depth (surface: two new destination edge classes, `corpus/knowledge/r42-attribute-and-outflag-destinations.md`, the tool) | `tool_absent=1 live_unflagged_v3=3 C2_R42_PASS=false`, exit 1, at base | target `C2_R42_PASS=true`, exit 0 | `python3 .ufo/evidence/round-42/census/measure.py --lane LANE --rev REV --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f` | see the after subsection | `.ufo/evidence/round-42/before/c2-at-base.stdout`, `.ufo/evidence/round-42/control/c2-v3-in-slot.stdout`, `.ufo/evidence/round-42/control/c2-junk.stdout` | see the after subsection |

Numeric axes at the base: depth 9 (command D `recorded_cases=9 depth_score=9`), calibration 6
(round-21 coldread monitor `calibration_restraint_score=6`), both re-run by wave-1 seat
ExecCommandD (`.ufo/waves/round-42/w1/ExecCommandD.md`). Neither claim edits the runner or a
SHONEN box, so neither number is expected to move. C1's gain is record agreement, and C2's gain
is a capability, not a ledger count.

Instrument limits, disclosed rather than repaired after data (full list in
`corpus/lessons/round-42.md`): m10 is content-blind and reads only boolean `present` beside
`report`/`path` under `.ufo/waves/`; m7 checks round-42 records only; C2's battery cannot tell a
resolver from a name- and line-special-casing tool, so a renamed-identifier falsifier runs
outside the predicate; and the oracle is stricter than both vendors on timeouts.

| sources-registry | curate where the lane learns: opened, tiered, rechecked source rows, mined into admitted entries, census-gated | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0, zero E codes; row count from the re-derivable command `grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md` → 113 rows at round 42 (restated by appending this row; the round-41 row above is unchanged; the counter reads the last standing row) ; `corpus/SOURCES.md` | fleet round 1 (kaika) |
