# T51W2ExecTool11 — C3 row falsification: `tools/receipt-measure.py`

Seat: `T51W2ExecTool11` (leaf executor, wave 2 falsify). Lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
Base `9962033fd7a75aa2f2847e979dd687a5d28505a1`; candidate `6d8c11e378aa90b12650808e1b79270742935f15` (CAND).
Row audited: **SKILL.md:2152**, `#### Gate/probe registry — round 51` (heading at 2138), row 11 of 30.
Raw receipts: `.ufo/waves/round-51/w2/T51W2ExecTool11/` (13 files, listed in §6). Scratch deleted before yield.

Verdict: **the row is operably true and the frozen C3 counter credits it** — self-test exits 0 from a fresh
`git clone --shared` at CAND with the exact registered command, the usage probe exits 2 as declared, and all
eight pinned paths are load-bearing. Two row-level mismatches and one **hard falsification of the enclosing
SKILL.md section** (§4), the last of which the C3 counter structurally cannot see.

---

## 1. The row as written

| field | cell value (SKILL.md:2152) |
|---|---|
| Name | round-20 receipt-window measure |
| Kind | `gate` |
| Entry command | `python3 tools/receipt-measure.py --repo REPO --rev REV --json` |
| Verdict map | 0 clean, six items PASS at REV; 1 failed, including an absent REPO or unresolvable REV which is graded as six FAIL items rather than could-not-evaluate; 2 could-not-evaluate only on usage, that is missing --repo value, unknown flag, or --selftest mixed with other arguments |
| Self-test command | `python3 tools/receipt-measure.py --selftest` → RECEIPT_MEASURE_SELFTEST: 10/10 pass |
| Pinned values | 8 paths: `.ufo/evidence/round-20/contract.json`, `.../stage/measure.py`, `.../stage/receipt-window.py`, `tools/receipt-window.py`, `.ufo/evidence/round-20/final/receipts.json`, `.../historical-receipts.json`, `.../receipt-window-selftest.json`, `.ufo/waves/round-20/dispatch.json` |
| Write scope | reads REPO at REV; no repo writes; scratch fixture trees under TMPDIR only, prefixes `receipt-measure-selftest.*` and `tameshi-r20-measure.*` |
| Owner | tameshi |

The counter's own parse of this cell (`registry_rows` → `row_reason` → `run_row`, executed for this seat against
the frozen `.ufo/evidence/round-51/c3/measure.py`):
`row_reason → (None, spec)`, `run_row → (None, 'RECEIPT_MEASURE_SELFTEST: 10/10 pass')`, i.e. **covered**
(receipt `05-counter-row.txt`). Row 16 of the table — the seat brief's "known clone-context failure" — is
`round21 measure facade` at SKILL.md:2157, **not this row**; this row's self-test is green from the counter's
fresh clone, so that blocker does not apply here.

## 2. Measurements (exact registered commands, from `git clone --shared` at CAND)

Clone: `git clone -q --shared --no-checkout LANE clone && git checkout -q --detach 6d8c11e…`, cwd = clone root,
`TMPDIR` = a scratch dir, stdin `/dev/null`. Python 3.14.8, git 2.56.0.

| run | exit | last stdout line | wall |
|---|---|---|---|
| `python3 tools/receipt-measure.py --selftest` | **0** | `RECEIPT_MEASURE_SELFTEST: 10/10 pass` | 1098 / 1573 / 1494 / 1484 ms (4 runs) |
| `python3 tools/receipt-measure.py --r51-no-such-flag` | **2** | *(stdout empty, 0 bytes)* | 51 / 73 / 78 / 79 / 78 ms |

Self-test stdout is the 10 PASS lines plus three trailers; the last line is the marker, exactly as the row
states. The tally is arithmetic, not prose: 8 fixture cases + the `--repo` usage case + the frozen-`--check`
case = 10 (`tools/receipt-measure.py:249,263,274`).

The usage probe satisfies the counter through the *delegated* argparse, not the wrapper's own guard, when
`--repo` is absent: stderr is `usage: measure.py … error: the following arguments are required: --repo`
(`.ufo/evidence/round-20/stage/measure.py:98`). With `--repo` supplied it is `error: unrecognized arguments:
--r51-no-such-flag`. Both are exit 2, so the probe is satisfied either way — but see §3.1.

## 3. Row-level mismatches

### 3.1 `2 could-not-evaluate **only on usage**` — falsified (`03-exit-code-survey.txt` I, J)

The cell enumerates exactly three exit-2 causes: missing `--repo` value, unknown flag, `--selftest` mixed with
other arguments. All three hold (measured: exits 2, 2, 2). But exit 2 is **also** reachable from a non-usage
condition that the cell denies exists:

