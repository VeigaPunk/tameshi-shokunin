author: hyaku closure (non-author integrator, zcode subagent (fresh session, non-author))

# tameshi round 61 — verifier spot-check (closure)

Base `8b0042bde0ca59aac9a23a8a707cf0902183d081`, tip `b82d61f030414174e0ca7b1671bddb9db4048c05`
(branch `master`, pushed). Recovery round after r60's rejected-honest-stop. Every command below
was run by this verifier at closure time (2026-11-01, win32 host) against committed bytes
(`git show <rev>:<path>`); index-free git only, no lane file edited.

## 1. Step-1 conformance

| Check | Result |
|---|---|
| Report committed by lane identity | PASS — `git log --format='%an <%ae> %H' -1 -- .ufo/reports/round-61/tameshi.md` → `tameshi-shokunin <tameshi@shokunin.local> ab9521f69ccafd9ab54db53d897aaf1a919a9361` |
| `SHONEN` heading in committed report | PASS — committed report carries `## SHONEN` with four `[~]` lines (grep count 1) |
| `SHONEN.md` not written by the round | PASS — `git diff-tree -r --stat base..tip -- SHONEN.md` empty; boxes remain `[~]`, no `[x]` |
| Cited lane commits exist + ancestors | PASS — all six (`19d7e996…`, `72d36ae1…`, `11f96a78…`, `0a29e3cf…`, `7a55de5a…`, `b82d61f0…`) `cat-file -e` + `merge-base --is-ancestor refs/heads/master` → ANCESTOR-OK ×6 |
| Tip pushed | PASS — `ls-remote origin refs/heads/master` = `b82d61f03041…` = local `refs/heads/master` |
| Round work reachable base..tip | PASS — exactly the six commits, all authored `tameshi-shokunin`, subjects match the report's table |
| Prompt fidelity | PASS — dispatched prompt carries the round-level contract (MISSION/AXES binding, L2 minimum, commit-then-push, push scope, L0 channel) and all five child-lane items (report path, commit-before-report, SHONEN heading, hash citation, write scope) |
| Sources & frontier section | PASS — rows 152 → 153 with counting command; six mistakes with class/evidence/captured-by/fix; census before/after pasted; C1 sourced on the S289 re-open |
| PROVINCE.md untouched | PASS — `diff-tree base..tip -- PROVINCE.md` empty (claimed and true) |
| L2 floor | standing defect, status-neutral — no dispatch surface on this host; the r60 L0 question (`.ufo/l0-questions.md` line 230, routing with (b)) stands unanswered and is disclosed in the lesson and report |

## 2. Claim re-checks

### C1 — operability, capability acquisition: `tools/coldread-precheck-portable.py` (RE-MEASURED)

1. **Frozen decision code byte-unchanged — VERIFIED.** The tool loads
   `.ufo/evidence/round-18/measure.py` from the repo bytes and calls `module.coldread(...)` verbatim;
   only `module.cat_file_blob` / `module.ls_tree_mode` are monkey-patched with cache-backed wrappers
   that fall back to the original functions on any miss. Byte checks:
   - worktree `.ufo/evidence/round-18/measure.py` == tip bytes (cmp OK); selector + ledger also worktree==tip;
   - tip bytes == round-18 landing `9ee1c8046295baf6c133c8d43b8315d562498aea` (last commit that ever
     touched the file, 2026-10-20) — the frozen code is byte-identical to the r18 freeze;
   - tool sha256 at tip = `3e09cace27da2acc859143052c7bd4a5f8f1825737932afb67223729ec0c2fce` — matches
     the report and SCORECARD; `tools/` copy == `.ufo/evidence/round-61/win-host/` as-run copy.
   Cached-semantics review: `cached_mode` serves only real `ls-tree -r -z` values; `cached_blob` returns
   None for tracked non-blobs exactly as the spawn would (tree/gitlink), falls back to the spawn otherwise;
   misses always delegate to the ORIGINAL functions. The `precheck_line` verdict/LOST format matches the
   round-48 frozen shell's output format.
