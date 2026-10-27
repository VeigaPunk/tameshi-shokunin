#!/usr/bin/env python3
"""Build a synthetic kept-regression workdir for tools/mte-interop.py --check --workdir,
so the gate's PASS (0) and FAIL (1) paths can be exercised without the live fleet.

Reads the runner's committed TABLE_* literals (the same source the tool reads) to derive
each leg's defect ids and recorded verdicts, then materialises, per leg:
  pristine.target.t.py, spec.copy, results.tsv
and one regression.stdout with the REGRESSION_TABLE lines the tool parses.
"""
import os, re, shutil, sys

LANE = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
REV = sys.argv[1]
OUT = sys.argv[2]
MODE = sys.argv[3] if len(sys.argv) > 3 else 'clean'   # clean | flip

LEG_TABLE = {'js-kimi-census': 'TABLE_JS', 'bash-surface-census': 'TABLE_BASH',
             'bash-tsukuroi-census': 'TABLE_TSUKUROI', 'bash-mado-verify': 'TABLE_MADO',
             'bash-checklist-run': 'TABLE_CHECKLIST', 'js-claims-check': 'TABLE_CLAIMS',
             'js-round-gate': 'TABLE_ROUNDGATE', 'js-sources-check': 'TABLE_SOURCESCHECK',
             'js-cite-check': 'TABLE_CITECHECK', 'bash-drift-pins': 'TABLE_DRIFTPINS'}

runner = subprocess_run = None
import subprocess
runner = subprocess.run(['git', '-C', LANE, 'show', '%s:tools/mutate-and-run.sh' % REV],
                        capture_output=True, text=True, check=True).stdout
tables = dict(re.findall(r"^(TABLE_\w+)='([^']*)'", runner, re.M))

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)
stdout_lines = []
for leg, var in sorted(LEG_TABLE.items()):
    pairs = [p.split(':', 1) for p in tables[var].split(',')]
    d = os.path.join(OUT, leg)
    os.makedirs(d)
    src_lines = []
    spec = []
    for ident, verdict in pairs:
        tok = 'TOKEN_%s_%s' % (leg.replace('-', '_').upper(), ident.replace('-', '_'))
        src_lines.append('%s = 1  # %s' % (tok, ident))
        spec.append('@defect %s | synthetic %s\n@old %s = 1\n@new %s = 2\n' % (ident, ident, tok, tok))
    open(os.path.join(d, 'pristine.target.t.py'), 'w').write('\n'.join(src_lines) + '\n')
    open(os.path.join(d, 'spec.copy'), 'w').write('\n'.join(spec))
    verdicts = dict(pairs)
    if MODE == 'flip':
        first = pairs[0][0]
        verdicts[first] = 'SURVIVED' if verdicts[first] == 'KILLED' else 'KILLED'
    rows = ['id\tverdict\texit\tduration-ms\tmutant-sha256\tdesc']
    for ident, verdict in pairs:
        rows.append('%s\t%s\t1\t1\tx\t%s' % (ident, verdicts[first] if MODE == 'flip' and ident == first else verdict, ident))
    open(os.path.join(d, 'results.tsv'), 'w').write('\n'.join(rows) + '\n')
    killed = sum(1 for v in verdicts.values() if v == 'KILLED')
    survived = sum(1 for v in verdicts.values() if v == 'SURVIVED')
    inc = sum(1 for v in verdicts.values() if v == 'INCONCLUSIVE')
    stdout_lines.append('REGRESSION_TABLE %s: match=%d/%d recorded-killed=%d measured-killed=%d survived=%d inconclusive=%d flips=0'
                        % (leg, len(pairs), len(pairs), killed, killed, survived, inc))
open(os.path.join(OUT, 'regression.stdout'), 'w').write('\n'.join(stdout_lines) + '\n')
print('built %s mode=%s legs=%d' % (OUT, MODE, len(LEG_TABLE)))
