# Round 36 lesson (TameshiR36, attempt 1, 2026-10-24)

Two claims, both routed from the round-35 closure: C1 (calibration, lowest
axis) cold-read refresh of the four drifted headings; C2 (depth surface)
successor counter with frozen public-slot cardinality + distinctness asserts.
The third routed defect (LOG dead pointer) is repaired in LOG.md; the fourth
(`code_view` after ANSI-C `$'…'`) is explicitly deferred to round 37 with the
reason recorded (a tool edit would void the round-35 capability pin).

## What this round attacked, and why

- The r35 closure pinned calibration at 6 (was 8): four SKILL headings lost
  cold-read credit because the r35 record repairs rewrote their cited inputs
  (`LOG.md`, `SCORECARD.md`, `corpus/README.md`, `corpus/SOURCES.md`,
  `corpus/QUALITY.md`, `corpus/knowledge/closeout-r11.md`,
  `corpus/knowledge/survivor-fixture-minimization.md`,
  `tools/mutate-and-run.sh` — the union across the four sections' failing
  ledger entries). The refresh re-anchors those headings at current bytes
  under the round-21 L1 author-source-read protocol (trace receipts + new
  ledger entries; scope: input-keyed source reads only, not a blind
  cold-read).
- The r35 closure's defect 2: the frozen v1 counter's PASS compared
  kill/accept counts only against the manifest's own slot counts, so an
  emptied public panel passes vacuously. The successor v2 counter freezes
  the public surface (6 kill slots, 3 accept slots, 9 distinct bodies) as
  asserted targets, pre-data.

## Gate

- Opened this round:
  - **S103 admit** — git-hash-object (Git reference manual) —
    https://git-scm.com/docs/git-hash-object — opened 2026-10-24 UTC
    (curl exit 0; 29,933 bytes; SHA-256
    `dd826daeeacaea01858ab1330e6f014ed1a0741652e5a710c578d137711f6100`;
    committed snapshot `.ufo/evidence/round-36/src/s103-git-hash-object.html`).
    Located quote, §DESCRIPTION first sentence (snapshot line region
    "DESCRIPTION"): "Computes the object ID value for an object with
    specified type with the contents of the named file" (19 words). Teaches:
    a blob's ID is computed from the file's contents, so a recorded digest
    binds audit evidence to exact bytes — the ground for sha256-pinned
    inputs, traces and tool pins. Mined into
    `.ufo/evidence/round-36/coldread/refresh-receipts.json` (the refresh's
    byte-identity discipline) and this lesson. Tier A, status `mined`.
- Rejected this round: none (no other source was opened; the r34/r35
  gnu.org Bash manual Comments-page rejections stand and were not re-tried).
- Rows: 99 → 100 (S103 only). No status/recheck/used-by flips on existing
  rows.
- Census: round start (tip `796e08b`) `sources-census.sh validate` exit 0,
  99 rows; round end (refresh commit) exit 0, 100 rows — both receipts kept
  under `.ufo/evidence/round-36/`.

## Mistakes

- **class: reference-drift** · evidence: `LOG.md` round-35 entry names
  `ResidualSentinelClosure.md`; `git log --all -- '*ResidualSentinelClosure*'`
  is empty and the residual dir holds exactly five committed reports
  (r35 closure routed defect 1) · captured-by: none at write time — the r35
  closure's non-author sweep caught it · fix: append-only correction entry in
  `LOG.md` (round-36 section) naming the five real residual reports, and
  `QUALITY.md` criterion 72 requiring every LOG evidence pointer to
  re-resolve before commit. Shown able to fail: criterion 72's falsifier
  pointer IS the r35 dead pointer; a future pointer that fails to resolve
  violates the criterion.

## Holds

- The `code_view` ANSI-C `$'…'` quote class (r35 routed defect 3; round-35
  lesson `## Holds` first filing) stays open: NOT fixed this round. Reason:
  the fix lives in `tools/tally-audit-v3.py`, whose sha256
  (`6188db16…`) is pinned by the round-35 capability row, the frozen v1
  counter and the v2 successor; a tool edit would void all three and demand
  a full re-audit beyond this round. Planned round 37 under
  freeze-before-data with re-pin + re-attest (real shell lexer or an
  enumerated supported-form list).
- Refresh scope honesty: the four re-anchored headings are credited by L1
  author source reads (byte-consumption observations), not by a fresh blind
  cold-read; a future round that wants the stronger credit re-reads the
  sections independently.

## Wave note

This L1 seat has no swarm-dispatch tool (host surface note): w1 (build, 39
seats) and w2 (falsify, 39 seats) are prepared under `.ufo/waves/round-36/`
as validator-checked specs for the orchestrator to dispatch between rounds;
the round report itemizes the 78 prepared-but-undispatched seats.

## Erratum — round-36 wave note (append-only, recorded in round 37)

The preceding sentence's “itemizes” means aggregate seat counts/role mix, not a list of all seat names. The lane report records 39 + 39 = 78 prepared seats; individual names/items are in `spec-w1.json` and `spec-w2.json`. The committed validator payload renders are `validate-w1.stdout` and `validate-w2.stdout` with empty `.stderr`; there are no `validate-w*.json` artifacts or separate exit receipts. This does not change the round-36 count or dispatch status.

## Errata — round-36 source/census record (append-only, recorded in round 37)

- **S103 quote count/location:** the quoted text in the prior Gate is 18 words, not 19, and is the opening prefix of the first sentence, which continues after “file” (`.ufo/evidence/round-36/src/s103-git-hash-object.html:1607-1611`). Round 37 re-counted the exact text with `printf '%s\n' 'Computes the object ID value for an object with specified type with the contents of the named file' | wc -w` → `18`; the S103 anchor remains §DESCRIPTION.
- **S103 use:** the r36 `refresh-receipts.json` contains a `cited_source` field, but the W2 peer audit reports this field is not consumed by the cold-read monitor. Round 37 makes no claim that S103 is load-bearing to C1 and changes S103 `used-by` from the receipt plus this lesson to this lesson only; S103 remains mined by this lesson. The peer report is preserved as peer-owned, uncommitted evidence and was not staged by this L1.
- **Start-census receipt:** the prior text says both census receipts were kept under `.ufo/evidence/round-36/`; only the end-side census receipt exists. The start value `99` re-derives at `796e08b` using `git show 796e08b888849308d0c4d5e932e56833600a139f:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → `99`, but no start-census stdout/exit receipt is committed. Round 37 commits its own start-census receipt.
