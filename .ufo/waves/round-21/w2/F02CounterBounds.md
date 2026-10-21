done — scoped C2 counter and after-B receipt attack completed; no production files changed.

# F02CounterBounds — C2 counter and receipt review

**Axes:** calibration (primary), evidence integrity. Target commit: `790abd2129f153c13b471e381d454186edbde65e`.

## Verdict

**Agree with the identified counter weaknesses; disagree that the live `c2-after-B.json` / F5 record exhibits them.** The frozen C2 counter can return success for hand-authored profile tuples, including all-seven-profile failures and arbitrary normalization. I reproduced those cases in a private clone. But the committed live F5 receipt is byte-identical to the final production receipt; its instrument and contract hashes match the actual files, every row says `normalization: none`, all nine clean exits are 0, each clean output tail has its selftest pass signal, and its one raw-output nondeterminism is correctly labelled. The actual producer rejects a nonzero clean exit; I confirmed that with a targeted synthetic producer fixture.

This is evidence that this case did not *show* exploitation of those counter weaknesses, not a cryptographic attestation: the receipt format is unsigned, and the counter itself cannot establish that every reported profile tuple came from an actual execution.

## Findings (severity ordered)

### Major — C2 success does not authenticate profile execution or require a clean baseline

`c2-count.py:32-40` validates tuple shape and hash syntax but permits any integer exit. `:43-83` checks pins, a declared normalization string, required profile tuple shape, and classification equality; it never requires `clean.exit == 0` or binds hashes to raw output. `:160-173` then counts all surfaces and gates final success on the separate `env-diff.py --selftest` exit and the source-entry check—not on execution of the nine target profiles. The selftest is for the tool, not a replay of the receipt's surface tuples.

I reproduced this against the frozen counter bytes (`9a34f77d…3520a2`) and frozen contract (`5bd7024d…d4c2bbd`) in a private clone based at `790abd…de65e`, with read-only sibling-repository symlinks and inherited `GIT_*` variables scrubbed. Each fixture changed only the private clone's committed `f5/receipt.json`; real frozen pins, the entry, tool, and contract remained in place. All three invocations also ran the counter's real `--selftest`, which exited 0.

| Private receipt mutation | Fixture revision | Counter result | Concrete implication |
|---|---|---|---|
| All 9 surfaces × all 7 profiles set to `exit: 1`, identical fabricated stdout/stderr digests, `normalization: none`, `invariant`, `sensitive_to: []` | `5c55956af35433c858458e8bd4f64e722ba97121` | exit 0; `classified=9/9`, tool selftest pass, F5 entry true | Uniform failed invocations are accepted as invariant. |
| All 63 profile tuples set to `exit: 0` and the same fabricated digests; no target-profile runs produced them | `8cd1530a0b71ba6041317edcaa79be4608a0b6c1` | exit 0; `classified=9/9`, tool selftest pass, F5 entry true | A valid-shaped receipt does not prove its hashes came from runs. |
| Same fabricated success tuples, but `normalization: erase-all-differences-with-made-up-rule` | `71eb3a6227c47cba8981bff7143e981c7018f57d` | exit 0; `classified=9/9`, tool selftest pass, F5 entry true | Any string is admitted as normalization; the counter does not apply or verify it. |

The synthetic digests were fixed `SHA256("fabricated profile stdout")` and `SHA256("fabricated profile stderr")`; the target surfaces were not executed to produce them. Probe commands and captured results are in `/tmp/tameshi-r21-F02CounterBounds-lg6bb1/probe.py` and `results.json`. This is a concrete counterexample to treating C2 exit 0 as independent proof of executed, successful F5 measurements. It does **not** establish that the actual 790 receipt was fabricated.

### Moderate — the frozen normalization predicate is weaker than the F5 profile protocol

The C2 contract's tuple prose at `.ufo/evidence/round-21/c2-contract.json:18` permits hashes after a declared normalization (possibly `none`), while the required F5 protocol is raw/un-normalized output. The counter checks only `isinstance(normalization, str)` at `c2-count.py:61`. The arbitrary-normalization fixture above was accepted with exit 0. This independently confirms the prior MT2 boundary control (`w1/MT2C2Counter.md:171-180`): its `normalization-not-none` fixture also returned exit 0 and 9/9.

The live receipt is not affected: all nine actual rows explicitly say `none`, and the producer source always emits `normalization: none` (`tools/env-diff.py:110-114`).

