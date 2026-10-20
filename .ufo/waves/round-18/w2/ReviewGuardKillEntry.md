# ReviewGuardKillEntry — round 18 wave 2 (FALSIFY)

Seat: TameshiR18.ReviewGuardKillEntry (reviewer, leaf). Target: `corpus/knowledge/guard-kill-closure.md` at read rev `01d586ddbc5fcd78659557c4e93a6ee8517b87d1` (sha256 `9312bdeb…91fb`, 136 lines; last changed in `58e5d53`, per `git log -- corpus/knowledge/guard-kill-closure.md`).

Axes: **accuracy** (does each sentence match what it cites?), **currency** (do the PENDING markers match the receipts measured since?), **citation fidelity** (do the S-ids match `corpus/SOURCES.md` rows and the live pages?), **overclaim** (does a "closed" result certify more than was measured?).

Method: I read the entry against every cited w1 report line, lane file at `183f87b`/`01d586d`, receipt, SOURCES row and live source page. The clone is `/tmp/tameshi-r18w2-ReviewGuardKillEntry-szvgTI/fleet/tameshi-shokunin`, checked out detached at the read rev, with siblings symlinked beside it. Every mutant ran in that clone, under bwrap (fleet read-only, `--unshare-net`, `env -i`) or inside the ruler's own bwrap envelope. Pristine bytes were restored each time, and the clone was re-checked-out at `01d586d` afterwards (`git status --porcelain` empty). Two scratch commits exist only in that /tmp clone (`cd160990…`, `fe2e00f6…`). No `lsp` device is mounted in this seat, so caller and definition checks are direct reads and grep, not semantic proof. No tools were installed or updated. Host: jj 0.45.1, git 2.56.0, bwrap 0.13.1, strace 7.2, Python 3.14.8.

## Findings by severity

### HIGH

**H1 — The entry still says nothing has been measured at the landed tip. At the read rev that is false.** The entry was written in `58e5d53` and not touched by `e08271a` or `01d586d`, which added the tip receipts.
- `:2` "Landed-tip results: PENDING". `:10` "Lines marked PENDING are not yet at the landed tip". `:132` "Tools not at the landed tip: `tools/trace-inputs.py` (untracked), staged … (X05) … (X07). Every landed-tip number is PENDING". `:136` puts all three after-measurements at PENDING.
- `:134` "Not run: no after-landing probe run, no `registry-check --json` held count at the landed tip" is **false at `01d586d`**:
  - `.ufo/evidence/round-18/c2-probes-v2-e08271a.txt:12` reads `DEFECT_PROBES: open=0 closed=11 total=11`, exit 0.
  - `.ufo/evidence/round-18/c2-probes-e08271a.txt:12` (v1 ruler) reads `could-not-evaluate (3 probe error(s))`, exit 2.
  - `.ufo/evidence/round-18/registry-full-e08271a.json:3,523` reads held 32 of 32, superseded 3, exit 0.
- Every staged tool landed byte-identical. `cmp` of staged against landed: `tools/registry-check.py` `e072fd39…`, `tools/bash-witness-study.py` `8dfaa25a…` (= X07:5), `tools/evidence-disposition.py` `66655a3a…`. The landed `tools/trace-inputs.py` hashes to `fb1d81f6…` (= X04:11). So the "staged-to-landed diff" asked for at `:136` is empty for every §4–§6 item.
- Effect: the C2 claim cites this entry, but at the read rev the entry denies the measurement the claim rests on.

**H2 — §2's branch-resolution rule and fixture recipe contradict the landed G2/G3 code, and the entry does not record it.**
- What the entry says:
  - `:49` gives the order `lane.branch` → `detect_branch()` (attached branch or `origin/HEAD`) → the unique one of master/main, and "Otherwise it is an error. Never HEAD".
  - The P08 recipe `:42-44` never sets `lane.branch`.
