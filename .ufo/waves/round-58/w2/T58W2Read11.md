# T58W2Read11 — verified-record

## Scope and identity

- C0: `8063d0a551fc5b3cb5a2d397da7353af53444534`; lane log confirmed newest dispatch commit.
- Read end to end: `### Round-13 gate/probe registry`, frozen sectionizer lines **1590–1605**.
- SHA256: `896722c4941841f228810678befe82e9910cc66eb67c3de45d7561ce4668566d`.
- Axes: factual accuracy, runnable commands, pointer integrity, calibrated historical authority.
- Shared scratch clone checked for its own toplevel before detached checkout at C0. No implementation edits.

## Findings by severity

None. All four listed commands ran successfully against C0 tools. Exact argv, cwd, exit codes and complete outputs are in `T58W2Read11.json` and `T58W2Read11-receipts/commands.json` beside this report. Absolute clone paths replace the section's relative tool/input paths; the documented fleet root is unchanged.

| Sweep | Observed output | Exit |
|---|---|---|
| `python3 /fast/scratch/hyaku/tameshi-r58/T58W2Read11/clone/tools/pin-disposition.py --manifest /fast/scratch/hyaku/tameshi-r58/T58W2Read11/clone/.ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` | `status: ok`, six legs, `result_reuse: not_established` | 0 |
| `python3 /fast/scratch/hyaku/tameshi-r58/T58W2Read11/clone/tools/pin-disposition.py --selftest` | `SELFTEST: PASS (19/19)` | 0 |
| `python3 /fast/scratch/hyaku/tameshi-r58/T58W2Read11/clone/tools/witness-metadata.py --check --companion /fast/scratch/hyaku/tameshi-r58/T58W2Read11/clone/.ufo/evidence/round-13/witness-metadata.json` | `WITNESS_METADATA: metadata_consistent reason=ok exit=0`, four verified inputs | 0 |
| `python3 /fast/scratch/hyaku/tameshi-r58/T58W2Read11/clone/tools/witness-metadata.py --selftest` | `SELFTEST: PASS 39/39` | 0 |
| `python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w2/T58W2Read11-receipts/sweep.py` | `1590 1605 896722c4941841f228810678befe82e9910cc66eb67c3de45d7561ce4668566d`; all eight file pointers resolved; seventh-case heading resolved; `SCOPED_DIFF_BYTES 0`; `SCOPE_SWEEP_COMPLETE` | 0 |

The sweep script loads the required frozen round-18 sectionizer using importlib and reads the exact C0 git blob. Full sweep output is retained in `T58W2Read11-receipts/sweep-output.txt`.

## Notes and residual risk

- Registry tools and SKILL.md have no base-to-C0 diff. Runtime checks nevertheless exercised both entries and both selftests, including documented error classifications.
- The historical producer SHA in the frozen summary is `249d9dcd2dfb410f7e6847989da2cb3ab6ef7dd693b87ec2b9b4d6b193d43f1a`; current producer SHA is `f2bb50c77a6b6ffc53fd4e31d06c729f9cface7c1684f232c060f6a4978bf261`. Companion checking deliberately retains the former. This validates retained identity, not independent historical execution authentication.
- S048 still supersedes S047 as stated; S266 subsequently updates S048's anchor/quote only. Mentioning S266 would improve freshness, not correct a false statement. The seventh-case heading and bounded historical wording agree.
- LSP device unavailable (`read xd://lsp`: `No such tool`); text searches were navigation only, not semantic proof. Definitions and executable selftests supply the bounded contract evidence.
- Live fleet observations are intentionally mutable and are not presented as frozen C0 sibling state. This scoped sweep does not establish C2 admission, hostile-runner integrity, or universal absence of defects.

## Cleanup and self-check

Scratch `/fast/scratch/hyaku/tameshi-r58/T58W2Read11` removed before delivery; existence check returned false. No tools installed. No lane implementation or prior-round evidence was edited.

Self-evaluation: accuracy 4/5 (historical execution remains unauthenticated); completeness 4/5 (bounded selftests, not exhaustive adversarial execution); clarity 4/5 (full output necessarily delegated to receipts); actionability 5/5 (reproducible script and exact outputs); conciseness 4/5 (table repeats argv for auditability). Overall 4.2/5. Highest-impact improvement is an explicit S266 link; no actionable false statement remains in assigned scope.
