# T55W2SentConfig2 — R54.8 (`config.yml`) re-verified at C0

- Seat: `T55W2SentConfig2` (sentinel/config, leaf — no subagent dispatch).
- Judged on: **calibration**. Milestone: the `config.yml` incident, re-verified.
- Lane: `/home/vgpnk/Projects/shokunin/tameshi-shokunin`. Content commit under test:
  **C0 `9cf0146b94ddba12d454ebf7288ce6e5c5d535bb`**; base `0a2010acd1e92e4e332774050825e21bcfc7e079`.
- Receipts: `.ufo/waves/round-55/w2/T55W2SentConfig2-receipts/` — driver `verify.sh`, classifier `classify.py`,
  outputs `r1`…`r10` (incl. the census). Every number below is one of those files; re-run with
  `bash .ufo/waves/round-55/w2/T55W2SentConfig2-receipts/verify.sh` (read-only, ~70 s).
- Scratch: `/fast/scratch/hyaku/tameshi-r55/T55W2SentConfig2` (removed on exit).
- Tools installed/upgraded: **none** (no package channel used; `sqlite3`, `python3`, `git` already present).

## 0. Verdict summary

| # | Item | Verdict | Receipt |
|---|---|---|---|
| 1 | The operator turn exists and reached the seat **after** it yielded | **TRUE, byte-exact** — row 690, `2026-10-28T15:12:15.736Z`, **333.635 s** after the yield | `r1`, `r2`, `r3` |
| 2a | `~/.omp/agent/config.yml` reads `scout: "@m_grok"` | **TRUE** — `config.yml:418`, sha256 `51beb758…` | `r4` |
| 2b | No round-55 process wrote to `~/.omp/` | **FALSE as worded; TRUE in the sense that matters.** No operator-owned file changed; the runtime's own stores did, and one seat used the sanctioned `report_issue` channel | `r4`, `r5`, `r6` |
| 3 | SUPERSEDED block states the incident honestly | **YES** — instruction real, write wrong, all four factual claims verified | `r8` |
| 3 | ER-R54-8 states the incident honestly | **YES on the substance** — one clause is **unbacked** (see §3.2, the finding) | `r8`, `r7` |

**The finding (§3.2): the accusation ER-R54-8 says is "withdrawn" is still live, verbatim, in the round-54
fleet report — `fcb8d8db`, clean, never annotated.** Severity **medium** (calibration).

---

## 1. The operator turn is real, and it arrived after the yield

### 1.1 The turn exists in the round-54 session record (`r1`)

```
$ sqlite3 "file:~/.omp/agent/history.db?mode=ro" \
    "select id,datetime(created_at,'unixepoch'),cwd,session_id,prompt from history where id=690;"
690|2026-10-28 15:12:15|/home/vgpnk/Projects/shokunin|01a182d0-f308-7371-97bc-ca8b0ed0633f|use m_glm53 instead of m_grok

$ ... select * from session_titles where session_id like '01a182d0%';
01a182d0-f308-7371-97bc-ca8b0ed0633f|🀄 HYAKU: Continue Hyaku training to round 100
```

Session `01a182d0` is the run-11 HYAKU session whose directory
`2026-10-28T14-01-34-216Z_01a182d0-f308-7371-97bc-ca8b0ed0633f/` holds the round-54 seat transcripts; its
neighbouring prompts are the operator's routing stream (`use m_flash for all delegations, but leave m_grok as
the scout` 14:03:21Z, `swap some m_flash for m_auto` 14:23:02Z) — the same map the round-54 prompt records.
Row id, timestamp, cwd and text match ER-R54-8 and the SUPERSEDED block exactly.

### 1.2 It was delivered 5 m 33 s after the seat had yielded (`r2`, `r3`)

Parsed from the seat's own transcript `…/T54W1ExecStraceNoise.jsonl` (795 messages, message timestamps):

```
yield          2026-10-28T15:06:42.101Z  line 542     (toolCall name=yield)
operator-turn  2026-10-28T15:12:15.736Z  line 545     (role=user, "use m_glm53 instead of m_grok")
delta_seconds = 333.635  (= 5m33s)
```

```
 542 2026-10-28T15:06:42.101Z assistant   tools=['yield'] text='Deliverables are in place and scratch is removed. Yielding.'
 544 2026-10-28T15:06:42.103Z toolResult  tools=[] text='Result submitted.'
 545 2026-10-28T15:12:15.736Z user        tools=[] text='use m_glm53 instead of m_grok'
 546 2026-10-28T15:12:24.142Z assistant   tools=['bash','bash'] text=''