- What landed (`tools/evidence-disposition.py:51-53` and `:460-525`, `resolve_historical_anchor`):
  - The order is `lane.branch`, then an attached `refs/heads/*` branch.
  - There is no `origin/HEAD` step and no master/main step.
  - An unbound jj workspace is **refused** with exit 2 `historical_input_unavailable` (`:492-496`).
  - An unbound detached non-jj checkout **anchors at HEAD** whenever any `refs/heads/` or `refs/remotes/` ref contains it (`:498-525`). The selftest `v2-registry-clone-detached-anchor` expects exit 0 for exactly this case (`:2255-2276`, `:2868-2873`).
- Running the entry's recipe against the landed tool does not produce the G2/G3 split; it produces could-not-evaluate.
  - Observed in `c2-probes-e08271a.txt:11`: `P08 error … G2-live-bytes produced unexpected verdict exit=2 status='could_not_evaluate' findings=['historical_input_unavailable']`.
  - The selftest `v2-jj-without-lane-branch` encodes the same refusal (`:2862-2867`).
  - Ruler v2 had to bind `lane.branch master` to grade P08 at all (`defect-probes.py:482-485`).
- The ruler's own P08 fixture also departs from the recipe:
  - It runs `bookmark set`, including `--allow-backwards`, and builds a side commit D (`defect-probes.py:493`, `:503-511`, `:530-531`). Recipe step 2 says "Do not run `bookmark set`".
  - It asserts neither `symbolic-ref` rc 1 nor a unique branch nor HEAD≠`@` (`:535`), all of which recipe step 3 requires.
- "Never HEAD" is therefore false for the landed design. As a rule it is also too broad: a detached `--rev` clone has to anchor at its checked-out commit. `:53` is still PENDING and records none of this.

**H3 — A P08 or P11 "closed" result certifies less than the C2 wording implies. I built a mutant for each that passes both the probe and the owning selftest.** `:128-134` (§7 Limits) states neither bound.
- **P11, GIT_\* scrub.** Swapping the prefix filter in `git_clean_env()` (`tools/bash-witness-study.py:335-336`) for the GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset that `:101` calls "not enough":
  - Selftest still passes: `WITNESS_SELFTEST: 43/43 pass`, `VERDICT: PASS`, exit 0. A two-name pop also passes 43/43.
  - The ruler still reads P11 closed: `defect-probes.py --rev cd1609903659d0fd6f7ccbd917f7ec1f354c7b3a --only P11`, exit 0.
  - Control: removing the filter entirely fails 41/43, exit 1.
  - Why it passes: the landed canary exports only GIT_DIR and GIT_WORK_TREE (`bash-witness-study.py:1298-1299`), and so does P11 (`defect-probes.py:897-900`). The ruler rejects any other `GIT_*` extra (`:170-173`). The GIT_OBJECT_DIRECTORY canary that `:101` requires ("passes only when the intended blob is returned", C04:89) was not built.
- **P08, branch value.** Making `resolve_historical_anchor` ignore the `lane.branch` value and hardcode `"master"` (`evidence-disposition.py:465`):
  - Selftest still passes: `SELFTEST: PASS (63/63)`, exit 0.
  - The ruler still reads P08 closed: `--rev fe2e00f6af39baf1fe7e1deeba46f14a3c2f224f --only P08`, exit 0.
  - Why it passes: K01:188-190 required "branch name ≠ `master` and ≠ the lane's real branch (kills hardcoded-ref fixes)". The ruler binds `master` (`defect-probes.py:485`), the selftest binds `master` (`:2166-2167`), and the entry's recipe names `refs/heads/master` (`:42`, `:44`).
- Effect: C2's "closed with failure-backed selftests" covers only GIT_DIR/GIT_WORK_TREE for the GIT_\* leak, and only the bound `master` path for jj G2/G3.

### MEDIUM

