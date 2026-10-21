# F06 — S080 rejection scope audit

**Verdict: done — agree, with a boundary caveat.** The `rejected` status is scoped to this round's frozen F5 population; the reviewed record does not reject SOURCE_DATE_EPOCH's truth or the source's quality. Do not broaden that into a claim that the variable was absent from every F5 invocation or could not affect any measured surface.
Audit axes: source fidelity; F5 scope/population; registry status and flip; observed-versus-unobserved behavior.

## Observed evidence

- Reopened primary source: [Reproducible Builds, SOURCE_DATE_EPOCH](https://reproducible-builds.org/docs/source-date-epoch/), opening definition paragraph (native-HTML `read`, 2026-10-21). Its text says that distributions can set this standardized environment variable centrally for build tools to consume to produce reproducible output, and defines the represented time as the last modification of something, usually source code.
- The L1 quote is verbatim in that paragraph and is 20 whitespace-delimited words (under the 25-word limit): “SOURCE_DATE_EPOCH specifies the last modification of something, usually the source code, measured in the number seconds since the Unix epoch”. The original's “number seconds” wording is preserved.
- The frozen contract `.ufo/evidence/round-21/c2-contract.json:9-16` names exactly seven profiles: `host`, `clean`, `clean_repeat`, `tz`, `locale`, `home`, and `columns`. None is a deliberately varied timestamp profile. The population is nine pinned surfaces (`:24-34`). Thus adding a controlled timestamp substitution profile would expand, rather than merely interpret, the frozen profile set.
- `corpus/SOURCES.md:89` records S080 as `rejected`; its scope says “rejected for this finite-profile claim,” its reason is that timestamp substitution is not a frozen F5 profile and would expand the denominator, and its flip is a separately frozen timestamp-sensitive fixture and profile population. Its used-by points to `corpus/lessons/round-21.md`.
- The decision agrees across `.ufo/evidence/round-21/l1-source-s080.json:2-9`, `corpus/lessons/round-21.md:30-37`, and the registry log at `corpus/SOURCES.md:197-202`: each says rejected for this round's frozen seven-profile population, not rejected as false; each records the separate-fixture/profile flip. The lesson explicitly says “S080 is not false or low quality.”
- The knowledge entry's source list (`corpus/knowledge/hermetic-env-differential.md:1-3`) names S079, S028, and S081—not S080—as support for the admitted finite method. That is consistent with the registry's rejected status.

## Counterexamples and boundary

- A claim that the source is false or irrelevant would be contradicted by the live source itself: its examples include Python reading `SOURCE_DATE_EPOCH` to derive a build date, CMake honoring it since version 3.8.0, and Docker Buildx propagation to timestamp metadata. These are concrete source examples of real timestamp-sensitive build output; they are not evidence that any of the nine frozen F5 surfaces consumes it.
- `host` is defined as the invoking environment minus `GIT_*` variables (`c2-contract.json:10`), so it could incidentally contain `SOURCE_DATE_EPOCH`; the contract does not say it is scrubbed. Conversely, `clean` is an `env -i` profile (`:11`), so it does not carry that variable unless explicitly added (it is not). The evidence therefore justifies “no controlled timestamp substitution axis was frozen,” not “SOURCE_DATE_EPOCH was absent from all observed environments” or “these tools are invariant to it.” A host-vs-clean difference, if present, would not by itself isolate timestamp causality.
- Literal search of this repository found `SOURCE_DATE_EPOCH` in source/decision records and task-history text, with no hit in the F5 implementation or knowledge entry. This is only a literal-string check, not proof that no program can consume the variable indirectly; the pinned surface sources were not searched in this audit.

## Flip assessment

The recorded flip—freeze a timestamp-sensitive fixture and a profile population separately—is coherent and scope-preserving: it requires the added axis to be specified before measuring it, rather than silently changing this round's denominator. It is a gate for a future claim, not a fully specified future experiment; a future population would still need to identify the fixture and define controlled baseline/changed-timestamp profiles. I found no disagreement between the registry, L1 evidence, and lesson on the present rejection.

## Commands and provenance

- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse HEAD && git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin status --porcelain | wc -l` — exit 0; output was `790abd2129f153c13b471e381d454186edbde65e` and `15`. Findings cite the checked-out source at that HEAD; the 15 worktree entries were not attributed by this audit.
- `functions.read` of the URL returned the page via native HTML; the reader did not report a process exit code.
- `functions.grep` for `S080` located the rows/decision references; literal `SOURCE_DATE_EPOCH` search returned records/history and no hit in this repository's F5 implementation or knowledge entry. The pinned surface sources were not searched; the search tool reports matches, not numeric exit codes.
- No tests, builds, or production changes were made. The only file written for this assignment is this report.

## Remaining unknowns

No separate timestamp-sensitive fixture/profile was executed; no result here establishes behavior of the nine surfaces when SOURCE_DATE_EPOCH is explicitly varied. The exact contents of the invoking environment used for the retained F5 receipt were not established by this source audit.
