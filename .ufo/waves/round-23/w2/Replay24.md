## Row audited: `verify-round15` only (frozen contract `command-binding-round23-v1`, base `28cae179`)

### 1. Evidence: present vs inferred

**Actually present (verified from artifacts + git objects):**
- Frozen row in `requirements.json` == `registry-baseline.json` active row *exactly*: `argv=["python3",".ufo/evidence/round-15/verify.py","--rev","7650fe4d…"]`, `expect={exit:0, stdout_contains:["measure-historical-preserved: PASS"]}`, `kind=gate`, `timeout_s=60`, `source=SCORECARD.md@98bea7d:247`, `external=true`.
- Baseline source binding is exact: `verify.py@28cae179` takes a required `--rev` only; the token is emitted only at `record_check("measure-historical-preserved", hist.get("all_baseline_bytes_preserved")==1, …)` (lines 827–832); exit 0 iff `not failures` (lines 343, 361).
- The check is non-vacuous: baseline `a9cf4da` holds **599** blobs under round-12/13/14; **0** differ at `7650fe4d`, and baseline is an ancestor of the requested rev. `changed=[]` is meaningful.
- Full output, not a tail: bundle receipt `stdout` is **5193 bytes**, byte-identical to the observations row; 45 lines; token count exactly 1 at byte **5030**, line **42**, carrying `all_baseline_bytes_preserved=1 changed=[]`. `stderr=""`, `exit=0`, `elapsed_s=1.758` matches the interval (1.758157 s).
- Freshness, not retrofill: the stream contains scratch id `/tmp/tameshi-r15-verify-2aeav6pv/lane/tools/candidate.py`, which differs from the committed round-15 receipts (`-4pexcuhm`, `-bcmjaf6y`). This is a new execution, not copied historical output.
- Content identity across revisions: `verify.py` git blob `b38cbf4c…` (sha256 `7e4519d9…`) is **identical** at `28cae179` and `496d212b`; `measure.py` blob `353c4359…` identical at `7650fe` and `496d212b`; gate tool blob `23eab57c…` identical at `496d212b` and `336565f`.

**Declared/inferred, not observed:**
- `receipt.argv`, `cwd`, `revision` are copied from the row declaration and the compiler's checkout (`replay.py:62,68–69`); no `/proc/<pid>/cmdline` capture. Popen does exec `row["argv"]`, so the copy is *faithful for this producer* but not independent evidence.
- `cwd=/tmp/tameshi-r23-replay-naxu6fzi/...` is deleted; unverifiable post hoc.
- Replay artifacts do not exist at `496d212b`; they are first committed in `8f66b5d`/HEAD `336565f`.
- Part of exit 0 is **live-fleet**, not revision-local: `verify.py:105,836` hardcodes `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`. `external=true` is erased by the `{name,argv,expect}` projection, so the gate cannot see it.

### 2. Static binding vs field-level false acceptance
**Confirmed exact binding** for this row's `argv`/`expect` against baseline source (above). I did **not** find a within-row argv/token false acceptance.

**False acceptance found — the `revision` field:** `command-binding.py:107` compares `receipt.revision` to `bundle.revision`; both are the *same producer variable* (`replay.py:62,69`), so `REVISION_MISMATCH` is structurally impossible for any compiler-produced bundle. This row passes at `496d212b` while the contract's `base_revision` is `28cae179` and the frozen delivered implementation revision is `336565f`; neither gate, compiler, nor ruler reads the contract (`grep` for `contract`/`base_revision`: zero hits). The ruler's `revision-mismatch` case (`measure.py:39–40`) mutates only the receipt to `b*40` while the bundle stays `a*40` — it never tests a self-consistent stale bundle. For this row the mis-binding is *content-immaterial* (identical `verify.py` blob), but the field accepts whatever revision the producer declares.

**Concrete adversarial delta:** keep `argv`, `cwd`, `revision`, `exit=0` untouched and replace `.ufo/evidence/round-15/verify.py` at the receipt revision with `print("measure-historical-preserved: PASS"); raise SystemExit(0)` (or shrink the receipt stdout to that single 34-byte line). The gate binds no digest of the executed file, and `expected.json` is recomputed by the same producer (`replay.py:75`), so `evaluate` returns exit 0 / `[]` with no real execution. Residual after any revision fix: `held` is not in the bundle, and token search is over full stdout while the registry held check used the 4096-byte tail — a head-only token would pass the gate and fail the runner (this row's token is in the tail, so no current divergence).

### 3. Affected axes
Receipt-field observability ✗ (declared ≈ observed); contract revision authority ✗ (self-referential); attribution/hermeticity ✗ for this row (live census); full-stream retention ✓ (real improvement); adversarial discrimination ✗ (fixture-level, not producer-level).

### 4. Proposed move (one)
Add a **contract-authoritative binding block**: contract declares `implementation_revision=336565f` plus per-requirement `executed_script_sha256` (git blob content digest; `verify-round15 → 7e4519d9…`, identical at `28cae179`/`496d212b`), carry `external` through the frozen projection, and have the gate reject a receipt whose revision/script digest falls outside the contract instead of comparing to `bundle.revision`. This lets this row pass by blob equivalence at `496d212b` while making the producer's revision non-authoritative.

### 5. Risks
Contract/requirements schema must be re-frozen (frozen until seats return); a script digest still does not prove stdout came from that script (the single-line forgery survives); live rows (`pin-disposition-read`, census leg here) have no revision-local digest and would need an explicit non-hermetic finding rather than a silent pass; if L1 requires `receipt.revision == implementation_revision` strictly, replay must be re-run at `336565f`.

### 6. Verification (not executed in this wave)
Already read-only-verified: blob identity `b38cbf4c`; `ls-tree` 599/0; receipt/observation stream equality; scratch-id divergence from committed receipts. Post-move fixture check: the stub bundle must yield non-zero (`INVALID_RECEIPT`/`SCRIPT_MISMATCH`), not `0/[]`.

**Contradiction:** Target says write `.ufo/waves/round-23/w2/Replay24.md`; Context forbids all writes and says L1 persists. I wrote nothing. No installs, no registry command, suite, build, or formatter ran — only read-only file/git-object inspection. I make no claim about historical R17-CMD-BIND.
