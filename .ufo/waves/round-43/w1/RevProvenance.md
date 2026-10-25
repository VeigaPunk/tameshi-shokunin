# RevProvenance — freeze chain and pin provenance (round 43, w1)

Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
BASEC `487b8f0da89fa0e2b8bea6930068accbf36e70a9`; ticket FREEZE `17f6ef0c72ec27e1aea305b5c95806b43bb2caef`.
Read-only: I wrote only this report; no measurement run (only permitted control modes); scratch `/tmp/tameshi-r43-RevProvenance-*`, deleted.
**Observed window 07:53–08:02 (2026-10-25). The freeze moved five times while I measured. §1–§7 are the chronological record (state at `17f6ef0` and the first reopen); §10 is the final state at HEAD `3aee2c0` and the freeze-of-record hazard.**

## 1. Pins at FREEZE `17f6ef0` — all five agree, and the worktree was byte-identical then

Method: `git -C LANE show FREEZE:<path> | sha256sum` vs `sha256sum <path>`, then `git show FREEZE:<path> | cmp -s - <path>`.

| artifact | contract pin | sha at FREEZE | sha on disk (at check) | pin agrees | freeze==disk |
|---|---|---|---|---|---|
| `tools/staged-id-guard.py` (`tool_sha256`, `frozen_tools[...]`) | `8140945a816873562eee8bcc6862d5e098f95b8083b4760b087812568f97b762` | same | same | **yes** | IDENTICAL |
| `tools/write-path-census-v4.py` (`frozen_tools[...]`) | `784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5` | same | same | **yes** | IDENTICAL |
| `.ufo/evidence/round-43/mutants/measure.py` (`claims.C1`) | `ad7ecf8c1c1ea1e84982eec5da6bb453ab5533eb6c4f0c09af5559f6ba6bc875` | same | same | **yes** | IDENTICAL |
| `.ufo/evidence/round-43/calibration/measure.py` (`claims.C2`) | `092c76cd6e10f9280af21237ec90dc14e63f0bdb9ae74fffb9da841730a8f286` | same | same | **yes** | IDENTICAL |
| `.ufo/evidence/round-43/guard/measure.py` (`claims.C3`) | `6278edcd691e230b32383a8b2ac25f38910e17f3041e4082271a5863a8d78601` | same | same | **yes** | IDENTICAL |

`git diff --stat FREEZE -- <five paths + contract.json>` was empty; `contract.json` at FREEZE and on disk were both `ef0f9ef39a637d1c766f31eca758b64ccdc67e74c19e1c13cd4831a11164aee2`. No `.gitattributes` exists, so no clean filter can mask a blob/worktree difference (the `cmp` above is raw blob bytes). Contract-internal consistency: `tool_sha256 == frozen_tools['tools/staged-id-guard.py']` (`8140945a…`); the census pin is the distinct `frozen_tools['tools/write-path-census-v4.py']` (`784de4c0…`).

## 2. Chain as it stood at check time

- `git merge-base --is-ancestor BASE FREEZE` → yes. `BASE..FREEZE` = exactly `697d2f1` 07:46:59 (contract + 3 counters + guard tool), `f0f2636` 07:48:13 (A1), `17f6ef0` 07:48:57 (A2/A3).
- HEAD was detached at FREEZE; `master`, `origin/master`, `origin/HEAD` all pointed at FREEZE — no commit on master after the freeze at that moment.
- `48148da` (only via `refs/jj/keep/…`) has the **same tree** as FREEZE with parent `f0f2636`: a jj same-tree twin, no content divergence.
- `1a02f63` (only via `refs/jj/keep/…`, 07:53:32) is a post-freeze child of FREEZE touching `corpus/SOURCES.md` only (+9/−2: S159/S160 append). The worktree registry was also modified (` M corpus/SOURCES.md`). No pinned artifact was in that commit, and the counters read the registry with `show(lane, rev, …)` (`calibration/measure.py:356-357`, `guard/measure.py:144`), never from the worktree, so a post-freeze registry edit cannot leak into a measurement at BASE or FREEZE.

## 3. Pin provenance per commit — pins moved only with their bytes

