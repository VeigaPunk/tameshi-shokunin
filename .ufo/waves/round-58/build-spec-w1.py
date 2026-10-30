#!/usr/bin/env python3
"""Build the round-58 wave-1 (v2) spec: 64 seats, build + attack mixed, >=25% attack roles."""
import json

GODSPEED = """You are a Godspeed-enabled subagent.

1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**

## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
BASE = '2a32aa8228d5f86a85c81a923a3148bf792a9538'
W1 = LANE + '/.ufo/waves/round-58/w1'

CONTEXT = f"""# Goal
tameshi round 58 (hyaku run 11; L1 TameshiR58), wave 1 of two (v2: build + attack mixed). Lane repo {LANE}; lane base `{BASE}` (the lane tip; the freeze commit adds instruments only and changes no monitored content). Every path you read, edit or write is ABSOLUTE: seat tools start at the fleet root /home/vgpnk/Projects/shokunin, so a relative `.ufo/...` lands in the FLEET repo. Every `Report:` trailer path the harness renders is relative to {LANE}: write it at {LANE}/<that path>.

# The round (contract {LANE}/.ufo/evidence/round-58/contract.json; wave reports under {W1}/)
- **C1 calibration**: the routed-defect ledger {LANE}/corpus/routed-defects.json gains one row per item of the frozen 51-item set {LANE}/.ufo/evidence/round-58/c1/defects.json (routed items of the closure spot-checks of rounds 50-56), statuses the tree supports; counter {LANE}/.ufo/evidence/round-58/c1/measure.py (round-57 arms A1-A9 re-pinned; base {BASE}; blind panel {LANE}/.ufo/evidence/round-58/c1/panel.json, pin set by amendment 1 after this wave).
- **C2 operability**: the strict element-equality counter {LANE}/.ufo/evidence/round-58/c2/measure.py must read total=0 at one committed REV: three executed registry gate rows (already landed at the tip), the registry's two refusal rows gain the BARE code elements (`RECEIPT_REV_CONTENT_DRIFT`, `RECEIPT_REV_UNRESOLVABLE`) — the pre-freeze upgrade that lands the round-57 critique T57W3CritContract B2; three gate mutants killed live; SKILL row and standing cell already true at the tip.
- **C3 coverage**: F9 (LLM-era mutant generation + equivalence) enters through `corpus/knowledge/llm-mutant-equivalence-cost.md`, citing new rows S286 (arXiv 2406.09843, opened 2026-10-30 by the L1) and S287 (dfcfw deck, opened 2026-10-30 by the L1); S288 supersedes S285's unreachable anchor. L1 fetch receipts: {LANE}/.ufo/waves/round-58/l1/sources/.
- NO-HARM: the round-21 cold-read monitor must read 64/64 at the deciding revision; the contract's coldread_forecast prices the round's planned edits. Re-readers ride wave 2, after content lands.

# Deliverables discipline
- Report {W1}/<your-seat-name>.md; machine-readable output beside it {W1}/<your-seat-name>.json; receipts under {W1}/<your-seat-name>-receipts/. Anything you would change is STAGED under {W1}/<your-seat-name>/stage/<repo-relative-path>; NEVER edit a lane file in place; never edit anything under {LANE}/.ufo/evidence/round-5[0-7]/ (read-only prior-round evidence).
- Scratch: `export HYAKU_SCRATCH=/fast/scratch/hyaku; S=$HYAKU_SCRATCH/tameshi-r58/<your-seat-name>; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT`; `/tmp` only for files under 50 MB; tools you write honour `TMPDIR`/`--work`; delete your scratch before you yield and say so in the report.
- Clones: `git clone --shared {LANE} "$S/clone"` then `git -C "$S/clone" checkout --detach <rev>`; every git call names `-C`. NEVER run a mutating git/jj command in the lane or the fleet repo (the L1 alone commits through the lane helper). Fixture repos: `D=$(mktemp -d -p "$S")`, `git -C "$D" init -q`, verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before a commit there; commit only with `-c user.name=fixture -c user.email=fixture@example.invalid` and `-C "$D"`.
- Never message agent://all; message only your own L1 (`TameshiR58`) when blocked.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task; first read /home/vgpnk/.omp/agent/RULES.md; record tool/version/channel/reason in your report. All pacman transactions are PAUSED host-wide: install via `uv tool` / `npx` / an official binary in `~/.local/bin`; never `pacman -S/-Sy/-Syu/-U/-R`, never downgrade, never restart a host service.
- An attack that finds nothing must show the sweep it ran (command + output). A finding without a command and its output is not a finding. An unrun check has not passed. Honesty: an unobserved or unverified statement is marked INFERENCE, never asserted.

