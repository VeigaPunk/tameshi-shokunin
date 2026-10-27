# Sibling-Overlap Scan — Round 52 Wave 1 (Seat T52W1ConnSibling)

## Overview & Scope
Investigation of the fleet (`/home/vgpnk/Projects/shokunin/*-shokunin`) for instances matching or near-missing the round's two defect shapes:
- **Shape 1 (Registered gate row / pinned count drift)**: A registered gate row whose expected output pins a count (`N/N`) that a later tool change moved.
- **Shape 2 (Undeclared fleet-bound self-test)**: A self-test that reads sibling repos through `Path(__file__).parents[k].parent` or `ROOT.parent` without declaring it.

---

## Sibling Fleet Hits (Up to 10)

### Hit 1: `kotodama-shokunin` — `SKILL.md:661` (`same-shape`, Shape 1)
- **Repo & File:Line**: `kotodama-shokunin`, `SKILL.md:661`
- **Commit**: `e06581b7648352cefcb11a5b816ba9a263fa789b` (line author); tool updated in `11df1fd525287e076dd03e0ca3b4eb835158654a`
- **Command**:
  `git -C /home/vgpnk/Projects/shokunin/kotodama-shokunin log -1 --format='%H %ci' -L661,661:SKILL.md`
  and
  `python3 /home/vgpnk/Projects/shokunin/kotodama-shokunin/tools/check-gate-battery.py | grep -C 2 '"coverage":'`
- **Evidence**:
  Row `isolated legacy selftest battery` in `SKILL.md:661` documents: `"duty 1 (selftests): 0 seven selftests pass ... 7/7 selftests, 0 uncovered ... coverage is the registered nine"`. In commit `11df1fd5`, `tools/check-gate-battery.py` added `register-law-gate.py` to `BASELINE_ONLY_GATE_NAMES`, moving coverage from `9/9` to `10/10` (`"coverage": "10/10"`, `"gates_registered": 10`), while `SKILL.md:661` remained un-updated pinning the earlier 9-gate count.

### Hit 2: `kengaku-shokunin` — `SKILL.md:609` (`same-shape`, Shape 1)
- **Repo & File:Line**: `kengaku-shokunin`, `SKILL.md:609`
- **Commit**: `77ea425ac217ebe2290490b2ebb3d0a60202ca9b` (round 43); tool updated in `02287ee429d332616f71d5b32e01df3ae0ad85ec` (round 44)
- **Command**:
  `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin log -1 --format='%H %ci' -L609,609:SKILL.md`
  and
  `python3 /home/vgpnk/Projects/shokunin/kengaku-shokunin/plans/gate_flip_check.py --selftest | tail -1`
- **Evidence**:
  Registered row `gate-flip-check` in `SKILL.md:609` documents: `python3 plans/gate_flip_check.py --selftest (19 built fixtures in a temp dir, each run as a subprocess: 10 red, 8 green, 1 setup; SELFTEST ok=19/19)`. In commit `02287ee`, 8 new test fixtures were added (cases 20–27), changing the tool output to `SELFTEST ok=27/27`. `SKILL.md:609` remained unchanged pinning `19/19`.

### Hit 3: `kake-shokunin` — `SKILL.md:1274` (`same-shape`, Shape 1)
- **Repo & File:Line**: `kake-shokunin`, `SKILL.md:1274`
- **Commit**: `c1e39ef3879f8269784358bb380590a9ab01844b` (round 57); tool updated in `ab6e100e47fe266c14101e4ec91fcbe64811f5fa` (round 58)
- **Command**:
  `sed -n '1274p' /home/vgpnk/Projects/shokunin/kake-shokunin/SKILL.md`
  and
  `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/id_resolver.py --selftest | tail -1`
- **Evidence**:
  Gate row `id-resolver-gate` in `SKILL.md:1274` documents: `python3 -B scripts/id_resolver.py --selftest (49 checks through round 57, 59 from round 58)`. Successive tool expansions added checks for HTML comments, setext headings, and symlinks, moving the tool's actual output to `selftest: 72/72`.

