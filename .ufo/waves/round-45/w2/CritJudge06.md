seat: CritJudge06

# Round-45 w2 — C1 falsify review of S026, S095, S105 (freshness)

Inputs read: `.ufo/evidence/round-45/contract.json` (frozen, not edited), the ledger at commit
`ad5942c6e9858af19d00000b58439b321ddfa62b` (`git show ad5942c6:…/freshness/ledger.json` → 73 entries, one
entry each for the three ids), the three committed snapshots `.ufo/evidence/round-45/freshness/sources/S0{26,95,105}.raw.gz`
(present at `ad5942c6`, `git cat-file -e` ok), the registry rows `corpus/SOURCES.md:37` (S026), `:104` (S095),
`:117` (S105), and the author reports `.ufo/waves/round-45/w1/ExecRows04.md`, `ExecRows18.md`, `ExecRows21.md`.
I am not the author of any of the three entries (authors: ExecRows04, ExecRows18, ExecRows21).

## Verdicts

S026 agree — reviewer CritJudge06 — sha equal (today's live fetch, `entry.raw_sha256` and the gunzipped snapshot are all `5d74dd1c…`), the 15-token quote is body text in the post's `articleBody` paragraph about post-submit CI (raw line 1132; identical text at 1097 in the Blogger `text/template` copy) followed by "This causes extra repetitive work", and it states the teaches 84% pass-to-fail clause while the 1.5% rate (line 1095) and the fail-3-times-in-a-row / ignore-flakiness clause (line 1101) are also still live.
S095 agree — reviewer CritJudge06 — sha equal (`1a40ae77…`), the 19-token quote is body text of the "Output comments" section (h2 at raw line 512, quote at 515-516, inside the row anchor's lines 512-519) immediately followed by "The test passes if the test's output matches its output comment", which is exactly the row's Output-comment teaches clause, and the "Examples are compiled (and optionally executed) as part of a package's test suite" clause of teaches is also live.
S105 agree — reviewer CritJudge06 — sha equal (`dda9f57d…`), the 13-token quote is the normative EXIT STATUS list (h4 at raw line 558, `<dl>` at 562-574, quote at 566, inside the row anchor's lines 564-574) introduced by "The following exit values shall be returned:", and it states the three outcomes 0/1/>1 that the row's teaches claims, so it is substantive normative content rather than a fragment that states nothing.

No dispute. All three quotes are 6-25 whitespace tokens (15 / 19 / 13), occur in the counter's normalized
snapshot text, share ≥2 content words with scope+anchor+teaches (6 / 3 / 4 distinct), and are not copied from
the row's own source/scope/anchor/teaches cells (each checked as a normalized substring of the folded row line:
False for all three).

## sha256 comparison (live today vs entry.raw_sha256 vs gunzip snapshot)

```
$ curl -fsSL -A 'Mozilla/5.0' --max-time 90 -o /tmp/tameshi-r45-CritJudge06/S###.live '<url>'   # rc=0 each
S026 236387 bytes  live=5d74dd1c3c75d5ec1b8d53d6a518b4b01ae085f03006f1f44febbb8143e92296  entry=5d74dd1c…2296  gunzip=5d74dd1c…2296
S095  40059 bytes  live=1a40ae77c967d7e203b8d7706784bd6633542ff3583d197d854755233c958178  entry=1a40ae77…8178  gunzip=1a40ae77…8178
S105  33988 bytes  live=dda9f57dac3b2420966b5f4d14417b84dfc76ac7c4bb14ead5e901af86a1de5a  entry=dda9f57d…de5a  gunzip=dda9f57d…de5a
```

Three-way equal for all three rows: provenance confirmed, no dynamic-chrome divergence, so no `--live` fallback
was needed. The live bytes extract identically to the snapshots (`cmp -s` on
`measure.py --extract S###.live` vs `--extract S###.snap`: equal for all three).

## Located context (words either side of the quote)

- S026 (raw line 1132, inside `<div class='post-body'><div class='post-content' itemprop='articleBody'>`):
  "…What we find in practice is that **[about 84% of the transitions we observe from pass to fail involve a flaky test]**! This causes extra repetitive work to determine whether a new failure is a flaky result or a legitimate failure…"
  Same sentence also at raw line 1097 inside `<script type='text/template'>` (line 1088) — the `--extract`
  occurrence is the `<noscript>` copy at 1132, i.e. the rendering a non-JS reader sees, still the article body,
  not a `<title>`/nav/footer/`og:description` (the latter is truncated at line 279 and does not carry the quote).
- S095 (raw lines 512-517): `<h2 id="output-comments">Output comments</h2>` → "What does it mean that the
  `ExampleString` function "passes"? As it executes the example, **[the testing framework captures data written
  to standard output and then compares the output against the example's "Output:" comment.]** The test passes if
  the test's output matches its output comment."
- S105 (raw lines 558-576): `<h4 class="mansect">EXIT STATUS</h4>` → `<blockquote><p>The following exit values
  shall be returned:</p><dl compact>` … **[0 No differences were found. 1 Differences were found. >1 An error
  occurred.]** `</dl></blockquote>` → `CONSEQUENCES OF ERRORS Default.`

## Counter self-check (seat mode, never a measurement)

```
$ python3 .ufo/evidence/round-45/freshness/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev 3310e7be803516ca5934b4e949d91bcec824b179 --check S###.json --snapdir /tmp/tameshi-r45-CritJudge06/snapdir
CHECK S026 verified ok   rc=0
CHECK S095 verified ok   rc=0
CHECK S105 verified ok   rc=0
```
(`--snapdir` holds symlinks `S###.raw -> ../S###.snap`, used because `/tmp` reported `No space left on device`
on `cp` at 17:25 while `df -h /tmp` showed 493M free and 1.6M inodes free — writing was avoided, nothing else
was affected.) The fragment JSONs are the ledger entries verbatim; no deciding `--rev` run was made.

## Notes / residual risk (no dispute)

- S105's quote is a `<dl>` definition list. I checked it against the "bare table/code fragment that states
  nothing" exclusion: the list is introduced by the normative sentence "The following exit values shall be
  returned:" and enumerates exactly the 0 / 1 / >1 semantics the row claims, so it does state the claim.
- S095's anchor records the 2026-10-23 sha `1a40ae77…`, identical to today's bytes — the page is unchanged
  since that fetch, but this round's fetch (2026-10-25) reproduces the same bytes, so the row is genuinely
  re-verified rather than merely re-cited.
- No tools installed (system `curl`, `python3`, `sha256sum` only); pacman untouched (host-wide pause respected).

## Files written

- `/tmp/tameshi-r45-CritJudge06/reviews.json` — `{"reviews":[…]}` with the three `agree` verdicts, `report`
  `.ufo/waves/round-45/w2/CritJudge06.md`, one reason each.
- This report only inside the lane checkout; no lane source, ledger, snapshot, jj or Git state touched.

Report: .ufo/waves/round-45/w2/CritJudge06.md
