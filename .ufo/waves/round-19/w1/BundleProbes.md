# BundleProbes: round-18 `final/checks.json` row `probes` (round 19, w1)

Seat `TameshiR19-2.BundleProbes` (scout, leaf). Date: 2026-10-21. Lane: `L=/home/vgpnk/Projects/shokunin/tameshi-shokunin`.

Ground rules for this seat:
- Read-only.
- The receipt argv was **not** executed.
- No lane selftests, builds or tests were run.
- Nothing was installed or updated.

Paths below are relative to `L/.ufo/evidence/round-18/` unless written in full.

## Verdict

Row `probes` is **current, successful evidence**, not a failed raw attempt.
- **Digest:** its one recorded digest matches the retained stdout (1/1).
- **argv:** conforms to the ruler's CLI source.
- **Revision attribution:** internally consistent (`argv[3] == revision == 921ef8077440f90d092aab4b9fdc750a45de1224`). The bytes corroborate it only indirectly.

No correction of the row is owed. There are four disclosure-level gaps:
1. The row does not digest stderr.
2. The executed ruler bytes, the cwd and the interpreter are not recorded.
3. The text-mode stdout carries no revision.
4. The P01–P04 `target=` line labels are base-`183f87b` line numbers, not lines at the measured revision.

**Treatment:** keep all three files verbatim. Classify the row as the effective historical receipt at `921ef807…`. No supersession and no erratum against the row (§6).

## 1. Digests: 1 recorded, 1 match, 0 mismatch; 1 retained stream unbound

| Item | Row | Observed (command) | Result |
|---|---|---|---|
| `stdout_sha256` | `d37c99e3…4eb8cf0` | `sha256sum final/probes.stdout` → `d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0`; `wc -c` → 4111; 12 lines | **match** |
| stderr | no key (row keys: `argv`, `exit`, `revision`, `stdout_sha256`) | `final/probes.stderr` is 0 bytes, sha256 `e3b0c442…7852b855` | **unbound by the row**; consistent with the success path |
| `checks.json` file | — | sha256 `fed3c8e6cba05c41…5815c671d`, the same value pinned in round-19 `before.json` and `after-21e7932.json` `inputs` | pinned |
| history | — | Git blobs are identical at 5923d89, a85f710, 4b7c682, 7243e7f, 78b99dd, 21e7932 and in the working tree: `checks.json` `d8c98a92…`, `probes.stdout` `8a0d3db0…`, `probes.stderr` `e69de29b…`. First committed 18:40:48-03:00 in 5923d89 (its jj-keep snapshot `3d47c781` has the same timestamp) | never rewritten |
| downstream pins | — | Every `probes.stdout` pin found records `d37c99e3…`: `coldread/ledger.json` (17/17 entries) and `coldread/traces/L1/*.json` (17/17 files). The verifier reconciled the same digest (`corpus/lessons/round-18-verifier-spotcheck.md:99-102`) | consistent |

## 2. argv vs CLI source: conforms

Row argv: `python3 .ufo/evidence/round-18/defect-probes.py --rev 921ef8077440f90d092aab4b9fdc750a45de1224`.

**Ruler identity.**
- The ruler is blob `dc6fe875…` (sha256 `99297d9645151dee…daebeaa`).
- The blob is the same at 01d586d, 921ef80, 5923d89, a85f710, 4b7c682, 7243e7f, 78b99dd, 21e7932 and in the working tree.
- After 01d586d (17:24:26-03:00), no commit in any ref touches the ruler, including `refs/jj/keep/*`.

**Parser.** `defect-probes.py:1035-1046` defines `--rev` (metavar `REV`), `--json`, `--only` (choices P01–P11) and `--selftest`. `--rev` is required unless `--selftest` is given. The usage line at `:17` reads `--rev REV [--json]`. The row uses the exact long option and a full 40-hex value.

**The output bytes match this argv form.**
- Text mode (no `--json`) prints 11 `PROBE` lines, then `DEFECT_PROBES: open=%d closed=%d total=%d`, to stdout (`:952-957`).
- Observed: P01…P11 in order, once each, with the summary at line 12.
- With `--json`, the PROBE lines would go to stderr and stdout would be JSON (`:938-951`). Not observed.
- A usage error prints usage to stderr and exits 64 (`:110-113`). Not observed: stderr is empty.

