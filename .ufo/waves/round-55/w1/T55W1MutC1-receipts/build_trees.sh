#!/bin/bash
# Build the probe-tree set around the C0 target (9cf0146) for the CURRENT frozen
# counter bytes (5e8f50d1). Every clone names -C and asserts its toplevel.
set -euo pipefail
S=/fast/scratch/hyaku/tameshi-r55/T55W1MutC1
C0=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
# (old target rev not reachable from this clone; the narrow diff fallback copies files)
export GIT_AUTHOR_NAME=seat GIT_AUTHOR_EMAIL=seat@local
export GIT_COMMITTER_NAME=seat GIT_COMMITTER_EMAIL=seat@local
cd "$S"

mk() {  # mk <dir>
  rm -rf "$1"
  git clone --shared "$S/current" "$1" >/dev/null 2>&1
  git -C "$1" checkout --detach "$C0" >/dev/null 2>&1
  [ "$(git -C "$1" rev-parse --show-toplevel)" = "$S/$1" ] || { echo "TOPLEVEL MISMATCH $1"; exit 1; }
}
commit() { git -C "$1" add -A >/dev/null && git -C "$1" commit -qm "$2"; }
ins_before_corr() {  # ins_before_corr <dir> <text-file>
  python3 - "$1" "$2" <<'PY'
import pathlib, sys
d, tf = sys.argv[1], sys.argv[2]
p = pathlib.Path(d, "SCORECARD.md")
t = p.read_text()
h = "## Round 55 - round-54 record corrections"
i = t.index(h)
p.write_text(t[:i] + pathlib.Path(tf).read_text() + "\n\n" + t[i:])
PY
}

# --- B: dirty = C0 content, uncommitted on the frozen rev
rm -rf dirtyC0
git clone --shared "$S/current" dirtyC0 >/dev/null 2>&1
git -C dirtyC0 checkout --detach 631cd6455e58dce969310b4c0466c3383d9f5108 >/dev/null 2>&1
[ "$(git -C dirtyC0 rev-parse --show-toplevel)" = "$S/dirtyC0" ]
# The C0 record content, laid into the dirty clone's worktree WITHOUT a commit
# (so HEAD stays the frozen rev while the record files read as C0).
for f in SCORECARD.md corpus/QUALITY.md corpus/lessons/round-54.md LOG.md \
         .ufo/evidence/round-55/c1/staged-at-freeze.txt; do
  mkdir -p "dirtyC0/$(dirname "$f")"
  sha=$(git -C "$S/current" rev-parse "$C0:$f")
  git -C dirtyC0 show "$C0:$f" > "dirtyC0/$f" || cp "$S/current/$f" "dirtyC0/$f"
done
echo "dirtyC0 HEAD=$(git -C dirtyC0 rev-parse HEAD) dirty=$(git -C dirtyC0 status --porcelain | wc -l)"

# --- corronly: corrections section + receipt present, in-place fixes reverted
mk corronly2
for f in corpus/QUALITY.md corpus/lessons/round-54.md LOG.md \
         .ufo/waves/round-54/w1/T54W1ExecStraceNoise.md; do
  git -C corronly2 show 631cd64:"$f" > "corronly2/$f"
done
git -C corronly2 show 631cd64:SCORECARD.md > corronly2/SCORECARD.md
python3 - <<'PY'
import pathlib
src = pathlib.Path("/fast/scratch/hyaku/tameshi-r55/T55W1MutC1/current/SCORECARD.md").read_text()
i = src.index("## Round 55 - round-54 record corrections")
p = pathlib.Path("/fast/scratch/hyaku/tameshi-r55/T55W1MutC1/corronly2/SCORECARD.md")
p.write_text(p.read_text() + "\n" + src[i:])
PY
commit corronly2 "corr-only: corrections section and receipt, in-place fixes reverted"

# --- tailsec: a later `## ` section quoting stale tokens
mk tailsec2
printf '\n## Round 55 - appendix after the corrections\n\nStale tokens quoted here deliberately: `CTL_POS_c1 true`, `total=14`, `7883e0e5`.\n' >> tailsec2/SCORECARD.md
commit tailsec2 "C0 + post-corrections ## section quoting stale tokens"

