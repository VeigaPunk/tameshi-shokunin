# T53W2Read12 — wave-2 re-read of `### Round-15 gate/probe registry`

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Read revision: `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e` (C**, fix pass 2), git objects only (`git -C <lane> show C**:SKILL.md`). The working tree was never read.
- Wave-1 content revision for comparison: `a41195dfc13a73958e4c5228ec196b28d03ded03` (C*).
- Section at C**: lines **1694–1723**, heading line `:1694`, 30 lines. Frozen-monitor `sectionize` (`.ufo/evidence/round-18/measure.py`, imported at C**, not reimplemented) reports `start=1694 end=1724`.
- `section_sha256` = `da6ef23c23f06af0c420a87476364031b107f82cf16260900040a6cb3fdac516`.
- Split verified before hashing, two independent ways: (1) the frozen `sectionize` imported from the blob at C**, whose returned `sha256` recalculated from its own start/end range matches; (2) a separate line-based re-derivation under the seat's stated rule (`^#{1,3}(\s|$)` outside ``` fences, heading line through the line before the next heading, trailing whitespace-only lines stripped, `\n` join, no trailing newline, UTF-8 surrogateescape) that prints `start/end: 1694 1724 lines: 30 sha256: da6ef23c…`. The single heading match is `:1694`; the next heading is `## Errata — round 16 full-page cold-read` at `:1725`.
- Verdict: **both wave-1 fixes are present in the C** bytes and both hold; no new finding.**

## Fix verification (run first)

The whole-section diff C* → C** is exactly the two named repairs and nothing else; the section keeps 30 lines at both revisions (only line content changed):

```
@@ -14 +14 @@
-rank, SHONEN authority, the six recorded cases, or the archived round-12–14
+rank, SHONEN authority, the six recorded cases at this write (seven since round 16), or the archived round-12–14
@@ -16 +16 @@
-successor sweep or seventh case is claimed.
+successor sweep beyond the recorded cases is claimed.
```

Source of the diff: frozen `sectionize` at both revisions (`C*`: start/end `1683`/`1713`, sha `b814e0af…`; `C**`: start/end `1694`/`1724`, sha `da6ef23c…`; end-exclusive, so 30 body lines each), then `difflib.unified_diff` on the two section bodies.

### Fix 1 — wave-1 F1 (`the six recorded cases` stale count): PRESENT, DATED, AND TRUE

- Verbatim at C** (section line 14, file line 1707): `the six recorded cases at this write (seven since round 16)`
- The count is correct for the write being dated: the page records `## Third case — cross-author confirmation (round 5, measured)` (`:671`) and `### Six-case confidence statement (round 8, measured)` (`:1098`), and the seventh case only from `## Seventh recorded case and full-page cold-read — round 16` (`:1772`). Six at the round-15 write is therefore right, and the parenthetical dates the onset of seven.
- The added form matches the page's own convention for a dated milestone rather than a current count: `:1751` `dated: four at r7-1, seven since round 16`, `:1758` `six at round 11, seven since round 16`, and the sibling sentence `:1573` `a seventh case is recorded since round 16, …`. A cold reader can no longer take six as the current set size, which was the wave-1 finding's exact complaint; the later progression to nine/ten remains stated where it belongs (`:1400`, `:1407`).

### Fix 2 — wave-1 F2 (`successor sweep or seventh case` negation): PRESENT AND NARROWED

- Verbatim at C** (section line 16, file line 1709): `successor sweep beyond the recorded cases is claimed.`
- The negation no longer denies a seventh case; it now denies only a sweep *beyond* the recorded cases, which is what the sentence can support. Checked for a contradicting claim at C**: `successor sweep` occurs exactly twice in SKILL.md (`:1636` `It adds no successor sweep, seventh recorded case, promotion credit,` and `:1709`), both negations; `grep -n "successor\|next sweep\|eleventh\|new sweep\|future sweep"` returns only history statements (`:793`, `:1434`, `:1462`, `:1471`, `:2063`) and no claim of a new independently measured sweep. The seventh/eighth/ninth/tenth cases are now inside the allowed "recorded cases" set, so the narrowed negation holds where the old one did not.

