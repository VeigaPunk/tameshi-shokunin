# MutCounterrelaxlen9 — C1 witness gate, `len(vec) != 9` rejection dropped

Round 34 / wave 1 / mutation-tester seat. Lane tip `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`.
Scratch `/fast/scratch/hyaku/tameshi-r34-seats/MutCounterrelaxlen9/` (all writes here + this file).
No tool installed/upgraded; no network; lane read-only (see §7). The counter was never run in
default mode — only imported as a module and its functions called (`block_run`,
`ho_witness_ok`, `validate_ho`, `apply_edits`, `run_tool_sandboxed`).

## Verdict (short)

| item | result |
|---|---|
| mutant | `validate_ho`: the two lines enforcing `len(witness.vector) == 9` deleted (counter lines 123-124) |
| assigned 8-case battery on mutant | **8/8 byte-identical to pristine** → **SURVIVED** |
| is the mutant a no-op? | **No** — proven behavior-bearing (§5): the same copy flips `INVALID` → certified on a 3-leg witness |
| which finding | **surviving semantics hole in the 8-case battery**, not a no-op mutant: none of the 8 probes carries a non-9 vector, so the battery has zero coverage of the length gate |
| could it have voided / falsely passed C1? | **Both** (§6): voids an accept copy the len-9 rule refuses and the tool KILLs; and can mint a "valid" must-accept whose witness never ran the tally loop (both runs crash identically) |

## 1. Setup and pins

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/MutCounterrelaxlen9
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin .../MutCounterrelaxlen9/lane       # clone_exit=0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach \
  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7                                          # checkout_exit=0
git -C .../lane rev-parse HEAD -> 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7          # rev_exit=0
git -C .../lane show 0b99d48…:tools/tally-audit-v2.py      > tool.py                 # show_tool_exit=0
git -C .../lane show 0b99d48…:tools/mutate-and-run.sh       > pristine.sh             # show_runner_exit=0
git -C .../lane show 0b99d48…:.ufo/evidence/round-33/c1/c1-measure.py > counter.py     # show_counter_exit=0
git -C .../lane show 0b99d48…:.ufo/evidence/round-32/c1-measure.py > ev/.ufo/evidence/round-32/c1-measure.py  # r32_exit=0
```

| artifact | sha256 | pin / expectation | match |
|---|---|---|---|
| `tool.py` (tally-audit-v2.py) | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | same | YES |
| `pristine.sh` (mutate-and-run.sh) | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | same | YES |
| `counter.py` = `.ufo/evidence/round-33/c1/c1-measure.py` | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | amendment-6 `f6b8868c…a07f28c` | YES |
| `.ufo/evidence/round-32/c1-measure.py` (import target) | `ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca` | tip blob | — |

The counter's module-level `import` of `../../round-32/c1-measure.py` (counter line 49-52) is why the
scratch tree mirrors `.ufo/evidence/round-33/c1/` + `.ufo/evidence/round-32/`; `ev/` holds pristine
counter bytes, `ev-mut/` the mutant.

## 2. The mutation (one semantic edit)

`diff -u ev/…/c1-measure.py ev-mut/…/c1-measure.py` (diff exit 1, expected):

```diff
@@ -120,8 +120,6 @@
             vec = w['vector']
             if not isinstance(vec, list) or not all(isinstance(x, int) and 0 <= x <= 255 for x in vec):
                 raise CounterError('witness.vector must be a list of ints 0..255')
-            if len(vec) != 9:
-                raise CounterError('witness.vector must name all 9 leg statuses (len %d)' % len(vec))
         elif w.get('kind') == 'head':
```

Before/after sha256 of the mutation target:

- pristine (also the restored/untouched copy): `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c`
- mutant: `1c299cf62c1dcc1a709a47313282b1dd850e50f0bb0633a12265a050f9d4bd50`

No other edit: `diff` shows one hunk, two deleted lines.

## 3. Probe battery — reconstruction and calibration

The lane commits only the *transcript* `.ufo/evidence/round-34/dev/witness-probes.{json,stdout}` — no
driver. `probe-battery.py` rebuilds the battery from the eight probe names and tuples recorded there:
each probe is a synthetic held-out object (`set` + `witness` + `edits` against `pristine.sh`) passed
through the counter's own `validate_ho` → `apply_edits` → `ho_witness_ok` (the counter's real flow,
lines 389-397). Calibration criterion: pristine bytes must reproduce the recorded transcript exactly.

```
python3 probe-battery.py ev/.ufo/evidence/round-33/c1/c1-measure.py pristine.sh work-base --json base.json \
  > base.stdout 2>base.stderr; echo "base_exit=$?"          # base_exit=0
