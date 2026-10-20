# AttackControl — positive git control failure → exit 1

Seat: critic, leaf. I only read source. I executed no gate, selftest, probe or fixture. Read revision: lane HEAD `a9cf4da78f2514c7bedd91a850a88590009d7df0` plus the uncommitted round-15 working tree. `tools/context-capture.py` was **absent** at review time (the `tools/` listing contains only `bash-witness-study.py`, `evidence-disposition.py`, `mutate-and-run.sh`, `pin-disposition.py`, `repeat-control.py` and `witness-metadata.py`). So this attacks the planned promotion of the historical `.ufo/evidence/round-14/capture-context.py` (`#096B`), not finished code. The host has `git version 2.55.0`; I only queried the version. I installed and updated no tools.

Axes: C1 calibration honesty (does exit 1 mean what it says), attribution of each finding to one cause, hermeticity of the selftest, historical integrity (round14 receipt not overwritten), and scope (no new environment claim).

## Observed source facts

- `positive_control_block` (`capture-context.py:395-411`) runs `git -C LANE_ROOT rev-parse --git-dir` twice: once under `control_env`, once under `control_env + {GIT_DIR: POISON_PATH}`.
  - `baseline_ok = baseline.exit == 0 and stdout.strip() != ""`
  - `reflects = POISON_PATH in injected.stdout or POISON_PATH in injected.stderr or injected.exit != baseline.exit`
  - `effective = baseline_ok and injected.exit != 0 and reflects`
- `decide` (`:553-580`) appends the **prose** reason `"git poison positive control is ineffective"` at `:570-571` and returns `("mismatch", 1, reasons)` (`:578-579`). The status `mismatch` is shared with comparison, digest, environment and mapping failures. **No stable finding ID exists for the control.**
- `evaluate` (`:465-550`) can raise `InvalidContext` → exit 2 before `decide` ever runs:
  - poison path exists, at `:469-472`; this is a host `lexists('/nonexistent/tameshi-round14-poison')`;
  - missing inputs or failed mapping parse, at `:476-515`;
  - `git` or `python3` not on PATH, at `:517-522`;
  - git or probe timeout and non-UTF-8 output, via `run_bounded` (`:190-210`);
  - a probe baseline that is not a six-leg ok `pin-disposition-v1` document (`comparison_block:352-361`). This runs **after** the control at `:547-548`.
- The retained round14 receipt shows only the real-git success path. In `context-receipt.json` `positive_control`: baseline exit 0 with `.git\n`; injected exit 128 with stderr `fatal: not a git repository: '/nonexistent/tameshi-round14-poison'`; `effective: true`; overall `ok`/0/`[]`.
- The SKILL registry row (`SKILL.md:1602`) labels the tool `probe`, maps "1 observed mismatch or failed control", has no selftest, and omits 64.

## Counterexample (CE-1): the exit-1 control case passes for the wrong cause

Suppose a nominal test calls `decide({... "positive_control": {"effective": False} ...})`, or makes the CLI exit 1 in any convenient way, and then asserts `exit == 1` and `status == "mismatch"`. That test cannot tell apart three different situations:

1. **The poison is ignored.** Baseline exits 0 and the injected run also exits 0. This is the only real "control ineffective" failure: the GIT_DIR injection was not observable to git.
2. **The baseline cannot be established.** The fixture root is not a git repo, so the baseline gives `rev-parse` exit 128, `baseline_ok` is False, and the run exits 1.
   - With real git under a temp root, the injected run also exits 128 and names the poison in stderr, so `reflects` is True. The failure comes only from the baseline.
   - Real git's stderr wording in a non-repo is `[INFERENCE]` from git behaviour; the injected stderr wording is the one observed in the retained receipt.
3. **Another predicate fails at the same time.** For example, a probe or runner digest mismatch also yields `mismatch`/1.

What makes this concrete:

- With **real git**, case 1 cannot be reached hermetically. The injected value is fixed to `/nonexistent/...`, so real git can only succeed if that path is a valid git dir. But an existing poison path is rejected with exit 2 (`:469-472`), and creating it would write outside the temp roots.
- So the easiest way for a "real-CLI" selftest to get exit 1 for the control is case 2: build a synthetic fixture in `/tmp` without `git init`.

Mutants that such a selftest would let survive:

- **M-a:** injected env built from `control_env` without `INJECTED_ENV`, i.e. the poison is never injected. Case 2 still exits 1, because the baseline fails anyway.
- **M-b:** delete `decide:570-571`. If case 3 also fires, the run still exits 1 with `mismatch`.
- **M-c:** `effective = injected.exit != 0`, i.e. drop `baseline_ok`. In case 2 this gives `effective = True`. The test then flips to exit 0 and kills M-c only if the fixture asserted exit 1 — fine. But a positive fixture without a repo would then pass spuriously.

All three pass a check of "exit 1 + mismatch". None of them are caught by a helper-only `decide()` test, because a helper test never exercises `positive_control_block`, the env wiring, PATH resolution of git, the ordering against `comparison_block`, or where the receipt is written.

## Secondary findings