## Checks executed (command → observed outcome)

All runs in scratch: `git clone --shared` of the lane (verified `git rev-parse --show-toplevel` = `/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read12/clone`), `git archive 28aeef4` extracted to `/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read12/a28`, `TMPDIR` bound to `/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read12/tmp`. No lane write; `git --no-optional-locks status --porcelain` on the clone is empty after every run.

| # | Command | Outcome |
|---|---|---|
| 1 | frozen `sectionize` at C** (imported from `.ufo/evidence/round-18/measure.py`) | one heading match; `start=1694 end=1724`; `sha256=da6ef23c…`; range body re-hash equal |
| 2 | independent line-split per seat rule | `start/end: 1694 1724 lines: 30 sha256: da6ef23c…` — agrees with #1 |
| 3 | `difflib` C* vs C** section bodies | only the two fix lines differ; 30 lines at both |
| 4 | `git show C**:tools/context-capture.py` + `grep` | `FROZEN_RECEIPT_SHA256` literal `05cb55b8…` (`:153`), `FROZEN_EXPECTED_ID = "context_consistent"`, `FROZEN_EXPECTED_EXIT = 0` (`:158-159`), `EXPECTED_SCHEMA = "tameshi-context-expected-v1"` (`:141`), ids `missing_injected_environment` exit 1, `snapshot_tampered` exit 2, `usage_error` exit 64 |
| 5 | `git show C**:.ufo/evidence/round-14/context-receipt.json \| sha256sum` | `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a` — equals the row's pin |
| 6 | `git show C**:.ufo/evidence/round-14/context-missing-env.json \| sha256sum` | `1ee9d09bc5277fd17b90c7f21e0ed4126825c97875b32b60dfcc2ca2852aa208` — equals the row's negative-fixture pin |
| 7 | `python3 tools/context-capture.py --check` (clone at C**, TMPDIR bound) | exit **0**, `CONTEXT: OK (id=context_consistent receipt=.ufo/evidence/round-14/context-receipt.json sha256=05cb55b8… exit=0 findings=0)` |
| 8 | `python3 tools/context-capture.py --selftest` | exit **0**, `SELFTEST: PASS (49/49)` |
| 9 | `python3 tools/context-capture.py -h` | exit **0** ("Help exits0 only as a non-verdict informational mode") |
| 10 | `python3 tools/context-capture.py --bogus` | exit **64** (`usage_error`) |
| 11 | `python3 tools/context-capture.py --check --receipt /nope/r.json --expected /nope/e.json --json` | exit **2**, `status=invalid_input id=expected_missing` — missing input is could-not-evaluate, matching the row's "2 and 64 could-not-evaluate (receipt/expected missing, …)" |
| 12 | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json` (clone at C**) | exit **2**, `id=expected_input_digest_mismatch`, first detail `tools/bash-witness-study.py: observed 4e999ff4… expects 49e9e5e2…` — the row's superseded entry command still returns its stated class |
| 13 | pin walk of `.ufo/evidence/round-13/expected.json` `inputs` vs C** blobs | 13 inputs: 10 MATCH, 3 MISMATCH (`tools/pin-disposition.py`, `tools/bash-witness-study.py`, `tools/mutate-and-run.sh`) — the runner input did move, so "because the runner input moved" is true (partial; see Observations) |
| 14 | `python3 tools/evidence-disposition.py --dispositions .ufo/evidence/round-18/dispositions.json --json --root .` | exit **0**, `effective 11 / superseded 1 / failed 0 / findings 0` — "Live entry … → 0" holds |
| 15 | `python3 tools/evidence-disposition.py --dispositions .ufo/evidence/round-17/dispositions.json --json --root .` | exit **2**, `expected_input_digest_mismatch` — "(round 17's now 2)" holds |
| 16 | in extracted `git archive 28aeef4` (`28aeef498cc070c3183271b709bc79d344ff547a`, "round-15 verifier spot-check …"): `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json` | exit **0**, `clean` — the row's "frozen replay: cwd = extracted `git archive 28aeef4` → 0" holds |
| 17 | same tree with `--dispositions .ufo/evidence/round-14/dispositions-before.json` | exit **1**, `failed` — matches the round-14 recipe's before→1 (the replay claim does not conflate the two) |
| 18 | `python3 tools/evidence-disposition.py --selftest` | exit **0**, `SELFTEST: PASS (66/66)` (row's self-test command) |
| 19 | `python3 tools/evidence-disposition.py --root . --dispositions /nope-dir/dispositions.json --json` | exit **2**, `status=could_not_evaluate id=dispositions_missing` |
| 20 | `python3 tools/evidence-disposition.py --bogus` / `--help` | exit **64** / exit **0** |
| 21 | `TMPDIR=<nonexistent> python3 tools/evidence-disposition.py --selftest` | exit **1** with an uncaught `RuntimeError: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory … (could-not-evaluate)` — exactly the section's "the disposition selftest: 0 pass, 1 case failure or an uncaught setup traceback; round 17" |
| 22 | `TMPDIR=<nonexistent> python3 tools/context-capture.py --selftest` | exit **2**, `SELFTEST: FAIL (setup error: RuntimeError: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory …)` — no silent `/tmp` fallback, so "selftest writes isolated temporary fixtures only" holds |
| 23 | `grep -n 'round-17 re-pin\|re-pin section'` + heading census at C** | pointer resolves: `## Live-tree re-pin and entry-command monitor — round 17` (`:1832`), `### Round-17 gate/probe registry — re-pin and monitor` (`:1864`) |
| 24 | `grep -n "Two evidences"` in C** SKILL.md; fleet-root `PROTOCOL.md` (read-only, outside lane) | lane page holds no such section (errata `:1755` says the lane holds no `PROTOCOL.md`); the standard's text is fleet-root `PROTOCOL.md:390` `- **Two evidences.** …` |
| 25 | `grep 'successor sweep'` and successor-sweep census at C** | two hits, both negations (`:1636`, `:1709`); no claimed sweep beyond the recorded cases |
| 26 | `git ls-tree -r --name-only C**` for `.ufo/evidence/round-1{2,3,4}/` | all three round archives present — "the archived round-12–14 bytes" resolves |
| 27 | `git ls-tree` for dispositions manifests at C** | `round-14/dispositions.json`, `round-14/dispositions-before.json`, `round-17/dispositions{,-before}.json`, `round-18/dispositions{,-before}.json` all present |

