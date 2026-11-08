#!/usr/bin/env bash
# T91S1 — census row-shape probe for a prospective S318 row (round 91).
#
# The S318 row does not exist in the lane yet (corpus/SOURCES.md tops out at
# S317, 177 rows). This probe answers, against the real fleet gate
# (scripts/sources-census.sh), what the gate says about the shape a new
# S318 row must have so that it does not turn the lane's census red.
#
# READ-ONLY on the lane and on the fleet: every mutated copy lives under
# $S (a scratch dir). The gate is never pointed at the real lane file.
#
# Usage: bash T91S1-census-row-shape.sh

set -euo pipefail

LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
FLEET=/home/vgpnk/Projects/shokunin
GATE="$FLEET/scripts/sources-census.sh"
S="${T91S1_SCRATCH:-/fast/scratch/hyaku/tameshi-r91/T91S1}"
mkdir -p "$S"
trap 'rm -rf -- "$S"' EXIT

run_case() {  # $1 = label, $2 = file
  echo "--- $1 ---"
  out=$("$GATE" validate --today 2026-11-08 --file "$2" tameshi 2>&1 || true)
  printf '%s\n' "$out" | grep "S318" || echo "(no S318 finding)"
  "$GATE" validate --today 2026-11-08 --file "$2" tameshi >/dev/null 2>&1 && echo "exit=0" || echo "exit=1"
}

# --- case A: distinct scope column (the shape the L1 should use) -----------
rm -rf "$S/a"; mkdir -p "$S/a"
cp -r "$LANE/corpus" "$S/a/corpus"; cp -r "$LANE/tools" "$S/a/tools"
python3 - "$S/a/corpus/SOURCES.md" <<'PY'
import sys
p = sys.argv[1]
src = open(p, encoding="utf-8").read()
row = ("| S318 | git(1): GIT_NO_REPLACE_OBJECTS and replacement refs (Git 2.56.0 docs) "
       "— https://git-scm.com/docs/git | docs | A | "
       "the `GIT_NO_REPLACE_OBJECTS` environment variable and the `--no-replace-objects` "
       "option: what they make Git do about replacement refs | "
       "ENVIRONMENT VARIABLES, the GIT_NO_REPLACE_OBJECTS entry (tag-stripped snapshot line "
       "1414-1415) @ page fetched 2026-11-08 | "
       "\"Setting and exporting this environment variable tells Git to ignore replacement refs "
       "and do not replace Git objects.\" (18 words) | "
       "mined | 2026-11-08 | 365d | corpus/knowledge/mutation-case-fleet-sources-census.md |")
lines = src.split("\n")
i = max(i for i, l in enumerate(lines) if l.startswith("| S3"))
lines.insert(i + 1, row)
open(p, "w", encoding="utf-8").write("\n".join(lines))
PY
run_case "A: distinct scope column" "$S/a/corpus/SOURCES.md"

# --- case B: scope column byte-identical to S063's -------------------------
rm -rf "$S/b"; mkdir -p "$S/b"
cp -r "$LANE/corpus" "$S/b/corpus"; cp -r "$LANE/tools" "$S/b/tools"
python3 - "$S/b/corpus/SOURCES.md" <<'PY'
import sys
p = sys.argv[1]
src = open(p, encoding="utf-8").read()
s063 = [l for l in src.split("\n") if l.startswith("| S063 ")][0]
scope63 = s063.split("|")[5].strip()
row = ("| S318 | git(1): GIT_NO_REPLACE_OBJECTS (Git 2.56.0 docs) "
       "— https://git-scm.com/docs/git | docs | A | " + scope63 + " | "
       "ENVIRONMENT VARIABLES @ page fetched 2026-11-08 | "
       "\"Setting and exporting this environment variable tells Git to ignore replacement refs "
       "and do not replace Git objects.\" | "
       "mined | 2026-11-08 | 365d | corpus/knowledge/mutation-case-fleet-sources-census.md |")
lines = src.split("\n")
i = max(i for i, l in enumerate(lines) if l.startswith("| S3"))
lines.insert(i + 1, row)
open(p, "w", encoding="utf-8").write("\n".join(lines))
print("scope63 =", scope63)
PY
run_case "B: scope column identical to S063 (E04)" "$S/b/corpus/SOURCES.md"

# --- case C: same as B but teaches says supersedes S063 --------------------
rm -rf "$S/c"; mkdir -p "$S/c"
cp -r "$LANE/corpus" "$S/c/corpus"; cp -r "$LANE/tools" "$S/c/tools"
python3 - "$S/c/corpus/SOURCES.md" <<'PY'
import sys
p = sys.argv[1]
src = open(p, encoding="utf-8").read()
s063 = [l for l in src.split("\n") if l.startswith("| S063 ")][0]
scope63 = s063.split("|")[5].strip()
row = ("| S318 | git(1): GIT_NO_REPLACE_OBJECTS (Git 2.56.0 docs) "
       "— https://git-scm.com/docs/git | docs | A | " + scope63 + " | "
       "ENVIRONMENT VARIABLES @ page fetched 2026-11-08 | "
       "supersedes S063: \"Setting and exporting this environment variable tells Git to ignore "
       "replacement refs and do not replace Git objects.\" | "
       "mined | 2026-11-08 | 365d | corpus/knowledge/mutation-case-fleet-sources-census.md |")
lines = src.split("\n")
i = max(i for i, l in enumerate(lines) if l.startswith("| S3"))
lines.insert(i + 1, row)
open(p, "w", encoding="utf-8").write("\n".join(lines))
PY
run_case "C: identical scope + 'supersedes S063' in teaches" "$S/c/corpus/SOURCES.md"

# --- case D: used-by names corpus/lessons/round-91.md, which does not exist
rm -rf "$S/d"; mkdir -p "$S/d"
cp -r "$LANE/corpus" "$S/d/corpus"; cp -r "$LANE/tools" "$S/d/tools"
rm -f "$S/d/corpus/lessons/round-91.md"
python3 - "$S/d/corpus/SOURCES.md" <<'PY'
import sys
p = sys.argv[1]
src = open(p, encoding="utf-8").read()
row = ("| S318 | git(1): GIT_NO_REPLACE_OBJECTS and replacement refs (Git 2.56.0 docs) "
       "— https://git-scm.com/docs/git | docs | A | "
       "the `GIT_NO_REPLACE_OBJECTS` environment variable and the `--no-replace-objects` "
       "option: what they make Git do about replacement refs | "
       "ENVIRONMENT VARIABLES, the GIT_NO_REPLACE_OBJECTS entry (tag-stripped snapshot line "
       "1414-1415) @ page fetched 2026-11-08 | "
       "\"Setting and exporting this environment variable tells Git to ignore replacement refs "
       "and do not replace Git objects.\" (18 words) | "
       "mined | 2026-11-08 | 365d | corpus/knowledge/mutation-case-fleet-sources-census.md, "
       "corpus/lessons/round-91.md |")
lines = src.split("\n")
i = max(i for i, l in enumerate(lines) if l.startswith("| S3"))
lines.insert(i + 1, row)
open(p, "w", encoding="utf-8").write("\n".join(lines))
PY
run_case "D: used-by names a not-yet-existing lesson file (E11)" "$S/d/corpus/SOURCES.md"
