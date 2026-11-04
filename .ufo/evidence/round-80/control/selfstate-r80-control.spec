# round-80 control spec: the three new survivors over the 14-arm base tool (do-nothing control for R80-C2).

@defect ss-bom-strip | the BOM guard is deleted, so a BOM-prefixed doc is decoded as text (round-79 scout T79W1SC2 S1 `ss-bom-strip` survived 14/14); arm15-ARM15_decode_refusals must kill it
@old     if raw.startswith(BOM):\n        raise SetupError('bom-present:%s' % label)
@new     pass

@defect ss-cache-key-drops-argv | the row cache key loses argv, so two rows on one path/rev with different argv share the first row's stdout (round-79 scout T79W1SC2 S4 `ss-cache-key-drops-argv` survived 14/14); arm16-ARM16_cache_key_keeps_argv must kill it
@old     key = (rev, path, argv, interp)
@new     key = (rev, path, interp)

@defect python-utf8-dropped | the python tuple loses `-X utf8`, so python rows run in the locale encoding instead of UTF-8 mode (round-79 mutation-tester T79W1M1 `python-utf8-dropped` survived 14/14); arm17-ARM17_python_utf8_mode_tuple must kill it
@old     'python': ('python3', '-I', '-X', 'utf8'),
@new     'python': ('python3', '-I'),
