# T54W2Read19 — fresh read at C1

- Section: `## Live-tree re-pin and entry-command monitor — round 17`
- Candidate: `99c3bc88d704566197783f66b211ee0a830e0330` (C1)
- `section_sha256`: `6395900104ed76b6f9dbfae1bb33384197982447e1db7dbaf89bf2b6b1b9beac` (lines 1840-1870 of `SKILL.md` at C1; recomputed from the bytes and matched)
- Findings: **1**

## Reader setup

```
mkdir -p /fast/scratch/hyaku/tameshi-r54/T54W2Read19
TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read19 \
python3 .ufo/waves/round-54/reader-section.py \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  99c3bc88d704566197783f66b211ee0a830e0330 \
  "## Live-tree re-pin and entry-command monitor — round 17"
```

Output:

```
{"heading": "## Live-tree re-pin and entry-command monitor \u2014 round 17", "cand": "99c3bc88d704566197783f66b211ee0a830e0330", "start": 1840, "end": 1871, "section_sha256": "6395900104ed76b6f9dbfae1bb33384197982447e1db7dbaf89bf2b6b1b9beac"}
```

Byte check (sectionize rule: heading line through the line before the next heading, trailing blank lines stripped, `\n`-joined, no trailing newline):

```
$ git -C <lane> show 99c3bc88d704566197783f66b211ee0a830e0330:SKILL.md | sed -n '1840,1870p' > sec.txt
$ python3 -c "...sha256('\n'.join(lines))..."
31 lines, 6395900104ed76b6f9dbfae1bb33384197982447e1db7dbaf89bf2b6b1b9beac
MATCH True
```

The section body (31 lines) is exactly: heading, `Sources:` paragraph, the 7-row
`Evidence condition | Decision | Error pattern / limit` table, `Recipe, from this lane root`, and
steps 1-4. The `### Round-17 gate/probe registry — re-pin and monitor` sub-table is a separate
section at C1 (line 1872) and is out of my span.

## Finding 1 — the round-54 re-pin under-reaches its own cited scrub

Quote (byte-exact substring of the section, verified with `str.count() == 1`):

> and scrubs inherited `GIT_*` (`tools/evidence-disposition.py:385-395`; selftests `v2-historical-replace-ref`, `v2-gitdir-env` expect exit 0; grafts by code reading only)

Why: the anchored range ends at the `GIT_ENV_OVERRIDES` closing brace; the clause's second object,
"scrubs inherited `GIT_*`", is executed twelve lines later, outside the anchor.

Evidence:

```
$ git -C <lane> show 99c3bc8:tools/evidence-disposition.py | sed -n '385,395p' | nl -ba -v385
   385	# ------------------------------------------------- historical input reading
   386	
   387	# G4: every git subprocess runs without inherited GIT_* state, without replace
   388	# refs and without grafts, so environment/replace/graft attacks cannot rewrite
   389	# the bytes this gate reads.
   390	GIT_ENV_OVERRIDES = {
   391	    "GIT_NO_REPLACE_OBJECTS": "1",
   392	    "GIT_GRAFT_FILE": "/dev/null",
   393	    "GIT_CONFIG_NOSYSTEM": "1",
   394	    "GIT_CONFIG_GLOBAL": "/dev/null",
   395	}
```

(`GIT_NO_REPLACE_OBJECTS` and `GIT_GRAFT_FILE`, the first two objects of the sentence, are inside;
the `startswith("GIT_")` filter is not.)

```
$ git -C <lane> show 99c3bc8:tools/evidence-disposition.py | grep -n 'startswith("GIT_")'
407:    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}

$ git -C <lane> show 99c3bc8:tools/evidence-disposition.py | sed -n '406,409p' | nl -ba -v406
   406	def git_environment():
   407	    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
   408	    env.update(GIT_ENV_OVERRIDES)
   409	    return env
```

This is drift, not a pre-existing choice: at the round-52 commit the range the cell used
(`368-390`) still contained both mechanisms, and the C1 fix only shifted its end to the dict:

