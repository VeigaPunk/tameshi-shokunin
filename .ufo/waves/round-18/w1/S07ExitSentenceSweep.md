# R17-KNOW-EXIT — exit sentences vs code (S07)

Base rev `183f87b899e6cae46be98d251cbc87fb5118f6ca`. Blob pins at that rev:
`corpus/knowledge/input-keyed-coldread-credit.md` = `f5b961b62f4b2033d3c462be8176ed3ebcda043f` (75 lines),
`.ufo/evidence/round-17/measure.py` = `bc4c0c538e2539b99e20872aca332a25f40bedd7`,
`.ufo/evidence/round-17/coldread/assemble.py` = `a99f49105f59bdc4f28e427f2e716848a0e11a3d`.

## Scope and method

Every byte was read from the commit (`git -C <lane> show <rev>:<path>`). Every run was made from a
fleet-mirror clone checked out at the base rev, cwd inside the clone, with `GIT_*` stripped
(`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR`, and Python's own
`env = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}`):

```
W=$(mktemp -d /tmp/tameshi-r18w1-S07ExitSentenceSweep-XXXXXX); mkdir -p $W/fleet
for s in /home/vgpnk/Projects/shokunin/*-shokunin; do [ "$s" = …/tameshi-shokunin ] || ln -s "$s" $W/fleet/; done
git clone -q …/tameshi-shokunin $W/fleet/tameshi-shokunin
git -C $W/fleet/tameshi-shokunin checkout -q 183f87b899e6cae46be98d251cbc87fb5118f6ca   # CLONE_OK
```

