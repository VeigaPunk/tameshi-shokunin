# RR12b — cold-read, SKILL.md lines 1740–1788 (round 16, wave 2)

Verdict on what I attacked: **holds.** The seventh mutation case (kumitate
`scripts/round-gate.mjs` @ 364f1d5, 10 mutants, 5/10 killed, 10/10 predictions)
reproduces exactly, and the survivor-probe rule executes as written: pristine
exit 0, discriminating mutants exit 1.

Page verified: `SKILL.md` @ c699c8c36d6e4eca4b796b81a8247904aa145ec8, sha256
`3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4` (matches the
interface pin). Scratch: `/tmp/tameshi-r16w2-RR12b` (+ `/tmp/tameshi-r16-rg.kLgTOh`).

## Section 1740 `## Seventh recorded case and full-page cold-read — round 16`

Mixed: record (case result, cold-read paragraph) + instruction (reproduce
block, four rules). Executed/anchored all.

### Reproduce block — executed verbatim (exit 0)

```sh
git -C ~/Projects/shokunin/kumitate-shokunin show 364f1d5…:scripts/round-gate.mjs > $W/round-gate.mjs
sha256sum → f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9   # == predicted pin
bash tools/mutate-and-run.sh --target $W/round-gate.mjs --defects $E/round-gate.defects.spec \
  --suite "$(cat $E/suite.txt)" --label js-round-gate --workdir $W/work
```

Lane tool run from a `/tmp` extraction of commit `c699c8c` (per lane contract);
kumitate read-only. Observed output:

```
CONTROL: GREEN (exit=0 … pristine-sha256=f890e277…a834d3e9)
DEFECT A1: KILLED · A3: KILLED · B1: KILLED · E3: KILLED · C1060: KILLED
DEFECT C1059: SURVIVED · A2: SURVIVED · B2: SURVIVED · CKIND: SURVIVED · E1: SURVIVED
MUTATE_RESTORE: OK (target-sha256 before=…d3e9 after=…d3e9)
MUTATE: DONE (target=js-round-gate defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)
```

Matches the recorded table 10/10 (kill-aimed all killed, hole-aimed all
survived), `inconclusive=0`, `MUTATE_RESTORE: OK`, tool exit 0. One divergence
from the case note, informational only: the sweep note records tool sha256
`75ed934d…adc5` (r10-2); the pinned commit now carries `89722ddb…5594`
(ledger-embedded r16 build, sha matches `runner-regression.txt`'s
REGRESSION_TOOL line). Behavior identical.

### Rule 1 (env sandbox) — observed in action

`suite.txt` runs `env -i PATH=… HOME=$h/home TMPDIR=$h/tmp LC_ALL=C
GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES=$h node $MUTANT --selftest`. My
shell exports nothing repo-facing; the per-defect `sandbox-$DEFECT_ID` dirs
appear in the workdir. Control 60/60 green — the sentinel design works.

### Rule 2 (grade by exit) — anchored

Case note §0: 8 pristine runs exit 0 with differing stdout (mkdtemp suffix);
runner verdict lines grade `exit=0/1` only. Reproduce block's own expectation
is exit-shaped ("CONTROL: GREEN … killed=5"), consistent.

### Rule 3 (interval edge) — measured

C1059 (`REPORT_MIN_BYTES` 1024→1059) SURVIVED exit 0; C1060 (→1060) KILLED
exit 1 — `ROUND_GATE_SELFTEST: 58/60` vs pristine 60/60; the 1059-byte r8
fixture is the only casualty (`REPORT_THIN` at round-gate.mjs:345). The edge of
the projected [26,1059] interval is exactly as recorded.

### Rule 4 (survivor probe) — executed

`probes.mjs` (15 probes) with `GATE=` selecting the artifact, `FXROOT=` in my
scratch:

- Pristine (`$W/work/pristine.round-gate.mjs`, sha == pin): all four named
  probes P1/P1b/P6/P9 exit 0; full run = 15/15 `ALL ASSERTIONS PASS`, exit 0.
- `mutant-A2`: P1 exit 1 (assertion "stdout is exactly one FAIL-CLOSED line
  with full detail tail" fails on the `detail: ` prefix — observed
  `ROUND_GATE: FAIL-CLOSED (REPORTS_DIR_MISSING) detail: --reports-dir …`),
  P1b exit 1; P6/P9 exit 0 (not its discriminator).
- `mutant-B2`: P6 exit 1; P1/P1b/P9 exit 0.
- `mutant-E1`: P9 exit 1; P1/P1b/P6 exit 0.

Each survivor's probe kills its own mutant and only its own — the record's
pristine-0/mutant-1 claim and the probe-id table in the case note hold.

