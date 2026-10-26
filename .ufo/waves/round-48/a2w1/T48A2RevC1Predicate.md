# T48A2RevC1Predicate — C1 predicate: contract vs code vs label

Seat: reviewer, round 48 attempt 2 wave 1 (leaf, no dispatch). Scope: the frozen C1 counter
`.ufo/evidence/round-48/calibration/measure.py` against `contract.json` claim C1 `statement`,
`predicate_label`, `kill_rule` and amendments 3-10. Read-only on the lane; nothing installed or
upgraded (no pacman/uv/npx/binary channel used — none needed); probes only. Scratch
`/fast/scratch/hyaku/tameshi-r48/T48A2RevC1Predicate` deleted before this report was finished.

Freeze identity verified before review:
- counter sha256 `572a5670deb7edb02f3a4e14f995a10110e6fbf63be37f63bd1981f6e90326f3` == freeze-2.json `counters["calibration/measure.py"].sha256`;
- statements pin `924102dfbc6135a7d9dabef7b8b2e681a5ce4c42ca72a031ea1f8d5ab9fb2e56` == freeze-2.json `statements_sha256` == the contract surface's pin.

Context: no attempt-1 predicate review landed — `T48RevC1Predicate` is in freeze-2.json
`pending_w1_seats_at_freeze` and no such report exists under `.ufo/waves/round-48/w1/`; this is
the first predicate review on record for round 48.

## Headline answer — the printed label makes the full condition visible

The contract's `predicate_label` string ("C1_R48_PASS=true iff self_pin=1 stmts_pin=1
statements=22 rounds=3 append_only=1 unpinned=0 total=0") is the pre-amendment label; amendments
4/5/7 extend the pass condition. The code's label implements and prints every extension:

- `measure.py:571` `total = mism + unparsed + unobs + depm + unpinned + unatt + over` — all seven
  statement terms.
- `measure.py:573-574` `passed = (self_pin == 1 and stmts_pin == 1 and len(statements) == n_expected
  and rounds == N_ROUNDS and append_only == 1 and total == 0 and fleet_drift == 0 and not only)`.
- `measure.py:575-581` the label prints, by name: `self_pin`, `stmts_pin`, `statements`, `rounds`,
  `append_only`, `unpinned`, `total`, `mismatches`, `unparsed`, `unobservable`, `dep_mismatch`,
  `unattested`, `oversize`, `attested_extra` (amendment 4), `fleet_drift` (amendment 5),
  `sibling_moves` (amendment 5), `base` (amendment 7), `rev`, `C1_R48_PASS`.
- `measure.py:572,578` probes (`--only`, `--rounds != 3`) print the `C1_R48_PARTIAL` prefix, so a
  probe receipt can never read as a deciding pass.

