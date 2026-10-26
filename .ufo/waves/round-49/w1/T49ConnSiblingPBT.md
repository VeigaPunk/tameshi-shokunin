# T49ConnSiblingPBT — sibling-overlap scan for C2 (F10 PBT generators)

Seat: T49ConnSiblingPBT (connector, leaf). Date: 2026-10-26. Read-only scan; no edits outside this file.
Tooling installed/updated: none (all checks were fleet read-only greps/lists).
Scratch: none needed — no counter runs, no fixture clones.
Hygiene: did not read `~/.local/state/`; did not open `c2-WITNESS.stdout` / `c2-CTL_FIX.stdout` / `c2-CTL_ABSENT.stdout` (item does not name them).

Scope of the scan: the 20 sibling lanes at `/home/vgpnk/Projects/shokunin/*-shokunin/` (tameshi excluded as self), for (a) SOURCES rows holding QuickCheck (DOI 10.1145/351240.351266) or Smallbone, and (b) property-based-testing / generator / QuickCheck / Hypothesis / fuzzing ground.

## 1. SOURCES rows for QuickCheck or Smallbone in sibling lanes: NONE

Exhaustive greps over all 20 sibling lanes, every file type, excluding `.git`:

- Command: `grep -rn "351240\|smallbone\|lic\.pdf\|quviq" <each sibling lane>` → the only hits are false-positive numeric substrings: `audio-shokunin/corpus/live/r89-reverify/runs/cot-r1-t2.receipt.json:932` and `cot-r1-t3.receipt.json:928` (pipewire nanosecond timestamps containing "351240"), and `souji-shokunin/census/round-6/seat-73.json:198451` (`"i": 351240`, a census integer). No DOI, no Smallbone, no Quviq anywhere in siblings.
- Command: `grep -rn "QuickCheck" <20 sibling lanes>` → zero hits.
- Command: `grep -rln "Hypothesis" <20 sibling lanes>` → only `audio-shokunin/corpus/live/*` scientific-hypothesis probes (e.g. `audio-shokunin/corpus/live/r73-reviewer/mpv_seekability_causal.py`, `r77-boundary/p1c_mechanism.py`, `r83-critic/probe_onset_hole.py`) — audio-causal hypotheses, not the PBT library.
- Command: `for d in …/*-shokunin/; do grep SOURCES.md files for 'quickcheck|smallbone|351240|joss.01891|property-based|pbt'` → zero rows in any sibling registry. `kengaku-shokunin/corpus/SOURCES.md:67` holds the nearest neighbour, **S045 evalmut 0.1.0** (grader equivalent/defect mutation tool — mutation-testing ground, not PBT).

Where QuickCheck/Smallbone actually live (all tameshi-side, consistent with seat T49ScoutSrcHypothesis):
- Staged for adoption this round in the read-only merge package `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md`: S182 = QuickCheck (Claessen & Hughes, ICFP 2000, doi 10.1145/351240.351266) and S183 = Smallbone (Chalmers TR 76L 2011, smallbone.se/papers/lic.pdf); both to be renumbered (ids collide with held S157–S160) and `opened 2026-10-26` to satisfy contract `sourced`.
- Held tameshi F10-adjacent rows at base: S018 Hypothesis API reference (`tameshi-shokunin/corpus/SOURCES.md:29`), S019 Goldstein et al. ICSE 2024 (`:30`), S020 de Oliveira et al. EMSE 2026 (`:31`), S021 Maaz et al. arXiv (`:32`), S046 pbt-bibliography rejected (`:55`), JOSS Hypothesis lead at `:278` (a Leads bullet, never evidence per `:273`).
- Prior mapping: `tameshi-shokunin/.ufo/waves/round-46/w1/ConnPackageCross.md:34` already tabled the F10 package (S157/S170/S182/S183/S166/S199); this scan re-verifies it from the sibling side.

## 2. Sibling PBT / generator / fuzzing ground (held vs round artifacts)

Held ground = corpus README frontier rows, corpus/knowledge entries, tools/. Everything found in siblings is either a one-off `.ufo/waves` artifact or an unrelated sense of "generator"/"hypothesis":

