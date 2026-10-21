# E01 — S049 re-open: quote verification and opened-date basis

Seat: `TameshiR20-3.E01S049Open` (scout, read-only + this trailer). Date of work: 2026-10-21.
No production file, tool, corpus, registry, Git/JJ ref, or sibling lane was modified. No installs (pacman untouched per host pause; used preinstalled `curl`, `python3` stdlib, read-only `git`).

## 1. Quote verification — VERIFIED

Command:
```
curl -s https://docs.python.org/3/library/subprocess.html -o /tmp/s049.html
sha256sum /tmp/s049.html   # dac28a6c853bad312071280b2d0c90d4df07f81f1238dd8fe1fe6b876fc1de37, 208624 bytes
```
Observed: page title `subprocess — Subprocess management — Python 3.15.0 documentation` (matches the row's "Python 3.15.0 docs").

Quote under test (14 whitespace-separated words, curly apostrophe U+2019):
> “these are used instead of the default behavior of inheriting the current process’ environment”

Verification: after HTML whitespace flattening, exact string occurs **2×**; word count = 14. A raw single-line grep of the HTML misses it because the sentence wraps across two HTML lines (`these are used instead of the default` at HTML lines 311 and 882; the phrase completes on the following line) — rendering caveat, not a mismatch.

Locations (both occurrences, nearest preceding `id="subprocess.*"` anchor):
1. **`subprocess.run` section** (anchor at HTML line 270; occurrence ~line 311) — the `run()` `env` argument paragraph. Full sentence: “If env is not None, it must be a mapping that defines the environment variables for the new process; these are used instead of the default behavior of inheriting the current process’ environment. It is passed directly to `Popen`.” — **this is the location the row and lessons cite**.
2. **`subprocess.Popen` section** (anchor at HTML line 606; occurrence ~line 882) — the `Popen()` `env` parameter paragraph, same opening sentence, continuing “This mapping can be str to str on any platform or bytes to bytes on POSIX platforms…”.

The SOURCES row (corpus/SOURCES.md:58, anchor “Using the subprocess Module, run() env paragraph; Python 3.15.0 docs served 2026-10-20”) and corpus/lessons/round-19.md:27–30 and corpus/lessons/round-20.md:13 all anchor to occurrence 1. Agree with the outside review at corpus/lessons/round-19-verifier-spotcheck.md:135 (“exact, 14 words, curly apostrophe, run() env paragraph”). Scope statement (“not proof of a particular historical environment”) matches the lesson usage.

## 2. Opened-date basis — explicit, with exact conversion

Observed inputs (read-only):
- Row cell `corpus/SOURCES.md:58`: `… | mined | 2026-10-20 | on-release | …` — introduced by round-14 commit `0c6e36d`, author date **2026-10-20 03:34:30 −0300**.
- Reopen: `corpus/lessons/round-19.md:27` “S049, reopened 2026-10-21”; `corpus/lessons/round-20.md:13` “S049 reopened 2026-10-21 **UTC**”. SOURCES/round-19 reopen commit `21e7932`, author date **2026-10-21 02:48:27 −0300**.
- Round-19 driver window (`corpus/lessons/round-19-verifier-spotcheck.md:12–13`): launch `2026-10-21T02:22:24−03:00`, complete `2026-10-21T04:21:02−03:00`.

Conversion (fixed offset; Brazil has had no DST since 2019, so BRT ≡ UTC−03:00 year-round):
```
0c6e36d  2026-10-20T03:34:30−03:00  =  2026-10-20T06:34:30Z   (row date 2026-10-20 in BOTH bases)
21e7932  2026-10-21T02:48:27−03:00  =  2026-10-21T05:48:27Z   (lesson date 2026-10-21 in BOTH bases)
window   2026-10-21T02:22:24−03:00  =  2026-10-21T05:22:24Z  →  2026-10-21T04:21:02−03:00 = 07:21:02Z
gap      2026-10-20T06:34:30Z → 2026-10-21T05:48:27Z  =  23 h 13 min 57 s
boundary UTC 2026-10-21T02:59:59Z = BRT 2026-10-20T23:59:59−03:00
         UTC 2026-10-21T03:00:00Z = BRT 2026-10-21T00:00:00−03:00
         (so UTC midnight 2026-10-21 = BRT 2026-10-20T21:00:00−03:00; any UTC instant in
          [00:00,03:00) of 2026-10-21 still has BRT date 2026-10-20)
```

Finding: the two dates are **two distinct events, not one event in two timezones** — (a) original opening of S049 in round-14, recorded in the row cell as a **local-BRT calendar date**, 2026-10-20; (b) the round-19 reopening, recorded in the lessons as a **UTC calendar date**, 2026-10-21. Both dates are stable under conversion in their respective bases, so no contradiction exists and no conversion can map one onto the other; they are ~23 h 14 m apart. The row's opened cell stays `2026-10-20` — agrees with `corpus/lessons/round-20.md:13` ("The immutable S049 row's opened date stays 2026-10-20; … different date bases"). **No row rewrite required or performed.**

## 3. Status and defects

- Quote: exact, located, recheck basis confirmed at Python 3.15.0 as served 2026-10-21 (page sha256 above). Disagree with nothing.
- Opened-date basis: made explicit as above. One observation (not a defect): `corpus/lessons/round-20.md` is currently untracked working-tree content (`git status --porcelain` → `??`), consistent with L1's in-flight round; it was read, not modified.
- Historical receipts and all frozen staged bytes untouched.
