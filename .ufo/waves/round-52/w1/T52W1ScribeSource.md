# T52W1ScribeSource — one primary source on test hermeticity, one SOURCES row

Seat: leaf scribe (L1 TameshiR52, wave 1). Item: open a primary source on test
hermeticity this round, snapshot it, locate a verbatim quote, draft one row in the
11-column census schema of `corpus/SOURCES.md`, and draft lesson lines for
`corpus/lessons/round-52.md`.

Lane state at read time, read-only: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse --short HEAD`
→ `1f72d7d`; the assignment's base is `ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4` and the C1
frozen counter names that same base (`.ufo/evidence/round-52/c1/measure.py:27`). No lane file was
edited; nothing was committed, added, stashed or checked out. No tool was installed.

## 1. Source opened

- URL: https://bazel.build/basics/hermeticity — Bazel Documentation, "Hermeticity", under
  *Build system basics*.
- Fetch: `curl -sS -L -o bazel-hermeticity.html -w 'HTTP=%{http_code} SIZE=%{size_download} URL=%{url_effective}\n' https://bazel.build/basics/hermeticity`
  → `HTTP=200 SIZE=126546 URL=https://bazel.build/basics/hermeticity`.
- Rendition used for the snapshot: the page's own markdown alternate, declared in the HTML head as
  `<link rel="alternate" type="text/markdown" href="/basics/hermeticity.md">`
  (`grep -o 'rel="alternate" type="text/markdown" href="[^"]*"' bazel-hermeticity.html`) —
  `https://bazel.build/basics/hermeticity.md`, `HTTP=200 SIZE=5878`; a second fetch was byte-identical
  (`cmp bazel-hermeticity.md md2 && echo BYTE_IDENTICAL` → `BYTE_IDENTICAL`).
- Access time: 2026-10-27T05:15Z UTC (`date -u` at the same session read 2026-10-27T05:16:58Z).
- Revision pin: the page is the unversioned default doc (no `/versions/<x.y>/` path); the HTML carries
  `"lastModified":"2026-10-20T15:33:42.788Z"` and `"originalFileLocation":"basics/hermeticity.mdx"`
  (`grep -o '"lastModified":"[^"]*"' bazel-hermeticity.html`). The anchor names that timestamp.
- sha256:
  - snapshot `T52W1ScribeSource-snapshot.txt` (5878 bytes) —
    `2355150f5e9b08c392de169a67b788f4b3f0c446919a8abea9180bf9daccbbc6`
  - opened HTML (126546 bytes) —
    `155fe288e24de47b01023d5292cec9c155ecfef1884bbccedcc7d5f9556f122c`
- Snapshot path: `.ufo/waves/round-52/w1/T52W1ScribeSource-snapshot.txt` (the markdown rendition,
  verbatim; nav/boilerplate absent). Quote line numbers below are lines of that file.

Alternative source was not needed; the Bazel page answered on the first fetch (no fallback to the
Google Testing Blog "Hermetic Servers" post).

## 2. Located quotes (verbatim, ≤25 words each, whitespace-normalised over the file's wrapped lines)

Checked mechanically: normalise each non-blank line, join with single spaces, `str.find`, and count
words — all five hits, all ≤25:

| quote | words | snapshot lines |
|---|---|---|
| "hermetic build system always returns the same output by isolating the build from changes to the host system" | 18 | 12-14 |
| "In order to isolate the build, hermetic builds are insensitive to libraries and other software installed on the local or remote host machine" | 23 | 16-17 |
| "This makes the build process self-contained as it doesn't rely on services external to the build environment" | 17 | 19-20 |
| "Hermetic build systems try to ensure the sameness of inputs" | 10 | 28-29 |
| "Execute a build within a docker container that contains nothing but the checked-out source tree and explicit list of host tools" | 21 | 77-78 |

