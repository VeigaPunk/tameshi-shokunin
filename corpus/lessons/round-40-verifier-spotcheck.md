author: hyaku closure (non-author integrator, @m_swe)
lane: tameshi · round: 40 · reviewer: Kimi fresh closure agent (non-author; did not author this round; not the @m_swe session)
date: 2026-10-24 · base `304e3355705640af2879c772fc9a5c2902c61763` → tip `46781274ea882274892dc1dbe81a07b7aee40e25`
measured commit `5641ed84c8dc148c34c8dd83f062279ddf06b4af` · fleet report `980dbb9177e8b14ce85d031d20dc4f84e2faecad`

Independent non-author closure. Nothing here is copied from the round's own report: every number
below was produced by a command I ran at closure time, and every command is quoted with the output
it printed. The round was not improved; defects are named in `## Routed defects` and are
status-neutral.

## Step-1 conformance

- Report `.ufo/reports/round-40/tameshi.md` is committed in the fleet repo under the lane identity:
  `git log --format='%an %H' -- .ufo/reports/round-40/tameshi.md` → `tameshi-shokunin
  980dbb9177e8b14ce85d031d20dc4f84e2faecad`; `git show --stat` on it touches that one path only
  (117 lines added), and it is an ancestor of fleet `HEAD` (`6b403b305a0b33b6834a32038b312f062e5bdd8b`).
  It is a real report, not a marker: it carries before→after measurements, a Sources & frontier
  section, three trend verdicts and a `## SHONEN` heading with one `[~]` line per box (4 boxes, no
  `[x]`).
- Cited lane commits exist and `git -C tameshi-shokunin merge-base --is-ancestor <hash> master`
  holds for `46781274ea882274892dc1dbe81a07b7aee40e25` (tip), `5641ed84c8dc148c34c8dd83f062279ddf06b4af`
  (freeze), `304e3355705640af2879c772fc9a5c2902c61763` (base) and `31687496b5f34b153626e123d12ae2febdbd86a0`
  (the revision the S137 flip names). Ancestry was tested against the branch ref `master`, never
  `@{u}`: the lane repo is jj-colocated and `git HEAD` is detached at the same commit.
  Both round-40 lane commits carry the lane identity
  `tameshi-shokunin <tameshi@shokunin.local>`.
- `scripts/hyaku/jj-lane.sh state tameshi-shokunin` → `state branch=master
  local=46781274ea882274892dc1dbe81a07b7aee40e25 remote=46781274ea882274892dc1dbe81a07b7aee40e25
  ahead=0 behind=0 head=detached tracked=0 untracked=0`. `git -C tameshi-shokunin status --porcelain`
  is empty (no uncommitted round work, no leftovers). `git -C tameshi-shokunin ls-remote origin
  refs/heads/master` → `46781274ea882274892dc1dbe81a07b7aee40e25` (the tip is pushed).
- Dispatched prompt `.ufo/prompts/tameshi-round-40.md` carries the template contract: `diff` against
  `templates/round-prompt.md` shows only placeholder substitution (`{{LANE}}`, `{{ROUND}}`,
  `{{FLEET_ROOT}}`) across all 140 template lines, plus the hyaku addendum §6. The five child-lane
  items are present — report path and filename (`§4`), commit-before-report ordering (`§4`, `§5`),
  the `SHONEN` heading requirement (`§4`), the commit-hash citation rule (`§4`, `§5`) and the lane
  write scope (`§5`).
- Driver digest (`.ufo/watchdog.log` is mutable; this is the copy):
  `2026-10-24T21:34:39-03:00 launch tameshi round=40 pgid=3086320 driver=hyaku-inline attempt=1` →
  `2026-10-24T22:36:57-03:00 complete tameshi round=40; hyaku-inline attempt=1`.
- L0 `d0531d78` (full id `d0531d7861011830e6f43f96fd60fc37b6d72f5a`) is the round-38 wave-dispatch
  question, filed once in `.ufo/l0-questions.md`. It was not re-filed here: `grep -c d0531d78
  .ufo/l0-questions.md` → `0`, and no `tameshi | round-40` line exists in that file. This closure
  does not duplicate it.
- Attempt inheritance is disclosed, not silent: the report's attempt note and the `LOG.md`
  "resumed L1 (attempt 1 continued, provider-route failure on the first L1)" subsection both say the
  first L1 died after the freeze commit and during the wave, and that its uncommitted outputs were
  inherited and dispositioned.

