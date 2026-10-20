# R17 wave 2 — R16-OP1 attack: v2 evidence-disposition gate

Seat: RerunOP1. Target: R16-OP1 at `eb7838b16490ca7ba17ea3242ade76a61f744af2`.
All execution in a fleet-mirror clone under `/tmp/tameshi-r17w2-RerunOP1-nEwXsI`
(`git clone` of the lane + checkout detached at the landing rev). Lane repo was
never written; `git -C <clone> status --short` empty and HEAD unchanged after the
run. No tools installed or upgraded.

Artifact hashes at the landing rev:

| artifact | sha256 |
|---|---|
| `tools/evidence-disposition.py` | `f8f05c7aa601cf0b6f0907cc1ead2fc01acaad6a3c19e81888c084a969583e27` |
| `.ufo/evidence/round-17/dispositions.json` | `55cf1b5d2f7f7a153035362752e5f08f0bc49c2f504bbced501d5a884736a05f` |
| `.ufo/evidence/round-17/dispositions-before.json` | `79f0b397b727152b260df90e3ba9aa886d20eb7b5e5a43f6c3d03c7d3ee32354` |
| `.ufo/evidence/round-14/dispositions.json` | `77faac587f7c0c984d0d91a4096d3539467d422c15060b09f7c734c6d2809005` |
| `.ufo/evidence/round-13/verification.json` | `a02718e976382696b59f49e044b05af3d05fb0d5c964e4d218bfc6a2a033f06f` |
| `.ufo/evidence/round-13/expected.json` | `a016079438e96f39b2ef025052e786626bb553068fc0d2de93b96a09e5394336` |

## 1. Stated behavior — all three commands reproduce

### 1a. v2 final manifest (clean)

```
$ cd $C && python3 tools/evidence-disposition.py --root . \
    --dispositions .ufo/evidence/round-17/dispositions.json --json
EXIT=0
"status": "clean"
"counts": {"effective": 11, "expected_checks": 12, "failed": 0,
           "findings": 0, "passed": 11, "superseded": 1}
"historical_text": [
  "HISTORICAL tools/mutate-and-run.sh rev=4acc607d... sha256=75ed934d...",
  "HISTORICAL tools/pin-disposition.py rev=4acc607d... sha256=29725397..."
]
```

`producer_before` is reported `state: superseded`, `raw_expectation_failed: true`,
`raw_mismatches: ["expected_contains_missing"]`, replacements
`["producer_before_oracle","producer_after_oracle"]`; both oracle rows pass
(exit 1 and 0 respectively). Disposition arithmetic: 12 expected checks =
11 effective passes + 1 honestly superseded with the raw observation retained
and re-evaluated.

### 1b. `-before` manifest (must fail on producer_before)

```
$ python3 tools/evidence-disposition.py --root . \
    --dispositions .ufo/evidence/round-17/dispositions-before.json --json
EXIT=1
"status": "failed"
"counts": {"effective": 12, "expected_checks": 12, "failed": 1,
           "findings": 1, "passed": 11, "superseded": 0}
finding: {"id": "expected_contains_missing", "expectation": "producer_before",
          "detail": "producer_before: stdout lacks 'summary preserves
          top-level exposed declaration kind'"}
```

### 1c. Old round-14 v1 manifest (must be unreproducible)

```
$ python3 tools/evidence-disposition.py --root . \
    --dispositions .ufo/evidence/round-14/dispositions.json --json
EXIT=2
"id": "expected_input_digest_mismatch"
"message": "tools/mutate-and-run.sh: observed fb6d86d59b5c9285864c9ebfa19d5a6f8938e91c47877a6d25b451a1da03001a
            expects 75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5"
```

The v1 manifest pins the round-13-era runner; the live/committed runner is the
round-16/17-rewritten blob, so the old command cannot be made green without
editing evidence (`dispositions.json` v1 has no waiver mechanism). The registry
row `evidence-disposition-round14-superseded` still declares `expect.exit: 0`
(`tools/registry.json:250-275`); `registry-check.py` excludes superseded rows from
`held/total` and prints their observed outcome only (`tools/registry-check.py:30-40,544-563`),
so "reported superseded, got=2" is the honest reading — C2's wording holds, but
the row's own `expect` is a stale expectation rather than a live one.

## 2. Adversarial matrix (every mutation in its own clone copy)

