# GateScribe — round 13 evidence scribe (advisory)

Seat: TameshiR13.GateScribe. Read-only. No sibling execution, no gate/probe/selftest run, no commits, no registry or SKILL edits. Tooling: none installed or updated. Reads and hashes only (`sha256sum`, `python3 hashlib`, read-only `git show` / `git rev-parse` / `git ls-tree` / `git cat-file`).

## 1. Landing state at write time

| Item | State |
|---|---|
| `tools/pin-disposition.py` | absent — interface **not** inspected; section 4 is spec-derived only |
| `tools/witness-metadata.py` | absent — interface **not** inspected; section 4 is spec-derived only |
| `.ufo/evidence/round-13/pin-manifest.json` | absent |
| `.ufo/evidence/round-13/witness-metadata.json` | absent |
| `.ufo/evidence/round-13/` | present, holds `before.json`, `claims.json`, `measure.py` (not from this seat; not inspected beyond existence) |
| `.ufo/waves/round-13/w1/` | sibling reports present (`MetadataSchema.md`, `MetadataSelftest.md`, `PinGit.md`, `PinSchema.md`); not read here |
| `git status --short` | `M corpus/SOURCES.md`, `?? .ufo/evidence/round-13/`, `?? .ufo/waves/round-13/` (HEAD `546b371a48a2f6bd1e7dca6ae8aee2a6dc1b0a50`) |

Re-inspect `tools/pin-disposition.py` and `tools/witness-metadata.py` once they land; the registry rows in section 5 must be re-checked against their real `argparse`/exit constants before L1 cites them.

## 2. Root cause of the nested `declaration.kind = null` (historical fact, not rewritten)

- Producer: `tools/bash-witness-study.py:787` inside `build_summary` (`:771-808`):
  `"kind": declaration.get("declared", {}).get("kind")`.
- The frozen top-level `kind` lives at the root of `declaration.json`, not under `declared`. Keys of `declaration.json`: `created_at, declared, disclosure, environment_at_declare, inputs, kind, round, seat, spec_precheck, study`. Keys of `declaration.declared`: `none_rows, path, rows, sha256` only.
- Frozen top-level value (exact): `kind` = `declared-witness mapping (not a blind preregistration)`.
- `disclosure` is read from the correct root (`:788`), so only `kind` is null. Both `summary.json` and `rerun-20261020T035435Z/summary.json` carry `declaration.kind = null` with `disclosure` present.
- Frozen digests (observed now, `sha256sum`; all match `.ufo/evidence/round-12/BashWitness/manifest.json` where listed):

| File | sha256 |
|---|---|
| `BashWitness/summary.json` | `acc01268cb5fb00985be7bf1c6711f6f97131ff20ae0020bbde1819bae4547b9` |
| `BashWitness/declaration.json` | `e8d2024ad13e021c5b7c41a66b881225beb9e0b30190833f0ab2310cf3670901` |
| `BashWitness/declared.tsv` | `0def0d3b370288f58048c7dfb05aec652f9a262664e9f9ce27ae8fad5e6741d3` |
| `BashWitness/manifest.json` | `273ffc39308a6c55bdb1c8f7a86bac9f95886ec470773c99b4d1e2db5b25e1cf` (not listed in its own `files`) |
| `BashWitness/bash-surface-census.spec` | `d2ad3f29ff206cca56a5c2718d53ece9407f74f602909a2203934b8279707741` |
| `BashWitness/pristine.sh` | `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f` |
| `BashWitness/rerun-20261020T035435Z/summary.json` | `6726421fde88e8d2aff4c9d0ff4a4fdce9b1d4651da50b89f2bf29f65a22a5f0` (manifest value) |
| `tools/bash-witness-study.py` (tool that produced summary) | `249d9dcd2dfb410f7e6847989da2cb3ab6ef7dd693b87ec2b9b4d6b193d43f1a` |
| `tools/mutate-and-run.sh` (runner in declaration) | `75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5` |
| `BashWitness/selftest.out` | `2cd01d5271fc017cdea9e5e62a197952a67fd7e676926ce8f97ddb4590ed461c` |

