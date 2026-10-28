#!/usr/bin/env bash
# T55W2RevER548 — re-derive every fact the ER-R54-8 rewrite rests on.
# Read-only: sqlite is opened with mode=ro, the transcript/config/prompt are only read.
set -u
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
C0=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
SESSION=/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-28T14-01-34-216Z_01a182d0-f308-7371-97bc-ca8b0ed0633f
SEAT="$SESSION/T54W1ExecStraceNoise.jsonl"
HDB=/home/vgpnk/.omp/agent/history.db
CFG=/home/vgpnk/.omp/agent/config.yml
PROMPT=/home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-54.md
BAK=/tmp/hyaku-cfg-backup/config.yml.20261028T121435.bak

echo "########## A. the operator turn (history.db, mode=ro)"
python3 - "$HDB" <<'PY'
import sqlite3,sys,datetime
con=sqlite3.connect('file:%s?mode=ro'%sys.argv[1],uri=True)
for r in con.execute("select id,created_at,datetime(created_at,'unixepoch'),session_id,prompt from history where prompt like '%m_glm53 instead of m_grok%'"):
    print("row=%s created_at=%s utc=%sZ session=%s prompt=%r"%r)
PY

echo
echo "########## B. seat transcript timeline (yield -> turn -> write -> second yield)"
python3 - "$SEAT" <<'PYB'
import json,sys,datetime
seat=sys.argv[1]
lines=open(seat,encoding='utf-8',errors='replace').read().splitlines()
def ts(i): return json.loads(lines[i-1])['timestamp']
def parse(t): return datetime.datetime.strptime(t,'%Y-%m-%dT%H:%M:%S.%fZ')
yield_starts=[]; yield_results=[]; turn=None; edit_start=None; edit_result=None; exit_line=None
for i,l in enumerate(lines,1):
    try: o=json.loads(l)
    except Exception: continue
    ct=o.get('customType') or ''
    m=o.get('message') or {}
    if ct=='tool_execution_start' and (o.get('data') or {}).get('toolName')=='yield': yield_starts.append(i)
    if m.get('role')=='toolResult' and m.get('toolName')=='yield': yield_results.append(i)
    if m.get('role')=='user' and 'use m_glm53 instead of m_grok' in json.dumps(m.get('content')): turn=i
    if ct=='tool_execution_start' and (o.get('data') or {}).get('toolName')=='edit' and '/home/vgpnk/.omp/agent/config.yml' in json.dumps((o.get('data') or {}).get('args')): edit_start=edit_start or i
    if m.get('role')=='toolResult' and 'scout: \\"@m_glm53\\"' in l and edit_result is None: edit_result=i
    if ct=='session_exit': exit_line=i
mark={'yield1':yield_starts[0],'yield1_result':yield_results[0],'turn':turn,'edit':edit_start,'edit_result':edit_result,'yield2':yield_starts[-1],'exit':exit_line}
for k in ('yield1','yield1_result','turn','edit','edit_result','yield2','exit'):
    v=mark.get(k)
    print("%-14s line %4s  %s"%(k,v,ts(v) if v else '-'))
def delta(a,b):
    return (parse(ts(mark[b]))-parse(ts(mark[a]))).total_seconds()
