# T53W2Read13 — wave-2 re-read of `### Round-17 gate/probe registry — re-pin and monitor`

Seat: re-reader (wave 2, round 53). Content revision under test: **C\*\* = 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e**
(`round-53: fix pass 2 — 40 wave-1 reader findings resolved (counts, anchors, scratch docs, registry rows); strict TMPDIR scratch-root helper in 7 tools …`).

All section/SKILL/tool bytes below came from git objects (`git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show C**:<path>`); the lane working tree was never read as evidence and never written.

Deliverable JSON: `.ufo/waves/round-53/w2/T53W2Read13.json`.

## Fix verification (run first)

Wave-1 reader of this section: `T53W1Read16` (1 finding, at C\* = a41195dfc13a73958e4c5228ec196b28d03ded03).

### Fix 1 — "registry-check exit-2 `--tag` cause added" — PRESENT and true at C\*\*

Diff of the section's 8-line window between C\* (lines 1853–1860) and C\*\* (lines 1864–1871) — exactly one line changed, and it is the registry-check row:

```
6c6
< | `tools/registry-check.py` | gate | `python3 tools/registry-check.py --rev REV [--registry PATH] [--tag TAG] [--json]` · `--selftest` | 0 every active row held · 1 a row differs · 2 registry invalid, rev unresolvable or clone failed · 64 usage |
---
> | `tools/registry-check.py` | gate | `python3 tools/registry-check.py --rev REV [--registry PATH] [--tag TAG] [--json]` · `--selftest` | 0 every active row held · 1 a row differs · 2 registry invalid, rev unresolvable, clone failed, or `--tag` matches no row · 64 usage |
```

Old clause occurrences at C\*\*: `grep -c 'registry invalid, rev unresolvable or clone failed'` → `0`. New clause occurrences → `1`.

The added cause is real, measured with C\*\*'s tool bytes (`git show C**:tools/registry-check.py`, sha256 `ad8cebb1449986568fb2feaa25781f7dfa3733f410da21b14be082c7c1fb6c13`) against a scratch git fixture holding C\*\*'s own `tools/registry.json`:

```
$ git -C $D init -q; git -C $D rev-parse --show-toplevel   # == $D (asserted before any commit)
$ python3 <C**:tools/registry-check.py> --root $D --registry $D/reg.json --rev HEAD --tag nosuchtag --json
  "rev_resolved": "939f7b9d0ddb4580d10eaabf48d92ac0892530d3",
  "tags": ["nosuchtag"],
REGISTRY_CHECK: could-not-evaluate (--tag ['nosuchtag'] selects no registry row)
exit=2
```

Valid registry, resolvable rev, no clone attempt — exit 2 for exactly the added cause. The wave-1 finding is resolved.

### Fix 2 — "pin-disposition `$TMPDIR` row" — NOT IN THIS SECTION

The dispatch parenthetical names a second fix. The C\*→C\*\* diff above shows one changed line in this section; the `tools/pin-disposition.py` row here is byte-identical between C\* and C\*\*:

```
| `tools/pin-disposition.py` (branch tip) | probe | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` · `--selftest` | as the round-13 row |
```

The `$TMPDIR` change for pin-disposition landed in the round-53 gate/probe table row (`| pin disposition | probe | …`, `… selftest writes isolated `$TMPDIR` fixtures (`tameshi-r13-pin-disposition-selftest.*`) …`), which is a different section. This row states no scratch path, so nothing was left unrepaired here; recorded as a fix-trace discrepancy for the L1, not as a finding (the section makes no claim that fails).

## Section identity (frozen-monitor split, not a hand split)

The splitter is `.ufo/evidence/round-18/measure.py:sectionize` (round-21 monitor's delegate), run over the C\*\* blob bytes:

```
{'start': 1864, 'end': 1872, 'heading': '### Round-17 gate/probe registry — re-pin and monitor',
 'sha256': '8a92f71e046aae243294c42153c6ed183ccd41edf4647ff9520e35a26b9c9643'}
n sections: 64 (preamble + 63 headings)
```

Independent second path (same bytes, different code): `sed -n '1864,1871p' skill-C2.md | head -c -1 | sha256sum` → `8a92f71e046aae243294c42153c6ed183ccd41edf4647ff9520e35a26b9c9643` (the final newline removed; `sha256sum` over the awk-style range *with* the newline yields `4729e689…`, which is the trailing-newline artefact the frozen definition excludes). Heading occurs exactly once at C\*\*, outside any fence; the next heading is line 1872 (`## Input-keyed cold-read credit — round 17`), so `end=1872` is exclusive.

**section_sha256 = 8a92f71e046aae243294c42153c6ed183ccd41edf4647ff9520e35a26b9c9643**

## Section text read (C\*\* bytes, verbatim)

