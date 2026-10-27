# Applied to a scratch `git clone --shared` of the lane at CAND1, then committed; nothing else.
# Adds seven synthetic ledger entries to probe the frozen C2 m6 shape rules:
#   PROBE-A zero findings + one existing reader file      -> passes
#   PROBE-B zero findings + no reader_files               -> findings-or-reader-missing
#   PROBE-C zero findings + one missing reader file        -> findings-or-reader-missing
#   PROBE-D zero findings + two missing reader files       -> PASSES (leniency, c2/measure.py:170-171)
#   PROBE-E one finding + wrong_expectations=0             -> count!=findings
#   PROBE-F one finding + wrong_expectations=1             -> passes
#   PROBE-G finding quote absent from reader file          -> quote-not-verbatim
import json
p='.ufo/evidence/round-21/coldread/ledger.json'
d=json.load(open(p)); base=d['entries'][0]
def mk(head, files, findings, we):
    e=dict(base); e.update({'heading':head,'sha256':'dead'*16,
        'read_rev':'7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135','seats':['T52W3Read02'],
        'reader_files':files,'findings':findings,'wrong_expectations':we,
        'verdict':'verified-record','blocking_gaps':0,'minor_gaps':0,'commands_executed_count':3})
    return e
Q='Finding PROBE-Q1: the statement "legs_conforming=10/10" holds'
R=['.ufo/waves/round-52/w3/PROBE-reader.md']
d['entries'] += [
 mk('PROBE-A-zero-findings-one-existing-reader',R,[],0),
 mk('PROBE-B-zero-findings-no-reader-files',[],[],0),
 mk('PROBE-C-zero-findings-one-missing-reader',['.ufo/waves/round-52/w3/NOPE-missing.md'],[],0),
 mk('PROBE-D-zero-findings-two-missing-readers',['.ufo/waves/round-52/w3/NOPE1.md','.ufo/waves/round-52/w3/NOPE2.md'],[],0),
 mk('PROBE-E-one-quote-count-zero',R,[{'quote':Q,'class':'stale'}],0),
 mk('PROBE-F-one-quote-count-one',R,[{'quote':Q,'class':'stale'}],1),
 mk('PROBE-G-forged-quote',R,[{'quote':'this sentence does not appear in the reader file at all','class':'stale'}],1),
]
json.dump(d, open(p,'w'), indent=1, sort_keys=True)
