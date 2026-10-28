#!/usr/bin/env bash
# T55W3R06 receipts: regenerate every observation cited in ../T55W3R06.md.
# Reads the lane only via `git -C ... cat-file/show` at C0 and runs the tools from
# a `git clone --shared` of the lane checked out at C0.  Writes only this directory.
set -u
R=/home/vgpnk/Projects/shokunin/tameshi-shokunin
C=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
W=$R/.ufo/waves/round-55/w3/T55W3R06-receipts
S=/fast/scratch/hyaku/tameshi-r55/T55W3R06
L=$S/lane
mkdir -p "$W" "$S/tmp"

if [ ! -d "$L/.git" ]; then
  git clone --shared -q "$R" "$L"
  git -C "$L" checkout -q "$C"
fi
echo "fixture-toplevel=$(git -C "$L" rev-parse --show-toplevel)"
echo "fixture-head=$(git -C "$L" rev-parse HEAD)"
[ "$(git -C "$L" rev-parse HEAD)" = "$C" ] || { echo "FIXTURE NOT AT C0"; exit 1; }

# 01 -- section sha, primary (frozen sectionizer) and prose cut
python3 "$W/section.py" > "$W/01-section.out" 2>&1
echo "exit=$?" >> "$W/01-section.out"

# 02 -- every path the section cites, as a blob at C0
{
  for f in corpus/SOURCES.md corpus/knowledge/repeated-control-precondition.md \
           .ufo/evidence/round-12/verification-final.json \
           .ufo/evidence/round-12/ControlGate/expected.json \
           .ufo/evidence/round-12/ControlGate/mismatch/expected.json \
           .ufo/evidence/round-12/BashWitness/declaration.json \
           .ufo/evidence/round-12/BashWitness/declared.tsv \
           .ufo/evidence/round-12/BashWitness/manifest.json \
           .ufo/evidence/round-12/BashWitness/summary.json \
           tools/repeat-control.py tools/bash-witness-study.py \
           .ufo/waves/round-27/w1/Read25.md .ufo/waves/round-27/residual/ReRead08.md \
           corpus/lessons/round-1-verifier-spotcheck.md SHONEN.md ; do
    printf '%-62s type=%s size=%s entries=%s\n' "$f" \
      "$(git -C "$R" cat-file -t "$C:$f" 2>&1)" \
      "$(git -C "$R" cat-file -s "$C:$f" 2>/dev/null)" \
      "$(git -C "$R" ls-tree "$C" -- "$f" | wc -l)"
  done
} > "$W/02-cited-paths.out" 2>&1

# 03 -- the SOURCES.md:503 anchor, and where the supersession line actually sits
{
  echo '$ git show C0:corpus/SOURCES.md | sed -n "496,508p" | nl -ba -v496'
  git -C "$R" show "$C:corpus/SOURCES.md" | sed -n '496,508p' | nl -ba -v496
  echo
  echo '$ git show C0:corpus/SOURCES.md | grep -nE "^\| *(S004|S026|S265) *\|"'
  git -C "$R" show "$C:corpus/SOURCES.md" | grep -nE '^\| *(S004|S026|S265) *\|' | cut -c1-160
  echo
  echo '# where the "superseding held S026" statement lived per revision'
  for rev in 5b703c6 99c3bc8 "$C"; do
    printf '%-41s ' "$rev"
    git -C "$R" show "$rev:corpus/SOURCES.md" | grep -n 'superseding held S026' | cut -d: -f1
  done
  echo
  echo '# the SKILL.md cite as written at each revision'
  for rev in 5b703c6 99c3bc8 "$C"; do
    printf '%-41s ' "$rev"
    git -C "$R" show "$rev:SKILL.md" | grep -o 'S026 superseded by S265, `corpus/SOURCES.md:[0-9]*`'
  done
  echo
  echo '# what C0 inserted above that line (SOURCES.md hunk headers only)'
  git -C "$R" diff -U0 99c3bc8 "$C" -- corpus/SOURCES.md | grep -E '^@@'
} > "$W/03-sources-anchor.out" 2>&1

