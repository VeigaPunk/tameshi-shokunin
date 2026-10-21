# FAudit1846 — scoped falsification (2026-10-21)

- **Scope:** strongest claim in `w1/Audit1846.md:91-111`: C1 corrections do not invalidate the historical audit-1846 receipt/ledger binding. Compared its stated 21e observation against explicit delivered revision `55e1d312c4e8ac67aefad80099bd27581ff805c9`; read `.ufo/evidence/round-19/measure.py`. No receipt argv, suite, selftest, build, or formatter was run.
- **Verdict: AGREE, narrowly.** No falsifier found for its no-harm conclusion; this is not C1 admission.

## Evidence

- At 55e, the trace `.ufo/evidence/round-18/coldread/traces/L1/audit-1846.json` still records `rev=a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4`, the original 17 input digests, and argv. Read-only `git cat-file`/SHA-256 comparison gives **16/16 non-page inputs matching**; the sole mismatch is the expected `SKILL.md` page digest (`1334c512…` recorded vs `0e3d7453…` at 55e). The trace inputs do not include the round-18 lesson or the two corrected knowledge files.
- The associated ledger entry remains unique for `(skill_sha256=1334c512…, start=1846)`, `read_rev=a9c94c5…`, `end=1854`; recomputing its section hash using `assemble.py:159-213` gives `ad2320cb7770e47aa5fa628f0a0aa96e751e42c821cff4fe9d0c9fe03af0dcd9`, equal to the entry at 55e. The audit stdout at 55e is still SHA-256 `97e7357a…`, 3264 bytes; stderr is empty.
- The report's page-hash note is dated to its 21e observation: its `4d0190fd…` page hash is stale at 55e. The scoped 21e→55e `SKILL.md` diff shows later changes at lines 1886 and 1932; neither changes section 1846. This freshness correction does not falsify the section-hash carry basis.
- `.ufo/evidence/round-19/measure.py:200-222` separately checks R18-5 against the appended round18-measure receipt. At 55e its receipt JSON has the exact argv `python3 .ufo/evidence/round-18/measure.py --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev 4b7c6823a462f5ea2eafcb262275300a545f3ed7 --explain`, revision 4b7…, exit 0; stdout digest, empty-stderr digest, receipt hash, and pinned round18 instrument hash all match their bytes/metadata. The result records revision=rev_input=4b7…, strict/no overrides, committed ledger, 60/60 sections, full-page flag, restraint score 8, and the lesson's explicit timing caveat. This is a distinct measurement receipt, not a retroactive stdout/argv binding for Audit1846.

## Concrete falsifier and residuals

- **Falsifier:** one non-page input digest in the Audit1846 trace differing at 55e would refute the no-harm assertion; none does (16/16 match), and the independently recomputed section digest also matches.
- Audit1846's own L1/L2 remain open: the round19 measure receipt does not add stdout/stderr digests or revision provenance to the historical Audit1846 trace. Its stated uncertainty about provenance of other historical runs and unre-evaluated asserts remains. L1's final same-ruler before/after measurement and public selftest are outside this review/pending.
- LSP device is not mounted (`xd://lsp` reports no such tool); no semantic-reference/diagnostic claim is made. No tests or installs.
