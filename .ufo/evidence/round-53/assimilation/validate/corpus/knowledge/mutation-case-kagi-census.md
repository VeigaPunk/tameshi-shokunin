# Mutation case — kagi `surface-census.sh` (TAMESHI-R3-1)

Run date 2026-10-14. Lane: tameshi (round 3; plan `tameshi-shokunin/plans/round-3.plan.md`,
axes: depth + operability). Substrate: kagi-shokunin **read-only** — every mutant is a copy under
`/tmp/tameshi-r3-1-work/`, and the kagi tree was not written (restore proof §0); this note is the
only fleet file written by this run. No external site was contacted; no secret file was
content-read (kagi's 0600 `stamps.tsv` appears in directory listings by name only).

Anchors: **O** = observation (file:line or command output), **I** = inference, **U** = unknown.
A bare `surface-census.sh:NNN` is `kagi-shokunin/corpus/surface-census.sh` at the revision pinned
below; `LOG.md:NNN` is `kagi-shokunin/LOG.md`.

Artifact under test (O: `sha256sum`, `stat`, `git`): sha256
`275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f`, 44212 B, 886 newlines (the
887th line carries no trailing newline — `tail -c1` prints `c`), mtime 2026-10-14 09:47:15 -0300,
mode 755; kagi `HEAD fecee8743e52eb8fb5fbb40782934cb619a1a96e`,
`git status --porcelain -- corpus/surface-census.sh` empty.

## 0. Gate choice, method, headline

**Why `surface-census.sh`, not `checklist-run.sh` (the assignment's fallback).** The question was
whether the census selftest is entangled with live substrate; measured: on this host it is not.

- O: the selftest builds every fixture under `mktemp -d` and re-invokes the gate as
  `bash "${BASH_SOURCE[0]}" verify --root "$R/host" --census/--shapes/--baseline "$R/…"`
  (`surface-census.sh:694-764`) — the verify/shape path reads no live path.
- O: the two trailing verb cases are substrate-gated: `command -v "$JANITOR"` (`:817`) records
  `skip-case … substrate-absent (handler not on PATH)` (`:820-823`) and does not execute the verbs
  block. Measured host facts: `the-janitor` is **MISSING** from PATH; `tmux has-session -t janitor`
  rc=1. Control output confirms `skip-case 15` / `skip-case 16`.
- O: kagi's own log records the round-18 repair of exactly this edge: `--selftest` "failed 2/16 on
  any handler-absent host … now `skip-case …` (count still 16)" (`LOG.md:741-744`).
- O: the case counter counts skips as cases — control shows `ok-case 01..14` + `skip-case 15`/`16`,
  epilogue `SELFTEST: PASS (16 cases)` (`:846-847`); the hermetic case set here is 14, plus 2
  substrate-gated cases that performed no execution.
- (I) On a handler-present host the two cases would exec the real binary (scratch overrides only —
  header `:45-46`); a verbs-logic mutant's verdict would then be host-dependent. All mutants below
  edit verify/shapes logic, so this does not touch the measured table; kept as U2.

**Method** (round-2 replica):

- O: control run, unmutated byte copy — `bash control.sh --selftest` →
  `SELFTEST: PASS (16 cases)`, exit 0, 1.0 s wall.
- O: each defect = ONE exact-string replacement applied to a fresh copy of `pristine.sh` (a
  `cp -p` byte copy, `cmp`-verified); the driver asserts the old string occurs exactly once before
  writing (`mutate_driver.py --check` → `all unique`, all 10). No defect compounds with another;
  the kagi original was never written, and no live host surface was read by any run.
- O: per-defect evidence: full combined output → `evidence/<id>.selftest.txt`; exit code + mutant
  sha256 + wall time + case summary → `evidence/<id>.meta.json`; aggregate → `evidence/results.json`.
- O: **kill rate 8/10 (80 %)**; survivors B5, B10. No inconclusive run — each of the 11 runs
  produced a definitive suite verdict; the suite count held (`(<n>/16 cases)` on every run; green
  runs printed exactly `SELFTEST: PASS (16 cases)`); the whole sweep took 11.0 s wall for 11 runs
  (~1.0 s each) against the 280 s per-run bound.
- O: restore proof — kagi sha256 before `275d8294…53009f` and after `275d8294…53009f`; 44212 B and
  mtime 09:47:15 unchanged; `git status --porcelain` for the path empty; `/tmp/…/pristine.sh` still
  `cmp`-identical to the kagi original after the sweep.
- Context: this is tameshi's second measured kill-rate; the first is round 2's
  `mutation-case-kimi-census.md` (compared in §4). Per `SKILL.md`'s bands the case sits on the
  50-80/>80 boundary, so that boundary reading is the worked one, and the survivors table below is
  attached as the band requires.

## 1. Kill-rate table

| # | Defect class | Injected defect (ref = edit site) | Exit | Suite line | Verdict | Failing cases |
|---|---|---|---|---|---|---|
| — | control | unmutated copy | 0 | `16 cases` / PASS | green | 0 |
| B1 | wrong `-eq` (guard inversion) | scan guard `-eq 0` → `-ne 0` (`surface-census.sh:241`) | 1 | `1/16` / FAIL | **killed** | 1 (undeclared-file) |
| B2 | numeric boundary off-by-one | rows floor `-ge` → `-gt` (`:435`) | 1 | `2/16` / FAIL | **killed** | 2 (clean, runtime-absent) |
| B3 | inverted test | CROSSCHECK `!=` → `==` (`:229`) | 1 | `3/16` / FAIL | **killed** | 3 (clean, runtime-absent, crosscheck-disagree) |
| B4 | dropped branch | symlink arm deleted (`:200-204`) | 1 | `1/16` / FAIL | **killed** | 1 (symlink-swap) |
| B5 | dropped branch | exec x-bit arm deleted (`:214-217`) | 0 | `16 cases` / PASS | **survived** | 0 |
| B6 | off-by-one (length) | magic `head -c len+1` → `len` (`:371`) | 1 | `2/16` / FAIL | **killed** | 2 (clean, runtime-absent) |
| B7 | off-by-one (count) | `N_UNVERIFIED + 1` → `+ 2` (`:405-406`) | 1 | `1/16` / FAIL | **killed** | 1 (sqlite-unavailable) |
| B8 | wrong exit mapping | `die` `exit 2` → `1` (`:85`) | 1 | `2/16` / FAIL | **killed** | 2 (malformed-row, fused-shape-row) |
| B9 | inverted class select | missing-branch `runtime` → `asset` (`:191`) | 1 | `2/16` / FAIL | **killed** | 2 (asset-gone, runtime-absent) |
| B10 | reported-but-unasserted count | CLEAN summary `ok=` arg `$N_OK` → `$N_ABSENT` (`:862`) | 0 | `16 cases` / PASS | **survived** | 0 |

By class: wrong `-eq` 1/1 · numeric boundary 1/1 · inverted test 1/1 · dropped branch 1/2 ·
off-by-one (length) 1/1 · off-by-one (count) 1/1 · wrong exit mapping 1/1 · inverted class select
1/1 · reported-but-unasserted count 0/1.

Failing-case labels (O: `evidence/<id>.selftest.txt`, exact bad-case lines):

- B1 (1): `bad-case 05 undeclared-file want exit=1 token=SURFACE UNLISTED got exit=0`. The guard
  inversion makes `verify_unlisted` return early whenever scan dirs **exist** (`:241-242`), so the
  UNLISTED arm goes quiet; the clean case still passes because its fixture has no stray child to
  miss — the single case that pins the arm is the one that fires.
- B4 (1): `bad-case 07 symlink-swap want exit=1 token=SURFACE LINK got exit=1` — the **exit code
  still matched** (the deleted arm's symlink falls into the regular-file arm and prints
  `SURFACE DIVERGED`); the token assert is what killed it. A suite asserting only exit would have
  passed this deletion.
- B7 (1): `bad-case 10 sqlite-unavailable exit=1` — the case demands the exact substring
  `unverified=3` (`:782`); +2 per event → `unverified=6`. This is the suite's only exact-count
  string over the UNVERIFIED class.
- B2 (2) / B6 (2): both die on the same two cases — 01 `clean` and 04 `runtime-absent` — the
  suite's two exit-0 green fixtures (case 04 is the full green fixture minus one runtime row,
  `:770`).
- B3 (3): 01 and 04 (the `==`-flipped predicate fires on *agreement* for every checked op.env row)
  plus 06 `crosscheck-disagree` (`token=SURFACE CROSSCHECK got exit=0` — it can no longer fire).
- B8 (2): 13 `malformed-row` and 14 `fused-shape-row` — the two exit-2 setup cases (`got exit=1`
  each).
- B9 (2): 03 `asset-gone` (missing asset reported ABSENT, exit 0) and 04 `runtime-absent` (missing
  runtime reported GONE, exit 1) — the two classes swap.

## 2. Surviving-defect class analysis

**B5 — deleted exec x-bit arm (`surface-census.sh:214-217`).** O: 16/16 PASS. O: no selftest case
exercises a row declared `exec` whose live file lost its x bit — the fixture creates that row at
`chmod 755` (`:707`) and no case strips it (the only chmods are `:521-588`, `:704-717`, `:768`);
the string `-x ` occurs exactly once in the file, inside the deleted arm itself (O:
`grep -n -- '-x ' surface-census.sh` → `214`). O (non-equivalence): on a probe row `asset exec -`
whose file is not executable, pristine prints
`SURFACE DIVERGED … (declared exec, no execute bit)` exit 1; B5 prints
`SURFACE OK       … (exec 644)` exit 0 (`evidence/probe-B5-non-equivalence.txt`). I: this is a
*fixture-absent arm* — the survivor class round 2 did not have: nothing reaches the arm, so no
implementation of it, right or wrong, moves the suite.

**B10 — CLEAN-summary count (`surface-census.sh:862`).** O: 16/16 PASS. O: no case asserts the
summary counts — `run_case` checks exit + one substring token only (`:747-760`), and the summary
line's fields are read by no case. O (non-equivalence): green one-row fixture → pristine
`SURFACE_CENSUS: CLEAN (assets=1 runtime=0 scanned=0 ok=1 absent=0 skipped=0)`; B10
`… ok=0 …`; both exit 0 (`evidence/probe-B10-non-equivalence.txt`). Same class as round-2's D10
(wrong reported constant): a mutant confined to displayed report data survives by construction.

**Shared class:** both survivors change what the suite's assert vocabulary never reads — one on
the fixture side (an arm no case reaches), one on the report side (a count no case reads).

## 3. What the 16-case suite protects — and does not

**Protected (each proven by the kill that died on it):**

- The scan guard and the UNLISTED arm: B1 dies on case 05 — blast radius 1: the guard is pinned
  only where a stray child exists.
- Floor boundary semantics on the sqlite row counts: B2 dies on both green fixtures (`-ge` vs
  `-gt` matters only at equality; the fixture's part table sits exactly at the floor).
- CROSSCHECK agreement: B3 dies on two green fixtures (fires on agreement) and on case 06 (cannot
  fire on disagreement) — one edit, both directions.
- The symlink arm: B4 dies on case 07, and the kill is carried by the *token* assert, not the exit
  code.
- The magic-length NUL probe: B6 dies on both green fixtures — the expected file is exactly
  `len+1` bytes, so a short head-cut mismatches on length (`cmp` sees the difference).
- The exact UNVERIFIED count: B7 dies on case 10's `unverified=3` substring — the only count
  string with a case behind it.
- The exit-2 setup map: B8 dies on cases 13/14.
- The missing-row class select: B9 dies on cases 03/04 — both classes pinned in both directions.

**Not protected (measured gaps):**

- The exec x-bit arm (B5): fixture-absent; real drift (an `exec`-declared row whose file loses +x
  while its mode still matches the declaration) would be reported `SURFACE OK`.
- The CLEAN/DRIFT summary counts (B10): `ok=`/`absent=`/`skipped=` and the assets/runtime tallies
  are reported, never read.

(I) Both gaps are the round-2 survivor family — behavior outside the assert vocabulary — with B5
adding the bash-side variant: an arm the fixtures never reach. Per tameshi's read-only discipline
this note reports the gaps; no fix is proposed to kagi from here.

**Scope (I):** single-text-edit defects on one artifact; the verbs path was not mutated (its two
cases skip on this host, U2); nothing here measures the live verify path against substrate drift
(hermetic by construction, U6).

## 4. Cross-language comparison (the plan's anti-claim)

The plan's anti-claim: if the bash kill-rate diverges wildly from the JS case, the divergence IS
the finding. Measured: it does not diverge wildly on the headline rate, and the language-class
differences sit elsewhere.

- O: headline rate — JS round 2: 8/10 (80 %, `corpus/knowledge/mutation-case-kimi-census.md:29-33`);
  bash round 3: 8/10 (80 %). Same boundary band; both sweeps held the suite count on every mutant
  run; neither produced an inconclusive run.
- O: kill **width** differs. The JS suite's baseline-breaking edits died on up to 16 of 43 cases;
  this run's widest kill is 3 of 16 (B3). (I) cause: the bash suite rebuilds a fresh fixture per
  case and asserts `exit + one token` per run (`:747-764`), while the JS suite shares in-memory
  fixtures and asserts exact verdict lines, so one wrong predicate colours many cases at once. A
  bash kill is structurally narrow — the failing-case labels above are near-singletons.
- O: survivor composition. JS survivors (D2, D10) were both reported-surface defects; bash
  survivors = one reported count (B10, same family as D10) + one fixture-absent arm (B5). The
  shared cross-language class is **reported-but-unasserted data**; the bash-only class is the
  **unreached arm** (in JS the analogous dropped-arm mutants D4/D5 were killed because cases
  pinned each arm; nothing pins the x-bit arm here).
- O: both suites' sharpest tools are exact strings: JS `'19 children, 18 declared'` and the exact
  CLEAN line; bash `unverified=3` (B7's tripwire).

## 5. Calibration and errata (append-only)

E1 — the pre-run expectation predicted the killed/survived verdict on **10/10** mutants but the
failing-case *counts* on only 6/10: B2 (predicted 1, measured 2), B3 (predicted 2, measured 3),
B6 (predicted 1, measured 2) all gained case 04 `runtime-absent`. Cause: I read case 04 as
special-purpose, but it is a second exit-0 green fixture — the full clean tree minus one runtime
row (`:770`) — so every defect that fires on green data kills it too. The miss was in reasoning
about the fixtures, not the edits (same shape as round-2 E1).

## 6. Unknowns

- U1 — coordinated multi-edit rewrites (e.g. both summary arg sets `:862` + `:866`, or a count
  increment plus its summary field) and check reordering are outside the single-edit experiment.
- U2 — verbs-logic mutants were excluded: on this host the two verb cases skip; on a
  handler-present host they exec the real binary, so their mutation verdicts would be host-gated.
- U3 — whether a handler-present host changes any of these ten mutant verdicts is unmeasured (the
  edits do not touch verbs code; I expect no change, but that is unmeasured).
- U4 — the fallback artifact `checklist-run.sh` was not exercised; its kill profile is unmeasured.
  (The census was used because its selftest proved hermetic here — §0.)
- U5 — kill-rate stability across hosts/toolchains (bash 5.x, sqlite3, python3, awk measured only
  on this host, 2026-10-14; ~1.0 s per run).
- U6 — nothing here measures the suite against live substrate drift; a hermetic suite never reads
  the live tree by construction.

## 7. Reproduce

Scratch (all under `/tmp/tameshi-r3-1-work/`): `pristine.sh` (byte copy of the pinned artifact),
`control.sh`, `mutant-B{1..10}.sh`, `mutate_driver.py`, `evidence/`
(`control.selftest.txt`, `B{1..10}.selftest.txt`, `B{1..10}.meta.json`, `results.json`,
`probe-B5-non-equivalence.txt`, `probe-B10-non-equivalence.txt`), probe fixtures `probe/`, `probe2/`.

Driver spec — the ten exact edits, each applied to a fresh copy (shown so the run can be rebuilt
from the note alone):

```
B1  surface-census.sh:241    [[ ${#SCAN_DIR[@]} -eq 0 ]] && return 0
                         ->  [[ ${#SCAN_DIR[@]} -ne 0 ]] && return 0
B2  surface-census.sh:435    elif [[ "$got" -ge "$floor" ]]; then printf 'SHAPE OK       %s rows %s %s >= %s\n' "$p" "$tbl" "$got" "$floor"
                         ->  elif [[ "$got" -gt "$floor" ]]; then printf 'SHAPE OK       %s rows %s %s >= %s\n' "$p" "$tbl" "$got" "$floor"
B3  surface-census.sh:229    if [[ -n "$want_mode" && "$want_mode" != "$mode" ]]; then
                         ->  if [[ -n "$want_mode" && "$want_mode" == "$mode" ]]; then
B4  surface-census.sh:200-204   the five-line symlink arm (`if [[ "$live" == "symlink" ]] … fi`) deleted
B5  surface-census.sh:214-217   the four-line exec x-bit block (`if [[ "$kind" == "exec" && ! -x "$abs" ]] … fi ;;`) -> `;;`
B6  surface-census.sh:371    if head -c "$(( ${#value} + 1 ))" "$abs" | cmp -s - "$MAGIC_EXPECT"; then
                         ->  if head -c "${#value}" "$abs" | cmp -s - "$MAGIC_EXPECT"; then
B7  surface-census.sh:405-406   printf 'SHAPE UNVERIFIED %s %s (%s)\n' "$p" "$assertion" "${S_ERR_A[$p]}"
                                N_UNVERIFIED=$((N_UNVERIFIED + 1)); FAILED=1
                            ->  the same two lines with N_UNVERIFIED + 2; the `:416` rows_min twin untouched
B8  surface-census.sh:85     die() { printf 'surface-census: %s\n' "$1" >&2; exit 2; }
                         ->  die() { printf 'surface-census: %s\n' "$1" >&2; exit 1; }
B9  surface-census.sh:191    if [[ "$cls" == "runtime" ]]; then  ->  if [[ "$cls" == "asset" ]]; then
B10 surface-census.sh:862    "${#SCAN_DIR[@]}" "$N_OK" "$N_ABSENT" "$N_SKIP"
                         ->  "${#SCAN_DIR[@]}" "$N_ABSENT" "$N_ABSENT" "$N_SKIP"
```

Commands (O: run in this order):

```
rm -rf /tmp/tameshi-r3-1-work && mkdir -p /tmp/tameshi-r3-1-work/evidence
cp -p kagi-shokunin/corpus/surface-census.sh /tmp/tameshi-r3-1-work/pristine.sh
sha256sum /tmp/tameshi-r3-1-work/pristine.sh            # 275d8294…53009f
python3 /tmp/tameshi-r3-1-work/mutate_driver.py --check # all unique
python3 /tmp/tameshi-r3-1-work/mutate_driver.py --run   # control + 10 mutants
# sensitivity checks (survivors, §2):
bash /tmp/tameshi-r3-1-work/mutant-B5.sh  verify --root /tmp/tameshi-r3-1-work/probe/host  --census /tmp/tameshi-r3-1-work/probe/census.tsv  --shapes /tmp/tameshi-r3-1-work/probe/shapes.tsv  --baseline /tmp/tameshi-r3-1-work/probe/baseline.tsv
bash /tmp/tameshi-r3-1-work/mutant-B10.sh verify --root /tmp/tameshi-r3-1-work/probe2/host --census /tmp/tameshi-r3-1-work/probe2/census.tsv --shapes /tmp/tameshi-r3-1-work/probe2/shapes.tsv --baseline /tmp/tameshi-r3-1-work/probe2/baseline.tsv
```

Sensitivity checks expected from the note alone: B5's run must print `SURFACE OK … (exec 644)`
exit 0 (pristine prints `SURFACE DIVERGED … no execute bit`, exit 1); B10's summary must read
`ok=0` (pristine `ok=1`), both exit 0.

Anchor spot-checks (three cited refs re-read on the pinned revision, 2026-10-14): `:241` →
`[[ ${#SCAN_DIR[@]} -eq 0 ]] && return 0`; `:214` →
`if [[ "$kind" == "exec" && ! -x "$abs" ]]; then`; `:862` →
`"${#SCAN_DIR[@]}" "$N_OK" "$N_ABSENT" "$N_SKIP"`.

## Erratum R21 — fixture mechanics and reproducibility (2026-10-21)

Section4's lines172–175 incorrectly inferred in-memory JS fixtures and
generally exact verdict assertions. The pinned JS `kimi-census.mjs` at
175de6ba uses filesystem fixtures and subprocesses (:430–460,471–512),
DRIFT prefix checks and an exact CLEAN assertion (:495–514); this note's
measured kill widths remain unchanged. The bash description is likewise
bounded: most fixture cases use exit/token checks, sqlite-unavailable
requires multiple tokens, and two verb cases are host-gated (14 executions
+2 skips on the recorded host). Width is not a quality ranking.
The old §7 commands depend on an unversioned scratch `mutate_driver.py`;
they do not by themselves recreate that driver after scratch loss.
Use `bash tools/mutate-and-run.sh --regression` for the maintained pinned
case replay. Evidence: round21 w2/Section0405.md and Section0375.md;
original historical bytes and8/10 observation remain unchanged.