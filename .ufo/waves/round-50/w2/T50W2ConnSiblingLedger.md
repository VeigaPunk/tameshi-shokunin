# T50W2ConnSiblingLedger — sibling ledger patterns vs tameshi's routed-defect ledger

Seat: `T50W2ConnSiblingLedger` (connector, wave 2, round 50). Item: compare the candidate ledger
(`corpus/routed-defects.json`) and counter (`.ufo/evidence/round-50/c1/measure.py`) at
`80ea77e99e239982ab0b93e416645ef2359725d3` with the machine-checkable disposition records the wave-1
connector found in siblings (`w1/T50ConnSiblingDefects.md`: kagi closure-dispositions, kengaku
routed-findings.jsonl + recurrence_of, kotoba, kotodama; read-only under
`/home/vgpnk/Projects/shokunin`); name the one sibling design element that closes a forgery route the
wave-1 attacks found (`w1/T50CritC1Contract.md` F1-F2), with file:line; state what the tameshi ledger
must not absorb.

Method: read-only reads/greps of sibling lanes; one scratch clone (`git clone --shared`; toplevel
asserted before use) at the candidate revision for a counter probe. Counter runs here are probes
(`--explain` on a scratch clone), never verdicts; the deciding run is the L1's. All line numbers are
at the revision read today (2026-10-26). Receipts in `T50W2ConnSiblingLedger.receipts/`:
`c1-probe.stdout` (counter probe), `keymatch.probe.txt` (path-suffix key matches), `measure-sha.txt`
(freeze vs candidate counter sha).

## 1. What the candidate ships

- `corpus/routed-defects.json` at `80ea77e9`: 49 rows, one per frozen routed id (R40.1..R49.6),
  `31 fixed / 7 open / 11 declined`. Every row carries `evidence[{path, lines, excerpt}]`; fixed rows
  carry a full 40-hex `commit`; declined rows carry a ≥40-char `reason`; schema
  `tameshi-routed-defects-v1`.
- `.ufo/evidence/round-50/c1/measure.py` at `80ea77e9` is byte-identical to the freeze commit
  `cdbf24c0` (sha256 `ceee320c9ad8…` at both revisions; receipt `measure-sha.txt`). The counter is
  the frozen form-check: text-in-tree, commit-ancestry, ACK-word ban, floors (fixed≥20, declined≤12,
  ≥5 fixes after base).
- Probe (scratch clone at `80ea77e9`, `--explain`, exit 0):

  ```
  C1_R50: self=ceee320c9ad8 rev=80ea77e99e239982ab0b93e416645ef2359725d3 defects=49 rows=49
  fixed=31 open=7 declined=11 fixed_this_round=8 missing=0 extra=0 duplicate=0 spotcheck_changed=0
  defects_pin=0 bad_status=0 evidence_bad=0 key_miss=0 fixed_bad=0 open_unplanned=0 declined_bad=0
  fixed_short=0 declined_over=0 this_round_short=0 total=0 C1_R50_PASS=true
  ```

  No EXPLAIN lines: all 49 rows pass the frozen textual form-check at the candidate; 8 fixes are
  counted as landed after base.

## 2. Comparison with sibling machine-checkable disposition records

| Sibling record | What it supplies | What tameshi's ledger/counter has |
|---|---|---|
| kagi `corpus/closure-dispositions.py` + `.json` | source digest pinning (`.json:4`; `verify()` `:155-157`); KINDS vocabulary (`:62`); per-row `pointer` resolution with `POINTER-ID` for fixed rows (`resolve_pointer` `:106-129`, esp. `:128`); fixed-without-pointer rejected (`:191-193`) | counter pins defect-set digest (`defects_pin`) and spot-check digests (`spotcheck_changed`); no pointer field, no disposition vocabulary |
| kengaku `corpus/routed-findings.jsonl` | rows carry `id/class/source/opened_round/status/close/blocker/check` (`:1-16`); `check` = executable shell command re-verifying the row (R39-R1, `:1`); `plans/defect_ledger.py:111` binds named check functions (`CHECKS = {f.__name__: f …}`), e.g. `r34_d1` `:37-44` | no executable per-row verification; counter is purely textual (docstring: "What it cannot see: … semantic support") |
| kotoba `verifiers/check_r63_routed_repairs.py` | full counter over five routed corrections; pins `BASE_REV` (`:77-81`), proves append-only growth (`check_append_only` `:153`), non-hex-bounded token scan (`:178-181`) | no LOG-based scanning; tree-path evidence only |
| kotodama `reports/round-14/routed-resolution.json` | one `resolutions` entry per routed id with `evidence` + `control` (machine-checkable statement, e.g. R8-AUDCNT: "embedded bash control exit 0; harness 14/14 accepted, 12/12 rejected"; `all_routed_from` `:5`) | evidence array but no per-row control statement |

tameshi adopted the record *shape* (one row per routed id + status + evidence + fix pointer) from the
siblings, but none of their machine-executable grounding.

## 3. The one sibling design element closing F1/F2: kengaku's per-row executable `check`

Wave-1 attacks (both live at candidate — the counter bytes are the freeze bytes, §1):
- F1 (`T50CritC1Contract.md:12-30`): one post-freeze commit with arbitrary keyed text plus an
  all-fixed ledger passes the counter; freshness is automatic because the path did not exist at
  `routed_at`; the after-base floor is bypassable; `C1_R50_PASS=true` certifies textual novelty.
