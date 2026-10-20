# CRRevenger — round-1 cold-read reconstructed; ledger-assembly checklist

Seat `TameshiR16.CRRevenger` (leaf revenger; no subagent dispatch). Lane root
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Scratch
`/tmp/tameshi-r16-CRRevenger-1NCcBP/`. Observed facts carry the command that
produced them; inferences are marked `[I]`. Nothing was executed against lane
code; the round-1 suites were not re-run — their committed evidence was
hash-verified instead.

## Bottom line

- Round 1 executed **16.2 % of the page** (240 of 1477 lines), **7 of 43**
  ledger buckets, every one only partially; **36 buckets were never opened**
  (including the preamble). "Appendix A + B" was not a conservative summary of
  the run — it was the run.
- The adjudication names two causes: partial page scope, and Appendix B
  survivor-probe fixtures **reconstructed by the seat** because the page points
  at a note (§7) it does not contain. The flood of detail around those two
  facts (route substitution, explicitly unexercised sections, lane-dispatched
  seat) is in the scope note too.
- Box 3's increment scored **0**. The mark stayed `[~]` as an unscored, scope-noted lane
  assertion; calibration pinned **6**. Criterion 13 generalises the rule: an
  Appendix A/B cold-read cannot earn full-page box-3 credit.
- The round-16 snapshot is **51 ledger buckets** (preamble + 50 ATX headings),
  not 50. Forty-two buckets are byte-identical to round 1, one differs only by
  a trailing blank line, and eight are appended (rounds 12–15). The full-page
  read is therefore *old scope finally covered* + 8 new sections, not a new
  page.
- One record section still says **"Box 3 remains `[ ]`"** (snapshot:1472)
  while `SHONEN.md:9` at the same HEAD says `[~]`. It is the ER-K5 stale-record
  class, unchanged since round 1. A full-page read must disposition it; it
  cannot be silently marked `verified-record` by a seat that is forbidden to
  open `SHONEN.md`.

## 1. Reconstruction of the round-1 cold-read

### 1.1 Page, buckets, counts

- Executed bytes: `git show 4eb4cf3:SKILL.md` → sha256
  `33e3009c919cd0fb0b2c67bbd7927655289450750f4f69d9ca86758d81000f81`,
  1477 lines, last byte `.` (no trailing newline). Matches the report's
  snapshot claim (`reports/round-1-kaika-coldread.md`).
- Fence-aware enumeration of `#`/`##`/`###` headings **outside code fences**:
  **42 heading sections + preamble 1–5 = 43 buckets**. Widths sum to 1477,
  contiguous.
- Naive `grep -E '^#{1,3} '` returns **46**: four false headings are code-block
  comments at 549 (`# write driver + manifest`), 552 (`# survivor probes`),
  618 (`# write driver + SPECS`), 621 (`# survivor probes (note §7 commands`).
  This is the first machine trap for the ledger.

Manifest statistics, observed:

```
SKILL.r1.md          entries=43 lines=1477 sum-widths=1477 contiguous=True
SKILL.snapshot.md    entries=51 lines=1705 sum-widths=1705 contiguous=True
```

### 1.2 Scope actually exercised

The report cites 21 distinct page ranges. Their union is **240 unique lines =
16.2 %** of 1477. Seven buckets are touched, all partially:

| bucket | lines touched / width | heading |
|---|---|---|
| 17–29 | 4 / 13 | `## Standing rules` |
| 131–245 | 105 / 115 | `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` |
| 375–404 | 1 / 30 | `## Restore discipline — proof the substrate never moved` |
| 527–593 | 51 / 67 | `## Appendix A — worked example: JS case` |
| 594–667 | 56 / 74 | `## Appendix B — worked example: bash case` |
| 668–793 | 4 / 126 | `## Third case — cross-author confirmation (round 5, measured)` |
| 827–857 | 19 / 31 | `### The protocol — ordered, fail-closed` |

The other **36 buckets** (preamble + 35 headings) were not opened at all:
`1–5` (preamble), `6–16`, `30–57`, `58–93`, `94–130`, `246–313`, `314–374`,
`405–465`, `466–496`, `497–526`, `794–805`, `806–826`, `858–882`, `883–898`,
`899–920`, `921–932`, `933–964`, `965–1009`, `1010–1020`, `1021–1068`,
`1069–1091`, `1092–1154`, `1155–1163`, `1164–1211`, `1212–1229`, `1230–1245`,
`1246–1271`, `1272–1280`, `1281–1301`, `1302–1364`, `1365–1379`, `1380–1395`,
`1396–1435`, `1436–1448`, `1449–1463`, `1464–1477`.

