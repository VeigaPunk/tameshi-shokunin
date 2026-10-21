#!/usr/bin/env python3
"""Round-21 C2 counter (frozen before dispatch): F5 env-differential coverage.

Reads only git objects at --rev (never the working tree):
  classified   frozen surfaces whose receipt record has verified pins, every
               required profile tuple, and a classification that follows the
               frozen rules in c2-contract.json
  tool_selftest  tools/env-diff.py --selftest exit 0 in a private clone at --rev
  f5_entry     knowledge entry exists and its `source:` header cites an S### row
               whose status is `mined` in corpus/SOURCES.md at --rev
Exit 0 iff classified == total and tool_selftest and f5_entry; 1 otherwise;
2 setup failure; 64 usage.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONTRACT = HERE / "c2-contract.json"
FLEET = Path("/home/vgpnk/Projects/shokunin")
HEX = re.compile(r"^[0-9a-f]{64}$")


def env():
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def show(repo, rev, path):
    p = subprocess.run(["git", "-C", str(repo), "show", f"{rev}:{path}"], capture_output=True, env=env())
    return p.stdout if p.returncode == 0 else None


def tuple_of(rec):
    if not isinstance(rec, dict):
        return None
    e, o, s = rec.get("exit"), rec.get("stdout_sha256"), rec.get("stderr_sha256")
    if not isinstance(e, int) or isinstance(e, bool) or not isinstance(o, str) or not isinstance(s, str):
        return None
    if not HEX.match(o) or not HEX.match(s):
        return None
    return (e, o, s)


def check_surface(c, frozen, rec, lane_rev):
    why = []
    if not isinstance(rec, dict):
        return ["missing-record"]
    pin = rec.get("pin") or {}
    want_rev = frozen["rev"]
    for k in ("repo", "rev", "path"):
        if pin.get(k) != frozen[k]:
            why.append(f"pin-{k}-mismatch")
    blob = show(FLEET / frozen["repo"], want_rev, frozen["path"])
    if blob is None:
        why.append("pin-unreadable")
    else:
        actual = hashlib.sha256(blob).hexdigest()
        if "blob_sha256" in frozen and actual != frozen["blob_sha256"]:
            why.append("frozen-blob-drift")
        if pin.get("blob_sha256") != actual:
            why.append("pin-blob-mismatch")
    if not isinstance(rec.get("normalization"), str):
        why.append("normalization-undeclared")
    profiles = rec.get("profiles") or {}
    tuples = {}
    for name in c["required_profiles"]:
        t = tuple_of(profiles.get(name))
        if t is None:
            why.append(f"profile-{name}-missing")
        tuples[name] = t
    if why:
        return why
    cls, sens = rec.get("classification"), rec.get("sensitive_to")
    if tuples["clean"] != tuples["clean_repeat"]:
        if cls != "nondeterministic":
            why.append("rule-nondeterministic")
    else:
        diff = sorted(n for n, t in tuples.items() if t != tuples["clean"])
        if not diff:
            if cls != "invariant" or sens not in ([], None):
                why.append("rule-invariant")
        elif cls != "env-sensitive" or sorted(sens or []) != diff:
            why.append("rule-env-sensitive")
    return why


def tool_selftest(repo, rev, tool):
    if show(repo, rev, tool) is None:
        return {"present": False, "exit": None}
    w = Path(tempfile.mkdtemp(prefix="tameshi-r21-c2."))
    try:
        d = w / "lane"
        subprocess.run(["git", "clone", "-q", "--no-hardlinks", str(repo), str(d)], check=True, env=env(), capture_output=True)
        subprocess.run(["git", "-C", str(d), "checkout", "-q", "--detach", rev], check=True, env=env(), capture_output=True)
        (w / "home").mkdir(); (w / "tmp").mkdir()
        argv = ["bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc", "--tmpfs", "/tmp",
                "--bind", str(w), str(w), "--unshare-net", "--die-with-parent", "--chdir", str(d),
                "env", "-i", "PATH=" + os.environ.get("PATH", "/usr/bin:/bin"), f"HOME={w}/home",
                f"TMPDIR={w}/tmp", "LC_ALL=C", "GIT_CONFIG_GLOBAL=/dev/null", "GIT_CONFIG_NOSYSTEM=1",
                "python3", tool, "--selftest"]
        try:
            p = subprocess.run(argv, capture_output=True, timeout=900, env=env())
        except subprocess.TimeoutExpired:
            return {"present": True, "exit": None, "timeout": True}
        lines = [l for l in p.stdout.decode("utf-8", "replace").splitlines() if l.strip()]
        return {"present": True, "exit": p.returncode, "summary": lines[-1] if lines else ""}
    finally:
        shutil.rmtree(w, ignore_errors=True)


def f5_entry(repo, rev, path):
    body = show(repo, rev, path)
    if body is None:
        return False, "entry-missing"
    head = body.decode("utf-8", "replace").splitlines()[:15]
    ids = [i for l in head if l.lower().startswith("source:") for i in re.findall(r"S\d{3,}", l)]
    if not ids:
        return False, "no-source-header"
    src = (show(repo, rev, "corpus/SOURCES.md") or b"").decode("utf-8", "replace")
    status = {}
    for line in src.splitlines():
        if re.match(r"^\|\s*S\d{3,}\s*\|", line):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) > 7:
                status[cells[0]] = cells[7]
    mined = [i for i in ids if status.get(i) == "mined"]
    return (bool(mined), ",".join(mined) if mined else "no-mined-source")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--skip-selftest", action="store_true", help="diagnostic only; never a counting receipt")
    try:
        a = ap.parse_args(argv)
    except SystemExit:
        return 64
    repo = Path(a.repo).resolve()
    p = subprocess.run(["git", "-C", str(repo), "rev-parse", "--verify", a.rev + "^{commit}"], capture_output=True, env=env())
    if p.returncode:
        print("C2: cannot resolve rev", file=sys.stderr)
        return 2
    rev = p.stdout.decode().strip()
    cbytes = CONTRACT.read_bytes()
    c = json.loads(cbytes)
    raw = show(repo, rev, c["receipt_path"])
    receipt, rows = None, {}
    if raw is not None:
        try:
            receipt = json.loads(raw)
            if receipt.get("schema") == c["receipt_schema"]:
                rows = {r.get("surface"): r for r in receipt.get("surfaces", []) if isinstance(r, dict)}
        except (ValueError, AttributeError):
            receipt = None
    per = {}
    for s in c["surfaces"]:
        per[s["name"]] = check_surface(c, s, rows.get(s["name"]), rev)
    classified = sum(1 for v in per.values() if not v)
    st = {"skipped": True} if a.skip_selftest else tool_selftest(repo, rev, c["tool_path"])
    ent, ent_why = f5_entry(repo, rev, c["entry_path"])
    out = {"schema": "tameshi-r21-c2-count-v1", "rev": rev,
           "counter_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           "contract_sha256": hashlib.sha256(cbytes).hexdigest(),
           "receipt_present": raw is not None, "classified": classified, "total": len(c["surfaces"]),
           "surface_findings": per,
           "classifications": {k: (rows.get(k) or {}).get("classification") for k in per},
           "tool_selftest": st, "f5_entry": ent, "f5_entry_detail": ent_why}
    if a.json:
        print(json.dumps(out, indent=1, sort_keys=True))
    ok_st = (not a.skip_selftest) and st.get("exit") == 0
    print(f"C2: classified={classified}/{len(c['surfaces'])} tool_selftest={'pass' if ok_st else 'fail'} f5_entry={ent} rev={rev}", file=sys.stderr)
    return 0 if classified == len(c["surfaces"]) and ok_st and ent else 1


if __name__ == "__main__":
    sys.exit(main())
