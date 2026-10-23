# MutateHead — landed selftest mutation probe

## Verdict

**7 killed; 11 survived; 0 inconclusive.** Of the survivors, three are equivalent for the landed control flow or input shape; eight demonstrate detector gaps, including one gap that requires an explicitly declared overcount stress. All twelve wave-A survivors named by the two assigned reports were replayed. The six wave-A tally defects are now killed; the equivalent guard rewrite still survives. The five wave-A harness survivors still survive, with three demonstrated losses of detector behavior.

Axis: **operability**. Probe dimensions: runnable detection, behavioral discrimination, and exact-byte restoration. Seat: **MutateHead**. These are mutation-probe outcomes, not a judgment or admission of exploratory C1. No contract, production code, or counter was changed.

## Evidence: revision, isolation, and exact commands

`S = /fast/scratch/hyaku/tameshi-r30a3-seats/MutateHead`; `C = S/c`; `R = C/tools/mutate-and-run.sh`.

Observed setup chain: exit 0, no stdout or stderr.
```sh
mkdir -p /fast/scratch/hyaku/tameshi-r30a3-seats/MutateHead && timeout 180 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /fast/scratch/hyaku/tameshi-r30a3-seats/MutateHead/c && timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/tameshi-r30a3-seats/MutateHead/c checkout -q --detach bb681566b18211adf8ae9c28df91e17678e3f545
```

Observed read-only identity command, working directory `C`:
```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0 git rev-parse HEAD && sha256sum tools/mutate-and-run.sh
```
```text
bb681566b18211adf8ae9c28df91e17678e3f545
a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9  tools/mutate-and-run.sh
```

Each mutant had its own `S/probes/<ID>/tools/mutate-and-run.sh`, copied byte-for-byte from R using `shutil.copy2`. Only that self-contained runner was copied; no sibling source was used. R itself remained pristine. Mutations and inverse restorations used surgical edits. At most four full detectors ran concurrently, each in its own mount/PID namespace and private `/tmp`. The process environment omitted GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE; the sandbox also cleared its environment.

For every ID in the results table, the following identical command ran on pristine, mutated, and restored bytes. `TREE` is exactly `S/probes/<ID>`; the Python subprocess working directory was C. The inner command is the requested bounded detector.
```sh
timeout 310 bwrap --unshare-all --die-with-parent --new-session --clearenv --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib /lib64 --symlink usr/bin /sbin --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp --setenv PATH /usr/bin --setenv HOME /w --setenv LANG C.UTF-8 --setenv TMPDIR /tmp --bind "$TREE" /w --chdir /w timeout 300 bash tools/mutate-and-run.sh --selftest
```

Python used `subprocess.run(command, cwd=C, env=clean_env, capture_output=True, text=True, timeout=320)`. Both streams were bounded by an assertion of fewer than 200,000 characters per invocation. All 54 invocations returned without timeout; all stderr was empty. All 18 pristine and all 18 restored outputs ended exactly:
```text
MUTATE_SELFTEST: 106/106 pass
VERDICT: PASS
```

### Expected detector and source locations

All following source pointers refer to the pristine pinned R, not drifting production bytes:

- Tally loop and three counter arms: `tools/mutate-and-run.sh:1432-1439`.
- FAIL before SETUP: `tools/mutate-and-run.sh:1441-1452`.
- Completeness guard: `tools/mutate-and-run.sh:1453-1461`.
- Independent assignment-name oracle: `tools/mutate-and-run.sh:1994-1997`.
- `tally_line` requires both exact first line and exit: `tools/mutate-and-run.sh:1998-2007`.
- All-pass and nine distinct singleton positions: `tools/mutate-and-run.sh:2008-2021`.
- New two-failure, two-setup, mixed FAIL/SETUP, and status-3 vectors: `tools/mutate-and-run.sh:2022-2032`.
- New missing-operand guard stress: `tools/mutate-and-run.sh:2033-2040`.

T01/T02 should fail the new guard stress; T03/T04/T05/T06 should fail their matching new vector; T07 should remain equivalent. N04 should make all four new vectors fail. The other probes attack what a green selftest does not distinguish; their concrete witnesses below establish the classification rather than treating survival alone as proof of a gap.

Prior-survivor correspondence is grounded in `.ufo/waves/round-30/wA/MutateTallyExtra.md:35-48` and `.ufo/waves/round-30/wA/MutateSelftestHarness.md:60-68,106-122`.

### Mutants and primary detector outputs

Every row has pristine exit 0 / 106 of 106 and restored exit 0 / 106 of 106. The mutated summary below is the exact `MUTATE_SELFTEST` value. All zero exits also printed `VERDICT: PASS`; all exit-1 rows printed `VERDICT: FAIL` with the exact temporary path recorded in the diagnostic section.

