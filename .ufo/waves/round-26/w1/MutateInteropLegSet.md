# MutateInteropLegSet — round-26 wave 1 (mutation tester)

## Verdict

**6 of 7 mutants KILLED, 1 SURVIVED (coverage finding).** The ninth-leg wiring in
`tools/mte-interop.py` is defended by two independent mechanisms, and both fire:

- the **leg-set guard** (`tools/mte-interop.py:317`, `set(legs) != set(LEG_TABLE) or set(tables) != set(LEG_TABLE)`)
  → refuses with `MTE_INTEROP: SETUP (...)`, exit **2** (M1, M4, M6);
- the **per-mutant verdict comparison** (`tools/mte-interop.py:257`, `per_mutant`) inside `judge()`
  → refuses the leg with `MTE_LEG js-cite-check: FAILS (... per_mutant=mismatch ...)`, exit **1**
  (M2, M3, M5).

The surviving mutant **M7** (weakening the set-equality guard to a count-only comparison) passes the
assigned nine-leg detector unchanged (`MTE_INTEROP: PASS legs_conforming=9/9`, exit 0). That is a
**detector coverage gap, not a production defect**: the committed code already compares sets. The
smallest safe correction is to the *detector suite*, not to the contract or to the tool (see
§5). The one-line probe that closes the gap is given and was run (§4, W1).

## 1. Target and pins

| item | value |
|---|---|
| lane clone | `/tmp/MutateInteropLegSet-r26` (private clone of `/home/vgpnk/Projects/shokunin/tameshi-shokunin`) |
| pinned revision | `a08e85c5d7f899e8a5992e20517edb1a380d79eb` (detached, `git status --porcelain` empty) |
| mutated file | `tools/mte-interop.py`, pristine sha256 `193ea6e32f89016baffe07d41fee17074651e74d4807f7fb70dff2fbe0f72cc4` (471 lines) |
| runner | `tools/mutate-and-run.sh`, sha256 `fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de` |
| mutant trees | `/tmp/mut-M1 … /tmp/mut-M7` (each: mutated `tools/mte-interop.py` + symlinked `tools/vendor`, `tools/mutate-and-run.sh`) |

The mutant file is a real file inside `/tmp/mut-M*/tools/`, because `mte-interop.py:59` derives
`ROOT = Path(__file__).resolve().parents[1]` — a symlinked script would resolve back to the pristine
clone and defeat the mutation. `tools/vendor` and `tools/mutate-and-run.sh` are symlinks
(`ROOT/'tools/...'` is read, not resolved).

Fleet staging (read-only): the runner resolves sibling lanes from its own grandparent directory
(`tools/mutate-and-run.sh:1356`), so a private fleet was staged at
`/tmp/mutate-interop-fleet/` — a copy of this checkout's runner plus **symlinks** to
`kumitate-shokunin`, `kagi-shokunin`, `tsukuroi-shokunin`, `mado-shokunin`. Sibling repos were only
read (`git show <rev>:<path>`); no write command, no `jj` command, in the fleet, the lane, or any
clone.

## 2. Detector (identical for baseline and every mutant)

```
bash /tmp/mutate-interop-fleet/tameshi-shokunin/tools/mutate-and-run.sh --regression --keep \
     --workdir /tmp/mutate-interop-rg > /tmp/mutate-interop-rg/regression.stdout
uv run --no-project --with jsonschema==4.25.1 python3 <script> --check --workdir /tmp/mutate-interop-rg
```

Regression (137 s, exit 0): `REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)`;
nine leg dirs with `results.tsv` and nine `REGRESSION_TABLE` lines; `regression.stdout`
sha256 `07b92720b93777fbfa8ea8aaa67f47465d1542c57c76102680a115386eacbe90`. The ninth leg replays at
the pinned rev `1205c6621a2eccbb8ffceae86d9e7b79a7990b3a`, blob sha256 `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`
(matches the round-26 contract), `REGRESSION_TABLE js-cite-check: match=10/10 recorded-killed=5 measured-killed=5 survived=5 inconclusive=0 flips=0`.

**Baseline** (pristine `tools/mte-interop.py`): nine `MTE_LEG … CONFORMS` lines, `MTE_INTEROP: PASS legs_conforming=9/9`, **exit 0**.
Pristine `--selftest`: `MTE_SELFTEST: 17/17 pass`, exit 0.

## 3. Mutants

Each mutant is a one-hunk edit of the pinned file; the pristine file was never edited (restoration proof in §6).

