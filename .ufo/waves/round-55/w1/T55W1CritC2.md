# T55W1CritC2 — attack on the C2 counter's design (round 55, wave 1)

Seat: critic, item "attack the C2 counter's design", axis **operability**.
Lane base `0a2010acd1e92e4e332774050825e21bcfc7e079`; freeze commit `631cd6455e58dce969310b4c0466c3383d9f5108`.
I edited no lane production file and no frozen counter; every tree below is a
`git clone --shared` under `$HYAKU_SCRATCH/tameshi-r55/T55W1CritC2/`, asserted with
`git -C <d> rev-parse --show-toplevel` before any commit.

Two counter byte-sets are in play and I report against both, because the ticket names the first
as *the* frozen set while the second is what the lane is drifting toward:

| set | bytes | sha256 of `c2/measure.py` | state |
|---|---|---|---|
| F (frozen, `631cd645`) | `git show 631cd645:.ufo/evidence/round-55/c2/measure.py` | `9d076812d9c0…` (matches `freeze.json@F`) | committed; 0 amendments |
| W (worktree, live) | `.ufo/evidence/round-55/c2/measure.py` | `0458f632087f…` (matches the *uncommitted* `freeze.json`) | 8 amendments, 9 allocating modes |

Receipts: `.ufo/waves/round-55/w1/T55W1CritC2-receipts/` (cited as `R/<file>`).

---

## Verdict

**The claim C2 measures does not survive.** Two independent, reproducible blockers make
`C2_R55_PASS=true` unreachable at F on *any* tree (F1, F2), and every arm of the counter is
weaker than the prose it is said to certify: I built a tree that prints
`total=0 C2_R55_PASS=true` (F14) while both tools still emit
`setup: RuntimeError:` / `SELFTEST: FAIL (setup error: RuntimeError: …)` for every unusable
`TMPDIR` except the counter's own fixture name.

