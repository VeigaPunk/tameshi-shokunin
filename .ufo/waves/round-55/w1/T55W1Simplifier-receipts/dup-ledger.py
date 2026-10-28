#!/usr/bin/env python3
"""Duplication ledger for the seven `strict_scratch_root` definitions (read-only).

Counts, at two revisions, what a shared `tools/scratch_root.py` would collapse:
the helper bodies, the raise token, and the `class ScratchRootUnusable` blocks.
Blanks/trailing newlines are excluded so the numbers are line counts a reader can
reproduce with `git show REV:tools/<tool>.py`.

Usage: dup-ledger.py LANE REV[:LABEL] REV[:LABEL] ...
"""
import hashlib
import subprocess
import sys

TOOLS = ("env-diff", "repeat-control", "registry-check", "bash-witness-study",
         "pin-disposition", "evidence-disposition", "context-capture")


def show(lane, rev, tool):
    p = subprocess.run(["git", "-C", lane, "show", "%s:tools/%s.py" % (rev, tool)],
                       capture_output=True, text=True)
    if p.returncode:
        raise SystemExit("git show failed for %s at %s: %s" % (tool, rev, p.stderr))
    return p.stdout.splitlines()


def helper(src):
    s = next(i for i, l in enumerate(src) if l.startswith("def strict_scratch_root():"))
    e = next(i for i in range(s, len(src)) if src[i].rstrip() == "    return tempfile.gettempdir()")
    return src[e:s - 1:-1][::-1]


def klass(src):
    idx = [i for i, l in enumerate(src) if l.startswith("class ScratchRootUnusable")]
    if not idx:
        return None
    s = idx[0]
    e = s + 1
    while e < len(src) and src[e].startswith("    "):
        e += 1
    return src[s:e]


def raiser(src):
    body = "\n".join(helper(src))
    for token in ("raise ScratchRootUnusable(", "raise RuntimeError("):
        if token in body:
            return token
    return "(none)"


def main():
    lane = sys.argv[1]
    for spec in sys.argv[2:]:
        rev, _, label = spec.partition(":")
        rows = {t: show(lane, rev, t) for t in TOOLS}
        groups, total = {}, 0
        for t, src in rows.items():
            body = helper(src)
            total += len(body)
            groups.setdefault(hashlib.sha256("\n".join(body).encode()).hexdigest()[:8], []).append(
                (t, len(body)))
        print("== %s (%s)" % (label or rev[:12], rev))
        print("   helper bodies: %d lines total, %d distinct" % (total, len(groups)))
        for h, v in sorted(groups.items()):
            print("      %s %2d lines  %s" % (h, v[0][1], [t for t, _ in v]))
        tokens = {}
        for t, src in rows.items():
            tokens.setdefault(raiser(src), []).append(t)
        print("   raise tokens: %d distinct" % len(tokens))
        for k, v in tokens.items():
            print("      %-28s %s" % (k, v))
        cgroups, ctotal, absent = {}, 0, []
        for t, src in rows.items():
            k = klass(src)
            if k is None:
                absent.append(t)
                continue
            ctotal += len(k)
            cgroups.setdefault(hashlib.sha256("\n".join(k).encode()).hexdigest()[:8], []).append(
                (t, len(k)))
        print("   class blocks: %d lines total, %d distinct, absent in %s"
              % (ctotal, len(cgroups), absent or "none"))
        for h, v in sorted(cgroups.items()):
            print("      %s %d lines  %s" % (h, v[0][1], [t for t, _ in v]))
        sizes = sum(len(src) for src in rows.values())
        print("   seven files: %d lines" % sizes)
        print()


if __name__ == "__main__":
    main()
