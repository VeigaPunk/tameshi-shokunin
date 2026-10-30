# T58W1Panel07 — blind calibration

Axes: factual status at base, resolving-commit provenance, independent reproducibility, blind isolation.

Base: `2a32aa8228d5f86a85c81a923a3148bf792a9538`. All five assigned items are **fixed**. No lane-content changes proposed.

## Commands and receipts

Created a shared scratch clone, asserted its toplevel, then checked out the base detached:

```sh
mkdir -p /fast/scratch/hyaku/tameshi-r58/T58W1Panel07
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r58/T58W1Panel07/clone
test "$(git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel07/clone rev-parse --show-toplevel)" = /fast/scratch/hyaku/tameshi-r58/T58W1Panel07/clone
git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel07/clone checkout --detach 2a32aa8228d5f86a85c81a923a3148bf792a9538
```

Output: clone completed; `HEAD is now at 2a32aa82 round-57 verifier spot-check (integrator, hyaku): non-author admit/reject`.

Executed:

```sh
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w1/T58W1Panel07-receipts/derive.py
```

Exit **0**, empty stderr. Complete command/output transcript: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w1/T58W1Panel07-receipts/derive.stdout`; executable derivation and stderr are beside it. The driver reads committed objects through `git -C ... show`, enumerates only round-54 reader JSON, and performs no git mutations. Its diff demonstrates the corrections were introduced, not merely asserted by a later disposition table.

Both resolving commits passed `git -C CLONE merge-base --is-ancestor COMMIT BASE` with exit 0. Here CLONE denotes the absolute clone path above; the receipt expands every command fully.

## Verdicts and concrete evidence

### R54.4 — fixed

Resolving commit: `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`.

`git show BASE:SCORECARD.md`, lines 2654–2657: `Old: 49280fe5 ... Corrected: 8528ee85` for `c2/measure.py`. `git show --unified=0 FIX -- SCORECARD.md` shows this block added by FIX. Independently SHA-256 hashing the committed round-54 counter returned `8528ee8555da068519af4159f5f9e0efac8b29de88a53534a7043d7ec007e790`, exactly matching the printed `freeze.json` key. This is an explicit lane erratum, not an attempt to rewrite the historical report.

### R54.5 — fixed

Resolving commit: `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`.

`SCORECARD.md:2659–2665` records `w1=28 w2=25 sections=12`, replacing 25 and 22/9. The commit diff adds the correction. The driver independently enumerated committed direct `T54W1Read*.json` and `T54W2Read*.json` files and summed their findings arrays:

```text
{"wave": 1, "readers": 23, "findings": 28, "sections_with_findings": 15}
{"wave": 2, "readers": 23, "findings": 25, "sections_with_findings": 12}
RESOLUTIONS {"sections": 12, "findings": 25}
```

Per-file counts are preserved in the receipt. No reliance on the contradictory historical commit subject.

### R54.6 — fixed

Resolving commit: `ff2a821a1e83acd92bb4d62bad15f380973a55ea`.

`git show --format=fuller --stat COMMIT --` the three named paths returned **3 files changed, 309 insertions** (report 282 lines; receipts 5 and 22). At BASE, `git ls-tree` returned regular blobs for each:

```text
7448be1be6510bfc261b5b120ce14c0a54489d88 T54W2Sent03.md
c63fc96c958c09377f2e8eb56fced010c7d11dba c1committed-positive.stdout
4cdc204cd232a2df6321ef9217810037dfd9e7ff rejection-attribution.txt
```

Comparing `git show COMMIT:PATH` with `git show BASE:PATH` returned `True` for all three byte comparisons. `SCORECARD.md:2667–2671` separately records the sweep. The old deciding run was dirty; committing the deliverables resolves durability, not historical cleanliness or a universal guarantee about future seat behavior.

### R54.7 — fixed

Resolving commit: `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` (the prose correction, not the earlier rename).

`SCORECARD.md:2673–2678`: `Corrected: the file was renamed into .../T54W2Sent01-receipts/forged-reader.json ... (R100)`; the diff introduces this correction. Independent `git show --name-status 7fa9a5e -- OLD NEW` returned full commit `7fa9a5e0104bc181872401547987d6744f3b570d` and `R100 OLD NEW`. `git ls-tree BASE -- NEW` returned blob `90f66a2e44168a0adf8e9b08a1c70c035d40c0af`. Thus this is rename, not deletion.

### R54.8 — fixed

Resolving commit: `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`.

Committed seat file `/fast/scratch/hyaku/tameshi-r58/T58W1Panel07/clone/.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md:332–343` explicitly says `SUPERSEDED` and `The claim that it authorised the write is withdrawn`, retaining the operator-owned-file rule. The same commit adds both this annotation and `SCORECARD.md:2680–2690`, which records the incident in the succeeding round-55 lesson rather than modifying the historical round-54 lesson. `corpus/lessons/round-55.md:62` records the unauthorized write, late operator turn, and withdrawn fabricated-turn characterization. This resolves the two missing records. I did not inspect the live host config/history DB: their historical state is a recorded explanation, not independently reproduced host evidence.

## Residual risk and verification gaps

- LSP unavailable: reading `xd://lsp` returned `No such tool`. Used literal searches and committed-object diffs, not claimed semantic-reference proof. These assigned defects concern documentation and artifact durability.
- No runtime/gate execution was needed to judge these five record defects; no counter pass or saturation claim is made.
- A broad filename glob exposed one round-57 staged path name incidentally; no round-57 wave file content, prior candidate ledger, prior panel, or other round-58 seat output was opened. All verdicts derive from base content and original item records.
- No tools installed or updated. No lane/fleet git mutations. No staged content fixes needed.

Scratch cleanup executed `rm -rf -- /fast/scratch/hyaku/tameshi-r58/T58W1Panel07 && test ! -e /fast/scratch/hyaku/tameshi-r58/T58W1Panel07`; exit 0, output `Scratch removed: /fast/scratch/hyaku/tameshi-r58/T58W1Panel07`.

Self-evaluation: accuracy 4 (host incident's underlying DB not re-opened); completeness 5 (five verdicts, introduction diffs, ancestor checks, cleanup); clarity 4 (long receipt separated from summary); actionability 5 (machine output plus replayable evidence); conciseness 4 (historical nuances require extra explanation). Average 4.4. Improvement: a future scoped host-incident audit could independently verify the historical operator-turn evidence; it is not required for the missing-record defect here. User agreement expected because every verdict is grounded in the tree, with gaps explicit.
