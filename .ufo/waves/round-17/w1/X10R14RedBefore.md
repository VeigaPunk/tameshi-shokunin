# X10R14RedBefore — R16-C2b red-before input overlay (round-14 bucket)

## Deliverables (all under `.ufo/evidence/round-17/redbefore/`)

- `legacy-r14-inputs.json` — overlay array, one entry for `## Effective expectation reconciliation — round 14` (start line 1563 of the 97cf436b page), `skill_sha256=97cf436b669ea445abe36cf6757202eec1c2a4bad2814b07f4159bb9dc623580`, `read_rev=e69b488f65b17bcfd41949abf7d538a77678dc26`, and 19 lane-relative `inputs` with the sha256 each file had at e69b488.
- `digest-diff.txt` — e69b488 vs 09ee1d0 digest table (status / path / sha@e69b488 / sha@09ee1d0).
- `logs/` — raw `strace -f -qq -e trace=openat,openat2,open,execve` logs (also gzipped), captured stdout JSON + stderr per run, `exits.tsv`.

## Method

Fleet-mirror clone `git clone /home/vgpnk/Projects/shokunin/tameshi-shokunin` with all sibling `*-shokunin` repos symlinked beside it; checkout `e69b488f65b17bcfd41949abf7d538a77678dc26`; `git worktree add --detach` for `09ee1d099190918ec388019bb79afbb6b93f1ff2`. Ran recipe steps 2 and 3 verbatim from each root under strace, then a small Python parser mapped successful `open*` calls back under each root (realpath, `.git/` excluded, directories excluded) to lane-relative paths and hashed the read bytes.

## Exits table

| rev | manifest | exit | expected |
|---|---|---|---|
| e69b488 | `dispositions-before.json` | 1 (`"status":"failed"`, 1 finding: `producer_before`) | 1 |
| e69b488 | `dispositions.json` | 0 (`"status":"clean"`, 0 findings) | 0 |
| 09ee1d0 | `dispositions-before.json` | 2 (`expected_input_digest_mismatch`) | 2 |
| 09ee1d0 | `dispositions.json` | 2 (same) | 2 |

## Drifted inputs e69b488 → 09ee1d0

- `tools/mutate-and-run.sh`: `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` → `0673d2e5374b94c651238e7497cbebaffb6483348400747b08f9d27cdc8118aa` — **DRIFTED**. Git diff: round-16 added the seventh `--regression` leg (`js-round-gate`, kumitate `scripts/round-gate.mjs`, 5/10 50%) plus comment updates. The gate's pinned digest in `expected.json` still demands the e69b488 bytes, hence exit 2 could-not-evaluate at 09ee1d0.
- `tools/pin-disposition.py`, `tools/witness-metadata.py`: opened at e69b488, **not opened** at 09ee1d0 (the `mutate-and-run.sh` pin check fails first and short-circuits — the 168-line 09ee1d0 traces vs 170 at e69b488).
- All 16 other inputs identical across both revs (all `.ufo/evidence/round-12|13|14` bytes, `dispositions*.json`, `tools/bash-witness-study.py`, `tools/evidence-disposition.py` sha `1609a9df…` — matches the tool's own reported `tool_sha256`).

## Notes for the L1 / C1 ledger

- The overlay `inputs` uses the **e69b488** digests — the rev CR26 actually read. With these pins the bucket is creditable at e69b488 and uncredited (`input-drift:tools/mutate-and-run.sh`) at any rev ≥ 09ee1d0 until the v2 `historical_inputs` manifest (R16-OP1, contract A) reads the moved tool from git. This is exactly the red-before fixture C1's `--selftest` needs.
- Both recipes at e69b488 produced their registered outcomes live (before→failed/producer_before unresolved; after→clean/0) — the r14 manifest behavior holds at the rev the reader used.

## Tooling

No installs; used `strace`, `git`, `python3` (stdlib only) already on host.

## Verdict

built — overlay + strace logs + exits table written; single drifted input `tools/mutate-and-run.sh` (r16 seventh-leg edit) with two downstream not-opened tools identified.