# Panel contract (seats named T58W1Panel*)
BLIND: you must NOT open, grep or read: `{LANE}/corpus/routed-defects.json` rows other than the 49 baseline rows is ALLOWED (it holds no round-50..56 rows), but these are FORBIDDEN paths: anything under `{LANE}/.ufo/waves/round-57/` (the round-57 candidate ledger and panels live there), `{LANE}/.ufo/evidence/round-57/c1/panel.json`, anything under `{LANE}/.ufo/waves/round-58/` except your own files, and `{LANE}/.ufo/waves/round-58/w1/T58W1Verify*` or `T58W1Fix*` outputs. Your verdicts are your own, from the item text and the tree at base `{BASE}`.
1. Your item ids are listed in your item text; the full item records (id, file, line, routed_at, text, keys) are in {LANE}/.ufo/evidence/round-58/c1/defects.json (read it from the working tree; it is committed at the freeze commit).
2. For EACH id, judge the item's status AT BASE `{BASE}` in a scratch clone detached at that rev: `fixed` (the defect the item describes is resolved in the tree at base; name the commit that resolved it — a full 40-hex hash, an ancestor of base), `open` (not resolved at base), or `declined` (the tree at base carries a recorded, reasoned decline of at least 40 characters for it). Cite for every verdict: the command(s) you ran and their output; for `fixed`, the located excerpt that shows the resolution and the commit that introduced it.
3. Write {W1}/<your-seat-name>.json: `{{"seat": "<name>", "base": "{BASE}", "verdicts": {{"<id>": {{"verdict": "fixed|open|declined", "commit": "<40-hex or null>", "reason": "<=200 chars, evidence-grounded"}}}}}}` — one entry per assigned id, no extras.
4. Write the report .md naming your commands and the evidence you relied on per id.

# Row-verify contract (seats named T58W1Verify*)
For EACH assigned id (records in {LANE}/.ufo/evidence/round-58/c1/defects.json; key tokens in {LANE}/.ufo/evidence/round-58/c1/keys.json): independently re-derive the item's TRUE status at base `{BASE}` and, when a fix is still owed, design the row the round-58 ledger should carry. Output {W1}/<your-seat-name>.json with `rows`: one object per id `{{"id", "status_at_base", "status_now_proposed", "commit" (the resolving commit for fixed-at-base, else the planned round-58 fix commit intent), "evidence": [{{"path", "lines", "excerpt"}}] (for proposed fixed rows: excerpt 15-400 chars, present in those lines at the planned state, containing one of the item's keys as a whole token, absent from that path at routed_at, none of the lane's ACK_WORDS), "reason" (for declined: >= 40 chars), "notes"}}`. Ground every claim in a command you ran. Do not copy any other seat's or prior round's status judgments — re-derive from the tree."""

ITEMS = []


def add(name, role, item, axes=None, milestone=None):
    ITEMS.append({'name': name, 'role': role, 'axes': axes or ['calibration'],
                  'milestone': milestone or '', 'item': item})


# ---- blind panel (11 reviewer seats, 51 items) ----
d = json.load(open(LANE + '/.ufo/evidence/round-58/c1/defects.json'))
ids = [x['id'] for x in d['defects']]
assert len(ids) == 51
for i in range(11):
    chunk = ids[i * 5:(i + 1) * 5] if i < 10 else ids[50:]
    add(f'T58W1Panel{i+1:02d}', 'reviewer',
        'Blind panel seat. Item ids: ' + ', '.join(chunk) +
        '. Follow the Panel contract exactly: one verdict per id at base ' + BASE +
        ', written to ' + W1 + '/T58W1Panel%02d.json.' % (i + 1),
        axes=['calibration'], milestone=f'blind panel {len(chunk)} items')

# ---- row verification (13 executor seats) ----
for i in range(13):
    chunk = ids[i * 4:(i + 1) * 4] if i < 12 else ids[48:]
    add(f'T58W1Verify{i+1:02d}', 'executor',
        'Row verification seat. Item ids: ' + ', '.join(chunk) +
        '. Follow the Row-verify contract exactly; output ' + W1 + '/T58W1Verify%02d.json.' % (i + 1),
        axes=['calibration'], milestone=f'row verify {len(chunk)} items')

