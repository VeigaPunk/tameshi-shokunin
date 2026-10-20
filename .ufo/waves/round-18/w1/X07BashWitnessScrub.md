# X07 — Bash witness GIT environment scrub

## Files changed

- `.ufo/waves/round-18/staged/tools/bash-witness-study.py` — staged copy of the base-revision tool, updated to remove inherited `GIT_*` variables and then pin child Git configuration. SHA-256: `8dfaa25aa2713635e7363f60effb442a474ba3656d6cf2bb171c0c22432e3a12`.
- `.ufo/evidence/round-18/dispositions.json` — v2 migration manifest carrying the original rows and input pins, the round-14 v1 `supersedes` document, and `tools/bash-witness-study.py` as a third historical input at `4acc607dfd79f19d508bd50cdd06b77269fccd1d`. SHA-256: `9caa2f76dcc36265bb11b58baa397b1015a91b086db63d203ab16020a1fc2676`.
- `.ufo/evidence/round-18/dispositions-before.json` — round-17-before v2 copy with the added third historical input and round-14-before `supersedes` pin. SHA-256: `dc948a5ee1bab7a89e21ef4d75b620a430559ae0b2b64573f7c2bcacbc4deb65`.
- `.ufo/waves/round-18/w1/X07BashWitnessScrub.md` — this report.

## Behavior and manifest

`git_clean_env()` filters every inherited `GIT_*` name, then sets `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1`; both production subprocess launch paths use this environment. `sweep_env()` also removes the existing sweep-specific variables. The canary selftest makes two private fixture repositories, exports `GIT_DIR` and `GIT_WORK_TREE` pointing at the canary, and exercises materialization and the sweep runner against the ordinary fixture. Fixture Git writes pass `-c core.hooksPath=/dev/null`. Selftest storage is created beneath an explicit mode-700 private root under `/tmp`; it checks canonical realpaths before fixture creation and before cleanup.

Per the L1 ruling, `supersedes` remains `.ufo/evidence/round-14/dispositions.json`, pinned by the copied round-17 input digest. G7 remains unchanged. The round-17-to-round-18 migration is represented by the proposed registry transition below and the new historical-input reason at `.ufo/evidence/round-18/dispositions.json:20-23`.

## Retained evidence

- Lane revision observed at dispatch: `183f87b899e6cae46be98d251cbc87fb5118f6ca`; initial read-only status showed pre-existing untracked `.ufo/evidence/round-18/` and `.ufo/waves/round-18/` trees. Only assigned implementation files and this report were written by this seat.
- The source snapshot at the dispatch revision had SHA-256 `49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80`.
- `sha256sum <staged source> <round-18 manifests>` — exit 0; digests are recorded above.
- `git show 4acc607dfd79f19d508bd50cdd06b77269fccd1d:tools/bash-witness-study.py | sha256sum` — exit 0; returned `49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80`, matching the old pin in `.ufo/evidence/round-13/expected.json:11`.
- Static inspection confirmed both production `subprocess.run` sites use the scrubbed environments. All selftest fixture Git subprocesses also use the helper; fixture repository writes disable hooks, and canary setup uses the same child-environment policy.
- Both round-18 manifests retain the corresponding round-14 v1 `supersedes` pin and original four input pins; each carries the same third historical input. Their rows are copied from the matching round-17 manifests.
- Acceptance used the fleet-mirror clone at `/tmp/tameshi-r18w1-X07BashWitnessScrub-mrToHx/fleet/tameshi-shokunin`; commands ran from that clone with `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR`. The staged source was committed only in this clone (`74cd574`) because the historical-input guard rejects dirty instrument bytes.
- `python3 tools/bash-witness-study.py selftest` — exit 0; `WITNESS_SELFTEST: 43/43 pass`, `VERDICT: PASS`.
- Scrub-removed mutant (clone only: changed the `git_clean_env()` filter predicate to `if True`), same selftest command — exit 1; both canary checks failed, `WITNESS_SELFTEST: 41/43 pass`, `VERDICT: FAIL`.
- `python3 tools/evidence-disposition.py --root /tmp/tameshi-r18w1-X07BashWitnessScrub-mrToHx/fleet/tameshi-shokunin --dispositions /tmp/tameshi-r18w1-X07BashWitnessScrub-mrToHx/fleet/tameshi-shokunin/.ufo/evidence/round-17/dispositions.json --json` — exit 2; `expected_input_digest_mismatch` names `tools/bash-witness-study.py`, observed `8dfaa25aa2713635e7363f60effb442a474ba3656d6cf2bb171c0c22432e3a12`, expected `49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80`.
- `python3 tools/evidence-disposition.py --root /tmp/tameshi-r18w1-X07BashWitnessScrub-mrToHx/fleet/tameshi-shokunin --dispositions /tmp/tameshi-r18w1-X07BashWitnessScrub-mrToHx/fleet/tameshi-shokunin/.ufo/evidence/round-18/dispositions.json --json` — exit 0; `status: clean`, 11 effective and 1 superseded; all three historical inputs verified.
- `python3 tools/evidence-disposition.py --root /tmp/tameshi-r18w1-X07BashWitnessScrub-mrToHx/fleet/tameshi-shokunin --dispositions /tmp/tameshi-r18w1-X07BashWitnessScrub-mrToHx/fleet/tameshi-shokunin/.ufo/evidence/round-18/dispositions-before.json --json` — exit 1; `status: failed`, `expectation: producer_before`, finding `expected_contains_missing`; 12 effective, one failed.
- `python3 tools/evidence-disposition.py --root /tmp/tameshi-r18w1-X07BashWitnessScrub-mrToHx/fleet/tameshi-shokunin --dispositions /tmp/tameshi-r18w1-X07BashWitnessScrub-mrToHx/fleet/tameshi-shokunin/.ufo/evidence/round-17/dispositions-before.json --json` — exit 2; `expected_input_digest_mismatch` names `tools/bash-witness-study.py`, observed `8dfaa25aa2713635e7363f60effb442a474ba3656d6cf2bb171c0c22432e3a12`, expected `49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80`.
- Initial round-18 main-manifest attempt on the uncommitted staged copy exited 2 with `historical_input_uncommitted`; after the scratch-clone commit, both round-18 gates passed their expected outcomes above.

