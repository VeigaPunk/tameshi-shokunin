# ReviewAttribution — audit of the C1 counter's kill-attribution rule

Seat: `L1tameshi35.ReviewAttribution` (leaf reviewer, godspeed). Lane pin at dispatch:
`7da6e076c2e25936a3b60dde2a4080d8f05b7e5b`. Slice: audit the counter's kill attribution
(`kill` rows must fail exactly `['runtime']`) across every public + sealed specimen class,
and verify `diverged_configs` comes from the counter's own behavior oracle, not the tool.

All scratch under `/tmp/r35w2-ReviewAttribution/` (`/fast` was at 99%, 1.7 G free) and a
read-only lane clone at `/fast/scratch/hyaku/tameshi-r35-seats/ReviewAttribution/lane`
(checked out at the dispatch commit; `git status --porcelain` clean throughout).
No installs, no `pacman`, no git mutations, no writes under `/home/vgpnk/Projects/shokunin/`
except this report.

## Apparatus actually audited (the worktree MOVED mid-seat — both snapshots named)

| bytes | sha256 | role |
|---|---|---|
| `tools/mutate-and-run.sh` @ 7da6e07 | `a7d3f2dd…912eb9` | pinned runner (re-verified `git show` blob) |
| `tools/tally-audit-v3.py` @ 7da6e07 | `ef98fc53…5885` | committed tool (A4/A5) |
| `c1-measure.py` @ 7da6e07 | `515b0b1b…f9cc` | committed counter |
| `tools/tally-audit-v3.py` worktree 18:38→19:0x | `ec236de2…b435` → `55601416…a4b` | A7-amended tool (uncommitted) |
| `c1-measure.py` worktree 18:38→19:0x | `b9ee1042…cf15` → `ae56a7a0…4cd4` | A7-amended counter (uncommitted) |

