# Round-35 w2 — ConnectorWitness

Seat: `tameshi-r35-w2-ConnectorWitness` (leaf connector, godspeed). Lane pin at dispatch:
`7da6e076c2e25936a3b60dde2a4080d8f05b7e5b` (scratch lane
`/fast/scratch/hyaku/tameshi-r35-seats/ConnectorWitness/lane`, fetch+checkout exit 0).

**Assignment:** assess transferability of the round-34 set-aware witness rule +
round-35 four-config sweep (A4) to kagi's `checklist-run.sh`, read-only; report as a
recommendation with path:line evidence, never an edit.

**Evidence base (kagi lane, HEAD `899c50b`; worktree bytes == committed blobs,
verified `git show HEAD:<path> | sha256sum` both matching):**

- `kagi-shokunin/corpus/checklist-run.sh` sha256
  `7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf` (506 lines,
  last modified round-15 commit `587fda0`)
- `kagi-shokunin/corpus/checklist.tsv` sha256
  `28bd238e549c579d92b9818a9a2e98c0e8153957a18bc89384b1cc5c39972f04` (same commit)

No installs (nothing needed; `pacman` untouched). No writes anywhere under
`/home/vgpnk/Projects/shokunin/` except this report. The kagi full `verify` mode was
**never executed** (it would run row E5 → `op-ref-probe.sh`, which execs `op run`, and
read `$HOME` state): everything below is `--selftest` (mktemp fixtures only),
`--ratio` (executes no row — proven by selftest case `ratio mode runs no row`,
checklist-run.sh:482-484), or the real gate binary driven with scratch
`--tsv/--skill` printf-only pairs under
`/fast/scratch/hyaku/tameshi-r35-seats/ConnectorWitness/chan/`.

---

## 1. The two assets being transferred

1. **Round-34 set-aware witness rule** (`corpus/knowledge/witness-equivalence-rule.md`,
   tameshi lane): a held-out specimen is *valid* only when its witness demonstrates the
   **labeled** behavior, branching on the specimen's set — accept ⇒ demonstrated
   **equivalence** on the oracle's tuple, kill ⇒ demonstrated **difference**; the
   set-blind predecessor validated inert edits as must-kill and lethal-behind-benign as
   must-accept (rule §"Why the set-blind predecessor was voidable"). Generalized: *every
   member of a declared accept set must carry its own demonstrated observable; the
   declaration and the demonstrated set must be the same set.*
2. **Round-35 four-config sweep (A4)** (`tools/tally-audit-v3.py:33-38`, answering wave-1
   `RevengerRootShape` CRITICAL): the oracle must exercise **all real config states of
   the object under audit, with the objects' REAL values** — the auto triples now run
   with the runner's actual `mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX` root, not a
   simulated literal, because a copy keyed on a real config value is invisible to an
   oracle that never runs in that config.

## 2. The target gate as an oracle

`checklist-run.sh` binds 16 SKILL.md items to TSV rows via a two-directional lead
bijection (checklist-run.sh:205-228) and, per runnable row, decides on **two independent
channels**: exit ∈ `expect_exit` (a set `A|B|C` allowed, :263-273) and last non-blank
output line ~ `expect_last` ERE (:274-278), from one execution:
`out=$(cd "$ROOT" && timeout "$ROW_TIMEOUT" bash -c "$check" 2>&1)` (:261). The gate's
own witness apparatus is the 34-case selftest (:338-499); the rows' accept sets are the
TSV declarations.

## 3. Findings (ranked; all kagi-side, none falsifies a tameshi round-35 claim)

### BOUND-1 — the oracle's channel is merged stdout+stderr; the contract says stdout, and a shipped row *depends* on the divergence
- Documented contract: "expect_last = ERE matched against the last non-blank **stdout**
  line" (checklist-run.sh:14-15; `kagi-shokunin/corpus/knowledge/checklist-execution.md`
  §2 line 41). Measured reality: `2>&1` capture at :261, last line taken from the merged
  stream (:262).
- **Live, fail-open direction** — a row whose entire verdict is written to stderr passes
  CLEAN (scratch pair `chan/tsvA.tsv`, check `printf 'A1: OK\n' >&2`):
  `CHECKLIST_RUN: CLEAN (items=6 runnable=4 by_hand=2 failed=0)`, exit 0. The declared
  channel contract is satisfied by a channel it does not name.
- **Live, fail-closed direction** — stdout verdict followed by trailing stderr noise
  hijacks the oracle (`chan/tsvB.tsv`): `ITEM-LASTLINE C1 (want /^A1: OK$/ got stderr\
  noise)` + `CHECKLIST_RUN: BROKEN (… failed=1)`, exit 1. A delegated gate that logs one
  warning line to stderr after its verdict false-fails its row.
