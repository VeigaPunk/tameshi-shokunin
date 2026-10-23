# Round-35 w2 — AttackTailHarness

Seat: `AttackTailHarness` (leaf mutation-tester, godspeed). Lane pin at dispatch: `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b` (scratch clone, read-only).

Frozen bytes, sha256, re-read after all work (all three unchanged):

- `tools/mutate-and-run.sh` `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9`
- `tools/tally-audit-v3.py` `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885`
- `tools/tally-audit-v2.py` `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10`

Attacked: the runner's tally selftest harness — the region `tally-audit-v3.py` brackets with `HARNESS_START` (`local tblock`, runner 1992) and `HARNESS_END` (`tblock=$tblock_full`, runner 2040) — plus the question the seat asks: what does `check_harness` actually certify, what is it blind to, and can an accepted copy change real runner behaviour?

Method: 23 harness-region edits on the frozen runner. Every copy's **tally block bytes are verified unchanged** with the runner's own extraction rule (`awk '/^  local nlegs=9 …/{f=1} f&&/^}$/{exit} f'`) before any audit. Each copy then scored by (a) `check_harness` directly, (b) the full `tally-audit-v3.py` audit, (c) the full `tally-audit-v2.py` audit, (d) the frozen C1 counter's own `behavior()`/`diverge()`/`score_copies()`.

No installs. Scratch: `/fast/scratch/hyaku/tameshi-r35-seats/AttackTailHarness/` (`work/probe.py`, `work/hmatrix.py`, `work/verify.py`, `work/score_demo.py`, copies under `work/copies/`, `st/`). Nothing written under `/home/vgpnk/Projects/shokunin/` except this report. No git mutation; lane worktree clean at the end (0 porcelain lines, HEAD `7da6e076…`).

---

## Headline

