#!/usr/bin/env python3
"""Build round-56 wave-2 spec (v1 band 32-64): 18 cold-read readers at C0 + 16 pre-bind checks.

C0 is the content commit the readers read; pass it as argv[1] (full 40-hex).
"""
import json
import sys
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
BASE = "981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1"
FREEZE = "c3e2ca9f020776b3d66c7af854fb82c834674fcf"
W = ".ufo/waves/round-56/w2"
E = LANE + "/.ufo/evidence/round-56"

C0 = sys.argv[1]
assert len(C0) == 40, C0

TEMPLATE = Path(LANE, '.ufo/waves/round-56/build-spec-w1.py').read_text('utf-8').split('TEMPLATE = """', 1)[1].split('"""', 1)[0]

CONTEXT = f"""# Goal
tameshi round 56 (hyaku run 11; L1 TameshiR56), wave 2 of three: the eighteen cold-read readers at the content commit C0 = `{C0}`, plus the pre-bind checks of what wave 1 produced. Lane repo {LANE} (absolute paths only: seat tools start at the fleet root /home/vgpnk/Projects/shokunin). Base `{BASE}`; frozen instruments `{FREEZE}`.

# What this wave is for
Round 55 was rejected-harmed because its own edits cost the round-21 cold-read monitor 18 of 64 credited sections and the re-key never landed (R55.3). The repair is mechanical and this wave is its read half: at C0 the eighteen headings below must be re-read by a fresh reader, and each reader's `section_sha256` is what the round-55 binder binds into `.ufo/evidence/round-21/coldread/ledger.json` under one `rekey-r56-<c0>` directory. A reader report that is not committed, names the wrong `cand`, or carries a hash the tree does not produce is refused by the binder and the round stops.

# The eighteen frozen headings (one reader seat each)
`{E}/c1/lost-headings-at-base.json` — every one lives in `SKILL.md`. Your item names yours.

# The claims (contract `{E}/contract.json`, frozen before any seat ran)
- **C1 calibration** (lowest non-retired axis). Target `C1_R56_PASS=true`: precheck `lost=0`, monitor `64/64 score=8 box3=true`, one `rekey-r56-<c0>` with 18/18 headings bound at `read_rev=C0`, 18/18 reader reports, no LOG/SCORECARD input, and the standing calibration row stating the monitor's own score. Counter: `python3 {E}/c1/measure.py --lane {LANE} --rev <rev> --work <empty dir> --explain`.
- **C2 operability** (sourced). Target `C2_R56_PASS=true`: `{LANE}/tools/receipt-revision-gate.py` refuses the real receipts rounds 54/55 accepted, the round's own receipts pass it at the certified revision, and the rule is stated in QUALITY, a sourced knowledge entry, SKILL.md and the registry. Counter: `python3 {E}/c2/measure.py --lane {LANE} --rev <rev> --work <empty dir> --explain`.

# Reader contract (the seats named `T56W2Read*`)
1. Compute your section's sha256 with the FROZEN round-18 sectionize at C0 — never reimplement it:
   `python3 - <<'PY'` with `importlib` loading `{LANE}/.ufo/evidence/round-18/measure.py`, `git -C {LANE} show {C0}:SKILL.md`, `m.sectionize(raw)`, then print `sec['start'], sec['end'], sec['sha256']` for your heading. Your JSON's `section_sha256` MUST be that value and `cand` MUST be `{C0}`.
2. Read the section end to end as a reader who must act on it: every command must exist and run; every pointer must resolve; every claim must be true of the tree at C0; no contradiction with another section.
3. Write `{LANE}/{W}/<your-seat-name>.json` with keys `heading`, `cand` (40-hex), `section_sha256`, `findings` (list; only statements that are FALSE or commands that FAIL, each with the command and its output), `notes` (list; improvements, stale-but-true, style), `commands` (non-empty list), `verdict` (`verified-record` when `findings` is empty, else `gap-minor`), and `{LANE}/{W}/<your-seat-name>.md` beside it naming the heading and the commands you ran.
4. Do NOT edit `SKILL.md`. A text fix costs eighteen re-reads, so findings are adjudicated by the L1 and deferred to round 57, named in the lesson. A finding without a command and its output is not a finding.

# Deliverables discipline
- Write into `{LANE}/{W}/<your-seat-name>.md` (and the `.json` the item asks for); receipts under `{LANE}/{W}/<your-seat-name>-receipts/`.
- Never edit a lane production file (`SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**`, `tools/**`) or a frozen instrument under `.ufo/evidence/round-56/`. The L1 integrates.
- Scratch: `export HYAKU_SCRATCH=/fast/scratch/hyaku; S=$HYAKU_SCRATCH/tameshi-r56/<your-seat-name>` with `trap 'rm -rf -- "$S"' EXIT`; `/tmp` only for files under 50 MB; clones are `git clone --shared` then `git -C <clone> checkout --detach <rev>`.
- Never run a mutating git/jj command anywhere. Fixtures: `D=$(mktemp -d)` under your scratch, every git call names `-C "$D"`, and `git -C "$D" rev-parse --show-toplevel` must equal `$D` before any commit there.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task - read `/home/vgpnk/.omp/agent/RULES.md` first (official channels, update-safety gate) and record tool/version/channel/reason in your report. **pacman transactions are PAUSED host-wide**: install via `uv tool`/`npx`/an official binary in `~/.local/bin`, or route around it.
- Every `Report:` trailer path the harness renders is relative to {LANE} - write it at {LANE}/<that path>. Never message `agent://all`; message only your own L1 (`TameshiR56`).
- An attack that finds nothing must show the sweep it ran. A finding without a command and its output is not a finding.

# Census
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` must exit 0 (141 rows after this round's one new row)."""

