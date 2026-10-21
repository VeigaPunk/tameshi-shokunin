# Round24 W1 — sibling overlap scan: kumitate gate-registry/replay vs `tools/registry-replay.py`

Lane: leaf connector, no subagent dispatch. Read-only across both trees; nothing
executed except read-only inspection (`grep`, `sed`, `git cat-file/show/log/merge-base`,
`sha256sum`, JSON reads). No installs or upgrades. No writes outside this file.

## Verdict

**One structural analog, zero shared code, zero shared schema; no duplication of
`tools/registry-replay.py` exists in `kumitate-shokunin`. Do not merge.** The sibling
contributes one property tameshi lacks — pin inputs read through git objects at the
replayed revision — and that property exposes a real, un-named provenance gap in
tameshi's own `--run`, not in kumitate.

Axes named: **A1 calibration** (judged this round), **A2 operability**,
**A3 verification independence**, **A4 coverage**, **A5 cross-lane coupling**.

## Evidence — overlap map (kumitate, read-only)

| kumitate surface | what it is | overlap class | evidence | merge? |
|---|---|---|---|---|
| `.ufo/waves/round-38/frozen/replay.py.txt` (32 lines) | one-shot replay harness for `anchor-truth.mjs`: verify pin digests, clone lane, detached checkout, run gate, compare verdict | **structural analog** of `registry-replay.py --run` + projection | `:14-20` digest verify via `git show`; `:24-25` clone/`--detach`; `:29-31` exit+verdict compare | **no** |
| `.ufo/waves/round-38/frozen/expected.json` (+ `expected-c938.json`) | committed pin: `measured_revision`, `baseline_revision`, `input_digests` (7), `source_digests` (80), `expected_exit`, `expected_verdict` | analog of `command-binding-expected-v1` + `requirements.json`, but pins the **runner/oracle source** too | `expected.json` keys; `input_digests["scripts/anchor-truth.mjs"]` | **no** |
| `scripts/anchor-truth.mjs` | the executed judge (811 prose anchors) | analog of `registry-check.py`/`command-binding.py` role | `:49-52` verdict/exit map, `:65` contract id | **no** |
| `scripts/round-gate.mjs` | lane round-artifact conformance gate | **conventions only** | `:63-64` exit map `0/1/2/64`, `:45-48` hermetic `--selftest`, `:127` fail-closed JSON | **no** |
| `scripts/sources-check.mjs` | source-registry validator (fields/tiers/status) | **name collision only** — a source table, not a command registry | `:4` `kumitate-sources-v1`, `:43` exit map | **no** |
| `scripts/claims-check.mjs`, `proxy-check.mjs`, `kimi-census.mjs`, `cite-check.mjs`, `surface-probe.mjs` | claim/citation/census probes over SCORECARD/SOURCES rows | **conventions only** | registry-row regexes at `claims-check.mjs:380`, `proxy-check.mjs:479-481` | **no** |

Search basis: no kumitate file carries an argv/expect/held command registry.
`grep -rn "argv" scripts/*.mjs` returns only CLI parsers (`anchor-truth.mjs:342`,
`round-gate.mjs:272`); `held` appears in prose and in an unrelated lease test name
(`.ufo/pins/anchor-truth.json:5250`), never as a replay row field.

## What is genuinely shared — and why it must stay separate

Convergent fleet conventions, not shared machinery:

- exit map `0 clean · 1 findings/refused · 2 fail-closed/invalid · 64 usage`
  (`round-gate.mjs:63-64`, `anchor-truth.mjs:52`,
  `sources-check.mjs:43`; tameshi `registry-replay.py:27-28`, `command-binding.py:15`);
- `--selftest` hermetic temp-dir fixtures (`round-gate.mjs:45-48`,
  `anchor-truth.mjs:355`; tameshi `registry-replay.py:190-245`);
- `--json`, stable UPPER_SNAKE finding ids, refuse-rather-than-green.

Merging is the wrong move on three counts: different substrate (ESM/Node vs Python),
different domains (prose-anchor truth and round-artifact conformance vs 43 argv/exit
rows), and collapsing two independent implementations into one oracle destroys A3.
These conventions are cheap to restate and expensive to couple.

## Contradiction — state both directions, do not scalar-score

- **kumitate is stronger on input provenance.** Every pin input is read from the
  committed blob at the replayed revision: `git -C lane show <rev>:<path>` then
  SHA-256 compare, exit 2 on mismatch (`replay.py.txt:14-20`). A dirty worktree
  cannot satisfy a stale pin; `final/frozen-tamper.txt` shows the refusal
  (`FROZEN: snapshot_tampered scripts/anchor-truth.mjs … EXIT=2`).
- **tameshi is stronger on pin layering.** The frozen bundle digest has an external
  literal in the source-controlled registry (`tools/registry.json:974`,
  `:984`), and the registry's own digest is frozen in `requirements.json`
  (`registry_sha256`, `:2`) with equality re-checked at run time
  (`registry-replay.py:139-146`). A substituted bundle *plus* regenerated
  `expected.json` still fails its row — exactly what K5 measures.
- **tameshi is weaker on input provenance.** `--run` reads both pin files from the
  ambient filesystem (`registry-replay.py:137-138`) and cross-checks them only
  against each other (`:139-146`). `--rev` binds the clone and the runner, not the pins.

Neither model dominates. Scoring them on one scalar would hide the trade.

## Fresh falsification — what I attacked, what held

1. *Attack: "kumitate already has a command-replay registry."* Held false. No
   `expect`/`held` row table; the only "Registry" sections are SCORECARD claim rows
   and `corpus/SOURCES.md` source rows.
2. *Attack: "`independent-measure.py.txt` is a second replay."* Held false. It runs
   only `git show`/`git ls-files` (`:30-42`); no child gate is executed — it is a
   re-derivation, not a replay.
