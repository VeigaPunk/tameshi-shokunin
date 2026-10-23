# ReviewLesson30 — residual review of round-30 lesson, SCORECARD block, LOG block

Seat: `ReviewLesson30`. Target: `corpus/lessons/round-30.md`, the Round-30 block of
`SCORECARD.md` (:1464-1480), and the Round-30 block of `LOG.md` (:1745-1756), all at
`957c5ddb2af61063c8993e8aed1321cb0d54b66a`, checked against committed bytes only.

## Verdict

**Pass with six imprecisions, none blocking.** Every lane path, every lane commit hash,
every digest and every quote I could trace resolves to committed bytes; the monitor,
binding, audit, ledger and selftest numbers are all correct. Six statements are wrong or
unsupported: two quote word counts, one ledger count stale at the pinned commit, one
wave-B provenance claim, one routed-survivor enumeration that misses N05, and two smaller
mismatches in seat-count wording. The five Mistakes rows each carry class, evidence,
captured-by and a fix with a shown-able-to-fail clause; every Gate reject names its reason.

## Findings, by severity

### M1 (medium) — wave-B provenance claim for ConnectorOverlap is unsupported
`corpus/lessons/round-30.md:159-160` (Mistake 4 evidence): "wave C (attempt 3) carries
ConnectorOverlap, RegressionReplayHead and SelftestsNoHarmHead, adapted from attempt 2's
unspawned wave-B spec". Observed:

- `git show 957c5dd…:.ufo/waves/round-30/spec-wB.json | grep -ic 'overlap\|connector'` → `0`
- `git show 957c5dd…:.ufo/waves/round-30/spec-wC.json | grep -c 'ConnectorOverlap'` → `2`
- `git show 957c5dd…:.ufo/waves/round-30/spec-wB.json | grep -oE '"[^"]*(RegressionReplay|SelftestsNoHarm)[^"]*"'` → `"RegressionReplayHead"`, `"SelftestsNoHarmHead"` present.

spec-wB names RegressionReplayHead and SelftestsNoHarmHead but contains no ConnectorOverlap
text; the wave-C ConnectorOverlap item cannot have been adapted from the wave-B spec on
committed bytes. (The sibling claim in the same sentence — the dead wave-A seats —
is supported: `.ufo/evidence/round-30/attempt3/attempt2-dead-seats.txt` lists
ConnectorOverlap, RegressionReplay and SelftestsNoHarm.)
Smallest safe correction: name the actual source of the wave-C ConnectorOverlap item
(wave-A, or state it was new) and keep "adapted from … wave-B spec" only for the two replays.

### M2 (medium) — "The runner is an input of 222 ledger entries" is stale at the pinned commit
`corpus/lessons/round-30.md:210-211`. Observed, computed from
`.ufo/evidence/round-21/coldread/ledger.json` at `957c5dd…` (456 entries, matches
`coldread/append-receipt-wC.json` current_entries=456):

- entries whose `inputs` contain exactly `tools/mutate-and-run.sh`: **270**
- the same count at `bb681566`'s ledger (393 entries): **222**

222 is correct only on the pre-append 393-entry ledger; at the cited head the figure is 270.
The same section uses the current count elsewhere ("0 of 456" for the knowledge entry,
verified: 0 entries list `corpus/knowledge/regression-tally-completeness.md` at 456).
Smallest safe correction: say "222 ledger entries at `bb681566` (270 after wave C's appends)",
or just 270.