2. **Differential re-run — PASS (re-derived by this verifier).** Harness
   `.ufo/evidence/round-61/win-host/differential.py` (read in full first; builds a synthetic fixture repo
   in scratch, lane read-only) re-run with the tip tool bytes:
   ```
   DIFF rev=6d46cb2b credited=3/6 sections-match=OK probe_mismatches=0
   DIFF rev=7915b22d credited=2/6 sections-match=OK probe_mismatches=0
   DISCRIMINATORS at rev2:
     # lane           no-ledger-entry
     ## Section A     input-drift:inputs/one.txt
     ## Section B     credited            (exec-bit 100755)
     ## Section C     input-not-blob:inputs/sym.txt   (symlink 120000)
     ## Section D     input-missing:inputs/absent.txt
     ## Section E     credited
   DIFFERENTIAL: PASS (frozen selector == portable batched form)   [exit 0]
   ```
   Identical verdict and identical discriminator cells to the committed `differential.stdout`.
3. **Final guard re-run at the pushed tip — lost=0 ok (re-derived).**
   `python -I tools/coldread-precheck-portable.py --repo . --floor 8b0042bde0ca… --cand b82d61f0… --work WORK` →
   ```
   COLDREAD_PRECHECK floor=8b0042bde0ca floor_credited=46 cand=b82d61f03041 cand_credited=64 lost=0 ok
   EQUIVALENCE floor_sampled=20 floor_mismatches=0 cand_sampled=20 cand_mismatches=0   [exit 0]
   ```
   Stronger than the committed receipt (which measured cand=`7a55de5a`): this is floor vs the actual tip.
   Single-rev tip measure re-run: `COLDREAD_PORTABLE rev=b82d61f03041 credited=64/64 elapsed=8.9s
   probe_sampled=20 probe_mismatches=0`, box3_full_page=true (receipt captured at closure).
4. **Before→after honest.** Before-state receipt `.ufo/evidence/round-60/win-host/amend1/coldread-precheck.out`
   exists at the tip (five failed ~112-min runs); after: verdict in seconds. Capability row entered the
   SCORECARD capabilities table the same round with a demonstrated run. **C1 verifies** (re-measured).

### C2 — calibration: the r60 remedy rekey + guard verdict (RE-MEASURED + EVIDENCE-VERIFIED)

- Ledger counts re-derived: 644 (base, tool commit) → 662 (`72d36ae1`, +18 batch 1) → 680
  (`7a55de5a`/tip, +18 batch 2). Matches the report.
- Trace receipts: 18 files in `rekey/traces/` (batch 1) and 18 in `rekey/traces-2/` (batch 2). All 18
  batch-2 receipts programmatically checked: `schema=tameshi-trace-inputs-v1`, `rev=0a29e3cf…` (the
  SOURCES-corrected pin), `exit=0`, `inputs` == the ledger entry's `inputs` (all 18), and every entry
  `commands_executed_count>0` (sample entry: 4).
- Input pins: batch-1 sum = 11,004, batch-2 sum = 11,004 — matches "11,004 input pins per batch".
- Coverage: the 18 rekeyed headings (rekey-summary-b2 sections) are set-equal to the 18 uncredited
  sections at base (from `measure-base.json`). `skill_sha256` in both rekey summaries equals the
  sha256 of SKILL.md at pin `0a29e3cf` (recomputed: `b56c0252…`). Verdicts honestly graded:
  9 `verified-record` + 9 `gap-minor`; the round-21 registry section carries `minor_gaps=2` (the two
  spacing defects the re-read found) as reported.
- Two-batch story verified at sha level: batch-1 entries pin `corpus/SOURCES.md` at the pre-correction
  bytes (sha `29d5d21e…` == 19d7e996 bytes; ≠ tip `602ba1ae…`) — so at the tip the batch-1 entries
  genuinely read `input-drift:corpus/SOURCES.md`, non-crediting; batch-2 pins equal the tip bytes and
  credit. Both batches stay in the ledger (append-only), disclosed in lesson/SCORECARD/LOG.
