#!/usr/bin/env bash
# probe.sh — driver for the S_FILE_READ survivor non-equivalence probe (tameshi
# round 18, wave 2, seat SurvivorSFILEREAD). Usage: bash probe.sh WORKDIR
# Reads pinned bytes only from git object stores (kumitate @KREV: the target;
# tameshi @LREV: tools/mutate-and-run.sh, suite.txt, the registered spec) and
# this directory; writes only under WORKDIR. Run it under bwrap with the fleet
# read-only; transcript.txt records the exact outer command.
set -u -o pipefail

W=${1:?usage: probe.sh WORKDIR}
HERE=$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")
KUMITATE=/home/vgpnk/Projects/shokunin/kumitate-shokunin
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
KREV=0acb7752d19058b953ebbeba253b1e35f6548de5
LREV=01d586ddbc5fcd78659557c4e93a6ee8517b87d1
PIN=6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f
EV=.ufo/evidence/round-18/sources-check
IN="$W/in"
T="$IN/sources-check.mjs"
M="$W/run-probe/mutant-S_FILE_READ.sources-check.mjs"

say() { printf '%s\n' "$*"; }
step() { printf '\n## %s\n' "$*"; }
cmd() { printf '$ %s\n' "$*"; }
sha() { sha256sum -- "$1" | cut -d' ' -f1; }
show() { while IFS= read -r l; do printf '%s\n' "$l"; done <"$1"; }

mkdir -p "$IN" || exit 2

step '0 environment'
say "date-utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
say "uid=$(id -u) gid=$(id -g) workdir-fs=$(findmnt -no FSTYPE -T "$W")"
say "node $(node --version) at $(readlink -f "$(command -v node)"); $(python3 --version 2>&1); kernel $(uname -r)"
say "env names: $(env | cut -d= -f1 | sort | tr '\n' ' ')"

