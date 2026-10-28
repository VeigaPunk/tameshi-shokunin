# T54W2Sent03 — sentinel attack: the `read_rev` arm of the frozen C1 counter

Seat T54W2Sent03, round 54 wave 2, L1 TameshiR54a2. Read-only with respect to the
lane: every fixture is a `git clone --shared` under my scratch, every git call names
`-C "$D"`, and nothing outside
`/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-54/w2/` was written.

## Verdict up front

| the two abuses the item names | frozen C1 counter | receipt |
|---|---|---|
| `read_rev` = 12-char prefix of c0 | **REFUSED** (exit 1, `rekeyed=6/7`) | `cur-prefix.stdout` |
| `read_rev` = an unrelated *ancestor* commit | **REFUSED** (exit 1, `rekeyed=6/7`) | `cur-ancestor.stdout` |
| `read_rev` = an unrelated **non-ancestor** commit | **REFUSED** (exit 1, `rekeyed=6/7`) | `cur-unrelated.stdout` |
| the honest control (all seven full 40-hex) | **PASSES** (exit 0, `rekeyed=7/7`) | `cur-positive.stdout` |

The arm that fires is **arm 3 (`arm3-rekey`)**, by the single predicate
`and str(e.get('read_rev')) == c0`. I attribute that rather than asserting it: the
attribution table shows `arm3=False / monitor=True` for each tampered variant, i.e.
the section still credits in arm 2 and it is arm 3's `read_rev` equality alone that
withholds it (`rejection-attribution.txt`).

The claim's letter therefore holds for the abuse the item names. **Two blind spots in
the same arm survived every one of these refusals and do pass the counter**, and I
report them as findings below, because they let a hand-bound re-key reach
`C1_R54_PASS=true` while the thing the claim says is pinned is not pinned.

## Exact bytes

The counter I attacked (operative bytes, sha256 `d7749f84…`, identical in verdict to
the bytes committed at C1 `6a39b387…` — see *instrument drift* below), lines 205–213:

```
        for h in frozen:
            good = [e for e in bound
                    if e.get('heading') == h
                    and str(e.get('read_rev')) == c0
                    and (e.get('wrong_expectations') in (0, '0'))
                    and (e.get('blocking_gaps') in (0, '0'))
                    and r18_mod.entry_reason(lane, rev, e, True) is None]
            if good:
                rekeyed += 1
```

and arm 4, lines 240–243:

```
        for path, d in readers.get(h, []):
            if d.get('cand') == c0 and d.get('section_sha256') == sec['sha256']:
                reader_ok += 1
                break
```

`sec` is `sections.get(h)` from `sectionize(skill_raw)` where `skill_raw = show(lane, rev, 'SKILL.md')`
— **the section at `rev`, never at `c0`.**

## F1 — arm 3's per-heading test is existential: a poisoned entry hides behind a clean twin

`good = [...]` then `if good:` — one bound entry per heading is enough. Two entries
that each satisfy *half* of the requirement together satisfy the arm, and **no single
bound entry then carries both the section's bytes and the full `c0`**.

Fixture `split` (from the passing positive control; only the `## Standing rules`
bound entry is replaced by two):

```
A: read_rev=99c3bc88d704                              sha=61736dce… (the section at REV)
B: read_rev=99c3bc88d704566197783f66b211ee0a830e0330  sha=896c782a… (no section anywhere)
```

Measured predicates (`rejection-attribution.txt`):

```
split          99c3bc88d704  99c3bc88d704                               False     True
split          99c3bc88d704  99c3bc88d704566197783f66b211ee0a830e0330   True      False    sha!=section
```

Counter verdict:

```
C1_R54: rev=768ec20daf9b c0=99c3bc88d704 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
```

`credit` for this section comes from the monitor against entry **A**; `rekeyed` comes
from arm 3 against entry **B**. The claim's wording — *"each of the seven base-lost
sections carries a fresh entry bound under `rekey-r54-<c0>` that credits"* — is
satisfied in aggregate but not by any one entry, which is what a reader of the ledger
would take it to mean. Impact: a ledger can show `rekeyed=7/7` for a heading whose only
correctly-bound entry pins bytes that belong to no section at all.

