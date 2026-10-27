# T51W2Read11 — cold-read re-key reader, `## The operator's runbook and the six-leg regression (round 10, measured)`

Seat T51W2Read11 (reader, round-51 wave 2). Candidate `6d8c11e378aa90b12650808e1b79270742935f15`, base
`9962033fd7a75aa2f2847e979dd687a5d28505a1`. Method: re-resolved the heading at CAND, read the whole section
through the next heading, then read every cited surface against candidate bytes (`git show CAND:<path>` for
lane files; `git -C <sibling> show/ls-tree` for the six leg targets; a `--shared` scratch clone detached at
the section's governed tool revision for the one executable claim). The fixture list and old READERS_JSON
were not used to enumerate pointers — every pointer below was taken from the section text itself. Read-only
everywhere except this report; scratch deleted before yield; no tools installed; no git/jj mutations.

## Section resolution at CAND

- Heading `## The operator's runbook and the six-leg regression (round 10, measured)` re-resolved at
  **SKILL.md:1272**; span **1272–1364**; next heading `## Final pointers — the standing map at the arc's
  close (round 11, measured)` at **:1365**. Same start line at base (1272).
- Section sha256 at CAND `6effbc3cfbca8180dc5b745fff92e0e4c6dc2c0c513334337fa5bb4f4f271667`;
  **byte-identical base→CAND** (`diff` of the 93 extracted lines at both revs: empty). The SKILL.md diff
  base→CAND touches only the appended round-51 registry block, so this section's monitor drop
  (`input-drift:tools/mutate-and-run.sh`) is caused purely by the runner's bytes changing (+126/−47,
  tenth leg + TMPDIR honoring), not by any edit to the section.

Two sha identities in the section are **content sha256 pins, not git objects** — both recovered from lane
history and verified:

- `75ed934d…` = `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` = sha256 of
  `tools/mutate-and-run.sh` at lane commit `606716f7` ("probation round 10", committed 2026-10-14
  18:28:23 -03 = 21:28:23Z). 1 642 L there (section says "1 642 L" ✓); `VERSION=` at :157 there is
  exactly `mutate-and-run.sh r10-2 (tameshi-shokunin, 2026-10-14)` ✓; "uncommitted worktree file at this
  write" is coherent (commit lands ~26 min after the section's 21:02:39Z receipt).
- `cf41efaa…` = `cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75` = sha256 of the runner
  at `9f1d3c33` ("probation round 7"), matching the runbook's own cells (:22, :95: "r7-1, 1341 L / 61 632 B")
  and the ledger's ER-2 (:281).
- `e1e349b6…` = `e1e349b69d798acb…` = sha256 of `corpus/knowledge/operator-runbook.md` at `606716f7`,
  exactly **511 L / 31 416 B** there — the section's "`e1e349b6…` / 511 L / 31 416 B" verifies digit-for-digit.

## Pointers (every cited surface, checked against candidate bytes; governed anchors also checked at their pinned bytes)

