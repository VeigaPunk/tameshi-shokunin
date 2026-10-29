#!/usr/bin/env python3
"""Build round-57 wave-3 spec (v1 band 32-64, 34 seats): 18 cold-read readers at C0b, 3 blind re-seats, 6 row writers,
amendment-2 selftest + mutation, ledger-row attackers, final contract and controls audits."""
import json
import sys
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
BASE = "5e3569969b532310d2b8a3d130901757a3df356b"
C0 = sys.argv[1]
assert len(C0) == 40
W = ".ufo/waves/round-57/w3"
E = LANE + "/.ufo/evidence/round-57"
WD = LANE + "/" + W
WV = LANE + "/.ufo/waves/round-57"
TEMPLATE = json.loads(open(WV + "/spec-w1.json").read())["template"]
lost = json.load(open(WV + "/lost-at-c0b.json"))
assert len(lost) == 18, len(lost)

CONTEXT = f"""# Goal
tameshi round 57 (hyaku run 11; L1 TameshiR57), wave 3 of three. Lane repo {LANE}; lane base `{BASE}`; final monitored-content commit C0b = `{C0}`. Every path you read, edit or write is ABSOLUTE: seat tools start at the fleet root /home/vgpnk/Projects/shokunin, so a relative `.ufo/...` lands in the FLEET repo. Every `Report:` trailer path the harness renders is relative to {LANE}: write it at {LANE}/<that path>.

# The round (contract `{E}/contract.json`; wave reports under `{WV}/w1/` and `{WV}/w2/`)
- **C1 calibration**: the routed-defect ledger `{LANE}/corpus/routed-defects.json` (49 base rows + 51 rows for the routed items of the closure spot-checks of rounds 50-56; set `{E}/c1/defects.json`) agrees with the tree; counter `{E}/c1/measure.py` (amendments 1 and 2, docstring A1-A9); dry run `bash {WV}/dry-c1.sh` (scratch overlay; `LEDGER=<file>` overrides the ledger).
- **C2 operability**: three executed registry gate rows for `tools/receipt-revision-gate.py`, a SKILL registry row and a true standing-rules cell, all landed; counter `{E}/c2/measure.py`.
- NO-HARM: the round-21 cold-read monitor must read 64/64 at the deciding revision. At C0b it reads 46/64: eighteen headings lost credit because C0/C0b changed pinned inputs (QUALITY, README, SOURCES, tools/registry.json, SKILL rows). The eighteen readers of this wave are the repair; the L1 binds their reports.

# Deliverables discipline
- Report `{WD}/<your-seat-name>.md`; machine-readable output beside it `<your-seat-name>.json`; receipts under `{WD}/<your-seat-name>-receipts/`. Anything you would change is STAGED under `{WD}/<your-seat-name>/stage/<repo-relative-path>`; NEVER edit a lane file in place; never edit a frozen path under `{LANE}/.ufo/evidence/round-5[0-6]/`.
- Scratch: `export HYAKU_SCRATCH=/fast/scratch/hyaku; S=$HYAKU_SCRATCH/tameshi-r57/<your-seat-name>; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT`; `/tmp` only for files under 50 MB; tools you write honour `TMPDIR`/`--work`.
- Clones: `git clone --shared {LANE} "$S/clone"` then `git -C "$S/clone" checkout --detach <rev>`; every git call names `-C`. NEVER run a mutating git/jj command in the lane or the fleet repo. Fixture repos: `D=$(mktemp -d -p "$S")`, `git -C "$D" init -q`, verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before a commit there; commit only with `-c user.name=fixture -c user.email=fixture@example.invalid` and `-C "$D"`.
- Never message agent://all; message only your own L1 (`TameshiR57`) when blocked.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; first read `/home/vgpnk/.omp/agent/RULES.md`; record tool/version/channel/reason in your report. All pacman transactions are PAUSED host-wide: install via `uv tool` / `npx` / an official binary in `~/.local/bin`; never `pacman -S/-Sy/-Syu/-U/-R`, never downgrade, never restart a host service.
- An attack that finds nothing must show the sweep it ran (command + output). A finding without a command and its output is not a finding. An unrun check has not passed.

# Reader contract (seats named `T57W3Read*`)
1. Compute your section's sha256 with the FROZEN round-18 sectionize at C0b - never reimplement it: a python3 snippet that loads `{LANE}/.ufo/evidence/round-18/measure.py` with `importlib`, reads `git -C {LANE} show {C0}:SKILL.md`, calls `m.sectionize(raw)` and prints `sec['start'], sec['end'], sec['sha256']` for your heading. Your JSON's `section_sha256` MUST be that value and `cand` MUST be `{C0}`.
2. Read the section end to end as a reader who must act on it: every command must exist and run; every pointer must resolve; every claim must be true of the tree at C0b; no contradiction with another section. Work in a scratch clone detached at C0b (the lane working tree holds uncommitted instrument files that are not part of C0b).
3. Write `{WD}/<your-seat-name>.json` with keys `seat`, `heading`, `cand` (40-hex), `section_sha256`, `section_start`, `section_end`, `findings` (list; only statements that are FALSE or commands that FAIL, each with the command and its output), `notes` (list; improvements, stale-but-true, style), `commands` (non-empty list), `verdict` (`verified-record` when `findings` is empty, else `gap-minor`), and `{WD}/<your-seat-name>.md` beside it naming the heading and the commands you ran.
4. Do NOT edit `SKILL.md`: a text fix costs a re-read of the section after the round's content is frozen; findings are adjudicated by the L1 and deferred to round 58. A finding without a command and its output is not a finding.
"""