diff <(head -10 base.stdout) …/.ufo/evidence/round-34/dev/witness-probes.stdout; echo $?   # transcript_diff_exit=0
```

`base.stdout` is byte-identical to the landed transcript (including the two fixture assertions):

```
VERSION in head: True
st_js line count: 1
Q1-comment-accept -> (True, 'vector-equivalence')
Q3-inert-head-kill -> (False, 'head-edit-cannot-kill')
Q3b-ridealong-accept -> (False, 'head-with-block-edit')
K-extra-leg-assign-kill -> (True, 'head-leg-assignment')
K-nonbare-leg-kill -> (True, 'head-leg-assignment')
A-inert-head-accept -> (True, 'head')
A-head-with-block -> (False, 'head-with-block-edit')
KV-block-identical -> (False, 'block-identical')
```

## 4. Mutant against the same 8 probes → SURVIVED

```
python3 probe-battery.py ev-mut/.ufo/evidence/round-33/c1/c1-measure.py pristine.sh work-mut --json mut.json \
  > mut.stdout 2>mut.stderr; echo "mut_exit=$?"             # mut_exit=0
diff <(head -10 mut.stdout) …/.ufo/evidence/round-34/dev/witness-probes.stdout; echo $?   # mut_vs_transcript_exit=0
```

All eight verdicts are unchanged, byte-for-byte. Structural reason: the battery's only two vector
witnesses (`Q1-comment-accept`, `KV-block-identical`) carry exactly 9 statuses, and the other six use
`kind=head`; the mutation is reachable **only** through `witness.vector` of length ≠ 9. The 8-case
battery therefore cannot see the deleted check — the mutant survives it by construction, not by luck.

## 5. The mutant is behavior-bearing (not a no-op)

Two probes outside the assigned eight (same machinery, different witness length), run on both trees:

```
python3 dual.py ev-mut work-dual-mut2 > dual-mut.json.stdout 2>&1     # dual_mut_exit=0
python3 dual.py ev     work-dual-base > dual-base.json.stdout 2>&1    # dual_base_exit=0
```

| copy (set) | witness | pristine counter | mutant counter | frozen tool on the copy |
|---|---|---|---|---|
| `D1-accept-delta-at-leg9` (accept) | `[0,0,0]` | `INVALID: …must name all 9 leg statuses (len 3)` | `(True, 'vector-equivalence')` | `KILL`, rc 1, `TALLY_AUDIT: FAIL (… runtime=fail …)` |
| same copy | `[0,0,0,0,0,0,0,0,2]` | `(False, 'vector-equivalence')` | `(False, 'vector-equivalence')` | (same copy) |
| `D3-accept-cosmetic-short-witness` (accept) | `[0,0,0]` | `INVALID: … (len 3)` | `(True, 'vector-equivalence')` | `ACCEPT`, rc 0, `TALLY_AUDIT: PASS` |
| `D2-kill-crash-path-only` (kill) | `[0,0,0]` | `INVALID: … (len 3)` | `(False, 'vector')` | `ACCEPT`, rc 0 |

The pristine and mutant verdicts differ on the short-vector rows: the deleted check is the only
difference between the trees, so the mutant is semantic, not cosmetic.

Mechanism, measured directly (same script, `ev-mut`):

```
block_run(tally_block, [0,0,0], work) -> (1, '')
block_run(tally_block, [0]*9,   work) -> (0, 'REGRESSION: PASS (cases=9 passed=9; ledger legs exact: …)')
```

With fewer than nine statuses `block_run` declares only a prefix of the leg variables (counter line
165), the tally loop then reads unset variables under `set -u` and the run dies with an empty first
line. A short-vector witness therefore compares **crash signatures**, never tally counts — exactly the
failure the round-33 amendment's line states ("shorter vectors only compare crash signatures, never
tally behavior", `corpus/knowledge/witness-equivalence-rule.md`).

## 6. Consequence if undetected: it can void C1, and it can falsely pass the witness condition

Counter flow (line numbers on the pinned counter): `validate_ho` 393 → `ho_witness_ok` 397 →
`ho_invalid += 1` 400 → set counting 403/405 → tool outcome 420/422 → the `ok` expression 426-427
(`ho_invalid == 0`, `ho_kt >= 8`, `ho_at >= 6`, `ho_k == ho_kt`, `ho_a == ho_at`).

**Void (blameless tool).** `D1` is an accept copy whose behaviour differs at leg 9. The amendment-6
rule refuses it on a 9-leg witness (`(False,'vector-equivalence')`, both trees); the mutant certifies
it as equivalent on a 3-leg witness. Closed in, the counter would count it as a valid must-accept
(`ho_at += 1`, line 405) and the frozen tool returns `KILL`/rc 1, so `ho_a` stays short and
`ho_a == ho_at` (line 427) fails → `C1_R33_PASS=false`. That is precisely the RevengerWitness Q3b
void the set-aware amendment was adopted to close, reopened by one deleted check.

**False pass (vacuous witness).** `D3` is a must-accept copy the tool PASSes. Under the mutant it is
certified `vector-equivalence` from two runs that both crashed identically — the witness demonstrates
nothing about the tally. On pristine bytes the same copy is `INVALID` (`ho_invalid += 1` → line 426
fails). The mutation thus converts a C1-failing sealed set into a PASS-eligible one whose "valid
must-accept" copies are certified without evidence; a PASS would attest `ho_at >= 6` valid copies
where some were never demonstrated.

Note the tool itself stays correct in both cases (`KILL` on `D1`, `PASS` on `D3`); only the counter's
certification changes. The deciding run at `c17e593b` used len-9 vectors and is unaffected.

## 7. Restoration / non-modification evidence

The mutation lived only in `ev-mut/.ufo/evidence/round-33/c1/c1-measure.py`; every frozen artifact was
extracted with `git show` into scratch and never written. Re-hashed after all runs:

- `tool.py` = `7b11ba25…b3598d10`, `pristine.sh` = `a7d3f2dd…dd912eb9`, `counter.py` =
  `f6b8868c…a07f28c` — unchanged, equal to the pins (sha256sum, exit 0).
- `ev/.ufo/evidence/round-33/c1/c1-measure.py` still `f6b8868c…a07f28c`; only the mutant copy differs.
- `lane/tools/tally-audit-v2.py` = `7b11ba25…` and `lane/tools/mutate-and-run.sh` = `a7d3f2dd…`
  (clone worktree equals the pins).
- `git -C lane rev-parse HEAD` → `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`; `git -C lane status
  --porcelain | wc -l` → `0` (worktree clean). No git/jj write command was run anywhere.

Evidence files (scratch): `base.stdout`, `mut.stdout`, `base.json`, `mut.json`, `cons-base.stdout`,
`cons-mut.stdout`, `dual-base.json.stdout`, `dual-mut.json.stdout`, plus drivers:

- `probe-battery.py` `9554f5816e82cdad2050b1a3e42e5db084f6ef4c853c57c7695988325a4e6324`
- `dual.py` `b4bc396f5aaaf02e318bcae52a5063461ef52bcdb23de46ce24c562d188fc292`
- `consequence.py` `42150e3af8e6e7e3aee91544fd53a7e8511849e3e083801c78b795faa2b2631c`

## 8. Finding for the corpus (observation, not a contract change)

The 8-case probe battery recorded at `.ufo/evidence/round-34/dev/witness-probes.stdout` has no
non-9-length vector probe, so the `len(vec) != 9` rejection — one of the amendment-6 clauses named in
`ho_witness_ok`'s comment (counter lines 186-190) — is unprobed. A ninth probe of the shape
`witness.vector = [0,0,0]` on an accept copy is sufficient to kill this mutant: it returns
`INVALID (… len 3)` on the landed counter and `(True,'vector-equivalence')` on the mutant (§5, `D1`/`D3`).
The landed claim is unaffected: the sealed set carries only len-9 vectors and `ho_invalid=0`.
