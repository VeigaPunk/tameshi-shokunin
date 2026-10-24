# Residual review — C2 (depth capability) — ResC2Counter

Lane: tameshi-shokunin @ tip `ba3c35fb6c9582fcf2351c59c61661dd7a8e7400` (master), tree clean (`git status --porcelain` = 0 entries) at audit start. Read-only attack; no lane/state writes (only artifact below; one gitignored `tools/__pycache__` created by my own selftest invocation was removed).

## Verdict

**Claim C2 SURVIVES.** Every axis re-executed from committed bytes reproduces the claim; no BLOCKER, no MAJOR. Two MINOR observations (neither affects C2).

## Executed checks + evidence

### 1. Counter at d9c496b → PASS=false ✅
```
$ python3 .ufo/evidence/round-37/code-view/measure.py --lane . --rev d9c496b19371b779ce0eec6dfee1b049b27a3a2d; echo EXIT=$?
CASE ansi-c-escaped-quote-trailing-comment FAIL
  expected=": $'it\\'s'                 \nst_tsu=9\n"
  actual=": $'it\\'s' # inert st_tsu=0\nst_tsu=9\n"
CASE ansi-c-literal-hash PASS
C2_R37: ansi_trailing_comment=0/1 ansi_literal_hash=1/1 tool_sha256=6188db16de045f2927df2a0e667bc1539f4acfce5a1ac116e6de3107bf15d354 rev=d9c496b… C2_R37_PASS=false
EXIT=1
```
`diff` of this re-run vs frozen `code-view/before.stdout`: **BEFORE_IDENTICAL** (byte-for-byte).

### 2. Counter at ae9b771 → PASS=true ✅
```
$ python3 .ufo/evidence/round-37/code-view/measure.py --lane . --rev ae9b771ab795fb5b4a6302165d8abdc0a2c6b229; echo EXIT=$?
CASE ansi-c-escaped-quote-trailing-comment PASS
CASE ansi-c-literal-hash PASS
C2_R37: ansi_trailing_comment=1/1 ansi_literal_hash=1/1 tool_sha256=da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede rev=ae9b771… C2_R37_PASS=true
EXIT=0
```
`diff` vs frozen `code-view/after.stdout`: **AFTER_IDENTICAL**.

Counter integrity: `measure.py` is frozen — worktree sha `1cb70e6b…452e6a` == `HEAD:` blob == blob at `ae9b771`; it loads the tool **from the given rev** via `git show <rev>:tools/tally-audit-v3.py` (exec'd with `__name__` set so no main runs), fixtures are hardcoded, and it checks content + length + newline count. Output cannot be influenced by worktree tool bytes.

### 3. Tool digest da8c1ef4… ✅ (independently re-hashed)
```
6188db16…  blob at d9c496b:tools/tally-audit-v3.py   (pre-fix, 6188db16de…d354)
da8c1ef4…  blob at ae9b771:tools/tally-audit-v3.py   (da8c1ef4b30ce4e42b1cc2b11229543e36e122457d2336f9a990d28161693ede)
da8c1ef4…  blob at ba3c35fb (tip):tools/tally-audit-v3.py
da8c1ef4…  worktree tools/tally-audit-v3.py
```
Claim precision: `da8c1ef4…` is the sha of the *tool at the rev the counter loads*, printed in the PASS=true run — matches exactly. (At d9c496b the tool legitimately hashes `6188db16…`; the claim's digest binds to the post-fix rev.)

### 4. Selftest 35/35 ✅ (live re-run, not just receipt)
```
$ python3 tools/tally-audit-v3.py --selftest; echo EXIT=$?
35 CASE lines, all PASS (incl. both code_view ANSI-C cases)
TALLY_AUDIT_V3_SELFTEST: 35/35 pass
EXIT=0                       (wall 272.5s)
```
Frozen receipt `.ufo/evidence/round-37/tool-selftest-after.stdout` tail agrees: `TALLY_AUDIT_V3_SELFTEST: 35/35 pass`.

### 5. Frozen r36 predicate re-attested (repin) ✅ — re-run at BOTH revs
```
$ python3 .ufo/evidence/round-37/c2-repin.py --lane . --rev ae9b771…; echo EXIT=$?
   → 16 COPY lines identical to frozen c2-repin-after.stdout
   C1_R36V2_CONTROL: … pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9
     ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1
     rev=ae9b771… C1_R36V2_CONTROL_PASS=true
   C2_R37_REPIN: counter_sha256=9eb8944c… tool_sha256=da8c1ef4…
     frozen_predicate_replayed=1 rev=ae9b771… C2_R37_REPIN_PASS=true   EXIT=0  (157s)
$ python3 .ufo/evidence/round-37/c2-repin.py --lane . --rev ba3c35fb…; echo EXIT=$?
   → same predicate line, rev=ba3c35fb…, C2_R37_REPIN_PASS=true        EXIT=0  (157s)
```
Frozen receipt agrees (`c2-repin-after.exit`=0, stderr empty). Wrapper enforces both pin digests before execution (`c2-repin.py` `pins_ok` gate → SETUP exit 2 on mismatch); the r36 counter itself re-loads the tool from rev bytes (`git_show(lane, rev, TOOL_PATH)`) and pins the runner (`a7d3f2dd…`, `runner_sha_ok=1`).

### 6. counter-pin.json vs committed bytes at tip ✅
- Pin blob identical at `ae9b771` and tip: sha256 `249d6620…fb8b66` both (`git diff ae9b771 HEAD -- <pin>` empty; `235608a` does not touch tip content).
- `tool_sha256 da8c1ef4…` == tip tool blob (re-hashed) ✅; `counter_sha256 9eb8944c…` == tip blob of `.ufo/evidence/round-36/c1/c1-measure-v2.py`, committed == worktree ✅.
- `control_mode` is honestly disclosed: historical v3 digest check bypassed via `--tool`, wrapper enforces the new digest independently — verified in source.

## Findings

- **MINOR (hygiene, not C2):** commit `235608ae235c916a10168364449e4b7651c52c1b` has **empty subject and body** and is a rewrite twin of `ae9b771` (same 3-file stat: c2-repin.py +79, counter-pin.json +11, tool ±44; tool bytes already `da8c1ef4…`). Reachable only via `refs/jj/keep/235608a…`, **not** in the tip chain — a jj history-rewrite artifact, outside the claimed ancestry. Smallest fix: `jj abandon`/drop the keep ref if lane hygiene is graded.
- **MINOR (hardening, not C2):** `c2-repin.py` attests the counter digest from *rev bytes* but executes the counter from the *worktree path* (`os.path.join(lane, COUNTER_PATH)`). Safe today (worktree==HEAD verified clean, both `9eb8944c…`), but a future dirty worktree would run unattested bytes under a rev-derived label. Smallest fix: write `counter_result.stdout` to the tmp workdir and exec that.

## Residual risk
- The repin replays 16 mutation copies (9 public + 7 sealed) with specimen bash contained in per-run `/tmp` dirs (HOME/TMPDIR redirected, non-`$root` `rm` targets refused by the filesystem-safety gate); no lane writes observed — tracked tree clean after the entire audit (only untracked sibling-owned `residual/` remains).
- Timing: full repin ≈ 157 s; selftest ≈ 272 s — reproducible within the wrapper's 1800 s budget.

## Verification gaps
None material. I did not re-derive the r36 predicate's own scoring semantics (out of C2 scope; the frozen counter bytes are pinned and unchanged, which is what C2 claims). Wave-2 mutation-refusal receipts (`dispatch-w2` items) belong to the sibling mutation seat and were not re-attacked here.
