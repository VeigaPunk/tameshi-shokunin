# tameshi round 60 — lesson (hyaku run 13, 2026-10-30)

L1 `TameshiR60` (attempt 1; fresh-start round under run 13). Base
`9806562c7efc816bd979923e702ef39bc41cade7` (= origin/master, clean tree);
contract `.ufo/evidence/round-60/contract.json`; plan `plans/round-60.plan.md`;
counter `tools/executor-source-pin-measure.py` (installed); freeze
`.ufo/evidence/round-60/freeze.json`; tool commit (measured)
`da2ae6b361de2d6294c6324a02ae141ff6cb482f`.

Fresh-start duty: the last three rejected closures were read before the
claims were declared — round 57 (honest stop, operator wrap-up; no freeze, no
counter scored), round 58 (not admitted: an unpinned claimant executor forged
the C2 tallies; C3 measured), round 59 (honest stop: the frozen counter was
cheat-passable — a fingerprint cheat scored 24/24) — plus the outside
discernment check `corpus/lessons/round-59-verifier-spotcheck.md`, whose
§6 routed eight defects. Every claim below is aimed at one of those routed
defects and is sized so a do-nothing control cannot reach it.

## Claims

- **C1 (operability, capability re-certification; sourced S290).** The
  round-59 executor-source-pin capability is re-certified on an installed,
  discriminating counter: `tools/executor-source-pin-measure.py` — 8 shuffled
  class cells (`equal`, `unrelated`, `execbit`, `changed`, `missing`,
  `symlink`, `corrupt`, `unresolvable`) over 5 declared paths in ONE tool
  invocation per cell, per-run nonce fixtures, an empty-blob declared path,
  and a corrupt cell expecting exit 2. At the round's final lane revision the
  amended `tools/executor-source-pin.py` v2 scores `passed=8/8
  C1_R60_PASS=true`, and every control arm scores `C1_R60_PASS=false`:
  do-nothing tool-absent 0/8, the unfixed v1 tool 7/8 (only the `corrupt`
  cell failing — the red-before for the exit-2 reconciliation), always-accept
  3/8, fingerprint 3/8, sequence 3/8 (3–5/8 across runs, order-shuffled),
  hash-only 3/8, first-path-only 6/8, empty-blob-unsound 4/8. Closes round-59
  routed defects 1, 2, 4 and 7. The claim's before-state is the round-59
  verdict: the counter that certified the capability was cheat-passable, so
  the capability was **not admitted** (honest stop, closure round 59).
- **C2 (calibration).** The round-59 closure's routed defects and
  uncaptured mistakes become tree-checkable records: `corpus/routed-defects.json`
  carries rows `R59.1`–`R59.8` (7 `fixed` with in-tree receipts, `R59.4`
  `open` with its reason), `corpus/QUALITY.md` carries five new criteria
  (111–115), one per round-59 mistake whose `captured-by` was `none`, each
  citing this lesson; `SCORECARD.md` carries the annotation `not admitted
  (honest stop, closure round 59)` on the round-59 C1 capability row and a
  saturation premise restated on the scored axes; and the cold-read precheck
  run at (base `9806562c…` → the round's final revision) is recorded with
  `lost=0`.

## Gate

- Sourced rows opened this round (URL, access date, located quote, word
  count, what it grounds):
  - **S290** — Python, `secrets` module documentation,
    https://docs.python.org/3/library/secrets.html, accessed 2026-10-30
    (HTTP date Fri, 30 Oct 2026 18:38:28 GMT; 36,411 B; extract
    `.ufo/evidence/round-60/sources/s290-secrets.html`). Located quote
    (§module abstract, first paragraph, 25 words): "The secrets module is
    used for generating cryptographically strong random numbers suitable for
    managing data such as passwords, account authentication, security tokens,
    and related secrets." It grounds the per-run nonce fixture design: a
    counter whose fixtures change every run cannot be defeated by a
    content-recognition cheat. `used-by`:
    `corpus/knowledge/executor-source-binding.md`.
  - **S291** — Git, index-format documentation,
    https://git-scm.com/docs/index-format, accessed 2026-10-30 (HTTP date
    Fri, 30 Oct 2026 18:39:52 GMT; extract
    `.ufo/evidence/round-60/sources/s291-indexformat.html`). Located quote
    (§cache entry layout, 9-bit unix permission, 22 words): "9-bit unix
    permission. Only 0755 and 0644 are valid for regular files. Symbolic
    links and gitlinks have value 0 in this field." It grounds the exec-bit
    boundary decision: exactly two permission values for regular files
    (modes 100644/100755) and a symlink as a distinct type, so mode is not
    bound beyond regular-ness. `used-by`:
    `corpus/knowledge/executor-source-binding.md`.
