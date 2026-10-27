# T53W1ExecTmpVerify — C2 tool patches at C* (operability)

Seat: `T53W1ExecTmpVerify` (wave-1 executor, round-53, L1 `TameshiR53a2`).
Item: verify the C2 tool patches at content commit `C* = a41195dfc13a73958e4c5228ec196b28d03ded03`.
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` — read-only for `tools/`, `SKILL.md`, `corpus/`,
`.ufo/evidence/`; this seat wrote only its two deliverable paths under `.ufo/waves/round-53/w1/`.
Scratch (all work + raw receipts): `/fast/scratch/hyaku/tameshi-r53/w1/T53W1ExecTmpVerify/` —
**deleted before yield**; the receipts are delivered alongside this report (see "Receipts").
Host: Linux 7.2.11-arch1-1 x86_64, Python 3.14.8, git 2.56.0, `bwrap` present at `/usr/bin/bwrap`.
Tooling installed/updated by this seat: **none** (no pacman, no uv, no npm, no cargo — the task needed only
stock `git`, `python3`, `strace`, `mktemp`).

---

## One-line verdict per check

| # | Check | Verdict |
|---|-------|---------|
| 1 | `grep -rn 'dir="/tmp"'` over the C* blobs of `tools/` is empty | **PASS** — 0 hits |
| 2 | `tools/registry-check.py --selftest` with `TMPDIR=<scratch>` exits 0 | **PASS** — exit 0, `SELFTEST: PASS (51 cases)` |
| 2 | `tools/env-diff.py --selftest` with `TMPDIR=<scratch>` exits 0 | **PASS** — exit 0, `ENVDIFF_SELFTEST: 9/9 pass` |
| 3 | `registry-check --selftest` with `TMPDIR=<nonexistent dir>` exits non-zero, names scratch creation, prints NO `REGISTRY_CHECK` verdict line | **FAIL** — exit **0**, no scratch-creation message; the "no verdict line" half **PASSES** |
| 4 | Scratch dirs were created under the redirected `TMPDIR` (not `/tmp`) | **PASS** — 213 / 146 `mkdir` under my `TMPDIR`, **0** under `/tmp` |

**Bottom line: 4 of 5 checks pass. Check 3 fails.** The frozen C2 counter at `C*` prints
`C2_R53_PASS=false` with `total=2`, problems `cr47-zero-exit` and `cr47-no-scratch-message`.
**C2 as frozen is not satisfied at `C*`.**

---

## Check 1 — `dir="/tmp"` is gone from the C* blobs of `tools/` — PASS

All git-object reads; the working tree was never used as a source.

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    grep -n 'dir="/tmp"' a41195dfc13a73958e4c5228ec196b28d03ded03 -- tools/
```
→ no output, exit 1 (git-grep no-match).

The counter's own regex is broader and also empty:

```
git -C … grep -n -E "dir\s*=\s*[\"']/tmp" a41195dfc13a73958e4c5228ec196b28d03ded03 -- tools/
```
→ no output, exit 1.

A **broader** scan than the counter's — every literal `dir=` assignment of any kind, in any `tools/` file
at `C*` — is also empty:

```
git -C … grep -n -E "dir\s*=\s*[\"'][^\"']+[\"']" a41195dfc13a73958e4c5228ec196b28d03ded03 -- tools/
```
→ no output, exit 1.

Provenance of the patch (the C2 edit itself is at `218bc6b`, an ancestor of `C*`; `C*` = `218bc6b` +
the later SKILL.md/QUALITY/LOG/lesson edits, with `tools/` byte-identical between the two and to `HEAD`):

```
git -C … diff --stat 218bc6b^ 218bc6b -- tools/
 tools/bash-witness-study.py   | 2 +-
 tools/context-capture.py      | 4 ++--
 tools/env-diff.py             | 2 +-
 tools/evidence-disposition.py | 2 +-
 tools/pin-disposition.py      | 2 +-
 tools/registry-check.py       | 8 ++++----
 tools/repeat-control.py       | 2 +-
 7 files changed, 11 insertions(+), 11 deletions(-)
```

