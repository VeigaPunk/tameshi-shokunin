#!/usr/bin/env python3
"""T55W2SentConfig2 — classify every omp session tool call that touches
~/.omp/agent/config.yml, from the session JSONL store. Read-only.

mode A : the authoritative mutation set (edit/write whose target IS the file,
         plus shell commands that write INTO it).
mode B : the round-55 touch census (mentions after the round-55 base commit).
"""
import json, os, pathlib, re, sys

ROOT = pathlib.Path(os.path.expanduser('~/.omp/agent/sessions'))
CFG = 'agent/config.yml'
CUT = '2026-10-28T16:24:31'

# a redirect whose payload is the config file:  > path   >> path   tee path
RE_REDIR = re.compile(r'(?:^|[\s;&|])(?:>>?|tee\s+-a?)\s+(\S*' + re.escape(CFG) + r')\b')
RE_SED = re.compile(r'sed\s+-i[^;|]*\s(\S*' + re.escape(CFG) + r')\b')
RE_CPMV = re.compile(r'(?:cp|mv|install)\s+[^;|]*\s(\S*' + re.escape(CFG) + r')\s*(?:$|[;&|])')


def edits_config(arg, name):
    if name not in ('edit', 'write'):
        return False
    p = str(arg.get('path', '')).strip()
    if not p:
        # block-style edit: "[~/.omp/agent/config.yml#TAG]\nPUT ..."
        m = re.match(r'\[(~?/?[^\]#]*' + re.escape(CFG) + r')(?:#\w+)?\]', str(arg.get('input', '')))
        return bool(m)
    p = p.split(':')[0]                      # drop a :410-425 selector
    return p in ('~/.omp/' + CFG, os.path.expanduser('~/.omp/' + CFG))


def bash_writes_into(arg):
    """Return the matched substring when a shell command writes INTO the config,
    else False. The substring is printed by both modes so a reader can adjudicate:
    a match inside a quoted literal of a read-only scan is visible as such."""
    cmd = str(arg.get('command', ''))
    if CFG not in cmd:
        return False
    for rx in (RE_REDIR, RE_SED, RE_CPMV):
        m = rx.search(cmd)
        if m:
            return m.group(0)
    return False


def calls():
    for f in ROOT.rglob('*.jsonl'):
        for l in open(f, errors='replace'):
            if CFG not in l:
                continue
            try:
                d = json.loads(l)
            except Exception:
                continue
            if d.get('type') != 'message':
                continue
            for c in (d.get('message', {}).get('content') or []):
                if isinstance(c, dict) and c.get('type') == 'toolCall':
                    yield d.get('timestamp') or '', f.name, c.get('name'), c.get('arguments', {}) or {}


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'A'
    if mode == 'A':
        print('# edit/write tool calls whose TARGET is ~/.omp/' + CFG + ' (all sessions, all time)')
        w = []
        for ts, f, name, a in calls():
            if edits_config(a, name):
                w.append((ts, f, name))
            elif name == 'bash' and bash_writes_into(a):
                w.append((ts, f, 'bash-write-into  match=%r' % bash_writes_into(a)))
        for t, f, n in sorted(w):
            print('%s  %-42s %s' % (t, f[:42], n))
        print('config_mutations_total=%d' % len(w))
        print('last_mutation=%s' % (sorted(w)[-1][0] if w else 'none'))
        return
    # mode B — round-55 census
    rd = wr = 0
    wrl = []
    files = set()
    for ts, f, name, a in calls():
        if ts < CUT:
            continue
        bw = bash_writes_into(a) if name == 'bash' else False
        is_write = edits_config(a, name) or bool(bw)
        if is_write:
            wr += 1
            wrl.append((ts, name, ('match=%r  ' % bw if bw else '') + str(a.get('command', a.get('path', '')))[:80]))
        else:
            rd += 1
            files.add(f)
    print('round55_touches_after_%s = %d' % (CUT, rd + wr))
    print('  read/probe (grep/stat/sha256/sqlite/jsonl parse): %d across %d seat files' % (rd, len(files)))
    print('  write-into-the-file:                              %d' % wr)
    for t, n, c in wrl:
        print('   WRITE %s %s %s' % (t, n, c))


if __name__ == '__main__':
    main()