This is the measurable meaning of the SHONEN scope note "Appendix A + B sweep
recipe only … audit recipe, fail-closed taxonomy, service/cadence/runbook not
exercised" (`SHONEN.md:10`).

### 1.3 What ran, verified from committed evidence

- JS: `appendixA/results.tsv` — 10 rows, **8 KILLED / 2 SURVIVED**
  (D2, D10). `A-tool.txt`:
  `MUTATE: DONE (target=appendixA defects=10 killed=8 survived=2 inconclusive=0 kill-rate=80%)`;
  `MUTATE_RESTORE: OK (target-sha256 before=83016d45… after=83016d45… pristine-sha256=83016d45…)`.
- Bash: `appendixB/results.tsv` — 10 rows, **8 KILLED / 2 SURVIVED**
  (B5, B10). `B-tool.txt`: same DONE line for `appendixB`; restore before/after
  `275d8294…`.
- Controls: `A-control.txt` — `KIMI_CENSUS_SELFTEST: 43/43 pass`, `VERDICT: PASS`;
  `B-control.txt` — `SELFTEST: PASS (16 cases)` with `skip-case 15/16`.
- Survivor probes: `B-probe-B5-pristine.txt` prints
  `SURFACE DIVERGED $HOME/bin/tool (declared exec, no execute bit)` +
  `SURFACE_CENSUS: DRIFT`; the mutant prints `SURFACE OK … (exec 644)` +
  `SURFACE_CENSUS: CLEAN`. `B-probe-B10-pristine/mutant` differ only in
  `ok=1` vs `ok=0`. A probes: `+22 more` vs `+23 more`, `frozen=25` vs `24`
  (per the report; the two A-probe files are present at 4016 and 4055 bytes).
- Provenance: **43 of the 44** in-repo evidence files listed in
  `.ufo/evidence/kaika-round-1/coldread/SHA256SUMS.txt` hash-match their
  round-time digests; the one mismatch is the report, explained below.
  The sums file's self-entry cannot verify itself and does not match — do not
  cite it; it is an artefact of how the file was generated.

Report/hash reconciliation, observed:

```
sha256(report[0:i]) where i = start of "\n---\nL1 integration note"
  = e1b7ea07b53e8daef07d5c4567aa2b99f964542d9c103732b87727200a509cc5
SHA256SUMS.txt entry for reports/round-1-kaika-coldread.md
  = e1b7ea07b53e8daef07d5c4567aa2b99f964542d9c103732b87727200a509cc5
sha256(full current report) = f94e0c0a94f65622f31edc38ac1cd879de16d3edf63ea98f9be468b0213b33e9
```

So the current report differs from the executed report **only** by the
appended L1 note; the executed prefix is still verifiable. This is the
technique the round-16 ledger should use for append-only corrections.

### 1.4 The reconstructed fixtures (the improvisation)

Appendix B's probe block (round-1 snapshot:621) says:

```
# survivor probes (note §7 commands; run from the work dir):
bash "$W/mutant-B5.sh"  verify --root "$W/probe/host"  --census "$W/probe/census.tsv" …
bash "$W/mutant-B10.sh" verify --root "$W/probe2/host" --census "$W/probe2/census.tsv" …
```

The commands are complete; the **fixture construction is not on the page** —
it lives in "note §7", which the contamination rule forbids. The seat rebuilt
it from the gate's input contract and retained the result at
`.ufo/evidence/kaika-round-1/coldread/probe-fixtures/`, observed:

| file | content |
|---|---|
| `probe/census.tsv` | `$HOME/bin/tool<TAB>asset<TAB>exec<TAB>-<TAB>probe no-x exec` |
| `probe/host/bin/tool` | one byte `x`, mode 644 |
| `probe2/census.tsv` | `$HOME/bin/tool<TAB>asset<TAB>file<TAB>600<TAB>probe file` |
| `probe2/host/bin/tool` | one byte `x`, mode 644 |
| `shapes.tsv`, `baseline.tsv` | empty in both trees |

