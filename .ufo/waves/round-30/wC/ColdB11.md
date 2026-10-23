# ColdB11 — wave C cold reads (3 sections, SKILL.md @ bb681566)

Clone: `/tmp/ColdB11-RjYK/fleet` (tameshi clone detached at
`bb681566b18211adf8ae9c28df91e17678e3f545`; SKILL.md sha256 verified
`c46ec02e…d3b5e36d6`). Sibling lanes symlinked read-only. No lane files
written; all scratch under `/tmp/ColdB11-work` and `/tmp/ColdB11-RjYK`.

```json
{"schema": "tameshi-coldread-report-v2", "seat": "ColdB11", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "bb681566b18211adf8ae9c28df91e17678e3f545",
 "sections": [
 {"start": 131, "heading": "## Mutation-sweep recipe — numbered steps; bounded cold-read evidence", "class": "instruction", "verdict": "executed-ok", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": ["The recipe names a literal `all unique` line for historical drivers; the modern harness prints `MUTATE_SPEC ... defects=` and `APPLY FAIL` instead — wording is explicitly historical in the section, so a nit only.",
                 "Round-16 end-to-end re-execution claim ('two seats; Errata — round 16') not independently re-checked by me; the cited Errata section exists at SKILL.md:1707.",
                 "My step-5/6 demo mutant printed PASS but its kill was on exit=1 (the recipe's own adjudication needs exit+verdict — consistent with the text's warning never to adjudicate exit alone; the KILLED mechanism was instead exercised end-to-end in the section-3 harness run)."],
  "commands_executed": ["python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md corpus/knowledge/gates-survey-kumitate.md corpus/knowledge/gates-survey-kagi.md corpus/README.md",
                        "bash -c 'sha256sum tools/mutate-and-run.sh && wc -l -c tools/mutate-and-run.sh && stat -c %y tools/mutate-and-run.sh && git status --porcelain -- tools/mutate-and-run.sh; echo \"porcelain-rc=$?\"'",
                        "bash -c 'set -e; mkdir -p /tmp/ColdB11-work/sweep/evidence; cp -p tools/mutate-and-run.sh /tmp/ColdB11-work/sweep/pristine.sh; sha256sum /tmp/ColdB11-work/sweep/pristine.sh tools/mutate-and-run.sh; python3 - <<PY (assert count==1 of \"  exit 0\" in a scratch gate, write mutant via str.replace, print \"all unique\") PY; sha256sum gate mutant; bash /tmp/ColdB11-work/sweep/mutant-K1.sh --selftest; echo mutant-exit=$?'"],
  "opened": ["corpus/knowledge/mutation-case-kimi-census.md", "corpus/knowledge/mutation-case-kagi-census.md", "corpus/knowledge/gates-survey-kumitate.md", "corpus/knowledge/gates-survey-kagi.md", "corpus/README.md", "tools/mutate-and-run.sh", ".gitignore"],
  "inputs": {"corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548",
             "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0",
             "corpus/knowledge/gates-survey-kumitate.md": "3dca7a1a5c621bf0ec75948d0836839dec98651673bb2987861d9aa122579b0e",
             "corpus/knowledge/gates-survey-kagi.md": "4734f0a0bd28e90f78b0a766b2aa6dac8238936550e1b1b0ec3316b00e1294c6",
             "corpus/README.md": "636b716e7891f09cc3eb4a2c47bcf3a5120460c356dcfc07f5d8ba9b63259909",
             "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
             ".gitignore": "0f699af0108f1ac4f43cd5f61c9151896b8328ec7edd0adf4ca1c638a2441116"},
  "external_inputs": {},
  "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB11-1-1.json",
             "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB11-1-2.json",
             "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB11-1-3.json"]},
 {"start": 375, "heading": "## Restore discipline — before/after identity, not continuous non-write proof", "class": "instruction", "verdict": "executed-ok", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": ["`bash tools/mutate-and-run.sh --regression` (item 6's named ledger replay) exceeded my 6-minute bound — it was killed by my own `timeout 400` at leg 8 of 9, so its receipt was never written (the collector dies with the child); the log shows the first 7 legs all `REGRESSION_CASE ...: PASS` with `match=10/10|15/15` exact-table replays, and `--selftest` (traced instead) passes 106/106 including the nine-leg tally harness checks. Replay works; full 9-leg wall time on this host is > ~400 s."],
  "commands_executed": ["python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md corpus/README.md",
                        "bash -c 'sha256sum tools/mutate-and-run.sh; stat -c \"size=%s mtime=%y\" tools/mutate-and-run.sh; git rev-parse HEAD; git status --porcelain -- tools/mutate-and-run.sh; echo porcelain-empty rc=$?'",
                        "bash /tmp/ColdB11-RjYK/fleet/tameshi-shokunin/tools/mutate-and-run.sh --regression --workdir /tmp/ColdB11-work/regression (executed under the collector; killed by my `timeout 400` at leg 8/9 — seven legs PASS recorded in /tmp/ColdB11-work/regression.out; NO receipt written, so it is not listed in traces; the credited replay-ledger command is the --selftest below)",
                        "bash /tmp/ColdB11-RjYK/fleet/tameshi-shokunin/tools/mutate-and-run.sh --selftest"],
  "opened": ["corpus/knowledge/mutation-case-kimi-census.md", "corpus/knowledge/mutation-case-kagi-census.md", "corpus/README.md", "tools/mutate-and-run.sh", ".gitignore"],
  "inputs": {"corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548",
             "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0",
             "corpus/README.md": "636b716e7891f09cc3eb4a2c47bcf3a5120460c356dcfc07f5d8ba9b63259909",
             "tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
             ".gitignore": "0f699af0108f1ac4f43cd5f61c9151896b8328ec7edd0adf4ca1c638a2441116"},
  "external_inputs": {"tameshi-shokunin@bb681566b18211adf8ae9c28df91e17678e3f545:SCORECARD.md": "9ba015ca568db27e71dd35322884952c18f7be0e306667f35391da7174fd920a"},
  "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB11-2-1.json",
             "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB11-2-2.json",
             "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB11-2-3.json"]},
 {"start": 827, "heading": "### The protocol — ordered, fail-closed", "class": "instruction", "verdict": "executed-ok", "blocking_gaps": [], "wrong_expectations": [],
  "minor_gaps": ["INCONCLUSIVE arms (timeout 124 / 126-127 not runnable) not exercised by my run — read in code and covered by the tool's own --selftest harness instead.",
                 "Step 1's caveat 'the original is never a write target unless --workdir is its own directory' — the tool never opens the target for writing at all; the clause is about writes landing beside the original, phrasing slightly loose but not false.",
                 "Pre-registration tail claim cites `mutation-case-mado-verify.md:73,:187-189`; verified there (10/10 verdict predictions held, six survivors), though the page's own phrasing is 'six survivors' — 'six survivor classes' is a fair paraphrase, not a quote."],
  "commands_executed": ["bash -c 'git rev-parse --verify \"b58b26fb^{commit}\" && git show b58b26fb:tools/mutate-and-run.sh | sha256sum && git show b58b26fb:tools/mutate-and-run.sh | wc -l && sha256sum tools/mutate-and-run.sh && wc -l < tools/mutate-and-run.sh'",
                        "bash tools/mutate-and-run.sh --target /tmp/ColdB11-work/gate.sh --defects /tmp/ColdB11-work/spec-ok.spec --suite 'bash \"$MUTANT\" --selftest' --workdir /tmp/ColdB11-work/ev1",
                        "bash tools/mutate-and-run.sh --target /tmp/ColdB11-work/gate.sh --defects /tmp/ColdB11-work/spec-noop.spec --suite 'bash \"$MUTANT\" --selftest' --workdir /tmp/ColdB11-work/ev2",
                        "bash tools/mutate-and-run.sh --target /tmp/ColdB11-work/gate.sh --defects /tmp/ColdB11-work/spec-absent.spec --suite 'bash \"$MUTANT\" --selftest' --workdir /tmp/ColdB11-work/ev3",
                        "python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-mado-verify.md"],
  "opened": ["tools/mutate-and-run.sh", "corpus/knowledge/mutation-case-mado-verify.md"],
  "inputs": {"tools/mutate-and-run.sh": "a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9",
             "corpus/knowledge/mutation-case-mado-verify.md": "f2d53d495e6c1d8b2c18e7bc0eac54955d477455958b10866c5f8712b2086bf3"},
  "external_inputs": {"tameshi-shokunin@b58b26fbeba8fd972e1d31ac8a9175a81e333b32:tools/mutate-and-run.sh": "597e141989065e038a1c2b35359ab3d20b565d3c959c2eec64166ecb1ff6331b"},
  "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB11-3-1.json",
             "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB11-3-2.json",
             "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB11-3-3.json",
             "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB11-3-4.json",
             "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/coldread/traces/ColdB11-3-5.json"]}]}
```

