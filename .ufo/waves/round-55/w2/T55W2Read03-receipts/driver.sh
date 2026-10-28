#!/usr/bin/env bash
# T55W2Read03 receipts — executor-sufficiency read of `## Standing rules` at C0.
# Re-runnable: every receipt below is (command, captured output, verdict).
# Writes only its own directory and $HYAKU_SCRATCH/tameshi-r55/T55W2Read03.
set -u
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
CAND=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
BASE=0a2010acd1e92e4e332774050825e21bcfc7e079
R="$(cd "$(dirname "$0")" && pwd)"
export HYAKU_SCRATCH=${HYAKU_SCRATCH:-/fast/scratch/hyaku}
S=$HYAKU_SCRATCH/tameshi-r55/T55W2Read03
mkdir -p "$S"
export GIT_CONFIG_NOSYSTEM=1

# ------------------------------------------------------------------ clone at C0
if [ ! -d "$S/clone/.git" ]; then
  git clone --shared -q "$L" "$S/clone"
fi
cd "$S/clone" || exit 90
[ "$(git rev-parse --show-toplevel)" = "$S/clone" ] || { echo "FAIL: toplevel mismatch"; exit 91; }
git checkout -q "$CAND" || exit 92

# ------------------------------------------------------- 00 boundary and sha256
{
  echo '$ python3 sec.py   # imports the frozen .ufo/evidence/round-18/measure.py sectionize()'
  python3 - <<'EOF'
import importlib.util, subprocess, re
spec = importlib.util.spec_from_file_location("m18", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py")
m18 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m18)
rev = "9cf0146b94ddba12d454ebf7288ce6e5c5d535bb"
raw = subprocess.run(["git","-C","/home/vgpnk/Projects/shokunin/tameshi-shokunin","cat-file","blob",rev+":SKILL.md"],capture_output=True,check=True).stdout
secs = m18.sectionize(raw)
hits = [s for s in secs if s["heading"] == "## Standing rules"]
assert len(hits) == 1
s = hits[0]
print("sections=%d heading=%r start=%d end=%d sha256=%s" % (len(secs), s["heading"], s["start"], s["end"], s["sha256"]))
EOF
  echo 'VERDICT: section = SKILL.md lines 17-44 at C0 (28 lines), sha256 acfb671a…, cut by the frozen round-18 sectionizer; no second heading matched.'
} > "$R/00-section-boundary-and-sha.txt" 2>&1

# ------------------------------- 01 tool scratch root vs the HYAKU_SCRATCH rule
{
  echo '$ env -u TMPDIR python3 -c "import tempfile;print(tempfile.gettempdir())"'
  env -u TMPDIR python3 -c "import tempfile;print(tempfile.gettempdir())"
  echo
  echo '$ git -C "$L" grep -c "HYAKU" '"$CAND"' -- tools      # does any tool read $HYAKU_SCRATCH?'
  git -C "$L" grep -c "HYAKU" "$CAND" -- tools; echo "rc=$? (1 = no match)"
  echo
  echo '$ HYAKU_SCRATCH=$HYAKU_SCRATCH strace -f -e trace=mkdir,mkdirat -o log env -u TMPDIR python3 tools/repeat-control.py --selftest'
  mkdir -p "$S/tmpdir-root"
  strace -f -e trace=mkdir,mkdirat -o "$S/strace-unset.log" env -u TMPDIR python3 tools/repeat-control.py --selftest > "$S/rc-unset.out" 2>&1
  echo "rc=$?"
  echo "mkdir calls under /tmp : $(grep -c '"/tmp' "$S/strace-unset.log")"
  echo "mkdir calls under \$HYAKU_SCRATCH: $(grep -c 'tameshi-r55' "$S/strace-unset.log")"
  grep '"/tmp' "$S/strace-unset.log" | head -3
  echo 'VERDICT: "the platform default" is /tmp; strict_scratch_root() never consults $HYAKU_SCRATCH, so with TMPDIR unset the tool scratch root and the section'"'"'s seat-scratch namespace are two different roots.'
} > "$R/01-scratch-root-vs-hyaku.txt" 2>&1

