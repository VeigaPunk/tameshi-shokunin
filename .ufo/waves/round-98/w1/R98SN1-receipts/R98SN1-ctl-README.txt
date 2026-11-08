# R98SN1 control artifacts (the four hostile-environment positive controls)

R98SN1-ctl-hostile.cfg
    a git config file:  [init]  templateDir = <scratch>/hostile-tpl
R98SN1-ctl-hostile-pre-commit
    the executable hook installed by that template; it appends "pwned" to <scratch>/hostile-fired
R98SN1-ctl-shim-git
    a PATH shim named `git` that exits 99

Reproduce the controls (from a scratch dir S of your own):

  env GIT_CONFIG_GLOBAL=$PWD/R98SN1-ctl-hostile.cfg \
      git init -q S/hp && ls -l S/hp/.git/hooks/pre-commit      # hook copied
  printf 'x\n' > S/hp/f
  env GIT_CONFIG_GLOBAL=$PWD/R98SN1-ctl-hostile.cfg git -C S/hp add f
  env GIT_CONFIG_GLOBAL=$PWD/R98SN1-ctl-hostile.cfg \
      git -C S/hp -c user.name=c -c user.email=c@invalid commit -qm t
  cat S/hostile-fired                                          # "pwned" -> the config was honoured

  env GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=init.templateDir \
      GIT_CONFIG_VALUE_0=<template dir> git init -q S/hp2       # same effect via env injection

  env PATH=$PWD/shim:$PATH git --version; echo rc=$?            # 99

The three tools replace their environment for every git call (a fresh dict: PATH, LANG, LC_ALL,
GIT_NO_REPLACE_OBJECTS, GIT_CONFIG_NOSYSTEM, GIT_CONFIG_GLOBAL=/dev/null, plus HOME/TMPDIR for
the battery), so none of these controls reaches them -- see env-*.out.
