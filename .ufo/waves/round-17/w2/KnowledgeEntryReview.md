# KnowledgeEntryReview — `corpus/knowledge/input-keyed-coldread-credit.md` @ `eb7838b`

Seat: `TameshiR17.KnowledgeEntryReview-2` (leaf reviewer, wave 2, round 17).
Lane root: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Read rev: `eb7838b16490ca7ba17ea3242ade76a61f744af2` (branch `master`).
Target sha256: `1fad5a57c56ea059ebfecedf37edb8256739d94382f89cf302d49d319ab9e57c`.
Clone (all executions): `/tmp/tameshi-r17w2-KnowledgeEntryReview-rG2F4Q/fleet/tameshi-shokunin`
(fleet-mirror symlinks; detached at the read rev). Scratch: `/tmp/tameshi-r17w2-KnowledgeEntryReview-src-yi74a2`
(fetched sources) and `/tmp/tameshi-r17w2-KnowledgeEntryReview-rG2F4Q`; the mutant worktree was removed.
No lane writes except this report; no `jj`; no git write in the lane or a sibling.

**Verdict (one line): all source, numeric, red-before and selftest claims hold; one factual error
in the exit contract (`missing default ledger` exits 0 `no-ledger`, not 2), one overbroad
`measure-*.json` citation, and minor omissions — provenance trio is conformant.**

## 1. Provenance trio (CORPUS.md)

| Requirement (`/home/vgpnk/Projects/shokunin/CORPUS.md:18-20, 163-170`) | Observation | Result |
|---|---|---|
| Entry opens with `source:`, `verified-at:`, `recheck:` | Lines 1, 2, 3 of the target, before the `#` title at line 6 | pass |
| External source cites its `S###` row alongside URL and anchor | Line 1 cites S058 URL + §4.2.2 p. 79:14; S059 URL + §Known issues quote; S064 URL + §Benefits/§Identifying non-hermeticity; S060 URL + §Filtering/%file, §General/-f, §Output format/-y | pass |
| Rows exist and name the entry in `used-by` | `corpus/SOURCES.md:67` (S058), `:68` (S059), `:69` (S060), `:73` (S064); all `mined`; each `used-by` contains `corpus/knowledge/input-keyed-coldread-credit.md` | pass |
| Own work is cited with path and commit | `corpus/lessons/round-16-verifier-spotcheck.md` exists at `98bea7d` (identical at `eb7838b`); §2 is `## 2. Claims, re-measured` (`:41`), §6 is `## 6. Routed defects` (`:214`), R16-C2b at `:226`; `.ufo/evidence/round-17/redbefore/` exists | pass |
| `verified-at` date and measured revs exist | `2026-10-20`; `e69b488`, `09ee1d0`, `98bea7d` all resolve as lane commits | pass |
| `recheck: 90d` is the tighter cited cadence and its commands pass | S059 recheck `90d`, S064 `180d`; both `--selftest` commands exit 0 (below) | pass |
| `ground: none` does not move a frontier row | `corpus/README.md:239-256` (Round 17 block): "No frontier row moves: F7 stays open"; the entry has its coverage row at `:246` | pass |

## 2. Claim-by-claim verification

