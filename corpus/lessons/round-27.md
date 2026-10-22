# Round 27 — cold-read monitor repair and frontier F8 (oracle anchoring)

L1 TameshiR27, attempt 1, 2026-10-22. Base `91edf9cd82ccc72e10f62f81d37181f549d593b8`.
Pre-registration `70df8d6a485418d9e57fed9d21e84fba71d4be66` (contract, both
counters, before-values, round-26 C2 correction); anchors and probe
`06a6707904582cc2f268d8a74861c6a8d09dd1fe`; content revision
`2227d8338c02aa9a5fd7d95c1a41b76865ad7647` (F8 entry, receipt, SOURCES, README,
QUALITY 53–54, counter amendment 1). Every cold read of this round is made at
the content revision.

## Claims

- **C1 calibration, harm repair.** SHONEN box 3 `[~]` cites the cold-read
  ledger; the strict monitor credited 25 of 64 sections at base, so box 3
  and the repo disagreed. Repair: independent seat cold reads of every
  uncovered section at `2227d83`, assembled into the round-21 ledger by
  append only. Counter `.ufo/evidence/round-27/c1-measure.py`.
- **C2 coverage, frontier F8, learning claim.** The four round-26
  cite-check hole survivors re-judged against expectations fixed outside the
  mutated code. Counter `.ufo/evidence/round-27/c2-measure.py`. Entry
  `corpus/knowledge/oracle-anchored-survivors.md`.

## Gate

Sources opened this round (ordinary fetch, 2026-10-22):

- **S012** (re-opened; row since round 1) — https://arxiv.org/abs/2608.17214,
  abstract. Quote (25 words): "An expectation is specification-anchored when
  composed from values fixed outside the code under mutation, and
  state-anchored when it flows, directly or transitively, from that code."
  Status `queued` → `mined`; used-by `—` →
  `corpus/knowledge/oracle-anchored-survivors.md`; opened and recheck cells
  unchanged (append-only rule). Decision: admit as the definition source for
  the F8 entry; its measured rates (one system, one author, tier B) are not
  used.
- **S090** (new) — https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3,
  §ERRORS. Quote (17 words): "EX_USAGE (64) The command was used incorrectly,
  e.g., with the wrong number of arguments, a bad flag". Status `mined`,
  recheck 365d. Decision: admit as an outside anchor for a usage exit of 64.
  The page calls the interface legacy and deprecated; the entry uses it only
  as a fixed convention, not as a recommendation.
- **S091** (new) — https://git-scm.com/docs/gitrevisions, §SPECIFYING
  REVISIONS `<sha1>`. Quote (18 words): "The full SHA-1 object name (40-byte
  hexadecimal string), or a leading substring that is unique within the
  repository." Status `mined`, recheck 365d. Decision: admit as a
  convention anchor only; it speaks of Git object names, not content pins, and
  the entry says so.

Rejected reading: "anchored_holes=4 shows the round-26 differential method is
sound". It shows the four calls agree with outside anchors on one gate; the
other eight legs' hole calls are not anchored.

## Mistakes

1. **Harm-repair wave cancelled; record contradicted the monitor (round 26).**
   Class: calibration record. Evidence:
   `lessons/round-26-verifier-spotcheck.md:112-135` (62/62, restraint 8 →
   25/64, restraint 6) against SCORECARD's round-26 C2 row "numeric 8 → 8".
   Captured-by: none in round 26. Fix: QUALITY 53 and the frozen counter
   `.ufo/evidence/round-27/c1-measure.py`, shown able to fail: it exits 1 with
   `box3_mismatch=1` at base `91edf9cd` (`c1-before.stdout`); the SCORECARD
   row is corrected by an appended entry.
2. **Frozen counter check that only a contract breach could pass (this
   round).** Class: counter design. Evidence: `c2-measure.py` as frozen in
   `70df8d6` required S012's `opened` cell to read 2026-10-22, but CORPUS.md
   SOURCES contract rule 2 lets only status, recheck and used-by change in
   place. Captured-by: the SOURCES contract, read before the row was edited.
   Fix: `contract-amendment-1.json`, before any after-measurement; the target
   (`classified=4`) is unchanged and the amended counter still reads 0 at base
   (`c2-before-amended.stdout`).
3. **Registry run outside a fleet mirror (this round).** Class: measurement
   setup. Evidence: `tools/registry-check.py --rev 2227d83` from clones in
   directories with no `*-shokunin` siblings read `held=46/49`: the runner
   regression and two dependent rows refused with `repo_identity_mismatch …
   is not its own repository`, because the tool symlinks the siblings of the
   clone's parent directory (`tools/registry-check.py:770-782`). Captured-by:
   none. Fix: run it from a clone whose parent holds symlinks to every
   sibling (the mirror receipt is the one committed); the earlier readings are
   kept in this lesson, not in the receipts.
