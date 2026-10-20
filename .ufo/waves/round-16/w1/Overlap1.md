# Overlap1 — sibling-overlap scan (round 16, routed defect 1)

Seat: Overlap1 (connector). Mode: read-only fleet scan; no sibling write, no gate edit, no mutant run.
Lane root: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (HEAD `28aeef498cc070c3183271b709bc79d344ff547a`, observed).
Fleet root: `/home/vgpnk/Projects/shokunin` (HEAD `0fb66cb26fa3083f8eef3d68680dea17f01fc8f7`, observed).
Scratch: `/tmp/tameshi-r16-Overlap1-EkZtYN`, `/tmp/tameshi-r16-Overlap1-sens-0vCv` (only writes outside the lane).
Round-15 defect this closes: "the named connector sibling-overlap scan has no credited completed output… Route the missing scan to tameshi next round" (`corpus/lessons/round-15-verifier-spotcheck.md:40`, `:159`).

## 1. What was scanned

tameshi's declared province (`PROVINCE.md:3-20,28-47`): verification-fixture craft — hermetic suites, mutation testing, fail-closed arms, verdict-line discipline, before/after proof; Core names sibling gates as read-only primary surfaces (kumitate, kagi, kaidoku, game lanes, tsukuroi, mado); Refuses every lane's gate code and product domain.

Scan target: every lane entry in `shokunin.conf` (SSOT for the roster), plus each lane's `PROVINCE.md` and `SKILL.md` (frontmatter description + claim text), plus the fleet-meta claim homes named by PROTOCOL (`PROTOCOL.md` §Gate standard; root `SCORECARD.md` registry sections for `protocol`/`aggregator`). `MANIFEST.json` was read read-only and compared, not trusted as roster (see F6).

## 2. Sweep and coverage proof

All commands below exit 0 unless noted. Run from `/home/vgpnk/Projects/shokunin`.

```
grep -cE '^[a-z0-9-]+\|[^|]+\|' shokunin.conf
# 23   (exit 0)
ls -d *-shokunin | wc -l
# 21   (exit 0)
for r in *-shokunin; do [ -f "$r/PROVINCE.md" ] && echo "$r"; done | wc -l
# 21   (exit 0)
python3 - <<'EOF'
import json,re
conf=set(re.findall(r'^([a-z0-9-]+)\|[^|]+\|',open('shokunin.conf').read(),re.M))
man={r['id'] for r in json.load(open('MANIFEST.json'))['roster']}
print(len(conf),len(man),sorted(conf-man))
EOF
# 23 13 ['aggregator','chousa','kotodama','mado','mori','protocol','souji','tabi','tameshi','tsukuroi']   (exit 0)
for r in *-shokunin; do echo "=== $r"; grep -n -m40 -E '^\*\*(Domain|Owns|Refuses)\*\*|^# |^## ' "$r/PROVINCE.md"; sed -n '1,25p' "$r/SKILL.md" 2>/dev/null | grep -n -E '^(name|description|---|# )'; done
# 21 blocks, 0 missing PROVINCE; SKILL.md absent in audio/game-dev-2d/game-dev-3d/revenger (0 files, exit 0)
grep -nE 'verif|verifier|test|mutat|fixture|gate|census|evidence|audit|check|selftest|hermetic|proof|calibrat|evaluat|fail-closed|determinis|ledger' */PROVINCE.md
# dense matches; the lanes with a verification-fixture interlock are in §4 (exit 0)
grep -rn -- 'tameshi' */PROVINCE.md */SKILL.md
# only 3 sibling lanes name tameshi: kotoba (PROVINCE.md:30), tsukuroi (PROVINCE.md:52; SKILL.md:554-568,706-707,1420,1474,1504), mado (SKILL.md:535,722-723,727,756,793,920,932,934-935,949,962,1267)   (exit 0)
for n in harness-integrity gate-evidence rlm-dispatch; do grep -c -- "$n" shokunin.conf; done
# 0 0 0   (grep exit 1 per zero-count search)
ls -l kumitate-shokunin/scripts/round-gate.mjs kagi-shokunin/corpus/surface-census.sh \
      kagi-shokunin/corpus/checklist-run.sh tsukuroi-shokunin/tools/tsukuroi-census.sh \
      mado-shokunin/tools/mado-verify.sh kengaku-shokunin/grader.py
# all 6 present (exit 0)
```

