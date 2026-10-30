# T58W2RevRows3 — R54 row re-verification

C0 `8063d0a551fc5b3cb5a2d397da7353af53444534`; base `2a32aa8228d5f86a85c81a923a3148bf792a9538`. Axes: semantic accuracy, provenance, calibration.

## Findings (severity order)

**Low — R54.5/R54.6: disclosed semantic underclaims, not false fixes.** Both are installed `open` / `status_at_base=open`, but the original asks are repaired at base and C0. This is deliberately distinguished from instrument qualification in the ledger and newest Planned paragraph (SCORECARD.md:2833-2834). Keep that distinction explicit; no fabricated fix is warranted.

Commands and observed outputs:

```text
$ python3 /fast/scratch/hyaku/tameshi-r58/T58W2RevRows3/clone/.ufo/waves/round-55/w1/T55W1Er05-receipts/derive_counts.py /fast/scratch/hyaku/tameshi-r58/T58W2RevRows3/clone 2a32aa8228d5f86a85c81a923a3148bf792a9538 w1
T54W1Read01.json findings=1
T54W1Read02.json findings=2
T54W1Read03.json findings=2
T54W1Read04.json findings=0
T54W1Read05.json findings=3
T54W1Read06.json findings=0
T54W1Read07.json findings=0
T54W1Read08.json findings=4
T54W1Read09.json findings=0
T54W1Read10.json findings=2
T54W1Read11.json findings=1
T54W1Read12.json findings=0
T54W1Read13.json findings=1
T54W1Read14.json findings=0
T54W1Read15.json findings=2
T54W1Read16.json findings=1
T54W1Read17.json findings=0
T54W1Read18.json findings=1
T54W1Read19.json findings=4
T54W1Read20.json findings=1
T54W1Read21.json findings=2
T54W1Read22.json findings=0
T54W1Read23.json findings=1
w1: reader_files=23 findings=28 sections_with_findings=15
exit=0
$ python3 /fast/scratch/hyaku/tameshi-r58/T58W2RevRows3/clone/.ufo/waves/round-55/w1/T55W1Er05-receipts/derive_counts.py /fast/scratch/hyaku/tameshi-r58/T58W2RevRows3/clone 2a32aa8228d5f86a85c81a923a3148bf792a9538 w2
T54W2Read01.json findings=1
T54W2Read02.json findings=2
T54W2Read03.json findings=1
T54W2Read04.json findings=1
T54W2Read05.json findings=1
T54W2Read06.json findings=1
T54W2Read07.json findings=1
T54W2Read08.json findings=0
T54W2Read09.json findings=0
T54W2Read10.json findings=0
T54W2Read11.json findings=0
T54W2Read12.json findings=0
T54W2Read13.json findings=0
T54W2Read14.json findings=0
T54W2Read15.json findings=2
T54W2Read16.json findings=2
T54W2Read17.json findings=0
T54W2Read18.json findings=1
T54W2Read19.json findings=1
T54W2Read20.json findings=0
T54W2Read21.json findings=0
T54W2Read22.json findings=11
T54W2Read23.json findings=0
w2: reader_files=23 findings=25 sections_with_findings=12
exit=0
$ python3 /fast/scratch/hyaku/tameshi-r58/T58W2RevRows3/clone/.ufo/waves/round-55/w1/T55W1Er05-receipts/derive_counts.py /fast/scratch/hyaku/tameshi-r58/T58W2RevRows3/clone 8063d0a551fc5b3cb5a2d397da7353af53444534 w1
T54W1Read01.json findings=1
T54W1Read02.json findings=2
T54W1Read03.json findings=2
T54W1Read04.json findings=0
T54W1Read05.json findings=3
T54W1Read06.json findings=0
T54W1Read07.json findings=0
T54W1Read08.json findings=4
T54W1Read09.json findings=0
T54W1Read10.json findings=2
T54W1Read11.json findings=1
T54W1Read12.json findings=0
T54W1Read13.json findings=1
T54W1Read14.json findings=0
T54W1Read15.json findings=2
T54W1Read16.json findings=1
T54W1Read17.json findings=0
T54W1Read18.json findings=1
T54W1Read19.json findings=4
T54W1Read20.json findings=1
T54W1Read21.json findings=2
T54W1Read22.json findings=0
T54W1Read23.json findings=1
w1: reader_files=23 findings=28 sections_with_findings=15
exit=0
$ python3 /fast/scratch/hyaku/tameshi-r58/T58W2RevRows3/clone/.ufo/waves/round-55/w1/T55W1Er05-receipts/derive_counts.py /fast/scratch/hyaku/tameshi-r58/T58W2RevRows3/clone 8063d0a551fc5b3cb5a2d397da7353af53444534 w2
T54W2Read01.json findings=1
T54W2Read02.json findings=2
T54W2Read03.json findings=1
T54W2Read04.json findings=1
T54W2Read05.json findings=1
T54W2Read06.json findings=1
T54W2Read07.json findings=1
T54W2Read08.json findings=0
T54W2Read09.json findings=0
T54W2Read10.json findings=0
T54W2Read11.json findings=0
T54W2Read12.json findings=0
T54W2Read13.json findings=0
T54W2Read14.json findings=0
T54W2Read15.json findings=2
T54W2Read16.json findings=2
T54W2Read17.json findings=0
T54W2Read18.json findings=1
T54W2Read19.json findings=1
T54W2Read20.json findings=0
T54W2Read21.json findings=0
T54W2Read22.json findings=11
T54W2Read23.json findings=0
w2: reader_files=23 findings=25 sections_with_findings=12
exit=0
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W2RevRows3/clone rev-parse ff2a821:.ufo/waves/round-54/w2/T54W2Sent03.md
7448be1be6510bfc261b5b120ce14c0a54489d88
exit=0
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W2RevRows3/clone rev-parse 2a32aa8228d5f86a85c81a923a3148bf792a9538:.ufo/waves/round-54/w2/T54W2Sent03.md
7448be1be6510bfc261b5b120ce14c0a54489d88
exit=0
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W2RevRows3/clone rev-parse 8063d0a551fc5b3cb5a2d397da7353af53444534:.ufo/waves/round-54/w2/T54W2Sent03.md
7448be1be6510bfc261b5b120ce14c0a54489d88
exit=0
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W2RevRows3/clone rev-parse ff2a821:.ufo/waves/round-54/w2/T54W2Sent03-receipts/c1committed-positive.stdout
c63fc96c958c09377f2e8eb56fced010c7d11dba
exit=0
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W2RevRows3/clone rev-parse 2a32aa8228d5f86a85c81a923a3148bf792a9538:.ufo/waves/round-54/w2/T54W2Sent03-receipts/c1committed-positive.stdout
c63fc96c958c09377f2e8eb56fced010c7d11dba
exit=0
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W2RevRows3/clone rev-parse 8063d0a551fc5b3cb5a2d397da7353af53444534:.ufo/waves/round-54/w2/T54W2Sent03-receipts/c1committed-positive.stdout
c63fc96c958c09377f2e8eb56fced010c7d11dba
exit=0
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W2RevRows3/clone rev-parse ff2a821:.ufo/waves/round-54/w2/T54W2Sent03-receipts/rejection-attribution.txt
4cdc204cd232a2df6321ef9217810037dfd9e7ff
exit=0
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W2RevRows3/clone rev-parse 2a32aa8228d5f86a85c81a923a3148bf792a9538:.ufo/waves/round-54/w2/T54W2Sent03-receipts/rejection-attribution.txt
4cdc204cd232a2df6321ef9217810037dfd9e7ff
exit=0
$ git -C /fast/scratch/hyaku/tameshi-r58/T58W2RevRows3/clone rev-parse 8063d0a551fc5b3cb5a2d397da7353af53444534:.ufo/waves/round-54/w2/T54W2Sent03-receipts/rejection-attribution.txt
4cdc204cd232a2df6321ef9217810037dfd9e7ff
exit=0
```

