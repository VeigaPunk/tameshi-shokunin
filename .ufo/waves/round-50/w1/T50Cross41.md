# T50Cross41 — independent coding (R41.1–R41.7)

**Axis: calibration** (independent item dispositions). I judged the base tree at `e3729de862f73ae080d98fcf522a7081ce16e40a`, not prose claims alone. The frozen statement set is `.ufo/evidence/round-50/c1/defects.json`; source routing text is `corpus/lessons/round-41-verifier-spotcheck.md:69-75`. Command for cited source lines: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show e3729de862f73ae080d98fcf522a7081ce16e40a:<path>`.

| ID | Code | Evidence and reasoning |
|---|---|---|
| R41.1 | fixed | `tools/write-path-census-v3.py:79` uses `BACKTICK_RE = re.compile(r'`([^`\\n]+)`')`; `:216-237` parses and walks source. The newline is excluded, repairing the routed pairing defect. Strongest doubt: AST parsing might be unrelated to regex behavior; checked the exact regex and its use in the counter. |
| R41.2 | open | `.ufo/waves/round-41/residual/receipt.json:14-16` still says `present:false`; the round-41 report exists. `corpus/lessons/round-42.md:159-160` documents the stale claim and superseding-receipt route, not a corrected receipt. The original counterexample remains in the tree. |
| R41.3 | fixed | `.ufo/evidence/round-42/calibration/measure.py:78-80` line-scopes backtick extraction. Its implementation/docstring includes the requested non-vacuous records, process invocation, resolved inspection and exit-plus-FAIL oracle (inspect via `python3 .ufo/evidence/round-42/calibration/measure.py --help` only if needed; no counter was run). Strongest doubt: only regex repair might not meet the compound successor pair; the counter includes the additional requested gates. |
| R41.4 | fixed | `corpus/knowledge/r42-attribute-and-outflag-destinations.md:31-33` names both context-capture false positives and registry-replay:123, states the resolved classifications, and explains their destinations. Round-42 lesson `:252-253` says v4 resolves them while v3 remains pinned. Strongest doubt: v3 still produces its old false positives; checked the explicit successor replacement, rather than assuming a prose claim fixed v3 itself. |
| R41.5 | fixed | `tools/write-path-census-v3.py:15-21` replaces the blanket “NOT resolved” scope with bounded resolution and explicit unresolved categories. Strongest doubt: the hash-pinned v3 may have retained the old docstring while v4 corrected it; the cited v3 docstring itself is the scoped correction. |
| R41.6 | open | `corpus/SOURCES.md:464-465` records S153/S154 collisions and says no renumber map was applied. Round-42 and round-43 records continue to report the staged collision hazard; no complete by-document renumbering of the staged package is evidenced. Strongest doubt: round 42 did safely map the specific adopted PIT documents; that partial mapping does not close this broader staged-package hazard. |
| R41.7 | open | `corpus/SOURCES.md:464-465` is the original registry block; `corpus/lessons/round-42.md:254-255` explicitly leaves the cosmetic list split untouched. Strongest doubt: later formatting might have repaired it; the lesson specifically confirms it remains. |

Cited evidence is anchored to source files and bounded lines; no spot-check prose or peer seat files were used. JSON codes and strongest-counter-reason checks are in `T50Cross41.json`.

## Summary
- Fixed: R41.1, R41.3, R41.4, R41.5.
- Open: R41.2, R41.6, R41.7.
- Commands: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show e3729de862f73ae080d98fcf522a7081ce16e40a:<path>`; `python3 .ufo/evidence/round-42/calibration/measure.py --help` (not run).
