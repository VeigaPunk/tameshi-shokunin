# ReviewQuality8182 — QUALITY criteria 81 and 82 (round 42, wave 2)

Seat: L1Tameshi42.ReviewQuality8182 (reviewer, read-only). Date 2026-10-25.
Attacked: `corpus/QUALITY.md:1001-1046` (criteria 81 and 82, landed in `5f739ac`).
Tools installed or updated: none.

## Falsifiers as written (LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin)

Criterion 81 (`corpus/QUALITY.md:1018-1021`):

```
python3 .ufo/evidence/round-42/calibration/measure.py --lane LANE \
  --rev c77c2b7e64d2e356381441ecf94abac03e984606 --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f
MISMATCH m10 .ufo/waves/round-41/residual/receipt.json asserts present=false for .ufo/waves/round-41/residual/ResidualReceipts.md; tree says true
MISMATCH records 3 of 6 round-41/42 records present
C1_R42: self_pin=1 m6=0 m7=0 m8=0 m10=1 m11=0 total=1 records=3 sources_rows=109 rev=c77c2b7e… freeze=322b5cd3… C1_R42_PASS=false
exit=1
```

This matches the stated result: `C1_R42_PASS=false`, exit 1.

Criterion 82 (`corpus/QUALITY.md:1042-1046`):

```
printf 'raise SystemExit("crash")\n' > /tmp/crash-probe.py
python3 .ufo/evidence/round-42/census/measure.py --lane LANE --rev 322b5cd3… --freeze 322b5cd3… --probe-mutant /tmp/crash-probe.py
PROBE outcome=runtime_error detail=F01_attr_scratch exit=1 ['crash']
C2_R42_CONTROL: probe_outcome=runtime_error rev=322b5cd3… freeze=322b5cd3…
exit=0
```

This matches the stated result: `probe_outcome=runtime_error`, not `killed`.

PRE-RUN (labelled, allowed rev): the C1 counter at `--rev a21845f5…` printed `m10=0 total=0 records=6 C1_R42_PASS=true`, exit 0. The C1 counter's `--selftest` printed `cases=9 failed=0`, including the four T2 supersede cases. The C2 counter has no `--selftest` flag (argparse rejected it).

## Findings by severity

### F1 (medium, calibration, criterion 82): "a non-zero exit is a run error" is broader than the lane rule it cites

- `corpus/QUALITY.md:1025-1029` applies the rule to "when the lane mutates its own tools": a mutant counts as killed only if the run finishes with parseable output, and "A non-zero exit … is a run error". It then calls this "the lane's own verdict rule (`SKILL.md:208-209`)".
- `SKILL.md:208-209` says "crash before the summary" is Inconclusive. It does not say any non-zero exit is.
- `SKILL.md:200-204` rules the other way for tools whose expected exit is 1. A kill "kept the exit code (… `got exit=1` like the expected one)" and is still a kill: "Adjudicate exit AND token/verdict; never exit alone."
- Probe evidence (scratch, deleted): I took v4 (`git show a21845f:tools/write-path-census-v4.py`) and prepended an atexit hook that forces exit 1. Its output stayed correct (`{"file": …, "sites": []}`, exit=1). The counter scored it `PROBE outcome=runtime_error detail=F01_attr_scratch exit=1`.
- For v4 this is right, because its contract is exit 0. As a lane-wide rule it misclassifies tools whose contract includes exit 1. Example: the census counter's own docstring says "Exit 0 iff the predicate is true; 1 if false" (`.ufo/evidence/round-42/census/measure.py:46-49`). Mutating such a tool would turn every real kill into a run error.
- Suggested wording for a later round: "an exit outside the tool's declared exit contract".

### F2 (medium, depth, criterion 81): two of the rule's clauses have no check a later round can fail

- Criterion 81 requires the receipt to be "written after the last write it describes", and requires the fix to be "not an in-place rewrite of closed-round evidence" (`corpus/QUALITY.md:1003-1008`). The C1 counter's m10 class compares assertions against the tree at REV only (`calibration/measure.py:187-222`).
- Scratch clone at `a21845f`, case B: I deleted the superseding receipt and rewrote `.ufo/waves/round-41/residual/receipt.json` in place (`present: false` → `true`). Result: `m10=0`. The only failures were two incidental `m8` citations of the deleted file.
- An in-place rewrite that keeps any superseding file in the tree would therefore pass m10 entirely. I did not run that combination; it follows from the `receipt_audit` code.
- Only the clause "contradicted and not superseded" fails mechanically. Case A (superseding receipt deleted) gave `m10=1`, `PASS=false`. The ordering and in-place clauses are prose-only.

### F3 (low, depth, criterion 81): the falsifier does not isolate the stale receipt at the base