7 tools patched — the claim's "7 tools patched at `C*`" holds. Every hunk is the same shape:
`dir="/tmp"` → `dir=tempfile.gettempdir()`.

```
git -C … diff --stat HEAD a41195dfc13a73958e4c5228ec196b28d03ded03 -- tools/
```
→ empty (identical), so `C*`'s `tools/` is what the working tree carries.

Residual `/tmp` strings remain in `tools/` at `C*`, but they are **not** `dir=` hardcodes and are
outside this item's stated check: `env-diff.py`'s inner bwrap namespace (`"/tmp/w"`, `--tmpfs /tmp`)
is a sandbox-internal path, and `mutate-and-run.sh` already uses `"${TMPDIR:-/tmp}/…"` (TMPDIR-honouring).
`write-path-census-v4.py:632` has `os.path.join("/tmp", "census")` inside a **string literal used as a
census test fixture**, not as a live write path. Flagged for the L1 as context only, not as a finding.

## Check 2 — both selftests exit 0 with `TMPDIR` redirected — PASS

Both tools were extracted from the git object store at `C*` (not copied from the working tree), and
byte-identity against the C* blob was proven before execution:

```
git -C … show a41195df…:tools/registry-check.py > scratch/toolcopy/registry-check.py
git -C … show a41195df…:tools/env-diff.py       > scratch/toolcopy/env-diff.py

registry-check.py blob=a03beb47df05071e1a50af2fc6fb5ffa94fe808d hashobj=a03beb47df05071e1a50af2fc6fb5ffa94fe808d match=YES
env-diff.py       blob=4186cdb75d92153c149cd3a85ddd3ac3386879ea hashobj=4186cdb75d92153c149cd3a85ddd3ac3386879ea match=YES
```

Run with `TMPDIR=/fast/scratch/hyaku/tameshi-r53/w1/T53W1ExecTmpVerify/tmpdir`:

| tool | exit | last stdout line |
|---|---|---|
| `registry-check.py --selftest` | **0** | `SELFTEST: PASS (51 cases)` |
| `env-diff.py --selftest` | **0** | `ENVDIFF_SELFTEST: 9/9 pass` |

Both stderr streams empty. Both runs took ~10 s and ~1.4 s respectively.

## Check 3 — `registry-check --selftest` with a **nonexistent** `TMPDIR` — **FAIL**

Contract wording (`.ufo/evidence/round-53/contract.json`, C2 predicate):
> "registry-check.py --selftest with a missing TMPDIR directory exits non-zero naming scratch creation
> (could-not-evaluate, round-18 CR47) and never prints a verdict-bearing diff line"

Command and observed result at `C*` (`TMPDIR=/…/no-such-dir-3047691`, which does not exist):

```
TMPDIR=$S/no-such-dir-3047691 python3 registry-check.py --selftest
EXIT=0                       <-- expected non-zero
stdout: … SELFTEST: PASS (51 cases)   (2700 bytes)
stderr: (empty)
grep -c 'REGISTRY_CHECK' stdout -> 0        <-- this half PASSES
grep -c 'cannot create clone scratch' stdout|stderr -> 0   <-- this half FAILS
```

**Verdict: FAIL.** The run exits 0, prints no scratch-creation message, and — correctly, and per the
contract — prints no `REGISTRY_CHECK` verdict line.

### Root cause (evidence-backed)

`tempfile.gettempdir()` **never fails and never honours an unusable `TMPDIR`**: CPython probes the
candidate directory for writability and, if it is missing or unwritable, silently falls back to `/tmp`.
Measured on this host:

```
nonexistent: TMPDIR=/…/no-such-dir-probe exists=False -> gettempdir()=/tmp
existing_unwritable: TMPDIR=/…/unwritable-probe exists=True -> gettempdir()=/tmp
```

So the C* patch (`dir="/tmp"` → `dir=tempfile.gettempdir()`) does not produce an error path when
`TMPDIR` is unusable — it produces a **silent `/tmp` fallback**. Consequences, all observed:

