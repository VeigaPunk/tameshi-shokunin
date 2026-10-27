# Round 43 lesson

author: tameshi L1 (hyaku run 6, attempt 1)
date: 2026-10-25

## Gate

Theme: **what a survivor is called** — the lane's own survivor-resolution rule,
grounded in two sources opened this round and in one held row re-opened. No
assimilation from the shokuknow package this round (`Assimilation: none`); the
package's staged ids were examined read-only for the collision hazard (below),
never adopted.

### Admit — S159 (new row): Wikipedia, *Mutation testing*

- URL https://en.wikipedia.org/wiki/Mutation_testing, fetched 2026-10-25 with
  `curl -fsSL`, 170793 B, 1159 lines, `<title>` `Mutation testing - Wikipedia`,
  revid 1373580212, sha256
  `6e4a06c0863ca2b0f68c36a1e29ca1eeeb01d20ae5e1d9ed4534a81406decc43`; a second
  fetch the same day was byte-identical. Snapshot:
  `.ufo/evidence/round-43/sources/wikipedia-mutation-testing.html`.
- Located quotes (both in the `Mutation testing overview` section; this
  revision has **no** equivalent-mutant section of its own, and `grep -c
  'Equivalent_mutants'` → 0):
  - line 794, `<p id="mw-Q">` (16 words): "The resulting program is
    behaviorally equivalent to the original one. Such mutants are called
    equivalent mutants."
  - line 796, `<p id="mw-w">` (15 words): "Equivalent mutants detection is one
    of the biggest obstacles to practical usage of mutation testing."
- Scope: the behavioural definition and the obstacle claim only. The page
  carries **no** survivor vocabulary (`surviv`, `unreach`, `unkilled`,
  `undetected` → 0 whole-artifact), so it is never cited as evidence that a
  dead-code survivor differs from an equivalent mutant; that separation is this
  lane's K/D/E/U rule.
- PROVINCE: mutation-outcome semantics for the lane's own kill verdicts is Core
  F1 ground. QUALITY: quotes ≤25 words and located, snapshot committed,
  coverage row in `corpus/README.md`.

### Re-open — S089 (held): Stryker Mutator, *Equivalent mutants*

- URL https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/,
  fetched 2026-10-25, 38687 B, 24 lines, `<title>` `Equivalent mutants | Stryker
  Mutator`, sha256
  `79f6501ad8f2a74e647532dba8f77f17482afa70ccbe6821d2368092454079ce`; a second
  fetch was byte-identical, but the bytes have **drifted** from S089's
  2026-10-22 anchor (`bc572676…`): same 38687 B, same quoted sentences at the
  same offsets, `last-modified: Sat, 24 Oct 2026 15:08:38 GMT`, so the anchor
  digest is stale while the cited text survives (wave-1 ScribeLessonGate D1;
  the round-44 recheck should move S089's anchor to this snapshot). Snapshot:
  `.ufo/evidence/round-43/sources/stryker-equivalent-mutants.html`.
- Located quotes: line 16 (12 words) "There is no definitive way for Stryker to
  find and ignore them."; line 15 (20 words) "even if we change >= to <= and
  even < or > we will get the same output each time!"; line 17 (9 words) "the only
  solution is by finding these by hand".
- Status, recheck unchanged; `used-by` extended `corpus/knowledge/mutation-case-kumitate-cite-check.md`
  → that plus `corpus/knowledge/r43-survivor-resolution-rule.md`.

### Refused this round — the duplicate row I first appended (self-caught)

The first append added a *new* row for the Stryker equivalent-mutants page. The
census printed `W04 S159 duplicate url stryker-mutator.io/... across scopes` and
`grep` showed S089 already holds exactly that document. The row was withdrawn
before any commit, S089 was re-opened instead, and the Wikipedia row took S159.
This is the guard's own dedupe rule applied to the lane's own append — see
Mistakes row 1.

### Deferral — the staged package's survivor material

Not opened for adoption this round: the theme slot is filled by the rule, and
the package's next unadopted entry (`mutation-score-semantics-cjk.md`, gates
admit in round 42) is adjacent ground for a later assimilation round. Its flip
condition is unchanged from the round-42 lesson: re-open and snapshot its three
sources, repair the dangling `CANNOT-ANSWER.md` §3.7 pointer, land its coverage
row.

