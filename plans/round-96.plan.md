# tameshi round 96 — frozen declarations (plan)

Lane `tameshi` (verification-fixture craft). Round 96, attempt 1. Base (lane tip at
round start): `c8de77f3de0fd4bf619ebe78fa0b28adaf320d3e`, branch `master`.

Round 95 landed admitted (`coverage improved`, `calibration improved`) but its own
sentinel R95SN1 measured 12 findings that remain live in the round-95 bytes:
F1 (HIGH, hostile PATH forges the C2 checker), F2 (HIGH, `--rev ''` grades the index),
F3 (MEDIUM, driver grades highest `.rerun-N.out`), F4 (MEDIUM, driver follows a symlinked
receipt), F5 (MEDIUM, `make-pins95.py` writes through a symlink), F6 (MEDIUM,
`--lane ''` writes into the CWD repo), F7 (MEDIUM, checker accepts any revspec), F8
(MEDIUM, checker inherits ambient env). This round seals those exact defects. It
declares **two claims**, each frozen before any scored receipt exists.

Axes: depth + calibration (lane axes). C1 moves **calibration** (the audit's identity
binding: which revision and which `git` the verdict is read from). C2 moves
**operability** (the pins tool is runnable without escaping the lane). No axis is
re-scored in this file; verdicts are measured in the round report. The DoD control
lane is round 95 at `4bd1e88f`; the new revision is the round-96 instruments at
`INSTRUMENT_REV` (the `freeze` commit that carries them).

---

## Claims (frozen before data)

### C1 — calibration: the sealed audit (rev identity + hostile-PATH refusal)

- **Axis:** calibration (the audit's evidence binding: which bytes and which revision
  the verdict is read from).
- **Surface:** `.ufo/evidence/round-96/conjunct-disposition-v96.py` + the committed
  manifest `.ufo/evidence/round-96/conjunct-disposition.json`, audited against the
  committed battery receipts under `.ufo/evidence/round-96/pre-freeze/controls/`.
- **Wording (frozen):** at the instrument revision the checker prints
  `DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0` exit 0 against the
  committed manifest and the receipts it names; the checker refuses with exit 2 and
  `DISPOSITION_SETUP rev-not-a-commit-id` when `--rev` is not a 40-hex object id and
  with `DISPOSITION_SETUP rev-unresolvable` when the id does not resolve, and it prints
  the resolved id in the `DISPOSITION_INSTRUMENT` line; the checker invoked on a lane
  with no committed receipts at `--rev` is refused (setup or receipt-absent findings),
  never green; a hostile `git` earlier in the inherited `PATH` does not affect the
  verdict — the same `findings=0` the honest `git` produces is reproduced by the honest
  control, and the hostile-PATH lane with no committed receipts gives findings (a
  receipt-absent finding), not `findings=0`; the round-95 checker at `6a2a1fdd` prints
  `findings=0` exit 0 on the hostile-PATH lane (the before-witness for F1).
- **Counter:** `python3 -I .ufo/evidence/round-96/conjunct-disposition-v96.py --lane <lane> --rev REV --min-falsifiable 17`
- **Battery:** `python3 -I .ufo/evidence/round-96/conjunct-disposition-v96.py --selftest`
- **Predicate:** `DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0`
- **Before:** at base `c8de77f3` the successor checker does not exist
  (`DISPOSITION_SETUP counter-absent-at-rev`); the round-95 checker at `6a2a1fdd` prints
  `DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0`, exit 0, when a
  hostile `git` earlier in `PATH` answers `cat-file`/`ls-tree` from a forged directory,
  even with zero committed receipts (the F1 reproduction), and prints the same green on
  `--rev <branch>` (F7).
- **After:** the positive prints 19/17/2/0 at the instrument revision; `--rev ''`,
  `--rev master` and `--rev deadbeef…` are refused at setup; the hostile-PATH lane
  gives receipt-absent findings, not green; the selftest prints
  `DISPOSITION_SELFTEST: 13/13 pass` (2 new cases: hostile-PATH, branch-revspec).
- **Kill rules:**
  - a: `findings=0` while a printed conjunct key has no row, a row names an unknown key,
    a state row's receipt does not move its conjunct, or an `unfalsifiable` reason is
    shorter than 40 characters, names no mechanism, or names no battery state and no
    pin digest;
  - b: fewer than 17 of the 19 rows carry a state;
  - c: the selftest cannot fail: a case that must produce a finding produces none, or
    the clean case produces one;
  - d: the checker or manifest blob at the named revision differs from the `claims.json`
    sha256;
  - e: a receipt that exists only in the working tree, or carries a wrong `counter_sha=`,
    is accepted;
  - f: a `refs/replace` entry is present and the checker proceeds instead of refusing at
    setup;
  - g: a hostile `git` earlier in `PATH` changes the verdict from findings to green;
  - h: a revspec that is not a 40-hex object id is graded instead of refused.
- **Declared limits:** a full-root compromise (attacker owns the resolver, the `/usr/bin`
  mount, or the interpreter) defeats any userland seal; the seal covers the inherited
  environment and the PATH directory, not the kernel. The checker still does not
  execute the counter.

### C2 — operability: the hardened pins tool (atomic, symlink and empty-lane refusal)

- **Axis:** operability (the pins tool runs and produces its stated outcome without
  escaping the lane).
