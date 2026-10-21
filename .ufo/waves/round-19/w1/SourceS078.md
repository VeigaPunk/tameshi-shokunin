# SourceS078 — re-open of registry row S078 (Linux man-pages: open(2))

Seat: `TameshiR19-2.SourceS078` (scout, round 19 w1, read-only). Date: 2026-10-21.
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin` (`L`). Read revisions: baseline
`7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`; delivered `HEAD` = `refs/heads/master` =
`21e79329f8bdcf01a62be63b3e46db4a7de6b6f9`. The working tree's `corpus/SOURCES.md` and
`corpus/knowledge/guard-kill-closure.md` are byte-identical to `21e7932`.
Scratch: `/tmp/tameshi-r19-S078-w6odJW/` (disposable). Tooling: nothing installed or updated.
I made no registry, production, Git/JJ or sibling edits. The only file written is this report.

## Verdict (advisory)

- **S078 holds.** On 2026-10-21 its anchor quote is verbatim on the live page, and the
  page is byte-identical to round 18's fetch. Its `teaches` matches the page. Tier A is right
  for its narrow scope. The 180-day recheck is not due until 2027-04-18.
- **Do not use it as C1 support.** S078 has no bearing on any of R18-1…R18-5 (verified-at
  metadata, the S008 status line, the five-line arithmetic, the selftest receipt argv/exit,
  the final-revision receipt). The frozen contract lists only S049 as C1's source
  (`.ufo/evidence/round-19/contract.json:14`). Citing S078 for C1 would be citation padding.
- **Keep it and use it in place of S072.** Any round-19 text that restates the O_RDWR/O_TRUNC
  point should cite S078, not S072. No registry change is recommended for C1.
- I found two advisory metadata gaps in the same class as R18-1 and R18-2. Both are outside
  the frozen population and do not change C1's 5/5 (§5). They are routed, not counted.

## 1. Row as registered (observed)

`L/corpus/SOURCES.md:87`, which reads the same at `7243e7f`, `21e7932` and in the working tree
(line sha256 `c78a992daba689da46bff6dd47ebf2b99b3c719d2754fdfd1a13c2658e7c2ecf` in all three):

- source: `https://man7.org/linux/man-pages/man2/open.2.html`
- kind / tier: `docs` / `A`
- scope: "supersedes S072's teaches: what an O_RDWR open is, without the O_TRUNC overstatement"
- anchor: §DESCRIPTION access-mode paragraph and O_TRUNC entry @ Linux man-pages 6.19, re-opened 2026-10-20
- status / opened / recheck: `mined` / 2026-10-20 / `180d`
- used-by: `corpus/lessons/round-18.md`

Round 19 made no S078 cell change, so nothing needs an old→new log entry.
`round-19.md:38-40` says: "No new source rows or tier changes … other source openings are advisory readings".

## 2. Source re-open (observed)

Command, run once:

    curl -sSL --max-time 60 -D headers.txt -o open.2.html \
      -w 'http_code=%{http_code} size=%{size_download} url_effective=%{url_effective}\n' \
      https://man7.org/linux/man-pages/man2/open.2.html && sha256sum open.2.html

Results:

- `http_code=200`, size 76506 B, no redirect. Server `Date: Wed, 21 Oct 2026 05:49:22 GMT`.
- `Last-Modified: Thu, 08 Oct 2026 17:39:35 GMT`, `ETag: "12ada-65d57b70ec3c0"`.
- Body sha256 `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789`. This is byte-identical
  to round 18's fetch (`.ufo/waves/round-18/w2/ReopenS072.md:19`: same sha256, 76506 bytes,
  2026-10-20). The page has not drifted between the row's opening and today.
- Footer: `Linux man-pages 6.19  2026-02-08  open(2)`. The COLOPHON gives tarball
  `man-pages-6.19.tar.gz` from mirrors.edge.kernel.org, fetched 2026-09-09. The colophon is
  man7's own addition ("not part of the original manual page"). Its request to mail
  corrections was treated as page data, not acted on.
