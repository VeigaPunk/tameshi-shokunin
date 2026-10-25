# Round 42 wave 2 — ReplayNoHarm (no-harm axes: depth, calibration)

Seat: L1Tameshi42.ReplayNoHarm (leaf; read-only except this report). Date 2026-10-25.
Attacked thing: wave-1 integration tip `a21845f523b75adbd3e3f7a62af91294db224ad9` must not
lower the no-harm monitors (depth_score, calibration_restraint_score) and must not delete
recorded content in the ledger-of-record files, relative to base
`c77c2b7e64d2e356381441ecf94abac03e984606`.
All runs at the tip are **pre-run** (labelled per contract); no default-mode counter run after the tip.
Scratch clone: `/tmp/tameshi-r42w2-ReplayNoHarm-clone` (`git clone --quiet --shared`), `git status --porcelain`
empty after the runs (0 lines), deleted before return. No tools installed or updated.

## Findings

### F1 — SCORECARD command D: depth_score=9 at tip, equal to base (held)

Command copied verbatim from `SCORECARD.md:73` (block `SCORECARD.md:69-76`), run in the lane via read-only `git show`:

```sh
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
for REV in a21845f523b75adbd3e3f7a62af91294db224ad9 c77c2b7e64d2e356381441ecf94abac03e984606; do
  git show "$REV:tools/mutate-and-run.sh" | python3 -c 'import re,sys; n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M)); print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
done
```

Output:

```
== D @ a21845f523b75adbd3e3f7a62af91294db224ad9   (pre-run)
recorded_cases=9 depth_score=9
== D @ c77c2b7e64d2e356381441ecf94abac03e984606
recorded_cases=9 depth_score=9
```

`git diff --stat c77c2b7e… a21845f5… -- tools/mutate-and-run.sh .ufo/evidence/round-21/coldread .ufo/evidence/round-18`
printed nothing: the runner, the coldread selector, and its round-18 implementation are byte-unchanged base→tip.

### F2 — round-21 coldread monitor: calibration_restraint_score=6, depth_score=9 at tip, equal to base (held)

Argv check: `.ufo/evidence/round-21/coldread/measure.py:103-113` accepts `--selftest`, refuses
`--ledger-file/--ledger-rev/--inputs-overlay` and prefixes (exit 64), then pins the ledger to
`.ufo/evidence/round-21/coldread/ledger.json` and delegates to round-18 `main()`. That parser
(`.ufo/evidence/round-18/measure.py:1516-1537`) takes `--rev`, `--repo`, `--explain`, `--selftest`.
So `--repo <clone> --rev <REV>` is the right invocation.

```sh
cd /tmp
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py \
  --repo /tmp/tameshi-r42w2-ReplayNoHarm-clone --rev <REV>
```

| field | tip a21845f5 (pre-run) | base c77c2b7e |
|---|---|---|
| exit | 0 | 0 |
| calibration_restraint_score | **6** | **6** |
| depth_score | **9** | **9** |
| recorded_cases | 9 | 9 |
| overrides_used | False | False |
| ledger_source / ledger_committed | rev / True | rev / True |
| ledger_guardrail | header_legs 9, regression_calls 9, selftest_tuples 9, unique_recorded_gates 9, lists_agree True | identical |
| shonen marks | `~ ~ ~ ~` (checked 0, asserted 4) | identical |
| coldread sections_covered/total | 60/64 | 60/64 |
| uncovered_headings | same 4 headings | same 4 headings |

The four uncovered headings are identical at both revisions (Mutation-sweep recipe; Restore discipline;
The map; Promotion-evidence calibration — fleet round-1), so the gap is inherited, not caused by wave 1.

### F3 — numstat on the ledger-of-record files: 2 deleted lines, both rewritten as superset rows (held)

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --numstat \
  c77c2b7e64d2e356381441ecf94abac03e984606 a21845f523b75adbd3e3f7a62af91294db224ad9 -- \
  LOG.md SCORECARD.md corpus/QUALITY.md corpus/README.md corpus/SOURCES.md PROVINCE.md SKILL.md SHONEN.md
```

Output (exit 0):

```
49	0	LOG.md
27	0	SCORECARD.md
50	0	corpus/QUALITY.md
15	0	corpus/README.md
10	2	corpus/SOURCES.md
```

PROVINCE.md, SKILL.md, SHONEN.md: unchanged (not listed). A line-prefix check (`git show REV:file`,
base lines == first N tip lines) is True for LOG.md, SCORECARD.md, corpus/QUALITY.md,
corpus/README.md, PROVINCE.md, SKILL.md, SHONEN.md. Those files are append-only base→tip.

Every deletion, all in `corpus/SOURCES.md`:

1. Base `corpus/SOURCES.md:12`, row **S001** (Stryker mutant states and metrics), was replaced at tip
   `corpus/SOURCES.md:12`. The tip row begins with the full base row. The only change is a longer
   destinations cell: `, corpus/knowledge/pit-outcome-vocabulary.md, corpus/knowledge/r42-attribute-and-outflag-destinations.md`.
2. Base `corpus/SOURCES.md:123`, row **S153** (Python `ast` docs), was replaced at tip `corpus/SOURCES.md:123`.
   The tip row begins with the full base row. The only change is a longer destinations cell:
   `, corpus/knowledge/r42-attribute-and-outflag-destinations.md`.

Both new destinations exist at the tip (`git cat-file -t a21845f5…:<path>` → `blob` for each).
No row, claim, locator, grade or date text is lost. The other +8 SOURCES lines are the new rows
S155–S158 plus the two rewritten rows.

## Residual risk / verification gaps

- The coldread `external_inputs` map hashes 1303 files outside the lane, so this monitor's output depends
  on the live host. It matched base at run time, 2026-10-25, but that match is not frozen.
- I did not run `--selftest` for either monitor. This seat only replays the scores.
- Command C (SHONEN mark census) was out of scope. SHONEN.md is byte-unchanged base→tip, so C cannot move.

Verdict: SURVIVES