### M3 (medium) — routed-survivor enumeration omits N05
`corpus/lessons/round-30.md:125` says "8 real survivors (routed below)" and
`SCORECARD.md:1480` says "Eight selftest survivors of the new guard (MutateHead) … are
routed to round 31". The routed list at `corpus/lessons/round-30.md:207-210` names seven
IDs: T08, N03, H03, H04, H05, N01, N02. `.ufo/waves/round-30/wC/MutateHead.md` reports 11
survivors = 3 equivalent (T07, H01, H02) + 8 real; the eighth real survivor is **N05**
(guard `!= nlegs` → `< nlegs`, "Real guard-test gap under declared overcount stress;
equivalent for the intact nine-operand loop"), named in MutateHead's "Smallest safe
correction" section but absent from the routed list. The knowledge-entry erratum E4 has the
same seven-item enumeration. Either eight are routed (add N05 with its stress bound) or the
counts are seven.
Smallest safe correction: add a clause for N05 or change "8 real survivors (routed below)"
to "7 routed, 1 bounded-equivalent survivor (N05)".

### L1 (low) — two quote word counts are wrong
`corpus/lessons/round-30.md:40` says the S093 located quote is "(15 words)"; the quote at
`.ufo/evidence/round-30/sources/S093-bwrap-0.13.1.xml:159` ("Unshare all possible
namespaces. Currently equivalent with: --unshare-user-try … --unshare-cgroup-try") has **13**
whitespace tokens. `corpus/lessons/round-30.md:45` says the S094 located quote is "(18
words)"; the sentence in `.ufo/evidence/round-30/sources/S094-arxiv-1411.2664v3.pdf`
(`pdftotext`, §1, footer page 2: "Each submitted model is evaluated on a (fixed) test set
that is available only to the organizers.") has **17** words. The S092 count "(9 words)"
(:36) is correct, so the convention is consistent and the two are simply miscounted. Quote
text, locations, sha256s (2cb77df2…/33289 B; 6e9532a9…/322643 B) and the "printed page 2"
locator all verified exact.
Smallest safe correction: 15→13, 18→17, or drop the counts.

### L2 (low) — "five other attempt-2 seats" undercounts the dead-seat file
`corpus/lessons/round-30.md:85`: "Seats CtlS3DenyList and CtlS8TokenBag (and five other
attempt-2 seats) died … recorded dead … in
`.ufo/evidence/round-30/attempt3/attempt2-dead-seats.txt`". The file lists **nine** seats
(CtlS3DenyList, CtlS8TokenBag, CriticC1Axis, CriticHoldRule, CriticV4Design,
ConnectorOverlap, RegistryNoHarm, RegressionReplay, SelftestsNoHarm), headed "attempt-2
control seats with no report". A subset reading of the parenthetical is defensible, but the
file's own header scopes all nine the same way, so "five other" sits inconsistently next to
it; Mistake 4's evidence already names three of the nine separately.
Smallest safe correction: "and seven other attempt-2 seats" or enumerate.

### L3 (low) — "5 edited afterwards by the same seat" includes a non-write creation
`corpus/lessons/round-30.md:12`. `.ufo/evidence/round-30/attempt3/inherited-wA-receipt.txt`
has 23 rows: 18 `last_write_equals_file=True`, 4 `False`, and `MutateTallyExtra` with
`calls=eval, last_write_equals_file=None` — that report was created by an `eval` call, so it
was never "equal to the last write" nor "edited afterwards"; the file is nonetheless by its
own seat, so the parent claim holds. 18+5=23 arithmetic is right; the wording is off for
one row.

## Verified against committed bytes (selected, all at 957c5dd… unless noted)

- **Hashes** (`git cat-file -e`): 9ed6db84, dcdf2d08, e59728df, 8a8d2540, f09d3425,
  713dee6a, bb681566, 07ed440a, 9207f226, a2fa6c92, 4df5107f, 65b6e84f — all present.
  Clone-scoped receipt revs (e606538e…, 8357d0b9…, a94e51a0…, 16a9ad36…, 210db74…,
  1fed832d…) are not lane objects — see Residual risk.
- **Paths**: every cited `.ufo/evidence/round-30/…`, `.ufo/waves/round-30/…`, corpus and
  tools path exists at the pinned commit (full `git ls-tree -r` sweep); `bind-select-v3.py`
  exists at `9207f226` and not at `9207f226^`; its sha256 `6f3a66bb…` equals the hash
  recorded in `attempt3/bind-controls.txt:2`.
- **Counter-jump receipts**: `ctl/CtlK7Keyed.stdout` `C1_R30_PASS=true` exit 0;
  `v4/K8-on-v3.stdout` `PASS=true`; `v4/ctl2/CtlS2SymEval-v4.stdout` `PASS=true` exit 0
  `sealed_killed=6/6 sealed_equiv=6/6` — matches amendment-4's own text.
- **Amendment-4 misstatements confirmed**: amendment-4 records CtlS1Normalize
  `sealed_killed=0/6` and CtlS4Sniff `sealed_equiv=5/6`; receipts read `sealed_killed=6/6
  sealed_equiv=5/6` (`v4/ctl2/CtlS1Normalize-v4.stdout`, rev `e606538e`) and
  `sealed_killed=0/6 sealed_equiv=6/6` (`v4/ctl2/CtlS4Sniff-v4.stdout`, rev `8357d0b9`).
  Both PASS=false — the lesson's gate erratum is accurate.
- **Monitors**: `monitor-at-base.stdout` `covered=64/64 restraint=8 box3_mismatch=0`;
  `head/c1monitor-at-bb681566.stdout` `covered=33/64 restraint=6 box3_mismatch=1` with 31
  `uncovered:` lines (matches "31 drifted sections"); `head/c1monitor-at-4df5107f.stdout`
  and `head/c1monitor-at-65b6e84f.stdout` `64/64 restraint=8 box3_mismatch=0` exit 0.
- **Binding**: `attempt3/bind-controls.txt` matches the lesson's 6-row table cell-for-cell
  (real 32/31, donothing 32/0, promptonly 0/0, textmention 32/0, noresult 32/0, forged
  32/30). CtlBindV3's report supports the five surviving shapes (different_tool,
  error_result, comment_only_shell, result_before_call, reused_call_id — each 31/32 kept)
  and two killed shapes. `bind-receipt-wC.json` assembled 63 / kept 63 / registry 38;
  `audit-bound-wC.out` 211 `ok` rows + `AUDIT: traces_ok=211 traces_fail=0`; every sample
  trace carries `rev: bb681566…`.
