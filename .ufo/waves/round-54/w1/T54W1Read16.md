# T54W1Read16 — cold read of `### Round-14 historical registry — superseded by round 15`

- **heading:** `### Round-14 historical registry — superseded by round 15`
- **cand (content commit C0):** `59c38109bf119d0e9d4f878644a82babc937bc1e`
- **section_sha256:** `06a6864fb05fd63df168597696407397c7d3f4d47337556c25ab60393fb959af`
- **span at C0:** start 1623, end 1634 (exclusive) — lines 1623-1633, 11 lines, 1639 bytes, no trailing newline (round-18 `sectionize` semantics: trailing blank lines stripped)
- **findings:** 1

## Method

Scratch: `export HYAKU_SCRATCH=/fast/scratch/hyaku`; tree `/fast/scratch/hyaku/tameshi-r54/T54W1Read16/` (removed at end; no tree left behind). All lane reads were of git objects at C0 (`git show REV:path`) or of a `git clone --shared` checkout of C0 under scratch; no working-tree read of `SKILL.md`.

```
$ cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
$ export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1Read16
$ python3 .ufo/waves/round-54/reader-section.py /home/vgpnk/Projects/shokunin/tameshi-shokunin 59c38109bf119d0e9d4f878644a82babc937bc1e "### Round-14 historical registry — superseded by round 15"
{"heading": "### Round-14 historical registry \u2014 superseded by round 15", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "start": 1623, "end": 1634, "section_sha256": "06a6864fb05fd63df168597696407397c7d3f4d47337556c25ab60393fb959af"}
```

Independent recomputation of the same bytes with the frozen round-18 sectionize (heading line through the line before the next heading, trailing blank lines stripped, `\n`-joined, no trailing newline) returned the same sha, `06a6864f…b959af`; the raw section text I cold-read is exactly the 11 lines 1623-1633.

Execution copy: `git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin lane`, `git checkout 59c38109bf119d0e9d4f878644a82babc937bc1e`; `git rev-parse HEAD` printed `59c38109bf119d0e9d4f878644a82babc937bc1e`.

## Section bytes read (verbatim, 1623-1633)

