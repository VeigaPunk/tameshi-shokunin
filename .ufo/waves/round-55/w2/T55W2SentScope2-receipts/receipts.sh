#!/usr/bin/env bash
# T55W2SentScope2 — scope audit of C0. Read-only against the lane; all fixtures in scratch.
# Produces the numbered receipts this seat's report cites. Safe to re-run.
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
R="$LANE/.ufo/waves/round-55/w2/T55W2SentScope2-receipts"
B=0a2010acd1e92e4e332774050825e21bcfc7e079      # base
F=e2979f277138da503af27b263b783f626f109be4      # counter freeze (amendments 1-7)
C0=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb     # content commit under attack
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tameshi-r55/T55W2SentScope2
mkdir -p "$S"
export HYAKU_SCRATCH=${HYAKU_SCRATCH:-/fast/scratch/hyaku}

# ---------------------------------------------------------------- 01 paths
{
  echo '$ git -C LANE diff --name-only BASE..C0 | wc -l'
  git -C "$LANE" diff --name-only "$B" "$C0" | wc -l
  echo '$ git -C LANE diff --name-only FREEZE..C0 | wc -l   (C0-only change set)'
  git -C "$LANE" diff --name-only "$F" "$C0" | wc -l
  echo '$ ... of which under .ufo/waves/round-55/w1/'
  git -C "$LANE" diff --name-only "$F" "$C0" | grep -c '^\.ufo/waves/round-55/w1/'
  echo
  echo '=== every path C0 touched OUTSIDE .ufo/waves/round-55/w1/ (freeze..C0) ==='
  git -C "$LANE" diff --name-status "$F" "$C0" | grep -v '^[AMD][[:space:]]\.ufo/waves/round-55/w1/'
  echo
  echo '=== top-level buckets, base..C0 ==='
  git -C "$LANE" diff --name-only "$B" "$C0" | awk -F/ '{print ($2==""?$1:$1"/")}' | sort | uniq -c
  echo
  echo '=== gitlinks (160000) and symlinks (120000) in the C0 tree ==='
  git -C "$LANE" ls-tree -r "$C0" | awk '$1=="160000"{print "GITLINK",$4} $1=="120000"{print "SYMLINK",$4}'
  echo '(none printed above = none)'
  echo
  echo '=== paths that look absolute or escape the lane ==='
  git -C "$LANE" diff --name-only "$B" "$C0" | grep -E '^/|(^|/)\.\./' || echo '(none)'
  echo
  echo '=== non-100644 entries introduced anywhere in base..C0 (raw) ==='
  git -C "$LANE" diff --raw "$B" "$C0" | awk '$2!="100644"{print}' | awk '{print $2, $5}' | sort | uniq -c
} > "$R/01-path-inventory.txt" 2>&1

