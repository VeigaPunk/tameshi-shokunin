#!/usr/bin/env python3
"""Independent C1 re-derivation (R99E1), written from plans/round-99.plan.md C1
wording only, without importing tools/tally-reconcile.py.

Reads records/receipts as blobs at --rev via git cat-file. Grammar:
  token tally:    TOKEN (3+ chars, UPPER) ':' N/M 'pass'
  selftest tally: word 'selftest' then <=12 non-digit chars then N/M,
                  not inside a token tally span
  citation:       same-line path ending .out/.txt/.log/.json, not in a URL,
                  not the record itself
Resolution: literal tree path, else under record round dirs
  .ufo/evidence/round-NN and .ufo/waves/round-NN (NN from record name);
  0 hits -> unresolved, >1 distinct -> ambiguous-path.
Grading: token pair matched iff every receipt line with same TOKEN shows
  claimed N/M (none -> unbound token-absent). selftest pair: receipt
  *_SELFTEST lines; none -> no-selftest-line; >1 distinct token ->
  ambiguous-selftest; else every observed N/M must equal claim.
Exit 0 iff no mismatched and no unbound, else 1.
"""
import argparse, re, subprocess, sys

TOKEN = re.compile(r"\b([A-Z][A-Z0-9_]{2,}):\s+(\d+)/(\d+)\s+pass\b")
SELFTEST = re.compile(r"(?i)\bselftest\b[^0-9\n]{0,12}?(\d+)/(\d+)\b")
CITE = re.compile(r"[A-Za-z0-9_./-]+\.(?:out|txt|log|json)\b")
RSELFTEST = re.compile(r"\b([A-Z][A-Z0-9_]*_SELFTEST):\s+(\d+)/(\d+)\s+pass\b")
ROUND = re.compile(r"round-(\d+)")

def git(repo, *a):
    p = subprocess.run(["/usr/bin/git", "-C", repo, *a], capture_output=True,
                       env={"PATH": "/usr/bin:/bin", "LANG": "C",
                            "GIT_NO_REPLACE_OBJECTS": "1",
                            "GIT_CONFIG_GLOBAL": "/dev/null",
                            "GIT_CONFIG_NOSYSTEM": "1"})
    return p.returncode, p.stdout

class BlobTree:
    def __init__(self, repo, rev):
        if not re.fullmatch(r"[0-9a-f]{40}", rev or ""):
            raise SystemExit("rev-not-40-hex")
        rc, out = git(repo, "cat-file", "-t", rev)
        if rc != 0 or out.decode().strip() != "commit":
            raise SystemExit("rev-not-commit")
        rc, out = git(repo, "ls-tree", "-r", "-z", "--name-only", rev)
        assert rc == 0
        self.repo, self.rev = repo, rev
        self.paths = set(x for x in out.decode("utf-8", "surrogateescape").split("\0") if x)

    def blob(self, path):
        rc, out = git(self.repo, "cat-file", "blob", f"{self.rev}:{path}")
        assert rc == 0, path
        return out.decode("utf-8", "replace")

def strip(s):
    s = s.strip("/")
    while s.startswith("./"):
        s = s[2:]
    return s

def tallies(line):
    found, spans = [], []
    for m in TOKEN.finditer(line):
        found.append(("token", m.group(1), int(m.group(2)), int(m.group(3))))
        spans.append(m.span())
    for m in SELFTEST.finditer(line):
        s, e = m.span(1)[0], m.span(2)[1]
        if any(a <= s < b or a < e <= b for a, b in spans):
            continue
        found.append(("selftest", "-", int(m.group(1)), int(m.group(2))))
    return found

def citations(line, rec):
    out = []
    for m in CITE.finditer(line):
        st = m.start()
        before = line[:st]
        # URL check: citation glued into a http(s)://... token
        if re.search(r"https?://\S*$", before):
            continue
        head12 = line[max(0, st - 12):st + 3]
        if "://" in head12:
            continue
        raw = m.group(0)
        if raw.startswith("/"):
            out.append(raw)
            continue
        p = strip(raw)
        if p and p != rec and p not in out:
            out.append(p)
    return out

def resolve(tree, cite, roots):
    if cite.startswith("/"):
        return None, "unresolved"
    if cite in tree.paths:
        return cite, None
    hits = sorted({r + "/" + cite for r in roots if (r + "/" + cite) in tree.paths})
    if not hits:
        return None, "unresolved"
    if len(hits) > 1:
        return None, "ambiguous-path"
    return hits[0], None

def grade(form, token, n, m, text):
    if form == "token":
        obs = [(int(a), int(b)) for t, a, b in TOKEN.findall(text) if t == token]
        if not obs:
            return "unbound", "-", "token-absent"
    else:
        rows = RSELFTEST.findall(text)
        if not rows:
            return "unbound", "-", "no-selftest-line"
        if len({t for t, _, _ in rows}) > 1:
            return "unbound", "-", "ambiguous-selftest"
        obs = [(int(a), int(b)) for _, a, b in rows]
    shown = ",".join(sorted({f"{a}/{b}" for a, b in obs}))
    return ("matched", shown, "equal") if all(o == (n, m) for o in obs) else ("mismatched", shown, "differs")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--record", action="append", required=True)
    a = ap.parse_args()
    tree = BlobTree(a.repo, a.rev)
    T = P = M = X = U = C = 0
    out = []
    for rec_raw in a.record:
        rec = strip(rec_raw)
        assert rec in tree.paths, f"record-absent:{rec}"
        roots = []
        mr = ROUND.search(rec.rsplit("/", 1)[-1])
        if mr:
            roots = [f".ufo/evidence/round-{mr.group(1)}", f".ufo/waves/round-{mr.group(1)}"]
        for ln, text in enumerate(tree.blob(rec).split("\n"), 1):
            fs = tallies(text)
            if not fs:
                continue
            cs = citations(text, rec)
            for form, token, n, m in fs:
                T += 1
                if not cs:
                    C += 1
                    out.append(f"TALLY uncited {rec}:{ln} {form} {token} claimed={n}/{m} receipt=- observed=- detail=no-citation")
                    continue
                for c in cs:
                    P += 1
                    path, why = resolve(tree, c, roots)
                    if path is None:
                        U += 1
                        out.append(f"TALLY unbound {rec}:{ln} {form} {token} claimed={n}/{m} receipt={c} observed=- detail={why}")
                        continue
                    v, obs, det = grade(form, token, n, m, tree.blob(path))
                    M += (v == "matched"); X += (v == "mismatched"); U += (v == "unbound")
                    out.append(f"TALLY {v} {rec}:{ln} {form} {token} claimed={n}/{m} receipt={path} observed={obs} detail={det}")
    out.append(f"TALLY_RECONCILE records={len(a.record)} tallies={T} pairs={P} matched={M} mismatched={X} unbound={U} uncited={C}")
    print("\n".join(out))
    return 0 if X == 0 and U == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