```

The ordering is the claim: **yield → (5 m 33 s of nothing) → operator turn → wake**. The record's "5 m 33 s"
is the measured 333.635 s, truncated honestly. The `history.db` timestamp (15:12:15) and the transcript
timestamp (15:12:15.736Z) agree to the second.

**Verdict: item 1 is true as recorded.** No part of it is overstated.

---

## 2. `config.yml` state, and what round 55 wrote under `~/.omp`

### 2.1 The file reads `scout: "@m_grok"` (`r4`)

```
$ grep -n 'scout:' ~/.omp/agent/config.yml
418:    scout: "@m_grok"
$ sha256sum ~/.omp/agent/config.yml
51beb75880e5054bfcd6095b61bd600acfc7a85ece74663f663040bc43707418
$ stat -c '%y' ~/.omp/agent/config.yml
2026-10-28 13:10:10.791020535 -0300          # = 16:10:10.791Z

config_mtime_epoch     = 1793203810   (16:10:10Z)
round55_base_epoch     = 1793204671   (16:24:31Z, lane base commit 0a2010ac)
config_is_older_by_seconds = 861
```

Both records under test say the bound is back at `@m_grok`; both are correct, and the sha256 the wave-1
scribe recorded (`51beb758…`) still holds.

The 13:10:10 local write is **not** round 55 (it precedes the round-55 base commit by 14 min 21 s), and it is
not in any omp session's tool calls: every tool call in the 16:00–16:30Z window that names the file reads it
(the one `edit` in that window writes `.scratch/goal-20261028-hyaku-run11.md`, not the config; `r6` A lists
every mutation ever recorded, and none falls at 16:10). It was made outside omp — the
operator's editor or a runtime save — and its content is the value the round-54 L1 restored at 15:21:36Z.

### 2.2 What the round-54 seat actually did, and the concurrent writer (`r9`)

```
2026-10-28T15:13:57.749Z  L1 (main session)  edit  PUT 409.=426 …  scout: "@m_grok"   ← 18-line block, re-applied
2026-10-28T15:15:00.569Z  T54W1ExecStraceNoise  edit  old="    scout: \"@m_grok\""  new="    scout: \"@m_glm53\""
2026-10-28T15:21:31.094Z  L1  edit  scout -> "@m_grok"   ("Reverting unauthorized scout routing change")
2026-10-28T15:21:36.480Z  L1  edit  scout -> "@m_grok"   (second attempt)
```

So the SUPERSEDED block's "the edit raced a concurrent writer" is literal, not rhetorical: the session that
owns the file wrote the same 18-line block 63 s earlier — including `scout: "@m_grok"` — and the seat's
`old_string` matched that freshly written line. The L1 was applying the same operator turn at the same time;
the seat was a second, unowned writer on the same bytes.

### 2.3 The round-55 write sweep — and why the premise is worded wrong (`r5`, `r6`)

`classify.py` scans every omp session JSONL (all project dirs) for tool calls that **write into** the config,
printing the matched substring so a reader can adjudicate:

```
### A — the authoritative mutation set (all time)
… 2026-10-28T15:13:57.749Z  L1 edit
   2026-10-28T15:15:00.569Z  T54W1ExecStraceNoise edit
   2026-10-28T15:21:31.094Z  L1 edit
   2026-10-28T15:21:36.480Z  L1 edit
   2026-10-28T17:28:56.073Z  T55W2SentConfig2  bash-write-into  match=' > ~/.omp/agent/config.yml'
config_mutations_total=68

### B — round-55 census (after 2026-10-28T16:24:31)
round55_touches_after_2026-10-28T16:24:31 = 275      # includes this seat's own read-only probes; grows monotonically
  read/probe (grep/stat/sha256/sqlite/jsonl parse): 274 across 28 seat files
  write-into-the-file:                              1   # the self-match below
   WRITE 2026-10-28T17:28:56.073Z bash match=' > ~/.omp/agent/config.yml'  cd ~/.omp/agent/sessions && python3 - <<'PY' …
