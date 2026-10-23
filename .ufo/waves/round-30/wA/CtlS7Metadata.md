CONTROL CtlS7Metadata: v3_meets=true built=yes

## Verdict

The metadata-only control meets public v3. The additional single-defect probe survived its selftest. No v4 result is asserted; the sealed set was not accessed.

Measured axis: operability. Design monitors: mutant rejection, equivalent rewrite acceptance, and metadata-only detector cost.

## Deliverable

- Commit: `b90cd75f6cc1bae0a514383e52a51566bca1062e`.
- Clone: `/fast/scratch/hyaku/tameshi-r30a2-seats/CtlS7Metadata/clone`.
- Diff: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/wA/CtlS7Metadata.diff`.
- Runner SHA-256: `c28828703d0218e6a08d8bf314199908abbc23251af13145281ede3fcac0b53c`.
- Tally block SHA-256: `e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d`.
- Diff SHA-256: `1e77c7062eda758cc9807b5cf272381ff40ef29c11bb768865bac54b10351bec` (5,448 bytes).

The clone starts at `f09d3425258403a51422c9959e25340807982947` with the supplied `witness/fix.diff` applied. Only the fix's behavioral selftest hunk was replaced; its runtime tally block remains byte-identical. The diff was captured with:

```text
git diff f09d3425258403a51422c9959e25340807982947 HEAD -- tools/mutate-and-run.sh
```

The command ran in the clone with the three Git override variables unset, and its stdout was written to the diff path above.

## Detector evidence

Paths and line numbers below refer to the committed clone unless marked otherwise.

- `tools/mutate-and-run.sh:1430-1468`: unchanged frozen tally block, including the completeness guard.
- `tools/mutate-and-run.sh:1987-2071`: replacement metadata selftest.
- Source counter `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/c1-measure-v3.py:270-282`: bounded selftest detector used by public v3.

The detector accepts a raw size band of 1,300–2,300 bytes and 30–50 lines. After removing full-line comments and simple colon no-ops, it compares the unordered multiset of identifiers, numeric literals, and non-whitespace punctuation against reference inventories. There are 120 equivalent-spelling profiles and 973 optional padding inventories, including the empty inventory. Token-inventory tolerance is zero within that catalog.

The catalog is deliberately constructed from the public equivalent-spelling vocabulary, including literal inventories for neutral arithmetic padding. It does not execute the tally, evaluate candidate expressions, inspect status vectors, use the commit identifier, or inspect counter labels or temporary paths. This is stronger than a size-only control, but it is still an order-blind lexical catalog, not a behavioral test.

The required tally hash command was run in the clone:

```text
python3 -c "import hashlib,sys;t=open(sys.argv[1]).read();s=t.find('  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n');e=t.find('\n}\n',s);print(hashlib.sha256(t[s:e+1].encode()).hexdigest())" tools/mutate-and-run.sh
```

Observed output:

```text
e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d
```

## Public v3 measurement

Working directory: the clone above. `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` were unset. `GIT_OPTIONAL_LOCKS=0`; `TMPDIR` was the clone's `.metadata-counter-tmp` directory. Exact executed argument vector, shown as a command:

```text
timeout -k 5 1500 python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/c1-measure-v3.py --repo /fast/scratch/hyaku/tameshi-r30a2-seats/CtlS7Metadata/clone --rev b90cd75f6cc1bae0a514383e52a51566bca1062e --jobs 4
```

Observed summary and exit:

```text
C1_R30: rev=b90cd75f6cc1bae0a514383e52a51566bca1062e pristine_selftest=1 harness=19/19 refused_drops=9/9 killed=13/13 equiv_pass=4/4 heldout_killed=12/12 heldout_equiv=4/4 insert_killed=8/8 insert_equiv=4/4
PREDICATE: C1_R30_PASS=true
V3_EXIT=0
```

Complete stdout and stderr are retained in the clone as `.metadata-v3.stdout` and `.metadata-v3.stderr`. The asynchronous tool attempt was refused before launch because the shared background job limit was full; the measurement above then completed synchronously.

## One mutation probe and exact restoration

Mutant: swap the `npass` and `nfail` arguments of the failure summary at `tools/mutate-and-run.sh:1441`:

```text
before:       "$nlegs" "$npass" "$nfail" "$nsetup"
after:        "$nlegs" "$nfail" "$npass" "$nsetup"
```

This changes one behavior-bearing argument line while preserving byte length, line count, and the complete token multiset. The expected detector is `--selftest`: a behavioral tally selftest should reject the incorrect failure summary.

The same bounded command was executed on pristine, mutated, and exactly restored working-tree bytes, with the same clone working directory and clean environment:

```text
timeout -k 5 300 bash tools/mutate-and-run.sh --selftest
```

Each run actually printed:

```text
TALLY_METADATA: PASS bytes=1562 lines=39 profiles=120 padding=973
MUTATE_SELFTEST: 98/98 pass
VERDICT: PASS
```

All three exited 0. Verdict: **survived**, not inconclusive; the pristine detector passed.

An independent use of public v3's `harness(text, ops, [1,0,0,0,0,0,0,0,0], tmp)` confirmed that the mutation changes the output. The harness scratch directory was inside the clone and was removed afterward:

```text
SUMMARY_PROBE pristine exit=1 output=REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)
SUMMARY_PROBE mutated exit=1 output=REGRESSION: FAIL (cases=9 passed=1 failed=8 setup=0)
SUMMARY_PROBE restored exit=1 output=REGRESSION: FAIL (cases=9 passed=8 failed=1 setup=0)
```

Runner hashes:

```text
pristine c28828703d0218e6a08d8bf314199908abbc23251af13145281ede3fcac0b53c
mutated  b5d93f658f5c1fdead26831ac9fc4e8641bed67e7c4200348b530e0712a44eb2
restored c28828703d0218e6a08d8bf314199908abbc23251af13145281ede3fcac0b53c
RESTORED_BYTES_EXACT=True
RESTORED_BLOCK_SHA256=e163133c0f54bb0cbd1c3f123e18b5efc17ced6df4558de034575089a8a2215d
```

The exact restored byte comparison used the saved pristine bytes, not only hashes. The temporary mutant was not committed and is not in the delivered diff. Probe stdout and stderr are retained in `.metadata-probe-{pristine,mutated,restored}.{stdout,stderr}` inside the clone. All invoked detector processes returned; no background run was launched and no process was killed.

## Smallest safe correction

Restore the frozen behavioral selftest hunk from `witness/fix.diff`. Its fixed vectors compare exact first-line output and exit status, so an order-blind metadata match is not substituted for checking tally behavior. No production correction was applied by this control seat.

Tool installs or updates: none.