| ID | Smallest edit; R line | Mutated exit; summary | Verdict; classification |
|---|---|---|---|
| T01 | Delete only the six-line completeness guard (wave-A tally M01). `1456-1461` | 1; `MUTATE_SELFTEST: 105/106 pass` | **KILLED**. Killed: missing-operand stress fails. |
| T02 | Change guard != nlegs to > nlegs (wave-A tally M02). `1456` | 1; `MUTATE_SELFTEST: 105/106 pass` | **KILLED**. Killed: missing-operand stress fails. |
| T03 | Move the SETUP branch before the FAIL branch (wave-A tally M04). `1441-1452` | 1; `MUTATE_SELFTEST: 105/106 pass` | **KILLED**. Killed: mixed FAIL/SETUP vector fails. |
| T04 | Change nfail -gt 0 to nfail -eq 1 (wave-A tally M06). `1441` | 1; `MUTATE_SELFTEST: 105/106 pass` | **KILLED**. Killed: two-failure vector fails. |
| T05 | Change nsetup -gt 0 to nsetup -eq 1 (wave-A tally M07). `1447` | 1; `MUTATE_SELFTEST: 105/106 pass` | **KILLED**. Killed: two-setup vector fails. |
| T06 | Insert case arm 3) npass=$((npass + 1)) ;; (wave-A tally M08). `1437` | 1; `MUTATE_SELFTEST: 105/106 pass` | **KILLED**. Killed: status-3 vector fails. |
| T07 | Reduce guard predicate to npass != nlegs (wave-A tally M09). `1456` | 0; `MUTATE_SELFTEST: 106/106 pass` | **SURVIVED**. Equivalent at this control-flow point: failure/setup counts are zero whenever the guard is reached. |
| T08 | Insert case arm 4) npass=$((npass + 1)) ;;. `1437` | 0; `MUTATE_SELFTEST: 106/106 pass` | **SURVIVED**. Real tally coverage gap: status 4 is no longer SETUP; ordinary leg reachability of status 4 is not asserted. |
| H01 | Derive status names from tally operands instead of independent assignments (wave-A harness H3). `1995` | 0; `MUTATE_SELFTEST: 106/106 pass` | **SURVIVED**. Equivalent for this landed nine-name shape. Oracle independence is weakened, but this probe establishes no escaped drop with H01 alone. |
| H02 | Weaken the nine-name check to a nonempty-name check (wave-A harness H4). `1996` | 0; `MUTATE_SELFTEST: 106/106 pass` | **SURVIVED**. Equivalent for the current nine assignments. This is not presented as a demonstrated runtime false PASS. |
| H03 | Remove the exact first-line comparison; retain only exit comparison (wave-A harness H5a). `2006` | 0; `MUTATE_SELFTEST: 106/106 pass` | **SURVIVED**. Real helper coverage gap: exact result text is no longer checked; declared bad-label witness is accepted. |
| H04 | Add rc=$? after the comparison without returning rc (wave-A harness H5b). `2006-2007` | 0; `MUTATE_SELFTEST: 106/106 pass` | **SURVIVED**. Real helper coverage gap: the final assignment makes failed comparisons succeed; declared dropped-operand witness is accepted. |
| H05 | Repeat singleton position 7 instead of position 8 (wave-A harness H6). `2013` | 0; `MUTATE_SELFTEST: 106/106 pass` | **SURVIVED**. Real vector coverage gap: final-leg nonzero statuses are never exercised; declared final-leg normalization witness is accepted. |
| N01 | Delete only the new mixed 1,2 vector. `2026` | 0; `MUTATE_SELFTEST: 105/105 pass` | **SURVIVED**. Real vector coverage gap: mixed precedence is no longer tested; primary selftest silently shrinks to 105 cases. |
| N02 | Change the guard-stress short-circuit operator from && to ||. `2037` | 0; `MUTATE_SELFTEST: 106/106 pass` | **SURVIVED**. Real guard-stress coverage gap: a successful block change now skips the actual tally invocation while reporting PASS. |
| N03 | Change tally_line conjunction from && to ||. `2006` | 0; `MUTATE_SELFTEST: 106/106 pass` | **SURVIVED**. Real helper coverage gap: correct text masks a wrong exit; declared FAIL-exits-0 witness is accepted. |
| N04 | Quote the deliberately split new status-vector expansion. `2030` | 1; `MUTATE_SELFTEST: 102/106 pass` | **KILLED**. Killed: all four new status vectors fail. |
| N05 | Change guard != nlegs to < nlegs, checking undercounts only. `1456` | 0; `MUTATE_SELFTEST: 106/106 pass` | **SURVIVED**. Real guard-test gap under declared overcount stress; equivalent for the intact nine-operand loop. No ordinary nine-status false PASS is alleged. |

### Actual nonzero detector diagnostics

The following are all failing assertion lines and terminal summaries from the seven killed primary runs. Stderr was empty.