Coverage of `corpus/knowledge` (25 files): `git grep -n -E 'measure\.py|measure-\*'` finds exit-code
prose in exactly one entry — `input-keyed-coldread-credit.md` §5 (`:75`) and the receipt citation at
`:47-48`. `incremental-pin-disposition.md:258` names a round-13 `measure.py` artifact but states no
exit code. `git grep -n -i assemble -- corpus/knowledge | grep -vi assembled` → no hit; **no knowledge
entry states exit codes for `coldread/assemble.py`** (its own docstring `assemble.py:95-98` declares
0/1/2, but that is outside this sweep's knowledge-entry scope).

## Code facts — `.ufo/evidence/round-17/measure.py`

| Anchor | Fact |
|---|---|
| `:93-95` | Docstring already states the correct rule: "0 measured (a missing default ledger is a measured `no-ledger` state, not an error) · 2 rev/required-blob missing, explicit --ledger-file/--ledger-rev unreadable, or overlay unreadable/forbidden-field · 64 usage." |
| `:113-118` | `REQUIRED_BLOBS = ('tools/mutate-and-run.sh', 'SHONEN.md', 'SKILL.md', 'corpus/SOURCES.md')` — the default ledger is **not** a required blob. |
| `:541-553` | `ledger_raw is None` → `ledger_present: False`, every section `reason: 'no-ledger'`, `return out` (no error). |
| `:1506-1517` | unresolved `--rev` → exit 2 `rev-missing`; missing `REQUIRED_BLOBS` → exit 2 `blob-missing`. |
| `:1520-1543` | explicit `--ledger-file` unreadable → exit 2 `ledger-file-unreadable`; `--ledger-rev` rev unresolved → exit 2 `ledger-rev-missing`; ledger blob absent → exit 2 `ledger-blob-missing`. |
| `:1545-1547` | no override → `ledger_raw = blob(repo, rev, DEFAULT_LEDGER_PATH)` (may be `None`). |
| `:1593-1598` | always prints the measurement and `return 0` on the measured path, `no-ledger` included. |
| `:143-147` | `UsageParser.error` → `raise SystemExit(64)`. |

## Empirical exit matrix (cwd = clone at base rev)

| # | Invocation (`python3 .ufo/evidence/round-17/measure.py …`) | rc | key output |
|---|---|---|---|
| A | `--rev 98bea7d… --repo <clone>` (default ledger absent: `git cat-file -e` rc=128) | **0** | `ledger_present=False`, `sections_covered=0/54`, `reasons={'no-ledger': 54}` |
| B | `--rev e3827ee… --repo <clone>` (ledger committed) | **0** | `ledger_present=True`, `box3_full_page=True`, `58/58` |
| C | `--rev 98bea7d… --ledger-file /nonexistent/ledger.json` | **2** | `{"error":"ledger-file-unreadable"}` |
| D | `--rev 98bea7d… --ledger-rev 98bea7d…:no/such.json` | **2** | `{"error":"ledger-blob-missing"}` |
| E | `--rev 98bea7d… --ledger-rev deadbeef…:path` | **2** | `{"error":"ledger-rev-missing"}` |
| F | `--repo <clone>` (no `--rev`) | **64** | stderr `measure.py: error: --rev is required` |
| H | `--rev 98bea7d… --inputs-overlay /nonexistent/ov.json` | **2** | `{"error":"overlay-unreadable"}` |
| I | `--rev 98bea7d… --ledger-file <readable bad JSON>` | **0** | `ledger_present=True`, `reasons={'invalid-ledger': 54}` |
| J | `--rev no-such-rev --repo <clone>` | **2** | `{"error":"rev-missing"}` |
| K | synthetic `/tmp` repo, `--rev HEAD` (all four required blobs absent) | **2** | `{"error":"blob-missing","missing":["tools/mutate-and-run.sh","SHONEN.md","SKILL.md","corpus/SOURCES.md"]}` |
| G | `--selftest` | **0** | `MEASURE_SELFTEST: 94/94 pass` |

Also measured for the entry's `:3` recheck claim: `trace-inputs.py --selftest` → rc 0, `SELFTEST: 27/27`.

## False sentence 1 — §5 exit map (`input-keyed-coldread-credit.md:75`)

> `number. Exits: 0 measured, 2 rev/blob/ledger missing, 64 usage.`

False as written. Measured A: a missing **default** ledger is exit **0** with `ledger_present:false`
and `reasons {"no-ledger":54}` (the ledger does not exist at `98bea7d` or `09ee1d0`; it exists at
`e3827ee`). Exit 2 applies to a missing **required** blob (`:113-118`, run K), an unresolved rev
(run J), or an **explicitly requested** `--ledger-file`/`--ledger-rev` that is unreadable/missing
(runs C/D/E). A readable but malformed ledger is also measured, exit 0 with `invalid-ledger` (run I).
`64 usage` is correct (`:143-147`, run F).

Corrected wording (replace `:73-75` tail):

```
and `calibration_restraint_score`; `overrides_used` must be false for a cited
number. Exits: 0 measured — including a missing default ledger (every section
`no-ledger`, `ledger_present: false`) and a readable but malformed ledger
(`invalid-ledger`); 2 for an unresolved rev, a missing required blob, an
explicit `--ledger-file` unreadable, a `--ledger-rev` rev/blob missing, or an
overlay unreadable/forbidden-field; 64 usage.
```

## False sentence 2 — receipt citation overbreadth (`input-keyed-coldread-credit.md:47-48`)

> `(`redbefore/measure-*.json`). Those runs use `--inputs-overlay`, so they are`
> `demonstrations; a cited score uses no override.`

The glob matches **four** committed receipts in `.ufo/evidence/round-17/redbefore/`:

| Receipt | `overrides_used` | `inputs_overlay_merged` | `ledger_present` | outcome |
|---|---|---|---|---|
| `measure-e69b488.json` | true | 1 | true | bucket `start 1563` `credited:true`, score 6 |
| `measure-09ee1d0.json` | true | 1 | true | section `input-drift:tools/mutate-and-run.sh`, score 6 |
| `measure-98bea7d.json` | true | 1 | true | section `input-drift:tools/mutate-and-run.sh`, score 6 |
| `measure-98bea7d-strict.json` | **false** | **0** | **false** | `reasons {'no-ledger': 54}`, score 6, exit 0 |

So "Those runs use `--inputs-overlay`" is false for `measure-98bea7d-strict.json`, which the same
sentence's glob cites; its producing command is recorded in `.ufo/waves/round-17/w1/X07MeasureV2.md:190-198`
(`--rev 98bea7da…`, no overlay, ledger absent at that rev). The three overlay receipts do confirm the
sentence's other claims: `measure-e69b488.json` has section `1563` (`## Effective expectation
reconciliation — round 14`) `{credited:true, reason:"credited"}`; `09ee1d0` and `98bea7d` both carry
`input-drift:tools/mutate-and-run.sh`. `legacy-r14-inputs.json` is one entry, `start:1563`,
`read_rev:e69b488…`, 19 inputs — the `:44` "19 inputs traced at `e69b488`" holds.

The final clause holds on separate receipts: `.ufo/evidence/round-17/c1-measure-e3827ee.json`
(`overrides_used:false`, `ledger_committed:true`, `58/58`, score 8) is the score receipt cited at
`SCORECARD.md:608`; `c1-measure-98bea7d.json` and `c1-measure-eb7838b.json` are also `overrides_used:false`
(no-ledger runs). Round-16 `measure-*.json` receipts are v1-schema (no `overrides_used` field) and the
round-16 `measure.py` has no `--inputs-overlay` option (`grep` over its source finds only its `:35`
`Exits:` line), so overlay status does not apply to them; they are not matched by the `redbefore/` glob.

Corrected wording (replace `:47-48`):

```
(`redbefore/measure-{e69b488,09ee1d0,98bea7d}.json`). Those three runs use
`--inputs-overlay` (`overrides_used: true`, one merged entry), so they are
demonstrations; `redbefore/measure-98bea7d-strict.json` is a separate
no-override run at the same rev, where the default ledger is absent
(`no-ledger: 54`, exit 0). A cited score uses no override
(`c1-measure-e3827ee.json`: `overrides_used: false`, 58/58, score 8).
```

## Holds

- `:44-46` credited at `e69b488` and `input-drift:tools/mutate-and-run.sh` at `09ee1d0` and `98bea7d` — verified from the four receipts above.
- `:3` recheck exit-0 claims — `measure.py --selftest` rc 0 (`94/94 pass`); `trace-inputs.py --selftest` rc 0 (`27/27`).
- `:41` "`SKILL.md` itself and the ledger are not inputs" — `IGNORED_INPUTS` at `measure.py:132` is exactly `('SKILL.md', DEFAULT_LEDGER_PATH)`.

## Limits / unresolved

- Inference: the two log-only lines in `redbefore/logs/exits.tsv` are dispositions-tool exits, not measure exits; they were not used as evidence here. [INFERENCE]
- No knowledge entry states `assemble.py` exits, so nothing there was falsified; no live `assemble.py` run was made (out of the assigned sentence set).
- The entry was not edited: wave instruments are staged/owner-installed; this report supplies the erratum text for the owner to append.

Verdict: falls — two false sentences in `corpus/knowledge/input-keyed-coldread-credit.md` (`:75` default-ledger exit 2; `:47-48` overlay claim over a glob that includes the strict receipt), both falsified by code anchors and committed receipts, with corrected wording supplied.
