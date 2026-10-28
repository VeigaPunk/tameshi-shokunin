# T55W2RevWaveArtifacts — wave-1 artifact integrity at C0

Seat `T55W2RevWaveArtifacts`, reviewer, round 55 wave 2 (falsify), milestone *wave-1 artifact
integrity*. Lane `tameshi-shokunin`, read at `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb` (C0).
Read-only on the lane: every command below ran in a `git clone --shared` at C0
(`/fast/scratch/hyaku/tameshi-r55/T55W2RevWaveArtifacts`, removed on exit) or was a `git`-read
against the lane. No lane production file, no frozen file, no wave spec was edited. No tool was
installed (python3 + git only; the RULES.md install path was not entered).

Receipts, all under `.ufo/waves/round-55/w2/T55W2RevWaveArtifacts-receipts/`:

| receipt | what it holds |
|---|---|
| `audit-w1-counts.txt` (+ `audit_w1.py`) | the count table of §1, one `git ls-tree` + set algebra over the dispatch |
| `er10-bytes.txt` | C0 sizes/sha256 of `T55W1Er10.{json,md}`, the `seat`/`id`/`old` probe, the pointer's first lines, and a 1254-file scan proving the restored bytes are nowhere in the tree |
| `er10-write-timeline.txt` (+ `.py`) | every tool-call write/edit/read on `T55W1Er10.{json,md}` recovered from the wave's session logs, with UTC timestamps |
| `claims-sweep.txt` (+ `sweep_claims.py`) | every backticked path token on a claim-verb line of all 59 wave-1 `.md` files, tested against the C0 tree / disk: 3 residues, all adjudicated below |
| `claims-adjudication.txt` | the eight claim/fact pairs examined, quoted, with the bytes that falsify or support each |
| `post-c0-landing.txt` | the 12 no-artifact seats: C0 membership vs worktree mtimes vs `git status` |
| `receipt-sections-summary.txt` (+ `sweep_receipt_sections.py`) | the deliverable-section citation sweep (612 tokens, 39 seats) that found `coldread-at-base.json` |

Artifacts opened by name: `.ufo/waves/round-55/{spec-w1.json, w1-dispatch.json, w1.ready,
w1.ready.dispatched, w1-run.err}`, all 59 `.md` and 43 `.json` files at the `w1/` root of C0,
the receipt dirs of `T55W1Er10`, `T55W1ScribeSources`, `T55W1ScribeMistakeSweep`,
`T55W1ScribeNote`, `T55W1RevWave`, `T55W1RevSources`, `T55W1Rev08`, `T55W1Rev05`,
`T55W1RevQuality`, `T55W1ExecNoHarm`, `T55W1ExecReKeyDryBind`, `T55W1MutC2`,
`T55W1ExecC2Full`, `T55W1ExecNote`, `T55W1ExecCensusAfter`; the wave session logs under
`~/.omp/agent/sessions/-Projects-shokunin/2026-10-28T14-01-34-216Z_01a182d0-f308-7371-97bc-ca8b0ed0633f/`
(read-only) — `T55W1Er10.jsonl`, `T55W1ScribeNote.jsonl`, `T55W1ScribeSources.jsonl`,
`T55W1ScribeMistakeSweep.jsonl`, `T55W1ExecRekeyPrep.jsonl`, `T55W1Revenger.jsonl`,
`T55W1CritC2.jsonl` and the 859-file sweep over that directory.

---

## 1. Counts — 75 dispatched, 63 seats with any artifact, 57 with a report

```
$ python3 audit_w1.py     # receipts/audit-w1-counts.txt
dispatch counts          : {'spawn': 75, 'resume': 0, 'total': 75}
w1 files at C0           : 1254
root .md files           : 59  seat-named: 57
root .json files         : 43  seat-named: 41
non-seat root .md        : ['T55W1ExecReKeyDryBind.reader', 'T55W1ScribeLesson-draft-round-55']
non-seat root .json      : ['T55W1ExecReKeyDryBind.reader', 'swarm-registry']
receipt dirs             : 63  all dispatched: True
seats md+json            : 39
seats md only            : 18   seats json only: 2   seats receipts only: 4
seats with nothing       : 12
md present total         : 57 / 75
json present total       : 41 / 75
any artifact total       : 63 / 75
```

