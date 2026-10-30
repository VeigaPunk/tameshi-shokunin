# executor-source-pin boundary — connector fragment (T59W1S53)

`tools/executor-source-pin.py` is a bounded source-identity prerequisite, not an
execution attestation. Given a verifier-supplied trusted commit and a candidate
commit, it compares the raw Git blobs of declared regular executable-source paths
and exits 0 only when all declared blobs are byte-equal, 1
(`EXECUTOR_SOURCE_DRIFT`) when a declared source differs, is missing, or is
nonregular at the candidate, and 2 (`EXECUTOR_SOURCE_UNAVAILABLE`) on bad
arguments, an invalid trusted commit/source, or an unresolvable candidate.

It exists because round 58's C2 falsification showed a claimant-swapped executor
(`tools/registry-check.py`) fabricating held/mutant tallies while the frozen
counter still printed PASS: nothing bound the executed bytes to a trusted
revision. Applied pre-execution, this gate rejects that forgery class at the
declared-path level (empirical link: the retained round-58 bent runner,
sha256 `3c058a32f93023bc`, differs in every byte-class from the trusted regular
blob `tools/registry-check.py`, sha256 `7984540cd3cbfcff`, at both the round-58
and round-59 bases).

It certifies nothing about execution, dependency or interpreter identity,
completeness of the declared closure (undeclared bent helpers pass), or the
trustworthiness of the verifier-supplied trusted revision itself; a cheat baked
into the trusted bytes would be certified, not caught. Exit 0 authorizes the
declared sources to be treated as the trusted sources for subsequent
measurement; the honesty of that subsequent measurement remains the verifier's
separate responsibility.

Staged fragment for connector use; not a knowledge entry (T59W1S54 owns
`corpus/knowledge/executor-source-binding.md`), not registry, not production.
