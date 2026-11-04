# round 74 mutant battery for tools/wave-reconcile.py (R74-C1).
# Each defect is the exact single edit a round-73 wave seat measured as a
# survivor; the named frozen arm is the kill the round installs.
# Run: bash tools/mutate-and-run.sh --target tools/wave-reconcile.py \
#        --defects tools/wave-reconcile-mutants.spec \
#        --suite 'python3 -I -X utf8 "$MUTANT" --selftest' --workdir <dir>

@defect m2-delimited-tautology | delimited() accepts any substring occurrence (r73 T73W1S02 m2); arm13-printed-undelimited-refused must kill it
@old     return re.search(r'(?<![0-9])%d(?![0-9])' % value, span) is not None
@new     return True

@defect span-rule-removed | the record-span byte-substring guard is deleted (r73 T73W1S02); arm14-span-not-in-record-refused must kill it
@old     if rec['span'].encode('utf-8') not in raw:\n        raise SetupError('span-not-in-record:%s:%s' % (row['id'], rec['path']))
@new

@defect seat-reports-any-depth | the top-level clause is dropped, nested .md counted (r73 T73W1S10 W2); arm15-seatreports-top-level-only must kill it
@old                  if p.startswith(prefix) and '/' not in p[len(prefix):]
@new                  if p.startswith(prefix)
