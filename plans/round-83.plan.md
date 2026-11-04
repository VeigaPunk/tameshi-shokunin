# round-83 plan — tameshi (frozen before data)

Lane: tameshi-shokunin (depth + calibration; verification-fixture craft).
Round: 83 (attempt 1), 2026-11-04. Base
`c63467bb5f5842fb63f2b24e6361ab6666a29cab` (= `origin/master`, the round-82
non-author closure's spot-check tip). Round shape: **one v1 wave, 13 seats** —
4 executor · 2 scout · 1 scribe · 2 reviewer · 1 critic · 1 mutation-tester ·
1 sentinel · 1 connector; attack seats 4/13 = 30.8 % (the addendum's attack
set is reviewer/critic/mutation-tester/labrat; the sentinel is a bounds seat,
not counted as attack — the round-82 closure's item 7a correction); policy
`scripts/hyaku/ufo-wave-policy.json`, band 8–16. The §3 planner seat stays with
the L1 (the validator rejects `planner`); its data walk rides the two scout
items. Saturation: scored axes depth 10, calibration 8, freshness 9 sit at or
above the line 8, window N = 2; this round enters no new capability row (all
three claims harden existing instruments), so the stagnation nudge does NOT
fire and C1 works **calibration (8), the lowest scored axis**.

Motivating evidence: the round-82 non-author spot-check
(`corpus/lessons/round-82-verifier-spotcheck.md` §2.3 and §6) routed two
instrument debts and the SCORECARD's own `Planned (round 83)` paragraph carries
four more. This plan takes three of them as claims (the manifest binding, the
registry bind, the non-regular path class) and leaves the rest named as honest
limits.

The base controls below were **measured before this file was written** and are
committed with it (`.ufo/evidence/round-83/controls/`); each control is the
cheapest run that skips the claimed work, scored with the claim's own counter.

## R83-C1 — calibration: the self-state sweep is bound to its declared manifest revision

- **Predicate (the claim's one sentence).** `tools/selfstate-freshness.py`
  measures its declared population only when the manifest is the object at the
  declared revision and every row id is line-safe: with `--manifest-rev REV` a
  worktree manifest whose bytes differ from `REV:<manifest>` is refused
  (`manifest-rev-mismatch`, exit 2, no `SELFSTATE:` line), the committed
  manifest measures `SELFSTATE: rows=26 match=24 stale=2 unexpected=0` exit 0,
  and a row `id` outside `[A-Za-z0-9._-]{1,64}` is refused
  (`row-id-alphabet:<repr>`, exit 2, no `SELFSTATE:` line).
- **Before (base tool bytes `c63467bb`, receipts under
  `.ufo/evidence/round-83/controls/`):**
  - `c1-before-flag.txt` → `error: unrecognized arguments: --manifest-rev
    HEAD`, exit 2: the binding does not exist.
  - `c1-before-silent-narrowing.txt` → the manifest with its one
    population-monitor row (`standing-pin-audit`) DELETED measures
    `SELFSTATE: rows=25 match=23 stale=2 unexpected=0`, exit 0: **the
    population narrowed and the counter certified**. (Deleting a different row
    is caught by that monitor's nested figure; deleting the monitor itself is
    the cheat, which is why the binding and not the nested row is the fix.)
  - `c1-before-id-forge.txt` → a row id carrying a newline prints a forged
    verdict line `SELFSTATE: rows=26 match=26 stale=0 unexpected=0` at output
    line 2, exit 0: a first-match parser reads a green summary the measure
    never produced.
- **After (measured at the records commit):**
  - `python3 -I -X utf8 tools/selfstate-freshness.py --repo . --manifest
    tools/selfstate-freshness.json --manifest-rev HEAD` →
    `SELFSTATE: rows=26 match=24 stale=2 unexpected=0`, exit 0.
  - the narrowed clone → `SELFSTATE error=setup
    manifest-rev-mismatch:<rev12>`, exit 2, no `SELFSTATE:` line.
  - the id-forge clone → `SELFSTATE error=setup
    row-id-alphabet:'forged\nSELFSTATE: …'`, exit 2, no `SELFSTATE:` line.
  - `--selftest` → `SELFSTATE_SELFTEST: 24/24 pass` (3 new arms: A22 the
    manifest binding including its narrowing and regular-file refusals, A23 the
    id alphabet, A24 the binding's own text pin refresh).
- **Do-nothing control.** The narrowed manifest at the base tool certifies
  `rows=25 … unexpected=0` exit 0 (receipt above) and the id forge prints a
  green summary at base; nothing appended changes either reading, and the base
  instrument refuses the new flag, so neither after-line is reachable without
  this round's code.
- **Kill rule.** With the instrument, the manifest and the declared population
  unchanged after this declaration, ANY of: the narrowed manifest reaching a
  `SELFSTATE:` verdict line; the committed manifest at `--manifest-rev HEAD`
  reading rows≠26; the newline id reaching a verdict line; a row removed from
  `tools/selfstate-freshness.json` or an `expect` relaxed — fails the claim.
- **Declared limits.** (a) The binding proves bytes at a *caller-named*
  revision, never that the revision is the intended one — a committed narrowed
  manifest binds at its own revision (round-82's limit, unchanged). (b) A
  `text`/`eol` conversion attribute on the manifest path, or the working tree's
  index conversion, would make the worktree bytes differ from the blob for a
  reason the binding cannot tell from a narrowing: this lane's paths carry no
  such attribute (`git check-attr text eol -- tools/selfstate-freshness.json`
  prints `unspecified`), and the binding is exact on object bytes. (c) The id
  alphabet refuses line-breaking and non-ASCII ids; an id that is line-safe but
  duplicated is already refused by the standing `row-id-duplicate` arm.
- **Counting commands.**
  `python3 -I -X utf8 tools/selfstate-freshness.py --repo . --manifest tools/selfstate-freshness.json --manifest-rev HEAD`
  and the two fixture runs of `.ufo/fixtures/round-83/c1/run.sh`.
- **Sourced:** S289 (`git-cat-file`; the object-read ground) and S291
  (index-format; the mode field that separates a symlink from a regular file),
  both re-opened this round.

## R83-C2 — freshness: the second copy of the defect-bind figures is measured

- **Predicate.** `tools/registry-figure-bind.py` binds the two `defect-bind`
  registry rows, so `tools/registry.json`'s copies of those figures are
  measured against their instruments, not trusted:
  `REGISTRY_BIND: rows=9 match=9 stale=0 absent=0 error=0 unexpected=0` exit 0
  over the live repo, and over a registry whose `defect-bind-selftest` figure
  reads `DEFECT_BIND_SELFTEST: 11/11 pass` the same instrument reads `stale`
  exit 1 while the base instrument reads `rows=7 match=7` exit 0.
- **Before (base tool bytes, receipts under
  `.ufo/evidence/round-83/controls/`):** `c2-before-rows7.txt` →
  `REGISTRY_BIND: rows=7 match=7 stale=0 absent=0 error=0 unexpected=0`,
  exit 0; `c2-before-drift-invisible.txt` → over the same fixture repo whose
  `defect-bind-selftest` figure is degraded to `11/11`,
  `REGISTRY_BIND: rows=7 match=7 … unexpected=0`, exit 0: the second copy of
  the figure is invisible to the binding.
- **After (measured at the records commit):**
  `REGISTRY_BIND: rows=9 match=9 …` exit 0 live, and over the drift fixture
  `REGISTRY_BIND_ROW registry-defect-bind-selftest … measured=stale`,
  `REGISTRY_BIND: rows=9 match=8 stale=1 … unexpected=1`, exit 1.
  `--selftest` → `REGISTRY_BIND_SELFTEST: 13/13 pass` (2 new arms: the
  registry-json drift arm and the registry-json duplicate-name refusal).
- **Do-nothing control.** The same drift fixture at the base tool reads
  `rows=7 match=7` exit 0 (receipt above); adding no manifest row leaves that
  reading unchanged, so the drift arm is only reachable through this round's
  manifest rows.
- **Kill rule.** Any of: the live read rows≠9; the drift fixture reading
  `match` or exit 0; a bound row whose declared token count is not exactly one;
  a `stdout_contains` entry removed from `tools/registry.json` to make the
  figure agree — fails the claim.
- **Counting commands.**
  `python3 -I -X utf8 tools/registry-figure-bind.py --repo . --manifest tools/registry-figure-bind.json`
  and `.ufo/fixtures/round-83/c2/run.sh` (clone, degrade, measure).
- **Declared limit.** The binding measures the *registry's* copy against the
  instrument's printed figure; it does not measure `SKILL.md`'s copies of the
  same figures beyond the rows already bound (the `skill-*` rows), and it does
  not measure a figure no row names. Round 82's `rows=7` covered three doc rows
  and four registry rows; this round adds the two registry rows the lane
  planned and leaves every other copy named, not bound.

## R83-C3 — coverage: a symlink is not a receipt in either receipt instrument

- **Predicate.** Both receipt instruments refuse a non-regular path:
  `tools/receipt-bytes-bind.py --root <fixture>` reads a symlink receipt as
  `unbound` with `detail=not-regular-file` and never reads its target's bytes
  (`RECEIPT_BIND: receipts=1 bound=0 corrected=0 design=0 unbound=1`, exit 1),
  and `tools/receipt-revision-gate.py` refuses a symlink receipt with code
  `RECEIPT_NOT_REGULAR` (exit 3); a regular file in the same population still
  binds and still passes (no over-kill).
- **Before (base tool bytes, receipts under
  `.ufo/evidence/round-83/controls/`):**
  - `c3-before-symlink-bound.txt` → the committed fixture
    `.ufo/fixtures/round-83/c3/root/link.receipt` (a symlink to
    `../target/receipt.bound`) measures
    `RECEIPT_BIND: receipts=1 bound=1 corrected=0 design=0 unbound=0`, exit 0:
    the symlink's *target's* bytes certify a receipt that is not in the tree.
  - `c3-before-gate-passes.txt` → the same path as a `positive` receipt
    measures `GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS`, exit 0.
- **After (measured at the records commit):** the fixture reads
  `RECEIPT_BIND_ROW … state=unbound detail=not-regular-file` and
  `RECEIPT_BIND: receipts=1 bound=0 corrected=0 design=0 unbound=1`, exit 1;
  the gate reads `GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_NOT_REGULAR
  verdict=REFUSED`, exit 3; the regular-file sibling of the fixture still reads
  `bound=1` / `PASS`. `--selftest` → `RECEIPT_BIND_SELFTEST: 14/14 pass` and
  `GATE_SELFTEST: 20/20 pass` (one new arm each).
- **Do-nothing control.** The same committed fixture at the base tools binds
  and passes (receipts above); nothing appended changes that, so the refusal is
  unreachable without this round's code.
- **Kill rule.** Any of: the symlink row reading `bound` or `design`; the gate
  reading PASS or any code other than `RECEIPT_NOT_REGULAR`; a regular-file
  receipt refused; the standing `.ufo/evidence` sweep losing a row or turning
  red — fails the claim.
- **Declared limits.** (a) The class is the *path's* type, not the target's
  content: a symlink whose target is a valid receipt is refused, deliberately —
  the population is the tree's regular files. (b) `receipt-bytes-bind` still
  walks with `os.walk` and does not descend symlinked *directories*
  (`followlinks=False` is the default; a symlinked directory is invisible, not
  refused) — named, not closed. (c) `receipt-revision-gate` reads receipts from
  the working tree only; a committed-only receipt is outside its population
  (unchanged).
- **Counting commands.**
  `python3 -I -X utf8 tools/receipt-bytes-bind.py --repo . --root .ufo/fixtures/round-83/c3/root`
  and `python3 -I -X utf8 tools/receipt-revision-gate.py --lane . --certified <rev> --receipt .ufo/fixtures/round-83/c3/root/link.receipt:positive`.
- **Sourced:** S291 (git index-format: the 9-bit permission field, "Symbolic
  links and gitlinks have value 0 in this field" — a symlink is a distinct
  type, not a permission variant of a regular file), re-opened this round.

## No-harm and registry coupling

`SELFSTATE_SELFTEST` 21 → 24, `REGISTRY_BIND_SELFTEST` 11 → 13,
`RECEIPT_BIND_SELFTEST` 13 → 14 and `GATE_SELFTEST` 19 → 20 change registry and
`SKILL.md` figures; `tools/registry.json`, the `SKILL.md` registry rows and the
`tools/registry-figure-bind.json` live figures are refreshed in the landing
commit and re-measured by `tools/registry-figure-bind.py` (`rows=9 match=9`,
exit 0). The self-state manifest's own rows are unchanged in population (26);
the `selftest-text-pin` row's figure moves 21/21 → 24/24 and
`registry-bind-selftest` 11/11 → 13/13, so both rows are re-pinned at the
instruments' last commits and the standing pin audit must read
`SELFSTATE_PINS: rows=26 settled=26 stale=0`. No SCORECARD axis score is
lowered. The round-82 closure's routed defects 1–7 land as an append-only
correction this round.

## Round-shape record

One v1 wave `w1`, 13 seats (policy band 8–16; attack 4/13 = 30.8 %; one
connector seat; two scout seats). Every seat is read-only in the lane except
its own report file; executors build in `$HYAKU_SCRATCH/tameshi-r83/<seat>/`
and delete their trees. Residual: none planned; any leftover seats go to one
ordinary ≤4-seat call counted in the round total.