**M1 — The meta-cheat detection rule in §1 cannot be applied to P05–P07.** `:25` says "Detection: the probe prints the failing case names".
- In fact the probe prints only the last output line: `excerpt()` at `defect-probes.py:248-254`, used at `:393-396`. For the trace collector that line is just `SELFTEST: 29/30`, with no case name (`c2-probes-v2-e08271a.txt:5-7`, and my replication below).
- I recovered the names only by running the mutants myself: `FAIL rdwr-open-excluded`, `FAIL pycache-prefix-private`, `FAIL root-exec-required`. They match X04:20-22, but a reader holding only the receipt cannot check for an incidental kill.
- P01–P04 are fine: their selftests' last lines happen to carry the case names.

**M2 — `:114` misreads an expected failure as a defect.** It says "The round-18 `dispositions-before.json` exits 1 with `expected_contains_missing` … The last item is an open defect in the staged work."
- That exit is the registered negative control:
  - `tools/registry.json:280-297` (`evidence-disposition-round18-before`) expects exit 1 with `"status": "failed"` and `"expectation": "producer_before"`.
  - `registry-full-e08271a.json:198-200` shows got 1, held true.
  - X07:31 says "both round-18 gates passed their expected outcomes".
  - The round-17 analogue row also expected exit 1 (`tools/registry.json:225-249`; K05:58).

**M3 — The S063 citation for the two config variables does not resolve, and the planned fix breaks the append-only rule.** Affected lines: `:1`, `:95`, `:99`, `:133`.
- The S063 row's anchor is still `ENVIRONMENT VARIABLES, "The Git Repository"` (`corpus/SOURCES.md:72`).
- The live git(1) page lists GIT_CONFIG_GLOBAL and GIT_CONFIG_NOSYSTEM under the **"other"** subsection. The heading order is Environment Variables › System › The Git Repository › Git Commits › Git Diffs › other. Both quoted sentences are present verbatim.
- The entry's remedy, "the L1 widens it", is an in-place anchor edit. The contract forbids that: only `status`, `recheck` and `used-by` may change in place, and a correction must be a new row (`CORPUS.md:116-118`; `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:49`).
- The staged gate leaves S063 unchanged (`.ufo/waves/round-18/staged/lesson-round-18-gate.md:85`). By the entry's own condition at `:133` ("sourced … once its anchor is widened"), both config variables are still unsourced at the read rev.
- `used-by` drift: S061 (`SOURCES.md:70`) and S063 (`:72`) list only `corpus/lessons/round-17.md`, although this entry cites both. `CORPUS.md:107` defines `used-by` as every citing knowledge entry.

**M4 — The entry describes only P10/P11 as behavioural probes and, by implication, treats P08/P09 as guard removals.**
- `:29` "P10 and P11 are behavioural probes, not guard removals". In fact P08–P11 are all behavioural: X03:41-48 lists them in the behavioural table, and `defect-probes.py:920-931` sends only P01–P07 through `GUARD_SPECS`.
- So the "Bound" at `:29` and §7's first limit at `:128` ("proves a mutant kills a selftest") describe only P01–P07. The fixture-specific bounds of P08–P11 go unstated (see H3, and L13 for P09).

**M5 — `:45` "G2 and G3 split only at tree level" is wrong for G3.**
- C02:61 is the cited report: in its second shape the trees are equal and G3 splits on ancestry.
- The ruler's own G3 sub-fixture splits the same way: master=D carries B's tool bytes, and the split is ancestry (`defect-probes.py:503-504`, `:553`; receipt `master=D`, findings `historical_input_unavailable`).

