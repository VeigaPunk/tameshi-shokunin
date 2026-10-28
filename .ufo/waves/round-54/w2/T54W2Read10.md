# T54W2Read10 — wave-2 cold read at C1

Seat: `T54W2Read10` (leaf reader, round 54 / hyaku run 11, wave 2).
Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`
Candidate read: `99c3bc88d704566197783f66b211ee0a830e0330` (C1)

## Section

| field | value |
|---|---|
| heading | `### The operator's runbook — \`corpus/knowledge/operator-runbook.md\`` |
| start / end (reader-section.py) | `1304` / `1324` |
| hashed body | lines `1304..1323` (20 lines; end=1324 is the blank line before the next H3 at 1325, trailing blanks stripped by the round-18 `sectionize`) |
| section_sha256 | `8801894537fb0c2821f0916cc2826a9e4c8d907f5acb1931bb9b05733b2afc12` |

## Verdict

**0 findings.** Every anchor named in the section resolves at C1, no sentence
contradicts another in the section, no cited cell is stale against the artifact it
cites, and no run-together token / missing space / duplicate parenthetical is present.

## Commands run (in order)

Scratch and TMPDIR as the seat spec requires:

```
cd /home/vgpnk/Projects/shokunin/tameshi-shokunin
mkdir -p /fast/scratch/hyaku/tameshi-r54/T54W2Read10
export TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read10
python3 .ufo/waves/round-54/reader-section.py \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin \
  99c3bc88d704566197783f66b211ee0a830e0330 \
  "### The operator's runbook — \`corpus/knowledge/operator-runbook.md\`"
```

Output (verbatim):

```
{"heading": "### The operator's runbook \u2014 `corpus/knowledge/operator-runbook.md`", "cand": "99c3bc88d704566197783f66b211ee0a830e0330", "start": 1304, "end": 1324, "section_sha256": "8801894537fb0c2821f0916cc2826a9e4c8d907f5acb1931bb9b05733b2afc12"}
```

Section bytes and independent hash reproduction:

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show \
  99c3bc88d704566197783f66b211ee0a830e0330:SKILL.md | sed -n '1304,1324p' | cat -A
python3 - <<'EOF'   # round-18 sectionize body, joined with \n, no trailing newline
raw = subprocess.run(['git','show','99c3bc88...:SKILL.md'],capture_output=True).stdout
...  body = lines[1303:1323]
EOF
```

Output:

```
20 8801894537fb0c2821f0916cc2826a9e4c8d907f5acb1931bb9b05733b2afc12
```

Anchor-resolution commands and outputs:

```
git -C <lane> show 99c3bc8:corpus/knowledge/operator-runbook.md | sha256sum
  8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859  -
git -C <lane> show 59c38109:corpus/knowledge/operator-runbook.md | sha256sum
  8b2e185ff011f6cfc2aee187ff1c2a1f8120e410c00f4b67eb6c7f1ebabb6859  -
git -C <lane> show 59c38109:corpus/knowledge/operator-runbook.md | wc -lc
      516   33515
git -C <lane> show 99c3bc8:corpus/knowledge/operator-runbook.md | wc -lc
      516   33515
git -C <lane> ls-tree -l 99c3bc8 corpus/knowledge/operator-runbook.md
  100644 blob 54c72164fa76f0a00f3b0bf1a2af6a87518a326b   33515  corpus/knowledge/operator-runbook.md
git -C <lane> show 99c3bc8:SKILL.md | awk 'NR>=1275 && NR<=1278'
  1275: the same rows as the detail of record — verbatim anchor quotes, the trigger column
  1276: and the intake-precondition check; this page is the compact rendering, and a
  1277: divergence between the two is the finding, never smoothed.
git -C <lane> show 99c3bc8:SKILL.md | awk 'NR<=1277 && /^#/ {h=NR": "$0} NR==1277 {print h}'
  1265: ### The service's limits — what tameshi refuses to mutation-test   (= the section the anchor points into)