The prose in `contract.json` ("one stderr line", "the value is named", "one exit class", "stdout
carries no setup error", "the seven cells state the grammar and the eight allocating modes") is
**not** the predicate in the code: of those five properties, only "exit 2" and "a line on stderr"
are measured. The rest are absent (F4–F7) or reduced to a substring paste (F10–F12).

---

## F1 — at F the *usable* arm fails on every tree: the frozen counter cannot reach total=0

F's usable arm takes the exit code from the traced run:

```
# c2-frozen.py:212-216
            if arm == "usable" and alloc:
                rc = trace(argv, clone, env_with(tmpdir), log)
```

`registry-check --selftest` fails **three of its own timeout cases** under `strace -f`
(`timeout-kills-setsid-pipe`, `timeout-kills-setpgid-pipe`), reproducibly:

```
$ for i in 1 2 3; do strace -f -e trace=mkdir,mkdirat -o log python3 tools/registry-check.py --selftest; echo rc=$?; done
strace run1 rc=1 fails=3      SELFTEST_CASE timeout-kills-setsid-pipe  FAIL (exit=1 elapsed=8.554s …)
strace run2 rc=1 fails=3      SELFTEST_CASE timeout-kills-setgid-pipe FAIL (exit=1 elapsed=8.483s …)
strace run3 rc=1 fails=3      SELFTEST_CASE timeout-kills-setsid-pipe  FAIL (exit=1 elapsed=8.542s …)
```
(R/06-registry-check-under-strace.out; the same selftest *without* the tracer is
`SELFTEST: PASS (51 cases)` 5/5 runs.)

Consequence, measured with F's own bytes at base (R/01-frozen-bytes-base-run.stdout):

```
C2_R55: rev=0a2010acd1e9 grammar=6/8 lazy=5/5 empty=13/13 usable=12/13 tmp_mkdirs=0
        docs=0/7 note=0/8 skill=0/1 total=19 C2_R55_PASS=false
```

The committed base receipt at F claims `usable=13/13 … total=18`
(`before/c2.stdout`). **That receipt was not produced by the bytes the manifest hashes**:
same bytes, same rev, different arm result, and the failing arm is the one amendment 4 exists to fix.
This is exactly the round-54 amendment-2 defect re-learned, and amendment 4 is *uncommitted* at F.

## F2 — at F the *note* arm is unreachable for a truthful note

F labels every self-test `"%s --selftest"` (`c2-frozen.py:90`), so the allocating labels include
`bash-witness-study --selftest` — a flag that tool does not accept (it takes the subcommand
`selftest`). The note arm requires every label as a substring:

```
$ python3 - <<'PY'   # frozen labels vs the lane's own (truthful) round-55 note
truthful note, frozen labels matched: 7 /8
  missing: ['bash-witness-study --selftest']
truthful note, amended labels matched: 8 /8
```

So a *correct* note scores 7/8 at F ⇒ `total ≥ 1` at F **regardless of the tree**. F is unsatisfiable
twice over. (W fixes the label — amendment 3 — and the same note scores 8/8; W now has 9 allocating
modes, so note/9.)

## F3 — the freeze gate cannot absorb the amendments as the ticket states it

If the amended counters are committed and `deciding-run.sh` is still passed `FREEZE=631cd645`
(which is what the ticket names), its own gate refuses:

```
$ git diff --quiet 631cd645 HEAD -- <the seven frozen paths>   # HEAD = amended counters committed in a scratch clone
FROZEN_UNCHANGED=0 (deciding-run rc=1)
 .ufo/evidence/round-55/c1/measure.py | 51 ++++++++++++++++++++++---
 .ufo/evidence/round-55/c2/measure.py | 72 ++++++++++++++++++++++++------------
 .ufo/evidence/round-55/contract.json | 48 +++++++++++++++++++++---
 .ufo/evidence/round-55/freeze.json   | 50 ++++++++++++++++++++++---
```

`deciding-run.sh` requires `FROZEN_UNCHANGED=1` and rc=0. The round must **re-cut a freeze commit**
and pass *that* as FREEZE; the ticket's "frozen counter set 631cd645" is stale the moment the
amendments land. (Reported, not fixed — the counters are frozen by instruction.)

## F4 — the grammar arm does not enforce "one line", and never looks at stdout

```
# c2-now.py:200-202  (identical predicate at F, c2-frozen.py:185-187)
ok = rc == 2 and any(GRAMMAR.match(l) for l in err.splitlines()) \
    and "RuntimeError" not in err + out and "Traceback" not in err + out
```

`any(...)` = "at least one stderr line", and stdout is policed only for two literal tokens. A tool
that prints the grammar line **plus two extra stderr lines and two stdout setup lines passes**:

```
===== a3 =====
GRAMMAR repeat-control --selftest       rc=2  stderr_lines=3  grammar_hits=1 stdout_lines=2 PASS
    HIT "repeat-control: could-not-evaluate: cannot create clone scratch under the scratch root: …"
    ERR 'repeat-control: extra stderr line one'
    ERR 'repeat-control: extra stderr line two'
    OUT 'REPEAT_CONTROL: setup_error'
    OUT 'BONUS: stdout also carries a setup error line'
GRAMMAR context-capture --selftest      rc=2  stderr_lines=2  grammar_hits=1 stdout_lines=1 PASS
    OUT 'SELFTEST: FAIL extra stdout setup line'
```
(R/02-grammar-arm-probes.txt, variant `a3`.) The round's own deliverable 1 says *"stdout carries no
setup error"*; that sentence is unmeasured. This matters for the shipped W fix too: W's
`repeat-control` prints `REPEAT_CONTROL: setup_error` on stdout during the class
(`R/…`: `TMPDIR=<unusable> python3 tools/repeat-control.py --selftest` → stdout `REPEAT_CONTROL: setup_error`).

## F5 — the grammar arm does not bind the value: a fabricated value passes

The value group is `'.+'` — any non-empty quoted string. A tool that prints the literal
`'<redacted>'` instead of the operator's `TMPDIR` passes:

```
GRAMMAR repeat-control --selftest       rc=2  stderr_lines=1  grammar_hits=1 stdout_lines=0 PASS
    HIT "repeat-control: could-not-evaluate: … TMPDIR is not a usable directory: '<redacted>' (could-not-evaluate)"
GRAMMAR context-capture --selftest      rc=2  stderr_lines=1  grammar_hits=1 stdout_lines=0 PASS
```
(R/02, variant `a4b`.) So "the value is named" — the property the round-54 falsifier
`CTL_NAMES` was about — is not measured by the round-55 counter.

## F6 — the grammar arm does not bind the tool identity

The prefix is `^[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?:` — any token. A tool may print another tool's
name, or a name that is not a tool at all:

```
GRAMMAR repeat-control --selftest       rc=2  stderr_lines=1  grammar_hits=1 stdout_lines=0 PASS
    HIT "zeta.helper: could-not-evaluate: cannot create clone scratch under the scratch root: …"
```
(R/02, variant `a5`; and the pattern table below: `"a: could-not-evaluate: …" match=True`.)
A caller that keys on the prefix to learn *which* tool refused is reading a field the counter never
checks — which is also the contract's declared blind spot ("whether a caller parses the grammar by
prefix"), now shown to be a hole in the *emitter*, not only in the caller.

## F7 — the grammar is not closed over legal `TMPDIR` values (false negative)

`'.+'` demands single quotes, but `%r` (the natural repr, and what the lane's tools use) switches to
double quotes when the value contains a `'` — legal in POSIX paths. The lane's own corrected tool
then fails the arm:

```
$ TMPDIR="$S/no'such-dir" python3 tools/repeat-control.py --selftest   # worktree tool, rc=2
repeat-control: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: "/fast/…/no'such-dir" (could-not-evaluate)
grammar match on the tool's own correct line: False
```
(R/04-quote-value-line.err.) No arm can see this because the counter only ever plants one fixed
unusable path.

## F8 — the lazy arm means "exited 0", nothing more

```
# c2-now.py:209 / :233
ok = rc == exp            # exp == 0 for all five lazy modes; stdout/stderr are captured and discarded
```

A lazy mode that does nothing passes:

```
$ TMPDIR=<unusable> python3 tools/context-capture.py --check --json     # base
{"exit": 0, … "status": "ok", … }        rc=0
$ TMPDIR=<unusable> python3 tools/context-capture.py --check --json     # tree with `return 0` stubbed in
                                         rc=0
```
The stub prints nothing and does not read the receipt at all; base prints a full verdict document —
both satisfy `rc == 0`. **How to distinguish** (the answer to the assigned question): compare the
lazy mode's `(rc, stdout)` against the same mode under a *usable* `TMPDIR` (byte equality proves the
mode did not depend on the scratch root), or trace the lazy modes for scratch allocation. The
counter does neither, and it never straces the five lazy modes.

## F9 — the empty arm does not test what S278 says; it tests only the exit code

`env_with("")` sets `TMPDIR=""` and the arm asserts `rc == 0` for 13 modes
(`c2-now.py:228-241`). It never observes *where* scratch landed, and the `/tmp` census runs only in
the usable arm. A tool that treats `""` as a path — the exact "silent, wrong scratch root" the note
says the arm exists to prevent — passes:

```
$ strace -f -e trace=mkdir,mkdirat … env TMPDIR= python3 tools/repeat-control.py --selftest
rc=0
SELFTEST: PASS (29 cases)
2051367 mkdir("tameshi-r12-repeat-control-selftest.vly00vxt", 0700) = 0     # <-- in the clone's cwd
```
(R/05-empty-arm-cwd-mkdir.strace.log, R/07-empty-arm-pass.out.) The scratch dir is then removed on
success, so not even a dirty `git status` would betray it. S278 says an empty `TMPDIR` is *skipped by
the resolver*; the tools never call the resolver for that case (`if t:` short-circuits), so the arm
measures the tool's truthiness check, not the resolver. It also leaves `TEMP`/`TMP` from the
counter's own environment unscrubbed, so "the platform default" is ambient.

## F10 — the docs arm is a substring paste; the cells need not state the grammar or any mode

```
# c2-now.py:244-248
cells = [row for row in reg["rows"] if row.get("scratch_root") and any(t in " ".join(row.get("argv", [])) for t in ("tools/%s.py" % t for t in SEVEN))]
docs = sum(1 for row in cells if MARKER in row["scratch_root"])      # MARKER is the *fragment*, not the grammar
```

`MARKER` = `could-not-evaluate: cannot create clone scratch under the scratch root` — no value, no
exit code, no mode list. Two predicate-level probes:

```
current rows: cells,marked = (7, 7)                       # the lane's own cells (503-char prose)
attack rows (7x env-diff, marker only): cells,marked = (7, 7)
```

So (a) seven cells carrying only the fragment pass, and (b) the cell filter counts **any** row whose
argv mentions a seven-tool, so seven rows that all name `tools/env-diff.py` score 7/7 without one
cell describing the other six. The assignment's integration item 2 ("the cells state the grammar and
the eight allocating modes") is unmeasured. `controls.sh`'s own `CTL_SKIP_c2` cannot detect this: it
is designed to fail on the *grammar* arm, so the docs arm has no independent control at all.

## F11 — the note arm is a label list, not a statement

```
# c2-now.py:258-259
note_names = [m for m in allocating if m[0] in note_txt]
note = len(note_names)            # MARKER is never required in the note
```

```
NOTE labels only, NO grammar/marker at all                    labels=9/9 marker=False
NOTE NEGATING note (says the modes do NOT print it) + marker  labels=9/9 marker=True
```
A note that says *"these modes do **not** print `<marker>`"* and lists the nine labels scores 9/9.
The three required contents of deliverable 3 (the grammar line, the eight allocating modes, the five
lazy modes, and the honest "not a shared Python type" note) are not measured — only nine substrings.

## F12 — the skill arm is satisfied by an HTML comment

```
# c2-now.py:260
skill = 1 if MARKER in norm((clone / "SKILL.md").read_text()) else 0
```
```
SKILL marker in an HTML comment at EOF                      skill_arm=1
SKILL marker inside a 'never do this' sentence               skill_arm=1
```
The deliverable's actual obligation — replace the false Standing-rules sentence, in that section,
and re-key the section — is not measured. My cheap tree satisfied it with
`\n<!-- could-not-evaluate: cannot create clone scratch under the scratch root -->\n` appended at EOF.

## F13 — the usable arm's `/tmp` census misses most of what it claims to cover

```
# c2-now.py:136, :145-152
subprocess.run(["strace", "-f", "-e", "trace=mkdir,mkdirat", …])
if "mkdir" in line and '"/tmp' in line: hits += 1
```
One probe process created four things under `/tmp`; the counter's function counted **one**:

```
$ strace -f -e trace=mkdir,mkdirat -o log python3 probe3.py   # absolute mkdir, open() file, chdir+relative mkdir, O_TMPFILE
tmp_mkdirs(counter function) = 1
--- mkdir/mkdirat lines in the trace ---
    1819939 mkdir("/tmp/crit55-absolute-mkdir", 0777) = 0                # counted
    1819939 mkdir("crit55-relative-mkdir", 0777) = 0                     # traced, NOT counted (no "/tmp" in the arg)
--- files created under /tmp by the probe ---
    ['/tmp/crit55-open-file', '/tmp/crit55-absolute-mkdir', '/tmp/crit55-relative-mkdir']   # + an O_TMPFILE inode
```
(R/03-census-probe.strace.log.) Notes on the assigned question: there is no `cloneat` syscall on
Linux (`mkdir`/`mkdirat` are the dir-creating pair and both are traced), so the gap is not the
filter's syscall list for *directories* — it is that (i) file creation (`openat O_CREAT`,
`O_TMPFILE`, `mkstemp`) is invisible, (ii) a relative path after `chdir` is invisible, (iii) only
the nine allocating modes are traced and only in the usable arm (lazy modes and the whole empty arm
are uncensused), and (iv) an **empty** trace log reads as zero hits — only a *missing* log is
flagged (`if not log.exists(): return None`), so a tracer that failed to attach silently scores 0.

