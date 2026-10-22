# ReviewSkillRows — round 26 wave 1, SKILL.md ninth case and the two mte-interop registry rows

Verdict: the section's factual claims about the sweep, the pin, the pre-registration and the
replay are all shown by committed evidence, and both registry commands run green live from a
/tmp copy. But the two new registry rows are **rejected by the lane's own registry gate**
(schema-invalid `source` field), so the contract's no-harm companion "every active row held"
fails at the integration revision. Second defect: the knowledge entry the section names does
not exist. Two wording defects in the exit map. Details below.

Method note: no `lsp` device exists in this session's tool inventory, so no language server
was consulted; every finding below rests on executing the lane's own tools at pinned revisions
inside /tmp scratch, plus byte reads of the named files. No lane file was modified; no
installs were made (nothing needed upgrading; uv 0.13.0 and node v24.21.0 were already
present). All sources were opened this session, cited by path.

## Findings

### High — both new registry rows fail `tools/registry-check.py`; the registry gate is red at the integration revision

`tools/registry.json` rows `mte-interop-selftest` and `mte-interop-check` (the last two rows,
`source` at lines 1008 and 1018) carry
`"source": "corpus/lessons/round-25-verifier-spotcheck.md:189-192 (routed item 1)"`.
The checker requires `^[^@]+@[0-9a-f]{7,40}:[0-9]+(-[0-9]+)?$` (`tools/registry-check.py:108`,
error text at :257-261). Observed, in a fresh clone of the lane at HEAD
(a08e85c5d7f899e8a5992e20517edb1a380d79eb, verified with `git rev-parse`):

    python3 tools/registry-check.py --rev a08e85c5d7f899e8a5992e20517edb1a380d79eb
    REGISTRY_CHECK: could-not-evaluate (registry invalid: rows[54].source must be
    <file>@<7-40 hex rev>:<line>, got 'corpus/lessons/round-25-verifier-spotcheck.md:189-192
    (routed item 1)'; rows[55].source must be ... )
    exit=2

The contract's no-harm companion `python3 tools/registry-check.py --rev REV -> every active
row held` (`.ufo/evidence/round-26/contract.json`, C1.no_harm_companions) therefore does not
hold at the revision that introduced the rows. All other fields of both rows passed the same
validation pass (name, kind, argv, expect, timeout_s <= 86400, status, tags — the error list
names only `source`), so the smallest correction is the `source` string in both rows:

    "corpus/lessons/round-25-verifier-spotcheck.md@d4140796f4e48e8ec81b793facba73fbd03b4443:189-192"

d414079 is the commit that added the lesson, and I verified lines 189-192 at that revision
contain exactly routed item 1 (the mte-interop registry-row defect). The `(routed item 1)`
annotation cannot survive the regex; move it to `tags` (e.g. `"routed-r25-item-1"`) or into
the SKILL prose.

### Medium — the knowledge entry the section names does not exist

SKILL.md's ninth-case section (lines 2086-2101) states, in present tense:
`Entry: corpus/knowledge/mutation-case-kumitate-cite-check.md`. No such file exists anywhere
in the lane (`find <lane> -name 'mutation-case-kumitate-cite-check.md'` returned nothing;
`corpus/knowledge/` holds the eight earlier `mutation-case-*.md` entries for legs 1-8 and
nothing for leg 9). The frozen contract makes this load-bearing: C1's `sourced` clause is
"the knowledge entry for the leg cites a SOURCES.md row opened this round"
(`.ufo/evidence/round-26/contract.json`). Until the entry lands, this sentence is a claim the
evidence does not show. Smallest correction: either write the entry in this wave, or reword to
mark it as pending (e.g. "Entry (to land with the wave's closeout): ...") until it exists.

### Minor — the SKILL exit map presents a partial SETUP cause list as the map

The table row's Exits cell says `2 SETUP (missing jsonschema, vendored package integrity, leg
set not equal to the nine ledger legs)`. Those three are real (mte-interop.py:296-299, :181,
:316-319), but the same exit 2 is also raised for at least: node not found (:303), fleet root
not a directory (:275), runner regression exit nonzero (:290), unexpected vendored tar member
(:211), official-metrics timeout or failure (:222-224), spec/results row mismatch (:147),
non-unique @old (:151), wrong pristine-target count (:137), unsupported escape in spec (:104).
The tool docstring (:36) deliberately does not enumerate; the round-24 correction to the
round-21 table (SKILL.md, same section) already established that an over-specific exit-map
cell is a defect because it reads as a safety promise. Suggest "2 SETUP (among other causes:
... )" or dropping the parenthetical to match the docstring.

### Minor — exit codes 2 and 64 are declared but not mapped onto a verdict class

PROTOCOL.md §Gate standard (:379-381) requires every nonzero code "declared in its registry
entry and mapped onto clean | failed | could-not-evaluate". The new row declares `2 SETUP` and
`64 usage` without the class; the lane's own round-21 precedent maps them explicitly
("2 ..., could-not-evaluate; 64 usage, could-not-evaluate", SKILL.md round-21 table). Append
"could-not-evaluate" to both.

## Verified clean (evidence, all commands observed this session)

- Exit map versus docstring: 0/1/2/64 wording matches tools/mte-interop.py:35-36 and the
  parser exits 64 (mte-interop.py:448-450). "at least one leg" correctly paraphrases "M >= 1"
  (zero found legs is SETUP via the leg-set check).
- Expected stdout, live: from a /tmp copy of `tools/` (no lane writes):
  `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --selftest`
  printed `MTE_SELFTEST: 17/17 pass`, exit 0, real 0m0.118s. The `--check --fleet-root
  /home/vgpnk/Projects/shokunin` form printed nine `MTE_LEG <leg>: CONFORMS` lines and
  `MTE_INTEROP: PASS legs_conforming=9/9`, exit 0, real 2m21.9s. Both byte-match the registry
  expects (`MTE_SELFTEST: 17/17 pass`, `MTE_INTEROP: PASS legs_conforming=9/9`) and the
  recorded integration outputs `.ufo/evidence/round-26/after/mte-selftest-a08e85c.stdout` and
  `mte-check-a08e85c.stdout` (17/17 and 9/9, exit 0).
- Timeouts: selftest 300 s against 0.12 s observed; check 900 s against 142 s observed. Both
  generous but safe; no change needed.
- uv dependency: the docstring's example command (mte-interop.py:37-38) is exactly the argv
  in both registry rows and the SKILL table cell. uv 0.13.0 resolved jsonschema==4.25.1 from
  cache; node v24.21.0 satisfies "node >= 18". No network was needed.
- Pin: `git -C kumitate-shokunin ls-tree 1205c662... scripts/cite-check.mjs` → mode 100755;
  `git show 1205c662...:scripts/cite-check.mjs | sha256sum` → 4057344833...c9f; `| wc -l` →
  2537. All three numbers in the SKILL sentence are correct.
- Pre-registration: commit 622d31d contains `cite-check.defects.spec`, `predictions.json`,
  `contract.json` and both counters; its message says "before any mutant run"; the sweep
  artifacts first appear later. Matches the SKILL claim.
- Sweep claims: `sweep/results.tsv` shows exactly 5 KILLED / 5 SURVIVED; every verdict matches
  `predictions.json` (5 predicted KILLED, 5 predicted SURVIVED) — "5/10 killed, 10/10 verdict
  predictions held" holds. `sweep/sweep.txt` shows `62/62 cases passed (hermetic)` for the
  control and each mutant — the "(62 cases)" claim holds, and the runner's leg 9 sandbox
  string (tools/mutate-and-run.sh:1426) is identical to legs 7 and 8 (:1416, :1421), matching
  "the hermetic env -i form of cases 7 and 8".
- Replay claim: the committed evidence `.ufo/evidence/round-26/cite-check/regression-worktree.stdout`
  ends `REGRESSION_CASE js-cite-check: PASS (...)` and `REGRESSION: PASS (cases=9 passed=9; ...)`,
  and its `REGRESSION_TOOL sha256=fb91ef76...` equals the current `tools/mutate-and-run.sh`
  digest, so the recorded replay ran the committed runner bytes. Note only: that run used
  `--keep` (workdir line says "(kept)"); the SKILL's plain `--regression` form prints the same
  REGRESSION_CASE and REGRESSION lines.
- Nine legs wired: in a fresh clone at the integration revision,
  `python3 .ufo/evidence/round-26/c1-measure.py --repo <clone>` printed nine `C1_LEG ...:
  WIRED` lines then `C1_DEPTH: recorded_cases=9 wired_legs=9 depth_score=9`, exit 0. The
  interop side also knows nine legs (LEG_TABLE, mte-interop.py:67-72).
- Table completeness against §Gate standard row fields (PROTOCOL.md:400-401): name, kind,
  entry command, verdict map, self-test spelling, pinned-value path ("reads the runner's
  committed tables"), write scope ("its own scratch and --emit DIR" — confirmed in code:
  mktemp workdir removed on PASS, emit only under the flag), owner. All present, compressed
  into four columns; no missing field.
- registry.json is valid JSON; the two rows sit at the end with `tags: ["new-r26"]`,
  status active, timeouts 300/900.

## Residual risk and verification gaps

- I verified the two rows against registry-check's row schema, not its full row-execution
  battery (it clones and re-runs active rows; the SKILL/registry fixes above are the L1's to
  land and re-verify). The execution evidence that exists is the recorded `after/` outputs
  plus my two live runs of the tool itself.
- `.ufo/evidence/round-26/after/` (the recorded selftest/check outputs cited above) is still
  untracked in the working tree; commit it with the fixes so the frozen-run evidence is
  committed bytes.
- I did not run the runner's full sweep fresh (only the regression replay via the check's
  staged fleet); the sweep verdicts rest on the committed sweep evidence, which is internally
  consistent (results.tsv, sweep.txt, defects.tsv agree).
