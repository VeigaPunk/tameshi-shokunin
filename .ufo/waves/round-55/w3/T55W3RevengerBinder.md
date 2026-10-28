# T55W3RevengerBinder — the round-54 re-key binder: intent, invariants, and this round's reuse

Seat: revenger (L1 TameshiR55, wave 3). Axis: calibration. Milestone: the binder's intent.
Write scope used: this file plus `.ufo/waves/round-55/w3/T55W3RevengerBinder-receipts/`.
Nothing in the lane was edited; every mutation happened in `git clone --shared` fixtures under
`/fast/scratch/hyaku/tameshi-r55/T55W3RevengerBinder/` (`git rev-parse --show-toplevel` asserted
equal to each fixture before any commit there). No lane production file, frozen file, contract,
freeze or spec was touched. No tool was installed (pacman paused anyway); no install was needed.

---

## 0. Verdict

**The mechanism is sound and is exactly the right instrument for this round; the landed copy is not
yet fit to run, and the argument that decides whether the round keeps or loses its 18 sections is
`PIN` — which must be re-derived at bind time and is *no longer C0*.**

Measured during this seat, the lane moved twice (HEAD `4f7a704` → `4c04c1d`): commits `51d1f0e`
(C1 fix pass) and `4c04c1d` (C2 QUALITY erratum) changed four pinned inputs after C0
(`tools/context-capture.py`, `tools/registry-check.py`, `tools/registry.json`, `corpus/QUALITY.md`).
A bind with `PIN=C0` therefore pins bytes the tree no longer has, and the credit gate reports
`input-drift` for every section whose prior input union names them. A bind with
`PIN=HEAD` reports clean. Receipts r10 / r9.

Three findings, in order of consequence:

1. **`PIN` is the one argument.** It must name the revision that last touches any pinned input,
   re-derived immediately before the bind. Passing C0 loses sections (r10); passing the base
   loses six inputs (r4). The code accepts either silently (r10, r4).
2. **The landed binder cannot execute at all.** `.ufo/evidence/round-55/integrate/binder.py:54`
   reads `item['n']` from `.ufo/evidence/round-55/integrate/resolutions.json`, which in this round
   is a wave-1 disposition list (`id/from/finding/decision/evidence`) — `KeyError: 'n'` before any
   work (r1). The heading set is also read from a file that does not exist at C0 (r6).
3. **Four invariants the docstring claims are not enforced by the code** (PIN validity, "committed"
   reader reports, adjudication before a verdict is rewritten, md/JSON agreement), plus six smaller
   ones. §5.

Confidence: high on 1 and 3 (each has a command + output below); high on 2 (reproduced);
high on the invariant reconstruction (code read line by line, cross-checked against the credit
algorithm in `.ufo/evidence/round-18/measure.py`, which is what actually verifies entries).

---

## 1. What the round-54 binder was built to do

The round-54 lesson's method section states the failure it repairs, verbatim:

> "Round 53 lost the cold-read floor to a mechanism, not to prose: an entry credits only while its
> pinned inputs still verify, so a re-key that pins `LOG.md` or `SCORECARD.md` is stale one commit
> later, and a section whose bytes changed has no matching entry at all. This round's repair is
> therefore ordering discipline: all content edits land first (`c0`), readers read the final bytes,
> the entries pin only artifacts those edits did not touch, and the deciding run re-derives 64/64
> from the committed tree."
> — `corpus/lessons/round-54.md`, `## The method (for the round report)`

The binder is the mechanical half of that discipline. It is not an evaluator: it never runs a
reader, never judges a section, never measures credit. It **manufactures the ledger entries** that
the frozen credit algorithm (`.ufo/evidence/round-18/measure.py`, wrapped by
`.ufo/evidence/round-21/coldread/measure.py`) will later re-verify at the deciding revision. Its
whole job is to write entries whose recorded state is *still true* at the deciding revision.

That is why it has two revision arguments instead of one. The credit algorithm matches entries to
sections **by `sha256` alone** (`by_sha` index, round-18 `measure.py`), and verifies each entry's
`inputs` by re-hashing `git cat-file blob` **at the deciding revision**
(`input_failures` → `input-drift:<path>`). So:

- the section bytes must be the bytes the reader read (`read_rev` = C0);
- the input digests must be the bytes the deciding tree will hold (`PIN` = content-final).

