# T56W1ExecGateFuzz — crafted-receipt fuzz of the frozen receipt-revision gate

Round 56, wave 1, seat `T56W1ExecGateFuzz`. Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Read-only against the lane: no production file, no frozen instrument and no git state was touched.
All revisions live in a scratch fixture; the gate was exercised from a scratch copy.

## Instrument under test

| item | value |
|---|---|
| file | `tools/receipt-revision-gate.py` |
| sha256 (working tree, lane) | `1d80f8a665f83508a05a33827de66ffd53c986e8de25f8f77937707cac78fbd2` |
| sha256 at frozen set `c3e2ca9f0207` | `1d80f8a6…78fbd2` (identical) |
| sha256 in `.ufo/evidence/round-56/freeze.json` | `1d80f8a6…78fbd2` (identical) |
| present at contract base `981c5e8b` | **no** — `git show 981c5e8b:tools/receipt-revision-gate.py` fails; the freeze commit `c3e2ca9f` adds the file (and is a descendant of the base) |

Integration consequence: C2's counter copies the gate out of REV (`show(lane, rev, GATE)`), so **REV cannot be the contract base**; any C0/REV for C2 must descend from the freeze commit.

Commands:

```
$ git -C <lane> show c3e2ca9f0207:tools/receipt-revision-gate.py | sha256sum
1d80f8a665f83508a05a33827de66ffd53c986e8de25f8f77937707cac78fbd2  -
$ sha256sum <lane>/tools/receipt-revision-gate.py
1d80f8a665f83508a05a33827de66ffd53c986e8de25f8f77937707cac78fbd2  <lane>/tools/receipt-revision-gate.py
$ git -C <lane> show 981c5e8b20a2:tools/receipt-revision-gate.py
fatal: path 'tools/receipt-revision-gate.py' exists on disk, but not in '981c5e8b20a2…'
$ git -C <lane> merge-base --is-ancestor 981c5e8b20a2 c3e2ca9f0207 && echo yes
yes
```

## Method

- Scratch: `export HYAKU_SCRATCH=/fast/scratch/hyaku; S=$HYAKU_SCRATCH/tameshi-r56/T56W1ExecGateFuzz`;
  fixture `D=$(mktemp -d "$S/fixture.XXXXXX")`, `git -C "$D" rev-parse --show-toplevel` == `$D` before every commit.
- Fixture: `A` (c0) → `B` (c1, `moved.txt` changed) → `C` (c2, `other.txt` changed, the certified revision); side branch `SD` from `A`.
  Tags: lightweight `rel-b`→B, annotated `ann-a`→A, and two deliberately hex-named tags `2765397` (= A's commit prefix) and `233c212` (= C's commit prefix), both pointing at **B**.
  Plus 80 000 `git fast-import` blobs to obtain a genuinely ambiguous 7-hex object prefix (`0199b70`, two blobs).
- 45 crafted receipts, one gate invocation each (`--lane D --certified <rev>`), receipts and outputs kept under
  `.ufo/waves/round-56/w1/T56W1ExecGateFuzz-receipts/` (`fuzz.tsv`, `fuzz.log`, `fuzz-receipts/`).
- "Expected" is what the C2 claim implies: a receipt must demonstrably bind the certified revision, a refusal must carry the code that names the actual reason (C2 kill rule: *"a refusal the gate reaches for the wrong reason is a miss"*).
- 20 one-token mutants of the gate, each run through the gate's own `--selftest` (C2 arm 1), to measure whether the suite can see the fuzz classes.

Gate hash on every fuzz row: `1d80f8a665f8`.

## Result summary (45 cases)

| verdict | n | meaning |
|---|---|---|
| RIGHT | 26 | accept/refuse and code match the C2 claim |
| FALSE_ACCEPT | 6 | PASS although no binding is established (04, 14, 16, 18, 42, 44) |
| FALSE_REFUSE | 7 | REFUSED although the receipt binds (06, 11, 15, 17, 19, 22, 23) |
| MISLABEL | 3 | refused, but the code names the wrong reason (03, 25, 36) |
| EXPLOITABLE | 1 | accepted via a caller-controlled `--paths` subset (30) |
| DECLARED_GAP | 1 | accepted; contract `cannot_see` declares it (07) |
| CRASH | 1 | no GATE line, exit 1, traceback (27) |

### The 45 cases

