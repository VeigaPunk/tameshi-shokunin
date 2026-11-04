# Registered before novel probe execution
Axes: fixture safety / behavioral detection / exact restoration.
Pinned plan revision: d39be4b04474bf393fee24ee2ac47de58e0159fd.
Target: scratch candidate.py, sha256 699637385316e0fb49557dbea0b05a50c63eaa18842b9ea435aed253add0e477, independently located arm20 lines 599–600.
One edit: replace `                shutil.rmtree(fix, ignore_errors=True)` with `                pass  # mutation: omit arm20 fixture cleanup` (retain finally syntax).
Detector, identical for pristine/mutant/restored: `python3 -I -X utf8 <scratch>/candidate.py --selftest`, TMPDIR=<scratch>/tmp, timeout 60s, run from scratch.
Prediction: SURVIVED; selftest stays 20/20 because it measures reconciliation but never checks fixture removal. Expected production-shaped discriminator: one normal CLI --selftest leaves one `wave-reconcile-git-*` real Git fixture directory under TMPDIR on the mutant, versus zero on pristine/restored. Count before/after each suite; this side observation is not silently added to the detector.
Restore original exact bytes even on failure; remove scratch after preserving receipts. No claim judgment.
