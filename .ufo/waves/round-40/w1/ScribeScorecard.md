# ScribeScorecard — round 40, wave 1: SCORECARD C1/C2 rows drafted from the frozen contract

Seat: ScribeScorecard (leaf, no delegation) · 2026-10-24 · Lane: tameshi-shokunin.
Contract: `.ufo/evidence/round-40/contract.json`, frozen at commit `5641ed84` ("round-40: freeze C1
write-form census and C2 S108 snapshot pin before data"; parent/base `304e3355`). Contract blob
sha256 at `5641ed84` = `8a8dd141…047d`, byte-identical to the on-disk file (verified this seat).
Not done, by bounds: counter default mode never run by this seat; `SCORECARD.md` untouched; live
checkout untouched (only this Report file written under `.ufo/waves/`); scratch in
`/tmp/tameshi-r40-ScribeScorecard/`. No tool installs (none needed).

## 1. Draft rows (paste-ready, SCORECARD.md:166 claims-table format)

After cells are deliberately **not measured** — the deciding run belongs to the L1 after settlement.

| # | Claim | Type | Axis | Before | After | Counting command | Measured commit |
|---|---|---|---|---|---|---|---|
| C1 | `write-path-census-v2`: counts the write forms the frozen v1 census misses (`expected.json` via `.write_bytes`, `os.replace`) | capability acquisition | depth | base `304e3355`: `tools/write-path-census-v2.py` absent (`git show 304e3355:tools/write-path-census-v2.py` → exit 128, this seat; pre-existing counter artifact `.ufo/evidence/round-40/before/c1-at-base.stdout`: `C1_R40: tool_absent=1 … C1_R40_PASS=false`, exit 1); v1 census `tools/write-path-census.py` (sha `bc8c660c…dc62`, unchanged base→freeze, this seat) scores the planted new forms 0 (`.ufo/evidence/round-40/control/v1-on-fixtures.stdout`: `C1_R40_CONTROL: v1_bytes_unflagged=0 v1_replace_writes=0 v1_replace_unflagged=0 C1_R40_CONTROL_PASS=false`, exit 1 — re-run byte-identical by this seat) | **not measured — deciding run pending (L1, after settlement).** Predicate at REV: v2 tool sha256 = `402285…878b` ∧ v1 sha still `bc8c660…dc62` ∧ planted `bytes_unflagged=1` and `replace_unflagged=1` ∧ `bytes_flagged=replace_flagged=scratch_replace=0` ∧ v1 scores `bytes_unflagged=0` and `replace writes=0` on the two planted cases ∧ ≥1 `expected.json` `.write_bytes` line in `tools/registry-replay.py` that v2's pattern hits and v1's misses ∧ ≥1 `os.replace` line in `tools/bash-witness-study.py` that v2 hits and v1 misses ∧ removing `os\.replace\s*\(` or `expected\.json` from the v2 source makes the selftest fail. Do-nothing falsifier: tool absent at base (observed) or v1 patterns on the planted fixtures. | `python3 .ufo/evidence/round-40/census/measure.py --lane LANE --rev REV` | pending; pins: freeze `5641ed84`, base `304e3355` |
| C2 | S108 golden-tests (zh-cn) snapshot re-pin: `.ufo/evidence/round-40/s108/golden_tests.zh-cn.html` | source-pin | freshness | base `304e3355`: snapshot absent (`git show 304e3355:.ufo/evidence/round-40/s108/golden_tests.zh-cn.html` → exit 128, this seat; pre-existing `before/c2-at-base.stdout`: `C2_R40: snapshot_absent=1 … C2_R40_PASS=false`, exit 1) | **not measured — deciding run pending.** Predicate at REV: blob sha256 = `f27cf27…2bf0` ∧ the quote occurs in the tag-stripped text; a missing file, or the file with the contiguous prefix `可以通过使用参数` removed, cannot pass (counter operationalizes this: `stripped_quote_fails=1` required, `.ufo/evidence/round-40/s108/measure.py:79-81`). Do-nothing falsifier: no snapshot at base (observed). | `python3 .ufo/evidence/round-40/s108/measure.py --lane LANE --rev REV` | pending; pins: freeze `5641ed84`, base `304e3355` |

Stagnation context carried by the contract (`contract.json` §stagnation): saturation line 8, window
N=2, depth 9 / calibration 8, last capability round 37, rounds 38–39 without capability → nudge
fires, lowest-axis obligation waived. C1 is the capability that would answer the nudge on depth.

## 2. Clause ledger — every C1/C2 clause checked at the freeze rev (this seat, scratch only)

Method: blobs read via `git show REV:path` (no counter default mode); scratch copies in
`/tmp/tameshi-r40-ScribeScorecard/`. Hash claims verified programmatically as sha256 equality
booleans on two independent paths (shell `sha256sum` + Python `hashlib`), both True.

C1 (all at `5641ed84` unless stated):
- v2 tool sha256 == contract pin `402285…878b`: **True** (also worktree file byte-identical to freeze blob).
- v1 sha256 == pin `bc8c660…dc62`: **True**; still `bc8c660…dc62` at base `304e3355`: **True**.
- v2 absent at base: **True** (exit 128); v2 tool-absent branch of the counter then forces `C1_R40_PASS=false` (`.ufo/evidence/round-40/census/measure.py:73-80`).
- Planted v2 classification (`classify_text` on `census/fixtures.json`, sha `af23747…fa5d`): `bytes_unflagged=(1,1)`, `replace_unflagged=(1,1)`, `bytes_flagged=(1,0)`, `replace_flagged=(1,0)`, `scratch_replace=(1,0)` — matches predicate and `planted_ok` (measure.py:210-218).
- Planted v1 scores (`v1_classify`, measure.py:33-51): `bytes_unflagged=(1,0)`, `replace_unflagged=(0,0)` → v1 unflagged-bytes 0, v1 replace-writes 0: **predicate holds**.
- `tools/registry-replay.py` @ freeze: exactly 1 `.write_bytes`+`expected.json` line; v2 `EXPECTED_RE`+`WRITE_RE` hit it, v1 `V1_EXPECTED_RE` misses → `v2=1, v1=0`. Example hit: ``(out / 'expected.json').write_bytes(encode({'schema': 'command-binding-expected-v1',…``.
- `tools/bash-witness-study.py` @ freeze: exactly 1 `os.replace` line; v2 hits, v1 `V1_WRITE_RE` misses → `1, 0`. Example hit: `os.replace(tmp, path)`.
- Mutation clause (scratch copies of the freeze-blob tool): pristine selftest exit 0, `WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0`; mutant with literal `os\.replace\s*\(` removed → exit 1 (`re.PatternError`, killed); mutant with literal `expected\.json` removed → exit 1 (`bytes_unflagged=0`, selftest assertion, killed). **Both killed, as required.**
- Control mode run by this seat: `python3 .ufo/evidence/round-40/census/measure.py --lane <lane> --control` → `C1_R40_CONTROL: v1_bytes_unflagged=0 v1_replace_writes=0 v1_replace_unflagged=0 C1_R40_CONTROL_PASS=false`, exit 1, byte-identical to the pre-existing control artifact. Direction per `measure.py:98-99` ("The v2 target is both new classes at 1. v1 cannot reach it."): `PASS=false` is the consistent do-nothing outcome; `true` would mean v1 also reaches the target and would falsify the claim.

C2:
- Contract `claims.C2.snapshot_sha256` == freeze blob sha256 `f27cf27…2bf0`: **True**; contract quote string == counter's `QUOTE` const (s108/measure.py:23): **True**.
- Quote in tag-stripped text: **True**; quote in raw contiguous bytes: **False** (confirms the counter's stripped-text rationale, s108/measure.py docstring).
- Contiguous prefix `可以通过使用参数` occurs exactly **once** in the raw blob; after removing that first occurrence, stripped-text quote → **False**, i.e. `stripped_quote_fails=1` semantics satisfiable.
- Snapshot absent at base: **True** (exit 128) → `C2_R40_PASS=false` per do-nothing branch (s108/measure.py:66-73).

## 3. Pre-existing artifacts found on disk (NOT produced by this seat)

`.ufo/evidence/round-40/{before,control,after}/` existed before this seat started; `after/` is
**untracked** in git (`git status --porcelain` → only `?? .ufo/evidence/round-40/after/`), author
and invocation unknown to this seat. Recorded verbatim, neither relied on nor adjudicated:

- `before/c1-at-base.stdout`: `C1_R40: tool_absent=1 bytes_unflagged=0 replace_unflagged=0 v1_bytes_unflagged=0 v1_replace_writes=0 rev=304e3355… C1_R40_PASS=false` (`.exit` = 1)
- `before/c2-at-base.stdout`: `C2_R40: snapshot_absent=1 quote_in_snapshot=0 sha_ok=0 stripped_quote_fails=0 rev=304e3355… C2_R40_PASS=false` (exit 1)
- `control/v1-on-fixtures.stdout`: `C1_R40_CONTROL: v1_bytes_unflagged=0 v1_replace_writes=0 v1_replace_unflagged=0 C1_R40_CONTROL_PASS=false` (exit 1)
- `after/c1-at-5641ed84.stdout`: `C1_R40: tool_absent=0 tool_sha_ok=1 v1_sha_ok=1 bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0 v1_bytes_unflagged=0 v1_replace_writes=0 live_json_v2=1 live_json_v1=0 live_replace_v2=1 live_replace_v1=0 mutant_replace_killed=1 mutant_json_killed=1 rev=5641ed84… C1_R40_PASS=true` (exit 0) — a **default-mode** counter run at the freeze rev.
- `after/c2-at-5641ed84.stdout`: `C2_R40: snapshot_absent=0 quote_in_snapshot=1 sha_ok=1 stripped_quote_fails=1 rev=5641ed84… C2_R40_PASS=true` (exit 0) — also default mode.

These are consistent, clause-for-clause, with this seat's independent replication, but the ticket
reserves the deciding run for the L1 after settlement; the draft rows above therefore keep After =
pending and treat these files as unowned prior observations.

## 4. Falsification attempts → results

1. Base invariance: tried to find v2 tool or S108 snapshot at base `304e3355` → absent (exit 128 twice); v1 unchanged at pin at base. Base `PASS=false` for both counters holds.
2. Do-nothing via v1: ran control mode + reimplemented `v1_classify` on the planted fixtures → v1 reaches neither new class (`0/0/0`). No v1-pass falsification.
3. C1 mutation clause: both source mutants kill the selftest (exit 1 each). No clause break.
4. C2 shortcut: raw contiguous byte search for the quote → absent (only the stripped text carries it); prefix occurs once, so the single-replacement ablation is well-defined and kills the quote as the predicate demands. No clause break.
5. Frozen-contract integrity: on-disk `contract.json` byte-identical to the `5641ed84` blob; worktree `tools/write-path-census-v2.py`, `tools/write-path-census.py`, `s108/golden_tests.zh-cn.html` byte-identical to their freeze blobs. No post-freeze drift.

No falsifying finding against the frozen predicates. Only open anomaly: the untracked default-mode
`after/` runs listed in §3 (provenance unknown; not this seat's).

## 5. Limits

- No default-mode counter run performed by this seat; the deciding run remains the L1's.
- Pre-existing `after/` outputs quoted, not reproduced or audited for invocation metadata.
- Terminal rendering in this session occasionally duplicated/dropped hex characters across tool
  surfaces; all pin equalities were therefore verified as programmatic sha256 equality booleans
  (both shell and Python paths), and pins are quoted from `contract.json` as read. Verbatim quotes
  above elide full 40-char revs after 8 chars (`…`) for transcription safety.

Scratch inventory: `/tmp/tameshi-r40-ScribeScorecard/` (`v2-freeze.py`, `v2-pristine.py`,
`v2-mutant-replace.py`, `v2-mutant-json.py`, `fixtures.json`). No installs performed.
