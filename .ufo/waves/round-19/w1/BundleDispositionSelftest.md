# BundleDispositionSelftest: round-18 `final/checks.json` row `disposition-selftest`

Seat: `TameshiR19-2.BundleDispositionSelftest` (scout, read-only). Date: 2026-10-21.
Scope: only the `disposition-selftest` row in
`.ufo/evidence/round-18/final/checks.json` and its retained `.stdout` / `.stderr` bytes.
Lane HEAD when read: `21e79329f8bdcf01a62be63b3e46db4a7de6b6f9`. Frozen baseline:
`7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`. I did not run the receipt argv or the tool.
This is advisory and does not close anything.

Labels: **O** = observed in bytes or command output; **I** = inference; **U** = unknown.

## Verdict

The row is a **sound current receipt, not a failed raw attempt**. It passes all four
audited axes:

- stdout digest: 1 of 1 matches.
- argv spelling: matches the CLI source.
- exit and output: they agree.
- revision attribution: consistent with the tool bytes.

It is **not** one of the five routed defects (R18-1…R18-5), so it needs no erratum or
supersession. One precision gap is real but not routed. The receipt binds stdout only. It
records no stderr digest, cwd, environment or tool digest. Against round-19 QUALITY 39
("both digests"), it is therefore incomplete *if it were reused as a new final-success
claim*. Recommended treatment: keep it byte-identical and classify it as effective and
not superseded (see §7).

## 1. Row under audit (O)

`checks.json:35-44`:
`argv ["python3","tools/evidence-disposition.py","--selftest"]`,
`revision 921ef8077440f90d092aab4b9fdc750a45de1224`, `exit 0` (JSON int),
`stdout_sha256 a5b86be8cf128d1b2cede3cfe9e5706222bb2b83df1ef86f578f509fe46ef091`.
A strict parse found no duplicate keys. Across all eight rows the schema keys are
exactly `argv, exit, revision, stdout_sha256`. No row has a stderr, cwd or path field. The
row binds to its stream files only by the file-name convention `final/<row-key>.stdout`.

## 2. Digest match count (O)

| Item | Recorded | Retained bytes | sha256 (computed) | Git blob | Match |
|---|---|---|---|---|---|
| stdout | `a5b86be8…ef091` | 3925 B, 64 lines, trailing `\n` | `a5b86be8cf128d1b2cede3cfe9e5706222bb2b83df1ef86f578f509fe46ef091` | `ddba37f0…` | **1/1** |
| stderr | — (not in schema) | 0 B | `e3b0c442…b855` (empty) | `e69de29b…` | unbound (0 recorded) |
| checks.json (container) | `before.json`/`after-21e7932.json` input pin `fed3c8e6…` | 2411 B | `fed3c8e6cba05c41d8fdcafc091328e3092e2018a42fb8a8594bd8b5815c671d` | `d8c98a92…` | 1/1 |

- `a5b86be8…` is unique among the 38 `final/*.stdout` files. It binds exactly one file.
- All three blobs are identical at `5923d89`, `4b7c682`, `7243e7f`, `78b99dd` and
  `21e7932`, and in the working tree (`git hash-object`). The delivered revision changed
  neither this row nor its streams.
- `git log` shows one commit for these paths: `5923d89` (`A`, added), whose parent is
  `921ef80`.

## 3. argv spelling vs CLI source (O)

The CLI source at the claimed revision is the `921ef80:tools/evidence-disposition.py`
blob `683876221797…`, sha256 `66655a3a692b…1f44`. The working tree is byte-identical.

- The docstring at `:120-121` (unchanged since `58e5d53`, 2026-10-20) reads:
  "evidence-disposition.py --selftest / Selftest also requires `jj` for its isolated
  colocated-repository cases." `USAGE` `:168` gives the same spelling.
- `parse_argv` `:3120-3124` accepts the exact literal `--selftest`. Lines `:3155-3157`
  require it alone: "--selftest takes no other arguments". Any other token raises
  `unknown argument` (`:3153-3154`), and `main` maps that to exit 64 (`:3182-3185`).
  `:3186-3187` returns `selftest()`.
- `tools/registry.json:329-335` (last changed `9ee1c80`, 2026-10-20) registers the same
  three-token argv for `evidence-disposition-selftest`.
