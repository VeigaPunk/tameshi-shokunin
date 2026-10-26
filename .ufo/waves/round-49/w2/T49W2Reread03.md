# T49W2Reread03 — C1 recipe semantic re-read

Reviewed candidate `f181a961ae44061af486f600e5ea257d2baf78f8` against the nine recipe rows (ordinals 18–26) in `reads.json`. All nine excerpts support the corresponding clauses. I found no unsupported row. Correction review: all four relevant SKILL edits are accurate; no meaning-changing error found. Full row-by-row result is in `T49W2Reread03.json`.

Commands and observed evidence (run from the lane path; each `show` names the candidate explicitly):

- Ordinal 18, clause `SKILL.md:195-196`: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f181a961ae44061af486f600e5ea257d2baf78f8:corpus/knowledge/mutation-case-kimi-census.md | nl -ba | sed -n '59,76p'` → line 59 names failing-case labels, and lines 61-76 enumerate exact labels/counts.
- Ordinal 19 and correction at `SKILL.md:197-199`: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f181a961ae44061af486f600e5ea257d2baf78f8:corpus/knowledge/mutation-case-kagi-census.md | nl -ba | sed -n '67p;82,103p'` → line 67 says `1/16` / FAIL; line 84 contains the exact bad-case example. Thus the corrected wording is supported, unlike the earlier unsupported `SELFTEST: FAIL (1/16 cases)` phrasing.
- Ordinal 20, clause `SKILL.md:200-204`: same Kagi `show` with `sed -n '88,91p'` → B4 `got exit=1`, exit still matched, and token assertion killed it.
- Ordinal 21, clause `SKILL.md:205-207`: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f181a961ae44061af486f600e5ea257d2baf78f8:corpus/knowledge/mutation-case-kimi-census.md | nl -ba | sed -n '43,53p'` → control and D2/D10 are 43/43 PASS; D2/D10 survived with zero failing cases.
- Ordinal 22 and correction at `SKILL.md:210-211`: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f181a961ae44061af486f600e5ea257d2baf78f8:tools/mutate-and-run.sh | nl -ba | sed -n '569,574p'` → percentage uses `total`; with inconclusives it emits DEGRADED and exits 1.
- Ordinal 23, clause `SKILL.md:212`: Kimi `show` with `sed -n '29,31p'` → 8/10, no inconclusives, 11 runs, 7.0 s.
- Ordinal 24, clause `SKILL.md:213`: Kagi `show` with `sed -n '50,53p'` → 8/10, 11 runs, 16-case suite count, 11.0 s.
- Ordinal 25, clause `SKILL.md:216-217`: Kimi `show` with `sed -n '82,99p'` → D2 pristine six ids/`+22 more`, mutant five/`+23 more`, both exit 1; D10 contrast at lines 98-99.
- Ordinal 26 and correction at `SKILL.md:221`: Kagi `show` with `sed -n '111,114p;118,122p;251,254p'` → B5 outcomes at 111-114, B10 `ok=1` vs `ok=0` at 118-122, and sensitivity expectation at 252-254 (251 is blank). Corrected range is right.
- Spacing-only denominator correction at `SKILL.md:193`: Kimi `show` lines 30-33 and Kagi `show` lines 50-53 support the denominators; only whitespace changed.

These are semantic reread findings only; no counter or deciding run was invoked.

## Summary
- Rows 18–26: 9/9 excerpts support their clauses.
- Corrections at SKILL.md lines 193, 198, 211, and 221: all accurate; no meaning-changing defect.
- No unsupported rows to report.
