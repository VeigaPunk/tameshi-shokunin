#!/usr/bin/env bash
# T55W2SentConfig2 receipt driver — R54.8 config.yml incident, re-verified.
# Read-only. Never writes to the lane, ~/.omp, or the fleet root.
# Usage: bash verify.sh            (writes r0*.txt beside this script)
set -u
SEAT=/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-55/w2/T55W2SentConfig2
R="$SEAT-receipts"
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
SESS=/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-28T14-01-34-216Z_01a182d0-f308-7371-97bc-ca8b0ed0633f
C0=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
BASE=0a2010acd1e92e4e332774050825e21bcfc7e079
mkdir -p "$R"

## r1 — the operator turn exists in the round-54 session record (read-only)
{
  echo '$ sqlite3 "file:~/.omp/agent/history.db?mode=ro" \'
  echo "  \"select id,created_at,cwd,session_id,prompt from history where id=690;\""
  sqlite3 "file:$HOME/.omp/agent/history.db?mode=ro" \
    "select id||'|'||datetime(created_at,'unixepoch')||'|'||cwd||'|'||session_id||'|'||prompt from history where id=690;"
  echo
  echo '$ sqlite3 ... "select * from session_titles where session_id like "01a182d0%";"'
  sqlite3 "file:$HOME/.omp/agent/history.db?mode=ro" \
    "select session_id||'|'||title from session_titles where session_id like '01a182d0%';"
  echo
  echo '# the same session id names the round-54 dispatch/session dir:'
  ls -d "$SESS" | sed 's|.*/||'
  echo
  echo '# neighbours of row 690 in the same session (the run-11 routing stream, operator prompts only):'
  sqlite3 "file:$HOME/.omp/agent/history.db?mode=ro" \
    "select id||'  '||datetime(created_at,'unixepoch')||'  '||substr(replace(prompt,char(10),' '),1,80) from history where session_id like '01a182d0%' order by created_at;"
  echo
  echo '# seat-transcript population of that session dir (rounds 54 and 55 share it):'
  echo "  seat_transcripts=$(find "$SESS" -maxdepth 1 -name '*.jsonl' ! -path "$SESS/2026*" | wc -l)"
} > "$R/r1-history-row-690.txt" 2>&1

