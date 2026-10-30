# T58W1Panel08 — blind base-tree review

Base: `2a32aa8228d5f86a85c81a923a3148bf792a9538`.
Axes: status accuracy, evidence provenance, historical-repair versus prospective-prevention, blind independence.

## Results

| Item | Verdict | Resolving commit |
|---|---|---|
| R54.9 | fixed | `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` |
| R54.10 | fixed | `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` |
| R55.1 | open | — |
| R55.2 | declined | — |
| R55.3 | fixed | `2f5512a8ab0771fb2eee463ec16db359174f5edd` |

These are recommendations about the five frozen items, not claim admission.

## Isolation and command evidence

Executed:

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r58/T58W1Panel08
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone
test "$(git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone rev-parse --show-toplevel)" = /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone
git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone checkout --detach 2a32aa8228d5f86a85c81a923a3148bf792a9538
```

Output: clone completed; `HEAD is now at 2a32aa82 round-57 verifier spot-check (integrator, hyaku): non-author admit/reject`; exit 0. All subsequent substantive tree reads were in that detached clone. No lane content edits, staged patches, runtime executions, or installations.

`read xd://lsp` returned `No such tool: xd://lsp`; consequently definition/references/diagnostics could not be requested. Literal text searches below are not semantic proof. Records were selected from the working-tree `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-58/c1/defects.json` using `.defects[] | select(...)` for precisely the five assigned IDs. The initial `.[]` query failed due to the wrapper object; the corrected query returned all five records.

In commands below, all paths are absolute. `read` and `grep` denote the actual specialized tools, not shell aliases. Report excerpts below preserve observed outputs; unrelated output is omitted.

## R54.9 — fixed

Executed `read /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone/SCORECARD.md:2688-2702`:

```text
2692:**ER-R54-9 - wave-table numbers and the staged-package count.**
2693:Old: 4 reviewers (report), a 26.3 % attack share, "the other 84 staged entries".
2694:Corrected: `reviewers=5 attack=21/76 seats=76` (27.6 %) from
2695:`.ufo/waves/round-54/w1-registry.json`, and `staged=81` staged `.md` files under
2696:`merge/tameshi/knowledge` (read-only count of the source package).
```

Executed `read /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone/.ufo/waves/round-54/w1-registry.json:1-32`:

```text
7: "seats": 76,
8: "attack_seats": 21,
16:  "reviewer": 5,
```

Executed:

```sh
git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone blame -L 2692,2702 2a32aa8228d5f86a85c81a923a3148bf792a9538 -- SCORECARD.md
git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone log --format='%H %s' -G 'ER-R54-9|ER-R54-10|c2-integrated|C2_R55|cold-read floor re-bound' 2a32aa8228d5f86a85c81a923a3148bf792a9538 -- SCORECARD.md
```

Blame attributes every line 2692–2702 to `9cf0146b`; log resolves that commit to `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`, subject `round-55: C0` (subject explicitly includes the ten round-54 record corrections). The exact numeric erratum resolves the described report defect, including its staged-package count; I did not independently recount the external source package.

## R54.10 — fixed

Same read/blame/log commands as R54.9 locate the correction and its introducing commit:

```text
2698:**ER-R54-10 - a quote under the wrong receipt.**
2699:Old: `CTL_R53 (58/64, rekeyed=0/30)` cited to `control/controls-a.stdout`.
2700:Corrected: `controls-a.stdout`'s `CTL CTL_R53` line prints `rekeyed=0/7`; the
2701:`rekeyed=0/30` reading belongs to `control/r53-counter-at-88afa941.stdout`, the
2702:round-53 counter's own bytes run at the round-53 final revision.
```

Executed `read /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone/.ufo/evidence/round-54/control/controls-a.stdout:1-25`:

```text
3:CTL CTL_R53 C1_R54: rev=88afa9415454 c0=none credited=58 lost=6 rekeyed=0/7 readers=0/7 monitor=6/58 unstable=0 total=4 C1_R54_PASS=false
```

The report now assigns the denominator to the correct receipt rather than silently deleting the historical misquote.

## R55.1 — open (actionable historical evidence gap)

Executed `read /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone/.ufo/evidence/round-55/after/c2.stdout:-12`. It ends at line 28:

```text
27:EXPLAIN empty  context-capture --check            rc=0  ok
28:EXPLAIN usable repeat-control --selftest          rc=0  ok
```

