# T50W2RevSuccessor — R49.2 closure review (round 50, wave 2)

Item: routed defect R49.2 (`corpus/lessons/round-49-verifier-spotcheck.md:123`, frozen keys `absent` / `differential` / `successor counter`, routed_at `e3729de8`). Reviewed instruments at the attacked content revision `80ea77e9` (read via `git show 80ea77e9:<path>`): `.ufo/evidence/round-50/successor/reads-v2.py` and `.ufo/evidence/round-50/successor/sandboxed-confirm.py`. All tool runs in scratch `S=/fast/scratch/hyaku/tameshi-r50/T50W2RevSuccessor`; receipts copied to this directory. A probe is never a verdict; the L1 decides the claim.

## Ask 1 — does reads-v2 cap and evidence `absent`? YES
- R1 (`reads-v2.py:451-482`): an `absent` row passes only with `absent_evidence` = `{path == raw token; history == git log --all --format=%H -- <path>` and empty; `not_a_file` quote 15–400 collapsed chars, contains the token, matches NOT_A_FILE_RE (`:94-96`), occurs in the section text}`. Anything else scores `absent_bad`.
- Cap: per-section counter, `absent_overflow` = sum(max(0, n−1)) (`:477-479`); both terms are in `total` (`:663-698`).
- Selftest (`TMPDIR=$S/w python3 -I reads-v2.py --selftest`, exit 0): `R1-absent-needs-evidence`, `R1-absent-history-empty`, `R1-absent-history-unrecorded`, `R1-quote-not-a-file`, `R1-quote-not-in-section`, `R1-quote-token-missing`, `R1-absent-cap-per-section` all PASS; `READS_V2_SELFTEST: cases=22 failed=0 measure_calls=28`.
- Real data at `bda60768` (round-49 deciding rev): the round-49 reads.json's evidence-less absent rows are scored `absent_bad=3` + `absent_overflow=1` — i.e. the old "no evidence, uncapped" behavior no longer passes.

## Ask 2 — does reads-v2 extract the missed forms? YES
- R2 regexes (`:87-89`), extraction (`:196-247`), resolution (`:309-350`): `§N` / `§N-§M` / `§N–§M` (block of the numbered heading `^#{1,6} N[.)]`), `FILE#frag` (heading-slug block), `dir/prefix-*.ext` globs (expansion at REV must equal the row's `files` exactly, via `git ls-tree -r`).
- Selftest: `census-forms` expects exactly `[alphabet.md, disc.md, ghost.py, §1, §3-§6, disc.md#box-1, corpus/knowledge/case-*.md]` (PASS); `census-section-region` / `census-anchor-region` / `census-glob-files` PASS; `R2-section-needs-row`, `R2-section-region`, `R2-anchor-needs-row`, `R2-glob-expansion-bound` PASS (a tenth glob file cannot pass unnoticed).
- Real SKILL.md at `bda60768`: 17 section + 1 anchor + 1 glob pointers extracted over the legacy 94 (`new=17/1/1`); every one resolves to a region (PTR lines print resolved ranges). They are `unverified=19` only because round-49 reads.json has no rows for them.

## Ask 3 — does reads-v2 refuse empty traces? YES
- R3 (`check_traces`, `:581-626`): a receipt with empty `inputs` scores `trace_empty`; an empty receipt set scores `trace_missing`; both are terms of `total`.
- `--trace` is mandatory: run without it exits 64 with `READS_V2: usage=--trace required (R3 refuses an unrecorded trace)` (observed).
- Selftest `R3-trace-empty-refused` and `R3-trace-missing-refused` PASS.

## Ask 4 — does the sandbox really hide the pristine guard (negative control)? YES
- Namespace (`sandboxed-confirm.py:222-236`): only `/run/{pbt-staged-id.py, staged-id-guard.py, scratch/}` plus read-only `/usr /lib /lib64 /etc/ld.so.cache /etc/alternatives(if present)` and `/proc /dev`; no `/home`, `--unshare-all`, `--clearenv`.
- Probe (`:95-133`) runs inside that namespace: lane guard path unopenable, lane panel unopenable, `/home` absent, exactly one `staged-id-guard.py` visible sha-pinned to the guard under test, `git -C lane` fails → `ok=true` for the baseline leg and all 12 mutant legs (`probes_ok=true`).
- Leak-detection positive control: selftest `probe-detects-bound-lane` binds the fixture lane read-only and requires the probe to fail — PASS (`leaked_probe_ok=False guard_open=True`).
- Independent check (this seat, `T50W2RevSuccessor.procprobe.out`): inside an identical-namespace sandbox, `/proc` exposes only namespace-local pids (`proc_pid_count=2`, `visible_pids=["1","2"]`), no `/proc/<pid>/root` host access, no `/home`, `guard_leak_pids=[]`.

