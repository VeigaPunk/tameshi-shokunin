# ColdReadKnowledgeWitness — cold-read re-credit of `corpus/knowledge/witness-equivalence-rule.md` (round 34 w1)

Seat: `tameshi-r34-w1-ColdReadKnowledgeWitness` · Date: 2026-10-23 · Lane tip: `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`
Method: cold read at TIP bytes in a scratch clone; the only counter execution was `import` of module functions on scratch copies (kill rule consumed; no default-mode run was attempted). Lane untouched; no writes outside scratch + this report.

**Verdict: the doc re-credits. All four rule bullets match `ho_witness_ok`'s branches, all Evidence pointers exist and say what the doc claims, both S-citations resolve to registry rows with verifiable digests, and the two historical claims (set-blind predecessor, shorter-vector degeneration) are confirmed against committed predecessor bytes. One minor doc defect (F1), one wording observation (O1). The deciding run stands; nothing here re-scores it.**

## 0. Environment and pinned bytes

```
S=/fast/scratch/hyaku/tameshi-r34-seats/ColdReadKnowledgeWitness
mkdir -p $S && env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin $S/lane   # exit 0
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  git -C $S/lane checkout -q --detach 0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7        # exit 0; rev-parse --short HEAD -> 0b99d48
git -C $S/lane show 0b99d48e...:tools/tally-audit-v2.py  > $S/tool.py      # exit 0
git -C $S/lane show 0b99d48e...:tools/mutate-and-run.sh  > $S/pristine.sh  # exit 0
sha256sum $S/tool.py $S/pristine.sh
```

- `tool.py` → `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` — equals the frozen pin.
- `pristine.sh` → `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` — equals the frozen pin.
- Counter at TIP `.ufo/evidence/round-33/c1/c1-measure.py` → `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` — equals the amendment-6 pin `f6b8868c…a07f28c`; byte-identical to the fleet working-tree copy (`cmp -s` exit 0).
- Doc under review: TIP `corpus/knowledge/witness-equivalence-rule.md` → `a7aa00b88c28ec18daf2d98bc4613fd4aa143a480771e1dba37536637f15afe2`; identical in the fleet tree (`cmp -s` exit 0) — no clone↔fleet drift.
- Ancestry: `git merge-base --is-ancestor c17e593b51802dd4ed568da3265f21c6d00c4273 0b99d48e…` exit 0; `--is-ancestor 6aaad5b389e7eed426ec3b452617bcbf9bf7f35a c17e593b…` exit 0. Amendment 6 (16:06:20 −0300) precedes the sealed-set commit c17e593b (16:25:00 −0300; `git log --diff-filter=A` on `.ufo/evidence/round-33/heldout/`).

## 1. The four rule bullets vs `ho_witness_ok` (md:10-23 ↔ counter sha `f6b8868c…`)

