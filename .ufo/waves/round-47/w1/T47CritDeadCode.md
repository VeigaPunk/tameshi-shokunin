# T47CritDeadCode — second implementation against T47ExecDeadCode

Seat: critic (leaf, no dispatch). Milestone: attack the dead-code scan.
Target: `.ufo/waves/round-47/w1/T47ExecDeadCode.scan.py` (sha256
`64826c3d2e4f3b68fdd280e2486e9b44569bad27ac6858cef3cc096e6cc35353`, 315 lines) and its report
`.ufo/waves/round-47/w1/T47ExecDeadCode.md` (257 lines), both landed 22:31 while this seat ran.

Bounds respected: read-only on the lane; the only lane write is this report. No git/jj command, no counter
run, no tool installed or upgraded (nothing was needed — `ast`, `tokenize`, `py_compile` are stdlib; pacman
paused and unused). Scratch: `/tmp/tameshi-r47-T47CritDeadCode/` (my scanner `scan2.py`, naive variants
`naive.py`/`naive2.py`, probe `probe.py`, fixtures `fx/`, `fx2/`, `fx3/`, `fx4/`).

Method is deliberately different from the target's block-recursion, so agreement is informative:

1. every file is `py_compile`d to a scratch cache and `compile(..., PyCF_ONLY_AST)`ed before any analysis
   (a file that does not parse is reported, not skipped);
2. class 1 is found by `ast.walk` over `Return`/`Raise`/`Continue`/`Break` plus a parent map, then the
   *parent statement list* is searched by object identity for later siblings — nesting comes from the AST,
   never from line order;
3. class 2 is found by `ast.walk` and cross-checked with a raw-line regex;
4. class 3 is computed twice — `tokenize` NAME tokens (strings/comments invisible, `.name` attribute uses
   counted separately) and a raw-text regex (strings/comments visible) — so the two reference channels are
   separable;
5. an extra class `dead_in_string` parses string constants that are themselves valid Python.

## 1. Agreement on the lane tree — identical findings

51 files (27 `tools/`, 1+4+13+6 under `.ufo/evidence/round-44..47`), 0 compile errors, 934 function defs
(972 def/class nodes).

| class | target | mine (AST) | agreement |
|---|---|---|---|
| after-terminator | 0 | 0 | identical; the same-indent text rule also returns 0 |
| constant-test | 0 | 0 | identical; `^\s*(if\|elif\|while)\s+(False\|0)\s*:` returns 0 |
| unreferenced | 2 (`tally-audit-v2.py:135`, `tally-audit-v3.py:234`) | 2 strict, same two lines | identical |

The wider tree agrees too: `.ufo/evidence` (150 files, 2104 defs) → target 4 findings, mine 4 strict, at the
same file:line (`round-12/BytesReview/probe.py:51`, `round-33/c2/c2-measure.py:43`,
`round-35/c1/c1-measure.py:266`, `round-36/c1/c1-measure-v2.py:283`).

So on real data **there is no location disagreement at all**. The disagreements are in the *decision
procedure*, in what the classes cannot see, and in two sentences of the report. Those follow.

## 2. Every disagreement, on fixtures

My planted corpus (`fx/tools/planted.py` + `naive_probe.py`, one legitimate example of each class plus the
traps the seat item names):

| class | target | mine | difference |
|---|---|---|---|
| after-terminator | 9 | 9 (+1 in a string) | the in-string `return` at `FIXTURE_SOURCE` (inner line 7) is invisible to the target |
| constant-test | 4, anchored on the guard (`66,70,72,74`) | 4, anchored on the dead statement (`67,71,73,75`) | convention only, same branches |
| unreferenced | 9 | 11 | mine adds the unreferenced **class** `Report:58` (target never scans `ClassDef`) and `multiline` (target suppresses it because the word occurs in an unrelated string) |

Their own fixtures agree exactly: `fixture/` 4 / 3 / 6 and `blocks/` 7 / 1 / 2 after anchor normalisation
(`Holder.method`, `async_loop` both reported), and the only row either of us lists and the other does not is
my `cmd_alpha` — the target is right to suppress it (a name string in `COMMANDS`), my bare-name set lists it
with a `string_or_comment_only_refs` entry. The `blocks/` fixture proves handler, `finally`, `try/else`,
`match` case, class-method and `with` bodies are all reached once each — the duplicate-yield defect the
report says it fixed is indeed fixed (7 distinct sites, and the code yields `body`/`orelse`/`finalbody` only).

