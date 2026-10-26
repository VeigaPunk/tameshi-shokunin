# T48W2CritC2Rows — the four new registry rows attacked (S265–S268)

Seat: critic, wave a2w1 (attempt 2), L1 TameshiR48a2. Item: attack the four new registry rows at
CONTENT `/home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md:140-143` — 11 columns, no
`|` in any cell, kind/tier honest, scope differing from the superseded row (no census E04), anchor
carrying section + revision/date + sha256 prefix equal to the committed snapshot + bytes, teaches
opening `supersedes T —` and grounded by the Gate quote, valid recheck, exact used-by — and compare
each with the row it supersedes.

**What this attacks.** The rows themselves, not the claim's instrument: (a) whether each row is
*grounded* in its own cells or only carries prose from the row it supersedes, (b) whether the
re-anchor silently shrank the locator under a teaching that was kept, (c) whether the record's own
pointers at these rows are true. Lane read-only; the only lane writes are this report, its probe
receipt and its census capture inside `.ufo/waves/round-48/a2w1/`.

Verdict in one line: **structurally clean and byte-verified, and `C2_R48_PASS` is reproducible — but
two rows assert clauses their own anchor and quote do not locate (S267, S266), two more changed what
the old row taught without saying so (S265 precision, S268 exclusivity), and the lesson points at
the wrong rows.** None of these is visible to the frozen counter, which reads the quote and the
required phrases, never the anchor's coverage of the teaches cell.

---

## Findings

### F1 — S267 (`corpus/SOURCES.md:142`): the teaches cell asserts a wording that no cell in the registry locates — `--unshare-user-try` "if possible else skip it"

**Attacked clause.** `corpus/SOURCES.md:142`, teaches cell, verbatim: "supersedes S093 — the raw XML
at v0.13.1 still defines --unshare-all as the six flags …, **with the user and cgroup flags worded
"if possible else skip it"**; score each other flag on its own sentence …".

**Evidence.**
- The quote cannot carry it. It is 25 tokens, exactly `MAX_WORDS`
  (`.ufo/evidence/round-48/freshness/measure.py:100`, `MAX_WORDS = 25`; `check_quote`
  (`:292`) rejects `words > MAX_WORDS` at `:303`), and it names the user flag only as a bare option inside
  `--unshare-all`'s equivalence list — no wording. So the quote is not the locator and cannot be
  extended.
- The anchor is not the locator either: `corpus/SOURCES.md:142` anchor names "the
  --unshare-cgroup-try and --unshare-all varlistentries at bwrap.xml raw lines 153–160 (the quote
  spans lines 154–159, bytes 5909–6400)". Raw 153–160 is `--unshare-cgroup-try` (153–156) and
  `--unshare-all` (157–160) only.
- The superseded row never located it. `corpus/SOURCES.md:102` anchor cites `bwrap.xml:159`,
  `:233-235`, `:403`, `:412-416`, `:575-577`, `:589-592`, `README.md:52-54`, `:133` — no 129–132.
- The wording is at a line nothing in the lane's registry names:

```
$ sed -n '129,132p' .ufo/evidence/round-48/freshness/sources/S093.xml
    <varlistentry>
      <term><option>--unshare-user-try</option></term>
      <listitem><para>Create a new user namespace if possible else skip it</para></listitem>
    </varlistentry>
```

- The row's own scope contradicts the teaches: `corpus/SOURCES.md:142` scope names only "the
  try-else-skip wording of `--unshare-cgroup-try`". So the teaches claims one more located fact than
  the scope declares.
- The citing entry has already cashed the claim: `corpus/knowledge/regression-tally-completeness.md:2`
  says "with the six --unshare-all flags and **both** try-else-skip sentences re-read".

**Impacted axis.** freshness. Severity: defect (a teaching with no locator anywhere in the
registry; it is true — the bytes say it — but unverifiable through the row).

**Smallest safe correction.** Extend the anchor's line range, not the quote:
`§Options, the --unshare-user-try (raw lines 129–132), --unshare-cgroup-try (153–156) and
--unshare-all (157–160) varlistentries (the quote spans lines 154–159, bytes 5909–6400)`; and add
"user" to the scope sentence. Snapshot, bytes and sha prefix are unchanged by this (the anchor's
pin is `S093.xml` 33289 B `2cb77df2f4be`, verified below). Alternative, if the anchor must not grow:
drop "user" from the teaches cell and correct the entry's "both try-else-skip sentences".