This is exactly the report's one `ADDITIVE-IMPROVISATION` cell. It did not
block round 1's own sufficiency verdict — the reconstructed fixtures reproduced
the page's recorded readings verbatim — but it is a **gap-minor**, never
`executed-ok`, and the adjudication cited it.

### 1.5 Route substitution

Round 1 ran the sweep through `tools/mutate-and-run.sh` plus its own
uniqueness checker. The appendices name `python3 "$W/mutate_driver.py"
--check/--run`. The harness is page-internal (the round-6 protocol at
snapshot:829–847 directs it), so this was disclosed latitude, not a blocking
gap. It still means the appendices' literal route was **not** exercised. A
full-page ledger must not turn that into `executed-ok` for the route
instruction.

## 2. Adjudication, exact

- `SCORECARD.md:209-214`:
  > **K1 re-pinned without the box-3 increment.** The cold-read covered
  > only Appendix A + B, with Appendix B survivor-probe fixtures
  > reconstructed by the seat; the box-3 `[ ]`→`[~]` move is **not
  > earned** and scores 0. Box 3 stays `[~]` as a scope-noted lane
  > assertion (`SHONEN.md:9-10`), carried as an unscored mark.
- `corpus/lessons/round-1-verifier-spotcheck.md:17`: "the box-3 increment is
  not credited (cold-read covered Appendix A+B only, probes reconstructed) …
  Debts: box 3 needs a fresh reader to run the full page-defined procedure".
- `corpus/QUALITY.md:43-46` criterion 13: "Promotion restraint remains separate
  from partial procedure exercises: an Appendix A/B cold-read cannot earn
  full-page box-3 score credit."
- `SHONEN.md:9-10` (unchanged at HEAD):
  "Instructions executable by an agent without oral context
  [lane assertion, scope-bounded: fleet round-1 cold-read of blob
  4eb4cf3:SKILL.md — Appendix A + B sweep recipe only, 8/10 + 8/10 = recorded,
  4/4 survivors probed (B probe fixtures reconstructed), 0 blocking gaps; run
  via tools/mutate-and-run.sh, not the appendices' python driver; audit recipe,
  fail-closed taxonomy, service/cadence/runbook not exercised; lane-dispatched
  seat; no independent promotion verifier]".
- `corpus/lessons/round-1.md:462-471` ER-K7: the line was broader than the run;
  the no-permissiveness audit recipe and fail-closed taxonomy were not
  exercised; the line was narrowed. The lesson is criterion-shaped: *a mark's
  evidence covers the mark's whole wording or the mark does not score.*
- Independence: `PROTOCOL.md:61-67` — "a subagent the lane dispatched is still
  the lane"; only a non-author may write `[x]`. SHONEN says the seat was
  lane-dispatched and no independent verifier signed.

Why box 3 failed, in one sentence each:

1. **Partial page**: 7/43 buckets, 16.2 % of lines; the service, cadence,
   runbook, leg-ledger, audit recipe and fail-closed taxonomy were never read.
2. **Reconstructed probes**: a page instruction whose material is off-page was
   completed by inference; the page is not self-contained at that point.
3. **Route substitution**: the literal driver route was not run.
4. **Claim breadth**: the mark's sentence covered the whole box, the evidence
   covered a subset; the sentence had to be narrowed and the increment lost.
5. **No independence**: even a perfect lane-seat read cannot write `[x]`.

## 3. Round-16 page deltas and specific traps

### 3.1 Bucket arithmetic

- Snapshot and HEAD are identical: `git show HEAD:SKILL.md` sha256
  `97cf436b…3580`, `cmp` against
  `.ufo/evidence/round-16/coldread/SKILL.snapshot.md` → identical. HEAD is
  `28aeef498cc070c3183271b709bc79d344ff547a`.
- 1705 lines, no trailing newline; **51 buckets** = preamble 1–5 + 50 headings.
  The claim says "50 sections": true for heading sections, **false as a ledger
  entry count**. Dropping the preamble violates the ledger schema.
- Naive heading grep gives **54**; the four in-fence lines are the same four
  content lines at 549, 552, 618, 621 (the page is unchanged through the
  appendices). A ledger built from naive grep would create four fake buckets
  and split real ones.