ITEMS = []


def add(name, role, axes, milestone, item):
    ITEMS.append({"name": name, "role": role, "axes": axes, "milestone": milestone, "item": item})


# ---- 18 readers ----
for n, s in enumerate(lost, 1):
    h = s["heading"]
    add("T57W3Read%02d" % n, "reviewer", ["calibration"], "cold-read re-read %d/18" % n,
        f"Read and certify ONE SKILL.md section at C0b = `{C0}`. Heading: `{h}` (it starts near line {s['start']} at C0b; recompute with the frozen sectionize). The monitor lost its credit because: `{s['reason'][:200]}`. Follow the Reader contract in this context exactly: compute `section_sha256` with the frozen sectionize, read the section end to end, run its commands in a scratch clone detached at `{C0}`, check its pointers, write `{WD}/T57W3Read{n:02d}.json` and `.md`.")

# ---- 3 blind re-seats ----
for a, b in (("R51.5", "R51.6"), ("R52.5", "R52.6"), ("R54.2", "R54.3")):
    seat = "T57W3Reseat" + a.replace(".", "") + b.replace(".", "")
    add(seat, "reviewer", ["calibration"], f"blind re-seat {a} {b}",
        f"BLIND PANEL RE-SEAT for routed items `{a}`, `{b}` (a first seat disclosed a blindness breach; you give the clean verdict). You judge the state of each item AT THE LANE BASE `{BASE}` and nothing else. BLINDNESS RULES (a breach voids your verdict): work ONLY in a scratch clone checked out detached at `{BASE}` (`git clone --shared {LANE} \"$S/clone\"; git -C \"$S/clone\" checkout --detach {BASE}`) and read ONLY files in that clone; do NOT read anything under `{LANE}/.ufo/waves/round-57/`, `{LANE}/.ufo/evidence/round-57/`, the lane working tree, any ledger row for these ids, and do NOT run any git command against the lane working tree (including `status`). The item text is in `corpus/lessons/round-NN-verifier-spotcheck.md` of the clone (NN = the digits after R); ids: the bold label `**R<NN>.<n>` if present, else the 1-based position among all items under the routed heading (R51.2 is the second item); round 54 also has `**R54.10`. Decide from the clone's bytes and git history up to `{BASE}`: `fixed` = a lane commit AFTER the spot-check file was added changed the cited surface so the defect no longer holds (name the commit and the line that now holds); `open` = the defect still holds, or only part of it was closed; `declined` = not the lane's to fix or withdrawn by the closure itself (say who and where). Re-derive with a command; do not trust the item's words or any later lesson's claim of a fix without checking bytes. Output `{WD}/{seat}.json` as {{\"seat\":..., \"verdicts\": {{\"<id>\": {{\"verdict\": \"fixed|open|declined\", \"basis\": \"<=60 words with command/path:line\", \"commit\": \"<40-hex or null>\"}}}}}} and a short report.")