A7→A8 (uncommitted at audit time): LAST-match `local nlegs=` locator + depth-0 `}` end in both
tool and counter; `check_head` non-assignment mention scan; counter `unsafe_block` lexical
safety gate (first `rm -rf`-count, then rescoped to `rm` targets that don't contain `$root`);
`auto_root` switched to real mktemp shape (`/tmp/tameshi-r4-2-regression.` + 6 alnum); counter
`(0,0)` root now `/tmp/tally-audit-explicit`; `behavior()` SystemExit caught → invalid row.
My audited counter/tool copies: `/tmp/r35w2-ReviewAttribution/c1-measure.py` (final snapshot
`53c4a4e7`), `/tmp/r35w2-ReviewAttribution/tool.py` (`55601416`).

## The attribution rule as implemented (`score_copies`, counter :336-356)

```python
row['pass'] = bool(div) and rc == 1 and failed == ['runtime']   # kill
row['pass'] = (not div) and rc == 0                             # accept
```
`failed` = `re.findall(r'^CHECK (\w+) FAIL', out, re.M)` from tool stdout; `div` = configs
where the counter's own `behavior()` tuples differ pristine-vs-copy.

---

## Findings (ranked)

### CRITICAL-1 — stale `TOOL_SHA256` pin: the deciding run fails unconditionally at dispatch head; pin-lag is systemic

Committed counter pins `TOOL_SHA256='da23d3a2…a16f'` (the pre-amendment tool). The tool blob
at `7da6e07` is `ef98fc53…5885`. `tool_sha_ok = tool_sha == TOOL_SHA256` gates `ok`
(counter :424). Receipt — byte-identical counter copy (`git show 7da6e07:…` = `515b0b1b`),
`--work` empty dir, no `--sealed`:

```
python3 c1-committed.py --lane …/lane --rev 7da6e07… --work /tmp/…/wA   # exit 1
C1_R35: mode=deciding tool_present=1 tool_sha=ef98fc5367cdb12c tool_sha_ok=0 runner_sha_ok=1
  pub_kill=5/5 pub_accept=3/3 pub_slots=8 pub_distinct=8 … C1_R35_PASS=false   (receiptA-committed.stdout)
```

Every specimen attributed perfectly and the run still fails **on the pin alone**. Worse, the
discipline lags every amendment: at audit end the worktree counter (`ae56a7a0`) pins
`ef98fc53`, the worktree tool is `55601416`, and the worktree contract's `pins_new` says
`ec236de2` — three live values, none equal at rest. Any commit that lands the tool without
the same-commit counter re-pin records `C1_R35_PASS=false` regardless of the claim's
substance: **the predicate measures the pin, not the behavior**. Fix: derive the constant
mechanically at pin-commit time (or a preflight that fails loud before specimens score).

### CRITICAL-2 — A7's LAST-match locator re-opens the decoy class at the TAIL (mirror of AttackPerIndexParse)

`AttackPerIndexParse` was: prepend a here-doc decoy carrying the pristine block → the audited
span is the decoy. A7 switched to `starts[-1]` — the symmetric construction now works: mutate
the real block, append a dead pristine block after `exit 0` inside `run_regression`.
Expressible as a 2-edit sealed specimen (`/tmp/r35w2-ReviewAttribution/taildecoy-specimen.json`,
materialized bytes sha256 `02c66a4145eee2346b22e45cd3f29c7c8b5c713d0ef9d1b8cd39a0484553458a`):

```json
{"copies":[{"class":"tail-decoy-pass-mask","set":"accept","edits":[
 ["  for st in \"$st_js\" \"$st_kagi\" \"$st_tsu\" \"$st_mado\" \"$st_checklist\" \"$st_claims\" \"$st_roundgate\" \"$st_sourcescheck\" \"$st_citecheck\"; do",
  "  for st in 0 0 0 0 0 0 0 0 0; do", 1],
 ["  exit 0\n}\n\n# ------------------------------------------------------------------ selftest",
  "  exit 0\n<dead verbatim copy of the pristine tally block>\n}\n\n# ------------------------------------------------------------------ selftest", 1]]}]}
```

Proven end to end (`mut/taildecoy-expr.sh`):
- counter `tally_block` audited span = the dead block, **byte-identical** to the pristine
  block (`b2 == b0` printed True); `unsafe_block` → `None` (gate blind, decoy is inert).
- counter oracle: `diverged_configs = []` under all four triples → a `set:"accept"` specimen
  is VALID and passes; as `kill` it is invalid (fail-closed).
- A7 tool: `python3 tool.py --runner mut/taildecoy-expr.sh` → all four checks PASS,
  `TALLY_AUDIT: PASS`, **exit 0**.
- real run: `bash mut/taildecoy-expr.sh --regression` → `REGRESSION: PASS (cases=9 passed=9;
  …) / REGRESSION_WORKDIR: … (removed on PASS)`, **exit 0** — while all 9 legs printed
  `SETUP` (missing fleet repos); pristine exits **2** (`REGRESSION: SETUP … cannot-verify=9`).
  The copy converts a real SETUP into a PASS and deletes the workdir.

The audited span is not the executed span; the fix must require uniqueness, not order
(stricter rule §1-2 below). As ACCEPT this specimen satisfies every counting conjunct — a
false pass of a demonstrably divergent runner.

### CRITICAL-3 — shadow `run_regression()`: first-match extraction vs bash's last-definition-wins

`regression_body`/`tally_block` regex-search the FIRST `run_regression()\s*{`; bash executes
the LAST definition. One edit — insert `run_regression() { printf 'REGRESSION: PASS …\n';
exit 0; }` before `case "$MODE" in` — yields `mut/shadowdef.sh`:
- A7 tool: `TALLY_AUDIT: PASS`, **exit 0** (all checks green; audited first def is pristine).
- real run: `bash mut/shadowdef.sh --regression` → `REGRESSION: PASS (…)` **exit 0** vs
  pristine `SETUP` exit 2. `bash -n` clean.
- counter oracle `div=[]` for the same reason (its extraction is the same first match).
This vector predates A7 and survives it; the claim's "behaviorally identical" ground truth
is extraction-shaped, not execution-shaped, on both axes.

### BOUND-1 — `unsafe_block` invalidates a legitimate kill class: FIXED mid-seat by the third counter snapshot (`53c4a4e7`)

`sealed/workdir-keep-cleanup-nested-config.json` is `set:"kill"` and its divergence *is* a
second `rm -rf "$root"` (added KEEP-dependent cleanup). Under the `ae56a7a0` counter the
gate counted `rm -rf` > 1 → invalid → `ho_invalid=1` → `ok=false`; the interim sealed table
was `kill_pass=3/4 accept_pass=3/3 invalid=1` (`sealed-score.stdout`). The `53c4a4e7`
snapshot rescoped the gate to `rm` targets not containing `$root`; re-scored live:
`UNSAFE` gone, row = `{valid: True, pass: True, failed_checks: ['runtime'], rc: 1,
diverged_configs: ['(1,1)']}` → sealed table is now `kill_pass=4/4 accept_pass=3/3 invalid=0`.
Attribution itself was exact on every one of the seven sealed specimens in both snapshots.

### BOUND-2 — `unsafe_block` is lexically evadable (fails open), still at `53c4a4e7`

- `mut/rootshadow.sh`: block line `local root="$TMPDIR/evade"; mkdir -p "$root"` — reassigns
  `root`, invisible to `^[ \t]*root=` → `unsafe_block` returns `None`, the specimen RUNS, is
  correctly scored `failed=['runtime']` (the block's `rm -rf "$root"` then deletes the evade
  dir and the printed workdir path diverges on every vector). Proven: gate = None; tool
  `runtime FAIL vectors=30316 mismatched=30316`, `TALLY_AUDIT: FAIL`, exit 1.
- Root-write evasions surviving the current regex: `local root=`, `$(true; root=/x)`,
  `declare root=`, `printf -v root`, `${root:=/x}`.
- `rm`-arm evasions surviving the `$root`-substring rescope (proven `unsafe_block` → `None`
  on both at `53c4a4e7`): `rm -rf "$root/../x"` (escapes the root), and `find "$root/../."
  -delete` (not an `rm` token at all). Conversely a benign `rm` naming `$root` anywhere in
  the segment passes — substring match is not target verification.
Safety property fails open in both directions; scoring unaffected → BOUND, but the gate
should not be trusted as the sandbox (confinement, §2 below).

### BOUND-3 — attribution strictness is correct as claim-literal but has three honest consequences

1. **Structural-attributed kills score miss.** `mut/headkill.sh` (insert `st_js=0` after
   `st_js=$?`): tool prints `CHECK head FAIL` (rc=1, `failed=['head']`) → counter row
   `pass=False` — the tool killed it; the claim only pays for runtime kills. Correct per
   the claim text ("failing check exactly `runtime`"), proven live.
2. **Head-region behavioral divergence is oracle-invisible.** The oracle runs the block with
   injected statuses; a head mask (`st_js=0`, `read st_js`) diverges the real runner but
   leaves `div=[]` → invalid. The L1 already excluded `SealKillHeadRead` for exactly this
   (manifest `excluded[]`, "the frozen counter oracle finds NO behavioral divergence (div=-)").
   `head`-failing kills are also unattributable by design — a real coverage bound of the
   "divergent behavior" definition, now partly enforced by A7's `check_head` mention scan.
3. **Refused/broken specimens.** rc=2 (`CannotAudit`) ⇒ `failed=[]`, miss — kills the tool
   *refuses* can never be credited (fail-closed, consistent). One residual hole: A7 wraps
   `behavior()` in try/SystemExit→invalid, but `tally_block(copy_text)` inside `unsafe_block`
   is still unguarded — a specimen with zero `local nlegs=` aborts the whole run
   (`RUN-ABORT-PROVEN SystemExit: SETUP: tally start not found`, demo exit 99) instead of
   becoming an invalid row.

### HYGIENE

- `FREEZE_REV = '__FREEZE_REV__'` is a dead constant (superseded by contract-first-add
  resolution); `run_tool`'s `tmp` arg is unused; `diverged_configs` labels drop the root
  slot (unique triples, so unambiguous).
- `AUTO_ROOT` and `/tmp/tally-audit-explicit` are fixed, shared paths reused across all
  specimens in a run: a stateful specimen could bleed filesystem state into a later
  specimen's oracle run (no current vector; fail-closed direction only — a `!isdir` check
  would *create* divergence). `auto_root`'s exists→makedirs is TOCTOU-trivial.