| id | mutation (hunk) | detector output | exit | verdict |
|---|---|---|---|---|
| M1 | drop `'js-cite-check': 'TABLE_CITECHECK'` from `LEG_TABLE` (line 78) → eight legs | `MTE_INTEROP: SETUP (leg set [... 'js-cite-check' ...] / table set [...] differs from the nine ledger legs [... 8 legs ...])` | 2 | **KILLED** (refused at the leg-set guard) |
| M2 | `'js-cite-check': 'TABLE_CITECHECK'` → `'TABLE_SOURCESCHECK'` | `MTE_LEG js-cite-check: FAILS (schema=ok official_score=50 official_killed=5 official_survived=5 official_invalid=0 recorded=5/10 per_mutant=mismatch failed=per_mutant …)` + `MTE_INTEROP: FAIL legs_conforming=8/9` | 1 | **KILLED** (per-mutant check) |
| M3 | drop the ninth leg **and** weaken the guard to `if not set(LEG_TABLE) <= set(legs) or not set(LEG_TABLE) <= set(tables):` | `MTE_LEG js-cite-check: FAILS (... per_mutant=mismatch failed=per_mutant …)` + `MTE_INTEROP: FAIL legs_conforming=8/9` | 1 | **KILLED** (guard no longer refuses; per-mutant check does) |
| M4 | drop `'js-sources-check': 'TABLE_SOURCESCHECK'` instead → eight legs | `MTE_INTEROP: SETUP (leg set [...] differs from the nine ledger legs [... 8 legs, no js-sources-check ...])` | 2 | **KILLED** (guard; the guard is set-equality, not "ninth-leg"-specific) |
| M5 | `'js-cite-check': 'TABLE_CITECHECK'` → `'TABLE_CITECHECK_MISSING'` (var absent from the runner) | `MTE_LEG js-cite-check: FAILS (... per_mutant=mismatch failed=per_mutant …)` + `MTE_INTEROP: FAIL legs_conforming=8/9` | 1 | **KILLED** (`recorded_verdicts` at line 228 skips the absent var → `verdicts` has no entry → `per_mutant` False) |
| M6 | key typo `'js-cite-check'` → `'js-cite-chek'` (nine entries, one wrong name) | `MTE_INTEROP: SETUP (leg set [... 'js-cite-check' ...] differs from the nine ledger legs [... 'js-cite-chek' ...])` | 2 | **KILLED** (guard) |
| M7 | weaken the guard to `if len(legs) != len(LEG_TABLE) or len(tables) != len(LEG_TABLE):` (set-equality → count-equality) | `MTE_INTEROP: PASS legs_conforming=9/9` | 0 | **SURVIVED** — coverage finding, §5 |

Exact diffs (one hunk each):

```
M1/M4/M6  tools/mte-interop.py:74-78   LEG_TABLE entries
M2/M5    tools/mte-interop.py:78       'js-cite-check' -> wrong TABLE_ var
M3       tools/mte-interop.py:74-78 + :317   LEG_TABLE + guard -> subset test
M7       tools/mte-interop.py:317      set(legs) != set(LEG_TABLE) -> len(legs) != len(LEG_TABLE)
```

### Which mutants are refused, and how

- **Refused before any leg is judged** (exit 2, `MTE_INTEROP: SETUP`, no `MTE_LEG` line printed):
  M1, M4, M6. Cause: `tools/mte-interop.py:317` compares the workdir's leg set and the runner's
  `REGRESSION_TABLE` set against `set(LEG_TABLE)`; a mismatch raises `Setup` and `check()` returns 2
  (`tools/mte-interop.py:322-324`).
- **Refused per leg** (exit 1, `MTE_LEG js-cite-check: FAILS`, `MTE_INTEROP: FAIL legs_conforming=8/9`):
  M2, M3, M5. Cause: the `per_mutant` check at `tools/mte-interop.py:257` compares the emitted
  per-defect statuses with the recorded table named by `LEG_TABLE`; a wrong or absent table name
  leaves no (or the wrong) verdict map for that leg.
- **Not refused**: M7 — the count-only guard accepts the nine-leg workdir and the run passes.

Notable detail from M2: the `ledger` check still passed (`recorded=5/10`, `official_killed=5`,
`official_survived=5` — `TABLE_CITECHECK` and `TABLE_SOURCESCHECK` have the same 5/5 split), so only
the id-level `per_mutant` comparison exposed the wrong table mapping. That is precisely the
"balanced flip" class the check exists for, and it did its job here.