| lane | artifact | kind | contested? |
|---|---|---|---|
| mado-shokunin | `.ufo/waves/round-41/w1/ExecDiffFuzz/fuzz.py` + `fuzz-receipt.txt` + `fuzz-summary.json` | differential mutation fuzz of mado's own C1 counter: 4843 mutants, byte-exact rc/stdout comparison, 0 disagreements; also `round-20/w2/AdvCrash/fuzz_eval.py`, `fuzz_deep.py` | nearest practice; round artifact, not corpus ground (`grep -ni 'fuzz|property-based|quickcheck|hypothesis' mado-shokunin/corpus/knowledge/ mado-shokunin/corpus/README.md` → no hits) |
| kagi-shokunin | `.ufo/waves/round-28/retained-probes/KagiR28.FObserveAnchor/fuzz.py` | version-token fuzz probe (no network) | round artifact |
| kaidoku-shokunin | `.ufo/waves/round-39/w1/artifacts/R39C1IndepReader/generator-probes.py` | measured limits of its squashfs fixture builder | round artifact |
| kumitate-shokunin | `.ufo/waves/round-63/build/K63SimplifyTool/fuzz-ready.mjs`, `fuzz-untested-arms.mjs`, `fuzz-ready-refutation.txt` | differential fuzz over gate CLI | round artifact |
| kengaku-shokunin | `.ufo/waves/round-29/scratch/falsify/FReviewDiff/fuzz.py`, `fuzz2.py`; `round-28/scratch/…/M04_fuzzy_any_elements.py` | scratch fuzz + a mutant file named "fuzzy" | scratch/round artifacts |
| kengaku-shokunin | `.ufo/waves/round-36/build/R36PlanNext.md:154` | names "property-based mutation testing (TU Wien)" as a search-summary lead, explicitly **not opened** by that seat | lead only |
| revenger-shokunin | `corpus/fixtures/firmware-r63/generator.py`, `corpus/fixtures/apk-r65/generator.py` (command: `head -25 …/generator.py`) | held corpus **fixture builders**, deterministic — not property-based | held, different craft object |
| mori-shokunin | `corpus/README.md:349` FR9 "Durable fixture evidence … retain a reproducible fixture generator and digest before making replay claims" (command: `sed -n '340,360p' mori-shokunin/corpus/README.md`) | held frontier row — durable-evidence discipline for host audits | held, different craft object |
| kotoba-shokunin | `.ufo/round-45/evidence/h11/census-generator-v10.py`; `corpus/README.md:21` "generator bugs" in a prompt-artifact resolvability sweep | round artifact + unrelated mention | no |
| kotodama-shokunin | `.ufo/waves/round-59/control/CtlOffTopicEcho59/echo-generator.py` | round control fixture generator from off-topic prose | no |
| souji-shokunin | `census/round-9/seat-09-generator.py` | round artifact | no |
| tabi-shokunin | `.ufo/waves/round-32/w2/CritForgeryRecheck/artifacts/forged-transcript-generator.mjs` | round artifact | no |
| tsukuroi-shokunin | `.ufo/waves/round-41/w1/C2RevPA8b/fuzz.txt` | differential-invariant probe receipt ("pairs tested: 2300 failures: 0") | round artifact |
| chousa-shokunin | `corpus/knowledge/dead-zone-pcre-r34.md`, `corpus/lessons/round-24.md:76`, `round-34.md:97`, `corpus/README.md:1005,1047` | natural-language "hypothesis" (planned-vs-measured discipline) | no |
| audio-shokunin | `corpus/live/r7*/…`, `r8*/…` | scientific hypotheses about audio playback | no |
| game-dev-3d-shokunin | `corpus/README.md:184` `NavigationMeshGenerator` | engine baking, unrelated | no |
| kengaku-shokunin | `corpus/README.md:466-467` generator/profile manifest | WebArena config projection, unrelated | no |
| kotodama-shokunin | `corpus/README.md:382,391,417` "generation engines" | mythology-grammar generators, unrelated | no |
| kake-, kama-, kasegi-, lore-shokunin | — | no PBT/generator/fuzz hits beyond prose | no |

Discovery commands (reproducible): `find … -name '*fuzz*' -o -name '*quickcheck*' -o -name '*pbt*' -o -name '*generator*' -not -path '*/.git/*'` per lane; `grep -rni 'fuzz\|property-based\|quickcheck\|hypothesis' <lane>/corpus/README.md`.

