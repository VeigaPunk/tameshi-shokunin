# SiblingImpact — round 18 wave 2

Seat: SiblingImpact. Read-only. Read rev `01d586ddbc5fcd78659557c4e93a6ee8517b87d1` (HEAD, porcelain clean on the five tools). No packages installed.

## Axes

Calibration (primary): separate a path call, a digest that is printed and not compared, and line cites. Operability (monitored): do not turn the printed digest into a gate. Depth: unchanged.

## What the old prefixes are

At tameshi `01d586dd` the working-tree sha256 values differ from every prefix in the ask. Mapping of the prefixes is from tameshi's own round-17 ledger (`.ufo/evidence/round-17/coldread/ledger.json`), not from a sibling pin:

| Prefix | Tool at the pre-move digest | sha256 now (`sha256sum`, exit 0) |
|---|---|---|
| `fb6d86d5` | `tools/mutate-and-run.sh` | `d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b` |
| `0bf9d1d2` | `tools/registry-check.py` | `e072fd3995ca1df1477613f009193e20f3797bc4673ee3045a04afb9927c2899` |
| `f8f05c7a` | `tools/evidence-disposition.py` | `66655a3a692b587fd0a6dc3f2cf0edd766a824eb86280753d0bd57efeecc1f44` |
| `49e9e5e2` | `tools/bash-witness-study.py` | `8dfaa25aa2713635e7363f60effb442a474ba3656d6cf2bb171c0c22432e3a12` |
| `521be955` | `trace-inputs.py` (ledger key `.ufo/evidence/round-17/coldread/trace-inputs.py`) | `tools/trace-inputs.py` = `fb1d81f67551fb04e9e447cbc706ef5cc9cfd5208169004184b24ab15f3f2636` |

`git show 01d586dd:tools/<file> | sha256sum` matched the working tree for all five (exit 0). Last commit that touches the five paths is `58e5d53` (parent on that log: `eb7838b`). Diff `--numstat eb7838b 01d586dd` (exit 0): mutate-and-run.sh `102/28`, registry-check.py `625/31`, evidence-disposition.py `345/23`, bash-witness-study.py `122/23`, trace-inputs.py `999/0`.

## Commands

Fleet-root ripgrep skips `*-shokunin/` because `/home/vgpnk/Projects/shokunin/.gitignore` line 1 is `*-shokunin/`. Each sibling was searched with the path set to that repo.

Pattern A (tool paths, old prefixes, `tameshi-shokunin/tools`): `mutate-and-run|registry-check|evidence-disposition|bash-witness-study|trace-inputs|fb6d86d5|0bf9d1d2|f8f05c7a|49e9e5e2|521be955|tameshi-shokunin/tools`.

Pattern B (old prefixes only), pattern C (`registry-check.py`, `evidence-disposition.py`, `bash-witness-study.py`, `trace-inputs`, and the four prefixes other than `fb6d86d5`), pattern D (`(mutate-and-run.sh|registry-check.py|evidence-disposition.py|bash-witness-study.py|trace-inputs.py):[0-9]`).

The search tool returns matches or "No matches found"; it does not emit a process exit code. Shell checks below do.

```
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE -u GIT_COMMON_DIR \
  git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse HEAD
# exit 0
# HEAD=01d586ddbc5fcd78659557c4e93a6ee8517b87d1
# status --porcelain on the five tools: empty

sha256sum tameshi-shokunin/tools/{mutate-and-run.sh,registry-check.py,evidence-disposition.py,bash-witness-study.py,trace-inputs.py}
# exit 0 — digests in the table above

git diff --numstat eb7838b 01d586dd -- tools/mutate-and-run.sh tools/registry-check.py \
  tools/evidence-disposition.py tools/bash-witness-study.py tools/trace-inputs.py
# exit 0 — numstat above
```

Line text at `eb7838b` vs `01d586dd` was taken with `git show <rev>:<path>` (python, exit 0).