### Record anchors re-checked

- Blob pin: `git show 364f1d5:scripts/round-gate.mjs | sha256sum` →
  `f890e277…a834d3e9` ✓ (also the sweep's MUTATE_TARGET/pristine sha).
- Spec sha `e99b87eb…11c4` == `predictions.json` pin == sweep `spec.copy` ✓.
- Pre-registration: `e69b488` committer 2026-10-20T10:39:59-03:00, ancestor of
  `c699c8c`, predictions committed before sweep 13:40:15Z ✓.
- Retained `sweep/results.tsv` and `sweep.log` match my measured table
  row-for-row; retained `runner-regression.txt` shows `REGRESSION_CASE
  js-round-gate: PASS`, `REGRESSION: PASS (cases=7 …)` ✓.
- Line anchors on the pinned blob: :163 envSrc branch, :167
  `REPORT_MIN_BYTES = 1024`, :171/:1488 `FINDING_KINDS` (only two readers —
  the CKIND "no other reader" claim holds), :175 enum row, :527 tracked
  failClosed, :535 `filed.length < 2`, :575–576 tracked verdict tail, :617
  FAIL-CLOSED write, :647 main-path failClosed, :677 audit verdict line ✓.
- Counting command: `python3 .ufo/evidence/round-16/measure.py --rev c699c8c`
  → exit 0; `recorded_cases=7` (`js-round-gate` present), `depth_score=7`,
  `coldread.box3_full_page=false` with `ledger_present=false` — expected at
  this commit, since the wave-2 ledger is being assembled now; the claim is
  about the assembled ledger, not this rev. SHONEN marks `~,~,~,~`, box3
  `box3_marked=true`, `box3_points=false` (no ledger link yet) — consistent
  with the section's own `[~]`-not-`[x]` rule.

### Cold-read paragraph (1781–1787)

Record of process, unverifiable-by-me parts left to the ledger; the
counting-command and `[~]` claims verified above. No blocker.

No installs performed (node v24.21.0, git 2.56.0, bash 5.3.20 already present).

```json
{"seat":"RR12b","skill_sha256":"3d8a1edb1803441cfef4ce46447af51a6b857644d8f5347b2aad7c612bbcb7a4","sections":[{"start":1740,"heading":"## Seventh recorded case and full-page cold-read — round 16","class":"instruction","verdict":"executed-ok","blocking_gaps":[],"wrong_expectations":[],"minor_gaps":[],"commands_executed":["git -C ~/Projects/shokunin/kumitate-shokunin show 364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs > $W/round-gate.mjs","sha256sum $W/round-gate.mjs","bash tools/mutate-and-run.sh --target $W/round-gate.mjs --defects .ufo/evidence/round-16/round-gate/round-gate.defects.spec --suite \"$(cat .ufo/evidence/round-16/round-gate/suite.txt)\" --label js-round-gate --workdir $W/work","GATE=$W/work/pristine.round-gate.mjs node probes.mjs (all 15 probes) → exit 0","GATE=$W/work/mutant-A2.round-gate.mjs node probes.mjs P1 → exit 1; P1b → exit 1","GATE=$W/work/mutant-B2.round-gate.mjs node probes.mjs P6 → exit 1","GATE=$W/work/mutant-E1.round-gate.mjs node probes.mjs P9 → exit 1","sha256sum .ufo/evidence/round-16/round-gate/round-gate.defects.spec tools/mutate-and-run.sh","git -C lane log -1 e69b488; git -C lane merge-base --is-ancestor e69b488 c699c8c","python3 .ufo/evidence/round-16/measure.py --rev c699c8c36d6e4eca4b796b81a8247904aa145ec8 → exit 0","grep -n FINDING_KINDS / sed -n anchor lines on pinned blob"],"opened":["SKILL.md:1740-1788","tools/mutate-and-run.sh","corpus/knowledge/mutation-case-kumitate-round-gate.md",".ufo/evidence/round-16/round-gate/round-gate.defects.spec",".ufo/evidence/round-16/round-gate/suite.txt",".ufo/evidence/round-16/round-gate/predictions.json",".ufo/evidence/round-16/round-gate/survivor-probes/probes.mjs",".ufo/evidence/round-16/round-gate/sweep/results.tsv",".ufo/evidence/round-16/round-gate/sweep/sweep.log",".ufo/evidence/round-16/round-gate/runner-regression.txt",".ufo/evidence/round-16/measure.py","kumitate-shokunin scripts/round-gate.mjs @364f1d5 (into /tmp)"],"scratch":"/tmp/tameshi-r16w2-RR12b"}]}
```
