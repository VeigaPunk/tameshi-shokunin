#!/usr/bin/env python3
"""Round 31 binding v5 (frozen before any round-31 cold-read data). v4 below, redesigned before data
because pre-data control seat CtlBindV4New (.ufo/waves/round-31/w1/CtlBindV4New.md) kept 63/63 forged
entries with five lexical shapes v4 reads as executed calls: a literal heredoc body, `python3 -c
tools/trace-inputs.py ...`, `false && <call>`, a call inside a function body never called, and a quoted
`';'` argument read as a separator. v5 changes only the command reading:
  - quotes are kept while splitting commands (non-POSIX shlex), so a quoted ; & | is an argument;
    each word is then unquoted for the argv comparison;
  - heredoc bodies (`<<WORD` / `<<-WORD` / quoted words, up to the delimiter line) are removed first;
  - a command that defines a shell function (`name() {`, `function name`) credits nothing;
  - python options `-c` and `-m` mean no script runs (option arguments of -W and -X are skipped);
  - a trace command after `||` (until the next `;`, `&` or newline), or joined by `&&` to a command
    that never succeeds (`false`, `exit`, `return`, `!...`), is unreachable and credits nothing.
    General reachability is not decidable from text; this rule covers the observed shapes only.
  - from seat ReviewBindV4 (.ufo/waves/round-31/w1/ReviewBindV4.md): `command -v/-V` and `timeout`
    without a duration run nothing; an --out value holding `$(`, a backtick or `)` is not a trace
    name; a call whose id also has a tool result BEFORE the call credits nothing.
Pilot before data: the 63 real round-30 wave-C entries keep 63/63 under v5
(.ufo/evidence/round-31/coldread/pilot/v5-on-r30-real-receipt.json); control receipts
.ufo/evidence/round-31/ctl/bind-v5-*.

Round 31 binding v4 (frozen at c111dab5, superseded by v5 before data): bind-select-v3.py of round 30
with its trace condition replaced by the round-30 post-data audit conditions, made stricter.
Routed by corpus/lessons/round-30-verifier-spotcheck.md item 4 and round-30 Mistake 2: seat CtlBindV3
(.ufo/waves/round-30/wC/CtlBindV3.md) showed five forged transcript shapes that v3 keeps (trace name in
another tool's call, error result, shell comment, result before call, reused call id).
v4 credits a trace basename B of seat S only when S's transcript holds an ASSISTANT tool call that
  - is named `bash`, has an id that no other tool call in the transcript reuses, and whose `command`,
    tokenised with shell comments removed (shlex) and split at ; & | and newlines,
    has a simple command that EXECUTES trace-inputs.py (after leading VAR=value, `env [-u X]...` and
    `timeout [opts] DURATION` wrappers, the program is trace-inputs.py itself or a python* interpreter
    whose first non-option argument is trace-inputs.py; an `echo trace-inputs.py ...` does not count)
    with an `--out` option whose value's basename is B (`--out B` or `--out=B`); the traced argv is
    the tokens after `--`;
  - has a toolResult with the same id that comes AFTER the call and is not marked isError;
and the trace receipt file named by the entry exists under --repo, parses, has `rev` equal to the
entry's read_rev, and records an `argv` that matches the traced argv token by token (argv_matches:
an unexpanded $, ` or ~ token matches any one token; a glob token matches one or more tokens that
fnmatch it, or itself). Unquoted fd duplications (2>&1) and redirections are not argv.
Pilot before data: the 63 real round-30 wave-C entries keep 63/63 under v4
(.ufo/evidence/round-31/coldread/pilot/v4-on-r30-real-receipt.json).
Everything else is unchanged from v3 (registry membership, report block, assistant COLDREAD line).
Controls: .ufo/evidence/round-31/ctl/ (scored before data).
v3 docstring, unchanged below:
v3 adds: for EVERY seat, the entry lists at least one trace whose basename (without `.json`, part
after the last '.') starts with `<seat>-` (the round-29 pilot showed seats that prefix the label),
and each such trace basename appears in an assistant-authored tool call whose arguments also name
`trace-inputs.py`, and that tool call has a tool result in the same transcript (matching
toolCallId). Receipts: .ufo/evidence/round-30/attempt3/bind-controls.txt.

Usage: bind-select.py --repo LANE --assembled IN.json --registry REG.json --sessions DIR
                      --prefix PREFIX --out OUT.json --receipt RECEIPT.json

An entry is bound when it names at least one report and one seat and, for EVERY seat it names
(label normalised: the part after the last '.', without a trailing '-<digits>' retry suffix, D3):
  - the normalised seat is a member of the wave registry;
  - one of the entry's own `reports` (D4) is `<...>/<seat>.md`, readable under --repo (D1), and holds
    a json block whose `seat` normalises to the same name, whose `read_rev` equals the entry's, and
    which has a section with the entry's `start` and `heading` (verdicts are not compared: the
    assembler normalises them, round-29 Mistake 5);
  - the host session store holds a transcript `<DIR>/<PREFIX><seat>.jsonl` or
    `<DIR>/<PREFIX><seat>-<N>.jsonl` (D7) in which an ASSISTANT-authored message (text or tool-call
    arguments) contains `COLDREAD <seat>:` (D2: the prompt also contains that string, so a
    whole-file substring test proves nothing).
The receipt records per kept entry and seat: raw label, registry key, transcript path, byte size,
sha256 and session id (D5: the registry carries no agent id). Exit 1 when nothing is kept or the
sessions directory is missing (D6).
"""
import argparse
import fnmatch
import functools
import glob
import hashlib
import json
import os
import re
import shlex
import sys


