# T54W2Read20 — cold read of `### Round-17 gate/probe registry — re-pin and monitor` at C1

- Section: `### Round-17 gate/probe registry — re-pin and monitor`
- Candidate: `99c3bc88d704566197783f66b211ee0a830e0330` (C1)
- Span: lines 1872..1879 of `SKILL.md` at C1 (reader-section.py prints `start: 1872, end: 1880`, end exclusive)
- `section_sha256`: `309f83283e7518eb00cf7ce4296daf4bf5e80843ff2b3046755eb55d3ba8fb8c`
- Findings: **none** (empty list; empty is a legitimate result)

## Findings

`[]` — no rule anchor failed to resolve at C1, no table cell was stale against the artifact it
cites, and no self-contradiction or run-together token / missing space / duplicate parenthetical
was found in the section.

## Section bytes read (C1, lines 1872..1879)

```
1872 ### Round-17 gate/probe registry — re-pin and monitor
1873 (blank)
1874 | Name | Kind | Command | Exits |
1875 |---|---|---|---|
1876 | `tools/evidence-disposition.py` (v2 manifests) | gate | `python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json` (round 18; the round-17 manifest now exits 2) · `--selftest` | 0 clean · 1 failed expectations · 2 could not evaluate (invalid, missing, tampered or unprovenanced input) · 64 usage |
1877 | `tools/registry-check.py` | gate | `python3 tools/registry-check.py --rev REV [--registry PATH] [--tag TAG] [--json]` · `--selftest` | 0 every active row held · 1 a row differs · 2 registry invalid, rev unresolvable, clone failed, or `--tag` matches no row · 64 usage |
1878 | `tools/mutate-and-run.sh` (guard + scrub) | gate | `bash tools/mutate-and-run.sh --selftest` · `--regression` | as the round-16 row; a borrowed repo identity is SETUP 2 |
1879 | `tools/pin-disposition.py` (branch tip) | probe | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` · `--selftest` | as the round-13 row, plus exit 2 could-not-evaluate when TMPDIR is set and unusable (round 54: the self-test names the value, no traceback) |
```

## Anchor checks performed at C1 (`git cat-file -e` / `git show` on the lane repo)

| Anchor named in the section | Resolves at C1 | Evidence |
|---|---|---|
| `tools/evidence-disposition.py` | yes | `git cat-file -s` → 121640 bytes |
| `tools/registry-check.py` | yes | 71440 bytes |
| `tools/mutate-and-run.sh` | yes | 112407 bytes |
| `tools/pin-disposition.py` | yes | 60312 bytes |
| `.ufo/evidence/round-18/dispositions.json` | yes | 4402 bytes; command exits 0 |
| `.ufo/evidence/round-13/pin-manifest.json` | yes | 2667 bytes; six legs |
| "as the round-16 row" | yes | `### Round-16 gate/probe registry` at C1 line 1832; mutate-and-run row at line 1836 reads `selftest 0 pass / 1 fail; regression 0 PASS · 1 FAIL · 2 SETUP · 64 usage` |
| "as the round-13 row" | yes | `### Round-13 gate/probe registry` at C1 line 1573; pin-disposition row at line 1577 (`0 observations, including changed/unavailable; 2 invalid input/could-not-evaluate`) |

## Stale-cell checks (each cited command run at C1, on a `git clone --shared` copy)