## r2 — yield time vs delivery time inside the seat's own transcript
{
  echo "# parse $SESS/T54W1ExecStraceNoise.jsonl (message timestamps)"
  python3 - "$SESS/T54W1ExecStraceNoise.jsonl" <<'PY'
import json,sys,datetime
p=sys.argv[1]; yield_ts=None; turn_ts=None; order=[]
for i,l in enumerate(open(p,errors='replace')):
    try: d=json.loads(l)
    except Exception: continue
    if d.get('type')!='message': continue
    m=d.get('message',{}); ts=d.get('timestamp')
    for c in (m.get('content') or []):
        if isinstance(c,dict) and c.get('type')=='toolCall' and c.get('name')=='yield':
            if yield_ts is None: yield_ts=ts; order.append(('yield',ts,i))
    if m.get('role')=='user' and 'instead of m_grok' in json.dumps(m):
        if turn_ts is None: turn_ts=ts; order.append(('operator-turn',ts,i))
def dt(s): return datetime.datetime.strptime(s,'%Y-%m-%dT%H:%M:%S.%fZ')
for k,t,i in order: print('%-14s %s  line %d' % (k,t,i))
print('delta_seconds = %.3f  (= %dm%02ds)' % ((dt(turn_ts)-dt(yield_ts)).total_seconds(),
      (dt(turn_ts)-dt(yield_ts)).seconds//60, (dt(turn_ts)-dt(yield_ts)).seconds%60))
PY
} > "$R/r2-yield-vs-delivery.txt" 2>&1

## r3 — the transcript's own ordering (yield, then the user turn, then a wake)
{
  echo "# roles/timestamps 540..548 of the seat transcript (yield -> user turn -> wake)"
  python3 - "$SESS/T54W1ExecStraceNoise.jsonl" <<'PY'
import json,sys
p=sys.argv[1]; rows=[]
for i,l in enumerate(open(p,errors='replace')):
    try: d=json.loads(l)
    except Exception: continue
    if d.get('type')!='message': continue
    m=d.get('message',{}); role=m.get('role')
    names=[c.get('name') for c in (m.get('content') or []) if isinstance(c,dict) and c.get('type')=='toolCall']
    txt=''
    for c in (m.get('content') or []):
        if isinstance(c,dict) and c.get('type')=='text': txt=c.get('text','')[:60]
    rows.append((i,d.get('timestamp'),role,names,txt))
for i,ts,role,names,txt in rows:
    if 540 <= i <= 548:
        print('%4d %s %-11s tools=%s text=%r' % (i,ts,role,names,txt))
PY
} > "$R/r3-transcript-order.txt" 2>&1

## r4 — config.yml reads scout: "@m_grok" and predates round 55
{
  echo '$ grep -n "scout:" ~/.omp/agent/config.yml'
  grep -n 'scout:' "$HOME/.omp/agent/config.yml"
  echo '$ sha256sum ~/.omp/agent/config.yml'
  sha256sum "$HOME/.omp/agent/config.yml"
  echo '$ stat -c "%y" ~/.omp/agent/config.yml   (offset -0300; UTC = +3h)'
  stat -c '%y' "$HOME/.omp/agent/config.yml"
  echo '$ date -u; date'
  date -u '+UTC %Y-%m-%dT%H:%M:%SZ'; date '+LOCAL %Y-%m-%dT%H:%M:%S %Z'
  echo
  echo '# round-55 start = the lane base commit'
  git -C "$LANE" log -1 --format='base %h committed %cI' "$BASE"
  echo
  echo '# numeric comparison (epoch seconds)'
  echo "config_mtime_epoch=$(stat -c %Y "$HOME/.omp/agent/config.yml")"
  echo "round55_base_epoch=$(git -C "$LANE" log -1 --format=%ct "$BASE")"
  echo "config_is_older_by_seconds=$(( $(git -C "$LANE" log -1 --format=%ct "$BASE") - $(stat -c %Y "$HOME/.omp/agent/config.yml") ))"
} > "$R/r4-config-state.txt" 2>&1

## r5 — every write under ~/.omp newer than round-55 start, by name
{
  R55=$(git -C "$LANE" log -1 --format=%ct "$BASE")
  echo "# epoch cutoff = round-55 base commit = $R55"
  echo '# operator-owned files (config.yml*, mcp.json*, lsp.json, agent/agents/) newer than cutoff:'
  find "$HOME/.omp" -newermt "@$R55" \( -name 'config.yml*' -o -name 'mcp.json*' -o -name 'lsp.json' -o -path '*/agent/agents/*' \) 2>/dev/null | sed 's/^/  /'
  echo '  (no lines above = no operator-owned file written since round-55 start)'
  echo
  echo '# every non-session file under ~/.omp newer than cutoff, collapsed by path shape:'
  find "$HOME/.omp" -newermt "@$R55" -type f 2>/dev/null | grep -v '/sessions/' \
    | sed "s|^$HOME/.omp/||" | sed -E 's#^(logs)/omp\.[0-9.]+\.log$#\1/omp.<pid>.log#; s#^(run/daemons)/.*#\1/...#; s#^(agent/[a-z]+\.db)(-wal|-shm)?$#\1<sfx>#' \
    | sort | uniq -c | sort -rn
} > "$R/r5-omp-write-sweep.txt" 2>&1

## r6 — config.yml: authoritative mutation set + round-55 touch census (classify.py)
{
  echo '### A — the authoritative mutation set'
  python3 "$R/classify.py" A
  echo
  echo '### B — the round-55 touch census (read vs write-into)'
  python3 "$R/classify.py" B
} > "$R/r6-config-mutations.txt" 2>&1

## r7 — the round-54 report's accusation, still live and unannotated
{
  echo '$ sed -n "106,112p" /home/vgpnk/Projects/shokunin/.ufo/reports/round-54/tameshi.md'
  sed -n '106,112p' /home/vgpnk/Projects/shokunin/.ufo/reports/round-54/tameshi.md
  echo
  echo '$ grep -c -i fabricat .ufo/reports/round-54/tameshi.md'
  grep -c -i fabricat /home/vgpnk/Projects/shokunin/.ufo/reports/round-54/tameshi.md
  echo '$ git -C /home/vgpnk/Projects/shokunin log -1 -- .ufo/reports/round-54/tameshi.md'
  git -C /home/vgpnk/Projects/shokunin log -1 --format='%h %cI %s' -- .ufo/reports/round-54/tameshi.md
  echo '$ git -C /home/vgpnk/Projects/shokunin status --porcelain -- .ufo/reports/round-54/tameshi.md'
  git -C /home/vgpnk/Projects/shokunin status --porcelain -- .ufo/reports/round-54/tameshi.md
  echo '  (empty = clean at that commit, i.e. never annotated after it was filed)'
  echo
  echo '# is the operator phrase "instead of m_grok" anywhere in the round-54 directive file?'
  grep -c 'instead of m_grok' /home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-54.md
  echo
  echo '# did the round-54 lesson mention the incident at all? (occurrences of config.yml at base)'
  echo "  $(git -C "$LANE" show "$BASE:corpus/lessons/round-54.md" | grep -c -i 'config.yml')" 
} > "$R/r7-report-live-accusation.txt" 2>&1

## r8 — the two records under test, at C0
{
  echo '### ER-R54-8 (SCORECARD.md at C0)'
  git -C "$LANE" show "$C0:SCORECARD.md" | sed -n '/ER-R54-8/,/ER-R54-9/p'
  echo
  echo '### corpus/lessons/round-55.md row R54.8 at C0'
  git -C "$LANE" show "$C0:corpus/lessons/round-55.md" | grep -n 'R54.8'
  echo
  echo '### SUPERSEDED block (round-54 seat file at C0)'
  git -C "$LANE" show "$C0:.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md" | sed -n '/SUPERSEDED (round 55/,$p'
  echo
  echo '### the round-54 prompt clause the records lean on (operator-owned)'
  sed -n '371,377p' /home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-54.md
} > "$R/r8-records.txt" 2>&1

## r9 — what the L1 wrote 63 s before the seat's edit (the "concurrent writer")
{
  echo '# main session 2026-10-28T14-01-34-216Z, config.yml edit at 15:13:57.749Z'
  python3 - <<'PY'
import json,pathlib,os
p=pathlib.Path(os.path.expanduser('~/.omp/agent/sessions/-Projects-shokunin/2026-10-28T14-01-34-216Z_01a182d0-f308-7371-97bc-ca8b0ed0633f.jsonl'))
for l in open(p,errors='replace'):
    if 'agent/config.yml' not in l: continue
    try: d=json.loads(l)
    except Exception: continue
    if d.get('type')!='message': continue
    ts=d.get('timestamp','')
    if not ts.startswith('2026-10-28T15:13:5'): continue
    for c in (d.get('message',{}).get('content') or []):
        if isinstance(c,dict) and c.get('type')=='toolCall' and 'config.yml' in str(c.get('arguments',{})):
            print('ts',ts,'tool',c.get('name')); print(c['arguments'].get('input','')[:900])
PY
  echo
  echo '# the seat edit 63 s later (seat transcript, 15:15:00.569Z):'
  echo '  old_string="    scout: \"@m_grok\""   new_string="    scout: \"@m_glm53\""'
  echo '# the L1 revert (15:21:31.094Z / 15:21:36.480Z): scout -> "@m_grok"'
  echo '#   ("Reverting unauthorized scout routing change")'
} > "$R/r9-concurrent-writer.txt" 2>&1

echo "receipts written to $R"
ls -1 "$R"

## r10 — census conformance (must exit 0)
{
  echo '$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi'
  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
  echo "census_rc=$?"
  echo "rows=$(git -C "$LANE" show "$C0:corpus/SOURCES.md" | grep -cE '^\| S[0-9]{3}')"
} > "$R/r10-census.txt" 2>&1