- Rejected this round, with reason and flip condition:
  - **git-ls-tree documentation as the mode ground** —
    https://git-scm.com/docs/git-ls-tree, opened 2026-10-30 (extract
    `.ufo/evidence/round-60/sources/s291-lstree.html`). REJECTED: the page
    documents `%(objectmode)` as a format placeholder but enumerates no
    octal mode values, so it cannot ground "regular modes 100644/100755,
    symlink 120000"; flip: a page that enumerates the mode values would
    carry the row instead. The row was re-targeted to `index-format` (S291),
    which does enumerate them.
- Id collision check before the append: `grep -c 'S290' corpus/SOURCES.md`
  → 0, `grep -c 'S291' corpus/SOURCES.md` → 0 (registry maximum was S289);
  `grep -c 'library/secrets\.html\|docs/git-ls-tree\|docs/git-hash-object'
  corpus/SOURCES.md` → 1 (S103, `git-hash-object` — an existing row, so the
  oid-equality ground was re-used, not duplicated).
- Status / recheck / used-by changes to existing rows, old → new: **S103**
  used-by `corpus/lessons/round-36.md` → `corpus/lessons/round-36.md,
  corpus/knowledge/executor-source-binding.md` (the content-addressed
  oid-equality ground now backs the binding entry too). No other row
  changed; no row was rewritten.
- Census before (round start): `scripts/sources-census.sh validate --root
  /home/vgpnk/Projects/shokunin tameshi` → exit 0, 149 rows, 16 W04
  duplicate-URL warnings and 1 W01 (S101) — all pre-existing. Census after
  the SOURCES append: exit 0, **151 rows**, malformed rows 0, warning set
  unchanged (no new W04/W01 from S290/S291).
- Assimilation: **none** — no `merge/tameshi/` package entry was adopted this
  round; the round's claims are counter-discrimination and routed-defect
  dispositions, and the staged package holds no entry on either ground (the
  package's own counter/mutation entries concern mutation-score semantics,
  not counter discrimination). No shokuknow registry row was appended.
- `considerthese/`: mined — proposal 4/5 of `considerthese/2026-10-28.md` were
  read; the one that fits this round's claims cheaply (a receipt-existence
  linter for records — the discipline criterion 108 already encodes) is
  carried into the ledger work as criterion 111–115 rather than as a new
  claim; the other was not applicable. Reflection is a pointer, not evidence.

## Mistakes

1. **A frozen counter publishes its fixtures, so a content-recognition
   cheat can meet the target (class: non-discriminating counter).** Evidence:
   `corpus/lessons/round-59.md` `## Mistakes` 1 and
   `.ufo/evidence/round-59/controls/cheat-cheat-fp.out`
   (`passed=24/24 C1_R59_PASS=true` for a cheat that never reads `--trusted`).
   Captured-by: **none** in round 59 (its freeze controls were tool-absent
   and do-nothing only). Fix: the round-60 counter derives every fixture
   byte and commit message from a per-run nonce (S290) and shuffles the class
   order, so the same cheat scores 3/8
   (`.ufo/evidence/round-60/controls/ctl-fingerprint.out`); criterion 111 now
   requires a cheat family before a counter certifies anything.