**M6 — Several citation qualifiers cannot be resolved from the entry, and filenames make some of them resolve to the wrong draft.**
- The qualifiers are "[src: S066, Gate note]" (`:57`), "[src: S069, Gate note]" (`:71`), "[src: S074, quotes A–C]" (`:47`), "[src: S073, quotes]" (`:120`), and "Ids follow the L1 map" (`:12`).
- `:10` defines `[src: Sxxx]` as the header row only, and no SOURCES row has a "Gate note" or quote labels.
- `corpus/lessons/round-18.md` is **absent** at `01d586d`. The Gate table and the id map exist only in `.ufo/waves/round-18/staged/lesson-round-18-gate.md:14-26,45-58`.
- The committed drafts under `.ufo/waves/round-18/sources/` keep provisional ids that collide with the final ones. `S074-B10SrcPycachePrefix.md` exists, while "quotes A–C" for final S074 are in `S075-B11SrcSymbolicRef.md:18-22`. Likewise `S066-*` is Google mutation, `S069-*` is prctl, and `S073-*` is open(2).

### LOW

- **L1 (`:63`).** "Two sub-defects", but the cited K01:106 has "P09 three sub-defects": (a) `parse_constant`, (b) `isfinite`, (c) naming `timeout_s`.
- **L2 (`:67`).** "aborts with exit 1 on a non-integer `--timeout`" is too broad. Per S09:73-80, only identifier-like values (`nan`, `abc`) hit exit 1. Values like `5x` and `08` exit 64, and `+5` and `0x10` are accepted. The arithmetic test is still at `tools/mutate-and-run.sh:467,1278` at the tip; not re-run (my dummy invocation stopped at spec setup, exit 2).
- **L3 (`:71`).** "so an escaping process must fork first" is too broad. EPERM applies only to a process-group leader: "setsid() fails if the calling process is already a process group leader" (live page, verified). The S069 row's `teaches` carries the same wording.
- **L4 (`:89`).** The UID-change/EPERM limit is labelled `[INFERENCE]` in V02:31. The entry states it as fact.
- **L5 (`:118`).** "has the exclusion at `:818-820`": those lines are the selftest case `rdwr-open-excluded`. The exclusion itself is the regex at `tools/trace-inputs.py:82`.
- **L6 (`:110`).** The causal chain is garbled. Per K05:45-58, the *tool edit* breaks the unwaived round-17 manifests, not the waiver. The `round17-before` row expects exit 1 with status failed, and gets exit 2.
- **L7 (`:133`).** "The subreaper page is row S068 once B13 installs it" is stale: S068 is installed and mined (`SOURCES.md:77`). B13 is the KnowExitErratum seat; the subreaper lead came from B05 (`B05SrcPrctl.md:13,24`).
- **L8 (`:8`).** The scope names R17-CMD-BIND, but no section covers command binding; §6 covers only the P05–P07 guards.
- **L9 (`:3`, `:10`).** The recheck cites the v1 base receipt, but the ruler at the read rev is v2 (`defect-probes.py:154-156,482-485`; base receipt `c2-probes-v2-183f87b.txt`), and the v1 ruler exits 2 at the tip. The ruler docstring (`defect-probes.py:8`, which `:129` cites) still shows `PATH=/usr/bin:/bin`; v2 prepends jj's directory. The recheck list also omits S061, which the entry cites.
- **L10 (`:27`).** "P05 27/27 both": the receipt records only the mutant run's last line (`defect-probes.py:396`). The pristine count is not recorded, only its exit 0.
- **L11 (`:112`).** The entry says the manifest "should pin the new digest as a live input". The landed `.ufo/evidence/round-18/dispositions.json` (sha `9caa2f76…`, = X07:6) has `inputs` = four round-13/14 files and no `tools/bash-witness-study.py`. A later committed edit to the tool would pass silently. The recommendation was not adopted, and the entry does not record that.
- **L12 (`:97`).** The config pins have no failure-backed coverage. Removing either `GIT_CONFIG_GLOBAL` or `GIT_CONFIG_NOSYSTEM` from `git_clean_env()` still passes the landed selftest 43/43, exit 0.
- **L13 (`:63-65`).** Removing `parse_constant` at the tip is killed only on diagnostic text. `timeout-nan`, `timeout-infinity` and `timeout-negative-infinity` each `FAIL (exit=2)`: the tool still rejects with exit 2 naming `timeout_s`, because `isfinite` catches NaN/Inf. P09 tests only NaN and Infinity, so it cannot tell whether `parse_constant` exists. The entry does not say this.
- **L14 (receipts).** Probe target labels are base line numbers that no longer match the tip: P01 `:445` → `:532`, P02 `:552` → `:645`, P03 `:466` → `:786`, P04 `:96` → `:104`, P11 `337-344` → `347-350`. Anchors are matched on content, so measurement is unaffected.