Routed item 3 (`corpus/lessons/round-12-verifier-spotcheck.md:146`): the nested null is to be repaired only through **new** digest-anchored evidence; the frozen declaration and summary bytes stay untouched.

## 3. Pinned recorded legs (six) — read-only verification

Source of truth: `tools/mutate-and-run.sh` (sha `75ed934d…`). Pins `:542-553`; revisions and call sites `:1113-1138`; `regression_case` git materialization `:894-960`.

Re-derived now with `git show <rev>:<path> | sha256sum`: all six equal the recorded pin (`pin_ok=yes`).

| Leg | Repo / path | Pin (`:line`) | Rev (`:line`) | Blob @rev | Mode @rev | HEAD (short) | Worktree vs pin (observed) |
|---|---|---|---|---|---|---|---|
| js-kimi-census | kumitate-shokunin `scripts/kimi-census.mjs` | `83016d45…f426` (`:542`) | `175de6ba…` (`:543`) | `a2bf15c0…84b4` | 100644 | 1770305 | **changed** (`5e8d5913…`) |
| bash-surface-census | kagi-shokunin `corpus/surface-census.sh` | `275d8294…3009` (`:544`) | `fecee874…` (`:545`) | `dcf878b9…dc2c` | 100755 | c2cab35 | unchanged |
| bash-tsukuroi-census | tsukuroi-shokunin `tools/tsukuroi-census.sh` | `084951be…8c5` (`:546`) | `165307fe…` (`:547`) | `dfcf6f59…4106` | 100755 | 9574a18 | **changed** (`d17d32a3…`) |
| bash-mado-verify | mado-shokunin `tools/mado-verify.sh` | `d7edaab4…0e13` (`:548`) | `eead56b2…` (`:549`) | `7ccc601f…5025` | 100755 | 95cbc41 | **changed** (`037b05dc…`) |
| bash-checklist-run | kagi-shokunin `corpus/checklist-run.sh` | `7e5ec98b…76bf` (`:550`) | `fecee874…` (`:551`) | `78f2c45e…98c` | 100755 | c2cab35 | unchanged |
| js-claims-check | kumitate-shokunin `scripts/claims-check.mjs` | `e9a21b44…61f` (`:552`) | `175de6ba…` (`:553`) | `fae4bbcd…2c99` | 100755 | 1770305 | unchanged |

Notes for the probe:
- "Worktree vs pin" above is a content comparison of the working-tree file against the recorded pin only. I did not compute `git rev-parse HEAD:<path>` per leg; the probe must compute HEAD blob itself.
- Full 40-hex revs: `REV_JS=175de6ba2e9e904010411b19cab27e0af9aad3d4`, `REV_BASH=fecee8743e52eb8fb5fbb40782934cb619a1a96e`, `REV_TSUKUROI=165307fe4746a8807b02ec4a7d7ecac0368454a6`, `REV_MADO=eead56b20ad2b28299ae4fa623d52a99b44c743c`, `REV_CHECKLIST=fecee8743e52eb8fb5fbb40782934cb619a1a96e`, `REV_CLAIMS=175de6ba2e9e904010411b19cab27e0af9aad3d4`.
- Modes differ (kimi 100644, others 100755); the runner mirrors 100755→+x. The probe should report mode too.
- Recorded tables (`:554-559`) are not pins; do not treat them as result reuse.

## 4. Spec-derived interface requirements (unverified until files land)