## F14 — the cheapest tree that reaches `total=0` without fixing the two tools

`$HYAKU_SCRATCH/tameshi-r55/T55W1CritC2/cheap/tree`, commit `092dd2ff2f41…`, diff vs base:
5 files, **+18/−71**, of which the tool change is **3 lines in each of the two tools**:

```diff
--- a/tools/repeat-control.py        (tools/context-capture.py is the same shape)
+++ b/tools/repeat-control.py
 def main(argv):
+    if argv and argv[0] == "--selftest" and (os.environ.get("TMPDIR") or "").endswith("no-such-tmpdir"):
+        emit_err("repeat-control: could-not-evaluate: cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '<redacted>' (could-not-evaluate)")
+        return 2
     try:
         status = dispatch(argv)
```
plus: seven registry `scratch_root` values replaced by the bare `MARKER` fragment, the note replaced
by the fragment plus nine mode labels, and `<!-- MARKER -->` appended to `SKILL.md`.

What it does **not** do: it does not touch `strict_scratch_root`, does not introduce a class, and
prints a fabricated value. The class is still broken for every other unusable `TMPDIR`:

```
$ TMPDIR="$S/no-such-tmpdir"  python3 tools/repeat-control.py --selftest      # the counter's fixture name
repeat-control: could-not-evaluate: … '<redacted>' (could-not-evaluate)          rc=2   <-- the arm passes
$ TMPDIR="$S/other-missing"   python3 tools/repeat-control.py --selftest
repeat-control: setup: RuntimeError: cannot create clone scratch under the scratch root: …   rc=2
$ TMPDIR="$S/other-missing"   python3 tools/context-capture.py --selftest
SELFTEST: FAIL (setup error: RuntimeError: cannot create clone scratch under the scratch root: …)   rc=2
```

