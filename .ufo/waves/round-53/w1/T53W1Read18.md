# T53W1Read18 — cold re-read of `### Round-21 gate/probe registry — finite environment differential`

Seat: T53W1Read18 (reader, wave 1). Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Content commit: `a41195dfc13a73958e4c5228ec196b28d03ded03` (C\*).
Source of bytes: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show C*:SKILL.md` only; the working tree was never read for section bytes.

## Section identity

| Field | Value |
|---|---|
| heading | `### Round-21 gate/probe registry — finite environment differential` |
| line range at C\* | heading 1971, last content line 2109 (139 content lines, 12239 bytes); line 2110 is the blank line before the next heading |
| boundaries | previous line 1970 is blank; next heading line 2111 is `## Ninth recorded case — round 26` |
| sha256 (UTF-8, surrogateescape, `\n` join, no trailing newline) | `eccd3ec82207fa69cee544f8f4ebfc0f9a473fe7254b8041ae2f5924f8d00a06` |
| fences inside the section | 0 |

Range/sha verification: the splitter (lines split, heading = `^#{1,3}(\s|$)` outside ``` fences, trailing whitespace-only lines stripped, `\n` join, no trailing newline) was first run against four revisions whose ledger entries record `start`, `end` and `sha256` under this exact heading, and it reproduced all four exactly:

```
8eaae28  computed 1964–1987  expected 1964–1987  sha_match True
2808f84  computed 1964–2008  expected 1964–2008  sha_match True
332dc89  computed 1964–2041  expected 1964–2041  sha_match True
bd38c02  computed 1964–2059  expected 1964–2059  sha_match True
```

(entries read from `.ufo/evidence/round-21/coldread/ledger.json` at C\*). The C\* range is therefore produced by the frozen monitor's own definition; the line shift 1964→1971 is this round's edit, not a splitter difference.

Only one line of this section differs between the round-52 base `6db1d220` and C\*, and it is this round's scratch-rules edit:

```
-| `tools/env-diff.py` | probe | `python3 tools/env-diff.py --contract .ufo/evidence/round-21/c2-contract.json --out /tmp/tameshi-f5.json` | ...
+| `tools/env-diff.py` | probe | `python3 tools/env-diff.py --contract .ufo/evidence/round-21/c2-contract.json --out "$HYAKU_SCRATCH/tameshi-f5.json"` | ...
```

## Checks run (holds)

Every row below was executed or read at C\*. "code" = source at C\* read with `git show`; "run" = the C\* bytes executed in scratch with `TMPDIR` bound under `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read18`.

| # | Statement in the section | Evidence | Result |
|---|---|---|---|
| 1 | `Source: corpus/lessons/round-21.md, QUALITY43–44 and corpus/knowledge/hermetic-env-differential.md (mined S079, reopened S028)` | `git cat-file -e` on both paths: present; `corpus/QUALITY.md` item 43 = pre-wave capacity/role resolution, item 44 = frozen mutation population rechecks its anchors (round-21 lesson cites "QUALITY43." / "QUALITY44." at lines 79/80); `SOURCES.md` S079 status `mined`; round-21 lesson line 39 "Existing S028 was reopened at https://bazel.build/…" | holds |
| 2 | "The frozen C1/C2 scripts and populations remain unchanged from 33d03b7" | `git diff --stat 33d03b7 C* -- .ufo/evidence/round-21/c1-survivors.py .ufo/evidence/round-21/c2-count.py` → empty; same for `c2-contract.json`; all three exist at `33d03b7` (`cat-file -e`). Control: the same command form on `tools/registry-check.py` prints `40 insertions(+), 6 deletions(-)`, so the empty result is a real no-diff, not a path typo | holds |
| 3 | "the maintained facade supplies public fixture selftests (the c2 fixture is fleet-bound, not isolated: it reads sibling blobs at the fleet root) without rewriting those instruments" | code `tools/round21-measure.py`: `SCRIPTS = {"c1": "c1-survivors.py", "c2": "c2-count.py"}`; the selftest copies the frozen scripts into a package and never edits them; its c2 fixture resolves `FLEET` out of the counter's source and runs `git -C {fleet}/{surface.repo} show` for every surface (lines ~80–86) — i.e. sibling blobs at the fleet root | holds |
| 4 | `tools/env-diff.py` Entry `--contract … --out "$HYAKU_SCRATCH/tameshi-f5.json"`; exit map 0/1/2/64; self-invocation `--selftest` | code: `add_argument("--contract"/"--out"/"--selftest")`; `return 2` on setup error; `return 0 if done == len(rows) else 1`; `Parser.error` exits 64. run: `python3 tools/env-diff.py --selftest` → `ENVDIFF_SELFTEST: 9/9 pass`, exit 0 | holds |
| 5 | write scope "isolated scratch sandbox under `$TMPDIR` (`tameshi-r21-envdiff.*`); sibling blobs read-only, no network" | code line 61 `TemporaryDirectory(prefix="tameshi-r21-envdiff.", dir=tempfile.gettempdir())` (honours `TMPDIR`), line 167 likewise for the pin sandbox; bwrap argv carries `--ro-bind / /` and `--unshare-net`; after the run above `TMPDIR`-pointed scratch dir was empty | holds |
| 6 | "frozen nine pins/seven profiles in `.ufo/evidence/round-21/c2-contract.json`; raw tuples in `.ufo/evidence/round-21/f5/receipt.json`" | contract JSON: `surfaces` = 9, `required_profiles` = 7 keys; receipt JSON: 9 surfaces, 7 profiles each | holds |
| 7 | `tools/wave-route-mix.py` Entry, exit map 0/1/2/64, "reads operator role routes, never edits routing", "max-share0.40" | code: `--max-share` default `0.40`; exits 0 ok / 1 refuse / 2 unreadable / 64 usage; docstring "Never writes anything."; `DEFAULT_CONFIG = Path.home() / ".omp/agent/config.yml"` | holds |
| 8 | round-28 correction: "`c2-count.py` sets `FLEET = Path("/home/vgpnk/Projects/shokunin")` (line 19) and reads … through `FLEET / frozen["repo"]` (line 52), not through `--repo`" | `git show C*:.ufo/evidence/round-21/c2-count.py` → line 19 is exactly the FLEET literal, line 52 is exactly `blob = show(FLEET / frozen["repo"], want_rev, frozen["path"])` | holds |
| 9 | "Current source re-anchors retain the199-entry prefix and label authorship; they are not blind/independent cold-read or required-command coverage" | ledger `round21_provenance.prefix_retained = 199`; ledger `provenance`: "original184 entries retained (159 round18 plus25 round19 author entries), plus15 actual L1-author source re-anchors; not blind/independent cold-read, recipe execution or required-command coverage" (184+15 = 199) | holds |
| 10 | "C1's guard kills include child-environment/command-pin contracts and synthetic process identities, not demonstrated malicious hooks or PID reuse" | round-21 lesson lines 93–95: "The input scrub/config checks assert the constructed child-environment contract; the three fixture hook checks assert command pins, not successful malicious-hook reproduction under scrubbed configuration." Read as written (constructed contracts / synthetic identities, not real attacks) it matches | holds |
| 11 | "C2's repeat comparison deliberately preserves random-path raw output variation; nine classified does not mean nine deterministic selftests" | `corpus/knowledge/hermetic-env-differential.md`: eight invariant + one nondeterministic (`js-round-gate`), stdout differs only by `mkdtemp` name, both exits 0; `f5/receipt.json` shows the same 8/1 split | holds |
| 12 | round-22 table: `wave-accounting.py` Entry `--bundle/--expected/--json`, exit map incl. 64, "eight literal public-CLI rejection fixtures in frozen round22 measure.py", "Supplemental isolated public-CLI fixtures cover16 further schema/accounting guards", "wrong-count-bundle.json / wrong-count-expected.json", "expected verdict is1/TOTAL_MISMATCH", "Normal `--help` exits0" | code `.ufo/evidence/round-22/measure.py`: `CASES` = 8 names, harness scores `0 if n == 8`; `.ufo/evidence/round-22/accounting-extra-cases.json` has 16 cases; both wrong-count files present; a `TOTAL_MISMATCH` entry pair is the first two CASES; run `python3 tools/wave-accounting.py --help` → exit 0 | holds |
| 13 | round-23 table: `command-binding.py` Entry `--bundle/--expected/--json`, "expected digest pins complete bundle", "public fixtures include `.ufo/evidence/round-23/extra-cases.json`", "frozen ten-case counter measure.py", "source-read bundle/expected pair is expected1/ARGV_MISMATCH" | code: `--help`/argparse at 198–201, `SNAPSHOT_TAMPERED` on digest mismatch; `extra-cases.json` = 19 cases; `.ufo/evidence/round-23/measure.py` present; registry rows for the source-read pair expect `exit 1` + `"finding_ids": ["ARGV_MISMATCH"]`; `corpus/knowledge/required-command-binding.md:59` calls them "The ten frozen rejection predicates" | holds |
| 14 | "The evidence-only `round-23/replay.py` runs the frozen baseline registry requirements … using the existing registry runner's opt-in `retain_streams=True` … It checks the requirements against the pinned source registry before running." | code `.ufo/evidence/round-23/replay.py`: digest check of `registry-baseline.json` then requirement/registry comparison before execution (lines 35–41); `module.run_row(..., retain_streams=True)` (line 60) | holds |
| 15 | round-23 correction: "Two external rows, `pin-disposition-read` and `verify-round15` … 41 revision-pinned rows plus 2 live-dependent rows" | `.ufo/evidence/round-24/replay/live-dependent.json`: `{"live_dependent": ["pin-disposition-read","verify-round15"], "revision_pinned": 41, "rows": 43}`; the 43-row `round-23/replay/bundle.json` contains both names | holds |
| 16 | "The replay gate covers all 43 stored receipts, including both declared-live rows." | bundle `receipts` length = 43; the two live rows are present (row 15) | holds |
| 17 | round-24 table: `registry-replay.py` Entry `--project/--run/--plan`, exit map 0/1/2/64; "Registry rows `command-binding-selftest-r24` (44/44), `command-binding-frozen-clean-pinned` and `command-binding-source-read-red-pinned` supersede the three round23 rows append-only. The two pinned rows also require their exact `bundle_sha256`." | `tools/registry.json` at C\*: 49 active + 7 superseded; active `command-binding-selftest-r24` expects `COMMAND_BINDING_SELFTEST: 44/44 pass`; the two pinned rows carry `"bundle_sha256": …` in `stdout_contains`; the three round-23 rows are `status: superseded`; run `python3 tools/command-binding.py --selftest` on C\* bytes → `COMMAND_BINDING_SELFTEST: 44/44 pass`, exit 0 | holds |
| 18 | "Frozen ruler: `.ufo/evidence/round-24/measure.py` (eleven predicates)." | docstring "eleven hardening predicates"; `.ufo/evidence/round-24/after.json` prints `"discriminated": 11` | holds |
| 19 | "The 47-row registry battery of round 24 (49 active rows from round 26 on; seat Read37)" | `.ufo/evidence/round-25/after/registry-final-3b20f07.json` = 47 active; `.ufo/evidence/round-26/after/registry-40a12bf.json` = 49 active; C\* `tools/registry.json` = 49 active | holds |
| 20 | "`registry-replay-selftest` is the fourth new active registry row and expects 10/10" | registry row order after the three command-binding rows is `registry-replay-selftest`, expectation `REGISTRY_REPLAY_SELFTEST: 10/10 pass`; run `python3 tools/registry-replay.py --selftest` on C\* bytes → `REGISTRY_REPLAY_SELFTEST: 10/10 pass`, exit 0 | holds |
| 21 | "The superseded 38/38 row still runs, fails against 44/44, and is excluded from the active tally." | registry: `command-binding-selftest` (superseded) still expects `38/38 pass` while the tool prints `44/44` → the row fails by construction; status `superseded` excludes it from the active tally | holds |
| 22 | round-24 correction: "The replay creates temporary clones; row commands can reach live siblings; Git hooks may run because the clone does not disable them." | code `tools/registry-replay.py` lines 152–154: `git clone --no-hardlinks …`, `checkout --detach`, no `core.hooksPath` override; line 19 comment: "private clone whose fleet mirror symlinks the live sibling repos" | holds |
| 23 | round-24 correction: "Use only caller-trusted local revision code and a fresh output directory; neither the clone nor this gate is a sandbox or producer authentication." | same code; table cells are explicitly flagged unreliable by the adjacent correction | holds (correction consistent with code) |
| 24 | "Full limitations and evidence: `corpus/lessons/round-24.md` Errata E–P and residual corrections" | lesson contains Erratum E, F, G, H, I, J, K, L, M, N, O, P (and the H addendum) | holds |
| 25 | round-28 correction: facade Entry "names the live lane path: a cold reader should substitute its own clone for `--repo` and expect the live lane read"; "The write-scope cells cover writes only, not reads." | Entry cell begins `--repo /home/vgpnk/Projects/shokunin/tameshi-shokunin`; the `c2-count.py` FLEET literal makes the pin read independent of `--repo` | holds |
| 26 | "The `tools/wave-route-mix.py` Entry reads the operator's live route table (`~/.omp/agent/config.yml`), so its exit today can differ from the retained round-21 receipt `.ufo/waves/round-21/routemix-spec1.json` (`ok: true`)" | code `DEFAULT_CONFIG = Path.home()/".omp/agent/config.yml"`; receipt `{"max_share": 0.4, "ok": true, … "seats": 71, "unrouted": []}` | holds |

Runtime checks were run on the C\* bytes only (`git show C*:tools/<tool> > scratch/run/tools/<tool>`), with `TMPDIR` bound to the seat scratch; none touched the lane or the fleet root.

## Observations (not findings)

These are real properties of the section or its instruments that do not make any statement false; they are recorded for the L1 and the closure, not as findings.

1. **Run-together tokens.** Line-level joins merge a space before numbers in these tokens: `from33d03b7` (1975), `the199-entry` (1993), `minedS082` (1997), `minedS083` (2018), `minedS084/S085` (2051), plus `max-share0.40` (1983), `selftest0 clean/1 failed` (1985), `cover16` (2008), `is1/TOTAL_MISMATCH` (2011), `exits0` (2014), `including62/62` (2019), `expected1/ARGV_MISMATCH` (2026). Every merged value was verified in the checks above (33d03b7 is a real commit and the counters are byte-identical to it; 199 = ledger `prefix_retained`; S082/S083/S084/S085 are `mined` rows; 0.40 is the `--max-share` default; 16 = `accounting-extra-cases.json`; exit 1 + `TOTAL_MISMATCH`; `--help` exit 0; exit 1 + `ARGV_MISMATCH`; 62/62 = `sections_covered: 62, sections_total: 62` in `.ufo/evidence/round-21/final/monitor-current.json`). The joins hide number boundaries and break exact search; they do not make a statement untrue, so they are not findings.

2. **Scope of "frozen C1/C2 scripts".** `tools/env-diff.py` does **not** exist at `33d03b7` (`git cat-file -e 33d03b7:tools/env-diff.py` → "exists on disk, but not in '33d03b7'"); it was added in `370f2df` and modified at C\*'s parent chain by `218bc6b` (this round's TMPDIR patch). The sentence is true of the frozen counters and contract (`c1-survivors.py`, `c2-count.py`, `c2-contract.json`: present at 33d03b7, byte-identical to C\*), which is also how the round-21 lesson uses the phrase ("the unchanged frozen C1/C2 scripts" = the two counters). Consequence worth knowing, not a contradiction of the text: the retained F5 receipt carries `instrument_sha256 e8b47ab7…`, while the C\* `tools/env-diff.py` hashes `f1bba50e…` (`218bc6b` changed exactly one line of it), so the receipt cannot be reproduced byte-identically by the patched tool; the section makes no claim that it can, and its round-28 paragraph already says the receipts, not a re-derivation, are the record.

3. **Frozen wrapper `/tmp`.** `.ufo/evidence/round-21/coldread/measure.py` still contains `TemporaryDirectory(prefix='tameshi-r21-selector-', dir='/tmp')` in its selftest. It is outside `tools/`, deliberately unchanged, and contract C2 declares "tools and counters outside tools/ (frozen .ufo/evidence counters with /tmp are routed, not claimed)". Not a violation of the host scratch directive either: the sandbox holds a few small fixture files, well under the 50 MB `/tmp` allowance. Reported as routed debt, not a finding against this section.

4. **Ledger verdicts for this heading.** The last pre-C\* ledger entries for this heading (read_rev `9f3084bc`, `bb681566`) are `verified-record` with `wrong_expectations: 0`, `blocking_gaps: 0` at range 1964–2103 and `sha256 16a5965b…`; the C\* section is re-keyed (`eccd3ec8…`, 1971–2109) by this round's scratch edit — the re-key, not a semantic repair, is what this heading owes wave 2.

## Findings

**None.** No statement in this section failed at C\*: `findings` is `[]`. Every count, pointer, exit map and receipt cited above resolves at `a41195dfc13a73958e4c5228ec196b28d03ded03`, and the three runtime checks performed on the C\* bytes (command-binding 44/44, registry-replay 10/10, env-diff 9/9) printed their documented verdicts with exit 0.

## Bounds of this read

- Verified by code reading and by running only the three self-contained selftests above; I did not run `--run`/`--claim` paths (they write bundles, run clones, or read live fleet state) and I claim nothing about them beyond the source I cite.
- Historical counts that cannot be rebuilt (e.g. "the 47-row battery of round 24") are verified against the committed registry snapshots named in the checks, not by re-running round-24 tooling.
- Live operator state (the current `~/.omp/agent/config.yml` routing) was not read; the section's own caveat says that exit can differ from the retained receipt.

## Tooling and scratch

- Tools installed/upgraded: none. Used the host `python3` (3.14) and `git`; no pacman, no network fetch, no `~/.local/bin` write.
- Scratch: `/fast/scratch/hyaku/tameshi-r53/w1/T53W1Read18` (extraction + four run dirs + `TMPDIR` sandboxes), deleted before yielding.
- Writes: only this report and `T53W1Read18.json` under `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-53/w1/`.