## PENDING markers vs measured receipts (read rev `01d586d`)

| Entry line | PENDING text | Measured fact | Evidence |
|---|---|---|---|
| `:2`, `:136` | "Landed-tip results: PENDING"; probe open/closed count PENDING | v2 at `e08271a`: 0/11 open, exit 0. My replication at `01d586d`: `DEFECT_PROBES: open=0 closed=11 total=11`, exit 0. v1 at `e08271a`: exit 2 | `c2-probes-v2-e08271a.txt:12`; `c2-probes-e08271a.txt:9-12`; my run below |
| `:136` | registry `--rev <tip> --json` held count PENDING | held 32/32, superseded 3, exit 0, at `e08271a`. The registry JSON is the same file at `01d586d` (`d2d1972e…`). `tools/` and `corpus/` are identical between `e08271a` and `01d586d`; the only changed row input, `defect-probes.py`, passes its row at `01d586d` (`--selftest`: `PASS (6 cases)`, exit 0). [INFERENCE: 32/32 carries over] | `registry-full-e08271a.json:3,523` |
| `:53` | G2/G3 retarget PENDING | Landed with a different design, `resolve_historical_anchor`: bound jj only, unbound jj refused, HEAD anchor for non-jj (H2). P08 closed only with `lane.branch` bound | `evidence-disposition.py:460-525`; `defect-probes.py:482-485` |
| `:65` | staged `parse_constant` + `isfinite` PENDING | Landed byte-identical. At the tip, removing `parse_constant` fails 3 named cases and removing `isfinite` fails `timeout-overflow` (both exit 1) | `registry-check.py:240,349`; my mutants below |
| `:91` | subreaper and walk only staged | Landed: `_enable_child_subreaper`, pidfd, bounded drain, `unavailable` on failure. P10 survivors=[] | `registry-check.py:384-409,641-723`; `c2-probes-v2-e08271a.txt:10` |
| `:97` | config pins PENDING | Landed (`bash-witness-study.py:333-339`) but not failure-backed (L12) | my mutants below |
| `:114` | X07 staged result PENDING | Landed; the round-18-before manifest exits 1 as registered (M2) | `registry-full-e08271a.json:198-200` |
| `:118`, `:120`, `:122` | trace collector PENDING (untracked) | Tracked at `01d586d` with sha `fb1d81f6…` = X04. P05–P07 closed 29/30. The frozen copy is still `521be955…` | `git ls-tree 01d586d tools/trace-inputs.py`; sha256 |
| `:134` | "Not run: no after-landing probe run, no … held count" | **False**: both exist. The third clause (no canary run after the scrub) still holds: there is no post-scrub canary receipt in `.ufo/evidence/round-18/` | H1 |

## S-id citation check

