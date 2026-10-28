# T55W2Connector3 — sibling scan: does any of kumitate / kagi / tsukuroi / mado already emit a `could-not-evaluate` class line?

Seat: connector (leaf). Judged axis: **operability**. Milestone: is the grammar a fleet pattern.
Lane read at **C0 `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`** (clone). Siblings read read-only, each
citation re-resolved with `git -C <lane> show HEAD:<path> | sed -n '<line>p'` at these revisions:

| lane | HEAD pinned for this scan |
|---|---|
| kumitate | `14057f3e3899180c95713bace088fb9c0d0046e3` |
| kagi | `69b61db46be4ed955994f6f1d1cba522bc5f4e97` |
| tsukuroi | `d7cfc27308e8af51b76b5cfe0c656acc1788cefb` |
| mado | `3b55b6e91e40f455dd56b2985e4ffc087ada92d5` |
| kama (bar check) | `7ee8cbdf16…` |
| souji (bar check) | `ed30b7f5b7…` (moved during this scan; all souji citations are `show HEAD:` reads, never worktree) |

Every claim below has a command and its captured bytes in
`.ufo/waves/round-55/w2/T55W2Connector3-receipts/` (`00-commands.txt` holds the command list).

---

## 1. Verdict for the round

**Not one of the four named lanes emits the hyphenated label `could-not-evaluate` on any line.**

- kumitate's line token is **`fail-closed`** (stderr) / **`FAIL-CLOSED`** (stdout).
- kagi's is **`SETUP`** / **`POLICY`** (stdout; one bootstrap site stderr).
- mado's is **`could_not_evaluate`** — underscore, stdout, closed enum.
- tsukuroi carries the class only **inside a JSON field** (`"status": "CANNOT_EVALUATE"`), on stdout.

Answer to the (a)/(b)/(c) question, split by layer because the layers do not share a verdict:

| layer | verdict | why |
|---|---|---|
| exit code 2 ⇒ `could-not-evaluate` | **general — but by protocol, not by the two-lane rule** | `PROTOCOL.md:380-383` pins the mapping fleet-wide; all four lanes hold it (kumitate `SKILL.md:595`, kagi `SKILL.md:700-701`, tsukuroi `tools/_revision.py:12`, mado `tools/mado-assessment.py:166`) |
| a *line* carrying a class token, exit 2 | **family-general (3/4)** | kumitate stderr+stdout, kagi stdout, mado stdout; tsukuroi JSON only |
| a line carrying it on **stderr** | **1/4 of the named lanes** (kumitate) | kagi and mado are stdout, tsukuroi has no line |
| the literal label `could-not-evaluate` on a line | **0/4** of the named lanes — held by **kama** and **souji**, which are *not* in the four | `kama-shokunin/tools/seat-report-immutability.py:410` (`NAME: could-not-evaluate: …`, **stdout**) and `kama-shokunin/tools/append-only-audit.py:1522` (`could-not-evaluate: …`, **stderr**, no prefix); `souji-shokunin/census/round-19/verify-agreement-pin.py:197-198` and `census/round-22/mutation-adequacy.py:264-265` (`tool: could-not-evaluate: …`, **stderr**, exit 2 — census instruments, not live `tools/`) |
| the **conjunction** tameshi froze: `<name>: could-not-evaluate: <cause>: '<value>' (could-not-evaluate)`, stderr, single line | **(a) lane invention — zero holders** | `(could-not-evaluate)` suffix: 0 lanes (wave-1's layer (d), re-checked here: unsuffixed in all four); prefix+label+stderr: souji only; prefix+label+stdout: kama only |

So: **(a) as written**. Only component-wise is it (b), and the components are held by two lanes
*outside* the four the item names (kama, souji). It is **not (c)**: `PROTOCOL.md:380-383` says
verbatim that "Nothing else is pinned: a gate's own vocabulary — WARN vs HIT, a missing baseline,
finding kinds — stays lane-owned, and this section governs the outer interface only." The line is
therefore not general *by rule*, and the two-lane bar admits the parts, not the whole.

The round must not write "the fleet's grammar" anywhere. It may write: exit 2 is protocol-pinned;
the one-line shape is this lane's declaration, with kumitate as the nearest family precedent and
kama+souji as the only label holders.

---

## 2. Live evidence — what each guard actually prints (stdout and stderr split, rc echoed)

| # | command (in the pinned clone) | rc | stdout | stderr |
|---|---|---|---|---|
| 1 | `node scripts/surface-probe.mjs --src /nonexistent/T55W2probe` (kumitate) | 2 | `SURFACE_PROBE: FAIL-CLOSED (--src /nonexistent/T55W2probe is missing)` | `surface-probe: fail-closed — --src /nonexistent/T55W2probe is missing` |
| 2 | `node scripts/cite-check.mjs --src /nonexistent/T55W2cite` (kumitate) | 2 | *(empty)* | `cite-check: fail-closed — --src /nonexistent/T55W2cite is missing` |
| 3 | `bash corpus/scope-gate.sh --data /nonexistent/adj.tsv` (kagi) | 2 | `ADJACENCY_SCOPE: SETUP (data file not found: /nonexistent/adj.tsv)` | *(empty)* |
| 4 | `PATH=/nonexistent bash corpus/scope-gate.sh` (kagi) | 2 | *(empty)* | `corpus/scope-gate.sh: line 82: dirname: command not found` + `scope-gate: SETUP (cannot resolve the script directory — is dirname on PATH?)` |
| 5 | `python3 tools/check-freshness-r17.py --revision zzzznotarev` (tsukuroi) | 2 | `{"findings":[{"detail":"7-64 hex commit required","id":"E-REVISION-INVALID",…}],"status":"CANNOT_EVALUATE",…}` | *(empty)* |
| 6 | `python3 tools/mado-assessment.py --check /nonexistent/a.json --root /nonexistent-root` (mado) | 2 | `{"code": 2, …, "finding_ids": ["assessment_input_invalid"], "result": "could-not-evaluate"}` | *(empty)* |
| 7 | `python3 tools/mado-tripwire.py /nonexistent/x.jsonl` (mado) | 2 | `MADO_TRIPWIRE: could_not_evaluate` + a second JSON line | `usage: mado-tripwire.py --scan PATH …` |

Rows 1–2 are the same lane on the same class with **two different stream profiles**; rows 3–4 are
the same gate on the same class with **both profiles**. "One uniform error grammar" is false even
*within* kumitate and *within* kagi, not only across lanes.

Replicator note: `c2/measure.py:186-189` **generates** `.ufo/evidence/round-55/c2/fixture-contract.json`
into the clone before the `env-diff --contract` arm; the file is not committed, so a bare clone
fails that arm with `ENVDIFF_SETUP: [Errno 2] …` instead of the grammar (my first attempt did —
recorded in `00-commands.txt`, and it is a setup artefact, not a round defect).

### Emitter sites (`path:line`, re-resolved at the pinned revs)

**kumitate** — stderr, lowercase `fail-closed —`:
`scripts/cite-check.mjs:2725`, `scripts/surface-probe.mjs:1872`, `scripts/wave-census.mjs:628`,
`scripts/round-gate.mjs:627`, `scripts/proxy-check.mjs:1259`.
stdout duplicate / uppercase variant: `scripts/surface-probe.mjs:1873`
(`SURFACE_PROBE: FAIL-CLOSED (…)`), `scripts/dispatch-evidence.mjs:280`
(`DISPATCH_EVIDENCE: FAIL-CLOSED contract=…`).
Declared map: `SKILL.md:595` — "`2` (fail-closed) and `64` (usage) → could-not-evaluate".

**kagi** — `SETUP` / `POLICY`, stream varies by branch:
`corpus/scope-gate.sh:83` (bootstrap, **stderr**, names the cause), `corpus/scope-gate.sh:102`
(`die()`, stderr, **no class token**), `corpus/scope-gate.sh:184` (**stdout**, names the value),
`corpus/sources-census.sh:120` (stdout), `corpus/row-identity.sh:43` (stdout),
`corpus/op-ref-probe.sh:232` (stderr, `POLICY`, names the value).
Declared map: `SKILL.md:33` ("2 `SETUP`/`POLICY`"), `SKILL.md:700-701` ("2 could-not-evaluate/setup/policy").

**tsukuroi** — no class line; JSON `status`:
`tools/check-freshness-r17.py:310` (code → `CANNOT_EVALUATE` map) emitted at `:321`;
`tools/check-self-assessment.py:1122-1126` (JSON `"status": "CANNOT_EVALUATE"` + exit 2);
docstrings `tools/_revision.py:12`, `tools/check-boot-chain.py:37`.

**mado** — JSON `result` and one enum line:
`tools/mado-assessment.py:166` and `:228` (`'result': 'could-not-evaluate'`);
`tools/mado-evidence-audit.py:117`; `tools/mado-tripwire.py:138` (documented first line),
`:2920` (print), `:3459` (internal-error print → `MADO_TRIPWIRE: could_not_evaluate`).

---

## 3. Negative sweep — the literal label in production code

`git -C <lane> grep -n "could-not-evaluate" -- '*.mjs' '*.js' '*.py' '*.sh'`:

- kumitate: **1 hit, a comment** — `scripts/wave-census.mjs:626`.
- kagi: **0 hits**.
- tsukuroi: hits only in **docstrings** (`_revision.py:12`, `check-boot-chain.py:37`,
  `check-freshness-r17.py:35`, …) plus `.ufo/waves/**` copies.
- mado: hits only in **docstrings** (`mado-assessment.py:5`, `mado-evidence-audit.py:5`,
  `mado-tripwire.py:135-139`) plus `.ufo/waves/**`.

No runtime string in any of the four lanes equals `could-not-evaluate`.

---

## 4. Where the two-lane bar lands (PROVINCE.md:14-17, re-read)

> `owns only the reusable craft (a pattern is admitted from evidence in TWO`
> `independent lanes before it is claimed general)`

Measured against that sentence, dimension by dimension:

| dimension of tameshi's grammar | independent non-tameshi lanes holding it | clears the bar? |
|---|---|---|
| exit 2 ⇒ could-not-evaluate | kumitate, kagi, tsukuroi, mado (+protocol) | yes — and it is protocol law, so it needs no lane evidence |
| one line, tool-prefixed, class token, name-the-cause, exit 2 | kumitate (stderr), kagi (stdout), mado (stdout enum) | yes (3) |
| the same on **stderr** | kumitate, souji | yes — but two of the four *named* lanes are counterexamples (kagi, mado) |
| the literal label `could-not-evaluate` | kama, souji | yes — neither is among the four named |
| prefix + label + **stderr** | souji only | **no** (1) |
| `(could-not-evaluate)` repeated at line end after the quoted value | none | **no** (0) |

The conjunction is therefore unheld by the fleet. That is the honest boundary: every *component*
has two holders somewhere; the *whole line* has none, and the two lanes that carry the label do it
on opposite streams without the suffix.

---

## 5. Contradictions found in the C0 artifacts (stated, not smoothed)

1. **The `<tool>:` slot is not a tool name in 3 of the 8 modes I could exercise.**
   `tools/env-diff.py:235` prints `ENVDIFF_SETUP: could-not-evaluate: …` (both `--selftest` and
   `--contract`) and `tools/bash-witness-study.py:1789` prints `WITNESS_STUDY: could-not-evaluate: …`;
   the live sweep at C0 confirms all eight modes verbatim in
   `T55W2Connector3-receipts/tameshi-eight-modes-streams.txt` (`registry-check --rev` is the ninth
   and is not exercised here — amendment 6 keeps it out of cheap arms). The note
   (`corpus/knowledge/scratch-root-contract.md`,
   `## One line, every mode`) and `SKILL.md:39-41` write the byte shape as
   `<tool>: could-not-evaluate: … (could-not-evaluate)` — i.e. the claim promises a tool name in a
   slot that three of the eight exercised modes fill with a **class** name. The frozen counter cannot see this:
   `c2/measure.py:47-50` matches `[A-Za-z][A-Za-z0-9_.-]*(?:\.py)?` in the prefix position, which
   accepts `ENVDIFF_SETUP` exactly as readily as `repeat-control`. tameshi's own contract flags the
   consequence as unmeasured: `contract.json` C2 `cannot_see` — "whether a caller parses the grammar
   by prefix or by the whole line".
2. **"one line" is not exclusive, and the round's own tool breaks the exclusive reading.**
   `tools/repeat-control.py:234` prints `REPEAT_CONTROL: setup_error` on **stdout** in addition to
   the grammar line (`:233`). Live: rc 2, stdout `REPEAT_CONTROL: setup_error`, stderr the grammar
   line (receipt `tameshi-repeat-control.out/.err`). kumitate does the same dual emission
   (`surface-probe.mjs:1872` + `:1873`), so **the dual shape is the one with sibling precedent**;
   the exclusively-single-stderr-line shape is tameshi's own. A wave-3 critic reading "one line"
   as exclusivity will score this as a violation of the lane's own contract.
3. **Wave-1's layer (b) table overstates stream uniformity.** It lists a "line carrying the class"
   as fleet-general across six lanes; re-measured on the four named here, 2 of them (tsukuroi,
   mado-assessment/mado-evidence-audit) carry it *only* as a JSON field, and kagi writes its
   `SETUP` on stdout. A class **line** on **stderr** is held by one of the four.

None of these is a defect in the frozen counter's arithmetic; all three are prose-vs-artifact
divergences that an operability reader will hit.

---

## 6. Proposed move (one, bounded, prose-only)

**Move.** In `corpus/knowledge/scratch-root-contract.md` `## One line, every mode` (and the
matching `SKILL.md` `## Standing rules` bullet, which the reader seats already force a re-key of):

1. change the byte shape from `<tool>: …` to **`<name>: …`** — it then matches what the nine modes
   actually print (`repeat-control`, `context-capture.py`, `registry-check`, `ENVDIFF_SETUP`,
   `pin-disposition.py`, `evidence-disposition.py`, `WITNESS_STUDY`) and it matches the frozen
   regex, so no counter byte moves; and
2. add three sentences under the byte shape: **exit class 2 is protocol-pinned** (`PROTOCOL.md:380-383`)
   and held by kumitate/kagi/tsukuroi/mado (their emitters named); **the line shape is lane-owned**
   — `PROTOCOL.md:380-383` refuses to pin it; **nearest siblings differ in stream** — kumitate
   `surface-probe: fail-closed — …` on stderr *and* `SURFACE_PROBE: FAIL-CLOSED (…)` on stdout
   (dual emission, as `REPEAT_CONTROL: setup_error` is here), kagi `ADJACENCY_SCOPE: SETUP (…)` on
   stdout, tsukuroi/mado carry the class only in a JSON field; no sibling repeats the class token at
   line end.

That converts an unmeasured generalisation risk into a declared, cited lane scope, which is the
operability gain: a parity seat no longer has to guess which half is fleet norm.

**Why not the alternative fix** (delete `REPEAT_CONTROL: setup_error`, `repeat-control.py:234`):
it changes tool bytes after C0, forces a re-freeze of the C2 measured revision, and contradicts the
one sibling precedent that exists (kumitate dual-emits). The counter never measured exclusivity, so
the edit buys nothing the prose does not.

**Axes.** operability ↑ (scope of the claim becomes checkable, prefix slot stops being a false
promise); calibration = (no SCORECARD row, no corrections entry, no counter byte touched);
evidence = (adds three pinned sibling citations); coverage = (three sibling emitters mapped).

**Risks.**
- The C2 `note` arm is a substring test (`c2/measure.py:257-259`, marker `:46`): the marker
  `could-not-evaluate: cannot create clone scratch under the scratch root` and all nine mode names
  must survive the edit. The proposed sentences name lanes, not modes, so the arm stays 9/9 — but
  the landing seat must re-run it to prove that, not assume it.
- Sibling line numbers move: souji advanced to `ed30b7f5b7` mid-scan. Any citation in the note must
  be by `path:line at <rev>`, never by worktree.
- If the round wants generality language after all, it must cite kama + souji for the *label* and
  still concede the conjunction is unmatched; the two-lane bar cannot be reached for the whole line.

**Verification of the move (for the landing seat).**
`python3 .ufo/evidence/round-55/c2/measure.py --lane LANE --rev <landing> --work <empty> --explain`
→ `grammar=9/9 … docs=7/7 note=9/9 skill=1/1 total=0 C2_R55_PASS=true`; plus
`grep -n "tool>:" corpus/knowledge/scratch-root-contract.md SKILL.md` → no hits; plus the four
sibling receipts above unchanged.

---

## 7. Bounds actually exercised

- Lane production files untouched; write scope is `.ufo/waves/round-55/w2/` only —
  `git status --porcelain -- .ufo/waves/round-55/w2` → `?? .ufo/waves/round-55/w2/`.
- All sibling work on `git clone --shared` copies under
  `/fast/scratch/hyaku/tameshi-r55/T55W2Connector3/`; no mutating git in any lane; the tameshi
  clone was `checkout`ed only inside scratch.
- Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi`
  → `tameshi ok …` exit 0 (140-row validation).
- No tool installed or upgraded; nothing written outside the report dir and scratch.

## 8. Artifacts opened

tameshi: `.ufo/evidence/round-55/contract.json`, `.ufo/evidence/round-55/c2/measure.py`,
`PROVINCE.md:1-30`, `SKILL.md` (`## Standing rules` at C0 via `git show`),
`corpus/knowledge/scratch-root-contract.md` (at C0 via `git show`), `.ufo/waves/round-55/w1/T55W1Connector1.md`,
`.ufo/waves/round-55/w1/T55W1Connector1-receipts/03-fleet-protocol-and-province.txt`,
`…/06-kumitate-and-tsukuroi-emitters.txt`, `PROTOCOL.md:376-384`.
kumitate: `scripts/surface-probe.mjs`, `scripts/cite-check.mjs`, `scripts/wave-census.mjs`,
`scripts/round-gate.mjs`, `scripts/proxy-check.mjs`, `scripts/dispatch-evidence.mjs`, `SKILL.md`.
kagi: `corpus/scope-gate.sh`, `corpus/sources-census.sh`, `corpus/row-identity.sh`,
`corpus/op-ref-probe.sh`, `SKILL.md`.
tsukuroi: `tools/check-freshness-r17.py`, `tools/check-self-assessment.py`, `tools/_revision.py`,
`tools/check-boot-chain.py`.
mado: `tools/mado-assessment.py`, `tools/mado-evidence-audit.py`, `tools/mado-tripwire.py`.
kama: `tools/seat-report-immutability.py`, `tools/append-only-audit.py`.
souji: `census/round-19/verify-agreement-pin.py`, `census/round-22/mutation-adequacy.py`.
