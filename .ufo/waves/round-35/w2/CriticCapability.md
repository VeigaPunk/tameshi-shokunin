# CriticCapability — round 35, wave 2

Review pin: `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`. Role: critic, not judge or integrator.

## Axes and scope

- **Calibration:** the capability sentence must not imply more than the executed demonstration.
- **Depth (C1):** distinguish finite, extracted-tally discrimination from correctness of the real regression runner.
- **Coverage / operability:** an executable audit can miss executed head/dispatch code; runnable is not whole-runner soundness.

Attacked: whether an audit PASS on a genuinely regressed runner copy can support a SCORECARD capability row. **Answer: not a whole-runner verification row. A strictly bounded repertoire sentence remains supportable only with its required passing round demonstration; it cannot rescue a failed frozen C1 predicate.** No admission or axis verdict is issued here.

## CRITICAL-1 — PASS does not establish real `--regression` correctness

This seat independently constructed and executed a dispatch-tail counterexample. It changes exactly the final dispatcher arm at pinned runner line 2078:

```bash
# old
  regression) run_regression ;;
# new
  regression) printf 'REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)\n'; exit 0 ;;
```

The copy now reports a successful nine-leg regression without invoking `run_regression`. A real CLI observation, not the audit's oracle, demonstrates the behavioral difference:

```bash
bash /fast/scratch/hyaku/tameshi-r35-w2/CriticCapability/pristine.sh --regression --target /fast/scratch/hyaku/tameshi-r35-w2/CriticCapability/never-used-target
# exit 64; stdout empty; stderr starts:
# mutate-and-run: --regression takes no --target/--defects/--suite/--label

bash /fast/scratch/hyaku/tameshi-r35-w2/CriticCapability/tail-bypass.sh --regression --target /fast/scratch/hyaku/tameshi-r35-w2/CriticCapability/never-used-target
# exit 0; stderr empty; FULL stdout:
# REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
```

Pristine stdout SHA256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (zero bytes).
Pristine stderr SHA256: `21b16f9e2340b83fc4acbdb3f0516fdcfe961ddfbef04d88182df18f88acd3fa`.
Mutant stdout SHA256: `53e6517344c54c60cb4b2ab90d3d4027e165c785aba459f00b56152e76996d31` (the displayed line, including final newline).

Yet the frozen v3 tool accepts the copy:

```bash
env PYTHONDONTWRITEBYTECODE=1 TMPDIR=/fast/scratch/hyaku/tameshi-r35-w2/CriticCapability python3 /fast/scratch/hyaku/tameshi-r35-w2/CriticCapability/tally-audit-v3.py --runner /fast/scratch/hyaku/tameshi-r35-w2/CriticCapability/tail-bypass.sh
# exit 0; FULL stdout:
CHECK head PASS legs=9
CHECK static PASS legs=9 operands=9 nlegs=9
CHECK runtime PASS vectors=30316 mismatched=0
CHECK harness PASS reference cases=9; faults rejected=34/34
TALLY_AUDIT: PASS (head=pass static=pass runtime=pass harness=pass)
```

Audit stdout SHA256: `46746e2b4740813443caccb89d80a96ae0c63d98f1def6b1fc3886d57c4e4e82`; stderr empty.
The exact subprocess argv/environment/exit are retained in `/fast/scratch/hyaku/tameshi-r35-w2/CriticCapability/audit-receipt.json` (SHA256 `3987e25181a8e19d26a78c7dfc6840036f8628ca6b2b1f786eb8a50ecc0f0bfd`).

Identity evidence:

