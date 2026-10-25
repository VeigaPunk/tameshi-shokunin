# ExecCommandD — no-harm re-run of command D (depth) and the round-21 cold-read monitor (calibration)

Scope: re-run the two canonical axis commands at BASE `487b8f0da89fa0e2b8bea6930068accbf36e70a9`
and at FREEZE `17f6ef0c72ec27e1aea305b5c95806b43bb2caef`, and report both lines.
Read-only: no lane file touched except this report; no git/jj state touched; no tool installed.
Scratch under `/tmp` was deleted at the end (see Records).

## 1. Exact commands (as printed in `SCORECARD.md:69-76`)

```sh
# D: recorded ledger case count = depth score (cap 10).
git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
```

Command D was executed verbatim with `cwd=/home/vgpnk/Projects/shokunin/tameshi-shokunin`
(`git show "$REV:…"` is repo-relative, so the lane is the required cwd).

```sh
# calibration monitor (round 21), canonical form per SCORECARD.md:1537
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py \
  --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV
```

`--repo` was made explicit (the round-21 wrapper's default repo resolution would otherwise be
derived from its own path); the wrapper uses this file only as a selector over the frozen
round-18 algorithm (`.ufo/evidence/round-21/coldread/measure.py:1-113`), and refuses
`--ledger-file`/`--ledger-rev`/`--inputs-overlay` (`:22-23`). No override was passed.

## 2. Results — both axes, both revisions

| axis | base `487b8f0` | freeze `17f6ef0` | delta |
|---|---|---|---|
| D (depth): `git show REV:tools/mutate-and-run.sh` regex count | `recorded_cases=9 depth_score=9`, rc 0 | `recorded_cases=9 depth_score=9`, rc 0 | 0 |
| calibration: `calibration_restraint_score` | **6**, exit 0 | **6**, exit 0 | 0 |

Exact lines produced:

```
REV=487b8f0da89fa0e2b8bea6930068accbf36e70a9
recorded_cases=9 depth_score=9
rc=0 0                          # git show | python3: both stages 0

REV=17f6ef0c72ec27e1aea305b5c95806b43bb2caef
recorded_cases=9 depth_score=9
rc=0
```

```
=== REV=487b8f0da89fa0e2b8bea6930068accbf36e70a9
exit=0
  "calibration_restraint_score": 6,
=== REV=17f6ef0c72ec27e1aea305b5c95806b43bb2caef
exit=0
  "calibration_restraint_score": 6,
```

**No harm.** Neither axis moved in either direction; the freeze adds nothing and removes nothing
on the two canonical counters. `depth_score=9` is 9/9 rather than the cap (cap 10), and
`calibration_restraint_score=6` is the contract's declared lowest non-retired axis value
(`.ufo/evidence/round-43/contract.json`, `axes.lowest_non_retired_axis`), i.e. consistent with the
frozen claim set rather than a regression.

## 3. Why the equality is structural, not incidental

Every input the two commands read is byte-identical at the two revisions (blob ids from
`git rev-parse REV:path`):

| path | base blob | freeze blob |
|---|---|---|
| `tools/mutate-and-run.sh` | `2d81b929c765d52d6ff38837bb76901cd3358c8e` | `2d81b929c765d52d6ff38837bb76901cd3358c8e` |
| `SHONEN.md` | `253f3c05d5a78fed5d6538d54351d1ef930b6937` | `253f3c05d5a78fed5d6538d54351d1ef930b6937` |
| `.ufo/evidence/round-21/coldread/ledger.json` | `b0522d3ca6e1ee6e06935a0265e3cd0c392c4d69` | `b0522d3ca6e1ee6e06935a0265e3cd0c392c4d69` |
| `.ufo/evidence/round-21/coldread/measure.py` | `9eb05868558224a1aaec3054de47feaf7219225a` | `9eb05868558224a1aaec3054de47feaf7219225a` |

The runner is unchanged by the freeze (round 43 is a survivor-resolution round; no ledger leg was
added), the SHONEN mark census is unchanged, and the round-21 ledger is unchanged and
`ledger_committed: true` at both revs.

## 4. Full monitor readout (axis-relevant keys; identical apart from the revision echo)

```
{"revision":"487b8f0…" | "17f6ef0…",
 "calibration_restraint_score": 6,
 "depth_score": 9, "recorded_cases": 9,
 "trace_gate": "strict", "ledger_source": "rev",
 "ledger_committed": true, "overrides_used": false,
 "shonen": {"boxes":4,"checked":0,"asserted":4,"untouched":0,
            "marks":["~","~","~","~"],
            "box3_marked":true,"box3_ledger_link":true,"box3_points":false},
 "ledger_guardrail": {"header_legs":9,"lists_agree":true,"regression_calls":9,
                      "selftest_tuples":9,"unique_recorded_gates":9},
 "coldread": {"box3_full_page":false,"ledger_present":true,
              "sections_covered":60,"sections_total":64,
              "inputs_overlay_merged":0,
              "missing":[4 entries, all reason=input-drift:…]}}
```

