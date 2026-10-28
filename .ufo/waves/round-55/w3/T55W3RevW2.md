# T55W3RevW2 — wave-2 integrity: 34 seats, dead attempts, and the three `## Standing rules` readers

Role: reviewer (wave 3). Axes: calibration. Milestone: wave-2 integrity.
Snapshot instant for every count below: **2026-10-28T14:49:02** (the directory was still growing; see §1.1).
Nothing in the lane, in `.ufo/evidence/round-55/*` or in the wave specs was modified. All receipts are in
`.ufo/waves/round-55/w2/T55W3RevW2-receipts/`.

---

## 0. Verdict in one paragraph

All 34 wave-2 seats were dispatched (`w2.ready.dispatched`, 34 entries); **26 reports had landed at the
snapshot and 8 had not**, and every one of the 8 belonged to a *live* agent at 14:48 — **no wave-2 seat is
dead at the snapshot**, though **11 of 34 seats (32%) lost at least one attempt and ≥20 attempts died
overall**. The three reader reports are **valid**: each carries `heading = "## Standing rules"`,
`cand = 9cf0146b…`, and `section_sha256 = acfb671a…`, which I re-derived independently with the frozen
round-18 sectionizer over `git cat-file blob C0:SKILL.md` (one match in 64 sections), and **all 12 of their
finding quotes are verbatim in the C0 section bytes**. They are **not content-redundant** with wave 3's
reader (only the `'<value>'` quoting edge appears twice), but they **are binding-redundant**: four valid
candidates now carry the same `(heading, cand, sha)` triple, and the shipped binder
(`.ufo/evidence/round-55/integrate/binder.py`) can bind exactly one. **As shipped it binds none of them**:
`resolutions.json` has no item with a `heading` key, so the findings quota is 0, and the first candidate in
path order (2 findings) trips the loop's `break` — `## Standing rules` is skipped and the binder would exit 1.

---

## 1. Counts: how many of the 34 reports exist

Command and output: `T55W3RevW2-receipts/08-seat-census.txt`, `12-dead-attempts.txt`.

| snapshot (local) | wave-2 reports landed |
|---|---|
| 14:41 | 18 / 34 |
| 14:43:00 | 21 / 34 |
| 14:47:15 | 25 / 34 |
| **14:49:02** | **26 / 34** |

Growth is real, not noise: `T55W2SentConfig2.md`, `T55W2RevNoteNine.md`, `T55W2SimplDiff.md`,
`T55W2RevRound54Wording.md`, `T55W2SentStrayWrites.md`, `T55W2CritDoNothing.md`, `T55W2RevNoHarm.md` and
finally `T55W2RevBaseReceipts.md` landed between 14:41 and 14:52. **Any "N/34" figure must carry its
timestamp**; the wave is not over.

### 1.1 The eight seats that had not landed at 14:49, and their evidence of life

`T55W3RevW2-receipts/08-seat-census.txt`; liveness from `proc://` read at 14:48.

| seat | receipts dir present | live agent at 14:48 | uptime |
|---|---|---|---|
| T55W2CritNinthMode | yes | `T55W2CritNinthMode-3` | 28m01s |
| T55W2MutC2 | no | `T55W2MutC2` | 27m09s |
| T55W2MutTools | yes | `T55W2MutTools-4` | 24m37s |
| T55W2CritClaimShape2 | no | `T55W2CritClaimShape2-3` | 23m03s |
| T55W2RevGateResidual | yes | `T55W2RevGateResidual` | 23m00s |
| T55W2RevMistakes | no | `T55W2RevMistakes-3` | 14m46s |
| T55W2CritC2Scope | yes | `T55W2CritC2Scope` | 14m37s |
| T55W2ExecFloorRekeyProbe | no | `T55W2ExecFloorRekeyProbe-3` | 11m11s |

Four of the eight are past 20 minutes with no report; that is a *risk*, not a death. The 26 landed reports
are all substantive: smallest 3,306 B, every one has a `<seat>-receipts/` directory (receipt 08 plus the
size sweep in this section), 25 of 26 carry fenced command blocks (`T55W2Connector3.md` carries its commands
inline and cites its receipts dir).

## 2. Which seats died

Command and output: `T55W3RevW2-receipts/12-dead-attempts.txt`.

