# T51W2ExecTool04 — C3 registry row falsification: `tools/env-diff.py` at CAND

Seat: T51W2ExecTool04, wave 2 (falsify), round 51. Item: independently audit the canonical
round-51 registry row for `tools/env-diff.py` at candidate
`6d8c11e378aa90b12650808e1b79270742935f15`; run the row's exact backticked self-test and the
`--r51-no-such-flag` usage probe from a `git clone --shared` at CAND with scratch TMPDIR and stdin
`/dev/null`; check every row field against the tool's source. Read-only on the lane, fleet and
sibling repos; I wrote only this report and `@P@ExecTool04/` under `.ufo/waves/round-51/w2/`.
Nothing installed, nothing repaired, no source or row edited. Scratch
`/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool04` deleted before yield.

Clone: `git clone -q --shared --no-checkout <lane> clone`; `git -C clone rev-parse --show-toplevel`
→ the clone; `checkout --detach 6d8c11e3…` → HEAD `6d8c11e378aa90b12650808e1b79270742935f15`.
`git -C clone status --porcelain` empty after every run (lane trees untouched). Raw receipts:
`.ufo/waves/round-51/w2/@P@ExecTool04/receipts.txt`.

## 0. The row under audit

`SKILL.md:2145`, inside `#### Gate/probe registry — round 51` (heading line 2138). Eight cells:

| # | cell |
|---|---|
| name | environment-profile differential |
| kind | `gate` |
| entry | `python3 tools/env-diff.py --contract .ufo/evidence/round-21/c2-contract.json --out DIR/receipt.json --jobs 3` |
| verdict map | `0 clean; 1 failed; 2 and 64 could-not-evaluate` |
| self-test | `python3 tools/env-diff.py --selftest` → exit 0, last line ENVDIFF_SELFTEST: 9/9 pass |
| pinned | `.ufo/evidence/round-21/c2-contract.json`, `.ufo/evidence/round-21/f5/receipt.json`; literal expected classifications in the tool selftest |
| scope | caller-chosen `--out` FILE plus sandboxes under `/tmp/tameshi-r21-envdiff.*` and TMPDIR-respecting selftest trees; lane trees read-only |
| owner | tameshi |

The counter's own parser sees exactly this row and accepts it: `measure.py` (the frozen C3 counter)
`registry_rows()` yields 32 eight-cell rows, exactly one of which names `tools/env-diff.py`;
`row_reason()` returns `None` (no structural defect) and `run_row()` returns
`(None, 'ENVDIFF_SELFTEST: 9/9 pass')` — i.e. the row passes the frozen counter. Receipts §5.

**Verdict: the row is mechanically conformant but semantically false on two fields the frozen
counter cannot see.** The C3 predicate's own `cannot_see` clause names exactly these: *"That a
row's kind, write scope and pinned-value description are true of the tool, and that the verdict map
names every exit code the tool can exit with beyond 0, 1 and the usage code."* Findings F1–F3 below
are that attack. **This does not falsify C3's counter** (the counter passes); it falsifies the
row's *truthfulness*, which is what this seat was asked to check.

## 1. Self-test and usage probe (as the row states them) — PASS

Exact backticked command, from the clone at CAND, `TMPDIR=$S/tmp`, stdin `/dev/null`:

```
$ cd CLONE && TMPDIR=$S/tmp python3 tools/env-diff.py --selftest </dev/null
ENVDIFF_CASE invariant PASS
ENVDIFF_CASE tz PASS
ENVDIFF_CASE locale PASS
ENVDIFF_CASE home PASS
ENVDIFF_CASE columns PASS
ENVDIFF_CASE repeat PASS
ENVDIFF_CASE missing-bwrap PASS
ENVDIFF_CASE timeout PASS
ENVDIFF_CASE pin-mismatch-public-cli PASS
ENVDIFF_SELFTEST: 9/9 pass
exit=0
```