- F2 (`:32-43`): status is a free label; the same tree passes as mixed open/declined (`open` only
  needs the id in the newest Planned paragraph; `declined` only a ≥40-char reason).

**The one element:** kengaku's per-row executable `check` field — each ledger row carries a shell
command the ledger checker executes, so a disposition is grounded in a check outcome, not in
keyed prose:
- Schema: `kengaku-shokunin/corpus/routed-findings.jsonl:1` — R39-R1 carries
  `"check": "grep -q '^| \`order-check\`' SKILL.md && grep -q '^| \`round39-c1-audit\`' SKILL.md"`.
- Enforcement: `kengaku-shokunin/plans/defect_ledger.py:111` — `CHECKS = {f.__name__: f …}` binds
  named check functions run over rows (behaviour probes e.g. `r34_d1` at `:37-44`).

Closure mechanics:
- F1 closes: a `fixed` row would have to carry an executable check whose green proves the requested
  fix exists behaviorally. The F1 fabrication authored text and a ledger only ("<key> is fully
  delivered by the round-50 disposition service."); any honest check (probe the real artifact, run
  the tool) fails, so the fabricated row cannot be declared `fixed`. Passing requires the fix to
  actually exist.
- F2 closes: status couples to check outcome (fixed iff green; open iff red/unresolved; declined iff
  operator-owned/no check owed), so marking actually-fixed items open/declined becomes observable;
  the F2 reproduction (20 fixed/17 open/12 declined on an all-fixed tree) fails because the 17
  "open" rows' checks are green.
- Complement considered and rejected as the named element: kagi's pointer resolution
  (`closure-dispositions.py:106-129`) forces fixed rows to name a tree pointer containing the
  obligation id (`POINTER-ID`, `:128`) but executes nothing; a fabricator can point at the fabricated
  file. The executable check is the element that closes the demonstrated routes.

## 4. What the tameshi ledger must not absorb (verified against the candidate)

1. **Spot-check citations as evidence** — keep the hard ban (measure.py excludes them; no candidate
   row cites a spot-check).
2. **Extra statuses** — kagi `KINDS` (`reported/rejected/no-action/operator-owned`, `:62`),
   kengaku `blocked`, kotodama `applied-with-control/resolved-by-documentation`; keep exactly
   `fixed/open/declined` (STATUSES in measure.py).
3. **Free-text `close` fields** (kengaku prose) — would reintroduce F2; keep keyed excerpt + full
   commit.
4. **Bare report/wave paths as evidence without key suffix** — counter soft-excludes
   `.ufo/waves/`/`.ufo/reports/` unless the path ends with a key (measure.py). Calibration note: the
   path-suffix rule itself is the weak form of F3 (`T50CritC1Contract.md:56-57`), and the candidate
   ledger already exercises it: R44.2 keys only by suffix `w1/summary.md`, and fixed rows R43.2/
   R49.1 pass keying by path suffix with zero key text in excerpts (receipt `keymatch.probe.txt`).
   Do not absorb unkeyed report pointers; if checks (§3) are added, key-suffix matches should not by
   themselves satisfy a fixed row.
5. **Log-scanning** (kotoba append-only `LOG.md` suffix technique) — keep tree-path evidence.
6. **Claim-ledgers** (kagi TSV, kama registry) — command/expect records, not dispositions; do not
   entangle.
7. **`recurrence_of` as a status/evidence dimension** — it is provenance, not a disposition; the
   frozen surface has no rule for it (it may be added later as an optional field only).

Additional calibration observation: fixed rows citing files created this round (e.g. R40.2/R40.3/
R45.2/R46.4/R47.2 cite `.ufo/evidence/round-50/routed/receipts/MANIFEST.md` or
`corpus/lessons/round-50.md`) ride the same "path absent at routed_at ⇒ fresh" mechanism F1 abuses;
the counter cannot tell the genuine from the forged without executable checks.

## Commands (probes; receipts above)

- `git -C <lane> show 80ea77e9:corpus/routed-defects.json` — ledger rows.
- `git -C <lane> show 80ea77e9:.ufo/evidence/round-50/c1/measure.py | sha256sum` — `ceee320c9ad8…`
  (same as freeze; receipt).
- `python3 $S/lane/.ufo/evidence/round-50/c1/measure.py --lane $S/lane --rev 80ea77e9 --explain`
  → PASS, total=0 (receipt `c1-probe.stdout`).
- `python3` key-match over ledger evidence vs frozen keys → suffix-only rows (receipt
  `keymatch.probe.txt`).

## Summary

- Candidate ships a 49-row ledger (31 fixed / 7 open / 11 declined) and the byte-identical frozen
  counter; probe: `C1_R50_PASS=true`, total=0, fixes after base=8.
- Counter self `ceee320c9ad8` identical at freeze and candidate ⇒ wave-1 F1/F2 forgery routes remain
  open.
- Sibling comparison: tameshi adopted the record shape, none of the machine-executable grounding.
- One element that closes F1/F2: kengaku's per-row executable `check` (routed-findings.jsonl:1;
  defect_ledger.py:111).
- Must not absorb: spot-check evidence, extra statuses, free-text close, unkeyed report paths, LOG
  scanning, claim ledgers, recurrence_of-as-status.
- Calibration note: path-suffix-only keying already passes R43.2/R49.1 (fixed) and R44.2, and
  new-file freshness carries several fixed rows — the same mechanisms F1 abuses.