## Route

One sibling executes a moved tool. No sibling compares any of the five old digests.

### mado — path call, digest observed, digest not gated

`mado-shokunin/tools/mado-verify.sh:2245` defaults the harness to `$MADO_R7_FLEET/tameshi-shokunin/tools/mutate-and-run.sh` (`MADO_VERIFY_HARNESS` overrides). `:2150` runs:

```
bash "$REGRESSION_RUNNER" --target "$target" --defects "$spec" --suite "$suite" \
  --workdir "$cwd/sweep" --label "$name"
```

`:2032` sets `HARNESS_SHA_RECORDED='b56c6e57f1b7ae91c85f06ee101d3a348158ab219fae4a16f5d3e6f77fd22bcb'`. `:2257-2258` prints that recorded revision next to the live sha256 and says `provenance, not gated`. Those are the only two uses of `HARNESS_SHA_RECORDED` in the file. The gate's pass/fail compares the derived target pin and the verdict table (`CONTROL: GREEN`, `MUTATE_RESTORE: OK`, killed/flips/inconclusive), not the harness digest.

`fb6d86d5` occurs in exactly 8 mado files (search offset 8: no further files), all receipts or wave notes, each stating the digest is provenance:

- `.ufo/waves/round-18/evidence/w2-gate-regression.txt:4`
- `.ufo/waves/round-18/w3/reports/MadoR18.W3FreshClone.md:234`
- `.ufo/waves/round-18/w3/reports/W3CriticC1Final.md:205`
- `.ufo/waves/round-19/evidence/final/harm/harm-gate-regression.txt:4`
- `.ufo/waves/round-19/evidence/harm/harm-gate-regression.txt:4`
- `.ufo/waves/round-19/w1/reports/GateFreshJj.md:102`
- `.ufo/waves/round-19/w2/reports/RerunGate.md:40` and `:126` (also cites harness `:1307` and `:1835` against digest `fb6d86d5`, not against `d22c4025`)
- `.ufo/waves/round-20/w1/reports/SentinelPause20.md:96`

No mado hit for `0bf9d1d2`, `f8f05c7a`, `49e9e5e2`, `521be955`, `evidence-disposition.py`, `registry-check.py`, or `trace-inputs`.

Sweep flags mado passes are still the runner's sweep options at `tools/mutate-and-run.sh:201-203` (`--workdir`, `--label`, `--timeout` default 300). Hunks `eb7838b..01d586dd` on that file are the eighth-leg comment and ledger rows, help text that adds `js-sources-check` to the `--regression` blurb, a 59-line insertion after an `EOT`, and `run_regression`. Mado's invocation is sweep mode. It does not pass `--regression`. This seat did not run `mado-verify.sh --regression`.

`bash-mado-verify` inside the runner (`mutate-and-run.sh:89`) is the reverse edge: tameshi replays a pinned mado blob. It is not a sibling pin of the runner.

### Line cites this commit moved (notes, not executors)

Compared with `git show eb7838b:<path>` vs `01d586dd`.

| Cite | At `eb7838b` | At `01d586dd` |
|---|---|---|
| tabi `.ufo/waves/round-18/w1/ConnSiblings.md:88` — `tools/registry-check.py:307` "SIGTERM process groups" | `:307` is the docstring of `_kill_group`: `SIGTERM the row's process group, then SIGKILL after a short grace.` | `:307` is `return path` inside `_json_marker_path`. SIGTERM is `_signal_row_processes(..., signal.SIGTERM)` at `tools/registry-check.py:575`. |
| mado `.ufo/waves/round-19/w1/reports/ConnSiblingTripwire.md:19` and `:34` — `tools/mutate-and-run.sh:249-253` git_clean / `GIT_DIR` | `:249-253` is the git_clean comment (function at `:257`) | `:249-252` is the tail of `sha_of`; the comment starts at `:253`; `git_clean()` is at `:262`. |
| same report — `mutate-and-run.sh:1685-1689` repo-identity guard | `:1685` is the selftest comment: a dir with no `.git` inside a super-repo must be refused | `:1685-1686` is the pin-mismatch selftest assert. The guard in the leg engine is `tools/mutate-and-run.sh:1109-1122`. The selftest comment is at `:1758`. |
| same report — `tools/bash-witness-study.py:334-336` | `:334-336` is `materialize_target`'s revision / object-store check | `:333-336` is `git_clean_env` (strip `GIT_*`, set `GIT_CONFIG_GLOBAL=/dev/null`). The post-move lines match the report's "environment-hygiene" wording; the pre-move lines do not. |

