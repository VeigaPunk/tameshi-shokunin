# T57W3Read02 — verified-record

## Scope and identity

Heading: `## Mutation-sweep recipe — numbered steps; bounded cold-read evidence`. Read end to end at C0b `adf87899c70d616140a81185a8f9acbbdfb30392`, lines 159–273.
Frozen round-18 `sectionize(raw)` SHA-256: `77d88c0226463dfc97f0074a5cafedc1044be0a2a16c85fbb6237ac06a5140da`.

Axes: calibration accuracy, executable completeness, pinned provenance, endpoint non-harm.

## Findings, by severity

None. No false statement or failing recipe command found in the assigned section.
Expected red mutant/probe exits are observations, not recipe failures.

## Executed evidence

- **JS:** control `KIMI_CENSUS_SELFTEST: 43/43 pass` / `VERDICT: PASS`, exit 0. Ten unique exact edits; **8 killed, 2 survived, 0 inconclusive**. D2/D10 survived; all mutant summaries retained denominator 43. Every kill's failing labels retained.
- **Bash:** control `SELFTEST: PASS (16 cases)`, exit 0. **14 executed + 2 explicitly skipped** per run, with the real handler deliberately unreachable via `THE_JANITOR_BIN`. Ten unique edits; **8 killed, 2 survived, 0 inconclusive**. B5/B10 survived. B4 failed its token check despite the expected exit 1, exactly as the section explains.
- **Non-equivalence:** pristine empty-root JS printed `+22 more` and `frozen=25`; D2 printed `+23 more`; D10 printed `frozen=24` (each exited 1). Bash pristine non-executable declared-exec row printed `SURFACE DIVERGED … no execute bit` (exit 1); B5 printed `SURFACE OK … (exec 644)` (exit 0). One-row pristine summary had `ok=1`; B10 had `ok=0` (both exit 0).
- **Identity:** source revisions stayed `175de6ba2e9e904010411b19cab27e0af9aad3d4` (JS) and `fecee8743e52eb8fb5fbb40782934cb619a1a96e` (bash). Before/after SHA-256, size, mtime and path porcelain matched; `cmp` passed. JS pin `83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426`, 43273 bytes; bash pin `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f`, 44212 bytes.
- **Pointers:** referenced files and explicit line ranges resolved in the C0b clone (`POINTER SWEEP: PASS`). Read the cited historical notes, dirty-pin erratum, maintained runner count/denominator blocks, adjacent taxonomy and restore policy. Round-16 ledger confirms recipe seats CR04a/CR04b, 18 commands, no blocking gaps, seven minor gaps; no gap-free claim was inferred.

## Residual risk and verification gaps

Only these two historical single-edit suites were replayed; this is not full-page certification, a new canonical admission, an independent promotion, cross-host stability proof, or a continuous non-write proof. Historical timing values remain dated observations. Current Node v26.12.0, bash 5.3.20(1)-release and Python 3.14.8 reproduced the recorded verdicts; actual timings are retained.

LSP was unavailable (`read xd://lsp` → `No such tool`); literal pointer checks are not semantic reference proof. No resume or runtime-routing changes occur in the assigned section. The maintained runner's inconclusive denominator differs from the normative formula, and the section explicitly discloses it. No inconclusive result occurred here.

No source fix proposed; `SKILL.md` and frozen evidence were not edited. No tools installed/updated. The historical one-off driver was rebuilt from the documented manifests; its exact executable source is retained, not assumed to exist in the historical tree. Scratch is removed after receipt retention.

## Receipts and commands

`T57W3Read02-receipts/commands.json` contains every command below with cwd, exit, complete stdout/stderr and duration. `js-sweep.json` and `bash-sweep.json` retain all 22 control/mutant streams and metadata. `mutate_driver.py` retains the executed driver; `section.txt` retains the assigned section. The sibling JSON carries the complete command records.

Commands (absolute scratch paths are historical invocation paths; placeholders were instantiated):