**T01**
```text
FAIL tally harness: loop missing one operand -> SETUP case-tally mismatch, exit 2
MUTATE_SELFTEST: 105/106 pass
VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.Cloeze)
```

**T02**
```text
FAIL tally harness: loop missing one operand -> SETUP case-tally mismatch, exit 2
MUTATE_SELFTEST: 105/106 pass
VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.DKI9Eq)
```

**T03**
```text
FAIL tally harness: statuses 1 2 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)
MUTATE_SELFTEST: 105/106 pass
VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.uJXk6R)
```

**T04**
```text
FAIL tally harness: statuses 1 1 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)
MUTATE_SELFTEST: 105/106 pass
VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.VcJQG4)
```

**T05**
```text
FAIL tally harness: statuses 2 2 0 0 0 0 0 0 0 -> REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)
MUTATE_SELFTEST: 105/106 pass
VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.Biduhl)
```

**T06**
```text
FAIL tally harness: statuses 3 0 0 0 0 0 0 0 0 -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)
MUTATE_SELFTEST: 105/106 pass
VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.tQ93ku)
```

**N04**
```text
FAIL tally harness: statuses 1 1 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=2 setup=0)
FAIL tally harness: statuses 2 2 0 0 0 0 0 0 0 -> REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)
FAIL tally harness: statuses 1 2 0 0 0 0 0 0 0 -> REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)
FAIL tally harness: statuses 3 0 0 0 0 0 0 0 0 -> REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)
MUTATE_SELFTEST: 102/106 pass
VERDICT: FAIL (scratch kept: /tmp/tameshi-r4-2-selftest.7tSgep)
```

## Evidence: survivor witnesses and equivalence boundary

The following supplemental probes do not change the primary killed/survived verdicts. They run only the actual extracted tally or the actual landed tally-harness section with one explicitly declared in-memory fault. They are not a second full selftest or a counter-family run. Each supplemental program was executed on pristine, saved mutated, and exact restored bytes. All 24 subprocesses returned with empty stderr; every restored result matched pristine in exit, complete stdout, and stderr.

Each command had this exact form, with C bound at /w and the generated program supplied on stdin:
```sh
timeout 30 bwrap --unshare-all --die-with-parent --new-session --clearenv --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/lib /lib --symlink usr/lib /lib64 --symlink usr/bin /sbin --ro-bind /etc /etc --proc /proc --dev /dev --tmpfs /tmp --setenv PATH /usr/bin --setenv HOME /w --setenv LANG C.UTF-8 --setenv TMPDIR /tmp --bind /fast/scratch/hyaku/tameshi-r30a3-seats/MutateHead/c /w --chdir /w timeout 20 bash -s
```

Python used `subprocess.run(command, input=program, cwd=C, env=clean_env, capture_output=True, text=True, timeout=40)`, asserting fewer than 100,000 output characters. No supplementary program file was written. The harness itself writes its normal tally script only inside the private temporary filesystem.

### Direct tally witnesses

Status names were independently extracted from the nine `st_*=$?` assignments before the tally, in order: `st_js st_kagi st_tsu st_mado st_checklist st_claims st_roundgate st_sourcescheck st_citecheck`.

| ID | Declared input or stress | Pristine / restored result | Mutated result |
|---|---|---|---|
| T08 | Status vector `4 0 0 0 0 0 0 0 0`; no second edit. | Exit 2; `REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)` | Exit 0; `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)` |
| N05 | All-zero status vector; duplicate only the final loop operand in the in-memory tally, producing ten counted iterations. This is a separate declared stress, not part of the primary mutant. | Exit 2; `REGRESSION: SETUP (case-tally mismatch: cases=9 counted=10)` | Exit 0; `REGRESSION: PASS (cases=9 passed=10; ledger legs exact: killed-delta<=0 flips<=0)` |

Each direct tally stdout had exactly one further line: `REGRESSION_WORKDIR: probe-tally (kept)`. The label is not a directory created or removed by the probe (`auto=0 KEEP=1`). N05 is therefore a guard coverage finding under overcount stress, not an assertion that the intact nine-operand loop currently overcounts. T08 is an actual wildcard-status difference without a second edit; no claim is made that a normal leg returns status 4.

### Actual tally-harness negative controls

These probes execute the source section beginning with `local tblock tgot tvec ti tj` through `tblock=$tblock_full`, with its actual `st()` accounting. Immediately after normal extraction, only tblock is overridden in memory with the declared behavioral fault. The original selftest comparisons and vectors are otherwise retained, except for the assigned harness mutation.

