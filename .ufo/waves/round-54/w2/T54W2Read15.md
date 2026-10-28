# T54W2Read15 — fresh read at C1

- Heading: `## Effective expectation reconciliation — round 14`
- Candidate: `99c3bc88d704566197783f66b211ee0a830e0330`
- Section span: start 1589, end 1622 (sectionized bytes = 33 lines, 1589–1621; trailing blank stripped)
- `section_sha256`: `6110606ea4a977c70f0fa67ef8bdc97b4a4d2e51e9e8c2a96e984c7886376cbe`
- Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W2Read15` (`TMPDIR` set there for every command)

## Findings (2)

### 1. `before either named round` — the referent does not resolve

Byte-exact quote (line 1608):

> `the runner in round 16, the bash witness-study tool in rounds 18 and 21, and `tools/pin-disposition.py` in round 17, before either named round`

Why: `either` presupposes exactly two rounds, but the same parenthetical names four (16, 17, 18, 21) for the
three moved inputs and the witness-study tool moved in rounds 18 and 21, so the trailing clause has no
consistent antecedent and names nothing an executor can check.

Evidence that the preceding list itself is accurate (so the defect is the trailing clause, not the list):
the three stale inputs of `.ufo/evidence/round-13/expected.json` at C1 are exactly
`tools/mutate-and-run.sh`, `tools/bash-witness-study.py`, `tools/pin-disposition.py` (3 of 13), and their
first post-round-14 moving commits are round 16 (`05a2247`), rounds 18/21 (`58e5d53`, `370f2df`) and
round 17 (`2a22ade`) respectively.

### 2. `which the commands below name` — the commands do not name that file

Byte-exact quote (line 1606):

> `which the commands below name`

Why: neither command in the recipe (`.ufo/evidence/round-14/dispositions-before.json` in step 2,
`.ufo/evidence/round-14/dispositions.json` in step 3) contains `expected.json`; the path appears only as
the `expected_file` field of the tool's JSON output, so the commands below do not name it as the sentence
asserts.

## Checks that came back clean (not filed as findings)

- Table shape: header + 5 rows, 3 columns each (1596–1602), no duplicate parenthetical, no missing space,
  no run-together token inside the section.
- `twelve expected checks, thirteen inputs` → `.ufo/evidence/round-13/expected.json` has
  `expected_checks`: 12, `inputs`: 13. Holds.
- `both manifests now return 2 expected_input_digest_mismatch` at `--root .` → both manifests exit 2 with
  exactly that `kind` (run on an extracted C1 tree).
- `three of its thirteen inputs are stale at the live bytes` → computed sha256 of all 13 pinned inputs
  against C1 bytes: exactly 3 stale (`tools/pin-disposition.py`, `tools/bash-witness-study.py`,
  `tools/mutate-and-run.sh`). Holds, including the round attributions.
- `git archive 28aeef4` replay: `dispositions-before.json` → exit 1 with finding
  `producer_before: stdout lacks 'summary preserves top-level exposed declaration kind'`;
  `dispositions.json` → exit 0, `effective 11 / superseded 1`, both oracle replacement rows effective. Holds.
- `verification.json` `initial 18-of-34 fixture failures` → its `disposition_selftest` stdout carries
  `SELFTEST: FAIL (18/34 failed: ...)`. `verification-final.json` holds
  `disposition_selftest exit 0`, `unresolved_before 1/1`, `resolved_after 0/0`. Holds.
- `round 14, runner 75ed934d…` → resolves as the sha256 prefix of `tools/mutate-and-run.sh`
  (`75ed934dc86360f5…`, pinned in `.ufo/evidence/round-13/pin-manifest.json`); not a git object, but the
  section labels it a runner digest, so the anchor is carried by committed evidence.
- `the round15 registry below` → `### Round-15 gate/probe registry` (line 1702) carries the
  `retained invocation-context gate`. Holds.
- `Live-tree form: the round-17 re-pin section (round-18 manifests since then)` → `## Live-tree re-pin…
  — round 17` (line 1840) uses `.ufo/evidence/round-18/dispositions*.json`. Holds.
- Sources: `corpus/lessons/round-13-verifier-spotcheck.md` items 1–3 exist under `## Routed defects and
  residuals`; `corpus/knowledge/incremental-pin-disposition.md` §8 is `Empirical correction and backlink —
  round 14`; census rows S049 and S003 match the glosses used.
- `.ufo/evidence/round-14/capture-context.py` and the retained `.ufo/evidence/round-14/context-receipt.json`
  both exist at C1; the script writes that receipt path, matching step 5's "must not be run again" reason.

## Artifacts opened (all at C1 unless noted)

- `SKILL.md:1589-1622` at `99c3bc88d704566197783f66b211ee0a830e0330` (section bytes; also at C0
  `59c38109bf119d0e9d4f878644a82babc937bc1e` for diff context only)