These three files are wave notes. Nothing in tabi or mado executes those line numbers.

### Living cite that was already off the sentence it names

`tsukuroi-shokunin/SKILL.md:568` cites `tameshi-shokunin/tools/mutate-and-run.sh:16-21,60` for "the target is never written — sha256 before/after is the restore proof", and pins r4-2 md5 `26a27d352690e64b2396a4aabaf4ddf6` (1001 lines). At `eb7838b`, `:16-21` is already the plan-anchor comment and `:60` is the `--suite` example. At `01d586dd`, `:16` is the new `js-sources-check` sentence, `:18-21` is the same plan anchor, and `:60` is the INCONCLUSIVE exit sentence (`124/126/127`). The restore-proof sentence in the current header is `:35-37`. No tsukuroi script compares `fb6d86d5` or that md5. `tools/tsukuroi-census.sh:2174` is a comment. `corpus/knowledge/memory-arm-mutants-s8.md:23` records an older sha256 `cf41efaa…` and a past `bash tameshi-shokunin/tools/mutate-and-run.sh` recipe (`:82`). That is a corpus record, not a gate.

### Historical cites (same tools, not routes)

- souji `.ufo/waves/round-16/w2/ConnSiblingOverlap2.md:34` and `census/round-16/transcripts/w2/ConnSiblingOverlap2.txt:170` — `mutate-and-run.sh:84-89` as a six-leg anchor. Current `:84-89` is the eight-leg list (`js-kimi-census` through `bash-checklist-run`). The transcript already says the range was revision-specific (`606716f`).
- mado `plans/round-7.plan.md:56` and `plans/round-7-record-draft.md:53,260`; round-13 through round-18 wave reports cite other runner lines (`:63`, `:359-366`, `:394`, `:481-526`, `:1594`). They are round notes. The round-13 `:63` / `:360-364` `@old` description is not re-checked here as a route; the executable contract is the call at `mado-verify.sh:2150`.
- kama `.ufo/waves/round-17/build/advice/ConnectTameshi.md:106` names `tools/mutate-and-run.sh` as outside a bounded read.
- tabi `.ufo/waves/round-13/w1/SiblingOverlap.txt:37-38` lists `tools/mutate-and-run.sh` and `tools/bash-witness-study.py` as tameshi instruments, no sha and no line.
- mado `.ufo/waves/round-17/w1/reports/FleetToolScan.md:96` names `bash-witness-study.py`. `.ufo/waves/round-19/w1/reports/ConnSiblingTripwire.md:19` is the line cite in the table above.

### No route

Pattern A returned no matches in: `mori-shokunin`, `kotodama-shokunin`, `lore-shokunin`, `kengaku-shokunin`, `kake-shokunin`, `kagi-shokunin`, `game-dev-2d-shokunin`, `audio-shokunin`, `kotoba-shokunin` (the only kotoba hit is the prose "registry-check theme" in `.ufo/round-31/scouts/R4.md:16`, not `registry-check.py`), `game-dev-3d-shokunin`, `revenger-shokunin`, `chousa-shokunin`, `tameshi-shokukin`.