## Freeze integrity — the inherited freeze commit was not rewritten

The round claims the freeze commit `5641ed84` was inherited from the dead predecessor and verified
rather than rewritten. Checked by blob identity, not by prose:

```
git rev-parse 5641ed84:<path>   vs   git rev-parse 46781274:<path>
.ufo/evidence/round-40/contract.json            0f012e56225a  0f012e56225a  SAME
.ufo/evidence/round-40/census/measure.py        ed95d236b072  ed95d236b072  SAME
.ufo/evidence/round-40/census/fixtures.json     499b53d88665  499b53d88665  SAME
.ufo/evidence/round-40/s108/measure.py          fb0e0c8cb3d2  fb0e0c8cb3d2  SAME
.ufo/evidence/round-40/s108/golden_tests.zh-cn.html
                                                54e4c8aed404  54e4c8aed404  SAME
tools/write-path-census-v2.py                   87baff20cca8  87baff20cca8  SAME
tools/write-path-census.py                      6cb647acf9cf  6cb647acf9cf  SAME
```

`5641ed84` is a direct child of the base (`git rev-list --parents -n 1 5641ed84` →
`5641ed84… 304e3355…`), so the freeze sits exactly where the round says, and no frozen byte moved
between the freeze and the tip. The contract's `base_rev` is `304e3355…` and
`frozen_before_any_seat_score: true`. Two jj-internal working-copy commits (`62f89b0`, `8f58ddf`,
same author and timestamp, unreferenced by any branch, `merge-base --is-ancestor … master` → no)
carry the *same* lesson blob (`c4c65c40fa5e…`) as the tip, so no earlier draft of the lesson was
published and then rewritten in place.

## Claims — re-measured by me (both counters re-run at base, measured commit and tip)

```
python3 .ufo/evidence/round-40/census/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV
python3 .ufo/evidence/round-40/s108/measure.py   --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev REV
```

### C1 — depth (capability acquisition): VERIFIED → improved

- Base `304e3355…`: `C1_R40: tool_absent=1 bytes_unflagged=0 replace_unflagged=0
  v1_bytes_unflagged=0 v1_replace_writes=0 rev=304e3355705640af2879c772fc9a5c2902c61763
  C1_R40_PASS=false`, exit 1.
- Measured `5641ed84…` and tip `46781274…`: `C1_R40: tool_absent=0 tool_sha_ok=1 v1_sha_ok=1
  bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0
  v1_bytes_unflagged=0 v1_replace_writes=0 live_json_v2=1 live_json_v1=0 live_replace_v2=1
  live_replace_v1=0 mutant_replace_killed=1 mutant_json_killed=1 rev=<rev> C1_R40_PASS=true`, exit 0.
  Identical lines at both revisions, and byte-identical to the committed receipts
  `.ufo/evidence/round-40/before/c1-at-base.stdout` and `.ufo/evidence/round-40/after/c1-at-5641ed84.stdout`.
- Do-nothing cannot pass: the base run is `tool_absent=1`, and the v1-pattern control on the planted
  fixtures is `C1_R40_CONTROL: v1_bytes_unflagged=0 v1_replace_writes=0 v1_replace_unflagged=0
  C1_R40_CONTROL_PASS=false`, exit 1 (I re-ran it: same line, same exit).
- The two recognizer-removal mutants are killed (`mutant_replace_killed=1 mutant_json_killed=1`),
  so the two new classes are load-bearing in the tool, not in the report's wording.
- The v1 tool pin did not move: `sha256sum tools/write-path-census.py` →
  `bc8c660c56f871f85dad8912be28446293fd63f62b4fd1c16eb153f7a27edc62`, and the counter's own
  `v1_sha_ok=1` at both revisions.
- The v2 `WRITE_RE` (read from the tool source) covers `open(...w|a…)`, `.write_text(`,
  `.write_bytes(`, `os.replace(` and `os.rename(`. It does **not** cover `os.symlink`, `os.link`,
  `Path.symlink_to`, `Path.rename`, `shutil.*`, `os.remove/unlink` or `handle.write`, and the tool
  makes no universality claim — its docstring says only "Sees two write forms the round-39 pattern
  misses". The gap is real and disclosed: `tools/repeat-control.py` lines 807–823 write
  `expected.json` through a variable path (`duplicate_path = os.path.join(...)`) and create it
  through `os.symlink`, neither of which v2 sees. The lesson's `## Holds` records this. The
  disclosure is accurate; the predicate was not widened after the freeze.
