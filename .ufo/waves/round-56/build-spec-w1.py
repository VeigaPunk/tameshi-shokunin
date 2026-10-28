#!/usr/bin/env python3
"""Build round-56 wave-1 spec (v1 band 32-64: build, recon and the first falsifiers)."""
import json
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
BASE = "981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1"
FREEZE = "c3e2ca9f020776b3d66c7af854fb82c834674fcf"
W = ".ufo/waves/round-56/w1"

TEMPLATE = """/skill:godspeed
You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls.

## Your item

{{item}}

Work the item end to end, then write your report file and return your findings.
"""

CONTEXT = f"""# Goal
tameshi round 56 (hyaku run 11; L1 TameshiR56), wave 1 of three: build the round's content and instruments' falsifiers. Lane repo {LANE} (absolute paths only: seat tools start at the fleet root /home/vgpnk/Projects/shokunin, so every read/edit/write names an absolute path under the lane). Base `{BASE}`; frozen instrument set `{FREEZE}` (`.ufo/evidence/round-56/`).

# Why this round exists (round 55 was rejected-harmed)
The non-author closure (`{LANE}/corpus/lessons/round-55-verifier-spotcheck.md`) rejected round 55: the round's own edits cost the cold-read monitor 18 of 64 credited sections (64/64 score 8 -> 46/64 score 6) and the 18-heading re-key never landed (R55.3); no C2 verdict named the measured revision (R55.1); a quoted total its own receipt contradicted (R55.2); a stale control sentence (R55.4); the deciding gate cannot compare the revision it certifies (R55.5); uncommitted round work at closure (R55.6); closure-seat contamination of the lane tree (R55.7). Round 56 repairs R55.3 (C1) and R55.5 (C2) and disposes the rest.

# The two claims (contract `.ufo/evidence/round-56/contract.json`, frozen before any seat ran)
- **C1 calibration** (the lowest non-retired axis: the monitor reads 6 at base; the standing row still asserts 8 — R55.3). The 18 base-lost cold-read headings are re-read at one content commit C0, bound under one `rekey-r56-<c0>` directory, the precheck reads `lost=0` / monitor `64/64 score=8 box3=true`, and the standing calibration row states the monitor's own score at the commit it names. Counter: `python3 {LANE}/.ufo/evidence/round-56/c1/measure.py --lane {LANE} --rev <rev> --work <empty dir> --explain`. Before at base: `C1_R56: rev=981c5e8b20a2 c0=none credited=46 lost=18 rekeyed=0/18 readers=0/18 monitor=6/46 unstable=0 restate=8 total=5 C1_R56_PASS=false` (`{LANE}/.ufo/evidence/round-56/before/c1.stdout`).
- **C2 operability** (sourced claim). Every receipt the lane certifies is bound to the revision it was measured against, by `{LANE}/tools/receipt-revision-gate.py`, and the gate refuses the real receipts the lane accepted in rounds 54 and 55. Counter: `python3 {LANE}/.ufo/evidence/round-56/c2/measure.py --lane {LANE} --rev <rev> --work <empty dir> --explain`. Before at the freeze: `C2_R56: rev=c3e2ca9f0207 selftest=14/14 red54=RECEIPT_REV_CONTENT_DRIFT red54b=RECEIPT_REV_UNRESOLVABLE red55=RECEIPT_REV_ABSENT own=own-receipts-missing docs=0/4 total=2 C2_R56_PASS=false` (`{LANE}/.ufo/evidence/round-56/before/c2.stdout`).

# What wave 1 must produce (the L1 integrates; seats never edit lane production files)
1. **C2 content** (all of it lands in the single content commit C0): the gate's registry cell; `corpus/knowledge/receipt-revision-binding.md` (provenance trio + a `mined` S-row); a `corpus/QUALITY.md` criterion whose falsifier is the gate's own refusal code on the real round-54 receipt; one SOURCES.md row for the source opened this round; the `SKILL.md` `## Standing rules` rule (that section only).
2. **The round's records**: the SCORECARD round-56 block with the restated standing calibration row (the score the monitor actually reads at the commit the row names), the LOG entry, the lesson (`## Gate` + `## Mistakes` + dispositions of R55.1-R55.7), and the report skeleton.
3. **Falsification of the instruments** (they are frozen; report defects, never edit them): arm liveness for both counters, gate fuzz and mutants, the controls/deciding/no-harm dry runs, the freeze discipline.
4. **Recon**: the 18-heading drift map, the pinned-input set that must not change between PIN and REV, the receipt inventory, the external source opened with a located quote.

# The 18 frozen headings (C1's obligation)
`{LANE}/.ufo/evidence/round-56/c1/lost-headings-at-base.json` — every one needs a fresh reader report at C0 in wave 2. Wave 1's job is the drift map: which file each heading lives in, its section start/end and sha256 at base, its prior pinned inputs, and which of those drifted. A heading whose text must change (only `## Standing rules`) is a content edit for C0; every other heading is re-read, not rewritten.

# Counter facts you may rely on (measured, not asserted)
- Base cold-read: `covered=46 score=6 box3=False`; 18 lost headings; the precheck at base reads `floor=0a2010acd1e9 floor_credited=64 cand=981c5e8b20a2 cand_credited=46 lost=18 RED`.
- The standing calibration row at base asserts `8` at `d33053f7`, where the monitor reads `6`.
- The real round-54 receipt `{LANE}/.ufo/evidence/round-54/control/controls-b.stdout` names `rev=077d431e6996` on its `CTL_POS_c1` line while the round measured `c2108100`, and its `CTL_EXIT0` line names `7df0e0426c98`, a revision absent from this repo; the round-54 gate accepted the set (`{LANE}/.ufo/evidence/round-54/after/deciding-run.exit` reads `DECIDING_RUN_EXIT=0`).
- The committed round-55 C2 receipt `{LANE}/.ufo/evidence/round-55/after/c2.stdout` is truncated mid-run and names no revision.
Re-derive, never trust this list: every item names the command.

# Deliverables discipline
- Write into `{LANE}/{W}/<your-seat-name>.md` (the report) and, where the item asks for a machine-readable list, `<your-seat-name>.json` beside it. Receipts (command output you cite) go under `{LANE}/{W}/<your-seat-name>-receipts/`.
- Never edit a lane production file (`SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/**`, `tools/**`) and never edit a frozen instrument under `.ufo/evidence/round-56/` — the L1 integrates, and the instruments are frozen. A patch you propose is a diff in your report plus a scratch-clone demonstration.
- Write scratch under `export HYAKU_SCRATCH=/fast/scratch/hyaku; S=$HYAKU_SCRATCH/tameshi-r56/<your-seat-name>` with `trap 'rm -rf -- "$S"' EXIT`; `/tmp` only for files under 50 MB. A clone is `git clone --shared` of the lane, then `git -C <clone> checkout --detach <rev>`.
- Never run a mutating git/jj command anywhere (no add/commit/push/checkout of the lane, no jj). Fixtures: `D=$(mktemp -d)` under your scratch, every git call names `-C "$D"`, and `git -C "$D" rev-parse --show-toplevel` must equal `$D` before any commit there.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task - read `/home/vgpnk/.omp/agent/RULES.md` first (official channels, update-safety gate) and record tool/version/channel/reason in your report. **pacman transactions are PAUSED host-wide**: install via `uv tool`/`npx`/an official binary in `~/.local/bin`, or route around it.
- Every `Report:` trailer path the harness renders is relative to {LANE} - write it at {LANE}/<that path>. Never message `agent://all`; message only your own L1 (`TameshiR56`).
- An attack that finds nothing must show the sweep it ran. A finding without a command and its output is not a finding.

# Census (round start and end, conformance)
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` must exit 0; 140 rows now (S001-S280)."""

