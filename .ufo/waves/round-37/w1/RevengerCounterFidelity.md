# RevengerCounterFidelity — r35/v2 counter fidelity vs the r37 empty-panel adapter

Axis: calibration. Scope: reverse-engineer the frozen r35 v1 (`c1-measure.py`) and r36 v2
(`c1-measure-v2.py`) counters' input loading and output semantics, and verify that the r37
adapter (`replay-empty-panel.py`) feeds them an equivalent empty panel and that the receipts'
`mode=control` labeling is produced by the counters' own branches. Read-only investigation of
the lane; no installs performed (none needed); no edits to any lane file.

## 1. Counter input loading (identical in v1 and v2)

- `load_copies_rev(lane, rev, reldir)` — `.ufo/evidence/round-35/c1/c1-measure.py:279-293`
  and `.ufo/evidence/round-36/c1/c1-measure-v2.py:296-310`: `git ls-tree -r --name-only
  <rev> -- <reldir>`, keep entries ending `.json` whose basename is not `manifest.json`
  (HYGIENE-1, docstring :280-283 "a manifest, never a specimen"), sort, `git show` each,
  `json.loads`, flatten via `_docs_to_copies` (v1 :253-264, v2 :270-281: a top-level doc is
  one copy; a `copies` list is expanded, each tagged with its file).
- The public panel read is hardcoded inside both `main()`s:
  v1 :452 / v2 :469 — `pub = load_copies_rev(lane, rev, '.ufo/evidence/round-35/c1/panel')`.
  Slot counts derive from the copies themselves (`pub_kill_slots`, `pub_accept_slots`,
  v1 :453-455); `pub_slots = pub_kill_slots + pub_accept_slots` (print args v1 :522-528).
- Sealed set: same loader at the `--sealed` relpath, plus freeze/provenance gates (v1 :467-500).
- Runner: `git show <rev>:tools/mutate-and-run.sh`, pinned `PIN_RUNNER=a7d3f2dd…` (v1 :21, v2 :64).
- Tool: deciding mode reads `tools/tally-audit-v3.py` at REV; control mode (`--tool PATH`)
  reads an absolute path from disk or `<rev>:<path>` from Git (v1 :436-446, v2 :453-463).

## 2. Counter output semantics and branches

- Per copy: `COPY %-5s %-34s %s div=… rc=… checks=… pass=…` (v1 :382-383; `UNSAFE` :353,
  `INVALID` :348/:366). Then one predicate line
  `<label>: mode=<m> tool_present=… tool_sha=<16> tool_sha_ok=… runner_sha_ok=…
  pub_kill=<k>/<slots> pub_accept=<a>/<slots> pub_slots=<s> pub_distinct=<d> ho_…=…
  sealed_after_freeze=… rev=<rev> <label>_PASS=<bool>` (v1 :522-528, v2 :546-552).
  Exit 0 iff `ok`.