- C1 is not an exploratory claim, so no `unprovable-but-better` judgment is needed; the verdict is
  measured, not self-asserted.

### C2 — freshness (source pin for the S108 quote): VERIFIED → improved

- Base `304e3355…`: `C2_R40: snapshot_absent=1 quote_in_snapshot=0 sha_ok=0 stripped_quote_fails=0
  rev=304e3355705640af2879c772fc9a5c2902c61763 C2_R40_PASS=false`, exit 1.
- Measured `5641ed84…` and tip `46781274…`: `C2_R40: snapshot_absent=0 quote_in_snapshot=1 sha_ok=1
  stripped_quote_fails=1 rev=<rev> C2_R40_PASS=true`, exit 0 — identical to the committed receipts
  `.ufo/evidence/round-40/before/c2-at-base.stdout` and `.ufo/evidence/round-40/after/c2-at-5641ed84.stdout`.
- Independent of the counter, from the blob at the tip: 111405 bytes;
  `sha256` = `f27cf274b5dd7c28122dcb5a137971b401dad7910f7702eb4cbd3c28cd782bf0` (matches the pin in
  `contract.json` and in the SOURCES/knowledge rows); `<title>黄金测试 | TensorFlow Federated</title>`;
  `lang="zh-CN"` present.
- The quote shape is exactly as reported: the frozen quote
  `可以通过使用参数 --test_arg=--update_goldens --test_strategy=local 运行受影响的测试目标来更新 .expected 文件。`
  is **not** a contiguous raw byte string in the snapshot (I searched the raw blob: absent) but **is**
  contiguous in the tag-stripped text (present). The page wraps the flag and `.expected` in `<code>`
  tags.
- The falsifier fires: replacing the prefix `可以通过使用参数` in a copy of the blob makes the quote
  miss in the tag-stripped text, so `stripped_quote_fails=1` on the green run is load-bearing and
  not a tautology.
- The S108 row itself is untouched: `git diff 304e3355 46781274 -- corpus/SOURCES.md` shows two
  appended rows only; S108 keeps `status=mined`, `recheck=180d`, `used-by
  corpus/knowledge/r8-golden-update-flag.md`. The round-39 routed item is answered with committed
  bytes, not with a status edit.

### No-harm re-measurement (base, measured commit and tip)

```
D: git show "$REV:tools/mutate-and-run.sh" | python3 -c '… recorded_cases / depth_score'
   304e3355 → recorded_cases=9 depth_score=9
   5641ed84 → recorded_cases=9 depth_score=9
   46781274 → recorded_cases=9 depth_score=9
C: git show "$REV:SHONEN.md" | python3 -c '… boxes / checked / asserted / untouched'
   304e3355 → boxes=4 checked=0 asserted=4 untouched=0
   5641ed84 → boxes=4 checked=0 asserted=4 untouched=0
   46781274 → boxes=4 checked=0 asserted=4 untouched=0
```

`git diff 304e3355 46781274 -- SCORECARD.md` shows one appended round-40 block: depth 9 → 9,
calibration 8 → 8, one new capability row (`write-path-census-v2`), no other axis touched.
`git diff --stat 304e3355 46781274 -- SHONEN.md` is empty (no box moved). `grep -cE '^\s*leg'
tools/mutate-and-run.sh` → `0`: the round-38 vacuous depth regex is still vacuous and still
unchanged — routed, not re-broken. `LOG.md` grew by 23 added lines and 0 removed lines
(append-only).

## Wave reconciliation — from registries and reports, not prose

- `swarm-registry.json` holds exactly 64 members. Roles counted from the registry:
  connector 1, scout 8, executor 6, scribe 3, sentinel 1, revenger 1, simplifier 1, reviewer 20,
  critic 12, mutation-tester 11 — the same split the report states. Attack roles (reviewer, critic,
  mutation-tester) = 43/64 = 67.1875 % ≈ 67.2 %. No `planner` member.
- 64 seat report files exist under `.ufo/waves/round-40/w1/`; I checked each for emptiness (none
  empty) and the set maps 1:1 onto the registry — no member without a report, no report without a
  member. `settlement-receipt.json` carries `registry_members: 64`, `seat_exits: 64`,
  `reports_present: 64`, `dead_seats: 0`.
- `dispatch-w1.json` carries exactly one `taskCall` with 64 tasks and `counts {spawn: 64, resume: 0,
  total: 64}`; `resumeSends` is empty. One wave directory (`w1`) exists, and the band is right:
  `scripts/hyaku/ufo-wave-policy-v2.json` has `waveMinLanes 64`, `waveMaxLanes 128`; 64 seats is
  inside it, and the wave was not padded or split.
