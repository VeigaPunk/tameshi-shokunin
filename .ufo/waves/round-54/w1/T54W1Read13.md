# T54W1Read13 — cold read: `## Pin disposition and provenance correction — round 13`

- Heading as given and read: `## Pin disposition and provenance correction — round 13`
- Candidate: `59c38109bf119d0e9d4f878644a82babc937bc1e` (C0)
- `reader-section.py` output: `{"heading": "## Pin disposition and provenance correction \u2014 round 13", "cand": "59c38109bf119d0e9d4f878644a82babc937bc1e", "start": 1542, "end": 1572, "section_sha256": "ad8d6c4010f2c584a8fd34795625d66ab1a7ffcc91463a49e6d122ca06e4bf15"}`
- Bytes read only from `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 59c38109bf119d0e9d4f878644a82babc937bc1e:SKILL.md`, lines 1542–1572. I re-derived the section with the frozen round-18 `sectionize()` at that blob and got the same span and `section_sha256` `ad8d6c40...f15`, so the span and the requested sha agree.

## Findings

### F1 — row 1's Observation→Decision pair is contradicted by the tool in a pin/digest-disagreement state

Quote (byte-exact from the section, and byte-exact in this MD):

```
| Recorded target bytes equal the current worktree | Report `unchanged` content |
```

Why: `unchanged` in the C0 tool requires a third precondition the row does not state — the pin must verify against the manifest digest (`tools/pin-disposition.py:67-71` "Content status semantics: `unchanged` requires a readable regular worktree file, verified pinned evidence (the manifest digest equals the blob at the recorded commit), and byte equality with expected_sha256", enforced at `:563-567` `elif pinned["status"] != "verified": content_status = "unavailable"` with `worktree["reason"] = "pin_not_verified"`), so a readable worktree whose bytes equal the recorded target is still reported `unavailable`, not `unchanged`, whenever the manifest digest disagrees — the very state the tool's own `pinned-blob-mismatch` selftest asserts (`tools/pin-disposition.py:1157-1179`: `pin-observed` and `worktree-sha` both `SELFTEST_V1_SHA256`, `content` `unavailable`, `worktree-reason` `pin_not_verified`).

The row is unqualified under either reading of "Recorded target bytes":

