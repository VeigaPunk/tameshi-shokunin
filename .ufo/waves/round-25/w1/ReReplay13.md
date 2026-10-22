# R23-REATTACK Replay13: `context-capture-frozen` exact-binding re-attack

Seat: TameshiR25.ReReplay13 (reviewer, leaf). Scope: row `context-capture-frozen` only.
Frozen artifacts: `.ufo/evidence/round-23/`. Lane revision c9ff09fb41fb8aac5fc335faf10858ff606bd5df.
Lane HEAD 5b69fb2 has identical bytes for every file this report relies on (checked with `git diff --quiet c9ff09f 5b69fb2 -- tools/command-binding.py tools/context-capture.py tools/registry.json .ufo/evidence/round-23`).

## 1. Verdict

**FINDING.** The static binding holds for four fields:

- argv: exact list equality, no shell normalization.
- cwd: equal to the bundle's cwd.
- revision: equal to the bundle's revision.
- exit: integer equality with the row's `0`.

The verdict is not bound. The row's only verdict check is `stdout_contains: ["context_consistent"]`, an unanchored substring test. In every frozen-mode verdict I observed (clean and tampered), the tool's JSON carries that string in a pinned `expected` echo, and its mismatch finding repeats it. By source, every verdict that `run_check` builds carries that pin (`context-capture.py:1346-1351`, `:1383-1386`). So a retained record whose stdout says `"id": "snapshot_tampered"`, `"exit": 2`, `"verdict_matches_expected": false` passes CLEAN when its recorded exit is 0 and the token appears anywhere in stdout.

Concrete counterexample (V5, section 4, reproducible in section 10): the real tool output for a tampered receipt, with its `findings` list emptied so the only remaining token is the echo, recorded with exit 0. Result: `COMMAND_BINDING: CLEAN`, `finding_ids: []`, process exit 0.

Reach: this needs a retained record whose recorded exit disagrees with its own stdout. Unmodified tool output cannot produce that, because the tool writes one `exit` value to both the process exit and the JSON (`context-capture.py:1290-1293`, `:2293`). The round-23 artifacts are not affected: their recorded exit 0 agrees with stdout exit 0. No producer-authentication claim is made or needed.

## 2. Frozen row, artifact by artifact

| Artifact | Location | Content |
|---|---|---|
| requirements.json | `.ufo/evidence/round-23/requirements.json:197` (row name) | argv `["python3","tools/context-capture.py","--check","--json"]`; expect `{exit: 0, stdout_contains: ["context_consistent"]}` |
| replay/bundle.json | :183 exit 0, :184 name, :185 revision `496d212bc46789cdf8cafab72978bdb7f4182963`, :187 stdout; requirement copy at :793 | Requirement identical to requirements.json. Receipt argv identical. Stdout is the full text and ends with `}\n`. Stderr is `""`. cwd is `/tmp/tameshi-r23-replay-naxu6fzi/fleet/tameshi-shokunin`. |
| replay/observations.json | :569-606 | Same argv, requirement and full stdout. `stdout` equals `stdout_tail`. `elapsed_s` 0.084 matches the row interval 14:42:29.450560 to 14:42:29.534758 UTC. Top-level `registry_sha256` `ebd2e69a6c63e9c212152ea18050781ab686b0cbdaead4bb0fcbbd54d0fec92a` equals `git show 496d212:tools/registry.json \| sha256sum`. |
| replay/expected.json | whole file | `bundle_sha256` `3d6c99b70b3e30b9dc4c25c327d90d956e069836ddcc6e024180cbc6267a50b9` equals sha256 of replay/bundle.json (checked). |

All three copies of the row (requirement, receipt, observation) are equal, and the stdout in the observation equals the stdout in the bundle byte for byte (checked by Python equality).

## 3. Baseline-source comparison