| commit | C1 counter / pin | C2 counter / pin | C3 counter / pin |
|---|---|---|---|
| `697d2f1` | `73000c9…` / `73000c9…` | `0586671…` / `0586671…` | `6ee86ed…` / `6ee86ed…` |
| `f0f2636` | unchanged | `092c76c…` / `092c76c…` | unchanged |
| `17f6ef0` | `ad7ecf8…` / `ad7ecf8…` | unchanged | `6278edc…` / `6278edc…` |

At each commit the pin equals the bytes committed in that commit; the contract diff spikes show the `counter_sha256` line changing with the counter body (A1: C2 pin + class texts + `distinct_axes` reformat + A1; A2/A3: C1 pin, C3 pin + A2/A3). `rule_changed:false` is consistent: `claims.*.target`, `rule`, `counting_command`, `do_nothing_control` were untouched by A1–A3. All three pin commits predate every wave-1 seat report (`.ufo/waves/round-43/w1/`, 07:53+) and every control receipt (07:49+); the only earlier receipts are the base-state runs in `.ufo/evidence/round-43/before/` (07:47:10–07:48:25), which are control/before data, not the deciding run. Corroboration: `.ufo/evidence/round-42/census/mutants.json` is byte-identical at BASE, FREEZE and disk (`b3abab06…`) — the contract's "at REV, unchanged" holds; the C1 counter declares exactly 12 fixtures including `F11_outflag_namespace` and `F12_method_two_returns`, matching `fixtures_pass=12/12`.

## 4. `self_pin` — verified, and it is the discriminator

- `mutants/measure.py:474-482`: `self_pin = 1 if sha(freeze_blob) == pin`; then `if running_sha != pin: self_pin = 0`.
- `calibration/measure.py:347` and `guard/measure.py:138`: `self_pin = 1 if sha(freeze_blob) == pin and running_sha == pin else 0`.

Re-executed the exact predicate against the real bytes at the check state: `self_pin=1` for C1/C2/C3 when both freeze blob and running file equal the pin; appending three bytes to the running copy flips all three to 0. The three counters also read the contract at FREEZE via `git show`, so a worktree contract edit is invisible to a measurement — the gate is the *running counter bytes*, not the contract's disk copy.