| Claim (target path:line) | Evidence executed | Exit / key output | Result |
|---|---|---|---|
| Round 16 credited each bucket by section sha256, plus verdict and command count (`:15-16`) | `.ufo/evidence/round-16/measure.py` `sectionize()`/`coldread()` (`:91-134`, `:218-265`); `entry_credit_reason()` (`:179-215`) | section sha matched; verdict/count fields consumed | holds |
| Bucket was read once by CR26 (`:17-18`) | Round-16 ledger entry for `start:1563`: `seats:["CR26"]`, `sha256:e8720037…`, `skill_sha256:97cf436b…`, `commands_executed_count:4`; `reports` names `CR26.md` | entry present, single seat | holds |
| Runner was `75ed934d…` at the read and moved to `0673d2e5…` (`:18-19`) | `sha256(git show e69b488:tools/mutate-and-run.sh)` = `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5`; at `09ee1d0` and `98bea7d` = `0673d2e5374b94c651238e7497cbebaffb6483348400747b08f9d27cdc8118aa` | exact match | holds |
| Section bytes did not change, so it stayed credited (`:19-20`) | `sectionize()` at `e69b488`, `98bea7d`, and the round-16 snapshot: section `start:1563` sha = `e8720037c0b1bd43db7b21fe2dd9a2669fe64db11f72649c754c85d1832e7cbd` at all three; page shas differ (`97cf436b…` vs `906fb649…`) | identical section sha | holds |
| Recipe now exits 2 `expected_input_digest_mismatch` (`:20-21`) | Worktree at `98bea7d`: both `dispositions-before.json` and `dispositions.json` commands | exit 2; `{"kind":"expected_input_digest_mismatch","message":"tools/mutate-and-run.sh: observed 0673d2e5… expects 75ed934d…"}` | holds |
| Round-16 measure reported 54/54, score 8 at `98bea7d` (`:21-22`) | `python3 .ufo/evidence/round-16/measure.py --rev 98bea7d…` | exit 0; `score 8`, `covered 54/54`, `box3 True`, `missing []`; independent run matches `S08RunR16Probes.md` | holds |
| One-character disposition mutation (exit 2→0) left all 54 credited (`:23-24`) | Reproduced in a /tmp worktree at `98bea7d`: `emit_could_not_evaluate` `return 2`→`return 0` (line 1081); round-16 measure at the mutant commit; behavior witness with a missing dispositions file | measure exit 0, `score 8`, `54/54`, `box3 True`, `missing 0`; witness exit 0 (payload `could_not_evaluate`), pristine exit 2; matches `M01ShaOnlyHole.md` | holds |
| Verifying-trace definition and cache-key claim (`:28-30`) | PDF §4.2.2 "record the values/hashes of dependencies used last time… verifying trace stores only hashes"; Bazel caching §Known issues quote | verbatim sections present; statement is a faithful paraphrase | holds |
| Input gate: non-empty, regular blob 100644/100755 at REV; `input-drift:`, `input-missing:`, `input-not-blob:` (`:32-34`) | `measure.py:315-337` (`canonical_lane_path`, `ls_tree_mode`, `input_reason`) | reasons emitted as stated | holds |
| Trace gate: committed receipts, subset inputs, `traces-unrecorded`, `trace-missing:`, `trace-input-unrecorded:` (`:35-38`) | `measure.py:355-408`; strict mode at `:373` | listed three reasons present; **also emits `trace-invalid:` (`:393`) and `live-lane-read:` (`:408`), not named** | holds with omission (F3) |
| Failing entry with verified inputs vetoes (`:39`) | `measure.py:67-69` doc + aggregation; `absent/empty inputs cannot prove staleness, so they veto` | stated condition true; **empty-input failing entries also veto, not stated** | holds with omission (F4) |
| `SKILL.md` and ledger are not inputs (`:40-41`) | `IGNORED_INPUTS = frozenset(('SKILL.md', DEFAULT_LEDGER_PATH))` at `measure.py:125`; dropped at `:315`, `:400` | exact | holds |
| Red-before: 19 inputs traced at `e69b488` (`:43-45`) | `legacy-r14-inputs.json`: one item, `start:1563`, `skill_sha256:97cf436b…`, `read_rev:e69b488…`, 19 `inputs`; all 19 sha256 values compared to `git show e69b488:<path>` | 19/19 match, `mismatches []` | holds |
| Bucket credited at `e69b488`; `input-drift:tools/mutate-and-run.sh` at `09ee1d0` and `98bea7d` (`:45-47`) | Committed JSONs: `measure-e69b488.json` section 1563 `{credited:true,reason:"credited"}`; `measure-09ee1d0.json` and `measure-98bea7d.json` `{credited:false,reason:"input-drift:tools/mutate-and-run.sh"}`. Reconstruction: `measure.py --rev <rev> --ledger-rev 09ee1d0:.ufo/evidence/round-16/coldread/ledger.json --inputs-overlay .ufo/evidence/round-17/redbefore/legacy-r14-inputs.json` | e69b488: exit 0, score 6, credited, reasons `{credited:1, inputs-unrecorded:43, verdict:gap-blocking:1, verdict:wrong-expectation:5, wrong-expectations:1:1}` = committed JSON; 09ee1d0/98bea7d: exit 0, section `input-drift`, reasons `{input-drift:tools/mutate-and-run.sh:1, inputs-unrecorded:53}` = committed JSON | holds |
| Those runs use `--inputs-overlay`, so they are demonstrations (`:47-48`) | `measure-*.json` `overrides_used:true`, `inputs_overlay_merged:1` for the three revision runs; **`measure-98bea7d-strict.json` also matches the glob** and has `overrides_used:false`, `inputs_overlay_merged:0`, `ledger_present:false`, `reasons {no-ledger:54}`, score 6 | true for the three red-before runs; false for the `-strict` file matched by the glob | citation overbreadth (F2) |
| `trace-inputs.py` runs under `strace -f -y` (`:52-53`) | `trace-inputs.py:555-580` probe requires `-y`; `:630-631` argv includes `-f -q -z -s 4096 -o … -e trace=…` plus `-y` flags | exact | holds |
| In a clone at a 40-hex commit (`:53`) | `REV_RE = ^[0-9a-f]{40}$` (`:93`); receipt `rev` 40-hex or null; `repo_filter()` reads HEAD (`:529-552`). The tool does not clone; it records the clone's HEAD. | usage description; not a false claim, but the entry does not say the clone is the caller's action | holds (minor wording) |
| Keeps regular files opened read-only by name, tracked at the commit (`:53-54`) | `Tracer.record()`/`digest()` (`:266-420`, `:640-660`): read-intent opens, `.git` exclusion, tracked set, `isfile`, writes set | exact | holds |
| Write-opened, untracked and `.git/` excluded; Python bytecode off; external/live-lane flags (`:54-58`) | `trace-inputs.py:33-41` doc; `WRITE_FLAGS_RE`, `DIR_FLAG_RE` (`:400-410`); `scrubbed_env()` sets `PYTHONDONTWRITEBYTECODE=1` + `PYTHONPYCACHEPREFIX`; `record()` external/lane branches (`:290-308`); selftest checks | selftest exit 0, 27/27 | holds |
| Limits: env, stat-only, inherited fds, directory listings, network, clock, `git show` (`:62-65`) | `S12StraceFeasibility.md:159-207` items 1, 2, 3, 5, 6, 7 (git show) observed; item 4 O_PATH, 8 mmap, 9 io_uring, 11 TOCTOU also listed. **No clock item in S12** | six of seven observed; clock is true by construction (trace set has no clock syscalls) but the cited observation does not include it | holds with attribution gap (F5) |
| Host binaries outside the key; S059 false-hit class (`:66-67`) | `trace-inputs.py:290-308`: paths outside root/fleet/lane are dropped (or home-counted); Bazel quote: compiler from `/usr/bin` gives wrong shared cache hits | holds | holds |
| Re-measure fields: `coldread.box3_full_page`, `coldread.sections_covered`, per-section `reason`, `calibration_restraint_score`, `overrides_used` (`:72-74`) | `measure.py` output keys: `coldread.{box3_full_page,sections_covered,sections_total,sections[],reasons,missing,…}`, `calibration_restraint_score`, `overrides_used`; `sections[]` has `{start,heading,credited,vetoed,reason}` | exact | holds |
| Exits: 0 measured, 2 rev/blob/ledger missing, 64 usage (`:75`) | `measure.py --rev eb7838b…` (default round-17 ledger absent) → **exit 0**, `ledger_present:false`, `reasons {no-ledger:58}`, score 6; `--ledger-file /tmp/does-not-exist-ledger.json` → exit 2 `ledger-file-unreadable`; `--ledger-rev 98bea7d:no/such.json` → exit 2 `ledger-blob-missing`; no `--rev` → exit 64; `--rev 000…` → exit 2 `rev-missing`; code default ledger read at `measure.py:1443`, no-ledger branch `:503-509`, selftest `exit0-no-ledger` at `:883` | **the stated exit 2 for a missing default ledger is false**; 2 is correct only for a missing required blob/rev or an explicitly requested ledger/overlay | **falls (F1)** |

