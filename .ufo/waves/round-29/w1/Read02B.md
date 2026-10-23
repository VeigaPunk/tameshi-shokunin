# Read02B — cold read, SKILL.md section at line 375

Seat: Read02B. Read revision: 9f3084bc60ad56aac01e4556ef4c7653df2f65e5 (fleet-mirror
clone detached there; `SKILL.md` sha256 c46ec02e… matched). Section: `## Restore
discipline — before/after identity, not continuous non-write proof`, lines 375–414
(next `##` at 415, inside no fence).

```json
{"schema": "tameshi-coldread-report-v2", "seat": "Read02B", "skill_sha256": "c46ec02e8016ec5dd2dd38c3c769658248d5386f6d84f21e95a3fccd3b5e36d6", "read_rev": "9f3084bc60ad56aac01e4556ef4c7653df2f65e5",
  "sections": [{"start": 375, "heading": "## Restore discipline — before/after identity, not continuous non-write proof", "class": "instruction", "verdict": "executed-ok", "blocking_gaps": [], "wrong_expectations": [],
    "minor_gaps": ["item 2 cites mutation-case-kimi-census.md:4-7 for `cp -p the artifact … and edit only copies`; lines 4-7 hold the read-only-substrate/copies-under-/tmp statement (edit-only-copies supported) but the literal `cp -p` command sits at :172", "`cp -p … into the lane namespace` is loose: the cited cases place copies under lane-owned /tmp scratch (/tmp/tameshi-r2-1-work, /tmp/tameshi-r3-1-work), not inside a lane path", "item 6's `reran from scratch` is anchored by SCORECARD.md:13's fresh /tmp copies + byte-identical restore; the wording is loose but consistent"],
    "commands_executed": ["python3 -c \"import sys;[print(open(p).read()[:200000]) for p in sys.argv[1:]]\" corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md", "bash -c \"git status --porcelain -- corpus/knowledge/mutation-case-kimi-census.md corpus/knowledge/mutation-case-kagi-census.md; cp -p corpus/knowledge/mutation-case-kimi-census.md /tmp/Read02B-scratch-copy.md && sha256sum corpus/knowledge/mutation-case-kimi-census.md /tmp/Read02B-scratch-copy.md && cmp corpus/knowledge/mutation-case-kimi-census.md /tmp/Read02B-scratch-copy.md && stat -c \\\"%s %y\\\" corpus/knowledge/mutation-case-kimi-census.md\"", "bash tools/mutate-and-run.sh --regression"],
    "opened": ["corpus/knowledge/mutation-case-kimi-census.md", "corpus/knowledge/mutation-case-kagi-census.md", "corpus/README.md", "tools/mutate-and-run.sh", "tools/trace-inputs.py", ".ufo/waves/round-26/w1/ColdreadPilot.md", ".gitignore"],
    "inputs": {"corpus/knowledge/mutation-case-kimi-census.md": "034524eff8f19cb8fca78cd5d13c6da9971f2ef2b5bedc1b950309c95c121548", "corpus/knowledge/mutation-case-kagi-census.md": "d3190a9940b9d47b7aae0025b2f4c80228d5a15cbb052cbef316ddff021d0bb0", "corpus/README.md": "91c782f6803a30f26734793f73733e58bb6afc117965e06cbe4c625b88fd3c67", "tools/mutate-and-run.sh": "fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de", "tools/trace-inputs.py": "f59c9312c56eb458d5e24fc9a40b79c8858d9e1a96174d9a24c8ead1dc4a29f4", ".ufo/waves/round-26/w1/ColdreadPilot.md": "428a61a30ff8cf9e02f5a2a0923f916cf5f4c98596d2ace022f9d982fc25ceb7", ".gitignore": "0f699af0108f1ac4f43cd5f61c9151896b8328ec7edd0adf4ca1c638a2441116"},
    "external_inputs": {"tameshi-shokunin@9f3084bc60ad56aac01e4556ef4c7653df2f65e5:SCORECARD.md": "004a411d7af71e1977d619f4ef72aba40c9b9db1059b4f2e7d34da023a98dbac"},
    "traces": ["/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read02B-1.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read02B-2.json", "/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-29/coldread/traces/Read02B-3.json"]}]}
```

What I checked, claim by claim (all in the detached clone, `rev` receipts above):

- Item 1 (before-state fingerprint): kimi note :13-16 carries sha256
  `83016d45…4f426` (full 64 hex), 43273 B, mtime `2026-10-13 18:53:12`,
  kumitate rev `175de6ba…`, `git status --porcelain` empty; kagi note :13-17
  carries `275d8294…53009f`, 44212 B, mtime `2026-10-14 09:47:15 -0300`, mode
  755, kagi `HEAD fecee874…`, porcelain empty. Both cite ranges land exactly.
- Item 2 (scratch edits): kagi :44-45 names "`cp -p` byte copy, `cmp`-verified";
  kimi's `cp -p` reproduce line is :172 (`:4-7` holds the read-only/copies
  statement) — literal-cite nit recorded as minor_gaps.
- Item 3 (after-sweep records): kimi :34-35 = sha before/after `83016d45…4f426`,
  size 43273 B, mtime unchanged, tree clean — no after-repo revision recorded
  (line 4 of the claim, accurate); kagi :54-56 = `275d8294…53009f`, 44212 B,
  mtime `09:47:15` unchanged, porcelain empty, `cmp`-identical scratch copy.
  Exact.
- Item 5 (never `git checkout`/`git restore`): I exercised the commands the
  section endorses (`git status --porcelain --`, `cp -p`, `sha256sum`, `cmp`,
  `stat`) against the case-note file — all rc=0, scratch copy byte-identical;
  did not run the prohibited restore commands.
- Item 6 (durable evidence): `SCORECARD.md:13` (read via `git show`, sha
  `004a411d…`, per the L1-append exception) is the round-2 row recording the
  probes on fresh /tmp copies with before=after sha. `mutate_driver.py` is
  untracked (`git ls-files` shows none), and the kagi note's own Erratum R21
  (:267-274) states the same — "do not by themselves recreate that driver
  after scratch loss … Use `bash tools/mutate-and-run.sh --regression`".
  I ran exactly that under the collector: `REGRESSION: PASS (cases=9
  passed=9; ledger legs exact)` in 285.77 s — legs 1-2 replayed js-kimi-census
  (`175de6ba`, `83016d45…4f426`) and bash-surface-census (`fecee874`,
  `275d8294…53009f`) from git objects with `match=10/10 flips=0`, and the run
  does not recover the old driver. Claim verified end-to-end.
- Item 7 (dirty-at-pin re-pin): `corpus/README.md:11` holds the G-R2-1
  round-2 addendum — surveyed `79294/357fb245` was a never-committed
  dirty-tree state, corrected pin `79301 B/93c5827202b9cdec`. Matches.

Section remains a faithful policy+record anchor at the read revision; the
monitor's `input-drift:corpus/README.md` flag is neutral here (README drift
is the Round-29 append, not a content change to the cited G-R2-1 addendum).
No installs were needed (strace, python3, git all present).

COLDREAD Read02B: executed-ok