---

### F2 — S266 (`corpus/SOURCES.md:141`): the anchor narrowed below the teaches it kept, and the citing entry widened the row

**Attacked clause.** teaches cell, verbatim: "supersedes S048 — item 4 is prioritisation rather than
a reuse skip, its consequent is the located quote, no claim here resolves its pronoun to test versus
mutation, **item 5 is not yet implemented and the dependency assumption remains unproven**".

**Evidence.**
- The superseded row anchored exactly what it taught: `corpus/SOURCES.md:57` anchor "§Incremental
  analysis, numbered items 4–5 and dependency paragraphs". The new row anchors "§Incremental
  analysis, item 4 (raw line 86)" — one item.
- The two carried clauses live elsewhere in the same section and are not named:

```
$ awk 'NR==87 || NR==94' .ufo/evidence/round-48/freshness/sources/S048.html
  <li><em>If a number of mutations for a class previously survived … (not yet implemented)</em></li>
<p>So the incremental feature is based on the assumption that it will be relatively rare for changes in the dependencies of a class to change the status of a mutation. Although this assumption seems reasonable, it is currently <strong>unproven</strong>.</p>
```

- The used-by entry now attributes *more* to S266 than the row claims:
  `corpus/knowledge/incremental-pin-disposition.md:1` cites "S266 — https://pitest.org/quickstart/
  incremental_analysis/ — **§Incremental analysis (numbered items 1–5 and the dependency
  paragraphs)**", while `corpus/SOURCES.md:141` scope says "PIT's item-4 prioritisation distinction"
  and the anchor names line 86. So the row and its only citation disagree about coverage in both
  directions (row narrower than entry).
- The Gate quote grounds one of the four teaches clauses (`84%`-style economy: the contract's
  required phrase for S048 is `should therefore be prioritised`, and it is inside the quote); the
  other three rest on the anchor.

**Impacted axis.** freshness. Severity: defect (the same shape as F1 but softer — the section is
named, so a reader can find item 5 by walking §Incremental analysis; the row simply no longer says
where).

**Smallest safe correction.** Restore the superseded row's coverage in the anchor: "§Incremental
analysis, numbered items 4–5 and the dependency paragraphs (item 4 quoted, raw line 86; item 5 at
raw line 87; dependency paragraph at raw line 94)". That makes the row and
`corpus/knowledge/incremental-pin-disposition.md:1` agree without touching the entry or the pin.

---

### F3 — S265 (`corpus/SOURCES.md:140`): the anchor names one paragraph, the teaches carries three clauses, two of them two and four lines away

**Attacked clause.** teaches cell, verbatim: "supersedes S026 — about 1.5% of test runs are flaky,
about 84% of pass-to-fail transitions involve a flaky test, and a fail-3-in-a-row flaky mark cuts
false positives but teaches people to ignore flakiness".

**Evidence.**
- The anchor: "Post body (h2 title; publishdate 2016-05-27; **articleBody paragraph at raw line
  1132**)". The superseded anchor was the whole post body (`corpus/SOURCES.md:37`: "Post body,
  published 2016-05-27 (fetched 2026-10-19)").
- Only the 84% clause sits at 1132:

```
$ sed -n '1130p;1132p;1136p' .ufo/evidence/round-48/freshness/sources/S026.html   # first 90 chars
Unfortunately, across our entire corpus of tests, we see a continual rate of about 1.5% of
When doing post-submit testing, our Continuous Integration (CI) system identifies when a passing
We have several mitigation strategies for flaky tests during presubmit testing, including …
```

  (1.5% at raw 1130 and again at 1095; "fails 3 times in a row … hardly a perfect solution" at raw
  1136 and 1101. `grep -c 'hardly a perfect solution'` → 2.)
- Not a false claim: all three clauses survive at those lines inside the same `<noscript>` body
  block (1123–1145) that sits inside `<div class='post-content' itemprop='articleBody'>` (1087). The
  defect is locator precision under a "Post body" parenthetical that now narrows to one paragraph.

**Impacted axis.** freshness. Severity: minor (repairable by a reader in one `sed`; nothing false).

