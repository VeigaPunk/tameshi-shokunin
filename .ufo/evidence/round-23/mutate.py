#!/usr/bin/env python3
"""Round23 bounded mutate/run/restore proof; only private copies are changed."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
from datetime import datetime, timezone

MUTANTS = [
    ('argv', "if receipt['argv'] != required['argv']:", 'if False:'),
    ('cwd', "if receipt['cwd'] != bundle['cwd']:", 'if False:'),
    ('revision', "if receipt['revision'] != bundle['revision']:", 'if False:'),
    ('membership', 'if set(receipts) != set(requirements):', 'if False:'),
    ('duplicate-command', "if row['name'] in receipts:", 'if False:'),
    ('exit', "if receipt['exit'] != required['expect']['exit']:", 'if False:'),
    ('stdout', "if any(token not in receipt['stdout'] for token in required['expect'].get('stdout_contains', [])):", 'if False:'),
    ('bool-exit', "or not revision(row.get('revision')) or type(row.get('exit')) is not int", "or not revision(row.get('revision')) or False"),
    ('snapshot-pin', "if digest != expected['bundle_sha256']:", 'if False:'),
    ('empty-requirements', "or not isinstance(bundle.get('requirements'), list) or not bundle['requirements']", "or not isinstance(bundle.get('requirements'), list)"),
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tool', type=Path, required=True)
    parser.add_argument('--revision', required=True)
    args = parser.parse_args()
    raw = args.tool.read_bytes()
    text = raw.decode()
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    def run(path):
        start = datetime.now(timezone.utc).isoformat()
        p = subprocess.run(['python3', str(path), '--selftest'], capture_output=True, text=True, env=env, timeout=90)
        return {'argv': p.args, 'exit': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr,
                'measurement_interval': {'start': start, 'end': datetime.now(timezone.utc).isoformat()}}
    with tempfile.TemporaryDirectory(prefix='tameshi-r23-mutants-') as tmp:
        path = Path(tmp) / 'tools/command-binding.py'
        path.parent.mkdir()
        fixtures = Path(tmp) / '.ufo/evidence/round-23/extra-cases.json'
        fixtures.parent.mkdir(parents=True)
        fixtures.write_bytes((args.tool.resolve().parents[1] / '.ufo/evidence/round-23/extra-cases.json').read_bytes())
        path.write_bytes(raw)
        control = run(path)
        rows = []
        for name, old, new in MUTANTS:
            count = text.count(old)
            if control['exit'] != 0 or count != 1:
                rows.append({'name': name, 'old': old, 'new': new, 'anchors': count, 'status': 'inconclusive'})
                continue
            path.write_text(text.replace(old, new, 1))
            result = run(path)
            result.update(name=name, old=old, new=new, anchors=count,
                          status='killed' if result['exit'] != 0 else 'survived')
            rows.append(result)
        path.write_bytes(raw)
        restored = run(path)
    result = {'revision': args.revision, 'tool_sha256': hashlib.sha256(raw).hexdigest(),
              'control': control, 'mutants': rows, 'restored': restored,
              'source_unchanged': args.tool.read_bytes() == raw,
              'killed': sum(r['status'] == 'killed' for r in rows),
              'survived': sum(r['status'] == 'survived' for r in rows),
              'inconclusive': sum(r['status'] == 'inconclusive' for r in rows)}
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if result['killed'] == len(MUTANTS) and restored['exit'] == 0 and result['source_unchanged'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