If those two revisions are the same commit, the code works. If they differ — content or record
edits landed after the readers read — only a correct `PIN` keeps the entry honest. Round 54 itself
pinned **8 commits after its C0** (`C0 99c3bc88` is an ancestor of `PIN 077d431e`), which is the
precedent this round inherits.

---

## 2. The four invariants it protects, as the code implements them

Line numbers are the landed round-55 copy (`.ufo/evidence/round-55/integrate/binder.py`, 195
lines, a five-constant adaptation of `.ufo/evidence/round-54/integrate/binder.py`; the round-54
copy is identical in every line cited below).

### I1 — `read_rev` is C0, and the section sha is the frozen sectionizer's at C0

- `:91` seeds the ledger from `git show C0:.ufo/evidence/round-21/coldread/ledger.json`.
- The sectionizer is **extracted from C0** (`show(c0, '.ufo/evidence/round-18/measure.py')`) and
  executed in scratch, so the sha is produced by the frozen code, not by the reader's prose:
  `sections = {s['heading']: s for s in mod.sectionize(skill)}` where `skill = show(c0,'SKILL.md')`.
- `:111` accepts a reader only when `d['cand'] == c0` **and** `d['section_sha256'] == sec['sha256']`.
- The entry carries `'read_rev': c0` and `'sha256': sec['sha256']`.

Protects: the reader read the same bytes the entry names; the judge can re-derive the sha from the
committed blob. Confirmed live: at C0 and at HEAD `4c04c1d` the section `## Standing rules`
(17–44) hashes `acfb671a…a9ad767`, and `SKILL.md` is byte-identical across `C0..HEAD`
(`git diff --stat 9cf0146..HEAD -- SKILL.md` empty) — so the readers' C0 `cand` still validates
even though the tree moved.

### I2 — inputs are pinned at PIN, not at C0

- `:133–143`: for each heading, the input set is the **union of the section's prior ledger entries'
  `inputs` keys**, re-hashed from `git show PIN:<path>` (`hashlib.sha256(b).hexdigest()`), skipping
  `DROP` members and paths absent at PIN.
- `:157–176` writes a `tameshi-trace-inputs-v1` receipt whose `inputs` map equals the entry's, with
  `rev: C0` and a `rev_reason` that names PIN in 12 characters.

Protects: the digest equals the blob at the deciding revision — the only thing the credit gate
checks. This is the invariant that fails when PIN is wrong, and it fails **silently**: the run still
prints `REKEY …` and `REFRESH rekeyed=1 skipped=17`, and the entry is written with stale digests.

### I3 — the DROP list

- `:48`: `DROP = ('LOG.md', 'SCORECARD.md', 'SKILL.md', '.ufo/evidence/round-21/coldread/ledger.json')`.
- `:136`: `if p in inputs or p in DROP: continue` — exact string membership, applied before the blob
  lookup.

Protects: the four paths that necessarily change *after* the bind. LOG and SCORECARD are the record
the round keeps editing; SKILL.md is the artifact being read (its bytes are already pinned as the
section sha); the ledger is self-referential. Round 53 died pinning LOG/SCORECARD.

### I4 — replace-on-second-pass

- `:187–193`: before appending, remove entries with the same heading, the same `str(read_rev)`, and
  a trace path under this OUT directory.

