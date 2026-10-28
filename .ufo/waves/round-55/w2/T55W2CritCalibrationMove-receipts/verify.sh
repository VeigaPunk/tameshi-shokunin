#!/bin/bash
# T55W2CritCalibrationMove -- independent re-derivation of the ten corrections at C0.
# Deliberately NOT the counter's code: each fact is recomputed with a different
# expression, then compared to what `## Round 55 - round-54 record corrections` states.
#   verify.sh LANE C0
set -u
L=$1; R=$2
say () { printf '%-6s %-46s %s\n' "$1" "$2" "$3"; }
sha () { git -C "$L" show "$R:$1" | sha256sum | cut -d' ' -f1; }

CORR=$(git -C "$L" show "$R:SCORECARD.md" | awk '/^## Round 55 - round-54 record corrections/{f=1;next} f')
has () { printf '%s' "$CORR" | grep -qF -- "$1" && echo present || echo ABSENT; }

# R54.1 controls-b: 2 of 3, one CTL_MISMATCH
CB=$(git -C "$L" show "$R:.ufo/evidence/round-54/control/controls-b.stdout")
say R54.1 "controls-b CTL_MISMATCH count / verdict" \
  "$(printf '%s\n' "$CB" | grep -c '^CTL_MISMATCH') / $(printf '%s\n' "$CB" | grep -o '^CONTROLS_B: [0-9]*/[0-9]*')"
say R54.1 "corrections state CTL_MISMATCH + 2/3" "$(has CTL_MISMATCH),$(has '2/3')"

# R54.2 frozen.stdout names one pointer
FP=$(git -C "$L" show "$R:.ufo/evidence/round-54/after/frozen.stdout" | grep -o 'freeze=[0-9a-f]\{40\}' | cut -d= -f2 | sort -u)
say R54.2 "frozen.stdout pointer(s)" "$FP len=$(printf '%s' "$FP" | wc -l)"
say R54.2 "corrections state 077d431e" "$(has 077d431e)"

# R54.3 receipt total
T=$(git -C "$L" show "$R:.ufo/evidence/round-54/before/c2.stdout" | grep -o 'C2_R54_PASS=[a-z]*' | head -1)
TL=$(git -C "$L" show "$R:.ufo/evidence/round-54/before/c2.stdout" | tr ' ' '\n' | grep '^total=' | head -1)
say R54.3 "receipt verdict token / total" "$T / $TL"
say R54.3 "corrections state total=13" "$(has 'total=13')"

# R54.4 the digest, derived from the bytes at the FREEZE commit (not from freeze.json)
D=$(sha .ufo/evidence/round-54/c2/measure.py)
STORED=$(git -C "$L" show "$R:.ufo/evidence/round-54/freeze.json" | python3 -c 'import json,sys;print(json.load(sys.stdin)["files"]["c2/measure.py"])')
say R54.4 "sha256 of c2/measure.py at C0 vs freeze.json" "${D:0:8} vs ${STORED:0:8} equal=$([ "$D" = "$STORED" ] && echo yes || echo no)"
say R54.4 "corrections state 8528ee85" "$(has 8528ee85)"

# R54.5 findings recounted with jq-free python, different traversal than the counter
read -r W1 N1 F1 <<<"$(python3 - "$L" "$R" <<'PY'
import json, subprocess, sys
L, R = sys.argv[1], sys.argv[2]
def ls(p): return subprocess.run(["git","-C",L,"ls-tree","-r","--name-only",R,"--",p],
                                 capture_output=True,text=True).stdout.split()
out=[]
for w in ("w1","w2"):
    tot=files=0
    for n in ls(".ufo/waves/round-54/"+w):
        if "/T54W" not in n or not n.endswith(".json") or "Read" not in n: continue
        raw=subprocess.run(["git","-C",L,"show","%s:%s"%(R,n)],capture_output=True,text=True).stdout
        try: f=json.loads(raw).get("findings") or []
        except Exception: continue
        tot+=len(f); files+= 1 if f else 0
    out.append("%d"%tot); out.append("%d"%files)
print(out[0], out[1], out[2])
PY
)"
say R54.5 "recount w1/w2 findings, w2 non-empty sections" "w1=$W1 w2=$N1 sections=$F1"
say R54.5 "corrections state w1=28 w2=25 sections=12" \
  "$(printf '%s' "$CORR" | grep -o 'w1=[0-9]* w2=[0-9]* sections=[0-9]*' | head -1)"

# R54.6 / R54.7 commit ids, found by the same predicate controls.sh uses
ADD=$(git -C "$L" log -1 --format=%h --diff-filter=A "$R" -- .ufo/waves/round-54/w2/T54W2Sent03.md)
REN=$(git -C "$L" log -1 --format=%h --diff-filter=R "$R" -- .ufo/waves/round-54/w2/T54W2Sent01-receipts/forged-reader.json)
say R54.6 "add-commit of swept seat file" "$ADD (corrections: $(has "$ADD"))"
say R54.7 "rename-commit of forged reader" "$REN (corrections: $(has "$REN"))"

# R54.9 wave registry + staged receipt, and whether the live source has moved
REG=$(git -C "$L" show "$R:.ufo/waves/round-54/w1-registry.json" | python3 -c 'import json,sys;r=json.load(sys.stdin);print("reviewers=%d attack=%d/%d seats=%d"%(r["role_mix"]["reviewer"],r["attack_seats"],r["seats"],r["seats"]))')
ST=$(git -C "$L" show "$R:.ufo/evidence/round-55/c1/staged-at-freeze.txt" | grep -o 'output=[0-9]*')
LIVE=$(find /home/vgpnk/Projects/shokuknow/merge/tameshi/knowledge -name '*.md' 2>/dev/null | wc -l)
say R54.9 "registry / receipt / live shokuknow" "$REG / $ST / live=$LIVE"
say R54.9 "corrections state registry + staged=" "$(printf '%s' "$CORR" | grep -o 'reviewers=[0-9]* attack=[0-9/]* seats=[0-9]* staged=[0-9]*' | head -1)"

# R54.10 the round-53 counter's own line at 88afa941
CA=$(git -C "$L" show "$R:.ufo/evidence/round-54/control/controls-a.stdout" | grep 'CTL_R53' | tail -1)
say R54.10 "controls-a CTL_R53 line (tail 60)" "…${CA: -60}"
say R54.10 "corrections state controls-a.stdout + rekeyed=0/7 + r53-counter-at-88afa941" \
  "$(has controls-a.stdout),$(has 'rekeyed=0/7'),$(has r53-counter-at-88afa941)"
