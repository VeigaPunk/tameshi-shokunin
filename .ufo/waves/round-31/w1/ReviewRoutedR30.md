# ReviewRoutedR30 — disposition of round-30 routed defects at c111dab

**Verdict: no committed fix exists at `c111dab58b0a8d55e991bbd2efe3aad56717b95a` for any routed defect —
the base→freeze diff (`36c1d39..c111dab`) adds only the 10 `.ufo/evidence/round-31/*` pre-freeze files
(+2109 lines; nothing under `corpus/`, `SCORECARD.md`, `tools/`). One routed item is resolved by that
freeze (binding v4). The runner fixes carry a verified deferral reason (270 of 456 ledger entries
confirmed by recount). Everything else is planned but uncommitted: the wave-1 spec assigns each defect
a seat and drafts exist in uncommitted `w1/` reports. Two coverage risks: (a) defect 2's rule is planned
as a QUALITY criterion and per-wave bound text, not as an edit to the cold-read recipe the routing names;
(b) the runner fix was routed to "open round 31's content revision" but `contract.json:43` re-defers it
beyond the round — a deviation the integration should acknowledge, even though the deferral reason holds.**

Frozen-byte check: `git diff c111dab -- .ufo/evidence/round-31/{contract.json,c1-measure.py,coldread/bind-select-v4.py}`
is empty (worktree equals frozen bytes); `git status` shows only untracked `.ufo/waves/round-31/*`.

## Disposition table

