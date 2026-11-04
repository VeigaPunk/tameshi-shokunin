# round 75 mutant battery for tools/wave-reconcile.py (R75-C1).
# Defects 1-3 are the round-74 spec verbatim (tools/wave-reconcile-mutants.spec);
# defects 4-6 are the three mutants measured as survivors at the round-74 base
# (plans/round-75.plan.md R75-C1): each is the exact single edit its named
# round-75 arm kills and no other round-75 arm covers.
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

@defect mc-record-bound | _record_claim binds printed to the whole decoded RECORD instead of the row's span (r74 M-C); arm16-printed-span-not-record must kill it
@old     if not delimited(printed, rec['span']):
@new     if not delimited(printed, _):

@defect roles-bypass | _record_claim is deleted from the roles branch only (r74 selective bypass); arm17-record-claim-live-on-roles must kill it
@old         _record_claim(row, readers)\n        _, records = _results(row, readers)
@new         _, records = _results(row, readers)

@defect attack-bypass | _record_claim is deleted from the attack_share branch only (r74 selective bypass); arm18-record-claim-live-on-attack-share must kill it
@old         _record_claim(row, readers)\n        seats, records = _results(row, readers)
@new         seats, records = _results(row, readers)

@defect adv-seatreports-require-printed-bypass | require_printed is dropped in the seat_reports branch only (r75 carry T75W1R1); arm19-seatreports-printed-required must kill it
@old     if kind == 'seat_reports':\n        printed = _record_claim(row, readers, require_printed=True)
@new     if kind == 'seat_reports':\n        printed = _record_claim(row, readers)
