# MutateC2Counter — calibration probes of the round-26 C2 counter

Seat: `TameshiR26.MutateC2Counter` (mutation-tester). Wave 1 of round 26, item C2
(calibration). Everything below was run inside a private clone and /tmp scratch trees.
The lane was not edited except for this report file.

## Verdict

**The counter can fail, and it is right on the states it was written for — but ten of my
twenty-six probes defeat it.** On a scratch repo where all three routed defects are still
in place, each dressed so that the counter's own literal tokens are present, the counter
answers `C2_ITEM R25-SPOT-1: RESOLVED`, `C2_ITEM R25-SPOT-2: RESOLVED`,
`C2_ITEM R25-SPOT-3: RESOLVED`, `C2_RECORD: mismatches=0/3` and **exits 0**. The
contract's target for C2 is exactly `mismatches=0/3, exit 0`, so that state and the
honest state are indistinguishable to the counter.

Summary over the 26 probes (ground truth taken from the routed text at
`corpus/lessons/round-25-verifier-spotcheck.md:189-199`):

| Class | Count | Probes |
|---|---|---|
| correct | 14 | the genuine states, the superseded row, the commented-out row, and eight pin probes |
| **gamed (false negative: counter says RESOLVED, the defect is still there)** | **10** | argv-only, code-fenced SKILL row, "amendment 3 was never applied", later-section-only, flag without seat evidence, stale receipt, unrelated receipt, receipt outside the repo, wrong selftest count, verified-at inside a code fence |
| **false positive (counter says MISMATCH, the record is fixed)** | **2** | SKILL row with extra spaces, "amendment three" spelled out |

**The freeze constrains the fix.** `contract.json` records the counter as frozen before
"any edit to the files the C2 counter reads", so the counter itself must not be edited
mid-round. The corrections below are therefore for the integrator to take in one of two
ways: apply the honest fix and add a *companion* checker (the round-25 precedent is
`c1-pins.py`), or harden the counter in the next round. I made no edit to any production
file and no edit to the counter.

## Setup (evidence)

```
git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/mutatec2-r26
git -C /tmp/mutatec2-r26 checkout -q --detach a08e85c5d7f899e8a5992e20517edb1a380d79eb
git -C /tmp/mutatec2-r26 log --oneline -1
a08e85c round-26: ninth ledger leg js-cite-check (5/10, 10/10 verdict predictions), runner and interop wired to nine legs, mte-interop registry rows and SKILL row, sweep evidence
```

Detector (unmodified, read out of the clone):

```
$ sha256sum /tmp/mutatec2-r26/.ufo/evidence/round-26/c2-measure.py
be14cc45baacbe39d115b44f6d6acbe17db7298d9938bd2766a5269b359630af
```

The same digest is in the lane tree (`sha256sum
/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-26/c2-measure.py`), so
the counter I probed is the frozen counter, byte for byte.

Baseline on the full clone at the integration revision:

```
$ python3 .ufo/evidence/round-26/c2-measure.py --repo /tmp/mutatec2-r26
C2_ITEM R25-SPOT-1: RESOLVED
C2_ITEM R25-SPOT-2: MISMATCH (SCORECARD after round-25 results lacks 'amendment 3'; SCORECARD after round-25 results lacks 'before_any_after_measurement'; lesson after ## Claims lacks 'amendment 3')
C2_ITEM R25-SPOT-3: MISMATCH (verified-at tool sha256 is not a prefix of sha256(tools/mte-interop.py)=193ea6e32f89; no named .stdout receipt at the revision carries the verified-at selftest count)
C2_RECORD: mismatches=2/3
EXIT=1
```

The lane worktree already carries uncommitted edits to five of the files this counter
reads (`SCORECARD.md`, `SKILL.md`, `corpus/lessons/round-25.md`,
`corpus/knowledge/mte-report-interop.md`, `tools/registry.json`) from the integrator and
from sibling seats. I measured only the frozen `a08e85c` bytes, so my numbers are not a
statement about the lane's current worktree.

### Probe method

