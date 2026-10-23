# Round 34 · wave 1 · LedgerDepth — depth-axis ledger verification

Seat: `LedgerDepth` (executor, axis **depth**). Lane tip at dispatch:
`0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`. Measurement revision:
`c17e593b51802dd4ed568da3265f21c6d00c4273`.

All work happened in the seat scratch dir `/fast/scratch/hyaku/tameshi-r34-seats/LedgerDepth/`.
The lane clone was read-only; no lane file, MANIFEST, template, `.ufo/state/`, or git/jj
index was written. The only write outside the scratch dir is this report.

---

## Finding (the one that matters)

**The dispatch's expected depth value is wrong. Command D at the tip prints
`recorded_cases=9 depth_score=9`, not `recorded_cases=6 depth_score=6`. The lane is
right; the dispatch carried a stale expectation.**

Reproduce (exit 0, exact stdout below):

```bash
cd /fast/scratch/hyaku/tameshi-r34-seats/LedgerDepth/lane
REV=0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7
git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
echo "exit=$?"
```

Exact output — stdout:

```
recorded_cases=9 depth_score=9
```

stderr: empty. `exit=0`.

Where the `6` comes from: `6` is the **fleet round-1 baseline** value, which the lane
still records but has explicitly superseded. Command D at the baseline revision
`284ab0f0b8b989ee73d9c00c0c0df0a59757af8d` prints exactly `recorded_cases=6 depth_score=6`
(verified, exit 0) — that revision's ledger comment has six legs at
`tools/mutate-and-run.sh:84-89`, matching `SCORECARD.md:66`. The lane's own **current**
axis table (`SCORECARD.md:1536`, round-31 measurement revision) states depth **9** and
cites the same command printing `recorded_cases=9 depth_score=9`. The round-34 block
itself records `depth 9 → 9 (command D, runner byte-identical at the pinned sha)`
(`SCORECARD.md:1659-1660`).

Leg growth across runner revisions (command D at each rev, all exit 0):

| runner revision | command D |
|---|---|
| `284ab0f0` (fleet round-1 baseline) | `recorded_cases=6 depth_score=6` |
| `606716f` (probation round 10) | `recorded_cases=6 depth_score=6` |
| `c699c8c` (round 16, leg 7 `js-round-gate`) | `recorded_cases=7 depth_score=7` |
| `58e5d53` (round 18, leg 8 `js-sources-check`) | `recorded_cases=8 depth_score=8` |
| `a08e85c` (round 26, leg 9 `js-cite-check`) | `recorded_cases=9 depth_score=9` |
| `bb68156` (round 30, tally guard) | `recorded_cases=9 depth_score=9` |
| `c17e593b` (measurement rev) | `recorded_cases=9 depth_score=9` |
| `0b99d48e` (lane tip) | `recorded_cases=9 depth_score=9` |

**No landed artifact is wrong here.** The dispatch expectation was copied from the
superseded round-1 baseline table. Nothing in the lane's live record claims depth 6:
every `recorded_cases=6` / `depth 6` occurrence is inside a explicitly historical
section — `SCORECARD.md:66` (round-1 baseline table, header
`## Current axes — fleet round-1 baseline`, superseded by the table at `SCORECARD.md:1530-1536`),
`SCORECARD.md:184` (round-1 kaika continuation), `SCORECARD.md:312` (round-12 block),
`LOG.md:400` (dated 2026-10-15 entry), `corpus/lessons/round-1.md`, `reports/round-1-calibration.md`,
plus dated wave reports under `.ufo/waves/round-1[2-9]/`.

---

## Pin verification (all three pins confirmed)

```bash
cd /fast/scratch/hyaku/tameshi-r34-seats/LedgerDepth
git -C lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/tally-audit-v2.py > tool.py   # exit 0
git -C lane show 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:tools/mutate-and-run.sh > pristine.sh  # exit 0
sha256sum tool.py pristine.sh
```

```
7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10  tool.py      # matches pin 7b11ba25…8d10
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  pristine.sh  # matches pin a7d3f2dd…2eb9
```