- **CE-2 (vacuous term, optional):** under `baseline_ok` (baseline exit 0) and `injected.exit != 0`, the clause `injected.exit != baseline.exit` is always true. So `reflects` never binds, and `effective ≡ baseline_ok ∧ injected.exit ≠ 0`. A git that fails the injected run for an unrelated reason would count as an effective control. The retained receipt does contain the poison in stderr, but nothing enforces it.
- **CE-3 (hermetic dependency, optional):** every CLI fixture stats the fixed host path `/nonexistent/tameshi-round14-poison` (`:469`). If that path ever exists on the host, every selftest case becomes exit 2. This is a host read outside the temp root, though not a lane or sibling read.
- **CE-4 (write location, required by the contract, not by defect 5):**
  - The historical `OUTPUT_REL` is the round14 receipt (`:58`). The CLI writes a receipt on exit 1 (`:629-632`), so a CLI selftest whose promoted root/output handling is not redirected would overwrite or create live receipts.
  - `LANE_ROOT` is four `dirname`s from `SELF` (`:46`). Copied unchanged into `tools/context-capture.py`, it resolves to `/home/vgpnk/Projects` instead of the lane.
  - A helper test can detect neither.

## Required routed fix vs optional hardening

### Required for routed defect 5

1. **Stable finding ID.** Emit one stable ID for the control failure, e.g. `control_ineffective`, in both the receipt and stdout. The selftest asserts the **exact** finding-ID set `== {control_ineffective}` and **exit 1**, through a real CLI subprocess.
   - An exact set kills M-b: if the control is the only failing predicate, deleting `:570-571` turns the run into exit 0.
   - The exit stays 1 and the decision semantics stay the same, as the integration interface requires.
2. **Attribute the fixture to case 1, not case 2.** The selftest must also assert `positive_control.baseline_ok == true` and `positive_control.injected.exit == 0` in the temp receipt. The only hermetic way to get there is a **git shim** placed first on the subprocess `PATH`. Such a shim resolves through `shutil.which("git")` (`:518`), and `safe_env` keeps `PATH`.
   - Shim behaviour: print `.git`, exit 0, and ignore `GIT_DIR`.
   - Do not shadow `python3`, which is resolved the same way.
   - Do **not** reach exit 1 through a non-repo temp root.
3. **Keep every other predicate green in the same fixture.** Otherwise the ID set is contaminated or the run exits 2:
   - a synthetic `tools/pin-disposition.py` that emits the same six-leg `status: ok`, `pinned.status: verified` document with `observed_at`, and with `tool_sha256` equal to its own on-disk digest;
   - `expected.json` `inputs["tools/pin-disposition.py"]` equal to that digest;
   - a manifest `derived_from` path ending in `tools/mutate-and-run.sh` whose sha matches the fixture runner;
   - a runner whose six header rows, `PIN_`/`REV_` constants and `run_regression` calls match the manifest, using the leg names in `EXPECTED_SUFFIX` (`:74-81`).
   Because `comparison_block` runs after the control, a broken synthetic probe shows up as exit 2, not a false exit 1. That is good, but only if the test asserts the literal exit.
4. **Paired green fixture.** The same tree with a shim that exits 128 and prints the poison path when `GIT_DIR` is set, and otherwise behaves like the case-1 shim → exit 0 with an empty ID set. This pins the control at both polarities. M-a and M-c then fail one of the two cases.
5. **Receipt location.** Receipts are written only under the temp fixture root. The CLI root/output must be honoured in selftest, the lane round14 receipt bytes must stay identical, and normal capture writes only round15 (see CE-4).

### Optional hardening (not required by defect 5; declare it if adopted)

- Use a distinct ID for case 2 (e.g. `control_baseline_failed`).
  - Keeping it at exit 1 preserves historical semantics.
  - Reclassifying it to 2, could-not-evaluate setup, is defensible but changes `decide` semantics and must be stated as a change.
- Bind `reflects` (CE-2) by requiring `POISON_PATH` in the injected stderr. The tradeoff is that this depends on git's message format; it is observed for real git in the retained receipt but is not version-stable.
- Make the poison-exists check hermetic under selftest (CE-3) without changing the declared production injection value.

## What the canonical judge should reject

- A selftest whose control case calls only `decide()`/`positive_control_block`.
- A selftest that asserts only `exit 1`/`mismatch`.
- A selftest that gets exit 1 from a non-repo fixture.
- Any claim that the control proves environment independence beyond the one GIT_DIR injection.

All of these are status-neutral conformance points on the context instrument. None of them is harm to C1 or an axis.

## Checks for L1 after seats return (not run here)

- `python3 tools/context-capture.py --selftest`: exit 0. The output names the control case with literal `exit=1` and ID `control_ineffective`, and the green pair with `exit=0`.
- Grep the selftest source for a PATH git shim, `baseline_ok`/`injected.exit == 0` assertions, and an exact ID-set comparison.
- `sha256sum .ufo/evidence/round-14/context-receipt.json .ufo/evidence/round-14/capture-context.py` matches before and after (`7313e9a2…` for the script).
