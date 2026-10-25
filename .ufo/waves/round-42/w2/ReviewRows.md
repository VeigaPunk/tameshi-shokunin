# ReviewRows — round 42 wave 2 (FALSIFY): rows S155–S158 and the round-42 SOURCES note

Seat: `L1Tameshi42.ReviewRows` (reviewer, read-only). Date 2026-10-25.
Attacked: `corpus/SOURCES.md` rows S155–S158 (lines 125–128) and the round-42 note (lines 446–448),
checked against `/home/vgpnk/Projects/shokunin/CORPUS.md` §"SOURCES.md — where a shokunin learns"
(schema 86–108, rules 110–129, census 131–148).
Revision: the lane worktree `corpus/SOURCES.md` is byte-identical to `a21845f` —
`diff <(git show a21845f:corpus/SOURCES.md) corpus/SOURCES.md && echo "worktree == a21845f"` → `worktree == a21845f`.
No counter (`measure.py`) was run. Tools installed: none.

## Findings (by severity)

### F1 — HIGH — S157 has no Gate record; its only citing entry is not admitted by the Gate (CORPUS rule 1 and rule 4)

- CORPUS.md:111–114 (rule 1): "The round lesson's `## Gate` records, for every new row, the URL, the access
  date, and a ≤25-word quote with its location grounding `teaches`."
- `corpus/lessons/round-42.md:10` says "One entry admitted, one refused, one left unadopted". The only Admit
  section is `:17` "### Admit — `corpus/knowledge/pit-outcome-vocabulary.md` (S155, S156, S158; S001 held)".
  It records quotes for S155 (`:19–23`), S156 (`:24–27`), S158 (`:28–35`) and S001 (`:36–37`), but nothing for S157.
- `grep -nE 'S157|r42-attribute|argparse' corpus/lessons/round-42.md` gives only three hits: `:76` "S157 and S158
  are new rows, not from the package." and the used-by log at `:90`/`:92`. There is no URL, no access date, no
  quote, and no admit verdict for `corpus/knowledge/r42-attribute-and-outflag-destinations.md`.
- S157's `used-by` cell (field 12) is `corpus/knowledge/r42-attribute-and-outflag-destinations.md` and nothing
  else. So S157 is the one appended row whose only citing entry has no admit verdict in the round's Gate.
  Rule 4 requires appended rows to be cited by admitted entries; this one isn't, as far as the lane's admission
  record shows.
- The records contradict each other. `LOG.md` round-42 section, line 31–33 of the block: "Two entries admitted:
  `corpus/knowledge/pit-outcome-vocabulary.md` and `corpus/knowledge/r42-attribute-and-outflag-destinations.md`".
  The lesson Gate says one.
- The grounding material exists only in wave-1 seat reports, not in the lesson:
  `.ufo/waves/round-42/w1/ScoutArgparse.md:16` and `.ufo/waves/round-42/w1/ScribeRows.md:19` (the 15-word §dest quote).
  I re-located it in the snapshot: `sed -n 1504,1505p .ufo/evidence/round-42/sources/python-argparse.html | sed -E 's/<[^>]+>//g'`
  → "For optional argument actions, the value of dest is normally inferred from / the option strings."
- Repair (for the L1, not done here): add an `### Admit — r42-attribute-and-outflag-destinations.md (S157, S158; S001, S153 held)`
  block to the Gate with S157's URL, the 2026-10-25 access date and the located quote, and correct `:10` to "two entries admitted".
  The other option is to withdraw S157.

### F2 — MEDIUM — S158 `teaches` claims more than the pinned file shows

- S158 field 8: "PIT marks RUN_ERROR and TIMED_OUT as detected and maps a non-zero child exit that is not out of
  memory or a timeout to RUN_ERROR, **so its score counts run errors as detections**".
- The first two clauses hold in the snapshot: `cat -n pit-DetectionStatus.java` → `37 TIMED_OUT(true),`,
  `63 RUN_ERROR(true),`, `91–98 getForErrorExitCode … else return DetectionStatus.RUN_ERROR`, `108 isDetected()`.
