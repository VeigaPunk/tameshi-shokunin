# ReviewCounterA — round 33 wave 1, C1 counter adversarial review

Item: tameshi-r33-w1-ReviewCounterA-3. Scope: frozen C1 counter
`.ufo/evidence/round-33/c1/c1-measure.py` vs `contract.json` C1, at lane commit
f6d8a891 (working tree bytes equal the amendment blob `edd8fbb0…`, see Operational note).
All experiments ran inside `/fast/scratch/hyaku/tameshi-r33-seats/ReviewCounterA/`
(sandbox git clone + bwrap runs). **No counter run ever touched lane bytes**; default-mode
runs were executed only against my own scratch clone with forged states. No tools were
installed (stdlib + bwrap + git only).

Verdict: **defects found — the counter as frozen is not sound.** One high-severity
operational break (witness runner cannot execute in its own sandbox), one medium-high
controls-gate forgery, one medium witness-validation gap, several low-fidelity items.

---

## Findings by severity

### 1. HIGH — `block_run` cannot execute inside its own bwrap sandbox (`timeout` is unresolvable), so every vector-witness sealed copy is `ho_invalid`; C1 structurally cannot PASS with the mandated sealed set

`c1-measure.py:172-196` builds the bwrap command as
`[bwrap --unshare-all --die-with-parent --new-session --clearenv
  --ro-bind <script> /x.sh --bind <d> /w --chdir /w --dev /dev --proc /proc,
  timeout, 60, bash, /x.sh]`.

`--clearenv` wipes `PATH` and the sandbox root contains no `/usr`/`/bin` bind, so the
container init `timeout` cannot be exec'd. Reproduction with the exact command (same args,
copy of the frozen script template):

```
exact counter cmd: rc=1 stdout='' stderr='bwrap: execvp timeout: No such file or directory'
```

Consequence: every vector-witness check degenerates to `(1,'') == (1,'')` for pristine and
mutated, i.e. `ho_witness_ok` always returns False → the held-out loop raises
`CounterError('witness does not demonstrate the fault')` → `ho_invalid += 1` for every
sealed copy carrying a vector witness. Kill copies necessarily exercise the tally block, so
their seals require vector witnesses (kind=head is only for head edits) → `ho_invalid > 0`
and/or `ho_kt < 8` → `C1_R33_PASS=false` for any measurement containing vector-witness
seals. Wave-2 measurement would fail even if the tool were perfect.

(Attempted fix in scratch — adding `--ro-bind /usr /usr` + `--setenv PATH /usr/bin:/bin` —
still ENOENT on `timeout`; the minimal robust fix is to bind the needed runtime and invoke
absolute paths, e.g. `--ro-bind /usr /usr --ro-bind /lib /lib --ro-bind /lib64 /lib64
--setenv PATH /usr/bin:/bin /usr/bin/timeout 60 /usr/bin/bash /x.sh`.)

### 2. MEDIUM-HIGH — the controls gate accepts a hand-forged receipt; `all_false` is self-attested and never re-verified

`c1-measure.py:262-275`: `controls_ok` requires only
`receipt.get('counter_sha256') == sha256(git show REV:SELF_PATH)` and
`receipt.get('all_false') is True`. No control rows are checked, no control tool existence
or re-scoring happens at measurement time, and the receipt carries no proof it was produced
by `--write-controls`.

Demonstrated (scratch clone): committed a hand-written receipt
`.ufo/evidence/round-33/c1/controls-receipt.json`

```
{"counter": "c1-measure.py", "counter_sha256": "<sha of counter blob at REV>",
 "all_false": true, "controls": [], "note": "hand-forged, no controls ever ran"}
```

and ran the counter default mode at that REV:

```
C1_R33: tool_present=1 tool_sha_ok=0 runner_sha_ok=1 controls_ok=1(ok) …
```

(exit 1 overall only because I tampered the tool to skip scoring; the gate itself passed).
So requirement (a) holds: a committed receipt can name the counter sha256 while recording
`all_false=true` without controls having failed. The gate is a version-binding check, not
an honesty check.

Counter-evidence (behavior is correct for version skew): at a rev whose counter blob is the
frozen `7ff776df…` with a receipt naming the amended `edd8fbb…`, the gate refuses:

```
C1_R33: … controls_ok=0(sha-or-allfalse-mismatch) …
```

So the routed repair "counter edit invalidates the receipt on its own" works; the forgery
path is the self-attested `all_false` with no re-derivation. Recommendation: default mode
should re-score the receipt's recorded control tools against the *receipt-recorded seed*
(`receipt['seed']`) at measurement time and recompute `all_false`; barring that, the gate
should at least require a non-empty `controls` list whose rows exist at REV and whose
`predicate_pass` values are all false — though re-scoring is the only sound fix.

### 3. MEDIUM — witness vector length is not validated (lengths 1, 3, 12 accepted), so the witness interface need not be the runner's 9-status interface

`validate_ho` (`c1-measure.py:111-116`) enforces only ints in 0..255; `ho_witness_ok`
(`:171-182`) runs the vector as-is. Demonstrated:

```
  vector len 3   -> VALID
  vector len 12  -> VALID
```

