# round-82 mutant battery for tools/defect-bind.py (R82-C3 population, plus
# the round's new C1 code paths).
# Defect 1 is the round-82 test-text mutant: arm A1's summary conjunct is
# deleted, keeping the arm name and its fixtures. At the BASE bytes it
# survives (11/11, the arm passes vacuously — the round-81 mutation-tester's
# named gap: this instrument carried no text pin); at the declared bytes it is
# killed by A14's selftest-text digest and by no other arm.
# Defects 2-5 are the new C1 code paths: each is the exact single edit its
# named arm kills. Population after this round: 5 defects.
# Run: bash tools/mutate-and-run.sh --target tools/defect-bind.py \
#        --defects tools/defect-bind-mutants.spec \
#        --suite 'python3 -I -X utf8 "$MUTANT" --selftest' --workdir <dir>

@defect db-a1-assertion-weakened | arm A1's summary conjunct is deleted, retaining the arm name and its fixture execution, so a suite whose case never measured anything still reports PASS (round-81 mutation-tester's unpinned-text gap; base bytes 11/11); A14_selftest_text_pin must kill it and no other arm may
@old             and "DEFECT_BIND: rows=1 closed=1 open=0 unexpected=0" in text,
@new             and True,

@defect db-manifest-binding-removed | the manifest byte binding is switched off, so a narrowed manifest measures green with the flag on (the round-81 D-CN3 cheat); A13_manifest_rev_binding must kill it
@old     raw = read_manifest_bytes(manifest_path)\n    bound = None\n    if manifest_rev:\n        bound = bind_manifest(repo, manifest_path, manifest_rev, raw)
@new     raw = read_manifest_bytes(manifest_path)\n    bound = None\n    if False:\n        bound = bind_manifest(repo, manifest_path, manifest_rev, raw)

@defect db-manifest-mismatch-accepted | the byte comparison is deleted, so a manifest edited after the declared revision is accepted as that revision's (the same cheat, one line down); A13_manifest_rev_binding must kill it
@old     if raw != proc.stdout:
@new     if False:

@defect db-regular-file-check-removed | check_tree_paths stops consulting the type/mode boundary, so a directory measures closed (round-81 reviewer D1a/D5); A12_regular_file_boundary must kill it. Re-derived at the round-82 repair: the boundary is shared with blob_bytes, so the edit targets the caller (recipe step 1, substrate movement), keeping the suite enumerating.
@old         state = regular_file_state(repo, rev, path)\n        if state == "missing":\n            missing.append(path)
@new         state = None\n        if state == "missing":\n            missing.append(path)
@defect db-tree-bytes-ignores-type | tree-bytes keeps the lookup and the skip but drops the wrong-kind verdict, so a symlink's row measures closed (round-81 executor cheat register: the target string satisfies min_bytes); A12_regular_file_boundary must kill it
@old     if wrong_kind:\n        return "open", ",".join(wrong_kind)
@new     if False:\n        return "", ""