AX = {
    "exec": ["operability"], "scribe": ["calibration"], "scout": ["freshness"],
    "connector": ["adjacency"], "crit": ["calibration"], "rev": ["calibration"],
    "mut": ["operability"], "sent": ["operability"], "simpl": ["operability"],
}

ITEMS = []


def add(name, role, axes, milestone, item):
    ITEMS.append({"name": name, "role": role, "axes": axes, "milestone": milestone, "item": item})


L = LANE
E = L + "/.ufo/evidence/round-56"

add("T56W1ExecC1Counter", "executor", ["calibration"], "C1 counter arm liveness dry run",
    f"Dry-run the frozen C1 counter `{E}/c1/measure.py` and prove every arm can fire. (a) Run it at base `{BASE}` in an empty work dir and confirm the before line matches `{E}/before/c1.stdout`. (b) Build a scratch clone at the freeze `{FREEZE}`, and in it construct the smallest tree that makes each arm move: remove one ledger entry that a re-key would bind (arm 3 must drop), fabricate one reader JSON under `.ufo/waves/round-56/w2/` with a wrong `section_sha256` (arm 4 must drop), set the standing calibration row to a wrong score (arm 6 must drop), and delete a prior pinned input (arm 5 must fire). (c) Report, per arm, the mutation, the before/after tally and the exact verdict substring that changed. Defects you find are reported, never edited: the counter is frozen. Scratch under `$HYAKU_SCRATCH/tameshi-r56/T56W1ExecC1Counter`, receipts in your `-receipts/` dir.")

add("T56W1ExecGateFuzz", "executor", ["operability"], "receipt-revision gate fuzz",
    f"Fuzz `{L}/tools/receipt-revision-gate.py` (frozen bytes at `{FREEZE}`) with at least 20 crafted receipts and report every accept/refuse with its code: a receipt with no rev; two different revs in a positive role; a rev embedded in a path string (`rev=...` inside a filename); a JSON receipt (`rev` as a JSON string key); a receipt naming the certified rev but produced for another claim; a sidecar `.sha256` that matches and one that does not; a receipt whose rev resolves to a tag rather than a commit; a receipt with `rev=` in a comment line; a 7-hex and a 12-hex prefix; a `rev=` inside a markdown code fence. For each, say whether the gate's answer is the right one for the claim C2 declares (`{E}/contract.json`) and why. Use a scratch git fixture (`mktemp -d` under your scratch) for the revisions; never touch the lane. Deliverable: your report + `-receipts/fuzz.tsv` (case, expected, observed, code).")