- Contract drift: `frozen_artifacts.tool_sha256`/`pins_new` already cite `ec236de2` while
  the worktree tool is `55601416` — same pin-lag class as CRITICAL-1, contract-side.

## Proposed stricter rule (the assigned ask)

Keep `failed == ['runtime']` — it is the claim text verbatim and structurally cannot be
satisfied without a real runtime FAIL (see could-not-break). Harden the ground truth:

1. **Unique locator**: reject (invalid) any specimen whose `run_regression` body has
   `len(starts) != 1` — never pick first or last. Same for `run_regression\s*\(` count == 1
   in the whole file (closes CRITICAL-2 and CRITICAL-3 in one stroke).
2. **Parse, don't grep, `unsafe_block`**: flag ANY write to `root`/`auto`/`KEEP` (all
   assignment forms incl. `local`/`declare`/`printf -v`/`read`/`${v:=}`) and any `rm`
   invocation whose argument isn't the literal `"$root"`; better, run `run_block` under a
   confined interpreter (unshare/bwrap tmpfs) so scoring never depends on lexical gates.
3. Wrap `tally_block` in `unsafe_block` with the same SystemExit→invalid handling
   `behavior()` got (closes BOUND-3.3).
4. `tool_sha_ok` preflight that aborts with a named reason before specimen scoring; derive
   `TOOL_SHA256` at commit time (closes CRITICAL-1).