def norm(label):
    return re.sub(r'-\d+$', '', str(label).split('.')[-1])


SEPARATOR_CHARS = set(';&|\n')
WRAP_RE = re.compile(r'^[A-Za-z_][A-Za-z0-9_]*=')
DURATION_RE = re.compile(r'^\d+(\.\d+)?[smhd]?$')


HEREDOC_RE = re.compile(r'(?<!<)<<(-?)\s*([\'"]?)([A-Za-z_][A-Za-z0-9_]*)\2')
FUNC_TOKEN_RE = re.compile(r'^[A-Za-z_][\w.-]*\(\)$')
NEVER_SUCCEEDS = {'false', 'exit', 'return', '!'}


def _drop_heredoc_bodies(cmd):
    out, delim = [], None
    for line in str(cmd).split('\n'):
        if delim is not None:
            if (line.lstrip('\t') if delim[0] else line) == delim[1]:
                delim = None
            continue
        out.append(line)
        m = HEREDOC_RE.search(line)
        if m:
            delim = (m.group(1) == '-', m.group(3))
    return '\n'.join(out)


def _unquote(tok):
    try:
        parts = shlex.split(tok, comments=False, posix=True)
    except ValueError:
        return tok
    return parts[0] if len(parts) == 1 else tok



def traced_commands(cmd):
    """Return [(out_basename, argv_after_dashdash)] for every reachable simple command in `cmd` that
    executes trace-inputs.py with an --out option (v5 rules in the docstring)."""
    try:
        lex = shlex.shlex(_drop_heredoc_bodies(cmd), posix=False, punctuation_chars=';&|\n')
        lex.whitespace_split = True
        lex.commenters = '#'
        lex.whitespace = ' \t\r'
        raw = list(lex)
    except ValueError:
        return []
    if any(t == 'function' or FUNC_TOKEN_RE.match(t) for t in raw):
        return []
    # Unquoted fd duplications lex as ['2>', '&', '1'] (or ['&', '>f'] for &>f): they are
    # redirections, not command separators. Quoted text is one token and never matches here.
    merged, i = [], 0
    while i < len(raw):
        t = raw[i]
        if t == '&' and merged and re.fullmatch(r'\d*[<>]', merged[-1]) and i + 1 < len(raw) \
                and re.fullmatch(r'\d+|-', raw[i + 1]):
            merged.pop()
            i += 2
            continue
        if t == '&' and i + 1 < len(raw) and raw[i + 1].startswith('>'):
            i += 1
            continue
        merged.append(t)
        i += 1
    found, seg, blocked, prev = [], [], False, []
    for t in merged + [';']:
        if t and set(t) <= SEPARATOR_CHARS:
            if seg:
                words = [_unquote(w) for w in seg]
                hits = _segment(words)
                if hits and not blocked:
                    found.extend(hits)
                prev = [w for w in _strip_redirections(words) if not WRAP_RE.match(w)]
            ops = t.replace('\n', ';')
            if ';' in ops or ops.replace('&&', '').count('&'):
                blocked = False          # a new list starts: the next command always runs
            if '||' in ops:
                blocked = True           # runs only if the previous command failed
            elif '&&' in ops and prev and (prev[0] in NEVER_SUCCEEDS or prev[0].startswith('!')):
                blocked = True           # `false && x`, `! true && x`, `exit && x`
            seg = []
        else:
            seg.append(t)
    return found