| Doc bullet | Branch(es) in `ho_witness_ok` / `validate_ho` | Match |
|---|---|---|
| **kill + `kind=head`** (md:10-13): leg-assignment line diff — multiset of bare `st_x=$?` captures OR of all `st_*=` assignments must change — AND block byte-identical; inert head edit validates invalid | counter 192-196: `kind=='head'` entry (192), head-differs check (193-194), block-identity refusal `head-with-block-edit` (195-196); kill branch 197-207: `A = r'^[ \t]*(st_[A-Za-z0-9_]+)=\$\?[ \t]*$'` (bare captures, exact bytes at :202), `X = r'^[ \t]*(st_[A-Za-z0-9_]+)[ \t]*='` (:203), `sorted(A.findall(...)) != … or sorted(X.findall(...)) != …` → `(True,'head-leg-assignment')` (:206) else `(False,'head-edit-cannot-kill')` (:207) | ✓ byte-exact, incl. "multiset" (sorted-list compare) and the OR of the two surfaces |
| **accept + `kind=head`** (md:14-16): head may differ but block byte-identical; lethal ride-along refused as `head-with-block-edit` | same 192-196 block-identity gate fires for both sets; accept falls through to `(True,'head')` (:208); refusal label string `'head-with-block-edit'` (:196) is verbatim the doc's | ✓ |
| **accept + `vector`** (md:17-20): equivalence — same `(exit, first-line)` tuple on the named 9-status vector, bytes changed | vector path 209-215: `a = block_run(pb, vec, work)`, `b = block_run(mb, vec, work)`; `return a == b and mutated != pristine, 'vector-equivalence'` (:215); `block_run` docstring "return (rc, stdout-first-line)" (:154-156) | ✓ (`a == b` is tuple equality = same exit + same first line) |
| **kill + `vector`** (md:21-23): behavioral difference on the named len-9 vector, block changed; len 9 enforced at validation | `if pb == mb: return False, 'block-identical'` (:216-217); `return a != b, 'vector'` (:218); len enforcement `if len(vec) != 9: raise CounterError('witness.vector must name all 9 leg statuses…')` in `validate_ho` (:123-124) | ✓ |

The md's parenthetical at :22-23 ("shorter vectors only compare crash signatures, never tally behavior — round-33 amendment") is **confirmed against history**: the creation-era counter (`git show f6d8a891f1d966c5c3cdda385090da3a6e804675:.ufo/evidence/round-33/c1/c1-measure.py`) has no len check in `validate_ho` (:94-121) and its `block_run` (:144-169) binds only `names[:len(vector)]` under `set -u` — a shorter vector leaves the remaining `st_*` unbound, so both legs crash and the tuple comparison degenerates to crash signatures. The len-9 raise appears first at `49876298` (round-33 amendments 3+4) :115-116. No committed revision contains a literal "crash"/"signature" code path — the phrase is an accurate rationale, not a quote.

History section (md:27-36) vs the pre-amendment gate (`git show 6aaad5b389e7eed426ec3b452617bcbf9bf7f35a~1:…c1-measure.py`, scratch `old_counter.py`): `ho_witness_ok` :176-188 is exactly the set-blind rule the doc describes — `if w.get('kind') == 'head': return head_of(mutated) != head_of(pristine), 'head'` (any textual head diff validates, either set) and `return a != b, 'vector'` for every vector witness (equivalent accept clones unsatisfiable). All three voidability consequences (md:30-36) follow mechanically from those two lines.

## 2. Evidence pointers (md:44-53) — all exist and check out

| Pointer | Check |
|---|---|
| `.ufo/evidence/round-33/c1/c1-measure.py` (md:44) | exists; sha256 `f6b8868c…a07f28c` = amendment-6 pin (§0) |
| `.ufo/evidence/round-33/contract-amendments.json` (md:45) | exists (4570 bytes); entry `"amendment": 6` discloses the same four branches, same refusal labels, and "adopted BEFORE any sealed held-out authoring" |
| `.ufo/evidence/round-34/dev/witness-probes.{json,stdout}` (md:47) | both exist; stdout = 2 precondition lines (`VERSION in head: True`, `st_js line count: 1`) + 8 probe result lines; json = the same 8 lines. Re-executed independently (§3): all 8 reproduce byte-identically → "8/8 exact" ✓ |
| `.ufo/evidence/round-33/heldout/` (md:48-51) | exactly 14 JSONs. kill: `ho-kill-head-{extra-assign,nonbare}` (2 head-surface, `kind=head`) + `ho-kill-vector-{arm-swap,fail-threshold,setup-arm-skip,count-field-swap,setup-threshold,fail-exit-swap}` (6, len-9 vectors) — the six names match the doc's block-class list one-for-one. accept: `ho-accept-head-{comment,version-rename}` (2 head-cosmetic) + `ho-accept-vector-{inert-line,tail-comment,arith-space,block-comment}` (4 block-equivalent) ✓. Every copy's `set`/`kind`/vector-length matches its filename and the doc taxonomy |
| `.ufo/evidence/round-34/dev/authoring-receipts.json` (md:51) | 14 receipts; `id` set == filename set (programmatic check: `id_eq_files True`); every `edits_ok=true`, `as_expected=true`; witness labels: 2×`head-leg-assignment`, 6×`vector`, 2×`head`, 4×`vector-equivalence` — exactly the branch outcomes the amended gate assigns |
| `.ufo/evidence/round-34/measure/` (md:52-53) | `c1-deciding-run.stdout` is byte-identical to the claim line (`C1_R33: … ho_kill=8/8 ho_accept=6/6 ho_invalid=0 … rev=c17e593b… C1_R33_PASS=true`); `c1-deciding-run.exit` contains `0` |