| S-id | Entry use | Row matches `SOURCES.md`? | Live quote | Result |
|---|---|---|---|---|
| S061 | `:1`, `:12`, `:33` | yes (`:70`); `used-by` omits this entry | detached-HEAD sentence and recipe comment "working-copy commit's parent" present | holds, but `used-by` drift (M3) |
| S063 | `:1`, `:3`, `:95`, `:99`, `:133` | anchor "The Git Repository" does not cover the config vars; `used-by` omits this entry | both config quotes verbatim, under "other" | gap (M3) |
| S065 | `:1`, `:57` | yes (`:74`) | gate quote and `parse_constant` text present | holds |
| S066 | `:1`, `:57` | yes (`:75`); "Gate note" is staged only | §6 sentence present | holds (M6 qualifier) |
| S068 | `:1`, `:73`, `:83`, `:133` | yes (`:77`) | reparenting sentence present | holds; `:133` stale (L7) |
| S069 | `:1`, `:71` | yes (`:78`) | ¶2 and EPERM sentences present; no "kill" on the page (confirms `killpg` is not named); page sha `52cbc190…` = B06:10 | holds (L3) |
| S070 | `:1`, `:95` | yes (`:79`), tier B | GIT_DIR sentence present | holds |
| S072 | `:1`, `:118` | yes (`:81`) | O_TRUNC sentence present (preceded by "If the file already exists and is a regular file and") | holds |
| S073 | `:1`, `:120` | yes (`:82`) | prefix and dont-write sentences present | holds |
| S074 | `:1`, `:47` | yes (`:83`) | quotes A, B, C all present | holds (M6 qualifier) |
| S067, S071 | `:12` (named as not cited) | rejected rows (`:76`, `:80`) | — | correct |

## Sentence checks that held

Every one of these was checked against the cited line and matched:
- **K04** — `:21` (K04:65-71).
- **X03** — `:21`, `:27` (X03:29, :13, :33-39), `:51` (X03:45), `:61` (X03:46), `:77` (X03:47), `:118` (X03:37), `:120` (X03:38), `:122` (X03:39), `:129` (X03:8), `:130` (X03:48).
- **Round-17 lesson** — `:23` (lesson §7 item 3 = `round-17-verifier-spotcheck.md:428-432` at `183f87b`; unchanged at the tip).
- **K01** — `:23` (K01:14-20), `:25` (K01:83-89, :91-96), `:29` (K01:30-32).
- **C02/C03** — `:33-38`, `:40`, `:44`, `:49` (fleet `state` description vs `scripts/hyaku/jj-lane.sh:113-126,155-180` at sha `3369dc27…`, read-only).
- **Base code lines** — `tools/evidence-disposition.py:441,450,518`; `tools/registry-check.py:96,221-227,281,306-323,375,387,466`; `tools/bash-witness-study.py:116-117,337-340`; frozen `trace-inputs.py:82,516,644`.
- **R05** — `:51` (R05:44).
- **S09** — `:59-61` (S09:33-37, :42-48).
- **S10/N02/V02/X05** — `:75-87` (S10:14-20,:42-43; N02:21,27-29,32; V02:33; X05:7,43).
- **C04/S11** — `:95`, `:101-103` (C04:44-48,60-65,79-89,96; S11:45-46,63-65).
- **X07/K05 migration** — `:105` (`.ufo/evidence/round-13/expected.json:11` = `49e9e5e2…`; `git show 4acc607:tools/bash-witness-study.py | sha256sum` gives the same value), `:109`, `:111`.
- **X04/M03** — `:120` (round-17 `MutateTraceInputs.md:122-131` M03).
- **K04/X09** — `:124` (K04:41-44,73-83), `:131` (X09:28,40-43).

## Commands executed (key output)

