#!/bin/bash
# T55W2RevLessonAccuracy — every finding in the seat report, re-derivable.
# Read-only against the lane: all execution happens on `git show` blobs or on a
# `git clone --shared` fixture under $HYAKU_SCRATCH. Nothing in the lane is written.
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
C0=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
PRE=631cd6455e58dce969310b4c0466c3383d9f5108      # the freeze commit before amendments 1-7
FRZ=e2979f277138da503af27b263b783f626f109be4      # the freeze pointer at C0 (7 amendments)
OUT=$(cd "$(dirname "$0")" && pwd)
SEC='## Round 55 - round-54 record corrections'
show () { git -C "$LANE" show "$1:$2"; }

echo "########## 01  S280 Gate quote word count (lesson line 11 says 17) ##########"
q1='Error messages from other noninteractive programs should look like this: program:sourcefile:lineno: message'
q2='program: message'
printf 'fragment1: %s\n' "$q1"
printf 'wc -w fragment1: '; printf '%s\n' "$q1" | wc -w
printf 'wc -w fragment2: '; printf '%s\n' "$q2" | wc -w
printf 'wc -w both quoted spans: '; printf '%s %s\n' "$q1" "$q2" | wc -w
printf 'wc -w with the 3-word section-title quote added: '; printf '%s %s Formatting Error Messages\n' "$q1" "$q2" | wc -w
printf 'snapshot sha256 (lesson quotes only the 8-hex prefixes):\n'
for f in S280-gnu-errors.txt S281-sysexits.txt; do printf '  %s ' "$f"; show "$C0" ".ufo/evidence/round-55/assimilation/$f" | sha256sum | cut -c1-64; done
printf 'fragment1 as it appears in the committed snapshot (byte-identical apart from the reflow):\n'
show "$C0" .ufo/evidence/round-55/assimilation/S280-gnu-errors.txt | sed -n '5,9p'

echo
echo "########## 02  S280 verdict ground: does the note cite S280? (lesson says it does) ##########"
printf 'grep -c S280 in corpus/knowledge/scratch-root-contract.md: '
show "$C0" corpus/knowledge/scratch-root-contract.md | grep -c "S280"
printf 'S-ids the note actually cites: '
show "$C0" corpus/knowledge/scratch-root-contract.md | grep -o "S[0-9]\{3\}" | sort -u | tr '\n' ' '; echo
printf 'http/URL references in the note: '
show "$C0" corpus/knowledge/scratch-root-contract.md | grep -c "http"
printf 'the SOURCES S280 row names this note as used-by: '
show "$C0" corpus/SOURCES.md | grep "^| S280 " | awk -F'|' '{print $12}'
printf 'census E11 checks the used-by PATH exists, not that the file cites the id: '
grep -c "E11-dangling-usedby" /home/vgpnk/Projects/shokunin/scripts/sources-census.sh

echo
echo "########## 03  freeze pointer and amendment count (lesson line 3: 631cd645 + amendments 1-4) ##########"
printf 'amendments listed in freeze.json at C0: '
show "$C0" .ufo/evidence/round-55/freeze.json | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["amendments"]))'
printf 'manifest files listed: '
show "$C0" .ufo/evidence/round-55/freeze.json | python3 -c 'import json,sys; print(len(json.load(sys.stdin)["files"]))'
printf '631cd645 is an ancestor of the C0 freeze pointer e2979f2: '; git -C "$LANE" merge-base --is-ancestor "$PRE" "$FRZ" && echo yes
echo 'frozen paths differ between the named freeze and C0 (so FROZEN_UNCHANGED would read 0):'
git -C "$LANE" diff --stat "$PRE" "$C0" -- .ufo/evidence/round-55/contract.json .ufo/evidence/round-55/freeze.json \
  .ufo/evidence/round-55/c1/measure.py .ufo/evidence/round-55/c2/measure.py .ufo/evidence/round-55/no-harm.sh \
  .ufo/evidence/round-55/deciding-run.sh .ufo/evidence/round-55/controls.sh