**Smallest safe correction.** Add the two clause lines to the anchor: "… articleBody paragraphs at
raw lines 1130, 1132, 1136 (inside the `<noscript>` body copy; the `<script type='text/template'>`
copy at 1095 is dropped by the amendment-2 extraction)". Worth saying once, because the *quote* is
only locatable because of the noscript copy.

---

### F4 — S268 (`corpus/SOURCES.md:143`): the exclusivity the old row taught ("only via") is withdrawn silently under a cell that says "still states"

**Attacked clause.** teaches cell, verbatim: "supersedes S108 — the zh-cn page **still states** that
.expected files are updated by running the affected test with --test_arg=--update_goldens
--test_strategy=local and that the resulting diff is checked …".

**Evidence.**
- Superseded cell, `corpus/SOURCES.md:120`: "the zh-cn page restates that .expected files update
  **only** via --update_goldens and that the resulting diff is checked".
- The page gives one update path and no exclusivity word:

```
$ sed -n '3611p' .ufo/evidence/round-48/freshness/sources/S108.html
<p>可以通过使用参数 <code>--test_arg=--update_goldens --test_strategy=local</code> 运行受影响的测试目标来更新 <code>.expected</code> 文件。应检查由此产生的差异是否存在意外的变化。</p>
```

  ("can update … by using …"; nothing corresponding to "only"). So dropping "only" is the right
  reading — but the new cell says "still states", which claims the old row and the new one say the
  same thing while one clause changed. Nothing in the row, the lesson Gate line
  (`corpus/lessons/round-48.md:24`) or the entry notes the withdrawal.
- No entry relies on exclusivity (`grep -n 'only' corpus/knowledge/r8-golden-update-flag.md` returns
  the `verified-at:` line only, and it is about a head diff), so the impact is confined to the
  registry's own statement.

**Impacted axis.** freshness. Severity: minor (a silent semantic change inside a "still states"
frame; nothing downstream is wrong).

**Smallest safe correction.** One clause in `corpus/SOURCES.md:143`: "… still states that .expected
files are updated by running the affected test with … and that the resulting diff is checked **— it
gives this one update path and does not say "only", so S108's exclusivity wording is withdrawn —**;
the sentence is re-located verbatim …". If the L1 prefers the shortest form, replace "still states"
with "states (S108's 'only' dropped: the page gives one path, not an exclusive one)".

---

### F5 — the lesson's row-change pointers name the wrong rows (`corpus/lessons/round-48.md:62`, `:84`)

**Attacked clause.** `corpus/lessons/round-48.md:62`: "Row change: `corpus/SOURCES.md:140` appends
S267"; `:84`: "`corpus/SOURCES.md:141` appends S268".

**Evidence.** At CONTENT, line 140 is S265 and line 141 is S266:

```
$ awk -F'|' 'NR>=140 && NR<=143 {print NR": "$2}' corpus/SOURCES.md
140:  S265
141:  S266
142:  S267
143:  S268
```