- Settlement, from the OMP log `/home/vgpnk/.omp/logs/omp.2026-10-24.3225220.log`: 65
  `Session exit recorded` lines — 64 seats plus the parent — every one `kind=normal`,
  `reason=dispose`, `pendingToolCalls=0`, 65 distinct session names, no duplicate. Last seat
  terminal `2026-10-24T22:02:36.564-03:00`; parent exit `2026-10-24T22:02:36.574-03:00`; the
  delta I computed is **+10 ms** (0 s at unix-second resolution, as the receipt's equal
  `1792890156` values imply).
- `python3 tools/wave-parent-settle.py --receipt .ufo/waves/round-40/settlement-receipt.json` →
  `WAVE_PARENT: verdict=SETTLED detail=parent exit >= last seat terminal`, exit 0.
  `python3 tools/wave-parent-settle.py --selftest` → `WAVE_PARENT_SELFTEST: 3/3 pass`, exit 0; the
  red fixture (parent exit 10, seat terminal 20) is classified `UNSETTLED` by the tool's own
  `classify()`, which I read in the source.
- One claim does **not** resolve at closure time: the report's grant pointer
  `1792889233 64 tameshi round-40-w1` in `~/.local/state/shokunin-hyaku/wave-slots`. The ledger
  deletes a lane/wave line on release by design (`scripts/hyaku/wave-slot.sh` release path), so the
  line is absent now. The grant itself is corroborated by the committed receipt
  (`parent_start_unix 1792889248`, 15 s after the claimed grant) and by the OMP log, but the cited
  ledger line is a transient runtime pointer, not closure-time-resolvable evidence. Routed below.

## Assimilation (prompt item 10) — what landed and what was refused

- Registry delta is exactly two appended rows: `S132` (tier A) and `S152` (tier B). Row count
  105 → 107 by `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'`. No existing row's `status`, `recheck`
  or `used-by` cell changed — the diff shows only the two `+` lines.
- Table normalization holds: `awk -F'|' '{print NF}'` over `corpus/SOURCES.md` at the tip gives 109
  lines at 13 fields (107 data rows + header + separator) and nothing else at 13 for a data row. No
  cell carries a literal or escaped pipe. `used-by` is restricted to the admitted entries that cite
  the row: S132 → `corpus/knowledge/r3-snapshot-fixture-update-paths.md`; S152 →
  `corpus/knowledge/r6-snapshot-practice-corpus.md`, `corpus/knowledge/r40-write-form-misses.md`.
  Both paths exist. `recheck` is normalized to `365d` on both rows; `opened` is this round's access
  date `2026-10-24`, not the campaign's `2026-10-23`.
- Validate-before-append: the mirrored scratch tree
  `.ufo/waves/round-40/assimilation/validate/corpus/SOURCES.md` is byte-identical to the landed
  `corpus/SOURCES.md`, and its committed receipt `census-scratch.exit` is `0` with the W01/W04
  warning set only — no E03/E04 on the new rows. Live
  `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` → exit 0,
  `ok`, the same ten W01/W04 warnings; the same set at the base revision — the new rows add no
  warning.
- Id-collision guard: `reg-ids` (105 ids, ending S108) and `staged-ids` (`S132`, `S152`) have an
  empty `collisions` file, and the renumber map is empty. The guard is proven, not asserted: the
  scratch proof shows a column-zero-only pattern finding nothing (`col0-ids` empty) while the
  0–3-space extractor catches the indented row (`collisions` = `S132`).
- The staged S137 (`r4-gate-write-path-audit`) was refused with a flip condition, and the flip is
  still unmet — I checked the revision the flip names: `git show --stat 31687496` touches two
  round-35 receipt files only; `git cat-file -e 31687496:tools/write-path-census.py` → absent; no
  write-path census artefact exists in that tree. The refuse is correct.
- The external campaign root was not written by this lane: `/home/vgpnk/Projects/shokuknow`'s
  register `absent-defect-register.md` is byte-identical to its HEAD and untouched since 08:37, and
  `merge/tameshi/` has no file modified inside the tameshi wave window (newest package mtime
  21:17:10, the wave started 21:47:13). The seat reports read the campaign outputs; one seat states
  it did not re-run the campaign's `quote-lint`.