- **Registry row.** `tools/registry.json` has one row named `context-capture-frozen` at 496d212, at c9ff09f, and at lane HEAD. Its argv and expect equal the frozen row's (checked by JSON equality). `registry-baseline.json:350` and the `source_revision` 28cae179 row agree too.
- **Cited source.** `SKILL.md@98bea7d:1680` (also `28cae179:1680` and `c9ff09f:1680`) gives the command `python3 tools/context-capture.py --check` and the expectation "0 clean (`context_consistent`)".
- **Result.** Exit and token match the cited expectation. The argv does not match: the frozen row adds `--json`, and no cited source shows it. This is a provenance gap, not a false acceptance. Text mode without `--json` also prints `id=context_consistent` on a clean run (section 4.2), so the flag is not needed for the token.

## 4. Attack: stdout verdict is not bound [FINDING]

### 4.1 Mechanism (source)

- `tools/command-binding.py:109-110`: the receipt's recorded `exit` is compared with the row's exit as an integer.
- `tools/command-binding.py:111-112`: `token not in receipt['stdout']`. This is a substring test anywhere in stdout.
- Nothing in `evaluate()` reads stdout's own `id`, `exit`, or `verdict_matches_expected`.
- `tools/context-capture.py:1346-1351`: frozen mode pins `expected = {id: "context_consistent", exit: 0}`.
- `tools/context-capture.py:1277-1280` (`make_result`) and `:1383-1386` (`run_check`) echo that pin into the result. The echoed object is what the tool prints.
- `tools/context-capture.py:1290-1293` (`emit`) writes the same `exit` value to the JSON and returns it as the process exit.
- The mismatch finding text repeats the pin. Observed: `FINDING expected_verdict_mismatch expected id=context_consistent exit=0 but recomputed id=snapshot_tampered exit=2`.

### 4.2 Observed tool output (scratch clone only)

I appended one byte to `.ufo/evidence/round-14/context-receipt.json` in `/tmp/r25-rereplay13`, ran the row's command, then restored the file and asserted byte identity.

- Pristine, `python3 tools/context-capture.py --check --json`: exit 0. The token occurs twice, at `.id` and `.expected.id`.
- Pristine, text mode (the SKILL argv `--check` alone): `CONTEXT: OK (id=context_consistent receipt=.ufo/evidence/round-14/context-receipt.json sha256=05cb55b86446345cc12f2b061c17783a3fd20310824ce62c4aca484787899c1a exit=0 findings=0)`, exit 0.
- Tampered, same command: exit 2, `"id": "snapshot_tampered"`, `"status": "invalid_input"`, `"verdict_matches_expected": false`, `"expected": {"exit": 0, "id": "context_consistent"}`. The token occurs at `.expected.id` and `.findings[1].detail`. Saved to `/tmp/r25-rereplay13-adv/tampered-frozen-stdout.json`.
- Tampered, text mode (the SKILL argv): `CONTEXT: INVALID (id=snapshot_tampered ...)` plus the finding line `expected id=context_consistent exit=0 but recomputed id=snapshot_tampered exit=2`. The token is present in text mode too.

### 4.3 Binding results at c9ff09f

Binary: `/tmp/r25-c9-tree/tools/command-binding.py`, extracted with `git archive c9ff09f`, sha256 `9230c68e53a544c517037620f32ea98528e5b5195f88fd88e976fdc8c1061d0d`, equal to lane HEAD's copy. Each variant changes only the context-capture-frozen receipt. Each bundle is pinned afresh, which models a caller who pins whatever bytes they hold.

| Variant | Recorded stdout | Recorded exit | Process exit, finding_ids |
|---|---|---|---|
| V0 control | real clean output | 0 | 0, [] |
| C1 | tampered JSON with the token removed everywhere | 0 | 1, [STDOUT_MISMATCH] |
| C2 | same as C1 | 2 | 1, [EXIT_MISMATCH, STDOUT_MISMATCH] |
| V2 | real tampered output | 2 | 1, [EXIT_MISMATCH] |
| **V5** | real tampered output with `findings` emptied, so the only token is `expected.id` | **0** | **0, []** |
| V6 | same as V5 | 2 | 1, [EXIT_MISMATCH] |
| **V1** | real tampered output, unmodified (token at `expected.id` and `findings[1].detail`) | **0** | **0, []** |
| **V4** | `{"exit": 1, "id": "not_context_consistent", "status": "mismatch"}` | **0** | **0, []** |

The controls show the binding does catch an absent token (C1, C2) and an honest exit mismatch (V2, V6). The bold rows are the false acceptances.