```
$ for r in a41195d 218bc6b 5b703c6 1077d81 59c3810; do
    echo -n "$r: "; git show $r:tools/evidence-disposition.py |
      grep -n 'GIT_ENV_OVERRIDES = {\|startswith("GIT_")' | head -2 | tr '\n' ' '; echo; done
a41195d: 371:GIT_ENV_OVERRIDES = { 388:    env = {key: ... if not key.startswith("GIT_")}
218bc6b: 371:GIT_ENV_OVERRIDES = { 388:    env = {key: ... if not key.startswith("GIT_")}
5b703c6: 385:GIT_ENV_OVERRIDES = { 402:    env = {key: ... if not key.startswith("GIT_")}
1077d81: 390:GIT_ENV_OVERRIDES = { 407:    env = {key: ... if not key.startswith("GIT_")}
59c3810: 390:GIT_ENV_OVERRIDES = { 407:    env = {key: ... if not key.startswith("GIT_")}
```

At round 52 the anchor `368-390` covered 368..390, which contains line 388 (the scrub). The
round-53 + round-54 insertions pushed the scrub to 402 then 407; the C1 re-pin
(`git diff 59c3810 99c3bc8 -- SKILL.md`: `:368-390` -> `:385-395`) moved the block start but
stopped at the dict, so the sentence now names a range that does not show the behaviour it
asserts. A cold executor following the anchor sees only a comment claiming the scrub; the code
is outside the range. Minimal repair: end the range at 407 (or `385-409`).

## What I checked and found clean

Every other anchor and cell in the section resolves and holds at C1:

| Claim in section | Check | Result |
|---|---|---|
| `corpus/lessons/round-16-verifier-spotcheck.md` §3 and §6; routed R16-OP1, R16-MON1 | `git show 99c3bc8:corpus/lessons/round-16-verifier-spotcheck.md \| grep -n '^#'` -> `## 3. Per-axis verdicts`, `## 6. Routed defects`; §6 items 1 and 6 are R16-OP1 / R16-MON1 | resolves |
| S062 (`git rev-parse --show-toplevel`) | `corpus/SOURCES.md:70-72` rows S061-S063; S062 states `--show-toplevel` reports the discovered top-level | matches |
| S063 (git repository discovery and `GIT_*` environment) | S063 row: "discovery walks parent directories and environment variables override it ... an inherited GIT_DIR redirects every `git -C`" | matches |
| S061 (jj leaves Git `HEAD` detached at `@-`) | S061 row: "jj leaves Git detached at the working-copy commit's parent" | matches |
| `.ufo/evidence/round-18/dispositions-before.json`, `dispositions.json`, `tools/registry.json`, `.ufo/evidence/round-13/pin-manifest.json` | `git cat-file -e 99c3bc8:<path>` for each | all present |
| `tools/evidence-disposition.py:479-544` | line 479 `def resolve_historical_anchor(lane):` ... line 544 `return "HEAD", commit` — covers bound `refs/heads/<lane.branch>` (481-509), attached branch tip (486-493), jj-without-binding exit 2 (511-515) and the detached-`HEAD`-contained-by-a-ref path (517-544) | exact |
| selftest `v2-registry-clone-detached-anchor` `:2910-2915` expects exit 0 | lines 2910-2915 are exactly that `historical_case(...)` block; its expected exit argument is `0` (line 2912) | exact |
| fixture docstring `:2275` "anchors at HEAD" | line 2275: `"""A detached harness clone anchors at HEAD, not its later remote tip."""` | exact |
| `historical_input_unneeded` / `historical_input_forbidden` / `historical_input_uncommitted` | `grep -n` -> line 625 (`historical_input_unneeded`), docstring 35 + raise sites, 632/640 (`historical_input_uncommitted`) | tokens exist |
| selftests `v2-historical-replace-ref`, `v2-gitdir-env` expect exit 0 | lines 2928-2942 and 2943-2955; expected exit `0` in both | matches |
| "Every lane tool scrubs `GIT_*` before git (round 18 adds `bash-witness-study.py`; historical `.ufo/evidence/round-16/measure.py` still does not)" | `bash-witness-study.py:355` filters `GIT_*`; `mutate-and-run.sh:270-284` unsets every `GIT_*` name found by `env \| sed -n 's/^\(GIT_[A-Za-z0-9_]*\)=.*/\1/p'`; `.ufo/evidence/round-16/measure.py` has no `startswith("GIT_")` filter (only sets `GIT_CONFIG_NOSYSTEM`, author/committer identity) | holds |
| "`registry-check.py` reports `differs`, exit 1" | `registry-check.py:48,52,917` | holds |
| "A row leaves `active` only as `superseded` with `superseded_by`, and still runs" | `registry-check.py:30` "every active row and every superseded row RUNS"; 289 requires `superseded_by`; 297 requires an active target | holds |
| Runner regression leg: SETUP `repo_identity_mismatch`, exit 2 | `mutate-and-run.sh:1263` prints `SETUP (repo_identity_mismatch: ...)`; selftest asserts it at 1945-1946 | holds |
| Step 1 → exit 1, `producer_before` unresolved, `"expectation": "producer_before"` | ran in a `git clone --shared` at C1: `EXIT=1`; the only failing row is `check/name = producer_before`, `outcome: fail`, `mismatches: ["expected_contains_missing"]`; `findings[0] = {"detail": "producer_before: stdout lacks 'summary preserves top-level exposed declaration kind'", "expectation": "producer_before", "id": "expected_contains_missing"}` | exact |
| Step 1 "(round 18; round 17's two now exit 2)" | `.ufo/evidence/round-17/dispositions-before.json` -> `EXIT=2` `expected_input_digest_mismatch`; `.ufo/evidence/round-17/dispositions.json` -> `EXIT=2` same | holds |
| Step 2 → 0 `clean`, `"effective": 11`, `"superseded": 1`; one `HISTORICAL ... rev=... sha256=...` line per waived instrument | ran: `EXIT=0`, `{'effective': 11, 'expected_checks': 12, 'failed': 0, 'findings': 0, 'passed': 11, 'superseded': 1}`; text mode `EVIDENCE_DISPOSITION: clean exit=0 expected=12 effective=11 superseded=1 passed=11 failed=0 findings=0` + 3 `HISTORICAL` lines | exact |
| Step 2's `HISTORICAL <path> rev=<rev> sha256=<sha>` shape | text mode printed `HISTORICAL tools/bash-witness-study.py rev=4acc607d... sha256=49e9e5e2...` (x3) | exact |
| Step 3 ends with `REGISTRY_CHECK: held=N/M superseded=K`; "siblings symlinked beside it"; `--registry` accepts a current registry file | `registry-check.py:50` documents the line, 920-921 emit `held=` + `superseded=` unconditionally, 787-796 build the sibling symlinks, CLI takes `--registry PATH` | holds (code-read only; the full replay is the L1's gate, not a reader's) |
| Step 4 `pin-disposition.py` head rows carry `branch` and `head_differs_from_branch` | `pin-disposition.py:403,426,408,445` | holds |
| Round-14 cross-reference ("restores the round-14 capability's live verdict") | `SKILL.md:1612` (round-14 recipe step 3): "Live-tree form: the round-17 re-pin section (round-18 manifests since then)" | coherent |

Quality pass (QUALITY 104): no run-together token, no missing space, no duplicated parenthetical,
no `C**` placeholder, no self-contradiction between rows 2 and 4 of the recipe (row 2's raw-`HEAD`
case is scoped to an unbound non-jj clone; step 4's "never at `HEAD`" is the reader rule for a
bound lane or a sibling — the two do not overlap).

## Artifacts opened

