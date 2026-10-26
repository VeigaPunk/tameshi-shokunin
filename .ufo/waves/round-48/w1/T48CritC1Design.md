# T48CritC1Design — pre-freeze attack on the C1 predicate

Seat: critic, round 48 wave 1. Scope: `.ufo/evidence/round-48/contract.json` claim C1 (`statement`, `amendments[2]`, `predicate_label`, `kill_rule`, controls) and the counter it is about to freeze
`.ufo/waves/round-48/w1/T48ExecC1Counter.measure.py` (48 530 B, delivered by T48ExecC1Counter; read only, never edited), plus `.ufo/waves/round-48/brief-c1-counter.md`.
Read-only on the lane; no scratch tree is left on disk. Nothing installed or upgraded (no uv/pip/pacman/npx/binary channel used; the probes were `git clone --shared`, `bash`, `python3` and `grep` on the existing host tools).

Verdict: **the predicate has one exploitable hole (unbound "observation receipt" attestation), one soundness-and-fairness defect (dependence observation is read against a flaky control profile), and one validity gap (two statements are not determined by REV). Four candidate attacks are blocked. CTL_A, CTL_B, CTL_C, CTL_D and CTL_E all behave as claimed.** All findings are pre-data and fixable by amendment before the counter freeze; none is a tradeoff, each has a one-sentence correction.

## 1. F1 — CRITICAL, false provenance: an "observation receipt" is unbound text, so any lane can attest any value

Contract (`contract.json:26`): a V member is attested if it is "observed in this run's P0 tuples **or recorded as a P0 tuple of that statement in a committed observation receipt under `.ufo/evidence/round-48/calibration/observations/` at REV**".
Brief clause (6) sharpens it to "recorded as that statement's P0 tuple in any committed `PROFILES <id>: P0=<line>|<exit> ...` line of a file under [that directory] at REV (the round-47 `--emit` stdout format; read via `git show` at REV)".

That is a *format*, not a derivation. The delivered counter implements exactly that, with no binding to the counter's own sha, to a run, to a revision of the run, or to the pinned tool:

- `.ufo/waves/round-48/w1/T48ExecC1Counter.measure.py:79` `OBSERVATIONS_DIR = '.ufo/evidence/round-48/calibration/observations'`
- `:241-260` `load_attestations()` — `git ls-tree -r` over that directory at REV, then for **every** file, `re.match(r'^PROFILES (.+?): (.*)$', line)`, and add the `P0=` token to `att[<id>]`. No header, no counter sha, no rev of the emitting run, no tool sha, no relation to a `--emit` invocation.
- `:504-509` a member passes if `m in observed or attest_token(...) in receipts`.
- Its own selftest blesses the path: `:734-739` `T51_three_members_one_observed_two_attested` — one round observed, two members supplied by two hand-written observation files — expects `('unattested=0', 'total=0')`.

The directory does not exist at the base revision (`git cat-file -e 473336d:.ufo/evidence/round-48/calibration/observations` → fatal: does not exist), so the lane creates it; every attestation in round 48 is lane-authored text.

### Counterexamples (each costs one `printf`)

**A. Revision-bound value declared `nondeterministic` (dodges the C2 coupling).** `sources-census-v2.sh` is resolved relative to cwd and the statement's cwd is `clone`, so at REV the census prints one count. Measured at the base tree in a scratch clone at `473336d`: `rows=124`, `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`, exit 0. C2 opens four rows, so at the content revision the same statement prints `rows=128`. A lane appends

`PROFILES sources-registry: P0=rows=124 SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)|0`

to `observations/pre-c2.md` and declares the row as two members (`rows=124 …`, `rows=128 …`, class `nondeterministic`). `mismatches=0`, `unattested=0`, `oversize=0` → `total=0`. The value is not nondeterministic at any revision; the row states a false class, and the receipt was never produced by the statement at REV.

