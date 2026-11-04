import hashlib, os, sys
S=os.path.dirname(os.path.abspath(__file__))
BASE=sys.argv[1]
SRC=open(BASE,encoding='utf-8').read()
def sub(t,o,n,l):
    c=t.count(o); assert c==1,(l,c); return t.replace(o,n,1)
def w(name,t):
    open(os.path.join(S,name),'w',encoding='utf-8',newline='\n').write(t)
    print('%-34s %s' % (name,hashlib.sha256(t.encode()).hexdigest()))
m=sub(SRC,'    _, rec = _record_span(row, readers)','    raw, rec = _record_span(row, readers)','mc1')
m=sub(m,"    if not delimited(printed, rec['span']):","    if not delimited(printed, raw):",'mc2')
w('l1_mc_record_bound.py',m)
m=sub(SRC,"    if kind == 'roles':\n        _record_claim(row, readers)\n","    if kind == 'roles':\n",'r')
w('l1_roles_bypass.py',m)
m=sub(SRC,"    if kind == 'attack_share':\n        _record_claim(row, readers)\n","    if kind == 'attack_share':\n",'a')
w('l1_attack_bypass.py',m)
m=sub(SRC,'    _, rec = _record_span(row, readers)','    raw, rec = _record_span(row, readers)','a16a')
m=sub(m,"    if not delimited(printed, rec['span']):","    if (not delimited(printed, rec['span'])\n            and not delimited(printed, raw)):",'a16b')
w('l1_a16_span_or_record.py',m)
m=sub(SRC,"""            for role, count in declared.items():
                if not re.search(r'(?<![0-9])%d\\s+%s\\b' % (count, re.escape(role)),
                                 span):
                    raise SetupError('declaration-absent-in-record:%s:%s'
                                     % (row['id'], role))
""","""            for role, count in declared.items():
                pass
""",'a17')
w('l1_a17_roles_decl_unbound.py',m)
m=sub(SRC,"    if kind == 'attack_share':\n        _record_claim(row, readers)\n","    if kind == 'attack_share':\n        _record_span(row, readers)\n",'a18')
w('l1_a18_attack_span_only.py',m)
