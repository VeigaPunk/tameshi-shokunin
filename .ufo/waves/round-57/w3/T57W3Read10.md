# T57W3Read10 — verified-record

Heading: ## Pin disposition and provenance correction — round 13

Candidate: `adf87899c70d616140a81185a8f9acbbdfb30392`. Frozen round-18 sectionizer: lines 1559–1589, SHA-256 `1fa3130bc6d4bc46124a1c0e234583657bb6c7623256dfa85f4db2a7fb91da31`.

Axes: calibration (truth and provenance), operability (recipe execution), no-harm (read-only content).

## Findings by severity

None. Read the full assigned section and checked every named local pointer at the detached candidate. No staged text changes.

## Executed commands and evidence

Working directory for recipe commands: `/fast/scratch/hyaku/tameshi-r57/T57W3Read10/clone`. Absolute paths below execute the candidate tools and candidate manifest/companion, preserving the recipe's explicit live fleet root.

```sh
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read10/clone/tools/pin-disposition.py --manifest /fast/scratch/hyaku/tameshi-r57/T57W3Read10/clone/.ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin
python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read10/clone/tools/witness-metadata.py --check --companion /fast/scratch/hyaku/tameshi-r57/T57W3Read10/clone/.ufo/evidence/round-13/witness-metadata.json
```

Both exited 0. The pin probe reported `{'legs': 6, 'unchanged': 1, 'changed': 5, 'unavailable': 0}`, six verified pins and `result_reuse=not_established`; its complete stdout includes observed timestamp, sibling branch-tip commits and `not_compared`. Witness check printed `WITNESS_METADATA: metadata_consistent reason=ok exit=0` with summary/declaration/declared/rerun_summary inputs.

Additional executed commands (full argv, stdout, stderr and exits retained):

- `python3 -c <frozen sectionizer import/git-show snippet>`: `1559 1589 1fa3130bc6d4bc46124a1c0e234583657bb6c7623256dfa85f4db2a7fb91da31`. Exact snippet in `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read10-receipts/section-identity.json`.
- `python3 -c <scoped pointer/provenance sweep>`: exit 0, `SWEEP_OK: pointers, source rows, preserved nulls, exact kind/disclosure, producer regression assertion, content decision`. Exact snippet and output in `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read10-receipts/scoped-sweep.json`.

Full recipe receipts: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read10-receipts/pin-disposition.json` and `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read10-receipts/witness-metadata.json`.

The sweep resolves eight direct file pointers, reads S003/S041/S047/S048, verifies both frozen summary nulls and digests, matches exact companion kind/disclosure to the declaration, and prints producer and canonical content-decision code. Canonical logic: `tools/pin-disposition.py:558-578` rejects missing worktree hashes or unverified pins before byte equality; changed/unchanged never upgrades reuse. `tools/bash-witness-study.py:816` reads top-level kind; `:1694-1701` asserts its exact exposed string.

## Residual risk and verification gaps

- Stale-but-true historical source framing: section names round-13 S047; C0b also contains S048, which supersedes S047 with an object-neutral correction. The section itself makes no disputed test-versus-mutation paraphrase.
- The narrow second code anchor :563-567 covers pin verification failure; full byte-equality/changed decision is :558-578. Existing anchor is relevant, not a false statement.
- Live fleet observation is dated, not a C0b sibling snapshot: observed_at=2026-10-30T04:41:43Z; {"legs": 6, "unchanged": 1, "changed": 5, "unavailable": 0}. All six rows retain result_reuse=not_established; branch-tip commits are retained verbatim in pin-disposition receipt.
- LSP device unavailable (xd://lsp returned No such tool). Pointer and definition checks used direct pinned-file inspection and an executed Python sweep, not semantic-reference proof.
- No sibling gate, mutation re-sweep, producer selftest, or external-source freshness check executed. Producer regression assertion was inspected at lines 1694-1701; historical evidence remains historical.
- No tools installed or updated. No lane content or frozen evidence modified; only assigned report/receipts written.

## Self-evaluation

Accuracy 4/5: commands and outputs retained; external source freshness not reassessed. Completeness 5/5: full assigned section, both recipe commands, all local pointers and provenance claims checked. Clarity 4/5: long exact Python argv lives in receipts rather than inline. Actionability 5/5: machine-readable record and raw receipts accompany this report. Conciseness 4/5: metadata repeated for independent binding. Overall 4.4/5. Improvement: use the receipt command argv for exact reproduction; no extra claims depend on unrun checks. User-assessment self-check: evidence is explicitly bounded to this section and candidate.