- 42 buckets are byte-identical to round 1; 1 (`## Promotion-evidence
  calibration — fleet round-1`, 1464–1478) differs only by a trailing blank
  line; 8 are new (table below). So the page is a strict superset of the
  round-1 page in substantive text.

| new bucket | heading |
|---|---|
| 1479–1498 | `## Repeated controls and gate registry — round 12` |
| 1499–1516 | `### Gate/probe registry` |
| 1517–1547 | `## Pin disposition and provenance correction — round 13` |
| 1548–1562 | `### Round-13 gate/probe registry` |
| 1563–1596 | `## Effective expectation reconciliation — round 14` |
| 1597–1608 | `### Round-14 historical registry — superseded by round 15` |
| 1609–1675 | `## Context gate classification and explicit exit classes — round 15` |
| 1676–1705 | `### Round-15 gate/probe registry` |

### 3.2 The stale record the snapshot still contains

- Snapshot:1472–1473: **"Box 3 remains `[ ]`"**, citing
  `corpus/knowledge/executor-test-sufficiency.md:160–184`.
- `git show HEAD:SHONEN.md` line 9: box 3 is **`[~]`**, scope-bounded. The
  working tree is clean (`git diff --stat -- SHONEN.md` empty), so this is a
  same-HEAD contradiction, not a working-copy accident.
- Snapshot:14–15 (intro): "Historical cold-read proof covers one JS mutant
  only; current full-sweep/bash sufficiency remains unverified." This is
  ER-K5's cited stale sentence and it is still present; the round-1 report
  measured both appendices. ER-K5 (`corpus/lessons/round-1.md:442-450`) names
  the owner: "the round that next edits `SKILL.md`, which must re-run the
  cold-read."
- The promotion section names **`SHONEN.md`**, **`reports/round-1-calibration.md#box-1`**
  and **`corpus/lessons/round-1.md`** — all three on the cold-read
  contamination Never-list. Of its verification anchors, only
  `corpus/knowledge/executor-test-sufficiency.md` is openable;
  `../PROTOCOL.md:63–68` is a rules reference, not an evidence anchor. A
  compliant seat therefore **cannot verify** the section's record claims; it
  must record a named gap, not `verified-record`.

This is the single most dangerous box-3 trap in the round: a seat that marks
the promotion section `verified-record` has either opened forbidden material
(contamination) or invented a verification. L1 must fix the ingestion rule
before assembly (see P12/P20).

## 4. Ledger-assembly checklist for L1

Round-1 defect → the control that prevents its repeat in the ledger:

| round-1 defect | round-1 evidence | ledger control |
|---|---|---|
| Partial page: 7/43 buckets, 16.2 % of lines | §1.2; `SHONEN.md:10` | P2–P5, P19 |
| Appendix B probe fixtures reconstructed off-page | §1.4; snapshot:621 | P9 (`gap-minor`, never `executed-ok`), P20, P23 |
| Harness route substituted for the page's driver | §1.5; ER-K7 | P11, P21 (claim must name the route) |
| Step table instead of per-section verdicts | report's step-sufficiency table | P15–P16 |
| Claim wider than the run (ER-K7) | `corpus/lessons/round-1.md:462-471` | P21 |
| Stale record claims (ER-K5) | snapshot:14–15, :1472 vs `SHONEN.md:9` | P20 |
| Record anchors named but forbidden to open | snapshot:1466–1467, :1477 | P12 |
| Evidence copy removed / append-only drift | `SKILL.snapshot.README`, §1.3 prefix hash | P17, P23 |
| Lane-dispatched seat, no independent verifier | `PROTOCOL.md:61-67`; `SHONEN.md:10` | P21 |
| Pins taken from a dirty worktree | round-1 O4 foreign edit | P1, P18 (blob pin; re-read after edit) |

Apply in order. "Reject" means stop and route the seat back for a clean
re-read; do not repair a seat report by editing it.

### A. Bind the page

- [ ] **P1 — snapshot identity.** `sha256sum .ufo/evidence/round-16/coldread/SKILL.snapshot.md`
  is `97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580`,
  and `git show HEAD:SKILL.md | sha256sum` is the same. Record HEAD in the
  build log. If they differ, the ledger is bound to the wrong bytes: reject
  the whole assembly and re-snapshot/re-read (ER-K5).