add("T56W1ExecC2Counter", "executor", ["operability"], "C2 counter dry run",
    f"Dry-run the frozen C2 counter `{E}/c2/measure.py`. (a) At base `{BASE}` confirm `error=gate-missing` (the claim's subject does not exist there). (b) At the freeze `{FREEZE}` confirm the before line in `{E}/before/c2.stdout` reproduces exactly. (c) Prove arms 2, 3 and 4 each depend on the REAL receipt they name: copy each red-before input into a scratch clone, edit one byte (e.g. change the `rev=` token to the certified revision), and show the arm's code changes. (d) Say precisely which files must exist at the deciding revision for arm 5 (`own`) to pass, and whether the L1's planned order produces them. Report defects; never edit the counter.")

add("T56W1ExecControls", "executor", ["operability"], "controls harness dry run",
    f"Dry-run `{E}/controls.sh` on the freeze revision with a synthetic round-56 tree so every mutation applies: build a scratch clone at `{FREEZE}`, add a fake `rekey-r56-<c0>` ledger entry set and 18 fake reader JSONs with correct section hashes (compute them with the frozen round-18 `sectionize`), commit, then run the harness with `PIN` = that commit. Report: does each phase-A mutation apply (the python heredocs find their needles), does each control print `CTL_MISMATCH`/`CTL_MATCH` as pre-registered, does phase B score the positive controls at the revision it certifies, and does `CONTROLS_A/B: n/m as pre-registered` print. Flag any needle that is fragile against a whitespace change. Receipts in your `-receipts/`.")

add("T56W1ExecNoHarm", "executor", ["freshness"], "no-harm monitor liveness",
    f"Dry-run `{E}/no-harm.sh` at the freeze `{FREEZE}`. Report every line: which are `ok`, which are `RED` and whether that RED is expected before the re-key (the cold-read floor must be RED at the freeze because the 18 headings are unbound). Then prove at least three monitors can fire: mutate a scratch clone (a) to drop one recorded ledger case, (b) to shrink SOURCES.md by one row, (c) to add a `/tmp` literal under `tools/`, and show the matching monitor turns RED. Flag any monitor that cannot turn RED by construction.")

add("T56W1ExecDecidingDry", "executor", ["operability"], "deciding-run refusal matrix",
    f"Prove `{E}/deciding-run.sh` refuses before it runs anything, in a scratch clone at `{FREEZE}`: (a) a tampered freeze manifest file (one digest changed) -> `DECIDING_REFUSED freeze-integrity`; (b) `REV` not equal to HEAD -> `head-is-not-rev`; (c) a missing control receipt -> `control-receipt-missing`; (d) a dirty tree -> `dirty-tree`; (e) a second invocation (`OUT/c1.start` present) -> `second-invocation`; (f) control receipts whose own commit does not descend from the freeze -> `control-receipt-not-after-freeze`; (g) the receipt-binding gate refusing (`receipt-gate.exit` 3) -> `receipt-binding`. Report each refusal with its exit code and the exact line. Note any refusal that cannot fire.")

add("T56W1ExecReaderSchema", "executor", ["operability"], "reader-report validator",
    f"Write `{L}/.ufo/waves/round-56/validate-readers.py` (stdlib only, `--selftest`): for every heading in `{E}/c1/lost-headings-at-base.json`, require a committed JSON under `{L}/.ufo/waves/round-56/w2` or `.../w3` matching `T56W*Read*.json` with keys `heading`, `cand` (40-hex == C0), `section_sha256` (== the sha256 of that section's bytes at C0, computed with the FROZEN round-18 `sectionize` at C0 — never a reimplementation), `findings` (list) and `commands` (non-empty list), plus an `.md` beside it that names the heading and the command it ran. Refuse: missing heading, wrong cand, wrong hash, a JSON without a sibling `.md`, and a JSON whose `findings` is not a list. Selftest must show each refusal firing on a synthetic tree and the accept arm passing. This tool gates the L1's bind; commit nothing.")

add("T56W1ExecBinderWrap", "executor", ["operability"], "re-key bind wrapper",
    f"Write `{L}/.ufo/waves/round-56/bind.sh` (the exact L1 sequence, `set -euo pipefail`): (1) compute the drift set at PIN with the round-21 monitor at the floor `0a2010acd1e9` and at PIN, and refuse if it is not exactly the 18 frozen headings; (2) run the round-55 binder `{L}/.ufo/waves/round-55/w1/T55W1ExecReKeyDryBind-receipts/binder-r55.py` with `--headings`, `--waves .ufo/waves/round-56/w2`, `--label 'L1 TameshiR56 re-key (round 56)'`, output `{L}/.ufo/evidence/round-21/coldread/rekey-r56-<C0:0:12>`; (3) refuse on any `SKIP`; (4) re-run the precheck at PIN. Demonstrate it end to end on a scratch clone with a synthetic reader set (18 correct JSONs + MDs), showing `REFRESH rekeyed=18 skipped=0` and `lost=0 ok`. Report the exact command the L1 should run and any fragility (e.g. the binder's DROP list, the `--resolutions` default).")

