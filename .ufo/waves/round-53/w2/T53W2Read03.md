# T53W2Read03 — re-read of `## Repeated controls and gate registry — round 12` at C**

Seat: T53W2Read03 (wave 2, re-read). Cand: `5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e` (C**).
Section bytes read from git objects only: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e:SKILL.md`.

**Verdict: 0 findings. Both wave-1 fixes are present in the C** bytes and every remaining statement in the section resolves at C**.**

## 1. Section identity (split verified before hashing)

Splitter used: `.ufo/evidence/round-16/measure.py` `sectionize()` at C** (its docstring is the frozen monitor's definition verbatim: heading `^#{1,3}(\s|$)` outside ``` fences, heading line through the line before the next heading, trailing whitespace-only lines stripped, `\n`-joined, no trailing newline, sha256 over UTF-8 bytes with `surrogateescape`). Run against the C** blob of `SKILL.md` it reports 64 sections (preamble included) and:

```
{'start': 1496, 'heading': '## Repeated controls and gate registry — round 12',
 'sha256': '2613c4fe5c89d2971d16622a0cf1888acc40b8c26a137b9c4bd120cc95053a96'}
```

Heading search on the same blob: 63 headings; this heading is index 42 at line 1496; the next heading is `### Gate/probe registry` at line 1516; the section is lines 1496–1514 (line 1515 is whitespace-only and is stripped), 19 lines including the heading.

`section_sha256 = 2613c4fe5c89d2971d16622a0cf1888acc40b8c26a137b9c4bd120cc95053a96` (an independent hand split produced the same digest).

## 2. Fix verification FIRST (the two named wave-1 fixes)

Method: split the section at C* `a41195dfc13a73958e4c5228ec196b28d03ded03` and at C** with the same splitter, then diff.

Commands:

```
git show a41195dfc13a73958e4c5228ec196b28d03ded03:SKILL.md > skill_c1.md   # C*
git show 5b703c6ff3ff26634e52b3d8ac98a14d4eb6137e:SKILL.md > skill_c2.md   # C**
diff -u section_c1.md section.md
```

Output (only two hunks; both are the named fixes):

```
-Source: S004/S026 and `corpus/knowledge/repeated-control-precondition.md`;
+Source: S004 and S265 (S026 superseded by S265, `corpus/SOURCES.md:500`) and `corpus/knowledge/repeated-control-precondition.md`;
...
-run `python3 tools/repeat-control.py --runs 3 --out /tmp/tameshi-r12-controls-UNIQUE -- COMMAND ARG...`;
+run `python3 tools/repeat-control.py --runs 3 --out $HYAKU_SCRATCH/tameshi-r12-controls-UNIQUE -- COMMAND ARG...`;
```

Section sha at C*: `532bebc8fad6dadff4ef3581677a15230b994cbbac56dbdaa571e59204cf0d74`; at C**: `2613c4fe…`.

### 2a. S026 → S265 supersession — PRESENT and SUPPORTED at C**

The cited anchor resolves, byte-exact, at C**:

```
$ git show C**:corpus/SOURCES.md | sed -n '500p'
- Round 48: four rows added, S265-S268 (superseding held S026, S048, S093, S108; snapshots and receipts under `.ufo/evidence/round-48/freshness/sources/`). The two "Next unused id: S265" lines above were not updated in round 48; this line corrects them without rewriting.
```

(That is the complete line, 272 bytes.) The registry rows the section names both exist at C**: `corpus/SOURCES.md:15` begins `| S004 | cargo-mutants book: Using the results` and `corpus/SOURCES.md:140` begins `| S265 | Flaky Tests at Google and How We Mitigate Them (John Micco, Google Testing Blog, 2016)` and carries `supersedes S026's anchor and quote only` (both quoted from their rows). The cited knowledge note exists and opens with `S265 (supersedes S026)` (`corpus/knowledge/repeated-control-precondition.md:1`). `corpus/knowledge/repeated-control-precondition.md` resolves at C**.

### 2b. `$HYAKU_SCRATCH` out path — PRESENT at C**; no `/tmp` left in the section

```
$ git show C**:SKILL.md | grep -n 'HYAKU_SCRATCH' | sed -n '4p'
1509:run `python3 tools/repeat-control.py --runs 3 --out $HYAKU_SCRATCH/tameshi-r12-controls-UNIQUE -- COMMAND ARG...`;
```

No `/tmp` token remains in the 19 section lines (`sed -n '1496,1514p' | grep -c /tmp` → 0). Standing rule it must satisfy resolves: `SKILL.md:28` defines `$HYAKU_SCRATCH` (default `/fast/scratch/hyaku`) with `/tmp` for files under 50 MB only.

## 3. Holds verified line by line at C**

Tool under the recipe is present at C** (`tools/repeat-control.py`, 36,082 B, sha256 `3f82aa5a97c4a67dd58e47aed10e0e2f0206bf65e306bcec80f57126f6309d51`); its stated precedence, exits and limitations were read at C** and match the section:

| Section statement (C**) | Backing at C** |
|---|---|
| `Three or more zero-exit controls match on raw stdout and stderr` → `controls_match` | `tools/repeat-control.py:276` `--runs must be >= 3`; `:220-234` `classify()`: any unavailable → `command_unavailable`; any `(exit_text, stdout, stderr)` disagreement → `controls_mismatch`; else nonzero → `baseline_nonzero`; else `controls_match`; `:24-27` "Bytes are compared as bytes: no decoding… DIR must not exist" |
| `Only this finite sample matched, on this host in this environment; not a determinism proof` | `tools/repeat-control.py:93-94` "A clean `controls_match` states that N finite observations agreed on this host in this environment — it is not a determinism proof and it cures no flakiness." |
| `All runs executed and any differ in exit or either stream` → `controls_mismatch` | `:220-234` (unavailable is classified first, so the row's "all runs executed" qualifier is exact); docstring `:30-37` |
| `Equal nonzero controls, or command unavailable` → `baseline_nonzero` / `command_unavailable`, exit 2 | `:42` map `controls_match 0 · controls_mismatch 1 · baseline_nonzero 2 · command_unavailable 2 · …`; `:232-233` |
| `put evidence outside any tree it inspects` | `:28` "keep it outside that tree" (`:26-29` explains self-mismatch) |
| `--runs 3 --out DIR -- COMMAND ARG...` with `The output directory must not exist` | `:268-276` (`--` separator required, runs ≥ 3), `:331` `--out already exists (refused, never overwritten)` → exit 64 |
| `retain raw observations before interpreting the finding` | `:22-26` numbered `run-<k>.{stdout,stderr,exit}` saved first, `finding.txt` "written last" (`:353`) |
| `Caller owns timeout policy; hanging commands yield no verdict` | `:84-85` "there is no timeout and no process supervisor — a command that hangs yields no verdict" |
| `runtime evidence: .ufo/evidence/round-12/verification-final.json` | file exists at C** (21,047 B), `passed: true`, `tool_sha256: 296fe566…`, checks `repeat-control-selftest`, `frozen-match` (exit 0), `frozen-mismatch` (exit 1), `real-pristine-three-controls` (exit 0, runs 1–3 exit=0), runner/witness checks |
| `standalone precondition check, not a change to the six-leg runner of round 12` | dated reading holds: the runner was six-leg at round 12 (`SKILL.md:1407` "six-leg registry at round 11, seven since round 16"); `verification-final.json` includes `runner-six-leg-regression` (exit 0) as a check, i.e. unchanged |
| `choose a non-secret fixture command before retaining evidence` | advisory, no in-tree counter-claim |

## 4. Findings

None. No statement in lines 1496–1514 fails at C**; the two wave-1 defects are repaired, and the repairs do not introduce a new false statement. (With zero findings there are no finding quotes to carry.)

## 5. Examined and deliberately NOT filed (calibration notes)

1. **Bare `$HYAKU_SCRATCH` / dash-form name.** Measured in this seat shell: `HYAKU_SCRATCH=<UNSET>`, so the literal recipe expands to `/tameshi-r12-controls-UNIQUE`; the name also is not the `<lane>-r<round>/<sub>/` shape of `SKILL.md:28`. Not filed: the round's own C2 contract forbids only `/tmp` scratch paths ("SKILL.md names no /tmp scratch path for either tool"), the same bare-variable convention is used by other C** sections (`SKILL.md:1993` `"$HYAKU_SCRATCH/tameshi-f5.json"`), and `HYAKU_SCRATCH` is defined as the namespace variable in the Standing rules. Reportable as a seat-environment note, not as a section falsehood.
2. **`the six-leg runner of round 12`.** Dated attribution; six legs held from round 11 until round 16 (`SKILL.md:1407`), so it is true at round 12, not a stale count. Not filed.
3. **`verification-final.json` tool sha drift.** Receipt pins `296fe566…`; the tool at C** is `3f82aa5a…` (round-53 TMPDIR-helper edit). The section presents the file as round-12 runtime evidence, not as current-tool evidence, and the finding-ID/exit semantics it evidences were re-read in the current code and are unchanged. Not filed.

## 6. Out-of-section observation (not a finding for this section; routed for the L1)

`corpus/knowledge/repeated-control-precondition.md` (cited by this section as a source) still names a `/tmp` out path in its open-arm command — line 79: `python3 tools/repeat-control.py --runs 3 --out /tmp/rc-kimi -- node …` — and line 3 still reads `recheck: 730d — S026's registry cadence` although its header declares `S265 (supersedes S026)`. Both are outside the 19 section lines, so they are not findings against my section; the C2 claim's surface is `tools/` + `SKILL.md`, and this note is `corpus/`.

## 7. Scratch discipline

Work tree `/fast/scratch/hyaku/tameshi-r53/w2/T53W2Read03/` (git objects only; no fixture repos, no commits) deleted before yield. No `/tmp` files used. No installs. No git/jj mutations in the lane; the lane tree was read through `git show`/`git grep` only.
