# T51W2Read06 — cold-read re-key reader: `### Using the ledger`

Seat T51W2Read06, round 51 wave 2 (falsify), lane `tameshi-shokunin`.
BASE `9962033fd7a75aa2f2847e979dd687a5d28505a1` · CAND `6d8c11e378aa90b12650808e1b79270742935f15`.

Method: the heading was re-resolved at CAND (`grep -n '^### \|^## '` on `git show CAND:SKILL.md`), the section
read in full through the next heading, and **every pointer in it checked against the candidate bytes** of the
file it cites (`git show CAND:tools/mutate-and-run.sh`, 2159 lines; BASE 2080). The same pointers were also
checked at the round-26 (`a08e85c`) and round-18 (`58e5d53`) runner revisions to date each staleness. Two
falsifiers were **executed**, not only read (§5). Read-only on the lane; all execution inside a `--shared`
scratch clone with its toplevel asserted; scratch deleted before yield. The old READERS_JSON and the w1
fixture list were not trusted: the pointers below were extracted from the section bytes themselves (they
match the fixture list's enumeration for this section, which is corroboration, not source).

## 1. The section at CAND

`### Using the ledger` = SKILL.md:933-964 at CAND; next heading `### Reading a receipt — the discipline` at
:965. **Byte-identical to BASE** (diff of 933-965 empty). Section sha256
`57ac17ec1a08473f278cff466eb799253adddd8cca8541fdd3cbaa330dc44746` (31 body lines, trailing blank popped) —
the same sha the round-21 ledger's existing entries for this heading pin, so the *page* did not move; what
moved is the one file every pointer cites: `tools/mutate-and-run.sh`.

Verbatim (CAND 933-963, wrapped as stored):

```text
### Using the ledger

- **One command replays every leg.** `bash tools/mutate-and-run.sh
  --regression [--workdir DIR] [--keep]` allocates a fresh default scratch
  `/tmp/tameshi-r4-2-regression.XXXXXX` after prerequisite checks. Once allocated,
  it is removed on PASS unless `--keep`, retained on FAIL/SETUP; caller workdirs
  are never removed. Pre-allocation SETUP has no root to retain. Exits0/1/2:
  PASS/FAIL/SETUP (`tools/mutate-and-run.sh:126-136,1273-1294,1364-1384`).
- **Each leg's bytes come from the repo's git object store, not the working
  tree.** `git show <rev>:<path>` materializes the pinned blob into the case
  workdir and validates mode/SHA (`tools/mutate-and-run.sh:1104-1175`);
  `REGRESSION_PIN` names repo/rev/path/pin (:1159-1160). Working-tree drift
  does not change that blob. The old tsukuroi/mado pins are historical,
  not a statement that their current trees match those recorded bytes.
  A missing repo/rev/blob or pin mismatch refuses before that leg's suite;
  later legs still run and their statuses aggregate (:1384-1450 since round 26).
- **Every kill-rate claim carries the receipt.** Cite `REGRESSION: PASS
  (cases=N passed=N; …)` (N=4 at r7-1, 7 since round 16, 8 since round 18, 9 since round 26) with the
  executed tool sha (`REGRESSION_TOOL`) and the per-leg pins
  (`REGRESSION_PIN`) — the receipt is tied to the tool revision that ran and
  to each leg's pinned bytes.
- **Contribution contract — what a leg carries.** A pinned target path,
  Git revision and SHA; one-edit defects with unique `@old` and `@new != @old`;
  a command exercising `$MUTANT` under controlled fixtures; enumerated,
  executed and skipped counts distinguished; and the exact recorded verdict
  table. Host-gated branches must be excluded/controlled or explicitly named,
  not called hermetic merely because the flag is `--selftest`.
  Current anchors (round 26): pins/revisions/tables `tools/mutate-and-run.sh:603-629`,
  first-four specs :657-839, inventory :83-108, nine dispatches :1384-1428.
  (U) The recorded case set remains tameshi-carried; no fleet-contributed
  leg is established by this registry.
```

Eight citations, ten line ranges, one cited file. All ten checked at CAND.

## 2. Pointer verdicts at CAND

| # | raw pointer | claim it anchors | what the cited range holds at CAND | verdict | described content located at CAND |
|---|---|---|---|---|---|
| 1 | `tools/mutate-and-run.sh:126-136` | scratch allocation/removal + exits (bullet 1) | materialization/stated-expectation header comment ("move a replay. The materialized copy's sha256 must equal the recorded pin; … Stated expectation: ledger legs are byte-pinned replays …") | **absent** | exit-map comment :139-143; scratch-root comment :149-151; allocation :1432; removal :1542-1544; exits :1548/:1523/:1529/:1538 |
| 2 | `:1273-1294` (same bullet) | (same) | git-show SETUP refusals + blob-mode mirror inside `regression_case` (:1271-1294: "path not in revision", "git show failed", blob-mode read/empty) — supports bullet 2's *refusal* claim, not bullet 1's scratch claim | **absent** | `run_regression` entry: usage refusals :1418-1422, prerequisite checks :1423-1427, workdir/specs setup :1429-1440 |
| 3 | `:1364-1384` (same bullet) | (same) | comparison-loop tail + expectation computation (:1364-1389: `done <"$rtsv"`, table-pair ABSENT loop, `delta`/`reasons`) | **absent** | FAIL/SETUP/PASS outcome blocks + `rm -rf "$root"` :1519-1548 |
| 4 | `tools/mutate-and-run.sh:1104-1175` | `git show` materializes pinned blob, validates mode/SHA (bullet 2) | tail of the embedded js-cite-check spec (:1104-1154) then the **new leg-10 `bash-drift-pins` spec header + first defects** (:1155-1175) | **absent** | `regression_case` comment :1222-1238; `git_clean -C "$repo" show "${rev}:${path}" >"$dst"` :1276; blob-mode read + 100755→+x mirror :1285-1300; sha validation :1307-1317 |
| 5 | `:1159-1160` | `REGRESSION_PIN` names repo/rev/path/pin (bullet 2) | drift-pins spec header lines: :1159 "# Predictions were fixed before any mutant run. Composition: 5 kill-aimed / 5 hole-aimed." · :1160 "# Matrix axes: mode compare, symbol GONE arm, …" | **absent** | `printf 'REGRESSION_PIN %s: source=git repo=%s rev=%s path=%s mode=%s sha256=%s\n' …` :1302-1303 (file variant :1305) |
| 6 | `:1384-1450 since round 26` | refusal before that leg's suite; later legs still run; statuses aggregate (bullet 2) | band-check/verdict prints ending `regression_case` (:1384-1402), `regression_case_git` (:1404-1415), `run_regression` entry (:1417-1450) | **absent** | refusals all before the suite: repo-identity guard :1252-1266, rev-not-found :1267-1270, path-not-in-rev :1271-1274, git-show failure :1276-1280, mode-read failure :1285-1294, pin mismatch :1307-1317, suite invoked only at :1320-1322; ten sequential dispatches capture statuses, no early exit (`set -u -o pipefail` :183); aggregation :1510-1517 + :1519-1548 |
| 7 | `tools/mutate-and-run.sh:603-629` | anchor "pins/revisions/tables" (bullet 4) | knowledge-note comment tail (:603-613) + PIN_JS..REV_SOURCESCHECK (:614-629) — **no TABLE_\* lines** | **absent** | pins/revisions :614-633 (PIN_JS :614 … REV_DRIFTPINS :633), tables :634-643 (TABLE_JS :634 … TABLE_DRIFTPINS :643) |
| 8 | `:657-839` | anchor "first-four specs" (bullet 4) | `table_lookup`/`table_count` (:646-668), `regression_specs` head (:669-671), first three specs (:673-839) | **absent** | `regression_specs() { # <dir> — write the ten embedded case specs` :671; spec writes :673 (js-kimi), :714 (bash-surface), :759 (bash-tsukuroi), :804 (bash-mado) — four specs span :673-852 |
| 9 | `:83-108` | anchor "inventory" (bullet 4) | `--regression` header (:84), leg inventory :88-97 **including the new `bash-drift-pins … 2/10 (20 %)` row :97**, sources :98-104 **including the leg-10 spec path :104** | **holds** (truncated tail) | provenance notes the range used to close on now extend to :121 (leg-10 note :111-113, "All ten defect specs…" :114-121) |
| 10 | `:1384-1428` | anchor "nine dispatches" (bullet 4) | same region as #6 (verdict prints, git wrapper, `run_regression` entry) | **absent** | the **ten** dispatches :1459-1508 (tenth `bash-drift-pins` :1504-1508); the text "nine dispatches" is itself stale |

## 3. Statements made false or stale at CAND (text level)

- **T1 — FALSIFIED (executed).** Bullet 1's literal scratch path `/tmp/tameshi-r4-2-regression.XXXXXX`. At
  CAND the template is `"${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX"` (:1432; header :149-151: "r51
  honours TMPDIR"). With TMPDIR set the scratch is not under /tmp. The same change hit the run-mode default
  (:491) and the selftest root (:1555). Executed probe in §5.2.
- **T2 — stale.** Bullet 3's receipt-count history "(N=4 at r7-1, 7 since round 16, 8 since round 18, 9 since
  round 26)" is true through round 26, but at CAND receipts print `cases=10` (:1540; the selftest asserts the
  exact line `REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)` at :2087).
  A reader following the bullet at CAND would cite N=9.
