#!/usr/bin/env python3
"""Build the round-44 wave spec (w1: build + falsify in one v1 wave, 32 seats)."""
import json
import os
import sys

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
FLEET = '/home/vgpnk/Projects/shokunin'
STAGED = '/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md'
DIRECTIVE = open('/home/vgpnk/.agents/skills/godspeed/directive.md', encoding='utf-8').read().rstrip()
BASE = '506e99c7b73c85711f066895984d501fcf7539cd'
FREEZE = 'ba01973c73ad7de60e5bd19ae08255a1b7ef917e'
COUNTER = '%s/.ufo/evidence/round-44/calibration/measure.py' % LANE

TEMPLATE = ('/skill:godspeed\n' + DIRECTIVE +
            '\n\n## Your item\n\n{{item}}\n\nWork the item end to end, then write your report '
            'file and return your findings.\n')

COMMON = """# Goal
tameshi round 44 (hyaku run 6, attempt 1). Lane repo %(lane)s. Base `%(base)s`; freeze `%(freeze)s` (round-44 contract + the C1 counter + the Stryker snapshot committed before any seat and before the first deciding run). Read %(lane)s/.ufo/evidence/round-44/contract.json first; never edit it.

Two declared claims:
- C1 calibration (lowest non-retired axis, 6): record-agreement counter successor (round-43 C2) carries all seven classes m6 m7 m8 m10 m11 m12 m13 and prints total=0 at the round-44 landing commit. The round-43 false m7 alarm (`safe_floor=S256` read as an unknown citation) is resolved because an S-id bound to an assignment (key=S###) is a value, not a citation; genuine unknown/unmined citations still flag. Freeze `%(freeze)s`; counter %(counter)s; predicate C2_R44_PASS=true iff self_pin=1, classes=7, total=0. Counting command: `python3 %(counter)s --lane LANE --rev REV --freeze %(freeze)s`.
- C2 freshness (sourced): S089's stale anchor digest (bc572676...; the page drifted on 2026-10-25, text survives at the same offsets) is superseded by a new census-valid row S160 opened this round from the live Stryker equivalent-mutants page (sha256 79f6501a..., snapshot `%(lane)s/.ufo/evidence/round-44/sources/stryker-equivalent-mutants.html`), status mined, cited by a knowledge entry, old->new logged in the round-44 lesson. Counting command: `grep -cE '^ {0,3}\\| S160 ' corpus/SOURCES.md` (0 at base -> 1 at landing).

REV values you may measure: `%(base)s` (base) and `%(freeze)s` (freeze). NEVER run a counter against any other revision as a measurement; the ONE deciding run is the L1's. Control modes allowed: `--selftest`; the old round-43 counter at %(lane)s/.ufo/evidence/round-43/calibration/measure.py (its freeze 6b83a11c61f0fad1074ec1f2a4c38a2fd7034685).

Assimilation package (READ-ONLY: never write, commit, fetch or push there, never run a campaign tool): /home/vgpnk/Projects/shokuknow. This round: `Assimilation: none`; the quarantine slice verdicts are held from the round-40 lesson; re-derive the slice read-only if your item says so.

Bounds for every seat: you are READ-ONLY on the lane checkout unless your item names a scratch directory or a draft. Never edit %(fleet)s (the fleet repo), a sibling lane, the lane's jj state or Git index. Never run git add/commit/stash/checkout/switch/reset/pull/push in the lane and never run a mutating jj command. Absolute paths only: seat tools start at the FLEET root, not the lane. Scratch work goes under /tmp/tameshi-r44-<YourName>-* and is deleted before you return unless your item says otherwise. Never run /home/vgpnk/Projects/shokuknow/scripts/* (they write into the campaign repo).

Every `Report:` trailer path is relative to %(lane)s — write it at %(lane)s/<that path>. Keep your report to findings with file:line and command output. Never `agent://all`.

Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first, use official channels only. **pacman is PAUSED host-wide**: no pacman transaction at all; use uv tool / npx / an official binary in ~/.local/bin, and record tool/version/channel/reason in your report. Route table, not this prompt, decides your model; never pass a model parameter.
""".replace('%(lane)s', LANE).replace('%(base)s', BASE).replace('%(freeze)s', FREEZE).replace(
    '%(staged)s', STAGED).replace('%(fleet)s', FLEET).replace('%(counter)s', COUNTER)

