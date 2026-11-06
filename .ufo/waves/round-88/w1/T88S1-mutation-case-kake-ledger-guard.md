source: S312 Python 3.15, Built-in Types: bytes and bytearray operations (docs, tier A, mined) — https://docs.python.org/3/library/stdtypes.html, §bytes.rindex (`id="bytes.rindex"` @4143; quote at `.ufo/evidence/round-88/sources/s312-stdtypes.html:4147-4148`: "Like rfind() but raises ValueError when the subsequence sub is not found") and §bytes.startswith (`id="bytes.startswith"` @4171; quote at `.ufo/evidence/round-88/sources/s312-stdtypes.html:4175`: "Return True if the binary data starts with the specified prefix, otherwise return False"); S001 Stryker mutant states and metrics (docs, tier A, mined) — relied on only for the `detected / valid` arithmetic behind the 50 % headline (scope: Stryker's own mutant-state and metric definitions, `corpus/SOURCES.md:12`); S006 shmutant README (code, tier A, mined) — scope-checked, not used as authority: its verdict grammar is shmutant's own bash semantics (scope: "authoritative only for its own semantics", `corpus/SOURCES.md:17`), so no verdict here is graded by it; kake `scripts/ledger_append_guard.py` @ e8d3a924249983972e5163d160cf236487986c55 (git blob `ed2a135e…9b56`, file sha256 `0c12838e…4067`, 6969 B, 153 lines, mode 100755; spec `.ufo/evidence/round-88/c1/py-kake-ledger-guard.defects.spec:2-4`), read-only; procedure: `corpus/knowledge/mutation-case-kumitate-round-gate.md` (case 7)
verified-at: 2026-11-06; spec sha256 `724beed3…2689e` written 15:44:41 -03:00, bound into the counter 15:47:51, committed with the controls in `6998726f` (`pre-freeze/sha256s.txt:2`, `pre-freeze/timeline.txt:1-4`); sweep `2026-11-06T18:58:27Z` (`c1/sweep.txt:2`); landing replay `2026-11-06T18:59:19Z` (`landing/runner-regression-candidate.txt:2`)
recheck: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show e8d3a924249983972e5163d160cf236487986c55:scripts/ledger_append_guard.py | sha256sum` → `0c12838e…4067`; `sha256sum /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-88/c1/py-kake-ledger-guard.defects.spec` → `724beed3…2689e`; `bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh --regression` → `REGRESSION_CASE py-kake-ledger-guard: PASS` (`landing/runner-regression-candidate.txt:59`)

# Mutation case 11 — kake `scripts/ledger_append_guard.py` (round 88, R88-C1)

The eleventh recorded case and the ledger's first Python leg (`py-kake-ledger-guard`,
`tools/mutate-and-run.sh:100` at `28ec588`). The target is a kake `scripts/*`
primary surface: the lane's Core names the recorded mutation legs' gates as
read-only primary surfaces (`plans/round-88.plan.md`, R88-C1, quoting
`PROVINCE.md` Core). kake's tree is not written: the measured bytes are a
scratch copy materialized from kake's git object store (`git show`),
sha256-equal to the pin (`c1/sweep.txt:3`), and the runner's restore line proves
the copy returned byte-identical (`c1/sweep.txt:54`). No owner opt-in was
required by that Core clause; none was sought.

A bare `ledger_append_guard.py:NN` below is the pinned blob at `e8d3a92`; a bare
`sweep.txt:NN` / `sweep-results.tsv:NN` is under `.ufo/evidence/round-88/c1/`,
and a bare `landing/…:NN` is under `.ufo/evidence/round-88/`.

## 0. Pin and suite

- Target: rev `e8d3a924249983972e5163d160cf236487986c55` (kake-shokunin
  <kake@shokunin.local>), git blob `ed2a135e…9b56`, file sha256
  `0c12838e…4067`, 6969 B, 153 lines, mode 100755
  (`py-kake-ledger-guard.defects.spec:2-4`; `c1/sweep.txt:3`). The landing
  receipt records the same rev, mode and sha (`landing/runner-regression-candidate.txt:55`).
- Suite: the gate's own `--selftest`, run as `env -i` + `python3 -I "$MUTANT"
  --selftest` in a per-defect sandbox, two checks: a pure append passes and an
  in-place edit fails (`py-kake-ledger-guard.defects.spec:5-6`; the leg's exact
  string at `tools/mutate-and-run.sh:1591`, `28ec588`). The verdict oracle is
  exit status only: nonzero = KILLED, 0 = SURVIVED, 124/126/127 = INCONCLUSIVE
  (`tools/mutate-and-run.sh:38`). The control is GREEN, exit 0, `2/2`
  (`c1/sweep.txt:5-8`).
- Fixture: one ledger, `.ufo/waves/round-58/receipt-rewrites.json`, committed
  into a mkdtemp fixture repo by the suite itself (`ledger_append_guard.py:88-99`);
  the sandbox bounds git discovery with `GIT_CEILING_DIRECTORIES` (spec:8-9).
  No fixture writes outside its sandbox.

## 1. The measured table — 5/10 killed (50 %)

Headline: 10 defects, 5 KILLED, 5 SURVIVED, 0 inconclusive, kill-rate 50 %
(`c1/sweep.txt:56`), measured `2026-11-06T18:58:27Z` under runner sha256
`977de470…0bda` (`c1/sweep.txt:1-2`). The control was green (exit 0, 73 ms,
pristine sha = pin; `c1/sweep.txt:5`) and the restore line shows
before = after = pin (`c1/sweep.txt:54`). Under S001's arithmetic
(`detected / valid`, `detected = killed + timeout`) that is 5/10 with no
timeouts (`corpus/SOURCES.md:12`).

Reading the receipt: `fixture append: passed|failed` is the first check; on the
`fixture non-prefix` line the word is the *fixture's* outcome, not the check's —
`failed` means the guard rejected the edited carrier (the wanted behaviour; the
check is `red`), `passed` means the guard accepted the edit and the check fails
(`ledger_append_guard.py:113-118`). The control prints `failed … byte 126` and
`2/2` (`c1/sweep.txt:6-8`).

| id | class | edit at the pin | pred. | meas. | exit | selftest reason (receipt) |
|---|---|---|---|---|---|---|
| K_CUT_WHOLE | kill-aimed | `cut = len(base)` (`:37`) | KILLED | KILLED | 1 | append fixture fails: the whole base is not a prefix of a carrier that inserts before the final `]`; the edit is still detected at 126 → 1/2 (`sweep.txt:9-12`; `sweep-results.tsv:2`) |
| K_STARTSWITH | kill-aimed | `startswith(head[:1])` (`:39`) | KILLED | KILLED | 1 | append passes; the em-dash edit is accepted (`first divergence at byte None`) → 1/2 (`sweep.txt:13-16`; `sweep-results.tsv:3`) |
| K_FILES_EQ | kill-aimed | append check `files == 2` (`:106`) | KILLED | KILLED | 1 | the one-ledger fixture has `files == 1`, so the append check is false; the edit is still red → 1/2 (`sweep.txt:17-20`; `sweep-results.tsv:4`) |
| K_GLOB | kill-aimed | glob `receipt-rewrite.json` (`:32`) | KILLED | KILLED | 1 | no ledger matches → `files=0`, `prefix_preserved=False`; both checks false, and the `res['detail'][0]` print raises IndexError at `:115` before the tally → traceback, exit 1 (`sweep.txt:21-29`; `sweep-results.tsv:5`) |
| K_SHOW_RC | kill-aimed | `show.returncode == 0` (`:61`) | KILLED | KILLED | 1 | every ledger is recorded "base does not carry the path" and never compared; append fails, the edit is accepted → 0/2 (`sweep.txt:30-33`; `sweep-results.tsv:6`) |
| S_HEAD_SHORT | hole-aimed | `head = base[:cut - 1]` (`:38`) | SURVIVED | SURVIVED | 0 | the em-dash edit at byte 126 is before the dropped byte, and the appended carrier keeps the shortened head → 2/2 (`sweep.txt:34-37`; `sweep-results.tsv:7`) |
| S_OFFSET_EQ | hole-aimed | `if head[i] == carrier[i]` (`:42`) | SURVIVED | SURVIVED | 0 | the `startswith` boolean is untouched; only the printed offset changes 126 → 0 → 2/2 (`sweep.txt:38-41`; `sweep-results.tsv:8`) |
| S_OK_ALL | hole-aimed | `ok_all = ok` (`:72`) | SURVIVED | SURVIVED | 0 | one ledger per fixture, so "last" equals "all" → 2/2 (`sweep.txt:42-45`; `sweep-results.tsv:9`) |
| S_VACUOUS | hole-aimed | `prefix_preserved` drops `any(compared)` (`:78`) | SURVIVED | SURVIVED | 0 | every fixture has one compared ledger, so `any(compared)` is true → 2/2 (`sweep.txt:46-49`; `sweep-results.tsv:10`) |
| S_RED_FILES | hole-aimed | `red` drops `files == 1` (`:111`) | SURVIVED | SURVIVED | 0 | every fixture has `files == 1`, so the dropped conjunct is redundant → 2/2 (`sweep.txt:50-53`; `sweep-results.tsv:11`) |

Two receipts need reading past the verdict line:

- **K_GLOB is not an accidental red.** Both checks are already false before the
  crash: with `files=0`, `prefix_preserved` is `True and any([])` = False
  (`:78`), so the append check (`:106`) is false and `red` (`:111`) is
  `False and files == 1` = false. The selftest would print `0/2` (`:116-117`);
  the `detail[0]` print (`:115`) instead raises because there is no detail row. The
  verdict is a witness kill; the traceback is an output artifact of the same
  zero-match state. (S006's witness-vs-accidental vocabulary is shmutant's,
  not this gate's; it is not applied as authority here.)
- **K_SHOW_RC's kill is broad, not targeted.** Inverting the base-read success
  test (`:61`) skips every ledger (the fixture repo's base does carry the
  path), so both fixtures fail. The suite has no fixture for the branch the
  inversion imitates — a base that genuinely lacks the path — and it does not
  assert that branch.

## 2. Predictions vs measured — 10/10

The spec was pre-registered with 10 defects, ids and predictions fixed before
any mutant ran: 5 kill-aimed (`PREDICT KILLED`, `spec:12-36`) and 5 hole-aimed
(`PREDICT SURVIVED`, `spec:38-62`), composition stated at `spec:7`. The
measured table is 5 KILLED + 5 SURVIVED (`sweep-results.tsv:2-11`), so every
prediction held: **10/10, no flips**. The landed leg replays the same table and
reports `match=10/10 … flips=0` (`landing/runner-regression-candidate.txt:57`).

Timing disclosure: the spec mtime is 15:44:41 -03:00, the counter's 15:47:51,
and the first kake mutant ran at 15:53 inside the `doctored` control
(`pre-freeze/timeline.txt:1-4`). The spec, counter and nine controls were
committed together in `6998726f`, so git alone does not order the predictions
before the first mutant; the file timestamps do, and the spec bytes are
unchanged since (sha256 `724beed3…2689e`, `pre-freeze/sha256s.txt:2`). Two
pre-freeze controls already show the binding is real: `doctored` inverts every
predicted verdict and agrees 0/10 (`reason=flip-K_CUT_WHOLE:SURVIVED->KILLED`,
`pre-freeze/ctl-doctored.out:11-12`), while `unprereg` changes one comment byte
and still counts the leg (`legs=11 python_legs=1`) but refuses it on
`prereg=mismatch` (`pre-freeze/ctl-unprereg.out:11-12`). The counter's positive
control is the base replay of the ten historical legs (`pre-freeze/ctl-nowork.out:11`).

## 3. Survivor classes — five holes, five killing fixtures

Each class names the hole the two-check suite leaves and the fixture that would
close it. The fixture arithmetic was re-derived from the pinned functions and
checked in `.ufo/waves/round-88/w1/T88S1-fixture-geometry.out` (all checks pass;
source `T88S1-fixture-geometry.py`); it is a re-implementation check, not a gate
run.

| survivor | class | why it survives at the pin | fixture that would kill it |
|---|---|---|---|
| S_VACUOUS | vacuous pass on zero ledgers | every fixture carries one compared ledger; the `any(compared)` guard at `:78` is never false, so dropping it is unobserved (`sweep.txt:46-49`) | a tree with no *compared* ledger (an empty governed set, or a ledger absent from the base); assert `prefix_preserved` is False / exit 1 (`:149`). Pristine passes it as a refusal; the mutant returns True / exit 0 (probe: `S_VACUOUS-*`) |
| S_OK_ALL | multi-ledger conjunction | `ok_all = ok_all and ok` (`:72`) and `ok_all = ok` agree when there is one ledger (`sweep.txt:42-45`) | two ledgers with the edited one sorting first and an appended one second; assert `prefix_preserved` False with `files == 2`. The mutant keeps the last (passing) ledger and returns True / exit 0 (`:149`; probe: `S_OK_ALL-*`; order matters) |
| S_OFFSET_EQ | unasserted offset | `prefix_probe`'s offset is printed, never asserted; the boolean comes from `startswith` (`:39`), so exits do not move (`sweep.txt:38-41`) | assert `first_divergence` equals the em-dash byte on the existing non-prefix fixture: 126 (`sweep.txt:7`; probe `fixture-emdash-offset-126`). The mutant reports 0 (`sweep.txt:40`) |
| S_HEAD_SHORT | one-byte head slack | `head = base[:cut - 1]` (`:38`) drops the byte at `cut-1`; the em-dash edit at 126 is earlier, so the shortened head still catches it, and the append fixture keeps it as a prefix (`sweep.txt:34-37`) | append, then flip the single byte at `cut-1` — the space at byte 151, `cut=152` (probe: `fixture-cut-1-is-space`). The short head accepts the flipped carrier; the full head rejects it (probe: `S_HEAD_SHORT-*`) |
| S_RED_FILES | redundant red conjunct | `red = prefix_preserved is False and files == 1` (`:111`) is only ever evaluated with `files == 1`; `red` is selftest-local and never read by the gate's exit path (`sweep.txt:50-53`) | no gate fixture can kill it. A meta-fixture that asserts `red` stays False when `files != 1` (zero- or two-ledger tree) kills the mutant (probe: `S_RED_FILES-*`); recorded as equivalent for gate behaviour, weakening only the suite's net |

The last entry is the same disposition as case 7's CKIND: a mutant that only
changes the suite's own bookkeeping cannot be distinguished by any observation
of the gate. S_OFFSET_EQ is different — it corrupts a real output field
(`first_divergence` in the detail/JSON), so a `--root --json` fixture or the
offset assert above is a genuine behavioural test, not a meta-test.

## 4. Limits

- One pin (`e8d3a92`), one host, one suite of **two checks** (`spec:5-6`;
  control `2/2`, `sweep.txt:8`). The 50 % is a property of this suite at this
  pin, not of kake's guards in general.
- The gate's `--root` mode, `--base-file` path, `--json` output and
  `DEFAULT_BASE` (`ledger_append_guard.py:31,123-126`) are **outside the
  suite**: the selftest calls `check_tree(repo, rev)` twice (`:105,:110`) with
  no base-file and never uses the CLI. The `base_file` branch (`:52-56`) and
  the missing-base-path branch (`:61-64`) have no fixture; the former is
  wholly unexercised.
- The fixture is a single ledger in a single round directory (`:88`), so
  multi-ledger and empty-tree behaviour are unobserved — the source of three of
  the five survivors (S_VACUOUS, S_OK_ALL, S_RED_FILES).
- The oracle is exit status only (`tools/mutate-and-run.sh:38`), so a crash
  after both checks are false (K_GLOB) is recorded KILLED like an assertion
  failure, and a survivor whose only change is printed text (S_OFFSET_EQ) is
  recorded SURVIVED even though its output is wrong.
- 5/10 mixes kill-aimed and hole-aimed defects by design; prediction accuracy
  (10/10) and kill rate are separate readings.
- The ten mutants are single-edit, non-hostile edits; the runner's restore
  proof (`sweep.txt:54`) covers byte identity, not confinement.
- The sweep ran under the pre-leg runner `977de470…0bda` (`sweep.txt:1`); the
  landed leg re-ran the same spec and suite under `0a0e46de…5a4a`
  (`landing/runner-regression-candidate.txt:1,55-59`) with the same table, which
  closes the "sweep predates the leg" gap.

## 5. Reproduce

Materialize the pinned bytes and run the standalone sweep under the landed
runner interface (`--target/--defects/--suite`; `tools/mutate-and-run.sh:215-227`):

```sh
S=/fast/scratch/hyaku/tameshi-r88/<seat>/replay
mkdir -p "$S"
git -C /home/vgpnk/Projects/shokunin/kake-shokunin \
  show e8d3a924249983972e5163d160cf236487986c55:scripts/ledger_append_guard.py \
  > "$S/target.ledger_append_guard.py"
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh \
  --target "$S/target.ledger_append_guard.py" \
  --defects /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-88/c1/py-kake-ledger-guard.defects.spec \
  --suite 'h="$WORKDIR/sandbox-$DEFECT_ID"; mkdir -p "$h/home" "$h/tmp" && cd "$h" && exec env -i PATH="$PATH" HOME="$h/home" TMPDIR="$h/tmp" LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CEILING_DIRECTORIES="$h" python3 -I "$MUTANT" --selftest' \
  --workdir "$S/work" --label py-kake-ledger-guard
```

Expected last line: `MUTATE: DONE (target=py-kake-ledger-guard defects=10
killed=5 survived=5 inconclusive=0 kill-rate=50%)` (`c1/sweep.txt:56`). The
original sweep used the pre-leg runner `977de470`; the suite string above is the
landed leg's (`tools/mutate-and-run.sh:1591`).

The governed replay, at the candidate revision:

```sh
bash /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh --regression
```

Expected: `REGRESSION_CASE py-kake-ledger-guard: PASS (band: killed-delta<=0
flips<=0 inconclusive=0 defects=10)` and
`REGRESSION: PASS (cases=11 passed=11; ledger legs exact: killed-delta<=0
flips<=0)`, exit 0 (`landing/runner-regression-candidate.txt:59-60,62`); the
pin line is `landing/runner-regression-candidate.txt:55` and the expected
kill-rate `py-kake-ledger-guard=5/10` is on `:4`. The runner's own selftest is
`108/108 pass`, exit 0 (`landing/runner-selftest-candidate.txt:109,111`). The
leg's table is embedded at `tools/mutate-and-run.sh:655` and its count at
`:1595`.