| # | case | role | expected (C2) | observed | code | verdict |
|---|---|---|---|---|---|---|
| 01 | no rev | positive | REV_ABSENT | REFUSE | RECEIPT_REV_ABSENT | RIGHT |
| 02 | two revs in one positive | positive | AMBIGUOUS | REFUSE | RECEIPT_REV_AMBIGUOUS | RIGHT |
| 03 | `rev=A` inside a path string | positive | REV_ABSENT | REFUSE | RECEIPT_REV_MISMATCH | MISLABEL |
| 04 | `rev=C` inside a path string | positive | REV_ABSENT | **ACCEPT** | none | FALSE_ACCEPT |
| 05 | JSON `{"rev": "C"}` | verdict | ACCEPT | ACCEPT | none | RIGHT |
| 06 | JSON `{"rev": "<C upper 12>"}` | verdict | ACCEPT | REFUSE | RECEIPT_REV_ABSENT | FALSE_REFUSE |
| 07 | names C but is a C1 receipt | verdict | ACCEPT (declared blind spot) | ACCEPT | none | DECLARED_GAP |
| 08 | sidecar matches | positive | ACCEPT | ACCEPT | none | RIGHT |
| 09 | sidecar = 64 zeros | positive | DIGEST_MISMATCH | REFUSE | RECEIPT_DIGEST_MISMATCH | RIGHT |
| 10 | sidecar empty | positive | DIGEST_MISMATCH | REFUSE | RECEIPT_DIGEST_MISMATCH | RIGHT |
| 11 | sidecar uppercase digest | positive | ACCEPT | REFUSE | RECEIPT_DIGEST_MISMATCH | FALSE_REFUSE |
| 12 | `rev=rel-b` (tag name) | positive | REV_ABSENT | REFUSE | RECEIPT_REV_ABSENT | RIGHT |
| 13 | `rev=ann-a` (annotated tag) | positive | REV_ABSENT | REFUSE | RECEIPT_REV_ABSENT | RIGHT |
| 14 | `rev=2765397` (A's prefix, tag→B), certified B | positive | MISMATCH | **ACCEPT** | none | FALSE_ACCEPT |
| 15 | `rev=233c212` (C's prefix, tag→B), certified C | positive | ACCEPT | REFUSE | RECEIPT_REV_MISMATCH | FALSE_REFUSE |
| 16 | `rev=C` only in a `#` comment | positive | REV_ABSENT | **ACCEPT** | none | FALSE_ACCEPT |
| 17 | `# rev=A` comment + real `rev=C` line | positive | ACCEPT | REFUSE | RECEIPT_REV_AMBIGUOUS | FALSE_REFUSE |
| 18 | `rev=C` only inside a markdown fence | positive | REV_ABSENT | **ACCEPT** | none | FALSE_ACCEPT |
| 19 | `rev=A` in fence + real `rev=C` line | positive | ACCEPT | REFUSE | RECEIPT_REV_AMBIGUOUS | FALSE_REFUSE |
| 20 | 7-hex prefix of B | positive | ACCEPT | ACCEPT | none | RIGHT |
| 21 | 12-hex prefix of C | positive | ACCEPT | ACCEPT | none | RIGHT |
| 22 | uppercase 12-hex of C | positive | ACCEPT | REFUSE | RECEIPT_REV_ABSENT | FALSE_REFUSE |
| 23 | 6-hex prefix of C | positive | ACCEPT | REFUSE | RECEIPT_REV_ABSENT | FALSE_REFUSE |
| 24 | 41 hex chars | positive | REV_ABSENT | REFUSE | RECEIPT_REV_ABSENT | RIGHT |
| 25 | `rev = C` (spaced) | positive | REV_ABSENT (format) | REFUSE | RECEIPT_REV_ABSENT | MISLABEL |
| 26 | `notrev=C` | positive | REV_ABSENT | REFUSE | RECEIPT_REV_ABSENT | RIGHT |
| 27 | receipt path is a directory | positive | NOT_BLOB | **CRASH** (exit 1, traceback) | none | CRASH |
| 28 | receipt missing | positive | MISSING | REFUSE | RECEIPT_MISSING | RIGHT |
| 29 | receipt blank | positive | EMPTY | REFUSE | RECEIPT_EMPTY | RIGHT |
| 30 | `rev=A`, `--paths` = one unchanged path | positive | CONTENT_DRIFT | **ACCEPT** | none | EXPLOITABLE |
| 31 | `rev=A`, `--paths` = the changed path | positive | CONTENT_DRIFT | REFUSE | RECEIPT_REV_CONTENT_DRIFT | RIGHT |
| 32 | control rev = side branch | control | NOT_ANCESTOR | REFUSE | RECEIPT_CONTROL_NOT_ANCESTOR | RIGHT |
| 33 | control rev = certified | control | ACCEPT | ACCEPT | none | RIGHT |
| 34 | control A + C | control | ACCEPT | ACCEPT | none | RIGHT |
| 35 | control rev unresolvable | control | UNRESOLVABLE | REFUSE | RECEIPT_REV_UNRESOLVABLE | RIGHT |
| 36 | ambiguous 7-hex object prefix | positive | ambiguity named | REFUSE | RECEIPT_REV_UNRESOLVABLE | MISLABEL |
| 37 | JSON rev + text rev | verdict | AMBIGUOUS | REFUSE | RECEIPT_REV_AMBIGUOUS | RIGHT |
| 38 | JSON `{"REV": "C"}` | verdict | REV_ABSENT (schema) | REFUSE | RECEIPT_REV_ABSENT | RIGHT |
| 39 | `rev=<blob sha>` | positive | UNRESOLVABLE | REFUSE | RECEIPT_REV_UNRESOLVABLE | RIGHT |
| 40 | required line absent | verdict | REQUIRED_LINE_MISSING | REFUSE | RECEIPT_REQUIRED_LINE_MISSING | RIGHT |
| 41 | same rev twice | positive | ACCEPT | ACCEPT | none | RIGHT |
| 42 | `rev=C` in a URL query | positive | REV_ABSENT | **ACCEPT** | none | FALSE_ACCEPT |
| 43 | `--paths` = comments only | positive | CONTENT_DRIFT | REFUSE | RECEIPT_REV_CONTENT_DRIFT | RIGHT |
| 44 | `--paths` = a nonexistent path | positive | CONTENT_DRIFT | **ACCEPT** | none | FALSE_ACCEPT |
| 45 | sidecar mismatch + unresolvable rev | positive | both codes | REFUSE | DIGEST_MISMATCH,UNRESOLVABLE | RIGHT (detail loss) |

## Findings

### F1 — the token model is "any `rev=<hex>` anywhere in the bytes" (false accepts; false refusals)

`REV_RE = r'\brev=([0-9a-f]{7,40})\b'` is applied to the whole decoded receipt with no line or field structure.
A filename (`04`), a comment (`16`), a fenced block (`18`) and a URL query (`42`) therefore bind the receipt:
four receipts that name no revision PASS. The mirror image is worse for real receipts: a historical revision
quoted in a comment or a fence plus the real `rev=` line is REFUSED `RECEIPT_REV_AMBIGUOUS` (`17`, `19`).

```
$ python3 <scratch>/gate.py --lane <fixture> --certified 233c2123… \
    --receipt …/04-rev-in-path-certified:positive
GATE OK …/04-rev-in-path-certified role=positive revs=233c212
GATE: receipts=1 ok=1 refused=0 codes=none verdict=PASS
$ … --receipt …/17-comment-plus-real:positive
GATE REFUSED …/17-comment-plus-real role=positive revs=2765397,233c212 code=RECEIPT_REV_AMBIGUOUS revs=2765397,233c212
```

For C2: "every receipt the lane certifies is bound to the revision it was measured against" is not delivered by
this rule. A copied token is declared in `cannot_see`, but a token that is a path component or a comment is not
even a copied claim, and the gate cannot tell the difference. The knowledge entry / QUALITY criterion must state
that the gate binds a *textual token*, not a field, or C2 must add a line-structured form.

### F2 — hex-named tags shadow commit prefixes (false accept and false refusal)

`resolve()` uses `git rev-parse --verify --quiet <rev>^{commit}`; git checks refs before object prefixes and only
warns on stderr, which the gate captures and discards.

```
$ git -C <fixture> rev-parse --disambiguate=2765397
27653978b812c14d60ba7eefb9ebdcf9bb4b22f7          # A's commit
$ git -C <fixture> rev-parse 2765397
warning: refname '2765397' is ambiguous.
1eaad2c99ea0675b5d285ac8b73d6212e1154088          # B, because tag 2765397 -> B
```

Case `14` (certified B, receipt `rev=2765397`) PASSES although the token is A's commit prefix; case `15`
(certified C, receipt `rev=233c212`) is REFUSED because a tag of that name points at B. The gate never sees the
ambiguity warning and has no code for it.

### F3 — the accepted spelling is narrower than git (false refusals, wrong code)

Lowercase, 7–40 hex only. Uppercase (`22`, `06`) and 6-hex (`23`) prefixes resolve in git — and the gate accepts
the same spellings for `--certified` — but a receipt is reported `RECEIPT_REV_ABSENT`:

```
$ python3 <scratch>/gate.py --lane <fixture> --certified 233C212305DB \
    --receipt …/22-uppercase-hex:positive
GATE REFUSED … revs=none code=RECEIPT_REV_ABSENT
$ python3 <scratch>/gate.py --lane <fixture> --certified 233c21 \
    --receipt …/23-prefix-6:positive
GATE REFUSED … revs=none code=RECEIPT_REV_ABSENT        # certified 6-hex resolved fine
```

Refusing is safe, but C2's kill rule makes the wrong reason a miss: the receipt does name the revision.

### F4 — ambiguity of an object prefix is reported as unresolvable

`0199b70` names two blobs in the fixture; `^{commit}` fails, so the gate emits `RECEIPT_REV_UNRESOLVABLE`
(`36`). `RECEIPT_REV_AMBIGUOUS` means "several rev tokens in the text", not "ambiguous object name". Likewise an
unresolvable `--certified` prints `codes=RECEIPT_REV_UNRESOLVABLE` with exit 2 — a receipt code for a non-receipt
condition.

### F5 — the gate is not total: a non-blob receipt crashes it (dead `RECEIPT_NOT_BLOB`)

```
$ python3 <scratch>/gate.py --lane <fixture> --certified 233c2123… \
    --receipt …/27-directory-receipt:positive
exit=1 observed=CRASH codes=none
--- stderr ---
  File "<scratch>/gate.py", line 98, in check
    data = p.read_bytes()
IsADirectoryError: [Errno 21] Is a directory: '…/27-directory-receipt'
```

No `GATE:` line, no code, exit 1. `RECEIPT_NOT_BLOB` is declared in the docstring and in `CODES` but appears
nowhere else (`grep -n RECEIPT_NOT_BLOB` → lines 26 and 46 only). Two more non-refusal exits: a missing
`--paths` file raises `FileNotFoundError`; a `:` in the receipt path is a usage error (exit 1).

### F6 — `--paths` is caller-controlled; one unchanged or one nonexistent path certifies any revision

`drifted_paths()` diffs only the listed paths. Case `30` (`rev=A`, list = `surface.txt`, unchanged between A and C)
PASSES; case `44` (`--paths` = `no-such-path.txt`) PASSES because git prints nothing for an absent path. An empty
list is refused (`43`, the sentinel), so the failure mode is silent under-specification, not emptiness. The
docstring declares content identity as intended, but the gate cannot know the list covers the claim's surface;
C2's own measure passes a frozen list, which is the right discipline — the *rule* must say the paths file is part
of the claim.

### F7 — the digest sidecar is adjacency-only, case-sensitive, and short-circuits

`<receipt>.sha256` is checked only when it sits next to the receipt. The real round-54 slice has a sidecar
(`3310ff60…`, matches) and C2 arm 2 copies the slice into `--work` without it, so the digest arm is silently
dropped; in place, the same invocation checks it:

```
$ python3 <scratch>/gate.py --lane <lane> --certified c2108100… --paths …/round-54-surface.paths \
    --receipt <lane>/.ufo/evidence/round-56/c2/red-before/round-54-ctl-pos-c1.stdout:positive
GATE REFUSED … code=RECEIPT_REV_CONTENT_DRIFT …            # digest checked and matched
$ cp …/round-54-ctl-pos-c1.stdout <scratch>/slice-copy.stdout   # what measure.py does
GATE REFUSED … code=RECEIPT_REV_CONTENT_DRIFT …            # digest arm never runs
```

An uppercase digest is a false refusal (`11`); a digest failure returns before the revision checks, so a bad
sidecar masks the drift (`lane-red54-slice-copy-badsidecar.out` reports only `RECEIPT_DIGEST_MISMATCH`).

### F8 — one `detail` slot for several causes

`check()` overwrites `detail`. Case `45` refuses with `codes=RECEIPT_DIGEST_MISMATCH,RECEIPT_REV_UNRESOLVABLE`
but `detail` names only `rev=deadbeefdead`; the sidecar cause is lost from the line (it survives in `--json` only
as the code list).

### F9 — declared blind spots and JSON shape

A receipt naming C for another claim passes (`07`; contract `cannot_see`). JSON receipts bind only the exact
lowercase key `"rev"`: `{"REV": …}` and a numeric rev are `RECEIPT_REV_ABSENT` (`38`, and `06` for the uppercase
value); `{"rev": "C"}` plus a text `rev=A` is `AMBIGUOUS` (`37`). If the round's knowledge entry advertises JSON
receipts, it must give the exact key spelling.

### F10 — dead code

`check(..., required)` never uses `required` (the regex comes from the receipt tuple); the sidecar file is read
twice; `RECEIPT_NOT_BLOB` is unreachable. None of these change a verdict today.

## Mutation test of C2 arm 1 (the gate's own suite)

20 one-token mutants, each run through `--selftest`; baseline `GATE_SELFTEST: 14/14 pass`, exit 0.
**14 killed / 6 survived.**

| mutant | result | failing selftest cases |
|---|---|---|
| M01 mismatch-off | KILLED | content-drift-refused, strict-mismatch-refused |
| M02 ambiguous-off | KILLED | ambiguous-refused |
| M03 ancestor-off | KILLED | control-not-ancestor-refused |
| M04 digest-off | KILLED | digest-mismatch-refused |
| M05 required-line-off | KILLED | required-line-refused |
| M06 empty-off | KILLED | empty-refused |
| M07 missing-off | KILLED | missing-refused (crash) |
| M08 drift-always-empty | KILLED | content-drift-refused |
| M09 drift-always-nonempty | KILLED | content-identical-positive-accepted |
| M10 rev-min-4 | **SURVIVED** | — |
| M11 json-rev-off | **SURVIVED** | — |
| M12 exit0-always | KILLED | 10 of 14 cases |
| M13 rev-uppercase-ok | **SURVIVED** | — |
| M14 resolve-always-none | KILLED | 13 of 14 cases |
| M15 sidecar-ignored | KILLED | digest-mismatch-refused |
| M16 control-as-positive | KILLED | control-ancestors-accepted, control-not-ancestor-refused |
| M17 rev-dedup-off | **SURVIVED** | — |
| M18 unresolvable-continues | KILLED | unresolvable-refused (crash) |
| M19 role-check-off | **SURVIVED** | — |
| M20 path-check-off | **SURVIVED** | — |

The six survivors are exactly the fuzz classes the suite does not cover: 6-hex/uppercase spellings (M10, M13),
JSON receipts (M11), duplicate tokens (M17), role validation (M19), the empty-paths sentinel (M20). No selftest
case exercises a `rev=` token in a path/comment/fence/URL, so the F1 false accepts are invisible to arm 1. Arm 1
is live for the core codes (M01–M09, M12, M14–M16, M18 are killed), but its 14/14 is not evidence about the token
model.

## Lane liveness (real receipts, read-only)

```
$ python3 <scratch>/gate.py --lane <lane> --certified c2108100… --paths …/round-54-surface.paths \
    --receipt …/round-54-ctl-pos-c1.stdout:positive
GATE REFUSED … revs=077d431e6996 code=RECEIPT_REV_CONTENT_DRIFT rev=077d431e6996 drift=.ufo/evidence/round-21/coldread/ledger.json,…
GATE: receipts=1 ok=0 refused=1 codes=RECEIPT_REV_CONTENT_DRIFT verdict=REFUSED      exit=3

$ … --certified c2108100… --receipt <lane>/.ufo/evidence/round-54/control/controls-b.stdout:positive
GATE REFUSED … revs=077d431e6996,7df0e0426c98 code=RECEIPT_REV_UNRESOLVABLE rev=7df0e0426c98   exit=3

$ … --certified 4c04c1d3… --receipt <lane>/.ufo/evidence/round-55/after/c2.stdout:verdict
GATE REFUSED … revs=none code=RECEIPT_REV_ABSENT                                                exit=3

$ python3 <scratch>/gate.py --selftest
GATE_SELFTEST: 14/14 pass                                                                        exit=0
```

The three red-before refusals C2 names are live with their named codes; the round-54 old-gate acceptance
(`DECIDING_RUN_EXIT=0`) is on record in `.ufo/evidence/round-54/after/deciding-run.exit` (not re-run here).
C2 arm 5's own receipts (`.ufo/evidence/round-56/control/controls-a.stdout`, `controls-b.stdout`) do not exist
yet, so they were not exercised; the `before/c2.stdout` line `own=own-receipts-missing` is consistent with that.

## Bearing on C2

- C2's declared arms are **not falsified**: selftest 14/14 holds; the three real receipts are refused with the
  codes C2 names; the deciding-run acceptance is on record. C2 can reach PASS.
- C2's *surface sentence* — "every receipt the lane certifies is bound to the revision it was measured against" —
  is **false as a universal**. Six crafted receipts that establish no binding PASS (04, 14, 16, 18, 42, 44), one
  more passes through a caller-chosen path subset (30), and the gate crashes instead of refusing on a non-blob
  receipt (27). The gate binds a *textual token found anywhere in the bytes* and cannot distinguish a claim from
  a filename, a comment, a fence, a URL, or a shadowing tag name.
- Therefore the C2 knowledge entry, the `corpus/QUALITY.md` criterion and the `SKILL.md` `## Standing rules` rule
  must not claim more than the arms measure. A defensible wording: the gate binds a `rev=<hex>` token anywhere in
  the receipt to the certified commit, resolves it with `git rev-parse <tok>^{commit}` (so tag names and ref
  precedence apply), checks a same-directory `.sha256` sidecar when present, and treats `--paths` as part of the
  claim; it does not prove the receipt was produced by the run it names, and it does not parse fields.
- If the round wants the stronger guarantee, the minimal patch (not applied — the gate is frozen) is: (1) match
  `rev=` only on lines beginning `VERDICT:`/`CTL` (or a dedicated `REVISION:` field) and ignore fenced/comment
  regions; (2) call `git rev-parse --disambiguate=<tok>` and emit a named ambiguity code when >1 object matches;
  (3) accept any case and 4–40 hex, consistent with `--certified`; (4) stat the receipt and emit
  `RECEIPT_NOT_BLOB` instead of crashing; (5) compare sidecar digests case-insensitively and keep both causes;
  (6) require the `--paths` file to exist, be non-empty, and be recorded in the gate output. Each of these is a
  scratch-clone demonstration only; no lane bytes were changed.

## Freeze discipline and lane hygiene

- Gate bytes identical at the frozen set, in `freeze.json`, and in the lane working tree (`1d80f8a6…`).
- No frozen instrument and no lane production file was written; my writes are the report, the JSON beside it and
  `…-receipts/` only.
- `git -C <lane> status --porcelain` after the run lists only untracked round-56 evidence/wave directories
  (peers' and mine); no tracked modification, HEAD still `c3e2ca9f0207`.
- Fixture mutations were confined to `$S/fixture.*`; `git -C "$D" rev-parse --show-toplevel` printed `$D` before
  any commit. Scratch removed at the end.

## Reproduction

```
export HYAKU_SCRATCH=/fast/scratch/hyaku
S=$HYAKU_SCRATCH/tameshi-r56/T56W1ExecGateFuzz; mkdir -p "$S"
# fixture (4 commits, tags, 80k fast-import blobs) — see the transcript in this report's method section
python3 .ufo/waves/round-56/w1/T56W1ExecGateFuzz-receipts/fuzz-driver.py \
    "$S/gate.py" "$S/fixture.XXXX" <receipts>/revs.env "$S/collision.txt" <receipts>
python3 .ufo/waves/round-56/w1/T56W1ExecGateFuzz-receipts/mutate.py "$S/gate.py" <receipts>
```

Artifacts: `fuzz.tsv` (45 rows: case, role, expected, observed, code, exit, verdict, gate_sha256), `fuzz.log`
(every invocation with stdout/stderr), `mutants.tsv` / `mutants.log`, `fuzz-receipts/` (the 45 receipt files and
sidecars), `lane-*.out`, `cli-probes.out`, `git-probes.out`.

## Risks / notes for the L1

- The scratch fixture and its revisions are gone after cleanup; `fuzz.tsv` records the observed codes and the
  full command lines are in `fuzz.log`, so the evidence is auditable but not re-runnable without rebuilding the
  fixture (the driver rebuilds it deterministically except for commit hashes).
- `--paths` laundering (F6) is the finding most likely to matter to C2's own arm 5: the round's own control
  receipts are accepted against a frozen paths list, which is correct discipline, but nothing in the gate binds
  that list to the claim — the C2 report should say the list is the claim, not the gate.
- Tooling: none installed or upgraded; `python3 3.14.8`, `git 2.56.0` as present.
