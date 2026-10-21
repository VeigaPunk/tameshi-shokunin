# Audit1905 — round-18 receipt `audit-1905` (tameshi round 19, w1, advisory)

Seat `TameshiR19-2.Audit1905` (reviewer, read-only), 2026-10-21. Serves the C1 no-harm and
verification boundary. These findings are advisory and do not close anything.

Scope (all paths are relative to `/home/vgpnk/Projects/shokunin/tameshi-shokunin`):
`.ufo/evidence/round-18/final/audit-1905.stdout`, `.ufo/evidence/round-18/final/audit-1905.stderr`,
`.ufo/evidence/round-18/coldread/traces/L1/audit-1905.json`, the ledger entry
`.ufo/evidence/round-18/coldread/ledger.json` `entries[156]` (lines 12567–12611), and the source record that
entry names: `.ufo/waves/round-18/w3/L1Residual.md:730-783`.

Legend: **O** = observed, **I** = inference, **U** = unknown.

## Verdict

The receipt's integrity holds. The retained stdout is a byte-for-byte reproduction of what the trace argv
prints over the committed blobs at `a9c94c5`, and the ledger entry is consistent with the trace. I found
no blocking defect.

There are two low-severity overclaims: what the receipt says it verified goes beyond what its argv
computes.

The C1 repairs do not invalidate the historical record. Two §5 repair targets, though, are hashed inputs
of this receipt (defects 2 and 4). Changing either file retires this receipt's input key at the delivered
revision. Defect 2 has already done so in the worktree, by an append-only edit. Defect 4 must not rewrite
`final/checks.json` in place.

## Axes

The audit checked seven axes:

- **A1** stdout hash
- **A2** argv↔stdout binding
- **A3** revision binding
- **A4** input facts
- **A5** claimed vs computed
- **A6** ledger consistency
- **A7** C1 interaction

## Observations

### A1 — Hashes (O)

| file | sha256 | bytes |
|---|---|---|
| `audit-1905.stdout` (49 lines) | `29c481fff1160208ac61712ba7fed30a88c97bd32c309c2913d2ac851edc03c6` | 5110 |
| `audit-1905.stderr` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) | 0 |
| trace `audit-1905.json` | `19d3c0ce41c3f2da3ae008616d4e2451982fc7f0a0f52ec00cfca3c6220eafb6` | 6155 |
| `ledger.json` | `d654f3d2755c6c7b35a000acfc4e37ff14d0d576c98321c75771c87b65185939` | — |

- **O:** The three receipt files were added only in commit `a134a09` (2026-10-20T18:47:13-03:00), the direct
  child of `a9c94c5` (18:46:21). Their bytes are identical at `4b7c682`, at the frozen baseline `7243e7f`,
  and in the worktree at 2026-10-21T02:52:54-03:00.
  - The ledger is identical at those same three points.
  - Note: `git log --follow` on the empty stderr falsely pairs it with an empty round-1 file (`c7986cd`).
    Without `--follow`, only `a134a09` touches it.
- **O:** No repo file records either digest. I ran grep for `29c481fff1160208|19d3c0ce41c3f2da` with
  gitignore off and got no matches.
  - Trace schema `tameshi-trace-inputs-v1` has no stdout or stderr digest or path field.
  - The ledger entry has none either.
  - See L2.

### A2 — Argv binding (O)

- **O:** I recomputed the argv script's deterministic prints statically from the blobs at `a9c94c5`. The
  receipt argv was not executed and no assert was re-evaluated. The recomputation covers:
  - the `SECTION` line;
  - `SKILL.md` lines 1905–1923;
  - the 16 `OPEN` lines;
  - line 1 and `TAIL[-700:]` of the one `corpus/knowledge/` path;
  - the constant `VERIFIED` line.

  The result is **byte-identical** to the retained stdout: sha256 `29c481ff…`, 5110 bytes. This check could
  have failed if the stdout or any of the 16 hashed inputs differed.
- **O:** Exit 0, an empty stderr and the presence of the `VERIFIED` line agree with each other. Every
  `assert` precedes the final print, and the interpreter runs without `-O`.
