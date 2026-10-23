# RevengerWitness-4 — witness semantics of the round-33 C1 counter (`.ufo/evidence/round-33/c1/c1-measure.py`)

Seat: tameshi-r33-w1 / RevengerWitness-4 · 2026-10-23 · Scratch: `/fast/scratch/hyaku/tameshi-r33-seats/tameshi-r33-w1-RevengerWitness-4/`
Runner bytes pinned: worktree `tools/mutate-and-run.sh` sha256 `a7d3f2dd…2eb9` = `PINNED_RUNNER_SHA` (verified at seat start). Tool bytes `9dbbce62…33a4` = frozen pin (verified). No production file edited; no counter default-mode run; no `--write-controls` run.

## Byte provenance (the counter is a moving target)

The counter changed three times during this seat. Everything below says which bytes each result comes from.

| time (mtime) | sha256 (first 8) | lines | note |
|---|---|---|---|
| freeze-era (read ~15:50) | not captured at read | 362 | the bytes I first read and imported for exp 1 |
| 15:58:25 | `81a8cfcc` | 409 | adds `bwrap_argv` helper, `timeout` moved outside bwrap, own `run_tool_sandboxed` |
| ~16:02 (observed during a batch) | `d43ead07` | — | bytes on which I first ran the counter's own `block_run` directly |
| 16:00:53 | `e5ba9cfe` | 412 | current at report time; adds `len(vec) != 9` rejection at :115-116 |

The contract (`contract.json` → `frozen_artifacts.c1_counter`) pins the counter by **path only**, not by sha; counter identity is enforced through the controls receipt (`counter_sha256`), which by design is invalidated by every edit — so `--write-controls` must be (re)run after this wave's amendments settle. Marked `[INFERENCE]` where I argue intent.

## Verdict summary

| # | Question | Result on current bytes `e5ba9cfe` |
|---|---|---|
| F0 | frozen `block_run` sandbox | broken on freeze-era bytes (every run `(1,'')`); independently repaired mid-wave; verified working on `d43ead07`+ |
| Q1 | kill copy, comment-only block edit (behaviorally identical on every vector) | `ho_invalid` — the RIGHT verdict for the kill label; but the same set-blind gate makes equivalence-class **accept** copies unsatisfiable (Q1b) — gap stands |
| Q2 | witness vector length 4 | mis-compared (constant crash signature `(1,'')` on both sides); **fixed** at :115-116 (`len(vec) != 9` rejected) |
| Q3 | kind=head witness on inert head edit (`VERSION` rename) | validated as a **must-kill** with zero fault demonstration; real tool PASSes it → claim voided with a blameless tool — gap stands |
| Q3b | lethal block edit riding behind a benign head edit, `set=accept`, kind=head | validated as a **must-accept**; real tool FAILs it → claim voided — gap stands |

---

## F0 — the frozen `block_run` could never execute a block (historical; already repaired by the L1 route)

Freeze-era argv (first read, `block_run`): `bwrap --unshare-all --die-with-parent --new-session --clearenv --ro-bind <script> /x.sh --bind <d> /w --chdir /w --dev /dev --proc /proc timeout 60 bash /x.sh`, run via `subprocess.run(..., capture_output=True)` with **stderr discarded**. Reproduction (scratch `exp/mini.sh` + `exp/bd/`):

```
$ bwrap --unshare-all --die-with-parent --new-session --clearenv --ro-bind bd/x.sh /x.sh \
    --bind bd /w --chdir /w --dev /dev --proc /proc timeout 60 bash /x.sh
bwrap: execvp timeout: No such file or directory      # rc=1, empty stdout
```

