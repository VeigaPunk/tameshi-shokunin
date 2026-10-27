# T53W1CritClaims — wave-1 critic: attacks on the frozen C1/C2 claims

Seat: T53W1CritClaims (critic, wave 1 of 2). Item: attack both claims as declared;
for each attack answer *would it pass the frozen counters — yes/no + the exact bytes
you'd plant*, with scratch fixtures under the seat dir only.

- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
- Freeze under attack: `e62d99711a0dd5d92b83acb96dd53ff22b31cb75` (amendments 1–5)
- Content commit C*: `a41195dfc13a73958e4c5228ec196b28d03ded03`
- Deciding host Python: `Python 3.14.8` (only `/usr/bin/python3.14` exists; `python3` → 3.14.8)
- Tools used: system `git`, `python3.14.8`, coreutils only. **No tools installed or upgraded.**
- Scratch: `/fast/scratch/hyaku/tameshi-r53/w1/T53W1CritClaims` (deleted on exit, per directive).

## Verdict summary

| # | Attack | Passes the frozen counters? | Status |
|---|--------|------------------------------|--------|
| C1-A | Re-key entry fabricated without fresh readers (trace self-forgery) | **YES** — counter is structurally blind | declared `cannot_see`; backstop gap in wave-2 roster |
| C1-B | Precheck green while a section is semantically stale | **YES** — input-keyed credit; SKILL.md is an ignored input | demonstrated live at C* |
| C1-C | 30-heading amendment weakens round-52 routing | predicate bytes unchanged; **two provenance defects** in the evidence trail | fixable; correction named |
| C2-A | TMPDIR redirection actually isolates | **NO** — silent fallback to real `/tmp` when TMPDIR is set-but-unusable or unset | **live falsifier at C*** |
| C2-B | Host ignores TMPDIR | this host **is** such a host; the frozen CR47 arm fails here | same falsifier |
| C2-C | Doc check misses an /tmp form | **YES** — 4 stale post-fix `/tmp` doc rows in SKILL.md pass `docs=ok` | concrete bytes below |

---

## C2-A/C2-B (decisive, reported first): the frozen C2 counter FAILS at C* on the deciding host

### Evidence

Ran the frozen counter bytes (hash-verified against `freeze.json`,
`1942cd8f9850727066439d317acaf5eb0a8e44458b0355ea4dceaf90e8c82c27`, identical at
e62d997 / a41195d / ace79e3 and in the working tree):

```
$ python3 .ufo/evidence/round-53/c2/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin \
    --rev a41195dfc13a73958e4c5228ec196b28d03ded03 --work $S/c2work --explain
C2_R53: rev=a41195dfc13a tmp_hits=0 registry_selftest=[rc=0 SELFTEST: PASS (51 cases)] envdiff_selftest=[rc=0 ENVDIFF_SELFTEST: 9/9 pass] cr47=rc=0 docs=ok total=2 C2_R53_PASS=false
PROBLEM cr47-zero-exit
PROBLEM cr47-no-scratch-message
```

Root cause — Python 3.14.8 `tempfile.gettempdir()` **silently falls back** instead of
raising when `TMPDIR` is set-but-unusable:

```
$ python3 -c 'import tempfile,os; os.environ["TMPDIR"]="/fast/.../c2work/missing-dir"; print(tempfile.gettempdir())'
/tmp
$ python3 -c 'import tempfile,os; os.environ["TMPDIR"]=""; print(tempfile.gettempdir())'
/tmp        # empty TMPDIR
$ python3 -c 'import tempfile,os; import os; del os.environ["TMPDIR"]; print(tempfile.gettempdir())'
/tmp        # unset TMPDIR
```

`registry-check.py --selftest` (C* bytes) opens with
`scratch = tempfile.mkdtemp(prefix="tameshi-r17-registry-check-selftest.", dir=tempfile.gettempdir())`
with no guard, so with a bad TMPDIR the fixtures land in **real `/tmp`** and the run passes:

```
$ env TMPDIR=$S/manual/no-such-dir python3 $S/manual/registry-check.py --selftest
rc=0 ; last line: SELFTEST: PASS (51 cases) ; 'cannot create' occurrences: 0
$ env TMPDIR=<read-only dir> python3 $S/manual/registry-check.py --selftest
rc=0 ; SELFTEST: PASS (51 cases)
```

I demonstrated the leak itself: a probe `mkdtemp(dir=gettempdir())` with a missing TMPDIR
**created a directory in real `/tmp`** (`/tmp/probe-xymlzr6t`; removed after capture).

Consequences, stated plainly:

1. **C2 cannot print `C2_R53_PASS=true` at any measured revision whose
   `tools/registry-check.py` equals the C* bytes, on this host.** The CR47 arm
   (`c2/measure.py` lines 106–121) requires rc≠0 *and* the message
   `cannot create (clone )?scratch` with TMPDIR naming a nonexistent directory;
   both fail here. This was visible since phase A: the committed
   `control/controls.stdout` line `CTL_C2_BASE ... cr47=rc=0 docs=stale-patterns=4 total=4`
   shows the symptom at BASE — masked then by the overall expected=false verdict,
   fatal at the post-fix candidate where tmp_hits=0 and docs=ok leave the CR47 arm
   as the sole blocker.
2. Wave-2 item `T53W2RevC2Counter (e)` (`TMPDIR=<read-only dir>`) fails identically here.
3. "TMPDIR redirection isolates a run" is **false in the fallback case** on the deciding
   host — the selftests happily write to real `/tmp`, which is itself against the
   host scratch directive (`/tmp` only for files under 50 MB).

What still works: with a **valid** TMPDIR, isolation holds. Verified for env-diff:
`env TMPDIR=$S/ev python3 env-diff.py --selftest` → rc=0, and
`find $S/ev -maxdepth 2` shows the sandbox root under TMPDIR with **no**
`/tmp/tameshi-r21-envdiff.*` created.

### Smallest safe correction (does not touch any frozen byte; `tools/` is not in the FROZEN set)

The L1's integration commit (seats may not edit `tools/`) should repair
`tools/registry-check.py` so an explicitly-set-but-unusable TMPDIR is
could-not-evaluate *before* `gettempdir()` can fall back. Exact bytes to insert as the
first statement of `selftest()` (and the same guard at the top of `clone_lane_at_rev`,
whose `except OSError` around `mkdtemp` never fires because the fallback happens first):

```python
    _td = os.environ.get("TMPDIR")
    if _td and (not os.path.isdir(_td) or not os.access(_td, os.W_OK | os.X_OK)):
        raise RuntimeError(
            f"cannot create clone scratch under the scratch root: TMPDIR unusable: {_td}"
        )
```

Uncaught `RuntimeError` → exit 1, stderr names "cannot create clone scratch", no
`REGISTRY_CHECK` verdict line — exactly what the frozen CR47 arm greps for. Mirror the
guard in `tools/env-diff.py::execute()` for symmetry (the predicate names only
registry-check for CR47, but w2 item (e) plus the scratch directive argue for both).
Then re-run the frozen counter: all four arms pass. Disclose the extra fix-pass commit
in LOG/lesson — the C2 "before" story (`dir=` hardcodes at registry-check.py:766,
env-diff.py:61) remains accurate.

---

## C1-A: trace self-forgery — a re-key entry fabricated with no fresh readers passes the frozen counter

### Would it pass? YES.

Read of `c1/measure.py` (frozen, hash `067c1685…` verified at e62d997/a41195d/ace79e3)
plus the round-48 precheck it wraps and the round-21/round-18 monitors it invokes. The
counter checks, and only checks:

1. precheck green: round-21 coldread measure credits 64/64 at REV — credit is
   **input-keyed** (round-18 measure docstring, "Credit rule (v2, fail-closed)" steps 3–5):
   `commands_executed_count>0`, ≥1 committed trace, every recorded `input` a blob at REV
   with matching sha256, traces of schema `tameshi-trace-inputs-v1` whose inputs ⊆ entry
   inputs with equal shas, no live-lane reads;
