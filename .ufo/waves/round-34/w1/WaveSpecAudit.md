# WaveSpecAudit — round-34 wave w1 spec conformance audit

Seat: `tameshi-r34-w1-WaveSpecAudit` (role: reviewer). Audited artifact pair:
`.ufo/waves/round-34/spec-w1.json` (177393 B, sha256 `4731b3250f5b1ee3a2d334f43bf39eba28ce3074b6e0b5b0177203ef041632c2`)
`.ufo/waves/round-34/dispatch-w1.json` (202265 B, sha256 `77336373dd863b03569cae51ae2d36a16be69b8510602e1e67de7a9fdb64e2d5`)
`dispatch-w1.stderr` is empty (0 B, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).

**Verdict: CONFORMS — no actionable defect. All six policy-v2 checks PASS.**

## Verification environment

```
mkdir -p /fast/scratch/hyaku/tameshi-r34-seats/WaveSpecAudit && \
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q --no-hardlinks \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  /fast/scratch/hyaku/tameshi-r34-seats/WaveSpecAudit/lane && \
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C .../lane checkout -q --detach \
  0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7        # exit 0
```

Pinned bytes extracted and verified (`git -C lane show <tip>:<path>`; `sha256sum`):
- `tools/tally-audit-v2.py` → `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` — **matches pin**
- `tools/mutate-and-run.sh` → `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` — **matches pin**
- `git -C lane rev-parse HEAD` → `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`; `git status --porcelain` empty.

Dispatch ordering confirmed: `stat -c %y` gives measure receipt `.ufo/evidence/round-34/measure/c1-deciding-run.{stdout,exit}` mtime `2026-10-23 16:28:02`, spec/dispatch mtime `2026-10-23 16:38:49`; receipt content is the claimed `C1_R33 … C1_R33_PASS=true` line with exit file `0`. Tip commit subject: `round-34: C1 measured true at c17e593b (deciding run receipt) + …` (via `git log --oneline -3`). Wave artifacts themselves are not committed at tip (expected dispatch-time files; `git ls-tree -r <tip>` shows only `.ufo/evidence/round-34/*`).

## Checks (each reproduced by the script in §Reproduce)

| # | Requirement | Result |
|---|-------------|--------|
| 1 | Seat count in band 64–128 | **PASS** — `len(spec.items)=64`; `dispatch.counts={spawn:64,resume:0,total:64}`; `len(taskCall.tasks)=64`; `len(registry.members)=64`; landed `w1/swarm-registry.json` has 64 members. Dispatch `policy.waveMinLanes=64`, `waveMaxLanes=128` encodes the band; 64 ≤ `maxLanes=256`/`hardCeiling=256`/`task.maxConcurrency=300` (config.yml:163). |
| 2 | Attack-role fraction ≥ 25% | **PASS** — 52/64 = **81.25%**. Counting set {reviewer, critic, mutation-tester, sentinel, revenger, labrat}: mutation-tester 28, reviewer 21, critic 1, sentinel 1, revenger 1, labrat 0. Build seats 12 (executor 7, scout 3, connector 1, scribe 1) → mixed build+attack. |
| 3 | Role values from allowed set | **PASS** — 9 distinct roles used: connector, critic, executor, mutation-tester, reviewer, revenger, scout, scribe, sentinel. Every one is a defined agent selector in `~/.omp/agent/config.yml` `task.agentModelOverrides` (lines 164–181). No unknown role; no empty/missing role field. |
| 4 | No planner seat | **PASS** — zero items with `role=="planner"`; zero `taskCall.tasks[].agent=="planner"`; `main` also absent. |
| 5 | Every prompt carries godspeed envelope + absolute-path target | **PASS** — all 64 `prompt` fields start with `---\nname: godspeed` (front matter at offset 0), contain `Godspeed-enabled`, `# Target`, an absolute `/home/vgpnk/Projects/shokunin/tameshi-shokunin/…` and/or `/fast/scratch/…` path, their own scratch dir `/fast/scratch/hyaku/tameshi-r34-seats/<name>` matching the item name, the tip rev `0b99d48e…` in the setup/pin commands, and a `Report:` trailer `.ufo/waves/round-34/w1/<name>.md` matching the name. |
| 6 | No model parameter anywhere | **PASS** — recursive key walk of both JSONs finds zero `model` keys; raw-byte scan finds zero `"model"` key occurrences; `taskCall.tasks[]` carry only `{name, agent, task}`. The only `model` substrings are the bounds text "never pass a model parameter" (spec+shared context). |

## Cross-consistency (spec ↔ dispatch ↔ landed registry)