Three runs: exit 0 each, last line `ENVDIFF_SELFTEST: 9/9 pass` each, wall **247 / 248 / 262 ms**,
stderr empty. The row's "exit 0, last line ENVDIFF_SELFTEST: 9/9 pass" is literally true, and the
finding id `ENVDIFF_SELFTEST:` is the tool's own diagnostic (`tools/env-diff.py:194`,
`print(f"ENVDIFF_SELFTEST: {passed}/{len(checks)} pass")`) — not author-chosen help text. The
counter's marker rule (`marker = last.split()[0]`) yields `ENVDIFF_SELFTEST:`, which is present in
the row's Self-test cell. **PASS.**

Usage probe:

```
$ python3 tools/env-diff.py --r51-no-such-flag </dev/null
usage: env-diff.py [-h] [--contract CONTRACT] [--out OUT]
                   [--fleet-root FLEET_ROOT] [--jobs JOBS] [--selftest]
ENVDIFF_USAGE: unrecognized arguments: --r51-no-such-flag
exit=64
wall=44 ms
```

Exit 64 is declared in the row's verdict map (`2 and 64 could-not-evaluate`), and 64 is the code
the tool actually raises for usage errors (`tools/env-diff.py:198-201`, a `Parser` subclass whose
`error()` calls `self.exit(64, ...)`). **PASS.** The counter's usage-code check
(`re.search(r'(?<![0-9])64(?![0-9])', vmap)`) is satisfied.

Exit-code sweep (receipts §12) — every reachable code is declared in the map:

| invocation | exit | row's map |
|---|---|---|
| `--selftest` | 0 | clean |
| `--r51-no-such-flag` | 64 | could-not-evaluate ✓ |
| missing `--out` | 64 | ✓ |
| `--jobs 0` / `--jobs 4` / `--jobs abc` | 64 | ✓ |
| contract not JSON / unreadable / `surfaces:[]` / surface missing keys / `--out` is a directory | 2 | ✓ |
| `--help` | 0 | (argparse; not a verdict) |

No code outside {0, 1, 2, 64} is reachable, and the map declares all four. The counter's
`verdict-map-lacks-0-or-1` and `usage-exit-N-undeclared` checks both hold.

## 2. F1 — kind `gate` is false: the tool cannot fail, so under §Gate standard it is a probe

`PROTOCOL.md` §Gate standard (fleet root, lines 377-379):

> "A **gate** is a committed, re-runnable verdict script a lane owns: it reads surfaces, compares
> them against expected values persisted in its own repo, and returns a verdict. **A tool that
> cannot fail is a probe**, and is registered as one."

The row declares `kind = gate` with `0 clean; 1 failed`. The tool **cannot fail against an
expected value**, because it has no expected value to compare against:

- The contract `.ufo/evidence/round-21/c2-contract.json` carries **no expected classification** per
  surface. Its per-surface keys are only `name, repo, rev, path, interp` (+`blob_sha256` on 8 of 9);
  `classification_rules` are *generic derivation rules* ("clean tuple != clean_repeat tuple ->
  classification must be `nondeterministic`"), not per-surface expectations. Receipts §8.
- The tool therefore only ever *derives* a classification (`classify()`, `tools/env-diff.py:98-107`)
  and reports it. `main()` (`:243-245`) computes
  `done = sum(r.get("classification") != "unavailable" for r in rows)` and returns
  `0 if done == len(rows) else 1`. **Exit 0 means "every surface got a classification", not "the
  subject is clean."** Nothing is compared to an expectation.
- Confirmed empirically with three controlled fixture repos (receipts §6; each fixture's
  `git rev-parse --show-toplevel` asserted equal to the fixture dir before its commit):

| fixture | classification | tool exit | what happened |
|---|---|---|---|
| nondeterministic target (`$BASHPID`) | `nondeterministic` | **0** | a non-invariant surface still exits 0 |
| target whose clean run exits 3 | `unavailable` | 1 | the *subject* failed, but the tool reports "unavailable", not "failed" |
| wrong `blob_sha256` pin | `unavailable` (error `PIN_MISMATCH`) | 1 | an input-pin problem, not a subject verdict |

The decisive point: a **nondeterministic** surface (the tool's own headline finding — the repeat
control differs) yields **exit 0**, and the pinned receipt committed at CAND proves it on real
data: `.ufo/evidence/round-21/f5/receipt.json` records `js-round-gate` with
`classification = "nondeterministic"` and `clean` tuple `25291d578518…` ≠ `clean_repeat` tuple
`dc4622235bdc…`, with **zero** `unavailable` surfaces — so that run exited 0 while carrying a
surface the tool itself calls non-invariant. Receipts §13. A reader of the row would read that
receipt as "0 clean".

Under §Gate standard's own words this is a **probe**, and §Verdict then requires the row to say
so: the map's `0 clean` is unreachable in the tool's semantics. The *pre-existing* round-21 row at
`SKILL.md:1975` says `kind = probe` and `0 all surfaces classified; 1 incomplete/failed
measurement` — which is **accurate** to the source. The candidate's new row silently upgrades the
same unchanged tool from `probe` to `gate` and rewrites `0 all surfaces classified` into
`0 clean`. The tool's bytes are identical at base and CAND (blob
`3a48aeccc55bc5ea4c6f436444f5a9ec69c83621` at both revs), so nothing in the tool justifies the
upgrade. Receipts §14.