## 4. Closing probe for the survivor (W1)

M7 survives the assigned nine-leg detector because the nine-leg workdir has the same *count* and the
same *membership* as `LEG_TABLE`. A probe with the same count but different membership kills it:

```
cp -a /tmp/mutate-interop-rg /tmp/mutate-interop-rg-renamed
mv /tmp/mutate-interop-rg-renamed/js-cite-check /tmp/mutate-interop-rg-renamed/js-cite-chek
uv run --no-project --with jsonschema==4.25.1 python3 <script> --check --workdir /tmp/mutate-interop-rg-renamed
```

- pristine tool → `MTE_INTEROP: SETUP (leg set [... 'js-cite-chek' ...] differs from the nine ledger legs [... 'js-cite-check' ...])`, exit **2** — the set-equality guard is load-bearing;
- M7 (count-only) → `MTE_LEG js-cite-chek: FAILS (... recorded=None per_mutant=mismatch failed=ledger,per_mutant ...)` + `MTE_INTEROP: FAIL legs_conforming=8/9`, exit **1** — killed, but by the per-leg checks, not by the guard.

## 5. Coverage finding (surviving mutant)

**Finding.** `tools/mte-interop.py:317` is the only place that ties the report to the *named* nine
ledger legs, and no detector in the committed suite exercises it as a leg-set guard:

- `mte-interop.py --selftest` (17/17) only drives `judge()` and `leg_report()`; it never calls
  `check()`, so the `set(legs) != set(LEG_TABLE)` branch has **no negative control**;
- the `--check` detector is only ever run against a well-formed nine-leg workdir, so a weakening of
  set-equality to count-equality (M7) is invisible to it.

**Smallest safe correction (detector suite, not the contract, not the tool's behaviour):** add one
negative control that renames a leg directory in a copied kept workdir (exactly the W1 probe above)
and asserts `MTE_INTEROP: SETUP` / exit 2, next to the existing emitter negative control in
`mte-interop.py:selftest()`. No production file change is implied by M7: the committed bytes already
compare sets, and this report does not propose any change to the nine-leg contract, the runner, or
`mte-interop.py` itself.

## 6. Restoration evidence

- Pristine file untouched: `sha256 /tmp/MutateInteropLegSet-r26/tools/mte-interop.py` =
  `193ea6e32f89016baffe07d41fee17074651e74d4807f7fb70dff2fbe0f72cc4` (identical before and after the
  probe), and `git -C /tmp/MutateInteropLegSet-r26 status --porcelain` is empty at
  `a08e85c5d7f899e8a5992e20517edb1a380d79eb`.
- Every mutant lives in its own scratch tree `/tmp/mut-M*/tools/mte-interop.py`; nothing was written
  into the clone, the lane, or a sibling repo. Mutant hashes:
  M1 `4af6e3941aeb7401b68e193eecef1d59bcb2b1104531e80b6fd4b1ee5a35ae80`,
  M2 `42fd351fe5e335358401370daf9573371f006e3d42d398163a22e6e8ac751341`,
  M3 `b94789171d91e385b01dfbb36f206df2945726917ec0d43950410c135311bff6`,
  M4 `bef4e88f93c7adb97471ae1da690784f17a6cbad2af574d126e09a1de14eff6c`,
  M5 `ad4d0c5fa3857368836e8cf1c0483da0507a7d58ae847833cd482216cefb8710`,
  M6 `f08967a453c5e4831e4036561065e9fc0ac563b41e61f0b290cc7f0d3c7dd505`,
  M7 `163eb0ea6ea3120c0011488e95eebdbc95fe5b9e8e70813c9ace46098eeddb27`.
- The kept regression workdir `/tmp/mutate-interop-rg` (137 s, nine legs, `regression.stdout`
  sha256 `07b92720b93777fbfa8ea8aaa67f47465d1542c57c76102680a115386eacbe90`) and its renamed-leg
  copy `/tmp/mutate-interop-rg-renamed` are left in place for re-verification.

## 7. Tooling

No system package was installed. `jsonschema` 4.25.1 was resolved on demand through the existing
`uv` (PyPI, official index) as `uv run --no-project --with jsonschema==4.25.1 python3 …` — the
tool's own documented invocation (`tools/mte-interop.py:37-38`). `node` v24.21.0, `python3`,
`bash`, `git` and `sha256sum` were already present. No `pacman` transaction, no service restart,
no `jj` command anywhere.
