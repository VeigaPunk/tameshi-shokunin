# ReviewSHONEN — round-34 w1

Seat: `tameshi-r34-w1-ReviewSHONEN` (reviewer). Scope: SHONEN.md per-box status at the lane tip, byte-pin verification, and falsification review of the landed C1 round-34 claim. Lane tip verified: `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7` (detached clone at `/fast/scratch/hyaku/tameshi-r34-seats/ReviewSHONEN/lane`, `git rev-parse HEAD` = tip, exit 0). All commands below ran against that clone or the read-only lane; all scratch writes stay under `/fast/scratch/hyaku/tameshi-r34-seats/ReviewSHONEN/`.

**Verdict: the landed C1 claim survives this review.** The deciding-run receipt is byte-identical to the claim, every receipt field was independently reproduced by re-running the frozen tool through the frozen counter's own machinery (allowed module import, never default mode), and all four SHONEN.md evidence pointers resolve at the tip with correct `[~]` markers. One low-severity informational observation; no blocking findings.

## 1. Byte pins (frozen artifacts)

Commands: `git -C lane show <rev>:<path> | sha256sum` (each exit 0).

| Artifact | Expected sha256 | At tip 0b99d48e | At measure rev c17e593b | At amendment rev 6aaad5b3 | Live tree | Match |
|---|---|---|---|---|---|---|
| `tools/tally-audit-v2.py` | `7b11ba25…8d10` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` | identical | identical | identical | yes |
| `tools/mutate-and-run.sh` | `a7d3f2dd…2eb9` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` | identical | — | identical | yes |
| `.ufo/evidence/round-33/c1/c1-measure.py` (counter) | `f6b8868c…a07f28c` | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` | identical | identical | — | yes |
| `.ufo/evidence/round-32/c1-measure.py` (counter chain dep) | n/a (observed) | `ecb265298d8cba6a6146f27f6679f1217ad3610104e3c2b46947516cf32f0aca` | identical | — | — | yes |

No path under `tools/` or `.ufo/evidence/round-33/` changed between `c17e593b` and the tip: `git log --oneline c17e593b..0b99d48e -- tools .ufo/evidence/round-33` → empty (exit 0). `c17e593b` is an ancestor of the tip: `git merge-base --is-ancestor` exit 0; exactly one intervening commit (`0b99d48e`, receipt + SCORECARD + lesson + knowledge + S101 + census; `git show --stat` confirms it touches no frozen artifact).

## 2. Deciding-run receipt — byte and field verification

- `.ufo/evidence/round-34/measure/c1-deciding-run.stdout` at tip is **byte-identical** to the claimed receipt (`printf '%s\n' '<claim>' | diff - <file>` → no output, exit 0):
  `C1_R33: tool_present=1 tool_sha_ok=1 runner_sha_ok=1 controls_ok=1(ok) v1_kill=18/18 v1_accept=8/8 ho_kill=8/8 ho_accept=6/6 ho_invalid=0 heldout_after_freeze=1 seed=685f63bd25263908 rev=c17e593b51802dd4ed568da3265f21c6d00c4273 C1_R33_PASS=true`
- `.ufo/evidence/round-34/measure/c1-deciding-run.exit` contains literal `0` (cat, exit 0).
- Cross-record consistency: the same receipt string appears verbatim in `SCORECARD.md:1643` (round-34 row) and `LOG.md` round-34 entry; the capability row at `SCORECARD.md:1657` cites `c17e593b` + tool pin `7b11ba25…8d10`. `corpus/lessons/round-34.md` Holds explicitly records the v3 residue classes as measurement-only (no tool edits this wave) — consistent with the unchanged tool pin.

## 3. Independent module-level replay (allowed mode)

The kill rule was honored: the frozen counter was **never run in default mode**. Replay used `importlib` on scratch copies (`replay/.ufo/evidence/round-33/c1/c1-measure.py`, sha `f6b8868c…a07f28c`; `replay/.ufo/evidence/round-32/c1-measure.py`, sha `ecb26529…`, byte-matching `c17e593b` bytes) and called `public_panel`, `score_tool`, `validate_ho`, `apply_edits`, `ho_witness_ok`, `run_tool_sandboxed`, `adding_commit`, `is_ancestor` — mirroring `main()`'s logic at `c1-measure.py:346-434`.

Command: `cd /fast/scratch/hyaku/tameshi-r34-seats/ReviewSHONEN/replay && python3 replay.py > replay.stdout 2> replay.stderr; echo $? > replay.exit` → **exit 0**, last line `REPLAY_PASS true`, `MISMATCHES {}`. Script: `replay/replay.py`; output: `replay/replay.stdout` (33 lines). Runtime: python 3.14.8, bwrap 0.13.1 (same host tools the deciding run's sandbox used: `bwrap --unshare-all --die-with-parent --new-session --clearenv`, `timeout` outside the boundary — code `c1-measure.py:223-262`).

Reproduced fields, all matching the receipt:

- `tool_present=1 tool_sha_ok=1 runner_sha_ok=1` — `git show c17e593b:<path>` bytes hashed.
- `controls_ok=1(ok)` — receipt `counter_sha256` equals sha256 of counter bytes at `c17e593b`; `all_false=true`; all 4 control rows `predicate_pass=false` (CtlDoNothing 0/18 kill, CtlAlwaysPass 0/18, CtlAlwaysFail 18/18 + 0/8, CtlShaOnly 18/18 + 1/8 — matches `controls-receipt.json` exactly).
- `v1_kill=18/18 v1_accept=8/8` — `public_panel(runner_b, '685f63bd25263908')` produced 18 kill + 8 accept copies; `score_tool` re-ran the tool byte-for-byte under bwrap: 18 KILL + 8 ACCEPT.
- `ho_invalid=0`, `ho_kill=8/8`, `ho_accept=6/6` — all 14 sealed JSONs: `validate_ho` clean, `apply_edits` clean, `ho_witness_ok` true with amendment-6 set-aware tags (`head-leg-assignment` ×2 kill-head, `head` ×2 accept-head, `vector` ×6 kill-vector, `vector-equivalence` ×4 accept-vector); `run_tool_sandboxed` produced `TALLY_AUDIT: FAIL`/rc 1 on all 8 must-kill and `TALLY_AUDIT: PASS`/rc 0 on all 6 must-accept.
- `heldout_after_freeze=1` — independently recomputed via git history: `adding_commit` for counter and tool = `f6d8a891f1d966c5c3cdda385090da3a6e804675` (round-33 freeze); every sealed file was added at `c17e593b` (`git log --diff-filter=A` per file); `merge-base --is-ancestor f6d8a891 c17e593b` exit 0 for all 14 — so all sealed copies postdate both freezes.
- `controls-receipt.json` provenance: added at `9dd3174c` (`git log --diff-filter=A`), receipt bytes identical at `9dd3174c` and tip (file sha256 `f1e6242182939c7f83c8cb42f6bfb3253bc2f8b415b4c2d98166ba92080de3aa`), and its `counter_sha256` field equals the counter's byte-sha at `6aaad5b3`, `9dd3174c`, `c17e593b` and tip (all `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c`).

Supporting corroboration: `.ufo/evidence/round-34/dev/authoring-receipts.json` has 14 entries, one per sealed id, each `as_expected=true edits_ok=true witness=[true,<tag>]` with tool outcome consistent with my replay tags. `.ufo/evidence/round-34/dev/witness-probes.json` records the 8/8 amendment-6 probe battery. `census-end.exit`=`0`.

## 4. SHONEN.md per-box status

`SHONEN.md` at tip is byte-identical to the live tree (`diff` → empty) and to `c17e593b` (`git show c17e593b:SHONEN.md | diff` → empty). It contains zero `[x]` marks (`grep -nE '\[x\]' SHONEN.md` → exit 1, no matches): all four boxes are `[~]` lane assertions, each pointing to durable evidence, and each annotation itself declares "no independent promotion verifier" — matching the expectation that no `[x]` should name a non-author verifier.

| Box | Mark | Text | Evidence pointer | Resolves at tip? | Status |
|---|---|---|---|---|---|
| 1 | `[~]` | SKILL.md contains real decision tables, error patterns, checklists, cited sources | `reports/round-1-calibration.md#box-1` | file exists; `## box-1` anchor at line 71 | verified — content plausible (SKILL.md has gate-shape decision table `:58`, fail-closed taxonomy `:497`, no-permissiveness checklist `:466`, 51 in-file corpus/S### citations) |
| 2 | `[~]` | At least one end-to-end domain task executed and logged in LOG.md | `reports/round-1-calibration.md#box-2` | file exists; `## box-2` anchor at line 105 | verified — `LOG.md` records domain tasks incl. round-3 kagi census and this round's measurement |
| 3 | `[~]` | Instructions executable by an agent without oral context | `.ufo/evidence/round-21/coldread/ledger.json` | file exists (40,189-line v2 ledger) | verified at pointer depth — qualifier "input-keyed monitor only" is honest: ledger has 493 entries but only 27 `executed-ok` + 53 `verified-record`, 374 `gap-minor`, 36 `wrong-expectation`, 3 `gap-blocking` (6 blocking gaps total); it is monitor input-keying, not a clean bill |
| 4 | `[~]` | No cross-domain bleed (PROVINCE.md still accurate) | `reports/round-1-calibration.md#box-4` | file exists; `## box-4` anchor at line 167 | verified — `PROVINCE.md:3-18` states verification-fixture craft domain, owned surfaces, sibling-refusal rules |