* The `round-18 w2 CR47` guard at `tools/registry-check.py:767-768` is **unreachable**:
  ```python
  try:
      work = tempfile.mkdtemp(prefix="tameshi-registry-check-", dir=tempfile.gettempdir())
  except OSError as exc:  # round-18 w2 CR47: an unusable /tmp is could-not-evaluate (2), never "differs" (1)
      raise RuntimeError(f"cannot create clone scratch under the scratch root: {exc}") from exc
  ```
  `mkdtemp` is handed a directory that `gettempdir()` has already validated, so `OSError` never fires
  and the `RuntimeError` never propagates. Confirmed by strace: with a nonexistent `TMPDIR`, the run
  created **213** directories under `/tmp/tameshi-*` and **0** under the requested `TMPDIR`:
  ```
  "/tmp/tameshi-registry-check-9bmdk17x
  "/tmp/tameshi-registry-check-k9m6uf74
  … (6 distinct clone-scratch roots, 213 mkdir calls total under /tmp)
  ```
  An **existing-but-unwritable** `TMPDIR` (mode `0500`) behaves identically: exit 0, no
  `cannot create clone scratch` message anywhere in stdout or stderr.
* The failure is a *host-scratch* failure mode as well: a caller who sets `TMPDIR` to a missing path
  gets scratch written to `/tmp` with no diagnostic, instead of a could-not-evaluate.

### Why the base behaved the same way (control relevance)

At the contract's `BASE = 6db1d220b337c35ff1e25bf9cfd74abc9db1498d` the same command also exits 0
(`SELFTEST: PASS (51 cases)`) — the base hardcoded `dir="/tmp"`, so it ignored `TMPDIR` entirely and
also could not raise. The C2 edit fixed the *hardcode* but did not create the *guard*: the "unusable
scratch ⇒ could-not-evaluate" arm of the C2 predicate is unmet at `C*` and was unmet before.

### Frozen counter corroboration

The frozen counter at `.ufo/evidence/round-53/c2/measure.py` (unmodified, read from the working tree
at the freeze bytes) run against `C*`:

```
$ python3 .ufo/evidence/round-53/c2/measure.py \
      --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
      --rev  a41195dfc13a73958e4c5228ec196b28d03ded03 --work <empty>
C2_R53: rev=a41195dfc13a tmp_hits=0 registry_selftest=[rc=0 SELFTEST: PASS (51 cases)] \
        envdiff_selftest=[rc=0 ENVDIFF_SELFTEST: 9/9 pass] cr47=rc=0 docs=ok \
        total=2 C2_R53_PASS=false
PROBLEM cr47-zero-exit
PROBLEM cr47-no-scratch-message
```
counter exit status **1**.

The counter's check 3 is the contract's check 3 verbatim: `TMPDIR=<work>/missing` (absent),
`rc != 0`, `'REGISTRY_CHECK' not in stdout`, and `re.search(r'cannot create (clone )?scratch', blob)`.
Only the last two-part requirement is satisfied. The counter's `docs=ok` arm also passes, so the
failure is isolated to the CR47 arm.

### Minimal repair — validated end to end (for the L1, not applied)

A `scratch_root()` helper that resolves `TMPDIR` **strictly** (no `gettempdir()` fallback) and raises
the contract's own message restores the predicate. Applied in a scratch clone of the lane at `C*`
(scratch clone only; the lane was not touched):

```python
def scratch_root():
    """TMPDIR when set (must be an existing directory); else the platform temp root."""
    v = os.environ.get("TMPDIR")
    if v:
        if not os.path.isdir(v):
            raise RuntimeError(
                "cannot create clone scratch under the scratch root: "
                "TMPDIR %s is not a directory" % v)
        return v
    return tempfile.gettempdir()
```
with `dir=tempfile.gettempdir()` → `dir=scratch_root()` at all three sites in
`tools/registry-check.py` (`clone_lane_at_rev` and `selftest`).

Measured on that scratch clone:

* missing `TMPDIR` → exit **1**, stderr carries `cannot create clone scratch under the scratch root: TMPDIR … is not a directory`, stdout has **0** `REGISTRY_CHECK` lines — satisfies the counter's CR47 arm.
* valid `TMPDIR` → exit **0**, `SELFTEST: PASS (51 cases)`, empty stderr — no regression.
* the **frozen counter** against that repaired clone now prints:
  ```
  C2_R53: rev=9c6ef7bc80c0 tmp_hits=0 registry_selftest=[rc=0 SELFTEST: PASS (51 cases)] \
          envdiff_selftest=[rc=0 ENVDIFF_SELFTEST: 9/9 pass] cr47=rc=1 docs=ok \
          total=0 C2_R53_PASS=true
  ```
  counter exit status **0**.

Note for the L1: the same `tempfile.gettempdir()` fallback exists in the **other six** patched tools
(`bash-witness-study.py`, `context-capture.py`, `evidence-disposition.py`, `pin-disposition.py`,
`repeat-control.py`, and `env-diff.py`). Only `registry-check.py` is *falsifier-covered* by the
contract's CR47 arm, but all seven share the silent-`/tmp`-fallback behaviour, and `env-diff.py
--selftest` under a missing `TMPDIR` also exits 0 (measured) rather than surfacing an error. A
uniform `scratch_root()` (or equivalent strict resolver) across the seven would close the class.

## Check 4 — scratch really is created under the redirected `TMPDIR` — PASS

Because both selftests clean up their scratch in a `finally`/context manager, a post-hoc `ls` of
`TMPDIR` is empty. The creation was therefore proven two ways.

**(a) `strace` of `mkdir`/`mkdirat`** (`strace -f -qq -e trace=mkdir,mkdirat`):

`registry-check.py --selftest`, `TMPDIR=$S/tmpdir3`:

```
mkdir("…/tmpdir3/tameshi-r17-registry-check-selftest.tn65z6mt", 0700) = 0
mkdir("…/tmpdir3/tameshi-r17-registry-check-selftest.tn65z6mt/lane", 0777) = 0
mkdir("…/tmpdir3/tameshi-r17-registry-check-selftest.tn65z6mt/canary", 0777) = 0
mkdir("…/tmpdir3/tameshi-r17-registry-check-selftest.tn65z6mt/selftest-lane-shokunin", 0777) = 0
…
"/…/tmpdir3/tameshi-registry-check-0dr0_q90
"/…/tmpdir3/tameshi-registry-check-2zwp5c8z
"/…/tmpdir3/tameshi-registry-check-lc1r6z2i
"/…/tmpdir3/tameshi-registry-check-otkm60bm
"/…/tmpdir3/tameshi-registry-check-srywxwwi
"/…/tmpdir3/tameshi-registry-check-whrj1mvv
```

* `mkdir` calls mentioning my `TMPDIR`: **213**
* `mkdir` calls under `/tmp`: **0**
* distinct scratch roots: 1 selftest root + 6 `tameshi-registry-check-*` clone roots, **all** under my `TMPDIR`.

`env-diff.py --selftest`, `TMPDIR=$S/tmpdir4`: **146** `mkdir` calls under my `TMPDIR`
(`tameshi-r21-envdiff.*` roots, each with `home/` and `tmp/`), **0** under `/tmp`.

**(b) live `ls` during the run** (poll loop racing the selftest):

```
SCRATCH_VISIBLE_DURING_RUN: tameshi-r17-registry-check-selftest.zylgibq6
selftest_exit=0 scratch_seen=1
--- after run (cleanup) ---
(empty=yes)
```

The scratch root is genuinely created under the redirected `TMPDIR`, and the tool removes it on exit.

---

## Concurrent development in the working tree (observed, not mine)

During this seat's run the **working tree** `tools/` was modified by another seat (not this one — the
helper is named `strict_scratch_root`, not `scratch_root`, and it touches all seven patched tools;
`git diff HEAD -- tools/` was empty when this seat began and non-empty at 10:41). The change applies
the **same class of fix** this report recommends — a strict `TMPDIR` resolver that raises instead of
falling back to `/tmp`:

```python
def strict_scratch_root():
    """Scratch root for mkdtemp: TMPDIR when set (must be a usable directory —
    round 53: a set-but-unusable TMPDIR is could-not-evaluate, never a silent
    fallback to /tmp, preserving CR47 semantics), else the platform default."""
    t = os.environ.get("TMPDIR")
    if t:
        if not os.path.isdir(t) or not os.access(t, os.W_OK):
            raise RuntimeError(
                "cannot create clone scratch under the scratch root: TMPDIR is not a usable "
                "directory: %r (could-not-evaluate)" % t)
        return t
    return tempfile.gettempdir()
