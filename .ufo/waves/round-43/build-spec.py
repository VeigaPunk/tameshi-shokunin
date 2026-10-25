#!/usr/bin/env python3
"""Build the round-43 wave specs (w1 build+falsify, w2 falsify)."""
import json
import os
import sys

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
FLEET = '/home/vgpnk/Projects/shokunin'
STAGED = '/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md'
DIRECTIVE = open('/home/vgpnk/.agents/skills/godspeed/directive.md', encoding='utf-8').read().rstrip()
BASE = '487b8f0da89fa0e2b8bea6930068accbf36e70a9'
FREEZE = os.environ.get('FREEZE', '')

TEMPLATE = ('/skill:godspeed\n' + DIRECTIVE +
            '\n\n## Your item\n\n{{item}}\n\nWork the item end to end, then write your report '
            'file and return your findings.\n')

COMMON = """# Goal
tameshi round 43 (hyaku run 6, attempt 1). Lane repo %(lane)s. Base `%(base)s`; freeze `%(freeze)s` (contract + three counters + the guard tool committed before any seat and before the first deciding run). Read %(lane)s/.ufo/evidence/round-43/contract.json first; never edit it.

Three declared claims:
- C1 depth: the two round-42 survivors are resolved under the pre-declared K/D/E/U rule — outflag_no_parse_args_check killed by a reachable-code fixture (F11_outflag_namespace); method_fold_several_returns classified dead_code_only (it diverges only on a fixture with a statement after an unconditional return). Round-42 mutant declaration unchanged.
- C2 calibration (lowest non-retired axis, 6): record agreement over seven classes, m6 m7 m8 m10 m11 carried from round 42 plus m12 (the newest SCORECARD round block declares the next round's planned claims) and m13 (the newest standing sources-registry counting command is census-valid and load-bearing on an indented mirror).
- C3 operability (capability): tools/staged-id-guard.py answers the round-42 post-append hazard before any append — collisions with the census-valid 0-3-space pattern, document-keyed dedupe, refusal of its own naive arithmetic map (its targets are still staged ids), admission only of a by-document map at or above the safe floor.

Counters (run them; they are read-only apart from /tmp):
  C1 `python3 %(lane)s/.ufo/evidence/round-43/mutants/measure.py --lane %(lane)s --rev REV --freeze %(freeze)s`
  C2 `python3 %(lane)s/.ufo/evidence/round-43/calibration/measure.py --lane %(lane)s --rev REV --freeze %(freeze)s`
  C3 `python3 %(lane)s/.ufo/evidence/round-43/guard/measure.py --lane %(lane)s --rev REV --freeze %(freeze)s`
REV values you may measure: `%(base)s` (base) and `%(freeze)s` (freeze). NEVER run a counter against any other revision as a measurement; the ONE deciding run is the L1's. Control modes that are allowed: C1 `--control` and `--probe-mutant PATH`, C2 `--selftest`, C3 `--control` and `--tool-file PATH`.

Assimilation package (READ-ONLY: never write, commit, fetch or push there, never run a campaign tool): /home/vgpnk/Projects/shokuknow — this round's theme is the survivor-resolution rule; stage bytes are at /home/vgpnk/Projects/shokuknow/merge/tameshi/ and the staged registry at %(staged)s. Do not adopt anything: this round is `Assimilation: none`.

Bounds for every seat: you are READ-ONLY on the lane checkout unless your item names a scratch directory. Never edit %(fleet)s (the fleet repo), a sibling lane, the lane's jj state or Git index. Never run git add/commit/stash/checkout/switch/reset/pull/push in the lane and never run a mutating jj command. Absolute paths only: seat tools start at the FLEET root, not the lane. Scratch work goes under /tmp/tameshi-r43-<YourName>-* and is deleted before you return unless your item says otherwise.

Every `Report:` trailer path is relative to %(lane)s — write it at %(lane)s/<that path>. Keep your report to your findings with file:line and command output.

Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first, use official channels only. **pacman is PAUSED host-wide** (mado r15 incident): no pacman transaction at all, not even a dry-run install; use uv tool / npx / an official binary in ~/.local/bin, and record tool/version/channel/reason in your report.
""".replace('%(lane)s', LANE).replace('%(base)s', BASE).replace('%(freeze)s', FREEZE).replace(
    '%(staged)s', STAGED).replace('%(fleet)s', FLEET)