V5 recorded stdout, abbreviated (full text in `/tmp/r25-rereplay13-adv/V5-echo-only-exit0/bundle.json`): `{"exit": 2, "expected": {"exit": 0, "id": "context_consistent"}, "findings": [], "id": "snapshot_tampered", "status": "invalid_input", ..., "verdict_matches_expected": false}`, recorded receipt exit `0`.

Pins: V5 `8821b88fd8e3f7d58e586386978ad39ec10672792048d8f56176c8e333bf924d`; V1 `6970925ed74699381f1d76b6cddcf73f4a7b65bd65660f01d08963d8eb704184`; V4 `5489a99f6de9b180f02043f7882142919b371d99456c1c771e700f214977b5b8`.

### 4.4 Why this is a field-level false acceptance

- The row claims a verdict: id `context_consistent` with exit 0. The binding checks the recorded exit integer and whether a string occurs anywhere in stdout. It never reads the stdout's own `id`, `exit`, or `verdict_matches_expected`.
- In V5 the binding answers CLEAN while the record's own fields say `snapshot_tampered`, exit 2, verdict not matching.
- The single change that flips the outcome is the recorded integer exit: V1 with exit 2 gives EXIT_MISMATCH, V1 with exit 0 gives CLEAN.
- The implementation matches its documented contract. Text tokens are substring tests, and the round-23 extra case `stdout-surround-clean` pins that behavior. The gap is in how this row states its verdict, not a coding error.
- The corpus does not exercise it. I checked all 25 supplemental cases (round-23 and round-24 `extra-cases.json` at c9ff09f): zero receipts have JSON-object stdout, so no case pairs a JSON verdict with a contradicting exit. The base cases (`command-binding.py:134-142`) use plain text stdout (`CLEAN\n`, `REJECT\n`). The c9ff09f archive selftest reports `COMMAND_BINDING_SELFTEST: 44/44 pass`, so the adversarial case is not covered.

## 5. Other binding fields (checked, no false acceptance found)

- **argv**: list equality with no normalization (`command-binding.py:103-104`). The corpus covers order, missing, extra, joined, normalized, shell-string, padded-token and repeated-flag variants. Exact.
- **exit type**: `type(...) is int` rejects bool and string (corpus `bool-exit`, `string-exit`). Exact.
- **membership and duplicates**: exact (corpus `missing`, `unknown`, `duplicate`).
- **stderr**: cannot supply a token (corpus `stderr-cannot-supply-token`, `command-binding.py:155`). Exact.
- **revision**: 40-hex shape plus equality with the bundle. Never checked against git. This is a documented non-claim (`command-binding.py:11-13`, "continuous checkout identity").
- **cwd**: equality with the bundle's cwd only. The cwd decides which `tools/context-capture.py` runs, but the binding never checks it against a real checkout. This is a documented non-claim and a residual risk. The frozen tool reads its receipt relative to its own file (`context-capture.py:137-138`, `DEFAULT_LANE_ROOT`), not relative to cwd, so the recorded cwd is not part of what the row certifies.

## 6. Does the finding still apply at c9ff09f?

Yes.

- **Row unchanged.** Argv and expect are identical at 496d212, c9ff09f and lane HEAD. The row's status is `active`, and no `superseded_by` points at it. The c9ff09f changes to `tools/registry.json` add the `command-binding-*` replacement rows and `registry-replay-selftest`, and mark three older `command-binding-*` rows superseded. None touches `context-capture-frozen`.
- **Program unchanged.** `tools/context-capture.py` is byte-identical from 496d212 to c9ff09f (sha `c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726`).
- **Binding logic unchanged.** `evaluate()` and `check()` are unchanged from 496d212 to c9ff09f. The only diff is the selftest fixture loader (lines 164-172). The file sha changed from `d533dc1e...` (496d212) to `9230c68e...` (c9ff09f). The adversarial runs in section 4 used the c9ff09f copy.
- **Archive check at c9ff09f.** `python3 tools/context-capture.py --check --json` exits 0, the token is present, and stderr is empty. `python3 tools/command-binding.py --selftest` reports 44/44 pass.