add("T56W1ExecFreezeGen", "executor", ["operability"], "freeze regeneration check",
    f"Write `{L}/.ufo/waves/round-56/freeze-gen.py` (stdlib only): given the lane and a revision, it regenerates `freeze.json` from `{E}/contract.json` `frozen_paths` and prints `FREEZE_GEN: files=N ok|MISMATCH`. It must map `tools/*` and `.ufo/evidence/round-21|48/*` keys verbatim and every other key relative to `.ufo/evidence/round-56/`, exactly as `{E}/deciding-run.sh` does. Demonstrate at `{FREEZE}`: the regenerated digests equal the committed `freeze.json`'s (`ok`), and changing one byte of any frozen file in a scratch clone makes it print `MISMATCH` naming that file. Report the output.")

add("T56W1ExecCensus", "executor", ["freshness"], "census receipts and after-harness",
    f"Produce the round's census receipts. (a) Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` at base and save stdout/stderr/exit under `{L}/{W}/T56W1ExecCensus-receipts/`; report the exit code and the row count (`grep -cE '^ {{0,3}}\\| S[0-9]{{3,}} \\|' corpus/SOURCES.md`). (b) Write `{L}/.ufo/waves/round-56/census-after.sh` that runs the same census, prints `CENSUS exit=N rows=M`, and additionally validates any new row's shape (11 columns, no literal or escaped pipe, ISO `opened`, valid `status`). Demonstrate the shape check refusing a 10-column row and a row with an escaped pipe in a scratch copy. Never edit `corpus/SOURCES.md`.")

add("T56W1ScribeKnowledge", "scribe", ["coverage"], "knowledge entry draft",
    f"Draft `{L}/corpus/knowledge/receipt-revision-binding.md` in full (provenance trio first: `source:` citing the S-row the scout opens this round — read `{L}/{W}/T56W1ScoutSource.md`/`-receipts/` for the URL, anchor, access date and quote; `verified-at:`; `recheck:`). Content: the rule (a receipt is evidence only for the content it was measured against), the two real defects it catches (ER-R54-1: `CTL_POS_c1` at `077d431e` certifying `c2108100`; R55.5: the deciding gate had no comparison), the gate's role/role codes, the content-identity exception and why it exists (a receipt cannot name the commit that contains it), the `cannot_see` (a copied `rev=` token passes; the sidecar narrows it), and the commands that re-derive every claim. Follow `{L}/corpus/QUALITY.md` and the lane's entry shape; cite `S###` plus URL plus anchor. Deliverable: the full file text in your report (the L1 commits it at C0).")

add("T56W1ScribeSources", "scribe", ["coverage"], "SOURCES row draft",
    f"Draft the `corpus/SOURCES.md` row for the source `{L}/{W}/T56W1ScoutSource.md` opened this round (the in-toto attestation statement spec or whatever it actually opened). 11 columns exactly as contract v1 (`CORPUS.md` §SOURCES.md): id = the next unused S-number after the current registry maximum (derive it: `grep -oE '^ {{0,3}}\\| S[0-9]{{3,}}' {L}/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort -u | tail -1`), source = title + canonical URL, kind, tier with the scope it is tiered for, anchor (exact section + revision/date), teaches (one grounded learner benefit), status `mined` (it will be cited by the knowledge entry), opened = today's date, recheck, used-by = `corpus/knowledge/receipt-revision-binding.md`. No literal or escaped `|` in any cell; ≤25-word located quote goes in the round lesson's `## Gate`, not the row. Also draft one REJECTED candidate row with `REJECTED: <reason>; flip: <what would change the verdict>` and the same quote discipline. Deliverable: the exact table rows in your report.")

add("T56W1ScribeQuality", "scribe", ["calibration"], "QUALITY criterion draft",
    f"Draft one new `corpus/QUALITY.md` criterion (append-only, numbered after the current maximum; derive the number) stating C2's rule: every receipt the lane certifies names the revision it was measured against, and a positive control or verdict whose content differs from the certified revision is refused by `tools/receipt-revision-gate.py` with a named code. The criterion must carry: the rule, its falsifier (the exact command and the exact refusal code it must print on the real round-54 receipt `{L}/.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout`), the lesson pointer (`corpus/lessons/round-56.md`), and the `considerthese/2026-10-28.md` proposal 1 pointer (receipt-existence linter) that motivated it — citing the file and date, and saying what this criterion does NOT cover (existence at the cited revision is checked; byte-for-byte quoted-line matching is not). Read the last five criteria first so the new one does not duplicate one. Deliverable: the exact criterion text in your report.")

