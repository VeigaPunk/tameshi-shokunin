# T54W2Read22 — fresh cold read at C1

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Seat: `T54W2Read22` (reader; wave 2)
- Heading: `### Round-21 gate/probe registry — finite environment differential`
- Candidate (C1): `99c3bc88d704566197783f66b211ee0a830e0330`
- Span at C1: `start=1990 end=2129`
- `section_sha256`: `eccd3ec82207fa69cee544f8f4ebfc0f9a473fe7254b8041ae2f5924f8d00a06`
- Findings: 11 (all one class: run-together token / missing space)

Span and sha come from `.ufo/waves/round-54/reader-section.py` run at C1 with
`TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read22`; the same sha was reproduced independently by
calling the frozen round-18 `sectionize()` on the C1 `SKILL.md` blob and hashing
`lines[1989:2129]` with trailing blank lines stripped
(`eccd3ec8…` — see commands below). The section is byte-identical at C0
`59c38109bf11` and at C1 (`diff` of both spans prints nothing; the helper prints the
same sha at both revisions), i.e. the C1 fix pass did not touch these bytes.

## Findings

| # | line | quote (byte-exact) | why |
|---|---|---|---|
| 1 | 1994 | `remain unchanged from33d03b7` | The rev abbreviation is glued to the preceding word (`unchanged from33d03b7` for `unchanged from 33d03b7`), a run-together token of the QUALITY-104 class. |
| 2 | 2002 | `max-share0.40` | The flag default is glued to its value; every other mention in SKILL.md keeps `max-share` a separate token (`grep -oE 'max-share[^ ]{0,10}'` returns 2x `max-share`, 1x `max-share,`, and only this 1x `max-share0.40`). |
| 3 | 2004 | `selftest0 clean/1 failed` | Missing space between `selftest` and the exit arm `0`, although the round-20 row 27 lines above writes the same cell as `selftest 0 clean/1 failed`. |
| 4 | 2012 | `retain the199-entry prefix` | Missing space between the article and the count (`the199-entry` for `the 199-entry`), a run-together token of the QUALITY-104 class. |
| 5 | 2016 | `minedS082` | Missing space between the verb and the source row id, while the same section writes `mined S079` and `mined S084/S085`. |
| 6 | 2027 | `cover16 further schema/accounting guards` | Missing space between the verb and the count (`cover16` for `cover 16`), a run-together token of the QUALITY-104 class. |
| 7 | 2030 | `expected verdict is1/TOTAL_MISMATCH` | Missing space between `is` and the verdict token (`is1/TOTAL_MISMATCH` for `is 1/TOTAL_MISMATCH`). |
| 8 | 2033 | `Normal \`--help\` exits0 as help` | Missing space between `exits` and the code (`exits0` for `exits 0`), a run-together token of the QUALITY-104 class. |
| 9 | 2037 | `minedS083` | Missing space between the verb and the source row id, inconsistent with `mined S079` earlier in the same section. |
| 10 | 2038 | `Source-read credit, including62/62` | Missing space between `including` and the count (`including62/62` for `including 62/62`). |
| 11 | 2045 | `pair is expected1/ARGV_MISMATCH` | Missing space between `expected` and the verdict token (`expected1/ARGV_MISMATCH` for `expected 1/ARGV_MISMATCH`). |

Each quote occurs exactly once in the section bytes (asserted before writing the JSON; `count(q) != 1`
would have aborted the write). All eleven are the same mechanical defect — a space dropped between a
word and a following number/id — and none changes the section's meaning; they are reported because the
round's read criterion names run-together tokens and missing spaces explicitly, and a cold executor
reading `from33d03b7` or `the199-entry` has to stop and re-parse.

No further finding met the "byte-exact quote + command output" bar. In particular the following were
checked and came back clean (an empty cell is a legitimate result, so the sweeps are recorded):