| Harness mutant | Explicit injected tally fault | Pristine exit / actual summary | Mutated exit / actual summary | Restored exit / actual summary |
|---|---|---|---|---|
| H03 | Replace tally output field `passed=%s` with `passing=%s`; exits remain correct. | 1 / `PROBE_HARNESS: 2/9 pass` | 0 / `PROBE_HARNESS: 9/9 pass` | 1 / `PROBE_HARNESS: 2/9 pass` |
| H04 | Remove the final tally-loop operand; leave runtime completeness guard intact. | 1 / `PROBE_HARNESS: 1/9 pass` | 0 / `PROBE_HARNESS: 9/9 pass` | 1 / `PROBE_HARNESS: 1/9 pass` |
| H05 | Set `st_citecheck=0` immediately after counter initialization, so the last leg is wrongly normalized to PASS. | 1 / `PROBE_HARNESS: 7/9 pass` | 0 / `PROBE_HARNESS: 9/9 pass` | 1 / `PROBE_HARNESS: 7/9 pass` |
| N01 | Use T03’s SETUP-before-FAIL block. | 1 / `PROBE_HARNESS: 8/9 pass` | 0 / `PROBE_HARNESS: 8/8 pass` | 1 / `PROBE_HARNESS: 8/9 pass` |
| N02 | Use T01’s block with its completeness guard removed. | 1 / `PROBE_HARNESS: 8/9 pass` | 0 / `PROBE_HARNESS: 9/9 pass` | 1 / `PROBE_HARNESS: 8/9 pass` |
| N03 | Change only the tally FAIL branch exit from 1 to 0, leaving its exact first line intact. | 1 / `PROBE_HARNESS: 6/9 pass` | 0 / `PROBE_HARNESS: 9/9 pass` | 1 / `PROBE_HARNESS: 6/9 pass` |

For H05, both pristine and restored singleton families reported `(8/9)` and failed; the mutated helper reported both `(9/9)` despite never exercising position 8. For N01, the mixed-precedence failure disappeared entirely. For N02, the missing-operand guard failure became PASS without executing `tally_line` at that site. These are real losses of detector behavior, not equivalent refactorings. H04 still swallows comparison failures after the new vectors and guard stress landed.

T07 is equivalent because both positive failure and setup counts exit before its guard; at that point the removed terms are zero. H01 and H02 are equivalent only for this landed input shape: both name derivations produce nine names and the weakened cardinality assertion receives nine. Their survival is not credited as an escaped production defect. The independent-oracle weakening in H01 remains a design concern, but no additional claim is inferred.

### Exact supplemental construction

The following is the construction actually executed in Python Eval. `pristine`, `mutated_bytes[ID]`, and `restored_bytes[ID]` are the complete runner bytes measured in the hash table below; `text = pristine.decode()`. `shell_probe` used the exact subprocess command above. This records the complete stdin recipe without depending on a temporary helper file.
```python
start_line = '  local nlegs=9 npass=0 nfail=0 nsetup=0 st\n'
def block(raw):
    s = raw.decode() if isinstance(raw, bytes) else raw
    a = s.index(start_line)
    return s[a:s.index('\n}\n', a) + 1]
baseblock = block(pristine)
regression_prefix = text[text.index('run_regression() {'):text.index(start_line)]
status_names = re.findall(r'^  (st_[a-z]+)=\$\?$', regression_prefix, re.M)
assert len(status_names) == 9

def tally_program(raw, statuses, stress=None):
    tb = block(raw)
    if stress == 'duplicate-last':
        old = ' "$st_citecheck"; do\n' 
        assert tb.count(old) == 1
        tb = tb.replace(old, ' "$st_citecheck" "$st_citecheck"; do\n', 1)
    decl = ' '.join(n + '=' + str(v) for n, v in zip(status_names, statuses))
    return 'set -u -o pipefail\ntally() {\n  local ' + decl + '\n  local root=probe-tally auto=0 KEEP=1\n' + tb + '}\ntally\n'

st_impl = text[text.index('  st() { # st <name> <rc>'):text.index('\n\n  local fx=', text.index('  st() { # st <name> <rc>'))]
extract_line = '  tblock=$(awk ' + shlex.quote('/^  local nlegs=9 npass=0 nfail=0 nsetup=0 st$/{f=1} f&&/^}$/{exit} f') + ' "$SELF")\n' 
assert text.count(extract_line) == 1

def tally_harness_program(raw, injected_block):
    s = raw.decode()
    a = s.index('  local tblock tgot tvec ti tj\n')
    b = s.index('\n\n  bash "$SELF" --help', a)
    harness = s[a:b] + '\n'
    assert harness.count(extract_line) == 1
    harness = harness.replace(extract_line, extract_line + '  tblock=' + shlex.quote(injected_block) + '\n', 1)
    return 'set -u -o pipefail\nSELF=/w/tools/mutate-and-run.sh\nprobe() {\n  local root\n  root=$(mktemp -d /tmp/mutatehead-harness.XXXXXX)\n  local cases=0 failed=0\n' + st_impl + '\n' + harness + "  printf 'PROBE_HARNESS: %s/%s pass\\n' \"$((cases - failed))\" \"$cases\"\n  [[ $failed -eq 0 ]]\n}\nprobe\n"

faults = {
    'H03': baseblock.replace('passed=%s', 'passing=%s'),
    'H04': baseblock.replace(' "$st_citecheck"; do\n', '; do\n', 1),
    'H05': baseblock.replace(start_line, start_line + '  st_citecheck=0\n', 1),
    'N01': block(mutated_bytes['T03']),
    'N02': block(mutated_bytes['T01']),
    'N03': baseblock.replace('    exit 1\n', '    exit 0\n', 1),
}
```

