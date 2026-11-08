#!/usr/bin/env python3
"""Round-93 pin generator (round-92 M5: no hand-copied instrument constants).

Derives every constant the round-95 counter checks from git objects at a named
revision and writes `.ufo/evidence/round-95/c1/pins.json`:

    spec_sha256   sha256 of the census spec blob
    gate_commit   the fleet commit the spec pins
    gate_path     the gate path inside the fleet repo
    gate_sha256   sha256 of the gate blob at that commit
    fixtures      the fixture tree the gate reads

`--check` re-derives the same five values and refuses (exit 1, `PINS_DRIFT`)
when any differs from the committed pins.json, which is what makes a stale
hand-copied constant impossible to ship silently.

Usage: python3 -I make-pins95.py --lane LANE --rev REV [--check]
Exit: 0 written/agreed; 1 drift or unreadable object; 2 usage.
"""
import argparse, hashlib, json, os, subprocess, sys

SPEC_PATH = ".ufo/evidence/round-95/c1/census-mutants.json"
PINS_PATH = ".ufo/evidence/round-95/c1/pins.json"


def git(repo, *a):
    p = subprocess.run(["git", "-C", repo, *a], capture_output=True,
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
    lane = os.path.realpath(a.lane)
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
    with open(out, "w", encoding="utf-8") as f:
        json.dump(derived, f, indent=1, sort_keys=True)
        f.write("\n")
    print("PINS_WRITTEN " + out)
    print("PINS_DERIVED " + " ".join("%s=%s" % (k, derived[k]) for k in sorted(derived)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