Consistency note: the round-1 audit's own disposition table (`reports/round-1-calibration.md:206-209`) downgraded box 3 to `[ ]` at that time; the current `[~]` reflects the later round-21 ledger evidence, and the box's own qualifier names it "input-keyed monitor only" — the mark is honestly bounded, not overstated.

## 5. Findings

**Low / informational (1):** `reports/round-1-calibration.md` (the evidence for boxes 1, 2 and 4) cites "Canonical seed row: `PROTOCOL.md:425-428`" (lines 73, 107, 134, 169) and `PROTOCOL.md:63-68` (lines 102, 130, 162), but `PROTOCOL.md` does not exist in this repository at the tip — `git cat-file -e 0b99d48e:PROTOCOL.md` fails; `git ls-tree -r --name-only 0b99d48e | grep -i protocol` returns only `corpus/knowledge/service-optin-protocol.md`. Repro: `cd <lane-clone> && git cat-file -e 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7:PROTOCOL.md` (nonzero). Impact: second-hop pointer only — every first-hop SHONEN.md pointer resolves and box annotations do not lean on the seed row for their `[~]` status; the canonical seed lives in the fleet-level PROTOCOL outside this repo. Recorded as a dangling second-hop citation, not a defect in any landed claim.

No other findings: every caller-facing contract I checked (receipt fields, pin shas, freeze provenance, controls chain, marker discipline, pointer resolution) verified clean.