The dispatch map is the ground truth for deaths: a logical seat whose spawned agent id carries a suffix
(`-2`, `-3`, `-4`) lost the earlier attempts of that name.

- **Seats with ≥1 dead attempt: 11 of 34 (32%).** CritNinthMode(-3), CritFreeze2(-2), MutTools(-4),
  CritClaimShape2(-3), ScoutColdread(-3), RevBaseReceipts(-3), RevNoteNine(-2), CritCalibrationMove(-3),
  RevWaveArtifacts(-2), RevMistakes(-3), ExecFloorRekeyProbe(-3).
- **Minimum dead attempts implied: 20** (MutTools alone lost 3).
- **Seats currently unrecovered: 0.** Every seat has a live attempt or a landed report.
- Landed reports prove the retries recovered the seat, not merely respawned it: CritFreeze2, RevNoteNine,
  RevWaveArtifacts, CritCalibrationMove, ScoutColdread and RevBaseReceipts all have reports from their
  suffixed attempt.

Residual: the dispatch map records only the *final* agent id per seat, so "≥20" is a floor, not a count; an
attempt that died and was re-spawned under the same name would be invisible in this evidence.

## 3. Are the three reader reports valid?

Command and output: `T55W3RevW2-receipts/10-reader-validation.txt`; independent quote sweep below.

