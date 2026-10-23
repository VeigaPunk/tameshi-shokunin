# ColdReadContractAmendments — cold-read re-crediting of `.ufo/evidence/round-33/contract-amendments.json`

Seat scratch: `/fast/scratch/hyaku/tameshi-r34-seats/ColdReadContractAmendments/` (lane clone detached at tip `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`; `git rev-parse HEAD` = `0b99d48ed4e3d00c2e5893b2d61f3dd97a7f68b7`, exit 0). No lane writes; no git/jj write commands; counter used by module import only (kill rule unconsumed). `bwrap` already present at `/usr/bin/bwrap`; no installs performed.

## Verdict: NO FINDING — all six records verified truthful; every `data_disclosure` consistent with committed git order and receipt bytes.

## Pin verification (tip `0b99d48` and measurement rev `c17e593b` agree)

| command | result |
|---|---|
| `git show 0b99d48:tools/tally-audit-v2.py \| sha256sum` | `7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10` = pin |
| `git show 0b99d48:tools/mutate-and-run.sh \| sha256sum` | `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` = pin |
| `git show 0b99d48:.ufo/evidence/round-33/c1/c1-measure.py \| sha256sum` | `f6b8868c54263c9d51f455b574e85c033d4e043392e7646992c65ad02a07f28c` = pin |
| `git show c17e593b:{tool,runner,counter} \| sha256sum` | identical three shas — the deciding run measured exactly the pinned bytes |

## Amendment 5 — `commit ee398492` (= `ee3984924c4d52703209f8b971717c975898f4ba`, 15:59:41)

