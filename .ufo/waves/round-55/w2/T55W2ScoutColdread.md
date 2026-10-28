# T55W2ScoutColdread — cold-read floor at base and at C0

## Verdict

At base `0a2010acd1e92e4e332774050825e21bcfc7e079` the round-21 cold-read monitor credits **64/64** (`calibration_restraint_score=8`, `box3_full_page=true`). At C0 `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` it credits **46/64** (`score=6`, `box3_full_page=false`). The round-48 precheck exits 1: `lost=18 RED`. The ledger blob is identical at the two revisions. Exactly one SKILL.md section changed bytes: `## Standing rules` (`no-ledger-entry`). The other 17 lost headings kept their section sha and failed the input gate.

Binding the three wave-2 readers to `## Standing rules` repays **one** of those 18. It does not return the floor to 64/64. The floor returns to 64/64 only when every heading below has a ledger entry whose `sha256` is that heading's C0 section sha and whose gated inputs verify at the revision being measured. `no-harm.sh`'s `coldread-floor` arm requires `score>=8` and `credited>=64`; the score drop 8→6 is the box-3 full-page term (`sections_covered == sections_total`), so 64 covered sections restores the score as well. `SHONEN.md` is unchanged between the two commits.

## Commands and output

```
LANE=/home/vgpnk/Projects/shokunin/tameshi-shokunin
FLOOR=0a2010acd1e92e4e332774050825e21bcfc7e079
CAND=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
python3 $LANE/.ufo/evidence/round-21/coldread/measure.py --repo "$LANE" --rev "$FLOOR" --explain
# exit 0
# rev=0a2010acd1e92e4e332774050825e21bcfc7e079
# calibration_restraint_score=8
# coldread.sections_total=64 sections_covered=64 box3_full_page=true
# reasons={"credited": 64}  missing=[]

python3 $LANE/.ufo/evidence/round-21/coldread/measure.py --repo "$LANE" --rev "$CAND" --explain
# exit 0
# rev=9cf0146b94ddba12d454ebf7288ce6e5c5d535bb
# calibration_restraint_score=6
# coldread.sections_total=64 sections_covered=46 box3_full_page=false
# uncovered=18 (one no-ledger-entry, seventeen input-drift)

bash $LANE/.ufo/evidence/round-48/quality/coldread-precheck.sh "$LANE" "$FLOOR" "$CAND"
# exit 1
# COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=9cf0146b94dd cand_credited=46 lost=18 RED
```

Section shas are `sectionize()` in `.ufo/evidence/round-18/measure.py` (the function the round-21 selector loads), over `git cat-file blob REV:SKILL.md`. Not a private hasher.

```
## Standing rules at FLOOR  start=17 end=40 sha256=61736dcebc2d3d148255f9b3edd0ceb1c7cf2284f2969475b8da838ded9a78fc
## Standing rules at CAND   start=17 end=44 sha256=acfb671afd767c32476f57b040399972f6c870cd7dde3d821c344cae1a9ad767
sections whose sha changed: 1 (## Standing rules). headings only at one rev: none. sections_total stays 64.
SKILL.md sha256 floor=b5ff9727485da844a0c93d8f5914f957eba03d2c37cda59e8e38fd7a04ada195
SKILL.md sha256 cand =e0ce89f7866062062f4987358e353c8626c18f56d2eb1589225af99f44d695a6
ledger .ufo/evidence/round-21/coldread/ledger.json identical at both revs.
```

`git diff --name-status --no-renames FLOOR CAND` outside `.ufo/waves/` is 24 paths. The production edits that move input bytes are:

```
M  LOG.md
M  SCORECARD.md
M  SKILL.md
M  corpus/QUALITY.md
M  corpus/SOURCES.md
M  corpus/knowledge/scratch-root-contract.md
M  corpus/lessons/round-54.md
A  corpus/lessons/round-55.md
M  tools/context-capture.py
M  tools/registry-check.py
M  tools/registry.json
M  tools/repeat-control.py
```

plus the added `.ufo/evidence/round-55/**` counter files. `git diff FLOOR CAND -- SKILL.md` is one hunk, inside `## Standing rules` (the scratch bullet, old lines 34–39). No other heading's bytes moved.