- **O:** The trace's `env_overrides` (`PYTHONPYCACHEPREFIX=/tmp/trace-inputs-run-hu7p5r8u/pycache`,
  `git_vars_removed`) describe the tracer's wrapper environment, not the child's.
  - The child runs `env -i` with an explicit list under `--tmpfs /tmp`. That list sets
    `GIT_CONFIG_GLOBAL=/dev/null` and `GIT_CONFIG_NOSYSTEM=1` again and has no `PYTHONPYCACHEPREFIX`.
  - This has no effect on output: the script makes no git or subprocess call.
- **U:** The identity and version of `python3` are not recorded. `PATH` puts mise shims before `/usr/bin`.
  This does not affect this output, since the recomputation is byte-identical.

### A3 — Revision (O / U)

- **O:** Trace `rev` = ledger `read_rev` = `a9c94c5c3a3ae857d7ee25e54fe4cf0f53fbbaa4`, and `rev_reason` is
  null.
- **O:** All 17 trace inputs equal the blobs at `a9c94c5`.
  - At its parent `5923d89`, `.ufo/evidence/round-18/final/registry-branch-aligned.stdout` is absent; it was
    added by `a9c94c5`.
  - The receipts are absent at `a9c94c5` and appear in its child.
  - So the input set is consistent with `a9c94c5` and excludes its parent.
- **O:** The same 17 blobs are also present at `4b7c682` and `7243e7f`. The facts therefore hold verbatim at
  the frozen baseline, but the hashes alone do not single out `a9c94c5` among later commits.
- **U:** The trace does not say how the tracer established `rev` (clone `HEAD` vs. an asserted value). I did
  not open `tools/trace-inputs.py`; it is out of scope.

### A4/A6 — Inputs and ledger (O)

- The trace inputs (17) equal `entries[156].inputs` (16) plus `SKILL.md`, which the ledger moves to
  `inputs_dropped`.
- The trace's `SKILL.md` hash equals `entries[156].skill_sha256`, which equals `_meta.expect_skill_sha`:
  `1334c5128c7e…`.
- `_meta.carry_coverage_basis` is `"section_sha256"`.
- Section hash: ledger `sha256` `1c5c0872…` = sha256(`"\n".join(SKILL.md@a9c94c5 lines 1905–1923)`) = the
  same hash over stdout lines 2–20.
  - The ledger's `end` is 1924 while the executed spec ends at 1923. `SKILL.md@a9c94c5:1924` is `''`, so this
    is a boundary convention and leaves no coverage gap.
- The ledger has a second `start=1905` entry, `entries[114]`: CR49 at `01d586dd`, end 1922, section sha
  `d48c111b…`, 10 traces. It covers superseded section text on a different skill-sha page and does not
  conflict with `entries[156]`.
- `commands_executed_count` = 1 = the length of `traces`.
- `minor_gaps` = 1, matching `L1Residual.md:738`.

### A5 — What the receipt establishes

**Established.** The asserts passed with exit 0, at the hashed bytes:

- `registry-branch-aligned.stdout` has `held==total==31`.
- `probes.stdout` contains `open=0 closed=11 total=11`.
- `regression.stdout` contains `cases=8 passed=8`.
- `historical.stdout` contains `cases=4 passed=4`.
- `case7.stdout` and `case8.stdout` each contain `killed=5 survived=5 inconclusive=0 kill-rate=50%`.
- `disposition` status is `clean`; `before` status is `failed`.
- `repeat.stdout` contains `controls_match`.
- It also establishes the sha256 and byte count of the 16 spec paths, the text of `SKILL.md` lines
  1905–1923, and line 1 and the last 700 characters of `mutation-case-kumitate-sources-check.md`.

**Not established by this receipt.** These items appear only as printed `SKILL.md` or knowledge text, or as
an uncomputed assertion:

- **The kumitate pin.** The printed text gives `0acb775…`, blob sha256 `6a293a…`, 897 lines, mode 100755.
  The script opens no kumitate path: no `kumitate`, `0acb775` or `sources-check.mjs` appears in the argv
  script, and every spec path is lane-local. The trace shows `external: {}`.
  - **U:** Whether the tracer records non-root reads at all.
- **Other case-8 claims:**
  - `10/10 predictions held` (`predictions.json` is only hashed);
  - the `93d22aa`-before-mutants ordering;
  - "eight pristine controls byte-identical" (the relation of `repeat.stdout` `controls_match` to the eight
    controls is not shown);
  - the wave-2 non-equivalence result and ER8-2;
  - the replay argv that produced `regression.stdout`.
