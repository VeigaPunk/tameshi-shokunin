# T47RevC1Predicate — C1: is the claim the predicate the label?

Seat: leaf reviewer, no dispatch. Lane checkout read-only; only this report was written.
Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, base `0b5b7cd2b2c15d23086e811a0f0348d84261277b`,
freeze `9acfbe21435e1976636a276448dee1d5e7155915` (worktree HEAD at review time `a944eb55d64a`, freeze + one
receipts/spec commit). Scratch: `/tmp/tameshi-r47-T47RevC1Predicate/`. No lane git write, no worktree write, no
mutating `jj`. Fixtures are `mktemp -d` + `git init -q` with `-C "$D"` on every call and
`git -C "$D" rev-parse --show-toplevel == $D` asserted before the first commit; identity passed as `-c user.name=t
-c user.email=t@t` only.

**Tooling:** nothing installed or upgraded (no pacman, no uv, no binary). Used the host `python3`, `git`, `bash`,
`bwrap 0.13.1` only.

**Scratch footprint:** `/tmp/tameshi-r47-T47RevC1Predicate/` peaked at **9.0 GB** (each counter run clones the lane six
times, once per profile). It was deleted at the end of the review; `/tmp` went from 8.7 GB free (94 %) to 17 GB free
(87 %). Nothing of mine remains under `/tmp`.

**Object under review.** `calibration/measure.py` sha256 `c54debb241c0df7fa282f619bb0905472a375ce0b3e5f800edc6f8945daa0f30`;
`calibration/statements.json` sha256 `924102dfbc6135a7d9dabef7b8b2e681a5ce4c42ca72a031ea1f8d5ab9fb2e56`, which equals the
contract's `statements_sha256` and the counter's `STATEMENTS_SHA256` constant (`measure.py:49`) — three copies agree.

---

## 1. Verdict in one line

The claim, the predicate and the receipt label are **the same statement about (line, exit, sha) and about `deps` as a
five-variant observation**, and the label prints every field the target names. They are **not** the same statement in
four places, each of which over-states in the contract or in the frozen docstring and under-states in the code:
`exit` for the 3 `axis` statements (§3.1), a *sorted* deps list (§3.2), `total`'s definition (§3.4), and `deps` read
as hermeticity rather than as "these five variants changed nothing" (§5). One structural defect is larger than any
wording gap: **`sources-registry`'s observation is a function of C3's deliverable**, so C1 is not causally separable
from C3 (§8, F1).

The counter's own selftest is green end to end (`cases=35 failed=0`, `VERDICT: PASS`, exit 0) and the emit path
round-trips (22/22 emitted rows parse, control `CTL_K` prints `total=0 C1_R47_PASS=true`), so the label is reachable
honestly. That selftest has no case that reaches any of F5, F6, F7 or F1/F2 (§10), so its greenness is not evidence
against them.

---

## 2. The three texts, side by side

### 2.1 The contract (`contract.json`, `claims.C1`)

> **statement**: "At REV, for each of the 22 frozen statements, the standing SCORECARD row states exactly the value,
> exit code and tool sha256 prefix that the statement's command prints under the live host profile P0, and a deps
> clause equal to the set of dependences observed by comparing its (line, exit) under the clean full profile P1 with
> P0 (`env`), P1 minus bwrap, minus jj, minus node, and P1 inside a bwrap-bound decoy fleet root (`fleet-root`):
> mismatches + unparsed + unobservable + dep_mismatch + unpinned = 0, the base SCORECARD.md stays a byte prefix, and
> the counter, its statements list (sha256 pinned) and its selftest are committed at REV."
>
> **target**: `C1_R47_PASS=true: self_pin=1 stmts_pin=1 statements=22 unpinned=0 append_only=1 total=0`
>
> **do_nothing_control**: "the unchanged tree at the freeze is the control (every standing row lacks the deps
> clause: `unparsed>0`); the cheapest pass attempt, every row restated with `deps none`, is control CTL_J in
> `control/controls-at-freeze.stdout`: `dep_mismatch>0`"

### 2.2 The frozen predicate (`measure.py:3-30`, docstring)

