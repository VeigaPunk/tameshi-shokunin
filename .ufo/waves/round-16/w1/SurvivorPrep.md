# C1 survivor non-equivalence prep — kumitate `scripts/round-gate.mjs` (TameshiR16.SurvivorPrep)

Seat: `TameshiR16.SurvivorPrep` (leaf; no delegation). Wave 1.
Scope: for each arm that `corpus/knowledge/arm-class-matrix.md` §13.5 (reported-unread)
and §13.6 (unreached) predicts will **survive** the 60/60 suite, produce an **off-suite
probe** that distinguishes a mutant in that arm from the pristine gate, verify every
probe on the **pristine** pinned blob, and record the pristine observable.

Boundary observed: **no mutant was cut, copied-with-an-edit, or executed.** Every run
below invoked the pristine blob (sha `f890e277…a834d3e9`, re-verified). Divergence
signatures for mutants are therefore (I); the pristine observables are (O).

## 0. Result

- 12 predicted-survivor arms (5 in §13.5, 7 in §13.6); **15 probes**, **86 assertions**,
  **all pass on pristine** (`node /tmp/tameshi-r16-survivorprep/probes.mjs` → exit 0).
- 11 arms have a probe whose pristine observable a mutant in that arm cannot reproduce;
  each probe names the mutant divergence it catches.
- **1 arm — `INTERNAL_ERROR` (:683) — is uninhabited.** No argv/env/filesystem input
  reaches the catch-all; two constructor-visible throw routes were attempted and neither
  yields the token. Consequence: a token-text mutant there is *semantically equivalent*
  under every reachable input, so "survives" is the correct and only possible verdict.

