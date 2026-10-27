# T51W2Read17 — cold-read re-key reader, `## Live-tree re-pin and entry-command monitor — round 17`

Seat T51W2Read17, round 51 wave 2 (falsify). Candidate (CAND) `6d8c11e378aa90b12650808e1b79270742935f15`,
base `9962033fd7a75aa2f2847e979dd687a5d28505a1`. Read-only on the lane/fleet/sibling repos; every command ran
in scratch under `/fast/scratch/hyaku/tameshi-r51/T51W2Read17/` (deleted before yield). No tools installed.
Contract (incl. both amendments), the C1/C2/C3 counter docstrings and `.ufo/evidence/round-51/integrate/l1-notes.md`
read before the item; the consuming instrument is `.ufo/evidence/round-51/coldread/refresh.py` (round-49 method).

## 1. The section at CAND

Heading re-resolved at CAND (not taken from the fixture list or the old READERS_JSON): `## Live-tree re-pin and
entry-command monitor — round 17` starts at **SKILL.md:1814**; the next heading is `### Round-17 gate/probe
registry — re-pin and monitor` at **SKILL.md:1846**; the section is **SKILL.md:1814-1845**, 32 lines, sha256 over
that span `07a598f065c8d3dd5719068e8852069be85129795188069fe2d46e0670844e26` — **byte-identical to base**
(diff of the extracted span at base (also :1814) vs CAND: empty). The SKILL.md diff base→CAND is a single hunk
`@@ -2134,3 +2134,38 @@` appending the `#### Gate/probe registry — round 51` table at :2138 (l1-notes N2's
placement, below this section), so nothing here moved. Verbatim:

```
## Live-tree re-pin and entry-command monitor — round 17

Sources: `corpus/lessons/round-16-verifier-spotcheck.md` §3 and §6 (routed
R16-OP1, R16-MON1); S062 (`git rev-parse --show-toplevel`), S063 (git
repository discovery and `GIT_*` environment), S061 (jj leaves Git `HEAD`
detached at `@-`). This section restores the round-14 capability's live
verdict and adds the monitor that would have caught its loss. It claims no
new mutation case and no promotion credit.

| Evidence condition | Decision | Error pattern / limit |
|---|---|---|
| A lane instrument pinned by historical `expected.json` moved by a committed change | Append a v2 manifest whose `historical_inputs` reads that path's pinned bytes from a 40-hex ancestor commit | Waive only paths that moved: a waiver of an unchanged file exits 2 `historical_input_unneeded`; evidence paths can never be waived (`historical_input_forbidden`) |
| A waived path's live bytes differ from `<anchor>:<path>` (round 18: the branch tip `refs/heads/<lane.branch>`, not `HEAD`) | Could not evaluate, exit 2 `historical_input_uncommitted` | A worktree edit is tampering, not a by-design move |
| The waiver rev is a tree id, dangling, not an ancestor, or shallow | Could not evaluate, exit 2 | The pinned sha256 still guards content; these guard provenance. Replace refs, grafts and an inherited `GIT_DIR` are neutralized, not refused: the tool sets `GIT_NO_REPLACE_OBJECTS=1`, `GIT_GRAFT_FILE=/dev/null` and scrubs inherited `GIT_*` (`tools/evidence-disposition.py:368-390`; selftests `v2-historical-replace-ref`, `v2-gitdir-env` expect exit 0; grafts by code reading only). Corrected in round 27, seat Read32 |
| A registered command's outcome changes after an instrument edit | Re-pin or supersede in the same round; sweep every mention | "By design" names the mechanism; it never excuses the outcome |
| A registry row stops holding its admitted outcome | `registry-check.py` reports `differs`, exit 1 | A row leaves `active` only as `superseded` with `superseded_by`, and still runs |
| A tool or fixture runs git while the caller exported `GIT_DIR`/`GIT_WORK_TREE` | Every lane tool scrubs `GIT_*` before git (round 18 adds `bash-witness-study.py`; historical `.ufo/evidence/round-16/measure.py` still does not — run it only through `registry-check`, which scrubs) | Unscrubbed fixture commits moved this lane's HEAD and index in round 17 |
| A repo path has no `.git` of its own inside a git super-repo | Runner regression leg: SETUP `repo_identity_mismatch`, exit 2 | Without the guard git silently answers from the parent repo's objects |

Recipe, from this lane root (round-13/14 evidence bytes stay immutable):

1. `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json` (round 18; round 17's two now exit 2)
   → 1 `failed`, the `producer_before` expectation unresolved (`"expectation": "producer_before"`).
2. The same command with `.ufo/evidence/round-18/dispositions.json` → 0 `clean`,
   `"effective": 11`, `"superseded": 1`; text mode prints one `HISTORICAL <path> rev=<rev> sha256=<sha>` line per waived instrument.
3. `python3 tools/registry-check.py --rev <40-hex lane commit>` replays every row of
   `tools/registry.json` in a scratch clone (siblings symlinked beside it) and ends with
   `REGISTRY_CHECK: held=N/M superseded=K`. Grade an older rev with `--registry <current registry file>`.
   Run it with `--rev`, never on the live tree: some rows write receipts into their root.
4. Read a sibling's or this lane's committed bytes at the branch tip `refs/heads/<branch>`
   (`tools/pin-disposition.py` head rows carry `branch` and `head_differs_from_branch`), never at `HEAD`.
```