| Defect (source) | Disposition (path:line or open) | Status | Deferral reason holds? |
|---|---|---|---|
| Spotcheck D1 — JudgeC1 called "non-author"; append erratum naming the spotcheck closure as the non-author C1 reviewer (`round-30-verifier-spotcheck.md:208-209`, defect text at :40-43) | open at c111dab: `SCORECARD.md:1473` and `corpus/lessons/round-30.md:115` still say "named non-author seat/judge". Planned: w1 item ScribeMistakes31 (`spec-w1.json:228`, `make-spec-w1.py:215-217`); drafted erratum at uncommitted `w1/ScribeMistakes31.md:9` | open (planned; draft exists) | n/a — not deferred |
| Spotcheck D2 — cold-read recipe: `--workdir` under own scratch on every `--regression`; cwd check before any kill; record ColdA09 kill in section-26 note (:210-211) | open at c111dab: recipe `SKILL.md:1879-1895` carries neither rule (only `--workdir` API mentions elsewhere). Planned coverage exists but off-target: wave bound text carries both rules (`make-spec-w1.py:41-43`, `make-spec-w2.py:59-61` — enforced per wave, not recipe), QUALITY criterion 67 drafted (`w1/ScribeQuality.md:37`), ColdA09 section-26 erratum drafted (`w1/ScribeMistakes31.md:15`); the w2 content-revision plan (`make-spec-w2.py:45`) does not list SKILL.md | partial | n/a — not deferred. Risk: the routing says "cold-read recipe"; the plan lands the rule as a criterion + bounds, not in `SKILL.md:1879-1895`. If criterion coverage is judged sufficient this is resolved-on-paper only |
| Spotcheck D3 — pre-dispatch dead-seat diff as committed check (:212) | open at c111dab: no dead-seat script in `tools/` (full `ls-tree` checked), no committed check. Planned: w1 item BuildDeadSeatCheck (`spec-w1.json:164`, `make-spec-w1.py:166-172`); report `w1/BuildDeadSeatCheck.md:3-15` says `dead-seat-check.py` (375 lines) flags `ConnectorOverlap` exit 1 on the real pair and passes two clean pairs; source pasted for L1 to commit | open (planned; artifact demonstrated, not yet committed) | n/a — not deferred |
| Spotcheck D4 — binding v4 from audit conditions; per-leg runtime tally check; 8 MutateHead survivors (:213-214) | binding v4: `.ufo/evidence/round-31/coldread/bind-select-v4.py:2-21` (docstring: v3 with the round-30 post-data audit conditions made stricter, frozen pre-data); contract `binding_v4` `contract.json:51-55`; pilot `coldread/pilot/v4-on-r30-real-receipt.json` kept=63/excluded=0. tally+survivors: `contract.json:43` `not_claimed` | **resolved** (v4) + deferred-with-reason (tally, survivors) | holds: ledger has exactly 456 entries, 270 key `tools/mutate-and-run.sh` (recount below); runner blob at c111dab `a7d3f2dd…2eb9` matches the ledger's pinned input sha. "about 31 sections" is directionally consistent: 26 sections' latest entry keys on the runner (23 by heading-only key, 44 ever-keyed); exact 31 derivation not reproduced |
| Spotcheck D5 — lesson cite `:60-62`→`:60`; stale `Next unused id: S092.` (:215) | cite: marking erratum is committed at `round-30-verifier-spotcheck.md:44-45`; the cited line `corpus/lessons/round-30.md:59` still reads `:60-62` (standing, append-only); no committed append-erratum; drafted at `w1/ScribeMistakes31.md:11`. S092: `corpus/SOURCES.md:355` `- Next unused id: S092.` still present; positionally superseded by `:363-364` ("Round 30" note + `- Next unused id: S095.`); planned: `make-spec-w2.py:45` says the content revision carries "S095-S097 and the Next-unused-id line" | partial (marked at source; correction drafted, uncommitted) | n/a — not deferred. Flag: unlike the S090 precedent (`SOURCES.md:353-354`), no explicit supersession note for S092 is yet visible in plan text — thin coverage |
| Spotcheck D6 — owner of `/tmp/tameshi-r4-2-regression.j0FKnk` / clone `tameshi-registry-check-i272er4j` (:216-217) | open at c111dab: `git grep -iE 'j0FKnk\|i272er4j' c111dab` hits only the spotcheck lines themselves. Planned: w1 item RevengerStrayTmp (`spec-w1.json:172`, `make-spec-w1.py:173-177`); no `w1/RevengerStrayTmp.md` in the w1 glob — seat still running | open (assigned, in flight) | n/a — not deferred |
| round-30.md routed — runner selftest gaps T08/N03/H03/H04/H05/N01/N02/N05 (`round-30.md:206-211`, survivors tabled at `wC/MutateHead.md:63-80`) | `contract.json:43` `not_claimed`: "per-leg tally check and the 8 MutateHead selftest survivors stay routed" | deferred-with-reason | holds (same 270/456 evidence). Flag: routing text says "the fix opens round 31's content revision"; the contract moves it out of round 31 — re-deferral with a measured reason, but the round-31 lesson should record it explicitly |
| round-30.md routed — binding v4 / Mistake 2 (`round-30.md:212`) | `contract.json:51-55` + `bind-select-v4.py` (sha256 `dd8bb393…04030b87f` = blob hash at c111dab, verified) + pilot 63/63 | resolved | n/a |
| round-30.md routed — QUALITY imprecisions F1-F4 (`wC/ReviewQualityR30.md:16-71`) + stale S092 line (`round-30.md:213-215`) | `corpus/QUALITY.md` unchanged at c111dab (no corpus diff base→freeze). Planned: criteria 66-69 and append-only F1-F4 errata drafted in `w1/ScribeQuality.md:27-75`; content revision planned at `contract.json:49` `drift_plan` and `make-spec-w2.py:45` | open (planned; drafts in flight) | n/a — planned, not deferred |

## Evidence commands (all read-only; lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, commit `c111dab`)

