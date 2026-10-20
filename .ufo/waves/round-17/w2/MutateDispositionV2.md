# MutateDispositionV2 — round 17, wave 2

## Scope and axes

- **Depth:** isolate the behavior-bearing v2 guards and distinguish rejection changes from false-clean admissions.
- **Calibration:** challenge `--selftest` sensitivity without treating a passing baseline as proof of complete guard coverage.
- Target: `tools/evidence-disposition.py` at `eb7838b16490ca7ba17ea3242ade76a61f744af2`.
- Nine independent one-defect mutants cover the seven requested guard groups; G3 commit/ancestor and G4 environment/replace-ref protections are split so one check cannot conceal the other.
- No production fix, integration, round judgment, subagent dispatch, REA, omp CLI, or sibling-source mutation. The only lane write is this report. Git writes occurred only in `/tmp` clone/fixture repositories.

## Result

**`--selftest`: 7 killed, 2 survived, 0 inconclusive. Both survivors are non-equivalent.** Every per-copy pristine and restored run exited 0 with `SELFTEST: PASS (56/56)`; the two survivor mutants also exited 0 with the same summary. Separate identical-input CLI witnesses distinguish both survivors from pristine/restored behavior. Those witnesses do not retroactively count as selftest kills.

## Commands and execution bounds

Assigned scratch root: `/tmp/tameshi-r17w2-MutateDispositionV2-bSsY3J`. Original mirror: `/tmp/tameshi-r17w2-MutateDispositionV2-bSsY3J/fleet/tameshi-shokunin`.

The required fleet mirror was created with the following shell sequence (exit 0); each independent mutant mirror repeated the sibling-link layout and cloned the pinned original mirror, then detached at the same landing (setup exit 0):

```sh
W=$(mktemp -d /tmp/tameshi-r17w2-MutateDispositionV2-XXXXXX)
mkdir "$W/fleet"
for s in /home/vgpnk/Projects/shokunin/*-shokunin; do
  [ "$s" = /home/vgpnk/Projects/shokunin/tameshi-shokunin ] || ln -s "$s" "$W/fleet/"
done
git clone -q /home/vgpnk/Projects/shokunin/tameshi-shokunin "$W/fleet/tameshi-shokunin"
git -C "$W/fleet/tameshi-shokunin" checkout -q --detach eb7838b16490ca7ba17ea3242ade76a61f744af2
```

For each name in the table below, the exact same detector command was run before mutation, while mutated, and after restoration, from that mirror root:

```sh
W=/tmp/tameshi-r17w2-MutateDispositionV2-bSsY3J
# NAME = G1 G2 G3Commit G3Ancestor G4Env G4Replace G5Mode G7Rows ToolsPrefix
C="$W/$NAME/fleet/tameshi-shokunin"
sha256sum "$C/tools/evidence-disposition.py"
 timeout 180s python3 "$C/tools/evidence-disposition.py" --selftest
sha256sum "$C/tools/evidence-disposition.py"
```

There were 27 matrix selftest executions, plus one initial pristine reconnaissance selftest (also exit 0, 56/56). Independent mirrors were measured concurrently; every worker joined before editing/restoration. No background jobs were used. The outer subprocess deadline was 190 seconds; no detector timed out. `sha256sum` calls before and after every matrix detector exited 0, and every detector left its tested source unchanged.

Unmodified selftest code allocates its own `/tmp/tameshi-r14-evidence-disposition-selftest.*` fixtures (`tools/evidence-disposition.py:2083`) and retains them on failure (`:2769-2773`); those locations appear verbatim in the outputs below. Manually created mirrors, supplementary fixtures, detector script, and raw receipt file are under the assigned scratch root.

## Kill table

Locations refer to pristine `tools/evidence-disposition.py` at the landing, not shifted mutant line numbers. `P/M/R` are actual selftest process exits for pristine/mutated/restored bytes.