# 04 -- committed control snapshots validate read-only
{
  cd "$L" || exit 1
  echo '$ python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate'
  python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate
  echo "exit=$?"
  echo
  echo '$ python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate/mismatch'
  python3 tools/repeat-control.py --snapshot .ufo/evidence/round-12/ControlGate/mismatch
  echo "exit=$?"
} > "$W/04-control-snapshots.out" 2>&1

# 05 -- the section's verdict table and the registry row, exercised
{
  cd "$L" || exit 1
  rm -rf "$S/rc-match" "$S/rc-nonzero" "$S/rc-unavail"
  echo '$ python3 tools/repeat-control.py --runs 3 --out $S/rc-match -- bash -c "echo hi"'
  python3 tools/repeat-control.py --runs 3 --out "$S/rc-match" -- bash -c 'echo hi'
  echo "exit=$?"
  echo
  echo '$ python3 tools/repeat-control.py --runs 3 --out $S/rc-nonzero -- false'
  python3 tools/repeat-control.py --runs 3 --out "$S/rc-nonzero" -- false
  echo "exit=$?"
  echo
  echo '$ python3 tools/repeat-control.py --runs 3 --out $S/rc-unavail -- tameshi-r12-no-such-command'
  python3 tools/repeat-control.py --runs 3 --out "$S/rc-unavail" -- tameshi-r12-no-such-command
  echo "exit=$?"
  echo
  echo '$ python3 tools/repeat-control.py --runs 2 --out $S/rc-runs2 -- true    # floor of 3'
  python3 tools/repeat-control.py --runs 2 --out "$S/rc-runs2" -- true 2>&1 | tail -n 1
  echo "exit=${PIPESTATUS[0]}"
  echo
  echo '$ python3 tools/repeat-control.py --runs 3 --out $S/rc-match -- true     # DIR must not exist'
  python3 tools/repeat-control.py --runs 3 --out "$S/rc-match" -- true 2>&1 | tail -n 1
  echo "exit=${PIPESTATUS[0]}"
} > "$W/05-control-classes.out" 2>&1

# 06 -- repeat-control selftest (registry row: SELFTEST: PASS, exit 0)
{
  cd "$L" || exit 1
  echo '$ TMPDIR=$S/tmp python3 tools/repeat-control.py --selftest'
  TMPDIR="$S/tmp" python3 tools/repeat-control.py --selftest 2>&1 | tail -n 2
  echo "exit=${PIPESTATUS[0]}"
  echo
  echo '# selftest scratch prefix actually used at C0'
  grep -n 'mkdtemp\|bash-witness-selftest-private' tools/repeat-control.py tools/bash-witness-study.py
} > "$W/06-control-selftest.out" 2>&1

# 07 -- witness study: count credits, check drifts
{
  cd "$L" || exit 1
  echo '$ python3 tools/bash-witness-study.py check'
  python3 tools/bash-witness-study.py check
  echo "exit=$?"
  echo
  echo '$ python3 tools/bash-witness-study.py count'
  python3 tools/bash-witness-study.py count
  echo "exit=$?"
} > "$W/07-witness-check-count.out" 2>&1

# 08 -- run/rerun refuse before any sweep starts
{
  cd "$L" || exit 1
  echo '$ python3 tools/bash-witness-study.py run'
  python3 tools/bash-witness-study.py run
  echo "exit=$?"
  echo '$ python3 tools/bash-witness-study.py rerun'
  python3 tools/bash-witness-study.py rerun
  echo "exit=$?"
  echo '$ git -C $L status --porcelain'
  git -C "$L" status --porcelain
  echo "(empty above = the refused modes wrote nothing)"
} > "$W/08-witness-run-refusal.out" 2>&1

# 09 -- witness selftest + usage class
{
  cd "$L" || exit 1
  echo '$ TMPDIR=$S/tmp python3 tools/bash-witness-study.py selftest'
  TMPDIR="$S/tmp" python3 tools/bash-witness-study.py selftest 2>&1 | tail -n 3
  echo "exit=${PIPESTATUS[0]}"
  echo
  echo '$ python3 tools/bash-witness-study.py badmode'
  python3 tools/bash-witness-study.py badmode > /dev/null 2>&1
  echo "exit=$?"
  echo
  echo '$ grep -n "^EXIT_OK" tools/bash-witness-study.py'
  grep -n '^EXIT_OK' tools/bash-witness-study.py
} > "$W/09-witness-selftest-usage.out" 2>&1

