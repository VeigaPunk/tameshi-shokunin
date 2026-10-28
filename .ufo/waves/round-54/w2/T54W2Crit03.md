# T54W2Crit03 — falsify the C1 fix pass (over-reach)

Axes: discernment, calibration.
Attack surface: C0 `59c38109bf119d0e9d4f878644a82babc937bc1e` → C1 `99c3bc88d704566197783f66b211ee0a830e0330` fix pass (`SKILL.md` 18 hunks + `tools/env-diff.py` ScratchRoot catch). Not the claim authors.

## Verdict

**Two rewritten sentences quietly changed the rule to fit the citation.** The other prose hunks are either line-anchor renumbers, lint, or honest corrections of SKILL text that was already false against the tool/census it cited. Receipts under `.ufo/waves/round-54/w2/T54W2Crit03-receipts/`.

| # | Sentence / cell | Same meaning? | Class |
|---|---|---|---|
| F1 | Recipe step 4: `one per class` → `at least one per class (… :47-48 …)` | **No** | **OVER-REACH** |
| F2 | Standing scratch-root: add `other modes are outside that measurement` | **No** (assurance narrowed) | **OVER-REACH** |
| F3 | Pin disposition `unchanged` row gains `AND the pin verifies…` | No | correction (tool already required it) |
| F4 | Disposition exit-arm: traceback/exit-1 → exit-2 never-traceback | No | correction (tool already exited 2) |
| F5 | `no leg skips — host-gated…` → host-qualified / kagi table | No | correction (kills same-sentence contradiction) |
| F6 | Pin record gains `size` | No (fields grow) | completion of step-9/census |
| F7 | bash-witness `4acc607`/dispositions → `PIN_BASH`/`REV_BASH` | No | correction of false provenance |
| F8 | empty arm `falls through … (S279)` → `documented list follows, S279` | Yes (arms unchanged) | provenance hygiene |
| — | Hunks 4–6, 8–12, 16 (line spans, `C**`, Exits spacing, runbook sha) | Yes / status fix | anchor or commit-state correction |

---

## F1 — OVER-REACH: `one per class` → `at least one per class`

### Command + output

```
$ git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 59c38109bf11:SKILL.md | nl -ba | sed -n '173,174p'
4. **Write the defect list from the templates.** 8–12 defects, one per class
   (catalog + entry template in the next section), each ONE exact-string

$ git -C … show 99c3bc88d704:SKILL.md | nl -ba | sed -n '173,174p'
4. **Write the defect list from the templates.** 8–12 defects, at least one per class (two of the JS ten share a class — the :47-48 pair — and the bash exemplar's :70-71 pair does the same)
   (catalog + entry template in the next section), each ONE exact-string

$ git -C … show 99c3bc88d704:corpus/knowledge/mutation-case-kimi-census.md | nl -ba | sed -n '44,48p'
    44	| D1 | off-by-one count | …
    45	| D2 | off-by-one count (findings cap) | …
    46	| D3 | inverted condition | …
    47	| D4 | dropped arm | …
    48	| D5 | dropped arm (presence gate) | …
```

Full receipt: `T54W2Crit03-receipts/F1-one-per-class.txt`, `C6-line-cite-accuracy.txt`.

### Why this changed meaning

- **C0 rule:** exclusivity — each defect is its own class (`one per class`).
- **C1 rule:** coverage floor that *blesses* sharing (`at least one per class` + explicit exemplar doubles).
- Read02’s defect was a contradiction between the rule and the cited exemplar (`:44-45` off-by-one **and** `:47-48` dropped arm; kagi `:70-71` dropped branch). The fix **rewrote the rule to match the exemplar** instead of keeping the rule and naming the doubles as debt.
- Extra calibration nick: the new text says “the `:47-48` pair” as *the* JS share; `:44-45` is the other share Read02 led with. `:47-48` is a real share (D4/D5), but the wording under-counts.

### Minimal wording that would not

> 8–12 defects, **one per class** (catalog + entry template in the next section) — the JS exemplar currently doubles off-by-one (`mutation-case-kimi-census.md:44-45`) and dropped arm (`:47-48`), and the bash exemplar doubles dropped branch (`mutation-case-kagi-census.md:70-71`); treat those doubles as named debt, not as the recipe.

---

## F2 — OVER-REACH: standing-rule measurement carve-out

### Command + output

```
$ git -C … show 59c38109bf11:SKILL.md | sed -n '37,42p'
  … never exit 1 (corpus/knowledge/scratch-root-contract.md; the
  seven tools and their registry `scratch_root` cells, measured by the round-54 C2
  counter).

$ git -C … show 99c3bc88d704:SKILL.md | sed -n '37,42p'
  1. Measured on each tool's `--selftest`/`selftest` path (round-54 C2 counter);
  other modes are outside that measurement (corpus/knowledge/scratch-root-contract.md;
  the seven registry `scratch_root` cells).

$ git -C … diff 59c38109bf11 99c3bc88d704 -- tools/env-diff.py
+    except ScratchRootUnusable as exc:
+        print("ENVDIFF_SETUP: could-not-evaluate: %s" % exc, file=sys.stderr)
+        return 2

$ rg -n "selftest" .ufo/evidence/round-54/c2/measure.py | head
# every tool invocation is `--selftest` / `selftest` (receipt B5 / F2)
```

