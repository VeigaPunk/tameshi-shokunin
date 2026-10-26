#!/usr/bin/env python3
"""Build the round-49 wave-2 spec (v1 band 32-64): falsify what wave 1 and the L1 integration produced, against
the candidate content revision. Usage: CAND=<sha> python3 build-spec-w2.py"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('w1spec', os.path.join(HERE, 'build-spec.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
CAND = os.environ.get('CAND') or sys.exit('CAND must name the candidate content revision')
W2 = m.LANE + '/.ufo/waves/round-49/w2'
READS = m.E + '/c1/reads.json'

CONTEXT = m.CONTEXT.replace(m.W1, W2) + """
# Wave 2 (falsify)
Wave 1 (reports and deliverables under %(w1)s) built the round's artifacts; the L1 integrated them into the candidate content revision `%(cand)s`: corrected SKILL.md sections, %(reads)s (one row per pointer, with the seat that read it), the re-key ledger entries (%(e)s/coldread/), tools/pbt-staged-id.py, the new SOURCES rows, corpus/knowledge/pbt-generator-pilot.md, the README F10 line, the lesson corpus/lessons/round-49.md, QUALITY, SCORECARD and LOG. Read everything at `%(cand)s` (`git -C %(lane)s show %(cand)s:<path>`; a scratch clone checked out at it for runs). The deciding run is the L1's and happens once, after this wave; nothing you run is a verdict. You did not author what you attack. Every finding names what it attacks, file:line, the command and its observed output. Deliverables go in %(w2)s.
""" % dict(w1=m.W1, cand=CAND, reads=READS, e=m.E, lane=m.LANE, w2=W2)


def fill(t):
    return m.fill(t).replace(m.W1 + '/@', W2 + '/@').replace('@W2@', W2).replace('@CAND@', CAND).replace('@READS@', READS)


REREAD = """Re-read C1 rows, section `{sec}`, ordinals {lo}-{hi} at the candidate `@CAND@`: for each row of @READS@ in that range, open the SKILL.md clause at `@CAND@` and the pointed target at `@CAND@`, and judge whether the row's excerpt really supports the clause (the counter only checks that the excerpt is there). Also judge every correction the L1 made in that range (`git -C @LANE@ diff @BASE@ @CAND@ -- SKILL.md`): is the new pointer right, did the sentence change meaning. Deliverable @W2@/@P@W2Reread{nn}.json {{"rows": [{{"ordinal", "raw", "supports": true|false, "why"}}], "corrections": [{{"skill_line", "ok": true|false, "why"}}]}}. Report every row that does not support its clause."""

RR = [('## Mutation-sweep recipe', 0, 8), ('## Mutation-sweep recipe', 9, 17), ('## Mutation-sweep recipe', 18, 26),
      ('## Mutation-sweep recipe', 27, 40), ('## Restore discipline', 0, 12), ('### The map', 0, 8), ('### The map', 9, 20),
      ('## Promotion-evidence calibration', 0, 10), ('## Repeated controls and gate registry', 0, 10),
      ('## Pin disposition and provenance correction', 0, 12), ('## Effective expectation reconciliation', 0, 12)]

ITEMS = []
for i, (sec, lo, hi) in enumerate(RR, 1):
    ITEMS.append(('W2Reread%02d' % i, 'critic' if i % 2 else 'reviewer', ['calibration'], 'C1 semantic re-read',
                  REREAD.format(sec=sec, lo=lo, hi=hi, nn='%02d' % i)))