# ---- fix preparation (8 executor seats) ----
FIXES = [
    ('R53.2', 'The round-53 deciding receipts were never committed: run the ROUND-53 counters (their committed bytes at tip: .ufo/evidence/round-53/c1/measure.py and .ufo/evidence/round-53/c2/measure.py) at the round-53 deciding revision 88afa941545469457c78c7f4014bcda1afdee52c in a scratch clone detached at that rev, capture full stdout of each, and stage the receipt files exactly as they should land: stage/.ufo/evidence/round-53/after/c1.stdout and c2.stdout (+ a run.log per counter with the exact commands). The counter bytes must be taken from the clone at 88afa941 (git show 88afa941...:<path>), not the tip.'),
    ('R53.3', 'The round-53 phase-B break-one controls have no committed receipt: run .ufo/evidence/round-53/control/break-fixtures.py per its own header at the round-53 final revision 88afa941545469457c78c7f4014bcda1afdee52c in a scratch clone, produce the CONTROLS_B tally receipt the item asks for, and stage it as stage/.ufo/evidence/round-53/control/controls-b.stdout (+ .exit and a .sha256 sibling, same format as round-57 control receipts). If the fixtures cannot run at that rev, stage the full failure log instead and say so - honesty over green.'),
    ('R53.4', 'The committed round-53 C2 receipt names a scratch-clone rev: re-run the round-53 c2 counter (.ufo/evidence/round-53/c2/measure.py at 88afa941545469457c78c7f4014bcda1afdee52c) against the LANE repo itself at that committed rev (--lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 88afa941545469457c78c7f4014bcda1afdee52c), capture stdout, and stage it as stage/.ufo/evidence/round-53/after/c2-anchored.stdout with a run.log. If the counter refuses a non-clone lane, document the refusal verbatim and stage the clone-based run whose rev= is an ANCESTOR of the lane tip (verify with git merge-base --is-ancestor).'),
    ('R53.5', 'The round-53 freeze receipts/pointers are stale: (a) find the round-53 freeze verification tooling (verify-freeze.stdout at tip names it), re-run it against the FINAL round-53 freeze cf872769 (resolve the full hash from the lane log: git log --format=%H --grep=cf872769 or the round-53 evidence), capture stdout, stage as stage/.ufo/evidence/round-53/verify-freeze-final.stdout; (b) draft the one-line LOG.md correction sentence (append-only style) naming cf872769 as the final freeze, staged as stage/LOG-correction-r53.5.md.'),
    ('R55.1', 'No round-55 C2 verdict exists at its measured revision 4c04c1d3: run the round-55 C2 counter (resolve its path from .ufo/evidence/round-55/ at tip; the counter bytes must be those committed at the round-55 tip) at --rev 4c04c1d3 in a scratch clone detached at that rev, capture FULL stdout (the committed after/c2.stdout is truncated mid-run), and stage it as stage/.ufo/evidence/round-55/after/c2-full.stdout + run.log.'),
    ('R51.6', 'Gate completeness practice: draft the round-58 lesson Gate-block skeleton that lists REJECTED candidates with reasons (not only admits), demonstrating the corrected practice the item demands; stage as stage/lessons-draft-gate-skeleton.md with 3 worked reject entries drawn from this round\'s real rejects (e.g. the refused staged package entries).'),
    ('R56.5', 'Controls generations pre-registration: the round-58 controls.sh header must pre-register the generation order (one generation, recomputed, never read) and the producer-provenance discriminator for any own-receipts arm. Read the staged /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-58/controls.sh and .ufo/evidence/round-58/deciding-run.sh headers, verify they carry both properties, and write a verdict + any missing sentence as a staged header patch (stage/controls-header-r56.5.md). Do not edit the instruments in place.'),
    ('R51.5', 'Cross-domain routing owed to kagi: read kagi-shokunin/corpus/drift-pins.sh READ-ONLY (repo /home/vgpnk/Projects/kagi-shokunin, at its tip; NEVER edit or commit there) and verify the three unanchored verdict-word grep sites the item names (lines ~400, ~403, and the path-printing DRIFT line ~158 at the revision the round-51 leg pinned; resolve that revision from the tameshi leg ledger .ufo/evidence evidence or corpus/knowledge/mutation-case-*). Produce the cross-domain evidence block for the round-58 fleet report: what the defect is, the exact lines, why it matters, and the recommendation; stage as stage/kagi-crossdomain-r51.5.md.'),
]
for i, (rid, text) in enumerate(FIXES):
    add(f'T58W1Fix{i+1:02d}', 'executor',
        f'Fix-preparation seat for routed item {rid}. {text} Also write the ledger row JSON this fix supports (id {rid}, status fixed, status_at_base from your own re-derivation, evidence with a keyed excerpt the fix commit introduces, commit = the planned round-58 commit message you propose, which MUST name {rid} or the evidence path). Output {W1}/T58W1Fix{i+1:02d}.json + the .md report; stage everything under {W1}/T58W1Fix{i+1:02d}/stage/.',
        axes=['calibration', 'operability'], milestone=f'fix prep {rid}')

# ---- C2 registry + instruments verification ----
add('T58W1ExecC2Reg', 'executor',
    'C2 registry seat. In a scratch clone of the lane at base %s: (a) apply the bare-code patch - copy the patched registry draft /fast/scratch/hyaku/tameshi-r58/c0-drafts/registry-patched.json over the clone tools/registry.json and diff against the clone original to show the delta is exactly two added expect.stdout_contains elements ("RECEIPT_REV_CONTENT_DRIFT" on receipt-gate-content-drift, "RECEIPT_REV_UNRESOLVABLE" on receipt-gate-unresolvable-certified); (b) overlay the round-58 instruments (.ufo/evidence/round-58/ c1, c2, control, controls.sh, no-harm.sh, deciding-run.sh, contract.json, freeze.json) from the lane working tree into the clone, commit, and run python3 -I .ufo/evidence/round-58/c2/measure.py --lane <clone> --rev <clone head> --work <scratch work dir> --explain - expect total=0 PASS=true (this previews the round-58 after-state); (c) also run it WITHOUT the registry patch (restore the base registry, commit) to show the red-before: the rows arm must count >=1 shortfall and PASS=false; (d) run tools/registry-check.py at the patched clone for the three receipt-gate rows and report held/differs. Output %s/T58W1ExecC2Reg.json with all three counter lines verbatim.' % (BASE, W1),
    axes=['operability'], milestone='C2 strict red-before + registry patch')
