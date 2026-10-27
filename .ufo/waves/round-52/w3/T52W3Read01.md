# Cold read — CAND1 round-17 live-tree re-pin section

## Findings

None. No failing statement found at CAND1.

## Holds

- `corpus/lessons/round-16-verifier-spotcheck.md` §§3 and 6: the cited routed defects and provenance align with the section's historical account.
- `tools/evidence-disposition.py`: v2 manifests, historical-input checks, the listed failure conditions, and environment/repository guards are present; section labels these as round-18/27 history where applicable.
- `tools/registry-check.py`: documented invocation, `--rev`/`--registry` semantics, clone/sibling layout, and row outcomes match its interface and usage text.
- `tools/mutate-and-run.sh`: fixture git operations use `git_clean`, which scrubs inherited `GIT_*` variables; section explicitly exempts the historical round-16 measure tool from the broad statement.
- `tools/pin-disposition.py`: reported branch-tip/head fields and `GIT_*` scrubbing match its documented output and implementation.

5 pointers checked; all hold. Checked CAND1 bytes using `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 7ff81a5b0ab0fbaefd68cf4ef9dcfe687a6d7135:<path>`. No LSP device/status route was available, so pointer checking used literal source inspection, not semantic reference analysis.

## Summary

- Findings: none.
- Holds checked: 5.
- Section SHA-256: `782f9494205bd686bb2b404ec49ebb79b5cba6e5914edff2f0d69b8438274f97`.
