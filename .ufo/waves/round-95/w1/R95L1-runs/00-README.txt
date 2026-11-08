R95L1 receipts — inertness probe of the four round-95 C1 parser fixes
======================================================================

Scratch root (deleted before yield): /fast/scratch/hyaku/tameshi-r95/R95L1
Lane clone used as counter --repo (read-only; no lane mutation): <S>/lane,
  `git -C <S>/lane rev-parse --show-toplevel` asserted equal to <S>/lane.
Rev for every honest-note run: 02ff6290945dde18062a366799a774abb50fb365 (round base).
Base counter bytes: .ufo/evidence/round-94/c1/measure-v94.py read from that rev,
  sha256 a22563b0c2b4a2b43922cec3d1ab3fa511110e035b9edfdfdc6eaebb97023010.
All five variants were rebuilt from those bytes by variants/build-variants.py,
  each SELF_SHA256 recomputed (strip the single pin line, sha256 the rest).
  Run command shape (fresh, empty --work per run):
    python3 -I <counter> --repo <S>/lane --rev 02ff6290... --work <S>/work-<name>

Files
-----
  pristine.out / .rc                  v94 counter, honest note            exit 0
  fix-indent-code.out / .rc           A2 indented-code single fix         exit 0
  fix-split-cells.out / .rc           A4 backslash cell split             exit 0
  fix-delimiter.out / .rc             A5 one/two-hyphen delimiter         exit 0
  fix-single-pin.out / .rc            A3 exactly one self-pin line        exit 0
  fix-combined.out / .rc              all four fixes together             exit 0
  cmp-pristine-<variant>.txt          cmp exit, both sha256s, rows+summary sha,
                                      conjuncts sha
  variants/<variant>.py               built counter (pin recomputed)
  variants/<variant>.diff             unified diff base -> variant
  variants/<variant>-conjuncts.out    --conjuncts output + exit
  variants/manifest.txt               sha256, self-pin, conjuncts rc per variant
  variants/build-variants.py          generator (reads the v94 bytes, applies each fix)
  variants/witness-double-pin.py/.out second pin line inserted, pin NOT recomputed
  variants/witness-byte-edit.py/.out  one byte edited outside the pin line
  v95-parser-vs-combined.diff         function-level diff vs the v95 snapshot
  r95tree-and-v95.sha256              sha256 of the staged round-95 tree + v95 snapshot
  honest-note-form-scan.txt           note form counts at the base rev
  probe-*.out / .rc                   boundary probes (see R95L1.md)
  note-*.md                           probe notes (honest note + appended lines)
  probe-fixtures.diff                 exact append diff per fixture
  revs.txt, r95tree-rev.txt           synthetic scratch commit ids (objects live only
                                      in the deleted scratch clone)

Identity results
----------------
All six honest-note outputs are byte-identical:
  sha256 709767fc7ecb8e5a850dacaa7164e2566ba3f15e0baf00c2c0b648d3c0edfcea
  C1_ROW + C1_SUMMARY sha256
    f97de35274968f94b82cb4d371534e760b52aa04eab24b71eb50a685f02ec4bc
  C1_CONJUNCTS sha256
    deb430296fb9abfae5bb6897760ad30bb3ba432b7a14bdc20bd8af9eded73e8b

Exit codes
----------
pristine 0; indent-code 0; split-cells 0; delimiter 0; single-pin 0; combined 0.
Probes: list-continuation 1; indent-literal 0; indent-literal-v94 1;
list-continuation-indent-only 1; no-local-continuation 0.
Supplemental real v95: honest note at a synthetic scratch rev, exit 1
  (source=false: the round-95 lesson is not landed at that rev; every note-reader
  field matches pristine); v95 on the list-continuation fixture, exit 1
  (stray-verdict:366).

Scope
-----
This seat edited nothing in the lane outside R95L1.md and this directory. No
commit, branch/ref update, stash, checkout in the lane, or replace ref: every
synthetic fixture commit was made in the scratch clone with plumbing
(hash-object/read-tree/update-index/write-tree/commit-tree), and
`git replace -l` was empty in the clone and in the fleet repo for every run.
Scratch was deleted before yielding.