- **Ledger**: `append-receipt-wC.json` prior 393 / appended 63 / current 456 /
  `prefix_entries_equal_as_data: true` / `other_top_level_keys_unchanged: true`; ledger
  counts 393 at `bb681566`, 456 at pinned; only `4df5107f` touched the ledger file
  ("landed 4df5107f" ✓). Knowledge-entry inputs: 0 of 456 ✓.
- **JudgeC1.md** carries every value the lesson and scorecard quote: `JUDGE C1:
  unprovable-but-better`, 106/106 pristine, 98/106 mutant selftest, `REGRESSION: SETUP
  (case-tally mismatch: cases=9 counted=8)` exit 2 vs base `REGRESSION: PASS (cases=9
  passed=8 …)` exit 0, sum-preserving miscount paragraph, guard-unreachability paragraph.
- **Selftests**: `SelftestsNoHarmHead.md` — 97/97 base, 106/106 head, every `tools/*.py`
  selftest same exit both revisions (two cells nonzero on both, documented);
  `attempt3/evidence-disposition-selftest.txt` — `SELFTEST: PASS (66/66)` exit 0 at both
  revs; `RegressionReplayHead.md` — `REGRESSION: PASS (cases=9 passed=9 …)` exit 0 and the
  dropped-operand `counted=8` SETUP.
