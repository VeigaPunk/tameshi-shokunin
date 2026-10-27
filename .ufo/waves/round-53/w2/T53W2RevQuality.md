# T53W2RevQuality — QUALITY-104 falsifier (wave-2 reviewer)

**Verdict: `QUALITY-104_FALSIFIER: PASS`** — base-shows / candidate-clean / zero un-fixed hits.

- Base: `6db1d220b337c35ff1e25bf9cfd74abc9db1498d` (SKILL.md sha256 `29b248ce932ac94e04fd16749ed4a6874b70fe8b6ebb0aafb4cf4da419658dcd`, 193791 B)
- Candidate: `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e` = C** (SKILL.md sha256 `4b4a05251208beb61b0ad70ff8f26fef42dd9d3187317c4286b06c42b06b3d6d`, 197139 B)
- All scanned bytes are `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show <rev>:<path>` objects; worktree never read for SKILL.md. Blob sha256 recomputed fresh during the run and bound to the reported digests.

## Checks run

1. **Base leg.** `git show 6db1d220:SKILL.md | grep -n` for both known patterns (plus encoding variants).
2. **Candidate leg.** Same greps at `5b703c6f`.
3. **Sectionize verification.** Frozen round-18 `sectionize` extracted from C** (`.ufo/evidence/round-18/measure.py`, the module the frozen C1 counter itself imports) run over the C** blob and compared — field-for-field (`start`, `end`, `heading`, `sha256`) — against an independent reimplementation of the wave-context split rule (`^#{1,3}(\s|$)` outside ```` ``` ```` fences, trailing blank lines stripped, `\n`-joined, surrogateescape, no trailing newline). **64/64 sections identical.**
4. **Duplicate-parenthetical scan.** The 21 re-fixed sections (heading list from `.ufo/waves/round-53/spec-w2.json`, T53W2Read01..21 — dispatch file, not committed at C**; only the heading list comes from it, all bytes are git objects). Detector: every adjacent `(...)` pair separated by whitespace only, inner normalized (`*` stripped, whitespace collapsed, casefolded) — flags equal inners. **Self-test on base bytes flags exactly the known pair** (`(**ten** since round 51)` `(ten since round 51)`), so the instrument is not vacuous.
5. **Auxiliary sweeps** (QUALITY-104 receipt class): immediate word repetitions, `/tmp/` mentions in the 21 sections — each hit classified, no un-verified zero.

## Leg results

**Pattern 1 — `(ten since round 51) (ten since round 51)`**

- Base: the duplicate-parenthetical exists at base line 1305 — `uncommitted worktree file at this write), \`--regression\` replays **six** in r10-2 (**ten** since round 51) (ten since round 51)`. The first instance is bolded (`**ten**`), so the literal form of the dispatch's quote does not byte-match; the normalized pattern and the class hit do. `since round 51` also occurs at base 925, 1384, 1390-1391 as single (non-duplicated) parentheticals.
- C**: `(**ten** since round 51) (ten since round 51)` — 0 hits; literal `(ten since round 51) (ten since round 51)` — 0 hits; all remaining `ten since round 51` occurrences (lines 1400, 1407) are single parentheticals in the map table. **Absent.**

**Pattern 2 — `still not embedded at this boundary (both are legs 5–6 since round 10-2`**

- Base: en-dash form present at base line 1227 — `read \`stale\`. Cases 5–6 were still not embedded at this boundary (both are legs 5–6 since round 10-2 — \`tools/mutate-and-run.sh:92-93\`): their rows carry no \`REGRESSION\``. ASCII-hyphen form (`legs 5-6 since round 10-2`) never existed at base.
- C**: `still not embedded` — **zero occurrences in the whole blob** (rc=1); `(both are legs` — zero. The section now carries the reworded "named debt" receipts (lines 1123, 1235, 1363, 1291). **Absent.**

**Duplicate-parenthetical scan over the 21 re-fixed sections at C** — zero adjacent duplicate parentheticals, zero known-pattern hits. 21/21 sections resolved uniquely (no missing, no ambiguous headings).

## Auxiliary classifications (all HOLD; none are un-fixed)

- **Doubled words, 22 raw hits, 0 defects.** All are `--flag PLACEHOLDER` invocation syntax in registry rows (e.g. `--rev REV`, `--tag TAG`, `--bundle BUNDLE.json`, `--expected EXPECTED.json`, `--pristine PRISTINE.py`, `--mutant MUTANT.py`, `--case CASE.json`, `--out OUT.json`, `--staged STAGED.md`, `--map MAP.json`, `--receipt RECEIPT.json`, `--spec SPEC.json`, `--config CONFIG.yml`, `--file FILE` — 18 in `### Round-26 gate/probe registry`, 2 in `### Round-17 gate/probe registry`), plus two pinned-sha columns (`175de6ba 175de6ba`, `fecee874 fecee874`, pin-vs-live table) in `### The tick and the pin read`. Not prose repetitions.
- **`/tmp/` inside the 21 sections, 9 hits, all dated receipts or tool-behavior descriptions:**
  - `:991` — `(negative run, \`/tmp/w7-tameshi-1/flip-run.out\` — [round 52: that volatile path is gone; the mechanism is corroborated at \`reports/r7-aud-t7.md\` §3 F4 and \`tools/mutate-and-run.sh:2010\`])` — bracketed as gone.
  - `:1045`, `:1072` — tick-executed instance `2026-10-14T19:15:14Z`, dated receipt.
  - `:1115` — `\`/tmp/w8-tameshi-t81/sweep/\` and \`/tmp/w8-t8-2-claims/work/\` — scratch paths long since reaped under the host scratch rule, named here as history only` — explicitly reaped.
  - `:1350` — `2026-10-14T21:02:39Z, tool \`75ed934d…\` before and after, scratch \`/tmp/w10-t10-4-ev/\`` — dated receipt.
  - `:1400` — `§7's default scratch still reads \`mktemp -d /tmp/…\` (\`corpus/knowledge/operator-runbook.md:349-351\`)` — pointer **verified at C**`: runbook :349-351 reads `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX, removed on PASS unless --keep`; the row correctly notes the runner honours TMPDIR and names the governing rule.
  - `:2178` (tally audit v2 row) — `the runtime sweep additionally removes the fixed literal /tmp/tally-audit-work whenever a PASS vector fires` — **verified against the tool at C**`: `tools/tally-audit-v2.py:265` encodes `('/tmp/tally-audit-work', '1', '0')` and :273 documents the runner's rm-on-PASS real default; the cell also states harness scratch is under TMPDIR (code: `mktemp -d "$TMPDIR/h.XXXXXX"` :514).
  - `:2179` (tally audit v3 row) — `one auto-root dir /tmp/tameshi-r4-2-regression.XXXXXX allocated to witness the runner shape and removed at exit` — **verified**: `tools/tally-audit-v3.py:408` builds the literal `/tmp/tameshi-r4-2-regression.<6alnum>` candidate to witness the runner's own auto-root, `atexit`-registers `shutil.rmtree` (:427).