## 3. F2 — the row's `1 failed` is a fiction: exit 1 means "unavailable", and it is
## environment-dependent, not subject-dependent

The row maps exit 1 to "failed". The tool's exit 1 is `done != len(rows)` — some surface was
`unavailable`. `unavailable` is produced by at least four *non-subject* causes, all confirmed:

1. **Host without bubblewrap.** `execute()` returns `{"error": "BWRAP_UNAVAILABLE"}` when
   `shutil.which("bwrap")` is None (`tools/env-diff.py:58-60`). Running the entry with `bwrap`
   absent from PATH: `ENVDIFF: classified=0/1`, exit **1**, with `error: None` on the surface —
   i.e. exit 1 with *no* diagnostic text at all. Receipts §7.
2. **Sibling repo missing.** `--fleet-root` pointing at an empty dir → all nine surfaces
   `PIN_UNREADABLE: <name>` → exit 1. Receipts §12.
3. **`--fleet-root` is a file** → exit 1.
4. **A pin mismatch** → `PIN_MISMATCH` → exit 1 (this one is at least about the input).

And the subject-failure case is *also* exit 1, but reported as `unavailable`, not `failed`
(fixture `failrun`, receipts §6): the target's clean-profile run exited 3, the tool set
`classification = unavailable`, exit 1. So exit 1 conflates "the measured subject misbehaved",
"the pin is wrong", "the sibling repo is absent" and "the host lacks bubblewrap" — and the row's
single word "failed" mislabels at least three of the four.

The decisive operational consequence: **the entry command's own success is not reproducible from a
clone.** The tool's `--fleet-root` default is `Path(__file__).resolve().parents[2]`
(`tools/env-diff.py:208`). From the lane that resolves to the fleet root
`/home/vgpnk/Projects/shokunin`; from the CAND clone at `$S/clone` it resolves to
`/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool04` — where no sibling repos exist. The row's entry
command, run verbatim from a clone, therefore yields:

```
ENVDIFF: classified=0/9 out=…/receipt-nofleet.json
exit=1
surfaces: 9 × PIN_UNREADABLE
```

Receipts §9. A reader following the row's entry command gets exit 1 = "failed" and a receipt of
nine `PIN_UNREADABLE` surfaces — a false red that the map gives no way to interpret, since the
row declares no `--fleet-root`. The pinned receipt at CAND is nonetheless reproducible **from the
lane** with the fleet root: `c2-count.py` (the round-21 counter) run against the lane at CAND
prints `C2: classified=9/9 tool_selftest=pass f5_entry=True`, exit 0 — so the underlying tool is
healthy; it is the row's entry command and verdict map that are unusable from a clone.

## 4. F3 — write scope: the row claims "TMPDIR-respecting selftest trees"; the sandboxes are
## hardcoded to `/tmp`

The row's Write scope cell says sandboxes live under `/tmp/tameshi-r21-envdiff.*` **and** that
selftest trees respect TMPDIR. Only the first is true, and the second is false for the dominant
tree family. `tools/env-diff.py:61`:

```python
with tempfile.TemporaryDirectory(prefix="tameshi-r21-envdiff.", dir="/tmp") as tmp:
```

`dir="/tmp"` is hardcoded — `TMPDIR` is ignored for every profile sandbox. Measured with
`strace -f -e trace=mkdir,mkdirat` over one self-test with `TMPDIR=$S/tmpX` (receipts §10):

- **132** mkdir events under the hardcoded `/tmp/tameshi-r21-envdiff.*` prefix, in **44** distinct
  sandbox directories;
- **14** mkdir events under `TMPDIR` — and those are the *pin-fixture* tree
  (`tameshi-r21-envdiff-pin.*`, `tools/env-diff.py:167`), which is the one place the tool uses the
  default `tempfile` dir and therefore does honour TMPDIR.

So the selftest writes 44 sandbox trees into the shared `/tmp` and only one tree into TMPDIR. The
row's phrasing "TMPDIR-respecting selftest trees" overstates the containment a reader would
infer, and the C3 counter's `run_cmd()` sets `TMPDIR` to a per-argv hash dir specifically to keep
runs isolated — for this tool that isolation is bypassed for the sandboxes. The lane trees
themselves are read-only as the row claims (the clone's `git status --porcelain` stayed empty
across every run), so that half of the cell holds.

This is also the mechanism behind the reproduction drift in §5: because the `host` profile is
`parent_env()` (`tools/env-diff.py:36-42`) it inherits the caller's `TMPDIR`, and inside the
bubblewrap sandbox `/` is `--ro-bind` and `/tmp` is `--tmpfs` (`:68-69`) — so a caller-set TMPDIR
on a read-only mount makes the host profile's `mktemp` fail and the host tuple differ from clean.

## 5. F4 — the pinned receipt does not reproduce from a scratch TMPDIR; the drift is deterministic

The row names `.ufo/evidence/round-21/f5/receipt.json` as a pinned value, and the contract's
`contract_sha256` in that receipt **matches** the contract at CAND exactly
(`5bd7024d0357ad3fb2a4b8550fd44f8371a3eb004f29948699368bea9d4c2bbd`) — the input side is intact.
But the receipt's *content* depends on the caller's `TMPDIR`, which the row does not disclose and
the "TMPDIR-respecting" claim implies is safe. Live re-runs of the row's entry command against the
real fleet root, same contract, same rev (receipts §13):

| run environment | surfaces differing from the pinned receipt |
|---|---|
| `TMPDIR=/tmp` | **0** (byte-identical classification set) |
| `TMPDIR` unset | **0** |
| `TMPDIR=$S/tmp` (scratch) | **5** — `js-kimi-census`, `bash-surface-census`, `bash-checklist-run`, `js-claims-check`, `js-sources-check` flip `invariant` → `env-sensitive` |

Deterministic: two independent scratch-TMPDIR runs produced the *same* five surfaces. Cause (shown
in §4): the `host` profile inherits `TMPDIR`; under bwrap the scratch path is on a read-only bind,
so the target's `mktemp` fails, the host profile's stderr digest changes, the host tuple stops
matching clean, and `classify()` returns `env-sensitive` instead of `invariant`. The pinned
receipt's `host`-profile stderr for `bash-surface-census` is `''`, while the drifted run's is
`"mktemp: failed to create directory via template '/fast/scratch/.../tmp/tmp.XXXXXXXXXX':
Read-only file system"`.

Consequence: the "pinned" receipt is only reproducible under an unset or `/tmp`-writable TMPDIR.
Anyone re-running the row's entry command in an isolated scratch environment gets a *different*
measurement of five surfaces from the committed pinned receipt while the tool still exits 0. This
is a pinned-value description that is not true of the tool in the environment the seat was told to
use.

## 6. What is NOT wrong (checked, and clean)

- **Self-test command, exit code, last-line finding id** — exact match to the row and to the tool
  source (§1). The id is a real tool diagnostic (`tools/env-diff.py:194`), not help text.
- **Usage probe** — exit 64, declared, and it is the tool's own usage code (`tools/env-diff.py:198-201`).
- **Verdict-map completeness** — every reachable exit code {0,1,2,64} is declared, and no other
  code is reachable (§1 table).