echo 'the gate that reads this (deciding-run.sh, frozen at C0), line 66:'
show "$C0" .ufo/evidence/round-55/deciding-run.sh | sed -n '65,66p'
printf 'control receipts committed at C0 (0 = no control scored yet, so "all pre-control" holds): '
git -C "$LANE" ls-tree -r --name-only "$C0" -- .ufo/evidence/round-55/control | wc -l
echo 'self-consistency of each freeze manifest (the gate re-hashes freeze.json at FREEZE):'
python3 - "$LANE" <<'PY'
import hashlib, json, subprocess, sys
lane = sys.argv[1]; E = ".ufo/evidence/round-55"
def blob(rev, path):
    r = subprocess.run(["git","-C",lane,"show","%s:%s"%(rev,path)], capture_output=True)
    return r.stdout if r.returncode == 0 else None
for rev in ("631cd6455e58dce969310b4c0466c3383d9f5108",
            "e2979f277138da503af27b263b783f626f109be4",
            "9cf0146b94ddba12d454ebf7288ce6e5c5d535bb"):
    fr = json.loads(blob(rev, E + "/freeze.json")); bad = []
    for rel, want in fr["files"].items():
        p = rel if rel.startswith(".ufo/") else "%s/%s" % (E, rel)
        b = blob(rev, p)
        if (hashlib.sha256(b).hexdigest() if b is not None else None) != want: bad.append(rel)
    print("  freeze rev=%s amendments=%d files=%d integrity=%s %s"
          % (rev[:12], len(fr["amendments"]), len(fr["files"]), "OK" if not bad else "MISMATCH", bad))
PY

echo
echo "########## 04  QUALITY 106 and the claimed 105 erratum ##########"
printf 'last criterion heading in corpus/QUALITY.md at C0: '
show "$C0" corpus/QUALITY.md | grep -E "^### Criterion" | tail -1
printf 'Criterion 106 in corpus/QUALITY.md at C0: '
show "$C0" corpus/QUALITY.md | grep -c "^### Criterion 106"
printf 'files in the tree at C0 that carry a "### Criterion 106" heading (drafts, not the record): '
echo
git -C "$LANE" grep -l "^### Criterion 106" "$C0" -- '*.md' | sed 's/^/  /'
printf 'any "erratum" heading attached to criterion 105: '
show "$C0" corpus/QUALITY.md | sed -n '/^### Criterion 105/,/^## /p' | grep -c -i "erratum"
echo 'the 105 falsifier as committed (rewritten in place, tagged [ER-R54-1]):'
show "$C0" corpus/QUALITY.md | sed -n '/^### Criterion 105/,/^## /p' | grep -n "rekeyed=3/7\|ER-R54-1"
echo 'the same false claim in LOG.md at C0:'
show "$C0" LOG.md | grep -n "QUALITY 106"
echo 'and the wave-1 seat that had already reported it before C0 landed:'
show "$C0" .ufo/waves/round-55/w1/T55W1ScribeLog.md | sed -n '221,226p'

echo
echo "########## 05  R54.2: lesson says "the two stale ids"; the routed defect names three ##########"
echo 'spotcheck R54.2 heading and body:'
show "$C0" corpus/lessons/round-54-verifier-spotcheck.md | grep -n "R54.2" | head -3
show "$C0" corpus/lessons/round-54-verifier-spotcheck.md | sed -n '110p'
echo 'the corrections section quotes all three:'
show "$C0" SCORECARD.md | sed -n "/^$SEC/,/^## /p" | grep -n "7883e0e5\|fe70474d\|097985c1"
echo 'the C1 counter stale scan watches only two (c1/measure.py, R54.2 class):'
show "$C0" .ufo/evidence/round-55/c1/measure.py | sed -n '212p'

echo
echo "########## 06  "no prior round had a dry run before the controls" ##########"
echo 'round-54 freeze.json amendment 1:'
show "$C0" .ufo/evidence/round-54/freeze.json | python3 -c 'import json,sys
for a in json.load(sys.stdin)["amendments"]:
    if a["n"]==1: print(a["what"])'