- **`final/checks.json`.** It is hashed only, never asserted and never printed.
- **The `VERIFIED` clause on ancestor instrument blobs.** See L1.

## Findings by severity

There are no Critical or High findings.

### M1 (conditional; C1 no-harm boundary) — input-key staleness at the delivered revision

**Evidence (O).** Two inputs of this receipt are §5 repair targets:

- `corpus/knowledge/mutation-case-kumitate-sources-check.md` is defect 2. Its input hash is `dd405bd3…`.
- `.ufo/evidence/round-18/final/checks.json` is defect 4. Its input hash is `fed3c8e6…`.

Both are byte-identical at `a9c94c5`, `4b7c682` and `7243e7f`. The targets of defects 1, 3 and 5 are not
inputs of this receipt.

**Worktree at 2026-10-21T02:52:54-03:00 (O, mid-flight snapshot):**

- **Knowledge file:** now sha256 `a69d9a867b5a…`, 19462 bytes.
  - Its first 18779 bytes equal the receipt input; the edit is **append-only**, adding 12 lines.
  - Line 1 is unchanged.
- **`checks.json`:** unchanged (`fed3c8e6…`).
- **`SKILL.md`:** now `4d0190fd…`, append-only (one line added at EOF).
  - Lines 1905–1923 are byte-identical at the same line numbers, so the `section_sha256` basis is unaffected.

**Effect.**

- The historical facts stay true for `a9c94c5` through `7243e7f`.
- At the delivered revision, `entries[156].inputs` will no longer match the knowledge file.
- **I:** Under input-keyed credit this retained read goes stale there. Precedent: the subject of commit
  `a85f710` (2026-10-20T18:47:45-03:00) is "refresh T2 section after lesson citation edit invalidated one
  retained read".
- **U:** Whether round-19 measurement carries coverage by `section_sha256` alone (it would still match) or
  also requires input equality (it would not). I did not read the rule; it is out of scope.

**Failing criterion, if violated.** A round-19 artifact fails this criterion if it presents section-1905
cold-read credit, or 60/60 coverage, at the delivered revision by citing `entries[156]` without either a
refresh or an explicit stale marking. C1 claims no new cold-read coverage, so the C1 verdict does not
depend on this row.

**Repair-mode constraints:**

- **Defect 4.** Repair it with a new dated receipt or erratum and leave `final/checks.json` at `fed3c8e6…`.
  - Spot-check §5 #4 (`corpus/lessons/round-18-verifier-spotcheck.md:199-200`, read 2026-10-21) says: "Do not
    leave a failed invocation as the selftest row of the final receipt bundle."
  - An in-place rewrite would mutate a retained round-18 receipt; the contract requires errata to be
    appended.
  - It would also break the input hash of this receipt and of any other receipt that hashes the file.
- **Defect 2.** Either option §5 #2 offers ("Sweep the metadata mention or append a correction naming it.",
  `:190-191`) changes the input hash.
  - Neither may touch `audit-1905.stdout:22`. That line is the correct historical record of the stale line 1.

### L1 — The `VERIFIED` line claims more than the argv computes

**Evidence (O).** `audit-1905.stdout:49` (committed in `a134a09`, 2026-10-20) reads: "VERIFIED actual
execution receipts; ancestor runs have the same instrument blobs as the read revision".

- In the argv script (trace line 33), this final print is unconditional.
- The script contains no `git` or `subprocess` call and takes no ancestor revision.

**Failed criterion.** A printed verification should be computed by the receipt's own argv.

- **Clause 1** rests only on substring and JSON-field checks of retained files. Those checks cannot show the
  files came from actual execution.
- **Clause 2** is not computed at all.

**Independent read-only corroboration (O; not established by the receipt, heuristic, no completeness
claim):**

- The ancestors named at `L1Residual.md:738` (`921ef807`, `5923d89`) are both ancestors of `a9c94c5`.
- From each of them to `a9c94c5`, no changed path matches `\.(sh|py|mjs|js|ts)$`, `tools/` or `scripts/`.
  That is 53 and 6 changed paths respectively.
- The `tools/mutate-and-run.sh` blob is equal at both.
- This does not map individual receipts to ancestors.

**Related.** `L1Residual.md:741` labels the command "Pinned-source and committed actual-execution receipt
audit", but it never reads the kumitate pin.