`git -C /fast/scratch/hyaku/tameshi-r58/T58W2RevRows3/clone show 2a32aa8228d5f86a85c81a923a3148bf792a9538:SCORECARD.md` contains ER-R54-5 (`w1=28 w2=25 sections=12`) and ER-R54-6 (three deliverables committed at `ff2a821`). Full outputs in receipts/commands.json (actual directory: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w2/T58W2RevRows3-receipts`).

## Per-id decisions

- **R54.1 — agree**: CTL_POS_c1 failed (3/7; CONTROLS_B 2/3); SCORECARD ER-R54-1 and QUALITY explicitly retract the false pass. Current round-58 guard requires equal tallies, no CTL_MISMATCH and exit 0.
- **R54.2 — agree**: ER-R54-2 identifies 077d431e, matching after/frozen.stdout and five freeze amendments.
- **R54.3 — agree**: ER-R54-3 and the live C2 row state total=13, exactly matching before/c2.stdout.
- **R54.4 — agree**: ER-R54-4 states 8528ee85; committed counter SHA256 exactly matches freeze.json.
- **R54.5 — disagree-semantic-underclaim**: Semantically fixed already at base: ER-R54-5 gives 28 wave-1 findings, 25 wave-2 findings in 12 sections. Independent committed-reader derivations at base and C0 agree; resolutions.json has 12 entries/25 findings. Open is an explicitly disclosed instrument-qualified underclaim, not missing semantic repair.
- **R54.6 — disagree-semantic-underclaim**: Semantically fixed already at base: ff2a821 adds all three deliverables; blob ids are identical at ff2a821, base and C0. Dirty measurement remains honestly preserved. Open is an explicitly disclosed instrument-qualified underclaim.
- **R54.7 — agree**: ER-R54-7 says renamed; git show --find-renames reports R100 and retains the incident file.
- **R54.8 — agree**: Substantive round-55 lesson row and seat SUPERSEDED appendix withdraw authorization and record the host-write incident. The historical operator-turn characterization is separately corrected. Incidental round-54 heading is not counted as proof.
- **R54.9 — agree**: Registry gives reviewers=5, seats=76, attacks=21 (27.6%); live source package has 81 markdown entries. ER-R54-9 matches; round-54 lesson says other 80 (one adopted).
- **R54.10 — agree**: ER-R54-10 attributes 0/7 to controls-a.stdout and 0/30 to the round-53 counter receipt; both committed receipts agree.

## Provenance sweep

All installed excerpts resolve at C0. Every fixed row has at least one substantive keyed excerpt introduced by 9cf0146b, absent at routing, and present already at base; that commit is ancestor of base and C0 (all merge-base commands exit 0). Extra stale/heading-only excerpts were not treated as resolution proof. Detailed individual checks: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w2/T58W2RevRows3-receipts/evidence-checks.json`. Full executed git commands, stdout, stderr and exit codes: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-58/w2/T58W2RevRows3-receipts/commands.json`; reader counts and derived arithmetic are beside it. Resolutions sum: 12 sections/25 findings. C2 SHA256: `8528ee8555da068519af4159f5f9e0efac8b29de88a53534a7043d7ec007e790`. No lane implementation or frozen evidence was edited.

## Residual risk / verification gaps

- No false fixed disposition found in the eight fixed rows.
- Historical host history.db content and present host config were not independently read; review establishes the committed supersession and incident lesson, not current host state.
- Package count is a live read and agrees with retained round-55 inventory; historical external package bytes are not lane-pinned.
- LSP device unavailable: read xd://lsp returned No such tool; no references/definition/diagnostics server available. Used git-object and literal checks, not semantic-LSP proof.
- Did not run full deciding runtime or C1/C2 acceptance counter; no admission recommendation. Runtime identity, resume and saturation are outside these record-only rows.

Scratch clone deleted before yielding. No tools installed.
