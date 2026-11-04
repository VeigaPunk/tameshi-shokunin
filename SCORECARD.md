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
| mutation sweep runner | inject → run → restore single-edit mutants with a green-control gate, verdict lines and byte-identity proof | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 107/107 pass`, exit 0 (`.ufo/evidence/kaika-round-1/capability-demo/h1a-selftest-host.stdout`) | historical round 3 (`SCORECARD.md:16`); re-demonstrated fleet round 1 |
| six-leg regression ledger | replay every recorded mutation case at its pinned blob; exact expectation | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=6 passed=6 …)`, exit 0 (`…/capability-demo/h1b-regression.stdout`) | historical round 7 (four legs) / round 10 (six); re-demonstrated fleet round 1 |
| repeated pristine-control gate | observe N≥3 exact exit/stdout/stderr tuples, distinguish mismatch from unavailable/uniform-nonzero baseline, validate digest-pinned observation snapshots | `python3 tools/repeat-control.py --selftest` → PASS (29 cases), exit 0; real bash controls match; red-before loop mutant fails the same mismatch oracle, restored loop passes; `.ufo/evidence/round-12/verification-final.json`, `oracle-repair.json`; measured `9df9212d33dc2dbda133e88f28ad47bb08839a5b` | round 12; lane demonstrated, outside admission pending |
| six-leg content-disposition probe | emit configured-pin, committed-HEAD and worktree SHA observations for every recorded leg, while explicitly withholding verdict reuse | `python3 tools/pin-disposition.py --selftest` → `SELFTEST: PASS (19/19)`; real read changed3/unchanged3/unavailable0; `.ufo/evidence/round-13/verification.json`, `pin-dispositions.json`; measured `4acc607dfd79f19d508bd50cdd06b77269fccd1d` | round 13; lane demonstrated, outside admission pending |
| exposed witness provenance correction | validate a new digest-anchored non-blind companion without rewriting frozen observations; prevent wrong-nesting in future producer output | metadata selftest39/39 PASS0; null-only companion FAIL1/corrected PASS0; producer same-oracle40/41 FAIL1→41/41 PASS0; `.ufo/evidence/round-13/producer-oracle-repair.json`, `verification-verdict.json`; measured `4acc607dfd79f19d508bd50cdd06b77269fccd1d` | round 13; lane demonstrated, outside admission pending |
| effective expectation reconciliation | account for every historical expected row, reject an exit-only setup crash, and preserve that raw failure under a checked explicit oracle supersession | `python3 tools/evidence-disposition.py --selftest` → `SELFTEST: PASS (66/66)`; same checker before FAIL1/contains_missing→after CLEAN0, eleven effective+one superseded; `.ufo/evidence/round-14/verification-final.json`, S050; executable measurement6431478 | round14; lane demonstrated, separate outside admission pending |
| retained invocation-context gate | re-derive bounded raw receipt predicates, check byte-pinned frozen receipts, and distinguish semantic mismatch from unavailable/tampered input through a standalone public-CLI selftest | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72` → exit0, copied-source CLI selftest49/49, registered frozen0, missing-env1, tamper2, usage64; `.ufo/evidence/round-15/verification-3.json`; S051 | round15; lane demonstrated, separate non-author admission pending |
| hermetic env-differential probe | classify the raw exit/stdout/stderr tuple of nine pinned selftests under seven explicit profiles, separating repeat variation from environmental sensitivity | `python3 tools/env-diff.py --selftest` first actual9/9; real receipt `f5/receipt-initial.json` under `.ufo/evidence/round-21/` classifies9/9 (eight invariant, one raw-output-variable); `corpus/knowledge/hermetic-env-differential.md`, S079/S081 | round21; lane demonstrated, separate non-author admission pending |
| callback-authoritative wave accounting | reconcile exact registered identities and terminal states while preserving failed seats' partial artifacts; reject mismatched totals and digest tampering | at11f55d64968778aaed07b001fc8b2480c38e1896: frozen counter8/8, actual146-seat replay66 completed/80 failed, wrong-count1/TOTAL_MISMATCH; `.ufo/evidence/round-22/final/verification.json`, S082 | round22; lane demonstrated, separate non-author admission pending |
| executor-source pin gate | compare each verifier-declared executor source Git blob in a candidate commit to the same path in a verifier-supplied trusted commit; exit 0 bound, 1 drift, 2 unavailable | `python3 -I .ufo/evidence/round-59/measure.py --lane LANE --rev 93acc996cbb7bfed27112e797c9d2392ff4aa6b3 --work EMPTY_DIR` → `passed=24/24 C1_R59_PASS=true`; controls `.ufo/evidence/round-59/controls/` (always-accept 8/24, skipped-work 0/24) | round59; lane demonstrated; counter cheat-passable (fingerprint 24/24, Mistake 1 in `corpus/lessons/round-59.md`); **not admitted (honest stop, closure round 59)**. Round 60: re-certified on the installed discriminating counter `tools/executor-source-pin-measure.py` at `da2ae6b361de2d6294c6324a02ae141ff6cb482f` — `passed=8/8 C1_R60_PASS=true` (`.ufo/evidence/round-60/after/cert.out`), full cheat family red (`.ufo/evidence/round-60/controls/`); admission still an operator ruling |
| host-feasible no-harm precheck | re-run the frozen round-48 coldread no-harm precheck to a verdict on the win32 host in seconds: the frozen decision code with its two per-input git plumbing functions batch-cached (spawn fallback + deterministic spawn-equivalence probe, chunked/resumable prefetch) | `python -I tools/coldread-precheck-portable.py --repo . --rev 8b0042bde0ca59aac9a23a8a707cf0902183d081 --work WORK` → `credited=46/64 elapsed=7.1s probe_sampled=20 probe_mismatches=0` (`.ufo/evidence/round-61/win-host/measure-base.out`); `DIFFERENTIAL: PASS` vs the frozen selector (`.ufo/evidence/round-61/win-host/differential.stdout`); S293 | round 61; lane demonstrated; execution form of the frozen instrument, not a replacement |
| monitored-record rekey run-book | absorb a monitored-record edit (QUALITY/SOURCES/PROVINCE/README/pinned-tool bytes) in one round: project the staled cold-read sections, regenerate fresh input-keyed ledger entries re-reading every section and union input at the pin revision via git objects, land the trace receipts, and restore the monitor to `lost=0` — with the pre-landing scratch rehearsal and file-path-only commit discipline as run-book steps | `python .ufo/evidence/round-63/win-host/coldread-rekey-rebind-r63.py --repo . --pin <rev> --plan .ufo/evidence/round-63/win-host/union-plan.json --manifest .ufo/evidence/round-63/win-host/rekey-manifest.json --traces-dir .ufo/evidence/round-63/rekey/traces --entries-out .ufo/evidence/round-63/win-host/entries-batch.json --merge-ledger` -> `REBIND OK sections=13 entries_added=13 ledger_before=680`; restore receipts `.ufo/evidence/round-63/win-host/precheck-b.json` (64/64, lost=0) | round 61 (batch rekeys); named run-book entered round 63 (re-demonstrated on a QUALITY+SOURCES pair) |
| receipt-existence sweep | sweep a named document's cited evidence paths on committed bytes: backtick-cited `.ufo/`+`tools/` paths extracted at a pinned rev, each resolved by `git cat-file -e REV:path` (blob or tree), fleet-root-surface cites resolved via a named `--extra-root` filesystem check | `python -I tools/receipt-exists.py --selftest` → `RECEIPT_EXISTS_SELFTEST: 4/4 pass`; `python -I tools/receipt-exists.py --repo . --rev 1763db52… --doc corpus/lessons/round-63.md --doc corpus/lessons/round-63-verifier-spotcheck.md --extra-root <fleet-root>` → `paths=16 missing=0 extra=2` (`.ufo/evidence/round-64/win-host/live-demo-sweep.txt`) | round 64 |
| commit-message receipt binding sweep | sweep a commit range on committed objects: every evidence file ADDED under `.ufo/evidence/` whose basename is named in a commit's message must exist in that commit's tree; violations named (`BIND_DEFECT`) with exit 1; ranges adding no evidence file refused exit 2 (no vacuous pass) | `python -I tools/receipt-commit-bind.py --selftest` → `RECEIPT_COMMIT_BIND_SELFTEST: 7/7 pass`; the r64 range `d0baf616..c7d28b19` → `findings=1` exit 1 naming `6876d746`; `7d7f9ca8..6db7e2fc` → `findings=0` exit 0 (`.ufo/evidence/round-65/win-host/live-bind-r64-range.txt`, `live-bind-r65-range.txt`) | round 65 |
| quoted-line receipt backability | check a record's quoted counter lines byte-for-byte against committed receipt bytes at a pinned rev: verdict-shaped backtick spans must be byte substrings of receipts the record itself cites (directory-cite expansion, unique-basename resolution, named `--extra-root` filesystem check for fleet-root surfaces); unbacked quotes named with exit 1; empty documents refused exit 2 | `python -I tools/quoted-line-exists.py --selftest` → `QUOTED_LINE_EXISTS_SELFTEST: 5/5 pass`; the r64-records demo at the tip → `quotes=16 backed=12 missing=4` exit 1 with all four named (`.ufo/evidence/round-65/win-host/live-quoted-demo.txt`, `live-quoted-explicit.txt`) | round 65 |
| counter-arm liveness check | verify that every declared red arm of a frozen counter carries one committed input that MOVES its tally: a manifest row pins the instrument bytes at a revision, the committed input, the tally field, its do-nothing baseline and the expected move; the checker extracts the instrument from git objects (never a worktree), runs it `python -I` against the input, and marks the row `ARM_LIVE` only when the exit matches and the parsed tally ≥ expect_min and > baseline, else `ARM_DEAD`; an empty manifest is refused exit 2 | `python -I tools/arm-liveness.py --selftest` → `ARM_LIVENESS_SELFTEST: 5/5 pass`; the standing manifest → `rows=9 live=9 dead=0` exit 0; the dead-arm demo — a scratch manifest row pinning the FROZEN bind tool over `7d7f9ca8..87e95597` reads `ARM_DEAD … findings=0` exit 1, the same row re-pinned to the r66 tool reads `ARM_LIVE … findings=4` exit 0 (`.ufo/evidence/round-66/win-host/live-selftest-liveness.txt`, `live-liveness-standings.txt`, `live-demo-dead.txt`, `live-demo-live.txt`, the two `live-demo-manifest-*.json`) | round 66 |
| figure-attribution check | verify that a record figure pinned to ONE named receipt lives in THAT receipt's committed bytes: a manifest row pins the doc bytes at a revision, the exact figure line and ONE receipt path at a revision, both read from git objects (never a worktree); rows carry an expectation (attributed or misattributed) so the standing red arm MEASURES misattributed on every sweep; unresolvable inputs are setup exit 2 before any effect, a zero-row manifest is refused exit 2; the anywhere-in-cited-set relaxation is the cheat family refused by construction — the committed control shows a set-matcher passing the exact pair the instrument flags | `python -I -X utf8 tools/figure-attribution.py --selftest` → `FIGURE_ATTRIBUTION_SELFTEST: 7/7 pass`; the standing manifest → `FIGURE_ATTRIBUTION: rows=3 met=3 unexpected=0` exit 0 with `FIGURE_ROW r66-stale-selftest-figure-red expect=misattributed measured=misattributed ok` (`.ufo/evidence/round-68/win-host/figattn-selftest-r68.txt`, `figattn-standings-r68.txt`, `controls/cheat-anywhere-passes-red.txt`, `controls/cheat-anywhere.py`) | round 68 |
| anchor-drift sweep | verify that a held source row's anchor heading is still the heading the row's own pinned snapshot carries: a manifest row pins (snapshot path at a revision, the exact heading string the anchor cell names, expect present or absent), the snapshot blob is read from git objects at that revision (never a worktree), h1-h6 texts are parsed through an html.parser.HTMLParser subclass (entity-decoding, whitespace-normalized, trailing paragraph mark dropped) and the row verifies only when measured presence matches expectation; an expect=absent row MEASURES the drift on every sweep, never assumes it; unresolvable snapshots are setup exit 2 before any row effect, a zero-row manifest is refused exit 2 | `python -I -X utf8 tools/anchor-drift-sweep.py --selftest` → `ANCHOR_DRIFT_SELFTEST: 5/5 pass`; the standing manifest → `ANCHOR_DRIFT: rows=16 met=16 unexpected=0` exit 0 with `ANCHOR_ROW s299-anchor-as-written expect=absent measured=absent ok` — the r68 closure's routed defect standing as a measured red arm (`.ufo/evidence/round-69/win-host/anchor-selftest-r69.txt`, `anchor-standings-r69.txt`; SOURCES S300) | round 69 |
| printed-count recheck | verify that a record's printed counting figure is still the count its named command produces at the revision the record names: a manifest row pins the record bytes at a revision, the exact record span that carries the figure, the printed integer and the counting command of record `git grep -c [-E] <pattern> <rev> -- <path>` (SOURCES S301: the --count contract; zero matches print nothing and exit 1, read as the count 0 - measured, disclosed); the span binding requires the span to be a byte substring of the record and the printed integer to occur in it as a delimited token; rows carry expect match or drift so the standing red arm MEASURES the drift on every sweep; unresolvable records are setup exit 2 before any row effect, a zero-row manifest is refused exit 2 | `python -I -X utf8 tools/count-recheck.py --selftest` → `COUNT_RECHECK_SELFTEST: 6/6 pass`; the standing manifest → `COUNT_RECHECK: rows=7 met=7 unexpected=0` exit 0 with both routed red arms reading `COUNT_ROW scorecard-r68corr-unanchored-r67tip expect=drift printed=4 measured=0 ok` and `COUNT_ROW lesson-r69-unanchored-r67tip expect=drift printed=4 measured=0 ok` (`.ufo/evidence/round-70/win-host/count-selftest-r70.txt`, `count-standings-r70.txt`; SOURCES S301) | round 70 |
| line-pointer recheck | verify that a record's cited line pointer still points at the content the record claims at the revisions the record names: a manifest row pins (the record bytes at a revision, the exact cited pointer token as it occurs in the record, the target path at a revision, the 1-indexed inclusive line span, the needle - the content the record claims the span carries); the span is extracted from git objects (never a worktree) with the engine of record `git cat-file blob <rev>:<path> | sed -n 'START,ENDp'` (SOURCES S302: the inclusive address-range contract; the page's numeric-address form grounds single-line spans), argv stages only, sed load-bearing (not spawnable = setup exit 2, could-not-evaluate, never a silent fallback); a span past the last line prints nothing (measured) and reads as a miss; needles match as UTF-8 bytes, mid-line needles terminator-agnostic (the CRLF selftest arm measures it); the pointer binding requires the token to occur in the record bytes (else ERROR - the always-match cheat refused by construction); rows carry expect hit or miss so the standing red arm MEASURES the drift on every sweep; unresolvable records/targets are setup exit 2 before any row effect, a zero-row manifest is refused exit 2 | `python -I -X utf8 tools/pointer-recheck.py --selftest` -> `POINTER_RECHECK_SELFTEST: 7/7 pass`; the standing manifest -> `POINTER_RECHECK: rows=12 met=12 unexpected=0` exit 0 with the three red arms reading `POINTER_ROW lesson-r48-s267-pointer-140 expect=miss measured=miss ok`, `POINTER_ROW lesson-r48-s268-pointer-141 expect=miss measured=miss ok` and `POINTER_ROW province-r16-sevenleg-85-91 expect=miss measured=miss ok` (`.ufo/evidence/round-71/win-host/pointer-selftest-r71.txt`, `pointer-standings-r71.txt`; SOURCES S302) | round 71 |
| rekey-cost forecast | price a planned edit set against the cold-read ledger's own input pins before any byte changes: which SKILL.md sections lose credit and how many re-read sections the rekey will owe | `python3 -I tools/rekey-cost.py --selftest` → `REKEY_COST_SELFTEST: 8/8 pass`; `python3 -I tools/rekey-cost.py --edit corpus/SOURCES.md --edit PROVINCE.md` → `REKEY_COST sections=64 planned=2 at_risk=17 predicted_lost=17`, equal to the guard's measured `lost=17 RED` at `d618518a`; arms 13/6/6/0/0 each equal to a guard-measured counterfactual (`.ufo/evidence/round-72/reh/`, five receipts); the rekey paid it (`REBIND OK sections=17 entries_added=17 ledger_before=797`, monitor back to 64/64 at both floors) | round 72 |
| wave-record reconciliation | re-derive a round record's own execution claims (seat count, committed seat-report count, role multiset, attack share) from the committed wave artifacts: four row kinds, each binding a record span by byte substring at the record revision with the printed integer a delimited token, artifacts read from git objects at their own revision, `expect` is meet or drift so a standing red arm MEASURES the drift on every sweep, a UTF-8 BOM refused as setup exit 2 (S066 §8.1) | `python3 -I -X utf8 tools/wave-reconcile.py --selftest` → `WAVE_RECONCILE_SELFTEST: 25/25 pass`; `python3 -I -X utf8 tools/wave-reconcile.py --repo . --extra-root fleet=/home/vgpnk/Projects/shokunin --manifest tools/wave-reconcile.json` → `WAVE_RECONCILE: rows=6 met=6 unexpected=0` with both r72-closure red arms measured (`printed=11 files=12`; plan `labrat` vs executed `revenger`); independent oracle `ORACLE_CMP rows=6 equal=6` (seat T73W1S01); `.ufo/evidence/round-73/`: `wave-selftest-r73.txt`, `wave-reconcile-live-r73.txt`, `hardening-r73.txt` | round 73 |

| round-range additivity sweep | measure a round's append-only / content-preservation claims over a declared commit range with a declared claim class per row, naming the worst commit and the class-specific counts | `python3 -I tools/additivity-range.py --repo . --manifest tools/additivity-range.json` → `ADDRANGE: rows=11 met=11 unexpected=0` exit 0; `--selftest` → `ADDITIVITY_RANGE_SELFTEST: 8/8 pass`; `.ufo/evidence/round-74/addr-r74.txt` | round 74 |
| non-Python instrument freshness row | execute a freshness row's instrument under a frozen per-row interpreter tuple (python as the unchanged default, bash added) and bind a non-Python instrument's printed figure to the capability row it demonstrates | `python3 -I -X utf8 tools/selfstate-freshness.py --repo . --doc-rev 5bcb13ea7cc08bb0b594fcd0c2bb770cb8fe64a0` -> `SELFSTATE: rows=22 match=20 stale=2 unexpected=0` exit 0 with `SELFSTATE_ROW mutation-runner-selftest capability=mutation sweep runner expect=match measured=match ok`; `--selftest` -> `SELFSTATE_SELFTEST: 14/14 pass`; re-demonstrated round 79 (`receipt-bind-selftest` row added, arm14); `.ufo/evidence/round-78/c1-landed-sweep.txt`, `c1-landed-selftest.txt` | round 78 |
| receipt-bytes binding sweep | bind a receipt's recorded `# tool_sha256:` to the committed blob of a revision the receipt names (or of an append-only `# measured_bytes_rev:`); a false correction, a malformed recognised header and a duplicate header are refused before any row effect | `python3 -I -X utf8 tools/receipt-bytes-bind.py --repo . --root .ufo/evidence/round-78` -> `RECEIPT_BIND: receipts=12 bound=4 corrected=8 unbound=0` exit 0; `--selftest` -> `RECEIPT_BIND_SELFTEST: 14/14 pass` (round 80 re-demonstration: the design class and the whole-tree sweep; round 83: a symlink enters the population as a declared `unbound detail=not-regular-file` row and its target's bytes are never read); `.ufo/evidence/round-79/c1-landed-sweep.txt`, `c1-selftest.txt` | round 79; round-83 non-regular-path class |

| registry-home figure binding | bind a gate figure printed in the lane's registry home (SKILL.md's latest named row and `tools/registry.json`) to the figure its instrument prints now: a declared 9-row manifest, `match`/`stale`/`absent`/`error` states, `expect` per row as a standing red arm, and a `--selftest` 13/13 with planted stale/absent/duplicate/unparsable/error arms (round 83 adds the registry-json drift arm and the registry-surface absent arm) | `python3 -I -X utf8 tools/registry-figure-bind.py --repo .` → `REGISTRY_BIND: rows=9 match=9 stale=0 absent=0 error=0 unexpected=0` exit 0; `--selftest` → `REGISTRY_BIND_SELFTEST: 13/13 pass`; measured at the round-83 records commit | round 80; round-83 two defect-bind registry rows bound |
| closure-defect bind | turn a non-author closure's routed-defect prose into declared rows whose state is measured over committed bytes (five probe kinds: tree-paths, tree-bytes, receipt-tokens, sources-cell, doc-contains), and bind the population to the bytes committed at a declared revision (`--manifest-rev`), so "closed" is a count and a narrowed register is refused rather than certified | `python3 -I -X utf8 tools/defect-bind.py --repo . --manifest tools/defect-bind.json --manifest-rev HEAD` → `DEFECT_BIND: rows=6 closed=6 open=0 unexpected=0 manifest=bound` exit 0; `--selftest` → `DEFECT_BIND_SELFTEST: 14/14 pass` (14 arms; A12 the regular-file boundary, A13 the manifest binding, A14 the selftest-text pin) | round 81; round-82 extension (`--manifest-rev`, the mode/type boundary, the text pin) |
| standing-pin audit | measure whether a standing sweep's declared population pins the instrument bytes the tip carries (`settled` = blob equality at pin vs tip), instead of trusting that a matching figure means settled bytes | `python3 -I -X utf8 tools/selfstate-freshness.py --repo . --manifest tools/selfstate-freshness.json --pin-audit --pin-rev HEAD` → `SELFSTATE_PINS: rows=26 settled=26 stale=0` exit 0; before the round-81 landing `settled=20 stale=3` (`.ufo/evidence/round-81/controls/c2-before.txt`) | round 81; the three capability rows are live under R82-C2 |
| selftest-text pin | pin a suite's own assertion text (digest of `inspect.getsource(selftest)` against a constant), so a weakened arm fails an arm instead of passing vacuously — the round-80 `ss-bom-only` / `wr-prefix` survivor class; extended to `tools/defect-bind.py` in round 82 | `SELFSTATE_SELFTEST: 24/24 pass`, `WAVE_RECONCILE_SELFTEST: 25/25 pass`, `DEFECT_BIND_SELFTEST: 14/14 pass`; batteries `defects=5 killed=5` / `defects=14 killed=14` / `defects=5 killed=5` with `CONTROL: GREEN`; base controls `killed=0 survived=1` per tool (`.ufo/evidence/round-81/controls/`, `.ufo/evidence/round-82/controls/c3-before-mutant.txt`) | round 81; the defect-bind arm is round 82 |

Rows enter only through a round that demonstrates the capability running (`AXES.md` §Capabilities); none enter through this rollout. The three round-81 capabilities above now live here rather than only in `## Round 81 — capabilities entered` (the round-81 closure's routed defect 6); each is a live self-state row from round 82 (`tools/selfstate-freshness.json` rows `closure-defect-bind`, `standing-pin-audit`, `selftest-text-pin`).

## Saturation

The lane's saturation line + stagnation window N are to be declared by the lane on its next round per `AXES.md` §The stagnation nudge; not asserted by this conformance change.

Declared fleet round 1 (kaika): **saturation line 8/10** on each owned
axis — calibration's lane-attainable cap is 8, the last 2 need
independent review; depth is capped at 10 recorded cases. **Stagnation
window N = 2** completed rounds without a capability entering the
table. Policy choices, not observations; the nudge does not fire now
(depth 6 < 8; calibration pinned 0, candidate 8 pending).

Round-60 correction (2026-10-30; round-59 spot-check defect 5), appended:
the paragraphs above are unchanged. The nudge premise is stated **on the
scored axes only** — depth, calibration and freshness carry numeric scores
(depth 10, calibration 8, freshness 9 at the round-59 close); coverage,
adjacency and operability are verdict-only axes with no numeric score, so
"each owned axis" reads as "each scored axis" from round 60 on. The nudge
fires on the scored axes (10, 8, 9 — all at or above the line 8) with no
capability admission since round 50 (window N = 2 exceeded).

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

At round 76: the two dated capability literals above are superseded by the
instruments’ own current selftest tokens: pin-disposition reads
`SELFTEST: PASS (19/19)` and evidence-disposition reads `SELFTEST: PASS (66/66)`
(rows `:244` and `:246`; receipts: selfstate sweep rows
`r76-pin-disposition-selftest`/`r76-evidence-disposition-selftest` at
`.ufo/evidence/round-76/`, instruments pinned at `451ed5cb`). The two bash-instrument
gaps named at round 17 stay routed, not population rows: the mutation sweep runner
selftest is now `MUTATE_SELFTEST: 107/107 pass` (round 17 said 95/95) and the
six-leg regression ledger now runs `cases=10` (round 17 said `cases=7`;
receipts `.ufo/evidence/round-76/c2-after-r76.txt`,
`.ufo/waves/round-76/w1/T76W1E3/mutate-selftest.out`,
`.ufo/waves/round-76/w1/T76W1E3/mutate-regression.out`).
The round-17 values stand as dated history; the rows stay as written elsewhere.

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
| C2 `tools/write-path-census-v4.py` binds attribute and output-flag destinations: the three live v3 false positives resolve with `mkdtemp` / `--out` in the resolved text, ten fixtures keep their classes, over tracked tools/ Python files (26 at the round commit), every declared mutant killed | depth (surface: two new destination edge classes, `corpus/knowledge/r42-attribute-and-outflag-destinations.md`, the tool) | `tool_absent=1 live_unflagged_v3=3 C2_R42_PASS=false`, exit 1, at base | target `C2_R42_PASS=true`, exit 0 | `python3 .ufo/evidence/round-42/census/measure.py --lane LANE --rev REV --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f` | see the after subsection | `.ufo/evidence/round-42/before/c2-at-base.stdout`, `.ufo/evidence/round-42/control/c2-v3-in-slot.stdout`, `.ufo/evidence/round-42/control/c2-junk.stdout` | see the after subsection |

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

### Round 42 — after the deciding run

Both counters ran at `242c1b4a1bb793d6ca4ac4e3b0da153767e78739`, the revision that carries the
wave evidence, the declared mutants and the corrected records:

```
C1_R42: self_pin=1 m6=0 m7=0 m8=0 m10=0 m11=0 total=0 records=6 sources_rows=113 rev=242c1b4a1bb793d6ca4ac4e3b0da153767e78739 freeze=322b5cd32b4319a05340d249ae752d12a9e6b19f C1_R42_PASS=true
C2_R42: self_pin=1 tool_absent=0 tool_sha256=784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5 v3_sha_ok=1 v2_sha_ok=1 selftest_exit=0 fixtures_pass=10/10 run_errors=0 live_1682_ok=1 live_1685_ok=1 live_123_ok=1 live_unflagged_v3=3 live_unflagged_v4=0 live_tool_errors_v4=0 mutants_declared=6 mutants_killed=4 mutant_classes_killed=attr,method,outflag rev=242c1b4a1bb793d6ca4ac4e3b0da153767e78739 freeze=322b5cd32b4319a05340d249ae752d12a9e6b19f C2_R42_PASS=false
```

C1 exit 0; C2 exit 1. Receipts: `.ufo/evidence/round-42/after/c1-at-242c1b4a.stdout` and
`.ufo/evidence/round-42/after/c2-at-242c1b4a.stdout` (exit files alongside). These are the
deciding runs.

Verdicts as measured: C1 **improved** (m10=1 → 0; the superseding receipt
`.ufo/waves/round-42/supersede/round-41-residual-receipt.json` covers the stale residual
receipt; all six round-41/42 records audit clean). C2 **missed** — the declared mutant set
is 4 of 6 killed, so `C2_R42_PASS=false` and the capability target is not met: the
survivors are `outflag_no_parse_args_check` (killable only by a fixture that registers
`--out` and reads `.out` off a non-parse_args object) and `method_fold_several_returns`
(differs only on dead code). The miss is reported, not narrowed; the surviving mutants stay
committed unchanged (`.ufo/evidence/round-42/census/mutants.json`). Numeric axes unchanged:
depth 9 → 9, calibration 6 → 6 (command D and the round-21 coldread monitor at the base
and at the round commit); no axis is harmed. The v4 tool's wider false-negative classes are
recorded in the lesson and the knowledge entry, outside the frozen claim.

## Round 43 — survivor resolution (depth) + record agreement extended (calibration) + staged-id guard (operability) (2026-10-25)

L1 tameshi, hyaku run 6, attempt 1. Nothing was inherited. Three claims on three distinct axes.
Calibration (6, the round-21 coldread monitor) is the lane's lowest non-retired axis and carries C2;
the stagnation nudge does not fire because round 41 admitted a capability inside the window N=2.
Contract `.ufo/evidence/round-43/contract.json`, frozen at `6b83a11c61f0fad1074ec1f2a4c38a2fd7034685`
before any seat ran and before the first deciding run; amendments A1–A3 are pre-data and change
extraction rules and control paths only (recorded in the contract and the lesson).

| Claim | Axis | Before | After | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|
| C1 the two round-42 survivors are resolved under the pre-declared K/D/E/U rule: `outflag_no_parse_args_check` killed by a reachable-code fixture, `method_fold_several_returns` classified dead-code-only, mutant declaration unchanged | depth | `mutants_declared=6 mutants_killed=4` with both survivors named, exit 1, at base `487b8f0da89fa0e2b8bea6930068accbf36e70a9` (round-42 counter) | target `mutants_killed=5 dead_code_only=1 equivalent=0 unresolved=0 C1_R43_PASS=true`, exit 0 | `python3 .ufo/evidence/round-43/mutants/measure.py --lane LANE --rev REV --freeze 6b83a11c61f0fad1074ec1f2a4c38a2fd7034685` | see the after subsection | `.ufo/evidence/round-43/before/`, `.ufo/evidence/round-43/control/`, `.ufo/evidence/round-43/after/` | see the after subsection |
| C2 the lane's records agree with the tree across seven classes — m6 m7 m8 m10 m11 carried from round 42 plus m12 (the newest SCORECARD block declares the next round's planned claims) and m13 (the newest standing registry command is census-valid and load-bearing on an indented mirror) | calibration (lowest axis) | `m12=1 m13=1 total=2 classes=7 C2_R43_PASS=false`, exit 1, at base `487b8f0da89fa0e2b8bea6930068accbf36e70a9` | target `m6=0 m7=0 m8=0 m10=0 m11=0 m12=0 m13=0 total=0 C2_R43_PASS=true`, exit 0 | `python3 .ufo/evidence/round-43/calibration/measure.py --lane LANE --rev REV --freeze 6b83a11c61f0fad1074ec1f2a4c38a2fd7034685` | see the after subsection | `.ufo/evidence/round-43/before/c2-at-base.stdout`, `.ufo/evidence/round-43/control/`, `.ufo/evidence/round-43/after/` | see the after subsection |
| C3 `tools/staged-id-guard.py` answers the round-42 post-append hazard before any append: census-valid collision extraction, document-keyed dedupe, refusal of its own naive arithmetic map (cascade), admission only of a by-document map at or above the safe floor | operability (capability) | `tool_absent=1 C3_R43_PASS=false`, exit 1, at base (tool not in the rev) | target `C3_R43_PASS=true`, exit 0 | `python3 .ufo/evidence/round-43/guard/measure.py --lane LANE --rev REV --freeze 6b83a11c61f0fad1074ec1f2a4c38a2fd7034685` | see the after subsection | `.ufo/evidence/round-43/before/c3-at-base.stdout`, `.ufo/evidence/round-43/control/c3-constant-empty.stdout`, `.ufo/evidence/round-43/after/` | see the after subsection |

Numeric axes at the base: depth 9 (command D `recorded_cases=9 depth_score=9`), calibration 6
(round-21 coldread monitor `calibration_restraint_score: 6`), both re-run at the base and at the
freeze by wave-1 seat ExecCommandD (`.ufo/waves/round-43/w1/ExecCommandD.md`: the tool, `SHONEN.md`
and the monitor are byte-identical at both revs; the only output differences are the echoed revision
fields). Neither C1 nor C3 edits the runner or a SHONEN box, so neither number is expected to move;
C2's gain is record agreement, C1's is a survivor class, C3's is a capability.

Capabilities table — row admitted this round:

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| staged-id adoption guard | decide, before any append, which ids of a staged registry package collide with the lane registry (0-3-space census pattern), dedupe a staged row whose document the registry already holds, refuse its own naive arithmetic map because the targets are still staged ids, and admit only a by-document map whose held rows dedupe to their registry id and whose new documents take ids at or above the safe floor | deciding receipt `C3_R43: … C3_R43_PASS=true` at the round-43 measured commit, counter `.ufo/evidence/round-43/guard/measure.py`, tool `tools/staged-id-guard.py` @ `03a796c5726c30367d48618f3cbb0226b8dea9bc319171cbf20ffce319c2dca8` | round 43 |

**Planned (round 44):** the whole-set staged adoption the guard's floor rule now admits (a map over
all 103 staged rows, injective and disjoint from the registry), and the two guard refusal classes
wave 2 leaves unfixed; the `cmp` / `git diff --exit-code` comparator lattices stay unmeasured since
round 39.

| sources-registry | curate where the lane learns: opened, tiered, rechecked source rows, mined into admitted entries, census-gated | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0, zero E codes; row count from the census-valid command `grep -cE '^ {0,3}\| S[0-9]{3} \|' corpus/SOURCES.md` → 114 rows at round 43 (the column-zero form of this command is what C2 class m13 replaced; the counter reads the last standing row) ; `corpus/SOURCES.md` | fleet round 1 (kaika) |

### Round 43 — after the deciding run

All three counters ran at `3c4003f6e97e5c787e7538b2eb35d62f49783aaf`, the revision that carries the
records, the wave evidence and the final counter/tool bytes. All three passed:

```
C1_R43: self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=0 fixtures_pass=12/12 run_errors=0 live_ok=3/3 live_unflagged_v4=0 live_tool_errors=0 mutants_declared=6 mutants_killed=5 dead_code_only=1 equivalent=0 not_killed=0 runtime_error=0 apply_error=0 unresolved=0 killed_names=attr_bind_several_assignments,attr_never_resolve_self,method_fold_disabled,outflag_dests_never_recorded,outflag_no_parse_args_check dead_code_names=method_fold_several_returns dead_code_cases=F12_method_two_returns dead_code_arg_ok=1 kill_binding=1 mutants_sha_ok=1 rev=3c4003f6… C1_R43_PASS=true
C2_R43: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=0 m12=0 m13=0 total=0 records=4 sources_rows=114 standing=114 receipts=17 revisions=3 rev=3c4003f6… C2_R43_PASS=true
C3_R43: self_pin=1 tool_absent=0 tool_sha_ok=1 selftest_exit=0 selftest_cases=24 selftest_failed=0 staged_rows=103 live_collisions=7 live_collisions_agree=1 live_held=3 live_held_agree=1 live_unmapped=0 live_cascade=1 live_verdict=refused naive_map_refused=1 safe_map_admitted=1 map_dedupe_live=1 held_refused=1 safe_floor=S256 staged_sha256=020fbeaa… naive_agree=1 substitute=0 rev=3c4003f6… C3_R43_PASS=true
```

All exit 0. Receipts: `.ufo/evidence/round-43/after/c1-at-3c4003f6.{stdout,exit}`,
`c2-at-3c4003f6.{stdout,exit}`, `c3-at-3c4003f6.{stdout,exit}`.

C1 **improved** — the two routed survivors are resolved under the frozen K/D/E/U rule: the outflag
mutant killed by the reachable F11 fixture (kill_binding=1), the method-fold mutant named
dead-code-only with the differential probe and the unreachable second top-level return (dead_code_arg_ok=1);
mutant declaration byte-pinned (mutants_sha_ok=1), round-42 `C2_R42_PASS=false` left untouched.
C2 **improved** — record agreement over the seven classes, `total=0`; the two classes that were live at
the base (m12=1, m13=1; the round-42 block had no `Planned (round 43)` field and the standing command
was column-zero) are zero at the measured commit.
C3 **improved** (capability) — the staged-id guard refuses its naive arithmetic map on the live package
(cascade onto staged ids), dedupes the three held documents, and admits only the by-document map at or
above the floor; the counter's independent recomputation agrees (naive_agree=1, live_held_agree=1).

Numeric axes, measured at `3c4003f6`: depth 9 → 9 (command D), calibration 6 → 6 (round-21 coldread
monitor) — no axis harmed. Receipts: `.ufo/evidence/round-41/census/command-d.stdout` re-run by wave-1
ExecCommandD at base and freeze; the coldread monitor's `calibration_restraint_score: 6` at both revs.

Disclosed limits and wave-2 attack residue: the C1 reachability gate is fixture-granular (a fixture that
contains dead code anywhere excludes that fixture's failure from a kill even when the failing site is
reachable — CritC1Standing); m12/m13 remain presence/pattern checks and the m13 mirror is the counter's
own (MutC2m13Prose); m10 requires a different receipt to re-assert a superseded claim before it is
skipped (MutC2m10Superseder); the guard's document key is path/extension based and a fragment-only
respell of a held URL still escapes dedupe (CritC3Arithmetic F1). All were named in the lesson before
the deciding run; none was used to reach a verdict.

## Round 44 — assignment-value citation repair (calibration) + S089 anchor supersession (freshness) (2026-10-25)

L1 tameshi, hyaku run 6, attempt 1. Two claims on distinct axes. Calibration (6, the round-21 coldread monitor) is the lowest non-retired axis. The stagnation nudge does not fire: round 43 admitted the staged-id guard capability inside window N=2. Contract `.ufo/evidence/round-44/contract.json`, frozen at `ba01973c73ad7de60e5bd19ae08255a1b7ef917e` before the wave and before the first deciding run.

| Claim | Axis | Before | After | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|
| C1 the seven-class record-agreement counter fixes its false m7 classification of the historical `safe_floor=S256` value while preserving unknown/unmined citation detection | calibration (lowest non-retired axis) | round-43 counter at base `506e99c7b73c85711f066895984d501fcf7539cd`: `m7=1 total=1 C2_R43_PASS=false`; round-44 counter at base: `m7=0 m12=1 total=1 C2_R44_PASS=false` | at `ef990aaea3f6546db20feccbff89ac9ab78c5405`: `m6=0 m7=0 m8=0 m10=0 m11=0 m12=0 m13=0 total=0 C2_R44_PASS=true`; assignment-mask control fails T6 when removed | `python3 .ufo/evidence/round-44/calibration/measure.py --lane LANE --rev REV --freeze ba01973c73ad7de60e5bd19ae08255a1b7ef917e` | `ef990aaea3f6546db20feccbff89ac9ab78c5405` | `.ufo/evidence/round-44/after/c1-at-ef990aa.stdout`, `before/c2-old-at-base.stdout`, `before/c2-new-at-base.stdout`, `control/mask-removed.selftest.stdout`, `w1/RevSelftestAudit.md` | improved (measured) |
| C2 S089's stale Stryker HTML digest is superseded by a new opened, mined S160 anchor row without editing S089 in place; S160 cites the new committed snapshot | freshness | `grep -cE '^ {0,3}\| S160 ' corpus/SOURCES.md` → 0 at base; S089 anchor digest `bc572676…e04d` | `grep -cE '^ {0,3}\| S160 ' corpus/SOURCES.md` → 1 at `ef990aaea3f6546db20feccbff89ac9ab78c5405`; snapshot digest `79f6501a…4079ce`; census exit 0 with expected W04 duplicate URL warning | `grep -cE '^ {0,3}\| S160 ' corpus/SOURCES.md`; `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` | `ef990aaea3f6546db20feccbff89ac9ab78c5405` | `before/s160-count.stdout`, `after/s160-count.stdout`, `corpus/lessons/round-44.md` Gate; `.ufo/evidence/round-44/sources/stryker-equivalent-mutants.html`; `corpus/SOURCES.md` S160 | improved (measured) |

### Round 44 — after the deciding run

The round-44 C1 counter ran at `ef990aaea3f6546db20feccbff89ac9ab78c5405`, freeze `ba01973c73ad7de60e5bd19ae08255a1b7ef917e`, exit 0:

```
C2_R44: self_pin=1 classes=7 m6=0 m7=0 m8=0 m10=0 m11=0 m12=0 m13=0 total=0 records=4 sources_rows=115 standing=115 receipts=17 revisions=2 m13_probe=standing=8_column0=114_valid=115 rev=ef990aaea3f6546db20feccbff89ac9ab78c5405 freeze=ba01973c73ad7de60e5bd19ae08255a1b7ef917e C2_R44_PASS=true
```

The first landing attempt at `83beaf980f246412368f89fbe7758375c8ca21e0` had `m6=1 standing=114 actual=115` because the standing registry row had not yet been advanced; that failure was recorded in `corpus/lessons/round-44.md`, a new census-valid standing row was appended, and the target was re-run without changing the predicate. Receipts: `.ufo/evidence/round-44/after/c1-at-83beaf9.stdout` and `c1-at-ef990aa.stdout`. C1 **improved**: the false `m7` on the historical assignment is removed, and all seven classes are zero at the deciding revision.

C2 source-row count: `grep -cE '^ {0,3}\| S160 ' corpus/SOURCES.md` → 0 at base (`before/s160-count.stdout`, exit 1) → 1 at `ef990aaea3f6546db20feccbff89ac9ab78c5405` (`after/s160-count.stdout`, exit 0). Round-end census exited 0, 115 rows, no E-codes; W04 duplicate URL for S160 is expected because S089 already holds that document. C2 **improved**: the opened Stryker snapshot and S160 supersede row correct S089's stale anchor; S089's old row remains unchanged.

The `freshness` axis is added to the tracked axis set this round with a deliberately narrow local score: 0→1 current snapshot-backed source rows for the Stryker equivalent-mutants document (the `S160` count command above). Saturation line 8. This is not a universal claim about all corpus anchors.

No-harm checks at base `506e99c7b73c85711f066895984d501fcf7539cd` and C1 measurement `ef990aaea3f6546db20feccbff89ac9ab78c5405`: command D → `recorded_cases=9 depth_score=9` at both; coldread monitor → `calibration_restraint_score=6`, `sections_covered=60/64` at both. Thus depth 9→9 and calibration 6→6; no numeric-score increase claimed. Base/after receipts: `.ufo/evidence/round-44/{before,after}/commandD.stdout` and `coldread.json`.

**Planned (round 45):** complete and measure the whole-set staged adoption map only after its by-document collision map is validated in scratch; measure the still-open guard refusal classes; and resume the `cmp` / `git diff --exit-code` comparator lattices left unmeasured since round 39. The staged package remains read-only this round.
| sources-registry | curate opened, tiered and rechecked rows, mined into admitted entries, census-gated | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0, zero E codes (expected W04 for the new Stryker row); row count from `grep -cE '^ {0,3}\| S[0-9]{3,} \|' corpus/SOURCES.md` → 115 rows at round 44 | `corpus/SOURCES.md` | 44 |

## Round 45 — held-row live re-verification (freshness) + GoogleTest F3 adoption (coverage) (2026-10-25)

L1 TameshiR45, hyaku run 7, attempt 1. Two claims on distinct axes. Freshness (1, the round-44 one-document unit) is the lane's lowest non-retired axis and carries C1; the stagnation nudge does not fire (freshness is below the saturation line 8). Contract `.ufo/evidence/round-45/contract.json`, frozen at `3310e7be803516ca5934b4e949d91bcec824b179` with both counters, the controls and the GoogleTest snapshots, before any seat ran; `amendments: []`. Base `5891bdb77aba8489683533ae4cdd3b49b5e2626b`.

| Claim | Axis | Before | After | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|
| C1 at least 50 of the 73 held external rows (mined, id ≤ S160, with a URL) are re-verified against live bytes: snapshot fetched 2026-10-25 from the row's own URL, a 6–25-token quote located afresh, and a non-author wave-2 agree with no dispute | freshness (lowest non-retired axis) | `fresh=0 score=0 C1_R45_PASS=false` at freeze (`.ufo/evidence/round-45/before/c1-at-freeze.stdout`) | `verified=73 disputed=2 fresh=71 score=9 C1_R45_PASS=true` (disputed rows S048, S093) | `python3 .ufo/evidence/round-45/freshness/measure.py --lane LANE --rev REV` | the content revision (deciding receipts under `.ufo/evidence/round-45/after/`, committed in the receipts-only commit that follows it) | `.ufo/evidence/round-45/freshness/ledger.json`, `reviews.json`, `sources/`, the 25 judge reports in `.ufo/waves/round-45/w2/`; controls `.ufo/evidence/round-45/control/controls-at-base.stdout` | improved (measured) |
| C2 GoogleTest upstream `docs/advanced.md` and `docs/primer.md` at commit `cd8e73f067129f8489e35c7b51c7a68552b289d2` enter as rows S256/S257 with committed snapshots, each cited by a re-grounded, indexed knowledge entry (frontier F3) | coverage | `rows=0 entries=0 C2_R45_PASS=false` at freeze (`.ufo/evidence/round-45/before/c2-at-freeze.stdout`) | `rows=2 entries=2 indexed=2 row_ids=S256,S257 C2_R45_PASS=true` | `python3 .ufo/evidence/round-45/coverage/measure.py --lane LANE --rev REV` | same content revision | `corpus/knowledge/r8-gtest-order-and-seed.md`, `corpus/knowledge/r8-gtest-primer-independence.md`, `corpus/lessons/round-45.md` Gate, `.ufo/evidence/round-45/assimilation/` | improved (measured) |

The after values above were read off the counters at the wave-2 evidence commit `f6a34f3900789dd3f693e824c4f874385a4177c3` before these records were written; the deciding runs are taken at the content revision that carries these records (QUALITY criterion 86) and committed afterwards in a receipts-only commit. A deciding line that differs from the after cell above voids this row; the report cites the deciding receipts.

Freshness score rule (replaces the round-44 one-document unit): `floor(10 * fresh / 73)` → 0 at freeze, 9 at the deciding run. The round-44 unit stays a monitor: `grep -cE '^ {0,3}\| S160 ' corpus/SOURCES.md` → 1. Distinct documents: 64 of the 65 distinct URLs in the population are fresh (S093's document is the one without a fresh row; S048 shares its URL with fresh S041/S047). Controls before data: a registry-derived ledger (no source opened) verifies 0 of 73 (`quote copied from row`); wave-1 critic CritC1Control built a forged 5-file ledger with a forged results file that passes the whole counter offline, so the counter's per-row gate is not the decisive check — the wave-2 non-author re-fetch is, and it disputed two author-verified rows.

No-harm at base and at the content revision: command D `recorded_cases=9 depth_score=9`; coldread monitor `calibration_restraint_score=6`; root census exit 0. The round-44 record-agreement counter named in the contract's `no_harm` is round-bound (it marks any newest block that is not round 44), so it cannot be green at a round-45 revision; it is reported, not cited green (`corpus/lessons/round-45.md` Mistakes).

**Planned (round 46):** kill the C1/C2 counter selftest survivors (`.ufo/waves/round-45/w1/MutC1Counter.md`, `MutC2Counter.md`, `.ufo/waves/round-45/w2/MutC1Reviews.md`) and add a per-snapshot fetch receipt to the freshness ledger (calibration/operability); re-pin the anchor-refresh candidates in `.ufo/waves/round-45/w2/ConnDriftAnchors.md` (freshness).
| sources-registry | curate opened, tiered and rechecked rows, mined into admitted entries, census-gated | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0, zero E codes; row count from `grep -cE '^ {0,3}\| S[0-9]{3,} \|' corpus/SOURCES.md` → 117 rows at round 45 | `corpus/SOURCES.md` | 45 |

## Round 46 — standing self-assessment re-stated; selftest hardening; flaky-failure ground (2026-10-25)

L1 TameshiR46, hyaku run 7, attempt 1. Three claims on distinct axes: calibration (C1, the lowest non-retired axis, monitor 6), operability (C2) and coverage (C3). Contract `.ufo/evidence/round-46/contract.json`, frozen at `745a583181648cfc7f9c1b476cd1be7dc68f7433` before any seat ran (`amendments: []`); base `683eedde3a50441c34d85a22f5fd5346f8b1ec6d`. The measured results and verdicts are in the subsections below the standing tables.

### Standing self-assessment — re-stated at round 46

This section supersedes, for every value it states, the standing rows of the capability and axis tables above: the round-31 restatement and the dated rows before it stay as written, as dated literals. Each capability row restates the line its frozen command prints at the round-46 revision (the arrow is U+2192), its exit code and, where the statement pins a tool, the first 12 hex of that tool's sha256; the counter `python3 .ufo/evidence/round-46/calibration/measure.py --lane LANE --rev REV --base 683eedde3a50441c34d85a22f5fd5346f8b1ec6d --work EMPTY_DIR` reads exactly these rows (last row wins) and re-runs the 22 commands of `.ufo/evidence/round-46/calibration/statements.json` (sha256 `a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9`). Values are what each command printed at records revision `a6892b196f923efbed242ce9ea599a3f745b2138`; the `What` and `First-working round` cells are carried unchanged from each capability's previous last row.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | curate where the lane learns: opened, tiered, rechecked source rows, mined into admitted entries, census-gated | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → `rows=120 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`, exit 0 | fleet round 1 (kaika) |
| mutation sweep runner | inject → run → restore single-edit mutants with a green-control gate, verdict lines and byte-identity proof; `--regression` refuses a miscounted tally (round 30) | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 106/106 pass`, exit 0, tool sha256 `a7d3f2dd7d47` | historical round 3; re-demonstrated round 31 |
| six-leg regression ledger | replay every recorded mutation case (nine legs since round 26; the name is kept as the row id) at its pinned blob; exact expectation | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=9 passed=9`, exit 0 | historical round 7 (four legs) / round 10 (six) / round 26 (nine) |
| repeated pristine-control gate | observe N≥3 exact exit/stdout/stderr tuples, distinguish mismatch from unavailable/uniform-nonzero baseline, validate digest-pinned observation snapshots | `python3 tools/repeat-control.py --selftest` → `SELFTEST: PASS (29 cases)`, exit 0, tool sha256 `296fe566dc59` | round 12 |
| six-leg content-disposition probe | emit configured-pin, committed-HEAD and worktree SHA observations for every recorded leg, while explicitly withholding verdict reuse | `python3 tools/pin-disposition.py --selftest` → `SELFTEST: PASS (19/19)`, exit 0, tool sha256 `331529eadafe` | round 13 |
| exposed witness provenance correction | validate a new digest-anchored non-blind companion without rewriting frozen observations | `python3 tools/witness-metadata.py --selftest` → `SELFTEST: PASS 39/39`, exit 0, tool sha256 `df3390682a04` | round 13 |
| effective expectation reconciliation | account for every historical expected row, reject an exit-only setup crash, and preserve that raw failure under a checked explicit oracle supersession | `python3 tools/evidence-disposition.py --selftest` → `SELFTEST: PASS (66/66)`, exit 0, tool sha256 `39ee5c5effd9` | round 14 |
| retained invocation-context gate | re-derive bounded raw receipt predicates, check byte-pinned frozen receipts, and distinguish semantic mismatch from unavailable/tampered input through a standalone public-CLI selftest | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72` → `SELFTEST: PASS (49/49)`, exit 0, tool sha256 `7e4519d9a0ea` | round 15 |
| hermetic env-differential probe | classify the raw exit/stdout/stderr tuple of nine pinned selftests under seven explicit profiles; the committed receipt `.ufo/evidence/round-21/f5/receipt-initial.json` classes eight `invariant` and one `nondeterministic` (`js-round-gate`), not "raw-output-variable" as the row above says | `python3 tools/env-diff.py --selftest` → `ENVDIFF_SELFTEST: 9/9 pass`, exit 0, tool sha256 `e8b47ab7cf23` | round 21 |
| callback-authoritative wave accounting | reconcile exact registered identities and terminal states while preserving failed seats' partial artifacts; reject mismatched totals and digest tampering | `python3 tools/wave-accounting.py --selftest` → `ACCOUNTING_SELFTEST: 8/8 pass`, exit 0, tool sha256 `96b3038a77f8` | round 22 |
| required-command-receipt-binding | validate a finite trusted bundle's exact named command/context/outcome declarations | `python3 tools/command-binding.py --selftest` → `COMMAND_BINDING_SELFTEST: 44/44 pass`, exit 0, tool sha256 `9230c68e53a5` | round 23 |
| refusing-registry-replay | replay frozen registry requirements and refuse to publish a binding bundle from rejected rows | `python3 tools/registry-replay.py --selftest` → `REGISTRY_REPLAY_SELFTEST: 10/10 pass`, exit 0, tool sha256 `9fcd2dbba737` | round 24 |
| mutation report interop | emit each recorded leg as a mutation-testing-elements report and check it with the official schema and metrics library | `python3 tools/mte-interop.py --selftest` → `MTE_SELFTEST: 17/17 pass`, exit 0, tool sha256 `193ea6e32f89` | round 25 |
| tally-audit-v2 runner audit | audit the mutation runner's regression tally without editing it: head/static/runtime/harness checks kill all 18 public + 8 sealed must-kill copies and accept all 8 public + 6 sealed must-accept copies, zero invalid sealed copies, controls-gated counter | `python3 tools/tally-audit-v2.py --selftest` → `TALLY_AUDIT_V2_SELFTEST: 22/22 pass`, exit 0, tool sha256 `7b11ba25aead` | round 34 (tool landed round 33, predicate honestly not decided there) |
| tally-audit-v3 runner audit | audit the runner's regression tally without editing it, across all four `(root,auto,KEEP)` triples, comparing the FULL stdout plus exit and scanning a comment-blinded code view; kills 6/6 public + 4/4 sealed must-kill copies (failing check exactly `runtime`), accepts 3/3 public + 3/3 sealed must-accept copies, zero invalid sealed copies, under a pinned sha256 | `python3 tools/tally-audit-v3.py --selftest` → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, exit 0, tool sha256 `da8c1ef4b30c` | round 35 |
| bounded ANSI-C code_view | Keep Bash `$'...'` quoted text intact across escaped single quotes, blank a following comment, and preserve a literal `#` inside the quote; nested substitutions and unquoted backslash-newline remain unsupported | `python3 tools/tally-audit-v3.py --selftest` → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, exit 0, tool sha256 `da8c1ef4b30c` | round 37 |
| write-path-census-v2 | classify a string-literal `expected.json` on `.write_bytes` and an `os.replace` / `os.rename` write, which the round-39 census misses, with planted flagged and scratch controls | `python3 tools/write-path-census-v2.py --selftest` → `WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0`, exit 0, tool sha256 `402285329588` | round 40 |
| write-path census destination resolution | resolve a write destination held in a variable through up to four assignments/`os.path.join`/`+`/`/`/f-string hops and classify it as expected-value, scratch or update-flagged, for `open`, `write_text`/`write_bytes`, `os.replace`/`os.rename` and `os.symlink`; v2 cannot connect a destination to a token that is not on the same line | `python3 tools/write-path-census-v3.py --selftest` → `WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0`, exit 0, tool sha256 `095924a7a165` | round 41 |
| staged-id adoption guard | decide, before any append, which ids of a staged registry package collide with the lane registry (0-3-space census pattern), dedupe a staged row whose document the registry already holds, refuse its own naive arithmetic map because the targets are still staged ids, and admit only a by-document map whose held rows dedupe to their registry id and whose new documents take ids at or above the safe floor | `python3 tools/staged-id-guard.py --selftest` → `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0`, exit 0, tool sha256 `03a796c5726c` | round 43 |

| Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
|---|---|---|---|---|
| depth | 9 | One point per recorded mutation case in the runner's ledger comment (`tools/mutate-and-run.sh:87-95`, nine legs), capped at 10; command D prints `recorded_cases=9 depth_score=9` (`.ufo/evidence/round-46/before/no-harm-at-base.stdout`, `after/no-harm.stdout`) | round-46 content revision (deciding receipts `.ufo/evidence/round-46/after/`) | 26 (held) |
| calibration | 6 | Restraint score of the strict cold-read monitor `python3 .ufo/evidence/round-21/coldread/measure.py --repo R --rev REV` (`calibration_restraint_score`; `box3_full_page=false`, 60 of 64 sections credited): two points per restrained, evidence-linked `[~]` SHONEN box; box 3 is not credited. The round-31 table above stated 8; the monitor prints 6 at the round-46 base, so 8 was a stale standing value | round-46 content revision | 46 (restated 8 → 6; no raise claimed) |
| freshness | 9 | `floor(10 * fresh / 73)` from the round-45 counter `python3 .ufo/evidence/round-45/freshness/measure.py --lane LANE --rev REV` (`fresh=71`, `score=9`; 2 rows disputed: S048, S093); the round-44 one-document unit (the S160 row count, 1; command in the round-45 block above) stays a monitor | round-46 content revision | 45 |

### Round 46 — claims, measurement and verdicts

| Claim | Axis | Before | After | Counting command | Measured commit | Evidence | Verdict |
|---|---|---|---|---|---|---|---|
| C1 the standing SCORECARD rows of 22 frozen statements state what each statement's frozen command prints (value, exit code, tool sha256 prefix): mismatches + unparsed + unobservable = 0 | calibration (lowest non-retired axis; monitor 6, unchanged) | `total=21` (mismatches 2: calibration stated 8 vs observed 6, the regression row quoted a truncated line; unparsed 19) at the freeze (`.ufo/evidence/round-46/before/c1-at-freeze.stdout`) | `total=0` `C1_R46_PASS=true` at records revision `e630ae791a831828f51b8f192996a907ff8ed78d` | `python3 .ufo/evidence/round-46/calibration/measure.py --lane LANE --rev REV --base 683eedde3a50441c34d85a22f5fd5346f8b1ec6d --work EMPTY_DIR` | the content revision (deciding receipts `.ufo/evidence/round-46/after/c1.stdout`) | `.ufo/evidence/round-46/calibration/`, standing tables above, `corpus/lessons/round-46.md` | improved (measured) |
| C2 the round-45 counters' selftests kill at least 23 of 25 declared survivors and none of 6 neutral mutants, with equal output on the round-45 data revision | operability (first scored this round) | `killed=0 survived=25` against the round-45 counters (`before/c2-at-freeze.stdout`, `--targets orig`) | `killed=25 survived=0 neutral_killed=0 pristine=1 equivalence=1` `C2_R46_PASS=true` at `a6892b196f923efbed242ce9ea599a3f745b2138` | `python3 .ufo/evidence/round-46/hardening/mutate.py --lane LANE --rev REV --targets hardened` | the content revision (`.ufo/evidence/round-46/after/c2.stdout`) | `.ufo/evidence/round-46/hardening/{freshness,coverage}-counter.py`, `mutants.json`, six seat additions `.ufo/waves/round-46/w1/Hard*.addition.py` | improved (measured) |
| C3 three flaky-failure documents enter as rows S258/S259/S260, each cited by a re-grounded, indexed entry with a located quote absent from the package copy | coverage (frontier F3; sourced, assimilation) | `rows=0 entries=0 C3_R46_PASS=false` at the freeze (`before/c3-at-freeze.stdout`) | `rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260` `C3_R46_PASS=true` at `a6892b196f923efbed242ce9ea599a3f745b2138` | `python3 .ufo/evidence/round-46/coverage/measure.py --lane LANE --rev REV` | the content revision (`.ufo/evidence/round-46/after/c3.stdout`) | `corpus/knowledge/r6-flaky-failures-cluster.md`, `r5-undetected-flaky-failures.md`, `r9-false-red-rate.md`, `corpus/lessons/round-46.md` `## Gate`, `.ufo/evidence/round-46/assimilation/` | improved (measured); expansion credit for two of three entries (the third restates a held claim through a readable carrier) |

The after values above were read off the counters at the wave-1 evidence commits named in the cells before these records were written; the deciding runs are taken at the content revision that carries these records (QUALITY criterion 86) by `.ufo/evidence/round-46/deciding-run.sh`, which also prints `FROZEN_UNCHANGED=1` (no counter, statements list, manifest, snapshot, package copy or contract changed since the freeze) and is committed afterwards in a receipts-only commit. A deciding line that differs from an after cell voids that row; the report cites the deciding receipts.

Operability score (new this round, narrow): `floor(10 * killed / 25)` over the declared mutant set, 0 at the freeze and 10 at the after cell; the comparable measure is the count `killed 0 → 25 of 25` (the same definitional caution as the round-45 freshness score applies). Calibration monitor: 6 → 6 (the restated axes table corrects the stale standing value 8 to the monitor's 6; no raise is claimed). Depth 9 → 9; freshness 9 → 9.

No-harm at base and at the records revisions: `.ufo/evidence/round-46/no-harm.sh` prints ok for all six monitors (`before/no-harm-at-base.stdout`; at the deciding run `after/no-harm.stdout`). The round-44 record-agreement counter is not a monitor: it prints `C2_R44_PASS=false` at base by construction (QUALITY criterion 88).

Controls before data (`.ufo/evidence/round-46/control/controls-at-freeze.stdout`): C3 package entries copied byte-exact `entries=0`; relabelled (header rewritten, quotes kept) `entries=0`; rows only `entries=0`; wrong digest `rows=0`. C2 selftest that pins its own byte length `killed=21 neutral_killed=6` false; always-failing selftest `pristine=0` false; round-45 counters unchanged `killed=0`. C1: the unchanged tree is the control (`total=21`); selftest T14/T16 refuse an edited or shortened statements list.

Disclosed limits and wave-1 attack residue (named before the deciding runs; none was used to reach a verdict): the C1 counter is pinned to its own committed bytes, so a later one-line edit of the counter passes it (CritC1Control cheat Z) — the deciding run therefore checks `git diff` of the frozen paths between the freeze and the content revision; five of the 22 statements pin no tool file (a tool edited together with its row is consistent by construction, cheat g2); the C3 counter accepts a relabel written at a different basename or with the package copies deleted (Vd3, Vd5) — the deciding run checks the entry basenames and the package copies; the C3 and C2 counters' own selftests leave 4 and 8 mutants alive (MutC3Counter, MutDriver), routed below; `no-harm.sh` exits 0 with `RED` lines, so the deciding run greps it.

Capabilities demonstrated this round (rows enter only through a demonstrated run; none is among the 22 frozen statements):

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| standing-statement counter | re-run 22 frozen commands and compare each to the last SCORECARD row that states it (value, exit, tool sha256 prefix), refusing an edited statements list, an unparseable row and a non-append-only edit | `python3 .ufo/evidence/round-46/calibration/measure.py --selftest` → `C1_R46_SELFTEST: cases=18 failed=0`, exit 0; before `total=21`, after `total=0` (`before/c1-at-freeze.stdout`, `after/c1.stdout`) | round 46 |
| declared-mutant driver with neutral controls | apply declared old→new mutants to a counter's source, refuse a selftest that kills a neutral mutant or fails pristine, and compare a hardened counter's output with its original over a data revision | `python3 .ufo/evidence/round-46/hardening/mutate.py --selftest` → `C2_R46_SELFTEST: cases=8 failed=0`, exit 0; `--targets orig` `killed=0`, `--targets hardened` `killed=25` | round 46 |
| no-harm-at-base gate and seat-name collision gate | refuse a contract whose no_harm monitor is red at the base; refuse a wave whose seat names are in use by another lane's concurrent wave | `python3 .ufo/evidence/round-46/quality/no-harm-gate.py --selftest` → `20/20 passed`; `python3 .ufo/evidence/round-46/quality/seat-name-check.py --selftest` → `SEAT_NAME_SELFTEST: cases=4 failed=0`; falsifiers `quality/c88-90-falsifiers.stdout` | round 46 |

**Planned (round 47):** route the frozen counters' selftest gaps (`.ufo/waves/round-46/w1/MutC3Counter.md`, `MutDriver.md`) into a successor hardening claim; continue frontier F3 with the next reachable package rows (`w1/ConnPackageCross.md` ranks S155 arXiv 2302.09330, S169 and S206 first, S158's PDF needs a committed text snapshot); pin the five statements of the standing list that name no tool file (sources-registry, six-leg regression ledger, depth, calibration, freshness) by sha256 beside the statement.

### Round 46 — wave-2 results, errata and disclosed limits (appended before the deciding runs)

Wave 2: 35 seats, all settled with a report, names prefixed `T46` after the wave-1 seat-name collision (QUALITY criterion 90); no dead seat (`.ufo/waves/round-46/w2-results.json`). The findings below are the ones that change a record or a claim's reading; each was fixed in the same-round files before the deciding runs or is routed.

Errata to the standing tables above (append-only; the tables stay as written, these lines qualify them):

- **Calibration row, section count.** The cell reads "60 of 64 sections credited". That is the cold-read monitor's value at the base and at records revision `e630ae79`; at the first content revision `6f2168e028ce7ff6e82ac92093ac05dd1f147c32` it printed 55 of 64, because this round's own `PROVINCE.md` append drifted a cold-read input (five sections lost credit: Standing rules, Kill-rate bands, Cross-language divergence, Third case, The service's limits). Three wave-2 seats found it (T46CritRestated F1, T46CritC1 F1, T46ReobsA F1). The `PROVINCE.md` append was reverted to the base bytes and `deciding-run.sh` now requires at least 60 credited sections. The score (6) was never affected.
- **Calibration row, rule.** The cell drops the clause of the round-31 rule: box 3 is credited only when the monitor credits the full page, and the last 2 points need independent promotion review of all four SHONEN boxes. Restated: the lane-attainable cap is 8; at the round-46 revision box 3 is not credited (`box3_full_page=false`) and no box has independent promotion review, so 6 is the measured value and 8 is not attainable by this lane's own action (T46CritRestated F3).
- **Scope of the supersession.** "Supersedes, for every value it states" means: for the values of the 22 frozen statements. The earlier tables' other cells (measured commits, descriptions) remain dated literals (T46CritRestated F2).
- **What a printed line proves.** Seventeen of the 19 capability rows restate a selftest tally; the tally proves the tool's selftest passes at the revision, not every clause of the row's `What` cell. Named narrowings: the `six-leg content-disposition probe` covers six recorded legs, the runner's ledger records nine (the other three are not compared; T46ReobsC F1); the `sources-registry` census gates the 13-cell shape, the tier/status/kind enums, duplicate ids and used-by existence, not "opened" or "rechecked" (T46ReobsC F3); the `bounded ANSI-C code_view` row restates the tally-audit-v3 selftest, and the code_view receipts are `.ufo/evidence/round-37/code-view/after.stdout` (2/2) and `.ufo/evidence/round-37/tool-selftest-after.stdout` (35/35) (T46CritRestated F6); the `six-leg regression ledger` row states the frozen statement's capture, `REGRESSION: PASS (cases=9 passed=9`, a prefix of the printed line (T46ReobsB F1, T46CritC1 F2).
- **Three standing statements are not hermetic.** The `retained invocation-context gate` exit code depends on a census run over the live fleet root and on `jj`/`bwrap` being on `PATH` for two siblings (T46ReobsD §7): `C1_R46_PASS=true` is a statement about this host at this revision, not a function of the revision alone. Routed.
- **C1 and C3 are coupled through one value.** The `sources-registry` row states `rows=120`, which counts C3's three rows (T46RevSeparable F1); each counter still verifies without the other's artifacts, but C1's row value moves with C3.
- **C3 verdict wording.** The C3 "Verdict" cell says the third entry restates a held claim "through a readable carrier"; the lane's extractor reads that claim from the held rendered page too (T46CritEntryFalseRed F12). The corrected wording: a second, byte-stable, pinned carrier. Expansion credit stays two entries of three.
- **Revision naming.** The restated rows' values were observed by `--emit` at records revision `a6892b196f923efbed242ce9ea599a3f745b2138` (the tables did not exist there; they were appended at `e630ae791a831828f51b8f192996a907ff8ed78d`), the C1 pass was read off at `e630ae79…`, and the deciding run is taken at the final content revision named in the report; the 22 values are identical at all three (no tool changed, the registry row count has been 120 since `a6892b19`), which the deciding receipt re-checks.
- **Operability score.** The 0 → 10 cell is a definitional first score on a set the authors were given (T46CritC2 F3); the comparable measure is the count `killed 0 → 25 of 25` and the capability rows above. No operability score is claimed as comparable to depth or freshness.

Wave-2 findings that do not change a verdict but qualify C2 (disclosed before the deciding runs):

- The frozen `equivalence` check masks `self_pin=` and the PASS token, the two tokens on which the hardened copies differ from the originals (their own path is absent at the round-45 data revision), so `equivalence=1` cannot see a verdict regression (T46CritC2 F1). Supplementary receipt `.ufo/evidence/round-46/after/extra-receipts.stdout`: with the hardened copy's `self_pin` line forced to 1, its stdout is byte-identical to the round-45 counter's over `ea25e022…` with nothing masked, for both counters.
- A selftest that pins the AST of its own source, with no rule assertion, would also reach `killed=25 neutral_killed=0` (T46CritC2 F2), because the six neutral mutants are AST-identical. The delivered selftests are not that: the same receipt lists, for each of the 25 declared mutants, the first `FAIL <rule case>` line (25 of 25 named rule cases, none a crash or a source-text pin; T46CritHarden agrees). The control that would refuse an AST pin is routed.
- Generalization: four wave-2 mutation seats applied 73 fresh single-line mutants (outside `mutants.json`) to the two hardened counters: 17 were killed and 56 survived (freshness 14 of 19 and 16 of 18 survive, coverage 12 of 16 and 14 of 20; a few are equivalent). The additions pin the declared rules and little more; killing cases for the real gaps are attached as code in `.ufo/waves/round-46/w2/T46Mut*.md` and routed to round 47.
- The operative counters are untouched: the credit lands on the hardened copies, which become the lane's counters only when a later round adopts them (T46CritC2 F4).

Disposition of the round-45 `Planned (round 46)` items: the first (kill the C1/C2 counter selftest survivors) is answered by C2; the second (a per-snapshot fetch receipt in the freshness ledger) and the third (re-pin the anchor-refresh candidates of `.ufo/waves/round-45/w2/ConnDriftAnchors.md`) were not worked and stay open for round 47 (T46ScoutCorrections #2).

**Planned (round 47), additions:** absorb the wave-2 killing cases into the hardened counters and re-attack them with a sealed held-out mutant set; add an AST-pin control to the C2 control set and count a mutant as killed only when a named rule case fails; give the frozen statements a hermetic observation (pin `jj`/`bwrap`/census inputs) and the five tool-less statements a sha256; carry the round-45 per-snapshot fetch receipt and anchor-refresh items.


## Round 47 — dependence-declaring standing rows; mutant-pool hardening; F3 measurement ground (2026-10-25)

L1 TameshiR47, hyaku run 7, attempt 1. Three claims on distinct axes: calibration (C1, the lowest non-retired axis, monitor 6), operability (C2) and coverage (C3). Contract `.ufo/evidence/round-47/contract.json`, frozen at `9acfbe21435e1976636a276448dee1d5e7155915` before any seat ran (`amendments: []`); base `0b5b7cd2b2c15d23086e811a0f0348d84261277b`. The measured results are in the report and the table below; the deciding runs are taken at the content revision by `.ufo/evidence/round-47/deciding-run.sh` (QUALITY criterion 86).

### Standing self-assessment — re-stated at round 47

This section supersedes, for the 22 frozen statements, the standing rows of the tables above: the round-46 restatement and earlier rows stay as written, as dated literals. Each row restates the line its frozen command prints under the live host profile P0, its exit code, the first 12 hex of the pinned tool's sha256 (all 22 now) and a `deps` clause: the dependences observed by `python3 .ufo/evidence/round-47/calibration/measure.py --lane LANE --rev REV --base 0b5b7cd2b2c15d23086e811a0f0348d84261277b --work EMPTY_DIR` (statements sha256 `924102dfbc6135a7d9dabef7b8b2e681a5ce4c42ca72a031ea1f8d5ab9fb2e56`). `deps none` means five variants (clean environment, no bwrap, no jj, no node, a decoy fleet root) changed nothing; it is not a hermeticity claim (free disk in /tmp, for one, is not varied: `/tmp` filling killed two probe runs this round). The `sources-registry` row states `rows=124`, which counts C3's four new rows (the C1/C3 coupling of round 46 persists).

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | curate where the lane learns: opened, tiered, rechecked source rows, mined into admitted entries, census-gated | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → `rows=124 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`, exit 0, tool sha256 `b9b754713c9c`, deps `none` | fleet round 1 (kaika) |
| mutation sweep runner | inject → run → restore single-edit mutants with a green-control gate, verdict lines and byte-identity proof; `--regression` refuses a miscounted tally (round 30) | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 106/106 pass`, exit 0, tool sha256 `a7d3f2dd7d47`, deps `none` | historical round 3; re-demonstrated round 31 |
| six-leg regression ledger | replay every recorded mutation case (nine legs since round 26; the name is kept as the row id) at its pinned blob; exact expectation | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: FAIL (cases=9 passed=7`, exit 1, tool sha256 `a7d3f2dd7d47`, deps `env,fleet-root,node` | historical round 7 (four legs) / round 10 (six) / round 26 (nine) |
| repeated pristine-control gate | observe N≥3 exact exit/stdout/stderr tuples, distinguish mismatch from unavailable/uniform-nonzero baseline, validate digest-pinned observation snapshots | `python3 tools/repeat-control.py --selftest` → `SELFTEST: PASS (29 cases)`, exit 0, tool sha256 `296fe566dc59`, deps `none` | round 12 |
| six-leg content-disposition probe | emit configured-pin, committed-HEAD and worktree SHA observations for every recorded leg, while explicitly withholding verdict reuse | `python3 tools/pin-disposition.py --selftest` → `SELFTEST: PASS (19/19)`, exit 0, tool sha256 `331529eadafe`, deps `none` | round 13 |
| exposed witness provenance correction | validate a new digest-anchored non-blind companion without rewriting frozen observations | `python3 tools/witness-metadata.py --selftest` → `SELFTEST: PASS 39/39`, exit 0, tool sha256 `df3390682a04`, deps `none` | round 13 |
| effective expectation reconciliation | account for every historical expected row, reject an exit-only setup crash, and preserve that raw failure under a checked explicit oracle supersession | `python3 tools/evidence-disposition.py --selftest` → `SELFTEST: PASS (66/66)`, exit 0, tool sha256 `39ee5c5effd9`, deps `jj` | round 14 |
| retained invocation-context gate | re-derive bounded raw receipt predicates, check byte-pinned frozen receipts, and distinguish semantic mismatch from unavailable/tampered input through a standalone public-CLI selftest | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72` → `SELFTEST: PASS (49/49)`, exit 0, tool sha256 `7e4519d9a0ea`, deps `fleet-root` | round 15 |
| hermetic env-differential probe | classify the raw exit/stdout/stderr tuple of nine pinned selftests under seven explicit profiles; the committed receipt `.ufo/evidence/round-21/f5/receipt-initial.json` classes eight `invariant` and one `nondeterministic` (`js-round-gate`), not "raw-output-variable" as the row above says | `python3 tools/env-diff.py --selftest` → `ENVDIFF_SELFTEST: 9/9 pass`, exit 0, tool sha256 `e8b47ab7cf23`, deps `bwrap,node` | round 21 |
| callback-authoritative wave accounting | reconcile exact registered identities and terminal states while preserving failed seats' partial artifacts; reject mismatched totals and digest tampering | `python3 tools/wave-accounting.py --selftest` → `ACCOUNTING_SELFTEST: 8/8 pass`, exit 0, tool sha256 `96b3038a77f8`, deps `none` | round 22 |
| required-command-receipt-binding | validate a finite trusted bundle's exact named command/context/outcome declarations | `python3 tools/command-binding.py --selftest` → `COMMAND_BINDING_SELFTEST: 44/44 pass`, exit 0, tool sha256 `9230c68e53a5`, deps `none` | round 23 |
| refusing-registry-replay | replay frozen registry requirements and refuse to publish a binding bundle from rejected rows | `python3 tools/registry-replay.py --selftest` → `REGISTRY_REPLAY_SELFTEST: 10/10 pass`, exit 0, tool sha256 `9fcd2dbba737`, deps `none` | round 24 |
| mutation report interop | emit each recorded leg as a mutation-testing-elements report and check it with the official schema and metrics library | `python3 tools/mte-interop.py --selftest` → `MTE_SELFTEST: 17/17 pass`, exit 0, tool sha256 `193ea6e32f89`, deps `node` | round 25 |
| tally-audit-v2 runner audit | audit the mutation runner's regression tally without editing it: head/static/runtime/harness checks kill all 18 public + 8 sealed must-kill copies and accept all 8 public + 6 sealed must-accept copies, zero invalid sealed copies, controls-gated counter | `python3 tools/tally-audit-v2.py --selftest` → `TALLY_AUDIT_V2_SELFTEST: 22/22 pass`, exit 0, tool sha256 `7b11ba25aead`, deps `none` | round 34 (tool landed round 33, predicate honestly not decided there) |
| tally-audit-v3 runner audit | audit the runner's regression tally without editing it, across all four `(root,auto,KEEP)` triples, comparing the FULL stdout plus exit and scanning a comment-blinded code view; kills 6/6 public + 4/4 sealed must-kill copies (failing check exactly `runtime`), accepts 3/3 public + 3/3 sealed must-accept copies, zero invalid sealed copies, under a pinned sha256 | `python3 tools/tally-audit-v3.py --selftest` → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, exit 0, tool sha256 `da8c1ef4b30c`, deps `none` | round 35 |
| bounded ANSI-C code_view | Keep Bash `$'...'` quoted text intact across escaped single quotes, blank a following comment, and preserve a literal `#` inside the quote; nested substitutions and unquoted backslash-newline remain unsupported | `python3 tools/tally-audit-v3.py --selftest` → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, exit 0, tool sha256 `da8c1ef4b30c`, deps `none` | round 37 |
| write-path-census-v2 | classify a string-literal `expected.json` on `.write_bytes` and an `os.replace` / `os.rename` write, which the round-39 census misses, with planted flagged and scratch controls | `python3 tools/write-path-census-v2.py --selftest` → `WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0`, exit 0, tool sha256 `402285329588`, deps `none` | round 40 |
| write-path census destination resolution | resolve a write destination held in a variable through up to four assignments/`os.path.join`/`+`/`/`/f-string hops and classify it as expected-value, scratch or update-flagged, for `open`, `write_text`/`write_bytes`, `os.replace`/`os.rename` and `os.symlink`; v2 cannot connect a destination to a token that is not on the same line | `python3 tools/write-path-census-v3.py --selftest` → `WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0`, exit 0, tool sha256 `095924a7a165`, deps `none` | round 41 |
| staged-id adoption guard | decide, before any append, which ids of a staged registry package collide with the lane registry (0-3-space census pattern), dedupe a staged row whose document the registry already holds, refuse its own naive arithmetic map because the targets are still staged ids, and admit only a by-document map whose held rows dedupe to their registry id and whose new documents take ids at or above the safe floor | `python3 tools/staged-id-guard.py --selftest` → `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0`, exit 0, tool sha256 `03a796c5726c`, deps `none` | round 43 |

| Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
|---|---|---|---|---|
| depth | 9 | One point per recorded mutation case in the runner's ledger comment (`tools/mutate-and-run.sh:87-95`, nine legs), capped at 10; command D prints `recorded_cases=9 depth_score=9` (`.ufo/evidence/round-46/before/no-harm-at-base.stdout`, `after/no-harm.stdout`), tool sha256 `a7d3f2dd7d47`, deps `none` | round-47 content revision | 47 (restated) |
| calibration | 6 | Restraint score of the strict cold-read monitor `python3 .ufo/evidence/round-21/coldread/measure.py --repo R --rev REV` (`calibration_restraint_score`; `box3_full_page=false`, 60 of 64 sections credited): two points per restrained, evidence-linked `[~]` SHONEN box; box 3 is not credited. The round-31 table above stated 8; the monitor prints 6 at the round-46 base, so 8 was a stale standing value, tool sha256 `657f009bdf1c`, deps `none` | round-47 content revision | 47 (restated) |
| freshness | 9 | `floor(10 * fresh / 73)` from the round-45 counter `python3 .ufo/evidence/round-45/freshness/measure.py --lane LANE --rev REV` (`fresh=71`, `score=9`; 2 rows disputed: S048, S093); the round-44 one-document unit (the S160 row count, 1; command in the round-45 block above) stays a monitor, tool sha256 `ba64041f49ff`, deps `none` | round-47 content revision | 47 (restated) |

### Round 47 — claims, measurement and verdicts

| Claim | Axis | Before | After | Counting command | Evidence |
|---|---|---|---|---|---|
| C1 22 standing rows state value, exit, tool sha256 and the observed `deps` set: total = mismatches + unparsed + unobservable + dep_mismatch + unpinned = 0 | calibration (monitor 6, unchanged; no raise claimed) | `total=22` at the freeze (`before/c1-at-freeze.stdout`) | see the report (deciding receipt `after/c1.stdout`) | `python3 .ufo/evidence/round-47/calibration/measure.py --lane LANE --rev REV --base 0b5b7cd2b2c15d23086e811a0f0348d84261277b --work EMPTY_DIR` | controls `control/controls-at-freeze.stdout` CTL_I (22), CTL_J (`dep_mismatch=5`), CTL_K (`total=0`) |
| C2 the v2 counters' selftests kill at least 150 of 183 pool mutants, none of 14 neutral | operability | `killed=122` (`before/pool-base.stdout`) | see the report (`after/c2.stdout`) | `python3 .ufo/evidence/round-47/hardening/pool.py --lane LANE --rev REV --targets v2` | nine seat additions `.ufo/waves/round-47/w1/T47Hard*.addition.py`; CTL_E/F/G/H; in-band oracle cheat disclosed (`w1/T47CritC2Control.md`), `quality/addition-lint.py` |
| C3 rows for three frozen documents each cited by a re-grounded, indexed entry | coverage (F3; sourced, assimilation) | `rows=0 entries=0` (`before/c3-at-freeze.stdout`) | see the report (`after/c3.stdout`) | `python3 .ufo/evidence/round-47/coverage/measure.py --lane LANE --rev REV` | `corpus/lessons/round-47.md` `## Gate`; rows S261-S264 |

The after values are read from the deciding receipts, never from this table (a deciding line that differs voids the row). Numeric axes: depth 9 and freshness 9 unchanged; calibration monitor 6 unchanged; operability and coverage carry no numeric score.

Capabilities demonstrated this round (rows enter only through a demonstrated run):

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| dependence-observing standing-statement counter | observe 22 frozen commands under six profiles and require each standing row's `deps` clause to equal the observed set, refusing a missing clause, an unpinned statement and an edited statements list | `python3 .ufo/evidence/round-47/calibration/measure.py --selftest` → `C1_R47_SELFTEST: cases=35 failed=0`; CTL_J `dep_mismatch=5`, CTL_K `total=0` | round 47 |
| deterministic mutant-pool scorer | enumerate single-site AST mutants of a counter's rule code, apply them by address, credit a kill only on a named `FAIL` line, and refuse a selftest that kills the 14 neutral commute edits | `python3 .ufo/evidence/round-47/hardening/pool.py --selftest` → `C2_R47_SELFTEST: cases=14 failed=0`; baseline `killed=122` | round 47 |
| lesson-quote byte-fidelity checker and addition lint | refuse a lesson quote that matches a snapshot only after folding, and a seat addition that embeds an oracle | `python3 .ufo/evidence/round-47/quality/lesson-quote-check.py --selftest` → `cases=11 failed=0`; `addition-lint.py --selftest` → `cases=7 failed=0` | round 47 |

**Planned (round 48):** adopt the carried round-45 items (per-snapshot fetch receipt and anchor refresh for S026/S093/S108, not worked in rounds 46-47); delete or re-pin the two dead `brace_depth_at` helpers (`tools/tally-audit-v2.py:135`, `tools/tally-audit-v3.py:234`; both are sha-pinned in standing rows); give the C1 counter selftest cases for its eight survivors (`w1/T47MutC1Counter.md`) and the C3 counter for its ten (`w1/T47MutC3Counter.md`); a located-name check for entry authorship; continue F3/F7 from the package (S161/S162/S205 candidates).

Disclosed limit (before the deciding run): two of the 22 observations are not stable across runs under host load. Across the four full observations taken so far (the pre-freeze `--emit` `control/emit-observed-pre-freeze.out`, the freeze receipt, the wave-1 probes `.ufo/waves/round-47/w1/T47ExecObs*.md` and the content-revision `--emit` the rows above restate), `hermetic env-differential probe` printed `9/9` or `2/9` under the same profile (P1) and its dependence set was {env, node} in one run and {bwrap, node} in another, and `six-leg regression ledger` printed `FAIL (cases=9 passed=7` once under P0 and `FAIL (cases=9 passed=8` once under P3. The rows above restate the content-revision `--emit`; a deciding run that observes a different set for either statement is a `dep_mismatch` and is reported as such, not re-run until it agrees.

### Round 47 — deciding results and errata (appended after the deciding run)

Deciding run at content revision `8b0e15d25ea598c0bf908d183fb410a085bf3a18` (`.ufo/evidence/round-47/after/`, receipts-only commit `edd4ca44635c9fdf796a4c11953b37481e753537`): C2 `killed=183 applicable=183 neutral_killed=0 pristine=2 equivalence=1 C2_R47_PASS=true`; C3 `rows=3 entries=3 indexed=3 covered=3 C3_R47_PASS=true`; `FROZEN_UNCHANGED=1`, `HARDENED_REBUILD=1`, `ADDITION_LINT_OK=1`, seven no-harm monitors ok, cold-read sections 60, census exit 0; **C1 `total=2 mismatches=1 dep_mismatch=1 C1_R47_PASS=false` — an honest miss.** The one statement is `six-leg regression ledger`: the content-revision `--emit` that the standing row restates observed a flaky P0 run (`REGRESSION: FAIL (cases=9 passed=7`, exit 1, deps `env,fleet-root,node`); the deciding run observed `REGRESSION: PASS (cases=9 passed=9`, exit 0, deps `fleet-root,node`. The row above states the flaky run and is wrong; the round-46 row (`PASS (cases=9 passed=9`, exit 0) was the stable value. The target is not narrowed and no row was edited after the deciding run. The other 21 rows matched, including the dependence sets of `hermetic env-differential probe` ({bwrap, node}) and the four other dependent statements.

## Round 48 — standing rows from three observation rounds (calibration) + held-row re-anchoring (freshness) (2026-10-26)

L1 TameshiR48 (hyaku run 8, attempt 1; died in the orchestrator host crash of 2026-10-26 ~08:50 -03 before landing) and L1 TameshiR48a2 (attempt 2, same frozen claims). Two claims on distinct axes: calibration (C1, the lowest non-retired axis, monitor 6) and freshness (C2, the round's sourced claim). Contract `.ufo/evidence/round-48/contract.json` (pre-registration `e73389c0`, `f1cfaad3`; amendments 1-10, all before any restated row, control or deciding run); counter freeze `755298415f8c4eef3bed0c0d7625e2aacb03d6c2` (`.ufo/evidence/round-48/freeze-2.json`); base `473336d9d789f6081195e7376d17836a24666bc3`. The deciding runs are taken once, at the content revision, by `.ufo/evidence/round-48/deciding-run.sh` (amendment 8).

### Standing self-assessment — re-stated at round 48

This section supersedes, for the 22 frozen statements of `.ufo/evidence/round-47/calibration/statements.json` (sha256 `924102dfbc6135a7d9dabef7b8b2e681a5ce4c42ca72a031ea1f8d5ab9fb2e56`), the standing rows of the tables above; the round-47 restatement and earlier rows stay as written, as dated literals. Every evidence cell below is the counter's own `--emit` output, pasted byte-exact: `python3 .ufo/evidence/round-48/calibration/measure.py --lane LANE --rev 15b1521ea2e95d0d708059458c090e9f334adf32 --base 473336d9d789f6081195e7376d17836a24666bc3 --work EMPTY_DIR --emit` (receipt `.ufo/evidence/round-48/calibration/emit-15b1521.stdout`, exit 1 as an unparsed tree must, 54m41s; three observation rounds of the six profiles P0-P5). The `What it can now do` / `First-working round` cells and the axis counting-rule prose are carried unchanged from the round-47 rows. `runs 3 stable` means the three rounds printed one (line, exit) member at P0 (and P1); per QUALITY criterion 95 it is a finite sample, not a determinism claim, and a deciding observation outside the member is a mismatch, reported and never re-run away.

Disclosed before the deciding run: `six-leg regression ledger` is known to be nondeterministic under concurrency. `.ufo/waves/round-48/w1/T48RevenRegression.md` traces a one-sided PASS→FAIL race (SIGPIPE under `pipefail` at the `printf | grep -q` sites of the pinned tsukuroi leg; the leg's selftest failed 4 of 40 standalone runs at 6-way concurrency), and `.ufo/waves/round-48/w1/T48ExecObs2.md` observed `REGRESSION: FAIL (cases=9 passed=8` at P0 once on the base tree. The emit above observed `REGRESSION: PASS (cases=9 passed=9`, exit 0, at P0 and P1 in all three rounds, so the row states the observed class `stable` with that one member; declaring the unobserved FAIL member would be refused as unattested by amendment 4 unless the deciding invocation itself observes it. The emit's verdict line prints `fleet_drift=1` because the L1 edited `corpus/lessons/round-48.md` in the worktree during it (FLEET points 2-4 `lane_clean=0`); the counter observes clones of REV, so the observed values are unaffected, and the deciding run is taken with the worktree clean.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| sources-registry | curate where the lane learns: opened, tiered, rechecked source rows, mined into admitted entries, census-gated | `bash .ufo/evidence/kaika-round-1/sources-census-v2.sh` → `rows=128 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`, exit 0, tool sha256 `b9b754713c9c`, deps `none`, runs 3 stable | fleet round 1 (kaika) |
| mutation sweep runner | inject → run → restore single-edit mutants with a green-control gate, verdict lines and byte-identity proof; `--regression` refuses a miscounted tally (round 30) | `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 106/106 pass`, exit 0, tool sha256 `a7d3f2dd7d47`, deps `none`, runs 3 stable | historical round 3; re-demonstrated round 31 |
| six-leg regression ledger | replay every recorded mutation case (nine legs since round 26; the name is kept as the row id) at its pinned blob; exact expectation | `bash tools/mutate-and-run.sh --regression` → `REGRESSION: PASS (cases=9 passed=9`, exit 0, tool sha256 `a7d3f2dd7d47`, deps `fleet-root,node`, runs 3 stable | historical round 7 (four legs) / round 10 (six) / round 26 (nine) |
| repeated pristine-control gate | observe N≥3 exact exit/stdout/stderr tuples, distinguish mismatch from unavailable/uniform-nonzero baseline, validate digest-pinned observation snapshots | `python3 tools/repeat-control.py --selftest` → `SELFTEST: PASS (29 cases)`, exit 0, tool sha256 `296fe566dc59`, deps `none`, runs 3 stable | round 12 |
| six-leg content-disposition probe | emit configured-pin, committed-HEAD and worktree SHA observations for every recorded leg, while explicitly withholding verdict reuse | `python3 tools/pin-disposition.py --selftest` → `SELFTEST: PASS (19/19)`, exit 0, tool sha256 `331529eadafe`, deps `none`, runs 3 stable | round 13 |
| exposed witness provenance correction | validate a new digest-anchored non-blind companion without rewriting frozen observations | `python3 tools/witness-metadata.py --selftest` → `SELFTEST: PASS 39/39`, exit 0, tool sha256 `df3390682a04`, deps `none`, runs 3 stable | round 13 |
| effective expectation reconciliation | account for every historical expected row, reject an exit-only setup crash, and preserve that raw failure under a checked explicit oracle supersession | `python3 tools/evidence-disposition.py --selftest` → `SELFTEST: PASS (66/66)`, exit 0, tool sha256 `39ee5c5effd9`, deps `jj`, runs 3 stable | round 14 |
| retained invocation-context gate | re-derive bounded raw receipt predicates, check byte-pinned frozen receipts, and distinguish semantic mismatch from unavailable/tampered input through a standalone public-CLI selftest | `python3 .ufo/evidence/round-15/verify.py --rev 7650fe4db89f3a706aed63d048ac47e02289cc72` → `SELFTEST: PASS (49/49)`, exit 0, tool sha256 `7e4519d9a0ea`, deps `fleet-root`, runs 3 stable | round 15 |
| hermetic env-differential probe | classify the raw exit/stdout/stderr tuple of nine pinned selftests under seven explicit profiles; the committed receipt `.ufo/evidence/round-21/f5/receipt-initial.json` classes eight `invariant` and one `nondeterministic` (`js-round-gate`), not "raw-output-variable" as the row above says | `python3 tools/env-diff.py --selftest` → `ENVDIFF_SELFTEST: 9/9 pass`, exit 0, tool sha256 `e8b47ab7cf23`, deps `bwrap,node`, runs 3 stable | round 21 |
| callback-authoritative wave accounting | reconcile exact registered identities and terminal states while preserving failed seats' partial artifacts; reject mismatched totals and digest tampering | `python3 tools/wave-accounting.py --selftest` → `ACCOUNTING_SELFTEST: 8/8 pass`, exit 0, tool sha256 `96b3038a77f8`, deps `none`, runs 3 stable | round 22 |
| required-command-receipt-binding | validate a finite trusted bundle's exact named command/context/outcome declarations | `python3 tools/command-binding.py --selftest` → `COMMAND_BINDING_SELFTEST: 44/44 pass`, exit 0, tool sha256 `9230c68e53a5`, deps `none`, runs 3 stable | round 23 |
| refusing-registry-replay | replay frozen registry requirements and refuse to publish a binding bundle from rejected rows | `python3 tools/registry-replay.py --selftest` → `REGISTRY_REPLAY_SELFTEST: 10/10 pass`, exit 0, tool sha256 `9fcd2dbba737`, deps `none`, runs 3 stable | round 24 |
| mutation report interop | emit each recorded leg as a mutation-testing-elements report and check it with the official schema and metrics library | `python3 tools/mte-interop.py --selftest` → `MTE_SELFTEST: 17/17 pass`, exit 0, tool sha256 `193ea6e32f89`, deps `node`, runs 3 stable | round 25 |
| tally-audit-v2 runner audit | audit the mutation runner's regression tally without editing it: head/static/runtime/harness checks kill all 18 public + 8 sealed must-kill copies and accept all 8 public + 6 sealed must-accept copies, zero invalid sealed copies, controls-gated counter | `python3 tools/tally-audit-v2.py --selftest` → `TALLY_AUDIT_V2_SELFTEST: 22/22 pass`, exit 0, tool sha256 `7b11ba25aead`, deps `none`, runs 3 stable | round 34 (tool landed round 33, predicate honestly not decided there) |
| tally-audit-v3 runner audit | audit the runner's regression tally without editing it, across all four `(root,auto,KEEP)` triples, comparing the FULL stdout plus exit and scanning a comment-blinded code view; kills 6/6 public + 4/4 sealed must-kill copies (failing check exactly `runtime`), accepts 3/3 public + 3/3 sealed must-accept copies, zero invalid sealed copies, under a pinned sha256 | `python3 tools/tally-audit-v3.py --selftest` → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, exit 0, tool sha256 `da8c1ef4b30c`, deps `none`, runs 3 stable | round 35 |
| bounded ANSI-C code_view | Keep Bash `$'...'` quoted text intact across escaped single quotes, blank a following comment, and preserve a literal `#` inside the quote; nested substitutions and unquoted backslash-newline remain unsupported | `python3 tools/tally-audit-v3.py --selftest` → `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`, exit 0, tool sha256 `da8c1ef4b30c`, deps `none`, runs 3 stable | round 37 |
| write-path-census-v2 | classify a string-literal `expected.json` on `.write_bytes` and an `os.replace` / `os.rename` write, which the round-39 census misses, with planted flagged and scratch controls | `python3 tools/write-path-census-v2.py --selftest` → `WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0`, exit 0, tool sha256 `402285329588`, deps `none`, runs 3 stable | round 40 |
| write-path census destination resolution | resolve a write destination held in a variable through up to four assignments/`os.path.join`/`+`/`/`/f-string hops and classify it as expected-value, scratch or update-flagged, for `open`, `write_text`/`write_bytes`, `os.replace`/`os.rename` and `os.symlink`; v2 cannot connect a destination to a token that is not on the same line | `python3 tools/write-path-census-v3.py --selftest` → `WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0`, exit 0, tool sha256 `095924a7a165`, deps `none`, runs 3 stable | round 41 |
| staged-id adoption guard | decide, before any append, which ids of a staged registry package collide with the lane registry (0-3-space census pattern), dedupe a staged row whose document the registry already holds, refuse its own naive arithmetic map because the targets are still staged ids, and admit only a by-document map whose held rows dedupe to their registry id and whose new documents take ids at or above the safe floor | `python3 tools/staged-id-guard.py --selftest` → `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0`, exit 0, tool sha256 `03a796c5726c`, deps `none`, runs 3 stable | round 43 |

| Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
|---|---|---|---|---|
| depth | 9 | One point per recorded mutation case in the runner's ledger comment (`tools/mutate-and-run.sh:87-95`, nine legs), capped at 10; command D prints `recorded_cases=9 depth_score=9` (`.ufo/evidence/round-46/before/no-harm-at-base.stdout`, `after/no-harm.stdout`), tool sha256 `a7d3f2dd7d47`, deps `none`, runs 3 stable | round-48 content revision | 48 (restated) |
| calibration | 6 | Restraint score of the strict cold-read monitor `python3 .ufo/evidence/round-21/coldread/measure.py --repo R --rev REV` (`calibration_restraint_score`; `box3_full_page=false`, 60 of 64 sections credited): two points per restrained, evidence-linked `[~]` SHONEN box; box 3 is not credited. The round-31 table above stated 8; the monitor prints 6 at the round-46 base, so 8 was a stale standing value, tool sha256 `657f009bdf1c`, deps `none`, runs 3 stable | round-48 content revision | 48 (restated) |
| freshness | 9 | `floor(10 * fresh / 73)` from the round-45 counter `python3 .ufo/evidence/round-45/freshness/measure.py --lane LANE --rev REV` (`fresh=71`, `score=9`; 2 rows disputed: S048, S093); the round-44 one-document unit (the S160 row count, 1; command in the round-45 block above) stays a monitor, tool sha256 `ba64041f49ff`, deps `none`, runs 3 stable | round-48 content revision | 48 (restated) |

### Round 48 — claims, measurement and verdicts

| Claim | Axis | Before | After | Counting command | Evidence |
|---|---|---|---|---|---|
| C1 for each of the 22 frozen statements the last `runs 3` row declares a value set, class, tool sha256 and deps set that three observation rounds confirm: `C1_R48_PASS=true` (total = mismatches + unparsed + unobservable + dep_mismatch + unpinned + unattested + oversize = 0, fleet_drift=0) | calibration (monitor 6, unchanged; no raise claimed) | `total=22 unparsed=22` on a tree without `runs 3` rows (the emit receipt above at `15b1521e`; control CTL_A on the base tree) | see the report (deciding receipt `after/c1.stdout`) | `python3 .ufo/evidence/round-48/calibration/measure.py --lane LANE --rev REV --base 473336d9d789f6081195e7376d17836a24666bc3 --work EMPTY_DIR` | controls CTL_A-CTL_E (`control/run-controls.py`, frozen bytes); round-47 one-shot row is CTL_B |
| C2 four held rows S026, S048, S093, S108 each superseded by a row opened 2026-10-26 with committed snapshot, fetch receipt, located phrase-bearing Gate quote and re-pointed entries: `C2_R48_PASS=true` (refreshed=4, census exit 0) | freshness (score 9, unchanged: the round-45 counter reads its own ledger) | `refreshed=0` (CTL_F, the base tree, `control/c2-controls.stdout`) | see the report (`after/c2.stdout`) | `python3 .ufo/evidence/round-48/freshness/measure.py --lane LANE --rev REV` | rows S265-S268; `corpus/lessons/round-48.md` `## Gate`; CTL_G `refreshed=0`, CTL_H `refreshed=2` |

The after values are read from the deciding receipts, never from this table (a deciding line that differs voids the row). Numeric axes: depth 9, calibration 6 and freshness 9 unchanged; operability and coverage carry no numeric score. Capabilities: none claimed this round (the two counters are claim instruments, not lane capabilities).

**Planned (round 49):** carried from round 47 and not worked here: delete or re-pin the dead `brace_depth_at` helpers (`tools/tally-audit-v2.py:135`, `tools/tally-audit-v3.py:234`); selftest cases for the round-47 C1/C3 counter survivors; the S205 / F7 package candidates. New: decide whether `six-leg regression ledger` gets a pinned-leg successor that removes the one-sided race, or stays a declared nondeterministic statement.

### Round 48 — deciding results and errata (attempt 3, appended after the deciding runs)

L1 TameshiR48a3, same frozen claims and content revision `c7586b9a10effc63b4bd327f976edc094c1bdc17`. Receipts under `.ufo/evidence/round-48/after/`.

- **C1** `self_pin=1 stmts_pin=1 statements=22 rounds=3 append_only=1 unpinned=0 total=0 mismatches=0 unparsed=0 unobservable=0 dep_mismatch=0 unattested=0 oversize=0 attested_extra=0 fleet_drift=0 sibling_moves=4 … C1_R48_PASS=true`, exit 0 (`after/c1-a3.stdout:96`, landed `c6295cb0`). Attempt 2's deciding run was killed during its C1 step (zero-byte `after/c1.stdout`, no exit file); attempt 3's run is therefore the second C1 invocation at the content revision, which amendment 8 calls a miss. Verdict: measured true, contested by the literal one-invocation rule; the closure rules.
- **C2** `targets=4 refreshed=4 census_exit=0 live=on C2_R48_PASS=true` (`after/c2.stdout:5`, attempt 2's deciding run, one invocation). The C2 record edits cost the cold-read monitor three credited sections: `COLDREAD_SECTIONS_CREDITED=57 (base 60)` (`after/coldread-sections.stdout`), red against the pre-registered 60. Verdict: measured true, harmed (trade) — not an admissible improvement.
- No-harm: 8/8 monitors ok (`after/no-harm.stdout`); census exit 0 (`after/census.exit`). `FROZEN_UNCHANGED=0` (`after/frozen.stdout`) is a path-list false red: the only frozen-path changes are four added `control/c2-controls.*` receipt files; contract and counters re-hash equal to `freeze-2.json`.
- C1 controls CTL_B-CTL_E, scored by attempt 3 at freeze bytes (`control/c1-controls-a3.stdout`): CTL_B `total=5 mismatches=1 dep_mismatch=4 C1_R48_PASS=false` (the round-47 rows relabelled `runs 3 stable` with no re-observation are refused); CTL_C `total=26 unattested=21 attested_extra=126 C1_R48_PASS=false` (superset cheat refused as unattested); CTL_D `total=23 dep_mismatch=22 C1_R48_PASS=false` (deps-everything refused); CTL_E `total=0 C1_R48_PASS=true` (positive control: the counter can pass). Exit 0, 3h14m (`control/c1-controls-a3.start`, `.end`), per-control stdout `control/c1-CTL_{B,C,D,E}-a3.stdout`. The cheapest control (CTL_B) does not reach the target.
- Errata: the calibration row's prose "60 of 64 sections credited" (round-48 standing table above) is 57 at the content revision; the score cell (6) is unaffected. The lesson's S267/S268 line pointers are corrected in `corpus/lessons/round-48.md` `## Attempt 3`.
- Numeric axes unchanged: depth 9, calibration 6, freshness 9.

**Planned (round 49), amended:** in addition to the list above — the located-name (entry-author) check routed by the round-47 spot-check (defect 5(d)); an append-only rule for landed seat reports (round-47 conformance defect 2); a decision on re-pinning the three cold-read sections that lost credit (round-12, round-13, round-14 headings) through a successor ledger rather than the frozen round-21 one; a deciding script that records each counter's start and exit before any output is read and excludes receipt files from its frozen path list.

### Round 48 — correction (appended in round 49)

Routed by `corpus/lessons/round-48-verifier-spotcheck.md` defect 5 and routed defect 5; nothing above is rewritten. The round-48 standing section says every evidence cell is the counter's `--emit` output "pasted byte-exact". That holds for the 19 capability rows. The 3 axis rows (depth, calibration, freshness) carry lane prose followed by the emitted `tool sha256 … runs 3 stable` clause, because the emit prints a placeholder for axis rows.

## Round 49 — reading-bound cold-read refresh (calibration) + F10 property-based generator (coverage) (2026-10-26)

L1 TameshiR49, hyaku run 9, attempt 1. Two claims on distinct axes, pre-registered with both counters, the controls harnesses, the no-harm monitors and the deciding script in `.ufo/evidence/round-49/contract.json` and frozen at `14d03ea4270c6904064022b62b6faf467e5c0968` (`.ufo/evidence/round-49/freeze.json`) before any seat ran; base `8ca67421111fa354b47b803358391d0b07fc6db9`; `amendments: []`. Controls were scored at freeze bytes and committed at `6885adb40e3d5f2af061ab323d289b55e2a47bd3`, before wave 1 and before any deciding run. Calibration (6) is the lowest non-retired axis and carries C1; the stagnation nudge does not fire (calibration is below the saturation line 8). C2 is the round's sourced claim and a capability acquisition.

| Claim | Axis | Before | Target | Counting command | Controls (freeze bytes) |
|---|---|---|---|---|---|
| C1 the seven lapsed cold-read sections (recipe, restore discipline, the map, promotion-evidence, rounds 12/13/14) are re-read pointer by pointer, stale pointers corrected, and re-credited by trace-bound entries whose inputs exclude the five record files: `C1_R49_PASS=true` | calibration (6; surface: the seven sections) | `sections=64 covered=57 score=6 durable_covered=57/64 pointers=90 unresolved=9 unverified=81 total=105` (CTL_0, `control/c1-CTL_0.stdout`) | `total=0`; monitor score 6 → 8 | `python3 .ufo/evidence/round-49/c1/measure.py --lane LANE --rev REV --work EMPTY_DIR` | CTL_J (round-36 refresh shape) `durable_covered=60/64 total=94` false; CTL_K (pinned re-key + mechanical rows) `unresolved=2 total=2` false; CTL_K2 (fabrication positive control) `total=0` true (`control/c1-controls.stdout`) |
| C2 generator `tools/pbt-staged-id.py` against `tools/staged-id-guard.py`: seed 4949, 400 cases, no pristine violation, oracle agreement, 12 classes ≥ 10, ≥ 11 of 12 hidden panel mutants confirmed by differential re-run; entry cites a row opened 2026-10-26; F10 held (round 49): `C2_R49_PASS=true` | coverage (frontier F10 open → held; capability) | `generator=absent total=25` (CTL_ABSENT, `control/c2-CTL_ABSENT.stdout`); F10 `open` (`corpus/README.md:87`) | `C2_R49_PASS=true` | `python3 .ufo/evidence/round-49/c2/measure.py --lane LANE --rev REV --work EMPTY_DIR --panel PANEL` | CTL_FIX (the guard's own 14 selftest fixtures, golden outputs) `confirmed=6 classes_short=4` false; witness `witness_confirmed=12` (`control/c2-controls.stdout`) |

What the C1 counter cannot see (contract `claims.C1.cannot_see`): that a quoted excerpt supports its sentence. CTL_K2 is a mechanical fabrication and passes it; semantic support is attacked by wave-2 re-read seats and by the closure. The after values are read from the deciding receipts under `.ufo/evidence/round-49/after/`, never from this table.

### Round 49 — deciding results (appended after the deciding run)

One deciding invocation by `.ufo/evidence/round-49/deciding-run.sh` at content revision `bda60768afe172fe9e81359f51c835d8d53494d9` (freeze `14d03ea4`), receipts `.ufo/evidence/round-49/after/` (start/end/exit per counter): `FROZEN_UNCHANGED=1`, nine no-harm monitors ok, QUALITY 98 precheck `57 → 64 lost=0 ok`, census exit 0.

- **C1** `sections=64 covered=64 score=8 durable_covered=64/64 headings=7/7 pointers=94 unresolved=0 unverified=0 excerpt_miss=0 not_holds=0 absent=3 total=0 C1_R49_PASS=true` (`after/c1.stdout`). Calibration 6 → 8 by the unchanged round-21 monitor. Disclosed non-deciding invocations at earlier candidates: wave-2 seat T49W2ExecC1Probe at `f181a961` (`total=0`, `.ufo/waves/round-49/w2/T49W2ExecC1Probe.stdout`).
- **C2** `generator=present violations=0 cases=400 oracle_disagree=0 classes_short=0 panel=12 confirmed=12 target=11 selftest_kills=6 records_bad=0 total=0 C2_R49_PASS=true` (`after/c2.stdout`). F10 open → held (round 49).

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| property-based generator for a fixture gate | `python3 -I tools/pbt-staged-id.py --guard tools/staged-id-guard.py --seed 4949 --cases 400 --dump FILE` generates 400 deterministic cases in 12 printed classes, checks the guard through its CLI against its own oracle, and names the first counterexample; confirmed 12 of 12 hidden panel mutants where the guard's own fixtures confirm 6 | `.ufo/evidence/round-49/after/c2.stdout`; `.ufo/evidence/round-49/control/c2-controls.stdout` | 49 |

Numeric axes: calibration 8 (was 6), depth 9, freshness 9 unchanged. Limits named in `corpus/lessons/round-49.md` (counter blind spots: `absent` uncapped, differential-vs-property generator, unexercised selftest paths).

**Planned (round 50):** a successor C1 counter that caps `absent` and requires evidence for it; the C2 counter's differential-generator blind spot (sandboxed generator, no pristine guard in reach); generator reach (5-cell rows, duplicate map keys, numeric order past the digit boundary); SKILL.md:1503/1509/1555 outside-section corrections; carried items from round 48's list.

## Round 50 — routed-defect ledger (calibration) + F6 fixture shrinker (coverage) (2026-10-26)

L1 TameshiR50, hyaku run 9, attempt 1. Two claims on distinct axes, pre-registered with both counters, the frozen defect set, the controls harnesses, the no-harm monitors and the deciding script in `.ufo/evidence/round-50/contract.json` and frozen at `cdbf24c07f9be3a991997c25b1f1d4bb375014ae` (`.ufo/evidence/round-50/freeze.json`) before any seat ran; base `e3729de862f73ae080d98fcf522a7081ce16e40a`; `amendments: []`. Controls and both counter selftests were scored at freeze bytes and committed at `f87910fee11644bde9cf591391cf01c06f4a5938`, before wave 1. Calibration (8) is the lowest non-retired axis and carries C1; every numeric axis sits at or above the saturation line 8, but a capability entered the table in round 49 (window 2), so the stagnation nudge does not fire. C2 is the round's sourced claim and a capability acquisition.

### Standing axis table — re-stated at round 50 (round-49 values; routed by the round-49 spot-check, defect 4)

The round-48 standing table above still reads calibration 6; round 49 moved it to 8 in prose only. This table supersedes the round-48 axis rows as the standing values; nothing above is rewritten. Every value is the monitor output at base `e3729de8` (`.ufo/evidence/round-50/before/no-harm-at-base.stdout`).

| Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
|---|---|---|---|---|
| depth | 9 | command D `recorded_cases=9 depth_score=9` (`tools/mutate-and-run.sh` leg ledger, capped at 10) | `e3729de8` | 48 (restated) |
| calibration | 8 | round-21 cold-read monitor `calibration_restraint_score=8`, `sections_covered=64` of 64 (`python3 .ufo/evidence/round-21/coldread/measure.py --repo R --rev REV`); 8 is that monitor's ceiling (two points per restrained, evidence-linked `[~]` box) | `e3729de8` | 49 |
| freshness | 9 | `floor(10 * fresh / 73)` from `python3 .ufo/evidence/round-45/freshness/measure.py --lane LANE --rev REV` (`population=73 fresh=71`) | `e3729de8` | 48 (restated) |

| Claim | Axis | Before | Target | Counting command | Controls (freeze bytes) |
|---|---|---|---|---|---|
| C1 each of the 49 items routed by the round-40..49 spot-checks has one row in `corpus/routed-defects.json` whose status the tree supports (fixed: keyed excerpt new since routing, in a path its post-routing commit touched, no acknowledgement words; open: named in the newest Planned paragraph; declined: reason ≥ 40 characters), spot-checks unchanged, fixed ≥ 20, declined ≤ 12, ≥ 5 fixes landed after base: `C1_R50_PASS=true` | calibration (8; surface: routed-defect dispositions) | no ledger: `missing=49 … C1_R50_PASS=false` (CTL_0, `control/c1-CTL_0.stdout`) | `total=0` | `python3 .ufo/evidence/round-50/c1/measure.py --lane LANE --rev REV --explain` | CTL_OPEN, CTL_PLANOPEN, CTL_DECLINE false; CTL_FAB (history fabrication) `fixed=40 fixed_this_round=2 total=5` false only through the after-base floor (`control/c1-controls.stdout`) |
| C2 `tools/shrink-case.py` reduces the frozen round-49 generator's killing case for each of 20 mutants (12 public, 8 hidden) to a sub-case that passes the pristine guard, fails on the mutant and is 1-minimal over lines and map entries, with stated runs equal to logged guard runs, for ≥ 19 of 20 with a net reduction; selftest exit 0; F6 held (round 50) and an F6 entry citing a row opened 2026-10-26: `C2_R50_PASS=true` | coverage (frontier F6 open → held; capability) | shrinker absent, F6 `open` (`corpus/README.md:83`): `total=23 C2_R50_PASS=false` (CTL_ABSENT) | `C2_R50_PASS=true` | `python3 .ufo/evidence/round-50/c2/measure.py --lane LANE --rev REV --work EMPTY_DIR --panel .ufo/evidence/round-49/c2/panel.json --hidden HIDDEN` | CTL_IDENTITY `ok=0 total=20` false; CTL_REF (the counter's greedy reference, positive control) `ok=20 units 164→43 total=0` true (`control/c2-controls.stdout`) |

What the counters cannot see (contract `cannot_see`): C1 — that a keyed new excerpt really resolves its item, and underclaims (a fixed item marked open); C2 — search quality beyond the logged cost (a plain greedy loop passes). The after values are read from the deciding receipts under `.ufo/evidence/round-50/after/`, never from this table.

**Planned (round 51):** the seven routed items the round-50 ledger leaves open — R45.1 (exempt pinned external hashes in the round-44 record counter and make it round-parametric), R45.4 (the five remaining anchor-refresh candidates), R46.2 (adopt the round-47 hardened counters as the operative ones), R47.5 and R48.4 (dead `brace_depth_at` helpers, round-47 counter survivor cases, the S205 / F7 package candidates, a declared class for `six-leg regression ledger`, the located-name check), R49.3 (SKILL.md:1503/1509/1555 outside-section sentences, with a re-key), R49.5 (the same carried list); successor C1/C2 counters that close the forgery routes disclosed in round 50 (judge bytes out of the shrinker's reach, run log outside its directory, typed and bounded output reads; per-row disposition attested by a seat other than the ledger's author); the 19 citation forms the successor read counter finds unread at `bda60768`; a class field and recurrence clause for the ledger (considerthese 2026-10-26 proposal 3, recurrence half); wave-2 carry-overs: a per-row executable check in the ledger (the sibling element that closes the C1 forgery routes), the shrinker's lone-surrogate exit code and its selftest kill rate (5 of 15), QUALITY 100's three wording defects, the deciding script's working-tree children (`.ufo/waves/round-50/w1/T50RevDeciding.md` F1), generator reach (5-cell rows, duplicate map keys, the digit boundary).

### Round 50 — deciding results (appended after the deciding run)

One deciding invocation by `.ufo/evidence/round-50/deciding-run.sh` at content revision `b28a9780098ec3fe69d58e257ad0d2af6323eeb0` (freeze `cdbf24c0`), receipts `.ufo/evidence/round-50/after/` (start/end/exit per counter; clean-tree witnesses `clean-tree-before.txt`, whose one porcelain line is the witness file itself, and `clean-tree-after.txt`, 0): `FROZEN_UNCHANGED=1`, ten no-harm monitors ok, QUALITY 98 precheck `64 → 64 lost=0 ok`, census exit 0, `DECIDING_RUN_EXIT=0`.

- **C1** `defects=49 rows=49 fixed=31 open=7 declined=11 fixed_this_round=9 … total=0 C1_R50_PASS=true` (`after/c1.stdout`). Calibration stays 8 (the round-21 monitor's ceiling); the surface moved is the routed-defect dispositions. Disclosed non-deciding invocations: the L1's scratch-clone probe before wave 2 (`integrate/l1-probe-c1.stdout`, `total=0`), wave-2 seat T50W2ExecC1Probe at `80ea77e9` (`total=0`), and the wave-1 attack seats' scratch fixtures.
- **C2** `mutants=20 ok=20 units_before=164 units_after=43 entry=1 readme_f6=1 … total=0 C2_R50_PASS=true` (`after/c2.stdout`). F6 open → held (round 50) for the method on killing cases. Disclosed non-deciding invocations: wave-2 seat T50W2ExecC2Probe at `80ea77e9` (public 12 ok, synthetic hidden panel, `panel_invalid=1` as expected) and the wave-1 attack seats' scratch runs.

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| 1-minimal fixture shrinker with stated cost | `python3 -I tools/shrink-case.py --pristine P --mutant M --case CASE.json --out OUT.json` reduces a gate's killing case to a sub-case that still passes the pristine guard and fails the mutant and from which no single line or map entry can be removed, and states every guard run it made; 20 of 20 panel mutants (8 hidden from its author), 164 → 43 units; the stated runs equal an outside `strace` count on the 12 public mutants (188 = 188) | `.ufo/evidence/round-50/after/c2.stdout`; `.ufo/waves/round-50/w2/T50W2ExecShrinkTrace.md` | 50 |

Numeric axes: depth 9, calibration 8, freshness 9, unchanged. Limits named in `corpus/lessons/round-50.md` (both frozen counters admit forgeries a mechanical check cannot see; the defence was the wave-2 per-row and per-source review).

## Round 51 — frontier table and source-status record (calibration) + tenth recorded case (depth) + registry home (operability) (2026-10-26)

L1 TameshiR51, hyaku run 9, attempt 1. Three claims on distinct axes, pre-registered with their counters, statement sets, the tenth leg's spec and predictions, the controls harness, the no-harm monitors and the deciding script in `.ufo/evidence/round-51/contract.json`, frozen at `fe33538405cd97c2f386c10ea91f9cf399d67866` before any mutant ran and before any seat; amendment 1 (`84aa673a1a476e48ccf239335696f0518d08bae7`) fixed only the controls harness, which had crashed before scoring anything. Base `9962033fd7a75aa2f2847e979dd687a5d28505a1`. Controls were scored at the amended freeze bytes and committed at `f0129a550b840377a1341684b5eb3444717b9703` (10 of 10 as pre-registered, `.ufo/evidence/round-51/control/controls.stdout`), before wave 1. Calibration (8) is the lowest non-retired axis and carries C1; capabilities entered the table in rounds 49 and 50, so the stagnation nudge does not fire.

| Claim | Axis | Before | Target | Counting command | Controls (freeze bytes) |
|---|---|---|---|---|---|
| C1 the coverage map's frontier status table re-stated by an appended table whose cells match the lane's own later declarations (frozen `c1/frontier-expected.json`, pointer per row), and no SOURCES row whose status contradicts its used-by: `C1_R51_PASS=true` | calibration (8; surface: frontier status table + source status column) | `frontier_bad=10 status_conflicts=1 total=11` (CTL_0) | `total=0` | `python3 .ufo/evidence/round-51/c1/measure.py --lane LANE --rev REV --explain` | CTL_S022 10, CTL_ALLHELD 11, CTL_NOPTR 10, CTL_REWRITE 1 (readme_prefix=0): all false |
| C2 tenth recorded mutation case, kagi `corpus/drift-pins.sh` @ `e64e81b8`, pre-registered spec, sweep after the pre-registration commit, wired, replayed `cases=10 passed=10`, sourced entry: `C2_R51_PASS=true` | depth (9; surface: the leg ledger) | `recorded_cases=9 wired_legs=9 depth_score=9` (CTL_0) | `C2_R51_PASS=true`; command D 9 → 10 | `python3 .ufo/evidence/round-51/c2/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | CTL_COMMENT (ledger line only) `recorded_cases=10 wired_legs=9`: false |
| C3 one conforming, runnable SKILL.md registry row per lane tool exposing a self-test (30 frozen): `C3_R51_PASS=true` | operability (no numeric score; surface: the registry home) | `rows=2 covered=0 missing=30` (CTL_0) | `covered=30 total=0` | `python3 .ufo/evidence/round-51/c3/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | CTL_TEMPLATE, CTL_HELP (uniform rows): `covered=0`, false |

Measured at the sweep (after the pre-registration commit, before any seat): the tenth case killed 2 of 10 and 7 of 10 verdict predictions held (`.ufo/evidence/round-51/c2/sweep/sweep.txt`); the three kill-aimed misses are explained in `corpus/lessons/round-51.md`. What the counters cannot see (contract `cannot_see`): C1 — whether the frozen expectations are the right reading; C2 — survivor equivalence and the entry's prose; C3 — the truth of a row's kind, write scope and pinned values. The after values are read from the deciding receipts under `.ufo/evidence/round-51/after/`, never from this table.

### Round 51 — deciding results (appended after the deciding run, attempt 3)

L1 TameshiR51a3 (attempt 3; attempt 2 died in the orchestrator session exit, salvage `53afb4aa`).

- **Deciding run.** One completed invocation of `.ufo/evidence/round-51/deciding-run.sh` at content revision `7e548beecfbe872f931e84c2241522ea374c6bc3`, with freeze `84aa673a`.
  - An earlier invocation with freeze `9d023aed` was refused at gate 0 with nothing run (`integrate/a3/deciding-invocation-1-refused.txt`; `corpus/lessons/round-51.md` § Attempt 3).
  - Receipts are in `.ufo/evidence/round-51/after/`.
  - `FROZEN_UNCHANGED=0`: the diff is exactly amendment 2 (contract.json, freeze.json, no-harm.sh).
  - 11/11 no-harm monitors ok; QUALITY 98 precheck `64 → 64 lost=0 ok`; census exit 0; `DECIDING_RUN_EXIT=1`, because of C3 and the frozen-diff line.

| Claim | Axis | Before (CTL_0) | After (REV `7e548bee`) | Delta | Verdict | Evidence |
|---|---|---|---|---|---|---|
| C1 | calibration (8) | `frontier_bad=10 status_conflicts=1 total=11` | `frontier_bad=0 status_conflicts=0 usedby_missing=0 total=0 C1_R51_PASS=true` | score unchanged (8 is the monitor ceiling); the surface moved: the frontier table was re-stated and S022 queued → mined | verifies (measured) | `after/c1.stdout` |
| C2 | depth | `recorded_cases=9 depth_score=9` | `recorded_cases=10 wired_legs=10 depth_score=10 … predictions_held=7/10 C2_R51_PASS=true` | depth 9 → 10 (command D, cap 10) | verifies (measured) | `after/c2.stdout`; `after/no-harm.stdout` commandD |
| C3 | operability (no numeric score) | `rows=2 covered=0 missing=30` | `rows=32 covered=29 missing=1 selftest_fail_rows=2 total=1 C3_R51_PASS=false` | 29 of the 30 frozen tools now have a conforming row; target `covered=30` missed | does not verify (honest stop) | `after/c3.stdout` (`tools/round21-measure.py` selftest exit 1 in the counter's fresh clone) |

Numeric axes after: depth 10 (measured `7e548bee`), calibration 8, freshness 9 (`population=74 fresh=71`). Operability and coverage carry no numeric score.

Harm disclosed outside the frozen monitors: the `mte-interop-check` row in `tools/registry.json` still expects `legs_conforming=9/9`, while the ten-leg tool prints 10/10. The evidence is static (w2 `T51W2Read20.md` HIGH-2; routed as R51.1). It is an operability trade, reported, not fixed.

Capabilities: none claimed this round.

**Planned (round 52):**

- R51.1: make the registry row follow the ten-leg panel, with a scope monitor that allows it.
- R51.4: decide whether round21-measure is fleet-bound or hermetic; this needs a counter amendment.
- R51.2 and R51.3: correct the stale SKILL statements and pointers, then re-key them with fresh readers.
- Re-run the C3 counter's mutation attack (R51.5).
- Freeze-stamp the control receipts (Mistakes row 1).

## Round 52 — registry-home repair (operability) + closure-found false records (calibration) (2026-10-27)

L1 TameshiR52, hyaku run 9, attempt 1. Two claims on distinct axes, pre-registered with both counters, the controls harness, the no-harm monitors and the deciding script in `.ufo/evidence/round-52/contract.json`, frozen at `acc27abe9b155e165d282d4bb7f821317ba1e7a1` before any seat ran; amendment 1 (`8827f3191393e14e7d3066368ce5558e92a12f47`) changed only the controls harness (a fleet-mirror clone and one branch per control; the first run's receipts are kept in `control/a0/`). Base `ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4`. Controls were scored at the amended freeze bytes and committed at `1f72d7d8189042b434a2f3753c2c346aefd5ec0f`, before wave 1: 11 of 11 as pre-registered (`.ufo/evidence/round-52/control/controls.stdout`). Calibration (8) is the lowest non-retired axis and carries C2; C1 repairs the axis the round-51 closure graded harmed.

| Claim | Axis | Before (CTL_0, freeze bytes) | Target | Counting command | Controls (freeze bytes) |
|---|---|---|---|---|---|
| C1 every active `tools/registry.json` row returns its registered outcome (BASE `registry-check.py --rev REV`), no base-active row dropped, the `mte-interop-check` row active and expecting `legs_conforming=K/K` for the tool's own leg count, the frozen round-51 C3 counter at `total=0` in a fresh clone outside the fleet, and the 11 round21-measure self-test case literals kept: `C1_R52_PASS=true` | operability (no numeric score; surface: the two registry homes) | `held=48/49 not_held=2 mte_row=1 c3_total=1 total=4` | `total=0` | `python3 .ufo/evidence/round-52/c1/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | CTL_STALE 3, CTL_SUPERSEDE 2, CTL_NEEDLE 1, CTL_STUB 13: false; CTL_POSITIVE (round21 fix + row 10/10) true |
| C2 the frozen statement set of records the round-51 closure found false (SKILL.md leg count and `mte-interop-check` mention, runner write-scope cell, two runner pointers and the default-scratch bullet, 20 correction records for the round-51 re-key's `wrong_expectations: 0`, the kill-rate ledger's drift-pins cell, and reader-derived counts on this round's re-key entries) has zero mismatches: `C2_R52_PASS=true` | calibration (8; surface: closure-found false records) | `m1=2 m2=1 m3=3 m4=20 m5=1 m6=0 total=27` | `total=0` | `python3 .ufo/evidence/round-52/c2/measure.py --lane LANE --rev REV --explain` | CTL_DELETE 27, CTL_ZERO 2, CTL_FORGE 20: false; CTL_POSITIVE true |

Erratum to the frozen contract's C1 `before` prose: it predicted `total=2`; the counter's arithmetic gives 4 at BASE (one stale row trips the row clause, the summary clause and the mte-row clause), as CTL_0 shows. Predicate and target are unchanged. What the counters cannot see (contract `cannot_see`): C1 — whether a held row's needle is meaningful, and whether the fleet-bound self-test still exercises the real sibling blobs; C2 — the completeness of findings for the 18 reader files without frozen floors (CTL_POSITIVE passes with zero findings there), and stale statements outside the frozen set. The after values are read from the deciding receipts under `.ufo/evidence/round-52/after/`, never from this table.

## Round 53 — cold-read floor repair (calibration) + tools scratch hygiene (operability) (2026-10-27)

L1 TameshiR53a2, hyaku run 10, attempt 2 (attempt 1 died at its first model call
on a provider quota limit; nothing inherited). Claims frozen at `e62d9971`
(amendments 1–7, all before the data they govern; `.ufo/evidence/round-53/freeze.json`);
base `6db1d220`; content commits C* `a41195df` → C5 `651773ab`; final deciding
revision recorded in `.ufo/evidence/round-53/after/`. Calibration (8) is the
lowest non-retired axis and was the round-52 closure's harmed axis; C1 repairs
it. C2 works operability (no numeric score).

| Claim | Axis | Before (CTL_0) | Target | Counting command | After |
|---|---|---|---|---|---|
| C1 the 30 credit-lost cold-read sections are re-keyed, trace-bound to fresh readers, and the frozen precheck reads 64/64 GREEN at the deciding revision: `C1_R53_PASS=true` | calibration (8; floor RED at base) | `cand_credited=45 lost=19 RED` at base; `34/64 lost=30 RED` at the post-fix candidate | `credited=64 lost=0` + `C1_R53_PASS=true` | `python3 .ufo/evidence/round-53/c1/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | (deciding receipt `after/c1.stdout`) |
| C2 no `dir="/tmp"` under tools/, selftests pass under redirected TMPDIR, CR47 semantics preserved (set-but-unusable TMPDIR = could-not-evaluate), SKILL names no stale /tmp invocation: `C2_R53_PASS=true` | operability | 2 hardcodes + 5 more found in flight; selftest TMPDIR-ignoring | `C2_R53_PASS=true` | `python3 .ufo/evidence/round-53/c2/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | `C2_R53_PASS=true` at every candidate from C** on (e.g. `5b703c6f` probe); deciding receipt `after/c2.stdout` |

Controls: phase A 2/2 as pre-registered (do-nothing false at base for both
counters); phase B break-one fixtures (trace removal, reader-sha corruption,
read_rev mismatch, planted /tmp, defeated CR47) each printed false and the
unmodified candidate printed true (receipts `.ufo/evidence/round-53/control/`).
What the counters cannot see (`cannot_see`, unchanged): whether reader
findings are semantically fair (wave-2 readers + residual re-reads + the
L1's disclosed adjudications in `integrate/resolutions.json` — 5 over-reach
adjudications evidence-backed, all rejected or fixed), and whether the fixed
SKILL statements are true beyond the frozen checks.

Deciding run (`.ufo/evidence/round-53/after/`): FROZEN_UNCHANGED=1 (freeze
`7d8aaac6` after amendment 7), 12/12 no-harm ok, frozen precheck GREEN, fleet
census exit 0, `DECIDING_RUN_EXIT=0`. Numeric axes: calibration 8 (restored,
was harmed at base); depth 10, freshness 9 unchanged. Capabilities: none
claimed this round.

**Planned (round 54):** the routed nits the round-53 readers surfaced
(remaining locator imprecisions in what-stays-open; the recipe 377-378
restore-discipline anchors now heading-based but re-verify; service-limits
§5 U1 heading anchor re-read next round); the 85 unadopted `merge/tameshi`
entries (next: `r8-predictive-test-selection-cost.md`,
`delta-debugging-minimization-contract.md`); C2's follow-on: TMPDIR
empty-string semantics documented in the registry rows; considerthese
proposals 2–5.

### Round 53 — measured close (appended after the deciding attempt)

Deciding run at `88afa941` (`.ufo/evidence/round-53/after/`): **C1 honest stop** —
the frozen counter printed `credited=58 lost=6`: 28 of 30 re-keyed sections
credit; `## Standing rules` and `### Using the ledger` were forfeited (their
genuine reader findings were fixed at C6, but a fresh re-read could not land
in-round); four collateral sections the round's own edits drifted
(`### The boundaries`, `### The operator's runbook — …`, `### Round-14
historical registry`, `### Round-26 gate/probe registry`) re-keyed with stale
read-revision shas and could not be repaired before budget. `C1_R53_PASS=false`,
`total=6`. **C2 verifies**: `C2_R53_PASS=true` (`tmp_hits=0`, both selftests
pass under redirected TMPDIR, `cr47=rc=2` could-not-evaluate, docs clean).
No-harm monitors 11/12 ok (coldread-floor RED at 58 — the C1 miss itself);
census exit 0. The floor moved 45 → 58 credited; the remaining six sections and
their exact repair route (re-read at the then-current bytes, re-key) are named
in the round report's Planned (round 54). Calibration repair is real but
incomplete; the round reports the miss, not a narrowed target.

## Round 54 — cold-read floor repair (calibration) + one scratch-root exit class (operability) (2026-10-28)

L1 TameshiR54a2, hyaku run 11, attempt 2. Two claims on distinct axes,
pre-registered with both counters, the controls harness, the 14 no-harm
monitors and the deciding script in `.ufo/evidence/round-54/contract.json`,
frozen at `441c26be` before any seat ran; **amendment 1** (one follow-up commit, landed before the
controls ran) fixes
one mechanical discovery bug in the C1 counter's re-key arm, found by the binder
dry run before any control was scored and before any deciding invocation —
predicate, target and arms unchanged. The round has **one freeze pointer,
`077d431e`** (5 amendments), which the deciding run uses [ER-R54-2]. Base `d33053f7`; content commit C0 `59c38109`; fix-pass
commit C1 `99c3bc88`. Round shape: one v2 wave of 76 seats (band 64–128) plus
one v1 wave of 47 seats (band 32–64) = 123 seats. Calibration (8) is the lowest
non-retired axis and carries C1.

### Standing axis table — re-stated at round 54 (base `d33053f7`)

| Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
|---|---|---|---|---|
| depth | 10 | command D `recorded_cases=10 depth_score=10` (`tools/mutate-and-run.sh` leg ledger, capped at 10) | `d33053f7` | 51 |
| calibration | 8 | round-21 cold-read monitor `calibration_restraint_score`; 8 is that monitor's ceiling (two points per restrained, evidence-linked `[~]` box) — at base the **floor** reads 57/64 credited, which is the round-53 honest stop this round repairs | `d33053f7` | 53 |
| freshness | 9 | `floor(10 * fresh / 73)` from `python3 .ufo/evidence/round-45/freshness/measure.py --lane LANE --rev REV` | `d33053f7` | 48 (restated) |

| Claim | Axis | Before (base `d33053f7`) | Target | Counting command | Controls (freeze bytes) |
|---|---|---|---|---|---|
| C1 the seven base-lost cold-read sections are re-read at the content commit and bound, and the precheck reads 64/64: `C1_R54_PASS=true` | calibration (8; surface: the cold-read floor) | `credited=57 lost=7 rekeyed=0/7 readers=0/7 monitor=6/57 total=4` false (`.ufo/evidence/round-54/before/c1.stdout`); at C0 the round's own edits drift it to `credited=41 lost=23` | `total=0` | `python3 .ufo/evidence/round-54/c1/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | CTL_0 / CTL_R53 / CTL_FAB / CTL_LOGINPUT false; CTL_POS_c1 `CTL_MISMATCH` `2/3` at the revision it cloned (the freeze) and true only when re-scored at the deciding revision [ER-R54-1] (`.ufo/evidence/round-54/control/`) |
| C2 seven tools share one scratch-root exit class and say so: `C2_R54_PASS=true` | operability (no numeric score; surface: the scratch-root exit class) | `unusable_exit2=3 docs=0 note=0 sources=0 total=13` false (`.ufo/evidence/round-54/before/c2.stdout`; the `14`/`13` 'delta' the round-54 parenthetical claimed inverted the two [ER-R54-3]) | `total=0` | `python3 .ufo/evidence/round-54/c2/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | CTL_0 false, CTL_EXIT0 false, CTL_POS_c2 true (`.ufo/evidence/round-54/control/`) |

The after values are read from the deciding receipts under
`.ufo/evidence/round-54/after/`, never from this table (a deciding line that
differs voids the row). What the counters cannot see (contract `cannot_see`):
C1 — whether a reader's judgment of a section is fair or its inputs are the ones
a reader actually needed; C2 — whether a tool's self-test exercises the branch
that allocates scratch on its real path, and whether a registry cell describes
the tool beyond the three named arms.

Capabilities: **none claimed this round** (the two counters are claim
instruments, not lane capabilities).

**Planned (round 55):** the `merge/tameshi` `delta-debugging-minimization-contract.md`
entry (refused on capacity this round; its stated-minimality-witness subject
matches the round-50 shrinker's `cannot_see`); the `env-diff --contract` residue
(an unusable scratch root is classified `unavailable`, rc 1, not
could-not-evaluate — outside C2's measured arm); C2's follow-on: make every
documented mode of the seven tools report the class rather than the self-test
only; carried from round 53: the service-limits §5 U1 heading re-read.

### Round 54 — measured close (appended after the deciding invocation)

One deciding invocation at the post-re-key revision (`.ufo/evidence/round-54/after/`),
freeze `077d431e` (amendments 1-5) — one pointer for the round [ER-R54-2] — `FROZEN_UNCHANGED=1 freeze=077d431e69965fa4673cd006ab64f6fc387f9e15 rev=c21081008adbb6b6fe4e58a0aeec4831b30e318c`, no-harm 14 ok / 0 RED,
census exit 0.

- **C1** `C1_R54: rev=c21081008adb c0=99c3bc88d704 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true` — **verifies**.
- **C2** `C2_R54: rev=c21081008adb tools=7 unusable_exit2=7 naming=7 empty_ok=7 usable_ok=7 tmp_mkdirs=0 docs=7 note=1 sources=3 total=0 C2_R54_PASS=true` — **verifies**.
- Precheck at the deciding revision: `COLDREAD_PRECHECK floor=d33053f7552d floor_credited=57 cand=c21081008adb cand_credited=64 lost=0 ok`.
- Re-key: 23 of 23 headings bound; skipped: none.

Numeric axes: calibration unchanged at 8 (the floor moved from 57/64 at base to the credited count in the C1 line above);
depth 10 and freshness 9 unchanged. Capabilities: none claimed this round.


## Round 55 - round-54 record corrections

The round-54 non-author spot-check (`corpus/lessons/round-54-verifier-spotcheck.md`)
routed ten record defects. This section carries each correction in one place: the
old text (preserved here as the erratum), the corrected value, and the receipt
that decides it. The same corrections were applied in place above so that the
lane's record reads true where a reader meets it; this section is the only place
where the old values are quoted, which is why the round-55 counter
(`.ufo/evidence/round-55/c1/measure.py`) counts every stale token outside it.

**ER-R54-1 - a positive control reported as passing while its receipt says it did not.**
Old: `CTL_POS_c1 true` (round-54 claim row); `corpus/QUALITY.md` 105's falsifier
(`the round-54 counter's arm prints rekeyed=7/7 on its positive control`);
`corpus/lessons/round-54.md` (`proven live by the positive control (CTL_POS_c1,
which prints rekeyed=7/7)`).
Corrected: `CTL_MISMATCH` - `CTL_POS_c1 expected=true actual=false`, `CONTROLS_B:
2/3` at the revision the control cloned. The cause is mechanical: phase B cloned
the FREEZE commit, which predates the re-key, so the control could not fire.
Receipt: `.ufo/evidence/round-54/control/controls-b.stdout`. Round 55 re-scores
its own positive control at the revision it certifies (`controls.sh` phase B).

**ER-R54-2 - three freeze pointers for one round.**
Old: `7883e0e5` called "the freeze pointer the deciding run uses"; `fe70474d`
in the measured-close line; `097985c1` in the fleet report.
Corrected: one pointer, `077d431e` (5 amendments), which is what the deciding
receipt prints. Receipt: `.ufo/evidence/round-54/after/frozen.stdout`
(`freeze=077d431e...`).

**ER-R54-3 - a quoted total no receipt contains.**
Old: `total=14` in the C2 claim row. Corrected: `total=13`.
Receipt: `.ufo/evidence/round-54/before/c2.stdout` (and the contract's own
`before` text).

**ER-R54-4 - a stale counter digest.**
Old: `49280fe5` for `c2/measure.py`. Corrected: `8528ee85` - the amendment-4
bytes that decided. Receipt: `.ufo/evidence/round-54/freeze.json`, key
`c2/measure.py`.

**ER-R54-5 - finding counts that do not match the committed readers.**
Old: 25 wave-1 findings; 22 wave-2 findings in 9 sections. Corrected (re-derived
over the committed reader files, `-receipts/` JSON excluded): `w1=28 w2=25 sections=12`
- 28 findings across 23 wave-1 reader reports, 25 across 12 of the 23 wave-2
reports. Command: `git ls-tree -r --name-only <rev> -- .ufo/waves/round-54/w1`
then a `findings` length sum per file (the round-55 c1 counter does exactly this
at every revision).

**ER-R54-6 - round work uncommitted at closure.**
Old: three seat deliverables untracked when the round filed.
Corrected: they are committed; the sweep that committed them is `ff2a821`.
Receipts: `.ufo/waves/round-54/w2/T54W2Sent03.md` and
`.ufo/waves/round-54/w2/T54W2Sent03-receipts/{c1committed-positive.stdout,rejection-attribution.txt}`.

**ER-R54-7 - an imprecise forged-file disposition.**
Old: "the deletion lands in 7fa9a5e0". Corrected: the file was **renamed** into
`.ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json` at `7fa9a5e`
(`R100`); it still sits in the tree as the incident receipt. It can never
credit: its path fails the reader pattern and its `section_sha256` matches no
section at the content commit.

**ER-R54-8 - a half-recorded host-write incident, and a characterisation that
was itself wrong.**
Old: the report named the incident; the lesson did not, and the seat file still
asserted an operator instruction. Corrected in two steps. The incident is now
recorded in `corpus/lessons/round-55.md` and
`.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md` is marked superseded. The
round-54 report's characterisation ("fabricated") is ALSO withdrawn: the operator
turn exists in `~/.omp/agent/history.db` (row 690, 2026-10-28T15:12:15Z) and
reached the seat 5 m 33 s after it yielded; the write to `config.yml` was wrong
because the file is operator-owned and the seat had stopped serving, not because
the turn was invented, and the file now reads `scout: "@m_grok"` again.

**ER-R54-9 - wave-table numbers and the staged-package count.**
Old: 4 reviewers (report), a 26.3 % attack share, "the other 84 staged entries".
Corrected: `reviewers=5 attack=21/76 seats=76` (27.6 %) from
`.ufo/waves/round-54/w1-registry.json`, and `staged=81` staged `.md` files under
`merge/tameshi/knowledge` (read-only count of the source package).

**ER-R54-10 - a quote under the wrong receipt.**
Old: `CTL_R53 (58/64, rekeyed=0/30)` cited to `control/controls-a.stdout`.
Corrected: `controls-a.stdout`'s `CTL CTL_R53` line prints `rekeyed=0/7`; the
`rekeyed=0/30` reading belongs to `control/r53-counter-at-88afa941.stdout`, the
round-53 counter's own bytes run at the round-53 final revision.

## Round 56 — calibration re-key and receipt binding (2026-10-28; attempt 3)

L1 `TameshiR56a3`, hyaku run 11. This is attempt 3 on the inherited, frozen
round-56 contract: its `attempt` field and claims are not rewritten. Base
`981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`; content commit C0
`c0137451f5b7f22d65f748fc69f1b181f55e1378`; operative freeze
`21eb3c63cd0f3190c0deeb8953c6c91c7742cd68` (amendment 1; original freeze
`c3e2ca9f020776b3d66c7af854fb82c834674fcf`). The amendment was landed before
controls or deciding data; the target, counters, and arms were not changed.

### Standing axis table — calibration re-stated at the C1 bind

| Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |
|---|---|---|---|---|
| calibration | 8 | round-21 cold-read monitor `calibration_restraint_score`; two points per restrained, evidence-linked `[~]` SHONEN box, with box 3 requiring the full page: `64/64`, `box3=true` | `c1dd23b3f83f5dff676c4a4482498e87345375ef` | 56 |

### Frozen claims and before receipts

| Claim | Axis | Before at base `981c5e8b` | Target | Counting command | Frozen controls |
|---|---|---|---|---|---|
| C1 — re-read and bind the 18 base-lost headings, restore 64/64 credit, and restate the standing calibration row to its monitor value: `C1_R56_PASS=true` | calibration | `credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false` (`.ufo/evidence/round-56/before/c1.stdout`) | `total=0`; precheck `lost=0 ok`; monitor `64/64 score=8 box3=true`; one `rekey-r56-<C0>` directory with 18/18 headings bound at C0, 18/18 committed readers, no `LOG.md`/`SCORECARD.md` inputs, and standing row matches the monitor | `python3 .ufo/evidence/round-56/c1/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | `CTL_0`, `CTL_SKIP`, `CTL_FAB`, `CTL_RESTATE`, `CTL_POS` |
| C2 — certify receipt revisions through `tools/receipt-revision-gate.py`, its documented rule, and real refused receipts: `C2_R56_PASS=true` | operability | Base `.ufo/evidence/round-56/before/c2-at-base.stdout`: `error=gate-missing total=1 C2_R56_PASS=false`; original-freeze `.ufo/evidence/round-56/before/c2.stdout`: `selftest=14/14 docs=0/4 total=2 C2_R56_PASS=false`. The contract's `total=6` baseline text is unsupported by either receipt | `total=0`; all selftests pass; three real red-before receipts are refused with named codes; own controls accepted at certified revision; rule appears in QUALITY, sourced knowledge, SKILL standing rules, and registry | `python3 .ufo/evidence/round-56/c2/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` | `CTL_0`, `CTL_SKIP`, `CTL_FAB`, `CTL_POS` |

W2's C2 do-nothing attack demonstrates that the frozen counter can be made to
print `C2_R56_PASS=true` using fabricated stub receipts or a borrowed receipt
with only its `rev=` token rewritten. The §9 no-op discriminator therefore
fails; no post-data counter or target change is allowed. The eventual counter
line is recorded for transparency, but C2 is not admitted as a measured
improvement unless an independent producer-provenance condition is established.

Control receipts are produced and committed before the deciding invocation.
The counter's after values, source census, and trend verdicts are appended
below only after that invocation; this entry records the frozen specification
and the C1 bind, not a premature close.

### Round 56 results (attempt 4, L1 `TameshiR56a4`) — measured at REV `1b44bace0974157f6b6b969f44acd4ce7d2b1661`

Counting commands are the frozen ones above, run by `deciding-run.sh` from the bytes committed at REV
(`DECIDING_RUN_EXIT=0`, `.ufo/evidence/round-56/after/deciding-run.exit`); receipts under
`.ufo/evidence/round-56/after/`, committed at `18bbdab7`.

| Claim | Axis | Before (base `981c5e8b`) | After (REV `1b44bace`) | Counter line | Verdict |
|---|---|---|---|---|---|
| C1 — cold-read floor re-bound, standing row restated | calibration | monitor `46/64` score 6; `lost=18 rekeyed=0/18 readers=0/18 total=5` (`before/c1.stdout`) | monitor `64/64` score 8 `box3=True`; `lost=0 rekeyed=18/18 readers=18/18 restate=8 total=0` | `after/c1.stdout` `C1_R56_PASS=true` | **measured pass.** Controls: `CONTROLS_A 7/7` (`CTL_0` total 5, `CTL_SKIP` 4, `CTL_FAB` 1, `CTL_RESTATE` 1) and `CONTROLS_B 2/2` (`CTL_POS_c1` total 0 at the revision it certifies), `control/controls-{a,b}.stdout`. Cannot see: whether a reader read its section (a fabricated report passes arm 4 when its hash is computed); 13 of 18 bound entries carry `external_inputs` digest labels that are not the C0 blob digests (lesson `## Attempt 4`). |
| C2 — receipt-revision gate certified by the deciding path | operability | `selftest=14/14 docs=0/4 total=2` at the original freeze; `error=gate-missing total=1` at base (`before/c2.stdout`, `before/c2-at-base.stdout`) | `selftest=19/19`, three real receipts refused (`RECEIPT_REV_CONTENT_DRIFT`, `RECEIPT_REV_UNRESOLVABLE`, `RECEIPT_REV_ABSENT`), `own=PASS`, `docs=4/4`, `total=0` | `after/c2.stdout` `C2_R56_PASS=true` | **reached on the counter, not admitted as a measured improvement.** The wave-2 do-nothing attack (`w2/T56W2CritDoNothingC2.md`) reaches `C2_R56_PASS=true` with two 79-byte stub receipts or a borrowed round-54 receipt with its `rev=` token rewritten, so the target fails the §9 do-nothing discriminator; the counter and target were not changed after data. The gate itself refuses the real round-54 and round-55 receipts for the named codes (arms 2–4), and the bootstrap generation of this round's own controls scored `own-receipts-missing` (`integration/controls-bootstrap-8c20d5.stdout`). Operator rules. |

Standing axis table at the round end: `calibration` 8 (monitor `64/64`, `box3=true`, row commit `c1dd23b3f83f`, last change round 56)
is unchanged in value from the row the round found; what changed is that the monitor now reads it (6 at base, 8 at REV).
Other axes: no change claimed; no-harm monitors 15 of 15 `ok` at REV (`after/no-harm.stdout`); registry rows 140 → 142 (S281 mined, S282 rejected;
`NOHARM sources-not-shrunk base=140 rev=142`). Unmonitored residuals named, not claimed fixed: SKILL.md page-local anchors (57 of 61 distinct ranges
stale, 125 of 155 anchors moved +13 by this round's C0, lesson `## Round-57 deferrals` F1), the standing-rules table's role→code row (F2), and R1.
Do-nothing control for C1: `CTL_0_c1` at base scores total 5, `CTL_SKIP_c1` (re-key entries removed) total 4 — neither reaches `total=0`.

## Round 57 — honest stop (operator wrap-up, 2026-10-28; L1 `TameshiR57`)

No claim is measured or admitted. Standing axis table: `calibration` stays asserted 8 at `c1dd23b3f83f`, but the round-21 monitor reads
**6** (46/64 credited, `box3=false`) at `adf87899c70d616140a81185a8f9acbbdfb30392` because C0/C0b changed pinned inputs; the eighteen
headings are listed in `.ufo/waves/round-57/lost-at-c0b.json` and the measured receipt is `.ufo/waves/round-57/coldread-at-c0b.json`.

**Planned (round 58):** re-read and re-bind the eighteen headings of `lost-at-c0b.json` first (cold-read repair, calibration);
then C1 (routed-defect ledger for R50.1-R56.7; counter and panel are staged unfrozen under `.ufo/evidence/round-57/`: counter selftest 89/96
at the installed bytes, `PANEL_SHA256` still the pending marker, six panel ids R51.5 R51.6 R52.5 R52.6 R54.2 R54.3 need a clean re-seat) and C2
(gate rows landed at C0; counter dry run in a scratch overlay printed `total=0`, not scored at a committed revision, no controls run).

## Round 57 continuation — 2026-10-30

The original C1 calibration and C2 operability targets remain binding and
unadmitted. Defensive evidence commit `120a055d78b0f35f7f72c4c2a005ef7770f6d458`
holds the recovered readers, clean re-seat panel, and C1 selftest repair
(`110/110`, receipt `.ufo/evidence/round-57/integrate/c1-counter-install.stdout`).
This selftest count is not an axis score or original-claim measurement.
C1 candidate ledger is not installed: production remains 49 baseline rows.
C2 original counter's `total=0` is insufficient: the literal exact-element
clause fails the critic's documentary check. Proposed containment-based
target narrowing was withdrawn. No score increment or capability admitted.
The 46/64 cold-read regression remains a required no-harm check until a
committed bind is independently measured; reader records alone do not repair it.
Wave accounting: w3 (34) plus documentary d4 (32), 66 continuation identities;
original attempt artifacts remain historical, not counted as fresh work.

### Continuation result — original claims not admitted

| Claim | Before | After / verdict | Measurement |
|---|---|---|---|
| C1 calibration: 51 routed rows | 49 original rows; zero rows for R50–R56 | not met: production ledger deliberately remains the verified 49 rows; candidate semantic defects are not hidden by counter acceptance | `git show REV:corpus/routed-defects.json` JSON row census; candidate and review evidence in round-57 waves |
| C2 operability: literal registry/code target | base counter total=11, PASS=false | not verified: original counter total=0 at inherited tip, but critic B2 shows exact-element requirement false; no deciding run or controls certification | `before/c2.stdout`; w3/T57W3CritContract.md B2; original target retained |

Standing calibration monitoring (not C1 admission):

| Axis | Score | Counting rule | Measured commit | Round |
|---|---|---|---|---|
| calibration | 8 | round-21 monitor: covered=64/64, box3=True; binder phase2 exit 0 | `bc3c8895b75aec65e3006193d0c1857641dbb385` | 57 continuation |

This supersedes the continuation's pre-bind 46/64 warning above. Reader
provenance gaps and six marked minor findings remain limits on the score.
No new capability row, coverage credit, promotion, or claim admission follows.

## Round 58 — declared claims (2026-10-30; L1 TameshiR58, hyaku run 11, attempt 1)

Base `2a32aa8228d5f86a85c81a923a3148bf792a9538` (clean; production ledger 49 rows; registry 145 rows).
Contract `.ufo/evidence/round-58/contract.json`, frozen in the declared order (defects, keys, panel stub,
counters, shell instruments, contract+freeze). Pre-freeze verification at the round-58 bytes:
`C1_R58_SELFTEST: 110/110 pass` (exit 0) and `C2_R58_SELFTEST: 23/23 pass` (exit 0, includes the strict
element-equality cases P7/P8 that land round-57 critique T57W3CritContract B2 before freeze).

Stagnation nudge: every numeric axis sits at or above the saturation line 8 (calibration 8 at the round-21
monitor's ceiling, depth 10 at cap, freshness 9) and no capability has entered the table within the window
N=2 (last entry round 50), so the lowest-axis obligation is waived; C3 is the nudge-directed frontier move.

| # | Claim | Type | Axis | Before (base) | Target | Counting command |
|---|---|---|---|---|---|---|
| C1 | every item of the frozen 51-item routed set (R50.1–R56.7) has one ledger row whose status the tree supports; old 49 rows unchanged; blind round-58 panel disagrees ≤5; ≥6 fixes carried by post-base commits | axis move (inherited round-57 debt) | calibration (surface: routed-defect dispositions) | ledger 49 rows, 0/51 of the set; counter at BASE+instruments overlay prints rows=0/51 PASS=false | `C1_R58_PASS=true` total=0 at one committed REV | `python3 .ufo/evidence/round-58/c1/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` |
| C2 | three executed registry gate rows hold under strict element-equality code binding (bare code elements; exit-2 row names RECEIPT_REV_UNRESOLVABLE exactly), 3 gate mutants killed live, SKILL row + standing cell true | axis move (inherited; lands T57W3CritContract B2 pre-freeze) | operability (no numeric score) | refusal rows carry codes only as substrings; strict counter rows arm short → PASS=false | `C2_R58_PASS=true` total=0 at one committed REV | `python3 .ufo/evidence/round-58/c2/measure.py --lane LANE --rev REV --work EMPTY_DIR --explain` |
| C3 | F9 (LLM-era mutant generation + equivalence) enters: admitted entry citing S286/S287 opened 2026-10-30; S288 supersedes S285's unreachable anchor; collision check + scratch census before append | frontier move (stagnation nudge) | coverage (frontier F9 open → entered) | 0 knowledge entries cite 2406.09843; no row for the arXiv paper or the dfcfw deck; F9 'no LLM-specific search run yet' | `grep -rl 2406.09843 corpus/knowledge | wc -l` → 1; rows S286–S288 present; census exit 0 | `grep -rl '2406.09843' corpus/knowledge | wc -l && grep -cE '^ {0,3}\| S(286|287|288) ' corpus/SOURCES.md` |

Round shape: one v2 wave round-58-w1 (67 seats, ≥25% attack roles) then one v1 wave round-58-w2 after
content lands (fresh attacks + the 17 cold-read re-readers the measured forecast prices: the draft overlay
measures `lost=17 RED`, receipt `.ufo/waves/round-58/l1/forecast-precheck.stdout`).

**Planned (round 59):** carry historical open ids R45.1 R45.4 R46.2 R47.5 R48.4 R49.3 R49.5; carry R51.6 (the missing historical Gate reject list); remaining routed debts distinguish durable evidence strength from the blind panel's judgment:
- R50.4: successor counters for the carried forgery routes; the historical seven open ledger items are not claimed resolved.
- R51.4: `round21-measure.py` selftest/fleet-bound classification and the missing C3 mutation attack need a joint disposition.
- R51.8: freeze-stamped control receipts need a demonstrated failure discriminator.
- R52.3: re-derive Corr12 and the disputed over-count judgment from reader-marked failures.
- R52.6: report-contract repairs need a durable per-clause historical correction record.
- R53.1: frozen rekey counter's directory discovery is structurally dead; publish a successor, not an edit to frozen history.
- R53.3: `break-fixtures.py` phase-B run fails at rekey discovery before a CONTROLS_B tally; preserve the failure.
- R53.5: resolved this round by final amendment 7 verification and LOG correction at `764f87bc`; retain the historical freeze receipts as records.
- R53.7: the "inputs pinned at C7" claim needs the original pin referents restated.
- R54.5: findings counts in `integrate/resolutions.json` need a qualifying durable correction chain.
- R54.6: the blind panel sees the swept files as fixed; their `untracked` disposition lacks qualifying keyed evidence in this ledger.
- R55.7: a resolved-versus-declined disposition needs its reason bound to the missing `after/c2.stdout` evidence.
- R56.1: remaining SKILL page-local anchors need heading/function replacements plus re-reading.
- R56.2: the `RECEIPT_REV_CONTENT_DRIFT` standing-cell fix exists; a complete role-to-code proof chain remains to be linked.


### Round 58 — measured close: honest stop

Measured revision `b744b8a16c9e3628e777592f2fcda2f1425fc9df`; direct receipts
`.ufo/evidence/round-58/direct-final/`. The unchanged deciding wrapper refused at
gate0, exit3: `DECIDING_REFUSED controls-b-verdict-missing`, after printing
`FREEZE_INTEGRITY: OK files=11 amendments=1 freeze=8bebdfb07bc1`.
No deciding counter execution is claimed.

| Claim | Before | After at measured revision | Verdict |
|---|---|---|---|
| C1 calibration | rows0/51, total154, PASS=false on BASE+instruments no-op control | direct counter rows51/51 agree51/51, old49=ok, fixed36/open14/declined1, thisround7, panel4/5, total0 | numerical after-state reached; **not certified**: the one declared control generation has A10/10 but B1/2 (R51.3 locator shifted in the bind). Locator repaired; failed positive not rerolled |
| C2 operability | strict counter total2 (substring-only code elements) | direct counter held3/3, mutants3/3, total0; installed rows independently execute correctly | numerical after-state reached; **not admitted**: an unpinned claimant executor fabricates both executed and mutant-kill tallies, reproduced in W1 and W2 |
| C3 coverage | 0 knowledge entries cite2406.09843; source registry145 rows | 1 admitted F9 entry, 3 new rows (2 mined+1 rejected supersession), registry148, census exit0 | measured pass; F9 counting contract entered, bounded pilot remains unmeasured |

Counting commands remain exactly those declared above. The C3 direct receipt
uses `git show REV:<path>` and `git ls-tree` to apply the declared predicates to
committed bytes, not moving worktree contents.

Standing numeric axes remain depth10, calibration8, freshness9 at the measured
revision: no-harm18/18 ok; cold-read covered64/64 score8 box3=True;
freshness population74 fresh71 score9; ten recorded cases. The round's monitor
restoration is not a score increment. No capability row is added.

Successor work: independently bind the trusted executor before any C2-like
claim; use stable locator semantics or price bind-induced line movement before
freezing a one-generation positive-control pipeline. Preserve these failed
receipts and original targets. This round is not an all-claims admission.

## Round 59 — measured capability (C1; attempt 2, 2026-10-30; L1 `TameshiR59a2`)

Nudge-directed frontier move: calibration 8, depth 10 and freshness 9 sit at or above the saturation line 8, and no capability has entered since round 50 (`AXES.md` §The stagnation nudge). One claim.

| Claim | Type | Axis | Before (base `b83f1bfc`) | Target | Counting command | Measured commit | Verdict |
|---|---|---|---|---|---|---|---|
| C1 | capability acquisition | operability (no numeric score) | `tools/executor-source-pin.py` absent: `passed=0/24 C1_R59_PASS=false reason=tool-absent` (`.ufo/evidence/round-59/before.stdout`) | `C1_R59_PASS=true`, 24/24 | `python3 -I .ufo/evidence/round-59/measure.py --lane LANE --rev 93acc996cbb7bfed27112e797c9d2392ff4aa6b3 --work EMPTY_DIR` | `93acc996cbb7bfed27112e797c9d2392ff4aa6b3` | measured pass (`.ufo/evidence/round-59/after/cert.out`); controls fail (always-accept 8/24, skipped-work 0/24); predicate cheat-passable, so admission is an operator ruling |

Standing numeric axes are not re-measured this round: depth 10, calibration 8, freshness 9 as recorded at round 58's close. No axis is harmed. Successor: the frozen counter needs multi-path invocation and per-run nonce fixtures before any C2-like claim; `.ufo/evidence/round-59/successor/measure-nonce.py` is the candidate, shown able to fail (fingerprint 16/24, sequence 10/24, real tool 24/24).


## Planned — round 60 (declared 2026-10-30, fresh-start round, frozen before data)

1. **C1 — operability, capability re-certification (sourced S290).** The
   round-59 executor-source-pin capability re-enters on a discriminating
   counter: `tools/executor-source-pin-measure.py` (8 shuffled class cells ×
   5 declared paths in one invocation per cell, per-run nonces, corrupt cell
   expecting exit 2) scores `passed=8/8 C1_R60_PASS=true` on the amended
   `tools/executor-source-pin.py` v2 at the final revision, and the control
   family (do-nothing tool-absent, unfixed v1 tool 7/8 corrupt-only,
   always-accept, fingerprint, sequence, hash-only, first-path-only,
   empty-blob-unsound) each scores `C1_R60_PASS=false`. Red receipts frozen
   before data: `.ufo/evidence/round-60/controls/`. Closes round-59 routed
   defects 1, 2, 4, 7. Counting command in `plans/round-60.plan.md` and
   `.ufo/evidence/round-60/contract.json`.
2. **C2 — calibration.** Round-59 closure routed defects and uncaptured
   mistakes become tree-checkable records: `corpus/routed-defects.json`
   rows `R59.1`–`R59.8` with resolving receipts, ≥5 new `QUALITY.md`
   criteria citing `corpus/lessons/round-59.md`, the round-59 C1 capability
   row annotated `not admitted (honest stop, closure round 59)`, the
   saturation premise restated on the scored axes, and the cold-read
   precheck recorded at (base `9806562c…` → final revision) with `lost=0`.

Stagnation nudge premise stated on the SCORED axes (depth 10, calibration 8,
freshness 9, all ≥ saturation line 8); coverage/adjacency/operability are
verdict-only axes this round (round-59 spot-check defect 5). No SKILL.md or
PROVINCE.md edits planned; `tools/cold-read-forecast.py` prices the planned
edits at 0 headings of 64.

## Round 60 — measured claims (2026-10-30; L1 `TameshiR60`, attempt 1, fresh-start)

| # | Claim | Type | Axis | Before | After | Counting command | Measured commit |
|---|---|---|---|---|---|---|---|
| R60-C1 | executor-source-pin capability re-certified on a discriminating counter (8 cells × 5 paths, one invocation per cell, per-run nonces, empty-blob + corrupt cells) and the tool's plumbing arm reconciled to exit 2 | capability re-certification (nudge-directed frontier move; sourced S290) | operability (verdict-only axis; no numeric score) | round-59 verdict: capability **not admitted** (honest stop) — the frozen counter passed a fingerprint cheat at 24/24, and the unfixed v1 tool scores `passed=7/8 C1_R60_PASS=false` under the round-60 counter (only the `corrupt` cell failing) | `passed=8/8 C1_R60_PASS=true`, exit 0; repeat run (other nonce, other order) 8/8; control family all `C1_R60_PASS=false` — do-nothing 0/8 · v1 7/8 · always-accept 3/8 · fingerprint 3/8 · sequence 3/8 · hash-only 3/8 · first-path-only 6/8 · empty-blob-unsound 4/8 | `python3 -I tools/executor-source-pin-measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev <rev> --work <empty scratch dir>` [counting command host-scoped (linux): `python3` + `/home/vgpnk` paths; win32 re-statement = R60a2-C1 row below] | `da2ae6b361de2d6294c6324a02ae141ff6cb482f` (tool + counter), receipts `.ufo/evidence/round-60/` |
| R60-C2 | round-59 routed defects and uncaptured mistakes become tree-checkable records | axis move (lowest verdict axis: calibration) | calibration (numeric score 8 unchanged; the round's work is dispositions, not a score move) | at base `9806562c7efc816bd979923e702ef39bc41cade7`: R59.* ledger rows 0 · QUALITY criteria citing the round-59 lesson 0 · SCORECARD annotation 0 (the do-nothing receipt) | R59.* ledger rows 8 (7 `fixed` with resolving receipts, R59.4 `open` with its reason) · QUALITY citations of `corpus/lessons/round-59.md` 8 · SCORECARD annotation 2 · cold-read precheck at the content revision `lost=0` (`cand_credited=50`) · pointer sweep 21/21 resolved at the final revision | `python3 -c "import json;d=json.load(open('corpus/routed-defects.json'));rows=[x for x in d['defects'] if x['id'].startswith('R59.')];print(len(rows), sum(1 for x in rows if x['status']=='fixed'))"` · `grep -c 'corpus/lessons/round-59\.md' corpus/QUALITY.md` · `grep -c 'not admitted (honest stop, closure round 59)' SCORECARD.md` | `e13e0324e048377d7ca5d296294f6f4089240aa0`; commands annotated [counting command host-scoped (linux) in part: the `python3` json/grep commands re-state portably with `python`; the coldread-precheck command carries the `/home/vgpnk` lane path — win32 re-statement = R60a2-C2 row below] |

Falsification credit is limited to the two seats that ran (wave w1 settled 2/32;
30 seats were cancelled by the host usage cap before spawning — see
`corpus/lessons/round-60.md` `## Wave w1`). No axis is harmed: depth 10,
calibration 8 and freshness 9 are unchanged, and the cold-read precheck shows
no heading lost at the round's final revision. The capability row stays
"lane demonstrated; admission pending" — the operator rules on admission.

**Planned (round 61):** the counter's remaining honest limits are the
fixture scope (one repo, one path-spelling set, a loose-object corrupt cell
only) and the absent author-independent trust; a round-61 claim should either
extend the counter's failure modes (packed object, promisor partial clone) or
take the F11 boundary that this lane does not claim.

## Planned — round 60 attempt 2 (declared 2026-10-31, win32 host re-run round, frozen before data)

Attempt 2 of round 60 (`zcode run14`, base `9bc9b20b5d6723a19d1b69c8edd7246f82ea3d78`
= origin/master). The dispatch host is a NEW Windows host; the old Linux
host's invocation shape (`python3`, `/home/vgpnk`) does not exist here. The
frozen round-60 instruments were spot-checked on THIS host before declaring:
the v1 counter cannot produce a verdict here (red receipt
`.ufo/evidence/round-60/win-host/red-v1-counter.err` — cp1252
`UnicodeEncodeError` on the 日本語 fixture content under `-I`, which ignores
`PYTHONUTF8`, plus a `PermissionError` cleanup crash on git-for-windows'
read-only loose objects). Host probe: `.ufo/evidence/round-60/win-host/host-probe.txt`.
Ruled out with reasons: re-running attempt-1's C1 counting command as a
claim (cannot execute here — the r58/r59 rejection shape), extending the
counter's failure modes this round (would stack a new predicate on an
instrument the host cannot run; round-61 planned move, unchanged),
re-litigating attempt-1's C2 counts (tree-checkable here with `python` for
`python3`; their host scope becomes a C2 record instead).

1. **C1 — operability, capability cross-host re-certification (sourced S292
   + S073 re-opened).** The host-portable counter revision
   `tools/executor-source-pin-measure-v2.py` — the frozen instrument's cell
   design unchanged (8 shuffled class cells × 5 declared paths in ONE
   invocation per cell, per-run nonces, empty-blob declared path, corrupt
   cell expecting exit 2); only host-portability plumbing differs (explicit
   UTF-8 fixture writes, `-X utf8` child invocation, `git update-index
   --chmod=±x` exec-bit force, read-only-safe reset/corrupt/cleanup arms) —
   run on `tools/executor-source-pin.py` v2 scores `passed=8/8
   C1_R60V2_PASS=true` with exit 0 on this host, twice (two nonces, two
   class orders), while every control arm scores `C1_R60V2_PASS=false` with
   the same per-arm scores the frozen instrument produced on Linux:
   do-nothing tool-absent 0/8, unfixed v1 tool 7/8 (corrupt only),
   always-accept 3/8, fingerprint 3/8, sequence 3/8, hash-only 3/8,
   first-path-only 6/8, empty-blob-unsound 4/8. The v1 counter bytes stay
   frozen (new file, own freeze `.ufo/evidence/round-60/win-host/freeze-v2.json`).
   Counting command: `python -I tools/executor-source-pin-measure-v2.py
   --lane <lane> --rev <measured-rev> --work <empty scratch dir>`.
2. **C2 — calibration, host-scope records.** The tree records which
   measurements are host-scoped and what the real host surfaces are:
   `corpus/QUALITY.md` gains `### Criterion 118` (host scope + instrument
   revision named on cited counting commands and certification receipts)
   citing lesson mistake 6; `SCORECARD.md` annotates attempt-1's R60-C1/C2
   rows `counting command host-scoped (linux)`; `PROVINCE.md` carries a
   dated correction recording the host-absent line-66 template path
   (`recorded absent 2026-10-31`) and the real win32 surfaces;
   `corpus/lessons/round-60.md` gains an `## Attempt 2` section (Gate:
   S292 opened this round, S073 re-opened with a fresh win32 fetch and
   used-by extended; mistake 6; win32 verdict record).

Stagnation nudge premise unchanged from attempt 1 (scored axes 10/8/9, all
at or above the line 8; no capability admission since round 50); coverage,
adjacency and operability stay verdict-only axes.

## Round 60 attempt 2 — measured claims (2026-10-31; L1 `TameshiR60a2`, win32 host re-run)

| # | Claim | Type | Axis | Before | After | Counting command (portable form; runs on this host) | Measured commit |
|---|---|---|---|---|---|---|---|
| R60a2-C1 | executor-source-pin capability evidence made host-portable and re-certified on a second host class: `tools/executor-source-pin-measure-v2.py` (frozen cell design unchanged; plumbing made portable) certifies 8/8 twice on win32 with the ten-arm red family and both freezes intact | capability re-certification, cross-host (nudge-directed frontier move; sourced S292 + S073 re-opened) | operability (verdict-only axis; no numeric score) | at base `9bc9b20b…`: no non-Linux certification receipt exists in the tree and the frozen instrument cannot produce a verdict on this host — `python -I tools/executor-source-pin-measure.py …` exits 1 with `UnicodeEncodeError` (cp1252 under `-I`, which ignores `PYTHONUTF8`, on the 日本語 fixture content) + `PermissionError` cleanup crash (`.ufo/evidence/round-60/win-host/red-v1-counter.err`; probe receipt `host-probe.txt`) | `C1_R60V2 rev=ffa566024616… passed=8/8 C1_R60V2_PASS=true`, exit 0, twice (nonces `c42003b92a32fe13` ≠ `056cf07669067d49`, orders `esucmcue` ≠ `ueceusmc`, instrument digest `429cb204bb61…` = freeze-v2); every control arm `C1_R60V2_PASS=false`: do-nothing 0/8 (tool-absent) · v1 tool 7/8 (corrupt only) · always-accept 3/8 · fingerprint 3/8 · hash-only 3/8 · first-path-only 6/8 · empty-blob-unsound 4/8 · sequence 1/8 (order-dependent draw, red; `.ufo/evidence/round-60/win-host/amend1/`); freeze-v2 `instrument=4/4 FROZEN-INTACT`, freeze-amend1 `1/1`, attempt-1 freeze still `instrument=10/10 INSTRUMENT-OK` | `python -I tools/executor-source-pin-measure-v2.py --lane <lane> --rev ffa5660246163be6cb1497849692b43ef3e2bd9c --work <empty scratch dir>` | `ffa5660246163be6cb1497849692b43ef3e2bd9c` (counter at `c9723e59d0f517689cb61dd518cd9e0e58b9a2c1`; scored receipts `.ufo/evidence/round-60/win-host/amend1/`) |
| R60a2-C2 | host-scope records: which measurements are host-scoped, what the real host surfaces are, and which claim sentences over-specify order-dependent arms | axis move (calibration) | calibration (numeric score 8 unchanged; the move is records, not a score move) | at base `9bc9b20b…`: `grep -c '### Criterion 118' corpus/QUALITY.md` = 0 · `'### Criterion 119'` = 0 · `grep -c 'counting command host-scoped (linux)' SCORECARD.md` = 0 · `grep -c 'recorded absent 2026-10-31' PROVINCE.md` = 0 · `grep -c '^## Attempt 2' corpus/lessons/round-60.md` = 0 (all via `git show 9bc9b20b…:<path> \|`, the do-nothing receipt in the round report) | criterion 118 = 1 · criterion 119 = 1 · host-scope annotations = 3 · province correction = 1 · lesson `## Attempt 2` section = 1; mistakes 6 (host-scoped-instrument) and 7 (over-specified-predicate) mined with captured-by fixes | the five grep commands in this row, run at the final revision with `python`/git available on this host | the records land at the round's final records commit; receipts in the round report |

Sentence-governance note (mistake 7): the planned block above pinned the
sequence arm at "3/8" copied from the Linux receipts; the first scored
family on this host drew 1/8 (still red). Amendment A1
(`.ufo/evidence/round-60/win-host/contract-a2-amend1.json`, frozen
pre-data) re-stated the arm order-dependent-red and the scored family was
re-run post-amendment at `ffa566024616…`. The counter bytes, cells, class
set, expected exits and PASS condition never changed.

**No-harm guard: unverified — provisional regression on record; the
attempt does not self-admit.** The frozen cold-read precheck is infeasible
on this host (75,889 ledger inputs x ~151,778 git spawns/rev x 0.044
s/spawn measured = ~112 min/rev; five runs failed — status receipt
`.ufo/evidence/round-60/win-host/amend1/coldread-precheck.out`). The
lane-authored substitute (noharm-cand.py: frozen decision functions +
proven-safe short-circuit; receipt `noharm-cand.json`) measures **46 of 64
sections credited at the attempt-2 cand** against the frozen instrument's
own **50 at b1ba0ebc** (attempt-1's receipt) — a provisional drop of up to
4 sections whose attribution across attempt-1's two unmeasured tail
commits and attempt-2's record edits (PROVINCE/QUALITY/SOURCES/SCORECARD/
LOG are all ledger-recorded inputs) is unmeasured here. Depth 10,
calibration 8, freshness 9 are unchanged; the harm, if it lands as
measured, is in cold-read credit (the discernment surface). **Round-61
first obligation (planned):** genuine re-reads of the affected SKILL.md
sections recorded as fresh input-keyed ledger entries pinning post-edit
hashes (with `tameshi-trace-inputs-v1` trace receipts), then the monitor
re-run at the final revision until lost=0; a host-portable or bounded form
of the monitor is round-61 design work.

## Planned — round 61 (declared 2026-11-01, fresh-start round, frozen before data)

Last three closures rejected (r58, r59, r60); the r60 verifier spot-check
was read in full before declaring. The lane's own routed remedy (genuine
re-reads → fresh input-keyed ledger entries → monitor re-run toward
lost=0; host-portable monitor design) is claim C2; closure defects D1–D3
land with it. Ruled out: re-running the frozen precheck as-is (host-
infeasible, five failed runs); claiming no-harm from r60's substitute
(cross-revision attribution unmeasured); extending the counter family
(admission is an operator ruling); re-running attempt-1's Linux counting
commands (host-scoped, annotated).

| Claim | The move | Axis / claim type | Before | After (measured) | Counting command | Measured commit |
|---|---|---|---|---|---|---|
| R61-C1 | the frozen no-harm precheck gains a host-portable batched execution form (`tools/coldread-precheck-portable.py`: frozen round-18 decision code unchanged; only `cat_file_blob`/`ls_tree_mode` cache-backed with spawn fallback; chunked/resumable prefetch; spawn-equivalence probe that fails empty) | operability (verdict-only axis); capability acquisition (sourced S289 re-open; S293 opened and rejected as a within-scope duplicate the same round) | the frozen precheck cannot produce a verdict on this host: 75,889 inputs x ~151,778 spawns/rev x 0.044 s/spawn = ~112 min/rev, five failed runs (`.ufo/evidence/round-60/win-host/amend1/coldread-precheck.out`) | full base measure in 7.1 s, `credited=46/64 … probe_sampled=20 probe_mismatches=0` (`.ufo/evidence/round-61/win-host/measure-base.out`); frozen selector vs portable form byte-identical at two revisions over discriminating cells (input-drift, exec-bit, symlink input-not-blob, input-missing, no-ledger-entry) — `DIFFERENTIAL: PASS` (`differential.stdout`) | `python -I tools/coldread-precheck-portable.py --repo . --rev 8b0042bde0ca59aac9a23a8a707cf0902183d081 --work WORK` | `19d7e996b9c88e847d22bcddf467893941a1d242` (tool digest `3e09cace27da2acc859143052c7bd4a5f8f1825737932afb67223729ec0c2fce`) |
| R61-C2 | the r60 remedy: genuine re-reads of all 18 uncredited sections, fresh input-keyed ledger entries + committed trace receipts, monitor re-run toward lost=0; closure defects D1 (first-family receipts landed), D2 (win32-era attempt-1 freeze re-run receipt), D3 (number-drift erratum) land with it | calibration (numeric score 8 unchanged; the move is the no-harm guard, the discernment surface) | at base `8b0042bd…`: 46/64 credited; the 18 uncredited sections all fail on `input-drift:` of r60-edited record files (`rekey-plan.json`, `union-plan.json`); the r60 provisional regression (46 vs 50, cross-revision) on record | TWO batches, both landed (append-only): batch 1 — 18 entries (11,004 input pins at `19d7e996…`), then `COLDREAD_PRECHECK floor=8b0042bde0ca floor_credited=46 cand=72d36ae1aff7 cand_credited=64 lost=0 ok` + `box3_full_page=true` + `EQUIVALENCE … mismatches=0` (receipts `precheck-final.{out,json}`) — superseded the same round by the S293/S289 SOURCES correction (the guard caught the lane's own record edit; batch-1 entries stay as disclosed landed history reading `input-drift:corpus/SOURCES.md`, non-crediting non-vetoing); batch 2 — 18 entries at the corrected bytes (same unions, traces `rekey/traces-2/`), re-establishing credit at the corrected tip, its guard receipt landing with the receipts commit | `python -I tools/coldread-precheck-portable.py --repo . --floor 8b0042bde0ca59aac9a23a8a707cf0902183d081 --cand <rekey rev> --work WORK` | rekey commit `72d36ae1aff7f001f946c326f9143581efc40220`; receipts land in the following commit (receipt-after-subject ordering, the r60 precedent) |

Erratum (round 61; r60 closure defect D3, non-author spot-check §7): the
R60a2-C1 row above reads "ten-arm red family"; both r60 contracts and the
landed receipts declare and carry EIGHT control arms (do-nothing, v1 tool,
always-accept, fingerprint, hash-only, first-path-only, empty-blob-unsound,
sequence). The r60 report's decomposition of the C2 grep count 4 is wrong
on its fourth item; the pinned decomposition at `49ddecf1`:
`grep -n 'counting command host-scoped (linux)' SCORECARD.md` → :2921
(R60-C1 row annotation), :2922 (R60-C2 row annotation), :2978 (the
attempt-2 "What landed" sentence), :2994 (the R60a2-C2 row quoting the
pattern itself — its own counting command). The raw count 4 was correct.
The R60a2-C1 row's "attempt-1 freeze still `instrument=10/10
INSTRUMENT-OK`" now carries its win32-era receipt:
`.ufo/evidence/round-61/win-host/freeze-a1-reverify.json` (r60 closure
defect D2).

## Planned — round 62 (declared 2026-11-01, frozen before data)

The r61 closure admitted with four status-neutral routed defects (RD1–RD4,
`corpus/lessons/round-61-verifier-spotcheck.md` §5), read in full before
declaring. The last three rejected closures (r58, r59, r60 spot-checks)
were re-read per the fresh-start duty; r61 was admitted, so the premise is
stale, but the duty was performed and the r61 fresh-start rulings stand
(frozen spawning precheck as-is: host-infeasible, ~112 min/rev, five failed
runs; no-harm claims from r60's substitute: cross-revision attribution
unmeasured; counter-family extension: admission is an operator ruling;
Linux counting commands: host-scoped, criterion 118). Also ruled out this
round: a new SOURCES row or ANY registry edit — a byte change to
`corpus/SOURCES.md` re-stales the 18 batch-2 rekey pins and owes an
18-section re-read rekey (the r61 carry note), and no correction this round
requires a registry write; and a QUALITY.md criterion append for the mined
mistake class — same monitored-record pricing, recorded as a proposal in
`corpus/lessons/round-62.md` instead.

| Claim | The move | Axis / claim type | Before | After (expected) | Counting command | Measured commit |
|---|---|---|---|---|---|---|
| R62-C1 | close routed defect RD1 in the shipped bytes: the portable precheck's documented probe contract ("fails the run on any mismatch OR an empty sample" — r61 report C1 bullet; lesson lines 32, 123–124) becomes true — a `probe_failed` gate (`sampled >= 1 and mismatches == 0`) guards both measure modes, and fail-closed arms prove the probe can fail (arm-liveness rule adopted from considerthese 2026-10-28 proposal 2: every arm carries an input that moves the outcome) | calibration (numeric score 8 unchanged, at the lane-attainable cap; the move repairs the no-harm instrument's honesty — an empty-sample vacuous pass is the r61 `probe-cannot-fail-empty` defect class); sourced on held row S289, source re-accessed this round (byte-identical re-fetch; no registry edit — pricing above) | `git show ed3a66c2…:tools/coldread-precheck-portable.py \| grep -c "probe_failed\|sampled.*< 1"` → 0; red-before: ARM-VACUOUS on the base bytes exits 0 — the vacuous pass (committed receipt) | the same grep at the work commit → 4 (1 def + 2 call sites + 1 `sampled < 1`); ARM-VACUOUS on the guarded bytes exits 2; ARM-MISMATCH (tampered resume chunk + manifest sha) exits 2 with `mismatches=1` on BOTH byte versions; ARM-CLEAN mismatches=0 both revs; guard re-run on the real repo: `lost=0 ok`, sampled >= 1, mismatches=0, exit 0 | `python -I .ufo/evidence/round-62/win-host/probe-arms.py --lane LANE --tool-base BASE.py --tool-new NEW.py` → `PROBE_ARMS: PASS …`; `python -I tools/coldread-precheck-portable.py --repo . --floor 8b0042bde0ca59aac9a23a8a707cf0902183d081 --cand <work commit> --work WORK` | the work commit (this one); receipts land in the following commit (receipt-after-subject ordering, the r61 precedent) |

RD2/RD3/RD4 corrections (status-neutral, carried with C1, not scored):
number/word-count drift errata for the r61 record — pinned in the erratum
below and in `corpus/lessons/round-61.md` (append-only) and
`corpus/lessons/round-62.md`.

## Erratum — round 61 routed defects RD1–RD4 (2026-11-01; sites re-verified against bytes this round)

- **RD1 (probe-guard prose vs code).** The r61 report C1 bullet and
  `corpus/lessons/round-61.md` (line 32; mistake-1 fix, lines 123–124)
  state the probe "fails the run on any mismatch OR an empty sample" /
  "exit 2 … requires sampled ≥ 1 and mismatches = 0". At base `ed3a66c2`
  the shipped bytes implement only the mismatch half
  (`grep -c "probe_failed\|sampled.*< 1"` → 0). Fixed this round
  (R62-C1 above). Tool digest `3e09cace27da2acc859143052c7bd4a5f8f1825737932afb67223729ec0c2fce`
  (the r61 capability-row digest) refers to the r61 bytes, preserved
  as-run at `.ufo/evidence/round-61/win-host/coldread-precheck-portable.py`;
  the guarded bytes digest is
  `892a045d8b508214804e2b26b78c15b83aae65bdae4bd5bf022b8cb735f3b33e`.
- **RD2 ("21 files" → 20).** `git ls-tree -r 19d7e996 | grep -c first-family/`
  → 20 (also 20 at the r62 base and tip; none elsewhere). The wrong count
  appears at `corpus/lessons/round-61.md:58` ("21 files") and `:134` ("the
  21 first-family receipt bytes") and in the fleet r61 report ("D1
  first-family receipts (21 files)"). Re-verified this round: LOG.md and
  SCORECARD.md carry NO count (`grep -n "21 files\|21 first" LOG.md
  SCORECARD.md` → no hits) and the `19d7e996` commit subject carries none —
  the spot-check's RD2 site list over-stated those three; the receipts
  themselves were genuine and resolving.
- **RD3 ("2,215-line SKILL.md" → 2,214).** `git show ed3a66c2:SKILL.md | wc -l`
  → 2214 (same at base `8b0042bd` and at pin `0a29e3cf`). The wrong number
  appears only in the fleet r61 report ("the complete 2,215-line SKILL.md
  read").
- **RD4 ("12 words" → 8 tokens).** The S289 re-open quote
  "<oid> SP <type> SP <size> LF <contents> LF" is 8 whitespace-separated
  tokens. The wrong label appears at `corpus/lessons/round-61.md:75` and in
  the `corpus/SOURCES.md` round-61 registry note (line 539); the row's
  quote and location are accurate. SOURCES.md is deliberately NOT edited
  this round (re-stale pricing, Planned above); this erratum and the r61
  lesson append are the corrections of record there.

## Round 62 — measured claims (2026-11-01)

| Claim | Verdict | After (measured) | Receipts | Measured commit |
|---|---|---|---|---|
| R62-C1 | verifies (measured) | `grep -c "probe_failed\|sampled.*< 1"`: base `ed3a66c2` → 0, work commit `6b15c943` → 4. `PROBE_ARMS: PASS (vacuous/base=ok vacuous/new=ok mismatch/base=ok mismatch/new=ok clean/new=ok)` — ARM-VACUOUS base exit 0 with `EQUIVALENCE floor_sampled=0 … cand_sampled=0 …` (the vacuous pass, red-before) vs guarded bytes exit 2 (`error=equivalence-probe sampled=0 mismatches=0`); ARM-MISMATCH exit 2 with `floor_mismatches=1` on BOTH byte versions (old gate `error=equivalence-mismatch`, new gate `error=equivalence-probe sampled=9 mismatches=1`); ARM-CLEAN `floor_mismatches=0 cand_mismatches=0`. Guard re-run on the real repo: `COLDREAD_PRECHECK floor=8b0042bde0ca floor_credited=46 cand=6b15c943a73d cand_credited=64 lost=0 ok` + `EQUIVALENCE floor_sampled=20 floor_mismatches=0 cand_sampled=20 cand_mismatches=0`, exit 0 — the r61 verdict unchanged at the guarded tip (no harm) | `.ufo/evidence/round-62/win-host/probe-arms.{py,stdout,stderr}`, `guard-rerun.{out,json}`, `sources/s289-reaccess.out` + `s289-r62.headers` | tool bytes at `6b15c943a73dad797fd1b2d8a96f5683b2d79a51` (digest `892a045d…`); receipts land in the following commit |

Calibration: 8 → 8 (at the lane-attainable cap; the axis verdict this
round is **improved** — the no-harm instrument's probe went from
documented-but-vacuous-pass-able to fail-closed in shipped bytes with a
demonstrated red arm and an intact mismatch arm; the r61
`probe-cannot-fail-empty` class is closed where it lives, in the code).
RD2/RD3/RD4 corrections landed status-neutral (erratum above; no axis
moved by them).

## Planned — round 63 (declared 2026-11-01, frozen before data)

The r62 closure admitted with one status-neutral routed defect (RD5,
`corpus/lessons/round-62-verifier-spotcheck.md` §4/§8) plus the carried RD6;
the spot-check was read in full before declaring, and the RD5 numbers were
re-derived on committed bytes FIRST (red-before receipt
`.ufo/evidence/round-63/win-host/red-before/additivity-redbefore.txt`).
Fresh-start duty: the last three rejected closures (r58, r59, r60
spot-checks) were re-read; r61 and r62 were admitted, so the premise is
stale, but the duty was performed. Ruled out, with reasons: (a) the standing
r59–r62 rulings — the frozen spawning precheck as-is (host-infeasible,
~112 min/rev, five failed runs), no-harm claims from r60's substitute
(cross-revision attribution unmeasured), counter-family extension (admission
is an operator ruling), Linux counting commands (host-scoped, criterion
118), capability admission of the r59 row (operator ruling); (b) any edit to
`tools/coldread-precheck-portable.py` — the guarded digest `892a045d…` is
pinned and any probe edit re-owes the probe-arms re-run (arm-liveness carry
note); this round needs no probe change; (c) an UNpriced registry edit —
this round pays the rekey deliberately (C2), so the QUALITY/SOURCES edits
ride that payment instead of being ruled out as in r62; (d) building
considerthese 2026-10-28 proposal 1 (receipt-existence linter) this round —
real, but it would compete with the rekey for round scope; recorded as a
proposal, not adopted (its cited-receipt-exists core is criterion 108/116
ground).

| # | Claim | The move | Axis / claim type | Before | After (expected) | Counting command | Measured commit |
|---|---|---|---|---|---|---|---|
| R63-C1 | the RD5 correction becomes a standing convention with an instrument: append-only receipts on line-ending-sensitive record files are computed on committed bytes with the normalization declared — `tools/additivity-receipt.py` (new) prints raw AND CR-normalized old-only/new-only counts, discloses a line-ending rewrite (`eol_rewrite_disclosed`), checks the verbatim-prefix property (empties dropped on both sides), judges append-only on the normalized comparison, and its selftest carries the r62 defect shape as a green arm (raw>0, norm=0, disclosed) plus red arms for content alteration and deletion; the RD5 correction row lands with re-measured receipts on the r62 pair | axis move (lowest scored axis; closes routed defect RD5; sourced on new row S294, opened this round: gitattributes — end-of-line conversion is a declared per-path attribute layer, and with no attributes + `core.autocrlf=false` this repo's blobs carry committed bytes verbatim, so byte comparisons must declare normalization) | calibration (numeric score 8 unchanged, at the lane-attainable cap; the move repairs receipt honesty — a receipt's stated command must reproduce its stated number, or state the normalization that reconciles it) | at head `0b81e8f5`: no instrument (`git show 0b81e8f5:tools/additivity-receipt.py` → path does not exist; `ls tools/ \| grep -c additivity` → 0) and the r62 receipts as stated measure 80 (LOG.md) / 30 (SCORECARD.md) old-only lines on raw committed bytes while the corrected content truth is 0/0 CR-stripped with a verbatim prefix (red-before receipt committed pre-data) | selftest `ADDITIVITY_SELFTEST: 5/5 pass` exit 0 (ARM-CLEAN-APPEND raw=0; ARM-EOL-REWRITE the r62 shape with raw>0 norm=0 disclosed; ARM-REQUIRE-RAW exit 1 on the same bytes; ARM-ALTER / ARM-DELETE exit 1); the r62 pair re-measured by the tool: raw_old_only 79/29, norm_cr_old_only 0/0, verbatim_prefix true, eol_rewrite_disclosed true, exit 0 (raw 80/30 vs 79/29 = the empty-line set-member difference, stated in the erratum below); this round's own record appends measure raw_old_only=0 (the rewrite is avoided, not normalized away) | `python -I tools/additivity-receipt.py --selftest`; `python -I tools/additivity-receipt.py --repo . --base ed3a66c2c5458fc6e4ecbc41cbaf93ed05f6db98 --tip 5721f7d5c872f3bf62b73c47bca2dc67015e06b0 --file LOG.md --file SCORECARD.md` | the work commit (tool + erratum); receipts land in the following commit (receipt-after-subject ordering, the r61/r62 precedent) |
| R63-C2 | the RD6 proposal lands through the payment it was waiting for: QUALITY Criterion 120 appended (a described fix is grep-addressable in the shipped bytes, with the counting command in the claim), the RD4 wrong count repaired at its registry-note site (SOURCES.md "12 words" → "8 tokens"), and new row S294 appended — the record edits stale the cold-read credit, and the r61 rebind run-book (analyze → union plan → manifest from genuine section re-reads → rebind) regenerates fresh input-keyed ledger entries with trace receipts, restoring the monitor | axis move + capability (operability, verdict-only; capability row `monitored-record rekey run-book` enters the table — first demonstrated round 61 as the batch rekeys, re-demonstrated this round on a QUALITY+SOURCES edit with the run-book named end to end; closes routed defect RD6) | operability (verdict-only axis; no numeric score — commands exist, run, and produce the stated outcome: the precheck verdict at the tip) | at head `0b81e8f5`: `git show 0b81e8f5:corpus/QUALITY.md \| grep -c "### Criterion 120"` → 0; registry rows 153; no receipt shows the rekey run-book executed for a QUALITY+SOURCES edit pair; at the post-edit pre-rekey revision the round-scoped guard (floor = the round base `0b81e8f5`) reads `cand_credited=51 lost=13 RED` with LOST lines whose input-drift lists name this round's edits `corpus/QUALITY.md` / `corpus/SOURCES.md` (plus record paths older entries already pinned), and rev mode reads `credited=51/64` (the guard catching the lane's own record edits; rehearsal receipt committed with the rekey; the historical-convention floor `8b0042bd` mode reads `lost=0` throughout and is not the stale-set detector) | criterion 120 grep → 1; registry rows 153 → 154; the ledger grows by the fresh entries (680 → 693) with trace receipts committed one file path each; the precheck at the final tip reads `cand_credited=64 lost=0 ok` exit 0 at BOTH floors (`0b81e8f5` and the historical `8b0042bd`) with the probe gate green (sampled ≥ 1, mismatches = 0) | the criterion/rows greps above on committed bytes; `python -c "import json;print(len(json.load(open('.ufo/evidence/round-21/coldread/ledger.json',encoding='utf-8'))['entries']))"`; `python -I tools/coldread-precheck-portable.py --repo . --floor 8b0042bde0ca59aac9a23a8a707cf0902183d081 --cand <tip> --work WORK` | the rekey commit (entries land); final precheck receipt at the receipts commit |

## Erratum — round 62 routed defect RD5 (2026-11-01; re-measured pre-data)

The r62 report's "Landed changes" section states: "Both commits verified
additive on the record files: LOG.md 0 lines removed (e.g. `comm -23` old vs
new sorted line sets → 0), SCORECARD.md 0 removed." As the r62 closure
routed (RD5), that stated command on the raw committed bytes measures 80
(LOG.md) and 30 (SCORECARD.md) old-only lines, not 0/0. This round
re-derives and corrects of record:

- **Cause (confirmed).** The r62 work commit `6b15c943` rewrote the r61 tail
  blocks' line endings LF → CRLF in LOG.md and SCORECARD.md (and inserted
  one blank line at LOG.md line 2). This repo carries no `.gitattributes`
  (`git ls-tree 0b81e8f5 -- .gitattributes` → empty) and no text/eol
  attribute applies to the record files (`git check-attr text eol --` →
  unspecified) with `core.autocrlf=false` in the user config: committed blob
  bytes are whatever was written, so an append that rewrites the file
  normalizes pre-existing lines at the blob level.
- **Content truth (unchanged).** CR-stripped old-only = 0 for both files,
  and each file's CR-stripped, empty-dropped base content is a verbatim
  prefix of its tip (re-verified this round; receipts
  `.ufo/evidence/round-63/win-host/red-before/additivity-redbefore.txt`).
  The r62 append-only claim holds at the content level; what failed was the
  receipt's silence about normalization.
- **Correction of record.** The r62 receipts read "0" only under CR
  normalization that was not stated. Corrected statement: "both commits
  append-only on committed bytes under declared CR normalization
  (raw_old_only 80/30 → 0/0 normalized; rewrite disclosed; verbatim prefix
  true)."
- **Convention adopted (R63-C1).** Future append-only receipts on these
  files are computed by `tools/additivity-receipt.py` on committed bytes and
  print both counts plus `eol_rewrite_disclosed`; append-only is judged on
  the normalized comparison; `--require-raw` exists for contexts that must
  forbid rewrites. Count convention: the tool's raw_old_only (79/29) is one
  line below the closure's sort-u count (80/30) because the inserted empty
  line is not a content member — the empty line is itself part of the
  rewrite disclosure.
- **Practice for this round's own appends.** r63 appends to LOG.md,
  SCORECARD.md, QUALITY.md and SOURCES.md are written as binary appends in
  each file's own ending (CRLF), touching no pre-existing byte; the round's
  receipts-commit run of the tool on the r63 pair is expected to read
  `raw_old_only=0 eol_rewrite_disclosed=false` (checked when the receipts
  land).

## Round 63 — measured claims (2026-11-01; L1 `TameshiR63`)

Work commit `8616d47ebbb825ecbe0e15be142d77946710a026` (declared block +
erratum + instrument + records + red-before receipts); rekey commit
`a18c20f07bb830245940c5d0a52b19d772f1f126` (pushed; entries, traces,
machinery as-run, the SCORECARD CRLF byte-restoration of lesson mistake 4,
lesson mistakes 3–4). Receipts: `.ufo/evidence/round-63/win-host/`. A
content-identical scratch-clone rehearsal (revs `9b3d0644`, `a46cb113`,
`15750f66`, `f0eefec9`) preceded the live run and produced lesson mistakes
3–4; the clone is deleted with the round's scratch.

| Claim | Verdict | After (measured) | Receipts | Measured commit |
|---|---|---|---|---|
| R63-C1 | verifies (measured) | selftest `ADDITIVITY_SELFTEST: 5/5 pass` exit 0 (ARM-CLEAN-APPEND raw=0 exit 0; ARM-EOL-REWRITE the r62 shape raw=10 norm=0 disclosed exit 0; ARM-REQUIRE-RAW exit 1 on the same bytes; ARM-ALTER / ARM-DELETE norm=1 exit 1). r62 pair re-measured by the tool: LOG.md raw_old_only=79 norm_cr_old_only=0, SCORECARD.md 29/0, round-61 lesson 0/0 — verbatim_prefix=true, eol_rewrite_disclosed=true on the two rewritten files, exit 0 (the raw counts sit one line under the closure's sort-u 80/30 because the inserted empty line is not a content member — stated in the erratum). The r63 landed pair reads raw_old_only=0 with eol_rewrite_disclosed=false on LOG.md, SCORECARD.md, QUALITY.md (the avoided-rewrite practice). Mistake-4 receipt: the instrument measures commit `8616d47`'s own SCORECARD as raw_old_only=2388 norm=0 prefix=true rewrite-disclosed — the RD5 class caught in this round's own commit and byte-restored before anything was pushed | `python -I tools/additivity-receipt.py --selftest`; `python -I tools/additivity-receipt.py --repo . --base ed3a66c2… --tip 5721f7d5… --file LOG.md --file SCORECARD.md`; `.ufo/evidence/round-63/win-host/additivity/receipts.txt` (all four runs); red-before `…/red-before/additivity-redbefore.txt` | tool bytes at `8616d47` (unchanged `8616d47` → `a18c20f0`); receipts at `a18c20f0` |
| R63-C2 | verifies (measured) | Criterion 120 grep 0 → 1; registry rows 153 → 154 (S294 appended, census-clean; the RD4 site repaired "12 words" → "8 tokens", logged old → new); ledger 680 → 693 (13 fresh input-keyed entries, 11,012 input pins at the pin rev `8616d47`) with 13 committed trace receipts; the guard caught the round's own record edits at `8616d47` — round-scoped floor `0b81e8f5`: `cand_credited=51 lost=13 RED` (LOST lines name `corpus/QUALITY.md` / `corpus/SOURCES.md`; rev mode `credited=51/64`) — and the rebind restored it at `a18c20f0`: rev mode `credited=64/64`, round-scoped floor `lost=0 ok`, historical floor `8b0042bd`: `lost=0 ok`, all exit 0 with the probe gate green (sampled=20, mismatches=0) | `git show a18c20f0:corpus/QUALITY.md \| grep -c "### Criterion 120"` → 1; `git show a18c20f0:corpus/SOURCES.md \| grep -cE '^\| S294 '` → 1; `python -c "import json;print(len(json.load(open('.ufo/evidence/round-21/coldread/ledger.json',encoding='utf-8'))['entries']))"` → 693; the three `COLDREAD_PRECHECK`/`COLDREAD_PORTABLE` lines above (receipts `precheck-b.json`, `precheck-b-histfloor.json`, `precheck-rev-b.json`, red receipt `…/win-host/live-red.json` at `8616d47`) | rekey commit `a18c20f07bb830245940c5d0a52b19d772f1f126` |

Capability row entered (see `## Capabilities`): **monitored-record rekey
run-book** — first demonstrated round 61 (the two batch rekeys), named and
re-demonstrated end to end this round on a QUALITY+SOURCES edit pair
(analyze → union plan → manifest from genuine section re-reads → rebind →
monitor restore), with the pre-landing scratch rehearsal and the
commit-plumbing path discipline (mistake 3) now part of the run-book.

Axis verdicts: **calibration: improved** (8 → 8 at the lane-attainable cap;
the move is receipt honesty — the r62 stated-command defect now has a
correction of record, a standing convention, a committed instrument with a
red/green selftest, and the defect class caught recurring in this round's
own tooling before push). **Operability: improved** (verdict-only axis; the
RD6 criterion landed through the payment it was priced at, and the run-book
executed end to end on this host a second time). No owned axis harmed:
depth 10, freshness 9 unchanged (not re-measured; no depth or freshness
surface touched); the no-harm guard reads `lost=0 ok` at the tip at both
floors with the probe gate green. SOURCES 153 → 154 (S294 mined,
census-clean); PROVINCE.md, SKILL.md, README.md, `tools/registry.json` and
the guarded probe (`892a045d…` digest) byte-unchanged `0b81e8f5` → `a18c20f0`.
## Planned — round 64 (declared 2026-11-01, frozen before data)

The r63 closure (non-author verifier spot-check, `d0baf616` = the commit
that landed it) admitted with two status-neutral carry-in observations; both
are addressed this round and C1 is one of them. Fresh-start duty: the last
three rejected closures (r58, r59, r60 spot-checks) re-read before
declaring; the premise is stale (r61/r62/r63 admitted) but the duty was
performed and the standing rulings honored (r58: certification/controls
discipline; r59: cheat-discriminating counters, criterion 111; r60: the
no-harm guard verified on this host — the portable precheck, digest
`892a045d…`, ran at every measured rev below). Ruled out, with reasons
(full detail in `corpus/lessons/round-64.md`): (a) any edit to
`tools/coldread-precheck-portable.py` — guarded digest pinned, probe-arms
re-run owed on any edit; the round-64 win-host copy is byte-identical
(digest verified); (b) the standing r59–r62 rulings (frozen spawning
precheck host-infeasible; counter-family extension an operator ruling;
Linux counting commands host-scoped); (c) SKILL/QUALITY/README/PROVINCE
edits — each extends the rekey payment; the measured pin sets (9 SKILL /
6 QUALITY / 7 README / 13 SOURCES latest-entry pins, QUALITY ⊂ SOURCES,
receipt `rehearsal/pin-sets.txt`) price this round's SOURCES edit at
exactly one rekey; (d) a full-corpus receipt sweep over all lessons since
round 1 — the tool exists after this round, the deciding demonstration is
scoped to the newest round's records, and the whole-history sweep is
declared future work here rather than a smuggled claim. Criterion 110
forecast: the SOURCES edit is predicted (measured in the scratch-clone
rehearsal BEFORE this declaration — receipts `rehearsal/rehearsal-B-guard.txt`,
candidate `b5568919`) to lose exactly the 13 SOURCES-pinning sections
(`lost=13 RED`), and the ledger edit alone to lose none (`lost=0 ok` at
`37d1bca1`); miss = 0 if the live work commit reproduces it.

| # | Claim | The move | Axis / claim type | Before | After (expected) | Counting command | Measured commit |
|---|---|---|---|---|---|---|---|
| R64-C1 | the ledger's run-book batch attribution becomes explicit, addressable, and self-recording: every run-book entry gains `rekey_batch` (insert-before pure insertions, CRLF — the field the r63 closure asked for), the convention is stated of record (`rekey_round` = run-book generation id 61; `rekey_batch` = executing run id), and the r64 rebind machinery itself emits `rekey_batch: r64-batch-1` on its fresh entries, so the next run-book run self-identifies; sourced on new row S295 (W3C PROV-DM — a derived record's provenance binds it to the activity that produced it and the generation event), opened this round | axis move (lowest scored axis; closes the r63 closure's carry-in observation 1; root cause located: `'rekey_round': 61` hardcoded in the as-run rebind, inherited r61 → r63 — lesson mistake 4) | calibration (numeric score 8 unchanged, at the lane-attainable cap; the move is record-attribution honesty: entries produced by one run-book execution become addressable as one batch, and the field that mislabeled them is corrected in data, convention and machinery) | at head `d0baf616`: run-book entries with a batch field → 0; the 49 entries carry only `rekey_round: 61` across read_revs `19d7e996…`/`0a29e3cf…`/`8616d47…` with no batch discriminator (18/18/13) | 49 entries carry `rekey_batch` (`r61-batch-1` 18, `r61-batch-2` 18, `r63-batch-1` 13), JSON valid, at the C1 commit; 62 with `r64-batch-1` 13 after the rekey commit; the ledger edit alone leaves the guard green (`lost=0 ok` — measured at rehearsal A; the frozen selector ignores the ledger as an input and no credited entry pins it); additivity `raw_old_only=0` at both edit points (pure insertions; `verbatim_prefix=false` disclosed — mid-file insertions) | `git show <rev>:.ufo/evidence/round-21/coldread/ledger.json \| grep -c '"rekey_batch"'` → 0 / 49 / 62; per-batch: `git show <rev>:<ledger> \| python -c "import json,sys,collections;d=json.load(sys.stdin);print(dict(collections.Counter(e.get('rekey_batch') for e in d['entries'] if e.get('rekey_batch'))))"`; the guard: `python -I tools/coldread-precheck-portable.py --repo . --floor d0baf616… --cand <C1 commit> --work WORK` | the C1 commit (declared work); receipts land in the following commit(s) |
| R64-C2 | `tools/receipt-exists.py` (new): the cited-receipt-existence sweep on committed bytes — the half of considerthese 2026-10-28 proposal 1 that criterion 120's landing left open (the r63 carry note names it the top unadopted proposal; this round adopts it): named documents read at a pinned revision via `git show REV:path`, backtick-cited `.ufo/`+`tools/` paths extracted (line-scoped spans, disclosed skip rules), each resolved by `git cat-file -e REV:path` (blob or tree — the r53.2 cited-directory class), `--extra-root` resolving the lane's fleet-root-surface cites with a named filesystem check; 4-arm hermetic selftest; the SOURCES edits that carry the sourcing (new row S295, the S289 used-by re-open with a fresh located quote, the round note) stale the 13 SOURCES-pinning sections and the r61 rekey run-book (reused: the r63 as-run machinery re-driven at this round's constants, diff receipted) regenerates them as `r64-batch-1` with trace receipts and restores the monitor; capability row `receipt-existence sweep` enters the table | axis move + capability (operability, verdict-only; closes the considerthese proposal-1 cited-receipt-exists half; ground re-opened on held S289) | operability (verdict-only axis: the tool exists, runs on this host, its selftest passes, and its demonstration sweep runs on committed bytes at the tip) | at head `d0baf616`: `git show d0baf616:tools/receipt-exists.py` → path does not exist; `git ls-tree d0baf616 tools/ \| grep -c receipt-exists` → 0; registry rows 154; the proposal's cited-receipt-exists half unimplemented | selftest `RECEIPT_EXISTS_SELFTEST: 4/4 pass` exit 0; demonstration sweep at the tip on `corpus/lessons/round-63.md` + `corpus/lessons/round-63-verifier-spotcheck.md` → `docs=2 paths=16 missing=0 extra=2` exit 0 (the 2 EXTRA lines name the fleet-root surfaces `.ufo/l0-questions.md` and `.ufo/reports/round-63/tameshi.md` cited lane-relatively — the sweep catches the cross-surface class and names where each resolves); S295 grep → 1; registry rows 154 → 155; the precheck RED at the work commit (`lost=13`, matching the forecast, miss=0) and `lost=0 ok` exit 0 at both floors at the rekey commit and the tip | the greps above on committed bytes; `python -I tools/receipt-exists.py --selftest`; `python -I tools/receipt-exists.py --repo . --rev <tip> --doc corpus/lessons/round-63.md --doc corpus/lessons/round-63-verifier-spotcheck.md --extra-root <fleet-root>`; `python -I tools/coldread-precheck-portable.py --repo . --floor 8b0042bd… --cand <tip> --work WORK` | the work commit (tool + SOURCES edits); demo and guard receipts at the receipts commit |
## Round 64 — measured claims (2026-11-01; L1 `TameshiR64`)

Work commits: C1 `33cb4b0d627f1b06067bf002c256bc6da1eed962` (declared
planned block + criterion-110 measured forecast + ledger `rekey_batch` +
lesson + LOG + rehearsal receipts); C2 `b31e81456b9860a1bf5dddfa678cfd2df59149d9`
(tool + SOURCES edits + fetch receipts); rekey
`1763db52b42c7e0776a2d03b39dbf0db5d6adc59` (the live RED paid: 13 fresh
entries as `r64-batch-1`, monitor restored). Receipts commit: this one.
A `--no-checkout` scratch clone rehearsed every stage before the live run
(rehearsal revs `37d1bca1` / `b5568919` / `1144148e`; receipts
`.ufo/evidence/round-64/win-host/rehearsal/`); the clone is deleted with
the round's scratch.

| Claim | Verdict | After (measured) | Counting commands (live outputs in the receipts commit) | Measured commit |
|---|---|---|---|---|
| R64-C1 | verifies (measured) | `rekey_batch` 0 → 49 at the C1 commit (batches 18/18/13), 0 → 62 at the rekey commit (`r61-batch-1` 18, `r61-batch-2` 18, `r63-batch-1` 13, `r64-batch-1` 13); JSON valid (693 → 706 entries); the ledger edit alone leaves the guard green — live at `33cb4b0d`: `COLDREAD_PRECHECK floor=d0baf616bb8a floor_credited=64 cand=33cb4b0d627f cand_credited=64 lost=0 ok`, probe 20/20 (the frozen selector ignores the ledger as an input; no credited entry pins it — measured, not assumed); additivity on the ledger pair base→C1/C: `raw_old_only=0` (pure insertions; 3 distinct inserted lines at C1, 32 at C; `verbatim_prefix=false` = the disclosed mid-file insertion shape) | `git show <rev>:.ufo/evidence/round-21/coldread/ledger.json \| grep -c '"rekey_batch"'` → 0 / 49 / 62; the per-batch counter; `python -I tools/coldread-precheck-portable.py --repo . --floor d0baf616… --cand 33cb4b0d… --work WORK` → `lost=0 ok` exit 0 (receipt `…/win-host/live-A-guard.txt`); `python -I tools/additivity-receipt.py --repo . --base d0baf616… --tip 1763db52… --file .ufo/evidence/round-21/coldread/ledger.json` (receipt `…/live-additivity-battery.txt`) | C1 commit `33cb4b0d627f1b06067bf002c256bc6da1eed962`; batch counter receipts at the rekey commit |
| R64-C2 | verifies (measured) | `tools/receipt-exists.py` 0 → 1; selftest `RECEIPT_EXISTS_SELFTEST: 4/4 pass` exit 0 (green / red exit 1 / usage exit 2 / extra-root arms, hermetic under TMPDIR); demonstration sweep at the rekey tip on the r63 records: `RECEIPT_EXISTS: docs=2 paths=16 missing=0 extra=2` exit 0 — the two EXTRA lines name the fleet-root surfaces `.ufo/l0-questions.md` and `.ufo/reports/round-63/tameshi.md` cited lane-relatively (the sweep catches the cross-surface class and names where each resolves); S295 0 → 1; registry rows 154 → 155 (census-clean, no new warning; mid-census exit 0 at the working tree, end census with the receipts commit); the SOURCES edit staled exactly the forecast: live RED at `b31e8145`: `cand_credited=51 lost=13 RED` — the same 13 headings the planned block named, miss = 0; the run-book restored it at `1763db52`: `lost=0 ok` exit 0 at the round floor AND the historic floor `8b0042bd` (46 → 64), rev mode `credited=64/64`, probe sampled=20 mismatches=0 everywhere | `git ls-tree <rev> tools/ \| grep -c receipt-exists` → 0 / 1; `python -I tools/receipt-exists.py --selftest`; `python -I tools/receipt-exists.py --repo . --rev 1763db52… --doc corpus/lessons/round-63.md --doc corpus/lessons/round-63-verifier-spotcheck.md --extra-root <fleet-root>`; `git show <rev>:corpus/SOURCES.md \| grep -cE '^\| S295 '` → 0 / 1; the `COLDREAD_PRECHECK`/`COLDREAD_PORTABLE` lines above (receipts `…/win-host/live-B-red.txt`, `live-C-green.txt`, `live-C-green-hist.txt`, `live-C-revmode.txt`, `live-demo-sweep.txt`) | rekey commit `1763db52b42c7e0776a2d03b39dbf0db5d6adc59` |

Capability row entered (see `## Capabilities`): **receipt-existence
sweep** — first working round 64.

Axis verdicts: **calibration: improved** (8 → 8 at the lane-attainable cap;
the move is record-attribution honesty — the r63 closure's precision
observation now has its field in the data, the convention of record, and
the machinery that writes it; root cause located at the hardcoded constant,
lesson mistake 4). **Operability: improved** (verdict-only axis; the
considerthese proposal-1 cited-receipt-exists half adopted and demonstrated;
the run-book executed end to end on this host a third time, reused rather
than re-derived). No owned axis harmed: depth 10, freshness 9 unchanged (no
depth or freshness surface touched); the no-harm guard reads `lost=0 ok` at
the rekey tip at both floors with the probe gate green; SOURCES 154 → 155
(S295 mined, census-clean); PROVINCE.md, SKILL.md, README.md,
`tools/registry.json` and the guarded probe (`892a045d…` digest) byte-unchanged
`d0baf616` → `1763db52`.
## Planned — round 65 (declared 2026-11-01, frozen before data)

The r64 closure (non-author verifier spot-check, `7d7f9ca8` = the commit
that landed it) admitted with status-neutral routed defects; all three
carry-in items are addressed FIRST this round, status-neutral, before any
claim work: the empty-commit `6876d746` correction note; the
tip-confirmation historic-floor line added by EXECUTION (guard re-run at
floor `8b0042bd` cand `6876d746` → `lost=0 ok` exit 0, receipt
`.ufo/evidence/round-65/win-host/tipfix-hist-floor.txt`, line appended to
the r64 receipt under a dated header); the live-B-red truncation note. A
convention of record is stated: a commit naming receipt content carries the
bytes. Fresh-start duty: the last three rejected closures (r58/r59/r60
spot-checks) re-read — the premise is stale (r61–r64 admitted), the standing
rulings are honored, and the ruled-out list with reasons is in
`corpus/lessons/round-65.md`. Criterion-110 forecast, measured in the
scratch-clone rehearsal BEFORE this declaration (receipts
`.ufo/evidence/round-65/win-host/rehearsal/rehearsal-red.out` and
`rehearsal-red.json`, candidate `77d439955bb6…`): the SOURCES edit (new row
S296 + the round-65 tail note, a pure 2-line insertion) is predicted to lose
exactly the 13 SOURCES-pinning sections — `cand_credited=51 lost=13 RED`,
the same 13 headings as the r63/r64 manifests (miss = 0 if the live work
commit reproduces it); the rekey run-book (the r64 as-run machinery
re-driven at this round's constants, batch `r65-batch-1`, diff receipted)
regenerates them and restores the monitor. No other planned edit touches a
monitored file (both tools are new files; LOG/SCORECARD appends are not
monitor inputs; the two r64 evidence receipts receive dated appends only).

| # | Claim | The move | Axis / claim type | Before | After (expected) | Counting command | Measured commit |
|---|---|---|---|---|---|---|---|
| R65-C1 | the receipt-commit binding convention becomes mechanically checkable: new `tools/receipt-commit-bind.py` sweeps a commit range (git objects only) and requires every path ADDED under `.ufo/evidence/` whose basename is named in a commit's message (with, or — 8+ chars — without extension, delimited-token match, disclosed rule) to exist in that commit's tree; violations print `BIND_DEFECT` with exit 1; a range adding no evidence file exits 2 (fail-closed, no vacuous pass); 4-arm hermetic selftest whose red arm is the synthetic 6876d746 shape; stated convention of record (lesson + this block) and the r64 correction note land first (status-neutral); sourced on new row S296 (git's own `--allow-empty` paragraph — a same-tree commit is a mistake), opened this round | axis move (lowest scored axis; closes the r64 closure's routed defect 1 class) | calibration (numeric score 8 unchanged, at the lane-attainable cap; the move is record-attribution honesty: the empty-commit receipt-mismatch class becomes a named, mechanically flagged defect instead of a closure observation) | at head `7d7f9ca8`: the class exists undetected — `git cat-file -e 6876d7460c75…:.ufo/evidence/round-64/win-host/tip-confirmation.txt` fails (exit 128, path not in that commit) while `git log -1 --format=%B 6876d7460c75… \| grep -c tip-confirmation` → 1; no instrument: `git ls-tree 7d7f9ca8 tools/ \| grep -c receipt-commit-bind` → 0 | selftest `RECEIPT_COMMIT_BIND_SELFTEST: 4/4 pass` exit 0; sweep over the r64 round range `d0baf616..c7d28b19` → exactly 1 BIND_DEFECT (`6876d746` naming `tip-confirmation`), exit 1 — the historical defect discriminated; sweep over this round's own range → `findings=0` exit 0 (this round's messages name only receipts they carry); S296 grep → 1; registry rows 155 → 156; the guard RED at the work commit (`lost=13`, matching the forecast, miss=0) and `lost=0 ok` exit 0 at both floors at the rekey commit and the tip | `python -I tools/receipt-commit-bind.py --selftest`; `python -I tools/receipt-commit-bind.py --repo . --base d0baf616… --tip c7d28b19…`; `python -I tools/receipt-commit-bind.py --repo . --base 7d7f9ca8… --tip <K5>`; `git show <rev>:corpus/SOURCES.md \| grep -cE '^\| S296 '`; the `COLDREAD_PRECHECK` lines above | the C1 work commit (declared work); receipts land in the following commit(s) |
| R65-C2 | `tools/quoted-line-exists.py` (new): the byte-for-byte quoted-line half of considerthese 2026-10-28 proposal 1 (the r64 landing left it open; this round adopts it — the ONE assimilation): quoted counter lines in a record must be byte-backed by committed receipt bytes at a pinned rev — document sweep extracts verdict-shaped backtick spans (disclosed shape rules) and the receipt cites the record itself makes (full `.ufo/`+`tools/` paths; directory cites expand; bare basenames resolve by unique-basename; fleet-root surface cites via a named `--extra-root` filesystem check — the r64 cross-surface class), each quote must be a byte substring of some cited receipt's committed bytes; explicit `--receipt/--quote` mode; exit map 0/1/2 with a fail-closed empty-document guard (a do-nothing record scores 2, not 0); 4-arm hermetic selftest whose red arms are the always-back and exit-0-always cheat family (criterion 111 shape); capability row `quoted-line receipt backability` enters the table | axis move + capability (operability, verdict-only; closes the considerthese proposal-1 quoted-line half) | operability (verdict-only axis: the tool exists, runs on this host, its selftest passes, and its demonstration sweep runs on committed bytes at the tip) | at head `7d7f9ca8`: `git show 7d7f9ca8:tools/quoted-line-exists.py` → path does not exist; `git ls-tree 7d7f9ca8 tools/ \| grep -c quoted-line` → 0; the r64 records' quotes had no byte-backing check (the r64 closure re-derived quotes by hand) | selftest `QUOTED_LINE_EXISTS_SELFTEST: 4/4 pass` exit 0; demonstration sweep at the tip on `corpus/lessons/round-64.md` + `corpus/lessons/round-64-verifier-spotcheck.md` → `backed=12 missing=4` exit 1 with all four unbacked quotes named — the disclosed finding class (one verifier re-derivation line in no committed receipt; three sha-abbreviated quote shapes), honest about the records without retroactive repair; explicit-mode pair on `live-selftest.txt` → backed exit 0; the precheck RED at the work commit (`lost=13`, miss=0 vs forecast) and `lost=0 ok` at the rekey commit and the tip | `python -I tools/quoted-line-exists.py --selftest`; `python -I tools/quoted-line-exists.py --repo . --extra-root <fleet-root> --doc <tip>:corpus/lessons/round-64.md --doc <tip>:corpus/lessons/round-64-verifier-spotcheck.md`; `python -I tools/quoted-line-exists.py --repo . --receipt <tip>:.ufo/evidence/round-64/win-host/live-selftest.txt --quote "RECEIPT_EXISTS_SELFTEST: 4/4 pass"`; the `COLDREAD_PRECHECK` lines above | the work commit (tool); demo and guard receipts at the receipts commit |
## Round 65 — measured claims (2026-11-01; L1 `TameshiR65`)

Carry-in `8fd65296ade85c802a22945fc2fbc2a8121f38f4` (status-neutral, before
any claim work); declaration `142125293358df7df8543643a8bdc06cac1775bc`
(planned block + criterion-110 measured forecast + lesson + rehearsal
receipts); work commits C1 `3b833293b1bf062c97f6169e650ddee42d2d5335` (bind
checker + SOURCES S296 + the round-65 tail note) and C2
`3fa08b2c66271989dbbe766720e54b19a911f1c6` (quoted-line checker); rekey
`6db7e2fcfee6d00ac6fc18445a52eed42db43054` (the live RED paid: 13 fresh
entries as `r65-batch-1`, monitor restored at both floors). Receipts
commit: this one. A `--no-checkout` scratch clone rehearsed every stage
before the live run (rehearsal revs `77d43995…` / `92472f92…` /
`5535367d…`; receipts `.ufo/evidence/round-65/win-host/rehearsal/`); the
clone is deleted with the round's scratch.

| Claim | Verdict | After (measured) | Counting commands (live outputs in the receipts commit) | Measured commit |
|---|---|---|---|---|
| R65-C1 | verifies (measured) | selftest `RECEIPT_COMMIT_BIND_SELFTEST: 4/4 pass` exit 0 at the committed bytes; the r64-range sweep flags exactly the carry-in defect — `BIND_DEFECT 6876d7460 names tip-confirmation -> .ufo/evidence/round-64/win-host/tip-confirmation.txt not carried at that commit`, `findings=1` exit 1, plus `BIND_OK c7d28b19e carries …` (the carrying commit reads green) — the historical class discriminated, no post-hoc rewrite; this round's own range sweep `commits=5 evidence=34 named=0 carried=0 findings=0` exit 0 (no commit in `7d7f9ca8..6db7e2fc` names an in-range-added evidence file without carrying it); S296 grep 0 → 1; registry rows 155 → 156 (census-clean, no new warning; start and end census exit 0, the same 17 W04 + 1 W01 set); the guard RED at the work commit `lost=13` matching the criterion-110 forecast (miss = 0, the same 13 headings) → `lost=0 ok` exit 0 at the rekey commit at BOTH floors (round `7d7f9ca8`, historic `8b0042bd` 46 → 64) + rev mode `credited=64/64`, probe 20/20 everywhere | `python -I tools/receipt-commit-bind.py --selftest`; `python -I tools/receipt-commit-bind.py --repo . --base d0baf616… --tip c7d28b19…` (receipt `…/win-host/live-bind-r64-range.txt`); `python -I tools/receipt-commit-bind.py --repo . --base 7d7f9ca8… --tip 6db7e2fc…` (receipt `live-bind-r65-range.txt`); `git show <rev>:corpus/SOURCES.md \| grep -cE '^\| S296 '` → 0 / 1; the `COLDREAD_PRECHECK` lines (receipts `live-red.out`, `live-green.out`, `live-green-hist.out`, `live-revmode.out`) | C1 commit `3b833293…`; sweep and guard receipts at the receipts commit |
| R65-C2 | verifies (measured) | `tools/quoted-line-exists.py` 0 → 1; selftest `QUOTED_LINE_EXISTS_SELFTEST: 4/4 pass` exit 0 (explicit green/red, doc-sweep red, vacuous-usage arms — the do-nothing record scores 2, the always-back cheat fails arm 2/3); demonstration sweep at the rekey tip on the r64 records: `docs=2 quotes=16 backed=12 missing=4` exit 1 — every receipt-backed quote in both records is byte-backed and the four unbacked quotes are NAMED (`SETS MATCH (miss=0 vs forecast confirmed)` — a verifier re-derivation line in no committed receipt; three sha-abbreviated quote shapes where the record's quote is not a byte substring of the receipt line) — the finding class the adopted proposal named, disclosed rather than retroactively repaired; explicit mode `RECEIPT_EXISTS_SELFTEST: 4/4 pass` backed exit 0 against `live-selftest.txt`; the shared no-harm story as C1 (RED `lost=13` miss=0 → `lost=0 ok` both floors) | `python -I tools/quoted-line-exists.py --selftest`; `python -I tools/quoted-line-exists.py --repo . --extra-root <fleet-root> --doc 6db7e2fc…:corpus/lessons/round-64.md --doc 6db7e2fc…:corpus/lessons/round-64-verifier-spotcheck.md` (receipt `…/win-host/live-quoted-demo.txt`); `python -I tools/quoted-line-exists.py --repo . --receipt 6db7e2fc…:.ufo/evidence/round-64/win-host/live-selftest.txt --quote "RECEIPT_EXISTS_SELFTEST: 4/4 pass"` (receipt `live-quoted-explicit.txt`) | C2 commit `3fa08b2c…`; demo receipts at the receipts commit |

Capability rows entered (see `## Capabilities`): **commit-message receipt
binding sweep** and **quoted-line receipt backability** — both first working
round 65 (the two mid-file insertions in the capabilities table are
disclosed; additivity `raw_old_only=0` on the file holds).

Axis verdicts: **calibration: improved** (8 → 8 at the lane-attainable cap;
the move is record-attribution honesty — the r64 closure's "a receipt named
in a commit subject should exist in that commit's bytes" is now a convention
of record with a mechanical checker whose red arm is the landed historical
defect itself). **Operability: improved** (verdict-only axis; the
considerthese proposal-1 quoted-line half adopted and demonstrated on real
records with genuine findings; the rekey run-book executed end to end on
this host a second reuse, constants-only machinery diff receipted). No owned
axis harmed: depth 10, freshness 9 unchanged (no depth or freshness surface
touched — PROVINCE.md `8388c23a…`, SKILL.md `95d1f935…`, README.md
`451e8236…`, `tools/registry.json` `62c4670d…` and the guarded probe
`tools/coldread-precheck-portable.py` `e827e6e5…` blob-identical `7d7f9ca8`
→ `6db7e2fc`; SHONEN.md `253f3c05…` unchanged; the leg ledger untouched, so
command D still reads `recorded_cases=10 depth_score=10`); the no-harm guard
reads `lost=0 ok` at the rekey tip at both floors with the probe gate green;
SOURCES 155 → 156 (S296 mined, census-clean); additivity `raw_old_only=0` on
every landed pair (`live-additivity-battery.txt`: SOURCES mid-file insertion
`verbatim_prefix=false` disclosed, LOG/SCORECARD pure appends
`verbatim_prefix=true`, ledger mid-file `verbatim_prefix=false` disclosed).
## Erratum — round 65 K7 (2026-11-01; appended at the receipts tip)

The tip-receipts commit `87e955975ff6f4fcfcc953ed8fe93ea37804b1df` repeated
the routed r64 defect shape: its message names four receipt files
(live-tip-guard.txt, live-tip-guard-hist.txt, live-bind-full-range.txt,
live-additivity-final.txt) while the commit is EMPTY — the files were
written to the scratch and never copied into the lane worktree before the
commit (`git diff-tree 5740805d 87e95597` prints nothing). Found by
inspection before closure, NOT by the frozen sweep: the sweep over
`7d7f9ca8..87e95597` reads `findings=0` (receipt
`live-bind-erratum-sweep.txt`) because the frozen rule's candidates are
range-added paths and the named files exist nowhere in the range — the
checker's own vacuous pass on a genuinely defective range (lesson mistake
5, routed to round 66 as the checker's next arm; NOT landed post-data this
round). Correction: this commit lands the four named receipt bytes plus
that sweep receipt. The R65-C1/R65-C2 measured rows above are unchanged —
their receipts all landed with the commits that name them (K0, K2, K3, K4,
K5, K6), the frozen demonstrations stand as measured (the r64-range red
arm, where the named file WAS range-added), and the no-harm guard receipts
(K5/K6) remain valid because this commit is evidence-only (no monitored
file changes base → tip: `git diff-tree 7d7f9ca8 <this commit> --
PROVINCE.md SKILL.md README.md corpus/QUALITY.md corpus/SOURCES.md
tools/registry.json` is empty).

## Planned — round 66 (declared 2026-11-01, frozen before data)

The r65 closure (non-author verifier spot-check, `469cde0f` = the commit
that landed it) admitted with one routed defect for this round: the frozen
bind sweep's candidates scope (range-added paths only) reads a vacuous
`findings=0` on `7d7f9ca8..87e95597`, the range whose empty tip commit
names four receipts it does not carry. Per the frozen-instrument discipline
the fix is THIS round's C1 (declared, not landed post-data), with the
red-before (the `87e95597` case flips from vacuous pass to flagged) and the
green-after (this round's own range sweeps clean). The SOURCES edit is the
round's only monitored-file change; the criterion-110 forecast below was
measured in the plumbing-only scratch rehearsal BEFORE this declaration
(receipts `.ufo/evidence/round-66/win-host/rehearsal/reh-red.out|.err`,
candidate `1a3b00b5cba4a5ec4ba5777996394ab22364fd44`): the SOURCES edit
(new row S297 + the round-66 note, a pure 2-line insertion) is predicted to
lose exactly the 13 SOURCES-pinning sections — `cand_credited=51 lost=13
RED`, the same 13 headings as the r63/r64/r65 manifests (rehearsal heading
sets byte-equal IN ORDER; miss = 0 if the live work commit reproduces it);
the rekey run-book (the r65 as-run machinery re-driven at this round's
constants, batch `r66-batch-1`, diff receipt
`rehearsal/reh-make-rebind-r66.diff`, 7 changed lines across 5 sites,
constants only) regenerates them and restores the monitor. No other planned
edit touches a monitored file (C1's tool is an existing non-monitored
file; C2's tool + manifest are new files; LOG/SCORECARD appends are not
monitor inputs).

| # | Claim | The move | Axis / claim type | Before | After (expected) | Counting command | Measured commit |
|---|---|---|---|---|---|---|---|
| R66-C1 | the bind sweep's candidates scope stops being range-added-only: `tools/receipt-commit-bind.py` gains two arms over every commit in the range — arm 2, every full `.ufo/evidence/…`/`tools/…` span in a commit message must resolve at that commit (`git cat-file -e <commit>:<path>`); arm 3, every file-like token (basename with a disclosed receipt/tool extension) in a commit message must resolve to a path anywhere in that commit's tree, so naming content the tree does not carry is the flagged defect whether or not the range adds it; arm 1 (the frozen range-added rule, per-path first-hit counting) unchanged; selftest 4/4 → 6/6 (new red arms: the nowhere-named `87e95597` shape, the span-absent shape); fail-closed empty-range guard now demands no evidence adds AND no spans AND no tokens; sourced on new row S297 (git-diff-tree docs — the page that defines what `--diff-filter=A` can see, i.e. the frozen scope itself), opened this round | axis move (closes the r65 closure's routed defect 1; the checker blob changes only this round, per the routing) | calibration (numeric score 8 unchanged, at the lane-attainable cap; the move is record-attribution honesty: the vacuous-pass class becomes a flagged defect instead of an inspection finding) | at head `469cde0f`: the frozen sweep over `7d7f9ca8..87e95597` reads `named=0 findings=0` exit 0 on the genuinely defective range (rehearsal receipt `rehearsal/reh-bind-frozen-vacuous.txt`; the r65 receipt `live-bind-erratum-sweep.txt` is the landed record); `git show 469cde0f:tools/receipt-commit-bind.py | grep -c "SPAN_RE\|TOKEN_RE"` → 0 (no message-span or token arm exists) | selftest `RECEIPT_COMMIT_BIND_SELFTEST: 6/6 pass` exit 0; sweep `7d7f9ca8..87e95597` → `findings=4` exit 1, exactly the four `names-unknown` defects at `87e95597` (the r65 empty-commit case caught); sweep `d0baf616..c7d28b19` → still exactly 1 BIND_DEFECT (`6876d746`) exit 1 — the frozen discriminator does not regress; sweep `7d7f9ca8..6db7e2fc` → `findings=0` exit 0; sweep `7d7f9ca8..ced05ce1` → `findings=8` exit 1 (arm 1's four + arm 3's four, all at `87e95597`); this round's own range → `findings=0` exit 0 (green-after); S297 grep 0 → 1; registry rows 156 → 157; the guard RED at the work commit (`lost=13`, miss=0 vs forecast) and `lost=0 ok` exit 0 at both floors at the rekey commit and the tip | `python -I tools/receipt-commit-bind.py --selftest`; `python -I tools/receipt-commit-bind.py --repo . --base 7d7f9ca8… --tip 87e95597…`; `python -I tools/receipt-commit-bind.py --repo . --base d0baf616… --tip c7d28b19…`; `python -I tools/receipt-commit-bind.py --repo . --base 469cde0f… --tip <round tip>`; `git show <rev>:corpus/SOURCES.md \| grep -cE '^\| S297 '`; the `COLDREAD_PRECHECK` lines | the C1 work commit (declared work); receipts land in the following commit(s) |
| R66-C2 | `tools/arm-liveness.py` + `tools/arm-liveness.json` (new; schema `tameshi-arm-liveness-v1`): every declared red arm of the receipt-family counters carries one committed input that must MOVE its tally — the checker extracts the instrument from git objects at the row's pinned revision (never a worktree), runs it `python -I` against the committed input, `ARM_LIVE` only when exit matches AND parsed tally ≥ expect_min AND > baseline, else `ARM_DEAD`; standing rows: bind r64-range red (findings≥1), quoted-line r64-records red (missing≥4), receipt-exists declaration-commit red (missing≥5), instruments pinned at `469cde0f` (C1-independent, causally separable); selftest 4/4 hermetic (live row, dead row, vacuous manifest, usage); capability row `counter-arm liveness check` enters the table | axis move + capability (operability, verdict-only; adopts considerthese 2026-10-28 proposal 2 — the ONE assimilation this round) | operability (verdict-only axis: the capability exists, runs on this host, its selftest passes, and its standing manifest verifies on committed bytes at pinned revisions) | at head `469cde0f`: `git ls-tree 469cde0f tools/ \| grep -c arm-liveness` → 0 — no liveness instrument exists, and the r65 blind spot (mistake 5) was found by inspection, not by any standing check | selftest `ARM_LIVENESS_SELFTEST: 4/4 pass` exit 0; the standing manifest sweep → `rows=3 live=3 dead=0` exit 0; the dead-arm demo — a scratch manifest row pinning the FROZEN bind tool over `7d7f9ca8..87e95597` (expect findings≥1) reads `ARM_DEAD … findings=0` exit 1 (the r65 blind spot caught mechanically), and the same row re-pinned to the r66 tool reads `ARM_LIVE … findings=4` exit 0 (rehearsal receipts `reh-demo-dead.txt` / `reh-demo-live.txt`; live re-run at the round tip) | `python -I tools/arm-liveness.py --selftest`; `python -I tools/arm-liveness.py --repo . --manifest tools/arm-liveness.json`; the demo pair with the scratch manifests at the receipts commit | the C2 work commit (tool + manifest); sweep and demo receipts at the receipts commit |

## Round 66 — measured claims (2026-11-01; L1 `TameshiR66`)

Declaration `b459653c49f262cc9a144d798410bfcb928e8758` (planned block +
criterion-110 measured forecast + lesson + rehearsal receipts); correction
commits `b60ecab3e5ae24d162bb7c0e366cb35fc6d9448d` (intended to land the 21
rehearsal receipt bytes its predecessor's pathspec list missed — but used
workspace-relative paths, so the helper's remove-on-missing semantics
dropped the lesson and LOG instead; lesson mistakes 3–4) and
`d5ab10ff88c0015e526a2cbcfb687fa2f121f8fd` (restores both files and lands
the 21 named receipts; both slips self-caught by the diff-tree-before-
next-stage practice and disclosed in the lesson); work commits C1
`ff251f386dcf368f4c7912f0a4feab2b5ff7c756` (bind checker candidates-scope
arms + SOURCES S297 + the round-66 note) and C2
`e8e0f0e9a06aa3b56d478dfd797fe2d108c902ec` (arm-liveness + manifest);
rekey `5d969f4edbb6611014ec30e133c4b243e4dbf47e` (the live RED paid: 13
fresh input-keyed entries as `r66-batch-1`, monitor restored at both
floors). Receipts commit: this one. A plumbing-only scratch repo rehearsed
every stage before the live run (rehearsal work `1a3b00b5…`, rekey
`42488eb7…`; receipts `.ufo/evidence/round-66/win-host/rehearsal/`, landed
at `d5ab10ff`); the scratch is deleted with the round.

| Claim | Verdict | After (measured) | Counting commands (live outputs in the receipts commit) | Measured commit |
|---|---|---|---|---|
| R66-C1 | verifies (measured), with the own-range erratum below | selftest `RECEIPT_COMMIT_BIND_SELFTEST: 6/6 pass` exit 0 (the two new red arms: nowhere-named `87e95597` shape, span-absent shape); the r65 pre-correction range `7d7f9ca8..87e95597`: FROZEN tool `named=0 carried=0 findings=0` exit 0 (`live-bind-vacuous.txt` — the vacuous pass, the before) vs the r66 tool `findings=4` exit 1 with exactly the four `names-unknown` defects at `87e95597` (`live-bind-erratum-range.txt` — the carry-in catch, the after); the r64 range `d0baf616..c7d28b19` → `findings=1` exit 1 naming `6876d746` only (`live-bind-r64-range.txt` — the frozen discriminator does not regress); the r65 clean range `7d7f9ca8..6db7e2fc` → `findings=0` exit 0 (`live-bind-r65-range.txt`); the full r65 range `7d7f9ca8..ced05ce1` → `named=9 carried=5 findings=8` exit 1, arm 1's four + arm 3's four all at `87e95597` (`live-bind-full-range66.txt`); S297 grep 0 → 1; registry rows 156 → 157 (census-clean, no new warning; the same 17 W04 + 1 W01 set); the guard RED at the work commit `lost=13` matching the criterion-110 forecast (heading sets byte-equal IN ORDER, miss = 0) → `lost=0 ok` exit 0 at the rekey commit at BOTH floors (round `469cde0f` 64 → 64, historic `8b0042bd` 46 → 64) + rev mode `credited=64/64` probe 20/20 | `python -I tools/receipt-commit-bind.py --selftest`; `python -I <frozen bytes> --repo . --base 7d7f9ca8… --tip 87e95597…`; `python -I tools/receipt-commit-bind.py --repo . --base 7d7f9ca8… --tip 87e95597…`; `python -I tools/receipt-commit-bind.py --repo . --base d0baf616… --tip c7d28b19…`; `python -I tools/receipt-commit-bind.py --repo . --base 7d7f9ca8… --tip 6db7e2fc…`; `python -I tools/receipt-commit-bind.py --repo . --base 7d7f9ca8… --tip ced05ce1…`; `git show <rev>:corpus/SOURCES.md \| grep -cE '^\| S297 '`; the `COLDREAD_PRECHECK` lines (receipts `live-red.out`, `live-green.out`, `live-green-hist.out`, `live-revmode.out`) | C1 commit `ff251f38…`; sweep and guard receipts at the receipts commit |
| R66-C2 | verifies (measured) | `tools/arm-liveness.py` + `tools/arm-liveness.json` 0 → 1; selftest `ARM_LIVENESS_SELFTEST: 4/4 pass` exit 0 (live row, dead row, vacuous manifest, usage); the standing manifest sweep → `rows=3 live=3 dead=0` exit 0 (`bind-r64-red findings=1`, `quoted-demo-red missing=4`, `rexists-declare-red missing=5` — every receipt-family red arm now has a committed input that moves it, instruments pinned at `469cde0f` so the rows are C1-independent); the dead-arm demo pair: the FROZEN bind tool pinned over `7d7f9ca8..87e95597` reads `ARM_DEAD bind-candidates-red tally=findings=0 exit=0` exit 1 — the r65 blind spot caught mechanically — and the same row re-pinned to the r66 tool at C2 reads `ARM_LIVE bind-candidates-red tally=findings=4 exit=1` exit 0; the shared no-harm story as C1 (RED `lost=13` miss=0 → `lost=0 ok` both floors + rev 64/64) | `python -I tools/arm-liveness.py --selftest`; `python -I tools/arm-liveness.py --repo . --manifest tools/arm-liveness.json`; the demo pair with the scratch manifests at the receipts commit (`live-demo-dead.txt`, `live-demo-live.txt`, `live-demo-manifest-frozen.json`, `live-demo-manifest-r66.json`) | C2 commit `e8e0f0e9…`; sweep and demo receipts at the receipts commit |

**Own-range erratum (self-caught, corrected in-round, disclosed).** The
declared green-after ("this round's own range → findings=0 exit 0") held at
the declaration state: the sweep over `469cde0f..b459653c` (K1) reads
`findings=0` (K1's message names no file tokens — receipt `live-bind-own-range-k1.txt`).
The correction chain then produced the exact routed defect class ON THIS
ROUND'S OWN HISTORY: K1b `b60ecab3` names 21 rehearsal receipt basenames
its tree does not carry (its pathspec list no-op'd; and its own two
workspace-relative paths dropped the lesson and LOG from the tree), and the
instrument's own sweep over `469cde0f..e8e0f0e9` reads `findings=42` exit 1
— 21 arm-1 defects + 21 arm-3 defects, ALL at `b60ecab3` — with the
correction commit `d5ab10ff` reading `BIND_OK` ×21 and `resolves` ×21
(receipt `live-bind-own-range.txt`). This is the routed r64/r65 class
caught BY THE INSTRUMENT on the round's own records in-round: the round
reports it honestly (the declared findings=0 does not hold on the full
range), the bytes landed at `d5ab10ff`, the slips are lesson mistakes 3–4,
and the standing value is real: any successor sweep of this range now
names `b60ecab3` mechanically instead of by inspection.

Capability row entered (see `## Capabilities`): **counter-arm liveness
check** — first working round 66 (the capabilities-table mid-file insertion
is disclosed; additivity `raw_old_only=0` on the file holds).

Axis verdicts: **calibration: improved** (8 → 8 at the lane-attainable cap;
the move closes the r65 closure's routed defect 1 — the vacuous-pass class
becomes a flagged defect, red arms on the landed historical defects
`6876d746` and `87e95597` and, in-round, on the round's own `b60ecab3`).
**Operability: improved** (verdict-only axis; considerthese proposal 2
adopted and demonstrated: the liveness checker exists, runs on this host,
its selftest passes, its standing manifest verifies on committed bytes at
pinned revisions, and its dead-arm demo catches the r65 blind spot on the
frozen bytes). No owned axis harmed: depth 10, freshness 9 unchanged (no
depth or freshness surface touched — PROVINCE.md, SKILL.md, README.md,
corpus/QUALITY.md, tools/registry.json, the guarded probe
`tools/coldread-precheck-portable.py` (worktree sha256 `892a045d…`),
SHONEN.md and the leg ledger blob-identical `469cde0f` → `5d969f4e`;
`git diff-tree -r --name-status 469cde0f 5d969f4e -- PROVINCE.md SKILL.md
README.md corpus/QUALITY.md tools/registry.json SHONEN.md
tools/mutate-and-run.sh tools/coldread-precheck-portable.py` is empty and
`corpus/SOURCES.md` is the only monitored file in the round's diffs); the
no-harm guard reads `lost=0 ok` at the rekey tip at both floors with the
probe gate green; SOURCES 156 → 157 (S297 mined, census-clean); additivity
`raw_old_only=0` on every landed pair (LOG/SCORECARD pure appends
`verbatim_prefix=true` at base→K4; SOURCES mid-file insertion
`verbatim_prefix=false` disclosed; ledger `verbatim_prefix=false`
disclosed).

## Round-67 corrections — the r66 closure's four routed record defects (appended 2026-11-02, status-neutral, append-only: the stale cells above are preserved and stay flagged by the standing quoted-line sweep; these paragraphs are the corrections of record)

R67 correction 1 — stale selftest figure. The R66-C1 planned row and the
R66-C1 measured row above carry the bind checker's selftest figure as
six-of-seven arms; the final corrected checker bytes (the name-rule v2 blob
landed at `5541abaff6ed2057c97e6c1243135b1da7f9ed6d`) read seven-of-seven —
receipt `.ufo/evidence/round-66/win-host/live-selftest-bind.txt`, whose
summary line is `RECEIPT_COMMIT_BIND_SELFTEST: 7/7 pass` (the seventh arm is
the suffix-collision green arm added with name rule v2). The same stale
figure also sits in the LOG round-final receipts line and in the round-66
lesson's pre-data Verdicts pin (that pin was declared before the rule
correction, and the lesson's mistake-5 section documents the change to
seven-of-seven); the correction of record for all three sites is this
paragraph and the LOG entry appended by the corrections commit.

R67 correction 2 — own-range receipt pointer. The own-range erratum above
cites the sweep as `469cde0f..e8e0f0e9`; the receipt it names
(`live-bind-own-range.txt`, unique in the tree) pins `469cde0f..5d969f4e` —
its summary `commits=6 evidence=42 named=43 carried=22 spans=3 bare=47
findings=42` reproduces byte-identically over that range at the pinned
checker bytes (re-run receipted this round), and the counts over the
formerly cited range are identical either way (all findings at `b60ecab3`).
Correction of record: the range is `469cde0f..5d969f4e`.

R67 correction 3 — "dropped from the tree" wording. The own-range erratum
above (and the correction commit `d5ab10ff`'s message, which is never
rewritten) say the `b60ecab3` slip dropped the lesson and LOG from the
tree. The committed tree never lost them: `b60ecab3` is an empty commit —
its tree is byte-identical to its parent's (`git diff-tree -r --name-status
469cde0f b60ecab3` prints nothing; both files present as the same blobs at
both revisions) — and the drop happened only inside the correction
attempt's landing-set construction, not in any committed tree. The record
states the tree-level fact here.

R67 correction 4 — registry-home sync (the r66 closure's routed defect 3).
The capabilities-table row "commit-message receipt binding sweep" (round
65) cites the selftest as four-of-four — the r65-era figure. The final
checker bytes read seven-of-seven (receipt cited in correction 1); the
row's two range citations remain accurate at the final bytes (the r64 range
still reads one defect, the r65 clean range zero — re-run receipted this
round as manifest-row demonstrations). Under the additivity discipline the
registry home is append-only, so this note is the sync of record; the
standing manifest rows that pin the checker's red arms on real history land
this round as claim R67-C2.

## Planned — round 67 (declared 2026-11-02, frozen before data)

The r66 closure (non-author verifier spot-check, `7362e15c` = the commit
that landed it) ADMITTED round 66 with four status-neutral routed record
defects; they are this round's carry-in and landed FIRST as C1 (corrections
commit `436b60c5`, before this declaration — the before-state is receipted
at the base bytes). The round's claims, declared frozen:

- **C1 (calibration, the lowest scored numeric axis at 8; the move is
  record-attribution honesty).** The four carry-in corrections land
  append-only and verifiably, and the round's own appends satisfy the
  byte-backing discipline: the standing quoted-line sweep over LOG and
  SCORECARD at the round tip reads EXACTLY the base missing and absent
  counts, and the round-67 lesson sweeps clean from birth. The
  instrument-boundary finding made while measuring the before-state is
  declared here, before any data: the stale six-of-seven selftest cells
  are NOT sweep-flagged (they are byte-backed by the r66 rehearsal
  receipt's preserved pre-correction bytes
  `.ufo/evidence/round-66/win-host/rehearsal/reh-selftest-bind.txt`) —
  figure-misattribution is beyond byte-backing, stays inspection-caught,
  and is named as successor instrument work rather than shipped as a
  heuristic (r59's ruling).
- **C2 (operability, verdict-only; sourced on new row S298, opened this
  round).** The counter-arm liveness manifest grows its two declared
  successor rows — the bind checker's erratum-range red arm (the r65
  vacuous-pass case) and the bind checker's own-range red arm (the r66
  self-caught erratum) — pinned at `5541abaf`, real-history committed
  inputs, zero synthetic arms. S298 (git-rev-list documentation, §DESCRIPTION
  first paragraph, fetched-page line 3330, 14 words: "List commits that
  are reachable by following the parent links from the given commit(s)")
  grounds the rows: rev-list enumerates COMMITS by parent links, so the
  r65 erratum range's empty tip commit `87e95597` is in the sweep's walk
  with its message — the exact reason the frozen scope (S297's
  `--diff-filter=A` path set) could never see it.
- Shared no-harm forecast: the SOURCES edit (one row + one tail note, the
  r66 edit shape) is the round's only monitored-file change; the live RED
  at the C2 work commit is forecast at `lost=13 RED` with
  `cand_credited=51` — the SAME 13 headings as the r66 measured RED,
  byte-equal in order, miss = 0 required — paid by the `r67-batch-1`
  rekey (13 fresh input-keyed entries; ledger 732 → 745), restoring
  `lost=0 ok` exit 0 at both floors plus rev mode 64/64 probe 20/20
  (receipts `live-green-r67.out`, `live-green-hist-r67.out`,
  `live-revmode-r67.out`, `rebind-stdout-r67.txt`,
  `arm-liveness-selftest-r67.txt`).

| # | Claim | The move | Axis / claim type | Before | After (expected) | Counting command | Measured commit |
|---|---|---|---|---|---|---|---|
| R67-C1 | the four r66-closure carry-in corrections land append-only (mistake row 4; the stale selftest figure; the own-range receipt pointer; the "dropped from the tree" wording + the registry-home sync note), and the round's own appends introduce zero unbacked quotes and zero absent path cites | axis move (record-attribution honesty; the routed defects fixed as append-only corrections of record, the instrument boundary disclosed pre-data) | calibration (numeric score 8 unchanged, at the lane-attainable cap) | at base `7362e15c` (receipts `corrections-before-greps.txt`, `qline-red-log-base.txt`, `qline-red-scorecard-base.txt`, `qline-red-round-66.txt`): mistake-row-4 grep 0; stale-figure greps 2 (SCORECARD) + 1 (LOG); correction markers 0; sweeps — LOG `missing=40 skipped=40` (8 absent), SCORECARD `missing=10 skipped=178` (6 absent), round-66 lesson `missing=2 skipped=7` (0 absent) | mistake-row-4 grep 1; SCORECARD correction markers 4; LOG corrections entry 1; tip sweeps — LOG `missing=40 skipped=40` and SCORECARD `missing=10 skipped=178` UNCHANGED (same absent counts), the round-67 lesson sweep exit 0 with zero missing and zero absent | `git show <rev>:corpus/lessons/round-66.md \| grep -cE '^4\. \*\*'`; `git show <rev>:SCORECARD.md \| grep -c 'R67 correction '`; `git show <rev>:LOG.md \| grep -c 'Round 67 corrections'`; `python -I -X utf8 tools/quoted-line-exists.py --repo . --doc <rev>:LOG.md` (+ SCORECARD.md, round-66.md, round-67.md) | corrections commit `436b60c5`; base receipts at the same commit; tip sweeps at the receipts tip |
| R67-C2 | the liveness manifest grows 3 → 5 rows: `bind-erratum-range-red` (r65 vacuous-pass case, `7d7f9ca8..87e95597`) and `bind-own-range-red` (r66 own-range erratum, `469cde0f..5d969f4e`), instruments pinned at `5541abaf`, real-history inputs only; sourced on S298 | axis move + capability extension (the r66 manifest note's declared scope flip, executed; no checker blob change — rows are data) | operability (verdict-only axis: the rows pin standing red arms that must stay live) | at base `7362e15c`: `rows=3 live=3 dead=0` exit 0 (receipt `arm-live-standings-base-r67.txt`); manifest id-grep 3; the two red inputs verified at the pinned bytes (receipts `bind-erratum-range-r67.txt`: summary `commits=7 evidence=47 named=0 carried=0 spans=2 bare=8 findings=4` exit 1; `bind-own-range-r67.txt`: summary `commits=6 evidence=42 named=43 carried=22 spans=3 bare=47 findings=42` exit 1) | manifest id-grep 5; standing sweep `rows=5 live=5 dead=0` exit 0 with `ARM_LIVE bind-erratum-range-red tally=findings=4 exit=1` and `ARM_LIVE bind-own-range-red tally=findings=42 exit=1` (receipt `arm-live-standings-r67.txt`); checker selftest unchanged 4/4 | `python -I tools/arm-liveness.py --repo . --manifest tools/arm-liveness.json`; `grep -c '"id"' tools/arm-liveness.json`; `python -I tools/arm-liveness.py --selftest` | the C2 work commit (manifest + S298 row); receipts at the receipts tip |

The corrections commit carries only corrections and their receipts; the C2
work commit carries the manifest rows and the SOURCES row; neither needs
the other (causally separable). Receipts land per the receipt-after-subject
ordering; every commit message names only file tokens its tree carries; the
round ends with a self-sweep of the round range (forecast: `findings=0`
exit 0) and a carries-what-it-names diff-tree check of the tip before push.

## Round 67 — measured claims (appended at the receipts commit, 2026-11-02)

| Claim | Verdict | After (measured) | Counting commands (live outputs in the receipts) | Measured commit |
|---|---|---|---|---|
| R67-C1 | verifies (measured), the C1 tip-invariant sweeps land at the tip receipts commit as pinned | the four carry-in corrections landed append-only at `436b60c5` (after-greps receipt `corrections-after-greps.txt`: mistake-row-4 grep 1, SCORECARD correction markers 4, LOG corrections entry 1 — before 0/0/0 at the base, receipt `corrections-before-greps.txt`); the byte-backing invariant: base sweeps (`qline-red-log-base.txt` LOG totals `missing=40 skipped=40` with 8 absent; `qline-red-scorecard-base.txt` SCORECARD totals `missing=10 skipped=178` with 6 absent; `qline-red-round-66.txt` the round-66 lesson `missing=2 skipped=7` — its two missing quotes are the r66 pre-data forecast shapes, named in the lesson and left as written, append-only) vs the tip sweeps (receipts `qline-tip-log.txt`, `qline-tip-scorecard.txt` at the tip commit: the same missing and skipped counts with the same absent 8 and 6 — the round's own appends introduced zero unbacked quotes and zero absent path cites) and the round-67 lesson sweep reads zero missing, zero absent, exit 0 (`qline-green-round-67.txt`, tip commit); the instrument boundary measured and disclosed pre-data: the stale six-of-seven cells read backed via the r66 rehearsal receipt's preserved pre-correction bytes (`.ufo/evidence/round-66/win-host/rehearsal/reh-selftest-bind.txt`) — figure-misattribution is beyond byte-backing, named successor instrument work | `git show 436b60c5:corpus/lessons/round-66.md \| grep -cE '^4\. \*\*'`; `git show <rev>:SCORECARD.md \| grep -c 'R67 correction '`; `git show <rev>:LOG.md \| grep -c 'Round 67 corrections'`; `python -I -X utf8 tools/quoted-line-exists.py --repo . --doc <rev>:LOG.md` (+ SCORECARD.md, round-66.md, round-67.md) | corrections `436b60c5`; base receipts at the same commit; tip sweeps at the tip receipts commit |
| R67-C2 | verifies (measured) | manifest id-grep 3 → 5; the standing sweep reads `rows=5 live=5 dead=0` exit 0 (`arm-live-standings-r67.txt`: the three r66 rows live + `ARM_LIVE bind-erratum-range-red tally=findings=4 exit=1` and `ARM_LIVE bind-own-range-red tally=findings=42 exit=1`), instruments pinned at `5541abaf` (the corrected r66 checker bytes); the row receipts (`bind-erratum-range-r67.txt`, `bind-own-range-r67.txt`, landed at the corrections commit) carry the pinned summaries `commits=7 evidence=47 named=0 carried=0 spans=2 bare=8 findings=4` exit 1 and `commits=6 evidence=42 named=43 carried=22 spans=3 bare=47 findings=42` exit 1 — the own-range summary byte-identical to the r66 receipt `live-bind-own-range.txt`; the checker blob is unchanged (selftest `ARM_LIVENESS_SELFTEST: 4/4 pass` exit 0, receipt `arm-liveness-selftest-r67.txt`); sourced on S298 (registry 157 → 158) | `python -I tools/arm-liveness.py --repo . --manifest tools/arm-liveness.json`; `grep -c '"id"' tools/arm-liveness.json`; `python -I tools/arm-liveness.py --selftest`; `python -I <blob at 5541abaf> --repo . --base 7d7f9ca8… --tip 87e95597…`; `python -I <blob at 5541abaf> --repo . --base 469cde0f… --tip 5d969f4e…` | C2 work commit `ab67ddd6`; sweep and selftest receipts at the receipts commit |

Shared no-harm story (measured): the RED at the C2 work commit `ab67ddd6`
reads `COLDREAD_PRECHECK … lost=13 RED` exit 1 with cand_credited=51 — the
13 LOST heading lines equal in order to the r66 set (decoded comparison;
the r66 receipt is cp1252-encoded, this round's UTF-8 — the lesson's
mistake-2 fix; miss = 0; receipt `live-red-r67.out` with the probes reading
EQUIVALENCE 20/0 on both sides) — paid by the `r67-batch-1` rekey: REBIND
OK sections=13 entries_added=13 ledger_before=732 (receipt
`rebind-stdout-r67.txt`; ledger 732 → 745; machinery constants-only diff
`make-rebind-r67.diff`, 7 changed lines; traces section-01..13) →
`lost=0 ok` exit 0 at BOTH floors at the rekey commit `5f86b8e6` (receipt
`live-green-r67.out`: round floor `7362e15c` 64 → 64; receipt
`live-green-hist-r67.out`: historic `8b0042bd` 46 → 64) plus rev mode
credited=64/64 probe 20/20 (receipt `live-revmode-r67.out`); additivity
raw_old_only=0 on SOURCES (`7362e15c` → `ab67ddd6`,
`verbatim_prefix=false` disclosed — the mid-file row insertion; receipt
`additivity-sources-r67.txt`) and on the ledger (`ab67ddd6` → `5f86b8e6`,
`verbatim_prefix=false` disclosed — the mid-file entries-array insertion;
receipt `additivity-ledger-r67.txt`), the LOG and SCORECARD pairs at the
tip receipts commit (`additivity-logscorecard-r67.txt`); selftests bind
7/7 (receipt `bind-selftest-r67.txt`) and quoted-line 4/4 (receipt
`qline-selftest-r67.txt`); the corrections-commit range sweep reads
`commits=1 evidence=4 named=4 carried=4` findings zero exit 0 (receipt
`self-sweep-k1-r67.txt`). Tip receipts pinned here pre-data (they land at
the tip receipts commit): the tip guards at both floors + rev
(`live-tip-guard-r67.txt`, `live-tip-guard-hist-r67.txt`,
`live-tip-revmode-r67.txt` — lost=0 ok / 46 → 64 / credited=64/64), the
tip invariant sweeps (`qline-tip-log.txt`, `qline-tip-scorecard.txt`,
`qline-green-round-67.txt`), the LOG/SCORECARD additivity pair
(`additivity-logscorecard-r67.txt`), the round-range self-sweep
(`tip-self-sweep-r67.txt` — forecast findings zero exit 0), and the census
end receipts (`census-end-r67.txt` at the fleet root, exit 0;
`census-end-lanetip-r67.txt` at the lane-tip-shaped fleet root, 158 rows).
No owned axis harmed: depth 10, freshness 9, calibration 8 unchanged (no
depth or freshness surface touched — PROVINCE.md, SKILL.md, README.md,
corpus/QUALITY.md, tools/registry.json, SHONEN.md,
tools/mutate-and-run.sh and the guarded probe
`tools/coldread-precheck-portable.py` (worktree sha256 `892a045d…`)
blob-identical base → tip; `git diff-tree -r --name-status 7362e15c
<tip> -- PROVINCE.md SKILL.md README.md corpus/QUALITY.md
tools/registry.json SHONEN.md tools/mutate-and-run.sh
tools/coldread-precheck-portable.py` is empty and corpus/SOURCES.md is the
only monitored file in the round's diffs, rekeyed).

**R67-C1 tip-count erratum (appended at the tip receipts commit, measured,
not re-scoped — the r66 own-range precedent).** The measured rows above
pinned the tip-invariant forecast ("the same missing and skipped counts
with the same absent 8 and 6"). Measured at the tip: the absent counts
hold EXACTLY (LOG 8, SCORECARD 6); the missing counts do not hold raw —
LOG 40 → 5, SCORECARD 10 → 0 — because this round's landed base-sweep
receipts (`qline-red-log-base.txt`, `qline-red-scorecard-base.txt`)
themselves quote the base MISSING lines, so the previously-missing quotes
became byte-backed by the record of their own missingness (quotes of 72
chars or less; the 5 remaining LOG missing are the >72-char truncation
escapes). The substantive invariant HOLDS, measured: tip-missing ⊆
base-missing and every quote added this round is backed (LOG 109 → 114
quotes with 69 → 109 backed; SCORECARD 326 → 337 quotes with 316 → 337
backed) — the round's own appends introduced zero unbacked quotes and
zero absent path cites; the round-67 lesson sweeps clean (receipt
`qline-green-round-67.txt`: 16 quotes, 16 backed, missing 0, exit 0).
Tip receipts at this commit: `qline-tip-log.txt`, `qline-tip-scorecard.txt`,
`additivity-logscorecard-r67.txt` (LOG and SCORECARD pairs raw_old_only=0,
verbatim_prefix=true — pure appends), `tip-self-sweep-r67.txt`
(`commits=5 evidence=44 named=23 carried=23 spans=1 bare=25 findings=0`
exit 0 — every round-67 commit message names only file tokens its tree
carries), `live-tip-guard-r67.out` (lost=0 ok, 64 → 64),
`live-tip-guard-hist-r67.out` (lost=0 ok, 46 → 64),
`live-tip-revmode-r67.out` (credited=64/64, probe 20/20),
`census-end-r67.txt` (fleet root, exit 0), `census-end-lanetip-r67.txt`
(the lane-tip-shaped fleet root, 158 rows, exit 0). Successor sweep work
(lesson mistake 4): a self-referential-backing exclusion.


## Planned — round 68 (declared 2026-11-02, frozen before data)

The r67 closure (non-author verifier spot-check, `859a736d` = the commit
that landed it) ADMITTED round 67 clean: no routed defects; the
machinery-diff figure note ("7 changed lines" vs the receipt's 6 changed
pairs) was ruled constants-only substance, verified — no action. The
round's claims, declared frozen:

- **C1 (calibration, the lowest scored numeric axis at 8; capability
  acquisition; adopts considerthese 2026-10-28 proposal 1's semantic
  half — the figure-attribution instrument the r67 lesson named as the
  successor calibration instrument, designed against the r59
  cheat-family ruling).** `tools/figure-attribution.py` +
  `tools/figure-attribution.json` (new; schema
  `tameshi-figure-attribution-v1`): a record figure pinned to ONE named
  receipt must be a byte substring of BOTH the record's committed bytes
  and that receipt's committed bytes, both read from git objects at
  pinned revisions (never a worktree); rows declare `expect`
  attributed|misattributed so the standing red arm MEASURES
  misattributed on every sweep; unresolvable inputs are setup exit 2
  before any row effect; a zero-row manifest is refused exit 2. The
  anywhere-in-cited-set relaxation is the cheat family it refuses by
  construction, demonstrated on a committed control. Capability row
  `figure-attribution check` enters the table.
- **C2 (operability, verdict-only; sourced on new row S299, opened this
  round — Python shutil documentation).** The arm-liveness checker
  gains the per-row scratch slot the r67 lesson named as the
  precondition (args literal `{work}` → a fresh mkdtemp directory per
  row, deleted with the run together with the instrument extraction
  directory via `shutil.rmtree(..., ignore_errors=True)`; S279 is
  mkdtemp's caller-deletion duty, S299 the rmtree contract); selftest
  4/4 → 5/5 (arm 5: the tally moves ONLY when the slot supplied the
  directory); the manifest grows 5 → 6 rows with the no-harm guard's
  RED arm — the last manifestable receipt-family arm without a
  committed input — pinned at the guarded probe bytes over the
  committed r67 pair; the capability row is synced append-only (the
  r67 correction-4 precedent; old → new logged in the lesson).
- Shared no-harm forecast: the SOURCES edit (one row + one tail note,
  the r67 edit shape) is the round's only monitored-file change; the
  live RED at the C2 work commit is forecast at `lost=13 RED` with
  `cand_credited=51` — the SAME 13 headings as the r67 measured RED and
  this round's rehearsal (decoded comparison `reh-red-decode-r68.txt`:
  equal in order, miss = 0), paid by the `r68-batch-1` rekey (13 fresh
  input-keyed entries; ledger 745 → 758) restoring `lost=0 ok` exit 0
  at both floors plus rev mode 64/64 probe 20/20 (receipts
  `live-green-r68.out`, `live-green-hist-r68.out`,
  `live-revmode-r68.out`, `rebind-stdout-r68.txt`,
  `figattn-selftest-r68.txt`, `arm-liveness-selftest-r68.txt`).

| # | Claim | The move | Axis / claim type | Before | After (expected) | Counting command | Measured commit |
|---|---|---|---|---|---|---|---|
| R68-C1 | `tools/figure-attribution.py` + `tools/figure-attribution.json` (new): a record figure pinned to ONE named receipt must be a byte substring of BOTH the record's committed bytes and that receipt's committed bytes at pinned revisions; rows carry expect attributed or misattributed so the standing red arm measures its verdict every sweep; fail-closed setup exit 2, vacuous-manifest exit 2; standing manifest = 3 real-history rows at `859a736d` (the r66 stale selftest figure — the SCORECARD cells' figure vs the live receipt reading 7/7 — expect misattributed; the same figure vs its true carrier the preserved rehearsal receipt — expect attributed; the R67-correction figure vs the live receipt — expect attributed); the cheat family (anywhere-in-cited-set matching) demonstrated on a committed control that passes the exact red pair; capability row enters the table; adopts considerthese 2026-10-28 proposal 1's semantic half | axis move + capability (the r67 named boundary, executed; two new files only — no checker blob changes) | calibration (numeric score 8 unchanged, at the lane-attainable cap; the move is record-attribution honesty: the figure-misattribution class becomes a standing measured red arm instead of an inspection finding) | at base `859a736d`: `git ls-tree 859a736d tools/ \| grep -c figure-attribution` → 0 (no instrument exists; the r66 stale cells were caught by a human, R67 correction 1, not by any standing check); the scratch set-matcher passes the red pair — `CHEAT_ANYWHERE: found=1 cited=2 (set-matcher: pass=true)` (rehearsal receipt `reh-figattn-cheat.txt`) | selftest `FIGURE_ATTRIBUTION_SELFTEST: 7/7 pass` exit 0 (rehearsed pre-data, `reh-figattn-selftest.txt`; live receipt `figattn-selftest-r68.txt`); standing sweep `FIGURE_ATTRIBUTION: rows=3 met=3 unexpected=0` exit 0 with the red row reading expect=misattributed measured=misattributed ok (rehearsed, `reh-figattn-standings.txt`; live receipt `figattn-standings-r68.txt`); the control receipt lands under `controls/` beside the instrument verdict on the same pair; capability-row grep 0 → 1 | `python -I -X utf8 tools/figure-attribution.py --selftest`; `python -I -X utf8 tools/figure-attribution.py --repo . --manifest tools/figure-attribution.json`; `git show <rev>:SCORECARD.md \| grep -c figure-attribution check` | the C1 work commit (declared work); receipts land in the following commit(s) |
| R68-C2 | `tools/arm-liveness.py` gains the per-row scratch slot the r67 lesson named as the precondition: args literal `{work}` → a fresh `tempfile.mkdtemp` directory per row, deleted with the run together with the instrument extraction directory (which earlier rounds leaked on disk) via `shutil.rmtree(..., ignore_errors=True)` in a finally; selftest 4/4 → 5/5 (arm 5: a toy-work instrument whose tally moves only when the slot supplied the directory — the slot itself under test); `tools/arm-liveness.json` grows 5 → 6 rows: `precheck-sources-red` — the no-harm guard's RED arm — pins `tools/coldread-precheck-portable.py` at `859a736d` (blob sha256 `892a045d…`, the guarded digest) over the committed pair floor `7362e15c` / cand `ab67ddd6`, tally lost expect ≥13 baseline 0 exit 1 (the r67 receipt `live-red-r67.out` is the pinned record); capability row synced append-only (selftest figure 4/4 → 5/5 and rows 3 → 6 at the r68 bytes, old → new in the lesson); sourced on new row S299 (Python shutil documentation), opened this round | axis move (closes the r67 lesson's priced-out item (f): the RED arm is manifestable only with a scratch slot) | operability (verdict-only axis: the checker change runs on this host, its grown selftest passes, and the standing manifest now re-executes every manifestable receipt-family red arm including the no-harm guard's, on committed bytes at pinned revisions) | at base `859a736d`: checker selftest `ARM_LIVENESS_SELFTEST: 4/4 pass` (the r66 receipt `live-selftest-liveness.txt`); manifest id-grep 5; no `{work}` literal in the checker bytes (no slot exists — the r67 lesson priced the precheck RED arm out for exactly this reason); the base 5-row sweep reads live at the r67 checker bytes (receipt `arm-live-standings-base-r68.txt`) | selftest `ARM_LIVENESS_SELFTEST: 5/5 pass` exit 0 (rehearsed, `reh-liveness-selftest.txt`; live receipt `arm-liveness-selftest-r68.txt`); standing sweep `ARM_LIVENESS: rows=6 live=6 dead=0` exit 0 with `ARM_LIVE precheck-sources-red tally=lost=13 exit=1` (rehearsed, `reh-liveness-standings.txt`; live receipt `arm-live-standings-r68.txt`; the row costs ~3 min on this host — the precheck's two monitor passes — recorded as cost profile in the lesson); manifest id-grep 5 → 6; S299 grep 0 → 1; registry rows 158 → 159 | `python -I tools/arm-liveness.py --selftest`; `python -I tools/arm-liveness.py --repo . --manifest tools/arm-liveness.json`; `grep -c '"id"' tools/arm-liveness.json`; `git show <rev>:corpus/SOURCES.md \| grep -cE '^\| S299 '`; the `COLDREAD_PRECHECK` lines | the C2 work commit (checker + manifest + S299 row); receipts land in the following commit(s) |

The C1 work commit carries only the two new files; the C2 work commit
carries the checker, the manifest and the SOURCES row; neither needs
the other (causally separable). Receipts land per the
receipt-after-subject ordering; every commit message names only file
tokens its tree carries; the round ends with a self-sweep of the round
range (forecast: `findings=0` exit 0) and a carries-what-it-names
diff-tree check of the tip before push.


## Round 68 — measured claims (appended at the receipts commit, 2026-11-02)

Declaration `c60d862277e4bf68d7fdbcd81d410c62e511ed5a` (planned block +
lesson + LOG declared entry + S299 extract + census receipt + rehearsal
receipts); work commits C1 `1a063d5f8e2f2b8fa6131bd1a28167c3a81a6871`
(the figure-attribution tool + manifest) and C2
`dcd10cc5f09cf0857ff8deab523992df37b0a284` (arm-liveness work slot +
manifest row + SOURCES S299 + tail note); rekey
`f694df16d74b03b3556cc4fcadc7107523781f42` (the live RED paid: 13 fresh
input-keyed entries as `r68-batch-1`, ledger 745 → 758, monitor restored
at both floors). Receipts commit: this one.

| Claim | Verdict | After (measured) | Counting commands (live outputs in the receipts) | Measured commit |
|---|---|---|---|---|
| R68-C1 | verifies (measured) | selftest `FIGURE_ATTRIBUTION_SELFTEST: 7/7 pass` exit 0 (`figattn-selftest-r68.txt`; rehearsed pre-data at `reh-figattn-selftest.txt`); the standing sweep `FIGURE_ATTRIBUTION: rows=3 met=3 unexpected=0` exit 0 (`figattn-standings-r68.txt`) with the red arm measured, not assumed: `FIGURE_ROW r66-stale-selftest-figure-red expect=misattributed measured=misattributed ok` (the r66 stale cells are a standing measured red arm from this round on); the cheat control `CHEAT_ANYWHERE: found=1 cited=2 (set-matcher: pass=true)` beside the instrument's named-receipt verdict on the same pair (`controls/cheat-anywhere-passes-red.txt`, the set-matcher script landed as `controls/cheat-anywhere.py`) — the anywhere-in-cited-set relaxation demonstrably cannot replace the named-receipt binding; capability-row grep 0 → 1 | `python -I -X utf8 tools/figure-attribution.py --selftest`; `python -I -X utf8 tools/figure-attribution.py --repo . --manifest tools/figure-attribution.json`; `git show <rev>:SCORECARD.md \| grep -c 'figure-attribution check'` | C1 commit `1a063d5f…`; receipts at the receipts commit |
| R68-C2 | verifies (measured) | selftest `ARM_LIVENESS_SELFTEST: 5/5 pass` exit 0 (`arm-liveness-selftest-r68.txt`; arm 5 is the work slot: the toy-work tally moves only when the slot supplied the directory); manifest id-grep 5 → 6; the standing sweep `ARM_LIVENESS: rows=6 live=6 dead=0` exit 0 (`arm-live-standings-r68.txt`) with `ARM_LIVE precheck-sources-red tally=lost=13 exit=1` — the no-harm guard's RED arm re-executed on every sweep at the guarded probe bytes (sha256 `892a045d…` pinned at `859a736d`) over the committed r67 pair floor `7362e15c` / cand `ab67ddd6`; the base 5-row sweep at the frozen r67 checker bytes reads live (`arm-live-standings-base-r68.txt`); unchanged checkers receipted: bind `RECEIPT_COMMIT_BIND_SELFTEST: 7/7 pass` (`bind-selftest-r68.txt`), quoted-line `QUOTED_LINE_EXISTS_SELFTEST: 4/4 pass` (`qline-selftest-r68.txt`); S299 grep 0 → 1; registry rows 158 → 159 | `python -I tools/arm-liveness.py --selftest`; `python -I tools/arm-liveness.py --repo . --manifest tools/arm-liveness.json`; `grep -c '"id"' tools/arm-liveness.json`; `git show <rev>:corpus/SOURCES.md \| grep -cE '^\| S299 '`; the `COLDREAD_PRECHECK` lines | C2 commit `dcd10cc5…`; receipts at the receipts commit |

Capability row entered (see `## Capabilities`): **figure-attribution
check** — first working round 68 (the mid-file insertion is disclosed;
additivity `raw_old_only=0` on the file holds).

**Arm-liveness capability-row sync (append-only; the r67 correction-4
precedent).** The `counter-arm liveness check` row (round 66) carries
the r66-era figures — selftest 4/4, standing manifest `rows=3 live=3
dead=0` — true at the r66 bytes and unchanged there; at the round-68
checker bytes the same instruments read selftest 5/5 and the manifest
`rows=6 live=6 dead=0` with the precheck RED arm live
(`arm-liveness-selftest-r68.txt`, `arm-live-standings-r68.txt`). Old →
new logged in the round-68 lesson; the row above is not edited in place
under the additivity discipline.

Shared no-harm story (measured): the RED at the C2 work commit
`dcd10cc5` reads `COLDREAD_PRECHECK floor=859a736deb1e floor_credited=64
cand=dcd10cc5f09c cand_credited=51 lost=13 RED` exit 1 (receipt
`live-red-r68.out` with the JSON receipt `red-receipt-r68.json`; the 13
LOST heading lines decode byte-equal in order to the r67 measured set
and to this round's rehearsal — miss = 0; receipts `red-decode-r68.txt`
and `reh-red-decode-r68.txt`, each side decoded by its own encoding) —
paid by the `r68-batch-1` rekey: `REBIND OK sections=13 entries_added=13
ledger_before=745` (`rebind-stdout-r68.txt`; ledger 745 → 758; machinery
constants-only diff `make-rebind-r68.diff`, 6 changed pairs, every
changed line constants-only: round number, batch id, trace path,
carried_from) → `lost=0 ok` exit 0 at BOTH floors at the rekey commit
`f694df16` (receipt `live-green-r68.out`: round floor `859a736d` 64 →
64; receipt `live-green-hist-r68.out`: historic `8b0042bd` 46 → 64) plus
rev mode credited=64/64 probe 20/20 (receipt `live-revmode-r68.out`);
additivity `raw_old_only=0` on SOURCES (`859a736d` → `dcd10cc5`,
`verbatim_prefix=false` disclosed — the mid-file row insertion + tail
note; receipt `additivity-sources-r68.txt`) and on the ledger
(`dcd10cc5` → `f694df16`, `verbatim_prefix=false` disclosed — the
mid-file entries-array insertion; receipt `additivity-ledger-r68.txt`),
the LOG/SCORECARD pairs at the tip receipts commit
(`additivity-logscorecard-r68.txt`); no owned axis harmed: depth 10,
freshness 9, calibration 8 unchanged (no depth or freshness surface
touched — PROVINCE.md, SKILL.md, README.md, corpus/QUALITY.md,
tools/registry.json, SHONEN.md, tools/mutate-and-run.sh and the guarded
probe `tools/coldread-precheck-portable.py` (blob sha256 `892a045d…`)
blob-identical base → tip; `git diff-tree -r --name-status 859a736d
<tip> -- PROVINCE.md SKILL.md README.md corpus/QUALITY.md
tools/registry.json SHONEN.md tools/mutate-and-run.sh
tools/coldread-precheck-portable.py` is empty and corpus/SOURCES.md is
the only monitored file in the round's diffs, rekeyed).

Tip receipts pinned here pre-data (they land at the tip receipts
commit): the tip guards at both floors + rev (`live-tip-guard-r68.out`,
`live-tip-guard-hist-r68.out`, `live-tip-revmode-r68.out`), the tip
invariant sweeps (`qline-tip-log.txt`, `qline-tip-scorecard.txt`,
`qline-green-round-68.txt`), the LOG/SCORECARD additivity pair
(`additivity-logscorecard-r68.txt`), the round-range self-sweep
(`tip-self-sweep-r68.txt` — forecast `findings=0` exit 0), and the
census end receipts (`census-end-r68.txt` at the fleet root, exit 0;
`census-end-lanetip-r68.txt` at the lane-tip-shaped fleet root, 159
rows).

## Round-69 corrections — the r68 closure's two routed record defects (declared 2026-11-02, appended at the declaration commit; status-neutral, append-only: the stale cells above are preserved and stay flagged by the standing quoted-line sweep)

1. **Capability-row counting command** (r68 spot-check routed defect 1): the R68-C1 counting command as printed — the unanchored `git show <rev>:SCORECARD.md | grep -c 'figure-attribution check'` — reads 4 at both the r67 tip and the r68 tip (the claim, verdict and plan rows carry the phrase), so it cannot measure the capability row's entry. The command of record is the anchored form `git show <rev>:SCORECARD.md | grep -cE '^\| figure-attribution check'` — measured 0 at the r67 tip `859a736d` → 1 at the r68 tip `434a96e4` (= this round's base; both re-measured at the r69 declaration). Every counting command this round prints is an anchored form; the r69 capability-row command below cites its anchored form.
2. **S299 anchor naming drift** (r68 spot-check routed defect 2): the S299 anchor cell names the section "Directory deletion operations"; the page's — snapshot and live agree — section heading is "Directory and files operations". The correction of record: `corpus/lessons/round-69.md` (the carry-in section), the round-69 SOURCES tail note (the next note touching S299), and the anchor-drift sweep's standing manifest — the drift carried as a measured red arm (s299-anchor-as-written, expect=absent) beside the true heading (s299-anchor-as-on-page, expect=present) on the same pinned snapshot. Rows are append-only; the anchor cell is not edited in place.

## Planned — round 69 (declared 2026-11-02, frozen before data)

The r68 closure (non-author verifier spot-check, `434a96e4` = the commit
that landed it) ADMITTED round 68 clean: no routed defects barred
admission; two status-neutral record defects routed to this round and are
corrected above and in the LOG. The round's claims, declared frozen:

- **C1 (calibration, the lowest scored numeric axis at 8; the r67 lesson
  mistake 4's named successor work — the self-referential-backing
  exclusion, executed).** `tools/quoted-line-exists.py` v2: the backing
  scans (doc sweep and explicit receipt/quote mode) remove each cited
  receipt's miss-record lines — the checker's own QUOTE MISSING output
  lines, which print the missing span bytes — before the substring test;
  a receipt that quotes a verdict line inside its own miss record is the
  record of a miss, not backing for the figure. Selftest 4/4 → 5/5
  (arm 5 the selfref red: a quote carried ONLY by a miss-record line
  reads MISSING exit 1 while its genuinely-carried sibling stays backed
  — the exclusion is the thing under test). The rehearsal carrier diff
  pins the mechanism: totals byte-identical at both recorded tips, 46
  false-carrier attributions re-pointed, and the r67 erratum's
  miss-record-carrier narrative corrected by measurement (no standing
  quote was ever solely miss-record-backed).
- **C2 (operability, verdict-only; capability acquisition; sourced on
  new row S300, opened this round — Python html.parser documentation).**
  `tools/anchor-drift-sweep.py` + `tools/anchor-drift-sweep.json` (new;
  schema `tameshi-anchor-drift-v1`): a held row's anchor heading must
  still be the heading the row's own pinned snapshot carries; an
  expect=absent row MEASURES the drift on every sweep; fail-closed setup
  exit 2, zero-row manifest refused exit 2; headings parsed through an
  html.parser.HTMLParser subclass (S300). Standing manifest: four rows —
  the r68 routed defect as the measured red arm (S299's cell heading vs
  its own pinned snapshot, expect absent), the true heading green, the
  page h1 green, and S300's own class heading green. Capability row
  `anchor-drift sweep` enters the table.
- Shared no-harm forecast: the SOURCES edit (one row + one tail note,
  the r67/r68 edit shape) is the round's only monitored-file change; the
  live RED at the C2 SOURCES work commit is forecast at lost=13 with
  cand_credited=51 — the SAME 13 headings as the r68 measured set and
  this round's rehearsal (decoded comparison `reh-red-decode-r69.txt`:
  equal in order, miss = 0), paid by the `r69-batch-1` rekey (13 fresh
  input-keyed entries; ledger 758 → 771) restoring lost=0 ok exit 0 at
  both floors plus rev mode 64/64 probe 20/20 (receipts
  `live-green-r69.out`, `live-green-hist-r69.out`, `live-revmode-r69.out`,
  `rebind-stdout-r69.txt`, `qline-selftest-r69.txt`,
  `anchor-selftest-r69.txt`).

| # | Claim | The move | Axis / claim type | Before | After (expected) | Counting command | Measured commit |
|---|---|---|---|---|---|---|---|
| R69-C1 | `tools/quoted-line-exists.py` v2 — the self-referential-backing exclusion: backing scans remove each cited receipt's miss-record lines (the checker's own QUOTE MISSING output lines, which print the missing span bytes) before the substring test, in both the doc sweep and the explicit receipt/quote mode; a receipt that quotes a verdict line inside its own miss record is the record of a miss, not backing for the figure (r67 lesson mistake 4's named successor); selftest 4/4 → 5/5, arm 5 the selfref red (a quote carried ONLY by a miss-record line reads MISSING exit 1 while its genuinely-carried sibling stays backed); the rehearsal carrier diff measured the mechanism before the declaration: totals byte-identical at both recorded tips (missing 5/0; backed 114/346 and 109/338) with 46 first-backing-receipt attributions re-pointed (35 LOG + 11 SCORECARD at the r68 tip, the same at the r67 tip) — and the r67 erratum's miss-record-carrier narrative corrected by measurement: no standing quote was ever solely miss-record-backed, the movement rode non-miss-record carriers | axis move (closes the r67 lesson's named successor work; one checker blob only — no monitored file, no manifest change: measured, no real-history tally-moving input exists for a manifest row, and manufacturing one would be synthetic, the r59 ruling) | calibration (numeric score 8 unchanged, at the lane-attainable cap; the move is record-honesty: the checker no longer attributes backing to a receipt that merely records the quote's absence, and the standing backing set is audited against the class — zero verdicts move) | at base `434a96e4`: `git show 434a96e4:tools/quoted-line-exists.py \| grep -c MISS_RECORD_LINE` → 0 (no exclusion exists); selftest 4/4 at the frozen bytes (`qline-selftest-r68.txt`); at the frozen bytes the r68-tip LOG sweep names a miss-record-only carrier for 35 of its 114 backed quotes and the SCORECARD sweep for 11 of its 346 (receipts `reh-qline-log-old.txt`, `reh-qline-sc-old.txt`; the r67-tip pair the same, `reh-qline-log-old-r67.txt`, `reh-qline-sc-old-r67.txt`) | selftest `QUOTED_LINE_EXISTS_SELFTEST: 5/5 pass` exit 0 (rehearsed pre-data, `reh-qline-selftest.txt`; live receipt `qline-selftest-r69.txt`); the four standing pairs re-swept at the exclusion bytes: totals byte-identical, 46 carriers re-pointed (receipt `qline-carrier-r69.txt`, the live twin of `reh-qline-carrier-diff.txt`); standing tip sweeps LOG missing=5 / SCORECARD missing=0 at the r69 bytes (`qline-tip-log-r69.txt`, `qline-tip-scorecard-r69.txt`); capability-row sync note appended (r65 figures stand at the r65 bytes; old → new in the lesson) | `python -I -X utf8 tools/quoted-line-exists.py --selftest`; `python -I -X utf8 tools/quoted-line-exists.py --repo . --doc <rev>:LOG.md`; `git show <rev>:tools/quoted-line-exists.py \| grep -c MISS_RECORD_LINE` | the C1 work commit (checker only); receipts land in the following commit(s) |
| R69-C2 | `tools/anchor-drift-sweep.py` + `tools/anchor-drift-sweep.json` (new; schema `tameshi-anchor-drift-v1`): a held row's anchor heading must still be the heading the row's own pinned snapshot carries — a manifest row pins (snapshot path at a revision, the exact heading string the anchor cell names, expect present or absent); the snapshot blob is read from git objects (never a worktree); h1-h6 texts parsed through an html.parser.HTMLParser subclass (S300: the handler contract on start tags, end tags, text and other markup; convert_charrefs decodes entities), whitespace-normalized with the trailing paragraph mark dropped; a row verifies only when measured presence matches expectation, so an expect=absent row MEASURES the drift on every sweep; unresolvable snapshots setup exit 2 before any row effect, zero-row manifest refused exit 2; standing manifest 4 rows — the r68 routed defect as the measured red arm (s299-anchor-as-written: the cell heading "Directory deletion operations" vs the row's own pinned r68 snapshot, expect absent), the true heading green (s299-anchor-as-on-page), the page h1 green (s299-page-h1), S300's class heading green (s300-class-heading, pinned at the declaration revision); capability row enters the table; sourced on new row S300 (Python html.parser documentation), opened this round | axis move + capability (the r68 closure's routed defect 2 becomes a standing measured red arm; two new files + the SOURCES row only — no checker blob changes) | operability (verdict-only axis: the new instrument runs on this host, its selftest passes, and the standing sweep re-measures the anchor-drift class — the freshness score is NOT touched: the r45 counter stays operator-priced future work, the r68 pricing stands) | at base `434a96e4`: `git ls-tree 434a96e4 tools/ \| grep -c anchor-drift` → 0 (no instrument; the drift was caught by the non-author closure reading the page, not by any standing check); the drift measurable pre-instrument: the cell's heading occurs 0 times in the pinned snapshot bytes, the page's heading occurs 3 times (grep -cF on the S299 snapshot); S300 anchored grep 0; registry rows 159 | selftest `ANCHOR_DRIFT_SELFTEST: 5/5 pass` exit 0 (rehearsed, `reh-anchor-selftest.txt`; live receipt `anchor-selftest-r69.txt`); standing sweep `ANCHOR_DRIFT: rows=4 met=4 unexpected=0` exit 0 with the red row expect=absent measured=absent ok (rehearsed 3 rows pre-data at the base revision, `reh-anchor-standings.txt`; live receipt `anchor-standings-r69.txt`); manifest id-grep → 4; S300 grep 0 → 1; registry rows 159 → 160; capability-row anchored grep 0 → 1 | `python -I -X utf8 tools/anchor-drift-sweep.py --selftest`; `python -I -X utf8 tools/anchor-drift-sweep.py --repo . --manifest tools/anchor-drift-sweep.json`; `grep -c '"id"' tools/anchor-drift-sweep.json`; `git show <rev>:corpus/SOURCES.md \| grep -cE '^\| S300 '`; `git show <rev>:SCORECARD.md \| grep -cE '^\| anchor-drift sweep'` | the C2 work commits (SOURCES first — the RED is measured there; tool + manifest follow); receipts land in the following commit(s) |

The C1 work commit carries only the checker; the C2 SOURCES work commit
carries only corpus/SOURCES.md; the C2 tool work commit carries the two
new files; neither claim needs the other (causally separable). Receipts
land per the receipt-after-subject ordering; every commit message names
only file tokens its tree carries; the round ends with a self-sweep of
the round range (forecast: findings=0 exit 0) and a carries-what-it-names
diff-tree check of the tip before push.

## Round 69 — measured claims (appended at the receipts commit, 2026-11-02)

Declaration `5eb09e849568f493996df359fb40dea54a80cbd6` (corrections
paragraph + planned block + lesson + LOG declared entry + S300 extract +
census receipt + rehearsal receipts); work commits C1
`baa63c452713c21762c21f092eea0a2e40930468` (the quoted-line
self-referential-backing exclusion), C2 SOURCES
`cf5570d37837c5eff16cc9013c07e58879e6f376` (row S300 + the round-69 tail
note — the RED measured here), C2 tool
`d958326ea469d7b598ddc983283688a4580d4842` (the anchor-drift sweep +
manifest); rekey `b59ca7fe63522f8c91865d31089e8d4d622117fb` (the live RED
paid: 13 fresh input-keyed entries as `r69-batch-1`, ledger 758 → 771,
monitor restored at both floors). Receipts commit: this one.

| Claim | Verdict | After (measured) | Counting commands (live outputs in the receipts) | Measured commit |
|---|---|---|---|---|
| R69-C1 | verifies (measured) | selftest `QUOTED_LINE_EXISTS_SELFTEST: 5/5 pass` exit 0 (`qline-selftest-r69.txt`; arm 5 the selfref red; rehearsed pre-data, `reh-qline-selftest.txt`); the four standing pairs re-swept at the exclusion bytes — totals byte-identical to the frozen receipts (missing 5/0 at the r68 tip, 5/0 at the r67 tip; backed 114/346 and 109/338) with the 46 false-carrier attributions re-pointed: 35 LOG + 11 SCORECARD at the r68 tip, the same at the r67 tip (`qline-carrier-r69.txt`; rehearsed pre-data, `reh-qline-carrier-diff.txt`) — the frozen checker named a receipt that merely records the quote's absence as the backing carrier for exactly those 46 quotes, and the r67 erratum's carrier narrative is corrected by measurement: no standing quote was ever solely miss-record-backed; unchanged standing instruments receipted at the r69 bytes: bind 7/7 (`bind-selftest-r69.txt`), receipt-exists 4/4 (`rexists-selftest-r69.txt`), figure-attribution 7/7 and rows=3 met=3 (`figattn-selftest-r69.txt`, `figattn-standings-r69.txt`), arm-liveness 5/5 and rows=6 live=6 dead=0 (`arm-liveness-selftest-r69.txt`, `arm-live-standings-r69.txt`) | `python -I -X utf8 tools/quoted-line-exists.py --selftest`; `python -I -X utf8 tools/quoted-line-exists.py --repo . --doc <rev>:LOG.md`; `git show <rev>:tools/quoted-line-exists.py \| grep -c MISS_RECORD_LINE` → 2 at the tip (the constant + the helper definition; anchored form) and `grep -c strip_miss_records` → 3 (helper + the two call sites) | C1 commit `baa63c45…`; receipts at the receipts commit |
| R69-C2 | verifies (measured) | selftest `ANCHOR_DRIFT_SELFTEST: 5/5 pass` exit 0 (`anchor-selftest-r69.txt`; rehearsed, `reh-anchor-selftest.txt`); the standing sweep `ANCHOR_DRIFT: rows=4 met=4 unexpected=0` exit 0 with the red arm measured, not assumed: `ANCHOR_ROW s299-anchor-as-written expect=absent measured=absent ok` — the r68 closure's routed defect standing as a measured red arm, beside the true heading (expect=present measured=present), the page h1, and S300's own class heading on their pinned snapshots (`anchor-standings-r69.txt`; rehearsed 3 rows pre-data at the base revision, `reh-anchor-standings.txt`); manifest id-grep 4; the drift measurable pre-instrument: the cell's heading occurs 0 times in the pinned snapshot bytes, the page's heading 3 times; S300 grep 0 → 1; registry rows 159 → 160 | `python -I -X utf8 tools/anchor-drift-sweep.py --selftest`; `python -I -X utf8 tools/anchor-drift-sweep.py --repo . --manifest tools/anchor-drift-sweep.json`; `grep -c '"id"' tools/anchor-drift-sweep.json` → 4; `git show <rev>:corpus/SOURCES.md \| grep -cE '^\| S300 '` | the C2 work commits `cf5570d3…` (SOURCES — the RED measured there) + `d958326e…` (tool + manifest); receipts at the receipts commit |

Capability row entered (see `## Capabilities`): **anchor-drift sweep** —
first working round 69 (the mid-file insertion is disclosed; additivity
raw_old_only=0 on the file holds).

**Quoted-line capability-row sync (append-only; the r67 correction-4
precedent).** The `quoted-line receipt backability` row (round 65) carries
the r65-era figures — selftest 4/4, the demo sweep at the r65 bytes — true
at those bytes and unchanged there; at the round-69 checker bytes the same
instrument reads selftest 5/5 with arm 5 the selfref red
(`qline-selftest-r69.txt`) and the exclusion in its backing scans. Old →
new logged in the round-69 lesson; the row above is not edited in place
under the additivity discipline.

Shared no-harm story (measured): the RED at the C2 SOURCES work commit
`cf5570d3` reads `COLDREAD_PRECHECK floor=434a96e47d08 floor_credited=64
cand=cf5570d37837 cand_credited=51 lost=13 RED` exit 1 (receipt
`live-red-r69.out` with the JSON receipt `red-receipt-r69.json`; the 13
LOST heading lines decode byte-equal in order to the r68 measured set AND
to this round's rehearsal — miss = 0; receipt `red-decode-r69.txt` with
the rehearsal twin `reh-red-decode-r69.txt`, both sides utf-8 per the
codec discipline) — paid by the `r69-batch-1` rekey: REBIND OK
sections=13 entries_added=13 ledger_before=758 (receipt
`rebind-stdout-r69.txt`; ledger 758 → 771; machinery constants-only diff
`make-rebind-r69.diff`, 10 changed pairs, every changed line
constants-only: docstring round, trace path, batch id, carried_from,
plus the batch and rekey_batch fields the r67/r68 as-run shape carries —
disclosed) → lost=0 ok exit 0 at BOTH floors at the rekey commit
`b59ca7fe` (receipt `live-green-r69.out`: round floor `434a96e4` 64 → 64;
receipt `live-green-hist-r69.out`: historic `8b0042bd` 46 → 64) plus rev
mode credited=64/64 probe 20/20 (receipt `live-revmode-r69.out`);
additivity raw_old_only=0 on SOURCES (`434a96e4` → `cf5570d3`, 2 new
lines disclosed — the mid-file row insertion + tail note,
verbatim_prefix=false; receipt `additivity-sources-r69.txt`) and on the
ledger (`cf5570d3` → `b59ca7fe`, 29 new lines disclosed — the mid-file
entries-array insertion; receipt `additivity-ledger-r69.txt`); no owned
axis harmed: depth 10, freshness 9, calibration 8 unchanged (no depth or
freshness surface touched — PROVINCE.md, SKILL.md, README.md,
corpus/QUALITY.md, tools/registry.json, SHONEN.md,
tools/mutate-and-run.sh and the guarded probe
`tools/coldread-precheck-portable.py` (blob sha256 `892a045d…`)
blob-identical base → tip; the diff-tree check over those paths is empty
and corpus/SOURCES.md is the only monitored file in the round's diffs,
rekeyed; the C1 checker file is in no section's input union — verified
against the r68 union plan's 7702 union paths pre-declaration).

Tip receipts pinned here pre-data (they land at the tip receipts commit):
the tip guards at both floors + rev (`live-tip-guard-r69.out`,
`live-tip-guard-hist-r69.out`, `live-tip-revmode-r69.out`), the tip
invariant sweeps (`qline-tip-log-r69.txt`, `qline-tip-scorecard-r69.txt`,
`qline-green-round-69.txt`), the LOG/SCORECARD additivity pair
(`additivity-logscorecard-r69.txt`), the round-range self-sweep
(`tip-self-sweep-r69.txt` — forecast findings zero exit 0), and the
census end receipts (`census-end-r69.txt` at the fleet root, exit 0;
`census-end-lanetip-r69.txt` at the lane-tip shape, 160 rows).

**Tip-self-sweep erratum (appended at the tip receipts commit; measured,
the r66 own-range and r67 tip-count precedents).** The tip receipts
paragraph above pinned the self-sweep forecast findings zero exit 0; the
sweep measured findings=2 exit 1 (receipt `tip-self-sweep-r69.txt`:
commits=6 evidence=58 named=26 carried=25): the rekey commit's message
names two receipts its tree does not carry (`red-decode-r69.txt`,
`reh-red-decode-r69.txt` — they land at the receipts commit). Disclosed,
not rewritten; the mined fix is the round-69 lesson's mistake 5 (a
commit message names only tokens its tree carries — receipts named in a
message land with or before that commit). The tip sweeps and the
LOG/SCORECARD additivity pair measured the pre-erratum bytes at the
receipts commit `89869bea` (the r67 tip-count precedent); the erratum
appends above stay within the pure-append discipline the additivity
receipts certify.
## Round-70 corrections - the r69 closure's routed record defects (declared 2026-11-02, appended at the declaration commit; status-neutral, append-only: the stale figures above are preserved and stay flagged by the standing count-recheck sweep)

1. **Number drift in the r68-defect-1 correction narrative** (r69 spot-check routed defect 1): the r68-corrections paragraph above and the round-69 lesson print the unanchored command `grep -c 'figure-attribution check'` as reading "4 at both the r67 tip and the r68 tip"; measured at the r70 declaration: 4 at the r68-tip candidates (`434a96e4`, `ec6852f3`, `e39f9ba0`) - correct - but 0 at both r67-tip candidates (`859a736d`, the hash the paragraph cites, and `94b0fd7b`), and 5 at the r70 base `0c2573d7` (the r69 appends added an occurrence); the operative anchored measurement in the same sentence (0 at `859a736d` -> 1 at `434a96e4`) verifies exactly. Correction of record: this paragraph, the LOG erratum, the round-70 lesson carry-in, and the receipt re-running every printed command at the revision it names (`.ufo/evidence/round-70/win-host/carryin-correct-r70.txt` - the specific re-run output the r69 report cited by directory only). The stale figures stand as the count-recheck instrument's measured red arms (rows `scorecard-r68corr-unanchored-r67tip` and `lesson-r69-unanchored-r67tip`, both reading drift ok on every sweep).
2. **Two count nits** (r69 spot-check routed defect 2, the r69 report's landed-changes table): "20 receipt files" at the R1 receipts commit - 19 files were added at `89869bea` under `.ufo/evidence/round-69/win-host/` (diff-tree --diff-filter=A); "19 rehearsal receipts" - 18 files exist under `rehearsal/` at `5eb09e84` and at the base. Neither figure is claim-bearing; both corrected here and in the same receipt (the counting commands and outputs are in its Defect-2 section).

## Planned - round 70 (declared 2026-11-02, frozen before data)

The r69 closure (non-author verifier spot-check, `0c2573d7` = the commit
that landed it) ADMITTED round 69 clean: no routed defects barred
admission; three status-neutral record defects routed to this round and are
corrected above and in the LOG. The round's claims, declared frozen:

- **C1 (calibration, the lowest scored numeric axis at 8; capability
  acquisition; sourced on new row S301, opened this round - Git git-grep
  documentation; the r69 closure's routed printed-count class, executed).**
  `tools/count-recheck.py` + `tools/count-recheck.json` (new; schema
  `tameshi-count-recheck-v1`): a record's printed counting figure must
  still be the count its named command produces at the revision the record
  names - a manifest row pins (the record bytes at a revision, the exact
  record span carrying the figure, the printed integer, the counting
  command of record `git grep -c [-E] <pattern> <rev> -- <path>`, S301's
  --count contract); the span binding requires the pinned span to be a
  byte substring of the record and the printed integer to occur in the
  span as a delimited token; zero matches print nothing and exit 1, read
  as the count 0 (measured, disclosed - the page carries no exit-status
  section); unresolvable records are setup exit 2 before any row effect; a
  zero-row manifest is refused exit 2; an expect=drift row MEASURES the
  drift on every sweep. Standing manifest: seven rows - the two
  routed-defect red arms (printed 4, recount 0 at `859a736d`, expect
  drift) and five green arms pinning the operative anchored figures beside
  them. Selftest 6/6 hermetic (match-met, drift-met, mismatch-caught,
  span-absent, unresolvable, vacuous-usage); rehearsal sweep rows=7 met=7
  with both red arms reading drift ok.
- **C2 (operability, verdict-only): the two standing manifests grow with
  their named successor rows, checker blobs unchanged.** (i)
  `tools/arm-liveness.json` 6 -> 7 rows: `bind-r69-own-range-red` - the
  r69 lesson mistake 5's named successor - pins the bind checker at
  `5541abaf` (blob byte-identical at the base, verified) over the r69 own
  range `434a96e4..89869bea`, tally findings expect >=2 exit 1 (the rekey
  commit `b59ca7fe` names `red-decode-r69.txt` and `reh-red-decode-r69.txt`
  one commit before they land). (ii) `tools/anchor-drift-sweep.json` 4 ->
  16 rows: the r69 lesson's next-round carry executed - every held row
  with a committed win-host snapshot extract whose bytes verify (S289's
  page via the r61 re-open extract, S294-S298; each blob sha256 re-computed
  against its recorded digest, all six match), two rows each: the page h1
  and the page's own section heading the anchor cell locates, extracted
  from the pinned bytes, never recalled; the S299 red arm stays; the
  anchor-drift and arm-liveness capability rows sync append-only.
- Shared no-harm forecast: the SOURCES edit (one row + one tail note, the
  r67/r68/r69 edit shape) is the round's only monitored-file change; the
  live RED at the C1 SOURCES work commit is forecast at lost=13 with
  cand_credited=51 - the SAME 13 headings as the r68 AND r69 measured sets
  and this round's rehearsal (decoded comparison `reh-red-decode-r70.txt`:
  equal in order to both, miss = 0), paid by the `r70-batch-1` rekey (13
  fresh input-keyed entries; ledger 771 -> 784) restoring lost=0 ok exit 0
  at both floors plus rev mode 64/64 probe 20/20 (receipts
  `live-green-r70.out`, `live-green-hist-r70.out`, `live-revmode-r70.out`,
  `rebind-stdout-r70.txt`, `count-selftest-r70.txt`,
  `anchor-standings-r70.txt`).

| # | Claim | The move | Axis / claim type | Before | After (expected) | Counting command | Measured commit |
|---|---|---|---|---|---|---|---|
| R70-C1 | `tools/count-recheck.py` + `tools/count-recheck.json` (new; schema `tameshi-count-recheck-v1`): a record's printed counting figure must still be the count its named command produces at the revision the record names; manifest rows pin (record at a revision, the exact span carrying the figure, the printed integer, the counting command of record `git grep -c [-E] <pattern> <rev> -- <path>`); span binding (span byte-substring of the record, printed integer a delimited token in the span); zero matches = no output + exit 1 = count 0 (measured, disclosed); unresolvable records setup exit 2 before any row effect, zero-row manifest refused exit 2; an expect=drift row MEASURES the drift on every sweep; standing manifest 7 rows - the two routed red arms (scorecard-r68corr-unanchored-r67tip, lesson-r69-unanchored-r67tip: printed 4, recount 0 at `859a736d`) and five green anchored arms beside them; selftest 6/6 hermetic; capability row enters the table; sourced on new row S301 (Git git-grep documentation), opened this round | axis move + capability (the r69 closure's routed printed-count class made standing; two new files + the SOURCES row only - no checker blob changes) | calibration (numeric score 8 unchanged, at the lane-attainable cap; the move is record-figure honesty: the printed-count drift class becomes a standing measured red arm instead of a closure finding) | at base `0c2573d7`: `git ls-tree 0c2573d7 tools/ | grep -c count-recheck` -> 0 (no instrument exists; the drift was caught by the non-author closure re-running the printed command, not by any standing check); the drift measurable pre-instrument: the unanchored recount reads 0 at `859a736d` where both records print 4 (receipt `carryin-correct-r70.txt`); S301 anchored grep 0; registry rows 160 | selftest `COUNT_RECHECK_SELFTEST: 6/6 pass` exit 0 (rehearsed pre-data, `reh-count-selftest.txt`; live receipt `count-selftest-r70.txt`); standing sweep `COUNT_RECHECK: rows=7 met=7 unexpected=0` exit 0 with both red arms reading expect=drift printed=4 measured=0 ok (rehearsed, `reh-count-standings.txt`; live receipt `count-standings-r70.txt`); manifest id-grep -> 7; S301 grep 0 -> 1; registry rows 160 -> 161; capability-row anchored grep 0 -> 1 | `python -I -X utf8 tools/count-recheck.py --selftest`; `python -I -X utf8 tools/count-recheck.py --repo . --manifest tools/count-recheck.json`; `grep -c '"id"' tools/count-recheck.json`; `git show <rev>:corpus/SOURCES.md | grep -cE '^\| S301 '`; `git show <rev>:SCORECARD.md | grep -cE '^\| printed-count recheck'` | the C1 work commits (SOURCES first - the RED is measured there; tool + manifest follow); receipts land in the following commit(s) |
| R70-C2 | the two standing manifests grow with their named successor rows, checker blobs unchanged: (i) `tools/arm-liveness.json` 6 -> 7 rows - `bind-r69-own-range-red`, the r69 lesson mistake 5's named successor: the bind checker pinned at `5541abaf` (blob byte-identical at the base, verified) over the r69 own range `434a96e4..89869bea`, tally findings expect >=2 exit 1 (the rekey commit `b59ca7fe` names `red-decode-r69.txt` and `reh-red-decode-r69.txt` one commit before they land); (ii) `tools/anchor-drift-sweep.json` 4 -> 16 rows - the r69 lesson's next-round carry: every held row with a committed win-host snapshot extract whose bytes verify (S289's page via the r61 re-open extract, S294-S298; blob sha256 re-computed at the base against each row's recorded digest, all six match), two rows each (page h1 + the section heading the anchor cell locates, extracted from the pinned bytes, never recalled; S295's Generation definition resolves to the page's own "5.1.3 Generation" heading, disclosed); the S299 red arm stays; capability rows sync append-only | axis move (the r69 lesson's two named successor works, executed; manifest data only - no checker blob changes) | operability (verdict-only axis: both standing sweeps re-measure their grown row sets on every run; the freshness score is NOT touched - the r45 operator-priced boundary held) | at base `0c2573d7`: `grep -c '"id"' tools/arm-liveness.json` -> 6; `grep -c '"id"' tools/anchor-drift-sweep.json` -> 4; `grep -c bind-r69 tools/arm-liveness.json` -> 0; the r69-range sweep reads findings=2 (receipt `tip-self-sweep-r69.txt`; re-measured `reh-bind-r69-range.txt`: commits=6 evidence=58 named=26 carried=25 spans=3 bare=27 findings=2, exit 1) | `ARM_LIVENESS: rows=7 live=7 dead=0` exit 0 with `ARM_LIVE bind-r69-own-range-red tally=findings=2 exit=1` (rehearsed, `reh-arm-live-standings-r70.txt`; live receipt `arm-live-standings-r70.txt`; checker selftest unchanged 5/5, `arm-liveness-selftest-r70.txt`); `ANCHOR_DRIFT: rows=16 met=16 unexpected=0` exit 0 with the red row expect=absent measured=absent ok (rehearsed, `reh-anchor-standings-r70.txt`; live receipt `anchor-standings-r70.txt`); manifest id-greps 7 and 16; both capability rows synced append-only (r69-era figures stand at the r69 bytes; old -> new in the lesson) | `python -I tools/arm-liveness.py --repo . --manifest tools/arm-liveness.json`; `grep -c '"id"' tools/arm-liveness.json`; `python -I -X utf8 tools/anchor-drift-sweep.py --repo . --manifest tools/anchor-drift-sweep.json`; `grep -c '"id"' tools/anchor-drift-sweep.json` | the C2 work commit (both manifests); receipts land in the following commit(s) |

The C1 SOURCES work commit carries only corpus/SOURCES.md; the C1 tool
work commit carries the two new files; the C2 work commit carries the two
manifests; neither claim needs the other (causally separable). Receipts
land per the receipt-after-subject ordering; every commit message names
only file tokens its tree carries; the round ends with a self-sweep of
the round range (forecast: findings=0 exit 0) and a carries-what-it-names
diff-tree check of the tip before push.
## Round 70 - measured claims (appended at the receipts commit, 2026-11-02)

Declaration `b7f6f1627121ae394ca588b3027bcf54983cea26` (corrections
paragraph + planned block + lesson + LOG declared entry + S301 extract +
census receipt + rehearsal receipts); work commits C1 SOURCES
`910a3c354f3d4c036d2d7dba184884da0c21c5d8` (row S301 + the round-70 tail
note - the RED measured here), C1 tool
`3af968fa136e0fe212644cd3652731532cf1d5b0` (the count-recheck tool +
manifest), C2 `6c4447ac3bb32fb5f7e0bb3d8c87261f9036ed73` (both manifests);
rekey `44f61fba44527fa5b90a479cee08618ee8a8db3e` (the live RED paid: 13
fresh input-keyed entries as `r70-batch-1`, ledger 771 -> 784, monitor
restored at both floors). Receipts commit: this one.

| Claim | Verdict | After (measured) | Counting commands (live outputs in the receipts) | Measured commit |
|---|---|---|---|---|
| R70-C1 | verifies (measured) | selftest `COUNT_RECHECK_SELFTEST: 6/6 pass` exit 0 (`count-selftest-r70.txt`; rehearsed pre-data, `reh-count-selftest.txt`); the standing sweep `COUNT_RECHECK: rows=7 met=7 unexpected=0` exit 0 with both red arms measured, not assumed: `COUNT_ROW scorecard-r68corr-unanchored-r67tip expect=drift printed=4 measured=0 ok` and `COUNT_ROW lesson-r69-unanchored-r67tip expect=drift printed=4 measured=0 ok` - the r69 closure's routed figures standing as measured red arms, beside the operative anchored greens (printed 0 measured 0 at `859a736d`, printed 1 measured 1 at `434a96e4`; `count-standings-r70.txt`); manifest id-grep 7; S301 grep 0 -> 1; registry rows 160 -> 161 | `python -I -X utf8 tools/count-recheck.py --selftest`; `python -I -X utf8 tools/count-recheck.py --repo . --manifest tools/count-recheck.json`; `grep -c '"id"' tools/count-recheck.json`; `git show <rev>:corpus/SOURCES.md \| grep -cE '^\| S301 '` | C1 commits `910a3c35...` (SOURCES - the RED measured there) + `3af968fa...` (tool + manifest); receipts at the receipts commit |
| R70-C2 | verifies (measured) | the arm-liveness standing sweep `ARM_LIVENESS: rows=7 live=7 dead=0` exit 0 with `ARM_LIVE bind-r69-own-range-red tally=findings=2 exit=1` - the r69 lesson mistake 5's carries-what-it-names class standing as a measured red arm (`arm-live-standings-r70.txt`; the checker selftest unchanged 5/5, `arm-liveness-selftest-r70.txt`); the anchor-drift standing sweep `ANCHOR_DRIFT: rows=16 met=16 unexpected=0` exit 0 with the S299 red arm still measured expect=absent measured=absent ok and the six successor snapshots resolving page h1 + anchor heading each (`anchor-standings-r70.txt`; the checker selftest 5/5, `anchor-selftest-r70.txt`); manifest id-greps 7 and 16 | `python -I tools/arm-liveness.py --repo . --manifest tools/arm-liveness.json`; `grep -c '"id"' tools/arm-liveness.json`; `python -I -X utf8 tools/anchor-drift-sweep.py --repo . --manifest tools/anchor-drift-sweep.json`; `grep -c '"id"' tools/anchor-drift-sweep.json` | C2 commit `6c4447ac...`; receipts at the receipts commit |

Capability row entered (see `## Capabilities`): **printed-count
recheck** - first working round 70 (the mid-file insertion is disclosed;
additivity raw_old_only=0 on the file holds).

**Arm-liveness capability-row sync (append-only; the r67 correction-4
precedent).** The `counter-arm liveness check` row (round 66) carries the
r66-era figures - selftest 4/4, standing manifest `rows=3 live=3
dead=0` - true at those bytes and unchanged there; at the round-70
manifest bytes the same instrument reads selftest 5/5 and the manifest
`rows=7 live=7 dead=0` with the precheck RED arm and the new
`bind-r69-own-range-red` row live (`arm-liveness-selftest-r70.txt`,
`arm-live-standings-r70.txt`). Old -> new logged in the round-70 lesson;
the row above is not edited in place under the additivity discipline.

**Anchor-drift capability-row sync (append-only; the same precedent).**
The `anchor-drift sweep` row (round 69) carries the r69-era figures -
selftest 5/5, standing manifest `rows=4 met=4 unexpected=0` - true at the
r69 bytes and unchanged there; at the round-70 manifest bytes the same
instrument reads `rows=16 met=16 unexpected=0` with the S299 red arm
still measured and the six successor snapshots resolving
(`anchor-standings-r70.txt`). Old -> new logged in the round-70 lesson;
the row above is not edited in place.

Shared no-harm story (measured): the RED at the C1 SOURCES work commit
`910a3c35` reads `COLDREAD_PRECHECK floor=0c2573d7a316 floor_credited=64
cand=910a3c354f3d cand_credited=51 lost=13 RED` exit 1 (receipt
`live-red-r70.out` with the JSON receipt `red-receipt-r70.json`; the 13
LOST heading lines decode byte-equal in order to the r68 measured set,
the r69 measured set AND this round's rehearsal - miss = 0; receipt
`red-decode-r70.txt` with the rehearsal twin `reh-red-decode-r70.txt`) -
paid by the `r70-batch-1` rekey: REBIND OK sections=13 entries_added=13
ledger_before=771 (receipt `rebind-stdout-r70.txt`; ledger 771 -> 784;
machinery constants-only diff `make-rebind-r70.diff`, 7 changed pairs,
every changed line constants-only: docstring round, trace path, round /
batch / carried_from / rekey_batch fields, and the stale round-64 reader
string fixed to round 70 - the committed r67 as-run bytes are the diff
base, disclosed) -> lost=0 ok exit 0 at BOTH floors at the rekey commit
`44f61fba` (receipt `live-green-r70.out`: round floor `0c2573d7` 64 ->
64; receipt `live-green-hist-r70.out`: historic `8b0042bd` 46 -> 64) plus
rev mode credited=64/64 probe_sampled=20 probe_mismatches=0 (receipt
`live-revmode-r70.out`); additivity raw_old_only=0 on SOURCES
(`0c2573d7` -> `910a3c35`, 2 new lines disclosed - the mid-file row
insertion + tail note, verbatim_prefix=false; receipt
`additivity-sources-r70.txt`) and on the ledger (`910a3c35` ->
`44f61fba`, 29 new lines disclosed - the mid-file entries-array
insertion, verbatim_prefix=false; receipt `additivity-ledger-r70.txt`);
no owned axis harmed: depth 10, freshness 9, calibration 8 unchanged (no
depth or freshness surface touched - PROVINCE.md, SKILL.md, README.md,
corpus/QUALITY.md, tools/registry.json, SHONEN.md,
tools/mutate-and-run.sh and the guarded probe
`tools/coldread-precheck-portable.py` (blob sha256 `892a045d...`)
blob-identical base -> tip; the diff-tree check over those paths is empty
and corpus/SOURCES.md is the only monitored file in the round's diffs,
rekeyed; the round's tool files and manifests are in no section's input
union - verified against the r69 union plan's 7702 union paths
pre-declaration).

Tip receipts pinned here pre-data (they land at the tip receipts commit):
the tip guards at both floors + rev (`live-tip-guard-r70.out`,
`live-tip-guard-hist-r70.out`, `live-tip-revmode-r70.out`), the tip
invariant sweeps (`qline-tip-log-r70.txt`, `qline-tip-scorecard-r70.txt`,
`qline-green-round-70.txt`), the LOG/SCORECARD additivity pair
(`additivity-logscorecard-r70.txt`), the round-range self-sweep
(`tip-self-sweep-r70.txt` - forecast findings zero exit 0), and the census
end receipts (`census-end-r70.txt` at the fleet root, exit 0;
`census-end-lanetip-r70.txt` at the lane-tip shape, 161 rows).
**Tip-self-sweep erratum (appended at the receipts-repair commit; measured,
the r66 own-range and r67 tip-count precedents).** The tip receipts paragraph
above pinned the self-sweep forecast findings zero exit 0; the sweep measured
findings=19 exit 1 (commits=6 evidence=32 named=14 carried=14 spans=4 bare=37
findings=19, all at `22807192`): the receipts commit's message names 19
receipts its tree does not carry - the 20 receipt paths were passed to the
plumbing helper as absolute paths, which it silently drops (it takes
repo-relative paths only), so `22807192` carried only LOG.md and
SCORECARD.md. Disclosed, not rewritten; the receipts land in the
receipts-repair commit with this erratum (the guards, sweeps and census
receipts follow at the tip receipts commit); the mined fix is the round-70
lesson's mistake 4 (repo-relative paths only, and verify the landing with
diff-tree before writing the message). A future bind-erratum manifest row may
pin the `22807192` pair as its standing red arm (the r69 erratum precedent).
**Receipts-repair erratum 2 (appended at the second repair commit;
measured, the recurrence disclosure).** The receipts-repair commit above
repeated the mistake it disclosed: its 20 receipt paths were relative to
the caller's working directory, not repo-relative, and were silently
dropped again (`6e6cf2f7` carried only LOG.md, SCORECARD.md and the
lesson; its message names the 20 receipts; the range sweep ending there
reads findings=39 - 19 at `22807192` + 20 at `6e6cf2f7`). The receipts
land in THIS commit, repo-relative, the landing verified by diff-tree
before push; the standing findings are disclosed, permanent landed
history; the mined fix is the round-70 lesson's mistake 5.
## Planned - round 71 (declared 2026-11-02, frozen before data)

The r70 closure (non-author verifier spot-check, `4ed9ce1c` = the commit
that landed it) ADMITTED round 70 clean: no routed defects barred
admission; three items carried - two operator-side (the SHONEN
promotion-review note; the L2-minimum prompt item, an L0 line appended
this round) and one lane carry executed this round as C2 (the
bind-erratum manifest rows the spot-check called "a reasonable
next-round carry"). The round's claims, declared frozen:

- **C1 (calibration, the lowest scored numeric axis at 8; capability
  acquisition; sourced on new row S302, opened this round - the GNU sed
  manual; adopts considerthese 2026-10-28 proposal 5, the one
  assimilation this round).**
  `tools/pointer-recheck.py` + `tools/pointer-recheck.json` (new; schema
  `tameshi-pointer-recheck-v1`): a record's cited line pointer must still
  point at the content the record claims at the revisions the record
  names - a manifest row pins (the record bytes at a revision, the exact
  cited pointer token as it occurs in the record, the target path at a
  revision, the 1-indexed inclusive line span, the needle - the content
  the record claims the span carries); the span engine of record
  `git cat-file blob <rev>:<path> | sed -n 'START,ENDp'` (S302's
  inclusive address-range contract), argv stages only, sed load-bearing
  (not spawnable = setup exit 2, never a silent fallback); span read from
  git objects, never a worktree; a span past the last line prints nothing
  (measured) and reads as a miss; needles match as UTF-8 bytes, mid-line
  needles terminator-agnostic (selftest arm 5 measures CRLF); the pointer
  binding requires the token in the record bytes, else the row is an
  ERROR (the always-match cheat refused by construction);
  expect=hit|miss rows so a standing red arm MEASURES the drift on every
  sweep; unresolvable records/targets setup exit 2 before any row
  effect; zero-row manifest refused exit 2. Standing manifest: eight
  rows pinned at the base `4ed9ce1c` whose bytes were verified
  pre-declaration - the two r48 red arms (the closure-routed
  line-pointer defect: `corpus/SOURCES.md:140`/`:141` cited for
  S267/S268; those lines hold S265/S266, the rows sit at 142/143), the
  PROVINCE r16 red arm (`:85-91`; leg 7 `js-round-gate` sits at 94 - the
  ten-leg ledger at 88-97; the stale cell stands append-only, the
  correction of record is the round-71 lesson), and five green arms
  beside them (the r48 erratum's corrected pointers 142/143, the
  spotcheck's `142-143`, the verdict-table's `SCORECARD.md:13-14` and
  `LOG.md:68`). Selftest 7/7 hermetic.
- **C2 (operability, verdict-only): the standing arm-liveness manifest
  grows with its named successor rows, checker blob unchanged.**
  `tools/arm-liveness.json` 7 -> 9 rows: `bind-r70-receipts-red` - the
  r70 lesson mistake 4's named successor and the r70 spot-check's
  suggested carry - pins the bind checker at `5541abaf` (blob
  byte-identical at the base, `c3e6a88e...`, verified) over the r70
  range `0c2573d7..22807192`, tally findings expect >=19 exit 1; and
  `bind-r70-repair1-red` - the r70 lesson mistake 5's named successor
  (the recurrence) - over `0c2573d7..6e6cf2f7`, tally findings expect
  >=39 exit 1; the arm-liveness capability row syncs append-only.
- Shared no-harm forecast: the SOURCES edit (one row + one tail note,
  the r67/r68/r69/r70 edit shape) is the round's only monitored-file
  change; the live RED at the C1 SOURCES work commit is forecast at
  lost=13 with cand_credited=51 - the SAME 13 headings as the r68, r69
  AND r70 measured sets and this round's rehearsal (decoded comparison
  `reh-red-decode-r71.txt`: equal in order to both reference sets, miss
  = 0), paid by the `r71-batch-1` rekey (13 fresh input-keyed entries;
  ledger 784 -> 797) restoring lost=0 ok exit 0 at BOTH floors plus rev
  mode 64/64 probe 20/20 (receipts `live-green-r71.out`,
  `live-green-hist-r71.out`, `live-revmode-r71.out`,
  `rebind-stdout-r71.txt`, `pointer-selftest-r71.txt`,
  `arm-live-standings-r71.txt`).

| # | Claim | The move | Axis / claim type | Before | After (expected) | Counting command | Measured commit |
|---|---|---|---|---|---|---|---|
| R71-C1 | `tools/pointer-recheck.py` + `tools/pointer-recheck.json` (new; schema `tameshi-pointer-recheck-v1`): a record's cited line pointer must still point at the content the record claims at the revisions the record names; rows pin (record at a revision, exact pointer token, target at a revision, 1-indexed inclusive span, needle); span engine of record `git cat-file blob <rev>:<path> | sed -n 'START,ENDp'` (S302), argv stages only, sed load-bearing (not spawnable = setup exit 2); span past last line reads as a miss (measured); UTF-8 needle bytes, mid-line needles terminator-agnostic (CRLF arm measured); pointer binding (token must occur in the record bytes, else ERROR - always-match refused by construction); expect hit/miss so the standing red arm MEASURES the drift every sweep; setup exit 2 before any row effect, zero-row manifest refused exit 2; standing manifest 8 rows - the two r48 red arms + the PROVINCE r16 red arm (expect=miss, measured) and five green arms beside them; selftest 7/7 hermetic; capability row enters the table; sourced on new row S302 (GNU sed manual), opened this round; adopts considerthese 2026-10-28 proposal 5 | axis move + capability (the stale-line-pointer class - r48 closure-routed, proposal-5-named - made standing; two new files + the SOURCES row only - no checker blob changes) | calibration (numeric score 8 unchanged, at the lane-attainable cap; the move is record-pointer honesty: the stale-line-pointer class becomes a standing measured red arm instead of a spot-check finding) | at base `4ed9ce1c`: `git ls-tree 4ed9ce1c tools/ | grep -c pointer-recheck` -> 0 (no instrument exists; the r48 defect was caught by the non-author spot-check, and the PROVINCE `:85-91` drift was measured by no standing check); the drift measurable pre-instrument: the 85-91 span holds no `js-round-gate` line (grep -> 0) while line 94 does, line 140 holds no S267 row marker (grep -> 0) while 142 does (receipt `base-measure-r71.txt`); S302 anchored grep 0; registry rows 161 | selftest `POINTER_RECHECK_SELFTEST: 7/7 pass` exit 0 (rehearsed pre-data, `reh-pointer-selftest.txt`; live receipt `pointer-selftest-r71.txt`); standing sweep `POINTER_RECHECK: rows=8 met=8 unexpected=0` exit 0 with all three red arms reading expect=miss measured=miss ok (rehearsed, `reh-pointer-standings-r71.txt`; live receipt `pointer-standings-r71.txt`); manifest id-grep -> 8; S302 grep 0 -> 1; registry rows 161 -> 162; capability-row anchored grep 0 -> 1 | `python -I -X utf8 tools/pointer-recheck.py --selftest`; `python -I -X utf8 tools/pointer-recheck.py --repo . --manifest tools/pointer-recheck.json`; `grep -c '"id"' tools/pointer-recheck.json`; `git show <rev>:corpus/SOURCES.md | grep -cE '^\| S302 '`; `git show <rev>:SCORECARD.md | grep -cE '^\| line-pointer recheck'` | the C1 work commits (SOURCES first - the RED is measured there; tool + manifest follow); receipts land in the following commit(s) |
| R71-C2 | the standing arm-liveness manifest grows with its named successor rows, checker blob unchanged: `tools/arm-liveness.json` 7 -> 9 rows - `bind-r70-receipts-red` (the r70 lesson mistake 4's named successor and the r70 spot-check's suggested carry): the bind checker pinned at `5541abaf` (blob byte-identical at the base `c3e6a88e...`, verified) over the r70 range `0c2573d7..22807192`, tally findings expect >=19 exit 1 (the receipts commit names 19 receipt files its tree does not carry - the helper silently dropped absolute paths); `bind-r70-repair1-red` (the r70 lesson mistake 5's named successor, the recurrence): over `0c2573d7..6e6cf2f7`, tally findings expect >=39 exit 1 (the first repair repeated the mistake cwd-relative, 20 more dropped); the arm-liveness capability row syncs append-only (old -> new in the lesson) | axis move (the r70 lesson mistakes 4-5's named successors, executed; manifest data only - no checker blob changes) | operability (verdict-only axis: the standing sweep re-measures its grown row set on every run; the freshness score is NOT touched - the r45 operator-priced boundary held) | at base `4ed9ce1c`: `git show 4ed9ce1c:tools/arm-liveness.json | grep -c '"id"'` -> 7; `git show 4ed9ce1c:tools/arm-liveness.json | grep -c bind-r70` -> 0; both range sweeps re-measured at their disclosed figures (`reh-bind-r70-receipts-range.txt` findings=19 exit 1; `reh-bind-r70-repair1-range.txt` findings=39 exit 1 - the r70 errata's numbers) | `ARM_LIVENESS: rows=9 live=9 dead=0` exit 0 with `ARM_LIVE bind-r70-receipts-red tally=findings=19 exit=1` and `ARM_LIVE bind-r70-repair1-red tally=findings=39 exit=1` (rehearsed, `reh-arm-live-standings-r71.txt`; live receipt `arm-live-standings-r71.txt`; checker selftest unchanged 5/5, `arm-liveness-selftest-r71.txt`); manifest id-grep -> 9; capability row synced append-only (r70-era figures stand at the r70 bytes; old -> new in the lesson) | `python -I tools/arm-liveness.py --repo . --manifest tools/arm-liveness.json`; `grep -c '"id"' tools/arm-liveness.json` | the C2 work commit (the manifest); receipts land in the following commit(s) |

The C1 SOURCES work commit carries only corpus/SOURCES.md; the C1 tool
work commit carries the two new files; the C2 work commit carries the one
manifest; neither claim needs the other (causally separable). Receipts
land per the receipt-after-subject ordering; every commit message names
only file tokens its tree carries; the round ends with a self-sweep of
the round range (forecast: findings=0 exit 0) and a carries-what-it-names
diff-tree check of the tip before push.
## Round 71 - measured claims (appended at the receipts commit, 2026-11-02)

Declaration `0f554e16a56be69f02b4462f7358c81cda31963e` (planned block +
lesson + LOG declared entry + S302 extract + census receipt +
base-measure receipt + rehearsal receipts); work commits C1 SOURCES
`1b9a029347a6e6d7800e4f6e39ff0c4b3efcd63e` (row S302 + the round-71 tail
note - the RED measured here), C1 tool
`8a50ed20380f90d5ee7f5e984a5940b5e56b3084` (the pointer-recheck tool +
manifest), C2 `105ac918d239186dd4b831ad1ebb9f142b4c1d19` (the
arm-liveness manifest); rekey `4f01e28ceda0be008f574688ef9f05429a93aa01`
(the live RED paid: 13 fresh input-keyed entries as `r71-batch-1`,
ledger 784 -> 797, monitor restored at both floors). Receipts commit:
this one.

| Claim | Verdict | After (measured) | Counting commands (live outputs in the receipts) | Measured commit |
|---|---|---|---|---|
| R71-C1 | verifies (measured) | selftest `POINTER_RECHECK_SELFTEST: 7/7 pass` exit 0 (`pointer-selftest-r71.txt`; rehearsed pre-data, `reh-pointer-selftest.txt`); the standing sweep `POINTER_RECHECK: rows=8 met=8 unexpected=0` exit 0 with all three red arms measured, not assumed: `POINTER_ROW lesson-r48-s267-pointer-140 expect=miss measured=miss ok`, `POINTER_ROW lesson-r48-s268-pointer-141 expect=miss measured=miss ok` and `POINTER_ROW province-r16-sevenleg-85-91 expect=miss measured=miss ok` - the r48 closure's routed line-pointer defect and the PROVINCE r16 append's measured-stale claim standing as measured red arms, beside the five green arms (the r48 erratum's corrected pointers hit, the spotcheck's range hit, the verdict-table's two receipt pointers hit; `pointer-standings-r71.txt`); manifest id-grep 8; S302 grep 0 -> 1; registry rows 161 -> 162 | `python -I -X utf8 tools/pointer-recheck.py --selftest`; `python -I -X utf8 tools/pointer-recheck.py --repo . --manifest tools/pointer-recheck.json`; `grep -c '"id"' tools/pointer-recheck.json`; `git show <rev>:corpus/SOURCES.md \| grep -cE '^\| S302 '` | C1 commits `1b9a0293...` (SOURCES - the RED measured there) + `8a50ed20...` (tool + manifest); receipts at the receipts commit |
| R71-C2 | verifies (measured) | the arm-liveness standing sweep `ARM_LIVENESS: rows=9 live=9 dead=0` exit 0 with both new arms firing at the disclosed figures: `ARM_LIVE bind-r70-receipts-red tally=findings=19 exit=1` and `ARM_LIVE bind-r70-repair1-red tally=findings=39 exit=1` - the r70 lesson mistakes 4-5's carries-what-it-names pair standing as measured red arms (`arm-live-standings-r71.txt`; the checker selftest unchanged 5/5, `arm-liveness-selftest-r71.txt`); manifest id-grep 9 | `python -I tools/arm-liveness.py --repo . --manifest tools/arm-liveness.json`; `grep -c '"id"' tools/arm-liveness.json` | C2 commit `105ac918...`; receipts at the receipts commit |

Capability row entered (see `## Capabilities`): **line-pointer recheck**
- first working round 71 (the mid-file insertion is disclosed;
additivity raw_old_only=0 on the file holds).

**Arm-liveness capability-row sync (append-only; the r67 correction-4
and round-70 precedents).** The `counter-arm liveness check` row (round
66) carries the r66-era figures - selftest 4/4, standing manifest
`rows=3 live=3 dead=0` - true at those bytes and unchanged there; at the
round-70 manifest bytes the same instrument reads selftest 5/5 and the
manifest `rows=7 live=7 dead=0` (the round-70 sync paragraph above); at
the round-71 manifest bytes it reads selftest 5/5 and the manifest
`rows=9 live=9 dead=0` with the two bind-erratum arms live at findings=19
and findings=39 (`arm-live-standings-r71.txt`,
`arm-liveness-selftest-r71.txt`). Old -> new logged in the round-71
lesson; the row above is not edited in place under the additivity
discipline.

Shared no-harm story (measured): the RED at the C1 SOURCES work commit
`1b9a0293` reads `COLDREAD_PRECHECK floor=4ed9ce1c52e2 floor_credited=64
cand=1b9a029347a6 cand_credited=51 lost=13 RED` exit 1 (receipt
`live-red-r71.out` with the JSON receipt `red-receipt-r71.json`; the 13
LOST heading lines decode byte-equal in order to the r68 measured set,
the r69 measured set, the r70 measured set AND this round's rehearsal -
miss = 0; receipt `red-decode-r71.txt`) - paid by the `r71-batch-1`
rekey: REBIND OK sections=13 entries_added=13 ledger_before=784 (receipt
`rebind-stdout-r71.txt`; ledger 784 -> 797; machinery constants-only
diff `make-rebind-r71.diff`, 7 changed pairs, every changed line
constants-only: docstring round, trace path, round / batch /
carried_from / rekey_batch fields, and the stale round-64 reader string
fixed to round 71 - derived from the committed r67 as-run bytes,
disclosed) -> lost=0 ok exit 0 at BOTH floors at the rekey commit
`4f01e28c` (receipt `live-green-r71.out`: round floor `4ed9ce1c` 64 ->
64; receipt `live-green-hist-r71.out`: historic `8b0042bd` 46 -> 64)
plus rev mode credited=64/64 probe_sampled=20 probe_mismatches=0
(receipt `live-revmode-r71.out`); additivity raw_old_only=0 on SOURCES
(`4ed9ce1c` -> `1b9a0293`, 2 new lines disclosed - the mid-file row
insertion + tail note, verbatim_prefix=false; receipt
`additivity-sources-r71.txt`) and on the ledger (`1b9a0293` ->
`4f01e28c`, 29 new lines disclosed - the mid-file entries-array
insertion, verbatim_prefix=false; receipt `additivity-ledger-r71.txt`);
no owned axis harmed: depth 10, freshness 9, calibration 8 unchanged (no
depth or freshness surface touched - PROVINCE.md, SKILL.md, README.md,
corpus/QUALITY.md, tools/registry.json, SHONEN.md,
tools/mutate-and-run.sh and the guarded probe
`tools/coldread-precheck-portable.py` (blob sha256 `892a045d...`)
blob-identical base -> tip; the diff-tree check over those paths is
empty and corpus/SOURCES.md is the only monitored file in the round's
diffs, rekeyed; the round's tool files and manifest edits are in no
section's input union - verified against the r70 union plan's 7702
unique union paths pre-declaration, receipt `reh-union-check-r71.txt`).

Tip receipts pinned here pre-data (they land at the tip receipts commit):
the tip guards at both floors + rev (`live-tip-guard-r71.out`,
`live-tip-guard-hist-r71.out`, `live-tip-revmode-r71.out`), the tip
invariant sweeps (`qline-tip-log-r71.txt`, `qline-tip-scorecard-r71.txt`,
`qline-green-round-71.txt`), the LOG/SCORECARD additivity pair at the
receipts commit (`additivity-logscorecard-r71.txt`), the round-range
self-sweep (`tip-self-sweep-r71.txt` - forecast findings zero exit 0),
and the census end receipts (`census-end-r71.txt` at the fleet root,
exit 0; `census-end-lanetip-r71.txt` at the lane-tip shape, 162 rows).

## Round 72 — declared claims (2026-11-03), frozen before data

Plan: `plans/round-72.plan.md` (predicates, counters, kill rules, arms).

- **R72-C1 — operability (capability acquisition): planning-time rekey-cost
  forecast.** Before: no instrument prices a planned monitored-file edit
  (`git ls-tree -r f20ba48 tools/ | grep -c rekey-cost` → 0). After:
  `python3 -I tools/rekey-cost.py --edit corpus/SOURCES.md --edit
  PROVINCE.md` → `REKEY_COST sections=64 planned=2 at_risk=17
  predicted_lost=17`, selftest 8/8, arms 13/6/6/0/0/exit-2 each equal to a
  guard-measured counterfactual, and the round's 17 equal to the guard's
  measured lost at the edit commit.
- **R72-C2 — calibration (lowest scored axis, 8).** Before: S302 cites §4.3
  where the snapshot's heading is §4.2; `PROVINCE.md:57` carries `:85-91`
  where the ledger sits at 88–97. After: S303 supersedes S302 with the §4.2
  anchor, the PROVINCE append names `:88-94` and `:88-97`, three pointer
  rows read hit at the tip and miss at base, census exit 0, and the rekey
  paid (17 sections) so the monitor reads 64/64 at both floors and in rev
  mode.

Verdicts and measurements are appended at the receipts commit; nothing above
is a measured result.

## Round 72 — measured claims (appended at the receipts commit, 2026-11-03)

Declaration `dfb534ca4f1156e8a45005b52a3c48e43461b348` (plan, wave spec +
dispatch, census-start, base measure, five counterfactual rehearsals). Work
commits: C2 `d618518a6783cc0384a8b2c699d757baae5a6b0f` (S303 supersession +
the PROVINCE append + corrections note + this lesson), rekey
`bc7dc2fba353e604e687f7cd594c8358937d8908` (17 sections, ledger 797 -> 814),
C1 `b3392010cc8b9e5b98acba5d0c2dff9fb08b4691` (the forecast tool + the
capability row). Receipts: this commit; every figure below is byte-backed under `.ufo/evidence/round-72/`.

| Claim | Verdict | After (measured) | Counting commands (live outputs in `.ufo/evidence/round-72/`) | Measured commit |
|---|---|---|---|---|
| R72-C1 | verifies (measured) | selftest `REKEY_COST_SELFTEST: 8/8 pass` exit 0; arms `at_risk=13` / `6` / `6` / `0` / `0` / `17`, no-path exit 2; the forecast 17 equals the guard's `COLDREAD_PRECHECK … lost=17 RED` at the edit commit; the model was validated against the guard on four single-edit counterfactuals before the freeze (`reh/`: `lost=13`, `lost=6`, `lost=6`, `lost=0`) | `python3 -I tools/rekey-cost.py --selftest`; `python3 -I tools/rekey-cost.py --edit <path>`; `python3 -I tools/coldread-precheck-portable.py --repo . --floor f20ba482c744 --cand d618518a6783` | `b3392010` (tool bytes; the live forecast at `d618518a`) |
| R72-C2 | verifies (measured) | `POINTER_RECHECK: rows=11 met=11 unexpected=0` with the three new rows `hit ok`; the control manifest `rows=2 met=2` both `miss ok`; the census on the edited file exits 0; the RED `lost=17 RED` at the edit commit paid by `REBIND OK sections=17 entries_added=17 ledger_before=797`, monitor `lost=0 ok` at both floors (`4ed9ce1c` 64 → 64, `8b0042bd` 46 → 64) and `credited=64/64` in rev mode | `python3 -I tools/pointer-recheck.py --repo . --manifest tools/pointer-recheck.json`; `… --manifest .ufo/evidence/round-72/control-manifest.json`; `python3 -I tools/coldread-precheck-portable.py …`; `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root … tameshi` | `d618518a` (edits) → `bc7dc2fb` (rekey) |

Capability row entered (see `## Capabilities`): **rekey-cost forecast** —
first working round 72; the mid-file insertion is disclosed and the file's
additivity holds (appends + one table row).

No axis harmed: depth 10, calibration 8 and freshness 9 unchanged — the
monitored bytes are identical base → tip (`monitored-bytes-r72.txt`), the
only monitored edits are SOURCES.md and PROVINCE.md and both are rekeyed, and
the standing instruments re-read clean (figure-attribution 3/3, count-recheck
7/7, anchor-drift 16/16, arm-liveness 9/9 live, pointer selftest 7/7).
Calibration's score is not re-scored by this round: the row records the axis
move (two routed defects measured-and-corrected), not a new number — a score
no reader can re-derive is an opinion.

### Round 72 — appended: third correction, batch-2 rekey, plan defect (2026-11-03)

Appended after the wave's attacks; the rows above stand as written.

- **Third correction.** Seat T72W1S05 found `PROVINCE.md:56`'s `:84-89` (the
  round-1 six-leg anchor) stale: the six-leg cut is `:88-93` (leg 6
  `js-claims-check` at 93). Corrected by a second append at `b7b98375`; the
  drift it owed was measured (`lost=6 RED`, `live-red2-r72.out`) and rekeyed as
  `r72-batch-2` (`REBIND OK sections=6 entries_added=6 ledger_before=814`;
  ledger 814 → 820, CRLF preserved). The fourth pointer row
  `province-r72-sixleg-cut-88-93` reads hit: the sweep is
  `POINTER_RECHECK: rows=12 met=12 unexpected=0` — the frozen plan said 11, the
  extra row is disclosed, never retro-fitted.
- **Plan defect (disclosed).** The frozen C2 control sentence ("the same three
  rows at base revs read three miss ok under rows=3 met=3") is unattainable as
  written: the instrument refuses a record revision whose pointer token is
  absent (`pointer-absent-in-record`), so a base-rev record cannot be scored
  (`POINTER_RECHECK error=setup … not in 'f20ba48'`, exit 2, seat T72W1S05). The
  control landed as the two-row stale-span manifest (`rows=2 met=2`, both miss)
  plus the seat's `rows=3 met=2 unexpected=1` measurement (the S303 row aims at
  the base line and MISSES) — the discriminating base evidence. C2's claim is
  unaffected; the frozen control line was wrong and is reported as wrong.
- **Coverage finding (carried).** The frozen arm battery does not cover the
  `IGNORED` filter: mutant M3 (drop it) survives every arm and is killed only by
  the selftest (seat T72W1S09). The arm table gains an ignored-path arm in the
  next round that re-prices the instrument.

Floor-id correction (round 72, appended): the round floor in `live-green-r72.out` is `f20ba482c744`; `4ed9ce1c` 64 -> 64 was measured separately at the tip (`live-green-floor4ed9-r72.txt`), and `8b0042bd` 46 -> 64 stands. All three read `lost=0 ok`.

## Round 73 — declared claims (2026-11-03), frozen before data

Plan: `plans/round-73.plan.md` (predicates, counters, kill rules, arms,
controls). Round shape: one v1 wave, 13 seats (3 executor · 2 scribe · scout ·
2 reviewer · critic · mutation-tester · sentinel · revenger · connector; attack
seats 4 = 30.8 %). `labrat` is a frozen-topology seat the validator rejects
(`ufo-swarm-wave.mjs:263`), so no labrat item exists.

- **R73-C1 — calibration (the lowest scored numeric axis at 8; capability
  acquisition; sourced on the re-opened S066).** `tools/wave-reconcile.py` +
  `tools/wave-reconcile.json`: a round record's execution claims (seat count,
  committed seat-report count, role multiset, attack share) are re-derivable
  from the committed wave artifacts, with the round-72 closure's two routed
  defects standing as MEASURED red arms.
- **R73-C2 — operability (verdict-only).** `tools/rekey-cost.py --arms`: the
  recorded arm table becomes a re-runnable 7-arm battery and gains the
  ignored-path arm the round-72 wave's coverage finding named.

## Round 73 — measured claims (appended at the receipts commit, 2026-11-03)

Declaration `17cd19396b36d4c15f1bce1bbdb7c42346f1df76`; work commits C1 tool
`fddbb667`, C1 record edits `be1199d3`, rekey batch-1 `2e89e539`, C2
`7982619f`, plan erratum `3e0ef1c8`, S066 repair `1d118c14`, rekey batch-2
`caa5c4c5`, pointer style repair `7c5ffe04`, C1 hardening `8f7ff279`,
criterion-122 pin `21a7332f`, rekey batch-3 `06ce20f7`. Receipts land under
`.ufo/evidence/round-73/`; the round's report cites the tip.

| Claim | Verdict | After (measured) | Counting commands (live outputs in the receipts) | Measured commit |
|---|---|---|---|---|
| R73-C1 | verifies (measured) | selftest `WAVE_RECONCILE_SELFTEST: 12/12 pass` exit 0; the standing sweep `WAVE_RECONCILE: rows=6 met=6 unexpected=0` exit 0 with both red arms measured (`printed=11 files=12`; plan `labrat` vs executed `revenger`); independent oracle `ORACLE_CMP rows=6 equal=6`; the three pre-freeze controls cannot reach the line (`rows=6 met=4 unexpected=2`; the green-only control reads `rows=4`); seat findings T73W1S03 adopted as hardening (`record` binding on every kind, unknown-root setup exit 2, roles rows de-printed) with the frozen counters unchanged | `python3 -I -X utf8 tools/wave-reconcile.py --selftest`; `python3 -I -X utf8 tools/wave-reconcile.py --repo . --extra-root fleet=/home/vgpnk/Projects/shokunin --manifest tools/wave-reconcile.json` | `fddbb667` → `8f7ff279` (tool bytes); rows pinned at `a3dd3574`/`3664a6d3` |
| R73-C2 | verifies (measured) | `REKEY_ARMS: arms=7 meet=7 unexpected=0` exit 0 at the C2 commit, after each of the round's three rekeys and at the tip; selftest `REKEY_COST_SELFTEST: 8/8 pass`; M3 killed by the battery (`ARM_UNEXPECTED ignored-skill expected=0 measured=9`, `arms=7 meet=6 unexpected=1` exit 1) and replicated origin-independently by seat T73W1S10 (1/7 battery arms, 1/8 selftest arms, value re-derived); before-state `KILLING_ARMS=0/6` over the six recorded arms | `python3 -I tools/rekey-cost.py --arms`; `python3 -I tools/rekey-cost.py --selftest` | `7982619f` (tool bytes); re-measured at `06ce20f7` and the tip |

Capability row entered (see `## Capabilities`): **wave-record reconciliation** —
first working round 73.

**No axis harmed.** depth 10, calibration 8, freshness 9 unchanged as numbers
(the round records axis moves, not new scores — r72's precedent). Monitored
bytes: `corpus/SOURCES.md` and `corpus/QUALITY.md` are the only monitored edits
and both are rekeyed (three batches: 13 + 13 + 6 sections, ledger 820 → 852);
`SKILL.md`, `corpus/README.md`, `PROVINCE.md`, `SHENON`/`SHONEN.md`,
`tools/registry.json`, `tools/mutate-and-run.sh` and
`tools/coldread-precheck-portable.py` are blob-identical base → tip. The guard
reads `lost=0 ok` at both floors and `credited=64/64` in rev mode at
`06ce20f7`; the standing instruments re-read clean (figure-attribution 7/7,
count-recheck 7/7, anchor-drift 16/16, arm-liveness 9/9 live, pointer 12/12,
bind 7/7 selftest).

**Named coverage gaps carried to round 74** (measured by wave seats, not this
round's counters): the delimited-token rule and the span-substring rule carry
no selftest arm (`delimited := True` survives 12/12 — T73W1S02); `seat_reports`
counting at any depth survives 12/12 and the sweep with a non-equivalence probe
(`files=12` vs `13` — T73W1S10); the IGNORED filter's *over-filtering*
direction survives both the battery and the selftest while turning a 20-pin
forecast into a false 0 (T73W1S09's M3c); rounds 61-71 carry no `results.json`
(11 unpinnable rounds) and round 60's artifact vocabulary is `agent='task'`
(T73W1S06).

**Counter-cheat and span disclosures (wave seats T73W1S07/T73W1S09, appended at
the same receipts commit).** Any output-pinned counter is spoofable by a stub
that echoes the manifest's own `expect` column (S07 measured a byte-exact
forgery with zero artifact reads), so the C1 line is a receipt, never an
authenticator, and this round does not represent its cheat coverage as
general; the evidence that the real tool derives its values is the independent
oracle (`ORACLE_CMP rows=6 equal=6`, S01), the two mutant batteries (S02, S10)
and the per-row `detail=` populations the summary line does not carry. The
`seat_reports` red arm is red by span choice: the same report self-corrects 25
lines later (S07), and the row deliberately pins the sentence the round-72
closure routed. The plan's own kill-rule wording ("any control below reaches
`unexpected=0`") is contradicted by the green-only control (`rows=4 met=4
unexpected=0` exit 0) and is reported as a frozen-text defect; the operative
reading is the frozen line with `rows=6`.

**Evidence pointers for the quoted spans above (full paths, so the standing
quoted-line sweep can back them).** `printed=11 files=12` and the six
`WAVE_ROW` lines live in `.ufo/evidence/round-73/wave-reconcile-live-r73.txt`;
`WAVE_RECONCILE_SELFTEST: 12/12 pass` in
`.ufo/evidence/round-73/wave-selftest-r73.txt`; `ORACLE_CMP rows=6 equal=6` in
`.ufo/waves/round-73/w1/T73W1S01.md`; `agent='task'` in
`.ufo/waves/round-73/w1/T73W1S06.md`; `rows=4 met=4 unexpected=0` in
`.ufo/evidence/round-73/reh/reh-c1-controls.txt`; `measured := expect` in
`.ufo/waves/round-73/w1/T73W1S07.md`; `TMPDIR_VIOLATIONS=0` and
`SECRETS=1` in `.ufo/waves/round-73/w1/T73W1S11.md`; `tameshi E01 S066
fields=8` in `.ufo/waves/round-73/w1/T73W1S05.md`.

## Round 74 — declared claims (2026-11-03), frozen before data

Plan: `plans/round-74.plan.md` (predicates, counters, kill rules, arms,
controls). Base `3d6ea1ee8e551e3baf94904384890e3a112088f0` (= `origin/master`,
the admitted round-73 closure). Round shape: one v1 wave, 12 seats (4 executor ·
1 scribe · 1 scout · 2 reviewer · 1 critic · 1 mutation-tester · 1 connector ·
1 sentinel; attack seats 4 = 33.3 %). `labrat` is a frozen-topology seat the
validator rejects, so no labrat item exists; the planner seat stays with the L1.

- **R74-C1 — operability (verdict-only).** The three arm gaps the round-73 wave
  named become measured arms of `tools/wave-reconcile.py`: the delimited-token
  rule, the record-span-substring rule, and `seat_reports` top-level-only
  counting. Before: `WAVE_RECONCILE_SELFTEST: 12/12 pass` and the three named
  mutants (`m2` `delimited := True`, the span-rule removal, `W2` any-depth)
  each survive all twelve arms. After: `15/15 pass` and a committed runner
  spec (`tools/wave-reconcile-mutants.spec`) that kills all three on their
  named arms.
- **R74-C2 — calibration (the lowest scored numeric axis at 8; sourced on the
  re-opened S294).** Append-only / content-preservation claims become a
  measured range sweep: `tools/additivity-range.py` +
  `tools/additivity-range.json` measure every commit of a declared range per
  file with a declared claim class and `expect: hold|violated`. Before: the
  per-pair tool has no range mode (`grep -c rev-list` → 0) and its default
  judgement on the round-73 `LOG.md` rewrite pair exits **0**; the round-73
  closure's two routed EOL rewrites have no standing measurement. After:
  `ADDRANGE: rows=6 met=6 unexpected=0` with both rewrites measured as declared
  violations at their own commits.

Capability to enter (if it verifies): **round-range additivity sweep** —
first-working round 74.

## Round 74 — measured claims (appended at the receipts commit, 2026-11-03)

Declaration `a7cd78ae4cbfc0cdd9656a203268087b6fbd589a`; work commits C1 tool
`2bbf9796`, C1 hardening `ee395675`, C2 tool `2e0ac486`, sourced Gate
`9fe58b40`, criterion-124/registry `607b96d8`, rekey batch-1 `9d9ab7d3`.
Receipts under `.ufo/evidence/round-74/`; the round's report cites the tip.

| Claim | Verdict | After (measured) | Counting commands (live outputs in the receipts) | Measured commit |
|---|---|---|---|---|
| R74-C1 | verifies (measured) | `WAVE_RECONCILE_SELFTEST: 15/15 pass` exit 0; battery `MUTATE: DONE (target=wave-reconcile-arms defects=3 killed=3 survived=0 inconclusive=0 kill-rate=100%)`; each named mutant dies on its named arm only (m2 → arm13, span rule → arm14, W2 → arm15); control GREEN; restore proof byte-identical; the standing six-row sweep unchanged (`rows=6 met=6 unexpected=0`) | `python3 -I -X utf8 tools/wave-reconcile.py --selftest`; `bash tools/mutate-and-run.sh --target tools/wave-reconcile.py --defects tools/wave-reconcile-mutants.spec --suite 'python3 -I -X utf8 "$MUTANT" --selftest' --label wave-reconcile-arms` | `2bbf9796` (tool bytes); hardened + re-run at `ee395675` |
| R74-C2 | verifies (measured) | `ADDRANGE: rows=6 met=6 unexpected=0` exit 0 with `ADDRANGE_TOTALS raw_old_only=8561 norm_cr_old_only=5`; the two round-73 routed EOL rewrites measure `violated` at their own commits (LOG.md `862e8844` raw 3484 / norm 0; QUALITY.md `21a7332f` raw 1593 / norm 5); selftest `ADDITIVITY_RANGE_SELFTEST: 8/8 pass`; the class control, the expect flip (`unexpected=1` exit 1) and the echo stub are in the controls receipt | `python3 -I tools/additivity-range.py --repo . --manifest tools/additivity-range.json`; `python3 -I tools/additivity-range.py --selftest` | `2e0ac486` |

Capability entered (see `## Capabilities`): **round-range additivity sweep** —
first working round 74. Gate-registry rows for both round-74 instruments (4
rows, `held=4/4`) land in the same round: r73 closure defect 5 paid for these
two instruments; the six older standing instruments still carry no row and are
named as an open carry.

**No axis harmed.** depth 10, calibration 8, freshness 9 unchanged as numbers
(the round records axis moves, not new scores). Monitored bytes: the two
monitored edits (`corpus/SOURCES.md`, `corpus/QUALITY.md`) plus
`tools/registry.json` staled 16 SKILL.md sections — measured RED at `607b96d8`
(`credited=48/64`, `.ufo/evidence/round-74/live-red-r74.out`) and rekeyed as
`r74-batch-1` (16 sections, ledger 852 → 868, EOL-preserving merge); the guard
then reads `credited=64/64` at `9d9ab7d3`
(`.ufo/evidence/round-74/live-green-r74.out`). The first rekey run used the
round-73 script copy and wrote its traces to the round-73 path; the ledger and
traces were restored byte-exactly from `607b96d8` and the corrected round-74
script re-ran (`141dead0` carries the superseded merge; `9d9ab7d3` the
corrected one).

**Named carries to round 75** (measured by wave seats, not this round's
counters): `M-C` (printed integer bound to the whole record instead of the
span) survives all fifteen arms — the next arm needs a fixture whose number is
delimited in the record but not in the span (T74W1M1); a selective
`_record_claim` bypass on roles/attack_share alone survives (T74W1R1); the
frozen plan's control-4 clause and its `eight-row` wording are frozen-text
defects (T74W1R2); the echo stub prints the summary line and is rejected only by
the totals line (T74W1R2); the range sweep's raw counts are predicate-dependent
(set-based 3484/1593 vs S1's line-counting 3801/3759 across the range) and the
`ADDRANGE` line is a receipt, never an authenticator; the six older standing
instruments still lack registry rows (T74W1SC1).

### Round 74 — appended: counter extension (wave seat T74W1C1) and the no-harm sequence

Appended after the wave; the measured-claims block above stands as written and
its frozen predicate is re-run, not replaced.

- **R74-C2 counter extended.** Every frozen `commits` row spanned one commit
  (seat T74W1C1), so the range mode was unexercised; the manifest now carries
  two whole-range walks plus the three missing commit-pairs (11 rows), and the
  extended line reads `ADDRANGE: rows=11 met=11 unexpected=0` with
  `ADDRANGE_TOTALS kind=commits-union keys=8 raw_old_only=5079
  norm_cr_old_only=7`. The frozen six-row line re-runs at `2e0ac486`:
  `ADDRANGE: rows=6 met=6 unexpected=0` exit 0
  (`.ufo/evidence/round-74/frozen-six-row-r74.txt`). The totals union, the
  `walked=` field and the `be1199d3` (damage) / `1d118c14` (repair) labels are
  corrected in the lesson's appended section.
- **No-harm sequence, measured.** `credited=64/64` at `9d9ab7d3` and
  `ee395675`; the records commit `1c3a428e` (LOG.md + SCORECARD.md) dropped the
  two sections whose newest entries pin those files → `credited=62/64`
  (receipt `.ufo/evidence/round-74/live-red2-r74.out`), rekeyed as
  `r74-batch-2` and re-measured green at the merging tip
  (`.ufo/evidence/round-74/live-green2-r74.out`).
- **Disclosure.** The first rekey attempt (commit `141dead0`) used the
  round-73 script copy, which wrote its traces to the round-73 path; the ledger
  and traces were restored byte-exactly from `607b96d8` and the corrected
  round-74 script re-ran (`9d9ab7d3`). `141dead0` stays in history as the
  superseded merge; no record cites it as the rekey.

Floor sequence correction (round 74, appended at the tip): the paragraph above
names `r74-batch-2` as the last rekey; the round paid **three** batches.
`r74-batch-2` (2 sections at `47cd112f`) restored `credited=64/64` at
`906303c7`; the round then re-pinned `additivity-range-sweep`'s registry needle
to the extended manifest line (`tools/registry.json` at `5f2f88aa`), which
re-staled 11 sections, and `r74-batch-3` (11 sections at `5f2f88aa`, ledger
870 → 881) restored `credited=64/64` at `9c27267b`
(`.ufo/evidence/round-74/live-green3-r74.out`). Ledger 852 → 881 across the
round; every merge is EOL-preserving (CRLF before/after printed by the tool).
The dependency the sequence exposes is named for the next round: a registry
needle and a LOG/SCORECARD append are cold-read inputs, so a round that does
both pays a batch after each — price them before the last rekey.

## Round 75 — declared claims (2026-11-03), frozen before data

Plan: `plans/round-75.plan.md` (predicates, counters, kill rules, arms,
controls; Correction 1 `7745d0e0` and Correction 2 `82f7a809`, both pre-data,
append-only). Base `21ef81e99966198cf8cdb2c6d8e56aa3c482da56` (= `origin/master`,
the admitted round-74 non-author closure). Declaration
`640d3fccfba7f6fab8e0341723b0fe6dbc200570`. Round shape: one v1 wave, 12 seats
(4 executor · 1 scribe · 1 scout · 2 reviewer · 1 critic · 1 mutation-tester ·
1 connector · 1 sentinel; attack seats 4 = 33.3 %), policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16. `labrat` is a frozen-topology
seat the validator rejects, so no labrat item exists; the planner seat stays
with the L1 per the orchestrator ruling.

- **R75-C1 — operability (verdict-only; sourced on the re-opened S006).** The
  round-74 survivors become measured arms of `tools/wave-reconcile.py`: `M-C`
  (printed integer bound to the whole record instead of the row's span) plus
  the selective `_record_claim` bypass on `roles` and on `attack_share`
  (three mutants, three arms). Before: `WAVE_RECONCILE_SELFTEST: 15/15 pass`
  (tool sha256 `97bb9272…`) and all three mutants alive. After: `18/18 pass`
  and each R75 mutant killed on its named arm (`arm16`/`arm17`/`arm18`) under
  the lane runner, with a committed six-defect spec that kills all six
  (three round-74 defects plus three new).
- **R75-C2 — calibration (the lowest scored numeric axis at 8).**
  `tools/selfstate-freshness.py` + `tools/selfstate-freshness.json`: 17 declared
  rows — the 16 live figures on 10 capability rows (the tuple table frozen in
  `.ufo/evidence/round-75/selfstate-control-scan.py`) plus 1 frozen historical
  statement — whose quoted figure must equal the instrument's own printed
  figure at the measured revision. Before (frozen counter at base):
  `SELFSTATE: rows=17 match=9 stale=8 unexpected=7`, exit 1. After:
  `SELFSTATE: rows=17 match=16 stale=1 unexpected=0` exit 0, with the frozen row
  measuring `stale` every sweep and the seven live cells superseded to their
  instrument's figure.

Capability to enter (it verifies): **self-state freshness check** — re-derive
a declared population of a record's live figures from the instruments that
print them at a measured revision, with a fail-closed setup exit and a standing
red row. First-working round 75.

## Round 75 — measured claims (appended at the records commit, 2026-11-04)

Declaration `640d3fcc`; corrections `7745d0e0`, `82f7a809`; work commit
`4e610748`. Receipts under
`.ufo/evidence/round-75/`; the round's report cites the tip.

| Claim | Verdict | After (measured) | Counting commands (live outputs in the receipts) | Measured commit |
|---|---|---|---|---|
| R75-C1 | verifies (measured) | `WAVE_RECONCILE_SELFTEST: 18/18 pass` exit 0; battery `MUTATE: DONE (target=wave-reconcile-arms-r75 defects=6 killed=6 survived=0 inconclusive=0 kill-rate=100%)`; each of the three R75 mutants fails only its named arm (17/18 each); the pre-existing mutants keep their named-arm kills (m2 also fails arm16; the span-rule mutant also fails arms 17/18 — the Correction-2 matrix); control GREEN; restore byte-identical | `python3 -I -X utf8 tools/wave-reconcile.py --selftest`; `bash tools/mutate-and-run.sh --target tools/wave-reconcile.py --defects tools/wave-reconcile-mutants.spec --suite 'python3 -I -X utf8 "$MUTANT" --selftest' --label wave-reconcile-arms-r75` | `4e610748` (tool bytes; battery `.ufo/evidence/round-75/c1-landed-battery.txt`) |
| R75-C2 | verifies (measured) | `SELFSTATE: rows=17 match=16 stale=1 unexpected=0` exit 0; every live row `match`; the frozen row `r74-frozen-addr-six expect=stale measured=stale ok`; selftest `SELFSTATE_SELFTEST: 10/10 pass`; the after-run at the repair commit re-derives every figure | `python3 -I -X utf8 tools/selfstate-freshness.py --repo . --manifest tools/selfstate-freshness.json --doc-rev <rev>`; `python3 -I -X utf8 tools/selfstate-freshness.py --selftest` | `4e610748` (repairs; after `.ufo/evidence/round-75/c2-after-r75.txt`) |

**No axis harmed.** depth 10, calibration 8, freshness 9 unchanged as numbers
(the round records axis moves, not new scores). Monitored edits this round:
`SCORECARD.md`, `LOG.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`,
`tools/registry.json` → forecast `REKEY_COST sections=64 planned=7 at_risk=16
predicted_lost=16` (`.ufo/evidence/round-75/rekey-cost-full-r75.txt`). One rekey
batch (`r75-batch-1`) after every content edit; the monitor's green receipt
lands in the final receipts commit.

**Named carries to round 76.** The `SKILL.md` gate-registry table still lists
neither `tools/wave-reconcile.py` nor `tools/additivity-range.py`
(round-74 closure defect 4; no `SKILL.md` edit is planned this round, so the
carry stays open); the six older standing instruments still carry no
`tools/registry.json` row; the `adv-seatreports-require-printed-bypass`
(R75 wave seat T75W1R1) drops `require_printed=True` in the `seat_reports`
branch and survives 18/18 — the next arm needs a printed-less `seat_reports`
row; the echo-stub disclosure stands (no printed line is an authenticator);
the `six-leg content-disposition probe` (`18/18` vs `19/19`) and `effective
expectation reconciliation` (`34/34` vs `66/66`) live cells stay as dated
literals under the round-17 disclosure (`SCORECARD.md:655-659`) whose own
superseding values are stale; round-73 routed items 3–4 and the r74 cold-read
pointer erratum remain open. If R75-C1 verifies, the two round-74 arm carries
(`M-C` and the selective `_record_claim` bypass) close.

## Round 76 — declared claims (2026-11-04), frozen before data

Plan: `plans/round-76.plan.md` (predicates, counters, kill rules, the frozen
kill matrix, controls and the C2 tuple table; plus the appended design-phase
correction 1 that repairs the committed evidence bytes). Base
`451ed5cb6d5f8c2bf4b3e10836e4634cfcb03ee0` (= `origin/master`, the round-75
non-author closure verdict commit). Declaration `5b7bbe1a`; design-evidence
repair `be4e7c86`. Round shape: one v1 wave, 12 seats (4 executor · 1 scribe ·
1 scout · 2 reviewer · 1 critic · 1 mutation-tester · 1 connector · 1
sentinel; attack seats 4 = 33.3 %), policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16. `labrat` is a frozen-topology
seat the validator rejects, so no labrat item exists; the planner seat stays
with the L1 per the orchestrator ruling.

- **R76-C1 — operability (verdict-only; sourced on the re-opened S006).** The
  two round-75 survivors become measured arms: `arm19-seatreports-printed-required`
  in `tools/wave-reconcile.py` (the seventh spec defect
  `adv-seatreports-require-printed-bypass` dies on arm19 only) and
  `ARM11_doc_rev_cli_binding` in `tools/selfstate-freshness.py` (the
  `--doc-rev-ignored` survivor dies on ARM11 only). Before: `18/18` and
  `10/10` with both survivors alive. After: `19/19` and `11/11`, battery
  `defects=7 killed=7`, five instrument mutants killed on their named arms.
- **R76-C2 — calibration (the lowest scored numeric axis at 8).** The selfstate
  population 17 → 20 rows: the two routed dated-literal capability cells
  (`six-leg content-disposition probe` `18/18` → `SELFTEST: PASS (19/19)`;
  `effective expectation reconciliation` `34/34` → `SELFTEST: PASS (66/66)`)
  and the round-17 line's `56/56` as a standing stale span row. Before:
  `SELFSTATE: rows=20 match=16 stale=4 unexpected=2` exit 1. After:
  `rows=20 match=18 stale=2 unexpected=0` exit 0, with the round-17 bash
  values (`95/95`, `cases=7`) disclosed as named gaps, never rows.

Capability to enter: none this round (no new capability row; the r75
settlement declined acquisition credit, so one capability-less completed
round sits inside the stagnation window N = 2; the nudge does not fire).

## Round 76 — measured claims (appended at the records commit, 2026-11-04)

Declaration `5b7bbe1a`; design repair `be4e7c86`; work commit `4af6695f`
(tool bytes, C2 cell repairs, SKILL registry rows; receipt
`.ufo/evidence/round-76/`). Receipts under `.ufo/evidence/round-76/`; the
round's report cites the tip.

| Claim | Verdict | After (measured) | Counting commands (live outputs in the receipts) | Measured commit |
|---|---|---|---|---|
| R76-C1 | verifies (measured) | `WAVE_RECONCILE_SELFTEST: 19/19 pass` exit 0; `SELFSTATE_SELFTEST: 11/11 pass` exit 0; battery `MUTATE: DONE (target=wave-reconcile-arms-r76 defects=7 killed=7 survived=0 inconclusive=0 kill-rate=100%)` with `CONTROL: GREEN` and byte-identical `MUTATE_RESTORE: OK` (target sha256 `ca05ec15…` = the landed bytes); the adv defect's frozen matrix row is the arm19 FAIL line `got=printed-none-reached-comparison` (`.ufo/evidence/round-76/c1-landed-battery.txt:75`); the five instrument mutants die on their named arms (`echo-doc-token` → ARM2 + disclosed ARM3/ARM9; `expect-ignored` → ARM2; `capability-absent-deflected` → ARM4; `zero-rows-success` → ARM6; `doc-rev-ignored` → ARM11 only; receipts `ss-mut-*-landed.txt`); arms 1–15 byte-identical base→landed (`c1-arms1-15-base.txt` vs `c1-arms1-15-landed.txt`, `cmp` empty) | `python3 -I -X utf8 tools/wave-reconcile.py --selftest`; `python3 -I -X utf8 tools/selfstate-freshness.py --selftest`; `bash tools/mutate-and-run.sh --target tools/wave-reconcile.py --defects tools/wave-reconcile-mutants.spec --suite 'python3 -I -X utf8 "$MUTANT" --selftest' --label wave-reconcile-arms-r76` | `4af6695f` |
| R76-C2 | verifies (measured) | `SELFSTATE: rows=20 match=18 stale=2 unexpected=0` exit 0 at the landing rev (`.ufo/evidence/round-76/c2-after-r76.txt`), the two repaired rows reading `measured_figure=19/19`/`66/66` from the pinned instruments' own stdout and the two stale-ok rows `r74-frozen-addr-six` + `r76-r17-evidence-disposition`; the 17-row base population re-runs green (`rows=17 match=16 stale=1 unexpected=0` exit 0, `c2-base17-at-landing.txt`); the landed manifest's rows[17:] canonical sha256 `14789e6a…` equals the critic's own transcription (`T76W1C1.md` §3) and the plan table | `python3 -I -X utf8 tools/selfstate-freshness.py --repo . --manifest tools/selfstate-freshness.json --doc-rev 4af6695f`; `python3 -I -X utf8 tools/selfstate-freshness.py --selftest` | `4af6695f` (repairs); after at `4af6695f` |

**No axis harmed.** depth 10, calibration 8 and freshness 9 unchanged as
numbers (the round records axis moves, not new scores). C1 and C2 are causally
separable as the critic re-verified from committed diffs (`T76W1C1.md` §4: C1
touches only `SELFTEST_ARMS`, two constants and the ARM11 block; C2 never
touches wave-reconcile or the spec; the `wave-record reconciliation` cell
repair is out-of-population, receipted, and outside both claims' counters).
Monitored edits this round: `SCORECARD.md`, `LOG.md`, `corpus/SOURCES.md`,
`corpus/QUALITY.md`, `SKILL.md`, `tools/registry.json` → forecast
`REKEY_COST sections=64 planned=6 at_risk=16 predicted_lost=16`
(`.ufo/evidence/round-76/rekey-cost-full-r76.txt`, pre-data); the rekey batch
and its receipts land in this round's final commits.

**Named carries to round 77.** The `adv-seatreports-require-printed-bypass`
and `--doc-rev-ignored` survivors closed; the round-77 list opens with the
mutation seat's new survivor: a recursion-removal mutant of the seat_reports
listing walk survives 19/19 and differs on a production-shaped listing
(127 reports → 0; `T76W1M1.md`) — the next arm needs a nested-listing fixture;
the two bash-instrument gaps (`95/95` → `107/107`, `cases=7` → `cases=10`)
stay routed until the selfstate runner widens beyond `python3 -I` scripts;
17 of the 44 `--selftest` tools still carry no `tools/registry.json` row
(`T76W1E4/registry-gaps.txt` names them); C1 wording notes (verify the adv
defect by its frozen matrix row, and C2's full summary line, not exit counts)
are recorded for the closure.

### Round 76 — appended: the rekey settlement (2026-11-04)

The block above's "one rekey batch" line measured out as **four** batches
(`r76-batch-1` 13 sections at `826d2fae`, `r76-batch-2` 4 at `beb0599b`
(after trace-restore `18cdc29f`), `r76-batch-3` 11 at `881ded79`,
`r76-batch-4` 3 at `b2b0f82a`; ledger 899 → 930). Monitor
`credited=65/65` at the landing tip `b2b0f82a`
(`.ufo/evidence/round-76/coldread-green-r76.txt`; red-before 48/65 at the
records commit). Two mined defects (the stale 2026-11-01 `rekey-plan.json`
the union-plan generator reads; the flat trace numbering that let b2
overwrite b1 receipts) and a third (`cp` over an edited plan) are recorded
in `corpus/lessons/round-76.md`; the corrected per-batch rebind script
(`--batch-tag`, `traces-<tag>/`, `rekey_round: 76` labels) is committed.

## Round 77 — declared claims and measured record (2026-11-04)

Plan: `plans/round-77.plan.md` (frozen at `d39be4b0`, predicates, counters,
kill matrix, control and `coldread_forecast` in that commit). Base
`ac6baf7a46df613b171b4c1ab834c888cd6321b9` (= `origin/master`, the round-76
non-author closure verdict commit). Round shape: one v1 wave, 12 seats
(4 executor · 1 scribe · 1 scout · 2 reviewer · 1 critic · 1 mutation-tester ·
1 connector · 1 sentinel; attack seats 4 = 33.3 %), policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16. `labrat` is a frozen-topology
seat the validator rejects, so no labrat item exists; the planner seat stays
with the L1 per the orchestrator ruling.

- **R77-C1 — operability (verdict-only; sourced on S305, opened this round).**
  The round-76 wave's recursion survivor becomes arm20 of
  `tools/wave-reconcile.py`. Before (base): `WAVE_RECONCILE_SELFTEST: 19/19
  pass` and the `git-listing-recursion-removed` mutant survives 19/19
  (`.ufo/evidence/round-77/base-survivor-r77.txt`). After:
  `WAVE_RECONCILE_SELFTEST: 20/20 pass` exit 0 and the battery
  `MUTATE: DONE (target=wave-reconcile-arms-r77 defects=8 killed=8
  survived=0 inconclusive=0 kill-rate=100%)` with `CONTROL: GREEN` and
  `MUTATE_RESTORE: OK` byte-identical (tool sha256 `67d3a4cc2e75…`),
  `.ufo/evidence/round-77/c1-landed-selftest-wr.txt` and
  `c1-landed-battery.txt`; every mutant dies on its frozen arm(s), the new
  defect on arm20 only, with `seat-reports-any-depth` → arm15 + arm20 as the
  plan's disclosed intrinsic collateral.
- **R77-C2 — calibration (the lowest scored axis at 8).** The cold-read credit
  the record claims is the monitor's reading at the revision the record names.
  Before (base): `COLDREAD_PORTABLE rev=ac6baf7a46df credited=63/65`,
  `sections_covered=63 sections_total=65 box3_full_page=false`, two
  uncredited headings (`## Standing rules`, `## Mutation-sweep recipe —
  numbered steps; bounded cold-read evidence`)
  (`.ufo/evidence/round-77/coldread-base-r77.json`). After: one settlement
  batch at the content tip `1d91c384` covering exactly the monitor's 14
  uncredited sections (ledger 930 → 944, `REBIND OK sections=14
  entries_added=14`), measured at the settlement commit `29a1a7d0`:
  `credited=65/65`, `sections_covered=65 sections_total=65
  box3_full_page=true` (`coldread-after-r77.json`). The round-76 sentence
  that named `b2b0f82a` as the landing tip is corrected append-only below.

**No axis harmed.** depth 10, calibration 8 and freshness 9 are unchanged as
numbers (the round records axis moves, not new scores). Standing instruments
at the content tip: `WAVE_RECONCILE: rows=6 met=6 unexpected=0` and
`SELFSTATE: rows=20 match=18 stale=2 unexpected=0`
(`.ufo/evidence/round-77/standing-sweep-wr-r77.txt`,
`standing-sweep-ss-r77.txt`). Round 77 enters no capability row (C1 is an arm
on an existing capability, C2 a settlement on an existing run-book), so the
stagnation nudge fires for round 78: that round should be a capability round.

**Correction of record for round 76 (append-only).** The round-76 blocks above
say `credited=65/65` "at the landing tip (`b2b0f82a`)"; `b2b0f82a` is the last
rekey batch of that round and the true tip is `ac6baf7a`, two record commits
later, where the monitor reads `63/65` with `box3_full_page=false`
(`.ufo/evidence/round-77/coldread-base-r77.json`). The round-76 `REBIND OK`
was true at its own pin; the record named that pin as the tip. Criterion 128
(`corpus/QUALITY.md`) captures the class, and the round-77 C2 settlement is
measured at the settlement commit it names.

### Round 77 — appended: wave disclosures and record corrections (2026-11-04)

Appended after the wave returned; the measured block above stands as written and
no frozen predicate is amended. Six disclosures, each from a committed seat
report under `.ufo/waves/round-77/w1/`:

1. **Stagnation nudge — off by one in the block above.** The block says "the
   stagnation nudge fires for round 78". Read against `AXES.md` §The stagnation
   nudge and `## Saturation` (line 8/10, window N = 2): rounds 75 and 76 are two
   capability-less completed rounds, so the window was already full at round-77
   start and the nudge was ACTIVE for this round (the lowest-axis obligation was
   waived; this round worked calibration anyway). It stays active for round 78,
   which should be the capability round. Wave critic `T77W1C1` raised it; the
   sentence above is superseded by this paragraph, append-only.
2. **C1's after-state is a set of guards, not one scalar.** The frozen claim
   carries 20/20, eight kills, control/restore and kill-set invariance; §9 asks
   for one re-derivable value. The one value the population yields is the
   surviving registered defects on the recursion surface: 1 at base (the mutant
   survives 19/19), 0 at the landing (the battery prints `survived=0`). The
   guards stay as frozen; the admission defect is the multi-value sentence.
3. **C2's counter measures the monitor, not the record's sentence.** The
   frozen counter re-derives `credited` and `box3_full_page` at the named
   revision; it does not parse `SCORECARD.md`/`LOG.md`, so "the record's claim
   and the monitor agree" is checked by a separate grep, not by the counter.
   Both halves are reported: the monitor half verifies (63/65 → 65/65 at
   `af754b92`), the record half is the correction paragraph above plus this
   block.
4. **Separability sentence corrected.** The plan says "Neither claim's counter
   reads the other's files". False for C2's counter: the cold-read
   `needed_paths` includes `tools/wave-reconcile.py` through a declared ledger
   pin (wave critic `T77W1C1` measured it). The claims are still each
   verifiable without the other's work landing — C2's predicate is attainable
   at any pre-rekey tip over whatever set the monitor reports — but the byte
   dependency exists and is disclosed.
5. **Named survivors for round 78** (wave mutation-tester and executor seats).
   `arm20`'s cleanup `finally` can be deleted with the suite still green
   (`T77W1M1`: 20/20 pass, one leaked `wave-reconcile-git-*` fixture per run) —
   the next arm needs a leftover-count post-condition and that edit as its spec
   defect. A `git-listing-uses-head` mutant (listing reads `HEAD` instead of
   the pinned rev) also survives all 20 arms (`T77W1E2`) — the next fixture
   needs two commits so HEAD ≠ rev.
6. **Provenance limitation (C2).** The monitor's decision code does not
   authenticate an entry's `read_rev`; a forged `read_rev` in a hand-edited
   ledger prints the same state (wave critic `T77W1C1`, in-memory probe). The
   claim's barrier is the producer receipt (`REBIND OK` + the trace files),
   which is producer evidence, not independent proof.

## Round 78 — declared claims and measured record (2026-11-04)

Plan: `plans/round-78.plan.md` (frozen at `c1c220d4`, predicates, counters,
kill rules, the frozen kill matrix and both do-nothing controls in that commit).
Base `5bcb13ea7cc08bb0b594fcd0c2bb770cb8fe64a0` (= `origin/master`, the round-77
non-author closure verdict commit). Round shape: one v1 wave, 12 seats
(3 executor, 1 scribe, 1 scout, 2 reviewer, 1 critic, 1 mutation-tester,
1 connector, 1 sentinel, 1 simplifier; attack seats 4 = 33.3 %), policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16. Saturation: depth 10,
calibration 8, freshness 9 all at or above the line 8; rounds 75, 76 and 77
entered no capability row, so the stagnation nudge was ACTIVE and this round is
the capability round.

- **R78-C1 — operability, capability acquisition (sourced on S306, opened this
  round).** A non-Python instrument can carry a live freshness row. Before
  (base): the runner executed every instrument under the hardcoded
  `python3 -I -X utf8` prefix, and the do-nothing control (base runner + the
  new manifest row) refused: `SELFSTATE error=setup
  figure-absent:mutation-runner-selftest` exit 2
  (`.ufo/evidence/round-78/c1-control-bash-row-on-base-runner.txt`); base sweep
  with the base manifest `rows=20 match=18 stale=2 unexpected=0` exit 0. After:
  a frozen interpreter tuple table (python default unchanged, bash added; an
  unknown name refused before any row effect) and the live row
  `mutation-runner-selftest` binding `MUTATE_SELFTEST: 107/107 pass` to
  `tools/mutate-and-run.sh --selftest` at the base revision →
  `SELFSTATE: rows=21 match=19 stale=2 unexpected=0` exit 0,
  `SELFSTATE_SELFTEST: 13/13 pass` exit 0
  (`.ufo/evidence/round-78/c1-landed-sweep.txt`, `c1-landed-selftest.txt`). The
  capability row above enters through this demonstration.
- **R78-C2 — coverage (sourced on S091, re-opened this round).** The two
  survivors the round-77 wave named become fixture coverage. Before (base):
  `WAVE_RECONCILE_SELFTEST: 20/20 pass`; the 10-defect spec on base bytes reads
  `MUTATE: DONE (target=wave-reconcile-base-control-r78 defects=10 killed=8
  survived=2 …)`, survivors exactly `git-listing-uses-head` and
  `arm20-cleanup-removed` (`.ufo/evidence/round-78/c2-base-control-battery.txt`).
  After: arm20 carries a leftover post-condition (`leak:<n>`), arm21 builds a
  two-commit fixture and measures at the pinned rev (HEAD ≠ rev) →
  `WAVE_RECONCILE_SELFTEST: 21/21 pass`; battery `CONTROL: GREEN`,
  `MUTATE_RESTORE: OK` byte-identical, `MUTATE: DONE
  (target=wave-reconcile-arms-r78 defects=10 killed=10 survived=0
  inconclusive=0 kill-rate=100%)` (`.ufo/evidence/round-78/c2-landed-selftest.txt`,
  `c2-landed-battery.txt`, per-defect streams `battery/`). Kill matrix as frozen:
  the eight base defects keep their arms except `git-listing-recursion-removed`,
  which now also fails arm21 (disclosed intrinsic collateral),
  `git-listing-uses-head` dies on arm21 only, `arm20-cleanup-removed` on arm20
  only.

**No axis harmed.** Arms 1–19 byte-identical between base and landed selftests;
the base 20 selfstate rows identical between base and landed sweeps; the bash
instrument unchanged (`MUTATE_SELFTEST: 107/107 pass` before and after).

**Planned (round 79):** the wave-named survivors and the connector's
assimilation verdict; the carried 17-of-44 registry rows and the bash-instrument
row widening for `selfstate`'s support-blob path stay carried unless a claim
slots them.

### Round 78 — appended: wave disclosures and record corrections (2026-11-04)

Appended after the wave returned; the measured block above stands as written and
no frozen predicate is amended. Seven disclosures, each from a committed seat
report under `.ufo/waves/round-78/w1/`:

1. **The declared C1 design carried a cache-key defect, and the fix's first
   shape violated the frozen count.** The row cache was keyed
   `(rev, path, argv)`; a `bash` row's stdout could satisfy a python-defaulted
   row on the same path/rev/argv (`T78W1R1` reproduced the bypass with an
   execution trace; `T78W1C1`, `T78W1E2` and `T78W1CN1` found it
   independently). The L1 fixed the key and first added a 14th arm; the
   reviewer voted FAIL because kill rule (iii) names `13/13` while the suite
   printed `14/14`. The L1 then folded the assertion into arm13
   (`ARM13_bash_interpreter_row_and_cache`) — same coverage, count unchanged —
   and the reviewer re-measured the final bytes and voted PASS. The pre-fold
   `14/14` state and the pre-fold FAIL vote are retained in the seat reports,
   not hidden. Receipts: `c1-cache-kill.txt` (mutant → `12/13`, arm13 FAIL),
   `c1-cache-kill-mutant.py`, `c1-landed-selftest.txt` (`13/13`); landed tool
   sha256 `ae53ac68fc6743edf36d7fc71d811fcb3c4d4776d1c17e3265ca4977b596c9f4`.
2. **The plan cited a receipt its declaration commit did not carry.** The
   `c2-base-control-battery.txt` path resolves only from the records commit
   (`git cat-file -e c1c220d4:…` exits 128, `T78W1C1`). The control was run
   before the freeze; its stdout landed later. `T78W1E3` re-ran the control on
   base bytes in a clone and reproduced `survived=2`, survivors exactly the two
   round-78 defects. Lesson `## Mistakes` 3.
3. **No-harm monitor coverage, restated.** The documented selftest diff covers
   arms 1–19; arm20's `meet` at base and landed is asserted separately; arm21 is
   new. The restated monitor is narrower and more exact than the plan's
   sentence, and it is stated as a correction, not as a widened rule.
4. **The separability sentence is too strong, corrected.** Neither counter reads
   the other claim's files, but both depend on `tools/mutate-and-run.sh`: C1's
   row reads its `MUTATE_SELFTEST` figure and C2's battery uses it as the
   harness. C1's sweep runs no `wave-reconcile.py` byte and C2's battery runs no
   `selfstate-freshness.py` byte.
5. **The nudge sentence contradicted itself.** The plan said "the lowest-axis
   obligation is not waived" while the nudge was ACTIVE. The nudge waives that
   obligation this round; C2 works coverage anyway because two axes were wanted.
6. **Both after-states are guard sets, with the natural scalar named.** C1:
   registered counter-defects surviving the interpreter/cache surface 1 → 0
   (the cache mutant survives the declared design `13/13`, dies `12/13` after
   the fold). C2: surviving registered defects 2 → 0. The remaining guards stay
   as frozen; the multi-value sentence is the plan's admission defect, as in
   round 77.
7. **Named survivors for round 79.** The leak detector is a nested closure and
   `return set()` survives 21/21 (`T78W1M1`, `T78W1SC1`) — the round's own new
   guard is unguarded; dropping `-I` from the python tuple survives; arm21's
   `HEAD != rev` self-guard removal survives. The scout's table adds 9
   selfstate and 11 wave-reconcile unprotected rules with a measured single-edit
   mutant each (`.ufo/waves/round-78/w1/T78W1SC1.md` §1) and a bounded 3-item
   data-walk; the connector reads the staged package as `Assimilation: none`
   with 8 id collisions between the registry and the staged set.

**No axis is harmed.** Arms 1–19 byte-identical between base and landed
selftests, arm20 `meet` on both, the base 20 selfstate rows identical, and the
bash instrument unchanged (`MUTATE_SELFTEST: 107/107 pass` at its pinned rev).

**Appended at the wave close (2026-11-04).** Two more wave findings changed the
landed bytes after the block above was written, and both are disclosed here:
the leak post-condition's shared-temp-dir scan was not concurrency-safe
(four concurrent `--selftest` runs on the pre-fix bytes fail 4/4 with a spurious
`leak:2`/`leak:3`; the per-fixture `os.path.exists(fix)` check passes 4/4,
receipt `c2-concurrency-prepost.txt`, battery matrix unchanged), and the
manifest note's "17 declared rows" count was stale against its 21 rows
(criterion 122; the count is removed). The simplifier's builder de-duplication
and the unguarded `isinstance(interp, str)` clause are named for round 79. No
frozen predicate is amended; the battery was re-run on the final bytes
(`defects=10 killed=10 survived=0`, `CONTROL: GREEN`, byte-identical restore).


## Round 79 — declared claims (2026-11-04), frozen before data

Plan: `plans/round-79.plan.md` (frozen at `92c00705`; predicates, counters,
kill rules, the frozen kill matrix and all three do-nothing controls in that
commit). Base `0cac8e4604e01ff2e2bc0813c745c99d928b5dd5` (= `origin/master`, the
round-78 non-author closure verdict commit). Round shape: one v1 wave, 12 seats
(3 executor · 1 scribe · 2 scout · 2 reviewer · 1 critic · 1 mutation-tester ·
1 connector · 1 sentinel; attack seats 4 = 33.3 %), policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16. `labrat` is a frozen-topology
seat the validator rejects, so no labrat item exists; the planner seat stays
with the L1 per the orchestrator ruling. Saturation: scored axes depth 10,
calibration 8, freshness 9; round 78 entered a capability row, so the
stagnation nudge does NOT fire and C1 works calibration (the lowest scored
axis).

- **R79-C1 — calibration, capability acquisition (sourced on S289, re-opened
  this round).** A receipt's recorded tool sha must exist in the committed
  bytes of a revision the receipt names. Before: the round-78 receipt
  population `receipts=12 bound=4 corrected=0 unbound=8` exit 1 (eight receipts
  name `6f532752…`, which does not carry their recorded `7edecba8…` /
  `f8071c8a…`). After: `tools/receipt-bytes-bind.py` + eight append-only
  `# measured_bytes_rev: 091d50e4…` correction lines → `receipts=12 bound=4
  corrected=8 unbound=0` exit 0, `RECEIPT_BIND_SELFTEST: 10/10 pass`; the
  capability row `receipt-bytes binding sweep` enters `## Capabilities`.
- **R79-C2 — coverage (sourced on S305, re-opened this round).** The two
  survivors the round-78 wave named become fixture coverage: the leftover
  detector's positive branch (arm22) and the pinned fixture's `HEAD != rev`
  refusal (arm23). Before (do-nothing control: landed tool minus the two arm
  registrations, suite 21/21): `defects=12 killed=10 survived=2`, survivors
  exactly `leak-detector-blind`, `head-guard-removed`. After:
  `WAVE_RECONCILE_SELFTEST: 23/23 pass`; battery `defects=12 killed=12
  survived=0` with `CONTROL: GREEN` and byte-identical restore.
- **R79-C3 — operability (sourced on S307, opened this round).** The selfstate
  runner's python tuple `-I` is load-bearing: arm14 measures
  `sys.flags.isolated` through the real CLI. Before (base bytes + the
  one-defect spec): `defects=1 killed=0 survived=1`. After:
  `SELFSTATE_SELFTEST: 14/14 pass`; battery `defects=1 killed=1 survived=0`,
  the mutant dying on arm14 only.

## Round 79 — measured claims (appended at the records commit, 2026-11-04)

Declaration `92c00705`; work commit `1f6709d0` (tools, specs, the eight receipt
corrections, the capability row; final receipts regenerated at the work commit
by `.ufo/evidence/round-79/gen-receipts-r79.py`). Round shape: one v1 wave,
12 seats (3 executor · 1 scribe · 2 scout · 2 reviewer · 1 critic · 1
mutation-tester · 1 connector · 1 sentinel; attack seats 4 = 33.3 %), policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16; 12 results, 0 dead seats.

| Claim | Verdict | After (measured) | Counting commands (live outputs in the receipts) | Measured commit |
|---|---|---|---|---|
| R79-C1 | verifies (measured) | `RECEIPT_BIND: receipts=12 bound=4 corrected=8 unbound=0` exit 0 at the work commit; `RECEIPT_BIND_SELFTEST: 10/10 pass` exit 0; the eight corrections are one inserted `# measured_bytes_rev: 091d50e4…` line each (`git diff --numstat` = `1 0` per file, zero deletions, every `# tool_sha256:` byte-identical); the false-correction control reads `unbound=1` `detail=bytes-rev-mismatch` exit 1; the capability row `receipt-bytes binding sweep` is in `## Capabilities` and its figure is a live selfstate row (`rows=22 match=20 stale=2 unexpected=0`) | `python3 -I -X utf8 tools/receipt-bytes-bind.py --repo . --root .ufo/evidence/round-78`; `python3 -I -X utf8 tools/receipt-bytes-bind.py --selftest` | `1f6709d0a00401658c2bff0a2f6818c810575fdf` |
| R79-C2 | verifies (measured) | `WAVE_RECONCILE_SELFTEST: 23/23 pass` exit 0; battery `MUTATE: DONE (target=wave-reconcile-arms-r79 defects=12 killed=12 survived=0 inconclusive=0 kill-rate=100%)` with `CONTROL: GREEN` and byte-identical restore; the do-nothing control (landed tool minus the two arm registrations) reads `killed=10 survived=2` with exactly `leak-detector-blind` and `head-guard-removed`; kill matrix as frozen (the ten base defects keep their arms; the two new mutants die on arm22 only and arm23 only) | `python3 -I -X utf8 tools/wave-reconcile.py --selftest`; battery command in `c2-landed-battery.txt` | `1f6709d0a00401658c2bff0a2f6818c810575fdf` |
| R79-C3 | verifies (measured) | `SELFSTATE_SELFTEST: 14/14 pass` exit 0; battery `MUTATE: DONE (target=selfstate-arms-r79 defects=1 killed=1 survived=0 inconclusive=0 kill-rate=100%)` with byte-identical restore; the mutant's FAIL set is exactly `ARM14_python_isolation_tuple`; the base-byte control reads `killed=0 survived=1` | `python3 -I -X utf8 tools/selfstate-freshness.py --selftest`; battery command in `c3-landed-battery.txt` | `1f6709d0a00401658c2bff0a2f6818c810575fdf` |

**No axis harmed.** Arms 1–21 (`wave-reconcile`) and arms 1–13
(`selfstate`) are byte-identical between the base and landed selftests; the
first ten spec defects keep their frozen kill sets; the standing sweeps read
`WAVE_RECONCILE: rows=6 met=6 unexpected=0` and `SELFSTATE: rows=22 match=20
stale=2 unexpected=0` (the base 21 rows identical plus the new
`receipt-bind-selftest` row); `MUTATE_SELFTEST: 107/107 pass` is unchanged.
The wave changed the landed bytes in six disclosed places (see
`corpus/lessons/round-79.md` §Wave findings) and every change was re-measured.

**Planned (round 80):** the wave-named survivors (`python-utf8-dropped`, the
scout's 18-row survivor shortlist) and the connector's assimilation verdict; the
carried 17-of-44 registry rows stay carried unless a claim slots them.

## Round 80 — declared claims (2026-11-04), frozen before data

Plan: `plans/round-80.plan.md` (frozen at `ae591d5a`; predicates, counters,
kill rules, the frozen kill matrix and the do-nothing controls in that commit).
Base `dd2b9e2c44df680174a829901829fe86a2185185` (= `origin/master`, the
round-79 closure and spot-check tip). Round shape: one v1 wave, 13 seats
(4 executor · 1 scribe · 2 scout · 2 reviewer · 1 critic · 1 mutation-tester ·
1 connector · 1 sentinel; attack seats 4 = 30.8 %), policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16. `labrat` is a frozen-topology
seat the validator rejects; the planner seat stays with the L1 per the
orchestrator ruling. Saturation: scored axes depth 10, calibration 8,
freshness 9; round 79 entered a capability, so the stagnation nudge does NOT
fire and C1 works calibration (the lowest scored axis).

- **R80-C1 — calibration.** The registry home's printed figures equal the
  instruments' figures. Before: `REGISTRY_BIND: rows=7 match=0 stale=5
  absent=2 error=0 unexpected=7` exit 1 (five stale rows for wave-record
  reconciliation and self-state freshness on both SKILL.md and
  `tools/registry.json`, plus the registry sweep row; two absent rows for
  `receipt-bytes binding sweep`). After: `rows=7 match=7 stale=0 absent=0
  error=0 unexpected=0` exit 0 and `REGISTRY_BIND_SELFTEST: 11/11 pass`; the
  capability row `registry-home figure binding` enters `## Capabilities`.
- **R80-C2 — coverage.** The four survivors the round-79 wave named become
  fixture coverage: selfstate arm15 (`ss-bom-strip`, both decode refusals),
  arm16 (`ss-cache-key-drops-argv`), arm17 (`python-utf8-dropped`, sourced on
  S308), wave-reconcile arm24 (`wr-record-unknown-root-check-removed`).
  Control batteries 0/3 and 0/1 on base bytes; landed `defects=4 killed=4`
  and `defects=13 killed=13` with `CONTROL: GREEN` and byte-identical restore;
  selftests 17/17 and 24/24.
- **R80-C3 — operability.** The receipt population covers the declared tree,
  design class included. Before `receipts=22` with no design field (seven
  round-79 design receipts invisible); after `receipts=29 bound=14 corrected=8
  design=7 unbound=0` exit 0 and `RECEIPT_BIND_SELFTEST: 13/13 pass`.

## Round 80 — measured claims (appended at the records commit, 2026-11-04)

| Claim | Verdict | After (measured) | Counting commands | Measured commit |
|---|---|---|---|---|
| R80-C1 | verifies (measured) | `REGISTRY_BIND: rows=7 match=7 stale=0 absent=0 error=0 unexpected=0` exit 0; `REGISTRY_BIND_SELFTEST: 11/11 pass`; the capability row `registry-home figure binding` is in `## Capabilities` and its figure is a live selfstate row | `python3 -I -X utf8 tools/registry-figure-bind.py --repo .`; `--selftest` | 01ca77cd1bdac3d991e0319644146ace3970b30d |
| R80-C2 | verifies (measured) | `SELFSTATE_SELFTEST: 17/17 pass`; `WAVE_RECONCILE_SELFTEST: 24/24 pass`; batteries `defects=4 killed=4 survived=0` and `defects=13 killed=13 survived=0`, `CONTROL: GREEN`, byte-identical restore; the kill matrix is the plan's (each new mutant on exactly its own new arm; defects 1–12 keep their arms) | the two selftest commands and the two battery commands in the plan | 01ca77cd1bdac3d991e0319644146ace3970b30d |
| R80-C3 | verifies (measured) | `RECEIPT_BIND: receipts=29 bound=14 corrected=8 design=7 unbound=0` exit 0; `RECEIPT_BIND_SELFTEST: 13/13 pass`; the `receipt-bytes-tree` registry row runs the whole-tree sweep | `python3 -I -X utf8 tools/receipt-bytes-bind.py --repo . --root .ufo/evidence`; `--selftest` | 01ca77cd1bdac3d991e0319644146ace3970b30d |

**Planned (round 81):** the two test-text survivors (`ss-bom-only`,
`wr-prefix`) stay named at the report/convention level; the design class's
open limits (64 KiB header window, trusted manifest argv) are documented, not
claims; the receipt alarm on a `design` receipt whose recorded sha exists in a
committed blob (it would be a measured-block orphan) is unbuilt.

## Round-81 erratum (D2): the round-80 C1 before-state live tokens

Round-81 erratum (D2): the round-80 C1 before-state live tokens are `24/24`
and `17/17` — the cited `.ufo/evidence/round-80/design/c1-before-sweep.txt`
prints them — not the `23/23` / `14/14` pair the round-80 report paragraph and
`plans/round-80.plan.md` state. The `23/23` / `14/14` figures belong to the
**base tool bytes** (`c2-base-*`/`c2-control-*` receipts, shas `ca8acdd9…` /
`d9336fcd…`); the declaration instrument ran against the candidate tools in the
declaration worktree. Status-neutral and append-only: the round-80 record above
is preserved as written and its cells stay flagged by the standing sweeps; the
round-80 C1 verdict is unaffected (the stale tokens `19/19` and `11/11` are
stale against either pair). Bound by `tools/defect-bind.json` row
`D2-before-tokens`.

## Round 81 — declared claims (2026-11-04), frozen before data

Plan: `plans/round-81.plan.md` (frozen at
`1b115ba038e3d3bffc1432e62bbe5eb422c81266`; predicates, counters, kill rules,
the do-nothing controls and the base receipts in that commit). Base
`56a0129fe9bfd0ce607290a36350e38ac4df9c72` (= `origin/master`, the round-80
closure and spot-check tip). Round shape: one v1 wave, 13 seats
(4 executor · 2 scout · 1 scribe · 2 reviewer · 1 critic · 1 mutation-tester ·
1 sentinel · 1 connector; attack seats 5 = 38.5 %), policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16. Saturation: scored axes depth
10, calibration 8, freshness 9; round 80 entered a capability, so the
stagnation nudge does NOT fire and C1 works calibration (the lowest scored
axis).

- **R81-C1 — calibration.** The round-80 closure's routed-defect register is
  bound to repo state: D1/D2/D4/D5/D6 (D3 is C2's) MEASURE `closed` under
  `tools/defect-bind.py`. Before: `DEFECT_BIND: rows=6 closed=0 open=6
  unexpected=6` exit 1. After: `rows=6 closed=6 open=0 unexpected=0` exit 0;
  selftest 11/11.
- **R81-C2 — freshness.** Every standing self-state row pins settled
  instrument bytes: before `SELFSTATE_PINS: rows=23 settled=20 stale=3`
  exit 1; after `settled=23 stale=0` exit 0 at the tip, the standing sweep
  green.
- **R81-C3 — coverage.** The suite's own assertion text is pinned
  (`ARM21_selftest_text_pin`, `arm25-selftest-text-pin`), so the two round-80
  test-text survivors die: before `defects=1 killed=0 survived=1` per tool;
  after `defects=5 killed=5` and `defects=14 killed=14`, both `CONTROL: GREEN`,
  byte-identical restore.

## Round 81 — capabilities entered

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| closure-defect bind | turn a non-author closure's routed-defect prose into declared rows whose state is measured over committed bytes (five probe kinds: tree-paths, tree-bytes, receipt-tokens, sources-cell, doc-contains), so "closed" is a count and not an assertion | `python3 -I -X utf8 tools/defect-bind.py --repo . --manifest tools/defect-bind.json` → `DEFECT_BIND: rows=6 closed=6 open=0 unexpected=0` exit 0; `--selftest` → `DEFECT_BIND_SELFTEST: 11/11 pass`; `.ufo/evidence/round-81/controls/c1-before.txt` (before: `open=6`) | round 81 |
| standing-pin audit | measure whether a standing sweep's declared population pins the instrument bytes the tip carries (`settled` = blob equality at pin vs tip), instead of trusting that a matching figure means settled bytes | `python3 -I -X utf8 tools/selfstate-freshness.py --repo . --manifest tools/selfstate-freshness.json --pin-audit --pin-rev HEAD` → `SELFSTATE_PINS: rows=23 settled=23 stale=0` exit 0; before `settled=20 stale=3` (`.ufo/evidence/round-81/controls/c2-before.txt`) | round 81 |
| selftest-text pin | pin a suite's own assertion text (digest of `inspect.getsource(selftest)` against a constant), so a weakened arm fails an arm instead of passing vacuously — the round-80 `ss-bom-only` / `wr-prefix` survivor class | `SELFSTATE_SELFTEST: 21/21 pass`, `WAVE_RECONCILE_SELFTEST: 25/25 pass`; batteries `defects=5 killed=5` / `defects=14 killed=14` with `CONTROL: GREEN`; base controls `killed=0 survived=1` per tool (`.ufo/evidence/round-81/controls/`) | round 81 |

## Round 81 — measured claims (appended at the records commit, 2026-11-04)

| Claim | Verdict | After (measured) | Counting commands | Measured commit |
|---|---|---|---|---|
| R81-C1 | verifies (measured) | `DEFECT_BIND: rows=6 closed=6 open=0 unexpected=0` exit 0; `DEFECT_BIND_SELFTEST: 11/11 pass`; each of the six rows prints its own `state=closed` detail (`.ufo/evidence/round-81/c1-after.txt`, `c1-selftest.txt`) | `python3 -I -X utf8 tools/defect-bind.py --repo . --manifest tools/defect-bind.json`; `--selftest` | `fc7ccfb7e9e4c64749fd453d420abb839bbe5bd8` |
| R81-C2 | verifies (measured) | `SELFSTATE_PINS: rows=23 settled=23 stale=0` exit 0; the standing sweep stays green (`SELFSTATE: rows=23 match=21 stale=2 unexpected=0`, exit 0); `SELFSTATE_SELFTEST: 21/21 pass` (`.ufo/evidence/round-81/c2-after.txt`, `c2-sweep.txt`, `c2-selftest.txt`) | `python3 -I -X utf8 tools/selfstate-freshness.py --repo . --manifest tools/selfstate-freshness.json --pin-audit --pin-rev HEAD`; the sweep and `--selftest` commands | `fc7ccfb7e9e4c64749fd453d420abb839bbe5bd8` |
| R81-C3 | verifies (measured) | `MUTATE: DONE (target=selfstate-arms-r81 defects=5 killed=5 survived=0 inconclusive=0 kill-rate=100%)` and `MUTATE: DONE (target=wave-reconcile-arms-r81 defects=14 killed=14 survived=0 inconclusive=0 kill-rate=100%)`, both `CONTROL: GREEN` and byte-identical `MUTATE_RESTORE: OK`; `SELFSTATE_SELFTEST: 21/21 pass`, `WAVE_RECONCILE_SELFTEST: 25/25 pass`; FAIL sets `ss-bom-only` → `ARM21_selftest_text_pin` only, `wr-prefix` → `arm25-selftest-text-pin` only (`.ufo/evidence/round-81/c3-landed-*.txt`) | the two battery commands of the plan; `--selftest` for both tools | `fc7ccfb7e9e4c64749fd453d420abb839bbe5bd8` |

**No axis harmed.** depth 10, calibration 8 and freshness 9 are unchanged as
numbers; the round's registry figures were refreshed (`REGISTRY_BIND: rows=7
match=7 stale=0 absent=0 error=0 unexpected=0`, exit 0), the standing sweeps
stayed green (`WAVE_RECONCILE: rows=6 met=6 unexpected=0`;
`RECEIPT_BIND: receipts=29 bound=14 corrected=8 design=7 unbound=0`;
`ADDRANGE: rows=11 met=11 unexpected=0`), and no SCORECARD row was lowered.

**Planned (round 82):** bind the three round-81 capability rows as live
selfstate rows (population 23 → 26, a claim of its own since it moves a frozen
number); the design-orphan alarm (a design receipt whose recorded
`design_tool_sha256` resolves to a committed blob) stays unbuilt and named; the
carried `arm19`/`arm20` multi-arm FAIL sets are evidence, not defects.

## Round-82 corrections — the round-81 closure's routed record defects (append-only)

Appended at the round-82 landing; the round-81 cells above are preserved as
written (the lane's append-only correction rule) and stay flagged where a
standing sweep pins them. The round-81 non-author closure
(`corpus/lessons/round-81-verifier-spotcheck.md` §6) routed six defects; these
paragraphs are the correction of record for its record items, and
`tools/defect-bind-r82.json` measures each as a row (the register is the
count, not this prose).

1. **Manifest-binding receipt (item 1).** The round-81 report's
   `git rev-parse 1b115ba0:tools/defect-bind.json = fc7ccfb7:…` equality no
   longer held: the manifest changed at the wave commit (D2's span extended;
   rows unchanged, no `expect` relaxed). Reissued at the round-81 measured
   commit in `.ufo/evidence/round-82/manifest-binding.txt`, which carries both
   blob ids and the delta; the round-81 predicate, population and kill rule
   are unchanged.
2. **Measured-claim pointers (item 2).** R81-C1's and R81-C2's evidence cells
   named the pre-wave receipts (`c1-after.txt`, `c2-after.txt`, recorded tips
   `e27f28e8`) while their measured-commit cell read `fc7ccfb7`. The tip
   receipts are `.ufo/evidence/round-81/final/c1-sweep.txt` and
   `.ufo/evidence/round-81/final/c2-pins.txt`; both are the ones this
   correction points at.
3. **Tip re-derivation (item 3).** The round-81 report's sentence "All three
   were re-derived at the lane tip `ccef5f1d` … identical outputs" had no
   committed receipt. The re-derivation is re-run and committed this round at
   `.ufo/evidence/round-82/tip-rederivation.txt`, naming the revision it
   measured.
4. **Capability placement (item 6).** The three round-81 capabilities now sit
   in the live `## Capabilities` repertoire table above, each bound by a live
   self-state row (R82-C2); the `## Round 81 — capabilities entered` table is
   preserved as the round snapshot it was.

## Round 82 — declared claims (2026-11-04), frozen before data

Plan: `plans/round-82.plan.md` (frozen at
`4005a48ac73a66c794ff8fd528e6926633fe2af3`; predicates, counters, kill rules,
the do-nothing controls and the base receipts in that commit). Base
`4dfc3181310088c2f32d51e87a4d82c047d05231` (= `origin/master`, the round-81
closure and spot-check tip). Round shape: one v1 wave, 13 seats
(4 executor · 2 scout · 1 scribe · 2 reviewer · 1 critic · 1 mutation-tester ·
1 sentinel · 1 connector; attack seats 5 = 38.5 %), policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16. Saturation: scored axes depth
10, calibration 8, freshness 9; round 82 enters no new capability row (it binds
existing ones), so the stagnation nudge does NOT fire and C1 works calibration,
the lowest scored axis.

- **R82-C1 — calibration.** The routed-defect register is content-bound: the
  six-row register measures `DEFECT_BIND: rows=6 closed=6 open=0 unexpected=0
  manifest=bound` at the declared revision, a manifest whose bytes differ from
  that revision is refused (exit 2, no row effect), and a path row reads the
  object's type and mode, so a directory or symlink cannot stand in for a
  regular file. Before (base instrument): the flag is unrecognized, the
  narrowed register reads `rows=5 closed=5` exit 0, a directory reads
  `state=closed`.
- **R82-C2 — freshness.** The three round-81 capabilities are live self-state
  rows: before `SELFSTATE: rows=23 match=21 stale=2 unexpected=0`; after
  `rows=26 match=24 stale=2 unexpected=0` and `SELFSTATE_PINS: rows=26
  settled=26 stale=0` at the tip.
- **R82-C3 — coverage.** The newest instrument's own assertion text is pinned:
  the single test-text mutant that survives at the base bytes
  (`defects=1 killed=0 survived=1`, suite `11/11`) is killed by
  `A14_selftest_text_pin`; the 5-defect battery reads `defects=5 killed=5
  survived=0`, FAIL set = A14 only.

## Round 82 — measured claims (appended at the records commit, 2026-11-04)

| Claim | Verdict | After (measured) | Counting commands | Measured commit |
|---|---|---|---|---|
| R82-C1 | verifies (measured) | `DEFECT_BIND: rows=6 closed=6 open=0 unexpected=0 manifest=bound` exit 0 at the measured revision; the same register with one row deleted, bound to that revision, is refused `manifest-rev-mismatch` exit 2 with no row effect; a `tree-paths` row naming a directory reads `state=open detail=not-regular-file:.ufo/evidence/round-81=040000` exit 1, and every kind reads through `blob_bytes`, so a directory or symlink doc/receipt is a setup refusal (the wave's reviewer D1); the manifest is read ONCE for both the binding and the parse (the wave's sentinel S1), the escaping-path check runs before that read, every git call carries `GIT_NO_REPLACE_OBJECTS=1` so a replacement ref cannot substitute the bytes the binding reads (the wave's executor E1), and the manifest itself must be a regular blob at the declared revision with its path not resolved through a symlink (the wave's critic C1); `DEFECT_BIND_SELFTEST: 14/14 pass`; the round's own register reads `rows=4 closed=4 open=0 unexpected=0 manifest=bound` (`.ufo/evidence/round-82/final/c1-bound.txt`, `c1-narrowed-refused.txt`, `c1-directory-open.txt`, `c1-selftest.txt`, `c-r82-register.txt`) | `python3 -I -X utf8 tools/defect-bind.py --repo . --manifest tools/defect-bind.json --manifest-rev HEAD`; the narrowed clone with the same flag; `--selftest` | `b37860b7bf95fe195359057ff24db7a4622d505c` |
| R82-C2 | verifies (measured) | `SELFSTATE: rows=26 match=24 stale=2 unexpected=0` exit 0 (the two `stale` rows are the declared red arms) and `SELFSTATE_PINS: rows=26 settled=26 stale=0` exit 0 at the tip; the three new rows each print `measured=match` with doc and measured figures identical — the named rows' lines are the discriminating evidence, since `rows=26` alone is reachable with fabricated rows (the wave's critic); deleting a row is NOT caught by these two commands (the wave's reviewer R2) (`.ufo/evidence/round-82/final/c2-landed.txt`, `c2-pins.txt`) | `python3 -I -X utf8 tools/selfstate-freshness.py --repo . --manifest tools/selfstate-freshness.json`; the same with `--pin-audit --pin-rev HEAD` | `b37860b7bf95fe195359057ff24db7a4622d505c` |
| R82-C3 | verifies (measured) | `MUTATE: DONE (target=defect-bind-arms-r82 defects=5 killed=5 survived=0 inconclusive=0 kill-rate=100%)`, `CONTROL: GREEN`, byte-identical `MUTATE_RESTORE: OK`; `db-a1-assertion-weakened` → `A14_selftest_text_pin` only; the manifest pair → `A13_manifest_rev_binding`; `db-tree-bytes-ignores-type` → `A12_regular_file_boundary` only; `db-regular-file-check-removed` → `A12` plus A2/A7/A10/A13 (that caller edit also disables the missing verdict, every failure genuine); the spec was re-derived once for the shared boundary (recipe step 1, substrate movement: the predicate line now also occurs in `blob_bytes`); at the base bytes the same text mutant survives (`defects=1 killed=0 survived=1`, suite `11/11`); the wave's two custom survivors (a non-commit `--manifest-rev`, the empty `--manifest-rev` guard) are pinned by the extended A13/A8 and their re-run reads `defects=2 killed=2 survived=0` (`.ufo/evidence/round-82/final/c3-battery.txt`, `c3-survivors.txt`, `controls/c3-before-mutant.txt`) | the battery command of the plan; the base control spec | `b37860b7bf95fe195359057ff24db7a4622d505c` |

**No axis harmed.** depth 10, calibration 8 and freshness 9 are unchanged as
numbers; the registry figures were refreshed and re-measured
(`REGISTRY_BIND: rows=7 match=7 stale=0 absent=0 error=0 unexpected=0`, exit 0,
7-row population unchanged — the `defect-bind-*` registry rows are NOT yet
monitored: named for round 83), the standing sweeps all exit 0
(`WAVE_RECONCILE: rows=6 met=6 unexpected=0`; `RECEIPT_BIND: receipts=29
bound=14 corrected=8 design=7 unbound=0`; `ADDRANGE: rows=11 met=11
unexpected=0`; `ARM_LIVENESS: rows=9 live=9 dead=0`; `COUNT_RECHECK: rows=7
met=7 unexpected=0`; `POINTER_RECHECK: rows=12 met=12 unexpected=0`;
`FIGURE_ATTRIBUTION: rows=3 met=3 unexpected=0`; `ANCHOR_DRIFT: rows=16 met=16
unexpected=0`; `MUTATE_SELFTEST: 107/107 pass`), and no SCORECARD score was
lowered.

**Planned (round 83):** bind the `defect-bind-selftest`/`defect-bind-sweep`
registry rows in `registry-figure-bind` (population 7 → 9) so the second copy
of the figures this round refreshed is measured, not trusted; give
`tools/selfstate-freshness.py` a `--manifest-rev` so a deleted row is refused
rather than counted (the wave's reviewer R2); carry the A12 type/mode class to
`tools/receipt-revision-gate.py` and `tools/receipt-bytes-bind.py` (the wave's
connector); refuse an unhashable/line-breaking row `id` (the wave's sentinel S2); the
`--manifest-rev` limit on a conversion-attribute path stays unmeasured (S294)
and needs an object-only comparison before it is claimed; the C3 limits
(module-level edits, the two-edit rewrite) stay declared and unclosed; the
design-orphan alarm remains unbuilt and named.
