# SiblingBoundary — round 19 w1 (connector, advisory)

Seat `TameshiR19-2.SiblingBoundary`, 2026-10-21 (reads 02:50–03:05 -03:00).
Everything here was read-only. Question: do the C1 calibration receipt and
metadata repairs stay inside tameshi's province, without absorbing kumitate's
ownership of the `sources-check.mjs` gate? Sources are tameshi `PROVINCE.md`
and the case-8 note.

**Verdict (advisory, not closure): the repairs stay in tameshi.** I found no
absorption in any of these:
- delivered `21e79329f8bdcf01a62be63b3e46db4a7de6b6f9`;
- L1's landed `7af123b`…`cecaefe73482504a814064dd7b2242c8c0b8ad50`;
- L1's uncommitted ruler edit seen at 03:04.

One cross-registry hazard is still open. Kumitate's own `corpus/SOURCES.md`
also has an `S008` row. That row is also `mined` and also opened `2026-10-19`.
The R18-2 predicate tells the two rows apart only by one *mutable* cell,
`used-by`. One bounded move follows below.

## Axes

- **A1 C1 calibration**: the five routed defects, with failure-capable checks.
- **A2 Province boundary**: tameshi absorbs no part of kumitate's gate,
  contract or registry. It also does not hand tameshi-owned registry work to
  kumitate.
- **A3 Evidence boundary**: evidence must separate before from after, and must
  resolve to the right repository.
- **A4 No-harm**: the frozen population, historical bytes, sibling trees and
  depth 8 stay unchanged.

## Evidence (O observed · I inference · U unknown)