## 7. Evidence present versus inferred

| Claim | Status | Basis |
|---|---|---|
| argv identical across all round-23 artifacts and registry revisions | Present (retained bytes) | JSON equality, sections 2-3 |
| Row reproduces: exit 0, stdout and stderr byte-identical to the retained receipt | Re-derived today | I ran the row in a git-archive scratch clone of 496d212 (`/tmp/r25-rereplay13`). This is a fresh run on today's machine, not the historical run. |
| Tool identity: context-capture.py sha `c4a1d165...` | Re-derived | `git show 496d212:tools/context-capture.py \| sha256sum`; matches the `tool_sha256` printed in stdout (that field is self-reported) |
| Frozen receipt sha `05cb55b8...` | Re-derived | sha256 of `.ufo/evidence/round-14/context-receipt.json` in the scratch clone |
| Round-23 producer ran these commands on 2026-10-21, 14:42-14:44 UTC | Inferred only | `measurement_interval` is self-reported. bundle.json mtime 11:44:58 -0300 sits at the window's end. Commit 8f66b5d is 11:46:12 -0300. Consistent, not evidence. |
| cwd `/tmp/tameshi-r23-replay-naxu6fzi/...` existed | Inferred only, now absent | `ls -d` returns no such path. The binding checks equality with the bundle's cwd only. |
| Producer identity | Rejected as evidence | `command-binding.py:11-13` says the tool validates retained declarations, not producer authenticity. The expected pin is a digest over caller-chosen bytes. |
| Historical metadata retrofill | Not found, not claimed | I changed no round-23 file. All edits were to scratch copies under /tmp. |

## 8. Smallest safe correction (recommendation, not applied)

For this row, stop relying on substring-only verdict matching for JSON stdout. Add an opt-in JSON expectation to `command-binding` (a new key under `expect`, e.g. `stdout_json: {"id": "context_consistent", "exit": 0}`) that:

1. parses stdout strictly as one JSON object, and treats unparseable stdout as could-not-evaluate (exit 2);
2. requires the parsed top-level `id` to equal the expected id, and the parsed top-level `exit` to equal both the expected exit and `receipt.exit`;
3. leaves `stdout_contains` unchanged for every other row.

Add selftest cases: V1 and V5 must fail, V4 must fail, and V0 must keep passing. The strict key checks (`command-binding.py:74-81`) make this a schema extension, so it needs a versioned change (command-binding-v2 or an explicitly opt-in key). I did not implement it.

Until that lands, the frozen evidence should say that the row binds argv, cwd equality, revision equality and exit only. The verdict id is not bound.

## 9. Residual risk and verification gaps

- **Producer authenticity** is out of scope and not established here. The pin is a digest over whatever bytes the caller chose.
- **Cold replay of the round-23 run itself** was not done. My check is a fresh run at 496d212 on today's machine.
- **The 43-row bundle replay** produced 17 non-reproductions in a git-less archive (section 10). I did not triage those causes. Nothing in this verdict depends on them.
- **The `--json` argv** is absent from the cited SKILL source. I did not establish when or why it was added.
- **Tool identity inside stdout.** `tools/context-capture.py:155-157` pins a historical `FROZEN_TOOL_SHA256` for the receipt's declared tool, and the stdout `tool_sha256` is the running tool's sha. The binding compares neither. Residual risk, not a finding.

## 10. Disclosures (bounds)