### Separation from counter families

Only the public v4 implementation was inspected, not invoked: `.ufo/evidence/round-30/c1-measure-v4.py:102-107,143-207,213-252,375-417`. Its listed defect families alter drops, counter arms, thresholds rejecting singleton statuses, or inserted constant counter terms. These probes instead target guard predicates/control flow, verdict precedence, multi-leg equality thresholds, extra status arms, or the selftest itself. None is the exact public generator edit shape. All tally survivors from wave A match pristine on the counter’s nineteen ordinary vectors; the counter sanity rule at lines 409-417 requires every accepted generated or sealed defect to differ on at least one of those vectors. Selftest-only edits also leave those tally observations unchanged. No sealed payload or sealed directory was opened, searched, listed, or recovered; no assertion about an unknown payload’s text is made.

## Evidence: hashes and restoration

`P = a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` is the SHA-256 of the complete runner file. All before and after entries are full-file hashes, not tally-only hashes. The initial bytes were preserved in memory; after inverse surgical edits, direct comparison `restored_bytes[ID] == pristine` was true for every ID. The same full detector then passed on each restored copy. SHA-256 was collected immediately before and after every detector invocation; no invocation changed its source bytes.

| ID | Before SHA-256 | Mutated SHA-256 | After SHA-256 | Exact byte equality; restored detector |
|---|---|---|---|---|
| T01 | P | `cb1dc1cd4e595f1cbcea2802487c7fdbe3021f6d6dcfe18c99311d67ea74d4ce` | P | true; exit 0, 106/106, PASS |
| T02 | P | `6638bb0a5331fb6bb97f33aa0c46358d7d6bd76f11c9ebd3c9812f9ae4a16e86` | P | true; exit 0, 106/106, PASS |
| T03 | P | `a1bebeebb418eca3b394946271143638853919be9f0985d0a96ff5798da8d02f` | P | true; exit 0, 106/106, PASS |
| T04 | P | `642ede6b251259cfddf40487fbefe247cb72bc9d7b65e9e52d5be9c578776431` | P | true; exit 0, 106/106, PASS |
| T05 | P | `b85ab3902bb16e681745fd61ee5263091e644b012f55bcc263c95e76dbf119d7` | P | true; exit 0, 106/106, PASS |
| T06 | P | `337431d8b9dc6327b8b5ed27e29b8b67773468a60f9ac8f76b7b95eab0087fdb` | P | true; exit 0, 106/106, PASS |
| T07 | P | `91066af826f69ecb6e6ccb0e837b3e2a37c1edfc6bf0aefb0c78e378bb1eeb28` | P | true; exit 0, 106/106, PASS |
| T08 | P | `12ad1d9076a55050624f0b104475afe95c1d89ede35245a345a1e2bbb03ee27b` | P | true; exit 0, 106/106, PASS |
| H01 | P | `3620f636ed2c0f5b6fb3aa907ea0e7a5cc9d24ea4d3939e2b7f328c2b4ff5ece` | P | true; exit 0, 106/106, PASS |
| H02 | P | `df5608b593e40b1880efb92afbe4fd301b90b889f8e7acac6e10fbc39a2d22ae` | P | true; exit 0, 106/106, PASS |
| H03 | P | `2ac4ce5344e6100a5980a2d44bbc4983562df5a0325ecf84610973094322f35c` | P | true; exit 0, 106/106, PASS |
| H04 | P | `0dc1e6b07452f6108f9dd7f99050aa0d8b8450456c3424f22da1a7fc54e5d6cd` | P | true; exit 0, 106/106, PASS |
| H05 | P | `adf6763d6524f342b5496ff52f0fce96e0b4a00b5ab26cfa43be2001654b36d0` | P | true; exit 0, 106/106, PASS |
| N01 | P | `c0a32ec4e69d3cb07a7949efb7c9a83ac2b4b431f6e4da3f8bd76a1cd0d4cb34` | P | true; exit 0, 106/106, PASS |
| N02 | P | `31128639afc3e57a0d68f0abe94cc5038954ff41d6f9949da4fa903331f56250` | P | true; exit 0, 106/106, PASS |
| N03 | P | `741907e82ca7e907881cb985b7a504771de78d14b1179530661066a8f22a5b6f` | P | true; exit 0, 106/106, PASS |
| N04 | P | `29e8cf6859ddef8a622e1a2e084c09e226249e675b9363b28b8edc8c251c0b9c` | P | true; exit 0, 106/106, PASS |
| N05 | P | `e1ef181c1e621962cf19574a0683109ee094387306af1766df14b215413929fe` | P | true; exit 0, 106/106, PASS |

