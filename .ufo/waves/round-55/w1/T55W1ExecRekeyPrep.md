# T55W1ExecRekeyPrep — re-key prep: the SKILL.md edit drifts exactly one cold-read section

Seat **T55W1ExecRekeyPrep** (leaf, reported to L1 `TameshiR55`). Lane
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`; frozen base
`631cd6455e58dce969310b4c0466c3383d9f5108`; contract base
`0a2010acd1e92e4e332774050825e21bcfc7e079`.

Item: apply **only** the `## Standing rules` edit C2 needs, in a scratch clone at
the frozen base, and measure the cold-read floor before/after with
`.ufo/evidence/round-21/coldread/measure.py` plus the round-48 precheck.

Machine-readable companion: `.ufo/waves/round-55/w1/T55W1Er10.json` (the name the
item gives) and an identical copy at
`.ufo/waves/round-55/w1/T55W1ExecRekeyPrep.json` (the deliverable-discipline
name). Receipts: `.ufo/waves/round-55/w1/T55W1ExecRekeyPrep-receipts/`
(`derivation.out` holds every command and its output quoted below).

I edited **no** lane production file. The edit was applied with `git apply` in a
scratch clone under `/fast/scratch/hyaku/tameshi-r55/T55W1ExecRekeyPrep/`,
`git -C <clone> rev-parse --show-toplevel` was asserted equal to the clone before
every commit, and no mutating git command ran against the lane. Writes in the
lane are this report, the two JSONs and the receipts dir. **No tool was
installed** this wave (git, python3 stdlib, jq, diff were already present); no
pacman/uv/npx/cargo invocation ran.

## 1. Answer

**Exactly one section loses credit: `## Standing rules`. Nothing else.** The
other 63 sections keep their sha256 and stay credited, no heading is gained, and
`sections_total` stays 64.

| revision | `sections_covered` | `calibration_restraint_score` | `box3_full_page` | precheck |
|---|---|---|---|---|
| `0a2010ac…` (contract base) | 64/64 | 8 | true | — |
| `631cd64…` (frozen base) | 64/64 | 8 | true | — |
| edited clone `64e76a75…` (SKILL.md only, +6/−3) | **63/64** | **6** | false | **exit 1, `LOST ## Standing rules`, RED** |
| re-key demo `0005a9d7…` | 64/64 | 8 | true | exit 0, `lost=0 ok` |

The lost section, at the edited revision, computed with the **round-18
`sectionize`** (`.ufo/evidence/round-18/measure.py`, imported from the clone at
the frozen base, run over `git show <REV>:SKILL.md`):

```
heading  ## Standing rules
start    17
end      43
sha256   4f959fd727cdb630d2507de403b2cb20ae5c14ccc170c527a0d708f997e08b9b
whole-file skill_sha256  a157f37d8915d460c0694b5eb660db48f37d9c3ce99e9d13917e74f01ec55545
```

For contrast, the same section at base: `start 17`, `end 40`, sha256
`61736dcebc2d3d148255f9b3edd0ceb1c7cf2284f2969475b8da838ded9a78fc`, whole-file
sha256 `b5ff9727485da844a0c93d8f5914f957eba03d2c37cda59e8e38fd7a04ada195`.

Credit fails with reason `no-ledger-entry` — the section's bytes changed, so no
ledger entry carries the new sha256. That is the whole failure; no input drift,
no trace failure, no veto.

**The edit text is the L1's own.** The exactly-applied patch
(`receipts/edit.patch`) reproduces the lane worktree's `SKILL.md`
byte-for-byte (`diff -q` → identical; both files hash to
`a157f37d8915d4…`), and sectionizing the lane worktree file directly returns the
same `start 17 / end 43 / sha256 4f959fd7…`. So the hash in the JSON binds to
whatever commit the L1 lands, without re-measurement, as long as `SKILL.md` is
not touched again.

## 2. Derivation (executed, quoted from `receipts/derivation.out`)