- Result: the spelling matches. Contrast this with R18-4's `bash-witness-study.py
  --selftest`, which was a usage error. This row has no such defect.

## 4. Exit vs output (O)

- stdout has 63 `SELFTEST_CASE … PASS`, 0 `FAIL`, and the final line
  `SELFTEST: PASS (63/63)`.
- Source `:3089-3101`: on any failure the tool prints `SELFTEST: FAIL (…)` and returns 1.
  Otherwise it prints `SELFTEST: PASS ({passed}/{total})` and returns 0. `exit 0` is the
  only exit consistent with these bytes.
- A static AST enumeration of `selftest()` at the `921ef80` blob found 64 named call
  sites and 63 unique names. `v2-identity-guard` appears twice, at `:3060` (success) and
  `:3066` (exception). The two are mutually exclusive branches.
- After removing that duplicate, the source names equal the 63 observed case names in
  the same order. The three `v2-jj-*` cases are PASS. **I**: jj was on PATH for this run.
- Corroboration: the verifier spot-check `:110` (2026-10-21) reads "Selftest tallies
  (evidence-verified): disposition `SELFTEST: PASS (63/63)`".

## 5. Revision attribution

- **O** `921ef80` is a commit, an ancestor of baseline `7243e7f`, and that baseline is an
  ancestor of HEAD `21e7932`.
- **O** The tool blob `683876…` is identical at all 14 revisions checked from `58e5d53`
  to `21e7932`, including `921ef80` and the retaining commit `5923d89`. It differs before
  that range (`aee4f36` → `22315cc6…`; last earlier change `eb7838b`).
- **O** The selftest reads only `SELF = os.path.realpath(__file__)` (`:136`) plus
  literal fixtures it builds under `/tmp` (`:1719-1722`, `:2350-2351`). The outcome
  therefore depends on the tool bytes and the environment (python, git, jj), not on
  other lane files.
- **O** Timing: stream mtimes are 2026-10-20 18:33:10.71 -0300 (stdout and stderr
  identical) and `checks.json` is 18:33:15.38. Both fall between the `921ef80` commit
  (18:28:40) and `5923d89` (18:40:48).
- **O** Independent corroboration, revision-bound:
  - `final/registry.stdout` was produced by `registry-check.py --rev 921ef80 --json`
    (`live: false`, root `/tmp/tameshi-registry-check-vdbzj6x3/…`). Its sha256
    `fe15a4d0…` equals the `checks.json` `registry` row's `stdout_sha256`.
  - Its `evidence-disposition-selftest` row has `expect 0, got 0, held true`, and its
    `stdout_tail` is byte-equal to all 3925 retained bytes.
  - Two further runs at `5923d89` are byte-equal: `registry-success.stdout` (overall
    exit 1, row held) and `registry-branch-aligned.stdout` (exit 0).
- Limits:
  - **I/O** The `revision` field is an assertion. The digest cannot attribute a run,
    because PASS output is deterministic (no temp paths). Four separate runs produced
    identical bytes. In my predicate, mutant M8 (revision `e08271a`, same blob) also
    passes the attribution check.
  - **U** The working-copy state at about 18:33 is not reconstructed. I used commit-end
    blob identity only. I did not run `jj op log`, to avoid any JJ state risk.
  - **O** The environment is not recorded, and `traced-commands.json` covers 9 other
    commands but no selftest.

## 6. Failed raw attempt vs current evidence

| Artifact | What it is | Tool blob | Disposition |
|---|---|---|---|
| `final/disposition-selftest.stdout` + `checks.json#disposition-selftest` | **current evidence**: 63/63 PASS, exit 0 | `683876…` | effective, not superseded |
| `.ufo/evidence/round-18/c2-probes-e08271a.txt:9-10` | **failed raw attempt** of the *pristine* selftest inside C2 ruler v1: "pristine selftest failed (exit=1): SELFTEST: FAIL (3/63 failed: v2-jj-prebookmark-branch-tip, v2-jj-branch-tip, v2-jj-without-lane-branch…" | same `683876…` (at `e08271a`) | retained by `01d586d` (2026-10-20), subject excerpt: "child PATH carries jj) — v1 tip receipt errored (retained)". The ruler v2 rerun `c2-probes-v2-e08271a.txt` supersedes it, *not* this row. |
| `.ufo/waves/round-18/w2/ReviewSkillDiff.md:57` (2026-10-20) | explains the cause: "Without jj it exits 1: SELFTEST: FAIL (3/63 …). With jj it exits 0 (63/63)." | n/a | explanation, not a receipt |
| `c2-probes-v2-e08271a.txt:1-2`, `final/probes.stdout:1-2` (`SELFTEST: FAIL (1/63 …)`) | **intended mutant kills** (`pristine_exit=0 mutant_exit=1`), not failed attempts | mutants of `683876…` | must not be read as selftest failures |
| round-17 `registry-full-2a22ade.json`, `c2-after-2a22ade.json` (`FAIL (2/56 …)`) | failed runs of an **older tool** (56 cases, pre-`eb7838b`) | different | outside this row |