2. unique `rekey-r53-<c0>` dir at REV, `c0` an ancestor of REV;
3. per frozen heading: ≥1 ledger entry with traces under the rekey dir, `read_rev`
   startswith c0, `wrong_expectations==0`, `blocking_gaps==0`, each trace a blob at REV;
4. per frozen heading: ≥1 committed `*Read*.json` under `.ufo/waves/round-53/` with
   matching `heading`, `cand[:12]==rev[:12]` or `cand.startswith(c0)`, and
   `section_sha256` equal to the frozen round-18 `sectionize` output at REV.

Nothing checks: who authored the trace blobs or reader JSONs; that reader `.md` files
exist (`rekey.py` checks quotes-in-md, but a forger bypasses `rekey.py`); seat identity;
finding counts; trace *provenance*. All checked values are computable by the integrator
alone (shas are public; sectionize is importable).

### Exact bytes to plant (at the measured revision, all inside the L1's own integration commit)

1. `.ufo/evidence/round-21/coldread/rekey-r53-a41195dfc13a/traces/section-NN.json`
   (one per frozen heading), any valid blob, e.g.:

```json
{"schema": "tameshi-trace-inputs-v1",
 "argv": ["python3", "rekey.py"], "cwd": ".",
 "inputs": {"tools/registry-check.py": "<sha256 at C0 of the cited input set>",
            "tools/registry.json": "<sha256 at C0>"}},
```

2. Appended ledger entries, one per heading:

```json
{"heading": "## Standing rules", "class": "record", "verdict": "verified-record",
 "commands_executed_count": 1, "read_rev": "a41195dfc13a73958e4c5228ec196b28d03ded03",
 "inputs": {"tools/registry-check.py": "<sha256 at REV>", "tools/registry.json": "<sha256 at REV>"},
 "traces": [".ufo/evidence/round-21/coldread/rekey-r53-a41195dfc13a/traces/section-07.json"],
 "wrong_expectations": 0, "blocking_gaps": 0, "skill_sha256": "<sha256 of SKILL.md at REV>"}
```

3. `.ufo/waves/round-53/w1/T53W1Read07.json`:

```json
{"heading": "## Standing rules", "cand": "a41195dfc13a73958e4c5228ec196b28d03ded03",
 "section_sha256": "<frozen sectionize sha at REV>", "findings": []}
```