## What I checked

**Section 1 (131, recipe).** Class `instruction`: it tells a reader to pin a
committed artifact, copy to scratch, assert `count(old)==1`, run control +
one-edit mutants, adjudicate exit AND verdict, probe survivors, restore-check.
I ran those named commands under the collector: `sha256sum`/`wc`/`stat`/`git
status --porcelain` on `tools/mutate-and-run.sh` (a7d3f2dd…, 2080 lines, clean
porcelain), `cp -p` pristine, the count==1 assert + `str.replace(old,new,1)`
mutant construction on a scratch gate. Every load-bearing citation held: kimi
pin `83016d45…4f426`/896 lines/43273 B, `43/43 pass`+`VERDICT: PASS`, 8/10 in
7.0 s (kimi-census :13-31); kagi pin `275d8294…53009f`/44212 B/887th line no
trailing newline, 14 executed +2 skip = 16, 8/10 in 11.0 s (kagi :13-53); B4
token-only kill (kagi :88-91); B5 `exec 644`/`DIVERGED no execute bit` and B10
`ok=0`/`ok=1` probe outputs (:111-122, :252-254); G-R2-1 dirty-pin lesson
(README:11, gates-survey-kagi errata :545+); E1 kept-miss entries in both
notes; U5 host-stability lines (kimi :204-205, kagi :203-204); the
`SKILL.md:377-378` self-cite resolves exactly to "endpoint identity, not that
no transient write occurred."