Protects: a second bind pass does not grow the ledger. **Nuance the docstring gets wrong:** the
predicate is nearly inert, because `:91` reseeds every run from C0's blob. Measured: three runs over
three different OUT dirs each ended at 592 entries (591 seeded + 1), each time replacing the previous
file wholesale (r2, r2b, r2c). So growth is impossible — but for a different reason than stated, and
the predicate does **not** replace an entry written at a *different* `read_rev` or under a different
OUT (a second bind at a new C0 leaves the old C0's entry in the ledger; credit then takes "any
matching entry credits", round-18 `measure.py`: `covered = credited > 0 and not vetoes`).

---

## 3. Which of them this round must respect

| invariant | this round's requirement | evidence |
|---|---|---|
| I1 `read_rev` | must stay `9cf0146b94dd…` — the 18 readers wrote `cand = 9cf0146…` and SKILL.md has not changed since | `git diff --stat C0..HEAD -- SKILL.md` empty; r10 shows `REKEY` accepted `T55W3R01` with `cand 9cf0146…` |
| I2 `PIN` | must be the **content-final** revision, re-derived at bind time; today `4c04c1d…` | r10: `PIN=C0` → `input-drift` on `tools/context-capture.py` + `tools/registry.json`; `PIN=HEAD` → `[]` |
| I3 DROP | unchanged. The round's post-bind record commit will edit SCORECARD/LOG (dropped). Must **not** add `corpus/QUALITY.md`, `corpus/SOURCES.md`, `tools/*` — they are the claims' evidence | r8: union 2500 − {LOG, SCORECARD, SKILL} = 2497 = trace inputs |
| I4 replace | do not reuse an OUT for a different C0; and commit ledger + traces before the deciding run | r7b: uncommitted trace → `entry_reason = trace-missing:…` |

Two further obligations that the receipt format imposes, both measured:

- **OUT must be a canonical lane path.** `trace_rel = relpath(OUT, LANE)`; an OUT outside the lane
  yields `../…`, and the credit gate's `canonical_lane_path()` rejects `..` (r8: `False`), so the
  entry can never pass the trace gate. Use
  `.ufo/evidence/round-21/coldread/rekey-r55-9cf0146b94dd/` (r7b: canonical, inputs equal the trace).
- **The bind must run in a tree that carries the round's heading file.**
  `:49` reads `.ufo/evidence/round-55/c1/lost-headings-at-c0.json` from the **working tree**; that
  file was introduced at `4f7a704`, i.e. it does not exist at C0 (r6: `FileNotFoundError`). A bind
  from a C0 checkout — which is how the round's own discipline says receipts are made — dies before
  the first heading.

---

## 4. The one argument the L1 must pass

**`PIN` (argv 3).** `C0` is not free: it is fixed by the 18 readers' `cand`. `LANE` and `OUT` are
fixed by the bounds. `PIN` is the only argument whose value the code cannot check and whose wrong
value is invisible.

Pass **the commit that last changed any pinned input**, resolved to a full sha, immediately before
the bind. At this writing that is:

```
PIN = 4c04c1d33377e5b6a3636199c5fdda197fc670d5     # HEAD; re-derive, it moved twice during this seat
```

Derivation (run it again at bind time; the answer is only valid for the tree it was taken on):

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
git diff --name-only 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb..HEAD -- tools corpus SKILL.md
#   -> corpus/QUALITY.md, corpus/knowledge/scratch-root-contract.md,
#      tools/context-capture.py, tools/registry-check.py, tools/registry.json
for p in $(cat union-of-pinned-inputs.txt); do git log -1 --format=%h -- "$p"; done | sort -u
```

Receipt r10 (the deciding one), heading `## Context gate classification and explicit exit classes —
round 15`, entry inputs 42:

```
PIN=C0   fails at HEAD: ['input-drift:tools/context-capture.py', 'input-drift:tools/registry.json']
PIN=HEAD fails at HEAD: []
corpus/QUALITY.md        C0=-                  HEAD=-
tools/context-capture.py C0=f1043425085a08dd   HEAD=831b781054d701d7
tools/registry.json      C0=81bc7eb20e637d5c   HEAD=cfb93b899ec7e2d9
```

Receipt r4 (the other direction), heading `## Standing rules`, entry inputs 2497:

```
input_failures(PIN=BASE 0a2010a) at C0 = ['input-drift:corpus/QUALITY.md', 'input-drift:corpus/SOURCES.md',
  'input-drift:tools/context-capture.py', 'input-drift:tools/registry-check.py',
  'input-drift:tools/registry.json', 'input-drift:tools/repeat-control.py']
input_failures(PIN=C0) at C0           = []
```

Post-seat note (added after the L1 filed): the lane tip moved again to
`875bb75693bd659c5c9794a09a1137c689778390`; `git diff --stat 4c04c1d..875bb75 -- tools corpus
SKILL.md` is empty, so `4c04c1d…` and the new tip pin **identical** digests for every input. The
argument is unchanged: pass the tip at bind time (today `875bb75…`), and re-derive it then — the
value moves whenever a content edit lands, and nothing in the binder reports that it is stale.

Generalised rule: **the pinned digests must equal the blobs at the deciding revision.** Therefore
(a) PIN ≥ the last input-changing commit, and (b) no commit after the bind may touch a pinned input
— a post-bind QUALITY/SOURCES/tools edit (an erratum routed by an attack seat, say) forfeits the
sections again and requires a re-bind with a new PIN. This is the same knife that cut round 53.

---

## 5. Invariants the code does **not** enforce

Each row has a receipt; "measured" means a run, not a reading.

**E1. No validation of PIN.** `resolve(PIN)` (`:74`) accepts any commit; no ancestry test against
C0, no byte comparison of the pinned blobs with the deciding tree. `PIN=BASE` produced six
`input-drift`s and `PIN=C0` produced two at HEAD, both with exit path `REFRESH rekeyed=…` and no
warning (r4, r10).

**E2. Heading set and findings allowance are read from the live working tree.** `:49` and `:50–54`
use `Path(LANE, …).read_text()`, not `git show`. A post-freeze edit to
`c1/lost-headings-at-c0.json` changes what is bound; a working-tree `integrate/resolutions.json`
changes the allowance. Measured: at C0 the heading file does not exist → `FileNotFoundError` (r6);
today the resolutions file uses another schema → `KeyError: 'n'` (r1).

**E3. Reader reports are read from the working tree, not from a commit.** `:96`
`glob.glob(str(Path(LANE, wd, '*.json')))`, `:99` `Path(f).read_text`. The docstring says
"committed reader report". Measured: the bound entry's `reports` names a file that is untracked in
the same tree (`git status --porcelain` → `?? .ufo/waves/round-55/w3/`). An uncommitted reader
binds.

**E4. First match wins; no uniqueness, no seat check.** The loop `:113–127` `break`s on the first
`cand`+sha match, and `WAVE_DIRS` is ordered `('…/w2', '…/w3')` (`:47`), so a w2 file shadows the
w3 reader. Measured today: `## Standing rules` has **five** reader files
(`T55W2Read01/02/03`, `T55W3R07` twice) and the binder stops at the first with
`reader-has-findings:2>0` (r11 census, r6 run). A findings-bearing reader vetoes the heading even
when another reader is clean; nothing checks that the file belongs to a registered seat.

**E5. "Newest prior entry" is a hash-order artifact, and verdicts are rewritten without an
adjudication record.** `:147` `newest = max(old, key=lambda e: str(e.get('read_rev','')))` — the
lexicographic maximum of sha strings, not recency. `:150–151` then rewrites any
`gap-blocking` / `wrong-expectation` / `not-executed` verdict to `verified-record` /
`executed-ok`. Measured (r5): a fixture commit that sets the lexicographic-max prior entry
(`eb7838b1…`, round 17) to `gap-blocking` binds as `executed-ok` with `minor_gaps 0` — no
adjudication file is consulted and none is required by the code. That is how the live entry for
`## Standing rules` came out `gap-minor` with `minor_gaps 0` in the round-54 run.

**E6. The reader's `.md` is existence-checked only.** `:122` `if not md.exists()`. Measured (r5):
a reader whose JSON declares `findings: []` and whose `.md` declares a FINDING binds clean.

**E7. DROP is exact-string, silent, and mis-reported.** `:136`; the receipt's `dropped` list (`:189`)
only counts inputs *absent at PIN*, so a run that removed three DROP paths prints `dropped=0` (r8:
union 2500, DROP members `['LOG.md','SCORECARD.md','SKILL.md']`, trace 2497, `dropped: []`). A
non-canonical spelling (`./SKILL.md`, a nested `…/SKILL.md`) would not be dropped; the round-18
gate would then see it as an input and fail it.

**E8. Inputs come only from prior entries' union → new inputs are never pinned.** A section that
starts citing a new artifact gets no digest for it. Measured (r8): the new
`corpus/knowledge/scratch-root-contract.md` — the evidence for `## Standing rules`' new scratch
bullet — is **not** in the re-key entry's 2497 inputs. (Credit-wise this is lax, not wrong; audit-wise
the entry does not pin the evidence of the sentence it credits.)