- The score clause is not in this file: `grep -niE 'score' pit-DetectionStatus.java` → `no 'score' in DetectionStatus.java`.
  The score is summed elsewhere, in upstream `pitest-entry/src/main/java/org/pitest/mutationtest/statistics/ScorePrecursor.java`
  at the same commit, lines 44–45: `a -> a.getStatus().isDetected()`. Command:
  `curl -fsSL https://raw.githubusercontent.com/hcoles/pitest/f7fe5adf…/pitest-entry/src/main/java/org/pitest/mutationtest/statistics/ScorePrecursor.java | grep -n isDetected`
  → `36`, `44`, `45`.
- So the claim is true, but the row's anchor ("enum constants RUN_ERROR and TIMED_OUT, isDetected() and
  getForErrorExitCode()") does not carry it. That breaks CORPUS.md:101 ("`teaches` — one grounded learner benefit").
  The S158 Gate quote (`round-42.md:33`, "`RUN_ERROR(true),`") grounds only the first clause.
- Repair: drop the "so its score…" clause, or cite `ScorePrecursor.java:44–45` (a separate pinned row or an anchor extension).

### F3 — LOW — Gate quotes ground only part of `teaches` for S156 and S158

- S156 field 8, second half: "a mutant may time out on one run and be killed or survive on another". The Gate
  (`round-42.md:24–27`) quotes only line 293. The supporting text is at `pit-faq.html:298–299` (§Timeouts, `:295`):
  "so a mutant may be detected as timed out on one run, / but killed or surviving on another."
  The row's anchor names §Timeouts, so the grounding exists, but the Gate does not record it.
- For S158, `TIMED_OUT(true)` (line 37) and `getForErrorExitCode` (91–98) are in `teaches` but not in the Gate.
  They are quoted in `corpus/knowledge/pit-outcome-vocabulary.md:33–34`.

### F4 — LOW — the round-42 note's counts carry no command, and no round-end census is recorded

- CORPUS.md:34 says "A count carries its command". `corpus/SOURCES.md:446` says "Rows 109 → 113" and `:447` says
  "registry ids 109 … staged ids 103" with no command. The round-41 note does it right: `:443` has a "Census:" line
  with round-start and round-end `sources-census.sh validate` results.
- Round-end receipt: `ls .ufo/evidence/round-42/census-sources/` → `start.exit start.stdout` only. There is no end receipt.
- I re-ran it read-only: `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` →
  exit 0, 9 × W04 + 1 × W01 (the same set as `start.stdout`), `tameshi ok`. The result is clean; it just isn't recorded.

### F5 — LOW — the collision note reports only the pre-append set

- `corpus/SOURCES.md:447` reports 2 collisions (S153, S154), measured before the append. After the append, the collisions are:
  `comm -12 <(grep -oE '^ {0,3}\| *S[0-9]{3,}' corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -u) <(sort -u .ufo/waves/round-42/assimilation/staged-ids)`
  → `S153 S154 S155 S156 S157 S158` (6).
