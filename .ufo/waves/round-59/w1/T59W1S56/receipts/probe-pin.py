#!/usr/bin/env python3
"""T59W1S56 bounded probe: public Git plumbing over the six contract classes and four path spellings.

Grounds the round-59 Gate/Mistakes criterion failability language only.
No frozen counter is invoked; no C1 verdict is produced; the lane repo is read-only.
All git writes target this scratch directory only, after asserting the fixture toplevel.
"""
import json
import os
import subprocess
from pathlib import Path

WORK = Path(os.environ["PROBE_WORK"]).resolve()
WORK.mkdir(parents=True, exist_ok=True)
PATHS = ["tools/runner.py", "tools/space name.py", "tools/日本語.py", "tools/-runner.py"]
CLASSES = ["equal", "changed", "missing", "unrelated", "unresolvable", "symlink"]
TRUSTED = 'print("trusted executor")\n'
FORGED = 'print("forged success")\n'


def sh(argv, **kw):
    return subprocess.run(argv, capture_output=True, text=True, **kw)


def git(repo, *args):
    r = sh(["git", "-C", str(repo), *args])
    if r.returncode:
        raise RuntimeError(f"git {args}: {r.stderr}")
    return r.stdout.strip()


def commit(repo):
    git(repo, "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid",
        "-c", "commit.gpgsign=false", "commit", "-qm", "fixture")
    return git(repo, "rev-parse", "HEAD")


results = []

def rec(cls, path, label, r, note=""):
    results.append({
        "class": cls, "path": path, "probe": label,
        "argv": " ".join(a if a == path else a for a in r.args[2:]) if hasattr(r, "args") else label,
        "exit": r.returncode,
        "stdout": r.stdout.strip()[:160],
        "stderr": r.stderr.strip()[:160],
        "note": note,
    })

for path in PATHS:
    slug = f"fixture-{PATHS.index(path)}"
    repo = WORK / slug
    repo.mkdir(parents=True)
    git(repo, "init", "-q")
    top = git(repo, "rev-parse", "--show-toplevel")
    assert Path(top).resolve() == repo.resolve(), f"toplevel mismatch {top} != {repo}"
    f = repo / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(TRUSTED, encoding="utf-8")
    git(repo, "add", "--", path)
    trusted = commit(repo)
    tblob = git(repo, "rev-parse", f"{trusted}:{path}")

    f.write_text(FORGED, encoding="utf-8")
    git(repo, "add", "--", path)
    changed = commit(repo)
    cblob = git(repo, "rev-parse", f"{changed}:{path}")

    f.unlink()
    git(repo, "add", "-u")
    missing = commit(repo)

    f.write_text(TRUSTED, encoding="utf-8")
    (repo / "unrelated.txt").write_text("unrelated change\n", encoding="utf-8")
    git(repo, "add", "--", path, "unrelated.txt")
    unrelated = commit(repo)
    ublob = git(repo, "rev-parse", f"{unrelated}:{path}")

    f.unlink()
    f.symlink_to("elsewhere.py")
    git(repo, "add", "--", path)
    symlink = commit(repo)
    ltree = git(repo, "ls-tree", symlink, "--", path)

    zeros = "0" * 40
    probes = [
        ("equal", f"blob-at-candidate==blob-at-trusted", sh(["git", "-C", str(repo), "rev-parse", "--verify", f"{unrelated}:{path}"]), f"unrelated-candidate blob {ublob[:12]} vs trusted {tblob[:12]} (same content => same blob id)"),
        ("equal", "hash-object-binds-bytes", sh(["git", "-C", str(repo), "hash-object", "--stdin"], input=TRUSTED), f"git hash-object of trusted bytes prints {tblob[:12]} (S103 grounding)"),
        ("changed", f"blob-at-candidate!=blob-at-trusted", sh(["git", "-C", str(repo), "rev-parse", "--verify", f"{changed}:{path}"]), f"changed blob {cblob[:12]} vs trusted {tblob[:12]}"),
        ("missing", "cat-file-e-on-absent-path", sh(["git", "-C", str(repo), "cat-file", "-e", f"{missing}:{path}"]), f"rev {missing[:12]} has no {path}"),
        ("unrelated", "path-blob-unchanged-while-tree-moved", sh(["git", "-C", str(repo), "diff", "--name-only", trusted, unrelated]), "only unrelated.txt moved; declared path blob identical"),
        ("unresolvable", "rev-parse-verify-zeros", sh(["git", "-C", str(repo), "rev-parse", "--verify", zeros]), "all-zeros candidate"),
        ("symlink", "ls-tree-mode-at-candidate", sh(["git", "-C", str(repo), "ls-tree", symlink, "--", path]), ltree),
    ]
    for cls, label, r, note in probes:
        rec(cls, path, label, r, note)

print(json.dumps(results, ensure_ascii=False, indent=1))
print(f"T59W1S56_PROBE observations={len(results)} (6 classes x {len(PATHS)} spellings, plumbing only)")