- [ ] **P2 — bucket count.** Expect **51** entries, not 50: preamble (1–5,
  heading `""`) + 50 heading sections. If the round's claim says "50 sections",
  amend the claim to "50 heading sections + preamble"; do not drop the preamble
  to make the number match.
- [ ] **P3 — fence-aware enumeration.** Heading = `^#{1,3} ` outside a
  backtick/tilde fence. Reject any manifest with 54/55 entries or with buckets
  starting at 549, 552, 618, 621; those are code comments.
- [ ] **P4 — exact section hash.** Section text = heading line through the line
  before the next heading, `"\n".join(...)`, **no trailing newline**; sha256
  over UTF-8. Recompute every entry from the snapshot; a mismatch is a corrupt
  ledger row, never a seat typo.
- [ ] **P5 — coverage arithmetic.** First start 1; each start = previous end +
  1; last end 1705; sum of widths 1705; no duplicate starts. Reject on any
  gap/overlap.

### B. Ingest seat blocks

- [ ] **P6 — one block per seat.** Exactly one fenced `json` block per CR
  report, at the end; parse the last. Reject reports with zero or two blocks.
- [ ] **P7 — bound bytes.** Every block's `skill_sha256` must be `97cf…`.
  A seat that read a different revision is a different experiment; reject it
  and re-read on the snapshot.
- [ ] **P8 — manifest alignment.** Each `start` must equal a manifest heading
  line (or 1 for preamble) and each `end` must equal the next heading − 1 (or
  1705 for the last). A seat assigned a cut range still speaks for the whole
  bucket; if it read only part, its verdict is `gap-minor`/`not-executed` with
  the unread remainder named — never `executed-ok`.
- [ ] **P9 — class/verdict coherence.** `class` ∈ {`instruction`,`record`};
  `verdict` ∈ {`executed-ok`,`verified-record`,`gap-minor`,`gap-blocking`,
  `wrong-expectation`,`not-executed`}. `record` cannot be `executed-ok`;
  `instruction` cannot be `verified-record`; `not-executed` must name why;
  `gap-minor` must name the inference and the observed outcome.
- [ ] **P10 — arrays and counts.** `blocking_gaps`, `wrong_expectations`,
  `minor_gaps`, `commands_executed`, `opened` are arrays of non-empty strings.
  Ledger ints = count of **unique** strings (dedupe across seats), not the sum.
- [ ] **P11 — executed evidence.** For `class=instruction` + `verdict=executed-ok`,
  `commands_executed` must be non-empty and must contain a command, not a
  description. This is the anti-copy-forward control: round 1's page-step table
  could not distinguish "read" from "ran", and the ledger must.
- [ ] **P12 — contamination audit.** Reject a seat if `opened` contains
  `LOG.md`, `SCORECARD.md`, `SHONEN.md`, `plans/`, `reports/`,
  `corpus/lessons/`, `.ufo/waves/`, or another seat's report — **even when the
  section names the path**. For a named-but-forbidden pointer, require a
  `gap-minor` naming the pointer and the blocked verification. This applies to
  snapshot:1466–1467 and :1477.
- [ ] **P13 — scratch.** `scratch` matches `/tmp/tameshi-r16-*/`; reject
  repo-local scratch (QUALITY 9).
- [ ] **P14 — prior exposure.** If a seat reports having opened round-1's
  report or evidence, mark its entry non-blind (record the exposure in the
  build log) and require a fresh seat for a blind verdict. Round 1's own
  witness discipline (criterion 12) and the S006 precedent apply.

### C. Build entries

- [ ] **P15 — one entry per bucket.** Never one per report. `seats[]` = all
  seats that gave a verdict for the bucket, sorted; `reports[]` = their
  lane-relative report paths. No bucket without at least one seat and one
  report.
- [ ] **P16 — merge rule.** One class per bucket; on conflict take the most
  severe verdict in this order: `wrong-expectation` > `gap-blocking` >
  `not-executed` > `gap-minor` > positive (`verified-record`/`executed-ok`).
  A conflict is a finding: record the rival verdict in the build log, do not
  silently pick the friendly one.
- [ ] **P17 — append-only history.** Keep the wave-1 ledger and the wave-2
  ledger as separate artifacts (or a JSONL history); the final `ledger.json`
  may supersede rows but must not erase the pre-repair verdict. The round-1
  report's prefix-hash proof (1.3) is the model: hash the superseded bytes,
  append the correction, keep both pointers.
