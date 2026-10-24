# ConnectorSiblingOverlap — round 36, wave 1

**Verdict: NO CONTESTED SCOPE.** No sibling owns the cold-read ledger refresh, the round-36 public-slot successor counter, or the `git-scm.com/docs/git-hash-object` registry URL. Absorb nothing. One calibration note follows; it does not re-score C1 or C2.

Axes: this seat is judged on **calibration**. The note below stops three false contests and one real citation weld from being read as ownership or as the ground of the 6→8 credit. **Depth** (C2 predicate 6/3/9 on `c1-measure-v2.py`) is untouched. No axis is re-measured here.

## What was attacked

Sibling lane repos under `/home/vgpnk/Projects/shokunin/` (one directory per lane), read-only, against tameshi round-36 claims C1 (cold-read refresh) and C2 (successor panel counter) and the new S103 row. Lane tip `d9c496b19371b779ce0eec6dfee1b049b27a3a2d`. Contract `.ufo/evidence/round-36/contract.json` (`new_source_row` names S103 and snapshot sha256 `dd826daeeacaea01858ab1330e6f014ed1a0741652e5a710c578d137711f6100`, matched below).

Conf lanes in `shokunin.conf` (repo not `.`): audio, game-dev-2d, game-dev-3d, kaidoku, kasegi, kengaku, kake, kumitate, kotoba, kagi, kama, lore, revenger, tameshi, mado, tsukuroi, tabi, mori, chousa, souji, kotodama. Also present on disk and not conf lanes: empty `kaidoku-sh2`, and stub dirs `mori-shokukin` and `tameshi-shokukin` (same HEAD `2b435dd6716b00ec52ed83deb0979ba5f9ae23aa`; not treated as owners).

## Commands (exact) and revisions

Scratch: `/fast/scratch/hyaku/tameshi-r36-seats/ConnectorSiblingOverlap/`. `GIT_OPTIONAL_LOCKS=0` on every git call. No mutating git/jj. No installs.

```sh
git --no-optional-locks -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse HEAD
# d9c496b19371b779ce0eec6dfee1b049b27a3a2d

/home/vgpnk/Projects/shokunin/scripts/sources-census.sh shared --root /home/vgpnk/Projects/shokunin
# exit 0; 55 data lines → scratch shared.tsv
# script sha256 3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30

/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-24 \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin
# exit 0; 8 W04 + 1 W01 + ok → scratch tameshi-validate.tsv

sha256sum .../s103-git-hash-object.html .../corpus/SOURCES.md
# dd826daeeacaea01858ab1330e6f014ed1a0741652e5a710c578d137711f6100
# 16fae0a17acc934ceab8ffd177e73604bc5cbe62f7b354ce9650f0f77986cbd7

# scratch only; does not write an object (-w not passed)
printf 'tameshi-r36-sibling-overlap\n' > "$SCRATCH/sample.txt"
git --no-optional-locks hash-object "$SCRATCH/sample.txt"
python3 -c 'import hashlib,pathlib; p=pathlib.Path(".../sample.txt"); print(hashlib.sha256(p.read_bytes()).hexdigest())'
# git 2.56.0 object id 5dfddb06bc508948364b415d313a41cc2ceb9ad1 (40 hex)
# raw SHA-256 43b21b40b9e2c2e0bc9bde7ba1dcebf53eaad37f9138582f1b67e042d02143c5 (64 hex)
# equal False
```

Per-lane `git --no-optional-locks rev-parse HEAD` (exit 0) plus a walk of each `*-shokunin` tree (skip `.git`/`.jj`/`node_modules`, depth ≤ 8) for any `SOURCES.md`, and for basenames `c1-measure-v2.py`, `c1-measure.py`, `coldread/ledger.json`, `coldread/measure.py`. `SOURCES.md` text was scanned for `hash-object`.