> "C1_R47_PASS=true iff self_pin=1, stmts_pin=1, statements=22, append_only=1, unpinned=0 and total=0, where
> **total = mismatches + unparsed + unobservable + dep_mismatch** over the 22 frozen statements of statements.json
> … `cap` row claim, in the evidence cell (cell 3): `CMD` -> `PRINTED LINE`, exit N, tool sha256 `12 hex`, deps
> `LIST` … `axis` row claim: the integer in cell 2 plus, in cell 3, tool sha256 `12 hex` and deps `LIST`. A row
> without all parts is `unparsed` … the claim (line, exit, sha / score, sha) must equal what the statement's command
> prints under profile P0 (the live host environment, as round 46 observed it) with the sha256 prefix of the pinned
> tool file at REV, else `mismatch` … **LIST is `none` or a sorted comma list over {bwrap, env, fleet-root, jj,
> node}**; it must equal the OBSERVED dependence set, else `dep_mismatch`. A dependence is observed when the
> statement's (picked line, exit code) under the variant differs from its tuple under the clean full profile P1:
> `env` = P0 differs from P1 (clean env: fresh HOME, LANG=C, LC_ALL=C, TZ=UTC, PATH shim of /usr/bin plus node, jj,
> jq) … `unpinned` counts statements whose statements.json entry has no `sha_file`."

### 2.3 The printed receipt (`measure.py:334-337`)

```
C1_R47[_PARTIAL]: self_pin=%d stmts_pin=%d statements=%d mismatches=%d unparsed=%d unobservable=%d
                  dep_mismatch=%d unpinned=%d append_only=%d total=%d rev=%s C1_R47_PASS=%s
```

Observed for real at the freeze (my probe, `--only sources-registry,depth`, scratch work dir):

```
C1_R47_PARTIAL: self_pin=1 stmts_pin=1 statements=2 mismatches=0 unparsed=2 unobservable=0 dep_mismatch=0
                unpinned=0 append_only=1 total=2 rev=9acfbe21435e1976636a276448dee1d5e7155915 C1_R47_PASS=false
```

### 2.4 Field-by-field: target vs label

| contract target field | printed by the label | same name | same value semantics |
|---|---|---|---|
| `C1_R47_PASS=true` | `C1_R47_PASS=%s` (`true`/`false`, lowercase) | yes | yes (`passed` at `measure.py:329-331`) |
| `self_pin=1` | `self_pin=%d` | yes | yes — `git show REV:measure.py` vs the running file |
| `stmts_pin=1` | `stmts_pin=%d` | yes | yes — `sha256(git show REV:statements.json) == 924102df…` |
| `statements=22` | `statements=%d` | yes | yes for the deciding run; a `--only` probe prints the subset |
| `unpinned=0` | `unpinned=%d` | yes | yes — entries of statements.json without `sha_file` (`:296`) |
| `append_only=1` | `append_only=%d` | yes | yes — `rev_sc.startswith(base_sc)` |
| `total=0` | `total=%d` | yes | **divergent definition** vs the docstring, see §3.4 |

The label carries four extra fields (`mismatches`, `unparsed`, `unobservable`, `dep_mismatch`) that `total` folds in;
the target does not name them, so a reader cannot tell from the target which component failed. Not a defect (the
receipt is a superset), but the target's `total=0` is the only place the components appear in the contract's
objective.

`--only` is guarded twice — `total == 0` **and** `not only` (`measure.py:329-330`) — and the label is suffixed
`_PARTIAL`. A probe can never print `C1_R47_PASS=true`, even when it names all 22 ids. Confirmed by the probe above
(exit 1).

---

## 3. Same statement? Every widening and narrowing

### 3.1 W1 (contract over-states): "exit code" for all 22

The contract says *for each of the 22* the row states "the value, exit code and tool sha256 prefix". `statements.json`
is **19 `cap` + 3 `axis`** (`depth`, `calibration`, `freshness`); an `axis` row is `| Axis | Score | Rule | Commit |
Round |` — cell 2 is an integer score and the parse is `(cells[1], sha)` (`measure.py:132-135`). There is no exit code
in an axis row and none in the axis claim tuple. The docstring knows this ("`line, exit, sha / score, sha`"); the
contract does not. **Effect on the label: none** (the label never mentions exit). Effect on a reader: 3 of 22 rows
are described by a contract sentence that cannot be satisfied by them.

### 3.2 W2 (docstring over-states) + counter accepts an illegal row: "sorted comma list"