Smallest remediation: make the per-heading witness single, e.g. require that **every**
bound entry for a frozen heading satisfies all five predicates (`all(...)` over the
heading's bound entries, or reject a heading that has a bound entry failing them), or
bind `sha256` into the arm-3 predicate: accept only an entry whose `e['sha256']` equals
`r18_mod.sectionize(show(lane, c0, 'SKILL.md'))[h]['sha256']`.

## F2 — `c0` is never verified: the counter accepts the round-48 floor as the "read revision"

Arm 3 resolves the directory name to *any* commit with `is_ancestor(lane, c0, rev)`;
arm 4 compares the report's `section_sha256` to the section at **`rev`**. Nothing
anywhere computes a section's bytes at `c0`. So the directory can be named after any
ancestor and every entry can claim `read_rev` = that ancestor.

Fixture `floor`: the re-key directory is renamed `rekey-r54-ef19d8e1e7ba` — after
`ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4`, the frozen round-48 FLOOR commit that the
counter's own `FLOOR` constant names — every bound entry's `read_rev` and every reader
report's `cand` are set to that commit, and the section shas are left exactly as they are.

```
EXPLAIN arm1-precheck exit=0 COLDREAD_PRECHECK floor=ef19d8e1e7ba floor_credited=64 cand=4da26d926869 cand_credited=64 lost=0 ok
EXPLAIN arm2-monitor exit=0 covered=64 score=8
EXPLAIN arm3-rekey dirs=['rekey-r54-ef19d8e1e7ba'] c0=ef19d8e1e7baef7172e8a4fa667daf6d3e29daa4
EXPLAIN arm4-readers 7/7
C1_R54: rev=4da26d926869 c0=ef19d8e1e7ba credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
```

The bytes those reports claim to pin at `c0` are **not** the bytes at that `c0` for 6 of
the 7 frozen headings (`c0-not-read.txt`):

```
  ## Standing rules                                          accepted=61736dcebc2d  sha_at_c0=976cffc97656  equal=False
  ## Mutation-sweep recipe — numbered steps; bounded cold-re accepted=77d88c022646  sha_at_c0=16878309483e  equal=False
  ### The boundaries — what a service run is not             accepted=ff4f61972eec  sha_at_c0=df053a03b9e5  equal=False
  ### Using the ledger                                       accepted=10c6288580f2  sha_at_c0=57ac17ec1a08  equal=False
  ### The operator's runbook — `corpus/knowledge/operator-ru accepted=8801894537fb  sha_at_c0=c246d3743e0a  equal=False
  ### Round-14 historical registry — superseded by round 15  accepted=06a6864fb05f  sha_at_c0=06a6864fb05f  equal=True
  ### Round-26 gate/probe registry — report interop          accepted=cc23587b353f  sha_at_c0=0ef95e1d5867  equal=False
EQUAL_COUNT=1/7  (arm4 compares against the section at REV, never at c0)
```

The same gap lets the wave-1 read commit pass as `c0` (`provenance`, `c0=59c38109bf11`,
`PASS=true`) even though `## Standing rules` has sha `164390276b45…` there and
`61736dcebc2d…` at C1.

This is the one that matters for the frozen wording: C1 claims *"a committed reader
report pins each section's bytes at `<c0>`"*, and the counter that is supposed to prove
it never reads a section at `<c0>`. A `c0` naming any ancestor — including the floor
the round-48 precheck itself uses — yields `C1_R54_PASS=true`.

Smallest remediation: in arm 3, after resolving `c0`, compute
`frozen_at_c0 = {h: sha of section h at c0}` with the same frozen `sectionize` over
`show(lane, c0, 'SKILL.md')` and require the bound entry's `sha256` (and arm 4's
`section_sha256`) to equal it; a `c0` at which a heading does not exist fails the arm
rather than passing on `rev`'s bytes.

## F3 — the ancestry guard does work (negative result, sweep shown)

The same rename against a commit that is **not** an ancestor is refused twice over:

```
EXPLAIN arm3-rekey dirs=['rekey-r54-de28a884cb09'] c0=de28a884cb09833bee5352dded9ffe5c62572f86
C1_R54: rev=366420304453 c0=de28a884cb09 credited=64 lost=0 rekeyed=0/7 readers=0/7 monitor=8/64 unstable=0 total=2 C1_R54_PASS=false
```