def _program(head):
    """Index of the script token when the simple command executes trace-inputs.py, else None."""
    i = 0
    while i < len(head):
        t = head[i]
        if WRAP_RE.match(t):
            i += 1
        elif t in ('env', 'command', 'exec', 'nice', 'nohup'):
            i += 1
            while i < len(head) and (head[i].startswith('-') or WRAP_RE.match(head[i])):
                if t == 'command' and head[i] in ('-v', '-V'):
                    return None      # `command -v x` looks x up, never runs it
                i += 2 if head[i] in ('-u', '--unset') else 1
        elif t == 'timeout':
            i += 1
            while i < len(head) and head[i].startswith('-'):
                i += 2 if head[i] in ('-s', '--signal', '-k', '--kill-after') else 1
            if i < len(head) and DURATION_RE.match(head[i]):
                i += 1
            else:
                return None          # timeout without a duration runs nothing (exit 125)
        else:
            break
    if i >= len(head):
        return None
    if os.path.basename(head[i]) == 'trace-inputs.py':
        return i
    if os.path.basename(head[i]).startswith('python'):
        j = i + 1
        while j < len(head) and head[j].startswith('-'):
            if head[j] in ('-c', '-m') or (len(head[j]) > 1 and head[j][1] != '-' and head[j][-1] in 'cm'):
                return None
            j += 2 if head[j] in ('-W', '-X') else 1
        if j < len(head) and os.path.basename(head[j]) == 'trace-inputs.py':
            return j
    return None


REDIR_ALONE = re.compile(r'^\d*(>>?|<)$')
REDIR_ATTACHED = re.compile(r'^\d*(>>?|<)\S')


def _strip_redirections(seg):
    out, skip = [], False
    for t in seg:
        if skip:
            skip = False
        elif REDIR_ALONE.match(t):
            skip = True
        elif not REDIR_ATTACHED.match(t):
            out.append(t)
    return out


def _segment(seg):
    seg = _strip_redirections(seg)
    if '--' in seg:
        cut = seg.index('--')
        head, argv = seg[:cut], seg[cut + 1:]
    else:
        head, argv = seg, []
    p = _program(head)
    if p is None:
        return []
    outs = []
    for i in range(p + 1, len(head)):
        t = head[i]
        if t == '--out' and i + 1 < len(head):
            outs.append(head[i + 1])
        elif t.startswith('--out='):
            outs.append(t[len('--out='):])
    return [(os.path.basename(o), argv) for o in outs if not any(x in o for x in ('$(', '`', ')'))]


def argv_matches(traced, recorded):
    """Exact token match, except: a token with an unexpanded expansion ($, `, ~) matches any one
    recorded token; a token with glob characters (*, ?, [) matches one or more recorded tokens that
    fnmatch it, or itself literally (bash leaves an unmatched glob as is)."""
    if not isinstance(recorded, list):
        return False
    rec = [str(r) for r in recorded]

    @functools.lru_cache(maxsize=None)
    def m(i, j):
        if i == len(traced):
            return j == len(rec)
        if j == len(rec):
            return False
        t = traced[i]
        if any(ch in t for ch in '$`~'):
            return m(i + 1, j + 1)
        if any(ch in t for ch in '*?['):
            if rec[j] == t and m(i + 1, j + 1):
                return True
            k = j
            while k < len(rec) and fnmatch.fnmatchcase(rec[k], t):
                k += 1
                if m(i + 1, k):
                    return True
            return False
        return rec[j] == t and m(i + 1, j + 1)
    return m(0, 0)


