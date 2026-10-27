#!/bin/bash
# Round-53 crash-resume freeze integrity check (considerthese 2026-10-26 proposal 1).
# Usage: verify-freeze.sh LANE FREEZE
# Re-derives every sha256 recorded in .ufo/evidence/round-53/freeze.json from the
# bytes committed at FREEZE and prints FREEZE_INTEGRITY: OK or the first mismatch.
# A resumed L1 runs this before trusting a freeze; any re-freeze or post-seat
# amendment then shows up as a mismatch against the recorded manifest.
set -u
LANE=$1; FREEZE=$2
cd "$LANE" || exit 2
python3 - "$FREEZE" <<'PY'
import hashlib, json, subprocess, sys
freeze = sys.argv[1]
env = {k: v for k, v in __import__('os').environ.items() if not k.startswith('GIT_')}
fr = json.loads(subprocess.run(['git', 'show', '%s:.ufo/evidence/round-53/freeze.json' % freeze],
                               capture_output=True, text=True, env=env, check=True).stdout)
bad = []
for rel, want in sorted(fr['files'].items()):
    r = subprocess.run(['git', 'show', '%s:.ufo/evidence/round-53/%s' % (freeze, rel)],
                       capture_output=True, env=env)
    if r.returncode != 0:
        bad.append('%s unreadable' % rel); continue
    got = hashlib.sha256(r.stdout).hexdigest()
    if got != want:
        bad.append('%s sha256 %s != recorded %s' % (rel, got[:12], want[:12]))
amend = fr.get('amendments', [])
print('FREEZE %s files=%d amendments=%d' % (freeze[:12], len(fr['files']), len(amend)))
for a in amend:
    print('AMENDMENT %s %s' % (a['n'], a['what'][:90]))
if bad:
    print('FREEZE_INTEGRITY: MISMATCH')
    for b in bad: print('MISMATCH', b)
    sys.exit(1)
print('FREEZE_INTEGRITY: OK')
PY
