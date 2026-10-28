#!/usr/bin/env python3
"""Fixture: an eighth lane tool that allocates scratch through strict_scratch_root().

Byte-for-byte shape of the round-53 helper as it stood before round 54's C0 gave
the four unmapped callers a ScratchRootUnusable subclass caught at the entry
point: the helper raises a plain RuntimeError, and --selftest does not catch it,
so a set-but-unusable TMPDIR exits 1 with a traceback (the R53.6 residue).

Usage: scratch-consumer.py --selftest
"""
import sys
import tempfile


def strict_scratch_root():
    import os as _os
    t = _os.environ.get("TMPDIR")
    if t:
        if not _os.path.isdir(t) or not _os.access(t, _os.W_OK):
            raise RuntimeError(
                "cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: %r (could-not-evaluate)" % t)
        return t
    return tempfile.gettempdir()


def selftest():
    with tempfile.TemporaryDirectory(prefix="tameshi-fixture.", dir=strict_scratch_root()):
        print("scratch-consumer-selftest: ok")
    return 0


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        sys.exit(selftest())
    sys.exit(64)