echo
echo "########## 07  mistake 2 mechanism, reproduced on the C0 bytes ##########"
python3 - "$LANE" "$C0" "$PRE" <<'PY'
import subprocess, sys
lane, c0, pre = sys.argv[1:4]
def show(rev, path):
    return subprocess.run(["git","-C",lane,"show","%s:%s"%(rev,path)],capture_output=True,text=True).stdout
MARKER="could-not-evaluate: cannot create clone scratch under the scratch root"
skill=show(c0,"SKILL.md")
print("SKILL.md at C0, correct edit present (whitespace-normalised):", MARKER in " ".join(skill.split()))
print("SKILL.md at C0, raw match (the pre-amendment arm's comparison):", MARKER in skill, "-> skill arm =",
      1 if MARKER in skill else 0, "/1")
lines=skill.splitlines()
for n,l in enumerate(lines,1):
    if "cannot create clone scratch under the scratch" in l:
        print("the marker is split here: line %d width %d -> line %d width %d" % (n,len(l),n+1,len(lines[n])))
        print("  line %d: %r" % (n, l[-30:]))
        print("  line %d: %r" % (n+1, lines[n][:40]))
note=" ".join(show(c0,"corpus/knowledge/scratch-root-contract.md").split())
seven=["env-diff","repeat-control","registry-check","bash-witness-study","pin-disposition","evidence-disposition","context-capture"]
old=["%s --selftest"%t for t in seven]+["env-diff --contract"]
new=[("bash-witness-study selftest" if t=="bash-witness-study" else "%s --selftest"%t) for t in seven]+["env-diff --contract"]
print("pre-amendment counter labels every selftest '--selftest' (blob %s):"%pre)
print("   ", subprocess.run(["git","-C",lane,"show","%s:.ufo/evidence/round-55/c2/measure.py"%pre],
      capture_output=True,text=True).stdout.splitlines()[89])
print("note arm with the OLD labels:", sum(1 for m in old if m in note), "/", len(old),
      "missing:", [m for m in old if m not in note])
print("note arm with the labels as invoked:", sum(1 for m in new if m in note), "/", len(new))
PY

echo
echo "########## 08  R54.5 counts re-derived ##########"
python3 - "$LANE" "$C0" <<'PY'
import json,subprocess,sys,re
lane,rev=sys.argv[1:3]
def tree(p):
    r=subprocess.run(["git","-C",lane,"ls-tree","-r","--name-only",rev,"--",p],capture_output=True,text=True)
    return r.stdout.split()
for wave in ("w1","w2"):
    names=[n for n in tree(".ufo/waves/round-54/%s"%wave) if re.search(r"/T54W\d+[A-Za-z]*Read\d+\.json$",n)]
    tot=files=0
    for n in names:
        b=subprocess.run(["git","-C",lane,"show","%s:%s"%(rev,n)],capture_output=True,text=True).stdout
        try: d=json.loads(b)
        except Exception: continue
        k=len(d.get("findings") or []); tot+=k; files+= 1 if k else 0
    print("%s reader_files=%d findings=%d files_with_findings=%d"%(wave,len(names),tot,files))
PY