`rekeyed=0/7` because `is_ancestor` fails; `readers=0/7` because arm 4 only accepts a
report whose `cand` equals the *resolved* `c0`, and the unresolved one is not a commit
in the lane. That arm is sound for the non-ancestor case; the defect is only that it
does not go on to check the bytes at the ancestor it does accept.

## Instrument drift observed during the seat

The operative `c1/measure.py` changed three times under this seat: the bytes at C1
`99c3bc8` hash `6a39b387…`; the bytes I first attacked (at lane HEAD `8da3539`) hash
`63f5f881…`; the operative bytes now (lane HEAD `077d431`) hash `d7749f84…`. The delta
is arm 4 scanning both waves (amendment 3) plus the arm-3 directory-component fix
(amendment 1) — **neither touches the `read_rev` predicate**, and I re-ran every fixture
against the current bytes with identical verdicts (`cur-*.stdout` vs `c1-*.stdout`).
The one consequence worth flagging: the counter bytes committed **at C1** still carry
the pre-amendment-1 arm 3, which discovers the re-key directory by
`Path(p).name` against a `/traces/` path — that matches nothing, so run against my
positive control the C1-committed bytes give `dirs=[] c0=None rekeyed=0/7 readers=0/7
C1_R54_PASS=false`. Anyone who reproduces the claim with `git show 99c3bc8:…/c1/measure.py`
gets a refusal on a correct tree. The freeze manifest pins the *later* bytes, so this is
a reproduction hazard, not a scoring one.

| counter bytes | sha256 | positive control | attack 1 (prefix) |
|---|---|---|---|
| at C1 `99c3bc8` | `6a39b38770e828aaa7624644169b07aed18f2f26477170c12d85a33799b1efec` | `C1_R54_PASS=false` (`dirs=[]`) | n/a |
| at `8da3539` | `63f5f88147b898ee795dc925a04668d473c1fc845e370947307e3ea141a0b77b` | `PASS=true` | `rekeyed=6/7` refused |
| operative `077d431` | `d7749f8469fbd49b4daaca6eacef89bc1cf48f553702b4f2fe1a7c80d5245812` | `PASS=true` | `rekeyed=6/7` refused |

Receipt for the first row: `c1committed-positive.stdout` (`arm3-rekey dirs=[] c0=None`,
`rekeyed=0/7 readers=0/7`, exit 1) against the same positive fixture that the operative
bytes pass — so the drift is real and not a fixture artifact.

## Artifacts opened

- `.ufo/evidence/round-54/contract.json` (claims, counter, kill rules, 5 amendments)
- `.ufo/evidence/round-54/freeze.json` (10 hashed files; `c1/measure.py` digest)
- `.ufo/evidence/round-54/c1/measure.py` (all 259 lines; operative, at `8da3539` and at `077d431`)
- `.ufo/evidence/round-54/c1/lost-headings-at-base.json`, `lost-headings-at-c0.json`
- `.ufo/evidence/round-18/measure.py` (`sectionize` 209–250, `entry_reason` 513–526,
  `entry_credit_reason` 477–510, `trace_reason` 373–427, `input_reason` 353–359)
- `.ufo/evidence/round-48/quality/coldread-precheck.sh`
- `.ufo/evidence/round-54/integrate/binder.py` (entry/trace construction, 80–200)
- `.ufo/evidence/round-54/control/controls.sh` (CTL_FAB, CTL_LOGINPUT, CTL_POS)
- `.ufo/evidence/round-54/deciding-run.sh`
- `.ufo/evidence/round-21/coldread/ledger.json` (schema of the 568 entries)

## Commands run (abridged; full stdout in the receipts dir)

```
git clone --shared /home/vgpnk/Projects/shokunin/tameshi-shokunin "$S/clone"
git -C "$S/clone" checkout --quiet 99c3bc88d704566197783f66b211ee0a830e0330
git -C "$S/fixtures/<v>" rev-parse --show-toplevel     # asserted == fixture dir
python3 "$S/fixtures/build.py" positive|prefix|ancestor
python3 "$S/fixtures/probe.py" split|provenance
python3 "$S/fixtures/unrelated.py" unrelated|unrelated_dir
python3 "$S/fixtures/duplicate.py"
python3 "$S/fixtures/floorprobe.py"
python3 "$S/code/cur/measure.py" --lane "$S/fixtures/<v>" --rev "$(git -C … rev-parse HEAD)" --work "$S/work/cur-<v>" --explain
```

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
→ exit 0.

