# T48ScoutConsiderthese — considerthese proposal pick (round 48, w1)

Read-only. Source: `considerthese/2026-10-25.md` (latest file; `ls considerthese/` = 10-19, 20, 22, 23, 24, 25), section `Self-improvement ideas` (5 proposals) and `Status of earlier ideas`. No tool installed; no counter run; scratch dir deleted.

## Already mined (grep `considerthese/2026-10-25` in `corpus/lessons/round-4[4-7].md`, `corpus/QUALITY.md`; `QUALITY.md` is at `corpus/QUALITY.md`, not the lane root)

| # | proposal | mined in | lands as |
|---|---|---|---|
| 1 | measured-to-landing drift check | round 45 (`round-45.md:130`) | QUALITY 86 (85 reserved) |
| 2 | cumulative mismatch-class regression run | round 46 (`round-46.md:101`) | lesson table (hits 3/0/2/2 for rounds 41-44, no class regressed) |
| 3 | dead-code debt list | round 47 (`round-47.md:92`) | scan `T47ExecDeadCode.scan.py`: `unreferenced=2`, nothing deleted |
| 4 | round tempo and capacity readout | **unmined** | — |
| 5 | proposal uptake ledger | **unmined** | — |

(The assignment says round 46 mined 2 and round 47 mined 3; the files say 1→r45, 2→r46, 3→r47. `QUALITY.md` has no `considerthese/2026-10-25` line other than 86's citation at `corpus/QUALITY.md:1174`.)

## Pick: proposal 5 (uptake ledger). Proposal 4 is rejected on evidence.

Why not 4: its input (elapsed time per round) is not recoverable from the lane repo. Commit timestamps are rewritten by the orchestrator: `git log` shows pairs of commits with the same second (`473336d`/`e73389c` both 2026-10-26 01:11:52; `0b5b7cd`/`9acfbe2` 2026-10-25 20:26:58; `683eedd`/`745a583` 17:45:21; `5891bdb`/`3310e7b` 10:28:28). A first-to-last-commit span per `round-N:` subject gives 0.3 h for rounds 36/38/39 and 0.5-0.6 h for 42-44, which contradicts the reflection's "seven rounds in about 26 hours". Seat counts (`ls .ufo/waves/round-N/w1 w2 | grep -c '\.md$'`: r40 65, r41 40, r42 84, r43 68, r44 33, r45 82, r46 75, r47 48) include non-seat files, so they are an upper bound. A tempo table would be built on numbers the lane cannot back.

Why 5 fits: it can be answered with real data, and it touches both claims.

- C2 (freshness): the 10-24 proposal 3 became QUALITY 79 (a located quote needs a committed snapshot), and its worked case was S108. S108 is a round-48 C2 target. Round 48 is the first round where criterion 79 is exercised on a target that previously had no re-fetch receipt. Live probe today (read-only, 7 fetches of `https://www.tensorflow.org/federated/golden_tests?hl=zh-cn`, HTTP 200, 0 redirects): 7 distinct raw sha256 prefixes (`dede6ebd`, `e0e67e9f`, `4db4d6db`, `f74006f9`, `2205dfaf`, `735ce737` plus the earlier `b070140e`), sizes 104924 / 111405 / 111409 bytes; after the contract's amendment-2 extraction (drop script/style, strip tags, unescape, collapse whitespace) there are exactly two text variants among the six fetches extracted, 3496 chars (sha `e83fc1ba`, four fetches) and 3148 chars (sha `a3f8a938`, two fetches); `--update_goldens` and `如何更新 .expected 文件` are present in every variant. The round-40 snapshot (`.ufo/evidence/round-40/s108/golden_tests.zh-cn.html`, 111405 bytes, sha `f27cf274…`) extracts to the 3496-char variant. Consequence for C2: a live check that compares raw bytes, or demands a byte-identical double fetch for S108, would be flaky by construction; the round-48 receipt must tie the snapshot to its own fetch (as the contract's `sha256 equal to the snapshot's` does) and any live check must be phrase-based. The same probe confirms S093's bytes are stable (raw `bwrap.xml` v0.13.1: 33289 bytes, sha prefix `2cb77df2`, equal to the SOURCES.md digest) and S048's page returns 200 (8892 bytes) and S026's returns 200 (236387 bytes; round-46 already records its live bytes differ from the snapshot).
- C1 (calibration): the same readout shows which criteria fired on real data after landing (below). 86 fired three further rounds and the round-47 closure still passed a tail commit touching `SCORECARD.md` ("records, no counted surface", `round-47-verifier-spotcheck.md:16`), i.e. an applied criterion whose strict form was relaxed by the closure; that is exactly the unrepeated-standing-value pattern C1 targets.

