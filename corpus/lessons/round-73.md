# tameshi round 73 — lesson

Round 73 (attempt 1), base `a3dd35742eee608d1205843dacebc461b4242b9e`
(`= origin/master`, clean tree — the round-72 non-author verifier spot-check
commit). Claims, counters, kill rules, arms and controls are frozen **before
any claim data** in `plans/round-73.plan.md` (declaration commit). Round
shape: one v1 wave, 13 seats (3 executor · 2 scribe · scout · 2 reviewer ·
critic · mutation-tester · sentinel · revenger · connector), policy band
8–16. `labrat` is a frozen-topology seat the validator rejects
(`~/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs:263`), so no labrat item
exists — the round-72 defect this round pays was a plan that declared one
anyway.

## Declared claims (frozen pre-data)

- **R73-C1 — calibration (the lowest scored numeric axis at 8; capability
  acquisition; sourced on the re-opened S066).** `tools/wave-reconcile.py` +
  `tools/wave-reconcile.json` (schema `tameshi-wave-reconcile-v1`): a round
  record's execution claims — seat count, committed seat-report count, role
  multiset, attack share — are re-derivable from the committed wave artifacts.
  Rows bind a record span by byte substring at the record revision with the
  printed integer a delimited token; artifacts are read from git objects at
  their own revision; `expect: meet|drift` so a standing red arm MEASURES the
  drift on every sweep; a UTF-8 BOM is a setup exit 2, never silently
  stripped. Standing manifest: six rows over the committed round-72 wave —
  four green and the round-72 closure's two routed defects as red arms.
- **R73-C2 — operability (verdict-only).** `tools/rekey-cost.py --arms`
  turns the recorded rekey-cost arm table into a re-runnable 7-arm battery
  and adds the ignored-path arm the round-72 wave's coverage finding named.
  Frozen outputs: `REKEY_ARMS: arms=7 meet=7 unexpected=0` exit 0, selftest
  unchanged 8/8, and the same battery under the IGNORED-filter mutant M3
  reads `unexpected=1` naming `ignored-skill`.

## Carry-in from the round-72 non-author closure

`corpus/lessons/round-72-verifier-spotcheck.md` (admitted; five status-neutral
routed defects, two carries). Dispositions declared pre-data in
`plans/round-73.plan.md`: defects 1 and 2 become C1's two measured red arms;
defect 3 is restated in this lesson's `## Gate`; defect 4 corrects the
pointer-recheck manifest's note count; defect 5 is paid in this round's LOG
entry (the three receipt-only commits of round 72 are named there as
inheriting the "Round 72 — appended after the wave" entry); carry 6 is C2;
carry 7 (inherited record misses) is re-measured at the tip and reported as
inherited.

## Gate — the source (S066 re-opened this round)

**Re-open, not a new row.** RFC 8259 is already held as S066 for a different
section (§6 number grammar). This round's instrument rests on §8.1's encoding
ground, so a new row on the same URL would be a within-scope duplicate
(CORPUS.md rule 2; the S289/S293 standing rejection, re-sampled by the
round-72 closure). The curation delta is therefore a **re-open**: S066's
`used-by` cell gains `corpus/lessons/round-73.md` and this Gate carries the
fresh located quotes.

- Source: RFC 8259, *The JavaScript Object Notation (JSON) Data Interchange
  Format* (T. Bray, Ed.), <https://www.rfc-editor.org/rfc/rfc8259>, text form
  <https://www.rfc-editor.org/rfc/rfc8259.txt>. Fetched 2026-11-04 (HTTP date
  `Wed, 04 Nov 2026 00:58:08 GMT`; 28,360 B; sha256
  `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7`;
  extract `.ufo/evidence/round-73/sources/rfc8259.txt`, headers
  `.ufo/evidence/round-73/sources/rfc8259-headers.txt`).
- Quote 1 (§8.1 Character Encoding, page lines 485–486, 18 words): "JSON
  text exchanged between systems that are not part of a closed ecosystem MUST
  be encoded using UTF-8" — the encoding of record for the artifacts the
  instrument parses.
- Quote 2 (§8.1, page lines 494–495, 17 words): "Implementations MUST NOT add
  a byte order mark (U+FEFF) to the beginning of a networked-transmitted JSON
  text."
- Quote 3 (§8.1, page lines 496–498, 21 words): "implementations that parse
  JSON texts MAY ignore the presence of a byte order mark rather than
  treating it as an error" — the RFC permits either; this lane chooses the
  fail-closed arm (a named setup exit 2) because silently stripping bytes the
  emitter was told not to add would let a rewritten artifact masquerade as
  clean (the round-72 EOL defect's class, made visible instead of invisible).
- **Admit:** S066's §8.1 re-open (the two normative sentences plus the
  permitted-alternative sentence above; the §6 number-grammar scope is
  unchanged and stays as written).
