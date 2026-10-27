# T53W1Read03 — cold read: `## Live-tree re-pin and entry-command monitor — round 17`

Verdict: **holds**. No statement in this section fails at C*. `findings` is `[]` in
`T53W1Read03.json`.

## Section identity

- Bytes read with `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md` (git object only, never the working tree).
- Split with the frozen monitor rule (headings `^#{1,3}(\s|$)` outside ``` fences).
  The heading at SKILL.md line 1821, the next heading (`### Round-17 gate/probe registry — re-pin and monitor`) at line 1853.
  Section = lines 1821–1851; line 1852 is whitespace-only and stripped; no trailing newline.
- `section_sha256` = `037c9df3076fc7ada495b906b9bf458e9d06099bfaf9d1270b88de0acb4151f3` (4071 UTF-8 bytes).
  Two independent extractions agree: the python splitter over `git show` output and `git show …:SKILL.md | sed -n '1821,1851p' | sha256sum`.
- The section contains no code fence and no scratch directive (`TMPDIR`, `HYAKU_SCRATCH`, `/tmp` are absent), so the host scratch rule has nothing to bind here.

## Holds (each pointer checked against C* bytes)

1. **Sources line.** `corpus/lessons/round-16-verifier-spotcheck.md` at C* has `## 3. Per-axis verdicts` (line 123) and `## 6. Routed defects` (line 214); §3 records the monitor blindness ("The ToolsNoHarm monitor ran selftests only, so it could not see this") and §6 carries **R16-OP1** as item 1 and **R16-MON1** as item 6. S061/S062/S063 exist in `corpus/lessons/round-17.md:35-37` and in `corpus/SOURCES.md:70-72`, and the section's one-line glosses match those rows (`--show-toplevel`; GIT_CEILING_DIRECTORIES / repository discovery; jj leaves Git detached at the working-copy commit's parent).
2. **Row 1 (waiver rules).** `tools/evidence-disposition.py` at C*: `check_historical_waiver` at `:601` raises `historical_input_unneeded` when the live bytes still equal the pin (`:604-608`); non-`tools/` historical inputs raise `historical_input_forbidden` (`:687-691`); the rev is validated as a 40-hex commit and an ancestor in `resolve_historical_rev` (`:528`).
3. **Row 2 (anchor).** `resolve_historical_anchor` at `:460-525`: `lane.branch` config → `refs/heads/<branch>`; otherwise `symbolic-ref -q HEAD` → the attached branch; a `.jj` workspace without a binding raises `historical_input_unavailable`; an unbound non-jj detached root falls back to raw `HEAD` only after `for-each-ref --contains` finds a local or remote-tracking ref (`:516-525`). Selftest `v2-registry-clone-detached-anchor` is exactly the block at `:2891-2896` (name at `:2892`) and expects exit 0; the fixture docstring is at `:2256` — "A detached harness clone anchors at HEAD, not its later remote tip." The round-52 bracket's line span `:460-525` ends on `return "HEAD", commit` (`:525`) and the next function starts at `:528`.
4. **Row 3 (provenance).** `GIT_ENV_OVERRIDES` at `:371-376` sets `GIT_NO_REPLACE_OBJECTS=1` and `GIT_GRAFT_FILE=/dev/null`; `git_environment()` at `:387-390` drops every inherited `GIT_*`. Selftests `v2-historical-replace-ref` (`:2909-2923`) and `v2-gitdir-env` (`:2924-2938`) both declare exit 0. `grep -i graft` over the tool returns only the comment, the docstring and the override — no graft selftest exists, matching "grafts by code reading only". The cited span `:368-390` is exactly the G4 comment through `git_environment()`.
5. **Row 5 (registry).** `tools/registry-check.py` states the exit lattice at `:49-52` (0 all held · 1 any differs · 2 could-not-evaluate) and the fixed trailer at `:50` / `:906`. `tools/registry.json` at C* has 56 rows: 49 `active`, 7 `superseded`, every superseded row carrying `superseded_by`. The `--rev` clone builds a `fleet/` holding one symlink per `*-shokunin` sibling of the lane (`:764-789`), and row argv that names an absolute live-fleet path without `"external": true` is reported `non-hermetic` (`:632-668`).
6. **Row 6 (GIT_* scrub).** Every `tools/` program that spawns git builds its child environment by dropping inherited `GIT_*`: `bash-witness-study.py:333-339`, `env-diff.py:36-37`, `evidence-disposition.py:387-390`, `pin-disposition.py:207-209`, `receipt-measure.py:47-53`, `registry-check.py:149-163`, `registry-replay.py:57-58`, `round21-measure.py:31-33`, `trace-inputs.py:509-512`; `tools/mutate-and-run.sh` routes every call through `git_clean` (`:270-308`). The historical `.ufo/evidence/round-16/measure.py` does not scrub — `:412-416` builds `dict(os.environ, …)` and only pins `GIT_CONFIG_NOSYSTEM`/identity, so an exported `GIT_DIR` survives; that matches "still does not". The two registry rows that execute it (`measure-round16-rev`, `measure-round16-selftest`) run under `registry-check`'s scrubbed row environment.
7. **Row 7 (repo identity).** `tools/mutate-and-run.sh:1259-1265` prints `REGRESSION_CASE …: SETUP (repo_identity_mismatch: …)` and `return 2`; the selftest at `:1940-1946` asserts exit 2 and the string.
8. **Recipe step 1.** Re-ran read-only at the current tip (C* is an ancestor of it): `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json` → exit 1, `"status": "failed"`, counts `effective 12 / failed 1 / passed 11 / superseded 0`, one finding `expected_contains_missing` with `"expectation": "producer_before"`. The archived receipt `.ufo/evidence/round-18/final/before.stdout` shows the same status, exit and counts.
9. **Recipe step 2.** Same command with `.ufo/evidence/round-18/dispositions.json` → exit 0, `"status": "clean"`, `effective 11`, `superseded 1`, `passed 11`, `failed 0`, and three `HISTORICAL <path> rev=4acc607dfd79f19d508bd50cdd06b77269fccd1d sha256=…` lines (bash-witness-study.py, mutate-and-run.sh, pin-disposition.py). Static read of the file confirms 12 rows = 11 `effective` + 1 `superseded`. The archived receipt `.ufo/evidence/round-18/final/disposition.stdout` matches.
10. **Step 1's parenthetical "round 17's two now exit 2".** Both `.ufo/evidence/round-17/dispositions.json` and `…-before.json` exit 2 at C*, `could_not_evaluate` id `expected_input_digest_mismatch`: `tools/bash-witness-study.py: observed cca77724… expects 49e9e5e2…` — round-17's manifests never waived that path, and round-13's `expected.json` pins it.
11. **Recipe step 3 format.** `python3 tools/registry-check.py --root . --only evidence-disposition-round18 --json` printed `ROW evidence-disposition-round18 expect=0 got=0 held` and closed with `REGISTRY_CHECK: held=1/1 superseded=0`.
12. **Recipe step 4.** `tools/pin-disposition.py:374-450` (`head_observation`) builds head rows with `branch`, `commit`, `blob_sha256` and `head_differs_from_branch`; the docstring at `:42-51` describes the branch tip and the null-field fallback.
13. **"round-13/14 evidence bytes stay immutable."** The five pins the recipe relies on all hash to the manifests at C*: `round-13/expected.json` `a0160794…`, `round-13/verification.json` `a02718e9…`, `round-13/producer-oracle-repair.json` `df83a729…`, `round-14/dispositions.json` `77faac58…`, `round-14/dispositions-before.json` `a7a965bb…`. `tools/witness-metadata.py` still hashes to its round-13 pin `df339068…`.