**I**: the e08271a failure was environment-caused (jj missing on the ruler child PATH),
not a tool defect. Identical tool bytes pass 63/63 when jj is present. The `checks.json`
row does not claim to supersede it and does not launder it.

## 7. Recommended preserved-history treatment

1. **Do not edit `checks.json`.** That includes adding `stderr_sha256` or a
   `superseded_by` field to this row. The bytes must stay `fed3c8e6…`, because
   `.ufo/evidence/round-19/before.json:4` and `after-21e7932.json:4` pin that digest as
   C1 ruler input. Keep `disposition-selftest.stdout` (`a5b86be8…`) and `.stderr`
   (0 B, `e3b0c442…`) byte-identical.
2. **Classify it as effective and not superseded.** Treat it as the round-18
   selftest receipt for tool blob `683876…` at `921ef80`. Do not fold it into R18-4's
   supersession. In `bash-witness-selftest-complete.json`, the only `checks.json`
   pointer in `supersedes` must stay `#bash-witness-selftest`; do not add
   `#disposition-selftest`. No erratum is owed for this row.
3. **Keep the failed raw attempt separate and labelled.** `c2-probes-e08271a.txt:9-10`
   stays as retained ruler-v1 history. My label for it, not a source quote: pristine
   selftest failed because jj was absent on the child PATH. Ruler v2 supersedes it. It
   is not a disposition-selftest receipt and not evidence against the tool.
4. **Append-only limits, if a future note cites this row.** Any such note should be a
   dated append and should state these limits:
   - stdout-only binding; the stderr is empty but unbound;
   - the revision is an assertion, corroborated by blob identity across `58e5d53..21e7932`
     and by the bound `registry --rev 921ef80` run;
   - the environment is unrecorded, and jj is required for 3/63 cases.
5. **Do not retro-repair it under QUALITY 39.** QUALITY 39 is dated round 19
   (`corpus/QUALITY.md:352-358`) and says "a later replay is dated as later". If a
   current claim needs a both-digest receipt for this selftest, make a new, separately
   named, later-dated receipt that names this row as prior evidence. Do not present it
   as a 2026-10-20 receipt.

## 8. Concrete failing criterion

- Against the receipt's own round-18 schema: **none fails**.
- Against round-19 QUALITY 39 (`:352-354`): the row fails on one element only. The
  criterion text is "retained stdout/stderr and both digests"; the stderr digest is
  absent, though the stderr file is retained. This is a schema-wide property of
  `checks.json` and not a routed C1 defect.

## 9. Failure-capable audit predicate (read-only, in-session Python; never imports or runs the tool)

Condensed from the executed cell. Only variable names changed, and the stderr byte-count
print is omitted; the logic is the same.