1. Exit 0: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff --stat 5e3569969b532310d2b8a3d130901757a3df356b adf87899c70d616140a81185a8f9acbbdfb30392 -- SKILL.md corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md tools/mutate-and-run.sh`
2. Exit 0: `git clone --shared /home/vgpnk/Projects/shokunin/kagi-shokunin /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kagi-shokunin`
3. Exit 0: `git -C /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kagi-shokunin checkout --detach fecee8743e52eb8fb5fbb40782934cb619a1a96e`
4. Exit 0: `git clone --shared /home/vgpnk/Projects/shokunin/kumitate-shokunin /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kumitate-shokunin`
5. Exit 0: `git -C /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kumitate-shokunin checkout --detach 175de6ba2e9e904010411b19cab27e0af9aad3d4`
6. Exit 0: `node --version`
7. Exit 0: `bash --version`
8. Exit 0: `python3 --version`
9. Exit 0: `git -C /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kumitate-shokunin rev-parse HEAD`
10. Exit 0: `git -C /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kumitate-shokunin status --porcelain -- /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kumitate-shokunin/scripts/kimi-census.mjs`
11. Exit 0: `sha256sum /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kumitate-shokunin/scripts/kimi-census.mjs`
12. Exit 0: `stat -c '%s %y %a' /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kumitate-shokunin/scripts/kimi-census.mjs`
13. Exit 0: `git -C /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kagi-shokunin rev-parse HEAD`
14. Exit 0: `git -C /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kagi-shokunin status --porcelain -- /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kagi-shokunin/corpus/surface-census.sh`
15. Exit 0: `sha256sum /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kagi-shokunin/corpus/surface-census.sh`
16. Exit 0: `stat -c '%s %y %a' /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kagi-shokunin/corpus/surface-census.sh`
17. Exit 0: `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read02/mutate_driver.py --skill /fast/scratch/hyaku/tameshi-r57/T57W3Read02/clone/SKILL.md --target /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kagi-shokunin/corpus/surface-census.sh --work /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash --kind bash --check`
18. Exit 0: `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read02/mutate_driver.py --skill /fast/scratch/hyaku/tameshi-r57/T57W3Read02/clone/SKILL.md --target /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kumitate-shokunin/scripts/kimi-census.mjs --work /fast/scratch/hyaku/tameshi-r57/T57W3Read02/js --kind js --check`
19. Exit 0: `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read02/mutate_driver.py --skill /fast/scratch/hyaku/tameshi-r57/T57W3Read02/clone/SKILL.md --target /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kumitate-shokunin/scripts/kimi-census.mjs --work /fast/scratch/hyaku/tameshi-r57/T57W3Read02/js --kind js --run`
20. Exit 0: `python3 /fast/scratch/hyaku/tameshi-r57/T57W3Read02/mutate_driver.py --skill /fast/scratch/hyaku/tameshi-r57/T57W3Read02/clone/SKILL.md --target /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kagi-shokunin/corpus/surface-census.sh --work /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash --kind bash --run`
21. Exit 0: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff 5e3569969b532310d2b8a3d130901757a3df356b adf87899c70d616140a81185a8f9acbbdfb30392 -- SKILL.md`
22. Exit 1: `node /fast/scratch/hyaku/tameshi-r57/T57W3Read02/js/pristine.mjs --root /fast/scratch/hyaku/tameshi-r57/T57W3Read02/js/empty-root`
23. Exit 1: `node /fast/scratch/hyaku/tameshi-r57/T57W3Read02/js/mutant-D2.mjs --root /fast/scratch/hyaku/tameshi-r57/T57W3Read02/js/empty-root`
24. Exit 1: `node /fast/scratch/hyaku/tameshi-r57/T57W3Read02/js/mutant-D10.mjs --root /fast/scratch/hyaku/tameshi-r57/T57W3Read02/js/empty-root`
25. Exit 1: `bash /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/pristine.sh verify --root /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/probe/host --census /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/probe/census.tsv --shapes /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/probe/shapes.tsv --baseline /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/probe/baseline.tsv`
26. Exit 0: `bash /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/mutant-B5.sh verify --root /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/probe/host --census /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/probe/census.tsv --shapes /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/probe/shapes.tsv --baseline /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/probe/baseline.tsv`
27. Exit 0: `bash /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/pristine.sh verify --root /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/probe2/host --census /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/probe2/census.tsv --shapes /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/probe2/shapes.tsv --baseline /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/probe2/baseline.tsv`
28. Exit 0: `bash /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/mutant-B10.sh verify --root /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/probe2/host --census /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/probe2/census.tsv --shapes /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/probe2/shapes.tsv --baseline /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/probe2/baseline.tsv`
29. Exit 0: `git -C /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kumitate-shokunin rev-parse HEAD`
30. Exit 0: `git -C /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kumitate-shokunin status --porcelain -- /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kumitate-shokunin/scripts/kimi-census.mjs`
31. Exit 0: `sha256sum /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kumitate-shokunin/scripts/kimi-census.mjs`
32. Exit 0: `stat -c '%s %y %a' /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kumitate-shokunin/scripts/kimi-census.mjs`
33. Exit 0: `cmp /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kumitate-shokunin/scripts/kimi-census.mjs /fast/scratch/hyaku/tameshi-r57/T57W3Read02/js/pristine.mjs`
34. Exit 0: `git -C /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kagi-shokunin rev-parse HEAD`
35. Exit 0: `git -C /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kagi-shokunin status --porcelain -- /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kagi-shokunin/corpus/surface-census.sh`
36. Exit 0: `sha256sum /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kagi-shokunin/corpus/surface-census.sh`
37. Exit 0: `stat -c '%s %y %a' /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kagi-shokunin/corpus/surface-census.sh`
38. Exit 0: `cmp /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kagi-shokunin/corpus/surface-census.sh /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/pristine.sh`
39. Exit 0: `python3 -c 'import importlib.util,subprocess; p='"'"'/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py'"'"'; s=importlib.util.spec_from_file_location('"'"'frozen18'"'"',p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); raw=subprocess.check_output(['"'"'git'"'"','"'"'-C'"'"','"'"'/home/vgpnk/Projects/shokunin/tameshi-shokunin'"'"','"'"'show'"'"','"'"'adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md'"'"']); sec=next(x for x in m.sectionize(raw) if x['"'"'heading'"'"']=='"'"'## Mutation-sweep recipe — numbered steps; bounded cold-read evidence'"'"'); print(sec['"'"'start'"'"'],sec['"'"'end'"'"'],sec['"'"'sha256'"'"'])'`
40. Exit 0: `mkdir -p /fast/scratch/hyaku/tameshi-r57/T57W3Read02/js/copy-check/evidence`
41. Exit 0: `cp -p /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kumitate-shokunin/scripts/kimi-census.mjs /fast/scratch/hyaku/tameshi-r57/T57W3Read02/js/copy-check/kimi-census.mjs`
42. Exit 0: `cmp /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kumitate-shokunin/scripts/kimi-census.mjs /fast/scratch/hyaku/tameshi-r57/T57W3Read02/js/copy-check/kimi-census.mjs`
43. Exit 0: `mkdir -p /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/copy-check/evidence`
44. Exit 0: `cp -p /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kagi-shokunin/corpus/surface-census.sh /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/copy-check/surface-census.sh`
45. Exit 0: `cmp /fast/scratch/hyaku/tameshi-r57/T57W3Read02/kagi-shokunin/corpus/surface-census.sh /fast/scratch/hyaku/tameshi-r57/T57W3Read02/bash/copy-check/surface-census.sh`
46. Exit 0: `python3 -c 'from pathlib import Path import re,json root=Path('"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read02/clone'"'"') text=(root/'"'"'SKILL.md'"'"').read_text(); lines=text.splitlines()[158:273]; section='"'"'\n'"'"'.join(lines) paths=['"'"'corpus/knowledge/mutation-case-kimi-census.md'"'"','"'"'corpus/knowledge/mutation-case-kagi-census.md'"'"','"'"'corpus/knowledge/gates-survey-kumitate.md'"'"','"'"'corpus/knowledge/gates-survey-kagi.md'"'"','"'"'corpus/README.md'"'"','"'"'tools/mutate-and-run.sh'"'"','"'"'.ufo/evidence/round-16/coldread/ledger.json'"'"'] for p in paths:  assert (root/p).is_file(),p  print('"'"'POINTER OK'"'"',p) for filename,start,end in re.findall(r'"'"'([A-Za-z0-9/-]+\.(?:md|sh)):(\d+)(?:-(\d+))?'"'"',section):  p=root/filename  if not p.exists(): p=root/'"'"'corpus/knowledge'"'"'/filename  assert p.is_file(),filename  count=len(p.read_text().splitlines()); assert 1<=int(start)<=int(end or start)<=count,(filename,start,end,count)  print('"'"'RANGE OK'"'"',filename,start,end or start) ledger=json.loads((root/'"'"'.ufo/evidence/round-16/coldread/ledger.json'"'"').read_text()) e=next(e for e in ledger['"'"'entries'"'"'] if e['"'"'heading'"'"']=='"'"'## Mutation-sweep recipe — numbered steps; bounded cold-read evidence'"'"') print('"'"'ROUND16'"'"',json.dumps(e,sort_keys=True)) print('"'"'POINTER SWEEP: PASS'"'"') '`
