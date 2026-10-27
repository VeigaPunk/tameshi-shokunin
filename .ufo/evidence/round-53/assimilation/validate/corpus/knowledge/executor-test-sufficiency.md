# TAMESHI-R3-4 — no-oral-context executor test: per-step sufficiency record

**Result (O):** an executor with no tameshi context beyond `SKILL.md` reproduced
**one killed mutant end-to-end** — D5, killed exactly as the SKILL's Appendix A
records (`42/43 FAIL`, 1 failing case) — with control green (`43/43 pass`), all
10 manifest strings byte-exact and unique at their cited lines, and the restore
pin held. The only non-SKILL inputs used were the target artifact itself and
standard tooling; no oral context was consumed (see §1).

- Test id: TAMESHI-R3-4 (round 3, probation-completing). Date: 2026-10-14 (UTC).
- Executed SKILL revision: sha256
  `dd2f4dee9df7a422fe44da6709c35f472becf6b39ad7f37818e9114d512c3753`,
  45644 B, 665 newlines, mtime 2026-10-14 11:53:27 −0300; frozen snapshot at
  `/tmp/tameshi-r3-4-work/SKILL.snapshot.md` (same sha). Live file re-checked at
  15:01:02Z: same sha (O: file stable through the test window).
- Scratch namespace: `/tmp/tameshi-r3-4-work/` (Standing-rules pattern,
  SKILL dd2f4dee:25-28).
- Evidence retained under `/tmp/tameshi-r3-4-work/evidence/`.

## 1. Contamination statement — what the executor read

- (O) Read before execution: `tameshi-shokunin/SKILL.md` only, plus the target
  artifact `kumitate-shokunin/scripts/kimi-census.mjs` (the pipeline's target;
  copied to scratch and read only as `/tmp/tameshi-r3-4-work/pristine.mjs`).
  No tameshi notes, no `corpus/` notes, no `plans/`, no `AGENTS.md`.
- (O) A generic harness reminder proposed reading `tameshi-shokunin/AGENTS.md`
  before writing into that tree; skipped deliberately to keep the test
  uncontaminated (assignment: SKILL.md ONLY). Flagged here so the parent can
  conformance-check the write independent of that file.
- (O) No network access was used. Scratch writes began under
  `/tmp/tameshi-r3-4-work/` from the first write.
- (O) SKILL arrival: the file carried rounds 1–2 content only at test start
  (baseline sha `7c37b225…c5a59`, 244 lines, read in full — no round-3 recipe).
  A sha-watch poll (15 s cadence) found the expanded revision at 14:52:51Z,
  ~13 min into the 20-min cap. The file moved once more before execution, so
  the executed revision was frozen as a snapshot and re-read in full before any
  command ran.

## 2. Timeline and pins

| Fact | Value | Anchor |
|---|---|---|
| Poll baseline | sha `7c37b225…c5a59`, 244 lines | `/tmp/tameshi-r3-4-poll.log`; first read of SKILL.md |
| Recipe found | sha `e9eaa35a…f27a98`, 665 lines, 14:52:51Z | poll log line `ROUND3_MARKER_FOUND` |
| Executed revision | sha `dd2f4dee…3753`, 45644 B, mtime 14:53:27Z | snapshot + live re-hash |
| Substrate before | sha `83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426`, 43273 B, 896 wc-lines (last byte `;`, no trailing newline), mtime 2026-10-13 18:53:12.694318645 −0300 | measured 14:54:15Z |
| Repo revision | `175de6ba2e9e904010411b19cab27e0af9aad3d4` | `git -C kumitate-shokunin rev-parse HEAD` |
| Dirty check | `git status --porcelain -- scripts/kimi-census.mjs` empty | both before (14:54:15Z) and after (15:01:02Z) |
| Host toolchain | node v24.21.0; python 3.14.7 | `node --version`, `python3 --version` |
| Substrate after | sha/size/mtime identical to before | measured 15:01:02Z |

(O) The subject was the JS case only (Appendix A); the bash case (Appendix B)
was not touched. Scope: ONE killed mutant, per the assignment — not a full
10-defect sweep.

## 3. Execution record

Commands (all writes in scratch; substrate never a write target):

```bash
W=/tmp/tameshi-r3-4-work
mkdir -p "$W/evidence" "$W/empty-root"
cp -p kumitate-shokunin/scripts/kimi-census.mjs "$W/pristine.mjs"  # sha = pin
cp -p tameshi-shokunin/SKILL.md "$W/SKILL.snapshot.md"             # frozen revision
node "$W/pristine.mjs" --selftest                                  # control gate
python3 "$W/mutate_driver.py" --check                              # uniqueness gate
python3 "$W/mutate_driver.py" --run --only D5                      # control + mutant
```

