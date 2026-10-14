# Mutation case — tsukuroi `tsukuroi-census.sh` census-v2 (T5-1)

Run date 2026-10-14. Lane: tameshi (round 5; plan `tameshi-shokunin/plans/round-5.plan.md`,
axis: depth — the third cross-author data point). Substrate: tsukuroi-shokunin **read-only**;
every mutant is a byte copy under `/tmp/w5-tameshi-1-work/`, and this note is the only fleet
file written by this run (the corpus/README row and the `LOG.md` entry fold in at lane
review). No external site contacted; no secret file read.

**Incident I1 — the substrate moved mid-run, by a concurrent lane (headline, not appendix).**
Pin at 17:04:17Z: sha256 `084951be…c78c5`, 44947 B, 976 newlines (977 lines; the last line
carries no trailing newline), mtime 11:52:22.988 -03, mode 755, tsukuroi HEAD `165307fe`,
`git status --porcelain -- tools/tsukuroi-census.sh` empty. Verified: `git show
165307fe:tools/tsukuroi-census.sh | sha256sum` = `084951be…c78c5` — **the pin was the committed
revision**. Re-pin after the sweep (~17:10Z): sha256 `aae45531…07df6`, 48410 B, 1032 newlines,
mtime 14:06:23.048 -03, working tree ` M tools/tsukuroi-census.sh` (plus ` M plans/round-5.plan.md`,
`?? plans/round-5-record-draft.md`, `?? plans/round-6.plan.md`). The diff is **+56 lines, zero
deletions**, inserted at old line 914: a `round-5 mutation hardening (lane S5-1, 2026-10-14)`
block adding **9 selftest cases (26 → 35)** labelled D02/D05/D06/D09/D10/D12/D14/D15/D19/D20,
whose own comment quotes "tameshi's mutate-and-run.sh, 23 single-edit defects, first pass
13 killed / 10 survived" (that lane's table is not read here; its working-tree draft traces
"26 → 35 by 17:07Z", `tsukuroi-shokunin/plans/round-5-record-draft.md:323-324`). Consequences,
recorded not smoothed:

- The assignment's check "tsukuroi original sha256 before/after identical" **cannot be made**:
  before ≠ after, cause = a concurrent lane's write to its own gate. This lane wrote nothing to
  the tsukuroi tree: every write of this run is under `/tmp/w5-tameshi-1-work/`, none of the ten
  edits below appears in the live diff, and the two mutant sets (B1–B10 here, D01–D23 there,
  per the quoted comment) are disjoint taxonomies. The negative claim that *is* provable: this
  lane's writes never touched the substrate; the positive claim that the bytes were stable is
  not available.
- **Every measurement in §§1–3 is on the pinned `084951be` bytes via the frozen copy** (sha
  re-verified at the end of the run); the sweep's inputs were frozen before the 14:06:23 write,
  so no §1/§2 run read the live path. The live revision is exercised only in §6's replay.
- Per lane discipline (`SKILL.md` restore rules 4–5: a drift is an incident; never repair by
  rewriting) the drift is reported, not repaired.

Anchors: **O** = observation (file:line, command output, re-quoted measured cell); **I** =
inference; **U** = unknown. `tsukuroi-census.sh:NNN` = `tsukuroi-shokunin/tools/
tsukuroi-census.sh` @ `084951be…c78c5`; line refs ≤ 914 are identical on the live `aae45531`
revision, refs beyond shift +56. Host: bash 5.3.15, python 3.14.7, kernel 7.2.3-arch1-3.

## 0. Gate choice, method, headline

**Why this gate.** The assignment names it (third artifact, different author): a 976-line bash
four-plane host census (`census-v2`) whose decision table is documented in its own header
(`:33-117`), with a hermetic `--selftest` and a stated read-only guarantee (`:118-120`).

**Hermeticity (O).** Every probe command and host path is env-overrideable (`:146-161`); the
selftest builds a `mktemp -d /tmp/tsukuroi-r3-2-selftest.XXXXXX` fixture tree with a dispatcher
stub for all seven probe binaries (`stub :635-685`), re-invokes the census against it via its
env overrides (`:750-766`: 14 names per case, plus `EXTRA_ENV` where a case needs one more —
cases 12 and 22 only), and its cases assert exit + verdict + evidence substrings + a
fixture-byte-unchanged hash (`fx_hash`/`fx_no_mutation`, `:735-741`) + a `host=fixture-host`
possible-host-read guard (`:771-772`). The census creates no files in live mode (`:118-119`).

