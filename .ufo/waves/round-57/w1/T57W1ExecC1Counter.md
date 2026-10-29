# T57W1ExecC1Counter - round-57 C1 successor counter (wave 1)

Staged (lane untouched): `.ufo/waves/round-57/w1/T57W1ExecC1Counter/stage/.ufo/evidence/round-57/c1/measure.py`
(641 lines, stdlib only, sha256 `936a520c31af5746ae8e5cf212c920db95d35f610c18e32de2a16f80c716fe85`, mode +x).
Install path in the lane: `.ufo/evidence/round-57/c1/measure.py`. Note: that path did not exist in the lane at start
(the brief's "read it" resolved to the round-50 counter, which is what this inherits).

## L1 ACTION REQUIRED before freeze
`DEFECTS_SHA256` is the explicit marker `PIN_PENDING_SET_BY_L1_AFTER_THE_EXTRACTOR_SEAT_STAGES_DEFECTS_JSON` (a miss, never a pass:
`defects_pin=1`). Set it to the sha256 of the final `defects.json`. The extractor seat's staged file is
`bef2293ba3db863b03247e9867b11aa2501aa54af0b098ce0f974817f485dee9` (51 items); if it is regenerated, re-pin. Editing the
constant changes `self=<sha12>`, so pin BEFORE freezing and re-run `--selftest` after (the selftest has a case that accepts
either a 64-hex pin or the PENDING marker, so it passes both ways). `BASE`, `OLD_COUNT=49`, floors are constants at the top.

## Verdict line (exactly the brief's)
`C1_R57: self=<sha12> rev=<rev12> rows=<have>/<N> agree=<n>/<N> old49=<ok|CHANGED> fixed=<n> declined=<n> thisround=<n> spot=<ok|DRIFT> total=<n> C1_R57_PASS=<true|false>`
Last stdout line; exit 0 pass / 1 miss / 2 setup. `--explain` adds EXPLAIN lines and a `C1_R57_TERMS:` line (per-term tally incl. open=)
before it. `--work`/TMPDIR honoured (selftest fixture and `tempfile`); no `/tmp` literal. Only `git show/cat-file/merge-base/diff-tree/rev-parse` on objects.

## What it checks
- Round-50 agreement rules kept verbatim (evidence resolves; key; fixed = post-routing commit touching a keyed path with an excerpt new at `routed_at` and no ACK words; open = id in newest `**Planned (round` paragraph; declined reason >= 40). Two deliberate edits: Planned-id regex `R4\d` -> `R5[0-6]\.\d+`; HARD list -> round-57 (c1/, control/, contract.json, freeze.json) + ledger + the set's spot-check files.
- Arm rows: one row per set id (`rows=have/N`; `missing`, `duplicate`, `extra`). Arm agree: rows with no fault.
- Arm old49: every row of the ledger at BASE (must be exactly 49 else setup error 2) present exactly once at REV and equal as canonical JSON (`sort_keys`; key/row order is not a change). Ids in the BASE ledger are never "extra"; a set id clashing with a BASE id is a setup error.
- Arm spot: every `corpus/lessons/round-5{0..6}-verifier-spotcheck.md` is in the set (else DRIFT) and sha256-equal at REV.
- Floors: fixed >= 20, declined <= 14, thisround (fixed commit not an ancestor of BASE) >= 6. BASE must be an ancestor of REV (else setup).
- Pin: sha256 of defects.json at REV == `DEFECTS_SHA256`.

## Evidence (receipts in `T57W1ExecC1Counter-receipts/`)
- `selftest.stdout`: `C1_R57_SELFTEST: 45/45 pass`. Arm liveness is asserted on the printed verdict line: rows `2/3`, agree `2/3`, old49 `CHANGED` (rewritten / deleted / duplicated old row), spot `DRIFT` (edited / deleted / absent from set), fixed floor, declined cap, thisround `0`, this-round floor, pin, plus HARD-path refusal per path (files exist and are keyed, so only the rule can refuse), older-round evidence path ALLOWED (narrowness), CLI exits 0/1/2.
- `mutants.stdout`: 27 hand mutants of the counter; first batch left 3 survivors (HARD rule, BASE-ancestor guard, count guard: fixture masked them), fixtures fixed (HARD files now exist; non-ancestor base now carries a valid ledger); the re-run killed all except `set(old) & set(ids)` guard, for which a case was added (now 44/45 under that mutant, killed). Final selftest 45/45 on the shipped file. Not re-run: the full 17-mutant batch against the final file after the last fixture edits (only the 10 + the clash mutant were re-run).
- `base-plus-defects-explain.stdout`: real lane clone at BASE + the extractor's staged defects.json committed on top (scratch clone, removed): `rows=0/51 agree=0/51 old49=ok ... spot=ok total=78 C1_R57_PASS=false` (77 with the correct pin; with the PENDING pin +1). 77 = 51 missing + fixed_short 20 + this_round_short 6: the expected "before" state; confirms the real 49-row BASE ledger and the 7 real spot-check hashes parse and match.
- `base-no-defects.stdout`: BASE with no defects.json: exit 2 (setup).

## Risks / things the L1 should know
- Row fault does not exclude the row from `fixed=`/`declined=` (round-50 behaviour: status counted before evidence checks); any fault already makes total>0.
- A rewrite of an old row's `evidence` text is CHANGED by design; the ledger header fields (`round`, `note`, `schema`) are not compared.
- Excluded evidence = only the set's seven spot-checks, not the older ten (spec "the spot-checks"); say if the older ten should be added.
- Not run: the counter against a real populated ledger (none exists until wave 2/3).
