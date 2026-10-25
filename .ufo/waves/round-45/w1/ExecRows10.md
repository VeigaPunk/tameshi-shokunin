seat: ExecRows10

# ExecRows10 — C1 row re-verification S063, S064, S065 (author)

All rows from `corpus/SOURCES.md` (lines 72–74). Live fetches done 2026-10-25, stored under `/tmp/tameshi-r45-ExecRows10/`. No tools installed or upgraded (used existing `curl`, `python3`, `sha256sum`; none needed). No other lane state touched. The three fragment files remain in `/tmp/tameshi-r45-ExecRows10/` for L1 integration; raw snapshots `S063.raw`, `S064.raw`, `S065.raw` kept there too.

Counter frozen at `3310e7be803516ca5934b4e949d91bcec824b179`; all `--check` runs used that rev.

## S063 — https://git-scm.com/docs/git (SOURCES.md:72)

- `curl -fsSL -A 'Mozilla/5.0'` exit 0; 244227 bytes; sha256 `a43b6eff834ea2eb2f4134c7be57a11c8b26d5a9884e5b331f6d5b99ea1a2f0e`
- CHECK: `CHECK S063 verified ok` (quote fixed once: first quote shared only 1 content word — `overlap 1` — because `GIT_DIR` tokenizes to `git`/`dir`; replaced with the `GIT_CEILING_DIRECTORIES` definition sentence)
- note: The GIT_CEILING_DIRECTORIES paragraph confirms the ceiling bounds the upward repository-discovery walk and does not override an explicit GIT_DIR, grounding the teaches claim that a ceiling is no identity check and an inherited GIT_DIR redirects every git -C.
- fragment:

```json
{"id":"S063","url":"https://git-scm.com/docs/git","opened":"2026-10-25","verdict":"holds","raw_sha256":"a43b6eff834ea2eb2f4134c7be57a11c8b26d5a9884e5b331f6d5b99ea1a2f0e","quote":"it is a list of directories that Git should not chdir up into while looking for a repository directory (useful for excluding slow-loading network directories)","snapshot":".ufo/evidence/round-45/freshness/sources/S063.raw.gz","author":"ExecRows10","note":"The GIT_CEILING_DIRECTORIES paragraph confirms the ceiling bounds the upward repository-discovery walk and does not override an explicit GIT_DIR, grounding the teaches claim that a ceiling is no identity check and an inherited GIT_DIR redirects every git -C."}
```

## S064 — https://bazel.build/basics/hermeticity (SOURCES.md:73)

- `curl -fsSL -A 'Mozilla/5.0'` exit 0; 126131 bytes; sha256 `70e9d811ce19161107f482f2734f0c1f06af499aec1ff4f13cccd6343be3f00d`
- CHECK: `CHECK S064 verified ok`
- note: The live §Identifying non-hermeticity list still names host binaries and absolute paths as non-hermetic inputs, and the Benefits section still ties cache validity to unchanged inputs, so the teaches claim holds.
- fragment:

```json
{"id":"S064","url":"https://bazel.build/basics/hermeticity","opened":"2026-10-25","verdict":"holds","raw_sha256":"70e9d811ce19161107f482f2734f0c1f06af499aec1ff4f13cccd6343be3f00d","quote":"System binaries that differ across hosts (such as /usr/bin binaries, absolute paths, system C++ compilers for native C++ rules autoconfiguration)","snapshot":".ufo/evidence/round-45/freshness/sources/S064.raw.gz","author":"ExecRows10","note":"The live §Identifying non-hermeticity list still names host binaries and absolute paths as non-hermetic inputs, and the Benefits section still ties cache validity to unchanged inputs, so the teaches claim holds."}
```

## S065 — https://docs.python.org/3/library/json.html (SOURCES.md:74)

- `curl -fsSL -A 'Mozilla/5.0'` exit 0; 116112 bytes; sha256 `110b871d2d983f95caf6b20996e5d4c6d48d0842a9f9dbcedffb9345d556b9e3`
- CHECK: `CHECK S065 verified ok`
- note: The live §Infinite and NaN Number Values section still says NaN and infinities are accepted by default as if valid JSON number literals, and the parse_constant parameter is documented to alter that behavior, grounding the teaches claim.
- fragment:

```json
{"id":"S065","url":"https://docs.python.org/3/library/json.html","opened":"2026-10-25","verdict":"holds","raw_sha256":"110b871d2d983f95caf6b20996e5d4c6d48d0842a9f9dbcedffb9345d556b9e3","quote":"Despite that, by default, this module accepts and outputs Infinity , -Infinity , and NaN as if they were valid JSON number literal values","snapshot":".ufo/evidence/round-45/freshness/sources/S065.raw.gz","author":"ExecRows10","note":"The live §Infinite and NaN Number Values section still says NaN and infinities are accepted by default as if valid JSON number literals, and the parse_constant parameter is documented to alter that behavior, grounding the teaches claim."}
```

## Result

Verdict `holds` for all three rows; all quotes located afresh in the live-fetched snapshots' normalized text (6–25 tokens, >=2 shared content words, not copied from row cells); each raw snapshot's sha256 matches `raw_sha256`; all `--check` runs at the freeze rev printed `verified ok`. Fragments and raws are in `/tmp/tameshi-r45-ExecRows10/` for L1 integration.
