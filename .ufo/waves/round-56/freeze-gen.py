#!/usr/bin/env python3
"""Round-56 freeze regeneration check.

Usage: freeze-gen.py --lane LANE --rev REV [--explain] [--out PATH]

Re-derives .ufo/evidence/round-56/freeze.json from the `frozen_paths` list in
.ufo/evidence/round-56/contract.json, reading every file as the blob committed at REV
(never the working tree), and compares the result with the freeze.json committed at the
same REV.

Path mapping, identical to the heredoc in .ufo/evidence/round-56/deciding-run.sh:
a contract path under `tools/`, `.ufo/evidence/round-21/` or `.ufo/evidence/round-48/`
is its own manifest key; every other contract path is relative to
`.ufo/evidence/round-56/` (so `.ufo/evidence/round-56/c1/measure.py` is keyed
`c1/measure.py`). A contract path that is neither under those prefixes nor under the
round directory is unmappable and fails closed. `.ufo/evidence/round-56/freeze.json`
is the manifest itself: a file cannot carry its own sha256, so it is listed and skipped,
exactly as the committed manifest does.

Verdict (one line, always printed):
  FREEZE_GEN: files=N ok          exit 0  regenerated digests == committed manifest
  FREEZE_GEN: files=N MISMATCH    exit 1  with one FREEZE_GEN_MISMATCH line per defect
Exit 2 is usage / not-a-repository and prints no verdict.

--explain adds FREEZE_GEN_FILE lines (key, resolved path, sha256) and the manifest-set
comparison. --out PATH writes the regenerated manifest (schema/round/lane/base and the
amendment list are carried from the committed manifest when readable, else from the
contract) and reports whether its bytes equal the committed blob; entries keep the
contract's frozen_paths order, which is the order the committed manifest uses, so a
faithful regeneration is byte-identical, not merely digest-identical.

Stdlib only; reads only git objects; writes only PATH when --out is given.
"""
import hashlib
import json
import os
import subprocess
import sys

E = ".ufo/evidence/round-56"
VERBATIM_PREFIXES = ("tools/", ".ufo/evidence/round-21/", ".ufo/evidence/round-48/")
SELF = E + "/freeze.json"
SCHEMA = "tameshi-freeze-v1"


def usage(msg=None):
    if msg:
        print("freeze-gen: %s" % msg, file=sys.stderr)
    print("usage: freeze-gen.py --lane LANE --rev REV [--explain] [--out PATH]",
          file=sys.stderr)
    sys.exit(2)