2. **A counter's invocation shape can under-cover the tool's declared
   interface (class: coverage hole in the predicate).** Evidence:
   `corpus/lessons/round-59.md` `## Mistakes` 2 — the round-59 counter
   invoked `--path` once per call, so a first-path-only strawman scored
   24/24. Captured-by: none. Fix: the round-60 counter declares all five
   paths in ONE invocation per cell, with the `symlink` cell on paths[1] and
   the `corrupt` cell on paths[3]; the first-path-only strawman now scores
   6/8 (`.ufo/evidence/round-60/controls/ctl-first-path-only.out`);
   criterion 112.
3. **A quote's word count drifts between the lesson and the source (class:
   reference-drift).** Evidence: `corpus/lessons/round-59.md` `## Gate`
   records the S289 quote as 17 words; the quote is 18 words (the round-59
   spot-check §6 item 8 names it). Captured-by: the QUALITY rule that a
   quote names its location — present, but it does not require the count.
   Fix: the round-59 lesson is left byte-unchanged (append-only) and the
   erratum is recorded here; every Gate quote in this lesson carries its
   word count (25 for S290, 22 for S291).
4. **A counter's control family can be strong while its positive arm is
   untested against the tool's own plumbing failures (class: coverage hole
   in the predicate).** Evidence: the round-59 counter had no cell in which
   the tool's blob read fails at plumbing level, so the tool mapped that
   arm to DRIFT (exit 1) while its own decision table said exit 2 — the
   mismatch the round-59 spot-check §6 item 7 named. Captured-by: none. Fix:
   the round-60 counter's `corrupt` cell deletes the candidate's loose blob
   object and expects exit 2; the unfixed tool scores 7/8 with only that
   cell failing (`.ufo/evidence/round-60/controls/v1-tool-red.out`), and the
   v2 tool maps the arm to `EXECUTOR_SOURCE_UNAVAILABLE`
   (`tools/executor-source-pin.py:249-266`).
5. **A freeze that digests nonce-bearing receipts can never re-verify against
   the tree (class: reference-drift).** Evidence: `.ufo/evidence/round-60/freeze.json`
   digests 16 files, 7 of which are counter receipts whose bytes carry a
   per-run nonce and a shuffled class order. After the control family was
   re-run at the certified revision, a naive re-verification of the freeze
   reports 7 mismatches and cannot distinguish a re-run receipt from a
   tampered instrument. Captured-by: none — the freeze has no instrument/receipt
   distinction to test. Fix: `.ufo/evidence/round-60/freeze-verify.py`
   classifies the comparison and reports `FREEZE_VERIFY instrument=10/10
   receipt=9/16 verdict=INSTRUMENT-OK (receipts re-run)`
   (`.ufo/evidence/round-60/freeze-verify.json`): every frozen INSTRUMENT
   digest still matches, and the pre-data receipt bytes remain recoverable
   from the freeze commit (`git show da2ae6b361de2d6294c6324a02ae141ff6cb482f:.ufo/evidence/round-60/controls/ctl-fingerprint.out`).
   Criterion 117 now requires the distinction.

6. **An instrument (and its counting command) can be bound to the dispatch
   host it was born on (class: host-scoped-instrument).** Evidence: the
   round-60 attempt-1 receipts and counting commands carry the old Linux
   host's invocation shape (`python3`, `/home/vgpnk/...`), and on the win32
   dispatch host `python3` is the Microsoft Store stub (exit 49, no
   version) while the lane path does not exist — so attempt-1's C1 counting
   command cannot execute at adjudication here, and the frozen instrument
   itself crashes before any verdict
   (`.ufo/evidence/round-60/win-host/red-v1-counter.err`):
   `UnicodeEncodeError: 'charmap' codec can't encode characters` (under
   `-I`, the interpreter ignores `PYTHONUTF8` — all `PYTHON*` env vars are
   ignored in isolated mode per the S073 page — so fixture writes used the
   locale codec cp1252, which cannot encode the 日本語 fixture content),
   followed in the same receipt by `PermissionError: [WinError 5]` from
   `shutil.rmtree` on git-for-windows' read-only loose objects (the
   `--work` cleanup arm fails and leaves residue). Captured-by: none — no
   criterion required a host-scope statement or a portable re-statement
   before attempt 2 (criterion 118 is the fix). Fix: the host-portable
   counter revision `tools/executor-source-pin-measure-v2.py` (same cells,
   class set, expecteds, invocation shape and PASS design; only
   host-portability plumbing differs), its own freeze
   (`.ufo/evidence/round-60/win-host/freeze-v2.json`), portable counting
   commands, and criterion 118. The v1 instrument bytes stay frozen
   (`freeze-verify` at the attempt-2 tree: `instrument=10/10`,
   `INSTRUMENT-OK (receipts re-run)`).