- Guard verdict at tip: my own re-run above (`lost=0`, `cand_credited=64/64`, `box3_full_page=true`)
  reproduces the committed `precheck-final-b2` receipt. **C2 verifies** (re-measured).

### Closure-defect dispositions (evidence-verified in committed bytes)

- **D1 — PASS with a number-drift defect.** `first-family/` is committed at `19d7e996` and resolves at
  the tip; `ctl-sequence.out` carries `passed=1/8 C1_R60V2_PASS=false`, exactly the draw the lesson
  records. All six formerly-deferred pointer paths resolve at the tip (checked individually). Committed
  sweep `pointer-sweep-r61.json` at rev `19d7e996`: `resolved_count=19/19`, 6 deferred all
  `resolved: true` — this time the bytes are actually present (the r60 failure mode). Defect: the
  report, lesson, LOG and commit subject all say "21 files"; the committed tree holds **20**
  (10 `.out` + 10 `.err`, none elsewhere).
- **D2 — PASS.** `freeze-a1-reverify.json` at the tip: `instrument_total=10 instrument_match=10`,
  `verdict="INSTRUMENT-OK (receipts re-run)"`, 7 nonce-bearing control receipts re-run;
  `freeze-verify.py` itself is committed at `19d7e996`. Receipt verified as committed evidence
  (lane-owned instrument, not executed by this verifier).
- **D3 — PASS.** `git show 49ddecf1f15a:SCORECARD.md | grep -n 'counting command host-scoped (linux)'`
  → exactly `:2921 :2922 :2978 :2994` (count 4), matching the erratum's pinned decomposition; the
  EIGHT-control-arms erratum is pinned in SCORECARD at the tip (line ~3044).

### S293/S289 same-round duplicate handling — PASS

S293 opened then REJECTED the same round as a within-scope duplicate of the held S289, kept as the
rejection record per CORPUS.md rule 2 with reason and flip; S289 re-opened, `used-by` extended
old → new and logged in the lesson `## Gate`; census exit 0 with S293's W04 disclosed as the
rejection's marker. The pricing (batch-1 SOURCES pins staled → batch-2 rekey) is disclosed everywhere
it matters. This is the instrument catching the lane's own record edit, honestly carried.

