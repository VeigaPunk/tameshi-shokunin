# T57D4Overlap — cross-report documentary consistency

## Axes and one proposed move

Declared axes: **C1 calibration**, **C2 operability**, and **no-harm cold-read coverage**. Proposed move: retain a single **scope-separated limitation table** in the round synthesis rather than collapsing reader recommendations, row statuses and counter outputs into “verified.” Each statement needs revision, subject, evidence class (source / retained execution / prospective), and unresolved limitation. This is a documentary proposal only: no target patches, ledger changes, admission or integration.

Expected benefit [INFERENCE]: more accurate calibration without reducing operability or cold-read coverage, because monitored bytes and criteria stay unchanged. It does not itself raise any measured score.

## Evidence and interactions

### 1. Executed gate rows do not establish the C2 equality clause

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RowAttack3.md:73-77` separates R56.2's cell repair from its later semantic-counter repair and reports R56.6's executed 0/3/2 gate fixtures as supported.
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read09.md:28-38` reports no section defect, but explicitly limits the scope to the section and retained study.
- **Contradiction if promoted:** `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3CritContract.md:33-61` reports a C2 PASS on a registry failing the exact-element target, and withdraws an earlier staged-candidate PASS produced with the original counter. Recorded command `git show adf87899…:tools/registry.json | python3 …` produced empty element-equal lists for both refusal rows; the retained counter line says `held=3/3 ... total=0 C2_R57_PASS=true`.
- Current source independently supports the mismatch: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/c2/measure.py:242-248,373-377` extracts tokens with `CODE_RE.findall`, whereas `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/contract.json:125,140` requires element equality and says registry substring matching does not enforce it.

Required limitation: **“Three executed gate rows and accurate documented exits are narrower evidence than C2 contract satisfaction; the exact-element counter/contract mismatch remains unsupported by those successes.”** No gate was executed by this seat.

### 2. Reader certification, command health and no-harm credit are different subjects

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read14.md:12,46-50` finds no false section statement while retaining two registry failures. `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read15.md:11-25` records the registry command and output `held=51/53`, sources-census exit 1 and verify-round15 pin failure.
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read18.md:9-39` additionally retains witness drift, 30 successful selftests, and an initial layout-dependent 49/53 later distinguished from 51/53. These are not independent additive defect counts or a clean registry.
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read17.md:14-35` records `classified=0/9` without explicit fleet root, `9/9` with it, replay refusal, and cold-read 46/64. This is not a hermetic C0b sibling snapshot.
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RowR551xR553-receipts/coldread-monitor.txt:1-18` retains the monitor command and outputs BASE=64/64, C0b=46/64, score 6 and box3=false. `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3CritContract.md:156-168` agrees and disclaims end-to-end controls/no-harm execution.

Required limitation: **“Reader records can support bounded section accuracy while registry entries remain red. Eighteen reader files are not an observed deciding-revision 64/64 bind, and a successful monitor process exit is not satisfaction of its floor.”** No deciding-revision restoration is established by this scan.

### 3. Current successor repair cannot retroactively alter BASE verdicts or historical completion

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RowAttack3.md:9-23,76` reports R56.5's successor structural repair at 870d9b98, explicitly not a deciding-run success.
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/c1/measure.py:18-30,446-455` distinguishes `status` from `status_at_base` and compares only the latter to the blind panel. A post-BASE successor observation is therefore not itself a disagreement with an open-at-BASE verdict.
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RowAttack1.json:33-36,63-66` separates historical textual/re-key completion from C0b's current 46/64 loss; its R52.1 finding distinguishes a setup commit from the actual completion receipt commit.
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3CritContract.md:104-119` reports six re-seat provenance issues and the post-commit panel correction tension. Current `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/contract.json:145-154,200-201` already describes staged corrections and UNVERIFIED continuation. The older critic's “absent panel” observations must not be copied as present-tense facts.

Required limitation: **“Structural successor implementation, historical completion, status at BASE, panel provenance, and final execution are separate claims. Neither current drift disproves historical completion nor current repair rewrites BASE.”** This seat makes no row-status disposition.

### 4. Lane corrections and deferred minor gaps are not repaired original bytes

- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3RowAttack2.md:9-25,63-68` distinguishes fleet-owned R52.6 report debt and incomplete R53.8 multi-commit provenance from lane-record corrections R54.1/R54.5. Original fleet report bytes were not repaired by lane errata.
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read05.md:11-30,43` and `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read08.md:6-12` retain citation-only gaps; Read17 retains clone guidance debt. Their deferral statements are observations in reports, not permission from this seat to change targets or weaken criteria.

Required limitation: **“Superseding lane corrections and gap-minor reader recommendations retain their ownership and scope; neither certifies correction of original report bytes or disappearance of the cited gap.”**

## Risks and verification boundaries

Risk: the limitation table could itself be misread as a new admission mechanism. Keep it explanatory only; canonical predicates and L1 authority remain unchanged. Do not patch registry/SKILL to reconcile prose: the critic records that registry edits change frozen/bind inputs (`T57W3CritContract.md:63` at the absolute path above). Provenance and bind dependencies cross runtime, contract and substrate surfaces (`T57W3CritContract.md:123-130`); prose consistency cannot close them.

Documentary sweep actually performed: `functions.grep` over the absolute `w3/T57W3Read*.md` paths for limitation/unsupported/contradiction/verification and finding headings; `functions.read` of the cited reader, attacker, critic, contract, counter and retained-monitor ranges. Outputs included the exact retained command results quoted above and current token-extraction source. These were source/report reads, not re-execution of their commands. All 18 reader reports were included in the text inventory; this was not a full receipt-by-receipt authenticity audit.

Verification required before any later stronger claim (not run here): revision-bound evidence of C1 panel/re-seat/result provenance and applicable counter preconditions; C2 exact-element compliance with the actual counter identity; final committed bind with the existing 64/64 no-harm floor and remaining contract monitors. Under the recovery directive these remain missing evidence, not executable instructions or passes.

No tests/builds, candidate gates, exploit reproduction, credentials, external requests, runtime invocation, production edits, delegation, commits or tool installations were performed. Only this report and its companion JSON were written.

Self-evaluation: accuracy 4/5 (retained executions not independently authenticated); completeness 4/5 (all reader reports inventoried, selected interaction receipts/source ranges inspected); clarity 4/5 (historical/current distinctions require several citations); actionability 4/5 (bounded wording supplied; no admission decision); conciseness 4/5 (absolute citations are lengthy). Overall 4.0. Highest-value improvement: preserve these scope labels in L1 synthesis rather than replacing them with a collective “verified.” User agreement is expected only for the explicitly documentary scope.