PinProbe (`tools/pin-disposition.py`, probe):
- `--manifest PATH --root FLEET`; six rows; each row: pinned repo/path/rev/pin, HEAD commit + blob, worktree SHA, `content_status ∈ {unchanged, changed, unavailable}`, `result_reuse = not_established` always.
- exit 0 = observations emitted (including drift); exit 2 = could-not-evaluate (invalid manifest, missing repo/path/blob, malformed digest, duplicate leg). Recommend exit 64 for usage errors to match `repeat-control.py` and `bash-witness-study.py` (both use 64; argparse default 2 would collide with could-not-evaluate).
- `--selftest` must use isolated fixtures and literal expected labels: unchanged, changed HEAD, dirty worktree, missing file/repo/blob, malformed digest, duplicate leg.

MetadataRepair (`tools/witness-metadata.py`, gate):
- `--check` (default live-read inside lane; no external writes); exit 0 `metadata_consistent`, 1 `metadata_inconsistent`, 2 `input_unavailable` or `snapshot_tampered`. Recommend 64 for usage, same reason as above.
- Writes only `.ufo/evidence/round-13/witness-metadata.json`; original frozen bytes untouched.
- `--selftest` expected literal IDs/exits: old null red, corrected companion green, tamper, wrong kind, absent disclosure, malformed JSON.
- Normalized kind must be derived from the frozen top-level `kind` (`declaration.json:kind`), not invented; the nested null stays as historical fact.

## 5. Registry row requirements (drafts for main to integrate; not written)

Target: `SKILL.md` `### Gate/probe registry` (`:1499-1503`), 8 columns: `Name | Kind | Entry command | Verdict map | Self-test command | Pinned values | Write scope | Owner`. Main owns SKILL.md.

Draft row A (probe):
`| recorded-leg pin disposition | probe | \`python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin\` | 0 observations emitted (drift included; result_reuse not_established); 2 could-not-evaluate; 64 usage | \`python3 tools/pin-disposition.py --selftest\` | six pins at \`tools/mutate-and-run.sh:542-553\` (sha \`75ed934d…adc5\`), revs \`:543,:545,:547,:549,:551,:553\`; manifest \`.ufo/evidence/round-13/pin-manifest.json\` (digest to be recorded at landing) | stdout only; manifest is the input; isolated \`/tmp/tameshi-r13-*\` selftest; siblings read-only | tameshi |`

Draft row B (gate):
`| witness companion metadata | gate | \`python3 tools/witness-metadata.py --check\` | 0 metadata_consistent; 1 metadata_inconsistent; 2 input_unavailable / snapshot_tampered; 64 usage | \`python3 tools/witness-metadata.py --selftest\` | frozen inputs: \`.ufo/evidence/round-12/BashWitness/summary.json\` \`acc01268…547b9\`, \`declaration.json\` \`e8d2024a…0901\`, \`declared.tsv\` \`0def0d3b…2741\`; companion \`.ufo/evidence/round-13/witness-metadata.json\` (digest recorded at landing) | companion file only; frozen round-12 bytes untouched; isolated \`/tmp/tameshi-r13-*\` selftest | tameshi |`

Constraints for both rows: no "seventh measured gate" claim; registry scope is round-13 instruments; the metadata gate does not extend the round-12 cold-read or promotion credit (`SKILL.md:1506-1515` already says so for round 12).

## 6. Code maps to mirror (existing conventions; read-only)

`tools/repeat-control.py` (913 lines, stdlib): header contract `:1-111` (interface, precedence, exit IDs); `EXIT_BY_ID` `:122-130`; `usage_failure`/`setup_failure` `:194-203`; `snapshot_mode` `:449`; `selftest()` `:592` with literal expectations; `dispatch` `:870`; `main` `:890` (catch-all so no traceback exits 1). Selftest invoked as `--selftest`.