## Credit rule (what "names an input" means)

From `.ufo/evidence/round-18/measure.py`, as the round-21 selector runs it (`measure.py` sets `LEDGER_PATH` and adds the round-21 ledger to `IGNORED_INPUTS` before `main()`):

- A section is covered only when at least one ledger entry whose `sha256` equals `sectionize()`'s sha of that section passes every gate, and no non-stale entry vetoes (`coldread`, match at `by_sha.get(sec['sha256'])`). Heading text is not the key. Changed section bytes ⇒ `no-ledger-entry`. The input gate is not reached, so the reason names no path.
- The input gate (`inputs_view` + `input_failures` + `input_reason`) checks every `inputs` key except `SKILL.md`, `.ufo/evidence/round-17/coldread/ledger.json`, `.ufo/evidence/round-18/coldread/ledger.json`, and `.ufo/evidence/round-21/coldread/ledger.json`. A blob whose sha256 differs from the recorded value is `input-drift:<path>`. The section reason is `';'.join(sorted(set(each matching entry's reason)))`. The precheck prints the unique `input-drift:` paths from that string.
- An entry that fails the input gate is stale and does not veto (`entry_is_stale`). Credit at the floor was carried by the one entry per heading that was input-clean there. For all 18 headings that entry's `read_rev` is `99c3bc88d704566197783f66b211ee0a830e0330`. Older sibling entries were already drifted at the floor; their paths still appear in the C0 reason string but they are not why credit was lost.

## The drifted section

`## Standing rules` — section bytes changed, `cand_matching_entries=0`, reason `no-ledger-entry`. Precheck: `LOST ## Standing rules | drifted=` (empty). The credit rule names **no inputs** at C0.

The floor-clean entry (2497 gated inputs, `class=instruction`, `verdict=gap-minor`, `read_rev=99c3bc88…`) would have failed the input gate on exactly these six paths, which are the C0 edits:

- `corpus/QUALITY.md`
- `corpus/SOURCES.md`
- `tools/context-capture.py`
- `tools/registry-check.py`
- `tools/registry.json`
- `tools/repeat-control.py`

`LOG.md`, `SCORECARD.md`, and `corpus/knowledge/scratch-root-contract.md` also changed and are not in that failing set. The round-21 ledger and `SKILL.md` are ignored by the gate even when an entry records them.

## The other 17 — inputs the credit rule names

Section sha is unchanged (floor sha = C0 sha). `named` is the precheck/`input-drift:` set (every matching entry). `causal` is the subset on the entry that was clean at the floor; that subset is what cost the credit. `stale-only` was already drifted at the floor on an older entry and did not veto.