## Holds (each row checked against C** bytes and command output)

- **Entry command, verdict map, self-test, pins of `retained invocation-context gate`** — checks 4–7, 9–11: bare `--check` is clean at the pinned receipt; the two pinned sha256 values are byte-identical to the committed files; the literal finding ids and exit classes exist in the tool; a wrong/missing input is exit 2, usage exit 64, help exit 0.
- **Entry command, verdict map, self-test, pins of `effective expectation disposition`** — checks 12–19: superseded `--root .` form → 2 `expected_input_digest_mismatch`, live round-18 entry → 0, round-17 manifest → 2, frozen replay → 0, before-manifest replay → 1, selftest → 66/66, usage → 64.
- **`check reads receipt/expected bytes and its own source for a reported digest, writes nothing, never opens recorded root paths or executes stored argv`** — the only `subprocess` use in `tools/context-capture.py` is inside `SelftestHarness` (`:1661`); the only `open(...,"w")` is the harness's fixture writer (`:1699`); check mode left the clone porcelain-clean (check 7 + status).
- **`retained replay is the committed-input evidence of the Gate standard's "Two`** (wrapped across `:1704-1706`) — the standard's clause exists at fleet-root `PROTOCOL.md:390`, and the round-14 receipt it replays is committed and digest-pinned (checks 5, 7, 24).
- **`Could-not-evaluate takes precedence over a mismatched expected verdict`** and **`A clean result with a wrong id/exit pin becomes failed/exit1`** — the tool's id table puts the exit-1 pinned-verdict family (`expected_verdict_mismatch`, `receipt_verdict_mismatch`, `:75-77`) after the could-not-evaluate kinds, and the selftest carries the tampered-before-semantic case (`tampered-before-semantic` → `snapshot_tampered` exit 2).
- **`The maintained gate's expected values are configured authority, not cryptographic proof of author authenticity`** — a scoping statement; nothing in the section claims author authentication, and the receipt pin is digest binding only.
- **`no sibling gate is registered or executed by this lane`** — this registry's two rows are lane-owned (`Owner` column `tameshi`), and the lane's own discipline says the same in `:1562` `Do not rerun a sibling's gate to obtain closure evidence` and `:1609` `A non-author closure reads committed evidence, never executes sibling gates.` Sibling `scripts/*.mjs` appear only as mutation *subjects* recorded as cases (`:1774`, `:1933`), not as rows here; see Observations for the gate-vs-subject reading.
- **Parenthetical `superseded in round 17`** — the supersession is recorded in the round-17 material the row points at (`:1832`, `:1864`), and the live replacement (round-18 manifest) is what check 14 exercised.
- **Write-scope cells** — `selftest writes isolated temporary fixtures only` and `selftest isolated temporary fixtures` hold under a bound `TMPDIR`, and both selftests fail closed on an unusable TMPDIR with no `/tmp` fallback (checks 21–22). No `/tmp` scratch path is named anywhere in the section, so no scratch-directive violation to report.

