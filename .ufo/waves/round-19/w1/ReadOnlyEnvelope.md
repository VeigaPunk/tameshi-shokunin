# ReadOnlyEnvelope — bounded audit safety review

**Review date:** 2026-10-21  
**Scope:** static read-only review of `.ufo/evidence/round-19/measure.py`; no gate, selftest, build, or shell command was run, and no private config was opened. No install or production edit.

## Findings

- **Retained argv execution — no defect observed (source-level).** `receipt()` parses retained JSON, requires exact equality with the expected literal argv and fixed receipt paths, and returns only bytes already in the revision-data map (`measure.py:61–76, 112–136`). No parsed receipt argv is passed to a process. The only non-Git child path in selftest invokes this same Python file with a synthetic snapshot (`measure.py:159–167, 196–206`). The retained witness/measurement commands are compared as data, not run.
- **Git writes — no mutating Git command observed.** The revision path uses only `git cat-file -e <rev>^{commit}` and `git show <rev>:<fixed-path>` (`measure.py:235–243`); argv is an array, not a shell string. No Git write operation is present in these calls. This is a source inspection, not an execution guarantee about an externally substituted `git` executable.
- **Inherited `GIT_*` — scrubbed, with deliberate fixed overrides.** `clean_env()` drops every inherited key beginning `GIT_`, then sets only fixed `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1` (`measure.py:54–58`); all subprocess calls pass that environment. Quote (opened 2026-10-21): `"if not k.startswith('GIT_')"` (`measure.py:55`).
- **Low, conditional path-boundary risk — `--repo` is not constrained.** CLI accepts caller-supplied `--repo` (`measure.py:216–220, 235, 241`) and feeds it to `git -C`. A misrouted or untrusted invocation can therefore make the audit read Git objects from a repository outside the authorized tameshi root. No such path was used or inspected here, and this is not evidence of a Git write or retained-argv execution.
  - **Impact:** results can be produced from the wrong repository; Git may also consult that repository's local configuration. This weakens the stated lane-only evidence boundary and can make an audit outcome misleading.
  - **Smallest remediation:** remove the override for the production audit path, or resolve and require `--repo` to equal the canonical tameshi root before invoking Git. Keep any fixture mode explicitly separate.

## Outcome / verification boundary

Observed source behavior meets the three requested safety checks for receipt argv, Git command intent, and inherited `GIT_*` scrubbing. The path-boundary finding remains conditional and unresolved until the audit constrains `--repo`. No runtime claim is made; no old gate was run.