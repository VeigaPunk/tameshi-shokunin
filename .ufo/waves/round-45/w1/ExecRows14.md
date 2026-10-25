seat: ExecRows14

# Round-45 w1 — C1 row re-verification (author), rows S074, S079, S084

Verdicts: S074 holds, S079 holds, S084 holds. All three fragments pass the frozen counter's seat-level `--check` against the freeze rev (`--rev 3310e7be803516ca5934b4e949d91bcec824b179`). Raw snapshots kept in `/tmp/tameshi-r45-ExecRows14/` for L1 integration.

Tools installed: none (curl/python3/git already present; no install was needed). RULES.md read per operator directive.

## S074 — git-symbolic-ref (Git manual)

Row: `corpus/SOURCES.md:83` (frozen at rev `3310e7be803516ca5934b4e949d91bcec824b179`).

- URL: `https://git-scm.com/docs/git-symbolic-ref` (first http(s) URL in the source cell, byte-exact)
- curl: exit 0 (`curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-ExecRows14/S074.raw https://git-scm.com/docs/git-symbolic-ref`), 28676 bytes
- sha256: `9615451998adf20b6a81c3a87969f460985c26b73d40e777c245f673c6c03b42`
- CHECK: `CHECK S074 verified ok`
- Note: the §NOTES exit-status sentence still reserves exit 1 for a non-symbolic ref and 128 for any other error, and the §OPTIONS `-q` line still says a detached HEAD exits non-zero silently, grounding the teaches' exit-code branching.

```json
{"id":"S074","url":"https://git-scm.com/docs/git-symbolic-ref","opened":"2026-10-25","verdict":"holds","raw_sha256":"9615451998adf20b6a81c3a87969f460985c26b73d40e777c245f673c6c03b42","quote":"with status 1 if the requested name is not a symbolic ref, or 128 if another error occurs.","snapshot":".ufo/evidence/round-45/freshness/sources/S074.raw.gz","author":"ExecRows14","note":"The NOTES exit-status sentence still reserves exit 1 for a non-symbolic ref and 128 for any other error, and the OPTIONS -q line still says a detached HEAD exits non-zero silently, grounding the teaches' exit-code branching."}
```

## S079 — Timezones (Reproducible Builds documentation)

Row: `corpus/SOURCES.md:88` (frozen at rev `3310e7be803516ca5934b4e949d91bcec824b179`).

- URL: `https://reproducible-builds.org/docs/timezones/` (first http(s) URL in the source cell, byte-exact)
- curl: exit 0, 40603 bytes
- sha256: `382b311453d53b6a107c287abe33e59267fe883c4fb407d0bfe5854c894aaf65`
- CHECK: `CHECK S079 verified ok`
- Note: the page still advises setting the TZ environment variable when no dedicated option exists, immediately before its TZ=UTC example, grounding the teaches' explicit-TZ method.

```json
{"id":"S079","url":"https://reproducible-builds.org/docs/timezones/","opened":"2026-10-25","verdict":"holds","raw_sha256":"382b311453d53b6a107c287abe33e59267fe883c4fb407d0bfe5854c894aaf65","quote":"When there is no dedicated option, it is most often possible to set the TZ environment variable:","snapshot":".ufo/evidence/round-45/freshness/sources/S079.raw.gz","author":"ExecRows14","note":"The page still advises setting the TZ environment variable when no dedicated option exists, immediately before its TZ=UTC example, grounding the teaches' explicit-TZ method."}
```

## S084 — os.path — Common pathname manipulations (Python docs)

Row: `corpus/SOURCES.md:93` (frozen at rev `3310e7be803516ca5934b4e949d91bcec824b179`).

- URL: `https://docs.python.org/3/library/os.path.html` (first http(s) URL in the source cell, byte-exact)
- curl: exit 0, 90223 bytes
- sha256: `f9c52515afbea4010d17b851ef344e4b6eda6806a503c02e8872f606a4fa0343`
- CHECK: `CHECK S084 verified ok`
- Note: the realpath first paragraph still defines the canonical path with symbolic links eliminated, and the section's strict-parameter discussion still says non-strict mode may leave missing or looping components, grounding the teaches' identity-vs-sandbox reading.

```json
{"id":"S084","url":"https://docs.python.org/3/library/os.path.html","opened":"2026-10-25","verdict":"holds","raw_sha256":"f9c52515afbea4010d17b851ef344e4b6eda6806a503c02e8872f606a4fa0343","quote":"Return the canonical path of the specified filename, eliminating any symbolic links encountered in the path","snapshot":".ufo/evidence/round-45/freshness/sources/S084.raw.gz","author":"ExecRows14","note":"The realpath first paragraph still defines the canonical path with symbolic links eliminated, and the section's strict-parameter discussion still says non-strict mode may leave missing or looping components, grounding the teaches' identity-vs-sandbox reading."}
```

## Evidence notes

- All three quotes are verbatim substrings of `measure.py --extract` output on the fetched `.raw` files (never copied from registry cells); token counts 18 / 17 / 16 (within 6–25), each sharing >= 2 content words with the row's scope/anchor/teaches (S074: `symbolic, status, error`; S079: `dedicated, option`; S084: `canonical, path`).
- The counter ran only as `--check` (seat-grade, never a deciding run), against the freeze rev `3310e7be803516ca5934b4e949d91bcec824b179`.
- `.raw` files retained at `/tmp/tameshi-r45-ExecRows14/S{074,079,084}.raw` for L1 snapshot integration; fragment JSONs at `/tmp/tameshi-r45-ExecRows14/S{074,079,084}.json`.
- No drift observed on any row; all three hold.