```
### Round-17 gate/probe registry — re-pin and monitor

| Name | Kind | Command | Exits |
|---|---|---|---|
| `tools/evidence-disposition.py` (v2 manifests) | gate | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json` (round 18; the round-17 manifest now exits 2) · `--selftest` | 0 clean · 1 failed expectations · 2 could not evaluate (invalid, missing, tampered or unprovenanced input) · 64 usage |
| `tools/registry-check.py` | gate | `python3 tools/registry-check.py --rev REV [--registry PATH] [--tag TAG] [--json]` · `--selftest` | 0 every active row held · 1 a row differs · 2 registry invalid, rev unresolvable, clone failed, or `--tag` matches no row · 64 usage |
| `tools/mutate-and-run.sh` (guard + scrub) | gate | `bash tools/mutate-and-run.sh --selftest` · `--regression` | as the round-16 row; a borrowed repo identity is SETUP 2 |
| `tools/pin-disposition.py` (branch tip) | probe | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` · `--selftest` | as the round-13 row |
```

## Holds (every exit in every row measured with C\*\*'s tool bytes)

Tools were extracted with `git show C**:tools/<file>` into scratch; lane read-only throughout. C\*\* is an ancestor of the pushed lane tip `b46885478b86568c88c3a067e841541b116cfffd` (`git merge-base --is-ancestor` → true), and `tools/registry.json` plus every tool named here are byte-identical between C\*\* and that tip, so the measurements apply to C\*\*'s bytes.

1. **Row 1, documented invocation = exit 0.** Run exactly as published, from the lane root:
   `python3 <C**:tools/evidence-disposition.py> --root . --dispositions .ufo/evidence/round-18/dispositions.json --json` → **exit 0**, `"status": "clean"`, `counts {'effective': 11, 'superseded': 1, 'failed': 0, 'findings': 0, 'expected_checks': 12, 'passed': 11}`. Matches "0 clean".
