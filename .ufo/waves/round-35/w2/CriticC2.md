# CriticC2 — round 35, wave 2

Scope: attack C2's six mismatch definitions, m1's historical cutoff, and rename-versus-reconciliation. Read-only dispatch pin: `7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`.

**Axes:** calibration (assessment versus evidence), with provenance and record-identity fidelity as discriminators. This is a critic's evidence report, not admission or a replacement judgment.

## Result

The recorded zero is not disproved as **the frozen counter's narrow arithmetic**. The repairs inspected are not renames. However, the contract's assurance that a mismatch necessarily follows a renamed record is false: an unreconciled contract can disappear from m4 solely by a byte-identical rename. The same defect exists for m6's capability label. Separately, **m4 is already zero while its landed reconciliation misattributes a round-33 tool re-pin to round 34**. Thus zero does not establish that the underlying self-assessment is accurate.

I found no evidence of intentional rigging. I found a frozen finite checklist with fail-open identity/presence checks and a mistaken historical cutoff rationale. Do not equate its zero with a complete calibration census.

## Method, commands, and byte identities

All repository inspection used read-only Git commands with an absolute `-C`. I did not clone/check out: the assignment's proposed setup would violate the higher-priority prohibition on mutating Git commands / writing a checkout's `.git`. Scratch is exclusively `/fast/scratch/hyaku/tameshi-r35-w2/CriticC2/`; this report is the only fleet/lane write. No agents, judge, orchestration runtime, installs, or canonical C1/C2 measurement commands were invoked.

Executed commands:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 -B /fast/scratch/hyaku/tameshi-r35-w2/CriticC2/probe-c2.py
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 -B /fast/scratch/hyaku/tameshi-r35-w2/CriticC2/probe-history.py
```

Both probe processes exited **0**. The first executes the **unchanged frozen counter's `main()`** against pinned real blobs through explicitly virtual reader interfaces: history is pinned, fleet status/files are controlled, and each named case changes only its listed reader results. These are in-memory counterexamples, **not commits, not a live-fleet census, and not a new deciding C2 receipt**. The second independently inspects actual history; it never invokes the counter. Every Git argv, exit code, and output SHA is retained in the JSON receipts. Both scripts scrub all inherited `GIT_*` for their real Git reads.

| Absolute artifact | SHA-256 |
|---|---|
| `/fast/scratch/hyaku/tameshi-r35-w2/CriticC2/probe-c2.py` | `19576f1adbd74c06b4d36cffd78bc828b88ebe5e22a55dd1ea6efc7f5f7649e8` |
| `/fast/scratch/hyaku/tameshi-r35-w2/CriticC2/receipts.json` | `fa5a974c89094d2f83ac0395598aab7b8290cd82736f9659d94dc04dc1f9aace` |
| `/fast/scratch/hyaku/tameshi-r35-w2/CriticC2/probe-history.py` | `bf55590f177276fd1225674c67c461f7a01840f37b12941cfd9b22456daf6bd6` |
| `/fast/scratch/hyaku/tameshi-r35-w2/CriticC2/history-receipts.json` | `3b40238058b1d7b6e5cfc1e97433f3582fa75627f3b3e5f323c127fd15603aa9` |

Key committed input bytes at the dispatch pin (all extracted by `git show`, exit 0; complete manifest in `receipts.json`):

| Artifact within `/home/vgpnk/Projects/shokunin/tameshi-shokunin/` | SHA-256 |
|---|---|
| `.ufo/evidence/round-35/c2/c2-measure.py` | `67bb71188cde259088646f960b6fda8e0a217fad5d8260e379054b381018f9cc` |
| `.ufo/evidence/round-35/contract.json` | `a9eb2b97226ad192352f9da8cc32f3f719db22a93f14355a5e2d1306cea027c0` |
| `.ufo/evidence/round-33/contract.json` | `bf8f477ce08da608f9fc68a31d14380dae673ae230c091c964b4d0cccfec9b40` |
| `.ufo/evidence/round-35/pin-reconciliation.json` | `9ff9f9c5a6d5a771e11021c29f275ec92885480c9f813e587380872c9733a662` |
| `.ufo/evidence/round-34/dev/authoring.stdout` | `ea1521327b46cb09b02e72ff190b586c80690513df4400170e477c9882a46669` |
| `.ufo/evidence/round-34/dev/authoring-receipts.json` | `5bec3e7927b6fd315d8a3214ce54e85afe96020a399ca2c584ade7c9cc6db798` |
| `SCORECARD.md` | `cbea24c85074baac8904cab3b2937c6e93634431c9ee408b711fc58e66e7961f` |
| `corpus/README.md` | `7c0fe513ac1999d1c489d0c0e6b0aa57c648c8b2855d0e4a28fd617dcbc2619f` |
| `corpus/SOURCES.md` | `f85c02e76b0994477df7ded8d95585d260885f2d93fbeb91e57deb358d7855fe` |

## Ranked findings

### CRITICAL-1 — the frozen anti-rename assurance is false; this is fail-open

The claim under attack is the sentence in `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/contract.json:55-58`: a rename rather than reconciliation is a falsifier, with the explanation that committed-byte reading makes the mismatch move with the record and remain counted.

Counterexample, using the unchanged counter and actual pinned contract/tool bytes:

1. Remove the virtual reconciliation record. Case `m4-unreconciled-pinned-contract` reports `m4=1 total=1 C2_R35_PASS=false`, counter exit **1**.
2. Keep that record absent, and move the contract's identical `bf8f477c…ec9b40` bytes from the logical Git path `.ufo/evidence/round-33/contract.json` to `.ufo/evidence/round-33/contract-renamed.json`. Case `m4-byte-identical-contract-rename-no-reconciliation` reports **`m4=0 total=0 C2_R35_PASS=true`, counter exit 0**.
3. The old pin is still `9dbbce62aeaeecbacfa1b82e15b61afcb4580e3920a0b827ae038fa4c06f33a4`; the actual tool is still `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10`. No disagreement was reconciled.

Why: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/c2/c2-measure.py:106-127` reads exactly one fixed contract path and skips the class when it is absent. Reading committed bytes does not establish record identity.