add("T56W1ScribeSkill", "scribe", ["operability"], "SKILL.md rule draft",
    f"Draft the `## Standing rules` change (that section only — the one heading with no ledger entry, which is why C1's re-key must re-read it). Add one bullet stating the receipt-binding rule with the gate path and one decision-table row (`situation -> rule -> code`) covering: a verdict receipt naming another revision, a positive control scored at the freeze, and a control set whose CTL lines name a revision absent from the repo. Keep the section's existing bytes wherever the rule does not change them, keep the edit under 20 added lines, and show the exact before/after hunk (`diff -u` of the section) in your report. Do not touch any other section: each one costs a re-read and the round prices exactly one.")

add("T56W1ScribeRegistry", "scribe", ["operability"], "registry cell draft",
    f"Draft the `tools/registry.json` addition for `tools/receipt-revision-gate.py`: read the file's schema first and match an existing row's keys exactly (no new key names). The cell must name: the tool, its modes (`--selftest`, the receipt form), the refusal codes (at least six of the eleven), the selftest command and its expected `GATE_SELFTEST: 14/14 pass`, and the scratch/read-only note. Validate the edited JSON parses (`python3 -c 'import json;json.load(open(...))'`) and that every existing row still parses. Deliverable: the exact JSON object in your report plus the parse receipt.")

add("T56W1ScribeScorecard", "scribe", ["calibration"], "SCORECARD block draft",
    f"Draft the round-56 `SCORECARD.md` block: (a) the restated standing axis table row for calibration, whose score is the value the round-21 monitor actually reads at a named commit (at base that is 6, not the 8 the row asserts at `d33053f7` — verify with `python3 {L}/.ufo/evidence/round-21/coldread/measure.py --repo {L} --rev <commit>`), with the evidence cell naming the monitor command and the last-change cell naming round 56; (b) the two claim rows (C1, C2) with before / target / counting command / controls; (c) the round's planned-next line. Keep the table's five columns; no `[x]`; do not invent a measured value — where the after value is not yet decided, write `pending deciding run at <the L1 fills this>` so the L1 cannot file a number no receipt carries. Deliverable: the exact block in your report.")

add("T56W1ScribeLog", "scribe", ["calibration"], "LOG entry draft",
    f"Draft the `LOG.md` round-56 entry (append-only, after the round-55 entry; read the last three entries for shape): date, round, the two claims with their axes, what landed, the evidence pointers (paths, not values), the freeze pointer `{FREEZE}`, and the disposition list of R55.1-R55.7. Commit hashes the L1 has not yet produced stay as `<L1 fills>`. Do not restate numbers a receipt does not carry; every value you write must name the receipt path that carries it. Deliverable: the exact entry text.")

add("T56W1ScribeLesson", "scribe", ["calibration"], "lesson draft",
    f"Draft `{L}/corpus/lessons/round-56.md`: `## Gate` (the source row opened this round with URL, access date and ≤25-word located quote, plus one rejected candidate with reason and flip), `## Mistakes` (rows in the CORPUS.md vocabulary: class · evidence pointer · captured-by · fix; include the R55.6 uncommitted-work class and the R55.7 closure-contamination class, each with the round-55 receipt; add this round's own mistake if wave 1 finds one), `## Round-55 routed defects — dispositions` (one row per R55.1-R55.7 naming the disposition and the receipt), and `## What the counters cannot see` (C1: a fabricated reader hash passes; C2: a copied `rev=` token passes). A fix counts only once shown able to fail: name the red-before receipt for each fix you claim. Deliverable: the exact file text.")

add("T56W1ScribeReport", "scribe", ["calibration"], "report skeleton",
    f"Draft the report skeleton at `{L}/{W}/T56W1ScribeReport.md` for `/home/vgpnk/Projects/shokunin/.ufo/reports/round-56/tameshi.md` with the required sections in this order: Work performed (opens by naming the two claims and their axes), Landed changes (table: change / LOG entry / commit), Before -> after measurements (one row per claim with the counting command and the measured commit), Sources & frontier, Trend verdicts (expansion/quality/discernment, no scalar), SHONEN (one line per box of `{L}/SHONEN.md`), Stale-lane line, and a final JSON block. Every value slot that needs a receipt is `<fill: receipt path>`; include the marker-rule check (`grep -c '^## SHONEN'` must print 1) and the pre-report gate (`git ls-remote origin refs/heads/master` must print the lane hash). Read the round-55 report for shape and the round-55 spotcheck for what the closure grades. Deliverable: the skeleton text.")