ITEMS += [
    ('W2ExecC1Probe', 'executor', ['calibration'], 'C1 counter probe at candidate',
     "Run the frozen C1 counter as a probe at the candidate into an empty scratch work dir: `python3 @E@/c1/measure.py --lane @LANE@ --rev @CAND@ --work \"$S/w\"` (minutes). Copy stdout to @W2@/@P@W2ExecC1Probe.stdout. Report the C1_R49 line and every PTR line that is not `ok`, and the UNCOVERED_* lines. A probe is not the deciding run."),
    ('W2ExecC2Probe', 'executor', ['coverage'], 'C2 generator probe',
     "Exercise tools/pbt-staged-id.py at the candidate (scratch clone at @CAND@): `--selftest`; seed 4949 with 400 cases against the pristine guard (time it; class table); seeds 1..5 with 400 cases each (does any seed find a pristine violation? a real one is a guard finding, an oracle bug is a generator finding); a run with --cases 0 and 1. Do not read /home/vgpnk/.local/state/. Deliverable @W2@/@P@W2ExecC2Probe.md with commands, exits, last lines and timings."),
    ('W2MutGenerator', 'mutation-tester', ['coverage'], 'generator mutation',
     "Mutation-test the generator's ORACLE, not the guard: copy tools/pbt-staged-id.py at @CAND@ into scratch and write 10+ single-edit mutants of its oracle and class logic (census regex, numeric sort, held normalization, naive map, cascade, map rules, refusal predictions). A good oracle mutant makes the generator report a false violation on the PRISTINE guard. Report which oracle mutants survive (the generator still prints violations=0 on the pristine guard, seed 4949, 400 cases) — each survivor is an oracle rule no generated case exercises. Deliverable @W2@/@P@W2MutGenerator.md."),
    ('W2MutGuardOwn', 'mutation-tester', ['coverage'], 'independent guard mutants',
     "Independent of the hidden panel (never read /home/vgpnk/.local/state/ or the c2-WITNESS/c2-CTL_FIX receipts): write 12 NEW single-edit mutants of tools/staged-id-guard.py yourself (scratch copies; the lane file is never edited), avoiding trivially equivalent ones, and run the candidate's generator (seed 4949, 400 cases) against each. For each kill, re-run the counterexample on the pristine and the mutant guard and confirm the outputs differ. Deliverable @W2@/@P@W2MutGuardOwn.md: kill table, confirmed kills, survivors with a hand-made input that distinguishes each (or an equivalence argument)."),
    ('W2ExecGenTrace', 'executor', ['coverage'], 'generator access trace',
     "Show from outside the counter that tools/pbt-staged-id.py at @CAND@ is property-based, not differential (wave-1 finding @W1@/@P@CritC2Contract.md F1: during a counter mutant run the generator's cwd also holds the pristine guard). In a scratch clone at @CAND@: (1) put a mutant copy of tools/staged-id-guard.py (your own single edit, never from /home/vgpnk/.local/state/) in \"$S/m/\" next to an untouched pristine copy, cd into the pristine copy's directory, and run the generator under `strace -f -e trace=openat,open,execve -o \"$S/trace\" python3 -I tools/pbt-staged-id.py --guard \"$S/m/staged-id-guard.py\" --seed 4949 --cases 400 --dump \"$S/d.jsonl\"`; list every file it opened or executed outside the Python install and its TMPDIR — any open of the pristine guard is a HIGH finding; (2) run the pristine-guard leg once with cwd = the guard's directory and once with cwd = an empty dir and cmp the two dumps (must be identical). Deliverable @W2@/@P@W2ExecGenTrace.md with the filtered open list and both checks."),
    ('W2CritGenOracle', 'critic', ['coverage'], 'generator independence',
     "Attack the generator's independence and honesty at @CAND@: does tools/pbt-staged-id.py import, exec, copy or regex-scrape the guard's code (it must use only the CLI); does it special-case the guard's bytes, sha or path; does it read anything outside its TMPDIR and its arguments; is the oracle a re-implementation that shares the guard's bugs (compare rule by rule with the guard's docstrings, not its code); is the distribution honest (QuickCheck: observe what you generate) or padded to meet class floors. Deliverable @W2@/@P@W2CritGenOracle.md with severity per finding."),
    ('W2RevGenCode', 'reviewer', ['coverage'], 'generator code review',
     "Code review of tools/pbt-staged-id.py at @CAND@: interface conformance with @E@/contract.json claims.C2.generator_interface (flags, dump format, last line, exits), determinism (same seed -> byte-identical dump: run twice and cmp), temp-file hygiene (TMPDIR only, cleanup), timeouts on guard calls, error paths (guard missing, unreadable, hangs), stdlib only. Deliverable @W2@/@P@W2RevGenCode.md."),
    ('W2RevRows', 'reviewer', ['coverage'], 'SOURCES rows re-open',
     "Re-open each SOURCES row the round appended (diff `git -C @LANE@ diff @BASE@ @CAND@ -- corpus/SOURCES.md`): fetch each URL today, compare with the committed snapshot and receipt under @W1@ / the evidence dir, locate each Gate quote (<= 25 words) in the lesson `## Gate` of corpus/lessons/round-49.md in the live bytes and in the snapshot, check tier, status, opened, recheck cell, used-by (exactly the admitted entries citing the row) and the 11-column schema. Run `@FLEET@/scripts/sources-census.sh validate --root @FLEET@ tameshi` is not allowed at a candidate (it reads the live tree) — instead validate a scratch mirror: `git -C @LANE@ archive @CAND@ corpus | tar -x -C \"$S/v\"` then `@FLEET@/scripts/sources-census.sh validate --file \"$S/v/corpus/SOURCES.md\"`. Deliverable @W2@/@P@W2RevRows.md."),
    ('W2CritEntry', 'critic', ['coverage'], 'pilot entry attack',
     "Attack corpus/knowledge/pbt-generator-pilot.md at @CAND@ against corpus/QUALITY.md (every applicable criterion) and its sources: does every sentence about QuickCheck/Smallbone match a located passage; are measured numbers marked as pending the deciding receipt rather than asserted; does it overclaim (F10 'held' from one generator against one lane-owned gate; no shrinking; panel size 12); is the `source:` header in the lane's shape. Deliverable @W2@/@P@W2CritEntry.md."),
    ('W2CritAssim', 'critic', ['coverage', 'adjacency'], 'assimilation decisions',
     "Attack the round's assimilation decisions at @CAND@ (lesson corpus/lessons/round-49.md `## Gate`; wave-1 triage reports @W1@/@P@ScribePkg*.md; package @PKG@ read-only): is each admit re-grounded (own access date, own located quote, CORPUS rule 1), each reject's decisive reason the right one (QUALITY 94), the id renumbering by document, used-by exact, no row appended that no admitted entry cites (CORPUS rule 4). Deliverable @W2@/@P@W2CritAssim.md."),
    ('W2CritC1Claim', 'critic', ['calibration'], 'C1 claim attack',
     "Attack C1 as a claim at @CAND@: (1) run the cold-read monitor `python3 @LANE@/.ufo/evidence/round-21/coldread/measure.py --repo @LANE@ --rev @CAND@` and report credited/score; (2) inspect the seven new ledger entries in .ufo/evidence/round-21/coldread/ledger.json at @CAND@ and their traces (@E@/coldread/traces/ at @CAND@): do the inputs exclude the five record files, are the traces real tools/trace-inputs.py receipts, do the seats named actually appear in @READS@; (3) is the score move 6 -> 8 earned under SHONEN/PROTOCOL rules (box 3 `[~]` with ledger link) or a monitor artifact; (4) does any SKILL.md edit outside the seven sections exist (`git diff @BASE@ @CAND@ -- SKILL.md`). Deliverable @W2@/@P@W2CritC1Claim.md."),
    ('W2ExecDurability', 'executor', ['calibration'], 'durability probe',
     "Independently of the counter, test C1's durability at @CAND@ in a scratch clone: commit (inside the clone only, throwaway identity, after verifying its toplevel) one appended line to each of LOG.md, SCORECARD.md, corpus/SOURCES.md, corpus/QUALITY.md, corpus/README.md, then separately an edit to one cited knowledge note of the recipe section (e.g. corpus/knowledge/mutation-case-kimi-census.md), and run the monitor (`python3 .ufo/evidence/round-21/coldread/measure.py --repo \"$S/lane\" --rev HEAD`) after each. Expected: records do not lapse any section; a cited-note edit lapses exactly the sections citing it. Deliverable @W2@/@P@W2ExecDurability.md with credited counts and lapsed headings per case."),
    ('W2ExecPrecheck', 'executor', ['calibration'], 'QUALITY 98 precheck',
     "Run QUALITY criterion 98's precheck on the candidate: `bash @LANE@/.ufo/evidence/round-48/quality/coldread-precheck.sh @LANE@ @BASE@ @CAND@` and the round-49 no-harm monitors `bash @E@/no-harm.sh @LANE@ @CAND@`. Copy both outputs to @W2@/@P@W2ExecPrecheck.*.stdout and report every RED line."),
    ('W2ExecMistake', 'executor', ['calibration'], 'mistake fix re-run',
     "Re-run the able-to-fail demonstration of deciding-run.sh gate 0 independently of wave 1 (@W1@/@P@ExecMistakeGate.md is the first one; do not copy its commands blindly): in a scratch clone at @CAND@, show (a) a missing control receipt refuses with exit 3 before any counter starts, (b) a pre-existing c1.start refuses, and (c) with all receipts present and an empty out dir gate 0 passes — then kill the run as soon as `FROZEN_UNCHANGED` prints (never let a counter finish; it is not a deciding run). Deliverable @W2@/@P@W2ExecMistake.md."),
    ('W2RevLesson', 'reviewer', ['calibration'], 'lesson review',
     "Review corpus/lessons/round-49.md at @CAND@: `## Gate` (every new row: URL, access date, <= 25-word located quote; >= 1 admit and >= 1 reject from the assimilation set; status/recheck/used-by changes logged old -> new), `## Mistakes` (class · evidence pointer · captured-by · fix · able-to-fail shown), the considerthese section (cites considerthese/2026-10-26.md + date, grounded through the lane's bar), and every evidence pointer resolving at @CAND@ (run `python3 @LANE@/.ufo/evidence/round-48/quality/pointer-check.py` per its usage line if it applies). Deliverable @W2@/@P@W2RevLesson.md."),
    ('W2RevQuality', 'reviewer', ['calibration'], 'QUALITY review',
     "Review the round's corpus/QUALITY.md additions at @CAND@ (`git diff @BASE@ @CAND@ -- corpus/QUALITY.md`): each new criterion cites its lesson, is not a duplicate of criteria 1-98 (grep), and carries a falsifier that can fail. Deliverable @W2@/@P@W2RevQuality.md."),
    ('W2RevScorecard', 'reviewer', ['calibration'], 'SCORECARD/LOG review',
     "Review the round's SCORECARD.md and LOG.md additions at @CAND@ (append-only? `git diff @BASE@ @CAND@ --numstat -- SCORECARD.md LOG.md` must show 0 deletions): every pointer resolves, every number matches a committed receipt, no after-value is asserted before the deciding run, the capability row (if any) is conditioned on the deciding receipt. Deliverable @W2@/@P@W2RevScorecard.md."),
    ('W2CritReadme', 'critic', ['coverage'], 'frontier move attack',
     "Attack the F10 frontier move at @CAND@: corpus/README.md's F10 line(s) and coverage-map row(s); is `held (round 49)` justified under the README's own rule (a ground reads held only when its next move is measured; and only through an admitted knowledge entry with a `source:` header citing a mined row); is the move conditioned on the deciding receipt; does it contradict PROVINCE.md. Deliverable @W2@/@P@W2CritReadme.md."),
    ('W2SentinelScope', 'sentinel', ['calibration', 'coverage'], 'scope and safety',
     "Scope and safety review of @CAND@ vs @BASE@: `git diff --name-status @BASE@ @CAND@` — every changed path is inside the lane's write scope, tools/ only adds tools/pbt-staged-id.py, no pinned tool changed (sha256 vs .ufo/evidence/round-49/freeze.json for staged-id-guard.py), no file > 1 MiB added outside evidence, no secret-looking content in snapshots or receipts, no /tmp path cited as evidence. Deliverable @W2@/@P@W2SentinelScope.md."),
    ('W2ScoutMisroot', 'scout', ['adjacency'], 'misroot sweep',
     "Misroot pre-sweep: `git -C @FLEET@ status --porcelain` (read-only). List every untracked or modified path, and for each say whether its content names tameshi round 49 (a wave-1 seat wrote it at the fleet root by mistake) — read the file, never move or delete it (the L1 does). Deliverable @W2@/@P@W2ScoutMisroot.md."),
    ('W2ConnPatterns', 'connector', ['calibration', 'coverage'], 'cross-wave patterns',
     "Cross-wave pattern finder: read every wave-1 report under @W1@ and the integration diff (`git diff @BASE@ @CAND@ --stat`). Find findings that were raised and not integrated, contradictions between seats, and recurring defect classes (compare with corpus/lessons/round-4*-verifier-spotcheck.md). Deliverable @W2@/@P@W2ConnPatterns.md: a table finding -> raised by -> integrated? -> where."),
    ('W2ConnSeparable', 'connector', ['calibration', 'coverage'], 'causal separability',
     "Check causal separability at @CAND@: list every path C1's evidence depends on and every path C2's depends on (contract + counters + integration diff); show that reverting C2's paths (generator, rows, entry, README F10 line) leaves C1's counter inputs byte-identical, and vice versa, by building both reverted trees in scratch (git archive + file restores) and comparing hashes of each counter's inputs. Deliverable @W2@/@P@W2ConnSeparable.md."),
]


def main():
    out = {'wave': 'round-49-w2', 'reportDir': '.ufo/waves/round-49/w2', 'template': m.TEMPLATE, 'context': CONTEXT,
           'items': [{'name': m.P + n, 'role': r, 'axes': a, 'milestone': ms, 'item': fill(t)} for n, r, a, ms, t in ITEMS]}
    for it in out['items']:
        if any(tok in it['item'] for tok in ('@LANE@', '@E@', '@W1@', '@W2@', '@SCR@', '@BASE@', '@CAND@', '@P@', '@PKG@',
                                             '@FLEET@', '@READS@')):
            raise SystemExit('unfilled placeholder in ' + it['name'])
    path = os.path.join(HERE, 'spec-w2.json')
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    roles = {}
    for it in out['items']:
        roles[it['role']] = roles.get(it['role'], 0) + 1
    print('wrote %s with %d items %s' % (path, len(out['items']), json.dumps(roles, sort_keys=True)))


if __name__ == '__main__':
    main()
