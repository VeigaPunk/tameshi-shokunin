# ConnectorSibling — sibling prior art for `write-path-census-v3.py`

Read-only. No sibling byte was edited; the only write is this file. No tool was
installed or upgraded. Counters were **not** run against the tip; the one
`--rev work` check named below is the L1's, labelled pre-run.

## 1. Evidence — who already does this, exactly

Two tools in **kotodama-shokunin** already do what `write-path-census-v3.py`
does: parse Python with `ast` and resolve a **write destination held in a
variable through assignment**.

| # | Path (lane-prefixed) | sha256 | Landed |
|---|---|---|---|
| A | `kotodama-shokunin/tools/harness/receipt_guard_adoption.py` | `5858abcd0261e8176ebb285db6d80a7c36185d9a12895b4b43b75710db036544` | 4a7aede 2026-10-19 (kotodama round 34) |
| B | `kotodama-shokunin/tools/harness/round_runner_conformance.py` | `a9b2fe017d8c9af0d202c29ae6f2baf86a7b3e925410179969145a7e0a0fdca3` | ac47c78 2026-10-19 (kotodama round 41) |

kotodama HEAD read: `3e59d1d63a4d95a9db041a9b1e67c6fc497413bd`.

**A — assignment-folded destination resolver.**
`receipt_guard_adoption.py:139` `class Resolver`; `:151` `collect()` walks
`ast.Assign`/`AnnAssign` and stores `self.consts[name] = (ast.unparse(...), value)`
at `:165`; `:175` `resolve()` folds `Constant`, `JoinedStr`, `BinOp` (`+`, `/`),
`Attribute` (`parent`/`parents`), `Subscript` `parents[N]` and `Call`
(`Path(...)`, `os.path.join`, `str`, `repr`) to depth 6 (`:151`, `:163`).
Write forms at `:66-70` — `write_text`, `write_bytes`, `open`
(`WRITE_MODES`), `os.replace`, `os.rename`, `shutil.move`, `Path.replace` —
resolved and recorded at `:429` `write_sites()` / `:468-471`
(`"resolved": resolved, "resolution": how`). Selftest `:1080`, fixtures `:867-1046`
include exactly the v3 shape: `temporary = ROOT / ".scratch/fixture-48.json"`
then `os.replace(temporary, ROOT / OUTPUT)` (`:1010-1014`).

**B — richer than v3 on every axis but one.**
`round_runner_conformance.py:34` `_resolve(node, constants, runner_path, depth=8)`;
`:103` `_constants()` runs a **5-pass fixpoint** over assignments (`:105-120`), so a
forward-declared constant resolves; it also folds `__file__` (`:39-41`),
`parents[N]` (`:73-80`), `with_name` / `joinpath` / `os.path.join` (`:86-99`).
Write sites at `:268` `_write_sites()`; destination resolution at `:283-288`
(`os.replace`, `os.rename`, `shutil.move`, `Path.open`, `open`, `write_text`,
`write_bytes`), plus a same-line literal fallback at `:291-292` and a guard
dominance check at `:298`.

**Near misses, named so they are not mistaken for hits.**

- `tsukuroi-shokunin/tools/check-recheck-commands.py:151,187,228,242` — a
  hand-rolled, quote-aware **Bash lexer** (`segments` / `words` / `command_word` /
  `simple_commands`) that skips assignment prefixes and wrapper words to find the
  command word. Not an AST, and it resolves no destination.
- `mado-shokunin/tools/mado-tripwire.py:395` — `shlex.shlex(line, posix=True,
  punctuation_chars=";&|()<>")`; the file documents the gap itself at `:123`
  (`/unparsed`) and `:126` ("shlex is not bash"). No AST.
- `souji-shokunin/tools/souji-seat-audit.py:270-273` — `shlex.shlex` over the tail
  of an `edit` call, `destination = next(lexer, None)`: it *does* resolve a write
  destination out of a Bash-form command, but by token position, with no AST and
  no assignment environment.
- `kaidoku-shokunin/tools/round-33/disk-command-audit.py:31-33` — the honest
  counter-example: lexical regex, and its docstring states that variables, aliases
  and command substitution are **not** resolved.
- Python-AST tools with no write destination: `tsukuroi-shokunin/tools/probe-child-env-allowlist-r33.py:503-525`
  (assignment env, but for `os.environ` allowlists), `tsukuroi-shokunin/tools/check-revision-binding.py:287-291`,
  `kaidoku-shokunin/tools/round-34/elf-version-needs.py:697-702`,
  `souji-shokunin/tools/cand-s16-cert.py:230-251`.

**No sibling parses Bash with an AST.** Fleet-wide sweep of `*/tools` and
`*/scripts` for `bashlex` / `tree-sitter-bash` / `shfmt` returns nothing; the four
Bash-facing tools above are lexers. A true Bash AST exists in this fleet only as a
*note*: `kotodama-shokunin/.ufo/waves/round-67/w1/ConnectorPriorArt.md:18-19`
classifies A and B, and tameshi already recorded B once at
`.ufo/waves/round-32/w1/ConnectorOverlap.md:20`.