### Uptake ledger (data; `grep -lE "(criterion|QUALITY) N\b" corpus/lessons/*.md`; waves/evidence not searched, so "fired" is a lower bound)

| proposal | absorbed as (round) | lessons/spot-checks citing the criterion afterwards | fired on real data after its own round |
|---|---|---|---|
| 10-24 p1 pin blast radius | QUALITY 80 (r41) | r41 spot-check only | no later citation; round-48 contract amendments 1-3 do not name 80 |
| 10-24 p2 unreachable provenance | QUALITY 76 (r38) | r38 + its spot-check only | no later citation |
| 10-24 p3 persistently unreachable sources | QUALITY 79 (r39/r40) | r40 spot-check, r42, r47 | yes: r42 coverage row, r47 (`round-47.md:105`, 79 and 87 fold U+2013, the defect that became 91), r48 C2 targets S108 |
| 10-24 p4 attempt/dispatch health | QUALITY 78 (r39) | r39 + spot-check only | no later citation in lessons |
| 10-24 p5 SHONEN readiness | r42 lesson table | — | SHONEN boxes still `[~]` (operator decision) |
| 10-25 p1 drift check | QUALITY 86 (r45) | r45, r46 + spot-check, r47 spot-check | yes, three rounds (receipts-only tail) |
| 10-25 p2 regression run | r46 lesson table | — | yes as data: 5 false positives, 0 regressions |
| 10-25 p3 dead-code list | r47 scan | — | yes: finds `brace_depth_at` x2, nothing deleted |

Reading: of 8 absorbed proposals, 3 carry later-round citations (79, 86, and the r46/r47 scans as data), 3 criteria (76, 78, 80) have no citation after the round that wrote them. The kind of proposal that fired: ones whose object recurs every round (quotes, landing commits). Ones about a one-off past incident (an emptied-panel commit, a dispatch death, a three-pin deferral) did not.

## Draft lesson section (for `corpus/lessons/round-48.md`)

```markdown
### considerthese — `considerthese/2026-10-25.md` idea 5 (proposal uptake ledger)

Operator-authored, read-only. Ideas 1-3 were mined in rounds 45-47; idea 4 (tempo and capacity readout) is not mined and is not buildable
from the repo: commit timestamps are rewritten by the orchestrator (`473336d` and `e73389c` share 2026-10-26 01:11:52; three more pairs
share a second), so no per-round elapsed time can be derived (`w1/T48ScoutConsiderthese.md`). Idea 5 is mined as a table, not a tool:
of the eight absorbed proposals (10-24 p1-p5, 10-25 p1-p3), criteria 79 and 86 were cited in later rounds' lessons and spot-checks, and criteria 76, 78
and 80 were not cited after the round that wrote them (`grep -lE "(criterion|QUALITY) N\b" corpus/lessons/*.md`; waves and evidence are not searched,
so this is a lower bound). Proposals about a thing that recurs every round (a quote, a landing commit) fired; proposals about a one-off past incident did not.
Round 48 exercises criterion 79 on S108: seven live fetches of the zh-cn page returned HTTP 200 with seven distinct raw sha256 values
(104924, 111405 or 111409 bytes) and, after the amendment-2 extraction of six of them, two text variants (3496 and 3148 characters), both carrying `--update_goldens`;
the round-40 snapshot extracts to the 3496-character one. The snapshot is therefore the only carrier a quote can be located in: the S108 row's receipt
is bound to the snapshot's own fetch, and no round-48 check treats a second live fetch as byte-identical. Lands as: this lesson section; no QUALITY
criterion (the table has no falsifier a counter could pin) and no SOURCES row.
```

Lands as: lesson section only. No criterion, because the "fired" column is a lower bound built from lesson text, not a counted surface; no SOURCES row (nothing new is mined).

## Caveats / unresolved

- Whether 76/78/80 fired in wave or evidence files was not searched; the table says lower bound.
- Round 48's C2 counter and S108 receipt were not seen (not built yet); the S108 note should be rechecked against the delivered receipt and the deciding live check before the lesson ships.
- If the L1 prefers not to mine at all: nothing in 10-25 proposals 4-5 is a C1 or C2 deliverable; this section is a lesson-only addition and costs no claim surface.