# ---- 6 row writers ----
ROWS = [("R51.4", "R51.6"), ("R53.7", "R54.2"), ("R54.3", "R54.4"), ("R54.6", "R54.7"), ("R54.8", "R54.9"), ("R55.1", "R55.3")]
for a, b in ROWS:
    seat = "T57W3Row" + a.replace(".", "") + "x" + b.replace(".", "")
    add(seat, "scribe", ["calibration"], f"ledger rows {a} {b}",
        f"Write the ledger rows `{a}` and `{b}` as adjudicated against the blind panel. Starting ledger: `{WD}/attack-ledger.json` (the working ledger; your two rows exist there with the wave-1 triage status and may be wrong). The independent verdicts are in `{LANE}/.ufo/waves/round-57/w2/T57W2Panel*.json` (grep your ids; `verdict`, `basis`, `commit`); the wave-2 repair notes for these ids are in `{LANE}/.ufo/waves/round-57/w2/T57W2Repair*.md`. The L1's adjudication: adopt the panel verdict as BOTH `status` and `status_at_base` (nothing is fixed this round for these ids) except where you PROVE the panel wrong with a command - then keep the triage status and say so loudly. Per status: `fixed` = commit (full 40-hex, ancestor of the base, introduced the excerpt, ties to the item: the commit message names the id OR the evidence path/basename occurs in the item text OR the panel's commit equals yours), evidence = a lane line that now holds; `open` = evidence is the lane line that still shows the defect (a lane file, not a spot-check, not the ledger; a `.ufo/waves/` or `.ufo/reports/` path is admitted only when it ENDS with one of the item's keys), the id is later named in SCORECARD's Planned paragraph by the L1; `declined` = `reason` >= 40 chars plus evidence. Every evidence excerpt is verbatim (15-400 chars, whitespace-normalised), span <= 30 lines, and contains a key of the item from `{E}/c1/defects.json` as a WHOLE token. Verify with `python3 {WV}/patch-ledger.py {WD}/attack-ledger.json {WD}/{seat}/rows.json $S/ledger.json` then `LEDGER=$S/ledger.json bash {WV}/dry-c1.sh 80` - your two ids must not appear in any EXPLAIN fault line (a `panel-pin` line and `panel-disagree` lines are expected while the panel is unpinned). Output `{WD}/{seat}/rows.json` (list of the two full row objects with `status_at_base`) and the report; an id with no admissible evidence is reported `unrepairable` with the sweep, never padded.")

# ---- instruments / attacks ----
add("T57W3ExecC1SelftestA2", "executor", ["calibration"], "C1 selftest for amendment 2",
    f"Extend the C1 counter's selftest for amendment 2 (read `{E}/c1/measure.py` docstring A7-A9 and the code: `npath`, `panel_provenance`, the `pcommits`/`panel_tie` tie in `judge`). Stage the full updated file at `{WD}/T57W3ExecC1SelftestA2/stage/.ufo/evidence/round-57/c1/measure.py` with `python3 measure.py --selftest --work DIR` printing `C1_R57_SELFTEST: n/n pass` and every amendment-2 arm proven live: (A7) evidence path `./corpus/lessons/round-50-verifier-spotcheck.md` and `corpus//x` are refused like their canonical forms (HARD, spot-check exclusions) while a canonical admissible path still passes; (A8) a fixed row whose commit names no id and whose evidence path is not in the item text passes ONLY when the panel's `detail[id].commit` is a prefix of the row commit, and fails when the panel commit differs or the panel verdict for the id is not `fixed`; (A9) `panel_prov`: missing seat file, wrong sha in `files`, verdict mismatch between panel.json and the seat file, seat absent from `w2-results.json`/`w3-results.json`, a `T57W3` seat resolved under `w3/`, all count; a clean panel counts 0. Do not change the pins or the verdict-line shape. Keep the existing 96 cases green. Report n.")
