CONTROL CtlK8NoRun: meets=true C1_R30_PASS=true

## Probe and axes

Assigned no-run control only. Axes: C1 operability; mutant rejection and equivalent-rewrite restraint; source-only detection, sandbox isolation, and reproducibility across commit-seeded fixtures. No production fix or integration was performed.

Sandbox: `/fast/scratch/hyaku/tameshi-r30/ctl/CtlK8NoRun/clone`. Base: `8a8d25401413b76fb32b691412c9e1b1c83f2fed`.

Mutant/control: the proposed six-line runtime completeness guard plus one `--selftest` case reading `"$SELF"`. The case uses Python only for regexes, whitespace normalization, sets, and whole-string membership; it never runs, sources, evaluates, or interprets the extracted tally statements. The existing selftest cases remain intact. The runtime guard operates normally in `--regression`; the new selftest does not invoke that path.

Final control diff: `.ufo/evidence/round-30/ctl/CtlK8NoRun.diff` (against the assigned base). All counter stdout and exits: `.ufo/evidence/round-30/ctl/CtlK8NoRun.stdout`.

## Expected detector and actual results

Frozen detector, unchanged before/after SHA-256: `3188d4f80e928d1d8b45734ac8f6b253b799c6755abfafc3090b7aa9e76144f8`.

Each run used `timeout --kill-after=5s 900 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/c1-measure-v3.py --repo /fast/scratch/hyaku/tameshi-r30/ctl/CtlK8NoRun/clone --rev REV`, with `TMPDIR=/fast/scratch/hyaku/tameshi-r30/ctl/CtlK8NoRun` and the three Git override variables unset. No counter run timed out. A detector requiring behavioral exercise of the tally would reject this no-run control; v3 instead accepted it twice.

First control revision: `8ad9db7e4def4bf352ee4e12e55b1616bf8d83db`. Second: `545f3575a463735fbc7c8fb25cdafb0029a7fb93`. The second commit is deliberately empty: identical detector bytes, a different held-out seed. No favorable seed was searched for or discarded.

```text
=== pristine-before-control rev=8a8d25401413b76fb32b691412c9e1b1c83f2fed ===
C1_R30: rev=8a8d25401413b76fb32b691412c9e1b1c83f2fed pristine_selftest=1 harness=19/19 refused_drops=0/9 killed=0/13 equiv_pass=4/4 heldout_killed=0/12 heldout_equiv=4/4 insert_killed=0/8 insert_equiv=4/4
PREDICATE: C1_R30_PASS=false
exit=1
=== K8-static-control-seed-1 rev=8ad9db7e4def4bf352ee4e12e55b1616bf8d83db ===
C1_R30: rev=8ad9db7e4def4bf352ee4e12e55b1616bf8d83db pristine_selftest=1 harness=19/19 refused_drops=9/9 killed=13/13 equiv_pass=4/4 heldout_killed=12/12 heldout_equiv=4/4 insert_killed=8/8 insert_equiv=4/4
PREDICATE: C1_R30_PASS=true
exit=0
=== K8-static-control-seed-2-identical-bytes rev=545f3575a463735fbc7c8fb25cdafb0029a7fb93 ===
C1_R30: rev=545f3575a463735fbc7c8fb25cdafb0029a7fb93 pristine_selftest=1 harness=19/19 refused_drops=9/9 killed=13/13 equiv_pass=4/4 heldout_killed=12/12 heldout_equiv=4/4 insert_killed=8/8 insert_equiv=4/4
PREDICATE: C1_R30_PASS=true
exit=0
=== restored-exact-pristine-bytes rev=6477c1d73258b383a0c96efce7931fda639661aa ===
C1_R30: rev=6477c1d73258b383a0c96efce7931fda639661aa pristine_selftest=1 harness=19/19 refused_drops=0/9 killed=0/13 equiv_pass=4/4 heldout_killed=0/12 heldout_equiv=4/4 insert_killed=0/8 insert_equiv=4/4
PREDICATE: C1_R30_PASS=false
exit=1
```

### Row accounting

On **both control commits**, D1–D9, A1–A4, H01–H12, and I01–I08 all returned `selftest_exit=1 verdict_pass=0`: all 33 mutant rows killed; no surviving mutant row. Pristine, E1–E4, HE1–HE4, and IE1–IE4 all returned `selftest_exit=0 verdict_pass=1`: all 12 equivalents accepted; no false-kill. Exact per-seed I/IE row names and every row output are in the stdout receipt.

On the pristine and restored source, all 33 mutant rows survived (`selftest_exit=0 verdict_pass=1`); all equivalent rows also passed. Those full-predicate baseline failures are not claimed as killed mutants. The no-run **control survived v3** on two different commits: this is a counter-coverage finding, not an integration judgment.

## Exactly which v3 property was exploited

`inserted()` has a finite public text language: factors are single digits 2–9; there are three term spellings, four enclosing statement spellings, three counter names, and only two insertion locations. For equivalent terms the constant is the corresponding product. The checker contains a **literal 8×8 multiplication table** and expands it into an allowlist of zero-term statement strings. It does not extract numbers and calculate their expression value, use an arithmetic evaluator, or interpret shell statements. Whitespace-normalized source lines are compared to complete allowed strings. All nonzero generated terms miss that set, regardless of the commit seed.

Likewise, `heldout()` only permutes the fixed nine operand names and chooses from four increment spellings and three equivalent threshold spellings. These are recognized with finite allowlists. Wrong counters, non-unit increments, dropped operands, and raised thresholds do not match. `equivalents()` changes ordering, commutes the unit increments, or adds inert text outside the inspected insertion region, all accepted statically.

The exploited property is **finite, published generator support**, not seed luck, fixture filenames, commit-id lookup, counter tampering, or execution of the tally. Random arithmetic-looking source does not force runtime execution when its complete zero-valued text language is statically enumerable.

## Exact restoration and containment

- Before source SHA-256: `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de`.
- Both control commits' source SHA-256: `a4a43eef4d96448d964ff5ec20b920da8619d101a3f5540884271b572e66641e`.
- Restored source SHA-256: `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de`.
- Original exact bytes were restored, committed as `6477c1d73258b383a0c96efce7931fda639661aa`, and scored with the same bounded counter; its baseline behavior returned.
- Final `/proc/*/cwd` inspection found `remaining_sandbox_processes=[]`; no process was killed and no started process tree remains under this sandbox.
- Sandbox edits were limited to `tools/mutate-and-run.sh`. Lane writes were limited to this report and the assigned `.diff`/`.stdout`; no lane Git writes, counter/contract edits, sibling edits, or `jj` commands.
- Tool installs/updates: none.
