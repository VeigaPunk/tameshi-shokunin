# T56W1ScoutReceipts — receipt revision inventory

Pin `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1` (verified with `git rev-parse --verify PIN^{commit}`). Machine inventory: `.ufo/waves/round-56/w1/receipt-inventory.json`. Grep and `rev-parse` output: `.ufo/waves/round-56/w1/T56W1ScoutReceipts-receipts/`.

## Counts

Certifying receipts under `.ufo/evidence/round-40` through `round-55` at that pin:

| class | files |
|---|---|
| bound | 133 |
| unbound | 5 |
| unresolvable | 48 |
| no-token | 71 |
| **files** | **257** |

Binding tokens on those files: bound 161, unbound 8, unresolvable 114, embedded 1. The 48 unresolvable files hold 58 distinct tokens that `git rev-parse --verify TOKEN^{commit}` rejects. Eight of the 257 also carry an unbound binding token; for seven of those the file class is `unbound`, and for `.ufo/evidence/round-54/control/controls-b.stdout` the file class is `unresolvable` because `CTL_EXIT0` fails to resolve while `CTL_POS_c1` and `CTL_POS_c2` are unbound.

Side transcripts (selftest, quality, routed, successor, integrate, calibration) are in the JSON with `certifying: false` and are not in the table above. That side tally is bound 7, unbound 6, unresolvable 5, no-token 16.

The defect class is not three files. Rounds whose certifying file class is `unresolvable`: 42 (1), 47 (2), 48 (8), 49 (4), 50 (8), 51 (2), 52 (20), 54 (2), 55 (1).

## Sweep