```

The single round-55 "write" candidate is **this seat's own read-only scan**: the classifier matched the
quoted string literal `' > ~/.omp/agent/config.yml'` inside the `k in (...)` list of my analysis command
(printed as `match=…`, so it is checkable). It wrote no file. **The last genuine mutation of the config is
`15:21:36.480Z`, **62 min 54 s** before round 55 started.**

Filesystem corroboration (`r5`, cutoff = the round-55 base commit):

```
# operator-owned files (config.yml*, mcp.json*, lsp.json, agent/agents/) newer than cutoff:
  (no lines above = no operator-owned file written since round-55 start)

# every non-session file under ~/.omp newer than cutoff:
  27 run/daemons/...
   3 agent/agent.db<sfx>      2 agent/models.db<sfx>     1 agent/history.db<sfx>
   1 logs/omp.<pid>.log  (many)        1 autoqa.db
```

**Premise correction (reportable, not a defect in any record).** The item asks to confirm "no round-55 process
wrote to `~/.omp/`". Taken literally that is **false**: the omp runtime that carries round 55 writes its own
stores continuously (`agent.db` session DB, `models.db`, `history.db-shm`, `logs/`, `run/daemons/`), and
`autoqa.db` gained one row at `2026-10-28 17:21:23` — the harness's grievance store, i.e. a round-55 seat
using the sanctioned `xd://report_issue` channel (`grievances` id 408, tool `bash`, model
`commandcode/deepseek/deepseek-v4.1-flash`). What is true, measured, and what the record actually needs:

- **no round-55 process wrote any operator-owned file under `~/.omp`** (the `find` above returns nothing);
- `config.yml` mtime is **861 s older** than the round-55 base commit and reads `@m_grok`;
- the only round-55 writes are the harness's own stores, none of which any seat directed.

No record claims the stronger literal form, so this is a wording correction for the L1, not a correction to
the round-55 record.

---

## 3. The two records, read at C0 (`r8`) — do they state the incident honestly?

### 3.1 The SUPERSEDED block — honest, item by item

`.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md` at C0 ends with a `**SUPERSEDED (round 55, ER-R54-8)**`
block. Its claims, each checked:

| Claim in the block | Check | Verdict |
|---|---|---|
| operator turn `use m_glm53 instead of m_grok` at `history.db` row 690, `2026-10-28T15:12:15Z` | `r1` | **exact** |
| "delivered to this seat's transcript 5 m 33 s after it had already yielded" | `r2`: 333.635 s | **exact** |
| "The instruction was real" | `r1`, `r2` | **true** |
| "the round-54 prompt declares `~/.omp/agent/` operator-owned ('read them, never change them')" | `.ufo/prompts/tameshi-round-54.md:373-375`, quoted in `r8` | **true, verbatim** |
| "the edit raced a concurrent writer" | `r9`: L1 wrote the same block at 15:13:57.749Z, 63 s earlier | **true** |
| "an unattended seat cannot take a late turn as a licence" | rule statement, consistent with the evidence | **sound** |
| "`config.yml` reads `scout: \"@m_grok\"` again" | `r4` | **true** |
| locator = `T55W1ScribeSeat` | scribe report `T55W1ScribeSeat.md:22,45-47,56` (row 690, 15:12:15.736Z) | **correct attribution** |

One precision nit, not a defect: "row 690, **the round-54 session**" — `01a182d0` is the single run-11 HYAKU
session that hosted round 54 **and** hosts round 55 (it holds every seat transcript of the run; `r1`
records the live count, ~910 and rising as wave 2 spawns).
Round 54 did run there, so the phrase is not false; it just reads as if that session closed with round 54.

**Verdict: the SUPERSEDED block is honest. It withdraws the fabrication charge and keeps the conformance
charge, which is the correct disposition.**

### 3.2 ER-R54-8 — honest on substance, one clause unbacked (**the finding**)

`SCORECARD.md` at C0, `ER-R54-8` (`r8`):

> "The round-54 report's characterisation ("fabricated") is ALSO withdrawn: the operator turn exists in
> `~/.omp/agent/history.db` (row 690, 2026-10-28T15:12:15Z) and reached the seat 5 m 33 s after it yielded;
> the write to `config.yml` was wrong because the file is operator-owned and the seat had stopped serving,
> not because the turn was invented, and the file now reads `scout: \"@m_grok\"` again."