Independent second witness: `m6-wrong-999-row-assessment` reports `m6=1` / exit **1** for a standing assertion of 999 rows against 99 actual rows. Changing only the capability label from `sources-registry` to `sources-registry-renamed` in the matching rows yields `m6-capability-label-renamed-999-still-wrong`: **all six zero / exit 0**, with the 999-row assertion untouched. The selector at counter lines 145-151 sees no row and does not count a missing authority.

Evidence: named cases in `/fast/scratch/hyaku/tameshi-r35-w2/CriticC2/receipts.json`; their input and stdout hashes are recorded there. The m4 rename PASS stdout SHA is `611277c8e7153ee36733dd9dd108b3ec7ba1654e152f798d655397c4802302ba`; its unreconciled control stdout SHA is `7a0082e6b464d84bba64a22a3897e4085d02f59dc80b08f7e797cc7c7c0df9ac`.

**Impact:** calibration / identity fidelity. This falsifies the apparatus explanation, **not** the existing zero receipt, and is not evidence that the landed repairs used this trick. The external rename falsifier remains meaningful; the counter does not enforce it.

**Smallest safe correction:** preserve frozen bytes and append this limitation. In a separately frozen successor, require the declared records/capability identities to exist; treat disappearance as a mismatch unless an explicit lineage-preserving migration reconciles it. A successful zero after dropping an authority is not a harmless tradeoff to silently credit.

### BOUND-1 — m1's historical rationale names the wrong commit and overcounts the before-state