add("T56W1ScoutSource", "scout", ["freshness"], "external source opening",
    f"Open ONE external source that grounds C2's rule and save the evidence. Candidate: the in-toto Attestation Framework statement spec (subject + digest binding: an attestation is about a subject identified by a digest, so a statement about another subject is not evidence). Fetch the page with a real HTTP client, save the extraction under `{L}/.ufo/evidence/round-56/assimilation/` with its sha256 and the access date, and record a ≤25-word quote with its exact location (section heading + line or paragraph). Check it is not already a `SOURCES.md` row (`grep -n '<url-fragment>' {L}/corpus/SOURCES.md`) — a within-scope duplicate URL must be refused, not appended. Also screen ONE rejected candidate (a page that looks related but cannot ground the rule) with its reason and flip. Report: URL, access date, quote, location, sha256, duplicate check output, and whether the source is tier A for the scope (a spec is A for its own statement shape).")

add("T56W1ScoutDrift", "scout", ["coverage"], "18-heading drift map (planner data walk)",
    f"Produce `{L}/{W}/drift-map.json`: for every heading in `{E}/c1/lost-headings-at-base.json`, the file it lives in (SKILL.md or a knowledge entry — the round-18 `sectionize` at base plus `{L}/.ufo/evidence/round-21/coldread/ledger.json` names it), its `start`/`end`/`sha256` at base `{BASE}`, the prior ledger entry's pinned `inputs` and `external_inputs`, which of those inputs drifted at base versus the entry's read_rev (use `{L}/.ufo/evidence/round-21/coldread/measure.py --repo {L} --rev {BASE} --explain` for the reason strings), and whether the heading's TEXT changed since its last read. Also state, per heading, whether the section is in SKILL.md (one section only may be edited this round) or in corpus (must not be edited at all). This is the L1's planning walk: the output decides what C0 must contain.")

add("T56W1ScoutReceipts", "scout", ["coverage"], "receipt inventory",
    f"Inventory every committed receipt under `{L}/.ufo/evidence/round-5*/` and `round-4*/` that carries a `rev=` or a JSON `rev` token: file, token(s), the claim it certifies, the revision the claim was measured at (from the round's report/SCORECARD), and whether the token equals it. Produce `{L}/{W}/receipt-inventory.json` with counts: bound / unbound / unresolvable / no-token. This extends C2's before count beyond the three receipts the counter names and is the evidence for the claim that the defect class recurs. Use `git grep -n` at `{BASE}` so the inventory is reproducible; report the exact commands.")

add("T56W1ScoutFreezeSet", "scout", ["coverage"], "pinned-input set",
    f"Derive the exact set of paths that must be byte-identical between the content-final revision PIN and the deciding revision: the union of every pinned `inputs` key across the ledger entries for the 18 headings (from `{L}/.ufo/evidence/round-21/coldread/ledger.json`), minus the binder's DROP list (`LOG.md`, `SCORECARD.md`, `SKILL.md`, the ledger). Write `{L}/{W}/pinned-inputs.txt`. Then check the round's planned content edits against it: which of these paths does C2's content (QUALITY, SOURCES, knowledge, registry, the gate) touch, and therefore which edits MUST land at or before C0. Flag any path the plan would edit after C0 — that is the round-55 failure mode. Report the set, the touched paths and the ordering constraint.")

add("T56W1ConnectorSiblings", "connector", ["adjacency"], "sibling-overlap scan",
    f"Scan the sibling lanes read-only (`/home/vgpnk/Projects/shokunin/*-shokunin/`, `grep -rn` over `corpus/knowledge`, `SKILL.md`, `tools/` for `rev=`, `receipt`, `attestation`, `provenance`, `digest`, `frozen receipt`) and report: does any sibling already own a receipt-to-revision binding rule or a provenance gate? For each hit, name the sibling, the path, what it owns, and whether tameshi's C2 duplicates it, complements it, or is contested scope that must be reported and not absorbed. Produce a table with one row per sibling hit and a final verdict line (`overlap=none|complement|contest`). Do not edit any sibling file. This is the connector seat for the round.")

add("T56W1CritC1", "critic", ["calibration"], "falsify C1",
    f"Falsify C1 (`{E}/contract.json`). The target is `C1_R56_PASS=true`. Answer with commands and outputs: (1) can a do-nothing control reach 64/64 — e.g. by deleting the 18 headings' ledger entries, by re-pinning inputs without a reader, or by editing the standing row to 6 without binding anything? Run each attempt in a scratch clone and show the counter's verdict. (2) Arm 4 accepts a reader JSON whose `section_sha256` is computed from the tree: build one without reading the section and show it passes — is the target then reachable by a fabrication? (3) Is `unstable` arm 5 vacuous at base (it prints 0 because there are no bound entries)? (4) Does arm 6 compare against the row's own named commit, and can a row name a commit where the score differs? Report each finding with the exact command and the verdict substring; state which findings would make the claim inadmissible.")

