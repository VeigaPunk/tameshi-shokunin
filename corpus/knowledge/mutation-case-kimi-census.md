# Mutation case — kumitate `kimi-census.mjs` (TAMESHI-R2-1)

Run date 2026-10-14. Lane: tameshi (round 2; plan `tameshi-shokunin/plans/round-2.plan.md`,
axis: depth). Substrate: kumitate-shokunin **read-only** — every mutant is a copy under
`/tmp/tameshi-r2-1-work/`, and no fleet file was written. No live `~/.kimi-code` path was
read: every run is `--selftest` (fixtures under the suite's own `mkdtemp` root) or `--root`
pointed at an empty dir under `/tmp`.

Anchors: **O** = observation (file:line or command output), **I** = inference, **U** =
unknown. A bare `kimi-census.mjs:NNN` is `kumitate-shokunin/scripts/kimi-census.mjs` at the
revision pinned below.

Artifact under test (O: `sha256sum`, `stat`, `git rev-parse`): sha256
`83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426`, 896 lines, 43273 B,
mtime 2026-10-13 18:53:12; kumitate repo `175de6ba2e9e904010411b19cab27e0af9aad3d4`,
`git status --porcelain -- scripts/kimi-census.mjs` empty.

## 0. Method and headline

- O: control run, unmutated copy — `node pristine.mjs --selftest` →
  `KIMI_CENSUS_SELFTEST: 43/43 pass` / `VERDICT: PASS`, exit 0 (node v24.21.0).
- O: each defect = ONE exact-string replacement applied to a fresh copy of the pristine
  copy; the driver asserts the old string occurs exactly once before writing
  (`mutate_driver.py --check` → `all unique`, first-line match on all 10). No defect
  compounds with another.
- O: per-defect evidence: `node mutant-<id>.mjs --selftest` full stdout →
  `evidence/<id>.selftest.txt`; exit code + mutant sha256 → `evidence/<id>.meta.json`;
  aggregate → `evidence/results.json`.
- O: **kill rate 8/10 (80 %)**; survivors D2, D10. No inconclusive run — each of the
  11 runs (control + 10) produced a definitive suite verdict; the whole sweep took 7.0 s
  wall against the 300 s timeout.
- O: suite count held: every mutant run still enumerated the full suite (`<n>/43`), and
  all three green runs printed exactly `KIMI_CENSUS_SELFTEST: 43/43 pass`.
- O: restore proof — original sha256 before `83016d45…4f426` and after `83016d45…4f426`;
  size 43273 B and mtime unchanged; kumitate working tree clean for that path.
- Context: the corpus carries no kill-rate measurement on any gate yet
  (`corpus/README.md:7` records that gap); this note is tameshi's first measured one.

## 1. Kill-rate table

| # | Defect class | Injected defect (ref = edit site) | Exit | Suite line | Verdict | Failing cases |
|---|---|---|---|---|---|---|
| — | control | unmutated copy | 0 | `43/43 pass` / `VERDICT: PASS` | green | 0 |
| D1 | off-by-one count | K2 counted dir `counted: 18` → `17` (kimi-census.mjs:105) | 1 | `27/43 pass` / `FAIL` | **killed** | 16 (incl. the exact baseline) |
| D2 | off-by-one count (findings cap) | `findings.slice(0, 6)` → `slice(0, 5)` (kimi-census.mjs:378) | 0 | `43/43 pass` / `PASS` | **survived** | 0 |
| D3 | inverted condition | `if (!e.children.includes(n))` → `if (e.children.includes(n))` (kimi-census.mjs:332) | 1 | `27/43 pass` / `FAIL` | **killed** | 16 |
| D4 | dropped arm | root-stray reporting loop deleted (kimi-census.mjs:351-353) | 1 | `40/43 pass` / `FAIL` | **killed** | 3 |
| D5 | dropped arm (presence gate) | chain presence `gens.length > 0` → `true` (kimi-census.mjs:255) | 1 | `42/43 pass` / `FAIL` | **killed** | 1 |
| D6 | wrong mode pin | `server.token` floor `0o600` → `0o644` (kimi-census.mjs:124) | 1 | `41/43 pass` / `FAIL` | **killed** | 2 |
| D7 | weakened predicate (floor semantics) | `(mode & floor) !== floor` → `(mode & floor) === 0` (kimi-census.mjs:306) | 1 | `41/43 pass` / `FAIL` | **killed** | 2 |
| D8 | wrong exit-code mapping | `failClosed` `return 2` → `return 1` (kimi-census.mjs:396) | 1 | `40/43 pass` / `FAIL` | **killed** | 3 |
| D9 | weakened secrecy pin | secret kind pin `isLeaf(kind)` → `kind === 'file'` (kimi-census.mjs:292) | 1 | `41/43 pass` / `FAIL` | **killed** | 2 |
| D10 | wrong reported constant | `FROZEN.K2 25` → `24` (kimi-census.mjs:145) | 0 | `43/43 pass` / `PASS` | **survived** | 0 |

By class: off-by-one 1/2 · inverted condition 1/1 · dropped arm 2/2 · wrong mode pin 1/1 ·
weakened predicate 1/1 · wrong exit mapping 1/1 · weakened secrecy pin 1/1 · wrong
reported constant 0/1.

Failing-case labels of the narrow kills (O: `evidence/<id>.selftest.txt`):

- D4 (3): `UNLISTED: a planted undeclared root child …`; `UNLISTED: a hidden root child is
  gated too …`; `root enum is orthogonal to counted-dir drift …` — exactly the three
  root-enumeration cases; no other case moves.
- D5 (1): `MEMBER_MISSING: the drift chain vanished entirely (presence is gated)` — a
  single-case tripwire.
- D6 (2): `SHAPE_DRIFT: server.token below its 0600 floor (checked counts the failure)`;
  `secrecy: server.token is a FIFO → still CLEAN …` (collateral, see §3).
- D7 (2): `SHAPE_DRIFT: credentials/ below its 0700 floor`; `SHAPE_DRIFT: server.token
  below its 0600 floor …`.
- D8 (3): the three fail-closed cases (`--root /nonexistent`, unreadable root, `--json`
  fail-closed).
- D9 (2): `secrecy: server.token is a FIFO → still CLEAN …`; `secrecy: a dangling symlink
  token is never followed (lstat-only → CLEAN)`.
- D1/D3 (16 each): the exact green baseline (`green fixture → CLEAN exit 0, members=49
  checked=49 chain=3 info=4`), the two `--json` family/totals cases, and 13 more — the
  remaining CLEAN/exact-line cases plus the count-string (`'19 children, 18 declared'`)
  and no-UNLISTED asserts; each fails because the green fixture itself now drifts. Full
  lists in `evidence/results.json`.

## 2. Surviving-defect class analysis

**D2 — render truncation off-by-one (kimi-census.mjs:378).** O: 43/43 PASS.
O: the boundary is never exercised — a probe copy (pristine + `appendFileSync` of
`findings.length` at `renderVerdict` entry; output unchanged, still 43/43) logged all 28
text-mode verify runs the suite makes: findings-count distribution `0×8, 1×19, 2×1`,
**max = 2**. O: the DRIFT verdict is asserted only by prefix —
`lastLine(run).startsWith('KIMI_CENSUS: DRIFT')` (kimi-census.mjs:498) plus substrings;
the only exact verdict-line assert is the CLEAN line (`lastLine(r) === 'KIMI_CENSUS:
CLEAN (members=49 checked=49 chain=3 info=4)'`, kimi-census.mjs:511-512).
O (non-equivalence): on an empty root (28 findings) — pristine prints six ids then
`+22 more`; D2 prints five ids then `+23 more`; both exit 1. The mutant is observably
different on ≥6-finding input and the suite cannot see it.

**D10 — wrong reported constant (kimi-census.mjs:145).** O: 43/43 PASS.
O: the only assert touching the frozen block is `j.totals.frozen.K5 === 3`
(kimi-census.mjs:526); the text `FAMILY … frozen=${FROZEN[f]}` line
(kimi-census.mjs:415) and `totals.frozen` (kimi-census.mjs:365) carry no assert anywhere.
O (non-equivalence): same empty root — pristine `FAMILY K2  members=0  checked=0
frozen=25`; D10 `… frozen=24`.

**Shared class: reported-but-unasserted surfaces.** Both survivors change *displayed
report* data and nothing the suite's asserts read. D2 lives in the verdict line's tail
past the asserted prefix; D10 lives in a constant only *reported* (the header itself calls
FROZEN an aid "for callers that compare to round 19/20", kimi-census.mjs:144-145).
I: the suite's assert vocabulary (exit code + prefix + substrings + selected counts)
pins behavior, not reporting completeness — a mutant confined to reporting survives by
construction. Whether other gates share this class is unmeasured (U4).

## 3. What the 43-case suite protects — and does not

**Protected (each proven by the kill that died on it):**

- Declared-count ↔ live-count agreement, both directions: D1 (a single-table edit, which
  desyncs `MEMBERS.counted` :105 from the duplicate `ENUMERABLE.childCount` :137) dies on
  16 cases including the exact baseline.
- The UNLISTED child predicate: D3 dies on 16 cases — the inversion flags every declared
  child of a green fixture, so the baseline itself catches it.
- The root-enumeration arm, including hidden children: D4 dies on exactly the three
  root-enum cases (arm isolation: deleting the reporting loop moves no other case).
- Drift-chain presence: D5 dies on the single no-chain case — thin, but a working tripwire
  for this defect.
- The fail-closed exit map: D8 dies on exactly the three fail-closed cases.
- Mode-floor value and checked accounting: D6 dies on the two loose-mode cases; the FIFO
  case falls as collateral (O: `fixtureTree` chmods members to `m.modeFloor ?? …`
  :437/:441, and the FIFO is made at fixed `-m 600` :637, so the mutant floor also fails a
  clean fixture path).
- Floor *semantics*: D7 dies on the two loose-mode cases. O: under the mutant both loose
  fixtures report `KIMI_CENSUS: CLEAN (members=49 checked=49 …)`, exit 0 — i.e. the
  fixtures use partial-overlap modes (0o500 vs 0o700 floor; 0o400 vs 0o600 floor) that
  discriminate "contains the floor" from "intersects the floor". I: a suite that tested
  only modes sharing **no** floor bits (e.g. 0o000) would have missed this class.
- The secret inode-kind pin: D9 dies on exactly the two anti-read fixtures (FIFO token,
  dangling symlink) — the secrecy cases double as leaf-pin guards.

**Not protected (measured gaps):**

- The verdict-line truncation boundary and its `+N more` arithmetic (D2): max findings in
  any suite run = 2 against a cap of 6. Because the DRIFT asserts are prefix-based (:498),
  even a case reaching 6 findings would not pin the tail.
- Frozen-block constants other than K5 (D10): only `frozen.K5` is asserted (:526).
- (I) Both gaps sit in the same region: reporting surfaces whose values no case reads.
  A caller consuming `--json` or the FAMILY lines is protected by nothing here.

**Scope (I):** this experiment mutates one artifact with single-text-edit defects. It does
not measure the live verify path against substrate drift (the suite's complement), and it
says nothing about coordinated multi-edit rewrites (U1).

## 4. Reproduce

Scratch (all under `/tmp/tameshi-r2-1-work/`): `pristine.mjs` (byte-copy of the pinned
artifact), `mutant-D{1..10}.mjs`, `probe.mjs`, `mutate_driver.py`, `evidence/`,
`empty-root/`. Driver spec = the ten exact edits, shown here so the run can be rebuilt
from the note alone (each applied to a fresh copy):

```
D1  kimi-census.mjs:105   kind: 'dir', counted: 18 },                  -> kind: 'dir', counted: 17 },
D2  kimi-census.mjs:378   findings.slice(0, 6).map                    -> findings.slice(0, 5).map
D3  kimi-census.mjs:332     if (!e.children.includes(n)) {            ->   if (e.children.includes(n)) {
D4  kimi-census.mjs:351-353   the three-line `for (const n of strays) { err(...) }` block deleted
D5  kimi-census.mjs:255   const present = gens.length > 0;            -> const present = true;
D6  kimi-census.mjs:124   kind: 'file', secret: true, modeFloor: 0o600 }, -> …0o644 },
D7  kimi-census.mjs:306   (mode & m.modeFloor) !== m.modeFloor        -> (mode & m.modeFloor) === 0
D8  kimi-census.mjs:396   return 2;                                   -> return 1;
D9  kimi-census.mjs:292   ? (… : isLeaf(kind))                        -> ? (… : kind === 'file')
D10 kimi-census.mjs:145   FROZEN K2: 25                               -> K2: 24
```

Commands (O: run in this order):

```
rm -rf /tmp/tameshi-r2-1-work && mkdir -p /tmp/tameshi-r2-1-work/evidence
cp -p kumitate-shokunin/scripts/kimi-census.mjs /tmp/tameshi-r2-1-work/pristine.mjs
sha256sum /tmp/tameshi-r2-1-work/pristine.mjs          # 83016d45…4f426
python3 /tmp/tameshi-r2-1-work/mutate_driver.py --check
python3 /tmp/tameshi-r2-1-work/mutate_driver.py --run  # control + 10 mutants
node /tmp/tameshi-r2-1-work/mutant-D2.mjs  --root /tmp/tameshi-r2-1-work/empty-root | tail -1
node /tmp/tameshi-r2-1-work/mutant-D10.mjs --root /tmp/tameshi-r2-1-work/empty-root | grep 'FAMILY K2'
```

Sensitivity check expected from the note alone: D2's verdict line must show one fewer id
and `+23 more`; D10's FAMILY K2 line must read `frozen=24`.

## 5. Calibration and errata (append-only)

E1 — the author's pre-run expectation held for 9/10 defects; it was **wrong on D7**. The
expectation filed D7 as a survivor (reasoning: "the loose fixtures lack the floor bits
entirely, so both predicates fire"). Measured: both loose fixtures go CLEAN under D7 and
the mutant dies on the two mode cases. The error was in the *reasoning about the fixture
modes*, not the edit: credentials 0o500 vs floor 0o700 and server.token 0o400 vs floor
0o600 share bits with their floors, so `(mode & floor) === 0` admits them while
`!== floor` rejects them (§3, D7). Recorded as a calibration miss.

## 6. Unknowns

- U1 — a *coordinated* edit of both count tables (`MEMBERS.counted` :105 **and**
  `ENUMERABLE.childCount` :137) was not probed. (I: the literal-count asserts
  `'19 children, 18 declared'` (:577, :730) would still kill it; not measured.)
- U2 — only single-text-edit defects. Multi-site semantic rewrites, check reordering,
  and timing/timeout mutants are outside this experiment.
- U3 — the max-findings probe covers text-mode verify runs only (`renderVerdict` path);
  `--json` and fail-closed runs are not in the distribution.
- U4 — survivor-class generality: one artifact. Whether other gates' suites share the
  "reported-but-unasserted" gap is unmeasured.
- U5 — kill-rate stability across node versions/hosts: measured only on node v24.21.0,
  this host, 2026-10-14.
- U6 — nothing here measures the suite against *substrate* drift; a hermetic suite never
  reads the live tree by construction.## Errata (round 5) — VER-T1 cross-check landing (append-only)

Applied 2026-10-14 by lane T5-2; scope: this file only; nothing above this block
is edited. Source: **VER-T1**, the round-4 independent cross-check of the
arm-class matrix's row E ("Unreached arms"), against the pinned bytes of
`kumitate-shokunin/scripts/kimi-census.mjs` @ sha256 `83016d45…4f426` (scratch
`/tmp/w4h-ver-t1-mut/`; cited in the round-4 `LOG.md` entry). Entry **E2**.

E2 (precision — "unreached" wording scope for this JS case). VER-T1 re-cut the
two JS arm-deletion mutants independently (D4 → 40/43 on exactly the three
root-enum labels; D5 → 42/43 on the singleton chain label — both identical to
§1), and re-measured the D2 boundary with its own probe: 28 text-mode verify
runs, findings distribution `0×8, 1×19, 2×1`, max **2** vs the cap of 6
(`:378`; the cap and the prefix-based DRIFT assert `:498` re-read live by T5-2
on the pinned sha). Two readings the numbers support must be kept apart:

1. the ≥6-findings truncation region is **fixture-unreached** — no suite run
   reaches the boundary, so the region is absent from the fixture set, not
   merely under-asserted; and
2. D2's survival is **assert-caused, not unreachability-caused** — the DRIFT
   assert is prefix-based (`:498`), so even a 6-finding fixture would not pin
   the `+N more` tail. D2 remains a reported-but-unasserted survivor (matrix
   rows A/D), **not** an instance of the unreached-arm class; that class's sole
   instance among the 20 mutants is bash B5.

Wording consequence: matrix §6's literal "Nothing in the JS case is an arm no
fixture reaches" overstates as written — any such generalization must be scoped
to the probed arm-deletion mutants (D4/D5). Cited here because the JS case's
evidence originates in this note; this is a scope note only — no verdict, cell,
or count in §0-§6 above changes, and §5's E1 stands. Companion VER-T1 erratum
(chmod enumeration `:608`/`:654`) lands in `knowledge/arm-class-matrix.md`
(E3 there).