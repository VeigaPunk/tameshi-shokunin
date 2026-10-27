# T53W1ExecRegCheck — registry-check operability at C* (round 53, wave 1)

Seat: T53W1ExecRegCheck (wave-1 executor). Item: run the entry-registry monitor at the
frozen content commit C* = `a41195dfc13a73958e4c5228ec196b28d03ded03` and report the
final `REGISTRY_CHECK` line; name any row that differs with its expectation vs observed.

Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. All subject bytes were read via
`git show`/`git cat-file` at the named revs, never from the working tree. No git
mutation was run in the lane (no commit/push/fetch/prune); the only commits were in a
throwaway fixture clone under this seat's scratch dir. No tool was installed or
upgraded (none needed). Scratch dir removed on exit.

## Headline

**The expectation in the item did not hold. The registry is RED at C*: one active row
differs.**

```
REGISTRY_CHECK: held=48/49 superseded=7
```

The item expected `held=N/N` over active rows, reasoning that "the C2 patches changed no
row expectations since selftest tallies are unchanged". That reasoning is half right and
half wrong, and the wrong half is the operative one:

- **Right:** `tools/registry.json` is byte-identical between the pre-fix-pass rev
  `a36d3e5` and C* (`git diff a36d3e5 a41195d -- tools/registry.json` → empty). No row's
  *expectation* changed. The C2 commit `218bc6b` also left `tools/registry.json`
  untouched (`git diff 218bc6b^ 218bc6b -- tools/registry.json` → empty).
- **Wrong:** the C2 patch changed the **bytes** of a tool whose bytes a registry row
  pins. The row's expectation is unchanged, but the row's *observed outcome* is now
  different. "No expectation changed" does not imply "every row still holds".

**The differing row: `verify-round15`.**

| | value |
|---|---|
| expectation | `exit=0` and stdout contains `measure-historical-preserved: PASS` |
| observed | `exit=1`; the stdout needle **is** present — the row fails on exit code only |
| row line | `ROW verify-round15 expect=0 got=1 differs` |

Row definition (unchanged at C*): `kind=gate`, `argv=["python3", ".ufo/evidence/round-15/verify.py", "--rev", "7650fe4db89f3a706aed63d048ac47e02289cc72"]`,
`timeout_s=60`, `status=active`, `external=true`, `source=SCORECARD.md@98bea7d:247`.

