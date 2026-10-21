done

# Python `time` / `locale` source findings

## Finding

Both requested official Python documentation pages were opened live on 2026-10-21. They are distinct canonical URLs, current Python 3.15.0 documentation, and directly cover the requested `TZ`/`time.tzset()` and `locale.LC_ALL` API contracts. Proposed statuses are `mined`, for the planned `corpus/knowledge/hermetic-env-differential.md` citation; these are draft rows only and `corpus/SOURCES.md` was not edited.

- **Access-time sample:** `2026-10-21T09:02:39-03:00` (`date --iso-8601=seconds`, exit 0). Both pages were fetched in the same parallel read batch.
- **Python docs version/footer observed on both pages:** Python 3.15.0 documentation; footer “Last updated on Oct 21, 2026 (07:27 UTC)”; Sphinx 8.2.3.
- **Duplicate check:** searched `corpus/SOURCES.md` for `https://docs\.python\.org/3/library/(time|locale)\.html`; no matches. The table already has other Python documentation URLs (e.g. subprocess and doctest), but neither proposed canonical URL is present. The source-search tool returned “No matches found” and does not expose a numeric process exit code.
- **Row ID basis:** `corpus/SOURCES.md` records S079 as next unused. S079/S080 below are proposals and should be reallocated if the integrator has since allocated them.

## Draft rows

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S079 | time — Time access and conversions (Python 3.15.0 docs) — https://docs.python.org/3/library/time.html | docs | A | Unix `time.tzset()` and the `TZ` input to local time-conversion rules | `time.tzset()` and `TZ` environment-variable note @ Python 3.15.0 docs; fetched 2026-10-21 09:02:39 -03:00; footer updated 2026-10-21 07:27 UTC | On Unix, `TZ` specifies the rules `time.tzset()` resets; changed-`TZ` effects without calling `tzset()` are explicitly not reliable. | mined | 2026-10-21 | on-release | corpus/knowledge/hermetic-env-differential.md |
| S080 | locale — Internationalization services (Python 3.15.0 docs) — https://docs.python.org/3/library/locale.html | docs | A | Python locale API's `LC_ALL` category and requesting user-preferred settings across categories | `locale.LC_ALL`; `setlocale()` and Background, details, hints, tips and caveats @ Python 3.15.0 docs; fetched 2026-10-21 09:02:39 -03:00; footer updated 2026-10-21 07:27 UTC | `LC_ALL` combines locale settings; `setlocale(LC_ALL, '')` requests the user's preferred locale settings for all categories (typically specified via `LANG`). | mined | 2026-10-21 | on-release | corpus/knowledge/hermetic-env-differential.md |

`mined` basis: both are official primary documentation for the scoped API behavior and the planned knowledge entry is the intended citation. The intended `used-by` path did not yet exist when checked; do not land these as mined rows unless the knowledge entry is created and cites the IDs (otherwise the contract's mined/used-by invariant is unmet). No rejection is proposed.

## Located quote evidence

1. **S079 — `time`:** “The environment variable `TZ` specifies how this is done.” (9 words.) Location: [`time.tzset()`](https://docs.python.org/3/library/time.html#time.tzset), immediately after the opening sentence “Reset the time conversion rules used by the library routines.” The same section says Unix availability and explicitly cautions that changes may affect `localtime()` without `tzset()` but “this behavior should not be relied on.”
2. **S080 — `locale`:** “Combination of all locale settings.” (5 words.) Location: [`locale.LC_ALL`](https://docs.python.org/3/library/locale.html#locale.LC_ALL), its definition paragraph. Additional grounding: the Background section says, “The program must explicitly say that it wants the user’s preferred locale settings for other categories by calling `setlocale(LC_ALL, '')`.” (19 words.) The `setlocale()` example paragraph says this sets all categories to the user's default setting, typically specified in `LANG`.

## Search and commands

- Bounded search: the two requested official Python Library pages, plus existing `corpus/SOURCES.md` rows for their canonical URLs. Identified 2, screened 2, included 2, excluded 0. Stop rationale: the official API docs directly state the requested contracts; no broader locale or timezone claim is made.
- Command executed: `date --iso-8601=seconds` — exit 0; output `2026-10-21T09:02:39-03:00`.
- No source registry edits, installs, builds, tests, or other checks were performed.

## Confidence and remaining limit

High confidence in the quoted API facts, URLs, version, footer, and current-date access: all were observed directly on the official pages. The locale source grounds Python's `LC_ALL` API/category and user-default request; it does not by itself establish that an arbitrary process actually received or honored particular environment values. The `used-by` knowledge entry is not present yet, so the `mined` status remains conditional on the planned citation.