| ord | raw text (as cited) | resolves to | verdict | located excerpt / evidence |
|---|---|---|---|---|
| 0 | `` `:1226-1228` `` (SKILL.md self; cited in the intro and again in the supersessions bullet) | SKILL.md :1226-1228 | **holds** | :1226-1228 = "…re-verified at this boundary, since all four legs matched while cases 3–4 read `stale`. Cases 5–6 are still not embedded: their rows carry no `REGRESSION` line — named debt, not smoothed (`fleet-kill-rate-ledger.md:282`)." — exactly the round-9 caveat the intro quotes. Early SKILL.md unchanged base→CAND. |
| 1 | `` `corpus/knowledge/operator-runbook.md` `` (`e1e349b6…` / 511 L / 31 416 B, "uncommitted worktree file at this read; the sha governs") | corpus/knowledge/operator-runbook.md | **holds as a governed record; identity stale at CAND (expected)** | e1e349b69d798acb… = the runbook blob at 606716f7, 511 L / 31 416 B exactly. At CAND the file is committed and larger: 516 L / 33 515 B, sha256 `8b2e185ff011f6cf…` — byte-identical base→CAND; it grew at `2a22adeb` (r17 ER-R3 substitutions) and `58e5d53d` (r18 ER-jj2 append) per its own errata. §-map claim holds at CAND: §0 :35, §1 :65, §2 :93, §3 :131, §4 :180, §5 :243, §6 :269, §7 :345, §8 :408, §9 :438, §10 :462, `## Errata (append-only)` :481 — all ten sections + append-only errata present as mapped. ER-R1 (:486) and ER-R2 (:504-512) exist and ER-R2 names the remedy: "The remedy is unchanged: the T2 step, once the edit lands" (:509-510). |
| 2 | `` `service-limits.md` (`:1250-1254`) `` | SKILL.md :1250-1254 (+ the file) | **holds** | :1250-1254 = "…The standalone note `corpus/knowledge/service-limits.md` (T9-2, this round) carries the same rows as the detail of record … this page is the compact rendering, and a divergence between the two is the finding, never smoothed." — exactly the rendering/divergence rule the section appeals to. `corpus/knowledge/service-limits.md` exists at CAND. |
| 3 | `` `cf41efaa…` (r7-1, four legs) `` | runner blob sha256 at 9f1d3c33 | **holds as a governed record** | Full value cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75, recomputed from lane history (runner blob at 9f1d3c33 and b8eb96e); corroborated by runbook :22/:95 and ledger :281 (same value, "1 341 L / 61 632 B"). |
| 4 | `` `75ed934d…` (`VERSION` = `mutate-and-run.sh r10-2`, 1 642 L; uncommitted worktree file at this write) `` | runner blob sha256 at 606716f7 | **holds as a governed record; identity triple stale at CAND** | Full value 75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5, recomputed; 1 642 L and the r10-2 VERSION line verified at those bytes. At CAND the runner is 2 159 L, sha256 `977de47034cbe52b…`, while the `VERSION` string is **unchanged** (:185) — see finding F3: VERSION no longer discriminates the pinned tool. |
| 5 | list `tools/mutate-and-run.sh:85-89` | tools/mutate-and-run.sh :85-89 | **off-by-one at its own governed sha; absent at range at CAND** | At 75ed934d (606716f7) the six leg entries sit at **:84-89** (js-kimi-census :84 … js-claims-check :89; caption :80-83) — the cited range covers legs 2–6 and **misses leg 1**. At CAND :85-89 = caption lines + the first two entries; the ten-entry list now lives at :88-97 (six-leg content :88-93). Finding F1. |
| 6 | sources `:90-97` | tools/mutate-and-run.sh :90-97 | **holds at governed sha; moved at CAND** | At 75ed934d: :90 = `# Sources: corpus/knowledge/mutation-case-kimi-census.md §1,` … :97 = "…against the pinned blobs at r10-2)." — exact. At CAND the block moved to :98-104 (provenance lines through :113, "All ten defect specs…" :114). |
| 7 | pins/tables `:550-559` | tools/mutate-and-run.sh :550-559 | **holds at governed sha for the two new pins + all six tables; partial as "pins/tables"; moved at CAND** | At 75ed934d: :550-553 = PIN_CHECKLIST/REV_CHECKLIST/PIN_CLAIMS/REV_CLAIMS; :554-559 = TABLE_JS…TABLE_CLAIMS (all six). The four base pin pairs sit just above (:542-549, PIN_JS…REV_MADO). At CAND: pins :614-633 (ten pairs), tables :634-643 (ten). |
| 8 | specs `:766`, `:841` | tools/mutate-and-run.sh :766 / :841 | **holds at governed sha; moved at CAND** | At 75ed934d: :766 = "# r10-2 leg 5: kagi corpus/checklist-run.sh @ fecee874 (pin 7e5ec98b…)" (heredoc :770); :841 = "# r10-2 leg 6: kumitate scripts/claims-check.mjs @ 175de6b (pin e9a21b44…)" (heredoc :845). At CAND the same comments are at :850 and :925. |
| 9 | registry `:1132-1141` | tools/mutate-and-run.sh :1132-1141 | **holds at governed sha as the two r10-2 leg registrations; moved at CAND** | At 75ed934d: :1132-1136 = `regression_case_git bash-checklist-run …`, :1137-1141 = `regression_case_git js-claims-check … st_claims=$?` — exactly the legs r10-2 embedded (the full six-leg registry spans :1112-1141). At CAND: checklist :1479, claims :1484, drift-pins :1506 (ten-leg registry :1459-1506). |
| 10 | exit map `tools/mutate-and-run.sh:115-119` | tools/mutate-and-run.sh :115-119 | **holds at governed sha; moved at CAND** | At 75ed934d: :115-117 = "Exit map (--regression): 0 all cases PASS · 1 >= 1 case FAIL … · 2 a case could not be verified — missing repo/rev/blob, pin mismatch, sweep setup refusal — with no FAIL." + :118-119 the receipt-line names — the map is exactly there. At CAND it is at :139-143. |
| 11 | mode mirror `:104-106` and `:932-960` | tools/mutate-and-run.sh | **holds at governed sha (both verbatim-located); moved at CAND** | At 75ed934d: :104-106 = "# r10-2 mirrors the blob's mode too (`git show` writes bytes, not modes): … so 100755 blobs are chmod +x'd after materialization."; :932-960 = the materialization body (dst :932, `git show` :933, r10-2 mode comment :938-941, `ls-tree` mode read :942, `REGRESSION_PIN … mode= … sha256=` printf :959-960). At CAND: comment :128-130, body ~:1276-1314 (printf :1302). |
| 12 | added selftest arms `:1488-1527` | tools/mutate-and-run.sh :1488-1527 | **holds at governed sha; moved at CAND** | At 75ed934d: :1488 = "# r10-2 (TAMESHI-T10-2) exec-bit mirror: …" block; :1523-1527 = "ledger leg: exec bit mirrored (self-exec gate runs)" / "exec-bit leg pin line carries mode=100755" / "exec-bit leg PASSes at the exact tolerance". At CAND the corresponding arms sit at :1885-1918 (`mode=100755` :1893, `mode=100644` :1917). |
| 13 | command line + default scratch "`mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`, removed on PASS unless `--keep`, kept on FAIL/SETUP, never removed when `--workdir` was given"; exit map "0/1/2 (`:115-119`)" | tools/mutate-and-run.sh | **held at governed sha (code :1089); superseded at CAND by the TMPDIR change** | At 75ed934d the regression root is literally `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX` (:1089). At CAND it is `mktemp -d "${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX"` (:149 comment "(r51 honours TMPDIR)"; code :1432; likewise run :157/:491 and selftest :160/:1555). The keep/remove semantics are unchanged at CAND (:149-152). Finding F2. |
| 14 | six-leg table (leg/target/recorded rev/rate × 6) | owner repos + runner pins | **holds; all six pins verified against live sibling bytes** | Rates match the embedded tables exactly (TABLE_JS 8 KILLED, TABLE_BASH 8, TABLE_TSUKUROI 6, TABLE_MADO 4, TABLE_CHECKLIST 7 of 15, TABLE_CLAIMS 7; identical strings at governed :554-559 and CAND :634-639). Revs resolve and blob sha256s match the embedded pins, measured now: kumitate `scripts/kimi-census.mjs@175de6ba2e9e…` → `83016d45049b009a…` = PIN_JS (:542), mode 100644; kagi `corpus/surface-census.sh@fecee8743e52…` → `275d8294a94e9eb7…` = PIN_BASH (:544), 100755; tsukuroi `tools/tsukuroi-census.sh@165307fe4746…` → `084951be50bcbfee…` = PIN_TSUKUROI (:546), 100755; mado `tools/mado-verify.sh@eead56b20ad2…` → `d7edaab4bf108625…` = PIN_MADO (:548), 100755; kagi `corpus/checklist-run.sh@fecee8743e52…` → `7e5ec98b9e1d0afa…` = PIN_CHECKLIST (:550), 100755; kumitate `scripts/claims-check.mjs@175de6ba2e9e…` → `e9a21b441f1216bf…` = PIN_CLAIMS (:552), 100755. Modes are consistent with the mirror rationale (checklist is the 100755 re-exec case; kimi is 100644 and is run via `node`, not exec'd). |
| 15 | receipt: "`--selftest` → `MUTATE_SELFTEST: 80/80 pass` / `VERDICT: PASS`, rc 0 — added arms include the exec-bit mirror and an embedded-ledger check" | executable claim at 75ed934d | **verified by execution** | Ran `bash tools/mutate-and-run.sh --selftest` in a `--shared` scratch clone detached at 606716f7 (toplevel asserted; outputs to my scratch): `MUTATE_SELFTEST: 80/80 pass` / `VERDICT: PASS`, rc 0 — exact match with the receipt. |
| 16 | receipt: "`--regression` → six legs, all exact: `match=10/10` (legs 1–4, 6), `match=15/15` (leg 5) … `REGRESSION: PASS (cases=6 passed=6; ledger legs exact: killed-delta<=0 flips<=0)`, rc 0"; "Each `REGRESSION_PIN` line now carries the blob's `mode=`"; "`REGRESSION_EXPECT` lists six recorded rates" | record + format anchors | **record stands; format anchors verified in code; shape superseded at CAND** | Format: `REGRESSION_EXPECT` printf at governed :1103 lists exactly six rates; `REGRESSION_PIN` printf carries `mode=` at governed :959; closing PASS format identical at CAND :1540. The 21:02:39Z six-leg receipt itself is a record (not re-run — the full replay sweeps four sibling repos; wave 1 already reproduced the registered suite). At CAND the shape is ten legs: `REGRESSION_EXPECT` lists ten (:1446), the selftest tally arm expects `cases=10 passed=10` (:2087-2088). |
| 17 | "the owner's own run at the same revision, 21:00:24Z, closes identically" | record | **record (untraceable); corroborated only in part** | No lane-held receipt names 21:00:24Z; the runbook's ER-R2 (:504) independently records owner-side tool motion "appended 2026-10-14 ~21:00Z". Kept as a record claim; not falsified, not verifiable from lane bytes. |
| 18 | "The round-7 section's 'Four legs at this revision' (`:925-929`; dated there since round 16)" | SKILL.md :925-929 | **holds** | :925 = "pinned original revision. Four legs at that revision (r7-1; seven since round 16; eight since round 18; nine since round 26)" — the dated text the section describes is exactly there; :929 anchors `tools/mutate-and-run.sh@9f1d3c3:72-109`. Info note F4: the dating still stops at "nine since round 26" at CAND while the runner wires ten. |
| 19 | "the round-9 receipt's `cases=4` (`:1218-1222`)" | SKILL.md :1218-1222 | **holds** | :1218 = "`--selftest` → `MUTATE_SELFTEST: 67/67 pass` / `VERDICT: PASS`, rc 0."; :1219-1221 = "4 legs … `REGRESSION: PASS (cases=4 passed=4; …)`, rc 0, tool `cf41efaa…`". |
| 20 | "Reading a receipt stays the round-7 discipline (`:965-1008`)" | SKILL.md :965-1008 | **holds** | `### Reading a receipt — the discipline` at :965; items 1–7 (read the block / PASS exact / FAIL names rows / SETUP not a verdict / instrument-not-gates / attestation / selftest arms) run through :1008. |
| 21 | "`fleet-kill-rate-ledger.md:85-88`" ("cases 1 and 2 only") | corpus/knowledge/fleet-kill-rate-ledger.md :85-88 | **holds** | :85-88 = "Embedding status (O, §5): the harness's `--regression` currently embeds **cases 1 and 2 only** (`PIN_JS`/`PIN_BASH`, `tools/mutate-and-run.sh:482-483`); cases 3 and 4 are not embedded at this write…". Ledger byte-identical base→CAND (the corpus/knowledge diff adds only `mutation-case-kagi-drift-pins.md`, +222). |
| 22 | "superseded in the ledger by ER-2 (`:281`, four legs)" | corpus/knowledge/fleet-kill-rate-ledger.md :281 | **holds** | :281 = "**§5 / ER-1 supersession (embedding + tool).** … the harness at `cf41efaa8be5f52d…` (r7-1; 1 341 L / 61 632 B) carries **four** materialized legs and passes them at the exact band — `REGRESSION: PASS (cases=4 passed=4; …)`…". |
| 23 | "the recorded T8-1/T8-2 spec files (their 25 `@old` strings re-verified `count==1`)" | embedded specs | **holds at CAND** | Counted at CAND bytes: `bash-checklist-run.spec` 15 `@old` + `js-claims-check.spec` 10 `@old` = **25**. The runner's own provenance comment states the same at CAND (:114-115 region, "legs 5–6 are the recorded T8-1/T8-2 spec files, their 25 @old strings…"). |
| 24 | receipt scratch "`/tmp/w10-t10-4-ev/` (regression workdir kept)" | /tmp/w10-t10-4-ev | **absent (ephemeral, expected)** | Path does not exist on this host; 2026-10-14 scratch. Known ephemeral-evidence class. |
| 25 | tags T10-1/T10-2, T8-1/T8-2, ER-4 caveat (a) | plans/round-10.plan.md; runner provenance comments | **tag surfaces present** | `plans/round-10.plan.md` exists at CAND; TAMESHI-T10-2 provenance comments in the runner (governed :12, :766, :841, :1488; CAND :2, :12, :850, :925). ER-4 caveat (a) lives in the ledger (record, unchanged base→CAND). |
| 26 | (the four panel-tool updates) | tally-audit.py / tally-audit-v2.py / tally-audit-v3.py / mte-interop.py | **not cited by this section** | The section contains no pointer to any panel tool; their updates touch it only via the shared `input-drift:tools/mutate-and-run.sh` drop (the runner bytes), same as every other re-keyed section. |
| 27 | `VERSION` = `mutate-and-run.sh r10-2` | tools/mutate-and-run.sh :185 at CAND | **holds as text, no longer discriminating (F3)** | The CAND runner still carries `VERSION='mutate-and-run.sh r10-2 (tameshi-shokunin, 2026-10-14)'` (:185) while embedding ten legs (2 159 L, sha `977de470…`). The runbook's own ER-R2 recorded the same phenomenon for the r10-2 drafts ("VERSION line still r10-2" at 1 547 L), so the tool has a habit of lagging its VERSION string. |

## Claims made false by this round's changes (the falsifiers named in the seat spec)

- **F1 (anchor precision, present at write time): `list :85-89` misses leg 1 at its own governed sha.**
  At `75ed934d…` (606716f7) the six entries are at :84-89; the cited range covers legs 2–6 only. Not caused
  by r51 — the section bytes are identical base→CAND and the anchor was already one line short at its pinned
  revision. Its sibling anchors are exact at the governed sha (sources :90-97, exit map :115-119, mirror
  :104-106/:932-960, arms :1488-1527, specs :766/:841) or exact-for-intent (registry :1132-1141 = the two
  r10-2 registrations; pins/tables :550-559 = the two new pins + all six tables, with the four base pin
  pairs at :542-549). At CAND every runner anchor has moved (new locations in the table).
- **F2 (made false by the round's TMPDIR change): the default scratch is no longer `/tmp/…`.** The section
  states the regression scratch as `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`. True at `75ed934d…`
  (code :1089); at CAND the runner honours TMPDIR — `${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX`
  (:149 "(r51 honours TMPDIR)", :1432), likewise the run workdir (:157/:491) and selftest scratch
  (:160/:1555). Behavior verified incidentally: my run of the r10-2 selftest wrote its scratch under the
  then-literal `/tmp` and cleaned it up on PASS; the CAND runner honors TMPDIR (wave evidence and Read10's
  fail-closed nonexistent-TMPDIR probe).
- **F3 (made false by the tenth leg): "replays **six** embedded legs" and the six-shaped receipt lines are
  superseded at CAND.** The CAND runner wires ten legs (header :84 "(… r26 nine; r51 ten)"; entries :88-97;
  usage :223-226; pins :614-633; tables :634-643; registry calls :1459-1506; `REGRESSION_EXPECT` ten rates
  :1446; selftest tally arms `cases=10` :2087-2117). The section's "six" statements remain true only as
  records of `75ed934d…` — which is how the section scopes them ("line anchors as read at `75ed934d…`, the
  sha governs"), so this is currency, not error; the re-key row carries the new locations. Related: the
  CAND `VERSION` string still reads r10-2, so the section's identification pattern (sha + VERSION + length)
  now resolves ambiguously by VERSION alone (F3's second half).
- **F4 (adjacent, not this section's text): the round-7 dating the section relies on now lags one leg.**
  SKILL.md:925 still reads "nine since round 26" at CAND while the runner wires ten; the registry owner may
  append "ten since round 51" there, exactly as rounds 16/18/26 did. No action for this seat.

## Strongest falsifier checked

Executed the section's only executable claim at the exact pinned bytes: `bash tools/mutate-and-run.sh
--selftest` in a `git clone --shared` scratch clone detached at `606716f7` (whose runner blob hashes to
`75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`; `git rev-parse --show-toplevel`
asserted; TMPDIR under scratch; outputs to my scratch) → **`MUTATE_SELFTEST: 80/80 pass` / `VERDICT:
PASS`, rc 0** — the receipt's central claim verifies character-for-character at the revision it names.
The full six-leg `--regression` was deliberately **not** re-run (it sweeps four sibling repos for ~an
hour; the receipt is a record whose format anchors I verified in code, and wave 1 already reproduced the
registered suite). Secondary falsifier: a byte-level anchor audit at both the governed sha and CAND,
which exposed the off-by-one list anchor (F1), the TMPDIR supersession (F2), the six→ten supersession
(F3), and verified all six leg pins/modes/revs against live sibling bytes (table row 14).

## Findings by severity

- **Minor (anchor precision, pre-existing): `list tools/mutate-and-run.sh:85-89` is one line short at its
  own governed sha** — the six-entry list sits at :84-89 there; js-kimi-census (:84) is outside the cited
  range. Every other governed anchor in the section located exactly. The re-key row carries the precise
  governed and CAND locations for all runner anchors.
- **Currency (made stale by this round, correctly scoped by the section's own "the sha governs" rule):**
  six→ten legs, `/tmp`→TMPDIR scratch, receipt shape (six legs / six `REGRESSION_EXPECT` rates / 80-case
  selftest at the pinned bytes vs ten legs / ten rates / 107-case selftest at CAND — Read10 measured the
  CAND selftest at 107/107 and base at 106/106), and the identity triple (sha/VERSION/length) of which
  only the sha still discriminates at CAND.
- **Info: ephemeral and owner-side records** — `/tmp/w10-t10-4-ev/` (and the runner's cited
  `/tmp/w8-*` spec sources) are absent; the owner's 21:00:24Z run has no lane-held receipt (ER-R2's
  ~21:00Z timestamp is the only corroboration). Both are record-class, not falsifiable from lane bytes.
- **No wrong expectation found**: every checkable recorded value (80/80 at the pinned bytes, the six
  rates 8/8/6/4/7-of-15/7, the six pins against live sibling blobs, all six revs, the exit map, the
  `mode=` pin-line format, `REGRESSION_EXPECT`'s six-rate shape at the pinned bytes, the 25 `@old`
  strings, the ledger's :85-88 and :281 texts, the runbook's 511 L / 31 416 B at `e1e349b6…`) matches the
  bytes exactly. The section survives falsification as a sha-governed record with two currency notes and
  one off-by-one anchor.

## reads.json row

```json
{
  "seat": "T51W2Read11",
  "heading": "## The operator's runbook and the six-leg regression (round 10, measured)",
  "candidate": "6d8c11e378aa90b12650808e1b79270742935f15",
  "base": "9962033fd7a75aa2f2847e979dd687a5d28505a1",
  "skill_md_span_at_cand": [1272, 1364],
  "next_heading_at_cand": "## Final pointers — the standing map at the arc's close (round 11, measured) (SKILL.md:1365)",
  "section_sha256_at_cand": "6effbc3cfbca8180dc5b745fff92e0e4c6dc2c0c513334337fa5bb4f4f271667",
  "section_bytes_unchanged_base_to_cand": true,
  "monitor_drop_reason": "input-drift:tools/mutate-and-run.sh (section bytes identical; runner changed +126/-47: tenth leg + TMPDIR honoring)",
  "governed_identities": {
    "tool_75ed934d": "75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5 = runner blob sha256 at 606716f7 (1 642 L; VERSION r10-2)",
    "tool_cf41efaa": "cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75 = runner blob sha256 at 9f1d3c33 (r7-1, 1 341 L)",
    "runbook_e1e349b6": "e1e349b69d798acb… = operator-runbook.md blob sha256 at 606716f7 (511 L / 31 416 B, exact)",
    "note": "these are content sha256 pins ('the sha governs'), not git objects; recovered from lane history"
  },
  "pointers": [
    {"ordinal": 0, "raw": ":1226-1228", "file": "SKILL.md", "ranges": [[1226, 1228]], "verdict": "holds", "located_excerpt": "'Cases 5–6 are still not embedded: their rows carry no REGRESSION line — named debt, not smoothed (fleet-kill-rate-ledger.md:282).' — the round-9 caveat quoted by the intro."},
    {"ordinal": 1, "raw": "corpus/knowledge/operator-runbook.md (e1e349b6… / 511 L / 31 416 B, uncommitted worktree file at this read; the sha governs)", "file": "corpus/knowledge/operator-runbook.md", "ranges": null, "verdict": "holds as governed record; identity stale at CAND", "located_excerpt": "e1e349b69d798acb… verified = blob at 606716f7, 511 L / 31 416 B exact; at CAND 516 L / 33 515 B / 8b2e185f… (committed; grew at 2a22adeb r17 and 58e5d53d r18; byte-identical base→CAND). §0-§10 + append-only errata all present as mapped (:35/:65/:93/:131/:180/:243/:269/:345/:408/:438/:462/:481); ER-R1 :486, ER-R2 :504-512 names the T2 remedy (:509-510)."},
    {"ordinal": 2, "raw": "service-limits.md (:1250-1254)", "file": "SKILL.md :1250-1254 (+ corpus/knowledge/service-limits.md)", "ranges": [[1250, 1254]], "verdict": "holds", "located_excerpt": ":1250-1254 = the compact-rendering/divergence-is-the-finding rule naming service-limits.md; file exists at CAND."},
    {"ordinal": 3, "raw": "cf41efaa… (r7-1, four legs)", "file": "tools/mutate-and-run.sh (blob sha256)", "ranges": null, "verdict": "holds as a record", "located_excerpt": "cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75 = runner blob at 9f1d3c33; corroborated by runbook :22/:95 and ledger :281."},
    {"ordinal": 4, "raw": "75ed934d… (VERSION = mutate-and-run.sh r10-2, 1 642 L; uncommitted worktree file at this write)", "file": "tools/mutate-and-run.sh (blob sha256)", "ranges": null, "verdict": "holds as governed record; identity triple stale at CAND", "located_excerpt": "75ed934dc863… = runner blob at 606716f7 (committed 21:28:23Z, ~26 min after the 21:02:39Z receipt); 1 642 L and the r10-2 VERSION line verified there. At CAND: 2 159 L, sha 977de470…, VERSION string unchanged (:185) — no longer discriminates."},
    {"ordinal": 5, "raw": "list tools/mutate-and-run.sh:85-89", "file": "tools/mutate-and-run.sh", "ranges": [[85, 89]], "verdict": "off-by-one at its own governed sha; absent at range at CAND", "located_excerpt": "At 75ed934d the six entries sit at :84-89 (js-kimi-census at :84; caption :80-83) — the range covers legs 2-6 and misses leg 1. At CAND :85-89 = caption + first two entries; the ten-entry list is :88-97 (six-leg content :88-93)."},
    {"ordinal": 6, "raw": "sources :90-97", "file": "tools/mutate-and-run.sh", "ranges": [[90, 97]], "verdict": "holds at governed sha; moved at CAND", "located_excerpt": "At 75ed934d :90 = '# Sources: …' through :97 '…against the pinned blobs at r10-2).' — exact. At CAND at :98-104 (provenance through :113)."},
    {"ordinal": 7, "raw": "pins/tables :550-559", "file": "tools/mutate-and-run.sh", "ranges": [[550, 559]], "verdict": "holds at governed sha for the two new pins + all six tables; partial for 'pins'; moved at CAND", "located_excerpt": "At 75ed934d :550-553 = PIN_CHECKLIST/REV_CHECKLIST/PIN_CLAIMS/REV_CLAIMS, :554-559 = TABLE_JS…TABLE_CLAIMS; the four base pin pairs sit at :542-549. At CAND pins :614-633, tables :634-643 (ten each)."},
    {"ordinal": 8, "raw": "specs :766, :841", "file": "tools/mutate-and-run.sh", "ranges": [[766, 766], [841, 841]], "verdict": "holds at governed sha; moved at CAND", "located_excerpt": "At 75ed934d :766 = '# r10-2 leg 5: kagi corpus/checklist-run.sh @ fecee874 (pin 7e5ec98b…)' (heredoc :770); :841 = '# r10-2 leg 6: kumitate scripts/claims-check.mjs @ 175de6b (pin e9a21b44…)' (heredoc :845). At CAND :850 and :925."},
    {"ordinal": 9, "raw": "registry :1132-1141", "file": "tools/mutate-and-run.sh", "ranges": [[1132, 1141]], "verdict": "holds at governed sha as the two r10-2 leg registrations; moved at CAND", "located_excerpt": "At 75ed934d :1132-1136 = regression_case_git bash-checklist-run…, :1137-1141 = js-claims-check… st_claims; full six-leg registry :1112-1141. At CAND checklist :1479, claims :1484, drift-pins :1506 (registry :1459-1506)."},
    {"ordinal": 10, "raw": "exit map :115-119", "file": "tools/mutate-and-run.sh", "ranges": [[115, 119]], "verdict": "holds at governed sha; moved at CAND", "located_excerpt": "At 75ed934d :115-117 = 'Exit map (--regression): 0 all cases PASS · 1 >= 1 case FAIL … 2 … cannot be verified … with no FAIL.' + :118-119 receipt-line names. At CAND at :139-143."},
    {"ordinal": 11, "raw": ":104-106 (mode mirror comment) and :932-960 (materialization/mirror code)", "file": "tools/mutate-and-run.sh", "ranges": [[104, 106], [932, 960]], "verdict": "holds at governed sha (both verbatim); moved at CAND", "located_excerpt": "At 75ed934d :104-106 = the r10-2 mode-mirror comment; :932-960 = dst/git-show/mode-read/REGRESSION_PIN printf with mode= (:959). At CAND comment :128-130, body ~:1276-1314 (printf :1302)."},
    {"ordinal": 12, "raw": "added selftest arms :1488-1527", "file": "tools/mutate-and-run.sh", "ranges": [[1488, 1527]], "verdict": "holds at governed sha; moved at CAND", "located_excerpt": "At 75ed934d :1488 = '# r10-2 (TAMESHI-T10-2) exec-bit mirror…' block ending :1527 ('exec-bit leg PASSes at the exact tolerance'). At CAND the arms sit at :1885-1918 (mode=100755 :1893, mode=100644 :1917)."},
    {"ordinal": 13, "raw": "--regression [--workdir DIR] [--keep]; default scratch mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX; exit map 0/1/2", "file": "tools/mutate-and-run.sh", "ranges": [[1089, 1089]], "verdict": "held at governed sha; superseded at CAND by the TMPDIR change", "located_excerpt": "At 75ed934d the root is literal /tmp/tameshi-r4-2-regression.XXXXXX (:1089). At CAND: mktemp -d \"${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX\" (:149 '(r51 honours TMPDIR)', code :1432; run :157/:491; selftest :160/:1555). Keep/remove semantics unchanged."},
    {"ordinal": 14, "raw": "six-leg table: js-kimi-census/kumitate scripts/kimi-census.mjs@175de6ba 8/10 · bash-surface-census/kagi corpus/surface-census.sh@fecee874 8/10 · bash-tsukuroi-census/tsukuroi tools/tsukuroi-census.sh@165307fe 6/10 · bash-mado-verify/mado tools/mado-verify.sh@eead56b2 4/10 · bash-checklist-run/kagi corpus/checklist-run.sh@fecee874 7/15 · js-claims-check/kumitate scripts/claims-check.mjs@175de6ba 7/10", "file": "owner repos + runner pins/tables", "ranges": [[542, 559]], "verdict": "holds; all six pins/revs/modes verified against live sibling bytes", "located_excerpt": "PIN_JS 83016d45…, PIN_BASH 275d8294…, PIN_TSUKUROI 084951be…, PIN_MADO d7edaab4…, PIN_CHECKLIST 7e5ec98b…, PIN_CLAIMS e9a21b44… all equal sha256 of the sibling blob at the recorded rev today; modes 100644 (kimi) / 100755 (other five), consistent with the exec-mirror rationale; rates equal the embedded TABLE_* strings (governed :554-559 = CAND :634-639)."},
    {"ordinal": 15, "raw": "--selftest → MUTATE_SELFTEST: 80/80 pass / VERDICT: PASS, rc 0", "file": "tools/mutate-and-run.sh @ 75ed934d", "ranges": null, "verdict": "verified by execution", "located_excerpt": "bash tools/mutate-and-run.sh --selftest in a --shared clone at 606716f7 (toplevel asserted) printed 'MUTATE_SELFTEST: 80/80 pass' / 'VERDICT: PASS', rc 0 — exact."},
    {"ordinal": 16, "raw": "--regression → six legs all exact, match=10/10 (1-4,6), match=15/15 (5), REGRESSION: PASS (cases=6 passed=6; …); REGRESSION_PIN carries mode=; REGRESSION_EXPECT lists six rates", "file": "tools/mutate-and-run.sh", "ranges": [[1103, 1103], [959, 960]], "verdict": "record stands; format anchors verified; shape superseded at CAND", "located_excerpt": "At 75ed934d: REGRESSION_EXPECT printf lists exactly six rates (:1103); REGRESSION_PIN printf carries mode= (:959). At CAND ten rates (:1446), selftest tally arms expect cases=10 (:2087). Full replay not re-run (four sibling repos; wave 1 reproduced the registered suite)."},
    {"ordinal": 17, "raw": "the owner's own run at the same revision, 21:00:24Z, closes identically", "file": null, "ranges": null, "verdict": "record, untraceable; partly corroborated", "located_excerpt": "No lane-held receipt names 21:00:24Z; runbook ER-R2 (:504) records owner-side motion 'appended 2026-10-14 ~21:00Z'."},
    {"ordinal": 18, "raw": ":925-929 (round-7 'Four legs at this revision', dated since round 16)", "file": "SKILL.md", "ranges": [[925, 929]], "verdict": "holds", "located_excerpt": ":925 = 'Four legs at that revision (r7-1; seven since round 16; eight since round 18; nine since round 26)'; :929 anchors tools/mutate-and-run.sh@9f1d3c3:72-109. Dating still stops at nine at CAND (info note)."},
    {"ordinal": 19, "raw": ":1218-1222 (round-9 receipt cases=4)", "file": "SKILL.md", "ranges": [[1218, 1222]], "verdict": "holds", "located_excerpt": ":1218 67/67 selftest; :1219-1221 4 legs, 'REGRESSION: PASS (cases=4 passed=4; …)', tool cf41efaa…"},
    {"ordinal": 20, "raw": ":965-1008 (reading-a-receipt discipline)", "file": "SKILL.md", "ranges": [[965, 1008]], "verdict": "holds", "located_excerpt": "'### Reading a receipt — the discipline' :965, items 1-7 through :1008."},
    {"ordinal": 21, "raw": "fleet-kill-rate-ledger.md:85-88 ('cases 1 and 2 only')", "file": "corpus/knowledge/fleet-kill-rate-ledger.md", "ranges": [[85, 88]], "verdict": "holds", "located_excerpt": ":85-88 = 'Embedding status (O, §5): … embeds **cases 1 and 2 only** …'. Ledger byte-identical base→CAND."},
    {"ordinal": 22, "raw": "ER-2 (:281, four legs)", "file": "corpus/knowledge/fleet-kill-rate-ledger.md", "ranges": [[281, 281]], "verdict": "holds", "located_excerpt": ":281 = '§5 / ER-1 supersession … the harness at cf41efaa8be5f52d… (r7-1; 1 341 L / 61 632 B) carries **four** materialized legs … REGRESSION: PASS (cases=4 passed=4; …)'."},
    {"ordinal": 23, "raw": "the recorded T8-1/T8-2 spec files (their 25 @old strings re-verified count==1)", "file": "tools/mutate-and-run.sh (embedded specs)", "ranges": null, "verdict": "holds at CAND", "located_excerpt": "bash-checklist-run.spec 15 @old + js-claims-check.spec 10 @old = 25, counted at CAND bytes; the runner's provenance comment states the same."},
    {"ordinal": 24, "raw": "/tmp/w10-t10-4-ev/ (regression workdir kept)", "file": null, "ranges": null, "verdict": "absent (ephemeral, expected)", "located_excerpt": "Path does not exist; 2026-10-14 scratch, known ephemeral class."},
    {"ordinal": 25, "raw": "T10-1/T10-2, T8-1/T8-2, ER-4 caveat (a)", "file": "plans/round-10.plan.md; runner provenance comments", "ranges": null, "verdict": "tag surfaces present", "located_excerpt": "plans/round-10.plan.md exists at CAND; TAMESHI-T10-2 comments at governed :12/:766/:841/:1488 (CAND :2/:12/:850/:925); ER-4 caveat (a) in the unchanged ledger."},
    {"ordinal": 26, "raw": "(four panel-tool updates: tally-audit.py, tally-audit-v2.py, tally-audit-v3.py, mte-interop.py)", "file": null, "ranges": null, "verdict": "not cited by this section", "located_excerpt": "No panel-tool pointer in the section; their only effect here is the shared input-drift drop via the runner bytes."},
    {"ordinal": 27, "raw": "VERSION = mutate-and-run.sh r10-2", "file": "tools/mutate-and-run.sh", "ranges": [[185, 185]], "verdict": "holds as text at CAND; no longer discriminates", "located_excerpt": "CAND :185 still 'mutate-and-run.sh r10-2 (tameshi-shokunin, 2026-10-14)' while the tool embeds ten legs (2 159 L, sha 977de470…); ER-R2 recorded the same lag for the r10-2 drafts."}
  ],
  "strongest_falsifier": "Executed the receipt's only executable claim at the exact pinned bytes: bash tools/mutate-and-run.sh --selftest in a --shared scratch clone detached at 606716f7 (runner blob sha256 = 75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5; rev-parse --show-toplevel asserted; TMPDIR under scratch) → MUTATE_SELFTEST: 80/80 pass / VERDICT: PASS, rc 0, matching the receipt exactly. Secondary: byte-level anchor audit at both the governed sha and CAND (found the off-by-one :85-89 list anchor, the TMPDIR supersession, the six→ten supersession) and verification of all six leg pins/modes/revs against live sibling blobs. The full six-leg --regression was not re-run (expensive sibling-repo sweep; wave 1 already reproduced the registered suite; format anchors verified in code).",
  "verdict": "record stands; re-keyable — every lane-file pointer resolves to real bytes at CAND, both sha identities and the runbook size triple verify exactly at their governed revisions, the receipt's selftest claim reproduces at the pinned bytes, and all six leg pins match live sibling bytes; residuals are one pre-existing off-by-one anchor (:85-89), the correctly-scoped currency notes (six→ten legs, /tmp→TMPDIR, identity triple), and the ephemeral/owner-side records",
  "seat_name": "T51W2Read11"
}
```

## Bounds and cleanup

Read-only on the lane and all sibling repos (every read via `git show`/`git ls-tree`, no working-tree
reads — the lane worktree is dirty at `f133b47f`); the only writes are this report. Scratch
`/fast/scratch/hyaku/tameshi-r51/T51W2Read11/` (one `--shared` clone, selftest output, tmp dir) deleted
before yield; the r10-2 selftest's `/tmp` scratch self-cleaned on PASS (verified: no
`/tmp/tameshi-r4-2-selftest.*` leftovers). No `/tmp` use beyond that absent-path check and the
self-cleaned selftest scratch (kilobytes). No tools installed; no git/jj mutations anywhere; no
`agent://all`.
