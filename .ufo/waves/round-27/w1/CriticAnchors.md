# CriticAnchors — round 27, wave 1: attack on the C2 anchoring

Seat: TameshiR27.CriticAnchors (critic, leaf). Content revision
`2227d8338c02aa9a5fd7d95c1a41b76865ad7647`. I did not write the content I attack.

## Verdict

C2's frozen target holds, and the run order holds: the anchors were committed before
the only probe run, and a fresh rerun gives the same four classes. Three of the four
expectations follow from header comment lines that are not executed and that predate the
round. They meet S012's definition in the sense that matters for cancellation.

The anchoring itself is weaker than the counter and its wording suggest:

1. **The counter cannot tell specification-anchored expectations from state-anchored
   ones.** It still reports `classified=4 anchored_holes=4` exit 0 when every anchor is
   replaced by a statement that admits the expectation was copied from the pristine run.
   This was variant V1 below, and it is the strongest counterexample. `classified=4` is
   necessary for C2, not sufficient. The anchoring claim rests on a human reading of
   `anchors.json`, not on anything the counter checks.
2. **All four expectations were written after the round-27 author read the round-26
   pristine outputs, and each matches them exactly.** For three survivors, the header
   implies the value on its own, so this does no harm. For S_PIN_INCLUDES it does not: the
   header line it cites holds for both programs.
3. **S_PIN_INCLUDES is not anchored by its header quote at all.** The prefix rule comes
   from S091, which is about Git object names and is applied here only by analogy. The
   entry and README admit this in prose, but the receipt and the counter's
   `anchored_holes=4` count it the same as the other three.
4. **The entry's restatement of S012 is looser than S012.** The entry says "outside the
   mutated statement"; S012 says "outside the code under mutation". As a recipe for
   future rounds, the entry's wording would accept state-anchored values. The four
   anchors in this round happen not to use any such value.

None of this makes C2 false as frozen. The counter weakness is a defect that can be
fixed; it is not a tradeoff the judge must reject. The wording issues need text changes
only.

## (1) Were the anchors fixed before the probe ran? Yes. Git alone does not prove it; the transcript does.

Command: `GIT_OPTIONAL_LOCKS=0 git -C tameshi-shokunin log --format="%H %cI %s" -- .ufo/evidence/round-27/f8/`

```
2227d8338c02aa9a5fd7d95c1a41b76865ad7647 2026-10-22T09:19:08-03:00 round-27: C2 F8 entry, probe receipt, ...
06a6707904582cc2f268d8a74861c6a8d09dd1fe 2026-10-22T09:17:23-03:00 round-27: C2 anchored expectations and probe, committed before the probe runs
```

- `git diff --stat 06a6707 2227d83 -- .ufo/evidence/round-27/f8/` touches only
  `probe.exit`, `probe.stdout` and `receipt.json`. `anchors.json` and `anchor-probe.py`
  have the same bytes in both commits: sha256 `780e1009fc48…` and `2d9308ba950c…`. Those
  equal the receipt's `anchors_sha256` and `probe_sha256`.
- File times: `anchors.json` 09:15:28, `anchor-probe.py` 09:15:05, `receipt.json` and
  `probe.stdout` 09:17:25.53 (-03:00). The receipt was written 2 seconds after the
  anchors commit.
- L1 transcript (`~/.omp/agent/sessions/.../TameshiR27.jsonl`):
  - Call #128 (12:15:05Z) wrote the probe, and call #135 (12:15:28Z) wrote the anchors.
  - The **only** `anchor-probe.py` run is call #171 (12:17:23Z). It is one bash command:
    `jj-lane.sh commit … -- anchors.json anchor-probe.py`, then the probe writing
    `receipt.json`. The result reads `landed 06a6707…`, then
    `ANCHOR_PROBE: ran=4/4 anchored_holes=4`.
  - No earlier run appears in the transcript, and I found no leftover receipt in `/tmp`
    from before 09:17:23. The search was `find /tmp -maxdepth 3 -newermt 08:50 ! -newermt 09:17:23`.