add("T56W1CritC2", "critic", ["operability"], "falsify C2",
    f"Falsify C2 (`{E}/contract.json`). The target is `C2_R56_PASS=true`. (1) Is the content-identity exception gameable — can a receipt naming a revision that differs from the certified one on an UNLISTED path be accepted for a claim that path matters to? Construct one and show the gate's answer. (2) Is the red-before receipt genuinely the one the round-54 gate accepted — read `{L}/.ufo/evidence/round-54/after/deciding-run.exit` and the round-54 `deciding-run.sh`, and say exactly which check was missing. (3) Does arm 5 (`own`) actually depend on the gate, or would any two files pass? Mutate `controls-b.stdout`'s `rev=` to a wrong commit in a scratch clone and show the arm fails. (4) Does arm 6 (`docs`) accept a QUALITY mention that is merely a path string? Construct the weakest text that still scores 4/4 and say whether it is enough. Report commands, outputs and verdicts.")

add("T56W1CritClaimShape", "critic", ["calibration"], "claim-shape audit",
    f"Audit the two claims against the fleet's claim-sizing rules (round-prompt §9 and `AXES.md`): (a) each after-state is one concrete value one command re-derives over committed bytes — check the exact verdict lines; (b) no universal clauses ('all', 'every', 'complete') without an enumerating command — sweep the contract, the two counters' docstrings and the drafted records; (c) at least one claim works the lowest non-retired axis — verify calibration really is the lowest by re-deriving depth (command D) and freshness (round-45 measure) at base; (d) C1 and C2 are causally separable — describe a tree where each holds and the other fails; (e) a do-nothing control cannot reach either target — name the cheapest do-nothing per claim and its score; (f) at least one claim is sourced (cites an S-row opened this round) — check the draft knowledge entry. Deliverable: a pass/fail row per item with the command that shows it.")

add("T56W1RevBaseC1", "reviewer", ["calibration"], "independent base re-derivation",
    f"Re-derive the base cold-read state WITHOUT the round-56 counter: run `python3 {L}/.ufo/evidence/round-21/coldread/measure.py --repo {L} --rev {BASE} --explain` and `bash {L}/.ufo/evidence/round-48/quality/coldread-precheck.sh {L} 0a2010acd1e92e4e332774050825e21bcfc7e079 {BASE}`, and report: credited/total, score, box3, the 18 lost headings with their reason strings, and whether the set equals `{E}/c1/lost-headings-at-base.json`. Then re-derive the standing row's defect: at `d33053f7` the monitor reads what, and what does the row assert? Report both numbers with the commands. Also confirm the base receipt `{E}/before/c1.stdout` reproduces (diff it against your run, ignoring the work-dir path).")

add("T56W1RevInherited", "reviewer", ["calibration"], "inherited-state audit",
    f"Audit the inherited-state resolution the L1 made at round start: (a) 96 untracked round-55 files were committed at `6efd2a19` and `981c5e8b`; verify each is lane-authored round-55 evidence (wave deliverables, receipts, results) and none is a misroot or another lane's file — `git show --stat 6efd2a19`, `git show --stat 981c5e8b`, and a content scan for paths naming another lane. (b) 23 tracked files were reverted to branch bytes (post-tip closure rewrites, R55.7); list them (`git log -1 --format=%H` on the two commits and `git diff fa48c06c 981c5e8b --stat`) and verify none carried round-55 content the lane needed (in particular `after/c2.stdout` must be the truncated original, not the post-tip green line). (c) Confirm nothing of round-55's claim substance was lost: the round-55 counter bytes, contract and controls are still at the round-55 evidence paths. Report each check with its command.")

add("T56W1MutCounterArms", "mutation-tester", ["calibration"], "C1 counter arm liveness",
    f"Mutation-test the frozen C1 counter `{E}/c1/measure.py`: 8 single-edit mutants, each in a fresh scratch clone of the lane at the freeze, one exact edit per mutant (assert the old string is unique first). Candidate mutations: (M1) precheck ok check `'lost=0 ok' in last` -> `True`; (M2) `covered == 64` -> `covered >= 46`; (M3) `score == 8` -> `score >= 6`; (M4) `rekeyed != len(frozen)` -> `rekeyed < 0`; (M5) reader `d.get('section_sha256') == sec['sha256']` -> `True`; (M6) `UNSTABLE_INPUTS = ('LOG.md','SCORECARD.md')` -> `()`; (M7) arm 6 `row_score == score` -> `True`; (M8) `is_ancestor(lane, row_commit, rev)` -> `True`. For each: the counter's verdict at the base revision and at a fixture revision where the arm should fire; report KILLED / SURVIVED / INCONCLUSIVE with the receipt. A survivor is a finding about the counter, not about the claim. Use `{L}/tools/mutate-and-run.sh` if it fits, else a documented driver; scratch only.")

add("T56W1MutGate", "mutation-tester", ["operability"], "gate mutation set",
    f"Mutation-test `{L}/tools/receipt-revision-gate.py`: 8 single-edit mutants, one exact edit each, each must be killed by `--selftest` (a mutant that survives the selftest is a hole in the suite). Candidates: drop the `RECEIPT_REV_ABSENT` return; make `drifted_paths` always return `[]`; make `is_ancestor` always true; skip the digest check; accept multiple revs in a positive role; skip the required-line check; treat an empty file as present; drop `RECEIPT_CONTROL_NOT_ANCESTOR`. For each: the selftest tally before/after and the case name that failed. Report KILLED / SURVIVED per mutant with the receipt, and name the selftest case that covers each code.")