**E9. The ledger is rewritten wholesale from C0's blob.** `:91` + `:195`. Any entry added to the
working-tree ledger after C0 is discarded by the bind. Also: a second bind at a *different* C0 does
not replace the first C0's entry (the predicate requires `read_rev == c0`), so two entries can
coexist for one heading — credit then accepts "any entry credits" and vetoes only on
`entry_failure`.

**E10. The trace's `argv` is not the argv that ran.** `:160`
`[sys.executable, __file__, LANE, c0, pin, str(OUT), 'section', h]` — a `section <heading>` suffix
the binder never received (there is no subcommand dispatch). Measured (r7b): the trace records 8
elements for a 5-element invocation. The round-55 dry-run copy
(`w1/T55W1ExecReKeyDryBind-receipts/binder-r55.py:192`) changed this to
`[sys.executable] + list(sys.argv) + ['section', h]` — still an appended fiction, only smaller.
`cwd` is likewise the script's directory, not the caller's. Also `:184` ships
`'L1 TameshiR55a2 re-key (round 54)'` as the seat string inside a round-55 file.

**E11. OUT placement is not validated.** `:93`; a non-canonical trace path can never pass the trace
gate (r8: `canonical_lane_path('../outA/traces/section-07.json') = False`).

**E12. Nothing checks that the section bytes at the deciding revision equal C0's.** Only sha
equality at credit time does that, so a post-C0 SKILL.md edit silently uncredits all 18 (here
SKILL.md is unchanged — verified).

