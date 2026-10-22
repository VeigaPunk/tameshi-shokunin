# ReviewPredictions — round 26 C1, cite-check pre-registration vs sweep evidence

Godspeed axes for this review: (1) **verdict fidelity** — predicted KILLED/SURVIVED vs observed;
(2) **witness fidelity** — the named selftest case vs the actual FAIL lines; (3) **mechanism
grounding** — every divergence explained from the pinned bytes.

## Inputs (all opened this session, 2026-10-22)

- Predictions: `.ufo/evidence/round-26/cite-check/predictions.json` (10 entries, 5 kill-aimed,
  5 hole-aimed).
- Spec: `.ufo/evidence/round-26/cite-check/sweep/spec.copy` (pre-registered @old/@new per defect).
- Results: `.ufo/evidence/round-26/cite-check/sweep/results.tsv` and `sweep.txt`; per-mutant
  selftest output under `sweep/evidence/<id>.out` plus `control.out`.
- Pinned code: `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show
  1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs`, extracted to
  `/tmp/r26-review/cite-check.mjs`; `sha256sum` observed
  `40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f`, 2537 lines — matches the
  pin recorded in predictions.json. Cited below as `pin:L<line>`.
- Tooling directive record: nothing installed or upgraded; existing `git` and coreutils sufficed.

## Method

For each of the 10 defect ids: read the predicted verdict and named selftest case from
predictions.json, read the observed verdict from results.tsv, and extract the FAIL lines from the
matching `sweep/evidence/<id>.out`. A witness match means the named case is (for KILL
predictions) among the FAIL lines, or (for SURVIVE predictions) correctly absent from them.
Every divergence was then explained from the pinned bytes.

## Tally

- **Verdict mismatches: 0 / 10.** All five K-prediction mutants exited 1 (KILLED); all five
  S-prediction mutants exited 0 with 62/62 (SURVIVED). Every entry in
  `predictions.json.predictions` agrees with `results.tsv`.
- **Witness mismatches: 1 / 10** — `K_FENCE_TILDE` (detailed below). One additional qualitative
  note on `K_PIN_KIND`: the named witness case did fail as predicted, but the prediction's stated
  mechanism is half wrong (also below).

| id | predicted | observed | verdict ok | named witness in FAIL lines |
|---|---|---|---|---|
| K_UNRESOLVED_SEV | KILLED | KILLED (exit 1, 55/62) | yes | yes (+6 more FAILs, same assertion) |
| K_PIN_KIND | KILLED | KILLED (exit 1, 61/62) | yes | yes (the sole FAIL) |
| K_FENCE_TILDE | KILLED | KILLED (exit 1, 60/62) | yes | **no** — named case PASSed |
| K_MISSING_WORD | KILLED | KILLED (exit 1, 61/62) | yes | yes (the sole FAIL) |
| K_EMPTY_VERDICT | KILLED | KILLED (exit 1, 61/62) | yes | yes (the sole FAIL) |
| S_OOR_EDGE | SURVIVED | SURVIVED (exit 0, 62/62) | yes | yes (no FAIL lines) |
| S_STRICT | SURVIVED | SURVIVED (exit 0, 62/62) | yes | yes (no FAIL lines) |
| S_EMPTY_GUARD | SURVIVED | SURVIVED (exit 0, 62/62) | yes | yes (no FAIL lines) |
| S_USAGE | SURVIVED | SURVIVED (exit 0, 62/62) | yes | yes (no FAIL lines) |
| S_PIN_INCLUDES | SURVIVED | SURVIVED (exit 0, 62/62) | yes | yes (no FAIL lines) |

## Witness mismatch: K_FENCE_TILDE