Permitted control modes actually run (python exit captured, not `tee`'s):

```
C1_R43_CONTROL: battery=round42_ten_fixtures fixtures_pass=10/10 mutants_declared=6 mutants_killed=4 C1_R43_CONTROL_PASS=false
C3_R43_CONTROL: stub_collisions_agree=0 expected_collisions=6 C3_R43_CONTROL_PASS=false
C2_R43_SELFTEST: cases=10 failed=0   VERDICT: PASS   (exit 0)
```

Control lines print neither `self_pin` nor `tool_sha_ok`, so a control PASS cannot be read as pin health; and `CONTROL_PASS=false` is the declared do-nothing outcome.

## 5. BLOCKING at `17f6ef0`: C1 compared its tool against the *other* tool's pin

- `mutants/measure.py:61` — `TOOL_REL = 'tools/write-path-census-v4.py'`.
- `mutants/measure.py:484-486` — `tool_raw = show(lane, rev, TOOL_REL)`; `tool_sha_ok = 1 if … sha(tool_raw) == contract['tool_sha256'] else 0`.
- `contract['tool_sha256']` at `17f6ef0` = `8140945a…` = the **staged-id-guard** pin; the census pin exists only at `frozen_tools['tools/write-path-census-v4.py']` = `784de4c0…`.

Measured:

```
base    census-v4 sha=784de4c0…  tool_sha_ok_vs_tool_sha256=False  vs_frozen_tools=True
freeze  census-v4 sha=784de4c0…  tool_sha_ok_vs_tool_sha256=False  vs_frozen_tools=True
```

So `tool_sha_ok=0` at both allowed revs while the predicate (`:595`) and target require `tool_sha_ok=1`: **C1_R43_PASS was unsatisfiable at `17f6ef0` regardless of the fixture battery.** C3 read the same key with `TOOL_REL='tools/staged-id-guard.py'` (`guard/measure.py:54,140-142`) and was consistent — the mismatch was C1-only.

Provenance of the defect: identical line text at `697d2f1:483`, `f0f2636:483`, `17f6ef0:486`, and `tool_sha256` was already the guard pin at `697d2f1` — so it was pre-declared, not introduced by an amendment. The base receipt `.ufo/evidence/round-43/before/c1-round42-at-base.stdout` records `tool_sha256=784de4c0…` as the value for the census tool, confirming intent. **It was then independently hit live**: A5's `why` reports that wave-1 seat MutC1F11 ran the frozen counter unmodified and printed `tool_sha_ok=0`. A5 repairs it to `pins.get(TOOL_REL, contract.get('tool_sha256'))`.

Correction to A5's narration: it says `tool_sha_ok=0 because A4 had moved the single top-level tool_sha256 to the guard tool`. The top-level key was **already** the guard pin at the first freeze commit `697d2f1`; A4 only re-pointed it at the repaired guard bytes (`efa5f129…`). `tool_sha_ok` was therefore 0 at `17f6ef0` before A4 existed; A4 was not the cause.

## 6. The freeze was reopened at 07:56:24 — HEAD `5cd2154` (A4/A5)

`5cd2154f7f4cf8ca1e0fae80c756d4186d91c4be` "round-43: freeze A4/A5 — guard map-shape repair (wave-1 finding) and C1 reachability gate + tool-pin source", parent `17f6ef0`; `master` and `origin/master` both moved to it. Files: `contract.json`, `control/c2-round42-counter.stdout`, `guard/measure.py`, `mutants/measure.py`, `tools/staged-id-guard.py`.

Verified at the new HEAD with the same pin procedure — **all five agree**:

| artifact | pin at `5cd2154` | bytes at `5cd2154` | agree |
|---|---|---|---|
| `mutants/measure.py` | `901d947f…` | `901d947f…` | yes |
| `calibration/measure.py` | `092c76cd…` | `092c76cd…` | yes |
| `guard/measure.py` | `fbc8ad3c…` | `fbc8ad3c…` | yes |
| `tools/write-path-census-v4.py` | `784de4c0…` | `784de4c0…` | yes |
| `tools/staged-id-guard.py` | `efa5f129…` | `efa5f129…` | yes |

`tool_sha256 == frozen_tools['tools/staged-id-guard.py'] == efa5f129…`. `claims.*` **minus** `counter_sha256` is byte-identical between `17f6ef0` and `5cd2154` for all three claims (C1 `0512057072bb0bad`, C2 `3251fceb343a10ce`, C3 `942f078466252eb8` via sorted-JSON sha), so the declared targets, rules, class texts, counting commands and controls survived the reopen exactly.

But the contract's own claims about the chain are now inaccurate and should be corrected (text, not data):
- `frozen_before` still reads "any wave seat ran and before the first deciding run…" at `5cd2154`. That is false for the current HEAD: the commit was created at 07:56:24, after wave-1 seats ran (w1 reports 07:53–07:56) and after the two wave-1 findings it repairs.
- `amendments_note` still reads "post-freeze amendments, if any, change citations and disclosures only; claims.*, the predicates, **counters**, targets, kill rule and controls are byte-unchanged". A4/A5 changed two counters, the tool, and three pins. The substantive scope was respected (claims minus pins identical) but the note's "counters byte-unchanged" is literally contradicted by the commit.

## 7. Live drift at 07:56:54 — one counter edited and not yet re-pinned

While I re-checked, `.ufo/evidence/round-43/calibration/measure.py` changed on disk (07:56:54, `52961c3709a39ef76f5a1c7de94080a384244703ea1b8ab9fcd6217c23666fdf`), and **neither contract pins it** (`5cd2154` and the worktree both still carry `092c76cd…`). The edit narrows m12 to the field form `**Planned (round N+1):**`, restricts m13 to backticked `grep` command cells, and rewrites the record-set docstring (citing wave-1 RevC2Classes F2/F3). This is a semantic change to m12/m13, i.e. exactly the kind of change the contract's `amendments_note` says cannot happen after the freeze.

`self_pin` matrix measured at 07:56:27–07:57:03 with the exact predicate (freeze blob vs pin, running disk bytes vs pin):

| running counter | FREEZE=`17f6ef0` (pin `ad7ecf8/092c76c/6278edc`) | FREEZE=`5cd2154` (pin `901d947/092c76c/fbc8ad3`) |
|---|---|---|
| C1 (`901d947…` on disk) | **self_pin=0** | self_pin=1 |
| C2 (`52961c3…` on disk, unpinned) | **self_pin=0** | **self_pin=0** |
| C3 (`fbc8ad3…` on disk) | **self_pin=0** | self_pin=1 |

Consequences: at the ticket's FREEZE `17f6ef0`, C1 and C3 now read `self_pin=0` because the counters on disk were edited after that freeze; at the current HEAD `5cd2154`, C1 and C3 read 1 but **C2 reads 0** because its bytes were edited at 07:56:54 and no contract pin (at either freeze) carries `52961c3…`. Any deciding run made right now fails `C2_R43_PASS` on `self_pin` alone, and A4/A5's `tool_sha_ok` repair only takes effect at a freeze whose contract carries the repaired counter/tool pins.

A second unpinned edit landed at 07:57:50, this time the C3 tool: `tools/staged-id-guard.py` on disk became `2484da72cf337d7e8fb3c8e7009b75f9803a24cfc924c2c23ea3049d1a2fa9ef` while `5cd2154` pins `efa5f129…` (and `17f6ef0` pins `8140945a…`). That diff added map-key normalisation (`staged:` prefix stripped, a non-S-id key raises `Refusal`), added `registry_sha256`/`staged_sha256` to the JSON result, and trimmed the `--json` docstring field list; its own selftest passed `cases=14 failed=0`. It was then rewritten again at 07:58:28 to `365bf95842ce9bb022af7edb5905f1d36e1a435a7365ff91469d2edcadb4b0c2` (still unpinned; +160/−57, document-keyed dedupe made form-insensitive over scheme/`www.`/trailing slash/case, `--map` keys accepted as `S153` or `staged:S153`), with `STAGED_ID_GUARD_SELFTEST: cases=23 failed=0 / VERDICT: PASS`. So at 07:58 the working tree carries two post-freeze, unpinned edits (C2 counter `52961c3…`, guard `365bf95…`); `tool_sha_ok` for C3 would be 0 against either committed freeze if measured from these bytes, and all of it must be re-frozen before it can be measured. (My pin tables in §1 and §6 are unaffected — they are statements about the two committed trees, and the §6 table was measured from `git show`, not the worktree.)

## 8. Secondary observations

1. `.ufo/evidence/round-43/before/c3-at-base.stdout` (07:48:22) was produced by the pre-A3 C3 bytes `6ee86ed…`, not by the pinned `6278edc…`. A3's entire diff is one line, `os.makedirs(os.path.dirname(tool_path), exist_ok=True)`, inside the `if args.tool_file:` branch (`guard/measure.py:155-166`), and the at-base run takes the absent-tool branch, so `[INFERENCE]` the printed fields are unaffected — but the receipt's producer is a superseded revision. `before/c1-round42-at-base.*` is a round-42-*counter* run (`C2_R42:` line); `before/c2-at-base.stdout` (07:48:25) postdates the final C2 commit and is produced by the then-pinned C2 bytes.
2. `mutants/measure.py:~519-527` labels the control line `C1_R43_CONTROL_PASS='true' if killed == len(muts)`, and `guard/measure.py` prints `C3_R43_CONTROL_PASS=false` when the stub disagrees: in both, `false` is the expected do-nothing outcome. The field name reads inverted against "control passed" and invites a false alarm.
3. The registry (`corpus/SOURCES.md`) is not hash-pinned anywhere in the contract, so its post-freeze edits are visible only in git/jj history, not through a declared pin. Only tools and counters are pinned.
4. Cross-referenced and reproduced against the pinned C2 bytes `97609511…`: wave-1 RevC2Classes' reachable crash is real. `calibration/measure.py:137` does `block_text[index + len(wanted):].splitlines()[0].strip()`; importing the pinned counter read-only and calling `m12_planned('## Round 9\n\n**Planned (round 10):**', 9)` raises `IndexError: list index out of range`. A trailing newline does not save it — `'**Planned (round 10):**\n'` and `'**Planned (round 10):**\n- claim one\n'` both return `['**Planned (round 10):** names nothing']`, because only same-line text after the field counts. For a deciding run the crash lands at `:443`, after `self_pin` is computed at `:385` but before the `C2_R43:` line, so the outcome would be a traceback and no receipt line rather than a silent false pass.

## 9. Tooling and cleanliness

No installs or upgrades (python3 + git only; pacman untouched). Counter runs used their own `tempfile.mkdtemp` trees under `/tmp`; my scratch `/tmp/tameshi-r43-RevProvenance-spin/` was deleted. Lane writes: this report only. At 07:57:03 the only pinned path modified on disk was `.ufo/evidence/round-43/calibration/measure.py`; at 07:58:04 two were modified — that file and `tools/staged-id-guard.py` (the two unpinned in-flight edits of §7). `contract.json`, `mutants/measure.py`, `guard/measure.py` and `tools/write-path-census-v4.py` matched HEAD throughout. `LOG.md`, `SCORECARD.md`, `corpus/{QUALITY,README,SOURCES}.md` and untracked evidence/waves dirs are sibling-seat edits, not mine.

## 10. Final state at 08:13 — HEAD `6b83a11` (A14), all pins agree, but the declared freeze of record is stale

`BASE..HEAD` now has thirteen commits. After the ticket freeze `17f6ef0` (A2/A3) the pin set moved seven more times: `5cd2154` (A4/A5), `114ffacd` (A6/A7), `53cb32b` (A8 narration), `273c047` (A9), `c5335c7` (records), `3aee2c0` (A10), `e20cf89` (receipts, contract byte-identical to `3aee2c0`), `b510ad1` (A11), `bb36f80` (A12 — the only pin != blob), `f551ca6` (A13), `e25cd2f` (records), and `6b83a11` (A14). `master`/`origin/master` and the worktree agree for every pinned path except `contract.json`, which is modified on disk at 08:14 (a fourth editing window just opened — the pins still govern the committed contract, not the worktree).

Pins at `e20cf89` (= `3aee2c0`), measured from `git show` and compared with the disk bytes:

| artifact | pin at `3aee2c0` | bytes at `3aee2c0` | disk | agree | self_pin (running bytes) |
|---|---|---|---|---|---|
| `mutants/measure.py` (C1) | `0d0f81bd…` | same | same | yes | **1** |
| `calibration/measure.py` (C2) | `97609511…` | same | same | yes | **1** |
| `guard/measure.py` (C3) | `ae66342d…` | same | same | yes | **1** |
| `tools/write-path-census-v4.py` | `784de4c0…` | same | same | yes | — |
| `tools/staged-id-guard.py` | `2e8f2e89…` | same | same | yes | — |

`tool_sha256 == frozen_tools['tools/staged-id-guard.py'] == 2e8f2e89…`. So the current tree is internally consistent and measurable — but only at `3aee2c0`.

**Freeze-of-record hazard.** `contract.json` `frozen_before` at `3aee2c0` still reads: "the freeze of record is `114ffacd…`, reached through 697d2f17 (first freeze) -> f0f26367 (A1) -> 17f6ef0c (A2/A3) -> 5cd2154f (A4/A5) -> 114ffacd (A6/A7)…". A8, A9 and A10 all postdate `114ffacd`, and A9/A10 changed all three counters and their pins. Measured `self_pin` for the *current* running bytes at each named freeze:

```
freeze 114ffacd (declared freeze of record)  C1=0 C2=0 C3=0   (each commit's pins agree with its own bytes)
freeze 53cb32b  (A8)                          C1=0 C2=0 C3=0
freeze 273c047  (A9)                          C1=1 C2=0 C3=1
freeze c5335c7  (records)                     C1=1 C2=0 C3=1
freeze 3aee2c0  (A10, HEAD)                   C1=1 C2=1 C3=1
```

A deciding run with `--freeze 114ffacd` (or `53cb32b`, `c5335c7`) therefore fails all three predicates on `self_pin=0` alone, even though the counters compute their numbers; only `--freeze 273c047`+ is valid for C1/C3, and only `--freeze 3aee2c0` is valid for all three. The `frozen_before` pointer must be updated to `3aee2c0` (or the deciding run must be documented with `--freeze 3aee2c0`), otherwise the contract names a freeze under which its own counter bytes read `self_pin=0`.

**Claims drift.** Against `17f6ef0`, `claims.C1` minus the pin is byte-identical; `claims.C2.classes` changed at `114ffacd` (A6/A7) in m8, m10, m11, m12 and m13 and is byte-stable from `53cb32b` to HEAD; `claims.C3.statement` changed. So my measurement (delta from the ticket freeze) and RevC2Classes' (delta across A8…HEAD) describe the same history: the class sentences were reworded once, at A6/A7. The `amendments_note` at `e20cf89` is stale three ways: it enumerates only "A1-A3… A4-A7… A8…" while the `amendments` array carries A1–A10 (A9 and A10 are undescribed yet they moved all three counter pins and the guard); it claims "the class sentences restated verbatim", which is false for the five C2 keys above (and C3's changed field is `statement`, not a class sentence); and it therefore no longer supports the pin-history it is meant to disclose. `A8` does correctly credit wave-1 RevProvenance for the earlier narration correction, and its replacement `frozen_before` was substantively right about who ran when — only to go stale again at A9/A10.

