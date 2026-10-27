"""Spec helper for mutate-and-run.sh: `list <spec>` | `apply <spec> <pristine>
<mutant> <id>`. Byte-exact single replace; count==1 asserted; refuses no-ops."""
import sys

ESCAPES = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\'}


def die(msg):
    sys.stderr.write('spec: %s\n' % msg)
    sys.exit(2)


def unescape(s, where):
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\':
            if i + 1 >= len(s):
                die('%s: trailing backslash' % where)
            n = s[i + 1]
            if n not in ESCAPES:
                die("%s: unknown escape '\\%s' (supported: \\n \\t \\r \\\\)" % (where, n))
            out.append(ESCAPES[n])
            i += 2
        else:
            out.append(c)
            i += 1
    return ''.join(out)


def parse(path):
    try:
        with open(path, encoding='utf-8') as fh:
            text = fh.read()
    except (OSError, UnicodeDecodeError) as e:
        die('cannot read spec file %s: %s' % (path, e))
    if '\r' in text:
        die('CR characters in spec (CRLF line endings are not supported)')
    defects = []
    cur = None

    def finish():
        nonlocal cur
        if cur is not None and ('old' not in cur or 'new' not in cur):
            die('line %d: defect %s incomplete (needs both @old and @new)' % (cur['line'], cur['id']))
        cur = None

    for no, line in enumerate(text.split('\n'), 1):
        if line.strip() == '':
            continue
        if line.lstrip().startswith('#'):
            continue
        if line == '@defect' or line.startswith('@defect '):
            finish()
            rest = line[len('@defect'):].lstrip(' ')
            idpart, sep, desc = rest.partition('|')
            idpart, desc = idpart.strip(), desc.strip()
            if not idpart or any(ch not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-' for ch in idpart):
                die('line %d: bad or missing defect id: %r' % (no, idpart))
            if any(d['id'] == idpart for d in defects):
                die('line %d: duplicate defect id %s' % (no, idpart))
            if '\t' in desc:
                die('line %d: description must not contain a tab' % no)
            cur = {'id': idpart, 'desc': desc, 'line': no}
            defects.append(cur)
        elif line == '@old' or line.startswith('@old '):
            if cur is None:
                die('line %d: @old outside a defect' % no)
            if 'old' in cur:
                die('line %d: duplicate @old for defect %s' % (no, cur['id']))
            cur['old'] = unescape('' if line == '@old' else line[len('@old '):], 'line %d' % no)
        elif line == '@new' or line.startswith('@new '):
            if cur is None:
                die('line %d: @new outside a defect' % no)
            if 'new' in cur:
                die('line %d: duplicate @new for defect %s' % (no, cur['id']))
            cur['new'] = unescape('' if line == '@new' else line[len('@new '):], 'line %d' % no)
        else:
            die('line %d: unrecognized line: %r' % (no, line[:80]))
    finish()
    if not defects:
        die('spec contains no defects')
    for d in defects:
        if d['old'] == '':
            die('defect %s: @old text is empty' % d['id'])
        if d['old'] == d['new']:
            die('defect %s: @new equals @old (no-op mutation)' % d['id'])
    return defects


def cmd_list(path):
    for d in parse(path):
        sys.stdout.write('%s\t%d\t%s\n' % (d['id'], d['line'], d['desc']))


def cmd_apply(path, pristine, mutant, did):
    hits = [d for d in parse(path) if d['id'] == did]
    if not hits:
        die('defect %s not found in spec' % did)
    d = hits[0]
    try:
        data = open(pristine, 'rb').read()
    except OSError as e:
        die('cannot read pristine %s: %s' % (pristine, e))
    old = d['old'].encode('utf-8')
    new = d['new'].encode('utf-8')
    count = data.count(old)
    if count != 1:
        sys.stderr.write('APPLY FAIL id=%s line=%d old-string-count=%d expected=1\n' % (did, d['line'], count))
        sys.exit(2)
    result = data.replace(old, new, 1)
    try:
        with open(mutant, 'wb') as fh:
            fh.write(result)
    except OSError as e:
        die('cannot write mutant %s: %s' % (mutant, e))
    sys.stdout.write('APPLY OK id=%s old-count=1 bytes-before=%d bytes-after=%d\n' % (did, len(data), len(result)))


if len(sys.argv) < 2 or sys.argv[1] not in ('list', 'apply'):
    sys.stderr.write('helper: usage: list <spec> | apply <spec> <pristine> <mutant> <id>\n')
    sys.exit(2)
if sys.argv[1] == 'list':
    if len(sys.argv) != 3:
        die('helper: list needs <spec>')
    cmd_list(sys.argv[2])
else:
    if len(sys.argv) != 6:
        die('helper: apply needs <spec> <pristine> <mutant> <id>')
    cmd_apply(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