7. **A claim sentence can pin a control arm's score when the arm is
   order-dependent by design (class: over-specified-predicate).** Evidence:
   the attempt-2 C1 sentence (frozen in
   `.ufo/evidence/round-60/win-host/contract-a2.json`) pinned "sequence
   3/8" copying the Linux receipts' modal score; the first scored family on
   this host drew an order scoring **1/8**
   (`.ufo/evidence/round-60/win-host/first-family/ctl-sequence.out`) — red,
   within the control's design, and false to the sentence as written. The
   sequence control answers with a fixed exit cycle `[0,0,1,1,2,1,0,2]`
   keyed by call index while the counter shuffles the class order, so its
   score is a property of the order drawn (attempt-1's own lesson already
   said "3–5/8 across runs, order-shuffled"). Captured-by: none — nothing
   required a sentence to distinguish deterministic arms from
   order-dependent arms. Fix: amendment A1
   (`.ufo/evidence/round-60/win-host/contract-a2-amend1.json`, frozen in
   `freeze-amend1.json` before the second scored family) re-states the
   sentence with the sequence arm described as order-dependent-red, the
   scored family was re-run post-amendment at
   `ffa5660246163be6cb1497849692b43ef3e2bd9c`
   (`.ufo/evidence/round-60/win-host/amend1/`), and criterion 119 is
   reserved for the rule (deterministic and order-dependent arms are named
   as such in a claim sentence). Analysis recorded so the kill rule is
   priced honestly: the cycle aligns with the shuffled expecteds on
   3!·3!·2!/8! = 1/560 of orders; on such an order the control scores 8/8
   and kills the counter per the kill rule — a per-run hazard both
   attempt-1's and attempt-2's scored runs carried (neither drew it).
8. **A no-harm monitor that cannot run on the host that edited the records
   leaves record edits unpoliced (class: host-infeasible-instrument).**
   Evidence: the round-48 precheck ran in minutes on the Linux host
   (attempt-1 receipt `lost=0`), and on the win32 host it needs ~112
   min/rev (75,889 recorded inputs x 2 git spawns per input per rev x
   0.044 s per spawn, measured); five completion attempts failed (status
   receipt `.ufo/evidence/round-60/win-host/amend1/coldread-precheck.out`),
   so attempt-2's record edits went unpoliced until a lane-authored
   substitute (noharm-cand.py: the frozen decision functions plus a
   proven-safe fail-fast short-circuit on changed input paths) measured a
   provisional 4-section credit drop. Captured-by: none — no criterion
   required the lane's no-harm instrument to be host-portable or to have a
   bounded fallback. Fix: the round-61 re-read obligation (see Honest
   limits) plus the committed host-feasibility analysis (spawn-rate
   measurement, ledger size, five run receipts); a portable or bounded
   form of the monitor is round-61 design work, not claimed here.

## Wave w1 — what was actually executed, and what was not

The wave was handed off as ONE batched dispatch of **32 seats** (policy band
32–48; the operator's final ruling fixed the band at exactly 32, which this
wave matched). The host's usage cap settled the wave after **2 of 32 seats**
ran: `w1-results.json` records `seats: 32, settled: 2,
dead_or_never_spawned: 30`, and the 30 never spawned (tranche fill halted by
the cap). They are reported as cap-cancelled, not as failed seats.