git -C <lane> show 99c3bc8:corpus/knowledge/operator-runbook.md | grep -n '^#'
  1:# Operator runbook — ... (round 10, T10-1)
  35:## 0. Quick start — the operator loop in one block
  65:## 1. The service in one page
  93:## 2. The tool — `tools/mutate-and-run.sh`
  131:## 3. The six-case ledger — the standing view
  180:## 4. The opt-in protocol — running/commissioning a sweep
  243:## 5. The limits — what the service refuses
  269:## 6. The cadence — the tick, the reading map, the triggers
  345:## 7. The regression mode — replaying the recorded legs
  408:## 8. The operator's full loop — commissioning to append
  438:## 9. Receipts from this writing — what was actually executed
  462:## 10. Unknowns carried — the service's open questions
  481:## Errata (append-only)
git -C <lane> show 99c3bc8:corpus/knowledge/operator-runbook.md | sed -n '269,345p' | grep -n "T1\|T2\|T3"
  20:- **T1 — a case reads `stale`** ...
  22:- **T2 — the harness sha ≠ the revision a case was measured under** ...
  25:- **T3 — an owner records a re-run at a new revision** ...
git -C <lane> show 99c3bc8:corpus/knowledge/operator-runbook.md | sed -n '345,380p'
  ... "**Embedding status:** four legs at this revision (cases 1–4); cases 5/6 are **not embedded** ..."
git -C <lane> show 99c3bc8:corpus/knowledge/operator-runbook.md | sed -n '438,462p'
  ... "--regression (above, §7) → rc 0, `cases=4 passed=4`, exact band. [O]" ...
git -C <lane> show 99c3bc8:corpus/knowledge/operator-runbook.md | sed -n '478,516p'
  ... "**ER-R1 — post-write tool drift ...** Every receipt in this runbook (§2, §6, §7, §9)
       was executed at tool `cf41efaa8be5f5...` (r7-1) ... **T2 is the fix** — when the edit
       lands, re-run `--selftest` and `--regression` under the new revision and record both pins"
  ... "**ER-R2 — the tool still in motion at close ...** VERSION line still r10-2 ..."
for c in $(git log --all --format=%H -- tools/mutate-and-run.sh); do
  h=$(git show $c:tools/mutate-and-run.sh | sha256sum); case "$h" in cf41efaa*) echo MATCH;; esac; done
  MATCH 9f1d3c339a7094968041c7708a65dbf7eab9fae6 cf41efaa8be5f52d92bf7806ddb3a99a031547bf12a6811b8ef45bce37242c75
git -C <lane> show 9f1d3c33:tools/mutate-and-run.sh | grep -n "VERSION="
  135:VERSION='mutate-and-run.sh r7-1 (tameshi-shokunin, 2026-10-14)'
git -C <lane> show 99c3bc8:SKILL.md | sed -n '1324,1400p'
  ### The six-leg regression — usage and this round's receipt
  ... "**Receipt, executed by this lane** ..., tool `75ed934d…` before and after ..."
  ... "- `--selftest` → `MUTATE_SELFTEST: 80/80 pass` at r10-2 ..."
  ... "- `--regression` → six legs at r10-2 ..., closing `REGRESSION: PASS (cases=6 passed=6; ...)`"
for c in $(git log --all --format=%H -- tools/mutate-and-run.sh); do
  h=$(git show $c:tools/mutate-and-run.sh | sha256sum); case "$h" in 75ed934d*) echo MATCH;; esac; done
  MATCH 606716f703f7699af458476a31fc78ddc9bf552c 75ed934dc86360f5c2cdd5b17abb8814249425e9c1835d36b81d74412719adc5
git -C <lane> show 99c3bc8:SKILL.md | sed -n '1304,1323p' | grep -nP '(?<=\S)  +|\(\s*\(|\b(\w+) \1\b'
  (no output — no mid-line double space, no doubled parenthesis, no repeated word)