HEADINGS = json.loads(Path(LANE, '.ufo/evidence/round-56/c1/lost-headings-at-base.json').read_text())
# start/end at base, for the reader's orientation (recomputed at C0 by the seat)
SECTIONS = [
    ("## Context gate classification and explicit exit classes — round 15", 1639, 1705),
    ("## Effective expectation reconciliation — round 14", 1593, 1626),
    ("## Live-tree re-pin and entry-command monitor — round 17", 1844, 1875),
    ("## Mutation-sweep recipe — numbered steps; bounded cold-read evidence", 146, 260),
    ("## Pin disposition and provenance correction — round 13", 1546, 1576),
    ("## Repeated controls and gate registry — round 12", 1508, 1527),
    ("## Standing rules", 17, 44),
    ("## The leg ledger — replay, receipt, and how it is read (round 7, measured)", 936, 949),
    ("## The operator's runbook and the six-leg regression (round 10, measured)", 1299, 1307),
    ("### Gate/probe registry", 1528, 1545),
    ("### Round-13 gate/probe registry", 1577, 1592),
    ("### Round-15 gate/probe registry", 1706, 1736),
    ("### Round-17 gate/probe registry — re-pin and monitor", 1876, 1884),
    ("### Round-18 gate/probe registry — routed-defect closure", 1955, 1967),
    ("### Round-21 gate/probe registry — finite environment differential", 1994, 2133),
    ("### Round-26 gate/probe registry — report interop", 2162, 2201),
    ("### The service's limits — what tameshi refuses to mutation-test", 1269, 1298),
    ("### Triggers T1–T3 and the re-pin rule", 1087, 1109),
]
assert sorted(h for h, _, _ in SECTIONS) == sorted(HEADINGS), 'heading set mismatch'

ITEMS = []


def add(name, role, axes, milestone, item):
    ITEMS.append({"name": name, "role": role, "axes": axes, "milestone": milestone, "item": item})