External sources (fetched 2026-10-20; HTTP 200 for all four):

- S058 PDF sha256 = `d6c175a48cc908ca3f185e1fb4620e3278c5655218ac687d83dfa7f405624ede` (exact match); PDF
  page 14 header is `79:14`, and §4.2.2 "Verifying Traces" states the verifying-trace rule.
- S059 `https://bazel.build/remote/caching`: `id="known-issues"` and the exact quoted text
  "Bazel does not track tools outside a workspace" (plus the `/usr/bin/` compiler false-hit example).
- S064 `https://bazel.build/basics/hermeticity`: `Benefits` and `Identifying non-hermeticity`
  headings present; §Benefits says the output can be cached and need not run again unless inputs change;
  §Identifying lists host system binaries/absolute paths and source-tree writes.
- S060 `https://man7.org/linux/man-pages/man1/strace.1.html`: the `Filtering` section contains
  `%file`; the `General` section (which begins before `Filtering`) contains `-f`; the
  `Output format` section contains `-y`; footer `strace 7.1.0.62.c605d6 2026-06-25`; host
  `strace -- version 7.2` (exit 0).

Recheck commands (`:3`): `measure.py --selftest` → exit 0, `MEASURE_SELFTEST: 89/89 pass`;
`trace-inputs.py --selftest` → exit 0, `SELFTEST: 27/27`; no FAIL lines.