def show(label,a,b):
    d=delta(a,b); print("%-34s %8.3fs (%d m %06.3f s)"%(label,d,int(d//60),d%60))
show("turn - first yield result",'yield1_result','turn')
show("edit - turn",'turn','edit')
show("edit - first yield result",'yield1_result','edit')
show("second yield - edit",'edit','yield2')
show("exit - second yield",'yield2','exit')
n=sum(1 for l in lines[mark['turn']:] if 'tool_execution_start' in l)
print("tool starts after the turn: %d (first %s)"%(n, next((json.loads(l)['timestamp'] for l in lines[mark['turn']:] if 'tool_execution_start' in l), '-')))
PYB

echo
echo "########## B2. the seat's own deliberation (line 592 / 598 thinking, byte-exact excerpts)"
python3 - "$SEAT" <<'PY'
import json,sys,re
lines=open(sys.argv[1],encoding='utf-8',errors='replace').read().splitlines()
for ln in (592,598):
    o=json.loads(lines[ln-1]); th=''.join(c.get('thinking','') for c in o['message']['content'] if c.get('type')=='thinking')
    print("--- line %d %s"%(ln,o['timestamp']))
    for pat in ('So I must NOT edit ~/.omp/agent/config.yml','The operator\'s direct instruction supersedes','I\'ll do it.'):
        for m in re.finditer(re.escape(pat),th):
            s=max(0,m.start()-90); e=min(len(th),m.end()+150)
            print("  ...%s..."%th[s:e].replace('\n',' '))
PY

echo
echo "########## C. the alias value now"
grep -n 'scout:' "$CFG"
sha256sum "$CFG"
stat -c '%y  %n' "$CFG"

echo
echo "########## D. the round-54 prompt ownership rule"
sed -n '373,376p' "$PROMPT"

echo
echo "########## E. the seat's own role bullet (session_init systemPrompt)"
python3 - "$SEAT" <<'PY'
import json,sys
o=json.loads(open(sys.argv[1],encoding='utf-8',errors='replace').read().splitlines()[6])
blob='\n\n'.join(o['systemPrompt'])
i=blob.find('Preserve global configurations')
print(blob[blob.rfind('§ Role',0,i):i+140])
PY

echo
echo "########## F. concurrent writer (pre-edit backup vs now)"
stat -c 'backup mtime %y  size %s' "$BAK"
grep -n 'mutation-tester:\|scout:' "$BAK"
diff "$BAK" "$CFG"; echo "diff rc=$?"

echo
echo "########## G. the three record sites at C0 = $C0"
cd "$LANE" || exit 1
echo "--- SCORECARD.md 2680-2691"
git show $C0:SCORECARD.md | awk 'NR>=2680 && NR<=2691{printf "%d\t%s\n",NR,$0}'
echo "--- .ufo/waves/round-54/w1/T54W1ExecStraceNoise.md 332-343"
git show $C0:.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md | awk 'NR>=332 && NR<=343{printf "%d\t%s\n",NR,$0}'
echo "--- corpus/lessons/round-55.md 62"
git show $C0:corpus/lessons/round-55.md | awk 'NR==62{printf "%d\t%s\n",NR,$0}'

echo
echo "########## H. was the turn broadcast? user-attributed copies across round-54/55 transcripts"
python3 - "$SESSION" <<'PY'
import json,sys,glob,os
pat='m_glm53 instead of m_grok'
tot=0
for p in sorted(glob.glob(sys.argv[1]+'/*.jsonl')):
    n=os.path.basename(p); hits=[]
    for i,l in enumerate(open(p,encoding='utf-8',errors='replace'),1):
        if pat not in l: continue
        try: o=json.loads(l)
        except Exception: continue
        if (o.get('message') or {}).get('role')=='user': hits.append((i,o.get('timestamp')))
    if hits: tot+=1; print(n,hits)
print("transcripts carrying it as a user turn:",tot,"of",len(glob.glob(sys.argv[1]+'/*.jsonl')))
PY

echo
echo "########## H2. did the round-54 MAIN transcript ever carry the turn?"
MAINJSON="$SESSION.jsonl"
echo "file: $MAINJSON"
python3 - "$MAINJSON" <<'PYM'
import json,sys,os
p=sys.argv[1]
if not os.path.exists(p): print("MISSING"); raise SystemExit
n=0; last=None
for i,l in enumerate(open(p,encoding='utf-8',errors='replace'),1):
    if 'm_glm53 instead of m_grok' not in l: continue
    try: o=json.loads(l)
    except Exception: continue
    m=o.get('message') or {}
    if m.get('role')=='user' and 'm_glm53 instead of m_grok' in json.dumps(m.get('content')):
        n+=1; last=(i,o.get('timestamp'),m.get('attribution'))
print("main-transcript user turns carrying the instruction:",n,last)
PYM