- [ ] **P18 — repairs are re-reads.** Every wave-1 `gap-blocking` gets a named
  repair and a **fresh wave-2 seat** verdict. L1 cannot repair a gap and then
  mark its own repair `executed-ok`; that is not a cold read. A repair that
  changes `SKILL.md` changes the snapshot sha → return to P1.

### D. Gate the box-3 claim

- [ ] **P19 — hard gate.** 51/51 buckets present; `blocking_gaps = 0` and
  `wrong_expectations = 0` across the ledger; no `not-executed`; every entry is
  `executed-ok`, `verified-record`, or a **named** `gap-minor` with its observed
  outcome. Reject the claim if any of these fail.
- [ ] **P20 — stale-record disposition.** The promotion bucket (1464–1478)
  and the intro bucket (6–16) carry claims that contradict SHONEN/round-1
  evidence. Record them in a `dispositions` block in the build log with the
  contradicting anchor and one of: (a) left untouched, debt named with owner
  (ER-K5 precedent; the cold-read stays bound to `97cf…`), or (b) an append to
  `SKILL.md` **after** the read, which triggers a re-read on the new sha.
  Do not mark them `verified-record` on a lane seat's word.
- [ ] **P21 — claim wording.** The SHONEN box-3 line must cite: snapshot sha,
  the ledger path, 51/51 entries, the verdict counts, `HEAD 28aeef4`, "50
  heading sections + preamble", every named minor gap, the stale-record
  disposition, and the independence caveat. It must remain `[~]`: a
  lane-dispatched seat is still the lane (`PROTOCOL.md:61-67`); the final 2
  points need independent promotion review. No `[x]`.
- [ ] **P22 — calibration arithmetic.** 6 → 8 requires boxes 1, 2, 3, 4 all
  `[~]` at 2 points each. Command C's `asserted_mark_upper_bound=8` is a mark
  census, not the pin; the pin is the rubric. State the distinction.