`measure.py:19` requires "a **sorted** comma list"; `measure.py:131` canonicalises to
`frozenset(deps.group(1).split(','))` and compares sets — order is never examined. The `STATEMENT` line then prints
`','.join(sorted(claim[1]))` (`:322-326`), so the receipt **re-sorts the declaration and hides the violation**.

Empirical (fixture lane, frozen counter, `measure()` imported from the frozen file): statement `both`
(`sh -c 'command -v node && command -v bwrap'`, observed set `{bwrap,node}`) with the row
`` deps `node,bwrap` `` — unsorted, which the docstring declares illegal:

```
STATEMENT cap/both: … MATCH declared_deps=bwrap,node observed_deps=bwrap,node DEPS-OK
C1_R47: self_pin=1 … dep_mismatch=0 unpinned=0 append_only=1 total=0 … C1_R47_PASS=true   (rc=0)
```

A row the frozen predicate forbids prints `C1_R47_PASS=true`. The contract only says "equal to the *set*", so the
counter implements the contract and the docstring is the wider text. The selftest case named
`T23_unsorted_unknown_dep_name_unparsed` does not cover this: its `Bwrap` fails on the unknown/uppercase name
(`[a-z,-]+`, `:56`), not on order — there is **no case that an unsorted valid list is rejected**, and none can pass,
because the code does not implement the rule. This must be settled pre-data: either the docstring drops "sorted"
(a predicate edit, allowed only before the first deciding run) or `claim_of` compares the raw string.

### 3.3 W3 (contract over-states): the deps comparison is over "(line, exit)" for every statement

`comparable()` (`measure.py:234-239`) returns `obs[:2]` for `cap` and `obs[:1]` **for `axis`**: for the 3 axis
statements the exit code is dropped from the dependence test. Empirical fixture: an axis statement
`sh -c 'echo value=7; command -v node >/dev/null || exit 1'` prints `value=7` with **exit 0 under P1 and exit 1 under
P4** (verified by running the same argv against the P4 shim: `stdout='value=7' exit=1`); the counter prints
`PROFILES axnode: P4=7` and `observed_deps=none DEPS-OK`. A `cap` statement with the identical node test does record
`node`. So the contract's "(line, exit)" is narrowed to "(line)" for 3 of 22 — invisible in the answer, because the
axis claim has no exit to display.

### 3.4 W4 (docstring narrows): the definition of `total`

- contract: `mismatches + unparsed + unobservable + dep_mismatch + unpinned = 0`
- docstring `:7`: `total = mismatches + unparsed + unobservable + dep_mismatch` (unpinned listed separately)
- code `:328`: `total = mism + unparsed + unobs + depm + unpinned`

Fixture with one statement's `sha_file` removed: printed `mismatches=1 unpinned=1 total=2` — the docstring's sum is 1.
(The sha-less statement is also double-counted, since dropping `sha_file` shrinks the observed tuple from 3 to 2 and
the claim still carries 3 parts.) The printed `total` follows the contract and the code, not the docstring — so the
"same sentence" requirement is met against the contract and broken against the predicate text.

### 3.5 N1 (counter narrows, disclosed): "what the command prints" = one regex-picked line, stdout **or stderr**

`pick_line()` (`:141-152`) returns the first match of `stmt['obs']` in `p.stdout + '\n' + p.stderr` (`:217`). Multi-
line output is otherwise uncompared, and a line the command prints on stderr counts as "prints". A row can therefore
be `MATCH` while the rest of the output changed. The docstring's "PRINTED LINE" discloses the single-line rule; the
stderr inclusion is not stated anywhere.

### 3.6 N2 (counter narrows, disclosed): `bwrap` has one extra flag

Contract: `bwrap --bind / / --dev-bind /dev /dev --bind DECOY /home/vgpnk/Projects/shokunin`; code `:212` adds
`--die-with-parent` and the docstring says so. No behavioural difference for an observation; listed for completeness.

### 3.7 N3: `env`'s described profile omits `TMPDIR`

`profile_env()` (`:182-190`) sets `TMPDIR=<work>/<prof>/tmp` for P1..P5; neither the contract nor the docstring names
it. A statement sensitive only to `TMPDIR` is labelled `env` under a caption that says "fresh HOME, LANG, LC_ALL, TZ,
PATH shim".

### 3.8 N4: the decoy stub content is not what the predicate says

