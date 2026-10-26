# T50Cross46 — C1 independent cross-coder, spot-check round 46

Seat: T50Cross46. Coded the five routed items R46.1..R46.5 from `.ufo/evidence/round-50/c1/defects.json` independently against the lane tree at base `e3729de862f73ae080d98fcf522a7081ce16e40a` (all reads via `git show e3729de8:<path>` in a `--shared` clone; no T50Disp*.* read). Judgment: 3 fixed, 2 declined, 0 open (no R46.x id appears in any `**Planned (round` paragraph of SCORECARD.md at base — `git show e3729de8:SCORECARD.md | grep -c 'R46\.'` → 0).

## R46.1 — anchor refresh + per-snapshot fetch receipt: FIXED

Commit `50545328e7ac4ba1703d70030e37dacec9362e68` (round-48 C2 records) adds rows S265-S268 and the receipts.

- `corpus/SOURCES.md:142` (row S267): `supersedes S093's anchor and quote only: ... quoted so that --unshare-all's six-flag expansion and the try-else-skip wording ... sit inside one 25-word quote` — pin by quote, not whole-page hash. Rows S265/S266/S267/S268 supersede S026/S048/S093/S108 respectively (lines 140-143).
- `.ufo/evidence/round-48/freshness/sources/S093.receipt.json:2-6`: url, `fetched_at 2026-10-26T08:41:10Z`, `http_status 200`, bytes 33289, sha256 `2cb77df2f4be…` = the row's anchor prefix. The same pattern exists for S026/S048/S108 (4 receipt files, `git ls-tree e3729de8 .ufo/evidence/round-48/freshness/sources/`).

Adversarial check: at routed_at `0b5b7cd2`, rows S265-S268 are absent (`git show 0b5b7cd2:corpus/SOURCES.md | grep -cE '^\| S(265|266|267|268) '` → 0; S026/S093/S108 → 3), so the fix is new since routing.

## R46.2 — hardened counters operative, wave-2 absorption, AST-pin control, named-rule-case kills: FIXED

Commit `9acfbe21435e1976636a276448dee1d5e7155915` (round-47 freeze) + deciding receipts `edd4ca446…`.

- `.ufo/evidence/round-47/hardening/pool.py:17-18`: kill rule requires a `FAIL ` line, i.e. "a named rule case failed"; crash/timeout are not kills.
- `.ufo/evidence/round-47/contract.json:37`: C2 claim is explicitly "adoption of the round-46 hardened counters and a deterministic held pool (round-46 spot-check routed defect 2)"; statement line 39 repeats the FAIL-line kill rule.
- `.ufo/evidence/round-47/control/run-controls.py:183`: `CTL_H_ast_pin_by_bare_assert` (plus CTL_E source-AST pin, line 180) — the AST-pin control proves a source-pinning selftest cannot score (`controls-at-freeze.stdout`: rc=1).
- `.ufo/evidence/round-47/after/c2.stdout:1-2`: the deciding v2 run (`targets=v2`, killed=183 real, neutral_killed=0) kills only via FAIL lines (e.g. `MUT coverage/Tree.read:const:0 killed | FAIL G01_…`); `killed=183` of `applicable=183`, `target=150`, PASS=true.

Adversarial check: the 17 wave-2 fresh mutants might not be individually present (the pool is a generic single-site enumeration, and the v2 counters are byte-equivalent to round-46: equivalence=1). Resolved: the wave-2 mutants were themselves single-point replacements on these same hardened counters (`.ufo/waves/round-46/w2-results.json` T46MutFreshA/B methods: "19/18 NEW single-replacement mutants … ast.parse verified"), so every one maps to a pool id; the pool is the sealed held-out re-attack.

## R46.3 — host-dependent statements hermetic + five tool-less statements sha256: FIXED

Commit `edd4ca44635c9fdf796a4c11953b37481e753537` (round-47 deciding receipts; counter at `9acfbe214…`).

- `.ufo/evidence/round-47/after/c1.stdout:15`: `STATEMENT cap/retained invocation-context gate: … MATCH declared_deps=fleet-root observed_deps=fleet-root DEPS-OK` — the host dependence is now declared and observed, not silent.
- `.ufo/evidence/round-47/after/c1.stdout:16`: profile row shows the fleet-root probe (P5 flips to exit 1; P0-P4 stable) — bwrap-decoy observation.
- `.ufo/evidence/round-47/after/c1.stdout:41`: `STATEMENT axis/calibration: claimed=6|657f009bdf1c observed=6|657f009bdf1c` — tool-less statements now carry a sha256 beside the claim; all 22 statements are pinned (`unpinned=0` in the deciding line; `calibration/measure.py` counts `sha_file`/unpinned).

Adversarial check: the deciding run still executes under the live host (P0) and the round-47 C1 verdict printed false (dep_mismatch=1 on the six-leg regression ledger, an honest miss elsewhere). Resolved: the defect asked for the *observation* to become declared/pinned/hermetic-probed plus sha256s — both exist; the false verdict is a different statement, not absence of the fix.

## R46.4 — lesson quote fidelity (S259 en dash / fold at the quote): DECLINED

`corpus/lessons/round-46.md:42` still prints the hyphen form (`for 9.8 %-16.3 % of failed pipeline runs.`); no fold statement sits at the quote. The en-dash fold is disclosed only in `corpus/knowledge/r5-undetected-flaky-failures.md:25-32`, which does not satisfy "in the lesson itself". The verifier spot-check file is byte-pinned (`sha256sum` = `104c609956cb75dda3214fa179ffa36472696fd3e47500e6893ebbba44b823a0` at both routed_at and base). The lane judged the fold wording-only (recorded at `round-46-verifier-spotcheck.md:20`) and declined to rewrite the landed lesson record; no Planned paragraph names R46.4 → declined (≥40-char reason), not open.

## R46.5 — SHONEN boxes [~], promotion operator-owned: DECLINED

`SHONEN.md` at base still shows all four boxes `[~]` with no independent promotion verifier (`git show e3729de8:SHONEN.md`). The item records a standing state rather than an actionable ask; nothing was implemented and no Planned paragraph names R46.5 → declined: the lane retains operator-owned promotion; no non-author-checkable promotion exists at base.

## Notes

- Spot-check files byte-unchanged (pin holds); no evidence cites a spot-check, the ledger, or the round-50 C1 instrument.
- Evidence lines are 1-based at base; every excerpt verified verbatim (whitespace-normalized match within its cited lines, 15-400 chars, spans ≤ 30, no ACK words).
- Commits cited are full 40-hex hashes, post-routing (0b5b7cd2), ancestors of base.

## Summary

- R46.1 fixed (commit 50545328e…): S265-S268 quote-pinned rows + per-snapshot receipts S026/S048/S093/S108, new since routing.
- R46.2 fixed (commit 9acfbe214…): hardened v2 counters operative, 183-mutant sealed pool (superset of the wave-2 single-point kills), AST-pin controls, FAIL-line kill rule.
- R46.3 fixed (commit edd4ca446…): dependence-declared + bwrap-decoy-probed observation, sha256 on all 22 statements (unpinned=0).
- R46.4 declined: round-46 lesson:42 still hyphen; fold only in entry r5:25-32; lesson record not rewritten.
- R46.5 declined: standing-state item; SHONEN boxes remain [~], promotion operator-owned.
- 0 open at base: no R46.x id in the newest Planned paragraph.
- Spot-check pin unchanged (104c609956…); no forbidden evidence paths used.
- No counter runs performed; coding only from tree reads (`git show e3729de8:<path>`).