def assistant_has(path, needle):
    """Return (hit, session_id, traced): hit when an assistant message holds `needle`; traced is the
    list of (out_basename, argv) of bash calls that ran trace-inputs.py, have a unique id and a later
    non-error tool result."""
    sid = None
    hit = False
    order = 0
    calls, seen_ids, results = {}, {}, {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get('type') == 'session' and sid is None:
                sid = d.get('id')
            m = d.get('message') if d.get('type') == 'message' else None
            if not m:
                continue
            order += 1
            if m.get('role') == 'toolResult' and m.get('toolCallId'):
                results.setdefault(m.get('toolCallId'), []).append((order, bool(m.get('isError'))))
                continue
            for c in m.get('content') or []:
                if c.get('type') == 'toolCall' and c.get('id'):
                    seen_ids[c['id']] = seen_ids.get(c['id'], 0) + 1
            if m.get('role') != 'assistant':
                continue
            for c in m.get('content') or []:
                if c.get('type') == 'text' and needle in (c.get('text') or ''):
                    hit = True
                elif c.get('type') == 'toolCall':
                    args = json.dumps(c.get('arguments'), ensure_ascii=False)
                    if needle in args:
                        hit = True
                    if c.get('name') == 'bash' and c.get('id'):
                        cmd = (c.get('arguments') or {}).get('command', '')
                        calls[c['id']] = (order, traced_commands(cmd))
    traced = []
    for cid, (o, outs) in calls.items():
        if seen_ids.get(cid) != 1 or not outs:
            continue
        res = results.get(cid, [])
        later = [r for r in res if r[0] > o]
        if later and not later[0][1] and len(later) == len(res):   # no result before the call
            traced.extend(outs)
    return hit, sid, traced


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--assembled', required=True)
    ap.add_argument('--registry', required=True)
    ap.add_argument('--sessions', required=True)
    ap.add_argument('--prefix', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--receipt', required=True)
    a = ap.parse_args()
    if not os.path.isdir(a.sessions):
        print('bind-select: --sessions is not a directory', file=sys.stderr)
        return 1
    reg = json.load(open(a.registry))
    members = reg.get('members', {})
    doc = json.load(open(a.assembled))
    keep, drop = [], []
    for e in doc['entries']:
        seats = list(e.get('seats') or [])
        reports = list(e.get('reports') or [])
        reasons, bindings = [], []
        if not reports:
            reasons.append('no-reports')
        if not seats:
            reasons.append('no-seats')
        for raw in seats:
            seat = norm(raw)
            if seat not in members:
                reasons.append('seat-not-registry-member:%s' % raw)
                continue
            named = [r for r in reports if os.path.basename(r) == seat + '.md']
            if not named:
                reasons.append('report-not-named-by-entry:%s' % seat)
                continue
            rp = named[0]
            full = rp if os.path.isabs(rp) else os.path.join(a.repo, rp)
            try:
                text = open(full, encoding='utf-8').read()
            except OSError:
                reasons.append('report-unreadable:%s' % rp)
                continue
            ok = False
            for blk in re.findall(r'```json\s*\n(.*?)\n```', text, re.S):
                try:
                    d = json.loads(blk)
                except ValueError:
                    continue
                if norm(d.get('seat')) == seat and d.get('read_rev') == e.get('read_rev') and any(
                        s.get('start') == e.get('start') and s.get('heading') == e.get('heading')
                        for s in d.get('sections', [])):
                    ok = True
            if not ok:
                reasons.append('report-block-unbound:%s' % seat)
                continue
            cands = sorted(glob.glob(os.path.join(a.sessions, '%s%s.jsonl' % (a.prefix, seat))) +
                           glob.glob(os.path.join(a.sessions, '%s%s-[0-9]*.jsonl' % (a.prefix, seat))))
            found = None
            for tp in cands:
                hit, sid, traced = assistant_has(tp, 'COLDREAD %s:' % seat)
                if hit:
                    found = (tp, sid, traced)
                    break
            if found is None:
                reasons.append('transcript-without-assistant-coldread:%s (%d candidates)' % (seat, len(cands)))
                continue
            tp, sid, traced = found
            own = [os.path.basename(t) for t in (e.get('traces') or [])
                   if os.path.splitext(os.path.basename(t))[0].split('.')[-1].startswith(seat + '-')]
            if not own:
                reasons.append('no-trace-of-seat:%s' % seat)
                continue
            paths = {os.path.basename(t): t for t in (e.get('traces') or [])}
            untraced = []
            for b in own:
                tpath = paths[b] if os.path.isabs(paths[b]) else os.path.join(a.repo, paths[b])
                try:
                    rec = json.load(open(tpath, encoding='utf-8'))
                except (OSError, ValueError):
                    rec = None
                if not (isinstance(rec, dict) and rec.get('rev') == e.get('read_rev') and
                        any(ob == b and argv_matches(av, rec.get('argv')) for ob, av in traced)):
                    untraced.append(b)
            if untraced:
                reasons.append('trace-without-executed-bash-call:%s:%s' % (seat, ','.join(untraced)))
                continue
            rawb = open(tp, 'rb').read()
            bindings.append({'seat_label': raw, 'seat': seat, 'session_id': sid, 'report': rp,
                             'transcript': tp, 'transcript_bytes': len(rawb),
                             'transcript_sha256': hashlib.sha256(rawb).hexdigest(),
                             'traces_matched_to_tool_calls': own})
        (drop if reasons else keep).append((e, reasons, bindings))
    out = dict(doc)
    out['entries'] = [e for e, _, _ in keep]
    json.dump(out, open(a.out, 'w'), indent=2)
    receipt = {
        'repo': os.path.abspath(a.repo), 'sessions': os.path.abspath(a.sessions), 'prefix': a.prefix,
        'assembled': len(doc['entries']), 'kept': len(keep), 'excluded': len(drop),
        'registry_members': len(members),
        'kept_entries': [{'start': e['start'], 'heading': e['heading'], 'verdict': e['verdict'],
                          'bindings': b} for e, _, b in keep],
        'excluded_entries': [{'start': e['start'], 'heading': e['heading'], 'verdict': e['verdict'],
                              'seats': e.get('seats'), 'reports': e.get('reports'), 'reasons': r}
                             for e, r, _ in drop],
    }
    json.dump(receipt, open(a.receipt, 'w'), indent=2)
    print(json.dumps({k: receipt[k] for k in ('assembled', 'kept', 'excluded')}))
    return 0 if keep else 1


if __name__ == '__main__':
    sys.exit(main())