| Seat | Role | What it did | Verdict |
|---|---|---|---|
| `T60W1S01` | executor | Independently reproduced the red-before on a scratch fixture it built itself: the unfixed v1 tool exits 1 `EXECUTOR_SOURCE_DRIFT` when the candidate blob cannot be read, and genuine drift produces the same token — v1 cannot tell a plumbing failure from real drift. Cause: `blob_bytes()` returning `None` is folded into the DRIFT branch (`tools/executor-source-pin.py:249-256` at `9806562c…`). | red-before independently reproduced |
| `T60W1S02` | executor | Green probe ×2 over the amended tool v2 with the working-tree counter: both runs `passed=8/8 C1_R60_PASS=true`, exit 0, nonces `8e61bb8702ebd036` ≠ `4bde7d5306c5f89e`, different class orders, and the five-path invocation evidenced by the tool's `5 declared source blob(s) equal trusted blobs` line (a four-path call would print `4`). | probe PASS (explicitly not certification) |

**Falsification credit is limited to these two seats.** The round's claims rest
on the L1's own committed instruments and their control family (eight arms,
all red, plus the frozen digest check), not on a wide independent panel: the
30 cap-cancelled seats include every planned reviewer, critic,
mutation-tester, connector, scout and sentinel seat, so no outside-of-the-L1
attack on the counter landed this round. The closure session may read the
claims as under-falsified on that ground, and the round says so rather than
counting unrun seats as credit.

Two seat findings are adopted into the lane's records:

- `T60W1S02`'s precision note — the counter's results JSON records
  `class/expected/exit/stdout/stderr` per cell, not the argv it used, so the
  empty-blob declared path is evidenced by the argv construction and the
  tool's own "5 declared source blob(s)" line rather than by a literal path
  string in the receipt. Recorded here as a known limit of the receipt's
  self-description; the counter is **not** changed, because its bytes are
  frozen (`.ufo/evidence/round-60/freeze.json`) and the kill rule forbids
  changing the instrument after the first scored run.
- `T60W1S01`'s root-cause reading of the v1 arm (`blob_bytes()` returning
  `None` folded into DRIFT) — the same arm the v2 tool now maps to exit 2;
  the reading is independent confirmation of the defect's mechanism.

## Verdicts

- **C1, measured.** Before (the round-59 verdict): the counter that
  certified the capability admitted a fingerprint cheat at 24/24, so the
  capability was **not admitted** (honest stop, closure round 59). After, at
  `da2ae6b361de2d6294c6324a02ae141ff6cb482f`: `passed=8/8
  C1_R60_PASS=true`, exit 0 (`.ufo/evidence/round-60/after/cert.out`), and a
  second run at the same revision with a different nonce and class order also
  scores 8/8 (`.ufo/evidence/round-60/after/cert-repeat.out`). Controls:
  do-nothing tool-absent 0/8, v1 tool 7/8 (corrupt only), always-accept
  3/8, fingerprint 3/8, sequence 3/8, hash-only 3/8, first-path-only 6/8,
  empty-blob-unsound 4/8 — every arm `C1_R60_PASS=false`
  (`.ufo/evidence/round-60/controls/`). The counter's digest is frozen
  (`.ufo/evidence/round-60/freeze.json`, sha256 `c136561d…`) and matches the
  committed bytes. **Admission remains an operator ruling**: the capability
  row is annotated `not admitted (honest stop, closure round 59)` and the
  round-60 row is written as "lane demonstrated; admission pending".
- **C2, measured.** Before (base `9806562c…`): R59.* ledger rows 0, QUALITY
  criteria citing the round-59 lesson 0, the SCORECARD annotation 0 — the
  do-nothing control receipt. After: 8 rows (7 `fixed`, 1 `open` with its
  reason), 6 QUALITY citations of `corpus/lessons/round-59.md` (criteria
  111–115 plus the section preamble), 2 matches for the annotation string,
  and the cold-read precheck recorded at the round's final revision with
  `lost=0`.