## 3. False positives found

**(F1) Framework override reported dead — target, reproducible.**
`fx3/tools/override.py`:

```python
import argparse
class UsageParser(argparse.ArgumentParser):
    def error(self, message):
        self.exit(64, 'usage')
```

`python3 T47ExecDeadCode.scan.py fx3/tools` → `[unreferenced] UsageParser.error` (`defs()` gives `key`
`UsageParser.error`; nothing in this file names `error`). It is live: `argparse.ArgumentParser` contains
`self.error(` three times (verified by `inspect.getsource`). This is the docstring's own blind-spot category —
base-class callbacks — and it is not covered: `__dunder__` and decorator registration are, overrides are not.
`tools/bash-witness-study.py:1722` defines exactly this method and is kept out of the report **only because
ten message strings in that file contain the word "error"**. Delete those strings and the target reports a
live override as dead. Enabled-and-live by coincidence is not a rule.

**(F2) Whole-module import masking is documented and printed, but not implemented — target, reproducible.**
Docstring: "an `import mod` of a scanned file marks that module's top-level functions live"; the per-run
caveat prints the same sentence. `collect_imports` only adds the module *stem* to `imported`, and `scan_file`
compares *definition names* and `module.name` keys against that set — nothing can ever match. `fx2/tools/`
(`a.py` with `helper_used_cross_file`, `b.py` doing `import a` and calling `a.helper_used_cross_file(1)`) →
`[unreferenced] a.py:1 helper_used_cross_file`. A false positive on the exact pattern the caveat promises to
handle. Impact on today's tree is zero (the target's own ch. 2 measurement is also vacuous for the same
reason: re-scanning `round-47/calibration` alone cannot differ, because the channel never suppresses
anything), but the caveat is user-visible reassurance that is false.

**(F3) The two false-positive shapes the item names are handled correctly by both scanners.** A `return`
inside a nested function does not make the outer block dead (`fx/tools/planted.py:25-31`: outer statements
not flagged), and a `raise` in a `try` whose `except` falls through does not make the handler or the post-try
code dead (`planted.py:34-40`: only the in-`try` sibling flagged). I also built the failure that produces
them: `naive2.py` walks terminators then flags every statement textually later *within the same function* —
on `planted.py` it flags 15 distinct statements, **7 of them false** (`return x` after a `raise` inside an
`if`, the next `for`/`break` after a `continue`, the handler body and post-try call after a `raise` in
`try`, `finally` body and `return 'b'` after a `return` inside an `if`).

## 4. Misses found

**(M1) In-situ embedded source — the target cannot see it, and neither can any scan of a commit root.**
The round-43 `dead_code_only` survivor is not code in `tools/write-path-census-v3.py`; it is the second
`return` inside the fixture string `FIXTURES['F12_method_two_returns']`, the `ast.Constant` at
`.ufo/evidence/round-43/mutants/measure.py:234-246` (inner line 8). `scan2.py` over `.ufo/evidence` reports
it in situ: `dead_in_string:dead_after_term`, string line 234, inner line 8, terminator at inner line 7.
The target reports 0 on the round-43 root, and its report is honest that it only found the case by
extracting the string to `/tmp/.../known/F12_method_two_returns.py` first (extraction byte-identical, md5
`6be5c04b4dd2c36034c038c55d787f69` for both). Correct conclusion, unavailable capability: nothing in the
delivered scanner proves the case can be found where it lives.

**(M2) Unreferenced classes.** `defs()` yields only functions/methods, so a never-instantiated class is
invisible (`planted.py:58 class Report`, dead in the fixture; 0 in the tree and 0 in the 150-file evidence
tree, so no current debt is hidden). Consistent with the frozen class definition ("functions"), but the debt
list should say so.

**(M3) Classes 1 and 2 inside string constants.** Same channel as M1; `constant-test` inside a fixture
string would be invisible. 0 occurrences in the tree (text regex also 0), so no live impact.