| Check | Result |
|---|---|
| Rev anchor `33d03b7` (`unchanged from …`) | resolves: `git rev-parse 33d03b7^{commit}` → `33d03b716d3edcf1d8656d46d6df61801d232c52`; `3d03b7` alone does not, and the text carries the resolvable one. |
| "frozen C1/C2 scripts and populations remain unchanged from 33d03b7" | true: blob ids of `.ufo/evidence/round-21/c1-survivors.py`, `c2-count.py` and `c2-contract.json` are identical at `33d03b7` and C1; `git diff --diff-filter=M 33d03b7 99c3bc88 -- .ufo/evidence/round-21/` is empty (only additions since). |
| "nine pins/seven profiles" (env-diff row) | `c2-contract.json` has 9 `surfaces` and 7 `required_profiles`; the facade selftest asserts `classified == 9`; `env-diff-selftest` expects `9/9`. |
| "fixtures cover sensitivity, repeat variation and pin refusal" | `tools/env-diff.py` selftest cases: invariant/tz/locale/home/columns/`repeat` (repeat), `missing-bwrap`, `timeout`, `wrong-pin` (pin refusal) — 9/9. |
| env-diff exit map `0/1/2/64` | `main()` returns 0 all classified, 1 short of the surface count, 2 on `ScratchRootUnusable`/setup error, and `Parser.error` exits 64; the C1 tool diff added the `ScratchRootUnusable → exit 2` arm to both run and `--selftest`, so the row's `2 could-not-evaluate` cell is current, not stale. |
| "the c2 fixture is fleet-bound … reads sibling blobs at the fleet root" | true: `tools/round21-measure.py::selftest` extracts `FLEET` from `c2-count.py` and runs `git -C fleet/repo show` for every surface. |
| Round-22 "eight literal public-CLI rejection fixtures", "16 further" | `.ufo/evidence/round-22/measure.py` `CASES` = 8; `.ufo/evidence/round-22/accounting-extra-cases.json` `cases` = 16; `ACCOUNTING_SELFTEST: …/8` and `ACCOUNTING_EXTRA_SELFTEST: …/<len(cases)>`. |
| "expected verdict is 1/TOTAL_MISMATCH" | `wrong-count-expected.json` exists and the round-22 ruler carries the `TOTAL_MISMATCH` rows. |
| Round-23 "frozen ten-case counter", `extra-cases.json`, "expected 1/ARGV_MISMATCH" | `.ufo/evidence/round-23/measure.py` docstring `ten public CLI predicates` and 10 `CASES` tuples; `.ufo/evidence/round-23/extra-cases.json` exists; registry `command-binding-source-read-red-pinned` expects `"finding_ids": ["ARGV_MISMATCH"]`. |
| Round-23 correction: `pin-disposition-read`, `verify-round15`, 41+2 | both rows exist and are `active`; `.ufo/evidence/round-23/replay/observations.json` has 43 rows, all revision-bearing. |
| Round-24 "eleven predicates" | `.ufo/evidence/round-24/measure.py` docstring: `eleven hardening predicates`. |
| Round-24 registry rows / 44/44 / superseded 38/38 row | `command-binding-selftest-r24` expects `44/44 pass`; the three superseded rows exist with `status: superseded`; the superseded row's expect is `38/38 pass`, so it fails against today's 44/44 while `tools/registry-check.py` still executes every superseded row (`Run semantics: every active row and every superseded row RUNS`). |
| "43 stored receipts", `revision_pinned=41` | `observations.json` = 43 rows for a 41+2 split; the two live rows are declared in the requirements, not in the receipt's `revision` field. |
| "49 active rows from round 26 on; seat Read37" | `tools/registry.json`: 56 rows, `Counter({'active': 49, 'superseded': 7})` — current. |
| "`registry-replay-selftest` … expects 10/10 … projection and planning, not `--run`" | registry row expects `REGISTRY_REPLAY_SELFTEST: 10/10 pass`; the tool's selftest invokes `--project` and `--plan` only. |
| `.ufo/evidence/round-24/extra-cases.json` (round24 counterpart) | present. |
| Round-28 correction lines 19 and 52 of `c2-count.py` | `sed -n '19p;52p'` prints `FLEET = Path("/home/vgpnk/Projects/shokunin")` and `blob = show(FLEET / frozen["repo"], want_rev, frozen["path"])` — exact. |
| `corpus/lessons/round-24.md` "Errata E–P" | Errata E, F, G, H(+addendum), I, J, K, L, M, N, O, P all present. |
| `~/.omp/agent/config.yml` and `routemix-spec1.json` `ok: true` | config file exists (16599 B); receipt parses `ok=True`. |
| Round-21 signature rows: `QUALITY43–44`, `QUALITY45`, `QUALITY46`, `QUALITY47`, `QUALITY48`; `S079`, `S028`, `S082`, `S083`, `S084`, `S085` | criteria 43–48 exist as numbered items in `corpus/QUALITY.md` (43:423, 44:432, 45:443, 46:457, 47:472, 48:489); all six S rows exist in `corpus/SOURCES.md`. `QUALITY<n>` without a space is the lane's own convention (7 of 8 occurrences in SKILL.md), so it is not reported. |
| Run-together sweep for the rest of the section | regex `[A-Za-z]{2,}\d[\w/.:]*|\d[\w/.:]*[A-Za-z]{2,}` over the 139-line section: the only non-conventional hits are the eleven listed above; `python3`, `roundNN`, `sha256`, `ReRead03`, `md`/`json` path fragments are the lane's normal forms. |
| Duplicate parenthetical / repeated sentence sweep | `re.findall(r'\(([^()]{4,40})\)\s*\(\1\)')` → none; repeated-sentence Counter over sentences > 40 chars → none; no line carries a double space outside tables. |
| Intra-section contradictions | The one visible tension — the facade write-scope cell "isolated fixture/private clones only" versus the same section's "the c2 fixture is fleet-bound" — is explicitly reconciled 20 lines later by "The write-scope cells cover writes only, not reads" and by the round-28 correction naming the live-object read; no contradiction remains. |

