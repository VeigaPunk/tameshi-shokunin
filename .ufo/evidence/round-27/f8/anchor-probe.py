#!/usr/bin/env python3
"""Round 27, frontier F8: judge four cite-check survivors against expectations
anchored outside the code under mutation, not against the pristine binary.

Usage: anchor-probe.py --kumitate DIR --anchors FILE --out RECEIPT.json

For each survivor in FILE (anchors.json) it materializes the pinned blob
`git -C DIR show <rev>:<path>`, checks the blob sha256, applies the survivor's
exact @old -> @new edit (exactly one occurrence), builds the survivor's witness
tree in a fresh temp dir, and runs pristine and mutant under `env -i`. The
oracle is the survivor's `expect` record (exit status and, when named, one
finding kind), which anchors.json derives from the gate's header contract and
from outside sources, never from a run of either binary. A survivor is an
`anchored-hole` when the pristine meets the anchored expectation and the mutant
does not; `anchor-disagrees-with-pristine` when the pristine itself misses it.
Exit 0 when every survivor ran; 1 when any did not; 2 on usage.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def sha(b):
    return hashlib.sha256(b).hexdigest()


def build_tree(root, witness):
    src, selfd, fleet = root / 'src', root / 'self', root / 'fleet'
    for d in (src / 'scripts', selfd / 'corpus' / 'knowledge', fleet):
        d.mkdir(parents=True, exist_ok=True)
    kind = witness['kind']
    argv = ['--src', str(src), '--self', str(selfd), '--fleet', str(fleet), '--json']
    facts = {}
    if kind == 'line-past-end':
        n = witness['lines']
        text = ''.join('// line %d\n' % i for i in range(1, n + 1))
        (src / 'scripts' / 'real.mjs').write_text(text)
        facts['newline_count'] = text.count('\n')
        (selfd / 'SKILL.md').write_text('# probe doc\n\nEdge citation: `scripts/real.mjs:%d`.\n' % (n + 1))
    elif kind == 'one-orphan-ref-strict':
        (src / 'scripts' / 'real.mjs').write_text('export const x = 1;\n')
        (selfd / 'SKILL.md').write_text('# doc\n\nSee `scripts/real.mjs`.\n')
        (selfd / 'corpus' / 'knowledge' / 'orphan-1.md').write_text(
            '# orphan 1\n\nA lone ref (:424242) with no path token anywhere above it.\n')
        argv.append('--strict')
    elif kind == 'unknown-flag':
        (src / 'scripts' / 'real.mjs').write_text('export const x = 1;\n')
        (selfd / 'SKILL.md').write_text('# doc\n\nSee `scripts/real.mjs`.\n')
        argv.append('--no-such-flag-r27')
    elif kind == 'interior-pin':
        body = b'// target file for the interior-pin witness\nexport const A = 1;\n'
        (src / 'scripts' / 'target.mjs').write_bytes(body)
        digest = sha(body)
        hexpin = digest[8:20]
        facts.update(digest=digest, pin=hexpin, pin_is_leading_substring=digest.startswith(hexpin),
                     pin_inside_digest=hexpin in digest)
        (selfd / 'SKILL.md').write_text('# doc\n\nThe cited file is `scripts/target.mjs`; its content pin is sha256 `%s`.\n' % hexpin)
    else:
        raise SystemExit('unknown witness kind %r' % kind)
    return argv, facts


def run(node, tool, argv, home):
    env = {'PATH': os.path.dirname(node) + ':/usr/bin:/bin', 'HOME': str(home), 'LANG': 'C', 'TZ': 'UTC'}
    p = subprocess.run([node, str(tool), *argv], env=env, capture_output=True, timeout=120)
    kinds = []
    try:
        doc = json.loads(p.stdout)
        kinds = sorted({f['kind'] for f in (x for fl in doc.get('files', []) for x in fl.get('findings', []))
                        if f.get('severity') in ('error', 'warn')})
    except (ValueError, TypeError):
        doc = None
    return {'exit': p.returncode, 'error_warn_kinds': kinds, 'json': doc is not None,
            'stdout_sha256': sha(p.stdout), 'stderr_head': p.stderr.decode('utf-8', 'replace')[:160]}


def meets(obs, expect):
    if obs['exit'] != expect['exit']:
        return False
    k = expect.get('kind')
    return k is None or k in obs['error_warn_kinds']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--kumitate', required=True)
    ap.add_argument('--anchors', required=True)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    node = shutil.which('node')
    if not node:
        print('ANCHOR_PROBE: node not found', file=sys.stderr)
        return 2
    spec = json.loads(Path(a.anchors).read_text())
    blob = subprocess.run(['git', '-C', a.kumitate, 'show', '%s:%s' % (spec['rev'], spec['path'])],
                          capture_output=True, check=True).stdout
    if sha(blob) != spec['blob_sha256']:
        print('ANCHOR_PROBE: pinned blob sha256 mismatch', file=sys.stderr)
        return 1
    text = blob.decode('utf-8')
    results, ran = [], 0
    with tempfile.TemporaryDirectory(prefix='tameshi-r27-anchor-') as tmp:
        tmp = Path(tmp)
        pristine = tmp / 'pristine.mjs'
        pristine.write_bytes(blob)
        for s in spec['survivors']:
            r = {'id': s['id']}
            if text.count(s['old']) != 1:
                r['error'] = '@old occurs %d times' % text.count(s['old'])
                results.append(r)
                continue
            mutant = tmp / ('mutant-%s.mjs' % s['id'])
            mutant.write_text(text.replace(s['old'], s['new']))
            root = tmp / s['id']
            argv, facts = build_tree(root, s['witness'])
            home = root / 'home'
            home.mkdir()
            r['witness_facts'] = facts
            r['expect'] = s['expect']
            r['pristine'] = run(node, pristine, argv, home)
            r['mutant'] = run(node, mutant, argv, home)
            r['pristine_meets_anchor'] = meets(r['pristine'], s['expect'])
            r['mutant_meets_anchor'] = meets(r['mutant'], s['expect'])
            if r['pristine_meets_anchor'] and not r['mutant_meets_anchor']:
                r['class'] = 'anchored-hole'
            elif not r['pristine_meets_anchor']:
                r['class'] = 'anchor-disagrees-with-pristine'
            else:
                r['class'] = 'mutant-meets-anchor'
            ran += 1
            results.append(r)
    receipt = {
        'schema': 'tameshi-f8-anchor-receipt-v1',
        'probe_sha256': sha(Path(__file__).read_bytes()),
        'anchors_sha256': sha(Path(a.anchors).read_bytes()),
        'node': subprocess.run([node, '--version'], capture_output=True, text=True).stdout.strip(),
        'target': {'repo': 'kumitate-shokunin', 'rev': spec['rev'], 'path': spec['path'], 'blob_sha256': sha(blob)},
        'results': results,
    }
    Path(a.out).write_text(json.dumps(receipt, indent=1) + '\n')
    for r in results:
        print('ANCHOR %s: %s pristine=%s mutant=%s' % (r['id'], r.get('class', r.get('error')),
                                                       r.get('pristine', {}).get('exit'), r.get('mutant', {}).get('exit')))
    ok = ran == len(spec['survivors'])
    print('ANCHOR_PROBE: ran=%d/%d anchored_holes=%d' % (ran, len(spec['survivors']),
                                                        sum(r.get('class') == 'anchored-hole' for r in results)))
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
