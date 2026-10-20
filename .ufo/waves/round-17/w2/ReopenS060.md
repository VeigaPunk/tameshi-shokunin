# ReopenS060 — source row S060 (strace(1)) re-opened live

Seat: `TameshiR17.ReopenS060-2` (leaf, no dispatch). Read rev:
`eb7838b16490ca7ba17ea3242ade76a61f744af2` (fleet-mirror clone checkout;
`git rev-parse HEAD` → same). Clone:
`/tmp/tameshi-r17w2-ReopenS060-ehA1Me/fleet/tameshi-shokunin`. Lane root untouched
apart from this report. Tools installed/upgraded: none.

Row under attack: `corpus/SOURCES.md:69` (S060); lesson quote
`corpus/lessons/round-17.md:34`; used-by
`corpus/knowledge/input-keyed-coldread-credit.md`.

## 1. Live page and the quote

| step | command | exit | key output |
|---|---|---|---|
| clone | fleet-mirror clone + `git checkout --detach eb7838b…` (contract recipe) | 0 | `rev-parse HEAD` = `eb7838b16490ca7ba17ea3242ade76a61f744af2` |
| fetch | `curl -fsSL -o strace.1.html https://man7.org/linux/man-pages/man1/strace.1.html` | 0 | 85238 bytes, sha256 `eedefecf7c55cf36976fce6fbfff8b1340c62b696bb7268a83df643ee8ea02f6` |
| headers | `curl -sSI …` | 0 | `Last-Modified: Thu, 08 Oct 2026 17:39:35 GMT`; `Date: Tue, 20 Oct 2026 16:05:37 GMT` |
| quote | `grep -n 'file name as an argument' strace.1.html` | 0 | `417: <b>file   </b>Traces all system calls that take a file name as an` (sentence continues `argument.` on 418) |
| join | Python: strip tags, collapse whitespace, search the quote | 0 | `quote-present: True`, `normalized occurrences: 1`, `words: 12` |
| footer | `grep -n 'strace 7.1.0.62.c605d6' strace.1.html` | 0 | `1487: <span class="footline">strace 7.1.0.62.c605d6          2026-06-25 …` |

Location: `OPTIONS` (strace.1.html:217) → `Filtering` (381) →
`-e trace=syscall_set` (382) → `%file` (416) → quote (417–418). The lesson's
stated location "(OPTIONS → Filtering → `-e trace=` → `%file`)" is exact.
The quote is verbatim, 12 words (≤25), and `corpus/lessons/round-17.md:34`
carries it character-for-character.

Cross-checks: the host `strace 7.2` man page has the same sentence on line 589
(`/usr/share/man/man1/strace.1.gz`, sha256
`a5a80dddd1417a887e98672a9a83104f16a62670e37843d8edc07ba430067501`;
`.TH STRACE 1 "2026-06-25" "strace 7.2"` at line 36). `strace --version` →
`strace -- version 7.2`. The fetched page sha256 equals the w1 fetch sha at
`.ufo/waves/round-17/w1/S16SrcStrace.md:6`, so the page bytes did not change
between the two reads.

## 2. Row cells (`corpus/SOURCES.md:69`, NF=13, 11 columns)

- **tier A — holds.** Contract `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:26-29`:
  A = primary/authoritative for the scope (official docs). The colophon
  `strace.1.html:1476` says the page is part of the strace project, obtained
  from its upstream Git repository.
- **scope — holds.** All four named sections exist: `General`/-f
  (218, 327–333), `Filtering`/%file (381, 416–425), `Output format`/-o
  (588, 751–762), `-y` (930–934; `Output format` ends at `Statistics`, 975).
- **anchor — holds exactly.** Footer `strace 7.1.0.62.c605d6` / `2026-06-25`
  (1487); host binary `strace 7.2`.
- **teaches — holds for the lane's observer; one wording gap.**
  - Supported: "file-name syscalls observable per followed process" (`%file`
    plus the `-f` text at 329–333); "open trace records files opened by name";
    "never reads on inherited descriptors" — `strace -f -qq -o t_inh.log
    -e trace=%file -- cat < f` exit 0, 7-line log, `grep -c '"f"\|read('` = 0;
    "env vars" — no syscall names one.
  - Gap (non-blocking): "never … stat-only probes" is false for the cited
    `%file` set. The page itself says `%file` is "an abbreviation for
    `--trace=open,stat,chmod,unlink,…`" and warns not to omit `newfstatat(2)`
    (418–424). Live: `strace -f -qq -o t_stat.log -e trace=%file --
    /bin/sh -c 'test -e /etc/hostname; true'` exit 0,
    `grep -c 'newfstatat\|access('` = 13. The exclusion is true only of the
    lane tool's explicit set `open,openat,openat2,creat,execve,…,dup,dup3,close`
    (`.ufo/evidence/round-17/coldread/trace-inputs.py:75-80`; argv `-e trace=…`
    at :630–632), which is not `%file` — same explicit set on the same command
    gives 0 stat lines. The knowledge entry §4 makes the same claim
    (`corpus/knowledge/input-keyed-coldread-credit.md:60-63`) and `SKILL.md:1893`
    states it as the method's limit; both are true of the tool, but the row's
    `scope` names `%file`, so a reader who runs `%file` sees probes the row
    calls invisible.
- **status `mined` + used-by — holds.** `corpus/knowledge/input-keyed-coldread-credit.md`
  exists at the rev as a regular blob (`git ls-tree`: `100644 blob
  f5b961b62f4b2033d3c462be8176ed3ebcda043f`; sha256
  `1fad5a57c56ea059ebfecedf37edb8256739d94382f89cf302d49d319ab9e57c`), and
  cites S060 at :1 (source header) and :53 (method step 3). Contract
  `mined` = cited by ≥1 `used-by` path (:36). `opened 2026-10-20` matches this
  fetch; `recheck on-release` matches the page lag (footer 7.1 vs host 7.2).

Contract constraint on any fix: rule 2 (`.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:49-51`)
is append-only — only `status`, `recheck` and `used-by` change in place; a
corrected `scope`/`teaches` must be a new row whose `teaches` opens
`supersedes S060 —`. Since the `teaches` claim is exactly right for the tool
the used-by entry describes, `mined` is not in question; the minimal future
fix is scope wording (e.g., naming the explicit open-family set rather than
`%file`) in a superseding row.

## 3. Remaining unknowns

- Whether L1 intends `scope`'s `%file` to name the source's teaching set or the
  tool's argv; that intent decides whether the stat clause needs any action.
- 7.1→7.2 drift beyond the quoted sentence and -f/-o/-y text was not compared
  (outside this row's cells).

Verdict: **S060 holds** — quote verbatim at `%file`, 12 words, location, tier,
scope, anchor and used-by all true; the single "never … stat-only probes"
clause is true of the lane's explicit open-family trace but false of the row's
cited `%file` set (minor, non-blocking wording gap).
