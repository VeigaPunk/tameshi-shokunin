# L1 adjudication of wave-2 cold reads — round 56 attempt 3

C0 remains `c0137451f5b7f22d65f748fc69f1b181f55e1378`; no `SKILL.md` bytes were changed. All 18 frozen headings have a final same-seat reader JSON and Markdown report after the two incomplete outputs were resumed under their original identities. No replacement seat was spawned.

The frozen binder's `RESOLUTIONS` map permits a per-heading maximum count of minor findings; the L1 adjudicates these specific `gap-minor` reports with their exact commands and outputs. That permits a C1 re-key measurement, but does not certify the cited details as accurate or clear a quality/no-harm defect. The stale or failing instructions remain explicit round-57 debt because changing `SKILL.md` after C0 would make its reader hash fail at REV.

| reader | findings | L1 disposition | evidence |
|---|---:|---|---|
| `T56W2Read04` | 1 | accept `gap-minor`: Kimi's summary omits the D1/D2 shared `off-by-one` class; its own tally and command output prove the omission. The `--check` observation is retained as a note, not an additional finding in the seat JSON. | `w2/T56W2Read04.json`, `.md`, `-receipts/` |
| `T56W2Read06` | 1 | accept `gap-minor`: `SOURCES.md:503` at C0 points to a stale `Next unused id` bullet, not the S026→S265 supersession. At C0 the target is line 506; after this round's appended search-log entry it is line 508. Do not edit the section before binding. | `w2/T56W2Read06.json`, `-receipts/02-anchor-SOURCES-503.txt`; `grep -n 'superseding held S026' corpus/SOURCES.md` → 508 |
| `T56W2Read07` | 3 | accept `gap-minor`: the scratch namespace's live dash-form boundary, the role-vs-`--paths` code mapping, and the exact stderr token shape are wrong/stale at C0; underlying commands and rule behavior are separately exercised. Defer text repair. | `w2/T56W2Read07.json`, `.md`, `-receipts/` |
| `T56W2Read15` | 2 | accept `gap-minor`: the env-diff entry omits `--fleet-root` for the mandated scratch-clone invocation; the active-row count is 50, not 49. Both are stale instructions/data, not a different result from the frozen round-21 sectionizer. | `w2/T56W2Read15.json`, `.md`, `-receipts/` |
| `T56W2Read16` | 2 | accept `gap-minor`: the named `bash-witness-study.py check` and registry-check example are non-clean against the current C0 tree; the seat recorded the exact exit/output. Defer text repair. | `w2/T56W2Read16.md`, `-receipts/` |
| `T56W2Read17` | 4 | accept `gap-minor`: five page-local anchors in the service-limits section (four findings) are 17 lines early. The section text itself is byte-identical base→C0; the loss is input drift on four round-55 tool/registry inputs, not a section edit. The page-wide exact sweep finds 57/61 line ranges stale; the +17 comes from the +4 (round 55) and +13 (round 56) insertions above them. Defer heading-anchored repair until round 57; an in-section edit would invalidate the C0 hash and re-create R55.3. | `w2/T56W2Read17.json`, `.md`, `-receipts/page-wide-sweep.txt`, `-receipts/calibration-mechanism.txt` |

All other 12 reader reports have empty findings and `verified-record` verdicts. The stale pointers and failing examples are **quality/depth harm not seen by the frozen no-harm monitors**; the 57/61 page-anchor defect is carried as a round-57 deferral, not fixed before binding.

The helper validator's 30-case selftest passes. The sentinel also found that its recursive reader glob can classify JSON receipts below `T56W2Read*-receipts/` as reader candidates; it refuses malformed receipt JSON, while the frozen C1 arm and binder have different globs. The L1 will bind only the 18 root-level reader reports after checking their `cand`, section SHA, `findings` list, command list, and sibling Markdown; the limitation is reported, not hidden.

## Frozen claim-size control results

- C1's five C0 scratch controls did not reach `C1_R56_PASS=true`; each failed and reported its
  exact frozen-counter line (`w2/T56W2CritDoNothingC1.md` and receipts). This supports the
  C1 target's no-op discrimination.
- C2's cheapest control **did reach** `C2_R56_PASS=true`: with the C0 docs already present,
  adding two 79-byte stub receipts with `rev=C0` gave `own=PASS docs=4/4 total=0`; a borrowed
  round-54 receipt with only its `rev=` token rewritten also passed (`w2/T56W2CritDoNothingC2.md`,
  v2/v3). The frozen gate can bind the bytes but cannot establish that the control ran. The
  contract predeclares this provenance blind spot; nevertheless, the §9 do-nothing discriminator
  fails for C2. No post-data target/counter change is made, and the round will not claim C2 as
  an admitted improvement solely from its final PASS line.
