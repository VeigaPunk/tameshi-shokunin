# T57D4Read10 — bounded documentary agreement

Axes: claim/receipt consistency; C0b content identity; evidence limits/no-harm.

## Findings by severity

No concrete contradiction found in the assigned T57W3Read10.md/.json claims against their four retained receipts and C0b `adf87899c70d616140a81185a8f9acbbdfb30392`. This is a documentary recommendation only, not admission or an executed correctness verdict.

- All four command records match their retained receipt on command, cwd, integer exit, stdout and stderr (20/20 fields). Each records exit 0 and empty stderr.
- C0b SKILL.md lines 1559–1589 contain the assigned heading; the next heading starts at 1590. Removing trailing blank lines and hashing newline-joined section bytes reproduces `1fa3130bc6d4bc46124a1c0e234583657bb6c7623256dfa85f4db2a7fb91da31`.
- All eight POINTER_OK digests in scoped-sweep.json match C0b blobs, including both executed tools, manifest and companion. All four printed source rows match C0b SOURCES.md. S048 does supersede S047, as the original report discloses.
- Retained pin output contains six verified pins, five changed and one unchanged leg, zero unavailable, and all six `result_reuse=not_established`. Each leg's repo/path/commit/expected digest matches the C0b manifest. Its tool digest matches the C0b tool blob. The observation is explicitly dated `2026-10-30T04:41:43Z`, not a current sibling snapshot.
- Retained witness stdout reports `metadata_consistent reason=ok exit=0` and the four claimed inputs. Independently inspecting C0b blobs confirms both summary null fields and companion-pinned digests, plus exact declaration kind/disclosure agreement.
- All printed canonical decision and producer excerpts match C0b: pin-disposition.py:558–578 makes an absent worktree hash or unverified pin unavailable before equality classification, and always retains RESULT_REUSE; bash-witness-study.py:816 reads top-level kind and :1694–1701 contains the exact assertion. These are source observations, not executed regression results.

## Executed documentary sweep and output

No candidate tool, recipe, gate, selftest, counter or imported candidate module was executed. SKILL was obtained only through:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md
```

Output: section begins `## Pin disposition and provenance correction — round 13`, contains the two recipe invocations described in the assigned report, and ends with the prohibition on rerunning sibling gates for closure. The next heading is `### Round-13 gate/probe registry`.

Read-only Python analysis ran through functions.eval (stdlib pathlib/json/hashlib/subprocess only). `blob(p)` used `subprocess.check_output(['git','-C',str(lane),'show',rev+':'+p])`, where lane is `/home/vgpnk/Projects/shokunin/tameshi-shokunin` and rev is C0b. It compared the five receipt fields by equality; compared SHA-256(blob(p)) with each POINTER_OK digest; compared recorded code/source lines with committed lines; and read frozen JSON as data. Observed output:

```text
METADATA True True ### Round-13 gate/probe registry 1fa3130bc6d4bc46124a1c0e234583657bb6c7623256dfa85f4db2a7fb91da31 True
RECEIPT_FIELD_TOTAL 4 /4
POINTER_TOTAL 8 /8
CODE_EXCERPT tools/pin-disposition.py 558 578 True
CODE_EXCERPT tools/bash-witness-study.py 810 819 True
CODE_EXCERPT tools/bash-witness-study.py 1694 1701 True
COMPANION_EXACT True
SOURCE_ROWS_MATCH True
MANIFEST_PIN_MATCH True
```

Both NULL_CHECKS entries had digest_matches=true and kind_null=true. Initial manifest comparison used nonexistent `sha256` and raised KeyError; corrected field `expected_sha256` produced the MANIFEST_PIN_MATCH output above. This was an auditor analysis error, not a candidate failure.

## Residual risk and verification gaps

- These are unsigned retained observations; matching report/receipt fields and committed hashes does not authenticate execution, demonstrate clean clone worktree bytes at execution time, or prove absence of transient writes. No contradictory evidence was found; authenticity is not established.
- Original report already excludes sibling gates, mutation replay, producer selftest and external-source freshness. This audit does not fill those gaps or establish 64/64 monitor credit, C1/C2 satisfaction, runtime/routing/saturation properties or resume continuity.
- `read xd://lsp` returned `No such tool`; semantic references/definition/diagnostics were unavailable. Direct committed-source inspection is the documentary fallback, not semantic proof.
- No tests/builds, candidate execution, external targets, installs, delegation, commits or production edits. Only this seat's d4 report/JSON were written.

Self-evaluation: accuracy 4/5 (unsigned provenance remains); completeness 4/5 (bounded documentary scope, no execution permitted); clarity 4/5 (full historical argv remains in linked receipts); actionability 4/5 (explicit non-admission and gaps); conciseness 4/5 (evidence detail retained). Overall 4.0/5. Improvement: use independently authenticated execution records if stronger provenance is required; no such claim is made here. User-assessment self-check: scope and limitations are explicit.