### Ids, collisions, census

- Registry before: 113 rows (S001–S158). After: **114** (S159 added; the next
  unused id follows it). `grep -cE '^ {0,3}\| S[0-9]{3} \|' corpus/SOURCES.md` → 114; the
  `Next unused id` line at the registry tail names it.
- Collision check, read-only, via `tools/staged-id-guard.py` against the staged
  package `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md`
  (never written): **7 collisions** `S153`–`S159`, of which **3 are documents
  the registry already holds** — `staged:S153`→S105 (POSIX diff),
  `staged:S154`→S106 (google/golden), `staged:S159`→S155 (PIT basic concepts) —
  and 4 are new documents. The naive arithmetic map (each collision moved to
  `max(registry)+1…`) lands on the eight ids immediately above the registry
  maximum, which are themselves staged ids: refused, cascade 7. The safe floor
  for a *partial* adoption is one above the larger of the two maxima
  (`max(registry, staged)+1`).
- Used-by changes, old → new (all in `corpus/knowledge/`): S089
  `mutation-case-kumitate-cite-check.md` → same plus `r43-survivor-resolution-rule.md`;
  S155 `pit-outcome-vocabulary.md` → same plus `r43-survivor-resolution-rule.md`;
  S158 `pit-outcome-vocabulary.md, r42-attribute-and-outflag-destinations.md` →
  same plus `r43-survivor-resolution-rule.md`. No status or recheck change.
- Census: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
  exit 0 at round start (113 rows, 9 × W04 + 1 × W01, zero E codes;
  `.ufo/evidence/round-43/census-sources/start.stdout`; the receipts carry the
  validate lines and the exit code in a sibling `.exit` file, not a row count,
  which is what `grep -cE` above is for) and exit 0 at round end
  (114 rows, the same warning set and no new one, zero E codes;
  `after.stdout`). Wave-1 seat ExecCensus independently reproduced the start
  capture byte-for-byte and pinned it to the 113-row blob.
- Quarantine slice: 17 data rows (14 `payload-absent`, 3 could-not-be-fetched),
  re-derived read-only and byte-identical to the round-42 slice; verdicts stay
  in the round-40 lesson and nothing was adopted **this round** (wave-1 ScoutQuarantine).

### considerthese

