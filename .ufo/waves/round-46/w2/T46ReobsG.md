seat: T46ReobsG
item: independent C1 re-observation at CONTENT `6f2168e028ce7ff6e82ac92093ac05dd1f147c32` of the four frozen statements `write-path-census-v2`, `write-path census destination resolution`, `staged-id adoption guard`, `freshness` — one frozen-argv run each in a scratch clone, claim re-derived with the counter's own `last_rows`/`claim_of` on the CONTENT `SCORECARD.md`, plus a full 22-statement counter cross-check and probe fixtures attacking the restated `What`/round cells.

Round 46, wave 2, C1 calibration seat. Read-only on the lane: no lane file, no `SCORECARD.md`, no `statements.json`, no counter was edited; no git/jj mutation anywhere (lane calls were `show`/`rev-parse`/`clone`/`checkout --detach` only, all inside `/tmp/tameshi-r46-T46ReobsG/`). No subagent dispatch, no background service, no network fetch. Nothing installed or upgraded; no pacman.

## 1. Setup (exact commands, all under `/tmp/tameshi-r46-T46ReobsG/`)

```
W=/tmp/tameshi-r46-T46ReobsG; mkdir -p $W/fleet
for d in /home/vgpnk/Projects/shokunin/*-shokunin; do b=$(basename $d); [ "$b" = tameshi-shokunin ] || ln -sfn $d $W/fleet/$b; done
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/clone
git -C $W/clone checkout -q --detach 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $W/fleet/tameshi-shokunin
git -C $W/fleet/tameshi-shokunin checkout -q --detach 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
git -C $W/clone rev-parse HEAD                       → 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
git -C $W/fleet/tameshi-shokunin rev-parse HEAD      → 6f2168e028ce7ff6e82ac92093ac05dd1f147c32
```

Pins at CONTENT (so the two pin flags the counter checks are not at issue in my run):

```
git -C $W/clone show HEAD:.ufo/evidence/round-46/calibration/statements.json | sha256sum
  → a15a8b4555f77bbf8149cd0161139fc7f66d696fa1ab5d178a5328e007f246e9   (== contract claims.C1.statements_sha256 ⇒ stmts_pin=1)
git -C $W/clone show HEAD:.ufo/evidence/round-46/calibration/measure.py | sha256sum
  → ad5f85df21b1e3f01ff5922242900d0b3bba1a044c9ff19828ecf00ab1ce680a
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-46/calibration/measure.py
  → ad5f85df21b1e3f01ff5922242900d0b3bba1a044c9ff19828ecf00ab1ce680a   (identical ⇒ self_pin=1)
```

Claims were read exactly as the item requires — `measure.py` imported via `importlib`, `last_rows()` on `git show 6f2168e…:SCORECARD.md` (2228 lines; `last_rows` returns 25 rows and contains a key for all 22 statement ids), then `claim_of(stmt, rows.get((kind,id)))`. No claim was read from the lane worktree.

## 2. Per-statement result (each frozen argv run once; `REV` = CONTENT in the env, cwd `$W/clone`)

| id | kind | claimed (CONTENT SCORECARD) | observed | verdict |
|---|---|---|---|---|
| `write-path-census-v2` | cap | `WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0` \| `0` \| `402285329588` | same three fields | **MATCH** |
| `write-path census destination resolution` | cap | `WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0` \| `0` \| `095924a7a165` | same three fields | **MATCH** |
| `staged-id adoption guard` | cap | `STAGED_ID_GUARD_SELFTEST: cases=24 failed=0` \| `0` \| `03a796c5726c` | same three fields | **MATCH** |
| `freshness` | axis | `9` | `9` | **MATCH** |

Raw commands and exits:

```
cd $W/clone
REV=6f2168e028ce7ff6e82ac92093ac05dd1f147c32 python3 tools/write-path-census-v2.py --selftest        → exit 0
  WRITE_CENSUS_V2_SELFTEST: bytes_unflagged=1 replace_unflagged=1 bytes_flagged=0 replace_flagged=0 scratch_replace=0
REV=… python3 tools/write-path-census-v3.py --selftest                                                → exit 0
  WRITE_CENSUS_V3_SELFTEST: var_unflagged=1 symlink_unflagged=1 literal_unflagged=1 scratch_var=0
REV=… python3 tools/staged-id-guard.py --selftest                                                     → exit 0
  STAGED_ID_GUARD_SELFTEST: cases=24 failed=0
  VERDICT: PASS
REV=… python3 .ufo/evidence/round-45/freshness/measure.py --lane $W/clone --rev 6f2168e…             → exit 0
  DISPUTED S048
  DISPUTED S093
  C1_R45: self_pin=1 population=73 entries=73 verified=73 drifted=0 unreachable=0 invalid=0 unreviewed=0 disputed=2 fresh=71 score=9 target=50 rev=6f2168e028ce7ff6e82ac92093ac05dd1f147c32 C1_R45_PASS=true
```

