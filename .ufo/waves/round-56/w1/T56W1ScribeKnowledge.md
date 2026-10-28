# T56W1ScribeKnowledge — `corpus/knowledge/receipt-revision-binding.md` draft (round 56, wave 1)

Seat `T56W1ScribeKnowledge` (scribe, leaf — no dispatch). Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`;
base `981c5e8b20a2ada6a4f83464cff8a64fecdd9aa1`; frozen instrument set `c3e2ca9f020776b3d66c7af854fb82c834674fcf`
(lane HEAD while this seat ran). Axis: coverage. No lane production file and no frozen instrument was edited:
everything below is a read, a run of committed bytes, or a write under `.ufo/waves/round-56/w1/` and my scratch.

**One blocker for C2 is reported here (F1): the frozen C2 counter cannot pass its own docs arm.** It is a
one-token defect in `.ufo/evidence/round-56/c2/measure.py:245`, demonstrated on identical bytes, with the
minimal amendment and the lane's own precedent (`round-50/c2/measure.py:352`) named. Because the L1 stood down
mid-seat, this report is written to stand alone for the successor.

---

## 1. Deliverable — the full entry text (L1 commits it at C0)

Ready-to-copy file (byte-identical to the block below):
`.ufo/waves/round-56/w1/T56W1ScribeKnowledge-receipts/receipt-revision-binding.md.draft` (13856 B).
Target path: `corpus/knowledge/receipt-revision-binding.md`.

````markdown
source: S281 — in-toto Attestation Framework, Statement layer specification — https://github.com/in-toto/attestation/blob/v1.2.0/spec/v1/statement.md — §Fields, `subject` field, IMPORTANT paragraph at lines 54-55 @ tag v1.2.0 (raw fetch 2026-10-28T18:42:42Z, sha256 cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea, 2492 B, byte-identical at `main` the same minute); S103 — https://git-scm.com/docs/git-hash-object — §DESCRIPTION, first sentence @ page fetched 2026-10-24 (a blob's object id is computed from the contents of the named file, so a recorded digest binds evidence to exact bytes); own work — `tools/receipt-revision-gate.py` (sha256 `1d80f8a6…fbd2` at `c3e2ca9f`), `.ufo/evidence/round-54/control/controls-b.stdout`, `.ufo/evidence/round-55/after/c2.stdout`, `.ufo/evidence/round-56/c2/red-before/`, `corpus/lessons/round-54-verifier-spotcheck.md` (R54.1), `corpus/lessons/round-55-verifier-spotcheck.md` (R55.5)
verified-at: 2026-10-28 — every command under §Re-derive ran at lane `c3e2ca9f0207` (HEAD when this note was written); the outputs are under `.ufo/waves/round-56/w1/T56W1ScribeKnowledge-receipts/`
recheck: 180d — `curl -fsSL https://raw.githubusercontent.com/in-toto/attestation/v1.2.0/spec/v1/statement.md | sha256sum` must print `cbe684a1…ebea` (anything else: the tag moved, re-open the row); `python3 tools/receipt-revision-gate.py --selftest` must print `GATE_SELFTEST: 14/14 pass`

# A receipt is evidence only for the content it was measured against (round 56)

An attestation is about a subject it identifies by digest: "Set of software
artifacts that the attestation applies to. Each element MUST have `digest` set",
and "Subject artifacts are matched purely by digest, regardless of content type"
(S281 §Fields, `subject`; the second sentence is the located quote, lines 54-55).
The lane's receipts are attestations of the same shape, one layer down: a control,
a positive control or a counter verdict is evidence about a *revision*, and a
receipt that names a different revision — or none — is evidence about something
else. Until round 56 the lane never checked that, and two accepted receipts were
exactly the defect the sentence names.

## The rule

A receipt is admitted as evidence only for the content it was measured against.
Concretely, every receipt a round certifies carries in its own bytes the revision
it was measured against (`rev=<sha>` or `"rev": "<sha>"`), and the lane's
certification path runs `tools/receipt-revision-gate.py` over it:

```
python3 tools/receipt-revision-gate.py --lane LANE --certified REV \
        [--paths SURFACE.txt] --receipt PATH:ROLE[:REQUIRE_REGEX] [--receipt …] [--json]
```

`REV` is the certified (measured) revision. `ROLE` is one of:

| role | what it admits | rule |
|---|---|---|
| `positive` | a control whose expected verdict is PASS | exactly one distinct `rev=`; it must equal `REV`, or — only with `--paths` — name a revision whose bytes are identical to `REV` on every listed path |
| `verdict` | a counter's verdict receipt | identical to `positive` (the code takes the two roles in one branch) |
| `control` | a control set with several `CTL` lines | every `rev=` token must resolve and be an ancestor of, or equal to, `REV`; `--paths` is not consulted |

One verdict line, and only that line is the verdict:
`GATE: receipts=N ok=N refused=N codes=<comma|none> verdict=PASS|REFUSED`.
Exit 0 iff `PASS`; exit 3 is a named refusal; exit 2 is
`GATE: error=unresolvable-certified … codes=RECEIPT_REV_UNRESOLVABLE`, a
could-not-evaluate — the gate did not run. The codes are a closed list of eleven
(`RECEIPT_MISSING`, `RECEIPT_EMPTY`, `RECEIPT_NOT_BLOB`, `RECEIPT_REV_ABSENT`,
`RECEIPT_REV_AMBIGUOUS`, `RECEIPT_REV_UNRESOLVABLE`, `RECEIPT_REV_MISMATCH`,
`RECEIPT_REV_CONTENT_DRIFT`, `RECEIPT_CONTROL_NOT_ANCESTOR`,
`RECEIPT_DIGEST_MISMATCH`, `RECEIPT_REQUIRED_LINE_MISSING`); the tool's own
selftest asserts the list is closed (case `codes-closed`).

The tool reads git objects and receipt bytes only. It writes nothing and allocates
no scratch outside `TMPDIR`; the lane's deciding runner extracts its bytes with
`git show REV:tools/receipt-revision-gate.py` and runs that copy, so the gate a
round is judged by is the gate the round froze.

## What it catches — three receipts the lane had already accepted

Each row is one command's output (§Re-derive), not a reading of the round's prose.

| receipt | what its bytes say | revision the round certified | gate | code |
|---|---|---|---|---|
| `.ufo/evidence/round-54/control/controls-b.stdout`, line `CTL_POS_c1` | `rev=077d431e6996` (the round-54 freeze) | `c2108100` | REFUSED | `RECEIPT_REV_CONTENT_DRIFT`, drift = `.ufo/evidence/round-21/coldread/ledger.json` plus five round-54 wave paths |
| the same file, line `CTL_EXIT0` | `rev=7df0e0426c98` | `c2108100` | REFUSED | `RECEIPT_REV_UNRESOLVABLE` (that revision is not in this repository: `git rev-parse --verify --quiet '7df0e0426c98^{commit}'` prints nothing) |
| `.ufo/evidence/round-55/after/c2.stdout` | no revision token at all (0 matches for `rev=` and for a JSON `rev` key, 28 lines) | `4c04c1d3` | REFUSED | `RECEIPT_REV_ABSENT` |

The first row is ER-R54-1: round 54's phase B scored its positive control at the
freeze `077d431e`, which predates the full re-key `7fa9a5e0`, so the control was
scored against a cold-read ledger the round had since changed — and the record
called it "proven live" in four files (`corpus/lessons/round-54-verifier-spotcheck.md`
R54.1). The round's own deciding gate saw nothing wrong:
`.ufo/evidence/round-54/after/deciding-run.exit` reads `DECIDING_RUN_EXIT=0`.

The third row is the R55.1/R55.5 shape one level up: round 55's `deciding-run.sh`
compared the freeze, the tree and the counters, but never compared a `CTL` line's
`rev=` with the revision under test, so a control scored elsewhere passed as
evidence (`corpus/lessons/round-55-verifier-spotcheck.md` R55.5). Round 56's
runner closes that: gate 0b gates the lane's own control receipts at `$REV`
(`.ufo/evidence/round-56/deciding-run.sh:66-74`) and gate 0c gates the verdict
receipts the run has just produced (`:100-107`, its exit participating in the
deciding status). A deciding run that cannot bind its own receipts now exits 3
before it measures anything else.

