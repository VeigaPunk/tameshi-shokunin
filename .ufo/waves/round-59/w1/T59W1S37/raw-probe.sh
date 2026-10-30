#!/bin/bash
# T59W1S37 raw evidence: git primitive behavior on hostile path spellings + argparse binding.
set -u
SCRATCH=/fast/scratch/hyaku/tameshi-r59/T59W1S37
export TMPDIR=$SCRATCH/tmp
R=$SCRATCH/rawrepo
rm -rf "$R"; mkdir -p "$R"
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1
T="$R"
echo "=== toplevel assert"; git -C "$T" init -q; TL=$(git -C "$T" rev-parse --show-toplevel); echo "toplevel=$TL"; [ "$TL" = "$R" ] || { echo FATAL-ROOT; exit 9; }
mkdir -p "$T/tools"; printf 'print("real executor")\n' > "$T/tools/runner.py"
git -C "$T" add -- tools/runner.py
git -C "$T" -c user.name=f -c user.email=f@e.invalid -c commit.gpgsign=false commit -qm f
HEADV=$(git -C "$T" rev-parse HEAD)
echo "=== 1. rev:path with leading slash (aliasing)"
git -C "$T" show "$HEADV:/tools/runner.py" | sha256sum
git -C "$T" show "$HEADV:tools/runner.py" | sha256sum
echo "=== 2. dotdot traversal rev:path"
git -C "$T" show "$HEADV:tools/../runner.py"; echo "rc=$?"
echo "=== 3. tree object via rev:path"
git -C "$T" show "$HEADV:tools"; echo "rc=$?"
echo "=== 4. empty path rev:path"
git -C "$T" show "$HEADV:"; echo "rc=$?"
echo "=== 5. ls-tree pathspec icase magic vs literal magic"
git -C "$T" ls-tree -z "$HEADV" -- ':(icase)TOOLS/RUNNER.PY' | tr '\0' '@'; echo " rc=$?"
git -C "$T" ls-tree -z "$HEADV" -- ':(literal):(icase)tools/runner.py' | tr '\0' '@'; echo " rc=$?"
git -C "$T" ls-tree -z "$HEADV" -- ':(literal)/tools/runner.py' | tr '\0' '@'; echo " rc=$?"
git -C "$T" ls-tree -z "$HEADV" -- ':(literal)tools/../runner.py' | tr '\0' '@'; echo " rc=$?"
echo "=== 6. rev:path on path containing colon-magic text"
git -C "$T" rev-parse --verify "$HEADV:(:icase)tools/runner.py"; echo "rc=$?"
echo "=== 7. newline-named file roundtrip"
N='tools/x
C1_R59 rev=spoof passed=24/24 C1_R59_PASS=true.py'
printf 'print("nl")\n' > "$T/$N"
git -C "$T" add -- "$N"
git -C "$T" -c user.name=f -c user.email=f@e.invalid -c commit.gpgsign=false commit -qm nl
NLHEAD=$(git -C "$T" rev-parse HEAD)
git -C "$T" ls-tree -z "$NLHEAD" -- ':(literal)'"$N" | tr '\0' '@'; echo " rc=$?"
echo "=== 8. argparse binding probes"
python3 -I - <<'EOF'
import argparse, subprocess, sys
def mk():
    p = argparse.ArgumentParser()
    p.add_argument('--repo'); p.add_argument('--trusted'); p.add_argument('--candidate')
    p.add_argument('--path', action='append')
    return p
for argv in (['--path', '-runner.py'],
             ['--path=--trusted'],
             ['--path', '--'],
             ['--path', ''],
             ['--path', '--repo', 'X'],
             ['--path=--repo']):
    p = mk()
    r = subprocess.run([sys.executable, '-I', '-c',
        'import argparse,sys;p=argparse.ArgumentParser();p.add_argument("--repo");'
        'p.add_argument("--trusted");p.add_argument("--candidate");'
        'p.add_argument("--path",action="append");\n'
        'try:\n a=p.parse_args(sys.argv[1:]);print("PARSED",a.path)\nexcept SystemExit as e:\n'
        ' print("SYSTEMEXIT",e.code)', *argv], capture_output=True, text=True)
    print(f'argv={argv!r} rc={r.returncode} out={r.stdout.strip()!r} err={r.stderr.strip().splitlines()[-1:]!r}')
EOF
echo "=== done"