Tool digests by the counter's own method (`git show HEAD:<file> | sha256sum | cut -c1-12`):
`tools/write-path-census-v2.py` → `402285329588`; `tools/write-path-census-v3.py` → `095924a7a165`; `tools/staged-id-guard.py` → `03a796c5726c` — equal to the three prefixes the rows state.

`obs` match counts on the captured streams: v2 = 1, v3 = 1, guard = 1 (the extra `VERDICT: PASS` line is not matched by the anchored regex), freshness = 1 (`\bscore=(\d+)\b` matches only the `C1_R45:` line). No statement matched nothing.

Stability and side effects: each cap selftest was run twice more (`python3 tools/<tool>.py --selftest`), `cmp -s run1 run2` → identical for all three, exit 0 each; `git -C $W/clone status --porcelain` → empty after every run (none of the four statements writes into its cwd).

Full counter cross-check, run only into a scratch work dir and reported as observed, not as a verdict (wave-2 header authorises `--rev` CONTENT runs):

```
python3 .ufo/evidence/round-46/calibration/measure.py --lane $W/clone \
  --rev 6f2168e028ce7ff6e82ac92093ac05dd1f147c32 --base 683eedde3a50441c34d85a22f5fd5346f8b1ec6d --work $W/c1work
  STATEMENT cap/write-path-census-v2: … MATCH
  STATEMENT cap/write-path census destination resolution: … MATCH
  STATEMENT cap/staged-id adoption guard: … MATCH
  STATEMENT axis/freshness: claimed=9 observed=9 (exit=0) MATCH
  C1_R46: self_pin=1 stmts_pin=1 statements=22 mismatches=0 unparsed=0 unobservable=0 append_only=1 total=0 rev=6f2168e028ce7ff6e82ac92093ac05dd1f147c32 C1_R46_PASS=true
  exit 0, wall 11m18s
```

## 3. The restated `What` / round cells

Rows read at CONTENT (`git show 6f2168e…:SCORECARD.md`): `:2192` (v2), `:2193` (v3), `:2194` (guard) in the round-46 capability table — each the last row of its `(cap, id)` in file order (earlier rows `:1889`, `:1920`, `:2074`) — and `:2200` (freshness) in the round-46 axis table `| Axis | Score (0–10) | Evidence / counting rule | Measured commit | Last-change round |`.

| row | `What` (verbatim) | round cell | does it still describe the capability? |
|---|---|---|---|
| `write-path-census-v2` `:2192` | "classify a string-literal `expected.json` on `.write_bytes` and an `os.replace` / `os.rename` write, which the round-39 census misses, with planted flagged and scratch controls" | `round 40` | mostly yes; two clauses are not proven by the row's own command (F3). Round 40 is right: `git log --diff-filter=A -- tools/write-path-census-v2.py` → `5641ed8 round-40: freeze C1 write-form census and C2 S108 snapshot pin before data`. |
| `write-path census destination resolution` `:2193` | "resolve a write destination held in a variable through up to four assignments/`os.path.join`/`+`/`/`/f-string hops and classify it as expected-value, scratch or update-flagged, for `open`, `write_text`/`write_bytes`, `os.replace`/`os.rename` and `os.symlink`; v2 cannot connect a destination to a token that is not on the same line" | `round 41` | the enumerated write forms are real; the **quantitative bound is false** (F1) and the command exercises none of `open`/`write_text`/`write_bytes`/`os.rename`/`+`/`/`/f-string/update-flag (F2). Round 41 is right: `d4ee4e6 round-41: freeze contract, write-path-census-v3, fixtures, C1/C2 counters`. |
| `staged-id adoption guard` `:2194` | "decide … which ids … collide (0-3-space census pattern), dedupe a staged row whose document the registry already holds, refuse its own naive arithmetic map …, and admit only a by-document map …" | `round 43` | **yes** — every clause maps to a named selftest case (F5). Round 43 is right: `697d2f1 round-43: freeze — contract, three counters, staged-id guard tool`. |
| `freshness` `:2200` | (rule cell) "`floor(10 * fresh / 73)` from the round-45 counter … (`fresh=71`, `score=9`; 2 rows disputed: S048, S093) …" | `45` | **yes**, every number re-observed (F6); `Measured commit` is a phrase ("round-46 content revision"), the same convention as the `depth` row. |