Contract wording fixes a witness as a status vector on which the mutated tally block's
exit+first line differ — with the 9 runner statuses being the real interface. A short
vector both (a) under-exercises the block and (b) changes bash semantics (`set -u` +
undeclared `st_*` locals). Recommend `len(vec) == 9` (exactly the 9 `st_*` names in
`block_run`). My attempt to build a full exploit (an edit that only changes behavior when
`$# < 9`, so witnessed at length 1 but identical at 9 args) was blocked by finding 1 —
the block never runs at all; the validation gap itself is confirmed.

### 4. LOW-MEDIUM — witness authenticity is author-attestable; head-witness precedence; block text is interpolated raw into bash

- `ho_witness_ok` checks `w.get('kind') == 'head'` first, so a witness carrying both
  `kind=head` and a `vector` (accepted by `validate_ho`) takes the head path; inconsistent
  dual-schema looseness.
- The tally `block` is interpolated verbatim into a bash script (`block_run`), so injected
  `new` text can emit a fake `RC<TAB>…` line and force `a != b` for any mutation pair once
  finding 1 is fixed — i.e. the witness proves only that the block text differs on some
  sandboxed run, not that the intended fault manifests at the runner's real interface.
  Contained by bwrap (no host access), but combined with finding 6 it weakens
  "witness demonstrates the fault" to an attestation.
- `kind=head` witnesses compare only head text; a dead comment edit in the head validates an
  accept copy with zero behavioral change (contract-scribed, noted as residual).

### 5. LOW — `NAME_RE` is dead code; docstring overstates routed repair 1

`NAME_RE` is defined (`:51`) and claimed in the docstring ("witness.loop names are
validated… before any bash use") but never referenced; the witness schema has no loop field
and `block_run` uses hardcoded names, so there is no name-injection surface today. The
docstring should be corrected, not the code.

Verified working (routed repairs 2-3): non-string witness → `CounterError('witness must be
an object')` → caught → `ho_invalid` (no crash); int witness → same; vector out of 0..255
→ `CounterError`; held-out discovery is recursive (`git ls-tree -r`, any depth).

### 6. LOW — contract-vs-implementation fidelity: `run_tool` runs the tool without the bwrap sandbox

Contract predicate: tool runs "in a bwrap sandbox (only the tool and one runner copy
visible, stdout only)". `v1.run_tool` (round-32 `c1-measure.py:159-187`, reused by
`score_tool`) runs `python3 -I <tool> --runner <copy>` directly with a minimal env/cwd
only — no bwrap, and the work dir (containing all sibling copies) is visible to the tool.
Given the tool bytes are sha-pinned this is not exploitable by the reviewed tool, but the
counter verifies a weaker condition than the contract sentence states.

### 7. LOW — panel composition is seed-random; measurement seed is not tied to the receipt seed

`public_panel` draws the 9 generated kill and 2 generated accept copies from
`random.Random(seed)`; default `seed = secrets.token_hex(8)` → the "18 public copies" are
not a fixed set across runs (counts are constant: 18/8). The controls receipt records its
seed but default measurement draws a fresh one, so controls and measurement evaluate
different panels. This also leaves seed-shopping as a procedural (not technical) risk under
the "first full default-mode run decides" kill rule. Recommendation: measurement should
default to `receipt['seed']` when present.

### 8. OPERATIONAL (for L1) — measurement REV must be on the amended line; amendment 1 must be disclosed

- Lane git HEAD (f6d8a89, "freeze …") holds counter blob `7ff776df…`; the working tree and
  the committed amendment `27902a1` hold blob `edd8fbb…` (only `--write-controls`/
  `--receipt` arg plumbing differs; predicate/label/rule unchanged). Receipts written now
  (from the working tree) name `edd8fbb…`, so measurement at REV = f6d8a89 (or any rev
  whose counter blob is `7ff776df…`) will refuse with `controls_ok=0(sha-or-allfalse-mismatch)`
  (demonstrated). L1 must measure at a REV ≥ 27902a1 line and include amendment 1 in the
  round-33 lesson disclosure per the kill rule.
- Also confirmed: counter and tool A commits are both f6d8a89; r32 held-out original A is
  24a5a5b (pre-freeze baseline).

### 9. LOW — freeze check is a commit-time proxy; rename-in of pre-authored content passes

Attempted bypass (d): `git mv` of a round-32 held-out file into
`.ufo/evidence/round-33/heldout/`. With pathspec-limited `git log --diff-filter=A` (what
`adding_commit` runs), the move commit itself is reported as the A commit for the new path
(rename detection is not applied to pathspec-limited log), so `adding_commit` returns a
post-freeze sha and the ancestor check passes. Empty-heldout-at-freeze history means no
pre-freeze path can gain a pre-freeze A for a round-33 heldout path; but the check cannot
distinguish content authored before the freeze from content committed after — it verifies
only commit-graph position (which is exactly the contract's "adding-commit descendant of
both" wording, so this is a residual-risk note, not a contract violation). Fresh-add
control returned the correct current A sha; frozen counter/tool A = f6d8a89.

---

## Verification gaps

- Full C1 measurement (public panel + held-out verdicts) was not run: my item forbids
  default-mode runs on lane bytes, and the tool runs are too slow to complete inside the
  time box; verdict-level behavior is delegated to the tool reviewer. Finding 1 makes the
  question moot until fixed.
- The witness-length exploit in 3 could not be demonstrated end-to-end because finding 1
  prevents any block run.
- `--write-controls` path was not exercised (control writing is other seats' item); the
  frozen version's CLI defect is covered by amendment 1 (see finding 8).