- **I:** The label probably means lane-local files pinned by hash; the wording is ambiguous.

**C1 relevance.** No C1 audit should cite `audit-1905` as evidence of ancestor instrument identity or of the
kumitate pin.

### L2 — No recorded digest binds the receipt pair to its trace

- The pairing rests on three things: the shared filename stem, the same commit (`a134a09`), and
  reconstructibility (A2).
- "Pair bound by a recorded digest" → **fails**.
- "Pair VCS-pinned and byte-reconstructible" → **passes**.
- This is not one of the five routed defects. It remains a residual risk for any new round-19 receipt that
  uses the same schema, such as replacement receipts for defects 4 and 5.

### Info

- **I1:** The ledger's `end` (1924) differs from the executed `end` (1923). Line 1924 is blank and the hash
  convention excludes it, so the two are consistent.
- **I2:** `env_overrides` describe the wrapper's environment, not the child's (A2).
- **I3:** The interpreter identity is unrecorded.
- **I4:** The ledger has two `start=1905` entries: `entries[114]` is superseded and `entries[156]` is current
  per `expect_skill_sha`.

## What this receipt contributes to the C1 measurement

This receipt independently shows **defect 2 present at the frozen baseline**:

- `stdout:22` prints the entry's line 1: "S008 Petrović, Ivanković, Fraser, Just, arXiv 2102.11378 (paper,
  tier A, **queued** — Q1 quote recorded in …, not yet a mined row)".
- The `TAIL` at `stdout:23-24` prints "whose quote now backs registry row **S008**".
- The blob at `7243e7f` equals the hashed input `dd405bd3…`.

It shows the bytes of `checks.json` (defect 4) but not the row's content. It is silent on defects 1, 3
and 5.

## Residual risk / verification gaps

- The worktree hashes are a mid-flight snapshot taken while L1 is the sole writer. Re-check the knowledge
  file, `checks.json` and `SKILL.md` lines 1905–1923 at the delivered revision.
- Tracer semantics (how `rev` is established, whether external reads are captured) were not read.
- The input-keyed credit rule was not read.
- The asserted receipts' contents were not re-evaluated. They are bound only through exit 0 and the listed
  hashes.

## Method (read-only) and scope statement

**Reads:** the receipt pair, the trace, ledger `entries[156]` and `_meta` scalars plus the
`entries[114]` header, `L1Residual.md:715-793`, and spot-check §5.

**Git:** used read-only with all `GIT_*` variables removed and `GIT_OPTIONAL_LOCKS=0`. Only these
subcommands were run: `rev-parse`, `cat-file blob`, `log`, `diff --name-status`, `merge-base --is-ancestor`.

**Not done:**

- no `jj`;
- no git writes;
- no execution of the receipt argv;
- no tests, builds, linters or formatters;
- no tool installs;
- no production edits.

The worktree versions of `SKILL.md` and the knowledge file were hashed and prefix-compared only; their new
content was not read.

**Investigation code** (Python, session kernel). This is the static recomputation that established A2:

```python
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}; ENV["GIT_OPTIONAL_LOCKS"] = "0"
blob = lambda p: subprocess.run(["git","-C",L,"cat-file","blob",f"{RA}:{p}"], env=ENV, capture_output=True).stdout
spec = json.loads(trace["argv"][-1]); sk = blob("SKILL.md").decode().splitlines(); buf = []
buf.append(f"SECTION {spec['start']} {spec['end']}\n" + "\n".join(sk[spec['start']-1:spec['end']]) + "\n")
for p in spec["paths"]:
    raw = blob(p); buf.append(f"OPEN {p} sha256={hashlib.sha256(raw).hexdigest()} bytes={len(raw)}\n")
    if p.startswith("corpus/knowledge/"):
        buf.append(raw.decode().splitlines()[0] + "\n" + "TAIL " + raw.decode()[-700:] + "\n")
buf.append("VERIFIED actual execution receipts; ancestor runs have the same instrument blobs as the read revision\n")
assert "".join(buf).encode() == open(f"{L}/.ufo/evidence/round-18/final/audit-1905.stdout","rb").read()  # held
```

The input comparison hashed `git cat-file blob <rev>:<path>` for each of the 17 trace inputs at
`a9c94c5`, `4b7c682`, `7243e7f` and `a9c94c5^`, and hashed the worktree file.

**Writes:** this report only.
