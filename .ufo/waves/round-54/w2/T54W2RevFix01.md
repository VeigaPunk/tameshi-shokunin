# T54W2RevFix01 — C1 fix-pass verify (cats 1–6 anchors)

Seat: `T54W2RevFix01` (wave 2, Godspeed)
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
C0: `59c38109bf119d0e9d4f878644a82babc937bc1e`
C1: `99c3bc88d704566197783f66b211ee0a830e0330`
Scope: anchor fixes in `### The boundaries`, `### Using the ledger`, `### The service's limits` (listed pins `:346-347`, `:819-820`, `:824-828`, `:834-836`, `:851-855`, `:875`, `:890-892`, `:952`, `:961`, `:970`).

## Axes

1. Citation accuracy — every re-pin resolves at C1 to the claimed bytes.
2. No overstatement — target text supports the citing sentence.
3. QUALITY 104 — no run-together token, missing space, or duplicate parenthetical introduced by the hunk.
4. Pin freshness — a moved line count is accompanied by a re-pin (not a silent drift).

## Method

```bash
export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2RevFix01
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  diff 59c38109bf119d0e9d4f878644a82babc937bc1e 99c3bc88d704566197783f66b211ee0a830e0330 \
  -- SKILL.md tools/
git -C … show 99c3bc88d704566197783f66b211ee0a830e0330:SKILL.md | sed -n '<lo>,<hi>p'
git -C … show 99c3bc88d704566197783f66b211ee0a830e0330:tools/mutate-and-run.sh | sed -n '<lo>,<hi>p'
```

`tools/mutate-and-run.sh` is byte-identical C0→C1 (`diff` empty). `tools/` only changes `tools/env-diff.py` (+3 ScratchRootUnusable arm) — outside the listed cats 1–6 line set; noted, not scored here.

## Hunk-by-hunk

### H1 — `### The boundaries` / SKILL.md:875 — Read-only cite `:808-809` → `:819-820`

- **Severity:** none (fix holds).
- **C1 quote:** `porcelain-clean is an opt-in precondition at open (SKILL.md:819-820)`.
- **`sed -n '819,820p'` at C1:** `1. **A pinned revision** — … and a porcelain-clean sibling tree at open.`
- **Verdict:** C0 `:808-809` pointed at the fleet-census intro; C1 re-pin lands on the porcelain-clean sentence. No overstatement.

### H2 — `### The boundaries` / SKILL.md:879 — Findings cite `:335` → `:346-347`

- **Severity:** none.
- **C1 quote:** `a low kill rate is a report, not a service failure (SKILL.md:346-347)`.
- **`sed -n '346,347p'` at C1:** `**Bands are a report convention, not a pass/fail gate.** An 8/10 admits, and so / does a <50 % — with the gap recorded in the table, not softened`.
- **Verdict:** Supports the claim. C0 `:335` was boundary-reading prose, not the report-convention rule.

### H3 — `### The service's limits` refusal **b** — `:813-817`; `:840-844` → `:824-828`; `:851-855`

- **Severity:** none.
- **C1 table cell:** `` `:824-828`; `:851-855` ``.
- **`sed -n '824,828p'`:** one-command hermetic suite requirement (matches refusal name).
- **`sed -n '851,855p'`:** `MUTATE: SETUP (<reason>)`, exit 2 — no headline; red control exits 2 (matches meaning).
- **Verdict:** C0 pins hit contract intro / harness bash fence; C1 pins match both columns. No overstatement.

### H4 — refusal **c** — `:823-825` → `:834-836`

- **Severity:** none.
- **C1 meaning:** `a recommendation, never an edit — the service never edits, repairs or re-pins a gate`.
- **`sed -n '834,836p'`:** `Nothing else. The service never edits, repairs or re-pins the gate; a needed change is a recommendation to the owner…`.
- **Verdict:** Anchor matches the meaning column. C0 `:823-825` mixed the moved-substrate clause with the start of the hermetic-suite item (refusal **b**). Title phrase “moved substrate” still lives at `:823`; the meaning column does not rely on that line. Not an overstatement of `:834-836`.

### H5 — refusal **f** — `:879-881` → `:890-892`

- **Severity:** none.
- **C1 cell:** `` `:890-892`; `fleet-kill-rate-ledger.md:156-158` ``.
- **`sed -n '890,892p'`:** `**Sensitivity, not truth** — … never whether the gate's verdicts are right`.
- **Ledger `:156-158`:** `suite sensitivity ≠ gate truth (nothing here measures whether a gate's verdicts about the real world are right)`.
- **Verdict:** C0 `:879-881` was the Findings-kept / Mado 40 % bullet. C1 pin is the sensitivity bullet. External ledger cite still holds.

### H6 — `### Using the ledger` / SKILL.md:952 — `Exits0/1/2` → `Exits 0/1/2`

- **Severity:** none.
- **QUALITY 104:** missing-space run-together repaired.
- **Unchanged tool cites `:139-143,1519-1548`:** exit map 0/1/2 and `exit 1` / `exit 2` / `exit 0` arms still at those lines (tool unchanged C0→C1).

### H7 — SKILL.md:961 — `C**` → `` `59c38109` (round 54) ``

- **Severity:** none.
- **C1 quote:** `tool lines re-verified at `59c38109` (round 54)`.
- **`59c38109` →** `59c38109bf119d0e9d4f878644a82babc937bc1e` (resolves).
- **Ranges `:1247-1317,1459-1517`:** per-leg SETUP `return 2` then ten sequential `regression_case_git` + status aggregate — supports “later legs still run and their statuses aggregate”. Tool identical at C1, so the C0 re-verify pin remains true for the shipping blob.

### H8 — SKILL.md:970 — round-52 skip parenthetical rewrite

- **Severity:** none.
- **C1:** replaces `no leg skips — host-gated branches run sandboxed` with `the ten legs report no skipped case on this host; the kagi leg's own table is the one that records two, as the bracket above says`.
- **Consistency:** bracket’s bash-surface-census 14+2 skipped is the kagi leg; paren names that table. No duplicate parenthetical; no contradiction with `tools/mutate-and-run.sh:78-79` (DONE/SETUP report shape).

## Findings

None. Every listed cats 1–6 re-pin resolves at C1, matches its citing claim, and introduces no QUALITY-104 defect. Empty findings list is the credit path for this seat.

## Residual risk / verification gaps

- Refusal **c** title (“moved substrate”) is not itself line-cited after the re-pin; only the meaning column is. Acceptable under the stated overstatement test; a title-pin of `:823` would be belt-and-braces, not a defect.
- `tools/env-diff.py` ScratchRootUnusable arm is in the C0→C1 diff but outside this seat’s listed line set; not re-audited here.
- No tool install this seat.

## Artifacts opened

- `SKILL.md` at C0 and C1 (via `git show`)
- `tools/mutate-and-run.sh` at C0 and C1
- `tools/env-diff.py` C0→C1 diff
- `corpus/knowledge/fleet-kill-rate-ledger.md` at C1 (`:156-158`)
- `corpus/knowledge/mutation-case-mado-verify.md` at C1 (`:229-230`)
