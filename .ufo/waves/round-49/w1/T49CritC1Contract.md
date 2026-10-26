# T49CritC1Contract — falsifying C1's design before data

Seat: T49CritC1Contract (C1 first falsifier, round 49 wave 1, calibration axis).
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Base `8ca67421111fa354b47b803358391d0b07fc6db9`.
Read first: `.ufo/evidence/round-49/contract.json` (`claims.C1`), `.ufo/evidence/round-49/c1/measure.py`,
`.ufo/evidence/round-49/control/c1-controls.py`, the frozen control receipts `control/c1-CTL_*.stdout`,
and the round-21/round-18 monitor pair the counter pins. Nothing in the lane was written; every probe
ran on a throwaway `git clone --shared` under `/fast/scratch/hyaku/tameshi-r49/T49CritC1Contract/`
(`S`), and `S` was deleted after the receipts below were copied into
`.ufo/waves/round-49/w1/T49CritC1Contract/`. **A probe is not a verdict — the L1 scores controls.**

Axes named: (1) cost-to-pass vs cost-to-fail (control ladder ordering), (2) census fidelity
(extractor vs the seven sections' real citations), (3) durability semantics (record append),
(4) the `absent` channel.

## Findings

| # | Finding | Severity |
|---|---|---|
| F1 | `absent` is unbounded, so a **cheaper** no-read control than CTL_K reaches `total=0`; CTL_G observed `C1_R49_PASS=true`, `absent=90` of 90 pointers | **high** |
| F2 | The frozen *expected-pass* control already records `absent` for three files that exist at base (`dispositions.json`, `verification.json`, `capture-context.py`); `absent` means "not under four roots", not "absent" | **high** |
| F3 | The durability term is a five-file sample: an entry passes it while depending on a record file outside `VOLATILE`, then lapses on one appended line — demonstrated with the CTL_K2 shape itself | **medium-high** |
| F4 | The extractor is not a faithful census: 21 citation forms in the seven sections are never extracted, 2 template tokens are false positives inside the map floor, and the page's own anchor convention is unimplemented | **medium** |
| F5 | `absent` rows bypass excerpt validation and never enter `total`; a row may omit `excerpt` entirely | **medium** |
| F6 | An empty-`inputs` trace receipt satisfies the trace gate, so "trace-bound inputs" constrains nothing | **medium** |
| F7 | `../` pointers accept any self-chosen 40-hex `fleet_commit`; nothing binds it to the fleet the round measured | low |
| F8 | Path-pointer excerpts need only 24 chars *anywhere* in the file; the frozen control quotes `text[:60]` (35 of 90 rows) | low (calibration note) |
| F9 | `--list` says `unresolved=8` at base while the scored `before` says 9 (the ninth is the external row's missing `fleet_commit`) | low (audit legibility) |
| F10 | `c1-controls.py` uses one fixed shared scratch path and `rmtree`s it at the end | low (operational) |

## F1 — a cheaper control than CTL_K reaches total=0 without reading  [high]

**Attack.** The predicate's floor is a *count* (`measure.py:78-80`, `:382` `counts[h] < FLOORS[h]`) and
the only pointer *kind* constraint is "every pointer the extractor finds" — which is content-blind.
`check_reads` short-circuits before opening anything for a `path` pointer whose token does not resolve
(`measure.py:271-279`): if `p['file'] is None`, `pointer_kind == 'path'`, and the row says `absent`
with `file: null`, it increments `absent` and `continue`s. No blob, no range, no excerpt.

**Control named: CTL_G (ghost-pointer).** For each of the seven sections, replace the *body* with
`FLOORS[h]` path pointers to files that do not exist (`ghost-i-jj.md`), keep the heading line
byte-identical, key one ledger entry per section to the new sha with a single stable input, and write
90 rows of `{heading, ordinal, raw, file:null, ranges:null, verdict:"absent", excerpt:""}`.
Driver: `.ufo/waves/round-49/w1/T49CritC1Contract/ghost_ctl.py` (self-contained; builds its own fixture).

**Observed** (`T49CritC1Contract/ctl-g.stdout`, 61 s):

```
POINTERS 90 {'path': 90} unresolved-before-reads 90
SECTION ## Mutation-sweep recipe … pointers=34 floor=34 present   (same for all seven)
C1_R49: self=a055e9297cc9 rev=7258dc161901ff8ac20298015d099c1259618187 sections=64 covered=64
  score=8 durable_covered=64/64 headings=7/7 pointers=90 floor_short=0 unresolved=0 unverified=0
  excerpt_miss=0 not_holds=0 absent=90 total=0 C1_R49_PASS=true
```

**Why it is cheaper than the frozen ladder.** The counter's cost to author a row is the evidence it
demands: CTL_K's 90 rows need 82 blob reads and 90 verbatim excerpts (`c1-controls.py:116-131`);
CTL_K2 needs the same plus two prefix edits. CTL_G needs **zero** blob reads of any cited artifact,
zero excerpt bytes, and it survives even if every artifact the section cited had been deleted. Its
`absent` count is the whole population. So the cheapest admissible *passing* shape is cheaper than the
cheapest *failing* control (CTL_K, `total=2`), which inverts the ladder: the controls cannot order
"read" above "not read".

**Impacted axes:** cost-to-pass ordering; calibration (the label can be earned with no reading);
the claim's own `cannot_see` note (it understates the hole: not only semantic support but the *entire
citation set* can be null).

**Smallest safe correction (counter, ~8 lines).** Load the frozen base census
(`control/c1-pointers-at-base-8ca67421.json`) and accept an `absent` row only when
`(heading, raw)` appears there with `file: null` **and** `pointer_kind == "path"`; cap
`absent <= base_absent` (6). CTL_G then dies: none of its 90 ghost raws is in the base census, so all
90 stay `unresolved` (`total=90`) and its seven sections fall under their floors.
Add CTL_G to the frozen control set as the negative control that must print false — it is the direct
discriminator, and it is cheaper to run than CTL_K.

## F2 — `absent` already covers files that exist, in the expected-pass receipt  [high]

**Attack.** `resolve()` probes exactly four roots — `token`, `corpus/knowledge/token`, `corpus/token`,
`corpus/lessons/token` (`measure.py:188`) — with no directory inheritance, so a section that names a
sibling of a path it just wrote out falls through to `absent`.

**Evidence.** At base the three r14 short names are real blobs:

```
$ git -C <lane> cat-file -t 8ca67421111f…:.ufo/evidence/round-14/dispositions.json   -> blob
$ ... :.ufo/evidence/round-14/verification.json      -> blob
$ ... :.ufo/evidence/round-14/capture-context.py     -> blob
$ ... :mutate_driver.py                              -> fatal: does not exist
$ ... :plans/round-N.plan.md / :plans/round-N-record-draft.md -> fatal: does not exist
```

and the frozen controls confirm they are scored as absent: `control/c1-CTL_K.stdout` ends
`unresolved=2 … absent=6 total=2`, `control/c1-CTL_K2.stdout` ends `unresolved=0 … absent=6 total=0` — six absent rows, of which at
most one (`mutate_driver.py`) is a genuine absence, two are *not artifacts at all*
(`plans/round-N*.md` templates), and three name files that exist. `c1-controls.py:123` writes those
rows mechanically (`row.update(verdict='absent', excerpt='')`), so the declared positive control —
the shape the round is told to reproduce — asserts false provenance three times and still prints
`C1_R49_PASS=true`.

**Impacted axes:** census fidelity; provenance (the claim's word is "resolves"); calibration, because
the reference passing shape encodes the defect.

**Smallest safe correction.** In `resolve()`: (a) inherit the directory of the nearest preceding path
token in the same paragraph/table row (`dispositions.json` after
`.ufo/evidence/round-14/dispositions-before.json` → `.ufo/evidence/round-14/dispositions.json`);
(b) as a fallback, accept a *unique basename* match over the REV tree. Then the three files resolve
and CTL_K2's `absent` drops from 6 to 3 (1 true absence + 2 template tokens, which should be excluded
from the census instead — see F4). Combined with F1's cap, the `absent` channel can no longer carry a
pass.

## F3 — the durability probe is a five-file sample, and the entry it must protect is not in it  [medium-high]

**Attack.** `VOLATILE` (`measure.py:65`) is exactly five files and `durability_commit`
(`measure.py:336-356`) appends `PROBE_LINE` to those five only. Any entry whose `inputs` cite a
mutable file outside that tuple passes the probe and lapses on a real append — which is precisely what
the claim's sentence ("a later record append cannot lapse them") denies.

**Counterexample using the frozen positive control's own shape.** `k2_record.py` replicates CTL_K2 in a
fixture: two prefix edits, `pinned_inputs` (equal to `c1-controls.py:107-113`, which excludes
`VOLATILE` and `SKILL.md`), mechanical rows. Its own input sets are:

```
Promotion-evidence calibration -> ['SHONEN.md', 'corpus/knowledge/executor-test-sufficiency.md',
                                   'corpus/lessons/round-1.md', 'reports/round-1-calibration.md']
Pin disposition (r13)          -> ['.ufo/evidence/round-13/pin-manifest.json', …,
                                   'corpus/lessons/round-12-verifier-spotcheck.md', …]
Effective expectation (r14)    -> ['.ufo/evidence/round-14/…', 'corpus/lessons/round-13-verifier-spotcheck.md', …]
```

Five of the seven entries pin record files. Scoring:

```
before-append  C1_R49: … covered=64 score=8 durable_covered=64/64 … absent=6 total=0 C1_R49_PASS=true
APPENDED corpus/lessons/round-1.md  (one line)  e639d60c594f
after-append   UNCOVERED_REV    ## Promotion-evidence calibration — fleet round-1
after-append   UNCOVERED_DURABLE ## Promotion-evidence calibration — fleet round-1
after-append   C1_R49: … covered=63 score=6 durable_covered=63/64 … total=3 C1_R49_PASS=false
```

(`T49CritC1Contract/probe2-before-append.stdout`, `probe2-after-append.stdout`.) The same shape with
`corpus/lessons/round-48.md` gives `record-dep-step1-probe-passes.stdout` (`total=0`) →
`record-dep-step2-record-append.stdout` (`total=3`). Lesson files are appended by design:
`git log --oneline -- corpus/lessons/round-48.md` = 3 commits (`5054532`, `c7586b9`, `e438777`);
`corpus/lessons/round-1.md` = 4 commits.

**And the lapse this round must repair is already of that class.** Re-running the monitor's
`entry_reason` per base-sha entry of the seven sections (round-21 ledger) shows the cause of every
lapse, and four sections' causes include files outside `VOLATILE`:

```
recipe   13 entries, 0 credited : 9× input-drift:corpus/README.md, 2× corpus/QUALITY.md, 1× LOG.md
restore  16 entries, 0 credited : 16× input-drift:corpus/README.md
map      13 entries, 0 credited : 13× input-drift:corpus/README.md
promotion 1 entry,  0 credited : 1× input-drift:reports/round-1-calibration.md      <-- not probed
r12      17 entries, 0 credited : 15× corpus/SOURCES.md, 2× corpus/knowledge/repeated-control-precondition.md
r13      20 entries, 0 credited : 18× corpus/SOURCES.md, 1× corpus/knowledge/incremental-pin-disposition.md
r14      14 entries, 0 credited : 12× corpus/SOURCES.md, 1× corpus/knowledge/incremental-pin-disposition.md
```

**Impacted axes:** durability semantics; calibration (the term is necessary but not sufficient, and
the claim states it as sufficient).

**Smallest safe correction.** Make the probe mean the sentence: append `PROBE_LINE` to **every
distinct `inputs` path of the credited entries**, not to a fixed five (the probe already builds a
synthetic tree with `read-tree`/`hash-object`/`commit-tree`, so this is a set change, not a mechanism
change). Consequence to accept deliberately: `tools/mutate-and-run.sh` and knowledge notes also drift,
so the integrator must either pin inputs from a *declared frozen* set or the predicate must be
restated as "durable against the five round-append files". The current wording cannot be true in
general, as `reports/round-1-calibration.md` above shows.

## F4 — the pointer set is not a faithful census  [medium]

**Attack.** The extractor (`measure.py:86-91`) sees only `FILE:RANGES`, bare `:RANGES`, `FILE`, and
`S\d{3,}`. `--list` at base returns 90 pointers (42 line, 41 path, 7 sid; 8 with `file: null`) —
receipt `T49CritC1Contract/list-base.json`. Against the seven sections' real citation forms,
`census-misses.json` records **21 forms never extracted**:

| form | example | SKILL.md (base) |
|---|---|---|
| section-sign | `mutation-case-kimi-census.md §1, §3-§6` / `…kagi… §1-§7` | 235, 236 |
| section-sign | runbook `§0 · §2 · §3 · §4 · §5 · §6 · §7 · §10`; `§1–§4 byte-frozen` | 1384, 1385 |
| glob path | `` `corpus/knowledge/mutation-case-*.md` `` (the map's "six…seven…eight…nine since round 26" row) | 1390 |
| fragment anchor | `reports/round-1-calibration.md#box-1` (file found, `#box-1` dropped) | 1467 |
| directory ref | `` `.ufo/evidence/round-13/` `` | 1522 |
| truncated digest | `hash83016d45…`, `hash275d8294…`, `75ed934d…` | 387, 389, 1581 |

Consequences that matter for the claim (not for the formula):

* The recipe's model citations `§1, §3–§6` and the map's eight runbook `§` refs are never resolved.
  Both are valid today (`mutation-case-kimi-census.md` headings `## 1.`…`## 6.`; runbook `## 0.`–`## 10.`),
  so a *later* rename of `§6` would pass this counter while the claim says "stale pointers are corrected".
* The map's glob row is a counted claim (`six/seven/eight/nine since round N`) that no pointer can
  falsify; adding a tenth `mutation-case-*.md` would not be noticed.
* `plans/round-N.plan.md` and `plans/round-N-record-draft.md` (SKILL.md:1393) are **false positives**:
  templates, not artifacts. They are 2 of the map's 17 floor and 2 of the 6 `absent` rows (F2).
* The page states its own anchor convention — "(Anchors `:…` are this page; …)" at
  **SKILL.md:1250** — which the extractor does not implement. That is why the map's two self-anchors
  are unresolvable, and why CTL_K2's fix is a SKILL.md text edit rather than a staleness repair.
  I checked the targets: `:1294-1297` is the "Pointer, not a second home … the anchored source governs"
  bullet (SKILL.md:1294-1297) and `:1246-1270` is the service-limits block (SKILL.md:1246-1270), so
  **CTL_K2's prefix is truthful, not fabricated** — see "What survived" below.
* `measure.py:37` says a bare pointer "inherits the FILE of the nearest preceding file pointer", but
  the code only records *line* pointers as `last` (`measure.py:151-153`). Documented-vs-implemented
  mismatch; a table row whose only file mention is a path pointer can never bind its `:ranges`.

**Smallest safe correction.** Either (a) declare the extractor's grammar in the contract as the
census's definition (then drop the word "faithful" and drop the §- and glob-based claims from the
seven sections' *evidence* role), or (b) add §-refs (`§N[-§M]` inherited from the paragraph's file
token, or the page itself per SKILL.md:1250), fragment anchors, and a directory-inheritance step, and
exclude wildcard/template tokens from the census. If (b), the floors will move — re-freeze them
*before* the deciding run; that is a contract amendment, i.e. an L1 call.

## F5 — `absent` rows carry no evidence and are not scored  [medium]

`measure.py:271-279` increments `absent` and `continue`s before the excerpt test at `:311`, and `total`
(`:401-404`) sums `unresolved, unverified, excerpt_miss, not_holds` — `absent` is printed (`:410`) and
never counted. A row may therefore be `{"heading":H,"ordinal":N,"raw":R,"file":null,"ranges":null,
"verdict":"absent"}` with no `excerpt` key at all (my CTL_G driver wrote `excerpt: ""` optionally).
**Correction:** require `searched` (≥2 roots tried) and a free-text `reason` on every absent row, and
gate the count (F1). Today `absent` is the only verdict class with no evidence contract and no cost.

## F6 — an empty-inputs trace receipt satisfies the trace gate  [medium]

`round-18/measure.py:373-431` binds a trace only *from* the receipt's `inputs` into the entry's
`inputs`; `receipt.get('inputs') == {}` passes (`isinstance(rec_inputs, dict)`), and the entry's own
`inputs` are what the input gate checks. My CTL_G entries used
`{"schema":"tameshi-trace-inputs-v1","inputs":{}}` and were credited (`covered=64`). The contract's
work-plan phrasing "trace-bound inputs" therefore adds no constraint: the durability burden is
entirely the entry's `inputs` dict. **Correction (integration, since the monitor is pinned):** the
re-keyed entries' receipts must list every input with equal sha — assert that in the wave-1
integration checklist, and have the L1 spot-check one receipt per section.

## F7 / F8 / F9 / F10

* **F7** `measure.py:281-288` accepts any `[0-9a-f]{40}` as `fleet_commit` and reads the fleet blob
  there, so `../PROTOCOL.md:63–68` (SKILL.md:1469) can be satisfied against an older fleet revision.
  `PROTOCOL.md` has moved this round-adjacent (`f47ad6ba`, `7c5b34f0`); at fleet tip `94ab3129` lines
  63-68 exist and match. Correction: pin `fleet_commit` to the fleet commit recorded in the round's
  freeze (`freeze.json`) and require equality.
* **F8** A path pointer's excerpt is checked against the *whole* file (`measure.py:305-311`), so 24
  characters from line 1 pass; the frozen control does exactly that (`c1-controls.py:9`, `:131`
  `text[:60]`). 35 of the 90 base pointers are path pointers. Not a defect against the docstring, but
  a calibration note: for path pointers the section should also carry a line range, or the excerpt
  should be required to fall in the region the sentence quotes.
* **F9** `--list` prints `file: null` for 8 pointers; the scored `before` says `unresolved=9`, the
  ninth being the external `../PROTOCOL.md:63–68` with no `fleet_commit` row (verified by calling
  `check_reads` with an empty reads doc: `{'unresolved': 9, 'unverified': 81, …}`). Anyone auditing the
  census against the contract's `before` line will trip on the difference; the base census file should
  record scored status, not only `resolve()` output.
* **F10** `c1-controls.py` fixes `SCR=<HYAKU_SCRATCH>/tameshi-r49/controls` (line 26) and
  `shutil.rmtree(SCR)` at line 171; two control runs (another seat re-running, or the L1 re-scoring)
  collide and one deletes the other's live clones. Use a per-run suffix and remove only after the
  receipts in `OUT` are written (they already are). Also `score('CTL_0', LANE, BASE)` reads the live
  lane's monitor files for the pin check, so a sibling editing `.ufo/evidence/round-18/measure.py`
  mid-wave would surface as a setup error, not as a control miss.

## What survived the attack (negative results, recorded)

* The monitor pins are honest: `MONITOR_SHA`/`MONITOR_IMPL_SHA` are re-checked in the live lane and at
  REV (`measure.py:369-373`); the counter's own suite passes (observed `C1_R49_SELFTEST: cases=34
  failed=0`, exit 0).
* Headings are pinned by exact text and counted (`target_sections`, `counts[h] != 1` → `missing` →
  `+1` each), so deleting/renaming/duplicating a target section cannot pass.
* Floors pin pointer count, so *removal* of citations is caught; only substitution is not (F1).
* The base `before` line is reproducible: `control/c1-CTL_0.stdout` at base prints exactly the
  contract's `before` (`sections=64 covered=57 score=6 … unresolved=9 unverified=81 total=105`).
* **The two map self-anchors are correct pointers.** SKILL.md:1250 states that `:…` anchors mean
  "this page"; SKILL.md:1294-1297 is the quoted "anchored source governs" bullet and 1246-1270 the
  service-limits rendering. CTL_K2's `SKILL.md` prefix is therefore a truthful normalization for an
  extractor that does not implement the page's convention — not fabricated provenance. (The census,
  not the control, is at fault: F4.)
* `absent` is *not* a blanket escape for line pointers: an unresolvable `line` pointer with
  `file: null` stays `unresolved` (`measure.py:271-279`), and a resolved pointer marked `absent`
  becomes `not_holds` (`:311` path) — the selftest cases `absent-needs-row` and
  `absent-on-resolved-is-not-holds` cover both.

## Reproduction (all commands relative to the lane; every counter run on a scratch clone)

```
python3 .ufo/evidence/round-49/c1/measure.py --selftest                       # 34/34, exit 0
python3 .ufo/evidence/round-49/c1/measure.py --lane . --rev 8ca67421… --list  # 90 pointers, 8 null
python3 -B <w1>/T49CritC1Contract/ghost_ctl.py "$S"      # CTL_G  -> total=0, absent=90
python3 -B <w1>/T49CritC1Contract/k2_record.py "$S"      # CTL_K2 -> total=0 then total=3 after append
python3 -B <w1>/T49CritC1Contract/record_dep.py "$S"     # lesson-input variant -> total=0 then total=3
git cat-file -t 8ca67421…:.ufo/evidence/round-14/dispositions.json          # blob
git log --oneline -- corpus/lessons/round-48.md                             # 3 commits
```
The three drivers write only inside `$S` (their own clone, work dirs and stdout receipts) and were
removed with `$S`. No tool was installed or upgraded; no pacman transaction was attempted
(host-wide pause respected). No model was passed to any script.

## Summary

1. **F1 (high):** `absent` is uncapped, so CTL_G — seven body rewrites + 90 empty `absent` rows —
   prints `C1_R49_PASS=true, absent=90, total=0` with zero blob reads of any cited artifact; the
   cheapest passing shape is cheaper than the cheapest failing control, inverting the ladder.
2. **F2 (high):** the frozen expected-pass control (CTL_K2) already records `absent` for
   `dispositions.json`, `verification.json`, `capture-context.py`, which are blobs at base;
   `absent` means "not under four roots", so the reference shape encodes false provenance.
3. **F3 (medium-high):** the durability term probes five files only; the CTL_K2 shape pins
   `corpus/lessons/round-1.md` and lapses (`total=3, score 6`) after one appended line, and the
   promotion section's real base lapse is `input-drift:reports/round-1-calibration.md` — unprobed.
4. **F4 (medium):** 21 citation forms (all `§` refs, the glob row, `#box-1`, directory refs,
   truncated digests) are never extracted, 2 template tokens are false positives in the map floor,
   and the page's own `:…`-is-this-page rule (SKILL.md:1250) is unimplemented.
5. **F5/F6 (medium):** `absent` rows need no evidence and are not scored; an empty-`inputs` trace
   receipt satisfies the trace gate, so "trace-bound inputs" binds nothing.
6. **Fix:** allow `absent` only for raws already null in the base census (cap 6), add CTL_G as a
   frozen negative control, inherit directories/uniqueness in `resolve()`, and probe every entry
   input instead of the five `VOLATILE` files.
7. **Survived:** monitor hashes, heading/text/count pinning, floors against removal, base `before`
   reproduction, and CTL_K2's map prefix — which is truthful, not fabricated.