Counter lines 35-38 and contract A1 call `284ab0f0…` the baseline where criterion 10 landed. Actual commands, each exit **0**:

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 284ab0f0b8b989ee73d9c00c0c0df0a59757af8d:corpus/QUALITY.md
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log --format='%H %s' -G '^10\. A new' 7da6e076c2e25936a3b60dde2a4080d8f05b7e5b -- corpus/QUALITY.md
```

The first contains criteria **1-5 only**, SHA `1923c94f49788adef82375c72b96b5448b5f52ea4a9971bab6411ff1c2c2f95b`. The second identifies **`c7986cdf051cbe9d047f02f76f2e1da0b36a84e3`**, whose criterion-10-bearing QUALITY bytes hash to `deeaf258ed3e6c66a4331fef7f9c3f4bc582394435a5ab38d6f028cf10d18643`. The introduction patch explicitly adds criteria 6-10 on October 19; `284ab0f0` is the October 14 training closeout.

Moreover, ancestry includes equality: `closeout-r11.md` was first added **at `284ab0f0`**, so it is counted despite the counter comment saying entries AFTER that commit. Independent history analysis in `probe-history.py` found **8** missing keys at the frozen anchor versus **5** at the actual criterion-introduction anchor. The difference is exactly the historical closeout's three fields, not three newly nonconforming entries. The pinned counter currently scopes **22/40** entries, excluding 18; see the explicit scope list in `receipts.json`.

**Impact:** calibration's historical denominator/provenance. This direction is conservative/fail-closed: it imposed extra headers, not a means to turn a genuine missing-key defect into zero. It does not invalidate the repaired zero, but the explanation that every counted pre-repair item was a criterion-10 defect is too strong.

**Smallest safe correction:** append the true cutoff history and identify the three retroactive repairs separately. Do not rescope the frozen metric after its measurement. A successor can bind the scope to the actual criterion introduction, with the equality policy stated explicitly.

### HYGIENE-1 — a landed m4 reconciliation has false repin attribution while m4 is zero

This is an **actual record**, not a virtual mutation. `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/pin-reconciliation.json:3,10` says the recorded round re-pinned the tool and names:

```text
repinned_by: round-34 (measurement revision c17e593b51802dd4ed568da3265f21c6d00c4273)
```

Actual history commands (all exit **0**, complete argv/output hashes in `history-receipts.json`):

```sh
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin log -1 --format='%H %s' c17e593b51802dd4ed568da3265f21c6d00c4273 -- tools/tally-audit-v2.py
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show ee3984924c4d52703209f8b971717c975898f4ba:tools/tally-audit-v2.py
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show c17e593b51802dd4ed568da3265f21c6d00c4273:tools/tally-audit-v2.py
```

The last modification is **`ee3984924c4d52703209f8b971717c975898f4ba`, round-33 amendment 5**, explicitly “tool re-pinned; still no data run.” Both tool byte streams are identical, SHA `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10`. Round 34 measured that already-repinned tool; it did not perform that re-pin. The reconciliation's measured-revision bytes have the same `9ff9f9c5…3a662` hash quoted above.

The original receipt `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-35/after/c2-at-d16f9b5a.stdout` records `m4=0` (SHA `33530e9a630082996b305a79a0ec7fce2613770cb6e4084ce8d366c2b35f0b54`). Counter lines 121-124 check only contract/path/old digest/new digest, never attribution. **This names a class that is zero while its underlying self-assessment remains wrong.**

**Impact:** calibration / false provenance, not tool-byte integrity. **Smallest safe correction:** append an attribution erratum separating `repinned_at=ee398492… (round 33)` from `measured_at=c17e593b… (round 34)`; preserve the old entry and counter. The digest reconciliation itself is real.

### HYGIENE-2 — the remaining zeros are deliberately weaker than semantic reconciliation

All cases below executed frozen `main()` and are recorded in `receipts.json`; every counter exit is explicit:

| Class / exact implementation | Failing control | Zero despite an unresolved underlying defect | Landed-state distinction |
|---|---|---|---|
| m1: three anchored key prefixes before first `## `; counter 66-83 | `m1-three-missing-header-keys`: m1=3, exit 1 | `m1-empty-values-no-provenance`: empty `source:`, `verified-at:`, `recheck:` all count as present; all zero, exit 0 | The actual three repaired headers contain substantive values; no allegation that they used empty placeholders. |
| m2: basename substring anywhere in README; counter 84-86, **inside m1's scope/continue** | `m2-no-index-or-mention`: m2=1, exit 1 | `m2-comment-only-not-a-row`: only an HTML comment carries the name; zero, exit 0. `m2-legacy-entry-missing-index`: a prebaseline note loses its index mention and still counts zero. | All 40 actual entries currently have the searched substring; the three new repairs are actual table rows. A1 names an m1 scoping amendment, but the shared loop also scopes m2. |
| m3: live fleet porcelain `??`, under waves, excluding hyaku, readable body contains `tameshi`; counter 88-104 | `m3-untracked-tameshi-seat`: original landed seat bytes at the original virtual fleet path give m3=1, exit 1 | `m3-same-bytes-in-excluded-hyaku`: relocating identical bytes to the excluded fleet hyaku namespace yields zero, exit 0 | This is an explicit namespace boundary, not proof of a complete misroot sweep or a claim that actual copying was fake. |
| m4: one fixed contract, exact old/new digest tuple in a separate record; counter 106-127 | Unreconciled control m4=1, exit 1 | Byte-identical record rename gives zero; actual wrong attribution is also unchecked. | The landed exact digest tuple does reconcile the byte disagreement; see CRITICAL-1 and HYGIENE-1. |
| m5: stdout has a false SEALED line, JSON all true, no anchored adjudication marker; counter 128-139 | `m5-actual-stale-generation-no-adjudication`: m5=1, exit 1 | `m5-marker-only-without-explanation`: append only `# ROUND-35 ADJUDICATION`; zero, exit 0 | The actual appended block is nine substantive lines distinguishing first and corrected generations, not a marker-only repair. |
| m6: last exact `sources-registry` row, first `N rows` token, lexical S-row count; counter 141-151 | 999 versus 99 gives m6=1, exit 1 | Renamed capability retains 999 but produces zero, exit 0. Missing row is not a mismatch. | The actual row keeps its identity and explicitly states 99 plus a re-derivable command. |

