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

# round 75 (R75-C1): the two round-74 survivors become measured defects.
@defect m3-printed-bound-to-record | R75 M-C: printed delimited against the decoded RECORD text instead of the bound span (round-74 survivor, T74W1M1 §4-5); arm16-printed-span-not-record must kill it
@old     if not delimited(printed, rec['span']):
@new     if not delimited(printed, _):

@defect roles-record-claim-bypass | R75: the _record_claim call deleted from the roles branch only (T74W1R1 §2); arm17-record-claim-live-on-roles must kill it
@old     if kind == 'roles':\n        _record_claim(row, readers)\n
@new     if kind == 'roles':\n

@defect attack-share-record-claim-bypass | R75: the _record_claim call deleted from the attack_share branch only (T74W1R1 §2); arm18-record-claim-live-on-attack-share must kill it
@old     if kind == 'attack_share':\n        _record_claim(row, readers)\n
@new     if kind == 'attack_share':\n
