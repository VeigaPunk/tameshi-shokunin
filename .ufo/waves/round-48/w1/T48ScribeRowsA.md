# T48ScribeRowsA — C2 rows and entry edits for S026 and S048

Round 48 (hyaku run 8, attempt 1), wave 1, seat T48ScribeRowsA (leaf, no dispatch).
Lane `tameshi-shokunin`, base `473336d9d789f6081195e7376d17836a24666bc3`, checkout HEAD
`f1cfaad` (pre-data amendments + wave-1 spec). Contract read first, including amendments
1–3; it was not edited. I ran no deciding measurement and scored no control.

## Deliverable

`.ufo/waves/round-48/w1/T48ScribeRowsA.rows.md` — paste-ready for the L1:

1. Two 11-cell registry rows: **S265** (supersedes S026) and **S266** (supersedes S048), with
   `opened 2026-10-26`, `status mined`, base cadence 730d/90d, used-by exactly each base
   used-by cell, scope deliberately distinct from the base row, anchor carrying section +
   revision/date + the snapshot's 12-hex digest + bytes, teaches opening `supersedes T —`.
2. Two Gate lines in the frozen amendment-2 format (S265/S026 15-token quote with `84%`;
   S266/S048 21-token quote with `should therefore be prioritised`).
3. Exact replacement `source:` lines and `verified-at: 2026-10-26` lines for
   `corpus/knowledge/repeated-control-precondition.md` and
   `corpus/knowledge/incremental-pin-disposition.md`, with old→new stated.
4. Gate block prose per CORPUS.md rule 1 (URL, access date, located quote, location, what it
   grounds).
5. Evidence: my own live fetch, quote offsets, per-claim re-checks, drift table, probe output,
   findings.

## Behaviour observed (all first-hand)

- **Live fetch, my own** (independent of the fetch seats' reports): S026 blog post HTTP 200,
  236387 B, sha256 `a4c5c46b4af9d54baa215b9d76c91cb5b8e9855ad153103b0a34ff3e39869d25`;
  S048 PIT page HTTP 200, 8892 B, sha256
  `e9cbc3e1ab7cce33e02692e47b0539094fc67dda5f862363d73c477ffae590db`. Both equal the committed
  wave-1 snapshots byte-for-byte, so the anchors describe exactly what the L1 will commit.
- **Quotes relocated with the counter's own `extract()`** (amendment 2, no folding): S026 quote
  one occurrence at char offset 2136 (raw line 1132 articleBody, 1097 template copy); S048
  quote one occurrence at offset 1013 (raw line 86, fourth `<li>` of §Incremental analysis).
  I adopted both fetch-seat quotes verbatim; neither needed replacement.
- **Entry claims still hold** against the live text: every sentence the two entries quote from
  S026 and from the PIT page was re-located verbatim (definition, 1.5%, 16%, 84%, monitors,
  rerun family, fail-3-in-a-row, 45 minutes; PIT rules 2–3, item 4 with `(since 1.14.4)`, item
  5 `(not yet implemented)`, the potential-error sentence, both dependency paragraphs, the
  history-provenance sentence). The entries' own recheck command still reads 2 for
  `hardly a perfect solution` (post body + template copy), its healthy count.
- **Byte drift**: S048 unchanged since 2026-10-20 (`cmp` identical to the round-45 snapshot).
  S026 drifted by 14 bytes at offsets 232727–232742, all inside the Blogger `dynamicviews`
  asset id (`fa12fcebe36ff135` → `2abac2b3aa987931`); the amendment-2 extracted text is
  identical between the round-45 snapshot and live (26246 chars, quote at the same offset).
  The entry's 2026-10-20 digest `ca1145fb…` (236385 B) and the round-45 `5d74dd1c…` are both
  stale as receipts, which is why the replacement source line carries the 2026-10-26 receipt.
- **Probe** (scratch clone, not the lane, not a verdict): staged my rows, both entry edits,
  both gate lines, the two snapshots+receipts under
  `.ufo/evidence/round-48/freshness/sources/`, and the wave-1 counter byte-exact at
  `.ufo/evidence/round-48/freshness/measure.py`; committed in the clone (`fc30ca1`) and ran
  `measure.py --lane <clone> --rev HEAD --no-live` and again live:
  `TARGET S026 row=S265 snapshot=ok receipt=ok quote=ok phrases=ok entries=ok live=skipped/ok REFRESHED`,
  the same for `S048 row=S266`, `self_pin=1`, `census_exit=0`. Only S093/S108 were `NOT`
  (other seats' deliverables), so the summary printed `refreshed=2` and exited 1 by design.

## Gates this draft clears (observed, not inferred)

- C2 per-target field chain through `entries` for both targets, and `live=ok` with the live
  check on.
- Census: `census_exit=0` on a tree containing both rows (no E01/E03/E04/E05–E11; the shared
  URL under a new scope can only raise the non-fatal W04).
- Amendment 1 URL set: each row's source cell carries the base URL, which is also the receipt
  URL; amendment 2 gate-line format and quote location; row selector (`id > 264`, teaches
  prefix with U+2014).

## Touched surfaces

- Written: `.ufo/waves/round-48/w1/T48ScribeRowsA.rows.md` (deliverable) and this report.
- Not written: `corpus/SOURCES.md`, `corpus/knowledge/*`, `corpus/lessons/round-48.md`,
  `.ufo/evidence/round-48/**`, any counter, any Git/jj state in the lane. All staging happened
  in one shared clone under `/fast/scratch/hyaku/tameshi-r48/T48ScribeRowsA/`, removed at the
  end.

## Findings for the L1

- **F1** S026 page chrome churns while content is stable; the anchor digest must be the live
  snapshot's, and if the L1's committed copy differs, substitute its first 12 hex for
  `a4c5c46b4af9` (placeholder `@SHA:S026@` is in the deliverable). The `--live` check compares
  the quote, not the digest.
- **F2** Pre-existing non-verbatim bracket in `repeated-control-precondition.md`: it writes
  `report[s] a failure`, the page reads `causing it to report a failure`. Claim holds; outside
  my two-line edit scope, so reported rather than silently changed.
- **F3** `corpus/knowledge/fleet-kill-rate-ledger.md:374` says `source method: S003 and S048`,
  but that file is not in S048's base used-by cell; C2 does not require re-pointing it and R's
  used-by cell must not list it (the counter compares the set exactly). Optional follow-up.
- **F4** The PIT page carries no in-body version/date; the anchor keeps `page version unstated`
  with the server's `Last-Modified: 2026-06-03` and the unchanged digest as revision evidence.
- **L1 mechanics**: commit exactly one snapshot per target under
  `.ufo/evidence/round-48/freshness/sources/` besides `<T>.receipt.json` (a headers file there
  would read `snapshot=ambiguous`), insert the rows after S264 at `corpus/SOURCES.md:139`, and
  paste the gate lines plus prose into `## Gate`.

## Out of scope / not done

- S093 and S108 (other seats, ids S267/S268), C1, control scoring, deciding runs, census-run
  outside the counter's own call.
- No tool install or upgrade (curl 8.23.0, python3, gzip already present; no pacman call).

## Provenance

Base `473336d9d789f6081195e7376d17836a24666bc3`; wave-1 snapshots
`.ufo/waves/round-48/w1/sources/{S026,S048}.{html,receipt.json}`; round-45 snapshots for the
drift comparison; counter `.ufo/waves/round-48/w1/T48ExecC2Counter.measure.py` (probe copy).
Scratch `/fast/scratch/hyaku/tameshi-r48/T48ScribeRowsA/` deleted; no scratch tree left.
