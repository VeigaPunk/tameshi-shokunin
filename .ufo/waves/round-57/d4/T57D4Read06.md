# T57D4Read06 — bounded documentary agreement; provenance gap

Axes: revision/section identity, command/receipt consistency, historical fidelity, evidence completeness, non-mutation.

Scope: documentary review of the absolute lane paths `.ufo/waves/round-57/w3/T57W3Read06.{md,json}` and their four retained receipts. Candidate: `adf87899c70d616140a81185a8f9acbbdfb30392` (C0b). No candidate gate, test, build, imported candidate module, or exploit was executed. No admission is granted; current integration remains UNVERIFIED.

## Findings by severity

### Low — clone and read-only-layout assertions lack retained provenance

`T57W3Read06.md:22` asserts a detached shared clone at C0b and read-only sibling symlinks; JSON notes repeat the layout/non-mutation claims. All four receipt objects retain only `command`, `cwd`, `exit`, `stdout`, and `stderr`. None retains clone HEAD, clone status, clone-creation output, symlink targets or permission/mount evidence. A pathname under scratch does not itself establish revision cleanliness, read-only access or absence of transient writes.

Evidence command (read-only Python Eval, executed):

```python
print('RECEIPT_KEYS', {n:sorted(r) for n,r in receipts.items()})
```

Here `receipts` is JSON-decoded from the four files under `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read06-receipts/`.

Output: each of `01-section-identity.json`, `02-regression.json`, `03-pointer-claim-sweep.json`, and `04-original-debt.json` has exactly `['command', 'cwd', 'exit', 'stderr', 'stdout']`. The full retained contents were also read. This is a missing-evidence finding, not evidence of a write or wrong checkout. Recommendation: qualify those environmental assertions as uncorroborated by retained receipts, rather than treating the aggregate regression stdout as complete execution provenance. The runner's retained SHA does independently match C0b, narrowing this gap.

## Bounded agreement

Executed source-read command:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md
```

Output at lines 1312–1320 is the reported heading and dated introduction, ending `never a re-cut.`; the next heading is a separate subsection. Read-only Python analysis of these git-show bytes, with trailing blank lines stripped per the documented frozen sectionizer, produced:

```text
SECTION 1312 1320 636e850f885cb39904d100f67446e1039aa48c6510c2a66ea6e6d5aaa089faf7 matches= True
RUNNER_C0b_SHA256 977de47034cbe52b87c3b4ba4a82ca334a6b88f1ef26d07dd59fd705649e0bda
```

The frozen measure was read as text only, not imported. Its docstring lines 18–22 specifies the byte normalization above.

Executed JSON comparison `sum(c == r for c in report['commands'])` returned **1 for every receipt**. Thus command, cwd, exit, stdout and stderr match the adjacent report JSON exactly. Each retained exit is 0 and each retained stderr is empty. This authenticates consistency of retained data, not execution.

`02-regression.json` records ten exact tables, zero flips/inconclusives, including checklist `15/15` and all other legs `10/10`, then:

```text
REGRESSION: PASS (cases=10 passed=10; ledger legs exact: killed-delta<=0 flips<=0)
```

Its runner hash matches C0b as above. No regression was rerun. C0b `tools/registry.json`, read through git show, agrees with the receipt: active `mutate-and-run-regression`, argv `["bash", "tools/mutate-and-run.sh", "--regression"]`, expected exit 0 / `REGRESSION: PASS`.

Additional executed git-show-only documentary comparisons:

- C0b runbook lines 1–10 identify round 10 / T10-1 and a single operator-facing document.
- C0b lesson lines 49–55 explicitly record embedding cases 5/6 and historical six-leg PASS. This is compatible with the retained current ten-leg summary, not a conflicting current count.
- Reconstructing the five retained ledger excerpts from C0b gave `04 stdout C0b equality: True`. Lines 341/350 retain the historical four-leg receipt and cases-5/6 caveat.
- Git-show reads at historical `606716f` reproduce the tool/runbook byte lengths **77904 / 31416** and every historical excerpt printed in receipt 03; no excerpt mismatch was emitted.

## Residual risk and verification gaps

Receipts are unsigned retained observations, not execution authentication. Historical operator experience was not observed; the original report already discloses this. Exact C0b content agreement cannot prove that all files read from the old clone were clean during the original run. No 64/64 monitor, C1/C2 counter, integration, resume continuity, rerouting or saturation result is established here; those are outside this assigned nine-line section. No unsupported global pass is inferred.

The mounted `xd://` inventory contains no LSP device. No semantic-reference proof is claimed. No installs/updates, production edits, delegation, commits or pushes occurred; only this seat's d4 report and JSON were written.

Self-evaluation: accuracy 4/5 (execution authenticity remains unavailable); completeness 4/5 (environmental assertions lack retained provenance); clarity/actionability/conciseness 4/5 (bounded findings and concrete qualification supplied; command context spans retained files). Overall 4.0/5. Highest-impact improvement: retain clone/layout provenance with future observations; do not retroactively fabricate it.