`unattested`/`oversize` need no separate predicate term (they are terms of `total`, printed both
summed and individually). `fleet_drift` is **not** a term of `total` (amendment 5: "Drift is never
counted as a mismatch"), so it had to be named — it is: required at `:574`, printed at `:577,580`.
No pass-condition input is invisible in the receipt.

## Conjunct → code map (C1.statement, amendment overrides noted)

| # | Conjunct | Code |
|---|---|---|
| 1 | "At REV" | rev resolved `:404-408`; all reads `git show <rev>:…` `:410,414,425-428,343-347`; clones detached at rev `:304-317` |
| 2 | "for each of the 22 frozen statements" | statements from the pinned statements.json at REV `:414-418`; loop `:496`; count guard `:573` (N_STATEMENTS=22 `:80`) |
| 3 | standing row = last data row of a table of its kind, first cell = id exactly, evidence carries `runs 3` | `last_rows :166-183` (kind `:172-177`, runs-3 filter `:179-181`, last-wins dict overwrite `:182`); lookup `:514`; amendment-6 mechanics: `strip_hidden :134-144`, `tables :147-158`, `cells_of :162-163` |
| 4 | V: one member `stable`; two or three `nondeterministic` | `parse_row :229-231` (`value = sorted(set(members))`, ok check), else `oversize :232-234` |
| 5 | declares tool sha256 prefix and deps D | `TAIL_RE :94-95`; `parse_deps :185-195` (`none` / sorted list over the five names; unsorted/dup/unknown → unparsed) |
| 6 | over R=3 rounds of the six profiles P0-P5 | rounds loop `:443-467`; PROFILES `:88`; `rounds == N_ROUNDS` guard `:573` |
| 7 | every observed P0 (line, exit) tuple ∈ V | `:526` |
| 8 | every member of V attested — ORIGINAL clause (committed observation receipts) superseded by amendment 4 | amendment-4 rule: `p1_seen :530`, `missing :531`, ≤6 extras `:532-536` (MAX_EXTRA=6 `:82`), extra tuple ∉ V → mismatch `:540-542`, `UNATTESTED :543-545`, `EXTRA` lines `:537-539`, `attested_extra` in label `:577,580`. Receipt reading has **no code** (load_attestations/attest_token removed per freeze-2.json) — but the docstring still claims it: **Finding 1** |
| 9 | tool sha256 prefix = pinned file at REV | `:526` (`claim['sha'] != pinned`); `pinned_prefix :343-347`, called `:515` |
| 10 | D ⊇ every dependence observed in all 3 rounds; D ∩ deps observed in none = ∅ | `required :510`, `never :512`, check `:549-552` |
| 11 | a dependence observed in some rounds only (`unstable`) may be declared or omitted | `unstable :513`, deliberately never checked against `declared` |
| 12 | per round, d observed when the variant tuple ≠ that round's P1 tuple (env: P0 ≠ P1) | dep_sets per round `:499-508` (env `:503-504`, variants `:505-507`) |
| 13 | profiles and variants are the round-47 counter's | constants `:85-89,96` ≡ r47 `:51-59`; `profile_env`/`setup_profile`/`pick_line` byte-identical to r47; `build_shim` refactor equivalent (sources list inlined); `observe` cosmetic only (ctx tuple, ternary); `dep_key`+`compare_part` ≡ r47 `comparable` (r47:234-240) |
| 14 | total = 7 terms = 0 | `:571`; passed `:574` |
| 15 | base SCORECARD.md stays a byte prefix | `append_only :429` (`rev_sc.startswith(base_sc)`); guard `:574` |
| 16 | counter, its selftest and the statements pin committed at REV | `self_pin :410-412` (the selftest is a `--selftest` mode of the same file, so one blob covers both); `stmts_pin :414` |

No conjunct lacks code (conjunct 8's original receipt clause is intentionally codeless — removed by
amendment 4 — and no code path implements it), and no code path lacks a conjunct/amendment basis:
fleet_drift/sibling_moves/FLEET lines (am 5), attested_extra/EXTRA/MAX_EXTRA (am 4), base pin
refusal + `base=` (am 7), `--work` under /tmp refusal (am 10), `C1_R48_PARTIAL` (kill rule/probe
discipline), `--jobs`/`scratch_root`/obs dumps (operational, docstring `:33-38,55-58`).

## total-term → computation

| term | computation |
|---|---|
| mismatches | `:526-528` (a round's P0 tuple ∉ V, or declared sha ≠ pinned) + `:540-542` (am 4: an extra tuple ∉ V) |
| unparsed | `:523-525` ← `parse_row` status `unparsed` (`:204-205` no tail; `:208-210` bad deps; `:212-216` axis score cell; `:218-227` cap arrow/body) and status `absent` (no standing row) `:519→523` |
| unobservable | `:516-518` (no P0 tuple in any round) |
| dep_mismatch | `:549-552` (`required ⊄ declared` or `never ∩ declared ≠ ∅`) |
| unpinned | `:494` (statement without `sha_file`) |
| unattested | `:543-545` (member in neither the P0 nor P1 round tuples nor ≤6 extras) |
| oversize | `:520-522` ← `parse_row :229-234` (count/class pairing, >3 members) |
| total | `:571` |

## Findings

### F1 (low — doc contradicts code) measure.py:48-50, with :11-13

The operational bullet defines `unattested` as "neither among this run's P0 tuples **nor recorded as
that statement's P0 tuple in a `PROFILES <id>: P0=<line>|<exit> ...` line of a committed file under
.ufo/evidence/round-48/calibration/observations/ at REV (read with `git show` at REV)**". Amendment
4 reversed exactly this ("Committed files under …observations/ are evidence for the report only,
never attestation") and freeze-2.json records "load_attestations/attest_token removed". The code
contains no receipt reading — the only remaining references are the docstring itself (`:12,50`) and
`OBSERVATIONS_DIR :79`, used solely by selftest T32 (`:745-746`), which asserts a committed
observation file does **not** attest. So the frozen artifact's own operational documentation
describes a code path that does not exist; a reader of measure.py alone would believe receipts
attest. Lines `:11-13` quote the superseded clause verbatim (faithful to the unamended
`contract.json` statement field, which was never rewritten) but the docstring nowhere notes
amendment 4's override. Doc-only; behavior and selftest are correct (T30/T32/T33a/T33f/T33/T33b all
pass). Fix: rewrite `:48-50` to the amendment-4 rule and annotate the quote at `:11-13`.

### F2 (low — amendment-3 grammar under-enforced) measure.py:218-227 with TAIL_RE :94-95

The amendment-3 cap evidence cell is `` `CMD` → `LINE1`, exit N1[…], tool sha256 `12 hex`, deps
`LIST`, runs 3 CLASS``. The code anchors only at the arrow (`:218-219`) and `TAIL_RE.search`
(`:204`) does not anchor the cell end, so:

- the leading `` `CMD` `` token is not enforced — probe: evidence
  `junk text no backtick cmd → `ALPHA: 3/3 pass`, exit 0, tool sha256 `aaaaaaaaaaaa`, deps `none`,
  runs 3 stable` parses `status=ok`;
- trailing text after `runs 3 CLASS` is accepted — probe: `… runs 3 stable JUNK trailing` parses
  `status=ok` (cap; axis variant too).

Inherited from the round-47 parser (r47 `CLAIM_CAP :54` is likewise arrow-anchored, prefix
unchecked). Severity low: the deciding rows are counter `--emit` output, which always writes
`` `cmd_text` → `` and nothing after CLASS (verified against the restated rows at the content
revision — sources-registry, six-leg regression ledger, calibration, freshness all well-formed),
and no contract control exercises these laxities; but the counter is the grammar's enforcer and
checks less than the grammar, so a hand-forged standing row (the CTL_B/C/D family is hand-forged)
that omits the command or appends junk still parses as valid.

### F3 (low — amendment-6 conformance, latent) measure.py:134-144

`strip_hidden` recognizes only ``` fences; amendment 6 says "tables inside fenced code blocks or
HTML comments are ignored". Probes (pure-function, scratch copy):

- a `runs 3` row inside a `~~~` fence **is picked as the standing row** (fence not recognized);
- a full table inside an **unclosed** `<!--` comment **is picked as the standing row** (the
  `<!--.*?-->` regex needs the closing delimiter); a closed comment hides correctly.

Latent only: the SCORECARD.md at the content revision c7586b9a contains 0 `~~~` lines and 0
`<!--`/`-->` (grep over `git show c7586b9a:SCORECARD.md`), so neither gap can fire in this round's
deciding run.

### F4 (trivial — wrong amendment cross-reference, introduced by the freeze edit) measure.py:370

`fleet_state`'s docstring says "(amendment 6)"; fleet/lane state is **amendment 5** (amendment 6 is
the table-of-its-kind rule). The line is new in the freeze edit — present verbatim in
`calibration/freeze-diff-vs-w1.patch` hunk `@@ -388,8 +366,31 @@`.

### F5 (trivial — wrong amendment cross-reference) measure.py:1012

The `--base` refusal prints "(amendment 8)"; the base pin is **amendment 7** (F5). Amendment 8 is
the one-deciding-invocation rule (F6). The refusal behavior itself is correct (exit 2, hard-coded
BASE `:83,1011-1013`; `base=` printed in the label `:577,580`).

## Observations (not defects)

1. `unpinned` sits outside the exclusive verdict chain (`:494` vs `:516-547`): a statement without
   `sha_file` could contribute twice to total (unpinned + its value verdict). Unreachable against
   the frozen file — all 22 statements carry `sha_file` (verified in statements.json) — and
   `stmts_pin :414` fails first if the file changes. Consistent with the docstring's exclusivity
   sentence (`:53-54`), which lists only the five value verdicts.
2. `dep_key :250-253` maps an unobservable result to `('UNOBSERVABLE', note)`: two profiles that
   both fail with different notes read as differing, so a dependence can be "observed" between two
   failing profiles. This is exactly round-47's `comparable` (r47:234-240), so conjunct 13 holds;
   semantics noted for the record.
3. `fleet_state :369-389` reads the census digest from the live fleet file (`:84,372-375`): a
   census script absent for the whole invocation yields `census='absent'` at every point →
   `fleet_drift=0` (`:470` requires >1 distinct digest). Conformant to the letter of amendment 5
   ("the census digest changes"); a fleet missing its census script is disclosed only via the FLEET
   lines (`:473-475`).
4. `attested_extra` (`:580`) prints `extra_used` (`:480`) — the number of extra observations
   **taken**, including ones that observed out-of-V or nothing. Amendment 4's "`attested_extra=<n>`"
   is ambiguous between "extras taken" and "members attested by extras"; the selftest is consistent
   with "taken" (T30/T51 expect 2 for 2 attesting extras; T32/T33f expect 6 for 6 non-attesting
   extras). A failed `setup_profile` extra (`:486-487`) also consumes one of the six.
5. The kill rule's "a deciding run taken at a revision other than the content revision" is enforced
   procedurally, not by the counter: the counter has no content-revision constant; it prints
   `rev=<sha>` (`:577,580`) and the deciding-run receipt pins the revision (deciding-run.sh step 4
   invokes the counter once at REV, no `--emit`/`--only`/`--rounds`, work under
   `/fast/scratch/hyaku/tameshi-r48/deciding/c1`, never /tmp). By design.
6. The restated rows at the content revision declare the six-leg ledger as
   `REGRESSION: PASS (cases=9 passed=9`, exit 0, deps `fleet-root,node`, runs 3 stable — the known
   ~10% SIGPIPE FAIL flake is deliberately not a member, so the predicate's kill rule ("a flaky
   deciding observation outside V is a mismatch, not a rerun") accepts that risk by design.

## What was run (probes only, per seat bounds)

- `python3 .ufo/evidence/round-48/calibration/measure.py --selftest` (TMPDIR under scratch) →
  `C1_R48_SELFTEST: cases=76 failed=0` / `VERDICT: PASS`, rc=0, 118 s, 76 PASS lines, no FAIL.
- sha256 checks: counter and statements pin equal freeze-2.json (values above).
- Pure-function probes on a scratch copy of the counter (`parse_row`/`last_rows`/`strip_hidden`/
  `dep_key`): the five probes behind Findings F2-F3 and Observation 2.
- Profile-machinery diff r47 vs r48 (`build_shim`/`profile_env`/`setup_profile`/`observe`/
  `pick_line` + constants): identical or equivalent.
- Freeze-diff review (`calibration/freeze-diff-vs-w1.patch`, 268 lines): confirms load_attestations
  removal, fleet_state/extra_observe additions, label extension, base pin; F4's wrong citation is
  in the added hunk.
- No tool installed or upgraded; no pacman transaction; no model passed; lane tree untouched
  (verified: nothing written outside this report file; a pre-existing `__pycache__` dated 07:23
  predates this seat and was left alone).

## Residual risk / verification gaps

- No live lane measurement was run (probes only, per bounds); the deciding run's outcome is the
  L1's to score, not this seat's.
- F2/F3 are latent for this round's tree (verified) but stay live for any future hand-authored row
  or future SCORECARD content using `~~~` fences or unbalanced comments.
- The selftest exercises `fleet_state` only through fakes (T33c/d/e); the real `fleet_state` ran
  only inside the deciding invocation, which this seat did not inspect beyond deciding-run.sh's
  invocation line.
