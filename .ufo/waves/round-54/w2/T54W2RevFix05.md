# T54W2RevFix05 — C1 fix-pass review: `tools/env-diff.py` run-path mapping

Seat: T54W2RevFix05 (FSD reviewer). Cand: C1 `99c3bc88d704566197783f66b211ee0a830e0330` vs C0 `59c38109bf119d0e9d4f878644a82babc937bc1e`.
Item: verify the C1 `ScratchRootUnusable` catch added on the `--contract` path before the `(OSError, ValueError, KeyError, TypeError)` tuple; then check every C0→C1 hunk under `SKILL.md` + `tools/` by hand with `sed -n` at C1.
Judged on: calibration, depth. Milestone: verify the C1 fix pass.
Lane: read-only. Scratch: `/fast/scratch/hyaku/tameshi-r54/T54W2RevFix05/` (trap-cleaned). Tool installs: none. Census: `sources-census.sh validate --root … tameshi` → 0.
Receipts: `.ufo/waves/round-54/w2/T54W2RevFix05-receipts/`.

Diff under review:

```text
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff \
  59c38109bf119d0e9d4f878644a82babc937bc1e 99c3bc88d704566197783f66b211ee0a830e0330 \
  -- SKILL.md tools/
# SKILL.md | 60
# tools/env-diff.py | 3 +++
# 2 files changed, 33 insertions(+), 30 deletions(-)
```

Only production tool edit at C1 is `tools/env-diff.py` (+3). All other hunks are SKILL re-pins / QUALITY fixes.

---

## Findings (by severity)

### Medium — SKILL.md:1853 re-pin `:385-395` overstates the scrub

**File:** `SKILL.md:1853` citing `tools/evidence-disposition.py:385-395`.

**Quote (C1):**

> the tool sets `GIT_NO_REPLACE_OBJECTS=1`, `GIT_GRAFT_FILE=/dev/null` and scrubs inherited `GIT_*` (`tools/evidence-disposition.py:385-395`; …)

**Why:** `sed -n '385,395p'` at C1 is only the section banner + `GIT_ENV_OVERRIDES` dict (the two named keys plus `GIT_CONFIG_*`). The actual scrub — drop every inherited `GIT_*` key — is `git_environment()` at `:406-409`:

```text
$ git -C … show 99c3bc88…:tools/evidence-disposition.py | sed -n '406,409p'
def git_environment():
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update(GIT_ENV_OVERRIDES)
    return env
```

C1 correctly moved the stale C0 cite off `read_dispositions` (`:368-…`) onto the overrides block, but the new range still does not contain the scrub the sentence asserts. A reader who opens only `:385-395` cannot see inherited-`GIT_*` removal.

**Receipts:** `T54W2RevFix05-receipts/evidence-385-395.txt`, `evidence-406-409-scrub.txt`, `hunk-anchor-checks.txt`.

---

## Hunk-by-hunk (file:line, severity)

### H0 — `tools/env-diff.py:263-265` (the assigned fix) — PASS

```diff
+    except ScratchRootUnusable as exc:
+        print("ENVDIFF_SETUP: could-not-evaluate: %s" % exc, file=sys.stderr)
+        return 2
     except (OSError, ValueError, KeyError, TypeError) as exc:
```

| Check | Result |
|---|---|
| Placement before the broad tuple | Yes (`:263` then `:266`) |
| `isinstance(ScratchRootUnusable, (OSError, ValueError, KeyError, TypeError))` | False — cannot be swallowed into the wrong class |
| `--selftest` unusable still exit 2, names TMPDIR, no traceback | EXIT 2; `ENVDIFF_SETUP: could-not-evaluate: … '…/missing-dir-xyz'` |
| `--contract` unusable at C0 | EXIT 1 + full traceback (`c0-contract-unusable.stderr`) |
| `--contract` unusable at C1 | EXIT 2 + one naming line, empty stdout (`c1-contract-unusable.stderr`) |
| `--contract` empty `TMPDIR=""` at C1 | EXIT 0; `ENVDIFF: classified=1/1` |
| Class docstring `:32-33` "never a traceback" | Now holds on both entry paths |
| Raise sites | Single raise at `:45`; only caller `execute` `:80`; reached from selftest and from `surface_result`→`probe`→`execute` |