Pattern B (`0bf9d1d2|f8f05c7a|49e9e5e2|521be955`) returned no matches in mado, tsukuroi, souji, kaidoku, kama, kasegi. `fb6d86d5` outside mado: no sibling match. Fleet `scripts/`, `templates/`, `.ufo/gates`, `shokunin.conf`, `.tower`: no matches for pattern A. Root search (lanes gitignored) found the old prefixes in no fleet file. `MANIFEST.json:1804` and `:1856` mention `tools/mutate-and-run.sh` / `mutate-and-run --regression` in training notes. `:8256` and `:8646` mention `evidence-disposition` and `bash-witness-study` in the same kind of note. None of those lines contain the five prefixes, and none is a call.

`evidence-disposition.py` and `trace-inputs.py`: no sibling path hit and no sibling prefix hit.

Name collisions, not these tools: `kasegi-shokunin` and `kumitate-shokunin` `registry-check.mjs` / `ops/registry-check.mjs`; kama `.ufo/waves/round-16/build/advice/ReviewSchemaAmbiguity.md:156` "registry-checked". kaidoku cites `tools/repeat-control.py` and `tools/pin-disposition.py` (`.ufo/waves/round-17/w2/ConnSiblingRows.md:29`, `.ufo/waves/round-18/w1/ConnFleetJjPractice.md:86`). Those paths are outside this set.

## Proposed move

Leave `mado-verify.sh` `HARNESS_SHA_RECORDED` at `b56c6e57…`. Do not write `fb6d86d5` or `d22c4025` into it. The route is the path at `:2245` plus the sweep CLI at `:2150`; the digest line is provenance on purpose. Scoring the tool move as "mado sha-pinned" would invent a comparison the gate does not perform, and the next runner edit would turn `--regression` into SETUP.

Calibration note only, for the two cites `58e5d53` invalidated: tabi `ConnSiblings.md:88` should name `registry-check.py:575` for the SIGTERM group signal; mado `ConnSiblingTripwire.md:19` and `:34` should name `mutate-and-run.sh:253-262` for `git_clean` and `:1109-1122` for the repo-identity guard. `bash-witness-study.py:334-336` already lands on `git_clean_env` at this rev. Do not retarget tsukuroi `SKILL.md:568` as if this commit created the mismatch: `:16-21` was already the plan anchor at `eb7838b`. The restore-proof sentence is current `:35-37`.

## Risks

- Mado's next `--regression` will run `d22c4025` bytes while receipts still say `fb6d86d5`. That does not fail the harness line. It can still fail if a sweep verdict line or exit class changed. The hunk list shows the sweep option block unchanged and the behavioral additions on `--regression` / the eighth leg, which this call does not use. Unrun: `bash tools/mado-verify.sh --regression`.
- `ConnSiblingTripwire.md` was written during concurrent rounds ("line numbers are as-read"). `bash-witness-study.py:334-336` matches this rev and does not match `eb7838b`. The mutate-and-run line numbers match `eb7838b` and do not match this rev. The note is a point-in-time reading, not a stable anchor.
- `.jj` object stores were not unpacked. A pin that exists only as an unmaterialized object would not show up. Checked-out text was searched.

## Verification

- Prefix and path searches above, per repo, plus fleet `scripts/`, `templates/`, `.ufo/gates`, `shokunin.conf`, `.tower`, and root `MANIFEST.json`.
- `sha256sum` and `git show 01d586dd:… | sha256sum`, exit 0, digests equal, HEAD `01d586dd`, porcelain empty on the five paths.
- `git diff --numstat eb7838b 01d586dd` on the five paths, exit 0.
- `git show eb7838b` vs `01d586dd` for the cited line ranges, exit 0.
- `fb6d86d5` files_with_matches in mado: 8 files; offset 8 empty.
- `HARNESS_SHA_RECORDED` in `mado-verify.sh`: `:2032` and `:2258` only.

Verdict: partial