```
### Round-14 historical registry — superseded by round 15

| Name | Kind | Entry command | Verdict map | Self-test command | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| effective expectation disposition | gate | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json` (historical; live entry since round 18: `.ufo/evidence/round-18/dispositions.json`; round 17's now exits 2, bash-witness moved) | 0 clean; 1 failed semantic expectations; 2 could-not-evaluate invalid/missing/tampered inputs; 64 usage | `python3 tools/evidence-disposition.py --selftest` | `.ufo/evidence/round-14/dispositions.json` and before counterpart pin historical expected/receipts; historical expected pins13 original inputs; literal isolated selftest expectations in tool | normal mode read-only lane evidence, stdout only; selftest isolated temporary fixtures | tameshi |
| archived invocation context capture | historical gate, not active | do not run; retained source `.ufo/evidence/round-14/capture-context.py` only | historical outcomes retained, not an active verdict map | historical helper-only controls do not satisfy the standalone gate selftest | unchanged round13 pin manifest and context receipt | archive bytes read-only; no supported invocation | tameshi |

The disposition manifest is configured authority, not cryptographic proof of
author authenticity. Receipt replay proves its recorded predicates, not that
every historical command was independently re-executed. Unmapped receipt-only
checks do not acquire new expected rows by being mentioned in a summary.
```

Both table rows carry 8 cells under an 8-column header (checked by pipe count).

## Findings

### F1 — the row's own entry command no longer resolves at C0, and the cell's exit-2 note is scoped to round 17

Quote (byte-exact in the section above and in `T54W1Read16.json`):

```
(historical; live entry since round 18: `.ufo/evidence/round-18/dispositions.json`; round 17's now exits 2, bash-witness moved)
```

Why: at C0 the command this cell annotates exits 2 (`expected_input_digest_mismatch` on `tools/bash-witness-study.py`), so the row's 0-clean verdict is reachable only by replaying at `28aeef4` — a revision this section never names — while the cell's only live-tree warning is attached to round 17.

Receipt (clone at C0, `TMPDIR` usable):

```
$ cd /fast/scratch/hyaku/tameshi-r54/T54W1Read16/lane   # HEAD = 59c38109bf119d0e9d4f878644a82babc937bc1e
$ TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W1Read16/tmp python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json
{
  "error": {
    "kind": "expected_input_digest_mismatch",
    "message": "tools/bash-witness-study.py: observed f2bb50c77a6b6ffc53fd4e31d06c729f9cface7c1684f232c060f6a4978bf261 expects 49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80"
  },
  "exit": 2,
  "id": "expected_input_digest_mismatch",
  "status": "could_not_evaluate",
  ...
}
EXIT=2
```

Same command with `TMPDIR=` (declared unset) and with a usable `TMPDIR` also exits 2 (the digest mismatch fires first), so no environment arm changes the row's live verdict. The same failure is present at the base revision:

```
$ cd /fast/scratch/hyaku/tameshi-r54/T54W1Read16/arch-base    # git archive d33053f7552d
$ TMPDIR=…/tmp python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json >/dev/null 2>&1
BASE_EXIT=2
```

The 0-clean verdict the row maps *is* reproducible at the round-14 archive the preceding section names (not in this section):

```
$ cd /fast/scratch/hyaku/tameshi-r54/T54W1Read16/arch         # git archive 28aeef4
$ python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions.json --json
EXIT=0   status clean exit 0 counts {'effective': 11, 'expected_checks': 12, 'failed': 0, 'findings': 0, 'passed': 11, 'superseded': 1}
$ python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-14/dispositions-before.json --json
EXIT=1   status failed exit 1 findings [('expected_contains_missing', 'producer_before')]
```

So the cell's numbers are historical-correct but its only live-tree annotation is scoped to the round-17 manifest, while the manifest in this very cell regressed identically; the pinned-values cell pins manifest data files, not the three moved tool bytes that decide the replay. A cold reader with no oral context runs the printed command, gets 2, and is never told which revision yields the mapped 0.

## Claims checked and resolved (no finding)

| Claim | What I opened | Result |
|---|---|---|
| `round 17's now exits 2, bash-witness moved` (round-17 manifest) | `.ufo/evidence/round-17/dispositions.json` at C0 | exit 2, `expected_input_digest_mismatch` on `tools/bash-witness-study.py` (observed `f2bb50c7…`, pinned `49e9e5e2…`) — claim true |
| `live entry since round 18: .ufo/evidence/round-18/dispositions.json` | `.ufo/evidence/round-18/dispositions.json` at C0 | exit 0, `status clean`, effective 11 / superseded 1 — claim true |
| verdict map `0 / 1 / 2 / 64` | C0 tool: round-18 manifest (0), round-18 before (1), missing dispositions + malformed JSON (2, `dispositions_missing` / `dispositions_json_invalid`), `--nonsense` (64) | every class observed; `--selftest` prints `usage-no-arguments PASS (exit=64 expects=64)` |
| self-test command `python3 tools/evidence-disposition.py --selftest` | C0 tool | exit 0, `SELFTEST: PASS (66/66)` |
| `historical expected pins13 original inputs` | `.ufo/evidence/round-13/expected.json` at C0 | `inputs` has exactly 13 entries — count true |
| `.ufo/evidence/round-14/dispositions.json` and before counterpart pin historical expected/receipts | both manifests at C0 | each pins 3 inputs: `round-13/expected.json`, `round-13/verification.json`, `round-13/producer-oracle-repair.json` — true |
| `literal isolated selftest expectations in tool` | `tools/evidence-disposition.py` at C0 | `selftest()` builds its fixtures with `tempfile.mkdtemp(prefix=…, dir=strict_scratch_root())` and prints inline `SELFTEST_CASE … literal checks` — true |
| `normal mode read-only lane evidence, stdout only` | clone `git status --porcelain` after every run | empty output — true (no lane write) |
| `do not run; retained source .ufo/evidence/round-14/capture-context.py only` | blob at C0 | exists; sha256 `7313e9a208ac7734d4a5440d04f9a9ea776efe4e1aac07f269f8deca24fe7d89`, matching the archived claim in the following round-15 section; not run |
| `unchanged round13 pin manifest and context receipt` | `.ufo/evidence/round-13/pin-manifest.json` and `.ufo/evidence/round-14/context-receipt.json` at base `d33053f7` and at C0 | manifest sha `64eaa43e…20af6` equals the sha the receipt records; receipt bytes identical at base and C0 (`05cb55b8…9c1a`) — true |
| `historical outcomes retained, not an active verdict map` / `historical gate, not active` | receipt exists, script archived, no registry row invokes it | consistent |
| `Unmapped receipt-only checks do not acquire new expected rows by being mentioned in a summary` | round-18 run output | `informational.receipt_only_checks` names 3 checks (`frozen_and_guardrail_unchanged`, `metadata_emit`, `pin_env_scrub`); rows remain 12 and `expected_checks` 12 — true |
| heading `superseded by round 15` | next heading at C0 (line 1635) | `## Context gate classification and explicit exit classes — round 15` — successor exists |

Considered and **not** reported: the run-together token `pins13` in the pinned-values cell. The count it states resolves (13 inputs) and a missing space is neither an unresolvable anchor, a stale cell, nor a self-contradiction, so it is not a defect under the cold-read categories.

## Raw receipt files (`w1/T54W1Read16-receipts/`)

| File | sha256 | Content |
|---|---|---|
| `c0-exit-classes.txt` | `8408a5242a22397e5ac1f1782e6e78b30484bf0db0dfe6b27698897d6220e1d5` | clone at C0 `head=59c38109…`; the five manifests above with `id`/`status`/`exit`/`counts` and exit codes (2,2,2,0,1) |
| `archive-28aeef4-round14-dispositions.json` | `11378601d2478ca2e61939babd57ad7a5716276b4365284ad5cdeda1bb74c8a7` | `git archive 28aeef4` replay of `.ufo/evidence/round-14/dispositions.json` — `status clean`, exit 0 |
| `archive-28aeef4-round14-dispositions-before.json` | `d61e9469a24b2c687d17eaa97db643fcf38ab96aaad3fa7fd58223b2a3abd9b7` | same tree, `dispositions-before.json` — `status failed`, exit 1 |

## Seat bounds observed

- Only `w1/T54W1Read16.json` and `w1/T54W1Read16.md` were written inside the lane; no lane production file, counter, contract, freeze, ledger or wave spec was touched; no `SKILL.md` edit.
- No mutating git command was issued in the lane: the clone was created with `git clone --shared` under scratch, and all fixtures/archives live under `/fast/scratch/hyaku/tameshi-r54/T54W1Read16/` (removed on exit; `trap 'rm -rf -- "$S"' EXIT`). No `npx`/`uv`/`pacman` install was needed (stock `python3`/`git` sufficed), so nothing was installed.
- LANE_TOOLING: none installed; python3 3.x + git only.