**Two contract-level gaps around the C1 pin, measured at `e20cf89` (independently reported by wave-1 RevC1Counter):**

1. `claims.C1.target` cannot be reproduced verbatim by the pinned counter. The target declares 16 `name=value` fields (`C1_R43_PASS` included); the counter's `fields.append` list at the same commit has 26. The target omits `live_tool_errors`, `not_killed`, `runtime_error`, `apply_error`, `killed_names`, `dead_code_names`, `dead_code_cases`, `rev`, `freeze` and `first_error`, and its last two fields are ordered `kill_fixture_reachable` then `dead_code_arg_ok` while the counter prints `dead_code_arg_ok` then `kill_fixture_reachable`. `first_error` is conditional (`measure.py:630` appends it only under `if errors:`), so the gap is 10 fields on a green run and 11 on a run error. (RevC1Counter reported 15 vs 25 by excluding the `C1_R43_PASS` flag — the mismatch and the reversed tail are the same.)
2. `claims.C1.mutant_set` names `.ufo/evidence/round-42/census/mutants.json at REV, unchanged`, but **no hash of it is pinned anywhere in the contract at `e20cf89`** (current bytes `b3abab06a48d…`). An edit to the mutant declaration between freezes would change what "6 declared / 5 killed" means without failing any `self_pin` or `tool_sha_ok`. (The file does read identical at BASE, `17f6ef0` and HEAD, so nothing is wrong today; the check was simply absent — the uncommitted A11 authoring in the next paragraph closes it.)

