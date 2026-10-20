# RR2 — round 17 wave 3 residual cold re-read: SKILL.md lines 1021–1091 at 0ff2734

Seat: RR2 (agent TameshiR17.RR2-2) · read_rev `0ff273448ac4e62893c9b28a4cea7c580712df19` · host `plazir27` · 2026-10-20, about 18:00–18:40Z.
Buckets: `### The tick and the pin read` (1021–1068) and `### Triggers T1–T3 and the re-pin rule` (1069–1091).

## Setup and page check

- Clone (fleet-mirror layout): `W=/tmp/tameshi-r17w3-RR2-hnbkmZ`, `C=$W/fleet/tameshi-shokunin`, detached at `0ff2734`; `git rev-parse HEAD` = `0ff273448ac4…`.
- Page: `git show 0ff2734:SKILL.md | sha256sum` → `de6c2b083be6f35d2c35e011ca37874f57204a2cdd195a106ff638fbea723dbc`, 1903 lines.
- Section sha256 was computed with assemble.py's rule (lines joined by `\n`, trailing blank lines stripped):
  - 1021–1068 → `66fdb741490cee395bfe372562b15991159761b054473e52d1c93cc4eb4cad1e`
  - 1069–1091 → `6eb7f28d1a172e480a8a81b0225f5ca625c0c422a38593d98413b2981577f502`
  - Both match the assignment. Lines 1021 and 1069 are exactly these headings.
- Read scope: only 1021–1091, plus SKILL.md:811-812 (named by the range as `(:811-812)`), plus the files these lines name. No LOG/SCORECARD/plans/reports/lessons/waves were opened. The L1-appended files were not read.

## Trace receipts (all under `.ufo/evidence/round-17/coldread/traces/RR2/`)

Every receipt has schema `tameshi-trace-inputs-v1`, rev `0ff2734…` and tracer exit 0. None carries a non-`.git` live-lane read, and no external path has two different digests.