All 24 supplemental payload SHA-256 values are recorded below. Identical pristine/restored payload hashes corroborate that the same supplemental detector was used after restoration.

| Probe | Pristine payload | Mutated payload | Restored payload |
|---|---|---|---|
| T08 | `32900c43ee267ef5febca3518dbc596050065c8947ac0ba472eb846027e116bb` | `e651d165e7c07cef1b172502f209956ccde7af58a5588a219cd21fe48195b132` | `32900c43ee267ef5febca3518dbc596050065c8947ac0ba472eb846027e116bb` |
| N05 | `9d7e63acd0344bfcffea0d14eb72d9fc3fdc36583b58806bb5c1b61891979275` | `0c6c2a4f2c695b90cf18cb5c127660209c2e1cc00ba995f5777c215c1a1a45c0` | `9d7e63acd0344bfcffea0d14eb72d9fc3fdc36583b58806bb5c1b61891979275` |
| H03 | `1a710877f982895334c317b6c779edb509b73099c9d8a294564890d463ac7687` | `e5bda46c29f3fcf3dafab8ad1eaf801f8d3448214da6fb7e6996d4a0e3b54814` | `1a710877f982895334c317b6c779edb509b73099c9d8a294564890d463ac7687` |
| H04 | `b296d8988d6845531834434821542f4ebc3e35a26c485eec37cba7e186f0049c` | `445fe64b1da7b9e5b689ee9178a05dccf6482a97e0fef000205348a03b692810` | `b296d8988d6845531834434821542f4ebc3e35a26c485eec37cba7e186f0049c` |
| H05 | `cfcfea8bc5996c6d4d859016b6703a4cc5a3c2f9f5a1e083bb75746f96e8a6cd` | `5141133757de43ab84a4410213369383f9303c9f89e1e21b5060656fdbfa50b8` | `cfcfea8bc5996c6d4d859016b6703a4cc5a3c2f9f5a1e083bb75746f96e8a6cd` |
| N01 | `24fcc697f5250a646d339256cda368fc43cdee3b705939196ab630c37141d642` | `e84e13fc35cacbbb20a68d816b321e06bc281e3bc91d296b8a763d1a9ded87cc` | `24fcc697f5250a646d339256cda368fc43cdee3b705939196ab630c37141d642` |
| N02 | `7b40dd97931c71f808ef874d0b448678efb5f363bed7dc164e99b16728e7d4cf` | `e588ebf6033aabc2d86efd72221bfda999b01f6ad64a121ca74ef90c04df9d08` | `7b40dd97931c71f808ef874d0b448678efb5f363bed7dc164e99b16728e7d4cf` |
| N03 | `e0491be5a1cd15278d83d12352298e7fbb160c5cdb8bbc6b6a43dd4ef0dee2d2` | `3e62a8da0b5652e38678cad337c7d40e15a5a14917c608d052be6c7654776c46` | `e0491be5a1cd15278d83d12352298e7fbb160c5cdb8bbc6b6a43dd4ef0dee2d2` |

Process closure: all subprocess.run calls returned; the four-worker executor was shut down with `pool.shutdown(wait=True)`. A final `ps -o pid,ppid,args --ppid 382390` returned exit 0 with only its own ps child:
```text
    PID    PPID COMMAND
1360067  382390 ps -o pid,ppid,args --ppid 382390
```

Bubblewrap used a private PID namespace and `--die-with-parent` for every run; no background service was started and no kill was issued. No process outside this seat was inspected for termination or killed. Private temporary files disappeared with their namespaces. Scratch runner copies remain restored.

No production source, sibling repository, fleet state, lane Git index, or jj state was changed. The only lane output is this report. Git clone and detached checkout ran only in the assigned scratch tree. No subagent, model, alternate agent runtime, v4 counter, or full fleet --regression replay was invoked. The requested selftests did run their own local fixture sweeps. Existing bubblewrap 0.13.1 was used. Tools installed or updated: none. `df -h /fast` before cloning reported 223G available (73% used).

## Exact transient mutation diffs

These diffs reconstruct the bytes actually tested. Every corresponding scratch runner is now back at P.

### T01

```diff
--- T01/pristine/tools/mutate-and-run.sh
+++ T01/mutated/tools/mutate-and-run.sh
@@ -1455,8 +1455,2 @@
   # of a mutation report are sums of its per-state counts).
-  if (( npass + nfail + nsetup != nlegs )); then
-    printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\n' \
-      "$nlegs" "$((npass + nfail + nsetup))"
-    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
-    exit 2
-  fi
   printf 'REGRESSION: PASS (cases=%s passed=%s; ledger legs exact: killed-delta<=0 flips<=0)\n' \
```