The runner at the tip, hashed directly from the object store
(`git show 0b99d48e…:tools/mutate-and-run.sh | sha256sum`, exit 0) →
`a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` — **matches the pin.**

The counter at the tip (`.ufo/evidence/round-33/c1/c1-measure.py`, `sha256sum`, exit 0) →
`f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` — **matches the
dispatch's pinned counter sha `f6b8868c…a07f28c` (amendment 6).**

The live repo's working tree is byte-identical to the tip for all three files
(`git status --porcelain -- tools/mutate-and-run.sh tools/tally-audit-v2.py .ufo/evidence/round-33/c1/c1-measure.py`
→ empty output, exit 0; `sha256sum` of the three live files gives the same three hashes).

Runner sha across the round-34 window (all via `git show <rev>:tools/mutate-and-run.sh | sha256sum`,
exit 0) — the runner was **byte-identical** from `bb68156` (round 30) through the tip:

```
732b6860 (r33 head)  a7d3f2dd7d47511a…
c17e593b (meas rev)   a7d3f2dd7d47511a…
0b99d48e (tip)        a7d3f2dd7d47511a…
```

This is what makes the round-34 `depth 9 → 9` claim sound: the runner bytes did not
move, so the ledger could not have moved.

---

## Independent cross-check: the lane's own depth counter

The lane ships a second, independently-written depth counter at
`.ufo/evidence/round-26/c1-measure.py` (a different implementation from command D: it
requires each recorded leg to be *wired* — embedded spec heredoc **and** a
`regression_case_git` call **and** a `'<leg>:<leg>.spec:TABLE_<X>:<n>:<k>'` entry **and**
a `TABLE_<X>` line with exactly `<n>` defects and `<k>` KILLED).

```bash
cp lane/.ufo/evidence/round-26/c1-measure.py ./depth-counter.py
python3 ./depth-counter.py --repo /fast/scratch/hyaku/tameshi-r34-seats/LedgerDepth/lane
echo "exit=$?"
```

stdout (exit 0):

```
C1_LEG js-kimi-census: WIRED
C1_LEG bash-surface-census: WIRED
C1_LEG bash-tsukuroi-census: WIRED
C1_LEG bash-mado-verify: WIRED
C1_LEG bash-checklist-run: WIRED
C1_LEG js-claims-check: WIRED
C1_LEG js-round-gate: WIRED
C1_LEG js-sources-check: WIRED
C1_LEG js-cite-check: WIRED
C1_DEPTH: recorded_cases=9 wired_legs=9 depth_score=9
```

`wired_legs=9` — every recorded leg is genuinely wired, so the 9 is not a comment-count
artifact.

---

## Ledger ↔ table consistency (static, per leg)

Command (exit 0): a python check over `lane/tools/mutate-and-run.sh` comparing, for each
of the 9 legs, the ledger comment rate, the `lent` tuple `(killed, total)`, and the
`TABLE_*` constant's actual KILLED/SURVIVED counts:

```
ledger legs: 9 lent tuples: 9
js-kimi-census         ledger=8/10   tuple=8/10  table=8/10  K=8 S=2  match=True
bash-surface-census    ledger=8/10   tuple=8/10  table=8/10  K=8 S=2  match=True
bash-tsukuroi-census   ledger=6/10   tuple=6/10  table=6/10  K=6 S=4  match=True
bash-mado-verify       ledger=4/10   tuple=4/10  table=4/10  K=4 S=6  match=True
bash-checklist-run     ledger=7/15   tuple=7/15  table=7/15  K=7 S=8  match=True
js-claims-check        ledger=7/10   tuple=7/10  table=7/10  K=7 S=3  match=True
js-round-gate          ledger=5/10   tuple=5/10  table=5/10  K=5 S=5  match=True
js-sources-check       ledger=5/10   tuple=5/10  table=5/10  K=5 S=5  match=True
js-cite-check          ledger=5/10   tuple=5/10  table=5/10  K=5 S=5  match=True
ALL_LEG_CONSISTENT= True
```