| n | command (abridged; full argv in the receipt) | inner exit / key line | cited |
|---|---|---|---|
| 1 | ledger `sed -n 165,180p`; `grep -n "REGRESSION: PASS"`; grep for T1 pins | 0; `:170-173` "…an appended row, not an edit of §1–§4"; `:47` 6/10 @`084951be`, `:48` 4/10 @`d7edaab4`; `:302` `dc864c6a… (2 186 L) \| 90d50cdd… \| dirty \| stale + drift` | S1, S2 |
| 2 | `sed -n 12,26p corpus/knowledge/mutation-case-mado-verify.md` | 0; I1: "Re-pin at 17:46:15Z: sha256 `b56c6e57…2bcb`… whether the new revision reproduces this table is **U**" | S2 |
| 3 | `sed -n 811,812p SKILL.md`; `grep -n 19:15:54` ledger | 0; "A moved substrate needs a re-pin, never a re-interpretation of the old table."; 19:15:54 → no hit | S2 |
| 4 | `grep -rn` across corpus/knowledge (25 inputs) | 0; duplicated by 5 and 7, so **not cited** (keeps cited inputs minimal) | — |
| 5 | `sed -n 185,238p` mutation-case (§5–§7) | 0; E4 "re-verification under the current `b56c6e57…` is **U**"; U3 "reproduction … is unmeasured" | S2 |
| 6 | `git grep` for the re-cut wording at rev over corpus/tools/SKILL.md | 0; the only hit for the b56c6e57 re-cut wording is SKILL.md:1077 (output head-capped) | S2 |
| 7 | fleet `git show 17c1fad:scripts/shokunin-watchdog.sh \| sed -n 1,16p`; live watchdog sha; `grep tameshi shokunin.conf`; live `jj-lane.sh:53-65`; `git grep 19:15:54` at rev | 0; `:3-5` round ends on report and "Tick 450s"; `:14` LANES has no tameshi; `shokunin.conf:55` names tameshi; live `:53-65` is usage text | S1 |
| 8 | `grep -n detect_branch` live jj-lane.sh; history; `detect_branch` at 14df5b9 and 67a3123 | 0; live `:115`; 67a3123 `:53` | S1 |
| 9 | sweep by git blob id (wrong method: the pins are content sha256) plus a rev map; its `$F/*-shokunin` glob ran `git cat-file`/`ls-tree` in the **live lane .git** (4 bound `.git` reads, read-only) | 0; superseded by 10/18, so **not cited** | — |
| 10 | content-sha256 sweep of every blob at the stated revs; branch-tip blobs | 0; all 8 pins HIT at the stated path; tsukuroi tip `d17d32a3`, mado tip `1036d100` | S1, S2 |
| 11 | `git show` on the five harness shas as commit names | 0; "unknown revision" for all five (they are content pins, not commits) | S2 |
| 12 | sha256 of `tools/mutate-and-run.sh` at every commit that touches it | 0; `597e1419` b58b26fb 16:57:18Z · `b56c6e57` 44947154 18:17:26Z · `cf41efaa` 9f1d3c33 19:06:31Z · `75ed934d` 606716f7 21:28:23Z (all 2026-10-14) | S1, S2 |
| 13 | scratch-repo rule falsifier; its `git -C $C status` hashed 2,194 racily-clean tracked files, including L1-appended files | 0; superseded by 18, so **not cited** | — |
| 14 | `git grep 4dc69ef9\|e3f838d4` and `b56c6e57` at rev; harness grep for SETUP/doctored/git-writes; §9; `uname -n`; `ls /tmp/w8-tameshi-t84` | 0; corpus/tools hits = none (rc 1); `plazir27`; `/tmp/w8-tameshi-t84` absent | S1, S2 |
| 15 | sibling identity; pin read now; tick-window commits; dc864c6a search; live-gate copy | 0; see the sections below; dc864c6a found in 0 of 17 commits | S1, S2 |
| 16 | commits between each stated HEAD and 19:15:14Z; clean-gate falsifier; FLEET_ROOT derivation; cf41efaa arms | 0; no commits in any gap; untouched → current, +1 line → drift, porcelain 0 | S1 |
| 17 | `bash tools/mutate-and-run.sh --regression` (0ff2734); cf41efaa `--selftest` and `--regression` (a fleet2 mirror at lane 9f1d3c33); current `--selftest` | all rc 0; `REGRESSION: PASS (cases=7 passed=7…)`; `MUTATE_SELFTEST: 67/67 pass`; `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)`; `MUTATE_SELFTEST: 95/95 pass`; clone porcelain 0 | S1, S2 |
| 18 | scratch-repo rule falsifiers; `sed` service-optin-protocol.md:232 and operator-runbook.md:289-293; full ids and blob sha256 | 0; see below | S1, S2 |

## Section 1021 — `### The tick and the pin read` — instruction (with records) → **gap-minor**

### What I executed and what agrees

**The tick.** The fleet watchdog at fleet `17c1fad` (2026-09-29; blob `b8b01a78…`) says:
- `:3-5`: "A lane's round ends when .ufo/reports/round-<N>/<lane>.md lands; … Tick 450s." (`INTERVAL=450`).
- `:14`: `LANES="protocol aggregator kasegi kengaku kake kumitate kotoba kagi kama"`.
- The word `tameshi` appears 0 times in that blob.

The live watchdog loads lanes from `shokunin.conf` (`CONF=${SHOKUNIN_CONF:-"$SHOKUNIN_ROOT/shokunin.conf"}`, `:37`), and `shokunin.conf:55` is `tameshi|tameshi-shokunin|…` ✓.

**Reading rules (receipt 18, scratch repo).**
- `current`: `rev-parse --verify --quiet --end-of-options "refs/heads/master^{commit}"` rc 0; blob `5cf53845` == pin.
- `stale`: the recorded rev is an ancestor of the tip, and the tip blob `b7697fed` ≠ the pin.
- Unresolvable `<branch>`: rev-parse rc **1** (the page maps this to SETUP rc 2).
- Path absent at the tip: `git show` rc 128, so the equality fails.
- `drift`, uncommitted edit: porcelain shows 1 line.
- `drift`, detached-HEAD commit (the jj `@-` analogue): **porcelain 0**, yet the live file ≠ the `refs/heads/master` blob and HEAD is not on the branch. This confirms "a clean porcelain is not tip evidence".