add('T58W1ExecInstr', 'executor',
    'Instruments seat. In a scratch clone of the lane detached at the FREEZE commit (resolve it: git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --format="%%H %%s" -8; the freeze is the tip commit whose message starts "round-58: freeze"; the instruments .ufo/evidence/round-58/ are committed there): (a) python3 -I .ufo/evidence/round-58/c1/measure.py --selftest --work <scratch> (expect C1_R58_SELFTEST: 110/110 pass, exit 0); (b) python3 -I .ufo/evidence/round-58/c2/measure.py --selftest --work <scratch> (expect C2_R58_SELFTEST: 23/23 pass, exit 0); (c) bash -n on controls.sh, no-harm.sh, deciding-run.sh (syntax only, expect silence); (d) diff the round-58 copies against the round-57 originals (.ufo/evidence/round-57/c1/measure.py, c2/measure.py) and enumerate every semantic delta beyond the re-pin (BASE, paths, labels, the strict row_named_codes upgrade, selftest case additions) - flag ANY other behavioral change. Output %s/T58W1ExecInstr.json.' % (W1,),
    axes=['calibration'], milestone='instrument selftests + diff audit')

# ---- assimilation ops (2 executor seats) ----
add('T58W1ExecAssim', 'executor',
    'Assimilation mechanics seat. In a scratch clone of the lane at base %s: build the assimilation mirror exactly per the fleet contract: copy corpus/ from the clone, add the draft entry /fast/scratch/hyaku/tameshi-r58/c0-drafts/entry-llm-mutant-equivalence-cost.md at corpus/knowledge/llm-mutant-equivalence-cost.md, append the three draft rows /fast/scratch/hyaku/tameshi-r58/c0-drafts/sources-append.md to the mirror registry table after its last S-row, commit in the clone (fixture identity), then run /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root <clone> tameshi (expect exit 0; warnings allowed) AND the manual census commands from /home/vgpnk/Projects/shokunin/CORPUS.md section SOURCES.md (rows, malformed NF, duplicate ids, enum violations, mined used-by existence). Then run the id-collision check: reg-ids from the tip registry vs staged ids from /home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md with the 0-3-leading-space pattern (grep -oE \'^ {0,3}\\|[[:space:]]*S[0-9]{3,}\' ...), comm -12; expect the staged S156/S165 ids to collide by ID (not by document) and confirm the draft rows use S286/S287 which must NOT collide. Also prove the guard: on a scratch fixture registry where an indented row carries a staged id, the collision list must be nonempty. Output %s/T58W1ExecAssim.json with every census command + output and both id lists.' % (BASE, W1),
    axes=['coverage'], milestone='assimilation mirror + census + collisions')
add('T58W1ExecSchem', 'executor',
    'Row schema seat. Validate the three draft source rows (/fast/scratch/hyaku/tameshi-r58/c0-drafts/sources-append.md) against the CORPUS.md contract v1 shape: 11 columns (awk -F"|" NF==13 on each row), id format and next-unused after the tip registry (S286-288; tip max S285), kind/tier/status enums, anchor exactness (each anchor names a section/lines + a fetch date + size or sha, and its extract path resolves in the lane working tree .ufo/waves/round-58/l1/sources/), no pipe characters inside cells, recheck a valid cadence, used-by paths exist in the lane working tree (the entry draft is staged at /fast/scratch/hyaku/tameshi-r58/c0-drafts/entry-llm-mutant-equivalence-cost.md - it will exist at corpus/knowledge/ post-C0; check the path string matches that location). Also verify each Gate quote is <= 25 words: S286 quote "the LLM-generated mutants have worse non-compilability, duplication, and equivalent mutant rates by 26.60, 10.14, and 3.51 percentage points", S287 quote the Chinese line at extract line 241, S288 quote "we understand and remediate the root cause of every incident with a severity of level 2 or higher" - count words with python len(q.split()) and report each count. Output %s/T58W1ExecSchem.json.' % (W1,),
    axes=['coverage'], milestone='SOURCES draft schema + gate quotes')

# ---- scouts (4) ----
add('T58W1ScoutCT', 'scout',
    'considerthese seat. Read all eight files in /home/vgpnk/Projects/shokunin/tameshi-shokunin/considerthese/ (read-only). Round 57 already mined 2026-10-28.md proposal 3. Identify the ONE best still-unimplemented proposal across the files (a "proposals only ... not implemented" item), preferably from the latest file; verify it is unimplemented by sweeping the lane tree for its subject (show the sweep). Return: file, proposal text verbatim, why it fits the lane PROVINCE (/home/vgpnk/Projects/shokunin/tameshi-shokunin/PROVINCE.md), and a landing route (lesson, QUALITY criterion, or SOURCES row). Output %s/T58W1ScoutCT.json.' % (W1,),
    axes=['coverage'], milestone='considerthese proposal')