# ------------------------------------------- 02 the size a --rev clone drops there
{
  echo '$ du -sh $L/.git'
  du -sh "$L/.git"
  echo
  echo '$ git clone --no-hardlinks $L $S/clonesize   # same flags registry-check.py:800-810 uses'
  rm -rf "$S/clonesize"
  git clone -q --no-hardlinks "$L" "$S/clonesize"
  du -sh "$S/clonesize"
  echo 'VERDICT: registry-check --rev copies a ~383 MB tree; under the unset arm (receipt 01) that tree lands in /tmp, which Standing rules bounds at 50 MB.'
} > "$R/02-registry-check-clone-size.txt" 2>&1

# --------------------------------- 03 the section's mode counts vs the counters
{
  echo '$ python3 mode-counts.py   # imports the C0 C2 counter, calls its own modes()'
  python3 "$R/mode-counts.py"
  echo
  echo '$ sed -n '"'"'17p'"'"' .ufo/evidence/round-55/c2/measure.py   # counter header'
  sed -n '17p' .ufo/evidence/round-55/c2/measure.py
  echo
  echo '$ grep -n "(8 - note)\|note=%d/9" .ufo/evidence/round-55/c2/measure.py'
  grep -n "(8 - note)\|note=%d/9" .ufo/evidence/round-55/c2/measure.py
  echo
  echo '$ git -C "$L" log --oneline -1   # the lane tip at receipt time (this seat read the pinned C0)'
  git -C "$L" log --oneline -1
  echo
  echo '$ git -C "$L" show HEAD:.ufo/evidence/round-55/c2/measure.py | grep -n "len(allocating) - note\|len(cheap) - empty\|skill = 1"'
  git -C "$L" show HEAD:.ufo/evidence/round-55/c2/measure.py | grep -n "len(allocating) - note\|len(cheap) - empty\|skill = 1"
  echo
  echo 'VERDICT: at the pinned C0 the section names nine allocating modes and the frozen contract target says 9/9, but the counter the section cites headers "8 allocating modes" and its total still subtracts (8 - note): a perfect tree at C0 scores total=-1, PASS=false. The tip (133b2ce, freeze amendment 8) fixes the two denominator terms; the `skill` arm is a MARKER substring test at both revisions, so the numerals themselves are unwatched.'
} > "$R/03-mode-enumeration-vs-counters.txt" 2>&1

# ------------------------------------------- 04 what the counter can see in SKILL
{
  echo '$ git -C "$S/clone" checkout -- SKILL.md   # start from the C0 bytes'
  git -C "$S/clone" checkout -- SKILL.md
  echo
  echo '$ python3 -   # the counter'"'"'s own skill-arm expression (measure.py:260), before/after a numeral mutation'
  echo 'import importlib.util, pathlib
p = pathlib.Path(".ufo/evidence/round-55/c2/measure.py")
spec = importlib.util.spec_from_file_location("c2", p); c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
norm = lambda t: " ".join(t.split())
skill = lambda: 1 if c2.MARKER in norm(pathlib.Path("SKILL.md").read_text()) else 0
print("skill before mutation:", skill())
t = pathlib.Path("SKILL.md").read_text()
t2 = t.replace("the seven self-tests plus", "the seventeen self-tests plus")
t2 = t2.replace("the five non-allocating modes stay lazy", "the ninety non-allocating modes stay lazy")
assert t2 != t
pathlib.Path("SKILL.md").write_text(t2)
print("skill after seven->seventeen and five->ninety:", skill())
print("mutated line:", [l for l in t2.splitlines() if "seventeen" in l][0].strip())' | python3 -
  echo
  echo '$ git -C "$S/clone" checkout -- SKILL.md   # restore the C0 bytes'
  git -C "$S/clone" checkout -- SKILL.md
  echo
  echo 'VERDICT: the only automated read of this rule in SKILL.md is a substring test for MARKER; the mode numerals can go arbitrarily false and the C2 skill arm stays 1/1.'
} > "$R/04-skill-arm-blindness.txt" 2>&1

# --------------------------------------- 05 the unusable arm, executed verbatim
{
  echo '$ TMPDIR=/nonexistent-r55 python3 tools/repeat-control.py --selftest'
  TMPDIR=/nonexistent-r55 python3 tools/repeat-control.py --selftest > "$S/grammar-rc.out" 2> "$S/grammar-rc.err"
  echo "rc=$?"
  echo "stderr: $(cat "$S/grammar-rc.err")"
  echo "stdout bytes: $(wc -c < "$S/grammar-rc.out")"
  echo
  echo 'section template: <tool>: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '"'"'<value>'"'"' (could-not-evaluate)'
  echo 'VERDICT: the unusable arm of the section IS executable from the text alone — rc 2, one stderr line, value named, no traceback token.'
} > "$R/05-grammar-line-repro.txt" 2>&1

