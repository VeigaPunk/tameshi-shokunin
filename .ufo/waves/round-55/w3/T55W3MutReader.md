# T55W3MutReader — mutation probe: reader deliverables vs the round-55 binder

Seat: mutation-tester (calibration). Lane `tameshi-shokunin`, base `0a2010ac`, content
commit **C0 `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`**. No lane production file, frozen
file or wave spec was touched: every run happened in `git clone --shared` copies inside
`/fast/scratch/hyaku/tameshi-r55/T55W3MutReader/`.

## Target and method

| item | value |
|---|---|
| mutated subject | reader deliverables under `<clone>/.ufo/waves/round-55/w3/*.json` |
| detector | `.ufo/evidence/round-55/integrate/binder.py` @ `4f7a704` (sha256 `cbe49ffab60a381d00596de51f83d6136d8db250501a74db9722dcfa77f51423`) |
| detector bytes | never edited — the mutation is entirely in the reader JSON |
| binder argv | `python3 <clone>/.ufo/evidence/round-55/integrate/binder.py <clone> 9cf0146b… 4f7a704… <clone>/.ufo/evidence/round-21/coldread/rekey-r55-mut` |
| PIN | `4f7a7040a57e7aed17db941be9c27b300aafb783` (HEAD/F5, carries the round's record edits) |
| clone | `git clone -q --shared <lane> <scratch>/lane`; `git -C <clone> rev-parse --show-toplevel` = the clone; detached at PIN |
| headings | the 18 of `.ufo/evidence/round-55/c1/lost-headings-at-c0.json` |
| section shas | frozen round-18 `sectionize`, module extracted at C0 (`git show 9cf0146b:.ufo/evidence/round-18/measure.py`), on `git show 9cf0146b:SKILL.md` → 64 sections, `skill_sha256=e0ce89f7866062062f4987358e353c8626c18f56d2eb1589225af99f44d695a6`, 0 of 18 headings missing (`0-headings-at-c0.json`) |
| restoration | before every arm: `git -C <clone> checkout -- .ufo/evidence/round-21/coldread/ledger.json`; verified back at `24dbe99a5788…` = the blob at PIN after the last arm (`Z-restoration-evidence.txt`) |

Detector power is established first: **A1b baseline** (18 genuine readers, H2 carrying its
two adjudicated findings) → `REFRESH rekeyed=18 skipped=0 headings=18`, exit 0, 609 ledger
entries (`A1b-baseline-2findings.stdout`). Every arm below changes exactly one reader
field relative to that baseline.

### Arm 0 — the binder cannot run against the round's own `resolutions.json`

```
$ git -C <clone> checkout -- .ufo/evidence/round-55/integrate/resolutions.json
$ <binder> <clone> 9cf0146b 4f7a704 <clone>/…/rekey-r55-mut
Traceback (most recent call last):
  File ".../integrate/binder.py", line 54, in <module>
    RES[item['heading']] = int(item['n'])
KeyError: 'n'
```

The committed `integrate/resolutions.json` (`ef6baf5b…`) is an **id-keyed adjudication log**
(`{"id","from","finding","decision","evidence"}`, 21 entries); `binder.py:54` wants
`{"heading","n"}` at module import, so the driver dies before any heading is examined.
Receipts `A0-committed-res.stderr`. The arms below therefore substitute the schema the
binder documents — the **one adaptation**: `[{"heading": "## Effective expectation
reconciliation — round 14", "n": 2}]` (`A1-adapted-res.json`, driven by `run.py`), keeping
the `.md` required next to each reader. **This is an integration blocker, not an artefact of
my probe: whichever seat runs the committed binder next gets a traceback.**

## The three required verdicts

| arm | corruption (one field of one reader) | expected | observed | verdict |
|---|---|---|---|---|
| A2 | `section_sha256` → `"0"*64` | refuse | `SKIP ## Context gate classification … — r no-clean-reader`, `REFRESH rekeyed=17 skipped=1`, exit 1, **no entry at C0** for that heading (ledger 608 = 591+17) | **killed / REFUSED** |
| A3 | `cand` → base `0a2010ac…` | refuse | identical: `SKIP … no-clean-reader`, rekeyed=17, exit 1, no C0 entry | **killed / REFUSED** |
| A4 | `heading` → `"… — round 15 (misspelled)"` | refuse | identical: `SKIP … no-clean-reader`, rekeyed=17, exit 1, no C0 entry | **killed / REFUSED (silently orphaned file)** |

Receipts: `A2-wrong-sha.{json,stdout}`, `A3-wrong-cand.{json,stdout}`,
`A4-heading-spelled.{json,stdout}`. The gate that does the work is `binder.py:114`
(`cand` **and** `section_sha256` must equal the C0 value) and `binder.py:102`
(`readers` is keyed by the literal `heading` string, so a misspelt heading simply never
matches and the heading falls through to `no-clean-reader`). All three arms leave the
ledger's older entries intact — the section keeps only its pre-C0 `read_rev`s, i.e. the
refusal forfeits the round's credit exactly as intended.

Two calibration details worth carrying:

- The three distinct causes collapse into one diagnostic (`no-clean-reader`), and a
  misspelt heading produces **no line of its own** — the orphan file is never mentioned,
  only the heading it failed to serve.
- A9 (`A9-gapped-twin-blocks`): with a *clean* reader for the heading present, a second
  file whose `heading` matches but which carries 1 unadjudicated finding sorts first and
  `binder.py:118` `break`s — `SKIP … reader-has-findings:1>0`, `rekeyed=16 skipped=2`. A
  gapped peer vetoes the heading outright; there is no fall-through to the clean sibling.
  Conservative (never launders), but it means one seat's finding denies a peer's credit.

## The findings arm — the rule holds only in one direction

The rule as coded is a **ceiling**: `allowed = RES.get(h, 0)` (`binder.py:111`) and
`if len(findings) > allowed` (`binder.py:118`). Controls that exercise the ceiling:

| arm | reader | observed |
|---|---|---|
| A5 | H2 carries **3** findings, adjudicated `n=2` | `SKIP ## Effective expectation reconciliation — round 14 reader-has-findings:3>2`, rekeyed=17, exit 1 — **refused** |
| A8 | H2 carries its **2** findings, **no** `resolutions` entry (`allowed=0`) | `SKIP … reader-has-findings:2>0`, rekeyed=17, exit 1 — **refused** |

So unadjudicated findings never bind. Now the corruption the item asks for — the same
finding-bearing reader with its `findings` list **emptied**:

```
$ python3 run3.py        # rebuilds the pair, snapshots it, runs the binder
snapshot: ['T55W3FIX01.json', 'T55W3FIX01.md']
{ "heading": "## Effective expectation reconciliation — round 14",
  "cand": "9cf0146b94ddba12d454ebf7288ce6e5c5d535bb",
  "section_sha256": "6110606ea4a977c70f0fa67ef8bdc97b4a4d2e51e9e8c2a96e984c7886376cbe",
  "findings": [] }
$ <binder> …   →  REKEY ## Effective expectation reconciliation — round 14 … reader=T55W3FIX01
                  REFRESH rekeyed=18 skipped=0 headings=18        (exit 0)
   BOUND '## Effective expectation reconciliation — round 14'  verdict=gap-minor minor_gaps=0
```

The sibling `.md` in `A6b-fixtures/` still names **both** findings (`finding A …`,
`finding B …`) — the binder only tests `md.exists()` (`binder.py:122`) and never reads it.
Baseline vs laundered entry, same heading and reader, differing in one number:

| arm | ledger sha256 | H2 entry |
|---|---|---|
| A1b (2 findings, `n=2`) | `0d09056c4be7…` | `verdict=gap-minor`, `minor_gaps=2` |
| A6b (findings `[]`, `n=2`) | `f2459f79918a…` | `verdict=gap-minor`, `minor_gaps=0` |
| A7 (findings `[]`, **no** `n` at all) | `f2459f79918a…` | `verdict=gap-minor`, `minor_gaps=0` |

**Verdict: SURVIVED — a coverage finding.** A6b/A7 are byte-identical ledgers
(`f2459f79918a…`): once the list is emptied, the adjudication record is worth nothing —
with `n=2` and with no entry at all the binder writes the same entry, `minor_gaps` drops
2 → 0 (`binder.py:178` recomputes it from the reader's own list), and the exit code is 0,
so the run reports a fully green refresh. The binder trusts the deliverable to describe its
own gaps; the only independent record (`resolutions.json`) is consulted as a ceiling, never
as a floor or an equality. `findings` **absent** behaves the same as `[]`
(`(d.get('findings') or [])`, `binder.py:117`), so the mutation needs no key at all.
The ceiling-only check is also why A7 is the sharper case: there the round has no
adjudication record to contradict the clean claim, so the laundered credit is
indistinguishable from a genuine clean read.

What would kill it (stated, not applied — the contract is not mine to change): compare
`len(findings)` to `RES[h]` for equality when an adjudication exists, and refuse a heading
whose reader asserts zero findings while the section's resolutions row records any; or bind
the entry's `minor_gaps` from `RES[h]` rather than from the reader's list.

## Restoration and blast radius

```
$ sha256sum <lane>/.ufo/evidence/round-55/integrate/binder.py            → cbe49ffab60a… (unchanged)
$ sha256sum <lane>/.ufo/evidence/round-55/integrate/resolutions.json     → ef6baf5bc1c3… (unchanged)
$ sha256sum <lane>/.ufo/evidence/round-21/coldread/ledger.json           → 24dbe99a5788… (unchanged)
$ git -C <clone> status --porcelain -- .ufo/evidence/round-21/coldread/ledger.json   → (clean)
$ sha256sum <clone>/…/ledger.json  ==  git -C <clone> show HEAD:…/ledger.json | sha256sum  == 24dbe99a5788…
```

`Z-restoration-evidence.txt`. The clone's only differences from PIN are my fixture wave dir,
the rekey OUT dir and the substituted `resolutions.json`; the lane working tree was never
written. Lane writes: this report and `T55W3MutReader-receipts/` only.

## Commands run

```
python3 run.py    # A0 committed-res crash, A1 baseline, A2 wrong-sha, A3 wrong-cand,
                  # A4 misspelled heading, A5 3>2, A6 emptied
python3 run2.py   # A1b baseline (both headings captured), A6b emptied+md kept,
                  # A7 emptied+no resolution, A8 2>0 unadjudicated
python3 run3.py   # A6c same as A6b with the fixture pair snapshotted into receipts
python3 run4.py   # A9 clean reader present, gapped twin sorts first
bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi   # rc=0 (census.txt)
```

Artifacts opened: `.ufo/evidence/round-55/integrate/binder.py`, `integrate/resolutions.json`,
`.ufo/evidence/round-55/c1/lost-headings-at-c0.json`, `.ufo/evidence/round-55/freeze.json`,
`.ufo/evidence/round-18/measure.py` (at C0), `SKILL.md` (at C0),
`.ufo/evidence/round-21/coldread/ledger.json`, `.ufo/waves/round-55/spec-w3.json`,
`.ufo/waves/round-55/w3/T55W3R06.json` (shape of a real reader).

No tool was installed or upgraded (nothing was needed); no `pacman` transaction was attempted.