- **Reject (standing, re-sampled):** a new RFC 8259 row for the §8.1 ground —
  same URL, same document, within-scope duplicate; flip condition: the §6
  scope is retired or the document is superseded by a new RFC, at which point
  the successor is a new document with a new row.

## Gate — the census sentence (round-72 closure defect 3, restated)

The round-72 report's sentence "the counter-run without the prefix prints
E04" is true only of a **same-scope fixture**: on the real registry a
superseding row with a restated scope prints `W04 duplicate url … across
scopes` and the lane still validates clean. Measured this round on the live
registry (`scripts/sources-census.sh validate --root <fleet> tameshi`): the
S303 row prints W04, exit 0. The correction of record is this paragraph; the
round-72 report is append-only history and stands as written.

## What was measured — R73-C1 (calibration, capability)

**Before.** `git ls-tree -r a3dd3574 -- tools/ | grep -c 'wave-reconcile'` → 0;
`git grep -c WAVE_RECONCILE a3dd3574 -- tools/` → 0. No instrument compared a
round record's execution claims with the committed wave artifacts, and the
round-72 closure's two routed defects were prose.

**After** (receipts `.ufo/evidence/round-73/wave-selftest-r73.txt`,
`wave-reconcile-live-r73.txt`, `hardening-r73.txt`; measured commit
`fddbb667`, re-measured at `8f7ff279` and at the round tip):

```
$ python3 -I -X utf8 tools/wave-reconcile.py --selftest
WAVE_RECONCILE_SELFTEST: 12/12 pass                       exit 0
$ python3 -I -X utf8 tools/wave-reconcile.py --repo . \
    --extra-root fleet=/home/vgpnk/Projects/shokunin --manifest tools/wave-reconcile.json
WAVE_ROW r72-report-seats kind=seats expect=meet measured=meet ok | printed=12 seats=12 records=12
WAVE_ROW r72-report-seatreports kind=seat_reports expect=drift measured=drift ok | printed=11 files=12
WAVE_ROW r72-plan-seats kind=seats expect=meet measured=meet ok | printed=12 seats=12 records=12
WAVE_ROW r72-spec-roles kind=roles expect=meet measured=meet ok | declared=… measured=…
WAVE_ROW r72-plan-roles kind=roles expect=drift measured=drift ok | declared={… "labrat": 1 …} measured={… "revenger": 1 …}
WAVE_ROW r72-attack-share kind=attack_share expect=meet measured=meet ok | attack=3/12=25.0% floor=25.0%
WAVE_RECONCILE: rows=6 met=6 unexpected=0                 exit 0
```

Independent support from the wave: seat T73W1S01 rebuilt the rule from the
plan and the docstring alone and diffed all six rows — `ORACLE_CMP rows=6
equal=6` (its own offsets agree: 3618 for the report span, 179 and 7042 for
the plan spans); seat T73W1S02 drove the six setup cases from outside the
tool (all exit 2 with their named lines) and measured three mutants; seat
T73W1S03 audited the binding of all six rows at their pinned revisions and
found the report's `11 reports` matches no population (0/9/10/12/13/17/20/26
are the populations that exist); seat T73W1S08 re-derived every fact from
committed bytes without the instrument (`AGREE rows=6/6`); seat T73W1S09
re-ran the four frozen lines at five tips and upheld both claims.

**Adopted as work (seat findings, fixed in-round).**
- T73W1S03: the `record` block was **inert** on `roles` and `attack_share`
  rows (a forged span was a silent pass), `r72-spec-roles` carried a
  meaningless `printed: 12` outside its span, and a row-level `root: fleet`
  without `--extra-root` raised an uncaught `KeyError`. Fixed at `8f7ff279`:
  `_record_claim()` binds the record for every kind, the two roles rows drop
  `printed`, and an unknown root is `WAVE_RECONCILE error=setup:unknown-root:…`
  exit 2 (`hardening-r73.txt`, each case shown able to fail). The frozen
  counters are unchanged by the hardening (12/12 and 6/6).
- T73W1S02: the docstring claimed "Binding rules (each is a frozen selftest
  arm)" while the delimited-token rule and the span-substring rule carried no
  arm; the docstring is narrowed at `8f7ff279` and the arm is a named
  next-round carry.
- T73W1S04: the landed criterion 122 falsifier read mutable bytes and stopped
  failing after the round's own correction; re-pinned to the round-72 revision
  at `21a7332f` (criterion form).