for n, (heading, start, end) in enumerate(SECTIONS, 1):
    add("T56W2Read%02d" % n, "reviewer", ["calibration"], "cold-read re-read %d/18" % n,
        f"Read and certify ONE SKILL.md section at C0 = `{C0}`. Heading: `{heading}` (at base it sat at lines {start}-{end}; recompute at C0). Follow the Reader contract in this context exactly: compute the section sha with the FROZEN round-18 sectionize at C0, read the section end to end (`git -C {LANE} show {C0}:SKILL.md`, the section's line range), run every command the section tells a reader to run (in a scratch clone at C0), and write `{LANE}/{W}/T56W2Read{n:02d}.json` + `.md`. `cand` = `{C0}`. Findings only for statements that are FALSE or commands that FAIL, each with the command and its output; improvements go in `notes`. Verdict `verified-record` when `findings` is empty, else `gap-minor`. Do not edit SKILL.md. Your JSON is what the round-55 binder binds into the cold-read ledger: a wrong `section_sha256`, a wrong `cand` or a missing `.md` stops the round.")

add("T56W2ExecC0Receipts", "executor", ["calibration"], "C0 drift set",
    f"Produce the C0 receipts the L1 records: (a) the precheck `bash {LANE}/.ufo/evidence/round-48/quality/coldread-precheck.sh {LANE} 0a2010acd1e92e4e332774050825e21bcfc7e079 {C0}` — expect RED with exactly the 18 frozen headings lost (the round-55 base read 64/64, so any heading lost at C0 beyond the 18 is a NEW cost and must be named); (b) the round-21 monitor at C0 (`covered`, `score`, `box3`); (c) the drift set as a JSON list. Report the three outputs and, for each lost heading, its reason string. If the lost set is not exactly the 18, say so loudly: the L1's C0 is then wrong. Scratch only; write nothing outside `{LANE}/{W}/`.")

add("T56W2ExecSchemaSelf", "executor", ["operability"], "reader validator selftest",
    f"Run the wave-1 tool `{LANE}/.ufo/waves/round-56/validate-readers.py --selftest` at C0 and report its tally. If the tool is missing or its selftest fails, write the tool yourself to the spec in `{LANE}/{W}/T56W1ExecReaderSchema.md` (read it first) and demonstrate every refusal firing. Then validate the reader JSONs that have landed so far in `{LANE}/{W}/` (report how many were present at your run — the wave is concurrent, so a partial count is expected and must be stated as such). Never edit a reader's JSON.")

add("T56W2ExecGateOnC0", "executor", ["operability"], "gate against the round's own C0 receipts",
    f"Run `{LANE}/tools/receipt-revision-gate.py` at C0 on the receipts that exist at C0: the before receipts (`{E}/before/c1.stdout`, `{E}/before/c2.stdout`), the C0 precheck stdout, and the C0 monitor dump, each as `verdict` against `--certified {C0}` with `--paths {E}/control/frozen-surface.paths`. Report every refusal with its code and decide whether each refusal is CORRECT (a receipt that names no revision cannot certify one) or a defect of the gate. Then show the accept arm: a receipt that names `{C0}` passes. This is the gate being used on the round's own bytes before the deciding run; report the exact command the L1 should cite.")

add("T56W2RevSources", "reviewer", ["freshness"], "independent source re-open",
    f"Re-open the external source the round added to `{LANE}/corpus/SOURCES.md` at C0 (find the new row: the highest S-number). Fetch its URL yourself, locate the quoted passage, and check: the row's `anchor` names a section that exists at that URL, its `teaches` is grounded by the passage, its `tier`/`kind`/`scope` follow `{LANE}/corpus/QUALITY.md`'s definitions, `opened` is today's date, `used-by` names `corpus/knowledge/receipt-revision-binding.md` (which must exist at C0 and cite the row), and the URL is not a within-scope duplicate (`grep -n` the fragment in `corpus/SOURCES.md`). Then re-run the census and report exit/rows. Report agree/disagree per check with the fetched text quoted.")