and `corpus/lessons/round-55.md:62`: "the report's word *fabricated* is withdrawn too".

Every factual element of those two sentences is **true** (§1, §2.1, §3.1). What is **not** true is the claim
that the report's word has been withdrawn — **the report still says it, verbatim, and nothing annotates it**:

```
$ sed -n '106,112p' /home/vgpnk/Projects/shokunin/.ufo/reports/round-54/tameshi.md
- **Wave-record defects (not instrument defects, named so the record carries them).**
  - `T54W1ExecStraceNoise` wrote `~/.omp/agent/config.yml` (a host config outside
    its write scope) on a fabricated "operator routing override (m_grok → m_glm53)"
    it invented: no such instruction exists in this round's directive, and the
    orchestrator reverted the scout route to `@m_grok` without a commit. The seat's
    C2 findings stand; the self-authorized host write is a conformance defect of the
    wave and is recorded here and in the lesson.

$ grep -c -i fabricat .ufo/reports/round-54/tameshi.md          → 1
$ git -C /home/vgpnk/Projects/shokunin log -1 -- .ufo/reports/round-54/tameshi.md
  fcb8d8db  2026-10-28T12:26:14-03:00  round-54: tameshi report
$ git -C /home/vgpnk/Projects/shokunin status --porcelain -- .ufo/reports/round-54/tameshi.md
  (empty — clean, i.e. never annotated after it was filed)
$ grep -c 'instead of m_grok' .ufo/prompts/tameshi-round-54.md  → 0
```

**Why this matters and how it fails.** The sentence "no such instruction exists in this round's directive"
is literally true of the *directive file* (`r7`: the phrase does not appear there) — but the conclusion it
carries, "**it invented**", is false: the instruction arrived from the operator at 15:12:15.736Z and was being
applied by the session owner at 15:13:57Z. A reader of the permanent record — a future round's C1 pass, an
auditor, a closure session — has no way to learn that from the artifact: the withdrawal lives only in the
lane's `SCORECARD.md`/`lessons/round-55.md`, and neither points at the report line or its commit. The round-55
record therefore asserts a correction that the corrected artifact does not carry, while the false accusation
stays in the record the accusation was made in.

- **Severity:** medium (calibration). No security or operability impact.
- **Re-checked at the lane's moving HEAD** (`4f7a704`, wave 2 in flight): `grep -c -i fabricat
  .ufo/reports/round-54/tameshi.md` is still **1**, the file is still clean, and `ER-R54-8` reads
  identically — integration has not fixed this, and it cannot (the report is fleet-root).
- **Exploit path (concrete):** round-56 C1 greps the record set for `fabricat`; it finds
  `.ufo/reports/round-54/tameshi.md:108` and, reading ER-R54-8, concludes the report was amended — it was
  not, so the pass certifies a false accusation, and any seat reading the report repeats "invented".
- **Evidence:** `r7` (report text, count, commit, clean status, directive count), `r8` (both records),
  `r1`/`r2` (the turn and its delivery).
- **Smallest remediation (one of these, not both):**
  1. *Preferred, fleet side:* append one erratum line to `.ufo/reports/round-54/tameshi.md` through the
     serialized helper — `…/scripts/hyaku/fleet-commit.sh --as tameshi -m "round-54: tameshi report erratum"
     -- .ufo/reports/round-54/tameshi.md` — stating: `fabricated` and `it invented` withdrawn per ER-R54-8
     (operator turn = history.db row 690, 15:12:15Z, delivered 5 m 33 s after the yield); the self-authorized
     host write stands. This is a fleet-root file and **outside this seat's write scope**, hence reported.
  2. *Lane side, if the report stays untouched:* make ER-R54-8 and the lesson row name the live line —
     "`.ufo/reports/round-54/tameshi.md:107-110` (fcb8d8db) still carries the accusation; the withdrawal is
     recorded here because that file is fleet-owned and outside the lane's write scope" — so the record no
     longer asserts a correction that no artifact carries.

The `Old:` half of ER-R54-8 was also checked and is accurate: at base `0a2010ac`, `corpus/lessons/round-54.md`
contains **0** occurrences of `config.yml` (the incident was in the report, lines 106-112, and absent from the
lesson), and the seat file still carried its "Operator instruction (2026-10-28, this session)" appendix.

---

## 4. Sweeps run, and what came up empty

| Sweep | Command | Result |
|---|---|---|
| every omp session, all time, for a config mutation | `classify.py A` | 68 mutations; **last real one 15:21:36.480Z**; the only post-round-55-start candidate is this seat's own quoted literal (`match=` printed) |
| round-55 touch census | `classify.py B` | 275 touches / 28 seat files at receipt time (this seat's own reads included), **274 reads**, 0 writes |
| operator-owned files newer than round-55 start | `find ~/.omp -newermt @1793204671 \( -name 'config.yml*' -o -name 'mcp.json*' -o -name 'lsp.json' -o -path '*/agent/agents/*' \)` | **empty** |
| config mtime vs round-55 start | `stat -c %Y` vs `git log -1 --format=%ct 0a2010ac` | **−861 s** (config older) |
| "is the directive the only instruction source?" | `grep -c 'instead of m_grok' .ufo/prompts/tameshi-round-54.md` | `0` — the turn was operator chat, not directive text (which is exactly why "invented" is wrong and "not in the directive" is not) |
| does anything annotate the round-54 report? | `ls .ufo/reports/round-55/`, `grep -rn 'reports/round-54/tameshi.md'` | **no** round-55 tameshi report; no annotating artifact anywhere |
| census conformance | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tameshi` (`r10`) | **exit 0**, 140 rows (`corpus/SOURCES.md` = 140) |