## 3. Discernment spot-check (non-author)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S289 re-open (admit; tier A, mined) | re-open with batch-framing ground | Live `https://git-scm.com/docs/git-cat-file` (fetched at closure) + committed extract `.ufo/evidence/round-61/win-host/sources/s293-cat-file-batch.html` (79,360 B, HTTP date matches the row) | **agree** | §Output, `--batch` without a custom format reads verbatim `<oid> SP <type> SP <size> LF` / `<contents> LF` — the quote is accurate (the row joins the two lines with a space); it grounds the batched reader's parser exactly. Row quote ≤25 words. Trivial drift: the Gate prose says "12 words"; the quote is 8 tokens. |
| S293 reject | rejected as within-scope duplicate of S289 | Same URL; census `W04 S293 duplicate url git-scm.com/docs/git-cat-file across scopes` | **agree** | The URL was already held; CORPUS.md rule 2 keeps the rejection as a taste record with reason + flip; consistent with the S073/S103 precedent cited. |
| `--batch-check` as prefetch primitive (reject) | rejected — returns metadata only, no contents | Same extract + live page: "Whereas --batch-check='%(objectname) %(objecttype) would produce: `<oid> SP <type> LF`" | **agree** | The frozen decision code consumes blob BYTES (sha256 over content; trace receipts parsed from bytes), so a check-only prefetch still needs one spawn per input. Ground accurate. |
| New SOURCES row re-open (S293 row itself) | row + quote check | Extract line-verbatim (two-line framing); location §Output `--batch` | **agree** | No literal pipe in any cell (r60's E01 lesson respected); status `rejected`, tier A with the rejection scope noted. |

SOURCES census re-run at closure:
`bash scripts/sources-census.sh validate --root <fleet-root> tameshi` → **exit 0**, 153 rows,
17 W04 + 1 W01 (all pre-existing or the disclosed S293 rejection marker), no E-errors — matches the
reported round-end census.

## 4. Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| operability | **improved** | New capability `host-feasible no-harm precheck` demonstrated running and re-run by this verifier (differential PASS; guard lost=0 at tip; probes 20/0). Before-state (no verdict possible, five failed runs) receipted. SCORECARD diff adds only the capability row + planned section + erratum. |
| calibration | **improved** | C2 verifies re-measured: 18 genuine re-reads with input-keyed receipts, guard restored from no-verdict to `lost=0 ok` 64/64 at the tip; verdicts graded honestly (gap-minor named); the lane's own SOURCES edit caught by its guard and paid for (batch 2) rather than rationalized. |
| depth | unchanged | No depth move claimed; SKILL.md bytes unchanged base→tip; SCORECARD carries no depth change. |
| freshness | unchanged | PROVINCE.md untouched (diff empty); no freshness claim; the r60 host correction stands unedited. |
| coverage | unchanged | PROVINCE.md untouched; no new surface claimed (capability, not surface). |
| adjacency | unchanged | No cross-domain absorption; shokuknow unreachable, `considerthese/` mined with nothing adopted, disclosed. |

No axis harmed. Trends: **expansion improved** (capability entered the table demonstrated; S289
re-open + honest S293 rejection row; census clean), **quality improved** (stale entries re-verified at
the pin with receipts; no admitted entry failing its re-check; the no-harm guard went from
unverified-with-provisional-regression to a re-runnable verdict), **discernment improved** (this
verifier's spot-check agrees with the gate on the sampled admit and both rejects; the round caught and
priced its own S293 mistake; superseded batch disclosed).

## 5. Routed defects for the lane (next round; none bar admission)

1. **RD1 (probe-guard prose vs code).** The report C1 bullet and lesson mistake-1 fix claim the
   spawn-equivalence probe "fails the run on any mismatch OR an empty sample" ("exit 2 … requires
   sampled ≥ 1 and mismatches = 0"). The shipped bytes do not implement the empty-sample half:
   `equivalence_probe` returns `{sampled: 0, mismatches: 0}` for an empty candidate set and `main()`
   gates only on `mismatches`. Unreachable on real runs of this repo (the ledger is always prefetched
   and always tracked, so the candidate set is non-empty; every receipt shows sampled=20), so the
   measurements stand — but the fix described as landed is not in the code. Fix next round: add the
   `sampled < 1 → exit 2` guard, re-run one receipt, and correct the lesson text (append-only).
2. **RD2 (number drift, "21 files").** Report, lesson, LOG entry and the `19d7e996` commit subject say
   the D1 first-family landing is 21 files; the committed tree holds 20 (`git ls-tree -r | grep -c
   first-family/` → 20 at `19d7e996` and at the tip; none elsewhere). The receipts themselves are
   genuine and resolving. Erratum.
3. **RD3 (number drift, "2,215-line SKILL.md").** The report says the full-page re-read covered "the
   complete 2,215-line SKILL.md"; SKILL.md at base, pin `0a29e3cf` and tip is 2,214 lines
   (`git show <rev>:SKILL.md | wc -l`; file is newline-terminated). Likely a `split('\n')` off-by-one.
   The read itself is receipted (skill_sha256 matches at the pin). Erratum.
4. **RD4 (trivial, fold with RD2/RD3).** Lesson `## Gate` calls the S289 re-open quote "12 words"; the
   quoted framing is 8 tokens. Quote location and content accurate.

## 6. Ruling

Status `ok` — real report, not a marker; step-1 clean. **Admitted**: C1 and C2 verify (re-measured by
this verifier from the repo alone), D1–D3 verify (committed receipts + independent byte checks), the
spot-check agrees with the gate, and no owned axis is harmed. Defects RD1–RD4 are status-neutral
conformance/craft defects routed above; the standing L2/L0 operator question remains open and disclosed.
