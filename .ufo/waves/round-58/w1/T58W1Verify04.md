# T58W1Verify04 — row verification

Base: `2a32aa8228d5f86a85c81a923a3148bf792a9538`. Assigned rows: R52.1–R52.4.

## Evidence and proposed rows

- **R52.1 — fixed at base.** Read `corpus/lessons/round-53.md` at base (`git show ...:corpus/lessons/round-53.md`): lines 6–10 identify the R52.1 cold-read floor repair as round-53's C1 claim and say it repairs what the round-52 closure routed. Read `LOG.md` at base: lines 2617–2622 identify commit `bc3c8895b75aec65e3006193d0c1857641dbb385` as landing the settled wave evidence and 18 bindings; phase 2 at that revision exited 0 with `covered=64/64 score=8 box3=True`, strict trace gate and no overrides. Resolving commit: `bc3c8895b75aec65e3006193d0c1857641dbb385` (not the initial repair-intent commit).
- **R52.2 — fixed at base.** `git show ...:LOG.md` shows the appended `2026-10-27 — round 52 (honest stop, run wrap-up)` entry, including landed `bcba8924 → f1a32461` and the wrap-up disposition (base LOG.md lines 2584–2592). `git log --all --format='%H %s' -- LOG.md` identifies the entry addition as `a41195dfc13a73958e4c5228ec196b28d03ded03`.
- **R52.3 — open at base.** `git show ...:corpus/lessons/round-52.md` lines 24–28 still gives the `8 over-count` result and Corr12's “0 of 14” example. `git show ...:corpus/lessons/round-52-verifier-spotcheck.md` lines 46–48 records the closure's contradictory re-derivation (at least 2 to 6 marked failures), yet does not replace that lesson row. Planned round-58 intent: independently re-derive all requested records under the routed counting rule and correct the lesson if warranted.
- **R52.4 — fixed at base.** `git show ...:corpus/lessons/round-52-verifier-spotcheck.md` lines 18 and 86 documents the four then-untracked paths. `git ls-tree -r --name-only 2a32aa8228d5f86a85c81a923a3148bf792a9538 .ufo/waves/round-52/w3 .ufo/evidence/round-52` lists the integration script and committed w3 tree at base. `git log --all --format='%H %s' -- .ufo/evidence/round-52/integrate/build-readers.py` reports `6db1d220b337c35ff1e25bf9cfd74abc9db1498d` as the round-52 wave-3 salvage commit, which committed those leftovers.

## Commands used

- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2a32aa8228d5f86a85c81a923a3148bf792a9538:corpus/lessons/round-52-verifier-spotcheck.md` — output contains the routed defects and their original claims.
- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2a32aa8228d5f86a85c81a923a3148bf792a9538:LOG.md` — output contains the round-52 entry and round-57 continuation binding record.
- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2a32aa8228d5f86a85c81a923a3148bf792a9538:corpus/lessons/round-53.md` — output states the R52.1 repair scope.
- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2a32aa8228d5f86a85c81a923a3148bf792a9538:corpus/lessons/round-52.md` — output preserves the disputed over-count claim.
- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree -r --name-only 2a32aa8228d5f86a85c81a923a3148bf792a9538 .ufo/waves/round-52/w3 .ufo/evidence/round-52` — output lists `build-readers.py` and the round-52 w3 artifacts as tracked.
- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --all --format='%H %s' -- LOG.md` — output includes `a41195dfc13a73958e4c5228ec196b28d03ded03` for the LOG entry change.
- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --all --format='%H %s' -- .ufo/evidence/round-52/integrate/build-readers.py` — output identifies the salvage commit `6db1d220b337c35ff1e25bf9cfd74abc9db1498d`.

No tests, builds, linters or formatters run. No tools installed. No scratch directory was created. Only the assigned JSON and report were written; no lane production file was edited. No additional receipts were required for this source-based verification.
