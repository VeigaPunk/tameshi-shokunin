#!/usr/bin/env python3
"""hardening-lint.py — the lane's inherited-hardening lint for counter instruments.

considerthese/2026-11-07.md idea 1: keep the list of defences the lane has already
paid for and grep every new counter for them BEFORE its freeze, reporting which are
missing. This is not a proof: it catches the class where a successor silently drops a
defence an earlier kill bought (round 90 M3: a sealed read hardened in round 82 was not
carried into the next instrument; round 91 M2: the pin that would have caught the
post-freeze repair was absent).

Usage: python3 -I hardening-lint.py <counter.py> [--json]
Exit: 0 every defence present; 1 at least one missing; 64 usage.

Defences (name -> what must be findable in the bytes; each entry is a list of
ALTERNATIVES, and an alternative is a group of patterns that must ALL be present):
  self-pin                 a SELF_SHA256 hex line and a self_pin check called before
                           any other action
  seal-no-replace-objects  GIT_NO_REPLACE_OBJECTS in the environment handed to git
  seal-scrubbed-config     GIT_CONFIG_GLOBAL / GIT_CONFIG_NOSYSTEM in that environment
  refuse-replace-refs      a `git replace -l` read whose non-empty output refuses
  pinned-spec              a spec blob digest comparison. Two admitted forms: a
                           hand-copied SPEC_SHA (round 92) and a digest derived from
                           git objects and compared against the committed pins.json
                           (round 93, which removes the hand-copied constant)
  header-named-verdict     the verdict column is located by header name. Two admitted
                           forms: `"verdict" in low` and a comparison over the
                           enumerated header cells
  refuse-out-of-set-ids    an id outside the spec's set refuses, reported as
                           `out-of-set:`. The shape-keyed form (round 91/92, an
                           `ID_SHAPE` regex used to decide what to key) is NOT
                           admitted as its own alternative: QUALITY 154 retired it
                           after it refused an honest note, and the content-keyed
                           form reaches the same finding
  refuse-unkeyed-verdict   a verdict token outside the one verdict table refuses,
                           reported as `unkeyed:` (round 91/92) or
                           `stray-verdict:` (round 93, where the rule is stated
                           once, outside the table, instead of per-row)
"""
import json
import re
import sys

DEFENCES = [
    ("self-pin", [[r'SELF_SHA256\s*=\s*"[0-9a-f]{64}"', r"def self_pin", r"self_pin_ok\(\)"]]),
    ("seal-no-replace-objects", [[r"GIT_NO_REPLACE_OBJECTS"]]),
    ("seal-scrubbed-config", [[r"GIT_CONFIG_NOSYSTEM", r"GIT_CONFIG_GLOBAL"]]),
    ("refuse-replace-refs", [[r'"replace",\s*"-l"', r"replace-refs-present"]]),
    ("pinned-spec", [[r"SPEC_SHA\s*=", r"sha256\(spec_bytes\)"],
                     [r'"spec_sha256"', r"sha256\(spec_bytes\)"]]),
    ("header-named-verdict", [[r'"verdict"\s+in\s+low'], [r'==\s*"verdict"']]),
    ("refuse-out-of-set-ids", [[r"out-of-set:"]]),
    ("refuse-unkeyed-verdict", [[r"unkeyed:"], [r"stray-verdict:"]]),
]


def check(path):
    text = open(path, encoding="utf-8").read()
    found, missing = {}, []
    for name, alts in DEFENCES:
        hit = any(all(re.search(p, text) for p in alt) for alt in alts)
        found[name] = hit
        if not hit:
            missing.append(name)
    return found, missing


def main(argv):
    if len(argv) < 2:
        sys.stderr.write(__doc__)
        return 64
    found, missing = check(argv[1])
    if "--json" in argv:
        print(json.dumps({"file": argv[1], "defences": found, "missing": missing}, indent=1))
    else:
        print("HARDENING file=%s defences=%d/%d missing=%s" % (
            argv[1], len(found) - len(missing), len(found), ",".join(missing) or "-"))
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