## Proposed registry rows

```json
[
  {
    "name": "evidence-disposition-round18",
    "kind": "gate",
    "argv": [
      "python3",
      "tools/evidence-disposition.py",
      "--root",
      ".",
      "--dispositions",
      ".ufo/evidence/round-18/dispositions.json",
      "--json"
    ],
    "expect": {
      "exit": 0,
      "stdout_contains": [
        "\"status\": \"clean\"",
        "\"effective\": 11",
        "\"superseded\": 1"
      ]
    },
    "timeout_s": 60,
    "source": "SKILL.md@98bea7d:1681",
    "status": "active",
    "tags": ["new-r18"]
  },
  {
    "name": "evidence-disposition-round18-before",
    "kind": "gate",
    "argv": [
      "python3",
      "tools/evidence-disposition.py",
      "--root",
      ".",
      "--dispositions",
      ".ufo/evidence/round-18/dispositions-before.json",
      "--json"
    ],
    "expect": {
      "exit": 1,
      "stdout_contains": [
        "\"expectation\": \"producer_before\"",
        "\"status\": \"failed\""
      ]
    },
    "timeout_s": 60,
    "source": "SKILL.md@98bea7d:1806",
    "status": "active",
    "tags": ["new-r18"]
  },
  {
    "name": "evidence-disposition-round17",
    "kind": "gate",
    "argv": [
      "python3",
      "tools/evidence-disposition.py",
      "--root",
      ".",
      "--dispositions",
      ".ufo/evidence/round-17/dispositions.json",
      "--json"
    ],
    "expect": {
      "exit": 0,
      "stdout_contains": [
        "\"status\": \"clean\"",
        "\"effective\": 11",
        "\"superseded\": 1"
      ]
    },
    "timeout_s": 60,
    "source": "SKILL.md@98bea7d:1681",
    "status": "superseded",
    "superseded_by": "evidence-disposition-round18",
    "tags": ["baseline"]
  },
  {
    "name": "evidence-disposition-round17-before",
    "kind": "gate",
    "argv": [
      "python3",
      "tools/evidence-disposition.py",
      "--root",
      ".",
      "--dispositions",
      ".ufo/evidence/round-17/dispositions-before.json",
      "--json"
    ],
    "expect": {
      "exit": 1,
      "stdout_contains": [
        "\"expectation\": \"producer_before\"",
        "\"status\": \"failed\""
      ]
    },
    "timeout_s": 60,
    "source": "SKILL.md@98bea7d:1806",
    "status": "superseded",
    "superseded_by": "evidence-disposition-round18-before",
    "tags": ["new-r17"]
  }
]
```

Existing row retargeting: `evidence-disposition-round14-superseded` keeps all other fields and changes `superseded_by` from `evidence-disposition-round17` to `evidence-disposition-round18`.

## Risks / blockers

No implementation blocker remains. The uncommitted-copy historical-input refusal was resolved by committing only the staged source in the temporary acceptance clone; no lane Git state was written. No tools were installed or updated. No build, lint, or formatter was run.

**Verdict: built — both round-18 manifests and both canary polarities matched their required outcomes.**
