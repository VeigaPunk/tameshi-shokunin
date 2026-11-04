# mutant battery for tools/selfstate-freshness.py.
# Defect 1 (round 79): the round-78 wave's `s3-python-isolation-dropped`
# survivor (T78W1M1) — the python tuple loses `-I`, measured FAIL on arm14
# only (round-80 executor T80W1E2 re-derived the singleton set; the tuple
# keeps `-X utf8`, so arm17's utf8_mode stays 1).
# Defects 2-4 (round 80, R80-C2): the three survivors the round-79 wave named
# for this tool — `ss-bom-strip` (T79W1SC2 S1), `ss-cache-key-drops-argv`
# (T79W1SC2 S4) and `python-utf8-dropped` (T79W1M1) — each killed by exactly
# one new arm: arm15, arm16, arm17.
# Run: bash tools/mutate-and-run.sh --target tools/selfstate-freshness.py \
#        --defects tools/selfstate-freshness-mutants.spec \
#        --suite 'python3 -I -X utf8 "$MUTANT" --selftest' --workdir <dir>

@defect ss-bom-strip | the BOM guard is deleted, so a BOM-prefixed doc is decoded as text (round-79 scout T79W1SC2 S1 `ss-bom-strip` survived 14/14); arm15-ARM15_decode_refusals must kill it
@old     if raw.startswith(BOM):\n        raise SetupError('bom-present:%s' % label)
@new     pass

@defect ss-cache-key-drops-argv | the row cache key loses argv, so two rows on one path/rev with different argv share the first row's stdout (round-79 scout T79W1SC2 S4 `ss-cache-key-drops-argv` survived 14/14); arm16-ARM16_cache_key_keeps_argv must kill it
@old     key = (rev, path, argv, interp)
@new     key = (rev, path, interp)

@defect python-utf8-dropped | the python tuple loses `-X utf8`, so python rows run in the locale encoding instead of UTF-8 mode (round-79 mutation-tester T79W1M1 `python-utf8-dropped` survived 14/14); arm17-ARM17_python_utf8_mode_tuple must kill it
@old     'python': ('python3', '-I', '-X', 'utf8'),
@new     'python': ('python3', '-I'),

@defect python-isolation-dropped | the python tuple loses `-I`, so python rows run without isolated mode (round-78 wave seat T78W1M1 `s3-python-isolation-dropped` survived 13/13); arm14-ARM14_python_isolation_tuple must kill it
@old     'python': ('python3', '-I', '-X', 'utf8'),
@new     'python': ('python3', '-X', 'utf8'),

# Defect 5 (round 81, R81-C3): the round-80 mutation-tester's `ss-bom-only`
# survivor (T80W1M1) — only arm15's non-UTF-8 assertion conjuncts are deleted,
# the arm name and both fixture executions are retained, so the suite stays
# 17/17. Killed by arm21's selftest-text pin (the digest covers the selftest
# function's source), never by arm15: a weakened test text is invisible to the
# test it weakens.
@defect ss-bom-only | only arm15's non-UTF-8 assertion conjuncts are deleted, retaining the arm name and both fixture executions (round-80 mutation-tester T80W1M1 `ss-bom-only` survived 17/17); arm21-ARM21_selftest_text_pin must kill it
@old             and 'SELFSTATE:' not in bom_txt\n            and bad_rc == 2 and 'not-utf8:SCORECARD.md' in bad_err\n            and 'SELFSTATE:' not in bad_txt,
@new             and 'SELFSTATE:' not in bom_txt,
