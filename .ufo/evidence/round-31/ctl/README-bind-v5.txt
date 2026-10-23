Round 31 binding v5 — pre-data control receipts (L1 TameshiR31, before any wave-2 data seat).

Why v5: binding v4 (frozen c111dab5) was attacked before data by seats CtlBindV4Old (all 7 round-30
shapes + 5 controls killed, 0/32) and CtlBindV4New (5 of 9 NEW forged shapes kept 63/63: literal
heredoc, python -c script argument, false && branch, uncalled function, quoted ';' argument), and
reviewed by ReviewBindV4 (FA-1..FA-8). v4 was redesigned before data into v5
(.ufo/evidence/round-31/coldread/bind-select-v5.py, sha256 8760ddc9014af73a20dc95627528b845af75c9539c780fa509fba2c9b2e61338).

Re-scoring (the seats' own harnesses, copied to the L1 scratch; only the binder path and expected
sha were changed; the output labels still say "v4_kept", which here is v5):
- bind-v5-real-r30.stdout: 63 real round-30 wave-C entries, kept 63/63 (no false reject).
- bind-v5-new-shapes.stdout: CtlBindV4New's 9 shapes, all killed (pristine and restored 63/63).
- bind-v5-old-controls.stdout / bind-v5-old-shapes.stdout: CtlBindV4Old's 5 controls and 7 shapes, all 0/32.
Harness copies: harness/probe-bind-new-shapes-for-v5.py (seat CtlBindV4New's probe),
harness/probe-bind-old-shapes-for-v5.py + harness/probe-bind-v3-copied.py (seat CtlBindV4Old's probe).
They need the seats' scratch fixtures (transcript copies) to re-run; the receipts here are the record.
Not covered (ReviewBindV4 FA-4, FA-7, FA-8 and its false-reject list): spaced fd-dup syntax errors,
mid-word '#', vacuous expansion-token argv matching, and every launch path outside the wrapper list.
General reachability and execution cannot be proven from transcript text; a hand-forged call and
result pair stays beyond any transcript binding.
