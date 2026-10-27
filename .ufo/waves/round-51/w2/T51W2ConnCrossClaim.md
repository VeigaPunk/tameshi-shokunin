# T51W2ConnCrossClaim — C1–C3 cross-claim dependencies

## Axes and evidence boundary

Axes named in the frozen contract: calibration (lowest numeric axis, 8; C1 surface), depth (9; C2 target 10), freshness (9, monitor floor), plus operability (C3, non-numeric), coverage and adjacency (non-numeric). The move under review is not a scoring adjustment: it is preserving the three frozen claim predicates while exposing their actual dependency edges. Sources: `.ufo/evidence/round-51/contract.json:8-15,17-60`; predicates and counter definitions at `c1/measure.py:5-17`, `c2/measure.py:5-21`, `c3/measure.py:5-24`.

## Shared surface / causal separability

| Surface | Claims touching it | Causal relationship and consequence |
|---|---|---|
| `corpus/README.md` | C1 directly; C2 entry evidence | C1 requires append-only bytes and a correct last frontier table (`contract.json:22`; `c1/measure.py:13-14,172-196`). C2 separately requires its newly-added knowledge entry name occur in README bytes beyond BASE (`c2/measure.py:190-219`). Thus C2 source-row/entry work is a C1 input, not an independent content area. Append-only README can satisfy both; rewrite breaks C1 even if C2 sees the entry. |
| `corpus/SOURCES.md` | C1 directly; C2 source evidence | C2's source row must be `mined`, opened 2026-10-26, and list the new knowledge entry (`c2/measure.py:190-218`). C1 rejects `queued` with used-by, mined without used-by, or missing used-by paths (`c1/measure.py:147-168`). A truthful mined row with the entry path satisfies both; an inaccurate status or absent path poisons C1 while C2 may also fail sourced-entry. |
| `tools/mutate-and-run.sh` | C2 directly; C3 registry rows/runner selftest path | C2 adds tenth wired leg and requires ten-case regression pass (`contract.json:32-43`; `c2/measure.py:75-102,162-188,222-280`). C3 rows execute tool selftests in a clone; its predicate explicitly includes every selftest-bearing tool (`contract.json:49`; `c3/measure.py:102-114,160-184`). Runner changes are therefore coupled to truthful C3 metadata and runtime behavior, not merely C2. Frozen no-harm allowlist was widened to four hard-coded-panel tools as noted `contract.json:91-92` (amendment details truncated in normal view). |
| `SKILL.md` canonical `Gate/probe registry` and later subsection | C3 directly; cold-read re-key | C3 searches registry headings and rows, runs commands; it does not care that a file is mentioned elsewhere (`c3/measure.py:89-99,187-238`). L1 notes 18/30 tool names appear somewhere but only 12 are absent everywhere; canonical predicate still requires conforming rows in registry section (`integrate/l1-notes.md:5-16`). The registry edit drops that cold-read section unless re-keyed (`contract.json:65-66`). |
| Cold-read ledger/re-key | All content claims indirectly through edited inputs | C2 runner byte changes drop 19 sections and C3 registry edit drops the registry section; L1 must recompute and obtain a named reader per heading, then commit re-key receipts at the measured revision (`w1/T51ExecRekey.md:78-80,147-161`). This is a calibration safeguard, not proof of C1/C2/C3 predicates. |
| Fresh-clone fleet context | C2 regression; C3 every self-test | C2 runner makes read-only sibling repo symlinks to support its regression (`c2/measure.py:162-187`). C3's self-test clone does not supply sibling fleet repos. This distinction is decisive for the round21 tool row below. |

The contract's separability statement (`contract.json:60`) is only partial: each counter can be invoked separately, but C2's source artifacts feed C1, and C2's runner/runtime is tested by C3. The three predicates are independently measurable, not causally independent. No evidence supports merging predicates or letting one pass stand in for another.

## Claim-level before / after dependency graph

