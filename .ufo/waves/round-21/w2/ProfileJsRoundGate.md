done

# F5 independent check: `js-round-gate`

## Result

The independent seven-profile run reproduces the producer's `nondeterministic` classification. In both independent sweeps, `clean` and `clean_repeat` have different raw tuples while each run exits 0 and reports `ROUND_GATE_SELFTEST: 60/60 pass` followed by `VERDICT: PASS`. All seven profiles passed; stderr was empty in every run. This is not a uniform usage/setup failure being mislabeled as invariant capability.

Independent evidence: `.ufo/waves/round-21/w2/surfaces/js-round-gate.json`.

## Pin and commands

- Contract SHA-256: `5bd7024d0357ad3fb2a4b8550fd44f8371a3eb004f29948699368bea9d4c2bbd`, matching the producer receipt's `contract_sha256`.
- Materialized the declared pin with `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs` (exit 0). SHA-256 of the actual returned bytes: `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9`, equal to the contract pin.
- Used an independent Python 3.14.8 subprocess harness; it did not invoke/import `tools/env-diff.py` or reuse its helpers. Each profile got a fresh scratch `R`, `home` and `tmp` directories, and the pinned blob as `target.mjs`.
- Executed the specified command for each profile (the child exit is the recorded result):

  ```text
  bwrap --ro-bind / / --dev /dev --proc /proc --tmpfs /tmp --bind R /tmp/w --unshare-net --die-with-parent --chdir /tmp/w node /tmp/w/target.mjs --selftest
  ```

  All seven profile executions returned exit 0. Profile environments were `host` (current invoking environment minus all `GIT_*`), `clean`, fresh `clean_repeat`, `tz`, `locale`, `home`, and `columns`, using the C2 contract's exact overrides. Normalization was none.
- The primary sweep used the invoking `PATH` and resolved Node `v26.12.0`; the recorded producer used Node `v24.21.0` and a different `PATH`. To remove that comparison confound, I also repeated all seven profiles with the producer-recorded `PATH`; this resolved Node `v24.21.0` and exactly matched the producer's recorded clean `PATH`. The additional replay also classified `nondeterministic`, with all seven suites passing.

## Raw stdout SHA-256 comparison

Every listed execution exited 0. For all profiles in both independent sweeps and the producer receipt, the raw stderr SHA-256 was the empty-byte digest `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. The table compares the producer receipt to the independent Node 24.21.0 / producer-PATH replay; each suite reported `60/60 pass` and `VERDICT: PASS`.

| Profile | Producer stdout SHA-256 | Independent Node 24 stdout SHA-256 | Fixture suffix (producer → independent) |
|---|---|---|---|
| host | `f46a8d8730a291cae9ae35c2fe893d864388761393e995264982d5a05bb2d4aa` | `3167aaf2bd30ab4f89f7ac8bef823c2378c3f9465557ec37307279b642bcffcf` | `qgCqM3` → `xGzRKr` |
| clean | `25291d5785187c13582eed7283c50f54c5b41bda37c08cb630ce3d7ed5828c43` | `2f51379212842ae19b259fe34fe9654b76e86bc01284398066f2be8f8ef50c6a` | `VozgDb` → `O0AWhl` |
| clean_repeat | `dc4622235bdc04fed4fc4a1bf5e575e3f5f6e53f9df0d9dfb110ceca6e06a1f9` | `54476beba0c276a63a5708c73440d821d003d13277307622ea9e301b1e1d5bc5` | `30MwHz` → `e2dLUm` |
| tz | `e428399bc3e949b135cd6e4140b27c3a59dcc7ef536cd16628ae2d4f73f6a903` | `e27e2b6b9707a041d1cbc376dfc19ff24c604c3c1f33802a04b4ca58d1296da9` | `nCTFEr` → `YSTK3l` |
| locale | `4a908cb91c934f0f261f4fc405bfb911380000fe66cb1962f2a1c40dd53dd63a` | `2a911ab10821582fa5857bbd0e9f692f48564eed40b565493ae97fc6c4d9ec07` | `mccOMi` → `kkIA7Z` |
| home | `969c9b546a0c4cafcec52cb9c27d3c055d21abc1866333a13edc5a80da055edf` | `49b1d170dae4337023bc21729cfee9611b61968ad6cc9266c3936a8f613e41c9` | `UnOjmv` → `r5bLBT` |
| columns | `11ed4d76be15c70caee866c7454f80d8f0a70a84333b43ad32e314fa782ceccf` | `fef14fdbea93b324f19c5e10903594b6d84f0e931cd3f4b616779a02269ea5b4` | `7Lf48D` → `WUZo80` |

For the Node 24 replay, the decisive raw tuples are:

- producer `clean`: `[0, 25291d5785187c13582eed7283c50f54c5b41bda37c08cb630ce3d7ed5828c43, e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855]`
- producer `clean_repeat`: `[0, dc4622235bdc04fed4fc4a1bf5e575e3f5f6e53f9df0d9dfb110ceca6e06a1f9, e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855]`
- independent `clean`: `[0, 2f51379212842ae19b259fe34fe9654b76e86bc01284398066f2be8f8ef50c6a, e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855]`
- independent `clean_repeat`: `[0, 54476beba0c276a63a5708c73440d821d003d13277307622ea9e301b1e1d5bc5, e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855]`

Thus the clean and repeat tuples differ in both the producer and independent replay, while their exits and suite outcome agree. All per-profile byte hashes, tuple hashes, captured output tails, and scratch paths are in the JSON evidence. The primary Node 26 sweep also had clean/repeat exits 0 and different stdout hashes (`0ac4240fa1d7a82af0bc5e1d56e643f791c657af23301078854f9756602f9584` vs `92731ced903b196b9e3a876cb7ca2f7a3252cfc1b8257af06bf26d7dcede37d6`); its complete seven-profile hashes are recorded there.

## Cause and source anchors

The pinned source imports `mkdtempSync` from `node:fs` and `tmpdir` from `node:os` at `scripts/round-gate.mjs:132-135`; the selftest creates its root with `const tmp = mkdtempSync(join(tmpdir(), 'kumitate-round-gate-selftest-'));` at line 690 of revision `364f1d5954158ef8844bca4a5fef57b05d2f2ca5`. Printed fixture diagnostics include that root, so each fresh execution emits a different suffix (`VozgDb` vs `30MwHz` in the producer; `O0AWhl` vs `e2dLUm` in the matched-runtime replay). With normalization `none`, those path bytes change stdout SHA-256 although all 60 checks pass. This observed random-path change explains the raw nondeterminism; I found no classification or clean-exit disagreement.

The contract pin is at `c2-contract.json:32`; its classification rule at lines 19-22 makes a clean/clean_repeat tuple mismatch `nondeterministic`. The producer's corresponding result is `receipt-final-production.json:613-630`, with class `nondeterministic`, clean and repeat exit 0, and `sensitive_to: []`.

## Verification gaps

The LSP device is not mounted (`read xd://lsp` returned “No such tool”), so no caller/reference/definition/diagnostics queries are claimed. The source-cause statement above is grounded in the pinned source read and the captured runtime paths; the literal search was only used to locate the `mkdtempSync` line. No installs, full batteries, builds, linters, or formatters were run; only this assigned item-specific profile check was executed.