## 3. Findings

### F1 — factual error: exit contract for a missing default ledger (`:75`)

The entry's documented invocation is `python3 .ufo/evidence/round-17/measure.py --rev REV`.
With the round-17 ledger absent at `REV` (the state at `eb7838b`), the command **exits 0** and
reports `coldread.ledger_present:false` with `reasons {"no-ledger":58}`, `calibration_restraint_score 6`.
The entry says "2 … ledger missing". The code reads the default ledger without error
(`measure.py:1443`) and coldread emits `no-ledger` (`:503-509`); the selftest names the case
`exit0-no-ledger` (`:883`). Exit 2 is observed only for an explicit `--ledger-file`/`--ledger-rev`
that is missing/unreadable (`:1422`, `:1437`) and for missing rev/blob/overlay.
Suggested correction: "0 measured (including a missing default ledger, reported as `no-ledger`);
2 for an unresolvable rev, a missing required blob, or an explicitly requested ledger/overlay
that is missing/unparseable; 64 usage." The `overrides_used:false` sentence remains correct.

### F2 — citation overbreadth: `measure-*.json` includes a strict, non-overlay run (`:47-48`)

`redbefore/measure-*.json` matches four files. `measure-98bea7d-strict.json` is a strict run
(`overrides_used:false`, `inputs_overlay_merged:0`, `ledger_present:false`, `reasons {"no-ledger":54}`,
score 6); it does **not** use `--inputs-overlay`, so the sentence "Those runs use `--inputs-overlay`"
is false for that cited file. The bucket-credit (`measure-e69b488.json`) and drift
(`measure-09ee1d0.json`, `measure-98bea7d.json`) claims are fully supported by the other three.
Fix: cite `redbefore/measure-{e69b488,09ee1d0,98bea7d}.json`, or name the `-strict` run separately.

### F3 — minor: the trace-gate reason list is incomplete (`:35-38`)

The entry names `traces-unrecorded`, `trace-missing:`, `trace-input-unrecorded:`.
`measure.py` also emits `trace-invalid:<p>` (`:393`, unparseable/wrong-schema receipt) and
`live-lane-read:<p>` (`:408`, trace `external` naming a live-lane path). A reader implementing the
note would miss two failure classes. Add them to the parenthetical.

### F4 — minor: the veto bullet omits the empty-input case (`:39`)

The entry states the sufficient condition "a failing entry whose inputs still verify vetoes".
`measure.py:67-69` is stronger: "an entry with drifted/missing inputs is stale and does not veto;
absent/empty inputs cannot prove staleness, so they veto." A failing entry with `inputs:{}` therefore
also vetoes. The entry does not state this fail-closed case; add it or cross-reference
`measure.py:67-69`.

### F5 — minor: the "clock" limit has no observed sweep in S12 (`:62-65`)

`S12StraceFeasibility.md:159-207` observes environment variables, network, stat-only checks,
O_PATH, directory enumeration, inherited fds, `git show`/objects, mmap, io_uring, attach, TOCTOU and
`-s` truncation — but not the clock. The clock claim is true by construction (`trace-inputs.py`'s
trace set is open/exec/chdir/dup, so `clock_gettime` is not captured), but the parenthetical
`(observed: w1/S12StraceFeasibility.md)` does not cover it. Either cite the syscall-set constant
or mark the clock item `[INFERENCE]` / "by construction".

### F6 — minor corpus-conformance: counts lack the required command/date form (`:21-22`, `:43-44`)

`/home/vgpnk/Projects/shokunin/CORPUS.md:34-38` requires any count in a corpus entry as
`<number> — <command> <date>`. The entry's `54/54` and `19 inputs` are accurate (verified above)
and point at retained evidence, but neither is written in that form. The `score 8` is a score, not
a count; the two counts still lack the inline command and date.

