# MTLedgerEntry4 — mutation probe: cold-read ledger refresh entry 4 (`read_rev` rewind)

Seat: mutation tester (leaf). Target claim: **C1** — the cold-read monitor refresh of the four
round-35-drifted SKILL sections restores calibration credit 6 → 8.
Probe authorised: scratch-copy the lane, set refresh entry 4's `read_rev` to its parent commit,
re-run the monitor, capture. Expected by dispatch: input-drift.

Lane state at probe time: `d9c496b19371b779ce0eec6dfee1b049b27a3a2d` (round-36 receipts).
Refresh commit `b455001e2589b3f4f471d94a3de7e5e549b9f54c`; its parent / entry `read_rev`
`e423c41ba253357ab8c8513f0376dad9d38ab248`; that commit's parent (the mutation target)
`796e08b888849308d0c4d5e932e56833600a139f`.

Frozen inputs verified by sha256 before probing:
`tools/tally-audit-v3.py` `6188db16…d354`, `tools/mutate-and-run.sh` `a7d3f2dd…12eb9`,
`round-36/c1/c1-measure-v2.py` `9eb8944c…8fa53`,
`round-21/coldread/ledger.json` `29bddc03f957ef962a6e8d6192e96527e017d86d294d1944b07cb3263ba3bbbf`.
None was written.

## Mutant

