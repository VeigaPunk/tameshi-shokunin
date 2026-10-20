# ReviewAssembleV2Code — `.ufo/evidence/round-17/coldread/assemble.py`

- Rev under review: `eb7838b16490ca7ba17ea3242ade76a61f744af2` (clone `/tmp/tameshi-r17w2-ReviewAssembleV2Code-2-DckMH3/fleet/tameshi-shokunin`, HEAD verified).
- Target hashes at that rev: `assemble.py` `d525c1807d5536983ff7cf154eb9849d24cc6373012720d23ba601a1df508aa3`; consumer `measure.py` `f348adc3d88a7adf98451b366bf7fdef1bafefc94df992961f2595c85a328c89`.
- Scope: trace binding, rejection reasons, grouping (failing entries separate), exempt inputs; plus the consumer contract (`measure.py`) where assemble's output must satisfy it.
- Seat: leaf reviewer, no delegation. No tool installs/upgrades were needed (none performed).

## Commands executed

| # | Command | Exit | Key output |
|---|---|---|---|
| 1 | `git clone -q <lane> $W/fleet/tameshi-shokunin && git checkout -q --detach eb7838b1…` | 0 | `rev-parse HEAD` = `eb7838b16490ca7ba17ea3242ade76a61f744af2` |
| 2 | `python3 .ufo/evidence/round-17/coldread/assemble.py --selftest` | 0 | 59 `[ok]`, last line `SELFTEST: all checks passed` |
| 3 | `python3 /tmp/tameshi-r17w2-.../harness2.py` (adversarial fixtures: own git repo, own reports/receipts, exit codes from the CLI) | 0 | cases below; full log `/tmp/tameshi-r17w2-ReviewAssembleV2Code-2-DckMH3/harness.out` |
| 4 | `assemble.py --reports <always-match report> --repo /nonexistent/repo` | 1 | rejected `read_rev … unresolvable in repo` (not exit 2) |
| 5 | `assemble.py --reports work/nomatch-*.md --repo <repo>` | 0 | `ledger written: … (0 entries)` / `coverage: 0/0 buckets covered` / `uncovered buckets: none` |
| 6 | `assemble.py` (no `--reports`) | 2 | argparse usage error |
| 7 | `assemble.py --out /proc/nope/x.json` | 2 | `ERROR: cannot write …` |
| 8 | full-coverage report for the real page, `--expect-skill-sha b1bd20…` | 0 | `coverage: 58/58 buckets covered`, `rejected reports: none` |
| 9 | `measure.py --rev eb7838b1…` (default ledger path) | 0 | `ledger_present False`, `sections_total 58`, `covered 0`, `reasons {"no-ledger": 58}`, `calibration_restraint_score 6` |
| 10 | measure credit-chain calls on adversarial entries (`entry_failure`, `entry_credit_reason`, `input_reason`, `trace_reason`, `entry_reason`) | 0 | outputs in F2/F6 below |

Selftest evidence: `/tmp/tameshi-r17w2-ReviewAssembleV2Code-2-DckMH3/selftest.log` (59 ok, 0 FAIL).

## Findings (severity ordered)

### F1 — HIGH — `read_rev` is not validated when the page sha is already cached (order-dependent bypass)

`assemble.py:673-675`:

```python
page = pages.get(sha)
if page is None:
    if not rev_ok(repo, rev):
```

The `rev_ok` / `resolve_page` checks run only on a cache miss. Any later report that reuses a `skill_sha256` already resolved by an earlier report skips both checks entirely, so an unresolvable (or page-less) `read_rev` is accepted. This contradicts `assemble.py:25` ("An unresolvable read_rev is also a rejection").

Reproduced (harness case 4):

- Order `(valid.md, bogus.md)` with `bogus.read_rev = "1"*40`, same page sha: **exit 0**, `reports_rejected: []`, `read_revs: ["cb0b5265…", "1111111111111111111111111111111111111111"]`; all four `SeatB` entries carry `read_rev=11111111` in the ledger.
- Order `(bogus.md, valid.md)`: **exit 1**, `bogus.md` rejected with `read_rev 1111… unresolvable in repo`.