add("T57W3MutC1A2", "mutation-tester", ["calibration"], "mutate amendment 2",
    f"Poll (file existence, at most 12 times at two-minute intervals) for `{WD}/T57W3ExecC1SelftestA2/stage/.ufo/evidence/round-57/c1/measure.py`; if absent use `{E}/c1/measure.py`. Build 10 single-edit mutants of the amendment-2 code only (npath normpath removed; `panel_tie` prefix test `startswith(pc[:40])` -> always true / `len(pc) >= 7` dropped; pcommits restricted to `fixed` verdicts dropped; provenance sha check removed; provenance verdict-equality removed; `listed` check removed; w3 path routing removed; `panel_prov` not added to TERMS; panel_prov count not assigned; provenance loop skipping ids) in fresh scratch copies (assert unique old strings) and run each against the selftest. Report KILLED/SURVIVED per mutant; give survivors a proposed case. Output `{WD}/T57W3MutC1A2.json`.")
_attack_ids = [i for i in json.load(open(WD + "/attack-ledger.json"))["defects"][49:]]
_skip = {"R51.4", "R51.6", "R53.7", "R54.2", "R54.3", "R54.4", "R54.6", "R54.7", "R54.8", "R54.9", "R55.1", "R55.3"}
_att = [r["id"] for r in _attack_ids if r["id"] not in _skip]
assert len(_att) == 39
for k in range(3):
    g = _att[k * 13:(k + 1) * 13]
    add("T57W3RowAttack%d" % (k + 1), "reviewer", ["calibration"], f"attack ledger rows {g[0]}..{g[-1]}",
        f"Attack the semantic support of these ledger rows in `{WD}/attack-ledger.json` (the working ledger; the counter checks presence, keying, introduction and tie but NOT that an excerpt resolves the defect): {', '.join(g)}. For each: read the item (`{E}/c1/defects.json` text and the spot-check line), the row's status, commit and evidence, and decide with commands whether (a) the excerpt really shows the defect fixed / still open / not the lane's, (b) the commit is the fix of THIS item and not an unrelated edit that happens to touch the path, (c) for `open` rows the defect still holds at the lane tip `git -C {LANE} rev-parse master` (a later commit may have fixed it: check `git -C {LANE} log` on the cited paths) and for `fixed` rows it still holds fixed. Output `{WD}/T57W3RowAttack{k+1}.json` `[{{id, verdict: supported|weak|wrong, reason, proposed_fix}}]` and a report; a `wrong` verdict needs the command that shows it. Never edit.")
add("T57W3CritContract", "critic", ["calibration"], "audit the final contract against the counters",
    f"Audit `{E}/contract.json` (final text, amendments 1 and 2, panel block) against the counters `{E}/c1/measure.py` and `{E}/c2/measure.py`: for each claim the predicate/target sentence must be the same sentence in the contract, the counter's docstring/code and the verdict line tokens (list each token and the clause it counts), contain no universal clause without an enumerating command, and name no value the counter does not compute; the `before` receipts it cites must exist or be produced by the L1 before the freeze (list the paths that do not exist yet: `{E}/before/`); `frozen_paths` must list every instrument the deciding run reads (diff against `{E}/deciding-run.sh`, `controls.sh`, `no-harm.sh`, `bind` inputs). Report defects with the exact replacement sentence as a staged `diff -u` under `{WD}/T57W3CritContract/stage/`. Never edit.")
add("T57W3RevControlsDry", "reviewer", ["operability"], "controls and deciding-run end to end",
    f"Run the whole controls harness `bash {E}/controls.sh {LANE} {BASE} <REV> <OUTDIR>` end to end in scratch with REV = the lane's current master (`git -C {LANE} rev-parse master`), overlaying the uncommitted instruments the way `{WV}/dry-c1.sh` does (read `{LANE}/.ufo/waves/round-57/w2/T57W2ExecControls.md` for the overlay protocol), with a synthetic panel + pins in the scratch clone where the real ones do not exist yet; report every CTL line, CONTROLS_A and CONTROLS_B tallies and any CTL_MISMATCH with its cause. Then dry-run `{E}/deciding-run.sh` the same way and report each refusal path it takes (missing freeze.json, missing panel pin, REV != HEAD) and its exact strings. Fix proposals as staged diffs under `{WD}/T57W3RevControlsDry/stage/.ufo/evidence/round-57/`. Never edit the lane.")

spec = {"wave": "round-57-w3", "reportDir": ".ufo/waves/round-57/w3", "template": TEMPLATE, "context": CONTEXT, "items": ITEMS}
Path(WV, "spec-w3.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
roles = {}
for it in ITEMS:
    roles[it["role"]] = roles.get(it["role"], 0) + 1
print("items", len(ITEMS), roles)