Prediction: KILLED via `R16 repro: ~~~ fence gives the same result as ``` (marker-symmetric)`,
reasoned "a three-tilde line stops opening a fence, so the tilde fixture tokenizes differently
from the backtick fixture." Observed: the mutant was killed, but that case **passed**
(`backtick=UNRESOLVED/error@line7 tilde=UNRESOLVED/error@line7` in `sweep/evidence/K_FENCE_TILDE.out`),
and the kill came from two un-named cases:

- `FAIL  fence content is never tokenized (by design, kept) — insideFence=1 afterFence=OK`
- `FAIL  R16 regression: fence content is never tokenized under line-local pairing — fenceSpans=1 afterFence=OK`

Explanation from the pinned code:

- The mutation rewrites the only fence-grammar gate,
  `const FENCE_LINE_RE = /^\s*(`{3,}|~{3,})/;` (pin:471), to `~{4,}`. `findFences` (pin:477-492)
  classifies a line as a marker solely through this regex, and `maskFences` (pin:494+) blanks
  only the bytes **inside** detected fence ranges.
- The named case's tilde fixture (`fence-tilde.md`, built at pin:1739-1741) is: header, blank,
  `~~~`, `fenced body text`, `~~~`, blank, then the only citation
  `` `scripts/no-such-file.mjs` `` at line 7 — **after** the fence. Under the mutant the `~~~`
  lines stop being markers, so the fence (and its masking) disappears, but the line-7 token sits
  outside the fence in both worlds: it is tokenized and reported `UNRESOLVED/error@line7`
  either way. The case at pin:1999-2006 compares only the single hit's kind/severity/line
  descriptors, which are identical — so the predicted mechanism ("tokenizes differently") is
  true only for bytes inside the fence, which this fixture never observes.
- The actual killers place the citation **inside** a `~~~` fence: `fence-content.md` is built as
  `fenceDoc('# fence fixture: fence content is never tokenized', '', T3, CITATION, T3, ...)`
  (pin:1755-1757). With `~{4,}`, the fence vanishes, the interior `CITATION`
  (`scripts/no-such-file.mjs`, pin:1718) becomes a live token, so
  `inside === 0` fails (case at pin:2020-2023, observed `insideFence=1`) and the line-local
  pairing probe finds one backtick span containing `no-such-file` (case at pin:2109-2112,
  observed `fenceSpans=1`).
- Corroborating the single-gate mechanism: in the same mutant run the cross-closing probe detail
  shifted from `tildeOpened[fences=[[59,146]]]` (control) to `[[80,146]]` — with the tilde arm
  requiring four tildes, the `~~~` opener at byte 59 is skipped and the ` ``` ` line at byte 80
  (backtick arm unchanged) opens an unclosed fence that masks to EOF. That case still passed
  because its citation stayed swallowed.

Verdict unaffected (the mutant died); the pre-registration simply named a witness that cannot
fire for this mutation, and the recorded 62-case suite kills it through different cases.

## Witness note: K_PIN_KIND — named case held, predicted mechanism half wrong

The named case `content pin match → OK; mismatch → PIN_MISMATCH` is the sole FAIL line
(`match=yes mismatch=no`), so the witness matches. But the prediction's reason — "rev-classified
pins go to git resolution and come back REV_UNKNOWN, not OK or PIN_MISMATCH" — is falsified for
the match arm. From the pinned code:

- The fixture SKILL.md writes two digest-derived pins: `rev \`digest.slice(0,12)\`` and
  `sha256 \`digest.slice(0,10)\`` plus a mismatch pin `rev-pinned sha256 \`0123456789ab\``
  (pin:1685-1687, with `digest = sha256File(srcRoot/scripts/real.mjs)` at pin:1680).
- Under the mutant (spec line 15), all three are classified `kind = 'rev'` (classification at
  pin:1126-1129), which routes them past the sha256 branch (pin:1186-1216, containing the
  `digest.startsWith(pin.hex)` → OK / PIN_MISMATCH arms) into rev resolution (pin:1217-1243).
- Match pin: git resolution fails, then the rev-path content-hash fallback
  `if (!resolvedBy && pin.kind === 'rev' && owner) ... digest.startsWith(pin.hex)` (pin:1218-1219)
  succeeds because the pin hex **is** a prefix of the digest — it resolves-by-content and emits
  OK. The case's finder accepts `/matches sha256/` or `/resolved-by-content/` (pin:1895-1897),
  hence `match=yes`. The prediction claimed this arm could not return OK; the fallback makes it
  return OK anyway.
- Mismatch pin `0123456789ab`: not a commit, and `digest.startsWith('0123456789ab')` is false,
  so it falls to `REV_UNKNOWN` (pin:1236-1241) instead of `PIN_MISMATCH` — hence
  `mismatch=no`, which alone fails the case (`ok` requires both arms, pin:1898).

So the kill is genuine and via the named case, but through a narrower path than registered: only
the mismatch arm diverges; the match arm is rescued by the co-existing content fallback.

## Confirmed witnesses (no action needed)

- **K_UNRESOLVED_SEV**: named witness `bogus-path → UNRESOLVED error` FAILed as predicted
  (`UNRESOLVED/warn @SKILL.md:3`), with six further FAILs, all the same assertion shape:
  `rec()` stamps `severity: SEVERITY[kind]` (pin:815-817) and the mutant flips
  `UNRESOLVED: 'error'` to `'warn'` in the table (pin:222). The extra FAILs are exactly the
  cases asserting error severity through `fpError` (`kind === 'UNRESOLVED' && severity ===
  'error'`, pin:2136-2138) and the backtick R16 repro (`hit[0].severity === 'error'`,
  pin:1993). Superset of the named witness; consistent with the registered reason.
- **K_MISSING_WORD**: exact witness. The case asserts
  `String(r.stderr ?? '').includes(\`--src ${want} is missing\`)` (pin:2342); the mutant word is
  `absent`, and the observed FAIL line shows `... is absent`.
- **K_EMPTY_VERDICT**: exact witness. Mutant reduces the guard to `const verdict = !drift ? ...`
  (spec line 30 of pin:1590); with `filesScanned=0` and no drift the verdict becomes PASS, and
  the named case asserts FAIL — observed `filesScanned=0 verdict=PASS`.
- **S_OOR_EDGE / S_STRICT / S_EMPTY_GUARD / S_USAGE / S_PIN_INCLUDES**: zero FAIL lines in each
  run (62/62), matching each prediction's "no case exercises this" or "case still passes" stance.
  Spot grounds: the only LINE_OOR fixture cites `:999` of a 20-line file, still out of range
  under `ref.start > n + 1` (pin:1312); no hermetic case sets `--strict` (parsed at pin:264,
  consumed only at pin:1589); the empty-scan case keeps failing because `resolved=0` when
  nothing is scanned, so the remaining guard at pin:1590 is co-extensive on that input; unknown
  arguments throw at pin:270 into `return 64` (pin:2512) and no case passes one; and
  `0123456789ab` is not a substring of the real digest, so `includes` at pin:1195 still yields
  PIN_MISMATCH.

## Residual risk and verification gaps

- The one witness mismatch shows pre-registration witness naming is not load-bearing for this
  suite: `K_FENCE_TILDE`'s registered witness was unfireable, and the recorded kill rests on the
  two fence-content cases. Any future claim of "the suite kills X via case Y" should be checked
  the way this review did, not assumed from the spec comment.
- `S_EMPTY_GUARD`'s "co-extensive guard" holds only on the exercised input. A case with
  `filesScanned > 0` but `resolved === 0` would separate the two guards; the hermetic suite has
  none. Gap, not a verdict defect.
- Cosmetic, no axis impact: the "real rev" pin hex differs across runs (`41328f10…` in
  control/K runs, `32ab3174…` in S runs) because the fixture writes the sandbox repo's HEAD at
  build time (`git rev-parse HEAD`, pin:1679). Both worlds PASS that case.
- I re-judged from committed evidence and the hash-verified pinned blob only; I did not rerun
  the sweep (lane bounds: no gates or selftests outside /tmp, and no rerun was needed — the
  recorded outputs are internally consistent with `results.tsv`).