### Hit 4: `chousa-shokunin` — `SKILL.md:130` (`near-miss`, Shape 1)
- **Repo & File:Line**: `chousa-shokunin`, `SKILL.md:130` (superseded by `SKILL.md:136`)
- **Commit**: `871c0d79d6389f417fafe8c34749f7e5270dcb72` (line 130); `32aab5edd70e43145cae72ec872278f3bc6efba7` (line 136)
- **Command**:
  `sed -n '130p;136p' /home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md`
- **Evidence**:
  Row `assimilate-rows` in `SKILL.md:130` recorded `python3 tools/assimilate-rows.py --selftest → SELFTEST=PASS findings=27 expected=27 ... LEGS=5/5`. Tool change `32aab5ed` moved the output to `findings=40 expected=40` and `LEGS=8/8`. `chousa` avoided breaking existing checks by appending a superseding row at `SKILL.md:136` (`assimilate-rows (v4, round 53)`), making this an intentional mitigation pattern rather than an unhandled drift.

### Hit 5: `kama-shokunin` — `tools/round35-statement-audit.py:31,75,157` (`same-shape`, Shape 2)
- **Repo & File:Line**: `kama-shokunin`, `tools/round35-statement-audit.py:31,75,157`
- **Commit**: `8c3b40ee53000b9533ca97ae9792671eb6df7cf5`
- **Command**:
  `git -C /home/vgpnk/Projects/shokunin/kama-shokunin grep -n "FLEET =" tools/round35-statement-audit.py`
  and
  `python3 /home/vgpnk/Projects/shokunin/kama-shokunin/tools/round35-statement-audit.py --repo /home/vgpnk/Projects/shokunin/kama-shokunin --selftest`
- **Evidence**:
  Line 31 sets `FLEET = Path("/home/vgpnk/Projects/shokunin")`. Its `--selftest` branch calls `audit(lane, "")`, which invokes `facts(lane)` executing `git_show(FLEET, REPORT_REV, REPORT_PATH)`. Outside `/home/vgpnk/Projects/shokunin`, the selftest crashes with `RuntimeError: git show failed`, yet the docstring never declares fleet-bound dependency.

### Hit 6: `kama-shokunin` — `tools/round36-statement-audit.py:28,74,235` (`same-shape`, Shape 2)
- **Repo & File:Line**: `kama-shokunin`, `tools/round36-statement-audit.py:28,74,235` (recurs in `round37-statement-audit.py:32,233`)
- **Commit**: `e5a8ececf3d60fd53b36bb74299693a29e8f74b6`
- **Command**:
  `git -C /home/vgpnk/Projects/shokunin/kama-shokunin grep -n "FLEET =" tools/round36-statement-audit.py`
- **Evidence**:
  Line 28 sets `FLEET = Path("/home/vgpnk/Projects/shokunin")`. In `--selftest` (line 235), `load_facts(args.repo, args.tip)` is invoked directly, reading `git_show(FLEET, REPORT_REV, REPORT_PATH)`. In a standalone clone where the fleet root is absent, `--selftest` fails without having declared its fleet dependency.

### Hit 7: `kagi-shokunin` — `corpus/scope-gate.sh:91,342,756` (`same-shape`, Shape 2)
- **Repo & File:Line**: `kagi-shokunin`, `corpus/scope-gate.sh:91,342,756`
- **Commit**: `e64e81b8eb96f3682b00c1e7a291e84420b280fa`
- **Command**:
  `ADJ_LANE_ROOT=/tmp/empty-nonexistent bash /home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/scope-gate.sh --falsify`
- **Evidence**:
  Line 91 sets `LANE_ROOT="${ADJ_LANE_ROOT:-$(cd -- "$SCRIPT_DIR/../.." && pwd)}"`. In `--falsify`, line 756 links `$LANE_ROOT/kotoba-shokunin` and line 342 resolves `lane:<lname>` citations against `$LANE_ROOT/${lname}-shokunin`. In an isolated clone where sibling repos do not sit at `../..`, `--falsify` fails (`SCOPE NOT-A-FILE ...`).