echo
echo "########## 09  R54.6 / R54.7 / R54.9 / R54.10 / R54.3 / R54.4 receipts ##########"
printf 'commit that added T54W2Sent03.md: '; git -C "$LANE" log --format=%h --diff-filter=A -- .ufo/waves/round-54/w2/T54W2Sent03.md | head -1
printf 'rename record at 7fa9a5e: '; git -C "$LANE" show --name-status --format='' 7fa9a5e | grep -i forged-reader | head -1
printf 'SUPERSEDED marker in the round-54 seat file: '; show "$C0" .ufo/waves/round-54/w1/T54W1ExecStraceNoise.md | grep -c "SUPERSEDED (round 55"
printf 'history.db row 690: '; python3 -c "
import sqlite3;c=sqlite3.connect('file:/home/vgpnk/.omp/agent/history.db?mode=ro',uri=True)
r=c.execute('select prompt,created_at from history where id=690').fetchone();print(r[0],'| epoch',r[1])"
printf 'round-54 w1-registry reviewer/attack/seats: '; show "$C0" .ufo/waves/round-54/w1-registry.json | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d["role_mix"]["reviewer"],d["attack_seats"],d["seats"])'
printf 'staged receipt: '; show "$C0" .ufo/evidence/round-55/c1/staged-at-freeze.txt | grep -E "^output="
printf 'controls-a CTL_R53 rekey: '; show "$C0" .ufo/evidence/round-54/control/controls-a.stdout | grep -o "CTL_R53.*rekeyed=[0-9]*/[0-9]*" | grep -o "rekeyed=[0-9]*/[0-9]*"
printf 'r53-counter-at-88afa941 rekey: '; show "$C0" .ufo/evidence/round-54/control/r53-counter-at-88afa941.stdout | grep -o "rekeyed=0/30" | head -1
printf 'round-54 before/c2 total: '; show "$C0" .ufo/evidence/round-54/before/c2.stdout | grep -o "total=[0-9]*" | tail -1
printf 'round-54 freeze.json c2/measure.py digest: '; show "$C0" .ufo/evidence/round-54/freeze.json | python3 -c 'import json,sys;print(json.load(sys.stdin)["files"]["c2/measure.py"])'
printf 'round-54 controls-b verdict lines: '; show "$C0" .ufo/evidence/round-54/control/controls-b.stdout | grep -E "CTL_MISMATCH|CONTROLS_B" | tr '\n' ' '; echo

echo
echo "########## 10  census: 140 rows and exit 0; the duplicate code for a within-scope URL ##########"
printf 'rows by the lesson own pattern: '; show "$C0" corpus/SOURCES.md | grep -cE '^ {0,3}\| S[0-9]{3,} \|'
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi >/dev/null 2>&1; echo "validate exit=$?"
echo 'CORPUS.md rule 2 (the lesson cites it for a duplicate URL):'
sed -n '116,118p' /home/vgpnk/Projects/shokunin/CORPUS.md
echo 'census code table: inside scope = E04, across scopes = W04:'
grep -n "E04 duplicate URL+scope\|W04 same URL across scopes" /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r55/T55W2RevLessonAccuracy/receipts-fixture
rm -rf "$S"; mkdir -p "$S/tameshi-shokunin"; trap 'rm -rf -- "$S"' EXIT
git -C "$LANE" archive "$C0" | tar -x -C "$S/tameshi-shokunin"
python3 - "$S/tameshi-shokunin" <<'PY'
import sys, pathlib
p=pathlib.Path(sys.argv[1])/"corpus/SOURCES.md"; out=[]
row=("| S281 | sysexits(3) duplicate candidate — https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3 | docs | A | "
     "BSD exit-status conventions for command-line programs; legacy and deprecated by its own text | §DESCRIPTION @ FreeBSD 15.1 | "
     "the interface is deprecated and retained for compatibility | queued | 2026-10-28 | 730d | — |\n")
for l in p.read_text().splitlines(True):
    out.append(l)
    if l.startswith("| S090 |"): out.append(row)
p.write_text("".join(out))
PY
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root "$S" "$S/tameshi-shokunin" 2>&1 | grep -E "S281"

echo
echo "########## 11  cannot_see claim 2, executed on the C0 counter bytes ##########"
D=$S/lane-fixture; git clone --shared --quiet "$LANE" "$D"
git -C "$D" checkout -q -B rev "$C0"
test "$(git -C "$D" rev-parse --show-toplevel)" = "$D" && echo "fixture toplevel ok: $D"
python3 - "$D" <<'PY'
import sys, pathlib
p=pathlib.Path(sys.argv[1])/"SCORECARD.md"; body=p.read_text()
head="## Round 55 - round-54 record corrections"
i=body.index(head)
plant_in="\nFixture plant (inside the block): `CTL_POS_c1 true` — the assertion the receipt refutes.\n"
j=body.find("\n## ", i+len(head))
body = (body[:j]+plant_in+body[j:]) if j!=-1 else (body.rstrip("\n")+"\n"+plant_in)
body += "\n## Fixture outside (not a corrections block)\n\nRound 54's phase-B positive control passed as pre-registered, and the sweep is complete.\n"
p.write_text(body)
PY
GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 git -C "$D" -c user.name=fix -c user.email=fix@invalid commit -qam "fixture"
mkdir -p "$S/work"; git -C "$LANE" show "$C0:.ufo/evidence/round-55/c1/measure.py" > "$S/c1.py"
python3 "$S/c1.py" --lane "$D" --rev "$(git -C "$D" rev-parse HEAD)" --work "$S/work"; echo "exit=$?"