git -C <lane> show 99c3bc8:SKILL.md | sed -n '1304,1324p' | cat -A
  (clean ASCII/UTF-8: em dash `M-bM-^@M-^T`, section sign `M-BM-7`/`M-BM-'`, ellipsis as U+2026, no stray NBSP/tab)
```

## Anchor table — each named anchor and its resolution at C1

| claim in the section | verification | result |
|---|---|---|
| document `corpus/knowledge/operator-runbook.md` | `git ls-tree 99c3bc8` | present, blob `54c72164…`, 33 515 B |
| `8b2e185f…` (sha of that document) | `sha256sum` of the blob at C1 **and** at `59c38109` | `8b2e185ff011f6cf…` — matches the 8-hex prefix |
| `/ 516 L / 33 515 B` | `wc -lc` on the blob | `516 33515`; last byte is `0x0a`, so 516 newline-counted lines = 516 displayed lines |
| `committed at 59c38109` | `git ls-tree -l 59c38109 corpus/knowledge/operator-runbook.md` | same blob `54c72164…`, same 33 515 B — the commit carries exactly the pinned bytes (same sha256 at C1, unchanged) |
| `the sha governs` | hash equality above | resolves: the pinned sha is the content sha256 of the committed blob |
| Section map §0–§10 + errata | `grep -n '^#'` on the runbook | all eleven numbered sections plus `## Errata (append-only)` exist with the described titles; §6 does carry `T1`/`T2`/`T3` bullets |
| "the tool, the six-case ledger, the opt-in protocol, the refusals, the cadence, and the regression mode" | runbook headings §2/§3/§4/§5/§6/§7 and its own preamble line | exact six-item match ("the limits" in the runbook = "the refusals" in SKILL) |
| "It adds no gate measurement of its own; every line restates an anchored source." | runbook preamble + §9 closing | runbook states the same rule verbatim in substance ("This runbook adds no gate measurement of its own: every line restates a measured source and carries its anchor") |
| runbook's own divergence rule ("the anchored source governs") | runbook lines 9–11 | present verbatim |
| `:1276-1277` (rendering/divergence rule for `service-limits.md`) | SKILL 1275–1278 at C1 | lines 1276–1277 read "…this page is the compact rendering, and a divergence between the two is the finding, never smoothed."; nearest heading above is `:1265 ### The service's limits …` — correct target, anchor resolves |
| `cf41efaa…` + `(r7-1, four legs)` | content hash sweep over every committed `tools/mutate-and-run.sh` | matches blob at `9f1d3c33`, whose `VERSION` is `mutate-and-run.sh r7-1`; runbook §7 says "four legs at this revision (cases 1–4)" and §9 records `cases=4 passed=4` |
| "§7's embedding-status line and §9's receipts were run there" | ER-R1 ("Every receipt in this runbook (§2, §6, §7, §9) was executed at tool `cf41efaa…` (r7-1)") + runbook revision-stamp table (`cf41efaa8be5f52d`, 1341 L) | resolves |
| "its errata ER-R1/ER-R2 record the r10-2 edit in motion" | runbook errata | ER-R1: VERSION `r10-2`, uncommitted worktree file; ER-R2: re-read still `r10-2`; both present and append-only |
| "name the T2 remedy (re-run under the new revision, record both pins)" | ER-R1 | "**T2 is the fix** — when the edit lands, re-run `--selftest` and `--regression` under the new revision and record both pins" — exact |
| "The receipt below is that T2 record." | next H3 `:1325` | records tool `75ed934d…` (matches committed tool blob at `606716f`) and both pins: `--selftest 80/80 pass` and `--regression` six legs `cases=6 passed=6`, rc 0 — i.e. the T2 (selftest + regression) record |

## Adversarial attempts that were examined and cleared (not findings)