**`<branch>`.** `master` for all four repos:
- kumitate and kagi have HEAD attached to master.
- tsukuroi is jj-colocated with a detached HEAD; `origin/HEAD` → master.
- mado has `lane.branch=master`.

At read time, the jj HEAD equalled `refs/heads/master` in both jj repos.

**Pin read now** (receipt 15, ≈18:20Z; the page says to re-run at each tick and never carry a reading):

```text
case                  rec rev   tip(master)  tip blob   pin        live      porcelain  reading
js-kimi-census        175de6ba  1770305f     5e8d5913   83016d45   5e8d5913  0          stale
bash-surface-census   fecee874  c2cab35b     275d8294   275d8294   275d8294  0          current
bash-tsukuroi-census  165307fe  661020f0     d17d32a3   084951be   d17d32a3  0          stale
bash-mado-verify      eead56b2  01b80946     1036d100   d7edaab4   071d39d9  1          stale + drift
kagi checklist-run    fecee874  c2cab35b     7e5ec98b   7e5ec98b   7e5ec98b  0          current
kumitate claims-check 175de6ba  1770305f     e9a21b44   e9a21b44   e9a21b44  0          current
```

That is 3 × `current` · 3 × `stale` · 1 × `drift`. The tool reads `moved`: `cf41efaa…` → `fb6d86d5…`.

Minutes later, mado's `master` moved to `0fa41252`, and its blob is the `071d39d9` bytes that had read as drift (receipt 18). This is a live example of "re-read, never carry".

**Executed-instance record (round-8 tick).**
- All 8 pin prefixes are the content sha256 of the named path at the named rev. Full ids are in receipt 18, e.g. `tsukuroi@165307fe…:tools/tsukuroi-census.sh` = `084951be…c78c5` and `mado@0c20a76f…:tools/mado-verify.sh` = `90d50cdd…`.
- The stale ancestry holds: `165307fe` ≤ `aa136d69` and `eead56b2` ≤ `0c20a76f`.
- The "live HEAD" column holds at 19:15:14Z. No commit landed on any ref between each stated HEAD and the tick:
  - tsukuroi `aa136d6` at 19:06:31Z; the next commit, `72b038d`, is at 19:55:09Z.
  - mado `0c20a76` at 19:06:31Z; the next commit, `12c8f08`, is at 19:55:09Z.
  - kumitate `175de6ba` at 09:56:19Z; kagi `fecee874` at 13:05:10Z.
- Tool `cf41efaa` is lane commit `9f1d3c33` (19:06:31Z); the next change, `75ed934d`, is at 21:28:23Z. So the tool was `held` at the tick.
- Host `plazir27` = `uname -n`. The 4/2/0 counts are consistent with the table.

**Re-read record.**
- The mtime 16:19:40 -0300 (19:19:40Z) falls between the tick and 19:20:29Z.
- The `dc864c6a` bytes were never committed (0 of 17 mado-verify.sh commits).
- Ledger `:302` corroborates the row.

**Falsifiers.** On the live clean gate kagi `corpus/checklist-run.sh` (receipt 16):
- The untouched scratch copy `7e5ec98b` == the master blob → `current`.
- The copy with one appended line, `f1db5278`, → `drift`.
- kagi porcelain shows 0 lines after.

Superseded-blob cases read `stale` (tsukuroi, mado, and now kimi-census). The doctored arm exists in cf41efaa (`regression engine fails a doctored table`, `regression pin mismatch is SETUP (exit 2)`). cf41efaa `--selftest` gives `MUTATE_SELFTEST: 67/67 pass`, `VERDICT: PASS`, rc 0 ✓.

### Minor gaps

1. **Stale anchor.** `../scripts/hyaku/jj-lane.sh:53-65` was `detect_branch` only in fleet `67a3123` (v1, exact 13 lines).
   - Fleet `14df5b9` landed at 16:05:01Z, after the page landed at `2a22ade` (15:54:21Z) and before `0ff2734` (16:45:39Z).
   - It moved `detect_branch` to `:115`; `:53-65` is now usage text.
   - It also narrowed the function to init-only, attached HEAD else `origin/HEAD`, with no master/main fallback. `state` now prefers `git config lane.branch`.
   - The resolved branch is still `master` everywhere, so the readings are unaffected.