Minimal-contract probe (scratch clone at C1, one bash surface, unusable TMPDIR):

```text
ENVDIFF_SETUP: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/fast/scratch/hyaku/tameshi-r54/T54W2RevFix05/usable-root/missing-dir-xyz' (could-not-evaluate)
C1_CONTRACT_UNUSABLE EXIT:2
```

Same argv at C0 ends in `ScratchRootUnusable: …` traceback, EXIT:1. Wave-1 F1 / Rev01 medium finding is closed by this hunk.

### H1 — `SKILL.md:31-40` Standing rules / three arms — PASS

Rephrases empty-arm rationale; keeps S278:163-165 (CPython `_candidate_tempdir_list` per `corpus/SOURCES.md` S278 locator) and S279; scopes measurement to `--selftest`/`selftest` and names the C2 counter blind spot. No overclaim relative to the env-diff run-path fix (behavior claim holds; measurement scope stays honest). No duplicate parenthetical.

### H2 — `SKILL.md:158` pin-artifact size word — PASS

Adds the missing `size,` token. No cite drift.

### H3 — `SKILL.md:170` defect-list wording — PASS

QUALITY clarification (`at least one per class` + exemplar pairs). No new line-range cite that fails.

### H4 — `SKILL.md:872-880` mado read-only / survivor cites — PASS

Re-pin `SKILL.md:808-809`→`:819-820` (porcelain-clean open precondition) and `:335`→`:346-347` (bands are a report). Both land on the named claims (`sed -n` in receipts).

### H5 — `SKILL.md:949-952` `Exits0/1/2` → `Exits 0/1/2` — PASS

QUALITY 104 spacing only. Adjacent `:139-143,1519-1548` still name the PASS/FAIL/SETUP map and the exit sites in `tools/mutate-and-run.sh`.

### H6 — `SKILL.md:958-961` `C**` → `` `59c38109` `` — PASS

Placeholder replaced with a real short hash; aggregate ranges `:1247-1317,1459-1517` still sit on the ten-leg runner materialization / dispatch block.

### H7 — `SKILL.md:967-970` contribution-contract round-52 bracket — PASS

Replaces the overstated "no leg skips" host claim with "ten legs report no skipped case on this host; the kagi leg's own table is the one that records two, as the bracket above says". Cross-reference, not a QUALITY-104 duplicate parenthetical. Cite `tools/mutate-and-run.sh:78-79` unchanged and correct.

### H8 — `SKILL.md:1266-1269` cadence range — PASS

`:1010-1154`→`:1023-1169` lands on `## The re-sweep cadence…`. Ledger cites `:285`/`:318` unchanged and still name ER-3/ER-4.

### H9 — `SKILL.md:1279-1289` refusal-table anchors — PASS

| Cell | New cite | Target at C1 |
|---|---|---|
| b | `:824-828`; `:851-855` | hermetic-suite requirement; spec-parse SETUP |
| c | `:834-836` | service never edits/re-pins |
| f | `:890-892` | sensitivity ≠ truth |

All four resolve; no duplicate parenthetical.

### H10 — `SKILL.md:1303-1306` (nearby refusal/cadence edit in same region) — PASS

Checked with the refusal-table pass; no stale line left behind in the edited rows.

### H11 — `SKILL.md:1316-1319` runbook pointer — PASS

`:1250-1254`→`:1276-1277`. New lines are exactly the rendering/divergence rule applied to `service-limits.md`. (C0 cite was already off the divergence text; C1 corrects it.)

### H12 — `SKILL.md:1503` SOURCES supersession — PASS

`:500`→`:503`; C1 line 503 is the Round 48 / S265 supersession note.

### H13 — `SKILL.md:1548-1551` pin-disposition unchanged cell — PASS

Adds `tools/pin-disposition.py:67-71` (unchanged semantics docstring) and bare `:563-567` (same-file convention) on the `pin_not_verified` → `content_status = "unavailable"` branch. Both support "AND the pin verifies against the manifest digest".

### H14 — `SKILL.md:1603-1609` context-capture exit arms — PASS

