source: S281 — in-toto Attestation Framework, Statement layer specification — https://github.com/in-toto/attestation/blob/v1.2.0/spec/v1/statement.md — §Fields, `subject` field, IMPORTANT paragraph at lines 54-55 @ tag v1.2.0 (raw fetch 2026-10-28T18:42:42Z, sha256 cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea, 2492 B, byte-identical at `main` the same minute); S103 — https://git-scm.com/docs/git-hash-object — §DESCRIPTION, first sentence @ page fetched 2026-10-24 (a blob's object id is computed from the contents of the named file, so a recorded digest binds evidence to exact bytes); own work — `tools/receipt-revision-gate.py` (sha256 `1d80f8a6…fbd2` at `c3e2ca9f`), `.ufo/evidence/round-54/control/controls-b.stdout`, `.ufo/evidence/round-55/after/c2.stdout`, `.ufo/evidence/round-56/c2/red-before/`, `corpus/lessons/round-54-verifier-spotcheck.md` (R54.1), `corpus/lessons/round-55-verifier-spotcheck.md` (R55.5)
verified-at: 2026-10-28 — every command under §Re-derive ran at lane `c3e2ca9f0207` (HEAD when this note was written); the outputs are under `.ufo/waves/round-56/w1/T56W1ScribeKnowledge-receipts/`
recheck: 180d — `curl -fsSL https://raw.githubusercontent.com/in-toto/attestation/v1.2.0/spec/v1/statement.md | sha256sum` must print `cbe684a1…ebea` (anything else: the tag moved, re-open the row); `python3 tools/receipt-revision-gate.py --selftest` must print `GATE_SELFTEST: 19/19 pass (ER-R56-K2)`

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
## Errata — round 56 wave-2 re-open (2026-10-28)

Corrections are additive; the original wording above remains the freeze-era record.

### ER-R56-K1 — the first S281 quotation is a splice, not a source sentence

Lines 7–10 join two excerpts while presenting the first as one quotation. The L1 re-opened
S281 on 2026-10-28. At `§Fields`, `subject`, snapshot lines 36–37, the exact text is:

> Set of software artifacts that the attestation applies to. Each element represents a
> single software artifact. Each element MUST have `digest` set.

The quote at lines 8–10 about subjects matched purely by digest remains verbatim at lines
54–55. Re-open evidence: `.ufo/waves/round-56/integration/l1-source-reopen.txt`.

### ER-R56-K2 — gate count and digest changed in amendment 1

The frontmatter `recheck:` and §Falsifier item 3 still name the original freeze's
`GATE_SELFTEST: 14/14 pass`. Amendment 1 at `21eb3c6` changed the gate before controls;
the C0 gate prints `GATE_SELFTEST: 19/19 pass` (exit 0), and its C0 sha256 is
`c60772ceb0ce3f51df57148bd006c9bd4544a5403317dffa87f8bf7ae0569ac9`. The freeze-era
digest `1d80f8a6…` and 14/14 result remain historical values for `c3e2ca9f`. For a
current-tree recheck, use 19/19 and verify the source snapshot independently. Receipt:
`.ufo/waves/round-56/w2/T56W2RevStalePointers.md` P8–P9.

### ER-R56-K3 — the fixture-demo invocation needs its environment

The §Re-derive step 6 commands as printed fail with `HYAKU_SCRATCH` unset (exit 1).
Use the following from the lane root:

```sh
export HYAKU_SCRATCH=/fast/scratch/hyaku
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
bash .ufo/waves/round-56/w1/T56W1ScribeKnowledge-receipts/fixture-gate-demo.sh
bash .ufo/waves/round-56/w1/T56W1ScribeKnowledge-receipts/fixture-gate-demo2.sh
```

The failing invocation and the corrected commands are preserved in
`.ufo/waves/round-56/w2/T56W2RevStalePointers.md` P15.