One defect, one line, in an isolated clone — plausibility: the refresh author stamps the parent
rev instead of the rev the read actually happened at (copy/paste of the previous entry's field).

- Location: `.ufo/evidence/round-21/coldread/ledger.json`, entry index 496
  (`start` 1436, heading `### Where to enter — four readers`), file line 40284.
- Edit: `"read_rev": "e423c41ba253357ab8c8513f0376dad9d38ab248"` →
  `"read_rev": "796e08b888849308d0c4d5e932e56833600a139f"` (= `e423c41^`).
- Uniqueness: the same line text occurs 4× (entries 493–496); the mutator asserted all four hit
  indices, that the last is line 40284 (0-based 40283), that it is preceded by
  `"commands_executed_count": 1,` and followed within 12 lines by `source-4.json`, and that the
  three sibling entries keep `e423c41`. Post-write JSON re-parsed; `entries[-1].read_rev` asserted
  equal to the parent, `start`/`heading` unchanged, entry count 497.
- Diff: `git diff --numstat` = `1 1` (one insertion, one deletion), scratch commit
  `759127ef03004513a9d15b6a0a29e3ac62e0331d`.
- Ledger sha256 before `29bddc03…bbbf` → after mutation `d17b74e82784bafdd761ccf3e74b2dbc66382f09c0397568c5e12290d38c9482`
  (verified as the blob consumed at the mutant rev).

## Detector (frozen, unmodified)

`python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/measure.py`
is the round-21 selector over the frozen round-18 credit algorithm. Run strict — no
`--ledger-file` / `--ledger-rev` / `--inputs-overlay` (the selector refuses each with exit 64),
so `overrides_used` is `false` and the input gate is the claim-bearing strict path. The mutant
ledger is supplied the only way the claim reads one: as the blob at `REV`.

## Commands and outputs

```
python3 <measure.py> --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev d9c496b      # pristine
  exit 0 · revision d9c496b… · calibration 8 · 64/64 covered · reasons {"credited": 64}
  section 1436: credited=true vetoed=false reason=credited

git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r36-seats/MTLedgerEntry4/lane      # .git only; lane never mutated
python3 <mutator>                                                # the single-line edit above
git -c user.name='MTLedgerEntry4 probe' … commit -am 'MTLedgerEntry4 mutant: … read_rev -> parent 796e08b'

python3 <measure.py> --repo /fast/scratch/hyaku/tameshi-r36-seats/MTLedgerEntry4/lane --rev 759127e   # MUTANT
  exit 0 · revision 759127e… · calibration 8 · 64/64 covered · reasons {"credited": 64}

python3 <measure.py> --repo /fast/scratch/hyaku/tameshi-r36-seats/MTLedgerEntry4/lane --rev 796e08b   # read-only diagnostic
  exit 0 · revision 796e08b… · calibration 6 · 60/64 covered
  section 1436: credited=false reason=input-drift:corpus/knowledge/closeout-r11.md

git reset --hard -q d9c496b                                                          # restore
python3 <measure.py> --repo /fast/scratch/hyaku/tameshi-r36-seats/MTLedgerEntry4/lane --rev d9c496b   # RESTORED
  exit 0 · revision d9c496b… · calibration 8 · 64/64 covered · reasons {"credited": 64}
```

Raw JSON kept at `/fast/scratch/hyaku/tameshi-r36-seats/MTLedgerEntry4/{pristine-lane,mutant,earlier-rev,restored}.json`.

## Verdict

**VERDICT: SURVIVED** — the mutant ledger (entry 4 `read_rev` = parent `796e08b`) still reads
`calibration 8`, section 1436 `credited=true`, reason `credited`. The detector emitted **no**
`input-drift` for entry 4 and no other reason string. Expected-under-dispatch, not observed:
`input-drift:SKILL.md` / `input-drift:corpus/knowledge/closeout-r11.md`.

### Why it survived (two independent causes, both verified)

1. **The gate is `read_rev`-blind.** `input_reason(repo, rev, entry)` → `input_failures(repo, rev, view)`
   (`.ufo/evidence/round-18/measure.py`:330,353,358; called at :523 and :537) verifies each recorded
   input with `ls_tree_mode/cat_file_blob(repo, **rev**, path)` — the *measurement* rev. `read_rev`
   has no runtime consumer in the load path: the only occurrences are the docstring (:85), the
   `--inputs-overlay` field allow-list (:139, a merged value that is never read), and selftest
   fixtures (:831,1347,1350). Docstring step 4 states the same design (`REV:<p>`).
2. **Entry 4's data makes a `read_rev`-aware gate inert anyway.** Both recorded inputs are
   byte-identical at `e423c41` and its parent `796e08b`:
   `SKILL.md` `2381873162fc21db756f8e8744d85aaa6dfc245a01175d5d5ac66557f617d35a`,
   `corpus/knowledge/closeout-r11.md` `f0894bf65aee32d81fde3f9233b8f35968e200bc7906d0035a786d3df94d1fd7`.
   The refresh commit changed only the ledger and its evidence files — never `SKILL.md` — so the
   dispatch premise "recorded shas no longer match at the earlier rev" is false for *this* entry
   specifically. (Entries 493–495 do record post-parent `LOG.md`/`SCORECARD.md`/`QUALITY.md` shas,
   so they would drift under a `read_rev`-aware gate; I did **not** run that second probe —
   [INFERENCE] from the same code path, outside the one-defect assignment.)

Additional observable the probe exposed: the mutated ledger declares `read_rev=796e08b` while its
own trace receipt `.ufo/evidence/round-36/coldread/traces/L1/source-4.json` records
`"rev": "e423c41…"`, `inputs` matching both the entry and the parent's blobs. The detector accepts
this contradiction and credits the section: `read_rev` truthfulness is not part of C1's audited
surface.

### Reading the diagnostic honestly

The `796e08b` run is **not** evidence of drift for entry 4. At that rev the monitor reads the
pre-refresh ledger blob `fc16d21a602ee6e8bc9d069cd0da6e3e26d4805cbb11b9e030a19deb4c9b5cd7`
(the same blob at `e423c41`; the ledger first changes in `b455001`), so entry 4 does not exist
there and the `input-drift:…closeout-r11.md` reason comes from an older entry over the same
section. It is the claim's before-state (6), reproduced, and it agrees with the committed receipt
line `monitor before(796e08b)=6`.

## Restoration evidence

- Restored blob sha256 `29bddc03f957ef962a6e8d6192e96527e017d86d294d1944b07cb3263ba3bbbf`, equal to
  the lane's pre-probe bytes and to `git cat-file blob d9c496b:…ledger.json`.
- `git status --porcelain` in the clone empty after `reset --hard`; pristine and restored detector
  JSON are byte-equal under canonical serialization (`pristine==restored JSON: True`) — same
  revision, same 64/64, same `{"credited": 64}`.
- Lane untouched throughout: HEAD still `d9c496b…`, lane ledger sha256 still `29bddc03…bbbf`;
  the mutant commit lives only in the scratch clone. The only lane path created by this seat is
  this report.

## Tooling

None installed or upgraded; no `pacman`. Probe used the system `python3` and `git` already present.
Scratch root: `/fast/scratch/hyaku/tameshi-r36-seats/MTLedgerEntry4/` (clone + 4 JSON captures).

VERDICT: SURVIVED (entry-4 `read_rev` rewind; detector read_rev-blind and data-inert for this entry)
