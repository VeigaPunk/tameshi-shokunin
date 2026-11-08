#!/usr/bin/env python3
"""Round-93 pin generator (round-92 M5: no hand-copied instrument constants).

Derives every constant the round-96 counter checks from git objects at a named
revision and writes `.ufo/evidence/round-96/c1/pins.json`:

    spec_sha256   sha256 of the census spec blob
    gate_commit   the fleet commit the spec pins
    gate_path     the gate path inside the fleet repo
    gate_sha256   sha256 of the gate blob at that commit
    fixtures      the fixture tree the gate reads

`--check` re-derives the same five values and refuses (exit 1, `PINS_DRIFT`)
when any differs from the committed pins.json, which is what makes a stale
hand-copied constant impossible to ship silently.

Usage: python3 -I make-pins96.py --lane LANE --rev REV [--check]
Exit: 0 written/agreed; 1 drift or unreadable object; 2 usage.
"""
import argparse, hashlib, json, os, subprocess, sys

GIT = "/usr/bin/git"

SPEC_PATH = ".ufo/evidence/round-96/c1/census-mutants.json"
PINS_PATH = ".ufo/evidence/round-96/c1/pins.json"


def git(repo, *a):
    p = subprocess.run([GIT, "-C", repo, *a], capture_output=True,
                       env={"PATH": "/usr/local/bin:/usr/bin:/bin", "LC_ALL": "C.UTF-8",
                            "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1",
                            "GIT_CONFIG_GLOBAL": "/dev/null"})
    return p.returncode, p.stdout, p.stderr


def derive(lane, rev):
    rc, spec_bytes, err = git(lane, "cat-file", "blob", rev + ":" + SPEC_PATH)
    if rc != 0:
        raise SystemExit("SPEC_UNREADABLE " + err.decode(errors="replace").strip()[:160])
    spec = json.loads(spec_bytes)
    g = spec["gate"]
    rc, gate_bytes, err = git(g["repo"], "cat-file", "blob", g["commit"] + ":" + g["path"])
    if rc != 0:
        raise SystemExit("GATE_UNREADABLE " + err.decode(errors="replace").strip()[:160])
    return {
        "spec_sha256": hashlib.sha256(spec_bytes).hexdigest(),
        "gate_commit": g["commit"],
        "gate_path": g["path"],
        "gate_sha256": hashlib.sha256(gate_bytes).hexdigest(),
        "fixtures": g["fixtures"],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if not a.lane or not a.lane.strip():
        print("PINS_SETUP lane-empty"); return 2
    if not a.rev or not __import__('re').fullmatch(r"[0-9a-f]{40}", a.rev):
        print("PINS_SETUP rev-not-a-commit-id"); return 2
    lane = os.path.realpath(a.lane)
    if not os.path.isabs(a.lane):
        print("PINS_SETUP lane-not-absolute"); return 2
    _top = __import__('subprocess').run([GIT,"-C",lane,"rev-parse","--show-toplevel"],capture_output=True,env={"PATH":"/usr/local/bin:/usr/bin:/bin","LC_ALL":"C.UTF-8","GIT_NO_REPLACE_OBJECTS":"1","GIT_CONFIG_NOSYSTEM":"1","GIT_CONFIG_GLOBAL":"/dev/null"})
    if _top.returncode != 0 or os.path.realpath(_top.stdout.decode().strip()) != lane:
        print("PINS_SETUP lane-toplevel-mismatch"); return 2
    derived = derive(lane, a.rev)
    if a.check:
        rc, have, _ = git(lane, "cat-file", "blob", a.rev + ":" + PINS_PATH)
        if rc != 0:
            print("PINS_DRIFT pins-absent-at-rev")
            return 1
        try:
            pins = json.loads(have)
        except Exception:
            print("PINS_DRIFT pins-unparsable")
            return 1
        drift = [k for k, v in derived.items() if pins.get(k) != v]
        print("PINS_DERIVED " + " ".join("%s=%s" % (k, derived[k]) for k in sorted(derived)))
        print("PINS_CHECK " + ("OK" if not drift else "DRIFT " + ",".join(drift)))
        return 0 if not drift else 1
    out = os.path.join(lane, PINS_PATH)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if os.path.lexists(out) and os.path.islink(out):
        print("PINS_SETUP pins-symlink-refused"); return 2
    _tmp = out + ".tmp-pins"
    if os.path.lexists(_tmp):
        import os as _o2
        if _o2.path.islink(_tmp): print("PINS_SETUP tmp-symlink-refused"); return 2
        _o2.unlink(_tmp)
    import os as _o3, json as _j3
    _fd = _o3.open(_tmp, _o3.O_WRONLY|_o3.O_CREAT|_o3.O_EXCL|getattr(_o3,"O_NOFOLLOW",0), 0o644)
    with _o3.fdopen(_fd, "w", encoding="utf-8") as f:
        json.dump(derived, f, indent=1, sort_keys=True)
        f.write("\n")
        f.flush()
        import os as _o4
        _o4.fsync(f.fileno())
    import os as _o5
    _o5.replace(_tmp, out)
    print("PINS_WRITTEN " + out)
    print("PINS_DERIVED " + " ".join("%s=%s" % (k, derived[k]) for k in sorted(derived)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