5. Fresh auto root **per specimen row**, not per run (closes the bleed channel in HYGIENE).

## What I attacked vs what stands

- `diverged_configs` honesty: computed solely by the counter's `behavior()`/`diverge()` —
  the tool is only ever a subprocess on the copy file; verified structurally and live
  (`root-keyed-shape6` diverges exactly `[(1,0),(1,1)]` under the 6-alnum `AUTO_ROOT
  /tmp/tameshi-r4-2-regression.KItojY`). **Could not make the oracle consult the tool.**
- `failed` injection: unreachable for credit — `rc==1` required (a fabricated `CHECK
  runtime FAIL` in stdout is never reachable: check names are literal, details are
  %-escaped/`%r`-quoted, `CannotAudit` exits 2 with zero CHECK lines, stderr is never
  parsed). Order can't be permuted (fixed 4-tuple print), names can't be duplicated,
  and a FAIL verdict requires ≥1 real `ok=False`. **Could not forge a `['runtime']`.**
- Full public panel + sealed attribution (receiptA + sealed-score): every kill exactly
  `checks=runtime`, every accept `div=- rc=0`. A4 parity between counter and tool
  (CONFIGS + auto_root shape) verified byte-equivalent at the audited snapshots.
- Sealed provenance gate (A5): manifest `freeze_rev` bound to `contract.json` first-add,
  strict ancestry, `--follow --diff-filter=A` lineage creation, committed-bytes scoring —
  the wave-1 BOUNDs I re-checked at head are closed.
- The two open false-pass axes are both **oracle-scope** defects (audited span ≠ executed
  span), not verdict-parsing defects — the attribution rule itself is honest; it inherits
  the shared extraction blind spot from the tool.

Evidence: `/tmp/r35w2-ReviewAttribution/` — `receiptA-committed.stdout`,
`receiptB-amended.stdout`, `sealed-score.stdout`, `mut-proofs.stdout`,
`mut/{taildecoy-expr,shadowdef,headkill,rootshadow,noextract}.sh`,
`taildecoy-specimen.json`, `counter.diff`, `tool.diff`.
