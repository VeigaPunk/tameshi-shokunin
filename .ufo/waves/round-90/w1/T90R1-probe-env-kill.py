#!/usr/bin/env python3
"""T90R1 probe: (1) do C1 selftest verdicts depend on the environment the counter fixes
(env_for: 5 vars, PATH fixed, LANG=C.UTF-8, no TZ)? (2) is each KILLED rc a check kill
(a `SURVIVED\t<label>` line + exit 3 `selftest FAILED`) or a crash/other exit?
Reads only the frozen spec/gate bytes from the fleet and lane at pinned commits; writes
only under --work (scratch). Never touches the lane or the fleet tree.
Usage: python3 -I probe_env_kill.py --work EMPTY_DIR
"""
import argparse, hashlib, json, os, subprocess, sys, tarfile, io

FLEET = "/home/vgpnk/Projects/shokunin"
LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
GATE_COMMIT = "f47ad6ba8d306f8125597401cb2ce45c1297a593"
GATE_PATH = "scripts/sources-census.sh"
GATE_SHA = "3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30"
FIXTURES = "scripts/fixtures/sources-census"
SPEC_REV = "3485ceb08df394edf5fbe26bd09b03985a04fba1"
SPEC_PATH = ".ufo/evidence/round-90/c1/census-mutants.json"
SPEC_SHA = "ce8983d577b1fa71afd1760b80304cba87c56ca339384df06eb2705a5bfde290"


def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True, check=True).stdout


def counter_env(work):  # byte-for-byte the frozen measure.py env_for
    tmp = os.path.join(work, "tmp")
    os.makedirs(tmp, exist_ok=True)
    return {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": work, "TMPDIR": tmp,
            "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}


def ordinary_env(work, variant):
    tmp = os.path.join(work, "tmp-" + variant)
    os.makedirs(tmp, exist_ok=True)
    e = dict(os.environ)
    e["TMPDIR"] = tmp
    if variant == "ordinary":
        e.update({"TZ": "America/Sao_Paulo", "LANG": "en_US.UTF-8", "LC_ALL": "",
                  "SHOKUNIN_ROOT": FLEET})
    elif variant == "posix":
        e.update({"LANG": "C", "LC_ALL": "C"})
        e.pop("TZ", None)
    return e


def materialize(text_bytes, dest, arch):
    os.makedirs(dest, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(arch)) as t:
        t.extractall(dest, filter="data")
    gp = os.path.join(dest, GATE_PATH)
    os.makedirs(os.path.dirname(gp), exist_ok=True)
    with open(gp, "wb") as f:
        f.write(text_bytes)
    os.chmod(gp, 0o755)
    return gp


def selftest(gp, env, cwd):
    p = subprocess.run(["bash", gp, "selftest"], cwd=cwd, env=env, capture_output=True,
                       timeout=180, stdin=subprocess.DEVNULL)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    work = os.path.realpath(a.work)
    assert os.path.isdir(work) and not os.listdir(work), "work must be an empty dir"

    spec_bytes = git(LANE, "cat-file", "blob", f"{SPEC_REV}:{SPEC_PATH}")
    assert hashlib.sha256(spec_bytes).hexdigest() == SPEC_SHA, "spec sha mismatch"
    spec = json.loads(spec_bytes)
    gate = git(FLEET, "cat-file", "blob", f"{GATE_COMMIT}:{GATE_PATH}")
    assert hashlib.sha256(gate).hexdigest() == GATE_SHA, "gate pin mismatch"
    arch = git(FLEET, "archive", "--format=tar", GATE_COMMIT, FIXTURES)
    gtext = gate.decode("utf-8")

    texts = {"pristine": gate}
    for m in spec["mutants"]:
        cnt = gtext.count(m["old"])
        texts[m["id"]] = (gtext.replace(m["old"], m["new"], 1) if cnt >= 1 else gtext).encode()
        if cnt != 1:
            print("PROBE_INVALID %s count=%d" % (m["id"], cnt))

    variants = {"counter": lambda w: counter_env(w), "ordinary": lambda w: ordinary_env(w, "ordinary"),
                "posix": lambda w: ordinary_env(w, "posix")}
    results = {}
    for name, text in texts.items():
        for vname, mk in variants.items():
            d = os.path.join(work, "%s-%s" % (name, vname))
            gp = materialize(text, d, arch)
            env = mk(os.path.join(work, "home-" + vname))
            os.makedirs(env["HOME"], exist_ok=True)
            rc, out, err = selftest(gp, env, os.path.dirname(gp))
            surv = [l for l in out.split("\n") if l.startswith("SURVIVED")]
            kl = sum(1 for l in out.split("\n") if l.startswith("killed"))
            failed_line = "selftest FAILED" in err
            results[(name, vname)] = (rc, len(surv), kl, failed_line, err.strip()[-160:])
            print("PROBE %-9s %-9s rc=%s surv=%d killed_checks=%d selftest_FAILED_on_stderr=%s err_tail=%r" % (
                name, vname, rc, len(surv), kl, failed_line, err.strip()[-160:]))
            if surv:
                for l in surv:
                    print("PROBE_SURVIVED_LINE %s %s %s" % (name, vname, l))
            if name != "pristine":
                os.system("rm -rf -- '%s'" % d)  # scratch-only; never the lane or fleet

    print("PROBE_SUMMARY")
    for m in spec["mutants"]:
        mid = m["id"]
        c = results[(mid, "counter")]
        same = all(results[(mid, v)][0] == c[0] for v in variants)
        reason = "check-kill" if (c[0] == 3 and c[3]) else ("survived" if c[0] == 0 else "crash-or-other-rc=%s" % c[0])
        print("PROBE_ROW %s counter_rc=%s ordinary_rc=%s posix_rc=%s same_rc_all_envs=%s reason=%s" % (
            mid, c[0], results[(mid, "ordinary")][0], results[(mid, "posix")][0], same, reason))


if __name__ == "__main__":
    main()
