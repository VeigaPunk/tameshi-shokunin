# X16BucketCommands — wave 1 (round 17)

Mechanical command-bearing census of every SKILL.md bucket at
`98bea7da5801f4bc58e4187690ee1687c8a5061f` vs the round-16 ledger's `class`.

## Method

- Sectionizer: `sectionize()` copied verbatim from
  `.ufo/evidence/round-16/measure.py` (blob at the target rev) — preamble +
  `#`/`##`/`###` heading blocks, headings inside ```` ``` ```` fences ignored,
  trailing blank lines stripped, sha256 over surrogateescape bytes.
- Ledger: `.ufo/evidence/round-16/coldread/ledger.json` at the same rev
  (75 entries, schema `tameshi-coldread-ledger-v1`); matched to buckets by
  section `sha256` exactly as `coldread()` does; crediting entry = first match
  for which `entry_credit_reason()` returns None.
- Mechanical rule (spec literals only): `executes_commands=yes` iff a fenced
  block contains a non-comment line starting with
  `python3|bash|git|node|sh|tools/` **or** an inline `` `…` `` string starts
  with the same prefixes. Numbered recipe steps and other executable-looking
  lines (`$`, `./`, `cd`, `jj`, …) are captured in the JSON but do NOT set the
  flag (`executes_commands_incl_numbered_steps` is the looser flag).

## Result

- 54 buckets, 27 execute-commands=yes, 0 uncovered by the ledger.
- Agreement (yes↔instruction, no↔record): 31/54.
- Disagreements: 23/54 — 13 `yes` classed `record`, 10 `no` classed `instruction`.

## Table

| start | heading | mech | ledger class | agree |
|------:|---------|:----:|:------------:|:-----:|
| 1 | *(preamble)* | no | record | agree |
| 6 | # tameshi-shokunin | no | record | agree |
| 17 | ## Standing rules | no | **instruction** | **disagree** |
| 30 | ## Source notes | no | record | agree |
| 58 | ## Gate-shape decision table | no | record | agree |
| 94 | ## The mutation bar | no | **instruction** | **disagree** |
| 131 | ## Mutation-sweep recipe | no* | **instruction** | **disagree** |
| 246 | ## Defect-taxonomy templates | no* | **instruction** | **disagree** |
| 314 | ## Kill-rate bands | YES | **record** | **disagree** |
| 375 | ## Restore discipline | YES | instruction | agree |
| 405 | ## Cross-language divergence | no | record | agree |
| 466 | ## No-permissiveness audit recipe | no* | **instruction** | **disagree** |
| 497 | ## Fail-closed arm taxonomy | no | record | agree |
| 527 | ## Appendix A — JS case | YES | instruction | agree |
| 594 | ## Appendix B — bash case | YES | instruction | agree |
| 668 | ## Third case | no | record | agree |
| 794 | ## The mutation service | no | record | agree |
| 806 | ### The opt-in contract | YES | instruction | agree |
| 827 | ### The protocol | YES | instruction | agree |
| 858 | ### The boundaries | no | record | agree |
| 883 | ### The report shape | no | **instruction** | **disagree** |
| 899 | ### The mado run | YES | **record** | **disagree** |
| 921 | ## The leg ledger | YES | **record** | **disagree** |
| 933 | ### Using the ledger | YES | instruction | agree |
| 965 | ### Reading a receipt | no* | **instruction** | **disagree** |
| 1010 | ## The re-sweep cadence | no | **instruction** | **disagree** |
| 1021 | ### The tick and the pin read | YES | instruction | agree |
| 1069 | ### Triggers T1–T3 | no | **instruction** | **disagree** |
| 1092 | ### Six-case confidence | YES | **record** | **disagree** |
| 1155 | ## Cadence's first tick | no | record | agree |
| 1164 | ### The tick, executed | YES | **record** | **disagree** |
| 1212 | ### The receipt at this boundary | YES | **record** | **disagree** |
| 1230 | ### The re-pin semantics | no | record | agree |
| 1246 | ### The service's limits | no | record | agree |
| 1272 | ## Operator's runbook / six-leg | no | record | agree |
| 1281 | ### The operator's runbook | no | record | agree |
| 1302 | ### The six-leg regression | YES | **record** | **disagree** |
| 1365 | ## Final pointers | no | record | agree |
| 1380 | ### The map | YES | **record** | **disagree** |
| 1396 | ### Boundary readings | YES | **record** | **disagree** |
| 1436 | ### Where to enter | no | **instruction** | **disagree** |
| 1449 | ### What stays open | no | record | agree |
| 1464 | ## Promotion-evidence calibration | no | record | agree |
| 1479 | ## Repeated controls | YES | instruction | agree |
| 1499 | ### Gate/probe registry | YES | **record** | **disagree** |
| 1517 | ## Pin disposition — round 13 | YES | instruction | agree |
| 1548 | ### Round-13 gate/probe registry | YES | instruction | agree |
| 1563 | ## Effective expectation reconciliation | YES | instruction | agree |
| 1597 | ### Round-14 historical registry | YES | **record** | **disagree** |
| 1609 | ## Context gate classification | YES | **record** | **disagree** |
| 1676 | ### Round-15 gate/probe registry | YES | instruction | agree |
| 1707 | ## Errata — round 16 | YES | **record** | **disagree** |
| 1754 | ## Seventh recorded case | YES | instruction | agree |
| 1806 | ### Round-16 gate/probe registry | YES | instruction | agree |

`no*` = no spec-literal commands but numbered recipe steps present
(131: 11 steps; 246: 6; 466: 8; 965: 7).

## Disagreement analysis

### YES + record (13) — mostly benign, two patterns

1. **Prefix-regex artifacts**: `bash-surface-census`,
   `bash-tsukuroi-census`, `bash-mado-verify` (names, not invocations) and
   `tools/mutate-and-run.sh:72-109`-style file:line refs trip the
   `bash\b`/`tools/` prefix. Affects 921, 1164, 1212, 1302, 1380.
   Line 1396 also has receipt *output rows* starting with `bash-…`.
   → mechanical rule over-fires; a word-boundary + whitespace/arg or
   `tools/…py|sh` arg-required refinement would clear most of these.
2. **Genuine commands in record buckets**: 314 (`git status --porcelain`),
   899 (`` `bash "$MUTANT" --selftest` ``), 1499 (4 `python3 tools/…`
   invocations), 1597 (2 `python3 tools/evidence-disposition.py`), 1609
   (`` `tools/context-capture.py` ``), 1707 (4 `git …` commands), 1092
   (`tools/tsukuroi-census.sh`, `tools/mado-verify.sh`), 1396 (three receipt
   rows starting `bash-…` inside a fence). These sections *do* carry runnable
   commands yet are classed `record` — seats verified receipts rather than
   re-executing. Under the round-16 credit rule that is legal
   (`verified-record|gap-minor`); under round-17's input-keyed rule it only
   matters if commands_executed_count>0 — note **record entries also carry
   nonzero commands_executed_count** (e.g. 1707: 27, 1302: 13, 1499: 15),
   so v2 measure will still demand `inputs` for them; recorded-command
   provenance in record buckets is the same crediting hole as instruction
   buckets.

### NO + instruction (10) — the load-bearing finding

All ten credited on `executed-ok|gap-minor` with `commands_executed_count`
4–14 while the section text contains **no spec-literal command at all**:

| start | heading | numbered steps | cmd_count | seats |
|------:|---------|---------------:|----------:|-------|
| 17 | Standing rules | 0 | 10 | CR01, RR14 |
| 94 | The mutation bar | 0 | 14 | CR03 |
| 131 | Mutation-sweep recipe | 11 | 7 | RR03 |
| 246 | Defect-taxonomy | 6 | 13 | RX2 |
| 466 | No-permissiveness audit | 8 | 14 | CR09 |
| 883 | The report shape | 0 | 6 | CR15 |
| 965 | Reading a receipt | 7 | 12 | CR17 |
| 1010 | Re-sweep cadence | 0 | 7 | CR18 |
| 1069 | Triggers T1–T3 | 0 | 6 | CR18, Replica1021 |
| 1436 | Where to enter | 0 | 4 | CR23 |

Six of these (17, 94, 883, 1010, 1069, 1436) are **pure prose** — no fences,
no inline commands, no numbered steps — yet were credited as executed
instructions. The seats ran commands sourced from other sections/tools and
attributed them to prose buckets. This is exactly the attribution hole
round-17 C1 (input-keyed credit) targets: nothing in the bucket text binds
the executed commands to it, so `inputs` recording is what makes the credit
checkable at all.

## Deliverable

`.ufo/evidence/round-17/coldread/bucket-commands.json`
(schema `tameshi-bucket-commands-v1`): all 54 buckets with start/end, heading,
section sha256, fenced-block inventory (command lines + advisory
executable-like lines), inline commands, numbered steps, both flags, matched
ledger class/verdict/cmd_count/seats, and the agreement verdict.
sha256 of file: `39b9392afb5d230750683e6ed5b1ce7ed74079a150318f136421293930328bf5`.

## Caveats

- Spec-literal prefix rule both over-fires (`bash-surface-census`,
  `tools/x.sh:N-M` refs, receipt rows) and under-fires (`jj`, `$`-prompt,
  `./tool`, `cd`); JSON keeps `other_executable_like` so the L1 can re-grade
  with a tighter/looser rule without re-parsing.
- Ledger `class` is the crediting entry's; sections matched by sha only.

Verdict: **built** — 54 buckets classified; 23 mechanical-vs-ledger class
disagreements, headed by 6 pure-prose buckets credited as executed
instructions with 4–14 phantom commands each.
