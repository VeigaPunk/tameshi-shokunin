# Tameshi round 53 — cold-read re-key repair, tools scratch hygiene, honest re-key

L1 TameshiR53a2, hyaku run 10, attempt 2 (attempt 1 died at its first model
call on a provider quota limit — nothing to inherit). Base `6db1d220`
(round-52 closure salvage). Claims frozen at `e62d9971` (amendments 1–5;
`.ufo/evidence/round-53/contract.json`, `freeze.json`): C1 calibration — the
cold-read floor repair (R52.1); C2 operability — `tools/` scratch hygiene
(R52.5). Both repair what `corpus/lessons/round-52-verifier-spotcheck.md`
routed back; the round-52 closure rejected-harmed with the frozen cold-read
floor RED at the tip (45/64 credited).

## Gate

Rows opened this round (CORPUS.md SOURCES contract v1 rule 1):

- **S275** — Change-Aware Mutation Testing for Evolving Systems (Ojdanić et
  al., ESEC/FSE 2022), `https://doi.org/10.1145/3540250.3558911`, opened
  2026-10-27 by L1 TameshiR53a2; the ACM copy is access-controlled (HTTP
  403), so the opened artefact is the author's camera-ready
  `https://ojda22.github.io/milos-ojdanic/assets/pdfs/change-aware-mutation-testing_camera-ready.pdf`
  (HTTP 200, 131622 B, sha256 `4d755c4e…`, snapshot
  `.ufo/evidence/round-53/assimilation/S161-camera-ready.pdf`). Located
  quote (20 words, camera-ready p. 3 (physical; printed footer 1787), pdftotext lines 289–294): "by
  selecting only subsuming commit relevant mutants, we reduce the number of
  mutants requiring analysis by around 93% on average". Assimilated from
  `merge/tameshi` (staged as S161, re-pointed by document to S275).
- **S276** — Keeping Mutation Test Suites Consistent and Relevant with
  Long-Standing Mutants (Ojdanić, Papadakis, Harman), arXiv:2212.11762,
  opened 2026-10-27 by L1 TameshiR53a2 (HTTP 200, 41423 B, sha256
  `d6dc4cf6…`, snapshot
  `.ufo/evidence/round-53/assimilation/S162-arxiv.html`). Located quote (20
  words, abstract): "re-compute mutant suites per release. Sadly, this makes
  mutation results inconsistent; mutant scores from each release cannot be
  directly compared". Assimilated from `merge/tameshi` (staged as S162,
  re-pointed by document to S276).

Admits (assimilation set, §10 per-entry gates):

- **change-aware-resweep-cadence.md** — ADMITTED. PROVINCE: verification-fixture
  craft (mutation cadence) — in scope. QUALITY bar: every claim cites its
  source with located quotes — holds. Coverage ground: F7 (incremental
  re-sweep granularity) was open — this is new ground, recorded in
  `corpus/README.md`'s frontier table (round-53 addendum). Both cited rows
  re-opened by the L1 this round (access dates and quotes above); the staged
  entry's quotes re-located verbatim in the round's copies before the rows
  were written. Id collision: staged S161/S162 renumbered to S275/S276
  (registry continuation; staged ids S161–S255 stay reserved by document);
  scratch collision check `assimilation/collisions` listed 8 collisions for
  other staged ids, none for the adopted rows; the 0–3-space indented-row
  guard was proven on a scratch fixture before any append.

Rejects (assimilation set):

- **The other 85 staged `merge/tameshi` entries** — REJECTED this round:
  capacity, not merit. The round's centre of gravity is the R52.1 re-key
  repair; §10 takes ONE theme and 1–3 entries per round. Flip: a later round
  adopts the next-ranked candidates (`r8-predictive-test-selection-cost.md`
  and `delta-debugging-minimization-contract.md` are the next fit against
  open frontier rows).