echo
echo "########## 12  lazy-mode failing-input probes scheduled? ##########"
python3 - <<'PY'
import json
d=json.load(open("/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-55/spec-w2.json"))
lazy=["repeat-control --snapshot","pin-disposition --read","evidence-disposition --json","context-capture --check","bash-witness-study count"]
print("wave-2 items:", len(d["items"]), "(spec-w2.json is NOT committed at C0; git ls-tree shows none)")
for it in d["items"]:
    s=json.dumps(it)
    if any(m in s for m in lazy): print("item naming a lazy mode:", it.get("name"))
print("items containing 'failing input':",
      sum(1 for it in d["items"] if "failing input" in json.dumps(it).lower()))
for it in d["items"]:
    if "lazy" in json.dumps(it).lower():
        print("  lazy mention:", it.get("name"), "->", (it.get("item") or it.get("task") or "")[:110].replace("\n"," "))
PY

echo
echo "########## 13  residual: the fleet round-54 report at C0 ##########"
R=/home/vgpnk/Projects/shokunin/.ufo/reports/round-54/tameshi.md
printf '%s still carries 49280fe5 x' ; grep -c "49280fe5" "$R"
printf '%s still carries 097985c1 x' ; grep -c "097985c1" "$R"
echo "(lane path .ufo/reports/round-54/tameshi.md does not exist in the lane: the report is a fleet file)"

echo
echo "########## 14  the live GNU page: is the no-period sentence there, and where? ##########"
if curl -sS --max-time 25 https://www.gnu.org/prep/standards/html_node/Errors.html -o /tmp/t55w2-gnu-errors.html; then
  python3 - <<'PY'
import re, html
t = open("/tmp/t55w2-gnu-errors.html", encoding="utf-8", errors="replace").read()
t = re.sub(r"<[^>]+>", " ", t); t = html.unescape(t); t = re.sub(r"\s+", " ", t)
i = t.find("should not begin with a capital letter")
print("live page:", t[i-80:i+330].strip() if i > 0 else "capital-letter sentence NOT FOUND")
print("committed snapshot contains 'Also, it should not end with a period.':")
PY
  git -C "$LANE" show "$C0:.ufo/evidence/round-55/assimilation/S280-gnu-errors.txt" | grep -c "Also, it should not end with a period" || true
else
  echo "network unavailable: live-page check skipped (the snapshot-side finding in F10 stands on section 01)"
fi

echo
echo "########## 15  what the deciding gate accepts from the control receipts ##########"
echo 'gate lines that decide whether a control receipt passes (verdict regex + commit order):'
git -C "$LANE" show "$C0:.ufo/evidence/round-55/deciding-run.sh" | sed -n '46,55p' | sed 's/^/  /'
echo 'round 54 was refused nowhere: its receipt line is the shape the regex above accepts:'
git -C "$LANE" show "$C0:.ufo/evidence/round-54/control/controls-b.stdout" | grep -E "^CONTROLS_B:"
python3 - <<'PY'
import re
accept = re.compile(r'^CONTROLS_B: [0-9]*/[0-9]* as pre-registered')
for line in ("CONTROLS_B: 3/3 as pre-registered", "CONTROLS_B: 2/3 as pre-registered"):
    print("  accepts %-40r -> %s" % (line, bool(accept.match(line))))
PY
echo 'and phase B in the round-55 controls clones the caller argv, with no check of what it certifies:'
git -C "$LANE" show "$C0:.ufo/evidence/round-55/controls.sh" | sed -n '119,123p' | sed 's/^/  /'