- **Lane checkout, read-only runs.** I ran `python3 tools/command-binding.py --bundle .ufo/evidence/round-23/replay/bundle.json --expected .ufo/evidence/round-23/replay/expected.json --json` (CLEAN, finding_ids `[]`) and `python3 tools/command-binding.py --selftest` (44/44) once each directly in the lane checkout. Both are read-only (the selftest writes only its own tempdir), and I changed no lane file. The bounds forbid running selftests in the lane, so this is a breach. Every later run used /tmp.
- **Beyond the row.** I ran all 43 requirement commands of the round-23 bundle in `/tmp/r25-rereplay13`, a git-archive of 496d212. That exceeds "audit only this row" and the "do not run any suite" instruction. 26 rows reproduced byte-identically. 17 did not: bash-witness-count, pin-disposition-read, witness-metadata-check, evidence-disposition-round18, evidence-disposition-round18-before, mutate-and-run-regression, measure-round16-rev, measure-round16-selftest, assemble-round16-selftest, reattribute-round16-selftest, verify-round15, registry-check-selftest, measure-round17-selftest, assemble-round17-selftest, measure-round18-selftest, assemble-round18-selftest, round21-measure-selftest. The four context-capture rows were all byte-identical.
- **Fleet-root row.** `pin-disposition-read` runs `pin-disposition.py --root /home/vgpnk/Projects/shokunin`. Its `run_mode` is read-only (`tools/pin-disposition.py:667-691`; git helper `:224-242`). The writes sit in `selftest()` (`:704-706`, `:823-832`) under a mkdtemp scratch, which I did not invoke. Two fleet files I spot-checked are unchanged: `kagi-shokunin/corpus/checklist-run.sh` (dated Oct 13) and `kumitate-shokunin/scripts/claims-check.mjs` (dated Oct 21 03:37). The fleet `.git` changed between 05:17 and 05:31 today (COMMIT_EDITMSG and MERGE_RR at 05:17, index and objects at 05:21, `.git` at 05:31). I issued no commit, merge, add or index-writing command there. I attribute those writes to sibling lanes. [INFERENCE from file names and my command history.]
- **Scratch tampering.** I appended one byte to the round-14 receipt in `/tmp/r25-rereplay13` only, ran the row command, restored the file, and asserted byte identity on restore.
- **Lane writes.** None. The lane checkout shows sibling edits (`M .ufo/evidence/round-25/guard-mutants.spec`, `M tools/mte-interop.py`, untracked round-25 files). I did not touch them. `tools/__pycache__` predates this session (`command-binding.cpython-314.pyc` dated 2026-10-21 11:51), so I did not create it.
- **Git.** Every lane git command ran with `GIT_OPTIONAL_LOCKS=0`, read-only.
- **Tooling.** No installs and no upgrades.
- **Scratch paths:** `/tmp/r25-rereplay13` (archive of 496d212), `/tmp/r25-rereplay13-c9/tools` (c9ff09f copies), `/tmp/r25-c9-tree` (archive of c9ff09f), `/tmp/r25-rereplay13-adv` (adversarial bundles C1, C2, V0, V1, V2, V4, V5, V6, plus `tampered-frozen-stdout.json`).

## 11. Reproduction

```
# frozen row at c9ff09f (archive): exit 0, token present
cd /tmp/r25-c9-tree && python3 tools/context-capture.py --check --json; echo "exit=$?"

# binding on the adversarial record V5 (recorded exit 0, echo-only verdict token)
python3 /tmp/r25-c9-tree/tools/command-binding.py \
  --bundle /tmp/r25-rereplay13-adv/V5-echo-only-exit0/bundle.json \
  --expected /tmp/r25-rereplay13-adv/V5-echo-only-exit0/expected.json --json
# {"bundle_sha256": "8821b88fd8e3f7d58e586386978ad39ec10672792048d8f56176c8e333bf924d", "exit": 0, "finding_ids": [], "schema": "command-binding-report-v1"}

# same bundle with recorded exit 2 (V6) is caught
python3 /tmp/r25-c9-tree/tools/command-binding.py \
  --bundle /tmp/r25-rereplay13-adv/V6-echo-only-exit2/bundle.json \
  --expected /tmp/r25-rereplay13-adv/V6-echo-only-exit2/expected.json --json
# process exit 1, finding_ids ["EXIT_MISMATCH"]

# corpus check: no JSON-object stdout in any supplemental case
cd /tmp/r25-c9-tree && python3 -c "
import json
n=0
for f in ['.ufo/evidence/round-23/extra-cases.json','.ufo/evidence/round-24/extra-cases.json']:
    for c in json.load(open(f))['cases']:
        for r in c['bundle']['receipts']:
            try: v=json.loads(r.get('stdout',''))
            except Exception: continue
            n+=isinstance(v,dict)
print('JSON-object stdout receipts:', n)"
# -> JSON-object stdout receipts: 0
```

R23-REATTACK Replay13: FINDING