## The content-identity exception, and why it has to exist

A receipt cannot name the commit that contains it. The run that produces
`controls-b.stdout` writes it before the commit that lands it, and the deciding
verdict receipts are written by the run the deciding revision certifies, so their
bytes can only exist *after* the revision they are about. Requiring the named
revision to equal the certified one would therefore refuse every receipt a round
produces about itself. The same shape recurs for a control legitimately scored at
the freeze PIN: the PIN is the right place to score it, and the surface it
certifies is the thing that must not have moved since.

So the gate admits a differing `rev=` only when the caller declares the surface
and the bytes on it are identical:

```
git -C LANE diff --name-only <named-rev> <certified-rev> -- $(cat SURFACE.txt)   # empty ⇒ accept
```

`--paths` is mandatory for the exception; without it a differing `rev=` is
`RECEIPT_REV_MISMATCH`, full stop. The lane's own surface is
`.ufo/evidence/round-56/control/frozen-surface.paths` — nine paths: `SKILL.md`,
`corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/knowledge`, `tools/registry.json`,
the gate itself, the cold-read ledger and both counters. A round that widens the
surface widens what a stale control may certify, so the list is frozen with the
instrument.

Measured, on a two-commit fixture (`fixture-gate-demo.sh` cases 2-4):

| named rev vs certified | `--paths` | verdict |
|---|---|---|
| older commit | none | REFUSED `RECEIPT_REV_MISMATCH` |
| older commit, declared surface unchanged (`a.txt`) | `a.txt` | **PASS** — the exception |
| older commit, one path drifted (`b.txt`) | `a.txt b.txt` | REFUSED `RECEIPT_REV_CONTENT_DRIFT`, `drift=b.txt` |

Two properties keep the exception from being a loophole: it is bounded by a list
the caller must write down, and it still refuses the round-54 case, because the
cold-read ledger is on the declared surface and did move between `077d431e` and
`c2108100`. One footgun is worth naming: an *empty* `--paths` file is not "no
surface to check". It makes the drift list the sentinel
`<no --paths given: content identity is not checkable>` and refuses every
differing revision with `RECEIPT_REV_CONTENT_DRIFT` (case 8). Fail-closed, but the
detail string reads as if the flag were missing.

## What the gate cannot see

- **A copied `rev=` token passes.** The gate reads the receipt's bytes, not the
  process that wrote them. A receipt that names the certified revision and was
  never run — `FABRICATED VERDICT: rev=<certified> total=0 PASS=true (never run)`
  — is accepted (case 7). The binding is necessary, not sufficient.
- **The digest sidecar narrows, it does not close.** If `PATH.sha256` exists its
  first field must equal the receipt's sha256 (`RECEIPT_DIGEST_MISMATCH`
  otherwise), so a receipt edited after it was hashed is caught — but a copier who
  copies the sidecar too passes. The sidecar binds bytes, not provenance.
- **Committing is not checked.** The gate reads the path from the filesystem; a
  receipt that exists only in a working tree is gated as if committed. Whether it
  reached the repository is criterion 97's job, not this tool's.
- **The claim text is not checked.** Any `rev=`-shaped token in the file counts,
  including one in a comment, a quoted line, or a sentence about another claim.
  `REQUIRE_REGEX` (`PATH:ROLE:REGEX` → `RECEIPT_REQUIRED_LINE_MISSING`) is the
  only lever for "this receipt is about *this* claim".
- **A non-hex revision name is invisible.** `rev=v1` does not match the token
  grammar, so a tag-named receipt is refused `RECEIPT_REV_ABSENT` (case 10), not
  resolved as a tag. Fail-closed, but the code names absence rather than
  "unresolvable". Hex prefixes are resolved: a 7-hex prefix of the certified
  revision passes (case 9), and the `revs=` column echoes what the receipt wrote,
  not the full sha.