The counter reads six things and nothing else: `tools/registry.json`, `SKILL.md`,
`SCORECARD.md`, `corpus/lessons/round-25.md`, `corpus/knowledge/mte-report-interop.md`,
the bytes of `tools/mte-interop.py`, plus whatever `.stdout` receipt the verified-at line
names. Each probe is therefore a slim scratch repo under
`/tmp/mutatec2-r26/probes/<name>/` holding exactly those files. The slim base
reproduces the full-clone baseline verbatim (`mismatches=2/3`, exit 1), which is what
makes the slim scratch a valid `--repo` argument.

The ground truth for each probe comes from the routed text, not from the counter:

- **R25-SPOT-1** (`:189-192`): the tool is a verdict tool "with no registry row at its
  registry home (`SKILL.md`; also absent from `tools/registry.json`)". Resolved means an
  *active* `tools/registry.json` row that actually runs `tools/mte-interop.py`, plus a
  table row for it in the `SKILL.md` registry home.
- **R25-SPOT-2** (`:193-196`): "the SCORECARD round-25 header and the lesson's `## Claims`
  name only amendments 1–2. Amendment 3 (in `77302fa`) appears only in its JSON and the
  report. Its `before_any_after_measurement` flag also omits that seats saw C2 PASS 8/8
  at `c9ff09f`/`09dc114`." Resolved means both records carry an affirmative amendment-3
  statement, and the flag records the seat evidence.
- **R25-SPOT-3** (`:197-199`): "verified-at records the `09dc114` run (tool `8c24255c…`,
  selftest 16/16), not the measured tool `8269b82f…` (17/17). Refresh it." Resolved means
  the verified-at names the tool at the revision, that tool's real selftest count, and a
  receipt that is that tool's own output.

### What the counter actually checks

`/tmp/mutatec2-r26/.ufo/evidence/round-26/c2-measure.py`:

- `:38-39` item1 — a row of `tools/registry.json` whose `status` is `active` and whose
  `argv` list has *some element containing* the substring `tools/mte-interop.py`.
- `:41` item1 — `SKILL.md` holds a line matching `^\| `tools/mte-interop\.py` \|`
  (searched over the whole file, fenced code and comments included).
- `:53-58` item2 — the text after the heading `### Round 25 — measured results
  (TameshiR25)` (which is the last section of the file) contains the case-insensitive
  substrings `amendment 3`, `77302fa`, `before_any_after_measurement`.
- `:60-69` item2 — the text after the first `\n## Claims` in `corpus/lessons/round-25.md`
  contains `amendment 3` and `77302fa`.
- `:74-76` item3 — exactly one line of the knowledge entry starts with `verified-at:`.
- `:80-81` item3 — that line names `tool sha256 <8..64 hex>` and the hex is a *prefix* of
  `sha256(tools/mte-interop.py)`.
- `:83-84` item3 — that line names `selftest N/N` with `N == N`.
- `:86-93` item3 — some backticked `.stdout` path in that line exists on disk and its
  bytes contain `MTE_SELFTEST: N/N pass`.
- `:106-115` — one `OSError`/`ValueError` in any item aborts the whole run with exit 2;
  exit 0 means zero mismatches, exit 1 means at least one.

## The 26 probes

`truth` is the routed defect state; `counter` is what the frozen counter answered.