- The two non-seat `.md`/`.json` names are legitimate: `T55W1ExecReKeyDryBind.reader.{md,json}`
  is the reader pair its own item required beside the executor report, and
  `T55W1ScribeLesson-draft-round-55.md` is the lesson draft the lesson scribe cites.
- md-only (18): Connector1, ExecCcPatch, ExecGrammarBreak, ExecNoHarm, ExecRepPatch, LabMode,
  Rev02, Rev04, Rev08, RevColdread, RevQuality, ScribeLesson, ScribeLog, ScribeNote,
  ScribeQuality, ScribeScratchDoc, ScribeSeat, ScribeSkill.
- json-only (2): `T55W1LabEmpty`, `T55W1ScribeCells`.
- receipts-only, no report file (4): `T55W1ExecC2Full`, `T55W1ExecCensusAfter`,
  `T55W1ExecNote`, `T55W1MutC2` — each has a populated `-receipts/` dir and neither a `.md`
  nor a `.json` at C0.

All 42 `.json` files at the C0 root other than `swarm-registry.json` (41 seat-named plus the
`.reader` pair) parse (`json.loads` on each; 0 failures) and every one carries an identity key
(`seat` / `id` / `heading` / `_not_a_reader_report`). Every seat-named `.md`'s first
heading names its own seat — the only two exceptions are the two non-seat files above, so no
report at C0 sits under the wrong name *except* the pair in §3.

## 2. The 12 seats with nothing at C0 — and why that is not 12 dead seats

At C0 these 12 have no `md`, no `json`, no `-receipts/`:
`T55W1CritC2`, `T55W1CritClaimShape`, `T55W1CritGate`, `T55W1CritSourcedClaim`,
`T55W1ExecFooterPaths`, `T55W1ExecRegistryGate`, `T55W1MutC1`, `T55W1RevLedger`,
`T55W1RevRekeyByteProof`, `T55W1Revenger`, `T55W1SentConfig`, `T55W1Simplifier`.

C0 was committed at `2026-10-28 14:16:25 -0300` (`17:16:25Z`). Every one of the twelve has a
live transcript whose last event is *after* that instant (17:30:47Z–17:37:12Z), and ten of them
wrote their reports into the worktree 2–22 minutes after C0 (`receipts/post-c0-landing.txt`):

```
T55W1CritClaimShape   md 14:32:57 22694B  json 14:32:16  8396B
T55W1CritGate         md 14:27:09 19828B  json 14:24:17  8845B
T55W1CritSourcedClaim md 14:26:01 25641B  json 14:25:38 12989B
T55W1ExecFooterPaths  md 14:25:38 22142B  json 14:24:20 10815B
T55W1ExecRegistryGate md 14:26:04 11573B  json 14:26:18  5952B
T55W1MutC1            md 14:31:56 19186B  json 14:32:08 14882B
T55W1RevLedger        md 14:38:10 27956B  json 14:37:36 12675B
T55W1RevRekeyByteProof md 14:30:20 22625B json 14:29:10  7001B
T55W1SentConfig       md 14:25:50 12212B  json absent
T55W1Simplifier       md 14:34:04 15358B  json 14:32:49  6712B
T55W1Revenger         — (wrote only /fast/scratch/.../gate-repro.sh; no wave-dir write at all)
T55W1CritC2           — (no write tool call in 171 events; still running at 17:37:12Z)
```

All of those post-C0 files are untracked at HEAD `c31cdd9` (`git status` `??`), and the wave dir
has grown from 1254 committed files at C0 to 2144 in the worktree while this audit ran. So:

- **at C0**: 12 of 75 have nothing; 63 of 75 have something; 57 of 75 have a report;
- **on disk now**: 10 of those 12 have delivered; `T55W1Revenger` and `T55W1CritC2` still have
  nothing (both still live), and `T55W1SentConfig` has a report but no `.json`.

Any statement of the form "N/75 seats delivered" is therefore *revision-bound*. The wave-1
self-audit (`T55W1RevWave.md`) does not state such a count (it audits the spec, not the yields),
so this is a property of the record, not a contradiction in it.