W1 = [
    ("SimplCounter", "simplifier", ["calibration"], "counter dead code / tautology",
     "Review %s -- for dead code, tautological conditions and unreachable branches (e.g. the MASK_IDS label-skip logic, the quantification lambda closures, any `if` whose truth is constant). Propose deletions that preserve the frozen predicate and the 16 selftest cases; verify each proposed deletion by copying the counter to /tmp/tameshi-r44-SimplCounter-/ and running `--selftest` (must stay 16/16). Report each deletion with file:line and the selftest line after it. Do NOT edit the lane file." % COUNTER),
    ("RevCounterDiff", "reviewer", ["calibration"], "counter delta review",
     "Diff the round-44 counter (%s) against the round-43 counter (git show %s:.ufo/evidence/round-43/calibration/measure.py) in /tmp/tameshi-r44-RevCounterDiff-/. Report every change chunk. The ONLY intended changes are: (1) ASSIGN_ID regex + its use in m7_citations (value-vs-citation assignment masking), (2) m7 refactored into m7_citations(), (3) four new T6 selftest cases, (4) label C2_R43->C2_R44, (5) self/contract paths point at round-44, (6) the contract-pin claim discovery loop. Flag anything else as an unintended change, with the diff hunk." % (COUNTER, BASE)),
    ("RevPredicateSame", "reviewer", ["calibration"], "claim sentence = predicate",
     "Read claims.C1/C2 in %s/.ufo/evidence/round-44/contract.json, the counter's docstring predicate, and the receipt label C2_R44_PASS. For each claim, quote the contract sentence, the predicate sentence and the printed label side by side and say whether they are the SAME statement. Flag any widening or narrowing, and any universal quantifier ('all', 'every', 'no') whose set the counter does not enumerate. Also check C2's target sentence equals the report plan wording." % LANE),
    ("RevSelftestAudit", "reviewer", ["calibration"], "selftest vacuity audit",
     "Audit the counter's 16 selftest cases for vacuity: for each case, state what rule it proves and construct a one-line mutation of the counter (in /tmp/tameshi-r44-RevSelftestAudit-/) that breaks that rule; run `--selftest` and require the case to FAIL. Report one mutation per case that fails, or name the case with no failing mutation (vacuity). At minimum prove T6_safe_floor_value_not_citation fails when ASSIGN_ID is removed and T6_genuine_unknown_still_flagged fails when the unknown branch is deleted." % {}),
    ("RevS160Row", "reviewer", ["freshness"], "S160 row contract review",
     "Validate the S160 draft row in the L1's report-scratch if present; otherwise validate against the CORPUS.md row contract: 11 columns (NF=13 when split on |), no literal or escaped `|` inside any cell, id S160 next-unused, kind=docs, tier=A (not community), scope scoped to 'supersedes S089's anchor only', anchor names the committed snapshot and sha256 79f6501a..., teaches opens `supersedes S089 —`, status=mined, opened=2026-10-25, recheck=180d, used-by lists the knowledge entry path. A duplicate-URL W04 census warning for S160 is acceptable (warning, exit 0) because S089 already holds the URL; verify the census CLI treats it as W04, not E-codes, with a scratch validate run. Report each deviation." % {}),
    ("RevAnchorOldNew", "reviewer", ["freshness"], "anchor old->new rule",
     "Read CORPUS.md rule 2 (append-only: only status/recheck/used-by change in place; a correction is a new supersede row) and the S092 precedent row (supersedes S059 anchor only). Verify that the planned S160 row (a) keeps S089 untouched except its log entry, (b) is the lane-canonical form for an anchor-digest refresh, (c) records old digest bc572676... -> new 79f6501a... in the round-44 lesson. Quote the rule line and the S092 row. Flag any in-place anchor edit plan as a violation." % {}),
    ("ExecCensusBefore", "executor", ["calibration"], "sources census before",
     "Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`. Report stdout, stderr, exit code, E-codes and warnings, and the implied row count (`grep -cE '^ {0,3}\\| S[0-9]{3} \\|' %s/corpus/SOURCES.md`). Save the output to /tmp/tameshi-r44-ExecCensusBefore-/census-start.stdout for the L1; do not edit corpus." % LANE),
    ("CritDoNothingC1", "critic", ["calibration"], "C1 do-nothing + red-before",
     "Prove the C1 control claims: (1) run the round-43 counter at base with `--rev %s --freeze 6b83a11c61f0fad1074ec1f2a4c38a2fd7034685` and confirm it prints `m7=1 total=1 first=m7:SCORECARD.md#round-43_unknown_S256 C2_R43_PASS=false` exit 1 (receipt exists at %s/.ufo/evidence/round-44/before/c2-old-at-base.stdout; verify the line rather than trust it). (2) copy the round-44 counter to /tmp/tameshi-r44-CritDoNothingC1-/, delete the ASSIGN_ID application line, run `--selftest` and confirm T6_safe_floor_value_not_citation FAILs with ['r unknown S256']. (3) attempt the cheapest alternate path to make C1 read total=0 without the mask fix (e.g. editing the scorecard block in a scratch mirror); report whether any such path is both legal (append-only) and reaches the target." % (BASE, LANE)),
    ("CritM7Escapes", "critic", ["calibration"], "mask escape attempts",
     "Attack the new assignment mask. In /tmp/tameshi-r44-CritM7Escapes-/ run the counter's m7_citations logic (import the module) over records containing each form: `safe_floor=S256`, `safe_floor = S256`, `safe_floor= S256`, `SAFE_FLOOR:S256`, `safe_floor(S256)`, `` `safe_floor=S256` ``, `safe_floor==S256`, `x=staged:S153`. Report for each whether it is masked or flagged, and whether the mask's documented scope ('an S-id bound to an assignment') covers it. Flag any form that both (a) appears in a real receipt or record and (b) is still flagged." % {}),
    ("CritM7Recall", "critic", ["calibration"], "mask recall preservation",
     "Prove recall is preserved. Use the counter module in /tmp/tameshi-r44-CritM7Recall-/ with a registry fixture {S001 mined, S002 queued, S153 mined} and records: (a) `claims cite S777` -> must hit 'unknown S777'; (b) `cites S002` -> must hit 'unmined S002'; (c) `cites S001` -> no hit; (d) `staged:S153` -> no hit; (e) `Next unused id: S999` -> no hit; (f) `safe_floor=S256` -> no hit. Paste the six outputs and the verdict." % {}),
    ("CritC2Target", "critic", ["freshness"], "C2 target reachability",
     "Attack the C2 target: can any do-nothing control make `grep -cE '^ {0,3}\\| S160 ' corpus/SOURCES.md` print 1 without appending a row? Check the registry tail for any pre-existing S160 mention, any other id that would match the pattern, and whether the next-unused id line or the search log section could match. Also check that appending S160 does not collide with staged ids (S153-S159 are the staged collisions; S160 is not staged). Report the grep output at base and the collision evidence." % {}),
    ("CritC1Loop", "critic", ["calibration"], "C1 loop attack",
     "Attack the measurement loop: in /tmp/tameshi-r44-CritC1Loop-/ create a scratch tree mirror of the lane at freeze-like state, remove the `**Planned (round 45):**` field from the newest SCORECARD block, and run the round-44 counter against the mirror (--lane /tmp/... --rev <mirror commit> --freeze %s). It must print m12=1. Then restore the field and confirm m12=0. This proves m12 is load-bearing. Report both lines. Also run the counter against a mirror where the standing sources-registry row's command is column-zero; it must print m13=1." % FREEZE),
    ("MutMaskRemove", "mutation-tester", ["calibration"], "mask mutation",
     "Copy the round-44 counter to /tmp/tameshi-r44-MutMaskRemove-/measure.py and remove ONLY the `ASSIGN_ID.sub(...)` line; run `--selftest`. Report cases/failed/exit verbatim. Expected: failed=2 (T6_safe_floor_value_not_citation, T6_assign_with_spaces_masked) with ['r unknown S256']. This is the red-before receipt for the fix." % {}),
    ("MutS160UsedBy", "mutation-tester", ["freshness"], "S160 load-bearing",
     "Prove S160's mined/used-by is load-bearing. Build /tmp/tameshi-r44-MutS160UsedBy-/corpus/SOURCES.md by copying the lane's corpus and inserting the S160 draft row, in two versions: (A) used-by = the knowledge entry path (mined), (B) used-by = '—' (still mined under census). Run the census CLI on both mirrors (`--file`) and run `grep -cE '^ {0,3}\\| S160 '` on both. Also run the knowledge-entry provenance trio check: an entry whose `source:` cites S160 must fail its own check when S160 is absent from the registry. Report which checks fire on A vs B and what that proves about C2's landing requirements." % {}),
    ("MutOldBug", "mutation-tester", ["calibration"], "old-bug reproduction",
     "Reproduce the round-43 bug precisely in /tmp/tameshi-r44-MutOldBug-: take the round-44 counter, remove `safe_floor` (underscore) from the ASSIGN_ID/mask surface by replacing the ASSIGN_ID pattern with the round-43 VALUE_ID_AFTER-only state, and run `--selftest`. Confirm T6 cases fail and that `VALUE_ID_AFTER` alone (with 'safe floor' prose) also misses `safe_floor=S256` — quote the regex and the failing stdout." % {}),
    ("ScoutBaseState", "scout", ["calibration"], "base state facts",
     "Gather the base facts for the L1: `git -C %s rev-parse master`, `git -C %s status --porcelain`, the S089 row bytes (`grep -n '| S089 |' %s/corpus/SOURCES.md`), the round-43 SCORECARD block's `safe_floor=S256` line and line number, the round-43 counter receipt line at base, and the next-unused-id note at the registry tail. Paste each raw. Do not change anything." % (LANE, LANE, LANE)),
    ("ScoutQuarantine", "scout", ["coverage"], "quarantine slice re-derivation",
     "Re-derive this lane's slice of /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md (read-only; header and By-lane summary are stale — derive data rows yourself): `awk -F'|' -v l='tameshi' '$2 ~ (\"`\" l \"`\") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}'`. Report the row count, the ids, and the family of each (payload-absent vs could-not-be-fetched). Compare to the round-40 lesson's 17-row list (must be byte-identical). Verdicts stay in the round-40 lesson; no adoption." % {}),
    ("ScoutConsiderthese", "scout", ["calibration"], "considerthese scan",
     "Read every file in %s/considerthese/ (operator-authored input; mine, never edit). List each proposal in 2026-10-24.md with its status, and name the ONE still-unimplemented proposal closest to this round's claims (record agreement, citation/revision provenance). Quote its text. Recommend the landing form (lesson / QUALITY criterion / SOURCES row citing considerthese/2026-10-24.md + date). Report which proposals earlier rounds already mined and which were implemented." % LANE),
    ("ScoutStrykerSnapshot", "scout", ["freshness"], "Stryker snapshot verify",
     "Open the committed snapshot %s/.ufo/evidence/round-44/sources/stryker-equivalent-mutants.html and the live https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/ (curl -fsSL into /tmp/tameshi-r44-ScoutStrykerSnapshot-/). Report size, sha256 and <title> for both; confirm byte-identity; locate lines 15-17 verbatim, the `10 ** 0` example, and the two <=25-word quotes with HTML line numbers; state your access date 2026-10-25. Confirm the sha256 equals 79f6501a... and differs from S089's 2026-10-22 anchor bc572676..." % LANE),
    ("ScoutMisroot", "scout", ["scope"], "fleet-root misroot scan",
     "Run `git -C /home/vgpnk/Projects/shokunin status --porcelain` (no pathspec). For every untracked or modified file at the fleet root, read its head and report whether its content names tameshi round-44 (or a seat name from this wave). Do NOT delete or edit anything; just report paths and matches. Also check %s/.ufo/waves/round-44/ exists and list its contents." % LANE),
    ("ExecMeasureBase", "executor", ["calibration"], "base measurements",
     "Run and save: (1) `python3 %s --lane %s --rev %s --freeze %s` -> receipt; (2) the old round-43 counter at the same rev -> receipt; (3) `git show %s:tools/mutate-and-run.sh | python3 -c 'import re,sys; n=len(re.findall(r\"^#   (?:js|bash)-\\S+\\s+\\S+\\s+\\d+/\\d+\",sys.stdin.read(),re.M)); print(\"recorded_cases=\"+str(n)+\" depth_score=\"+str(min(10,n)))'` (command D); (4) `python3 %s/.ufo/evidence/round-21/coldread/measure.py --repo %s --rev %s` (calibration monitor). Paste all four verbatim with exit codes into /tmp/tameshi-r44-ExecMeasureBase-/ (the L1 copies receipts from there)." % (COUNTER, LANE, BASE, FREEZE, BASE, LANE, LANE, BASE)),
    ("ExecRegistryMirror", "executor", ["freshness"], "registry mirror gate",
     "Build /tmp/tameshi-r44-ExecRegistryMirror-/corpus/ by copying the lane's corpus/ (cp -r %s/corpus .). Insert the S160 draft row before the registry tail note and the knowledge-entry file at its planned path. Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /tmp/tameshi-r44-ExecRegistryMirror-/corpus/SOURCES.md`; report exit, warnings, E-codes. Then indent one data row by two spaces in a second copy and re-run; confirm the row count still counts it. Paste the validate lines." % LANE),
    ("ExecEntryProbe", "executor", ["freshness"], "entry provenance trio",
     "Implement and run a read-only provenance-trio probe for the planned knowledge entry (source:, verified-at:, recheck:): in /tmp/tameshi-r44-ExecEntryProbe- write the three-line check (source: cites S160 and the URL; verified-at: is an ISO date; recheck: is an ISO date or cadence), run it against the draft entry if available, else against the r43-survivor-resolution-rule.md entry as a model, and report the outputs. Show the probe fails when `source:` is removed." % {}),
    ("SentinelScope", "sentinel", ["scope"], "write scope audit",
     "List every file the round-44 changes need to touch: corpus/SOURCES.md (append S160 + used-by log), corpus/knowledge/r44-anchor-refresh-rule.md (new), corpus/lessons/round-44.md (new), SCORECARD.md (append round-44 block), LOG.md (append), .ufo/evidence/round-44/** (receipts; .ufo/waves/round-44/** (wave specs/reports), and the dirty .ufo/waves/round-43/w1/RevC2Classes.md (commit or revert). Confirm none lies outside the lane, in a sibling, in /home/vgpnk/Projects/shokuknow, or in /home/vgpnk/Projects/shokunin/.ufo/state. Report any planned path outside that set with its justification." % {}),
    ("SentinelIdGuard", "sentinel", ["freshness"], "staged id collision guard",
     "Run the staged-id guard read-only: `python3 %s/tools/staged-id-guard.py --registry %s/corpus/SOURCES.md --staged %s --json` (or the folder's own tool) and report collisions, held, unmapped, safe_floor and verdict. Confirm S160 is not a staged id (the staged set tops out below S160) and that appending S160 does not collide with any staged id. Paste the id lists (registry tail ids vs staged ids)." % (LANE, LANE, STAGED)),
    ("ConnOverlap", "connector", ["adjacency"], "sibling overlap scan",
     "Scan sibling lane repos under /home/vgpnk/Projects/shokunin (kumitate, kagi, kaidoku, kake, kotoba, mado, tsukuroi) for (a) any registry-row practice with in-place anchor edits or supersede rows, and (b) any extractor that distinguishes citation S-ids from value S-ids. Report paths, scope, and whether this round's S160 supersede row / ASSIGN_ID mask overlaps or duplicates one. Read-only; never write a sibling. If none, say which lanes you searched and the command." % {}),
    ("RevCause", "revenger", ["calibration"], "closure failure root cause",
     "Reverse-engineer the byte-level cause of the round-43 closure m7 first-hit. In the committed SCORECARD round-43 block at %s, locate the exact `safe_floor=S256` token (line number and bytes). Show the round-43 mask handles `safe floor` (space) but not `safe_floor` (underscore) by quoting the regex and running the old counter's m7 mask on the exact line in /tmp/tameshi-r44-RevCause- (import the old measure.py from git show). Report the old output line, the new output line (run the round-44 counter on the same block), and the byte diff of the two regexes." % BASE),
    ("ScribeLessonDraft", "scribe", ["depth"], "round-44 lesson draft",
     "Draft `## Gate` and `## Mistakes` for %s/corpus/lessons/round-44.md in your report (do not write the lesson). Gate: one admit block for S160 (URL, access date 2026-10-25, byte count 38687, sha256 79f6501a..., two <=25-word located quotes with line numbers 15-16, and the teaches sentence 'supersedes S089 — anchor only'); one note for S089 re-open (digest drift, text survives, old->new log). Mistakes rows (CORPUS.md vocabulary): (a) class scope/extractor-narrower — m7 missed the underscore form safe_floor=S256; evidence pointer = old-counter receipt `m7=1 ... first=m7:SCORECARD.md#round-43_unknown_S256`; captured-by = none (no criterion required the mask to cover assignment forms); fix = ASSIGN_ID mask + T6 cases, shown able to fail by the mask-removed control. (b) class landing — the round-43 wave-1 note .ufo/waves/round-43/w1/RevC2Classes.md was left modified in the worktree at closure; captured-by = none; fix = committed under round 44 (or reverted), disposition named. Read %s/corpus/lessons/round-43.md for the shape." % (LANE, LANE)),
    ("ScribeScorecardDraft", "scribe", ["calibration"], "scorecard round-44 block draft",
     "Draft the `## Round 44` SCORECARD block in your report (do not edit the file), matching the contract sentences verbatim: the claims table with rows C1 (calibration, before = old counter at base `m7=1 total=1 C2_R43_PASS=false` and new counter at base `m12=1 total=1 C2_R44_PASS=false`, after = landing `C2_R44_PASS=true total=0`, command = `python3 .ufo/evidence/round-44/calibration/measure.py --lane LANE --rev REV --freeze FREEZE`) and C2 (freshness, before = `grep -cE '^ {0,3}\\| S160 ' corpus/SOURCES.md` -> 0, after -> 1). Include the numeric-axes receipt lines (command D, coldread monitor) and the `**Planned (round 45):**` field with a real planned list. Keep every cell free of `|`." % {}),
    ("ScribeLogDraft", "scribe", ["depth"], "LOG entry draft",
     "Draft the round-44 LOG.md entry skeleton in your report (do not edit): one line per claim with evidence pointer (receipt path), the frontier-step lines (census before/after, S160 opened, mistake mined, sourced claim), the misroot sweep line, and the tooling/install line (none unless you installed). Match the existing LOG.md entry format in %s/LOG.md's newest entry." % LANE),
    ("RevAccidents", "reviewer", ["calibration"], "landing-block S-token pre-scan",
     "Pre-scan what the round-44 landing SCORECARD block and lesson will carry for m7-relevant tokens: list every S[0-9]{3,} token the drafts will carry (S089, S159, S160, etc.), check each against the registry (exists? mined?), and check for `key=S###` receipt fields that the ASSIGN_ID mask will hide (list them explicitly). Report any token that is (a) neither a registry row nor an assignment value, or (b) an unmined registry row — those must be resolved before landing. Read %s/corpus/SOURCES.md rows S089/S159 and the round-43 scorecard block." % LANE),
    ("ScoutGoalFile", "scout", ["scope"], "goal file and session bounds",
     "Read %s/.scratch/goal-20261025-hyaku-12h.md (orchestrator-owned; read-only) and report the lane-order and blocks/holds entries that name tameshi, including any hold or operator ruling affecting round 44. Quote the relevant lines. Do not edit anything under .scratch/." % FLEET),
]

assert len(W1) == 32, len(W1)


def build(wave, report_dir, items):
    return {
        "wave": "round-44-%s" % wave,
        "reportDir": report_dir,
        "template": TEMPLATE,
        "context": COMMON,
        "items": [
            {
                "name": name,
                "role": role,
                "axes": axes,
                "milestone": milestone,
                "item": item,
            }
            for name, role, axes, milestone, item in items
        ],
    }


def main():
    w = build("w1", ".ufo/waves/round-44/w1", W1)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spec-w1.json")
    with open(out, "w", encoding="utf-8") as handle:
        json.dump(w, handle, indent=2, ensure_ascii=False)
    print("wrote %s with %d items" % (out, len(w["items"])))


if __name__ == "__main__":
    main()