Both texts say the decoy holds "only a stub `scripts/sources-census.sh` that exits 7"; `measure.py:274-277` writes
exactly that file, and `--bind DECOY FLEET` makes every other fleet path absent. Consistent; no finding.

---

## 4. Universal words, and the sets the counter does enumerate

| universal / set phrase | where | enumerated by | verified |
|---|---|---|---|
| "for each of the 22 frozen statements" | contract + docstring | `statements.json`, pinned by sha256 | **yes** — 22 entries, no duplicate ids, 19 `cap` + 3 `axis` |
| "tool sha256 prefix" on all 22 | contract `surface` ("all 22 (17 before)") | row parse (`CLAIM_CAP` group 3 / `SHA_RE`) ⇒ a sha-less row is `unparsed` | **yes**, and the base fact "17 before" is exact: 17 of the 22 base rows carry `tool sha256`, 0 carry `deps` (measured with the counter's own `last_rows` on `0b5b7cd…:SCORECARD.md`) |
| "a dependence is observed when …" over 5 named variants | contract + docstring | `VARIANTS` (`:57`) = bwrap, jj, node, fleet-root + `env` | **yes** — five, and only five |
| "`none` or a sorted comma list over {bwrap, env, fleet-root, jj, node}" | docstring `:19` | `frozenset` compare | **`sorted` NOT enumerated** (§3.2); the name set is only enforced negatively (an unknown lowercase name ⇒ `dep_mismatch`, an uppercase name ⇒ `unparsed`) |
| "LIST … must equal the OBSERVED dependence set" | docstring | `claim[1] != observed_deps` (`:319`) | **yes** |
| "mismatches + unparsed + unobservable + dep_mismatch + unpinned = 0" | contract | `:328` | **yes** |
| "the base SCORECARD.md stays a byte prefix" | contract | `:272` | **yes** — one file, one check |
| "statements=22" | target | `len(statements) == n_expected` + `stmts_pin` | **yes** — double-pinned (constant + sha) |
| "every standing row lacks the deps clause" (do-nothing control) | contract | `control/controls-at-freeze.stdout` CTL_I | **yes** — `unparsed=22 total=22 C1_R47_PASS=false`; reproduced by my probe (`unparsed=2` on 2 statements) |
| "every row restated with `deps none` … `dep_mismatch>0`" (CTL_J) | contract | CTL_J receipt | **yes** — `dep_mismatch=5 … total=5 … PASS=false`, with the five offending rows printed |
| "the cheapest pass attempt" is refused | contract | CTL_K positive control prints `total=0 C1_R47_PASS=true` | **yes** — the counter is satisfiable, so a `PASS` is not vacuous |

**No universal clause in the C1 contract is outside the counter's enumeration** except `sorted` (§3.2) and the
`exit` phrase of §3.1. The `surface` sentence's "now carrying a tool sha256 on all 22" is an *after*-state: at the
freeze it is still 17.

**The 22 are 21 distinct commands.** `bounded ANSI-C code_view` and `tally-audit-v3 runner audit` share
`argv`, `cwd` and `sha_file`; only `obs` differs (`^(TALLY_AUDIT_V3_SELFTEST: \d+/\d+ pass)` vs
`^(TALLY_AUDIT_V3_SELFTEST: .*)$`). One of the 22 frozen statements cannot falsify anything the other does not, and
the row for a *code_view* capability is calibrated by the v3 runner's selftest line (F10).

**The emitted artifact round-trips.** All 22 `EMIT_*` lines in `control/emit-observed-pre-freeze.out` were fed back
through `claim_of()` as the rows the L1 would paste: 22/22 parse (0 `None`), both kinds included. So the emit path
cannot produce `unparsed` rows, and CTL_K corroborates it end to end.

---

## 5. Is a dependence set read from five fixed variants a claim about `hermeticity`?

**It is only a claim about those five variants — but the rows will read as universal hermeticity, and the row format
is what makes them read that way.**

- The predicate is scoped: "the set of dependences observed by comparing … under [P1, P1−bwrap, P1−jj, P1−node,
  P1-in-decoy-fleet-root]". Nothing probes the network, `/usr/local` or any other install prefix, the interpreter
  version, the locale beyond `C`, the kernel, the user, the cwd, or a second host.
