# ReviewArchive — round 15 wave 2: historical capture-context.py archive review

Seat: TameshiR15.ReviewArchive (reviewer, leaf). Static review only. Nothing was executed: no gate, selftest, probe, measure.py, or historical script run. Git was used only for read-only `status`, `ls-files`, `diff`, and `diff --quiet`. Tool installs/updates: none. All findings are author-side advisory.

Question: is the old `.ufo/evidence/round-14/capture-context.py` still treated as historical and immutable, and not as active probe guidance?

## Exact source read

- `tools/context-capture.py`: 1–14, 102–103 (docstring), 136–146 (pins), 1152–1180 (`check_receipt`, `tool_declaration` check), 1298–1344 (`run_check`, frozen path), 1581 and 1717 and 2017 (selftest tempdir and cleanup). A grep of the whole file for `capture-context`, `round-14/capture`, `open(`, `os.replace`, `unlink`, and `shutil` returned no code reference to the historical script path.
- `.ufo/evidence/round-14/capture-context.py`: 1–34, 46–58, 583–647. Disk SHA-256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`, which matches `tools/context-capture.py:140-141`.
- `.ufo/evidence/round-14/context-receipt.json`: disk SHA-256 `05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a`, which matches `tools/context-capture.py:137-139`.
- `SKILL.md`: 1563–1602 (round-14 recipe step 5 at 1592–1595; round-14 registry at 1597–1602), 1609–1675 (round-15 classification and archive status at 1623–1641), 1676–1691 (round-15 registry).
- `.ufo/evidence/round-15/measure.py`: 28–35, 56, 134–154 (`registry_rows`), 204–272, 315.
- Corpus and log: `corpus/lessons/round-14-verifier-spotcheck.md:160`; `corpus/lessons/round-15.md:50–51`; `corpus/README.md:186` and `:197–203`; `corpus/SOURCES.md:59–60` (S050, S051); `LOG.md:900–940`.
- Git state, read-only: `git status --porcelain` shows only ` M SKILL.md` and `?? tools/context-capture.py`. The historical script is tracked and `git diff --quiet 0c6e36d -- .ufo/evidence/round-14/capture-context.py` exits 0. `git diff -U0 -- SKILL.md` contains no changed line in the round-14 probe row or step 5; the only addition is the round-15 section.

## Findings (by severity)

### F1 — High: the historical script still writes the frozen round-14 receipt, and the registry misdescribes that write

- `.ufo/evidence/round-14/capture-context.py:58` sets `OUTPUT_REL = ".ufo/evidence/round-14/context-receipt.json"`. The docstring at `:23–24` says "Output: … context-receipt.json (atomic, 0644); no other path is written."
- `write_receipt` (`:583–602`) runs `mkstemp` and then `os.replace` onto that path.
- `main` (`:605–643`) reaches `write_receipt` on the `InvalidContext` branch (`:617–627`) and on the normal branch (`:629–636`) for every status (`ok`, `mismatch`) before it returns. Only `-h`/`--help` (`:607–609`) and unexpected arguments (`:610–613`) exit without writing.
- Counterexample (static trace, not run): a no-argument run of the historical script replaces the frozen receipt. `tools/context-capture.py` frozen mode then hashes the file (`:1323–1333`) and returns `snapshot_tampered`, exit 2, against the pin at `:137–139`. The committed C1 replay no longer reproduces `context_consistent`/exit 0.
- The active registry text is false. `SKILL.md:1592–1593` says the script "writes only its new round14 receipt". `SKILL.md:1602` says "writes only new round14 context receipt". The output is the existing frozen file, not a new one.
- The supersession note at `SKILL.md:1633–1638` says the script is "not an entry point". The file is still runnable, and nothing in the repo blocks it.
- Recommended fix (lane decision): inline marker at `SKILL.md:1592` and `:1602`, for example "SUPERSEDED, DO NOT RUN: writes frozen `.ufo/evidence/round-14/context-receipt.json` (historical `:58`, `:583–602`); use `tools/context-capture.py --check`." Historical bytes stay untouched.

### F2 — Medium: historical immutability is claimed by the active gate but not enforced by it

- `tools/context-capture.py:13–14` says "The historical script and every round-12..14 byte remain untouched." No code in the tool opens, reads, or hashes `.ufo/evidence/round-14/capture-context.py`. The grep of the whole file (see above) found only docstring references.
- `FROZEN_TOOL_SHA256` (`:140–141`) is compared only to the receipt's stored string `receipt["tool_sha256"]` (`:1175–1179`). It is never compared to the bytes on disk.
- Counterexample (static): any edit to the historical script leaves frozen `--check` at exit 0 `context_consistent`. The receipt bytes and the stored string are unchanged, so nothing notices.
- Only advisory coverage exists: `.ufo/evidence/round-15/measure.py:32–35` (`HISTORICAL_DIGEST_PATHS`) and `:315` (`historical_script_sha256`). `measure.py` is a count printer, not a gate, and I did not verify its output.
- Recommended fix: either qualify the docstring at `:13–14` to say the tool never reads or writes the historical script, with its bytes pinned only by round-15 `measure.py`; or add an on-disk hash check with its own selftest case. Gate owner's choice.

### F3 — Medium: the round-14 section of the active registry still presents the historical script as a live probe, and the supersession sits far away

- `SKILL.md:1592–1595` (recipe step 5) reads "is an opt-in prospective probe" in the present tense, with a runnable command.
- `SKILL.md:1601–1602` (round-14 registry) keeps the row `invocation context capture | probe | python3 .ufo/evidence/round-14/capture-context.py | 0 … 1 … 2 …`. It has no 64 class.
- `measure.py:56` includes `probe` in `REGISTRY_KINDS`, and `:146` matches the needle in the entry column. So the row is parsed as an active `probe` entry. `measure.py:213` and `:270–272` report it only as `context_historical_registry_rows`. No measured verdict depends on it, but any consumer scanning the registry for `kind=probe` finds a live entry.
- The supersession is declared at `SKILL.md:1633–1638`, 30+ lines below and under a different heading. It names `:1592–1595` and `:1602`, but those lines carry no local marker. The round-14 disposition row at `:1601` still says "64 usage" (the round-15 correction is at `:1669–1675`).
- Tension to decide: `SKILL.md:1630–1631` says the round-14 row is "retained unedited as the historical record". An inline annotation would be additive and would not change the historical text. Lane decision.

### F4 — Low: corpus index row cites the historical script without the word "archived"

- `corpus/README.md:186` lists `../.ufo/evidence/round-14/capture-context.py` as the source for "explicit invocation context", with no archive label. `corpus/README.md:197–203` correctly says the historical script is "frozen evidence, not an active probe recipe". The index row is not runnable guidance, so this is minor. Suggested fix: add "archived" to the cell, if the append-only policy allows it.

## Bounded agreement (no counterexample found)

- `tools/context-capture.py:9–10` labels the historical script "archived" and the new tool "the promoted, active replacement". Lines `:102–103` say it is never imported. No code path imports or executes it. Selftest fixtures live only under `tempfile.mkdtemp` (`:1581`) and are removed with `rmtree` (`:1717`, `:2017`).
- Pins match the disk today: frozen receipt `05cb55b8…99c1a` (`:137–139`); FROZEN_TOOL_SHA256 `7313e9a2…7d89` (`:140–141`) equals the historical script on disk.
- The round-15 narrative is consistent: `SKILL.md:1623–1641`, `LOG.md:932–938`, `corpus/lessons/round-15.md:50–51`, and `corpus/README.md:197–203` all describe the historical script as archived and `tools/context-capture.py` as the maintained gate.
- Historical bytes are unchanged in the working tree, as shown by the git state above.

This agreement is textual and static. It is not a prediction that any check will pass.

## Verification gaps

- Nothing was executed. The F1 and F2 counterexamples are traces of the source, not observed runs.
- I searched only the tameshi lane tree. I did not search fleet-root dispatchers or other lanes for anything that runs the historical script.
- `.ufo/evidence/round-15/claims.json` and `integration-decisions.json` returned no hits for `capture-context` or `context-capture` in the grep. I did not read them in full.
- I did not validate `measure.py` output, and I did not compare its `HISTORICAL_DIGEST_PATHS` digests against the disk.