**Impact:** calibration. These are fail-open semantic limits, not BOUND/fail-closed findings. Presence, mention, and a waiver marker are not proof of accurate provenance, a coverage-map row, or a justified adjudication. Their existence alone does not make the finite metric dishonest; presenting its zero as those stronger properties would.

**Smallest safe correction:** disclose the exact predicates now. In any successor, keep m2 outside m1's legacy exemption, require an actual index row, and bind adjudication/reconciliation to the named evidence rather than marker presence. Do not silently replace the frozen definitions in this round.

## What I could not break, and what remains unproved

- **No demonstrated rename-as-repair in the landed changes.** The read-only repair diff command recorded in `/fast/scratch/hyaku/tameshi-r35-w2/CriticC2/receipts.json` exited 0 and reports eight paths: six modifications (authoring stdout, SCORECARD, README, three knowledge notes) and two additions (reconciliation, lane seat report). **No R status.** More directly, the patch adds real header values and three index rows, appends the generation explanation, and keeps the `sources-registry` identity while changing its count. The m4 attribution error is a separate defect, not a rename.
- **Each class can actually fail.** The six controls above return respectively m1=3, m2=1, m3=1, m4=1, m5=1, m6=1, each exit 1; no class was merely hardcoded zero. The clean pinned-blob / empty-fleet fixture returns all zero, exit 0. It is not a claim about the live fleet.
- **The misroot report landed with durable bytes.** `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-34/w1/ReviewDevReceipts.md` hashes to `ff532da39c28846c3d0ff832340312cdb97a457e68843ddc8e8642898267b3c2`, matching the round-35 lesson's recorded short digest. The deleted fleet source is not retained in this review, so I cannot independently re-prove the historical `cmp` or deletion provenance from that hash alone.
- **Counter pin stands.** The pinned committed source is exactly `67bb7118…18f9cc`, as required, and no frozen bytes were changed. The inherited after receipt genuinely contains the narrow all-zero assertion. I did not rerun the consumed deciding measurement or certify C2 at the wave's eventual head; that recount belongs to L1 after records land.
- C1 root/sealed amendments were read as required background but were not exercised in this C2-only seat. No C1 verdict is implied.

The safe retained claim is the literal six-predicate zero with these identity/semantic limits named. The stronger “rename cannot hide a mismatch” claim is broken; comprehensive calibration or correct reconciliation provenance cannot be inferred from this tally alone.