def parse_args(argv):
    opts = {"lane": None, "rev": None, "explain": False, "out": None}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--lane", "--rev", "--out"):
            if i + 1 >= len(argv):
                usage("%s needs a value" % a)
            opts[a[2:]] = argv[i + 1]
            i += 2
        elif a == "--explain":
            opts["explain"] = True
            i += 1
        elif a in ("-h", "--help"):
            usage()
        else:
            usage("unknown argument %r" % a)
    if not opts["lane"] or not opts["rev"]:
        usage("--lane and --rev are required")
    return opts


ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ENV.update(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1")


def git(*args):
    return subprocess.run(["git"] + list(args), capture_output=True, env=ENV)


def manifest_key(path):
    """Contract path -> freeze.json key, or None when the key cannot be represented."""
    if path.startswith(VERBATIM_PREFIXES):
        return path
    if path.startswith(E + "/"):
        key = path[len(E) + 1:]
        return key or None
    return None


def key_path(key):
    """freeze.json key -> contract path (the inverse of manifest_key)."""
    if key.startswith(VERBATIM_PREFIXES):
        return key
    return "%s/%s" % (E, key)


def sha(data):
    return hashlib.sha256(data).hexdigest() if data is not None else "UNREADABLE"


def main():
    opts = parse_args(sys.argv[1:])
    lane = os.path.abspath(opts["lane"])
    if not os.path.isdir(lane):
        usage("lane is not a directory: %s" % lane)
    top = git("-C", lane, "rev-parse", "--show-toplevel")
    if top.returncode != 0:
        usage("lane is not a git work tree: %s" % lane)
    lane = top.stdout.decode().strip()
    rev = git("-C", lane, "rev-parse", "--verify", "%s^{commit}" % opts["rev"])
    if rev.returncode != 0:
        usage("revision does not resolve to a commit: %s" % opts["rev"])
    rev = rev.stdout.decode().strip()

    def blob(path, at=rev):
        r = git("-C", lane, "show", "%s:%s" % (at, path))
        return r.stdout if r.returncode == 0 else None

    bad = []
    contract_bytes = blob(E + "/contract.json")
    if contract_bytes is None:
        bad.append("contract.json unreadable-at-rev %s" % rev[:12])
        contract = None
    else:
        try:
            contract = json.loads(contract_bytes)
        except ValueError as exc:
            bad.append("contract.json unparseable-at-rev %s: %s" % (rev[:12], exc))
            contract = None

    files = {}
    self_listed = False
    if contract is not None:
        frozen_paths = contract.get("frozen_paths") or []
        if not isinstance(frozen_paths, list) or not frozen_paths:
            bad.append("contract.json frozen_paths missing-or-empty")
            frozen_paths = []
        for path in frozen_paths:
            if not isinstance(path, str):
                bad.append("contract.json frozen_paths non-string entry %r" % (path,))
                continue
            if path == SELF:
                self_listed = True
                continue
            key = manifest_key(path)
            if key is None:
                bad.append("%s unmappable (not tools/, .ufo/evidence/round-21|48/ or %s/)"
                           % (path, E))
                continue
            if key in files:
                bad.append("%s duplicate-key %s" % (path, key))
                continue
            back = key_path(key)
            if back != path:
                bad.append("%s mapping-does-not-round-trip (%s -> %s)" % (path, key, back))
                continue
            data = blob(path)
            if data is None:
                bad.append("%s unreadable-at-rev %s" % (path, rev[:12]))
                files[key] = "UNREADABLE"
                continue
            files[key] = sha(data)

    manifest_bytes = blob(E + "/freeze.json")
    manifest = None
    if manifest_bytes is None:
        bad.append("freeze.json unreadable-at-rev %s" % rev[:12])
    else:
        try:
            manifest = json.loads(manifest_bytes)
        except ValueError as exc:
            bad.append("freeze.json unparseable-at-rev %s: %s" % (rev[:12], exc))
    recorded = (manifest or {}).get("files")
    if manifest is not None and not isinstance(recorded, dict):
        bad.append("freeze.json has no files object")
        recorded = None

    # The manifest's own header is pinned by the freeze commit, not by any digest, so a
    # header-only edit would otherwise pass a digest-only check. Cross-check it against
    # the contract (the amendment list is the manifest's own record and is not compared).
    if manifest is not None and contract is not None:
        for field, want in (("schema", SCHEMA), ("round", contract.get("round")),
                            ("lane", contract.get("lane")), ("base", contract.get("base"))):
            got = manifest.get(field, "<absent>")
            if got != want:
                bad.append("freeze.json header %s=%r != %r" % (field, got, want))

    if recorded is not None:
        for key in sorted(set(files) | set(recorded)):
            if key not in recorded:
                bad.append("%r missing-from-manifest regenerated=%s"
                           % (key, files[key][:12]))
            elif key not in files:
                bad.append("%r extra-in-manifest recorded=%s (not a contract frozen path)"
                           % (key, recorded[key][:12]))
            elif files[key] != recorded[key]:
                bad.append("%s %s != %s" % (key, files[key][:12], recorded[key][:12]))

    if opts["explain"]:
        print("FREEZE_GEN_LANE %s" % lane)
        print("FREEZE_GEN_REV %s" % rev)
        print("FREEZE_GEN_CONTRACT %s" % (E + "/contract.json"))
        print("FREEZE_GEN_SELF %s listed=%s" % (SELF, "yes" if self_listed else "no"))
        for key in sorted(files):
            print("FREEZE_GEN_FILE %s path=%s sha256=%s"
                  % (key, key_path(key), files[key]))
        print("FREEZE_GEN_SET regenerated=%d manifest=%d amendments=%d"
              % (len(files), len(recorded or {}),
                 len((manifest or {}).get("amendments") or [])))

    if opts["out"]:
        base = contract or {}
        src = manifest or {}
        regen = {
            "schema": src.get("schema", SCHEMA),
            "round": base.get("round", src.get("round")),
            "lane": base.get("lane", src.get("lane")),
            "base": base.get("base", src.get("base")),
            "files": dict(files),
            "amendments": src.get("amendments", base.get("amendments", [])),
        }
        payload = (json.dumps(regen, indent=1) + "\n").encode()
        with open(opts["out"], "wb") as fh:
            fh.write(payload)
        same = manifest_bytes is not None and payload == manifest_bytes
        print("FREEZE_GEN_OUT %s bytes=%d identical=%s sha256=%s"
              % (opts["out"], len(payload), "yes" if same else "no", sha(payload)))
        if manifest_bytes is not None and not same:
            bad.append("regenerated-bytes != committed freeze.json")

    verdict = "ok" if not bad else "MISMATCH"
    print("FREEZE_GEN: files=%d %s" % (len(files), verdict))
    for b in bad:
        print("FREEZE_GEN_MISMATCH %s" % b)
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
