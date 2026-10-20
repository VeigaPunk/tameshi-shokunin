# Review — v2 path of `tools/evidence-disposition.py` (round 17, wave 2)

Scope: `tools/evidence-disposition.py` at `eb7838b16490ca7ba17ea3242ade76a61f744af2`, reviewed against
SKILL.md's round-17 re-pin decision table (SKILL.md:1823-1831 at that rev) and the round-17 gate registry row
(SKILL.md:1850). Second half: v1 path unchanged against `98bea7da5801f4bc58e4187690ee1687c8a5061f`.

Reviewed tool sha256 (at both the checked-out clone and `git show eb7838b:tools/evidence-disposition.py`):
`f8f05c7aa601cf0b6f0907cc1ead2fc01acaad6a3c19e81888c084a969583e27`.
v1 rev sha256 (`git show 98bea7d:tools/evidence-disposition.py`):
`1609a9df970dcde345b4eceadd35d34d016ba0e3f5c3c02415b51592d42d2d95`.

All executions ran in a fleet-mirror clone at `/tmp/tameshi-r17w2-ReviewDispositionV2Code-l08229/fleet/tameshi-shokunin`
(siblings symlinked beside it), detached at `eb7838b`. The lane root was never a tool target; the clone's
`git status --porcelain` was empty after every run. No tool install/upgrade was needed or performed.

## Decision table, row by row (SKILL.md:1825-1831)

| Table row | Stated id / exit | Observed | Evidence |
|---|---|---|---|
| 1 — instrument moved by a committed change; append v2 manifest with `historical_inputs` | waiver of unchanged file: 2 `historical_input_unneeded`; evidence path: 2 `historical_input_forbidden` | reachable, both ids | real manifest tamper tests below; selftest `v2-historical-unneeded`, `v2-historical-forbidden` |
| 2 — waived path's live bytes differ from `HEAD:<path>` | 2 `historical_input_uncommitted` | reachable | worktree edit, live symlink, uncommitted deletion all exit 2 with that id |
| 3 — rev is a tree id, dangling, not an ancestor, shallow, or reached through replace refs, grafts or inherited `GIT_DIR` | 2 (`historical_input_unavailable`) | reachable for every enumerated condition | probes below; tree/dangling/shallow also in selftest |
| 6 — tool or fixture runs git under exported `GIT_DIR`/`GIT_WORK_TREE` | every lane tool scrubs `GIT_*` | holds | all production git calls funnel through `git_call`; `--selftest` and the recipe stay exit 0 with a foreign `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` exported and leave that repo untouched |
| 4, 5, 7 | `registry-check.py` / `mutate-and-run.sh` outcomes | not produced by this file | row 4 is process guidance enabled by the v2 re-pin; row 5 is `registry-check.py`; row 7's decision names the *runner* regression leg. This file's analogous identity guard exits 2 with `historical_input_unavailable` (arm of row 3), not `repo_identity_mismatch` |

### Commands, exits, key output lines

1. `python3 tools/evidence-disposition.py --selftest` → **exit 0**; `SELFTEST: PASS (56/56)`, of which 21 are
   `v2-`prefixed (20 matrix cases plus `v2-identity-guard`). Includes `v2-historical-unneeded`, `-uncommitted`,
   `-tree-id`, `-dangling`, `-replace-ref`, `-shallow-repo`, `-gitdir-env`, `-blob-bytes-crlf`,
   `-committed-deletion`, `v2-live-mismatch-nonhistorical-tool`/`-fixture`,
   `v2-supersedes-missing`/`-unpinned`/`-rows-mismatch`.
2. `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions-before.json --json`
   → **exit 1**; `"status": "failed"`, `findings = [{"id":"expected_contains_missing",
   "expectation":"producer_before", ...}]`. Matches recipe step 1.
3. Same with `.ufo/evidence/round-17/dispositions.json --json` → **exit 0**;
   `"status":"clean"`, `effective 11`, `superseded 1`, `expected_checks 12`, `findings 0`;
   `expected_inputs_historical` = `{tools/mutate-and-run.sh: 4acc607d…, tools/pin-disposition.py: 4acc607d…}`.
   Matches recipe step 2.
4. Same in text mode → **exit 0**; `EVIDENCE_DISPOSITION: clean exit=0 expected=12 effective=11 superseded=1 …`,
   then exactly one `HISTORICAL <path> rev=4acc607d… sha256=75ed934d…` and `… sha256=29725397…` line per waiver.
