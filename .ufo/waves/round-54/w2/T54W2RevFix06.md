# T54W2RevFix06 — QUALITY 104 over the C1 fix pass

Seat: verify Criterion 104 on `59c38109bf119d0e9d4f878644a82babc937bc1e` → `99c3bc88d704566197783f66b211ee0a830e0330` (`SKILL.md`, `tools/`).

Axes: (1) duplicate-phrase / run-together / duplicate-parenthetical residue in touched sections; (2) every **new** citation resolves to a receipt that establishes its clause; (3) no overstated target.

## Commands

```bash
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff \
  59c38109bf119d0e9d4f878644a82babc937bc1e 99c3bc88d704566197783f66b211ee0a830e0330 \
  -- SKILL.md tools/
# then per citation: git show 99c3bc88…:<path> | sed -n '<lo>,<hi>p'
```

Receipts: `.ufo/waves/round-54/w2/T54W2RevFix06-receipts/{c0-c1.diff,hunk-headers.txt,quality104-scan.txt}`.

Diff shape: `SKILL.md` 18 hunks; `tools/env-diff.py` +3 lines (`ScratchRootUnusable` on the non-selftest path). No other `tools/` edits.

## Verdict

QUALITY 104 does **not** clear cleanly. Two actionable findings (below). Duplicate-parenthetical scan over the +lines of the fix pass: **zero** exact `(same)(same)` debris of the round-53 falsifier shape. Citation re-pins for refusal-table / porcelain / cadence / operator-runbook / SOURCES / pin-disposition / mutate ranges / bash-witness PIN lines: **hold** at C1 under `sed -n`.

## Findings (by severity)

### 1. medium — run-together residue left in the same paragraph the fix re-spaced

**Where:** `SKILL.md:1728-1730` (hunk `@@ -1728,7 +1728,7 @@`, section `## Context gate classification and explicit exit classes — round 15`).

**Quote (C1):**

```
Could-not-evaluate takes precedence over a mismatched expected verdict: an
edited snapshot or unavailable input stays exit2, with any expectation
disagreement secondary. A clean result with a wrong id/exit pin becomes
failed/exit1. Help exits0 only as a non-verdict informational mode; context-capture's selftest
exits 0/1/2 for pass/case failure/could-not-evaluate (setup inability) and 64 for invalid invocation …
```

**Why:** The hunk fixed `exits0/1/2` → `exits 0/1/2` and `and64` → `and 64` on line 1731, then stopped. The immediately preceding prose still carries the same QUALITY 104 class (`exit2`, `exit1`, `exits0`). Criterion 104's check is a scan over the **touched section** listing zero hits; a re-read of this hunk before commit would have caught the glued tokens on 1728–1730 next to the spaced clause on 1731.

**Proof:**

```bash
git -C … show 99c3bc88…:SKILL.md | sed -n '1727,1731p'
# hits: exit2 (1728), exit1 (1730), exits0 (1730); clean spacing only on 1731
```

### 2. medium — new citation overstates the scrub clause

**Where:** `SKILL.md:1852` (hunk `@@ -1849,8 +1849,8 @@`, waiver-rev row).

**Quote (C1):**

```
… the tool sets `GIT_NO_REPLACE_OBJECTS=1`, `GIT_GRAFT_FILE=/dev/null` and scrubs inherited `GIT_*` (`tools/evidence-disposition.py:385-395`; …)
```

**Why:** At C1, `:385-395` is only the G4 comment + `GIT_ENV_OVERRIDES` dict (establishes the two assignments). The actual scrub — `env = {k:v for … if not key.startswith("GIT_")}` — is `git_environment()` at **`:406-408`**, outside the cited range. `evidence-disposition.py` is byte-identical at C0 and C1 (`0588ae2f0aa3`); the re-pin moved the window onto the dict but still does not establish "scrubs inherited `GIT_*`". QUALITY 104: a citation whose receipt does not establish its clause.

**Proof:**

```bash
git -C … show 99c3bc88…:tools/evidence-disposition.py | sed -n '385,409p'
# 390-395: GIT_ENV_OVERRIDES; 406-408: startswith("GIT_") scrub — outside :385-395
```

## Hunk-by-hunk (file:line = C1 new-side)