**Named coverage gaps (not this round's counters).**
- T73W1S02: `delimited := True` (m2) survives all twelve arms and the sweep —
  only an out-of-suite probe catches it; next-round arm.
- T73W1S10: `seat_reports` counting at any depth (W2) survives all twelve arms
  and the sweep, and its non-equivalence probe reads `files=12` vs `13`; a
  nested-`.md` fixture arm is the next-round carry. W1 (`ok := True`) is killed
  by arms 2 and 6 but invisible to the standing sweep.
- T73W1S06: rounds 61-71 carry no `results.json` (11 unpinnable rounds) and
  round 60's artifact vocabulary is `agent='task'`, so future rows need a
  vocabulary map; one disagreement exists in the sweep (r72's `11 reports`).

## What was measured — R73-C2 (operability)

**Before.** `git show a3dd3574:tools/rekey-cost.py | grep -c REKEY_ARMS` → 0;
the tool had no battery mode, and the seven arm figures existed only as the
static receipts `cost-live-arm-*.txt` / `cost-arm-*.txt`. The round-72 wave's
coverage finding is the consequence: the IGNORED-filter mutant M3 survives all
six recorded arms (`KILLING_ARMS=0/6`,
`.ufo/evidence/round-73/reh/reh-c2-m3-six-arms.txt`).

**After** (receipt `.ufo/evidence/round-73/rekey-arms-r73.txt`, measured
commit `7982619f`, re-measured after the rekey at `2e89e539` and at the tip):

```
$ python3 -I tools/rekey-cost.py --arms
REKEY_ARM sources        expected=13 measured=13 ok
REKEY_ARM province       expected=6 measured=6 ok
REKEY_ARM quality        expected=6 measured=6 ok
REKEY_ARM scorecard      expected=0 measured=0 ok
REKEY_ARM pointer        expected=0 measured=0 ok
REKEY_ARM union          expected=17 measured=17 ok
REKEY_ARM ignored-skill  expected=0 measured=0 ok
REKEY_ARMS: arms=7 meet=7 unexpected=0            exit 0
$ python3 -I tools/rekey-cost.py --selftest
REKEY_COST_SELFTEST: 8/8 pass                      exit 0
```

Under M3 the same battery reads `ARM_UNEXPECTED ignored-skill expected=0
measured=9` and `REKEY_ARMS: arms=7 meet=6 unexpected=1` exit 1
(`.ufo/evidence/round-73/reh/reh-c2-m3-battery.txt`; the pristine/M3 sha256
pair is pinned in `reh/README.txt`). Seat T73W1S10 replicated M3
origin-independently on the same pristine bytes (sha256 `85ca2b69…`) and
scored the kill at 1/7 battery arms and 1/8 selftest arms
(`.ufo/waves/round-73/w1/T73W1S10/kill-matrix.md`), and re-derived the
measured value 9 without the tool. C2 verifies.

The battery is stable across the round's own rekey: the 13 sections the
rekey re-pinned do not move any arm (7/7 at `2e89e539` and at the tip), which
is the property the frozen predicate asks for ("at both the C2 commit and the
round tip"). A future legitimate ledger movement is a recorded amendment of
the arm table, never a silent pass: the battery names the arm, its expected
value and the measured one.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| destructive-prefix-edit | the S066 `used-by` append at `be1199d3` replaced a span that carried four cells (`[INFERENCE: refusing it is a design choice] | mined | 2026-10-20 | 365d | corpus/knowledge/guard-kill-closure.md`) with ONE cell, leaving an 8-field row: `awk -F'|' '/^\| S066 /{print NF}'` → `10`, `sources-census.sh validate` → `tameshi E01 S066 fields=8` exit 1, and the same malformed row rode into the rekey pin `be1199d3`. Caught by seat **T73W1S05**, which measured the field count per rev and refused to splice the cell into the collapsed line. | none in the round's own run list — the L1's pre-commit check was `git diff --numstat`, which showed `3 1` and looked like a one-line cell edit; nothing counted the row's fields. | the row was rebuilt from the base bytes with only `used-by` changed (`1d118c14`), re-verified `bad_rows=0` and census exit 0, and the repair's 13-section cost was paid by rekey batch-2 (`caa5c4c5`). Shown able to fail: `awk -F'|' … NF!=13` read `1` before and `0` after. The rule adopted: an edit to a table row is verified by a FIELD count, never by a diff line count. |
| piped-exit-capture | the first base-measure receipt printed `exit=0` next to an argparse error, because `$?` after `… \| tail -2` is `tail`'s status (`.ufo/evidence/round-73/mistake-exit-capture-r73.txt`). | none — the receipt's own text contradicted its exit field; the L1 read the output rather than the status. | every receipt-producing run now saves to a file and reads `$?` before any pipe; the receipt demonstrates the class (`… \| tail -2 ; echo exit=$?` → `0`; the same command unpiped → `2`). |
| copied-key-not-in-schema | the first wave-spec draft carried `solutionSpace` on every item (copied from the dispatch-bridge hint, not from the validator's item schema): `ufo-swarm-wave.mjs run` → `{"code":"invalid_spec","message":"items[0] has unknown key \"solutionSpace\""}` exit 1 (`.ufo/evidence/round-73/mistake-spec-key-r73.txt`). | the validator itself, at the first `run` — the wave would not have dispatched. | the key was dropped and the shipped spec validates exit 0; the receipt keeps the failing run beside the passing one. |

## Gate — census sentence correction (round-72 closure defect 3)

Measured this round on the live registry: `sources-census.sh validate --root
<fleet> tameshi` prints `tameshi W04 S303 duplicate url … across scopes` and
`tameshi ok`, exit 0; the `E04` finding appears only when a superseding row's
scope string equals the superseded row's (a same-scope fixture). The round-72
report's sentence therefore names the fixture behaviour, not the live one; the
correction of record is the paragraph appended above in this lesson, and the
report is append-only history.

## Gate — wave attacks (adopted, refuted, carried)

- **T73W1S07 (reviewer) — `[landed]` the frozen counter is spoofable by
  `measured := expect`.** A stub that parses the manifest and echoes each
  row's `expect` prints the byte-exact frozen line with zero artifact reads.
  No output-pinned counter can be immune in principle; the round's control
  class (always-meet, echo-printed, green-only) does not cover it. **Carried:**
  the claim's predicate is unchanged (it is a receipt, not an authenticator),
  but the report must not represent the counter's cheat coverage as general;
  a next-round hardening is a summary line that carries the derived population
  totals (the per-row `detail=` fields already do) instead of only the tally.
- **T73W1S07 — `[landed]` the plan's kill-rule wording is wrong.** The frozen
  sentence "C1 fails if … any control below reaches `unexpected=0`" is
  contradicted by the round's own receipt: the green-rows-only control reads
  `rows=4 met=4 unexpected=0` exit 0. The operative reading is the frozen LINE
  (`rows=6 met=6 unexpected=0`), which the control cannot print; the plan's
  control-(iii) text also describes a different stub than the receipt's third
  control. **Reported as a frozen-text defect, not repaired after data** (the
  r72 plan-defect precedent); C1's claim is unaffected.
- **T73W1S07 — `[landed, span-sensitivity]` the `seat_reports` red arm is red
  by span choice.** The same report self-corrects at its line 81 ("All 12
  seats settled and returned a report"), which rebounds to `meet`. The row
  measures the sentence the round-72 closure routed (line 56), which is the
  defect's own text; **disclosed in the SCORECARD row and the report** — the
  row pins a sentence, not the document's overall truth.
- **T73W1S07 — `[refuted]` the `plan-roles` red arm is robust**: `revenger`
  occurs 0 times at the pinned rev, and the round-73 erratum's `1 **revenger**`
  is unmatchable by the `N role` token regex (setup exit 2), so no meet-capable
  span exists at any revision. Caveat recorded: the invulnerability is partly
  accidental (an unbolded future append would open one at that new rev).
- **T73W1S07 — `[refuted for the standing manifest]` wrong-reason meets are
  constructible at kind level** (self-comparison, wrong noun, identifier
  token); no standing row does any of them and every standing span occurs
  exactly once. **T73W1S07 — `[residual]` `attack_share` is trust-me on
  `named` and sits at zero margin** (3/12 = 25.0 % against floor 25).
- **T73W1S09 (critic) — upheld both claims**, and measured the over-filtering
  direction: M3c (a real pin swallowed) survives the battery and the selftest
  while turning a 20-pin forecast into a false `0`; M3b (ledger members) also
  survives both. **Carried as the next round's arm**; also recorded that C2's
  values are a function of ledger content (a legitimate rekey entry that
  unpins PROVINCE.md makes two arms read 5), which is why the battery's
  docstring calls a value move a recorded amendment.
- **T73W1S11 (sentinel) — `SECRETS=1`**: the RFC fetch's response headers
  carried Cloudflare's `set-cookie` line; it was redacted to its name
  (`__cf_bm=<redacted …>`) in the same round, the value never reproduced in a
  record. `TMPDIR_VIOLATIONS=0` for both tools; `MISROOT=3` entries are
  orchestrator-owned runtime state (`.scratch/run13-state.json`, the
  dispatcher log, the watchdog log), none written by this round, and
  `.scratch/` is orchestrator-owned and was not touched.
