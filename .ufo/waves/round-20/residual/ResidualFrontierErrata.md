# ResidualFrontierErrata — S049 used-by transition + round-19 appended erratum

seat: TameshiR20-3.ResidualFrontierErrata · 2026-10-21 · source-only falsification attack.
No code, gate, census or counting command was executed; no Git/JJ query was run; no file
outside this report was written. Every claim below cites read source bytes.

## Verdict

No High or Medium defect found in the assigned surfaces. The S049 used-by transition is
exact, completely logged, and immutability holds; the appended round-19 erratum matches
its outside-routed trigger instrument-for-instrument and supersedes only the named
singular phrase. Two Low findings and one out-of-scope observation follow, plus
verification gaps that only L1's post-wave git/digest pass can close.

## Findings

### Low-1 — round-20 S049 reopen has no `## Search log` bullet; validator scan omits rule-5 counts

- Precedent: every prior reopen of S049 carries a dated Search-log bullet in
  `corpus/SOURCES.md` — round-14 (`:155-159`, identified2/screened2/included2/excluded0),
  round-15 (`:160-163`, 1/1/1/0), round-19 (`:165-171`, 1/1/1/0). Round-20's reopen is
  documented only by a trailing paragraph after `## Id allocation` (`SOURCES.md:225-228`)
  plus the lesson Gate (`corpus/lessons/round-20.md:13`, `:35-38`).
- Contract mapping: `SOURCES-CONTRACT-v1.md` rule 2 requires the old→new transition logged
  "in the round lesson" — satisfied (`round-20.md:35-38`). Rule 5's Search-log note is
  "one prose note per bounded search"; the round-20 bounded validator scan
  (`round-20.md`, "Source transitions and bounded search") records question, locations,
  date and stop rationale but explicitly declines identified/screened/included/excluded
  counts ("No search-result count or global absence is inferred"). It also disclaims any
  absence claim, so no negative claim carries an underswept log.
- Harm: none to claim validity; register hygiene/precedent drift only. Fix belongs to L1
  as an append-only dated Search-log bullet at the next corpus touch. Not fixed here
  (read-only seat, single permitted output file).

### Low-2 — erratum's "local BRT" names a civil zone the sources do not

- `corpus/lessons/round-19.md:367-368`: "historical local BRT, UTC−03:00". Source
  evidence grounds the offset (host timestamps `-03:00`, `round-19.md:299` region —
  pycache birth `2026-10-21T02:59:17-03:00`) and the "local" label (outside review
  `round-19-verifier-spotcheck.md:174`: "row `2026-10-20` local vs lesson … UTC").
  "BRT" as the civil name is the lane's label; UTC−03:00 is not uniquely Brazil. The
  operative content (different date bases, row date retained) is unaffected. No edit
  required; precision note for future errata.

### Out-of-scope observation (pre-existing, not this diff)

- `corpus/SOURCES.md` Search log is not in append order: the round-19 bullet (2026-10-21,
  `:165`) precedes the round-16 bullet (2026-10-20, `:173`). Either the round-16 entry was
  backfilled or a mid-log insertion occurred. Outside the assigned S049/erratum surfaces;
  flagged for L1's registry pass, not judged here.

## Verified positives (per assigned axis)

### A — S049 used-by transition is exact and fully chain-logged

- Old→new chain, each logged in its own round lesson: round-14 `round-14.md:30-33`
  (`round-14.md` → +`incremental-pin-disposition.md`); round-15 `round-15.md:22-24`
  (+`round-15.md`); round-19 `round-19.md:35-38` (+`round-19.md`); round-20
  `round-20.md:35-38` (+`round-20.md`).
- Current row `corpus/SOURCES.md:58` used-by is byte-equal to round-20's "new" list
  (five paths, no more, no fewer). Status `mined`, recheck `on-release` unchanged.
- All five used-by paths genuinely cite S049 (no decorative backlink):
  `round-14.md:16,24`; `incremental-pin-disposition.md:359`; `round-15.md:13-16,22-24`;
  `round-19.md:27-38`; `round-20.md:13,35-38`.
- Round-19's other mutable edits retained: S063/S077/S078 used-by each = old list +
  `corpus/knowledge/guard-kill-closure.md` (`SOURCES.md:77-79` region), matching
  `round-19.md` source-sweep addendum. No new row: registry ends at S078, footer and
  id-allocation keep "next unused id: S079" (`SOURCES.md:220-228`).

### B — original opening vs separate reopening (not one midnight conversion)

- Three date statements cohere: immutable row `opened 2026-10-20` (`SOURCES.md:58`,
  retained per `round-20.md:34-38` Gate and footer `:225-228`); round-19 lesson
  "reopened 2026-10-21" (`round-19.md:27`); round-20 reopen "2026-10-21 UTC"
  (`round-20.md:13`). Outside review routed item 3 prescribed exactly this explicit
  basis split (`round-19-verifier-spotcheck.md:174-175`); round-20 implements it.
- Distinctness is documentation-grounded, not clock-grounded: round-14's opening and
  round-19's reopening are independent bounded searches with different questions and
  counts (round-14 bullet: 2 sources incl. new S049; round-19 bullet: 1 source, receipt
  question) — one physical access cannot be both. The erratum correctly disclaims
  "No exact access instant is inferred from commit time" (`round-19.md:372-373`), so the
  two-commit corroboration (`0c6e36d` / `21e7932`, `:369-371`) is offered as chronology,
  not as access-time proof. The midnight-conversion reading is excluded on the
  documentation itself.