**E13. `commands_executed_count = 1 + len(inputs)`** (`:181`-ish) is a formula, not a count of
commands executed; for `## Standing rules` it records 2498.

---

## 6. Is this round's reuse sound?

**Mechanically yes — and the C0/PIN split is precisely what keeps the 18 sections alive**, because
the readers read C0 while the inputs moved to `51d1f0e`/`4c04c1d`. **As landed, no** — the copy
cannot run, and three of the round-55 dry run's five deltas were not carried:

```
$ python3 .ufo/evidence/round-55/integrate/binder.py LANE 9cf0146… 133b2ce… OUT
  File ".../integrate/binder.py", line 54, in <module>
    RES[item['heading']] = int(item['n'])
KeyError: 'n'
```

Required before the bind (all cheap, none of them a redesign):

1. **Neutralise or relocate the `RES` read** (`:50–54`). Round 55's
   `integrate/resolutions.json` is a disposition list, not a `{heading, n}` allowance file. Either
   treat an absent/incompatible file as zero allowance (strict) and name the allowance file
   separately, or change the file's name/schema. Do not silently keep reading it.
2. **Pass `PIN` = the content-final commit, re-derived at bind time** (today `4c04c1d…`). §4.
3. **Run where `c1/lost-headings-at-c0.json` exists** (a lane tree at ≥ `4f7a704`, not a C0
   checkout) — or pass the heading set explicitly, as the dry-run copy's `--headings` does.
4. **OUT inside the lane** at `.ufo/evidence/round-21/coldread/rekey-r55-<c0:12>/`, and **commit**
   ledger + traces before the deciding run.
5. **Adjudicate before binding.** 11 of the 18 headings already carry readers with ≥1 finding (r11
   census) — including `## Standing rules` (2 findings across five reader files), `### The service's
   limits` (4) and `### Triggers T1–T3` (2). With zero allowance the binder exits 1 with
   `reader-has-findings:n>0` for each. The allowance file must be in the binder's schema, and each
   allowance needs the adjudication record the round-54 `resolutions.json` carried.
6. Optional but record-correct: take the dry-run copy's truthful-ish `argv`/`seats`/`--label`
   handling and fix the `(round 54)` seat string.

What the L1 should **not** do: pass `PIN=C0` "because C0 is the content commit". That was true when
this wave's spec was written; it stopped being true at `51d1f0e`. The whole point of the binder's
two revision arguments is that the answer to `PIN` is a property of the tree at bind time, not of
the wave spec.

---

## 7. Receipts (command + output)

All produced in `/fast/scratch/hyaku/tameshi-r55/T55W3RevengerBinder/` from
`git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin <fixture>` (toplevel asserted).
The binder copy used for the experiments is the landed file with only the `RES` block replaced by
`RES = {}` (`binder-nop.py`, `binder-nop4.py`); the landed file itself was also run unmodified (r1).