The first quote is the definition; the second and third give isolation from the host; the fourth gives
input identity (the "declared inputs" half); the fifth is the page's own operational test — a container
holding only the source tree and an *explicit list* of host tools, so any dependency missing there was
an undeclared input.

## 3. SOURCES row (draft, S274)

Validated as a single line: `awk -F'|' '{print "NF="NF}' row.txt` → `NF=13` (11 columns), no `|`
inside any cell, id free (see §5).

| S274 | Hermeticity (Bazel Documentation) — https://bazel.build/basics/hermeticity | docs | A | what "hermetic" asserts for a build or test run: isolation from the host machine and identity of every declared input | §Overview, §Identifying non-hermeticity and §Troubleshooting non-hermetic builds @ https://bazel.build/basics/hermeticity (unversioned default docs page, lastModified 2026-10-20T15:33:42.788Z), fetched 2026-10-27T05:15Z UTC (snapshot lines 12-14, 16-17, 19-20, 28-29, 77-78): HTML HTTP 200, 126546 bytes, SHA-256 155fe288e24de47b01023d5292cec9c155ecfef1884bbccedcc7d5f9556f122c; markdown rendition https://bazel.build/basics/hermeticity.md HTTP 200, 5878 bytes, SHA-256 2355150f5e9b08c392de169a67b788f4b3f0c446919a8abea9180bf9daccbbc6, two fetches byte-identical; snapshot .ufo/waves/round-52/w1/T52W1ScribeSource-snapshot.txt | Quotes (each at most 25 words), the definition: "hermetic build system always returns the same output by isolating the build from changes to the host system"; host independence: "In order to isolate the build, hermetic builds are insensitive to libraries and other software installed on the local or remote host machine"; self-containment: "This makes the build process self-contained as it doesn't rely on services external to the build environment"; source identity: "Hermetic build systems try to ensure the sameness of inputs"; the declared-input test: "Execute a build within a docker container that contains nothing but the checked-out source tree and explicit list of host tools" | mined | 2026-10-27 | 180d | corpus/lessons/round-52.md |

Field grounding against the contract in `CORPUS.md:64-170` ("SOURCES.md — where a shokunin learns"):
`kind=docs` and `tier=A` (official documentation, primary for its own scope; `community` never A and not
used here); `scope` bounded to what the page itself asserts; `anchor` names sections, revision timestamp,
byte counts and hashes — never the bare homepage; `status=mined` because `used-by` cites one path
(`CORPUS.md`: mined = cited by ≥1 used-by path); `recheck=180d` for fast-moving vendor docs (the page's
`lastModified` is 2026-10-20, seven days old at open); `used-by` is the lesson this round writes.

## 4. Lesson lines for `corpus/lessons/round-52.md` (draft)

- **S274 (Bazel, "Hermeticity") — where a selftest stops being hermetic.** A hermetic build system
  "always returns the same output by isolating the build from changes to the host system"
  (S274, §Overview, snapshot lines 12-14): the outcome must be a function of declared inputs only, so
  "insensitive to libraries and other software installed on the local or remote host machine"
  (lines 16-17) and "self-contained as it doesn't rely on services external to the build environment"
  (lines 19-20).
- Routed defect R51.4 sits exactly on that line: `tools/registry.json` is rebuilt by a selftest whose
  fixture writes its own repo, but `tools/round21-measure.py:77-84` reads a `FLEET` literal out of
  `.ufo/evidence/round-21/c2-count.py:19`
  (`FLEET = Path("/home/vgpnk/Projects/shokunin")`) and then runs
  `git -C <fleet>/<repo> show <rev>:<path>` on a sibling repo that the fixture repo never contains.
- That is a *declared* input only if it is written down as one; it is not in the fixture's inputs, so
  the selftest is fleet-bound, not hermetic — its verdict moves with the host's filesystem, and the page's
  own test for this is the container holding "nothing but the checked-out source tree and explicit list of
  host tools" (lines 77-78): whatever is absent there must be absent from the test.