### T02

```diff
--- T02/pristine/tools/mutate-and-run.sh
+++ T02/mutated/tools/mutate-and-run.sh
@@ -1455,3 +1455,3 @@
   # of a mutation report are sums of its per-state counts).
-  if (( npass + nfail + nsetup != nlegs )); then
+  if (( npass + nfail + nsetup > nlegs )); then
     printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\n' \
```

### T03

```diff
--- T03/pristine/tools/mutate-and-run.sh
+++ T03/mutated/tools/mutate-and-run.sh
@@ -1440,2 +1440,8 @@
 
+  if [[ $nsetup -gt 0 ]]; then
+    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\n' \
+      "$nlegs" "$npass" "$nsetup"
+    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
+    exit 2
+  fi
   if [[ $nfail -gt 0 ]]; then
@@ -1445,8 +1451,2 @@
     exit 1
-  fi
-  if [[ $nsetup -gt 0 ]]; then
-    printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\n' \
-      "$nlegs" "$npass" "$nsetup"
-    printf 'REGRESSION_WORKDIR: %s (kept)\n' "$root"
-    exit 2
   fi
```

### T04

```diff
--- T04/pristine/tools/mutate-and-run.sh
+++ T04/mutated/tools/mutate-and-run.sh
@@ -1440,3 +1440,3 @@
 
-  if [[ $nfail -gt 0 ]]; then
+  if [[ $nfail -eq 1 ]]; then
     printf 'REGRESSION: FAIL (cases=%s passed=%s failed=%s setup=%s)\n' \
```

### T05

```diff
--- T05/pristine/tools/mutate-and-run.sh
+++ T05/mutated/tools/mutate-and-run.sh
@@ -1446,3 +1446,3 @@
   fi
-  if [[ $nsetup -gt 0 ]]; then
+  if [[ $nsetup -eq 1 ]]; then
     printf 'REGRESSION: SETUP (cases=%s passed=%s cannot-verify=%s)\n' \
```

### T06

```diff
--- T06/pristine/tools/mutate-and-run.sh
+++ T06/mutated/tools/mutate-and-run.sh
@@ -1436,2 +1436,3 @@
       1) nfail=$((nfail + 1)) ;;
+      3) npass=$((npass + 1)) ;;
       *) nsetup=$((nsetup + 1)) ;;
```

### T07

```diff
--- T07/pristine/tools/mutate-and-run.sh
+++ T07/mutated/tools/mutate-and-run.sh
@@ -1455,3 +1455,3 @@
   # of a mutation report are sums of its per-state counts).
-  if (( npass + nfail + nsetup != nlegs )); then
+  if (( npass != nlegs )); then
     printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\n' \
```

### T08

```diff
--- T08/pristine/tools/mutate-and-run.sh
+++ T08/mutated/tools/mutate-and-run.sh
@@ -1436,2 +1436,3 @@
       1) nfail=$((nfail + 1)) ;;
+      4) npass=$((npass + 1)) ;;
       *) nsetup=$((nsetup + 1)) ;;
```

### H01

```diff
--- H01/pristine/tools/mutate-and-run.sh
+++ H01/mutated/tools/mutate-and-run.sh
@@ -1994,3 +1994,3 @@
   tblock=$(awk '/^  local nlegs=9 npass=0 nfail=0 nsetup=0 st$/{f=1} f&&/^}$/{exit} f' "$SELF")
-  mapfile -t tnames < <(awk '/^run_regression\(\) \{$/{f=1} /^  local nlegs=9 npass=0 nfail=0 nsetup=0 st$/{f=0} f&&/^  st_[a-z]+=\$\?$/{sub(/^  /,""); sub(/=\$\?$/,""); print}' "$SELF")
+  mapfile -t tnames < <(awk '/^  for st in /{for (i=4; i<NF; i++) {s=$i; gsub(/["$;]/,"",s); print s}}' "$SELF")
   [[ -n "$tblock" && ${#tnames[@]} -eq 9 ]]
```

### H02

```diff
--- H02/pristine/tools/mutate-and-run.sh
+++ H02/mutated/tools/mutate-and-run.sh
@@ -1995,3 +1995,3 @@
   mapfile -t tnames < <(awk '/^run_regression\(\) \{$/{f=1} /^  local nlegs=9 npass=0 nfail=0 nsetup=0 st$/{f=0} f&&/^  st_[a-z]+=\$\?$/{sub(/^  /,""); sub(/=\$\?$/,""); print}' "$SELF")
-  [[ -n "$tblock" && ${#tnames[@]} -eq 9 ]]
+  [[ -n "$tblock" && ${#tnames[@]} -gt 0 ]]
   st "tally harness: block extracted, leg status names=${#tnames[@]} (want 9)" $?
```

### H03

