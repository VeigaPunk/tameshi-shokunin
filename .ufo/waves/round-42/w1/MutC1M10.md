# C1 m10 mutation probe

Findings:
- Baseline `python3 /tmp/tameshi-r42-MutC1M10/m.py --selftest`: `C1_R42_SELFTEST: cases=9 failed=0`.
- Drop `theirs <= mine` coverage check (receipt_audit, source lines 211–213): killed; `SELFTEST T2_partial_supersede_still_counts FAIL`.
- Treat any `supersedes` as covering (remove `sup not in receipts` guard, source lines 202–204): survived; all 9 cases OK, `failed=0`.
- Compare `present` to `True` always (replace `repo.resolves(rep)` in source line 198): survived; all 9 cases OK, `failed=0`.

Restoration: each mutant was applied only to scratch m.py, restoring pristine bytes from the lane source before the next mutation. Final hashes matched: `9782a5a0e6404d2f305a51db085c7606914a2c381b35da7f7927c804df914c0e` (scratch and source). Scratch directory removed.
