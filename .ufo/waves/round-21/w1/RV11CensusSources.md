# RV11 — Source census and row-shape baseline

**Verdict: done — AGREE.** Both commands run on REV=33d03b716d3edcf1d8656d46d6df61801d232c52 reproduce the frozen round-21 baselines exactly; no defect found.

## Commands run (exact) and exits

1. Fleet census validate (exact argv as assigned; read-only over the fleet):
   ```sh
   /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi
   ```
   - exit **0** (`census-now.exit`), stderr empty.
   - stdout (tabs shown as `^I`): 6× `tameshi  W04  <id> duplicate url … across scopes` for S047, S048, S075, S076, S077, S078, then `tameshi  ok  /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md`. No E-codes.
   - `cmp /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-21/census-start.stdout census-now.stdout` → **IDENTICAL** (byte-for-byte; baseline file shows the same lines with tabs rendered as spaces). `census-start.exit` = `exit=0` matches.

2. Row-count command from `/home/vgpnk/Projects/shokunin/.ufo/reports/round-20/tameshi.md:84-86` (the `git show "$REV:corpus/SOURCES.md" | python3 -c …` block) with `REV=33d03b716d3edcf1d8656d46d6df61801d232c52`, run in the lane repo (read-only `git show`):
   - stdout: `{"rows": 76, "status": {"mined": 48, "queued": 23, "rejected": 5}, "tiers": {"A": 67, "B": 7, "C": 2}}`, exit **0**.
   - Matches `.ufo/evidence/round-21/sources-before.json` (`rows: 76, tiers A67/B7/C2, status mined48/queued23/rejected5, malformed: 0, exit: 0`) field-for-field.

## Baseline comparability across revs (evidence)

- Lane HEAD verified = `33d03b716d3edcf1d8656d46d6df61801d232c52` (`git rev-parse HEAD`). `sources-before.json` was recorded at `08175c62d661fddf052ed10abc91313dec8eb77d`; `git diff --stat 08175c6… 33d03b7… -- corpus/SOURCES.md scripts/sources-census.sh` is **empty** (the 18-file +1135 delta between the revs touches only `.ufo/evidence/round-21/*`, `SCORECARD.md`, `tools/wave-route-mix.py`), so the two baselines measure identical census inputs.
- Working tree is clean for everything the census reads: `git status --porcelain` shows only `M LOG.md` and untracked `.ufo/*` files. `sha256sum corpus/SOURCES.md` = `9715f44dca8dfc2beac94b17e19f0f0206b1efa4d973eb1183650a0f9179794f` and `git show 33d03b7…:corpus/SOURCES.md | sha256sum` = same → working tree == pinned rev blob.

## Independent cross-check (not just re-running the frozen tool)

Ad-hoc python parse of the working-tree registry: **76 rows, all inside `## Registry` (0 row-shaped lines outside), 0 malformed (NF=11), 76 unique ids spanning S001–S078 (two id gaps, no duplicates), tiers A67/B7/C2, statuses mined48/queued23/rejected5.** Agrees with both the census tool and the row-count command. The 6 W04 duplicate-url warnings (S047/S048 same pitest.org quickstart URL; S075–S078 man-page/jj-doc URLs) are warnings only and do not affect the clean exit, consistent with SOURCES-CONTRACT-v1.

## Disagreements / defects

None. C1/C2 frozen rulers' source-population premise (76 rows, 0 malformed) holds at the round-21 frozen base.

## Artifacts

- Scratch (mine, disposable): `/tmp/tameshi-r21-RV11CensusSources-1/out/{census-now.exit,census-now.stdout,census-now.stderr}`
- Baselines compared: `.ufo/evidence/round-21/census-start.{exit,stdout,stderr}` (stderr empty), `.ufo/evidence/round-21/sources-before.json`
- No tool installs performed (none needed). No writes outside this report and scratch. No git/jj mutating commands; only `rev-parse`, `status --porcelain`, `show`, `diff --stat` (read-only).