```
$ python3 tools/receipt-measure.py --repo <a directory that is not a git repo>     # no --rev
MEASURE: COULD_NOT_EVALUATE (no revision)
EXIT=2
$ python3 tools/receipt-measure.py --repo <a plain file>                          # no --rev
MEASURE: COULD_NOT_EVALUATE (no revision)
EXIT=2
```

Source: `.ufo/evidence/round-20/stage/measure.py:104-107` — `rev = args.rev or git(repo,"rev-parse","master")…`;
`if not rev: print("MEASURE: COULD_NOT_EVALUATE (no revision)"); return 2`. This is a *setup* could-not-evaluate,
not usage.

Consequence for the row's own text: the same cell also promises "an absent REPO … graded as six FAIL items
rather than could-not-evaluate". Measured, that is true **only when `--rev` is supplied** (case B: exit 1, six
FAIL). Without `--rev`, an absent REPO is exit 2 with *zero* items — the opposite classification. The registered
entry command always passes `--rev`, so the entry path is unaffected; the absolute language in the cell is what
is wrong.

Severity: **moderate, on the row text only.** PROTOCOL §Gate standard requires every non-{0,1} code to be
"declared … and mapped onto clean | failed | could-not-evaluate". Code 2 *is* declared and *is* mapped to
could-not-evaluate, so the standard's letter is met; what is falsified is the parenthetical gloss "only on
usage", and with it the reader's ability to tell a typo from an unresolvable repo. Fix suggestion (L1's call,
not mine to write): drop "only on usage" and add "an unresolvable revision without --rev".

### 3.2 The *executing* instrument is the caller's worktree, not REPO@REV (`09-*`, `11-worktree-contamination.txt`)

The row says "reads REPO at REV; no repo writes", and lists `.ufo/evidence/round-20/stage/measure.py` among the
pinned values. The data reads are indeed `git show REV:path` (`stage/measure.py:109-118`). The *program that
computes the verdict*, however, is resolved from the caller's checkout and executed:

```
tools/receipt-measure.py:18   ROOT = Path(__file__).resolve().parent.parent
tools/receipt-measure.py:19   MEASURE = ROOT / ".ufo/evidence/round-20/stage/measure.py"
tools/receipt-measure.py:310-313  subprocess.run([sys.executable,"-B",str(MEASURE), *arguments], env=clean_env())
```

Measured with `--repo` pointing at a **pristine** clone at CAND while the *local* instrument was edited:

- local `stage/measure.py` patched so item 1 always fails → `corrected=5`, item 1 FAIL `detail="TAMPERED-BY-WORKTREE"`, exit 1;
- local instrument patched so all six items always PASS, `--repo` pointing at an **absent** directory →
  `corrected=6`, all six PASS, **exit 0** — a false clean on a repo with no evidence at all.

So the entry command grades *worktree instrument × REV data*. PROTOCOL §Gate standard "Two evidences" names
exactly this hazard: "a gate grades the tree it runs on, so a run over a moving worktree is not comparable to
one over the cited commit". The capability side is fine — the **self-test** does pin the executing instrument:
the fixture builds the contract from `ROOT`'s staged bytes and compares against the `FROZEN_MEASURE_SHA` literal
(`tools/receipt-measure.py:29-30,89-90`) — and it catches exactly this drift:

| injected fault | self-test result | exit |
|---|---|---|
| `FROZEN_MEASURE_SHA` literal zeroed in a scratch copy | `RECEIPT_MEASURE_SELFTEST: 4/10 pass` | 1 |
| 1 byte appended to the worktree `stage/measure.py` | `RECEIPT_MEASURE_SELFTEST: 4/10 pass` | 1 |
| worktree instrument patched to force all six PASS | `RECEIPT_MEASURE_SELFTEST: 3/10 pass` | 1 |
| `git` absent from PATH (python3 present) | `RECEIPT_MEASURE_SELFTEST: 1/10 pass` | 1 |

So the row's pinned-values claim is true of the *self-test* and false of the *entry command*. The C3 predicate
runs only the self-test plus the usage probe, so the counter credits the row and cannot see this.
Severity: **moderate.** The registered entry command is correct when run from a clean checkout at REV (which is
how the counter and the wave sandbox both invoke it); a stale lane worktree silently produces a wrong clean.

### 3.3 Checked and true

- **Kind `gate`, not probe** — it genuinely fails: each of the 8 pinned paths mutated alone in a scratch clone
  yields exit 1 with the expected item FAIL (`04-pinned-matrix.txt`):

  | mutated pinned path | corrected | item that flipped |
  |---|---|---|
  | `contract.json` | 1 | 1,2,3,5,6 |
  | `stage/measure.py` | 5 | 2 |
  | `stage/receipt-window.py` | 5 | 2 |
  | `tools/receipt-window.py` | 5 | 3 |
  | `final/receipts.json` | 5 | 5 |
  | `final/historical-receipts.json` | 5 | 6 |
  | `final/receipt-window-selftest.json` | 5 | 4 |
  | `.ufo/waves/round-20/dispatch.json` | 5 | 1 |