## Falsifier

This note is wrong if any of these happens; each is a command, not an opinion.

1. The gate accepts the round-54 positive control at `c2108100` (it must exit 3
   with `RECEIPT_REV_CONTENT_DRIFT`).
2. The gate refuses a receipt naming a revision that is content-identical on the
   declared surface (case 3 must be `PASS`).
3. `--selftest` reports anything other than `14/14 pass`, or `codes-closed` fails.
4. A receipt with two distinct revisions in a `positive` role is accepted (it must
   be `RECEIPT_REV_AMBIGUOUS`, case 11), or a `control` line naming a
   non-ancestor is accepted (case 6 must be `RECEIPT_CONTROL_NOT_ANCESTOR`).

## Re-derive

```sh
L=/home/vgpnk/Projects/shokunin/tameshi-shokunin
# 1. the gate's own suite, at the frozen bytes
git -C "$L" show c3e2ca9f:tools/receipt-revision-gate.py | sha256sum      # 1d80f8a6…fbd2
python3 "$L/tools/receipt-revision-gate.py" --selftest                    # GATE_SELFTEST: 14/14 pass
# 2. ER-R54-1: the real positive control, refused, with the ledger named
python3 "$L/tools/receipt-revision-gate.py" --lane "$L" --certified c21081008adb \
  --paths "$L/.ufo/evidence/round-56/c2/red-before/round-54-surface.paths" \
  --receipt "$L/.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout:positive"
#   → exit 3, codes=RECEIPT_REV_CONTENT_DRIFT, drift=.ufo/evidence/round-21/coldread/ledger.json,…
# 3. the same round's control set, one revision absent from the repo
python3 "$L/tools/receipt-revision-gate.py" --lane "$L" --certified c21081008adb \
  --receipt "$L/.ufo/evidence/round-54/control/controls-b.stdout:positive"
#   → exit 3, codes=RECEIPT_REV_UNRESOLVABLE rev=7df0e0426c98
# 4. round 55's committed verdict, which names no revision
python3 "$L/tools/receipt-revision-gate.py" --lane "$L" --certified 4c04c1d33377 \
  --receipt "$L/.ufo/evidence/round-55/after/c2.stdout:verdict"
#   → exit 3, codes=RECEIPT_REV_ABSENT
# 5. the round-54 gate accepted the set this one refuses
cat "$L/.ufo/evidence/round-54/after/deciding-run.exit"                   # DECIDING_RUN_EXIT=0
# 6. the exception and the blind spot, on a scratch fixture (never the lane)
bash .ufo/waves/round-56/w1/T56W1ScribeKnowledge-receipts/fixture-gate-demo.sh
bash .ufo/waves/round-56/w1/T56W1ScribeKnowledge-receipts/fixture-gate-demo2.sh
```

The round-56 C2 counter exercises this note as arm 2 (`red54`), arm 3 (`red54b`),
arm 4 (`red55`), arm 5 (`own`, the round's own receipts accepted at the certified
revision) and arm 6 (`docs`, that this file opens with its provenance trio and
cites a `mined` row): `python3 .ufo/evidence/round-56/c2/measure.py --lane "$L"
--rev REV --work EMPTY_DIR --explain`.

## Limits

- **[INFERENCE]** The gate's codes are the ones a *correct* producer trips. A
  receipt can be wrong about its claim and still be bound to the right revision;
  the binding is a necessary condition on the evidence, never a sufficient one,
  and no arm of the C2 counter claims otherwise.
- **[INFERENCE]** Had this gate existed at round 54's deciding run, that run would
  have refused. The measured half is that the gate at today's bytes refuses the
  retained receipt; the counterfactual about round 54's process is not measured
  and is not counted anywhere in the lane.
- **Unknown:** whether any pre-round-54 receipt in `.ufo/evidence/` names a
  revision that has since drifted on its own claim surface. The round-56 receipt
  inventory (`.ufo/waves/round-56/w1/receipt-inventory.json`) counts tokens; it
  does not re-gate every historical receipt, and no claim here rests on one.