Coverage: 23/23 `shokunin.conf` lane entries have a row in §4. 21 have a physical repo and `PROVINCE.md`; `protocol` and `aggregator` are fleet-meta lanes on `.` whose claim homes are `PROTOCOL.md` and root `SCORECARD.md:177,234` (per `PROTOCOL.md:398-401`). The 3 lanes without `SKILL.md` (`audio`, `game-dev-2d`, `revenger`) were checked from `PROVINCE.md` only; 18 of 21 lanes have both files.

## 3. Frozen inputs (replay manifest)

`sha256sum` over every file this scan cited: 4 fleet-root files, 21 `PROVINCE.md`, 5 `SKILL.md` = 30. Recompute and diff to prove this report describes these bytes.

```
bfdf96c4feddb37a4411a750c706e5b53ecd1402153c53983e2bd4923614a3f8  shokunin.conf
870f8124ef2fc91a53f1d10c1aef474bd1b941182771002131070416b94f95f6  MANIFEST.json
886e459b2aa79b8198912ad54bd57fbb025cc424d78684a02fb3d4c832d4411a  PROTOCOL.md
54396be8a0b3565ba5b634d215e626e2d2761ed446419c5c4eb7515f190cf6ba  SCORECARD.md
a9a7f00d4fd9202f7c743aa9d003be0a708fef4c390735151f178aabf7b6f574  kumitate-shokunin/SKILL.md
9a237472b07f8e8cf5d8055bbccf42d0ad3428bbcf7dded210b4b44f2c9a421e  mado-shokunin/SKILL.md
2fe32af80644e57133df925faeaba4f36ce5fe5566b8a2ed6efbe69e65a9c54d  tsukuroi-shokunin/SKILL.md
c8b245b7dd2cfeb99855e968fb2cf778d820dcbcecd21195e320d5fa41eaa0fb  kotoba-shokunin/SKILL.md
97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580  tameshi-shokunin/SKILL.md
```

Per-lane `PROVINCE.md` digests (21):