Leg-name set equality, three ways (each `diff` exit 0, no output): ledger comment lines
(`grep -oE "^#   (js|bash)-[a-z-]+"`, 9) vs. `regression_case_git` call sites
(`grep -oE "^  regression_case_git (js|bash)-[a-z-]+"`, 9) vs. `lent` tuples
(`grep -oE "^    '(js|bash)-[a-z-]+:"`, 9). Embedded spec heredocs:
`grep -cE '^  cat >"\$d/[a-z-]+\.spec" <<' tools/mutate-and-run.sh` → **9**. Distinct
targets in the ledger → 9; distinct leg names → 9. `nlegs` declaration
(`tools/mutate-and-run.sh:1432`) → `local nlegs=9 npass=0 nfail=0 nsetup=0 st`.

The counter's `START` constant (`c1-measure.py:61`) is the same string, so the round-33
counter and the runner agree on 9 legs.

---

## Runtime verification 1 — the runner's own hermetic selftest

```bash
cp pristine.sh runner.sh && chmod +x runner.sh
bash runner.sh --selftest > selftest.out 2> selftest.err
echo "exit=$?"
```

`exit=0`, stderr empty, 108 stdout lines. Tail:

```
MUTATE_SELFTEST: 106/106 pass
VERDICT: PASS
```

Leg-count agreement lines from the same run (`selftest.out:83-94`):

```
PASS embedded leg specs: nine files written
PASS leg-count agreement: calls=9 specs=9 nlegs=9 (want 9)
PASS leg-count agreement: selftest leg tuples=9 (want 9)
PASS embedded leg js-kimi-census: spec and recorded table agree
PASS embedded leg bash-surface-census: spec and recorded table agree
PASS embedded leg bash-tsukuroi-census: spec and recorded table agree
PASS embedded leg bash-mado-verify: spec and recorded table agree
PASS embedded leg bash-checklist-run: spec and recorded table agree
PASS embedded leg js-claims-check: spec and recorded table agree
PASS embedded leg js-round-gate: spec and recorded table agree
PASS embedded leg js-sources-check: spec and recorded table agree
PASS embedded leg js-cite-check: spec and recorded table agree
```

The tally-harness vectors also all exercise 9 positions (e.g.
`PASS tally harness: one leg status 1 at each of 9 positions -> REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0) (9/9)`).

## Runtime verification 2 — the full 9-leg `--regression` replay

The runner materializes each leg from the **sibling repos' git object stores** at its
pinned revision (read-only on the fleet). To let it find them, a scratch fleet root was
built with symlinks to the real sibling repos and a copy of the pinned runner — no fleet
path was written:

```bash
mkdir -p fleet/tameshi-shokunin/tools
cp pristine.sh fleet/tameshi-shokunin/tools/mutate-and-run.sh
chmod +x fleet/tameshi-shokunin/tools/mutate-and-run.sh
for r in kumitate-shokunin kagi-shokunin tsukuroi-shokunin mado-shokunin; do
  ln -sfn /home/vgpnk/Projects/shokunin/$r fleet/$r
done
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  bash fleet/tameshi-shokunin/tools/mutate-and-run.sh \
  --regression --workdir /fast/scratch/hyaku/tameshi-r34-seats/LedgerDepth/regression-work --keep \
  > regression.out 2> regression.err
echo "exit=$?"
```

`exit=0` (wall 197 s), stderr empty, 51 stdout lines.

Header:

```
REGRESSION_TOOL: …/fleet/tameshi-shokunin/tools/mutate-and-run.sh sha256=a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
REGRESSION_BAND: ledger legs exact (killed-delta<=0 flips<=0 inconclusive=0 defects=exact); fixture-mode default killed-delta<=1 flips<=1
REGRESSION_EXPECT: recorded kill-rates — js-kimi-census=8/10 bash-surface-census=8/10 bash-tsukuroi-census=6/10 bash-mado-verify=4/10 bash-checklist-run=7/15 js-claims-check=7/10 js-round-gate=5/10 js-sources-check=5/10 js-cite-check=5/10
```

Per-leg results (every leg PASS, every verdict table match with **0 flips**, 0 inconclusive):