**B. The routed one-shot flake becomes a legal standing member.** Six-leg regression ledger prints `REGRESSION: PASS (cases=9 passed=9|0` in **6 of 6** committed observations (see §3), and the round-47 deciding receipt records that value (`.ufo/evidence/round-47/after/c1.stdout`: `STATEMENT cap/six-leg regression ledger: claimed=REGRESSION: FAIL (cases=9 passed=7|1|a7d3f2dd7d47 observed=REGRESSION: PASS (cases=9 passed=9|0|a7d3f2dd7d47 … MISMATCH`). Round-47's closure routed that row as defect 1. Under the round-48 predicate a lane re-appends it as `… or REGRESSION: FAIL (cases=9 passed=7, exit 1 …, runs 3 nondeterministic` with a one-line receipt `PROFILES six-leg regression ledger: P0=REGRESSION: FAIL (cases=9 passed=7|1`. `attested` is satisfied, `PASS passed=9` is in V, class matches count → **the round-47 defect is now reachable by construction, and the predicate calls it honest.**

**C. Receipt from a mutated tree.** `--emit` run against a scratch clone whose pinned tool (or a fixture it reads) is mutated emits `PROFILES` lines; copied into the observations directory of the lane they attest a tuple the REV tree never prints. Nothing distinguishes those bytes from a real receipt.

**D. Any junk member, any statement.** Because the receipt is free text, `CTL_C`'s "three invented members" cheat is refused only in the variant *without* receipts. With receipts it passes: invent two members per statement, add two `PROFILES` lines per statement, and the whole card can be declared `nondeterministic` with `total=0` and zero re-observation.

### Smallest safe correction (amendment, pre-data)

Replace the parenthetical in `contract.json:26` with a re-derivation rule — the only evidence that cannot be typed is evidence the counter produced:

> every member of V is attested: observed as a P0 (line, exit) tuple in this run's three rounds, or, for a declared member not so observed, **re-observed by the counter itself in up to 6 extra P0 rounds of that statement at REV** (extras counted and printed as `attested_extra=<n>` in the label, each extra round's tuple printed as a `PROFILES` line). No file under `.ufo/evidence/round-48/calibration/observations/` is evidence for attestation; a declared member that no round (three or extra) prints is `unattested`.

Cost: extra P0 runs only for declared-but-unobserved members (bounded, per statement). The three decision rounds stay exactly three, so `rounds=3` is untouched. `CTL_C` still fails (invented members are never produced), `CTL_E` still passes (`--emit` emits only observed members), and counterexample A dies (the counter cannot re-observe `rows=124` at REV), as does B (it cannot re-observe `passed=7`), C and D.

Cheaper fallback if the L1 will not pay for extra runs: **attested = observed in this run's three rounds only; delete the receipt clause**. Then V ⊆ observed by construction, `nondeterministic` is reachable only from two distinct observed P0 tuples (so the class always states a real observed instability), and `unattested` survives as the check on a row that over-declares. Its cost is sampling risk: an authoring run that misses a rare P0 flake can mismatch at the deciding run (the contract already accepts exactly this risk in the kill rule).

## 2. F2 — HIGH, soundness and fairness: `deps` is read against a control profile that is itself flaky

Contract (`contract.json:26`, last sentence): "Per round, dependence d is observed when the variant profile's tuple **differs from that round's P1 tuple** (env: P0 differs from P1)"; required = observed in all 3 rounds, never = observed in none, unstable may be declared or omitted. The delivered counter implements it verbatim (`T48ExecC1Counter.measure.py:471-480`: `ref = dep_key(P1)`, `required = ∩`, `never = DEP_NAMES - ∪`).

P1 is not stable. Measured from every committed `PROFILES` line in `.ufo/evidence/round-47/**` and `.ufo/waves/round-47/**` (20 files, 6 complete observations), `hermetic env-differential probe`:

| profile | value | receipts |
|---|---|---|
| P0 | `ENVDIFF_SELFTEST: 9/9 pass\|0` | 6/6 |
| P1 (clean env) | `9/9 pass\|0` | 3/6 |
| P1 (clean env) | `2/9 pass\|1` | 3/6 |
| P2 (no bwrap) | `2/9 pass\|1` | 6/6 |
| P3 (no jj) | `2/9 pass\|1` / `9/9 pass\|0` | 3 / 3 (follows P1) |
| P4 (no node) | `1/9 pass\|1` / `8/9 pass\|1` | 3 / 3 |
| P5 (decoy fleet root) | `2/9 pass\|1` / `9/9 pass\|0` | 3 / 3 (follows P1) |