# --- m1tree: CTL_POS_c1 true outside corrections
mk m1tree2
printf '\nProbe: `CTL_POS_c1 true` stated as if it passed.\n' >> m1tree2/corpus/QUALITY.md
commit m1tree2 "probe: CTL_POS_c1 true in QUALITY"

# --- m2tree: the receipt derives total=15 and the section follows it
mk m2tree2
sed -i 's/total=13$/total=15/' m2tree2/.ufo/evidence/round-54/before/c2.stdout
python3 - <<'PY'
import pathlib
p = pathlib.Path("/fast/scratch/hyaku/tameshi-r55/T55W1MutC1/m2tree2/SCORECARD.md")
t = p.read_text(); n = "`total=13`"
assert t.count(n) >= 1
p.write_text(t.replace(n, "`total=15`"))
PY
commit m2tree2 "probe: receipt derives total=15, section follows"

# --- m7tree: corrections quote w1=99
mk m7tree2
python3 - <<'PY'
import pathlib
p = pathlib.Path("/fast/scratch/hyaku/tameshi-r55/T55W1MutC1/m7tree2/SCORECARD.md")
t = p.read_text(); n = "w1=28 w2=25 sections=12"; c = t.count(n)
assert c >= 1, c
p.write_text(t.replace(n, "w1=99 w2=25 sections=12"))
PY
commit m7tree2 "probe: corrections quote w1=99"

# --- m9tree: a later commit also touches the swept seat file
mk m9tree2
printf '\n<!-- later touch by the probe tree -->\n' >> m9tree2/.ufo/waves/round-54/w2/T54W2Sent03.md
commit m9tree2 "probe: second commit on the swept seat file"

# --- m10tree: freeze.json pins cafebabe and the section follows it
mk m10tree2
python3 - <<'PY'
import json, pathlib
p = pathlib.Path("/fast/scratch/hyaku/tameshi-r55/T55W1MutC1/m10tree2/.ufo/evidence/round-54/freeze.json")
d = json.loads(p.read_text()); d["files"]["c2/measure.py"] = "cafebabe" + "0" * 56
p.write_text(json.dumps(d, indent=1) + "\n")
q = pathlib.Path("/fast/scratch/hyaku/tameshi-r55/T55W1MutC1/m10tree2/SCORECARD.md")
t = q.read_text(); assert t.count("8528ee85") >= 1, t.count("8528ee85")
q.write_text(t.replace("8528ee85", "cafebabe"))
PY
commit m10tree2 "probe: freeze.json pins cafebabe, section follows"

# --- m12tree: the staged receipt says 3 and the section follows it
mk m12tree2
printf 'staged_at=2026-10-28T00:00Z\ncommand=probe\noutput=3\n' > m12tree2/.ufo/evidence/round-55/c1/staged-at-freeze.txt
python3 - <<'PY'
import pathlib
p = pathlib.Path("/fast/scratch/hyaku/tameshi-r55/T55W1MutC1/m12tree2/SCORECARD.md")
t = p.read_text(); assert t.count("staged=81") >= 1, t.count("staged=81")
p.write_text(t.replace("staged=81", "staged=3"))
PY
commit m12tree2 "probe: staged receipt says 3, section follows"

# --- m13tree: frozen.stdout names deadbee1 and the section follows it
mk m13tree2
sed -i 's/freeze=077d431e69965fa4673cd006ab64f6fc387f9e15/freeze=deadbee11111111111111111111111111111111111/' m13tree2/.ufo/evidence/round-54/after/frozen.stdout
python3 - <<'PY'
import pathlib
p = pathlib.Path("/fast/scratch/hyaku/tameshi-r55/T55W1MutC1/m13tree2/SCORECARD.md")
t = p.read_text().replace("077d431e", "deadbee1")
p.write_text(t)
assert "077d431e" not in p.read_text()
PY
commit m13tree2 "probe: frozen.stdout names deadbee1, section follows"

# --- m14tree: a hard-wrapped positive-control claim (scan_span arm only)
mk m14tree2
cat >> m14tree2/corpus/lessons/round-54.md <<'EOF'

Probe (wrapped): the arm was proven live by the
positive control (`CTL_POS_c1`, which prints
`rekeyed=7/7`) at the deciding revision.
EOF
commit m14tree2 "probe: wrapped positive-control claim"