The round's own monitors do not see it: no-harm's `tools-scope` allows exactly the files touched,
and the row names are unchanged:

```
NOHARM tools-scope [M:tools/context-capture.py M:tools/registry.json M:tools/repeat-control.py ] ok
NOHARM registry-row-names-unchanged ok
```

Score, first attempt at commit `092dd2ff2f41` **with `tools/registry-check.py` left at base**
(R/09-cheap-tree-first-score.stdout):

```
EXPLAIN grammar registry-check --rev               rc=2  FAIL
C2_R55: rev=092dd2ff2f41 grammar=8/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0
        docs=7/7 note=9/9 skill=1/1 total=1 C2_R55_PASS=false
```

That single miss is not the cheat failing — it is **F15** (below) surfacing on my tree: W's ninth
allocating mode is `registry-check --rev`, whose *base* handler prints the class in a different
shape. Adding the two-line canonical line to that handler (commit `2527429`, diff vs base now
6 files, **+19/−82**) turns the arm green:

```
$ TMPDIR=<unusable> python3 probe/gp.py cheap/tree "registry-check --rev"
GRAMMAR registry-check --rev           rc=2  stderr_lines=1  grammar_hits=1 stdout_lines=0 PASS
```

Score with that patch, W bytes (`c2-now.py`, sha256 `0458f632087f…`), commit `252742953e0c`
(R/11-cheap-tree-final-score.stdout):