- **SOURCES**: 89 rows at base → 92 at head (S092-S094 appended at :101-103); S087
  `used-by` adds `corpus/knowledge/regression-tally-completeness.md` with status `mined`
  and recheck `180d` unchanged; no commit touched SOURCES after `bb681566` ("no … change
  in attempt 3" ✓); stale `- Next unused id: S092.` at :355 beside new `S095` at :364
  (RerunCensus finding 1) ✓.
- **Digests**: S092 pin `266915c5…` 16210 B equals `sources/S059-bazel-remote-caching.md`
  bytes (verified `sha256sum`, ReopenS092 timestamps 07:14:23Z/07:15:44Z both with that
  hash); `sources/S093-bwrap-0.13.1.xml` = `2cb77df2…` 33289 B; `sources/S094-…pdf` =
  `6e9532a9…` 322643 B; S087 tarball `sha512sum|base64` = the row's `E2i+8bXo…` exactly.
- **Quotes**: `S059:345` "Bazel currently does not track tools outside a workspace." exact;
  `bwrap.xml:159` quote exact; `bwrap.xml:233-235` `--clearenv` keeps PWD and `--setenv`
  items exact (supports the knowledge-entry gate reject); knowledge entry `:42` contains
  "with a cleared environment"; `:60-62` is the S094 paragraph; errata E1-E4 appended
  (:72-75); E1's "PATH, HOME, LANG and TMPDIR" = the four set variables.
- **QUALITY**: criteria 56 and 63 are the round-order rules cited; 58-65 are all "Round 30"
  additions; 60 = binding-to-outside-artifact; 62 = measured-revision receipt rule;
  65 = the verdict-only counter class (Mistake 1's "QUALITY 65 records the class" ✓).
- **README**: `corpus/README.md:449-454` carries the Round-30 section consistent with the
  lesson ("23 fixed status vectors and a guard stress case (97 → 106 cases)").
- **Routed dispositions**: spotcheck item 7 is "Carried items" with the S059 row,
  MutateLegSum and the uncommitted-mtime evidence — matching LOG's "(runner leg-sum defect,
  MutateLegSum; S059 supersedes row)"; `r29-mistake1-ordering.txt` first committed at
  `bb681566`; `c2-at-E.stdout` reads `quote_located=0` and the scorecard C2 row names only
  `7a45f7b9` as measured commit (erratum basis checks out); ReviewRoutedR29's verdicts
  align (the two "partial" items get their missing receipts in attempt-3 commits).
- **Timing**: `a2fa6c92` committer date 2026-10-23T07:14:15Z vs lesson "dispatched at
  07:13Z" (dispatch precedes its record commit — plausible); `4df5107f` at 07:52:47Z vs
  "all returned by about 07:52Z" ✓; `9207f226` at 06:48:53Z is before wave-C dispatch ✓;
  `bb681566` at 06:11:04Z before the 06:19:06Z orchestrator death ✓; amendment-4 written
  06:09Z and committed at `713dee6a` before `bb681566` ✓ (CriticC1Exploratory confirms).
- **Structure**: 38 dispatch-wC `spawn` members, 22 cold-read reports (ColdA01-A11 +
  ColdB01-B11), 63 bound entries over 22 seats, verdict mix gap-minor 35 /
  verified-record 22 / executed-ok 6 — all exact. SHONEN.md holds exactly four `[~]` marks.
  Fleet-root `/home/vgpnk/Projects/shokunin/.ufo/waves/round-30/` absent now (ColdA01's
  self-repaired misroot), consistent with the lesson's sweep claim; ColdA01.md's Errata
  paragraph carries the pgrep/kill disclosure verbatim.
- **Mistakes structure**: all five rows carry **class**, **evidence**, **captured-by**,
  **fix** and a "Shown able to fail" clause; every Gate reject (knowledge-entry overreach,
  amendment-4 receipt summary, binding v2, binding v3 limit) names its reason.

## Residual risk and verification gaps

- **Clone-scoped revs**: the `rev=` fields in counter receipts (e606538e…, 8357d0b9…,
  a94e51a0…, 16a9ad36…, 210db74…, 1fed832d…) resolve to no object in the lane repo; they are
  commits of the disposable sandbox clones the counters were run on. The lesson quotes them
  faithfully as receipt fields, but `git cat-file -e` cannot resolve them by design. The
  receipts are complete evidence of their own fields.
- **Not re-executed**: I did not re-run the runner, counters or the census; correctness of
  claimed outputs is established against committed receipts and seat reports, not fresh
  runs. The attempt-1 death timestamp (05:25:25Z) and the S094 "unversioned URL returns the
  same bytes" claim are attributable assertions, not committed bytes.
- **Unverified claim not counted as finding**: "Read12B named its traces in lower case"
  (`round-30.md:77`) is supported indirectly — `w1/Read12B.md:17-39` names its receipts
  `read12b-*.json` while the pilot peers use `Read11B-*.json` spelling — but no committed
  receipt states the reason for the real-pilot exclusion. The claim is consistent and
  plausible; it is simply not receipt-anchored.

## Tooling

None installed or updated. `pdftotext` (poppler, `/usr/bin/pdftotext`) already present for
the S094 quote check. All verification used read-only git with `GIT_OPTIONAL_LOCKS=0`; no
git write commands, no `jj`, no production edits. One report file written (this file).