2. **Row 1, "(round 18; the round-17 manifest now exits 2)" = true.** `.ufo/evidence/round-17/dispositions.json` → **exit 2**, `"status": "could_not_evaluate"`, `id: expected_input_digest_mismatch`, detail `tools/bash-witness-study.py: observed 4e999ff4553948e4fffdbc55f7a18c3d41604af4acb3292a8499fb6cb4557142 expects 49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80`. The C\*\* tool edit moved this tool's digest away from the round-17 pin, so the stated exit still holds (its *reason* is digest drift, which is the claim's own sense of "now"). Round-18 stays clean because its three tool inputs are `historical_inputs` pinned at rev 4acc607.
3. **Row 1, remaining map.** `.ufo/evidence/round-18/dispositions-before.json` → **exit 1** (failed expectations); a missing dispositions file → **exit 2** (`status: could_not_evaluate`); `--nope` → **exit 64**; `--selftest` → `SELFTEST: PASS (66/66)`, **exit 0**. Tampered/unprovenanced input is the round-17 digest-mismatch case above (exit 2).
4. **Row 2, `0` / `1`.** On a schema-valid synthetic registry committed in the fixture repo (`argv ["/usr/bin/true"]`, `expect.exit 0`, `status active`, `source SKILL.md@a41195df…:2100`, `timeout_s 30`): one holding active row → `ROW probe-hold expect=0 got=0 held` / `REGISTRY_CHECK: held=1/1 superseded=0`, **exit 0**; adding an active row with `expect.exit 2` → `ROW probe-differ expect=2 got=0 differs` / `held=1/2`, **exit 1**.
5. **Row 2, `2` and `64`.** Missing registry → exit 2, `REGISTRY_CHECK: could-not-evaluate (registry unreadable: … No such file or directory …)`; `--rev deadbeef` → exit 2, `"error": "rev 'deadbeef' unavailable in …"`; `--tag nosuchtag` → exit 2 (message quoted in fix verification); unknown flag → exit 64, `registry-check: unknown argument '--bogus-flag'`; `--selftest` → `SELFTEST: PASS (51 cases)`, **exit 0**. Tool docstring at C\*\* (`:52-53`) states the same four families: `2 could-not-evaluate (registry unreadable/invalid, root or rev missing, clone failure, --only/--tag miss)`.
6. **Row 2, live rows at C\*\* bytes.** A `git clone --shared` of the lane into scratch (toplevel asserted == the clone dir; `tools/registry-check.py` sha256 `ad8cebb1…` == C\*\*'s), default `--root`, published shape:
   `python3 tools/registry-check.py --rev HEAD --tag new-r19 --json` → `ROW round19-correction-ruler-selftest expect=0 got=0 held`, `ROW round19-coldread-selector-selftest expect=0 got=0 held`, `REGISTRY_CHECK: held=2/2 superseded=0`, **exit 0** — the "every active row held" outcome is reachable on real rows, not just fixtures.
7. **Row 3, pointer resolves and its map is consistent.** The round-16 row at C\*\* is `SKILL.md:1828` (heading at `:1824`): `| `tools/mutate-and-run.sh` | gate | `bash tools/mutate-and-run.sh --selftest` · `--regression` | selftest 0 pass / 1 fail; regression 0 PASS · 1 FAIL · 2 SETUP · 64 usage |`. C\*\*'s tool bytes: `bash tools/mutate-and-run.sh --selftest` → `MUTATE_SELFTEST: 107/107 pass`, `VERDICT: PASS`, **exit 0**; SETUP refusal is `printf 'REGRESSION_CASE %s: SETUP (repo_identity_mismatch: %s is not its own repository; toplevel=%s)\n'` (`:1263`) and a SETUP-only tally exits **2** (`:1526-1529`); usage exits **64** (`:250`). So "a borrowed repo identity is SETUP 2" holds.
8. **Row 4, documented invocation = exit 0, and "as the round-13 row" resolves.** `python3 <C**:tools/pin-disposition.py> --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` → **exit 0** with `content_status: changed` observations, i.e. exit 0 *including* changed rows, exactly as the round-13 row (`SKILL.md:1569`, heading at `:1565`) reads: `0 observations, including changed/unavailable; 2 invalid input/could-not-evaluate; selftest 1 failed`. `--selftest` → `SELFTEST: PASS (19/19)`, **exit 0**, with the `exit=2` cases (`missing-manifest`, `invalid-root`, `malformed-digest`, `duplicate-leg`, `missing-leg`, `malformed-json`) all expecting 2. "(branch tip)" is still real: `branch_tip_missing` reason at `tools/pin-disposition.py:437`, `detached-head-uses-branch-tip` case at `:1313`.
9. **Names/paths in the section exist at C\*\*.** `tools/evidence-disposition.py`, `tools/registry-check.py`, `tools/mutate-and-run.sh`, `tools/pin-disposition.py`, `.ufo/evidence/round-18/dispositions.json`, `.ufo/evidence/round-13/pin-manifest.json` all present; `evidence-disposition.py` self-reports `"tool_sha256": "4573b51ee19fbc483af5bc4805e40675d1c029630e612dde7a042a8f4c4b01d6"`, equal to `sha256sum` of the C\*\* blob (so its self-pin is not stale).

## Findings

**None.** Every statement in the section holds at C\*\*, and the wave-1 finding is verified fixed.

## Examined, not filed (with the reason it is a hold)

- **`--only` miss also exits 2** (`REGISTRY_CHECK: could-not-evaluate (--only 'no-such-row' matches no registry row)`, exit 2 on the same fixture). Not this row's surface: the row publishes `--rev`, `--registry`, `--tag`, `--json`, `--selftest` — not `--only` — so the post-fix cause list covers every documented flag. The same tool's other row (`| entry-registry walk | …`) does publish `--only` and does list "only or tag miss"; that row is another seat's section.
- **Set-but-unusable TMPDIR makes the documented `--rev` invocation exit 2**: `TMPDIR=/nonexistent/hyaku-r53-probe python3 <C**:registry-check.py> --root $D --registry $D/reg.json --rev HEAD --json` → exit 2, `"error": "cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent/hyaku-r53-probe' (could-not-evaluate)"`. Read as covered by the row's own `clone failed` cause (the failing step is clone-scratch creation) and consistent with the round-53 scratch directive; not filed.
- **`--selftest` failure exits 1** (`return 1` at `tools/registry-check.py:1826-1829`) while the row's exit cell says "1 a row differs". The selftest-failure arm is not separately described, but it is only reachable by breaking the tool, and the row's cell reads as the row-mode map (as in the round-16 row, which spells the selftest arm out). Not filed.
- **Active/superseded asymmetry** (the wave-1 watch item): still only active rows decide the exit; unchanged at C\*\*.
- **Heading says "Round-17" while row 1 documents round-18 state** — the row dates itself ("round 18; …"), which the round's dated-history rule covers (as wave 1 held).
- **Lane moved after C\*\***: pushed tip `b4688547` ("re-key pass 1b") and detached HEAD `d0088220` ("revert the errata-table row edit") differ from C\*\* in exactly one SKILL.md line, in the errata table at `SKILL.md:1751` — outside this section (section bytes and hash identical to C\*\*). Not a defect of this section; noted so the L1 knows the section is stable across those revisions.

## Limits of this read

- No full live run of all 49 active registry rows: I ran fixtures plus one real 2-row tag subset (`new-r19`) in a shared clone. "0 every active row held" is therefore verified as a mapping plus a partial live sample, not as a census of the registry at C\*\*.
- "clone failed" was exercised through clone-scratch creation failing (unusable TMPDIR) and through rev resolution failing (a PATH-shadowed fake `git`), not through a mid-clone transport failure.
- No `--regression` run of `mutate-and-run.sh` (ten lanes, executor-scale); row 3 was verified by the selftest plus the code paths that implement the SETUP 2 clause and the round-16 row text it points at.
- No lane writes, no git/jj mutation in the lane: the only repository writes were a `git init` fixture and a `git clone --shared` inside my scratch tree, each with `git rev-parse --show-toplevel` asserted first. No installs, no pacman.
- Scratch used: `/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read13/` (extracted blobs, fixtures, TMPDIR, clone) — removed before this seat yields.