- `considerthese/2026-10-24.md` was not edited (`git diff 304e3355 46781274 -- considerthese/` is
  empty). Its proposal 3 is "Persistently unreachable sources … suggest pinned alternatives",
  which is what QUALITY criterion 79 generalises; the criterion names the round-40 lesson, the
  proposal, and a falsifier that fails at the base revision (I ran it: `snapshot_absent=1
  C2_R40_PASS=false`, exit 1).
- S108 was **not** used as support for the new write-form entry: `corpus/knowledge/r40-write-form-misses.md`
  opens `source: S152 — …`, and states "S108 is not support for this entry". The entry's own
  "What is not claimed" paragraph refuses both universality and the `os.replace` destination
  claim.

## Discernment spot-check (LEARNING.md — checked from outside)

I re-opened five gate decisions, two admits and two rejects plus one present-but-not-appended row,
from the source each verdict rests on.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S152 → `corpus/knowledge/r6-snapshot-practice-corpus.md` | admit | live PDF `https://repositorio.ufmg.br/bitstreams/271f8a97-e79d-4935-86fd-33515a3073ad/download` (HTTP 200, 1474183 bytes, sha256 `65f9603f364d9e811312600b0a161943cdae09fe1dbd53dbe4f19e0699a89703`) and the committed excerpt `.ufo/evidence/round-40/sources/s152-excerpt.txt` | agree | The live digest equals the digest the row and the entry pin. The quote "drawbacks such as fragility and lack of context can lead to false positives" is present verbatim in the committed excerpt; the entry refuses the campaign's 569-project figure and claims no gate count. ≤25 words: yes. |
| S132 → `corpus/knowledge/r3-snapshot-fixture-update-paths.md` | admit | live raw README `https://raw.githubusercontent.com/VictorGazzinelli/snapshot-testing/master/README.md` (HTTP 200, 10269 bytes, sha256 `8871d19c34165b60b5847f390955c247d8665758ecddb206448127bf3b1922ea`) and committed snapshot `.ufo/evidence/round-40/sources/s132-readme.md` | agree | The live digest equals the pinned snapshot digest, so the pin is current, not stale. Row D29's title cell reads "Snapshot Testing: Use With Care - Randy Coulman" verbatim; the entry claims only that title, and the ≤25-word located quote holds. |
| staged S137 → `r4-gate-write-path-audit` | reject | `git show 31687496b5f34b153626e123d12ae2febdbd86a0` | agree | The commit touches two round-35 receipt files; `tools/write-path-census.py` is absent at that revision and no write-path census artefact exists there. The flip condition ("locates a write-path census artefact at that revision whose counts reproduce") is unmet, so the refusal stands. |
| S143 | reject | lane repo at `31687496` (source: `https://github.com/VeigaPunk/tameshi-shokunin`) | agree | `git grep -c "mavis-trash" 31687496` returns nothing — the quoted payload is in none of the cited tree. The source is live but the quote is absent: refusal, not fabrication. |
| S105 | present, not appended | live `https://pubs.opengroup.org/onlinepubs/9699919799/utilities/diff.html` (HTTP 200, 33988 bytes) | agree | The three exit-status phrases are present verbatim and in order ("0 No differences were found. 1 Differences were found. >1 An error occurred."), so the register's `payload-absent` class is a whitespace-fold artifact. "Present but not appended" is the right verdict: no admitted entry cites S105. |

S108 (the row the round-39 closure could not re-open) was re-opened through its new committed
snapshot rather than the live page: 111405 bytes, sha256 `f27cf274…`, the quote contiguous in the
tag-stripped text and absent from the raw bytes, the prefix-removal falsifier firing. That is the
r39 routed item answered with committed bytes.

The gate block's own per-row table is internally consistent and matches the report: one row adopted
(S132), six refused (S109, S131, S137, S140, S141, S143), ten present-but-not-appended (S105, S110,
S113, S118, S119, S123, S124, S126, S129, S134) — 17 rows, one verdict each, one seat pointer each.
The lesson's closing summary sentence does **not** match that table; see routed defect 1.

## Axis verdicts

- depth: **improved** (C1 re-measured at base/measured/tip; capability row `write-path-census-v2`
  admitted with a demonstrated run; numeric depth stays 9).
- calibration: **unchanged** (numeric calibration stays 8; SHONEN remains four `[~]` lane assertions
  and no box moved; the round's disclosed limits — the `os.symlink`/`handle.write` coverage gap and
  the live-site matching shortcut — are named honestly in the report, the SCORECARD and the lesson's
  `## Holds`).