| # | Mutation | Exit | Gate response |
|---|---|---|---|
| A1 | edit `.ufo/evidence/round-13/verification.json` (append one space) | 2 | `input_digest_mismatch`: observed `dd5e87ff...` expects `a02718e9...` |
| A17 | edit `.ufo/evidence/round-13/witness-metadata.json` | 2 | `expected_input_digest_mismatch`: observed `5d9aa412...` expects `46328227...` |
| A2 | edit `tools/witness-metadata.py` (unwaived expected input) | 2 | `expected_input_digest_mismatch`: observed `9acf051c...` expects `df339068...` |
| A3 | edit `tools/mutate-and-run.sh` uncommitted (waived path) | 2 | `historical_input_uncommitted`: "live bytes differ from HEAD:tools/mutate-and-run.sh" |
| A4 | edit `tools/mutate-and-run.sh` and **commit** it (`d1005c9`) | 0 | clean; `historical_text` still `75ed934d...`/`29725397...` — gate reads the pinned `4acc607d` blobs, not HEAD |
| A5 | point `mutate-and-run` rev at tree id `b40a9b8b4c90329fa9dd19fb70be94d5c9c4e61a` | 2 | `historical_input_unavailable`: "rev '...' does not resolve to that commit (got '')" |
| A6 | point rev at non-ancestor commit `7078fd35...` (root commit in clone) | 2 | `historical_input_unavailable`: "rev 7078fd... is not an ancestor of HEAD" |
| A7 | replace waived live path with a symlink | 2 | `historical_input_uncommitted`: "live path is absent or not a regular file but HEAD has an entry" |
| A8 | point rev at HEAD `eb7838b...` (live bytes then equal the rev) | 2 | `expected_input_digest_mismatch`: HEAD runner `fb6d86d5...` != pin `75ed934d...` |
| A9 | rev = abbreviated `4acc607d` | 2 | `dispositions_field_invalid`: "rev must be 40 lowercase hex characters" |
| A11 | add a waiver for unwaived `tools/witness-metadata.py` at `4acc607d` | 2 | `historical_input_unneeded`: live bytes still equal the pin; waiver refused |
| A10 | edit a round-13 receipt **and re-pin** it in the v2 manifest | 2 | `supersedes_mismatch`: "superseded input .ufo/evidence/round-13/verification.json is not pinned identically" |
| A12 | `git replace 4acc607d` with a commit carrying the HEAD tree (live replace ref) | 0 | clean; normal `git cat-file` shows replaced bytes `fb6d86d5...`, gate still reads original `75ed934d...` (`GIT_NO_REPLACE_OBJECTS`, `evidence-disposition.py:364-369,380-382`) |
| A13 | hostile `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE`/`GIT_OBJECT_DIRECTORY`/`GIT_CONFIG_GLOBAL` in env | 0 | clean; control `git rev-parse` under the same env exits 128 "not a git repository: '/tmp/evil-gitdir'" — the scrub is load-bearing and works |
| A14 | shallow clone (`--depth 1`, `--is-shallow-repository=true`) | 2 | `historical_input_unavailable`: "root is a shallow repository; historical blobs are not provable" |
| A16 | linked git worktree (`git_dir = <repo>/.git/worktrees/A16-wt`) | 2 | `historical_input_unavailable`: "git dir '...' is not <root>/.git" |

Mechanism citations: pin hashing is integrity-first and unconditional at
`tools/evidence-disposition.py:1493-1507`; expected inputs are re-hashed from
live or historical blobs at `:1529-1545`; repo identity/shallow guard `:409-438`;
rev exactness + ancestry `:441-459`; waiver necessity/commit check `:491-541`;
historical blob mode/type check `:543-557`.

**All five mandated vectors fail closed.** No mutation of evidence, unwaived
tool, uncommitted waived tool, or rev selector produced a false green.

## 3. Findings

### Blocking
None.

### Minor / residual risk

1. **`supersedes` is self-consistent, not anchored (A15).** I forged the
   `producer_before` stdout marker into `verification.json`, re-pinned it, copied
   `.ufo/evidence/round-14/dispositions-before.json` to
   `.ufo/evidence/round-17/fake-supersedes.json`, re-pinned the receipt in the
   copy, and re-pointed the `-before` manifest's `supersedes`+`inputs` at the
   copy. The gate then reports:
   `EXIT=0`, `status: clean`, `effective 12, failed 0, findings 0`,
   `producer_before: pass`, despite the receipt carrying a forged line and a
   stderr that still shows the original `FileNotFoundError`.
   `check_supersedes_lineage` (`tools/evidence-disposition.py:1412-1433`) only
   requires the named document to be v1 with equal `rows` and identically pinned
   `inputs`; the path is whatever the manifest names, so authoring a matching v1
   document defeats the "actually extends" intent. This requires rewriting the
   manifest itself, which is the reviewed/committed root of trust — outside the
   gate's stated tamper model, hence minor. If post-landing manifest edits are in
   scope, pin the manifest digest in the registry/QUALITY layer or compare
   `supersedes` against the known round-14 path. [INFERENCE] on intent.
2. **A committed edit to a waived tool is invisible by design (A4).** The gate
   reads `tools/mutate-and-run.sh` and `tools/pin-disposition.py` at the pinned
   `4acc607d` blobs; a later committed behavioural change is accepted as long as
   live==HEAD. That is correct for re-evaluating round-13 receipts, but it means
   this gate says nothing about the current runner/pin tool's behavior; their own
   selftests/registry rows must carry that. Advisory only.
3. **Registry expectation drift (informational, R16-MON1 scope).**
   `evidence-disposition-round14-superseded` expects exit 0 while the command now
   exits 2 (`tools/registry.json:250-275`). `registry-check.py` deliberately does
   not judge superseded rows, so the baseline verdict is unaffected; only a
   reader of the row alone could be misled.

## 4. Verdict

v2 disposition gate at `eb7838b`: **holds** — clean 11/1 on the landed manifest,
honest exit 1 on `producer_before`, exit 2 on the superseded round-14 command; all
five mandated lie vectors (round-13 evidence, unwaived tool, uncommitted/committed
waived tool, tree-id/non-ancestor rev) plus replace-ref, GIT_* env, shallow-repo,
worktree, symlink, unneeded-waiver and re-pin attempts fail closed (with
`supersedes`-document fabrication reported as a manifest-rewrite-only residual
risk).
