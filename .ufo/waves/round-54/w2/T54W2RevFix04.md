# T54W2RevFix04 — verify C1 fix pass for cats 18-23

Seat: verify remaining fix hunks at C1 `99c3bc88d704566197783f66b211ee0a830e0330` vs C0 `59c38109bf119d0e9d4f878644a82babc937bc1e`.
Scoped hunks: `## Mutation-sweep recipe` steps 2 and 4; `## Standing rules` scratch-root bullet; runbook pin cell.

Axes: calibration (does each fix's citation resolve to the clause it names?), depth (hand re-pin of every new/kept anchor).

## Method

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff \
  59c38109bf119d0e9d4f878644a82babc937bc1e 99c3bc88d704566197783f66b211ee0a830e0330 \
  -- SKILL.md tools/
# then per hunk: git show C1:SKILL.md | sed -n '<lo>,<hi>p'
# plus sed -n on each cited receipt path at C1
```

Receipts: `.ufo/waves/round-54/w2/T54W2RevFix04-receipts/` (`anchor-checks.txt` and per-hunk extracts).
No lane production file edited. No mutating git. LSP: no language server for `SKILL.md` — text/`git show`+`sed` used (recorded).
No tools installed this seat.

---

## Hunk-by-hunk

### H1 — `## Standing rules` scratch-root bullet — `SKILL.md:32-39` — CLEAN

**Diff:** rephrases empty-TMPDIR arm; scopes the C2 measurement to `--selftest`/`selftest`; keeps `S278:163-165`, `S279`, `corpus/knowledge/scratch-root-contract.md`, seven `scratch_root` cells.

**Anchor checks at C1:**

| Citation | Command | Result |
|---|---|---|
| `S278:163-165` | `sed -n '163,165p' .ufo/evidence/round-54/assimilation/S278-tempfile.py` | `for envname in 'TMPDIR', 'TEMP', 'TMP':` / `dirname = _os.getenv(envname)` / `if dirname: dirlist.append(dirname)` — empty skipped |
| `S279` | `corpus/SOURCES.md` S279 row + contract note `:20-22` | documented TMPDIR→TEMP→TMP fall-through |
| seven `scratch_root` cells | walk `tools/registry.json` for key `scratch_root` | count **7** (all `*-selftest` rows) |
| selftest scoping | contract C2 target | "7/7 **self-tests** exit 2…" — matches the new "Measured on each tool's `--selftest`/`selftest` path" clause |

No duplicate parenthetical; no overstatement vs C2. **Verdict: hold.**

### H2 — Mutation-sweep recipe step 2 (`size`) — `SKILL.md:161` — CLEAN

**Diff:** `Record: path, full sha256,` → `Record: path, full sha256, size,`

**Anchor checks:**

```text
# mutation-case-kimi-census.md:13-16 — carries "43273 B"
# mutation-case-kagi-census.md:13-17 — carries "44212 B"
# step 9 (SKILL.md:235-237) — "sha256 after == before, size and mtime unchanged"
```

Step 9's size compare now has a before-value in step 2's record set; both cited pin records print a byte size. No new bare anchors. **Verdict: hold.**

### H3 — Mutation-sweep recipe step 4 (`at least one per class`) — `SKILL.md:173` — FINDINGS

**Diff:** `one per class` → `at least one per class (two of the JS ten share a class — the :47-48 pair — and the bash exemplar's :70-71 pair does the same)` immediately before the existing `(catalog + entry template in the next section)`.

#### F1 — severity: high — bare `:47-48` / `:70-71` do not establish the cited clause (QUALITY 104)

**Quote (C1 `SKILL.md:173`):**

```text
at least one per class (two of the JS ten share a class — the :47-48 pair — and the bash exemplar's :70-71 pair does the same)
```

**Why:** This page's own rule is `Anchors \`:…\` are this page` (`SKILL.md:1273`). Re-running the page anchors:

```text
$ git show 99c3bc88…:SKILL.md | sed -n '47,48p'
- `corpus/knowledge/gates-survey-kumitate.md` — the six kumitate suites: exit
  maps, case counts, mutation controls, fail-closed arms, verdict asserts.

$ git show 99c3bc88…:SKILL.md | sed -n '70,71p'
## Gate-shape decision table — hermetic vs live vs audit-lane

| Shape | Answers | …
```

Those are Source-notes / gate-shape lines — not a shared-class defect pair. The pairs the parenthetical means live only under file-qualified paths (and the catalog already cites them that way at `SKILL.md:309`):

```text
$ git show 99c3bc88…:corpus/knowledge/mutation-case-kimi-census.md | sed -n '47,48p'
| D4 | dropped arm | …
| D5 | dropped arm (presence gate) | …

$ git show 99c3bc88…:corpus/knowledge/mutation-case-kagi-census.md | sed -n '70,71p'
| B4 | dropped branch | …
| B5 | dropped branch | …
```

The fix-pass therefore gained a citation whose receipt on the page does **not** establish the shared-class clause (QUALITY 104). Same-section later cites correctly as `mutation-case-kimi-census.md:41-53` — the bare forms on `:173` were never re-pinned to that prefix.

#### F2 — severity: medium — step 4 now contradicts the "next section" it points at

**Quote (C1 `SKILL.md:173` + `:260`):**

```text
… at least one per class (…)
   (catalog + entry template in the next section), …

## Defect-taxonomy templates and exact-string guidance
…
One defect per class per sweep, and widen beyond the measured set when the
artifact offers a new mechanism.
```

**Why:** The hunk repairs step 4 against the JS/bash exemplars (two defects in one class) but leaves the forward-referenced catalog section stating the old "One defect per class per sweep" rule. A cold reader following step 4's own pointer hits a contradictory instruction; the fix pass did not re-pin or rewrite that sentence. (Not a QUALITY-104 duplicate-parenthetical of the round-52 `(ten since round 51) (ten since round 51)` shape — adjacent distinct parens — so not filed under that label.)

### H4 — runbook pin cell — `SKILL.md:1306-1307` — CLEAN

**Diff:**

```text
- (`e1e349b6…` / 511 L / 31 416 B, uncommitted worktree file at this read; …)
+ (`8b2e185f…` / 516 L / 33 515 B, committed at `59c38109`; …)
```

**Anchor checks:**

```text
$ git show 59c38109:corpus/knowledge/operator-runbook.md | sha256sum
8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859  -
$ git show 59c38109:corpus/knowledge/operator-runbook.md | wc -lc
    516   33515
$ git rev-parse --verify 59c38109^{commit}   # resolves
$ git rev-parse --verify 'e1e349b6^{commit}' # fails (old pin was never a git object)
```

Triple (digest / lines / bytes) matches the blob at the named revision; `59c38109` resolves; "committed at" replaces the false "uncommitted worktree" claim. **Verdict: hold.**

(Note: the sibling pointer re-pin `:1250-1254` → `:1276-1277` on the next bullet is in T54W2RevFix02's cats 7-12 scope, not re-adjudicated here.)

---

## Summary

| Hunk | File:line | Verdict |
|---|---|---|
| Standing rules scratch-root | `SKILL.md:32-39` | clean |
| Recipe step 2 (`size`) | `SKILL.md:161` | clean |
| Recipe step 4 (`at least one per class`) | `SKILL.md:173` | **F1 high** (bare `:47-48`/`:70-71`); **F2 medium** (contradicts `:260`) |
| Runbook pin cell | `SKILL.md:1306-1307` | clean |

## Residual risk / verification gaps

- Did not re-litigate out-of-scope C1 hunks (ledger `C**`, refusal table, round-17/18 registry rows, `tools/env-diff.py`).
- Did not execute the C2 counter; standing-rules selftest scoping was checked against `contract.json` text and the seven registry cells only.
- Taxonomy `:260` vs catalog rows that already show two-per-class evidence was pre-existing tension; F2 is that step 4's fix made the recipe agree with the exemplars while leaving the pointed-to rule sentence stale.
