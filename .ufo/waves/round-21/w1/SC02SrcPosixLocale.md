done

# POSIX environment-variable source

## Findings

- **Live source:** [POSIX.1-2024 XBD Chapter 8, “Environment Variables”](https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap08.html). Opened with the native web reader on 2026-10-21; local timestamps immediately bracketing the final fetch were **09:13:35–09:13:46 -03:00**. The returned page identifies **The Open Group Base Specifications Issue 8 / IEEE Std 1003.1-2024**. Its footer says “Copyright © 2001-2024 The IEEE and The Open Group”; the reader metadata identifies HTML Tidy for HTML5 5.8.0. No separate page-modified date was exposed.
- **Coverage:** §8.2 gives the locale category precedence order: a defined, non-null `LC_ALL`, then the corresponding defined, non-null `LC_*`, then defined, non-null `LANG`, otherwise the implementation-defined default. §8.3 says `TZ` provides timezone information used to override the default timezone for named time interfaces and various utilities. This is authoritative scope for the F5 profile dimensions, not a claim that every program responds identically.
- **Duplicate check:** case-sensitive `grep` search of `corpus/SOURCES.md` for `opengroup|posix|POSIX` returned no matches. The canonical URL does not duplicate an existing registry row. The registry records **S079** as the next unused ID (lines 233 and 238).

## Proposed registry row (draft only; SOURCES.md was not changed)

| S079 | POSIX.1-2024 XBD Chapter 8: Environment Variables — https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap08.html | spec | A | F5 — POSIX locale-variable precedence and timezone-variable semantics for hermetic environment normalization | §8.2, locale-category precedence order, items 1–4; §8.3, TZ @ The Open Group Base Specifications Issue 8 / IEEE Std 1003.1-2024, opened 2026-10-21 | POSIX specifies first-non-null locale selection (LC_ALL, then corresponding LC_*, then LANG, else implementation-defined default) and defines TZ as timezone information used to override the default timezone | mined | 2026-10-21 | on-release | corpus/knowledge/hermetic-env-differential.md |

`mined` is proposed because this primary specification directly grounds the F5 locale/TZ dimensions; the `used-by` knowledge entry must cite S079 for that status to satisfy the registry contract.

## Located quote evidence

All excerpts below are verbatim lexical excerpts from the live page; each is under 25 words.

- §8.2, `LC_ALL` description: “The value of the LC_ALL environment variable has precedence over any of the other environment variables starting with LC_*” (19 words).
- §8.2, locale-category precedence paragraph: “The values of locale categories shall be determined by a precedence order; the first condition met below determines the value:” (20 words).
- §8.2, precedence item 1: “If the LC_ALL environment variable is defined and is not null, the value of LC_ALL shall be used.” (18 words).
- §8.2, precedence item 2 (excerpt following the listed LC_* category names): “is defined and is not null, the value of the environment variable shall be used to initialize the category that corresponds to the environment variable.” (25 words).
- §8.2, precedence item 3: “If the LANG environment variable is defined and is not null, the value of the LANG environment variable shall be used.” (21 words).
- §8.3, `TZ` description: “This variable shall represent timezone information.” (6 words).
- §8.3, `TZ` description: “and by various utilities, to override the default timezone.” (9 words).

## Commands and evidence

- `date --iso-8601=seconds` — exit 0; observed before the final page read: `2026-10-21T09:13:35-03:00`.
- `date --iso-8601=seconds` — exit 0; observed immediately after the final page read: `2026-10-21T09:13:46-03:00`.
- Native `read` of the URL above — returned the page successfully with `Content-Type: text/html`, `Method: native`, Issue 8 / IEEE Std 1003.1-2024 identification, §8.2 locale precedence, §8.3 TZ text, and the copyright footer. The reader does not expose a process exit code.
- `grep` tool search in `corpus/SOURCES.md`, pattern `opengroup|posix|POSIX` — `No matches found`; the tool does not expose a process exit code.

No package or tool was installed or updated. No disagreement or source-access defect observed.