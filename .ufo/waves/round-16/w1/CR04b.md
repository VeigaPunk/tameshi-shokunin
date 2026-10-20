# CR04b — cold-read, SKILL.md lines 131-245 (`## Mutation-sweep recipe`)

Snapshot: copied to `/tmp/tameshi-r16-CR04b-q8A6/SKILL.snapshot.md`; sha256 verified
`97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580` (one heading in
range, at line 131; the section runs past 245 — I also read lines 246-313 and
375-404, which my range *explicitly names* as "the next section" (step 4) and
"Full checklist below (Restore discipline)" (step 9), per the transitive rule).

## Section class and verdict

**Class: instruction** — the whole section is a numbered recipe a reader is told
to run ("Pick the target and prove its control", "Write the defect list", "Run
control + mutants"…). Embedded claims about the two historical sweeps are records
cited as evidence, but the section's own voice is imperative.

**Verdict: executed-ok.** I executed the recipe end to end on a permitted target
with no oral context. Details below.

## Execution — the recipe end to end (steps 1-10)

Target selection: the section designates "a suite" whose selftest is hermetic and
prints `<n>/<m>` + `VERDICT:`; `mutation-case-kimi-census.md` (explicitly cited,
:8-17) names `kumitate-shokunin/scripts/kimi-census.mjs`. Chosen.

**Step 1 — control.** `node /tmp/tameshi-r16-CR04b-q8A6/work/pristine.mjs
--selftest` → `KIMI_CENSUS_SELFTEST: 45/45 pass` / `VERDICT: PASS`, exit 0,
0.69 s (node v24.21.0). Hermetic: fixtures under the suite's own mkdtemp root.
Note: the printed count is now 45/45, not the cited 43/43 — the suite grew since
round 2; the recipe's shape claim (`n/m pass` + `VERDICT:`) held.

**Step 2 — pin.** `kumitate-shokunin` HEAD `1770305fae20826b39905a8251ddeca6b4957ac4`;
`scripts/kimi-census.mjs` sha256 `5e8d591324064fff714fb85b9d254b726deb9fd9cf15261eba135ccff6db3dc0`,
44770 B, 922 lines, mtime 2026-10-19 20:49:24 -0300; `git status --porcelain --
scripts/kimi-census.mjs` empty. (Substrate moved since the round-2 pin
`83016d45…4f426` / 896 lines — re-derived all `old` strings from the new bytes.)

**Step 3 — pristine copy.** `cp -p` → `/tmp/tameshi-r16-CR04b-q8A6/work/pristine.mjs`;
sha256 re-verified identical.

**Step 4 — defect list (pre-registered BEFORE any mutant run).** 11 defects, one
per catalog class + one widened class (inverted class select — the bash B9 analog
the catalog invites: "widen beyond the measured set when the artifact offers a
new mechanism"). All `old` strings copied from the pinned bytes. Expectations
filed in `mutate_driver.py` before `--run`:

| id | class | site (pinned rev) | expect |
|---|---|---|---|
| D1 | off-by-one count (table desync) | :109 `counted: 18`→`17` | killed |
| D2 | boundary/truncation cap | :382 `slice(0, 6)`→`slice(0, 5)` | **survived** |
| D3 | inverted condition | :336 `!e.children.includes(n)`→`e.children.includes(n)` | killed |
| D4 | dropped arm | :355-357 strays loop deleted | killed |
| D5 | weakened presence gate | :259 `gens.length > 0`→`true` | killed |
| D6 | wrong constant pin | :128 `modeFloor: 0o600`→`0o644` | killed |
| D7 | weakened predicate semantics | :310 `!== m.modeFloor`→`=== 0` | killed |
| D8 | wrong exit-code mapping | :400 `return 2`→`return 1` | killed |
| D9 | weakened kind pin | :296 `isLeaf(kind)`→`kind === 'file'` | killed |
| D10 | wrong reported constant | :149 `K2: 26`→`K2: 25` | **killed** (new assert :530-531) |
| D11 | inverted class select (widened) | :301 `'a directory'`↔`'a non-directory leaf'` | killed |

D10 prediction deliberately flipped vs round 2: the file now asserts all five
frozen counts at :530-531 (round 2 asserted only `frozen.K5`), so the round-2
survivor class is now pinned.

**Step 5 — uniqueness gate.** `python3 mutate_driver.py --check` → per-defect
`count=1` with first lines 109/382/336/355/259/128/310/400/296/149/301, literal
`all unique`; `new != old` asserted in code, exit 0.

**Step 6 — control + mutants.** `python3 mutate_driver.py --run`: fresh copy per
defect, literal `str.replace(old, new, 1)`, mutant sha256 ≠ pristine asserted,
300 s timeout, `evidence/<id>.selftest.txt` + `<id>.meta.json` + `results.json`
written. 12 runs in 8.40 s wall (~0.70 s each).

**Step 7 — adjudication.** Green = exit 0 AND `VERDICT: PASS` with the full count.

| id | exit | suite line | verdict | failing-case labels (verbatim) |
|---|---|---|---|---|
| control | 0 | `45/45 pass` / PASS | green | 0 |
| D1 | 1 | `29/45` FAIL | **killed** | 16 (green baseline exact-line, `--json` family/totals, `UNLISTED: a 19th lane file…`, 4 secrecy, chain/root-enum cases, 3 K5 MEMBER_MISSING, `verify` verb, …) |
| D2 | 0 | `45/45` PASS | **survived** | 0 |
| D3 | 1 | `29/45` FAIL | **killed** | 16 |
| D4 | 1 | `41/45` FAIL | **killed** | 4 (all root-enum/UNLISTED-root cases) |
| D5 | 1 | `44/45` FAIL | **killed** | 1 (`MEMBER_MISSING: the drift chain vanished entirely`) |
| D6 | 1 | `43/45` FAIL | **killed** | 2 (`SHAPE_DRIFT: server.token below its 0600 floor…`, FIFO collateral) |
| D7 | 1 | `43/45` FAIL | **killed** | 2 (both floor cases) |
| D8 | 1 | `42/45` FAIL | **killed** | 3 (all KIMI_ROOT_MISSING fail-closed cases) |
| D9 | 1 | `43/45` FAIL | **killed** | 2 (FIFO + dangling-symlink secrecy cases) |
| D10 | 1 | `44/45` FAIL | **killed** | 1 (`--json families read 3/26/9/9/3 and members=50`) |
| D11 | 1 | `43/45` FAIL | **killed** | 2 (kind-pin + leaf-pin cases) |

Kill rate = **10/11 (90.9 %)**, no inconclusive run, suite count held at `(n/45)`
on every run. Expectations: **11/11 correct** — including both judgment calls
(D2 survived, D10 now killed).

**Step 8 — survivor probe.** `node {pristine,mutant-D2}.mjs --root
work/empty-root`: pristine `DRIFT (…6 ids…; +22 more)` exit 1; mutant `DRIFT
(…5 ids…; +23 more)` exit 1 — observably different on ≥6-finding input; the suite
cannot see it. Non-equivalent, same "reported-but-unasserted tail" class as
round 2 (the DRIFT assert at :502 is still `startsWith` prefix + substrings).

**Step 9 — restore proof.** Re-ran step 2's checks after the sweep: sha256
`5e8d5913…dc0` identical, 44770 B and mtime 20:49:24 unchanged, porcelain empty,
HEAD unchanged. All edits lived in `/tmp`; the original was never a write target.
Satisfies the Restore-discipline checklist (items 1-3, 6; no drift → items 4-5
n/a; artifact was clean at pin → item 7 n/a).

**Step 10 — record.** The sweep record is this report's table + driver +
`evidence/results.json` (scratch retained). The "corpus row" half is L1/ledger
scope — a leaf seat may not write `corpus/`; noted as a scope boundary, not a
failure (see minor gaps).

Cost profile (per the section's own record requirement): 8.40 s wall for 12 runs,
300 s per-run timeout unused, node v24.21.0, python 3.14.8, this host. Cross-host
stability unmeasured (same U5 as both cited sweeps).

## Re-checked record anchors (the section's cited claims)

- `mutation-case-kimi-census.md`: :20-21 control `43/43`/`VERDICT: PASS` ✓;
  :22-25 driver `all unique` ✓ (mirrored in my driver); :29-33 kill 8/10, 7.0 s,
  count held ✓; :82-99 D2/D10 survivor probes (`+23 more`, `frozen=24`) ✓;
  :183-191 E1 miscall kept ✓.
- `mutation-case-kagi-census.md`: :24-26 mktemp fixtures ✓; :42-43
  `SELFTEST: PASS (16 cases)` ✓; :50-53 8/10, 11.0 s ✓; :88-91 B4 token-only
  kill ✓; :111-122 B5/B10 probes ✓.
- `gates-survey-kumitate.md:19-31`: six-gate table incl.
  `KIMI_CENSUS_SELFTEST: 43/43 pass` ✓ (round-2-era count, now stale vs live 45 —
  expected, it's a survey record).
- `gates-survey-kagi.md` §10/round-2 errata block: dirty-pin re-pin narrative ✓;
  `corpus/README.md` G-R2-1 row describes exactly the intermediate-dirty-state
  re-pin the recipe warns about ✓.
- Executable anchor: `tail -c1 kagi-shokunin/corpus/surface-census.sh` → `c`
  (887th line has no trailing newline, as :22-24 asserts) ✓; file still sha256
  `275d8294…53009f` at kagi HEAD `c2cab35b` ✓.

## Minor gaps (non-blocking inferences a reader must make)

1. Step 10's "record … a corpus row" is only half-executable by a leaf seat —
   corpus writes belong to L1. I recorded everything else; the corpus row needs
   an owner the page doesn't name.
2. Scratch convention `/tmp/<lane>-r<round>-<n>-work/` leaves `<n>` undefined for
   a replica seat; I used `/tmp/tameshi-r16-CR04b-q8A6/work/` (same namespace
   discipline).
3. The recipe never says which of the two historical suites to pick when both
   exist — "the suite" is any gate meeting the step-1 shape; correct by
   construction but a first-time reader must infer the freedom.

No blocking gaps; no wrong expectations — every instruction executed, every
cited record anchor re-checked true.

## Files opened

- `tameshi-shokunin/.ufo/evidence/round-16/coldread/SKILL.snapshot.md` (sha256-verified copy in scratch; lines 131-245 assigned + 246-313 and 375-404 as named references)
- `tameshi-shokunin/corpus/knowledge/mutation-case-kimi-census.md` (whole — cited throughout)
- `tameshi-shokunin/corpus/knowledge/mutation-case-kagi-census.md` (whole — cited throughout)
- `tameshi-shokunin/corpus/knowledge/gates-survey-kumitate.md:19-31` (cited)
- `tameshi-shokunin/corpus/knowledge/gates-survey-kagi.md` (errata refs, grep)
- `tameshi-shokunin/corpus/README.md` (G-R2-1 row, grep)
- `kumitate-shokunin/scripts/kimi-census.mjs` (pinned bytes; read via copies/grep only — substrate untouched)
- `kagi-shokunin/corpus/surface-census.sh` (`tail -c1` + `sha256sum` anchor checks only)

No installs performed. Scratch: `/tmp/tameshi-r16-CR04b-q8A6/` (driver, mutants,
evidence/, probes retained as the recipe's step-9.6 retention requires).

```json
{"seat":"CR04b","skill_sha256":"97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580","sections":[{"start":131,"heading":"## Mutation-sweep recipe — numbered steps; bounded cold-read evidence","class":"instruction","verdict":"executed-ok","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":["step 10 corpus-row half is L1 write scope, not executable by a leaf seat","/tmp/<lane>-r<round>-<n>-work/ leaves <n> undefined for replica seats","target suite ('the suite') is any step-1-shaped gate; which to pick is implicit"],"commands_executed":["sha256sum /tmp/tameshi-r16-CR04b-q8A6/SKILL.snapshot.md","git -C kumitate-shokunin rev-parse HEAD → 1770305fae20826b39905a8251ddeca6b4957ac4","sha256sum kumitate-shokunin/scripts/kimi-census.mjs → 5e8d5913…dc0 (44770 B, 922 lines, porcelain empty)","node work/pristine.mjs --selftest → KIMI_CENSUS_SELFTEST: 45/45 pass / VERDICT: PASS, exit 0","python3 mutate_driver.py --check → all unique (11/11 count=1)","python3 mutate_driver.py --run → control + 11 mutants, 12 runs in 8.40 s, kill rate 10/11 (90.9%), 0 inconclusive","node mutant-D2.mjs --root empty-root → '+23 more' vs pristine '+22 more', both exit 1 (non-equivalence proven)","restore: sha256/size/mtime/porcelain/HEAD identical after sweep","tail -c1 kagi-shokunin/corpus/surface-census.sh → 'c' (887th line, no trailing newline)"],"opened":["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-16/coldread/SKILL.snapshot.md","/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/mutation-case-kimi-census.md","/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/mutation-case-kagi-census.md","/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/gates-survey-kumitate.md","/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/gates-survey-kagi.md","/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/README.md","/home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/kimi-census.mjs","/home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/surface-census.sh"],"scratch":"/tmp/tameshi-r16-CR04b-q8A6/"}]}
```
