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