No runtime mount ⇒ no `/usr` ⇒ `timeout`/`bash` unresolvable. `block_run` then falls through its parse loop and returns `(1, '')` for **every** block and **every** vector — exp 1 (`out/witness-exp.stdout`, frozen bytes): even the pristine block on `[1,2,0,0,0,0,0,0,0]` returned `(1, '')` instead of `(1, 'REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)')`. Consequence had it survived to measurement: every vector witness would read as `a == b` → `ho_invalid > 0` → `C1_R33_PASS=false` regardless of the sealed set. The committed before-value (`before/c1-at-base.stdout`) could not catch this: `controls_ok=0` short-circuits `main()` before the held-out loop, so `block_run` is never reached pre-data.

The 15:58 amendment repairs exactly this (docstring: "the frozen form execvp'd timeout inside a sandbox with no runtime mounts"); I verified the counter's **own** `block_run` on bytes `d43ead07`:

```
CURRENT counter block_run pristine [1,2,0,0,0,0,0,0,0]: (1, 'REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)')
CURRENT counter block_run pristine [4]*4: (1, '')
```

All Q1/Q2/Q3 results below were re-derived with a **working** oracle (`exp/witness-exp2.py`: the counter's own script template verbatim, only the bwrap argv repaired with `--ro-bind /usr /usr` + `--symlink usr/bin /bin …` + `--tmpfs /tmp`; 30 oracle calls, `out/witness-exp2.stdout`), and the decisive witness-gate calls were re-run against the counter's own current functions (`out/final-semantics-check.stdout`, bytes `e5ba9cfe`).

## Q1 — comment-only block mutant, kill label: `ho_invalid` is right, but the gate is set-blind

Mechanism (current lines 181-188): the witness runs **one** author-chosen vector, and only after `pb != mb` textually; `return a != b, 'vector'` has **no branch on `ho['set']`**.

Evidence (working oracle, `exp/witness-exp2.py`): block text differs (`pb != mb` True), head identical; pristine vs comment-mutant block on six vectors spanning PASS/FAIL/SETUP and count regimes — all tie, e.g.

```
vec=[1, 2, 0, 0, 0, 0, 0, 0, 0]  both (1, 'REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)')
vec=[0]*9                        both (0, 'REGRESSION: PASS (cases=9 passed=9; ledger legs exact: …)')
vec=[255]*9                      both (2, 'REGRESSION: SETUP (cases=9 passed=0 cannot-verify=9)')
```

The inserted line (`      # audit note (witness probe)\n` after the `0)` arm, inside the case body) is lexically inert in bash — it cannot expand, execute, or alter adjacent parsing — so the tie holds on **every** 0..255 vector at every position, not just the six probed. The real v2 tool confirms the copy is inert: `v1.run_tool` (round-32 frozen runner of tools, plain subprocess) on `work2/copy-q1-comment-kill…` → `ACCEPT rc=0`, last line `TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)`.

**Verdict:** for a copy labeled `set=kill`, `ho_invalid` is the right verdict — the copy is behaviorally pristine, so it is a mislabeled non-defect, and voiding the claim (ok requires `ho_invalid == 0`, line 396) is the fail-closed choice consistent with the counter's own witness language ("witness does not demonstrate the fault", line 365). Skipping or silently relabeling would let an author pad or poison the tallies. `[INFERENCE]` on intent.

**The actual defect exposed here (Q1b):** the same set-blind gate makes genuinely-equivalent **accept** copies unsatisfiable. On current bytes (`out/final-semantics-check.stdout`):

```
comment-only block edit, set=accept, vector len-9 -> (False, 'vector')   # demands a != b — impossible for an equivalence copy
comment-only block edit, set=accept, kind=head    -> (False, 'head')     # head unchanged
```

There is **no** witness a cosmetic/decoy accept clone (round-32 classes B4-cosmetic, gB7-nonce-in-block, B3-decoys-post-block) can carry. Any such clone in the sealed set ⇒ `ho_invalid > 0` ⇒ whole claim false. Note also the post-block region (selftest/main) belongs to neither `head_of` nor `tally_block_of`, so post-block-only edits fail both witness kinds for both sets.

## Q2 — witness vector length 4 mis-compared; already fixed upstream

Mechanism (freeze-era and pre-`e5ba9cfe` bytes): `decl` uses `names[:len(vector)]` (line 157); `validate_ho` accepted any length of ints 0..255 (line 114), including `[]` (rejected only later by the falsy `no-witness` branch) and length 10+ (silently aliased to 9 names, since `names[:12]` is the same 9 names — demonstrated: len-12 `[4]*12` behaved identically to len-9).

With a working oracle, a **genuine** arm-4 defect (T08: `4) npass=$((npass+1)) ;;` added after ARM1):

```
len=9  [4]*9      pristine=(2,'…SETUP (cases=9 passed=0 cannot-verify=9)') mutated=(0,'…PASS (cases=9 passed=9…)')
len=4  [4,4,4,4]  pristine=(1,'')  mutated=(1,'')   differ=False
len=4  [1,1,1,1]  pristine=(1,'')  mutated=(1,'')   differ=False
len=1  [1]        pristine=(1,'')  mutated=(1,'')   differ=False
```

Why: with only `len` leg vars declared, the pristine 9-operand loop dies on the first undeclared operand (iteration len+1, `$st_checklist` for len 4) under `set -u` before any output — so for **every** vector of length 1..8 the pristine side is the constant crash signature `(1,'')`, and the comparison never measures tally behavior. A genuine arm/guard defect ties → false `ho_invalid`; the only len<9 "distinctions" possible are crash-vs-completes artifacts of loop-shape edits (D01 drop@4: len-4 ties because the duplicated operand merely defers the crash to the next undeclared name; len-9 distinguishes properly, `(…failed=1 setup=1)` vs `(…failed=2 setup=1)`).

**Status:** fixed in current bytes — `validate_ho` :115-116 rejects `len(vec) != 9` (`witness.vector must name all 9 leg statuses`), verified on `e5ba9cfe`: len-4 and len-12 both rejected. This matches the patch I would have recommended (the runner has exactly 9 legs; nothing else preserves the harness's semantics). Reminder: the counter's sha changed again, so the controls receipt must be regenerated after amendments settle.

## Q3 — `kind=head` is a text-only witness: inert copies validate as must-kill, lethal ones as must-accept

Mechanism (current lines 178-179): `if w.get('kind') == 'head': return head_of(mutated) != head_of(pristine), 'head'` — a pure textual diff, no behavioral demonstration, and only the head is inspected (block content unchecked).

**Q3 experiment** — rename the genuinely unused head variable `VERSION` (runner line 177; `grep -c '\bVERSION\b'` = 1, the assignment itself, so no code path can observe the rename; a fortiori no `--regression` outcome can change):

```
validate_ho(kill, kind=head): OK
ho_witness_ok -> (True, 'head')          # counted as a VALID must-kill  (verified on bytes d43ead07 AND e5ba9cfe)
real v2 tool (9dbbce62…):     ACCEPT rc=0  TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```

**Should it be kill or invalid?** Invalid. The counter's own freeze language requires the witness to "demonstrate the fault"; a text diff demonstrates nothing, and the demonstrable fact is the opposite — the tool correctly PASSes the copy. As written, the copy is counted in `ho_kill_total`, the tool misses it, and `C1_R33_PASS=false` with a blameless tool. An author can void the claim with comment-level effort and no real defect.

**Q3b — ride-along (worse):** `edits` is a list, so a benign head edit can carry an arbitrary block mutation behind a `kind=head` witness:

```
edits = [VERSION rename (benign head), GUARD '!= nlegs' -> '< nlegs' (lethal block)]
set=accept, kind=head -> (True, 'head')     # VALID must-accept   (e5ba9cfe)
real v2 tool: KILL rc=1  TALLY_AUDIT: FAIL (… runtime=fail …)     # ho_accept miss -> claim voided
```

So `kind=head` lets a sealed author void the claim in **both** directions with zero fault demonstration.

**Exact counter patch (minimal, non-circular; mirrors tally-audit-v2's actual killable head surface):**

```python
# ho_witness_ok, replacing the kind=head branch (and adding set-awareness to the vector branch):
def ho_witness_ok(ho, pristine, mutated, work):
    w = ho.get('witness') or {}
    pb, mb = tally_block_of(pristine), tally_block_of(mutated)
    if w.get('kind') == 'head':
        if head_of(mutated) == head_of(pristine):
            return False, 'head'
        if tally_block_of(mutated) != pb:          # block edits must prove themselves, never ride
            return False, 'head-with-block-edit'
        if ho['set'] == 'kill':
            # v2's head check kills exactly: leg-var not assigned exactly once as bare `st_x=$?`
            # before the block, or an extra assignment to a leg var. Require the diff to touch that.
            A = re.compile(r'^[ \t]*(st_[A-Za-z0-9_]+)=\$\?[ \t]*$', re.M)
            X = re.compile(r'^[ \t]*(st_[A-Za-z0-9_]+)[ \t]*=', re.M)
            if (sorted(A.findall(head_of(pristine))) != sorted(A.findall(head_of(mutated)))
                    or sorted(X.findall(head_of(pristine))) != sorted(X.findall(head_of(mutated)))):
                return True, 'head-leg-assignment'
            return False, 'head-edit-cannot-kill'
        return True, 'head'
    vec = w.get('vector')
    if not vec:
        return False, 'no-witness'
    a = block_run(pb, vec, work)
    b = block_run(mb, vec, work)
    if ho['set'] == 'accept':
        return a == b and mutated != pristine, 'vector-equivalence'
    if pb == mb:
        return False, 'block-identical'
    return a != b, 'vector'
```

Rationale per branch: kill+head must touch a leg-assignment line (the only head surface `tally-audit-v2` can fail — an inert `VERSION` rename then gets the right `invalid` verdict); accept+head must leave the block untouched (kills Q3b ride-alongs; admits harness renames like round-32's B5, which v2 correctly passes); accept+vector flips to **equivalence** (`a == b`), making Q1b's cosmetic class satisfiable and lethal riding vectors impossible; kill+vector keeps `a != b` (with len==9 already enforced). Residual, declared out of scope: an accept+head edit that changes only `--regression`-visible head behavior (e.g. `BAND_KILLED`) is not observable by the counter's no-`--then-regression` scoring and stays valid; closing that would require running the copy's `--regression` (needs the sibling repos, outside the counter sandbox). Post-block-only equivalence edits are covered by the accept+vector branch (`pb == mb` ⇒ `a == b` trivially).

## Bounds, receipts, tooling record

- All execution in `/fast/scratch/hyaku/tameshi-r33-seats/tameshi-r33-w1-RevengerWitness-4/` (`exp/`, `exp/work*`, `out/`). The counter was **imported as a module** (no `main()`, no default mode, no `--write-controls`); the v2 tool ran only via `v1.run_tool` on scratch copies. Every cited command's exit code is captured: `out/witness-exp.rc` (0), `out/witness-exp2.rc` (0), plus the heredoc runs logged with `rc=$?` in `out/current-counter-check.stdout` and `out/final-semantics-check.stdout`.
- No tool installs (bwrap 0.13.1 already present; pacman untouched). No jj/git write commands anywhere; the lane was only read.
- Background job `bg_1191` (exp 2) completed on its own; no process killed.
- Untested residual: I did not run the amended counter's own `run_tool_sandboxed` end-to-end (my tool verdicts used the frozen round-32 runner of tools); its argv binds `/usr /bin /lib /lib64 /etc` read-only and was visually consistent with the repaired `block_run` that I did run.

**Confidence:** F0, Q1, Q2, Q3, Q3b observed by execution (commands and outputs above). "Every vector" for Q1 is execution on six spanning vectors plus a lexical argument. Patch behavior is `[INFERENCE]` from the cited code paths, not executed (counter edits are out of my bounds).