| Command (cwd = clone unless noted) | Exit | Key output |
|---|---:|---|
| `git clone` + `checkout --detach 01d586d…` (env -u GIT_*) | 0 | HEAD `01d586ddbc5f…` |
| `git log --format='%h %s' -- corpus/knowledge/guard-kill-closure.md corpus/SOURCES.md` | 0 | the entry appears only in `58e5d53` |
| `git diff --stat e08271a 01d586d -- tools/ corpus/` | 0 | empty |
| `curl -sSL` for the 10 source URLs (S061/63/65/66/68/69/70/72/73/74), then tag-strip and match | 0 each | all entry and Gate quotes found; S063 config vars under "other" |
| `python3 mutants.py $C` under bwrap (registry-check and trace-inputs mutants) | 0 | RC pristine `PASS (46 cases)`; no-`parse_constant` `FAIL (3 of 46 …)` exit 1; no-`isfinite` `FAIL (1 of 46 cases: timeout-overflow)` exit 1; TI pristine `30/30`; M01/M03/M04 exit 1, `29/30`, named FAILs as in M1 |
| `python3 bws-mutant.py $C` under bwrap | 0 | pristine, two-name-pop and trio-unset all `43/43 pass` exit 0; no-filter `41/43` exit 1 |
| `python3 bws-mutant2.py $C` under bwrap | 0 | removing the global or nosystem pin: `43/43 pass` exit 0 each |
| `python3 ed-mutant.py $C` under bwrap | 0 | pristine `PASS (63/63)`; hardcode-master `PASS (63/63)` |
| `defect-probes.py --rev 01d586d… --only P11` | 0 | P11 closed |
| `defect-probes.py --rev cd160990… --only P11` (trio-unset commit) | 0 | P11 closed |
| `defect-probes.py --rev fe2e00f6… --only P08` (hardcode-master commit) | 0 | P08 closed, findings `historical_input_uncommitted` / `historical_input_unavailable` |
| `defect-probes.py --rev 01d586d…` (full ruler) | 0 | `DEFECT_PROBES: open=0 closed=11 total=11` (54.6 s) |
| `defect-probes.py --selftest` under bwrap | 0 | `SELFTEST: PASS (6 cases)` |
| `mutate-and-run.sh … --timeout nan` and `5x` under bwrap | 2 | `MUTATE: SETUP (spec is not a regular file …)`; L2 not re-measured |

Input hashes at the read rev:
- `corpus/SOURCES.md` `1d4b5910…`
- `defect-probes.py` `99297d96…`
- `c2-probes-183f87b.txt` `60e9994e…`
- `c2-probes-e08271a.txt` `1e2fddbb…`
- `c2-probes-v2-183f87b.txt` `f5e657d0…`
- `c2-probes-v2-e08271a.txt` `e61e777b…`
- `registry-full-e08271a.json` `ba7025da…`
- `tools/registry.json` `d2d1972e…`
- External: `CORPUS.md` `88556402…`, `SOURCES-CONTRACT-v1.md` `6c674a22…`

## Residual risk and verification gaps

- I did not run the full registry at `01d586d`. The 32/32 at the read rev is the inference stated in the PENDING table (identical `tools/`, `corpus/` and registry; the one changed row input re-run green).
- L2 (`--timeout nan` → exit 1) was not re-measured at the tip. My dummy spec stopped at setup with exit 2; the arithmetic check at `mutate-and-run.sh:467` is unchanged in form.
- Mutant coverage is sampled, not exhaustive. A mutant that keeps the `lane.branch` lookup but ignores its value survives (H3); I did not search wider P10 escape shapes such as double-fork plus a sentinel process (K01 C7).
- C2 wording is outside this entry's scope, but H3 bounds it: "GIT_\* leak … closed with failure-backed selftests" is backed for GIT_DIR/GIT_WORK_TREE only, and "jj HEAD-vs-tip G2/G3" only for a lane bound to `master`.
- No `lsp` device was available. Definitions and callers were read directly (`resolve_historical_anchor`, `git_clean_env`, `excerpt`, `guard_probe`), not resolved semantically.

**Verdict: partial.** The base-rev content and source quotes hold. But at the read rev the entry is stale and in places wrong: the PENDING and "Not run" lines, the §2 "Never HEAD" rule and recipe, the P05–P07 detection claim, the "open defect" misreading, the G3 tree-level claim, and the S063 sourcing. It also does not bound P08/P11, for which I built mutants that the probes still report as closed.