add('T58W1ScoutReg', 'scout',
    'Register slice seat. Read-only: /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md. Extract the tameshi slice exactly per the fleet contract (awk -F"|" lane cell `tameshi`, round cell roundN, id cell S-id; print id + class). Count rows; classify each class cell: a prose class (e.g. "could not be fetched", "named no locator") is unverifiable, an S-id-with-payload-absent class is quarantined pending hand-check. Verdict per row: quarantined / unverifiable - NEVER verdict a row adoptable this round (adoption of register rows is not planned; say so). Also verify the register header and By-lane summary are stale for tameshi by comparing the summary totals with your derived slice. Output %s/T58W1ScoutReg.json.' % (W1,),
    axes=['coverage'], milestone='register slice + quarantine verdicts')
add('T58W1ScoutKagi', 'scout',
    'QUALITY map seat. Read /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/QUALITY.md criteria list and the round-57 closure routed items (/home/vgpnk/Projects/shokunin/.ufo/reports/round-57/tameshi.md, the routed-defects section). For each routed item, state whether the round-58 contract ( /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-58/contract.json) answers it with a fix, and whether any NEW QUALITY criterion is owed (LEARNING.md rule: a disagreement becomes a criterion or the report says why not). Also verify criterion 110 (coldread_forecast) is satisfied by the contract: the key exists, committed at the freeze (before content), entries per planned edit to pinned files. Output %s/T58W1ScoutKagi.json.' % (W1,),
    axes=['calibration'], milestone='QUALITY map for routed items')
add('T58W1ScoutPin', 'scout',
    'Forecast inputs seat. Read /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/coldread/ledger.json (committed). Enumerate which bound sections list any of these files as pinned inputs: corpus/SOURCES.md, corpus/README.md, tools/registry.json, corpus/routed-defects.json, and which list none of them. This predicts which headings the round-58 edits (2 SOURCES rows + README F9 row + registry expect arrays + ledger install) will drift and how many re-readers wave 2 needs. Output %s/T58W1ScoutPin.json with the section-by-input map and a count.' % (W1,),
    axes=['calibration'], milestone='coldread input map')

# ---- connector (1) ----
add('T58W1ConnSib', 'connector',
    'Sibling overlap scan. Check the sibling lanes (repos /home/vgpnk/Projects/*-shokunin, READ-ONLY) for work that overlaps the round-58 claims: routed-defect ledgers, blind adjudication panels, strict registry-code binding, LLM-mutant/equivalence corpus entries, or delta-debugging/minimization entries. Report any overlap with evidence (path + line), classify absorb-vs-report per the lane PROVINCE Adjacent rule, and name what round-58 must cite or route instead of absorb. Output %s/T58W1ConnSib.json.' % (W1,),
    axes=['adjacency'], milestone='sibling overlap')

# ---- attack seats ----
add('T58W1CritClaims', 'critic',
    'Claim-shape critic. Read /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-58/contract.json. Attack each claim per the fleet claim-sizing rules: one concrete value re-derivable by one command over committed bytes; no universal clauses; calibration claim counts mismatches; do-nothing control pre-registered for each (C1 CTL_0/SKIP/... in controls.sh, C2 CTL_0/FAB..., C3 adoption sweep); counter == predicate == receipt label same sentence. Name any clause a do-nothing control could reach. Output %s/T58W1CritClaims.json.' % (W1,),
    axes=['calibration'], milestone='claim shape')
add('T58W1CritDisc', 'critic',
    'Do-nothing critic. For each claim, build the CHEAPEST do-nothing control in scratch and score it with the frozen counters: (C1) clone at base %s, overlay the instruments from the tip working tree, run .ufo/evidence/round-58/c1/measure.py --lane <clone> --rev <overlay head> --work <scratch> --explain - expect rows=0/51 and PASS=false; (C2) the same overlay WITHOUT the registry bare-code patch - expect rows shortfall >=1 and PASS=false; (C3) grep -rl 2406.09843 at base corpus/knowledge - expect 0 hits (the adoption cannot have happened). Also replay the round-56 C2 stub-receipt attack against the round-58 strict counter: show whether forged receipts can move any arm (they should not - the counter runs registry-check and the gate live; prove it by attempting the stub-receipt route and showing it cannot reach the arms). Output %s/T58W1CritDisc.json with every command + output.' % (BASE, W1),
    axes=['calibration'], milestone='do-nothing discriminators')