- Mode labeling is the counters' own branch logic: `--before` prints `mode=before …
  *_PASS=false` and returns 1 (v1 :431-434, v2 :448-451); otherwise `label='C1_R35'`
  → `'C1_R35_CONTROL'` when `a.tool` (v1 :436-438), `label='C1_R36V2'` →
  `'C1_R36V2_CONTROL'` (v2 :453-455), and the mode field prints
  `'control' if a.tool else 'deciding'` (v1 :522-528 args, v2 :546-552 args).
- `tool_sha_ok = tool_bytes is not None and (a.tool is not None or tool_sha == TOOL_SHA256)`
  (v1 :445-446 area, v2 :462-463 area): the counter itself pins the tool digest only in
  deciding mode (`TOOL_SHA256=6188db16…` v1 :24 / v2 :65). In control mode the digest pin is
  external — the adapter (:90-94) and c2-repin.py (:50-53) enforce it.
- Predicates:
  - v1 `ok` v1 :516-520: `pub_kill == pub_kill_slots and pub_accept == pub_accept_slots` plus
    runner/tool pins and unconditional sealed-set gates (`ho_kill_total >= 4`,
    `ho_accept_total >= 2`, `ho_kill == ho_kill_total`, `ho_accept == ho_accept_total`,
    `ho_invalid == 0`, `sealed_ok`). On a zero-slot panel the public conjuncts hold vacuously
    (0 == 0) — exactly the defect v2's docstring records (v2 :10-12).
  - v2 `ok` v2 :538-544: adds frozen targets `PUB_KILL_SLOTS_TARGET=6`,
    `PUB_ACCEPT_SLOTS_TARGET=3`, `PUB_DISTINCT_TARGET=9` (v2 :68-70; frozen in
    `.ufo/evidence/round-36/contract.json` C2 `frozen_targets`, `counter_sha256=9eb8944c…`).
    A zero-slot panel fails on `pub_kill_slots == 6` ⇒ `C1_R36V2_PASS=false`, exit 1.
  - So on any empty panel the frozen pair necessarily yields v1 PASS / v2 FAIL — the adapter's
    expected divergence is the counters' own semantics, not an adapter artifact.

## 3. How the r37 adapter feeds the panel, and equivalence

- `.ufo/evidence/round-37/control/replay-empty-panel.py` execs each counter's committed bytes
  at `--rev` (:104-107), then wraps `namespace["load_copies_rev"]` (:118-123): only when
  `reldir == SOURCE_PANEL` (the hardcoded public path, :17) does it call the original loader
  with `(lane, panel_rev, EMPTY_PANEL)` (:18). Sealed and every other reldir stay at `--rev`.
  `sys.argv` forces `--tool tools/tally-audit-v3.py` (:129-130), so both counters run in
  control mode; `--sealed` defaults to the committed r35 sealed dir.
- SETUP gates pin the input: source panel tree at d9c496b equals the manifest's
  `source_panel_tree`, 9 specimens, expected 0 (:72-75); specimen basenames equal the
  manifest's `source_specimens` list, len 9 (:82-84); the empty-panel tree at `panel_rev` is
  exactly `[empty-panel/manifest.json]` (:85-89); tool bytes at `--rev` hash to
  `FROZEN_TOOL_SHA256=6188db16…` (:24, :90-94) — the same digest both counters pin for
  deciding mode, so control-mode bytes equal deciding-mode bytes.
- Equivalence chain (why "equivalent empty panel" holds):
  - The committed manifest `.ufo/evidence/round-37/control/empty-panel/manifest.json`
    declares source `d9c496b…`, panel tree `4f3d8af5…`, the 9 specimen names, mutation
    "Remove all nine JSON specimen files … retain only this manifest", `expected_specimen_count: 0`.
  - The counters' own loader ignores `manifest.json` (HYGIENE-1, §1), so the manifest-only
    tree yields zero copies — behaviorally identical to the unreachable r36 scratch mutant
    `91373d55…`, which physically deleted the files. r36 receipts
    (`.ufo/evidence/round-36/control/v1-at-emptypanel.stdout`,
    `v2-at-emptypanel.stdout`) show that scratch run reporting
    `pub_kill=0/0 pub_accept=0/0 pub_slots=0 pub_distinct=0` in deciding mode at `rev=91373d55…`.
  - The r37 control receipt (`.ufo/evidence/round-37/control/replay-at-final-control.stdout`)
    shows the identical public surface (`pub_kill=0/0 pub_accept=0/0 pub_slots=0
    pub_distinct=0`) and identical sealed surface (`ho_kill=4/4 ho_accept=3/3 ho_invalid=0
    ho_distinct=7 sealed_after_freeze=1`), identical pins (`tool_sha=6188db16de045f29`,
    `runner_sha_ok=1`), and counter digests `COUNTER_SOURCE v1 sha256=d360a159…` /
    `v2 sha256=9eb8944c…`. The only deltas vs the scratch run are provenance
    (`91373d55…` → resolvable `d9c496b…`) and mode (`deciding` → `control`).
- Ground truth re-checked this session (read-only):
  - `git cat-file -e 91373d55557fe26c431e9e3dd9e8fa4a00d7b57f^{commit}` →
    `fatal: Not a valid object name …`, exit 128 (still unreachable).
  - `git rev-parse d9c496b…:.ufo/evidence/round-35/c1/panel` →
    `4f3d8af5b62ba04a5ff825bfdaec6c9193f8489e`; `git ls-tree -r --name-only d9c496b… -- …/panel`
    → exactly the 9 manifest names.
  - `git ls-tree -r --name-only c2b08d70… -- .ufo/evidence/round-37/control/empty-panel` →
    only `manifest.json`; `merge-base --is-ancestor c2b08d70… HEAD` → 0 (HEAD=e6185d5).
  - `git show d9c496b…:{c1-measure.py,c1-measure-v2.py,tools/tally-audit-v3.py} | sha256sum`
    → `d360a159…`, `9eb8944c…`, `6188db16…` — all three match the receipt's COUNTER_SOURCE
    lines, the r36 contract's `counter_sha256`, and both counters' `TOOL_SHA256`.
  - Live reproduction: `python3 .ufo/evidence/round-37/control/replay-empty-panel.py --lane .
    --rev d9c496b… --panel-rev c2b08d70… --work-root /tmp/r37-counter-fidelity/work` →
    exit 0 after 223 s; `diff` against the committed `replay-at-final-control.stdout` is
    empty (byte-identical, including both `COUNTER_SOURCE` lines and the final
    `EMPTY_PANEL_REPLAY: … v1_pass=1 v2_reject=1 EMPTY_PANEL_REPLAY_PASS=true` line).

## 4. mode=control labeling matches the counters' own branches

- The receipts say `mode=control` because both counters took their own `--tool` branch:
  label `*_CONTROL` (v1 :436-438, v2 :453-455) and mode field `'control'` (v1 :522-528,
  v2 :546-552). The adapter's acceptance gates grep exactly these tokens plus exit codes:
  v1 rc 0 + `C1_R35_CONTROL_PASS=true` + `mode=control` + `tool_sha_ok=1` + `pub_kill=0/0`
  + `pub_accept=0/0` (:146-148); v2 rc 1 + `C1_R36V2_CONTROL_PASS=false` + same tokens +
  `pub_slots=0` + `pub_distinct=0` (:149-152). The counters cannot be made to print
  `mode=control` except through their own branch, so the label is first-party.
- The calibration counter independently re-validates the receipt:
  `.ufo/evidence/round-37/calibration/measure.py:74-84` requires `mode=control`,
  `EMPTY_PANEL_REPLAY_PASS=true`, `counter_rev == manifest.source_revision` (d9c496b), and
  `panel_rev` resolvable and an ancestor of the measured rev, against
  `REPLAY_RECEIPT=.ufo/evidence/round-37/control/replay-at-final-control.stdout` (:13).
- Receipt lineage (git log on the adapter): `65b799d` separate counter and panel revisions →
  `21b96a2` align replay checks with counter output → `7397981` label mutant counter runs as
  controls. `replay-at-final-fixed.stdout` is the superseded deciding-mode run (labels
  `C1_R35:`/`C1_R36V2:`, which the current adapter would reject for lacking `mode=control`);
  the canonical receipt is the control one.
- C2 interplay, no conflict: the adapter pins the r35/r36 tool digest at `counter_rev`, so the
  C2 tool extension (new pin `da8c1ef4…`) cannot perturb the control replay. The re-attestation
  at the new pin (`.ufo/evidence/round-37/c2-repin-after.stdout`) shows v2's frozen targets
  restored on the full 9-specimen panel (`pub_kill=6/6 pub_accept=3/3 pub_slots=9
  pub_distinct=9`, `C1_R36V2_CONTROL_PASS=true` at rev `ae9b771a…`) — the same counters, same
  output grammar, full panel.
- Calibration counter live: `python3 .ufo/evidence/round-37/calibration/measure.py --lane .
  --rev HEAD` → `C1_R37: unresolved_control_inputs=0 old_mutant_resolves=0 correction=1
  manifest_ok=1 receipts_ok=1 rev=e6185d5… C1_R37_PASS=true`, exit 0 (recorded chain:
  `before-final-control.stdout` =1/false at d9c496b → `after-control-final.stdout` =0/true at
  32826f37; `.exit` files 1 and 0).

## 5. Observations (no claim impact)

- Docstring vs predicate: "control … never needs sealed" (v1 :29, v2 :41) is true only for
  *scoring the public surface*; the sealed-set gates sit unconditionally in `ok`
  (v1 :516-520, v2 :538-544), so a control run without `--sealed` would print
  `*_CONTROL_PASS=false`. The adapter always passes `--sealed`, so receipts are unaffected.
- In control mode the counter does not itself verify the tool digest (`a.tool is not None`
  short-circuits the pin); the adapter (:90-94) and c2-repin.py (:50-53) carry the pin, per
  the adapter docstring ":2-6".
- Control-mode receipts still print the 7 sealed `COPY` lines (sealed copies are scored when
  `--sealed` is given); the adapter's v1/v2 acceptance ignores `ho_*` fields, so the verdicts
  rest on the public tokens and exit codes only.

## Confidence

High. Every semantic statement above is anchored to read code; every provenance statement to a
command run this session; the adapter receipt was reproduced byte-identically live. The §5
notes are observations on counter-internal redundancy, not claim widening.
