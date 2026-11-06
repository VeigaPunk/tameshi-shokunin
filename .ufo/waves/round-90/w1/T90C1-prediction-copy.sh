#!/usr/bin/env bash
# T90C1 — attack R90-C1 under the plan's kill rule (a):
# build the cheapest committed lane state that reaches C1_R90_PASS=true
# WITHOUT performing the measurement the claim names ("a reproducible
# mutation case ... measured under its own selftest mode").
#
# State built (clone of the lane at the freeze commit, fixture identity):
#   * corpus/knowledge/mutation-case-fleet-sources-census.md — a table whose
#     12 verdict cells are copied MECHANICALLY from the pre-registered
#     predictions receipt (pre-freeze/expected.tsv, committed at dd0ddce9,
#     three commits before the freeze). The note says so in prose and states
#     that no mutant was executed. No witness, arm, edit or survivor table.
#   * corpus/SOURCES.md — one appended row S316, `mined`, used-by = the note,
#     for a URL that was never opened (example.invalid).
#   * corpus/README.md — one line starting with `|` that names the note.
# Then run the frozen counter exactly as the plan commands it.
#
# Probe B (same clone, second commit): add the survivor table the plan says
# the case note must carry (per-survivor rows keyed by the mutant id with a
# verdict cell). Expected effect: the note parser counts two verdict rows per
# id -> ids=false, so the HONEST note shape the plan describes is refused.
#
# No writes outside the scratch dir and the fixture clone.
set -euo pipefail
SEAT=T90C1
ROOT=/home/vgpnk/Projects/shokunin/tameshi-shokunin
FREEZE=3485ceb08df394edf5fbe26bd09b03985a04fba1
S=/fast/scratch/hyaku/tameshi-r90/$SEAT
trap 'rm -rf -- "$S"' EXIT
mkdir -p "$S"
D=$(mktemp -d -p "$S" fx.XXXXXX)
REPO=$D/repo
git clone -q --shared --no-checkout "$ROOT" "$REPO"
[ "$(git -C "$REPO" rev-parse --show-toplevel)" = "$(realpath "$REPO")" ] || { echo "TOPLEVEL-MISMATCH"; exit 1; }
git -C "$REPO" checkout -q -B probe "$FREEZE"
git -C "$REPO" config user.name ctl
git -C "$REPO" config user.email ctl@fixture.invalid

python3 - "$REPO" <<'PY'
import os, sys
repo = sys.argv[1]
tsv = open(os.path.join(repo, ".ufo/evidence/round-90/pre-freeze/expected.tsv"), encoding="utf-8").read().splitlines()
rows = [tuple(l.split("\t")[1:3]) for l in tsv if l.startswith("predict\t")]
assert len(rows) == 12, rows
killed = sum(v == "KILLED" for _, v in rows)
note = [
    "# Mutation case — fleet registry gate (probe)",
    "",
    "This table was generated mechanically from the pre-registered prediction",
    "receipt `.ufo/evidence/round-90/pre-freeze/expected.tsv`. No mutant was",
    "executed for it; no witness, arm, edit or survivor table is recorded here.",
    "",
    "| mutant | verdict |",
    "|---|---|",
]
note += ["| %s | %s |" % (i, v) for i, v in rows]
note += ["", "measured: %d/%d killed" % (killed, len(rows)), "", "source: S316", ""]
open(os.path.join(repo, "corpus/knowledge/mutation-case-fleet-sources-census.md"), "w", encoding="utf-8").write("\n".join(note))

src = os.path.join(repo, "corpus/SOURCES.md")
lines = open(src, encoding="utf-8").read().split("\n")
row = ("| S316 | Probe source — https://probe.invalid/never-opened | docs | B | probe | "
       "§1 | a row written only to satisfy the counter's source conjunct | mined | 2026-11-06 | "
       "90d | corpus/knowledge/mutation-case-fleet-sources-census.md |")
i = lines.index("## Paths")
lines[i:i] = [row]
open(src, "w", encoding="utf-8").write("\n".join(lines))

with open(os.path.join(repo, "corpus/README.md"), "a", encoding="utf-8") as f:
    f.write("\n## Probe\n\n| Note | Scope |\n|---|---|\n| `knowledge/mutation-case-fleet-sources-census.md` | probe row |\n")
print("NOTE_ROWS", len(rows), "KILLED", killed)
PY

git -C "$REPO" add -A
git -C "$REPO" -c user.name=ctl -c user.email=ctl@fixture.invalid commit -qm "probe A: prediction-copy note, unopened source, README row"
echo "PROBE_A_REV $(git -C "$REPO" rev-parse HEAD)"
git -C "$REPO" show --stat --format='PROBE_A_DIFF %H %s' HEAD
git -C "$REPO" show HEAD:corpus/knowledge/mutation-case-fleet-sources-census.md
W=$(mktemp -d -p "$S" workA.XXXXXX)
python3 -I "$ROOT/.ufo/evidence/round-90/c1/measure.py" --repo "$REPO" --rev HEAD --work "$W" || rc=$?
echo "PROBE_A_EXIT=${rc:-0}"

# Probe B: add the survivor table the plan requires (witness + drafted killing arm).
python3 - "$REPO" <<'PY'
import os, sys
p = os.path.join(sys.argv[1], "corpus/knowledge/mutation-case-fleet-sources-census.md")
t = open(p, encoding="utf-8").read()
t += """
## Survivors

| id | witness | drafted killing arm | verdict |
|---|---|---|---|
| C02 | thin-reject boundary | 7-char rejection row | SURVIVED |
| C03 | supersedes id width | 4-digit supersedes row | SURVIVED |
| C06 | separator alignment colons | aligned separator fixture | SURVIVED |
| C08 | used-by is a directory | directory used-by fixture | SURVIVED |
| C09 | URL fragment normalization | fragment-differing pair | SURVIVED |
| C10 | symbolic cadence with a space | spaced cadence fixture | SURVIVED |
| C12 | used-by comma list trim | two-path used-by row | SURVIVED |
"""
open(p, "w", encoding="utf-8").write(t)
PY
git -C "$REPO" add -A
git -C "$REPO" -c user.name=ctl -c user.email=ctl@fixture.invalid commit -qm "probe B: survivor table keyed by mutant id"
echo "PROBE_B_REV $(git -C "$REPO" rev-parse HEAD)"
W2=$(mktemp -d -p "$S" workB.XXXXXX)
rc=0
python3 -I "$ROOT/.ufo/evidence/round-90/c1/measure.py" --repo "$REPO" --rev HEAD --work "$W2" || rc=$?
echo "PROBE_B_EXIT=$rc"
