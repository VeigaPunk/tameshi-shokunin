# CriticUniversal — universal readings and full-set enumeration (round 41, w1)

Seat `L1Tameshi41.CriticUniversal`. Read-only: no lane edit, no counter run against the tip; base-rev
runs, `--control`, tool-level selftests and `/tmp/tameshi-r41-criticuniv/` scratch only.
Base `a3d6c690…`, freeze `d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937`.

Artefacts as reviewed (2026-10-25T03:47–03:52 −03):

| artefact | sha256 |
|---|---|
| `.ufo/evidence/round-41/contract.json` | `529cb1606fe86d4dd9b78a3e08f92f14e1439be072544102e7409a98358aae35` |
| `.ufo/evidence/round-41/calibration/measure.py` (C1) | `9aaa99ac5a5abd16a42123fba4bf5c90151b3d043aa2d92ee99116e5789d92cd` |
| `.ufo/evidence/round-41/census/measure.py` (C2) | `83268eff97048cd4223a6f015b901c5efbde15d7b0d506bd40e5611b373ce94c` |
| `.ufo/evidence/round-41/census/fixtures.json` | `20b6254d39a75fb9b09b783131a7cdcaf360c36642e39424343166515aa26329` |
| `tools/write-path-census-v3.py` | `095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279` |
| `corpus/knowledge/r41-variable-destination-writes.md` | `ee7df01249e11d53a8f29911e3c1345bb78f93be7d9b7654474470fe74f3903a` (107 lines) |
| `corpus/lessons/round-41.md` | `b86930367cc298f4dc222d964e1162a31621dc111f568a9a09253e89d96e18ca` |
| `SCORECARD.md` | `b8bcc114fdb88f7031b64686734d8950b2845733e804c5920378d04537ec3f82` (1946 lines) |

**Verdict:** the universal in each claim does not describe what the counting command enumerates. C1
audits three artefacts out of this round's records and counts S-id *mentions*; C2 pins two live sites
by line window rather than enumerating them. C1's instrument reach is stated in the
SCORECARD now (`:1937-1943`), which is the right content, but the contract's claim sentences still
read as universals ("no round-41 record", "both live … sites") and C2's window is disclosed nowhere.

---

## 0. Defects that closed during this review (so the ledger is honest)

I found these in the frozen bytes; the swarm closed them while I was reading. They are listed because
each one was live at the freeze, and each fix is now pinned:

- **C1 `m7` read `cells[9]`, the `opened` date.** Frozen counter on the freeze blob:
  `registry()[S152] = '2026-10-24'`; header `corpus/SOURCES.md:1` puts status at index 8. So `m7 ≥ 1`
  for *any* S-id citation and C1's target was unreachable. **Closed by A1** (`cells[8]`); verified
  `S152/S153/S154 → 'mined'`.
- **`fixtures.json` was mutable without detection.** No `fixtures_sha256` check existed in
  `census/measure.py`; the pinned `a4123ce3…` and the worktree `20b6254d…` both exit 0 from
  `--selftest`. **Closed by A2** re-pinning the fixtures + adding the `symlink_arg` mutant.
- **C1 counter bytes drifted past its pin.** At 03:43 the contract pinned `8bc9b422…` while the file
  hashed `9aaa99ac…` (an m9 change with no amendment). **Closed by A5** (m9 derives its expected words
  from the round-40 table instead of hardcoding `six refused`/`ten present`; verified the contract now
  pins `9aaa99ac…`).
- The knowledge entry's earlier "two unflagged sites" and "what v3 resolves = a path" wording were
  false; the current draft states three sites and that the record field is a concatenation. Verified.

Residual record defects from that churn (still open):

1. `contract.json` `kill_rule_note` reads "no default-mode run … before **A1/A2/A3**" — five
   amendments exist. Narrow: "… before any amendment" or list A1–A5.
2. `contract.json` keeps `frozen_before_any_seat_score: true` / `frozen_before_deciding_run: true`
   as bare booleans while five amendments were applied after seats scored. Add
   `amended_after_seat_scores: true` so a reader of the top-level fields alone is not misled.
3. `SCORECARD.md:1904-1906` says the five amendments are "none of them a change to a claim's
   predicate, **counter target** or kill rule", but its own A2 entry adds
   `mutant_symlink_arg_killed` to `claims.C2.target` and changes `fixtures_sha256`. The two round-41
   records contradict each other; narrow the SCORECARD sentence to "no class rule or kill rule" and
   say the C2 target gained a third mutant.

---

## 1. C1 — does `calibration/measure.py` enumerate the full set? **No.**

### 1A. Record set = three artefacts