## 4. Findings

### F1 — HIGH — the v3 `What` cell's "up to four assignments … hops" is falsified by measurement
Attacks `SCORECARD.md:2193` (re-stated verbatim from `:1920`). This is cell accuracy, not the C1 comparison: `claim_of` compares only the evidence cell's printed line, exit and tool sha, so `total=0` is unaffected.

Probe sources under `/tmp/tameshi-r46-T46ReobsG/probes/`, run as `python3 tools/write-path-census-v3.py --file <probe>` in `$W/clone`; the expected token sits at the far end of the chain and the write is `os.replace("src", <last>)`:

| chain form | links that resolve | first failing length |
|---|---|---|
| bare re-assignment (`a0="expected.json"; a_i=a_{i-1}`) | 2 → `expected_sites=1`; 3 → `1` | 4 → `expected_sites=0`, 5 → `0` |
| `os.path.join` (`p0=join(root,"expected.json"); p_i=join(p_{i-1},"h_i")`) | 2 → `1` | 3, 4, 5, 6 → `0` |
| `+` (`b0="expected.json"; b_i=b_{i-1}+"/h_i"`) | 1 → `1` | 2 → `0`, 3 → `0` |

`MAX_DEPTH = 4` (`tools/write-path-census-v3.py:46`) and the docstring's "to a depth of four" (`:15-19`) are about recursion depth, where each assignment link costs two units (a `Name` plus its bound). So the reach is 3 bare re-assignments, 2 joins, 1 concatenation — the cell overstates by 1, 2 and 3 links respectively. The row's own selftest exercises at most 2 links and no `+`/`/`/f-string at all.
Smallest safe correction: say what is measured ("three re-assignments, two `os.path.join` links, one `+` link"), or repeat the tool's own wording ("recursion depth four").

### F2 — LOW — the v3 selftest does not exercise the branches its `What` cell enumerates, though the tool implements them
Attacks the same row. Fixture scan (`json.load('.ufo/evidence/round-41/census/fixtures.json')`, construct membership per body):
`var_unflagged {os.path.join, os.replace}`, `symlink_unflagged {os.path.join, os.symlink}`, `literal_unflagged {os.path.join, os.replace}`, `scratch_var {os.path.join, os.replace}` — no `open(`, `write_text`, `write_bytes`, `os.rename`, `+`, `/`, f-string or `--update_goldens` anywhere.
That the capability itself is real (so this is an evidence gap, not a false capability):

```
probes/fstring_open.py     (open(dest,"w"), dest = f"{root}/expected.json")   → expected_sites=1 … unflagged=1
probes/plus_div_4hops.py   (write_text, Path "/" + "+")                        → expected_sites=1 … unflagged=1
probes/rename_dest.py      (os.rename(src, dst), dst from a variable)          → expected_sites=1
probes/update_flag.py      (source contains "--update_goldens")                → expected_sites=1 … unflagged=0
```

### F3 — LOW — the v2 `What` cell names `os.rename` and a comparison its command never runs
Attacks `SCORECARD.md:2192`. The five fixtures (`fixtures.json` of round 40) are `bytes_unflagged`, `bytes_flagged`, `replace_unflagged`, `replace_flagged`, `scratch_replace` — none uses `os.rename`, and the selftest never runs the round-39 census, so "which the round-39 census misses" is not proven by the row's pointer. Both clauses are true elsewhere: `classify_text("os.rename(tmp, 'case.expected')")` → `(1, 1)`; the v1 comparison is the round-40 counter's receipt (`SCORECARD.md:1876`: `v1_bytes_unflagged=0 v1_replace_writes=0 … C1_R40_PASS=true`).