The same cache also means a report may cite a rev whose tree does not contain the page blob at all; headings are validated against the first-resolving rev's text. Fix: hoist `if not rev_ok(repo, rev): reject` above the `pages.get(sha)` branch (and optionally re-verify `resolve_page(repo, rev, sha)` per rev).

### F2 — HIGH — "trace binding" binds neither the commands nor provenance signals

`load_trace_receipt` (`assemble.py:422-462`, field loop at 445-446) reads only `schema`, `rev`, `inputs`, `external`. `apply_trace_binding` (`assemble.py:511-543`) unions those maps and applies the only command rule at `assemble.py:516-521` (commands non-empty **and** no `traces` → reject). Everything else a real receipt carries is dropped: `argv`, `cwd`, `exit`, `untracked`, `live_lane_reads`, `dropped_home_count` (`trace-inputs.py:7-16`; observed in the real receipt `.ufo/evidence/round-17/coldread/traces/CR02/01-section-hash.json`).

Consequences, each reproduced:

1. **One empty receipt backs arbitrary claimed commands.** Section with `commands_executed=["dd if=/dev/zero of=/dev/null count=1"]` and `traces=["traces/empty.json"]` where the receipt is `{"schema":"tameshi-trace-inputs-v1","rev":<read_rev>,"inputs":{},"external":{}}`: assemble exit 0, entry `commands_executed_count=1`. `measure.entry_failure`, `entry_credit_reason`, `input_reason`, `trace_reason`, `entry_reason` all return `None` at a rev containing the receipt — the entry is fully credited. There is no comparison of receipt `argv`/`exit` to `commands_executed`.
2. **A receipt that self-declares a provenance violation is accepted.** Receipt with `live_lane_reads={"/home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md": …}`: assemble exit 0, `reports_rejected: []`; `measure.trace_reason(...) = None` (measure's trace check inspects only `inputs`/`external` too, `measure.py:382-410`).
3. **A claimed input that is absent from every receipt is accepted and credited.** Report inputs `tools/x.py` (real sha at rev) with the empty receipt above: assemble exit 0; measure's `input_reason` = `None` (measure verifies the sha against the rev's tree, not that the seat read it). Trace/subset checking is one-directional (`receipt.inputs ⊆ entry.inputs`), so "input-keyed credit" proves tree membership, not a read.

This is the sharp edge for C1's "input-keyed credit": the gate is keyed on content hashes at the rev, and the trace layer adds almost no command evidence. Recommended: match `commands_executed` to receipt `argv` (or require one receipt per claimed command and surface `argv`/`exit` in the ledger); reject or flag receipts with non-empty `live_lane_reads`/`untracked`; keep the one-directional union only if the docs say explicitly that per-read provenance is not claimed.

### F3 — MEDIUM — A5 external/lane separation bypass via `repo@rev:path` shape

`assemble.py:496-506`:

```python
if k.startswith("/"):
    real = os.path.realpath(k)
    if real == root or real.startswith(root + os.sep): reject external-input-lane
elif "@" not in k or ":" not in k: reject external-input-shape
```

An absolute lane path suffixed into the `repo@rev:path` shape starts with `/`, so the `@`/`:` shape check is never reached; `realpath()` of the nonexistent composite string is outside the lane root and the key is accepted.

Reproduced (harness case 5):

- `external_inputs = {"/tmp/…/work/repo@cb0b5265:SKILL.md": "a"*64}` → **exit 0**, `reports_rejected: []`.
- Control `external_inputs = {"/tmp/…/work/repo/SKILL.md": "a"*64}` → rejected `external-input-lane:…/SKILL.md`.

Fix: validate shape first; for `repo@rev:path` apply the under-lane realpath check to the `path` component (and require the repo component to be a real path), or reject absolute keys that contain an `@`/`:` shape marker.

### F4 — MEDIUM/HIGH (integration) — assemble accepts trace locations its only consumer rejects; C1's stated measurement cannot pass at the landing rev

