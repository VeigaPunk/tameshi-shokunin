# Survivor fixture minimization — B5 probe, delta debugging

source: S024 (https://www.fuzzingbook.org/html/Reducer.html, re-opened 2026-10-23; snapshot `.ufo/evidence/round-29/sources/S024-fuzzingbook-Reducer.html`, sha256 3abede35…e99)

Round 29, frontier F6 ("fixture minimization for survivors", `corpus/README.md`
`## Frontier` row F6, pre-registered in the Round-29 section). Outcome: **the
frozen target was not reached.** The attempt produced a finding about survivor
B5 instead, recorded below with its receipts. F6 stays open.

## What S024 teaches, and what it needs

Delta debugging reduces an input that makes a test fail while keeping that
failure. S024 states the result property this round used: "Its result is
1-minimal, meaning that every character contained is required to produce the
error" (section "Delta Debugging"). Its reducer asserts that the starting input
is itself failing before it removes anything. A reducer therefore needs an
interesting input to start from; it cannot create one.

## The F6 method as frozen

Counter `.ufo/evidence/round-29/c2-measure-v2.py` (contract
`.ufo/evidence/round-29/contract-amendment-1.json`):

- The original fixture's `census.tsv` is byte-identical to the pinned kagi
  declaration `corpus/surface-census.tsv` at `fecee874`. Shapes and baseline lines
  are subsets of the pinned files. The host is a manifest (`host.tsv`), one node
  per line, so file modes survive git.
- `Oracle.kills()`: the pinned gate exits 1 with a `SURFACE DIVERGED` line naming
  `(declared exec, no execute bit)`, and the B5 mutant (exec x-bit arm deleted, the
  runner's own `@defect B5` spec) exits 0.
- The counter's own `ddmin()` (an integer-partition variant of S024's complement
  loop; seat CriticC2v2 Q3 shows the two can pick different 1-minimal results)
  must reproduce the committed minimized fixture, which must be 1-minimal at line
  granularity.

## What happened

Builder BuildF6B built the anchored original:
`.ufo/evidence/round-29/f6/original/` (copied byte for byte from
`.ufo/evidence/round-29/f6/BuildF6B/original/`). Its census is the pinned file
(sha256 `4af0dbcc…`). The host has every declared node at its declared mode,
except `.config/the-janitor/client.py` at 644. Counter at the round's head:
units_original=105 units_minimized=105, `anchored=1 kill_original=0`, PASS false.

- Pristine: one divergence, `SURFACE DIVERGED $HOME/.config/the-janitor/client.py
  (declared exec, no execute bit)`, exit 1.
- B5 mutant: the same row as `(mode 644, declared 755)`, exit 1.

ddmin made 171 oracle tests and kept nothing, because no subset kills. The
committed `minimized/` is a byte copy of `original/`.

## The finding: B5 is masked under the pinned declaration

All three exec rows of the pinned census declare mode `755`
(`surface-census.tsv:22,30-31` at `fecee874`). The pristine gate checks the
execute bit (`surface-census.sh:214-217`) before the exact mode
(`:219-223`). A file without the execute bit has a mode other than 755, so the
mutant still fails it on the mode check. A 755 file is executable, so it never
reaches the exec-bit verdict. BuildF6B swept all 512 modes on each of the three
exec rows with the counter's own oracle and found no killing state
(`.ufo/waves/round-29/w1/BuildF6B.md`, "exhaustive sweep"). Seat CriticC2v2
reached the same conclusion from the code before any builder ran (Q5).

So under the pinned declaration the exec-bit arm is redundant with the
exact-mode check. B5 can only be killed by a fixture that declares an exec row
with mode `-`. The round-3 and kaika probes did exactly that (`$HOME/bin/tool`
declared `asset exec -`), and the pinned declaration has no such row. With mode
`-` and the same host, the mutant exits 0 and the oracle kills (BuildF6B, state B).

Bound: this holds on an ordinary executable mount. On a `noexec` mount a 755 file
fails `-x`. That would be a different, environment-made witness, not the craft
F6 asks for, and no seat used it.

## What F6 needs next

- A survivor whose kill is reachable inside its own pinned declaration. Seat
  ScoutF6Next ranks 24 fixture-absent survivors (`.ufo/waves/round-29/w1/ScoutF6Next.md`).
  Before freezing a target, commit one hand-built instance that meets it, as a
  reachability witness.
- Or freeze, before data, a stated transformation of the declaration (for
  example exec rows set to mode `-`), and measure minimization from there.