So `bwrap` is "observed" exactly in the rounds where P1 happened to print `9/9` (then P2's `2/9` differs), and "not observed" where P1 printed `2/9` (P2 equals it). Consequences over 3 rounds:

- P1 = `9/9` in all three → `bwrap` required; a row declaring only `node` is `dep_mismatch`.
- P1 = `2/9` in all three → `bwrap` observed in **none** → declaring `bwrap,node` (the round-47 row, and what `--emit` produces when authored under the 9/9 regime) is `dep_mismatch`.
- There is **no deps line that is safe in both regimes.** An honest lane therefore has a substantial chance of an honest miss decided entirely by host load, and the same lane can flip the outcome by taking its three rounds at a different moment (the kill rule forbids the rerun; nothing detects it).

This is the concrete form of "declaring unstable deps to dodge dep_mismatch": the *contract's own rule* makes a real dependence omit-or-declare-lottery, and the round-47 counter (single run, exact equality) had forced `bwrap,node` to be declared.

### Smallest safe correction

Replace "differs from that round's P1 tuple" with "is not a member of V":

> Per round, dependence d is observed when that round's variant-profile tuple is **not a member of V** (env: when that round's P1 tuple is not a member of V). A dependence observed in all three rounds is required and must be declared; one not observed outside V in any round must not be declared; a dependence observed in some rounds only is `unstable` and may be declared or omitted.