- The observed sets at the freeze (`CTL_J` receipt) are non-empty for exactly **5 of 22** statements —
  six-leg regression ledger `fleet-root,node`; effective expectation reconciliation `jj`; retained
  invocation-context gate `fleet-root`; hermetic env-differential probe `env,node`; mutation report interop `node`.
  **17 of 22 rows will read `deps `none``** — with no scope marker, in a standing document whose subject is what the
  lane depends on.
- The lane already distinguishes the two ideas in its own artifact: `tools/env-diff.py:7` says *"A classified
  surface is not a proof of universal hermeticity."* The C1 row format discards that qualifier: the deps token is
  `` `([a-z,-]+)` `` (`:54-56`), so a scope marker cannot go inside the backticks.
- **Fix available inside the frozen predicate:** `claim_of` uses `re.search(CLAIM_CAP, evidence)` (`:137`), so prose
  *after* the deps backticks still parses. Rows can read
  ``… deps `none` (five round-47 profiles only)`` and remain `MATCH`. Recommended for all 22 rows before the
  deciding run; it costs nothing and stops the standing row from claiming hermeticity the counter never tested.

---

## 6. Is `P0 differs from P1` well-defined as `env` when P0 contains a path P1 cannot have?

**Well-defined as a diff; not well-defined as a claim about environment variables.** It is also not a function of
REV alone (F2).

(a) **`env` is a catch-all over P1's synthetic profile, not over the environment.** `env` is set whenever the P0
tuple differs from the P1 tuple (`:303-305`) — no attribution of cause. P1 is not the host with variables cleared; it
is a *single-directory* PATH shim built from `/usr/bin` plus exactly three names resolved by `shutil.which`
(`node`, `jj`, `jq`; `:169-174`), with fresh `HOME` and `TMPDIR` and `LANG/LC_ALL/TZ`. P0 is the whole host PATH,
which on this host contains `/home/vgpnk/.local/bin`, `/home/vgpnk/.opencode/bin`, `/home/vgpnk/.local/share/mise/…`,
`/run/user/1000/fnm_multishells/…`, `~/.minimax/bin`, `~/.kimi-code/bin`. **Every tool reachable only through those
directories is invisible to P1 and is therefore recorded as `env`** — a missing-binary path, not an environment
variable. The `bwrap`/`jj`/`node` variants cannot correct the attribution: they are built from the same `/usr/bin`
base and diffed against P1, so they are blind to the same paths.
*Live exposure today: none observed.* The only `env`-labelled statement is `hermetic env-differential probe`, whose
selftest is environment-sensitive by design (`P0=9/9`, `P1=2/9` at the freeze). The finding is about what the row's
`env` will mean to a reader, and about the label's reach: it says "`env`", the counter can only say "P0 ≠ P1".

(b) **`jj`/`node` presence in P1 is decided by the invoking shell, not by the host.** `jj` is not in `/usr/bin`
(`/home/vgpnk/.local/bin/jj`); `node` resolves to `/run/user/1000/fnm_multishells/13812_…/bin/node` (a per-session
fnm path) although `/usr/bin/node` exists. The shim gets them only via `shutil.which` at run time. Demonstrated on
the same REV, same counter bytes, same statements.json, with the *invoking* PATH set to `/usr/bin:/bin`:

```
STATEMENT cap/effective expectation reconciliation: observed=- (exit=1) UNOBSERVABLE … observed_deps=none DEPS-OK
PROFILES …: P0=UNOBSERVABLE P1=UNOBSERVABLE P2=UNOBSERVABLE P3=UNOBSERVABLE P4=UNOBSERVABLE P5=UNOBSERVABLE
C1_R47_PARTIAL: … unobservable=1 total=1 … rev=9acfbe21… C1_R47_PASS=false
```

The `jj` dependence recorded in the committed freeze receipt became `none` (all six profiles collapsed to
`UNOBSERVABLE`, which the comparison treats as equal), and "P1 minus jj" became a no-op because `which('jj')` found
nothing to remove. **So the deps clause is a function of (REV, invoking environment), and the receipt records no
environment** — the counter writes `obs-<id>.stdout` per profile (`:219-221`) and nothing else. The `--emit` pass and
the deciding run must be executed from the same shell, or the emitted rows can flip. Recommend recording `PATH`, the
resolved `which()` paths for bwrap/jj/node/jq, and the P0 environment into the work dir (or into the receipt as
`p0_sha`), so the claim becomes auditable after the fact.