```diff
--- H03/pristine/tools/mutate-and-run.sh
+++ H03/mutated/tools/mutate-and-run.sh
@@ -2005,3 +2005,3 @@
     rc=$?
-    [[ $rc -eq $want_rc && "${out%%$'\n'*}" == "$want_line" ]]
+    [[ $rc -eq $want_rc ]]
   }
```

### H04

```diff
--- H04/pristine/tools/mutate-and-run.sh
+++ H04/mutated/tools/mutate-and-run.sh
@@ -2006,2 +2006,3 @@
     [[ $rc -eq $want_rc && "${out%%$'\n'*}" == "$want_line" ]]
+    rc=$?
   }
```

### H05

```diff
--- H05/pristine/tools/mutate-and-run.sh
+++ H05/mutated/tools/mutate-and-run.sh
@@ -2012,3 +2012,3 @@
     tgot=0
-    for ti in 0 1 2 3 4 5 6 7 8; do
+    for ti in 0 1 2 3 4 5 6 7 7; do
       local -a tst=(0 0 0 0 0 0 0 0 0)
```

### N01

```diff
--- N01/pristine/tools/mutate-and-run.sh
+++ N01/mutated/tools/mutate-and-run.sh
@@ -2025,3 +2025,2 @@
     '2 2 0 0 0 0 0 0 0:2:REGRESSION: SETUP (cases=9 passed=7 cannot-verify=2)' \
-    '1 2 0 0 0 0 0 0 0:1:REGRESSION: FAIL (cases=9 passed=7 failed=1 setup=1)' \
     '3 0 0 0 0 0 0 0 0:2:REGRESSION: SETUP (cases=9 passed=8 cannot-verify=1)'; do
```

### N02

```diff
--- N02/pristine/tools/mutate-and-run.sh
+++ N02/mutated/tools/mutate-and-run.sh
@@ -2036,3 +2036,3 @@
   tblock=$(printf '%s\n' "$tblock_full" | sed -E '0,/^  for st in /s/ "\$st_[a-z]+"; do$/; do/')
-  [[ "$tblock" != "$tblock_full" ]] &&
+  [[ "$tblock" != "$tblock_full" ]] ||
     tally_line 2 'REGRESSION: SETUP (case-tally mismatch: cases=9 counted=8)' 0 0 0 0 0 0 0 0 0
```

### N03

```diff
--- N03/pristine/tools/mutate-and-run.sh
+++ N03/mutated/tools/mutate-and-run.sh
@@ -2005,3 +2005,3 @@
     rc=$?
-    [[ $rc -eq $want_rc && "${out%%$'\n'*}" == "$want_line" ]]
+    [[ $rc -eq $want_rc || "${out%%$'\n'*}" == "$want_line" ]]
   }
```

### N04

```diff
--- N04/pristine/tools/mutate-and-run.sh
+++ N04/mutated/tools/mutate-and-run.sh
@@ -2029,3 +2029,3 @@
     # shellcheck disable=SC2086 # the status list splits into nine arguments on purpose
-    tally_line "${tj%%:*}" "${tj#*:}" ${tvec%%:*}
+    tally_line "${tj%%:*}" "${tj#*:}" "${tvec%%:*}"
     st "tally harness: statuses ${tvec%%:*} -> ${tj#*:}" $?
```

### N05

```diff
--- N05/pristine/tools/mutate-and-run.sh
+++ N05/mutated/tools/mutate-and-run.sh
@@ -1455,3 +1455,3 @@
   # of a mutation report are sums of its per-state counts).
-  if (( npass + nfail + nsetup != nlegs )); then
+  if (( npass + nfail + nsetup < nlegs )); then
     printf 'REGRESSION: SETUP (case-tally mismatch: cases=%s counted=%s)\n' \
```

## Smallest safe correction

No correction was applied: this is a scoped mutation probe, and every mutant was restored. Preserve the frozen contract and existing passing checks. For a later explicitly authorized hardening change, the smallest corrections are:

- Keep the exact first-line **and** exit comparison as the final result of `tally_line`; do not append a successful assignment without explicitly returning the captured comparison status. Add negative helper cases for correct-exit/wrong-line, wrong-exit/correct-line, and both wrong. These address H03, H04, and N03 without changing tally semantics.
- Check that the singleton position set has nine distinct entries and retain all four new vectors, rather than trusting only a success count or a shrinking selftest denominator. These address H05 and N01.
- Do not let the guard-stress block-change assertion short-circuit past the actual behavioral check. Retain the declared undercount case, and add an explicit duplicate-operand overcount case if both sides of the existing mismatch guard are to be protected. These address N02 and the stress-bounded N05 finding.
- If wildcard status behavior is part of the intended tested surface, include status 4 as a second representative beyond status 3. T08 does not establish ordinary leg reachability or authorize a broader claim.

T07 needs no correction; H01 and H02 are reported as equivalent for the landed shape, not forced kills. These findings do not change C1’s exploratory status or constitute a shipping decision.
