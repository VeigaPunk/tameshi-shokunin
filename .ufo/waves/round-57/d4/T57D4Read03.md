# T57D4Read03 — documentary audit

Recommendation: **bounded agreement, with one minor evidence-retention gap**. This is not admission. Current candidate integration remains **UNVERIFIED**.

Axes: candidate/section identity; claim-to-receipt consistency; historical-anchor fidelity; retention completeness; documentary-only safety.

## Findings by severity

### Low — aggregate driver exit/full-output claim lacks its own retained receipt

Paths (all under `/home/vgpnk/Projects/shokunin/tameshi-shokunin/`):
- `.ufo/waves/round-57/w3/T57W3Read03.json:20-25` records `python3 …/T57W3Read03-receipts/sweep.py`, exit 0, and a compact output summary, pointing to `static.json`.
- `.ufo/waves/round-57/w3/T57W3Read03.md:23` says all listed commands exited 0 and full outputs/command records are adjacent.
- The retained `static.json` contains constituent static-operation records, not the parent Python invocation's exit/stdout/stderr. `regression.json` separately retains the child regression invocation. Neither establishes the parent exit. Historical `git show` outputs in `static.json` are selected excerpts, not full command stdout.

Documentary sweep and observed output:

```text
read /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read03-receipts
=> static.json, milestones.json, regression.json, regression.stdout,
   regression.stderr, sweep.py, and ten per-leg directories;
   no parent-driver exit/stdout/stderr receipt listed.

read /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read03-receipts/sweep.py:35-39,48-49,56-59,70-75
=> historical output is replaced with selected numbered ranges;
   static.json stores results; regression.json/stdout/stderr store the child;
   the parent prints JSON records and does not retain its own process outcome.

read /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read03-receipts/static.json:1-46
=> array of five constituent records, each with exit_code 0;
   no record of the parent python3 sweep.py process.
```

This is **not evidence that the driver failed**, nor a contradiction of the ten-leg result. Narrow the report's retention assertion to constituent records/excerpts, or bind an already-existing original parent transcript if available. Do not manufacture a receipt or rerun the driver under this assignment.

## Bounded agreement

Only source reads, read-only `git show`, and in-memory documentary/hash comparisons were performed. No candidate gate, replay, imported sectionizer, tests, or builds ran.

Actual source command:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md
```

Observed section: heading at line 949; final content line 961; blank line 962; next heading `### Using the ledger` at 963. The frozen round-18 sectionizer source, also read using `git show`, defines end as the next heading's zero-based offset and strips trailing blank lines for hashing. An independent in-memory hash of those committed section bytes produced:

```text
949 962 430dd86f25b6ce3d5ed51012d54de7cdad7213c6353eb7701323de762b9fb993
```

This exactly matches both assigned reports. Candidate metadata consistently names C0b `adf87899c70d616140a81185a8f9acbbdfb30392`.

The documentary comparison sweep used `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show REV:PATH` to read committed blobs, and parsed existing receipt JSON/TSV/logs without executing their contents. Observed results:

```text
C0b runner sha256=977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda
static.json pointer digests equal C0b: 6/6
9f1d3c3:tools/mutate-and-run.sh retained ranges 72-109,511-522 equal source: True
4b7c682:tools/mutate-and-run.sh retained range 597-620 equals source: True
C0b round-16/round-gate/runner-regression.txt equals milestones.json retained output: True
regression.json output equals regression.stdout: True; recorded child exit=0; stderr empty
ordered per-leg results.tsv verdict tables equal C0b TABLE_* declarations: 10/10
retained ledger rows present verbatim in C0b: 8/8
```

The six digest comparisons cover the runner, standing ledger, cite-check note, drift-pins note, corpus README and SOURCES. Historical milestone source contains `local nlegs=8` at `4b7c682` and `local nlegs=9` at `a08e85c5d7f899e8a5992e20517edb1a380d79eb`; the round-16 committed receipt retains `cases=7 passed=7` and `rc=0`. The failed auxiliary `89722ddb` lookup is disclosed consistently, not laundered into a successful revision read.

Retained tables and per-leg `sweep.log` summaries agree on killed/defects:

| Leg | Killed/defects |
|---|---:|
| js-kimi-census | 8/10 |
| bash-surface-census | 8/10 |
| bash-tsukuroi-census | 6/10 |
| bash-mado-verify | 4/10 |
| bash-checklist-run | 7/15 |
| js-claims-check | 7/10 |
| js-round-gate | 5/10 |
| js-sources-check | 5/10 |
| js-cite-check | 5/10 |
| bash-drift-pins | 2/10 |

All 105 retained defect rows agree, in order, with the corresponding committed tables; no inconclusive TSV verdict appears. Retained stdout reports flips=0 for every leg and `REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)`. These are corroborated retained observations, **not newly executed passes**.

## Residual risk and verification gaps

- Retained local receipts are not execution authentication. The source/receipt comparisons establish internal documentary consistency, not who executed the historical command, exactly-once execution, or absence of transient writes.
- No current integration, 64/64 cold-read monitor, repeat determinism, host independence, saturation, canonical runtime, identity rerouting, or resume preflight/zero-mutation claim is established here. The assigned 949–962 record section does not specify those latter runtime contracts; no such inference was made.
- LSP unavailable: `read xd://lsp` returned `No such tool`. Semantic references/definitions/diagnostics could not be obtained; source comparisons are textual, not semantic caller proof.
- No production files, frozen evidence, receipts, PATH directories or Git state changed. Only this seat's two d4 report files were written. No tools installed.

Self-evaluation: accuracy 4/5 (unsigned historical observations remain bounded); completeness 4/5 (parent transcript unavailable in retained directory); clarity 4/5 (cross-file evidence necessarily spans several artifacts); actionability 4/5 (original transcript recovery belongs to evidence owner); conciseness 4/5 (explicit command/output evidence adds length). Overall 4.0/5. Highest-value improvement: retain/bind original parent process metadata, without representing a new execution as historical evidence.
