# T58W1RevengerC2 — round-56 C2 admission failure, reconstructed; round-58 counter attacked

Item: reverse-engineer the round-56 C2 do-nothing failure, verify the round-58 counter reads no
claimant receipt, then run one novel forgery at it. Lane: `tameshi-shokunin`, measured tip
`0fdb71d26fab` (HEAD moved during the sweep; `2a32aa82` is an ancestor). Scratch:
`/fast/scratch/hyaku/tameshi-r58/T58W1RevengerC2/` (clone at base, fixture lanes, `attack.py`,
`claimant-repo`, `work-*`). Receipts: `.ufo/waves/round-58/w1/T58W1RevengerC2-receipts/`.
No lane file was edited; nothing installed; nothing staged (no fix is mine to land).

## 1. The round-56 failure, reconstructed

SCORECARD.md (round-56 section, line ~2727): the wave-2 do-nothing attack
(`w2/T56W2CritDoNothingC2.md`) reached `C2_R56_PASS=true` with **two 79-byte stub receipts** or a
borrowed round-54 receipt whose `rev=` token was rewritten. The frozen round-56 counter graded
committed receipt *files*: once the files existed and carried the right tokens, the counter's
selftest/doc/registry arms passed. The §9 no-op discriminator therefore failed — C2 was "reached
on the counter, not admitted as a measured improvement," and no post-data counter change was
allowed.

The failure class: **the counter trusted claimant-authored artifacts as the evidence of its own
target.** Producer and evidence were the same party.

## 2. Does the round-58 counter still read receipts? — No

Every file `.ufo/evidence/round-58/c2/measure.py` reads (full read, 811 lines):

| Path | How read | Claimant receipt? |
|---|---|---|
| `tools/receipt-revision-gate.py` | `git show REV:path` (measure.py:357) | no — gate source |
| `tools/registry-check.py` | `git show REV:path` (:358) | no — runner source |
| `tools/registry.json` | `git show REV:path` (:359) | no — row declarations |
| `SKILL.md` | `git show REV:path` (:360) | no |
| `.ufo/evidence/round-58/c2/mutants.json` | `git show REV:path`, sha256-pinned (:502) | no — frozen instrument |
| `__file__` + `mutants.json` beside it | `Path.read_bytes()` (:486, :641, :669) | no — counter self-hash and selftest only |

Live executions: `registry-check.py` (REV bytes, staged into `--work/bin`) runs each gate row via
`--root LANE --rev REV --only NAME` and re-runs them inside the mutant clone (:267-278, :401-438);
the cell arm builds its own scratch repo and **writes the only receipt the gate ever sees**
(:309-342). The three registry rows *do* name committed receipt fixtures
(`tools/fixtures/receipt-gate/{accept,drift}.receipt`), but those are gate *input*: the gate parses
only `rev=` tokens and verifies them against git objects (rev-parse + `diff --name-only` on the
declared `--paths` surface, gate :113-155). A stub or borrowed receipt certifies nothing the tree
doesn't already say. **The round-56 attack surface is closed at the receipt level.**

Honest baseline at tip (receipt `honest-run.txt`):

```
C2_R58: self=d4219039f02c rev=0fdb71d26fab gate_rows=3 exits=0,2,3 held=3/3 mutants=3/3
        skill_row=1 codes_known=4/4 standing_cell=ok total=0 C2_R58_PASS=true
```

(Note: `--work` must be **absolute**; a relative `--work` resolves `bin/registry-check.py` as
`work/work/bin/...` and every row reports `error rc=2`. Found during this sweep.)

## 3. Attack A — claimant fixture rows bypass the drift surface → CAUGHT by the mutants arm

Registry (claimant-authored): `c2-fx-ok` (exit 0), `c2-fx-absent` (exit 3, receipt
`fx/no-such.receipt` — absent file → `RECEIPT_MISSING`), `c2-fx-unresolvable` (exit 2). Real gate,
real registry-check (`attack-out.txt`):

```
executed c2-fx-absent expect=3 got=3 held          <- rows look honest
mutant M1 accept-on-drift: SURVIVED                <- drift branch never exercised
mutant M2 wrong-refusal-code: SURVIVED
mutant M3 exit-0-on-unresolvable: killed
total=2 C2_R58_PASS=false
```

The **mutants arm catches it**: a held-baseline row that never exercises the drift branch cannot
kill M1/M2. The executed arm alone is blind to the substitution.

