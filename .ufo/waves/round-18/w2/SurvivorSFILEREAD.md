# SurvivorSFILEREAD — C1 survivor non-equivalence probe, defect S_FILE_READ

Seat: TameshiR18.SurvivorSFILEREAD · round 18 wave 2 (FALSIFY) · read rev 01d586ddbc5fcd78659557c4e93a6ee8517b87d1.
Target: kumitate `scripts/sources-check.mjs` @ 0acb7752d19058b953ebbeba253b1e35f6548de5 (blob sha256
6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f, 897 lines, 100755). Defect as registered:
`.ufo/evidence/round-18/sources-check/sources-check.defects.spec:53-56` (spec sha256 c8d24cb4…c91), one edit at
`scripts/sources-check.mjs:356`: `failClosed('READ_FAILED', …)` → `failClosed('SOURCES_MISSING', …)` in the
per-entry `corpus/knowledge/*.md` read catch.

## Result

**Non-equivalent.** I found off-suite inputs on which the pristine and the mutant give different outputs.
Each one is the suite's own `clean` fixture plus a single direct `corpus/knowledge/*.md` regular-file entry
that `readdirSync` lists but `readFileSync` cannot open. All three distinguish. Exit status is the same (2)
for both artifacts on all three. What differs is the fail-closed kind:

| witness | how the per-entry read fails | pristine (text final line / `--json failClosed.kind`) | mutant |
|---|---|---|---|
| `eacces` | `alpha.md` chmod 000 | `SOURCES_CHECK: FAIL-CLOSED (READ_FAILED)` / `READ_FAILED`, exit 2 | `SOURCES_CHECK: FAIL-CLOSED (SOURCES_MISSING)` / `SOURCES_MISSING`, exit 2 |
| `enoent` | extra regular file named `b'\xff.md'`: readdir decodes it to U+FFFD`.md`, which names no file | same as above, detail `cannot read corpus/knowledge/�.md (ENOENT)` | `SOURCES_MISSING`, exit 2, same detail |
| `enametoolong` | `--self` 3883 bytes long; an extra 253-byte entry name puts `join(knowledgeDir, name)` at 4154 > PATH_MAX 4096 | same as above, detail `… (ENAMETOOLONG)` | `SOURCES_MISSING`, exit 2, same detail |
| `clean` (control) | none | `SOURCES_CHECK: CLEAN (rows=1 …)`, exit 0 | identical (same stdout sha256) |

The first text line differs too: `SOURCES  fail-closed  READ_FAILED  …` vs `SOURCES  fail-closed  SOURCES_MISSING  …`.
The detail string is byte-identical between the two artifacts. Retained transcript: pristine at
`survivor-probes/S_FILE_READ/transcript.txt:155-173`, mutant at `:181-199`, summary at `:233-238`.

The harness reproduces both verdicts on the same mutant bytes. I ran lane `tools/mutate-and-run.sh` @01d586dd
(sha256 d22c4025…a8b) twice, with a one-defect spec cut verbatim from the registered spec (`transcript.txt:17-20`):
- Registered suite (`suite.txt`, sha256 6e550d5a…f7b): `CONTROL: GREEN`, then `DEFECT S_FILE_READ: SURVIVED (exit=0)`
  (`transcript.txt:82,86`). This matches the recorded row at `.ufo/evidence/round-18/sources-check/sweep/sweep.txt:101`.
- Off-suite probe (`probe-suite.sh`): `CONTROL: GREEN` (the pristine passes 4/4 witnesses), then
  `DEFECT S_FILE_READ: KILLED (exit=1)` and `MUTATE: DONE … killed=1` (`transcript.txt:101,115,131`).
- Mutant identity: sha256 67cb07e9e6952c223c26193575047b9c5bb82be874137abba80a4fcf5fe94ba0 in both harness runs
  (`transcript.txt:134-139`). My independent byte-exact replace gave the same hash (APPLY OK old-count=1,
  43497→43501 bytes). So did the wave-1 sweep's own mutant (`/tmp/tameshi-r4-2-run.ZIz4V0/mutant-S_FILE_READ.sources-check.mjs`,
  the MUTATE_EVIDENCE at sweep.txt:111). `diff` shows only `356c356` (`transcript.txt:141-145`).

## Why it survived (coverage)