```
20d881a694fe96b32e36b4c6e896a75936dd3da8c2cec63e5329b2ec5133c149  audio-shokunin/PROVINCE.md
cf7826a43aaab7c00708ab54bb46577217e7a67ab44a43a33e17ee2a58c1bbec  chousa-shokunin/PROVINCE.md
06b3c868274368ddf11542e1421381639cd6fc62ab74d32e77e31b2b068c0c45  game-dev-2d-shokunin/PROVINCE.md
dd8b032814479bdd6811f6b18fef814e21c5e35cbc3093814fa8d9531d8817ff  game-dev-3d-shokunin/PROVINCE.md
4a346e2df81f7b2e649914d0d99da974d6c484caf12fed1c6bd530d106a78523  kagi-shokunin/PROVINCE.md
369d8502fe7c0a756ac92d774f7f272be7f0b7a411056f007a423decf3d22111  kaidoku-shokunin/PROVINCE.md
650e65224fff95351a35f5c30755a77e8e8fe5bb2a9c3af5feab69610dac9a39  kake-shokunin/PROVINCE.md
a7728760f777573f9a4184df83efadc37fddc29159521c3ec48b11472579c0c6  kama-shokunin/PROVINCE.md
bfea62f21a4a54118fb82c1c3a0801b87d0ece37f6332f57ec3e803b581226e8  kasegi-shokunin/PROVINCE.md
ed1a0c8aaaf8b428cdd3837d260d27a83eef9229b4932a8b8359962b15e4f3c8  kengaku-shokunin/PROVINCE.md
c1fa9d97e4fe4798ea873cf2e80acac5f14f8c84b30036c927e1ae038b5fe524  kotoba-shokunin/PROVINCE.md
05b34a579c5d4f4ec78957cdedb658246ff292df3e21181c66186403f2b942d6  kotodama-shokunin/PROVINCE.md
fcd69667a1027d5edd07a8ff0390a716a467aff92719071e33cb6157673b665f  kumitate-shokunin/PROVINCE.md
c51cc6b29c52c737dbd19597557730a36e27660f6ff82f5b096bab147c62baab  lore-shokunin/PROVINCE.md
7aad7b863dc3c10b9fbafb8b04b7f73084adbdf91616a0859f7bfd4b0edb135a  mado-shokunin/PROVINCE.md
e6ed8cda7c51257afc0844c782a8380274873070602b8bd6f6bb6da36e08f0f9  mori-shokunin/PROVINCE.md
63acc3d033869f93f3e13da79e35023d86baa60b3f1d3b52861b019183b4b19f  revenger-shokunin/PROVINCE.md
835b42f9aca34f9f3c6769fafd04b125f34e2560778266d19c37957228237d2d  souji-shokunin/PROVINCE.md
16c27b12a60dbbcc43903d40334c314f6587bd8703d1e890e076398eac1a946a  tabi-shokunin/PROVINCE.md
3c67d81c481b7b8e1bb07b72bfba8a96ce993b0155ba72f7bcbb749f7309b634  tameshi-shokunin/PROVINCE.md
aeb7a5dd7a6c5e370d43c27c202d608830d369fea545943b2624d7ebe51d9523  tsukuroi-shokunin/PROVINCE.md
```

**Observed drift (recorded, not hidden).** Re-running `sha256sum -c` over the 30-line manifest later in the same session returned **29 OK / 1 FAILED**: `MANIFEST.json` changed from `870f8124…b94f95f6` to `c3092a97483597a3b85a80776790da8b55c53b390d7b0985753d78a3f8218a05` (live fleet ledger write during the wave). The two MANIFEST-dependent findings were re-checked at the new bytes and are unchanged: roster still 13 vs conf 23 with the same 10 missing ids, and `harness-integrity`/`gate-evidence`/`rlm-dispatch` still 0/0. This is exactly the freeze-then-drift case move M1 grades as a finding, not a failure.

## 4. Overlap matrix (one row per `shokunin.conf` lane)

Classification: **contested** = a claim conflict requiring an owner-side correction (never an ownership transfer); **complementary** = compatible ground with a named interface; **none-observed** = no verification-fixture interlock found.