A2 variant — row argv `--lane` points at a **fully absolute claimant repo** outside the fleet root
(`--lane`, `--paths`, `--receipt` all `/fast/scratch/...`): `_argv_outside_fleet`
(registry-check.py:632-645) only flags absolute tokens **under the live fleet root**, so the row is
not even marked non-hermetic. It **holds** and honestly kills mutants (the real gate ran against
claimant git objects) — `total=0 PASS=true` — yet its verdict was produced entirely by files that
never existed at REV. The `--rev` clone is cosmetic for that row. Provenance hole, secondary to B.

## 4. Attack B — forged `tools/registry-check.py` + cheat gate → **PASSES the counter**

The claimant ships its own oracle. `tools/registry-check.py` is target content (not frozen, not
pinned): replace it with a script that never executes any row — `held` when
`tools/receipt-revision-gate.py` is clean in the worktree, `differs` when the counter's mutant
write dirties it. The gate resolves `--certified` but never reads receipts; mutant anchors live in
a string literal plus real code; every `verdict`-role receipt is refused with
`RECEIPT_REV_CONTENT_DRIFT` (enough for the cell arm). Result (`attack-b-out.txt`):

```
mutant M1: killed by c2-fx-ok(got=1),c2-fx-drift(got=4),c2-fx-unresolvable(got=3)   <- forged
mutant M2: killed by ...                                                           <- forged
mutant M3: killed by ...                                                           <- forged
C2_R58: ... held=3/3 mutants=3/3 skill_row=1 codes_known=2/2 standing_cell=ok total=0 PASS=true
```

Control: the **same forged lane under the real registry-check.py**:

```
ROW c2-fx-ok expect=0 got=3 differs     <- the sham exposed instantly (held=1/3)
```

Neither the executed arm nor the mutants arm catches it — both are *produced by the forged
runner*. The counter sha256-pins `mutants.json` and recomputes truth by running the gate (cell
arm), but the two execution arms inherit `rc_raw = show(lane, rev, REGCHECK)` — the
artifact-under-test's own executor. The round-56 failure returns one level up: not a forged
receipt, a forged **executor**.

## 5. Reconstructed contract of the counter, divergences, confidence

- **Reads**: only git objects at REV + its own bytes — confirmed end to end (§2 table).
- **Trust root**: `tools/registry-check.py` at REV — **unverified claimant code** grading claimant
  rows and mutant kills. Confident divergence from the "nothing claimant-authored decides" intent.
- **Hermeticity**: `--rev` clones are bypassed by any absolute argv path outside the fleet mirror;
  unflagged. Confirmed live (`held`, `got=3`, gate output quoting the external repo).
- **What still works**: a forged *registry* alone cannot fake mutant kills (attack A); the cell arm
  and CODES pin catch stale SKILL cells and substring needles (selftest cases, T57W3CritContract
  B2 landed).

Recommendations (for the L1, not landed): execute each gate row's `argv` directly inside the
counter's own clone instead of trusting the lane's runner (or sha256-pin `registry-check.py` like
`mutants.json`); flag *any* absolute argv token unless `external` is declared; add a bent-runner
selftest fixture.

## Commands run

- `python3 .ufo/evidence/round-58/c2/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev HEAD --work <abs> --explain` → `total=0 PASS=true` (receipt `honest-run.txt`)
- `python3 tools/registry-check.py --root LANE --rev HEAD --only receipt-gate-accept` → `held` (manual sanity)
- `python3 attack.py` (driver: builds fixture lanes via the counter's own `build_lane`, runs `measure()`; receipts `attack-out.txt`, `attack-b-out.txt`)
- `python3 real-registry-check.py --root <forged-lane> --only <row>` → `c2-fx-ok differs` (sham gate exposed)
- `git clone --shared` + `checkout --detach 2a32aa82` in scratch; `git rev-parse --show-toplevel` asserted on every fixture dir before committing (`user.name=fixture`); never a mutating git call in the lane.

- `python3 .ufo/evidence/round-58/c2/measure.py --selftest --lane LANE --rev HEAD` → `C2_R58_SELFTEST: 23/23 pass` (receipt `selftest.txt`)

Tools: none installed or upgraded. Scratch `/fast/scratch/hyaku/tameshi-r58/T58W1RevengerC2/` deleted before yield (fixture lanes, claimant repo and work dirs are reproducible from `attack.py`, kept in receipts).