## Next-round carry

- Author-independent trust for the binding itself stays outside the lane's
  claims (F11's remaining ground); the lane does not claim it.
- `R59.4` stays open: the seat-result completeness check belongs to the
  wave validator in the ufo-fsd-alpha checkout, outside this lane's write
  scope; the lane-side criterion 114 is the mitigation.
- The counter's remaining honest limits: one fixture repo per run, one
  declared path spelling set, and no packed-object or promisor-partial
  failure modes (the `corrupt` cell deletes a loose object only).

## Attempt 2 — win32 host-portability re-run (2026-10-31)

L1 `TameshiR60a2` (attempt 2; `zcode run14`; the dispatch host is a NEW
Windows host — the old Linux host `/home/vgpnk` does not exist here). Base
`9bc9b20b5d6723a19d1b69c8edd7246f82ea3d78` (= origin/master; attempt-1's
round-60 work is committed lane state). Contract
`.ufo/evidence/round-60/win-host/contract-a2.json`; amendment A1
`.ufo/evidence/round-60/win-host/contract-a2-amend1.json`; plan
`plans/round-60-attempt2.plan.md`; counter revision
`tools/executor-source-pin-measure-v2.py` (digest `429cb204bb61…`, frozen
`.ufo/evidence/round-60/win-host/freeze-v2.json` pre-data); freeze verified
at the final tree: `FREEZE_VERIFY instrument=4/4 receipt=2/2
verdict=FROZEN-INTACT` (freeze-v2), `instrument=1/1 FROZEN-INTACT`
(freeze-amend1), and attempt-1's freeze still `instrument=10/10
INSTRUMENT-OK (receipts re-run)` — the v1 bytes were never touched.

Fresh-start duty: the last three rejected closures (r57, r58, r59) and the
round-59 spot-check were re-read before declaring; attempt-1's instruments
were then spot-checked ON THIS HOST before any claim was declared. Ruled
out: re-running attempt-1's C1 counting command as a claim (it cannot
execute here — the r58/r59 rejection shape); extending the counter's
failure modes this round (a new predicate on an instrument the host cannot
run); re-litigating attempt-1's C2 counts (tree-checkable here with
`python` for `python3`; their host scope became C2's record instead).

Host facts (probe receipt `.ufo/evidence/round-60/win-host/host-probe.txt`):
`python3` on PATH is the Microsoft Store stub (exit 49); `python` is
3.13.15; `PYTHONUTF8=1` is set in the dispatch env but `-I` ignores it
(S073 page, §-I: "All PYTHON* environment variables are ignored, too");
symlinks are creatable (Developer Mode); git 2.55.0.windows.3 with
`core.symlinks=false`. On this host the symlink cell's DRIFT is produced by
the content/mode the worktree can express (`git add` with
`core.symlinks=false`), not by a 120000 tree entry — the expected verdict
(exit 1) is unchanged; the mechanism difference is recorded, not absorbed.

### Gate (attempt 2)

- Sourced rows opened or re-opened this round:
  - **S292** (new) — Git `git-update-index` documentation,
    https://git-scm.com/docs/git-update-index, fetched 2026-10-31 (HTTP
    date Sun, 01 Nov 2026 02:28:15 GMT; 84,442 B; extract
    `.ufo/evidence/round-60/win-host/sources/s292-update-index.html`).
    Located quote (§Options, `--chmod=(+|-)x`, 8 words): "Set the execute
    permissions on the updated files." It grounds the exec-bit cell's
    index-mode force: with `core.fileMode=false` (the git-for-windows
    default) a worktree chmod alone never reaches a commit and the
    candidate would collapse to the trusted tree; `update-index --chmod=±x`
    sets the mode the commit records. `used-by`:
    `corpus/lessons/round-60.md` (this section).
  - **S073** (re-opened, re-used — not duplicated; the lane's S103
    precedent for a held URL) — Python command line and environment,
    https://docs.python.org/3/using/cmdline.html, re-fetched 2026-10-31
    (HTTP 200; 171,073 B; extract
    `.ufo/evidence/round-60/win-host/sources/s073-cmdline-refetch.html`).
    Located quotes (both ≤25 words): "-X utf8 enables the Python UTF-8
    Mode." (§-X, 7 words) and "-I option can be used to run the script in
    isolated mode … All PYTHON* environment variables are ignored, too."
    (§-I, 24 words). They ground the two encoding halves of mistake 6: the
    frozen instrument's `-I` discipline ignores `PYTHONUTF8`, so on win32
    the locale codec (cp1252) decided fixture bytes; `-X utf8` is the
    route that survives `-I`. `used-by` old → new:
    `corpus/knowledge/guard-kill-closure.md` →
    `corpus/knowledge/guard-kill-closure.md, corpus/lessons/round-60.md`.
- Id collision check before the append: `grep -c 'S292' corpus/SOURCES.md`
  → 0 (registry maximum was S291); the cmdline URL is already held as
  S073, so no row was added for it (a second row would be a W04
  within-scope duplicate; CORPUS.md rule 2). No existing row's status or
  recheck changed; only S073's `used-by` moved (old → new above).
- Census: `bash scripts/sources-census.sh validate --root <fleet-root>
  tameshi` exit 0 at round start (151 rows, 16 W04 + 1 W01, all
  pre-existing). First end run: **exit 1 — `E01 S292 fields=12`**: the new
  row's located field carried the git option's alternation notation
  `--chmod=(+|-)x`, whose literal pipe splits the census `-F'|'` field
  count. The byte was fixed to `--chmod=(+/-)x` (same notation, no pipe)
  and the end run exits 0 (152 rows, warning set unchanged at 16 W04 +
  1 W01; receipt `.ufo/evidence/round-60/win-host/amend1/census-end.stdout`).
  The row landed at `c9723e59…` with the broken field and the fix lands
  with the receipts — the census gate caught its own lane's row, which is
  the gate working.

### What landed (attempt 2)

- `tools/executor-source-pin-measure-v2.py` — host-portable revision of the
  frozen counter; deltas from the frozen instrument are plumbing only:
  explicit UTF-8 fixture writes; `-X utf8` child invocation; `git
  update-index --chmod=±x` exec-bit force after `git add -A`;
  read-only-attribute-safe reset/corrupt-cell/cleanup arms; receipt JSON
  ASCII-escaped; receipt lines name the producing instrument digest.
- Amendment A1 after the first scored family (mistake 7): the C1 sentence's
  sequence clause re-stated order-dependent-red; second scored family run
  post-amendment.
- C2 records: `corpus/QUALITY.md` criteria 118 (host scope + instrument
  revision named) and 119 (deterministic vs order-dependent arms named in a
  claim sentence); `SCORECARD.md` attempt-1 rows annotated `counting
  command host-scoped (linux)` with the win32 re-statement pointer, plus
  the attempt-2 measured rows; `PROVINCE.md` dated host correction
  (line-66 template path recorded absent 2026-10-31; real win32 surfaces
  named); portable re-statements of attempt-1's C2 counting commands in the
  round report.

### Verdicts (attempt 2)

- **C1, measured.** At the measured revision
  `ffa5660246163be6cb1497849692b43ef3e2bd9c`: `C1_R60V2 rev=ffa566024616…
  passed=8/8 C1_R60V2_PASS=true`, exit 0, twice — nonces
  `c42003b92a32fe13` ≠ `056cf07669067d49`, class orders `esucmcue` ≠
  `ueceusmc`, instrument digest `429cb204bb61…` matching freeze-v2 —
  `.ufo/evidence/round-60/win-host/amend1/cert{,-repeat}.out`. Controls,
  every arm `C1_R60V2_PASS=false` (same directory): do-nothing
  tool-absent 0/8 (`reason=tool-absent`) · v1 tool 7/8 (corrupt only —
  the same red the Linux receipts show) · always-accept 3/8 · fingerprint
  3/8 · hash-only 3/8 · first-path-only 6/8 · empty-blob-unsound 4/8 ·
  sequence 1/8 (order-dependent draw; first family drew 1/8 at
  `c9723e59…` too: `first-family/ctl-sequence.out`). The first family at
  `c9723e59d0f517689cb61dd518cd9e0e58b9a2c1` is kept under
  `first-family/` as the run that surfaced mistake 7.
- **C2, measured.** Counting commands (portable forms, run at the final
  revision): `grep -c '### Criterion 118' corpus/QUALITY.md` → 1;
  `grep -c '### Criterion 119' corpus/QUALITY.md` → 1;
  `grep -c 'counting command host-scoped (linux)' SCORECARD.md` → 2;
  `grep -c 'recorded absent 2026-10-31' PROVINCE.md` → 1;
  `grep -c '^## Attempt 2' corpus/lessons/round-60.md` → 1. All five at
  base `9bc9b20b…` score 0 (`git show` pipes) — the do-nothing receipt is
  in the round report.

### Honest limits (attempt 2)

- The capability row stays "lane demonstrated; admission pending" —
  admission is an operator ruling; this attempt widens the demonstration
  to a second host class and changes nothing about author-independence.
- The falsification panel is again thin: the L2 surface named by
  MISSION.md (one batched AgentSwarm call on the Kimi host) does not exist
  on this host, and the round's one batched wave (attempt-1's, 32 seats)
  was settled 2/32 by the host usage cap, with every attack seat among the
  30 cap-cancelled. This attempt did not re-roll a wave against that cap;
  the host's available batched-subagent surface is gated on an explicit
  operator request by its own contract, so the decision is routed to L0
  (`.ufo/l0-questions.md`) and the claims rest on the committed
  instruments, their ten-arm red family, two independent green runs, and
  the freeze verifications — every receipt re-runnable by the closure
  judge on this host.
- The sequence control's 1/560 kill hazard (mistake 7) is a property of
  the round-60 counter family design, not new; it is now priced in
  writing.
- **No-harm arc (attempt 2's own catch, honestly carried).** The frozen
  no-harm instrument (round-48 precheck) cannot run on this host: the
  round-21 ledger records 75,889 inputs, the monitor spawns ~151,778 git
  processes per measured rev, and a spawn costs ~0.044 s here -> ~112
  min/rev (status receipt
  `.ufo/evidence/round-60/win-host/amend1/coldread-precheck.out`; five
  runs attempted, none completed). In its place, noharm-cand.py ran the
  frozen module's own decision functions with a proven-safe fail-fast
  short-circuit on the changed input paths and measured **46 of 64
  sections credited at the attempt-2 cand** against the frozen
  instrument's own **50 credited at b1ba0ebc** (attempt-1's receipt) — a
  provisional drop of up to 4 sections, attributable across attempt-1's
  two unmeasured tail commits and attempt-2's record edits (PROVINCE,
  QUALITY, SOURCES, SCORECARD, LOG are all ledger-recorded inputs), with
  the split unmeasured here. Consequence, applied honestly: **this
  attempt does not self-admit.** C1 and C2 measure true, but the no-harm
  guard is unverified with a provisional regression on record, and a
  trade anywhere is not an improvement. Remedy routed to round 61 as its
  first obligation: genuine re-reads of the affected SKILL.md sections,
  recorded as fresh input-keyed ledger entries pinning post-edit hashes
  (schema `tameshi-coldread-ledger-v2`; entry requires
  commands_executed_count>0 and a committed
  `tameshi-trace-inputs-v1` trace receipt whose `inputs` match the
  entry's), then a re-run of the monitor at the final revision until
  lost=0. Mistake 8 records the class.
- `python3`-spelled commands in historical records (attempt-1 receipts,
  freeze-verify/pointer-sweep usage lines) remain historical records; the
  portable spellings are in this lesson and the round report.
