# C05 — knowledge overlap: where input-keyed cold-read credit belongs

Seat: `TameshiR17.C05KnowledgeOverlap` (connector, wave 1, round 17). Lane tip
read: `98bea7da5801f4bc58e4187690ee1687c8a5061f`. Scope: corpus scan and a
recommendation plus outline. No corpus file was edited; no lane command was
executed; every byte read came from `git show 98bea7d:<path>` or read-only
`grep`/`git grep`. Tool installs: none.

## 1. What the corpus already holds

Census at the dispatch rev: 24 knowledge files —
`git ls-tree --name-only 98bea7d corpus/knowledge/ | grep -c '\.md$'` → `24`.
Provenance headers: `source:` 5, `verified-at:` 5, `recheck:` 5, `ground:` 4 —
`git grep -lE '^<field> *:' 98bea7d -- corpus/knowledge | wc -l` for each field.

| Entry | Ground / axis | What it holds that overlaps this round | What it does **not** hold |
|---|---|---|---|
| `corpus/knowledge/incremental-pin-disposition.md` | `ground: F7` (:4) | The unchanged-inputs predicate from S003/S048 (:16-85); the lane's pin object is one blob/rev/sha and coarser than a reuse predicate (:105-150); §5a measures three legs' unpinned inputs (:208-250); §6 gives the disposition-receipt invariants (:251-283); §8 appends the round-14 empirical correction (:314) | Its scope sentence (:9) is "one bounded method step — how a *content* disposition of the six recorded legs must be read". It disposes mutation legs, not instruction credit; `result_reuse` is fixed at `not_established` (:196). No cold-read, ledger or bucket vocabulary exists in it |
| `corpus/knowledge/repeated-control-precondition.md` | `ground: F3` | Retained-receipt discipline; a clean verdict names its finite sample; §3.2 is a receipt table (:56-68) | Controls, not credit; no notion of a verdict whose inputs moved |
| `corpus/knowledge/witness-scoped-kill-verdict.md` | `ground: F2` | Verdict attribution needs a declared object before the run (:19-25); errata are append-only (:56) | Aggregate kill verdicts, not instruction-bucket credit |
| `corpus/knowledge/verification-patterns-fleet.md` | no `ground:` (census) | P1-P10 and D0-D10, incl. P7 "anything changed after verification must carry its own proof" and D9 receipts (:50-66, :164-171) | A census of *other lanes'* verifier shape; its bar is ≥2 independent lanes (:14, :22). No input-keyed credit rule |
| `corpus/knowledge/fleet-kill-rate-ledger.md` | no `ground:` | Standing per-leg rows and stale-successor triggers; receipts are row-bound | Mutation legs only |
| `corpus/knowledge/mutation-score-semantics.md` | `ground: F1` | Verdict vocabulary map | Score arithmetic |

