# tameshi round 63 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

Lane repo: `C:/Users/jpvei/.zcode/workspace/95b1ba4d-5089-47a4-9fd8-54adebbce2ae/fleet/tameshi-shokunin`
(branch `master`). Base `0b81e8f575627d8de2e3a9cf598d5360c42bfeb6` → tip
`e9673d2ddfa3e2b445d93c21f20c4b34dc55ab07`. All commands below were run by this
verifier at closure time (2026-11-01); all measurements are on committed bytes via
index-free git plumbing, per the host note (no `git status`, no mutating commands).
Verdict: **admitted** — both claims re-measured green by this verifier, no owned
axis harmed. Two status-neutral observations for next round (bottom).

## 1. Step-1 conformance — all pass

| Check | Command | Observed |
|---|---|---|
| Report committed by lane identity | `git -C <fleet-root> log --format='%an %ae %H' -1 -- .ufo/reports/round-63/tameshi.md` | `tameshi-shokunin tameshi@shokunin.local 674b6b7d1f4435148313548b30d03d652160776c` |
| Report commit scope / lands last | `git diff-tree --no-commit-id --name-only -r 674b6b7d` | only `.ufo/reports/round-63/tameshi.md`; committed 2026-11-01 08:15:20 -0800 (= the complete digest time) |
| `SHONEN` heading in committed report | `git show 674b6b7d:<report> \| grep -n '^## SHONEN'` | line 166; 4 `[~]` lines (one per box; lane-asserted, no independent promotion verifier — correct, none written this round) |
| Cited hashes exist + ancestry | `git cat-file -e <h>^{commit}` + `git merge-base --is-ancestor <h> refs/heads/master` for `8616d47e`, `a18c20f0`, `e9673d2d`, base `0b81e8f5` | all exist, all ancestors of `refs/heads/master` |
| Pushed | `git rev-parse refs/heads/master` vs `git ls-remote origin refs/heads/master` | both `e9673d2ddfa3e2b445d93c21f20c4b34dc55ab07` |
| Round work in range | `git log --format='%h %an' 0b81e8f5..e9673d2d` | exactly 3 commits (`8616d47e`, `a18c20f0`, `e9673d2d`), all `tameshi-shokunin` |
| Diff footprint | `git diff-tree -r --name-status 0b81e8f5 e9673d2d` | 39 paths: 34 A + 5 M (`LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `.ufo/evidence/round-21/coldread/ledger.json`) — matches the report's table |

## 2. Claim re-checks — both RE-MEASURED by this verifier (not evidence-verified only)

### R63-C1 (calibration; closes r62 routed defect RD5) — verifies, re-measured

- Before re-derived: `git cat-file -e 0b81e8f5:tools/additivity-receipt.py` →
  `fatal: path … does not exist` (confirmed); `git ls-tree 0b81e8f5 tools/ | grep -c additivity` → `0`.
- Tool blob identical at all three work commits: `74996652b52bc1484a46a36ef3e5dc16ea4f8f14`
  (`git rev-parse <rev>:tools/additivity-receipt.py` at `8616d47e`, `a18c20f0`, `e9673d2d`).
- Selftest run by this verifier at the tip:
  `python -I tools/additivity-receipt.py --selftest` →
  `ADDITIVITY_SELFTEST: 5/5 pass`, exit 0. ARM-EOL-REWRITE is the exact r62 defect
  shape as a green arm (raw_old_only=10, norm_cr_old_only=0, `eol_rewrite_disclosed=true`,
  exit 0); ARM-REQUIRE-RAW turns the same bytes red (exit 1); ARM-ALTER/ARM-DELETE exit 1.
- Red/green demo on the real r62 pair (`ed3a66c2c5458fc6e4ecbc41cbaf93ed05f6db98` →
  `5721f7d5c872f3bf62b73c47bca2dc67015e06b0`), run by this verifier:
  - RED: `--require-raw` → LOG.md raw_old_only=79 / norm_cr_old_only=0, SCORECARD.md
    raw_old_only=29 / norm_cr_old_only=0, `verbatim_prefix=true`,
    `eol_rewrite_disclosed=true`, **exit 1**.
  - GREEN: same pair, normalized judgment → same numbers, **exit 0**.
  - Matches the report and the committed receipts battery
    (`.ufo/evidence/round-63/win-host/additivity/receipts.txt`) line for line.
- The 80/30 vs 79/29 reconciliation re-derived: `comm -23 <(show base | sort -u)
  <(show tip | sort -u) | wc -l` → `80` / `30`; same pipe with `grep -c .` → `79` / `29`
  (the inserted empty line is not a content member) — exactly the erratum's stated
  count convention. The committed red-before receipt
  (`.ufo/evidence/round-63/win-host/red-before/additivity-redbefore.txt`) records
  the wc-l form (80/30) and the CR-stripped 0/0 content truth, pre-data.
- RD5 erratum present in SCORECARD (`## Erratum — round 62 routed defect RD5`):
  cause, content truth, correction of record, convention, practice — all consistent
  with this verifier's own re-measurements.

### R63-C2 (operability, verdict-only + capability; closes RD6 + the RD4 site) — verifies, re-measured

- Counters re-derived on committed bytes:
  `git show <rev>:corpus/QUALITY.md | grep -c '### Criterion 120'` → `0` at base,
  `1` at tip; `grep -cE '^\| S294 '` on SOURCES → `0` → `1`; registry rows → `153` → `154`;
  ledger entries (`python -I -c "import json;print(len(json.load(...)['entries']))"`) →
  `680` → `693`. Criterion 120 carries its lesson citation
  (`corpus/lessons/round-62.md ## Mistakes 1`).
- Guard run by this verifier (`tools/coldread-precheck-portable.py`, digest
  `892a045d…` byte-unchanged, cached batched mode, work dir in verifier scratch):
  - RED at the work commit: `--floor 0b81e8f5… --cand 8616d47…` →
    `COLDREAD_PRECHECK floor=0b81e8f57562 floor_credited=64 cand=8616d47ebbb8
    cand_credited=51 lost=13 RED`, exit 1; 13 LOST lines (the record sections),
    LOST input-drift lists name `corpus/QUALITY.md` / `corpus/SOURCES.md`;
    `EQUIVALENCE floor_sampled=20 floor_mismatches=0 cand_sampled=20 cand_mismatches=0`.
  - GREEN at the tip, round floor: `--cand e9673d2d…` →
    `cand_credited=64 lost=0 ok`, exit 0, probe sampled=20 mismatches=0.
  - GREEN at the tip, historic floor `8b0042bd…` → `floor_credited=46
    cand_credited=64 lost=0 ok`, exit 0, probe mismatches=0.
  - Both floors match the report's claimed tip re-confirmation.
- Rekey chain spot-checked: `rekey-summary.json` (pin `8616d47…`, ledger 680 → +13
  entries, 13 sections each with a written trace and `verified-record` verdict);
  trace blob `.ufo/evidence/round-63/rekey/traces/section-01.json` exists at the tip
  and is a genuine as-run receipt (`tameshi-trace-inputs-v1`, argv at the pin). The
  guard's credit rule (trace must exist as a blob at the measured rev) is exercised
  by this verifier's own GREEN runs at credited=64/64.
- RD4 site repair: the SOURCES diff shows the round-61 **prose note** (not a registry
  row cell) changed `the §Output batch framing, 12 words` → `8 tokens`, logged
  old → new in the new round-63 note, named as the r62 erratum RD4 site. Disclosed
  in-place repair of a closure-routed defect; CORPUS rule 2's append-only column
  discipline (status/recheck/used-by) is not implicated.
- Capability row `monitored-record rekey run-book` entered the SCORECARD capabilities
  table (mid-file insertion — the round's disclosed mid-file insertion), with a
  run-book command and first-working-round provenance (r61 batch rekeys; re-demonstrated r63).

### The self-caught SCORECARD CRLF→LF rewrite (lesson mistake 4) — restoration VERIFIED at byte level

- The instrument measures commit `8616d47`'s SCORECARD as raw_old_only=2388,
  norm_cr_old_only=0, rewrite disclosed (committed receipt; the whole-file rewrite shape).
- Direct check by this verifier: at `a18c20f0`, the base `SCORECARD.md` blob bytes are a
  raw byte prefix of the tip blob (`new[:len(old)] == old` → **True**; base 353,534 B,
  restored + 66 appended lines) — the rewrite was truly restored at binary level before
  the rekey commit, exactly as claimed.
- At the final tip the raw prefix check is False only because the R3 commit inserted the
  capability row mid-file (disclosed); `raw_old_only=0` and `norm_cr_old_only=0` still hold
  (no pre-existing line altered), and the tip file is uniformly CRLF (3240 CRLF lines,
  0 LF-only lines — the inserted row also carries CRLF).

## 3. No-harm check — no owned axis harmed

- `git diff-tree -r -p 0b81e8f5 e9673d2d -- SCORECARD.md` + spot reads: no pre-existing
  axis row altered (SCORECARD base→tip measures `raw_old_only=0`, `norm_cr_old_only=0`);
  additions only (erratum, planned block, r63 claim rows, measured rows, capability row).
- Protected surfaces byte-unchanged base→tip (blob-id compare): `PROVINCE.md`
  `8388c23a…`, `SKILL.md` `95d1f935…`, `README.md` `451e8236…`, `tools/registry.json`
  `62c4670d…`, guarded probe `tools/coldread-precheck-portable.py` `e827e6e5…`
  (sha256 `892a045d8b508214804e2b26b78c15b83aae65bdae4bd5bf022b8cb735f3b33e` — matches
  the report's pinned digest).
- Axis verdicts re-checked against the measurements above.

## 4. Per-axis verdicts (this verifier, non-author)

| Axis | Verdict | Basis |
|---|---|---|
| calibration | **improved** | 8 → 8 at the lane-attainable cap; the move is receipt honesty: RD5 correction of record + standing convention + committed red/green instrument, all re-measured green by this verifier; the defect class was caught recurring in the round's own tooling pre-push (mistake 4) and the restoration is byte-verified |
| operability | **improved** | verdict-only axis: criterion 120 landed, RD4 site repaired, the rekey run-book executed end to end on this host (RED lost=13 → GREEN 64/64 lost=0 at both floors, re-run by this verifier); capability row entered with a demonstrated run |
| depth | unchanged | no depth surface touched (probe/tooling bytes unchanged; no new mutation cases claimed) |
| freshness | unchanged | no freshness claim made this round; monitor restored to its r61/r62 state at the tip |
| coverage | unchanged | SOURCES 153 → 154 is claim-grounding for C1, not a new domain surface; PROVINCE/README unchanged |
| adjacency | unchanged | nothing absorbed; PROVINCE.md byte-unchanged |

## 5. Discernment spot-check table

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S294 (gitattributes docs, tier A docs, mined) — the round's admit | admit (row + used-by lesson) | committed extract `.ufo/evidence/round-63/win-host/sources/s294-gitattributes.html`, sha256 re-computed `56f2e80e4afadac4458da6c8e0e952e514eba23a125383eab1931cc6210e9d30` = recorded; quote read at cited fetched-page lines 2678–2679 | **agree** | The ≤25-word quote (18 words as stated) is verbatim on the cited lines — "Setting the `text` attribute on a path enables end-of-line conversion on checkin and checkout as described above." — and genuinely grounds C1's premise (conversion is a declared attribute layer; this repo has no `.gitattributes` and `core.autocrlf=false`, so blobs carry committed bytes). Duplicate sweep re-run: `git show 0b81e8f5:corpus/SOURCES.md | grep -c gitattributes` → `0`; census-clean (no new warning). |
| S293 standing rejection (git-cat-file docs) — the reject sample; r63's Gate cites its W04 marker | reject (within-scope duplicate of S289, kept as the rejection record) | SOURCES rows at tip: S289 (line 164) holds `https://git-scm.com/docs/git-cat-file`; S293 (line 168) reads `REJECTED: within-scope duplicate … per CORPUS.md rule 2 (and the S073/S103 precedent)` | **agree** | The URL is genuinely already held by S289; rule 2 forbids a second row for a held source; keeping the rejection as a row with reason + flip is exactly the contract's rejection discipline. The r63 census note correctly leaves the S293 W04 standing as the rejection's marker. |
| considerthese 2026-10-28 proposal 1 (receipt-existence linter) priced out | reject-as-candidate this round (recorded as proposal) | `considerthese/2026-10-28.md` lines 73–77 (proposal text re-read) | **agree** | The proposal is real and priced honestly: building a record-wide linter this round would compete with the rekey the round deliberately paid for, and its counting-command half already landed as criterion 120 (verified: criterion text + lesson citation present). Carrying the cited-receipt-exists half as a proposal is the honest disposition. |

Census re-run by this verifier:
`bash scripts/sources-census.sh validate --root <fleet-root> tameshi` → **exit 0**;
17 W04 + 1 W01, all pre-existing (S047…S293 duplicates + S101 tierC-mined); S294 adds
no warning — matches the report's census claim.

Note: the r63 `## Gate` section contains no fresh rejected source row this round (its
only new row is the S294 admit); the reject sample above is the standing S293 rejection
the Gate itself cites, plus the round's candidate price-out. Not a violation (the
contract sets no rejection quota) — recorded so the discernment trail stays visible.

## 6. Trend verdicts (this verifier, non-author)

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | **unchanged** | `git diff-tree` base→tip shows 0 additions under `corpus/knowledge/`; no frontier move; the one SOURCES row is C1's claim ground; report declares the round repair-and-convention |
| quality | **improved** | RD5 now has a correction of record + a standing convention + a committed instrument this verifier ran green (5/5 selftest; real-pair red/green reproduced); RD6 criterion landed; RD4 site repaired; monitor green at the tip at both floors (re-run by this verifier) |
| discernment | **improved** | four mistakes mined with class · evidence · captured-by · fix; two self-caught pre-push (mistakes 3–4); the guard catching the lane's own record edits is receipted as designed behavior; the in-place registry repair is logged old → new; this verifier's spot-check agrees with the gate on the admit and both rejects sampled |

## 7. Routed defects / carried items for next round

None routed. Two status-neutral observations for the lane:

1. **`rekey_round: 61` labels the 13 r63-created ledger entries.** The field is the
   run-book generation id (49 entries carry it, across read_revs `19d7e996`, `0a29e3cf`,
   `8616d47` — r61's two batches and r63's batch), and `read_rev` distinguishes the
   batches, so no round-attribution error is implied. A `rekey_batch`/run-id field would
   read clearer next time the run-book runs.
2. **Gate carried no fresh rejected source row this round** (see §5 note). No action
   owed; keep sampling rejections when a round actually rejects something.

Also noted (operator-visible, status-neutral): SHONEN.md remains four `[~]`
lane-asserted boxes with no independent promotion verifier on record; per protocol only
a non-author may write `[x]` — this verifier did not write any mark. The r60 L0
question (option (b)) stands open and unanswered, as the report discloses.