- The sign of it is cheap to see: on this host
  `TMPDIR=$S python3 tools/round21-measure.py --selftest` printed
  `ROUND21_MEASURE_SELFTEST: 13/13 pass`, exit 0 (probe, not a verdict) — the dependency is invisible
  exactly where the fleet root exists, and the frozen C1 counter has to clone the lane outside it
  (`.ufo/evidence/round-52/c1/measure.py` component C, "a fresh clone outside the fleet root:
  a self-test that reads sibling repos through ROOT.parent fails there").
- Repair direction: either make the sibling blobs a materialised fixture input (write the pinned blobs into
  the fixture and read them there) or declare the case fleet-bound in a row class the counter scores —
  and the file's own docstring already states the condition to remove: "the selftest is fleet-bound,
  not hermetic" (`tools/round21-measure.py:9-12`).

## 5. Findings

F1. The source opened clean on the first attempt — no unreachable-URL fallback was needed.
    `curl -sS -L -o bazel-hermeticity.html -w 'HTTP=%{http_code} SIZE=%{size_download} URL=%{url_effective}\n' https://bazel.build/basics/hermeticity`
    → `HTTP=200 SIZE=126546`. Evidence: snapshot + receipt in §1.

F2. The page offers a markdown rendition that is byte-stable across two fetches, which is what the
    snapshot uses; the HTML body's compiled paragraph carries the same sentences
    (HTML `"mdxSource"` block: "a hermetic\nbuild system always returns the same output by isolating the
    build from changes\nto the host system"), so the quote is not a transcription artefact.
    Command: `python3` whitespace-normalised `str.find` over the snapshot, 5/5 hits, §2 table.

F3. Row shape is census-clean on its own: 13 awk fields (`NF=13`), no embedded `|`, one line.
    Command: `awk -F'|' '{print "NF="NF}' row.txt` → `NF=13`; `grep -c '|' row.txt` → `1` (the row line).

F4. Id S274 is free: the only occurrence in the registry is the bookkeeping line itself.
    Command: `grep -rn 'S274' corpus/SOURCES.md` → `502:- Next unused id: S274 (staged ids S161-S255 stay
    reserved by document for the package).` No registry row and no duplicate.

F5. The fleet-bound mechanism the lesson describes is present at base and self-documented:
    `tools/round21-measure.py:9-12` ("The c2 fixture reads the pinned sibling blobs at the fleet root that
    the subject counter itself reads (its `FLEET` literal), so the selftest is fleet-bound, not hermetic,
    ... round 52, routed defect R51.4"), `:26` `ROOT = Path(__file__).resolve().parents[1]`,
    `:77-84` the `FLEET` regex plus `git -C str(fleet / surface["repo"]) show ...`; and
    `.ufo/evidence/round-21/c2-count.py:19` `FLEET = Path("/home/vgpnk/Projects/shokunin")`,
    `:52` `blob = show(FLEET / frozen["repo"], want_rev, frozen["path"])`. The routing line is
    `corpus/lessons/round-51-verifier-spotcheck.md:129` ("Either make `tools/round21-measure.py --selftest`
    hermetic or give the counter a declared fleet-bound row class (R51.4)"). Commands:
    `grep -n 'ROOT\|parent\|sibling\|fleet' tools/round21-measure.py`, `grep -n 'FLEET'
    .ufo/evidence/round-21/c2-count.py`, `grep -n 'R51.4' corpus/lessons/round-51-verifier-spotcheck.md`.

F6. Probe (not a verdict): the selftest passes on this host, which is the non-hermetic signature, not a
    counter result. Command and output:
    `TMPDIR=$S HOME=$S timeout 180 python3 tools/round21-measure.py --selftest` →
    13 `MEASURE_CASE ... PASS` lines, `ROUND21_MEASURE_SELFTEST: 13/13 pass`, `EXIT=0`.
    (The frozen C1 counter's case list is the 11 literals at base, `.ufo/evidence/round-52/c1/measure.py:35-38`;
    the file at lane HEAD has 11 static `check(` call sites — 9 named literals plus
    `claim + "-unknown-rev"` and `claim + "-usage"` inside a `for claim in SCRIPTS` loop
    (`grep -n 'check(' tools/round21-measure.py`, lines 101-138) — hence 13 cases at runtime.
    Reported as observed, not scored.)

## 6. Known limits / out of scope

- `corpus/lessons/round-52.md` does not exist yet (`ls corpus/lessons/round-52*.md` → `No such file or
  directory`; the newest are `round-51.md`, `round-51-verifier-spotcheck.md`). So S274's `mined` status
  rests on a used-by path the L1 writes in this round; the frozen census check "mined rows whose used-by
  paths do not exist — must print nothing" (`CORPUS.md`, Census block) will flag it until that file lands.
  The row is drafted exactly as the item specifies, and this is the single conditional in it.
- Not mine, flagged for the L1: appending S274 to `corpus/SOURCES.md` also needs (a) the registry row count
  and the `- Next unused id: S275 …` line updated, (b) a "Round 52" bookkeeping line in the tail log, and
  (c) the round lesson's `## Gate` entry carrying "URL, the access date, and a ≤25-word quote with its
  location" for the new row (`CORPUS.md` rule 1). The census (`scripts/sources-census.sh validate`) and the
  `tools/staged-id-guard.py` check were not run here: the lane is read-only for this seat and a row that is
  not yet in the file would not be scored by either.
- The quote about the page being "unversioned" is an observation from the fetched HTML
  (`navMaps.firstHrefInVersion.HEAD.href = /basics/hermeticity`), i.e. HEAD-default docs; a versioned URL
  under `/versions/9.3.0/...` would be a different anchor if the L1 wants a pinned one.
- Scratch `/fast/scratch/hyaku/tameshi-r52/T52W1ScribeSource` held the two fetches and the row candidate;
  its content is snapshotted into `T52W1ScribeSource-snapshot.txt` here and the directory is removed.
  Nothing was written under `/tmp` beyond the selftest's own `TMPDIR` (which pointed into scratch).

## Summary
- Bazel "Hermeticity" (https://bazel.build/basics/hermeticity) opened 2026-10-27T05:15Z, HTTP 200,
  126546 bytes; snapshot `.ufo/waves/round-52/w1/T52W1ScribeSource-snapshot.txt` (5878 bytes,
  sha256 2355150f5e9b08c392de169a67b788f4b3f0c446919a8abea9180bf9daccbbc6).
- Five verbatim quotes located by whitespace-normalised search, 18/23/17/10/21 words, snapshot lines
  12-14, 16-17, 19-20, 28-29, 77-78 — the definition, host isolation, self-containment, input identity,
  and the declared-input container test.
- S274 row drafted in the frozen 11-column schema: `docs`, tier A, mined, opened 2026-10-27, recheck 180d,
  used-by `corpus/lessons/round-52.md`; `awk` NF=13, no embedded pipe, id free (`grep -rn S274` → only
  the bookkeeping line at `corpus/SOURCES.md:502`).
- Lesson draft separates hermetic from fleet-bound: `tools/round21-measure.py:77-84` +
  `.ufo/evidence/round-21/c2-count.py:19` read a sibling repo at a hard-coded fleet root — an undeclared
  input; the page's container test (lines 77-78) is the test for exactly that.
- Probe, not verdict: `--selftest` on this host printed 13/13 pass, exit 0 — the dependency is invisible
  where the fleet root exists.
- Known conditional: `corpus/lessons/round-52.md` does not exist yet, so the `mined` used-by path resolves
  only when the L1 writes it; registry append and the `## Gate` quote record are the L1's moves, not this seat's.