```

This seat did **not** write that edit (verified: `grep -rn 'def scratch_root' tools/` → no match, and
the peer helper's name and file set differ from this seat's probe). This seat only **measured** it, in
a scratch clone of the lane, without touching the lane:

* with a **missing** `TMPDIR`: exit **1**, stderr carries `cannot create clone scratch under the
  scratch root: …`, stdout has 0 `REGISTRY_CHECK` lines — the CR47 arm is satisfied;
* the **frozen counter** against a scratch clone carrying that working-tree `tools/`:

  ```
  C2_R53: rev=b63547a014bd tmp_hits=0 registry_selftest=[rc=0 SELFTEST: PASS (51 cases)] \
          envdiff_selftest=[rc=0 ENVDIFF_SELFTEST: 9/9 pass] cr47=rc=1 docs=ok \
          total=0 C2_R53_PASS=true
  ```
  counter exit status **0**.

**One caveat worth flagging to the L1 (measured, and it is easy to get wrong):** an *earlier* revision
of that pending fix raised
`"scratch root from TMPDIR is not a usable directory: %r (could-not-evaluate)"` — semantically
correct, exit code 1, but it does **not** match the frozen counter's regex
`re.search(r'cannot create (clone )?scratch', blob)`. Measured on that intermediate revision:

```
C2_R53: … cr47=rc=1 docs=ok total=1 C2_R53_PASS=false
PROBLEM cr47-no-scratch-message
```

So the message wording is load-bearing for the counter, not merely cosmetic. The current working-tree
revision has since been reworded to include `cannot create clone scratch under the scratch root:` and
the counter passes (`total=0 C2_R53_PASS=true`). **The L1 should verify the counter's
`cr47-no-scratch-message` arm against the final integrated bytes before accepting C2.**

Note also that the pending fix's resolver lives in `tools/registry-check.py` **and** the six sibling
tools; `git diff HEAD -- tools/` showed all seven modified. This seat did not audit the siblings'
individual semantics (out of its item scope), only that the class-level defect it reported — the
silent `/tmp` fallback — is what they now address.

## Receipts

Receipts were produced under
`/fast/scratch/hyaku/tameshi-r53/w1/T53W1ExecTmpVerify/receipts/` and are **delivered with this
report** at
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-53/w1/T53W1ExecTmpVerify-receipts/`
(29 files, 232 KB). The scratch tree itself was deleted before this yield (scratch discipline: a seat
that ends with its tree on disk reports that as its own defect). Receipt contents:

| receipt | content |
|---|---|
| `VERDICT.txt` | the five one-line verdicts + frozen-counter verdict + problems |
| `check1-grep.txt` | the three grep receipts, the 7-tool patch diffstat, C*-vs-HEAD identity |
| `registry-check-selftest.stdout` / `.stderr` | check-2 registry-check run (exit 0, 51 cases) |
| `env-diff-selftest.stdout` / `.stderr` | check-2 env-diff run (exit 0, 9/9) |
| `registry-check-badtmp.stdout` / `.stderr` | check-3 run at `C*` (exit **0**, no scratch message) |
| `env-diff-badtmp.stdout` / `.stderr` | env-diff under missing `TMPDIR` (exit 0) |
| `unwritable-tmp.stdout` / `.stderr` | existing-but-mode-0500 `TMPDIR` (exit 0, no message) |
| `base-registry-badtmp.stdout` / `.stderr` | same command at `BASE` (exit 0 — control) |
| `c2-counter.stdout` / `.stderr` | frozen counter at `C*` → `C2_R53_PASS=false`, exit 1 |
| `c2-counter-explain.stdout` | the two `PROBLEM` lines |
| `strace-registry-mkdir.txt` | mkdir trace, registry-check, valid `TMPDIR` (213 under TMPDIR, 0 under /tmp) |
| `strace-envdiff-mkdir.txt` | mkdir trace, env-diff, valid `TMPDIR` (146 under TMPDIR, 0 under /tmp) |
| `strace-badtmp-mkdir.txt` | mkdir trace, missing `TMPDIR` → **213 under /tmp** (the fallback) |
| `repair2.stdout` / `.stderr` | repaired scratch copy, missing `TMPDIR` → exit 1 + scratch message |
| `repair-ok.stdout` / `.stderr` | repaired scratch copy, valid `TMPDIR` → exit 0, 51 cases |
| `c2-counter-repaired.stdout` | frozen counter on the repaired scratch clone → `C2_R53_PASS=true`, exit 0 |
| `pending-fix-snapshot.txt` | the peer's working-tree `tools/` diff + the counter verdict against it |
| `wt-counter.stdout` | counter against the peer's **earlier** fix revision → `total=1`, `cr47-no-scratch-message` (message-wording trap) |
| `wt-counter3.stdout` | counter against the peer's **current** fix revision → `total=0`, `C2_R53_PASS=true`, exit 0 |
| `wt-badtmp.stderr` | the peer's fix under a missing `TMPDIR`: exit 1 + `cannot create clone scratch …` |

