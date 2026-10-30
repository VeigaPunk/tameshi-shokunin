#!/usr/bin/env bash
# T59W1S38 adversarial probe: non-UTF8 blob contents vs frozen gate design/counter.
# All fixture git writes use explicit -C into $D (scratch); root asserted before mutations.
set -u
export TMPDIR=/fast/scratch/hyaku/tameshi-r59/T59W1S38
R=/fast/scratch/hyaku/tameshi-r59/T59W1S38
D=$R/demo
REC=$R/receipts
mkdir -p "$REC"
rm -rf "$D"
mkdir -p "$D/tools"

g(){ git -C "$D" "$@"; }
say(){ echo; echo "== $* =="; }

say "0. fixture root guard"
g init -q
g rev-parse --show-toplevel

say "1. trusted commit: non-UTF8 blob b'\\xff\\xfe\\x00exec\\n' at tools/runner.py"
printf '\xff\xfe\x00exec\n' > "$D/tools/runner.py"
g add -- tools/runner.py
g -c user.name=fixture -c user.email=fixture@example.invalid -c commit.gpgsign=false commit -qm trusted
T=$(g rev-parse HEAD); echo "T=$T"

say "2. candidate EQUAL: same bytes, drift only in unrelated file"
echo '# note' > "$D/note.txt"
g add -- note.txt
g -c user.name=fixture -c user.email=fixture@example.invalid -c commit.gpgsign=false commit -qm eq
CE=$(g rev-parse HEAD); echo "CE=$CE"

say "3. candidate DRIFT: single non-UTF8 byte \\xfe->\\xfd"
printf '\xff\xfd\x00exec\n' > "$D/tools/runner.py"
g add -- tools/runner.py
g -c user.name=fixture -c user.email=fixture@example.invalid -c commit.gpgsign=false commit -qm drift
CD=$(g rev-parse HEAD); echo "CD=$CD"

say "4. git primitive truth: blob OIDs and raw bytes"
echo "OID T :$(g rev-parse "$T:tools/runner.py")"
echo "OID CE:$(g rev-parse "$CE:tools/runner.py")"
echo "OID CD:$(g rev-parse "$CD:tools/runner.py")"
echo "bytes T :$(g cat-file blob "$T:tools/runner.py" | od -An -tx1 | tr -d ' \n')"
echo "bytes CD:$(g cat-file blob "$CD:tools/runner.py" | od -An -tx1 | tr -d ' \n')"

say "5. ATTACK A: strict-UTF8-decode comparator crashes on EQUAL non-UTF8 case"
python3 - "$D" "$T" "$CE" <<'PY'
import subprocess, sys
repo, trusted, cand = sys.argv[1:4]
def read_text(rev, path):
    r = subprocess.run(['git','-C',repo,'cat-file','blob',f'{rev}:{path}'],
                       capture_output=True, text=True)  # text=True == strict locale decode
    return r.stdout
try:
    a = read_text(trusted,'tools/runner.py'); b = read_text(cand,'tools/runner.py')
    print('decoded-compare equal?', a == b)
except UnicodeDecodeError as e:
    print('UNICODE_DECODE_ERROR:', e)
    print('gate would exit 1 with traceback and NO semantic token -> false DRIFT on a BOUND case')
PY

say "6. ATTACK B: lossy decode (errors=replace) turns DRIFT into false BOUND"
python3 - "$D" "$T" "$CD" <<'PY'
import subprocess, sys
repo, trusted, cand = sys.argv[1:4]
def read_bytes(rev, path):
    return subprocess.run(['git','-C',repo,'cat-file','blob',f'{rev}:{path}'],
                          capture_output=True).stdout
a = read_bytes(trusted,'tools/runner.py'); b = read_bytes(cand,'tools/runner.py')
print('byte-equal (git truth):', a == b)
print('replace-decode-equal  :', a.decode('utf-8','replace') == b.decode('utf-8','replace'))
print('-> a text-projecting gate prints EXECUTOR_SOURCE_BOUND and exits 0 on drifted candidate')
PY