**(M4) Definition-boundary misses shared by both scanners** (measured over the 176 files I scanned; the item's
scope plus `kaika-round-1`): post-`try` code after an unconditional terminator in a handler-less
`try/finally` = **0**; post-loop code after `while True:` without `break` = **0**; code after a
`sys.exit()`/`os._exit()` call in the same block = **0** (57 `sys.exit(` sites exist, none followed by a
same-block statement). So the boundary costs nothing today, but the report names only the `while True` shape
and omits the `try/finally` shape, which is the commoner one.

**(M5) A text search cannot corroborate class 1** — see §6.

## 5. Is `unreferenced` a usable class?

Yes, as an advisory one-shot list; no, as anything else. Numbers:

- yield **2 hits / 934 function defs** in scope (0.21%); both are the same helper, `brace_depth_at`, in two
  tools (`tally-audit-v2.py:135`, `tally-audit-v3.py:234`), byte-identical bodies, no caller, no
  `getattr`/`globals()`/string dispatch (verified: the only code occurrence of the name is the `def`).
  Neither is an entry point, a selftest helper, or a decorator target: both are real dead code, and the
  round-35 record already named it (`.ufo/waves/round-35/w2/AttackPerIndexParse.md:58`, "defined and never
  called"; round-36 re-filed the surviving copy, `W2RevengerV1Docstring.md:49`). Precision 2/2.
- recall parity with an independent method: my token+attribute+text scan finds the same two and no others in
  scope. Nine further defs have no bare-name call (`context-capture.py` `case_dir`/`check_case`/`usage_case`,
  `registry-check.py` `communicate`/`wait`, `trace-inputs.py` `fd_path`/`resolve`/`feed`,
  `write-path-census-v4.py` `method_return`) — I grepped each and every one is live through
  `self.`/`harness.`/`proc.`/`tracer.`/`ctx.cls.` dispatch. So the class is not vacuous, and its precision on this tree
  depends on attribute-name matching, which is type-blind.
- the decision rule is fragile in both directions: one live method (`UsageParser.error`) is protected only by
  the word "error" in unrelated messages; one dead-looking name in my fixture (`multiline`) is suppressed by
  the phrase "after multiline return"; a raw-text reference search misses both `load_copies` hits because
  each is "referenced" by the other file's `def` line. On this tree those channels cost 0 real hits
  (`only_string=1` and that one is live-by-override, `only_docstring=0`), so the list is right — by
  measurement, not by rule.
- the idea's second clause ("flag any tool whose `dead_code_only` count grows") is not delivered and cannot
  be from a single snapshot. There is no stored list to diff against, so the scanner is a debt *snapshot*,
  not the growth monitor idea 3 describes. Two rows is also close to saturation: the growth signal would have
  to come from class 1/2, which are empty across 201 files.

Verdict: usable (0 false positives on the tree, 2/2 against an independent method) but the label must stay
advisory, and deletion of the two rows is safe only after the one-line grep the report already prescribes.

## 6. Claim-by-claim audit of `T47ExecDeadCode.md`

Verified as stated: sha256 and 315 lines; `scanned_files=51 findings=2 after-terminator=0 constant-test=0
unreferenced=2 parse_errors=0`; per-root file counts (27 / 1 / 4 / 13 / 6); exit 0 on a clean dir, exit 2 on a
missing root, `--class` filtering; byte-identical stdout on two runs (determinism); the 150-file evidence run
with its four findings at the quoted lines; `load_copies` at `round-35/c1/c1-measure.py:266` matching the
round-36 seat's O1 note; the two round-45 rows (`import json` is used nowhere in
`round-45/coverage/measure.py`, `results = []` at :145 is never read); the `blocks/` duplicate fix.

Two claims do not hold:

**(C1) The class-1 corroboration is unreproducible as written (calibration).** The report says: "plain-regex
pass … for `(return|raise|continue|break)` followed by a more-indented statement on the next line … zero
hits, matching the scanner." Run literally over the same roots that shape has **256 hits** — every multi-line
`return` is followed by a more-indented continuation line. The only readings that give 0 are (a) a bare
terminator alone on its line followed by a more-indented line, which cannot parse, so the zero is syntactic,
not evidential; or (b) the *same-indent* successor, which is the real class-1 shape and does give 0 — but that
is not the shape the sentence describes. Additional datum: the same-indent text rule returns **124** hits over
those files, and all 124 are the closing `}`/`)`/`]` lines of multi-line terminators, i.e. a text search alone
cannot corroborate this class at all; it needs the AST `end_lineno` boundary. The conclusion (class 1 = 0) is
right — I reached it twice — but the printed evidence for it is not what the document says.

