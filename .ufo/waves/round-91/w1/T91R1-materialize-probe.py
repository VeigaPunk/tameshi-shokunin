#!/usr/bin/env python3
"""T91R1 materialize probe: the counter's `materialize` (measure-v91.py:65-75)
uses `git archive --format=tar <commit> <fixtures>`; verify that the archive is
byte-identical to the pinned tree's blobs (no .gitattributes export filter can
silently drop or rewrite a fixture file).

Usage: python3 -I T91R1-materialize-probe.py <fleet-repo> <commit> <fixtures-path>
"""
import hashlib, io, os, subprocess, sys, tarfile

fleet, commit, fixtures = sys.argv[1], sys.argv[2], sys.argv[3]
env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8",
       "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null"}
arch = subprocess.run(["git", "-C", fleet, "archive", "--format=tar", commit, fixtures],
                      capture_output=True, env=env).stdout
tree = subprocess.run(["git", "-C", fleet, "cat-file", "-p", commit + ":" + fixtures],
                      capture_output=True, env=env)
# list blobs under the fixtures path from the tree
out = subprocess.run(["git", "-C", fleet, "ls-tree", "-r", commit, fixtures],
                     capture_output=True, text=True, env=env).stdout.strip().split("\n")
want = {}
for line in out:
    meta, path = line.split("\t", 1)
    want[path] = meta.split()[2]
got = {}
with tarfile.open(fileobj=io.BytesIO(arch)) as t:
    for m in t.getmembers():
        if not m.isfile():
            continue
        f = t.extractfile(m).read()
        got[m.name] = hashlib.sha1(b"blob %d\0" % len(f) + f).hexdigest()
attrs = subprocess.run(["git", "-C", fleet, "ls-tree", "-r", "--name-only", commit],
                       capture_output=True, text=True, env=env).stdout
n_attrs = sum(1 for l in attrs.split("\n") if l.endswith(".gitattributes"))
print("gitattributes_in_tree=%d" % n_attrs)
print("tree_blobs=%d archive_files=%d" % (len(want), len(got)))
print("materialize_matches_tree=%s" % (want == got))
miss = sorted(set(want) - set(got))
extra = sorted(set(got) - set(want))
print("missing=%s extra=%s" % (miss or "-", extra or "-"))