- Reading A (the blob bytes at the recorded commit): equals the worktree, yet the tool says `unavailable` when the manifest digest points elsewhere.
- Reading B (the manifest's recorded digest): equals the worktree, yet the tool says `unavailable` when the pinned blob differs from that digest.

Row 3 ("Repo, commit, path or pin cannot be evaluated | Report `unavailable`, with reason") does not close the gap: in both states the pin *was* read and evaluated; it disagreed. Neither row states the verified-pin precondition, while row 2 does ("Readable verified pin differs from current bytes"), so the table is internally asymmetric on exactly the `unchanged` decision.

## Runnable receipts for F1

Both run the C0 `tools/pin-disposition.py` from a `git clone --shared` of the lane checked out at `59c38109bf119d0e9d4f878644a82babc937bc1e` (`/fast/scratch/hyaku/tameshi-r54/T54W1Read13/lane`, `git rev-parse --show-toplevel` printed that clone). Fixture root: six canonical leg repos, one commit per leg; manifests and full outputs under `.ufo/waves/round-54/w1/T54W1Read13-receipts/`.

`T54W1Read13-receipts/reproduce.sh` rebuilds both fixtures and reruns the probe under its own `mktemp -d` scratch (last run exit 0; outputs A and B as quoted below, identical figures).

Fixture A (reading A: recorded blob bytes equal the worktree; manifest digest disagrees):

```
$ printf '%s' 'KIMI-WRONG-DIGEST-Y' | sha256sum   # Y = 5654df33...13953, committed blob X = 3c3bd58d...e6236
$ python3 tools/pin-disposition.py --manifest $S/fixture-manifest.json --root $S/fixture-root
exit=0
counts: {'legs': 6, 'unchanged': 5, 'changed': 0, 'unavailable': 1}
js-kimi-census: pinned.blob_sha256 3c3bd58d3232a6d416ecd23c0bf966cbfb59ebc039e94c3df62bc6de9d9e6236 (status mismatch, reason pinned_blob_mismatch)
                worktree.sha256    3c3bd58d3232a6d416ecd23c0bf966cbfb59ebc039e94c3df62bc6de9d9e6236 (status unavailable, reason pin_not_verified)
                content_status     unavailable
```

Fixture B (reading B: manifest digest equals the worktree; pinned blob differs):

```
$ python3 tools/pin-disposition.py --manifest $S/fixture-manifest-b.json --root $S/fixture-root
exit=0
counts: {'legs': 6, 'unchanged': 5, 'changed': 0, 'unavailable': 1}
js-kimi-census: pinned.blob_sha256 3c3bd58d...e6236 (status mismatch)
                worktree.sha256    5654df33...13953 (== manifest expected; status unavailable, reason pin_not_verified)
                content_status     unavailable
```

In both states the row-1 observation holds and the tool reports `unavailable`.

## What I opened and checked

Section span and sha: `reader-section.py` at C0, then the same `sectionize()` over `git show C0:SKILL.md`.

Anchors cited by the section:

- `corpus/SOURCES.md` at C0: rows S003 (line 14), S041 (line 50), S047 (line 56), S048 (line 57) all resolve; S047 still describes itself as superseding S041, and S048 supersedes S047's paraphrase. The section's "Sources: S003 and PIT precision correction S047 (historical S041 retained)" still matches the anchored document's own line ("S047 — ... cited as the round-13 precision-correction row that supersedes S041's teaches cell", `corpus/knowledge/incremental-pin-disposition.md` line 3), so I do not report the later S048 refinement as a defect in this section.
- `corpus/knowledge/incremental-pin-disposition.md` exists at C0; its §3 (lines 123–137) gives the same three-identity/`not_established` reading the table rows 4 and 5 encode, and §6 (lines 327–337) records the same six rows the round-13 artifact holds.
- `corpus/lessons/round-12-verifier-spotcheck.md` exists at C0; "## Routed defects and residuals" item 3 (line 146) states exactly what table row 5 and recipe step 4 claim (nested `declaration.kind=null` repaired only through new evidence, frozen declaration not rewritten).
- `.ufo/evidence/round-13/` exists at C0 with `pin-manifest.json`, `pin-dispositions.json`, `witness-metadata.json` and the other round-13 receipts.

Commands in the recipe, executed at C0 in the clone (both resolve and run):

- `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` → exit 0, `observed_at` 2026-10-28T14:29:34Z, `not_compared` present (8 entries), every row carries `head.commit` (the sibling branch tip) and `result_reuse=not_established`, `counts` `{"legs": 6, "unchanged": 3, "changed": 3, "unavailable": 0}` — matches the artifact.
- `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` → exit 0, `WITNESS_METADATA: metadata_consistent reason=ok ... inputs=summary,declaration,declared,rerun_summary`.

Table cells checked against the artifacts:

- Row 2 (`changed`) and row 1 in the ordinary cases: the round-13 `pin-dispositions.json` unchanged rows have `pinned.blob_sha256 == head.blob_sha256 == worktree.sha256`; the changed rows have `pinned.status=verified` and `pinned.blob_sha256 != worktree.sha256`.
- Row 4: all six rows carry `result_reuse=not_established`, and the three identities are exactly the three hashes in the artifact (pinned blob, branch-tip blob, worktree).
- Row 5 and step 4: `.ufo/evidence/round-12/BashWitness/summary.json` has `declaration.kind=null` with the explicit top-level kind only in `declaration.json` (`declared-witness mapping (not a blind preregistration)`); the rerun summary's `declaration.kind` is also null; the companion's `scope.covered_null_observations` covers the canonical summary only and names the rerun summary in `uncovered_null_observations`. The producer at C0 writes the summary kind from the top-level `declaration.get("kind")` (`tools/bash-witness-study.py:816`) and its selftest asserts `summary preserves top-level exposed declaration kind` (`:1699-1701`), so step 4's "fixed separately ... regression selftest" resolves.
- Step 2's "observes only hashes and git metadata. ... It executes no sibling gate": `tools/pin-disposition.py` runs only `rev-parse`, `symbolic-ref`, `show-ref`, `for-each-ref`, `cat-file` (docstring `:82-92`), and the run above produces observations only.
- Step 5 (do not rerun a sibling gate) does not contradict step 3: `witness-metadata --check` validates local digest-pinned receipts, it does not execute a sibling gate.

No other self-contradiction, unresolved anchor, or stale cell found in this section. The only reported defect is F1.
