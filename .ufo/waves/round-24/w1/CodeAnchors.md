# CodeAnchors — validation of the four new round-24 registry `source` anchors

Lane: leaf reviewer (no dispatch). Scope: do the cited lines exist at revision
`6a1821a8897eea6e7d9669292160ec9593669409`, and do they support the row each
anchor is attached to?

Reviewed tree: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` at delivered
revision `c8c5b88c8e961a929cdc351b95a7074c76958909` (HEAD).

## Verdict

**PASS on existence, PASS-with-caveats on support.**

All three cited ranges resolve verbatim at the cited revision, and the cited
file is byte-identical at the base revision and at HEAD, so none of the four
anchors is stale or mis-numbered. Three of the four rows are fully supported by
the lines they cite. The fourth (`registry-replay-selftest`, anchor `:74-93`)
is supported for three of the four defect statements inside its range; the
fourth is implemented in code but not exercised by the row's own
`10/10 pass` expectation, and one of the range's lines has a second half that
is not delivered and not disclosed.

No production file was modified; this report is the only write. No registry
battery, gate or selftest was executed in the lane repo (lane bound).

## What was checked

| Check | Method | Result |
|---|---|---|
| Anchor file present at the cited revision | `GIT_OPTIONAL_LOCKS=0 git ls-tree -r 6a1821a… -- .ufo/waves/round-23/` | `.ufo/waves/round-23/fresh-adjudication.json` present |
| Cited file bytes at base rev vs HEAD | `git show 6a1821a…:… \| sha256sum` vs `sha256sum` of worktree file | both `44f9fb583121365732e9723cc44142dba03623b3eeb05a7d3a12b035acc03fee` → anchor is stable, not stale |
| Cited revision resolves | `git cat-file -t 6a1821a…` → `commit`; `git log -1` → `6a1821a round-23: land final measured receipts, seat accounting and verdict` | valid commit, and it is the round-24 contract `base_revision` |
| Line ranges exist and say what is claimed | numbered dump of the base blob | 53–59, 66, 74–93 all present (file is 130 lines) |
| Anchor syntax accepted by the registry checker | `tools/registry-check.py:108` `SOURCE_RE = ^[^@]+@[0-9a-f]{7,40}:[0-9]+(-[0-9]+)?$` | all four match; note the checker **regex-validates only** — nothing in the repo resolves an anchor at its cited revision (see gaps) |

## Anchor-by-anchor

### 1. `command-binding-selftest-r24` — `.ufo/waves/round-23/fresh-adjudication.json@6a1821a…:53-59`

Cited lines (routed defects, `routed_not_executed`):

- **:53** — "A name-insensitive argv mutant (receipt argv in any requirement argv)
  is outside the ten-anchor sweep and would survive all 38 selftest cases
  [seat inference, not executed]. Needs a swapped-name supplemental case plus
  that mutant." (finding label `ArgvExact`)
- **:59** — "An unexecuted negative-exit guard-weakening candidate. Its expected
  survival is a seat inference, not a measured survivor." (finding label
  `MutationDesign`)

Support — **full**, and the arithmetic closes exactly:

- At the base revision the tool loaded one fixture file only
  (`git show 6a1821a…:tools/command-binding.py` → `fixtures = …/round-23/extra-cases.json`,
  19 cases); 17 built-in cases + 19 + 2 = 38, matching the superseded row's
  `38/38` and the "38 selftest cases" wording at :53.
- The delivered tool loads both fixtures
  (`tools/command-binding.py:164-168`: `for fixtures in (evidence / 'round-23/extra-cases.json', evidence / 'round-24/extra-cases.json')`),
  17 + 19 + 6 + 2 = **44**, matching the new row's `COMMAND_BINDING_SELFTEST: 44/44 pass`.
- The six new cases are precisely what :53 and :59 ask for:
  `.ufo/evidence/round-24/extra-cases.json` → `argv-swapped-between-names`
  ("each receipt argv belongs to some requirement, but not to its own name
  (kills a name-insensitive comparison)") = the "swapped-name supplemental case";
  `negative-exit-mismatch` (receipt `-9` vs expected `0`) and
  `negative-exit-declared-match` (declared `-15` that matches stays clean) = the
  negative-exit guard cases.
- The frozen ruler uses the same mutant wording as the cited defect:
  `.ufo/evidence/round-24/measure.py:27-32` K1 mutant
  `if receipt['argv'] not in [row['argv'] for row in requirements.values()]:`
  is literally the "receipt argv in any requirement argv" mutant named at :53;
  K3 `exit-negative-ignored` is the :59 candidate.

### 2. `command-binding-frozen-clean-pinned` and 3. `command-binding-source-read-red-pinned` — `…@6a1821a…:66`

Cited line:

- **:66** — "The `command-binding-frozen-clean` and `source-read-red` registry
  rows do not pin `bundle_sha256` literals, so a regenerated bundle and
  expected pair would still hold." (finding labels `RevisionDeclared F1`,
  `CorpusClaim F3`)

Support — **full, and load-bearing**:

- The cited line names exactly these two rows, and both successors add exactly
  the missing literal to `expect.stdout_contains`
  (`tools/registry.json:971-978` and `:981-988`).
- The pinned literals equal the actual digests of the frozen bundle bytes:
  `sha256sum .ufo/evidence/round-23/replay/bundle.json` =
  `3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9`;
  `sha256sum .ufo/evidence/round-23/source-read-bundle.json` =
  `db620668efe12c00f55518b993c3ffd20dc254f3ace8f06bc82bb661a580d3cf` — identical
  to the two pinned literals and identical to the base-revision blob digests
  (bundles unchanged since `6a1821a`).
- The retained round-23 gate receipts already contain the exact stdout the rows
  now require:
  `.ufo/evidence/round-23/replay-gate-A.json` → `exit 0`, stdout
  `{"bundle_sha256": "3d6c99b7…", "exit": 0, "finding_ids": [], …}`;
  `.ufo/evidence/round-23/source-read-gate-A.json` → `exit 1`, stdout
  `{"bundle_sha256": "db620668…", "exit": 1, "finding_ids": ["ARGV_MISMATCH"], …}`.
  The token spellings (`"finding_ids": []`, `"bundle_sha256": "…"`) match the
  tool's `json.dumps(..., sort_keys=True)` output format
  (`tools/command-binding.py:209-213`).
- The pin is what makes the ruler's K5/K6 predicates real:
  `.ufo/evidence/round-24/measure.py:92-94`
  (`registry_rows_for`) keeps only `status == 'active'` rows, so the two pinned
  successors are the only rows that can detect a self-consistent substituted
  bundle; the three superseded round-23 rows no longer count.

### 4. `registry-replay-selftest` — `…@6a1821a…:74-93`

Cited lines (four separate routed defects inside the range):

- **:74** — "The replay projection drops the runner fields `held`, `cleanup_ok`,
  `external` and `non_hermetic_argv`. The receipt schema cannot carry a
  live-dependency marker." (`Replay31`, `Replay34`, `CwdDeclared 2`)
- **:81** — "`runner_sha256` and `instrument_sha256` hash the live-tree copy of
  `registry-check.py`, not the clone copy that ran." (`RevisionDeclared F3`, `CorpusClaim F2`)
- **:87** — "`replay.py` compares sibling identity by string and does not take
  the realpath of the fleet root." (`CwdDeclared 3`)
- **:93** — "Replay streams are retained without size bounds **or redaction**.
  No secret was observed in the inspected rows." (`RunnerIsolation Medium x2`)

Support — **three of four fully; two caveats**:

- :74 → the successor tool keeps the dropped fields
  (`tools/registry-replay.py:72-113`: `held`, `cleanup_error`, `external`,
  `non_hermetic_argv`, plus `live_dependent` / `revision_pinned` in the report),
  and the selftest cases `not-held`, `held-missing`, `cleanup`, `external`,
  `non-hermetic` cover exactly these five fields (5 of the tool's 10 cases).
- :87 → `plan()` realpath-normalises lane, fleet root and siblings
  (`tools/registry-replay.py:63-67`); selftest case `plan-realpath` exercises a
  symlinked alias path.
- :93 (size-bound half) → `--max-stream-bytes` with `STREAM_LIMIT`
  (`tools/registry-replay.py:96-98`); selftest cases `stream` and
  `stream-at-limit`.
- The ten cases are `clean, not-held, cleanup, held-missing, stream,
  stream-at-limit, external, non-hermetic, invalid` + `plan-realpath`; the tool
  prints `REGISTRY_REPLAY_SELFTEST: %d/%d pass` with `total = len(cases) + 1`
  (`tools/registry-replay.py:243-245`), i.e. `10/10` — matching the row's
  expectation and the ruler's K7–K11 predicates
  (`measure.py:139-202`: RUNNER_NOT_HELD, RUNNER_CLEANUP_FAILED, STREAM_LIMIT,
  live_dependent, realpath `fleet_root`/`repo`/`siblings`).

## Findings

**F1 — Low — the anchor range for `registry-replay-selftest` cites a defect
whose remedy the row's expectation cannot prove.**
Line :81 (runner digest must hash the clone copy that executes) is inside the
cited range `:74-93`. The remedy exists in code
(`tools/registry-replay.py:177` `runner_sha256_clone_copy`, carried into
`observations.json` at `:175-180`), but **no selftest case and no ruler predicate
covers it**. The knowledge entry discloses this honestly —
`corpus/knowledge/replay-projection-hardening.md` row "runner digest from the
live tree" ends with "— (recorded per run, not a ruler predicate)" — so nothing
is overclaimed, but the registry row's anchor implies more coverage than
`10/10 pass` proves.
*Smallest safe correction (no registry change):* add one clause to the
knowledge row's "Hardened rule" cell naming the anchor line, e.g. "clone-copy
digest is recorded per run (adjudication :81) and is not asserted by the
selftest" — the disclosure already exists; it just is not attached to the
anchor that cites it. If instead a case is added, the row's expectation must
change `10/10` → `11/11`.

**F2 — Low — one half of cited line :93 is delivered neither nor disclosed.**
:93 names two properties ("without size bounds **or redaction**"). The tool
bounds stream size but implements no redaction — `grep -rn redact
tools/registry-replay.py corpus/knowledge/replay-projection-hardening.md
SKILL.md .ufo/evidence/round-24/measure.py` returns nothing. The knowledge
table restates the weak link as "unbounded retained streams" only, dropping
the redaction half without saying it was dropped. No predicate depends on it
(K9 is a size bound), so this is a disclosure gap, not a measurement error.
*Smallest safe correction:* one sentence in the knowledge row's "Hardened
rule" cell — "stream size is bounded; redaction is not implemented and remains
open" — and, if the anchor is meant to be read literally, narrow the row's
anchor to `:74`–`:93` minus that half is not expressible in `SOURCE_RE`
(single line or contiguous range), so the disclosure route is the correct one.

**F3 — Low — SKILL.md documents three of the four new registry rows.**
`SKILL.md:2054-2057` (round-24 addition) names
`command-binding-selftest-r24` (44/44), `command-binding-frozen-clean-pinned`
and `command-binding-source-read-red-pinned`, but never names the fourth new
row `registry-replay-selftest` (10/10). The tool itself is documented at
`SKILL.md:2052` including its self-invocation
`python3 tools/registry-replay.py --selftest`, but the registry row and its
`10/10` expectation are absent from the registry listing.
*Smallest safe correction:* extend `SKILL.md:2054-2055` to
"…and `registry-replay-selftest` (10/10)".

**Non-finding (checked, clean):** the superseded round-23 rows do not fail the
battery. `tools/registry-check.py:30-38` and `:877-882` run superseded rows but
exclude them from `held`/`total` and from the exit code, so the now-stale
`38/38` expectation in the superseded `command-binding-selftest` row is
reported (`ROW … superseded expect=… got=…`) but cannot turn the verdict red.
This is the `CodeSupersession` seat's lane; recorded here only because it is
adjacent to anchor :53 (the 38→44 change).

## Residual risk and verification gaps

1. **No machine enforcement of anchors.** `tools/registry-check.py` only
   regex-checks `source` (`SOURCE_RE`, line 108). Nothing resolves the cited
   file at the cited revision, so a wrong revision or a drifted line number
   would pass the registry check silently. My verification is manual and
   revision-exact (`git show 6a1821a…` byte-identical to HEAD), not a
   tooling-enforced invariant.
2. **No execution of the two row expectations.** Lane bounds forbid running
   gates/selftests in the lane repo. `44/44` and `10/10` are verified
   **statically**: case counts (17 built-in + 19 round-23 + 6 round-24 + 2 = 44;
   9 + 1 = 10) and per-case expected findings re-derived by reading
   `evaluate()` in `tools/command-binding.py:65-114` and `project()` in
   `tools/registry-replay.py:72-113`. Each of the six new fixtures and the nine
   projection cases was checked by hand against those two functions; a
   mismatch in any one would make the corresponding row fail at run time.
3. **The digests are pinned to bytes, not to a producer.** The two pinned
   literals prove the frozen bundle bytes are unchanged since `6a1821a`; they
   prove nothing about who produced them (consistent with the round-24 bounds
   and `corpus/lessons/round-24.md`).
4. **Anchor convention is "cited content exists at the cited revision",** not
   "the row was added there" — the four rows are new at `c8c5b88` but cite
   `6a1821a`, where the adjudicated defect text exists. This matches the
   convention used by the other new rows (e.g. `SKILL.md@66a25ab…:1997`), so it
   is not a violation.
5. **Adjudication status.** All four cited defects sit under
   `routed_not_executed` in `fresh-adjudication.json` — the round-23 wave
   explicitly deferred them (deferral_reason at :107). Anchoring new rows to
   deferred defects is legitimate only because criterion 48
   (`corpus/QUALITY.md`) requires a frozen predicate that fails at base and
   holds after; the anchors themselves do not establish that, the ruler does.

## Smallest safe correction (whole lane)

One documentation edit in `corpus/knowledge/replay-projection-hardening.md`
(attach the already-written "not a ruler predicate" disclosure to adjudication
line :81 and state that redaction is not implemented) plus one clause in
`SKILL.md:2054` naming `registry-replay-selftest` (10/10). No registry row,
no expected value and no tool behaviour needs to change for the four anchors
to be accurate as cited.

## Tooling record

No tool was installed, upgraded or removed for this lane; every check used
tools already present (`git`, `python3`, `grep`, `sha256sum`). No pacman/uv/
cargo/npm transaction was performed, so no channel/version/reason entry is
owed.