### F4 — INFO — v3 counts an expected-named *source* as an expected write, so the `var_unflagged` fixture does not exercise a variable-held *destination*
`_write_call` returns `[node.args[1], node.args[0]]` for `os.replace`/`os.rename` (`tools/write-path-census-v3.py:138-141`). Fixture records (`classify_source` on the two variable fixtures):
`var_unflagged → [('os.replace', expected=True, scratch=False, unflagged=True, resolved='os.path.join(root, "actual.json")os.environ.get("REPO", ".")')]` — the expected token comes from the **source** `dest`, while the write destination is the literal join to `actual.json`. The selftest's `var_unflagged=1` therefore proves variable resolution (it would be 0 otherwise), not "a write destination held in a variable". The docstring documents "(both arguments)", so this is not a counter defect; the cell's phrasing is looser than the fixture.

### F5 — INFO — the guard row's `What` cell is fully covered by its 24 cases (no overstatement found)
`tools/staged-id-guard.py:307-396` builds 24 cases: `T1_indented_collision_seen`, `T1_column0_blind`, `T1_extractor_label` (`extractor == '0-3space'`) → the census clause; `T3_cascade_refused`, `T3_map_onto_registry_refused`, `T3_map_onto_staged_refused` → "refuse its own naive arithmetic map because the targets are still staged ids"; `T5_dedupe_to_registry_id`, `T5_document_form_insensitive`, `T5_dedupe_map_admitted` → the dedupe clause; `T4_valid_map_admitted`, `T4_multi_entry_map_admitted`, `T4_partial_map_refused`, `T4_non_injective_refused` → "admit only a by-document map"; plus `T2`, `T6`, `T7`, `T8`, `T9`×4, `T10`, `T11`, `T12`. This concurs with w2 `T46CritRestated.md` F7 only on the form point (the printed tally `cases=24 failed=0` does not name them); unlike the rows F7 lists, the guard's claims *are* exercised case by case.

### F6 — INFO — the freshness row's numbers all re-observed; nothing overstates
`floor(10 * 71 / 73) = 9`; observed `fresh=71 score=9 disputed=2` with `DISPUTED S048` and `DISPUTED S093` printed. `Last-change round 45` is consistent with the contract (`freshness 9 (round-45 floor(10*fresh/73))`). The counter compares only column 2 (`('9',)`), so the `Measured commit` phrase is outside the claim.

## 5. Difference from wave 1's observation of the same statements

Wave 1 `w1/ExecStmt07.md` observed exactly these four statements at the freeze `745a5831`; `w1/ExecStmt02.md` (all 22) and `w1/ExecStmt04.md` corroborate.

- **Observed side: no difference at all.** v2 `… scratch_replace=0` / 0 / `402285329588`; v3 `… scratch_var=0` / 0 / `095924a7a165`; guard `cases=24 failed=0` / 0 / `03a796c5726c`; freshness `9` (from `fresh=71 score=9`) — identical to my CONTENT values. No value drifted between the freeze and CONTENT.
- **Claimed side: all four were `None` at the freeze and parse now.** ExecStmt07: three cap rows carried only the tool's full sha256 and no `→ value, exit N` triple, and `last_rows` had no `('axis','freshness')` row at all (21 keys for 22 statements); at CONTENT all four parse and MATCH, and `last_rows` has 25 rows covering all 22 ids. This is the form/placement fix ExecStmt07 predicted, and it is the only change.
- No contradiction with `w1/ExecStmt04.md`'s "freshness has no standing axis row": the row now exists at `:2200`.

## 6. Not run (deliberately out of seat scope)

- The deciding run of the C1 counter is the L1's; my `--rev CONTENT` run above is a cross-check, reported as observed.
- No `--emit`, no `no-harm.sh`, no C2 (`mutate.py`) or C3 (`coverage/measure.py`) counter, no `--selftest` of the C1 counter itself, no lane write besides this file, no commit.
- The two axis statements outside my item (`depth`, `calibration`) were not re-run; I only note that both parsed in my `last_rows` pass.

## 7. Risks

- `freshness` re-derives from the round-45 counter's committed ledger and its 73 held rows, not from live fetches; a different ledger at another revision changes the value.
- F1/F2/F3/F4 rest on probe sources I wrote in `/tmp`, run through the tools' `--file` mode or their internal functions — not through the frozen statements. They inform cell accuracy, not the C1 comparison, which the four `--selftest`/`--rev` observations above settle.
- The four cap selftests are local and deterministic over the window I ran (3 runs each, byte-identical); a longer window is not evidenced.