- **Surface:** `.ufo/evidence/round-96/c1/make-pins96.py`
  (`--lane LANE --rev REV [--check]`), plus the driver read-side Rank fix in
  `.ufo/evidence/round-96/c1/controls-v96.py` (F3 rank, F4 O_NOFOLLOW read).
- **Wording (frozen):** `make-pins96.py --lane <lane> --rev <40-hex>` writes
  `PINS_WRITTEN <lane>/.ufo/evidence/round-96/c1/pins.json`, exit 0, and the written
  bytes equal the five derived values at that revision; `--lane ''` is refused with
  exit 2 `PINS_SETUP lane-empty` and writes nothing; a symlink at `pins.json` is
  refused with exit 2 `PINS_SETUP pins-symlink-refused` and the target outside the
  lane is not modified; the write is atomic (temp + `os.replace`); the driver grades
  the lowest-index receipt (`<name>.out` wins over any planted `<name>.rerun-9.out`)
  and refuses a symlinked receipt (`SYMLINK-REFUSED` counts as missing, never a MATCH).
- **Counter:** `python3 -I .ufo/evidence/round-96/c1/make-pins96.py --lane LANE --rev REV [--check]`
- **Battery:** the C1 battery (`controls-v96.py`) plus the four F2–F7 pre-registered
  states below, plus the before-witness (round-95 tools on the same attacks).
- **Predicate:** `PINS_WRITTEN` + `PINS_CHECK OK`, exit 0 (positive); `lane-empty`,
  `pins-symlink-refused`, `rev-not-a-commit-id` (negative); driver
  `C1_CONTROLS states=50 matched=50 mismatches=0 missing=0` (carried, unchanged
  except for the F3/F4 read-side fix — the state set is unchanged).
- **Before:** at base `c8de77f3` the successor tool does not exist; the round-95
  `make-pins95.py` with `--lane ''` writes into the CWD repository, exit 0 (F6), and
  with a symlink at `pins.json` overwrites the outside target, exit 0 (F5); the
  round-95 driver grades the planted `ctlX.rerun-9.out` over the fresh `ctlX.out` (F3)
  and follows a symlinked receipt (F4).
- **After:** the four attacks are refused as above; the positive tool and driver
  unchanged in outcome; `--check` prints `PINS_CHECK OK`.
- **Kill rules:**
  - a: `--lane ''` writes any file or exits 0;
  - b: a symlinked `pins.json` target is modified, or the refusal is not exit 2;
  - c: a partial `pins.json` is observable (write is not atomic) — the tool writes
    directly to the destination path;
  - d: the driver grades a planted higher-index rerun over the fresh receipt;
  - e: the driver follows a symlinked receipt and grades its outside content;
  - f: the positive path does not write the derived bytes (`--check` fails).
- **Declared limits:** the tool does not defend against a writer that already owns the
  lane's filesystem root; it defends against a symlink or an empty lane naming the
  CWD.

---

## Pre-registered controls (F2–F7, pre-freeze)

| state | attack | expected at v96 | before (v95 at `6a2a1fdd`) |
|---|---|---|---|
| `rev-empty` | counter with `--rev ''` on a clone with a staged (uncommitted) note row | exit 2, `C1_SETUP rev-not-a-commit-id` | exit 1, `badrows=1` naming the staged row (`C1_SUMMARY rev=` empty) |
| `rev-branch` | checker with `--rev master` | exit 2, `DISPOSITION_SETUP rev-not-a-commit-id` | exit 0, `DISPOSITION rows=19 falsifiable=17 unfalsifiable=2 findings=0` |
| `path-hostile` | checker with a hostile `git` earlier in `PATH` on a lane with no committed receipts at `--rev` | receipt-absent findings, exit 1 (not green) | exit 0, `findings=0` (F1) |
| `pins-empty-lane` | `make-pins96.py --lane ''` from a CWD that is a git repo | exit 2, `PINS_SETUP lane-empty`, nothing written | exit 0, `PINS_WRITTEN <cwd>/…/pins.json` (F6) |
| `pins-symlink` | symlink at `pins.json` → outside target | exit 2, `PINS_SETUP pins-symlink-refused`, target unmodified | exit 0, outside target overwritten (F5) |
| `rerun-plant` | driver grades a state with a planted `.rerun-9.out` next to a fresh `<name>.out` | grades the fresh `<name>.out` (MATCH) | grades the planted rerun (MISMATCH) |
| `receipt-symlink` | driver grades a receipt that is a symlink to outside content | `SYMLINK-REFUSED` counts as missing | grades the outside content |

## Implications
- The successor manifest keeps the round-95 19-row shape; the two new selftest cases
  are `hostile-path-cheat` and `branch-revspec-cheat` (both must produce a finding).
- `controls-v96.py` state set is unchanged (50); the F3/F4 fix is read-side only.
- `measure-v96.py` reader is unchanged except for the rev guard; the battery is the
  round-95 45-state shape plus the same 5 (D01–D05) = 50.

## Kills for the round
- C1 kill rules (a)–(h) and C2 kill rules (a)–(f) above are the frozen rules.
- Any `falsifies-wording` artifact of the round's own wave that contradicts the
  frozen wording above is handled by amending the wording down to the enforceable
  property in `plans/round-96.plan.md` §Amendments, not by filing the wider sentence.
