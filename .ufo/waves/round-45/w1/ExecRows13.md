seat: ExecRows13

C1 row re-verification; rows S072, S078, S073 (author of these ledger entries). All verdicts `holds`; all three `--check` runs against freeze `3310e7be803516ca5934b4e949d91bcec824b179` print `verified ok`. No tools installed (used existing python3/curl; pacman paused, nothing needed). Raw files kept at /tmp/tameshi-r45-ExecRows13/ for L1 integration.

## S072
- URL: https://man7.org/linux/man-pages/man2/open.2.html (first http(s) URL in source cell, byte-exact)
- Fetch: `curl -fsSL -A 'Mozilla/5.0' --max-time 90` exit 0; 76506 bytes; sha256 `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789`
- Anchor located in normalized `--extract` text: O_TRUNC entry in file creation flags list ("O_TRUNC If the file already exists and is a regular file and the access mode allows writing (i.e., is O_RDWR or O_WRONLY ) it will be truncated to length 0. If the file is a FIFO or terminal device file, the O_TRUNC flag is ignored. Otherwise, the effect of O_TRUNC is unspecified.")
- CHECK: `CHECK S072 verified ok` (exit 0)
- Note: The live open(2) page still states O_TRUNC truncates the file when the access mode allows writing, grounding S072's teaches that an O_RDWR+O_TRUNC open is write-capable.
- Fragment:
```json
{"id":"S072","url":"https://man7.org/linux/man-pages/man2/open.2.html","opened":"2026-10-25","verdict":"holds","raw_sha256":"d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789","quote":"a regular file and the access mode allows writing (i.e., is O_RDWR or O_WRONLY ) it will be truncated to length 0.","snapshot":".ufo/evidence/round-45/freshness/sources/S072.raw.gz","author":"ExecRows13","note":"The live open(2) page still states O_TRUNC truncates the file when the access mode allows writing, grounding S072's teaches that an O_RDWR+O_TRUNC open is write-capable."}
```

## S073
- URL: https://docs.python.org/3/using/cmdline.html (first http(s) URL in source cell, byte-exact)
- Fetch: `curl -fsSL -A 'Mozilla/5.0' --max-time 90` exit 0; 171073 bytes; sha256 `fd147b22f36d8162649d7cb3ace6f3acf93a05e1bceb07c305d6962e8d3be9f6`
- Anchor located in normalized `--extract` text: §1.2 envvar entries "PYTHONDONTWRITEBYTECODE ¶ If this is set to a non-empty string, Python won't try to write .pyc files on the import of source modules. This is equivalent to specifying the -B option." and "PYTHONPYCACHEPREFIX ¶ If this is set, Python will write .pyc files in a mirror directory tree at this path, instead of in __pycache__ directories within the source tree. This is equivalent to specifying the -X pycache_prefix=PATH option. Added in version 3.8."
- CHECK: `CHECK S073 verified ok` (exit 0)
- Note: The live CPython 3.15 cmdline docs define PYTHONPYCACHEPREFIX as redirecting .pyc writes into a mirror tree at the given path, grounding S073's teaches.
- Fragment:
```json
{"id":"S073","url":"https://docs.python.org/3/using/cmdline.html","opened":"2026-10-25","verdict":"holds","raw_sha256":"fd147b22f36d8162649d7cb3ace6f3acf93a05e1bceb07c305d6962e8d3be9f6","quote":"Python will write .pyc files in a mirror directory tree at this path, instead of in __pycache__ directories within the source tree.","snapshot":".ufo/evidence/round-45/freshness/sources/S073.raw.gz","author":"ExecRows13","note":"The live CPython 3.15 cmdline docs define PYTHONPYCACHEPREFIX as redirecting .pyc writes into a mirror tree at the given path, grounding S073's teaches."}
```

## S078
- URL: https://man7.org/linux/man-pages/man2/open.2.html (first http(s) URL in source cell, byte-exact)
- Fetch: `curl -fsSL -A 'Mozilla/5.0' --max-time 90` exit 0; 76506 bytes; sha256 `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789`
- Anchor located in normalized `--extract` text: §DESCRIPTION access-mode paragraph ("These request opening the file read-only, write-only, or read/write, respectively.") and the O_TRUNC entry ("If the file already exists and is a regular file and the access mode allows writing (i.e., is O_RDWR or O_WRONLY ) it will be truncated to length 0. If the file is a FIFO or terminal device file, the O_TRUNC flag is ignored. Otherwise, the effect of O_TRUNC is unspecified."). (Quote chosen from the O_TRUNC entry, not the access-mode sentence, because the access-mode sentence appears verbatim in the row's anchor cell and would fail the not-copied-from-row check.)
- CHECK: `CHECK S078 verified ok` (exit 0)
- Note: The live open(2) page confirms O_TRUNC truncates a regular file when write access is allowed and is ignored for FIFOs/terminals, supporting S078's correction of S072.
- Fragment:
```json
{"id":"S078","url":"https://man7.org/linux/man-pages/man2/open.2.html","opened":"2026-10-25","verdict":"holds","raw_sha256":"d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789","quote":"a regular file and the access mode allows writing (i.e., is O_RDWR or O_WRONLY ) it will be truncated to length 0.","snapshot":".ufo/evidence/round-45/freshness/sources/S078.raw.gz","author":"ExecRows13","note":"The live open(2) page confirms O_TRUNC truncates a regular file when write access is allowed and is ignored for FIFOs/terminals, supporting S078's correction of S072."}
```

Evidence summary: 3 rows fetched live (all curl exit 0), quotes located afresh in normalized extract output, all `--check` runs print `verified ok`. Raw files S072.raw, S073.raw, S078.raw retained at /tmp/tameshi-r45-ExecRows13/. No blockers.