| lane | HEAD |
|---|---|
| audio-shokunin | `7a2fcd4f08831154686e4e323031f41fffdb077f` |
| chousa-shokunin | `6ac1007e6a5d699d0742801026554fac1d900b5d` |
| game-dev-2d-shokunin | `7753d49b16674e122ed134403e7a9b301f2cbf7e` |
| game-dev-3d-shokunin | `89dd182b70943a20ae9aa6c1ed0e3c9b6e79c080` |
| kagi-shokunin | `899c50b42634a3a4ad0b28ab7509786315e2fc2b` |
| kaidoku-shokunin | `f432c8e3bc58934887c83f1db2b26f9910a9d87f` |
| kake-shokunin | `cd42e3c310ba442e89dde638ba6401adaefaf3e8` |
| kama-shokunin | `907cdcc0a76f8656fde4574c0a50725fcea42fa9` |
| kasegi-shokunin | `1fafde8f11454f3b0b98ab7f2b2e640aaf7f399a` |
| kengaku-shokunin | `1f3b0f1ec41ec297130e8944ff97968d32324632` |
| kotoba-shokunin | `11385e04e368c1e94ab1a5a89d7439033eb1f855` |
| kotodama-shokunin | `f107e84924ff53d72b55d9aa1c0e60b41135089f` |
| kumitate-shokunin | `383ad787ac3a9301b25422e50ebfef256d534924` |
| lore-shokunin | `380ef3abc7c7af11d7f23e9f9c82bb1937e1f695` |
| mado-shokunin | `3ae437caf71a3a945285109e014d6d2a0b0d2e5b` |
| mori-shokunin | `ede486b7a09afbacfb380d5871c46a8051a6dc2e` |
| revenger-shokunin | `8214e4dd7289d5a96cc23c0b2bf6407a9a43dbe0` |
| souji-shokunin | `4edb25dfe262515d0da63224bbba71e02e36cba5` |
| tabi-shokunin | `e3cf4e0d30bb835532ff44b118c5ad52e09eb76d` |
| tsukuroi-shokunin | `564db0b614b2914de5452f9ebd537a0653ae1de5` |
| tameshi-shokunin | `d9c496b19371b779ce0eec6dfee1b049b27a3a2d` |

## Ownership (three questions)

**(1) Cold-read ledger refresh.** Canonical `coldread/ledger.json` and `coldread/measure.py` appear only under `tameshi-shokunin/.ufo/evidence/round-{16,17,18,19,20,21}/`. No sibling tree in the walk has either file. Sibling `PROVINCE.md` files do not claim cold-read or tally-audit; kotoba's province table names tameshi as the adjacent owner of verification-fixture craft (`kotoba-shokunin/PROVINCE.md` tameshi row). Kengaku `ConnTameshi.md` cites tameshi's `calibration_restraint_score` wording; that is a read of this lane, not a second monitor.

**(2) Successor mutation-panel counter.** The only `c1-measure-v2.py` paths are tameshi's own historical counters (`round-29`, `round-30`, `round-32/v2`) and `.ufo/evidence/round-36/c1/c1-measure-v2.py`. A content search for `PUB_KILL_SLOTS` / `C1_R36V2_PASS` hits fleet reports of this lane, not sibling code. Kagi's homonym is not this counter: `kagi-shokunin/.ufo/waves/round-27/tools/c1-measure.py` (and sandbox copies) emits `format: kagi-round27-c1-measure-v2` and has no public-slot / tally-audit predicates.

**(3) git-hash-object SOURCES row.** The only `SOURCES.md` line containing `hash-object` is tameshi `corpus/SOURCES.md:112` (S103, URL `https://git-scm.com/docs/git-hash-object`). `shared` mode (normalized URL in ≥2 lanes, 55 URLs) does **not** list `git-scm.com/docs/git-hash-object`. Nearby shared pages are different manuals (`git-rev-parse` includes tameshi; `git-cat-file` is kama+souji and does not include tameshi; `gitrevisions` is kama+tameshi+mori). Tameshi `validate` W04 ×8 are intra-registry scope duplicates of other URLs (S047, S048, S075, S076, S077, S078, S081, S092), plus W01 on S101. S103 is not among them. Exit 0. Do not read that warning count as a hash-object contest (same count already noted by seat MTSourcesRow on this wave).

## Bounded proposal (one)

**Do not weld S103's object-ID sentence to the refresh's raw SHA-256 pins, and do not absorb a sibling row to "fix" the weld.**

Contradiction, stated separately (not averaged):

