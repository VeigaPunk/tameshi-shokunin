#!/usr/bin/env python3
"""Build the round-48 attempt-2 wave spec a2w1 (one v2 wave, 64 seats: the 32 falsify items attempt 1 prepared
in w2-items.py, patched where amendments 4-10 or the attempt-2 state changed their premise, plus the 32 items of
a2-items.py). Usage: CONTENT=<content sha> python3 build-spec-a2.py
Reuses build-spec.py (template, fill, ITEMS_W2) unchanged; never rewrites it."""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if not os.environ.get('CONTENT'):
    sys.exit('CONTENT must name the content revision')
spec = importlib.util.spec_from_file_location('build_spec_r48', os.path.join(HERE, 'build-spec.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

WAVE = 'a2w1'
m.W2D = m.LANE + '/.ufo/waves/round-48/' + WAVE
CONTENT = m.CONTENT
DECIDE = m.E + '/after'

PATCH = {
    'W2MutC1CounterA': [('attestation (observation file discovery under .ufo/evidence/round-48/calibration/observations/, PROFILES parsing, P0 extraction)',
                         'attestation (amendment 4: a member is attested only by a P0 or P1 tuple of the three rounds or by one of at most 6 EXTRA P0 observations of the same invocation; an EXTRA outside V is a mismatch; committed observation files never attest)')],
    'W2CritC1Rows': [('the committed observation receipts (@E@/calibration/observations/*.stdout, PROFILES lines) and the L1\'s emit receipt (@E@/calibration/emit-*.stdout if present)',
                      'the committed observation receipts (@E@/calibration/observations/*.stdout, PROFILES lines; evidence only, they never attest under amendment 4), the L1\'s emit receipt @E@/calibration/emit-15b1521.stdout and, once committed, the deciding receipt @E@/after/c1.stdout')],
    'W2CritC1Controls': [('CTL_A..E as committed at the counter freeze', 'CTL_A..E, scored by the attempt-2 L1 with the harness and counter bytes of the counter-freeze commit 755298415f8c; receipt @E@/control/c1-controls.stdout')],
    'W2RevC1Freeze': [('(5) the control receipts were taken at the freeze commit.', '(5) the control receipts (@E@/control/c1-controls.*, c2-controls.*) were scored with the harness and counter bytes of the freeze commit (sha256 in freeze-2.json `controls`) and before the deciding run (commit order).')],
    'W2ExecNoHarm': [('@LANE@/.ufo/evidence/round-47/deciding-run.sh line 62', '@E@/deciding-run.sh (the `COLDREAD_SECTIONS_CREDITED` line)')],
}

items = []
for n, r, a, ms, t in m.ITEMS_W2:
    for old, new in PATCH.get(n, []):
        if old not in t:
            sys.exit('patch anchor missing in %s: %r' % (n, old[:60]))
        t = t.replace(old, new)
    items.append((n, r, a, ms, t))
ns = {}
exec(open(os.path.join(HERE, 'a2-items.py'), encoding='utf-8').read(), ns)
items += ns['ITEMS_A2']

CONTEXT = """# Goal
tameshi round 48, attempt 2 (hyaku run 8; L1 TameshiR48a2). Attempt 1 (L1 TameshiR48) died in the orchestrator host crash of 2026-10-26 ~08:50 -03 before landing; its committed outputs are reused only where re-verified. Lane repo %(lane)s (verification-fixture craft: mutation testing, golden/fixture gates, flaky-test evidence). Base `%(base)s`. Claims, predicates, targets, kill rules and controls were pre-registered before any seat in %(e)s/contract.json (read it first, including all ten `amendments`; never edit it) and the counters were frozen at commit 755298415f8c (%(e)s/freeze-2.json).

Two declared claims (distinct axes):
- C1 calibration (lowest non-retired axis, 6): the standing SCORECARD.md self-assessment of the 22 frozen statements (%(e47)s/calibration/statements.json) is restated in section `### Standing self-assessment — re-stated at round 48` from R=3 observation rounds of the six profiles, with a `stable` / `nondeterministic` value class, values attested by the counter's own observation in the same invocation (amendment 4), the tool sha256 prefix and a deps set. Frozen counter %(e)s/calibration/measure.py; predicate label `C1_R48_PASS`.
- C2 freshness (sourced): held rows S026, S048, S093, S108 superseded by S265-S268 (opened 2026-10-26) with committed snapshots + fetch receipts (%(e)s/freshness/sources/), <=25-word `C2-QUOTE` Gate lines in %(lane)s/corpus/lessons/round-48.md carrying the required phrases, and the citing knowledge entries re-pointed. Frozen counter %(e)s/freshness/measure.py; label `C2_R48_PASS`.

CONTENT revision: `%(content)s` (the records). The L1 runs the single deciding invocation (%(e)s/deciding-run.sh, receipts under %(decide)s/, landed in a receipts-only commit) while this wave runs. You are NOT an author of what you attack. Run counters only as `--selftest`, `--only` / `--no-live` probes or against scratch trees, into scratch work dirs, and report output as observed; a probe is never a verdict. Every item names what it attacks; a finding names file:line and the command that shows it. Wave-1 reports (attempt 1) are under %(w1)s; earlier receipts under %(e)s.

Bounds for every seat: you are READ-ONLY on the lane checkout except your own report file and any deliverable file your item names (always inside %(w2)s). Every `Report:` trailer path is relative to %(lane)s — write it at %(lane)s/<that path>. Never edit %(fleet)s (the fleet repo), a sibling lane, the lane's jj state or Git index, and never write anything under %(lane)s/corpus, %(lane)s/tools or %(lane)s/SCORECARD.md (the deciding run checks that they stay clean). Never run git add/commit/stash/checkout/switch/reset/pull/push in the lane and never run a mutating jj command. Any fixture repo is created as `D=$(mktemp -d -p "$S") && git -C "$D" init -q`; every later git call names `-C "$D"`; verify `git -C "$D" rev-parse --show-toplevel` equals `$D` before the first commit; a throwaway identity is used only there. SCRATCH: every clone, work dir and temp file lives under %(scr)s/<YourSeatName>/ (`S=%(scr)s/<YourSeatName>; mkdir -p "$S"; export TMPDIR="$S"; trap 'rm -rf -- "$S"' EXIT`), never /tmp (files under 50 MB only, and only where your item says so); prefer `git clone -q --shared`; copy receipts you cite into your deliverable/report first, and delete your scratch dir before you finish (a tree left on disk is a defect you report). Check `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` before a heavy pass; on ENOSPC report the free space and stop. Never message agent://all.

Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first, official channels only, and record tool/version/channel/reason in your report. pacman guard: ALL pacman transactions are PAUSED host-wide (no -S, -Sy, -Syu, -U, -R, no downgrade, no service restart); install via uv tool / npx / an official binary in ~/.local/bin instead. Never pass a model; the route table decides.
""" % dict(lane=m.LANE, base=m.BASE, e=m.E, e47=m.E47, content=CONTENT, decide=DECIDE, w1=m.W1D, w2=m.W2D,
           fleet=m.FLEET, scr=m.SCR)

out = {
    'wave': 'round-48-' + WAVE,
    'reportDir': '.ufo/waves/round-48/' + WAVE,
    'template': m.TEMPLATE,
    'context': CONTEXT,
    'items': [{'name': m.P + n, 'role': r, 'axes': a, 'milestone': ms, 'item': m.fill(t)} for n, r, a, ms, t in items],
}
for it in out['items']:
    if '@' in it['item'] and any(tok in it['item'] for tok in ('@LANE@', '@E@', '@W2@', '@CONTENT@', '@BASE@', '@P@', '@SCR@')):
        sys.exit('unfilled placeholder in ' + it['name'])
path = os.path.join(HERE, 'spec-%s.json' % WAVE)
with open(path, 'w', encoding='utf-8') as fh:
    json.dump(out, fh, indent=2, ensure_ascii=False)
roles = {}
for it in out['items']:
    roles[it['role']] = roles.get(it['role'], 0) + 1
print('wrote %s with %d items %s' % (path, len(out['items']), json.dumps(roles, sort_keys=True)))