Full receipt: `T54W2Crit03-receipts/F2-carveout.txt`, `C2-envdiff-scope.txt`, `B5-c2-scope.txt`.

### Why this changed meaning

- Read01: at C0, env-diff `--contract` raised `ScratchRootUnusable` outside the selftest catch (traceback / exit 1), so the universal three-arm sentence was false for that mode.
- C1 **fixed the tool** (contract-path catch → exit 2, naming, no traceback).
- C1 **also** inserted `other modes are outside that measurement` into the standing rule. That is not required once the tool maps the arm; it quietly narrows what the standing page vouchsafes, fitting C2’s selftest-only counter (`c2/measure.py` only runs selftests) instead of keeping the behavioural claim universal.
- Behavioural opener still says tools that call `strict_scratch_root()` honour the three arms; the new sentence teaches a cold reader that non-selftest modes are an admitted unmeasured hole.

### Minimal wording that would not

Keep the three-arm behavioural sentence. Append only:

> The round-54 C2 counter measures that class on each tool’s `--selftest`/`selftest` path.

Omit `other modes are outside that measurement`.

(The S279 soften from `falls through the documented list (S279)` → `the documented list follows, S279` is separate provenance hygiene and does **not** change the arms — F8.)

---

## Corrections that changed wording but are not over-reach

### F3 — pin disposition `unchanged` AND pin verifies

```
C0: | Recorded target bytes equal the current worktree | Report `unchanged` content |
C1: | Recorded target bytes equal the current worktree AND the pin verifies against the manifest digest (`tools/pin-disposition.py:67-71`, `:563-567`) | … |
$ git diff C0 C1 -- tools/pin-disposition.py   # empty
```

Tool docstring/code at C0 already required verified pin + byte equality for `unchanged` (`T54W2Crit03-receipts/B3-pin-tool.txt`, `F3-pin-correction.txt`). SKILL was understating the tool; C1 restates it. **Correction.**

### F4 — disposition / context-capture exit-arm

```
C0: … (the disposition selftest: 0 pass, 1 case failure or an uncaught setup traceback; round 17).
C1: … (the disposition selftest: 0 pass, 1 case failure, 2 could-not-evaluate — an unusable scratch root or an unreadable input is named, never a traceback; round 54).
$ TMPDIR=$BAD python3 tools/evidence-disposition.py --selftest   # at C1 clone
# stderr: could-not-evaluate: … TMPDIR is not a usable directory …
# EXIT:2 ; NO_TRACEBACK
```

Receipt `F4-exit-arm.txt` / `C3-disp-unusable.txt`. **Correction** of stale SKILL vs tool.

### F5 — contribution-contract skip parenthetical

Absolute `no leg skips — host-gated branches run sandboxed` → host-qualified + points at kagi’s own 2-skipped table. Removes the contradiction with the round-53 bracket in the same sentence. **Correction.**

### F6 — recipe step 2 adds `size`

Census pins already carry byte size; step 9 already compared size. C0 step 2 omitted the before-value. **Completion**, not a quiet semantic flip of the kind F1 is.

### F7 — bash-witness provenance

`4acc607` through dispositions.json → parses `PIN_BASH`/`REV_BASH` from `mutate-and-run.sh:616-617`. Read21: tool had zero refs to dispositions/4acc607/round-13. **Correction** of false provenance.

### F8 — S279 empty-arm attribution

Arms unchanged; causal “falls through (S279)” softened. Matches Crit04’s empty→skip is S278-only point. **Hygiene.**

---

## Sweep completeness

All 18 `SKILL.md` hunks classified in `T54W2Crit03-receipts/R-hunk-class.txt` and `01-hunk-inventory.txt`. Non-SKILL C1 edits (`QUALITY` 105 append, S275 `p.4`→`p.3 (physical)`, lesson dispositions, env-diff catch) inspected: S275 is a locator correction; QUALITY/lesson are append-only; env-diff is the tool half of F2.

## Smallest safe correction (for L1; this seat does not edit)

1. Revert step 4 to **one per class** and name the exemplar doubles as debt (F1 minimal wording).
2. Drop `other modes are outside that measurement` from the standing scratch-root bullet; keep a factual “C2 measures selftest paths” note only (F2 minimal wording).
3. Leave F3–F8 as landed.

## Artifacts opened / commands run

- `git diff 59c38109bf11 99c3bc88d704 -- SKILL.md tools/env-diff.py corpus/…`
- `git show` C0/C1 on `SKILL.md`, `mutation-case-kimi-census.md`, `mutation-case-kagi-census.md`, `tools/pin-disposition.py`, `tools/env-diff.py`, `tools/evidence-disposition.py`
- `.ufo/evidence/round-54/c2/measure.py`, `contract.json`
- Wave-1 `T54W1Read01.json`, `T54W1Read02.json` (driver findings only; not used as evidence of C1 bytes)
- Live: `git clone --shared` at C1; `TMPDIR=<absent> python3 tools/evidence-disposition.py --selftest` → exit 2, no traceback
- No pacman/uv installs this seat.

## Tooling

None installed. Host pacman paused; unused.