add("T56W2RevQuality", "reviewer", ["calibration"], "QUALITY criterion falsifier",
    f"Verify the new `corpus/QUALITY.md` criterion (the highest number at C0) actually says what the claim needs and that its falsifier fires: run the exact command the criterion names and check it prints the refusal code the criterion names, on the real receipt `{E}/c2/red-before/round-54-ctl-pos-c1.stdout`; then run it on a receipt that names the certified revision and check it does NOT refuse. Report: the criterion's number, its rule in one sentence, the command, both outputs, and any mismatch between what it claims and what the gate does. Also check it cites `corpus/lessons/round-56.md` and the `considerthese/2026-10-28.md` pointer with a date.")

add("T56W2RevSkillScope", "reviewer", ["calibration"], "SKILL.md drift scope",
    f"Prove the round's SKILL.md edit is confined to ONE section: `git -C {LANE} diff {BASE} {C0} -- SKILL.md` must show exactly one hunk inside `## Standing rules` and nothing else. Then, for each of the other 17 frozen headings, confirm its bytes at C0 equal its bytes at base (`git show {C0}:SKILL.md` sectionized vs `{BASE}`, section by section) — a heading whose text changed is a reader obligation the round did not price. Report the hunk, the per-heading equality table, and the sha256 of the section the readers must read.")

add("T56W2RevFreeze2", "reviewer", ["calibration"], "instruments unchanged at C0",
    f"Check that every frozen instrument is byte-identical between the freeze `{FREEZE}` and C0: `git -C {LANE} diff {FREEZE} {C0} -- {E}/contract.json {E}/freeze.json {E}/c1/measure.py {E}/c1/lost-headings-at-base.json {E}/c2/measure.py {E}/control/frozen-surface.paths {E}/c2/red-before/round-54-surface.paths {E}/no-harm.sh {E}/deciding-run.sh {E}/controls.sh {LANE}/tools/receipt-revision-gate.py` must print nothing. Then re-derive `freeze.json`'s digests from the C0 bytes and confirm they match. Report both with the exact output. If anything differs, name it: an instrument that changed without an amendment voids the freeze.")

add("T56W2RevCensusAfter", "reviewer", ["freshness"], "census after C0",
    f"Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` and report exit code, trailer, row count and warnings. Compare with the base count (140) and name every added row. Then check the new row by hand against contract v1 (11 columns, no literal or escaped pipe, valid enums, ISO dates, `used-by` resolving to a file that exists at C0). Report the row count before->after and the row's verdict.")

add("T56W2SentReaders", "sentinel", ["operability"], "reader-report tampering",
    f"Attack the bind path. On a scratch clone at C0 with a synthetic wave dir, craft and test: (1) a reader JSON with the right `section_sha256` but `cand` set to the base revision; (2) a correct JSON with no `.md` beside it; (3) a JSON whose `heading` matches but whose section was never read (hash copied from a sibling section); (4) a JSON with `findings` as a string instead of a list; (5) two JSONs for the same heading with different hashes. For each, run the wave-1 validator (`validate-readers.py`) and the round-55 binder on the synthetic dir, and report whether each is refused, which refusal it prints, and whether a binder `SKIP` is produced. State the residual: which of these could reach the ledger if the L1 ran the bind without the validator.")

add("T56W2CritDoNothingC1", "critic", ["calibration"], "C1 do-nothing control",
    f"Build the cheapest tree that skips C1's claimed work and score it with the frozen counter. Attempts, each in a scratch clone at C0: (1) delete the eighteen headings' ledger entries entirely — does the monitor then credit 64/64? (2) edit the standing calibration row to the score the monitor reads at base (6) and change nothing else; (3) re-pin one entry's inputs to C0 without a reader report; (4) add a `rekey-r56-<c0>` directory with traces but no reader JSONs. For each: the counter's verdict line and whether it reaches `C1_R56_PASS=true`. Report the control scores; if any reaches the target the counter or the target is wrong and you must say so with the receipt.")