# --------------------------- 06 undefined terms, unresolvable clause, no anchors
{
  echo '$ git -C "$L" grep -n -i "write surface" '"$CAND"' -- PROVINCE.md AGENTS.md'
  out=$(git -C "$L" grep -n -i "write surface" "$CAND" -- PROVINCE.md AGENTS.md); rc=$?
  [ -n "$out" ] && echo "$out"
  echo "matches=$(printf '%s' "$out" | grep -c . ) rc=$rc"
  echo
  echo '$ git -C "$L" grep -n "shape-only" '"$CAND"' -- corpus tools AGENTS.md PROVINCE.md   # any definition?'
  git -C "$L" grep -n "shape-only" "$CAND" -- corpus tools AGENTS.md PROVINCE.md | head -8
  echo "definitional hits (means|defined as|shape-only is): $(git -C "$L" grep -n "shape-only" "$CAND" -- corpus tools AGENTS.md PROVINCE.md | grep -c 'means\|defined as\|shape-only is')"
  echo
  echo '$ git -C "$L" grep -c "^| S27[89] " '"$CAND"' -- corpus/SOURCES.md   # the empty-arm anchors resolve'
  echo "S278/S279 rows: $(git -C "$L" grep "^| S27[89] " "$CAND" -- corpus/SOURCES.md | wc -l)"
  echo
  echo '$ grep -rn "dash-form" .ufo/evidence/round-53/integrate/resolutions.json   # where the stated count actually lives'
  grep -rn "dash-form" "$L/.ufo/evidence/round-53/integrate/resolutions.json" | head -2
  echo
  echo '$ grep -rn "host scratch directive" "$L" --include=*.md -l   # the cited directive as an artifact'
  grep -rn "host scratch directive" "$L" --include=*.md -l | head -5
  echo
  echo 'VERDICT: "write surface" has no referent in PROVINCE.md/AGENTS.md at C0 (0 matches); "shape only" has no definition anywhere (0 definitional hits; only usage, incl. one ls -l example at corpus/knowledge/gates-survey-kagi.md:617); the dash-form counts live in a round-53 adjudication file the section does not cite; "the host scratch directive of 2026-10-25" resolves only to SKILL.md copies and wave notes, not to an artifact.'
} > "$R/06-undefined-terms-and-unanchored-claims.txt" 2>&1

# --------------------------------------------------- 07 scope of the wave-1 drift
{
  echo '$ git -C "$L" diff --stat '"$BASE"' '"$CAND"' -- SKILL.md'
  git -C "$L" diff --stat "$BASE" "$CAND" -- SKILL.md
  echo
  echo '$ git -C "$L" diff '"$BASE"' '"$CAND"' -- SKILL.md | grep "^[-+]" | grep -v "^[-+][-+]"'
  git -C "$L" diff "$BASE" "$CAND" -- SKILL.md | grep "^[-+]" | grep -v "^[-+][-+]"
  echo 'VERDICT: one hunk, inside Standing rules; the errata blocks are byte-identical base..C0, so the append-only rule (B4) holds over this edit and is checkable by exactly this diff.'
} > "$R/07-section-scope-diff.txt" 2>&1

# --------------------------- 08 the class sweep, both streams, seven self-tests
{
  echo '$ python3 class-sweep.py   # TMPDIR=/nonexistent-r55-sweep, cwd = C0 clone'
  python3 "$R/class-sweep.py"
  echo
  echo 'VERDICT: the seven self-tests all exit 2 with the grammar on stderr, but "one stderr line" leaves the other stream undefined: repeat-control emits REPEAT_CONTROL: setup_error (28 bytes) on stdout, a second verdict token naming a different class. A caller that parses stdout cannot tell could-not-evaluate from a test failure; the cited counter tests only stderr + the RuntimeError/Traceback tokens, so it stays green.'
} > "$R/08-class-sweep-both-streams.txt" 2>&1

echo "RECEIPTS_WRITTEN: $R"
ls -1 "$R"