## Commands executed (all read-only against the lane)

1. `git -C <lane> show a41195d…:SKILL.md` (whole file) — split and hashed.
2. `git -C <lane> show a41195d…:<path>` for each cited tool, lesson, source row and receipts listed above.
3. `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json` → exit 1 (step 1).
4. `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json` → exit 0 (step 2).
5. `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions{,-before}.json --json` → exit 2 each.
6. `python3 tools/registry-check.py --root . --only evidence-disposition-round18 --json` → one row held, trailer printed.

No lane file was created, modified or deleted by these runs; the pre-existing untracked `.ufo/evidence/round-53/*` and the `D .ufo/waves/round-53/w1.ready.partial` entry were present before this seat and are not mine.

## Verification limits

- The full `registry-check --rev` replay was **not** executed (round-27 measured it past a 360 s cap). Only one row was replayed, which fixes the trailer wording but not "every row".
- Grafts, rows 5 and 7, and the `corpus/SOURCES.md` rows are verified by code/doc reading only; no web source was opened.
- The `measure-round16-*` registry rows were not executed; the "does not scrub" claim rests on `measure.py:412-416` bytes.
- Live-tree runs reproduce because the working tree's `tools/` are clean and `master` (the anchor) points at the same commit as `HEAD`; they are evidence about the current tip, which contains C*, not about the round-18 tree.

## Tooling

No tool was installed or upgraded by this seat.

## Scratch

`/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read03/` was created for the extraction and run scratch and is removed before yield.

## Findings

None. Every statement in the section either reproduces when run or matches the cited bytes at C*, so `T53W1Read03.json` carries `"findings": []`.