## 3. Independent re-execution (module import only — kill rule respected)

Staged scratch module layout (`counter-mod/round-33/c1/c1-measure.py` + `counter-mod/round-32/c1-measure.py`, both extracted from TIP; staged r33 counter `cmp` vs clone exit 0) and imported with `importlib.util`; called `m.ho_witness_ok(ho, pristine, mutations, probe-work)` with bwrap 0.13.1 (`/usr/bin/bwrap`) available. Mutations built by single-occurrence `str.replace` (count==1 asserted). All 8 probe labels reproduced exactly, equal to my per-branch predictions and to the committed stdout lines 3-10 verbatim:

```
Q1-comment-accept       -> (True,  'vector-equivalence')
Q3-inert-head-kill      -> (False, 'head-edit-cannot-kill')
Q3b-ridealong-accept    -> (False, 'head-with-block-edit')
K-extra-leg-assign-kill -> (True,  'head-leg-assignment')
K-nonbare-leg-kill      -> (True,  'head-leg-assignment')
A-inert-head-accept     -> (True,  'head')
A-head-with-block       -> (False, 'head-with-block-edit')
KV-block-identical      -> (False, 'block-identical')
```

This exercises every branch the four bullets name, on TIP bytes, first-hand.

## 4. Sources (md:57-66)