add("T56W1SentTamper", "sentinel", ["operability"], "receipt forgery attempts",
    f"Attack the gate as an adversary. Craft receipts that satisfy it while certifying nothing, and report each acceptance: (1) copy the certified revision's `rev=` token into a receipt for a different claim; (2) forge the `.sha256` sidecar to match a tampered receipt; (3) embed `rev=<certified>` in a path or a prose sentence with no verdict line; (4) use a JSON receipt whose rev key is a string plus a second `rev=` in a comment; (5) name a tag or a tree object instead of a commit; (6) name a merge commit whose tree equals the certified tree but whose history differs; (7) point `--paths` at a file listing paths that do not exist. For each: the gate's answer and whether that answer is safe for the lane's use. Then state the residual risk the gate cannot remove and how the round's report should say it. Never edit the gate.")

add("T56W1RevNoHarmSet", "reviewer", ["freshness"], "no-harm monitor audit",
    f"Audit the 15 monitors in `{E}/no-harm.sh` against `{E}/contract.json` (`no_harm_monitors: 15`): list each monitor, what it would catch, and whether it can turn RED by construction. Identify (a) any monitor that reads the working tree instead of REV bytes and could pass on a contaminated tree, (b) any monitor whose base constant makes it vacuous, (c) any axis with no monitor at all (adjacency? coverage? operability?). Report the table and a verdict per monitor (`live`/`vacuous`/`weak`) with the line you would change. Do not edit the script; it is frozen.")

add("T56W1RevFreeze", "reviewer", ["calibration"], "freeze discipline",
    f"Audit the freeze: (a) `{E}/freeze.json` keys vs `{E}/contract.json` `frozen_paths` — every frozen path must be covered (map the same way `{E}/deciding-run.sh` does) and every digest must re-derive (`sha256sum` at the freeze revision `{FREEZE}`); (b) `{E}/deciding-run.sh`'s `FROZEN=` list vs `freeze.json` — a path in one and not the other is a hole; (c) the amendment protocol: can an instrument change after the freeze without an amendment? Show what the deciding run prints when one does (mutate a copy); (d) the freeze commit `{FREEZE}` must contain every instrument and no content edit. Report each check with its command and the exact output; name every hole.")

add("T56W1SimplScope", "simplifier", ["operability"], "delete-what-is-not-needed",
    f"Propose deletions that preserve verified behavior. Candidates to examine: (1) `{E}/control/frozen-surface.paths` — is the content-identity exception needed at all, or could the positive control simply be re-scored at the certified revision (the L1 controls the order)? (2) `{E}/deciding-run.sh`'s second gate invocation (`receipt-gate-verdicts`) — does any claim arm read it? (3) `{E}/c2/red-before/round-54-surface.paths` — could the arm use the round-54 counter's own frozen path list instead? (4) `validate-readers.py`/`bind.sh`/`freeze-gen.py` (wave-1 deliverables) — which of them does the round actually run? For each: the deletion, what evidence would be lost, and whether the claim's predicate survives. Report a ranked list with `keep`/`delete` and the reason. Do not edit anything.")

add("T56W1RevCensus", "reviewer", ["freshness"], "census conformance",
    f"Verify the sources census conformance for the round's start: run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`, report exit code, the trailer line, the row count and the warning count at `{BASE}`; then check the row the scribe drafts (`{L}/{W}/T56W1ScribeSources.md`) against contract v1 by hand: 11 columns, no literal/escaped pipe, valid kind/tier/status enums, `opened` ISO, `recheck` ISO or cadence, `used-by` naming a path that will exist, and no duplicate URL (`grep -n` the URL fragment in `corpus/SOURCES.md`). Report the row's verdict and the exact fix if it fails. Never edit `corpus/SOURCES.md`.")

add("T56W1RevRound55Dispositions", "reviewer", ["calibration"], "round-55 disposition check",
    f"Take the seven routed defects from `{L}/corpus/lessons/round-55-verifier-spotcheck.md` (R55.1-R55.7) and check each against the round-56 plan and drafts (`{L}/{W}/T56W1ScribeLesson.md`, `T56W1ScribeScorecard.md`, `{E}/contract.json`): is there a disposition that lands this round, with a receipt that can carry it? Name any that is only prose, any that the plan silently drops, and any whose fix cannot be shown able to fail. Report a row per defect (`fixed-this-round` / `carried` / `declined` + why) and the receipt each will carry. This is the discernment check on the round's own honesty.")

spec = {
    "wave": "round-56-w1",
    "reportDir": ".ufo/waves/round-56/w1",
    "template": TEMPLATE,
    "context": CONTEXT,
    "items": ITEMS,
}
out = Path(LANE, ".ufo/waves/round-56/spec-w1.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
roles = {}
for it in ITEMS:
    roles[it["role"]] = roles.get(it["role"], 0) + 1
print("items", len(ITEMS), roles)