| # | Probe | Label | truth | counter | Verdict |
|---|---|---|---|---|---|
| 1 | `p1-base-genuine` (active rows + genuine SKILL row) | SPOT-1 | RESOLVED | RESOLVED | correct |
| 2 | `p1-argv-mentions-only` (`argv` = `["sh","-c","echo tools/mte-interop.py"]`) | SPOT-1 | MISMATCH | **RESOLVED** | **gamed** |
| 3 | `p1-skill-row-in-code-fence` (row deleted, same text left in a fenced example) | SPOT-1 | MISMATCH | **RESOLVED** | **gamed** |
| 4 | `p1-superseded-rows` (both rows `status: superseded`) | SPOT-1 | MISMATCH | MISMATCH | correct |
| 5 | `p1-skill-row-commented-out` (row inside an HTML comment) | SPOT-1 | MISMATCH | MISMATCH | correct |
| 6 | `p1-skill-row-extra-spaces` (`\|  `tools/mte-interop.py`  \|`) | SPOT-1 | RESOLVED | MISMATCH | **false positive** |
| 7 | `p1-skill-row-absent` (pin) | SPOT-1 | MISMATCH | MISMATCH | correct |
| 8 | `p2-genuine` (real amendment-3 correction in both files) | SPOT-2 | RESOLVED | RESOLVED | correct |
| 9 | `p2-never-applied` ("Amendment 3 was never applied … `before_any_after_measurement` … `77302fa`") | SPOT-2 | MISMATCH | **RESOLVED** | **gamed** |
| 10 | `p2-later-section-only` (tokens only in a later `## Round 26` section and a later lesson section) | SPOT-2 | MISMATCH | **RESOLVED** | **gamed** |
| 11 | `p2-flag-without-seat-evidence` (flag named, but no `8/8`, no `c9ff09f`/`09dc114`) | SPOT-2 | MISMATCH | **RESOLVED** | **gamed** |
| 12 | `p2-spelled-out` ("Amendment three") | SPOT-2 | RESOLVED | MISMATCH | **false positive** |
| 13 | `p2-flag-omitted` (pin) | SPOT-2 | MISMATCH | MISMATCH | correct |
| 14 | `p2-lesson-omits` (pin) | SPOT-2 | MISMATCH | MISMATCH | correct |
| 15 | `p2-no-hash-scard` (pin) | SPOT-2 | MISMATCH | MISMATCH | correct |
| 16 | `p2-no-hash-lesson` (pin) | SPOT-2 | MISMATCH | MISMATCH | correct |
| 17 | `p3-genuine` (current tool sha256, 17/17, real receipt of this tool's run) | SPOT-3 | RESOLVED | RESOLVED | correct |
| 18 | `p3-stale-receipt` (names the round-25 receipt) | SPOT-3 | MISMATCH | **RESOLVED** | **gamed** |
| 19 | `p3-unrelated-receipt` (names a file that merely contains the string) | SPOT-3 | MISMATCH | **RESOLVED** | **gamed** |
| 20 | `p3-receipt-outside-repo` (absolute path outside the repo) | SPOT-3 | MISMATCH | **RESOLVED** | **gamed** |
| 21 | `p3-wrong-selftest-count` (`selftest 1/1`) | SPOT-3 | MISMATCH | **RESOLVED** | **gamed** |
| 22 | `p3-verified-at-in-code-fence` (live line renamed, fenced example carries `verified-at:`) | SPOT-3 | MISMATCH | **RESOLVED** | **gamed** |
| 23 | `p3-no-receipt` (pin) | SPOT-3 | MISMATCH | MISMATCH | correct |
| 24 | `p3-wrong-tool-sha` (names `8c24255c…`, the previous build) | SPOT-3 | MISMATCH | MISMATCH | correct |
| 25 | `p3-unequal-count` (`selftest 17/18`) | SPOT-3 | MISMATCH | MISMATCH | correct |
| 26 | `p-all-gamed` (all three defects still in place, tokens present) | all | MISMATCH | `mismatches=0/3`, **exit 0** | **gamed** |

Probe 26 in full:

```
$ python3 .ufo/evidence/round-26/c2-measure.py --repo /tmp/mutatec2-r26/probes/p-all-gamed
C2_ITEM R25-SPOT-1: RESOLVED
C2_ITEM R25-SPOT-2: RESOLVED
C2_ITEM R25-SPOT-3: RESOLVED
C2_RECORD: mismatches=0/3
EXIT=0
```

Its three ingredients are each individually legal-looking: the registry rows exist but
their `argv` only names the path (`sh -c "echo tools/mte-interop.py"`), the SCORECARD and
the lesson carry a sentence saying amendment 3 was never applied, and the verified-at
names the round-25 receipt.

### Probe 18 deserves its own note

The stale receipt is not a hypothetical. `tools/mte-interop.py` changed between the
round-25 receipt commit and the integration revision:

```
$ git show 154bf4d:tools/mte-interop.py | sha256sum
8269b82f213e094ffd30adc20b20e28b1f67764d2eccb089983eb9dc546eb02c
$ sha256sum tools/mte-interop.py            # at a08e85c
193ea6e32f89016baffe07d41fee17074651e74d4807f7fb70dff2fbe0f72cc4
$ git log --oneline -3 -- .ufo/evidence/round-25/after/c2-selftest.stdout
154bf4d round-25: after receipts, emitted reports, measured SCORECARD rows, lesson and LOG; harmed monitor intermediate retained
```

So `.ufo/evidence/round-25/after/c2-selftest.stdout` is the output of the *old* tool
(`8269b82f…`) and it does contain `MTE_SELFTEST: 17/17 pass`. A verified-at that names
the current tool `193ea6e3…` together with that receipt passes the counter, and the
record it produces is false: the receipt is not this tool's output.

The genuine receipt used in probe 17 was produced by running the tool at the integration
revision:

```
$ timeout 600 uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --selftest > /tmp/mutatec2-r26-selftest.stdout
EXIT=0
$ tail -1 /tmp/mutatec2-r26-selftest.stdout
MTE_SELFTEST: 17/17 pass
```

## Counter-mutant sweep (are the checks load-bearing?)

I mutated the counter itself, one check at a time, in copies under
`/tmp/mutatec2-r26/counter-mutants/` (the lane counter was never touched), and ran every
mutant over the same 26 frozen probe fixtures. A mutant is *detected* when some probe's
label verdict changes.

| Mutant | Change | Detected by |
|---|---|---|
| M1 | item1 ignores `status` (a superseded row counts) | `p1-superseded-rows` |
| M2 | item1 SKILL regex loosened to any mention of the path | `p1-skill-row-commented-out`, `p1-skill-row-extra-spaces` |
| M10 | item1 drops the SKILL.md table-row requirement | `p1-skill-row-absent`, `p1-skill-row-commented-out`, `p1-skill-row-extra-spaces` |
| M3 | item2 bounds the SCORECARD search to the round-25 section | `p2-later-section-only` (this mutant *tightens* the counter: it turns the gamed state into MISMATCH) |
| M7 | item2 drops `before_any_after_measurement` from the SCORECARD list | `p2-flag-omitted` |
| M9 | item2 drops `77302fa` from the SCORECARD list | `p2-no-hash-scard` |
| M8 | item2 drops the lesson's Claims token requirement | `p2-lesson-omits`, `p2-no-hash-lesson` |
| M11 | item2 drops `77302fa` from the lesson list | `p2-no-hash-lesson` |
| M4 | item3 accepts any verified-at without checking the receipt | `p3-no-receipt` |
| M5 | item3 accepts any tool sha256 | `p3-wrong-tool-sha` |
| M6 | item3 accepts an unequal `selftest N/N` | `p3-unequal-count` |

**11 of 11 mutants detected.** Every individual check in the counter is load-bearing and
pinned by at least one probe, so the ten gamed states are coverage holes in the checks,
not dead code. The sweep also gives the cheapest hardening for free: mutant M3 is a
four-line change to the counter that closes probe 10 on its own.

## Failure modes of the counter itself

The counter aborts, or reports a crash as a mismatch, in five states. All five were
produced by mutating a probe fixture and running the frozen counter.

| Fixture | Counter output | Exit |
|---|---|---|
| `corpus/lessons/round-25.md` deleted | `C2_ITEM R25-SPOT-1: RESOLVED` then `C2_RECORD: SETUP (R25-SPOT-2: [Errno 2] No such file or directory: …/corpus/lessons/round-25.md)` — items 1 and 3 are never measured | 2 |
| `tools/registry.json` replaced by a JSON list | empty stdout, `AttributeError: 'list' object has no attribute 'get'` on stderr — **no `C2_RECORD:` line at all** | 1 |
| `tools/registry.json` invalid JSON | `C2_RECORD: SETUP (R25-SPOT-1: Expecting value: line 2 column 1 (char 11))` | 2 |
| `SKILL.md` holds a non-UTF-8 byte | `C2_RECORD: SETUP (R25-SPOT-1: 'utf-8' codec can't decode byte 0xff …)` | 2 |
| `--repo` pointing at a missing directory | `C2_RECORD: SETUP (R25-SPOT-1: [Errno 2] No such file or directory: …)` | 2 |
| no arguments | `usage: c2-measure.py --repo CLONE_AT_REV` on stderr | 64 |

Two of these matter for how a caller should read the counter:

1. **A crash is indistinguishable from a mismatch.** The JSON-list case exits 1 with no
   `C2_RECORD:` line; exit 1 is also the "at least one mismatch" code. A caller that
   looks only at the exit status reads a crash as a measurement.
2. **One unreadable file kills the whole measurement.** The missing lesson file aborts
   after item 1, so two measurable labels are lost to one missing input.

## Named holes and the smallest safe correction

The counter is frozen for this round (see `contract.json`, `frozen_before`), so nothing
below was applied. Each item names the smallest change that closes it and whether it can
be done without touching the frozen counter.

1. **A registry row that only names the path counts as a registry row (probe 2).**
   `:38-39` tests `any("tools/mte-interop.py" in str(a) …)` over `argv`. Smallest fix in
   the counter: require the tool path to be a whole `argv` element
   (`any(str(a) == "tools/mte-interop.py" for a in r.get("argv", []))`), so a shell
   string that merely contains the path does not count. This can be done in a companion
   script as well, because the registry row's own `argv` is machine-readable.
2. **The SKILL.md row may live anywhere in the file (probes 3 and 6).** `:41` searches
   the whole file, so a fenced example or a differently spaced row both count. Smallest
   fix in the counter: strip fenced code blocks and HTML comments before searching, and
   match the table row with a whitespace-tolerant pattern
   (`^\|\s*`tools/mte-interop\.py`\s*\|`). Probe 6 is the false-positive twin: today a
   correct row written `|  `tools/mte-interop.py`  |` is reported as MISMATCH.
3. **The SCORECARD search is unbounded below the heading (probe 10).** `:56` takes
   everything after `### Round 25 — measured results (TameshiR25)` to the end of file,
   and that heading is the last section, so any later section satisfies the check.
   Smallest fix in the counter: cut the tail at the next `\n## ` heading. This is
   mutant M3 above, and it is the single cheapest hardening in this report.
4. **Substring presence cannot tell an affirmative record from a denial (probe 9).**
   `:57-58` and `:66-69` ask only whether three and two strings occur. A sentence that
   says amendment 3 was never applied contains all of them. Smallest fix that keeps the
   counter textual: require the amendment-3 tokens to appear in one affirmative
   sentence or one table row, and require that row to name the seat evidence the routed
   item asks for (`8/8`, `c9ff09f`, `09dc114`). The honest reading of the routed item is
   that the correction is a *record* of amendment 3, so a companion checker that reads
   `contract-amendment-3.json` and compares the named fields against the SCORECARD row
   is stronger than any string test — the round-25 lane already used that shape
   (`c1-pins.py`).
5. **The flag can be named without its content (probe 11).** The routed item asks the
   `before_any_after_measurement` flag to record "that seats saw C2 PASS 8/8 at
   `c9ff09f`/`09dc114`". The counter only requires the flag's name. Smallest fix: require
   `8/8` and both commit ids in the same section as the flag.
6. **The receipt need not be the named tool's output (probes 18, 19, 20).** `:86-93`
   requires only that some named `.stdout` file exists and contains the string
   `MTE_SELFTEST: N/N pass`. Three escapes follow: the stale round-25 receipt (probe 18),
   an unrelated file that happens to contain the string (probe 19), and an absolute path
   outside the repo (probe 20 — `Path(repo) / "/tmp/x"` resolves to `/tmp/x`). Smallest
   fix in the counter: reject absolute paths and any path containing `..`, require the
   receipt to live under the repo, and require the receipt to name the tool itself (the
   run prints `MTE_INTEROP:`/`MTE_SELFTEST:` from `tools/mte-interop.py`; the receipt
   path or a banner in the bytes can be required). The strongest version binds the
   receipt to the tool digest: require the receipt's own recorded sha256 to equal the
   `tool sha256` in the same verified-at line.
7. **The selftest count is never compared with the tool's real count (probe 21).** `:83-84`
   only requires `N == N`, so `selftest 1/1` passes. The tool runs 17 cases at this
   revision (`MTE_SELFTEST: 17/17 pass`). Smallest fix: compare the recorded `N` with the
   number of cases the tool's own selftest prints in the named receipt, and require the
   receipt's `N/N` to equal the recorded `N/N`.
8. **The verified-at line is found by prefix match over the whole file (probe 22).** `:74-76`
   takes every line starting with `verified-at:` and requires exactly one; a fenced
   example satisfies it. Smallest fix: strip fenced code blocks and HTML comments before
   selecting the line, and require exactly one surviving line.
9. **An 8-hex-char prefix is accepted as the tool digest (`:80-81`).** The regex allows
   8 to 64 hex characters and the check is `tool.startswith(prefix)`. The record should
   carry the full digest; the smallest fix is to require the full 64 characters.
10. **A crash reads as a mismatch, and one bad input kills the run.** `:106` catches only
    `OSError` and `ValueError`; an `AttributeError` escapes and exits 1 with no
    `C2_RECORD:` line, and any `OSError` aborts the remaining labels. Smallest fix:
    catch `Exception` per label, report that label as `SETUP`, continue with the others,
    and reserve exit 1 for a real mismatch.

## Restoration evidence

- The lane was not edited by this seat except for this report file. All fixtures,
  mutant counters and receipts live under `/tmp/mutatec2-r26/`.
- The counter is byte-identical in the lane and in the clone:
  `be14cc45baacbe39d115b44f6d6acbe17db7298d9938bd2766a5269b359630af` for
  `.ufo/evidence/round-26/c2-measure.py`.
- `tools/mte-interop.py` is unchanged in the clone and in the lane
  (`193ea6e32f89016baffe07d41fee17074651e74d4807f7fb70dff2fbe0f72cc4`), and it is
  byte-identical to the blob at `a08e85c`.
- `git -C /tmp/mutatec2-r26 status --porcelain` shows only the untracked scratch
  directories; the tracked files the counter reads are the committed blobs.
- The lane's own `git status --porcelain` shows modifications to `LOG.md`,
  `PROVINCE.md`, `SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`,
  `corpus/SOURCES.md`, `corpus/knowledge/mte-report-interop.md`,
  `corpus/lessons/round-25.md` and `tools/registry.json`. Those are the integrator's and
  the sibling seats' in-flight edits for this wave, not mine: this seat wrote only
  `/tmp/mutatec2-r26/**` and this report file. I made no change to any of them.
- No git write command was run in the lane (no add, commit, checkout, reset, stash,
  push, fetch or pull), and no `jj` command was run anywhere.

## Tooling

No tool was installed or upgraded for this item. `git`, `python3`, `bash` and `sha256sum`
were already present. One dependency was fetched for a single command, the genuine
selftest receipt: `uv run --no-project --with jsonschema==4.25.1` (PyPI, through the uv
resolver; the package was already in the local uv cache). No pacman transaction was
attempted, because host pacman transactions are paused, and no host service was
restarted.

## What the integrator can take from this

The counter is green on the three states it was written for, it fails on the base
revision, and every one of its eleven internal checks is load-bearing. But ten of my
twenty-six probes pass it while the routed defect is still in place, and one of them
drives the whole counter to `mismatches=0/3, exit 0` — the contract's own target value
— with all three defects present. The honest fixes for items 2 and 3 must therefore
carry the substance the counter cannot see (an affirmative amendment-3 record with the
seat evidence, a verified-at whose receipt is this tool's own output at this revision),
not only the three literal tokens the counter looks for. If extra teeth are wanted
inside this round, the cheapest counter-side hardening is mutant M3 (bound the SCORECARD
search to the round-25 section) plus a companion checker that reads the amendment JSON
and the tool digest, in the shape of the round-25 `c1-pins.py`.

Report: .ufo/waves/round-26/w1/MutateC2Counter.md