| # | lane | their claim (path:line) | tameshi's claim (PROVINCE.md line) | class | report-not-absorb action |
|---|---|---|---|---|---|
| O-01 | protocol (fleet-meta) | `PROTOCOL.md:375-423` §Gate standard (verdict map, self-test, two evidences, registry home, scope, closure); `SCORECARD.md:177-195` protocol registry home + `closure-check`, `root-ledgers` gates | `:3-5` gate-craft domain, `:28-38` Core; does **not** cite §Gate standard | complementary | Cite §Gate standard as the outer interface in any tameshi gate advice; route standard changes to protocol, never edit `PROTOCOL.md`. |
| O-02 | aggregator (fleet-meta) | `shokunin.conf:21`; `SCORECARD.md:234` cross-lane quality, corpus review | `:20` out-of-province → report | complementary | This report is the routed artifact; no claim on aggregator review authority. |
| O-03 | kaidoku | `PROVINCE.md:5` evidence-first; `:61` evidence discipline row; `:115` verdict wording | `:10-11` owns audit-lane pattern (verify: lines, evidence ids) | complementary | Source lane for the pattern; keep existing `corpus/knowledge/verification-patterns-fleet.md` citation; no new claim without a recorded case. |
| O-04 | kasegi | `PROVINCE.md:29-30` claim gates/submission packaging; fail-closed validators in `SKILL.md:44,985` | none | none-observed | None. Product claim validation is not fixture craft. |
| O-05 | kengaku | `PROVINCE.md:19` `grader.py` exit 0/1/2, `--selftest` S0–S7, hermetic replay of four trees, "round-14 mutation test killed 4/4 fresh corruptions" | none (not in Core `:28-38`) | complementary | Do not cite its 4/4 as a tameshi measurement; a new tameshi case needs its own record and `SOURCES.md` row. |
| O-06 | kake | `PROVINCE.md:17-18` own gates `freshness-sweep.mjs`, `probe-delta.mjs`; publishing operator-gated | none | none-observed | None. |
| O-07 | kumitate | `PROVINCE.md:12-15` owns script/runtime surfaces + own instruments; `SKILL.md:589-605` **seven** gates with 0/1/2/64 maps; `SKILL.md:607-609` named gaps (no two-evidence frozen run; no revision in verdict line) | `:8-9` "`scripts/*` (six gates with selftest suites + mutation controls)"; `:30-31` Core names `kimi-census.mjs`, `claims-check.mjs`; runner leg table `tools/mutate-and-run.sh:84-89` | **contested (claim-level)** | tameshi corrects its own wording (see F1): seven gates; mutation controls are tameshi's, not kumitate's. No kumitate edit. |
| O-08 | kotoba | `PROVINCE.md:12-14` SKILL.md checklist craft + `verifiers/verify_skill_checklist.py` (`--skill PATH`, `--self-test`; argparse `:2097-2119`); `:30` names tameshi adjacent | `:44-47` adjacent "every sibling gate's code and product clauses"; C2 full-page cold-read (`SHONEN.md:9-10`; `corpus/QUALITY.md:43-46`) | complementary | C2's cold-read is **not** kotoba's checklist-fidelity instrument; if that verifier is run, name kotoba as owner and do not claim its standard (F4). |
| O-09 | kagi | `PROVINCE.md:46-53` 8 gates: `surface-census` (`--selftest` 16, `--verbs`/`--deep`), `drift-pins`, `transcript-scan`, `op-ref-probe` (36 cases), `checklist-run`, `scope-gate` (61 cases, `--falsify` 18/18), `claim-ledger` ("calibration gate", 97 cases), `sources-census` (47 cases) | `:9` `corpus/*check*.sh` + census gates; `:31-32` Core names `surface-census.sh`, `checklist-run.sh` | complementary | Keep only the two measured gates named; no claim on the other six; kagi's "calibration gate" refers to claim/citation cells, not tameshi's calibration axis. |
| O-10 | kama | `PROVINCE.md:10-14` probes `listeners`/`snapshot`/`check`, endpoint-consumer registry | `:18` refuses endpoint health (→ kama) | none-observed | None; probe-vs-gate distinction already matches `PROTOCOL.md:377-379`. |
| O-11 | lore | `PROVINCE.md:3` consistency verification; `:17` mechanical checks CM-01…CM-12, manual CM-09/CM-12 | none | complementary | None; lore's content-consistency checks stay lane-owned. |
| O-12 | revenger | `PROVINCE.md:3-7` evidence-ledger (observation/inference/unknown, Evidence IDs); `:22` refuses "harness/evidence auditing"; `:31-32` "does not take ownership of generic harness gates" | `:10-11` owns kaidoku audit pattern; `:14-17` refuses sibling gate code | complementary | The disclaimed generic-harness ground is tameshi's craft, but tameshi claims method only; do not merge revenger's ledger claim into tameshi's. |
| O-13 | tameshi | `PROVINCE.md:3-20,28-47` | same | self | n/a. |
| O-14 | mado | `SKILL.md:535` `mado-regression` gate: `MADO_VERIFY_HARNESS=/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh bash tools/mado-verify.sh --regression`; `:722-727` explicit `--target/--defects` use; `:932` harness "read-only — a needed change is a recommendation to tameshi, never a patch"; `:962` harness revision moved mid-round | `:32-33` Core names `tools/mado-verify.sh`, cites `tools/mutate-and-run.sh:84-89` | complementary + **interface coupling** | Runner v1 flag surface is a published interface (F2); C1's leg-7 edit must be additive. mado owns its default path and gate wrapper. |
| O-15 | tsukuroi | `PROVINCE.md:52` ADJ-07 routes "census blind spot raises a reusable verification/mutation-testing question" to tameshi; `SKILL.md:554-568` own-gate sweep via tameshi runner, tool pin r4-2 md5 `26a27d35…`; `:706-708` two-author sweeps of one artifact | `:32` Core names `tools/tsukuroi-census.sh` | complementary + **interface coupling** | Answer ADJ-07 with method advice only; never transfer gate ownership; the r4-2 pin is historical and must be re-hashed before quoting. |
| O-16 | tabi | `PROVINCE.md:12-13` "dynamic-page evidence patterns (what to capture so a claim about a page is re-verifiable)" | `:5` before/after proof | complementary | None; evidence-capture craft for browser claims is tabi's. |
| O-17 | mori | `PROVINCE.md:6-16` fleet observability, detection/report only | none | none-observed | None. |
| O-18 | chousa | `PROVINCE.md:5-8` source hierarchy, citation chaining, claim-vs-source verification | `:40-42` Frontier moves need a `mined` `SOURCES.md` row | complementary | Cite chousa's method; never restate it in tameshi's sources contract. |
| O-19 | kotodama | `PROVINCE.md:9-14` own gates, linguistic-cultural coupling | none | none-observed | None. |
| O-20 | souji | `PROVINCE.md:14-17` dry-run census + preservation ledger; `:56` "isolated write-safety fixture acquired r13"; `:78-80` evidence-integrity limited to own receipt fragments, "not … an independent promotion authority" | none | complementary | Souji's write-safety fixture and receipts stay lane-owned; no promotion authority crosses either way. |
| O-21 | audio | `PROVINCE.md:41` headless measurement battery (`fixture-battery`, `audio-checklist`, `threshold-calibration`); `:31` separate non-author verifier requirement | `:11` "the game lanes' verifier-AGREE loops" | complementary | `corpus/knowledge/verification-patterns-fleet.md:22` defines "game lanes = audio/g2d/g3d"; PROVINCE wording is ambiguous but corpus resolves it. Optional tameshi-side wording fix (R4). |
| O-22 | game-dev-2d | `PROVINCE.md:3` executable headless fixtures; `:10` refuses "harness/evidence auditing (harness-integrity, gate-evidence, rlm-dispatch)"; `:32-33` "generic harness/evidence audits → their owning lanes" | `:11` owns the game lanes' verifier-AGREE loops | complementary + **routed-stale-owner** | Refusal names do not resolve to a rostered lane (F3). Report to integrator/game lane; never edit its PROVINCE. |
| O-23 | game-dev-3d | `PROVINCE.md:3` headless fixtures; `:34-39` same refusal names; `:77-78` defers evaluation/RE | `:11` same | complementary + **routed-stale-owner** | Same as O-22. |