`tools/bash-witness-study.py` (1629 lines, stdlib): header `:1-92` (modes, exit codes 0/1/2/64, disclosure); constants `:93-118` (`EXIT_OK, EXIT_FAIL, EXIT_CANNOT, EXIT_USAGE = 0, 1, 2, 64`); `Cannot`/`Fail` exceptions `:204-209`; `sha256_file` `:216`; `write_json` tmp+`os.replace` `:765`; `build_summary` `:771` (kind bug at `:787`); `manifest_files`/`write_manifest` `:811-833`; `cmd_declare` `:836`, `cmd_run` `:1000`, `cmd_rerun` `:1008`, `cmd_count` `:1041`, `cmd_check` `:1118`, `cmd_selftest` `:1218`; `UsageParser` (exit 64) `:1570`; `build_parser` `:1578`; `main` `:1613`. Selftest invoked as subcommand `selftest`, not `--selftest`.

Note the two precedents differ (`--selftest` flag vs `selftest` subcommand). The new tools must pick one form and the registry row must spell it exactly.

## 7. Exact checks for L1 (named, NOT executed by this seat)

Run after all seats finish, in this order:
1. `python3 -m py_compile tools/pin-disposition.py tools/witness-metadata.py` — syntax.
2. `python3 tools/pin-disposition.py --selftest` — expect literal labels per PinProbe acceptance; exit 0.
3. `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` — expect six rows, `result_reuse=not_established` on every row, exit 0; cross-check the six pins against section 3.
4. `python3 tools/witness-metadata.py --selftest` — literal IDs/exits incl. old-null red and corrected green.
5. Red-before for companion: run `python3 tools/witness-metadata.py --check` against the frozen round-12 inputs and confirm the nested null is reported (exit 1 metadata_inconsistent or the documented red); then against the new companion (exit 0 metadata_consistent).
6. Frozen-bytes proof: `sha256sum` of the three frozen BashWitness files (section 2) and `tools/bash-witness-study.py` must equal the table values before and after; `git status` must show no modification to `.ufo/evidence/round-12/`.
7. Sibling non-touch: `git status --short -- tools/ .ufo/evidence/round-12/ corpus/knowledge/` ; expect only the two owned tool paths and round-13 outputs.
8. Registry integrity (main, after landing): the two rows in section 5 use the real entry/selftest strings and the real exit constants; no new "seventh gate" claim.
9. `bash tools/mutate-and-run.sh --selftest` and `bash tools/mutate-and-run.sh --regression` — only if L1 decides to re-demonstrate the six-leg ledger; not required by this seat's acceptance. Do not claim PASS without the observed output.

## 8. Findings, open items, and limits

- F1 (root cause, grounded): the `declaration.kind = null` is a key-path error at `tools/bash-witness-study.py:787` (reads `declared.kind`; the value lives at top-level `kind`). Frozen summary bytes must not be edited; repair is companion-only.
- F2 (pin verification, grounded): all six recorded pins re-derive from git blobs at their pinned revisions (`pin_ok=yes` ×6). Worktree content vs pin: **changed** for js-kimi-census, bash-tsukuroi-census, bash-mado-verify; **unchanged** for bash-surface-census, bash-checklist-run, js-claims-check. Probe output must report these as `changed`/`unchanged` per leg, never as fresh or reusable.
- F3 (exit-code collision risk): both new tools' spec'd could-not-evaluate codes (2) collide with argparse's default usage exit. Recommend exit 64 for usage, as in the two precedents.
- F4 (naming drift): precedents use `--selftest` flag (`repeat-control.py`) and `selftest` subcommand (`bash-witness-study.py`). Pick one per tool; registry must match.
- F5 (unknown, not verified): whether `pin-disposition.py` computes HEAD blob via `git rev-parse HEAD:<path>` or `git ls-tree`; and whether the new companion uses `"kind"` at top-level. Verify on landing.
- Limit: no interface of the two new tools was observed; no selftest or gate was executed; no outputs were fabricated. All hashes above are direct reads.
- Scope note (not this seat's to resolve): `corpus/SOURCES.md` has an uncommitted modification and `.ufo/evidence/round-13/` contains files not created by this seat; reported as observed, not inspected further.