- assemble (`assemble.py:414-419`) resolves lane-relative receipts against the **worktree** and takes absolute receipts "as given". measure (`measure.py:382-392`) requires each `traces[]` entry to be a canonical lane-relative blob **at `REV`**; otherwise `trace-missing`.
- Reproduced: absolute receipt in `/tmp`: assemble exit 0, ledger `traces=["/tmp/…/abs-receipt.json"]`; `measure.trace_reason(rev_rec) = 'trace-missing:/tmp/…/abs-receipt.json'`.
- Reproduced: receipt present in the worktree but uncommitted at the rev: assemble exit 0; `measure.trace_reason(rev_rec) = 'trace-missing:traces/uncommitted.json'`.
- Real layout: the wave receipts exist only in the live lane worktree (`…/coldread/traces/CR02/01-section-hash.json` is 930 bytes there), and `git cat-file -e eb7838b1:.ufo/evidence/round-17/coldread/traces/CR02/01-section-hash.json` exits **128**. A clone at the landing rev therefore rejects such a report (`trace-receipt-missing:…CR02/01-section-hash.json`), i.e. assembly must run with `--repo` pointed at the live worktree, or the receipts must be committed before assembly.
- The landing tree also has no `coldread/ledger.json`: `measure.py --rev eb7838b1` prints `ledger_present False`, `58 × no-ledger`, `calibration_restraint_score 6`, `box3_full_page False`. C1's command (`measure.py --rev <landing>` with `box3_full_page true`, score 6→8) is executable only at a rev that contains **both** the ledger and every trace receipt (or with `--ledger-file`, which still validates declared traces per `measure.py:59-64`). [INFERENCE] The L1's intended post-integration commit may be that rev; the landing commit as cited is not.

Fix options: (a) document and enforce "receipts are lane-relative and committed at the measured rev" in assemble (reject absolute/traversal specs, and resolve against `git ls-tree REV` rather than the worktree); or (b) teach measure the same worktree/absolute tolerance. Do not leave the two contracts divergent.

### F5 — MEDIUM — Zero reports exits 0 with an empty ledger (fail-open)

`discover_reports` silently drops non-files/globs with no matches (`assemble.py:634-651`). With no reports and no `--expect-skill-sha`, `_finish` computes `total=0`, prints `coverage: 0/0 buckets covered` and `uncovered buckets: none`, and returns 0.

Reproduced: `assemble.py --reports 'work/nomatch-*.md' --repo <repo>` → exit 0, ledger with 0 entries, no rejection. A typo in a report path is reported as success. `AsmError` (`assemble.py:147`, documented for "repo unusable") is never raised or caught anywhere. A truly unusable `--repo` with a real report also exits 1 (every report rejected `read_rev … unresolvable`), not the documented operational exit 2.

Fix: raise `AsmError` (exit 2) when `report_paths` is empty, and use it for an unusable repo if the docstring's exit-2 contract is intended.

### F6 — LOW — `canonical_path_reason` accepts `.` components that measure rejects

`assemble.py:381-398` rejects `""`, `..`, `.git` components but not `"."`. measure's `canonical_lane_path` (`measure.py:292-306`) rejects `"."`. Reproduced: inputs `{"tools/./x.py": <sha>}` → assemble exit 0, ledger input preserved; `measure.input_reason(...) = 'input-not-blob:tools/./x.py'`. Assemble should reject `"."` too (and the non-UTF-8-encodable keys measure rejects), so a producer-side pass does not become a consumer-side veto.

### F7 — LOW — Falsy non-dict `inputs`/`external_inputs` silently accepted as `{}`

`assemble.py:608-611` (`s.get("inputs") or {}`) and `assemble.py:446` (`data.get(field) or {}`). A report with `"inputs": []` or `"inputs": 0` is loaded as an empty map instead of the documented `non-dict inputs/external_inputs` rejection (docstring lines 28-33). Reproduced: `"inputs": [], "external_inputs": []` → exit 0, no rejection, entry inputs `{}`. Fix: distinguish absent from present-with-wrong-type.

### F8 — LOW — `traces` key removed from entries when empty

`assemble.py:811-812` deletes `entry["traces"]` when empty, although the ledger paragraph (docstring lines 84-87) says every entry carries `read_rev, inputs, external_inputs, traces`. Consumers tolerate absence, but the schema is not uniform. Keep `[]` or state the omission.

### F9 — LOW / residual — exempt set is hardcoded to the default paths