- freshness: **improved** (C2 re-measured; the S108 quote became citable from a pinned committed
  snapshot, which answers the round-39 routed item — an owned-but-unscored surface, not a numeric
  score move).
- coverage: unchanged. operability: unchanged. adjacency: unchanged (the SENTINEL/SCOPE seats found
  no cross-domain bleed; `PROVINCE.md` was not touched).
- No axis is harmed, so the round is admissible under the protocol's admission rule. Neither claim is
  exploratory; no `unprovable-but-better` verdict is used anywhere in this closure.

## Trend verdicts

- **expansion: improved.** Two package knowledge entries (`r3-snapshot-fixture-update-paths.md`,
  `r6-snapshot-practice-corpus.md`) and one lane-authored entry (`r40-write-form-misses.md`) landed
  on F4 snapshot-practice ground the lane's coverage map did not hold, and the coverage map
  (`corpus/README.md`) grew by two rows. The registry count 105 → 107 is the row count, not the
  expansion measurement; the expansion is the new entry surface and the instrument behind it.
- **quality: improved.** The round-39 vacuous-pattern limit has a successor instrument that fails
  the do-nothing path (`tool_absent=1`, exit 1), fails the v1 patterns on the planted fixtures
  (`C1_R40_CONTROL_PASS=false`, exit 1), and fails both recognizer-removal mutants
  (`mutant_replace_killed=1 mutant_json_killed=1`). The tool is pinned by sha256, so a hardcoding
  tool cannot forge the pass. Both admitted entries were re-opened live by me and their pinned
  digests still match. Staged rows were transformed and census-validated in scratch before the
  append, and the new rows carry no census error.
- **discernment: improved.** The gate records one admit-of-a-row, six refuses and ten
  present-but-not-appended, each with a reason and, where refused, a flip condition; the three
  prose-class rows the inherited draft called unreachable were re-checked and corrected after seats
  falsified the draft, and the correction is disclosed in the lesson's `## Mistakes` row
  `draft-summary-drift` and in the report's attempt note. My outside spot-check agrees with every
  decision I re-opened (two admits, two refuses, one present-not-appended). Criterion 79 has a
  falsifier that fails at the base revision.

## Routed defects (status-neutral; the lane fixes these next round)

1. **The lesson's quarantine summary contradicts its own table.**
   `corpus/lessons/round-40.md` closes the Gate block with "One row adopted, seven refused (S109,
   S131, S137, S140, S141, S143 and the two prose-class rows whose premise a seat falsified), nine
   present-but-not-appended." The table in the same file, and the report's Sources & frontier
   section, both say **one adopted, six refused, ten present-but-not-appended** (17 rows either
   way). The sentence also names eight rows under the word "seven" and says "two prose-class rows"
   where the table marks three (S113, S123, S134). This is a leftover of the very
   `draft-summary-drift` class the lesson mines: the table was rewritten from the seat reports, the
   summary sentence was not. Fix by an appended correction in the round-41 lesson — do not rewrite
   the closed round-40 file in place.
2. **The wave grant pointer does not resolve at closure time.** The report cites the seat-ledger
   line `1792889233 64 tameshi round-40-w1` in `~/.local/state/shokunin-hyaku/wave-slots`, but the
   release path deletes that line by design, so a reviewer at closure cannot re-check it. Cite a
   durable artefact instead (the committed `settlement-receipt.json` and the OMP log both carry the
   wave's timing).
3. **Item 10 asked for both id lists to be pasted into the report.** They are committed as wave
   evidence (`.ufo/waves/round-40/assimilation/reg-ids`, 105 ids, and `staged-ids`, 2 ids) and the
   report cites the collision count and the empty renumber map, but the 105-id list itself is not
   pasted into the report text.
4. **Word-count slip on the S152 quote.** The lesson and the seat brief label the quoted string
   "11 words"; it has 13 tokens. The quote itself is verbatim and correct — only the label is off.
5. **The round-38 vacuous depth guard is still vacuous.** `^\s*leg` matches 0 lines of
   `tools/mutate-and-run.sh` (I re-checked). Round 40 does not use that regex and does not re-break
   it, but the round-38 routing stays open until a guard that can fail replaces it.

SHONEN: the four boxes remain `[~]` — lane assertions, no independent promotion verifier this round.
This closure did not write `[x]` into `SHONEN.md` and did not audit the boxes for promotion;
promotion is operator-owned.
