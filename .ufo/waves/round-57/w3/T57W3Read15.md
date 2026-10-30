# T57W3Read15 — cold-read report

### Round-17 gate/probe registry — re-pin and monitor

Candidate: `adf87899c70d616140a81185a8f9acbbdfb30392`; frozen section lines 1889–1897; SHA256 `309f83283e7518eb00cf7ce4296daf4bf5e80843ff2b3046755eb55d3ba8fb8c`.

Verdict: **gap-minor**.

## Finding (minor)

The documented registry invocation fails at C0b: 51/53 active rows hold, exit 1. sources-census reports an S280 missing id-or-path citation; verify-round15 rejects the changed tools/context-capture.py source pin. The documented exit mapping is accurate; the failure is operability, not a false clean-result claim.

Locations: `SKILL.md:1894; tools/registry.json:576,596`.

Command: `TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read15 python3 tools/registry-check.py --rev adf87899c70d616140a81185a8f9acbbdfb30392 --json`

```text
REGISTRY_CHECK: held=51/53 superseded=7
sources-census expect=0 got=1; SOURCES_CENSUS: VIOLATIONS
no-id-or-path-cite: S280 corpus/knowledge/scratch-root-contract.md (Errors.html)
verify-round15 expect=0 got=1
registered-tool-source-pin: FAIL worktree tools/context-capture.py sha256=831b781054d701d7347df62c4044eb274a775967aaf0ce3d49bef4056b111d8d pinned=c4a1d1658b93c94228acd0f4bee7a29f474367dd62081dace1ae298691601726
```

Full command stdout/stderr: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3Read15-receipts/registry-current.json`. No patch staged.

## Executed commands

All run with cwd `/fast/scratch/hyaku/tameshi-r57/T57W3Read15/clone`; TMPDIR points inside seat scratch. Full stdout/stderr and exit codes are retained in the adjacent receipts directory.

- rc 0: `TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read15 python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-18/dispositions.json --json` — `evidence-current.json`
- rc 2: `TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read15 python3 tools/evidence-disposition.py --root . --dispositions .ufo/evidence/round-17/dispositions.json --json` — `evidence-old.json`
- rc 0: `TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read15 python3 tools/evidence-disposition.py --selftest` — `evidence-selftest.json`
- rc 0: `TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read15 python3 tools/registry-check.py --selftest` — `registry-selftest.json`
- rc 1: `TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read15 python3 tools/registry-check.py --rev adf87899c70d616140a81185a8f9acbbdfb30392 --json` — `registry-current.json`
- rc 0: `TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read15 bash tools/mutate-and-run.sh --selftest` — `runner-selftest.json`
- rc 0: `TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read15 bash tools/mutate-and-run.sh --regression --workdir /fast/scratch/hyaku/tameshi-r57/T57W3Read15/regression` — `runner-regression.json`
- rc 0: `TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read15 python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` — `pin-current.json`
- rc 0: `TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read15 python3 tools/pin-disposition.py --selftest` — `pin-selftest.json`
- rc 2: `TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read15 python3 tools/registry-check.py --rev adf87899c70d616140a81185a8f9acbbdfb30392 --tag t57-no-such-tag --json` — `registry-no-tag.json`
- rc 2: `TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read15 python3 tools/registry-check.py --rev t57-missing-rev --json` — `registry-bad-rev.json`
- rc 64: `TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read15 python3 tools/registry-check.py --unknown-t57` — `registry-usage.json`
- rc 64: `TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read15 python3 tools/evidence-disposition.py --unknown-t57` — `evidence-usage.json`
- rc 2: `TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read15 python3 tools/pin-disposition.py --unknown-t57` — `pin-usage.json`
- rc 2: `TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read15/nonexistent python3 tools/pin-disposition.py --selftest` — `pin-unusable-tmpdir.json`
- rc 0: `TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read15 python3 -c 'import importlib.util,subprocess; p='"'"'/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py'"'"'; s=importlib.util.spec_from_file_location('"'"'r18'"'"',p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); raw=subprocess.check_output(['"'"'git'"'"','"'"'-C'"'"','"'"'/home/vgpnk/Projects/shokunin/tameshi-shokunin'"'"','"'"'show'"'"','"'"'adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md'"'"']); sec=next(x for x in m.sectionize(raw) if x['"'"'heading'"'"']=='"'"'### Round-17 gate/probe registry — re-pin and monitor'"'"'); print(sec['"'"'start'"'"'],sec['"'"'end'"'"'],sec['"'"'sha256'"'"'])'` — `frozen-sectionize.json`
- rc 0: `TMPDIR=/fast/scratch/hyaku/tameshi-r57/T57W3Read15 python3 -c 'from pathlib import Path; paths=['"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read15/clone/tools/evidence-disposition.py'"'"', '"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read15/clone/tools/registry-check.py'"'"', '"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read15/clone/tools/mutate-and-run.sh'"'"', '"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read15/clone/tools/pin-disposition.py'"'"', '"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read15/clone/.ufo/evidence/round-18/dispositions.json'"'"', '"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read15/clone/.ufo/evidence/round-17/dispositions.json'"'"', '"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read15/clone/.ufo/evidence/round-13/pin-manifest.json'"'"', '"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read15/clone/tools/registry.json'"'"']; [(print(p, '"'"'exists='"'"'+str(Path(p).is_file()))) for p in paths]; assert all(Path(p).is_file() for p in paths)'` — `pointer-sweep.json`

## Notes and residual risk

- Axes: calibration accuracy, executable coverage, isolated writes, reproducible evidence.
- All section text (1889–1897) read end to end; round-13 and round-16 exit-map pointers resolve. All eight file pointers exist.
- LSP unavailable: xd://lsp returned No such tool; literal grep used only for line locations, not semantic caller proof.
- The old round-17 manifest exits 2 as documented; current v2 manifest is clean. All four listed tools selftest successfully.
- Pin read is deliberately live fleet-dependent, not a C0b snapshot of sibling state. Regression uses read-only sibling object stores linked into scratch; all ten pinned legs pass. No saturation or independent admission claim.
- No lane content or frozen evidence modified; no tools installed. Findings deferred for L1 adjudication.
- Verification gaps: not every possible exit/input combination was exercised; selftests plus specific negative invocations cover the section error maps. No runtime routing/resume change lies in this section.

## Self-evaluation

Accuracy 4/5 (live sibling readings remain time-dependent); completeness 4/5 (error-map combinations not exhaustive); clarity 4/5 (full registry output is long, preserved separately); actionability 5/5 (two failing rows and exact pin diagnostics retained); conciseness 4/5 (command/hash provenance requires a long snippet). Overall 4.2/5. Highest-impact improvement: adjudicate the two existing active-row failures; do not relabel them as passes.