The repaired scratch clone lived at `$S/laneclone` (a `git clone --no-hardlinks` of the lane, checked
out at `C*`, with the `scratch_root()` patch committed under a throwaway local identity). It was
`git rev-parse --show-toplevel`-verified to be `$S/laneclone` before that commit, and it was deleted
with the scratch tree.

## Scope / hygiene statement

* No lane file was created, modified, or deleted by this seat except this report
  (`.ufo/waves/round-53/w1/T53W1ExecTmpVerify.md`) and the delivered receipt directory
  (`.ufo/waves/round-53/w1/T53W1ExecTmpVerify-receipts/`), both under the seat's write scope.
* No `git`/`jj` mutating command was run in the lane, the fleet root, the source repo, or any sibling
  lane. All reads of `tools/` and `SKILL.md` were `git show`/`git grep` at `C*`, i.e. git objects only.
* No `pacman` / `uv` / `npm` / `cargo` transaction was performed.
* The scratch tree `/fast/scratch/hyaku/tameshi-r53/w1/T53W1ExecTmpVerify/` was removed before yield.
* The two `/tmp/tameshi-r4-2-regression.*` directories seen during the run were **not** created by this
  seat (they are the `mutate-and-run.sh` shape, created by another process); this seat's own stray
  `/tmp` writes (from the missing-`TMPDIR` fallback) were self-cleaned by the tools.

## Findings for the L1 (1 actionable)

1. **`C2` does not hold at `C*` as frozen.** The contract's C2 predicate requires
   `registry-check.py --selftest` under a missing `TMPDIR` to exit non-zero naming scratch creation.
   At `C*` it exits 0 and prints no such message; the frozen counter prints `C2_R53_PASS=false`
   (`total=2`, `cr47-zero-exit`, `cr47-no-scratch-message`). The C2 patch removed the `dir="/tmp"`
   hardcodes (check 1, check 4 pass) but left the CR47 guard unreachable, because
   `tempfile.gettempdir()` silently falls back to `/tmp` instead of raising.
   *Minimal validated fix:* resolve `TMPDIR` strictly (`scratch_root()` above) in
   `tools/registry-check.py` — with it the frozen counter prints `C2_R53_PASS=true` (exit 0), and the
   valid-`TMPDIR` selftest still exits 0. Extending the same strict resolver to the other six patched
   tools would close the class. **This seat did not apply the fix** — tools/ is outside the seat's
   write scope; the L1 integrates.
   *Status at report time:* a peer seat has since applied an equivalent strict resolver to the working
   tree (`strict_scratch_root()`, all seven tools). Measured against a scratch clone carrying those
   bytes, the frozen counter now prints `C2_R53_PASS=true` (`total=0`, exit 0) — see "Concurrent
   development in the working tree" above. **The L1 should re-run the counter against the final
   integrated bytes and confirm the `cr47-no-scratch-message` arm still clears**, because an
   intermediate revision of that fix failed it on message wording alone.

Nothing else in this seat's scope fails.