```text
BASE (CTL_0): C1 false (frontier_bad 10 + S022 conflict); C2 false (9 legs); C3 false (canonical rows insufficient)
     |
     +-- C2 candidate work: runner leg + embedded spec/sweep + knowledge entry
     |       |-- runner leg/sweep -> C2 wiring, pin, chronology, regression checks
     |       |-- knowledge entry -> C2 source: target path + S-id + README addition
     |       |                    +-> C1 SOURCES mined/used-by/path-exists checks
     |       +-- runner changed bytes -> C3 truthful runner row/selftest must still pass
     |
     +-- C1 candidate work: append corrected frontier table and mined S022 + C2 source row
     |       +-- README append preserves BASE prefix, and supplies C2 entry name
     |
     +-- C3 candidate work: registry rows -> truthfully named command, pins, scope and verdicts
             +-- registry section byte change -> cold-read re-key; does not cure tool failure

Final evaluation: C1 depends on append/table + all SOURCES consistency; C2 depends on all runner/sweep/source evidence; C3 depends on every tool's actual fresh-clone selftest and usage exit. Any one false remains a false claim even if the other two pass.
```

## C3 truthful row blocker — explicit contradiction, not repaired by prose

The frozen C3 predicate requires every row's selftest to exit 0 from a fresh clone at REV (`contract.json:49`; `c3/measure.py:18-21`). But the C2 counter's own regression implementation creates sibling fleet symlinks only for its regression clone (`c2/measure.py:162-176`), and the known truthful `tools/round21-measure.py --selftest` exits 1 in C3's fresh clone because its fixture expects sibling fleet repos (disclosed assignment fact; C3 test environment at `c3/measure.py:187-215`). Therefore a truthful C3 registry row for that tool cannot satisfy frozen C3 as currently specified. This is a contract/runtime inconsistency, not evidence permitting a fake command, shim, or false row. Unless underlying tool's real selftest is fixed within allowable scope (the assignment explicitly says no shim or lie; no-harm limits matter), C3 must fail honestly. C2 may independently pass while C3 fails; C1 may pass only if the shared new SOURCES row and README append are truthful and valid. Do not describe overall C1–C3 as jointly green from partial evidence.

## W1 attacks and calibration

C2 exact-suite result is reported as 2/10 killed; independent neutral-path experiments produce 5/10 by killing K_GONE_ARM, K_AMBIG_GT, K_SHAPE_OPTIN, hence those three are harness-masked rather than equivalent. This attacks interpretation of C2's sweep, but frozen C2 kill rule treats prediction misses as data and only checks receipt/provenance consistency (`contract.json:42-43`; C2 counter's `sweep_check` checks one verdict per defect and receipt structure, `c2/measure.py:134-159`). CritPrereg's provenance gap (suite only in prose; receipt consistency not suite provenance) and 15 surviving weakening mutants/forges mean a green C2 counter is not proof of mutation sensitivity or suite provenance. Keep those disclosures separate from the frozen predicate.

C3 W1 attack shows pure SKILL edit can forge rows and get counter pass, including `--help --selftest`; it also reports baseline existing rows are nonconforming (`w1/T51CritC3Counter.md:9-20,37-73,91-104`). This is a counter construct-validity limitation: C3's operational claim is not established merely by `C3_R51_PASS=true`. Conversely the truthful round21 row blocker means a faithfully described registry cannot pass. These are two distinct contradictions (counter admits false positive; predicate imposes an unsatisfiable truthful row in the stated clone context), not a reason to weaken or reinterpret the frozen rule.

C3 base narrative discrepancy is disclosed: 18 tools mentioned across subsections, only 12 absent anywhere; canonical-table measurement remains all 30 tools (`integrate/l1-notes.md:5-16`). Treat as claim-language overstatement, not a changed predicate. The 20 cold-read targets are computed dynamically; fixture headings/pointers are in `w1/T51ExecRekey.md:93-127`; real readers must verify candidate bytes and identify sections rather than reproduce fixture conclusions.

## Bounded move and verification

Move: use the round's own frozen dependency graph as a conjunctive closeout matrix: independently report each frozen counter outcome, then append explicit edges `C2 SOURCES -> C1`, `C2 runner -> C3`, and the C3 fresh-clone blocker; do not claim aggregate success from the separability sentence or a counter-only green result. This improves calibration and operability of the decision without changing any claim, axis, target, counter, or spec. Risks: may reveal expected C3 failure and prevent an attractive but misleading aggregate pass; no added code or altered measurement. Verification: at the deciding revision run frozen C1, C2 and C3 commands exactly as specified (`contract.json:25,38,52`), preserve raw outputs/exit codes, check C2's S-row through C1 and runner selftest through C3, and report C3 false if the truthful row still fails. Separately run cold-read refresh against actual candidate bytes and confirm all dynamically computed headings have named readers and precheck lost=0; do not treat re-key success as claim verification.