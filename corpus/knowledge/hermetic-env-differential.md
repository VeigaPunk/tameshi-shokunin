source: S079 — https://reproducible-builds.org/docs/timezones/ §Avoid writing the current timezone, paragraph before the TZ=UTC example; S028 — https://bazel.build/reference/test-encyclopedia §Background and §Purpose of tests; S081 — the same Bazel page, §Role of the test runner normal-completion paragraph (precise replacement for S028's result shorthand). Opened 2026-10-21. Executed evidence: .ufo/evidence/round-21/f5/receipt-initial.json and c2-contract.json.
verified-at: 2026-10-21; nine pinned surfaces executed under seven profiles, clean controls exit0; raw tuple classifications below. This is a finite experiment, not a universal hermeticity certificate.
recheck: python3 tools/env-diff.py --contract .ufo/evidence/round-21/c2-contract.json --out /tmp/tameshi-f5-recheck.json; python3 tools/env-diff.py --selftest. Reopen S079, S028 and S081; compare the located quotes in lessons/round-21.md.
ground: F5 — hermetic environment normalization; finite environment-differential method moves from Frontier to Core. F3 universal determinism and successor freshness remain unclaimed.

# Hermetic environment differential — vary one input, keep the repeat control

## What the experiment asks

Does a pinned selftest's **raw exit/stdout/stderr tuple** change when the
launcher changes a finite, declared environmental input? A passing result
is not proof that the target accesses only declared resources. Bazel S028's
hermeticity definition is stronger than this experiment: declared inputs,
not merely seven observed environmental configurations.

S079 demonstrates explicit TZ as a way to control timezone-dependent tool
output. It supports the controlled-TZ profile, not the claim that every gate
will honor TZ or that every source of nondeterminism has been removed.

## Frozen population and recipes

The nine repo/revision/path pins are in
`.ufo/evidence/round-21/c2-contract.json`; eight SHA-256 pins are the existing
mutation-ledger pins, and the ninth fixes the tameshi runner at08175c6.
No target or sibling repository is modified. The tool materializes each
blob, verifies any declared SHA, and starts the selftest in a fresh bwrap
scratch with a read-only root, private writable `/tmp/w`, and no network.
The interpreter and filesystem outside scratch remain host resources;
this does not isolate kernel/runtime versions or provide a full VM.

| Profile | Environment delta |
|---|---|
| host | inherit invoking environment except all GIT_* variables |
| clean | empty environment plus PATH, private HOME/TMPDIR, LANG=C, LC_ALL=C, TZ=UTC |
| clean_repeat | the same clean values, a second execution in fresh scratch |
| tz | clean, changing only TZ to Pacific/Chatham |
| locale | clean, changing LANG/LC_ALL to en_US.UTF-8 |
| home | clean, changing HOME to /nonexistent |
| columns | clean, adding COLUMNS=20, LINES=5, TERM=dumb |

PATH remains a declared host dependency, not a pinned executable identity.
The locale profile requires that locale on the observation host; missing
locale behavior is not silently normalized. Host inheritance is not an
inventory of all possible environmental values. No environment dump or
credential values are persisted in the receipt.

## Decision table

| Observation | Classification | Allowed conclusion |
|---|---|---|
| Missing process/bwrap, timeout, missing/mismatched blob, or red clean control | unavailable | No completed comparison; do not count this surface |
| clean raw tuple differs from clean_repeat | nondeterministic | The raw observation is not repeat-identical; do not attribute profile differences to one environment variable |
| repeat-identical clean; every profile tuple equals clean | invariant | No difference observed in this seven-profile sample |
| repeat-identical clean; one or more other profiles differ | env-sensitive | Name exactly the differing profiles; diagnose their output and target source before claiming cause |

Raw streams are SHA-256 hashed without replacing paths or times
(`normalization: none`). Timings are recorded but are not part of the tuple.
No semantic equivalence is inferred from matching exits alone.

## Executed result

Counting the initial committed-receipt candidate's records:
`python3 -c 'import json,collections; d=json.load(open(".ufo/evidence/round-21/f5/receipt-initial.json")); print(collections.Counter(s["classification"] for s in d["surfaces"]))'`
observed eight invariant and one nondeterministic (2026-10-21); all nine
clean-control exits were0. The frozen C2 counter separately checks pins,
profile completeness, classification arithmetic, the tool selftest and a
mined source header at a named committed revision.

| Surface | Raw tuple classification |
|---|---|
| tameshi-runner | invariant |
| js-kimi-census | invariant |
| bash-surface-census | invariant |
| bash-tsukuroi-census | invariant |
| bash-mado-verify | invariant |
| bash-checklist-run | invariant |
| js-claims-check | invariant |
| js-round-gate | nondeterministic |
| js-sources-check | invariant |

The round-gate clean and clean_repeat stdout tails contain different
`kumitate-round-gate-selftest-<random>` directories beneath `/tmp/w/tmp`.
Both exits are0 and both stderr digests equal SHA-256(empty). Thus this is
**raw output variation**, not evidence of flaky pass/fail outcomes. It is
not relabeled an environmental sensitivity, and no path normalization is
retroactively applied to make the observation green.

The public selftest actually exercised invariant, TZ/locale/HOME/COLUMNS
sensitivity and repeated-output variation fixtures, missing-bwrap and timeout
paths, and a public-CLI pin mismatch refusal:9/9, exit0
(`.ufo/evidence/round-21/envdiff-private-first.stdout`). The synthetic
sensitive fixtures are capability evidence; they are not measurements of
sibling gates or evidence of general environmental coverage.

## Reuse boundary

A receipt is reproducible evidence of what was recorded, not authenticated
proof that an arbitrary producer executed it. The frozen counter's metadata
checks cannot detect a fabricated, internally consistent profile receipt;
independent executions remain necessary. New pins, extra profiles, different
runtime versions or output normalization require a new observation with a
separately named population. Do not silently expand the frozen ruler.
