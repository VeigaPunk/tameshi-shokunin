# round 79 mutant battery for tools/selfstate-freshness.py (R79-C3).
# The one defect is the round-78 wave's surviving `s3-python-isolation-dropped`
# mutant (T78W1M1): the python tuple loses `-I`, so every python-defaulted row
# runs without isolated mode and no arm noticed (13/13 survived). arm14
# (ARM14_python_isolation_tuple) must kill it and no other arm may change.
# Run: bash tools/mutate-and-run.sh --target tools/selfstate-freshness.py \
#        --defects tools/selfstate-freshness-mutants.spec \
#        --suite 'python3 -I -X utf8 "$MUTANT" --selftest' --workdir <dir>

@defect python-isolation-dropped | the python tuple loses `-I`, so python rows run without isolated mode (round-78 wave seat T78W1M1 `s3-python-isolation-dropped` survived 13/13); arm14-ARM14_python_isolation_tuple must kill it
@old     'python': ('python3', '-I', '-X', 'utf8'),
@new     'python': ('python3', '-X', 'utf8'),
