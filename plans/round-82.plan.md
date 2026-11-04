# round-82 plan — tameshi (frozen before data)

Lane: tameshi-shokunin (depth + calibration; verification-fixture craft).
Round: 82 (attempt 1), 2026-11-04. Base
`4dfc3181310088c2f32d51e87a4d82c047d05231` (= `origin/master`, the round-81
non-author closure's spot-check tip). Round shape: **one v1 wave, 13 seats** —
4 executor · 2 scout · 1 scribe · 2 reviewer · 1 critic · 1 mutation-tester ·
1 sentinel · 1 connector; attack seats 5/13 = 38.5 %; policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16. The §3 planner seat stays
with the L1 (the validator rejects `planner`); its data walk rides a scout
item. Saturation: scored axes depth 10, calibration 8, freshness 9 sit at or
above the line 8, window N = 2; this round's C2 admits no new capability row
(it binds existing ones), so the nudge does NOT fire and C1 works **calibration
(8), the lowest scored axis**.

Motivating evidence: the round-81 non-author spot-check
(`corpus/lessons/round-81-verifier-spotcheck.md` §6) routed six defects to
this round. Three are record defects (item 1 the stale manifest-binding
receipt, item 2 the SCORECARD measured-claim pointers, item 3 the unreceipted
tip re-derivation) and one is a table-placement defect (item 6); item 5
carries the instrument's own hardening debt, of which two are named
counterexamples this round closes: **the register is bound by a path, not by
bytes** (connector D-CN3: "`defect-bind.py` reads its manifest from the path
given, so the kill rule's 'no row removed / `expect` relaxed / population
narrowed' clause is enforced by the frozen commit, not by the instrument")
and **a path row accepts a tree or a symlink** (reviewer D1a/D5 + executor E1:
"`git cat-file -e` accepts a tree or an empty blob"; "a `tree-bytes` row is
satisfied by a symlink entry whose target string is large enough"). The
mutation-tester named the third: "`defect-bind.py`'s selftest text is not
pinned, so the C3 class does not yet cover the round's newest instrument —
round 82's move."

## R82-C1 — calibration: the routed-defect register is content-bound

- **Predicate (the claim's one sentence).** The six-row register
  (`tools/defect-bind.json`, the round-80 D-set, population unchanged) measures
  **bound to its declared revision and closed on regular blobs**:
  `DEFECT_BIND: rows=6 closed=6 open=0 unexpected=0 manifest=bound`, exit 0,
  and a manifest whose bytes differ from the declared revision is REFUSED
  (exit 2, `manifest-rev-mismatch`) before any row effect.
- **Before (base tip `4dfc3181`, base instrument, receipts under
  `.ufo/evidence/round-82/controls/`):**
  - `c1-before-flag.txt` → `error: unrecognized arguments: --manifest-rev
    HEAD`, exit 2: the binding does not exist.
  - `c1-before-narrowed-certifies.txt` → the same register with one row
    DELETED (D6) measures `DEFECT_BIND: rows=5 closed=5 open=0 unexpected=0`,
    exit 0: **the population narrowed and the counter certified**.
  - `c1-before-directory-closed.txt` → a `tree-paths` row naming a DIRECTORY
    (`.ufo/evidence/round-81`) measures `state=closed detail=paths-present`,
    exit 0: a tree stands in for a file.
- **After (measured at the records commit):**
  - `python3 -I -X utf8 tools/defect-bind.py --repo . --manifest
    tools/defect-bind.json --manifest-rev HEAD` →
    `DEFECT_BIND: rows=6 closed=6 open=0 unexpected=0 manifest=bound`, exit 0.
  - the narrowed-manifest clone → `manifest-rev-mismatch`, exit 2, no rows.
  - the directory row → `state=open detail=not-regular-file:...=040000`; a
    symlink row → `not-regular-file:...=120000`.
  - `--selftest` → `DEFECT_BIND_SELFTEST: 14/14 pass` (3 new arms: A12 the
    mode/type boundary, A13 the manifest binding including its narrowing
    cheat, A14 the text pin).
- **Do-nothing control.** Nothing appended changes the reading: the base
  instrument on the same narrowed manifest still certifies `rows=5 closed=5`
  (receipt above), and the base instrument refuses the new flag, so neither
  the bound line nor the refusal is reachable without this round's code. The
  "cheapest control that skips the claimed work" is exactly this narrowed
  manifest: it MEETS the target only under the base instrument, which is why
  the target requires `manifest=bound` on the full six-row population.
- **Kill rule.** With the instrument, the manifest and the register's declared
  population unchanged after this declaration, ANY of: a row measuring `open`;
  the bound line reading `manifest=unbound`; the narrowed manifest being
  accepted; a row removed or an `expect` relaxed; a directory or symlink
  satisfying a path row — fails the claim.
- **Declared limit (S311).** Byte equality between the worktree file and the
  declared revision's blob holds only where no `text`/`eol`/filter attribute
  converts the path; with conversion the binding is exact on the object bytes
  only. `tools/defect-bind.json` and its cited receipts carry no conversion
  attributes.
- **Counting command**
  `python3 -I -X utf8 tools/defect-bind.py --repo . --manifest tools/defect-bind.json --manifest-rev HEAD`.
- **Capability row on landing:** `closure-defect bind` gains the binding
  (the row already exists; its evidence cell is refreshed).

## R82-C2 — freshness: the three round-81 capability rows are live self-state rows

- **Predicate.** The standing self-state sweep's population carries the three
  round-81 capabilities as **live** rows, each measuring the figure its
  instrument prints now, and every pin is settled at the tip:
  `SELFSTATE: rows=26 match=24 stale=2 unexpected=0` exit 0 (the two `stale`
  rows are the standing declared red arms) and
  `SELFSTATE_PINS: rows=26 settled=26 stale=0` exit 0 at the tip.
- **Population.** `tools/selfstate-freshness.json` gains
  `closure-defect-bind` (figure `DEFECT_BIND:`, the sweep),
  `standing-pin-audit` (figure `SELFSTATE_PINS:`) and
  `selftest-text-pin` (figure `DEFECT_BIND_SELFTEST:`, the suite the A14 pin
  protects). The three live `## Capabilities` rows the monitors look up are
  moved into the repertoire table (round-81 spot-check §6 item 6) with their
  figures refreshed.
- **Before (base tip, receipt `.ufo/evidence/round-82/controls/c2-before.txt`):**
  `SELFSTATE: rows=23 match=21 stale=2 unexpected=0` exit 0 and
  `SELFSTATE_PINS: rows=23 settled=23 stale=0` exit 0 — the three capabilities
  have no live monitor, so a stale figure in them is invisible.
- **Do-nothing control.** Adding nothing leaves `rows=23`; the target's
  `rows=26` is unreachable without the three rows. A row added with a stale
  figure measures `unexpected` (the arm-4 fixture in the tool's selftest is
  the standing demonstration).
- **Kill rule.** Any of the three new rows unmeasured (absent from the
  sweep's row lines), any new row `unexpected`, or the pin audit reading a
  stale row fails the claim. The standing sweep must stay exit 0.
- **Counting commands** (both, they are one claim):
  `python3 -I -X utf8 tools/selfstate-freshness.py --repo . --manifest tools/selfstate-freshness.json`
  and the same with `--pin-audit --pin-rev HEAD`.

## R82-C3 — coverage: the mutation suite's own assertion text is pinned on the newest instrument

- **Predicate.** `tools/defect-bind.py` carries a selftest-text pin
  (`SELFTEST_TEXT_SHA256`, arm `A14_selftest_text_pin`) and its battery kills
  the test-text mutant: `MUTATE: DONE (target=defect-bind-arms-r82 defects=5
  killed=5 survived=0 inconclusive=0 kill-rate=100%)`, `CONTROL: GREEN`,
  byte-identical `MUTATE_RESTORE: OK`; the FAIL set for
  `db-a1-assertion-weakened` is `A14_selftest_text_pin` only.
- **Surface it moves.** The edge class "the suite's own assertion text" had no
  arm on this instrument: at the base bytes the same single edit (arm A1's
  summary conjunct deleted, name and fixtures kept) leaves the suite at
  `11/11 pass` and the mutant SURVIVES. The pin digests
  `inspect.getsource(selftest)` and refuses a text edit until the constant is
  deliberately recomputed.
- **Before (base tool bytes, `controls/c3-before-mutant.txt`):**
  `MUTATE: DONE (target=c3-base-db defects=1 killed=0 survived=1
  inconclusive=0 kill-rate=0%)`, `DEFECT_BIND_SELFTEST: 11/11 pass`,
  `CONTROL: GREEN`, restore byte-identical.
- **Do-nothing control.** The base bytes with the same single edit: survival.
- **Kill rule.** The mutant must be KILLED and its FAIL set must be exactly
  the pin arm; a pin that also fails an unrelated arm is an over-kill defect
  to report, and a surviving mutant fails the claim. Declared limits (carried
  from round 81, unchanged): the digest covers the function's source only —
  module-level edits, a vacuous comment inside the function, and a two-edit
  rewrite (weaken an arm AND recompute the constant) stay outside the class.
- **Counting command**
  `bash tools/mutate-and-run.sh --target tools/defect-bind.py --defects tools/defect-bind-mutants.spec --suite 'python3 -I -X utf8 "$MUTANT" --selftest' --label defect-bind-arms-r82 --workdir <scratch>`.
- **Sourced:** S310 (`inspect.getsource`, re-opened this round) and S311
  (`gitattributes` conversion attributes — the C1 limit; opened this round).

## No-harm and registry coupling

`DEFECT_BIND_SELFTEST` 11 → 14 and `SELFSTATE` 23 → 26 change registry and
`SKILL.md` figures; `tools/registry.json`'s `defect-bind-selftest`,
`selfstate-freshness-sweep`, `selfstate-pins` rows and `SKILL.md`'s registry
rows are refreshed in the landing commit, re-measured by
`tools/registry-figure-bind.py` (`rows=7 match=7`, exit 0) — a figure the round
does not refresh is a measured defect, not a silent drift. The three
round-81 capability rows move into the live `## Capabilities` table. The
closure's record defects (items 1–3) are closed with reissued receipts and an
append-only SCORECARD erratum, and are measured by a new register
`tools/defect-bind-r82.json` so "closed" is a count. No SCORECARD axis score is
lowered.

## Round-shape record

One v1 wave `w1`, 13 seats (policy band 8–16; attack 5/13 = 38.5 %; one
connector seat; two scout seats). Every seat is read-only in the lane except
its own report file; executors build in `$HYAKU_SCRATCH/tameshi-r82/<seat>/`
and delete their trees. Residual: none planned; any leftover seats go to one
ordinary ≤4-seat call counted in the round total.
