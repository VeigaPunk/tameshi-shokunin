# T57W3Read04 — Triggers T1–T3 and the re-pin rule

Recommendation: **verified-record**. Findings: none.

C0b `adf87899c70d616140a81185a8f9acbbdfb30392`; SKILL.md lines 1100–1122; frozen round-18 section SHA256 `2350210704efcc3becfbcd40a63775ad591910039744ac6d072881b3deef7801`.

## Scope and evidence

- Axes: calibration (primary), pointer fidelity, historical pin integrity, zero lane mutation.
- LSP device unavailable: read xd://lsp returned No such tool. Literal searches and pinned-file reads are documentary evidence, not semantic reference proof.
- The section contains policy prose and historical output tokens, not an executable command block. Historical regression results were checked against their C0b receipts; no current-run regression pass is claimed.
- All five directly named pointers resolve. The short RerunSweep.md pointer resolves to .ufo/waves/round-16/w2/RerunSweep.md; the three knowledge pointers resolve under corpus/knowledge/.
- Committed runner history independently reproduces d8abee52 -> 597e1419 -> b56c6e57 -> cf41efaa -> 75ed934d on 2026-10-14: four committed moves. Working-tree transient hashes remain supported by the timestamped round-8 plan, not recoverable committed blobs.
- RerunSweep runner 89722ddb and subsequent selftest runner 0673d2e5 match independently hashed committed bytes. SCR-T6 evidence supports 4/10 under b56c6e57 while the original mado note honestly retains U.
- No in-scope false statement or failing section command found. No code, SKILL content, frozen evidence, tracked lane/fleet file or PATH directory modified. No tools installed.

Read the full section and all cited ranges. T1 historical identities match ledger 301–302 and 328–338. T2 matches RerunSweep 19–24, service protocol 232, mado note 17–23, SCR-T6 draft 243–262, and plan 69–76. T3 and append-only policy match ledger 170–173, 310–312 and 318. Quoted four-leg result matches ledger 281 and kumitate claims 315–322. Base-to-C0b SKILL diff was read; this section is unchanged.

## Executed sweep

Full literal commands, exit statuses and outputs are in `T57W3Read04-receipts/commands.json` and beside this report in JSON. All recorded sweep commands exited 0.

### Command 1

```sh
git -C /fast/scratch/hyaku/tameshi-r57/T57W3Read04/clone rev-parse HEAD
```

Exit: 0. Output: `T57W3Read04-receipts/command-01.txt`.

### Command 2

```sh
git -C /fast/scratch/hyaku/tameshi-r57/T57W3Read04/clone diff 5e3569969b532310d2b8a3d130901757a3df356b adf87899c70d616140a81185a8f9acbbdfb30392 -- SKILL.md
```

Exit: 0. Output: `T57W3Read04-receipts/command-02.txt`.

### Command 3

```sh
sha256sum /fast/scratch/hyaku/tameshi-r57/T57W3Read04/clone/corpus/knowledge/fleet-kill-rate-ledger.md /fast/scratch/hyaku/tameshi-r57/T57W3Read04/clone/corpus/knowledge/service-optin-protocol.md /fast/scratch/hyaku/tameshi-r57/T57W3Read04/clone/corpus/knowledge/mutation-case-mado-verify.md /fast/scratch/hyaku/tameshi-r57/T57W3Read04/clone/plans/round-8.plan.md /fast/scratch/hyaku/tameshi-r57/T57W3Read04/clone/.ufo/waves/round-16/w2/RerunSweep.md
```

Exit: 0. Output: `T57W3Read04-receipts/command-03.txt`.

### Command 4

```sh
git -C /fast/scratch/hyaku/tameshi-r57/T57W3Read04/clone log '--format=%H %aI %s' --reverse -- tools/mutate-and-run.sh
```

Exit: 0. Output: `T57W3Read04-receipts/command-04.txt`.

### Command 5

```sh
python3 -c 'import importlib.util, subprocess
p='"'"'/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-18/measure.py'"'"'
spec=importlib.util.spec_from_file_location('"'"'frozen18'"'"',p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
raw=subprocess.check_output(['"'"'git'"'"','"'"'-C'"'"','"'"'/home/vgpnk/Projects/shokunin/tameshi-shokunin'"'"','"'"'show'"'"','"'"'adf87899c70d616140a81185a8f9acbbdfb30392:SKILL.md'"'"'])
sec=next(s for s in m.sectionize(raw) if s['"'"'heading'"'"']=='"'"'### Triggers T1–T3 and the re-pin rule'"'"')
print(sec['"'"'start'"'"'],sec['"'"'end'"'"'],sec['"'"'sha256'"'"'])
'
```

Exit: 0. Output: `T57W3Read04-receipts/command-05.txt`.

### Command 6

```sh
python3 -c 'import subprocess,hashlib,pathlib
r=pathlib.Path('"'"'/fast/scratch/hyaku/tameshi-r57/T57W3Read04/clone'"'"')
rows=subprocess.check_output(['"'"'git'"'"','"'"'-C'"'"',str(r),'"'"'log'"'"','"'"'--reverse'"'"','"'"'--format=%H %aI'"'"','"'"'--'"'"','"'"'tools/mutate-and-run.sh'"'"'],text=True).splitlines()
for row in rows:
 c,t=row.split(); b=subprocess.check_output(['"'"'git'"'"','"'"'-C'"'"',str(r),'"'"'show'"'"',c+'"'"':tools/mutate-and-run.sh'"'"']); h=hashlib.sha256(b).hexdigest()
 if t.startswith('"'"'2026-10-14'"'"') or h.startswith(('"'"'89722ddb'"'"','"'"'0673d2e5'"'"')): print(c,t,h)
for p,lo,hi in [('"'"'corpus/knowledge/fleet-kill-rate-ledger.md'"'"',297,312),('"'"'corpus/knowledge/fleet-kill-rate-ledger.md'"'"',318,341),('"'"'corpus/knowledge/service-optin-protocol.md'"'"',225,232),('"'"'corpus/knowledge/mutation-case-mado-verify.md'"'"',17,23),('"'"'plans/round-8.plan.md'"'"',69,76),('"'"'.ufo/waves/round-16/w2/RerunSweep.md'"'"',19,24),('"'"'corpus/knowledge/mutation-case-kumitate-claims.md'"'"',315,323),('"'"'plans/round-6-record-draft.md'"'"',243,262)]:
 print('"'"'POINTER'"'"',p,lo,hi)
 lines=(r/p).read_text().splitlines()
 assert len(lines)>=hi
 print('"'"'\n'"'"'.join(str(i)+'"'"':'"'"'+lines[i-1] for i in range(lo,hi+1)))
'
```

Exit: 0. Output: `T57W3Read04-receipts/command-06.txt`.

## Residual risk and verification gaps

Historical scratch logs and uncommitted intermediate runner blobs were not regenerated; findings certify consistency with retained C0b documents and committed runner bytes, not a fresh historical replay. No executable command appears in this section. No runtime admission, broader saturation or resume-continuity claim is made by this scoped reader record.

## Self-evaluation

Accuracy 4/5 (historical scratch unavailable); completeness 5/5 (full assigned section, all direct pointers and runner chain); clarity 4/5 (historical context needs cited sources); actionability 5/5 (exact commands/output retained); conciseness 4/5 (commands are long but reproducible). Overall 4.4/5. Highest-impact improvement: preserve original ephemeral logs in future runs.