### F7 — minor: abbreviated citations (`:23-24`, `:45-48`, `:65`)

`w1/M01ShaOnlyHole.md`, `w1/S12StraceFeasibility.md` and `redbefore/measure-*.json` are not
lane-relative paths; they resolve only against bases established earlier in the entry
(`.ufo/waves/round-17/` and `.ufo/evidence/round-17/`). The full paths exist; use them in a
fresh citation or keep the base explicit.

## 4. Residual risk / verification gaps

- The M01 mutant commit named in the report (`5d6b9d55…`) is a `/tmp` clone commit, not a lane
  object; I reproduced the one-character edit and the 54/54 result in a separate `/tmp` worktree
  (commit `dbcaae4e…`, removed). [INFERENCE] The report's exact mutant object and mine are not
  byte-identical commits (timestamps/identity differ); the behavioral claim is reproduced.
- The round-16 ledger blob is absent at `e69b488`; it exists at `09ee1d0` and `98bea7d` with the
  same sha (`b84151a3…`). The red-before reconstruction needs `--ledger-rev 09ee1d0:…` (or
  `98bea7d:…`); the entry says "round-16 ledger" but not which revision supplies it (X07:171-181
  documents the command). The result holds; the exact ledger-rev is a reproducibility detail.
- The "clock" limit is structural, not observed (F5).
- Web sources are live pages; the PDF is content-addressed and matched exactly. The caching quote
  and hermeticity headings matched at fetch time; a later page edit would be caught by the 90-day
  recheck.
- No live-lane gate was run and no `jj`/git write touched the lane or a sibling; the round-14
  recipe and the M01 mutant ran only in /tmp clones/worktrees. The live lane's untracked
  `c1-*`/`c2-*`/`coldread/traces/` files are other seats' and were not touched.
- I did not re-run the full `registry-check` or the C1/C2 claims; this review is the knowledge
  entry's factual surface only.

## 5. Commands and exits (representative)

```
strace --version                          -> 7.2 (exit 0)
sha256sum build-systems-final.pdf         -> d6c175a48cc908ca3f185e1fb4620e3278c5655218ac687d83dfa7f405624ede
pdftotext -f 14 -l 14 build-systems-final.pdf -> page header 79:14; 4.2.2 Verifying Traces
curl -sSL <caching|hermeticity|strace.1>  -> 200; known-issues id; both headings; section titles
python3 .ufo/evidence/round-17/measure.py --selftest -> exit 0, 89/89
python3 .ufo/evidence/round-17/coldread/trace-inputs.py --selftest -> exit 0, 27/27
python3 .ufo/evidence/round-16/measure.py --rev 98bea7d… -> exit 0, score 8, 54/54, box3 true
python3 tools/evidence-disposition.py --root . --dispositions …/dispositions-before.json --json -> exit 2 expected_input_digest_mismatch
python3 tools/evidence-disposition.py --root . --dispositions …/dispositions.json --json -> exit 2 expected_input_digest_mismatch
measure.py --rev e69b488 --ledger-rev 09ee1d0:.ufo/evidence/round-16/coldread/ledger.json --inputs-overlay …/legacy-r14-inputs.json -> exit 0, score 6, bucket credited
measure.py --rev 09ee1d0 [same ledger+overlay] -> exit 0, section input-drift
measure.py --rev 98bea7d [same ledger+overlay] -> exit 0, section input-drift
measure.py --rev eb7838b… (default ledger absent) -> exit 0, ledger_present false, reasons no-ledger 58, score 6
measure.py --rev 98bea7d… --ledger-file /tmp/does-not-exist-ledger.json -> exit 2, ledger-file-unreadable
measure.py --rev 98bea7d… --ledger-rev 98bea7d:no/such.json -> exit 2, ledger-blob-missing
measure.py (no --rev) -> exit 64; measure.py --rev 000…0 -> exit 2 rev-missing
M01 repro: mutant commit dbcaae4e (return 2→0), round-16 measure -> exit 0, 54/54, score 8; witness exit 0 vs pristine 2
```

## 6. Verdict

**Holds on every source, number, red-before, section/runner hash and selftest claim; falls on
one exit-contract sentence (F1) and one overbroad citation glob (F2); F3-F7 are minor omissions.
The provenance trio is present and conformant.**