### Hit 8: `kotoba-shokunin` — `verifiers/verify_corpus_independent.py:45,265,938` (`near-miss`, Shape 2)
- **Repo & File:Line**: `kotoba-shokunin`, `verifiers/verify_corpus_independent.py:45,265,938`
- **Commit**: `14774a2cb588d927d3c013b8a1c97a53606f7bb8`
- **Command**:
  `git -C /home/vgpnk/Projects/shokunin/kotoba-shokunin grep -n "FLEET_ROOT =" verifiers/verify_corpus_independent.py`
- **Evidence**:
  Line 45 defines `FLEET_ROOT = "/home/vgpnk/Projects/shokunin"`. In `selftest()` line 938, `analyse_pointers(proot, corpus_markdown(proot))` is called with two arguments, causing the pointer check to default `fleet_root` to the live host fleet root. This is a near-miss: the test passes on the host, but ambiently couples to `/home/vgpnk/Projects/shokunin`.

### Hit 9: `kengaku-shokunin` — `plans/round32_defects.py:44,212-215` (`near-miss`, Shape 2)
- **Repo & File:Line**: `kengaku-shokunin`, `plans/round32_defects.py:44,212-215` (recurs in `plans/round33_defects.py:40,183-185`)
- **Commit**: `45a892b152d0fa5a5fef1096057a6e1338dfba1d`
- **Command**:
  `git -C /home/vgpnk/Projects/shokunin/kengaku-shokunin grep -n "FLEET =" plans/round32_defects.py`
- **Evidence**:
  Module defines `FLEET = Path("/home/vgpnk/Projects/shokunin")` for live inspection. However, `selftest()` lines 212–215 explicitly notes: `# R1/R2 read absolute fleet paths by default... Run them against synthetic fixtures so the selftest stays hermetic`. The test constructs private fixtures in a tempdir, successfully avoiding the Shape 2 defect.

### Hit 10: `tsukuroi-shokunin` — `tools/check-adjacency-overlap.py:48-51,903,929` (`near-miss`, Shape 2)
- **Repo & File:Line**: `tsukuroi-shokunin`, `tools/check-adjacency-overlap.py:48-51,903,929`
- **Commit**: `41b4dca8a6669bc6726204c35694a532385b2e54`
- **Command**:
  `python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-adjacency-overlap.py --selftest`
- **Evidence**:
  Evaluates cross-lane overlap with `mori-shokunin` via `--siblings-root` (defaulting to `/home/vgpnk/Projects/shokunin`). When `mori-shokunin` is absent, it safely falls back to reporting `sibling-unavailable` rather than crashing. In `--selftest`, it constructs its own temporary fixtures and tests both absent and synthetic sibling trees.

---

## Tameshi-Only Scan (C1 Cannot_See Items)

### 1. Shape 1 (Count-pinning Gate Rows)
- **`tools/registry.json:1011` (`mte-interop-check`)** — `same-shape`:
  Expected `legs_conforming=9/9` while `tools/mte-interop.py` grew to 10 legs (`bash-drift-pins`), causing R51.1 failure. Repaired in round 52 to `10/10`.
- **`tools/registry.json:928` (`command-binding-selftest`)** — `same-shape` (precedent):
  Originally pinned `COMMAND_BINDING_SELFTEST: 38/38 pass`. When `tools/command-binding.py` grew to 44 cases, row 928 was marked `status: superseded` by row 961 `command-binding-selftest-r24` (`44/44 pass`).
- **`tools/registry.json:982` (`mutate-and-run-regression`)** — `near-miss` (C1 `cannot_see` risk):
  Invokes `bash tools/mutate-and-run.sh --regression`, but pins `stdout_contains: ["REGRESSION: PASS"]` rather than `cases=10 passed=10`. This prevented breakage when leg 10 was added, but creates an operability blind spot: `registry-check.py` cannot see whether the full intended panel of legs executed.
- **`tools/registry.json:1018` (`evidence-disposition-round18`)** — `near-miss` (fragility):
  Pins exact JSON counts: `'"status": "clean"', '"effective": 11', '"superseded": 1'`.