**Exit contract.** `defect-probes.py:21` (read 2026-10-21): "Exits: 0 measured (any open/closed mix); 2 could-not-evaluate; 64 usage."
- The row says exit 0.
- The stdout has 0 `could-not-evaluate` lines and 0 `PROBE … error` lines.

**Same spelling elsewhere:** the recheck at `corpus/knowledge/guard-kill-closure.md:3` and the SKILL row quoted at `final/audit-1925.stdout:6`.

**Not recorded:**
- The `python3` interpreter is not pinned.
- The row has no cwd. The relative script path resolves only from the root of a lane checkout.

## 3. Revision attribution: consistent, corroborated only indirectly

**The row agrees with itself.** `argv[3] == revision` is true (`921ef807…`).

**How the ruler pins the graded tree.**
1. `resolve_revision` (`:274-280`) runs `rev-parse --verify … REV^{commit}` and requires a 40-hex result.
2. `clone_lane_at` (`:283-332`) clones LANE_ROOT, checks out REV detached, and refuses unless the clone's `HEAD` equals REV (`:324-327`).
3. The graded tools are therefore content-addressed to `921ef807…`.

The ruler itself is **not** taken from REV. The invoked file is copied into the clone (`:328-331`), and its executed bytes are not recorded.

**The stdout carries no revision.** `grep -c 921ef80 final/probes.stdout` → 0. `rev_resolved` is emitted only in `--json` mode (`:945`).

**Content corroboration.**
- P03 and P04 read `1 of 48 cases`.
- The earlier runs read `1 of 46 cases`: `c2-probes-v2-e08271a.txt` and `.ufo/waves/round-18/w2/RerunC2After.md:32-33` (01d586d).
- The case counts agree with the other selftest outputs in `final/`:
  - registry-check: `final/registry-selftest.stdout:49` reads `SELFTEST: PASS (48 cases)`.
  - P01/P02 `1/63` vs `final/disposition-selftest.stdout:64`, `PASS (63/63)`.
  - P05–P07 `29/30` vs `final/trace-selftest.stdout:31`, `30/30`.
- In 01d586d..21e7932, only 9ee1c80 (18:09:03) touches `tools/`, `.ufo/evidence/round-17/coldread/` or the ruler.
- So the bytes fit 921ef80 and do not fit e08271a or 01d586d. They cannot tell 9ee1c80…21e7932 apart.

**Ancestry and byte identity.**
- `git merge-base --is-ancestor` gives 921ef80 → 4b7c682 → 7243e7f → 21e7932.
- `git diff --stat 921ef80 {4b7c682,7243e7f,21e7932} -- tools/ .ufo/evidence/round-17/coldread/ .ufo/evidence/round-18/defect-probes.py` is empty.

**Timing.**

| Event | Time (-03:00) |
|---|---|
| 921ef80 committed | 18:28:40 |
| `registry.stdout` mtime | 18:32:16.58 |
| `probes.stdout` mtime | 18:33:00.69 |
| `checks.json` mtime | 18:33:15.38 |
| 5923d89 commits the receipt | 18:40:48 |

- The mtime order equals the key order of `checks.json`: registry → probes → registry-selftest → … → assemble-selftest → checks.json. [INFERENCE] One sequential driver produced the row and its bytes.
- The probes slot is at most 44.1 s (from the end of the registry write to the end of the probes write). That is close to the full tip runs seen in wave 2 (45 s, 49.9 s, 54 s, 54.6 s) and above the 31.4 s base run.
- The bytes differ from every earlier retained run (temp-dir suffixes, P08 fixture commits, P11 declaration sha). This was a fresh run, not a copy.

**Three distinct revisions.**
- Measured: `921ef807…`.
- Commit that first contains the receipt: `5923d89…`.
- Landed tip: `4b7c682…`.

Erratum R18-1 (`corpus/knowledge/guard-kill-closure.md:179-183`) attributes the result to 921ef80 and claims no run at the tip. That is correct.

**Label hazard.**
- The P01–P04 `target=` lines (445, 552, 466, 96) are positions at base 183f87b, taken from `GUARD_SPECS` (`:53-103`).
- At 921ef80 the anchors sit elsewhere (`git show 921ef80:<tool> | grep -nF`):
  - `evidence-disposition.py:532` and `:645`;
  - `registry-check.py:796` and `:108`.