````

### 1a. Why the text is shaped this way (constraints it must satisfy at C0)

| Constraint | Where it comes from | Satisfied by |
|---|---|---|
| `source:` / `verified-at:` / `recheck:` first, and a `S\d{3}` in that head | `corpus/QUALITY.md` criterion 10; `CORPUS.md` "each `knowledge/` entry opens with…"; C2 arm 6 | lines 1-3, before the first `---` (there is none in the head; `text.split('---',1)[0]` is 2773 chars, receipt `arm6-simulation.stdout`) |
| a cited S-row that is `mined` | C2 arm 6 (`cited & mined`) | cites S281 (the row this round opens, `mined`) **and** S103 (`mined` at base) — so the arm survives even if S281's row lands late, and fails if both are absent |
| one external source with a located quote | `## Gate` requirement; S281 | the ≤25-word quote is 11 words, §Fields/`subject`, lines 54-55 |
| a coverage-map row in the same round | `corpus/QUALITY.md` criterion 7 (MK-4) | proposed row below — **the L1 must land it with the entry** |
| append-only corpus discipline | criterion 4/35 | the file is new; nothing existing is rewritten |

**Proposed `corpus/README.md` coverage-map row** (criterion 7; the L1 lands it with the entry, in the
`## Coverage map` table, next to the round-56 rows):

```markdown
| `knowledge/receipt-revision-binding.md` | A receipt is evidence only for the content it was measured against: the gate's three roles and eleven closed refusal codes, the content-identity exception and the declared surface it is bounded by, and the blind spot (a copied `rev=` token passes); the real round-54 positive control and the round-55 verdict are refused by the gate the lane now runs, where the round-54 deciding gate accepted them | S281, S103 |
```

### 1b. The source line is bound to the scout's row — check it before commit

The `source:` cell quotes `.ufo/waves/round-56/w1/T56W1ScoutSource.json` exactly: URL
`https://github.com/in-toto/attestation/blob/v1.2.0/spec/v1/statement.md` (raw fetch), access
`2026-10-28T18:42:42Z`, sha256 `cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea`, 2492 B,
quote "Subject artifacts are matched purely by digest, regardless of content type.", location
`## Fields / subject / IMPORTANT paragraph, lines 54-55`. I re-fetched the same URL independently and got the
same digest and size (`receipts/fetch-in-toto-statement.{stdout,sha256}`), so the snapshot the scout committed
(`.ufo/evidence/round-56/assimilation/in-toto-statement-v1.md`, 2492 B) is the byte set I cite.

If `T56W1ScribeSources` lands a different anchor or a different id, **change my `source:` line, not its row**:
the counter only requires the head to cite a `mined` id. The scout's rejected candidate (DSSE protocol,
`secure-systems-lab/dsse`) is correctly not cited here: it authenticates a payload, never a subject.

---

## 2. FINDING F1 — the frozen C2 counter cannot pass its docs arm (blocker for C2)

**Claim.** `.ufo/evidence/round-56/c2/measure.py:245` reads the SOURCES registry's status column at
`cells[8]`; every row in `corpus/SOURCES.md` carries status at `cells[7]`. No row can ever satisfy
`cells[8] == 'mined'`, so the note half of arm 6 never passes, `docs` is capped at 3/4, and
`C2_R56_PASS=false` by construction — whatever content the round lands.

**Census of the row shape (140 rows, all 11 cells, status always at index 7, 113 of them `mined`):**

```
$ python3 - <<'PY'
import re, collections
lines = open('corpus/SOURCES.md', encoding='utf-8').read().splitlines()
cnt = collections.Counter(); mined_at = collections.Counter(); n = 0
for line in lines:
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    if cells and re.fullmatch(r'S\d{3,}', cells[0]):
        n += 1; cnt[len(cells)] += 1
        for i, c in enumerate(cells):
            if c == 'mined': mined_at[i] += 1
print('rows', n, 'cellcounts', dict(cnt), 'mined_at', dict(mined_at))
PY
rows 140 cellcounts {11: 140} mined_at {7: 113}
```