```python
import ast, hashlib, json, re, subprocess, os, copy
L = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"; F = L + "/.ufo/evidence/round-18/final/"
GENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}; GENV["GIT_OPTIONAL_LOCKS"] = "0"
def git(*a): return subprocess.run(["git", "-C", L, *a], capture_output=True, env=GENV)
def strict_load(b):
    def hook(p):
        ks = [k for k, _ in p]
        if len(ks) != len(set(ks)): raise ValueError("duplicate key")
        return dict(p)
    return json.loads(b, object_pairs_hook=hook)
def cli_literals(src):  # exact flag literals compared against `arg` in parse_argv
    fn = next(n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.FunctionDef) and n.name == "parse_argv")
    lits = set()
    for n in ast.walk(fn):
        if isinstance(n, ast.Compare) and isinstance(n.left, ast.Name) and n.left.id == "arg":
            for c in n.comparators:
                if isinstance(c, ast.Constant) and isinstance(c.value, str): lits.add(c.value)
                elif isinstance(c, ast.Tuple): lits |= {e.value for e in c.elts if isinstance(e, ast.Constant)}
    return lits
def tool_blob(rev):
    p = git("rev-parse", "--verify", "-q", rev + ":tools/evidence-disposition.py")
    return p.stdout.decode().strip() if p.returncode == 0 else None
def audit(row, out, err, retaining="5923d89ac491ec3d296905561a8ab0faf3fda65a"):
    r = {"A1_stdout_digest": hashlib.sha256(out).hexdigest() == row.get("stdout_sha256")}
    rev = row.get("revision", ""); ok40 = bool(re.fullmatch(r"[0-9a-f]{40}", rev or ""))
    src = git("show", rev + ":tools/evidence-disposition.py").stdout if ok40 else b""
    argv = row.get("argv")
    r["A2_argv_spelling"] = (isinstance(argv, list) and argv[:2] == ["python3", "tools/evidence-disposition.py"]
                             and argv[2:] == ["--selftest"] and bool(src) and "--selftest" in cli_literals(src))
    text = out.decode("utf-8", "strict"); lines = text.splitlines()
    cases = [l for l in lines if l.startswith("SELFTEST_CASE ")]
    npass = sum(" PASS (" in l for l in cases); nfail = sum(" FAIL (" in l for l in cases); ex = row.get("exit")
    r["A3_exit_vs_output"] = (type(ex) is int and ex == 0 and nfail == 0 and npass == len(cases) > 0
                              and text.endswith("\n") and lines[-1] == "SELFTEST: PASS ({0}/{0})".format(npass))
    is_commit = ok40 and git("cat-file", "-t", rev).stdout.strip() == b"commit"
    r["A4_revision_attribution"] = bool(is_commit) and tool_blob(rev) is not None and tool_blob(rev) == tool_blob(retaining)
    r["A5_stderr_bound"] = "stderr_sha256" in row
    return r
# mutants: M1 stdout byte flip; M2 argv 'selftest'; M2b '--self-test'; M3 exit False; M4 exit 1;
# M5 failed-raw 3/63 FAIL bytes relabelled exit 0 with recomputed digest; M6 revision '0'*40;
# M7 revision eb7838b (different tool blob); M8 revision e08271a (same blob)
```

Observed results (O):

- **Pristine:** A1 True, A2 True, A3 True, A4 True, A5 False (stderr unbound), stderr 0 B.
- **Mutants:**
  - M1 fails A1 and A3.
  - M2 and M2b fail A2.
  - M3, M4 and M5 fail A3.
  - M6 fails A4, and A2 too, because no source exists at that revision.
  - M7 fails A4.
  - M8 **passes**: this is the documented attribution limit in §5.

## 10. Commands and sources used (O)

- `sha256sum`, `wc -c`, `stat` on `final/disposition-selftest.{stdout,stderr}`,
  `disposition.{stdout,stderr}`, `checks.json` and all `final/*.stdout` → values in §2
  and §5.
- Read-only git with `GIT_OPTIONAL_LOCKS=0`:
  - `log --name-status` on the three paths → single `A` in `5923d89`.
  - `rev-parse <rev>:tools/evidence-disposition.py` on 15 revisions → blob table in §5.
  - `ls-tree` at 5 revisions and `hash-object` on the working tree → identical blobs.
  - `cat-file -t 921ef80` → `commit`.
  - `merge-base --is-ancestor` (both true).
  - `show --stat` on `21e7932` and `78b99dd`; `show --name-status 5923d89`.
  - `log -1` dates for the quoted sources.
- Static AST enumeration of `selftest()`, plus a JSON comparison of the three registry
  `stdout_tail` values against the retained stdout → §4 and §5.
- Files read: `tools/evidence-disposition.py` (`:117-122`, `:2349-2459`, `:3036-3200`,
  plus greps); `tools/registry.json:326-348`; `final/registry.stdout:220-248`;
  `c2-probes-e08271a.txt`; `corpus/lessons/round-18-verifier-spotcheck.md:94-120`,
  `:180-208`; `corpus/QUALITY.md:330-363`; `.ufo/evidence/round-19/before.json`;
  `.ufo/evidence/round-19/measure.py` (grep only).
- No tool or receipt argv was executed. No jj command was run. No install or update.
  The only write is this report.

## 11. Remaining unknowns

- **U** The working-copy contents at the 18:33 capture: whether any uncommitted change
  briefly touched the tool between `921ef80` and `5923d89`. The blob is identical at both
  ends.
- **U** The python, git and jj versions in the 18:33 run. None are recorded.
- **U** The cwd. The relative argv implies the lane root, but nothing records it.