- **Pinned paths exist at REV** — all 8 resolve at CAND (`git cat-file -e`), matching the counter's PATHISH check.
- **Entry command clean at CAND** — `--repo LANE --rev CAND --json` → exit 0, `corrected=6 open=0`, six PASS,
  run against the real lane read-only and against the clone.
- **Write scope true** — no lane writes: `git status --porcelain` for the lane over `.ufo/evidence/round-20` and
  the two tools is empty; the clone is clean after every run; `/tmp` entry count unchanged (1223 → 1223); scratch
  lived under `TMPDIR`. The two declared prefixes are the two in source: `receipt-measure-selftest.`
  (`tools/receipt-measure.py:251`) and `tameshi-r20-measure.` (`stage/measure.py:82`).
- **Marker is a computed diagnostic, not author help text** — it moves with injected faults (§3.2 table:
  10/10 → 4/10 → 3/10 → 1/10), so it is a real tally; the counter's "first token of the last non-empty stdout
  line" lands on `RECEIPT_MEASURE_SELFTEST:` and that token appears in the row.
- **Exit-code set is closed at {0,1,2}** — no 64 is reachable through this wrapper; the delegated
  `receipt-window.py`'s 64 is consumed as a subprocess return code, never propagated. `--help` exits 0 with no
  verdict, which the row does not mention; every argparse tool in the table shares this, so I do not score it.

## 4. `## Reader` — section claim verification (hard falsification)

I am the named reader for the section my row lands in. Because `#### Gate/probe registry — round 51` uses four
hashes and the round-21 monitor's `HEADING_RE` is `^#{1,3}`, the cold-read section is
**`### Round-26 gate/probe registry — report interop`**, SKILL.md **2132-2172** at CAND (the round-51 heading at
2138 and its 30-row table at 2140-2171 sit *inside* it). Verified claim by claim against candidate bytes
(`13-reader-verify.txt`, `12-section-mte-falsified.txt`):

| section claim (SKILL.md:2136) | at CAND |
|---|---|
| exit map `0 PASS … 1 FAIL · 2 SETUP · 64 usage` | **TRUE** — `tags/mte-interop.py:36`, `Parser.error`→`exit(64)` at :450, SETUP 2 at :323, 0/1 at :347 |
| `mte-interop-selftest (17/17)` | **TRUE** — 16 case tuples + 1 emitter-locations check; `:442 total = len(cases)+1`; the self-test never reads `LEG_TABLE`, so the tenth leg cannot move it |
| `leg set not equal to the nine ledger legs` | **FALSE** — `tools/mte-interop.py:318` at CAND reads `differs from the ten ledger legs %s`; at BASE it read `nine` |
| `mte-interop-check (9/9)` | **FALSE, and unreachable** — see below |
| writes only its own scratch and `--emit DIR` | **TRUE** — `tempfile.mkdtemp(prefix='tameshi-mte-*')`, `--emit` at :336-342 |
| "replays live sibling object stores, so it is not hermetic" | **TRUE** — `--fleet-root` default is the checkout's parent (:460); `--check` runs `tools/mutate-and-run.sh` |
| owner tameshi | **TRUE** |

**Why `9/9` is unreachable.** `tools/mte-interop.py:78` at CAND adds `'bash-drift-pins': 'TABLE_DRIFTPINS'`, so
`LEG_TABLE` has **ten** entries. The guard at :316-318 raises SETUP unless
`set(legs) == set(tables) == set(LEG_TABLE)`, so `len(legs)` is 10 on every scored path; :343-344 prints
`'legs_conforming=%d/%d' % (…, conforming, len(legs))`. The only reachable tallies are `n/10`. The literal
needle `MTE_INTEROP: PASS legs_conforming=9/9` therefore **cannot appear** at CAND. Wave 1 corroborates the
positive side independently: `w1/T51ExecEmbed.md:114` records `MTE_INTEROP: PASS legs_conforming=10/10`.

**Downstream, and why it is not repairable inside the frozen scope.** `tools/registry.json` is **unchanged**
BASE..CAND (`git diff --stat` empty) and still pins the dead needle on an `active` row:
`mte-interop-check expect={"exit":0,"stdout_contains":["MTE_INTEROP: PASS legs_conforming=9/9"]}`.
`registry-check.py:720` sets `held = (got == expect.exit and no missing needle)`; `:884` exits 1 when any active
row differs. Every branch ends the same way — the row runs and prints `/10` (needle missing), or it SETUPs (got 2
≠ expect 0), or it times out (got timeout ≠ expect 0) — so **`python3 tools/registry-check.py --rev CAND` cannot
exit 0**, while its own C3 row (SKILL.md:2154) declares "0 clean" as the entry result. `[INFERENCE]` from
`registry-check.py`'s source plus the unreachability proof above; I did not execute `--rev` (that is the parent's
gate).

