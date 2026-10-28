#!/bin/bash
# CTL_SKIP_c2 audit: build the docs-only mutant at BASE exactly as controls.sh does,
# then evaluate the counter's three documentation arms and prove no tool file moved.
set -u
S=${1:?usage: doc-arms.sh SCRATCHDIR}
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
BASE=0a2010acd1e92e4e332774050825e21bcfc7e079
d="$S/clones/skip2"; rm -rf "$d"; mkdir -p "$S/clones"
git clone --shared --quiet "$L" "$d" || exit 2
git -C "$d" -c advice.detachedHead=false checkout --quiet "$BASE" || exit 2
[ "$(git -C "$d" rev-parse --show-toplevel)" = "$(cd "$d" && pwd -P)" ] || { echo "TOPLEVEL MISMATCH"; exit 2; }
python3 - "$d" <<'PY'
import json, sys, pathlib
lane = pathlib.Path(sys.argv[1])
mark = "could-not-evaluate: cannot create clone scratch under the scratch root"
reg = json.loads((lane / "tools/registry.json").read_text())
for row in reg["rows"]:
    if row.get("scratch_root"):
        row["scratch_root"] = row["scratch_root"] + " | control: " + mark
(lane / "tools/registry.json").write_text(json.dumps(reg, indent=1) + "\n")
note = lane / "corpus/knowledge/scratch-root-contract.md"
modes = ["env-diff --selftest", "env-diff --contract", "repeat-control --selftest",
         "registry-check --selftest", "bash-witness-study selftest",
         "pin-disposition --selftest", "evidence-disposition --selftest",
         "context-capture --selftest"]
note.write_text(note.read_text() + "\n\n" + mark + "\n\n" + ", ".join(modes) + "\n")
skill = lane / "SKILL.md"
skill.write_text(skill.read_text() + "\n<!-- control: " + mark + " -->\n")
PY
GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 git -C "$d" -c user.name=ctl -c user.email=ctl@invalid commit -aqm "skip control: documentation only" || exit 2
echo "--- files changed vs BASE (the mutant must not touch tools/*.py) ---"
git -C "$d" diff --name-only "$BASE" HEAD
python3 - "$d" <<'PY'
import json,sys,pathlib
clone=pathlib.Path(sys.argv[1])
MARKER="could-not-evaluate: cannot create clone scratch under the scratch root"
SEVEN=("env-diff","repeat-control","registry-check","bash-witness-study","pin-disposition","evidence-disposition","context-capture")
reg=json.loads((clone/"tools/registry.json").read_text())
cells=[r for r in reg["rows"] if r.get("scratch_root") and any(t in " ".join(r.get("argv",[])) for t in ("tools/%s.py"%t for t in SEVEN))]
docs=sum(1 for r in cells if MARKER in r["scratch_root"])
print("docs cells=%d docs=%d/7"%(len(cells),docs))
allocating=["repeat-control --selftest","registry-check --selftest","bash-witness-study selftest","pin-disposition --selftest","evidence-disposition --selftest","context-capture --selftest","env-diff --selftest","env-diff --contract","registry-check --rev"]
note=" ".join((clone/"corpus/knowledge/scratch-root-contract.md").read_text().split())
names=[m for m in allocating if m in note]
print("note names=%d/9 missing=%s"%(len(names),[m for m in allocating if m not in note]))
skill=1 if MARKER in " ".join((clone/"SKILL.md").read_text().split()) else 0
print("skill=%d/1"%skill)
print("behavioural arms: the mutant touches no tools/*.py, so the 9 grammar / 5 lazy / 13 empty / 13 usable arms")
print("are the BASE arms already measured in c2-donothing.explain (grammar 6/9).")
PY
