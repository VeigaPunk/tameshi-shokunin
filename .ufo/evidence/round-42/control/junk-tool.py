import importlib.util, json, sys
spec = importlib.util.spec_from_file_location('v3', '/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/write-path-census-v3.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
if '--selftest' in sys.argv: sys.exit(0)
src = open(sys.argv[sys.argv.index('--file') + 1], encoding='utf-8', errors='replace').read()
sites = [{'lineno': r['lineno'], 'kind': r['kind'], 'expected': bool(r['expected']), 'scratch': bool(r['scratch']),
          'explicit_out': False, 'unflagged': False, 'resolved': r['resolved']} for r in mod.classify_source(src)]
print(json.dumps({'sites': sites}))