W1 = [
    ("ScoutStrykerEquiv", "scout", ["freshness"], "S159 (Stryker equivalent mutants)",
     "Open https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/ with curl -fsSL into /tmp/tameshi-r43-ScoutStrykerEquiv-/. Report bytes, sha256 and the <title>. Locate the verbatim sentence that says a tool cannot find and ignore equivalent mutants, plus the 10 ** 0 example, with HTML line numbers. Give two <=25-word located quotes with your access date 2026-10-25 and say which sentence would ground a lane rule that a survivor needs an explicit classification rather than a tool verdict."),
    ("ScoutWikiEquiv", "scout", ["depth"], "S160 (Wikipedia mutation testing)",
     "Open https://en.wikipedia.org/wiki/Mutation_testing with curl -fsSL into /tmp/tameshi-r43-ScoutWikiEquiv-/. Report bytes, sha256, <title>. In the Equivalent mutants section locate the sentences defining an equivalent mutant and calling their detection an obstacle, with HTML line numbers. Give two <=25-word located quotes with access date 2026-10-25. State whether the page distinguishes an equivalent mutant from a survivor on unreachable code — this lane must not conflate them."),
    ("ScoutPitEquiv", "scout", ["depth"], "held S156 re-open",
     "Re-open the committed snapshot %(lane)s/.ufo/evidence/round-42/sources/pit-faq.html and the live https://pitest.org/faq/ (curl -fsSL into /tmp/tameshi-r43-ScoutPitEquiv-/). Report whether the FAQ says anything about equivalent or unkillable mutants, with line numbers, and whether the live page still matches the snapshot sha256 ccf6ac49. If it says nothing, say so and name the nearest section. Two <=25-word located quotes or an explicit 'no such text'." % {"lane": LANE}),
    ("RevC1Counter", "reviewer", ["depth"], "C1 counter correctness",
     "Read %(lane)s/.ufo/evidence/round-43/mutants/measure.py and %(lane)s/.ufo/evidence/round-43/contract.json claims.C1. Check line by line: the exit-plus-FAIL oracle, the K/D/E/U derivation, which fixture each kill rests on, the naming requirement (killed must contain outflag_no_parse_args_check; dead_code_only must contain method_fold_several_returns), and whether the predicate can pass while a survivor is only relabelled. Report each mismatch as file:line + what the code prints instead. Do not edit anything." % {"lane": LANE}),
    ("CritC1DeadCode", "critic", ["depth"], "C1 dead-code judgment",
     "Attack the dead-code judgment. method_fold_several_returns changes `if len(returns) != 1` to `if len(returns) < 1` in %(lane)s/tools/write-path-census-v4.py:139. Construct Python inputs in /tmp/tameshi-r43-CritC1DeadCode-/ where a method has two or more TOP-LEVEL returns without one being unreachable (i.e. a case that is reachable code). Run the pristine tool and the mutant (copy the tool, apply the one edit; the mutant bytes are reproducible from %(lane)s/.ufo/evidence/round-42/census/mutants.json) and diff their JSON. If you find a reachable-input difference, the dead_code_only classification is wrong and you must say so with the exact source. If you cannot, state the structural argument that makes two top-level returns imply unreachable code." % {"lane": LANE}),
    ("MutC1F11", "mutation-tester", ["depth"], "F11 kill attribution",
     "Prove the F11 kill is F11's. Copy the C1 counter to /tmp/tameshi-r43-MutC1F11-/measure.py, remove only the F11 entry from its FIXTURES dict (keep F12), run it with --rev %(freeze)s --freeze %(freeze)s --lane %(lane)s and report mutants_killed and killed_names. Then run the unmodified counter the same way and report the same fields. The delta is F11's attribution; report both lines verbatim and the exit codes." % {"lane": LANE, "freeze": FREEZE}),
    ("MutC1F12", "mutation-tester", ["depth"], "F12 differential attribution",
     "Verify F12 is not counted as a kill. Copy the counter to /tmp/tameshi-r43-MutC1F12-/measure.py and change F12's declared `want` from expected=False to expected=True (a wrong declaration), run it with --rev %(freeze)s --freeze %(freeze)s --lane %(lane)s, and report whether method_fold_several_returns moves from dead_code_only to killed — it must, because the mutant then FAILs the battery. Then restore F12 and report the unmodified line. Also state whether `dead_code_arg_ok` is computed from the differential or hardcoded." % {"lane": LANE, "freeze": FREEZE}),
    ("RevC1FixtureSpec", "reviewer", ["depth"], "fixture-as-spec review",
     "Review F11_outflag_namespace and F12_method_two_returns in %(lane)s/.ufo/evidence/round-43/mutants/measure.py as SPEC statements, not as observations: what is each fixture asserting about %(lane)s/tools/write-path-census-v4.py's documented behavior (read its docstring and the round-42 knowledge entry %(lane)s/corpus/knowledge/r42-attribute-and-outflag-destinations.md), and is the declared classification derivable from that document rather than from running the tool? Report any fixture whose declared class is only 'whatever the tool printed'." % {"lane": LANE}),
    ("CritC1Overfit", "critic", ["depth"], "kill-oracle overfit",
     "Attack the kill oracle. The counter pins %(lane)s/tools/write-path-census-v4.py by sha256 from the contract. In /tmp/tameshi-r43-CritC1Overfit-/ build a tool that special-cases the twelve fixture filenames and the three live paths and reports their declared classes, then run the C1 counter with that file substituted for the tool (clone the counter into /tmp, point TOOL_REL at the substitute) and report whether it passes C1_R43_PASS. If the pin stops it, report the exact field that fails; if a path around the pin exists, name it." % {"lane": LANE}),
    ("RevC2Classes", "reviewer", ["calibration"], "C2 class-to-code agreement",
     "Read %(lane)s/.ufo/evidence/round-43/calibration/measure.py against claims.C2 in the contract. For each of m6 m7 m8 m10 m11 m12 m13, quote the class sentence from the contract and the code that implements it (file:line) and say whether they are the same statement. Report any class whose code is broader or narrower than its sentence, and any class that can be zero without its subject existing (vacuity)." % {"lane": LANE}),
    ("CritC2Vacuous", "critic", ["calibration"], "C2 vacuity attack",
     "Attack the new classes for vacuity and for masking. In /tmp/tameshi-r43-CritC2Vacuous-/ construct (a) a record text whose only S-id is inside a `staged:S###` token or after 'Next unused id:' (m7 must stay 0, and you must say whether that is right), (b) a backtick path cite in a form the m8 extractor drops (absolute path, `…/` elision, brace form, a directory), (c) a presence receipt whose path resolves only after prefix resolution. Report, for each, what the counter does and whether the counter is right to do it. Do not edit the lane." % {}),
    ("ExecC2IndentProbe", "executor", ["calibration"], "m13 indent probe reproduction",
     "Independently reproduce the m13 probe. In /tmp/tameshi-r43-ExecC2IndentProbe-/ copy %(lane)s/corpus/SOURCES.md, indent one data row by two spaces, and count rows with (a) `grep -cE '^\\| S[0-9]{3} \\|'` and (b) `grep -cE '^ {0,3}\\| S[0-9]{3} \\|'`. Report both counts, the delta and the row you indented. Then report what %(lane)s/scripts/… is not to be edited; instead quote the census clause in %(fleet)s/CORPUS.md that accepts 0-3 leading spaces (file:line)." % {"lane": LANE, "fleet": FLEET}),
    ("RevC2DoNothing", "reviewer", ["calibration"], "C2 do-nothing control",
     "Verify the C2 do-nothing control claim in the contract: that the round-42 C1 counter (%(lane)s/.ufo/evidence/round-42/calibration/measure.py) prints no m12/m13 and no classes field, so it cannot satisfy the round-43 target. Read its printed fields from %(lane)s/.ufo/evidence/round-42/after/c1-at-242c1b4a.stdout and from its source, and state whether a reader could score the round-43 target from that line. Also say whether `classes=7` in the round-43 counter is evidence that seven classes ran, or a constant." % {"lane": LANE}),
    ("CritC2Gaming", "critic", ["calibration"], "C2 gaming",
     "Attack m12 and m13 for gameability. m12 wants a `**Planned (round 44):**` line in the newest SCORECARD block; m13 wants the newest standing sources-registry row to name the 0-3-space pattern. In /tmp/tameshi-r43-CritC2Gaming-/ write what the cheapest edit that passes both is, and whether that edit requires any real repair (the planned line naming 1-3 claims, the standing row's count still matching the registry). Report whether the target is reachable by a do-nothing edit and, if so, what the counter should require." % {}),
    ("ScoutC2Records", "scout", ["calibration"], "SCORECARD contract sweep",
     "Sweep %(lane)s/SCORECARD.md for other missing required fields from the AXES.md SCORECARD contract (axes, capabilities, planned, saturation, retired): for each `## Round N` block from round 38 on, list which of those five the block carries (file:line). Report the round-42 block's gap verbatim and whether any other block has the same gap. Read %(fleet)s/AXES.md 'SCORECARD.md contract' for the field list." % {"lane": LANE, "fleet": FLEET}),
    ("RevC3Tool", "reviewer", ["operability"], "guard logic review",
     "Review %(lane)s/tools/staged-id-guard.py line by line: parse_rows (0-3-space pattern, malformed and duplicate refusals), document_key (URL then path-like head; the `[/.]` gate), analyse (collisions, held dedupe, naive map, cascade), validate_map (injective, registry clash, staged clash for partial maps, safe floor, coverage, self-map), and the selftest. Report each place the code and the docstring differ, and any refusal path that cannot fire. Do not edit it." % {"lane": LANE}),
    ("CritC3Maps", "critic", ["operability"], "adversarial adoption maps",
     "Build adversarial maps against %(lane)s/tools/staged-id-guard.py in /tmp/tameshi-r43-CritC3Maps-/: (1) a map that reuses a registry id for a DIFFERENT document, (2) a map that leaves one collision on itself, (3) a map covering every staged row (whole-set) with targets inside the staged range, (4) a map with duplicate targets, (5) a map whose target is below the safe floor. Run each through `--registry %(lane)s/corpus/SOURCES.md --staged %(staged)s --map <file> --json` and report verdict + reasons. Say for each whether refusal is CORRECT or a false refusal, with the CORPUS.md clause that decides it." % {"lane": LANE, "staged": STAGED}),
    ("MutC3Selftest", "mutation-tester", ["operability"], "guard selftest load-bearing",
     "Mutation-test the guard's selftest. In /tmp/tameshi-r43-MutC3Selftest-/ copy %(lane)s/tools/staged-id-guard.py and make three single edits, each alone: (M1) make ROW_RE column-zero (`^\\|`), (M2) drop the staged-clash reason, (M3) make document_key always return '' (no document). Run `--selftest` on each copy and report cases/failed/exit and which case caught it. A mutant the selftest does NOT catch must be reported as a selftest gap with the case that should have existed." % {"lane": LANE}),
    ("ScoutC3Package", "scout", ["operability"], "staged package documents",
     "Read %(staged)s (read-only) and classify its 103 rows: how many carry a URL/DOI, how many carry only a repo path, how many carry neither (these would be `unmapped`), how many documents are duplicates WITHIN the staged set, and how many documents the lane registry %(lane)s/corpus/SOURCES.md already holds (give the lane id). Report the counts and the exact ids for the neither-case and the within-set duplicates. Use grep/python, no writes outside /tmp." % {"staged": STAGED, "lane": LANE}),
    ("ExecC3Live", "executor", ["operability"], "live guard run",
     "Run `python3 -I %(lane)s/tools/staged-id-guard.py --registry %(lane)s/corpus/SOURCES.md --staged %(staged)s --json` and `--selftest`; report byte counts and sha256 of both input files at run time, the full JSON (collisions, held, unmapped, naive_map, cascade, safe_floor, verdict) and the selftest line. Then build the by-document safe map yourself in /tmp/tameshi-r43-ExecC3Live-/ (held rows -> their registry id; new documents -> ids at or above safe_floor), run it with --map, and report verdict + map_dedupe." % {"lane": LANE, "staged": STAGED}),
    ("RevC3Counter", "reviewer", ["operability"], "C3 counter independence",
     "Review %(lane)s/.ufo/evidence/round-43/guard/measure.py: is its own extraction independent of the tool it measures (separate parse, own dedupe), or does it reuse the tool's logic? Check the safe-map construction, the naive-map round trip, the control path, and whether tool_sha_ok can pass for a substitute. Report each weakness with file:line and a concrete scenario." % {"lane": LANE}),
    ("ScoutAssim", "scout", ["coverage"], "next assimilation theme",
     "Read /home/vgpnk/Projects/shokuknow/merge/tameshi/MERGE-REPORT.md (read-only) and list what the package stages by theme with counts, the entries still unadopted (round 42 adopted two, refused one, deferred one), and which theme the lane should take next with the reason. No adoption this round: the report's line is `Assimilation: none`. Do not run any campaign tool." % {}),
    ("ScoutQuarantine", "scout", ["coverage"], "quarantine slice re-derivation",
     "Re-derive this lane's slice of /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md (read-only; its header and summary totals are stale — derive the data rows yourself): awk -F'|' -v l='tameshi' '$2 ~ (\"`\" l \"`\") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}'. Report the row count, the ids, and the family of each (payload-absent vs could-not-be-fetched). No adoption; verdicts stay in the lane lesson." % {}),
    ("ScoutConsider", "scout", ["calibration"], "considerthese proposals",
     "Read every file in %(lane)s/considerthese/ (operator-authored input; mine, never edit). List each proposal with its status line, and name the ONE still-unimplemented proposal closest to this round's claims (survivor classification, record agreement, id registries) that could be landed as a lesson/QUALITY criterion. Quote its text and say what the lane already implements." % {"lane": LANE}),
    ("ScribeQuality", "scribe", ["calibration"], "QUALITY criteria draft",
     "Draft two criteria for %(lane)s/corpus/QUALITY.md in your report (do not edit the file): (83) a survivor is never relabelled equivalent without a differential probe and a structural argument, and a dead-code-only survivor is named as such; (84) a self-assessment counting command must use the census-valid pattern of the registry it counts. Each must carry a falsifier command that FAILS when the rule is broken, modelled on criteria 81/82 already in the file. Quote the two nearest existing criteria to match the numbering and shape." % {"lane": LANE}),
    ("ScribeLessonGate", "scribe", ["depth"], "lesson Gate draft",
     "Draft the `## Gate` block for %(lane)s/corpus/lessons/round-43.md in your report (do not write the lesson): one admit block per new source row (Stryker equivalent-mutants page, Wikipedia mutation testing) each carrying URL, access date 2026-10-25, byte count, sha256 and <=25-word located quotes with line numbers; one reject or deferral block for the staged package's equivalent-mutant material if any exists. Read %(lane)s/corpus/lessons/round-42.md '## Gate' for the shape and CORPUS.md rule 1 for the requirements." % {"lane": LANE}),
    ("ConnOverlap", "connector", ["adjacency"], "sibling overlap scan",
     "Scan the sibling lane repos under /home/vgpnk/Projects/shokunin (kumitate, kagi, kaidoku, chousa, kotodama, kake) for any existing tool that answers 'which staged/imported ids collide with a registry' or 'classify a mutant survivor'. Report paths, their scope, and whether this round's tools/staged-id-guard.py overlaps or duplicates one. Read-only; never write a sibling. If nothing overlaps, say which lanes you searched and the command." % {}),
    ("SentGuardIO", "sentinel", ["operability"], "guard input/output safety",
     "Security-review %(lane)s/tools/staged-id-guard.py: it reads a path outside the lane (%(staged)s). Check every write path (should be none), every subprocess, every eval/exec, path traversal in --map, JSON handling of an untrusted map file, and whether a hostile registry or staged file can make it write, hang or leak. Report each finding with file:line and severity, and the command you ran. Read-only." % {"lane": LANE, "staged": STAGED}),
    ("RevProvenance", "revenger", ["calibration"], "pin provenance",
     "Verify the freeze chain. For FREEZE=%s: `git -C %s show FREEZE:tools/staged-id-guard.py | sha256sum`, the same for tools/write-path-census-v4.py, and for the three counters, against contract.json's pins; then diff each counter's bytes at FREEZE against the working tree. Report each pair (pin, actual, agree) and any disagreement. Note that a counter whose running bytes differ from its own pin sets self_pin=0." % (FREEZE, LANE)),
    ("SentMutantIO", "sentinel", ["operability"], "counter write scope",
     "Audit where the three round-43 counters write. Read %(lane)s/.ufo/evidence/round-43/{mutants,calibration,guard}/measure.py, list every open(...,'w'), makedirs, subprocess and tempfile use with file:line, and state which paths can receive bytes outside /tmp. Then run the C2 counter with --selftest and confirm with `git -C %(lane)s status --porcelain` that nothing in the lane changed. Report the porcelain output verbatim." % {"lane": LANE}),
    ("ExecCommandD", "executor", ["depth"], "no-harm re-run",
     "Re-run the two canonical axis commands at BASE=%s and at FREEZE=%s and report both lines: command D (`git show REV:tools/mutate-and-run.sh | python3 -c '...regex...'` as printed in SCORECARD.md) and the round-21 coldread monitor (`python3 %s/.ufo/evidence/round-21/coldread/measure.py --rev REV`, report calibration_restraint_score and exit). Paste the exact commands. Read-only." % (BASE, FREEZE, LANE)),
    ("ExecCensus", "executor", ["calibration"], "sources census before",
     "Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` and report stdout, stderr, exit code and the row count it implies. Save the output to /tmp/tameshi-r43-ExecCensus-/census-start.stdout for the L1 to copy. Do not edit corpus/SOURCES.md." % {}),
    ("RevReportDraft", "reviewer", ["calibration"], "claim sentence = predicate",
     "Read claims.C1/C2/C3 in %(lane)s/.ufo/evidence/round-43/contract.json and each counter's docstring predicate. For each claim, say whether the contract sentence, the predicate sentence and the printed label are the SAME statement, and quote the three side by side. Flag any widening (a sentence that claims more than the counter tests) or narrowing. Also flag any universal quantifier ('all', 'every', 'no') whose set the counter does not enumerate." % {"lane": LANE}),
    ("ScribeRows", "scribe", ["depth"], "S159/S160 row draft",
     "Draft the two new corpus/SOURCES.md rows in your report (do not edit the registry): S159 Stryker equivalent-mutants docs and S160 Wikipedia mutation testing, both kind=docs, tier=A, status=mined, opened=2026-10-25, recheck=180d, used-by corpus/knowledge/r43-survivor-resolution-rule.md. Match the 11-column shape exactly (read the S155 row and the CORPUS.md row contract), keep every cell free of `|`, and state each row's `teaches` in one sentence grounded in a located quote from the source you opened. If you could not open a source, say which and why."),
]


def build(wave, report_dir, items):
    return {
        "wave": "round-43-%s" % wave,
        "reportDir": report_dir,
        "template": TEMPLATE,
        "context": COMMON,
        "items": [
            {"name": name, "role": role, "axes": axes, "milestone": milestone,
             "item": item_text}
            for name, role, axes, milestone, item_text in items
        ],
    }


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'w1'
    spec = build(which, '.ufo/waves/round-43/%s' % which, W1)
    path = os.path.join(LANE, '.ufo/waves/round-43/spec-%s.json' % which)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as handle:
        json.dump(spec, handle, indent=1)
    names = [item['name'] for item in spec['items']]
    print('items=%d unique=%d path=%s' % (len(names), len(set(names)), path))