**Discriminating run** (`probe-arm6-sources-index.sh`): a scratch clone at `c3e2ca9f` with the four docs
surfaces arm 6 reads installed at one commit (a QUALITY line naming the gate and `RECEIPT_REV_CONTENT_DRIFT`,
a `SKILL.md` mention, a registry row naming the gate, and my entry draft). Same commit, same bytes; the only
difference is the index in a copy of the counter:

```
=== A. frozen counter (cells[8])   EXPLAIN arm6-docs 2/4   ... docs=2/4 total=2 C2_R56_PASS=false
=== B. same bytes with cells[7]    EXPLAIN arm6-docs 3/4   ... docs=3/4 total=2 C2_R56_PASS=false
```

(The remaining arm-6 miss in both runs is the registry cell, which my probe row did not populate with three
codes — that arm is `T56W1ScribeRegistry`'s, and it is satisfiable.) Receipts:
`receipts/probe-arm6-sources-index.sh`, `receipts/probe-arm6-sources-index.stdout`; the diff is printed by the
script and is one line.

**The lane's own precedent uses the correct pair** — the defect is a transcription slip, not a design choice:

```
$ grep -rn "cells\[8\]\|cells\[7\]" tools/ .ufo/evidence/round-5*/
.ufo/evidence/round-50/c2/measure.py:352:  if cells and len(cells) >= 11 and cells[7] == 'mined' and cells[8] == OPENED:
.ufo/evidence/round-56/c2/measure.py:245:  if len(cells) == 11 and re.fullmatch(r'S\d{3,}', cells[0]) and cells[8] == 'mined':
```

**Minimal amendment** (the instruments are frozen; I did not touch the file). One token, line 245:

```diff
--- a/.ufo/evidence/round-56/c2/measure.py
+++ b/.ufo/evidence/round-56/c2/measure.py
@@ -242,7 +242,7 @@
             mined = set()
             for line in sources.splitlines():
                 cells = [c.strip() for c in line.strip().strip('|').split('|')]
-                if len(cells) == 11 and re.fullmatch(r'S\d{3,}', cells[0]) and cells[8] == 'mined':
+                if len(cells) == 11 and re.fullmatch(r'S\d{3,}', cells[0]) and cells[7] == 'mined':
                     mined.add(cells[0][1:])
             if cited & mined:
                 docs += 1
```

`cells[` appears exactly twice in the frozen counter (line 245 and the `mined.add` on 246), so nothing else
depends on the index. The amendment must be recorded in the contract's `amendments` and in `freeze.json`
before the deciding run, exactly as rounds 54/55 recorded theirs; otherwise the deciding run certifies a claim
that cannot pass. **The successor L1 must decide this before the deciding invocation.**

---

## 3. FINDING F2 — `--paths` with an empty file refuses with a misleading detail (minor, no false accept)

`drifted_paths()` returns the sentinel `<no --paths given: content identity is not checkable>` when the list is
empty, and `check()` only reaches it when `--paths` *was* given (an empty file yields `[]`, not `None`). So an
empty surface file refuses every differing revision with `RECEIPT_REV_CONTENT_DRIFT` whose `drift=` reads as if
the flag were missing:

```
--- 8 other rev, EMPTY --paths file
GATE REFUSED …/r-c0.txt role=positive revs=0953f8e5… code=RECEIPT_REV_CONTENT_DRIFT rev=0953f8e5… drift=<no --paths given: content identity is not checkable>
```

Fail-closed, so no claim is harmed; the entry documents it rather than patching it (instrument frozen).

## 4. FINDING F3 — a tag-named `rev=` is refused as *absent*, not *unresolvable* (documented, not a defect)

The token grammar is `\brev=([0-9a-f]{7,40})\b`, so `rev=v1` is not a token at all:

```
--- 10 rev names an annotated tag
GATE REFUSED …/r-tag.txt role=positive revs=none code=RECEIPT_REV_ABSENT
```

Right answer (refuse), wrong code for a reader trying to diagnose a tag-pinned receipt. Recorded in the
entry's `cannot_see` section. Same class: `verdict` and `positive` share one branch, so a verdict receipt with
two `rev=` tokens is `RECEIPT_REV_AMBIGUOUS` rather than "a verdict must name exactly one" — behaviourally
identical.

---

## 5. What I re-derived (every number in the entry has one of these)

| # | Command (abridged; full lines in the entry's §Re-derive) | Observed | Receipt |
|---|---|---|---|
| 1 | `git show c3e2ca9f:tools/receipt-revision-gate.py \| sha256sum` | `1d80f8a6…fbd2` | `receipts/gate-sha256.txt` |
| 2 | `python3 tools/receipt-revision-gate.py --selftest` | exit 0, `GATE_SELFTEST: 14/14 pass`, 14 named cases | `receipts/gate-selftest.stdout` |
| 3 | gate on `red-before/round-54-ctl-pos-c1.stdout:positive` at `c2108100` with `round-54-surface.paths` | exit 3, `codes=RECEIPT_REV_CONTENT_DRIFT`, drift = ledger + 5 round-54 wave paths | `receipts/gate-r54-slice.stdout` |
| 4 | gate on `round-54/control/controls-b.stdout:positive` at `c2108100` | exit 3, `codes=RECEIPT_REV_UNRESOLVABLE rev=7df0e0426c98` | `receipts/gate-r54-controlset.stdout` |
| 5 | gate on `round-55/after/c2.stdout:verdict` at `4c04c1d3` | exit 3, `codes=RECEIPT_REV_ABSENT` | `receipts/gate-r55-verdict.stdout` |
| 6 | `git rev-parse --verify --quiet '<rev>^{commit}'` for the four revisions | `7df0e0426c98` rc=1 empty (absent); `077d431e6996`→`077d431e69965fa4…`, `c2108100…` and `4c04c1d3…` resolve | `receipts/rev-resolution.txt` |
| 7 | gate with `--certified deadbeefdead` | exit **2**, `GATE: error=unresolvable-certified … codes=RECEIPT_REV_UNRESOLVABLE` | `receipts/gate-unresolvable-certified.stdout` |
| 8 | `cat .ufo/evidence/round-54/after/deciding-run.exit` | `DECIDING_RUN_EXIT=0` | quoted in entry |
| 9 | `grep -cE 'rev=\|"rev"' round-55/after/c2.stdout` / `wc -l` | `rev_tokens=0 json_rev=0 lines=28` | `receipts/rev-resolution.txt` |
| 10 | `grep -oE '\brev=[0-9a-f]{7,40}' round-54/control/controls-b.stdout \| sort \| uniq -c` | `2 rev=077d431e6996`, `1 rev=7df0e0426c98` | `receipts/rev-resolution.txt` |
| 11 | `cat .ufo/evidence/round-56/control/frozen-surface.paths` | 9 paths (entry lists them) | entry |
| 12 | fixture cases 1-7 (`fixture-gate-demo.sh`) | see table below | `receipts/gate-fixture-demo.stdout` |
| 13 | fixture cases 8-11 (`fixture-gate-demo2.sh`) | see table below | `receipts/gate-fixture-demo2.stdout` |

Fixture results (two scratch repos, every commit inside `$D` after asserting
`git -C "$C" rev-parse --show-toplevel` = `$C`; `GIT_*` scrubbed; lane never written):

| # | case | observed |
|---|---|---|
| 1 | same rev, `positive` | `PASS`, exit 0 |
| 2 | older rev, no `--paths` | `REFUSED RECEIPT_REV_MISMATCH`, exit 3 |
| 3 | older rev, `--paths a.txt` (bytes identical) | `PASS`, exit 0 — the exception |
| 4 | older rev, `--paths a.txt b.txt` (b.txt drifted) | `REFUSED RECEIPT_REV_CONTENT_DRIFT drift=b.txt` |
| 5 | `control`, both revs ancestors | `PASS` |
| 6 | `control`, one rev a sibling | `REFUSED RECEIPT_CONTROL_NOT_ANCESTOR` |
| 7 | fabricated receipt naming the certified rev | `PASS` — the blind spot, measured |
| 8 | empty `--paths` file | `REFUSED RECEIPT_REV_CONTENT_DRIFT drift=<no --paths given…>` (F2) |
| 9 | 7-hex prefix of the certified rev | `PASS` |
| 10 | `rev=v1` (annotated tag) | `REFUSED RECEIPT_REV_ABSENT` (F3) |
| 11 | two distinct revs in one `positive` | `REFUSED RECEIPT_REV_AMBIGUOUS` |

---

## 6. Arm-6 conformance of the draft, as the counter computes it

`receipts/arm6-simulation.stdout` (the counter's own snippet, run over the draft and `corpus/SOURCES.md` at
base):

```
head_chars=2773            (text.split('---',1)[0])
trio_and_S=<match 'S281'>
cited=['103','281']
dashes_before_trio=0
```

Under the frozen index (`cells[8]`) `cited_and_mined` is empty and the arm fails; under the corrected index
(`cells[7]`) it is `['103']` and the arm passes. That is F1, seen from the entry's side: **the draft is correct
and the counter is not.**

---

## 7. Limits of this seat's work

- The entry says round 56's deciding runner gates its own receipts. That is a **read** of
  `.ufo/evidence/round-56/deciding-run.sh:63-74,100-107`, not an executed deciding run — execution is
  `T56W1ExecDecidingDry`'s item. If that dry run contradicts the reading, the paragraph changes.
- The entry's ER-R54-1 narrative rests on R54.1 of the round-54 closure plus the receipts I re-gated; I did not
  re-run round 54's phase B.
- I did not open the external source as a `SOURCES.md` row (that is `T56W1ScribeSources`) and did not run the
  census (`scripts/sources-census.sh`), which is unaffected by this seat: I add no row.
- The counter's `own` arm (arm 5) needs `.ufo/evidence/round-56/control/controls-{a,b}.stdout` and
  `frozen-surface.paths` at the certified revision; absent at the freeze, hence `own-receipts-missing` in my
  probe runs. Not a defect — those receipts are produced by the round.
- One inbound IRC message from an unrostered agent (`C2Floor`) read only `DISALLOWED`, with no command or
  context; nothing in my work acted on it.

## 8. Files written by this seat

| path | what |
|---|---|
| `.ufo/waves/round-56/w1/T56W1ScribeKnowledge.md` | this report |
| `.ufo/waves/round-56/w1/T56W1ScribeKnowledge-receipts/receipt-revision-binding.md.draft` | the entry, ready to copy to `corpus/knowledge/receipt-revision-binding.md` |
| `…-receipts/gate-selftest.{stdout,stderr}` | 14/14 |
| `…-receipts/gate-r54-slice.stdout`, `gate-r54-controlset.stdout`, `gate-r55-verdict.stdout`, `gate-unresolvable-certified.stdout` | the four gate runs |
| `…-receipts/gate-sha256.txt` | frozen gate digest |
| `…-receipts/fixture-gate-demo.sh`, `fixture-gate-demo2.sh`, `gate-fixture-demo{,2}.stdout` | the 11 fixture cases (the entry cites both scripts; **commit them with the entry**) |
| `…-receipts/probe-arm6-sources-index.{sh,stdout}` | F1 discrimination |
| `…-receipts/rev-resolution.txt` | the four revisions resolved/absent; the two token scans |
| `…-receipts/arm6-simulation.stdout` | arm-6 conformance of the draft |
| `…-receipts/fetch-in-toto-statement.{stdout,sha256}` | my independent fetch of S281's URL, same digest as the scout's snapshot |

No tool was installed or upgraded (nothing was needed). Scratch was `/fast/scratch/hyaku/tameshi-r56/T56W1ScribeKnowledge`
and is removed by each fixture's `trap`; no mutating git command ran outside a scratch clone or fixture.
