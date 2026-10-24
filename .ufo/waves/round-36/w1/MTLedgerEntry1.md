# MTLedgerEntry1 — mutation probe: round-36 ledger refresh entry 1 (section `## Mutation-sweep recipe`, start 131)

Seat: mutation tester (leaf). Wave round-36 / w1. No production edits; scratch-only mutation.
Lane tip under attack: `d9c496b19371b779ce0eec6dfee1b049b27a3a2d` ("round-36: receipts — …").
Scratch: `/fast/scratch/hyaku/tameshi-r36-seats/MTLedgerEntry1/` (clone of the lane, `--no-hardlinks`; lane `.git` never written).

## Attack surface

C1's refresh delta lives in `.ufo/evidence/round-21/coldread/ledger.json`. Entry 1 of the refresh is the
`start=131,end=245` entry with `skill_sha256=2381873162…`, `read_rev=e423c41b…`, trace receipt
`.ufo/evidence/round-36/coldread/traces/L1/source-1.json`, and eight recorded inputs
(`SKILL.md`, `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`,
`corpus/knowledge/closeout-r11.md`, `corpus/knowledge/survivor-fixture-minimization.md`,
`tools/mutate-and-run.sh`).

Claimed invariant: the refresh entry is input-keyed — credit at the refresh commit is granted only while
every recorded input still hashes to its pinned value at the measured revision.

**Mutant applied (one byte):** in that entry's `inputs`, `"corpus/README.md": "7c0fe513…"` became
`"8c0fe513…"` — first hex digit `7`→`8`, only that value, nothing else.

- Pristine ledger file sha256 `29bddc03f957ef962a6e8d6192e96527e017d86d294d1944b07cb3263ba3bbbf` (blob at `d9c496b`)
- Mutant ledger file sha256 `c323e18bbe69924024107e7080e979b49696a66b61e7cd16bf8c7fb29d4fc544` (git blob `22ba7871849cc813e18256aca88aa9bd438e5c58`)
- Byte-diff against `HEAD:…/ledger.json`: `len old=new=3489570`, exactly **1** differing byte at 0-based offset `3485283` (`7`→`8`); `git diff --numstat` = `1 1`.
- Deliberately a non-`IGNORED_INPUTS` key: the frozen round-18 algorithm ignores the entry's self-referential `SKILL.md` pin (`IGNORED_INPUTS`), so mutating that value cannot fail the entry; `corpus/README.md` is a verifiable recorded input.

## Commands and revisions (detector = the C1 monitor, frozen bytes)

Detector bytes used throughout: `.ufo/evidence/round-21/coldread/measure.py` sha256 `657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb`; `.ufo/evidence/round-18/measure.py` sha256 `7ca87a7c98196d87a86627cf96e2e9bc7b3a8769496a75ce8caca1955b26dd37`.

1. Baseline, pristine `d9c496b19371b779ce0eec6dfee1b049b27a3a2d`:
   `python3 <lane>/.ufo/evidence/round-21/coldread/measure.py --repo /fast/scratch/hyaku/tameshi-r36-seats/MTLedgerEntry1/repo --rev d9c496b19371b779ce0eec6dfee1b049b27a3a2d`
   → exit 0, `calibration_restraint_score 8`, `sections_covered 64/64`, `box3_points true`, `trace_gate strict`, `overrides_used false`, `reasons {"credited": 64}`.
2. Mutant committed in scratch: `e365c8b7900937e059c5f522b7bfcdaa5b55c815` (`1 file changed, 1 insertion(+), 1 deletion(-)`).
3. Mutant run, same command with `--rev e365c8b7900937e059c5f522b7bfcdaa5b55c815`:
   → exit 0 (monitor does not hard-fail; it withholds credit), `calibration_restraint_score 6`, `sections_covered 63/64`,
   `box3_points false`, `trace_gate strict`, `overrides_used false`.
   Section 131: `credited false`, `vetoed false`; aggregate missing reason (joined over all failing entries for that section sha) contains `input-drift:corpus/README.md`.
4. Per-entry gate, same frozen module, at `e365c8b7900937e059c5f522b7bfcdaa5b55c815` for the mutated entry
   (`start=131`, `read_rev=e423c41b…`):
   - `input_reason  = 'input-drift:corpus/README.md'`
   - `trace_reason  = 'trace-input-drift:corpus/README.md'`
   - `entry_reason  = 'input-drift:corpus/README.md'`
   At pristine `d9c496b…` the same entry reported `input_reason = trace_reason = entry_reason = None`.
5. Restore: `git checkout d9c496b19371b779ce0eec6dfee1b049b27a3a2d -- .ufo/evidence/round-21/coldread/ledger.json`
   → sha256 `29bddc03f957ef962a6e8d6192e96527e017d86d294d1944b07cb3263ba3bbbf` (byte-identical to pristine), committed as
   `3c43520efeaecbe8c77ad192ffc782baf04356a8`; `git diff --name-only d9c496b…3c43520` is empty (restored tree == pristine tree).
6. Restored run at `3c43520efeaecbe8c77ad192ffc782baf04356a8`:
   → exit 0, `calibration_restraint_score 8`, `sections_covered 64/64`, `box3_points true`, `reasons {"credited": 64}`.

## Evidence files (scratch, hashes of raw monitor stdout)

`/fast/scratch/hyaku/tameshi-r36-seats/MTLedgerEntry1/`

| file | sha256 |
|---|---|
| `base.json` (pristine `d9c496b`) | `b2f493e0d9dbce3d22206f8e16090f58a3729268529c6ddbc637d1ef9feb925a` |
| `base-explain.json` | `d421ccb90bb46ebfa491ed2263586772872420b76ce5f40fd66285ba7f5cd5d1` |
| `mutant.json` (`e365c8b`) | `4320da415a5108504ff45605c6ccdb5f802fdbe200f7c9af5e546ac4ad990411` |
| `mutant-explain.json` | `0d52885431af9eda3b8d2d5519566ded12deff0f0856ef977037da462bcb1f8f` |
| `restored.json` (`3c43520`) | `aa30adc7d1806abd473734d2e097c04e30eb89c7da9ae3ca0c26759a73a176eb` |

Lane untouched: `git -C <lane> status --porcelain` shows only untracked `.ufo/waves/round-36/w1/` (wave reports); lane `HEAD` remains `d9c496b19371b779ce0eec6dfee1b049b27a3a2d` and the lane ledger still hashes to `29bddc03…`. Scratch worktree clean at restore commit. No tool installs.

## Verdict

**KILLED.** The one-hex-digit input mutant in round-36 refresh entry 1 is detected: the entry's own gate returns
`input-drift:corpus/README.md` (and the independent trace gate returns `trace-input-drift:corpus/README.md`), the
section loses credit and the C1 monitor falls from `8, 64/64` to `6, 63/64`; restoring the exact bytes returns it to
`8, 64/64`. The refresh entries are genuinely input-keyed at the measured revision, so the 6→8 credit movement is not
a rubber stamp: one drifted input pin revokes it.
