# R74-C1 draft defect spec (mutate-and-run spec format v1, LF only).
# Three edits the round-73 wave measured as survivors against wave-reconcile.py
# at base 3d6ea1ee8e551e3baf94904384890e3a112088f0.
@defect delimited-tautology | delimited() constant-true: the printed-in-span delimited-token rule is dropped (round-73 m2)
@old     return re.search(r'(?<![0-9])%d(?![0-9])' % value, span) is not None
@new     return True

@defect span-rule-removed | the record-span byte-substring guard in _record_span() is deleted
@old     if rec['span'].encode('utf-8') not in raw:\n        raise SetupError('span-not-in-record:%s:%s' % (row['id'], rec['path']))\n
@new

@defect seat_reports-any-depth | seat_reports counts every *.md under the wave dir instead of only top-level ones (round-73 W2)
@old                  if p.startswith(prefix) and '/' not in p[len(prefix):]
@new                  if p.startswith(prefix)