- **S097** (md:57-61) → `corpus/SOURCES.md:106` row exists ("GNU Bash Reference Manual, Bash 5.3 source (`doc/bashref.texi`) …", grade A, §Exit Status lines 3890-3916 + §case lines 1044-1084, 415804 bytes, SHA-256 `f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5`). The row pins remote bytes (no committed snapshot is claimed, consistent with the md's wording "opened in an earlier round"). Re-fetched first-hand: `curl -fsSL --max-time 40 'https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bashref.texi?id=b8c60bc9ca365f8261fa97900b6fa939f6ebc303' -o bashref-5.3.texi` → curl exit 0, 415804 bytes, sha256 `f3d37d57…d5` — **digest matches the row today**. Committed corroboration: `.ufo/waves/round-32/w1/SrcBashExit.md:22` and `.ufo/waves/round-32/w2/ReviewSources.md:49-52`; the `case` first-match quote is committed at `corpus/lessons/round-32.md:24`.
- **S101** (md:62-66) → `corpus/SOURCES.md:109` row exists ("Major Mutation Framework (mutation-testing.org)", grade C; "suppressing equivalent mutants… the set of live mutants"; committed snapshot `.ufo/evidence/round-34/src/s101-mutation-testing.html`). Snapshot exists; `sha256sum` = `0fde8a7bf52acdc5d1c04f01f9ccc94896db1844cfdeced98a419861ab7cf420` and `wc -c` = 4341 — **both equal the row's digest and byte count**. The doc's quoted phrases are verbatim in the snapshot: "suppressing equivalent mutants;" (:45) and "computing the mutant-detection rate and the set of live mutants" (:46). Row's used-by column names this very doc — citation resolves.

## 5. Findings

**F1 (minor, doc defect): count word disagrees with list length.** `corpus/knowledge/witness-equivalence-rule.md:28` says "Consequences, **both** demonstrated by execution:" but introduces **three** bullets (md:30-31, 32-33, 34-36) — and all three are real (each follows from `old_counter.py:178-179`/`:188`; Q1b/Q3/Q3b routed per amendment 6). Suggested byte: "both" → "all three". Reproduce:
```
grep -n "both demonstrated" corpus/knowledge/witness-equivalence-rule.md   # -> 28
sed -n '28,36p' corpus/knowledge/witness-equivalence-rule.md               # one intro line, three bullets
```
No semantic impact on the rule or the claim.

**O1 (observation, not drift): "cosmetically" (md:14) is narrower than the code.** The accept+head branch (:192-196, :208) accepts *any* head diff with a byte-identical block — the load-bearing check is block identity, not the head diff's cosmetic character. The two authored accept-head copies are indeed cosmetic (comment insertion; `VERSION='… sealed-a2'` suffix), so the bullet describes its set truthfully; it just isn't a code-enforced restriction. Quoting both sides: md:14 "the head may differ cosmetically but the tally block must be byte-identical" vs counter :195-196+208 (block-identity gate, then unconditional `(True,'head')`). No action required; the branch map in §1 is otherwise exact.

No further findings. The four-bullet↔branch mapping, every Evidence pointer, and both S-citations verify; nothing observed contradicts the deciding-run receipt.

## 6. Residual risk / verification gaps

- The deciding run was **not** re-executed (kill rule consumed; bounds). The receipt is verified as committed bytes (byte-identical stdout, exit file `0`, ancestry §0), not re-derived.
- `ho_kill=8/8 ho_accept=6/6 ho_invalid=0` was not independently re-scored through `score_tool`/`run_tool_sandboxed` (tool-semantics seats' territory); this seat re-credits the *knowledge doc*, whose claims stop at the gate, pointers, and sources.
- S097: the digest is pinned to remote bytes (no committed snapshot for that row); today's live fetch matches, but the row's durability rests on the pinned Savannah commit id — same trust model the row itself declares.
- No LSP server was available for this md/python mix in this environment; all checks are byte-level + executed (grep used as literal fallback, recorded here per protocol).
- Tooling authorization (operator 2026-10-19): **no tools installed or upgraded** for this seat; pacman untouched (paused per 2026-10-20 ruling). Only `git` (read-only), `curl`, `python3`, `bwrap` (pre-existing, 0.13.1) were used.

## Command ledger (exit codes)

| Purpose | Command (abridged, `$S` as above) | Exit |
|---|---|---|
| clone+checkout TIP | `env -u GIT_DIR … git clone -q --no-hardlinks … $S/lane && … checkout -q --detach 0b99d48e…` | 0 (`setup_exit=0`) |
| pin extraction | `git -C $S/lane show 0b99d48e…:tools/{tally-audit-v2.py,mutate-and-run.sh} > …` | 0 / 0 |
| pin verify | `sha256sum $S/tool.py $S/pristine.sh` | hashes match (§0) |
| counter pin | `sha256sum` clone+fleet counter; `cmp -s` | `f6b8868c…a07f28c` both; cmp 0 |
| doc drift | `sha256sum`+`cmp -s` md clone vs fleet | `a7aa00b8…` both; cmp 0 |
| ancestry | `git merge-base --is-ancestor c17e593b… 0b99d48e…` / `6aaad5b… c17e593b…` | 0 / 0 |
| S101 snapshot | `sha256sum` + `wc -c` | `0fde8a7b…`, 4341 (match row) |
| S097 re-fetch | `curl -fsSL --max-time 40 '…bashref.texi?id=b8c60bc9…'` | 0; 415804 B; `f3d37d57…` |
| probe re-run | python3 importlib on staged TIP counter; `m.ho_witness_ok(...)` ×8 | all 8 == prediction == committed stdout |