Re-run from the lane, read-only, at the pin:

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse --verify 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1^{commit}
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r --name-only 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1 -- .ufo/evidence
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin grep -n -E -e 'rev=[0-9a-f]{7,40}' 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1 -- '.ufo/evidence/round-4*' '.ufo/evidence/round-5*'
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin grep -n -E -e '"rev"[[:space:]]*:[[:space:]]*"[0-9a-f]{7,40}"' 981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1 -- '.ufo/evidence/round-4*' '.ufo/evidence/round-5*'
```

Results: 1189 blobs under `round-4*` and `round-5*`, 443 `rev=` lines, 38 JSON `"rev"` lines, 223 files with at least one token. Nineteen of those are not receipts (assimilation snapshots, `*.py`, `*.sh`, `contract.json`, `freeze.json`) and are listed as `excluded_non_receipts`. Token patterns are the ones in `tools/receipt-revision-gate.py`: `rev=[0-9a-f]{7,40}` and `"rev":"[0-9a-f]{7,40}"`.

The measured revision for each round is the deciding revision named by that round's fleet report (`.ufo/reports/round-N/tameshi.md`), the SCORECARD block at the pin, and `corpus/lessons/round-N-verifier-spotcheck.md`. Each cited hash was resolved with `git rev-parse --verify`. Round 52 has no deciding revision: the report says the deciding run did not happen. Round 53's deciding revision is `88afa941` (SCORECARD measured close and the report). The authority block in the JSON records the full hashes and the source line.

## How a token was classed

A line that starts with `EXPLAIN`, or that contains ` stale:`, is an embedded quotation. It does not set the file class. One such token exists: `round-55/before/c1.stdout` line 12 quotes `rev=c21081008adb` inside an R54.2 stale citation. The file's own verdict line is `C1_R55: rev=0a2010acd1e9`, which is the round base, so the file is bound.

Otherwise:

- `before/` verdict → the round base. `at-base` filename → base. `at-freeze` filename → the settled freeze. `at-<hash>` filename → that commit. `after/` verdict, `frozen.stdout` → the deciding revision.
- `CTL_POS` / `CTL_POSITIVE` → the deciding revision only. That is the round-54 positive-control class.
- `CTL_0` / `do-nothing` → base, freeze, or another revision the report names.
- Any other control line → bound if the token resolves and is the base, the freeze, the deciding revision, a revision the report names, or an ancestor of the deciding revision (the gate's control-ancestor rule). Unresolvable if `rev-parse` fails.
- A cold-read trace under `rekey-<hash>` → that hash. Any other read → a revision the report names.

File class is the worst binding line: unresolvable, then unbound, then no-token, then bound. A file can be unresolvable and still contain an unbound line (`classes_present`).

## The three receipts the C2 counter already names

`round-54/control/controls-b.stdout` is unresolvable, and two of its lines are unbound. `CTL_POS_c1` and `CTL_POS_c2` name `rev=077d431e6996`, which resolves to `077d431e69965fa4673cd006ab64f6fc387f9e15`, the freeze. The claim was measured at `c21081008adbb6b6fe4e58a0aeec4831b30e318c` (spot-check deciding revision; the after receipts below name it). `CTL_EXIT0` names `rev=7df0e0426c98`. `git rev-parse --verify 7df0e0426c98^{commit}` exits 128, `fatal: Needed a single revision`.

The counter verdicts for that same claim are bound. `round-54/after/c1.stdout` and `c2.stdout` both name `rev=c21081008adb`. `round-54/before/c1.stdout` and `c2.stdout` both name `rev=d33053f7552d`, the base.

`round-54/after/deciding-run.exit` is the bytes `DECIDING_RUN_EXIT=0` and has no `rev=` token, so it is no-token. That is the acceptance record the C2 counter cites.

`round-55/after/c2.stdout` is 1666 bytes, stops at `EXPLAIN usable repeat-control --selftest`, and contains no `rev=` and no `C2_R55` verdict line. Class no-token. `round-55/after/c1.stdout` is bound: `C1_R55: rev=4c04c1d33377`, the measured revision. `round-55/before/c1.stdout` and `before/c2.stdout` are bound to the base `0a2010acd1e9`.

`round-55/control/controls-a.stdout` is unresolvable. `CTL_0_c1` and `CTL_0_c2` name the base and are bound. `CTL_SKIP_c1` (`2fd7f27ca799`), `CTL_FAB_c1` (`61aaf834c377`) and `CTL_SKIP_c2` (`13bb9e5d92df`) do not resolve. Same shape as round 54's break-controls, one round later.

`round-54/control/controls-a.stdout` is the same shape: `CTL_0` bound to the base, `CTL_R53` bound to `88afa9415454` (an ancestor of the deciding revision), `CTL_FAB` `042655edec78` and `CTL_LOGINPUT` `de700f6ccc7c` unresolvable (`rev-parse` exit 128).

## Five unbound files

The token resolves and is not the revision that line was supposed to name.

1. `round-43/prerun/c1-at-freeze.stdout` and `c3-at-freeze.stdout` name `rev=114ffacd813d`, which resolves to `114ffacd813d67286e369fc8f7b89f2c0418aaf4`. The settled freeze is `6b83a11c61f0fad1074ec1f2a4c38a2fd7034685`. `git merge-base --is-ancestor 114ffacd813d 3c4003f6e97e` exits 0, and the round-43 report names `114ffacd` as amendment A6/A7. The filename says freeze; the token is a later amendment.
2. `round-46/after/extra-receipts.stdout` lines 1 and 17 carry `rev=ea25e0224fc8` on `round45_line=C1_R45` / `C2_R45`. That is round 45's content revision, not round 46's deciding revision `3ae8b0484977`.
3. `round-47/before/pool-base.stdout` line 200 is `C2_R47: ... rev=9acfbe21435e ...`. `9acfbe21` is the freeze. The before slot's base is `0b5b7cd2`. The file is named `pool-base` and names the freeze.
4. `round-51/coldread/reads/T51W2Read14.md` has `"rev": "6d8c11e378aa90b12650808e1b79270742935f15"`. That commit exists (`git log -1` subject `round-51: integrate frontier/S022 correction, ...`) and `git merge-base --is-ancestor 6d8c11e3 7e548bee` exits 0. The deciding revision is `7e548bee` and the rekey directory is `rekey-02ec217c`. Neither the report, the SCORECARD block, nor the spot-check cites `6d8c11e3`.

## No-token

71 certifying files have no binding `rev` token. Ten of them are verdict-shaped:

- `round-45/control/controls-at-base.stdout`
- `round-46/control/controls-at-freeze.stdout`
- `round-48/after/c1.stdout` (empty; the C1 verdict is `c1-a3.stdout`, which is bound to `c7586b9a10ef`)
- `round-49/after/deciding-run.stdout`, `round-50/after/deciding-run.stdout`, `round-51/after/deciding-run.stdout` (body is `DECIDING_RUN_EXIT=0`)
- `round-50/control/c1-CTL_FAB.ledger.json`
- `round-53/control/controls.stdout`
- `round-54/after/deciding-run.exit`
- `round-55/after/c2.stdout`

The other 61 are auxiliary output that does not print `rev=` (census, no-harm, clean-tree, command D, cold-read section counts). They are in the JSON. They are not counter verdicts.

## Absent at the pin

`git cat-file -e 981c5e8b:.ufo/evidence/round-53/after/c1.stdout` exits 128. `git ls-tree -r --name-only PIN -- .ufo/evidence/round-53/after` is empty. `git log PIN -- .ufo/evidence/round-53/after/c1.stdout` is empty. The SCORECARD measured-close and the round-53 report both cite `after/c1.stdout` and `after/c2.stdout` at `88afa941`. Those blobs are not in this repo at the pin, so they are not in the 257. Round 53's committed certifying set here is two no-token files (`before/coldread-precheck-at-tip.stdout`, `control/controls.stdout`).

## What the classes do not show

A token that equals the right commit is bound even if it was copied. The round-56 contract's C2 `cannot_see` is the same gap.

A break-control that names an ancestor of the deciding revision is bound. That is why `CTL_R53 rev=88afa941` is bound and why the unresolvable count is only tokens `rev-parse` rejects. Positive controls are not given that pass: they have to equal the deciding revision.

Side-repo fixture hashes inside selftest transcripts are classified in the JSON and left out of the 257. The 58 unresolvable tokens above are already inside `control/` receipts, not inside selftests.