- **Owner `tameshi`** — correct.
- **Entry command names the tool and uses no shell metacharacters** — correct.
- **Pinned paths exist at REV** — both exist (`git cat-file -e` at CAND).
- **Lane trees read-only** — confirmed; clone `git status --porcelain` empty throughout; the
  sibling repos were only read (`git -C <sibling> show <rev>:<path>`), never written.
- **The round-21 c2 counter is green at CAND** — `c2-count.py` prints
  `C2: classified=9/9 tool_selftest=pass f5_entry=True`, exit 0. The underlying tool is sound;
  the defects are in the round-51 row, not in `tools/env-diff.py` (whose bytes are unchanged from
  base anyway).
- **Tool blob identical at base and CAND** — `3a48aeccc55bc5ea4c6f436444f5a9ec69c83621` both sides.
  The candidate changed only the *row*, not the tool.

## 7. Adjacent inconsistency (not in this row, noted for the L1)

`SKILL.md` at CAND carries **two live registry rows for the same tool** — `SKILL.md:1975` under
`### Round-21 gate/probe registry — finite environment differential` (kind `probe`, map `0 all
surfaces classified; 1 incomplete/failed measurement`) and `SKILL.md:2145` under
`#### Gate/probe registry — round 51` (kind `gate`, map `0 clean; 1 failed`). Neither section is
marked superseded (SKILL.md marks other stale registries, e.g. `### Round-14 historical registry —
superseded by round 15` at line 1597). The C3 counter is unaffected — its `HEAD_RE` matches only
`^#{2,4} Gate/probe registry`, so it reads the round-51 table and never the round-21 one — but a
human reader of the registry home sees two contradictory rows for `tools/env-diff.py`, and the
older one is the accurate one. `tools/registry.json` still points its `env-diff-selftest` entry at
the *old* row (`source: SKILL.md@370f2dff…:1975`), i.e. the machine-readable registry and the
round-51 prose row disagree about which row is current.

## 8. Bottom line for this row

The row **passes** the frozen C3 counter mechanically (`row_reason → None`, `run_row → None`) and
the counter's C3 verdict is unaffected by anything here. But against the source the row is wrong
on three fields the counter cannot see, all of which the C3 predicate's `cannot_see` clause names
explicitly:

| field | row says | source says |
|---|---|---|
| kind | `gate` | cannot fail against any expected value ⇒ **probe** (§Gate standard, `PROTOCOL.md:377-379`); the older row at `SKILL.md:1975` already says `probe` |
| verdict map | `0 clean; 1 failed` | `0` = all surfaces *classified* (a nondeterministic surface still exits 0); `1` = some surface *unavailable* — host-without-bwrap, missing sibling repo, bad pin, or subject failure, four different causes under one word (§2, §3) |
| write scope | "…and TMPDIR-respecting selftest trees" | 44/45 self-test sandbox trees are hardcoded to `/tmp` (`dir="/tmp"`, `tools/env-diff.py:61`); only the pin fixture honours TMPDIR (§4) |

Plus the pinned receipt's reproducibility caveat (§5): it reproduces under `TMPDIR` unset or
`/tmp`, and deterministically drifts on five surfaces under a scratch TMPDIR.

The C3 predicate as frozen does not test any of this, and the row as written satisfies the frozen
predicate. Whether the frozen predicate *should* test it is the L1's call — I am not amending the
contract, the counter, the row or the tool. My measurement is that the row's kind, verdict map
and write scope are not true of `tools/env-diff.py` at CAND.

## 9. Files written

- `.ufo/waves/round-51/w2/T51W2ExecTool04.md` (this report)
- `.ufo/waves/round-51/w2/@P@ExecTool04/receipts.txt` (raw receipts, sections 0–14)

Scratch `/fast/scratch/hyaku/tameshi-r51/T51W2ExecTool04` deleted before yield. No tool installed
or updated. No mutation in any lane, fleet or sibling repo — fixture git operations were confined
to `mktemp`-style directories under my own scratch, each with `git rev-parse --show-toplevel`
asserted equal to the fixture directory before its commit.