# 10 -- frozen set vs manifest.json, declaration pin, disclosure
{
  echo '$ git show C0:.ufo/evidence/round-12/BashWitness/manifest.json  # membership'
  git -C "$R" show "$C:.ufo/evidence/round-12/BashWitness/manifest.json" | python3 -c '
import json,sys
f=json.load(sys.stdin)["files"]
for k in ("declaration.json","declared.tsv","pristine.sh","bash-surface-census.spec","summary.json"):
    print("listed:", k, k in f)
print("listed: manifest.json (top level)", "manifest.json" in f)
print("n files:", len(f))
print("per-sweep manifests:", [k for k in f if k.endswith("manifest.json")][:4])'
  echo
  echo '$ git show C0:.ufo/evidence/round-12/BashWitness/declaration.json  # runner pin + disclosure'
  git -C "$R" show "$C:.ufo/evidence/round-12/BashWitness/declaration.json" | python3 -c '
import json,sys
d=json.load(sys.stdin)
print("inputs keys:", sorted(d["inputs"]))
print("runner pin:", d["inputs"]["runner"]["sha256"])
print("kind:", d["kind"])
print("disclosure:", d["disclosure"])'
  echo
  echo '$ git cat-file blob C0:tools/mutate-and-run.sh | sha256sum'
  git -C "$R" cat-file blob "$C:tools/mutate-and-run.sh" | sha256sum
} > "$W/10-witness-frozen-set.out" 2>&1

# 11 -- SHONEN box 3 at round 12 and at C0; the spot-check lesson
{
  echo '$ git show 9df9212:SHONEN.md | grep -n "^- \["      # round-12 evidence add (2026-10-20)'
  git -C "$R" show 9df9212:SHONEN.md | grep -n '^- \['
  echo
  echo '$ git show C0:SHONEN.md | grep -n "^- \["'
  git -C "$R" show "$C:SHONEN.md" | grep -n '^- \['
  echo
  echo '$ git show C0:corpus/lessons/round-1-verifier-spotcheck.md | grep -n "box-3\|box 3"'
  git -C "$R" show "$C:corpus/lessons/round-1-verifier-spotcheck.md" | grep -n 'box-3\|box 3'
  echo
  echo '$ git log -1 --format="%h %ad %s" --date=short c7986cd'
  git -C "$R" log -1 --format='%h %ad %s' --date=short c7986cd
} > "$W/11-shonen-lesson.out" 2>&1

# 12 -- seat references: Read25 and ReRead08
{
  echo '$ git show C0:.ufo/waves/round-27/w1/Read25.md | grep -nE "75ed934d|DRIFT|never reads|refuse"'
  git -C "$R" show "$C:.ufo/waves/round-27/w1/Read25.md" | grep -nE '75ed934d|DRIFT|never reads|refuse' | cut -c1-260
  echo
  echo '$ git show C0:.ufo/waves/round-27/residual/ReRead08.md | grep -nE "manifest|not blind|disclosure"'
  git -C "$R" show "$C:.ufo/waves/round-27/residual/ReRead08.md" | grep -nE 'manifest|not blind|disclosure' | cut -c1-300
} > "$W/12-seat-references.out" 2>&1

# 13 -- the round-12 runtime evidence actually covers both instruments
{
  echo '$ git show C0:.ufo/evidence/round-12/verification-final.json  # check names'
  git -C "$R" show "$C:.ufo/evidence/round-12/verification-final.json" | python3 -c '
import json,sys
d=json.load(sys.stdin)
print("checks:", [c["name"] for c in d["checks"]])
print("passed:", d["passed"])
print("all observed_exit==expected_exit:", all(c["observed_exit"]==c["expected_exit"] for c in d["checks"]))'
  echo
  echo '$ git show C0:corpus/knowledge/repeated-control-precondition.md | grep -nE "^#{1,3} |floor of 3|not a determinism proof"'
  git -C "$R" show "$C:corpus/knowledge/repeated-control-precondition.md" | grep -nE '^#{1,3} |floor of 3|not a determinism proof' | cut -c1-200
} > "$W/13-runtime-evidence.out" 2>&1

echo "receipts written to $W"
ls "$W"