QUALITY spacing (`exits 0/1/2` / `64`) plus round-54 could-not-evaluate wording for unusable scratch. No false cite.

### H15 — `SKILL.md:1728` (same family as H14 in the diff stream) — PASS

Aligned with the disposition/context-capture exit-class cleanup; no orphaned line pin.

### H16 — `SKILL.md:1849-1853` evidence-disposition re-pins — FAIL (see Finding)

| Cite | Verdict |
|---|---|
| `:479-544` `resolve_historical_anchor` | PASS — function is exactly that span |
| selftest `:2910-2915` / docstring `:2275` | PASS — case + "anchors at HEAD" |
| `:385-395` scrub claim | **FAIL** — overrides only; scrub is `:406-409` |

### H17 — `SKILL.md:1876` pin-disposition TMPDIR note — PASS

Adds self-test unusable → exit 2 naming line. Matches `tools/pin-disposition.py` (scratch only on selftest; catch at entry). Does not overclaim a non-existent run-path.

### H18 — `SKILL.md:1955-1960` bash-witness PIN/REV — PASS

`tools/mutate-and-run.sh:616-617` is exactly `PIN_BASH=275d8294…` / `REV_BASH=fecee874…` as the cell states; `4acc607` remains the dispositions `historical_inputs` rev (narrative, not a broken line pin).

---

## Residual risk / verification gaps

- C2 still measures self-tests only; this seat proved the `--contract` arm by hand, which is outside the frozen counter (as the standing-rules / scratch-root-contract blind spot already says).
- No LSP server in this seat's tool surface; line identity is from `git show` + `sed -n` / AST walk of `except` handlers, not semantic references.
- `execute` still short-circuits on missing `bwrap` before `strict_scratch_root`; host has `/usr/bin/bwrap`, and the contract probe hit the helper (same path Rev01 used).

## Verdict

**Env-diff run-path fix: closed.** C1 maps `ScratchRootUnusable` on the `--contract` path to exit 2 with a naming line; C0 traceback/exit 1 is gone; catch order cannot swallow the class into the OSError tuple; class docstring is no longer a lie on that path.

**One medium finding remains in the fix pass:** the evidence-disposition scrub cite at `SKILL.md:1853` was re-pinned to a range that still does not contain the scrub (`:406-409`). Every other SKILL/tools hunk either lands on the claim it names or is a defendable QUALITY-only edit.

## Commands run (absolute)

```text
mkdir -p /fast/scratch/hyaku/tameshi-r54/T54W2RevFix05
export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2RevFix05 HYAKU_SCRATCH=/fast/scratch/hyaku
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff \
  59c38109bf119d0e9d4f878644a82babc937bc1e 99c3bc88d704566197783f66b211ee0a830e0330 \
  -- SKILL.md tools/
git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin "$D/work"
# assert: git -C "$D/work" rev-parse --show-toplevel == "$D/work"
git -C "$D/work" checkout 99c3bc88d704566197783f66b211ee0a830e0330   # and again for C0 compare
TMPDIR=$UNUS python3 "$D/work/tools/env-diff.py" --contract … --out … --fleet-root … --jobs 1
TMPDIR=$UNUS python3 "$D/work/tools/env-diff.py" --selftest
TMPDIR= python3 "$D/work/tools/env-diff.py" --contract …   # empty arm
git -C … show 99c3bc88…:tools/env-diff.py | sed -n '263,268p'
git -C … show 99c3bc88…:tools/evidence-disposition.py | sed -n '385,395p'
git -C … show 99c3bc88…:tools/evidence-disposition.py | sed -n '406,409p'
# + sed -n for every re-pinned cite listed above
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --root /home/vgpnk/Projects/shokunin tameshi
```

Artifacts opened: C0/C1 blobs of `tools/env-diff.py`, `SKILL.md`, `tools/evidence-disposition.py`, `tools/pin-disposition.py`, `tools/mutate-and-run.sh`, `corpus/SOURCES.md` (S278), `corpus/knowledge/scratch-root-contract.md`, `tools/registry.json` (`env-diff-selftest` scratch_root cell), wave-1 `T54W1Rev01.md` / `T54W1ExecExitClass.md` (context for the defect C1 claims to close — not used as evidence about C1 bytes).
