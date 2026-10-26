# T49Read14 — C1 reader, `## Repeated controls and gate registry — round 12` (ordinals 0-4)

Lane `tameshi-shokunin`, base `8ca67421111fa354b47b803358391d0b07fc6db9`. Item: read every pointer of the
section at base against its target, decide `holds` / `stale` / `unresolved` / `absent`, and quote located text.
Deliverable: `.ufo/waves/round-49/w1/T49Read14.rows.json` (5 rows). No row needed a `proposed_fix`: all five hold.

## Method

- Pointer set: `python3 .ufo/evidence/round-49/c1/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 8ca67421111fa354b47b803358391d0b07fc6db9 --list` → 90 pointers, of which **5** are in this heading (`0-4`), byte-identical to `.ufo/evidence/round-49/control/c1-pointers-at-base-8ca67421.json` (sha256 `92a2e532…`).
- Section body is SKILL.md lines **1479-1497**: the next heading is `### Gate/probe registry` at 1499, which `sectionize` treats as a new section, so the registry table's many paths are *not* in this pointer set. Confirmed by the frozen `section_sha256`: joining lines 1479-1497 and popping the trailing blank reproduces `f994914ddd4d310f85f47c28aea2046cd39e3a64efccb20ac45061d8cb20ae56`.
- Excerpts tested with the counter's own rule (`norm()` = `re.sub(r'\s+',' ',t).strip()`, `EXCERPT_MIN=24`, `EXCERPT_MAX=400`, path pointer → whole blob, sid pointer → the registry row line). All five excerpts occur; all five claims are verbatim substrings of the section. Receipt: `.ufo/waves/round-49/w1/T49Read14.excerpt-check.txt`.
- Only `--list` was run against the lane. No verdict invocation. No fixture repo created. No tool installed.

## Pointer verdicts

| ord | raw | skill line | target | verdict |
|---|---|---|---|---|
| 0 | `corpus/knowledge/repeated-control-precondition.md` | 1481 | note exists, 114 lines | holds |
| 1 | `.ufo/evidence/round-12/verification-final.json` | 1482 | receipt exists, 180 lines | holds |
| 2 | `tools/repeat-control.py` | 1492 | tool exists, 913 lines | holds |
| 3 | `S004` | 1481 | `corpus/SOURCES.md:15` | holds |
| 4 | `S026` | 1481 | `corpus/SOURCES.md:37` | holds |

**#0 — holds.** The clause is the attribution `Source: S004/S026 and \`corpus/knowledge/repeated-control-precondition.md\`;` (SKILL.md:1481). The target carries exactly this material: `repeated-control-precondition.md:26` states the section's calibration thesis ("Stream agreement is stronger than pass/fail stability — and still weaker than determinism.") and `:35` describes this CLI (`--runs N --out DIR -- COMMAND ARG...`, floor 3, DIR must not exist). Shown by `git -C LANE show BASE:corpus/knowledge/repeated-control-precondition.md | sed -n '26p;35p'`.

**#1 — holds.** Clause `runtime evidence: \`.ufo/evidence/round-12/verification-final.json\`.` (SKILL.md:1482). The file is the gate's runtime receipt, not a stub: check `real-pristine-three-controls` (`:47-76`) records `REPEAT_RUN 1/2/3 exit=0 … REPEAT_COMPARE identical=yes runs=3` (`:73`), `red-before-single-control-mutant` (`:77-98`) records the honest failed oracle, `green-after-restored-repetition` (`:99-119`) the repaired one, and the file-level result is `"passed": true` (`:176`). Shown by `git -C LANE show BASE:.ufo/evidence/round-12/verification-final.json | grep -n '"name"\|REPEAT_COMPARE'`.

**#2 — holds.** Clause `run \`python3 tools/repeat-control.py --runs 3 --out /tmp/tameshi-r12-controls-UNIQUE -- COMMAND ARG...\`;` (SKILL.md:1492). The tool's own usage string is that form (`tools/repeat-control.py:13`), the floor of three is enforced at `:261-262` (`--runs must be >= 3`), and `:317` refuses an existing `--out` — the sentence "The output directory must not exist." No drift in flags, floor or refusal. Shown by `git -C LANE show BASE:tools/repeat-control.py | sed -n '13p;261,262p;317p;874,878p'`.

**#3 — holds.** `S004` resolves to exactly one row, `corpus/SOURCES.md:15`, and its range `[[15,15]]` has not drifted. The row teaches cargo-mutants outcome semantics and the reliable-baseline precondition ("tests must first pass reliably in a copied tree"), and lists `corpus/knowledge/repeated-control-precondition.md` in `used-by`. Shown by `git -C LANE show BASE:corpus/SOURCES.md | sed -n '15p'`.

**#4 — holds.** `S026` resolves to exactly one row, `corpus/SOURCES.md:37`, range `[[37,37]]` not drifted. The row teaches the flakiness precondition ("about 1.5% of test runs are flaky; about 84% of pass-to-fail transitions involve a flaky test") and lists the same note in `used-by`. Shown by `git -C LANE show BASE:corpus/SOURCES.md | sed -n '37p;140p'`.

## Findings outside the pointer set (no row; for the L1)