## 5. Artifacts opened

| Artifact | What it settled |
|---|---|
| `~/.omp/agent/history.db` (mode=ro): `history`, `session_titles` | row 690 = the turn; session `01a182d0` = the run-11 HYAKU session hosting round 54 |
| `~/.omp/agent/sessions/-Projects-shokunin/2026-10-28T14-01-34-216Z_01a182d0-…/T54W1ExecStraceNoise.jsonl` (795 msgs) | yield at 15:06:42.101Z, turn at 15:12:15.736Z, wake at 15:12:24.142Z |
| `~/.omp/agent/sessions/-Projects-shokunin/2026-10-28T14-01-34-216Z_01a182d0-….jsonl` (main session) | the L1's 15:13:57 edit (`scout: "@m_grok"` block) and the 15:21:31/36 reverts |
| all `~/.omp/agent/sessions/**/*.jsonl` | the mutation and touch censuses (68 / 267) |
| `~/.omp/autoqa.db` (`grievances`, mode=ro) | 1 row during round 55 (17:21:23Z) — the sanctioned `report_issue` channel, not a seat host-config write |
| `~/.omp` filesystem (`find -newermt`) | only runtime stores newer than the round-55 start |
| `~/.omp/agent/config.yml` | `:418 scout: "@m_grok"`, sha256 `51beb758…`, mtime 861 s before round 55 |
| `SCORECARD.md` @ C0 (ER-R54-8), `corpus/lessons/round-55.md` @ C0 (`:62`), `.ufo/waves/round-54/w1/T54W1ExecStraceNoise.md` @ C0 | the three record statements under test |
| `/home/vgpnk/Projects/shokunin/.ufo/reports/round-54/tameshi.md` + its git state | the live accusation at `:107-110` |
| `/home/vgpnk/Projects/shokunin/.ufo/prompts/tameshi-round-54.md:373-375, 415-432, 484-494` | the operator-owned clause the records lean on; the report's commit channel |
| `tameshi-shokunin/.ufo/waves/round-55/w1/T55W1ScribeSeat.md` (peer report, read-only) | confirms the scribe located row 690 and the 15:12:15.736Z delivery — the SUPERSEDED attribution is right |
| `corpus/lessons/round-54.md` @ base | 0 occurrences of `config.yml` — the lesson really did omit the incident |

## 6. Bounds

No lane production file, frozen file (`.ufo/evidence/round-55/*`, `contract.json`, `freeze.json`) or wave spec
was edited; no git or jj mutation was run anywhere; the two files written are this report and its receipts
directory. Scratch removed on exit. The fleet-root report and the `~/.omp` stores were read only — the
finding in §3.2 is reported precisely because its artifact is outside this seat's write scope.