- The located quote is faithful. Snapshot `.ufo/evidence/round-36/src/s103-git-hash-object.html:1589` is "Compute object ID and optionally create an object from a file". `:1607-1611` is the DESCRIPTION sentence the lesson quotes (`corpus/lessons/round-36.md:36-38`): object ID, default type blob, report the object ID. The snapshot contains no `SHA-1` / `SHA-256` / `sha256` string.
- The teaches cell and the receipt citation are a different claim. Lesson `:39-41` and `refresh-receipts.json` `cited_source` (four copies, e.g. `:32`) say a blob ID is why a recorded digest binds evidence, "the ground for sha256-pinned inputs". The receipt argv (`:19` and traces `source-1.json`–`source-4.json`) does not run `git hash-object`. It runs `hashlib.sha256` on raw file bytes.
- Those functions are not the same. On the scratch sample above, `git hash-object` (2.56.0, no `-w`) emitted a 40-hex object id and `hashlib.sha256` of the same bytes emitted a different 64-hex digest.

Sibling surfaces that already say the nearer thing, and that this lane must not absorb:

- chousa S059 (`chousa-shokunin/corpus/SOURCES.md`, HEAD `6ac1007e…`) mines Python hashlib SHA-256 of bytes fed to a hash object. That is the function the receipt actually runs.
- mori S065 (HEAD `ede486b7…`) **rejects** hashlib as sole support for measured-revision provenance: a hash API describes byte digests, not which revision supplied the bytes.
- kama S033 (HEAD `907cdcc0…`) mines `git-cat-file` for raw object contents. That is still not `hashlib.sha256` of worktree files, and the URL is already shared with souji.

Move: leave S103, the ledger, the traces, `refresh-receipts.json`, `measure.py`, and `c1-measure-v2.py` byte-identical. An append-only lesson erratum (not this seat, not a receipt edit) may say: S103 grounds an object-ID report; it does not ground the refresh's raw SHA-256 pins; chousa/mori/kama rows are not imported. `.ufo/evidence/round-21/coldread/measure.py` has no `cited_source` / `hashlib` / `hash-object` string, so the restraint score does not read this citation. The 6→8 claim is not reopened here. C2's frozen counter is not an input to this note.

## Second-order effects

- **Runtime:** no monitor run, no v2 deciding run, no sibling gate executed. The hash comparison used a scratch file and `git hash-object` without `-w`.
- **Contract:** C1's kill rule is that the refresh receipts are the control→refresh delta. Editing them to swap the citation would change that delta after the deciding measurement. The proposal refuses that edit.
- **Substrate:** siblings stayed read-only. No product gate, no hashlib row, no kagi counter copied in.
- **Depth:** predicate 6/3/9, sealed panel, and `tally-audit-v3.py` were not opened for mutation and are not changed by naming the citation weld.

## Risks

A later seat can misread this note as voiding C1. It does not: credit is ledger entries, traces, and input blob hashes (ScoutCitedInputs on this wave already checked those hashes at `b455001e`); `cited_source` is unused by the monitor. The other misread is treating kagi's format string, kagi's `git hash-object` command logs, or the eight W04 lines as a contest. They are not. Copying chousa S059 into tameshi would create a new cross-lane share of `docs.python.org/3/library/hashlib.html` (already mori+chousa in `shared.tsv:53`) and would be absorption. The depth-8 walk can miss a sandbox buried deeper than 8; the census `shared` scan does not have that cap and still shows no hash-object URL, and the `PUB_KILL_SLOTS` content search across the fleet root found no sibling owner.

## Verification

L1 can re-run the two census commands and the scratch hash pair above; expected: S103 absent from `shared` output, absent from the eight W04 ids, and the two digests unequal. Confirm `measure.py` still has no `cited_source` before anyone treats the citation as score-bearing. Do not re-run the C1 monitor or the C2 deciding command for this note.

Only discovery reads, the read-only census, read-only git, one scratch `git hash-object` (no `-w`), and this report were produced. No production edits, no Git/jj writes, no counter or monitor runs, no model calls, no other agent runtime. Tools installed or updated: none.

Report: .ufo/waves/round-36/w1/ConnectorSiblingOverlap.md