(c) **`env` when the diff direction is reversed** (P0 lacks what P1 has — e.g. the fresh `HOME`/`TMPDIR`): same
catch-all, same non-attribution; `tools/env-diff.py`'s own P1-style profiles are the live example (`P1=2/9 pass`,
because that selftest measures the host-vs-clean delta and inside a clean env there is no delta to find).

---

## 7. Is the contract's `before_state` a value the committed counter prints at the freeze?

**Yes.** `before/c1-at-freeze.stdout` ends
`C1_R47: self_pin=1 stmts_pin=1 statements=22 mismatches=0 unparsed=22 unobservable=0 dep_mismatch=0 unpinned=0
append_only=1 total=22 rev=9acfbe21435e1976636a276448dee1d5e7155915 C1_R47_PASS=false`, i.e. `total=22 > 0` and
`C1_R47_PASS=false` — both halves of the contract's `before_state`, in fields the counter prints, at the freeze rev.
My independent probe at that rev reproduces the same shape and the same `UNPARSED` verdict for both statements it
touched, including `sources-registry`'s `rows=120 … |0|b9b754713c9c` and `depth`'s `9|a7d3f2dd7d47`.

Two caveats: (i) the file landed one commit **after** the freeze (`a944eb5 "round-47: before receipts, deciding
script, falsifiers, wave-1 spec and dispatch"`; the freeze commit `9acfbe2` contains `before/no-harm-at-base.stdout`,
`before/base-freshness.txt`, `before/base-coverage.txt` but **not** `c1-at-freeze.stdout`); (ii) consequently the
deciding run's `FROZEN_UNCHANGED` step (`deciding-run.sh:27-28`) does not cover it — its `FROZEN` list names only
`before/base-freshness.txt` and `before/base-coverage.txt`. The receipt is honest and pre-data, but nothing would
catch a later edit of the very file the before-state rests on (F8).

---

## 8. Causal separability from C2 and C3

**No counter reads another claim's files** — checked, not assumed:
`coverage/measure.py` and `hardening/pool.py` contain zero `SCORECARD` / `calibration` / `statements.json` /
`round-47/calibration` references; `calibration/measure.py` contains zero `hardening` / `coverage` / `pool.json` /
`assimilation` references. The sha256 pins of C1's rows cover round-21 coldread, round-45 freshness, round-46-era
tools and the lane `tools/` — none of the C2 v2 counters (`round-47/hardening/*`), none of the C3 snapshots.

**But C1 is not separable from C3 through its first statement's command.** `sources-registry` runs
`bash .ufo/evidence/kaika-round-1/sources-census-v2.sh`, whose Part A is

```
f=corpus/SOURCES.md; … echo "== A rows"; grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' $f
```

and `pick_line` folds it into the observed string `rows=<N> SOURCES_CENSUS: CLEAN (contract v1 + H4 id-or-path)`.
Verified: `corpus/SOURCES.md` holds **120** registry rows at base *and* at the freeze, and no `S26x` row exists yet
(last row `S260`). C3's deliverable is 3 rows (`S261`, `S263`, `S264`) plus an optional **uncounted** 4th (`S262`,
`extra_row`). Therefore, at any deciding REV that carries C3's rows, this statement prints `rows=123` or `rows=124`,
and if a new row's used-by path is missing (Part A "mined used-by missing") or an id/tier/kind is malformed, it prints
`SOURCES_CENSUS: VIOLATIONS` about a line that no longer matches the `obs` alternation ⇒ C1 `unobservable=1`.

Consequences, in the contract's own terms:

1. C1's `sources-registry` row must be emitted **after** C3's rows are final and at the **same** rev as the deciding
   run, or it is wrong on arrival. The row is a function of C3's landing state, not of the lane's own work.
2. AXES.md requires "each verifiable without the others having landed". For this statement, C1 cannot be verified
   without C3, and a C3 miss (rows not adopted, or adopted with a broken used-by) is scored as a C1 failure —
   `unobservable`, which is in `total`.
3. The optional 4th row moves the value again, and C3's own counter deliberately does not count it — so the number
   C1 must state is partly governed by a C3 detail C3 does not police.