**Section 2 (375, restore discipline).** Class `instruction` (ordered policy
with named commands). Items 1-3's commands ran under the collector on a
committed artifact (before/after fingerprints agree, porcelain empty — the
endpoint-identity shape the section describes). Item 6's cite `SCORECARD.md:13`
was read via `git show` (exception file, untraced): the cell does record
"sensitivity re-runs from the lane's retained scratch" — the "reran from
scratch" claim holds. Item 6's `--regression` ledger replay was executed under
the collector: 7 of 9 legs completed `PASS` with exact table matches
(kimi 8/10=80%, kagi 8/10=80%, tsukuroi 6/10=60%, mado 4/10=40%,
checklist 7/15=47%, claims 7/10=70%, round-gate 5/10=50%) before my own
`timeout 400` cut it at leg 8; the collector died with the child so no receipt
was written — the credited trace is `--selftest` (106/106 PASS, including the
nine-leg tally harness and case-tally-mismatch detector), which confirms the
replay machinery end-to-end hermetically. It does confirm "it does not recover
the old driver" (replay uses embedded specs, not `mutate_driver.py`).

**Section 3 (827, protocol).** Class `instruction` with a literal command block.
Run verbatim against a scratch gate: `CONTROL: GREEN`, `KILLED` on exit≠0,
`SURVIVED` on exit 0, `MUTATE_RESTORE: OK` with identical before/after sha256,
`MUTATE: DONE (... killed=1 survived=1 inconclusive=0 kill-rate=50%)`, exit 0,
and the evidence dir holds `pristine.gate.sh`, `mutant-K1/S1.gate.sh`,
`evidence/control.out`, `evidence/K1.out`, `evidence/S1.out`, `results.tsv`,
`spec.copy`, `MUTATE_EVIDENCE` line — every step-6 claim. Fail-closed verified:
`@new == @old` refused `MUTATE: SETUP (spec parse failed)` exit 2; absent
`@old` refused `spec/preparation failed ... no suite run` exit 2 before any
suite run. The pin claim is exact: `git show b58b26fb:tools/mutate-and-run.sh`
= `597e1419…ff6331b`, 1001 lines; the live path now holds `a7d3f2dd…` at 2080
lines ("a later revision"); `MUTATE_TOOL` pin appears on every run log.
`mutation-case-mado-verify.md:73,:187-189` confirms 10/10 verdict predictions
held.

No tools installed or upgraded; no installs needed.
COLDREAD ColdB11: executed-ok, executed-ok, executed-ok