## Live 790 receipt: pins, profiles, and classification

`c2-after-B.json:2-20` records the exact counter command at revision `790abd…de65e`, counter exit 0, `classified=9/9`, empty findings for every surface, `tool_selftest.exit=0`, and `f5_entry=true`. Its reported counter and contract hashes match the committed counter and contract hashes.

The actual F5 `receipt.json` and `receipt-final-production.json` are byte-identical (SHA-256 `9c61cc717b3d074f4eca750a1dda4151b10bfbe99f099642aec161027aa85264`); `git show 790abd…de65e:.ufo/evidence/round-21/f5/receipt.json` yields the same digest. Its `instrument_sha256` (`e8b47ab7cf2323764d9e9d3519352cd75e1abda4d5e98e7df602dc23bc099ead`) matches both the checked-in `tools/env-diff.py` bytes and the receipt's recorded producer. Its `contract_sha256` matches the frozen C2 contract (`5bd7024d0357ad3fb2a4b8550fd44f8371a3eb004f29948699368bea9d4c2bbd`). The final receipt records the producer invocation and measurement interval (2026-10-21 12:25:25.257578–12:26:07.396003 UTC).

For each row below, I independently ran `git -C <repo> show <rev>:<path> | sha256sum`; each command exited 0 and its output equalled the receipt pin and, where present, the frozen contract blob hash (`c2-contract.json:25-33`). The `tameshi-runner` contract entry has no preset blob hash, so its receipt pin was compared to the actual blob at its frozen revision.

| Surface | Frozen source (`repo@rev:path`) | Verified SHA-256 |
|---|---|---|
| `tameshi-runner` | `tameshi-shokunin@08175c62d661fddf052ed10abc91313dec8eb77d:tools/mutate-and-run.sh` | `d22c4025e8ce38b8890bedc1eb9eb5f61366c22f4741910bbe5a942582294a8b` |
| `js-kimi-census` | `kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs` | `83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426` |
| `bash-surface-census` | `kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/surface-census.sh` | `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f` |
| `bash-tsukuroi-census` | `tsukuroi-shokunin@165307fe4746a8807b02ec4a7d7ecac0368454a6:tools/tsukuroi-census.sh` | `084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5` |
| `bash-mado-verify` | `mado-shokunin@eead56b20ad2b28299ae4fa623d52a99b44c743c:tools/mado-verify.sh` | `d7edaab4bf108625d213393b77432d7c0104daaa487c801fbc8bba16e32d0e13` |
| `bash-checklist-run` | `kagi-shokunin@fecee8743e52eb8fb5fbb40782934cb619a1a96e:corpus/checklist-run.sh` | `7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf` |
| `js-claims-check` | `kumitate-shokunin@175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/claims-check.mjs` | `e9a21b441f1216bf41d1cca037b36021c581ec7892df3bf973295f9321b0f61b` |
| `js-round-gate` | `kumitate-shokunin@364f1d5954158ef8844bca4a5fef57b05d2f2ca5:scripts/round-gate.mjs` | `f890e277af83a78f2dd265e442c8c5912dc3975a36b18ae1be927022a834d3e9` |
| `js-sources-check` | `kumitate-shokunin@0acb7752d19058b953ebbeba253b1e35f6548de5:scripts/sources-check.mjs` | `6a293a72800123a2a78184e4e67b34a8eeab2e35e15cc0bc353029c9f37e258f` |

A direct receipt query returned: 9 surfaces, exactly 63 profile records, and the exact required key set on every row (`host`, `clean`, `clean_repeat`, `tz`, `locale`, `home`, `columns`); all profile exits are integers; all stdout/stderr digests are lowercase 64-hex; all nine `normalization` values are `none`; all nine clean exits are 0. The C2 output's empty `surface_findings` confirms the frozen checker also accepted each full tuple and classification. Actual result: eight `invariant`, one `nondeterministic` (`js-round-gate`), matching both the receipt and `c2-after-B.json`.

Every clean stdout tail has a selftest pass signal: `MUTATE_SELFTEST: 96/96` (`tameshi-runner`); `KIMI_CENSUS_SELFTEST: 43/43`; `SELFTEST: PASS (16 cases)` (`bash-surface-census`); `TSUKUROI_CENSUS_SELFTEST: PASS (26 cases)`; `MADO_SELFTEST: 28/28 assertions passed`; `CHECKLIST_SELFTEST: PASS (34 cases)`; `CLAIMS_SELFTEST: 39/39`; `ROUND_GATE_SELFTEST: 60/60`; and `SOURCES_SELFTEST: 46/46`. The applicable tails also show `VERDICT: PASS` where those scripts emit that marker.

