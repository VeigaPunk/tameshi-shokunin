#!/usr/bin/env python3
"""Round-75 C2 discriminating controls (seat T75W1E2).

1. ECHO-STUB: a mutant that copies the doc's figure as its measurement must
   NOT reach unexpected=0 — not on the base doc and not on the landing doc —
   because the frozen span row expects stale. This shows the target count is
   not self-authenticating and the measured tokens are instrument-sourced.
2. ROW-DELETION: removing one declared capability row from the doc must be a
   setup refusal (capability-absent, exit 2), before any row effect, so the
   count cannot be lowered by deleting the row it measures.
3. DUPLICATE-ID: a manifest with two rows sharing an id must be refused.
4. Usage/setup refusals through the public CLI: no --repo, an unresolvable
   --doc-rev, an absent manifest, and a set-but-unusable TMPDIR.
"""
import ast
import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.join(HERE, 'tools', 'selfstate-freshness.py')
ECHO = os.path.join(HERE, 'tools', 'echo-mutant.py')
SIM = os.path.join(HERE, 'simulate-landing-tip.py')
REPO = '/home/vgpnk/Projects/shokunin/tameshi-shokunin'
REV = '21ef81e99966198cf8cdb2c6d8e56aa3c482da56'
MANIFEST = os.path.join(HERE, 'tools', 'selfstate-freshness.json')
failures = 0


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def verdict(name, ok, detail=''):
    global failures
    print('CONTROL_%s: %s%s' % (name, 'PASS' if ok else 'FAIL',
                                '' if ok else ' ' + detail))
    if not ok:
        failures += 1


cand = load(CAND, 'ssf_cand')
echo = load(ECHO, 'ssf_echo')
with open(MANIFEST, encoding='utf-8') as fh:
    rows = json.load(fh)['rows']
base_text = cand.GitReader(REPO).blob(REV, 'SCORECARD.md').decode('utf-8')

# Reuse the landing-tip simulation's repair table to build the repaired doc
# (the simulation driver itself executes on import, so its REPAIRS constant is
# read statically).
tree = ast.parse(open(SIM, encoding='utf-8').read())
REPAIRS = None
for node in ast.walk(tree):
    if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == 'REPAIRS' for t in node.targets):
        REPAIRS = ast.literal_eval(node.value)
if REPAIRS is None:
    raise SystemExit('could not read REPAIRS from the simulation driver')


def repaired_text():
    text = base_text
    for rid, cap, old, new in REPAIRS:
        line = cand.parse_capabilities(text)[cap]
        text = text.replace(line, line.replace(old, new), 1)
    return text


def summarize(mod, text, runner):
    buf = io.StringIO()
    rc = mod.run_measurement([dict(r) for r in rows], text.encode('utf-8'),
                             text, runner, out=buf,
                             err=io.StringIO())
    return rc, buf.getvalue()


with tempfile.TemporaryDirectory(prefix='ssf-controls-',
                                 dir=os.environ.get('TMPDIR') or None) as work:
    runner = cand.GitInstrumentRunner(REPO, work)
    # 1a. echo-stub on the base doc
    rc, txt = summarize(echo, base_text, runner)
    summary = [l for l in txt.splitlines() if l.startswith('SELFSTATE:')]
    verdict('ECHO_BASE', rc == 1
            and summary == ['SELFSTATE: rows=17 match=17 stale=0 unexpected=1'],
            'rc=%r %r' % (rc, summary))
    # 1b. echo-stub on the repaired landing doc
    rc, txt = summarize(echo, repaired_text(), runner)
    summary = [l for l in txt.splitlines() if l.startswith('SELFSTATE:')]
    verdict('ECHO_LANDING', rc == 1
            and summary == ['SELFSTATE: rows=17 match=17 stale=0 unexpected=1'],
            'rc=%r %r' % (rc, summary))
    # 2. row deletion from the doc -> capability-absent setup refusal, no rows
    tiny = base_text.replace(cand.parse_capabilities(base_text)['rekey-cost forecast'],
                             '', 1)
    buf, err = io.StringIO(), io.StringIO()
    rc = cand.run_measurement([dict(r) for r in rows], tiny.encode('utf-8'),
                              tiny, runner, out=buf, err=err)
    verdict('ROW_DELETION_REFUSED', rc == 2 and 'SELFSTATE:' not in buf.getvalue()
            and 'capability-absent' in err.getvalue(),
            'rc=%r %r %r' % (rc, buf.getvalue()[:120], err.getvalue()[:160]))
    # 3. duplicate id -> setup refusal
    dup = [dict(rows[0]), dict(rows[1])]
    dup[1]['id'] = dup[0]['id']
    buf, err = io.StringIO(), io.StringIO()
    rc = cand.run_measurement(dup, base_text.encode('utf-8'), base_text,
                              runner, out=buf, err=err)
    verdict('DUPLICATE_ID_REFUSED', rc == 2 and 'row-id-duplicate' in err.getvalue()
            and 'SELFSTATE:' not in buf.getvalue(),
            'rc=%r %r' % (rc, err.getvalue()[:160]))

# 4. public-CLI usage/setup refusals
def cli(*args, env=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    p = subprocess.run(['python3', '-I', '-X', 'utf8', CAND] + list(args),
                       cwd=REPO, capture_output=True, env=e)
    return p.returncode, p.stdout.decode('utf-8', 'replace'), \
        p.stderr.decode('utf-8', 'replace')

rc, out, err = cli('--manifest', MANIFEST, '--doc-rev', REV)
verdict('USAGE_NO_REPO', rc == 2 and 'SELFSTATE:' not in out
        and 'error=usage' in err, 'rc=%r %r' % (rc, err[:160]))
rc, out, err = cli('--repo', '.', '--manifest', MANIFEST, '--doc-rev', 'zzz')
verdict('BAD_DOC_REV_REFUSED', rc == 2 and 'SELFSTATE:' not in out
        and 'rev-unresolvable' in err, 'rc=%r %r' % (rc, err[:160]))
rc, out, err = cli('--repo', '.', '--manifest',
                   '/nonexistent/ssf-manifest.json', '--doc-rev', REV)
verdict('ABSENT_MANIFEST_REFUSED', rc == 2 and 'SELFSTATE:' not in out,
        'rc=%r %r' % (rc, err[:160]))
rc, out, err = cli('--repo', '.', '--manifest', MANIFEST, '--doc-rev', REV,
                   env={'TMPDIR': '/nonexistent-ssf-tmpdir'})
verdict('UNUSABLE_TMPDIR_REFUSED', rc == 2 and 'SELFSTATE:' not in out
        and 'error=setup' in err, 'rc=%r %r' % (rc, err[:160]))

print('CONTROL_SUMMARY: %s' % ('GREEN' if failures == 0 else 'RED'))
sys.exit(0 if failures == 0 else 1)