Repair is blocked by the freeze: the no-harm tools-scope allowlist (`no-harm.sh:35`) names exactly
`M:tools/mutate-and-run.sh`, `M:tools/tally-audit.py`, `M:tools/tally-audit-v2.py`,
`M:tools/tally-audit-v3.py`, `M:tools/mte-interop.py`. `tools/registry.json` is **not** on it, so fixing the
registry row turns `NOHARM tools-scope` RED. W1 flagged the risk in prose (`w1/T51CritRekey.md:153`: "At-risk:
… both become ten/10") but not the `registry.json` consequence, and neither `contract.json`, `l1-notes.md` nor
any other w1 report records it. **This needs an L1 decision (amendment 3 to widen tools-scope to
`tools/registry.json`, or an accepted, disclosed red).** I wrote no source and repaired no row.

Note for the re-key: the same byte edit that fixes the sentence would itself re-key this section, and the section
is already in the 20-section dropped set — so the fix and the re-key can ship together.

## 5. What the C3 counter can and cannot see here

Credited: the row exists with 8 conforming cells, its self-test exits 0 from a clone at CAND and its last-line
token appears in the row, and the usage probe's code is declared. Not seen: the verdict map's *semantics*
(§3.1), the entry command's instrument provenance (§3.2), and — because the counter never runs
`registry-check --rev` — the dead `9/9` needle (§4). This is precisely contract C3 `cannot_see`: "that a row's
kind, write scope and pinned-value description are true of the tool, and that the verdict map names every code
the tool can exit with beyond 0, 1 and the usage code". No claim rule, target, counter or spec was amended by
this seat.

## 6. Files changed, evidence, risks

**Files changed:** none in the lane, fleet or any sibling repo. New files only, under this seat's report paths:
`.ufo/waves/round-51/w2/T51W2ExecTool11.md` (this report) and `.ufo/waves/round-51/w2/T51W2ExecTool11/`:

| receipt | content |
|---|---|
| `01-selftest.txt` | registered self-test from the clone at CAND: exit 0, last line, wall |
| `02-usage-probe.txt` | `--r51-no-such-flag`: exit 2, 0 stdout bytes, stderr, last stdout line |
| `03-exit-code-survey.txt` | 10 invocations A-J: 0/1/2 for entry, absent repo, bad rev, three usage forms, `--help`, two non-usage exit-2 paths |
| `04-pinned-matrix.txt` | 8 single-path mutations, item that flipped, exit |
| `05-counter-row.txt` | the frozen counter's own `row_reason` / `run_row` for SKILL.md:2152 |
| `06-source-facts.txt` | sha256 of tool + 3 instruments; the literals, prefixes, exit-map lines |
| `07-marker-mutation.txt` | marker under three injected faults (4/10, 4/10, 1/10) |
| `08-marker-meaning.txt` | marker-is-a-tally summary |
| `09-worktree-instrument.txt` | wrapper `ROOT`/`MEASURE` lines and the false-clean demonstration |
| `10-section-claims.txt` | structural re-derivation of the round-51 table: 30 rows, all 8 cells, 30 distinct tools, none absent, kinds `{gate,probe}`, owner tameshi |
| `11-worktree-contamination.txt` | A/B/C/D of the entry-command instrument test |
| `12-section-mte-falsified.txt` | base-vs-CAND leg counts, guard, print, registry.json diff-empty, allowlist line |
| `13-reader-verify.txt` | the §4 claim table, provenance, repairability |

**Tooling:** nothing installed or upgraded (no pacman/uv/cargo/npm/brew call); `pacman` was not touched. Only
Python 3.14.8 and git 2.56.0, both already present.

**Risks / blockers for the parent:**
1. §4 is a live defect on a frozen-claim surface and is **not repairable inside the frozen no-harm scope**; it
   needs an L1 decision. `tools/registry.json` pins a needle the candidate tool can never print, so the
   `entry-registry walk` C3 row's declared "0 clean" entry result is false at CAND.
2. §3.2 means the registered entry command's verdict depends on the caller's worktree instrument; a dirty lane
   gives a wrong clean with no error. The self-test does catch the drift, so running the row's self-test before
   the entry command is a sufficient guard and is worth stating in the row.
3. §3.1 is editorial (row text) — no counter, no claim, no score is affected.
4. `@P@` in the seat brief appears unexpanded; I used the concrete `Report:` path (`T51W2ExecTool11.md`) and the
   sibling-seat convention (`T51W2ExecTool03/`, `T51W2ExecTool08.md`).
5. Scratch `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool11/` (~971 MB of `git clone --shared` worktrees) is
   deleted before yield; `/tmp` grew by zero entries.