**(C2) "each masking channel was measured, not assumed" is incomplete in the channel that matters most.** The
five channels listed omit attribute-name collision, which is the channel that actually suppresses 9 of the 11
in-scope bare-name-unreferenced defs and 15 of 19 across the evidence tree. I measured it (numbers in §5) and
verified every one of the suppressed defs is genuinely live — so the outcome stands, but the sentence that
claims the audit is complete is not supported by the audit performed.

Minor: the F12 span is cited as `measure.py:236-243`; the `ast.Constant` node is `234-246` (the extracted
bytes are identical, so only the citation is imprecise). The `while True` limit is described in a sentence
that does not parse ("no `break` is unreachable if the loop never ends") and omits the `try/finally` shape.

## 7. Impacted axes and the smallest safe correction

Impacted: **depth** (the list's credibility) and **calibration** (two sentences assert evidence or behaviour
that does not exist). Operability, coverage, C2 and C3 are untouched — no counter was run and no claim is
affected. The hazard is downstream: a wave-2 scribe quoting "each masking channel was measured" or the
printed import caveat into a record would carry the same defect round 43 was refused for (a record asserting
a check that was not performed).

Smallest safe corrections, in order of blast radius:

1. Replace the corroboration sentence with the reproducible version: same-indent successor regex → 0 hits,
   and state that the more-indented shape is 256 continuations, so a text rule needs the AST `end_lineno` to
   be usable at all. (One sentence; removes the only load-bearing false statement about class 1.)
2. Either implement whole-module liveness (`import X` + `X.name` attribute use in another scanned file) or
   delete the sentence from the docstring **and** from the per-run caveat line; do not ship a printed
   guarantee that `collect_imports` cannot honour.
3. Add the attribute-collision channel to the masking list with the measured 9 / 15 and the grep-verified
   live status, and move `UsageParser.error` from "safe by design" to "safe by coincidence" — or add
   override-awareness (skip methods whose name matches a base-class attribute).
4. Fix the F12 citation to `234-246`; keep the extraction, and either say plainly that the in-situ capability
   is absent or add the ~14-line embedded-string walk, which finds it where it lives (`measure.py:234`,
   inner line 8) and costs one false-positive risk to document: a documentation string that happens to be
   valid Python would also be reported.
5. Add the handler-less `try/finally` post-try shape to the documented limits (measured 0), and drop the
   malformed `while True` sentence.

## 8. Commands run (exit codes)

```
python3 /tmp/tameshi-r47-T47CritDeadCode/scan2.py --json mine.json --table            # 0  (51 files, 0/0/11)
python3 /tmp/tameshi-r47-T47CritDeadCode/scan2.py --rounds round-12,... --json mine-all.json  # 0 (176 files, 0/0/19, 1 in-string)
python3 /tmp/tameshi-r47-T47CritDeadCode/probe.py .                                   # 0  (only_string=1 only_doc=0 dead=2; M4 all 0)
python3 .ufo/waves/round-47/w1/T47ExecDeadCode.scan.py tools .ufo/evidence/round-4[4-7]   # 1 (findings: 2)
python3 .ufo/waves/round-47/w1/T47ExecDeadCode.scan.py .ufo/evidence                  # 1 (4 findings, 150 files)
python3 .ufo/waves/round-47/w1/T47ExecDeadCode.scan.py <fixture|blocks|fx2|fx3|fx4>  # 1 each (F1, F2 repros)
python3 .ufo/waves/round-47/w1/T47ExecDeadCode.scan.py /tmp/.../clean                 # 0
python3 .ufo/waves/round-47/w1/T47ExecDeadCode.scan.py /tmp/.../nonexistent           # 2
diff run1.txt run2.txt                                                               # 0  (deterministic)
python3 naive.py <51 files> | wc -l                                                  # 124 (all continuation closers)
python3 naive2.py fx/tools/planted.py                                                # 7 false of 15 flagged
```