| # | receipt | command (abridged) | output |
|---|---|---|---|
| r1 | `r1-landed-binder-keyerror.stderr` | landed binder, `PIN=133b2ce…` | `line 54 … RES[item['heading']] = int(item['n']) → KeyError: 'n'`, exit 1 |
| r2 | `r2-pin-c0.stdout` | patched binder, `PIN=C0` | `REKEY ## Standing rules start=17 inputs=2497 dropped=0`, `REFRESH rekeyed=1 skipped=17 headings=18`; 591→592 entries |
| r2b | `r2b-second-pass-same-out.stdout` | same OUT again | 592 entries, one entry for the heading |
| r2c | `r2c-second-pass-new-out.stdout` | new OUT | 592 entries (C0-blob reseed), trace path moved |
| r3 | `r3-pin-freeze.stdout` | `PIN=133b2ce…` (post-C0) | digests identical to `PIN=C0` — the freeze pointer is *after* C0 (`git merge-base --is-ancestor 9cf0146 133b2ce` → yes) |
| r4 | `r4-pin-base.stdout` | `PIN=0a2010a` (base) | six differing digests; `input_failures(PIN=BASE) at C0` = 6 `input-drift` |
| r5 | `r5-verdict-laundering.stdout` | fixture commit: prior entry set to `gap-blocking`; reader JSON `findings: []`, md declares a FINDING | `REKEY … reader=T55W3RevengerBinder-probe2`; bound entry `verdict executed-ok`, `minor_gaps 0` |
| r6 | `r6-c0-checkout-headings-missing.stderr` | clone checked out at C0, patched binder | `FileNotFoundError: …/c1/lost-headings-at-c0.json` |
| r7b | `r7b-inside-lane-trace.stdout` | OUT = `.ufo/evidence/round-21/coldread/rekey-r55-9cf0146b94dd/` | canonical trace; `entry_reason strict = trace-missing:…` until committed; trace `argv` = 8 elements |
| r8 | `r8-facts.txt` | digests C0 vs base, DROP union, canonical path | see §4/§5 rows E7, E11 |
| r9 | `r9-pin-C0-at-head.stdout`, `r9-pin-HEAD-at-head.stdout`, `r9-facts.txt` | clone at HEAD `4c04c1d`, heading `### Round-18 gate/probe registry — routed-defect closure` (71 inputs) | `PIN=C0` → `['input-drift:corpus/QUALITY.md','input-drift:tools/registry-check.py','input-drift:tools/registry.json']`; `PIN=HEAD` → `[]` |
| r10 | `r10-pin-C0.stdout`, `r10-pin-HEAD.stdout`, `r10-facts.txt` | same on heading `## Context gate classification…` | `PIN=C0` → `['input-drift:tools/context-capture.py','input-drift:tools/registry.json']`; `PIN=HEAD` → `[]` |
| r11 | `r11-reader-census.txt` | census of live reader JSONs against the 18 headings | 16/18 have a reader; 11 carry ≥1 finding |

## 8. Artifacts opened

- `.ufo/evidence/round-54/integrate/binder.py` (full, 212 lines)
- `.ufo/evidence/round-55/integrate/binder.py` (full) and its diff against round-54
- `.ufo/evidence/round-55/integrate/resolutions.json` (schema: `id/from/finding/decision/evidence`)
- `.ufo/evidence/round-55/freeze.json`, `contract.json` (claims, `frozen_paths`)
- `.ufo/evidence/round-55/c1/lost-headings-at-c0.json` (18 headings; introduced at `4f7a704`)
- `.ufo/evidence/round-21/coldread/ledger.json` (at C0 and at HEAD: 591 entries; `## Standing rules`
  has 8 prior entries)
- `.ufo/evidence/round-21/coldread/measure.py`, `.ufo/evidence/round-18/measure.py`
  (`sectionize`, `canonical_lane_path`, `input_failures`, `inputs_view`, `entry_reason`, section
  credit: `by_sha`, `covered = credited > 0 and not vetoes`)
- `.ufo/evidence/round-21/coldread/rekey-r54-99c3bc88d704/{traces/section-01.json,refresh-receipts.json}`
- `corpus/lessons/round-54.md` (`## The method`), `corpus/lessons/round-55.md` (read for context)
- `.ufo/waves/round-55/{spec-w3.json, w3-dispatch.json}`, `.ufo/waves/round-55/w1/T55W1ExecReKeyDryBind.md`
  + `T55W1ExecReKeyDryBind-receipts/binder-r55.py`
- live reader JSONs in `.ufo/waves/round-55/{w2,w3}/*.json` (census only, read-only)

## 9. What I did not do (bounds)

No lane write outside this file and its receipts dir; no mutating git/jj in the lane; no frozen file
touched; no `rm -rf` on the shared scratch parent (only my own `$S`); no subagent (leaf); no attempt
to run the deciding run or judge a section.
