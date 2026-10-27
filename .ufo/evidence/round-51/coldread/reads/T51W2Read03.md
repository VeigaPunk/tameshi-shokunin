# T51W2Read03 — cold read: `### The protocol — ordered, fail-closed` (SKILL.md:827–857) at candidate 6d8c11e

Seat T51W2Read03, round 51 wave 2 (falsify), lane `tameshi-shokunin`.
Candidate `6d8c11e378aa90b12650808e1b79270742935f15` (commit 2026-10-26 22:32:17 -0300, "round-51: integrate frontier/S022 correction, sourced tenth case, registry rows, runner panel and controls"); base `9962033fd7a75aa2f2847e979dd687a5d28505a1`.

Method: every read against **candidate bytes** pulled with `git -C <lane> show <rev>:<path>` into scratch
(`/fast/scratch/hyaku/tameshi-r51/T51W2Read03/`, TMPDIR-scoped, deleted before yield). The runner was also read
at base and at the pinned revision `b58b26fb`; the round-27 Read08 record was read as provenance. No writes
outside my report file and scratch; no git/jj mutations anywhere.

## Heading resolution (re-resolved, not trusted from the fixture list)

- Exact bytes `### The protocol — ordered, fail-closed` (em dash U+2014) at **SKILL.md:827**; next `#` heading
  `### The boundaries — what a service run is not` at **SKILL.md:858**. Section = **827–857** (31 lines). Matches
  the seat spec ("starts at line 827").
- SKILL.md at candidate is 2171 lines; a full base→candidate diff shows **35 changed lines, all ≥ 2134** (the
  appended `#### Gate/probe registry — round 51` block). This section's bytes are **identical to base** — its
  cold-read risk is purely the input-drift kind (its cited runner changed), which is what this row re-binds.

## Pointer-by-pointer verification (the reads.json row body)

Every pointer the section cites, checked against candidate bytes. Runner line numbers refer to the candidate
blob `tools/mutate-and-run.sh` (2159 lines, sha256 `977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda`).