- **Second-order trace (why the naive fix is forbidden):** H7's exit-2 witness lives ON
  stderr — `transcript-scan.sh:261` prints `transcript-scan: db not found: $DB >&2;
  exit 2`, and H7's `expect_last` alternative `transcript-scan: db not found: .*`
  (checklist.tsv row H7) is only matchable **because** of the merge. Aligning the code to
  the doc (stdout-only capture) would break a shipped row's declared accept state; only
  the doc-to-code direction is safe. This is A4 inverted: kagi's fixed value is real and
  load-bearing, but the contract text names a different value — the tameshi HYGIENE
  analogue is `c1-measure.py:46-47` duplicating the tool's literals (RevengerRootShape
  §4): apparatus and documentation must stay in lockstep.
- No selftest fixture exercises either direction today (`>&2` appears in
  checklist-run.sh only at :84-88 usage errors; the fixture table :371-407 has no
  stderr case).

### BOUND-2 — H7's declared exit set and its ERE encode different accept sets; member `0` is declared, unwitnessed, and unwitnessable
- H7 declares `expect_exit=0|1|2` with `expect_last =
  ^(TRANSCRIPT_SCAN: HITS=2 \(cells=…\)|transcript-scan: db not found: .*)$`
  (checklist.tsv row H7).
- `transcript-scan.sh` verdict semantics (:11, :278-284): hits>0 ⇒ `TRANSCRIPT_SCAN:
  HITS=<n> …` exit 1; hits=0 ⇒ `TRANSCRIPT_SCAN: CLEAN (…)` exit 0 (clean-or-warn);
  db absent ⇒ stderr + exit 2 (:261).
- So the ERE admits exactly two states — (exit 1, HITS=2 **exactly**) and (exit 2,
  db-not-found) — which the lane itself documents as the intent
  (checklist-execution.md §6.4: "names exactly two states … Any third state fails").
  The declared exit member `0` has **no** last-line observable that can satisfy the ERE:
  when the transcript is actually clean the row fails ITEM-LASTLINE despite `0 ∈
  expect_exit`. Per the round-34 rule the accept set must be the witnessed set: `0` is
  the residue of a set-blind declaration. Behaviorally the row is fail-closed either way
  (an operator who resolves both hits gets BROKEN and a forced re-pin — defensible
  teeth); the defect is the *declaration lying about what is accepted*, the exact class
  the set-aware rule was written to close.

### BOUND-3 — set membership is validated for shape, never for reachability (demonstrated)
- `load_rows` validates only `^[0-9]+(\|[0-9]+)*$` (checklist-run.sh:145); membership
  then decides (:263-273). **Live:** scratch pair `chan/tsvC.tsv` — check
  `printf 'A1: OK\n'` (can only exit 0) with `expect_exit=0|3` ⇒ `CHECKLIST_RUN: CLEAN`,
  exit 0. The dead member `3` is invisible to every check in the gate. The lane's own
  bound 11 already concedes the adjacent class ("a 16-row TSV whose every runnable
  check is a constant printf passes CLEAN", checklist-execution.md §6.11); this extends
  it from check strength to *accept-set honesty*: no mechanical witness for member
  reachability exists below per-row review — which is why the round-34 rule puts the
  witness at **authoring time**, not in the gate.

### HYGIENE-1 — the config corners the gate already sweeps, and the two it does not
- Swept and proven: timeout budget (selftest case `row timeout`, CT=1, :439), mode
  variants verify/--ratio/--only/--list (:427-491), `--ratio`-runs-no-row (:482-484),
  row-shape/policy classes (20+ cases, :434-479), and one-time foreign-cwd proof
  (round-15 LOG receipt, `kagi-shokunin/LOG.md:545` "runs from a foreign cwd").
- Not swept: the two stream-channel corners of BOUND-1 (verdict-on-stderr pass;
  trailing-stderr-noise fail) — no fixture class exists.

## 4. The recommendation (one bounded, kagi-side move; nothing executed here)

**Transfer the sweep to the selftest, transfer the set-awareness to the declarations,
and fix the contract text, not the capture.** Four kagi-side actions:

1. **Declare the merged channel** — one line each in checklist-run.sh:14-15 and
   checklist-execution.md §2: "last non-blank **output** line (stdout and stderr
   merged)". Do NOT switch :261 to stdout-only capture: that breaks H7's exit-2 witness
   (BOUND-1 second-order trace).
2. **Add two selftest fixtures** (printf-only, scratch, zero side effects): (a)
   verdict-on-stderr row asserting CLEAN — pinning the merged-channel contract as
   intended behavior; (b) stdout-verdict-then-stderr-noise row asserting
   `ITEM-LASTLINE` — making the hijack direction a proven, documented behavior instead
   of a surprise. These are the gate-level analog of A4's "sweep the real config
   states": the channel is a real, fixed gate config, and both its corners get a
   witness.
3. **Align H7's exit set to its witnessed states** — `expect_exit` `0|1|2` → `1|2`
   (one TSV token). Outcome for every reachable state is unchanged (clean and
   HITS≠2 both already BROKEN via the ERE); what changes is that the declaration equals
   the demonstrated accept set — the round-34 rule verbatim, applied to a TSV instead
   of a sealed JSON.
