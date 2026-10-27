# T52W1Corr08 — correction record for round-51 re-key `### The tick and the pin read`

Seat: T52W1Corr08 (scribe). Item: derive the reader's own findings for the round-51 re-key entry
`### The tick and the pin read` (read_rev `02ec217c4d0afabe727fde2e261b7951d28fb4e9`, reader `T51W2Read08`)
and emit one correction record with `wrong_expectations == len(findings)`.

Deliverable: `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-52/w1/T52W1Corr08.json`
(sha256 `345d86dd1b31f5c82a4cf2543b809d20964fda1c545fe37bc02c8d9c84e799fd`, 6 keys, 2 findings).

## What was read (identities first)

| Item | Command | Observed |
|---|---|---|
| Contract, frozen counters, controls, read first, never edited | `read .ufo/evidence/round-52/contract.json` | C2 m4 = "one correction record per round-51 cold-read re-key entry (20) … with verbatim reader quotes and wrong_expectations == len(findings)"; T51W2Read08 is one of the 20 |
| Section identity at read_rev | `git show 02ec217c…:SKILL.md` lines 1021-1068; heading line 1021, next heading (`### Triggers T1–T3 and the re-pin rule`) at 1069 | heading exact `### The tick and the pin read`, 1021-1068; `'\n'.join(lines[1020:1067])` hashes to `60d658245f87d166809e43a14a1bc8b873d2604032b37fa9ab6c3d2965ed5853`, equal to the ledger entry's `sha256` and the reader's `section_sha256` |
| Reader file, in full, byte hash | `sha256sum .ufo/evidence/round-51/coldread/reads/T51W2Read08.md` | `0f8a0efc3cb63968da16a889dc8d421cc29bb14bf65474a8b2f47d2cf2cbf95c`, 127 lines |
| Ledger entry this record corrects | `.ufo/evidence/round-21/coldread/ledger.json`, entry with `heading` = this heading and `read_rev` prefix `02ec217c` | exactly 1 entry; `seats: ["T51W2Read08", "L1 TameshiR51a3 integration (attempt 3)"]`; recorded `wrong_expectations: 0`, `minor_gaps: 0`, `verdict: "verified-record"` — the refresh.py code-written zeros of routed defect 3 (`corpus/lessons/round-51-verifier-spotcheck.md`, "Routed defects" item 3) |
| Counter rule I must satisfy | `.ufo/evidence/round-52/c2/measure.py:82-95` (`check_findings`) and `:150-165` (m4) | quote must be non-empty, `squash(q)` length ≥ 20 and a substring of `squash(reader_text)`; record must match on `heading`, `read_rev` prefix, `reader == seat`, `reader_file == .ufo/evidence/round-51/coldread/reads/<seat>.md`, and `wrong_expectations == len(findings)`. `FLOORS` has no entry for T51W2Read08 |

## Findings (2)

### F1 — stale-count, `MUTATE_SELFTEST: 67/67`

- Reader text: `T51W2Read08.md:11` — `- **Current-engine self-test count is stale, but its historical framing matters.** … the CAND runner receipt prints `MUTATE_SELFTEST: 107/107 pass`; base-era receipts already print `106/106`. Thus the number was already stale as a current-engine count before this round`. The reader's own pointer row for `MUTATE_SELFTEST: 67/67` (`:75-80`, verdict at `:79`) carries `"verdict": "absent"`.
- Section statement: `SKILL.md:1062-1064` — "the engine's own doctored-pin refusal is a different arm, selftested `MUTATE_SELFTEST: 67/67`". The clause carries no date qualifier at that point; it is presented as the engine's selftest output.
- Corroboration that the count is not the current one (probe, not a verdict): `git show 02ec217c…:tools/mutate-and-run.sh | grep -n MUTATE_SELFTEST` → the emitter is `:2125  printf 'MUTATE_SELFTEST: %s/%s pass\n' "$((cases - failed))" "$cases"`, a computed tally, not a fixed 67; the receipt the reader cites, `.ufo/waves/round-51/w1/T51ExecEmbed/selftest.stdout:108`, reads `MUTATE_SELFTEST: 107/107 pass`.
- Quote in the record: `Current-engine self-test count is stale, but its historical framing matters.` (76 chars, substring of line 11).

### F2 — unsupported, the three readings are not exhaustive

- Reader text: `T51W2Read08.md:13` — `- **Potential taxonomy gap (strongest falsifier checked).** The stated `current`/`stale`/`drift` readings leave a possible history-rewrite case unclassified if the three labels are meant to be exhaustive. … Applying the section's rules yielded `current=no, stale=no, drift=no``. Restated in the structured row at `:67` ("If the three labels are exhaustive, this is an unclassified edge case") and at `:121-122` (`"result": "No stated label applies…"`).
- Section statement: `SKILL.md:1027-1028` frames the readings as the pair "the target's relation to each repo's branch-tip bytes (`current` / `stale` / `drift`)", and the three rule rows at `:1033-1035` define only those three; the `stale` row (`:1034`) requires "the recorded revision is an ancestor of `refs/heads/<branch>`", so a non-ancestor rewritten branch tip falls outside all three rules. The section supplies no fourth label.
- Boundary recorded honestly: the reader's pointer verdict on the rules themselves is `"holds"` (`:66`) — "Rules match the six recorded cases" — and it explicitly says this "demonstrates an uncovered state, not a contradiction in the six recorded examples". I record it as `unsupported` (the exhaustiveness premise is unsupported), not `false`.
- Quote in the record: `The stated `current`/`stale`/`drift` readings leave a possible history-rewrite case unclassified` (96 chars, substring of line 13).

