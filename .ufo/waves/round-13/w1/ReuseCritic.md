# ReuseCritic — round 13 w1 (critic, read-only)

Target inference under attack: **"pinned target sha256 unchanged ⇒ recorded mutation verdict table reusable."**
Verdict: **falsified.** Every leg's `result_reuse` must stay `not_established`. No content status, including all-six `unchanged`, may derive a reuse value.

Axes: depth (C1 F7 disposition), honesty/provenance (no false reuse claim), no score movement (depth 6 stays 6).
Reviewed at 2026-10-20T04:49Z, baseline `546b371`, runner `tools/mutate-and-run.sh` sha256 `75ed934d…adc5` (= HEAD blob).
Manifest `.ufo/evidence/round-13/pin-manifest.json` sha256 `1d0000d7…b242`; knowledge draft `corpus/knowledge/incremental-pin-disposition.md` sha256 `d5747907…f5e3`.
`tools/pin-disposition.py` had **not landed** at review time, so its behavior is unreviewed.

## 1. Current content facts (O, read-only `git show|sha256sum`, `ls-tree`, `merge-base --is-ancestor`)

| leg | pin == HEAD blob | worktree == HEAD | mode pin→HEAD | pin ancestor of HEAD | file commits since pin |
|---|---|---|---|---|---|
| js-kimi-census | **no** (`5e8d5913…`) | yes | 100644→100644 | yes | 1 (`1a8eed5`, 2026-10-19 19:41 −0300) |
| bash-surface-census | yes | yes | 100755→100755 | yes | 0 |
| bash-tsukuroi-census | **no** (`d17d32a3…`) | yes | 100755→100755 | yes | 5 |
| bash-mado-verify | **no** (`037b05dc…`) | yes | 100755→100755 | yes | 7 |
| bash-checklist-run | yes | yes | 100755→100755 | yes | 0 |
| js-claims-check | yes | yes | 100755→100755 | yes | 0 |

Result: 3 unchanged and 3 changed. The 2026-10-14 reading of "4 current · 2 stale" (`fleet-kill-rate-ledger.md` §ER-4) no longer holds, because kimi-census drifted on 2026-10-19. The three unchanged legs are where a reuse claim would be tempting, so the counterexamples below target those three.

## 2. Counterexamples: identical pinned bytes, different verdict or outcome

**CE-1 (strongest, observed in repo history): mode is outside the sha256 and the git blob OID.**
- Round 10 got `REGRESSION: SETUP (cases=6 passed=5 cannot-verify=1)` on checklist-run. The bytes matched the pin, but the materialized copy had no exec bit, so the control went red at exit 126 (`plans/round-10-record-draft.md:84-88`).
- The fix mirrors the mode (`tools/mutate-and-run.sh:104-106, :942-956`), and selftest arms `:1529-1554` prove that a 100644 copy of the same bytes is refused.
- Scratch git fact (/tmp, removed): a chmod-only commit keeps blob `4163036e…` and the sha256 unchanged, while `ls-tree` moves 100755→100644.
- So "HEAD blob == pin" can hold while the outcome changes from PASS to SETUP.
- checklist-run re-execs `"$SELF"` (`kagi corpus/checklist-run.sh:65,:416` @fecee87).

**CE-2: host tools found on PATH (surface-census, unchanged leg).**
- The selftest branches on `command -v "$JANITOR"` (`surface-census.sh:817-823`; `THE_JANITOR_BIN` at `:82`). When the handler is absent, two cases are `skip-case`. When it is present, they exec the real external handler, so its version becomes a verdict input.
- The recorded host had `the-janitor` **MISSING** (`corpus/knowledge/mutation-case-kagi-census.md:27-30`). The owner note leaves U3 (handler-present verdicts) and U5 (cross-host stability) unmeasured (`:198-204`).
- The sqlite arms need `sqlite3` (`SQLITE3_BIN` `:83`, `:269`, fixture `:710`, `:789-790`). The recorded B2 and B7 kills ride those arms (`mutation-case-kagi-census.md:73,92,134`). With no sqlite3, or a different sqlite3, the bytes stay identical but the kill attribution differs.

**CE-3: the runner is part of the verdict, and it is not in the target pin.**
- The defect specs (`:587-…`), recorded tables (`:554-559`), suite command strings (`:1112-1140`), `TIMEOUT_S=300` and the exit semantics 124/126/127 → INCONCLUSIVE (`:57-58`) all live in `mutate-and-run.sh`.
- An edit to any of them changes KILLED/SURVIVED while every target sha stays unchanged.
- `REGRESSION_TOOL` prints the runner sha (`:1099`), but a target-only disposition row carries none of it.