add('T58W1CritBlind', 'critic',
    'Panel-blindness critic. Audit the wave-1 dispatch for leaks that would break the blind panel: read /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-58/c1/defects.json (item texts only - confirm they carry no status judgments), the spec at /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/spec-w1.json (context + item texts), and the round-58 contract.json claims. Confirm none of them states or implies any item\'s round-58 status, and list every forbidden path the panel contract names. Then spot-check two panel seat JSONs (your pick, after they land - if none landed yet, say so and audit the contract only). Output %s/T58W1CritBlind.json.' % (W1,),
    axes=['calibration'], milestone='blindness audit')
add('T58W1CritC1', 'critic',
    'C1 semantics critic. Read /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-58/c1/measure.py (the round-58 copy). Verify the re-pin is semantically sound: status_at_base now means "at 2a32aa8228d5f86a85c81a923a3148bf792a9538", so items fixed by round-57 commits (ca75c267, adf87899, 120a055d, bc3c8895) are fixed-at-base with commit ancestors of base; the panel (judged at the same base by wave-1 seats) may disagree on at most PANEL_ALLOWED=5; THIS_ROUND_FLOOR=6 counts only post-base fixes. Name any way a do-nothing or round-57-recycled row set could still pass (e.g. old49 arm, spot arm, floors), and whether the <=5 disagreement budget plus the 6-new-fix floor jointly prevent claim laundering from round 57. Output %s/T58W1CritC1.json.' % (W1,),
    axes=['calibration'], milestone='C1 re-pin semantics')
add('T58W1CritC2', 'critic',
    'C2 strict critic. Read /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-58/c2/measure.py. Attack the strict element-equality upgrade: (a) confirm row_named_codes counts only elements EQUAL to a CODES member and the exit-2 row must name RECEIPT_REV_UNRESOLVABLE exactly; (b) try three bypasses in scratch fixture lanes: an element with trailing whitespace or case variants, an exit-2 row naming a different exact code plus the right one in another element, a registry row whose argv differs cosmetically (extra flag) - each must still be caught or you must report the bypass with a runnable command; (c) confirm the selftest cases P7/P8 pin the behavior. Output %s/T58W1CritC2.json.' % (W1,),
    axes=['operability'], milestone='C2 strict bypass attempts')
add('T58W1RevengerC2', 'revenger',
    'Reverse-engineer the round-56 C2 admission failure and attack the round-58 counter with it. Read /home/vgpnk/Projects/shokunin/tameshi-shokunin/SCORECARD.md round-56 section (the do-nothing discriminator note) and .ufo/waves/round-57/w3/T57W3CritContract.md. The round-56 counter passed on stub receipts; the round-58 counter must not read receipts at all. Verify by reading .ufo/evidence/round-58/c2/measure.py end to end: list every file path it reads and confirm none is a verdict receipt produced by a claimant (registry-check and the gate run live). Then attempt one novel forgery: e.g. a registry whose rows point registry-check at a fixture the claimant also wrote - does the mutants arm or the executed arm catch it? Show the command and result. Output %s/T58W1RevengerC2.json.' % (W1,),
    axes=['operability'], milestone='producer-provenance attack')
for i, target in enumerate(['c1', 'c2']):
    add(f'T58W1Mut{i+1:02d}', 'mutation-tester',
        f'Mutation seat for the round-58 {target} counter. In a scratch clone of the lane at the freeze/tip: apply 6 single-edit mutants to a COPY of .ufo/evidence/round-58/{target}/measure.py inside the clone (one behavioral edit each: flip a comparison, loosen a bound, weaken the strict matching, skip an arm, accept a malformed row, invert a verdict), run each mutated copy (selftest for behavior, and --lane <clone> --rev <rev> for measure behavior where feasible), and report killed/survived per mutant with the exact diffs and outputs. A survivor is a counter hole - name the input class that exploits it. Output {W1}/T58W1Mut{i+1:02d}.json.',
        axes=['calibration', 'operability'], milestone=f'{target} counter mutations')
add('T58W1Mut03', 'mutation-tester',
    'Mutation seat for the round-58 ledger generator. In a scratch clone of the lane at base %s with the round-58 instruments overlaid from the tip working tree, run .ufo/evidence/round-58/control/gen_ledger.py in each documented mode (skip, fab, open, bulkopen, quote-file+quote) and score each generated ledger with the round-58 C1 counter: every mode must make the counter print PASS=false and trip its named arm (CTL_SKIP panel_over, CTL_FAB evidence_bad, CTL_OPEN open_unplanned, CTL_BULKOPEN panel_over, CTL_QUOTE fixed_bad). Report per-mode command + verdict term. Output %s/T58W1Mut03.json.' % (BASE, W1),
    axes=['calibration'], milestone='gen_ledger modes scored')
add('T58W1Sent01', 'sentinel',
    'Write-scope sentinel. After the wave lands (or at your end), sweep /home/vgpnk/Projects/shokunin (fleet repo) `git status --porcelain` and the lane repo for files your sibling seats wrote outside /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w1/ (misroots at the fleet root); check no seat edited corpus/, SKILL.md, tools/ or .ufo/evidence/round-5[0-7]/; verify no seat ran a mutating git/jj command in the lane or fleet (scan the wave .md reports for the commands they claim). Output %s/T58W1Sent01.json; a clean sweep still prints the commands you ran.' % (W1,),
    axes=['calibration'], milestone='write scope sweep')