# ------------------------------------------------------- 02 frozen intersection
{
  echo '=== frozen_paths from contract.json at C0, intersected with the C0-only change set ==='
  echo '$ git diff --name-only FREEZE..C0  ∩  contract.frozen_paths'
  python3 - "$LANE" "$B" "$F" "$C0" <<'PY'
import json,subprocess,sys
lane,B,F,C0=sys.argv[1:5]
def g(*a): return subprocess.run(['git','-C',lane]+list(a),capture_output=True,text=True,check=True).stdout
contract=json.loads(g('show',f'{C0}:.ufo/evidence/round-55/contract.json'))
freeze=json.loads(g('show',f'{C0}:.ufo/evidence/round-55/freeze.json'))
frozen=set(contract['frozen_paths']); manifest=set(freeze['files'])
print('frozen_paths:',len(frozen),' freeze manifest entries:',len(manifest),
      ' manifest subset of frozen_paths:',manifest<=frozen,
      ' (manifest excludes freeze.json by design:',freeze.get('note','')+')')
for name,rng in (('base..C0',(B,C0)),('freeze..C0',(F,C0))):
    paths={p for p in g('diff','--name-only',*rng).split('\n') if p}
    print(f'--- {name}: {len(paths)} paths')
    print('    intersect contract.frozen_paths :',sorted(paths&frozen) or 'NONE')
    print('    intersect freeze manifest       :',sorted(paths&manifest) or 'NONE')
    print('    under .ufo/evidence/round-55/   :',sorted(p for p in paths if p.startswith('.ufo/evidence/round-55/')) or 'NONE')
    print('    under .ufo/state/               :',sorted(p for p in paths if p.startswith('.ufo/state/')) or 'NONE')
    print('    .ufo/watchdog.log               :',sorted(p for p in paths if p=='.ufo/watchdog.log') or 'NONE')
    print('    sibling-lane segments           :',sorted(p for p in paths if {'shokuknow','kagi','mado','kama','kumitate','tsukuroi','souji','merge'}&set(p.split('/'))) or 'NONE')
# every frozen path is an A (introduced by the freeze commit), untouched by C0
status={}
for line in g('diff','--name-status',B,C0).splitlines():
    st,p=line.split('\t')[0],line.split('\t')[-1]
    status[p]=st
print('--- status in base..C0 of each frozen path (A = added by the freeze commit, not edited at C0):')
for p in sorted(frozen): print('   ',status.get(p,'<not in diff>'),p)
PY
  echo
  echo '=== worktree: any frozen file dirty? (empty = clean) ==='
  git -C "$LANE" status --porcelain -- \
    .ufo/evidence/round-55/contract.json .ufo/evidence/round-55/freeze.json \
    .ufo/evidence/round-55/c1/measure.py .ufo/evidence/round-55/c2/measure.py \
    .ufo/evidence/round-55/no-harm.sh .ufo/evidence/round-55/deciding-run.sh \
    .ufo/evidence/round-55/controls.sh .ufo/evidence/round-55/c1/staged-at-freeze.txt
  echo '(empty above = no frozen file dirty)'
} > "$R/02-frozen-intersection.txt" 2>&1

# ------------------------------------------------- 03 registry semantic diff
{
  echo '$ git -C LANE diff --numstat FREEZE..C0 -- tools/registry.json'
  git -C "$LANE" diff --numstat "$F" "$C0" -- tools/registry.json
  echo
  echo '=== structural + value diff of the parsed JSON (freeze vs C0) ==='
  git -C "$LANE" show "$F:tools/registry.json" > "$S/reg-freeze.json"
  git -C "$LANE" show "$C0:tools/registry.json" > "$S/reg-c0.json"
  python3 - "$S" <<'PY'
import json,sys
S=sys.argv[1]
f=json.load(open(f'{S}/reg-freeze.json')); c=json.load(open(f'{S}/reg-c0.json'))
rawf=open(f'{S}/reg-freeze.json','rb').read(); rawc=open(f'{S}/reg-c0.json','rb').read()
diffs=[]
def walk(a,b,p=''):
    if type(a)!=type(b): diffs.append((p,'TYPE',a,b)); return
    if isinstance(a,dict):
        if list(a.keys())!=list(b.keys()): diffs.append((p,'KEY-ORDER-OR-SET',list(a.keys()),list(b.keys())))
        for k in a:
            if k in b: walk(a[k],b[k],p+'/'+k)
    elif isinstance(a,list):
        if len(a)!=len(b): diffs.append((p,'LEN',len(a),len(b)))
        for i,(x,y) in enumerate(zip(a,b)): walk(x,y,p+'[%d]'%i)
    elif a!=b: diffs.append((p,'VAL',a,b))
walk(f,c)
print('rows:',len(f['rows']),'->',len(c['rows']),' schema:',f['schema'],'->',c['schema'])
print('rows carrying scratch_root:',sum('scratch_root' in r for r in f['rows']),'->',sum('scratch_root' in r for r in c['rows']))
print('semantic diffs:',len(diffs))
for p,k,a,b in diffs:
    print(f'  {k:16s} {p}')
    print(f'      freeze: {a!r}'[:200])
    print(f'      C0    : {b!r}'[:200])
print()
print('=== serialization: was the file rewritten? ===')
print(f'freeze: {len(rawf)} bytes, {rawf.count(chr(10).encode())} newlines')
print(f'C0    : {len(rawc)} bytes, {rawc.count(chr(10).encode())} newlines')
for name,raw in (('freeze',rawf),('C0',rawc)):
    ok=[i for i in range(0,9) if (json.dumps(json.loads(raw),indent=i)+'\n').encode()==raw]
    print(f'{name} reproduces as json.dumps(obj, indent=N)+NL for N in {ok or "none"}')
g=json.loads(json.dumps(f))
for i in range(len(c['rows'])):
    if 'scratch_root' in c['rows'][i]: g['rows'][i]['scratch_root']=c['rows'][i]['scratch_root']
print('C0 bytes == json.dumps(freeze_obj_with_7_cells_patched, indent=1)+NL :',
      (json.dumps(g,indent=1)+'\n').encode()==rawc)
PY
} > "$R/03-registry-semantic.txt" 2>&1

