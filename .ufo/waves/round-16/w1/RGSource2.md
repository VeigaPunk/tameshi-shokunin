# RGSource2 — C1 own-work source row draft (round-gate.mjs)

Seat: TameshiR16.RGSource2 (leaf, no delegation, no edits to SOURCES.md, no lane code run).
Scratch: /tmp/tameshi-r16-RGSource2-9bMu/ (materialized file only).

## Behaviour
- Materialized the pinned blob read-only with `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs > /tmp/tameshi-r16-RGSource2-9bMu/round-gate.mjs` (exit 0).
- `sha256sum` → `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9` (matches Target). 1511 lines.
- `git rev-parse --verify -q 364f1d…^{commit}` exit 0; `merge-base --is-ancestor 364f1d5… HEAD` exit 0 (pin is an ancestor of kumitate HEAD).
- `git log -1 -- scripts/round-gate.mjs` → `364f1d5 round-24: triage — … round-gate (60/60) …`. The "60/60" count is the commit subject's claim. I did NOT run `--selftest` (no execution authorized for this seat), so 60/60 is unobserved by me.

## Anchors observed (path:line @ pin)
- round-gate.mjs:2-21 header; :3 "lane-local pre-check of the fleet round-close contract."
- :14-18 the integrator's fleet step is `PROTOCOL.md:263-267`; the tool is the lane-local pre-check of those invariants.
- :19-20 quote (verbatim, leading ` * ` stripped): "a green verdict asserts nothing fleet-wide, and running the gate does not change mission completion (mission state is projected read-only from". 21 words (`wc -w` says 23 only because each ` *` counts as a word).
- :45-48 `--selftest` = HERMETIC fixture suite, temp dirs only, zero network; "bogus flags and a polluted env cannot affect it".
- :294-296 `--origin` derivation skipped under selftest.
- :635 `if (opts.selftest) return selfTest();`
- :689-690 `selfTest()` uses `mkdtempSync(join(tmpdir(), 'kumitate-round-gate-selftest-'))`.
- :1505-1508 selftest prints `ROUND_GATE_SELFTEST: <p>/<n> pass` and `VERDICT: PASS|FAIL`; returns 0 only when all pass.
- :677-681 audit verdict line `ROUND_GATE: <verdict> (round=… lane=… checks=… errors=… warnings=…)`; `return exitCode`.
- Exit map: :63-64 (0 clean, 1 findings, 2 fail-closed, 64 usage); code paths return 2 at :618 and 64 at :633, :638.

## Shape check against fleet-gate rows
- `corpus/SOURCES.md` S032 (line 43, kimi-census.mjs) and S037 (line 48, claims-check.mjs): kind `code`, tier `A`, scope "the gate's own behavior at the measured revision", anchor "kumitate-shokunin/<path> @ <rev> (blob sha256 <8hex>…<5hex>)", status `mined`, opened 2026-10-19, recheck 180d. S033–S036 are the same shape for kagi/tsukuroi/mado gates.
- No row names round-gate.mjs (grep for `round-gate` in SOURCES.md: no match; the only grep hits were S032/S037 on `kumitate-shokunin/scripts/` paths).
- Id: `SOURCES.md:172` "Next unused id: S052". S049–S051 are own-work rows outside the S031–S039 block (precedent for this row). S052 is the id to use, subject to L1 allocation.

## Draft row (for L1 to paste; NOT written to SOURCES.md)

| S052 | kumitate `scripts/round-gate.mjs` (fleet gate, read-only) — kumitate-shokunin/scripts/round-gate.mjs | code | A | round-gate.mjs selftest/verdict behaviour at this pin | kumitate-shokunin/scripts/round-gate.mjs:2-21, :45-48, :635, :677-681 @ 364f1d5954158ef8844bca4a5fef57b05d2f2ca5 (blob sha256 f890e277…4d3e9) | a green verdict from this lane-local pre-check asserts nothing fleet-wide: the integrator's step (PROTOCOL.md:263-267) still decides fleet conformance | mined | 2026-10-20 | 180d | <mutation-case note path — pending L1> |

Notes on the draft:
- Teaches = one learner benefit (green ≠ fleet conformance), quote-backed by :19-20.
- Do NOT add "60/60" to the row unless L1 observes `node scripts/round-gate.mjs --selftest` exit 0 on a /tmp mirror of the pin.
- used-by: no mutation-case note for js-round-gate exists yet in the lane (not checked by me beyond the target). Leave the placeholder for L1.

## Bounded recommendations
1. L1 uses id S052; paste the draft row after S051 (SOURCES.md:60) and bump "Next unused id" to S053.
2. L1 (or a verifier) runs the hermetic selftest once in a /tmp mirror to turn "60/60" from commit-message claim into observation, if the mutation-case note cites it.
3. Keep the abbreviated sha in the row (`f890e277…4d3e9`) to match S032/S037; full sha256 stays in this report.
4. Recheck 180d, status `mined` (not `queued`), matching S032/S037.

## Tooling
- No installs or updates performed.

## Opened paths
- /tmp/tameshi-r16-RGSource2-9bMu/round-gate.mjs (materialized from kumitate-shokunin blob 364f1d5…:scripts/round-gate.mjs)
- /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md (read-only: lines 1-40, 42-51, 60, 137-172 and greps)
- /home/vgpnk/Projects/shokunin/kumitate-shokunin (git show/cat-file/rev-parse/log/merge-base only)
- /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-16/w1/RGSource2.md (write)

## Not run
- No `node round-gate.mjs` of any kind (no selftest, no audit, no mutant). The Target did not authorize execution for this seat, and wave-1 rules forbid mutant runs.