2. **"unresolvable `<branch>` → SETUP rc 2" names no emitter.** The named jj-lane.sh exits 0/1/3/64, and `git rev-parse --verify --quiet` exits 1 (measured). A reader must assign rc 2 by hand.
3. **`MUTATE_SELFTEST: 67/67` is unpinned.** It is true at cf41efaa (measured). The harness at 0ff2734 (`fb6d86d5…`) reports **95/95**.
4. **The cited round-8 evidence is gone.** `/tmp/w8-tameshi-t84/` (`pin-read.txt`, `drift-demo.txt`) no longer exists, and the re-read's `dc864c6a…` bytes were never committed. Every checkable claim was re-derived from git objects instead.

## Section 1069 — `### Triggers T1–T3 and the re-pin rule` — instruction (with records) → **gap-minor**

### What I executed and what agrees

**T1.** Three cases read `stale` today. I record the STALE cells here and edit no table. The reason is the same for each: the recorded rev is an ancestor of `master` and the tip blob differs.
- `js-kimi-census` `83016d45`@`175de6ba` → `1770305f` / `5e8d5913`.
- `bash-tsukuroi-census` `084951be`@`165307fe` → `661020f0` / `d17d32a3`.
- `bash-mado-verify` `d7edaab4`@`eead56b2` → `0fa41252` / `071d39d9`.

These were not re-measured at the live revisions; the page allows recording the STALE cell instead.

The T1 record checks out:
- The ledger `:47`/`:48` rates 6/10 and 4/10 at those pins.
- `bba6cdf6`@`aa136d69` and `90d50cdd`@`0c20a76f` are exact.
- "Both have moved again since" ✓.