Summary: 23/23 lanes covered; **0 ownership contests**; **1 claim contest** (O-07); **2 routed stale-owner defects** (O-22, O-23); **2 cross-lane consumer couplings** (O-14, O-15); the remaining rows are complementary or no-overlap. Only 3 sibling lanes name tameshi at all (kotoba, tsukuroi, mado) — the rest do not know the craft exists, which is why the stale refusal names persist.

## 5. Material findings

**F1 — tameshi's kumitate parenthetical is wrong twice (contested claim).**
`PROVINCE.md:8-9` says kumitate provides "six gates with selftest suites + mutation controls". kumitate's own registry says **seven** gates: `SKILL.md:589` "All seven are gates", rows `:599-605` (`cite-check`, `surface-probe`, `round-gate`, `proxy-check`, `claims-check`, `kimi-census`, `sources-check`). `scripts/sources-check.mjs` was added at `kumitate-shokunin` commit `1a8eed5` 2026-10-19 19:41:02 -0300 — after tameshi's six-gate survey dated 2026-10-14 (`corpus/knowledge/gates-survey-kumitate.md:3`). On "mutation controls", tameshi's own survey contradicts the parenthetical: "no gate ships a kill-rate harness or fault injection against its own code"; only `cite-check` has a mutation copy and it is "integration-gated" (`gates-survey-kumitate.md:278-281` §7.1; cite-check's mutation copy at `:51-64`). The mutation controls live in **tameshi's** legs, not in kumitate's gates. This is exactly the kind of claim C2's full-page cold-read is supposed to expose; it is a tameshi-side correction only.