**Method (round-2/3 replica).** Control run on the unmutated copy; each defect = ONE exact
replacement (text or one line range) applied to a fresh copy of `pristine.sh`; the driver
asserts `count(old) == 1` and `new != old` per defect (`--check` → literal `all unique`, all ten
unique, first matching lines equal to the pinned bytes); mutants never compound and are never
patched; per-mutant evidence = full combined output (`evidence/B*.selftest.txt`), meta
(`evidence/B*.meta.json`: exit, sha256, wall, summary, failing labels), aggregate
(`evidence/results.json`).

- O: control — `TSUKUROI_CENSUS_SELFTEST: PASS (26 cases, 26 passed, 0 failed)`, exit 0, 1.77 s.
  The suite's grammar: per-case `PASS <label> (exit N, VERDICT)` / `FAIL <label>: exit X wanted
  Y` / `FAIL <label>: verdict not V` / `FAIL <label>: plane evidence missing: '<re>'`;
  cases run through `check() :744-787`; the census's own case count holds on every run.
- O: **kill rate 6/10 (60 %)**; survivors B7, B8, B9, B10; no inconclusive run — all 11 runs
  (control + 10 mutants) produced a definitive suite verdict, and the count held:
  `(26 cases, …)` on every run, green runs printing exactly `PASS (26 cases, 26 passed,
  0 failed)`.
- O: cost — 11 runs in 19.6 s wall (control 1.77 s; mutants 1.72–1.82 s each) against a 280 s
  per-run timeout; ~1.8 s per run, the slowest of the three cases (JS 7.0 s, kagi 11.0 s for
  11 runs) — this gate re-invokes the whole census per case.
- O: **pre-registration held 10/10 on verdicts and 10/10 on failing-case counts** (§5 E1) —
  the first sweep of the three with no calibration miss.
- Composition (pre-registered before any run): 6 mutants aimed at defects the asserts *should*
  catch (B1–B6) — all six killed; 4 aimed at the matrix's predicted survivor families (B7–B10)
  — all four survived. A sweep's rate is only comparable across sweeps of similar composition;
  see §4's band amendment.
- Restore result (this lane): pristine copy `cmp`-identical to the pin at copy time; final sha
  of the frozen copy `084951be…c78c5`; all writes confined to `/tmp/w5-tameshi-1-work/`; the
  fleet's original moved by another writer (I1).

## 1. Kill-rate table

| # | Defect class | Injected defect (site = edit site on the pinned rev) | Exit | Suite line | Verdict | Failing cases |
|---|---|---|---|---|---|---|
| — | control | unmutated copy | 0 | `26 passed, 0 failed` / PASS | green | 0 |
| B1 | inverted condition | nvidia guard `[ "$smi" != ok ]` → `== ok` (`:473`) | 1 | `24 passed, 2 failed` | **killed** | 2 (2 healthy-gpu, 15 blocked-gpu) |
| B2 | boundary (rc tolerance) | Qkk rc tolerance {0,1} → {0,2}; rc=1 rejected (`:281`) | 1 | `23 passed, 3 failed` | **killed** | 3 (4 backup-only, 5 drift, 13 sample-error) |
| B3 | dropped fail-closed arm | empty-ring re-check arm + comment deleted (`:434-452`) | 1 | `25 passed, 1 failed` | **killed** | 1 (17 empty-ring) |
| B4 | weakened kind pin (classifier) | journal kernel alternative dropped from err classifier (`:578`) | 1 | `25 passed, 1 failed` | **killed** | 1 (19 boot errors) |
| B5 | off-by-one count | journal drift counter `+1` → `+2` per drifting timer (`:615`) | 1 | `25 passed, 1 failed` | **killed** | 1 (21 timer-drift) |
| B6 | behavior predicate (rollup) | `worse()` `-gt` → `-lt`; worse plane no longer wins (`:210`) | 1 | `5 passed, 21 failed` | **killed** | 21 (every non-HEALTHY case) |
| B7 | boundary / cap unreached | default Qkk sample cap 8 → 9 (`:160`); fixture samples 4 | 0 | `26 passed, 0 failed` | **survived** | 0 |
| B8 | wrong exit-code mapping (out-of-band) | usage refusal `exit 2` → `1` (`:935`); no case runs the CLI parser | 0 | `26 passed, 0 failed` | **survived** | 0 |
| B9 | reported-but-unasserted fields | roll-line printf args `"$PKG_V" "$SYS_V"` swapped (`:967`) | 0 | `26 passed, 0 failed` | **survived** | 0 |
| B10 | unreached arm | PCI-unreadable branch → silent `nv='absent(pci_10de=0)'` (`:487-493`) | 0 | `26 passed, 0 failed` | **survived** | 0 |

By class: inverted condition 1/1 · boundary (rc) 1/1 · dropped arm 1/1 · weakened kind pin 1/1 ·
off-by-one count 1/1 · predicate (rollup) 1/1 · cap unreached 0/1 · out-of-band exit map 0/1 ·
unasserted fields 0/1 · unreached arm 0/1.

Failing-case labels (O: `evidence/<id>.selftest.txt`, exact bad-case lines, abbreviated to the
diagnostic):

- B1 (2): case 2 `exit 2 wanted 0` — the flipped guard makes a present-and-answering GPU
  `BLOCKED`; case 15 `plane evidence missing: 'nvidia-smi not answering'; got: PLANE drivers:
  BLOCKED (pci_10de=1 but no nvidia module loaded — …)` — **exit still matched (2 = 2), the
  reason substring carried the kill** (same species as kagi B4's token-only kill).
- B2 (3): cases 4 `exit 2 wanted 0` and 5 `exit 2 wanted 1` (rc=1 is the fixture's own value at
  the tolerance boundary); case 13 `plane evidence missing: 'sample probe error'; got: PLANE
  packages: BLOCKED (pacman -Qkk sample rc=1 [probe cannot run])` — again **token-only**, the
  suite pins *why* it blocked, not just that it did.
- B3 (1): case 17 `exit 0 wanted 2` — with the re-check gone, an empty ring rides the
  `kerr=0` path to `HEALTHY`; the case's `HEALTHY`-vs-`BLOCKED` split is the arm's only case.
- B4 (1): case 19 `plane evidence missing: '^PLANE journal: DEGRADED .*err=4
  \(coredump=1 kernel=1 other=2\)'; got: … (coredump=1 kernel=0 other=3)` — the entry-level
  class tally is pinned by exact counts (the same fixture's drivers note is unaffected, which
  is correct: the drivers plane counts with `CLASS_*` patterns, the journal plane with its own
  `awk`).
