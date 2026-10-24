# ReviewToolPin — round 37 wave 1 (Tool pin)

Scope: verify the new tally-audit tool SHA in `counter-pin.json` matches committed bytes, and the
r36 counter sha is unchanged. Report any digest or revision mismatch. Live lane checkout untouched
(read-only git + sha256sum only; no tool installs, no pacman).

**VERDICT: PIN VERIFIED — no digest or revision mismatch.**

## 1. Tool pin matches committed bytes

Pin: `.ufo/evidence/round-37/counter-pin.json:8` — `tool_path: tools/tally-audit-v3.py`,
`tool_sha256: da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede`.

```
$ cd <lane> && sha256sum tools/tally-audit-v3.py
da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede  tools/tally-audit-v3.py
$ git hash-object tools/tally-audit-v3.py
b0c7d48e526bd7aa15775f9358de26794238e1b6
$ git ls-tree HEAD tools/tally-audit-v3.py
100644 blob b0c7d48e526bd7aa15775f9358de26794238e1b6	tools/tally-audit-v3.py
$ git show ae9b771ab795fb5b4a6302165d8abdc0a2c6b229:tools/tally-audit-v3.py | sha256sum
da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede  -
```

Working bytes == committed blob == pin. `git status --porcelain` on the file is clean.
Prior bytes at r36 freeze rev `d9c496b` were blob `4190a84d` (old sha `6188db16…d354`);
superseded exactly once, in commit `ae9b771` "round-37: add bounded ANSI-C code-view support"
(2026-10-24) — consistent with the C2 kill rule "new digest recorded in a pre-run pin; no
code-view edit follows that pin".

## 2. r36 counter sha unchanged

Pin: `.ufo/evidence/round-37/counter-pin.json:6` — `counter_sha256: 9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53`.

```
$ sha256sum .ufo/evidence/round-36/c1/c1-measure-v2.py
9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53  .ufo/evidence/round-36/c1/c1-measure-v2.py
$ git ls-tree d9c496b19371b779ce0eec6dfee1b049b27a3a2d -- .ufo/evidence/round-36/c1/c1-measure-v2.py
100755 blob 5f1c2047ce533182a8938cb2b44d73938a54c153	.ufo/evidence/round-36/c1/c1-measure-v2.py
$ git ls-tree HEAD .ufo/evidence/round-36/c1/c1-measure-v2.py
100755 blob 5f1c2047ce533182a8938cb2b44d73938a54c153	...
```

Same blob at r36 freeze rev, pin commit, and HEAD; clean status. Equals the pre-r37 frozen
record at `.ufo/evidence/round-36/contract.json:24` (`counter_sha256 9eb8944c…fa53`) and every
r36 receipt citation of it.

## 3. Revision coherence (no rev mismatch)

- Pin commit `ae9b771ab795fb5b4a6302165d8abdc0a2c6b229` is an ancestor of HEAD `e6185d5f0b63a6963205110cb098f2f1eca27622`;
  `git diff ae9b771..HEAD --stat -- tools/tally-audit-v3.py .ufo/evidence/round-36/c1/c1-measure-v2.py .ufo/evidence/round-37/counter-pin.json` is empty → zero post-pin drift on pinned paths (post-pin commits touch only evidence output files).
- `counter-pin.json` committed at `ae9b771`, bytes at that commit == worktree (`git show …:counter-pin.json | sha256sum` = `249d66200db7ce5d609d67834fa780251822db3912183f91571ec0cd92fb8b66`, both).
- Deciding replay recorded in `.ufo/evidence/round-37/c2-repin-after.stdout:17-18`:
  `…tool_sha=da8c1ef4b30ce4e4 tool_sha_ok=1 runner_sha_ok=1 … C1_R36V2_CONTROL_PASS=true`
  `C2_R37_REPIN: counter_sha256=9eb8944c…fa53 tool_sha256=da8c1ef4…3ede frozen_predicate_replayed=1 rev=ae9b771ab795…229 C2_R37_REPIN_PASS=true`;
  `c2-repin-after.exit` = 0, stderr 0 bytes. rev string equals the full hash of `ae9b771` (rev-parse confirmed).
- Independent C2 deciding run agrees: `.ufo/evidence/round-37/code-view/after.stdout` — `tool_sha256=da8c1ef4…3ede rev=ae9b771ab795…229 C2_R37_PASS=true`, both cases PASS (vs `before.stdout` at `d9c496b`: old sha `6188db16…`, `ansi_trailing_comment=0/1`).

## 4. Enforcement is real, not decorative

`.ufo/evidence/round-37/c2-repin.py` reads the pin from the verified rev itself, recomputes both
digests, and exits 2 (`SETUP pin_mismatch`) on any mismatch before running the counter; success
additionally requires the full token set (`pub_kill=6/6 … ho_invalid=0`, `rev=<rev>`) in the
frozen counter's output. The counter's control-mode bypass is genuine and matches the pin's
`control_mode` note: `.ufo/evidence/round-36/c1/c1-measure-v2.py:462` —
`tool_sha_ok = tool_bytes is not None and (a.tool is not None or tool_sha == TOOL_SHA256)`
(embedded constant at line 65 still names the historical `6188db16…` pin, unsatisfiable against
the new tool in deciding mode — by design; r37 deciding uses its own measure).

## Findings

- **None at INFO-or-above within scope.** No digest mismatch, no revision mismatch.

## Residual risk / verification gaps

1. **Wrapper bytes unpinned**: `c2-repin.py` (sha256 `f25eafa5d38bcddffd66289fda22e8a9f1eca78edd426e791c2136f74ab8bd3b` as observed, committed and clean at HEAD) is not digested inside `counter-pin.json`. The pin's enforcement rests entirely on it; a post-hoc wrapper edit would silently weaken the check. Not a mismatch today.
2. Historical `6188db16…` references (r35 contract, r36 contract/dispatch/spec waves, receipts, v1/v2 counters' embedded constants) remain — frozen records, correct as-is; only `c1-measure-v2.py` deciding mode can never accept the new tool bytes, which is the sanctioned control-mode arrangement.
3. I did not re-execute the repin myself; I verified the committed receipts, exits, and all digest/rev cross-edges against the object database.