```
## command: python3 <clone>/.ufo/evidence/round-21/coldread/measure.py --repo <clone> --rev <REV>
floor rev=0a2010acd1e9 covered=64/64 restraint=8 box3=True reasons={'credited': 64}
base  rev=631cd6455e58 covered=64/64 restraint=8 box3=True reasons={'credited': 64}
cand  rev=64e76a753862 covered=63/64 restraint=6 box3=False reasons={'credited': 63, 'no-ledger-entry': 1}
rekey rev=0005a9d79deb covered=64/64 restraint=8 box3=True reasons={'credited': 64}
lost_headings=['## Standing rules'] gained_headings=[]
lost_record={"start": 17, "end": 43, "heading": "## Standing rules", "reason": "no-ledger-entry", "reasons": ["no-ledger-entry"]}

## command: bash <clone>/.ufo/evidence/round-48/quality/coldread-precheck.sh <clone> 0a2010acd1e9… <REV>
--- at edited cand (exit 1):
LOST ## Standing rules | drifted=
COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=64e76a753862 cand_credited=63 lost=1 RED
--- at rekey demo (exit 0):
COLDREAD_PRECHECK floor=0a2010acd1e9 floor_credited=64 cand=0005a9d79deb cand_credited=64 lost=0 ok
```

`drifted=` is empty in the `LOST` line: this is a section-bytes loss, not an
input-drift loss. The precheck names the same single heading the measure does,
by two independent code paths.

Section arithmetic (`receipts/sectionize.txt`):

```
sections base 64 cand 64
changed_sections 1
 CHANGED heading='## Standing rules' base=17..40 sha=61736dce… -> cand=17..43 sha=4f959fd7…
shifted_sections 61 deltas [3]
sections_with_unchanged_sha 63
```

The 61 later sections shift `start`/`end` by +3 because the edit adds three
lines. **That shift costs no credit** — the round-18 algorithm matches ledger
entries by section `sha256`, not by `start` (verified: all 63 unchanged-shas
still credit at the edited revision). The 3 unshifted sections are the preamble,
`# tameshi-shokunin`, and `## Standing rules` itself.

Pristine ledger entry that has to be re-keyed (`receipts/ledger-entry-574-at-base.txt`,
read from the base blob, not the edited clone):

```
index 574 of 591   schema tameshi-coldread-ledger-v2
heading '## Standing rules'  start 17  end 40
sha256 61736dcebc2d3d148255f9b3edd0ceb1c7cf2284f2969475b8da838ded9a78fc
skill_sha256 b5ff9727485da844a0c93d8f5914f957eba03d2c37cda59e8e38fd7a04ada195
class instruction  verdict gap-minor  blocking_gaps 0  wrong_expectations 0  minor_gaps 1
commands_executed_count 2498   read_rev 99c3bc88d704566197783f66b211ee0a830e0330
inputs_count 2497  external_inputs_count 2497  traces_count 1
traces ['.ufo/evidence/round-21/coldread/rekey-r54-99c3bc88d704/traces/section-07.json']
reports ['.ufo/waves/round-54/w2/T54W2Read01.json', '.ufo/waves/round-54/w2/T54W2Read01.md']
drop_keys_present []      # LOG.md / SCORECARD.md / SKILL.md / ledger.json already absent
```

## 3. Why it matters: two frozen gates read this number

Both are frozen, so a miss here is not a bookkeeping nicety — it stops the round.

- `.ufo/evidence/round-55/no-harm.sh:16-17` requires
  `calibration_restraint_score >= 8 and sections_covered >= 64`. Without the
  re-key the edited tree prints `score=6 credited=63` → **`NOHARM coldread-floor
  … RED`**, and `deciding-run.sh` greps for `RED` and requires all 15 monitors
  `ok`. The monitor's own header comment pre-registers the obligation: *"The one
  calibration-critical monitor (the cold-read floor) is monitored at 64/64,
  which is the re-key obligation this round carries for the one SKILL.md section
  its edit drifts."* My measurement is the independent confirmation that the set
  is **one** section and not more.