| Artifact / compared span | SHA256 |
|---|---|
| `/fast/scratch/hyaku/tameshi-r35-w2/CriticCapability/pristine.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |
| `/fast/scratch/hyaku/tameshi-r35-w2/CriticCapability/tail-bypass.sh` | `33a53ffcb38d9219be098f9a5079e91800235913666cb49b4715f30a19de5abc` |
| `/fast/scratch/hyaku/tameshi-r35-w2/CriticCapability/tally-audit-v3.py` | `ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885` |
| `regression_body` output, identical pristine/copy, 6,879 bytes | `5da485753b03c3509794fc3f7e31e6fc1a97f2fd83a859dae5a93f16303da4e1` |
| `harness_section` output, identical pristine/copy, 2,924 bytes | `b7ac097dca167b7693c03978aad964cbd0749d6d566dec6466e8d37f3a81c311` |

Reproduction/capture commands executed by this seat:

```bash
python3 /fast/scratch/hyaku/tameshi-r35-w2/CriticCapability/capability-probe.py
# exit 0; creates the byte-pinned copies, asserts the single replacement, compares both spans,
# executes both CLI commands, and records every subprocess exit/output digest.
python3 /fast/scratch/hyaku/tameshi-r35-w2/CriticCapability/audit-once.py
# exit 0; invokes the audit exactly once, with the environment/argv displayed above.
```

Probe source SHA256: `2672ff4db094236fda67c7fd0003416d3b2816aaafd061840b27a70a417fd0b2`.
Probe receipt `/fast/scratch/hyaku/tameshi-r35-w2/CriticCapability/probe-receipt.json`: `25b7ff61063ff4040ce1ccb0941e496ff685f76ac4fb491cf7215583f4797ddf`.
Audit capture source SHA256: `ece5d67ff84f096bd1e9d397047da1fcda5287a1a6a7d5675abae175622f1f6e`.

This is a **fail-open coverage defect**, not a BOUND/fail-closed limitation. It falsifies the proposed strong sentence below, not by itself the finite deciding predicate.

## CRITICAL-2 — the strongest available witness also breaks head-integrity wording

Inherited execution evidence from AttackSpanTail was read and hashed, not rerun by this seat. Its stronger fixture is inside `run_regression`, immediately after the last status capture and before `local nlegs=`:

```bash
  for n in js kagi tsu mado checklist claims roundgate sourcescheck citecheck; do eval "st_$n=0"; done