5. Independent git checks of the real waivers: `git merge-base --is-ancestor 4acc607d… HEAD` → **0**;
   `git show 4acc607d…:tools/mutate-and-run.sh` sha256 `75ed934d…` = round-13 `expected.json` pin;
   live and `HEAD:` bytes both `fb6d86d5…` (≠ pin); same shape for `tools/pin-disposition.py`
   (`29725397…` = pin, live/HEAD `331529ea…`). So G1/G2/G5 are exercised on the real artifact, not only fixtures.
6. Old tool (98bea7d bytes) on `.ufo/evidence/round-17/dispositions.json` → **exit 2**
   `schema_mismatch: dispositions schema must be 'evidence-dispositions-v1'` — the capability genuinely differs
   at the older rev, as C2 states.
7. `python3 tools/evidence-disposition.py` (no argv) and `--selftest --json` → **64 / 64**, matching the
   registry row's usage exit.

### Real-manifest tamper probes (each run against the clone, `--json`)

| Mutation of `.ufo/evidence/round-17/dispositions.json` | exit | id | detail |
|---|---|---|---|
| add waiver for the **unchanged** `tools/witness-metadata.py` | 2 | `historical_input_unneeded` | `live bytes still equal the expected pin; the waiver is unnecessary` |
| add waiver for evidence path `.ufo/evidence/round-13/producer-before.py` | 2 | `historical_input_forbidden` | `historical inputs must be tools/* paths` |
| set `tools/mutate-and-run.sh` rev to `1…1` (unresolvable) | 2 | `historical_input_unavailable` | `rev '111…' does not resolve to that commit` |
| set rev to `HEAD` (`eb7838b`) | 2 | `expected_input_digest_mismatch` | `observed fb6d86d5… expects 75ed934d…` (HEAD cannot launder a moved pin) |

### Adversarial probes (fixture lanes built with the tool's own fixture helpers)

| Scenario | exit | id / key observation |
|---|---|---|
| control: pinned bytes at ancestor, committed move at HEAD | 0 | clean |
| worktree edit of waived path | 2 | `historical_input_uncommitted` |
| live path is a symlink (HEAD has an entry) | 2 | `historical_input_uncommitted` |
| uncommitted deletion (HEAD has an entry) | 2 | `historical_input_uncommitted` |
| tree id as rev | 2 | `historical_input_unavailable` |
| orphan/non-ancestor commit as rev | 2 | `historical_input_unavailable` |
| shallow clone | 2 | `historical_input_unavailable` |
| rev exists **only** through `refs/replace/<oid>` | 2 | `historical_input_unavailable`; same rev under replace refs resolves (`git rev-parse` exit 0), with `GIT_NO_REPLACE_OBJECTS=1` exit 128 |
| graft makes a non-ancestor rev an ancestor | 2 | `historical_input_unavailable`; `merge-base --is-ancestor` exit 0 with the graft, exit 1 with `GIT_GRAFT_FILE=/dev/null` |
| inherited `GIT_DIR`/`GIT_WORK_TREE` whose object db holds the declared rev | 2 | `historical_input_unavailable`; the rev resolves (exit 0) under the inherited env |
| foreign repo nested root inside a git super-repo | 2 | `historical_input_unavailable` (`root is not the toplevel of its own work tree`) |
| bare repo as root | 2 | `historical_input_unavailable` |
| committed deletion at HEAD, rev holds pinned bytes | 0 | clean (documented allowance) |
| replace ref rewrites HEAD, declared rev genuinely ancestral | 0 | clean; `merge-base --is-ancestor` is exit 1 with replacement honoured and exit 0 with `GIT_NO_REPLACE_OBJECTS=1` — G4 is load-bearing |
| benign inherited `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` | 0 | clean (scrub is transparent) |
| uppercase rev / missing `reason` / missing `historical_inputs` | 2 | `dispositions_field_invalid` |
| waived path also pinned in `inputs` | 2 | `input_digest_mismatch` (integrity-first wins) |
| `supersedes` names a v2 document | 2 | `supersedes_mismatch` |

### GIT_* attack on the tool and its fixtures

