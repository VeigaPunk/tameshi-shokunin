# FRoute01 — Route01 falsification (2026-10-21)

**Verdict: Disagree with the report’s complete-correction/F2-closure assertion; agree that the R18-1 line-2 correction and its historical 0→5 measurement were accurate at the stated revisions.**

## Strongest assertion attacked
Route01 §1 says the correction is exact and every mechanically checkable clause verifies; §4 F2 says the two conditional source-installation phrases are covered by the addendum. The latter does not hold for S063’s source anchor in delivered revision `55e1d312c4e8ac67aefad80099bd27581ff805c9`.

## Evidence and reproduced arithmetic
- `before.json`: `corrected=0`, `open=5`, `total=5`; R18-1 through R18-5 are all `open` (baseline `7243e7f…`).
- `after-21e7932.json`: `corrected=5`, `open=0`, `total=5`; all five rows are `corrected` (revision `21e7932…`). Both receipts’ rows sum to five; both pin ruler SHA-256 `c538c33d…e18e`.
- `checks.json` `.probes` row records argv `python3 .ufo/evidence/round-18/defect-probes.py --rev 921ef807…`, revision `921ef807…`, exit 0 and stdout SHA-256 `d37c99e3…`. Read-only `sha256sum` reproduced that digest; `probes.stdout` contains P01–P11 closed and one `DEFECT_PROBES: open=0 closed=11 total=11` tally. The exact revision is an ancestor of both `refs/heads/master` and `4b7c682…` (read-only ancestry checks succeeded).
- F1’s old non-durability observation is stale at the frozen delivery: `55e1…` contains `after-21e7932.json`. Do not count it as a current defect.
- The final `55e1…` tree’s note and `SOURCES.md` match the inspected files. At `SOURCES.md:72`, S063’s anchor remains `ENVIRONMENT VARIABLES, “The Git Repository”`; round-19 lesson lines 153–157 says the source sweep changed S063’s `used-by`, while status/recheck stayed unchanged. Yet the committed note’s R18-1 addendum lines 197–199 says “S063’s anchor is widened.” The cited Git docs put `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_NOSYSTEM` under `ENVIRONMENT VARIABLES > other`, not “The Git Repository” (opened 2026-10-21; Git 2.56.0 docs). Quote: “Whether to skip reading settings from the system-wide `$(prefix)/etc/gitconfig` file.” — `git-scm.com/docs/git`, Environment Variables > other > `GIT_CONFIG_NOSYSTEM`.
- The current `measure.py` R18-1 guard (lines 139–148) checks required note strings, the original stale sentence, receipt fields/digest and presence of the tally; it does not check S063’s anchor or the addendum. Thus the 5/5 result does not falsify this citation mismatch.

## Concrete falsifier / residual gaps
**Falsifier:** the committed addendum asserts S063’s anchor was widened, while the frozen `SOURCES.md` row still names only “The Git Repository”; the source documentation locates the two config-variable definitions under “other.” F2 therefore was not fully resolved; correct the source anchor/attribution or narrow the addendum claim. This does not invalidate the line-2 R18-1 correction.

The historical before/after receipts still pin the earlier `c538…` ruler; current `55e1…` `measure.py` is a different blob (SHA-256 `bb651eefdbe0f85b2d01408ec61e9accebeca8041c20b70982ae698634ff5053`). No final same-ruler 55e1 before/after receipt was present in the inspected evidence; I do not infer a current final count. No receipt argv was executed. LSP was unavailable (`xd://lsp`: no such mounted tool); grep only located the source row, which was read directly. Read-only checks only; no suites, selftests, builds, lint, or formatter run.