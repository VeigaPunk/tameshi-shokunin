seat: T46ExecDrill
item: dry re-run (seat check, never a verdict) of the C2 and C3 counters, the seven controls, the three counter selftests and `no-harm.sh` at the CONTENT revision `6f2168e028ce7ff6e82ac92093ac05dd1f147c32`, plus the frozen-file diff against the freeze `745a583181648cfc7f9c1b476cd1be7dc68f7433`; C1 deliberately not run (L1's deciding run).

## Bounds and scratch

- Read-only on the lane checkout except this report. No `git add/commit/stash/checkout/switch/reset/pull/push`, no `jj`, no write to `/home/vgpnk/Projects/shokunin` or `/home/vgpnk/Projects/shokuknow`.
- Scratch: `/tmp/tameshi-r46-T46ExecDrill/` (`c2-hardened.out/.err`, `c3.out/.err`, `controls.out/.err`, `noharm.out/.err`, `census.out/.err`, the three extracted snapshots, `quote_check.py`, `fresh_quotes.py`).
- Lane `git status --porcelain` before and after my work shows only other seats' files (`w2.ready`, `w2.ready.dispatched`, `w2/T46ExecLive.md`, `w2/T46RevGate.md`) and this report. Lane `HEAD` at run time: `eada0b36d4c9e6380d111d2037acd97cdf91d2eb` (wave-2 spec), which is a descendant of CONTENT; `git diff --stat 6f2168e HEAD` touches only `.ufo/waves/round-46/{spec-w2.json,w2-dispatch.json,w2/swarm-registry.json}` (1283 insertions, 0 deletions), i.e. no control input differs between the working tree and CONTENT.
- No tool install or upgrade was made; no pacman transaction.

## 1. C2 — hardened mutant driver (dry re-run, not the deciding receipt)

```
$ cd /tmp/tameshi-r46-T46ExecDrill
$ python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-46/hardening/mutate.py \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 6f2168e028ce7ff6e82ac92093ac05dd1f147c32 --targets hardened
PRISTINE freshness pass VERDICT: PASS
EQUIVALENCE freshness 1
MUTANT freshness F01..F15 mutant killed          (15 lines, all killed)
MUTANT freshness FN1..FN3 neutral survived       (3 lines)
PRISTINE coverage pass VERDICT: PASS
EQUIVALENCE coverage 1
MUTANT coverage C01..C10 mutant killed           (10 lines, all killed)
MUTANT coverage CN1..CN3 neutral survived        (3 lines)
C2_R46: self_pin=1 targets=hardened declared=25 killed=25 survived=0 inapplicable=0 neutral_killed=0 pristine=1 equivalence=1 rev=6f2168e028ce7ff6e82ac92093ac05dd1f147c32 C2_R46_PASS=true
EXIT=0        (wall 6.51 s)
```

Full output: `/tmp/tameshi-r46-T46ExecDrill/c2-hardened.out` (33 lines, no `SURVIVORS` line). The driver reads every target, the manifest and its own bytes with `git -C LANE show REV:path` (`mutate.py:44-45,104-127`), so this run is genuinely at CONTENT and not at the working tree. `mutants.json` declares 31 entries: freshness 15 `mutant` + 3 `neutral`, coverage 10 `mutant` + 3 `neutral` (enumerated from `manifest['groups']`), i.e. `declared=25` matches the manifest.

## 2. C3 — coverage counter (dry re-run, not the deciding receipt)

```
$ python3 .../.ufo/evidence/round-46/coverage/measure.py \
    --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
REFUSED corpus/knowledge/*.md no provenance trio   (23 lines, same set as at the freeze)
ENTRY corpus/knowledge/r5-undetected-flaky-failures.md
ENTRY corpus/knowledge/r6-flaky-failures-cluster.md
ENTRY corpus/knowledge/r9-false-red-rate.md
C3_R46: self_pin=1 rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260 rev=6f2168e028ce7ff6e82ac92093ac05dd1f147c32 C3_R46_PASS=true
EXIT=0
```

Full output: `/tmp/tameshi-r46-T46ExecDrill/c3.out`. The counter reads the registry, the entries, the README, the snapshots and the package copies through `git show` / `git ls-tree` at `rev` (`measure.py:82-93`).

## 3. Controls (do-nothing and cheapest-cheat)

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
$ python3 .ufo/evidence/round-46/control/run-controls.py
CTL_A_package_byte_exact rc=1 C3_R46: self_pin=1 rows=3 entries=0 indexed=0 covered=0 row_ids=S258,S259,S260 rev=HEAD C3_R46_PASS=false
CTL_B_relabel_header_only rc=1 C3_R46: self_pin=1 rows=3 entries=0 indexed=0 covered=0 row_ids=S258,S259,S260 rev=HEAD C3_R46_PASS=false
CTL_C_rows_only rc=1 C3_R46: self_pin=1 rows=3 entries=0 indexed=0 covered=0 row_ids=S258,S259,S260 rev=HEAD C3_R46_PASS=false
CTL_D_wrong_digest rc=1 C3_R46: self_pin=1 rows=0 entries=0 indexed=0 covered=0 row_ids=- rev=HEAD C3_R46_PASS=false
CTL_E_selftest_pins_own_bytes rc=1 C2_R46: self_pin=1 targets=hardened declared=25 killed=21 survived=4 inapplicable=0 neutral_killed=6 pristine=1 equivalence=0 rev=HEAD C2_R46_PASS=false
CTL_F_selftest_always_fails rc=1 C2_R46: self_pin=1 targets=hardened declared=0 killed=0 survived=0 inapplicable=0 neutral_killed=0 pristine=0 equivalence=0 rev=HEAD C2_R46_PASS=false
CTL_G_round45_counters_unchanged rc=1 C2_R46: self_pin=1 targets=orig declared=25 killed=0 survived=25 inapplicable=0 neutral_killed=0 pristine=1 equivalence=-1 rev=HEAD C2_R46_PASS=false
EXIT=0        (wall 4.14 s)
```

`diff .ufo/evidence/round-46/control/controls-at-freeze.stdout /tmp/tameshi-r46-T46ExecDrill/controls.out` → `CTL_DIFF_EXIT=0`: byte-identical to the receipt committed at the freeze, so the control answers did not move between the freeze and CONTENT (and HEAD, whose delta is wave-2 spec files only). Every control is false, each for the reason the contract names.

## 4. Selftests of the three counters

```
$ python3 .../round-46/calibration/measure.py --selftest
C1_R46_SELFTEST: cases=18 failed=0
VERDICT: PASS
EXIT=0
$ python3 .../round-46/hardening/mutate.py --selftest
C2_R46_SELFTEST: cases=8 failed=0
VERDICT: PASS
EXIT=0
$ python3 .../round-46/coverage/measure.py --selftest
C3_R46_SELFTEST: cases=24 failed=0
VERDICT: PASS
EXIT=0        (three runs, wall 2.09 s total)
```

All 50 cases pass; no case was skipped and every case printed `PASS <case> want=… got=…`.

## 5. No-harm at CONTENT

```
$ bash .../round-46/no-harm.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
NOHARM commandD recorded_cases=9 depth_score=9 ok
NOHARM coldread score=6 box3_full_page=False ok
NOHARM r45-freshness population=73 fresh=71 C1_R45_PASS=true ok
NOHARM r45-coverage rows=2 entries=2 C2_R45_PASS=true ok
NOHARM S160-count 1 ok
NOHARM registry-rows-not-below-117 120 ok
EXIT=0        (wall 28.70 s)
```

No `RED` line, so `deciding-run.sh`'s `grep -q RED` step would pass. The contract's `no_harm` sentence also names "the root census exits 0"; `no-harm.sh` does not run it (deciding-run step 4 does), so I ran it separately:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
tameshi ok /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md
CENSUS_EXIT=0   (12 output lines: 11 W04/W01 warnings + 1 ok line)
```

The 11 warnings are the set the lesson records ("11 W04/W01 warnings (same set as round 45)"). Registry rows at CONTENT: 120 (no-harm line above).

## 6. Frozen files — the requested diff

```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --stat \
    745a583181648cfc7f9c1b476cd1be7dc68f7433 6f2168e028ce7ff6e82ac92093ac05dd1f147c32 -- \
    .ufo/evidence/round-46/calibration/measure.py \
    .ufo/evidence/round-46/coverage/measure.py \
    .ufo/evidence/round-46/hardening/mutate.py \
    .ufo/evidence/round-46/hardening/mutants.json \
    .ufo/evidence/round-46/contract.json
(no output)
EXIT=0
$ git ... diff --name-status <same five paths>
(no output)
EXIT=0
```

Empty, as required. I extended the same check to the full `FROZEN` list of `deciding-run.sh` (contract, calibration `measure.py` + `statements.json`, coverage `measure.py` + `sources/`, `assimilation/package/`, `assimilation/adoption-map.json`, `hardening/mutate.py` + `mutants.json`, `control/run-controls.py`, `no-harm.sh`):

```
$ git ... diff --stat 745a583… 6f2168e… -- <full FROZEN list>
(no output)   FULL_FROZEN_DIFF_EXIT=0
```

So `deciding-run.sh` step 0 would print `FROZEN_UNCHANGED=1` at CONTENT. Counter digests at CONTENT (and identical at the freeze, where compared):

```
ad5f85df21b1e3f01ff5922242900d0b3bba1a044c9ff19828ecf00ab1ce680a  .ufo/evidence/round-46/calibration/measure.py
f8bfefdf6c08ce880c3f329018d946168dd022c50391d24551853326dbcfb5f5  .ufo/evidence/round-46/coverage/measure.py
999e0a4b6e4725666d002130ada8dcad05f81d2fbaaefb4ba7ada4b1fd82ca66  .ufo/evidence/round-46/hardening/mutate.py
bd21304a48a0d1e5427387485ffce90dfe02dddfeb3873dc2b9f46a3a03847cd  .ufo/evidence/round-46/hardening/mutants.json
f2a8ec0fc3e08be1f439527cab8abfe6607353e91e22a1ca9277e010c623c507  .ufo/evidence/round-46/hardening/freshness-counter.py
200c777ff32ff6e6d7faa9ff872e4e6bff14b989c22707c66e4586f15402b5f9  .ufo/evidence/round-46/hardening/coverage-counter.py
```

The C3 counter digest `f8bfefdf…` is the digest `w1/MutC3Counter.md` audited and restored to, and `999e0a4b…ca66` / `bd21304a…87cd` are the digests `w1/MutDriver.md` records for the driver and manifest — the files the wave-1 seats attacked are the files at CONTENT.

## 7. Comparison with the SCORECARD round-46 block and the lesson

| Stated (SCORECARD round-46 block / lesson) | Observed at CONTENT | Match |
|---|---|---|
| C2 after: `killed=25 survived=0 neutral_killed=0 pristine=1 equivalence=1` `C2_R46_PASS=true` (SCORECARD claim row; operability score `floor(10*killed/25)` = 10; capability row "`--targets hardened` `killed=25`") | `killed=25 survived=0 neutral_killed=0 pristine=1 equivalence=1` `C2_R46_PASS=true`, `declared=25 inapplicable=0` | yes, field for field |
| C2 before: `killed=0 survived=25` (`before/c2-at-freeze.stdout`, `--targets orig`) | reproduced inside CTL_G: `targets=orig declared=25 killed=0 survived=25` | yes |
| C3 after: `rows=3 entries=3 indexed=3 covered=3 row_ids=S258,S259,S260` `C3_R46_PASS=true` | identical | yes |
| C3 before: `rows=0 entries=0 C3_R46_PASS=false` (`before/c3-at-freeze.stdout`) | receipt re-read, unchanged; my run is the after state | yes (receipt only; before-state run is not mine) |
| Controls: CTL_A/B/C `entries=0`, CTL_D `rows=0`, CTL_E `killed=21 neutral_killed=6` false, CTL_F `pristine=0` false, CTL_G `killed=0` | identical, byte-identical file to `controls-at-freeze.stdout` | yes |
| Selftests: C1 `cases=18 failed=0`, driver `cases=8 failed=0` (capability rows); lesson "the C3 and C2 counters' own selftests leave 4 and 8 mutants alive" | `18/0`, `8/0`, C3 `24/0`; nothing contradicts the 4/8 survivors (those are mutant audits, not selftest counts) | yes |
| no-harm: "prints ok for all six monitors"; contract `command D 9, coldread 6, fresh=71, rows=2 entries=2, S160 count 1, registry rows not below 117` | six `ok` lines, exit 0; registry 120; census exit 0, 11 warnings | yes |
| Depth 9 / calibration 6 / freshness 9 monitors | command D 9, coldread 6, fresh=71 (score 9) | yes |
| C1 after `total=0 C1_R46_PASS=true` at `e630ae79…` | **unrun by bounds** (item: do not run C1; the L1's deciding run) | not checked here |

No difference between the observed counter final lines and the numbers the SCORECARD round-46 block and the lesson state.

## 8. Extra checks I ran (independent of the counters)

- **Snapshot digests vs the lesson's `## Gate`.** Extracted each snapshot from CONTENT and hashed it: `arxiv-2504.16777-abs.html` 43,376 bytes `28d2954d22ea45af7bd0454f1a8b01bb5db40e8e5cc235eed176a1621aa26a14`; `tum-portal-flaky-failures.html` 51,850 bytes `5eb59adf099304a07059530b0857f7b517eaa72c832049f46952915a77e71a6f`; `google-flaky-feed-6277555988217606236.json` 8,353 bytes `434d86586ecf3ea03f57d4342c6e8575576eef6a9fd452a5c0a9e67bd8889929`. All three byte counts and full sha256 match the lesson exactly.
- **Lane package copies vs the read-only package.** `cmp` of each `assimilation/package/*.md` against `/home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge/corpus/knowledge/<same name>` → `IDENTICAL` for r5 (`77b3d448…`), r6 (`a73c076c…`), r9 (`34b343a3…`). So the counter's "quote absent from the package copy" test is measured against the real package, not a doctored copy.
- **Independent re-open of the lesson's requested spot-check** (admit S258, and the other two). Reimplementing the counter's `norm_text`/`fold` in `/tmp` and reading the snapshots at CONTENT: S258 quote 22 tokens, found once in the snapshot; S259 quote 18 tokens, found three times (the abstract appears three times, as the lesson says); S260 quote 15 tokens, found once. Enumerating every double-quoted 6–25-token span of each entry that is located in its snapshot: S258 has 14 located quotes fresh against the package copy (the headline 22-token quote is *not* fresh — it is in the package), S259 has 12 fresh, S260 has 14 fresh. The re-grounding is substantive, not one accidental string.
- **Registry rows at CONTENT.** `git show 6f2168e:corpus/SOURCES.md` lines 133/134/135 are S258/S259/S260 with the three frozen URLs (`arxiv.org/abs/2504.16777`, the `portal.fis.tum.de` record, the `testing.googleblog.com` per-post feed).
- **Content→HEAD scope.** See Bounds: only the three wave-2 spec files differ, so my controls run from the working tree is the CONTENT run for every copied input.

## 9. Findings

**F1 — LOW — the lesson cites an end-of-round census receipt that was never committed.**
Attacks: `corpus/lessons/round-46.md:124-125` ("End: `.ufo/evidence/round-46/census-end.stdout` (recorded at the content revision)").
Command/output: `git ls-tree -r --name-only 6f2168e… -- .ufo/evidence/round-46/ | grep -i census` → only `census-start.exit`, `census-start.stderr`, `census-start.stdout`; `git log --all --oneline -- .ufo/evidence/round-46/census-end.stdout` → no output (never committed in any branch reachable from this repo). The *number* is fine — my own `sources-census.sh validate` exits 0 with 120 rows and 11 warnings — but the receipt the lesson points at does not exist at CONTENT, and the sentence "recorded at the content revision" is false as written. Fix: commit the census output as `census-end.stdout` in the receipts commit, or soften the sentence to name the deciding-run receipt.

**F2 — LOW — the SCORECARD's deciding-receipt paths (`after/*.stdout`) do not exist at CONTENT or at the commits the After cells name.**
Attacks: `SCORECARD.md` round-46 block, 4 occurrences of `.ufo/evidence/round-46/after/` (depth row, C1/C2/C3 Evidence cells, no-harm sentence).
Command/output: `git ls-tree -r --name-only 6f2168e… -- .ufo/evidence/round-46/after/` → empty; `git log --all --oneline -- .ufo/evidence/round-46/after/` → empty; `ls -la .ufo/evidence/round-46/after/` → empty directory on this disk only (git cannot track it). The C2/C3 "After" cells additionally name measured commit `a6892b196f923efbed242ce9ea599a3f745b2138`, where `after/` also did not exist. This is declared-forward by the landing rule (the deciding run writes the receipts, then a receipts-only commit follows) and the paragraph under the table says so — but at the revision the block itself calls "the content revision", a reader cannot open any of the cited evidence files. My dry run reproduces the numbers independently, so the claims are not at risk; the citation is. Fix: land the receipts commit with the block, or mark the paths "to be written by the deciding run".

**F3 — LOW — `deciding-run.sh` cannot write its receipts from a clean checkout of CONTENT.**
Attacks: `.ufo/evidence/round-46/deciding-run.sh` step 0 and the `after/` directory.
Command/output: `grep -n mkdir .ufo/evidence/round-46/deciding-run.sh` → `NO_MKDIR_IN_DECIDING_RUN`; the script `tee`s `$OUT/frozen.stdout` and redirects the counters into `$OUT/…` while `$OUT` must be "an existing directory inside LANE". `after/` is empty and untracked, so `git clone`/`git worktree add` of `6f2168e` has no such directory; the run then loses every receipt and exits 1 on the `cat "$OUT/c2.exit"` comparison. It fails closed (no false pass), and the L1's working checkout happens to carry the empty directory, so this does not affect the deciding run as executed here — it affects reproduction. Fix: `mkdir -p "$OUT"` (and commit a `.gitkeep`) in the script.

**F4 — INFO — the C2 driver counts a hung selftest as a kill and takes `declared` from the manifest at REV without a byte pin.**
Attacks: `hardening/mutate.py:58-62,75-79,104-118`.
`run_selftest` returns `('timeout','timeout')` on `TimeoutExpired`; `judge` maps any non-`pass` state to `killed`. Not exercised here: the whole 31-mutant run finished in 6.51 s against a 300 s per-mutant timeout, so no mutant was killed by hanging. Likewise `declared`/`killed` are read from `mutants.json` at REV with no sha256 check inside the driver (only the frozen-diff step guards the manifest); my diff of `mutants.json` freeze→CONTENT is empty and the manifest enumerates 25+6, so the guard holds. Also note a `neutral` mutant that is `inapplicable` would not increment `neutral_killed` (it is not counted as killed either) — `inapplicable=0` here. No action required for this round; worth naming for the round-47 successor claim.

**F5 — INFO — the contract's `no_harm` names a census monitor that `no-harm.sh` does not run.**
Attacks: `contract.json` `no_harm` ("…and the root census exits 0") vs `.ufo/evidence/round-46/no-harm.sh` (six monitors, no census).
The census is deciding-run step 4; I ran it separately (exit 0, 120 rows, 11 warnings). No defect in the numbers; the two-script split is only implicit in the contract.

**F6 — INFO — nothing in the claim numbers moved.** C2 and C3 reproduce the SCORECARD After cells field for field at CONTENT; the controls reproduce the freeze receipt byte for byte; the no-harm monitors and the census are green; the frozen diff is empty. The only claim I could not check is C1, by instruction.

## 10. Unrun checks (reported as unrun)

- C1 counter (`calibration/measure.py --lane … --rev … --base … --work …`) — explicitly excluded by the item; the L1 runs it.
- `deciding-run.sh` as a whole (it would take C1) — unrun. I verified its step-0 diff and its C2/C3/no-harm/census steps individually.
- The receipts-only commit and any claim verdict — not mine.
- No build/lint/test/formatter run, per the wave bounds.

## 11. Risks

- The C2 equivalence check runs the round-45 and hardened counters over `ea25e022…` inside temp dirs; it passed (1/1 for both groups) in 6.5 s, so it is not silently skipping. A future change to that data revision would need the L1's re-run, not a seat's.
- The controls script copies the *working tree*; I established that the working tree differs from CONTENT only in wave-2 spec files, but a later wave-2 seat that edits a copied path (counter, snapshot, package, registry, entry) would make a future controls run differ from CONTENT. Nothing in this wave is authorized to edit those paths.
- `no-harm.sh` greps for `RED` only in `deciding-run.sh`; a seat reading the script alone would not see the census monitor (F5).