Why it is a re-key target — measured at CAND, not copied from the fixture list: the round-21 monitor at CAND
(`--repo <clone> --rev CAND`) scores 6, 44/64; this section is uncredited with the aggregated reason

```
input-drift:corpus/QUALITY.md;input-drift:corpus/README.md;input-drift:corpus/SOURCES.md;input-drift:tools/mte-interop.py;input-drift:tools/mutate-and-run.sh;input-drift:corpus/QUALITY.md;input-drift:corpus/README.md;input-drift:corpus/SOURCES.md;input-drift:tools/mutate-and-run.sh;input-drift:corpus/SOURCES.md;input-drift:tools/mutate-and-run.sh;input-drift:tools/mutate-and-run.sh
```

— five distinct drifted paths: the three growing record files (QUALITY.md, README.md, SOURCES.md), the C2 runner
edit (tenth leg + r51 TMPDIR honouring), and — **not visible in the w1 fixture list** — `tools/mte-interop.py`,
one of the four panel-tool updates. The heading has 18 ledger entries; 12 pin `tools/mutate-and-run.sh`
(CR55, CR46, Read32, ReRead01, Read11B, Read09A, ColdA08, ColdB08, ColdA02, ColdB02, …), entry 343 (ReRead01,
read_rev `b1cc95e1`) pins `tools/mte-interop.py`, and the last re-anchor entries (read_rev `329b6ddb`) pin the
round-18 dispositions, nine `.ufo/evidence/round-18/final/*.stdout` receipts and the four tools
(evidence-disposition.py, pin-disposition.py, registry-check.py, registry.json) — none of which changed
base→CAND.

Pointer-extraction cross-check (round-49 `extract()` on the section text — the extractor refresh.py reuses):
**15 pointers** — 1 line-range (`tools/evidence-disposition.py:368-390`), 11 path tokens, 3 S-ids
(S062, S063, S061). Eight path tokens resolve to lane files at CAND; three resolve to nothing
(`expected.json` :1825 generic; bare `registry-check.py` :1829 and bare `bash-witness-study.py` :1830 — both
files exist at `tools/`, the bare prose names just do not resolve); the S-ids resolve to
`corpus/SOURCES.md:70-72`. No internal pointer (the section carries file pointers, so refresh's one-hop
internal follow does not apply).

## 2. Pointers verified against candidate bytes

Method: `git clone --shared` of the lane detached at CAND (`$S/lane`, later moved to
`$S/fleet/tameshi-shokunin` with `*-shokunin` sibling symlinks beside it; `git rev-parse --show-toplevel`
asserted), `TMPDIR=$S/tmp` on every invocation; repo reads via `git show CAND:<path>`; the section's own recipe
executed as written.

### P0 `tools/evidence-disposition.py:368-390` (SKILL.md:1827) — **holds**

- The range at CAND is exactly the claimed content: G4 comment :368-370; `GIT_ENV_OVERRIDES` :371-376
  (`GIT_NO_REPLACE_OBJECTS: "1"`, `GIT_GRAFT_FILE: "/dev/null"`, `GIT_CONFIG_NOSYSTEM: "1"`,
  `GIT_CONFIG_GLOBAL: "/dev/null"`); `git_environment()` :387-390 drops every inherited `GIT_*` then applies
  the overrides.