| Hunk (C1) | Change | QUALITY 104 / citation | Severity |
|---|---|---|---|
| `SKILL.md:31-42` | Scratch-root three-arms prose; S278:163-165 / S279 | Assimilation `S278-tempfile.py:163-165` is the `if dirname: dirlist.append` skip; contract cites match. No dup-paren. | clean |
| `SKILL.md:158-164` | Add `size` to pin record | No new citation. | clean |
| `SKILL.md:170-176` | `one per class` → `at least one per class` + JS/bash pair note | Bare `:47-48` / `:70-71` are the same pairs as `mutation-case-kimi-census.md:47-48` / `mutation-case-kagi-census.md:70-71` (table at `:309`). No dup-paren of the round-53 shape. | clean (resolved via same-page table) |
| `SKILL.md:872-882` | Re-pin `SKILL.md:808-809`→`:819-820`; `:335`→`:346-347` | `:819-820` porcelain-clean sibling; `:346-347` bands-as-report. | clean |
| `SKILL.md:949-955` | `Exits0/1/2` → `Exits 0/1/2` | Exactly the run-together class; fixed. | clean |
| `SKILL.md:958-964` | `C**` → `` `59c38109` (round 54) ``; keep `:1247-1317,1459-1517` | Ranges still the pin-mismatch refuse / ten-leg status tally on `mutate-and-run.sh` at C1 (=C0 blob). | clean |
| `SKILL.md:967-973` | Round-52 skip-count bracket rewritten | Removes the overstated "no leg skips" reading; cites `:78-79` (report fields). No new dup-paren. | clean |
| `SKILL.md:1266-1272` | Cadence span `:1010-1154`→`:1023-1169` | Lands on `## The re-sweep cadence…` through end of that block. | clean |
| `SKILL.md:1279-1289` | Refusal b/c/f anchors shifted | `:824-828` hermetic suite; `:851-855` SETUP/exit 2; `:834-836` never edit/re-pin; `:890-892` sensitivity≠truth. | clean |
| `SKILL.md:1303-1310` | operator-runbook pin `e1e349b6…`/511 L → `8b2e185f…`/516 L/33515 B at `59c38109` | `sha256sum` of blob = `8b2e185f…`; 516 lines / 33515 bytes; same blob at C0 and C1. | clean |
| `SKILL.md:1316-1322` | Divergence rule `:1250-1254`→`:1276-1277` | "divergence … is the finding, never smoothed". | clean |
| `SKILL.md:1503-1509` | `SOURCES.md:500`→`:503` | Round-48 line naming S265 superseding S026. | clean |
| `SKILL.md:1548-1554` | `unchanged` now requires pin verify (`pin-disposition.py:67-71`, `:563-567`) | `:67-71` defines verified-pin requirement; `:563-567` `pin_not_verified` → unavailable. | clean |
| `SKILL.md:1603-1611` | Clarify twelve expected / thirteen inputs belong to round-13 `expected.json` | No broken cite. | clean |
| `SKILL.md:1728-1734` | Exit-arm / disposition selftest rewrite (round 54) | **Finding 1** — spaced the edited clause, left `exit2`/`exit1`/`exits0` above it. | **medium** |
| `SKILL.md:1849-1856` | Re-pin evidence-disposition ranges after helper growth | Anchor/selftest/docstring pins (`:479-544`, `:2910-2915`, `:2275`) hold. **Finding 2** — `:385-395` misses scrub at `:406-408`. | **medium** |
| `SKILL.md:1876-1882` | pin-disposition registry cell + unusable TMPDIR exit 2 | `--selftest` path catches `ScratchRootUnusable` and prints the value (`:1396-1400`); matches clause. | clean |
| `SKILL.md:1955-1964` | bash-witness PIN/REV parse + `lessonround19` → `` `corpus/lessons/round-19.md` `` | `mutate-and-run.sh:616-617` = `275d8294…` / `fecee874…`; dispositions.json historical rev `4acc607…` for the tool. Run-together `lessonround19` fixed. | clean |
| `tools/env-diff.py:260-268` | `except ScratchRootUnusable` on main path | Mirrors existing selftest handler; exit 2, names value, no traceback. No SKILL cite in hunk. | clean |

## Residual risk / verification gaps

- Section-wide scan of `## Context gate…` also sees compact `exit0`/`exit1`/`exit2` table cells higher in the section (e.g. `:1688-1691`); those are pre-existing table idiom, not introduced by this hunk. Finding 1 is scoped to the prose immediately adjacent to the fix-pass edit.
- No LSP server used (markdown/shell); all anchors checked with `git show` + `sed -n` at C1.
- Did not re-run frozen C1/C2 counters (out of seat scope — attack seats own those instruments).

## Tools installed

None.
