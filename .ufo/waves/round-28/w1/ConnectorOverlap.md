# Round 28 — sibling overlap

## Verdict

Adjacent overlap found in Souji, Mori and Tabi. **Report only: Tameshi absorbs nothing.** No production changes, integration, claim judgment or monitor execution were performed. This report is the only file written.

**Axes:** adjacency is this assignment's axis; calibration is the round's declared C1 axis. Freshness and operability are affected surfaces of the proposed ordering change, not additional round claims. No axis improvement or no-harm result is asserted as measured.

## Evidence

Paths below are relative to `/home/vgpnk/Projects/shokunin/`, not to Tameshi. Findings are static readings of local sibling files. Tameshi's content, monitor and receipts were not searched; its input-drift incident and C1 target come from the assignment, not an independent measurement here.

### Direct overlaps

| Owner and evidence | Mechanism and relevance | Boundary |
|---|---|---|
| Souji — `souji-shokunin/tools/souji-evidence-cache.py:6-17,39-47,76-80,1019-1021` | Retained-result eligibility depends on declared input SHA-256 values. Changed bytes produce `dependency-digest-mismatch`, not continued reuse of an earlier success. This is the closest overlap with bookkeeping invalidating previously earned credit. | Souji owns workspace hygiene and preservation receipts (`souji-shokunin/PROVINCE.md:3-17`). Its cache gate is not a Tameshi cold-read monitor. |
| Mori — `mori-shokunin/tools/mori-content-review.py:271-280,309-329` | Review rows carry `blob_sha256`; the checker hashes the selected revision's blobs and emits `CONTENT_REVIEW_STALE` when a row names different bytes. Review coverage is therefore attached to particular content, not merely a path or an earlier decision. | Mori observes fleet and wave state; detection and report only (`mori-shokunin/PROVINCE.md:3-18`). No review-ledger ownership moves to Tameshi. |
| Tabi — `tabi-shokunin/scripts/check-measurement-binding.mjs:4-11,580-613` | Checks the counter digest at both measured and target revisions, then diffs the declared counted inputs **and the counter path**. `counted_input_changed` prevents carrying a measurement forward across a relevant edit, even if its count happens to remain the same. | Tabi owns browser and web-interaction craft (`tabi-shokunin/PROVINCE.md:3-21`). This is measurement-binding adjacency, not browser scope for Tameshi. |

### Ordering and integration lessons

- **A correction file is itself an input.** `mori-shokunin/corpus/knowledge/freeze-order-r18.md:40-57` requires both the register and supplied corrections to match their explicit input revision. `mori-shokunin/tools/mori-freeze-order.py:126-160` hashes loaded bytes and compares them with the revision's blob; `:397-404` records separate register, corrections and executing-script identities. The bookkeeping correction cannot silently inherit the original measurement's binding.
- **Frozen-before-build and final-before-review are different orders.** Mori's lesson `:7-24` says editing a frozen requirement after implementation yields `co-evolved`; appended corrections do not rewrite the historical label. This does not license retroactively calling a late Tameshi bookkeeping freeze pre-build.
- **A correct stale detector is insufficient if its caller ignores it.** `souji-shokunin/corpus/lessons/round-14.md:9-12,42-50` records a consumer returning the old source after the gate had reported `dependency-digest-mismatch`. This is a sibling's recorded observation, not an execution repeated here.
- **Concurrent review and integration can mix revisions.** `souji-shokunin/corpus/lessons/round-16.md:14` records reviews of one committed revision while L1 changed the working tree, and forbids inheriting acceptance numbers from those older reviews. Its correction explicitly remains a rule without a mechanical check.

### Exact commands and observed output

Read-only metadata commands ran from `/tmp`:

```text
env GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin/souji-shokunin rev-parse HEAD
4edb25dfe262515d0da63224bbba71e02e36cba5

env GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD
ac696ad3037c3071584df60d84b5bf0af9818dd6

env GIT_OPTIONAL_LOCKS=0 git -C /home/vgpnk/Projects/shokunin/tabi-shokunin rev-parse HEAD
e3cf4e0d30bb835532ff44b118c5ad52e09eb76d
```

The heads locate the sibling repositories; no clean-working-tree assertion is made. The inspected file bytes were separately fingerprinted:

```text
sha256sum /home/vgpnk/Projects/shokunin/souji-shokunin/tools/souji-evidence-cache.py /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-content-review.py /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-freeze-order.py /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/freeze-order-r18.md /home/vgpnk/Projects/shokunin/tabi-shokunin/scripts/check-measurement-binding.mjs
dd279ba95eebd13a6674f79983cec286fd856aa6d7e0719bf551ae0fc08939d6  /home/vgpnk/Projects/shokunin/souji-shokunin/tools/souji-evidence-cache.py
fa88a6b034d1cdb955fc9db1c0aa38efd44bcc9495d6086873b3ebd6476b29cc  /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-content-review.py
ec1be305d9fbf81d8169554cdb8f681a819f97ee89bb1362f08c4de0b427b547  /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-freeze-order.py
00d791bfe61bd7818855e1d5bc527490ecb71347c24f93782c7d160419df52c1  /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/freeze-order-r18.md
388c2b4987bbb9f39f172cd40ca392b03bc9c869c1682b77576b0b986c14af74  /home/vgpnk/Projects/shokunin/tabi-shokunin/scripts/check-measurement-binding.mjs

sha256sum /home/vgpnk/Projects/shokunin/souji-shokunin/corpus/lessons/round-14.md /home/vgpnk/Projects/shokunin/souji-shokunin/corpus/lessons/round-16.md
a2a59bf8d4a95da47448e720ce254bc5c56b8dda00fe49f45ad54bbf1b4112fe  /home/vgpnk/Projects/shokunin/souji-shokunin/corpus/lessons/round-14.md
1a057e10f9a0f6ad49cac3791ad0c1e7a231f63455d850cb6c5a1692f0dbb34c  /home/vgpnk/Projects/shokunin/souji-shokunin/corpus/lessons/round-16.md
```

Search method: sibling-root enumeration with `glob`, followed by searches for `input-drift`, input digests, cache keys, stale results and edit/verification ordering. Broad recursive searches timed out or returned duplicate nested worktree copies; evidence was narrowed to explicit sibling tool and lesson files. This is a positive overlap scan, not an exhaustive claim that other siblings have no overlap. No external sources or additional runtime were used. No tools were installed or updated.

## One bounded proposed move — final-input barrier before cold reads

Smallest safe correction, for L1 consideration only: **finish every bookkeeping edit within the monitor's existing declared input set before the final fresh cold reads, then treat that input revision as closed until the terminal C1 measurement.** In particular, finish source reopening and its required recorded corrections before those reads. Keep the existing dependency declarations, digest checks, independence requirement and valid-failure recording unchanged.

If another declared input must change afterward, retain the old receipt with its original binding and obtain new independent reads for the sections the existing monitor invalidates. Never refresh an old receipt's digests to fit the new tree. No new cache, sibling tool import, dependency exclusion or production patch is proposed.

[INFERENCE] The useful synthesis is that bookkeeping belongs on the **input side** of the final review barrier whenever the monitor declares it an input. It is not automatically harmless output merely because humans call it bookkeeping.

### Second-order effects and contradictions

- **Runtime:** ordering changes, not monitor behavior. Independent reads can remain concurrent against the same fixed revision. A late input change can still require additional work; no runtime saving is measured.
- **Contract / calibration:** a digest mismatch legitimately removes current credit even when the previously reviewed paragraph is unchanged. Semantic similarity and byte binding are different claims. Repair ordering, not the digest check; do not recover credit by rewriting history.
- **Substrate / operability:** reviewers and the final measurement must refer to the same declared bytes, not a mixture of a committed revision and live working-tree edits. A report written last is harmless only if it is outside the existing input set; this scan did not establish that for Tameshi.
- **Verification / freshness:** a gate's stale finding must reach its consumer, as Souji's fallthrough lesson shows. Conversely, Souji's success-only reuse policy must **not** be imported as a filter on cold-read evidence: a fresh failing Tameshi read remains valid evidence under this assignment.
- **Risk:** the recommendation is only as complete as the existing declared input set; Souji explicitly disclaims transitive dependency completeness (`souji-evidence-cache.py:217-229`). Freezing incomplete declarations would not prove adequate coverage. Do not silently narrow them to avoid invalidation.

## Verification for the integrator — not executed here

In the integrator's own `/tmp` clone, use the assignment's unchanged monitor:

```sh
python3 .ufo/evidence/round-27/c1-measure.py --repo CLONE --rev 06b59b93697c9b0a8795ac2d0fe3d0bd7e18572c
python3 .ufo/evidence/round-27/c1-measure.py --repo CLONE --rev LANDED_HEAD
```

The assignment's expected baseline is `covered=60/64 restraint=6 box3_mismatch=1`; its target is `covered=64/64 restraint=8 box3_mismatch=0`, exit 0. Neither was observed by this seat. Inspect the final declared inputs and read receipts together: all required independent reads must bind to the final inputs, failing reads must remain recorded, and stale receipts must not be counted merely because a caller retained them. If further bookkeeping changes a declared input, the earlier measurement cannot stand as the terminal measurement.

No monitor, gate, selftest or sweep was run. This report supplies adjacency evidence and one ordering proposal only.