**Pin timeline.** Every contract revision and the pins it carried (each value equals the bytes committed in that commit):

| commit | C1 | C2 | C3 | guard |
|---|---|---|---|---|
| `697d2f1` | `73000c93` | `0586671a` | `6ee86ed0` | `8140945a` |
| `f0f2636` (A1) | `73000c93` | `092c76cd` | `6ee86ed0` | `8140945a` |
| `17f6ef0` (A2/A3, ticket freeze) | `ad7ecf8c` | `092c76cd` | `6278edcd` | `8140945a` |
| `5cd2154` (A4/A5) | `901d947f` | `092c76cd` | `fbc8ad3c` | `efa5f129` |
| `114ffacd` (A6/A7, named freeze of record) | `901d947f` | `52961c37` | `8c8147e7` | `365bf958` |
| `53cb32b` (A8) | `901d947f` | `52961c37` | `8c8147e7` | `365bf958` |
| `273c047` (A9) | `0d0f81bd` | `52961c37` | `ae66342d` | `e219007f` |
| `c5335c7` (records) | `0d0f81bd` | `52961c37` | `ae66342d` | `e219007f` |
| `3aee2c0` (A10) | `0d0f81bd` | `97609511` | `ae66342d` | `2e8f2e89` |
| `e20cf89` (receipts) | `0d0f81bd` | `97609511` | `ae66342d` | `2e8f2e89` |
| `b510ad1` (A11) | `b56a34d7` | `97609511` | `ae66342d` | `2e8f2e89` |
| `bb36f80` (A12) | `b56a34d7` (blob `3d1ff3dc` — **MISMATCH**) | `97609511` | `47a6afce` | `2e8f2e89` |
| `f551ca6` (A13) | `3d1ff3dc` | `ab76cbd3` | `47a6afce` | `2e8f2e89` |
| `e25cd2f` (records) | `3d1ff3dc` | `ab76cbd3` | `47a6afce` | `2e8f2e89` |
| `6b83a11` (A14) | `601c1840` | `ab76cbd3` | `47a6afce` | `03a796c5` |