| # | Raw text in section (loc) | File / ranges | Verdict | Located evidence |
|---|---|---|---|---|
| P1 | "the pinned harness \`tools/mutate-and-run.sh\`" (829) | tools/mutate-and-run.sh | **holds** | exists at candidate, unique at lane root (`.ufo/waves/round-1{7,8}/staged/tools/` copies are not this path); 2159 lines |
| P2 | "the mado run used revision \`597e1419…ff6331b\`, 1001 lines, commit \`b58b26fb\`" (830) | tools/mutate-and-run.sh @ b58b26fb | **holds** | `git show b58b26fb:tools/mutate-and-run.sh` = 1001 lines, sha256 `597e141989065e038a1c2b35359ab3d20b565d3c959c2eec64166ecb1ff6331b`; commit resolves to `b58b26fbeba8fd972e1d31ac8a9175a81e333b32`; corroborated by the note itself (`mutation-case-mado-verify.md:17-22`, I1: sweep+regression pinned that sha in `MUTATE_TOOL`/`REGRESSION_TOOL`) |
| P3 | "this path now holds a later revision" (830) | tools/mutate-and-run.sh | **holds** | candidate blob `977de470…` (2159 L) ≠ `597e1419…` (1001 L) |
| P4 | "so pin by \`git show b58b26fb:tools/mutate-and-run.sh\`" (830–831) | command pointer | **holds** | executed against the lane repo: resolves, prints the 1001-line blob |
| P5 | "every run log carries its own \`MUTATE_TOOL\` pin" (831) | tools/mutate-and-run.sh:506 | **holds**, imprecise (standing) | `printf 'MUTATE_TOOL: %s sha256=%s\n' "$SELF" "$(sha_of "$SELF")"` prints once per run **on stdout**; per-defect logs `evidence/<id>.out`/`evidence/control.out` hold suite output only (round-27 Read08 minor gap, never reworded) |
| P6 | "corrected in round 27, seat Read08" (831) | .ufo/waves/round-27/w1/Read08.md | **holds** | Read08 verdict "wrong-expectation" is exactly the pin/revision issue (path held a later revision than the named `597e1419` bytes); the current text's pin-by clause **is** that correction |
| P7 | code block (833–836): `--target/--defects/--suite 'bash "$MUTANT" --selftest'/--workdir` | tools/mutate-and-run.sh:2139–2142, :56, :213, :464–465 | **holds** | all four flags parsed (:2139–2142); suite runs as `bash -c CMD` with `MUTANT` exported (:464–465); missing-flag refusals :477–479 |
| P8 | step 1: "copied to a pinned pristine; every mutant is a fresh byte copy" (838–839) | :499–504, :523–525 | **holds** | `cp -p` target → `$WORKDIR/pristine.<basename>`, sha pinned + read-race check (:499–504); `cp -p` pristine → `mutant-<id>.<basename>` (:523–525); apply edits the mutant only |
| P9 | step 1 clause: "the original is never a write target unless \`--workdir\` is its own directory (keep scratch apart)" (839) | :490–494, :500, :518, :519, :524, :548 | **FALSIFIED** (standing; see F1) | fixed-name outputs `$WORKDIR/results.tsv` (:548), `defects.tsv` (:518), `spec.copy` (:519) plus prefixed `pristine.`/`mutant-<id>.` names (:500, :524) are written into `--workdir` with **no guard** refusing workdir = target dir (:490–494 just `mkdir -p`); a target named `results.tsv` inside `--workdir` is overwritten by the sweep itself |
| P10 | step 2: "@old exactly once (non-overlapping), asserted before any suite run; @new == @old refused" (840–841) | :411–412, :432, :510–513, :526–534 | **holds** | `@new==@old` refused at parse (:411–412); `count = data.count(old)` is non-overlapping (:432); per-defect count==1 asserted via `apply` during mutant build, then `die_setup "spec/preparation failed for N defect(s); no suite run"` **before** the control run (:526–534) |
| P11 | step 2: "Any spec failure is \`MUTATE: SETUP (<reason>)\`, exit 2 — no headline" (841–842) | :253–256, :506–508, :1677–1680 | **holds** | `die_setup` prints `MUTATE: SETUP (<reason>)` to stderr, exit 2 (:253–256); selftest asserts no `CONTROL:`/`DEFECT` lines on refusal (:1677–1680); provenance lines `MUTATE_TOOL/DATE/TARGET` do print before a parse SETUP (:506–508) — "no headline" (no `MUTATE: DONE`) holds |
| P12 | step 3: "Control first… a red control exits 2" (843–844) | :536–545 | **holds** | control runs on the pristine (:536); red → `CONTROL: RED` + `die_setup "control run on the pristine copy is red (exit=N); cannot attribute kills"` (:539–542) |
| P13 | step 4: "KILLED (suite exit ≠ 0) / SURVIVED (exit 0) / INCONCLUSIVE (timeout 124, or 126/127 not runnable)" (845–846) | :554–559 | **holds**, wording overlap standing | case: 0=SURVIVED; 124 note=timeout; 126 note=suite-not-executable; 127 note=suite-not-found; *=KILLED. "KILLED (≠ 0)" is superseded by the INCONCLUSIVE carve-out in the same sentence; Read08's tighter wording ("exit not 0, 124, 126 or 127") was never applied |
| P14 | step 5: "Target sha256 before = after — \`MUTATE_RESTORE: OK\|DRIFT\`" (847–848) | :566–575 | **holds**, incomplete (standing) | the check compares **target and pristine** shas (:566–569); DRIFT → `MUTATE_RESTORE: DRIFT` + `die_setup` exit 2, no headline (:570–572) — the section states neither the pristine half nor the DRIFT consequence (Read08 minor gaps) |
| P15 | step 6: "\`MUTATE: DONE (… killed=… survived=… inconclusive=… kill-rate=…%)\`; exit 0, DEGRADED exit 1 on any inconclusive" (849–850) | :579–587 | **holds** | DEGRADED exit 1 when inconclusive>0 (:580–583); DONE exit 0 (:585–587); kill-rate rounded pct (:579) |
| P16 | step 6 evidence list: pristine, every mutant, \`evidence/<id>.out\`, \`results.tsv\`, \`spec.copy\` (\`MUTATE_EVIDENCE: <dir>\`) (851–852) | :495–496, :500, :518, :519, :524, :536, :548, :552, :563, :576 | **holds**, list incomplete (standing) | `MUTATE_EVIDENCE` prints `$WORKDIR` (:576); all listed artifacts written at the cited lines; the list **omits** `defects.tsv` (:518) and `evidence/control.out` (:495–496, :536) — incomplete, not wrong |
| P17 | "T6-1 wrote its 10 verdict predictions and six survivor classes first, and the prediction held 10/10 (\`mutation-case-mado-verify.md:73, :187-189\`)" (854–856) | corpus/knowledge/mutation-case-mado-verify.md:73, :187–189 | **holds** | file exists at candidate at that path (unique in the candidate tree); :73 = "- O: **pre-registration held 10/10 on verdicts and 4/4 on the named kill mechanisms** (§5 E1)."; :187–189 = E1 "Predicted and measured tables are identical (4/10 killed; same six survivors)… \`probe/../predictions.txt\`, written 17:42Z before the sweep."; 10 verdict rows = D1–D9 + R1 (:80–89); six survivors = D3, D5, D7, D8, D9, R1 (:60, :82–89). Read08 wording note: section says "classes", note says "same six survivors" — wording, not a defect |

## Falsifiers checked (strongest first)

**F1 — the workdir clause (P9) is false at candidate; standing, documented by round-27 Read08, never fixed.**
Claim: "the original is never a write target unless `--workdir` is its own directory". The candidate runner
writes fixed-name outputs into `--workdir` — `$WORKDIR/results.tsv` (:548), `$WORKDIR/defects.tsv` (:518),
`$WORKDIR/spec.copy` (:519) — plus `pristine.<basename>` (:500) and `mutant-<id>.<basename>` (:524), and has
**no guard** refusing `--workdir` == the target's directory (:490–494 only `mkdir -p`). So a target named
`results.tsv` (or `defects.tsv`/`spec.copy`) placed inside `--workdir` **is overwritten by the sweep itself**;
the restore check then reports `MUTATE_RESTORE: DRIFT` and exits 2, with no restore of the target. This is not
hypothetical: round-27 seat Read08 measured it (Read08-15: target sha `2c2913b…`→`66bf2e8f…`, DRIFT, exit 2)
and rewording was recommended ("the target is overwritten when a harness output name matches it inside
--workdir"). The named condition ("--workdir is its own directory") is neither necessary (Read08-12: workdir =
target dir with no name clash leaves the target byte-identical) nor correctly stated — the real condition is a
harness output name colliding with the target inside `--workdir`. Checked at candidate bytes: the write sites
(:500, :518, :519, :524, :548) and the workdir handling (:490–494) are byte-identical to base (the base→cand
runner diff touches none of them), so the falsifier carries over unchanged. **Not made false by the r51
changes — it was already false.**

**F2 — KILLED wording overlap (P13), standing minor.** "KILLED (suite exit ≠ 0)" overlaps the INCONCLUSIVE
classes; the runner's case statement gives 124/126/127 INCONCLUSIVE precedence (:554–559). Recoverable because
the carve-out is in the same sentence; Read08's suggested tightening was never applied.

**F3 — step 5 incompleteness (P14), standing minor.** The section omits that the restore check also covers the
pristine copy (:566–569) and that DRIFT ends in `MUTATE: SETUP` + exit 2 with no headline (:570–572).

**F4 — "every run log carries its own MUTATE_TOOL pin" (P5), standing minor.** The pin prints on the run's
stdout (:506); the per-defect logs hold suite output only. True of the run's stdout transcript, false if "run
log" is read as every `evidence/*.out`.

**F5 — evidence-list incompleteness (P16), standing minor.** `defects.tsv` (:518) and `evidence/control.out`
(:495–496, :536) are kept but not listed.

**F6 — r51 runner TMPDIR change: checked, no falsity.** The change replaces three `mktemp -d /tmp/…` defaults
with `"${TMPDIR:-/tmp}/…"` (run :491, regression scratch root, selftest root) plus header/usage comments
("(r51 honours TMPDIR)"). The section's "All writes in scratch" (829) still holds: every harness write is under
`WORKDIR` (default under `TMPDIR`), and the section's own code block passes `--workdir <scratch>` explicitly.
No section statement contradicted.

**F7 — tenth leg: checked, no falsity.** The section makes no leg-count or ledger statement; the tenth leg
(`bash-drift-pins`, `TABLE_DRIFTPINS` 2/10) lives in the runner header/ledger and the round-51 registry
section, not here. No statement falsified.

**F8 — four panel-tool updates: checked, no falsity.** `tally-audit.py`, `tally-audit-v2.py`,
`tally-audit-v3.py`, `mte-interop.py` are not cited anywhere in 827–857. No statement falsified.

**F9 — unsupported-premise sweep: none beyond F1–F5.** Every other premise is grounded in candidate bytes:
the pin-by command works (P4); all `MUTATE_*` markers exist (P5, P11, P14–P16); the flag set parses (P7); the
order of operations matches the runner header's "(1)…(7)" (:65–70); "All writes in scratch" holds for the
harness's own writes (the suite command runs from the caller's CWD by contract, :55–56 — the suite's own
writes are the suite's, outside the harness's write set).

## r51-change impact summary (what the tenth leg / TMPDIR change / panel-tool updates did to this section)

- Section bytes: identical to base; no self-drift. The section loses cold-read credit only via
  `input-drift:tools/mutate-and-run.sh` (its cited runner changed sha), which this row re-binds.
- Runner bytes: 2080 → 2159 lines; changes confined to header/usage comments (tenth leg, TMPDIR), three
  `mktemp` defaults, the embedded leg-10 spec + `TABLE_DRIFTPINS` + `regression_case_git bash-drift-pins` call
  + `nlegs=10`, and the selftest leg-count agreement (9→10). **None of the lines the section's step claims rest
  on (:253–256, :411–412, :477–479, :490–508, :510–545, :548–563, :566–587, :2139–2145) changed.**
- Verdict: the section **holds** at candidate except the one standing falsified clause (F1) and four standing
  minor imprecisions (F2–F5) — all already on record from round-27 seat Read08, none introduced or worsened by
  the r51 changes. No stale or moved pointers: every cited file/range resolves at candidate.

## reads.json row

```json
{
  "seat": "T51W2Read03",
  "heading": "### The protocol — ordered, fail-closed",
  "cand": "6d8c11e378aa90b12650808e1b79270742935f15",
  "base": "9962033fd7a75aa2f2847e979dd687a5d28505a1",
  "section": {"file": "SKILL.md", "start": 827, "end": 857,
              "next_heading": "### The boundaries — what a service run is not (SKILL.md:858)"},
  "section_bytes_vs_base": "identical (base→cand diff touches only lines >= 2134)",
  "verdict": "holds-with-one-standing-falsified-clause",
  "pointers": [
    {"raw": "the pinned harness `tools/mutate-and-run.sh`", "loc": "SKILL.md:829",
     "file": "tools/mutate-and-run.sh", "ranges": [], "verdict": "holds",
     "excerpt": "candidate blob 2159 lines sha256 977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda; unique at lane root"},
    {"raw": "the mado run used revision `597e1419…ff6331b`, 1001 lines, commit `b58b26fb`", "loc": "SKILL.md:830",
     "file": "tools/mutate-and-run.sh @ b58b26fb", "ranges": [], "verdict": "holds",
     "excerpt": "git show b58b26fb:tools/mutate-and-run.sh = 1001 lines, sha256 597e141989065e038a1c2b35359ab3d20b565d3c959c2eec64166ecb1ff6331b; commit b58b26fbeba8fd972e1d31ac8a9175a81e333b32; corroborated by mutation-case-mado-verify.md:17-22 (MUTATE_TOOL/REGRESSION_TOOL pins)"},
    {"raw": "this path now holds a later revision, so pin by `git show b58b26fb:tools/mutate-and-run.sh`",
     "loc": "SKILL.md:830-831", "file": "tools/mutate-and-run.sh", "ranges": [], "verdict": "holds",
     "excerpt": "candidate blob 977de470… != 597e1419…; the pin-by command resolves at the lane repo"},
    {"raw": "every run log carries its own `MUTATE_TOOL` pin", "loc": "SKILL.md:831",
     "file": "tools/mutate-and-run.sh", "ranges": ["506"], "verdict": "holds (imprecise: stdout, not per-defect logs; standing since round 27)",
     "excerpt": "printf 'MUTATE_TOOL: %s sha256=%s' \"$SELF\" \"$(sha_of \"$SELF\")\" (:506); evidence/<id>.out hold suite output only"},
    {"raw": "corrected in round 27, seat Read08", "loc": "SKILL.md:831",
     "file": ".ufo/waves/round-27/w1/Read08.md", "ranges": ["1-53"], "verdict": "holds",
     "excerpt": "Read08 verdict wrong-expectation = the pin/revision issue; the current pin-by clause is that correction"},
    {"raw": "bash tools/mutate-and-run.sh --target <gate> --defects <spec> --suite 'bash \"$MUTANT\" --selftest' --workdir <scratch>",
     "loc": "SKILL.md:833-836", "file": "tools/mutate-and-run.sh", "ranges": ["2139-2142", "56", "213", "464-465"],
     "verdict": "holds",
     "excerpt": "all four flags parsed (:2139-2142); suite runs as bash -c CMD with MUTANT exported (:464-465)"},
    {"raw": "The target is copied to a pinned pristine; every mutant is a fresh byte copy", "loc": "SKILL.md:838-839",
     "file": "tools/mutate-and-run.sh", "ranges": ["499-504", "523-525"], "verdict": "holds",
     "excerpt": "cp -p target -> $WORKDIR/pristine.<basename> with sha pin + read-race check (:499-504); cp -p pristine -> mutant-<id>.<basename> (:523-525)"},
    {"raw": "the original is never a write target unless `--workdir` is its own directory (keep scratch apart)",
     "loc": "SKILL.md:839", "file": "tools/mutate-and-run.sh", "ranges": ["490-494", "500", "518", "519", "524", "548"],
     "verdict": "FALSIFIED (standing; documented round-27 Read08, never fixed; not caused by r51 changes)",
     "excerpt": "fixed-name outputs $WORKDIR/results.tsv (:548), defects.tsv (:518), spec.copy (:519) and prefixed pristine./mutant- names (:500, :524) written into --workdir with no guard refusing workdir == target dir (:490-494); a target named results.tsv inside --workdir is overwritten (Read08-15: sha changed, MUTATE_RESTORE: DRIFT, exit 2, no restore)"},
    {"raw": "Every `@old` must occur exactly once (non-overlapping count), asserted **before any suite run**; `@new == @old` is refused",
     "loc": "SKILL.md:840-841", "file": "tools/mutate-and-run.sh", "ranges": ["411-412", "432", "510-513", "526-534"],
     "verdict": "holds",
     "excerpt": "@new==@old refused at parse (:411-412); count=data.count(old) non-overlapping (:432); die_setup 'spec/preparation failed for N defect(s); no suite run' before the control run (:526-534)"},
    {"raw": "Any spec failure is `MUTATE: SETUP (<reason>)`, exit 2 — no headline", "loc": "SKILL.md:841-842",
     "file": "tools/mutate-and-run.sh", "ranges": ["253-256", "506-508", "1677-1680"], "verdict": "holds",
     "excerpt": "die_setup prints MUTATE: SETUP (<reason>) to stderr, exit 2 (:253-256); selftest asserts no CONTROL/DEFECT lines on refusal (:1677-1680); provenance lines do print before a parse SETUP (:506-508)"},
    {"raw": "Control first. The unmutated copy must run green; a red control exits 2 (kills could not be attributed)",
     "loc": "SKILL.md:843-844", "file": "tools/mutate-and-run.sh", "ranges": ["536-545"], "verdict": "holds",
     "excerpt": "run_one on the pristine (:536); red -> CONTROL: RED + die_setup 'control run on the pristine copy is red (exit=N); cannot attribute kills' (:539-542)"},
    {"raw": "KILLED (suite exit ≠ 0) / SURVIVED (exit 0) / INCONCLUSIVE (timeout 124, or 126/127 not runnable)",
     "loc": "SKILL.md:845-846", "file": "tools/mutate-and-run.sh", "ranges": ["554-559"],
     "verdict": "holds (wording overlap standing; Read08 suggested 'exit not 0, 124, 126 or 127')",
     "excerpt": "case: 0=SURVIVED; 124 note=timeout; 126 note=suite-not-executable; 127 note=suite-not-found; *=KILLED (:554-559)"},
    {"raw": "Target sha256 before = after — `MUTATE_RESTORE: OK|DRIFT`", "loc": "SKILL.md:847-848",
     "file": "tools/mutate-and-run.sh", "ranges": ["566-575"],
     "verdict": "holds (incomplete: pristine sha also compared; DRIFT -> SETUP exit 2 unstated; standing)",
     "excerpt": "checks target AND pristine (:566-569); DRIFT -> MUTATE_RESTORE: DRIFT + die_setup exit 2, no headline (:570-572); OK line (:574-575)"},
    {"raw": "`MUTATE: DONE (… killed=… survived=… inconclusive=… kill-rate=…%)`; exit 0, DEGRADED exit 1 on any inconclusive",
     "loc": "SKILL.md:849-850", "file": "tools/mutate-and-run.sh", "ranges": ["579-587"], "verdict": "holds",
     "excerpt": "DEGRADED exit 1 when inconclusive>0 (:580-583); DONE exit 0 (:585-587)"},
    {"raw": "The evidence dir keeps pristine, every mutant, `evidence/<id>.out`, `results.tsv`, `spec.copy` (`MUTATE_EVIDENCE: <dir>`)",
     "loc": "SKILL.md:851-852", "file": "tools/mutate-and-run.sh",
     "ranges": ["495-496", "500", "518", "519", "524", "536", "548", "552", "563", "576"],
     "verdict": "holds (list incomplete: omits defects.tsv and evidence/control.out; standing)",
     "excerpt": "MUTATE_EVIDENCE prints $WORKDIR (:576); all listed artifacts written at the cited lines"},
    {"raw": "T6-1 wrote its 10 verdict predictions and six survivor classes first, and the prediction held 10/10 (`mutation-case-mado-verify.md:73, :187-189`)",
     "loc": "SKILL.md:854-856", "file": "corpus/knowledge/mutation-case-mado-verify.md", "ranges": ["73", "187-189"],
     "verdict": "holds",
     "excerpt": ":73 'pre-registration held 10/10 on verdicts and 4/4 on the named kill mechanisms'; :187-189 E1 'Predicted and measured tables are identical (4/10 killed; same six survivors)… predictions.txt, written 17:42Z before the sweep'; 10 rows D1-D9,R1 (:80-89); six survivors D3,D5,D7,D8,D9,R1 (:60)"}
  ],
  "falsifier_checked": "F1 (strongest): the workdir clause 'the original is never a write target unless --workdir is its own directory' is false at candidate — the runner writes fixed-name outputs (results.tsv :548, defects.tsv :518, spec.copy :519) into --workdir with no guard refusing workdir == target dir (:490-494); a target named results.tsv inside --workdir is overwritten (round-27 Read08-15 measured: sha changed, MUTATE_RESTORE: DRIFT, exit 2, no restore). Write sites byte-identical base->cand, so the falsifier carries over. Also checked and cleared: KILLED/INCONCLUSIVE wording overlap (standing minor), step-5 pristine/DRIFT omissions (standing minor), MUTATE_TOOL stdout imprecision (standing minor), evidence-list omissions (standing minor), r51 TMPDIR change (no falsity), tenth leg (no falsity), four panel-tool updates (not cited here, no falsity).",
  "r51_impact": "section bytes identical to base; runner changes (tenth leg + TMPDIR defaults + leg-count selftest) touch none of the lines the step claims rest on; no stale or moved pointers"
}
```

## Re-key relevance

This section is one of the cold-read sections whose ledger entry pins the runner's sha
(`input-drift:tools/mutate-and-run.sh`): the r51 runner edit changed that sha, so the section loses credit at
CAND until the round-49-style trace-bound re-key runs. This row re-read the section and every cited
non-record surface at candidate bytes (runner at candidate; pinned blob at `b58b26fb`; mado note at candidate;
Read08 record as provenance), so the re-key can bind the section's pointers to the new runner bytes with a
real read behind them. The one falsified clause (F1) is pre-existing (round-27 record), disclosed here — not a
new r51 harm and not a reason to withhold the re-key.