| heading | C0 section sha256 | named by the credit rule | causal (floor-clean entry) | stale-only |
|---|---|---|---|---|
| `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` | `77d88c0226463dfc97f0074a5cafedc1044be0a2a16c85fbb6237ac06a5140da` | QUALITY, SOURCES, context-capture, registry-check, registry.json, repeat-control | same (7702 keys) | — |
| `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` | `430dd86f25b6ce3d5ed51012d54de7cdad7213c6353eb7701323de762b9fb993` | SOURCES | SOURCES (30 keys) | — |
| `### Triggers T1–T3 and the re-pin rule` | `2350210704efcc3becfbcd40a63775ad591910039744ac6d072881b3deef7801` | QUALITY, SOURCES, service-limits, bash-witness-study, context-capture, evidence-disposition, pin-disposition, registry-check, registry.json, repeat-control | QUALITY, SOURCES, context-capture, registry-check, registry.json, repeat-control (89 keys) | service-limits, bash-witness-study, evidence-disposition, pin-disposition |
| `### The service's limits — what tameshi refuses to mutation-test` | `7e240e714c6e6fa75a01061ef171238401b3a91fdd69cc86c13f97b151b848f6` | context-capture, registry-check, registry.json, repeat-control | same (39 keys) | — |
| `## The operator's runbook and the six-leg regression (round 10, measured)` | `636e850f885cb39904d100f67446e1039aa48c6510c2a66ea6e6d5aaa089faf7` | registry.json | registry.json (11 keys) | — |
| `## Repeated controls and gate registry — round 12` | `3a78cbfcef65ada68c09342e5cbc71dc067d2b5258c3afbff6ea94e37a82b831` | SOURCES, repeat-control | same (168 keys) | — |
| `### Gate/probe registry` | `99285e24a71a8d2a0ea3fd6bcafe7e080acb23bfd653e7cbb3b71dfdc5144c77` | bash-witness-study, repeat-control | repeat-control (124 keys) | bash-witness-study |
| `## Pin disposition and provenance correction — round 13` | `1fa3130bc6d4bc46124a1c0e234583657bb6c7623256dfa85f4db2a7fb91da31` | SOURCES | SOURCES (33 keys) | — |
| `### Round-13 gate/probe registry` | `896722c4941841f228810678befe82e9910cc66eb67c3de45d7561ce4668566d` | SOURCES, bash-witness-study, pin-disposition | SOURCES (24 keys) | bash-witness-study, pin-disposition |
| `## Effective expectation reconciliation — round 14` | `6110606ea4a977c70f0fa67ef8bdc97b4a4d2e51e9e8c2a96e984c7886376cbe` | SOURCES, context-capture | same (42 keys) | — |
| `## Context gate classification and explicit exit classes — round 15` | `132cfb9ef1aa07111af42389e4fe862152e3118b3a8bb66f1d84a6a332e7edf6` | SOURCES, bash-witness-study, context-capture, evidence-disposition, mutate-and-run.sh, pin-disposition, registry.json, trace-inputs | SOURCES, context-capture, registry.json (42 keys; 20 entries match, 1 was clean) | bash-witness-study, evidence-disposition, mutate-and-run.sh, pin-disposition, trace-inputs |
| `### Round-15 gate/probe registry` | `78edbb693cdddcab61902811985918087529c444d3fb01da7bcaf4a674daf4ea` | context-capture | context-capture (38 keys) | — |
| `## Live-tree re-pin and entry-command monitor — round 17` | `6395900104ed76b6f9dbfae1bb33384197982447e1db7dbaf89bf2b6b1b9beac` | QUALITY, SOURCES, context-capture, registry-check, registry.json, repeat-control | same (78 keys) | — |
| `### Round-17 gate/probe registry — re-pin and monitor` | `309f83283e7518eb00cf7ce4296daf4bf5e80843ff2b3046755eb55d3ba8fb8c` | SOURCES, context-capture, registry-check, registry.json, repeat-control | same (51 keys) | — |
| `### Round-18 gate/probe registry — routed-defect closure` | `661f63518af62b198f68ec5400778d9662df725d84744ad428dacc08823e6d7e` | QUALITY, SOURCES, registry-check, registry.json | same (71 keys) | — |
| `### Round-21 gate/probe registry — finite environment differential` | `eccd3ec82207fa69cee544f8f4ebfc0f9a473fe7254b8041ae2f5924f8d00a06` | round-15/verify.py, QUALITY, SOURCES, env-diff.py, registry-check, registry.json | QUALITY, SOURCES, registry-check, registry.json (75 keys) | `.ufo/evidence/round-15/verify.py`, `tools/env-diff.py` |
| `### Round-26 gate/probe registry — report interop` | `cc23587b353fb780d4310aebc7277e4030729ae767850e2e826d2ff151bdea52` | context-capture, registry-check, registry.json, repeat-control | same (74 keys) | — |

Path prefixes omitted above: `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/knowledge/service-limits.md`, `tools/<name>`. The stale-only paths did **not** change between the two commits; they are named because an older entry still matches the section sha and still fails `input_failures`.

This 18-heading set is identical to the precheck `LOST` lines and to the worktree file `.ufo/evidence/round-55/c1/lost-headings-at-c0.json` (that file is untracked: not at C0, not in HEAD).

## What the three wave-2 readers must bind

The three seats are `T55W2Read01`, `T55W2Read02`, `T55W2Read03` (`spec-w2.json`). Each must write `.ufo/waves/round-55/w2/<seat>.json` **and** the sibling `.md`:

```json
{"heading": "## Standing rules", "cand": "9cf0146b94ddba12d454ebf7288ce6e5c5d535bb", "section_sha256": "acfb671afd767c32476f57b040399972f6c870cd7dde3d821c344cae1a9ad767", "findings": []}
```