4. **Adopt the per-member witness convention for any future exit set** — each
   `A|B|C` member must name a distinct, mutually exclusive `expect_last` alternative
   (H7's ERE already does this for members 1 and 2: HITS=2 line vs db-not-found line)
   and each member must have been observed at least once. That is checklist-execution
   §6.4's "exactly two states" discipline, promoted from one row's note to the schema's
   rule — the direct import of "the check branches on the copy's set".

**What does NOT transfer, deliberately:** the literal per-row four-config sweep. The
tameshi (auto,KEEP) knobs are *internal* states of the artifact under audit, so the
oracle can and must visit all four (A4). checklist-run's corresponding state axes are
*host-external* — substrate presence (`$HOME/.local/bin/the-janitor` in H1,
`~/.config/the-janitor/*` in H3/H4, the transcript DB in H7) and handler lifecycle —
and the lane's own policy freezes them: handler start/stop/run and `op.env` are denied
surfaces (DENY_CHECK, checklist-run.sh:75), rows H2/H5 are by-hand precisely because
start/stop is operator scope (checklist-execution.md §5), and nothing schedules the
gate (§6.2). Sweeping those states would require the one class of action the checklist
exists to ration (handler ops, config deletion) for near-zero gain: reality already
sweeps that axis for free and the gate fails closed on it (host-move receipt,
`kagi-shokunin/LOG.md:736`: absent substrate ⇒ `CHECKLIST_RUN: BROKEN (… failed=6)`,
exit 1). Likewise a per-row re-execution under a second cwd or timeout adds nothing:
the gate pins cwd to the repo root at :261 — a *real* pinned value, so the A4 evasion
class (fixed literal ≠ any real value) has no analogue here. Verified live: a
cwd-keyed check (`case "$PWD" in *kagi-shokunin) … OK;; *) … WRONG-ROOT;; esac`,
scratch `chan/tsvD.tsv`) passes CLEAN under the gate even when the gate itself is
invoked from `/`, while the identical check string run by hand from `/` prints
`A1: WRONG-ROOT`, exit 0 — the gate's pin is the real config, so config-keyed rows
cannot evade the gate; only the by-hand re-run of a row's check string diverges, which
is a documentation matter (the contract already says "cwd = repo root"), not a gate
defect.

## 5. Cost (measured where measurable)

- Selftest today: `bash corpus/checklist-run.sh --selftest` ⇒ `CHECKLIST_SELFTEST: PASS
  (34 cases)`, exit 0, 2.59 s wall (measured this seat). +2 printf fixtures ≈ +0.2 s.
- `--ratio` (declaration audit, no row executed): `CHECKLIST_RATIO: runnable=9/16
  floor=8 by_hand=7 delegated=3 direct=6`, exit 0, 0.32 s — unchanged by the move; the
  16↔16 bijection holds at head.
- Full-run cost unchanged: ~2.3 s at the round-15 receipt (LOG.md:541-542); worst-case
  budget stays 9 × 240 s (checklist-run.sh:72). **Zero new handler/`op` interactions,
  zero new `$HOME` reads** — the sweep lives in mktemp fixtures, and E5's `op run`
  exec-count (the lane's declared boundary cost, checklist-execution.md §5) is not
  multiplied. That is the decisive cost argument against the literal per-row ×4 sweep:
  it would 4× the only expensive side effect for zero discriminating power.
- Kagi-side edit surface (recommended, not executed): 1 TSV token (H7 exit set), 2 doc
  lines, 2 selftest fixtures, 1 knowledge-entry sentence.

## 6. What I could NOT break (proofs)

- **The 34-case selftest at head** — PASS, exit 0 (command above). Every defect class
  the fixtures seed still fires.
- **The declaration bijection at head** — `--ratio` exit 0, 16 items ↔ 16 rows, no
  UNDECLARED/EXTRA/UNMATCHED/DUPLICATE defect.
- **`--ratio` executes no row** — selftest case `ratio mode runs no row` (:482-484)
  proves it with a row that would fail if executed; my run finished in 0.32 s with the
  ratio line only.
- **The cwd pin** — live D/D2 pair above: gate-invocation-from-`/` CLEAN, by-hand
  divergence `A1: WRONG-ROOT` exit 0. No cwd-keyed evasion of the gate exists.
- **Exit-set membership and ERE matching as implemented** — no counterexample to
  :263-278 found; every seeded exit/last-line mismatch in the selftest fires. The
  BOUND-3 dead-member result is a limit of *what is validated*, not a wrong verdict on
  any reachable state.
- **No tameshi round-35 claim is touched.** C1's apparatus (`tally-audit-v3.py`,
  runner, counters, panel, sealed dir) was read, never executed or edited; C2 is
  unaffected; the frozen artifacts' pins were not re-hashed by this seat (inherited
  wave-1 verifications). This move claims only **adjacency**: the round's two rules,
  reduced to practice on a sibling lane's gate, with the one inversion (fix the doc,
  not the code) that keeps a shipped witness alive.

Scratch artifacts: `/fast/scratch/hyaku/tameshi-r35-seats/ConnectorWitness/chan/`
(gen.sh, tsvA-D.tsv, SKILL.md). Lane checkout read-only throughout; no git/jj mutation
in any repo; no `pacman`; no tool installs.
