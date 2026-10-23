# RerunC2Head — residual falsification of claim C2 (F6), round 29

## Verdict

**MISS confirmed; the miss is structural and the reporting is honest.** The frozen
counter `c2-measure-v2.py` at E (`7a45f7b9d6a2542a553276330c8b02ac2e28c7ef`, which
is also current `master`) reproduces the recorded output byte-for-byte. Two
independent, frozen-before-data conditions make `C2_F6_V2_PASS` unreachable:

1. **Kill is impossible under the anchor.** `Oracle.kills()` needs the pinned gate
   to emit `(declared exec, no execute bit)` while the B5 mutant exits 0. The
   anchor (clause 1) pins `census.tsv` byte-identical to the kagi declaration, in
   which **every exec row declares mode 755** (`client.py`, `the-janitor`,
   `tac-check` — all `asset\texec\t755`). A non-executable file under an exec row
   has mode != 755, so the mutant — which deletes only the x-bit arm and keeps the
   mode check (`surface-census.sh:220-224`) — still diverges and exits 1. A 755
   file has the x bit, so the pristine prints no exec token. Observed on the
   committed fixture: pristine `exit=1` with the exec token on `client.py`;
   mutant `exit=1` on `SURFACE DIVERGED $HOME/.config/the-janitor/client.py
   (mode 644, declared 755)`. Same masking the seat BuildF6B reported
   (`.ufo/waves/round-29/w1/BuildF6B.md:105-136`).
2. **`quote_located` cannot fire at E.** `corpus/lessons/round-29.md` does not
   exist at E (`git ls-files` at E: no round-29 lesson), so clause 5's quote scan
   has no line to match.

No narrowing, no post-data predicate change: `contract-amendment-1.json` and
`c2-measure-v2.py` were committed once, at `6ab11a6` (2026-10-22T22:21:28-03:00),
before any data-seat output (the BuildF6 wave was dispatched on `09e4f27`
22:26:47 and the seat's receipt shows the identical miss fields; the fixture
landed at `7a45f7b` 23:46:49). `counter_sha256` in the amendment equals
`sha256sum c2-measure-v2.py` = `adc721f9260c87f34d444b7481c45db8e469178237a9e0f198d29cef440ada4c`.
The kill_rule ("`PASS=false` at the landed head is a miss: reported as an honest
stop, never amended or re-scaled") was honored — `LOG.md:1740-1742` states the
miss and the masking cause.

## Evidence

Commands run in my clone `/fast/scratch/hyaku/tameshi-r29-rerunc2head`
(`git clone --no-hardlinks`, detached at `7a45f7b`; `GIT_*` unset):

- `git rev-parse master` → `7a45f7b9d6a2542a553276330c8b02ac2e28c7ef` — E is the
  head; the "later commits" clause does not apply. `git log --oneline -8` shows
  E on top; no branch ahead.
- `timeout 900 python3 .ufo/evidence/round-29/c2-measure-v2.py --repo
  /fast/scratch/hyaku/tameshi-r29-rerunc2head --rev 7a45f7b9d6a2542a553276330c8b02ac2e28c7ef`
  (run from the lane's evidence dir, read-only) →
  `  oracle tests run: 1`
  `C2_F6_V2: fixture=present anchored=1 kill_original=0 units_original=105
   units_minimized=105 ddmin_match=0 kill=0 one_minimal=0 entry_sourced=1
   quote_located=0 rev=7a45f7b…`
  `PREDICATE: C2_F6_V2_PASS=false`, `EXIT=1` — identical to
  `.ufo/evidence/round-29/c2-at-E.stdout`.
- Same counter at freeze rev `--rev 9f3084bc…` → `fixture=absent`, all fields 0,
  `PASS=false`, exit 1 — matches `c2v2-at-A.stdout`; the unmoved command reads
  absent before data, so the counter discriminates.
- Pinned gate: `git -C kagi-shokunin show
  fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh` → sha256
  `275d8294…53009f` = `PIN_BASH` at `tools/mutate-and-run.sh:605`;
  `REV_BASH=fecee874…` at :606; runner untouched since 2026-10-22T07:06
  (pre-freeze). Pinned exec rows: three, all `exec 755`.
- Materialized the committed `f6/original/` fixture myself (host.tsv manifest,
  modes via `chmod`): pristine gate → `exit=1`,
  `SURFACE DIVERGED $HOME/.config/the-janitor/client.py (declared exec, no
  execute bit)` (diverged=1, all other counters 0). B5 mutant built by the
  counter's exact `b5_mutant`/`dec` (count(old)==1, mutant differs) → `exit=1`,
  `SURFACE DIVERGED … (mode 644, declared 755)`. Kill halves: pristine side
  holds, mutant side does not — `kill_original=0` is the true reading.
- `anchored=1` verified by hand: `original/census.tsv` byte-identical to pinned
  `surface-census.tsv` (both end without a trailing newline); `shapes.tsv` empty
  (⊆ pinned); all 15 `baseline.tsv` lines are pinned `drift-baseline.tsv` lines.
- Timing: `git log -- contract-amendment-1.json` and `-- c2-measure-v2.py` each
  show exactly `6ab11a6` (22:21:28); wave-1 spec/dispatch `09e4f27` (22:26:47);
  fixture + `w1/BuildF6B.md` committed `7a45f7b` (23:46:49). First BuildF6 seat
  output postdates the amendment by ≈85 min; the seat's own counter run
  (BuildF6B.md:159-162) already printed the same miss fields.
- Fixture pair: `original/` vs `minimized/` differ only in census.tsv's trailing
  newline — 105 vs 105 units, identical `(file, index)` keys, so `kills(mu)` hit
  the oracle cache; the receipt's `oracle tests run: 1` is the original probe.

## Residual risk

- `Oracle.kills()` cache keys on `(file, index)` and ignores line content
  (`c2-measure-v2.py:165`). Harmless here (minimized is a content-identical copy
  and both verdicts are False), but a future fixture that reordered or rewrote
  lines within the same index set could inherit a stale kill verdict. Worth
  fixing only if F6 is re-attempted.
- `oracle tests run` counts calls, not fresh tests; cosmetic only.
- The committed `minimized/` is the original plus one trailing newline — not a
  cheat: `ddmin` is gated behind `kill_original`, so the counter never demanded a
  real reduction. The seat report states this plainly.

## Smallest safe correction

None to the reporting. To make F6 passable in a future round the counter's kill
clause must change (frozen before data): either anchor to a census where at least
one exec row declares mode `-` (unchecked) or a non-755 mode, or require the kill
through a divergence the mode check cannot mask. As written, the frozen predicate
is unreachable — the miss is a property of the freeze, not of the measurement.

## Process

Clone only in `/fast/scratch/hyaku`; no git writes in the lane; no `jj`; no
processes left running (scratch materialization `/tmp/c2manual-*` removed). No
tools installed or upgraded. Time used: well under the 15-minute box.

Report: .ufo/waves/round-29/res/RerunC2Head.md