## 2. Does `tools/write-path-census-v3.py` duplicate one?

**Yes — functionally, and it is the weaker of the two.** The committed tool's
sha256 is `095924a7a165be96e69ff9dad67d3e513d23ba6737c35a0537f898482eef0279`,
which matches the contract pin, so this comparison is against the frozen bytes.

- `tools/write-path-census-v3.py:58` `_resolve` and `:142` `_bind` are a subset of
  B's `_resolve`/`_constants`: v3 is `MAX_DEPTH = 4` (`:43`) against B's depth 8;
  v3 resolves assignments in one forward statement walk (`_walk_stmts`), while B
  iterates a fixpoint five times, so v3 misses a destination bound after its use;
  v3 has no `__file__`, no `with_name`, no `joinpath`.
- v3's write table (`:112-140`) is a subset of A's (`:66-70`, `:429-471`) and B's
  (`:268-296`) **except** `os.symlink` (`:135-137`), which neither sibling recognises.
- Not a byte copy: different architecture (per-statement env vs whole-tree
  constants), no shared helper, no import. It is a one-week-later reimplementation
  of a capability that already existed in the fleet.

The genuine net-new content of v3 is therefore narrow and should be stated as
such: (i) the `os.symlink` destination, (ii) the `EXPECTED_RE` / `SCRATCH_MARKERS`
classification (`:32-42`), (iii) scratch tracing **through** the assignment chain
(`_resolve` returns `trace`, `:58-60`), which neither sibling does.

## 3. Would absorbing it violate PROVINCE.md?

**Copying the sibling code would. Citing it would not — and is what the province
actually asks for.**

- `PROVINCE.md:44` — "**Adjacent** — report, never absorb: every sibling gate's
  code and product clauses (owner lane)". Both A and B are kotodama's own gates.
- `PROVINCE.md:13-14` — "Never edits a sibling's gate code (read-only probes;
  recommendations travel in round reports)."
- `PROVINCE.md:20` — "Out of province → report, never absorb."

So: lifting `Resolver`/`_resolve` into `tools/write-path-census-v3.py` is out of
province, and so is any edit to A or B. Conversely `PROVINCE.md:7-9` makes "the
fleet's existing gates as primary surfaces" **Core** — reading A and B and citing
them is in-province.

One more constraint lands here: `PROVINCE.md:14-16` admits a pattern "from
evidence in TWO independent lanes before it is claimed general". A and B are the
same lane and share an author lineage, so they count as **one** independent lane.
C2's `declared_scope_limit` already refuses universality, so nothing is broken;
the claim must simply not drift into "the fleet's write-path census now resolves
variables".

## 4. Proposed move (one, bounded)

Append a prior-art paragraph to the round-41 report/lesson — **not** to
`contract.json`, **not** to any sibling — that:

1. names A and B with lane-prefixed paths and the sha256 pins above;
2. restates C2 as *in-lane* capability acquisition, with v3's net-new content
   limited to `os.symlink` + expected/scratch classification + assignment-traced
   scratch, and its resolver declared weaker (depth 4 vs 8, no fixpoint, no
   `__file__`);
3. records A and B as one lane's evidence, so the two-lane admission rule is not
   silently satisfied.

No tool change is required or proposed; the contract's predicate, pins and
`declared_scope_limit` stay untouched.

## 5. Risks

- **m8 is the live risk, and it is mechanical.** `calibration/measure.py:46-51`
  tokenises only backticked paths starting `corpus/`, `tools/`,
  `.ufo/evidence/round-41/`, `.ufo/waves/round-41/` (plus root files at `:52-59`).
  A backticked `` `tools/harness/round_runner_conformance.py` `` in a round-41
  record is lane-relative in *tameshi* and does not resolve → m8=1. Always write
  `kotodama-shokunin/tools/harness/...` (or the absolute path); neither form is
  tokenised, so the citation cannot become a calibration miss.
- **Framing risk.** Calling v3 a "capability acquisition" without the in-lane
  qualifier reads as a fleet-level claim on a single lane's evidence, which is the
  exact defect `PROVINCE.md:14-16` guards.
- **Not a risk:** C2's predicate. It never mentions the fleet and declares its own
  scope limit, so the prior art does not falsify it.

## 6. Verification the L1 should run

- `sha256sum kotodama-shokunin/tools/harness/receipt_guard_adoption.py` and
  `.../round_runner_conformance.py` — expect `5858abcd…` and `a9b2fe01…` above.
- After the append, as a **pre-run** check only:
  `python3 .ufo/evidence/round-41/calibration/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev work`
  — m8 must stay 0; label it pre-run, never as the measurement.
- `grep -c 'kotodama-shokunin/tools/harness' corpus/lessons/round-41.md` — the
  citation must carry the lane prefix (≥1), and
  `grep -c '`tools/harness/' corpus/lessons/round-41.md` must be 0.
