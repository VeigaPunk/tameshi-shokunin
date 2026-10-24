# ScoutProtocolAnchor — PROTOCOL anchor for the r36 scratch-unresolvable control input

seat: scout (leaf, read-only findings) · round 37 w1 · lane: tameshi-shokunin
date: 2026-10-24 · scope: rule + line citations violated by the r36 empty-panel control's
scratch-commit input pointer (`91373d55557fe26c431e9e3dd9e8fa4a00d7b57f`)

## The violated rule — PROTOCOL §Evidence standard

`/home/vgpnk/Projects/shokunin/PROTOCOL.md` (`## Evidence standard`, L343–373):

- **L356–358 (primary clause):** "An evidence pointer must resolve at *closure* time, not
  only at write time: paths under `tmpfs` (`/tmp`, `/dev/shm`), session-scoped `local://`
  artifacts, **and any pointer a fresh session cannot reach are not evidence — commit the
  artifact or cite a reproducible command.**"
- **L345–347 (definitional clause):** evidence "means a resolvable pointer: a repo path, a
  command and its output, a commit, or an external document — never a naked assertion. …
  an unreachable claim in a lane report does not exist."
- **L368–369 (adjacent commit-citation clause, same section):** "Commits are cited by hash,
  never by subject or tag" — the r36 receipts do cite by hash, so the defect is
  resolvability (L356–358), not citation form.
- **Appendix provenance:** `PROTOCOL-APPENDIX.md` §"Evidence standard" row (L28) records the
  exact class this falls in — "unresolvable pointers: kake `/tmp/kimi_audit.py`, kumitate
  `local://kumitate-r6-*`, kengaku `/tmp/bench-r7/`" — session/scratch-scoped objects a
  non-author cannot reach.

## The violating input — r36 empty-panel control

Committed receipts name the measured revision as a commit the lane object database does
not contain:

- `.ufo/evidence/round-36/control/v1-at-emptypanel.stdout:8` —
  `rev=91373d55557fe26c431e9e3dd9e8fa4a00d7b57f C1_R35_PASS=true` (exit file `V1_EXIT=0`)
- `.ufo/evidence/round-36/control/v2-at-emptypanel.stdout:8` —
  `rev=91373d55557fe26c431e9e3dd9e8fa4a00d7b57f C1_R36V2_PASS=false` (exit file `V2_EXIT=1`)

Verified unresolvable in the lane repo (run this scout, read-only):

```
$ git -C tameshi-shokunin cat-file -t 91373d55557fe26c431e9e3dd9e8fa4a00d7b57f
fatal: git cat-file: could not get object info
$ git -C tameshi-shokunin cat-file -t d9c496b19371b779ce0eec6dfee1b049b27a3a2d   # lane tip
commit
$ git -C tameshi-shokunin cat-file -t 4f3d8af5b62ba04a5ff825bfdaec6c9193f8489e   # r35 panel tree
tree
```

So: both control receipts are committed and coherent, but their `rev=` input pointer is a
scratch-clone mutant commit unreachable to any fresh session — a per-receipt
L356–358 violation (the receipts exist; their measured-revision input does not resolve at
closure time).

## The r36 verifier spotcheck — the routing citation

`corpus/lessons/round-36-verifier-spotcheck.md` (author: hyaku closure, non-author
integrator) routed this as defect/note #1, L90:

> "(minor, status-neutral) The emptied-panel mutant commit `91373d55…` cited in the two
> control receipts was created in a scratch clone and is not reachable from the lane repo.
> The receipts are committed, coherent, and name the revision measured, and the mutant is
> reconstructable from the committed sealed panel — but a future control should commit the
> mutant tree (or its spec) so every input pointer resolves at closure time
> **(PROTOCOL §Evidence standard)**."

The spotcheck itself: step-1 conformance all-pass (L16–21), C1 re-measured/verified
(L33–52), C2 evidence-verified (L54–65); the defect is expressly **status-neutral** — it
degrades the evidence-pointer class, not the r36 verdicts, and it is what the frozen r37
C1 claim now resolves.

## Frozen r37 C1 linkage (contract already on record)

`.ufo/evidence/round-37/contract.json`:
- L13: before-state = "one live evidence/self-assessment mismatch: the empty-panel
  receipts cite scratch commit `91373d55…`, absent from the lane object database"
- L15: `after_target` requires the old scratch input "explicitly superseded by a committed
  empty-panel specification" + both v1/v2 receipts on a resolvable lane revision
  (v1 PASS / v2 FAIL on the committed zero-specimen input)
- L17 kill_rule: same counter reports one unresolved mismatch at `d9c496b`, zero at the
  final evidence revision
- L32–39 `frozen_control_input`: source panel `.ufo/evidence/round-35/c1/panel` @ tree
  `4f3d8af5…` (9 specimens) → committed replacement
  `.ufo/evidence/round-37/control/empty-panel`

## Observed / inferred / gaps

- **Observed:** rule text (PROTOCOL.md L343–373, appendix L28), spotcheck routing line
  (lesson L90), receipt lines and exit files, git-object resolution results above,
  contract.json freeze.
- **Inference:** the remedy clause is the same sentence as the violated clause —
  "commit the artifact or cite a reproducible command" (L358). The r37 C1 path (committed
  empty-panel spec + lane-resolvable replay receipts) is exactly the "commit the
  artifact" horn; nothing further is needed to classify the fix.
- **Gap (none blocking):** the spotcheck calls the violation "(PROTOCOL §Evidence
  standard)" without a line cite; this report supplies L356–358 as the operative clause
  and L345–347 as the definition it instantiates.
