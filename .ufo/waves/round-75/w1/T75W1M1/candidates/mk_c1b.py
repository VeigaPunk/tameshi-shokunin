import hashlib, os
S=os.path.dirname(os.path.abspath(__file__))
SRC=open(os.path.join(S,'cand18.py'),encoding='utf-8').read()
def sub(t,o,n,l):
    c=t.count(o)
    assert c==1, (l,c)
    return t.replace(o,n,1)
def w(name,t):
    open(os.path.join(S,name),'w',encoding='utf-8',newline='\n').write(t)
    print('%-30s %s' % (name,hashlib.sha256(t.encode()).hexdigest()))
# a19: delimited() also accepts a token immediately followed by '.', even
# after a digit ("21." admits 1). No arm carries a decimal-adjacent token.
a=sub(SRC, "    return re.search(r'(?<![0-9])%d(?![0-9])' % value, span) is not None",
      "    return re.search(r'(?<![0-9])%d(?![0-9])|%d\\.' % (value, value), span) is not None", 'a19')
w('a19_delimited_dot_adjacent.py',a)
# a20: the record-span binding refuses a record where the span occurs twice
# (bound to the FIRST occurrence). No arm's record carries a duplicate span.
b=sub(SRC, "    _, rec = _record_span(row, readers)\n    printed = rec.get('printed')",
      "    raw, rec = _record_span(row, readers)\n"
      "    if raw.find(rec['span'], raw.find(rec['span']) + 1) >= 0:\n"
      "        raise SetupError('span-first-occurrence-only:%s' % row['id'])\n"
      "    printed = rec.get('printed')", 'a20')
w('a20_span_first_occurrence.py',b)
