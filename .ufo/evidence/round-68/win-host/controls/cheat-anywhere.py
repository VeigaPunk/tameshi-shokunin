#!/usr/bin/env python3
"""cheat-anywhere.py — the round-68 control cheat for the figure-attribution
class. This is the anywhere-in-cited-set matcher the instrument exists to
refuse: given the red row's inputs it searches the WHOLE cited receipt set
(the live selftest receipt AND the preserved rehearsal receipt) and passes
when the figure is found in ANY of them — exactly the relaxation that let
the r66 stale cells pass every sweep until a human wrote R67 correction 1.

Run (scratch control, receipted at
.ufo/evidence/round-68/win-host/controls/cheat-anywhere-passes-red.txt):

  python -I -X utf8 cheat-anywhere.py REPO DOC_REV DOC_PATH FIGURE RECEIPT1 [RECEIPT2 ...]

Prints CHEAT_ANYWHERE: found=N and exits 0 when the figure is in any cited
receipt — for the red pair this is a FALSE pass (the named receipt's bytes
do not contain the figure; only the other cited receipt does).
"""
import subprocess
import sys


def blob(repo, rev, path):
    r = subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, path)],
                       capture_output=True)
    if r.returncode != 0:
        sys.stderr.write("CHEAT_ANYWHERE error=setup %s:%s\n" % (rev[:12], path))
        sys.exit(2)
    return r.stdout


def main():
    if len(sys.argv) < 6:
        sys.stderr.write("usage: cheat-anywhere.py REPO DOC_REV DOC_PATH "
                         "FIGURE RECEIPT1 [RECEIPT2 ...]\n")
        sys.exit(2)
    repo, doc_rev, doc_path, figure = sys.argv[1:5]
    receipts = sys.argv[5:]
    doc = blob(repo, doc_rev, doc_path)
    fig = figure.encode("utf-8")
    if fig not in doc:
        print("CHEAT_ANYWHERE: found=0 figure-absent-from-doc")
        sys.exit(1)
    found = 0
    for path in receipts:
        rev = "859a736deb1e26fd16a0cbd10f6bab0636c7a3a2"
        if fig in blob(repo, rev, path):
            found += 1
    print("CHEAT_ANYWHERE: found=%d cited=%d (set-matcher: pass=%s)"
          % (found, len(receipts), "true" if found else "false"))
    sys.exit(0 if found else 1)


if __name__ == "__main__":
    main()
