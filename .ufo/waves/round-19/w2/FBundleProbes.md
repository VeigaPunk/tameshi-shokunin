# FBundleProbes — round 19, w2

Date: 2026-10-21. Read-only source/JSON review; no receipt, suite, or selftest was executed.

## Verdict

**Disagree, narrowly, with the strongest conclusion** in `w1/BundleProbes.md` §§1, 4–6: its observed row is a successful-looking historical receipt, but the delivered C1 ruler still does not enforce the report's own proposed argv/stderr falsifier for that row. The report did identify this omission in §5; its claim that it is not a C1 gap is the part that does not survive the frozen source.

## Evidence and arithmetic

- `.ufo/evidence/round-19/before.json`: revision `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`, corrected `0`, open `5`, total `5`; all five rows are open.
- `after-21e7932.json`: corrected `5`, open `0`, total `5`; all five rows are corrected, but this receipt is revision `21e79329f8bdcf01a62be63b3e46db4a7de6b6f9`, not `55e1d312…`. It is not evidence of a final 55e1 measurement. The only `after*` receipt present is `after-21e7932.json`.
- `final/checks.json` SHA-256 is `fed3c8e6…5815c671d`; its `probes` row records argv `python3 .ufo/evidence/round-18/defect-probes.py --rev 921ef8077440f90d092aab4b9fdc750a45de1224`, revision equal to argv[3], and integer exit 0. The retained stdout SHA-256 is `d37c99e3…aeb8cf0`, matching the row; it has P01–P11 closed and the `open=0 closed=11 total=11` summary. The retained stderr is 0 bytes, SHA-256 `e3b0c442…b855`.
- Source attribution is consistent but not process-authenticated: `defect-probes.py` requires `--rev` (`:1035–1046`), resolves a full commit and checks detached clone HEAD (`:274–327`), and text mode prints the summary (`:952–957`). It copies the invoked script into the clone (`:328–331`), so the receipt does not itself prove the executed script bytes, cwd, or interpreter. The source SHA-256 at 921ef and 55e1 is `99297d96…dadebeaa`; the exact old source behavior cited by w1 is therefore not stale.

## Concrete falsifier / missing correction

At frozen revision `55e1d312…`, `measure.py` is blob `d13dc4fb…`, identical to the worktree. Its `guard()` reads `old['revision']`, `old['exit']`, `old['stdout_sha256']`, and stdout summary (`measure.py:139–148`), but never reads `old['argv']`; `PATHS` includes `checks.json` and `probes.stdout`, not `probes.stderr` (`:46–51`). The exact-argv/two-stream `receipt()` helper (`:78–96`) is used for the newer witness/measure receipts (`:183–205`), not the old `probes` row. This conflicts with QUALITY39's effective-receipt requirement (`corpus/QUALITY.md:352–361`) for the success claim w1 makes.

Concrete falsifier (not executed): change only `checks.json['probes']['argv'][3]` to another revision, leaving its `revision`, exit, stdout digest and stdout bytes unchanged. The frozen R18-1 `guard()` predicate still passes, since it does not inspect argv. Binding that field and retaining/digest-checking stderr remain missing corrections in this ruler; the current receipt's values themselves are not shown to be wrong.

## Residual unknowns

No final same-ruler before/after measurement at 55e1 was present; L1's final run remains the needed evidence. The row does not establish the historical producer's actual interpreter, cwd, or executed runner bytes. No broader admission or closure judgment is made.