## 3. The `T55W1Er10` collision — the surviving artifacts are **not** the R54.10 draft

**Verdict: at C0 neither file is the R54.10 draft.** The JSON parses, but it is a different
seat's payload; the `.md` is a one-line redirect.

```
$ git cat-file -s / sha256 at 9cf0146   # receipts/er10-bytes.txt
  11908  a70ea19db384b077a731fe20a99501a2ef097685a79db84f1db0e1c224abf7a5  T55W1Er10.json
   1181  f32e53597d177968e772fe767f07e881cff3bbbf36d75755054b008fb8e06b9e  T55W1Er10.md
  11908  a70ea19db384b077a731fe20a99501a2ef097685a79db84f1db0e1c224abf7a5  T55W1ExecRekeyPrep.json
$ json probe: seat= T55W1ExecRekeyPrep | id= None | has old= False | 20 top keys (incl. _not_a_reader_report)
$ head -3 T55W1Er10.md:  "# T55W1Er10 — pointer" / "The item's report for this seat is filed at its seat path:" / "…T55W1ScribeMistakeSweep.md"
$ 1254-file scan for the restored bytes: 0 matches
```

- `T55W1Er10.json` is **byte-identical to `T55W1ExecRekeyPrep.json`** (occurrence 2 of the
  collision), i.e. the re-key prep payload, self-labelled `_not_a_reader_report`.
- `T55W1Er10.md` is **1181 B** and redirects to `T55W1ScribeMistakeSweep.md` — a *third*
  overwrite, by a fourth seat, that the wave-1 audit never saw.
- The restored draft (`3640 B / 2e15a640…` and `11366 B / 128c8e83…`) is **absent from every
  revision** — not at C0, not at HEAD; the R54.10 draft survives only as text inside
  `T55W1Er10-receipts/` (its counter runs) and as the title line quoted in
  `T55W1RevWave-receipts/collision*.txt` and `T55W1Rev08-receipts/derivations.stdout:62`.

**Write timeline** (`receipts/er10-write-timeline.txt`; UTC, C0 = 17:16:25Z) — 11 writes/edits
by four seats on the two paths:

```
16:50:15.645Z  T55W1Er10                write T55W1Er10.json     <- owner
16:50:53.050Z  T55W1Er10                write T55W1Er10.md       <- owner
16:51:08.181Z  T55W1ScribeNote          write T55W1Er10.md
16:51:08.212Z  T55W1Er10                edit  T55W1Er10.md
16:51:14.576Z  T55W1Er10                edit  T55W1Er10.md
16:52:30.438Z  T55W1ScribeSources       write T55W1Er10.md
16:52:34.857Z  T55W1ScribeNote          write T55W1Er10.md
16:55:20.478Z  T55W1ScribeNote          edit  T55W1Er10.md
16:56:23.945Z  T55W1ScribeSources       write T55W1Er10.md       <- the "restore"
17:01:39.605Z  T55W1ExecRekeyPrep       write T55W1Er10.json     <- occurrence 2 (survives at C0)
17:16:14.887Z  T55W1ScribeMistakeSweep  write T55W1Er10.md       <- occurrence 3 (survives at C0)
```

The last write lands **10.4 s before C0 is committed**, which is why C0 records the pointer.
The md path was overwritten seven times by four seats; the json path twice. (`T55W1ScribeSources`
also wrote the json once by `cp`/replay, which the tool-call log cannot see; that is the
13:56:04 local state the audit recorded.)

**Root cause is in the spec, not the seats** — six items instruct writing another seat's report
path (found independently, `spec` scan):

```
T55W1Er10.json <- T55W1Er10, T55W1ScribeCells, T55W1ScribeSources, T55W1ExecRekeyPrep
T55W1Er10.md   <- T55W1Er10, T55W1ScribeNote, T55W1ScribeCells, T55W1ScribeSources,
                  T55W1ScribeConsiderthese, T55W1ScribeMistakeSweep
```