Exported `GIT_DIR=<foreign>/.git`, `GIT_WORK_TREE=<foreign>`, `GIT_INDEX_FILE=<foreign>/.git/index`, then
`--selftest` → **exit 0**, `SELFTEST: PASS (56/56)`; the recipe → **exit 0**, `clean 11 1`. The foreign repo's
`HEAD` and tree ids were unchanged before/after (`d2f02dcf…`, `0c4ef531…`), and it still had exactly one commit.
Production git calls all go through `git_call` (`tools/evidence-disposition.py:386`), whose `git_environment`
(`:380`) drops every `GIT_*` key and sets `GIT_NO_REPLACE_OBJECTS=1`, `GIT_GRAFT_FILE=/dev/null`,
`GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null` (`:364-370`). Fixture helpers use `_selftest_git_env`
(`:1900`) with the same scrub plus commit identities; `grep -n 'subprocess.run'` finds only `git_call`, the two
fixture git helpers (`_git` `:1916`, `_git_raw` `:1930`), the tool-subprocess launcher `run_cli` (`:2102`), and
the usage-error run (`:2756`) — no unscrubbed git call exists.

## v1 path unchanged against 98bea7d

AST diff of every top-level function/constant between the two revs:

- new only: the v2/git/fixture set (`git_call`, `git_environment`, `verify_repo`, `resolve_historical_rev`,
  `tree_entry`, `read_blob`, `live_regular_bytes`, `check_historical_waiver`, `historical_blob`,
  `validate_historical_inputs`, `check_supersedes_lineage`, `_dispositions_v2`, all `_setup_*`, …);
- removed: none;
- changed: `$USAGE`, `$VERSION`, `_build_lane`, `emit_result`, `run_mode`, `selftest`.

`run_mode`'s only v1-visible change is `schema not in SCHEMAS` replacing `schema != SCHEMA` with the same
`schema_mismatch` detail; every other added block is gated on `schema == SCHEMA_V2` (`:1452`, `:1476`, `:1508`,
`:1518`, `:1579`). `emit_result` only appends `payload.get("historical_text", ())` (`:1404`), a no-op when
absent. `validate_inputs`, `validate_rows`, `validate_expected`, `load_receipts`, and `evaluate_dispositions`
are AST-identical.

Empirical confirmation:

- same v1 fixture lane under both tools: both **exit 0**, and the JSON is byte-identical after removing
  `tool` and `tool_sha256` (the version stamp, which necessarily changes);
- v1 schema mismatch in text mode: stdout **byte-identical**, both exit 2,
  `EVIDENCE_DISPOSITION: could_not_evaluate exit=2 id=schema_mismatch detail=dispositions schema must be 'evidence-dispositions-v1'`;
- real v1 `.ufo/evidence/round-14/dispositions.json` under both tools: both **exit 2**,
  `expected_input_digest_mismatch`, identical detail `tools/mutate-and-run.sh: observed fb6d86d5… expects 75ed934d…`.

The only v1-observable deltas are the `tool`/`tool_sha256` payload fields and five appended `--help` lines
documenting v2; no v1 branch, id, message, or ordering changed.

## Findings

No blocking defect. Ordered by severity; all line refs are at `eb7838b`.

**Minor — G2 accepts symlink HEAD entries as "blob"** (`tools/evidence-disposition.py:531`). G2 checks
`head[1] != "blob"` but never `head[0] in TREE_MODES`, and git stores a symlink as type `blob` with mode
`120000`. Repro: commit a symlink at `tools/pinned-tool.py` (`ls-tree HEAD` → `120000 blob …`), replace the live
path with a regular file whose bytes equal the link target text (`../fixtures/input.txt`), declare the pre-symlink
ancestor rev: **exit 0 clean**. Arbitrary tampered bytes are still caught (the content comparison fires); what
slips through is a mode-only symlink→regular transition when the text coincides. The docstring's G2 wording says
"a symlink … is tampering" (`:44-46`), which is stricter than the code. Non-blocking (contrived precondition).

**Minor — diagnostics: G1 shadows G2 when a committed move is locally reverted.** With a committed move at HEAD
and the worktree reverted to the pinned bytes, `check_historical_waiver` raises `historical_input_unneeded`
(`:512-517`) because live == pin, although the row-2 condition (live ≠ `HEAD:<path>`) is also true and the real
condition is an uncommitted edit. Both are exit 2; only the id/detail misdirects. Same class: an EACCES on the
waived live file is swallowed by `live_regular_bytes` (`:491-507`) and reported as `historical_input_uncommitted`
with detail "live path is absent or not a regular file" rather than an unreadable-file error.