| Mutant | Source path:line | Single defect | Expected detector case | P/M/R | Selftest verdict |
|---|---|---|---|---|---|
| G1 | `tools/evidence-disposition.py:513` | `if live is not None and sha256_bytes(live) == pin:` → `if False:` | `v2-historical-unneeded` | 0/1/0 | killed |
| G2 | `tools/evidence-disposition.py:518-540` | Insert `return` immediately before the HEAD/worktree checks at line 518; retain G1 | `v2-historical-uncommitted` | 0/1/0 | killed |
| G3Commit | `tools/evidence-disposition.py:445` | `if proc.returncode != 0 or resolved != rev:` → `if False:`; retain ancestry check | `v2-historical-tree-id (incomplete exact-object coverage)` | 0/0/0 | survived; non-equivalent |
| G3Ancestor | `tools/evidence-disposition.py:451` | `if proc.returncode != 0:` after `merge-base` → `if False:`; retain exact commit check | `v2-historical-dangling` | 0/1/0 | killed |
| G4Env | `tools/evidence-disposition.py:381` | Filtered environment comprehension → `env = dict(os.environ)`; retain overrides | `v2-gitdir-env` | 0/1/0 | killed |
| G4Replace | `tools/evidence-disposition.py:365` | Remove only `"GIT_NO_REPLACE_OBJECTS": "1",` from overrides | `v2-historical-replace-ref` | 0/1/0 | killed |
| G5Mode | `tools/evidence-disposition.py:552` | `if kind != "blob" or mode not in TREE_MODES:` → `if kind != "blob":` | `No dedicated non-regular-mode case; CRLF case tests bytes, not mode` | 0/0/0 | survived; non-equivalent |
| G7Rows | `tools/evidence-disposition.py:1420-1421` | Rows-equality conditional → `if False:`; retain schema/path/input-pin lineage checks | `v2-supersedes-rows-mismatch` | 0/1/0 | killed |
| ToolsPrefix | `tools/evidence-disposition.py:594` | `if not canonical.startswith("tools/"):` → `if False:` | `v2-historical-forbidden` | 0/1/0 | killed |

### Actual key mutant output

```text
[G1] process exit=1
SELFTEST_CASE v2-historical-unneeded FAIL (exit=0 expects=2; ids=[] expects=['historical_input_unneeded']; payload exit=0; status='clean' expects='could_not_evaluate')
SELFTEST: FAIL (1/56 failed: v2-historical-unneeded; fixtures kept at /tmp/tameshi-r14-evidence-disposition-selftest.6uu637ki)
[G2] process exit=1
SELFTEST_CASE v2-historical-uncommitted FAIL (exit=0 expects=2; ids=[] expects=['historical_input_uncommitted']; payload exit=0; status='clean' expects='could_not_evaluate')
SELFTEST: FAIL (1/56 failed: v2-historical-uncommitted; fixtures kept at /tmp/tameshi-r14-evidence-disposition-selftest.fupg7av6)
[G3Commit] process exit=0
SELFTEST: PASS (56/56)
[G3Ancestor] process exit=1
SELFTEST_CASE v2-historical-dangling FAIL (ids=['expected_input_digest_mismatch'] expects=['historical_input_unavailable'])
SELFTEST: FAIL (1/56 failed: v2-historical-dangling; fixtures kept at /tmp/tameshi-r14-evidence-disposition-selftest.gtuqrpba)
[G4Env] process exit=1
SELFTEST_CASE v2-gitdir-env FAIL (exit=2 expects=0; ids=['historical_input_unavailable'] expects=[]; payload exit=2; status='could_not_evaluate' expects='clean'; informational=[])
SELFTEST: FAIL (1/56 failed: v2-gitdir-env; fixtures kept at /tmp/tameshi-r14-evidence-disposition-selftest._gw3e85k)
[G4Replace] process exit=1
SELFTEST_CASE v2-historical-replace-ref FAIL (exit=2 expects=0; ids=['historical_input_unavailable'] expects=[]; payload exit=2; status='could_not_evaluate' expects='clean'; informational=[])
SELFTEST: FAIL (1/56 failed: v2-historical-replace-ref; fixtures kept at /tmp/tameshi-r14-evidence-disposition-selftest.ghv6kq45)
[G5Mode] process exit=0
SELFTEST: PASS (56/56)
[G7Rows] process exit=1
SELFTEST_CASE v2-supersedes-rows-mismatch FAIL (exit=0 expects=2; ids=[] expects=['supersedes_mismatch']; payload exit=0; status='clean' expects='could_not_evaluate')
SELFTEST: FAIL (1/56 failed: v2-supersedes-rows-mismatch; fixtures kept at /tmp/tameshi-r14-evidence-disposition-selftest.mzxqf0e2)
[ToolsPrefix] process exit=1
SELFTEST_CASE v2-historical-forbidden FAIL (ids=['historical_input_unavailable'] expects=['historical_input_forbidden'])
SELFTEST: FAIL (1/56 failed: v2-historical-forbidden; fixtures kept at /tmp/tameshi-r14-evidence-disposition-selftest.z0qkuozq)
```

