#!/usr/bin/env python3
"""Prove the round-54 wrapper is value-transparent for the four tools.

Imports each tool module from a given clone, substitutes only the self-test
callable in the *harness's* namespace (the tool bytes are untouched), and calls
the real entry point. For stub returns 0/1/2 the entry point must return the same
value; for a raised ScratchRootUnusable the base tree must let it escape and the
C0 tree must map it to 2 with one naming line.

Usage: wrapper-probe.py CLONE_DIR
"""
import contextlib
import importlib.util
import io
import sys
from pathlib import Path

CLONE = Path(sys.argv[1])

TOOLS = (
    ('tools/env-diff.py', 'selftest', ['--selftest']),
    ('tools/bash-witness-study.py', 'cmd_selftest', ['selftest']),
    ('tools/evidence-disposition.py', 'selftest', ['--selftest']),
    ('tools/pin-disposition.py', 'selftest', ['--selftest']),
)


def load(path):
    name = 'probe_' + Path(path).stem.replace('-', '_')
    spec = importlib.util.spec_from_file_location(name, str(CLONE / path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def call(mod, attr, stub):
    setattr(mod, attr, stub)
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = mod.main(ARGV)
    return rc, out.getvalue() + err.getvalue()


print('TOOL\tSTUB\trc\tverdict')
fail = 0
for path, attr, argv in TOOLS:
    mod = load(path)
    ARGV = argv
    for value in (0, 1, 2):
        rc, text = call(mod, attr, (lambda v=value: (lambda *a, **k: v))())
        ok = rc == value and text == ''
        print('%s\treturns %d\t%s\t%s' % (path, value, rc, 'PASS' if ok else 'MISMATCH stderr=%r' % text[:120]))
        fail += (not ok)

    def raiser(exc_cls):
        def _(*a, **k):
            raise exc_cls('probe-value /no/such/tmpdir (could-not-evaluate)')
        return _

    try:
        rc, text = call(mod, attr, raiser(mod.ScratchRootUnusable))
        caught = True
    except BaseException as exc:  # uncaught at base: the wrapper does not exist there
        rc, text, caught = None, '%s: %s' % (type(exc).__name__, exc), False
    if caught:
        ok = rc == 2 and 'could-not-evaluate' in text and 'probe-value' in text and 'Traceback' not in text
    else:
        ok = rc is None
    print('%s\traises ScratchRootUnusable\t%s\tescaped=%s\t%s'
          % (path, rc, not caught, 'PASS' if ok else 'MISMATCH %r' % text[:160]))
    fail += (not ok)
print('WRAPPER_PROBE: %s' % ('ALL PASS' if fail == 0 else '%d mismatches' % fail))
sys.exit(0 if fail == 0 else 1)