## Artifacts opened (read-only)

- `SKILL.md` at C1 (`99c3bc88…`) and at C0 (`59c38109…`), lines 1990–2129 (`git show`).
- `.ufo/waves/round-54/reader-section.py` (the helper itself, to pin the sha definition).
- `.ufo/evidence/round-18/measure.py` (`sectionize`, exit arms) — read from the C1 blob.
- `.ufo/evidence/round-21/{c2-contract.json,c2-count.py,coldread/measure.py,coldread/ledger.json,f5/receipt.json}`.
- `.ufo/evidence/round-22/{measure.py,accounting-extra-cases.json,wrong-count-expected.json}`.
- `.ufo/evidence/round-23/{measure.py,extra-cases.json,replay/{observations.json,bundle.json,expected.json}}`.
- `.ufo/evidence/round-24/measure.py`, `.ufo/evidence/round-24/extra-cases.json`.
- `.ufo/waves/round-21/{spec1.json,routemix-spec1.json}`, `.ufo/evidence/round-21/routemix-r20-spec1.json`.
- `tools/{env-diff.py,wave-route-mix.py,round21-measure.py,wave-accounting.py,command-binding.py,registry-replay.py,registry-check.py}` (read), `tools/registry.json` (parsed).
- `corpus/QUALITY.md` (criteria list, 43–48 and 104), `corpus/SOURCES.md` (row scan),
  `corpus/lessons/round-24.md` (errata list).
- Existence-checked only (`git cat-file -e`, no content read): `corpus/lessons/round-21.md`,
  `corpus/knowledge/{hermetic-env-differential.md,required-command-binding.md,replay-projection-hardening.md}`.
- `.ufo/evidence/round-54/contract.json` (claims C1/C2, frozen paths).
- `~/.omp/agent/config.yml` (existence only).

## Commands run (all read-only; no git/jj mutation anywhere)

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read22
python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  99c3bc88d704566197783f66b211ee0a830e0330 "### Round-21 gate/probe registry — finite environment differential"
# -> {"start": 1990, "end": 2129, "section_sha256": "eccd3ec8…"}

python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  59c38109bf119d0e9d4f878644a82babc937bc1e "### Round-21 gate/probe registry — finite environment differential"
# -> same start/end/sha  => section unchanged C0 -> C1
diff <(git show 59c38109:SKILL.md | sed -n '1990,2129p') \
     <(git show 99c3bc88:SKILL.md | sed -n '1990,2129p')   # no output

git rev-parse --verify 33d03b7^{commit}          # 33d03b716d3edcf1d8656d46d6df61801d232c52
git rev-parse --verify 3d03b7^{commit}           # fails (only the 7-char form is cited)
git diff --diff-filter=M --stat 33d03b7 99c3bc88 -- .ufo/evidence/round-21/   # empty
git rev-parse 33d03b7:.ufo/evidence/round-21/c2-contract.json \
             99c3bc88:.ufo/evidence/round-21/c2-contract.json                 # 7fc1afaa… == 7fc1afaa…

python3 -c "import json;d=json.load(open('.ufo/evidence/round-21/c2-contract.json'));print(len(d['surfaces']), len(d['required_profiles']))"   # 9 7
sed -n '19p;52p' <(git show 99c3bc88:.ufo/evidence/round-21/c2-count.py)
python3 -c "import json;d=json.load(open('tools/registry.json'));import collections;print(collections.Counter(r.get('status') for r in d['rows']))"  # active 49
python3 -c "import json;d=json.load(open('.ufo/evidence/round-23/replay/observations.json'));print(len(d['rows']))"   # 43
python3 -c "import json;d=json.load(open('.ufo/evidence/round-22/accounting-extra-cases.json'));print(len(d['cases']))" # 16
grep -oE "max-share[^ ]{0,10}" <(git show 99c3bc88:SKILL.md) | sort | uniq -c    # only 1 run-together form
git show 99c3bc88:SKILL.md | sed -n '1977p' | grep -o "selftest 0 clean/1 failed" # space form used 27 lines above
```

The quote-exactness assertion (`body.count(quote) == 1` for every finding, `body` = the canonical
section bytes whose sha is `eccd3ec8…`) ran immediately before the JSON write.

## Tooling

No tool was installed or upgraded for this seat (no channel used). Scratch only:
`/fast/scratch/hyaku/tameshi-r54/T54W2Read22/` (extracted section, C1 `SKILL.md` and `r18.py` copies).
Nothing outside `.ufo/waves/round-54/w2/T54W2Read22.{json,md}` was written in the lane.