## 6. Residual risk and verification gaps

- The replay exercised the counter's logic paths directly (`score_tool`, `ho_witness_ok`, `run_tool_sandboxed`) — it did **not** execute `main()`'s CLI/argparse/SETUP exits (default mode is the consumed kill rule; prohibited). Receipt-format and exit-path defects there would be invisible to this replay; code review of `main()` (`c1-measure.py:332-442`) shows the printed line matches the receipt format 1:1.
- `seed=685f63bd25263908` reproducibility relies on `random.Random(seed)` determinism in `generated_kill`/`generated_accept` — stable under CPython's documented str-seed behavior; verified empirically (my panel reproduced the same 18/8 sizes and kill/accept outcomes).
- `controls_ok` was verified statically (receipt fields + counter sha identity across revs); the four control tools' `predicate_pass=false` results were recomputed only through my fresh `score_tool` runs of the real tool — the control tools themselves were not re-executed (round-34 `ctl/` copies exist; out of seat scope, other seats cover control critique).
- Box-3 `[~]` rests on monitor input-keying at `eb7838b` (round-21); post-monitor appends (SCORECARD/LOG/lessons/SOURCES rounds 22-34) are explicitly flagged in `corpus/lessons/round-34.md` Holds as pending cold-read re-crediting — an honest, disclosed gap, tracked elsewhere in this wave.
- No `lsp` device in this seat's tool inventory; semantic checks used git-object resolution and targeted grep as the literal fallback.
- Tooling: no installs performed (host `python3 3.14.8`, `bwrap 0.13.1`, `git`, `coreutils` sufficed); pacman untouched per the pause ruling.

## 7. Compliance

- Lane untouched except this report file; all scratch work under `/fast/scratch/hyaku/tameshi-r34-seats/ReviewSHONEN/` (clone `lane/`, staged copies `replay/.ufo/`, replay script/output `replay/`).
- Kill rule honored: the counter was imported as a module only; `main()`/default mode never invoked; every captured exit code recorded (`replay.exit`).
- No git/jj writes, no `agent://all`, no model parameter, no frozen-artifact edits.