- **`/tmp/` elsewhere in the blob (outside the 21; informational).** All classified, none current-directive violations: `:345` mutant copies (KB-scale, under the "/tmp only <50 MB" allowance, historical `<lane>-r<round>-<n>` shape); `:546`,`:602`,`:614` Appendix worked-example scratch (KB-scale); `:922`,`:1414`,`:1446` dated receipts; `:1785` reproduced-run recipe `mktemp -d /tmp/…` (KB-scale). The all-blob executor lint (T53W2ExecDupLint) has the full surface as its own item.

## Notes for calibration

- Base pattern-1 exists as the **bolded** variant `(**ten** since round 51) (ten since round 51)`; the dispatch's literal quote is the normalized form. Counted as "exists" (the defect being falsified is the duplicate parenthetical).
- Base pattern-2 exists only in **en-dash** form; the ASCII encoding quoted in the wave-2 spec never existed at base. Counted as "exists" via the en-dash line-1227 hit.
- The wave-1 QUALITY-104 labrat's receipt was not committed under `.ufo/waves/round-53/w1/` at C** (only `swarm-registry.json` exists there at that rev), so the scan instrument used here is self-contained and is shown effective by the base self-test.

## Instrument

- `q104-scan.py` (sha256 `19ff08cb8de2eeb51dc836dccc4f6902e81500b0ce23260bd21318b28c742703`): frozen-split verification + all legs above; output `q104-scan-result.json` (both lived in scratch, deleted after run per scratch discipline; content embedded above).
- Commands: `git -C <lane> show <rev>:SKILL.md | grep -n <pattern>`; `git show C**:.ufo/evidence/round-18/measure.py` (sectionize source); `git show C**:tools/tally-audit-{v2,v3}.py`; `git show C**:corpus/knowledge/operator-runbook.md`.

## Per-section result table (C**, frozen split)

| Seat | Section (lines) | dup parens | patterns | /tmp/ | 2x-words |
|---|---|---|---|---|---|
| T53W2Read01 | 1581–1614 | 0 | 0 | 0 | 0 |
| T53W2Read02 | 134–248 | 0 | 0 | 0 | 0 |
| T53W2Read03 | 1496–1515 | 0 | 0 | 0 | 0 |
| T53W2Read04 | 17–32 | 0 | 0 | 0 | 0 |
| T53W2Read05 | 924–937 | 0 | 0 | 0 | 0 |
| T53W2Read06 | 1287–1295 | 0 | 0 | 0 | 0 |
| T53W2Read07 | 1015–1025 | 0 | 0 | 0 | 0 |
| T53W2Read08 | 1516–1533 | 0 | 0 | 0 | 0 |
| T53W2Read09 | 970–1014 | 0 | 0 | 1 (bracketed-gone) | 0 |
| T53W2Read10 | 1565–1580 | 0 | 0 | 0 | 0 |
| T53W2Read11 | 1615–1626 | 0 | 0 | 0 | 0 |
| T53W2Read12 | 1694–1724 | 0 | 0 | 0 | 0 |
| T53W2Read13 | 1864–1872 | 0 | 0 | 0 | 2 (CLI syntax) |
| T53W2Read14 | 2150–2189 | 0 | 0 | 2 (tool-behavior, verified) | 18 (CLI syntax) |
| T53W2Read15 | 1098–1161 | 0 | 0 | 2 (reaped-history) | 0 |
| T53W2Read16 | 1396–1411 | 0 | 0 | 1 (verified pointer) | 0 |
| T53W2Read17 | 1237–1256 | 0 | 0 | 0 | 0 |
| T53W2Read18 | 1317–1380 | 0 | 0 | 1 (dated receipt) | 0 |
| T53W2Read19 | 1026–1074 | 0 | 0 | 2 (dated receipt) | 2 (pinned-sha cols) |
| T53W2Read20 | 938–969 | 0 | 0 | 0 | 0 |
| T53W2Read21 | 1465–1480 | 0 | 0 | 0 | 0 |

## Findings

None. PASS condition met: base shows both patterns, candidate is clean, zero un-fixed hits in the 21-section duplicate-parenthetical scan.

## Residual risk

- The falsifier certifies the absence of the *named* defect classes at C**. It does not re-verify every semantic claim in the 21 sections — that is the re-reader seats' item (T53W2Read01..21).
- `/tmp/` hits outside the 21 sections were classified only to support calibration; the full-blob lint is T53W2ExecDupLint's assignment.