**F1 — `corpus/SOURCES.md:140` supersedes `S026` for anchor/quote only; the section cites `S026` alone.** Row `S265` (opened 2026-10-26, status `mined`) reads "supersedes S026's anchor and quote only … re-anchored to the 2026-10-26 bytes". This is *not* staleness under the frozen definition (the S026 row still resolves, is still `mined`, and still supports the clause), but if the L1 wants the current anchor, swapping `S026` → `S265` in SKILL.md:1481 keeps the section at 5 pointers (floor 5) and needs one re-derived row at `SOURCES.md:140`. Shown by `git -C LANE show BASE:corpus/SOURCES.md | sed -n '140p'`.

**F2 — the cited note's own refs into the tool have drifted, so the section's source contains stale line numbers.** `repeated-control-precondition.md:35` cites `tools/repeat-control.py:245-247` for the `--runs` floor; at base `:245-247` is `--out` argument parsing and the floor is `:261-262`. `repeated-control-precondition.md:58` cites ":115-123 (finding map), :191-205 (precedence), :337-435 (snapshot validator), :545 (selftest)"; at base those are `:122-130` (`EXIT_BY_ID`), `:206` (`classify`), `:449` (`snapshot_mode`), `:592` (`selftest`), and its "30,557 B, sha256 29d80254…" is the earlier revision — the base tool is 35,454 B / `296fe566…`, which the note's own §6 addendum records correctly (`:84`). The SKILL clause is an attribution, not a line ref, so row #0 holds; the drift lives in the note, which is not one of the seven C1 target sections, so no SKILL correction follows from it. Shown by `git -C LANE show BASE:corpus/knowledge/repeated-control-precondition.md | sed -n '35p;58p;84p'` and `git -C LANE show BASE:tools/repeat-control.py | sed -n '122,130p;206p;261,262p;449p;592p'`.

**F3 — SKILL.md:1483 names the runner by a superseded leg count.** "This is a standalone precondition check, not a change to the six-leg runner." The runner gained a seventh leg at round 16 (`repeated-control-precondition.md:105-114`: "§3.1's runner pin … was true at round 12. At round 16 the runner gained a seventh leg (sha256 `89722ddb…`, legs at `:85-91`)"). The *claim* (this check is not a mutation leg) stands; only the noun phrase is outdated, and the same section's `### Gate/probe registry` already disclaims conformance assertions about the historical runner. Not pointer-backed → no row and no required correction; flagged because C1 is the calibration surface that would carry such a wording fix. Evidence: `git -C LANE show BASE:SKILL.md | sed -n '1483p'`, `git -C LANE show BASE:corpus/knowledge/repeated-control-precondition.md | sed -n '105,114p'`.

## Receipts (all inside the lane, at base)

- `git -C LANE show BASE:SKILL.md` → 2136 lines, 166,524 B, sha256 `2381873162fc21db756f8e8744d85aaa6dfc245a01175d5d5ac66557f617d35a`.
- `git -C LANE show BASE:corpus/knowledge/repeated-control-precondition.md` → 114 lines, 14,142 B, sha256 `e56f5876fa5af3e83b8f13d4076d566f27c1897a4bb5c67c8e2f52406ccf2ee7`.
- `git -C LANE show BASE:corpus/SOURCES.md` → 490 lines, 116,284 B, sha256 `7e99c6a068521cf3e3d581a52a74e8f58551309ecb2c3a284dda9b9c17235c7e`.
- `git -C LANE show BASE:.ufo/evidence/round-12/verification-final.json` → 180 lines, 21,047 B, sha256 `9f3d117af3b613d0a00b7d0a623d31136e36f53cb6fcb5626e42cf0c6e022201`.
- `git -C LANE show BASE:tools/repeat-control.py` → 913 lines, 35,454 B, sha256 `296fe566dc59380b6baa518b61cef92fe3c7af09d538b2dde9e7f4af1b8cbc25`.
- Deliverables: `T49Read14.rows.json` (sha256 `aebc37cc1b68fc1c917743db13bcda51726c64093e3356f24bbf39a52a48205a`, 5 rows, all `base_verdict: holds`, `verdict: holds`), `T49Read14.excerpt-check.txt`.

## Limits

- I did not decide C1; I produced read rows. The counter's semantic-support gap (a located excerpt is not proof the sentence is true) is exactly why these notes name the supporting sentence, not just the file.
- Scratch `/fast/scratch/hyaku/tameshi-r49/T49Read14/` held only exported base blobs and was removed; no `/tmp` path is cited. Nothing under `/home/vgpnk/.local/state/` was read, and the C2 witness/control stdouts were not opened.
- Tooling: no install or upgrade was needed or performed.

## Summary

Section `## Repeated controls and gate registry — round 12` has 5 frozen pointers; all five **hold** at base, none stale, none unresolved, none absent, so this seat proposes no SKILL.md correction and this section needs no `proposed_fix`.
#0 the cited note exists and carries the repeated-controls precondition and this CLI (§2:26, §3.1:35).
#1 `verification-final.json` is real runtime evidence: three identical pristine control runs plus a failed/repaired oracle check.
#2 the recipe's argv, the `--runs >= 3` floor (:261-262) and the "output directory must not exist" refusal (:317) are all still the tool's.
#3/#4 `S004`/`S026` resolve to one row each at `SOURCES.md:15`/`:37`, ranges undrifted, both teaching the section's preconditions and listing the cited note in `used-by`.
Advisory, not corrections: `S265` (`SOURCES.md:140`) supersedes `S026`'s anchor/quote only (swap keeps 5 pointers); the cited note's internal tool refs have drifted (`:35`, `:58`); SKILL.md:1483 still says "six-leg runner" after round 16's seventh leg.