add('T58W1Sent02', 'sentinel',
    'Scratch + secrets sentinel. (a) Audit the round-58 instruments (c1/measure.py, c2/measure.py, controls.sh, no-harm.sh, deciding-run.sh, control/*.py) for hardcoded /tmp or non-TMPDIR scratch (QUALITY: a counter that writes under /tmp regardless of TMPDIR is a routed defect) - grep and report; (b) check the new source extracts (/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/l1/sources/) and the entry draft (/fast/scratch/hyaku/tameshi-r58/c0-drafts/) for credential material, session URLs or op:// references (none may land); (c) check /fast/scratch/hyaku usage: df -h /fast and du -sh /fast/scratch/hyaku/tameshi-r58, confirm no seat tree exceeds разумный size (report what you see). Output %s/T58W1Sent02.json.' % (W1,),
    axes=['operability'], milestone='scratch + secrets sweep')
add('T58W1RevFixOld', 'reviewer',
    'Fixed-at-base reviewer A. Independently verify, from the tree at base %s (scratch clone), whether these routed items are ALREADY resolved at base: R54.7, R54.9, R55.2, R56.2. For each: the item text is in .ufo/evidence/round-58/c1/defects.json; find the resolving commit (must be an ancestor of base) and the keyed excerpt that shows the resolution; note the round-57 blind panel judged these open - if you conclude fixed, your evidence becomes one of the <=5 panel disagreements, so hold it to a commit + excerpt standard. Output %s/T58W1RevFixOld.json.' % (BASE, W1),
    axes=['calibration'], milestone='fixed-at-base sample A')
add('T58W1RevFixOld2', 'reviewer',
    'Fixed-at-base reviewer B. Same contract as reviewer A for: R56.3, R56.4, R56.6, R56.7. Output %s/T58W1RevFixOld2.json.' % (W1,),
    axes=['calibration'], milestone='fixed-at-base sample B')
add('T58W1RevExcerpts', 'reviewer',
    'Excerpt compliance reviewer. Read the row-verify outputs %s/T58W1Verify01.json through T58W1Verify13.json as they land (poll once near your end; if absent, audit the contract instead). For a sample of 12 proposed fixed rows: check the excerpt is 15-400 chars, present in the named lines at the named state, carries a key token (from .ufo/evidence/round-58/c1/keys.json) as a whole token, is absent from the path at routed_at, and carries none of the counter ACK_WORDS (read ACK_WORDS in .ufo/evidence/round-58/c1/measure.py). Report per-row pass/fail with commands. Output %s/T58W1RevExcerpts.json.' % (W1, W1),
    axes=['calibration'], milestone='excerpt compliance sample')
add('T58W1RevPanelOld', 'reviewer',
    'Old-panel cross-check reviewer. The round-57 blind panel (.ufo/evidence/round-57/c1/panel.json - READ it, you are not blind) judged the 51 items against the ROUND-57 base; the round-58 panel judges against %s. For the 23 items the old panel calls fixed: verify in a scratch clone at the NEW base that the resolution still stands (the round-57 content commits are ancestors of the new base, so most should). Report per-item: old verdict, your re-check at new base, agree/disagree with command evidence. Output %s/T58W1RevPanelOld.json.' % (BASE, W1),
    axes=['calibration'], milestone='old panel cross-check')
add('T58W1RevSources', 'reviewer',
    'Sources reviewer. Re-open ONE of the three new sources independently (your pick: the arXiv abstract page, the dfcfw deck extract, or the Atlassian page) with your own fetch, locate the Gate quote, and compare with the L1 extract at /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/l1/sources/ - agree/disagree with your own access date and byte count. Then check the draft rows (/fast/scratch/hyaku/tameshi-r58/c0-drafts/sources-append.md) against the re-opened facts: any number, date or sha in a row that your fetch contradicts is a finding. Output %s/T58W1RevSources.json.' % (W1,),
    axes=['coverage'], milestone='source re-open sample')
add('T58W1RevC3Gate', 'reviewer',
    'C3 gate reviewer. Apply the per-entry gates to the draft entry /fast/scratch/hyaku/tameshi-r58/c0-drafts/entry-llm-mutant-equivalence-cost.md: (a) PROVINCE scope check (verification-fixture craft; LLM-mutant survivor counting is in-scope method, not product) - read /home/vgpnk/Projects/shokunin/tameshi-shokunin/PROVINCE.md; (b) QUALITY bar (read corpus/QUALITY.md criteria - provenance trio, falsifiable, no unverifiable claim); (c) expansion credit only on coverage-map ground the lane did not hold: verify F9 had zero held entries at base (grep corpus/knowledge for 2406.09843 and LLM-mutant entries at base via git show) and that the entry does not restate ground S001-S030 already hold; (d) the CANNOT-ANSWER / boundary honesty. Verdict: admit / reject with reasons. Output %s/T58W1RevC3Gate.json.' % (W1,),
    axes=['coverage'], milestone='C3 per-entry gate')