## 3. Contested scope (adjacency: report, never absorb)

- **No sibling lane claims PBT-generator ground.** `grep -rni 'quickcheck|smallbone|351240|hypothesis|property-based|pbt|fuzz' <20 sibling PROVINCE.md files` → zero hits. No frontier row in any sibling registry covers property-based generators.
- The nearest methodological neighbours — mado's differential mutation fuzz (`mado-shokunin/.ufo/waves/round-41/w1/ExecDiffFuzz/fuzz.py:1-22`) and kumitate's gate differential fuzz (`kumitate-shokunin/.ufo/waves/round-63/build/K63SimplifyTool/fuzz-ready.mjs:1-7`) — are ad-hoc seat artifacts inside their own rounds, never promoted to held `corpus/knowledge/` method entries or README frontier rows. They do **not** contest F10: nobody holds it.
- Under `tameshi-shokunin/PROVINCE.md:44-46` (**Adjacent** — "report, never absorb: every sibling gate's code and product clauses (owner lane)") these artifacts stay mado/kumitate property; tameshi's C2 generator must be built on tameshi's own named gate (`tools/staged-id-guard.py`) and tameshi's own opened SOURCES rows, not on sibling fuzz harnesses.
- mori FR9 (`mori-shokunin/corpus/README.md:349`) and revenger's fixture builders overlap only in the word "generator" (durable-evidence / deterministic builders vs property-based random generation with an oracle). Adjacent, not contested.

## 4. Is F10 tameshi ground by PROVINCE.md? — YES (frontier ground)

- `tameshi-shokunin/PROVINCE.md:40-42` (**Frontier** clause): "Frontier — F1–F10 in `corpus/README.md` `## Frontier`; ground moves to Core only through an admitted, source-headed `knowledge/` entry whose `source:` cites a `mined` `SOURCES.md` row."
- `tameshi-shokunin/corpus/README.md:87`: `| F10 | PBT generators for gate fixtures | S018, S019, S020, S021 | open | no PBT fixture method → one generator against a named fixture gate |` — the row sits in `## Frontier` (header at `:68`, verified `grep -n '^## Frontier' corpus/README.md`).
- Contract C2 (`contract.json` claims.C2) is exactly the open→held move on this row, with QuickCheck (staged S182) and Smallbone (staged S183) re-opened 2026-10-26 from the read-only merge package; the pilot entry `corpus/knowledge/pbt-generator-pilot.md` must cite a row `opened 2026-10-26`, and README must mark F10 held (round 49).
- Sibling scan confirms no competing claim: F10 is uncontested tameshi frontier ground.

## Summary

- No sibling lane holds any SOURCES row for QuickCheck (DOI 10.1145/351240.351266), Smallbone, Hypothesis-the-library, or any PBT source; only numeric/prose false positives (audio JSON receipts, souji census integer).
- Sibling fuzz/generator practice exists only as one-off `.ufo/waves` artifacts (mado r41 differential fuzz 4843 mutants/0 disagreements; kagi r28; kaidoku r39; kumitate r63; kengaku r29; kotodama r59; souji r9; tabi r32) — none promoted to held corpus ground.
- Held-but-different craft objects: mori FR9 durable fixture-generator evidence (`mori-shokunin/corpus/README.md:349`) and revenger's deterministic fixture builders (`corpus/fixtures/{firmware-r63,apk-r65}/generator.py`).
- Contested scope: none. Per tameshi PROVINCE.md:44-46 sibling artifacts are Adjacent — report, never absorb; C2 builds on `tools/staged-id-guard.py` alone.
- F10 is tameshi frontier ground by PROVINCE.md:40-42 via `corpus/README.md:87`; no sibling PROVINCE.md contests it.
- QuickCheck/Smallbone rows are staged (not held) in read-only `shokuknow/merge/tameshi/SOURCES.append.md` (S182/S183 → renumber, e.g. S269/S270, opened 2026-10-26) — matches T49ScoutSrcHypothesis.md.
- No tools installed; no counter runs; no scratch created; hidden C2 panel and control stdout files untouched.
