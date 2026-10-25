# ExecC2Control — C2 census counter, `--control` mode (v2 patterns vs the v3 fixtures)

Seat: `L1Tameshi41.ExecC2Control` (read-only). Lane checkout not modified; only this report written.

## Exact command

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/census/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --control
```

## stdout (verbatim, single line)

```
C2_R41_CONTROL: v2_var_expected=0 v2_symlink_sites=0 C2_R41_CONTROL_PASS=false
```

## exit code (verbatim)

```
1
```

(measured as `EXIT=1`, appended by the harness after `; echo "EXIT=$?"`)

## Why exit 1 here is the declared control result, not a harness fault

`--control` is a discriminator, not a pass gate. `.ufo/evidence/round-41/census/measure.py:101-110`
computes `meets = var_expected == TARGET['var_expected'] and symlink_sites == 0`; `TARGET['var_expected']`
is `1` (`measure.py:50`), while v2 scores `0`. So `C2_R41_CONTROL_PASS=false` / exit 1 is exactly the
value the contract pins under `claims.C2.do_nothing_control`:

> "the embedded v2 patterns score v2_var_expected=0 v2_symlink_sites=0 on the same planted fixtures
> (C2_R41_CONTROL_PASS=false)"

A gate that reads a non-zero exit from `--control` as "harness broken" would misread a frozen, correct
result. Only `--rev <measurement>` default mode carries `C2_R41_PASS`.

## Why v2's patterns cannot reach the v3 target on the same fixtures (two sentences)

v2 decides per physical line — `tools/write-path-census-v2.py:32-42` requires `WRITE_RE` **and**
`EXPECTED_RE` to hit the same `line` from `text.splitlines()` (`:36`, `:40`) — so on
`.ufo/evidence/round-41/census/fixtures.json` `var_unflagged` the expected token
`"expected.json"` sits on line 4 inside `dest = os.path.join(root, "fixtures", "expected.json")`
while the write `os.replace(dest, ...)` is on line 5, and v2 records the site with 0 expected-value
destinations; and v2's write alternation (`tools/write-path-census-v2.py:16-22`) contains no
`os.symlink` branch at all, so `symlink_unflagged` scores 0 sites by construction — both counts are
structurally pinned at 0 while `TARGET` (`measure.py:48-55`) demands `var_expected=1`, which no
same-line literal regex can supply without becoming v3's multi-hop resolver.

The control path exercises exactly this: `v2_fixture_misses` (`measure.py:88-99`) applies the
counter's embedded copies of v2's regexes (`V2_WRITE_RE` `measure.py:37-43`, `V2_EXPECTED_RE`
`measure.py:44-46`) line by line, conjoining both per line at `:92` and counting write sites alone at
`:96`.

Mechanism, in one place:

| Fixture class | Where the evidence is | v2 score | v3 target |
|---|---|---|---|
| `var_unflagged` | token on `fixtures.json` line 4, write on line 5 | `v2_var_expected=0` | `var_expected=1` (`measure.py:50`) |
| `symlink_unflagged` | `os.symlink(` — absent from `WRITE_RE` (`write-path-census-v2.py:16-22`) | `v2_symlink_sites=0` | `symlink_expected=1` (`measure.py:52`) |
| `literal_unflagged` (pre-integration fixture; see addendum) | literal inside a multi-line `os.replace(` call | not scored by v2 | `literal_unflagged=1` (`measure.py:53`) |

## Retained evidence (re-checked in this seat, not asserted)

| Check | Command | Result |
|---|---|---|
| counter pin matches contract `claims.C2.counter_sha256` | `sha256sum .ufo/evidence/round-41/census/measure.py` | `5d57c7097fb33a66d11cb19b834dd7f92ade268c56562c8a34d7a94bf64ef696` — identical to the frozen pin |
| fixtures pin matches contract `claims.C2.fixtures_sha256` | `sha256sum .ufo/evidence/round-41/census/fixtures.json` | `a4123ce373447563a93ad86c21cc3344f5448f1c6157ba696a7239569a58dc31` — identical to the frozen pin |
| v3 tool (working tree) matches `tool_sha256` | `sha256sum tools/write-path-census-v3.py` | `095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279` — identical |
| v3 tool at freeze `d4ee4e63` | `git show d4ee4e63…:tools/write-path-census-v3.py \| sha256sum` | `095924a7a165…` — identical, so the working tree carries the frozen blob |
| v2 tool matches `v2_sha256` at freeze | `git show d4ee4e63…:tools/write-path-census-v2.py \| sha256sum` | `4022853295882c5a11e192274e9215ea5a008e54eb0a2f77a8a2365f522d878b` — identical |
| live variable site | `tools/repeat-control.py:808` (`duplicate_path = os.path.join(tamper_duplicate_key, "expected.json")`) + `:811` (`with open(duplicate_path, "wb") as handle:`) | token and write on different lines → `live_var_expected_v2=0` as the predicate requires |
| live symlink site | `tools/repeat-control.py:820-823` (`os.symlink(` with its arguments on the following lines) | no `os.symlink` in v2's `WRITE_RE` → `live_symlink_sites_v2=0` |
| lane tree untouched by this seat | `git status --porcelain` | `?? .ufo/evidence/round-41/sources/`, `?? .ufo/waves/round-41/`, `?? corpus/knowledge/r41-variable-destination-writes.md` — all sibling artefacts; nothing written by this seat except this report |

Contract file read-only per instruction and never edited: `.ufo/evidence/round-41/contract.json`.

## Post-integration addendum — the lane advanced after this run

The lane moved from the freeze `d4ee4e63a0a4402bd8628fbc80f06bbd8f37d937` to `b37ce974b6efb8c465626d7346149549a3300a4b`
("round-41: C1 records reconciliation + C2 write-path-census-v3 … amendments A1-A4") after the run above.
A reader comparing the pins in this report against the current tree would otherwise see a bare mismatch, so
both states are recorded here.

| State | counter sha256 | fixtures sha256 | v3 tool sha256 | `--control` stdout | exit |
|---|---|---|---|---|---|
| A — freeze `d4ee4e63`, what this report measured at 03:38 | `5d57c709…ef696` | `a4123ce3…8dc31` | `095924a7…f279` | `C2_R41_CONTROL: v2_var_expected=0 v2_symlink_sites=0 C2_R41_CONTROL_PASS=false` | `1` |
| B — `b37ce97` / current worktree, re-measured | `83268eff…ce94c` | `20b6254d…26329` | `095924a7…f279` (unchanged) | `C2_R41_CONTROL: v2_var_expected=0 v2_symlink_sites=0 C2_R41_CONTROL_PASS=false` | `1` |

The control value is identical in both states, so no conclusion in this report turns on which one is read.
State B was measured with the same command plus `--control` only; no default-mode run was performed.

What the integration changed in the C2 inputs (`git diff d4ee4e63 HEAD -- .ufo/evidence/round-41/census/`):

- `census/measure.py` +5 lines: a third recognizer-removal mutant `symlink_arg`
  (`ARG_MARK = "            return 'os.symlink', [node.args[1]]"` → `[node.args[0]]`), asserting v3 takes
  the **link destination** argument, not the link name; wired into `killed` and into the `ok` conjunction.
- `census/fixtures.json`, `symlink_unflagged`: `root = "tests/golden"` → `root = "tests/fixtures"`, removing
  the literal `golden` that v2's `EXPECTED_RE` also matches (`tools/write-path-census-v2.py:23-25`) — the
  confound is gone, and v2 still scores 0 sites because its write alternation has no `os.symlink` at all.
- `census/fixtures.json`, `literal_unflagged`: rewritten from
  `os.replace(join("tests","expected.json"), join("tests","actual.json"))` to
  `root = "tests/fixtures"` / `os.replace(join(root,"actual.json"), join(root,"expected.json"))`. The old
  fixture placed the expected token in `args[0]`, which v3 reads as the **source**
  (`tools/write-path-census-v3.py:131-134` returns `[node.args[1], node.args[0]]`), so the pre-integration
  fixture was semantically inverted; the new one puts `expected.json` in the destination slot and off the
  write line, which makes it a resolution test rather than a same-line literal test.
- `contract.json`: C2 pins updated to state B (`counter_sha256 83268eff…`, `fixtures_sha256 20b6254d…`),
  amendments A1-A4 committed, A5 present only in the worktree.

Recomputed v2 same-line hits on the state-B fixtures (both regexes applied per physical line, as
`measure.py:88-99` does): `var_unflagged` 0, `symlink_unflagged` 0, `literal_unflagged` 0,
`scratch_var` 0 — the amendment tightens the fixtures without loosening the gap this report describes.

The integration commit also carries `.ufo/evidence/round-41/control/c2-control.{stdout,exit}` holding
exactly the state-B line above with `1`; this seat's independent re-run reproduced it byte-for-byte.

## Scope discipline

- Only `--control` was executed — twice: once against state A (freeze) and once against state B (the
  post-integration worktree), both recorded verbatim in the addendum. No default-mode run of either
  counter was performed at any revision, and no `--rev work` run was made; the single deciding run
  belongs to the L1.
- No `--selftest` run here; that belongs to `L1Tameshi41.ExecV3Selftest`.
- No file in the lane checkout, no jj state, no Git index touched. The `M .ufo/evidence/round-41/contract.json`
  and `?? .ufo/evidence/round-41/after/` entries now in `git status` are other seats' work, not this seat's.

## Tooling

No install or update performed (nothing needed; `python3` and `git` already present). pacman
transactions untouched per the host-wide pause.

## Risks / blockers

None. One documentation-level hazard worth the L1's attention: `--control` exiting 1 with
`C2_R41_CONTROL_PASS=false` is the frozen, correct discriminator value, and must not be quoted as a
failed control when the measurement run is scored.

Report: .ufo/waves/round-41/w1/ExecC2Control.md