# --- m15tree: CTL_POS_c1 true in LOG.md only
mk m15tree2
printf '\nProbe: the claim `CTL_POS_c1 true` stands in the log alone.\n' >> m15tree2/LOG.md
commit m15tree2 "probe: CTL_POS_c1 true in LOG.md only"

# --- m16tree: the SUPERSEDED block removed from the seat file
mk m16tree2
python3 - <<'PY'
import pathlib
p = pathlib.Path("/fast/scratch/hyaku/tameshi-r55/T55W1MutC1/m16tree2/.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md")
t = p.read_text(); i = t.find("**SUPERSEDED (round 55, ER-R54-8).**")
assert i > 0, i
p.write_text(t[:i].rstrip() + "\n")
PY
commit m16tree2 "probe: SUPERSEDED block removed"

# --- f1b2: the third wrong pointer 097985c1 outside the corrections block
mk f1b2
printf 'Probe: the fleet report named freeze `097985c1` for this round.\n' > /tmp/f1.$$
ins_before_corr f1b2 /tmp/f1.$$
commit f1b2 "probe: 097985c1 outside corrections"

# --- f2b2: a wrong total that is not the literal 14
mk f2b2
python3 - <<'PY'
import pathlib
p = pathlib.Path("/fast/scratch/hyaku/tameshi-r55/T55W1MutC1/f2b2/SCORECARD.md")
t = p.read_text(); h = "## Round 55 - round-54 record corrections"; i = t.index(h)
n = "sources=0 total=13` false"; assert t[:i].count(n) == 1, t[:i].count(n)
p.write_text(t[:i].replace(n, "sources=0 total=16` false") + t[i:])
PY
commit f2b2 "probe: total=16 outside corrections"

# --- f3b2: the same false claim in lower case
mk f3b2
printf '\nProbe: ctl_pos_c1 true is asserted again, in lower case.\n' >> f3b2/corpus/QUALITY.md
commit f3b2 "probe: lowercase ctl_pos_c1 true"

# --- p7b: the stale c2 digest 49280fe5 outside corrections (R54.4 has no stale arm)
mk p7b
printf 'Probe: the deciding c2 counter was `49280fe5`.\n' > /tmp/p7.$$
ins_before_corr p7b /tmp/p7.$$
commit p7b "probe: stale c2 digest outside corrections"

# --- p9b: a different wrong staged count (regex is the literal 84)
mk p9b
printf '\nProbe: the other 86 staged entries were refused.\n' >> p9b/corpus/lessons/round-54.md
commit p9b "probe: 86 staged"

# --- p5b: old finding counts outside corrections (R54.5 has no stale arm)
mk p5b
printf 'Probe: the round-54 waves held 22 wave-1 findings across 9 sections.\n' > /tmp/p5.$$
ins_before_corr p5b /tmp/p5.$$
commit p5b "probe: old finding counts outside corrections"

# --- p10b: the rekeyed=0/30 quote outside corrections (R54.10 has no stale arm)
mk p10b
printf 'Probe: the phase-A CTL_R53 quote is `58/64, rekeyed=0/30`.\n' > /tmp/p10.$$
ins_before_corr p10b /tmp/p10.$$
commit p10b "probe: rekeyed=0/30 quote outside corrections"

# --- p8b: a fabricated config.yml claim (fabricated token absent from corrections)
mk p8b
python3 - <<'PY'
import pathlib
p = pathlib.Path("/fast/scratch/hyaku/tameshi-r55/T55W1MutC1/p8b/SCORECARD.md")
t = p.read_text(); assert t.count("fabricated") >= 1
p.write_text(t.replace("fabricated", "authorised"))
PY
commit p8b "probe: corrections drop the word fabricated"

for d in dirtyC0 corronly2 tailsec2 m1tree2 m2tree2 m7tree2 m9tree2 m10tree2 m12tree2 \
         m13tree2 m14tree2 m15tree2 m16tree2 f1b2 f2b2 f3b2 p7b p9b p5b p10b p8b; do
  printf '%-10s %s\n' "$d" "$(git -C "$d" rev-parse HEAD)"
done