- **T3 — stale.** Bullet 4's "nine dispatches": ten at CAND (:1504-1508).
- **T4 — pre-existing (since round 26), not caused by r51.** Bullet 1's three ranges and bullet 2's
  `:1159-1160` were **already stale at BASE** (see §6): the round-26 SKILL edit (`40a12bf`) refreshed the
  anchors and added "since round 26" but did not refresh these four ranges.
- **T5 — minor wording.** "validates mode/SHA": the sha is validated (:1312-1317); the mode is read and
  mirrored (:1285-1300), never compared against a recorded mode.
- **T6 — weak anchor.** "enumerated, executed and skipped counts distinguished": the runner has no skip
  concept (`grep -i skip` hits only embedded spec text; the outcome taxonomy is
  KILLED/SURVIVED/INCONCLUSIVE); the enumerated/executed convention lives in the knowledge-note manifests
  (e.g. `corpus/knowledge/mutation-case-kimi-census.md:32` "every mutant run still enumerated the full
  suite"), which this bullet does not cite. Unverifiable from the cited ranges alone; no falsifier.

## 4. Claims verified TRUE at CAND (behavioral, pointer-independent)

- One command replays every leg — now ten (`nlegs=10` :1510; selftest leg-count agreement wants 10,
  :2045/:2047-2048).
- Scratch: allocated after prerequisite checks (:1423-1427 → :1432); removed on PASS unless `--keep`
  (:1542-1544); retained on FAIL/SETUP (:1522/:1528/:1537 print "(kept)", no removal); caller workdirs never
  removed (`auto=1` guard :1542); pre-allocation SETUP has no root to retain (die_setup :1423-1427 precede
  the allocation).
- Exits 0/1/2 = PASS/FAIL/SETUP (:1548 / :1523 / :1529,:1538). (Regression misuse additionally exits 64 via
  `usage_exit` :1419 — the bullet never claimed an exhaustive map.)
- Materialization from the object store, not the working tree: `git show <rev>:<path>` :1276 into
  `<case-workdir>/target.<basename>` :1275; sha must equal the recorded pin :1312-1317; mode mirrored for
  re-exec gates :1281-1300.
- `REGRESSION_PIN` names repo/rev/path/pin (plus mode) :1302-1305.
- Refusal before that leg's suite; later legs still run; statuses aggregate (§2 row 6 located lines).
- Receipt: `REGRESSION: PASS (cases=N passed=N; ledger legs exact: killed-delta<=0 flips<=0)` :1540-1541;
  `REGRESSION_TOOL: <self> sha256=…` :1442; per-leg `REGRESSION_PIN` :1302-1305.
- Contribution contract: duplicate `@old` refused (count==1 asserted) and `@new == @old` refused (format
  comment :45-53, enforced by the parser); `$MUTANT` exercised (suite contract :54-62); exact recorded table
  compared :1342-1374.
- (U) "recorded case set remains tameshi-carried; no fleet-contributed leg": holds at CAND — leg 10's spec is
  tameshi's round-51 pre-registration (committed in fe335384 before any mutant ran, runner header :111-113)
  and its sweep is tameshi's recorded evidence (`.ufo/evidence/round-51/c2/sweep/sweep.txt`); the target
  being a kagi file matches legs 2 and 5 and does not make the leg fleet-contributed.

## 5. Executed falsifiers

1. **Runner selftest at CAND.** `git clone -q --shared <lane> $S/selftest/lane` → `checkout -q --detach
   6d8c11e…` (toplevel asserted = the clone) → `TMPDIR=$S/tmp bash tools/mutate-and-run.sh --selftest` →
   **exit 0, `MUTATE_SELFTEST: 107/107 pass`, `VERDICT: PASS`**. The runner is green at CAND (C3's
   requirement) and the tenth leg is exercised inside it: leg tuples = 10 (:2045, count asserted :2047) and
   the tally harness asserts the exact `cases=10` receipt line (:2087).
2. **TMPDIR probe (run mode, same clone).** 2-line fixture target + 1-defect spec, `TMPDIR=$S/tmp2 bash
   tools/mutate-and-run.sh --target … --defects … --suite 'bash "$MUTANT"' --keep` → exit 0,
   `MUTATE_EVIDENCE: /fast/scratch/hyaku/tameshi-r51/T51W2Read06/tmp2/tameshi-r4-2-run.qX27Rx` — the default
   workdir allocated under the caller's TMPDIR, **not /tmp**. Same mktemp construct as the regression scratch
   (:1432), so bullet 1's literal `/tmp/…` claim is false at CAND.
3. **Sha chain.** sha256(BASE runner) = `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` —
   exactly the input sha the round-21 ledger's existing `### Using the ledger` entries pin;
   sha256(CAND runner) = `977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda`. That delta is
   the `input-drift:tools/mutate-and-run.sh` that drops this section's credit at CAND, and the re-key trace
   will bind the new sha. Section sha unchanged (`57ac17ec…` at both revs).

## 6. When each pointer was last correct

- **Bullet 1's bundle (:126-136, :1273-1294, :1364-1384): exact at round 18** (`58e5d53`): :126-136 = the
  exit map + "Scratch root: mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX by default; removed on PASS unless
  --keep, kept on FAIL/SETUP, never removed when --workdir was given. In this mode --target/… refused (usage
  error)"; :1273-1294 = `run_regression()` entry (usage refusals :1275-1276, workdir handling :1292-1294);
  :1364-1384 = the FAIL/SETUP/PASS outcome blocks (`rm -rf "$root"` :1380, `exit 0` :1384). Stale since
  round 26 (the leg-9 spec insertion shifted everything below ~:1150 by +62; verified: at `a08e85c` the
  ranges land on the comparison loop and the specs/receipt-header instead).
- **`:1159-1160`: exact at round 18** — `58e5d53:1159-1160` is exactly the `REGRESSION_PIN … source=git
  repo=… rev=… path=… mode=… sha256=…` printf. Stale since round 26 (print moved to ~:1228), never
  refreshed; still stale at BASE (:1230-1233) and at CAND (:1302-1305).
- **Anchors `:603-629`, `:1384-1428`, `:1384-1450`: exact at round 26** (`a08e85c`: :603 = PIN_JS … :629 =
  TABLE_CITECHECK; :1384-1428 = the nine dispatches exactly; :1384-1450 = dispatches + tally + FAIL/SETUP).
  `:603-629` lost its last two tables at round 30 (r30's +2 shift pushed TABLE_SOURCESCHECK/TABLE_CITECHECK
  to :630-631 — already 2 tables short at BASE); the :1384-\* ranges still contained their content at BASE
  (the +2 shift was absorbed by the ranges' width); **all broken by r51's insertions** (+7 after :17, +8
  after :144, +9 after :221, +11 after :625, +12 after :634, +72 after :1150, +73 after :1389, +79 in the
  selftest).
- **`:83-108`: held at BASE, holds at CAND** for the inventory core (leg list + sources, now including the
  tenth leg), with the provenance tail now running to :121 past the cited end.
- **`:1104-1175`: comment-level support at BASE/round 26** (the `regression_case` comment sat inside; the
  code never did); at CAND the range lands on spec text.

## 7. reads.json row

```json
{
  "seat": "T51W2Read06",
  "heading": "### Using the ledger",
  "read_rev": "6d8c11e378aa90b12650808e1b79270742935f15",
  "base_rev": "9962033fd7a75aa2f2847e979dd687a5d28505a1",
  "section": {"file": "SKILL.md", "start": 933, "end": 964,
              "sha256": "57ac17ec1a08473f278cff466eb799253adddd8cca8541fdd3cbaa330dc44746",
              "identical_to_base": true},
  "cited_files": ["tools/mutate-and-run.sh"],
  "pointers": [
    {"raw": "tools/mutate-and-run.sh:126-136,1273-1294,1364-1384",
     "file": "tools/mutate-and-run.sh", "ranges": ["126-136", "1273-1294", "1364-1384"],
     "claim": "regression allocates a fresh default scratch after prerequisite checks; removed on PASS unless --keep; retained on FAIL/SETUP; caller workdirs never removed; pre-allocation SETUP has no root; exits 0/1/2 PASS/FAIL/SETUP",
     "verdict": "absent",
     "at_cand": "126-136 = materialization/stated-expectation header comment; 1273-1294 = git-show SETUP refusals + blob-mode mirror in regression_case; 1364-1384 = comparison-loop tail + expectation computation",
     "located": "allocation :1432 after prereqs :1423-1427; removal-on-PASS :1542-1544; kept on FAIL/SETUP :1522,:1528,:1537; caller-workdir guard auto=1 :1542; exits 0/1/2 :1548,:1523,:1529,:1538; exit-map comment :139-143; scratch-root comment :149-151",
     "excerpt": "root=$(mktemp -d \"${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX\") || die_setup 'mktemp -d failed'  (cand :1432)",
     "falsifier": "literal /tmp/tameshi-r4-2-regression.XXXXXX false at CAND (template honours TMPDIR; executed probe: workdir under seat TMPDIR); already stale at BASE (stale since round 26)"},
    {"raw": "tools/mutate-and-run.sh:1104-1175",
     "file": "tools/mutate-and-run.sh", "ranges": ["1104-1175"],
     "claim": "git show <rev>:<path> materializes the pinned blob into the case workdir and validates mode/SHA",
     "verdict": "absent",
     "at_cand": "1104-1154 = js-cite-check spec tail; 1155-1175 = new bash-drift-pins spec header + first defects",
     "located": "regression_case comment :1222-1238; git show :1276; mode read+mirror :1285-1300; sha validation :1307-1317",
     "excerpt": "if ! git_clean -C \"$repo\" show \"${rev}:${path}\" >\"$dst\" 2>\"$cwd/git-show.err\"; then  (cand :1276)",
     "falsifier": "none — behavior true at CAND; pointer moved +~118 lines; 'validates mode' overstates (mode mirrored, not compared)"},
    {"raw": ":1159-1160",
     "file": "tools/mutate-and-run.sh", "ranges": ["1159-1160"],
     "claim": "REGRESSION_PIN names repo/rev/path/pin",
     "verdict": "absent",
     "at_cand": "1159 = drift-pins spec header 'Predictions were fixed before any mutant run…'; 1160 = 'Matrix axes: mode compare, symbol GONE arm…'",
     "located": "printf 'REGRESSION_PIN %s: source=git repo=%s rev=%s path=%s mode=%s sha256=%s\\n' … :1302-1303 (file variant :1305)",
     "excerpt": "printf 'REGRESSION_PIN %s: source=git repo=%s rev=%s path=%s mode=%s sha256=%s\\n' \\  (cand :1302)",
     "falsifier": "already stale at BASE (print at :1230-1233); last correct at round 18 (58e5d53:1159-1160 is exactly this printf); pre-existing defect, not caused by r51"},
    {"raw": ":1384-1450 since round 26",
     "file": "tools/mutate-and-run.sh", "ranges": ["1384-1450"],
     "claim": "a missing repo/rev/blob or pin mismatch refuses before that leg's suite; later legs still run and their statuses aggregate",
     "verdict": "absent",
     "at_cand": "1384-1402 = band-check/verdict prints ending regression_case; 1404-1415 = regression_case_git; 1417-1450 = run_regression entry (refusals, prereqs, mktemp, receipt header)",
     "located": "refusals before suite :1252-1266,:1267-1270,:1271-1274,:1276-1280,:1285-1294,:1307-1317; suite invoked :1320-1322; ten sequential dispatches :1459-1508 (statuses captured, no early exit); aggregation :1510-1517,:1519-1548",
     "excerpt": "tsha=$(sha_of \"$target\"); if [[ \"$tsha\" != \"$pin\" ]]; then … return 2  (cand :1312-1317, before the suite at :1320)",
     "falsifier": "none — behavior true at CAND; at BASE the range still covered dispatches+tally+FAIL/SETUP (aggregation half); refusal half was never inside the range; broken by r51's +72-line insertion"},
    {"raw": "tools/mutate-and-run.sh:603-629",
     "file": "tools/mutate-and-run.sh", "ranges": ["603-629"],
     "claim": "anchor (round 26): pins/revisions/tables",
     "verdict": "absent",
     "at_cand": "603-613 = knowledge-note comment tail; 614-629 = PIN_JS..REV_SOURCESCHECK (no TABLE_* lines)",
     "located": "pins/revisions :614-633; tables :634-643 (TABLE_DRIFTPINS :643)",
     "excerpt": "TABLE_DRIFTPINS='K_MODE_CMP:KILLED,K_GONE_ARM:SURVIVED,K_AMBIG_GT:SURVIVED,K_COUNT_GE:KILLED,K_SHAPE_OPTIN:SURVIVED,S_SHA_CMP:SURVIVED,S_HARDLINK:SURVIVED,S_POLICY:SURVIVED,S_DUP_UNIQ:SURVIVED,S_USAGE_EXIT:SURVIVED'  (cand :643)",
     "falsifier": "at BASE the anchor already missed TABLE_SOURCESCHECK/TABLE_CITECHECK (:630-631, r30 +2 shift); exact at round 26; moved by r51"},
    {"raw": ":657-839",
     "file": "tools/mutate-and-run.sh", "ranges": ["657-839"],
     "claim": "anchor (round 26): first-four specs",
     "verdict": "absent",
     "at_cand": "646-668 = table_lookup/table_count; 669-671 = regression_specs head; 673-839 = first three specs",
     "located": "regression_specs :671; spec writes :673,:714,:759,:804 (four specs span :673-852)",
     "excerpt": "regression_specs() { # <dir> — write the ten embedded case specs  (cand :671)",
     "falsifier": "none — content moved +12 lines; 'first-four' composition itself unchanged"},
    {"raw": ":83-108",
     "file": "tools/mutate-and-run.sh", "ranges": ["83-108"],
     "claim": "anchor (round 26): inventory",
     "verdict": "holds",
     "at_cand": "84 = --regression header; 88-97 = leg inventory incl. 'bash-drift-pins  kagi-shokunin/corpus/drift-pins.sh  2/10 (20 %)' :97; 98-104 = sources incl. '.ufo/evidence/round-51/c2/bash-drift-pins.defects.spec (leg 10)' :104",
     "located": "inventory core inside the cited range; provenance notes now extend to :121 (leg-10 note :111-113, 'All ten defect specs…' :114-121) past the cited end",
     "excerpt": "#   bash-drift-pins       kagi-shokunin/corpus/drift-pins.sh          2/10 (20 %)  (cand :97)",
     "falsifier": "none — the inventory the anchor names is present at CAND; tail truncated"},
    {"raw": ":1384-1428",
     "file": "tools/mutate-and-run.sh", "ranges": ["1384-1428"],
     "claim": "anchor (round 26): nine dispatches",
     "verdict": "absent",
     "at_cand": "same region as the :1384-1450 pointer (verdict prints, regression_case_git, run_regression entry)",
     "located": "the TEN dispatches :1459-1508 (tenth bash-drift-pins :1504-1508)",
     "excerpt": "regression_case_git bash-drift-pins \\  (cand :1504)",
     "falsifier": "text stale too: 'nine dispatches' — there are ten at CAND"}
  ],
  "text_findings": [
    "T1 falsified+executed: literal /tmp/tameshi-r4-2-regression.XXXXXX -> ${TMPDIR:-/tmp}/… at CAND (:1432, header :149-151 'r51 honours TMPDIR'); run-mode :491 and selftest :1555 likewise",
    "T2 stale: receipt-count history stops at '9 since round 26'; CAND receipts print cases=10 (:1540, selftest asserts :2087)",
    "T3 stale: 'nine dispatches' -> ten (:1504-1508)",
    "T4 pre-existing since round 26: bullet 1's three ranges and :1159-1160 already stale at BASE (round-26 SKILL edit refreshed anchors but not these)",
    "T5 minor: 'validates mode/SHA' — sha validated :1312-1317; mode read+mirrored :1285-1300, never compared to a recorded mode",
    "T6 weak anchor: 'enumerated, executed and skipped counts distinguished' — no skip concept in the runner (grep: only embedded spec text); convention lives in uncited knowledge-note manifests"
  ],
  "strongest_falsifier": "the runner TMPDIR change: the section's literal default scratch /tmp/tameshi-r4-2-regression.XXXXXX is false at CAND — executed run-mode probe printed MUTATE_EVIDENCE under the seat's TMPDIR (…/tmp2/tameshi-r4-2-run.qX27Rx), and the regression template at :1432 is ${TMPDIR:-/tmp}/…; second falsifier: the tenth leg makes receipts print cases=10 while the section's history stops at 9",
  "executed": [
    "runner --selftest at CAND in a --shared scratch clone (toplevel asserted), TMPDIR set: exit 0, MUTATE_SELFTEST: 107/107 pass, VERDICT: PASS; tenth leg exercised (leg tuples=10 :2045/:2047, tally asserts cases=10 :2087)",
    "run-mode TMPDIR probe at CAND: MUTATE_EVIDENCE under $TMPDIR, exit 0",
    "sha chain: base runner a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9 == round-21 ledger input pin; cand runner 977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda; section sha 57ac17ec… unchanged"
  ],
  "holds_summary": "every behavioral claim of the section verified true at CAND except the literal /tmp template (T1), the receipt-count history (T2) and 'nine dispatches' (T3); 9 of 10 pointer ranges absent/moved at CAND, 1 holds with truncated tail; 4 ranges were already stale at BASE (pre-existing, since round 26)"
}
```

## 8. Bounds

- Reads: `git show <rev>:<path>` / `git log -L` / `git log --format` on the lane repo only; no lane, fleet or
  sibling writes; no git/jj mutations anywhere.
- Executions: one `--shared` clone in the seat scratch with `rev-parse --show-toplevel` asserted before use;
  the runner's hermetic `--selftest` and one run-mode probe, both writing only under the seat's explicit
  TMPDIR; no fixture commits; nothing executed against the live lane.
- No tools installed (none needed). Scratch `/fast/scratch/hyaku/tameshi-r51/T51W2Read06/` and the two <1 KB
  `/tmp` extracts deleted before yield.