**F2 — `tools/mutate-and-run.sh` is a published cross-lane interface.**
mado's `mado-regression` gate defaults `MADO_VERIFY_HARNESS` to the absolute tameshi checkout (`mado-shokunin/SKILL.md:535`), invokes the explicit-target path (`:722-727`), and states the harness is read-only with changes travelling as recommendations (`:932`). tsukuroi records a runner pin (r4-2 md5 `26a27d35…`, `SKILL.md:568`). The runner's v1 surface is `Usage:` `:176-192` (`--target`, `--defects`, `--suite`, `--workdir`, `--label`, `--timeout`, `--tail`, `--regression`, `--selftest`) and the six-leg expectation table `:84-89`. C1's seventh leg (`js-round-gate`) is additive to that table; renaming a flag, changing an exit code, or altering the six recorded expectations would break two sibling gates' embedded use. Interface-critical for the L1 runner edit.

**F3 — game lanes' refusal names are stale owners.**
`game-dev-2d-shokunin/PROVINCE.md:10,32-33` and `game-dev-3d-shokunin/PROVINCE.md:34-35` refuse "harness/evidence auditing (harness-integrity, gate-evidence, rlm-dispatch)". `grep -c` for each name in `shokunin.conf` and `MANIFEST.json` → 0/0 (exit 1 per search). Those three names are not rostered lanes; the generic-harness ground they refuse is now tameshi's declared method. lore already shows the self-correcting pattern for a stale owner name (`lore-shokunin/PROVINCE.md:33`, `art-east-asian` → 0 in MANIFEST). tameshi reports; the game lanes own their text.

**F4 — kotoba owns the SKILL-checklist instrument; C2 must not conflate it.**
kotoba's Core includes `verifiers/verify_skill_checklist.py` with `--skill PATH` and `--self-test` (argparse `:2097-2119`; fixtures `:271,1528`), and it names tameshi adjacent (`kotoba-shokunin/PROVINCE.md:30`). C2's claim is different: a full-page **cold-read** earns box 3 where an Appendix A/B-only read cannot (`SHONEN.md:9-10`; `corpus/QUALITY.md:43-46`). Running kotoba's verifier would be a sibling-tool dependency, not a cold-read, and its `evaluated N` output is checklist fidelity, not oral-context executability. Cite or run read-only with kotoba named; never claim its standard.

**F5 — protocol owns the outer gate standard; kumitate's named gap is kumitate's.**
`PROTOCOL.md:375-423` fixes the gate/probe distinction, verdict map, self-test clause, two-evidences rule, registry home and closure consequence; root `SCORECARD.md:177-195` is the protocol lane's registry home with `closure-check` and `root-ledgers` rows. kumitate's named gap — "no gate yet ships the §Gate standard 'two evidences' frozen-snapshot run … and no verdict line names the revision it measured" (`SKILL.md:607-609`) — is a normative conformance gap in kumitate under that standard. Tameshi's "verdict-line discipline" (`PROVINCE.md:4`) can supply method advice, but the repair is kumitate's and the standard's text is protocol's.

