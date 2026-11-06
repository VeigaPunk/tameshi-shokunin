#!/usr/bin/env python3
"""Cheap probe: replay the frozen prereg spec against candidate gate blobs with the
counter's own parser/suite/oracle (imported from the frozen measure.py, read-only)."""
import hashlib
import importlib.util
import os
import subprocess
import sys
import tempfile
from pathlib import Path

MEASURE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-88/measure.py"
SPEC = Path("/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-88/c1/py-kake-ledger-guard.defects.spec")
KAKE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
TABLE = ("K_CUT_WHOLE:KILLED,K_STARTSWITH:KILLED,K_FILES_EQ:KILLED,K_GLOB:KILLED,"
         "K_SHOW_RC:KILLED,S_HEAD_SHORT:SURVIVED,S_OFFSET_EQ:SURVIVED,S_OK_ALL:SURVIVED,"
         "S_VACUOUS:SURVIVED,S_RED_FILES:SURVIVED")
SUITE = ('h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i '
         'PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 '
         'GIT_CEILING_DIRECTORIES="$h" python3 -I "$MUTANT" --selftest')

spec_mod = importlib.util.spec_from_file_location("measure", MEASURE)
m = importlib.util.module_from_spec(spec_mod)
spec_mod.loader.exec_module(m)

spec_text = SPEC.read_text()
print("spec sha", hashlib.sha256(spec_text.encode()).hexdigest())
defects = m.parse_spec(spec_text)
table = dict(p.split(":", 1) for p in TABLE.split(","))


def probe(label, blob, root):
    print("==", label, "sha256", hashlib.sha256(blob).hexdigest()[:16], "len", len(blob))
    lw = Path(root) / label.replace("/", "_")
    lw.mkdir(parents=True, exist_ok=True)
    pristine = lw / "pristine.target.py"
    pristine.write_bytes(blob)
    pristine.chmod(0o755)
    rc0 = m.run_suite(SUITE, pristine, pristine, lw, "CONTROL")
    print("  control rc", rc0, m.verdict(rc0))
    agree = 0
    killed = 0
    misses = []
    for d in defects:
        old, new = d["old"].encode(), d["new"].encode()
        c = blob.count(old)
        if c != 1:
            misses.append((d["id"], "old-count-%d" % c))
            continue
        mp = lw / ("mutant-%s.target.py" % d["id"])
        mp.write_bytes(blob.replace(old, new, 1))
        mp.chmod(0o755)
        v = m.verdict(m.run_suite(SUITE, mp, pristine, lw, d["id"]))
        if v == "KILLED":
            killed += 1
        if v == table[d["id"]]:
            agree += 1
        else:
            misses.append((d["id"], "%s!=%s" % (v, table[d["id"]])))
    print("  agree %d/%d killed %d misses %s" % (agree, len(defects), killed, misses))


def git_blob(rev, path):
    r = subprocess.run(["/usr/bin/git", "-C", KAKE, "show", "%s:%s" % (rev, path)],
                       capture_output=True)
    if r.returncode != 0:
        raise SystemExit("git show failed: " + r.stderr.decode())
    return r.stdout


def main():
    root = tempfile.mkdtemp(prefix="probe-", dir=sys.argv[1])
    probe("e8d3a924_gate", git_blob("e8d3a924249983972e5163d160cf236487986c55",
                                    "scripts/ledger_append_guard.py"), root)
    probe("12116017_gate", git_blob("12116017c7eb07cc15372e619ea7935438956c03",
                                    "scripts/ledger_append_guard.py"), root)


if __name__ == "__main__":
    main()