`considerthese/2026-10-22.md` proposal 5 (survivor reclassification tracker; the
one still-unimplemented proposal touching this round's work) is mined, not
implemented: the K/D/E/U rule and criterion 83 record *transitions* for the two
round-42 survivors, but there is no `(gate, mutant id)` register and no
overturn rate. A future round lands it as criterion 85. The other mined
proposals are unchanged. Wave-2 RevConsider corrected this paragraph: rounds
35–42 already carried a re-derivable standing command for the registry count (m6
checks the row's count), and C2's m13 *pattern-matches* the standing command
without executing it — so neither "first mechanical instance" nor "re-derivation"
is claimed for m13.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| duplicate-document append | the first working-tree append added `S159 | Equivalent mutants (Stryker Mutator docs)` while S089 already held that URL | the census W04 warning plus `grep -n stryker-mutator.io corpus/SOURCES.md`; no round-43 criterion existed | row withdrawn before any commit; S089 re-opened and cited instead; quality criterion 83's rule ("by document, never arithmetic") was already the intent, and `tools/staged-id-guard.py`'s dedupe is the mechanical form. Shown able to fail: the guard reports `held={S153:S105, S154:S106, S159:S155}` for exactly this class |
| frozen-rule-without-code | the C1 counter printed `mutants_killed=6 dead_code_only=0`: the K rule's reachability gate was written in the contract and never implemented, so the dead-code fixture counted as a kill | wave-1 mutation-tester MutC1F11, which ran the unmodified counter at the freeze | contract amendment A5: the kill oracle now requires at least one failing fixture with no unreachable statement; the K/D/E/U text, target, predicate and controls are unchanged. Shown able to fail: `control/c1-round42-battery.stdout` (ten fixtures → 4 kills) and the F11 ablation (`11/11` → `5 kills, 1 equivalent×`), both in `.ufo/evidence/round-43/control/` |
| join-then-fullmatch | `tools/staged-id-guard.py` checked map targets with `re.fullmatch(r'S\d{3,}', ''.join(targets))`, which can only match a one-entry map, so every multi-entry map was refused while the selftest stayed green (its admission case had one entry) | wave-1 mutation-tester MutC3Selftest, which reproduced the refusal of the counter's own six-entry safe map | amendment A4: per-target check plus `T4_multi_entry_map_admitted`; the selftest is now 14 cases. Shown able to fail: the pre-fix tool refused a two-entry by-document map with "map has a target that is not an S-id" |
| control-kept-the-kill-fixture | the first C1 `--control` skipped only the dead-code fixture, so the ten-fixture do-nothing control scored 11/11 and 5 kills — it was not a do-nothing control | the L1's own control run, pre-data | amendment A2: `--control` skips both new fixtures; the control now prints `10/10 mutants_killed=4 C1_R43_CONTROL_PASS=false` |
| lstrip-on-a-dotpath | the C2 counter normalised `.ufo/waves/round-43/` with `lstrip('./')`, which strips the leading dot, so every superseding receipt's re-assertions read as missing paths (m10=9) | the L1's own base run, pre-data | amendment A1: strip only a literal `./` prefix; m10 counts only receipts not named in a `supersedes`; base run then printed the declared `m10=0` |
| single-tool-pin-field | the contract carried one top-level `tool_sha256` that both C1 and C3 read; repinning it for the guard made `tool_sha_ok=0` for the census tool | wave-1 MutC1F11 (`tool_sha_ok=0` on both revs) | amendment A5: both counters read `frozen_tools[<path>]`; the top-level field stays for older readers |
| classes-is-a-constant | `classes=7` is a declared constant with a tautological `declared == 7` conjunct, so it is not evidence that seven classes ran | wave-1 RevC2DoNothing and RevC2Classes | disclosed, not repaired: the evidence a class ran is its own m-field, and the per-class fields are computed unconditionally. The sentence in the docstring was corrected (amendment A6) |
| extractor-narrower-than-the-sentence | m8 dropped brace-form and directory cites, m12 matched a prose mention of `Planned`, m13 matched `0,3` anywhere in the row, m10 excluded the superseding receipt's own claims, m11 required a commit rather than any object | wave-1 RevC2Classes (F1–F7) | amendment A6: brace expansion, directory resolution, the field form of `planned`, the backticked command cell only, superseded-target-only exclusion, `.ufo/waves/` scope, any-object resolution; three new selftest cases (prose-only `planned`, column-zero-plus-prose `0,3`, multi-entry map) |

| asserted-digest-equality | the Gate's S089 block said the re-opened bytes were "byte-identical to S089's 2026-10-22 anchor" while printing a different sha256 (`79f6501a` vs `bc572676`); the knowledge entry repeated it | wave-1 ScribeLessonGate D1, which compared the two digests and the `last-modified` header | the Gate and the entry now say the document drifted, with the size, the unchanged quoted offsets and the `last-modified` date; A11's lesson revision. Shown able to fail: `sha256sum` of the committed snapshot vs the anchor digest printed in the S089 row |
| uncounted-quote-length | the Gate gave 17 and 14 words for two Wikipedia quotes that are 16 and 15 words, and the Stryker line-15 quotation dropped the word `or` (`even < >` for `even < or >`) | wave-1 ScribeLessonGate D2–D4, re-run by the L1 with `split()` counts on the committed snapshot lines | word counts corrected and the quotation restored verbatim; the ≤25-word rule held either way, so no admission changed. Shown able to fail: `python3 -c` word count on the line, pasted in the report |

Append-only held: `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`,
`corpus/README.md` and `corpus/knowledge/r43-survivor-resolution-rule.md` are
insertions only; `corpus/SOURCES.md` changes are the two new rows (S159 only,
after the withdrawal) and three `used-by` cells, logged above.

## C1 instrument — limits, disclosed not repaired

- The reachability gate reads the *fixture's* source: a statement after an
  unconditional `return`/`raise` in the same block marks the fixture
  unreachable. It does not follow `if False:`, `raise NotImplementedError` under
  a guard, `sys.exit`, or a `while True` with no `break`; those are unreachable
  code the class would treat as reachable.
- `dead_code_only` requires every differing case to be an unreachable fixture.
  A mutant that differs on one unreachable fixture and one reachable one lands
  in `not_killed` (the stricter reading), which is intended but not obvious from
  the field names.
- The differential corpus is the twelve fixtures only. A drift on a real
  `tools/*.py` file that no fixture exercises is invisible to the verdict —
  `lane_unflagged_v4` measures false positives, not drift.
- The K rule's "reachable" gate is a source-text property, not a runtime one: a
  fixture whose discriminating construct is reachable in principle but never
  executed still counts as a kill.
- Numeric depth stays 9: the counter adds a decision table and two fixtures, not
  a ledger leg.

## C2 instrument — limits, disclosed not repaired

- m6 depends on the standing row's exact phrasing (`N rows at round M`); any
  other wording reads as a mismatch.
- m7 audits the record set it can read: an absent lesson is skipped and
  `records=` reports how many were read, so the class is vacuous on a round with
  no lesson yet.
- m8 resolves repo paths only; a cite of a file that lives in another lane or in
  the assimilation package is out of scope by construction.
- m10 reads only boolean `present` beside a `report`/`path` string, only under
  `.ufo/waves/`, in parseable JSON. Other key names, string booleans and
  malformed JSON are invisible; a receipt that is superseded is skipped wholesale
  (`superseded-target-only`), so a stale superseded receipt cannot be graded.
- m12 audits **one** block, the newest; the round-41 block also lacks its
  `planned` line and is invisible to the class (wave-1 ScoutC2Records).
- m13 proves the standing command's *pattern* and its load-bearing behaviour on
  a two-space indent; it does not prove the command is the one that produced the
  printed number.
- `classes=7` is a constant; the per-class fields are the evidence.
- Numeric calibration stays 6: C2 measures record agreement, not the SHONEN
  restraint rubric, and no box moved.

## C3 instrument — limits, disclosed not repaired

- The counter's own collision parse is a second implementation of the same
  regex, not an independent oracle: a shared misreading of the row shape would
  agree with itself. The census CLI is the third-party check, and it was run
  separately.
- The safe-map construction is the counter's, so `safe_map_admitted` shows the
  tool admits *a* correct map, not that it admits every correct map.
- `--tool-file` lets a substitute tool be scored; the counter pins the tool at
  REV but a falsifier can pass any file. The control receipt shows the
  constant-empty stub is caught; it does not show a hostile but accurate tool is.
- The live half reads a path outside the repository
  (`/home/vgpnk/Projects/shokuknow/...`), so the receipt depends on bytes no lane
  commit pins. `live_collisions`/`live_held` are recomputed by the counter, which
  catches a moved package, but the staged file's own digest is not printed in the
  C3 fields (sentinel F4; routed to round 44).
- `--control` uses the stub to prove the collision check is load-bearing; it
  does not measure the tool.

## Holds

- The whole-set adoption the floor rule now admits is unmeasured: a map over all
  103 staged rows (injective, disjoint from the registry, at or above the safe
  floor) is
  admissible by the rule but untested live. Planned for round 44.
- Two guard classes wave 1 leaves open: a staged row whose *document* is prose
  (no URL, no path) is refused as `unmapped`, which is correct but blunt — the
  message does not say which of the three causes fired. And a registry row that
  is itself indented four spaces is invisible to both patterns (census says
  indented code), so a lane that reformats its table silently loses a row from
  both counts.
- m10's superseded-target-only rule grades the superseding receipt, so a lane
  that supersedes with a false claim now fails; the round-42 supersede receipts
  were re-read under the new rule and agree with the tree.
- Wave-1 critic and reviewer findings not repaired in-round are listed in the
  report; the frozen predicates did not change for them.