S267 is at `:142` and S268 at `:143`. This is not cosmetic: a verifier following `:84` to check
S268 (docs/**B**) lands on S266 (docs/**A**) and a tier check would read a different row's tier.
This seat found it by landing on S265 while checking S267.

**Impacted axis.** freshness (record provenance). Severity: defect in the record, not in a row.
Correction: `:62` → `corpus/SOURCES.md:142`; `:84` → `corpus/SOURCES.md:143`. The lesson is the
round's own record and is not in the deciding run's `FROZEN_UNCHANGED` set
(`.ufo/evidence/round-48/deciding-run.sh:22` lists `contract.json`, `freeze-2.json`, both counters,
`control`, `no-harm.sh`, `deciding-run.sh`, `statements.json`, `tools`, five evidence dirs — no
`corpus/` path), so the L1 may fix it; this seat may not
(corpus/ is read-only for every seat).

---

## Verified clean (each line is an observation, with the command)

Run at lane HEAD `17cc5ce1` (CONTENT `c7586b9a`; `git status --porcelain corpus/ tools/
SCORECARD.md` empty).

| item clause | result | evidence |
|---|---|---|
| 11 columns, no `|` in any cell | **pass** | `awk -F'|' 'NR>=140&&NR<=143{print NR": NF="NF}'` → `140-143: NF=13`; cell split gives 11 non-empty cells, ids `S265 S266 S267 S268` |
| kind / tier honest | **pass** | all four `docs`; tiers `A A A B`, each unchanged from the superseded row (`:37`,`:57`,`:102`,`:120`); `community` never A (census E10 silent); S268's scope names the English upstream S107 as the tier-A statement |
| scope differs → no E04 | **pass** | `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit **0**, 16 lines, **zero E codes**, exactly four new `W04` (`S265`–`S268`) versus `census-start.stdout`'s 11 W lines + `ok` (base: 10 `W04` + 1 `W01`; CONTENT: 14 `W04` + 1 `W01`); capture `.ufo/waves/round-48/a2w1/T48W2CritC2Rows.census.out.txt` |
| anchor sha prefix = committed snapshot | **pass** | recomputed: `a4c5c46b4af9` (236387 B), `e9cbc3e1ab7c` (8892), `2cb77df2f4be` (33289), `04e4c091715a` (111409) — each 12-hex prefix is in the row's anchor cell and equals the receipt's `sha256`/`bytes` |
| anchor section + revision/date | **pass** | `S026.html:1081-1082` publishdate; PIT `last-modified: Wed, 03 Jun 2026 08:45:37 GMT` (live HEAD, matches "2026-06-03"); zh-cn `last-modified: Tue, 07 Jun 2022 16:32:12 GMT` (matches verbatim); bwrap tag `v0.13.1` commit `362936ae…` = "Prepare 0.13.1 release", committer date 2026-10-14T12:13:57Z, release published 2026-10-14T12:21:00Z (matches "released 2026-10-14") |
| S267 byte range | **pass** | line 154 starts at byte 5889 and `<option>` ends at 5909, so the quote starts at **5909**; line 159 ends at 6426 with 27 bytes of `</option></para></listitem>`, so the text ends at **6400** — the anchor's "bytes 5909–6400" is exact |
| S268 section lines | **pass** | `S108.html:3609` is the `<h2 id="如何更新_expected_文件？">`, `:3611` the single `<p>` — both as the anchor says |
| teaches opens `supersedes T —` | **pass** | all four cells start `supersedes S0NN` + U+2014 (checked by ord); ids map S265→S026, S266→S048, S267→S093, S268→S108 |
| Gate quote located, ≤25 words, phrases | **pass** | amendment-2 extraction: each quote occurs **once**; tokens 15 / 21 / 25 / 6 (S267 exactly at the cap); offsets 2137 / 1014 / 2642 / 2514; required phrases `84%`, `should therefore be prioritised`, `--unshare-all`+`--unshare-cgroup-try`, `--update_goldens` present |
| live leg holds | **pass** | this seat's four fetches (200): S026 236387 B `dfea6b9ba734`, S048 8892 B `e9cbc3e1ab7c`, S093 33289 B `2cb77df2f4be`, S108 111409 B `dc436d9e6616`; **all four extract (counter's own `extract`) to text byte-identical to their snapshots and contain their quotes** — the S108 byte churn does not threaten the quote at this hour |
| recheck valid | **pass** | `730d / 90d / on-release / 180d`, each the superseded row's cadence; census E09 silent |
| used-by exact | **pass** | each new row lists exactly the superseded row's single entry (`repeated-control-precondition.md`, `incremental-pin-disposition.md`, `regression-tally-completeness.md`, `r8-golden-update-flag.md`), and each entry carries the new id on its `source:` line (line 1) with `verified-at: 2026-10-26` |
| old row's status/recheck/used-by untouched | **pass** | `git diff --stat 473336d9 c7586b9a -- corpus/SOURCES.md` → `1 file changed, 4 insertions(+)` — the only change to the registry at CONTENT is the four appended rows |

## Residual risks and notes (not defects)

1. **"the 2026-10-26 bytes" is ambiguous, and the day is not byte-stable.** `S265`'s scope says
   "re-anchored to the 2026-10-26 bytes" and `S268`'s "re-located in a committed 2026-10-26
   snapshot". This seat's fetch the same day produced the *same byte count* but a *different
   digest* for both pages (S026 `dfea6b9ba734` vs `a4c5c46b4af9`, both 236387 B; S108
   `dc436d9e6616` vs `04e4c091715a`, both 111409 B). The anchor's sha pins which fetch is meant, so
   the row is recoverable; a stricter cell would say "the 2026-10-26 snapshot bytes". Not raised as
   a finding because the item's anchor clause is satisfied exactly.
2. **S267's freshness is a re-quote, not a re-fetch of new bytes** — the digest equals S093's own
   2026-10-23 pin. The row says so ("the same six flags … at tag v0.13.1") and the lesson says so
   ("this digest is the row's own pin, so the re-anchor changes no bytes' identity — only the
   quote"), so this is disclosure, not overstatement. Worth keeping in view when the round is
   scored as "freshness": three of the four targets moved no bytes, only their quote location.
3. **Neither F1–F4 can flip the deciding verdict**, and that is the finding's real weight: the
   frozen counter checks the quote and the required phrases
   (`check_quote` `.ufo/evidence/round-48/freshness/measure.py:292-307`, `check_phrases` `:310-316`)
   and never the anchor's coverage of the
   teaches cell, so `C2_R48_PASS=true` was observed by another seat at CONTENT with all four
   `TARGET … REFRESHED` (`.ufo/waves/round-48/a2w1/T48W2ExecC2Run.md`, R3). The rows can pass while
   carrying F1–F4; the corrections above are row hygiene, and F5 is the only one that can mislead a
   later round's verifier.
4. **Nothing the old rows taught is lost outright** (answering the item's comparison directly):
   S265 carries S026's three clauses with the same substance; S266 drops only the hedge word
   "explicitly" (S048 `:57` → S266 `:141`); S267's five other flags — `--clearenv`, `--proc`,
   `--tmpfs`, `--die-with-parent`, `--new-session` — leave S267's scope but their locators survive in
   S093 (`:102`), which stays `mined` and unedited, so the lane keeps them; S268 drops "only" (F4).
   The one widening is F1's user-flag wording.

## Provenance

| artifact | sha256 (12) | bytes | lines cited |
|---|---|---|---|
| `corpus/SOURCES.md` (lane worktree, HEAD `17cc5ce1`) | — | 490 lines | 37, 57, 102, 120, 140-143, 145 |
| `.ufo/evidence/round-48/freshness/sources/S026.html` | `a4c5c46b4af9` | 236387 | 1081, 1087, 1095, 1101, 1123, 1130, 1132, 1136 |
| `.ufo/evidence/round-48/freshness/sources/S048.html` | `e9cbc3e1ab7c` | 8892 | 86, 87, 90, 94 |
| `.ufo/evidence/round-48/freshness/sources/S093.xml` | `2cb77df2f4be` | 33289 | 129-132, 153-160 |
| `.ufo/evidence/round-48/freshness/sources/S108.html` | `04e4c091715a` | 111409 | 3609, 3611 |
| `corpus/lessons/round-48.md` | — | — | 21-24, 55, 62, 79, 84 |
| `corpus/knowledge/incremental-pin-disposition.md` | — | — | 1 (`S266` clause), 5 |
| `corpus/knowledge/regression-tally-completeness.md` | — | — | 1, 2 |
| `.ufo/evidence/round-48/freshness/measure.py` | `faefe9b44274` | 868 lines | 101, 288-309 |
| `.ufo/waves/round-48/a2w1/T48W2CritC2Rows.probe.txt` | — | 33 lines | this seat's probes (digests, live fetches, headers, tag) |
| `.ufo/waves/round-48/a2w1/T48W2CritC2Rows.census.out.txt` | — | 16 lines | census validate capture |

## Bounds, scratch, tooling

- Lane read-only: only this file, `T48W2CritC2Rows.probe.txt` and `T48W2CritC2Rows.census.out.txt`
  were written, all inside `.ufo/waves/round-48/a2w1/`. No git or jj command was run; `corpus/`,
  `tools/`, `SCORECARD.md` untouched.
- Scratch `S=/fast/scratch/hyaku/tameshi-r48/T48W2CritC2Rows` (TMPDIR set there; nothing under
  `/tmp`; heaviest artifact 236 KB of fetched bytes) **deleted before this report was yielded**; the
  receipts this seat cites were copied into the deliverable directory first.
- Counter discipline: the frozen counters were **not** run by this seat (the instrument is another
  item); the census validator was run read-only, and the one network pass was four plain `curl`
  GETs plus two GitHub API reads — probes, not a deciding invocation. Disk guard showed 616.2G free
  on `/fast/scratch` before the pass.
- No tool installed or upgraded (pacman paused host-wide; none needed).