- `git -C … diff --stat 36c1d39..c111dab` → 10 files, +2109, all `.ufo/evidence/round-31/*`; zero corpus/SCORECARD/tools changes.
- `git show c111dab:.ufo/evidence/round-31/before/c1-at-base.stdout` → `… mismatches=7 … C1_R31_PASS=false` at base `36c1d39`, exit-file `c1-at-base.exit`=1 — matches contract `before`.
- `git show c111dab:.ufo/evidence/round-31/before/drift-sim.txt` → six probes appending one comment line to each widely read input (sources, scorecard, log, quality, readme, lesson); `C1_MONITOR covered` drops to 60-63/64 each time — demonstrates that a single widely read input edit drifts section credit, which is the deferral mechanism claimed for `mutate-and-run.sh`.
- Ledger recount (read-only): `.ufo/evidence/round-21/coldread/ledger.json` at c111dab → `entries=456`; entries with `tools/mutate-and-run.sh` in `inputs` → **270**; sections whose *latest* entry keys on it → 26 (any-entry basis → 44). Matches "270 of 456"; "about 31" is the same order, not exactly reproduced.
- `git cat-file blob c111dab:tools/mutate-and-run.sh | sha256sum` → `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` — equal to the `inputs` hash the 270 entries pin, so editing it drifts all 270.
- `git cat-file blob c111dab:.ufo/evidence/round-31/coldread/bind-select-v4.py | sha256sum` → `dd8bb393…04030b87f` = contract `binding_v4.sha256`; `c1-measure.py` → `657fcc12…7584` = contract `counter_sha256`.
- Pilot receipt `v4-on-r30-real-receipt.json`: `assembled=63, kept=63, excluded=0, registry_members=38`.
- `git grep -n 'Next unused id' c111dab -- corpus/SOURCES.md` → `:355 S092` still present, `:364 S095` current.
- `git grep -nE '60-62' c111dab -- corpus/lessons` → marking at `round-30-verifier-spotcheck.md:44`, defect at `:215`, offending text at `round-30.md:59`.
- `git grep -niE 'j0FKnk|i272er4j' c111dab` → only `round-30-verifier-spotcheck.md:216-217`.
- `git grep -n -i 'judgec1' c111dab -- SCORECARD.md LOG.md corpus/lessons/round-30.md` → `SCORECARD.md:1473` ("named non-author seat"), `round-30.md:115` ("named non-author judge"), `LOG.md:1755`; spotcheck `:40-43` rules a dispatched seat is still the lane.

## Residual risk

- Wave-1 reports and specs cited as "planned" are uncommitted bytes (`.ufo/waves/round-31/` is untracked at this snapshot). The dispositions above describe plan state; the integrator can still drop an item.
- Defect 2's literal target is the recipe text; if `SKILL.md` is never edited, the fix exists only as per-wave bound text and a QUALITY criterion — durable only if bound text is regenerated each wave (it is: `make-spec-w1.py`/`make-spec-w2.py` both carry it).
- "about 31 sections" in `contract.json:43` could not be exactly reproduced (26 latest-keyed / 44 ever-keyed). The measured 270/456 core holds; the section figure is an estimate and should be read as such.
- Drift-sim used a comment-append proxy, not a `mutate-and-run.sh` edit; mechanism transfer is documented but the direct simulation was not run (consistent with deferring the edit itself).

## Verification gaps

- No committed `w2` spec or content revision yet — statuses "planned" will flip to resolved/open at integration.
- RevengerStrayTmp (defect 6) had no report at snapshot time; the j0FKnk owner is still unidentified in any committed byte.
- `lsp` check not applicable (markdown/json review of committed blobs; no language server for this content). Text grep over the `c111dab` tree was used throughout and is the primary evidence.

## Tooling record

None installed or updated. All inspection used `git show/grep/ls-tree/cat-file/diff` (read-only), `sha256sum`, and a local Python count over the ledger blob. No `jj`, no git write commands, no gates/selftests/sweeps/counter runs; nothing killed. Scratch dir `/fast/scratch/hyaku/tameshi-r31-seats/ReviewRoutedR30/` created, left empty.

Report: .ufo/waves/round-31/w1/ReviewRoutedR30.md