```

This computes names rather than spelling literal `st_js` etc. The pinned tool's head/static/runtime/harness checks all PASS. The actual runner reports nine SETUP legs but then changes its aggregate from SETUP/exit 2 to PASS/exit 0. Thus the pinned docstring's broad “Catches out-of-block masking/overwrites of leg statuses” description is not an integrity guarantee (tool lines 67–70); the head check is syntactic, not execution of the head.

Exact recorded peer commands and exits, with full absolute paths expanded:

```bash
python3 /fast/scratch/hyaku/tameshi-r35-seats/AttackSpanTail/lane/tools/tally-audit-v3.py --runner /fast/scratch/hyaku/tameshi-r35-seats/AttackSpanTail/w2/work/m-maskall.sh
# exit 0; all four checks PASS; audit stdout SHA256 46746e2b4740813443caccb89d80a96ae0c63d98f1def6b1fc3886d57c4e4e82
bash /fast/scratch/hyaku/tameshi-r35-seats/AttackSpanTail/w2/work/pristine.sh --regression
# exit 2; REGRESSION: SETUP (cases=9 passed=0 cannot-verify=9)
bash /fast/scratch/hyaku/tameshi-r35-seats/AttackSpanTail/w2/work/m-maskall.sh --regression
# exit 0; REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
```

Bytes inspected and hashed by this seat (`sha256sum` over these absolute artifact paths exited 0):

| Artifact | SHA256 |
|---|---|
| `/fast/scratch/hyaku/tameshi-r35-seats/AttackSpanTail/w2/work/m-maskall.sh` | `bf932a36d3bee736ff9cd470c53fb891627aab239ccbf919c09bbbe8cc98c6a3` |
| `/fast/scratch/hyaku/tameshi-r35-seats/AttackSpanTail/w2/out/pin-m-maskall.txt` | `46746e2b4740813443caccb89d80a96ae0c63d98f1def6b1fc3886d57c4e4e82` |
| `/fast/scratch/hyaku/tameshi-r35-seats/AttackSpanTail/w2/out/e2e-rc.txt` | `d8f342a7db36f88c6844b5a5e7a35745544e479a7f9778ba4cd484e6a257ba26` |
| `/fast/scratch/hyaku/tameshi-r35-seats/AttackSpanTail/w2/out/e2e-pristine-default.txt` | `68dbf4b01e801cb89fcde94516e76ce3b55962dbc4a8869c8b834d9cec40228a` |
| `/fast/scratch/hyaku/tameshi-r35-seats/AttackSpanTail/w2/out/e2e-m-maskall-default.txt` | `4306c64015f030da421262baeeae98aea37c28aecf86ae5bda40387c3ae45f66` |
| `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-35/w2/AttackSpanTail.md` | `6b29bba76785515118a68e9dadc97426124e51d234b1f9321a123fe8b14e98a4` |

The peer report also records all four real CLI flag combinations and mixed-vector FAIL→PASS witnesses (§§2,6). The default CLI pair above is already sufficient: unavailable verification must not become a successful regression. No claim here depends on its live, uncommitted successor-tool tests.

## What I could NOT break, and what this review does not prove

1. **The narrow extraction boundary is real, not an omitted post-tally slice inside the function.** At the pin, the tool's `regression_body`, `tally_block`, and `harness_section` are at lines 196–244 and 619–635; the audit uses those spans at 683–705. `tally_block` includes everything from `local nlegs=` to the function's closing brace. My dispatch change is after that function; the peer's status change is before the block. The identical-span hashes above explain why this does not contradict `runtime ... mismatched=0`.
2. **A4's exact old root-value specimen is rejected.** Inspected peer command:

   ```bash
   python3 /fast/scratch/hyaku/tameshi-r35-seats/AttackSpanTail/lane/tools/tally-audit-v3.py --runner /fast/scratch/hyaku/tameshi-r35-seats/AttackSpanTail/w2/work/m-rootkeyed.sh
   # exit 1; runtime alone FAIL; mismatched=15158; first failure uses a real /tmp/tameshi-r4-2-regression.* root
   ```

   Specimen SHA256 `80a4fd7c9e987ec75ef833b0ac75c03e74fc21cdafbbe061b7d2df44a03b9b6e`; retained output `/fast/scratch/hyaku/tameshi-r35-seats/AttackSpanTail/w2/out/v3-m-rootkeyed.txt`, SHA256 `7a649b8b6cbb6d0bded23ba9e83ade8b97231cf1ab9ba208734e7fb7ec1679ec`. This is a bounded negative, not proof about every root-sensitive construction.
3. **An in-span, second-stdout-line defect is rejected.** Inspected peer command:

   ```bash
   python3 /fast/scratch/hyaku/tameshi-r35-seats/AttackSpanTail/lane/tools/tally-audit-v3.py --runner /fast/scratch/hyaku/tameshi-r35-seats/AttackSpanTail/w2/work/m-inspan.sh
   # exit 1; runtime alone FAIL; mismatched=10; first failure cfg(0,0): WORKDIR “removed” versus “kept”
   ```

   Specimen SHA256 `4f1d07ba6a9e8e26d6588b4d9a042ef3198ffdc86f840d414d9468991bd918ed`; output `/fast/scratch/hyaku/tameshi-r35-seats/AttackSpanTail/w2/out/v3-m-inspan.txt`, SHA256 `4bd4db161ad49ff239b65ed5cd2282d4650a5e62879ca514188ae46ec6a67622`.
4. **No deciding C1 result was established or falsified here.** The frozen counter defines specimen truth by extracted block behavior (lines 8–15, 132–153, 204–217, 285–310), not whole CLI behavior. The two constructions above can be invisible to that truth function while being real runner regressions. This shared *scope* of tool and counter is not independent evidence of whole-runner soundness. I did not run the default C1 counter, reclassify either construction as a sealed kill, change the frozen rule, or assert that its deciding receipt passed/failed.
5. **No C2 result is inferred.** Its six classes are enumerated at contract lines 44–59. Zero m1–m6 does not measure the semantic breadth of a new capability sentence. No C2 rerun or native judge invocation was performed.

## Exact capability sentences and smallest safe correction

**Sentence a successful, judge-supported round-35 row may carry, without enlarging the measured claim:**

> `tally-audit-v3` runs syntactic head/static consistency checks, finite four-(auto,KEEP)-configuration exit/full-stdout tests of the extracted regression tally with the real auto-root template, and a fixed fault panel against the extracted tally selftest; its round-35 deciding receipt establishes discrimination only for its named specimens, not correctness of whole-runner execution or detection of pre-tally/head and dispatch-tail regressions.

The evidence column must identify the actual deciding revision, frozen tool/counter hashes, receipt and observed specimen counts. This sentence is **conditional**, not a claim that that demonstration has happened. A false or absent frozen deciding predicate cannot be replaced after data by “the smaller extracted checker runs” to earn the promised successful C1 row. The existing finite v2 row at pinned SCORECARD lines 1653–1657 is historical fixture evidence, not whole-runner provenance and not a v3 demonstration.

**Sentence the row may not carry:**

> A PASS from `tally-audit-v3` proves the real mutation runner has no `--regression` regression in any of its four configurations, including head and tail, and rejects every behaviorally divergent runner copy.

Smallest safe correction now: preserve the freeze and deciding rule; keep the repertoire description explicitly specimen-/span-limited and disclose these fail-open counterexamples beside it. No global “head masking closed”, “runner verified”, or saturation/retirement inference follows from four configuration labels or zero C2 mismatches. This is a calibration correction, not a code change or admission by this critic.

If the intended capability really is whole-runner soundness, wordsmithing is not a repair: a future frozen design must account for the real pre-tally execution and dispatch path in both the tool and its independent behavioral truth. Merely teaching both extractors to ignore the same region retains the correlated blind spot. Accepting a broader guarantee despite the demonstrated false green is a trade/scope substitution for the canonical Rust judge to reject, not a BOUND/fail-closed result. No separate HYGIENE finding is needed to explain it.

## Pin/provenance and scope receipts

The source claims above refer to the dispatch pin, not mutable wave-2 working-tree successors. These exact read-only commands exited 0:

```bash
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:tools/mutate-and-run.sh
# stdout SHA256 a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:tools/tally-audit-v3.py
# stdout SHA256 ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:.ufo/evidence/round-35/contract.json | sha256sum
# a9eb2b97226ad192352f9da8cc32f3f719db22a93f14355a5e2d1306cea027c0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:.ufo/evidence/round-35/c1/c1-measure.py | sha256sum
# 515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b:SCORECARD.md | sha256sum
# cbea24c85074baac8904cab3b2937c6e93634431c9ee408b711fc58e66e7961f
```

The first two blob reads were executed inside the probe with GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE removed from its child environment; their exact argv/exits are in the probe receipt. The last three pipelines were directly executed as displayed. The required background contract, wave-1 root/provenance reports, round-34 Holds and v3 docstring were read before probing. A5 was not attacked or declared closed by this seat.

No clone/checkout was made: the stronger no-mutating-git/no-`.git`-write bound was honored through revision-addressed reads and isolated plain-file copies. All this seat's scratch writes are under `/fast/scratch/hyaku/tameshi-r35-w2/CriticCapability/`; only this report was written under the project tree. No frozen artifact, sibling report, lane source, state, route or judge input was edited. No subagent was dispatched. No installs/upgrades or `pacman` transaction occurred.