- **A staged row appended as-is** — REJECTED by rule (§10 scratch
  transformation): the staged S161/S162 rows carry escaped pipes in the
  recheck cells; the appendable rows normalize them to the fleet schema
  (date + `365d` cadence), the stripped re-check commands recorded here:
  S275 — `curl -fsSL
  'https://ojda22.github.io/milos-ojdanic/assets/pdfs/change-aware-mutation-testing_camera-ready.pdf'
  | sha256sum` expect `4d755c4e…`; S276 —
  `curl -fsSL 'https://arxiv.org/abs/2212.11762' | grep -c '52% degrade'`
  expect 1.

considerthese mining: `considerthese/2026-10-26.md` proposal 1 (crash-resume
integrity check) mined this round — implemented as
`.ufo/evidence/round-53/verify-freeze.sh` and executed by the L1 at freeze
time (receipt below). Proposals 2–5 remain unmined (at most one per round).

## Mistakes

- **class: integration debris from an in-line fix pass.**
  evidence: round 52's L1-applied replacements landed half-applied in at
  least three places — SKILL.md "replays **six** in r10-2 (**ten** since
  round 51) (ten since round 51)" (duplicate parenthetical, fixed this
  round), the contradictory "Cases 5–6 were still not embedded at this
  boundary (both are legs 5–6 since round 10-2 …)" (fixed this round), and
  the round-52 parenthetical claiming "rc 0, at tool sha `977de470…` — see
  `T52W2Fix06.selftest.out`" where the receipt names no command, exit, or
  sha (re-anchored this round to the seat's report + receipt pair). The
  T52W3 readers caught all three as findings 12–14 (`.ufo/waves/round-52/w3/`).
  captured-by: none — no mechanical check guards a fix pass against
  duplicate-parenthetical or self-contradicting edits; the cold-read readers
  caught them one round late. fix: this round's L1 fix pass re-verified each
  replacement hunk in place; wave 2 carries a duplicate-phrase lint over the
  touched sections; a QUALITY criterion is drafted below.
- **class: claim-scope surprise from an honest edit.** evidence: the C2
  tool fixes (7 files) input-drifted 10 sections the round did not intend to
  touch; the frozen re-key scope grew 19 → 30 headings (amendment 5,
  disclosed before wave 1). captured-by: none — the precheck LOST diff after
  the fix pass caught it (45 → 34 credited) before any seat ran. fix:
  amendment 5 froze the 30-heading set; the no-harm floor requires 64/64 at
  the deciding run, so an unrepaired drift cannot land silently.
- **class: freeze-file syntax defect (self-caught, pre-seat).** evidence:
  the first frozen c1 counter carried a NUL byte (syntax error) and its
  do-nothing control crashed instead of printing a verdict; both caught by
  the phase-A control run before wave 1 (amendments 1–2). captured-by: the
  frozen do-nothing control — exactly what it exists for. fix: re-freeze;
  the do-nothing control must print a verdict line (never a traceback) —
  now part of the c1 contract.

## QUALITY criterion (drafted; lands with the round commit)

- **104. A fix-pass hunk is re-read before commit; no section may gain a
  duplicate parenthetical, a self-contradicting sentence, or a citation
  whose receipt does not establish the cited clause. Falsifier: a
  duplicate-phrase scan over the touched sections lists zero hits, and every
  new citation resolves to a receipt establishing command, exit and pinned
  bytes.**

## The re-key method (for the round report)

The T52W3 reader findings (16 findings across 10 sections, plus the missing
Read18) were fixed L1-inline at `218bc6b5`; the fix pass also closed the
scratch-directive staleness (Standing rules, recipe, registry rows) that the
T52 readers did not reach. The round's own edits drifted 11 further
sections; the frozen re-key set is the 30 headings credit-lost at the
post-fix candidate. Wave 1 re-reads all 30 sections at the content commit;
the L1 then binds fresh ledger entries (trace-bound, read_rev = content
commit, inputs re-pinned at candidate shas) for every heading a fresh reader
cleared; the frozen precheck must print 64/64 GREEN at the deciding run.
S276 is the practice authority for the repair: a pinned long-standing suite
is the consistency device; re-computing per change is the bug.