| # | rank | finding |
|---|---|---|
| F1 | **CRITICAL** (contract surface) | **C1's accept side is false.** C1 defines an accept specimen as behaviourally identical on every config and vector; the frozen counter's ground truth is the **tally block's behaviour**. A rename-only refactor (`st_kagi`→`st_surface`, 3 tokens) and a harness edit are therefore accept specimens by definition — and v3 rejects both (`rc=1 checks=harness`), as it rejects **9 of my 22** harness edits. Scored through the counter's own `score_copies`: `valid=True pass=False`. If any sealed accept copy renames a leg or touches the harness region, `ho_accept` drops and `C1_R35_PASS=false`. |
| F2 | **BOUND** (fail-closed) | `check_harness` certifies text, not the live harness. (a) A byte-equality stub (injected block == the file's own block) does **zero behavioural testing** yet `TALLY_AUDIT: PASS`, selftest green at **99/99**. (b) `harness_section()` takes the **first** `local tblock` in the file, so a dead decoy function placed before `selftest()` satisfies the panel while the live harness is the stub: `check_harness PASS reference cases=9; faults rejected=34/34`, full audit **exit 0**, selftest **99/99**. v2 accepts both identically. |
| F3 | **BOUND** (fail-closed) | An accepted weakening (status-2 positional sweep dropped) **masks a real tally defect in the runner's own `--selftest`**: same defect, pristine harness → `--selftest` exit **1** (105/106); weakened harness → exit **0** (105/105). The full audit still kills the combined copy on `runtime`. |
| F4 | **BOUND** (fail-closed) | The harness panel never runs an injected block under more than one config: the reference harness pins `auto=0 KEEP=1` (runner 2003). A defect gated on `auto==1 && KEEP==0` — the runner's real default — escapes the **pristine** harness `(9,0)`. `check_runtime` kills it (`P+F2`: v3 exit 1, check `runtime`, only config `(1,0)` diverged). |
| F5 | **BOUND** (scope, by construction) | The cheapest copy that changes real runner behaviour and is ACCEPTED: `regression_case_git() { return 0 … }` — every regression leg trivially passes, `--regression` can no longer fail a leg. v3 exit **0**, v2 exit **0**, counter `ACCEPT(identical)`. This is *correct* under C1 because the counter's ground truth is `behavior()` = tally block only (`c1-measure.py:204-216`); it is the documented limit of the claim, not a falsification. |
| F6 | **no regression found** | `faults()`, `harness_section`+`run_harness`+`check_harness` are **byte-identical** in v2 and v3 (sha256 of the extracted regions below). All 23 mutants scored identically by both tools. No class v2 caught and v3 accepts exists on this surface at this pin. |
| F7 | **HYGIENE** (observation, not my write) | The shared fleet worktree at the time of writing carries uncommitted peer edits: `tools/tally-audit-v3.py` = `55601416a193a2e9…` (pinned `ef98fc53…`), `.ufo/evidence/round-35/c1/c1-measure.py` = `53c4a4e7b51d289d…` (frozen `515b0b1b…`), `contract.json` modified. Committed bytes at `7da6e076` are still the frozen ones (`git show HEAD:…` → `ef98fc53…`, `a7d3f2dd…`). All measurements here were taken against my own clone of the pin (clean worktree, counter `515b0b1b…`), never the shared worktree. If the single C1 run is taken from the worktree rather than the pin, `tool_sha_ok`/`runner_sha_ok` will disagree with the freeze. |

---

## F1 — CRITICAL: C1's accept predicate is narrower than the tool's acceptance criterion

C1 (`contract.json`, claim C1) says the tool "accepts every accept specimen (behaviourally identical on every config and vector)". The frozen counter computes an accept copy's verdict as (`c1-measure.py:309-310`):

```python
row['valid'] = not div                                  # div = behaviour() divergence, tally block only
row['pass']  = (not div) and rc == 0
```

`behavior()` (`c1-measure.py:204-216`) extracts **the tally block** and runs `vectors_for(n)` under the four configs. It never reads the harness. So **any** harness-region edit is `div=[]`, `valid=True` — an accept specimen under the contract's own definition — and v3's `harness` check then decides `rc`.

Measured, through the counter's own scoring function (`work/score_demo.py`):

```text
COPY accept harness-skip-position8 (accept, behaviorally inert) demo.json div=- rc=1 checks=harness pass=False
COPY accept harness-tnames-literal (accept, behaviorally inert) demo.json div=- rc=0 checks=-        pass=True
COPY kill  tally-setup8-zero (kill)                             demo.json div=(1,0),(1,1),(0,1),(0,0) rc=1 checks=runtime pass=True
```

The first line is a behaviourally inert copy (`for ti in 0…8` → `0…7 7`, one character of the position loop; tally block byte-identical, sha `adf6763d6524f342b5496ff52f0fce96e0b4a00b5ab26cfa43be2001654b36d0`) that the counter scores as a **failed accept copy**. Full audit: `TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)` / `EXIT=1`, `CHECK harness FAIL reference cases=9; faults rejected=32/34; accepted: ignore-st_citecheck ignore-alone-st_citecheck`.

Of 22 applicable harness edits (all with a byte-identical tally block), **9 were rejected**: `M01` (skip position 8), `M02` (skip position 0), `M04` (drop status-3 vector), `M06` (drop two-fail vector), `M07` (drop two-setup vector), `M08` (drop all-pass case), `M09` (drop guard stress), `M10` (exit only), `M11` (line only). Each becomes `pass=False` if authored as a sealed accept copy. The rejection is not evidence of a defect in the copy; it is the harness check doing its job against a ground truth the contract does not use for accept specimens.

**The cleanest instance needs no harness edit at all.** `R3-rename-leg-consistent` renames one leg variable consistently (3 occurrences: the `local` declaration, the bare `st_kagi=$?`, the tally-loop operand), copy sha `4bc9a1ac25a8382ae312976a4121d6ad7dcea63cbf57cc9360e5e1bf5b99872c`:

```text
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=30316 mismatched=0
CHECK harness FAIL leg names differ from the reference panel (st_js st_surface st_tsu …)
TALLY_AUDIT: FAIL (head=pass static=pass runtime=pass harness=fail)   (exit 1)
```

- Runner's own selftest on the same copy (`bash copies/R3-rename-leg-consistent.sh --selftest`): **exit 0**, `MUTATE_SELFTEST: 106/106 pass`, `VERDICT: PASS`.
- Frozen counter: `COPY accept rename-leg-consistent demo-rename.json div=- rc=1 checks=harness pass=False`.

So a refactor that changes **nothing** observable — head, static and the 30 316-vector runtime sweep all pass, and the runner's own 106 cases pass — is scored as a failed accept copy, solely because `check_harness` pins `REF_NAMES` (`tally-audit-v3.py:665-666`). This is the highest-probability way for the sealed set to make C1 read false, and it needs no sealed author to know anything about the tool.

Symmetric hazard on the kill side (`c1-measure.py:307`): `row['pass'] = bool(div) and rc == 1 and failed == ['runtime']`. A kill copy that *also* carries a harness edit fails a second check and is scored `pass=False` even though its tally behaviour diverges. Sealed kill copies must be confined to the tally block.

**Action implied, not taken (contract is frozen, and this seat does not amend it):** the sealed-authoring rule must either forbid harness-region edits in both sets, or C1's accept sentence must be read as "behaviourally identical **and** harness-panel clean". As written, the sentence is false for a permitted copy class, so the upcoming single C1 run is at risk from an authoring choice, not from a tool defect.

---

## F2 — BOUND: `check_harness` cannot tell behavioural testing from a byte-equality stub

The panel's reference block (`REF_BLOCK`, v3:100-139) is **byte-identical to the runner's own tally block**. Therefore the predicate "accept REF, reject every fault" is satisfied by an equality test:

```bash
local tblock_full=$tblock
[[ "$tblock" == "$(awk '/^  local nlegs=9 npass=0 nfail=0 nsetup=0 st$/{f=1} f&&/^}$/{exit} f' "$SELF")" ]]
st 'tally harness: block matches the file text' $?
tblock=$tblock_full
```

`work/probe.py` mutant `M23-tautology-block-compare` replaces the whole `tally_line` machinery (24 `tally_line` call sites) with those 3 statements, keeping the extraction line so `EXTRACT_RE` still matches. Copy sha `84036c29e76a0e7123d42797a746b4af20d79effc7fe262fcca7524eb9e6e74a`; tally block pristine (`True`).

- `check_harness`: **ACCEPTED** — `reference cases=2; faults rejected=34/34`.
- Full v3 audit: **exit 0** — `CHECK harness PASS reference cases=2; faults rejected=34/34` / `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`.
- Full v2 audit: **exit 0** (same detail).
- Counter: `ACCEPT(identical)`.
- Real runner behaviour: `bash work/st/M23.sh --selftest` → **exit 0**, `MUTATE_SELFTEST: 99/99 pass`, `VERDICT: PASS`; the only tally-harness cases left are `block extracted` and `block matches the file text`.

The runner now ships a tally selftest that can never fail, and the audit says `harness=pass`. Why the panel cannot see it: in the tool's wrapper the injected block is `AUDIT_INJECT` (strict compare, all faults differ → rejected); in the runner's own run `tblock` is the awk extraction of `$SELF`, so the comparison is `x == x` — a tautology. This is not the "abort counted as reject" limit already recorded by the w2 scout (`ScoutHarnessRegion.md`, BOUND — abort is scored as a reject); this harness never aborts, returns `cases=2 failed=0`, and its own selftest is green.

`cases=2` is accepted because `check_harness` (v3:669) requires only `cases>0 and failed==0` for the reference; nothing pins `cases==9`.

**Structural variant (R4): the check reads the wrong text.** `harness_section()` uses `HARNESS_START = ^[ \t]*local tblock\b` with `.search()` over the **whole file** (v3:619), not the region inside `selftest()`. Any earlier function that declares `local tblock` — a plausible refactor artefact — hijacks it. `R4-relocated-decoy-harness` (sha `d3cd107cf454a8b2b1578e75664b3535cfeea7e363c5cd1b1801d71c4841371c`) puts the pristine strict harness body inside a never-called `tally_selftest_strict()` defined immediately before `selftest()`, and leaves the live harness as the M23 tautology:

```text
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)   (v3 exit 0; v2 exit 0)
COPY accept relocated-decoy-harness demo-r4.json div=- rc=0 checks=- pass=True   (frozen counter)
bash copies/R4-relocated-decoy-harness.sh --selftest  -> exit 0, MUTATE_SELFTEST: 99/99 pass, VERDICT: PASS
```

The tool audits the dead function; the live harness has two cases, one of them tautological. `CHECK harness PASS` therefore certifies "some text in this file rejects the panel", not "the tally selftest rejects the panel".

---

## F3 — BOUND: an accepted weakening masks a real defect in the runner's own selftest; the audit still kills it

Edit `M03` = drop the status-2 positional entry of the per-position sweep:

```diff
-  for tvec in '1:1:…FAIL…' \
-    '2:2:…SETUP…'; do
+  for tvec in '1:1:…FAIL…'; do
```

Copy sha `ce2e1729e3a23a752327751002ee999264ad7869826b34ac0f0bf1df0facc916`; tally block pristine; `check_harness` **ACCEPTED** (`reference cases=8; faults rejected=34/34`); full v3 **exit 0**; full v2 **exit 0**; counter `ACCEPT(identical)`.

Real tally defect `F` = the block with `if [[ $st_citecheck == 2 ]]; then st_citecheck=0; fi` inserted after `local nlegs=…` (a single setup leg at index 8 reports PASS). End-to-end, the runner's real selftest:

| copy | command | exit | result |
|---|---|---|---|
| pristine | `bash st/pristine.sh --selftest` | 0 | `MUTATE_SELFTEST: 106/106 pass` / `VERDICT: PASS` |
| pristine + F | `bash st/PF.sh --selftest` | **1** | `MUTATE_SELFTEST: 105/106 pass`; `FAIL tally harness: one leg status 2 at each of 9 positions … (8/9)` |
| M03 + F | `bash st/M03F.sh --selftest` | **0** | `MUTATE_SELFTEST: 105/105 pass`; the status-2 case is **gone**, the defect is invisible |

Fail-closed proof: the same combined copy through the full audit — `M03+F`, v3 **exit 1**, `CHECK runtime FAIL`, `failed=['runtime']`; v2 identical. The harness check never participates in `check_runtime`, and the harness region is outside the audited function: `regression_body()` spans runner bytes 68425–75302 while the harness `local tblock` sits at byte 101921 (`True` inside `run_regression`? **False**). So a weakened harness can never make a defective tally block pass the audit; it only blinds the runner's own regression net.

Injected-fault matrix (`work/hmatrix.py`, the tool's own `run_harness`, `(cases, failed)`; `failed==0` = fault escapes):

| harness | REF | F-setup8 | F-auto `(1,0)` | F-prefix | F-stderr |
|---|---|---|---|---|---|
| pristine | (9,0) | (9,1) rejected | **(9,0) escapes** | (9,1) rejected | (9,8) rejected |
| M03 (accepted) | (8,0) | **(8,0) escapes** | (8,0) escapes | (8,1) rejected | (8,7) rejected |
| M12 (accepted) | (9,0) | (9,1) rejected | (9,0) escapes | **(9,0) escapes** | (9,8) rejected |
| M13 (accepted) | (9,0) | (9,1) rejected | (9,0) escapes | (9,1) rejected | **(9,0) escapes** |
| M14 (accepted) | (9,0) | (9,1) rejected | (9,0) escapes | (9,1) rejected | (9,8) rejected |

M12 = first-line comparison loosened to a prefix (`… == "$want_line"*`), sha `382bfd16c7d9f560b41f72518a99a7bf6c6185f4c06f352fe59f07f1109d7e1f`; M13 = `2>&1` dropped from `out=$(bash "$root/tally.sh")`, sha `896e6d0b29d823972d5a6d5461d4cb72749f5f9347ec4627b571c0d4acb756b3`; M14 = config pin `auto=0 KEEP=1` → `auto=1 KEEP=0`, sha `57e315c2649c772a60948782a6cb10401d5cac54ca8df7f5e266eab770c443b6`. All three `check_harness` ACCEPTED, full v3 and v2 exit 0.

---

## F4 — BOUND: the harness panel never sweeps `(auto,KEEP)`, and its own pin is not the runner's default

The reference harness writes `local root=selftest-tally auto=0 KEEP=1` (runner 2003). The runner's real `--regression` default is `(auto=1, KEEP=0)`. Consequences, measured on the **pristine, unmutated** harness:

- `F-auto` (`if [[ $auto -eq 1 && $KEEP -eq 0 ]]; then nfail=0; fi` before the fail check) → `(9,0)`, **escapes**. This is the round-35 fix-1 class (`cfg00-accept-swap`, `cfg11-pass-mask`, `workdir-branch-swap` in the public kill panel) — covered by `check_runtime`, never by `check_harness`.
- `faults()` (v3:569-616) contains **no config-gated fault**, so the panel cannot distinguish a harness that pins one config from one that pins another: `M14` and `M15` (`auto=1 KEEP=1`) are ACCEPTED.
- `P+F2` — the post-loop `auto==1 && KEEP==0 → nfail=0` gate in the tally block — diverges under exactly `(1,0)`; v3 **exit 1** `runtime`, v2 **exit 1** `runtime`. Fail-closed.

So the harness check's blind spots are: config, second stdout line, stderr, status set, and the non-tally cases in the same section. Each is independently covered by `check_runtime` (config/full stdout/status 0..255) except stderr and the non-tally cases, which are out of C1's ground truth by design.

---

## F5 — BOUND (scope, by construction): cheapest accepted real behaviour change

`R1-leg-fn-always-0` inserts `  return 0` after `regression_case_git() {` (runner 1332). Every one of the nine `st_<leg>=$?` captures then sees 0, so `--regression` can only print `PASS (cases=9 passed=9 …)`; a leg can never fail again. Copy sha `be49a9041ae9f2f5bb0c466a1ec1db63abc8d70c54c1da6b4f778d3c59517847`, tally block pristine.

- v3 **exit 0** (`head/static/runtime/harness` all pass), v2 **exit 0**, counter `ACCEPT(identical)`.

The class is closed *by construction*, not by the tool: `c1-measure.py:204-216` defines ground truth as the tally block's behaviour. Any change outside that block — leg bodies, the sweep, the fixture, the harness — has `div=[]` and is an accept specimen, so accepting it is consistent with C1. The same holds for `R2-drop-canary-cases` (the three `GIT_* scrub: canary …` assertions deleted, v3 exit 0, v2 exit 0) and `M19`/`M20` (`help exits 0`, `--regression refuses --target` cases deleted from inside the extracted harness section, v3 exit 0).

What the tool *does* guarantee is the arithmetic of the tally, not the integrity of the statuses fed into it. That is the honest limit of `CHECK runtime PASS vectors=30316`.

---

## F6 — What I could NOT break

1. **The tally block itself, even with a weakened harness.** `check_runtime` is independent of `check_harness`; `M03+F` and `P+F2` both die on `runtime` under v3 and v2. Boundary proof: harness region outside `regression_body()` (bytes 101921 vs 68425–75302).
2. **No v2→v3 regression on this surface.** The three regions are byte-identical between the tools (sha256 of the extracted text):

   | region | v2 | v3 | equal |
   |---|---|---|---|
   | `faults()` | `8f17f32d9f8ce118` | `8f17f32d9f8ce118` | yes |
   | `HARNESS_START` … `def audit(` (`harness_section`, `run_harness`, `shquote`, `check_harness`) | `0ccbecb6c47d2948` | `0ccbecb6c47d2948` | yes |
   | `run_harness` (`def run_harness(` … `def shquote(`) | `def0148f80249c76` | `def0148f80249c76` | yes |

   And empirically **every one of the 29 copies I scored** behaves identically under both tools — no disagreement anywhere:

   - v3 = v2 = **1 / `harness`** (10): `M01 M02 M04 M06 M07 M08 M09 M10 M11 R3`
   - v3 = v2 = **0** (16): `M03 M12 M13 M14 M15 M16 M17 M18 M19 M20 M21 M22 M23 R1 R2 R4`
   - v3 = v2 = **1 / `runtime`** (3): `M03+F`, `P+F`, `P+F2`
   - inconclusive (1): `M05` (my edit broke shell syntax; not counted)

   A "v2 caught, v3 accepts" class would have to come from the round-35 fixes (`code_view`, full stdout, four configs, real auto root); all four are stricter, and the harness panel did not change in round 35 — the v2/v3 runtime vector counts show the widening directly (`vectors=15158` vs `30316`, exactly ×2 for the config sweep).
3. **Positional coverage is enumerated; positional *status* coverage is not.** Skipping an index is caught, contrary to the assignment's example: `M01` (position 8 → 7) accepted faults `ignore-st_citecheck` + `ignore-alone-st_citecheck`; `M02` (position 0 skipped) accepted `ignore-alone-st_js`. The `ignore-alone-*` family fires at a lone status 1 **or** 2, so the retained status-1 sweep alone pins every index. That is exactly why dropping the status-2 positional sweep (`M03`) is invisible to the panel while the index coverage survives. Dropping the status-3 vector (`M04`) is caught by `status-3-passes`; the two-fail, two-setup, mixed, all-pass and guard vectors each have exactly one witness (`M06`–`M09` rejected). Note the w2 scout's independent measurement agrees on both single-arm drops (`ScoutHarnessRegion.md`, BOUND §"three asserts are not load-bearing").
4. **No over-kill of the public accept panel (by construction, not re-measured).** The public panel's three accept copies are comment-only edits (`panel/comment-brace.json`, `comment-esac.json`, `comment-names-leg.json`); the tool's own `selftest()` lists exactly those three shapes as exit-0 cases (`tally-audit-v3.py:781-783`). The only panel receipt at this pin is the v2 control (`.ufo/evidence/round-35/control/c1-v2-control.stdout`: `pub_kill=0/5 pub_accept=0/3`). I did **not** re-score the public panel with v3: the contract's kill rule allows exactly one default-mode C1 run, and the counter was used only at unit level (`score_copies`/`behavior`/`diverge`; `main()` never invoked, no `C1_R35` line produced). F1 is a hazard for the sealed set only.

## F7 — HYGIENE: frozen bytes vs the shared worktree

At the time of writing the shared fleet worktree (`/home/vgpnk/Projects/shokunin/tameshi-shokunin`) carries **peer** uncommitted edits: `tools/tally-audit-v3.py` hashes `55601416a193a2e9c15f17aa45d6a6b6f24651f9dc55b145f68471f614337a4b`, `.ufo/evidence/round-35/c1/c1-measure.py` hashes `53c4a4e7b51d289da637ec9fde4211da1e3d432fe4d9fd71ae4b620c78d6df72`, and `contract.json` is modified. None of those are my writes. The **committed** bytes at the pin are unchanged (`git show HEAD:tools/tally-audit-v3.py | sha256sum` → `ef98fc53…`; runner → `a7d3f2dd…`), and my clone is byte-identical to the freeze (clean worktree, counter `515b0b1b…`, contract `a9eb2b97…` as committed).

Consequence: every number in this report was produced against the pinned clone, not the worktree. A C1 measurement taken from the worktree would not be at the frozen tool bytes — `tool_sha_ok` would be 0.

---

## Mutation scoreboard (v3 / v2 / counter)

All `M*` copies: `tally_block_pristine=True` (verified with the runner's own awk extraction), sha256 in `work/copies/`. `R3` renames the loop operand inside the block (behaviour identical: counter `div=-`); `R4` keeps the block pristine.

| mutant | edit (harness region) | `check_harness` | v3 rc | v2 rc | counter |
|---|---|---|---|---|---|
| M01 | `for ti in 0…8` → `0…7 7` | REJECTED 32/34 | 1 harness | 1 harness | ACCEPT → **false kill (F1)** |
| M02 | → `6 1 2 3 4 5 6 7 8` | REJECTED 33/34 | 1 | 1 | ACCEPT → false kill |
| M03 | drop status-2 positional vector | **ACCEPTED** 34/34 | **0** | 0 | ACCEPT |
| M04 | drop status-3 vector | REJECTED 33/34 | 1 | 1 | ACCEPT → false kill |
| M06 | drop two-fail vector | REJECTED 33/34 | 1 | 1 | ACCEPT → false kill |
| M07 | drop two-setup vector | REJECTED 33/34 | 1 | 1 | ACCEPT → false kill |
| M08 | drop all-pass case | REJECTED 33/34 | 1 | 1 | ACCEPT → false kill |
| M09 | drop guard stress | REJECTED 31/34 | 1 | 1 | ACCEPT → false kill |
| M10 | compare exit only | REJECTED 28/34 | 1 | 1 | ACCEPT → false kill |
| M11 | compare line only | REJECTED 32/34 | 1 | 1 | ACCEPT → false kill |
| M12 | first-line prefix match | **ACCEPTED** 34/34 | **0** | 0 | ACCEPT |
| M13 | drop `2>&1` | **ACCEPTED** 34/34 | **0** | 0 | ACCEPT |
| M14 | pin `auto=1 KEEP=0` | **ACCEPTED** 34/34 | **0** | 0 | ACCEPT |
| M15 | pin `auto=1 KEEP=1` | **ACCEPTED** 34/34 | 0 | 0 | ACCEPT |
| M16 | `tnames` literal instead of head awk | **ACCEPTED** 34/34 | **0** | 0 | ACCEPT |
| M17 | drop `-n "$tblock" && 9 names` guard | **ACCEPTED** 34/34 | 0 | 0 | ACCEPT |
| M18 | drop the extract case | **ACCEPTED** 34/34 | 0 | 0 | ACCEPT |
| M19 | drop `help exits 0` case | **ACCEPTED** 34/34 | **0** | 0 | ACCEPT |
| M20 | drop `--regression refuses --target` case | **ACCEPTED** 34/34 | 0 | 0 | ACCEPT |
| M21 | drop `set -u` from the tally driver | **ACCEPTED** 34/34 | 0 | 0 | ACCEPT |
| M22 | drop leg-count agreement case (outside section) | **ACCEPTED** 34/34 | 0 | 0 | ACCEPT |
| M23 | tautological byte-equality stub | **ACCEPTED** 34/34 | **0** | 0 | ACCEPT |
| R1 | `regression_case_git` returns 0 | ACCEPTED (section intact) | 0 | 0 | ACCEPT |
| R3 | rename `st_kagi`→`st_surface` ×3 (outside harness, tally block renamed) | REFUSED: names ≠ panel | **1 harness** | 1 harness | ACCEPT → **false kill (F1)** |
| R4 | live harness = M23 tautology + strict decoy function before `selftest()` | **ACCEPTED** 34/34 | **0** | 0 | ACCEPT |
| R2 | canary assertions deleted (outside section) | ACCEPTED | 0 | 0 | ACCEPT |

`M05` (drop mixed vector) is **inconclusive**: my edit broke shell syntax (`harness rejects or cannot run the reference block (None)`); the class is already witnessed by `M06`/`M07`/`M09`. Not counted.

---

## Commands and exits

| # | command | exit | established |
|---|---|---|---|
| 1 | `git clone -q --no-hardlinks … /fast/…/AttackTailHarness/lane && git -C … checkout -q --detach 7da6e076…` | 0 (after removing an attempt-1 tree at `d16f9b5a` whose v3 sha was `da23d3a2…`, not the freeze) | pin + frozen hashes |
| 2 | `python3 lane/tools/tally-audit-v3.py --runner lane/tools/mutate-and-run.sh` | 0 | pristine `TALLY_AUDIT: PASS`, `CHECK harness PASS reference cases=9; faults rejected=34/34` |
| 3 | `python3 work/probe.py` | 0 | 23-mutant `check_harness` matrix, each with `tally_block_pristine=True` |
| 4 | `python3 work/hmatrix.py` | 0 | injected-fault matrix (F3 table) |
| 5 | `python3 work/verify.py <mutants>` | 0 | full v3 + v2 audits + counter divergence per copy |
| 6 | `python3 work/score_demo.py` | 0 | F1: `COPY accept harness-skip-position8 … rc=1 checks=harness pass=False` |
| 7 | `bash st/{pristine,PF,M03F,M23}.sh --selftest` | 0 / **1** / 0 / 0 | F3 and F2 end-to-end (`106/106`, `105/106`, `105/105`, `99/99`) |
| 7b | `bash copies/R3-rename-leg-consistent.sh --selftest` | 0 | rename is behaviourally inert at the runner level (`106/106 pass`) |
| 7c | `python3 work/score_rename.py` | 0 | F1 cleanest: `COPY accept rename-leg-consistent div=- rc=1 checks=harness pass=False` |
| 7d | `python3 lane/tools/tally-audit-v3.py --runner work/copies/R4-relocated-decoy-harness.sh` | 0 | F2(b): `CHECK harness PASS … 34/34`, full PASS |
| 7e | `python3 lane/tools/tally-audit-v2.py --runner work/copies/R4-relocated-decoy-harness.sh` | 0 | v2 identical (`vectors=15158` vs v3's 30316 — v2 sweeps two configs) |
| 7f | `bash work/copies/R4-relocated-decoy-harness.sh --selftest` | 0 | live harness green at `99/99` while the audited text is dead |
| 8 | `sha256sum lane/tools/{tally-audit-v3,tally-audit-v2}.py lane/tools/mutate-and-run.sh` | 0 | `ef98fc53…`, `7b11ba25…`, `a7d3f2dd…` — unchanged |
| 9 | `git -C lane status --porcelain` | 0 | 0 lines; `HEAD = 7da6e076…`; `pristine.sh` sha == runner sha |

Restoration: the lane checkout was never written to (all mutations live in `work/copies/` and `st/`); the three frozen sha256s are identical before and after, the worktree is clean, and `work/copies/pristine.sh` hashes to the runner's own `a7d3f2dd…`.

---

## One-line consequences for the L1

- Before the single C1 run: the sealed accept set must contain **no** harness-region edit and **no** leg rename (F1), or C1 reads false through no fault of the tool (a 3-token consistent rename is already enough); the sealed kill set must likewise stay inside the tally block (`c1-measure.py:307`).
- `CHECK harness PASS` means "the first `local tblock` text in this file rejects the 34 panel faults", not "this runner's tally selftest tests behaviour" (F2). A tautology passes it, and a dead decoy function is audited instead of the live harness.
- The audit's soundness about the tally is independent of the harness check and survived every weakening I built (F3, F6.1).