- Caveats:
  - Commit timestamps are self-asserted and rewritten by jj. For example, `70df8d6`
    carries author date 08:57:30-03:00, about 20 minutes before its contents were written
    (12:15–12:16Z in the transcript). Its committer date (09:17:15) matches. So
    "committed before the probe runs" is shown by the transcript, not by git.
  - Call #171 chains the commit and the probe with `;`, not `&&`, so the probe would have
    run even if the commit had failed. The commit did land.
  - The C2 counter (`c2-measure.py`, call #138, 12:15:52Z) was written 24 seconds
    **after** `anchors.json`. The "frozen at pre-registration" counter was therefore
    designed with the anchors in hand. For example, it accepts `arithmetic` anchors
    without checking them, which is the kind S_OOR_EDGE uses. Its before-value
    `classified=0` at base is true by construction, because `f8/` did not exist at base.
    This is a provenance point, not a false statement: the contract says the counter was
    frozen before the probe ran and before any content edit, and both are true.

## (2) Is a header comment line of the same file "fixed outside the code under mutation" in S012's sense? Yes for these four mutants, with two caveats.

S012 abstract (opened by ordinary fetch, `curl https://arxiv.org/abs/2608.17214`, title
"Oracles That Cannot Fail: Anchoring and the Expectation That Moves With the Fault"):
"An expectation is specification-anchored when composed from values fixed outside the
code under mutation, and state-anchored when it flows, directly or transitively, from
that code. … restrict the predicate to values flowing from the mutate target". Both
quotes in the entry (`oracle-anchored-survivors.md:14-18`) match the abstract.

- **For it:**
  - The header is not executed, so no value flows from it at runtime. A fault cannot
    "move measurement and expectation together" through a comment.
  - All four round-26 edits are code lines: :1312, :1589, :2512 and :1195.
  - The header lines predate both rounds. `git blame` at `1205c66` attributes :35-38,
    :61 and :69-71 to `2075363` (kumitate round-8, 2026-09-28). No one rewrote them
    after round 26 to fit a pristine output.
- **Caveat a, common origin.** `git blame` attributes the mutated code lines (:338,
  :1195, :1312, :1589, :2512) to the **same commit** `2075363`. Header and code share an
  author and a moment, so a misunderstanding in the author's intent would appear in both.
  The entry discloses this (§5, `:78-80`). It limits how independent the anchor is; it is
  not a cancellation channel.
- **Caveat b, the entry's paraphrase is looser than S012.**
  - The entry's own wording: §2 item 1 (`:25-29`) says "anchors outside the mutated
    statement". The README row (`corpus/README.md:422`) and the lesson say "fixed outside
    the mutated code". The `anchors.json` note justifies its anchors as "the mutated
    statements are code lines, so no survivor edit can move them". The §4 recipe
    (`:67-70`) asks for "an expectation the mutant cannot move".
  - Counterexample: the severity table `LINE_OOR: 'error'` at `cite-check.mjs:222` is
    outside the S_OOR_EDGE statement, and that mutant cannot move it. Yet it is a code
    value in the mutate target, so S012 calls it state-anchored.
  - The round's anchors do not use any such line, so the four results stand. The recipe
    as written would admit state-anchored values in later rounds.

## (3) Is S_PIN_INCLUDES honestly anchored, given the header fixes only 7-40 hex? Not by its header quote. It rests on S091 by analogy, which the prose admits and the counted output hides.

- Header :37-39: "Pins: `<rev|…|sha256|pinned>` + optional `sha256`, backticks/whitespace,
  then 7-40 hex." The witness pin is `02bcfdc3dba1`: 12 hex, digest chars 8–20
  (`receipt.json`, `pin_is_leading_substring: false`). It satisfies this line under both
  the pristine (`startsWith`) and the mutant (`includes`). The quote does not separate the
  two programs.
- **Variant V4** removes the S091 anchor and keeps only the header :38 quote. The counter
  still prints `S_PIN_INCLUDES: anchored-hole` and `classified=4 anchored_holes=4` exit 0.
  The counter treats an anchor that discriminates nothing as anchoring.
- The prefix rule appears only in code: :1195 `digest.startsWith(pin.hex)`, and :1219 in
  the rev path. The L1 searched kumitate docs for a pin-prefix rule (transcript call
  #115) and found nothing. My search finds no such statement outside `cite-check.mjs`:
  `git grep -i -E "(prefix|leading|abbreviat).{0,80}(pin|sha256|digest)|…" 1205c66 -- ':!scripts/cite-check.mjs'`.
  The nearest hit, kumitate `corpus/lessons/round-16.md:147` ("abbreviated to their first
  eight hex"), is about another tool's printed digests.
- The expected kind `PIN_MISMATCH` is only *listed* in the header (:61). That a
  `sha256`-marker pin is compared with the digest of the nearest cited file is not in the
  header. It is in code (:1180-1207) and in kumitate `SKILL.md:617-620`, a doc outside the
  code that the round did not cite.
- S091 itself checks out: `curl https://git-scm.com/docs/gitrevisions` gives "The full
  SHA-1 object name (40-byte hexadecimal string), or a leading substring that is unique
  within the repository." It speaks of Git object names, not sha256 content pins.
- [INFERENCE] One unused strengthening: the header's 7–40 range is exactly Git's default
  abbreviation length up to a full SHA-1. Line :37 also puts `rev`/`commit` and `sha256`
  markers under one grammar. That suggests pins are modelled on Git abbreviations, but it
  is still an inference, not a statement.
- What is already honest: `anchors.json:53` (`anchor_strength`), entry §4 `:59-63`
  ("held by convention only … would become a contract change, not a defect"), and README
  `:422` ("one of them held by convention only").
- What is not:
  - `receipt.json` gives S_PIN_INCLUDES `class: anchored-hole` with no strength field.
  - The counter ignores `anchor_strength` and prints `anchored_holes=4`.
  - Entry table row `:47` lists header :38 as an anchor, although it carries no weight for
    the expectation.

## (4) Could any anchored expectation have been read off the pristine output? Yes, all four, and the author read those outputs first.

- Before writing `anchors.json` (#135, 12:15:28Z), the L1 read:
  - `corpus/knowledge/mutation-case-kumitate-cite-check.md` (calls #85 and #127);
  - the round-26 probe reports `ProbeSOOREDGE.md`, `ProbeSSTRICT.md` and
    `ProbeSPININCLUDES.md` with their exit lines (calls #106, #109 and #112, 12:13:34–12:13:52Z).
- Rows `mutation-case-kumitate-cite-check.md:89-92` record the pristine results: exit 1
  `LINE_OOR`; pristine DRIFT under `--strict`; exit 64; `PIN_MISMATCH` exit 1. Each
  `expect` record equals the matching pristine observation.
- The round-27 witnesses use the same shapes as round 26: line n+1 of a 20-line file; one
  warning under `--strict`; an unknown flag; an interior digest slice.
- Committing before the run protects only against fitting to the round-27 run. It cannot
  protect against fitting to round-26 pristine outputs already in the corpus.
- Whether it matters, per survivor:
  - S_STRICT is implied by :35 and :69.
  - S_USAGE is implied by :71 and by S090. A fresh fetch confirms: "EX_USAGE (64) The
    command was used incorrectly, e.g., with the wrong number of arguments, a bad flag".
  - S_OOR_EDGE: the witness has 20 lines, so line 21 does not exist. That LINE_OOR is an
    error and errors exit 1 comes from :61 and :69.
  - For those three, the value would be the same without the pristine.
  - For S_PIN_INCLUDES, the prefix direction and the `PIN_MISMATCH` kind appear only in
    the code and the pristine output, plus the S091 analogy. That one is read off state
    with an outside convention added afterwards.
- No search for contrary anchors is recorded.
- The counter cannot detect any of this; see V1.

## (5) Does `anchored_holes=4` overstate anything the entry or README says?

The prose surfaces mostly avoid overstating:

- the entry, §4 and §5;
- the README row: "4 anchored holes, one of them held by convention only";
- the lesson's rejected reading, `corpus/lessons/round-27.md:49-51`;
- SCORECARD `:1358`: "reported as observed".

Overstatements remain in four places:

- **`c2-measure.py` docstring:** it "Counts … survivors that are classified against an
  independently anchored expectation". V1 and V3 refute that: the counter counts
  state-anchored and irrelevant anchors the same way.
- **QUALITY 54** (`corpus/QUALITY.md:603-611`) is true about byte binding. A reader could
  take binding as evidence of anchoring; V1 has a bound receipt with no anchoring.
- **"Independently anchored" versus entry §5.** The entry says header comments "are not
  an independent specification document" (`:78-80`). The README F8 criterion
  (`corpus/README.md:85`) and its round-27 status move (`:424-427`) speak of an
  "independently anchored expectation". By the entry's own §5:
  - S_STRICT is header-only;
  - S_OOR_EDGE's exit and kind still come from the header;
  - S_PIN_INCLUDES rests on analogy;
  - only **S_USAGE** has its whole expectation fixed by an outside source (S090).

  F8's "partly held" needs one such survivor, and S_USAGE supplies it. "4 anchored holes"
  is true only if same-author header text counts as anchoring.
- **Machine output:** `receipt.json` and the counter's `anchored_holes=4` do not separate
  three header-anchored holes from one convention-anchored hole.

## Strongest counterexample: the counter passes tampered anchors

All runs were in my own clone `/tmp/r27-critic-anchors/lane`, checked out at `2227d83`.
For each variant I edited `anchors.json`, regenerated `receipt.json` with the committed
probe, committed **in the clone only**, and ran
`python3 .ufo/evidence/round-27/c2-measure.py --repo . --rev HEAD`.

| variant | change to `anchors.json` | counter output | exit |
|---|---|---|---|
| baseline `2227d83` | none | `classified=4 anchored_holes=4` | 0 |
| V1 | every survivor's anchors replaced by `{"kind":"arithmetic","statement":"copied from the round-26 pristine output (state-anchored)"}` | `classified=4 anchored_holes=4` | 0 |
| V2 | S_PIN_INCLUDES `expect` set to the mutant's behaviour `{"exit":0}`, same anchors | `classified=4 anchored_holes=3` (S_PIN_INCLUDES `anchor-disagrees-with-pristine`) | 0 |
| V3 | S_STRICT anchors replaced by an unrelated header line (:71 `64 usage error.`) | `classified=4 anchored_holes=4` | 0 |
| V4 | S_PIN_INCLUDES keeps only header :38 | `classified=4 anchored_holes=4` | 0 |

Why it passes:

- `anchor-probe.py` never reads the `anchors` array. Its oracle is the `expect` record
  alone (`meets`, `anchor-probe.py:83-87`).
- `c2-measure.py` checks only three things: the quotes appear on the named line or row,
  the receipt is byte-bound, and the receipt has a class. It accepts any `arithmetic`
  anchor without a check (`elif an['kind'] != 'arithmetic'`).
- So "classified" measures form and binding, not whether the expectation follows from
  its anchors.

Rerun of the committed probe in the clone: `ANCHOR_PROBE: ran=4/4 anchored_holes=4`, same
classes and the same probe and anchors sha256, node v24.21.0. The `stdout_sha256` fields
differ from the receipt for S_OOR_EDGE, S_STRICT and S_PIN_INCLUDES, and match for
S_USAGE. [INFERENCE] The likely cause is that the JSON output embeds the random temp-dir
paths. A rechecker told to "compare every result field with the committed receipt"
(transcript call #216) will see three mismatches that mean nothing.

## What evidence would make C2 false

- A run of `anchor-probe.py`, or of the pristine and mutant on these witnesses, before
  `06a6707`, with the anchors changed afterwards. None is in the L1 transcript; the only
  run is #171.
- A header anchor line edited after round 26. None: blame shows `2075363`, 2026-09-28.
- A survivor edit, or any mutant in the round-26 spec, that touches a cited header line.
  None: all four edits are code lines.
- A fresh rerun that changes a class. None: my rerun gives four `anchored-hole`.
- For S_PIN_INCLUDES specifically: a statement by the gate owner, or a kumitate doc, that
  substring pins are legal. That would turn its class into `mutant-meets-anchor`, which
  the entry already concedes. No such statement exists at `1205c66`.
- At the level of the claim: if C2 is read as "the counter shows the expectations are
  specification-anchored", V1 already makes it false. If it is read as "an executed probe
  judged each survivor against an expectation composed outside the code, as reviewed",
  it stands for three survivors and stands by convention for the fourth.

## Impacted axes

- **Coverage (F8):** the claimed axis. It holds as a reviewed claim; the counter's
  evidential weight is overstated.
- **Calibration:** wording in the counter docstring, QUALITY 54, and README "independently
  anchored" against entry §5.
- **Provenance:** the counter was written after the anchors; jj commit dates are
  self-asserted.

## Smallest safe correction

These are text changes, except the counter rule in item 4, which belongs in a next-round
counter because round-27 counters are frozen evidence.

1. **Entry §2 item 1 and the §4 recipe; README `:422`.** Replace "outside the mutated
   statement" and "fixed outside the mutated code" with S012's predicate: "no code line or
   run of the mutated file supplies it (non-executed header text, outside sources,
   witness arithmetic)". Change the recipe from "an expectation the mutant cannot move" to
   "an expectation that does not flow from the mutate target".
2. **Entry §3 and the README row.** State the count as "3 header-anchored (S_USAGE also by
   an outside source) + 1 convention-anchored". In row `:47`, mark header :38 as
   non-discriminating (both programs satisfy it).
3. **`c2-measure.py` docstring (amendment note) and QUALITY 54.** Say that "classified"
   means a byte-bound receipt plus verbatim anchor quotes. Say that whether an
   expectation follows from its anchors is a reviewed claim the counter does not check,
   and cite V1.
4. **Next counter, for a QUALITY entry.**
   - Reject an `arithmetic` anchor unless the receipt carries the named witness fact.
   - Require each survivor to have at least one `contract` or `external` anchor whose
     quote contains the expected exit status or finding kind.
   - Make the receipt carry `anchor_strength`.

   Under that rule, V1 and V3 fail, and S_PIN_INCLUDES fails unless an outside quote names
   the prefix rule, which would be an honest result.

## Side finding outside the five questions

- `corpus/SOURCES.md:338` still reads "Next unused id: S090." although rows S090 and S091
  (`:99-100`) were added this round. The append-only convention (lines `:262-338`)
  expects a new line, "Next unused id: S092."

## Commands and sources

- Read-only git with `GIT_OPTIONAL_LOCKS=0`: log, diff, show and blame in tameshi-shokunin
  and kumitate-shokunin; L1 transcript read with python.
- Code ran only in `/tmp/r27-critic-anchors/`.
- Sources opened by ordinary `curl`: arxiv.org/abs/2608.17214, git-scm.com/docs/gitrevisions,
  man.freebsd.org sysexits(3). None was left unopened.
- No tools installed or upgraded. Nothing written outside this report and `/tmp`.
