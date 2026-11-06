#!/usr/bin/env python3
"""T88M1 — two controls shaped like the round-88 after-state (candidate runner at
28ec5885), for the two counter checks no pre-freeze control can drive to
C1_R88_PASS=true.

usage: T88M1-make-round88-shape.py <candidate-runner> <out> (dup11|inert) <blob.sh>

dup11  M3 (duplicate-target) funder: the declared count stays 11 but one distinct
       leg (bash-drift-pins) is replaced by a re-declaration of js-kimi-census
       under a new name. Frozen counter: duplicate-target -> legs=10. With the
       duplicate check dropped: 11 counted legs including the pre-registered
       Python leg -> C1_R88_PASS=true.

inert  M6 (killed>=1) funder: bash-drift-pins keeps its pin and allow-listed
       suite, but its embedded spec is ten comment-only (behaviourally inert)
       edits of the pinned blob and its table reads all SURVIVED. The runner
       passes it (killed-delta 0, flips 0); the frozen counter refuses it with
       reason=no-kill. With `killed >= 1` dropped it counts -> 11 counted legs
       with the pre-registered Python leg -> C1_R88_PASS=true.

Both start from the candidate runner bytes (git cat-file blob 28ec5885:tools/mutate-and-run.sh)
so the counter sees the real after-state shape, not a base-runner forgery.
"""
import re
import sys
from pathlib import Path

DRIFT_LEG = """  regression_case_git bash-drift-pins \\
    'kagi-shokunin/corpus/drift-pins.sh' "$PIN_DRIFTPINS" "$REV_DRIFTPINS" \\
    "$specs/bash-drift-pins.spec" 'h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C bash "$MUTANT" --selftest' "$TABLE_DRIFTPINS" \\
    "$root/bash-drift-pins"
"""
DUP_LEG = """  regression_case_git js-kimi-census-again \\
    'kumitate-shokunin/scripts/kimi-census.mjs' "$PIN_JS" "$REV_JS" \\
    "$specs/js-kimi-census.spec" 'node "$MUTANT" --selftest' "$TABLE_JS" \\
    "$root/js-kimi-census-again"
"""
OLD_TABLE = ("TABLE_DRIFTPINS='K_MODE_CMP:KILLED,K_GONE_ARM:SURVIVED,K_AMBIG_GT:SURVIVED,"
             "K_COUNT_GE:KILLED,K_SHAPE_OPTIN:SURVIVED,S_SHA_CMP:SURVIVED,S_HARDLINK:SURVIVED,"
             "S_POLICY:SURVIVED,S_DUP_UNIQ:SURVIVED,S_USAGE_EXIT:SURVIVED'")
SPEC_START = '  cat >"$d/bash-drift-pins.spec" <<\'EOT\'\n'


def once(t, old, new):
    assert t.count(old) == 1, "anchor count=%d for %r" % (t.count(old), old[:70])
    return t.replace(old, new, 1)


def pick_anchors(blob: str, n: int = 10) -> list[str]:
    """Ten full-line comments whose exact text occurs once in the blob."""
    out = []
    for line in blob.split("\n"):
        s = line.strip()
        if not s.startswith("#") or len(s) < 24:
            continue
        if blob.count(line) != 1 or "\\" in line:
            continue
        out.append(line)
        if len(out) == n:
            return out
    raise SystemExit("only %d unique comment anchors" % len(out))


def main() -> int:
    cand, out, variant = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
    t = cand.read_text()
    if variant == "dup11":
        t = once(t, DRIFT_LEG, DUP_LEG)
    elif variant == "inert":
        blob = Path(sys.argv[4]).read_text()
        anchors = pick_anchors(blob)
        ids = ["I%02d" % (i + 1) for i in range(len(anchors))]
        spec = "".join("@defect %s | inert comment-only edit\n@old %s\n@new %s \n\n"
                       % (i, a, a) for i, a in zip(ids, anchors))
        # drop the final blank line so the heredoc body stays well formed
        spec = spec.rstrip("\n") + "\n"
        start = t.index(SPEC_START) + len(SPEC_START)
        end = t.index("\nEOT\n", start) + 1
        t = t[:start] + spec + t[end:]
        t = once(t, OLD_TABLE, "TABLE_DRIFTPINS='%s'" % ",".join("%s:SURVIVED" % i for i in ids))
        print("inert anchors:", len(anchors))
        for a in anchors:
            print("   @old %s" % a)
    else:
        raise SystemExit("unknown variant " + variant)
    legs = len(re.findall(r"^  regression_case_git \S+ \\$", t, re.M))
    print("declared legs=%d" % legs)
    assert legs == 11, legs
    out.write_text(t)
    print("wrote %s (%s) bytes=%d" % (out, variant, len(t.encode())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