## Deliberate exclusions (reader notes that are holds or dated-and-accurate)

| Reader note | Where | Why not counted |
|---|---|---|
| `/tmp/w8-tameshi-t84/pin-read.txt`, `/tmp/w8-tameshi-t84/drift-demo.txt` do not exist now (pointer verdicts `absent`) | `:12`, `:90-102` | The reader marks them as dated round-8 scratch observations: "They are presented as round-8 scratch observations; they cannot be replayed from those paths now. The runner's current TMPDIR/scratch policy does not change the truth of those dated observations." The section never claims they exist now, so this is disclosure, not a failing statement. |
| Historical host/time and transient live mado worktree state "not re-observable now", "not disproved" | `:15` | Reader's own wording: not disproved. |
| mado HEAD-at-round-8 pin `90d50cdd…` correct; live `dc864c6a…` no longer present; `050efc72…` is the present file | `:14`, `:84-88` | Reader verdict `holds` for the dated pin; the section's drift paragraph says "never carried as a standing claim". Historical and accurate. |
| Tool pin `cf41efaa…` differs from present runner sha `977de470…` | `:69-74` | Reader calls the section's pin "the explicitly dated round-8 `cf41efaa…` tool pin" — verdict `holds`. |
| Six-row pin table, `MARKERS`, round-17 cross-reference, `:14` lane map, `shokunin.conf` | `:26-117` | All `"verdict": "holds"`. |
| `67/67` repeated at `SKILL.md:1003` and `:1218` | reader `:11` | Outside lines 1021-1068; other sections, others' reader records. |

## Self-check output (the frozen counter's rule, `check_findings`)

Loaded the frozen counter module and called `check_findings(rec['findings'], reader_text, ())`, plus a per-line byte-exact check:

```
counter-check: None
count==findings: True 2
per-line-substring lines=[11] len=76 class=stale-count quote='Current-engine self-test count is stale, but its historical framing matters.'
per-line-substring lines=[13] len=96 class=unsupported quote='The stated `current`/`stale`/`drift` readings leave a possible history-rewrite case unclassified'
squashed-substring-all: True
keys: ['findings', 'heading', 'read_rev', 'reader', 'reader_file', 'wrong_expectations']
```

`None` is `check_findings`' success return (`.ufo/evidence/round-52/c2/measure.py:82-95`); both quotes are also byte-exact substrings of exactly one reader line (11 and 13).

Record/entry match simulated in memory against the real ledger (no lane write):

```
check_findings: None
matching ledger entries: 1 [['T51W2Read08', 'L1 TameshiR51a3 integration (attempt 3)']]
entry wrong_expectations recorded: 0 minor_gaps: 0 verdict: verified-record
seat: T51W2Read08 reader match: True reader_file ok: True
heading ok: True read_rev prefix ok: True 40
corrections list present: False 0
```

The ledger currently has no top-level `corrections` list (`ledger.json` keys: `schema`, `entries`, `carried_from`, `provenance`, `round21_provenance`), so this record is a file for the L1 to append to `corrections`; I did not edit the ledger (lane read-only outside my named files).

## Bounds and surfaces

- Files written: `.ufo/waves/round-52/w1/T52W1Corr08.json` (deliverable) and this report. Nothing else. No lane, fleet, sibling-lane, jj, Git-index or registry edit; no `git add/commit/checkout/reset`.
- No scratch dir was created for this seat: every check was a read (`read`, `git -C <lane> show`, `sha256sum`, in-memory Python). No `/tmp` or scratch path is cited as evidence.
- Counters: none run against the lane. I imported the frozen C2 module and called `check_findings` only, as a probe.
- Tooling: nothing installed or upgraded (the host pacman guard was not touched; no uv/npx/binary changes were needed).
- Out of scope, for the L1: appending the record to the round-21 ledger `corrections` list, re-scoring m4/m6 at the content revision, and the SKILL.md text fixes that F1/F2 point at (C2 m1-m3/m6 owners). F1's `67/67` also appears at `SKILL.md:1003` and `:1218` in other sections — not fixed or claimed here.

## Summary

- Read the round-52 contract, the C2 counter (m4 + `check_findings`), the round-51 routed defects, the reader file in full, and section 1021-1068 at `02ec217c`.
- Reader `T51W2Read08` recorded 2 statements that do not hold at its candidate; the ledger entry records `wrong_expectations: 0`/`minor_gaps: 0` from `refresh.py` code.
- F1 `stale-count`: section's `MUTATE_SELFTEST: 67/67` is not the current count (emitter is a computed tally; cited receipt prints 107/107).
- F2 `unsupported`: the `current`/`stale`/`drift` label set leaves a non-ancestor rewrite unclassified; reader demonstrated `current=no, stale=no, drift=no`.
- Five reader notes excluded as `holds` or dated-and-accurate (`/tmp` scratch paths, host/time, mado drift, dated tool pin, six-row table) — reasons tabulated.
- Deliverable `.ufo/waves/round-52/w1/T52W1Corr08.json` passes `check_findings` (`None`), quotes are single-line byte-exact, `wrong_expectations == 2 == len(findings)`, record fields match the m4 selectors.
- Ledger append and m4/m6 re-scoring are the L1's; the SKILL text fixes belong to the C2 statement-set owners.
