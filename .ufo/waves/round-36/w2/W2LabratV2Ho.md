# W2LabratV2Ho — sealed-accept-removal probe against c1-measure-v2.py (round 36, wave 2)

Seat: W2LabratV2Ho (labrat-style read-only probe, leaf seat, no subagents). Judged on: calibration.
Attacked: the sealed-side (`ho_*`) conjuncts of the `C1_R36V2_PASS` predicate in
`.ufo/evidence/round-36/c1/c1-measure-v2.py` (sha256 9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53, verified).

## Probe

Assigned hypothesis: remove one sealed accept copy in a scratch clone, re-run v2 in deciding
mode; predicate "must fail on ho counts". If it still passes, the sealed asserts are decorative.

Method: all work under `/fast/scratch/hyaku/tameshi-r36-seats/W2LabratV2Ho/`. The lane was never
mutated — four `git clone --no-local` copies of `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
at tip `fbb01cf46f8437fd1264c1a3acc053c882fa2164`, one mutant commit per clone (v2 reads sealed
bytes via `git show` at REV, so the removal had to be committed inside the scratch clone). Each
run used the frozen counting-command shape with a fresh empty `--work` dir:

```
python3 <clone>/.ufo/evidence/round-36/c1/c1-measure-v2.py \
    --lane <clone> --rev HEAD --work work-<clone> \
    --sealed .ufo/evidence/round-35/c1/sealed
```

| run | rev | mutation (scratch commit) | ho counts | predicate line |
|-----|-----|---------------------------|-----------|----------------|
| ctl  | fbb01cf46f8437fd1264c1a3acc053c882fa2164 | none (lane tip baseline) | ho_kill=4/4 ho_accept=3/3 | `C1_R36V2: mode=deciding tool_present=1 tool_sha=6188db16de045f29 tool_sha_ok=1 runner_sha_ok=1 pub_kill=6/6 pub_accept=3/3 pub_slots=9 pub_distinct=9 ho_kill=4/4 ho_accept=3/3 ho_invalid=0 ho_distinct=7 sealed_after_freeze=1 rev=fbb01cf46f8437fd1264c1a3acc053c882fa2164 C1_R36V2_PASS=true` |
| mutA | 0d898c595e11ae4c32424826c3463f8aeb199c7b | `git rm` `sealed/accept-trailing-comments.json` (accepts 3→2) | ho_kill=4/4 ho_accept=2/2 | `... ho_accept=2/2 ho_invalid=0 ho_distinct=6 sealed_after_freeze=1 rev=0d898c595e11ae4c32424826c3463f8aeb199c7b C1_R36V2_PASS=true` |
| mutB | c2c71e5ec5555a31d6d34fa0525eb152ec2e5b4a | `git rm` two sealed accepts (3→1) | ho_kill=4/4 ho_accept=1/1 | `... ho_accept=1/1 ho_invalid=0 ho_distinct=5 sealed_after_freeze=1 rev=c2c71e5ec5555a31d6d34fa0525eb152ec2e5b4a C1_R36V2_PASS=false` |
| mutC | a40ce5d30fdc0280898eb286f834dcf24340cb13 | `git rm` `sealed/cfg00-setup-as-pass.json` (kills 4→3) | ho_kill=3/3 ho_accept=3/3 | `... ho_kill=3/3 ho_accept=3/3 ho_invalid=0 ho_distinct=6 sealed_after_freeze=1 rev=a40ce5d30fdc0280898eb286f834dcf24340cb13 C1_R36V2_PASS=false` |

## Findings (observed)

1. **Assigned probe result: the predicate STILL PASSES after removing one sealed accept copy**
   (mutA, `C1_R36V2_PASS=true`, exit 0). The hypothesis "must fail on ho counts" is refuted.
2. **Why, exactly:** the sealed-side conjuncts (c1-measure-v2.py:542-543) are floors, not
   cardinality pins — `ho_kill_total >= 4 and ho_accept_total >= 2`, plus
   `ho_kill == ho_kill_total and ho_accept == ho_accept_total`. Removing one accept leaves
   `ho_accept_total == 2`, which still meets the floor. The same expression is verbatim in the
   frozen v1 counter (c1-measure.py:518-519); v2's only delta is the PUB_* public-panel asserts,
   untouched by sealed mutations.
3. **The sealed asserts are NOT wholly decorative** — they bite at the floor: mutB
   (`ho_accept_total=1 < 2`) and mutC (`ho_kill_total=3 < 4`) both print `PASS=false`, exit 1.
   Precise margin: with the round-35 sealed set (4 kill / 3 accept), the predicate tolerates
   deletion of up to **1 accept copy** and **0 kill copies**.
4. **Genuinely decorative surfaces found:** `ho_distinct` is computed and printed but never
   referenced in `ok` (both v1 and v2); the sealed manifest's per-copy `sha256` entries and
   file list are never verified — the counter reads only `manifest.freeze_rev` (v2:488-497).
   A behavior-preserving rewrite of a sealed copy, or a missing-but-floored accept, escapes.
5. Control sanity: baseline clone at lane tip passes exactly as the committed receipt claims
   (deciding PASS, pub 6/6 + 3/3, pub_distinct=9, ho 4/4 + 3/3, sealed_after_freeze=1).

## Verdict

**REFUTED-as-stated / NARROWED:** removing one sealed accept copy does NOT fail v2 deciding
mode — `C1_R36V2_PASS=true` at mutA — so the sealed asserts are decorative *within the
floor slack* (1 accept deletable). They are load-bearing floors, not exact-set pins: crossing
`ho_accept_total < 2` or `ho_kill_total < 4` fails the run (mutB, mutC). If C2's intent is
"the sealed panel is pinned," that holds only modulo the floors and the never-checked manifest
sha256 list.

## Environment / tools

No installs (python3 3.14.8, git, bash — all present). Frozen pins re-verified pre-run:
mutate-and-run.sh a7d3f2dd…, tally-audit-v3.py 6188db16…, c1-measure-v2.py 9eb8944c… — all
match contract.json. Lane untouched; scratch only at /fast/scratch/hyaku/tameshi-r36-seats/W2LabratV2Ho/.