**T2, executed.** The harness is now `fb6d86d5…` ≠ `cf41efaa…` (round-8 replay) ≠ `597e1419…` (the mado table's revision). I re-ran the reproduction under the new revision:
- `REGRESSION: PASS (cases=7 passed=7; ledger legs exact: killed-delta<=0 flips<=0)`, rc 0, `REGRESSION_TOOL … sha256=fb6d86d59b5c9285…`.
- Every leg reads `match=N/N … flips=0`; the mado leg reads `match=10/10 recorded-killed=4 measured-killed=4 … flips=0`.
- Both pins recorded: old `cf41efaa8be5f52d…`, new `fb6d86d59b5c9285…`.

**T3.** Ledger `:170-173` is verbatim support ✓.

**Re-pin rule.** SKILL.md:811-812 ✓.

**Round-8 replay receipt, reproduced under cf41efaa itself today.** I ran it in a `/tmp` fleet mirror at lane `9f1d3c33`; both harness revisions derive `FLEET_ROOT` from their own path.
- `REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0)`, rc 0, every leg `match=10/10 … flips=0`. This is the exact line.
- "The recorded tables hold at their own pinned blobs regardless of the live drift" ✓. Both harness revisions pass while 3 cases read stale and mado had drifted.

### Minor gaps

1. **The T2 precedent is mis-anchored.**
   - `mutation-case-mado-verify.md:17-23` records the `597e1419`→`b56c6e57` re-pin, but leaves reproduction under `b56c6e57` **U** (also E4 `:199-200` and U3 `:230-231`, "unmeasured").
   - The identical-verdicts / mutant-shas re-cut is recorded instead at `corpus/knowledge/service-optin-protocol.md:232`: "SCR-T6 re-ran the spec under `b56c6e57…`: 4/10, all ten mutant shas identical". It also appears at `operator-runbook.md:291-292`. The range names neither file.
2. **The harness chain `597e1419… → b56c6e57… → 4dc69ef9… → e3f838d4… → cf41efaa…` is partly uncorroborated.**
   - Only `597e1419`, `b56c6e57` and `cf41efaa` are committed blobs. The committed same-day chain is `d8abee52→597e1419→b56c6e57→cf41efaa→75ed934d`.
   - `4dc69ef9` and `e3f838d4` appear in no corpus/ or tools/ file (git grep rc 1).
   - By file name only, they appear in SKILL copies, the unnamed `.ufo/evidence/round-17/tool-pin-map.json`, `plans/round-8.plan.md` and wave reports. [INFERENCE] They are uncommitted live-tree states.
3. **The 19:15:54Z receipt is not retained at any cited path.** It appears only in SKILL copies. The ledger carries the same PASS line at 19:14:16Z (`:281`) and 19:58:18Z (`:341`), and the line reproduced exactly today.

## Hygiene, deviations and tooling

- I ran no jj and no git write in the lane or the siblings. `GIT_*` was never exported. Sibling status reads used `--no-optional-locks`.
- I touched the live lane only:
  - for the contract clone;
  - through receipt 9's read-only `.git` queries (4 bound `.git` reads; receipt not cited);
  - through the instructed `assemble.py` validation.
- The harness's own mktemp template ignores `TMPDIR`. It created `/tmp/tameshi-r4-2-regression.{IOkUSK,kbiEEl}`, and both were removed on PASS.
- The mado gate's selftest leaked 8 `/tmp/w5-mado-m52-selftest.*` dirs: 4 per mado leg (`killed=4`) inside my two leg windows (18:26:57–18:27:04Z and 18:30:05–18:30:11Z). [INFERENCE: attributed by timing.] This is the same leak the mado note's U4 records. I removed those 8 exact paths.
- Receipts 4, 9 and 13 stay on disk but are not cited, for the reasons above.
- Tools installed or updated: none.

## Validation

`python3 $C/.ufo/evidence/round-17/coldread/assemble.py --reports /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-17/w3/RR2.md --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --out /tmp/tameshi-r17w3-RR2-hnbkmZ/RR2.json`
- Exit 1. The only cause is coverage: this one report covers 2 of 58 buckets.
- `rejected reports: none`; `ledger written: … (2 entries)`.
- `1021-1068 instruction gap-minor ### The tick and the pin read`: sha256 `66fdb741…`, commands 10, traces 10, 6 inputs.
- `1069-1091 instruction gap-minor ### Triggers T1–T3 and the re-pin rule`: sha256 `6eb7f28d…`, commands 12, traces 12, 6 inputs; `inputs_dropped: ["SKILL.md"]` from receipt 3, as designed.

**Verdict: holds (gap-minor ×2).** Both buckets execute from the page at 0ff2734, with no wrong expectation and no blocking gap. The only defects are four plus three minor anchor/record gaps.

```json
{"schema":"tameshi-coldread-report-v2","seat":"RR2","skill_sha256":"de6c2b083be6f35d2c35e011ca37874f57204a2cdd195a106ff638fbea723dbc","read_rev":"0ff273448ac4e62893c9b28a4cea7c580712df19","sections":[{"start":1021,"heading":"### The tick and the pin read","class":"instruction","verdict":"gap-minor","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["Stale anchor: `../scripts/hyaku/jj-lane.sh:53-65` is detect_branch only in fleet 67a3123 (v1); fleet 14df5b9 (2026-10-20T16:05:01Z, before lane 0ff2734 at 16:45:39Z) moved it to :115 (lines 53-65 are now usage text) and narrowed it to init-only attached-HEAD-else-origin/HEAD with `state` preferring git config lane.branch; the resolved branch is still master for all four repos, so readings are unaffected","`unresolvable <branch> -> SETUP rc 2` names no emitting tool: the named jj-lane.sh exits 0/1/3/64 and `git rev-parse --verify --quiet` exits 1 (measured), so rc 2 is a convention the reader assigns by hand","`selftested MUTATE_SELFTEST: 67/67` is unpinned: measured 67/67 PASS at the round-8 tool cf41efaa, but the harness at 0ff2734 (fb6d86d5) reports 95/95 PASS","Executed-instance evidence is ephemeral: /tmp/w8-tameshi-t84/ (pin-read.txt, drift-demo.txt) no longer exists and the re-read's dc864c6a bytes were never committed (0 of 17 mado-verify.sh commits); corroborated only by fleet-kill-rate-ledger.md:302"],"commands_executed":["trace 1: sed -n 165,180p and grep of corpus/knowledge/fleet-kill-rate-ledger.md for REGRESSION PASS lines and pins (tick-table corroboration :301-302, :328-337)","trace 7: git -C <fleet> show 17c1fad:scripts/shokunin-watchdog.sh | sed -n 1,16p; sha256 of that blob and of the live watchdog; grep -n tameshi shokunin.conf; sed -n 53,65p live scripts/hyaku/jj-lane.sh","trace 8: grep -n detect_branch live jj-lane.sh; git log --follow jj-lane.sh; detect_branch at 14df5b9 and 67a3123","trace 10: content-sha256 sweep of every blob at 175de6ba/fecee874/165307fe/aa136d69/eead56b2/0c20a76f for the 8 pins; branch-tip blobs now","trace 12: sha256 of tools/mutate-and-run.sh at every lane commit touching it, with dates (tool at the tick = cf41efaa)","trace 14: grep SETUP/doctored/regression/git-write surface in tools/mutate-and-run.sh; uname -n; ls /tmp/w8-tameshi-t84","trace 15: sibling lane.branch/.jj/HEAD/refs; pin read now with the page's rules (rev-parse --verify --quiet --end-of-options refs/heads/master^{commit}, git show tip:path | sha256sum, live sha256, git --no-optional-locks status --porcelain -- path, merge-base --is-ancestor); tick-window commits; dc864c6a search over 17 commits; live-gate copy plus one line","trace 16: git log --all between each stated live HEAD and 19:15:14Z; kagi corpus/checklist-run.sh untouched copy vs copy plus one line vs master blob, porcelain after; FLEET_ROOT derivation in cf41efaa and current harness; cf41efaa doctored arms","trace 17: bash tools/mutate-and-run.sh --regression (0ff2734); cf41efaa harness --selftest (67/67 PASS) and --regression in a /tmp fleet mirror at lane 9f1d3c33; current --selftest (95/95 PASS)","trace 18: scratch-repo falsifiers for current/stale/unresolvable branch/path absent/drift uncommitted/drift via detached-HEAD commit; full 40-hex ids and blob sha256 for every pin"],"opened":["corpus/knowledge/fleet-kill-rate-ledger.md","tools/mutate-and-run.sh","/home/vgpnk/Projects/shokunin/scripts/shokunin-watchdog.sh (live and @17c1fad)","/home/vgpnk/Projects/shokunin/shokunin.conf","/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh (live and @67a3123)","kumitate/kagi/tsukuroi/mado gate files (live and git objects at the stated revs)"],"inputs":{".gitignore":"0f699af0108f1ac4f43cd5f61c9151896b8328ec7edd0adf4ca1c638a2441116","tools/mutate-and-run.sh":"fb6d86d59b5c9285864c9ebfa19d5a6f8938e91c47877a6d25b451a1da03001a","corpus/knowledge/fleet-kill-rate-ledger.md":"ac7f69d928e5ba0fb687821c2a2c0900e1375a8454901a285874735e35c21033","corpus/knowledge/mutation-case-mado-verify.md":"f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3","corpus/knowledge/operator-runbook.md":"531571cb110fdafb57b9abe5a6532ddceaf5fcdea582d8081f1eb3391ae97397","corpus/knowledge/service-optin-protocol.md":"84d0c1547eed257d921b832468d6f010bcca331e8ce67ed378852d7993da8e0e"},"external_inputs":{"/home/vgpnk/Projects/shokunin@17c1fadfddc5ecbfa5ef362ef44d111792fa3e94:scripts/shokunin-watchdog.sh":"b8b01a78b9f66e343a6d5eefd027622b3c3718f79db2c7c06bb69c047fbe2226","/home/vgpnk/Projects/shokunin@67a3123e83a89be56b4be94435e4633ae38aacef:scripts/hyaku/jj-lane.sh":"2479041653c6a77c6cca099a37948d6c16361173c68fb14c8c2e2feae9dc2b1d","kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs":"83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426","kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/claims-check.mjs":"e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b","kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh":"275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f","kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/checklist-run.sh":"7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf","tsukuroi-shokunin@165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh":"084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5","tsukuroi-shokunin@aa136d69e0e4666b86782152cd1d1fa00f90a0b3:tools/tsukuroi-census.sh":"bba6cdf6f5b7a7372e43230821bb7c12aa64192266c549f39475c948803a4f55","mado-shokunin@eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh":"d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13","mado-shokunin@0c20a76fa5ff985047c8ca2d455c75179c3dd0d1:tools/mado-verify.sh":"90d50cdd4d18410bd1e4222e12f566986c5d8d8cfdffd6f86864a3de5a3100bd","tameshi@9f1d3c339a7094968041c7708a65dbf7eab9fae6:tools/mutate-and-run.sh":"cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75"},"traces":[".ufo/evidence/round-17/coldread/traces/RR2/1.json",".ufo/evidence/round-17/coldread/traces/RR2/7.json",".ufo/evidence/round-17/coldread/traces/RR2/8.json",".ufo/evidence/round-17/coldread/traces/RR2/10.json",".ufo/evidence/round-17/coldread/traces/RR2/12.json",".ufo/evidence/round-17/coldread/traces/RR2/14.json",".ufo/evidence/round-17/coldread/traces/RR2/15.json",".ufo/evidence/round-17/coldread/traces/RR2/16.json",".ufo/evidence/round-17/coldread/traces/RR2/17.json",".ufo/evidence/round-17/coldread/traces/RR2/18.json"]},{"start":1069,"heading":"### Triggers T1–T3 and the re-pin rule","class":"instruction","verdict":"gap-minor","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["T2 precedent is mis-anchored: mutation-case-mado-verify.md:17-23 records the 597e1419->b56c6e57 re-pin but leaves reproduction under b56c6e57 U (also E4 :199-200, U3 :230-231 'unmeasured'); the identical-verdicts/mutant-shas re-cut is recorded at corpus/knowledge/service-optin-protocol.md:232 (SCR-T6: 4/10, all ten mutant shas identical) and operator-runbook.md:291-292, which the range does not name","Harness chain 597e1419 -> b56c6e57 -> 4dc69ef9 -> e3f838d4 -> cf41efaa: only 597e1419/b56c6e57/cf41efaa are committed blobs of tools/mutate-and-run.sh (committed same-day chain d8abee52->597e1419->b56c6e57->cf41efaa->75ed934d); 4dc69ef9/e3f838d4 appear in no corpus/ or tools/ file (git grep rc 1), only in SKILL copies, the unnamed .ufo/evidence/round-17/tool-pin-map.json, plans/round-8.plan.md and wave reports, so they are uncorroborated from the page's reach","Round-8 replay receipt timestamp 19:15:54Z is not retained at any cited path (found only in SKILL copies); the ledger carries the same PASS line at 19:14:16Z (:281) and 19:58:18Z (:341), and the line reproduces exactly under cf41efaa today"],"commands_executed":["trace 1: sed -n 165,180p corpus/knowledge/fleet-kill-rate-ledger.md (T3 :170-173); grep -n 'REGRESSION: PASS'; grep T1 pins and rates (:47-48)","trace 2: sed -n 12,26p corpus/knowledge/mutation-case-mado-verify.md (T2 citation); grep -n b56c6e57","trace 3: sed -n 811,812p SKILL.md (named by the range as :811-812); grep -n 19:15:54 ledger","trace 5: sed -n 185,238p corpus/knowledge/mutation-case-mado-verify.md (E4, U3)","trace 6: git grep re-cut / identical verdicts / mutant shas at 0ff2734 over corpus, tools, SKILL.md","trace 10: branch-tip blobs of tsukuroi and mado now (moved again since)","trace 11: git show <harness sha> as commit names -> unknown revision (content pins, not commits)","trace 12: sha256 of tools/mutate-and-run.sh at every lane commit touching it (committed chain and dates)","trace 14: git grep 4dc69ef9|e3f838d4 (corpus/tools rc 1; file names elsewhere) and b56c6e57 at 0ff2734; sed -n 262,300p mutation-case §9","trace 15: pin read now across the six cases (T1 trigger evaluation: 3 stale)","trace 17: T2 executed - bash tools/mutate-and-run.sh --regression at 0ff2734 -> REGRESSION: PASS (cases=7 passed=7), rc 0; cf41efaa harness --regression -> REGRESSION: PASS (cases=4 passed=4; ledger legs exact: killed-delta<=0 flips<=0), every leg match=10/10 flips=0, rc 0","trace 18: sed -n 232p corpus/knowledge/service-optin-protocol.md; sed -n 289,293p corpus/knowledge/operator-runbook.md; full 40-hex ids and blob sha256 for the harness and gate pins"],"opened":["corpus/knowledge/fleet-kill-rate-ledger.md","corpus/knowledge/mutation-case-mado-verify.md","SKILL.md:811-812 (named by the range)","corpus/knowledge/service-optin-protocol.md","corpus/knowledge/operator-runbook.md","tools/mutate-and-run.sh (and git objects at b58b26fb, 44947154, 9f1d3c33)"],"inputs":{".gitignore":"0f699af0108f1ac4f43cd5f61c9151896b8328ec7edd0adf4ca1c638a2441116","tools/mutate-and-run.sh":"fb6d86d59b5c9285864c9ebfa19d5a6f8938e91c47877a6d25b451a1da03001a","corpus/knowledge/fleet-kill-rate-ledger.md":"ac7f69d928e5ba0fb687821c2a2c0900e1375a8454901a285874735e35c21033","corpus/knowledge/mutation-case-mado-verify.md":"f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3","corpus/knowledge/operator-runbook.md":"531571cb110fdafb57b9abe5a6532ddceaf5fcdea582d8081f1eb3391ae97397","corpus/knowledge/service-optin-protocol.md":"84d0c1547eed257d921b832468d6f010bcca331e8ce67ed378852d7993da8e0e"},"external_inputs":{"tameshi@b58b26fbeba8fd972e1d31ac8a9175a81e333b32:tools/mutate-and-run.sh":"597e141989065e038a1c2b35359ab3d20b565d3c959c2eec64166ecb1ff6331b","tameshi@44947154c23772f766f9f5439090fb5c7ad76e46:tools/mutate-and-run.sh":"b56c6e57f1b7ae91c85f06ee101d3a348158ab219fae4a16f5d3e6f77fd22bcb","tameshi@9f1d3c339a7094968041c7708a65dbf7eab9fae6:tools/mutate-and-run.sh":"cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75","tsukuroi-shokunin@165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh":"084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5","tsukuroi-shokunin@aa136d69e0e4666b86782152cd1d1fa00f90a0b3:tools/tsukuroi-census.sh":"bba6cdf6f5b7a7372e43230821bb7c12aa64192266c549f39475c948803a4f55","tsukuroi-shokunin@661020f077f510e5ec3bc8d3799fecda2e9125bc:tools/tsukuroi-census.sh":"d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e","mado-shokunin@eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh":"d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13","mado-shokunin@0c20a76fa5ff985047c8ca2d455c75179c3dd0d1:tools/mado-verify.sh":"90d50cdd4d18410bd1e4222e12f566986c5d8d8cfdffd6f86864a3de5a3100bd","mado-shokunin@0fa412525f8e9f9a7489276da3e35f07637919b9:tools/mado-verify.sh":"071d39d99aa94d9e3d0c0a8c9d9e9e98b4bc79b51af0703e4dba774f85f7c75d","kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs":"83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426","kumitate-shokunin@1770305fae20826b39905a8251ddeca6b4957ac4:scripts/kimi-census.mjs":"5e8d591324064fff714fb85b9d254b726deb9fd9cf15261eba135ccff6db3dc0"},"traces":[".ufo/evidence/round-17/coldread/traces/RR2/1.json",".ufo/evidence/round-17/coldread/traces/RR2/2.json",".ufo/evidence/round-17/coldread/traces/RR2/3.json",".ufo/evidence/round-17/coldread/traces/RR2/5.json",".ufo/evidence/round-17/coldread/traces/RR2/6.json",".ufo/evidence/round-17/coldread/traces/RR2/10.json",".ufo/evidence/round-17/coldread/traces/RR2/11.json",".ufo/evidence/round-17/coldread/traces/RR2/12.json",".ufo/evidence/round-17/coldread/traces/RR2/14.json",".ufo/evidence/round-17/coldread/traces/RR2/15.json",".ufo/evidence/round-17/coldread/traces/RR2/17.json",".ufo/evidence/round-17/coldread/traces/RR2/18.json"]}]}
```