- The criterion says the command fails "at the base, where the stale receipt is not yet superseded". But at the base it also fails `records 3 of 6`.
- Scratch case E: base plus the stale receipt repaired in place gave `m10=0 total=0 records=3 C1_R42_PASS=false`, exit 1. The output is identical even with no m10 instance at all.
- The criterion-specific signal is `m10=1`, not `C1_R42_PASS=false` or the exit code. The text should name `m10=1`.

### F4 (low, depth, criterion 82): the falsifier exits 0 on every outcome and tests only the frozen round-42 counter

- In probe mode, `census/measure.py:398-401` prints the outcome and returns 0. The scratch probes gave `survived` (v4 itself), `killed` (`{"sites": []}`), and `runtime_error` (garbage stdout; a Traceback on stderr with exit 0; a crash on F01 only). All exited 0.
- So the falsifier "fails" only through its stdout text.
- It also runs at the pinned `322b5cd` with the pinned counter, which makes it a regression check on round-42's oracle. A later round with its own oracle is not exercised by it. For later rounds, the failable part is "a kill count must say which oracle produced it" (`:1032-1033`), and that can only be checked by reading.
- The oracle itself is not vacuous: all three outcomes are reachable.

### F5 (info, calibration, criterion 82): Stryker agrees only on runtime errors; the criterion is silent on timeouts

- The Stryker snapshot (`.ufo/evidence/round-42/sources/stryker-mutant-states.html`) says a timeout "is counted as 'detected'".
- The counter makes a timeout `runtime_error` (`census/measure.py:232-233`), and `SKILL.md:208` makes it Inconclusive.
- Criterion 82 only covers crashes, so its Stryker citation stays true. The gap is recorded in `corpus/lessons/round-42.md:163-165`. This is not a misquote.

## Citation check (criterion 82, PIT and Stryker): correct

- Snapshot digests: `sha256sum -c .ufo/evidence/round-42/sources/sha256.txt` returns OK for all five files. PIT master at fetch was `f7fe5adf…` (`opened-at.txt`).
- Stryker (S001, `corpus/SOURCES.md:12`): the quote "is not represented in your mutation score" appears twice in the snapshot, under "Runtime error" and "Compile error". It is located, ≤25 words, accessed 2026-10-25.
- PIT (S158, `corpus/SOURCES.md:128`): `pit-DetectionStatus.java:63` reads `RUN_ERROR(true),`. The flag is stored in `detected` (`:80-81`) and returned by `isDetected()` (`:108-110`). `getForErrorExitCode` (`:91-99`) maps any exit code other than OOM or timeout to `RUN_ERROR`.
- So "its code scores `RUN_ERROR` as detected" holds at the enum level.
- [INFERENCE] The snapshot does not show that PIT's aggregate mutation score uses `isDetected()`; the criterion claims "code", not "score".
- PIT's docs page (S155, `pit-basic-concepts.html`) only says a run error "means something went wrong". Grounding the claim in S158 rather than S155 is correct.
- The contract's post-freeze amendment P1 (`contract.json` `post_freeze_amendments[0]`) withdraws "PIT Run error" as support, with `rule_changed: false`.
- The pinned counter docstring (`census/measure.py:19-21`) still says "PIT's 'Run error' and Stryker's RuntimeError, which neither tool counts as a kill". This is disclosed at `QUALITY.md:1036-1037` and in lesson row `:115`.

## Does each criterion state a rule a later round can fail?

- Criterion 81: yes, partly. The "contradicted and unsuperseded" clause fails on `m10` (case A). The "written after" and "no in-place rewrite" clauses cannot fail mechanically (F2), and the base falsifier is overdetermined (F3). The known limits (content-blind, `present`-key-only) are recorded at `corpus/lessons/round-42.md:127-136`. Case C (superseded path truncated to 0 bytes) gave `m10=0 PASS=true`, which confirms the recorded content-blindness. Case D (superseding key renamed to `report_exists`) gave `m10=1`, so the supersede is not counted.
- Criterion 82: yes, by reading only. "Cite the tool whose rule you follow" and "a kill count must say which oracle" are checkable in records. The command checks only the frozen counter (F4), and the exit rule is too broad as a lane-wide rule (F1).

## Residual risk and verification gaps

- No timeout probe was run (it would take 60 s per case). The timeout → `runtime_error` path is read from code at `census/measure.py:232-233` only.
- The scratch clone `/tmp/tameshi-r42w2-ReviewQuality8182-c1` and the probe dir `…-c2` are deleted. `/tmp/crash-probe.py` is left in place; the criterion's command re-creates it.
- No lane write except this file. The untracked `dispatch-w2.json`, `spec-w2.json` and `w2/` in the lane are not mine.
- Tool anomaly: the Read tool refused 30–185-line ranges of the two ~17–20 KB counters with "exceeds 100000 characters". I read them with `sed -n` instead.

Verdict: SURVIVES. Both falsifiers print what the criteria state, and the PIT and Stryker citations are accurate against the snapshots. Two medium wording and depth defects remain: F1, the over-broad non-zero-exit rule; and F2, the ordering and in-place clauses have no check.
