# K04 — Attack contract B: trace-collector promotion

Axes attacked: correctness of the P05–P07 measurement, ledger/receipt
integrity, duplicate-authority drift, premature-saturation (a "closed" probe
that measures nothing). Read at dispatch tip
`183f87b899e6cae46be98d251cbc87fb5118f6ca`; live tree inspected read-only
(`git --no-optional-locks status --porcelain` shows `?? tools/trace-inputs.py`,
`?? .ufo/evidence/round-18/` — X04's uncommitted build).

## Q1 — do receipts, measure, or assemble depend on the collector's path?

**No — receipts and both checkers are path-blind to the collector.** This leg
of the promotion is clean.

- Receipt payload is content-addressed: `argv`, `cwd`, `root`, `rev`, `inputs`,
  `external`, `live_lane_reads` — the collector's own path appears only if the
  *traced command* opened it (e.g. `traces/CR02/09-helper-open.json` argv
  `sha256sum <abs>/trace-inputs.py SKILL.md`).
- `assemble.py` validation is schema-shape only:
  `.ufo/evidence/round-17/coldread/assemble.py:439-494` (`load_trace_receipt`)
  checks `schema == tameshi-trace-inputs-v1` (const at :130), `rev ==
  read_rev`, `live_lane_reads` bound-ness, and digest shape of `inputs`/
  `external`. `trace_receipt_path` (:434) resolves the receipt path in the
  repo, not the collector path. Round-18 `assemble.py` inherits this
  (:129-133, :440).
- `.ufo/evidence/round-17/measure.py:136` gates on `TRACE_SCHEMA` + per-input
  sha resolution against rev blobs (`:172`); the collector path is never a
  constant. Round-18 `measure.py:140` identical; `IGNORED_INPUTS` (:135) is
  `SKILL.md` + both ledger paths — correctly does **not** exempt either
  collector path, so recorded collector reads stay credit-bearing.
- The collector itself is location-independent by construction: `DEFAULT_FLEET`
  hardcodes `/home/vgpnk/Projects/shokunin` (r17 :69); `__file__` is used only
  by `--selftest` to re-exec itself (`tools/trace-inputs.py:770`,
  `tool = os.path.abspath(__file__)`). Selftest is synthetic-only per docstring.

## Q2 — promoted tool as recorded input (self-invalidation)

**Yes, and correctly so — with one nuance.** `tools/trace-inputs.py` is
recorded as an input whenever a traced command opens it (r18 measure keeps it
out of `IGNORED_INPUTS`), so later edits force input-keyed re-reads — intended
drift, no leak. Nuance: the collector's *own* open is never recorded when it
is the traced root (Python reads the script before strace attaches), and seats
invoke it directly — so **collector edits do not invalidate existing entries
unless seats traced opens of the file**. Verified: 20 of 68 round-17 ledger
entries record `.ufo/evidence/round-17/coldread/trace-inputs.py` sha
`521be955…` (CR02/08/11/14/24/28/39/40/46/47/48/51/52/54/55/56/57/58, RR7,
RR8 — seats sha256summed the helper). Input drift on a collector edit is real
but bounded to such explicit reads; not a hazard.

## Q3 — does the probe's base/after target-switch game P05–P07?

**Mechanically sound, fail-closed toward `open` — but the `closed` definition
has two exploitable holes and one fragility.**

- Anchors verified unique in both copies (count==1 in each): `RDWR|` at
  `tools/trace-inputs.py:82`, `env["PYTHONPYCACHEPREFIX"] = cache` at :516,
  `first_pid … not in tracer.exec_ok` at :644 — all three r17 mutants re-die in
  the promoted file (X04 report: `rdwr-open-excluded`, `pycache-prefix-private`,
  `root-exec-required` each FAIL 29/30; pristine `SELFTEST: 30/30`).
- The switch `tools/trace-inputs.py` when tracked at REV else the frozen path
  is fail-closed: at base it mutates a file whose selftest is blind (open);
  after promotion it must mutate the hardened file (closed iff real). Keeping
  the frozen file in place prevents silent target confusion — good.

**FINDING 1 (C2 false-positive hole).** Contract A defines `closed` = mutated
selftest exits nonzero; it never requires the *pristine* selftest to exit 0.
A promoted file that is broken outright (always-failing `--selftest`, syntax
error) reports all three probes `closed` — measuring nothing. Smallest
correction: each probe first runs the unmutated selftest; nonzero →
`could-not-evaluate` (exit 2), then mutate. Same defect shape as "dead gate
passes a mutation sweep" from SKILL's own bands.

**FINDING 2 (frozen-copy integrity unmeasured by the ruler).** Contract B's
"round-17 copy stays byte-identical" clause has no probe. If the builder (or
a later edit) hardens the frozen file in place — a tempting "fix both copies"
move — P05–P07 still close via `tools/`, probes stay green, but the historical
evidence sha `521be955…` is falsified: 20 carried ledger entries would carry
dead sha-pins, and `registry.json` row `trace-inputs-round17-selftest`
(`tools/registry.json:600-614`, argv = frozen path) keeps exercising bytes no
longer historical. Only the measure's input-keyed drift would surface it,
post-hoc. Smallest correction: one pure-integrity probe line in
defect-probes.py asserting sha256(frozen) == `521be955…` — costs ~5 lines,
converts a silent identity change into a probe failure.

**FINDING 3 (anchor fragility → exit-2 unmeasurability).** The mutant is a
literal text replacement requiring count==1. Any future edit that duplicates
an anchor token (e.g. a second `PYTHONPYCACHEPREFIX = cache`-style assignment
added by a refactor, already at risk: the token now appears in selftest code
at :925-928 context) or rewrites the guarded line drops the probe to exit 2 —
`could-not-evaluate` fails the *entire* C2 ruler run, not just that probe.
Contract B's "byte-for-byte behaviour" phrasing does not pin the anchor lines
verbatim; it should (they are probe API), or probes should match with context
windows. Status today: safe (counts verified 1/1/1 in both files).

## Q4 — duplicate authorities after promotion (the real regression surface)

The promotion as landed (`tools/trace-inputs.py`, sha `fb1d81f6…`, mode 755
— frozen copy verified intact at `521be955…`) leaves **three live references
to the frozen path that now diverge from the measured/canonical artifact**:

1. **`SKILL.md:1885` and `:1902`** — the trace command recipe and tool table
   still name `.ufo/evidence/round-17/coldread/trace-inputs.py`. Contract F
   says seat traces come "from tools/trace-inputs.py", but the documented
   workflow invokes the frozen copy. Both produce identical receipts today
   (implementation bytes equal except docstring + selftest), so this is a
   provenance-split defect, not a correctness defect: P05–P07 will have
   measured a file other than the one the lane's own playbook tells seats to
   run. Fix: stage a SKILL.md edit naming `tools/trace-inputs.py` (accepts
   the input-keyed wave-2 re-reads — that's the mechanism working).
2. **`tools/registry.json:600-614` row `trace-inputs-round17-selftest`** —
   exercises the frozen file's 27-case selftest. Harmless as an integrity
   canary (it *would* flag in-place mutation of the frozen file — actually a
   free mitigation for Finding 2), but the promoted file's 3 new guard cases
   have **no registry coverage**: a later regression in `tools/trace-inputs.py`
   is invisible to the C2 no-harm gate. Fix: add a
   `trace-inputs-tools-selftest` row (argv `python3 tools/trace-inputs.py
   --selftest`, expect `SELFTEST: `); registry edits are L1-proposed, not
   seat-edited — flagged for the L1.
3. **`corpus/knowledge/input-keyed-coldread-credit.md:3`** — the 90-day
   drift recheck rule runs the *frozen* selftest. Verified the staged copy
   (`.ufo/waves/round-18/staged/corpus/knowledge/input-keyed-coldread-credit.md:3`)
   still says this — so the staged edit does **not** fix it. After promotion,
   the drift detector is permanently blind to the live tool. Fix: point the
   recheck at `tools/trace-inputs.py --selftest` (keep or drop the frozen
   invocation — it doubles as a Finding-2 canary if kept).

## Tooling

None installed (nothing needed beyond system python3/git/diff).

## Verdict

**partial** — promotion mechanics are clean (no path dependence anywhere in
receipts/measure/assemble; anchors verified; frozen bytes intact), but P05–P07
can be gamed by a broken tool (no pristine control), the frozen-copy
byte-identity clause has no probe, and three committed authorities still route
invocation/recheck/coverage to the frozen path while the ruler measures the
promoted one.
