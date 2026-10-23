# ReviewCounterV2 — counter v2 vs amendments 1 and 2 (round 32, wave 2)

Seat: `ReviewCounterV2`. Scope: code review of `.ufo/evidence/round-32/v2/c1-measure-v2.py`
against `contract-amendment-1.json` and `contract-amendment-2.json`: predicate identity, held-out
validity rules as written vs code, sandbox flags, heldout-after-freeze logic, side channels, exit
codes. Read-only: I did not run the counter (the L1's first full v2 run is the measurement); all
behavioral evidence below is static reading plus function-level repros in my scratch dir, using
functions copied verbatim from the counter.

## Verdict first

The predicate sentence, label, code_conditions, thresholds, freeze logic, amendment-2 side-channel
closures and exit-code contract are implemented as written (details under "Verified"). Two real
defects exist, both in the held-out validation path: an unvalidated `witness.loop` is interpolated
into shell that the counter executes outside the sandbox (command execution from committed file
content), and a non-string kill `witness.block` crashes the counter with an uncaught exception.
Two smaller contract divergences: held-out discovery is non-recursive, and one undocumented
validity rule can silently shrink the sealed set.

## Verified (evidence)

1. **Pins.** `sha256sum` on the working tree: `tools/tally-audit.py` = `9639c458002ce2f954addbe047427010ae011353e073b293396bec800fa699ef`
   (= counter line 66 `TOOL_SHA256`, = amendment-2 `new_TOOL_SHA256`); `tools/mutate-and-run.sh` =
   `a7d3f2dd…2eb9` (= v1 line 43, which v2 reuses). At lane commit `528f8dee…` (the amendment-2
   commit): `git show 528f8dee…:tools/tally-audit.py | sha256sum` → `9639c458…99ef`; the counter
   blob there hashes `1ab9e9cf…f7f7c94`, byte-identical to the working-tree counter.
2. **"Frozen" identifiers are commit ids, not stale hashes.** `git log` shows amendment-1.json was
   introduced at `b50a18f0…` and amendment-2.json at `528f8dee…`, matching the `frozen` fields
   ("frozen b50a18f0…", "lane commit 528f8dee…"). amendment-1.json is unchanged since its commit
   (blob at 528f8dee = working-tree blob `3d1634af…`). No staleness defect.
3. **Predicate identity.** The docstring sentence (counter lines 17–22) is byte-equal to
   amendment-1's `predicate` after normalizing the docstring's line wrapping (observed
   `AMEND==DOC: True` from a text comparison script; no counter import). Label `C1_R32V2_PASS`
   matches amendment-1 `label` and the output line (counter 397–399).
4. **code_conditions vs code.** kill/accept: `rc == 1 and any(x.startswith('TALLY_AUDIT: FAIL'))` /
   `rc == 0 and any(x.startswith('TALLY_AUDIT: PASS'))` — exactly counter 268–272. pass: the
   condition string in amendment-1 is token-identical to counter 394–396. sandbox: `bwrap
   --unshare-all --clearenv` with only /usr, /etc, /proc, /dev, tmpfs /tmp, tool at /t, copy at /in
   — matches 257–264.
5. **18 + 8 is reachable for every seed.** v1 `frozen_kill` returns 9 entries and
   `generated_kill` appends exactly 9 unconditionally (each `rng.randrange(2)` only picks a
   variant) = 18; `frozen_accept` returns 6 (including `B0-pristine`) and `generated_accept` 2 = 8.
   The `== 18` / `== 8` checks (counter 394) are therefore satisfiable; v2 adds no length check of
   its own but inherits fixed sizes.
6. **heldout_after_freeze direction is correct.** `freeze` = adding commit of
   `.ufo/evidence/round-32/v2/c1-measure-v2.py` (counter 326, `SELF_PATH` line 67). For every
   listed held-out file: `after = 0` if the adding commit is missing, equal to freeze, or if
   `git merge-base --is-ancestor freeze add` FAILS (counter 333–335; exit 1 = not a descendant).
   So `after = 1` requires every file's adding commit to be a strict descendant of the counter's
   adding commit — exactly amendment-1 `code_conditions.after`. `adding_commit` takes the oldest
   adding commit (278–281), which is the strict reading for delete/re-add histories.
7. **Amendment-2 item 2 (side channel) implemented as written.** Copies written in a shuffled
   order (365–366, fresh entropy), every copy and the tool get mtime/atime 0 (373, 379), the tool
   file is written after all copies (376–379), the tool-run order is shuffled again (382–383), and
   each copy is mounted alone into its own bwrap instance so no sibling copy or lane path is
   visible (257–264). Residual host-side metadata (work-dir mtimes, copy sizes, printed COPY
   lines) either never enters the sandbox or is inherent copy content — no set-membership leak to
   the tool.
8. **Amendment-2 item 3.** A non-hex `--seed` prints `C1_R32V2: --seed must be hex` to stderr and
   returns 2 (main).
9. **Exit codes.** `return 0 if ok else 1` (401) with `raise SystemExit(main())` (404–405); 2 on
   non-empty `--work`, unresolvable rev, bad seed, pinned-runner unavailable, and v1.CounterError.
   Exceptions to this contract are findings 2 and 6 below.
10. **Tool CLI contract matches the outcome mapping.** `tools/tally-audit.py` docstring line 32
    (exit 0 PASS, 1 FAIL, 2 cannot audit) and final line `TALLY_AUDIT: PASS|FAIL …` (375–377) line
    up with `run_sandboxed`'s KILL/ACCEPT/OTHER classification (268–272).

## Findings by severity

### HIGH 1 — `witness.loop` is interpolated into shell the counter executes unsandboxed (code execution from committed file content)

- The written schema (counter docstring line 30) says `"loop": [optional leg names]`. No code
  enforces any of that: `validate` line 225–226 passes `w['loop']` straight to `set_loop`
  (109–114), which splices each element into the loop line as a `"$%s"` word; `tally_outputs`
  (129–137) embeds the rewritten block into a driver script; `bash_run` (116–127) executes it with
  plain `bash`, no bwrap, with the counter's privileges.
- The obvious `$( )` payload is accidentally defused — the template's leading `$` turns `"$$(…)"`
  into PID-concatenation (verified: first repro attempt, payload file not created). But a backtick
  is live inside double quotes.
- Exposing input — any held-out file with `"set":"kill"`, a valid `"witness":{"vector":[0,0,0,0,0,0,0,0,0], …}`
  and `"loop":["` + backtick + `touch <path>` + backtick + `"]`. For example:
  `"witness": {"vector": [0,0,0,0,0,0,0,0,0], "loop": ["`touch /fast/scratch/hyaku/tameshi-r32-seats/ReviewCounterV2/pwned-proof`"]}`
  (backticks literal in the JSON string), plus any one-occurrence edit pair so the copy differs
  from pristine.
- Observed (repro script `repro-inject.py` in my scratch dir; `set_loop`, `bash_run`,
  `tally_outputs` copied byte-for-byte from the counter, block text a minimal stand-in with the
  real pinned loop-line shape):
  ```
  rewritten loop line:   for st in "$`touch /fast/scratch/hyaku/tameshi-r32-seats/ReviewCounterV2/pwned-proof`"; do
  tally_outputs returned: [('0', 'passed=0 total=9')]
  payload executed (file exists): True
  ```
- Impact: the payload runs at validation time, before the tool ever sees the copy, and even when
  the copy is then rejected (here both blocks get the same rewritten loop, so the copy typically
  dies with `vector witness shows no difference`). The seal is inverted: the counter executes
  content it was supposed to judge. Any wave-2 seat can commit such a witness and the L1's
  unedited commit duty carries it into the measurement run.
- Smallest correction: validate `w['loop']` in `validate` — require a list of strings matching a
  leg-name pattern (e.g. `^[A-Za-z_][A-Za-z0-9_]*$`), raise `Invalid` otherwise.

### MEDIUM 2 — a non-string kill `witness.block` crashes the counter (uncaught AttributeError), exit 1, no verdict line

- `validate` lines 231–233 pass `w['block']` to `harness_failed` with no type check — contrast the
  accept-side witness collector at 340–342, which does check `isinstance(…, str)`.
  `harness_failed` line 153 calls `injected.rstrip('\n')`.
- Exposing input: held-out file with `"set":"kill"` and `"witness":{"block":123}` (edits valid).
- Observed (class check): `AttributeError: 'int' object has no attribute 'rstrip'`. The except
  tuple at line 350 catches `(Invalid, KeyError, TypeError, ValueError)` — not AttributeError —
  so the process dies with a traceback, exit 1, and never prints the `C1_R32V2:` line.
- Impact: contradicts docstring line 40 ("a copy the counter cannot parse is invalid") and the
  exit contract (2 = counter error). On the measurement run this turns one malformed held-out
  file into an ambiguous crashed run instead of a listed invalid copy or an exit-2 error.
- Correction: type-check `w['block']` (isinstance str) before the kill block branch, or add
  AttributeError to the caught tuple.

### MEDIUM 3 — held-out discovery is non-recursive and suffix-strict; nested or `.JSON` files are invisible to every check

- Lines 327–328: `git ls-tree --name-only <rev> .ufo/evidence/round-32/heldout/` lists only the
  top level, and the filter `endswith('.json')` drops everything else.
- Observed (scratch repo, same command shape): `git ls-tree --name-only HEAD d/` → `d/a.json`,
  `d/sub` — the subdir entry carries no `.json` suffix and everything under it is unseen.
- Exposing input: commit a valid kill copy at `.ufo/evidence/round-32/heldout/nested/x.json` (or
  name an existing copy `y.JSON`).
- Impact, both directions: such copies are never validated, never counted in `ho_n`/`cnt`, and
  exempt from the after-freeze check, so PASS can print true while an untested valid held-out copy
  exists — violating the predicate's "every valid held-out copy" / "every held-out file added
  after this counter". Symmetrically, a set hidden this way fails the ≥6 thresholds for reasons
  the run cannot report.
- Correction: use `git ls-tree -r --name-only` (or `-r` with the dir prefix) before the suffix
  filter.

### LOW 4 — undocumented validity rule: kill vector witnesses must keep pinned leg names

- Lines 223–224: `if cn != pnames: raise Invalid('vector witness needs pinned leg names')`. The
  written kill rule (docstring 30–33, amendment-1 `heldout.validity`) only requires the copy's
  block and the pinned block to differ on the witness vector; nothing forbids renamed legs for
  kill copies.
- Impact: a kill copy that is valid by the written rule is silently excluded (prints `valid=0`),
  shrinking the sealed set; if that drops `ho_kill` below 6 the run is a miss traceable to a rule
  that exists only in code. Doc-vs-code divergence in the validity contract.
- Correction: state the leg-name requirement in docstring and amendment, or drop the check.

### LOW 5 — sandboxed invocation deviates from the predicate's literal command

- Predicate (amendment-1 and docstring 17–22): run as `python3 tally-audit.py --runner COPY`.
  Code line 264: `python3 -I /t/tally-audit.py --runner /in/runner.sh`.
- `-I` (isolated mode) changes interpreter semantics, and argv/path differ from the written
  sentence; `code_conditions.sandbox` does not mention `-I` either. A tool whose behavior keys on
  argv shape or `sys.flags` is measured in a world the predicate does not name.
- Correction: add `-I` and the /t path to the written sentence and code_conditions, or run the
  literal command (e.g. bind the tool into the chdir and invoke `python3 tally-audit.py`).

### LOW 6 — sandbox/infrastructure failure is indistinguishable from an evaluated miss, or crashes

- Line 265 runs `timeout 600 bwrap …` with no preflight that `timeout`/`bwrap` exist or that
  unprivileged user namespaces work. `bwrap` missing → FileNotFoundError → uncaught → traceback,
  exit 1, no verdict. `bwrap` present but userns disabled → every copy OTHER → the line prints
  `C1_R32V2_PASS=false`, which the kill rule reads as a miss although no tool behavior was
  observed.
- Correction: one preflight probe (same bwrap profile around `true`) returning 2 on failure.

### INFO 7 — out-of-sandbox execution of seat-authored copy bodies is by design but unstated

Validating a copy necessarily runs its extracted tally block and harness section
(`tally_outputs`, `harness_failed`) outside bwrap; held-out `edits` shaping those blocks are
seat-authored and `bash -n` is the only pre-check, so any edit inside the block is live shell at
validation time. The amendment does not promise sandboxed validation, and this is distinct from
HIGH 1 (there a witness *parameter* violates its own written schema), but the docstring should say
plainly that the counter executes copy-derived shell.

### INFO 8 — latent uncaught RuntimeError in `fault_blocks`

`fault_blocks` (164–183) raises `RuntimeError('fault panel malformed')` if the panel self-check
fails; that class is not in the caught tuple at 350. Only reachable if the pinned runner bytes
drift from the anchors — impossible while the runner pin holds — so latent only.

## Residual risk and verification gaps

- I did not run the counter end-to-end (prohibited here; the L1's first full v2 run is the
  measurement). HIGH 1 and MEDIUM 3 are demonstrated at function level with verbatim counter
  functions, not through `main()`; MEDIUM 2's crash class is demonstrated, its exact uncaught
  propagation follows from reading line 350.
- The `fault_blocks` 18-panel integrity against the real pinned block was not executed.
- bwrap behavior on the eventual measurement host is untested (see LOW 6).
- I reviewed tally-audit.py only at its CLI/output contract; the tool's internals are another
  seat's target.
- Tooling: no installs or updates were performed (none needed); no tool installed or updated by
  this seat.

Report: .ufo/waves/round-32/w2/ReviewCounterV2.md
