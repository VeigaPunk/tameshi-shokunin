# ResMonitorReanchor-5 — residual falsification (Tameshi round24)

Seat: reviewer (read-only; no production file edited; no git/jj write command run in
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`; the fleet repo and sibling lanes untouched).
Scratch/clone (per L1 host directive, not `/tmp`):
`/fast/scratch/hyaku/tameshi-r24/ResMonitorReanchor-5/` (clone: `.../clone`).
Tools installed/updated: **none** (no package was needed; every check ran on stdlib + `git` +
`/usr/bin/strace 7.2`, already present).

---

## Verdict

**PASS on all three attacked points, with two documentation-grade nits (M1, M2) and no
correctness defect found.**

1. **`.ufo/evidence/round-24/source-traces-B/{source-6,source-1938}.json` are genuine
   `tools/trace-inputs.py` runs bound to rev `250069f1b4ea735cbe89a0637a96af9fae640dca`, and their
   inputs equal the prior ledger entry's planned paths.** I reproduced both receipts byte-for-byte
   with the frozen tool at that rev; every recorded input digest equals that rev's blob content; the
   argv path list equals the appended ledger entry's `inputs` key set, which equals the
   immediately-preceding ledger entry's path set exactly.
2. **The ledger prefix is byte-preserved.** `source-prefix-preservation-B.json` is honest on all four
   counts (prior 282 / appended 2 / current 284 / `prefix_bytes_unchanged: true`) and its
   `prefix_entries_sha256` reproduces exactly under the lane's established canonicalization.
3. **`monitor-intermediate-B.json` is an honest retained harmed intermediate at 60/62.** My
   independent re-run of the identical command produced **byte-identical stdout** (sha
   `fa111be944959fec58e77b059339943d5e848b01e55dbecf685e96d718fe96a1`, incl. all 1202
   `external_inputs` digests). It is a faithful capture, not a transcription.

Supporting: the C1 counter reproduces **before 1/11 @ `6a1821a`** and **after 11/11 @ `c8c5b88`
*and* @ the final tip `4903959`** — i.e. no tool/fixture/ruler/registry drift after wave 1.

Nothing here is producer authentication, promotion, or a numeric score uplift.

---

## 1. Assigned run — coldread selector in rev mode

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
python3 .ufo/evidence/round-21/coldread/measure.py \
        --repo /home/vgpnk/Projects/shokunin/tameshi-shokunin \
        --rev 4903959687d16623adeeeae059bc010dcfc9d23f --explain
```
Observed: **exit 0**, wall 9.2 s, stdout JSON on `coldread-rev.json` (240 329 B).

| Axis | Observed value |
|---|---|
| **sections covered / total** | **62 / 62** (`coldread.sections_covered=62`, `coldread.sections_total=62`) |
| **restraint** | **8** (`calibration_restraint_score=8`) |
| **depth** | **8** (`depth_score=8`) |
| **overrides** | **false** (`overrides_used=false`) |
| missing / uncovered | `coldread.missing=[]`, `coldread.uncovered_headings=[]` |
| credit reasons | `{"credited": 62}` (single reason class) |
| ledger source | `ledger_source="rev"` (measured at the commit, not the worktree) |
| trace gate | `trace_gate="strict"`, `inputs_overlay_merged=0`, `ledger_committed=true` |
| recorded cases | `recorded_cases=8`; `ledger_legs` = 8 legs (js-kimi-census, bash-surface-census, bash-tsukuroi-census, bash-mado-verify, bash-checklist-run, js-claims-check, js-round-gate, js-sources-check) |
| ledger guardrail | `header_legs=8`, `regression_calls=8`, `selftest_tuples=8`, `unique_recorded_gates=8`, `lists_agree=true` |
| shonen boxes | `boxes=4`, `asserted=4`, `marks=["~","~","~","~"]`, `box3_ledger_link/marked/points=true`, `checked=0`, `untouched=0` |
| sources census | `rows=83`, tiers A74/B7/C2, status mined54/queued23/rejected6, `malformed=0` |

Nit (documentation, not a defect): the round-24 counter
`.ufo/evidence/round-24/measure.py` **does not accept `--rev`/`--explain`** —
`argparse` error, exit 2 (`usage: measure.py [-h] --repo REPO`). The `--rev/--explain` CLI belongs
to the round-21 coldread *selector* (`.ufo/evidence/round-21/coldread/measure.py`, which delegates
to the frozen round-18 credit algorithm). Two different rulers; I exercised both (§5).

---

## 2. Attack A — are the `source-traces-B/*.json` real trace-inputs runs bound to `250069f1`?

### A.1 Receipt shape
`.ufo/evidence/round-24/source-traces-B/source-6.json`, `source-1938.json` (both present at tip
`4903959`; `git diff 4903959 -- .ufo/evidence/round-24/` empty).

```
schema=tameshi-trace-inputs-v1  rev=250069f1b4ea735cbe89a0637a96af9fae640dca  rev_reason=None
tracked_filter=True  exit=0  untracked={}  external={}  live_lane_reads={}  dropped_home_count=0
inputs: 21 (source-6) / 15 (source-1938)
cwd=root=/tmp/tameshi-r23-reanchor-final-w_543he9/lane
```

### A.2 Every recorded digest equals that rev's blob content
For each `inputs` key I compared the recorded sha256 with `sha256(git show 250069f1:<path>)`:

```
source-6.json     : all 21 inputs match rev 250069f1 content  -> mismatches: NONE
source-1938.json  : all 15 inputs match rev 250069f1 content  -> mismatches: NONE
```
(e.g. `corpus/QUALITY.md` = `b0800d1a…`, `tools/registry.json` = `a8f255f1…`,
`corpus/knowledge/mutation-case-kumitate-sources-check.md` = `d961a0d6…` — all post-errata
digests, i.e. the run saw the post-`250069f` tree.)

### A.3 Inputs == the prior entry's planned paths
The traced command's planned path list is `argv[6]` (a JSON array). Ledger entries 283/284
(appended at `671a6e2`) carry `inputs` with exactly those keys; the sole extra recorded read is
`SKILL.md`, which the ledger carries separately as `skill_sha256`:

```
entry 283 (start 6,   end 16  )  planned=20  ledger inputs=20  planned == inputs keys : True
entry 284 (start 1938,end 1963)  planned=14  ledger inputs=14  planned == inputs keys : True
entry 283 skill_sha256 fcc50f9ee189d5be9c56ae7a96bda87824fd31daaa671c0a92365fd58aec60ab
          == sha256(SKILL.md @ 250069f1)                                      : True
```
Immediate prior ledger entries for the same sections (in the 282-entry `c8c5b88` ledger) have
**identical** path sets:
```
idx 267  section   6-16  read_rev bd38c02  inputs 20  planned-path set == new trace inputs : True
idx 280  section 1938-1963 read_rev bd38c02  inputs 14  planned-path set == new trace inputs : True
(also idx 249/264 and 262/265 from round-23: True)
```
Only the digests moved (e.g. `corpus/QUALITY.md` `9959bf4e…` → `b0800d1a…`), i.e. the re-anchor
refreshed the same planned path set at the new rev — exactly the intended shape.

### A.4 Section identity is the rev's own content
Using the frozen ruler's own `sectionize()` (imported from `.ufo/evidence/round-18/measure.py`):

```
rev 250069f1 : section 6-16   sha 79aa3f5ed3172c11837dac2fdbb70d1aca91b1bcc7dd51b42231cfd17256bb30
               section 1938-1963 sha 27fc0d2e4c5278283ba66d053d83583f0fcd047bf04fddd825ba88eb8d4b4c74
ledger 283.sha256 = 79aa3f5e…  ✔     ledger 284.sha256 = 27fc0d2e…  ✔
rev 4903959 : identical section hashes and identical skill_sha256 → credit holds at the tip
```

### A.5 Independent reproduction (the decisive test)
Private clone (`git clone --no-hardlinks` → `.../clone`), checked out `250069f1`, frozen
`tools/trace-inputs.py` run with the recorded argv:

```
tools/trace-inputs.py sha256 @250069f1 = f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4
source-refresh-receipts-B.json observation instrument_sha256 = f59c9312…               → MATCH

my receipt (source-6)     : rev 250069f1…  rev_reason None  tracked_filter True  exit 0
                            inputs identical to recorded : True (21/21)
                            untracked/external/live_lane_reads identical : True
my receipt (source-1938)  : inputs identical to recorded : True (15/15)
re-running the traced command:
   observation 0 stdout identical : True  (sha 776fa3429fe09b71…)   stderr identical : True
   observation 1 stdout identical : True  (sha d2459189cf4c3878…)   stderr identical : True
```
So the receipts are the real product of the frozen instrument, not hand-authored. The recorded
invocation shape (`.ufo/evidence/round-24/source-refresh-receipts-B.json`, `read_revision =
250069f1…`) is
`python3 <clone>/tools/trace-inputs.py --root <clone> --out <repo>/.ufo/evidence/round-24/source-traces-B/source-6.json -- python3 -c <script>`,
`cwd=<clone>`.

### A.6 Cross-artifact consistency
`.ufo/evidence/round-24/source-refresh-entries-B.json` (`entries[2]`) is **field-for-field identical**
to `ledger.json[-2:]` (same key set, zero differing fields). `read_revision`/`read_rev` agree
(`250069f1…`).

**Conclusion A: the two B trace receipts are actual trace-inputs runs bound to `250069f1`, and their
inputs equal the prior entry's planned paths. No defect.**

---

## 3. Attack B — is the ledger prefix byte-preserved?

`source-prefix-preservation-B.json` claims `prior_entries=282`, `appended=2`, `current_entries=284`,
`prefix_bytes_unchanged=true`, `prefix_entries_sha256=9d80b01c…`.

Independent check (read-only `git`):

```
ledger entry counts:  c8c5b88 = 282   671a6e2 = 284   4903959 = 284
  -> prior/appended/current = 282/2/284                                  ✔
  -> 671a6e2 (the B append) touched only 7 files; 4903959 touched NO ledger file
     (`git show --name-only 4903959 | grep ledger` → nothing)          ✔
prefix equality:
  sha256(json.dumps(entries[:282], sort_keys=True))
     c8c5b88 (all 282)      = 91e80b4b0fddd00329cef521f24680284c4a3d16e95406b7c926ad495bdcae54
     671a6e2 (first 282)   = 91e80b4b…  IDENTICAL                     ✔
     4903959 (first 282)   = 91e80b4b…  IDENTICAL                     ✔
  raw file bytes: c8c5b88 vs 671a6e2 identical for the first 1 565 787 bytes;
     the only difference is the insertion point ("," -> ",\n{…") — prior entry bytes untouched  ✔
claimed digest reproduces exactly:
     sha256(json.dumps(entries[:282], sort_keys=True)) @ c8c5b88 = 9d80b01c61070b293cc948279952d0f0bbc2524397082f74f5d8bfe788d3f234
     claimed prefix_entries_sha256                             = 9d80b01c61070b293cc948279952d0f0bbc2524397082f74f5d8bfe788d3f234   ✔
same convention confirmed on two independent prior instances:
     round-23 final  (264 entries @336565f) -> 038fe060…  == claimed 038fe060…   ✔
     round-24 A      (267 entries @bd38c02) -> dcc2a073…  == claimed dcc2a073…   ✔
non-`entries` top-level keys (schema, carried_from, provenance, round21_provenance):
     unchanged c8c5b88 -> 671a6e2 -> 4903959 (key set equal, values equal)         ✔
```
**Conclusion B: `source-prefix-preservation-B.json` is honest on every field; the ledger prefix is
byte-preserved and the two appends are append-only. No defect.**

---

## 4. Attack C — is `monitor-intermediate-B.json` an honest retained harmed intermediate (60/62)?

### C.1 Envelope
```
argv = [python3, <repo>/.ufo/evidence/round-21/coldread/measure.py, --repo, <repo>, --rev,
        250069f1b4ea735cbe89a0637a96af9fae640dca, --explain]
cwd = <repo>   exit = 0   stderr = ""   revision = 250069f1b4ea735cbe89a0637a96af9fae640dca
instrument_sha256 = 657f009bdf1cc89ac614ed7c8424858f5f802b5a5330d8917db788f67982f3eb
  == sha256(.ufo/evidence/round-21/coldread/measure.py) @250069f1  ✔  == @4903959  ✔ (ruler unchanged)
note = "harmed intermediate 60/62, restraint 6 after replacement-L1 QUALITY.md errata append
        (input drift on QUALITY.md); stdout captured by shell redirect"
```
### C.2 Reproducibility — the receipt is a faithful capture
I re-ran the identical command (same argv, same repo, `--rev 250069f1…`):

```
recorded stdout sha256 = fa111be944959fec58e77b059339943d5e848b01e55dbecf685e96d718fe96a1
my rerun   stdout sha256 = fa111be944959fec58e77b059339943d5e848b01e55dbecf685e96d718fe96a1   IDENTICAL
  -> including all 1202 coldread.external_inputs digests (0 differ)
  -> parsed values identical field-by-field (restraint 6, depth 8, overrides false,
     ledger_source rev, trace_gate strict, 60/62, missing =
     ["# tameshi-shokunin", "### Round-20 gate/probe registry — frozen receipt instruments"])
```
### C.3 The harm story is causally correct, not a coincidence
```
corpus/QUALITY.md digest:  c8c5b88 = 9959bf4e…   bd38c02 = 9959bf4e…
                           250069f1 = b0800d1a… (the E–N / QUALITY49 errata append)
                           671a6e2  = b0800d1a…   4903959 = b0800d1a…
the two drifted sections are exactly the two whose ledger entries listed corpus/QUALITY.md
  -> at 250069f1 the prefix entries still record 9959bf4e => input-drift => 60/62, restraint 6
  -> the two B entries record b0800d1a => credit restored
```
### C.4 The lesson text that cites it is accurate
`corpus/lessons/round-24.md` (Mistakes addendum, replacement L1), line 220:
> "errata append drifted the source monitor | QUALITY.md append at 250069f → monitor 60/62, restraint 6
> (`monitor-intermediate-B.json`) | strict monitor input-drift | two actual traced re-reads
> (`source-traces-B/`) restore 62/62 at 671a6e2. Shown able to fail: the retained B receipt"

Both halves verified independently:
```
re-run at rev 250069f1 : 60/62, restraint 6   (== monitor-intermediate-B, byte-identical stdout)
re-run at rev 671a6e2 : 62/62, restraint 8    (== "restore 62/62 at 671a6e2")
re-run at rev 4903959 : 62/62, restraint 8    (== the assigned run, tip)
```
### C.5 A vs B are two distinct intermediates, both honestly retained
```
monitor-intermediate-A.json : revision bd38c02…  covered 47/62  restraint 6
                               note "harmed intermediate 47/62, restraint6 after round24 implementation edits"
monitor-intermediate-B.json : revision 250069f1… covered 60/62  restraint 6
                               note "harmed intermediate 60/62, restraint 6 after replacement-L1 QUALITY.md errata append"
stdout sha: A 747fe2b75145e252…  B fa111be944959fec…  (different, as they should be)
```
No contradiction: A is the earlier (implementation-edit) intermediate, B the post-errata one; each
retains a distinct, reproducible capture.

**Conclusion C: `monitor-intermediate-B.json` is an honest retained harmed intermediate at 60/62 with
restraint 6, reproducible byte-for-byte. No defect.**

---

## 5. Supporting checks (C1 calibration, no drift after wave 1)

```
clone @ 6a1821a8897eea6e7d9669292160ec9593669409, frozen counter .ufo/evidence/round-24/measure.py
   -> discriminated 1 / 11   (only K4 discriminated; K1,K2,K3,K5,K6,K7,K8,K9,K10,K11 not)
   -> matches contract.before {discriminated:1, total:11}                      ✔
clone @ c8c5b88c8e961a929cdc351b95a7074c76958909
   -> discriminated 11 / 11                                                      ✔ (after.json)
clone @ 4903959687d16623adeeeae059bc010dcfc9d23f (final lane tip)
   -> discriminated 11 / 11 (K1..K11 all True)                                  ✔ no drift
git diff --stat 250069f 4903959 -- tools/ .ufo/evidence/round-24/measure.py .ufo/evidence/round-21/ .ufo/evidence/round-23/
   -> only .ufo/evidence/round-21/coldread/ledger.json (+92 lines)              ✔ no tool/fixture/ruler/registry byte changed
```
Run context: all execution happened in `/fast/scratch/hyaku/tameshi-r24/ResMonitorReanchor-5/`
(`TMPDIR` redirected there; the frozen counter's `tempfile` work area was kept off the full `/tmp`).

---

## 6. Residual risk / verification gaps

* **M1 (documentation, low).** `source-prefix-preservation-B.json` omits the attestations its
  round-23 precedent carries (`prefix_byte_length`, `prefix_entries_equal_as_data`,
  `other_top_level_keys_unchanged`) and never states the digest canonicalization; I had to recover
  it (`sha256(json.dumps(entries_prefix, sort_keys=True))`) and confirm it on two independent
  instances. An independent verifier cannot recompute the digest from the file alone.
* **M2 (documentation, low).** The B trace receipts' `cwd`/`root` is
  `/tmp/tameshi-r23-reanchor-final-w_543he9/lane` — a round-23-era temp path (the L1 host directive
  reports `/tmp` filled earlier). The receipts are therefore not re-runnable *in place*; they are
  content-verifiable only (which I did — full byte-identical reproduction in a fresh clone).
  Cosmetic naming oddity: a round-24 re-anchor executed inside an `r23`-named clone.
* **Not attacked (out of my item):** the 64-seat wave-1 accounting, the errata E–P dispositions and
  the routed-defect table in `corpus/knowledge/replay-projection-hardening.md` (other residual seats).
  I did confirm the one corpus sentence that cites my artifacts (`corpus/lessons/round-24.md:220`)
  is factually correct.
* **Environment caveat.** The `external_inputs` block (1202 fleet-root paths) is read from the live
  fleet root; my re-run matched it exactly today, so the fleet files cited are unchanged since the
  capture.

## 7. Smallest safe correction

None required for correctness. If the lane wants the nits closed, the minimal append-only edit is to
add to `source-prefix-preservation-B.json` (and, for symmetry, `source-prefix-preservation.json`):

```json
"digest_canonicalization": "sha256(json.dumps(entries_prefix, sort_keys=True))",
"prefix_byte_length": <first-differing-byte offset of the prior ledger file>,
"prefix_entries_equal_as_data": true,
"other_top_level_keys_unchanged": true
```

No ledger byte, tool byte, fixture byte, ruler byte or registry byte changes; the digests already
published remain valid. (I did **not** apply this: my item forbids editing production files, and
`source-prefix-preservation-B.json` is a committed production artifact owned by the L1 integrator.)