Negative sweep (this is the "negative claim carries its sweep" evidence):
`for p in credit restraint cold-read coldread box-3 'box 3' input-keyed; do
grep -rliF "$p" corpus/knowledge/*.md | wc -l; done` → `0` for every term
(working tree at the read; `git status --porcelain` listed only `.gitignore` and
`.ufo/evidence/round-16/round-gate/runner-sha256.txt` as modified, so the
knowledge bytes equal HEAD). No `knowledge/` entry covers it. `corpus/README.md`
mentions cold-read and credit only in round-16 status prose (:144-146, :160,
:190, :207, :219-234 — "full-page cold-read or promotion credit", "cold-read is
calibration evidence"), never in a coverage-map row for a credit ground; no row
indexes a note on input records or verdict invalidation.

Frontier: F1-F10 only — `git show 98bea7d:corpus/README.md | grep -nE '^\| F'
…` shows F7 at :84 (`incremental re-sweep granularity … open`) and F10 at :87;
`grep -n F11` → no hits. The README rule at :72-74: "A ground moves to held only
through an admitted `knowledge/` entry with a `source:` header citing a `mined`
`SOURCES.md` row." No frontier row describes verification-artifact credit
freshness.

## 2. The delta this round adds (why the existing entries cannot absorb it)

The round-16 closure routed the hole as `R16-C2b`
(`corpus/lessons/round-16-verifier-spotcheck.md:226`), and its §2 states why C2
failed (:94-121): the ledger credits a bucket by its section sha, so the bucket
`## Effective expectation reconciliation — round 14` (`SKILL.md:1563-1596` at
`98bea7d`) kept the CR26 credit taken at page sha `97cf436b` against runner
`75ed934d`, while the runner moved to `0673d2e5` and the bucket's step 3
(`SKILL.md:1584`; step 2 at :1581) now returns exit 2
`expected_input_digest_mismatch`.

The v1 rule is exactly the credit function in
`.ufo/evidence/round-16/measure.py` at the dispatch rev:

- `entry_credit_reason` (:178-216) is a function of verdict, `blocking_gaps`,
  `wrong_expectations`, `class` and `commands_executed_count` only — no input
  term, no path, no digest.
- `coldread` (:218-260) matches buckets to entries by section sha only
  (`by_sha` at :243-248, `matches = by_sha.get(sec['sha256'], [])` at :248).
- `LEDGER_PATH`/`BOX3_LINK` are both the round-16 ledger (:54, :68).

So a non-empty `commands_executed_count` is used as a *proxy* for "the commands
ran", and the bytes those commands opened are never part of the receipt. The
new object is therefore: **credit of an executed instruction bucket, keyed to
the inputs it ran against**. That is a different object from F7's mutation-leg
content disposition: F7 asks "do the recorded target bytes still name the object
in front of us"; this asks "do the inputs the credited commands opened still
hash to what the seat recorded". They share a predicate (S003/S048) but not a
receipt shape, not a failure mode and not a counterexample.

The round's binding contract C adds the instruments that make this measurable:
`measure.py --rev` with the input rule and reasons `inputs-unrecorded`,
`input-missing:<path>`, `input-drift:<path>`; ledger v2 with `read_rev`,
`inputs`, `external_inputs`; `trace-inputs.py` recording successful regular-file
opens under the lane root; `assemble.py` building the ledger from v2 reports.
Naming that instrument family in a knowledge entry is what makes the repair a
reusable method instead of a local patch.

## 3. Decision

**Add `corpus/knowledge/input-keyed-coldread-credit.md`; do not put the method
inside `incremental-pin-disposition.md`. Append at most a pointer paragraph
there (optional, §4 below).**

| Option | Improves | Harms | Verdict |
|---|---|---|---|
| A. Extend `incremental-pin-disposition.md` with the full method | F7 reader gets the transfer | Falsifies the entry's own scope sentence (:9) and its `ground: F7`; F7's next move is "per-leg reuse decisions classified", so a cold-read rule would be mis-mapped; two receipt shapes under one entry with one `ground:` | reject |
| B. New entry only, no pointer | New ground gets its own coverage row; the round-16 routed defect gets a falsifiable home | A future F7 reader can still over-read the predicate as covering credit | acceptable; pointer optional |
| C. New entry + one-paragraph append to §9 of the disposition entry | Both objects keep honest scopes; the shared predicate is stated once and pointed to once | One extra append-only block in a file another seat may be reading this wave | **recommend** |

Reasons, each anchored:

1. **Scope honesty.** The disposition entry's opening sentence (:9) and its
   `ground:` (:4) bound it to the six recorded legs. Appending a second object
   family would silently widen F7 and make that sentence false. CORPUS's
   append-only rule covers *corrections and backlinks*, not new grounds.
2. **One ground, one row.** QUALITY 7 requires the coverage-map row in the same
   round the file lands. A new entry gets its own row; an extension would claim
   ground already indexed under F7 whose next move is unrelated.
3. **Distinct falsifier.** The new entry's red-before is concrete and different
   from F7's: an input-drift case must uncredit an otherwise credited bucket
   (contract C's measure `--selftest`), with the round-14 bucket as the real
   counterexample. F7's falsifier is a disposition row that transfers a rate.
4. **Provenance stays readable.** A fresh entry can carry the trio over its own
   bytes; editing an existing entry's header to cite new instruments would shift
   or overload its provenance line.

Cost: one 24-file corpus becomes 25, one README row, and S003/S048 `used-by`
gains a path (append-only, logged old→new in the round lesson). That is cheap
against the alternative of leaving the round's new rule unrecorded.

## 4. The pointer (only if the L1 wants it)

Append after §8 of `incremental-pin-disposition.md`, never editing §1-§8:

```markdown
## 9. Non-leg application pointer — round 17 (append-only)

The predicate in §2-§3 — reuse is licensed only by unchanged inputs, and change
detection is incomplete — also governs an object this entry does not cover: the
credit a cold-read ledger gives an instruction bucket. That object, its v2 rule,
its measured counterexample and its unpinned closure are held in
`corpus/knowledge/input-keyed-coldread-credit.md`. No claim in §1-§8 moves; F7's
six-leg scope and `result_reuse=not_established` stand. This is a pointer, not a
seventh leg and not a cold-read promotion.
```

If the L1 judges that any append to another seat's file is riskier than the
mis-read it prevents, option B stands on its own.

## 5. Provenance trio required (CORPUS.md)

CORPUS: "Each `knowledge/` entry opens with `source:`, `verified-at:` and
`recheck:`"; the kaika rule adds: when the source is external, `source:` cites
its `S###` row in `corpus/SOURCES.md` alongside the URL and anchor; provenance in
prose or HTML comments is unreadable to a freshness sweep. QUALITY 10 repeats
the requirement and adds that an external source enters through a `SOURCES.md`
row opened in the round that writes it, and that a tier-C row is never sole
support. The lane's five compliant headers show the working shape.

| Field | Requirement | What this entry must put |
|---|---|---|
| `source:` | First line. External: `S###` row + URL + anchor (section/heading, access date, sha256 where fetched). Own-work: path `@ <rev>`, sha256. Multiple sources separated by `;`. | `S003` and `S048` with anchors (S003 §Incremental mode/§Limitations; S048 §Incremental analysis items 4-5 + dependency paragraphs; state "S048 supersedes S047; S041/S047 retained historical" inside the body, not as a new `source-correction:` row). Own-work: `.ufo/evidence/round-17/coldread/{measure.py,trace-inputs.py,assemble.py}` and `ledger.json` at the landing rev with their sha256; the counterexample bucket `SKILL.md:1563-1596` at `98bea7d`. Do **not** cite any of these instruments before it exists at the measured rev (round-16 landing mistake). |
| `verified-at:` | ISO date; may carry the run time/revision like `mutation-case-kumitate-round-gate.md:2` does. | `2026-10-20`, plus the measured rev(s): the landing rev for v2 and `98bea7d` for the counterexample. If the S003/S048 drift greps were not re-run this round, say so here; do not present the cross-object transfer as a freshly re-verified external claim. |
| `recheck:` | ISO date or cadence (`90d`, `180d`, `on-release`) **with a drift command**. All five compliant headers carry a command; four carry a cadence as well, while the round-16 entry carries commands only — so the cadence is the lane's practice, not a census-complete field. | `90d` (the tighter of S003's 180d and S048's 90d, as the disposition entry already chose) with three commands: the S003 `grep -c` and the PIT-URL `grep -c` already recorded in `incremental-pin-disposition.md`'s `recheck:`, and one credit re-measure — e.g. `python3 .ufo/evidence/round-17/measure.py --rev <REV> --ledger-rev <REV>:.ufo/evidence/round-17/coldread/ledger.json` plus the red-before receipt path. State what 0 and what a non-zero mean. |

Lane extras (not the trio, but expected): `ground:` naming the frontier row
(see §6), and `source-correction:` only if a `SOURCES.md` row's `teaches` is
being superseded — not applicable here, S048 already superseded S047.

Corpus obligations that ride with the entry:

- Coverage-map row in `corpus/README.md` the same round (QUALITY 7). Because
  C04FrontierMap also maps the frontier this wave, either take the next free id
  from it or omit `ground:` and write the row as "bounded method note; outside
  admission pending". Do not pre-claim an id another seat may use.
- `SOURCES.md` `used-by` for S003 and S048 gains
  `corpus/knowledge/input-keyed-coldread-credit.md`; current value on both rows
  is `corpus/knowledge/incremental-pin-disposition.md` (11 cells per row,
  i.e. NF=13). SOURCES rule 2: only status/recheck/used-by change in place, and
  each change is logged old→new in the round lesson. No new external row is
  needed; no new fetch is required unless the writer wants a fresh quote.
- Counts carry their command; the negative sweeps (§1) carry theirs; quotes name
  location; [O]/[I]/[U] stay separate; errata append-only; no existing entry is
  rewritten.

## 6. Outline — `corpus/knowledge/input-keyed-coldread-credit.md`

**Header** (lines 1-4): the trio above, then `ground:` (F11 or the id C04/L1
assigns). Optional short subtitle: "Section sha is necessary, not sufficient".

1. **Scope and the claim.** One paragraph, bounded: this entry supports one
   method step — how credit for an executed instruction bucket is invalidated
   when an input its commands opened moves. It does not adopt incremental
   testing, does not re-measure any bucket, does not establish full-page
   cold-read sufficiency, and does not promote. Name the object pair: bucket
   (section sha) vs input record (path → sha256).
2. **Objects and definitions.** What a bucket is (preamble + every `#`/`##`/`###`
   heading outside code fences, trailing blank lines stripped, joined by `\n`);
   what `read_rev` is; what credit means (the v1 credit predicate); what an
   input is (successful open of a regular file under the lane root, `.git/`
   excluded). Cite the sectionizer only from the assembled ledger/measure bytes
   at the landing rev, not from prose.
3. **What the sources license, and what is transfer (O / I).** Quote S003's two
   reuse conditions and its Limitations list (environment, dependencies,
   `.snap`, non-mutated files) and S048's items 4-5 plus the dependency
   paragraphs. Then state the transfer explicitly as [I]: neither page discusses
   an instruction bucket, a ledger or a section hash; the shared predicate is
   "reuse is licensed only by unchanged inputs and detection is incomplete",
   and the cold-read application rests on this lane's own counterexample.
4. **The measured counterexample (O).** The round-14 bucket at
   `SKILL.md:1563-1596`: credit at page sha `97cf436b`; CR26 run against runner
   `75ed934d`; the runner moved to `0673d2e5`; step 2 (:1581) and step 3 (:1584)
   now exit 2 `expected_input_digest_mismatch`; v1 `measure.py` cannot see it
   (`entry_credit_reason` :178-216 has no input term; bucket match by sha at
   :243-248). State what was read and what was not executed by the writer.
5. **The rule (contract, exact).** An entry with
   `commands_executed_count > 0` credits only when its `inputs` is non-empty and
   every input path's blob at `REV` has the recorded sha256; otherwise it is
   uncredited with `inputs-unrecorded`, `input-missing:<path>` or
   `input-drift:<path>`. Entries with no executed commands keep the v1 rules.
   `external_inputs` are reported, never credited. Exit classes: 0 measured,
   2 rev/blob missing, 64 usage. Name the red-before (input drift uncredits an
   otherwise credited bucket) and the green-after (a fresh read records the new
   digest and credits again).
6. **The unpinned closure (U).** What `trace-inputs.py` does and does not see,
   in the same spirit as the disposition entry's §5a: it sees successful opens
   of regular files under the root and records external regular files under
   `/home`; it does not see environment variables, argv policy, `PATH`
   resolution, interpreter or dependency identity, shell-builtin reads, reads
   that fail after open, mtime/permission-only effects, or sibling repos outside
   the root. Mark each arm measured or [U]; the entry is partial if a command's
   input set is not traced.
7. **Receipt invariants and the reader's checklist.** One ledger entry per
   bucket; `read_rev` recorded; `inputs` lane-relative; digests recomputed at the
   measured rev; red-before retained; green-after from a fresh read; no external
   input credited; no v1 ledger rewritten; box-3 link points at the round-17
   ledger. A receipt that omits the unpinned closure is partial even when all
   buckets credit.
8. **Boundaries.** No generality claim (two vendor docs are not two independent
   lanes; PROVINCE). No determinism, correctness or durability claim about the
   instruction. No promotion and no box-3 score. The instrument family is new;
   cite it only at the landing rev with its receipts.
9. **Errata (append-only).** Empty at write.

What the entry must **not** say: that a passing `--selftest` proves the rule
(criterion 22's shape); that a credit means the bucket's instruction is still
correct or complete; that `external_inputs` are safe; that full-page cold-read
is earned; that a seventh leg or a new rate exists.

## 7. Risks and falsifiers

- **Vacuous landing (highest risk).** The entry, README row or SHONEN text
  citing instruments before they exist is exactly round-16's landing mistake
  (`corpus/lessons/round-16.md`, landing rows). Gate the entry on X07/X08/X09
  landing plus the red-before receipt; if they slip, write the entry with [U]
  arms and no result claims, or defer it.
- **Ground-id collision.** C04FrontierMap may assign F11 elsewhere this wave.
  The recommendation degrades safely: use its id, or no `ground:`.
- **Over-read.** A reader may take the pointer in §4 as F7 now covering credit.
  The pointer text says the opposite explicitly.
- **Instrument change during the wave.** If `measure.py` is repaired in wave 2
  after seats read it (criterion 21), any receipt used by the entry must name
  the instrument sha it ran. The entry should carry that sha in `source:`.
- **Falsifier for this recommendation:** a corpus audit finding that the new
  entry duplicates ≥1 section of `incremental-pin-disposition.md` without adding
  an object, a counterexample or a receipt invariant — then option A was right.
  The outline above is written so that only §3's predicate summary overlaps, and
  it points back rather than restating.

## 8. Commands run (all read-only)

| Purpose | Command | Exit / result |
|---|---|---|
| Knowledge census at rev | `git ls-tree --name-only 98bea7d corpus/knowledge/ \| grep -c '\.md$'` | `24` |
| Header census at rev | `git grep -lE '^source *:' 98bea7d -- corpus/knowledge \| wc -l` (likewise `verified-at`, `recheck`, `ground`) | `5`, `5`, `5`, `4` |
| Negative sweep | `for p in credit restraint cold-read coldread box-3 'box 3' input-keyed; do grep -rliF "$p" corpus/knowledge/*.md \| wc -l; done` | `0` each |
| Tree state | `git status --porcelain` | only `.gitignore` and the round-16 receipt modified; corpus clean |
| Disposition scope/anchors | `git show 98bea7d:corpus/knowledge/incremental-pin-disposition.md \| grep -nE '^Scope:\|ground: F7\|^## 3\|^### 5a\|^## 6\|^## 7\|^## 8'` | `:4 :9 :105 :208 :251 :284 :314` |
| v1 credit rule | `git show 98bea7d:.ufo/evidence/round-16/measure.py \| sed -n '175,218p'` | no input term in `entry_credit_reason` |
| Bucket match | `…measure.py \| grep -nE 'by_sha\|matches = '` | `:243-248` |
| Counterexample anchors | `git show 98bea7d:SKILL.md \| grep -nE 'dispositions(-before)?\.json\|evidence-disposition'` | steps `:1581`, `:1584`; registry `:1601`, annotation `:1681` |
| Frontier state | `git show 98bea7d:corpus/README.md \| grep -nE '^\| F(7\|10) \|'`; `grep -n F11` | F7 `:84`, F10 `:87`; no F11 |
| Routed defect | `git show 98bea7d:corpus/lessons/round-16-verifier-spotcheck.md \| grep -n 'R16-C2b\|Why C2 still fails'` | `:226`, `:94` |
| SOURCES rows | python cell split over `S003/S041/S047/S048` | 11 cells each; all `mined`; used-by the disposition entry |

Advisory only: no corpus edit, no frontier edit, no lane command outside
`git show`/`grep`.

VERDICT: holds — add `corpus/knowledge/input-keyed-coldread-credit.md` over the
round-17 instruments (after they land), keep `incremental-pin-disposition.md`
at F7's six-leg scope, and at most append a pointer.