| Arm (matrix §) | Source | Probe | Pristine observable (verified) | Mutant divergence (I) |
|---|---|---|---|---|
| FAIL-CLOSED detail tails + stderr diagnostic (§13.5 #1) | :615, :617, :648-649 | P1, P1b | exact stdout tail + exact stderr line, all six reachable tokens | tail/stderr edits |
| selftest summary counts (§13.5 #2) | :1505-1506 | P2 | `ROUND_GATE_SELFTEST: 60/60 pass` | `61/60`, recomputed counts |
| `durationMs` value (§13.5 #3) | :569, :613, :671 | P3, P7, P10 | `0 < d ≤ wall+5` at all three emission sites | constant 0, epoch, `started` |
| JSON `citations.mainProbeable/unresolved/notAncestor` (§13.5 #4) | :375-389 | P4, P4b | exact field values, both probeable polarities | dropped/forced pushes |
| text finding details (§13.5 #5) | :343, :350, :402, :430 | P5a, P5b | exact detail strings incl. paths | message/path edits |
| `INTERNAL_ERROR` (§13.6 #1) | :683 | P12 | **uninhabited** — no token, ever | none observable |
| tracked `REPORTS_DIR_MISSING` (§13.6 #2) | :527-529 | P6 | mode=tracked, checks=0, exact tail | arm removal → `NO_FILED_REPORTS` |
| main-repo `UPSTREAM_MISSING` (§13.6 #3) | :486-493 | P7 | `--main-repo … exit 128`, checks=12 | guard removal → **false CLEAN** |
| `--round` non-safe, `dirValue` flag-like, env-lane (§13.6 #4) | :246, :256, :278 | P8 | three exit-64 messages | validation removal |
| `UFO_SRC` set-value branch (§13.6 #5) | :161-163 | P9 | env origin wins; whitespace falls back | env branch lost/inverted |
| `--help`/`-h`, `--selftest --json`, main-repo flag>env (§13.6 #6) | :273, :635, :266-273 | P10 | unknown-arg 64; text suite; flag wins | special-case / precedence edits |
| `citationTokens` range form (§13.6 #7) | :315-324 | P11 | `checked=2`, `cited=2` | split removed → `checked=0` |

## 1. Artifact pin and pristine baseline (O)

`scripts/round-gate.mjs` lives in **kumitate-shokunin**, not the lane root. First
materialization attempt against the lane root failed (`fatal: path 'scripts/round-gate.mjs'
does not exist in '364f1d5…'`); the correct source repo is `kumitate-shokunin`.

```
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin \
    show 364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs \
    > /tmp/tameshi-r16-survivorprep/round-gate.mjs        # exit 0
$ sha256sum /tmp/tameshi-r16-survivorprep/round-gate.mjs
f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9
$ wc -l  → 1511
```

- Blob identity: `git ls-tree 364f1d5… scripts/round-gate.mjs` → `100755 blob 1f7d623e…b8579f3`.
- The matrix §13.10 pin is `f890e277…a834d3e9` at kumitate `175de6ba`. The C1 rev
  `364f1d5…` carries the **same blob sha**, so every §13 static read applies unchanged.
  Current kumitate HEAD `1770305f…` still hashes the script to the same sha (§13 is not stale).
- `grep -c "check('"` → **60**.
- Hermetic baseline: `node round-gate.mjs --selftest` → exit 0 in 3.68 s;
  `ROUND_GATE_SELFTEST: 60/60 pass`; `VERDICT: PASS`.
- Toolchain used: node v24.21.0, git 2.56.0. No installs or upgrades were needed or made.
- kumitate tree porcelain-clean before/after (`git status --porcelain | wc -l` → `0`);
  the only writes are this report and `/tmp/tameshi-r16-survivorprep/**`.

Probe harness (scratch): `/tmp/tameshi-r16-survivorprep/probes.mjs`
sha256 `131c2835b1b5ce5fab60960fbca864c444d2cd75c19f08da410616e49bd332fb`. It builds
every fixture from scratch (deterministic git identity/dates), so probes are independent
of the suite's fixtures. `GATE` and `FXROOT` are overridable:

```
GATE=<path to the exact script copy under test> FXROOT=/tmp/<unique-dir> \
  node /tmp/tameshi-r16-survivorprep/probes.mjs <PROBE-ID>
```

The override was validated on a byte-identical copy at a different path
(`gate-copy/round-gate.mjs`, same sha) for P2: all assertions pass, exit 0. **For a
survivor mutant, point `GATE` at that mutant's copy and give each run its own `FXROOT`.**

## 2. Probe catalogue

Common environment for every probe: `{PATH, HOME}` only (plus the per-probe overrides
named below); `KUMITATE_*`/`UFO_SRC` are *not* inherited. Fixtures are rebuilt per run;
paths below are the ones observed.

### P1 — FAIL-CLOSED detail tail + stderr diagnostic (§13.5 #1)
Gate argv (observed):
`--round 5 --repo /tmp/tameshi-r16-survivorprep/fx/p1/lane --reports-dir /tmp/tameshi-r16-survivorprep/fx/p1/absent-reports`
Pristine (O): exit **2**;
stdout exactly
`ROUND_GATE: FAIL-CLOSED (REPORTS_DIR_MISSING) --reports-dir /tmp/tameshi-r16-survivorprep/fx/p1/absent-reports is absent`
stderr exactly
`round-gate: fail-closed — REPORTS_DIR_MISSING: --reports-dir /tmp/tameshi-r16-survivorprep/fx/p1/absent-reports is absent`
`--json` variant (O): 13 frozen top-level keys
(`checks,citations,contract,durationMs,errors,findings,lane,mode,repo,reportsDir,round,verdict,warnings`),
`checks=[]`, `citations` all-default (`checked:0`, empty lists, both probeable `null`), and
`findings[0].detail ==` the stdout tail.
Mutant divergence (I): the suite (fcA/jFc) reads token/kind only. Any edit to the detail
tail or to the `:615` stderr line (`round-gate: fail-closed — ${token}: ${detail}`) leaves
every suite check green and one of the exact-string assertions red. A schema-key edit in
the fail-closed body is invisible to `jClean` (audit body only) and caught by the key-set
assertion.

### P1b — remaining FAIL-CLOSED tails (§13.5 #1, §13.6 #2 adjacent)
Five invocations over a shared fixture tree. Pristine (O):

| Site | argv (key parts) | exit | exact observable |
|---|---|---|---|
| `NOT_A_GIT_WORKTREE` :644 | `--round 5 --repo <plain> --reports-dir <empty>` | 2 | `ROUND_GATE: FAIL-CLOSED (NOT_A_GIT_WORKTREE) --repo <plain> is not a git work tree` |
| `NO_CLOSED_ROUND` :652 | `--repo <git> --reports-dir <empty>` | 2 | `ROUND_GATE: FAIL-CLOSED (NO_CLOSED_ROUND) no round-<N>/kumitate.md under <empty>` |
| `MAIN_REPO_NOT_GIT` :531 (tracked) | `--tracked --reports-dir <empty> --main-repo <plain> --json` | 2 | `mode=tracked`, `checks=[]`, detail `--main-repo <plain> is not a git work tree` |
| `MAIN_REPO_NOT_GIT` :471 (close) | `--close --json --round 5 --repo <lane+upstream> --reports-dir <reports> --main-repo <plain> --origin <absent>` | 2 | `mode=close`, **`checks=12`**, same detail |
| `NO_FILED_REPORTS` :536 | `--tracked --reports-dir <one round-7 report> --main-repo <git> --json` | 2 | `checks=[]`, detail `filed=1 round-<N>/kumitate.md under <reports> (the highest round is excluded as in-flight, so >=2 are needed)` |

Mutant divergence (I): fcB–fcF/rt3/rt5 assert the token only. Tail edits die on the exact
strings; a site-local change (e.g. only the tracked `MAIN_REPO_NOT_GIT`) flips
`mode/checks` (tracked/0 vs close/12) and is caught even when the text is shared.

### P2 — selftest summary counts (§13.5 #2)
`node <gate> --selftest` → exit 0; last two lines exactly
`ROUND_GATE_SELFTEST: 60/60 pass`, `VERDICT: PASS` (O).
Mutant divergence (I): the suite's hermeticity check reads
`/^ROUND_GATE_SELFTEST: \d+\/\d+ pass$/` (:1399) and `VERDICT: PASS`; it never reads the
numbers. `${passed + 1}/${results.length}` prints `61/60 pass`, keeps `VERDICT: PASS`, and
passes every suite check while failing P2. Note: a *recomputation* that equals `passed`
on the all-pass path (e.g. `${results.length}`) is genuinely equivalent and P2 cannot
distinguish it — P2 kills count-*printing* mutants, not refactors.

### P3 — `durationMs` value, audit emission (:671) (§13.5 #3)
Clean-audit fixture (10 checks green, CLEAN). `--json` run (O):
`verdict=CLEAN checks=10 durationMs=2 outerWall=20.19 ms`; second run `durationMs=3
outerWall=17.82 ms`. Assertions: `0 < d ≤ wall+5` on both.
Tracked (:569) and fail-closed (:613) emissions are covered by P10 and P7 respectively
(observed `3` vs `17.21 ms`, `7` vs `21.81 ms`).
Mutant divergence (I): the suite asserts `typeof === 'number'` only (:1263). `0`,
`Date.now()`, `started`, or a large offset all fail the bracket; **a ±1 ms additive edit
is inside the noise envelope and is not claimed**.

### P4 / P4b — JSON citations fields (§13.5 #4)
Fixture P4: lane repo with an orphaned commit (`HEAD` reset back one), a main repo with
its own commit, an origin repo, one report citing `«orphan» «main-commit» deadbeef1234`.
Pristine (O), exit 1:
`checked=3 external=["faa0781b3a4a169297938050775afda012dfd660"]
unresolved=["deadbeef1234"] notAncestor=["bf252667f5dd8fd6b9bd55487cc9f3d5b4c16671"]
unverifiable=[] mainProbeable=true originProbeable=true`;
check details `cited=3 unresolved=1 [deadbeef1234]` and
`cited=3 notAncestor=1 [bf252667…]`.
P4b polarizes `mainProbeable`: non-git `--main-repo`, git `--origin`, one unknown token →
`mainProbeable=false originProbeable=true unresolved=[] unverifiable=["deadbeef1234"]` (O).
Mutant divergence (I): the suite reads `checked` (clean fixture, 0), `external`
(derived-origin fixtures), `unverifiable`/`originProbeable`, never `mainProbeable`,
`unresolved`, `notAncestor`. Dropping either `push` fails P4; forcing `mainProbeable`
true/false fails exactly one of P4/P4b.

### P5a / P5b — text finding details (§13.5 #5)
P5a (report absent), pristine (O), exit 1, stdout exactly:
```
ROUND_GATE  error  REPORT_MISSING  /tmp/…/fx/p5a/empty-reports/round-5/kumitate.md
ROUND_GATE: DRIFT (round=5 lane=kumitate checks=5 errors=1 warnings=0)
```
P5b (mismatched report + rowless SCORECARD + wrong LOG), pristine (O), exit 1, exact lines:
```
ROUND_GATE  error  REPORT_ROUND_MISMATCH  neither "round-5" nor "round <5>" in /tmp/…/fx/p5b/reports/round-5/kumitate.md
ROUND_GATE  error  SCORECARD_ROW_MISSING  no table row starting "| 5 |" in /tmp/…/fx/p5b/lane/SCORECARD.md
ROUND_GATE  warning  SCORECARD_PLAN_MISSING  no ## Planned section in /tmp/…/fx/p5b/lane/SCORECARD.md
ROUND_GATE  error  LOG_ENTRY_MISSING  no "- YYYY-MM-DD — round 5" line in /tmp/…/fx/p5b/lane/LOG.md
ROUND_GATE  error  COMMIT_MISSING  no message matching \bround[- ]5\b in <n> messages of /tmp/…/fx/p5b/lane
```
Mutant divergence (I): r3 pins the kind list/count; r7's message and r10's/r15's paths
are unread; any path or message edit is caught by exact-line equality.

### P6 — tracked-mode `REPORTS_DIR_MISSING` (:527) (§13.6 #2)
`--tracked --lane kumitate --reports-dir <absent> --main-repo <git> --json` → exit 2 (O):
`mode=tracked round=null verdict=FAIL-CLOSED checks=0`, finding
`REPORTS_DIR_MISSING`, detail `--reports-dir <absent> is absent`; stderr diagnostic same
tail. Main-site control: identical token/tail, `mode=audit` (text).
Mutant divergence (I): fcA/jFc exercise the main site only. A token edit differs here;
deleting the tracked guard falls through to `roundReports()` on an absent dir →
`NO_FILED_REPORTS` (`filed=0`) with a different detail — both caught.

### P7 — main-repo `UPSTREAM_MISSING` (:488) (§13.6 #3)
Close fixture: lane repo clean + upstream (`ahead=0`), main repo tracks the report and has
**no upstream**, origin absent. `--close --json …` → exit 2 (O):
`mode=close verdict=FAIL-CLOSED checks=12`,
detail `--main-repo /tmp/…/fx/p7/main: exit 128 fatal: no upstream configured for branch 'main'`,
`durationMs=7` vs `wall=21.81 ms`.
Mutant divergence (I): fcE exercises the lane `--repo` site and matches `/no upstream|exit
128/` only. Swapping the detail prefix `--main-repo`→`--repo` is invisible to the suite and
caught by the prefix assertion. Removing the `return` after the non-zero `git log
@{u}..HEAD` is worse: `names` becomes empty, `REPORT_UNTRACKED` is added *ok*
(`tracked+pushed: …`) and the gate returns **exit 0 / CLEAN** — a false green that P7
catches on exit/verdict/kind/checks.

### P8 — usage/validation siblings (§13.6 #4)
Pristine (O), each exit **64**, first stderr line exact:
```
--round 9007199254740992      → round-gate: --round out of range (got "9007199254740992")
--repo --json                 → round-gate: --repo requires a directory (got "--json")
(env KUMITATE_LANE=1bad)      → round-gate: KUMITATE_LANE must match ^[A-Za-z][A-Za-z0-9-]*$ (got "1bad")
```
Each is followed by a blank line and the usage block.
Mutant divergence (I): u1 pins `--bogus`, u2/u3 pin `--round abc`/missing, u4 pins an
invalid `--lane`, none pins these branches. Removing `Number.isSafeInteger` accepts 2^53
and falls through to normal failure codes; removing the `startsWith('--')` guard resolves
`--json` as a directory; removing the env-lane regex accepts `1bad`. All three change
exit/message and are caught.

### P9 — `UFO_SRC` set-value branch (:161-163) (§13.6 #5)
Fixture: `HOME=<tmp>` with a real `Projects/ufo-fsd-alpha` repo (candidate) **and** a
separate alt-origin repo. No `--origin` is passed.
- A: `HOME=<tmp> UFO_SRC=<alt>` → exit 1 (thin report) but citations (O):
  `external=["a3706ee327d8f706a51177670195e6e8c6ba360e"]`, `originProbeable=true`,
  `unresolved=[]`.
- B: `HOME=<tmp> UFO_SRC="   "` (3 spaces), report cites the candidate commit →
  `external=["3131ae056275222d65a17d3e0d4d1643395700ea"]`, `originProbeable=true` (O).
Mutant divergence (I): every derived-origin suite fixture forces `UFO_SRC: ''`, and the
nested hermetic run never resolves the default. If the env branch returns the candidate
instead of `resolve(envSrc)`, A flips to `external=[] unresolved=[altSha]`; if the trim
guard is dropped, B resolves the whitespace path (non-git) and flips to
`originProbeable=false unverifiable=[candSha]`.

### P10 — documented readings with no pin (§13.6 #6)
Pristine (O):
```
--help  → exit 64, first stderr line: round-gate: unknown argument: --help
-h      → exit 64, first stderr line: round-gate: unknown argument: -h
--selftest --json → exit 0; first line "kumitate round-gate --selftest (hermetic, node v24.21.0)";
                    last line "VERDICT: PASS"; not JSON
--tracked --json --main-repo <good>, env KUMITATE_MAIN_REPO=<bogus> →
        exit 0, mainRepo=<good>, checked=2, excludedRound=5, durationMs=3 vs wall=17.21
```
Mutant divergence (I): u1 pins `--bogus` only, so `--help`/`-h` special-casing is caught
here. No suite fixture combines `--selftest` with `--json`; an edit to the `:635`
precedence line changes the output shape. r45 discriminates reports-dir/lane precedence
only; an env-first main-repo mutant fail-closes `MAIN_REPO_NOT_GIT` instead of returning
CLEAN — caught by exit+mainRepo.

### P11 — `citationTokens` range form (:315-324) (§13.6 #7)
Lane repo with two commits; report cites `` `aaaaaaa..bbbbbbb` `` (7-hex parts) (O):
`citations.checked=2`; `COMMIT_CITED_UNRESOLVED.detail == "cited=2 unresolved=0"`;
`COMMIT_CITED_NOT_ANCESTOR.detail == "cited=2 notAncestor=0"`.
Mutant divergence (I): all suite citations are single backticked tokens. Removing the
`split(/\.\.…/)` makes the whole span fail `^[0-9a-f]{7,40}$` → `checked=0`, detail
`no cited commit tokens`; caught.

### P12 — `INTERNAL_ERROR` (:683) (§13.6 #1): uninhabited
Attempted routes on pristine (O):
| Route | Result |
|---|---|
| `TMPDIR=/nonexistent/t node <gate> --selftest` | exit **1**, raw `node:fs:3134 … binding.mkdtemp` stack, **no** `INTERNAL_ERROR` (selfTest is called at :635, outside main's `try` at :638) |
| stdout to `/dev/full` on a CLEAN audit run | exit 1, `node:events:505 … Unhandled 'error' event`; the write error is asynchronous, delivered after `main()` returned — token does **not** fire |
| `--repo <regular file>` | exit 2, `NOT_A_GIT_WORKTREE` (normal refusal) |

Why no route exists (I, from the pinned bytes): every inner failure is caught or returned
inside the `try` — `statKind`/`readText` catch, `readdirSync` catches, `spawnSync` returns
`{status,error}` rather than throwing, and all argv/env-derived values are strings
(`resolve`/`RegExp`/`Buffer.byteLength` cannot throw on them). The only throw sources
(`mkdtempSync` in `selfTest`) sit outside the catch. `INTERNAL_ERROR` is therefore dead
code on this platform; a single-edit token mutant is an equivalent mutant, and no probe
can show non-equivalence. Do not score it as a detection loss.

## 3. Verification log (O)

```
$ node /tmp/tameshi-r16-survivorprep/probes.mjs        # exit 0
15 probes, 86 assertions, all pass
P1  ALL PASS   P1b ALL PASS   P2  ALL PASS   P3  ALL PASS   P4  ALL PASS
P4b ALL PASS   P5a ALL PASS   P5b ALL PASS   P6  ALL PASS   P7  ALL PASS
P8  ALL PASS   P9  ALL PASS   P10 ALL PASS   P11 ALL PASS   P12 ALL PASS
$ sha256sum round-gate.mjs  → f890e277…a834d3e9   (same file before and after)
```
Key durations: audit `durationMs=2` vs wall `20.19`; tracked `3` vs `17.21`; fail-closed
`7` vs `21.81`. Fixture commit shas quoted above are deterministic for the pinned
`GIT_*` identity/date environment and are recomputed by the harness (nothing is hardcoded).

## 4. Bounded recommendations for L1

1. **Pre-register the arm-level predictions now**: every row in §0 except `INTERNAL_ERROR`
   is expected to survive the 60/60 suite if the edit lands in that arm, and each has a
   probe that decides non-equivalence. Attach this table to leg `js-round-gate` before the
   sweep.
2. **After the sweep, run each survivor's probe against that mutant's exact copy**:
   `GATE=<mutant-copy>/round-gate.mjs FXROOT=/tmp/tameshi-r16-survivorprep/fx-<mutant> \
   node /tmp/tameshi-r16-survivorprep/probes.mjs <PROBE-ID>`.
   A failing assertion is the non-equivalence witness; quote the first failing
   `name/expected/got` triple in the ledger entry.
3. **`INTERNAL_ERROR`**: if the 10-mutant set includes a token-text edit at :683, record
   the survivor as *equivalent-by-unreachability* with P12 as evidence, or omit the mutant;
   either way it is not a suite hole that a fixture can close.
4. **Highest-value mutant of the set**: the main-repo `UPSTREAM_MISSING` guard (§13.6 #3).
   It is not just unread text — deleting the guard turns a refusal into a **false CLEAN**
   (P7 divergence), which is the strongest non-equivalence in this projection.
5. **Keep these probes out of `round-gate.mjs`.** They are off-suite, CLI-level evidence
   for the ledger; folding them into the suite would change the artifact under audit and
   invalidate the 60/60 pin.
6. **Probe limits**: P3's bracket is a gross-value discriminator (not ±1 ms); P2 kills
   printed-count edits, not equivalent recomputations; P12 has no observable at all.

## 5. Method boundaries and opened material

- Read: `corpus/knowledge/arm-class-matrix.md` (headline, §1, §13 including §13.1–§13.10,
  errata), the pinned `round-gate.mjs` (line ranges 1–200, 200–340, 340–470, 470–560,
  560–700, 700–880, 1170–1240, 1240–1400, 1400–1511, plus targeted `grep -n`), and
  kumitate git metadata (`show`, `rev-parse`, `ls-tree`, `status`).
- Did **not** open the lane's LOG/SCORECARD/SHONEN/plans/reports/corpus-lessons/other
  seats' reports; no sibling repo was written, checked out, stashed or committed.
- No tool installs/upgrades. No mutant executed. One concise `agent://TameshiR16` message
  with the post-sweep classifier command and the `INTERNAL_ERROR` disposition; this report
  remains the full evidence.
- Scratch: `/tmp/tameshi-r16-survivorprep/` (`round-gate.mjs`, `probes.mjs`,
  `probes.pristine.log`, fixtures under `fx/`). Report: this file.