**Minor — doc drift on the read primitive.** The docstring says bytes are read with
`git -C <root> cat-file blob --end-of-options <rev>:<path>` (`:27`), but the implementation uses
`ls-tree -z --full-tree <rev> -- <path>` (`:463`) then `cat-file blob <object_id>` (`:485`); `--end-of-options`
is applied to `rev-parse`/`merge-base`/`ls-tree`, never to `cat-file`. The code is stricter than the doc (mode
whitelist at `:552`), but a reader auditing provenance looks for a command the tool never runs.

**Minor — decision-table row 1 is not a sufficient construction recipe.** SKILL.md:1825 says "Append a v2
manifest whose `historical_inputs` reads that path's pinned bytes from a 40-hex ancestor commit", but a v2
manifest must also carry `supersedes` as a string (`:1453-1459`) that is itself pinned (`:1476-1481`) and a
non-empty per-entry `reason` (`:610-615`); neither is named in the table. Selftest `v2-supersedes-missing` and my
missing-`historical_inputs`/uppercase-rev probes both exit 2 `dispositions_field_invalid` before any row-1 id is
reachable. The schema is documented in the tool's own docstring/`--help`, not in the table; gap-minor.

**Minor — wording risk on row 3's "reached through replace refs".** The table groups replace refs with the
exit-2 provenance failures, while the selftest `v2-historical-replace-ref` (`:2565`) deliberately expects
**exit 0**: a replace ref rewrites `HEAD`, the declared rev is genuinely ancestral, and G4 ignores the
replacement. The guarantee holds (rev-dependent probes exit 2 `historical_input_unavailable`), but a reader can
read the row as "any replace ref ⇒ exit 2" and then mis-grade the selftest.

**Note — "evidence paths can never be waived" is a literal `tools/` prefix check** (`:595-600`), so it is exactly
as strong as that namespace convention; a data artifact stored under `tools/` would be waivable, and a lane
instrument stored elsewhere could not be. Matches the docstring's operational definition; flagged so the
assertion is not read as identity-based.

**Adjacent (registry seat's scope).** `tools/registry.json` row `evidence-disposition-round17` cites
`"source": "SKILL.md@98bea7d:1681"`; at `98bea7d`, line 1681 is the round-14 disposition row, and the v2 recipe
first appears at `eb7838b:1835-1838` / `1850`. The row data itself (`argv`, `expect`, `tags`) matches the page.
Not scored here; `registry-check` behavior is the other reviewer's lane.

## Residual risk

- G2 pins `HEAD`, not `refs/heads/<branch>`; under jj colocation (S061) a move committed in `@` while `HEAD` is
  `@-` will be reported `historical_input_uncommitted`. The landing satisfies the guard because the waived tools
  moved in commits ancestral to `HEAD`, but the rule is branch-tip-blind by construction.
- The identity guard rejects linked worktrees/submodules (`--absolute-git-dir` must be `<root>/.git`,
  `:409-432`); intentional, but it means the tool cannot grade evidence from a worktree checkout.
- `merge-base --is-ancestor --end-of-options` requires a git new enough to accept the option; verified on git
  2.56.0 only.

## Verification gaps

- `tools/registry-check.py`, `tools/mutate-and-run.sh`, `tools/pin-disposition.py` and the C1 `measure.py`
  assertions were not executed here (other seats); rows 4, 5 and 7 were assessed only as "not claimed by this
  file".
- No concurrency/TOCTOU stress between `live_regular_bytes` and the `HEAD` blob read (single-threaded review);
  `read_regular`'s lstat/fstat identity check (`:310-344`) covers substitution during the read itself.
- The symlink-mode gap was reproduced once; I did not fuzz other mode combinations (e.g. submodule gitlinks at
  `HEAD`, which are type `commit` and therefore rejected).

**Verdict: holds** — every decision-table row reachable from this file yields the stated id and exit (rows 1, 2,
3, 6 verified live on the real round-17 manifest, the selftest's 56/56, and constructed provenance attacks),
and the v1 path is semantically unchanged against `98bea7d` (identical results minus the version stamp); the
findings are diagnostic/doc hardening, not soundness holes.