## Findings

**None.** No statement in the section fails at C**: both wave-1 statements are repaired, and every remaining claim was exercised against the committed bytes (or is a scoping/limit statement with no falsifiable premise).

## Observations (recorded, not filed as findings — deliberately not inflated)

1. `historical expected pins13 original inputs` — the space between `pins` and `13` is missing. The substance is true: `.ufo/evidence/round-13/expected.json` carries exactly 13 `inputs` keys (check 13), and the round-14 recipe at `:1598` states `distinguish twelve expected rows from thirteen pinned inputs`. Cosmetic only; also noted by the wave-1 seat.
2. `because the runner input moved` — true but partial at C**: the run in check 12 reports `tools/bash-witness-study.py` first, and three of the thirteen pins are stale (`tools/pin-disposition.py`, `tools/bash-witness-study.py`, `tools/mutate-and-run.sh`). The runner is one of them, and the page's fuller list at `:1599-1600` names all three — the runner in round 16, the bash witness-study tool in rounds 18 and 21, and `tools/pin-disposition.py` in round 17 — so the clause is not false, only under-specified. Round-18 CR42 filed the same point as a minor gap; it is not a statement that does not hold.
3. `no sibling gate is registered or executed by this lane` read strictly against the mutation cases that run kumitate `scripts/*.mjs`: those are subjects under test (the runner's `js-round-gate` / `js-sources-check` / `js-cite-check` legs), not gates consulted for a verdict, which is the distinction the lane states at `:1562`/`:1609`. Read as written in a gate-registry paragraph, the sentence holds.

## Scratch and provenance

- Scratch root `/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read12/` (clone, C** archive extract, 28aeef4 extract, TMPDIR) was created by this seat and deleted before yield; nothing was written outside the seat's named report paths in the lane.
- No installs or upgrades were needed; no tool/version/channel entry to record.
- No git/jj mutation in the lane; the only repository mutation was `git checkout` inside the seat's own `--shared` clone, after asserting `git rev-parse --show-toplevel` there.
- Deliverables: `.ufo/waves/round-53/w2/T53W2Read12.json`, `.ufo/waves/round-53/w2/T53W2Read12.md`.