```
C2_R55: rev=252742953e0c grammar=9/9 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0
        docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true
```

**`C2_R55_PASS=true` on a tree where the class is not fixed.** The tree's own arms are clean while
the operator-visible behaviour for every real unusable `TMPDIR` is unchanged (last block above), and
the two monitors that could have noticed stay green. A counter whose green light is reachable this
cheaply does not certify the property the contract states.

## F15 — W's ninth allocating mode is outside the round's stated work set

Amendment 6 adds `registry-check --rev HEAD` as an allocating mode, and the base handler cannot
satisfy the grammar:

```
$ cd <clone at base>; TMPDIR=<unusable> python3 tools/registry-check.py --rev HEAD
REGISTRY_CHECK: could-not-evaluate (cannot create clone scratch under the scratch root: TMPDIR is not a usable directory: '…' (could-not-evaluate))
rc=2                                              # note: parentheses, not "<tool>: … : ", and on stdout
```
The lane's worktree `registry-check.py` already carries the two-line fix, but the round's integration
items name **only** `repeat-control` and `context-capture` (item 1). A seat that implements items
1–6 literally leaves `grammar=8/9 ⇒ total=1 ⇒ C2_R55_PASS=false` at W. Either item 1 gains
`registry-check --rev` or W's denominator is re-stated; the counter's own `contract.json` "before"
text still says "eight allocating modes".

## F16 — the "before" receipt is blank in the worktree and is not reproducible at F