step '1 materialize pinned inputs (git object stores only)'
cmd "git -C $KUMITATE show $KREV:scripts/sources-check.mjs > $T"
git -C "$KUMITATE" show "$KREV:scripts/sources-check.mjs" >"$T" || exit 2
chmod 755 "$T"
say "target: $(git -C "$KUMITATE" ls-tree "$KREV" -- scripts/sources-check.mjs) sha256=$(sha "$T") lines=$(wc -l <"$T")"
if [[ "$(sha "$T")" != "$PIN" ]]; then say "SETUP: target sha256 != pinned $PIN"; exit 2; fi
say "pin-match: yes ($PIN)"
for p in tools/mutate-and-run.sh "$EV/suite.txt" "$EV/sources-check.defects.spec"; do
  git -C "$LANE" show "$LREV:$p" >"$IN/${p##*/}" || exit 2
  say "tameshi@$LREV:$p sha256=$(sha "$IN/${p##*/}")"
done
sed -n '/^@defect S_FILE_READ /,/^@new /p' "$IN/sources-check.defects.spec" >"$IN/S_FILE_READ.spec"
say "S_FILE_READ.spec (cut verbatim from the registered spec) sha256=$(sha "$IN/S_FILE_READ.spec") lines=$(wc -l <"$IN/S_FILE_READ.spec")"
while IFS= read -r l; do say "  spec | $l"; done <"$IN/S_FILE_READ.spec"
for f in probe.sh probe-suite.sh cov-count.mjs fixture/corpus/SOURCES.md fixture/corpus/knowledge/alpha.md; do
  say "probe-dir $f sha256=$(sha "$HERE/$f")"
done

step '2 contract and code anchors in the pinned target (cat -n)'
cat -n "$T" | sed -n '39,44p;116p;168,170p;181,189p;341,357p;443,452p'

step '3 harness, registered suite (suite.txt): the recorded S_FILE_READ row'
cmd "bash $IN/mutate-and-run.sh --target $T --defects $IN/S_FILE_READ.spec --suite \"\$(cat $IN/suite.txt)\" --workdir $W/run-suite --timeout 120 --tail 3"
bash "$IN/mutate-and-run.sh" --target "$T" --defects "$IN/S_FILE_READ.spec" --suite "$(cat "$IN/suite.txt")" \
  --workdir "$W/run-suite" --timeout 120 --tail 3 >"$W/run-suite.log" 2>&1
say "[exit=$?]"
show "$W/run-suite.log"

step '4 harness, off-suite probe (probe-suite.sh): same mutant construction'
PSUITE="bash '$HERE/probe-suite.sh' \"\$MUTANT\""
cmd "bash $IN/mutate-and-run.sh --target $T --defects $IN/S_FILE_READ.spec --suite '$PSUITE' --workdir $W/run-probe --timeout 120 --tail 13"
bash "$IN/mutate-and-run.sh" --target "$T" --defects "$IN/S_FILE_READ.spec" --suite "$PSUITE" \
  --workdir "$W/run-probe" --timeout 120 --tail 13 >"$W/run-probe.log" 2>&1
say "[exit=$?]"
show "$W/run-probe.log"

step '5 mutant identity'
say "run-suite mutant sha256=$(sha "$W/run-suite/mutant-S_FILE_READ.sources-check.mjs")"
say "run-probe mutant sha256=$(sha "$M")"
cut -f1-5 "$W/run-suite/results.tsv"
cut -f1-5 "$W/run-probe/results.tsv"
cmd "diff $T $M"
diff "$T" "$M"
say "[exit=$?]"

step '6 side by side on every witness (SHOW=1): pristine, then mutant'
for a in "$T" "$M"; do
  cmd "SHOW=1 bash $HERE/probe-suite.sh $a"
  SHOW=1 bash "$HERE/probe-suite.sh" "$a" >"$W/side-${a##*/}.log" 2>&1
  say "[exit=$?]"
  show "$W/side-${a##*/}.log"
done

step '7 V8 block coverage of the pristine: registered suite vs probe (every fail-closed return site + the per-entry read)'
POINTS=('175:is not a directory' '177:return failClosed(' '182:corpus/SOURCES.md is absent' \
  '183:cannot inspect corpus/SOURCES.md' '185:return failClosed(' '189:cannot read corpus/SOURCES.md (' \
  '349:cannot read corpus/knowledge (' '355:readFileSync(join(knowledgeDir, name)' '356:cannot read ${relPath}')
h="$W/cov-suite"
mkdir -p "$h/home" "$h/tmp" "$h/cov"
cmd "cd $h && env -i PATH=\$PATH HOME=$h/home TMPDIR=$h/tmp LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES=$h NODE_V8_COVERAGE=$h/cov node $T --selftest   # suite.txt sandbox + NODE_V8_COVERAGE"
(cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 \
  GIT_CEILING_DIRECTORIES="$h" NODE_V8_COVERAGE="$h/cov" node "$T" --selftest) >"$h/selftest.out" 2>&1
say "[exit=$?] $(grep -E '^(SOURCES_SELFTEST|VERDICT):' "$h/selftest.out" | tr '\n' ' ')"
node "$HERE/cov-count.mjs" "$h/cov" "$T" "${POINTS[@]}"
say "[exit=$?]"
p="$W/cov-probe"
mkdir -p "$p/tmp" "$p/cov"
cmd "NODE_V8_COVERAGE=$p/cov TMPDIR=$p/tmp bash $HERE/probe-suite.sh $T"
NODE_V8_COVERAGE="$p/cov" TMPDIR="$p/tmp" bash "$HERE/probe-suite.sh" "$T" >"$p/probe.out" 2>&1
say "[exit=$?] $(sed -n '$p' "$p/probe.out")"
node "$HERE/cov-count.mjs" "$p/cov" "$T" "${POINTS[@]}"
say "[exit=$?]"

step '8 summary (derived from the logs above)'
say "registered suite: $(grep -h '^CONTROL:\|^DEFECT S_FILE_READ:' "$W/run-suite.log" | tr '\n' ' ')"
say "probe suite:      $(grep -h '^CONTROL:\|^DEFECT S_FILE_READ:' "$W/run-probe.log" | tr '\n' ' ')"
say "pristine kinds/exit per mode vs mutant (stdout sha256 fields dropped):"
for w in eacces enoent enametoolong; do
  for mode in text json; do
    say "  $w $mode: pristine[$(grep -h "^PROBE $w $mode:" "$W/side-${T##*/}.log" | sed 's/^PROBE [a-z]* [a-z]*: //; s/ stdout-sha256=[0-9a-f]*//; s/ stderr-bytes=[0-9]*//')] mutant[$(grep -h "^PROBE $w $mode:" "$W/side-${M##*/}.log" | sed 's/^PROBE [a-z]* [a-z]*: //; s/ stdout-sha256=[0-9a-f]*//; s/ stderr-bytes=[0-9]*//')]"
  done
done
