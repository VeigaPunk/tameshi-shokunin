# S084 — live re-verification of the realpath row and Gate caveat

Verdict: **AGREE**. The S084 quote is a verbatim prefix of the live section's
first sentence, the section is the one named, and the non-strict caveat is
confirmed — the resulting path "may be missing or inaccessible, may still
contain links or loops". Scope ("identity, not a sandbox") is supported.
Three precision defects noted below; none makes the row or Gate false.

## Observed (live, 2026-10-21)

- `curl -sSL https://docs.python.org/3/library/os.path.html#os.path.realpath`
  → HTTP 200, no redirect away from `https://docs.python.org/3/...`,
  `size_download` 90223. `<title>` = "os.path — Common pathname manipulations
  — Python 3.15.1 documentation"; anchor `id="os.path.realpath"` present
  (byte 59604). So the row's "Python 3.15.1 documentation opened 2026-10-21"
  and "section `os.path.realpath`" are both accurate (`SOURCES.md:93`,
  `corpus/lessons/round-24.md:31-32`).
- First paragraph of the section (P0), normalised:
  "Return the canonical path of the specified filename, eliminating any
  symbolic links encountered in the path (if they are supported by the
  operating system)."
  The quoted text in `SOURCES.md:93` / `corpus/knowledge/replay-projection-hardening.md:1`
  / `corpus/lessons/round-24.md:33-34` reproduces that prefix exactly, but
  silently drops the parenthetical qualifier.
- P1: "By default, the path is evaluated up to the first component that does
  not exist, is a symlink loop, or whose evaluation raises OSError. All such
  components are appended unchanged to the existing part of the path."
- P2: "Thus, the resulting path may be missing or inaccessible, may still
  contain links or loops, and may traverse non-directories."
- P4/P5: `strict=True` re-raises the first error; `ALL_BUT_LAST` and
  `ALLOW_MISSING` sentinels exist in 3.15. `ALLOW_MISSING` re-raises every
  error except `FileNotFoundError`, so its result "will not contain any
  symbolic links, but the named file and some of its parent directories may
  be missing."
- Cross-version check: `https://docs.python.org/3.14/library/os.path.html`
  → HTTP 200, title "Python 3.14.9 documentation"; P0–P2 wording identical,
  P4 without `ALL_BUT_LAST` (3.15 addition). The local interpreter is
  3.14.8.
- Behavioural confirmation on 3.14.8 (scratch dir `/tmp/s084probe`, symlink
  pair a↔b, nothing in the repo touched):
  - `os.path.realpath('/tmp/s084probe/a')` → `/tmp/s084probe/a` (loop left
    unresolved, no raise);
  - `os.path.realpath('/tmp/s084probe/a', strict=True)` → `OSError` errno 40
    "Too many levels of symbolic links";
  - `os.path.realpath('/tmp/s084probe/nope/x')` → unchanged, `exists=False`;
  - `os.path.realpath('/tmp/s084probe/nope/x/../y')` → `/tmp/s084probe/nope/y`
    (lexical `..` around a missing component), still `exists=False`.
- Applied use matches the row's scope: `tools/registry-replay.py:64-69`
  realpath-normalises `repo`, `fleet_root` and sibling lanes;
  `:13` states it; `:20-21` states rows are "not write-isolated from
  siblings". No isolation claim is made from realpath.
- `--plan` (`tools/registry-replay.py:269-274`) has no directory/existence
  guard: a missing `--repo` still exits 0 with a normalised-but-absent
  identity. That is consistent with the S084 caveat (identity, not
  existence) but is not spelled out in the knowledge entry's bounds.

## Precision defects (do not overturn the verdict)

1. **`corpus/lessons/round-24.md:35` narrows the stop conditions.** It says
   non-strict mode "may still contain links or loops" *"for missing
   components"*. P1 names three stops: a missing component, a symlink loop,
   or a component whose evaluation raises `OSError` ("access denied", "not a
   directory", "bad argument to internal function"). The caveat therefore
   holds more broadly than the lesson states; "for missing components"
   understates it.
2. **"Non-strict mode" is not one behaviour in 3.15.** `strict` accepts
   `False` (default), `ALL_BUT_LAST`, and `ALLOW_MISSING`. Only the default
   can leave a *loop* in the result; `ALLOW_MISSING` re-raises loop/other
   errors and leaves only missing names. The row's "missing or looping
   components" is correct for `strict=False`, which is all the lane uses
   today, but the row should say "default (strict=False)" to stay true if a
   sentinel is ever passed.
3. **Unmarked quote truncation** at `SOURCES.md:93`,
   `knowledge/replay-projection-hardening.md:1`, `lessons/round-24.md:33-34`:
   the parenthetical "(if they are supported by the operating system)" is
   elided without an ellipsis. Cosmetic; the retained words are verbatim.
4. Cosmetic: the SOURCES row's source URL omits `#os.path.realpath` while the
   knowledge entry includes it; the anchor resolves.

## Smallest safe correction

- `corpus/lessons/round-24.md:35`: replace "for missing components" with
  "when resolution stops at a missing, looping, or OSError-raising
  component" (keep the verbatim "may still contain links or loops").
- `SOURCES.md:93` claim: change "non-strict mode may still leave missing or
  looping components" to "the default non-strict (strict=False) result may
  still be missing or contain links or loops".
- Optional, if `--plan` output is ever used as evidence of an existing
  sibling: add "plan output is identity, not existence" to the bounds in
  `corpus/knowledge/replay-projection-hardening.md:36-37`.

No quote change is required; the cited sentence and section are real and
current. No tools installed or upgraded. No producer authentication,
promotion, or score claim is made.
