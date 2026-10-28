# T55W3SentReaders — reader deliverable integrity (round 55, wave 3)

Seat: T55W3SentReaders (sentinel, axis calibration, milestone *reader deliverable integrity*).
Attacked surface: the 18 re-key reader deliverables this wave writes, their sha/cand/heading
agreement with the frozen round-18 sectionizer at C0, and the consumer that turns them into
ledger credit (`.ufo/evidence/round-55/integrate/binder.py`).

C0 `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`; lane HEAD at audit time `4f7a704` (F5 amendment 9).
Nothing in the lane was written outside `.ufo/waves/round-55/w2/T55W3SentReaders-receipts/` and this
report; every git mutation ran in `git clone --shared` copies under
`/fast/scratch/hyaku/tameshi-r55/T55W3SentReaders` (removed by the driver's `trap`).

## 1. What I recomputed, and how

* Section bytes: `git -C LANE cat-file blob C0:SKILL.md` (never the working tree).
* Cuts and shas: the frozen round-18 sectionizer `.ufo/evidence/round-18/measure.py`, `sectionize()`,
  imported — no home-grown hashing. The copy at C0 and the copy in the lane are the same blob
  (`sha256 7ca87a7c…dd37`), so the recompute is rev-pinned.
* Reader deliverables: read from **both** `.ufo/waves/round-55/w2/` and `w3/` — the reader discipline
  in the wave context names `w2/<seat>.json`, the binder globs both, and only 3 of the landed JSONs
  are in `w3/` (see F3).
* Every command and output: `.ufo/waves/round-55/w2/T55W3SentReaders-receipts/run-receipts.sh`
  (re-runnable, arms 01–10) and its `run.log`.

## 2. The 18 headings at C0 — independent recompute

| # | heading | sectionizer cut | sha256 at C0 | seat | json dir | findings |
|---|---|---|---|---|---|---|
| 1 | `## Context gate classification and explicit exit classes — round 15` | 1639–1705 | `132cfb9ef1aa07111af42389e4fe862152e3118b3a8bb66f1d84a6a332e7edf6` | T55W3R01 | w2 | 0 |
| 2 | `## Effective expectation reconciliation — round 14` | 1593–1626 | `6110606ea4a977c70f0fa67ef8bdc97b4a4d2e51e9e8c2a96e984c7886376cbe` | T55W3R02 | w2 | 0 |
| 3 | `## Live-tree re-pin and entry-command monitor — round 17` | 1844–1875 | `6395900104ed76b6f9dbfae1bb33384197982447e1db7dbaf89bf2b6b1b9beac` | T55W3R03 | w2 | 1 |
| 4 | `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` | 146–260 | `77d88c0226463dfc97f0074a5cafedc1044be0a2a16c85fbb6237ac06a5140da` | T55W3R04 | w2 | 2 |
| 5 | `## Pin disposition and provenance correction — round 13` | 1546–1576 | `1fa3130bc6d4bc46124a1c0e234583657bb6c7623256dfa85f4db2a7fb91da31` | T55W3R05 | w2 | 0 |
| 6 | `## Repeated controls and gate registry — round 12` | 1508–1527 | `3a78cbfcef65ada68c09342e5cbc71dc067d2b5258c3afbff6ea94e37a82b831` | T55W3R06 | w3 | 1 |
| 7 | `## Standing rules` | 17–44 | `acfb671afd767c32476f57b040399972f6c870cd7dde3d821c344cae1a9ad767` | T55W3R07 | w2 **and** w3 (identical) | 2 |
| 8 | `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` | 936–949 | `430dd86f25b6ce3d5ed51012d54de7cdad7213c6353eb7701323de762b9fb993` | T55W3R08 | w2 | 3 |
| 9 | `## The operator's runbook and the six-leg regression (round 10, measured)` | 1299–1307 | `636e850f885cb39904d100f67446e1039aa48c6510c2a66ea6e6d5aaa089faf7` | T55W3R09 | — | pending |
| 10 | `### Gate/probe registry` | 1528–1545 | `99285e24a71a8d2a0ea3fd6bcafe7e080acb23bfd653e7cbb3b71dfdc5144c77` | T55W3R10 | w2 | 2 |
| 11 | `### Round-13 gate/probe registry` | 1577–1592 | `896722c4941841f228810678befe82e9910cc66eb67c3de45d7561ce4668566d` | T55W3R11 | w3 | 1 |
| 12 | `### Round-15 gate/probe registry` | 1706–1736 | `78edbb693cdddcab61902811985918087529c444d3fb01da7bcaf4a674daf4ea` | T55W3R12 | w2 | 1 |
| 13 | `### Round-17 gate/probe registry — re-pin and monitor` | 1876–1884 | `309f83283e7518eb00cf7ce4296daf4bf5e80843ff2b3046755eb55d3ba8fb8c` | T55W3R13 | w3 | 0 |
| 14 | `### Round-18 gate/probe registry — routed-defect closure` | 1955–1967 | `661f63518af62b198f68ec5400778d9662df725d84744ad428dacc08823e6d7e` | T55W3R14 | w2 | 0 |
| 15 | `### Round-21 gate/probe registry — finite environment differential` | 1994–2133 | `eccd3ec82207fa69cee544f8f4ebfc0f9a473fe7254b8041ae2f5924f8d00a06` | T55W3R15 | — | pending |
| 16 | `### Round-26 gate/probe registry — report interop` | 2162–2201 | `cc23587b353fb780d4310aebc7277e4030729ae767850e2e826d2ff151bdea52` | T55W3R16 | — | pending |
| 17 | `### The service's limits — what tameshi refuses to mutation-test` | 1269–1298 | `7e240e714c6e6fa75a01061ef171238401b3a91fdd69cc86c13f97b151b848f6` | T55W3R17 | w2 | 4 |
| 18 | `### Triggers T1–T3 and the re-pin rule` | 1087–1109 | `2350210704efcc3becfbcd40a63775ad591910039744ac6d072881b3deef7801` | T55W3R18 | w3 | 2 |

*The three `pending` rows were still being written when this table was frozen; §6 re-runs the audit
against the live tree and is the authoritative final state.*

**Result for every landed deliverable: `heading` matches the seat's assignment exactly, `cand` is
`9cf0146b…`, and `section_sha256` equals the frozen sectionizer's value at C0. No mismatch, no
wrong-rev sha, no heading duplicated across seats (R07's dual copy is the same file in two dirs),
no malformed JSON, and every finding entry is `{quote, why}`.**

## 3. The 18-heading list is exactly the forfeited set (completeness check)

```
python3 .ufo/evidence/round-18/measure.py --repo LANE --rev 9cf0146b… --ledger-rev 9cf0146b…:.ufo/evidence/round-21/coldread/ledger.json
sections_covered=46/64 credited=46
uncovered=18 lost-headings-at-c0.json=18 set_equal=True
uncovered minus lost: []
lost minus uncovered: []
```

Receipt `08-credit-at-c0-46of64.txt`. The wave's 18 assignments are not a sample: they are the
whole set of sections the credit rule refuses at C0, and the spec's 18 headings are set-equal to
`lost-headings-at-c0.json` and to the counter's own `uncovered_headings`.

## 4. Findings

### F1 (high) — the re-key binder cannot run against the round's own adjudication file

`binder.py` builds its allowance table at import time:

```python
for item in json.loads(RES_PATH.read_text('utf-8')):
    RES[item['heading']] = int(item['n'])
```

Round 55's `.ufo/evidence/round-55/integrate/resolutions.json` carries **no `heading` and no `n`
key on any row**: 21 rows in the worktree, 11 rows at HEAD, all `{id, from, finding, decision,
evidence}`. The binder therefore dies before it reads a single reader report:

```
--- arm: resolutions.json as at worktree
  File ".../binder.py", line 54, in <module>
    RES[item['heading']] = int(item['n'])
KeyError: 'n'
exit=1
--- arm: resolutions.json as at HEAD
KeyError: 'n'
exit=1
```

Receipt `04-binder-crash.txt`. The mechanism's own precedent (`.ufo/evidence/round-54/integrate/
resolutions.json`) is 12 rows, 12 of them carrying `heading`+`n` — the round-55 file is a different
schema (per-finding adjudications keyed by `id`), so the binder's contract was not carried forward.
Impact: **the deciding re-key cannot execute at all**, so the floor cannot return to 64/64 from the
18 readers regardless of how good the deliverables are. Smallest remediation: either make the table
read tolerate mixed rows (`if 'heading' in item and 'n' in item`) and add per-heading allowance rows,
or emit a second section-level table the binder reads.

### F2 (high) — with a schema-compatible table, 10 of 15 landed readers are skip-fated

Substituting round-54's table (the only schema-compatible witness) and running the binder in a clone
at C0 over the live wave artifacts:

```
REFRESH rekeyed=8 skipped=10 headings=18
SKIP ## Repeated controls and gate registry — round 12 reader-has-findings:1>0
SKIP ## Standing rules reader-has-findings:2>1
SKIP ## The leg ledger — replay, receipt, and how it is read (rou reader-has-findings:3>1
SKIP ### Gate/probe registry reader-has-findings:2>0
SKIP ### Round-13 gate/probe registry reader-has-findings:1>0
SKIP ### The service's limits — what tameshi refuses to mutation- reader-has-findings:4>0
SKIP ### Triggers T1–T3 and the re-pin rule reader-has-findings:2>1
...
```

Receipt `05-binder-round54-schema.txt`. The wave context invites findings ("an empty list is a
legitimate, valuable verdict"), the binder treats `len(findings) > allowed` as a skip, and the
round's table grants no allowance to any heading. The 10 seats that found something (1–4 findings
each, 19 findings total) are exactly the ones the bind discards unless the L1 writes a
`{heading, n}` row for each. §5 gives the counts the table must carry.

### F3 (medium) — the audit item's stated path holds 3 of the landed JSONs

The item names `.ufo/waves/round-55/w3/T55W3R*.json`; the reader discipline names
`w2/<seat>.json`. Landed: 12 in `w2/`, 3 in `w3/`, 1 in both. The binder is safe (`WAVE_DIRS`
globs both), but any consumer — including this audit read literally — sees a third of the wave.
Receipt `02-deliverable-audit.json` (`path` column). The two instructions should name one directory.

### F4 (medium) — the reader discipline's cut rule contradicts the mandated hash for 7 of 18 sections

The wave context says "cut between that heading and the next heading of the same or higher level".
The frozen sectionizer cuts at **any** `#`/`##`/`###` heading. For the seven `##` sections that are
immediately followed by a `###` section, the two cuts differ and the sha differs:

| heading | sectionizer | context-rule cut | sha(sectionizer) | sha(context rule) |
|---|---|---|---|---|
| `## Context gate classification…` | 1639–1705 | 1639–1736 | `132cfb9e…` | `3cdd296c…` |
| `## Effective expectation reconciliation — round 14` | 1593–1626 | 1593–1638 | `6110606e…` | `41ca34d0…` |
| `## Live-tree re-pin…` | 1844–1875 | 1844–1884 | `63959001…` | `e0832b48…` |
| `## Pin disposition…` | 1546–1576 | 1546–1592 | `1fa3130b…` | `9e6a128d…` |
| `## Repeated controls and gate registry — round 12` | 1508–1527 | 1508–1545 | `3a78cbfc…` | `19a921cf…` |
| `## The leg ledger…` | 936–949 | 936–1026 | `430dd86f…` | `75f9c30c…` |
| `## The operator's runbook…` | 1299–1307 | 1299–1392 | `636e850f…` | `6ad6ea4b…` |

Receipt `10-cut-rule-divergence.txt`. **No landed reader recorded the context-rule cut** — every
JSON carries the sectionizer's sha, because the readers ran the tool rather than following the prose.
A reader that followed the prose literally would be rejected by the binder as `no-clean-reader`.
The same conflict surfaces in the prose of three reports: R01's report says the `### Round-15`
table "belongs to the section" (it is a separate section, 1706–1736, bound by R12), R02 describes
its read as 1593–1638 while recording 1593–1626, and R03 judged the following `###` block as well.

### F5 (medium) — one finding quotes bytes outside the section it is bound to

R03 (`## Live-tree re-pin and entry-command monitor — round 17`, sha `63959001…`, 1844–1875) quotes
`` | `tools/registry-check.py` | gate | `python3 tools/registry-check.py --rev REV …` ``. That row
does not occur in the bound section; it lives in `### Round-17 gate/probe registry — re-pin and
monitor` (1876–1884, sha `309f8328…`), which is R13's section. The seat discloses this in its md
("it was judged too … The recorded sha is the sectionizer's 1844–1875 cut only"), so the ledger
entry would carry a `gap-minor` finding whose quote a verifier cannot find in the bound bytes.
Receipt `03-quote-presence.txt` — 18 of 19 landed findings resolve inside their section; this is
the one that does not.

### F6 (low) — R07 writes the same deliverable to both directories and exceeds the four-key schema

`w2/T55W3R07.json` and `w3/T55W3R07.json` are byte-identical (`sha256 e30ec45b…`), and both carry
`bounds` and `sectionizer` in addition to `heading`/`cand`/`section_sha256`/`findings`. The binder
reads only the four keys and takes the first match in sorted order (w2), so this is harmless today;
it becomes a divergence hazard the moment one copy is edited.

### F7 (medium) — the binder binds untracked reports while its docstring promises committed ones

`binder.py` docstring: "find a **committed** reader report". The code globs the live worktree
(`glob.glob(str(Path(LANE, wd, '*.json')))`) with no `git ls-files` check. All 15 landed reader
JSONs are untracked (`git status --porcelain` → `??`). A ledger entry can therefore cite a reader
path that exists in no commit, which is exactly the provenance the ledger is supposed to carry.

## 5. What the adjudication table must carry (from the landed readers)

| heading | seat | findings | binder needs `n ≥` |
|---|---|---|---|
| `## Repeated controls and gate registry — round 12` | R06 | 1 | 1 |
| `## Standing rules` | R07 | 2 | 2 |
| `## The leg ledger — replay, receipt, and how it is read (round 7, measured)` | R08 | 3 | 3 |
| `## Live-tree re-pin and entry-command monitor — round 17` | R03 | 1 | 1 |
| `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence` | R04 | 2 | 2 |
| `### Gate/probe registry` | R10 | 2 | 2 |
| `### Round-13 gate/probe registry` | R11 | 1 | 1 |
| `### Round-15 gate/probe registry` | R12 | 1 | 1 |
| `### The service's limits — what tameshi refuses to mutation-test` | R17 | 4 | 4 |
| `### Triggers T1–T3 and the re-pin rule` | R18 | 2 | 2 |
| (clean, 0 findings: R01, R02, R05, R13, R14 — bind with `allowed=0`) | | 0 | 0 |

## 6. Did any reader read the working tree instead of C0?

Three independent tests, all negative:

1. **Byte identity forecloses the section-sha test.** `SKILL.md` is the same blob at C0, at HEAD
   and in the worktree (`sha256 e0ce89f7…95a6`, 64 sections, empty `git diff C0 HEAD -- SKILL.md`),
   so a worktree read cannot change the section sha; the discriminator has to be elsewhere.
2. **The one section that differs from base.** `## Standing rules` is `61736dce…` at base and
   `acfb671a…` at C0; R07 records `acfb671a…`, so it did not read the base blob. The other 17
   sections are byte-identical at base and C0.
3. **The four files that drifted after C0** (`tools/registry-check.py`, `tools/context-capture.py`,
   `tools/registry.json`, `corpus/knowledge/scratch-root-contract.md`) are cited only at line ranges
   outside the post-C0 hunks — `tools/registry-check.py:11-12`, `:757`, `tools/context-capture.py:113`,
   `:153` (hunks are at 1848-1860/1934-1955 and 2216-2226) — and no reader artifact contains the
   worktree-only phrases ("the token this tool actually prints", `REPEAT_CONTROL: setup_error`,
   "wave-2 F1/F2"). Receipt `06-worktree-read-sweep.txt` (grep exit 1, no match).

Every landed report also shows its own `git show`/`cat-file` of `SKILL.md` at C0
(`09-c0-read-evidence.txt`; four reports describe the read generically — `git show <C0>:<path>` or a
`checkout C0` clone — which is why that sweep is corroborating, not primary).

## 7. Receipts

`.ufo/waves/round-55/w2/T55W3SentReaders-receipts/`

| file | what it shows |
|---|---|
| `run-receipts.sh` | re-runnable driver, arms 01–08, clones under `$HYAKU_SCRATCH`, `trap` cleanup |
| `run.log` | one end-to-end run |
| `01-section-sha-recompute.txt` | the 18 cuts and shas from the frozen sectionizer at C0 |
| `02-deliverable-audit.json` | per-seat heading/cand/sha/findings verdict + duplicate detection |
| `03-quote-presence.txt` | each finding's quote resolved against its bound section |
| `04-binder-crash.txt` | `KeyError: 'n'` against the worktree file and against HEAD's |
| `05-binder-round54-schema.txt` | `REFRESH rekeyed=8 skipped=10` with the only schema-compatible table |
| `06-worktree-read-sweep.txt` | no worktree-only phrase in any reader artifact |
| `07-md-pairing.txt` | every reader JSON has its `.md` beside it (binder's `reader-md-missing` gate) |
| `08-credit-at-c0-46of64.txt` | 46/64 credited, 18 uncovered, set-equal to `lost-headings-at-c0.json` |
| `09-c0-read-evidence.txt` | per-report evidence of a git read of `SKILL.md` |
| `10-cut-rule-divergence.txt` | the 7 sections where the context cut rule and the sectionizer differ |
| `shas.py`, `audit.py`, `quotes.py`, `c0-sections.json` | the scripts and the recomputed table |

## 8. Verdict

The 18 reader deliverables themselves are sound: every landed one names its assigned heading, pins
`cand` to C0, and carries the frozen sectionizer's sha (0 mismatches in 15 recomputations). The
integrity failure is on the consuming side and in the instruction, not in the readers: the binder
crashes on the round's own adjudication file (F1), the allowance table grants nothing to the 10
seats that found something (F2), the discipline's cut rule would have produced the wrong sha for 7
of the 18 had the readers followed it instead of the tool (F4), and the binder will bind reports
that no commit contains (F7). One finding is bound to bytes its section does not contain (F5).
