# T49W2Reread11 — C1 semantic re-read

Reviewed the candidate at `f181a961ae44061af486f600e5ea257d2baf78f8`; detailed row judgments are in `T49W2Reread11.json`.

## Findings

- `SKILL.md:1565` — ordinal 0 does not support the full `Routed defects 1–3` citation: the recorded excerpt only contains the heading and the beginning of defect 1. Command: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f181a961ae44061af486f600e5ea257d2baf78f8:.ufo/evidence/round-49/c1/reads.json`; observed row 0 excerpt ends at “exact kind assertion.” The pointed lesson has defects 1, 2, and 3 at lines 179–181 (`git show f181a961...:corpus/lessons/round-13-verifier-spotcheck.md`), but the excerpt doesn't evidence the latter two.
- `SKILL.md:1567` — ordinal 1 excerpt does not identify the substance of empirical correction 8; it only describes the supersession scope. Same `reads.json` command shows row 1 excerpt ending with “present knowledge.” The pointed source's correction details are at `corpus/knowledge/incremental-pin-disposition.md:353–359` and `:378–384` (`git show f181a961...:corpus/knowledge/incremental-pin-disposition.md`).
- `SKILL.md:1583–1584` — ordinal 3 excerpt shows manifest schema, expected-file path, and an input digest, not the producer_before row/failure used by the replay claim. `reads.json` row 3 excerpt contains only those metadata fields; target manifest rows are later in `.ufo/evidence/round-14/dispositions-before.json` (the pointed file's row producer_before is at lines 35–39).
- `SKILL.md:1588–1590` — ordinal 6 excerpt shows one failed selftest case, not the claimed aggregate 18-of-34 fixture failures. `reads.json` row 6 excerpt is the `clean-superseded FAIL` line; the target's stdout contains the broader suite output.

Commands and observed excerpts: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f181a961ae44061af486f600e5ea257d2baf78f8:.ufo/evidence/round-49/c1/reads.json` returned the above excerpts; `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show f181a961ae44061af486f600e5ea257d2baf78f8:corpus/knowledge/incremental-pin-disposition.md` showed correction detail at 353–359 and the effective ledger at 378–384; the lesson command showed defects at 179–181. No counter was run.

## Summary
- Four excerpts (ordinals 0, 1, 3, 6) fail to support the whole associated clause.
- Corrections reviewed: lines 1582, 1585, 1588, and 1593; pointers/meaning are acceptable.