- `.ufo/evidence/round-13/expected.json`
- `.ufo/evidence/round-13/pin-manifest.json`
- `.ufo/evidence/round-14/dispositions-before.json`
- `.ufo/evidence/round-14/dispositions.json`
- `.ufo/evidence/round-14/verification.json`
- `.ufo/evidence/round-14/verification-final.json`
- `.ufo/evidence/round-14/capture-context.py`
- `.ufo/evidence/round-14/context-receipt.json`
- `tools/evidence-disposition.py`
- `corpus/SOURCES.md` (rows S003, S048, S049)
- `corpus/lessons/round-13-verifier-spotcheck.md`
- `corpus/knowledge/incremental-pin-disposition.md`
- `SKILL.md:1702-1733` (round-15 registry) and `SKILL.md:1840-1875` (round-17 re-pin), `SKILL.md:1881-1925`
  (round-17 input-keyed credit, which supersedes the earlier sha-only credit line)
- `.ufo/waves/round-54/reader-section.py`, `.ufo/evidence/round-18/measure.py` (`sectionize`, via the reader)

## Commands run and outcomes

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read15
python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  99c3bc88d704566197783f66b211ee0a830e0330 "## Effective expectation reconciliation — round 14"
→ {"heading": "## Effective expectation reconciliation — round 14",
   "cand": "99c3bc88d704566197783f66b211ee0a830e0330", "start": 1589, "end": 1622,
   "section_sha256": "6110606ea4a977c70f0fa67ef8bdc97b4a4d2e51e9e8c2a96e984c7886376cbe"}
```

```
git show 99c3bc88…:SKILL.md | sed -n '1589,1622p'          # read + cat -A pass for invisibles
```
Output: the 33-line section; only em dashes and backticks; no double space, no adjacent parentheses,
no run-together token inside the section.

```
git show 99c3bc88…:SKILL.md | sed -n '1589,1622p' > sec.txt
python3  # join lines, strip trailing blanks -> sha256
→ 6110606ea4a977c70f0fa67ef8bdc97b4a4d2e51e9e8c2a96e984c7886376cbe (33 lines)
```
Both filed quotes test `in` this exact byte string → True.

```
grep -n "expected" sec.txt
11 (table row 2), 18 (step 1, the "commands below name" claim), 20 (step 2)
```
No command line in the recipe contains `expected.json`.

```
python3 -c 'compare .ufo/evidence/round-13/expected.json inputs sha256 vs C1 blobs'
→ OK ×10, STALE: tools/pin-disposition.py, tools/bash-witness-study.py, tools/mutate-and-run.sh
→ stale count: 3 of 13
```

```
git show 99c3bc88…:.ufo/evidence/round-13/expected.json | python3 -c ...
→ inputs: 13  expected_checks: 12
```

```
git show 99c3bc88…:.ufo/evidence/round-14/verification.json | python3 -c ...
→ disposition_selftest exit 1 / expected 0, stdout contains "SELFTEST: FAIL (18/34 failed: ...)"
git show 99c3bc88…:.ufo/evidence/round-14/verification-final.json | python3 -c ...
→ [('disposition_selftest',0,0), ('unresolved_before',1,1), ('resolved_after',0,0)]
```

```
git archive 99c3bc88… | tar -x -C $TMPDIR/c1 ; git archive 28aeef4 | tar -x -C $TMPDIR/a28
cd $TMPDIR/c1
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json
  → exit 2, error.kind = expected_input_digest_mismatch
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json
  → exit 2, error.kind = expected_input_digest_mismatch
cd $TMPDIR/a28
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json
  → exit 1; finding: producer_before: stdout lacks 'summary preserves top-level exposed declaration kind'
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json
  → exit 0; counts effective 11, superseded 1, passed 11, failed 0; rows producer_before_oracle and
    producer_after_oracle effective
```

```
git log --oneline -8 -- tools/mutate-and-run.sh        → round-16 05a2247, round-30, round-51 (first post-14 move: round 16)
git log --oneline -8 -- tools/bash-witness-study.py    → round-18 58e5d53, round-21 370f2df
git log --oneline -8 -- tools/pin-disposition.py       → round-17 2a22ade
git cat-file -t 75ed934d                                → "Not a valid object name"
git grep -n "75ed934d" 99c3bc88…                        → sha256 75ed934dc86360f5… of tools/mutate-and-run.sh
```

```
cd /home/vgpnk/Projects/shokunin
bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
→ exit 0 (17 lines; 15 duplicate-url warnings W04 S268/S274 etc.; final line "tameshi ok …/corpus/SOURCES.md")
```

No lane file was edited; the only writes were `.ufo/waves/round-54/w2/T54W2Read15.{json,md}`.
No tool install/upgrade was needed, so no tool record.