I collected V8 block coverage of the pristine (`NODE_V8_COVERAGE`, counted with `cov-count.mjs`). The registered
suite ran in the `suite.txt` sandbox with only `NODE_V8_COVERAGE` added, and it still passed 46/46
(`transcript.txt:203`). Across 43 processes, the catch at `:356` ran **0** times, the try at `:355` ran 37 times,
and the directory-level catch at `:349` ran once (`transcript.txt:204-213`). Under the probe, `:356` ran 6 times
and `:349` ran 0 times (`transcript.txt:217-226`). This confirms the pre-registered rationale (spec:53): the suite's
`read-failed` fixture (`scripts/sources-check.mjs:790`, `knowledgeIsFile`, written at `:539`) hits the
directory-read catch, never the per-entry arm.

The selftest's checks are strong enough to kill this mutant: the fail-arm loop compares the exact final line
`SOURCES_CHECK: FAIL-CLOSED (${kind})` at `:796-801`. The gap is that no fixture reaches `:356`.

## Does the header contract promise this difference?

**Not explicitly.** In the header comment (`scripts/sources-check.mjs:2-45`):
- Promised, and kept by the mutant:
  - exit 2 for fail-closed (`:43-44`)
  - the final-line shape `SOURCES_CHECK: FAIL-CLOSED (<kind>)` (`:42`)
  - one JSON object under `--json` (`:44`)
- Not stated anywhere in the header: which fail-closed kinds exist, or which condition maps to which kind.
  - The header lists only finding kinds (`:10-31`).
  - USAGE (`:117-132`) lists only finding kinds (`:130`) and the exit map (`:131`).
- The mutant's kind, `SOURCES_MISSING`, is still a member of the code's vocabulary `FAIL_CLOSED_KINDS` (`:116`).

The mapping exists only in code and the selftest:
- `SOURCES_MISSING` is emitted only for ENOENT on `corpus/SOURCES.md` (`:182`, detail `corpus/SOURCES.md is absent`).
- Every other inspect/read failure maps to `READ_FAILED` (`:183`, `:185`, `:189`, `:349`, `:356`).
- The selftest pairs `SOURCES_MISSING` with the omit-SOURCES fixture and `READ_FAILED` with the unreadable-knowledge fixture (`:789-794`).

Nothing else in kumitate @0acb7752 uses the two kind names. `git -C kumitate grep -c -e SOURCES_MISSING -e READ_FAILED 0acb7752 --`
→ `scripts/sources-check.mjs:9` only (exit 0).

So the difference is externally observable (final line, first line, `--json failClosed.kind`). It contradicts the
code's own kind semantics: the mutant says `SOURCES_MISSING` while `corpus/SOURCES.md` exists and was parsed, and
its detail names a knowledge file. But the header contract leaves `<kind>` open, so the header does not promise it.
Any exit-only oracle (spec:3) can never distinguish the two artifacts, because every fail-closed result returns 2 (`:452`).

## Related finding (outside the S_FILE_READ brief; same coverage run)

5 of the 8 fail-closed return sites never run under the registered suite: `:175`, `:183`, `:185`, `:189`, `:356`
(`transcript.txt:205-213`; only `:177`, `:182`, `:349` run). The selftest's "every fail-closed arm fires" check
(`:803-804`) counts kinds, not return sites. `READ_FAILED` counts as covered once `:349` fires, which hides the
other four `READ_FAILED` sites.

Possible fixes for the owner (not done here):
- Add a fail arm whose fixture reaches `:356`. `enoent` and `enametoolong` do not depend on running as non-root; `eacces` does.
- Account for fail arms per return site rather than per kind.

kumitate HEAD is 1770305fae20826b39905a8251ddeca6b4957ac4. `git diff --stat 0acb7752 HEAD -- scripts/sources-check.mjs`
is empty (exit 0), so the file is byte-identical and the gap is still there at HEAD.

## Commands and exits

- `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 0acb7752…:scripts/sources-check.mjs` → sha256 6a293a72… = pin, 897 lines (exit 0).
- Byte-exact python replace in scratch → `APPLY OK old-count=1 bytes-before=43497 bytes-after=43501`, mutant sha256 67cb07e9… (exit 0).
- Fixture cross-check: `node suite-fixture.mjs pristine sources|entry | cmp - fixture/…` → both cmp exit 0. The stored `fixture/` is byte-identical to the selftest's `clean` fixture, regenerated from the pinned blob's own `makeRow`/`fixtureSources`/`BASE_ENTRY`.
- Driver, run with the fleet read-only and no network: `bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind $W $W --unshare-net --die-with-parent --chdir $W env -i PATH=$PATH HOME=$W/home TMPDIR=$W/tmp GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 LC_ALL=C bash …/S_FILE_READ/probe.sh $W/run` → outer exit 0 (`transcript.txt:2,240`). Inside it:
  - harness with the registered suite: exit 0
  - harness with the probe: exit 0
  - probe-suite on the pristine: exit 0
  - probe-suite on the mutant: exit 1
  - coverage runs: exit 0