1. **`8b2e185f…` is not a git object.** `git cat-file -t 8b2e185f` → `fatal: Not a
   valid object name`. Cleared, not reported: it is a content sha256, the document's
   own pin format (`SKILL.md:161` "Record: path, full sha256, size"; `SKILL.md:1017`
   annotates `cf41efaa…` as "a content sha, not a git revision"), and the bytes it
   names are reachable through the adjacent `committed at 59c38109`, where the
   `sha256sum` matches. This is the same pin style used in the very next bullet.
2. **`59c38109` vs the runbook's own last-touching commit `58e5d53`.** The phrase
   "committed at `59c38109`" is verified literally: that commit's tree carries the
   pinned blob and hash. Cleared.
3. **"that lane's executed receipts" (§9) has no lane name inside the section.**
   Within 1304–1323 `grep -c T10-1` = 0; the antecedent is the immediately preceding
   paragraph of the same page (`:1301` "(T10-1, this round)"), and runbook §9 itself
   names "the author lane (T10-1)". Interpretable without oral context; not a
   contradiction, not reported.
4. **"four legs" vs the six/ten-leg regression.** Different revisions by
   construction: the section pins r7-1 (four legs) for the runbook receipts and then
   points at the T2 receipt below (r10-2, six legs; ten since round 51) in its own
   words. No contradiction. Cleared.
5. **Line-count convention ("516 L").** The runbook ends with `0x0a`, so
   `wc -l` = displayed lines = 516; the +1 caveat the runbook states for `SKILL.md`
   and the ledger does not apply here. Cleared.
6. **Typography sweep (QUALITY 104).** No mid-line double space, no tab/NBSP, no
   doubled `((`, no repeated word, balanced parentheses in all four bullets; the only
   non-ASCII characters are the intended em dash, `§`, `·`, `…`, `–`. Cleared.

## Artifacts opened

- `SKILL.md` at `99c3bc88d704566197783f66b211ee0a830e0330`, lines 1290–1400 (section
  bytes 1304–1324 plus the preceding paragraph and the following H3 `:1325`).
- `corpus/knowledge/operator-runbook.md` at `99c3bc8` and at `59c38109` (full
  headings, preamble/revision-stamp table, §6 triggers, §7 embedding status,
  §8–§9 receipts, errata `478–516`).
- `tools/mutate-and-run.sh` at `9f1d3c33` and `606716f` (content-hash sweep across
  every committed revision of the path; VERSION line at `9f1d3c33:135`).
- `.ufo/waves/round-54/reader-section.py` (to know exactly which bytes
  `section_sha256` covers).
- `.ufo/evidence/round-18/measure.py` at `99c3bc8` — `sectionize()` (hashed body =
  heading line .. line before next heading, trailing blanks stripped, `\n`-joined,
  no trailing newline).
- `git diff 59c38109 99c3bc8 -- SKILL.md` (the C1 fix hunks at `@@ -1303,8 +1303,8`
  and `@@ -1316,7 +1316,7`, i.e. this section's pin and anchor).

## Scope and provenance

- No lane file, counter, contract, freeze, ledger or wave spec was edited. Wrote
  only `.ufo/waves/round-54/w2/T54W2Read10.json` and `.ufo/waves/round-54/w2/T54W2Read10.md`.
- No mutating git/jj command was run anywhere; all reads use `git show`/`ls-tree`/
  `log --all`/`rev-list` against the lane and `sha256sum`/`wc` on object bytes.
  No fixture directory was needed for this reader seat.
- Scratch: `TMPDIR=/fast/scratch/hyaku/tameshi-r54/T54W2Read10` (also used by
  `reader-section.py` for its temporary `measure.py`); no file left behind.
- Tooling: nothing installed or upgraded (pacman paused host-wide); used only the
  preinstalled `python3`, `git`, `sha256sum`, `wc`, `sed`, `awk`, `grep`, `xxd`.
- Wave-1 reader JSONs were not opened; this read is of the C1 bytes only.

Report: .ufo/waves/round-54/w2/T54W2Read10.md