`DROPPED_INPUT_KEYS` (`assemble.py:125-128`) is `("SKILL.md", ".ufo/evidence/round-17/coldread/ledger.json")`. If `resolve_page` finds the page at another path (tree scan, `resolve_page` at 305-323), or the L1 passes `--out` elsewhere, the in-flight page/ledger is not exempt. No bypass is demonstrated (`inputs` are independently verified by measure, and absolute/`..` keys are rejected), but the exemption does not follow the tool's own configuration.

## Verified to hold (executed)

- **Selftest**: exit 0, 59 checks, `SELFTEST: all checks passed` (command 2).
- **Receipt rev mismatch**: `trace-rev-mismatch:traces/oldrev.json: receipt rev 'e08c…' != read_rev cb0b…`, exit 1 (harness case 3).
- **Receipt-vs-receipt conflict**: `trace-conflict:tools/x.py: receipt traces/conf-b.json declares bbbb…, section declares aaaa…`, exit 1 (case 7). Section-vs-receipt conflicts are also covered by the selftest.
- **Commands without any receipt**: rejected `trace-receipt-missing: start=3 ran 1 command(s) without a trace receipt` (observed when the fixture omitted traces; selftest also asserts it).
- **Exempt inputs**: report-side `SKILL.md` + default ledger path dropped and recorded (`inputs_dropped: ['.ufo/evidence/round-17/coldread/ledger.json','SKILL.md']`, case 8a); receipt-side `SKILL.md` dropped (`inputs_dropped: ['SKILL.md']`, case 8b).
- **Fail-closed grouping**: a clean observation and a failing observation with identical inputs stay separate (case 9a: `SeatClean` entry `bg=0` beside `SeatFail` entry `bg=1`); two failing observations with identical inputs merge into one entry with `seats=['FailA','FailB']`, `blocking_gaps=2`, `verdict=gap-blocking`. An entry carrying `executed-ok` + `blocking_gaps=1` is still vetoed by measure (`entry_failure = 'blocking-gaps:1'`), so the group verdict not being escalated does not launder it.
- **Sectionizer parity**: on the real page at `eb7838b1` (sha256 `b1bd20aee58a0bd241e257f69e3610f3b8c2b805b2ebbb18f48b8e3184bf9d09`), `assemble.sectionize` and `measure.sectionize` produce identical `(start, heading, sha256)` for all **58** buckets.
- **Real-scale assembly**: full-coverage report → exit 0, `58/58 buckets covered`, `rejected reports: none`.
- **GIT_\* scrub**: every git subprocess goes through `_git`/`_git_env` (`assemble.py:196-228`); selftest sets `GIT_DIR`/`GIT_WORK_TREE` to a decoy repo and asserts reads resolve to the real repo and the decoy HEAD is untouched.
- **Argparse error → 2**; **unwritable `--out` → 2**; `_meta.reports_rejected` carries one entry per rejected report.
- **By design, not a defect**: claimed inputs not present in any receipt are accepted (harness case 2); measure verifies them against the rev's tree, so the credit remains content-addressed (but see F2).

## Residual risk / verification gaps

- Not run: `measure.py --selftest` (out of scope; other seat). All measure calls above were direct function calls or a single `--rev` run.
- I did not read any seat report or the lane's `SCORECARD.md`/`LOG.md`; the only live-lane file read was receipt `traces/CR02/01-section-hash.json` for its field shape.
- [INFERENCE] The L1 may intend a post-integration commit as C1's "landing"; the claim as written (`--rev <landing>`) fails at `eb7838b1` because neither ledger nor receipts exist there.
- Not exercised: concurrent assemble runs racing on `<out>.tmp`; multi-page (`skill_sha` per page) assemblies beyond the synthetic fixtures.

**Verdict**: I attacked trace binding, rejection reasons, fail-closed grouping, and the exempt-input rule. Grouping, rev-mismatch/conflict rejections, exempt drops, the sectionizer and the selftest hold; but `read_rev` is bypassable behind the page cache (F1), A5 is bypassable via `repo@rev:path` (F3), trace receipts are not bound to commands/provenance and one empty receipt earns full credit (F2), zero reports exits 0 (F5), and assemble's accepted trace locations are rejected by measure, so C1's stated measurement needs the ledger **and** receipts committed at the measured rev (F4). Partial.