All 48 other active rows hold, and all 7 superseded rows produce byte-identical
observations to the round-52 baseline (checked row by row; the three
`evidence-disposition` superseded rows read `got=2` at both C* and the baseline, so that
is pre-existing and not this round's doing).

## Root cause

`verify-round15` runs the round-15 verifier. That verifier makes 44 checks; exactly one
fails at C*:

```
registered-tool-source-pin: FAIL worktree tools/context-capture.py sha256=07bac55b9a02c782317516d80c4c3ef031596fa53ab06405fbe1de54c962737a pinned=c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726
```

`.ufo/evidence/round-15/verify.py` (at C*, line 110) holds one constant:

```python
PIN_TOOL_SHA256 = (
    "c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726")
```

It is used at two distinct places with two distinct meanings:

- line 392, `"tool-source-pin"` — the **git blob** of `tools/context-capture.py` at the
  requested revision `7650fe4d`. This **passes**: that historical blob still hashes to
  `c4a1d165…`.
- line 642, `"registered-tool-source-pin"` — the **live worktree file**
  `ROOT/tools/context-capture.py` (the verifier's own docstring calls this "the actual
  maintained tool (not the temp copy)"). This **fails**.

The C2 commit `218bc6b` ("tools/ /tmp hardcodes honour TMPDIR") edited
`tools/context-capture.py` — two `dir="/tmp"` → `dir=tempfile.gettempdir()` changes plus
one docstring line. That changed the file's bytes, so the *maintained* tool no longer
hashes to the round-15 published digest. The round-15 verifier's `registered-tool-source-pin`
is a **live-worktree** check, and the C2 patch is exactly the kind of legitimate edit it
cannot absorb: the verifier conflates "the round-15 historical blob still hashes to X"
with "the currently maintained tool still hashes to X". Once the maintained tool is
edited for a later round, those two facts diverge, and the row turns red.

### Evidence chain (each step a command whose output is quoted)

1. **The bytes changed in C2.** `git show a41195d:tools/context-capture.py | sha256sum`
   → `07bac55b9a02c782317516d80c4c3ef031596fa53ab06405fbe1de54c962737a`.
   `git show a36d3e5:tools/context-capture.py | sha256sum` (immediately pre-fix-pass)
   → `c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726` — the pin.
   The two differ, and the difference is introduced by `218bc6b`.

2. **The regression is bracketed to exactly `218bc6b`.** Running the single row at each
   rev (`registry-check.py --rev REV --only verify-round15`):
   - `bcba892` (round 52 content) → `ROW verify-round15 expect=0 got=0 held`
   - `218bc6b` (the C2 fix pass) → `ROW verify-round15 expect=0 got=1 differs`
   - `e62d997` → `differs`; `a41195d` (C*) → `differs`

3. **Baseline control.** The full registry at the round-52 content commit:
   `TMPDIR=<scratch> python3 tools/registry-check.py --rev bcba892` →
   `REGISTRY_CHECK: held=49/49 superseded=7`, exit 0, **no** `differs` line. At C* the
   same command → `REGISTRY_CHECK: held=48/49 superseded=7`, exit 1, one `differs` line.
   The full baseline run is retained at scratch as `base_bcba892.out`.

4. **The single failing check is the worktree pin, and it is the only one.** Re-running
   the verifier directly in a scratch clone checked out at C* yields exactly one `FAIL`
   line — `registered-tool-source-pin` (the other `FAIL` token in the output is the
   literal word inside the passing line `mapping-oracle-discriminates: PASS oracle
   old=FAIL/1 new=PASS/0`). Every other check, including
   `tool-source-pin`, `prefix-source-pin`, `gate-frozen-builtin`, `gate-clean`,
   `gate-missing-env`, `gate-tampered-snapshot`, `gate-usage`, `mapping-oracle-old`,
   `mapping-oracle-new`, `measure-*`, and `sources-census`, reports PASS.

5. **Counterfactual: reverting only that one file restores the row.** In a scratch
   clone at C*, `git checkout a36d3e5 -- tools/context-capture.py` (restoring the
   pre-C2 bytes) and re-running the verifier → **exit 0**, zero `FAIL` lines, and
   `registered-tool-source-pin: PASS … sha256=c4a1d165… pinned=c4a1d165…`. Nothing else
   was changed. This isolates the cause to the C2 edit of that one file.

6. **The stdout needle is present.** The row's `stdout_contains` needle
   `measure-historical-preserved: PASS` appears in the observed stdout
   (`measure-historical-preserved: PASS all_baseline_bytes_preserved=1 changed=[]`).
   The row's failure is the exit code alone.

## Repair, verified end to end

The row is fixable without touching any row expectation. The verifier needs **two**
constants, not one: the round-15 historical blob digest (already passing, unchanged) and
the currently maintained tool's digest.

Verified in the throwaway fixture clone (`/fast/scratch/…/isolate/lane`, created with
`git clone` from the lane; `git rev-parse --show-toplevel` asserted equal to that path
before its only commit; that commit used a fixture identity and never touched the lane):

- Patch `verify.py` to add
  `PIN_MAINTAINED_TOOL_SHA256 = "07bac55b9a02c782317516d80c4c3ef031596fa53ab06405fbe1de54c962737a"`
  and to compare `worktree_sha` against `PIN_MAINTAINED_TOOL_SHA256` at line 642, leaving
  line 392 and the rest of `PIN_TOOL_SHA256`'s uses (lines 396, 529, 805) untouched.
- Running the verifier directly in that clone → **exit 0**, no `FAIL` line, and
  `measure-historical-preserved: PASS` present.
- Running the **actual registry row** against that clone
  (`registry-check.py --root <clone> --rev <fixture-commit> --only verify-round15`) →
  `ROW verify-round15 expect=0 got=0 held`.
- Control: the same clone with `verify.py` restored to the C* bytes →
  `ROW verify-round15 expect=0 got=1 differs`. The repair is the cause of the fix, not
  an artefact of the fixture.

This preserves the lane's own re-pin rule (SKILL.md:1085, "The re-pin rule"): a moved
pin is never re-interpreted against the new bytes — the round-15 blob digest stays where
it is, and the moved maintained-tool digest lands as its own appended fact.

**Recommended L1 action:** land a `verify.py` change that splits the two pins (as above)
and re-run the registry. Do **not** relax the row's `expect` (exit 0 → exit 1) and do
**not** delete or supersede the row — the row's intent (the maintained context gate
still matches its published digest) is sound; only the verifier's single-constant
encoding of it was outgrown by this round's own legitimate tool edit.

### Confirmation at the current lane HEAD

The L1 landed further commits while this seat was measuring. Re-running the full
registry at the then-current HEAD `651773ab9e3295777a087c033e620ea81b9717b6`
(the registry rows and `verify.py`'s `PIN_TOOL_SHA256` are unchanged there, and
`tools/context-capture.py` at that rev hashes to
`be539b4cd1cebe17227f91ffa202b7f3dac994fdfc6be20454d5277bd673183d`, still ≠ the
`c4a1d165…` pin) reproduces the same single red row:

```
REGISTRY_CHECK: held=48/49 superseded=7
ROW verify-round15 expect=0 got=1 differs
```

So the finding is **live and un-repaired at HEAD**, not a transient of C*. The
recommended split-pin repair above is still needed.

## Secondary finding: the C2 counter's `cr47` arm is RED at C*

Independent of the registry row, running the round's own frozen C2 counter at C*
reproduces a failure in the claim's own instrument.

```
C2_R53: rev=a41195d tmp_hits=0 registry_selftest=[rc=0 SELFTEST: PASS (51 cases)] envdiff_selftest=[rc=0 ENVDIFF_SELFTEST: 9/9 pass] cr47=rc=0 docs=ok total=2 C2_R53_PASS=false
PROBLEM cr47-zero-exit
PROBLEM cr47-no-scratch-message
```

The counter file is unmodified and matches the freeze record byte for byte
(`sha256sum .ufo/evidence/round-53/c2/measure.py` →
`1942cd8f9850727066439d317acaf5eb0a8e44458b0355ea4dceaf90e8c82c27` = the value in
`.ufo/evidence/round-53/freeze.json`), so this is the frozen instrument's own verdict.

**Cause.** The counter's `cr47` arm (`.ufo/evidence/round-53/c2/measure.py:98-111`) runs
`registry-check.py --selftest` with `TMPDIR` naming a **nonexistent** directory and
requires a non-zero exit naming scratch creation (the round-18 CR47 semantic: an
unusable scratch is could-not-evaluate, never a silent fallback). At C*,
`tools/registry-check.py` calls `tempfile.mkdtemp(..., dir=tempfile.gettempdir())`.
`tempfile.gettempdir()` **falls back to `/tmp`** when `TMPDIR` names a missing directory
(verified directly: `TMPDIR=<missing> python3 -c "import tempfile; print(tempfile.gettempdir())"`
→ `/tmp`). So the selftest succeeds (exit 0) and its scratch lands in `/tmp` — observed
live: `/tmp/tameshi-r17-registry-check-selftest.gmkb0a57` appeared during the run.
The C2 patch traded one silent `/tmp` fallback for another, and in doing so made the
selftest **write to `/tmp` when the caller explicitly asked for a different scratch root** —
against the host scratch directive (2026-10-25: `/tmp` is for files under 50 MB only) and
against the counter's own `cr47` clause.

The same arm is RED at the base rev (`6db1d220`: `cr47=rc=0`, `PROBLEM cr47-zero-exit`,
`PROBLEM cr47-no-scratch-message`, `total=4`), so the C2 patch did not *introduce* this
arm's failure — it failed at base too — but it also did not close it, and C2's own
target `C2_R53_PASS=true` is therefore **not met at C***.

**Status now (informational; the L1's in-flight work already addresses it).** At the
current lane HEAD the counter passes:
`C2_R53: rev=ac52387 tmp_hits=0 registry_selftest=[rc=0 SELFTEST: PASS (51 cases)] envdiff_selftest=[rc=0 ENVDIFF_SELFTEST: 9/9 pass] cr47=rc=2 docs=ok total=0 C2_R53_PASS=true`.
The repair is a strict scratch-root helper (`strict_scratch_root()` in
`tools/registry-check.py`, landed in `5b703c6`/`ceb372c`) that treats a set-but-unusable
`TMPDIR` as could-not-evaluate instead of falling back. That change is **not** in C*;
my C* measurement above is against the frozen C* bytes, which is what the item asked for.

## What is a HOLD, not a finding

- **`tools/registry.json` unchanged by the C2 patch** — `git diff 218bc6b^ 218bc6b --
  tools/registry.json` → empty. Row expectations genuinely did not change. This is the
  half of the item's premise that holds.
- **All 7 superseded rows** produce identical observations at C* and at the round-52
  baseline, including the three `evidence-disposition` rows that read `got=2`. The
  `superseded=7` count is stable.
- **The 48 remaining active rows** all hold, including the 30 `selftest` rows — so the
  item's premise that "selftest tallies are unchanged" is confirmed by the row outcomes.
- **`tools/registry.json` digest drift** vs `.ufo/evidence/round-23/requirements.json`
  (`registry_sha256: ebd2e69a…` vs the current `d65a5c42…`): this drift was introduced by
  `bcba892` (round 52), not by this round, and the `registry-replay` row is not in the
  active registry, so it does not affect this measurement. Noted only so the L1 is not
  surprised by it elsewhere.

## Commands run (all read-only in the lane; the only writes are in this seat's scratch)

- `TMPDIR=<scratch> python3 tools/registry-check.py --rev a41195dfc13a73958e4c5228ec196b28d03ded03`
  → exit 1, `REGISTRY_CHECK: held=48/49 superseded=7`, one `differs` row.
- Same with `--rev bcba892` (baseline control) → exit 0, `REGISTRY_CHECK: held=49/49 superseded=7`.
- Same with `--rev {218bc6b, e62d997, a41195d, 0494c24, 7650fe4d} --only verify-round15`
  (regression bracketing).
- Same with `--rev a41195d --only verify-round15 --json` (per-row stdout/stderr tails).
- `git show <rev>:tools/context-capture.py | sha256sum` at `7650fe4d`, `bca5deb`,
  `bcba892`, `a36d3e5`, `218bc6b`, `a41195d`.
- `git diff a36d3e5 a41195d -- tools/registry.json`; `git diff 218bc6b^ 218bc6b -- tools/registry.json`.
- `python3 .ufo/evidence/round-53/c2/measure.py --lane <lane> --rev {a41195d, 6db1d220,
  ac52387} --work <scratch> --explain`.
- `git clone` of the lane into scratch; a fixture commit there carrying the split-pin
  repair; `registry-check.py --root <fixture> --rev <fixture-commit> --only verify-round15`.

## Risk

- The `verify-round15` row is `external=true` and reads live fleet state; the repair
  touches a frozen round-15 evidence script. The L1 should land the split-pin change
  as an explicit re-pin (append the moved digest; leave the round-15 blob pin and the
  `expected.json` `source_sha256` payload as they are), and should re-run the registry
  at the resulting rev to confirm `held=49/49` before the deciding run.
- I did **not** edit `tools/`, `corpus/`, `SKILL.md`, `MANIFEST.json`, or
  `.ufo/evidence/` — those are L1-owned. The split-pin patch was exercised only in a
  throwaway fixture clone and is described here for the L1 to land.
- Lane tree left as found: `git status --porcelain` shows only the pre-existing
  round-53 wave outputs and the L1's own in-flight commits; no `.ufo/evidence/round-15/`
  files were added by these runs (the verifier's own writes landed in the scratch clone).