This is the round's most consequential finding for the claim, and it is not fixable by wording: the L1 must either
sequence C1's emit strictly after C3's rows (and re-check the census at the deciding rev), or the report must state
that C1's first row is contingent on C3. Nothing in the frozen predicate prevents the sequencing; `deciding-run.sh`
runs both counters at the same REV, so the ordering risk is entirely in *when the rows are written*.

*(Checked and cleared: the other candidate couplings are inert. C3's rows cannot reach the round-45 freshness
population — `population()` filters `status == 'mined' and id <= MAX_ID` with `MAX_ID = 160`
(`round-45/freshness/measure.py:61,95-97`), so `S261..S264` never enter `population=73`, `fresh=<n>` or the
`freshness` axis score; the no-harm registry floor is `>= 120`, not `== 120`. No other statement tool reads the live
`corpus/SOURCES.md`, `corpus/README.md` or the C3 snapshots at run time — grepped all 18 distinct tool files; their
`corpus/` mentions are comments, fixture paths and spec strings.)*

---

## 9. Findings by severity

**F1 — HIGH — C1's statement #1 measures C3's deliverable; the claims are not causally separable.** Evidence §8:
`corpus/SOURCES.md` rows 120 at base and freeze, 120 + 3(+1) at any C3-carrying rev; `sources-census-v2.sh` Part A
prints that count into C1's observed line. A C3 miss also flips C1 to `unobservable`. Action: emit the C1 rows at the
same rev as, and strictly after, C3's rows; state the contingency in the report.

**F2 — MEDIUM-HIGH — the deps set and the P0 observation are functions of the invoking shell, not of REV, and the
receipt records neither.** Evidence §6(b): same REV / same counter bytes / same statements.json, `PATH=/usr/bin:/bin`
turns `jj` into `none` and the statement into `UNOBSERVABLE`; `jj` lives only in `~/.local/bin`, `node` resolves
through a per-session fnm path. `host_env()` (`:62-66`) is `os.environ` minus `GIT_*`; `build_shim` (`:156-175`) adds
exactly `node`, `jj`, `jq` by `shutil.which`. Action: one shell for emit + decide; record `PATH`, the four `which()`
resolutions and the P0 env in the receipt.

**F3 — MEDIUM — `env` is a catch-all over P0-vs-P1, not an environment-variable claim; P0 necessarily holds paths P1
cannot.** Evidence §6(a): P1's PATH is one `/usr/bin`-derived shim plus three names; the host PATH also carries six
other directories; any tool from them is filed under `env`. Also `TMPDIR` and the absence of every other variable are
folded in without being named. No live misattribution among the 22 today (only `hermetic env-differential probe` is
`env`-labelled, and it is env-sensitive by design) — this is a label-reach defect, so it matters for what the 22
standing rows assert, not yet for a wrong value.

**F4 — MEDIUM — 17 of 22 rows will read `deps `none`` = universal hermeticity, though only five variants were
probed.** Evidence §5; `tools/env-diff.py:7` states the distinction the row format discards; the deps token regex
forbids a scope marker, but `re.search` allows prose after it. Action: append the scope in the evidence cell prose for
every row.

**F5 — MEDIUM — the frozen predicate's `sorted` rule is unimplemented; an illegal row prints `C1_R47_PASS=true`.**
Evidence §3.2 (fixture: unsorted `node,bwrap` ⇒ `DEPS-OK`, `total=0`, `PASS=true`), plus `:131` and the re-sorting
print at `:322`. Pre-data, so resolvable by dropping "sorted" from the docstring or enforcing it; must not survive
into the deciding run as a predicate that the counter contradicts.

**F6 — MEDIUM — the contract's "exit code" universal is false for the 3 axis statements, and the predicate narrows
`(line, exit)` to `(line)` for them.** Evidence §3.1, §3.3 (fixture: axis exit differs under P4, `observed_deps=none`).
Action: correct the contract's sentence for `axis` rows in the round report (the counter is the stricter reader and
fails closed; the contract over-claims).

**F7 — LOW-MEDIUM — `total` is defined two ways: the docstring excludes `unpinned`, the contract and the code include
it.** Evidence §3.4 (fixture: `unpinned=1` ⇒ printed `total=2`, docstring sum 1). The label follows the contract;
the docstring's sentence is wrong, and the docstring is what "the same sentence" is judged against.