The precheck then credits all 64 sections at REV (the forged entries verify input shas
at REV; the integrator's evidence commit does not touch the cited inputs), the rekey arm
finds 30/30, the reader arm finds 30/30 → `C1_R53_PASS=true`. **No fresh reader involved
at any step.**

### Backstops and their limits

This blind spot is declared (`contract.json` C1 `cannot_see`: "whether a fresh reader
finding is semantically fair… the non-author closure attack this"). Within the lane,
wave-2 partially covers it — but note the gap: `T53W2RevReadersA–E` recompute shas and
quote byte-exactness, which a forger passes trivially (same sha); `T53W2MutLedger`
mutates, it does not check authorship; `T53W2CritSemantic` reads 6 sections. **No
wave-2 seat performs a non-author admit/reject on reader-file authorship** (rounds
51–52 had explicit "verifier spot-check (integrator, hyaku): non-author admit/reject"
commits `c1d49d7`/`ef19d8e`; round-53 `spec-w2.json` has none). Smallest safe
correction: add such a seat (or have the hyaku layer run the spot-check) before closure;
do not touch the frozen counter.

## C1-B: precheck green while a section is semantically stale — YES, structurally, with a live instance

The credit rule never inspects section *text*: SKILL.md is an explicit ignored input
(round-21 measure binds `IGNORED_INPUTS |= {LEDGER}` and round-18 step 4 ignores
"SKILL.md and both the round-17 and round-18 ledger paths"). So any semantic staleness
introduced by editing SKILL.md alone (or by the world drifting under an unchanged
citation set) leaves credit untouched; the re-key then mints fresh credit keyed to
whatever inputs the old entry cited (`rekey.py` reuses the prior citation set, refreshed
at C0 — `cannot_see`: "whether the recorded inputs are the semantically right citation
set").

Live instance at C*, evidenced by running the frozen round-21 monitor at C*
(`$HYAKU_SCRATCH/.../r21-at-Cstar.json`):

```
{"credited": true, "heading": "## Seventh recorded case and full-page cold-read — round 16",
 "reason": "credited", "start": 1761, "vetoed": false}
```

That section's body contains an imperative /tmp-scratch recipe (SKILL.md at C*,
lines 1771–1774):

```
Reproduce it (read-only on kumitate; scratch in `/tmp`):
W=$(mktemp -d /tmp/tameshi-r16-rg.XXXXXX)
```

— credited while instructing scratch in `/tmp` under the 2026-10-25 host directive.
(Dated-case context makes it a reader-discipline call, not a counter failure; the point
is the floor *cannot see it*.) The round's own history is the sharper proof: the 21
findings the fix pass resolved at 218bc6b were exactly such semantic staleness,
invisible to the floor monitor until readers found them.

## C1-C: the 30-heading amendment — predicate intact, two provenance defects

Predicate/target/kill-rule bytes: unchanged by amendments 1–5 except the C1 predicate
sentence's "30 headings" mirroring the frozen file (amendment-5 note; hashes verified:
`contract.json 5fb52e4d…`, `c1/measure.py 067c1685…`, `no-harm.sh e4e6b7ad…` identical at
e62d997, a41195d, ace79e3). The routing substance is preserved and disclosed
(`corpus/lessons/round-53.md`: "the frozen re-key scope grew 19 → 30 headings
(amendment 5…)", "The round's own edits drifted 11 further sections"). Two defects:

1. **False provenance note in the operative freeze.** `git merge-base --is-ancestor
   218bc6b5 e62d99711a0dd5d92b83acb96dd53ff22b31cb75` → true (fix pass landed
   10:15:50, amendment 5 at 10:18:54), yet `freeze.json` at e62d997 still carries
   `"frozen_at": "before any seat ran and before the fix pass"` — carried verbatim from
   the original freeze cf87276 into a re-freeze whose 30-heading scope was chosen with
   knowledge of the fix pass's damage. A reader of the evidence trail is misled.
2. **Mis-cited `before` receipt.** `contract.json` C1 `before` claims
   "cand_credited=34 lost=30 RED at the post-fix-pass candidate 218bc6b5
   (before/coldread-precheck-at-tip.stdout, exit 1)", but the committed bytes of that
   file (unchanged since cf87276; verified across cf87276 and a36d3e5) show
   `cand=6db1d220b337 cand_credited=45 lost=19 RED`. No committed round-53 receipt
   contains the 218bc6b run (`grep -rn 'lost=30' .ufo/evidence/round-53/` matches only
   `contract.json`). The number itself is true at C* — I reproduced it with the frozen
   counter (`C1_R53: rev=a41195dfc13a credited=34 lost=30 …`, rc=1) — but the cited
   receipt does not evidence it.

Smallest safe correction: no predicate change; record both items in the round report
and let `T53W2CritContract` carry them into the §9 conformance audit (its item text
already asks for exactly this). The 19→30 absorption itself is a disclosed tradeoff,
not a hidden routing change.

## C2-C: the doc check misses /tmp forms — four stale post-fix rows pass `docs=ok`

`FLEET_DOC_PATTERNS` (frozen `c2/measure.py` lines 33–38) covers exactly four literal
forms. SKILL.md at C* still documents four repaired tools' selftest scratch as
hardcoded `/tmp` — none of the patterns match, so the frozen check prints `docs=ok`
while SKILL.md asserts the opposite of C2's premise. Exact bytes (all `git show
a41195d:SKILL.md`):

- Line 2161, section `### Round-26 gate/probe registry — report interop` (**frozen
  heading #21**), the registry-check row:
  `selftest and --rev fixture trees via mkdtemp under /tmp (hardcoded, TMPDIR ignored), removed afterwards`
  — stale since 218bc6b; the code now reads `dir=tempfile.gettempdir()`.
- Line 2151, same frozen section (context-capture row):
  `selftest fixtures under /tmp/context-capture-selftest-*, removed in finally` — stale post-fix.
- Line 2163, same frozen section (repeat-control row):
  `selftest scratch under /tmp/tameshi-r12-repeat-control-selftest.* (removed on pass)` — stale post-fix.
- Line 1511, section `### Gate/probe registry` (**frozen heading #11**)
  (bash-witness-study row): `isolated /tmp/bash-witness-selftest-private.* (selftest only)` — stale post-fix.

Also missed by the same four patterns (dated-case context; reader-discipline call):
line 1771 `Reproduce it (read-only on kumitate; scratch in /tmp)` and line 1774
`W=$(mktemp -d /tmp/tameshi-r16-rg.XXXXXX)` in `## Seventh recorded case … round 16`;
and the sweep-narrative forms at lines 342–346, 543–611 (`W=/tmp/<lane>-r<round>-<n>-work`).
Verified the *fixed* forms: line 136 now reads
`Scratch for a sweep: \`$HYAKU_SCRATCH (default /fast/scratch/hyaku)/<lane>-r<round>-<n>-work/\``
and the env-diff row (line 1982) names `$HYAKU_SCRATCH/tameshi-f5.json` — so the four
patterns' original targets are genuinely repaired; what remains is outside their letter.

The grep arm's form-blindness, checked and classified: `tools/write-path-census.py:60`
and `tools/write-path-census-v4.py:632` contain `/tmp` only as **planted fixture text**
(the tool's own probe strings — inert, evidence: `classify_source` selftest maps); the
`env-diff.py` `/tmp/w` strings (lines 44, 69–71, 132) are **bwrap container-interior**
mount names, not host paths. One live non-`dir=` form survives: `tools/trace-inputs.py`
`make_workdir` (lines 575–599) falls back through a candidate list ending in `/tmp`
when `gettempdir()`'s result is unsuitable — reachable in real runs, invisible to the
frozen regex, low severity (trace logs can exceed 50 MB, but TMPDIR is consulted first).

Impact assessment: the frozen counter passes; the missed rows are **stale pointers in
two of the 30 frozen headings**, i.e. the wave-1 readers owning `### Gate/probe
registry` and `### Round-26 gate/probe registry — report interop` should file them as
findings (C1 surface), and the round report should note that the C2 doc arm is
form-bound, not semantic.

---

## What I checked and did NOT find

- `no-harm.sh` tools-scope correctly anticipates the C2 edits
  (`M:tools/registry-check.py|M:tools/env-diff.py` allowed); the 12th monitor is the
  same `dir=` regex as the counter — consistent, no contradiction.
- Phase-B `control/break-fixtures.py` is well-formed: `break_cr47` plants a
  `REGISTRY_CHECK` verdict line (caught by `cr47-verdict-line` regardless of host
  behaviour), but `PROBE_C2_CANDIDATE` (expects `true` at the candidate) **will fail on
  this host** until the registry-check guard above lands — the phase-B receipt cannot
  be 5/5 green as things stand.
- All frozen files hash-consistent across e62d997 → a41195d → ace79e3 (verified
  individually above).
- Re-ran the frozen c1 counter at C*: do-nothing state confirmed
  (`C1_R53: rev=a41195dfc13a credited=34 lost=30 rekeyed=0/30 readers=0/30 total=32 C1_R53_PASS=false`),
  matching the contract's `before` numbers (substance; see C1-C defect 2 on the citation).

## Report conformance

- No writes outside `.ufo/waves/round-53/w1/` (this file) and the seat scratch dir.
- No git/jj mutations anywhere; no frozen file, `SKILL.md`, `tools/`, `corpus/`, or
  `.ufo/evidence/` byte was touched.
- Seat scratch tree `/fast/scratch/hyaku/tameshi-r53/w1/T53W1CritClaims` removed on
  exit; my one deliberate `/tmp` probe leak (`/tmp/probe-xymlzr6t`) was deleted; no
  other `/tmp` litter from my runs remains (`ls -d /tmp/tameshi-r17* /tmp/probe-*` → none).
- Tools: system `git` and `python3 3.14.8` only; nothing installed or upgraded.