`measure.py:18-21` and `round41_records` (`:142-146`): `corpus/lessons/round-41.md`, the SCORECARD
`## Round 41` section, the LOG `## 2026-10-25 — round 41` section. Not scanned: the knowledge entry
(this round's S153/S154 and both snapshot paths), the README row, `corpus/QUALITY.md`, the lesson's
sibling reads. So contract C1's "**no round-41 record** cites an unmined S-id or an unresolvable repo
path" is false as a universal — for the knowledge entry both classes are simply unchecked.
Narrow to: "no round-41 *lesson, SCORECARD Round-41 section or LOG round-41 entry* cites …".

### 1B. `m7` counts mentions, so `m7=0` is reached by omission

`S_CITE_RE = \bS(\d{3,})\b` (`:44`) has no notion of "cited as a source". The ScribeLesson item
required the Gate to name staged **S185/S189** and **S137**; none exist in the registry (109 rows,
max S154). The shipped lesson avoids all three ids — it says "the two staged F4 gate-census entries"
and "the staged row the round-40 Gate already refused" (`corpus/lessons/round-41.md:28-38`) — and A3
discloses the same device for the collision sentence. So the claim is true *by omission*, not by
citation discipline. Receipt (fixed index, work registry):

```
m7 candidates for a Gate naming its sources: S137 None · S153 mined · S154 mined · S185 None · S189 None
=> m7 = 3
```

That is a fixable-defect/tradeoff split: the class definition ("does not hold as mined") is right, but
the record can only satisfy it by dropping id-level refusals, and the drop is only disclosed for one
sentence (A3). Two options, both narrowing:
(a) class: "cites **as a source** …", excluding ids on a line matching `refus` (the heuristic `m9`
already uses at `:161`); or (b) statement: "… except ids the record names as refused", plus one
sentence in the lesson disclosing that its refusals are recorded without ids.

### 1C. `m8` path set is a whitelist of four prefixes

`path_tokens` (`:181-190`) admits only backticked tokens starting with `corpus/`, `tools/`,
`.ufo/evidence/round-41/`, `.ufo/waves/round-41/` or equal to one of seven root files, and drops any
token containing a space or comma. Outside: `considerthese/…` (cited by the round-41 QUALITY
criterion), `docs/`, `scripts/`, markdown links, `path:line, path2:line` runs, `rev:path` forms
(the lesson's `31687496:tools/write-path-census.py`, `:36`), and absolute sibling paths
(`/home/vgpnk/Projects/shokuknow/merge/tameshi/`, `:30` — correctly ignored as *repo-relative*, but
worth saying so). Narrow the class to "… a whitelisted backticked repo path …".

### 1D. `m6` is silent zero and counts distinct ids

`:216-223`: no matching row ⇒ `m6 = 0`; a row without `N rows` ⇒ `m6 = 0`. Deleting the standing row
satisfies a class that says the count matches. `len(rows)` (`:211`) is distinct S-ids; the SCORECARD's
own re-derivation (`grep -cE '^\| S[0-9]{3} \|' corpus/SOURCES.md`) is physical rows (109 = 109 today;
a duplicated id row would diverge, and `S\d{3,}` accepts 4-digit ids the grep does not).
Narrow: count physical rows, and add a non-zero/absent-row finding instead of 0.

### 1E. `m9` is not sentence-scoped

`:249-259` (as amended by A5) accepts the words `round-40`, `<table refused> refused`,
`<table present> present` anywhere in the lesson. A5 fixed the *values* (they now come from the table)
but not the *locality*: a lesson that mentions `round-40` in one section and has the counts in a
different one still passes; counts above 20 fall back to digits only (`counts.get(table[1], str(…))`).
Also `quarantine_summary` (`:168-178`) searches the whole lesson, so a summary-shaped sentence can be
found anywhere. Narrow: match one sentence that contains `round-40` and both counts.

### 1F. No `declared_scope_limit` on C1

C2 has one; C1 does not. The SCORECARD now discloses C1's limits (`SCORECARD.md:1937-1943`), which is
the right content in the wrong artefact — the claim lives in the contract. Add the same paragraph as
`claims.C1.declared_scope_limit` (four prefixes; three artifacts; vacuous when records are absent;
whole-lesson m9; no self-pin).

---

## 2. C2 — does `census/measure.py` enumerate the full set? **No.**

### 2A. "both live variable-destination sites" is a line window, not an enumeration

`:221-224` selects the *last* expected record with `open` in [805,815] and `os.symlink` in [815,825].
Independent enumeration of the base blob (`git show a3d6c690:tools/repeat-control.py` through
`classify_source`) yields 6 records and exactly 2 expected sites — 811 `open`, 820 `os.symlink`, both
`scratch=1` — so **"both" is true today**, but a third expected site outside 805–825 leaves the
predicate green while the sentence still reads as a universal. Correction: choose the first expected
record of each kind and assert the expected-site total, keeping the line numbers as identity assertions.
(Also: 815 lies in both windows, so a site at 815 would be tested twice.)

### 2B. "v2's own patterns resolve none" is a site count for the symlink class

`census/measure.py:88-98` counts `symlink_sites` by matching `V2_WRITE_RE` lines; its own docstring at
`:89` says "a resolution miss, not a site miss". `V2_WRITE_RE` (`:37-43`) has no `os.symlink`
alternative, so the result is pattern absence, not a failed resolution. Narrow: "v2 has no
`os.symlink` pattern, so it records no write site on the planted symlink fixture; on the
variable-destination fixture it records no expected-value destination".

### 2C. The fixtures pin is declared, never verified

The amended contract pins `fixtures_sha256 = 20b6254d…` and the counter reads that blob
(`:151-164`) but never hashes it; only `claims.C2.tool_sha256` is enforced (`:140-147`). Both
`a4123ce3…` (frozen) and `20b6254d…` (current) exit 0, so "v3's selftest exits 0 with all four
planted fixtures at their declared values" is satisfiable by any mutated fixture file. The third
mutant is genuinely killed, though — verified on the new fixtures:
`python3 v3-mut-arg.py --selftest …` → `symlink_unflagged=0` and two `FAIL`, exit 1.

---

## 3. The v3 docstring is falsified by the round's own scope seat

`tools/write-path-census-v3.py:18-21` (pinned bytes): "Aliases, closures over reassigned names,
attribute reassignment, conditional assignment, dictionary and list elements, and any path computed by
a function call that does not fold to a literal are **NOT resolved**."

`.ufo/waves/round-41/w1/ReviewV3Scope.md:70-90` measures the opposite for several members:
`1_alias_rebinding.py:22` → "**resolved** — docstring too broad"; `2_closure_reassigned.py:10/21` →
stale resolves; `3_attribute_reassign.py:25-26` and `4_conditional_assign.py:10,26` and
`5_nonfolding_helper.py:36,42` → expected claims from the callee name/source text. My independent
probes agree: `dest = helper("golden"); open(dest,"w")` → `expected=1 unflagged=1`;
`open(os.path.join(compute("snapshot"), root), "w")` → `expected=1 unflagged=1`.

Because the tool is sha-pinned (`095924a7…`), the docstring cannot be corrected without changing the
capability artefact. That is a **tradeoff**, not a hot-patch: the knowledge entry's "What is not
claimed" (`:98-107`) already carries the honest, narrower wording ("not tracked consistently … a
non-folding helper is resolved by its name"). Smallest safe move: leave the pin, and add one line to
the entry or SCORECARD — "the tool's docstring lists these as not resolved; `ReviewV3Scope.md` shows
they are resolved inconsistently, which is the behaviour this entry claims" — so a future reader does
not treat the docstring as the scope statement. Also note `kw_open`/`kw_replace` are invisible
(`open(file=dest, mode="w")`, `os.replace(src=…, dst=…)` → `sites=0`), so the docstring's
"open(path, …)"/"both arguments" are positional-only.

---

## 4. Offenders in the drafts

### 4A. `corpus/knowledge/r41-variable-destination-writes.md` (sha `ee7df012…`)

Verified true and worth keeping: three unflagged `tools/` sites including `registry-replay.py:123`
(match); the seven `os.replace`/`os.rename` records in `tools/` all `expected=False` (exact match);
`scratch = tempfile.mkdtemp(…, dir="/tmp")` at `repeat-control.py:597` with three name hops to `:811`
(match); the six scratch markers (match); 811/820 both `scratch=1` (match). Remaining offenders:

| line | reading | falsifier | narrowing edit |
|---|---|---|---|
| 89 | "Both landed 2026-10-19, **six days** before this lane's v2" | v2's first commit is `2026-10-24` (`git log --diff-filter=A --format=%as -- tools/write-path-census-v2.py`); prior art `ac47c78`/`4a7aede` are `2026-10-19` → **five** days | "five days before this lane's v2" |
| 90 | "v3 is a **subset** of that machinery — … — **plus three things those do not do**" | a subset cannot contain three members the superset lacks; the sentence contradicts itself | "v3 shares the assignment-resolution idea at a lower depth (4 vs 8/6) and adds `os.symlink` destinations, the expected/scratch/update-flag classification, and scratch tracing" |
| 73-75 | "resolve a destination through `os.path.join`, `+`, `/`, `JoinedStr` and attribute chains to a depth of four" | `_resolve` (`v3:96-103`) also folds **any** call expression by splicing its source segment and its arguments' resolutions — the mechanism behind the false-positive class in `:48-60` and the seven `tools/` sites | append: "and any call expression, whose source segment and arguments are spliced into the trace" |

### 4B. `SCORECARD.md` round-41 block (sha `b8bcc114…`)

1. **Dangling "after" subsection.** Both claim rows say "see the after subsection below"
   (`:1910`, `:1911`); the file ends at 1946 with the disclosed limit and there is **no** after
   subsection and **zero** `NOT-YET-MEASURED` strings in the file. The item said: where no receipt
   exists, write `NOT-YET-MEASURED`. Narrow: measure column = `NOT-YET-MEASURED (deciding run pending)`,
   and drop the pointer.
2. **Unlabelled measurement.** The C1 delta cell says the record-audit classes "**were all measured**
   on this round's records" — present/past-tense receipt claim with no receipt path and no `--rev work`
   label. Narrow: "pre-run check at `--rev work`" (if that is what it was) or `NOT-YET-MEASURED`.
3. **Amendment count** — now says five ✓, but see §0.3: "none … a change to a claim's … counter
   target" contradicts A2.
4. Positive: `:1937-1943` now declares C1's instrument limits (no self-pin, vacuous when records are
   absent, four prefixes, whole-lesson m9). This is the content §1F asks for in the contract.

### 4C. `corpus/lessons/round-41.md` (sha `b8693036…`)

- `:53-58` Correction: "one adopted, six refused, ten present-but-not-appended" plus "round-40" in one
  paragraph — satisfies `m9` as amended (A5). True against the table `(1, 6, 10)`.
- No `S185`/`S189`/`S137` anywhere (verified) — which is exactly why `m7` reads 0 (§1B). If §1B(b) is
  chosen, this omission should be stated in the lesson rather than implied.
- `:64` word-label mistake row is correctly self-falsifying ("the label read 16 where the count reads 15").

---

## 5. Full-set table

| class | audit surface | full set? |
|---|---|---|
| `m6` | last `\| sources-registry \|` row vs distinct S-ids | **no** — silent 0 if the row is deleted/unparsable; distinct ids, not rows |
| `m7` | 3 artefacts × every `\bS\d{3,}\b` | **no** — knowledge/README/QUALITY unscanned; refusals counted as citations; 0 reached by omitting ids |
| `m8` | 3 artefacts × backticked paths, 4 prefixes + 7 root files | **no** — `considerthese/`, `docs/`, links, comma-joined and `rev:path` forms never checked |
| `m9` | round-40 lesson vs 3 substrings anywhere in the round-41 lesson | **partially** — values now derived (A5), locality still unscoped |
| C2 live sites | two fixed line windows 805–825 | **no** — 2 verified at the frozen blob, but the counter does not enumerate |
| C2 fixtures | selftest exit only | **no** — `fixtures_sha256` unenforced; the tool pin is the only byte check |

## 6. Impacted axes

- **calibration** — the C1 claim sentence overstates its own instrument on every class; the scores are
  now reachable (`m6` restated to 109 at `SCORECARD.md:1851`, `m9` corrected at `LESSON:53-58`,
  `m7`/`m8` by omission), but the universal wording survives the run.
- **depth** — C2's capability is intact and the third mutant kills; the residual is the docstring's
  negative list (§3) and the window-based live-site claim (§2A).
- **conformance** — three contract-pinned artefacts were mutated after the freeze and re-pinned by
  A1/A2/A5 within minutes; the ledger is now consistent except for §0.1–0.3.

## 7. Smallest safe correction, ordered

1. Contract record: fix `kill_rule_note` scope (A1–A5), add `amended_after_seat_scores: true`, and add
   `claims.C1.declared_scope_limit` = §1A–1E verbatim.
2. Narrrow the C1 statement: three named artefacts; `m7` "cites as a source"; `m8` "whitelisted
   backticked repo path". Narrrow the C2 statement: "the two expected-value sites at
   `tools/repeat-control.py:811` and `:820`" instead of "both live … sites"; say "v2 has no
   `os.symlink` pattern" instead of "resolves none".
3. Counter changes belong to a successor counter (routed to round 42 per `SCORECARD:1943`): expected-site
   enumeration instead of windows, a fixtures self-pin, a `records >= 1` gate, a non-silent `m6`, and a
   sentence-scoped `m9`. Do **not** hot-patch the pinned counters again.
4. Draft edits: knowledge entry lines 73-75, 89, 90; SCORECARD `:1904-1906`, `:1910-1911` (write
   `NOT-YET-MEASURED` and drop the dangling pointer); add the docstring-vs-`ReviewV3Scope` line (§3).

Report: `.ufo/waves/round-41/w1/CriticUniversal.md`
