done — live source scouting complete; proposed rows and located quotes recorded below. `corpus/SOURCES.md` was not modified.

## Findings

- **S079 candidate, TZ:** Node.js Command-line API, §Environment variables → `TZ` (`#tz`). The live v26.12.1 page says `TZ` specifies the timezone configuration, lists basic timezone IDs, and its history states that changing `process.env.TZ` changes the timezone on POSIX since v13.0.0 and Windows since v16.2.0. This is a primary, in-scope source for the Node timezone profile axis.
- **S080 candidate, Intl:** Node.js Internationalization support, §Embed a limited set of ICU data (`small-icu`). Its example says an output can depend on the user's default locale when Spanish locale data is unavailable. This is narrower than evidence that `LANG`/`LC_ALL` select the default locale: the page does not establish that environment-variable mapping. The proposed scope and teaching below deliberately do not claim it does.
- **URL duplicate check:** searched `corpus/SOURCES.md` for `https?://nodejs\.org/api/|nodejs\.org/api/`; the specialized search returned “No matches found.” The registry's Id allocation section says the next unused ID is S079, so the proposed IDs are S079 and S080.
- **Open/version evidence:** both live pages identify Node.js **v26.12.1** in the rendered title and `meta-nodejs.org:node-version`. At **2026-10-21T12:11:22Z**, `curl -sSI` returned HTTP/2 200 for both. Response `Last-Modified`: CLI page `Wed, 21 Oct 2026 07:34:25 GMT`; Intl page `Wed, 21 Oct 2026 07:34:28 GMT`. The reader exposed the version metadata, not a separate footer string.
- **Status/consumer caveat:** the proposed `mined` rows name the C2 target consumer `corpus/knowledge/hermetic-env-differential.md`. Under the SOURCES contract, retain `mined` only if that entry is actually created and cites the corresponding row; this scout report is not itself a `used-by` knowledge citation.

## Proposed rows (draft only; 11-column registry shape)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S079 | Environment variables: `TZ` (Node.js Command-line API) — https://nodejs.org/api/cli.html | docs | A | Node.js `TZ` timezone selection and documented runtime updates through `process.env.TZ`; not every libc `TZ` extension | §Environment variables → `TZ` (`#tz`), including History @ Node.js v26.12.1 docs, fetched 2026-10-21 | `TZ` selects timezone configuration; Node documents basic timezone IDs and records `process.env.TZ` timezone updates on POSIX (v13.0.0) and Windows (v16.2.0), grounding a timezone environment-profile axis | mined | 2026-10-21 | on-release | corpus/knowledge/hermetic-env-differential.md |
| S080 | Internationalization support (Node.js) — https://nodejs.org/api/intl.html | docs | A | Node.js `Intl.DateTimeFormat` behavior in `small-icu` when non-English locale data is unavailable; not how environment variables select the default locale | §Embed a limited set of ICU data (`small-icu`), example output comment @ Node.js v26.12.1 docs, fetched 2026-10-21 | The `small-icu` example documents locale-dependent fallback output; it supports measuring Intl output under profiles but does not identify the source of the default locale | mined | 2026-10-21 | on-release | corpus/knowledge/hermetic-env-differential.md |

## Located verbatim quotes (each ≤25 words)

1. **S079**, `https://nodejs.org/api/cli.html#tz`, §Environment variables → `TZ`, History table, v13.0.0 row: “Changing the TZ variable using process.env.TZ = changes the timezone on POSIX systems.” (12 words.)
2. **S079**, same page/section, prose after the History table: “The `TZ` environment variable is used to specify the timezone configuration.” (11 words.)
3. **S080**, `https://nodejs.org/api/intl.html`, §Embed a limited set of ICU data (`small-icu`), example comment: “// Prints either "M01" or "January" on small-icu, depending on the user’s default locale” (13 words.)

## Commands and evidence

- `date -u '+ACCESS %Y-%m-%dT%H:%M:%SZ' && curl -sSI https://nodejs.org/api/cli.html | tr -d '\r' && echo '--- intl ---' && curl -sSI https://nodejs.org/api/intl.html | tr -d '\r'` — bash tool succeeded (exit 0); access time was 2026-10-21T12:11:22Z and both responses were HTTP/2 200, with the Last-Modified headers above.
- Read live URLs `https://nodejs.org/api/cli.html#environment-variables`, `https://nodejs.org/api/process.html#processenv`, and `https://nodejs.org/api/intl.html` — reader returned v26.12.1 content. The process fragment did not focus the section; the targeted CLI search below located TZ.
- Specialized search `pattern: TZ|time.zone|timezone|locale`, `path: https://nodejs.org/api/cli.html` — returned the TZ section and history rows (no numeric exit code exposed by this tool).
- Specialized search `pattern: default locale|locale.*environment|environment.*locale|LANG|LC_ALL`, `path: https://nodejs.org/api/intl.html` — returned the small-ICU example's default-locale comment; no numeric exit code exposed.
- Specialized search `pattern: https?://nodejs\.org/api/|nodejs\.org/api/`, `path: corpus/SOURCES.md` — “No matches found” (no numeric exit code exposed).
- No packages/tools were installed or updated.

## Remaining unknowns

- The opened Node.js Intl page does not say whether or how `LANG` or `LC_ALL` controls Node's default Intl locale. Do not attribute that behavior to this page; the F5 profiles' observed tuples must establish what the runner actually varies.
- The Intl quote is specifically an example for `small-icu`; it should not be generalized to official full-ICU Node binaries without separate evidence.
