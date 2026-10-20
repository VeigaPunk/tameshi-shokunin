# R09 — Supersession-harm review

## Finding — high: superseding round 17 also requires retargeting round 14

The round-17 registry has `evidence-disposition-round14-superseded` with `status: "superseded"` and `superseded_by: "evidence-disposition-round17"` (`tools/registry.json:250-270`); the round-17 row is presently active and expects exit 0 (`tools/registry.json:197-220`). The proposed round-18 transition adds an active round-18 row and demotes round 17. If it leaves the round-14 pointer unchanged, the result is an invalid registry: `registry-check.py` requires each `superseded_by` target to exist and be active (`tools/registry-check.py:248-269`), and returns 2 on registry validation errors before row execution (`tools/registry-check.py:514-516`). This breaks the no-harm registry check; it is not the expected exit-2 behavior of a superseded gate.

**Required correction:** point both superseded rows (round 14 and round 17) at the new active `evidence-disposition-round18` row. Keep the old commands and `expect.exit: 0` values intact. Do not drop either old row. The same active-target invariant is explicitly exercised in the registry-check selftest (`tools/registry-check.py:851-900`).

## R17 precedent and evidence required

The exit-2 mismatch of the old round-17 gate is **not by itself a harm**. The predecessor precedent is explicit: the round-14 command still ran, returned 2 against expected 0, and remained visible as superseded rather than being repaired or removed (`corpus/lessons/round-17-verifier-spotcheck.md:249-253`). The checker contract says active and superseded rows both run; superseded results remain observable but are excluded from the active held/total calculation (`tools/registry-check.py:30-38`). Its final exit is 0 iff every active row holds; it reports the superseded count separately (`tools/registry-check.py:541-551`), and prints each superseded row's expected/observed exit (`tools/registry-check.py:562-575`).

The R17 closure backed that precedent with revision-bound full-registry receipts: the old baseline was 22/23 active rows held, then 23/23 after the fix; the older round-14 mismatch remained visible as one superseded row (`corpus/lessons/round-17-verifier-spotcheck.md:239-255`). That is the pattern to preserve, not a warrant to suppress the mismatch.

For this migration, the accompanying evidence must include:

1. The appended round-18 dispositions manifest required by contract E: schema `evidence-dispositions-v2`, supersedes the round-17 manifest, records the round-13 pins and `tools/bash-witness-study.py` as historical inputs at the required pinned revision, and runs `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json` with exit 0 and a clean result. Preserve the old round-13 and round-17 evidence bytes.
2. Before/after **full registry** reports at explicit revisions, with registry digest and per-row output available. The after report must show the round-18 row active and passing, the round-17 and round-14 rows still executed and their observed outcomes visible as `superseded` (including `expect=0 got=2` where observed), and all active rows held. Do not change the old rows' expected exit to 2 merely to make them pass.
3. Correct supersession links: both old rows target the active round-18 row. With only this one row added and the round-17 row demoted, the expected aggregate is 28/28 active held and `superseded=2` **[INFERENCE: assumes no other registry-row changes]**, with registry-check exit 0. The complete output must establish this; a scoped `--only` pass is not a substitute.

## Other recorded pins of the old tool bytes

I made a revision-pinned snapshot of `183f87b899e6cae46be98d251cbc87fb5118f6ca` (`git archive` into `/tmp`; command completed successfully). The specialized grep search for prefix `49e9e5e2` found 65 files; searching the full SHA-256 `49e9e5e20b73f115626fb4f81aac9b238e0f01811230c4fd0ff726c1f350ad80` found 53 files in that committed snapshot. Of those, 42 are structured JSON pin/receipt records. The round-13 `expected.json` and `verification.json` are the historical migration anchors; the following are the **other** structured records containing that exact SHA:

- `.ufo/evidence/round-17/c1-measure-e3827ee.json:182`
- `.ufo/evidence/round-17/coldread/ledger.json:1508,2215,2393,2441,2530,2586,2687,2767,3025,3103,3534,3593,3715`
- `.ufo/evidence/round-17/coldread/traces/CR30/06-no-daemon-timer.json:106`
- `.../CR45/04-witness-count.json:51`, `05-witness-selftest.json:26`, `06-witness-check.json:122`, `11-witness-usage-64.json:25`, `12-witness-cannot.json:28`, `13-witness-tampered-integrity.json:28`, `15-count-readonly.json:55`
- `.../CR46/5.json:29`
- `.../CR48/01-live-before.json:43`, `02-live-fixed.json:43`, `03-frozen-before.json:43`, `04-frozen-fixed.json:43`, `06-round17-live-entry.json:44`
- `.../CR49/2.json:43`, `3.json:44`
- `.../CR51/03-disposition-r14-superseded.json:43`, `04-disposition-r17-live.json:44`, `06b-disposition-frozen-replay-rooted.json:43`, `23-disposition-relabel-only.json:42`
- `.../CR52/01.json:43`
- `.../CR55/01-step1-before.json:44`, `02-step2-json.json:44`, `03-step2-text.json:43`, `18-p7b-gitdir-clean.json:40`, `p2-unneeded-trace.json:34`
- `.../CR56/16.json:44`, `2.json:44`
- `.../CR57/3-historical-r14-recipe.json:43`
- `.../RR2/13.json:2211`; `.../RR4/4.json:30`; `.../RR5/8.json:43`, `9.json:44`; `.../RR7/6.json:43`, `7.json:43`
- `.ufo/evidence/round-17/noharm-baseline-98bea7d.json:14,70`
- `.ufo/evidence/round-17/tool-pin-map.json:20,25,172,191,205,4075,4094,4108` (repeated expanded entries also retain the digest in the listed line neighborhoods)
- `.ufo/evidence/round-17/redbefore/legacy-r14-inputs.json:22`

The two migration-anchor occurrences are `.ufo/evidence/round-13/expected.json:11` and `.ufo/evidence/round-13/verification.json:11`. Other exact-SHA text hits are historical evidence/prose rather than additional JSON manifests: `.ufo/evidence/round-17/historical-rev.txt`, `.ufo/evidence/round-17/redbefore/digest-diff.txt`, `.ufo/waves/round-13/w1/MetadataSchema.md`, `.ufo/waves/round-14/w1/ProducerMechanism.md`, `.ufo/waves/round-17/w2/CR45.md`, `CR46.md`, `CR47.md`, `.ufo/waves/round-17/w3/RR4.md`, `RR7.md`, `corpus/lessons/round-13-verifier-spotcheck.md`, and `corpus/lessons/round-17-verifier-spotcheck.md`. These are historical records; do not rewrite them as part of the manifest migration.

## Verification gaps

- Revision-pinned `git show` reads of `tools/registry.json` and `tools/registry-check.py` completed successfully; the immutable snapshot was created from the dispatch revision. No registry gate or runtime was run in this reviewer pass.
- The LSP device is unavailable (`write xd://lsp` returned “No such tool”); semantic source findings above come from direct reads of the pinned files, not grep. Grep was used only for the requested literal-digest census; its result reports matches but no process exit code.
- No round-18 full-registry after-receipt was available in the dispatch snapshot, so the planned clean result is not verified here.

**Verdict: falls as currently specified unless the existing round-14 supersession link is retargeted to the active round-18 row; the expected superseded-row exit-2 itself is precedent-compatible.**