**CE-4: toolchain and environment.**
- Suites: `node "$MUTANT" --selftest` and `bash "$MUTANT" --selftest`.
- Recorded on one host: node v24.21.0, bash 5.3.15 (`mutation-case-kumitate-claims.md:340`, `mutation-case-kimi-census.md:204-205`, `mutation-case-kagi-checklist.md:350`).
- claims-check reads `homedir()`, `tmpdir()`, `process.env.UFO_SRC` and `process.execPath`, and gives each child run a 60 s timeout (`claims-check.mjs:79-90, :582-583, :600` @175de6b).
- checklist-run reads `CHECKLIST_TIMEOUT`, and its timing arm `CT=1` races `sleep 5` (`:72, :438-439`).
- The existing env fingerprint (`.ufo/evidence/kaika-round-1/capability-demo/env-fingerprint.txt`) records bash, node, python, git, LANG, HOME, nproc and loadavg. It does **not** record PATH, sqlite3, the-janitor presence, TMPDIR or the runner timeout.
- H3 there ("insensitive to a scrubbed environment") covers the runner's own `--selftest`, not the six legs.

**CE-5: companion files and location outside the single-file pin.**
- kagi `SKILL.md` changed between `fecee87..HEAD` (+4/−2), and checklist-run's default `SKILL="$ROOT/SKILL.md"` (`:66-68`).
- surface-census defaults read `$SCRIPT_DIR/{surface-census,state-shape,drift-baseline}.tsv` (`:75-78`).
- The recorded sweeps ran a copy materialized into a fresh workdir, where those companions are absent. A worktree file with a matching sha sits beside different companions.
- [I] The selftest fixtures seen pass `--tsv`/`--skill` explicitly (`:343-344,:416`), so the recorded verdict is probably insensitive to this. That is inferred, not measured.

**CE-6: one sample is not a reproducible verdict.**
- QUALITY.md criterion 11 says a clean repeated control never proves determinism.
- Each recorded table is a finite set of replays on one host. Even with every input identical, a stored table is a past observation, not a present one.
- This agrees with the knowledge draft §3 item 4 ("A replay is not reuse") and with S041's "potential error" sentence.

## 3. Implementation defects routed to owners (messaged directly)

**PinProbe** (`tools/pin-disposition.py`, `pin-manifest.json`):
- **D1 (defect).** Manifest rows carry no mode, and blob OID/sha256 are mode-blind (CE-1). Derive `pinned_mode` from `git ls-tree <rev> -- <path>` (a git fact, not an invented pin), `head_mode` from `ls-tree HEAD`, and the worktree exec bit from `os.stat`. A mode difference must not report as bare `unchanged`; use a separate `mode_status` or `changed`. GateScribe and PinSchema flag the same gap.
- **D2.** Each receipt row, or the receipt header, must list `not_compared` inputs literally: runner sha256, suite command, interpreter versions, PATH tools (the-janitor, sqlite3), env vars (THE_JANITOR_BIN, SQLITE3_BIN, TMPDIR, CHECKLIST_TIMEOUT, HOME, UFO_SRC), timeouts, companion files and sample count. The manifest `note` names classes only. The knowledge draft §5 says a receipt that omits the closure "is partial".
- **D3.** `result_reuse` must be a literal constant with no branch on status. The selftest should assert `not_established` on the **unchanged** fixture specifically, because that is the arm where a derived value would flip.
- **D4.** Hash raw worktree bytes with hashlib. Do not use `git hash-object`, which applies clean filters. Reject path types other than blob or symlink: PinGit #4 found that `git show rev:<dir>` exits 0. No `.gitattributes` or autocrlf is configured on these four repos today (observed), but the probe must not depend on that.

**IncrementalKnowledge** (`corpus/knowledge/incremental-pin-disposition.md`):
- §5 and §7 mark the env, dependency and sibling-file cells as `[U]` "unmeasured here". CE-1 through CE-5 provide measured per-leg anchors that can replace those generic cells.
- Typo: the §5 row 1 cell reads "the rm -f/`PATH`/…".

## 4. Checks L1 should run (not executed by this seat)

1. `python3 tools/pin-disposition.py --selftest` → exit 0. It must contain an arm that asserts `result_reuse == "not_established"` on the unchanged fixture, and a mode-only-change arm (chmod-only commit) that is not reported as plain `unchanged`.
2. `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` → exit 0, six rows. Expect the three unchanged rows to be surface-census, checklist-run and claims-check, and the three changed rows to be kimi, tsukuroi and mado (per §1, if HEADs are unmoved). Every row must read `result_reuse: not_established`, and the output must carry a `not_compared` list.
3. `python3 - <<'EOF'` / `jq` over the receipt: assert that `[.rows[].result_reuse] | unique == ["not_established"]` and that no field named `reused`, `kill_rate` or `verdict` appears.
4. `grep -n 'result_reuse' tools/pin-disposition.py`: every hit must be an assignment of the literal or an assertion. There must be no conditional assignment.
5. `git -C <repo> ls-tree <rev> -- <path>` and `ls-tree HEAD` for each of the six legs: compare against the receipt's mode fields.
6. `git diff --quiet 546b371 -- tools/mutate-and-run.sh .ufo/evidence/round-12` → the runner and frozen inputs are unchanged.
7. Wording audit of LOG, SCORECARD and the lesson draft. There must be no "reusable", "still valid", "current kill-rate" or "7th case" phrasing. Depth stays `6 → 6`.

## 5. Bounds

- Read-only. No gate, selftest or sibling code was executed. The only execution was a throwaway /tmp git repo for the blob/mode fact, which was then removed.
- No sibling or implementation file was edited.
- No tools were installed or updated.