- Grading is unaffected, because `replace_once` (`:257-262`) mutates by a unique byte count, not by line.
- These labels are not revision attribution. `.ufo/waves/round-18/w2/RerunC2After.md:147` already noted stale labels.
- The P05–P07 labels (82, 516, 644) do match `tools/trace-inputs.py` at 921ef80.

**Unknown.**
- **cwd / LANE_ROOT.** Either the live lane or the L1 scratch clone `/tmp/tameshi-r18-L1-final-a2vitd82/fleet/tameshi-shokunin`. The L1 traces record that clone at rev 921ef80 (e.g. `coldread/traces/L1/bash-witness.json:35-37`, `before.json:39-41`).
- Probes are deliberately untraced, because nested ptrace makes P05–P07 error (`.ufo/waves/round-18/w2/CR50.md:106`).
- Interpreter, bwrap and jj versions are not recorded.
- Fleet siblings are linked live (`:297-307`). P11's kagi input is pinned at `fecee874…` (`:831`).

## 4. Failed raw attempt vs current evidence

| Retained receipt | Ruler | Rev | Exit | Summary | Class |
|---|---|---|---|---|---|
| `c2-probes-183f87b.txt` | v1 | 183f87b | 0 | open=11 | v1 base, historical |
| `c2-probes-e08271a.txt` | v1 | e08271a | **2** | `could-not-evaluate (3 probe error(s))` — P01, P02, P08 | **failed raw attempt**, retained |
| `c2-probes-v2-183f87b.txt` | v2 | 183f87b | 0 | open=11 | effective base |
| `c2-probes-v2-e08271a.txt` | v2 | e08271a | 0 | closed=11 (46-case registry) | historical tip |
| `final/probes.stdout` + `checks.json#probes` | v2 | 921ef80 | 0 | closed=11 (48-case registry) | **current effective receipt** |

- The traced wave-2 runs also exited 2 (`w2/CR50.md:106` r6; `w2/SentinelProbeEnvelope.md:43`). They exist only in reports and are not receipts in `final/`.
- **This row is not a failed attempt:**
  - exit 0;
  - counts closed=11, open=0, error=0;
  - stderr is empty.
- **Contrast `bash-witness-selftest`:** exit 64 with empty stdout (R18-4). The bundle's nonzero rows are `registry` (1) and `bash-witness-selftest` (64) only.
- **The `FAIL` tokens inside the bytes are kill signals, not attempt failures.**
  - 4 × `SELFTEST: FAIL` (P01–P04) and 3 × `SELFTEST: 29/30` (P05–P07).
  - Each follows `pristine_exit=0 mutant_exit=1` (7/7): the mutant's selftest fails, which is what closes the probe.
  - A grep for `FAIL` must not classify this row as failed.

## 5. Boundary: the round-19 check that consumes this row (advisory)

This section reports a gap in the round-19 measure check. On the present bytes it is not a C1 failure.

**What R18-1 checks.** `round-19/measure.py:89-96` at 21e7932 has ruler sha256 `c538c33d…`, which equals the `ruler_sha256` in `before.json` and `after-21e7932.json`. It checks four things:
- `revision == TOOLS18`;
- `exit` is an integer equal to 0;
- `stdout_sha256 == digest(probes.stdout)`;
- the summary substring is present.

So it can fail against a failed raw attempt: a nonzero exit or a digest mismatch reads `open`.

**What it does not bind.** Neither `argv` (the script path or the `--rev` value) nor `probes.stderr`. A row whose argv graded another commit, while `revision` still read 921ef80, would read `corrected`. The present bytes are consistent (`argv[3] == revision`), so this is not a live defect.

**Uncommitted working copy.** `measure.py` (sha256 `1d275750…`, `:100-109`, mtime 02:56:23) adds the PROBES-in-note and line-2-preserved checks. It still binds neither argv nor stderr.

**Suggested falsifier.** Either of these mutations should reopen R18-1:
- require `old['argv'] == ['python3', '.ufo/evidence/round-18/defect-probes.py', '--rev', TOOLS18]`;
- require the retained `final/probes.stderr` to be `b''` (add that path to `PATHS`).

