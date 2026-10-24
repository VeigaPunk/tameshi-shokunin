# Round 36 W1 — mutation probe: v2 predicate constant

Attacked: C2 depth surface — the frozen successor counter
`.ufo/evidence/round-36/c1/c1-measure-v2.py` (sha256 `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53`)
and its deciding predicate `C1_R36V2_PASS`, which must enforce the frozen public-slot
cardinality/distinctness targets (`PUB_KILL_SLOTS_TARGET=6`, `PUB_ACCEPT_SLOTS_TARGET=3`,
`PUB_DISTINCT_TARGET=9`).

Mutant: one line in an isolated scratch clone, line 68 —
`PUB_KILL_SLOTS_TARGET = 6` -> `PUB_KILL_SLOTS_TARGET = 7`.
Nothing else changed (`git diff` in the scratch clone: 1 file, 1 insertion, 1 deletion).
The committed lane file was never edited.

## Setup

```sh
S=/fast/scratch/hyaku/tameshi-r36-seats/MTV2Predicate1
git clone -q /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/lane"       # pristine @ d9c496b19371b779ce0eec6dfee1b049b27a3a2d
git clone -q /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/lane-mut"   # mutant; HEAD 87acdaa63a23a844e0bcf4dda9357de399cf017e
```

Frozen inputs re-hashed in both clones before running:

| artifact | sha256 |
|---|---|
| `tools/tally-audit-v3.py` | `6188db16de045f2927df2a0e667bc1539f4acfce5a1ac116e6de3107bf15d354` |
| `tools/mutate-and-run.sh` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` |
| pristine `c1-measure-v2.py` | `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53` |
| mutant `c1-measure-v2.py` | `122c420bf052a6ffbe5032bf67516d9c8c85bc8c78daa21a2951f4f2090bc4bb` |

Sealed provenance was satisfiable at both scratch revisions: contract first-add
`d16f9b5a18945ede3852ec3df7eb4ee4b0afbafc` equals the sealed manifest `freeze_rev`, and all
seven sealed specimen files last changed at `691bb5128e98`.

## Detector (identical command for all three runs; distinct empty `--work` dirs)

Control mode with the real round-35 public panel and the real tool, plus the sealed set so the
predicate's `ho_*` terms are satisfiable (see note at end):

```sh
python3 .ufo/evidence/round-36/c1/c1-measure-v2.py \
  --lane <SCRATCH_LANE> --rev HEAD \
  --work /fast/scratch/hyaku/tameshi-r36-seats/MTV2Predicate1/work-<RUN> \
  --sealed .ufo/evidence/round-35/c1/sealed \
  --tool tools/tally-audit-v3.py
```

### 1. Pristine bytes, scratch rev `d9c496b19371b779ce0eec6dfee1b049b27a3a2d`

```text
C1_R36V2_CONTROL: mode=control tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=d9c496b19371b779ce0eec6dfee1b049b27a3a2d C1_R36V2_CONTROL_PASS=true
```

Process exit 0. All 16 public+sealed copies scored `pass=True` (9 public: 6 kill / 3 accept;
7 sealed: 4 kill / 3 accept); full transcript at
`/fast/scratch/hyaku/tameshi-r36-seats/MTV2Predicate1/baseline-sealed.txt`.

### 2. Mutated bytes, scratch rev `87acdaa63a23a844e0bcf4dda9357de399cf017e`

```text
C1_R36V2_CONTROL: mode=control tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=87acdaa63a23a844e0bcf4dda9357de399cf017e C1_R36V2_CONTROL_PASS=false
```

Process exit 1. Predicate line captured above; all per-copy `COPY ... pass=True` lines are
byte-identical to the pristine run. Full transcript at
`/fast/scratch/hyaku/tameshi-r36-seats/MTV2Predicate1/mutant-sealed.txt`.

### 3. Restored bytes, scratch rev `4669acd1b16f6f955259920a29cf1296ac8f1e5d`

```text
C1_R36V2_CONTROL: mode=control tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=4669acd1b16f6f955259920a29cf1296ac8f1e5d C1_R36V2_CONTROL_PASS=true
```

Process exit 0. Full transcript at
`/fast/scratch/hyaku/tameshi-r36-seats/MTV2Predicate1/restored-sealed.txt`.

## Verdict

**KILLED.** Expected detector: the deciding predicate flips `true` -> `false` while every
measured count stays at the real panel's shape (6/6, 3/3, 9), because the target constant alone
changed. Actual: pristine `C1_R36V2_CONTROL_PASS=true` (exit 0), mutant
`C1_R36V2_CONTROL_PASS=false` (exit 1), restored `C1_R36V2_CONTROL_PASS=true` (exit 0). The
failure is attributable to `pub_kill_slots == PUB_KILL_SLOTS_TARGET` (the only term whose inputs
differ), so the frozen-cardinality assert is load-bearing in the predicate, not dead text.

The captured line is the control-mode label (`C1_R36V2_CONTROL_PASS`), which prints the same
`ok` boolean the contract names `C1_R36V2_PASS`; no default-mode (deciding) run was executed in
the scratch clone, so the contract's "exactly one deciding v2 run at the measurement commit"
kill rule is not disturbed by this probe.

## Restoration evidence

- `cp` of the pristine lane file back over the mutant scratch file; sha256 after restore
  `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53` equals the frozen
  `counter_sha256` in `.ufo/evidence/round-36/contract.json`.
- Scratch clone `lane-mut` history: `87acdaa` (mutant) then `4669acd` (restore); working tree
  clean; post-restore run 3 printed `PASS=true`.
- Real lane untouched: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-36/c1/c1-measure-v2.py`
  sha256 `9eb8944c...fa53`. During the probe the lane advanced from `d9c496b` (our clone base)
  to `fbb01cf46f8437fd1264c1a3acc053c882fa2164` ("round-36 verifier spot-check", integrator
  commit by another seat, not this seat); the committed v2 bytes at that new HEAD still hash
  `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53`, so the frozen input
  under attack is unchanged and the mutation result stands. `git status --porcelain` in the
  lane shows only the untracked `.ufo/waves/round-36/w1/` report directory. No mutating
  git/jj command was run in any checkout; the only commits were in the disposable scratch
  clone. No tool installs were needed.

## Bounded observation (not a contract judgement)

In control mode the `ho_kill_total >= 4 and ho_accept_total >= 2` terms are unconditional,
so a `--tool` run *without* `--sealed` can never print `PASS=true` even though all public terms
hold. Evidence: a fourth run (same command, no `--sealed`, pristine bytes @ `d9c496b`) printed
`pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=0/0 ho_accept=0/0 ...
C1_R36V2_CONTROL_PASS=false` (transcript `baseline-control.txt`). This matches the counter's
own predicate code; it is why the discriminating detector above includes `--sealed`, and why
a control invocation that omits it is not a usable baseline. Noted for the calibration record
only — the docstring's "control never needs sealed" phrasing is satisfied in the sense that a
control run does not *require* sealed, but its PASS line then does not reflect the public
surface alone.