`A14` (`6b83a11`, 08:10:15) closed the two open sightings verbatim: `mutants/measure.py` `601c1840…` and `tools/staged-id-guard.py` `03a796c5…` are now committed and pinned in its contract, all five `blob==pin` and `disk==pin` at HEAD `6b83a11`. So the 08:10 "two unpinned edits" line above is also an authoring window that closed cleanly.
So the named freeze of record `114ffacd` pins `901d947f`/`52961c37`/`8c8147e7`/`365bf958`, while the current instruments at `6b83a11` are `601c1840`/`ab76cbd3`/`47a6afce`/`03a796c5` — the pointer now lags the instrument by four freeze commits, exactly the `self_pin=0` result measured above (and in `c3-at-freeze`, which prints `self_pin=1` because the A6/A7 counter is run with `--freeze 114ffacd`, not because the pointer is accurate).
**The in-flight sightings were authoring windows, not divergence — except one commit.** Each worktree byte-state I flagged as unpinned was subsequently committed verbatim by the next freeze: C2 `52961c37` (seen 07:56:54) → A6/A7; guard `365bf958` (seen 07:58:28) → A6/A7 (whose C3 counter committed as `8c8147e7`); C1 `0d0f81bd` → A9; C2 `97609511` + guard `2e8f2e89` → A10; C1 `b56a34d7` → A11 (`b510ad1`, self-consistent: `claims.C1.mutants_sha256 = b3abab06…` landed, `kill_binding`, `mutants_sha_ok`, `held_refused`/`naive_agree`/`substitute` in the C3 target). At 08:06 the authoring window for A11 was open; it closed as `b510ad1`. `bb36f80` (A12, 08:07:08) then committed a **broken C1 pin**: `claims.C1.counter_sha256` stayed `b56a34d7…` while the committed `mutants/measure.py` blob became `3d1ff3dc…`, so `self_pin=0` unconditionally — and the L1's own prerun receipt `prerun/c1-at-A12.stdout` (08:07:25) shows it live: `self_pin=0 tool_sha_ok=1 … mutants_sha_ok=1 C1_R43_PASS=false`, every other field green. C2 `97609511` and C3 `47a6afce` are clean at `bb36f80`. `f551ca6` (A13, 08:09:36) repaired the pin (C1 `3d1ff3dc`, C2 `ab76cbd3`, C3 `47a6afce`, all `blob==pin`); `prerun/c1-at-A13.stdout` prints `self_pin=1 … C1_R43_PASS=true` and `prerun/c3-at-A13.stdout` prints `self_pin=1 … C3_R43_PASS=true`, while `prerun/c2-at-A13.stdout` prints `self_pin=1` but `C2_R43_PASS=false` on `first=m7:corpus/lessons/round-43.md_unknown_S259` — a class-extraction miss on the records, not a pin failure. `e25cd2f` (08:09:36) touched only `corpus/lessons/round-43.md`. `6b83a11` (A14, 08:10:15) then committed the two byte-states I had just measured open on disk (C1 `601c1840…`, guard `03a796c5…`) — another authoring window closed verbatim — and it is currently clean (C1/C2/C3/tools all `blob==pin` and `disk==pin` at HEAD `6b83a11`).