- Witness manifest: ran the `probe-suite.sh` builder block (extracted verbatim), then `witness-walk.py` → exit 0 and 0. Result in `witness-manifest.txt`: mode, size and content sha256 of every witness entry; the `\xff.md` and 253-byte entries are copies of `alpha.md` (sha256 4568a06e…55e); `alpha.md` at mode 000 → `open-error=Permission denied`.
- `git -C kumitate grep -c …`, `git -C kumitate diff --stat 0acb7752 HEAD -- scripts/sources-check.mjs`, `git -C kumitate log --oneline -4 -- scripts/sources-check.mjs` → exit 0 each (results above).
- `grep '^S_FILE_READ' /tmp/tameshi-r4-2-run.ZIz4V0/results.tsv` plus sha256sum of that mutant → `SURVIVED 0 … 67cb07e9…`.

Environment: uid 1000; node v24.21.0; Python 3.14.8; kernel 7.2.11-arch1-1; scratch filesystem xfs.
No tools were installed or updated. All git operations were reads (`show`, `ls-tree`, `grep`, `diff`, `log`, `rev-parse`).
No GIT_* variables were set, and nothing was written outside the owned dir, this report, and `/tmp/tameshi-r18w2-SurvivorSFILEREAD-vmVcH2`.
That scratch dir is kept: it holds the harness workdirs and the coverage JSON.

## Files written (lane-relative)

`.ufo/evidence/round-18/sources-check/survivor-probes/S_FILE_READ/`:

| file | sha256 |
|---|---|
| `fixture/corpus/SOURCES.md` | 981bd0eb7d5ef8e8400eb8fdaadc773ff5798fabca2cffc88e6ef9d5f52f143c |
| `fixture/corpus/knowledge/alpha.md` | 4568a06e3dd7904d2d0593dadf5d204c20bcf1116f2822903e19bafdb0fc255e |
| `probe-suite.sh` (witness builder and the pristine-expectation suite) | 08a985916bb5599b4d140e371c3b4dd0368fd519deb18e0da540d5a5a84c978f |
| `probe.sh` (driver) | 6e9973b9ae92c23ada1346fd88259e36b2f3bd1f842d75ac9b0d8f475055adf2 |
| `cov-count.mjs` | c94e20651c9b766645bdedbc15e5fb2d9adb78ad198ffcfebeae4f6405d46aab |
| `transcript.txt` | 3b74a6c85a033315774871891f7a54e8ecde9dfcb29fba8cb2caca194226f175 |
| `witness-manifest.txt` | 26b12ea676867ca4ea3709a1dea04b9f95c691180001424bc39232d3078f1e9a |
| `witness-walk.py` | 6ab10a56b4e99e778e08c97cb4ecaf98e48cad76d2b6003b74f3ef696e5a67e9 |

The mode-000 file and the odd-name entries are created at probe time, not stored. A mode-000 file inside the lane
would break `git add`, and the non-UTF-8 and over-PATH_MAX names cannot be stored safely. Their exact bytes are
recorded in `witness-manifest.txt`. Lane tools read only the root `corpus/SOURCES.md` path (git grep of tools and
measure scripts @01d586dd), so the stored fixture corpus is not picked up by any lane census.

## Risks and limits

- The `eacces` witness needs a reader without root/CAP_DAC_*; the builder exits 125 if mode 000 is still readable.
- The `enoent` witness needs a filesystem that stores arbitrary name bytes and reports d_type (xfs here).
  [INFERENCE] On DT_UNKNOWN, Node lstat's the mangled name inside `readdirSync`, which would fail at `:349` instead.
  The probe's exact-detail assertion would then turn the pristine control red (SETUP), so it cannot produce a false kill.
- The `enametoolong` witness needs PATH_MAX 4096 and a short enough scratch root; the builder checks the geometry.
- The coverage selftest run is the `suite.txt` command plus one environment variable, not the registered suite verbatim; its outcome (46/46 PASS) matches.
- The lane harness used is @01d586dd (d22c4025…). The sweep's tool hash was fb6d86d5… (sweep.txt:7), but all three mutant constructions produced the same hash.

Verdict: **holds**. S_FILE_READ is not an equivalent mutant: the off-suite inputs above distinguish it in the final line and in `--json failClosed.kind`, though not in the exit status and not in anything the header contract promises. The recorded SURVIVED is a real gap in the suite's fixtures, and the pre-registered reason for it is confirmed by coverage, so C1's leg-8 record (5/10, 10/10 predictions) stands against this probe.