```
$ wc -c tameshi-shokunin/.ufo/evidence/round-55/before/c2.stdout
0 tameshi-shokunin/.ufo/evidence/round-55/before/c2.stdout          # 0 bytes, modified in the worktree
$ git show 631cd645:.ufo/evidence/round-55/before/c2.stdout | wc -l
43                                                                   # the committed receipt
$ git show 631cd645:.ufo/evidence/round-55/before/c2.stdout | tail -1
C2_R55: rev=0a2010acd1e9 grammar=6/8 lazy=5/5 empty=13/13 usable=13/13 tmp_mkdirs=0 docs=0/7 note=0/8 skill=0/1 total=18
```

The committed receipt cites `usable=13/13 total=18`; the bytes the freeze manifest hashes produce
`usable=12/13 total=19` (F1). Separately, the worktree has the receipt truncated to zero bytes and
`contract.json` / `freeze.json` / `c1/measure.py` / `c2/measure.py` modified with 8 amendments while
the named freeze commit has 0 — a live re-freeze. Reported, not fixed.

## F17 — the printed `total` is not a defect count: it can go negative while `bad` is non-empty

```
$ python3 -  # the counter's own docs-arm expression, c2-now.py:244-252
7 marker-only rows naming only env-diff:  (7, 7, {})
9 such rows:                              (9, 9, {'docs': 'expected 7 scratch_root cells, found 9'})
```

`total` adds `(7 - docs)`, `(9 - note)` and `(1 - skill)`, all of which go negative when a document
over-satisfies; and the verdict is `total == 0 and not bad`, so a tree can print
`total=0 C2_R55_PASS=false` (one grammar failure `+1` masked by one surplus docs cell `-1`). The
ticket's C2 target is written as `total=0`; that number is not equivalent to PASS and must not be
quoted as if it were. `bad` is the only real gate.

---

## Answers to the six assigned questions

1. **Is the grammar regex anchored so a tool cannot pass by printing the line anywhere (e.g. stdout)?**
   *Anchored:* yes, and stdout is not searched. `GRAMMAR` is `^…$` and matched per `err.splitlines()`;
   a line printed only to stdout **fails** (`a6`), a line with trailing text **fails**, a line with a
   verdict prefix **fails**, an empty value **fails**. *But* the anchoring buys less than it looks:
   extra stderr lines are allowed (F4), the value is unbound (F5), the prefix is unbound (F6), and
   the quote style is over-specified (F7). "One line" is asserted but never counted.
2. **Does the lazy arm's pass mean anything?** No (F8): the predicate is `rc == 0`, stdout/stderr are
   discarded, and no lazy mode is traced. A stub that prints nothing passes. Distinguish it by
   byte-comparing the lazy mode against its usable-`TMPDIR` run, or by tracing it.
3. **Does the empty arm's `TMPDIR=""` really test what S278 says?** No (F9): it tests the tool's own
   truthiness guard, not the resolver's fall-through (the tools never hand `""` to `tempfile`), and it
   reads only the exit code — a tool that allocates in the working directory still passes.
4. **Is the docs arm satisfiable by pasting the marker without describing the modes?** Yes (F10), and
   more cheaply than the assignment assumes: the marker is a *fragment*, the cell filter accepts any
   row that *mentions* a seven-tool, and neither the exit code nor a single mode id is required. The
   note (F11) and skill (F12) arms are the same kind of paste and can even state the opposite.
5. **Can the usable arm's strace census miss a mkdir (`cloneat`, `openat` with `O_TMPFILE`)?**
   There is no `cloneat` syscall; `mkdir`/`mkdirat` are covered. The census still misses 3 of 4
   `/tmp` creations in one probe (F13): file creation (`openat O_CREAT`, `O_TMPFILE`, `mkstemp`), a
   relative `mkdir` after `chdir("/tmp")` (traced but not counted — the `'"/tmp'` substring test),
   every lazy mode, the whole empty arm, and — worst — an empty/failed trace log, which reads as
   "zero mkdirs".
6. **Cheapest tree that reaches `total=0` without fixing the two tools?** F14: 3 lines per tool keyed
   on the counter's own fixture name, plus marker pastes; `total=0`, while the class is untouched for
   any other unusable `TMPDIR`, and no-harm stays green.

---

## Impacted axes

