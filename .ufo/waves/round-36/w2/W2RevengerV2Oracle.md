# W2RevengerV2Oracle — v2 counter oracle-separation reverse-engineering

Seat: W2RevengerV2Oracle (leaf, read-only). Wave: Tameshi round 36, v1 policy wave.
Attacked: C1 fixture — `.ufo/evidence/round-36/c1/c1-measure-v2.py` (the frozen v2 counter).

## Question

Does the v2 counter import or exec `tools/tally-audit-v3.py` for its behavioral
oracle (it must compute divergence itself), and is the tool run only as the
object under test?

## Frozen-byte verification (commands + revisions)

```
sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-36/c1/c1-measure-v2.py \
          /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/tally-audit-v3.py \
          /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh
```
- v2 counter `9eb8944c25414da11400dce92afaf047c4874b6bd800bfe15219572e9da8fa53` — matches the frozen pin; all citations below are against exactly these bytes (559 lines).
- tool `6188db16de045f2927df2a0e667bc1539f4acfce5a1ac116e6de3107bf15d354` — matches.
- runner `a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9` — matches `PIN_RUNNER` at v2 line 63.

Lane tip read (read-only): `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin rev-parse HEAD`
→ `fbb01cf46f8437fd1264c1a3acc053c882fa2164` (`fbb01cf` round-36 verifier spot-check (integrator, hyaku): non-author admit/reject).

## Finding 1 — the counter does NOT import or exec the tool for its oracle

**Import surface (c1-measure-v2.py:50-61).** The complete import block is
`argparse, atexit, hashlib, json, os, random, re, shutil, string, subprocess, sys,
tempfile`. Nothing tool-related; no `importlib`, no `__import__`, no `exec(`, no
`eval(`, no `runpy`, no `sys.path` insertion anywhere in the file (full-file grep;
sole positive hit for the exec/import channel sweep is `re.compile` at :204, a
false positive). Every Python `subprocess.run` call site is enumerated below —
there is no `os.system`/`popen`/`check_*` channel at all.

**The tool's only references are metadata, not code (lines 63-67).**
```
63: PIN_RUNNER  = 'a7d3f2dd…'
64: TOOL_PATH   = 'tools/tally-audit-v3.py'
65: TOOL_SHA256 = '6188db16…'  # v3 after A7 (final bytes)
```
`TOOL_PATH`/`TOOL_SHA256` are used in exactly three places, all *materialization
of the object under test*, never as code:
- :446 `tool_bytes = git_show(lane, rev, TOOL_PATH)` — fetch the tool's committed bytes at REV;
- :461-462 `tool_sha = …` / `tool_sha_ok = … tool_sha == TOOL_SHA256` — hash-pin gate;
- :464-467 write those bytes to `tmp/tool.py` for the run below.

The counter never imports, parses, or introspects the tool's source.

**The oracle is the counter's own computation (behavior-oracle section, :126-265).**
- `code_view` :128 — quote-aware shell-comment blanking;
- `tally_block` :165 — brace-depth walk from `run_regression()` to the unique
  `local nlegs=` and its closing depth-0 `}` (ambiguity refused, :178-187);
- `ASSIGN_RE` :204 / `leg_names` :207 — extracts `st_*=$?` leg names;
- `vectors_for` :238 — all-zero vector + all 256 first-byte values + 10 fixed corner vectors;
- `run_block` :211-235 — writes a bash driver that binds `st_*` from the vector and
  `root/auto/KEEP` from the config triple, runs it via `subprocess.run(['bash', path])` :225,
  and collects `(exit, FULL stdout)` tuples per vector;
- `behavior` :252-261 — ground truth = that tuple list under each of the four
  `CONFIGS` triples :75-76;
- `diverge` :264-265 — the counter's own comparison of pristine vs copy maps.

**Ground truth is computed before and independently of the tool (:375-398).**
`copy_beh = behavior(copy_text, bdir)` :376 and `pristine_beh = behavior(runner_text, bdir)`
:377; `div = diverge(pristine_beh, copy_beh)` :386. Only afterwards is the tool run :391.
Validity (the behavioral ground truth) is decided purely by `div`: kill `row['valid'] = bool(div)` :394,
accept `row['valid'] = not div` :397. The tool's outputs enter only the verdict terms:
`row['pass'] = bool(div) and rc == 1 and failed == ['runtime']` :395 and
`row['pass'] = (not div) and rc == 0` :398 — i.e. the tool's rc/failed-check lines are
the *claim under test* evaluated against the counter-computed truth, never the truth itself.

**Design intent is stated in the code (:72-74):**
```
# The tool carries the same four triples; the oracle must not import the object it tests,
# so the two lists are kept in lockstep by hand and by the control receipt.
```
The CONFIGS duplication (:75-76) is the concrete consequence.

**Subprocess inventory (complete):** git plumbing :116, :123, :301, :430, :492, :505, :507;
bash specimen driver :225; tool-under-test :325. Nothing else spawns or loads code.

## Finding 2 — the tool is only run as the object under test

`run_tool` :324-331 is the sole execution path of the tool:
```
324: def run_tool(tool_path, runner_copy, tmp):
325:     p = subprocess.run([sys.executable, tool_path, '--runner', runner_copy],
326:                        capture_output=True, timeout=1800)
327:     out = p.stdout.decode('utf-8', 'replace')
328:     failed = re.findall(r'^CHECK (\w+) FAIL', out, re.M)
330:     … last line starting with 'TALLY_AUDIT:' …
```
It is invoked as a black-box process auditing a specimen copy of the runner
(`--runner rpath`, written at :388-390), and the counter consumes only its exit
code, `CHECK … FAIL` lines, and trailing `TALLY_AUDIT:` line — the tool's
*verdict*. The only callsites are :391 (per-copy scoring) and the scoring entry
points :476 and :522, which pass `tool_file` (the REV-fetched or `--tool`
control bytes at :440-445, :464-467). Consistent with this one-directional role,
`--before` mode (:448-451) merely asserts the tool is absent at REV and scores
nothing — the tool is the treatment, not the oracle.

## Divergences

None. The implemented behavior matches the stated contract ("ground truth is
BEHAVIOR, computed by this counter without using the tool", docstring :19-27) and
the oracle-separation comment (:72-74).

## Confidence

High. Static analysis of the complete 559-line file, byte-verified against the
frozen sha256; negative sweeps covered every dynamic import and process-exec
channel Python offers; the tool's use sites are exhaustively enumerated (3
metadata uses, 1 execution path, 3 scoring callsites).

## Verdict

**CONFIRMED — c1-measure-v2.py computes its behavioral oracle itself (bash-driven
(exit, stdout) tuples over four CONFIGS, compared by its own `diverge`), never
imports or execs `tools/tally-audit-v3.py` for ground truth, and executes the
tool only as the black-box object under test (`run_tool`, :324-331 → :391/:476/:522).**

No tools were installed or upgraded (none needed).