say "7. ATTACK C: counter run(text=True) crashes if tool emits non-UTF8 bytes"
STUB=$R/stubtool.py
printf 'import sys;sys.stdout.buffer.write(b"\\xffEXECUTOR_SOURCE_BOUND\\n")\n' > "$STUB"
python3 - "$STUB" <<'PY'
import subprocess, sys
stub = sys.argv[1]
try:
    r = subprocess.run([sys.executable,'-I',stub], capture_output=True, text=True, timeout=30)
    print('counter run() ok, stdout=', r.stdout)
except UnicodeDecodeError as e:
    print('COUNTER_CRASH UnicodeDecodeError:', e)
    print('-> no C1_R59 verdict line; verdict unrecoverable from counter output')
PY

say "8. SMALLEST SOUND BEHAVIOR: blob-OID comparison, encoding-agnostic"
python3 - "$D" "$T" "$CE" "$CD" <<'PY'
import subprocess, sys
repo, T, CE, CD = sys.argv[1:5]
def oid(rev, path):
    r = subprocess.run(['git','-C',repo,'rev-parse',f'{rev}:{path}'],
                       capture_output=True, text=True)
    return r.returncode, r.stdout.strip()
for label, cand in [('equal-nutf8', CE), ('drift-nutf8', CD)]:
    rt, ot = oid(T,'tools/runner.py'); rc, oc = oid(cand,'tools/runner.py')
    verdict = 'BOUND(0)' if (rt == 0 and rc == 0 and ot == oc) else 'DRIFT(1)'
    print(f'{label}: trusted_oid={ot[:12]} cand_oid={oc[:12]} rc={rc} -> {verdict}')
PY

say "9. OID semantics reproduce frozen six-class map (counter's own fixture shape, path tools/runner.py)"
python3 - "$D" <<'PY'
import subprocess, sys, pathlib
repo = pathlib.Path(sys.argv[1])
def git(*a):
    return subprocess.run(['git','-C',str(repo),*a],capture_output=True,text=True,check=True).stdout.strip()
p = repo/'tools/runner.py'
p.write_text('print("real executor")\n')
git('add','--','tools/runner.py')
def commit():
    git('-c','user.name=fixture','-c','user.email=fixture@example.invalid','-c','commit.gpgsign=false','commit','-qm','fixture')
    return git('rev-parse','HEAD')
trusted = commit()
versions = {'equal': trusted}
p.write_text('print("forged success")\n'); git('add','--','tools/runner.py')
versions['changed'] = commit()
p.unlink(); git('add','-u')
versions['missing'] = commit()
p.write_text('print("real executor")\n'); (repo/'unrelated.txt').write_text('unrelated change\n')
git('add','--','tools/runner.py','unrelated.txt')
versions['unrelated'] = commit()
versions['unresolvable'] = '0'*40
p.unlink(); p.symlink_to('elsewhere.py'); git('add','--','tools/runner.py')
versions['symlink'] = commit()
def oid(rev, path):
    r = subprocess.run(['git','-C',str(repo),'rev-parse',f'{rev}:{path}'],capture_output=True,text=True)
    return r.returncode, r.stdout.strip()
expected = {'equal':0,'changed':1,'missing':1,'unrelated':0,'unresolvable':2,'symlink':1}
ok = True
for cls in ['equal','changed','missing','unrelated','unresolvable','symlink']:
    cand = versions[cls]
    # resolve candidate commit first
    rc = subprocess.run(['git','-C',str(repo),'rev-parse','--verify',cand+'^{commit}'],capture_output=True,text=True)
    if rc.returncode:
        got = 2
    else:
        rt,_ = oid(trusted,'tools/runner.py'); rcc,oc = oid(cand,'tools/runner.py')
        got = 1 if (rt != 0 or rcc != 0 or oid(trusted,'tools/runner.py')[1] != oc) else 0
    mark = 'OK' if got == expected[cls] else 'MISMATCH'
    ok &= got == expected[cls]
    print(f'{cls:12s} expected={expected[cls]} oid-semantics={got} {mark}')
print('ALL_FROZEN_CLASSES_REPRODUCED' if ok else 'OID_SEMANTICS_DEVIATE')
PY
echo "DONE"