- [ ] **P23 — evidence placement.** The ledger, seat reports and any
  reconstructed fixtures live in-repo under `.ufo/evidence/round-16/coldread/`
  (or the wave dir); scratch is `/tmp` only. Any removed byte copy keeps its
  hash plus a re-derivation command (round 1's `SKILL.snapshot.README`).
- [ ] **P24 — validator run.** Run the checker in §5 once after assembly.
  Expected: `LEDGER OK buckets=51 lines=1705` and a verdict histogram; any
  nonzero exit blocks the claim.

### E. Do not conflate the two ledgers

- [ ] **P25 — depth leg is separate.** C1's `js-round-gate` leg is counted by
  command D's regex over `tools/mutate-and-run.sh`:
  `^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+`. At the measured commit it must print
  `recorded_cases=7 depth_score=7`. The cold-read `ledger.json` is not a
  mutation ledger and must not be cited by command D. If the leg comment does
  not match the regex (indentation, missing colon-free id, missing `n/m`), the
  depth claim silently fails.

## 5. Validator

Run from the lane root after assembly. It derives the manifest from the
snapshot, so it cannot be satisfied by a hand-written bucket list.

```python
#!/usr/bin/env python3
import hashlib, json, re, sys

SNAP = ".ufo/evidence/round-16/coldread/SKILL.snapshot.md"
LEDGER = ".ufo/evidence/round-16/coldread/ledger.json"
WANT = "97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580"
CLASSES = {"instruction", "record"}
VERDICTS = {"executed-ok", "verified-record", "gap-minor",
            "gap-blocking", "wrong-expectation", "not-executed"}

def manifest(path):
    raw = open(path, "r", encoding="utf-8").read()
    text = raw[:-1] if raw.endswith("\n") else raw
    lines = text.split("\n")
    heads, fence = [], None
    for i, line in enumerate(lines, 1):
        m = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if m:
            ch, n, rest = m.group(1)[0], len(m.group(1)), m.group(2)
            if fence is None:
                fence = (ch, n)
            elif ch == fence[0] and n >= fence[1] and rest.strip() == "":
                fence = None
            continue
        if fence is None and re.match(r"^#{1,3} ", line):
            heads.append((i, line))
    bounds = []
    if heads[0][0] > 1:
        bounds.append((1, heads[0][0] - 1, ""))
    for i, (ln, h) in enumerate(heads):
        end = heads[i + 1][0] - 1 if i + 1 < len(heads) else len(lines)
        bounds.append((ln, end, h))
    return [{
        "start": s, "end": e, "heading": h,
        "sha256": hashlib.sha256("\n".join(lines[s - 1:e]).encode()).hexdigest(),
    } for s, e, h in bounds], len(lines)

snap_sha = hashlib.sha256(open(SNAP, "rb").read()).hexdigest()
assert snap_sha == WANT, f"snapshot sha {snap_sha} != {WANT}"
buckets, total = manifest(SNAP)
ledger = json.load(open(LEDGER))
errs = []
if ledger.get("schema") != "tameshi-coldread-ledger-v1":
    errs.append(f"schema {ledger.get('schema')!r}")
entries = ledger.get("entries", [])
if len(entries) != len(buckets):
    errs.append(f"entries {len(entries)} != buckets {len(buckets)}")
prev = 0
for i, (entry, bucket) in enumerate(zip(entries, buckets)):
    tag = f"entry[{i}] start={entry.get('start')}"
    for key in ("skill_sha256", "start", "end", "heading", "sha256", "class",
                "verdict", "blocking_gaps", "wrong_expectations", "seats", "reports"):
        if key not in entry:
            errs.append(f"{tag} missing {key}")
    if entry.get("start") != bucket["start"] or entry.get("end") != bucket["end"]:
        errs.append(f"{tag} range {entry.get('start')}-{entry.get('end')} != "
                    f"{bucket['start']}-{bucket['end']}")
    if entry.get("heading") != bucket["heading"]:
        errs.append(f"{tag} heading mismatch")
    if entry.get("sha256") != bucket["sha256"]:
        errs.append(f"{tag} section sha mismatch")
    if entry.get("skill_sha256") != WANT:
        errs.append(f"{tag} skill_sha256")
    if entry.get("class") not in CLASSES:
        errs.append(f"{tag} class {entry.get('class')!r}")
    if entry.get("verdict") not in VERDICTS:
        errs.append(f"{tag} verdict {entry.get('verdict')!r}")
    if entry.get("class") == "record" and entry.get("verdict") == "executed-ok":
        errs.append(f"{tag} record marked executed-ok")
    if entry.get("class") == "instruction" and entry.get("verdict") == "verified-record":
        errs.append(f"{tag} instruction marked verified-record")
    for key in ("blocking_gaps", "wrong_expectations"):
        if not isinstance(entry.get(key), int) or entry[key] < 0:
            errs.append(f"{tag} {key} not a non-negative int")
    if not entry.get("seats"):
        errs.append(f"{tag} no seats")
    if not entry.get("reports"):
        errs.append(f"{tag} no reports")
    if entry.get("start") != prev + 1:
        errs.append(f"{tag} gap/overlap after {prev}")
    if isinstance(entry.get("end"), int):
        prev = entry["end"]
if prev != total:
    errs.append(f"last end {prev} != line count {total}")

hist = {}
for entry in entries:
    hist[entry.get("verdict")] = hist.get(entry.get("verdict"), 0) + 1
blocking = [e for e in entries if e.get("blocking_gaps") or e.get("wrong_expectations")
            or e.get("verdict") in ("gap-blocking", "wrong-expectation", "not-executed")]
for err in errs:
    print("FAIL", err)
print(f"buckets={len(entries)} lines={total} verdicts={hist} "
      f"blocking_entries={len(blocking)}")
if errs:
    sys.exit(1)
print(f"LEDGER OK buckets={len(entries)} lines={total}")
```

## 6. Bounded recommendations

1. **Write 51 entries and say so.** The schema's preamble row is mandatory; the
   claim's "50 sections" must be restated as "50 heading sections + preamble =
   51 ledger entries" or it will read as an off-by-one.
2. **Add a `dispositions` block to the build log** for (a) snapshot:1472
   "Box 3 remains `[ ]`", (b) snapshot:14–15 intro staleness, (c) the three
   named-but-forbidden pointers in 1466–1467/1477, and (d) the round-1 report
   as prior exposure if any seat touched it. Do not force these into
   `wrong-expectation` without an anchor; `gap-minor` plus a disposition is the
   honest row.
3. **Do not edit `SKILL.md` after the snapshot.** HEAD == snapshot today. Any
   append changes the sha and triggers ER-K5's re-read clause; if the round
   must fix the stale record, either do it in the same edit that re-snapshots
   and re-reads, or leave the page untouched and carry the debt with an owner.
4. **Require executed commands for every `executed-ok` instruction entry.**
   Round 1 failed at section granularity precisely because a step table cannot
   show which parts of a section actually ran; the per-entry
   `commands_executed` field is the structural fix.
5. **Reuse round-1's provenance techniques, not its verdicts.** Blob pin
   before/after, control-first, restore byte-identity, off-suite survivor
   probes, evidence hashes in-repo, prefix-hash for append-only reports. The
   round-1 verdicts are a prior-exposure disclosure, not ledger input.
6. **Keep the cold-read ledger and the mutation leg separate.** `recorded_cases=7`
   is C1's depth evidence; the cold-read ledger is C2's calibration evidence.
   Neither counts the other.

## 7. Evidence log (commands and observed results)

| command | result |
|---|---|
| `git show 4eb4cf3:SKILL.md \| sha256sum` | `33e3009c…0f81`, 1477 lines |
| `git show HEAD:SKILL.md \| sha256sum` | `97cf436b…3580`; `cmp` with snapshot → identical |
| `git rev-parse HEAD` | `28aeef498cc070c3183271b709bc79d344ff547a` |
| Python manifest | r1: 43 buckets/1477 lines/contiguous; r16: 51/1705/contiguous |
| `grep -E '^#{1,3} '` naive vs fence-aware | 46 vs 42 (r1); 54 vs 50 (r16); false heads 549/552/618/621 |
| cited-range union | 240 unique lines = 16.2 %; 7 buckets touched, 36 untouched |
| section hash comparison | 42 identical, 1 changed (promotion + blank line), 8 new |
| `awk`/Python on `appendix{A,B}/results.tsv` | 10 rows each, 8 KILLED / 2 SURVIVED |
| `A-tool.txt` / `B-tool.txt` | `MUTATE: DONE … killed=8 survived=2 … 80%`; `MUTATE_RESTORE: OK` before = after |
| SHA256SUMS verification | 43/43 in-repo files match; report mismatch is the append-only note |
| report prefix hash | `e1b7ea07…` = SHA256SUMS entry; full file `f94e0c0a…` |
| `grep -n "Box 3 remains"` snapshot | 1472: ``Box 3 remains `[ ]` `` |
| `git show HEAD:SHONEN.md` | line 9 `[~]`, scope note as quoted |
| `git diff --stat -- SHONEN.md` | empty (working tree = HEAD) |
| validator on a synthetic 51-entry ledger | `LEDGER OK buckets=51 lines=1705`, exit 0; one corrupted section sha → `FAIL entry[3] … section sha mismatch`, exit 1 |

## 8. Opened (this seat)

`reports/round-1-kaika-coldread.md`; `SCORECARD.md:55-110,140-190,189-263,230-330,300-340`;
`SHONEN.md`; `corpus/QUALITY.md`; `corpus/lessons/round-1-verifier-spotcheck.md`;
`corpus/lessons/round-1.md:70-130,440-500`;
`.ufo/evidence/round-16/coldread/SKILL.snapshot.md` (hash + headings + cited
record sections only); `.ufo/evidence/kaika-round-1/coldread/` (all files
listed above; `probe-fixtures/` contents); `.ufo/waves/round-16/w1/swarm-registry.json`
(seat entry); `/home/vgpnk/Projects/shokunin/PROTOCOL.md:55-75,335-350`;
git metadata for `4eb4cf3`, `HEAD`, `SHONEN.md`, `c7986cd`, `121696b`.
Not opened: `LOG.md`, `SKILL.md` body outside the snapshot, `plans/`, other
seats' reports, `reports/round-1-calibration.md`. A lane-wide grep matched the
ledger schema string in `.ufo/waves/round-16/spec1.json` and `dispatch1.json`;
those files were not opened beyond the grep match.

This seat has no assigned cold-read range. The mandatory block below is
schema-valid with zero sections and must not be counted as coverage.

```json
{"seat":"CRRevenger","skill_sha256":"97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580","sections":[]}
```