Canonical key, recomputed, not trusted:
`sectionize(git cat-file blob 9cf0146b…:SKILL.md)` from `.ufo/evidence/round-18/measure.py` (its `sectionize`,
`:209-253`) returns 64 sections, exactly one `## Standing rules`, `{"start":17,"end":44,
"sha256":"acfb671afd767c32476f57b040399972f6c870cd7dde3d821c344cae1a9ad767"}` (2,246 UTF-8 bytes after the
sectionizer's trailing-blank strip). `T55W3RevW2-receipts/04-history-and-section-sha.txt` also shows the
drift premise is true and still current: base `0a2010ac` has `sha 61736dce…, lines 17-40`; C0, the freeze tip
`133b2ce6` and `HEAD 4f7a7040` all have `acfb671a…, lines 17-44`. So the C0 sha is the correct bind key and
no post-C0 commit moved the section.

| reader | heading | cand | sha | findings | quotes verbatim in the C0 section | shape |
|---|---|---|---|---|---|---|
| T55W2Read01 | ✓ | ✓ | ✓ | 2 | 2/2 | exactly `{quote, why}` |
| T55W2Read02 | ✓ | ✓ | ✓ | 3 | 3/3 | exactly `{quote, why}` |
| T55W2Read03 | ✓ | ✓ | ✓ | 7 | 7/7 | exactly `{quote, why}` |
| T55W3R07 (wave 3) | ✓ | ✓ | ✓ | 2 | 2/2 | `{quote, why}` + extra top-level `bounds`, `sectionizer` |

Quote grounding was tested by whitespace-normalised substring containment against the section text cut at
C0 (the readers' `why` fields are not substring-checked; only the quotes they attribute to the section are).
All three w2 reports name their commands and their artifacts (`T55W2Read01.md:13,164-173`,
`T55W2Read02.md:20-31,245`, `T55W2Read03.md:5-18,175-176`), and all three state the section sha.

**Validity verdict: all three wave-2 reader reports are valid reader entries.** I reproduced two of their
load-bearing claims myself rather than trusting the seats:

- `'<value>'` quoting edge (Read02 finding 1): `TMPDIR="…/no-such-r55'q"` on a C0 clone prints
  `… usable directory: "/fast/…/no-such-r55'q" (could-not-evaluate)`, exit 2, one stderr line, and the
  frozen `GRAMMAR` from `133b2ce6:.ufo/evidence/round-55/c2/measure.py:47-50` returns **False** on it
  (`T55W3RevW2-receipts/02-frozen-grammar-and-tool-prefixes.txt`). Confirmed.
- nine allocating / five lazy modes (Read02 finding 3's premise): running every argv from the counter's own
  `modes()` under an unusable TMPDIR gives **9/9 allocating modes at exit 2 with one GRAMMAR-matching stderr
  line** and **5/5 lazy modes at exit 0 with empty stderr**
  (`T55W3RevW2-receipts/05-nine-allocating-five-lazy.txt`), and the same sweep shows `repeat-control` writing
  `REPEAT_CONTROL: setup_error` (28 B) to stdout — Read03 finding 7, confirmed.
- the per-tool token divergence (Read01 finding 1): `WITNESS_STUDY`, `ENVDIFF_SETUP`,
  `.py`-suffixed pin/evidence-disposition, bare `repeat-control`/`registry-check` — five distinct prefixes
  across nine modes, all GRAMMAR-accepted because the prefix class is `[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?`
  (same receipt). Confirmed.

One reader claim is true at C0 and fixed at the freeze tip, and that is not a validity defect: Read02
finding 3 measures the **C0** counter bytes (`36ca47d3`), and freeze amendment 8 at `133b2ce6` is exactly
the bookkeeping change that removes it. Findings read at C0 remain correct statements about C0.

## 4. Redundant with wave 3's reader, or not?

Content: **not redundant.** Over the four deliverables there are 12 distinct claims (2+3+7+2); exactly
**one** is duplicated: the `'<value>'` quoting edge, stated by `T55W2Read02` finding 1 and `T55W3R07`
finding 2. R07 finding 1 is its own, stronger claim (lane-wide completeness: `tools/registry.json` documents
30 selftest rows, 23 without a `scratch_root` cell, 21 of those naming a `mkdtemp`/`TemporaryDirectory`
target) and is not in the w2 set.

Binding: **fully redundant.** All four carry the same `(heading, cand, section_sha256)` triple, and the credit
rule keys sections by sha alone (`measure.py:602-612`, `matches = by_sha.get(sec['sha256'], [])`), so only
one of them can ever be the bound record.

### 4.1 The blocker that decides the question anyway

`T55W3RevW2-receipts/11-binder-selection.txt` replays the binder's selection read-only (nothing is written):

```
RES (resolutions items keyed by heading): {}
allowed (findings quota) for the heading: 0
  cand .ufo/waves/round-55/w2/T55W2Read01.json  cand_ok=True sha_ok=True findings=2 md=True
  cand .ufo/waves/round-55/w2/T55W2Read02.json  cand_ok=True sha_ok=True findings=3 md=True
  cand .ufo/waves/round-55/w2/T55W2Read03.json  cand_ok=True sha_ok=True findings=7 md=True
  cand .ufo/waves/round-55/w2/T55W3R07.json     cand_ok=True sha_ok=True findings=2 md=True
  cand .ufo/waves/round-55/w3/T55W3R07.json     cand_ok=True sha_ok=True findings=2 md=True
SELECTED: None
SKIPPED: [('## Standing rules', 'reader-has-findings:2>0')]
binder exit would be: 1 (0 iff no skip)
```

Three facts, each with its line in `binder.py`:

1. `RES` is built only from resolutions items carrying a `heading` key (`:53-54`). `resolutions.json` holds 22
   items, none with that key, so `allowed = RES.get(h, 0) = 0` (`:111`).
2. Every candidate has findings, and the loop **breaks** on the first over-quota candidate (`:118-121`). The
   first is `w2/T55W2Read01.json` (path order, `:96`), so the scan stops before R07 is ever looked at. A
   *clean* wave-3 reader could not rescue this heading; the break is unconditional.
3. `## Standing rules` is one of the 18 headings in `c1/lost-headings-at-c0.json` (position 7), so this skip
   is on the round's critical path and the binder exits 1.

### 4.2 Verdict: which reader should the binder use

**Use `T55W3R07`** — wave 3's designated re-key reader for this heading. It is key-valid, quote-grounded, has
the lowest finding count of any valid candidate (2, i.e. the least `minor_gaps` the ledger must carry for the
same certification), and its `w2/` and `w3/` copies are byte-identical (sha256 of both `.json` and `.md`
match), so it cannot bind stale bytes.

Two conditions, both mechanical:

- **Record the adjudication.** `resolutions.json` needs `{"heading": "## Standing rules", "n": 2}` before the
  bind; with `n` absent nothing binds (4.1). With `n = 2` the supervisor's gate is satisfied for both
  two-finding readers.
- **Fix the selection order, or accept `Read01`.** As shipped, `n = 2` makes the binder bind
  `w2/T55W2Read01.json`, not R07, because candidates are taken in sorted-path order (`:96`) and it is first.
  That entry is valid and honest, so the result is *defensible* — but it makes R07 dead weight and it means
  the choice of reader is decided by filename, not by adjudication. This affects exactly one heading (the
  other 17 have only wave-3 candidates), so a one-line change — prefer the `w3` directory, or pick the
  candidate with the fewest findings — is enough.

**Do not bind `T55W2Read03`** even though it is the most informative attack record (7 findings, the executor-
sufficiency read): binding it would stamp `minor_gaps: 7` on the certification. Its findings belong in the
round report's section-verdict discussion, which is where an L1 reader will look for the `## Standing rules`
attack record anyway.

---

## 5. Findings, by severity

**F1 — blocking (the round's credit).** `## Standing rules` cannot bind with today's artefacts: `RES` is empty
so `allowed = 0` (`binder.py:111`), and the first key-valid candidate trips the unconditional `break`
(`binder.py:118-121`), skipping the heading and exiting 1. Evidence: receipt 11. Remedy: record
`{"heading":"## Standing rules","n":2}` (or the count the L1 adjudicates) in
`.ufo/evidence/round-55/integrate/resolutions.json`.

**F2 — medium.** Reader selection is filename order, not adjudication (`binder.py:96`). With four valid
candidates for one heading, the L1 cannot steer which is bound once the quota is ≥2; the fullest reader
(Read03, 7 findings) and the designated wave-3 reader are both unreachable behind `Read01`. One heading, so
the blast radius is small, but it is the only heading where the question can even arise.

**F3 — medium (record shape).** `w2/` mixes the two waves: at 14:49 it holds 35 `.md` files and 14 reader
`.json` files, of which 10 and 10 belong to **wave 3** (`T55W3R01/02/03/04/05/07/08/10/12/17`). Counting
`w2/*.json` as wave-2 reader output overstates wave 2 by 2.5× (4 real wave-2 JSONs: Read01-03, SentScope2).
Cause below (F4); consequence: any wave-2 deliverable count taken by glob is wrong.

**F4 — low/medium (spec defect, wave 3).** Spec `w3`'s "Reader discipline" block was copied verbatim from
`w2` and tells the 18 readers to write
`…/.ufo/waves/round-55/**w2**/<your-seat-name>.json`, while `T55W3SentReaders` is told to audit
`…/w3/T55W3R*.json`. The seats split: R01–R05 have a `.json` only in `w2/` (and two differing `.md` copies,
so the `w2` copy of R01–R05 is a *different file*, not a twin), R06/R11/R13 wrote to `w3/` only, R07/R10 wrote
identical copies to both. The sentinel's audit path therefore undercounts the readers it is meant to audit.
This is outside wave 2's own scope but it is what pollutes wave 2's directory.

**F5 — low.** `binder.py:15` documents step 2 as "find a committed reader report `.ufo/waves/round-55/w1/*.json`"
while `:47` globs `w2` and `w3`. Anyone reading the docstring instead of the code would conclude no reader
qualifies for any heading.

**Not findings (checked, clean):**
- Report-trailer compliance: the wave-2 context only fixes the *resolution* of a `Report:` path; it does not
  mandate the trailer for wave-2 seats, and 22/26 reports have none by design. No defect.
- `T55W2Connector3.md` has zero fenced blocks but its commands are inline and its receipts dir is populated.
  Not a finding on the evidence I checked; a stricter reading of "runnable receipt (command + output +
  verdict)" could call it thin, and I am not making that call from a title scan.
- Reader JSON shape: the three w2 files are exactly the four documented keys; only R07 adds `bounds` and
  `sectionizer`, which no consumer reads. Harmless.

## 6. Residual risk and verification gaps

- **Counts move.** 18 → 26 reports in eight minutes. My 26/34 is a 14:49:02 reading; the L1 must re-read at
  bind time and must not quote this number as final.
- **"≥20 dead attempts" is a floor.** The dispatch map keeps only the surviving agent id per seat; deaths
  re-spawned under an unsuffixed name are invisible here.
- **Two long-running seats are the acute risk**: `T55W2MutC2` (27m, no receipts at all) and
  `T55W2RevGateResidual` (23m). If either dies, its seat has no fallback evidence.
- **I did not re-verify the readers' `why` claims beyond the three I reproduced** (apostrophe edge, nine/five
  mode sweep, tool-token prefixes). The registry-cell claim (Read02 finding 2) I confirmed only at C0 by
  reading the seven cells — they do quote `<tool>.py:` — and `resolutions.json` `W2-TOOLDIFF-F3` says the
  cells are "fixed at C1", but **no C1 commit exists in the lane** (`git log` shows only C0, 133b2ce, c31cdd9,
  4f7a7040); so that finding is still live at HEAD and the adjudication's "fixed" is forward-looking.
- **The binder was replayed, not run.** Running it writes the lane ledger and needs `PIN`; I refused to run
  it because the write is out of my scope. A live run with `n = 2` (in a scratch copy of the lane) is the
  natural next check for whoever owns the bind.
- Verification gaps: no `lsp` server answers this repository's JSON/markdown artefacts, so caller checks were
  done by reading the single consumer (`binder.py`) end to end rather than by reference queries.

## 7. Receipts (all under `.ufo/waves/round-55/w2/T55W3RevW2-receipts/`)

| receipt | what it shows |
|---|---|
| `01-apostrophe-quote-edge.txt` | `TMPDIR` with `'` emits a double-quoted value; exit 2, one stderr line, 28 B `REPEAT_CONTROL: setup_error` on stdout |
| `02-frozen-grammar-and-tool-prefixes.txt` | frozen `GRAMMAR` returns False on that line (True if double quotes were allowed) |
| `03-registry-cells.txt` | the seven `scratch_root` cells at C0 all quote `<tool>.py:` |
| `04-history-and-section-sha.txt` | section sha at base / C0 / freeze tip / HEAD; the drift premise |
| `05-nine-allocating-five-lazy.txt` | 9/9 allocating rc=2 + grammar, 5/5 lazy rc=0, per-mode prefix table |
| `06-envdiff-contract-grammar.txt` | `env-diff --contract` with the counter's own fixture: rc=2, grammar True |
| `07-counter-header-vs-arms.txt` | frozen counter header says 8 allocating; `modes()` returns 9 |
| `08-seat-census.txt` | 34 dispatched / 26 landed / 8 absent, with receipts-dir state and the wave-3 strays |
| `09-census.txt` | `sources-census.sh validate` → exit 0, `tameshi ok …/corpus/SOURCES.md` |
| `10-reader-validation.txt` | canonical sha, per-reader heading/cand/sha/findings/quote grounding, R07 byte-identity |
| `11-binder-selection.txt` | read-only replay: `RES={}`, `allowed=0`, `SELECTED None`, skip, exit 1 |
| `12-dead-attempts.txt` | 11 retried seats, ≥20 dead attempts implied, landing count at snapshot |

## 8. Artifacts opened

Lane (read-only, by explicit rev where the content mattered): `SKILL.md` at `0a2010ac`, `9cf0146b`, `133b2ce6`,
`HEAD`; `tools/registry.json` at C0; `tools/repeat-control.py`, `tools/context-capture.py`,
`tools/registry-check.py`, `tools/env-diff.py`, `tools/bash-witness-study.py`, `tools/pin-disposition.py`,
`tools/evidence-disposition.py` at C0 (executed in a `git clone --shared` at C0 with
`rev-parse --show-toplevel` asserted equal to the clone before every run; restored to 0 dirty paths after the
fixture run); `.ufo/evidence/round-18/measure.py` (`sectionize`, `entry_failure`, `coldread`);
`.ufo/evidence/round-55/c2/measure.py` bytes at `133b2ce6`; `.ufo/evidence/round-55/c1/lost-headings-at-c0.json`;
`.ufo/evidence/round-55/integrate/{binder.py,resolutions.json}`; `.ufo/evidence/round-55/freeze.json` (shape
only); `.ufo/waves/round-55/spec-w2.json`, `spec-w3.json`, `w2.ready`, `w2.ready.dispatched`, `w3.ready.partial`;
`.ufo/waves/round-55/w2/*` (26 seat reports, 12 reader JSONs, all receipt dirs, `swarm-registry.json`);
`.ufo/waves/round-55/w3/{T55W3R*.json,T55W3R*.md,T55W3R07-receipts/*}`; `scripts/sources-census.sh` (executed).

Tooling: nothing installed, upgraded, or downgraded — no package manager, no `uv`, no `npx`; the whole audit
ran on `python3`, `git`, `sha256sum`, `stat` already present. Scratch was
`/fast/scratch/hyaku/tameshi-r55/T55W3RevW2`, removed on completion; the shared parent was never touched.

Report: .ufo/waves/round-55/w3/T55W3RevW2.md