- `.ufo/evidence/round-55/deciding-run.sh:70-71` requires the round-48 precheck
  exit 0 at `REV`; it is exit 1 RED on the un-re-keyed tree and exit 0 after the
  bind.

## 4. Binder handoff

Precedent: `.ufo/evidence/round-54/integrate/binder.py` (`binder.py LANE C0 PIN
OUTDIR`). The round-55 equivalent needs:

1. **C0** = any revision whose `SKILL.md` `## Standing rules` section sha256 is
   `4f959fd7…` (the section bytes are the content; the commit need not be the
   one I committed in scratch).
2. **A fresh reader report** at `.ufo/waves/round-55/w1/<seat>.json` beside its
   `.md`, carrying `heading: "## Standing rules"`, `cand: <C0>`,
   `section_sha256: "4f959fd7…"`, `findings: []` (non-empty findings are
   allowed only if the L1 adjudicates them; `minor_gaps` then counts them).
   I deliberately emitted **no** top-level `heading`/`cand`/`section_sha256`/
   `findings` in `T55W1Er10.json`, so a binder globbing `w1/*.json` cannot
   mistake my prep file for a reading.
3. **PIN** = the content-final revision; inputs recomputed as canonical blobs at
   PIN, dropping `LOG.md`, `SCORECARD.md`, `SKILL.md` and the ledger itself (the
   round-53 failure mode the round-54 binder encodes).
4. **The entry**: copy `.entries[574]` and retarget exactly five fields —
   `.sha256 = 4f959fd7…`, `.skill_sha256 = a157f37d…`, `.start = 17`,
   `.end = 43`, `.read_rev = <C0>` — then replace `verdict`, `blocking_gaps`,
   `wrong_expectations`, `minor_gaps`, `commands_executed_count`, `traces`,
   `seats`, `reports` with the fresh reader's own; keep `inputs`,
   `external_inputs`, `class`. `commands_executed_count = 1 + len(inputs)`.

A ready-to-use list for a binder that reads a `lost-headings` file is at
`receipts/lost-headings-at-c0.json` (`["## Standing rules"]`). Note
`.ufo/evidence/round-55/c1/measure.py` contains no `coldread`/`lost-headings`
code path — C1 counts record classes, not cold-read sections — so that list
cannot come from the C1 counter for this round.

**Mechanical demonstration (necessary *and* sufficient).** In the same scratch
clone I re-keyed entry 574 with exactly the five field changes above and
re-measured: `64/64`, score 8, `box3_full_page` true, precheck `lost=0 ok`.
Credit at that revision required all 2497 carried inputs to verify at C0, so the
input set survived this round's edits outside `SKILL.md`.

**Honesty boundary on the demo.** It carried the round-54 verdict metrics
(`gap-minor`, `minor_gaps 1`) and the round-54 trace. It is a key-mechanics
proof, **not** a fresh reading of the drifted section. The round's obligation is
*"a fresh reader at the content commit + a bound ledger entry"*; the binder must
bind the fresh reader's report and traces, not these carried values.

## 5. Risks, and one incident

- **Scratch sweep (observed).** My seat tree was deleted by an external process
  at 13:54 local, mid-run: the first precheck invocation died with `rc=2` and
  `cat: …/T55W1ExecRekeyPrep/precheck-rekey.out: No such file or directory`,
  while sibling trees under `/fast/scratch/hyaku/tameshi-r55/` all carried a
  13:54 mtime. I rebuilt the clone at the same frozen base and reproduced every
  number identically (base 64/64 score 8; edited 63/64 score 6; same section
  sha `4f959fd7…`), so no result here rests on the destroyed run. Two peers were
  executing scratch cleanup in that window (`T55W1Er07-2`, `MutK18K19`); a
  cleanup that globs the shared `tameshi-r55/` parent destroys other seats'
  in-flight clones and, worse, could do so between a counter run and its
  receipt. Reported, not fixed (outside my write surface).