- `SKILL.md` at `99c3bc88d704566197783f66b211ee0a830e0330` — lines 1840-1870 (the section), plus 1589-1615 (round-14 cross-reference) and the headings index.
- `.ufo/waves/round-54/reader-section.py` (read, to confirm `start`/`end`/sha semantics).
- `.ufo/evidence/round-18/measure.py` docstring (the sectionize rule).
- `tools/evidence-disposition.py` at C1 (whole file read for the anchors: 385-395, 406-409, 479-544, 2275, 2910-2915, 2928-2955, 625, 632, 640).
- `tools/evidence-disposition.py` at `a41195d` / `218bc6b` / `5b703c6` / `1077d81` / `59c3810` (line-position trace only).
- `tools/registry-check.py` at C1 (lines 25-50, 61-73, 277-297, 660-661, 781-796, 891-921, 1299-1352).
- `tools/mutate-and-run.sh` at C1 (lines 270-284, 1263, 1930-1961).
- `tools/pin-disposition.py` at C1 (lines 398-445, 541-546).
- `tools/bash-witness-study.py` at C1 (line 355).
- `.ufo/evidence/round-16/measure.py` at C1 (GIT_* lines).
- `corpus/SOURCES.md` rows S061-S063.
- `corpus/lessons/round-16-verifier-spotcheck.md` §3 and §6.
- `.ufo/evidence/round-18/dispositions.json`, `.ufo/evidence/round-18/dispositions-before.json`, `.ufo/evidence/round-17/dispositions.json`, `.ufo/evidence/round-17/dispositions-before.json`, `.ufo/evidence/round-13/pin-manifest.json`, `tools/registry.json` (presence at C1, and the two round-18 manifests executed).
- `git diff 59c3810 99c3bc8 -- SKILL.md` (the C1 fix pass, my section's hunks).

## Commands run (all read-only against the lane; writes only in scratch and w2)

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read19 python3 .ufo/waves/round-54/reader-section.py <lane> 99c3bc8 "<heading>"
git -C <lane> show 99c3bc8:SKILL.md > $S/SKILL.md ; sed -n '1840,1870p'
git -C <lane> cat-file -e 99c3bc8:<each cited path>
git -C <lane> show 99c3bc8:tools/evidence-disposition.py > $S/ed.py
sed -n '385,395p' / '406,409p' / '474,548p' / '2265,2285p' / '2900,2955p' $S/ed.py
grep -n 'startswith("GIT_")|GIT_ENV_OVERRIDES = {' $S/ed.py $S/ed_c0.py
git -C <lane> show <a41195d|218bc6b|5b703c6|1077d81|59c3810>:tools/evidence-disposition.py | grep -n ...
git -C <lane> show 59c3810:tools/evidence-disposition.py > $S/ed_c0.py
git -C <lane> diff 59c38109bf11 99c3bc8 -- SKILL.md
git -C <lane> grep -n '<token>' 99c3bc8 -- tools/<file>
git clone --shared -q <lane> $S/clone ; git -C $S/clone checkout -q --detach 99c3bc8
git -C $S/clone rev-parse --show-toplevel   # -> $S/clone  (host-guard assertion)
cd $S/clone
TMPDIR=$S python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json     # exit 1
TMPDIR=$S python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json            # exit 0
TMPDIR=$S python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json                    # text mode, 3 HISTORICAL lines
TMPDIR=$S python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions-before.json            # exit 2
TMPDIR=$S python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions.json                   # exit 2
```

No lane production file, counter, contract, freeze, ledger or wave spec was written. No mutating
git command was run against the lane; the clone lives at
`/fast/scratch/hyaku/tameshi-r54/T54W2Read19/clone` and every git call on it names `-C`.

## Verdict

One genuine defect (an under-reaching line anchor on the sentence's own third clause). Everything
else in the section — the seven evidence-condition cells, the token names, the selftest line
citations, and all four recipe steps — resolves and reproduces at C1, including the exact
`effective: 11` / `superseded: 1` counts and the `"expectation": "producer_before"` finding.
