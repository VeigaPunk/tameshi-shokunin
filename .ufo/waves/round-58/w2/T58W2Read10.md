# T58W2Read10 — verified-record

- Candidate: `8063d0a551fc5b3cb5a2d397da7353af53444534`; lane log confirmed C0 at dispatch.
- Section: `## Pin disposition and provenance correction — round 13`, lines 1559–1589.
- Frozen round-18 section SHA-256: `1fa3130bc6d4bc46124a1c0e234583657bb6c7623256dfa85f4db2a7fb91da31`.
- Findings by severity: none. Both documented recipes exited 0 from the C0 detached scratch clone.

## Sweep and evidence

Full commands, stdout, stderr and exits are in the adjacent JSON and `T58W2Read10-receipts/`.

1. Frozen importlib sectionizer: `1559 1589 1fa3130bc6d4bc46124a1c0e234583657bb6c7623256dfa85f4db2a7fb91da31`.
2. `python3 <clone>/tools/pin-disposition.py --manifest <clone>/.ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin`: exit 0, status `ok`, six verified pins, five `changed`, one `unchanged`, all `result_reuse=not_established`. Receipt retains full sibling branch-tip commits and `not_compared`.
3. `python3 <clone>/tools/witness-metadata.py --check --companion <clone>/.ufo/evidence/round-13/witness-metadata.json`: exit 0, `WITNESS_METADATA: metadata_consistent reason=ok exit=0`, inputs `summary,declaration,declared,rerun_summary`.
4. Scoped audit: exit 0; all six pointers exist, source rows S003/S041/S047/S048 resolve, both historical nulls remain, explicit declaration kind is `declared-witness mapping (not a blind preregistration)`. Canonical `evaluate_leg` lines 558–579 enforce verified-pin-before-content comparison and never establish reuse. Producer line 816 and regression assertion lines 1699–1701 support the provenance-fix statement.

## Residual risk and verification gaps

- Source list names superseded S047; S048 is already disclosed in the linked knowledge page. Improvement only, not a false statement in this section.
- Live fleet observations are dated, not reconstructed sibling states at C0. No reuse conclusion is drawn.
- LSP device unavailable (`No such tool: xd://lsp`); fallback source reading only. Producer regression assertion inspected, not executed. No sibling gates ran.
- No code changes or tool installations. Scratch `/fast/scratch/hyaku/tameshi-r58/T58W2Read10` deleted before delivery.

Self-check: accuracy 4 (live sibling state is not C0-pinned), completeness 4 (producer assertion inspected rather than executing its broader selftest), clarity 4 (full detail lives in receipts), actionability 5 (commands and outputs retained), conciseness 4 (necessary provenance detail); mean 4.2. No scope expansion warranted.