- **Two JSON names.** The item names `T55W1Er10.json`; the discipline names
  `<seat>.json`. I wrote both, identical, and neither can be mistaken for a
  reader report (see §4.2).
- **Do not "fix" the 61 shifted `start`/`end` bookkeeping values** as part of
  the re-key. They cost no credit (measured), and rewriting 61 historical
  entries mid-round adds risk for no gain to any axis.
- **The section text is a live dependency.** Any further `SKILL.md` word in
  `## Standing rules` changes the sha and re-opens this. Since the section is
  cold-read re-keyed this round, the L1 should land the edit once and freeze the
  text.
- **Frozen-set state, observed and not touched.** At the frozen base the
  committed `contract.json` and `freeze.json` carry `amendments: []`, and the
  manifest is self-consistent there (`sha256` of all 6 listed files matches at
  `631cd64`). The lane **working tree**, read at 14:0x, is mid-amendment:
  `contract.json` lists 5 amendments and `freeze.json` 3, and three manifest
  hashes no longer match the working-tree bytes —

  ```
  WORKTREE_FREEZE_INTEGRITY: MISMATCH files=6 amendments=3
  FREEZE_MISMATCH .ufo/evidence/round-55/c1/measure.py 711507e7b5bd != 77abe1e9daf4
  FREEZE_MISMATCH .ufo/evidence/round-55/c2/measure.py d6ca1d851bb0 != ab3ae7514691
  FREEZE_MISMATCH .ufo/evidence/round-55/contract.json 5de4f37b14db != ed6871e17697
  ```

  That is a transient of in-flight edits, not a defect, **but** the deciding run
  refuses on it: `deciding-run.sh:20-41` re-derives every manifest hash from the
  bytes **at `FREEZE`** and exits 3 on mismatch, and `:66` requires
  `git diff --quiet "$FREEZE" "$REV" -- $FROZEN`. So the last amendment must
  regenerate `freeze.json`, that commit must be the `FREEZE` pointer, and no
  frozen path may be edited after it. I edited none of these; my measurements
  use only `round-21`, `round-18` and `round-48` scripts, so this state does not
  affect any number in §1–§2.

## 6. What the main agent must verify after integration

1. `python3 .ufo/evidence/round-21/coldread/measure.py --repo <lane> --rev <REV>`
   → `sections_covered=64`, `calibration_restraint_score=8`,
   `box3_full_page=true`.
2. `bash <lane>/.ufo/evidence/round-48/quality/coldread-precheck.sh <lane>
   0a2010acd1e92e4e332774050825e21bcfc7e079 <REV>` → exit 0, `lost=0 ok`.
3. `.ufo/evidence/round-55/no-harm.sh` → `NOHARM coldread-floor score=8
   credited=64 ok`, and all 15 monitors `ok`.
4. That the bound ledger entry's `sha256` is `4f959fd7…` and its reader report's
   `section_sha256` matches it at the L1's `C0`.

## 7. Receipts index

| file | what it holds |
|---|---|
| `derivation.out` | every command quoted in §2 with its output |
| `edit.patch`, `skill-edit.diff` | the applied patch and the resulting commit diff |
| `cand.rev`, `rekey.rev` | the two scratch revisions (`64e76a75…`, `0005a9d7…`) |
| `floor.json`, `base.json`, `cand.json`, `rekey.json` | full `measure.py` output at the four revisions |
| `sectionize.txt`, `sections.json` | round-18 sectionize at base and edited |
| `precheck-cand.out`, `precheck-rekey.out` | precheck stdout, RED then ok |
| `ledger-entry-574-at-base.txt` | pristine ledger entry read from the base blob |
| `rekeyed-entry.json` | the demo entry as bound |
| `lost-headings-at-c0.json` | `["## Standing rules"]` for a binder that reads a list |
| `frozen-set-state.out` | freeze-manifest integrity at the worktree and at `631cd64` (see §5) |
