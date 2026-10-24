# MTSourcesRow — S103 census-row mutation probe (round 36, w1)

**Verdict: KILLED ×2 — both mutations detected by the census validator as specified.**

## What was attacked

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` at rev `d9c496b19371b779ce0eec6dfee1b049b27a3a2d` (read-only; never edited).
- Target artifact: `corpus/SOURCES.md`, row `S103` (`| S103 | git-hash-object ... |`), pristine sha256
  `16fae0a17acc934ceab8ffd177e73604bc5cbe62f7b354ce9650f0f77986cbd7` (13 pipe fields, NF=13).
- Detector: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` sha256
  `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30` — `validate` mode
  (E01 malformed row, E11 used-by path missing on disk).
- Scratch copy (all mutation work): `/fast/scratch/hyaku/tameshi-r36-seats/MTSourcesRow/tameshi-shokunin/`
  (`rsync -a --exclude='.git'` of the lane; pristine bytes kept at `.../MTSourcesRow/SOURCES.pristine.md`).

## Commands (exact)

Baseline on the real lane (read-only):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-24 \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin
# exit=0; last line: tameshi-shokunin  ok  <lane>/corpus/SOURCES.md
```

Baseline on the pristine scratch copy (same output modulo the ok-path; `.../baseline.out`, exit 0).

Mutant 1 — drop the `recheck` column (`365d`) from the S103 row → NF 13→12:

```
ed: | mined | 2026-10-24 | 365d | .ufo/.../refresh-receipts.json ... |
 -> | mined | 2026-10-24 | .ufo/.../refresh-receipts.json ... |
sha256(SOURCES.md)=938f6d378fd3749cd3078b186194a8a60621042495acd9f18d4d0ea2d36dfc7a  (NF=12)
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-24 \
  /fast/scratch/hyaku/tameshi-r36-seats/MTSourcesRow/tameshi-shokunin
```

Actual output (`mut1-drop-column.out`, stderr empty):

```
tameshi-shokunin	E01	S103 fields=10
*** exit=1 ***  (no `ok` line)
```

Expected: E01 malformed-row (NF!=13). **Observed: E01 S103 fields=10, exit 1 → KILLED.**

Mutant 2 — used-by cell first path replaced with a nonexistent path, 13 fields preserved:

```
ed: | mined | 2026-10-24 | 365d | .ufo/evidence/round-36/coldread/refresh-receipts.json, corpus/lessons/round-36.md |
 -> | mined | 2026-10-24 | 365d | .ufo/evidence/round-36/coldread/does-not-exist-s103.json, corpus/lessons/round-36.md |
sha256(SOURCES.md)=4e56ba0b29a4b2144f2d75b2a2a56387f9b5e8589ccab54f9380922581c97d13  (NF=13)
<same validator command as above>
```

Actual output (`mut2-dangling-usedby.out`, stderr empty):

```
tameshi-shokunin	E11	S103 missing used-by .ufo/evidence/round-36/coldread/does-not-exist-s103.json
*** exit=1 ***  (no `ok` line)
```

Expected: E11 missing used-by path. **Observed: E11 S103 missing used-by …, exit 1 → KILLED.**

## Restoration evidence

- After each mutant, `cp -p .../SOURCES.pristine.md <scratch>/corpus/SOURCES.md`.
- Final scratch sha256 `16fae0a17acc934ceab8ffd177e73604bc5cbe62f7b354ce9650f0f77986cbd7`,
  byte-identical to `SOURCES.pristine.md` and to the live lane `corpus/SOURCES.md`
  (all three hashes equal; `cmp` identical).
- Post-restore validator rerun: `tameshi-shokunin ok …/SOURCES.md`, exit 0.
- Real lane left untouched: its `corpus/SOURCES.md` hash is still `16fae0a…`; no lane file was edited.
- Baseline failure? No — pristine baseline was clean (exit 0) before both mutants, so both kills are conclusive.

## Notes

- Only pre-existing W-codes (W04 ×8, W01 ×1) appear in every run; they do not change exit status
  (warning-only registry stays exit 0), and E01/E11 each flipped the lane to exit 1.
- No tool installs or upgrades were needed; no subagents dispatched.
- Scratch tree retained at `/fast/scratch/hyaku/tameshi-r36-seats/MTSourcesRow/`
  (`baseline.out`, `mut1-drop-column.out`, `mut2-dangling-usedby.out`, `*.err`, `SOURCES.pristine.md`).
