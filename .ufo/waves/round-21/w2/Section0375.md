done

# Section 375 — Restore discipline

**Verdict: blocking.** The section is about historical round-2/round-3 sweeps, not the current state of the external kumitate or kagi repositories. The source notes date both runs to 2026-10-14. Their named line citations resolve; I found one blocking evidence gap and one incorrect reproducibility expectation.

## Findings

1. **Blocking — the “never written / every value identical” proof is stronger than the cited observations.** `SKILL.md:377-391` frames the negative claim as proof, says to rerun the same checks with every value identical, and then summarizes the outcomes. The before snapshots do record a repository revision: Kimi `corpus/knowledge/mutation-case-kimi-census.md:13-16`, Kagi `corpus/knowledge/mutation-case-kagi-census.md:13-17`. But the cited after proofs (`Kimi:34-35`, `Kagi:54-56`) record hash, size, mtime and path cleanliness (plus Kagi's scratch-copy `cmp`); neither records the after repository revision. Thus “every value identical” is unsupported for one of the explicitly required values. More fundamentally, before/after fingerprints show the observed final state, not by themselves that no transient write occurred and was undone. The notes separately report copy-only operation and no original write (Kimi:4-7; Kagi:44-47), which supports the historical authors' account, but the section should distinguish that report from what its endpoint checks prove.

2. **Wrong expectation — the notes do not directly rebuild the sweeps after `/tmp` is wiped.** `SKILL.md:396-400` says each reproduce spec rebuilds the sweep even if scratch is gone. Kimi §4 (`mutation-case-kimi-census.md:150-177`) and Kagi §7 (`mutation-case-kagi-census.md:210-249`) enumerate artifacts/edit specifications and commands, but those commands invoke `mutate_driver.py`; the notes name that driver as an existing scratch artifact and do not include its implementation or instructions to create it. `SCORECARD.md:16` explicitly describes the old driver as one-off, unversioned, and not in-tree. `SCORECARD.md:13` confirms sensitivity re-runs from retained scratch, not a scratch-free reconstruction. The note specs may help someone reimplement a driver; they are not a self-contained executable replay as claimed.

## Citation and temporal checks

- The explicit Kimi and Kagi line ranges in `SKILL.md:380-391` resolve and support the associated initial fingerprints, copy-only procedure, and reported post-run observations. I found no wrong numeric line range.
- The `G-R2-1` historical example is accurate: `corpus/README.md:11` summarizes the dirty intermediate claim-ledger pin, and `corpus/knowledge/gates-survey-kagi.md:554-560` records why it was re-pinned. The warning in `SKILL.md:401-403` is historical guidance, not a claim that the current repo is dirty.
- “SCORECARD round-2 verification row” is locatable as `SCORECARD.md:13` but is not an exact line citation. It supports sensitivity reruns from retained scratch, not reconstruction after scratch loss.
- I identified no obsolete Git command: `git status`, `cp -p`, `git checkout --`, and `git restore` remain meaningful for the uses described. The recipes' fixed `/tmp` locations and external sibling paths are historical context, not portable current commands. **No mutation recipe was re-executed.**

## Verification and limitations

The pinned repository's `HEAD` and `master` resolved to `790abd2129f153c13b471e381d454186edbde65e`; the merge-base ancestor check printed `ANCESTOR-OK`. `git show 790abd2129f153c13b471e381d454186edbde65e:SKILL.md` materialized the pinned blob, and `wc -l` reported 1,987 lines. `git status --short` showed 15 untracked wave/evidence paths; it did not show tracked modifications. Those commands completed through their success outputs; no source or evidence file was changed.

The LSP device was unavailable: reading `xd://lsp` returned “No such tool”; reading `xd://lsp/status` returned “Tool 'lsp' has no doc topics.” Consequently no LSP status, references, definition, or diagnostics were available. Direct source reads above are the evidence; text search was only used to locate citations, not as semantic proof. No build, tests, lint, formatter, install, or mutation command was run.