- Both named selftest cases exist and expect exit 0: `v2-historical-replace-ref` :2910-2923,
  `v2-gitdir-env` :2925-2938; `--selftest` at CAND bytes exits 0 (cases PASS). Grafts indeed have no selftest
  case — "grafts by code reading only" is accurate.
- Provenance verified: `.ufo/waves/round-27/w1/Read32.md` exists at CAND and is the correction this line
  records (its "smallest safe correction" matches the current text).
- Strongest falsifier: the range not containing the overrides/scrub, or either selftest case absent or
  failing — checked all three; holds.

### P1 `corpus/lessons/round-16-verifier-spotcheck.md` §3 and §6 (SKILL.md:1816) — **holds**

- §3 `## 3. Per-axis verdicts` :123-133 (operability **harmed** :129, basis :134+); §6 `## 6. Routed defects`
  :214-239 routes **R16-OP1** :216-221 ("Restore a clean-capable live-tree verdict for
  `tools/evidence-disposition.py`") and **R16-MON1** :237-239 ("Add the registered entry commands
  (`--root .` forms) so a live-tree verdict change is caught inside the round").
- Precision note (pre-existing, immaterial): both routed ids live in §6; §3 supplies the harmed-operability
  basis. The source sentence is accurate as written.
- Strongest falsifier: either section missing or the ids not routed where claimed — checked; holds.

### P2 `expected.json` (SKILL.md:1825, generic mention) — **token resolves to no file; sentence holds**

- `resolve()` returns None (no `expected.json` at the lane root or the corpus/knowledge|corpus|corpus/lessons
  prefixes). The concrete referent in context — the manifests' `"expected_file":
  ".ufo/evidence/round-13/expected.json"` — exists at CAND. The instrument records the token unresolved; the
  sentence is about the mechanism, not a file path. No falsifiable file claim.

### P3 `registry-check.py` (bare, SKILL.md:1829) — **holds as prose; bare token unresolved**

- Claim "reports `differs`, exit 1": **observed** in the full replay (P9): `ROW mte-interop-check expect=0
  got=0 differs`, final exit 1.
- Claim "A row leaves `active` only as `superseded` with `superseded_by`, and still runs":
  `tools/registry.json` at CAND has 56 rows, 7 `superseded`, each `superseded_by` naming an existing row
  (loader enforces :277-293); docstring :30-31 "every active row and every superseded row RUNS … counted in
  `superseded=K`" — and the replay ran 49+7=56 rows.
- File exists at `tools/registry-check.py` (unchanged base→CAND); the bare prose name resolves to no lane file.

### P4 `bash-witness-study.py` (bare, SKILL.md:1830) — **holds as prose; bare token unresolved**

- `tools/bash-witness-study.py` exists at CAND (unchanged base→CAND) and scrubs: docstring :66-67 ("every
  child process drops inherited `GIT_*` variables, then sets `GIT_CONFIG_GLOBAL=/dev/null` and
  `GIT_CONFIG_NOSYSTEM=1`"), env build :336-338.

### P5 `.ufo/evidence/round-16/measure.py` (SKILL.md:1830) — **holds**

- Exists at CAND, unchanged base→CAND. Its only three `GIT_` occurrences (:413-415) SET
  `GIT_CONFIG_NOSYSTEM` and author/committer env for a fixture commit — no scrub of inherited `GIT_*`, so
  "still does not [scrub]" is true.
- "run it only through `registry-check`, which scrubs": registry-check scrubs every row's environment
  (:150-163).

### P6 Recipe step 1 (SKILL.md:1835-1836) — **holds, executed at CAND bytes**

- `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json
  --json` → **exit 1**, `"status": "failed"`, exactly **1** failed row, finding `"expectation":
  "producer_before"` (id `expected_contains_missing`, detail "producer_before: stdout lacks 'summary preserves
  top-level exposed declaration kind'").
- Parenthetical "(round 18; round 17's two now exit 2)": verified — the same command with
  `.ufo/evidence/round-17/dispositions.json` → **exit 2**, and with
  `.ufo/evidence/round-17/dispositions-before.json` → **exit 2**.

### P7/P8 Recipe step 2 (SKILL.md:1837-1838) — **holds, executed at CAND bytes**

- With `.ufo/evidence/round-18/dispositions.json` → **exit 0**, `"status": "clean"`, `"effective": 11`,
  `"superseded": 1` (12 rows, 1 superseded by the round-14 producer_before policy).
- Text mode prints exactly **3** `HISTORICAL <path> rev=<rev> sha256=<sha>` lines, one per waived instrument —
  `tools/bash-witness-study.py`, `tools/mutate-and-run.sh`, `tools/pin-disposition.py`, all at rev
  `4acc607dfd79f19d508bd50cdd06b77269fccd1d` (40-hex ancestor, as :1825 requires), shas matching the manifest's
  own reason strings (49e9e5e2…, 75ed934d…, 29725397…).

### P9 `tools/registry-check.py` step 3 (SKILL.md:1839-1842) — **holds, executed end-to-end at CAND for the first time**

- Full replay from the lane root: `python3 -B tools/registry-check.py --rev 6d8c11e…` (TMPDIR in scratch),
  **613 s** wall. It replayed **all 56 rows** (49 active + 7 superseded — "every row … and still runs") and
  ended with exactly the claimed shape: `REGISTRY_CHECK: held=48/49 superseded=7`, exit **1** on one differs
  row (§3). Read32 could only run one row inside the six-minute cap; this closes that gap at CAND bytes.
- "in a scratch clone (siblings symlinked beside it)": the `mutate-and-run-regression` row **held** inside the
  replay — that row SETUP-fails without sibling owner repos (Read16's bare-clone control observed exactly
  that), so the sibling symlinking is empirically confirmed, not just docstring.
- "Grade an older rev with `--registry <current registry file>`": usage :12-13, :66-68 (docstring-verified,
  not executed).
- "Run it with `--rev`, never on the live tree: some rows write receipts into their root": docstring :31
  (cwd = the clone root under --rev); after the replay the live lane shows **zero tracked modifications**
  (status porcelain clean apart from the wave dirs' untracked reports).

### P10 `tools/registry.json` (SKILL.md:1840) — **holds**

- Exists at CAND, unchanged base→CAND; 56 rows parse; statuses active|superseded; the 7 superseded rows:
  evidence-disposition-round17→evidence-disposition-round18, evidence-disposition-round17-before→
  evidence-disposition-round18-before, evidence-disposition-round14-superseded→evidence-disposition-round18,
  trace-inputs-round17-selftest→trace-inputs-selftest, command-binding-selftest→command-binding-selftest-r24,
  command-binding-frozen-clean→command-binding-frozen-clean-pinned,
  command-binding-source-read-red→command-binding-source-read-red-pinned.

### P11 `tools/pin-disposition.py` step 4 (SKILL.md:1843-1844) — **holds, executed**

- `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root
  /home/vgpnk/Projects/shokunin` → **exit 0**, `"unavailable": 0`; head rows carry `"branch": "master"` and
  `"head_differs_from_branch": false` — the two fields the section names, observed in output. detect_branch
  mirrors `scripts/hyaku/jj-lane.sh` (:324-331); the anchor is the branch tip per S061.

### P12-P14 S062 / S063 / S061 (SKILL.md:1817-1818) — **hold**

- `corpus/SOURCES.md` at CAND: **S062 at :71** (git-rev-parse(1) --show-toplevel; "comparing its realpath with
  the caller's repo path tests repository identity"), **S063 at :72** (git(1) repository discovery; "an
  inherited GIT_DIR redirects every `git -C`"), **S061 at :70** (jj colocated workspaces; "jj leaves Git
  detached at the working-copy commit's parent, so `git rev-parse HEAD` is not the bookmark tip; read the
  branch ref"). All three `mined`, glosses match; the record span :70-72 matches the w1 fixture list.

### Runner claim without a path token (SKILL.md:1831) — **holds at CAND bytes**

- "Runner regression leg: SETUP `repo_identity_mismatch`, exit 2": tools/mutate-and-run.sh at CAND :1263
  prints `REGRESSION_CASE %s: SETUP (repo_identity_mismatch: …)`; die_setup exits 2 (:253-256); Read16
  observed exit 2 end-to-end in a sibling-less clone. The tenth leg and the r51 TMPDIR change (:149-160,
  three mktemp sites now `"${TMPDIR:-/tmp}/…"`) do not touch this leg, and this section names no leg count,
  case count or temp path.

## 3. Adversarial summary

- **No stale or moved pointer.** All eight resolved files exist at CAND at the cited paths and are
  byte-unchanged base→CAND (the only lane changes are SKILL.md's appended round-51 table at :2138+,
  corpus/README.md, corpus/SOURCES.md, tools/mutate-and-run.sh and the four panel tools — none of the eight).
- **One real, round-51-introduced inconsistency found — caught by this section's own monitor, exactly as the
  section claims.** The four panel-tool updates (amendment 2) changed `tools/mte-interop.py`; its `--check`
  now prints `MTE_INTEROP: PASS legs_conforming=10/10` (observed in a fleet-mirror clone at CAND, exit 0,
  267 s — the runner regression inside it passed over all ten legs), while the registered row
  `mte-interop-check` in `tools/registry.json` (unchanged, and outside the widened no-harm tools-scope) still
  expects `stdout_contains "legs_conforming=9/9"`. The full replay therefore reports
  `ROW mte-interop-check expect=0 got=0 differs` and exits 1: `REGISTRY_CHECK: held=48/49 superseded=7`.
  This instantiates the section's :1828-:1829 decision rows ("A registered command's outcome changes after an
  instrument edit → Re-pin or supersede in the same round; sweep every mention"; "A registry row stops holding
  its admitted outcome → `registry-check.py` reports `differs`, exit 1") — the mechanism claim is confirmed by
  a live instance. **Data for the L1:** within the frozen scope (M:tools/mutate-and-run.sh + the four tools
  only) the registry.json re-pin cannot land this round, so `registry-check --rev CAND` keeps exiting 1 unless
  the L1 widens the scope or accepts the red row. It falsifies no sentence in this section (the section claims
  the monitor catches such a row, which it did).
- **Nothing is made false by the tenth leg, the runner TMPDIR change, or the panel updates** in this section's
  own sentences: it names no leg count, no case count, no temp path; its one runner claim (the repo-identity
  SETUP leg) is verified in the CAND bytes; its mte-interop exposure is via entry 343's pinned input (drift,
  handled by the re-key), not via a false sentence.
- **Pre-existing nuances (disclosed or immaterial):** :1826's "not `HEAD`" is flat — the docstring (:51-53)
  allows a HEAD fallback for an unbound detached non-jj harness when a local/remote-tracking ref contains it
  (Read32 flagged the same); grafts are neutralized by code reading only, which the section itself states; two
  bare prose names (`registry-check.py`, `bash-witness-study.py`) and the generic `expected.json` resolve to no
  lane file (the instrument records them unresolved; the files exist at their real paths).
- **Recipe status at CAND:** steps 1-2 reproduce exactly (first re-execution at CAND bytes; Read32 ran them at
  2227d833); step 3 executed end-to-end for the first time (613 s) and works as described, red on the one stale
  row; step 4 executed and matches.

## 4. Row for `reads.json`

```json
{
  "seat": "T51W2Read17",
  "candidate": "6d8c11e378aa90b12650808e1b79270742935f15",
  "heading": "## Live-tree re-pin and entry-command monitor — round 17",
  "start": 1814,
  "end": 1845,
  "section_sha256": "07a598f065c8d3dd5719068e8852069be85129795188069fe2d46e0670844e26",
  "section_bytes_equal_base": true,
  "pointers": [
    {
      "raw": "tools/evidence-disposition.py:368-390",
      "file": "tools/evidence-disposition.py",
      "ranges": [[368, 390]],
      "skill_line": 1827,
      "verdict": "holds",
      "excerpt": "CAND :368-370 G4 comment 'every git subprocess runs without inherited GIT_* state, without replace refs and without grafts'; :371-376 GIT_ENV_OVERRIDES {GIT_NO_REPLACE_OBJECTS:'1', GIT_GRAFT_FILE:'/dev/null', GIT_CONFIG_NOSYSTEM:'1', GIT_CONFIG_GLOBAL:'/dev/null'}; :387-390 git_environment() drops every inherited GIT_* then applies the overrides",
      "falsifier": "range not containing the overrides/scrub, or selftests v2-historical-replace-ref (:2910, expect 0) / v2-gitdir-env (:2925, expect 0) absent or failing — all checked; --selftest run at CAND bytes exits 0"
    },
    {
      "raw": "corpus/lessons/round-16-verifier-spotcheck.md",
      "file": "corpus/lessons/round-16-verifier-spotcheck.md",
      "ranges": null,
      "skill_line": 1816,
      "verdict": "holds",
      "excerpt": "CAND §3 '## 3. Per-axis verdicts' :123 (operability harmed :129/:134); §6 '## 6. Routed defects' :214 with R16-OP1 :216-221 (restore clean-capable live-tree verdict for tools/evidence-disposition.py) and R16-MON1 :237-239 (add registered entry commands to the operability monitor)",
      "falsifier": "either section absent or the routed ids not where claimed — checked; both ids live in §6, §3 is the harmed-operability basis (precision note, sentence still accurate)"
    },
    {
      "raw": "expected.json",
      "file": null,
      "ranges": null,
      "skill_line": 1825,
      "verdict": "holds",
      "excerpt": "generic mention 'pinned by historical `expected.json`'; resolve() -> None at all four candidate prefixes; the concrete referent (the manifests' expected_file) .ufo/evidence/round-13/expected.json exists at CAND",
      "falsifier": "n/a — mechanism sentence, not a file path; instrument records the token unresolved"
    },
    {
      "raw": "registry-check.py",
      "file": null,
      "ranges": null,
      "skill_line": 1829,
      "verdict": "holds",
      "excerpt": "bare prose name (file is tools/registry-check.py, exists at CAND, unchanged); claim 'reports differs, exit 1' OBSERVED in the full replay (ROW mte-interop-check expect=0 got=0 differs, exit 1); 'a row leaves active only as superseded with superseded_by, and still runs' — registry.json 56 rows / 7 superseded each with superseded_by naming an existing row, loader :277-293, docstring :30-31, replay ran 49+7=56 rows",
      "falsifier": "registry-check failing to report a stale row as differs, or a superseded row without superseded_by / not run — checked by the full replay and the registry parse; holds"
    },
    {
      "raw": "bash-witness-study.py",
      "file": null,
      "ranges": null,
      "skill_line": 1830,
      "verdict": "holds",
      "excerpt": "bare prose name (file is tools/bash-witness-study.py, exists at CAND, unchanged); it scrubs: docstring :66-67 'every child process drops inherited GIT_* variables, then sets GIT_CONFIG_GLOBAL=/dev/null and GIT_CONFIG_NOSYSTEM=1', env build :336-338",
      "falsifier": "the round-18-added tool missing or not scrubbing — checked both; holds"
    },
    {
      "raw": ".ufo/evidence/round-16/measure.py",
      "file": ".ufo/evidence/round-16/measure.py",
      "ranges": null,
      "skill_line": 1830,
      "verdict": "holds",
      "excerpt": "exists at CAND, unchanged base->CAND; only three GIT_ occurrences (:413-415) SET GIT_CONFIG_NOSYSTEM/author env for a fixture commit — no scrub of inherited GIT_*; registry-check scrubs (:150-163)",
      "falsifier": "the historical tool secretly scrubbing GIT_* (would make 'still does not' false) — grep shows no scrub loop; holds"
    },
    {
      "raw": "tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json",
      "file": ".ufo/evidence/round-18/dispositions-before.json",
      "ranges": null,
      "skill_line": 1835,
      "verdict": "holds",
      "excerpt": "executed at CAND bytes: exit 1, '\"status\": \"failed\"', exactly 1 failed row, finding '\"expectation\": \"producer_before\"' (id expected_contains_missing); parenthetical verified: round-17/dispositions.json -> exit 2, round-17/dispositions-before.json -> exit 2",
      "falsifier": "the before-manifest run exiting 0/clean or a different expectation failing — ran it; holds"
    },
    {
      "raw": ".ufo/evidence/round-18/dispositions.json",
      "file": ".ufo/evidence/round-18/dispositions.json",
      "ranges": null,
      "skill_line": 1837,
      "verdict": "holds",
      "excerpt": "executed at CAND bytes: exit 0, '\"status\": \"clean\"', '\"effective\": 11', '\"superseded\": 1' (12 rows, 1 superseded); text mode prints exactly 3 HISTORICAL lines (bash-witness-study.py, mutate-and-run.sh, pin-disposition.py @ rev 4acc607dfd79f19d508bd50cdd06b77269fccd1d, shas 49e9e5e2…/75ed934d…/29725397… matching the manifest reasons)",
      "falsifier": "effective/superseded counts or the HISTORICAL line format differing — ran both modes; holds"
    },
    {
      "raw": "tools/registry-check.py --rev <40-hex lane commit>",
      "file": "tools/registry-check.py",
      "ranges": null,
      "skill_line": 1839,
      "verdict": "holds",
      "excerpt": "full replay from the lane root at CAND: 613 s, all 56 rows replayed (49 active + 7 superseded), ends 'REGISTRY_CHECK: held=48/49 superseded=7', exit 1 on the one differs row; siblings symlinked (mutate-and-run-regression row held — it SETUP-fails without them); --registry/--tag/--json/--selftest in usage :12-13; receipts go to the clone root under --rev (docstring :31); live lane untouched after (0 tracked modifications)",
      "falsifier": "the replay crashing (exit 2), miscounting rows, omitting the REGISTRY_CHECK line, or silently passing a stale row — ran the first-ever end-to-end replay at CAND; shape and differs-detection hold"
    },
    {
      "raw": "tools/registry.json",
      "file": "tools/registry.json",
      "ranges": null,
      "skill_line": 1840,
      "verdict": "holds",
      "excerpt": "exists at CAND, unchanged base->CAND; 56 rows; 7 superseded (evidence-disposition-round17->round18, round17-before->round18-before, round14-superseded->round18, trace-inputs-round17-selftest->trace-inputs-selftest, command-binding-selftest->-r24, command-binding-frozen-clean->-pinned, command-binding-source-read-red->-pinned)",
      "falsifier": "registry invalid or rows missing — parsed and replayed; holds"
    },
    {
      "raw": "tools/pin-disposition.py",
      "file": "tools/pin-disposition.py",
      "ranges": null,
      "skill_line": 1844,
      "verdict": "holds",
      "excerpt": "executed: --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin -> exit 0, '\"unavailable\": 0', head rows carry '\"branch\": \"master\"' and '\"head_differs_from_branch\": false'; detect_branch mirrors scripts/hyaku/jj-lane.sh (:324-331)",
      "falsifier": "head rows lacking the two named fields — ran the probe; holds"
    },
    {
      "raw": "S062",
      "file": "corpus/SOURCES.md",
      "ranges": [[71, 71]],
      "skill_line": 1817,
      "verdict": "holds",
      "excerpt": "SOURCES.md:71 git-rev-parse(1) --show-toplevel: 'comparing its realpath with the caller's repo path tests repository identity instead of assuming it' — matches the gloss",
      "falsifier": "row absent/moved or gloss mismatched — read at CAND; holds"
    },
    {
      "raw": "S063",
      "file": "corpus/SOURCES.md",
      "ranges": [[72, 72]],
      "skill_line": 1817,
      "verdict": "holds",
      "excerpt": "SOURCES.md:72 git(1) GIT_CEILING_DIRECTORIES and repository discovery: 'an inherited GIT_DIR redirects every `git -C`' — matches the gloss",
      "falsifier": "row absent/moved or gloss mismatched — read at CAND; holds"
    },
    {
      "raw": "S061",
      "file": "corpus/SOURCES.md",
      "ranges": [[70, 70]],
      "skill_line": 1818,
      "verdict": "holds",
      "excerpt": "SOURCES.md:70 jj git-compatibility: 'in a colocated workspace jj leaves Git detached at the working-copy commit's parent, so `git rev-parse HEAD` is not the bookmark tip; read the branch ref' — matches 'detached at `@-`'",
      "falsifier": "row absent/moved or gloss mismatched — read at CAND; holds"
    },
    {
      "raw": "Runner regression leg: SETUP `repo_identity_mismatch`, exit 2 (no path token; tools/mutate-and-run.sh)",
      "file": "tools/mutate-and-run.sh",
      "ranges": [[1263, 1263]],
      "skill_line": 1831,
      "verdict": "holds",
      "excerpt": "runner at CAND :1263 prints 'REGRESSION_CASE %s: SETUP (repo_identity_mismatch: %s is not its own repository; toplevel=%s)'; die_setup exit 2 :253-256; Read16 observed exit 2 end-to-end in a sibling-less clone; r51 TMPDIR change (:149-160) and tenth leg do not touch it",
      "falsifier": "the repo-identity leg removed or renamed by the C2 runner edit — grep at CAND bytes; holds"
    }
  ],
  "falsifier_checked": "strongest: the first-ever end-to-end `python3 tools/registry-check.py --rev CAND` replay from the lane root (613 s, TMPDIR in scratch) — step 3's recipe could fail by crashing, miscounting, omitting the terminal line, or silently passing a stale row; observed all 56 rows replayed, the exact terminal line 'REGISTRY_CHECK: held=48/49 superseded=7', and one real round-51-introduced staleness (mte-interop-check expects legs_conforming=9/9, tool now prints 10/10) caught as 'ROW mte-interop-check expect=0 got=0 differs', exit 1 — the section's :1829 mechanism demonstrated live",
  "notes": [
    "section bytes identical base->CAND (SKILL.md diff is one hunk at :2134+ appending the round-51 registry table below it); it is a re-key target via input-drift on five paths: corpus/QUALITY.md, corpus/README.md, corpus/SOURCES.md (record growth), tools/mutate-and-run.sh (C2 tenth leg + TMPDIR), tools/mte-interop.py (panel update; entry 343 ReRead01 pins it) — the last one is not visible in the w1 fixture list",
    "no stale or moved pointer; all eight resolved files byte-unchanged base->CAND",
    "round-51-introduced data for the L1: tools/registry.json row mte-interop-check is stale at CAND (expects legs_conforming=9/9; observed 'MTE_INTEROP: PASS legs_conforming=10/10', exit 0, 267 s in a fleet-mirror clone) and registry.json is outside the widened no-harm tools-scope, so registry-check --rev CAND exits 1 (held=48/49 superseded=7) — the section's own :1828-:1829 decision rows name the required action (re-pin or supersede in the same round; sweep every mention)",
    "pre-existing nuances: :1826 'not HEAD' is flat (docstring :51-53 allows a HEAD fallback for an unbound detached non-jj harness; Read32 flagged it); grafts neutralized by code reading only (stated in the section itself); bare tokens registry-check.py / bash-witness-study.py and generic expected.json resolve to no lane file (files exist at tools/; instrument records them unresolved)",
    "recipe steps 1-2 executed at CAND bytes for the first time (Read32 ran them at 2227d833); step 3 executed end-to-end for the first time (Read32 capped at one row); step 4 executed"
  ]
}
```

## 5. Method, provenance, cleanup

- Reads: candidate SKILL.md via `git show CAND:SKILL.md`; heading re-resolved by grep at CAND (1814) and next
  heading (1846); every cited file read from the CAND clone (`git show` / direct opens in the clone); the
  round-49 extractor (`extract`/`resolve` from `.ufo/evidence/round-49/c1/measure.py`) run on the section text
  for the pointer cross-check (15 pointers, 8 resolved files, 3 unresolved tokens, 3 sids → SOURCES.md:70-72).
- Counter context read before the item: `.ufo/evidence/round-51/contract.json` (incl. both amendments); the
  C1/C2/C3 counter docstrings; `.ufo/evidence/round-51/integrate/l1-notes.md` (N1 surface disclosure, N2 row
  placement — the reason this section did not move); w1-results.json; the re-key instrument report
  `.ufo/waves/round-51/w1/T51ExecRekey.md` §3 (used only as a cross-check, not trusted); sibling reader report
  `T51W2Read16.md` for format and the regression/SETUP controls it observed.
- Heavy executions: evidence-disposition (before/after/round-17×2/text/selftest — all in the CAND clone),
  registry-check full replay (613 s, from the live lane with `--rev`, TMPDIR in scratch; lane untouched:
  0 tracked modifications after), mte-interop `--check` (267 s, fleet-mirror clone, toplevel asserted),
  pin-disposition probe, round-21 monitor at CAND (drop-reason capture).
- All scratch under `/fast/scratch/hyaku/tameshi-r51/T51W2Read17/` (clone, fleet mirror, tmp, outputs),
  **deleted before yield**; no `/tmp` use beyond tools' defaults redirected to scratch; no git/jj mutations
  anywhere but the scratch clone (no fixture commits needed); no tools installed; no writes outside `$S` and
  this report.