* **operability (C2's axis)** — primary: the counter that is supposed to certify one parseable line
  accepts a line it cannot attribute, with a value it cannot trust, in multiples, next to stdout
  setup noise, and it certifies documentation it never reads. A lane can pass C2 while the operator
  still gets `RuntimeError` for every real unusable `TMPDIR`.
* **calibration** — secondary: F1 shows the committed base receipt at F (`usable=13/13`, `total=18`)
  is not reproducible from the bytes the freeze manifest hashes (`usable=12/13`, `total=19`), so the
  round's "before" number is a provenance claim, not a measurement — the same class of defect C1 is
  correcting.
* **the round's kill_rule** — at F the kill_rule ("any arm short of its denominator makes
  `C2_R55_PASS=false`") is satisfied for *every* tree, so the claim is not false, it is
  **not evaluable**; a `false` from F carries no information and must not be read as "the work was
  not done".

---

## Smallest safe correction (proposal only — the counters are frozen; I edited nothing)

1. **Re-cut the freeze** so the *committed* counter is the amended one (amendments 1–4 are
   necessary), and pass the new commit as `FREEZE` to `deciding-run.sh`; otherwise F3's
   `FROZEN_UNCHANGED=0` refuses the run. Re-derive `freeze.json` from the committed bytes (the
   worktree `freeze.json` currently matches the worktree files, which is not the same thing).
2. **Randomise the unusable fixture** — `work/"no-such-tmpdir-%s" % secrets.token_hex(4)` — so a
   name-keyed pre-flight cannot pass (F14).
3. **Tighten the grammar arm** to the claim's own words:

```python
def grammar_ok(label, rc, out, err, tmpdir, tool):
    lines = err.splitlines()
    want = ("%s: could-not-evaluate: cannot create clone scratch under the scratch root: "
            "TMPDIR is not a usable directory: %s (could-not-evaluate)" % (tool, tmpdir))
    return rc == 2 and lines == [want] and not out.strip()
```
   (value = the actual `TMPDIR`, rendered without imposing a quote style, so F5 and F7 both close;
   exactly one stderr line and empty stdout, so F4 closes; `tool` = the mode's own tool, so F6 closes).
4. **Lazy arm**: run each lazy mode under both `TMPDIR`s and require `(rc, stdout)` equality; add the
   lazy modes to the `/tmp` census.
5. **Empty arm**: trace it and require every `mkdir`/`mkdirat` path to be absolute and outside the
   clone's working tree (F9); scrub `TEMP`/`TMP` so "platform default" is not ambient.
6. **Docs/note/skill arms**: require the full grammar (not the fragment) and the row's own mode id in
   each cell; require the marker *and* the nine allocating *and* the five lazy labels in the note;
   slice the `## Standing rules` section out of `SKILL.md` and require the marker there plus the
   absence of the round-54 sentence (F10–F12).
7. **Census**: trace `openat` as well, resolve relative paths against the traced cwd, and fail when a
   trace log contains no syscalls at all (F13).

---

## Sweeps that found nothing (so the negative is a sweep, not an omission)

* Grammar anchoring against a verdict prefix, a trailing-suffix line, an empty value, a
  double-quoted value → all `match=False`, as intended (R/02 + pattern table).
* stdout-only emission → grammar arm `FAIL` for both tools (`a6`), i.e. the stream binding is real.
* `registry-check --rev HEAD` (W's ninth allocating mode) does carry the grammar and exits 2 in 75 ms
  under an unusable `TMPDIR` (R/08-registry-check-rev-grammar.err), so W's new denominator is
  satisfiable.
* The docs arm's `len(cells) != 7` guard does reject an inflated cell count (my earlier variant with
  9 cells was refused), so F10 is about *substring* sufficiency, not about count.
* Source census: `scripts/sources-census.sh validate --root … tameshi` → exit 0 (139 rows), at round
  start and at report time.

## Tooling

No install or upgrade was needed; no package manager transaction was run (host pacman is paused by
the operator directive). Tools used: `git 2.5x`, `python3 3.14.8`, `strace 7.2`.

## Scratch

`$HYAKU_SCRATCH/tameshi-r55/T55W1CritC2/` (receipts copied to
`.ufo/waves/round-55/w1/T55W1CritC2-receipts/`). Every fixture and clone is a `git clone --shared`
whose `rev-parse --show-toplevel` was asserted before any commit; no lane file was modified; no
mutating git command was run on the lane.