Blast radius at C0: one seat lost both deliverables (`T55W1Er10`), one lost its `.md`
(`T55W1ScribeCells`, json-only at C0; it wrote `T55W1ScribeCells.md` at 14:30 post-C0 and its
`filename_note` self-documents the collision), and two consumers of the R54.10 draft
(`T55W1Rev05`, `T55W1Rev08`) signed verdicts against bytes that no revision carries.
`T55W1ScribeConsiderthese.md:333-336` is the only co-writer that refused to overwrite.

## 4. Claims whose files do not exist / do not contain the claim

**Sweep.** `sweep_claims.py` reads all 59 wave-1 `.md` files at C0, keeps every backticked token
on a line carrying a claim verb (`wrote|written|created|restored|landed|applied|produced|
appended|committed|generated|saved|staged`), normalises `:line`, `@rev`, brace expansion and
lane/fleet-absolute forms, and tests existence against the C0 tree, the lane worktree and the
fleet root. 921 tokens tested; **3 residues**, all benign:

| residue | adjudication |
|---|---|
| `T55W1Connector1:197` `…-receipts/01..09` | range shorthand for nine receipts that all exist (`01-`…`09-`) |
| `T55W1RevColdread:168` `.ufo/evidence/round-55/integrate/binder.py` | phrased as a recommendation ("the binder **must be landed** at a round-55 path (e.g. …)"); the file does not exist at C0 and is committed one commit later, at `c31cdd9` |
| `T55W1ScribeConsiderthese:262` `.ufo/evidence/round-56/quality/arm-census.py` | explicitly "the census tool (draft **for** …)", a future path |

A second sweep (`sweep_receipt_sections.py`, 612 tokens, 39 seats with a receipts/deliverables
section) found every own-receipt citation resolvable except one, below. **No report claims a
deliverable of its own that is missing at C0**, with the single exception of `T55W1ScribeCells.md`
(spec-collision victim, §3), and four seats wrote receipts with no report at all (§1).

**However, six claim/fact pairs are falsified at C0** (`receipts/claims-adjudication.txt`):

1. **`T55W1ScribeSources.md:224-232`** (quote at :229) (and `peer-er10-restore.txt:8-15`): "the restored files
   are `T55W1Er10.json` 3640 B sha256 `2e15a640…` and `T55W1Er10.md` 11366 B sha256 `128c8e83…`".
   Neither byte-string exists at C0 (0/1254). The restore was real at 13:58 but undone twice.
2. **`T55W1RevWave.md:240-248`**: "the `.md` (13:58:54, 11 366 B) still survives" — false at
   C0: 1181 B pointer. The audit's remediation ("leave both as they are") points at a file that
   no longer exists, and it undercounts the co-writers (it names six; a seventh,
   `T55W1ScribeMistakeSweep`, wrote last).
3. **`T55W1Rev08.md:197-202` and the "Stable across both instants (hashes I verified myself)"
   block at `T55W1Rev08.md:389-397`**: it certifies `2e15a640…`/`128c8e83…` as stable and derives its R54.10 "agree" from
   `T55W1Er10.json old[0]`. At C0 that file has no `old` key. The verdict is unsupported by the
   committed record (it was true for ~3 minutes).
4. **`T55W1Rev05.md:199`**: "`T55W1Er10.json` is the sources seat (S280/S281)" — at C0 it is the
   RekeyPrep payload; the sources payload survived only 13:56:04–13:58:54.
5. **`T55W1ScribeNote.md:159-161`**: "my writes sit only under … (`T55W1ScribeNote.md`,
   `T55W1Er10.md`, `T55W1ScribeNote-receipts/`)" — the writes happened (three tool calls,
   16:51–16:55); at C0 the path carries another seat's pointer, and the write itself was to
   another seat's report path.
6. **`T55W1ExecNoHarm.md:207`** cites `coldread-at-base.json` as its receipt: the file exists
   (3 022 874 B) but is **untracked at C0 and at HEAD** (`??`, not gitignored). A committed report
   cites an artifact no clone of the round can resolve.

## 5. Findings

