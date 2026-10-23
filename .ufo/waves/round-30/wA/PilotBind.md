# PilotBind — round-30 wave A, routed item 2/3 pilot

Seat `TameshiR30A2.PilotBind-7`. Question: is the attempt-1 draft
`.ufo/evidence/round-30/coldread/bind-select.py` fit to be frozen as the round-30 binding
check (QUALITY draft criterion 60, "a binding check runs on real assembled entries before it
is frozen")?

## Verdict

**Not fit to freeze.** The draft runs cleanly and is deterministic, but it is unsound in two
independent ways and it **silently loses 4 of the 32 real round-29 entries** — the exact defect
shape (assembler/registry shape mismatch, not evidence failure) that criterion 60 was written to
prevent. The 4 losses are recoverable: a one-line label normalisation keeps 32/32.

Three defects are load-bearing; the rest are secondary. All are falsified by measurement below,
not by reading.

| # | Defect | Where | Severity |
|---|---|---|---|
| D1 | Report path resolved **relative to the cwd** | `bind-select.py:40,56,62` | high — total silent loss from a wrong cwd |
| D2 | `COLDREAD <seat>:` transcript check is **satisfied by the seat's own prompt** | `bind-select.py:83` | high — the check cannot distinguish work from a received prompt |
| D3 | **No seat-label normalisation**: 4 genuinely bound entries excluded | `bind-select.py:52,56,70,77` | high — 4/32 coverage loss; criterion-60 target defect |
| D4 | The report is read from `registry.reportDir`, **not from the entry's own `reports`** | `bind-select.py:56-62` | medium — a substituted file can satisfy the binding |
| D5 | `agent_id` is **always null** in the receipt | `bind-select.py:88` + registry | medium — criterion 60's "names … its agent id" is unmet |
| D6 | Exit 0 and a plausible receipt when **everything** is excluded, or when `--sessions` does not exist | `bind-select.py:104` | medium — failure looks like success |
| D7 | Transcript naming is `<prefix><seat>.jsonl`; round-30 wA transcripts are `<seat>-<N>.jsonl` under a subdir | `bind-select.py:77` | high for round-30 reuse — 0/32 found |

## What ran (exact commands, observed output)

Seat clone at `/fast/scratch/hyaku/tameshi-r30a2-seats/PilotBind-7/clone` (clone of
`/home/vgpnk/Projects/shokunin/tameshi-shokunin` at `f09d342`), cwd = clone root, `GIT_DIR`/
`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset. Round-29 inputs in the clone are byte-identical to the
lane tree (verified: 50/50 files under `.ufo/waves/round-29/w1` equal by sha256;
`assembled-w1.json` sha256 `0ef402815708ca2233e6c52f36674345e8d98cc63c1ff2a2da4fef2213ad2731`
in both).

The assignment's `--sessions` path was correct as given; the round-29 transcripts do not sit
elsewhere. They are at
`~/.omp/agent/sessions/-Projects-shokunin/2026-10-23T00-54-50-959Z_01a16640-e34f-76e4-8a3b-4d245a8bb241/TameshiR29/TameshiR29.<seat>.jsonl`
(65 `.jsonl`, 36 of them `Read*`).

```
$ cd /fast/scratch/hyaku/tameshi-r30a2-seats/PilotBind-7/clone
$ timeout 300 python3 .ufo/evidence/round-30/coldread/bind-select.py \
    --assembled .ufo/evidence/round-29/coldread/assembled-w1.json \
    --registry .ufo/waves/round-29/w1/swarm-registry.json \
    --sessions ~/.omp/agent/sessions/-Projects-shokunin/2026-10-23T00-54-50-959Z_01a16640-e34f-76e4-8a3b-4d245a8bb241/TameshiR29 \
    --prefix TameshiR29. \
    --out /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/wA/pilot-bound.json \
    --receipt /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-30/wA/pilot-receipt.json
{"assembled": 32, "kept": 28, "excluded": 4, "excluded_verdicts": ["gap-minor", "verified-record"]}
exit=0
```

Artifacts written (the files my item names, under `.ufo/evidence/round-30/wA/`):

| file | sha256 |
|---|---|
| `pilot-bound.json` | `2ddf9d4e98fec344e1d51479713315b15c5b0e3d944dfd41358e7506f81316a4` |
| `pilot-receipt.json` | `d319bf79dbc811fea81a5be9b4006c4394ae05e0f5d9bf6e05dc3ceb014f0b03` |

Determinism: a second run to `/tmp` produced byte-identical `pilot-receipt.json`
(`d319bf79…` both). The receipt also equals, byte for byte, the pre-existing
`.ufo/evidence/round-30/coldread/pilot-r29-bind-receipt.json` (`d319bf79…`, written 02:16), so
this run independently reproduces the earlier pilot.

## Kept / excluded

32 assembled entries, 49 registry members, **28 kept / 4 excluded**, 30 bindings over 28 kept
entries (2 entries carry two seats). Kept verdicts: `executed-ok` 9, `gap-minor` 15,
`verified-record` 4. No failing verdict was dropped — the excluded set is
`verified-record` ×3 + `gap-minor` ×1.

**Excluded, all four for the same reason** (`seat-not-registry-member`):

| start | verdict | entry seat label | registry key present | report the entry names | transcript present |
|---|---|---|---|---|---|
| 1609 | verified-record | `TameshiR29.Read08A` | `Read08A` | `.ufo/waves/round-29/w1/Read08A.md` | `TameshiR29.Read08A.jsonl` |
| 1609 | verified-record | `TameshiR29.Read08B` | `Read08B` | `.ufo/waves/round-29/w1/Read08B.md` | `TameshiR29.Read08B.jsonl` |
| 1938 | verified-record | `TameshiR29.Read11B` | `Read11B` | `.ufo/waves/round-29/w1/Read11B.md` | `TameshiR29.Read11B.jsonl` |
| 1964 | gap-minor | `TameshiR29.Read12B` | `Read12B` | `.ufo/waves/round-29/w1/Read12B.md` | `TameshiR29.Read12B.jsonl` |

These are **false exclusions, not bad evidence** (D3). Measured per entry:

```
entry_start 1609 seat TameshiR29.Read08A
   registry_has_short_name True | registry_has_full_label False
   report_exists True | json_block_binds True | block seat field TameshiR29.Read08A
     | section verdict verified-record | entry verdict verified-record
   transcript_exists True | has COLDREAD Read08A: True | sha256 1b57ff4843493267
… identical shape for Read08B (3c1e9ca064c7607f), Read11B (68c5b61c4210a430),
  Read12B (1e176632b0df3e55, entry verdict gap-minor vs section verdict verified-record)
```

The seat names itself `TameshiR29.Read08A` in its report's json block; the wave registry keys
are bare (`Read08A`). `members.get(seat)` misses, so the entry is dropped before the report is
even opened. This is round-29 Mistake 5 repeating in a new place: the check is keyed on a label
form the assembler emits, not on the evidence.

**Relative to the frozen round-29 selection.** Both kept-start sets are the same 12 starts
(starts repeat across entries). At entry level the draft keeps **6 entries the round-29 frozen
`select-bound.py` dropped** and drops **0 it kept**:

```
r29 frozen: kept 22 excluded 10    draft: kept 28 excluded 4
r29-only-excluded, now kept: start 375, 1517, 1548, 1563, 1814, 1964
```

Those 6 are the assembler-normalised-verdict entries (entry `gap-minor`, report section
`executed-ok`). The draft drops the verdict comparison on purpose (`bind-select.py:12-14`,
round-29 Mistake 5) — correct, and the reason the two kept sets differ. The 4 seat-label
exclusions are a separate, unintentional loss.

## Three kept bindings checked by hand

Requirement: transcript exists, sha256 matches, contains `COLDREAD <seat>:`. All three hold —
**but see D2: "contains" is trivially true and is not evidence of work.**

```
Read01A exists True bytes 471202 receipt_bytes 471202 sha_match True
        coldread_present True  report_exists True   sha256 f9d0b939d6f6b22f…
Read06A exists True bytes 427071 receipt_bytes 427071 sha_match True
        coldread_present True  report_exists True   sha256 6c0f7047bfd5ec7f…
Read10C exists True bytes 832725 receipt_bytes 832725 sha_match True
        coldread_present True  report_exists True   sha256 6128ddef2bb05bb9…
```

A second, stronger hand-check (assistant-authored only — see the correction) passes for all
three and for all 36 `Read*` seats:

```
Read01A prompt-echo hits [6, 10, 67]  assistant-authored hits [7, 12, 103, 106]
Read06A prompt-echo hits [6, 10, 65]  assistant-authored hits [7, 12, 70, 79, 81, 84, 88]
Read10C prompt-echo hits [6, 10, 152] assistant-authored hits [7, 12, 250, 261, 262, 267, 274]
```

## Defects, falsified

### D1 — report path resolved relative to the cwd (`bind-select.py:40,56,62`)

`report_dir = reg.get('reportDir', …)` is `.ufo/waves/round-29/w1`, a **relative** path, and
`open(rp)` (`:62`) resolves it against the process cwd. Nothing records or checks the root.

```
$ cd /tmp && python3 <clone>/.ufo/evidence/round-30/coldread/bind-select.py \
    --assembled <abs>/assembled-w1.json --registry <abs>/swarm-registry.json \
    --sessions <abs>/TameshiR29 --prefix TameshiR29. --out /tmp/x.json --receipt /tmp/xr.json
{"assembled": 32, "kept": 0, "excluded": 32, "excluded_verdicts": ["executed-ok", "gap-minor", "verified-record"]}
exit=0
reason histogram: {'report-block-unbound': 30, 'seat-not-registry-member': 4}
```

Same inputs, same script, different cwd → 28 kept becomes 0 kept, and the run still exits 0 with
a plausible receipt. Note the misleading label: a report that could not be **opened** is reported
as `report-block-unbound` (`:63` swallows `OSError` into `text = ''`), not as "report missing".

### D2 — the `COLDREAD <seat>:` check is satisfied by the prompt (`bind-select.py:83`)

The check is `('COLDREAD %s:' % seat).encode() not in raw`, a whole-file byte substring. The
seat's own task prompt contains that literal string as the instruction
("Last line exactly `COLDREAD Read01A: <verdict>`"), and the prompt is stored verbatim in the
transcript (`session_init.task`, plus the echoed user message).

Falsifier: I built 36 transcripts containing **only** the first record carrying that string —
i.e. the prompt, with every scrap of seat work removed — and re-ran the draft unmodified:

```
$ python3 … build prompt-only transcripts into /fast/scratch/…/PilotBind-7/fake-sessions
fabricated prompt-only transcripts: 36
$ python3 bind-select.py … --sessions /fast/scratch/…/PilotBind-7/fake-sessions --prefix TameshiR29. …
{"assembled": 32, "kept": 28, "excluded": 4, "excluded_verdicts": ["gap-minor", "verified-record"]}
```

Identical result to the real run (28/4). The check has **zero discriminating power**: a seat that
received its prompt and did nothing passes it. (Sanity control: control seats that got a different
prompt — `CtlC1Shortcut`, `CtlC2Shortcut`, `BuildF6A`, `CriticC1Design`, `CtlC1Cheap` — do not
contain the string, so the check is not universally vacuous, only vacuous for exactly the seats it
guards.) The docstring (`:16`) also claims the check reads the seat's **final line**; the code never
checks finality, and the real transcript's last record is a `session_exit` custom record, not the
`COLDREAD` line.

### D3 — no seat-label normalisation (`bind-select.py:52,56,70,77`)

`members.get(seat)`, `'%s/%s.md' % (report_dir, seat)`, `d.get('seat') == seat` and
`'%s%s.jsonl' % (prefix, seat)` all use the raw entry label. For `TameshiR29.Read08A` the draft
would build `.../TameshiR29.Read08A.md` and `TameshiR29.TameshiR29.Read08A.jsonl` — neither
exists; the real files are `Read08A.md` and `TameshiR29.Read08A.jsonl`.

Falsifier: a variant with **only** the label normalised (`seat.split('.')[-1]` at all four points,
nothing else changed) keeps everything:

```
{"assembled": 32, "kept": 32, "excluded": 0, "excluded_verdicts": []}
34 bindings over 32 entries; receipt sha256 2f03233b719caf8051ad9c7d8d32cfdbfa281126639b7b7194529ea73493d054
```

So the 4 exclusions are purely syntactic, and the 28 result understates coverage by 4.

### D4 — the report read is not the report the entry names (`bind-select.py:56-62`)

`rp` is derived from `registry.reportDir` + seat; the entry's own `reports` list is used only for
a name test (`:57`). With the registry's `reportDir` pointed at a copy of the tree,
`/tmp/decoy2`:

```
{"assembled": 32, "kept": 1, "excluded": 31, …}
receipt report field : /tmp/decoy2/Read01A.md
entry named reports  : ['.ufo/waves/round-29/w1/Read01A.md']
receipt report is one the entry named? False
```

A binding can therefore be satisfied by a file the entry never named, and the receipt records a
path the entry does not own. Symmetrically, with `reportDir` pointed at a directory holding a
same-named report **with the json block stripped**, all 32 are excluded
(`kept 0, excluded 32`) even though every entry's named report is intact and bound. On the
round-29 data the two paths coincide, so this is latent rather than corrupting here — but it is
unsound for a check whose stated purpose is "binding to an artifact outside the report".

### D5 — `agent_id` is always null (`bind-select.py:88`)

`m.get('agentId')` reads the registry, where `agentId` is `None` for **all 49** round-29 members
and **all 32** round-30 wA members:

```
agentId values: Counter({'None': 49})      # round-29 w1
agentId values: Counter({'None': 32})      # round-30 wA
all agent_id null: True                    # over all 30 bindings in the receipt
```

Criterion 60 asks the receipt to name "the registry member, **its agent id** and its host session
transcript path with sha256". The transcript does carry a distinct agent identity — the
`session_init` record's `id`, 36 distinct values for 36 `Read*` seats (`Read01A` → `f2523f4e`) —
but the script never reads it. So the receipt cannot answer "which agent" without a session
search, which is the thing criterion 60 exists to avoid.

### D6 — total exclusion and a missing session store both exit 0 (`bind-select.py:104`)

```
# everything excluded (wrong cwd / wrong reportDir)
… {"assembled": 32, "kept": 0, "excluded": 32} exit=0
# --sessions /nonexistent/dir
… {"assembled": 32, "kept": 0, "excluded": 32, …} exit=0
```

No assertion that `kept > 0`, no check that `--sessions` exists. A broken invocation is
indistinguishable from a wave whose evidence failed.

### D7 — round-30 transcript naming does not match (`bind-select.py:77`)

The script builds `<sessions>/<prefix><seat>.jsonl`. Round-30 attempt-2 transcripts live at
`<sessions>/TameshiR30A2/TameshiR30A2.<seat>-<N>.jsonl` (per-seat numeric suffix, e.g.
`TameshiR30A2.PilotBind-7.jsonl`, `TameshiR30A2.CtlS1Normalize-11.jsonl`):

```
wA members 32  script-built transcript path found 0  missing 32
every actual seat file carries a -N suffix: True
```

Run as written against the round-30 wA registry, the draft binds nothing. This is a blocker for
adopting the draft as the round-30 check, independent of D1-D3.

### Docstring vs code

`:14-16` says an entry is bound when "the host session store holds the seat's transcript
`<DIR>/<PREFIX><seat>.jsonl` … and that transcript contains the seat's **final line**
`COLDREAD <seat>:`". Implemented (`:77,83`): a flat filename join and a whole-file substring —
no finality, no authorship, no distinction between prompt echo and seat output.

## Smallest safe correction

Ordered by severity; each is small and independently testable against the round-29 data.

1. **D3 (do this first — it changes a result from 28 to 32).** Normalise the label once, at the
   top of the seat loop: `norm = seat.split('.')[-1]`, then use `norm` for the registry lookup
   (`:52`), the report path (`:56`), the block seat test (`:70`, accept `seat` or `norm`) and the
   transcript path (`:77`). Measured: kept 32 / excluded 0.
2. **D1.** Take an explicit `--repo` root (default cwd, recorded in the receipt) and build
   `rp = os.path.join(a.repo, report_dir, norm + '.md')`. Report a **missing/unreadable** report
   as its own reason instead of folding `OSError` into `report-block-unbound`.
3. **D2.** Replace the substring test with a parse: load the `.jsonl`, and require the needle in
   an **assistant-authored** message — `type == "message"`, `message.role == "assistant"`, content
   of type `text` or `toolCall` arguments. Measured on the round-29 store: real transcripts
   36/36 pass; prompt-only fabricated transcripts 0/36 pass. (Do not implement "final assistant
   text message ends with the line": 9 of 36 real seats put it only in the report-write tool-call
   argument, so that stricter form false-negatives 9 real seats.)
4. **D4.** Read the report from the entry's own `reports` list, not from `registry.reportDir`;
   if the registry's `reportDir` disagrees with what the entries name, fail loudly.
5. **D5.** When `registry.agentId` is null, record the transcript's `session_init.id` as
   `agent_id`, and record both the raw entry seat label and the normalised registry key.
6. **D6.** Exit non-zero when `kept == 0`, and when `--sessions` is not a directory.
7. **D7.** Accept a transcript path template (`--transcript-template
   '{sessions}/TameshiR30A2/TameshiR30A2.{seat}-*.jsonl'`) or a glob fallback, so one script
   serves both naming conventions; record the resolved path in the receipt either way.

Not defects, recorded so they are not "fixed" later:

- **Verdict is deliberately not compared** (`:12-14`). The assembler normalises verdicts
  (round-29 Mistake 5); the draft's 6 extra kept entries versus the frozen round-29 predicate are
  the intended consequence and are all `gap-minor` entries whose report section says `executed-ok`.
- **The binding check is syntactic** — it cannot tell a seat-written report from a forged one.
  Unchanged by this pilot; the round-29 contract already bounds this claim, and the closure checks
  transcripts outside the counter.

## Risks

- **Coverage: 4/32 entries uncredited** under the draft as written (D3). Exclusion cannot raise a
  pass count, but 12.5% of the wave's real reads is a material calibration loss and is exactly
  the falsifier shape named in criterion 60.
- **The transcript leg is currently decorative** (D2). Freezing it gives a receipt whose
  `transcript_sha256` proves a file existed, not that the seat did the work. A forged transcript
  containing only the prompt yields a byte-identical receipt.
- **D1 makes a wrong-cwd run indistinguishable from a failed wave** (exit 0, plausible JSON).
  Combined with D6, an automated driver that runs the script from any directory other than the
  repo root will report a clean miss.
- **D5 leaves criterion 60's "its agent id" unmet** in both registries as they stand.
- Round-29 data exercises only the happy path for D4 (registry `reportDir` and entry `reports`
  agree), so D4 is latent here and would bite only on a future shape change.

## Blockers

None for this pilot. D7 is a blocker for reusing the draft unmodified on the round-30 wA
registry (0/32 transcripts resolve); the correction above is mechanical.

## Bounds compliance

- Wrote only this report and the two artifacts my item names:
  `.ufo/evidence/round-30/wA/pilot-bound.json`, `.ufo/evidence/round-30/wA/pilot-receipt.json`.
- All code ran inside my own clone
  `/fast/scratch/hyaku/tameshi-r30a2-seats/PilotBind-7/clone` with `GIT_DIR`, `GIT_WORK_TREE`,
  `GIT_INDEX_FILE` unset; every long run wrapped in `timeout 300`.
- No git write commands in `/home/vgpnk/Projects/shokunin/tameshi-shokunin` or
  `/home/vgpnk/Projects/shokunin`; no `jj` command anywhere; read-only git used only with
  `GIT_OPTIONAL_LOCKS=0`.
- Nothing under `/fast/scratch/hyaku/tameshi-r30a2` was opened, listed or searched.
- No subagent spawned (the single labrat allowance was not needed — the probes are deterministic
  and were run in-process). No process started by me remains; a post-run scan of
  `/proc/*/cmdline` for `bind-select|probe-*` returned nothing.
- No tool installs or upgrades; no pacman transactions.