| leg | table match | recorded-killed | measured-killed | flips | verdict |
|---|---|---|---|---|---|
| `js-kimi-census` | 10/10 | 8 | 8 | 0 | PASS |
| `bash-surface-census` | 10/10 | 8 | 8 | 0 | PASS |
| `bash-tsukuroi-census` | 10/10 | 6 | 6 | 0 | PASS |
| `bash-mado-verify` | 10/10 | 4 | 4 | 0 | PASS |
| `bash-checklist-run` | 15/15 | 7 | 7 | 0 | PASS |
| `js-claims-check` | 10/10 | 7 | 7 | 0 | PASS |
| `js-round-gate` | 10/10 | 5 | 5 | 0 | PASS |
| `js-sources-check` | 10/10 | 5 | 5 | 0 | PASS |
| `js-cite-check` | 10/10 | 5 | 5 | 0 | PASS |

Final line:

```
REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)
```

Materialized pins (each `REGRESSION_PIN` line, from the real sibling object stores):

| leg | rev | path | mode | sha256 |
|---|---|---|---|---|
| `js-kimi-census` | `175de6ba2e9e904010411b19cab27e0af9aad3d4` | `scripts/kimi-census.mjs` | 100644 | `83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426` |
| `bash-surface-census` | `fecee8743e52eb8fb5fbb40782934cb619a1a96e` | `corpus/surface-census.sh` | 100755 | `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f` |
| `bash-tsukuroi-census` | `165307fe4746a8807b02ec4a7d7ecac0368454a6` | `tools/tsukuroi-census.sh` | 100755 | `084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5` |
| `bash-mado-verify` | `eead56b20ad2b28299ae4fa623d52a99b44c743c` | `tools/mado-verify.sh` | 100755 | `d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13` |
| `bash-checklist-run` | `fecee8743e52eb8fb5fbb40782934cb619a1a96e` | `corpus/checklist-run.sh` | 100755 | `7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf` |
| `js-claims-check` | `175de6ba2e9e904010411b19cab27e0af9aad3d4` | `scripts/claims-check.mjs` | 100755 | `e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b` |
| `js-round-gate` | `364f1d5954158ef8844bca4a5fef57b05d2f2ca5` | `scripts/round-gate.mjs` | 100755 | `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9` |
| `js-sources-check` | `0acb7752d19058b953ebbeba253b1e35f6548de5` | `scripts/sources-check.mjs` | 100755 | `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f` |
| `js-cite-check` | `1205c6621a2eccbb8ffceae86d9e7b79a7990b3a` | `scripts/cite-check.mjs` | 100755 | `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f` |

This is the strongest depth evidence available: the 9 recorded legs are not a comment
count, they are 9 independently replayable, byte-pinned mutation cases that all still
reproduce their recorded kill-rate exactly today.

---

## The deciding run stands

The dispatch's C1 claim is untouched by anything above. The deciding-run receipt in the
lane is byte-identical to the one quoted in the dispatch:

```
$ cat lane/.ufo/evidence/round-34/measure/c1-deciding-run.stdout
C1_R33: tool_present=1 tool_sha_ok=1 runner_sha_ok=1 controls_ok=1(ok) v1_kill=18/18 v1_accept=8/8 ho_kill=8/8 ho_accept=6/6 ho_invalid=0 heldout_after_freeze=1 seed=685f63bd25263908 rev=c17e593b51802dd4ed568da3265f21c6d00c4273 C1_R33_PASS=true
$ cat lane/.ufo/evidence/round-34/measure/c1-deciding-run.exit
0
```

The counter's own freeze-time monitor already recorded the depth axis independently
(`lane/.ufo/evidence/round-33/dev/monitor-at-freeze.stdout:1770` → `"depth_score": 9`,
`:1792` → `"recorded_cases": 9`), and the round-33 contract states the stagnation
nudge against `depth 9, calibration 8 >= line 8`
(`lane/.ufo/evidence/round-33/contract.json:16`).

