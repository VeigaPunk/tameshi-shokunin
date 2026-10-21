verdict: blocked

# Section 131–245 — mutation-sweep recipe

## Blocking findings

1. **`--selftest` is not an unconditional hermeticity guarantee** — `SKILL.md:138–145`. The Kagi citation at `mutation-case-kagi-census.md:24–26` proves only that the verify/shape fixtures use a temporary root. The same note explains the omitted host-gated branch: on the measured host, two verb cases skipped because `the-janitor` was absent (`:27–35`); on a handler-present host they execute the real binary and become host-dependent (`:36–38`). The recorded round-3 run was hermetic on its observed host, but the section must not let readers infer hermeticity from the flag alone. Require proving the actual run has no host/live effects, or record the host-gated branch as excluded/controlled.

2. **The Kagi 16-case denominator is mislabeled as executed cases** — `SKILL.md:141–148` (and the full-count language at `:192–194`). The cited source explicitly says the total is 14 `ok-case` executions plus two `skip-case` entries that performed no execution (`mutation-case-kagi-census.md:33–35`). Thus `SELFTEST: PASS (16 cases)` is a 16-case enumerated count including skips, not 16 executed cases. Keep the enumerated denominator and executed/skipped counts distinct; otherwise the recipe overstates coverage.

## Non-blocking citation and scope corrections

- **Step 6 metadata citation is overbroad** (`SKILL.md:184–187`): Kimi `mutation-case-kimi-census.md:26–28` says full stdout, exit code, mutant SHA and aggregate results; it does not establish combined output or per-mutant duration/summary. Kagi `:48–49` does. If the added fields are requirements for future runs, label them as such rather than implying both historical records did them.
- **Cost citation ranges need correction** (`SKILL.md:240–244`): Kimi `:204–205` is its U5 host/version limitation, not the 7.0 s / 11-run result; that measurement and 300 s bound are at `:29–31` (Node v24.21.0 is at `:20–21`). Kagi `:50–53` supports its 11.0 s / 280 s numbers, while its U5 host-stability statement is at `:203–204` and is not cited by the section's final “U5 each.”
- **The no-op-driver historical claim lacks an anchor** (`SKILL.md:175–177`): cited Kimi `:22–25` documents the uniqueness gate, not `new != old` or the quoted “replacement was a no-op” assertion. The later current driver contract (`SKILL.md:557–563`) states `new != old`, but does not independently establish what the round-2 driver did. I could not locate original round-2 driver source in the opened repository evidence.
- The cold-read record previously identified no literal target path, no supplied driver implementation, and an undefined scratch `<n>` as minor reader inferences, not blockers (`CR04a.md:95–115`; `CR04b.md:134–147`). The two cold-read executions themselves are supported: current `SKILL.md:1707–1726` cites CR04a/b, whose reports document end-to-end runs (`CR04a.md:14–36`; `CR04b.md:16–71`).

## Historical claims and revision boundary

Round-2 Kimi's 43/43 control and 8/10 mutation result, and round-3 Kagi's 16-case control and 8/10 result, are accurate for their dated pinned records (`mutation-case-kimi-census.md:13–35, 41–53`; `mutation-case-kagi-census.md:42–56`). They are not portable expected outputs for a changed target. CR04b reports the later Kimi source at 45/45 and explicitly calls 43/43 the round-2-era value (`CR04b.md:25–35, 115–126`). The dirty-pin warning is also accurate: the G-R2-1 claim-ledger correction is documented in `corpus/README.md:11` and `gates-survey-kagi.md:554–571`.

## Review boundary and verification

- Pinned review revision: `790abd2129f153c13b471e381d454186edbde65e`. `git rev-parse HEAD` returned that revision; `git status --porcelain -- SKILL.md corpus/README.md` was empty.
- `git diff --unified=1 790abd2129f153c13b471e381d454186edbde65e^ 790abd2129f153c13b471e381d454186edbde65e -- SKILL.md` and the corresponding `--stat` returned no output (exit 0): this commit did not change `SKILL.md`; this is a review of the pinned section, not new behavior introduced by that commit.
- LSP status/references/definition/diagnostics unavailable: `read xd://lsp` returned “No such tool”; the mounted-device inventory has no LSP route. Text search was used only to locate evidence; conclusions rely on directly read source lines above.
- No mutation recipe, tests, build, lint, or formatter were run. No installs/upgrades were performed.

.ufo/waves/round-21/w2/Section0131.md