All matrix stderr streams were empty.

### What the kills establish—and do not

- G1, G2, and G7 removals cause their invalid fixture to become `exit=0`, `status=clean`, `ids=[]`. These are direct false-clean kills.
- G3Ancestor is killed only because its finding changes from `historical_input_unavailable` to `expected_input_digest_mismatch`; tool exit remains 2. Its dangling fixture uses HEAD’s already-drifted tool bytes (`tools/evidence-disposition.py:2002-2010`), so this kill does **not** demonstrate acceptance of a dangling commit containing the pinned bytes.
- ToolsPrefix is likewise a finding-ID kill: tool exit remains 2. Its forbidden-path fixture uses an all-zero revision and does not set up a valid historical repository (`tools/evidence-disposition.py:2464-2479`); removing the prefix check reaches another rejection. Do not over-credit this as a demonstrated evidence-path false-clean detector.
- G4Env and G4Replace are fail-closed kills: fixtures that should remain clean under injected Git state become unavailable. This demonstrates sensitivity to removing those protections, not a successful attacker-controlled-blob admission.

## Survivors and non-equivalence witnesses

An added scratch-only rejection detector reuses the target’s fixture constructors and executes the real CLI, with a 30-second inner timeout and a 60-second outer bound. It expects CLI exit 2 and exactly `historical_input_unavailable`; detector exit 0 means that rejection was observed. Both witness commands are unchanged across pristine, mutated, and restored runs, and the same fixture manifests/repositories are reused:

```sh
timeout 60s python3 /tmp/tameshi-r17w2-MutateDispositionV2-bSsY3J/equivalence-probe.py --root /tmp/tameshi-r17w2-MutateDispositionV2-bSsY3J/G3Commit/fleet/tameshi-shokunin --fixture /tmp/tameshi-r17w2-MutateDispositionV2-bSsY3J/witness-G3Commit --kind tag
timeout 60s python3 /tmp/tameshi-r17w2-MutateDispositionV2-bSsY3J/equivalence-probe.py --root /tmp/tameshi-r17w2-MutateDispositionV2-bSsY3J/G5Mode/fleet/tameshi-shokunin --fixture /tmp/tameshi-r17w2-MutateDispositionV2-bSsY3J/witness-G5Mode --kind symlink
```

The scratch script is `/tmp/tameshi-r17w2-MutateDispositionV2-bSsY3J/equivalence-probe.py`, SHA-256 `3952cbeb3cca8f8c0c2aa04744ed8d60cad98cecde27f234316b95543e8cac51`.

| Selftest survivor | Witness input | Pristine / mutant / restored detector exits | Actual CLI exits | Actual finding IDs | Equivalent? |
|---|---|---|---|---|---|
| G3Commit | 40-hex annotated-tag object ID pointing to the pinned ancestor commit | 0/1/0 | 2/0/2 | `historical_input_unavailable` / `[]` / `historical_input_unavailable` | **No—observed CLI difference** |
| G5Mode | Historical mode `120000`, type `blob`; live path is a different, committed regular file | 0/1/0 | 2/0/2 | `historical_input_unavailable` / `[]` / `historical_input_unavailable` | **No—observed CLI difference** |

### G3Commit: exact commit-object identity is not redundant

Pristine rejects the tag object even though Git can peel it to an ancestor commit; removing the exact-resolution guard admits it. The surviving tree-ID selftest is insufficient because the retained `merge-base --is-ancestor` still rejects a tree. Tag peeling is different.