**F6 — `MANIFEST.json` roster is not a complete roster.**
`shokunin.conf` has 23 lane entries; `MANIFEST.json` `roster[]` has 13, missing 10 entries (`aggregator`, `chousa`, `kotodama`, `mado`, `mori`, `protocol`, `souji`, `tabi`, `tameshi`, `tsukuroi`). Any future overlap sweep keyed on MANIFEST would silently drop tameshi itself. Key on `shokunin.conf:20-83`.

**F7 — prior overlap artifact had partial coverage.**
`.ufo/evidence/round-12/SiblingOverlap/overlap-mapping.json` names 9 distinct lanes across three boundary classes (engine flakiness: audio/g2d/g3d; product ownership: kumitate/kagi/tsukuroi/mado/tabi; secrets/health: kagi/kama) and is a boundary contract, not a per-lane claim scan. This report closes 23/23 with per-lane claim anchors.

## 6. Bounded recommendations (owner-side; tameshi does not edit siblings)

- **R1 (tameshi-owned).** In `PROVINCE.md:8-9`, replace "six gates with selftest suites + mutation controls" with "seven gates with selftest suites (`kumitate-shokunin/SKILL.md:589-605`); mutation controls are this lane's legs, not the gates'". Add `round-gate` to the Core name list at `:30-31` if C1 lands.
- **R2 (tameshi-owned, C1 precondition).** Make the C1 runner edit additive only: append `js-round-gate` after the six legs in `tools/mutate-and-run.sh:84-89` and the header note `:12-14`; do not change `:176-192` flags, the 0/1/2/64 mapping, or any of the six recorded expectations (F2).
- **R3 (integrator-routed).** Send O-22/O-23 to `game-dev-2d`/`game-dev-3d` as a stale-owner correction; tameshi makes no edit.
- **R4 (tameshi-owned, optional).** Clarify `PROVINCE.md:11` "game lanes" as audio + g2d + g3d, matching `corpus/knowledge/verification-patterns-fleet.md:22`.
- **R5 (next-round scan).** Re-run §2's commands and diff them against §3's manifest; a drift row is a finding, not a gate failure, and every drifted input must be re-read before its row is requoted.

## 7. One bounded move (round axes: depth + calibration)

**Move M1 — freeze this scan as a replayable census instead of prose.**

Evidence: the round-15 scan was credited but left no completed artifact (spotcheck `:40`), so its completion could not be distinguished from its absence. The fix is not a new gate; it is giving the scan the two-evidences shape tameshi already requires of gates (`PROTOCOL.md:390-397`): (1) the live run, and (2) a committed input manifest plus stable row IDs the next seat can replay. This report already carries both — 30 digests (§3) and rows O-01…O-23 — so L1 can commit them under `.ufo/evidence/round-16/Overlap1/` without a new registry row.

- Affected axes: **calibration** (primary — C2's box-3 evidence gains a machine-checkable, non-oral artifact, and the scan's 23/23 coverage becomes falsifiable); **depth** (secondary — one more recorded connector artifact for the method corpus). No harm to either: read-only, no sibling writes, no product gate, no ownership movement.
- Risks: (a) sibling trees drift every round, so a live re-run will legitimately differ — grade the frozen manifest, report live drift as a finding; (b) free-text rows can be silently reordered — the O-NN IDs exist to prevent that; (c) committing under `.ufo/evidence/` is within tameshi's write scope but L1 must confirm round-16's sealed-file policy before landing.
- Verification (observed, not assumed): `sha256sum -c` over the 30-line manifest returned 29 OK / 1 FAILED (`MANIFEST.json`, live ledger drift — see §3); the two MANIFEST-dependent checks re-ran unchanged at the new bytes; the count commands returned 23/21/21/18; appending a fake `tameshi` mention to a `/tmp` copy of one lane `SKILL.md` changes the cross-reference hit set (sensitivity check, not just green).

## 8. Limits and honesty