### C — four distinct historical instrument SHAs vs the wave-2 frozen ruler

- Erratum table `round-19.md:344-352` lists exactly four identities — `96a68b60…`
  (wave-1 round-19 ruler, `w1/ReceiptDesign.md`), `8dfaa25a…` (witness tool) +
  `d22c4025…` (witness runner, "same witness receipt"), `7ca87a7c…` (round-18 measure,
  `w1/RevisionBinding.md`) — all pairwise distinct by inspection, none equal to the
  wave-2 ruler bytes `bb651eef…5053` (`:353-354`), which is kept separate with its git
  pin `55e1d312…805c9`.
- The four match outside routed item 2's instrument set exactly
  (`round-19-verifier-spotcheck.md:172-173`: same four SHAs, same grouping, same
  `bb651eef…` caution) — the erratum is the routed fix, not a paraphrase.
- Cross-corroboration: `7ca87a7c…26dd37` matches the round-18 instrument blob cited at
  `round-19.md` No-harm/AxisBound section; `bb651eef…` matches the frozen55e1
  restoration line in the workflow-mistake section; `96a68b60…` is corroborated by LOG
  (`LOG.md:1320` region: "E07 reconstructs historical SHA96a68b60 from the committed
  ReceiptDesign fenced code, not a nonexistent standalone blob") — provenance stated as
  reconstruction, no invented execution.
- Three probes → four identities is explained in-table ("same witness receipt" binds
  tool + runner). Supersession is scoped: "Supersedes only line 299's singular 'the
  frozen SHA'" (`:341-342`); original round-19 bytes and the ADMITTED verdict remain —
  append-only respected.

### D — immutable source cells retained

- Current S049 row (`SOURCES.md:58`): id/source/kind=docs/tier=A/scope/anchor
  ("Python 3.15.0 docs served 2026-10-20")/teaches/opened=2026-10-20 all agree with the
  independent round-19 spotcheck's row reading (`:135`: scope quote "not proof of a
  particular historical environment"; quote exactness "14 words, curly apostrophe") and
  with round-14's admission record (`round-14.md:16,24`). Only mutable cells moved, and
  only in the logged pattern (axis A).

### E — QUALITY41, sourced claim, grounded mistakes/falsifiers

- QUALITY41 exists (`corpus/QUALITY.md`, "Criterion appended — round 20 (2026-10-21)"):
  freezes SHA-256 before dispatch, installs after readers return, interval rules
  (frozen ends ≤ edit start; installed starts ≥ edit end), "classify older instrument
  identities explicitly instead of calling them all 'the frozen SHA'" — the exact
  failure the erratum repairs. Its falsifier (exit-1 fixtures UNKNOWN_INSTRUMENT /
  FROZEN_AFTER_EDIT / INSTALLED_BEFORE_INSTALL) matches the round-20 Gate reject list
  (`round-20.md:16`) one-for-one and the SKILL receipt-window exit map
  (`SKILL.md:1944` region: 0 clean; 1 failed; 2 could-not-evaluate; 64 usage).
  It does not supersede QUALITY20/21, as LOG records (`LOG.md:1316-1319`).
- Sourced claim: round-20 C1's S049 use stays inside the row's scope — "Supports only
  explicit child environment construction, not authenticity of a historical execution"
  (`round-20.md:13`). The quoted sentence is 14 whitespace-separated words (hand-
  counted) with the curly apostrophe, identical across `round-19.md:29-30`,
  spotcheck `:135`, `round-20.md:13`.
- All four round-20 Mistakes rows name evidence, capture, and a failure-capable fix
  (`round-20.md:39-46`): freeze-order + red/green fixture receipts; the four-identity
  erratum with old bytes retained; the `--check` command correction keeping the usage
  rejection ("command correction, not a new ruler or denominator"); failed-provider
  recording with no replacement. Minor citation nit: Mistakes row 1 names QUALITY20/21
  but not QUALITY41 itself; the linkage runs QUALITY41 → the Mistakes table and via
  LOG/README/SKILL, so the cross-reference is discoverable — informational only.

## Residual risk and verification gaps (L1's final pass; unreachable source-only)

1. Commit identities cited but unread (no Git execution allowed here): `0c6e36d`
   (original S049 row present), `21e7932` (reopening lesson), `6fd220b` (frozen
   contract/instruments), `c144dcd` (baseline), `55e1d312` (wave-2 ruler commit),
   `c51eb32f` (pushed registry anchors). The erratum's "two commits corroborate" rests
   on E01S049Open's chronology plus lane records until L1 runs the git reads.
2. SHA-256 digests not recomputed (no hashing/counting commands): the five 64-hex
   identities (`96a68b60…`, `8dfaa25a…`, `d22c4025…`, `7ca87a7c…`, `bb651eef…`) passed
   only consistency cross-checks (abbreviated forms, routed item 2, LOG/E07 note), not
   byte recomputation from receipts.
3. Byte-level proof that round-20 changed exactly one mutable cell of SOURCES.md needs
   a git diff at L1's final verification. Every source-visible signal agrees (row bytes,
   footer, id allocation, S063/S077/S078 retention, S079 next unused), but diff
   evidence was not produced here.

Advisory only; this seat makes no admission, promotion, or non-author judgment.
