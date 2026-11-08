#!/usr/bin/env python3
"""R94SC1 probe: which manifest does a disposition checker actually audit, and can
its receipt tell you?

Read-only on the lane. Both checker revisions are extracted with `git cat-file`
from their own commits; no working-tree file is executed and nothing in the lane
is written.

What it shows:
  * the MANIFEST constant each checker revision reads by default;
  * that the rev-1 checker's receipt is BYTE-IDENTICAL for the round-93 manifest
    and the round-94 manifest, i.e. the receipt does not name the manifest it
    audited, so a green line cannot be attributed to a manifest;
  * that the two manifests are NOT interchangeable: the round-93 checker rejects
    the round-93 manifest (findings=2) and the mechanism-word cheat
    (findings=20);
  * that rev 1 accepts the same mechanism-word cheat (findings=0), so only the
    --min-falsifiable floor rejected it.

Usage: R94SC1-manifest-binding.py [lane]
"""
import hashlib
import os
import subprocess
import sys

LANE = sys.argv[1] if len(sys.argv) > 1 else "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
REV = "7084358c732ebe1334c2eb9a352c3ed96b547f7c"
REV3 = "6a2a1fdd35d15d3958f9860beb2569b443760b46"
HEAD = "HEAD"
SCRATCH = "/fast/scratch/hyaku/tameshi-r94/R94SC1"

CHECKER = ".ufo/evidence/round-94/conjunct-disposition-v94.py"
R93_MANIFEST = "tools/conjunct-disposition.json"
R94_MANIFEST = ".ufo/evidence/round-94/conjunct-disposition.json"
CHEAT = ".ufo/evidence/round-94/pre-freeze/cheat-manifest.json"


def blob(rev, path):
    p = subprocess.run(["git", "-C", LANE, "cat-file", "blob", "%s:%s" % (rev, path)],
                       capture_output=True)
    return p.stdout if p.returncode == 0 else b""


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run(checker_bytes, manifest, tag, rev=REV):
    path = os.path.join(SCRATCH, "chk-%s.py" % tag)
    with open(path, "wb") as fh:
        fh.write(checker_bytes)
    out = os.path.join(SCRATCH, "out-%s.txt" % tag)
    p = subprocess.run([sys.executable, "-I", path, "--lane", LANE, "--rev", rev,
                        "--min-falsifiable", "17", "--manifest", manifest],
                       capture_output=True, text=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(p.stdout + p.stderr)
    rows = [l for l in p.stdout.split("\n") if l.startswith("DISPOSITION rows")]
    finds = [l for l in p.stdout.split("\n") if l.startswith("DISPOSITION_FINDING")]
    return p.returncode, (rows[0] if rows else "-"), len(finds), out


def main():
    c1 = blob(REV, CHECKER)
    c3 = blob(REV3, CHECKER)
    print("LANE %s" % LANE)
    print("REV1 %s  sha256=%s" % (REV, sha(c1)))
    print("REV3 %s  sha256=%s" % (REV3, sha(c3)))
    for rev, b in ((REV, c1), (REV3, c3)):
        man = [l for l in b.decode().split("\n") if l.startswith("MANIFEST")]
        print("  rev %s default %s" % (rev[:8], man[0] if man else "-"))
    print()
    for tag, path in (("r93man", R93_MANIFEST), ("r94man", R94_MANIFEST), ("cheat", CHEAT)):
        b = blob(REV, path)
        print("manifest %-7s %-56s sha256=%s" % (tag, path, sha(b) if b else "ABSENT"))
    print()

    results = {}
    for tag, chk, name in (("rev1", c1, "rev1"), ("rev3", c3, "rev3")):
        for mtag, mpath in (("r93man", R93_MANIFEST), ("r94man", R94_MANIFEST), ("cheat", CHEAT)):
            # the cheat manifest was committed after the frozen revision, so it is read
            # at HEAD; the two round manifests are read at the frozen revision.
            rev = HEAD if mtag == "cheat" else REV
            rc, rows, nf, out = run(chk, mpath, "%s-%s" % (name, mtag), rev)
            results[(name, mtag)] = out
            print("%-5s + %-7s exit=%d  %-52s findings=%d" % (name, mtag, rc, rows, nf))
    print()

    # the receipt must not be able to tell the two manifests apart
    a = open(results[("rev1", "r93man")], encoding="utf-8").read()
    b = open(results[("rev1", "r94man")], encoding="utf-8").read()
    print("REV1_RECEIPT_IDENTICAL_ACROSS_MANIFESTS %s" % ("true" if a == b else "false"))
    print("REV1_RECEIPT_MENTIONS_MANIFEST %d" % (a.lower().count("manifest")))
    c = open(results[("rev3", "r94man")], encoding="utf-8").read()
    print("REV3_RECEIPT_MENTIONS_MANIFEST %d" % (c.lower().count("manifest")))
    print("REV1_REV3_RECEIPT_IDENTICAL %s" % ("true" if a == c else "false"))
    print()
    print("SAMPLE_RECEIPT (rev1, round-94 manifest) first and last lines:")
    ls = [l for l in a.split("\n") if l.strip()]
    for l in ls[:2] + ls[-2:]:
        print("  " + l)


if __name__ == "__main__":
    main()