# ------------------------------------------------------ 04 tool diff surface
{
  for t in tools/repeat-control.py tools/context-capture.py tools/registry-check.py; do
    echo "########## $t"
    echo "\$ git -C LANE diff --numstat FREEZE..C0 -- $t"
    git -C "$LANE" diff --numstat "$F" "$C0" -- "$t"
    echo "\$ git -C LANE diff -U0 FREEZE..C0 -- $t   (hunk headers + added lines only)"
    git -C "$LANE" diff -U0 "$F" "$C0" -- "$t" | grep -E '^(@@|\+\+\+|---|\+[^+])'
    echo
  done
  echo '=== functions touched (AST): each added hunk must land in the refusal or the --rev handler ==='
  python3 - "$LANE" "$C0" <<'PY'
import ast,subprocess,sys
lane,C0=sys.argv[1:3]
def blob(p): return subprocess.run(['git','-C',lane,'show',f'{C0}:{p}'],capture_output=True,text=True,check=True).stdout
for tool in ('tools/repeat-control.py','tools/context-capture.py','tools/registry-check.py'):
    src=blob(tool); lines=src.split('\n')
    spans=[(n.lineno,n.end_lineno,n.name) for n in ast.walk(ast.parse(src))
           if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
    def encl(ln):
        c=[s for s in spans if s[0]<=ln<=s[1]]
        return max(c)[2] if c else '<module>'
    print(f'--- {tool}')
    for i,l in enumerate(lines,1):
        if 'strict_scratch_root()' in l and 'def strict_scratch_root' not in l:
            print(f'   scratch call @{i} inside {encl(i)}()')
        if 'except ScratchRootUnusable' in l:
            print(f'   handler      @{i} inside {encl(i)}()')
PY
} > "$R/04-tool-diff-surface.txt" 2>&1

# --------------------------------------------- 05 refusal probe (C0 clone)
{
  echo "=== clone at C0 into scratch, verify toplevel, never in the lane ==="
  rm -rf "$S/c0-probe"; mkdir -p "$S/c0-probe"
  git clone --shared --no-hardlinks -q "$LANE" "$S/c0-probe"
  echo "\$ git -C clone rev-parse --show-toplevel"; git -C "$S/c0-probe" rev-parse --show-toplevel
  echo "\$ git -C clone checkout --detach $C0"; git -C "$S/c0-probe" checkout -q --detach "$C0"
  echo "\$ git -C clone rev-parse HEAD"; git -C "$S/c0-probe" rev-parse HEAD
  echo
  echo '=== every allocating mode with a set-but-unusable TMPDIR: rc, stderr line count, stdout grep ==='
  probe(){ n=$1; shift; ( cd "$S/c0-probe" && TMPDIR=/nonexistent-probe-$n "$@" >"$S/p-$n.out" 2>"$S/p-$n.err" ); rc=$?
    printf '%-24s rc=%s stderr_lines=%s RuntimeError_in_streams=%s Traceback_in_streams=%s\n' \
      "$n" "$rc" "$(wc -l <"$S/p-$n.err")" \
      "$(grep -c 'RuntimeError' "$S/p-$n.out" "$S/p-$n.err" | awk -F: '{s+=$2}END{print s+0}')" \
      "$(grep -c 'Traceback' "$S/p-$n.out" "$S/p-$n.err" | awk -F: '{s+=$2}END{print s+0}')"
    sed 's/^/    stderr: /' "$S/p-$n.err"
  }
  probe repeat-control           python3 tools/repeat-control.py --selftest
  probe context-capture          python3 tools/context-capture.py --selftest
  probe registry-check           python3 tools/registry-check.py --selftest
  probe bash-witness-study       python3 tools/bash-witness-study.py selftest
  probe pin-disposition          python3 tools/pin-disposition.py --selftest
  probe evidence-disposition     python3 tools/evidence-disposition.py --selftest
  probe env-diff                 python3 tools/env-diff.py --selftest
  echo
  echo '=== non-allocating modes stay lazy with the same bad TMPDIR (must not refuse) ==='
  probe-lazy(){ n=$1; shift; ( cd "$S/c0-probe" && TMPDIR=/nonexistent-probe-$n "$@" >"$S/pl-$n.out" 2>"$S/pl-$n.err" ); rc=$?
    printf '%-24s rc=%s stderr_lines=%s\n' "$n" "$rc" "$(wc -l <"$S/pl-$n.err")"; }
  probe-lazy context-capture-check python3 tools/context-capture.py --check
  echo
  echo '=== documented cell token vs emitted token, all seven ==='
  python3 - "$S" "$LANE" "$C0" <<'PY'
import json,re,subprocess,sys
S,lane,C0=sys.argv[1:4]
reg=json.loads(subprocess.run(['git','-C',lane,'show',f'{C0}:tools/registry.json'],capture_output=True,text=True,check=True).stdout)
emitted={  # measured by the probe above; tooling name -> stderr file
 'repeat-control.py':'repeat-control','context-capture.py':'context-capture',
 'registry-check.py':'registry-check','bash-witness-study.py':'bash-witness-study',
 'pin-disposition.py':'pin-disposition','evidence-disposition.py':'evidence-disposition',
 'env-diff.py':'env-diff'}
bad=0
print(f"{'row':32s} {'documented':26s} {'emitted':18s} match")
for r in reg['rows']:
    if 'scratch_root' not in r: continue
    doc=re.search(r'"([A-Za-z][A-Za-z0-9_.-]*):\s*could-not-evaluate',r['scratch_root']).group(1)
    err=open(f"{S}/p-{emitted[doc]}.err").read().splitlines()
    got=err[0].split(':')[0] if err else '<no stderr>'
    ok = doc==got
    bad += 0 if ok else 1
    print(f"{r['name']:32s} {doc:26s} {got:18s} {'ok' if ok else 'MISMATCH'}")
print(f'\ncells whose documented tool token no run emits: {bad}/7')
PY
} > "$R/05-refusal-probe.txt" 2>&1

# ------------------------------------------------------- 06 worktree status
{
  echo "\$ date -u '+%FT%TZ'   # snapshot time"; date -u '+%FT%TZ'
  echo '$ git -C LANE rev-parse HEAD'; git -C "$LANE" rev-parse HEAD
  echo
  echo '$ git -C LANE status --porcelain | awk "{print \$1}" | sort | uniq -c'
  git -C "$LANE" status --porcelain | awk '{print $1}' | sort | uniq -c
  echo
  echo '=== every dirty path NOT under .ufo/waves/round-55/ ==='
  git -C "$LANE" status --porcelain | sed 's/^...//' | grep -v '^\.ufo/waves/round-55/' | sed 's/^/  /'
  echo
  echo '=== dirty paths under production surfaces (tools/, corpus/, LOG.md, SCORECARD.md, SKILL.md, .ufo/state/) ==='
  git -C "$LANE" status --porcelain -- tools corpus LOG.md SCORECARD.md SKILL.md MANIFEST.json .ufo/state .ufo/watchdog.log | sed 's/^/  /'
  echo '(empty above = production surfaces and .ufo/state clean)'
  echo
  echo '=== deletions (committed wave-1 receipts removed from the worktree) ==='
  git -C "$LANE" status --porcelain | grep '^ D' | sed 's/^...//' | sed 's/^/  /'
  echo
  echo '=== untracked paths outside wave dirs ==='
  git -C "$LANE" status --porcelain | grep '^??' | sed 's/^...//' | grep -v '^\.ufo/waves/' | sed 's/^/  /'
} > "$R/06-worktree-status.txt" 2>&1

# ---------------------------------------- 07 post-dispatch edits under waves/
{
  echo '=== wave-1 dispatch marker (committed at C0) ==='
  echo '$ git -C LANE show C0:.ufo/waves/round-55/w1.ready.dispatched | head -1'
  git -C "$LANE" show "$C0:.ufo/waves/round-55/w1.ready.dispatched" | head -1
  echo
  echo '=== spec / dispatch / marker bytes: C0 vs HEAD vs worktree ==='
  printf '%-46s %-12s %-14s %s\n' file C0==HEAD C0==worktree mtime
  for f in .ufo/waves/round-55/build-spec-w1.py .ufo/waves/round-55/spec-w1.json \
           .ufo/waves/round-55/w1-dispatch.json .ufo/waves/round-55/w1.ready \
           .ufo/waves/round-55/w1.ready.dispatched .ufo/waves/round-55/w1-run.err; do
    printf '%-46s %-12s %-14s %s\n' "$f" \
      "$( [ "$(git -C "$LANE" rev-parse "$C0:$f")" = "$(git -C "$LANE" rev-parse "HEAD:$f")" ] && echo yes || echo NO)" \
      "$( [ "$(git -C "$LANE" rev-parse "$C0:$f")" = "$(git -C "$LANE" hash-object "$LANE/$f")" ] && echo yes || echo NO)" \
      "$(date -r "$LANE/$f" '+%F %T')"
  done
  echo
  echo '=== files under .ufo/waves/round-55/ with mtime after the marker (14:16:09) ==='
  find "$LANE/.ufo/waves/round-55" -newermt '2026-10-28 14:16:09' -type f | wc -l
  echo '=== ... of which under w1/ (wave-1 seats still writing) vs w2/, w3/ (this wave, permitted) ==='
  for d in w1 w2 w3; do printf '  %-3s %s\n' "$d" "$(find "$LANE/.ufo/waves/round-55/$d" -newermt '2026-10-28 14:16:09' -type f 2>/dev/null | wc -l)"; done
  echo
  echo '=== committed-at-C0 wave-1 REPORT files (.md/.json) now dirty (C0 is a mid-flight snapshot) ==='
  git -C "$LANE" status --porcelain -- .ufo/waves/round-55/w1 | grep -E '^ M' | grep -E '\.(md|json)$' | sed 's/^/  /'
  echo
  echo '=== owners of those paths are named in the wave-1 dispatch roster ==='
  for n in T55W1ScribeCells T55W1ExecCensusAfter T55W1CritGate T55W1ExecFooterPaths T55W1SentConfig T55W1CritSourcedClaim; do
    printf '  %-24s in w1 roster: %s\n' "$n" "$(git -C "$LANE" show "$C0:.ufo/waves/round-55/w1.ready.dispatched" | grep -c "$n")"
  done
} > "$R/07-post-dispatch-writes.txt" 2>&1

# --------------------------------------------------------------- 08 census
{
  echo '$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi'
  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
  echo "CENSUS_EXIT=$?"
  echo
  echo '$ grep -cE "^\| S[0-9]{3} \|" corpus/SOURCES.md'
  grep -cE '^\| S[0-9]{3} \|' "$LANE/corpus/SOURCES.md"
} > "$R/08-census.txt" 2>&1

# ------------------------------------------------- 09 cited base receipt drift
{
  echo '$ git -C LANE diff --stat -- .ufo/evidence/round-55/before/c2.stdout   # committed vs worktree'
  git -C "$LANE" diff --stat -- .ufo/evidence/round-55/before/c2.stdout
  echo
  echo '$ git -C LANE diff -- .ufo/evidence/round-55/before/c2.stdout'
  git -C "$LANE" diff -- .ufo/evidence/round-55/before/c2.stdout
  echo
  echo '=== committed blob intact at C0 and at HEAD? ==='
  echo "C0  verdict line: $(git -C "$LANE" show "$C0:.ufo/evidence/round-55/before/c2.stdout" | tail -1)"
  echo "HEAD verdict line: $(git -C "$LANE" show 'HEAD:.ufo/evidence/round-55/before/c2.stdout' | tail -1)"
  echo "worktree verdict line: $(tail -1 "$LANE/.ufo/evidence/round-55/before/c2.stdout")"
} > "$R/09-base-receipt-drift.txt" 2>&1

echo "receipts written to $R"
ls -1 "$R"
