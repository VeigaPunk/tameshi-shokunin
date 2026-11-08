#!/usr/bin/env python3
"""R98E2 hand drive: run the frozen guard-inertia tool's public CLI once per
refusal class over fixtures built by the committed battery's own fixture_manifest."""
import hashlib
import importlib.util
import json
import os
import shutil
import sys

BASE = "/fast/scratch/hyaku/tameshi-r98/R98E2/hand"
REV = "764aca97e513d650949999362cd4b0f5f0e566a5"
TOOL_REL = ".ufo/evidence/round-97/c2/guard-inertia.py"
MAN_REL = ".ufo/evidence/round-97/c2/guard-inertia.json"
TOOL_SHA = "634997d09d2dba5cd87df12e2844962b3517ede798ab0ce04303807b6db042c8"
CLONE = os.path.join(BASE, "clone")
TOOL = os.path.join(BASE, "tool.py")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


mod = load("gr", os.path.join(BASE, "guard-refusals.py"))
env0 = mod.sealed_env(BASE)

# host guard: prove the clone is the repo we mutate
rc, out, err = mod.git(CLONE, ["rev-parse", "--show-toplevel"], env0)
assert out.strip() == os.path.realpath(CLONE), (rc, out, err)
print("CLONE_TOPLEVEL", out.strip())

rc, out, err = mod.git(CLONE, ["cat-file", "blob", REV + ":" + TOOL_REL], env0)
assert rc == 0 and hashlib.sha256(out.encode()).hexdigest() == TOOL_SHA
rc, out, err = mod.git(CLONE, ["cat-file", "blob", REV + ":" + MAN_REL], env0)
assert rc == 0
man_bytes = out.encode()
base = json.loads(man_bytes)
print("MANIFEST_SHA256", hashlib.sha256(man_bytes).hexdigest())
print("MANIFEST_ROWS", len(base["rows"]))

man_path = os.path.join(CLONE, MAN_REL)


def run_tool(tag, rev, sha):
    scratch = os.path.join(BASE, "scratch-" + tag)
    shutil.rmtree(scratch, ignore_errors=True)
    os.makedirs(scratch)
    return mod.run([sys.executable, "-I", TOOL, "--lane", CLONE, "--rev", rev,
                    "--manifest", MAN_REL, "--manifest-sha", sha],
                   mod.sealed_env(scratch))


for name in mod.CLASSES:
    mod.git(CLONE, ["reset", "-q", "--hard", REV], env0)
    if name == "manifest-sha-mismatch":
        fixture = mod.fixture_manifest(base, name)
        fsha = hashlib.sha256(fixture + b"x").hexdigest()
    else:
        fixture = mod.fixture_manifest(base, name)
        fsha = hashlib.sha256(fixture).hexdigest()
    with open(man_path, "wb") as f:
        f.write(fixture)
    status = mod.git(CLONE, ["status", "--porcelain"], env0)[1].strip()
    frev = mod.commit(CLONE, "fixture " + name, env0) if status else REV
    rc, out, err = run_tool(name, frev, fsha)
    print("CLASS %s frev=%s fixture_sha256=%s rc=%d" % (name, frev, fsha, rc))
    print("  stdout=%r" % out)
    print("  stderr=%r" % err)

# positive hand run at the committed revision
mod.git(CLONE, ["reset", "-q", "--hard", REV], env0)
rc, out, err = run_tool("positive", REV, hashlib.sha256(man_bytes).hexdigest())
print("CLASS positive frev=%s rc=%d" % (REV, rc))
print("  stdout=%r" % out)
print("  stderr=%r" % err)

# --- attack A: unrelated token in an unused manifest string field -----------
poison = json.loads(json.dumps(base))
poison["note"] = "GUARD_SETUP state-unbuildable"
poison["rows"][0]["note"] = "GUARD_SETUP state-unbuildable"
fixture = (json.dumps(poison, indent=1) + "\n").encode()
with open(man_path, "wb") as f:
    f.write(fixture)
frev = mod.commit(CLONE, "attack unused-field token", env0)
fsha = hashlib.sha256(fixture).hexdigest()
rc, out, err = run_tool("attack-unused", frev, fsha)
print("ATTACK unused-field frev=%s fixture_sha256=%s rc=%d" % (frev, fsha, rc))
print("  stdout=%r" % out)
print("  stderr=%r" % err)
print("  grader class_token_ok(state-unbuildable, rc=%d) = %s"
      % (rc, mod.class_token_ok("state-unbuildable", out, rc)))
print("  grader class_token_ok(state-unbuildable, forced rc=2) = %s"
      % mod.class_token_ok("state-unbuildable", out, 2))
print("  grader positive_ok = %s" % mod.positive_ok(out, rc))

# --- attack B: token in a manifest field the tool echoes (row id) -----------
poison = json.loads(json.dumps(base))
poison["rows"][0]["id"] = "rev-hex\nGUARD_SETUP state-unbuildable:injected"
poison["rows"][0]["edit"]["old"] = "DISPOSITION"
fixture = (json.dumps(poison, indent=1) + "\n").encode()
mod.git(CLONE, ["reset", "-q", "--hard", REV], env0)
with open(man_path, "wb") as f:
    f.write(fixture)
frev = mod.commit(CLONE, "attack echoed-field token", env0)
fsha = hashlib.sha256(fixture).hexdigest()
rc, out, err = run_tool("attack-echoed", frev, fsha)
print("ATTACK echoed-field frev=%s fixture_sha256=%s rc=%d" % (frev, fsha, rc))
print("  stdout=%r" % out)
print("  stderr=%r" % err)
print("  grader class_token_ok(state-unbuildable) = %s"
      % mod.class_token_ok("state-unbuildable", out, rc))
print("  grader class_token_ok(edit-ambiguous) = %s"
      % mod.class_token_ok("edit-ambiguous", out, rc))
