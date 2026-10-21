# Route05 — routed defect 5: final-revision measurement receipt

## Axis and scope

C1 CALIBRATION only: preserve restraint score 8 and make no promotion or new numeric-score claim. This is receipt attribution/durability, not an added claim or a new cold-read credit.

## Finding

Round-18 verifier spot-check §5 item 5 routes the report's final-revision 60/60 statement: the round-18 receipt names `a85f7107c4167cd9968248722256fcaf617fc30c`, not the claimed `4b7c6823a462f5ea2eafcb262275300a545f3ed7`. The fleet report still has the unqualified assertion at `.ufo/reports/round-18/tameshi.md:53` and repeats it in the Box3 line at `:77` (“strict60/60 at `a85f710…` and final tip”). `final/measure-final-60.json` confirms `revision` and `rev_input` are both `a85f710…`, with 60/60, restraint 8, and no overrides. `final/checks.json` has no main-measure receipt row; its `measure-selftest` row is not evidence of a 60/60 measurement.

The current corpus lesson already contains an append-only `Errata R18-4 / R18-5` at `corpus/lessons/round-18.md:135-155`. Its R18-5 links a later exact-tip replay and explicitly distinguishes its timing from the original round-18 report. Keep that erratum; do not rewrite the fleet report or duplicate the correction. Its key qualification is “repairs missing evidence, not its original timeliness” (round-18 lesson, R18-5, 2026-10-21).

The linked replay receipt `.ufo/evidence/round-19/round18-final-measure.json` records argv `python3 .ufo/evidence/round-18/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 4b7c6823a462f5ea2eafcb262275300a545f3ed7 --explain`, revision `4b7c682…`, exit 0, and stdout/stderr digests. I did not invoke that old measurement tool. Read-only `sha256sum` of the two recorded output files matched both receipt digests. The committed stdout reports `sections_covered=60`, `sections_total=60`, `calibration_restraint_score=8`, `overrides_used=false`, and both `revision` and `rev_input` equal to `4b7c682…`.

## Exact append-only correction to retain

If R18-5 is absent in the delivered lane tree, append the following dated erratum to `corpus/lessons/round-18.md`; otherwise retain the existing R18-5 without duplication:

> **Erratum R18-5 — final-revision measurement provenance (2026-10-21).** The round-18 report's 60/60 statement at final `4b7c6823a462f5ea2eafcb262275300a545f3ed7` lacked a receipt at that revision when the report was issued. The round-18 `final/measure-final-60.json` receipt binds only `a85f7107c4167cd9968248722256fcaf617fc30c`. The later replay in `.ufo/evidence/round-19/round18-final-measure.json` records a successful strict measurement at the exact `4b7c682…` revision: 60/60 input-keyed sections, restraint 8, no overrides. This later receipt repairs the missing evidence, not its original timeliness; it does not show the receipt existed at round-18 close or establish 60/60 for any later round-19 revision. The historical fleet report remains unchanged.

This wording preserves the original report as history, attributes the later observation to its actual replay, and avoids extending the result to a different revision.

## Failure-capable predicate for the delivered audit

Run a read-only receipt audit against explicit **committed tree objects**, not the worktree and not by re-running `measure.py`. Inputs are the fleet commit containing `.ufo/reports/round-18/tameshi.md` and the delivered lane revision. Read each blob with `git show <commit>:<path>`; a missing object/blob or any failed assertion returns nonzero. Require all of:

1. The fleet report blob contains the historical `4b7c682…` statement and the delivered lane's `corpus/lessons/round-18.md` blob contains the R18-5 correction/link and its no-retroactive-timeliness qualification.
2. The delivered lane tree contains `.ufo/evidence/round-19/round18-final-measure.json`, plus the receipt's referenced stdout and stderr blobs. The wrapper `revision` equals the full target hash `4b7c6823a462f5ea2eafcb262275300a545f3ed7`, `exit == 0`, and `argv` is exactly the recorded `measure.py --repo <lane> --rev <target> --explain` invocation.
3. SHA-256 of each committed stdout/stderr blob equals the wrapper's `stdout_sha256` / `stderr_sha256`. Parse committed stdout as JSON and require `revision == rev_input == <target>`, `coldread.sections_covered == coldread.sections_total == 60`, `calibration_restraint_score == 8`, and `overrides_used is false`.
4. The predicate must reject the round-18 `final/measure-final-60.json` as a substitute: its `revision` is `a85f710…`, so pointing at the wrong revision cannot pass merely because its metrics are also 60/60.

This is failure-capable: deleting the exact-tip receipt/output, changing the target revision, returning a nonzero exit, breaking either digest, altering any required metric, or omitting the erratum causes a failed assertion/nonzero status. The source reads establish the current receipt contents and output digests; membership in the final delivered lane commit is intentionally left to the main audit and is not asserted here.

## Sources and observed commands

- Read `corpus/lessons/round-18-verifier-spotcheck.md` §5, defect 5; observed the original defect is specifically missing evidence at `4b7c682…`, with the 60/60 receipt at `a85f710…`.
- Read fleet `.ufo/reports/round-18/tameshi.md:19-80`, especially `:53` and `:77`; observed the duplicate final-tip claims remain in the historical report.
- Read lane `.ufo/evidence/round-18/final/measure-final-60.json` and `checks.json`; observed the former binds only `a85f710…` and the latter has no main-measure receipt row.
- Read lane `corpus/lessons/round-18.md:135-155`, `.ufo/evidence/round-19/round18-final-measure.json`, and its referenced stdout/stderr; observed R18-5 and the exact-tip replay described above.
- Executed only `sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-19/round18-final-measure.stdout /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-19/round18-final-measure.stderr`; both output digests matched the wrapper. No old tool, build, test, lint, or formatter was run; the committed-tree predicate above was proposed, not executed.