# ---- labrats (6) ----
LABRATS = [
    ('freshness at base', 'Run python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-45/freshness/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev %s and report population/fresh/score.' % BASE),
    ('coldread at base', 'Run bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-48/quality/coldread-precheck.sh /home/vgpnk/Projects/shokunin/tameshi-shokunin %s %s and report the last line (expect ok at base-vs-base).' % (BASE, BASE)),
    ('census manual at tip', 'Run the six manual census commands from /home/vgpnk/Projects/shokunin/CORPUS.md section SOURCES.md against /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md and report each output (rows count, malformed=0, tier histogram, status histogram, no duplicate ids, no enum violations, no missing used-by).'),
    ('gate rows held at tip', 'In a scratch clone of the lane at tip, run python3 tools/registry-check.py --root <clone> --rev <rev> --only receipt-gate-accept, --only receipt-gate-content-drift, --only receipt-gate-unresolvable-certified and report ROW lines (expect held 3/3).'),
    ('gate selftest at tip', 'Run python3 -I tools/receipt-revision-gate.py --selftest in a scratch clone at tip; expect GATE_SELFTEST: 19/19 pass.'),
    ('shrinker selftest at tip', 'Run python3 -I tools/shrink-case.py --selftest in a scratch clone at tip; report the last line (the no-harm monitor expects " failed=0").'),
]
for i, (ms, text) in enumerate(LABRATS):
    add(f'T58W1Lab{i+1:02d}', 'executor', 'Bounded probe (read-only; scratch clones only; no lane edits). %s Output %s/T58W1Lab%02d.json with command + output.' % (text, W1, i + 1),
        axes=['operability'], milestone='probe: ' + ms)

# ---- additional seats to reach 64 with genuine work ----
add('T58W1ExecS288', 'executor',
    'S285 supersession seat. Read the S285 row in /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md (read-only) and the L1 re-open receipt /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/l1/sources/atlassian-postmortems.txt. Verify the supersession draft row S288 (/fast/scratch/hyaku/tameshi-r58/c0-drafts/sources-append.md, third row) is the correct correction shape per CORPUS.md rule 2 (a new row whose teaches opens "supersedes S0NN -"; the old row untouched; status/reason preserved). Verify the S285 flip condition is restated in the new row or the lesson plan. Stage the exact SOURCES.md insertion point (the line after which the three rows append; show the surrounding lines). Output %s/T58W1ExecS288.json.' % (W1,),
    axes=['coverage'], milestone='S288 supersession check')
add('T58W1CritC3', 'critic',
    'C3 adoption critic. Attack the coverage claim before data: read the contract C3 entry, the draft entry and rows (/fast/scratch/hyaku/tameshi-r58/c0-drafts/), and the tip F9 row (corpus/README.md). (a) Is the before-state real: zero knowledge entries citing 2406.09843 at base (run the sweep at base via git show)? (b) Can a do-nothing control reach the after-state? (c) Does the entry cite BOTH new rows with used-by pointing at the entry (census mined rule)? (d) Is any number in the entry unsupported by the L1 extract receipts? (e) Does the adoption append rows the entry actually cites, and no more (CORPUS rule 4)? Output %s/T58W1CritC3.json.' % (W1,),
    axes=['coverage'], milestone='C3 pre-data attack')
add('T58W1RevDisagree', 'reviewer',
    'Disagreement-budget reviewer. Read the OLD round-57 panel verdicts (.ufo/evidence/round-57/c1/panel.json) and the contract\'s disagreement budget (PANEL_ALLOWED=5 in .ufo/evidence/round-58/c1/measure.py). List every item where a fixed-at-base conclusion at the NEW base would contradict the old panel\'s "open" verdict, ranked by the strength of the committed evidence you can see at base (commands you ran). Recommend which <=5 disagreements the round should spend, and which items should stay open even if arguably fixed (weakest evidence). Output %s/T58W1RevDisagree.json.' % (W1,),
    axes=['calibration'], milestone='disagreement budget plan')

assert len(ITEMS) == 67, len(ITEMS)
from collections import Counter
roles = Counter(i['role'] for i in ITEMS)
attack = roles['reviewer'] + roles['critic'] + roles['mutation-tester'] + roles['labrat']
print('roles:', dict(roles), 'attack:', attack, '/67 =', round(100 * attack / 67, 1), '%')

spec = {
    'wave': 'round-58-w1',
    'reportDir': '.ufo/waves/round-58/w1',
    'template': '/skill:godspeed\n' + GODSPEED + '\n\n## Your item\n\n{{item}}\n\nWork the item end to end, then write your report file and return your findings.\n',
    'context': CONTEXT,
    'items': ITEMS,
}
json.dump(spec, open('/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/spec-w1.json', 'w'), indent=1, ensure_ascii=False)
print('spec written:', '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/spec-w1.json')
