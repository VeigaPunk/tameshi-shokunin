# T58W1Panel04 — blind panel

Base: `2a32aa8228d5f86a85c81a923a3148bf792a9538`.
Axes: calibration accuracy, evidence completeness, blind independence.

## Open findings, by severity

### R53.1 — material counter defect — open

` .ufo/evidence/round-53/c1/measure.py` lines 94–100 still execute:

```python
r = git(['-C', lane, 'ls-tree', '--name-only', rev,
         '.ufo/evidence/round-21/coldread'])
rekey_dirs = [n for n in r.stdout.decode().split('\n')
              if re.fullmatch(r'rekey-r53-[0-9a-f]{12}', n)]
```

Command actually run in the detached base clone:

```
git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel04/clone ls-tree --name-only HEAD .ufo/evidence/round-21/coldread
.ufo/evidence/round-21/coldread
exit=0
```

The returned full directory path cannot match the basename-only regular expression. This is direct static resolution evidence, not a rerun of the full counter. The requested discovery repair is absent, so the compound item remains open regardless of other counter arms.

### R53.2 — missing deciding evidence — open

```
git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel04/clone ls-tree -r --name-only HEAD .ufo/evidence/round-53/after
[empty stdout]
exit=0
```

`git show HEAD:LOG.md`, lines 2489–2490, still says `Deciding receipts: .ufo/evidence/round-53/after/`. `git show HEAD:SCORECARD.md`, lines 2506–2507, still says `final deciding revision recorded in .ufo/evidence/round-53/after/`. Neither the receipts nor the requested pointer correction is present. The scoped `git log --format='%H %s' -- .ufo/evidence/round-53/c1/measure.py .ufo/evidence/round-53/after` records counter amendments but no after-directory landing.

### R52.6 — report-contract repair — open, evidence-limited

```
git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel04/clone ls-tree -r --name-only HEAD .ufo/reports
.ufo/reports/round-1/tameshi.md
exit=0
```

The lane's later lesson `corpus/lessons/round-53.md` (read lines 1–128) has no Landed changes, Before → after or per-box SHONEN section; it is a lesson rather than the canonical fleet report. Later closure documents contain partial report-shape observations, but I do not substitute another reviewer's conformance judgments for independently located report bytes. The required canonical successor reports are not in the specified base lane tree. **INFERENCE:** the complete compound repair is not established at base; this verdict does not assert that every fleet successor report failed. No reasoned decline of this complete item was located. This is the principal calibration uncertainty in this panel.

## Fixed items

### R52.4 — fixed

Resolving ancestor: `6db1d220b337c35ff1e25bf9cfd74abc9db1498d`.

```
git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel04/clone show --format=fuller --stat 6db1d220b337c35ff1e25bf9cfd74abc9db1498d
```

Located introduced-file excerpt:

```
round-52 w3: commit wave markers and integrate script (closure salvage)
.ufo/evidence/round-52/integrate/build-readers.py | 41 +
.ufo/waves/round-52/w3.ready | 1 +
.ufo/waves/round-52/w3.ready.dispatched | 2 +
.ufo/waves/round-52/w3/T52W3ConnShonen.md | 16 +
...
80 files changed, 8295 insertions(+)
```

A separate `git ls-tree --name-only BASE` over the four named paths returned the integrate script, both marker files and the committed w3 children. The marker's introduced content includes `"lane":"tameshi","round":52,"wave":"w3"`. The defect is disposition of those specific leftovers, not a claim that future rounds never create new untracked files.

### R52.5 — fixed

Resolving ancestor: `218bc6b5c25d6a3c57dd44600febd552f0167cee`.

```
git -C /fast/scratch/hyaku/tameshi-r58/T58W1Panel04/clone show 218bc6b5c25d6a3c57dd44600febd552f0167cee -- tools/registry-check.py
```

Actual introduced diff:

```diff
- work = tempfile.mkdtemp(prefix="tameshi-registry-check-", dir="/tmp")
+ work = tempfile.mkdtemp(prefix="tameshi-registry-check-", dir=tempfile.gettempdir())
```

The same commit replaces the selftest's `dir="/tmp"` with `dir=tempfile.gettempdir()`. At base, lines 761–772 define `strict_scratch_root()` with `t = _os.environ.get("TMPDIR")`, return usable `t`, otherwise return `tempfile.gettempdir()`. Line 784 passes `dir=strict_scratch_root()`; selftest lines 934–935 use the same helper. The hard-coded-root defect is resolved; later strictness changes do not undo it.

For each fixed hash I ran `git -C CLONE merge-base --is-ancestor HASH HEAD`: both returned exit 0 with empty stdout. `git -C CLONE rev-parse HEAD` returned the exact base hash.

## Receipts, scope and gaps

Full command/output receipts: `T58W1Panel04-receipts/git-evidence.txt`; line-numbered base excerpts and corresponding `git show` commands: `T58W1Panel04-receipts/excerpts.txt`.

Created a shared clone at `/fast/scratch/hyaku/tameshi-r58/T58W1Panel04/clone`, asserted its top-level identity before detached checkout, and reviewed only the assigned base. No lane source edits or staging proposals. No forbidden round-57 panels, round-58 peer outputs, or candidate defect rows were opened. No runtime tests were run; this assignment's proof is tracked-tree/history inspection plus the live `ls-tree` discovery probe. No saturation or runtime-admission claim.

LSP device was unavailable: `read xd://lsp` returned `No such tool: xd://lsp`. Text searches were literal discovery fallback, not semantic caller proof. No tools installed or updated. Scratch was deleted with `rm -rf -- /fast/scratch/hyaku/tameshi-r58/T58W1Panel04` (exit 0) before this report was written.

Self-evaluation: accuracy 4/5 (R52.6 has explicit fleet-report visibility uncertainty); completeness 4/5 (all five items judged, but canonical successor report bytes unavailable in base); clarity 4/5 (compound R52.6 warrants the longer caveat); actionability 4/5 (resolving hashes and open failure paths supplied; external report evidence could change R52.6); conciseness 4/5 (retained excerpts required by panel contract). Overall 4.0/5. Highest-impact improvement would be base-anchored canonical successor-report evidence for R52.6; this panel does not invent it.