**F8 — LOW-MEDIUM — the before-state receipt is not pinned.** `before/c1-at-freeze.stdout` is in `a944eb5`, not in the
freeze; `deciding-run.sh`'s `FROZEN` list covers only `before/base-freshness.txt` and `before/base-coverage.txt`.
Evidence §7. Action: add the three `before/*-at-freeze.stdout` and `before/pool-base.stdout` to `$FROZEN`.

**F9 — LOW — the kill_rule names 3 of the 6 conditions that fail the counter** ("total > 0 or stmts_pin=0 or
append_only=0"), omitting `self_pin=0` and `statements≠22` (both in `passed`, `:329-331`). Behaviour is fail-closed;
only the prose is short.

**F10 — LOW — statement #16 duplicates #15** (`bounded ANSI-C code_view` vs `tally-audit-v3 runner audit`: identical
argv/cwd/sha_file, different `obs`), so 22 statements are 21 observations and the code_view row is calibrated by the
v3 runner's selftest line (§4). Not a false claim; a calibration surface that reads wider than it is.

**F11 — LOW (operability) — the counter prints nothing until all 132 observations resolve** (`measure()` collects
every future before the first print, `:288-300`), and statement timeouts are 2700 s (`six-leg regression ledger`) and
1800 s (three others). My full scratch reproduction at the freeze rev was cut at 1500 s with 128/132 observations on
disk (P0–P3 complete; `bounded ANSI-C code_view` and `tally-audit-v2 runner audit` outstanding in P4/P5), and a
2-statement probe of exactly those two (`--only "bounded ANSI-C code_view,tally-audit-v2 runner audit"` @ freeze) was
still running at 400 s with **no output at all** — the two `tally-audit-{v2,v3}.py --selftest` statements are the long
pole. Not a hang (their declared timeouts are 900 s and 1800 s), and the committed before receipt covers those cells,
but the deciding run needs a ≥45 min allowance and yields no partial receipt if one statement stalls.

---

## 10. Residual risk and verification gaps

- **The counter's own selftest passes:** `--selftest` → `C1_R47_SELFTEST: cases=35 failed=0`, `VERDICT: PASS`,
  exit 0, 88 s (35 cases: T01–T23, T24/T25 × 5 dependences, T26 only-probe-never-passes, T27 only-probe-is-labelled-
  partial). It does **not** cover F5 (no case rejects an unsorted valid deps list — it cannot, the code does not
  implement it), F6 (no axis case whose exit differs under a variant with an unchanged line), F7 (`T21` asserts only
  `unpinned=1`, never the `total` it produces), or F1/F2 (no case varies the invoking PATH or the registry row
  count). A green selftest is therefore not a counter-argument to any finding above. The selftest is host-bound
  (`T24/T25` execute real `bwrap` and the `/usr/bin` shim), so a host without `bwrap` fails it — not a claim defect,
  worth knowing before the deciding run.
- **Not run to completion by this seat:** the full 22-statement deciding measurement (1500 s cap; 2 of 132
  statement-profile observations unverified here, both `tally-audit-*` statements).
- **Every divergence above was reproduced by calling the frozen `measure()` directly on fixture lanes**, not inferred
  from the docstring of a future state.
- **My probes are probes, not verdicts.** The only full-run number I quote is the committed freeze receipt, which I
  reproduced in shape (2/2 statements, same observed tuples, `UNPARSED`, `C1_R47_PARTIAL`).
- **Host-relative claims:** F2/F3 depend on this host's PATH layout (`jj` outside `/usr/bin`, fnm `node`). On a host
  where `jj` is in `/usr/bin`, P3 is a real variant without `which()`; the *finding* (attribution is ambient) is
  unchanged, its instance differs.
- **Not in scope, not verified:** whether the L1's chosen row prose keeps the `append_only` prefix (it will, since
  rows are appended); the C2 and C3 counters' own predicates (separate seats).
- **Recommendation set, pre-data:** (1) sequence the C1 emit after C3's rows and re-run the census at the deciding rev
  (F1); (2) emit and decide from one shell and record the env (F2); (3) add the scope suffix after `deps` in all 22
  rows (F4); (4) drop or enforce "sorted" (F5); (5) fix the contract's axis sentence in the report (F6); (6) fix the
  docstring's `total` (F7); (7) add the before receipts to `$FROZEN` (F8).