Executed:

```sh
git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone log --format='%H %s' -- .ufo/evidence/round-55/after/c2.stdout .ufo/reports/round-55/tameshi.md
```

Output was one commit:

```text
875bb75693bd659c5c9794a09a1137c689778390 round-55: remaining wave-2/3 seat deliverables and receipts as they stand (the round filed before every seat settled; nothing here is a claim input, they are the falsification record)
```

A literal corrective-disposition sweep used `grep` pattern `R55\.1|R55\.2|c2-integrated\.out|08d64e946006|T55W1ScribeSkill` over absolute clone paths `corpus`, `LOG.md`, `SCORECARD.md`, and `.ufo/evidence/round-56`. Relevant output: `corpus/lessons/round-56.md:102` calls R55.1 `FIXED by C2's deciding gate`; the actual description is prospective gate 0c, not a new round-55 measurement. `read /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone/.ufo/evidence/round-56/deciding-run.sh:133-166` confirms:

```text
156:# gate 0c: the verdicts this run just produced must name the certified revision.
157:python3 "$SCR/gate/gate.py" --lane "$LANE" --certified "$REV" \
158:  --receipt "$OUT/c1.stdout:verdict:C1_R56_PASS=" \
159:  --receipt "$OUT/c2.stdout:verdict:C2_R56_PASS=" \
```

This gate checks newly produced **round-56** verdicts. It neither supplies the missing `C2_R55` verdict at `4c04c1d3` nor restates round 55's measurement at C0. The claimed preventive fix must not substitute for the item’s requested historical correction. The original fleet report is not present at the lane's corresponding `.ufo/reports/round-55` path; I did not read outside the assigned tree to reconstruct it. No counter was rerun and no absent run is asserted green.

## R55.2 — declined (recorded reasoned rejection)

Executed `read /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone/corpus/lessons/round-57.md:7-28`:

```text
19:- **R55.2 — the quoted C2 total is not in the report.** The round-55 verifier
20:  (`corpus/lessons/round-55-verifier-spotcheck.md:123-124`) quotes the scribe report as
21:  `grammar=9/9 … note=9/9 skill=1/1 total=0`. That string does not occur in
22:  `.ufo/waves/round-55/w1/T55W1ScribeSkill.md`. The report quotes the 9-mode run as
23:  `total=1 C2_R55_PASS=false` (its line 148; receipt `c2-integrated.out:44`, `rev=08d64e946006`).
24:  Its only `total=0` (line 157) is the earlier 8-mode run, `grammar=8/8 … total=0 C2_R55_PASS=true`,
25:  labelled as earlier. The 9-mode run is `total=1`, verdict false. This line answers the item; the
26:  round-55 wave report is not edited.
```

That is a recorded, item-specific reasoned refusal exceeding 40 characters, so I classify it as **declined**, not as a newly instrumented fix. I did not adopt the lesson's assertion that candidate ledger rows exist; the panel does not inspect those rows.

Executed `read /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone/.ufo/waves/round-55/w1/T55W1ScribeSkill.md:138-163`:

```text
146:```
147:C2_R55: rev=08d64e946006 grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0
148:        docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false
154:**Counter, pre-amendment-6 bytes, earlier content** (`-receipts/c2-demo.out`,
155:8 allocating modes, counter sha `d6ca1d851bb0037368c304f4d80254f7dc5bf76b1c3119cdf0f2a64bca95631a`
157:commit 9de7deac0d72`): `grammar=8/8 … total=0 C2_R55_PASS=true` — the same
```

Executed `read /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone/.ufo/waves/round-55/w1/T55W1ScribeSkill-receipts/c2-integrated.out:38-46`:

```text
44:C2_R55: rev=08d64e946006 grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false
```

Executed `git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone blame -l -L 19,26 2a32aa8228d5f86a85c81a923a3148bf792a9538 -- corpus/lessons/round-57.md`; every displayed line is attributed to `adf87899c70d616140a81185a8f9acbbdfb30392`. Declined JSON commit is null as allowed by the contract.

Residual: the frozen item refers to a report quoting the scribe, while the decline checks the scribe itself. The external original round report was not available in the detached lane. Therefore the decline is established as a **recorded reasoned disposition**, not independent proof that every version of the external report quoted accurately.

## R55.3 — fixed

Executed `read /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone/.ufo/evidence/round-56/after/c1.stdout:1-20`:

```text
1:EXPLAIN arm1-precheck exit=0 COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=1b44bace0974 cand_credited=64 lost=0 ok
2:EXPLAIN arm2-monitor covered=64 score=8 box3=True
3:EXPLAIN arm3-rekey dirs=['rekey-r56-c0137451f5b7'] c0=c0137451f5b7f22d65f748fc69f1b181f55e1378
4:EXPLAIN arm4-readers 18/18
5:EXPLAIN arm6-restate row_score=8 row_commit=c1dd23b3f83f score_at_row=8 evidence='round-21 cold-read monitor `calibration_restraint_score`; tw' round='56'
6:C1_R56: rev=1b44bace0974 c0=c0137451f5b7 credited=64 lost=0 rekeyed=18/18 readers=18/18 monitor=8/64 unstable=0 restate=8 total=0 C1_R56_PASS=true
```

Executed `read /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone/.ufo/waves/round-56/integration/bind-precheck.stdout:1-8`:

```text
1:COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=c1dd23b3f83f cand_credited=64 lost=0 ok
```

Executed:

```sh
git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone show --format=fuller 2f5512a8ab0771fb2eee463ec16db359174f5edd -- SCORECARD.md
```

Observed introducing patch adds `### Standing axis table — calibration re-stated at the C1 bind` and:

```text
+| calibration | 8 | Round-21 cold-read monitor `calibration_restraint_score`; two points per restrained, evidence-linked `[~]` SHONEN box, with box 3 requiring the full page: `64/64`, `box3=true` | `c1dd23b3f83f5dff676c4a4482498e87345375ef` | 56 |
```

The bind was already in the parent; this commit supplies the second owed component, the standing-row restatement, completing the original repair. A later regression is explicitly superseded in the base tree: `read /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone/SCORECARD.md:2757-2799` returns:

```text
2795:| calibration | 8 | round-21 monitor: covered=64/64, box3=True; binder phase2 exit 0 | `bc3c8895b75aec65e3006193d0c1857641dbb385` | 57 continuation |
2797:This supersedes the continuation's pre-bind 46/64 warning above. Reader
2798:provenance gaps and six marked minor findings remain limits on the score.
```

I did not open the forbidden round-57 wave artifacts to validate that later bind. The round-56 repair is supported by the allowed committed receipts quoted above; current 64/64 is supported by the allowed base scorecard record, not a fresh monitor execution.

Both fixed-at-base commits were checked with:

```sh
git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone merge-base --is-ancestor 2f5512a8ab0771fb2eee463ec16db359174f5edd 2a32aa8228d5f86a85c81a923a3148bf792a9538
git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel08/clone merge-base --is-ancestor 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb 2a32aa8228d5f86a85c81a923a3148bf792a9538
```

Both succeeded silently (combined command exit 0).

## Verification gaps, independence, cleanup

No forbidden round-57 wave files, round-57 panel, other round-58 seat output, or candidate ledger rows were opened. Git commit-stat output incidentally named round-57 wave paths; their contents were not read. No tests or counters were executed, no saturation or runtime admission is claimed. Literal sweeps and committed receipts are the evidence. No tools installed or updated.

Scratch cleanup executed:

```sh
rm -rf -- /fast/scratch/hyaku/tameshi-r58/T58W1Panel08 && test ! -e /fast/scratch/hyaku/tameshi-r58/T58W1Panel08 && printf '%s\n' 'SCRATCH_REMOVED=/fast/scratch/hyaku/tameshi-r58/T58W1Panel08'
```

Output: `SCRATCH_REMOVED=/fast/scratch/hyaku/tameshi-r58/T58W1Panel08`, exit 0. Scratch was deleted before handoff.

Self-evaluation: accuracy 4 (external round-55 report unavailable; decline caveat explicit), completeness 4 (all five IDs, source excerpts and fixing ancestry; current monitor not freshly executed), clarity 4 (historical versus prospective distinction stated), actionability 4 (R55.1 names the exact still-missing evidence), conciseness 4 (long command record retained to satisfy auditability). Overall 4.0. Highest-impact improvement would be authorized access to the original external report for the R55.2 semantic distinction; it does not change the observed recorded decline. The user can inspect the cited excerpts and machine-readable verdicts directly.