3. *Attack: "`round-gate.mjs` runs commands."* Held false. It reads files and git
   (`git ls-files --error-unmatch`, `merge-base --is-ancestor`); no execution table.
4. *Attack: "kumitate's pin is unpinned, so its replay is weaker than it looks."*
   Partly true and already bounded: `git cat-file -e 01aab4b0…:.ufo/waves/round-38/frozen/expected.json`
   → present, so the pin lives inside the measured commit; a coordinated change to
   both pin and tree selects a new revision/contract — the same bound tameshi states.
5. *Attack: "tameshi records the runner digest without pinning it."* The knowledge
   note already names this ("recorded per run, not a ruler predicate",
   `corpus/knowledge/replay-projection-hardening.md`, runner-digest row). I checked the
   recorded value: `observations.json.runner_sha256_clone_copy =
   cba16646902e89548060fd1b4b4fcb9e0ac8de1cb3fb02a347243912292944ad`, and that
   equals the committed blob at both `d2eaecd` (replay revision) and `c8c5b88`
   (delivered revision) — no drift. **Not a defect; do not report it as one.**
6. *Defects found in kumitate's replayed surface:* none. Its digest refusal is
   demonstrated with a concrete counterexample (zeroed digest → exit 2), and its
   verdict compare is exact-string (`:29-31`), not prefix.

## Finding (in-lane, from the comparison)

`tools/registry-replay.py` advertises "replay **frozen** registry requirements"
(`:1-3`), but the two inputs it treats as frozen are read from paths supplied on the
command line, from the ambient tree:

```
137:    frozen = json.loads(Path(args.requirements).read_bytes())
138:    raw_registry = Path(args.registry_baseline).read_bytes()
139:    if hashlib.sha256(raw_registry).hexdigest() != frozen['registry_sha256']:
```

Code-path consequence (derived, not executed — this lane is read-only): a worktree
`registry-baseline.json` whose rows disagree with revision R, paired with a
`requirements.json` copy carrying the matching `registry_sha256` and mirrored
`requirements`, replays at R and publishes a `command-binding-v1` bundle stamped
`revision: R` whose receipts satisfy expectations that do not exist at R.
`command-binding.py` cannot detect it — the bundle is internally consistent, and
`expected.json` is regenerated by the same run (`:123`). The only external guard is a
registry row literal, and `grep -n "round-24" tools/registry.json` returns **rc=1**:
no row pins the round-24 bundle (the two active literals at `:974`/`:984` cover
round-23 artifacts only).

Scope discipline: this is **not** a claim that K5/K6 are wrong (they measure the
round-23 pins, which do carry registry literals), **not** producer authentication, and
**not** a score finding. It is a one-hop gap between the instrument's adjective and its
binding surface.

## Proposed move — one, bounded

**Read both pin inputs through the clone at the resolved revision, and refuse when
they are not committed there.** Mirror `replay.py.txt:14-20` inside
`registry-replay.py`.

- After the clone `head` check (`:157-159`), map `--requirements` and
  `--registry-baseline` to repo-relative paths against `layout['repo']` (already
  realpath'd, `:63-70`); refuse `..` escapes and non-files with
  `PIN_NOT_IN_REVISION`, exit 2.
- Read bytes with `git -C <clone> show <head>:<relpath>`; keep the existing equality
  and `registry_sha256` checks unchanged.
- Record both blob digests in `observations.json` beside `runner_sha256_clone_copy`.

Affected axes: **A1 improves** (the word "frozen" becomes true at the input
boundary); **A2 slightly improves** (one exit-2 refusal, no new flag); **A3/A4/A5
unchanged** (no ruler edit, no coverage claim, no import from kumitate).

## Risks / second-order effects

- Recorded argv remains replayable: both pin paths are repo-relative and tracked at
  both revisions (`git cat-file -e` → tracked for `requirements.json`,
  `registry-baseline.json`, `tools/registry-replay.py`, `tools/command-binding.py` at
  `d2eaecd` and `c8c5b88`). A re-run should reproduce bundle sha `4f424023…` — verify,
  do not assume.
- `replay-command.json.instrument_sha256` (`9fcd2dbb…`) goes stale the moment the tool
  changes. Take a new receipt; never edit the old one.
- If a selftest case is added, the active row literal
  `"REGISTRY_REPLAY_SELFTEST: 10/10 pass"` (`tools/registry.json:994`) turns red.
  Supersede the row append-only (`superseded_by`), never rewrite it.
- `measure.py` exercises only `--project`/`--plan` (`:139-202`), so K7–K11 are
  unaffected by the code change; 11/11 is neither claimed nor improved here.
- Do **not** "fix" this by pinning the instrument's own `expected.json`: that drifts
  into producer authentication, which the contract disclaims.
- Symlinked `--repo` aliases: relpath must be computed on the realpath'd repo or a
  legitimate pin path will be refused.

## Verification (for the integrator; not run in this lane)

1. Fixture: commit a baseline with `expect.exit: 0` at R; in the worktree flip it to 1
   and re-hash into a requirements copy. Before: `--run` exits 0 and publishes. After:
   exit 2 `PIN_NOT_IN_REVISION` (or the clone-sourced read makes the flip inert).
2. Re-run the exact `replay-command.json` argv at the delivered revision; expect
   `4f4240230d4faecb54f488bb0d889de472e4e3f97e693e9304288429a722a9c6`, else record a
   new contract.
3. `python3 .ufo/evidence/round-24/measure.py --repo CLONE_AT_REV` → 11/11 unchanged.
4. `registry-check.py` all active rows held after superseding the selftest row.
5. `command-binding.py --selftest` unchanged (bundle schema untouched).