- `spec.items` names == `dispatch.taskCall.tasks` names == `dispatch.registry.members` names == `w1/swarm-registry.json` members (all 64; symmetric diffs empty; no duplicates).
- `taskCall.context` is byte-identical to `spec.context`.
- For all 64: `tasks[].agent == item.role`, and `tasks[].task == "/skill:godspeed\n\n" + item.prompt + footer`, where the footer's `Judged on:` line equals `", ".join(item.axes)` and its `Report:` line repeats the same `.md` path. So the dispatched payload is the spec prompt plus the `/skill:godspeed` envelope header — envelope satisfied at both levels.
- Registry `members[].role`/`axes` match spec for all 64; all `kind="spawn"`; `item=null` (fresh wave); `resumeSends=[]` consistent with `counts.resume=0`; `registry.path` points at `w1/swarm-registry.json`, `reportDir` == spec `reportDir` == `.ufo/waves/round-34/w1`; `wave` == `round-34-w1` in both files.
- `dispatch.note` prescribes exactly one batched `taskCall` — consistent with the single `{context,tasks}` object present.
- Referenced absolute lane paths in prompts all exist (the lone regex "miss" was a `:176-210` line selector suffix on `c1-measure.py`, which exists). All 14 held-out JSONs referenced by mutation-tester seats exist under `.ufo/evidence/round-33/heldout/`.
- Item schema uniform: every item has exactly `{axes, name, prompt, role}`; every `axes` non-empty; observed axes vocabulary: operability 38, calibration 27, depth 25, freshness 17, quality 4, adjacency 1. Prompts all unique (sha256).

## Observations (not defects)

- **O1 — seat-name/role curiosity:** `LabratPanelReplay` carries role `executor` (build seat), so the `labrat` attack count is 0 despite the name. Names are free-form and `executor` is allowed; attack fraction is unaffected (81.25% ≫ 25%). If the orchestrator intended a labrat attack seat, the role assignment silently reclassified it to build — noting for completeness only.
- **O2 — registry agentIds:** landed `w1/swarm-registry.json` (12 455 B) has all `agentId=null` at audit time (16:43) while peers already run — the registry binds ids lazily/at spawn bookkeeping; outside spec conformance scope.
- **O3 — wave files uncommitted:** spec/dispatch/registry are working-tree artifacts, not in tip tree — consistent with prior waves (dispatch JSONs never appear in `ls-tree` output of earlier round tips either, e.g. round-12/13 dispatch files exist in worktree pattern).

## Residual risk / verification gaps

- I verified the *artifact pair* (spec + dispatch prescription) and the landed registry — not the orchestrator's actual `task` invocation wire-format. The registry showing all-`spawn` kinds is the strongest landed evidence consistent with the prescription.
- Conformance of *content* (whether each prompt's attack instructions are sound, whether the 14 held-out names cover the sealed set correctly) is other seats' job; I checked envelope/referential integrity only.
- "Allowed set" for roles was taken as the operator route table `agentModelOverrides` (the only authoritative role list found); no stricter policy-v2 role whitelist exists in `.ufo/` (grep for `policy.?v2|allowed.?role|roles?.*set` found only historical dispatch files and an r12 lesson noting role/mix precedent).

## Reproduce

```bash
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-34
sha256sum spec-w1.json dispatch-w1.json dispatch-w1.stderr   # pins above
python3 - <<'EOF'                                          # exit 0
import json, re, collections, hashlib, os
spec=json.load(open('spec-w1.json')); disp=json.load(open('dispatch-w1.json'))
items=spec['items']; ATTACK={'reviewer','critic','mutation-tester','sentinel','revenger','labrat'}
assert 64<=len(items)<=128                                    # check 1
atk=sum(i['role'] in ATTACK for i in items)
assert atk/len(items)>=0.25, atk                              # check 2 (52/64)
assert not any(i['role']=='planner' for i in items)           # check 4
def walk(o,p=''):
    if isinstance(o,dict):
        for k,v in o.items():
            assert 'model' not in k.lower(), p+k              # check 6
            walk(v,p+'/'+k)
    elif isinstance(o,list):
        [walk(v,f'{p}[{j}]') for j,v in enumerate(o)]
walk(spec); walk(disp)
tm={t['name']:t for t in disp['taskCall']['tasks']}
for i in items:                                               # check 5
    p=i['prompt']
    assert p.startswith('---\nname: godspeed') and '# Target' in p
    assert f'/fast/scratch/hyaku/tameshi-r34-seats/{i["name"]}' in p
    assert '0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7' in p
    assert f'.ufo/waves/round-34/w1/{i["name"]}.md' in p
    t=tm[i['name']]; assert t['agent']==i['role']
    assert t['task'].startswith('/skill:godspeed\n\n'+p)
print('roles:', collections.Counter(i['role'] for i in items))
print('ALL CHECKS PASS')
EOF
grep -n 'planner\|mutation-tester\|reviewer\|critic\|sentinel\|revenger\|labrat\|executor\|scout\|connector\|scribe' \
  ~/.omp/agent/config.yml        # allowed roles at lines 164-181, exit 0
```

## Tooling

None installed (used system `git`, `python3` 3.x stdlib, `sha256sum`, `stat`). pacman untouched per the pause ruling.
