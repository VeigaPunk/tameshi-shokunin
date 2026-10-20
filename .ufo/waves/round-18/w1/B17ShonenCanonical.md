# B17ShonenCanonical — round 18 wave 1 — staged canonical SHONEN.md

Verdict: **built** (staged file written and verified; install by L1 pending). Box-3 pointer resolves only after wave 2 writes `.ufo/evidence/round-18/coldread/ledger.json`; that file is absent at base rev.

## Behaviour

Wrote `.ufo/waves/round-18/staged/SHONEN.md` (739 bytes, 12 lines) in the canonical seed form from L1's correction (PROTOCOL.md seed block, name = `tameshi-shokunin`):

- each box line is the template text verbatim, mark changed `[ ]` → `[~]`, no ` — pointer` suffix;
- followed by exactly one indented evidence line (two spaces + markdown link);
- box 1 → `reports/round-1-calibration.md#box-1`; box 2 → `reports/round-1-calibration.md#box-2`; box 3 → `.ufo/evidence/round-18/coldread/ledger.json`; box 4 → `reports/round-1-calibration.md#box-4`.

The staged directory did not exist before; it was created inside the lane root. No other file was touched.

## Evidence (commands run from the lane root; base = 183f87b899e6cae46be98d251cbc87fb5118f6ca)

1. `diff <template name-substituted> staged` — exit 1; the only differences are the four box lines (mark `[ ]`→`[~]`) and the four added indented evidence lines (hunk `5,8c5,12`). Box lines match the template modulo mark: `BOX_LINES_MATCH_TEMPLATE_MODULO_MARK`.
2. Prefix: `cmp` of base lines 1–4 and staged lines 1–4 → `PREFIX_IDENTICAL` (heading, blank, "Promotion to shokunin requires all of:", blank).
3. `diff base staged`: base lines 10–11 (box-3 round-16 full-page pointer and its Correction paragraph) replaced by the single ledger line; base line 13 (box-4 label) trimmed to the standard label; box 1, 2 and their pointers and all marks otherwise unchanged. Base had 13 lines; staged has 12.
4. Command C (SCORECARD.md:75) on staged: `boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8`.
5. Box-3 block contains the path: `staged:10` — `  [lane assertion, no independent promotion verifier](.ufo/evidence/round-18/coldread/ledger.json)`.
6. Pointer anchors at base: `reports/round-1-calibration.md` has `## box-1` (line 71), `## box-2` (line 105), `## box-4` (line 167) — each count 1.
7. `git cat-file -e 183f87…:.ufo/evidence/round-18/coldread/ledger.json` → exit 128 (absent at base, expected; created by wave 2).
8. Source of the seed: `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:440–470` (seed block at 446, 453–465) and `templates/mint/SHONEN.md`; they match after name substitution.

## Interpretation notes

- The Target's "base + appended block only" wording is superseded by L1's binding correction (the box region is replaced). The only byte-identical prefix is the four-line header, which `cmp` confirms.
- Box wording is unchanged from the template, so the SCORECARD calibration falsifier ("any changed box wording") does not fire.
- Box-4 label text that was removed from SHONEN is preserved verbatim in the LOG draft below (round-1 PROVINCE correction note), so nothing is lost.

## Draft LOG.md lines (verbatim preservation of removed correction prose)

Append to `LOG.md` (L1 installs; this seat does not edit LOG.md). Bytes are copied from base `SHONEN.md` lines 10–11 and 13 and are not reworded:

```
Round 18 — SHONEN.md canonical seed restore (B17). Removed from SHONEN.md; preserved verbatim:

- box 3 round-16 full-page evidence line (was SHONEN.md:10 at 183f87b899e6cae46be98d251cbc87fb5118f6ca):
  [lane assertion, full page: round-16 cold-read of every SKILL.md bucket (preamble + every heading outside code fences) by lane-dispatched seats, instructions executed in /tmp, records re-anchored, wrong expectations repaired and re-read; ledger .ufo/evidence/round-16/coldread/ledger.json, counted by .ufo/evidence/round-16/measure.py; supersedes the round-1 Appendix A + B-only scope (reports/round-1-kaika-coldread.md); no independent promotion verifier](.ufo/evidence/round-16/coldread/ledger.json)
- box 3 correction paragraph (was SHONEN.md:11 at 183f87b899e6cae46be98d251cbc87fb5118f6ca):
  Correction (round 17, routed R16-C2c): the round-16 full-page assertion above was wrong at 09ee1d0 on one bucket, `## Effective expectation reconciliation — round 14`: its credit was sha-only, its runner input had moved (`75ed934d…` → `0673d2e5…`), and its recipe exited 2 instead of the recorded 1/0 (corpus/lessons/round-16-verifier-spotcheck.md §2). Round 17 keys every credit to the recorded input digests and re-reads the page; lane assertion, no independent promotion verifier: [round-17 input-keyed cold-read ledger](.ufo/evidence/round-17/coldread/ledger.json)
- box 4 evidence label (was SHONEN.md:13 at 183f87b899e6cae46be98d251cbc87fb5118f6ca; pointer unchanged):
  [lane assertion, no independent promotion verifier; PROVINCE.md Core list corrected by append (tsukuroi and mado gates), fleet round 1](reports/round-1-calibration.md#box-4)
```

Note on the draft: the `—` and `…` characters are the base bytes; the draft is reproduced from the base file in this seat's review and must be checked with `git show 183f87b…:SHONEN.md | sed -n '10,11p;13p'` before it is appended to LOG.md.

## Out of scope / not done

- Not installed into the lane (L1 installs from `staged/`).
- SCORECARD.md, LOG.md, MANIFEST.json, reports/ untouched.
- No verification beyond the listed commands; no subagent dispatch; no tool installs.