**F1 (HIGH) — `T55W1Er10`'s deliverable is absent at C0 and two reviewer verdicts rest on it.**
Both artifacts at C0 belong to other seats (json = `T55W1ExecRekeyPrep.json` byte-identical;
md = 1181 B pointer to `T55W1ScribeMistakeSweep.md`). The R54.10 JSON the C1 corrections section
consumes is not in the tree; the restored bytes survive nowhere in git. `T55W1Rev05`'s and
`T55W1Rev08`'s R54.10 rows, and the wave audit's repair narrative, are stale or unresolvable at
the revision the round is built on. Receipt: `er10-bytes.txt`, `er10-write-timeline.txt`.

**F2 (MEDIUM) — the wave-1 audit's collision finding is stale by one overwrite, and its
remediation is wrong.** `T55W1RevWave.md` concludes no residual divergence and says both files
be left as they are; 10.4 s before the audited revision, a seventh co-writer replaced the `.md`
with a pointer. Fixing the six spec items (its prescription) does not restore `T55W1Er10`'s data —
that needs a second replay from `T55W1Er10.jsonl`, or the R54.10 row must be re-derived from its
receipts. Receipt: `claims-adjudication.txt` C2.

**F3 (MEDIUM) — C0 is a mid-flight snapshot, so any deliverable count is revision-bound.**
At C0 12/75 seats have nothing; within 22 minutes ten of them wrote reports (all untracked), and
the wave dir grew 1254 → 2144 files. Two seats (`T55W1Revenger`, `T55W1CritC2`) still have
nothing. A "wave-1 delivered 57/75" claim is true only at `9cf0146`. Receipt:
`post-c0-landing.txt`.

**F4 (MEDIUM) — a committed report cites a receipt no commit carries.** `T55W1ExecNoHarm.md:207`
→ `coldread-at-base.json` (3.0 MB) is untracked at C0 and HEAD. Either it belongs in the commit
policy or the report must say the receipt is worktree-only. Receipt: `claims-adjudication.txt` C7.

**F5 (LOW) — an undeclared write to another seat's path.** `T55W1ScribeMistakeSweep.md:7-9`
declares writing only its own `{md,json}` + receipts, yet its session records the
`T55W1Er10.md` write at 17:16:14.887Z that *is* the surviving pointer. No wave artifact
attributes that file, so a reader of the record cannot tell who wrote it. Receipt:
`er10-write-timeline.txt`.

**F6 (LOW) — dispatch provenance for the executing window is not preserved.** The only dispatch
ledger at C0 is `w1.ready.dispatched`, stamped `2026-10-28T14:16:09` (i.e. after the wave had
been running ~29 min) with all 75 keys and 21 respawn suffixes; the live `w1.ready.partial`
that `T55W1RevWave.md:50` cites ("60 seat→agent keys at 13:59:45") is gone from C0 and from the
worktree — only `w2.ready.partial`/`w3.ready.partial` remain. Seat→agent attribution for the
interval that produced the reports survives only in the session transcripts.

**F7 (INFO) — the four receipts-only seats are compliant on evidence, not on report.**
`T55W1ExecC2Full`, `T55W1ExecCensusAfter`, `T55W1ExecNote`, `T55W1MutC2` left populated receipt
dirs but no report file; the C2 landing they evidenced is therefore only reachable by reading
their directories (C2's landed claim is carried by the scribes' reports, not by these seats).

## 6. Residual risk and verification gaps

- **The collision cannot be closed from the record.** Nothing in git holds the R54.10 draft's
  bytes; only `T55W1Er10.jsonl` does. Every downstream R54.10 statement (SCORECARD corrections
  section, Rev05, Rev08, the wave audit) is a second-hand derivation.
- My counts are a snapshot: the wave was writing into `w1/` while I measured it (RevLedger's files
  changed between two of my reads, 14:35 → 14:38). The C0 numbers are reproducible from the
  revision; the worktree numbers are not.
- The claim sweep covers backticked tokens on claim-verb lines, not prose claims without a path,
  and not claims of *values* (that is C1/C2's axis, not mine). Absence of a residue is evidence
  about cited paths, not a proof that no claim is false.
- The write timeline comes from tool-call logs, so it misses bash-side writes (`cp`, replay
  scripts). The md path count (7 overwrites) is a floor, not a census.
- `w1.ready.partial` cannot be recovered, so F6 is stated from absence plus the audit's quote, not
  from a byte of the missing file.