- All sibling repos were read read-only (`git show`/`sed`/`grep`); no checkout, write, stash or mutant run occurred; no mutant was run against `round-gate.mjs` (wave-1 rule respected).
- I did **not** execute any sibling gate or selftest; every sibling claim above is their text, not my measurement. Where I say a gate exists, I observed the file only.
- `PROVINCE.md` is the claim source per the assignment; `SKILL.md` was opened only where the province delegates detail (kumitate registry, mado/tsukuroi dependency, kotoba instruments).
- Unknown: whether `harness-integrity`/`gate-evidence`/`rlm-dispatch` are unwritten project names rather than dead lanes. Only roster absence is established.
- No tools installed or upgraded; no package transactions attempted.

## 9. Verification (commands and observed results)

```
# 1. input manifest (30 lines) and its replay
cd /home/vgpnk/Projects/shokunin
{ sha256sum shokunin.conf MANIFEST.json PROTOCOL.md SCORECARD.md; \
  sha256sum *-shokunin/PROVINCE.md; \
  sha256sum kumitate-shokunin/SKILL.md mado-shokunin/SKILL.md tsukuroi-shokunin/SKILL.md \
            kotoba-shokunin/SKILL.md tameshi-shokunin/SKILL.md; } > /tmp/manifest.sha256
wc -l < /tmp/manifest.sha256        # 30
# replay of §3's frozen manifest (not the just-generated one): 29 OK / 1 FAILED
#   MANIFEST.json — live fleet ledger write during the wave; counts re-checked unchanged (§3)

# 2. coverage counts
grep -cE '^[a-z0-9-]+\|[^|]+\|' shokunin.conf   # 23
ls -d *-shokunin | wc -l                          # 21
ls *-shokunin/PROVINCE.md | wc -l                 # 21
ls *-shokunin/SKILL.md | wc -l                    # 18

# 3. contested anchors
grep -n 'All seven are gates' kumitate-shokunin/SKILL.md            # 589
sed -n '599,605p' kumitate-shokunin/SKILL.md | grep -c '| gate |'   # 7
git -C kumitate-shokunin log --diff-filter=A --format='%h %ad' --date=iso -- scripts/sources-check.mjs
# 1a8eed5 2026-10-19 19:41:02 -0300
nl -ba tameshi-shokunin/corpus/knowledge/gates-survey-kumitate.md | sed -n '278,281p'
# 278  1. Corpus-wide, the only true mutation-testing style control is cite-check's
# 279     mutation copy (2372-2384) and it is integration-gated; **no gate ships a
# 280     kill-rate harness or fault injection against its own code** ...
# 281     `mutant|kill|mutation` across all six returns only cite-check's mutation

# 4. interface anchors
grep -n 'MADO_VERIFY_HARNESS' mado-shokunin/SKILL.md                 # 535, 920
grep -n 'read-only — a needed change is a recommendation' mado-shokunin/SKILL.md  # 932
grep -n 'mutate-and-run.sh:16-21,60' tsukuroi-shokunin/SKILL.md      # 568
sed -n '176,192p' tameshi-shokunin/tools/mutate-and-run.sh           # v1 flag surface
sed -n '84,89p'   tameshi-shokunin/tools/mutate-and-run.sh           # six-leg table

# 5. stale-owner names
for n in harness-integrity gate-evidence rlm-dispatch; do
  printf '%s %s %s\n' "$n" "$(grep -c -- "$n" shokunin.conf)" "$(grep -c -- "$n" MANIFEST.json)"; done
# each 0 0; grep exit 1
```

Every result above was observed in this session via these or equivalent commands (scratch paths differ); the manifest content is byte-identical to §3. Outputs quoted above are verbatim, truncated only where marked `…`.

Erratum (2026-10-20, appended): §2's sweep comment at :34 wrongly lists game-dev-3d among lanes lacking SKILL.md — `game-dev-3d-shokunin/SKILL.md` exists and is tracked (`git -C game-dev-3d-shokunin ls-files --error-unmatch SKILL.md` rc=0); the absent set is audio, game-dev-2d, revenger (3 lanes), so 18/21 lanes carry SKILL.md, consistent with :47 and §9, and no §4–§9 row depends on the erroneous comment.