## Ask 5 — are the committed receipts what the tools print? YES
- Tool shas pinned: reads-v2.py sha256 `a01d88d119d0…42cc9` (equals self-printed `self=a01d88d119d0`); sandboxed-confirm.py sha256 `1bbdc3b188d8…c6db2`; both byte-identical to the w1 files (T50ExecSuccC1/C2) at 80ea77e9.
- `reads-v2` at `bda60768` re-run with the receipt's argv (trace paths `.ufo/evidence/round-49/coldread/refresh-receipts.json` + `.ufo/evidence/round-49/coldread/traces`): stdout byte-identical to committed `reads-v2.at-bda60768.stdout` (`diff` empty; `total=23 READS_V2_PASS=false`, exit 1).
- `sandboxed-confirm` panel re-run (same argv, rev `e3729de8`, seed 4949, 400 cases, panel `.ufo/evidence/round-49/c2/panel.json`): stdout identical to committed `sandboxed-confirm.r49-panel.stdout` modulo the `SANDBOXED_CONFIRM_OUT` scratch path (`confirmed=12/12 unconfirmed=0 probes_ok=true ok=true`, exit 0); receipt JSON identical after scratch-path normalization.
- Selftests: reads-v2 case-lines + summary identical to committed `reads-v2.selftest.stdout`; sandboxed-confirm selftest identical (18/18 checks, `failed=0 ok=true`) after scratch-root normalization (committed lines were recorded truncated at 512 B).
- `bwrap-version.txt` (`bubblewrap 0.13.1`) matches `/usr/bin/bwrap --version`.

## Findings by severity
1. [Observation — not a defect] `reads-v2` is still RED at head: at `80ea77e9` the run prints `total=23 READS_V2_PASS=false` (exit 1) — exactly the same numbers as at `bda60768`: 19 unverified new-form pointers (round-49 `reads.json` has no rows for them), 3 evidence-less `absent` rows, 1 overflow. The counter therefore *detects and scores* the round-49 gap (red-before), but the tree at head does not pass its own check. The round-49 `reads.json` is frozen evidence; nothing in this review modifies it, and a green run would require rows for the new forms (lane/L1 decision).
2. [Observation] `sandboxed-confirm` is explicitly a probe/executable spec (`sandboxed-confirm.py:3-23`, `:141-143` of the w1 report); the w1 seat itself records that a lane-path carrier (e.g. under `tools/`) is still needed for the actual C2 counter. The round-50 C2 measure (`.ufo/evidence/round-50/c2/measure.py`) is separate and not part of this review.
3. [Limit] Confirmation semantics are the round-49 ones (exit code + JSON minus the two sha fields on the single counterexample case); the harness inherits that definition as stated.

## Commands
```
sha256sum reads-v2.py sandboxed-confirm.py        # a01d88d119d0…42cc9 / 1bbdc3b188d8…c6db2
TMPDIR=$S/w python3 -I reads-v2.py --selftest      # 22/22, exit 0
python3 -I sandboxed-confirm.py --lane <lane> --selftest --work $S/selftest   # 18/18, exit 0
python3 -B reads-v2.py --lane <lane> --rev bda60768… --trace .ufo/evidence/round-49/coldread/refresh-receipts.json --trace .ufo/evidence/round-49/coldread/traces   # exit 1, total=23
python3 -B reads-v2.py --lane <lane> --rev 80ea77e9… --trace …   # exit 1, total=23
python3 -I reads-v2.py --lane <lane> --rev bda60768…   # exit 64 (usage)
python3 -I sandboxed-confirm.py --lane <lane> --rev e3729de8… --panel .ufo/evidence/round-49/c2/panel.json --work $S/w/run --out $S/w/run/sandboxed-confirm.json   # exit 0, ok=true, 12/12
bwrap … python3 -I /run/scratch/procprobe.py   # pid count 2, guard_leak_pids=[]
```

## Summary
- **Ask 1 YES** — reads-v2 R1 requires `absent_evidence` (path, empty history, not-a-file quote in section) and caps at 1 absent row per section; selftest R1a–d PASS; the old un-evidenced rows in round-49 reads.json are scored `absent_bad=3`/`absent_overflow=1`.
- **Ask 2 YES** — R2 extracts `§N`/`§N-§M`/`§N–§M`, `FILE#frag`, globs; census + per-form selftests PASS; real SKILL.md yields `new=17/1/1`.
- **Ask 3 YES** — R3 refuses empty-input receipts and empty receipt sets; `--trace` mandatory (exit 64 observed); R3a/R3b PASS.
- **Ask 4 YES** — probe passes all 5 isolation checks on every leg; leak-detection positive control PASS; my /proc probe shows only namespace-local pids, no host root, zero guard leaks.
- **Ask 5 YES** — reproductions byte-identical for the at-run and panel stdout, JSON-identical for the receipt; selftests match; self-sha and bwrap-version pins hold.
- The successor instruments exist, are byte-exact to the w1 originals, and behave as claimed; reads-v2 is red at head by design (round-49 reads.json has no rows for the new forms), and sandboxed-confirm is a probe — both documented.