This complements NegativeControls NC-1 (`.ufo/waves/round-19/w1/NegativeControls.md:25`), which covers the path cited in the erratum, not the row.

## 6. Recommended preserved-history treatment

1. **Keep the files byte-identical:** `final/checks.json` (`fed3c8e6…`), `final/probes.stdout` (`d37c99e3…`) and `final/probes.stderr` (empty).
   - No overwrite, reformat, re-run into these paths, or new keys in `checks.json`.
   - Any change breaks the round-19 `fed3c8e6…` pin and the 34 `probes.stdout` pins in the ledger and traces.
2. **Classify the row as an effective historical receipt:** measured at `921ef807…`, exit 0, `open=0 closed=11 total=11`.
   - No supersession record and no erratum against the row; nothing in it failed.
   - The R18-4 supersession pattern does not apply.
3. **Keep the failed attempt as history.** `c2-probes-e08271a.txt` stays the retained failed raw attempt and is never cited as effective. `c2-probes-v2-*` stay historical.
4. **Cite the row with the full tuple:**
   - `final/checks.json` row `probes` (file sha256 `fed3c8e6…`);
   - argv `python3 .ufo/evidence/round-18/defect-probes.py --rev 921ef807…`, exit 0;
   - stdout `final/probes.stdout`, sha256 `d37c99e3…` (4111 B);
   - stderr `final/probes.stderr`, retained empty (`e3b0c442…`) and not digested by the row;
   - first committed in `5923d89…`;
   - ruler blob `dc6fe875…` (the executed bytes are inferred, not recorded).
5. **Optional disclosure:** append a dated, named note in a round-19 file, never in `checks.json`, listing the four gaps from the Verdict.
6. **Tip statements.** Any statement about the landed tip 4b7c682 or the round-19 tip must be phrased as transfer by byte identity of the lane-tracked probe inputs (empty diff, §3), not as a measurement. A real tip measurement needs a new, separately named receipt.

## Commands run (all read-only) and outcomes

| Command | Outcome |
|---|---|
| `sha256sum`, `wc -c`, `stat` on `final/probes.{stdout,stderr}` and `checks.json` | §1 values |
| `git rev-parse <rev>:<path>` for the ruler and receipts across 9 revisions; `git hash-object` (no `-w`) on the working tree | identical blobs |
| `git log --all -- <ruler/receipts>`; `git log --all --since 18:20 --until 18:45`; `git for-each-ref --points-at` | only `refs/jj/keep/*` snapshots, every one with ruler `dc6fe875…` |
| `git diff --stat` on the probe-input paths: 921ef80 vs 4b7c682/7243e7f/21e7932; e08271a/01d586d vs 921ef80 | empty; and only `registry-check.py`/`registry.json` (plus the ruler for e08271a) |
| `git merge-base --is-ancestor`, three times | true each time |
| `diff` of `c2-probes-v2-e08271a.txt` lines 1–12 against `final/probes.stdout` | lines 1–4, 8 and 11 differ (temp names, 46→48 cases, P08 ids, P11 sha) |
| `grep -c` for status, kill and FAIL tokens | closed 11, open 0, error 0; kills 7; `FAIL` 4; `29/30` 3 |
| `git show <rev>:<tool> \| grep -nF <anchor>` at 921ef80 and 183f87b | the line numbers in §3 |
| `python3 -c` with `json.load(final/checks.json)` | row keys; nonzero rows `registry` and `bash-witness-selftest` |

Static reads:
- `defect-probes.py:1-113, 274-359, 457-503, 808-963, 1021-1087`;
- `round-19/measure.py`, committed and working copy;
- `corpus/knowledge/guard-kill-closure.md:1-3, 171-190`;
- verifier spot-check §5.

## Process disclosure

- One `git status --porcelain -- .ufo/evidence/round-18/` ran without `--no-optional-locks`. Its output was empty.
- `.git/index` now has mtime 02:50:01.93-03:00. That falls inside this seat's run window: round-19 `frozen-runs.json` (mtime 02:49:32) showed as "just now" in a listing one batch earlier.
- [INFERENCE] That call may have opportunistically refreshed git's index stat cache.
- This seat changed no index entries, refs, jj state or tracked bytes. No other command wrote anything.