- **`tools/registry.json:967,975` (`wave-accounting-frozen-entry`, `wave-accounting-wrong-count-entry`)** — `near-miss`:
  Pin exact seat tallies `'"completed": 66', '"dead": 80', '"seats": 146'`.

### 2. Shape 2 (Fleet-Bound Self-Tests & Tools)
- **`tools/round21-measure.py:74`** — `same-shape`:
  At base `ef19d8e1`, line 74 read `ROOT.parent / surface["repo"]` without declaring fleet-bound dependency. Repaired in round 52 by declaring fleet dependency in docstring and reading `FLEET` from the subject counter.
- **`tools/mte-interop.py:311`** — `near-miss`:
  Line 311 defaults fleet root to `args.fleet_root or ROOT.parent` in `--check` mode. Selftest is hermetic, but `--check` mode is fleet-bound.
- **`tools/mutate-and-run.sh:1430`** — `near-miss`:
  `FLEET_ROOT=$(dirname "$(dirname "$(dirname "$SELF")")")` in `run_regression`. When run outside the fleet tree, regression legs cannot resolve sibling repos unless `--workdir` and mirrors are supplied.
- **`tools/bash-witness-study.py:97`** — `near-miss`:
  `KAGI_DEFAULT = REPO.parent / "kagi-shokunin"` used by `declare` and `run` modes. Selftest is hermetic.
- **`tools/env-diff.py:208`** — `near-miss`:
  `--fleet-root` defaults to `Path(__file__).resolve().parents[2]`.

---

## Connector Move Proposal

### Evidence
- In Shape 1, lanes either rigidly pin `N/N` (which breaks operability upon tool enhancement, e.g., `mte-interop-check`, `kotodama` battery, `kengaku` flip-check) or loosely pin a status string like `REGRESSION: PASS` (which passes but creates a `cannot_see` calibration blind spot).
- In Shape 2, lanes either undeclaredly crawl `ROOT.parent` or `/home/vgpnk/Projects/shokunin` (breaking clones outside the fleet root), or build synthetic hermetic sandboxes (as `kengaku` and `tsukuroi` did).

### Affected Axes
- **C1 Operability**: Eliminates false-positive gate failures caused by tool enhancements outrunning static string needles.
- **C2 Calibration**: Eliminates `cannot_see` blindness from generic status needles and enforces truth between declared execution scopes and runtime requirements.

### Proposed Move
Synthesize a **Registry Self-Contract Declaration**:
1. For Shape 1: Extend `tools/registry.json` schema to allow parameterized expectations (`"stdout_pattern": "legs_conforming=(\\d+)/\\1"` or dynamically checking equality between tool panel size and expected output) or mandate that gate rows pinning literal fractions must have an automated pre-commit hook verifying that tool updates co-commit registry expectation updates.
2. For Shape 2: Introduce an explicit `"env_scope": "fleet-bound" | "hermetic"` property on registry rows in `tools/registry.json`. In `tools/registry-check.py`, when running in a standalone clone without fleet mirrors, skip fleet-bound rows with a clean `SKIPPED (fleet-bound)` notice rather than failing exit 1.

### Risks & Verification
- **Risks**: Relaxing `N/N` matching to regex could admit under-count regressions if not strictly checking `N == total`.
- **Verification**: Run `python3 tools/registry-check.py --rev <rev>` on a standalone clone to verify that hermetic rows pass and fleet-bound rows explicitly report their scope.

---

## Summary
- Scanned 21 sibling lanes for Shape 1 (stale N/N needles) and Shape 2 (undeclared fleet-bound selftests).
- Identified same-shape count drift in `kotodama-shokunin` (battery coverage 9/9→10/10) and `kengaku-shokunin` (flip-check 19/19→27/27).
- Identified same-shape undeclared fleet reads in `kama-shokunin` (`round35/36/37-statement-audit.py`) and `kagi-shokunin` (`scope-gate.sh`).
- In `tameshi-shokunin`, identified `command-binding-selftest` as Shape 1 precedent and `mutate-and-run-regression` as near-miss cannot_see item.
- Proposed adding explicit `"env_scope"` metadata and parameterized equality needles to prevent recurrence.