- Re-pin verified: `git show ee398492:tools/tally-audit-v2.py | sha256sum` = `7b11ba25…8d10` (record's "re-pinned to 7b11ba25...8d10" is byte-exact; parent `ee398492^` = `7a59f576…38833`, so the re-pin lands at this commit).
- `git show ee398492 --stat`: `tools/tally-audit-v2.py` +9, `corpus/lessons/round-33.md` +124, `c1-measure.py` +2. The tool diff adds the twice-only rule (`head.count(nm) != 2` per leg name — the `local` declaration + bare `st_x=$?`), matching "each leg name appears exactly twice in the head". Rule present in pinned bytes (tool.py:326–334).
- "19/35 head survivors killed, validated on all 35" supported by `git show ee398492:corpus/lessons/round-33.md` lines 50–53 (DevHead: "19/35 head mutants survived… the twice-only rule kills all 35, pristine and selftest 21/21 green"); commit message concurs. [INFERENCE] the 35-run itself is not independently replayed here — lesson/commit record agreement only.
- `data_disclosure` "no default-mode run had occurred": the only r33 C1 receipt (`c1-at-head-notrun`) was committed at `5bfa3b59` (16:01:11) with `rev=732b6860` (16:00:07) — both timestamps are AFTER ee398492's 15:59:41. Consistent.

## Amendment 6 — gate change verified by `git diff 61401c2..6aaad5b3 -- c1-measure.py` (63 lines, 40 changed)

Every claim clause lands in the diff, and behavior was exercised on scratch copies (`probe_gate.py`, `probe_sealed.py`, both exit 0; counter imported as module, never run default-mode):

| record claim | code (lines 184–218) | observed |
|---|---|---|
| kill+head requires leg-assignment-line diff, identical block | set-scoped `A`/`X` multiset diff → `head-leg-assignment` | `st_js=$?`→`(( st_js = $? ))` → `(True,'head-leg-assignment')`; inert head comment → `(False,'head-edit-cannot-kill')` |
| accept+head requires identical block, lethal ride-along refused | `mb != pb → 'head-with-block-edit'` | head-comment + `nfail+0` ride-along → `(False,'head-with-block-edit')`; benign head edit → `(True,'head')` |
| accept+vector = `a==b` with bytes changed | line 215 | cosmetic comment copy, vector `[0]*9` → `(True,'vector-equivalence')`; identical bytes → `False` |
| kill+vector keeps `a!=b`, len-9 enforced | lines 216–218; `validate_ho` line 123 raises on len≠9 | `[1]*9` on `nfail+0` mutant → `(True,'vector')`; block-identical copy → `(False,'block-identical')`; len 8/10 refused by `validate_ho` |

"Frozen set-blind rule was voidable in both directions" — demonstrated against the extracted pre-amendment counter (`git show 61401c2:…/c1-measure.py`, sha `e5ba9cfe…051c`):

- All 4 sealed accept+vector copies: OLD `False:'vector'`/`block-identical` (unsatisfiable class) → NEW `True:'vector-equivalence'`.
- Inert head edit as must-kill: OLD `(True,'head')` (would bless a non-killing mutant) → NEW `(False,'head-edit-cannot-kill')`.
- Lethal ride-along as must-accept: OLD `(True,'head')` → NEW `(False,'head-with-block-edit')`.
- Full sealed set (`git ls-tree c17e593b .ufo/evidence/round-33/heldout/` = 8 must-kill + 6 must-accept, all vectors len 9): edits applied via `apply_edits`, NEW gate accepts **14/14** — matching the deciding receipt `ho_kill=8/8 ho_accept=6/6`.

"Adopted BEFORE any sealed held-out authoring": `git log -- heldout/` shows exactly one authoring commit, `c17e593b` (16:25:01); `git merge-base --is-ancestor 6aaad5b3 c17e593b` = 0 (16:24:04 precedes it). Controls receipt commit `9dd3174c` (16:24:50) sits between them; receipt carries `counter_sha256=f6b8868c…a07f28c`, four controls all `predicate_pass=false`. Deciding receipt `0b99d48:.ufo/evidence/round-34/measure/c1-deciding-run.stdout` reads byte-identically to the assignment's `C1_R33` line; `c1-deciding-run.exit` = `0`.

`data_disclosure`: only r33 head receipt is `c1-at-head-notrun.{exit,stdout}` — a verdict line with `controls_ok=0(receipt-missing)`, `heldout_after_freeze=0`, `C1_R33_PASS=false`, exit `1` — an aborted/not-run structural false under the kill rule (does not decide). The diff `61401c2..6aaad5b3` under `.ufo/evidence/` contains only dev/panel/authoring receipts — the disclosed "observations".

## Records 1–4 spot-verified for completeness

- a1 (`27902a16`): `write_controls` signature/receipt-path arg refactor — matches "arg handling". a2 (`e6a5f4ba`): `c2-measure.py` +7/-2 — matches "c2 counter hardening". a3+a4 (both in `49876298`): c1 counter +73, c2 +5, tool +164, `contract-amendments.json` +6 — consistent with the `amends` texts. Amendments 1, 2, 4, 5 all carry timestamps earlier than the first (not-run) receipt at `732b6860`; their `data_disclosure` lines are consistent.

## Residual risk / notes (not findings)

1. **Disclosure tense**: amendment 5's "no default-mode run had occurred" is true at its commit time (15:59:41); the not-run receipt landed ~20 s later. Amendment 6's wording ("no default-mode *deciding* run") is the more precise phrasing; the file's earlier records are staler prose but not contradicted by git order.
2. **`commit` field absent on records 3, 4, 6** (a convention inconsistency, not a falsity): their landing commits are recoverable via `git log -- contract-amendments.json` → `49876298` (3+4) and `6aaad5b3` (6).
3. **Head-diff gate is a syntactic proxy**: trailing comments (`st_js=$? # x`) flip the kill+head gate's `A`/`X` multisets — verified the tool also treats those as non-bare/must-kill (tool.py:316–320 `fullmatch(r'\$\?')`), so proxy and predicate stay aligned; a pathological inert head edit that alters only `st_*` assignment-line text could still pass the kill gate, but no such form survives the tool's checks identified in this read.

Key commands (all exit 0): the sha/ancestry/git-diff invocations quoted above; `python3 probe_gate.py` (10/10 gate observations as listed); `python3 probe_sealed.py` (14/14 NEW-gate acceptances, OLD/NEW voidability pairs as listed). Probe scripts and the counter diff remain in the scratch dir.