Tooling: no installs or upgrades were needed; nothing was added to any PATH directory.

## Receipts

All under `.ufo/waves/round-54/w2/T54W2Sent03-receipts/`:

- `cur-<variant>.stdout` — the operative counter (`d7749f84…`) on each fixture; the ten
  variants are `positive`, `prefix`, `ancestor`, `unrelated`, `unrelated_dir`, `split`,
  `floor`, `provenance`, `duplicate`, plus `c1committed-positive.stdout` for the
  C1-committed bytes.
- `c1-<variant>.stdout` / `.exit` — the same fixtures on the `8da3539` bytes.
- `c0-not-read.txt` — the per-heading table showing arm 4's accepted sha is the section
  at `rev`, never at the claimed `c0` (1/7 equal).
- `rejection-attribution.txt` — per variant, the `read_rev` under test and whether
  arm 3 / the monitor accepts it.
- `predicate-bytes.txt` — the five-predicate `good = [...]` block and arm 4's two-clause
  condition, byte-exact.
- `predicate-attribution.txt`, `tampered-entry-bytes.txt` — earlier per-variant tables.
- `counter-attacked.sha256` — the digest of the counter bytes attacked.
- Fixture drivers, reproduced verbatim from my scratch: `build.py` (`build.py VARIANT`
  for `positive|prefix|ancestor`), `probe.py` (`split|provenance`), `unrelated.py`
  (`unrelated|unrelated_dir`), `duplicate.py`, `floorprobe.py`. Each clones
  `--shared` from the lane, checks out C1, hand-binds the re-key, asserts
  `rev-parse --show-toplevel` is the fixture dir, and commits only inside the fixture.

To reproduce: clone the lane, check out `99c3bc88d704566197783f66b211ee0a830e0330`,
copy the driver you want plus `.ufo/evidence/round-54/c1/measure.py` and
`lost-headings-at-base.json` into a scratch tree, run the driver, then run the counter
with `--lane <fixture> --rev <fixture HEAD> --work <empty dir> --explain` under a
`TMPDIR` that exists.

## Relation to the round's own deciding run

While this seat was finishing, the lane's deciding run wrote
`.ufo/evidence/round-54/after/c1.stdout` at `c210810`, and the operative counter bytes
are unchanged (`d7749f84…`, `read_rev` predicate still at line 208). That run reads:

```
C1_R54: rev=c21081008adb c0=99c3bc88d704 credited=64 lost=0 rekeyed=7/7 readers=7/7 monitor=8/64 unstable=0 total=0 C1_R54_PASS=true
```

So C1 does pass at the real deciding revision. That is exactly why F1 and F2 matter:
the claim passes, but the arms do not establish the two things its wording asserts —
that *one* bound entry carries both the section's bytes and the full `c0` (F1), and
that the pinned bytes are the section's bytes **at the `c0` named** (F2). Neither
finding contradicts the deciding run; both say the deciding run's `true` is weaker
evidence than the claim reads.

## Findings (for the L1)

1. **arm 3 is existential per heading** — a bound entry with the right bytes and a
   12-char `read_rev` plus a bound entry with the full `read_rev` and a sha belonging to
   no section gives `rekeyed=7/7` and `C1_R54_PASS=true`; no single entry is both
   (`split`). Smallest fix: require every bound entry for a frozen heading to pass, or
   bind `e['sha256']` into the arm.
2. **`c0` is never verified against section bytes** — naming the re-key directory after
   any ancestor (the round-48 floor `ef19d8e1e7ba` or the wave-1 commit `59c38109bf11`)
   and pointing `read_rev`/`cand` at it passes with `rekeyed=7/7 readers=7/7`, while the
   accepted section shas differ from the section at that `c0` for 6 of 7 headings
   (`floor`, `provenance`). Smallest fix: recompute the frozen headings at `c0` and
   compare, in both arm 3 and arm 4.
3. **Reproduction hazard** — the counter bytes committed *at C1* (`6a39b387…`) cannot
   discover a re-key directory at all (`dirs=[]`), so reproducing the claim from the
   cited revision refuses a correct tree. The manifest pins the amended bytes, so this
   is a citation problem; the report should cite the freeze-manifest digest, not
   `C1:.ufo/evidence/round-54/c1/measure.py`.