**The kill rule was honored.** No default-mode
`python3 .ufo/evidence/round-33/c1/c1-measure.py --lane … --rev … --work …` was run in
this seat. The counter was read as bytes only (`sha256sum`, plus reading its source to
confirm its `START`/leg accounting); the depth counter actually executed was the
*different* round-26 script `.ufo/evidence/round-26/c1-measure.py`, which takes
`--repo CLONE_AT_REV` and only reads the runner text — it neither runs the runner nor
invokes the round-33 counter. Every command's exit code was captured with
`cmd; echo $? > file`, never `&&`.

## Secondary observation (not a finding against the lane)

The runner's `# Sources:` block (`tools/mutate-and-run.sh:96-99`) cites the legs 1–7
knowledge entries, but cites legs 8 and 9 by their **evidence spec paths**
(`.ufo/evidence/round-18/sources-check/sources-check.defects.spec`,
`.ufo/evidence/round-26/cite-check/cite-check.defects.spec`) rather than by their
knowledge entries `corpus/knowledge/mutation-case-kumitate-sources-check.md` and
`corpus/knowledge/mutation-case-kumitate-cite-check.md` — both of which exist
(`ls` shows 19820 and 9735 bytes) and are cited from `SKILL.md:1913` / `SKILL.md:2113`
and `corpus/README.md:265` / `:405`. This is a citation-style inconsistency in a
comment block; it does not change the ledger count, the wiring, or any recorded verdict.
Noted for the record only; no edit is proposed here (the runner is byte-pinned).

Reproduce:

```bash
cd /fast/scratch/hyaku/tameshi-r34-seats/LedgerDepth/lane
sed -n '96,101p' tools/mutate-and-run.sh
grep -rn "mutation-case-kumitate-sources-check\|mutation-case-kumitate-cite-check" --include=*.md . | grep -v "^./.ufo/waves/"
```

## Depth-axis verdict

- **Depth at the tip = 9**, confirmed by four independent routes: SCORECARD command D
  (exit 0, `recorded_cases=9 depth_score=9`), the lane's independent round-26 depth
  counter (`wired_legs=9 depth_score=9`, exit 0), the runner's own selftest leg-count
  agreement (`calls=9 specs=9 nlegs=9`, 106/106 PASS, exit 0), and the full 9-leg
  `--regression` replay (`cases=9 passed=9`, 0 flips on every leg, exit 0).
- **Depth 9 → 9 for round 34** is correct: the runner bytes are unchanged from `bb68156`
  through the tip (sha `a7d3f2dd…2eb9` throughout), so the ledger could not have moved.
- The dispatch's expected `recorded_cases=6 depth_score=6` reflects the superseded
  round-1 baseline (`284ab0f0`), not the tip. **No landed artifact is wrong; the
  expectation was stale.** The lane's live current-axis table already says 9.
- No axis was harmed and no repair is warranted on the depth axis by this seat.

## Tooling

No installs or upgrades were performed by this seat; no package manager was invoked.
Everything used was already present: `git 2.56.0`, `node v24.21.0`, `python3`, `bash`,
`sha256sum`, `diff`, `grep`. The operator tooling directive in
`/home/vgpnk/.omp/agent/RULES.md` was read before any command; the pacman guard was
respected (no pacman transaction of any kind was attempted).

## Artifacts left in the seat scratch dir

`/fast/scratch/hyaku/tameshi-r34-seats/LedgerDepth/` — `lane/` (read-only clone at the
tip), `tool.py`, `pristine.sh`, `runner.sh`, `fleet/` (scratch fleet root with symlinks
to the real sibling repos), `regression-work/` (replay workdir, `--keep`),
`commandD.out` / `commandD.exit`, `depth-counter.py` / `.out` / `.exit`,
`selftest.out` / `.err` / `.exit`, `regression.out` / `.err` / `.exit`.

## Suggested routing (observation, not action)

If the orchestrator wants the depth expectation to be self-consistent in future
dispatches, the number to quote for this lane is **9**, not 6, and the pointer is
`SCORECARD.md:1536` (current axis table) rather than `SCORECARD.md:66` (round-1
baseline table). The `6` is still correct *for its own revision* `284ab0f0`; the two
numbers are not in conflict once the revision is named.