1. Row 1876, `evidence-disposition.py`:
   - `.ufo/evidence/round-18/dispositions.json` → exit **0**, `status: clean`, `effective: 11`, `superseded: 1` (matches the cell "0 clean" and the "round 18" parenthetical).
   - `.ufo/evidence/round-17/dispositions.json` → exit **2**, `status: could_not_evaluate` (the cell's stated "(round 17 manifest now exits 2)" holds).
   - `.ufo/evidence/round-18/dispositions-before.json` → exit **1**, `failed: 1` (the cell's "1 failed expectations" arm is live).
   - `--selftest --json` → exit **64** (the cell's "64 usage" arm is live).
2. Row 1877, `registry-check.py`: usage text at C1 documents exactly `--rev`, `--registry`, `--tag` (repeatable), `--json`, `--selftest` (also `--root`, `--only`, which the cell omits — an abbreviation, not a stale claim). `--tag zzz-nope` → exit **2** with `could-not-evaluate (--tag ['zzz-nope'] selects no registry row)`; unresolvable `--rev deadbeef…` → exit **2**; missing `--registry` path → exit **2**; `--selftest extra` → exit **64**.
3. Row 1878, `mutate-and-run.sh`: `--selftest` → exit **0**, `MUTATE_SELFTEST: 107/107 pass`, `VERDICT: PASS`. The `SETUP 2` identity claim is asserted by the tool's own selftest (`tools/mutate-and-run.sh:1944 st 'repo-identity guard: no-.git dir inside super-repo refused (exit 2)'`), and line 1263 emits `REGRESSION_CASE %s: SETUP (repo_identity_mismatch: ...)`.
4. Row 1879, `pin-disposition.py`: the literal entry command (`--manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin`) → exit **0**, `schema: pin-disposition-v1`, six legs (`js-kimi-census`, `bash-surface-census`, `bash-tsukuroi-census`, `bash-mado-verify`, `bash-checklist-run`, `js-claims-check`), four `changed` / two `unchanged` — consistent with the round-13 row's "0 observations, including changed/unavailable". The round-54 parenthetical is live: with `TMPDIR=/nonexistent/unusable`, `--selftest` → exit **2**, stderr `pin-disposition.py: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '/nonexistent/unusable' (could-not-evaluate)`, no traceback and the value is named.

## Quality scan (QUALITY 104)

- `grep -nP '  |\(\('` over lines 1872..1879 → no output (no double space, no duplicated parenthetical).
- Parentheticals in the section are distinct: `(v2 manifests)`, `(round 18; …)`, `(invalid, missing, tampered or unprovenanced input)`, `(guard + scrub)`, `(branch tip)`.
- Table is well formed: 4 columns in header, separator and every row; no unescaped pipe inside a cell.
- No sentence in the section contradicts another: the "as the round-16/round-13 row" back-references resolve and their exit maps do not conflict with the row-local additions.

## Commands run (all under scratch `HYAKU_SCRATCH=/fast/scratch/hyaku/tameshi-r54/T54W2Read20`)

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/reader-section.py \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  99c3bc88d704566197783f66b211ee0a830e0330 "### Round-17 gate/probe registry — re-pin and monitor"
# -> {"start": 1872, "end": 1880, "section_sha256": "309f8328…fb8c"}

git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 99c3bc88...:SKILL.md | sed -n '1872,1879p'
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 99c3bc88...:SKILL.md | sed -n '1860,1895p' | cat -A   # invisibles
for f in tools/evidence-disposition.py tools/registry-check.py tools/mutate-and-run.sh \
         tools/pin-disposition.py .ufo/evidence/round-18/dispositions.json \
         .ufo/evidence/round-18/dispositions-before.json .ufo/evidence/round-13/pin-manifest.json; do
  git cat-file -e 99c3bc88...:$f && git cat-file -s 99c3bc88...:$f; done

git clone --shared --quiet /home/vgpnk/Projects/shokunin/tameshi-shokunin $S/c1
git -C $S/c1 rev-parse --show-toplevel   # $S/c1 (asserted before any fixture work)
git -C $S/c1 checkout -q 99c3bc88d704566197783f66b211ee0a830e0330

cd $S/c1
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json ; echo $?   # 0
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions.json --json ; echo $?   # 2
python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions-before.json --json ; echo $?  # 1
python3 tools/evidence-disposition.py --selftest --json ; echo $?                                                          # 64
python3 tools/registry-check.py --rev 99c3bc88... --tag zzz-nope --json ; echo $?                                          # 2
python3 tools/registry-check.py --rev deadbeefdeadbeefdeadbeefdeadbeefdeadbeef ; echo $?                                   # 2
python3 tools/registry-check.py --rev 99c3bc88... --registry /nonexistent/reg.json ; echo $?                               # 2
python3 tools/registry-check.py --selftest extra ; echo $?                                                                 # 64
bash tools/mutate-and-run.sh --selftest ; echo $?                                                                          # 0, 107/107
python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin ; echo $?  # 0
TMPDIR=/nonexistent/unusable python3 tools/pin-disposition.py --selftest ; echo $?                                         # 2, names value, no traceback
grep -n "borrowed\|SETUP 2\|identity" tools/mutate-and-run.sh
grep -n "def main\|write_text\|open(.*w\|mkdir\|makedirs" tools/pin-disposition.py   # writes only in selftest (lines >713); normal mode read-only
```

Independent sha recomputation: `sha256("\n".join(lines[1871:1879]))` = `309f83283e7518eb00cf7ce4296daf4bf5e80843ff2b3046755eb55d3ba8fb8c`, confirming the
reader's sha is the exact section bytes with no trailing newline.

## Artifacts opened

- `SKILL.md` at `99c3bc88d704566197783f66b211ee0a830e0330`, lines 1860–1895 (section + neighbours), 1573–1588 (round-13 registry), 1832–1851 (round-16 registry)
- `tools/evidence-disposition.py`, `tools/registry-check.py`, `tools/mutate-and-run.sh`, `tools/pin-disposition.py` at C1 (usage blocks, exit paths, selftest assertions)
- `.ufo/evidence/round-18/dispositions.json`, `.ufo/evidence/round-18/dispositions-before.json`, `.ufo/evidence/round-17/dispositions.json`, `.ufo/evidence/round-13/pin-manifest.json` at C1
- `.ufo/waves/round-54/reader-section.py`

## Notes / limits

- The row-1877 claim "clone failed" was not exercised (needs a broken git transport fixture); the other three exit-2 arms and the 64 arm were reproduced.
- The row-1877 `--rev` full replay (exit 0 "every active row held") was not run: it clones and re-executes the whole registry, and the cell's claim is the verdict map, not a at-C1 pass. No contradiction was observed.
- Read-only on the lane and the fleet root; the only writes are this JSON/MD pair. No tool installs were needed (python3/git present).