Check against the measured data, with V = `{ENVDIFF_SELFTEST: 9/9 pass|0}` (P0 6/6): P2's `2/9` is never in V → `bwrap` required in every round; P4's `1/9`/`8/9` never in V → `node` required; P3/P5 alternate into `2/9`, which is outside V → `jj`, `fleet-root` unstable (may be declared or omitted); P1 alternates → `env` unstable. Required = `{bwrap,node}` **deterministically**, which is exactly the round-47 row. The 12.5 %-each-way lottery disappears, for every statement, without weakening `CTL_D` (a fully stable statement's variants are always in V, so declaring all five still yields `dep_mismatch>0`) and without weakening `CTL_B` (§3). Disclosed limit to record: a dependence that moves a value *inside* V is still undetectable — the same limit the contract has today, but now with a stable test.

## 3. F3 — HIGH validity, "at REV" is not achievable for two of the 22 statements

The statement is quantified "over R=3 observation rounds … **at REV**". Two pinned commands read the live fleet, so their printed tuples are not functions of REV:

- `retained invocation-context gate` (`.ufo/evidence/round-15/verify.py`) — `:105` `CENSUS_TOOL = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`, `:835-836` `[CENSUS_TOOL, "validate", "--root", "/home/vgpnk/Projects/shokunin", "tameshi"]`. Both the fleet-level script and the lane's registry are read at their **live** content, not at REV. Its `fleet-root` dependence (`P5` prints `SELFTEST: PASS (49/49)|1` in 5/5 receipts) is itself evidence the command reaches the fleet root.
- `six-leg regression ledger` — `tools/mutate-and-run.sh:178` `SELF=$(readlink -f …)`, `:1358` `FLEET_ROOT=$(dirname ×3 "$SELF")`, `:1340` `repo="$FLEET_ROOT/${rel%%/*}"`, legs at `:87-95` name nine sibling lanes (`kumitate-`, `kagi-`, `tsukuroi-`, `mado-`). The counter puts the lane's *mirror clone* under `<work>/P0/fleet/` but every sibling lane is a **symlink to its live checkout** (`T48ExecC1Counter.measure.py:329-331`, inherited from the round-47 counter), so nine live repos are read on every round.

Consequence: a sibling-lane commit, a dirty tameshi worktree (the round-15 command reads `--root /home/vgpnk/Projects/shokunin tameshi`), or a fleet-repo edit between rounds or between rounds and the deciding run flips a value **for reasons outside the lane**, and the kill rule turns that into a mismatch. The lane cannot prevent it. Today no drift is visible (`retained invocation-context gate`: `P0..P4` identical in 5/5 receipts; six-leg `P0` `PASS passed=9|0` in 6/6), so this is a latent validity gap, not a demonstrated flake — but it is exactly the class the round-47 disclosure recorded for six-leg (`P3` = `FAIL (cases=9 passed=8|1` in 1 of 6).

### Smallest safe correction

> The counter records the live state it reads — the HEAD short sha and dirty flag of every sibling `*-shokunin` lane, and the sha256 of `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` — requires it identical across the three rounds, prints it as `fleet=<list>` in the label, and a deciding run requires the lane worktree clean at REV (`git -C LANE status --porcelain` empty and `HEAD == REV`). A change is reported as `fleet_drift` and voids the observation; it is never counted as a mismatch.

## 4. F4 — MEDIUM, the contract does not define "a table of its kind" or exclude hidden regions

`contract.json:26` says "the last data row of a SCORECARD.md table **of its kind**" and `amendments[2]` fixes only the row grammar. The round-47 and round-48 counters both silently use: kind `cap` ⇔ header cell 1 == `Capability`; kind `axis` ⇔ header cell 2 starts with `Score`; tables inside fenced code blocks or HTML comments ignored (`strip_hidden`); a table line starts with `|` at column 1; cells split on `|` after stripping the outer pipes; the first cell must equal the id exactly (`T48ExecC1Counter.measure.py:149-182`, round-47 selftest T08-T11). The label (`unparsed`, `mismatch`) depends on all of it, and the contract does not.

Attack available to a lane against a counter that drops `strip_hidden`: append a fenced code block at the end of `SCORECARD.md` — a natural thing to do when documenting the row format — containing `| Capability | … | … runs 3 stable |` for a statement id; that row is last in file order and wins. The delivered counter blocks it; the *frozen contract* does not require the block. (Verified not exploitable in the delivered code: `strip_hidden` at `:143-148` and T10/T11 in the inherited selftest.)

### Smallest safe correction (append to amendment 3)

> A table of its kind is a Markdown table whose header cell 1 is `Capability` (kind `cap`) or whose header cell 2 begins `Score` (kind `axis`); tables inside fenced code blocks or HTML comments are ignored; a table line is a line beginning `|` at column 1; cells are split on `|` after stripping the outer pipes and surrounding whitespace, and the first cell must equal the statement id exactly; the standing row is the last matching row in file order across all tables of that kind.

## 5. F5 — MEDIUM, `append_only` is measured against a caller-supplied `--base`

`T48ExecC1Counter.measure.py:428` `append_only = int(rev_sc.startswith(base_sc))`, where `base_sc` comes from the free `--base` flag. The contract fixes `--base 473336d…` in the invocation line, but the counter does not. `append_only` is the only thing preventing the round-47 standing rows' text from being rewritten rather than appended to (this lane is a jj working copy; history rewriting is a normal jj operation). With a self-chosen base, the premise is void.

### Smallest safe correction

> The counter hard-codes `BASE = 473336d9d789f6081195e7376d17836a24666bc3`, exits 2 on any `--base` that differs from it, and prints `base=<sha>` in its label.

## 6. F6 — LOW/MEDIUM (procedure, must be named before the freeze): nothing limits the deciding run to one invocation

`contract.json:29` says "a flaky deciding observation outside V is a mismatch, **not a rerun**", but no mechanism detects a second invocation. A lane can run the counter repeatedly in wave 2 and commit the favourable stdout as the deciding receipt. Round-47's answer was `.ufo/evidence/round-47/deciding-run.sh` with `FROZEN_UNCHANGED=1`; round-48's contract does not name an equivalent.

> Before freeze step 2: name `.ufo/evidence/round-48/deciding-run.sh` (one invocation per claim, receipts-only commit, `FROZEN_UNCHANGED=1` recomputed over the counter, `statements.json`, the contract and the snapshots). A second invocation of either counter at the content revision is a miss.

## 7. F7 — CTL_B checked: it fails, and it fails for the claimed work (with one caveat)

Required check: "does CTL_B really fail for a reason tied to the claimed work?"

- The six-leg row states `REGRESSION: FAIL (cases=9 passed=7`, exit 1, deps `env,fleet-root,node`.
- The tree prints `REGRESSION: PASS (cases=9 passed=9`, exit 0: this is the P0 tuple in **6 of 6** committed observations (`.ufo/evidence/round-47/control/emit-observed-pre-freeze.out`, `control/controls-at-freeze.stdout`, `.ufo/waves/round-47/w1/T47ExecObs*.md`, `.ufo/evidence/round-47/after/c1.stdout`) and in the round-47 deciding run. `FAIL (cases=9 passed=7` appears in **no** committed receipt; its only trace is the round-47 errata's account of the discarded content-revision `--emit`.
- Therefore CTL_B yields `mismatches=1` on six-leg. It also yields `dep_mismatch=1` on the same row: `env` was only ever produced by the flaky P0 (`FAIL passed=7` vs P1 `PASS passed=9`); with P0 = P1 = `PASS passed=9`, `env` ∈ `never`, so the round-47 row's declared `env` is a forbidden declaration. `fleet-root` (P5 `SETUP passed=0|2`) and `node` (P4 `SETUP passed=4|2`) are required in every round and are declared correctly.
- The other 21 rows are not collateral: the round-47 deciding receipt records "the other 21 rows matched", and `473336d` adds only `corpus/lessons/round-47-verifier-spotcheck.md` (`git show --stat`), so tools and corpus are the round-47 content revision. Under F2's correction the one row with a shaky deps line, `hermetic env-differential probe`, becomes deterministic `{bwrap,node}` and passes either way.

Both CTL_B failure modes therefore trace to the routed defect (the one-shot flake restated as a standing value). Caveat: **score CTL_B at a pre-C2 revision.** At the base tree the census prints `rows=124` (measured, exit 0), so CTL_B's `sources-registry` row matches. Scored after C2's four rows land, that row would also mismatch (`rows=128`), still false but no longer diagnostic. The contract does not say which revision the controls are scored at; `freeze_plan` implies the freeze-2 commit.

> Amendment: `control/controls-at-freeze.stdout` records the revision it was taken at; CTL_B is scored there (before C2's four rows), and every control's revision is printed in its receipt.

## 8. F8 — candidates that are blocked (checked, no amendment needed)

| Candidate | Blocked by | Evidence |
|---|---|---|
| census count "checked at another revision" | cwd is `clone`; `sources-census-v2.sh` reads `corpus/SOURCES.md` relatively; the counter clones and checks out REV per profile (`setup_profile`) | measured `rows=124`, exit 0 in a base clone; `cwd: clone` in statements.json |
| rows in fenced blocks / HTML comments / other tables | delivered parser (`strip_hidden`, kind filter, exact first-cell match) — **but see F4 for the contract-level gap** | `T48ExecC1Counter.measure.py:149-182`; round-47 selftest T10/T11 |
| observation receipts committed after scoring | receipts are read with `git show REV:path`, so a commit after REV cannot enter REV's tree | `load_attestations`, `:246-252` |
| a do-nothing lane reaches `total=0` | the base SCORECARD has **0** standing rows carrying the literal `runs 3` (0 occurrences of `runs 3` in the whole file; all 22 statement rows present but none selectable) → `unparsed=22`, `total=22` | measured on the base `SCORECARD.md` with the round-47 picker |
| a 3-member set "swallowing flakiness" | legal **by design** once each member is observed — with F1's correction a 3-member set requires three distinct observed P0 tuples, i.e. a true observed instability; the only swallow that survives today is a *revision-bound* value, which F1's re-derivation kills | §1 counterexample A |
| wrong row (`stable` with 2 members, `nondeterministic` with 1, 4 members) | `oversize` in the delivered grammar (`:226-229`) and in amendment 3 | `parse_row` |
| statements list edited / counter edited | `stmts_pin` against `924102df…`, `self_pin` against the blob at REV | `:397-410` region, round-47 T14/T15 |

## 9. F9 — LOW, out-of-predicate but axis-relevant: the calibration row restates a monitor the lane writes into

The `calibration` axis row's value is `calibration_restraint_score` from `.ufo/evidence/round-21/coldread/measure.py`, computed from the lane's own corpus (`two points per restrained, evidence-linked [~] SHONEN box; box 3 is not credited` — round-47 row). C1 only requires the row to restate whatever the monitor prints, so a lane that edits its cold-read sections upward can pass C1 *and* raise the axis in one move, with no calibration work. The guard today is the no-harm monitor (`coldread 6`), which is the L1's, not C1's.

> Optional amendment: the `calibration` axis row declares `6` and the deciding run's cold-read monitor prints `6`; a raise is a separate claim with its own evidence.

## 10. What the predicate does certify (stated so the L1 reads the result correctly)

After F1, the residual "cheap pass" is: run the counter with `--emit` at REV, paste the rows, commit. That is the intended procedure — the claim is "the standing self-assessment is restated from R=3 repeated observation rounds", and the counter's own three rounds *are* the observation. What the predicate then certifies is the restatement procedure (no stale one-shot value, no undeclared dependence, no unobserved member), not that the lane learned anything about its tools. The three residual risks, in order: F2's lottery (fixed by the V comparison), sampling risk on a rare P0 flake (accepted by the kill rule; mitigated by F1's extra rounds), and the fact that `nondeterministic` does not distinguish host-load variance from harness interference (the counter runs 22 statements × 6 profiles concurrently per round, default `--jobs 6`; if the L1 wants the class to mean "the tool is flaky", the cheapest guard is `--jobs 1` for any statement the three rounds declare `nondeterministic`, recorded as `isolation=serial`).

## 11. Ranked minimal pre-data amendments (for the L1, before the counter freeze)

1. **A1 (F1, critical)** — attestation by counter re-derivation (up to 6 extra P0 rounds, `attested_extra=<n>`); no file under `observations/` is evidence. Fixes A/B/C/D; keeps `CTL_C`, `CTL_E`.
2. **A2 (F2, high)** — dep observed iff the variant tuple ∉ V (env: P1 ∉ V); required / never / unstable unchanged. Removes the 12.5 %-each-way honest miss; keeps `CTL_B`, `CTL_D`.
3. **A3 (F3, high)** — record and require a stable live fleet state (`fleet=<list>`, sibling HEADs + dirty flags + census-tool sha256, identical across rounds) and require the lane worktree clean at REV in the deciding run; drift voids the observation, never counts as a mismatch.
4. **A4 (F4, medium)** — paste the round-47 table taxonomy and hidden-region stripping into amendment 3.
5. **A5 (F5, medium)** — hard-code `BASE`, exit 2 on a differing `--base`, print `base=`.
6. **A6 (F2/§7, medium)** — record the control scoring revision (freeze-2 commit) in `controls-at-freeze.stdout`.
7. **A7 (F6, low/medium)** — name `deciding-run.sh`: one invocation per claim, `FROZEN_UNCHANGED=1`.
8. **A8 (F9, low)** — the calibration row declares 6 and the deciding cold-read monitor prints 6.

Axes impacted: **calibration** (A1-A8; A1/A2 change what "honest restatement" means and are the difference between a certified claim and a typed one), **depth** (none — no value, target or count changes), **freshness** (none — A1's counterexample A is the only C2 coupling and the amendment removes it), **operability/coverage** (none).

## 12. Method and receipts

- Read: `contract.json` (whole, incl. `amendments` 1-3), `brief-c1-counter.md` (whole), `.../round-47/calibration/measure.py` (whole, incl. selftest), `.../round-47/calibration/statements.json`, `SCORECARD.md` (round-47 stand section and errata), `.ufo/waves/round-48/w1/T48ExecC1Counter.measure.py` (read-only; attestation, dep, row-parse and label paths), `.ufo/evidence/round-15/verify.py:102-108,832-840`, `tools/mutate-and-run.sh:178,1320-1360` and the leg table `:87-95`, fleet `scripts/sources-census.sh` header/usage.
- Measured (scratch clone `git clone -q --shared` of the lane at `473336d` under `$S=/fast/scratch/hyaku/tameshi-r48/T48CritC1Design`, `TMPDIR=$S`, removed before this report was written):
  - base `SCORECARD.md`: 22 statement rows picked, **0** carrying `runs 3`, 0 occurrences of the literal `runs 3` → CTL_A `unparsed=22`.
  - base census in the clone: `rows=124`, `SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`, exit 0.
  - per-profile value counts for `six-leg regression ledger` and `hermetic env-differential probe` over all 20 committed files carrying `PROFILES` lines (§2, §3 tables).
  - round-47 deciding receipt `.ufo/evidence/round-47/after/c1.stdout`: `C1_R47: … mismatches=1 … dep_mismatch=1 … total=2 … C1_R47_PASS=false`, the six-leg row the only mismatch.
- One 500 s probe of `bash tools/mutate-and-run.sh --regression` in a faithful `fleet/` layout was cancelled before it finished (the statement's own timeout is 2700 s and nine mutation legs run under a host carrying ~100 agents); its result is not used — the six-leg value is taken from the six committed `PROFILES` receipts and the round-47 deciding stdout instead. Note for the deciding-run budget: six-leg alone may cost up to 45 min per P0-P3 round.
- No tool installed or upgraded. No writes outside this file. Scratch directory deleted.