- Tag-stripped extraction: `/tmp/…/open.2.txt`, sha256 `c96f67e1…f2d837`; whitespace-normalised
  sha256 `22892fbe…fec4c8f`. My stripping method differs from round 18's, so these digests are
  not comparable to `ReopenS072.md:20`. The raw-body identity above is the drift check.

### Located quotes (access date 2026-10-21, man-pages 6.19)

- **Q1 (10 words)**, §DESCRIPTION ¶5, the paragraph that begins "The argument flags must include
  one of the following access modes":
  "These request opening the file read-only, write-only, or read/write, respectively."
- **Q2 (15 words)**, §DESCRIPTION, the list "The full list of file creation flags and file status
  flags is as follows", entry `O_TRUNC`:
  "If the file is a FIFO or terminal device file, the O_TRUNC flag is ignored."

### Verbatim checks

Each phrase was tested as a substring of the tag-stripped, whitespace-normalised page.

| text | present | note |
|---|---|---|
| Q1 (also S078's anchor quote and `round-18.md:111`) | True | 10 words |
| Q2 | True | 15 words |
| "Otherwise, the effect of O_TRUNC is unspecified." | True | 7 words |
| Full O_TRUNC sentence "If the file already exists and is a regular file and the access mode allows writing (i.e., is O_RDWR or O_WRONLY) it will be truncated to length 0." | True | 28 words: cited by location, not quoted as a source quote |
| S072's 17-word fragment, as quoted at `guard-kill-closure.md:118` | True | still verbatim. The overstatement comes from dropping the conditions, not from changed words (`ReopenS072.md:121-128`) |
| S072's paraphrase "whenever the access mode allows writing" | **False** | absent from the page, which confirms S078's correction |

## 3. `teaches` against the page

| S078 teaches clause | Basis | Class |
|---|---|---|
| "O_RDWR requests read/write access" | Q1 | observed |
| "so an O_RDWR open is write-capable" | Q1 plus success of the open | inference, faithful: the page states the requested mode, not an observed write |
| "and is not recorded as a pure read input" | lane classification policy for the trace collector | inference / design choice, not page text |
| "O_TRUNC truncates only an existing regular file (ignored for FIFOs/terminals, otherwise unspecified)" | O_TRUNC entry, Q2, and the "Otherwise…" sentence | observed. "Only" states a necessary condition; the page also requires a writable access mode |
| "S072's 'whenever the access mode allows writing' overstated the page" | the absence check above | observed |

## 4. Tier and limits

Under the kaika contract (`/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:26-30`),
A means "primary or authoritative for that scope (spec, official docs …)". I read that fleet
file read-only, because `SOURCES.md:4` names it as the contract. Tier A and kind `docs` fit:
this is the man-pages project's own interface documentation, not the POSIX standard.

Limits on what S078 can support:

1. **Requested access only.** The page documents the access mode an open requests. An O_RDWR
   open is not evidence that a write happened.
2. **O_PATH.** §DESCRIPTION, O_PATH entry: "When O_PATH is specified in flags, flag bits other
   than O_CLOEXEC, O_DIRECTORY, and O_NOFOLLOW are ignored." So an `O_PATH|O_RDWR` open is not
   write-capable, and a regex on `RDWR` over-classifies it. That error is in the conservative
   direction.
3. **Access mode 3.** §NOTES › File access mode: Linux's nonstandard mode 3 returns a descriptor
   that "can't be used for reading or writing".
4. **Rendering and version.** man7.org serves an HTML rendering of man-pages 6.19, not kernel
   source. The anchor names version 6.19 but not the footer date (S072 had "(footer
   2026-02-08)"). Under the contract a version is enough, so this is not a defect.
5. **No coverage of round-19 subjects.** The page says nothing about receipts, provenance
   metadata, revision binding, errata or diff arithmetic. It gives zero support to
   R18-1…R18-5 (`contract.json:7-11`).

Round-19 use, checked with the `grep` tool over `.ufo/evidence/round-19` and
`.ufo/waves/round-19/w1` for `S072|O_RDWR|O_TRUNC|open\(2\)`: no matches. Outside planner
JSON and the census W04 lines, nothing in round 19 uses S078.

The census warning `S078 duplicate url … open.2.html across scopes`
(`.ufo/evidence/round-19/census-start.txt:9`) is expected for a supersedes row. The verifier
accepted it (`round-18-verifier-spotcheck.md:157-158`). It is not a defect.

## 5. Advisory observations

These are outside C1's frozen population. They do not reduce 5/5, and they are routed, not counted.

**A1 — S078 `used-by` omits a citing entry.** Observed: the S078 used-by cell is
`corpus/lessons/round-18.md` only. However, `corpus/knowledge/guard-kill-closure.md:163-166`
(EG-4) says "S078 supersedes it" and that the entry's claims "rest on the O_RDWR access-mode
sentence", which is S078's anchor. Both `corpus/README.md:280-281` and
`round-18-verifier-spotcheck.md:214` say guard-kill-closure cites S077/S078.

- Failing criterion: the contract defines `used-by` as "repo-relative paths of the knowledge
  entries or lessons citing the row" (`SOURCES-CONTRACT-v1.md:40-41`).
- S077 has the same pattern (`SOURCES.md:86`).
- Any fix is a mutable-cell change, logged old→new in the round lesson (contract rule 2).
- Confidence: medium-high. It depends on whether a prose "supersedes" mention counts as
  citing. README and the verifier both treat it that way.

**A2 — guard-kill-closure header still routes to S072.** Observed at both `7243e7f` and `21e7932`:

- `guard-kill-closure.md:1` `source:` lists "S072 — open(2) §DESCRIPTION, O_TRUNC" and does not
  list S078.
- `:3` `recheck:` says "Re-open S065–S074 and S063", which leaves out S075–S078.
- EG-4 (`:163`) corrects this only in the body and names neither line.
- R18-1 targets line 2 only (`contract.json:7`; erratum at `:171-190`).

Failing criterion: QUALITY 37 (`corpus/QUALITY.md:334-335`): "A metadata correction names the
exact stale provenance field and line, not merely a body statement on the same subject."

Effect: a recheck that follows line 3 would re-verify S072's fragment. That fragment is still
verbatim (§2), so the recheck would pass without noticing the overstatement.

Unknown: whether a round-19 criterion applies retroactively to a round-18 erratum. This is
the same defect class as R18-1 and R18-2, but not one of the five frozen items.

## 6. Distinctions

- **Observed:** the fetch identity, the quotes and their presence, the row and file bytes at
  three revisions, and the grep results above.
- **Inference:** "write-capable" as a reading of Q1, and the lane's "not a pure read" policy.
  Also A1/A2 as defects, which rests on how the contract and QUALITY 37 are read.
- **Unknown:** the 2026-10-20 fetch time of day (round 18 recorded only the date), and kernel
  behaviour beyond the documented interface.

## 7. Commands and code (read-only)

    # page text extraction (Python, in-session; files under /tmp/tameshi-r19-S078-w6odJW)
    txt = re.sub(r'<script.*?</script>|<style.*?</style>', '', html_text, flags=re.S|re.I)
    txt = re.sub(r'<br\s*/?>', '\n', txt, flags=re.I); txt = html.unescape(re.sub(r'<[^>]+>', '', txt))
    norm = lambda s: re.sub(r'\s+', ' ', s).strip(); present = norm(q) in norm(txt)

    # lane bytes: read-only git, inherited GIT_* removed (none were set),
    # GIT_OPTIONAL_LOCKS=0 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
    git -C L rev-parse --verify REV^{commit}; git -C L for-each-ref refs/heads
    git -C L show REV:corpus/SOURCES.md            # S078 line sha256 per REV
    git -C L show REV:corpus/knowledge/guard-kill-closure.md   # lines 1-3, EG-4, R18-1
    git -C L diff --numstat 7243e7f 21e7932 -- corpus/SOURCES.md corpus/knowledge/guard-kill-closure.md
    #   -> 9/1 SOURCES.md (S049 used-by + search log), 21/0 guard-kill-closure.md (R18-1)