add("T56W2CritDoNothingC2", "critic", ["operability"], "C2 do-nothing control",
    f"Build the cheapest tree that skips C2's claimed work and score it with the frozen counter, in scratch clones at C0: (1) add the docs text (QUALITY mention, knowledge file, SKILL bullet, registry cell) but no control receipts at all; (2) add two files under `.ufo/evidence/round-56/control/` that merely contain the string `rev={C0}` and a `CONTROLS_A: 7/7 as pre-registered` line; (3) copy the round-54 slice with its `rev=` rewritten to the certified revision; (4) delete the red-before receipts so the arms error instead of refuse. For each: the counter's verdict line, which arm moved, and whether it reaches `C2_R56_PASS=true`. Name the weakest text that still scores `docs=4/4` and say whether that is enough.")

add("T56W2MutGateOnC0", "mutation-tester", ["operability"], "gate mutants against C0",
    f"Run the wave-1 gate mutant set again at C0 (the gate is frozen and unchanged): 8 single-edit mutants, one exact edit each in a fresh scratch clone, each must be killed by `--selftest`. Mutants: drop `RECEIPT_REV_ABSENT`; `drifted_paths` returns `[]`; `is_ancestor` always true; skip the digest check; allow multiple revs in a positive role; skip the required-line check; treat an empty file as present; drop `RECEIPT_CONTROL_NOT_ANCESTOR`. Report KILLED/SURVIVED per mutant with the failing case name and the receipt. A survivor is a hole in the selftest and a finding.")

add("T56W2RevNoHarmC0", "reviewer", ["freshness"], "no-harm at C0",
    f"Run `{E}/no-harm.sh {LANE} {C0}` and report every line. Expected: the cold-read floor RED (the 18 headings are not bound yet) and every other monitor ok. Name any monitor that is RED for a reason other than the cold-read floor, and say whether the round's content caused it. Then verify that each RED line is the one the deciding run will require to be ok, and list the monitors the deciding run counts (15).")

add("T56W2ConnectorSeparability", "connector", ["adjacency"], "claim separability and sibling overlap",
    f"Two jobs. (a) Separability: demonstrate on scratch clones at C0 a tree where C1 holds and C2 fails (bind the re-key, leave the docs absent) and one where C2 holds and C1 fails (add the docs and own receipts, leave the 18 headings unbound). Report both counters' verdict lines for each tree. (b) Sibling overlap on the final bytes: `grep -rn` the sibling lanes (`/home/vgpnk/Projects/shokunin/*-shokunin/`) for the gate's rule (`rev=` binding, provenance, attestation, digest binding) and report whether tameshi's C2 duplicates a sibling's owned rule, complements it, or is contested. One verdict line (`overlap=none|complement|contest`) and one row per hit. Never edit a sibling file.")

add("T56W2RevStalePointers", "reviewer", ["freshness"], "new-pointer resolution",
    f"Resolve every pointer the round's new content introduces at C0: the SOURCES row's URL/anchor, the knowledge entry's `S###` citation and its URL, the QUALITY criterion's command and code, the SKILL bullet's gate path, the registry cell's selftest command, and any `corpus/lessons/round-56.md` reference. For each: the pointer, the resolution command, the observed value, and ok/stale. A pointer that resolves to a different line than claimed is `stale` and must be named with the correct value. Report the table.")

add("T56W2ExecGateSelf", "executor", ["operability"], "gate selftest at C0",
    f"Run `python3 {LANE}/tools/receipt-revision-gate.py --selftest` from a copy of the C0 bytes in a scratch dir and report `GATE_SELFTEST: n/n pass` plus every case name. Then run the same selftest with `TMPDIR` pointing at a set-but-unusable directory (a regular file) and report what the tool does — a scratch-root refusal or a crash — and whether that is acceptable for a tool this round asks a reader to run. Report both outputs verbatim.")

spec = {"wave": "round-56-w2", "reportDir": ".ufo/waves/round-56/w2",
        "template": TEMPLATE, "context": CONTEXT, "items": ITEMS}
out = Path(LANE, ".ufo/waves/round-56/spec-w2.json")
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
roles = {}
for it in ITEMS:
    roles[it["role"]] = roles.get(it["role"], 0) + 1
print("items", len(ITEMS), roles, "c0", C0[:12])