- `round-42.md:58` already flags one of them (`staged:S156` is arXiv 2406.09843, not the lane's S156). The note
  should give the post-append set to the next assimilation round as the hazard to resolve, the way the round-41 note did.

### F6 — LOW (lane-wide, not specific to round 42) — no Search-log note for the two new searches

- CORPUS.md:126–128 (rule 5) asks for one prose note per bounded search. S157 and S158 are new rows (not from the
  package), but `## Search log` (`corpus/SOURCES.md:136–249`) has no round-42 note. Its last dated note is from round 21.
  The lane has recorded searches in the `## Id allocation` notes instead since round 22, so this is drift that predates this round.

### Adjacent, out of row scope (reported, not scored here)

- `corpus/knowledge/pit-outcome-vocabulary.md:1–3`: the `source:` trio has S155, S156 and S158 but not S001. The
  Gate says the headline "rests on S158 and S001" (`round-42.md:47`), and the entry cites S001 only in the body (`:35`).
  The kaika rule (CORPUS.md:163–166) wants each external source's `S###` in `source:`. S001's `used-by` is still
  correct, because the entry does cite S001.
- `corpus/knowledge/r42-attribute-and-outflag-destinations.md` places the "Any internal - characters…" quote at
  "Lines 1513–1514". It starts at raw line 1512 (`sed -n 1512p … | sed -E 's/<[^>]+>//g'` → "…initial - character.  Any").

## What held (attacks that failed)

- **Schema and census** (CORPUS.md:131–148, run on the lane file): rows 113, malformed 0, tier `A=101 B=9 C=3`,
  status `mined=85 queued=22 rejected=6`, no duplicate ids, no enum or tier-inflation hits, no missing `used-by`
  paths. Each S155–S158 row has NF=13 and every cell is filled.
- **Row counts**: `git show <rev>:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` gives
  c77c2b7 109, 322b5cd 109, a21845f 113. "109 → 113" is correct.
- **Append-only** (rule 2): the per-cell diff from c77c2b7 to the worktree for S001 and S153 changes only field 12
  (`used-by`). Both changes are logged old→new at `round-42.md:89–92`. No other existing row changed:
  `git diff --stat c77c2b7 a21845f -- corpus/SOURCES.md` → 10+/2−, and the two removed lines are S001 and S153.
- **Snapshots**: `sha256sum` and `wc -c` on `.ufo/evidence/round-42/sources/*` match each row's anchor and
  `sha256.txt`: c51d8423 / 12155 B, ccf6ac49 / 20845 B, 3158c439 / 328434 B, 3bf295ad / 2988 B.
- **S158 tier and kind** (`code`, `A`): correct. CORPUS.md:93–95 names "source code" as tier A for its scope, and
  `code` is the right kind for a single source file. The pin is real:
  `git ls-remote https://github.com/hcoles/pitest refs/heads/master` → `f7fe5adf… refs/heads/master`. Raw at
  that commit: `sha256sum` → `3bf295ad…c6`, 2988 B, byte-identical to the committed snapshot. The GitHub API dates
  commit `f7fe5adf` to 2026-10-14T07:18:34Z ("update readme for 1.30.1"). The URL is pinned to the commit, not a
  branch. One nit: the anchor's revision reads "file fetched 2026-10-25"; the commit appears only in the source
  cell and URL. That satisfies CORPUS.md:99–100 through the commit-pinned URL.
- **S155–S157 tier/kind** (`docs`, `A`): official PIT and CPython docs, scoped to their own vocabulary and
  behaviour. S157's "Python 3.15.1 documentation" title matches the snapshot's `<title>`.
- **Located quotes**: `pit-basic-concepts.html:163,175,179,192`, the `:154` heading "Running the tests", and
  `pit-faq.html:293` say what the Gate quotes. Every quote is 25 words or fewer.
- **Opened date**: `opened-at.txt` is 2026-10-25T09:35:08Z (06:35 −03:00), before integration commit `5f739ac`
  (06:41:37 −03:00), so each row was written in the round that opened it (rule 1, first sentence).
- **Rule 4 for S155, S156, S158**: each is cited in the `source:` trio of `pit-outcome-vocabulary.md`, which the
  Gate admits. The other package candidates (`survivor-classification.md` refused, `mutation-score-semantics-cjk.md`
  not adopted) got no rows: `staged:S163–S166` were not appended. Only F1's S157 fails rule 4.
- **Recheck normalization**: the staged `365d — curl…` cells became `180d`, a valid cadence (CORPUS.md:105–106).
  The stripped commands are kept at `round-42.md:84–87`.

## Residual risk and gaps

- I did not re-fetch pitest.org or docs.python.org live; I relied on the committed snapshots, which is what the
  rows pin. I re-fetched S158 live and it matched.
- I did not check whether `ScorePrecursor` feeds the HTML report's displayed percentage, only that it sums `isDetected()`.
- Scratch: `/tmp/tameshi-r42w2-ReviewRows-*` (3 `git show` copies and 1 raw fetch), deleted before return.

BROKEN: S157 was appended with no round-42 Gate record (URL, access date, located quote) and is cited only by `r42-attribute-and-outflag-destinations.md`, which the Gate does not admit ("One entry admitted", round-42.md:10), so it fails CORPUS rules 1 and 4; S158's `teaches` score clause is not grounded in its pinned file.