| # | Source / command | Outcome |
|---|---|---|
| E1 | tameshi `PROVINCE.md:14-20,37-38,44-45,80-83` (read 2026-10-21) | O. `:16-17` says "Never edits a sibling's gate code (read-only probes; recommendations travel in round reports)." `:20` says "Out of province → report, never absorb." Core (`:37-38`) includes "this lane's runner, corpus and source registry (`corpus/SOURCES.md`)". `:80-83`: kumitate owns `sources-check.mjs` and its contract. |
| E2 | kumitate `PROVINCE.md:15` (worktree = HEAD `cb80bc1`, sha256 `fcd69667…`, last touched `1a8eed5`) | O. Kumitate owns "its learning registry `corpus/SOURCES.md` (checked by `scripts/sources-check.mjs`)". That is kumitate's own registry, not tameshi's. |
| E3 | case-8 note `:11-15`, `:191-195`, `:242-243`, `:263-264`; R18-2 `:266-276`; sweep addendum `:278-282` (all at `cecaefe`) | O. `:13-14` says "tameshi owns the method and this measurement only." R18-2 and its addendum correct only tameshi's `source:` metadata about tameshi's S008 row. They say nothing about the gate's verdicts, its survivors or kumitate's registry. |
| E4 | `git show --stat 21e7932`; `git diff 7243e7f 21e7932`, grepping added lines for `kumitate\|sibling\|sources-check` | O. The commit touches 26 paths, all in the tameshi repository; kumitate is a separate repository. Every hit is one of three things: the case-8 file name, the `contract.json:13` invariant "no sibling gate edits", or the LOG line "no … sibling gate change". |
| E5 | In kumitate, read-only: `git log --all --author=tameshi` and `--committer=tameshi`; author emails since 2026-10-20; `git status --porcelain -- scripts/sources-check.mjs corpus/SOURCES.md PROVINCE.md`; `sha256sum scripts/sources-check.mjs` | O. Both logs return 0. The emails since 2026-10-20 are kumitate, protocol, `t@e` and one operator identity. Status is empty. The gate hashes to `6a293a72…258f`, which equals the case-8 pin; its last touching commit is `0acb775`. So tameshi has no commits in kumitate, and the gate, registry and PROVINCE files carry no edits. I: Git alone cannot rule out unattributed uncommitted writes elsewhere, but the paths that matter are clean. |
| E6 | `tools/bash-witness-study.py:1228-1279 @4b7c682` (R18-4 replay); round-18 `measure.py:47-65,423-445 @4b7c682` (R18-5 replay) | O. The witness selftest builds `git init` fixtures under `/tmp` and runs no kumitate code. The round-18 ruler credits only lane-relative inputs read at REV. For `external` trace paths it checks only whether they sit under the live lane (tameshi's root). It does not re-hash sibling digests. |
| E7 | Drift probe (code below) over `round18-final-measure.stdout` → `coldread.external_inputs` | O. 110 kumitate keys: 95 live-tree paths, 13 rev-pinned keys and 2 `/tmp` scratch paths. Of the 95 live-tree paths, 63 still match kumitate's tree and 32 differ. The differing files include `scripts/claims-check.mjs`, `kimi-census.mjs`, `proxy-check.mjs`, `surface-probe.mjs` and `corpus/SOURCES.md`. `round-gate.mjs`, `sources-check.mjs`, `cite-check.mjs` and `PROVINCE.md` still match. All 13 rev-pinned keys resolve. The receipt prints kumitate `SOURCES.md` as `203b34e6…`, which is the blob at kumitate `1a8eed5`. Kumitate HEAD has held `46caaff9…` since `3d5760a` (00:43 -03:00), before the 02:28 -03:00 replay. I: the printed sibling digests are recorded provenance, not live re-reads. The 60/60 therefore depends only on tameshi's revision and on no sibling state. U: kumitate's working tree at 02:28 was not observed. |
| E8 | `QUALITY.md:328-330`; case-8 ER8-2 `:232-243`; `.ufo/waves/round-18/w2/KumitateRouting.md` | O. The contract's 18 "guard survivors" are tameshi's own survivors in new code: 3 registry-check, 3 evidence-disposition, 2 trace-inputs and 10 bash-witness. They are not case-8's five survivors in kumitate's gate, which stay routed to kumitate. The gate's bytes have not changed since the pin, so none of the routed checks is in the gate yet. Round 19 claims closure for neither group. |
| E9 | `grep '^\| S00[18] '` in both registries; kumitate `git cat-file -e REV^{commit}`; cell-by-cell comparison | O. Kumitate has its own S001 and S008, both `mined`. Comparing kumitate's S008 with tameshi's pinned S008: id, tier, status and opened (`2026-10-19`) are the **same**. The immutable cells source, kind, scope, anchor and teaches differ, and so do the mutable cells recheck and used-by. Tameshi revisions `4b7c682`, `7243e7f` and `21e7932` are absent from kumitate's object store (exit 128). `after-21e7932.json` records `corpus/SOURCES.md` as `3ecc4a09…`, the tameshi blob; kumitate's file is `46caaff9…`. Tameshi's S008 row is byte-identical at `4b7c682`, `7243e7f`, `21e7932` and `cecaefe`. It also matches L1's pinned `source-round18-final.txt` (`018ee9a8…`, which equals tameshi `SOURCES.md` at `4b7c682`). |
| E10 | kumitate `sources-check.mjs @0acb775` (= HEAD blob): `:3-6`, `:123`, `:359-391` | O. `--self DIR` can point the gate at any lane root ("lane root (default: this script's parent directory)"). Its header checks are presence-only regexes plus `\bS\d{3,}\b` tokens read from line 1. Used-by asymmetry is reported only as a warning. |
| E11 | Compare at `7243e7f` and `21e7932` (and the worktree): the first 5 lines of both corrected notes, and the 15 S-rows their line 1 cites | O. All identical, because the corrections are appended below line 5. I: if the sibling gate were run with `--self`, its findings relevant to R18-1/R18-2 would be the same before and after. It cannot measure these corrections. |
| E12 | fleet `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:428-430` | O. The integrator "does not execute a sibling's gate, whose dependencies and write scope are the lane's." |
| E13 | fleet `/home/vgpnk/Projects/shokunin/.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:40-41,49-51` (tameshi `SOURCES.md:4` subscribes to it) | O. `used-by` lists the "paths of the knowledge entries or lessons citing the row". The contract also says "Only `status`, `recheck` and `used-by` change in place". The symmetry and immutability rules L1 now applies come from this fleet contract, not from kumitate. |

## Contradictions (stated, not smoothed)

1. **MetadataDraft misattributes ownership.** `w1/MetadataDraft.md:76` reads:
   "That is a SOURCES used-by gap for the kumitate-side registry; route it, do
   not edit the registry from this seat." That is false. Kumitate's registry
   ends at S032 and has no S063 (count 0). S063 is a tameshi row (E1
   `:37-38`). L1 fixed it inside tameshi's registry at `7af123b`
   (`round-19.md:153-158`), which is consistent with PROVINCE. Mark that
   routing clause superseded. Sending tameshi registry work to kumitate would
   be abdication, the mirror image of absorption.
2. **The hardened opened-date guard does not identify the lane.**
   `measure.py:116 @cecaefe` pins S008's opened date to `2026-10-19`.
   Kumitate's S008 has the same opened date, the same status and the same
   13-field shape (E9). R18-2 still separates the two rows only by the mutable
   `used-by` cell (`:117`).
3. **Anchor nuance (low).** Tameshi `PROVINCE.md:80-81` cites kumitate
   `PROVINCE.md:15` for the contract name `kumitate-sources-v1`. That name
   appears only in `sources-check.mjs:4,55`. Ownership is unaffected, and no
   C1 correction is needed.

## Proposed move (one, bounded): repository-identity binding for R18-2

L1 does the integration; this seat edits nothing.

1. **Ruler.** L1's uncommitted R18-3 hardening already does three things:
   - it parses SOURCES rows into named cells;
   - it pins `source-round18-final.txt` (tameshi SOURCES at `4b7c682`, `018ee9a8…`);
   - it treats every field except status, recheck and used-by as immutable.

   Move `parse` out of `compare_sources` so both checks can call it. Then make
   `source()` also require two things:
   - (a) the `SOURCE_AFTER` pin still holds;
   - (b) every immutable cell of S008 at REV equals S008 in that pinned
     snapshot.

   This reuses L1's existing abstraction instead of adding a second one. It
   needs no literal arXiv string, and it subsumes the opened-date literal.

   For the selftest, take the positive S008 fixture row from the pinned
   snapshot. Add the mutant
   `('foreign-S008-kind', SOURCES, '| paper |', '| own-work |', 'R18-2')`
   next to `immutable-opened`.

   Expected results (I, from reading the code; nothing was run):
   - **Before** (`7243e7f`): stays 0/5. R18-2 is open because the erratum
     heading is absent.
   - **After** (`21e7932` and the final revision): stays 5/5, because the S008
     row is identical (E9).
   - **Foreign-row control**: give S008 kumitate's immutable cells but keep
     tameshi's used-by. Today the hardened ruler reports R18-2 **corrected**,
     because it checks only status, opened, shape and used-by. With the
     binding it reports **open**.
2. **Gate.** Add one reject row to `corpus/lessons/round-19.md` `## Gate`.
   - Candidate: use kumitate `sources-check.mjs` (`kumitate-sources-v1`,
     including `--self`), or any sibling census verdict, as evidence for
     R18-1, R18-2 or R18-3.
   - Decision: reject.
   - Reason: it is kumitate's gate over kumitate's own registry (kumitate
     `PROVINCE.md:15`; tameshi `PROVINCE.md:14-20,80-83`; `PROTOCOL.md:429-430`).
     Its header checks are presence- and token-only
     (`sources-check.mjs:359-391 @0acb775`). Every input it would read for
     these items is byte-identical at `7243e7f` and `21e7932`, so it cannot
     tell before from after.
3. **Bound sentence** for "Measurements and bounds":

   > R18-2 is bound to tameshi's registry by revision `4b7c682` (absent from
   > kumitate), by S008's immutable cells, and by the receipt's
   > `corpus/SOURCES.md` digest. Kumitate's own S001 and S008 are also
   > `mined`, so a recheck of status alone does not discriminate. R18-5's
   > recorded sibling `external_inputs` are provenance only: 32 of 95 kumitate
   > live-tree paths differ at kumitate `cb80bc1` (2026-10-21), so the receipt
   > says nothing about the sibling's current state.

   Item 3 also covers case-8 `:275` ("Verify with that revision's
   `corpus/SOURCES.md` S008 row"). That line sits in a note whose `:3`
   recheck command runs `git -C kumitate-shokunin`. A check by revision fails
   closed in kumitate; a status-only grep run there does not.

Effect on the axes:
- A1 and A3 improve: one more failure-capable negative control, and one
  laundering path closed.
- A2 becomes explicit.
- A4 is unharmed: no change to population, claim or score, no kumitate edit,
  and historical bytes are untouched.

## Risks

- **The ruler changes again.** L1 already plans final before/after
  measurements with the strengthened ruler (`round-19.md:123-125`). Today's
  receipts carry the first ruler, `c538c33d…`; HEAD is `e9b44cad…`, with a
  further worktree edit in progress. Land item 1 before those final
  measurements. Otherwise skip it and keep items 2–3, which are prose only and
  cause no measurement churn, and name the one-cell limit.
- **Point-in-time drift counts.** Kumitate is actively changing its tree
  (round-36 commits between 00:43 and 02:50 -03:00). Cite the counts with
  their timestamp, never as a standing fact.
- **Things not to do.** Do not "confirm" anything by running kumitate's gate,
  editing kumitate's registry, or routing tameshi's S063, S061 or S066 items
  to kumitate.
- **Residuals outside C1** (tameshi-owned, not routed):
  - `guard-kill-closure.md:1` still cites S061, and S061's used-by lacks the
    note (so does S076's).
  - Case-8 `:1` contains the token `S066` inside a draft file name. A
    `\bS\d{3,}\b` reader counts it as a citation; ER8-5 explains it only in
    prose.
  - If the sweep claims that line-1 citations were reconciled, name these
    open.

## Verification (read-only commands)

- In kumitate:
  - `git cat-file -e 4b7c6823…^{commit}` → 128.
  - `grep '^| S008 ' corpus/SOURCES.md` → own-work / mined / 2026-10-19.
  - `log --all --author=tameshi` and `--committer=tameshi` → 0.
  - `status --porcelain` on the gate, SOURCES and PROVINCE → empty.
  - Gate sha256 → `6a293a72…258f`.
- Identity loop: for each `f` and `id`, run `git show REV:f | sed -n 1,5p | sha256sum` and `git show REV:corpus/SOURCES.md | grep "^| $id " | sha256sum`, with REV = `7243e7f` and `21e7932` → identical (E11).
- After item 1:
  - `--selftest` shows the new mutant reopening R18-2.
  - `--rev 7243e7f… --check` → exit 1, 0/5.
  - `--rev <final> --check` → exit 0, 5/5.
  - A `--snapshot` whose S008 carries kumitate's immutable cells → R18-2 open.

Drift probe, exactly as executed: `cd /tmp && python3 - <<'EOF' … EOF`. It
read files and git objects only and wrote nothing.

```python
import json, hashlib, os, subprocess
T='/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-19/round18-final-measure.stdout'
KR='/home/vgpnk/Projects/shokunin/kumitate-shokunin'
env={k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_NOSYSTEM='1')
sha=lambda b: hashlib.sha256(b).hexdigest()
ext=json.load(open(T))['coldread']['external_inputs']
cls={'live-tree':[], 'rev-pinned':[], 'scratch':[]}
for k,v in ext.items():
    if 'kumitate-shokunin' not in k: continue
    if '@' in k: cls['rev-pinned'].append((k,v))
    elif k.startswith(KR+'/'): cls['live-tree'].append((k,v))
    else: cls['scratch'].append((k,v))
same=[k for k,v in cls['live-tree'] if os.path.isfile(k) and sha(open(k,'rb').read())==v]
gone=[k for k,v in cls['live-tree'] if not os.path.isfile(k)]
drift=[k for k,v in cls['live-tree'] if os.path.isfile(k) and sha(open(k,'rb').read())!=v]
print('kumitate keys:', sum(len(x) for x in cls.values()), {c:len(x) for c,x in cls.items()})
print('live-tree: same', len(same), 'drifted', len(drift), 'absent', len(gone))
pin_ok=0
for k,v in cls['rev-pinned']:
    spec=k.split('kumitate-shokunin@',1)[1]; rev,path=spec.split(':',1)
    r=subprocess.run(['git','-C',KR,'show',rev+':'+path],capture_output=True,env=env)
    ok = r.returncode==0 and sha(r.stdout)==v; pin_ok+=ok
print('rev-pinned resolving with recorded digest:', pin_ok, '/', len(cls['rev-pinned']))
for k,v in sorted(cls['live-tree']):
    if '/scripts/' in k:
        st='same' if k in same else ('drift' if k in drift else 'absent')
        print('  script', k.replace(KR,'K'), st)
print('  PROVINCE same?', KR+'/PROVINCE.md' in same, '| SOURCES same?', KR+'/corpus/SOURCES.md' in same)
```

Observed output, 2026-10-21 about 03:00 -03:00:

```text
kumitate keys: 110 {'live-tree': 95, 'rev-pinned': 13, 'scratch': 2}
live-tree: same 63 drifted 32 absent 0
rev-pinned resolving with recorded digest: 13 / 13
  script K/scripts/cite-check.mjs same
  script K/scripts/claims-check.mjs drift
  script K/scripts/kimi-census.mjs drift
  script K/scripts/proxy-check.mjs drift
  script K/scripts/round-gate.mjs same
  script K/scripts/sources-check.mjs same
  script K/scripts/surface-probe.mjs drift
  PROVINCE same? True | SOURCES same? False
```

## Scope and writes

- This report is the only file written.
- One transient file, `/tmp/tameshi-r19-SiblingBoundary-sources.md` (git-show
  output), was created and deleted in the same command.
- Every git call was read-only: `--no-optional-locks`, with `GIT_DIR`,
  `GIT_WORK_TREE` and `GIT_INDEX_FILE` unset. The probe also drops every
  `GIT_*` variable.
- Nothing was run: no gate, selftest, test, build, lint or formatter, and no
  kumitate code.
- No tool was installed or updated.