- B5 (1): case 21 `plane evidence missing: '…timer_drift=1 …' ; got: … armed=0 timer_drift=2
  timer_unknown=0 (ai-usage.timer=inactive)` — the exact-count substring `timer_drift=1` is the
  tripwire (B7-of-kagi's analog).
- B6 (21): every non-HEALTHY case fails `exit 0 wanted 1|2`; the mutant's verdict line reads
  e.g. `TSUKUROI_CENSUS: HEALTHY (packages=DEGRADED systemd=HEALTHY drivers=HEALTHY
  journal=HEALTHY)` — verdict `HEALTHY` while a plane is red: the worst-plane-wins contract
  (:31) is gone, and one edit upstream of the shared exit channel colours 21 of 26 cases
  (§4, width amendment).

## 2. Survivor analysis and probes (recipe step 8)

All four survivors are observable differences on inputs outside the suite's fixtures
(`evidence/probe-survivors.txt`, built by `probe.py` on its own stub + fixtures):

- **B7 — sample cap 8→9 (`:160`).** O: 26/26 PASS. The fixture delivers 4 packages against a
  default cap of 8; `head -n "$SAMPLE_N"` truncates nothing either way, and no case reads the
  `sample=` field (O: field inventory §3.1; grep of the 26 asserts). Non-equivalence (O, probe
  P7, 9-package fixture): pristine `… sample=8(alpha,…,theta) …`; B7 `… sample=9(alpha,…,
  theta,iota) …` — the *sampled set itself* differs; the suite's stub ignores `-Qkk` argv and
  returns the same `qkk.out`, so the suite cannot see which packages were probed even when the
  note line is read. This is the round-2 D2 shape (cap never reached) reproduced on bash.
- **B8 — usage refusal `exit 2`→`1` (`:935`).** O: 26/26 PASS. The parser (`:921-937`) is never
  exercised: all cases invoke the census with zero arguments (`check() :766`); `--sample`/
  `--help`/unknown-arg paths have no case. Non-equivalence (O, probe P8): `--bogus` → pristine
  exit 2, B8 exit 1, same message. The artifact's *in-band* exit map (verdict → 0/1/2, `:969-974`)
  is pinned by 12 blocked cases; the out-of-band refusal is pinned by none.
- **B9 — roll-line fields swapped in the printf args (`:967`).** O: 26/26 PASS. `check()` asserts
  the verdict *prefix* `^TSUKUROI_CENSUS: <VERDICT> \(` and never the four `planes=` fields,
  except case 18 — the suite's only full-roll-line assert (`:874-876`) — which sits on the
  suite's only all-HEALTHY fixture, where a field swap is invisible (all four fields equal).
  Non-equivalence (O, probe P9, packages-DEGRADED fixture): pristine `TSUKUROI_CENSUS: DEGRADED
  (packages=DEGRADED systemd=HEALTHY …)`; B9 `… (packages=HEALTHY systemd=DEGRADED …)` — same
  verdict word, same exit 1, wrong plane attribution for any consumer reading the fields. This
  is the kagi-B10/D2 family on the verdict line itself.
- **B10 — PCI-unreadable branch replaced by a silent absent (`:487-493`).** O: 26/26 PASS. Every
  fixture `mkdir -p`s the pci dir (`fx_default :698`), so `count_pci_nvidia` never returns its
  `-1` sentinel (`:228`) and the `-1` branch is unreachable in-suite. Non-equivalence (O, probe
  P10, pci dir pointed at a missing path): pristine `PLANE drivers: BLOCKED (PCI inventory
  unreadable and no positive nvidia evidence — cannot assess read-only; … pci_10de=-1)` exit 2;
  B10 `PLANE drivers: HEALTHY (… nvidia=absent(pci_10de=0) … pci_10de=-1)` exit 0 — a full
  verdict flip (BLOCKED→HEALTHY) on an unreadable inventory, precisely the anti-claim the gate
  documents (`:79-80`).

Shared class: three of the four survivors change what no assert reads (an unasserted cap's only
trace, an unasserted refusal path, unasserted verdict fields); the fourth is a branch no fixture
reaches. Both are the matrix's admitted survivor families (§4).

## 3. What the 26-case suite protects — and does not

**3.1 Asserted vs unread note fields (O: parse of all 26 `check()` statements, label text
stripped).** Read: packages `drift=` (1), `backup_diffs=` (4), `foreign=` (6), `pins=` (7),
`db.lck=` (11); systemd `failed=` (8), `timer_fail=` (9); drivers `ring=` (3), `kerr=` (3,10),
`nvidia=` (2); journal `boots= current= target= err= failedhist= armed= timer_drift= coredump=
kernel= other= timers_enabled= timers_scanned= timer_unknown=` (18, and 19/20/21/24).
**Unread on this revision:** packages `sample=`, `nonroot_artifacts=`, `holds=`; systemd `state=`,
`timers_enabled=`, `timers_scanned=`, `timer_unknown=` (case 18's identical tokens are the
*journal* plane's); drivers `dmesg_restrict=`, the class tally (`oom=/io=/gpu=/other=`),
`smi=`, `modules=`, `nodes=`, `pci_10de=`. So this gate asserts far deeper into its notes than
kagi's did (whose whole CLEAN summary was unread), but the unread set is non-empty and includes
the entire driver-plane evidence tail and the sample inventory (B7's only trace).

**3.2 Unreached arms (I: static read of the fixture set; each is a probe candidate, none
mutated here).** Fixture-value inventory first (O: grep of the selftest's writes): `qkk.rc` ∈
{0,1}; `sysrunning` ∈ {`running`, bus-failure text}; `pq` never emptied; pci vendor ∈ {absent, 1};
`smi.rc` ∈ {0,1,6}; `lsmod` ∈ {empty, 2 rows}; `pacman.conf` fixed; no `*.rc` for `pq`,
`failedunits`, `timerlist`, `timerresult`, `timeractivestate` (default 0). Consequently these
arms cannot be reached by any case: packages — `pacman -Qq rc≠0` (`:265-268`), empty-list
(`:272-276`), sample rc ∉ {0,1} (`:281-285`); systemd — `systemctl` missing (`:333-337`),
state offline/maintenance (`:350-354`), `list-units`/`list-unit-files` rc (`:358-362`,
`:367-371`), the documented *deliberate* `degraded|starting|stopping` refinement (`:392`, whose
policy note lives at `:62-65`), unreadable timer Result (`:380-381`); drivers — journalctl-k
empty-ring variant (`:437-443`; case 17 exercises the dmesg variant), module-missing and
nodes-missing subarms (`:476-481`), the `pci_n=-1` inventory branch (`:487-493`, B10);
journal — `--list-boots` rc (`:523-527`), target-probe default branch (`:550-553`), timer-plane
unreadable (`:599-603`), timer ActiveState unreadable (`:610-611`). No abstention exists in this
suite (0 skips; every case executes) — the kagi `skip-case` shape has no counterpart, so all
gaps here are *silent*, not declared.

## 4. Cross-author comparison against the arm-class matrix (TAMESHI-R4-1)

Headline first: **80 % (JS r2) / 80 % (kagi bash r3) / 60 % (tsukuroi bash r5)** — but the third
sweep's composition is 6 kill-aimed + 4 hole-aimed probes, with 6/6 and 4/4 respectively. The
rate difference is composition, not quality (band amendment, E3). All three sit in the 50–80
band; the boundary/interior question (SKILL.md bands) is still carried by these three points.

Row by row (matrix rows A–G; each cell O unless marked I):

- **Row A — Verdict paths: confirm, plus one new shape.** The admitted phenomenon reproduces on
  a third gate: the asserted stem (exit + verdict word + `(` + per-case evidence substrings) is
  protected — all six kills are read through it — and a mutant confined to the verdict line's
  unasserted remainder survives (B9, §2). New shape: this gate's *only* full-roll-line assert
  (case 18) is structurally blind to field swaps on mixed verdicts, because its fixture is the
  all-HEALTHY one where every field reads the same; JS pinned its CLEAN line on the same
  all-green fixture but the line's fields carried distinct values there. Pin-style spectrum is
  now three points: JS one exact line + prefixes; kagi substring-only; tsukuroi prefix + an
  exact line that cannot discriminate the interesting case.
- **Row B — Fail-closed arms: confirm in-band, amend out-of-band.** The shared property (a 2→1
  exit-map edit dies) holds *per executed refusal path*: 12 blocked cases pin exit 2 with reason
  substrings, and B3 shows a fail-closed arm (empty-ring re-check) dying on exactly its 1 case.
  Amended: tsukuroi's *usage* refusal (`:935`) has no case, and B8 survives 26/26 (probe P8:
  exit 2 vs 1). So "fail-closed exit-map protected" is case-coverage-bound even inside one
  artifact, not a property of the artifact. Species inventory extends the round-3 reading (JS
  environment-failure, kagi malformed-data): tsukuroi's exit-2 species is *cannot-assess /
  cannot-tell-clean-from-empty* — the class kagi deliberately mapped to exit **1** as a
  verdict-shaped line lives here at exit **2** as `BLOCKED`. Three gates, three exit-map
  philosophies for the same epistemic class; all three deliberate and documented.
- **Row C — Counts: confirm, plus the boundary amendment.** B5 dies on the exact substring
  `timer_drift=1` — the third exact-count tripwire across three gates (JS literal counts, kagi
  `unverified=3`, tsukuroi `timer_drift=1`). B2 dies where the fixture value sits exactly on the
  tolerance (rc=1) — and one of its three kills is token-only. B7 *survives*: a cap +1 edit with
  the fixture far below the cap (4 vs 8; also 1 vs 12 timers, 2 vs 6 names). Amended: in the
  pair, bash boundary mutants died because those fixtures sat exactly on their boundaries
  (kagi floor/`len+1`); this gate's caps are all unreached. **Cap reachability is per-cap** —
  the row-C counterpart of row E's per-arm rule; a boundary edit's fate is a fixture-alignment
  fact, not a language fact.
- **Row D — Reported-but-unasserted surfaces: confirmed (3rd gate).** B9 is the exemplar
  (verdict fields); B7's behavioral difference is visible in-suite only through an unread field
  (`sample=`). The unread-field inventory (§3.1) shows the family is smaller here than in kagi
  but present, and it now sits in the *verdict products* (roll line, sampled-set display), not
  only in a summary tail. Two independent measures (this sweep and the static inventory) agree.
- **Row E — Unreached arms: promoted from "proposed" toward pattern.** B10 survives (second
  bash instance; still zero JS instances across three gates); B8 is a refusal path with no case
  (the gates-survey F-2 pattern, now measured); B7 is a cap no case reaches; and §3.2 is a static
  inventory of a dozen more across all four planes. Confidence: two bash instances measured in
  two different artifacts, plus a static inventory; the class still has no JS instance, so it
  remains bash-weighted and *proposed*, not admitted — but its repair shape is consistent
  (add one case per arm; contrast row D's repair: assert the value).
- **Row F — Coordinated edits: unchanged.** Single-edit experiment only; no coordinated mutant
  injected. B9's vicinity (roll printf) and kagi's U1 (both summary arg sets) remain unmeasured.
- **Row G — Behavior predicates: confirmed 3/3 here** (B1 inversion, B4 weakened classifier,
  B6 rollup comparison) — 9/9 killed across three gates. **Width amendment:** B6 kills 21/26
  (81 %), the widest bash kill measured, vs kagi's widest 3/16. (I) The round-3 reading "a bash
  kill is structurally narrow" is true only for *per-arm* edits; width is set by where the edit
  sits relative to the suite's shared assert channel — here every case asserts `exit`, and the
  exit is one `worse()` rollup of four plane verdicts, so a rollup edit crosses 21 of 26 cases.
  Language is not the variable; mutant placement is.
- **Independent corroboration (O: live diff, quoted claim).** A concurrent lane's separate
  sweep of this artifact (23 defects, quoted 13/10 split) landed hardening cases for exactly
  the hole classes this case's §3 inventory names: empty local db (D02), unread nonroot count
  (D05), sample size/field (D06), unreadable timer Result (D09), scope state degraded (D10),
  missing /dev node (D12), driver class counts (D14/D15), PCI unreadable (D19 — B10's arm),
  journal timer plane (D20). Two independent sweeps converging on the same hole set is stronger
  evidence for the family than either sweep alone; the overlap is O, their 23-defect table is
  not in this note's evidence.

**Fleet axes table (third data point).**

| Axis | JS r2 (kumitate) | bash r3 (kagi) | bash r5 (tsukuroi) |
|---|---|---|---|
| artifact | `kimi-census.mjs` 896 ln | `surface-census.sh` 886 ln | `tsukuroi-census.sh` 977 ln |
| suite grammar | `n/43 pass` + `FAIL` labels | `ok/bad-case` + `SELFTEST (n/16)` | `PASS/FAIL <label>` + `SELFTEST (26 cases, n passed)` |
| abstention | none | 2/16 `skip-case` substrate-gated | none (0/26; all gaps silent) |
| kill rate | 8/10 (80 %) | 8/10 (80 %) | 6/10 (60 %; composition 6 kill-aimed + 4 hole-aimed) |
| widest kill | 16/43 | 3/16 | 21/26 |
| survivors | D2 tail, D10 frozen | B5 unreached arm, B10 summary field | B7 unreached cap, B8 out-of-band exit, B9 verdict fields, B10 unreached branch |
| restore pin | `83016d45` before=after | `275d8294` before=after | `084951be` before; `aae45531` after (other writer — I1) |
| cost | 11 runs / 7.0 s | 11 runs / 11.0 s | 11 runs / 19.6 s (~1.8 s/run) |

## 5. Calibration and errata (append-only)

- **E1 — pre-registration held 10/10 on verdicts and 10/10 on failing-case counts** (B6's 21
  included), the first perfect sweep of the three. (I) Cause, recorded because it is not
  repeatable luck: both prior notes' E1 misses were *case-set* reasoning slips — this time the
  26 labels and their assert texts were parsed into tables (as §3.1 does) before the defects
  were written, so each predicted failing set came from the case grammar, not from memory. The
  advantage came from the two prior E1s; record it as method, not as skill.
- **E2 — incident errata (I1): the pin moved mid-run.** The assigned before/after sha claim is
  unsatisfiable (other writer). The record keeps both pins, the frozen copy's sha, and the
  write-fencing evidence. Method note (I): mutation cases on *concurrently edited* substrates
  need the pin to be a *committed revision* and the case to say so (it was, and does); the
  fleet's `mutate-and-run.sh` records the target sha before/after but cannot distinguish "the
  operator's run moved it" from "another lane moved it" — a mtime/inode note in its receipt
  would separate the two. Recommendation only; no tool edit from this lane (assignment bound).
- **E3 — band convention amendment (composition binding).** The kill-rate bands compare rates
  across sweeps; this case's 60 % is depressed by design (4 of 10 mutants were aimed at
  predicted holes). A rate without its composition (kill-aimed vs hole-aimed) is not comparable
  across authors — record composition beside every rate from now on. This does not move the
  bands; it binds them.
- **E4 — convergence, recorded as corroboration not as double-counting.** This sweep's survivor
  and hole classes (B7/B8/B9/B10, §3.2) overlap 8/9 with the concurrent lane's hardening classes
  (D02…D20). Two sweeps, two authors of the target, same holes — the strongest single datum in
  this note for rows D/E; it is *not* a second measurement of any cell in §1.

## 6. Cross-revision replay on the live revision (measured, brief)

A frozen copy of the live `aae45531` revision (the S5-1 hardening; sha stable across the pulse,
17:1xZ; `PASS (35 cases, 35 passed, 0 failed)` exit 0, and stable across the replay) was used
to re-cut this case's four survivors from *its* bytes (`evidence/replay-*.selftest.txt`,
`replay-results.json`):

- B7 (default cap 8→9): **still survived** 35/35 — the new D06 case sets `TSUKUROI_SAMPLE_N=2`
  by env, which overrides the default the mutant edits; the cap's default site is still unpinned.
- B8 (usage exit 2→1): **still survived** 35/35 — the CLI parser still has no case.
- B9 (roll fields): **still survived** 35/35 — no new case reads the roll-line fields.
- B10 (PCI-unreadable): **killed** by the new case `blocked: unreadable PCI inventory is not a
  pass (D19)` — `exit 0 wanted 2` with the verdict `HEALTHY` where the case wants `BLOCKED`.
So of this case's four holes, the concurrent hardening closed one (B10) and left three open
(B7's default site, B8, B9) as of `aae45531`. These four replay cells are measured on that
uncommitted revision; the live tree may move again (I1 continues) — re-pin before quoting.

## 7. Unknowns

- U1 — coordinated multi-edit rewrites (roll fields *and* their printf format; both summary
  arg sets) and edit reordering are outside the single-edit experiment (row F unmeasured).
- U2 — the §3.2 unreached arms are a static reading of the fixture set. Only B10's arm has a
  measured mutant; the other dozen are probe candidates, not measurements (two of them — empty
  db, PCI — were later closed by the S5-1 cases, but their mutants were not run here).
- U3 — no systemd-plane mutant was injected (the plane appears only as fixture/assert context);
  its kill profile for plane-local edits is unmeasured in this case.
- U4 — host-gated behaviour: this suite has no substrate-gated cases (all 26 execute), so unlike
  kagi U2 there is no host-conditional verdict — but the *live* census path (real pacman/systemd/
  dmesg/journal on this host) is not exercised by any mutant; hermetic by construction.
- U5 — kill-rate and timing stability across hosts/toolchains (bash 5.3.15, python 3.14.7,
  kernel 7.2.3, one host, 2026-10-14; ~1.8 s/run).
- U6 — the live revision `aae45531` (and any successor) is unpinned by this case beyond §6's
  four-celled replay; the concurrent lane's 23-defect table is quoted, not read.
- U7 — whether the S5-1 hardening cases would also kill the *rest* of this case's mutants was
  not measured (only B7–B10 were re-cut) — B1–B6 target v2 logic unchanged in the new revision
  (O: all seven text sites still unique in `aae45531`), so their verdicts are expected to hold;
  unmeasured.

## 8. Reproduce

Scratch: `/tmp/w5-tameshi-1-work/` — `pristine.sh` (byte copy of `084951be`), `control.sh`,
`mutant-B{1..10}.sh`, `mutate_driver.py`, `probe.py`, `replay.py`, `live-1450.sh` (frozen
`aae45531`), `replay-B{7..10}.sh`, `evidence/` (control + B1–B10 outputs, metas, `results.json`,
`probe-survivors.txt`, `replay-*`).

Driver manifest — the ten exact edits, each applied once to a fresh copy of `pristine.sh`
(`old` extracted from the pinned bytes; `--check` prints `count=1` per defect and the literal
line `all unique`):

```
B1  tsukuroi-census.sh:473    if [ "$smi" != ok ]; then
                          ->  if [ "$smi" == ok ]; then
B2  tsukuroi-census.sh:281    if [ "$s_rc" -ne 0 ] && [ "$s_rc" -ne 1 ]; then
                          ->  if [ "$s_rc" -ne 0 ] && [ "$s_rc" -ne 2 ]; then
B3  tsukuroi-census.sh:434-452  the empty-ring re-check block (2 comment lines + `if [ "$kerr" -eq 0 ] … fi`) deleted
B4  tsukuroi-census.sh:578      /"SYSLOG_IDENTIFIER":"kernel"|"_TRANSPORT":"kernel"/ { k++; next }
                            ->  /"_TRANSPORT":"kernel"/ { k++; next }
B5  tsukuroi-census.sh:615      drift=$((drift + 1))   ->  drift=$((drift + 2))
B6  tsukuroi-census.sh:210      if [ "$(rank "$2")" -gt "$(rank "$1")" ]; then printf '%s' "$2"; else printf '%s' "$1"; fi
                            ->  the same line with -lt in place of -gt
B7  tsukuroi-census.sh:160      SAMPLE_N=${TSUKUROI_SAMPLE_N:-8}  ->  SAMPLE_N=${TSUKUROI_SAMPLE_N:-9}
B8  tsukuroi-census.sh:935      the unknown-argument line: … usage >&2; exit 2 ;;  ->  … exit 1 ;;
B9  tsukuroi-census.sh:967      "$roll" "$PKG_V" "$SYS_V" "$DRV_V" "$JRN_V"
                            ->  "$roll" "$SYS_V" "$PKG_V" "$DRV_V" "$JRN_V"
B10 tsukuroi-census.sh:487-493  the PCI-unreadable else-branch body -> `  else` + `    nv='absent(pci_10de=0)'`
```

Commands (in order; O):

```
sha256sum tsukuroi-shokunin/tools/tsukuroi-census.sh   # 084951be…c78c5 (was the pin)
mkdir -p /tmp/w5-tameshi-1-work/evidence && cd /tmp/w5-tameshi-1-work
cp -p <artifact> pristine.sh && cp -p pristine.sh control.sh && cmp pristine.sh control.sh
python3 mutate_driver.py --check    # all unique
python3 mutate_driver.py --run      # control + 10 mutants -> evidence/
python3 probe.py   > evidence/probe-survivors.txt
python3 replay.py  > evidence/replay.txt
```

Sensitivity checks expected from the note alone: P7 pristine `sample=8(alpha…theta)` /
B7 `sample=9(alpha…iota)`; P8 pristine exit 2 / B8 exit 1 on `--bogus`; P9 pristine
`packages=DEGRADED` / B9 `packages=HEALTHY systemd=DEGRADED`; P10 pristine
`drivers: BLOCKED … pci_10de=-1` exit 2 / B10 `drivers: HEALTHY … nvidia=absent(pci_10de=0)` exit 0.

**Spot-checks (three cited refs re-read on the pinned bytes — `pristine.sh`, sha re-verified
`084951be`; the live tree no longer holds this revision, I1).** (1) `:473` → `if [ "$smi" != ok
]; then`; `:281` → `if [ "$s_rc" -ne 0 ] && [ "$s_rc" -ne 1 ]; then`; `:210` → the `worse()`
one-liner with `-gt`. (2) `:939-942`/`:966-967` → the selftest/main split and roll printf;
`:744-787` → `check()` asserting exit, `host=fixture-host`, verdict prefix, evidence substrings;
`:735-741` → `fx_hash`/`fx_no_mutation`. (3) live pulse on the frozen `aae45531` copy →
`TSUKUROI_CENSUS_SELFTEST: PASS (35 cases, 35 passed, 0 failed)` exit 0; original sha at 17:11Z
`aae45531…07df6` (moved once, by another writer; re-checked stable across the pulse).