## Actual producer guard and targeted runtime check

`tools/env-diff.py:57-91` executes the pinned payload as `<interp> /tmp/w/target.<ext> --selftest` in the declared bubblewrap sandbox and hashes captured raw stdout/stderr. `:98-114` returns `unavailable` if a profile has no integer exit or if `clean.exit != 0`, and `probe()` hard-codes `normalization: none`. `:243-245` returns exit 1 if any surface is unavailable. Thus the actual producer cannot generate the counterexample's uniform nonzero-clean `invariant` record through its normal probe path.

I confirmed the path with an item-specific fixture, not a full battery: a private clone based on 790 with a synthetic `tools/f02-clean-fail.sh` that prints `SYNTHETIC_SELFTEST_FAIL` then exits 1. Running the exact producer SHA above against that one-surface fixture executed all seven profiles, recorded exit 1 for each, classified the row `unavailable`, printed `ENVDIFF: classified=0/1`, and exited 1. Driver/receipt: `/tmp/tameshi-r21-F02CounterBounds-lg6bb1/producer-fail.py` and `producer-fail-results.json`; fixture commit `1ee946169e37dce59e829208794f06f352a3c921`.

## Agreement / disagreement with wave-1 reports

- **MT2C2Counter:** agree with its bounded mutation results and its explicit limit that the counter cannot authenticate hashes as executed-profile outputs (`:14`, `:171-180`). My separate private-clone probe independently reproduced fabricated tuples, uniform failed tuples, and non-`none` normalization. The live frozen counter/contract hashes are the same values MT2 measured.
- **RV12F5Definition:** agree that the counter accepts uniform failures and arbitrary normalization (`:19-25`); both were reproduced. Disagree with treating those weaknesses as evidence that this particular receipt used them: the committed production receipt is unnormalized, clean exits are all 0 with pass tails, and the exact producer rejects a failed clean baseline. The producer/receipt evidence remains unsigned, so this is not a cryptographic proof against deliberate fabrication.
- RV12's separate ambiguity about whether the frozen nine surfaces faithfully name F5's intended “six gate selftests,” and its broader source-entry provenance concern, are not resolved by this counter/receipt attack. `9/9` here means the explicit frozen list was covered, not that the population ambiguity is settled.

## Residual risks and verification gaps

- Do not use C2 counter exit 0 alone as evidence that target profiles actually ran or passed: the counterfeit fixture exits 0 even when all 63 tuples are invented or every clean invocation failed. The live receipt is supported here by its committed byte identity, matching producer/contract hashes, pinned blobs, all clean pass tails, and producer behavior—not by the C2 classifier alone.
- This audit validated the receipt and ran targeted counter/producer fixtures; it did **not** rerun all nine surfaces across seven profiles. The stored profile digests are producer-recorded and not independently recomputed from raw full outputs, which are not stored as artifacts.
- `bash-surface-census`'s clean tail reports two verb tests skipped because the handler was absent, despite the suite's `SELFTEST: PASS (16 cases)`. The producer checks exit status, not that every subcase executed.
- Seven specified profiles are not a universal environment-independence claim; the clean repeat is a single repeat and other environments/combinations are untested (RV12 `:27-31`).
- LSP tooling is unavailable in this environment: `read xd://lsp` returned `No such tool: xd://lsp`. No references/definition/diagnostics requests were possible. `grep` was used only to locate producer lines; behavior claims above are from the directly read source ranges.
- No installs, builds, full batteries, or production changes. Exact targeted commands/exits: the nine pin `git show … | sha256sum` calls and checksum queries exited 0; `python3 /tmp/tameshi-r21-F02CounterBounds-lg6bb1/probe.py` exited 0 (all three synthetic C2 invocations exited 0); `python3 /tmp/tameshi-r21-F02CounterBounds-lg6bb1/producer-fail.py` exited 0 as a harness while its nested producer invocation exited 1 as expected; the initial `git rev-parse HEAD` returned the target commit. No verification beyond these item-specific checks is claimed.

Report: `.ufo/waves/round-21/w2/F02CounterBounds.md`