`diff` of the two saved stdout files differs at exactly two lines — `rev_input` and `revision`
(the echoed SHA). Byte comparison of the whole JSON: 247,177 bytes, differing only in those two
fields (`python3` key-wise comparison printed `DIFF KEY: rev_input` and `DIFF KEY: revision`, no
other key).

Score decomposition (formula `.ufo/evidence/round-18/measure.py:681-683`):
`restraint = 2·(credited boxes 1,2,4) + 2·box3_points`; `box3_full_page = sections_covered ==
sections_total` (`:655`). Here `60 ≠ 64`, so `box3_points=false` and the score is `2·3 = 6`.
Both revs produce the same 4 missing sections and the same drift reason strings, so the freeze
introduces **zero new cold-read input drift** (the drift set is pre-existing, from
`input-drift:corpus/README.md`, `…:corpus/knowledge/closeout-r11.md`,
`…:reports/round-1-calibration.md`, `…:tools/mutate-and-run.sh` — the last one is the runner
itself pinning an older blob).

Exit semantics caveat (useful when reading "exit 0"): `main()` returns 0 unconditionally after
printing the JSON and 2 only for refusals (repo/rev/blob/overlay errors,
`round-18/measure.py:1652-1657`). So `exit=0` means "measured, not refused"; the axis value is the
JSON field, not the exit code. Both revs are on the success path.

## 5. Depth probe: does command D's regex count what it claims?

Independent precision check on the same bytes (read-only probe, not a replacement counter):

```
strict = re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+", text, re.M)
loose  = re.findall(r"^\s*#\s+(?:js|bash)-[^\n]*\d+/\d+", text, re.M)
all-`#   `-prefixed lines = 33
```

Both revs: `strict=9 loose=9`, and the 9 matched lines are exactly the contiguous ledger rows
`tools/mutate-and-run.sh:87-95` at FREEZE (base identical, same blob):

```
87 MATCH #   js-kimi-census        kumitate-shokunin/scripts/kimi-census.mjs   8/10 (80 %)
88 MATCH #   bash-surface-census   kagi-shokunin/corpus/surface-census.sh      8/10 (80 %)
89 MATCH #   bash-tsukuroi-census  tsukuroi-shokunin/tools/tsukuroi-census.sh  6/10 (60 %)
90 MATCH #   bash-mado-verify      mado-shokunin/tools/mado-verify.sh          4/10 (40 %)
91 MATCH #   bash-checklist-run    kagi-shokunin/corpus/checklist-run.sh       7/15 (47 %)
92 MATCH #   js-claims-check       kumitate-shokunin/scripts/claims-check.mjs  7/10 (70 %)
93 MATCH #   js-round-gate         kumitate-shokunin/scripts/round-gate.mjs    5/10 (50 %)
94 MATCH #   js-sources-check      kumitate-shokunin/scripts/sources-check.mjs 5/10 (50 %)
95 MATCH #   js-cite-check         kumitate-shokunin/scripts/cite-check.mjs    5/10 (50 %)
```

The other 24 `#   ` lines are unmatched and are not ledger rows: spec/help text (`:43-52`),
env/verdict labels (`:56-59`, `:73-78`), the MutateHead arm-class map (`:847-850`) and one
continuation row (`:796`). The 9 leg names also agree with the monitor's independent
`ledger_legs` list (`js-kimi-census, bash-surface-census, bash-tsukuroi-census, bash-mado-verify,
bash-checklist-run, js-claims-check, js-round-gate, js-sources-check, js-cite-check`) and with
`ledger_guardrail.lists_agree: true`. Command D is therefore reading the ledger it names, not a
subset or a superset of comment lines — the measurement is exact, which is what "no harm on
depth" needs to mean.

## 6. Risks / limits of this receipt

- Depth here is *documented* case depth (ledger rows at REV), by construction of command D; it is
  not a re-execution of the mutation cases. Re-execution is the C1 counter's job, not this seat's.
- `calibration_restraint_score` is a mark census plus the strict cold-read gate; it cannot award
  the last 2 points (independent promotion review) by design (`SCORECARD.md:66-67`), so 6 is the
  ceiling reachable with `box3_full_page=false`.
- The monitor reads live external inputs (digests of `/home/vgpnk/Projects/shokunin/**`,
  `~/.omp/agent/config.yml`, kimi PROTOCOL.md …) that are outside this lane; those digests were
  identical across both runs, but any host-side edit between runs would change the JSON without
  changing the lane.
- I did not run the C1/C2/C3 round-43 counters (`--lane/--rev/--freeze`); the deciding run belongs
  to the L1.

## 7. Records

- Tools installed/upgraded: **none** (pacman is paused host-wide; nothing was needed —
  `git` and the system `python3` sufficed).
- Scratch used and deleted: `/tmp/cmdD-487b8f0….out`, `/tmp/cmdD-487b8f0….err`,
  `/tmp/cmdD-17f6ef0….out`, `/tmp/cmdD-17f6ef0….err`. The axis-relevant slices of those files are
  transcribed into §2/§4 above; the full 247 KB stdout is not retained in the lane because this
  seat's write scope is this report only.
- Files changed by this seat: this report (`.ufo/waves/round-43/w1/ExecCommandD.md`) and nothing
  else. No `git`/`jj` mutation, no sibling/fleet-repo/shokuknow write.