```text
pristine: detector_exit=0 tool_exit=2 status=could_not_evaluate ids=['historical_input_unavailable']
rev=6589079eb4ffeeaf460cc35536fb6ee93d4fda5f type=tag
finding: rev '6589079eb4ffeeaf460cc35536fb6ee93d4fda5f' does not resolve to that commit (got '52897eaad601f73d532f33a6ae1d4ea1e1d2f6b2')
mutated: detector_exit=1 tool_exit=0 status=clean ids=[]
restored: detector_exit=0 tool_exit=2 status=could_not_evaluate ids=['historical_input_unavailable']
```

### G5Mode: a symlink is a blob, but not an allowed regular blob

The fixture initially commits `tools/pinned-tool.py` as a symlink whose recorded link-text bytes equal the expected pin, then commits its replacement as a different regular file. Thus G1/G2/G3 still hold. Historical mode `120000` should be rejected, even though its Git object type is `blob`. Dropping only the mode restriction admits the manifest. The existing CRLF case (`tools/evidence-disposition.py:2608-2623`) exercises byte preservation, not this distinction.

```text
pristine: detector_exit=0 tool_exit=2 status=could_not_evaluate ids=['historical_input_unavailable']
tree_entry=120000 blob 083b9286b28436a825945dea68c00ef90ab17284	tools/pinned-tool.py
finding: tools/pinned-tool.py: tree entry mode 120000 type blob is not a regular blob
mutated: detector_exit=1 tool_exit=0 status=clean ids=[]
restored: detector_exit=0 tool_exit=2 status=could_not_evaluate ids=['historical_input_unavailable']
```

These observations establish missing selftest fixtures for annotated-tag object IDs and historical symlink modes; they do not falsify either corresponding guard in the pristine implementation.

## Before / mutant / restored hashes

Common pristine/restored SHA-256 **H0**: `f8f05c7aa601cf0b6f0907cc1ead2fc01acaad6a3c19e81888c084a969583e27`.

Every mutated-source hash was also unchanged after its detector; every restored-source hash was unchanged after the restored detector. Restoration used inverse anchored edits, not git reset/checkout. All nine restored runs returned `SELFTEST: PASS (56/56)`.

| Mutant | Before | Mutated SHA-256 | Restored |
|---|---|---|---|
| G1 | H0 | `e91e0421f2fad24ded8bab776ebd5094f285a84f8315ba39f672f1cd87aac2c8` | H0 |
| G2 | H0 | `769965aa29dc147383b20fd358dbbe5ae694da465e723f0d311e1ee5e26319af` | H0 |
| G3Commit | H0 | `272d89cac17469344ff72223e5e94269fd468360e626425c17cafb8c863c9d45` | H0 |
| G3Ancestor | H0 | `324f4eab90557815d91a8369395f9d427abce9ab79a7cba0e82aa70820c54c4d` | H0 |
| G4Env | H0 | `3ff2c493806cfa12a72db01bb57c8c168a357f2e88c77466c944d9be0659520f` | H0 |
| G4Replace | H0 | `b4bbc2908603af52341d7661cf0dd76462df80d05c214b1d515b890b14bd5210` | H0 |
| G5Mode | H0 | `6f01c1f9775c24cd4c15227978000f2ae0899d54540e2cb6af5e99d999a1b503` | H0 |
| G7Rows | H0 | `5a77ddb1aa2b144c78b83ce23d31e08bb6ed3f3993e79e287d6e533dbed94604` | H0 |
| ToolsPrefix | H0 | `ee6e58652fb7a75141649f5d44db837157ee2b6a1df22378dea8a404d2d66228` | H0 |

## Evidence and tooling

- Full commands, process exits, stdout/stderr, and before/after hashes for all 27 matrix selftests and six witness runs: `/tmp/tameshi-r17w2-MutateDispositionV2-bSsY3J/probe-results.json` (scratch evidence, not a committed artifact).
- Tools exercised: `python3 --version` → exit 0, `Python 3.14.8`; `git --version` → exit 0, `git version 2.56.0`; existing `sha256sum` and `timeout`.
- Auxiliary `timeout --version` returned exit 125: `the following required arguments were not provided: <COMMAND>...`. No timeout version is claimed; actual bounded detector commands completed normally.
- Tool installs/updates: none. No pacman transaction, host-service restart, or Git environment export.

Verdict: partial — `--selftest` kills 7/9 isolated v2-guard mutants; exact commit-identity and historical-blob-mode removals survive and are demonstrably non-equivalent, while all restored bytes and detectors match pristine behavior.