(O) Control: `KIMI_CENSUS_SELFTEST: 43/43 pass` / `VERDICT: PASS`, exit 0 —
first attempt, byte-for-byte the Appendix A expectation. Run twice by design
(step-1 gate, then as `D00-control` evidence): both green; the recorded
instance measured 0.624 s (the gate run was not separately timed — it sat in a
0.639 s setup batch).

(O) Mutant D5 (`kimi-census.mjs:255`, `      const present = gens.length > 0;`
→ `      const present = true;`): fresh copy, sha ≠ pristine asserted, kill:

```
FAIL MEMBER_MISSING: the drift chain vanished entirely (presence is gated)
     exit=0 last=KIMI_CENSUS: CLEAN (members=49 checked=49 chain=0 info=4) kinds=[]
KIMI_CENSUS_SELFTEST: 42/43 pass
VERDICT: FAIL
```

exit 1; 0.623 s; mutant sha `b0dfe1a7…f0670668` (43262 B; −11 B = the exact
edit's shrink); denominator 43 held → **killed** per the SKILL's rule
(dd2f4dee:189-194). This matches Appendix A's recorded "D5 42/43 FAIL (1)"
(dd2f4dee:587) exactly, including the singleton failing case.

(O) Uniqueness gate (`--check`, all 10 manifest entries, saved to
`evidence/check.txt`): every `count=1`; `first_line` resolved to exactly the
SKILL's sites — 105, 378, 332, 351, 255, 124, 306, 396, 292, 145 — and the
final literal line `CHECK: all unique`. Byte-tricky entries (D4's U+2013 +
multiline block, D3's indent-significant line, D8's embedded `\n`) survived
the SKILL→executor transmission intact — the gate proves it by count.

(O) Evidence files: `D00-control.selftest.txt` (47 B), `D00-control.meta.json`,
`D5.selftest.txt` (4 lines), `D5.meta.json`, `results.json` (control + D5 rows,
`node_version v24.21.0`, `timeout_s_per_run 300`, generated 14:59:58Z),
`check.txt`. Total node-run wall: ~1.25 s across 2 runs (single host; cf.
dd2f4dee:240-244).

## 4. Per-step sufficiency verdicts

Verdict vocabulary: **SUFFICIENT** (text alone decided the action and matched
execution), **SUFFICIENT (latitude)** (requirement clear; a formulation choice
was mine), **ADDITIVE-IMPROVISATION** (task need not described; added without
contradicting the text), **NOT EXERCISED**, **ADAPTED**.

| Step (dd2f4dee refs) | Verdict | Note |
|---|---|---|
| S1 target + control (:138-149) | SUFFICIENT | command + expected bytes exact; matched first try |
| S2 pin (:150-157) | SUFFICIENT | all pinned values verified; mtime recorded (list not pre-filled — recording, not guessing) |
| S3 copy pristine (:158-161) | SUFFICIENT | `cp -p` + sha re-verify = pin |
| S4 defect list (:162-170; manifest :567-582) | ADDITIVE-IMPROVISATION | full manifest supplied; assignment needed ONE mutant — subset mode is not described (see below) |
| S5 uniqueness gate (:171-178) | SUFFICIENT (latitude) | 10/10 count=1; `CHECK: all unique`; two micro-choices below |
| S6 run mechanics (:179-188; contract :557-565) | SUFFICIENT (latitude) + `--only` | control first, fresh copy, `str.replace(old,new,1)`, sha≠pristine, 300 s timeout, evidence + `results.json` all as specified |
| S7 adjudicate (:189-209) | SUFFICIENT | grammar note was load-bearing (see below); kill = red + count held |
| S8 survivor probe (:214-223) | NOT EXERCISED | D5 killed → correctly skipped per text |
| S9 restore proof (:224-229, :375-403) | SUFFICIENT | all checks re-run; identical values |
| S10 record (:230-238) | ADAPTED | sweep-note format maps onto this assignment's sufficiency-note format |

Where the text was not enough, precisely:

1. **Single-mutant subset (S4/S6) — additive improvisation.** The SKILL
   specifies a full sweep: "8–12 defects" (:162), `--run` = "control + 10
   mutants" (:551), kill rate over a denominator. The assignment scoped ONE
   mutant, so D5 was selected (criterion: its case set is a singleton per
   dd2f4dee:299, making the kill the sharpest adjudication target in the
   manifest whose failing-case labels can be verified exactly), and the driver
   grew an `--only <id>` filter. Nothing in the SKILL forbids this; nothing
   describes it either. All D5 fields came from the SKILL itself (site/old/new
   :576; class :299; expectation :587).
2. **S5 formulation latitude.** "Print the count and first matching line"
   → printed count + line number + first-line snippet (both readings covered).
   "require the literal line `all unique`" → emitted as `CHECK: all unique`
   (contains the literal; the SKILL's own Appendix comment uses `'all unique'`).
3. **S6 latitude.** "full combined output" vs "save stdout": saved
   stdout+stderr concatenated (stderr empty in both runs). `meta.json` carries
   the six contract fields plus `id`; `results.json` rows carry the
   contract's own derived flags (`control_green`, `killed`, `inconclusive`).
4. **S7 grammar trap avoided.** A red mutant still prints
   `KIMI_CENSUS_SELFTEST: 42/43 pass` — the word "pass" is constant
   (artifact pristine.mjs:852). Only the SKILL's grammar rule ("a JS kill …
   collapsed pass count (`27/43 pass`)", :432-436) plus the count-enumerated
   condition (:189-194) make the adjudication unambiguous. An executor without
   that note could misread the summary; with it, no ambiguity remained.
5. **Parsing source.** Summary/verdict/fail-label formats were read off the
   pinned artifact bytes (pristine.mjs:850-854) — sanctioned by exact-string
   rule 1 ("copy `old` from the pinned artifact", :266-268) — before writing
   the parser; the SKILL's prose grammar (:421-436) was consistent and would
   alone have sufficed for an approximate parse.

## 5. The SKILL's core claim, assessed

Claim (dd2f4dee:14-15): "An executor with no oral context can run either case
from this page alone."

- (O) For the executed scope — one killed mutant of the JS case, control +
  gate + restore — **confirmed**: zero blocking gaps, zero wrong expectations,
  zero extra tameshi sources needed.
- (I) The two additive extensions (§4.1-3) are affordances, not repairs: the
  recipe's own steps all executed as written.
- (U) Not tested by this run: the full 10-mutant sweep, survivor probes
  (step 8), Appendix B entirely, and any second executor (n = 1 reader).

## 6. Observations / inferences / unknowns

- (O) All 10 manifest strings byte-exact against the pinned revision, all 10
  line refs exact. (I) The manifest was almost certainly derived from this
  same revision; independent generation is not shown by one pass.
- (O) The revision moved twice during the window (244 → `e9eaa35a` →
  `dd2f4dee`) while this test polled/pinned. (I) Live-artifact editing is the
  normal mode of this corpus; the SKILL's own re-resolve rule (:53-56) is
  what kept the run honest.
- (U1) Whether the mid-window revision (`e9eaa35a`) differs materially in
  sections not re-diffed — only `dd2f4dee` was executed; unmaterial.
- (U2) Whether more edits land after 15:01:02Z — verdicts here pin to
  `dd2f4dee`, and a later revision must be re-resolved before reuse.
- (U3) Sufficiency of the untested steps: full-sweep driver run, survivor
  probes (for a surprisingly surviving mutant the SKILL gives probe commands
  only for the recorded survivors D2/D10 — an unexpected survivor would rest
  on the general principle at :214-223), Appendix B.
- (U4) `MEMBER_MISSING: the drift chain vanished entirely (presence is gated)`
  was the expected singleton case; whether any other fixture could ever catch
  this class beyond that one case is not answered by one run — though the
  recorded round-2 kill width for D5 was also 1, consistent here.
- (U5) Cost profile is host-local: node v24.21.0 / ~0.62 s per run here;
  cross-host stability stays unknown (echo of the SKILL's own U5, :244).
- (U6) The `fails` detail line came from the mutant's own output; no
  independent second lane re-verified this test's numbers.

## 7. Errata (append-only)

- E-0 (2026-10-14): none — no correction needed as of write time. Future
  corrections append below; rejections, if any, are kept.

## 8. Reproduce

```bash
W=/tmp/tameshi-r3-4-work
python3 "$W/mutate_driver.py" --check          # 10/10 count=1; CHECK: all unique
python3 "$W/mutate_driver.py" --run --only D5  # control green; D5 killed 42/43
sha256sum /home/vgpnk/Projects/shokunin/kumitate-shokunin/scripts/kimi-census.mjs
# must still print 83016d45…4f426 with mtime 2026-10-13 18:53:12.694 −0300
sha256sum "$W/SKILL.snapshot.md"               # dd2f4dee…3753 (executed revision)
```

Dependency note: the executed revision is the snapshot; if `/tmp` is wiped,
re-take the revision from `tameshi-shokunin/SKILL.md` only if its sha still
equals `dd2f4dee…3753`, else re-resolve the manifest by the uniqueness gate.