`cand` is the full 40-hex commit. The binder compares `d.get('cand') != c0` after `git rev-parse --verify C0^{commit}` (`.ufo/evidence/round-55/integrate/binder.py` at HEAD `c31cdd92345a06f056e430090b818058d86f949c`, not present at C0). `section_sha256` is the C0 `sectionize` sha above, not the floor sha `61736dce…`. `start`/`end` are not part of the match; the binder recomputes them (`start=17`, `end=44` at C0).

`findings` must be `[]`. The binder's allowed count is `RES.get(heading, 0)`. HEAD's `resolutions.json` items have `id`/`from`/`finding`/`decision`/`evidence` and no `heading` or `n`, so the loader at binder.py:51–54 (`RES[item['heading']] = int(item['n'])`) raises `KeyError` before `main` if that file is left as it is. With the loader satisfied and this heading absent, allowed is 0, and `len(findings) > 0` skips the heading (`reader-has-findings`). A non-empty `findings` list is a legitimate reader verdict and is **not** a re-key bind.

Order matters. `WAVE_DIRS = (w2, w3)` and the file list is `sorted` across both. `w2` sorts before `w3`. The first file whose `heading`+`cand`+`section_sha256` match is accepted, and a match with too many findings `break`s without trying a later file (binder.py:113–127). `T55W2Read01.json` sorts before Read02 and Read03, and before wave 3's `T55W3R07` (the w3 reader for this same heading). A findings-bearing Read01 blocks the other two and blocks `T55W3R07`. All three wave-2 readers must bind the object above with `findings: []` and a sibling `.md`.

That bind is the key for `## Standing rules` only. After a successful re-key of that one heading the monitor would read 47/64, still RED. The other 17 headings need the same shape of reader, each with `cand` = the full C0 hash and `section_sha256` = the unchanged sha in the table (those are the `T55W3R01`–`T55W3R18` seats in `spec-w3.json`, one heading each, including a second Standing-rules reader at `T55W3R07`). The binder then re-hashes the union of prior entries' inputs at PIN, dropping `LOG.md`, `SCORECARD.md`, `SKILL.md`, and the round-21 ledger. Old drifted entries stay stale and do not veto, so the new entry credits **if** those re-hashed blobs still match at the revision `no-harm.sh` measures. A PIN that edits any causal path again drops the section a second time.

## Artifacts opened

- `.ufo/evidence/round-21/coldread/measure.py` (selector; ledger path; `IGNORED_INPUTS`)
- `.ufo/evidence/round-18/measure.py` (`sectionize`, `coldread`, `input_failures`, `input_reason`, `inputs_view`, `entry_is_stale`)
- `.ufo/evidence/round-48/quality/coldread-precheck.sh`
- `.ufo/evidence/round-55/no-harm.sh` (the `credited>=64` arm; present at C0)
- `.ufo/evidence/round-55/integrate/binder.py` and `resolutions.json` (HEAD `c31cdd92`, absent at C0)
- `.ufo/evidence/round-55/c1/lost-headings-at-c0.json` (untracked worktree; set-equal to the measured 18)
- `.ufo/waves/round-55/spec-w2.json`, `spec-w3.json` (reader seat names)
- git blobs `SKILL.md` and `.ufo/evidence/round-21/coldread/ledger.json` at both revisions; `git diff --name-status` and `git diff -- SKILL.md` between them

Receipts: `.ufo/waves/round-55/w2/T55W2ScoutColdread-receipts/precheck.stdout`, `summary.json` (uncovered sections and reasons), `causal.json` (per-heading named vs causal inputs and shas), `inputs.json` (full per-entry input classification, including still-matching keys).

No tools installed. No lane production file edited. Scratch was `$HYAKU_SCRATCH/tameshi-r55/T55W2ScoutColdread` with an EXIT trap on that directory only.

## Confidence

High on the two credited counts, the 18 headings, the section shas, and the named/causal input split: those are outputs of the frozen measure, the precheck, and `sectionize` over the two commits. High on the reader bind: it is the comparison in the HEAD binder plus the seat names in `spec-w2.json`. Not executed: the binder itself (it writes the lane ledger). Unknown: which PIN the L1 will pass, and whether `resolutions.json` will grow a `heading`/`n` item before the bind.