**Verdict for the ticket's question.** At the ticket FREEZE `17f6ef0`, every declared pin agreed with its freeze blob and with the then-current worktree (5/5, byte-identical) and all three counters read `self_pin=1`; the one blocking defect at that freeze was C1's tool-pin source (§5), since repaired. The chain is now `BASE → 697d2f1 → f0f2636 → 17f6ef0 → 5cd2154 → 114ffacd → 53cb32b → 273c047 → c5335c7 → 3aee2c0 → e20cf89 → b510ad1 → bb36f80 → f551ca6 → e25cd2f → 6b83a11`. Every committed tree from `697d2f1` through `f551ca6`/`e25cd2f`/`6b83a11` is internally pin-consistent **except `bb36f80` (A12), the only commit that shipped `pin != blob`** — and `self_pin` caught it, twice (statically and in the `c1-at-A12` rehearsal). The mechanism worked exactly as designed. What did not hold is the disclosure layer: `frozen_before` still names `114ffacd` (stale through A8–A14), `amendments_note` enumerates only A1–A8 while the array carries A1–A14, and its "class sentences restated verbatim" is false vs `17f6ef0` (C2 m8/m10/m11/m12/m13, C3 `statement`). The deciding run needs `--freeze` at `f551ca6`/`e25cd2f`/`6b83a11` or a later self-consistent rev — never `114ffacd` (A9/A10 bytes ⇒ 0/0/0) and never `bb36f80` (C1 `self_pin=0`).


