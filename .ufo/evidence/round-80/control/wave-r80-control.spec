# round-80 control spec: the new survivor over the 23-arm base tool.

@defect record-unknown-root-check-removed | `_record_span`'s unknown-root guard is deleted, so a row whose record names an undeclared reader root reads the default reader silently (round-79 scout T79W1SC2 W7 `wr-record-unknown-root-check-removed` survived 23/23); arm24-record-unknown-root-refused must kill it
@old     root = rec.get('root', 'lane')\n    if root not in readers:\n        raise SetupError('unknown-root:%s:%s' % (root, row.get('id')))
@new     root = rec.get('root', 'lane')
