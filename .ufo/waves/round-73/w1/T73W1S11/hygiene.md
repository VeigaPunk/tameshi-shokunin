# Seat T73W1S11 — hygiene and security review (round 73)

Read-only review of the round's artifacts. Lane root
`/home/vgpnk/Projects/shokunin/tameshi-shokunin`, fleet root
`/home/vgpnk/Projects/shokunin`, base `a3dd3574` = origin/master.
No tracked file was written, no git/jj mutation was issued (read-only
`log/show/diff/status/rev-parse/ls-files/ls-tree/check-ignore/grep` only), no
git fixture repo was created (one non-git scratch copy of three lane files
was used for the `.pyc` reproduction in section 5), no subagent was spawned.

The lane is **live**: HEAD moved `17cd1939 -> 2e89e539 -> 7982619f ->
4ebf7a1e -> 3e0ef1c8 -> 1d118c14 -> caa5c4c5 -> 06ce20f7` during the review,
and the untracked artifact set grew from 15 to 140 files. Every measurement
below is timestamped; conclusions that depend on a moving set name the sample.

## Summary

| # | check | result |
|---|---|---|
| 1 | credential material in round artifacts | **1 secret-shaped artifact** (committed `set-cookie` session token) |
| 2 | TMPDIR discipline / hardcoded `/tmp` | **clean** — 0 violations, 0 hardcoded `/tmp` |
| 3 | misroot at the fleet root | 3 files total name this lane or round 73; **0 written by this round** |
| 4 | lane write scope | 18 sampled entries, **all this round's**; 0 inherited, 0 foreign |
| 5 | symlinks and write escapes | 0 symlinks; 1 real write outside declared outputs (implicit `.pyc`) |

Two defects are real and measured (1 and 5-second-item), one contract defect
in the new C1 instrument (5-third-item). The TMPDIR, misroot and symlink
predicates hold. Details, commands and outputs follow.

---

## 1. Credential material — SECRETS=1

Artifact inventory: **72 files / 2,758,199 bytes** at the 22:07 scan and
**140 files / 7,399,273 bytes** at the final 22:12 re-scan under
`.ufo/evidence/round-73/` + `.ufo/waves/round-73/`, recursively (the growth
includes this seat's own report files). Both runs agree on the one hit below.

Scanner (run from the lane root; 13 pattern families: private-key headers,
PGP private key, cloud AKID, forge tokens, chat-API keys, JWT, bearer,
`set-cookie`/`cookie`, `authorization`/`x-api-key`, URL credentials,
password/secret assignments, credential paths, env token assignments):

```
# scan 1 — artifact set at 22:07
files_scanned= 72 bytes= 2758199
pattern_counts= {'cookie-header': 1}
  HIT ('cookie-header', '.ufo/evidence/round-73/sources/rfc8259-headers.txt', 9)

# scan 2 — final set at 22:12, which includes this seat's own report files
files_scanned= 140 bytes= 7399273
pattern_counts= {'cookie-header': 1}
  HIT ('cookie-header', '.ufo/evidence/round-73/sources/rfc8259-headers.txt', 9)
```

Reported as shape only (no value reproduced here):

- file `.ufo/evidence/round-73/sources/rfc8259-headers.txt`, line 9, 323 bytes:
  `set-cookie: __cf_bm=<43-char base64url>.<unix-epoch>.1.0.1.1.<87-char base64url signature>`
- embedded epoch `1793753888` = `2026-11-04T00:58:08Z`, i.e. the capture time;
  `__cf_bm` is a Cloudflare bot-management session cookie with a ~30-minute
  lifetime, so the value was **live at capture** and at/just past expiry at
  scan time.
- the same 13-line response-header dump also carries `cf-ray` (21-char
  PoP-tagged value), `date`, `server`, `alt-svc` — fetch-time / edge-PoP
  metadata, not credentials.

Committed, not just in the worktree:

```
$ git log --oneline --diff-filter=A -- .ufo/evidence/round-73/sources/rfc8259-headers.txt
17cd1939 round-73: declaration (frozen plan, lesson gate, LOG, census/base receipts, wave spec+dispatch)
$ git show HEAD:.ufo/evidence/round-73/sources/rfc8259-headers.txt | grep -ci '^set-cookie:'
1
$ git grep -c '__cf_bm' a3dd3574 -- .      # base: absent
$ git grep -c '__cf_bm' HEAD -- .
HEAD:.ufo/evidence/round-73/sources/rfc8259-headers.txt:1
```

Negative results, all measured: 0 private-key headers, 0 PGP private keys,
0 cloud AKIDs, 0 forge/chat-API tokens, 0 JWTs, 0 `bearer` strings, 0 URL
credentials, 0 password/secret assignments, 0 hits on the credential-store
path patterns (SSH key material, netrc, cloud credential files, the psql
password file, Kubernetes cluster config and git-credential stores were all
in the pattern set and all returned zero), 0 SSH public-key lines. The high-entropy pass produced
23 raw hits; each was classified individually: 19 git SHA-1/SHA-256 hex
digests (revs and artifact hashes in receipts) and 4 absolute-path fragments
(`home/vgpnk/...`, `add/...`). None was an encoded secret.

The round's tracked delta outside those two directories was scanned with the
same patterns at HEAD `06ce20f7` — 11 files
(`git diff --name-status a3dd3574..HEAD` minus the two round dirs: modified
`LOG.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `plans/round-72.plan.md`,
`tools/pointer-recheck.json`, `tools/rekey-cost.py`,
`.ufo/evidence/round-21/coldread/ledger.json`; added
`corpus/lessons/round-73.md`, `plans/round-73.plan.md`,
`tools/wave-reconcile.{py,json}`):
`tracked_files_scanned= 11 tracked_secret_shaped_hits= 0`.

**Severity: LOW.** Impact: a ≤30-minute replay window on a third-party
public-fetch session cookie, no account/lane credential, no geographic value
beyond the PoP code. The durable harm is procedural — a receipt generator
committed raw response headers, so the next capture can carry a longer-lived
credential. **Smallest remediation:** redact the value on line 9
(`set-cookie: <redacted>`) and have the header-dump receipt strip
`set-cookie`/`cookie`/`authorization`/`x-api-key` before writing.

---

## 2. Scratch discipline — TMPDIR_VIOLATIONS=0

Static check (both tools, no literal `/tmp`):

```
$ grep -n '/tmp' tools/wave-reconcile.py tools/rekey-cost.py
$ echo $?
1
```

Both scratch sites are TMPDIR-driven, with the only environment read in
either file being `TMPDIR`:

```
tools/wave-reconcile.py:363:    work = tempfile.mkdtemp(prefix='wave-reconcile-selftest-',
tools/wave-reconcile.py:364:                            dir=os.environ.get('TMPDIR') or None)
tools/rekey-cost.py:252:    work = tempfile.mkdtemp(prefix='rekey-cost-selftest-',
tools/rekey-cost.py:253:                            dir=os.environ.get('TMPDIR') or None)
$ grep -n 'os\.environ\|getenv' tools/wave-reconcile.py tools/rekey-cost.py
tools/wave-reconcile.py:364:                            dir=os.environ.get('TMPDIR') or None)
tools/rekey-cost.py:253:                            dir=os.environ.get('TMPDIR') or None)
```

Cleanup is unconditional: `shutil.rmtree(work, ignore_errors=True)` inside
`finally` (`wave-reconcile.py:448`, `rekey-cost.py:289`).

Dynamic matrix — 4 commands x 3 TMPDIR cases, run from the lane root:

```
CASE=fresh        TMPDIR=/fast/scratch/.../tmpA  rc=0 LAST=WAVE_RECONCILE_SELFTEST: 12/12 pass
CASE=fresh        TMPDIR=/fast/scratch/.../tmpA  rc=0 LAST=WAVE_RECONCILE: rows=6 met=6 unexpected=0
CASE=fresh        TMPDIR=/fast/scratch/.../tmpA  rc=0 LAST=REKEY_COST_SELFTEST: 8/8 pass
CASE=fresh        TMPDIR=/fast/scratch/.../tmpA  rc=0 LAST=REKEY_ARMS: arms=7 meet=7 unexpected=0
CASE=empty        TMPDIR=<empty>                 rc=0 LAST=WAVE_RECONCILE_SELFTEST: 12/12 pass
CASE=empty        TMPDIR=<empty>                 rc=0 LAST=WAVE_RECONCILE: rows=6 met=6 unexpected=0
CASE=empty        TMPDIR=<empty>                 rc=0 LAST=REKEY_COST_SELFTEST: 8/8 pass
CASE=empty        TMPDIR=<empty>                 rc=0 LAST=REKEY_ARMS: arms=7 meet=7 unexpected=0
CASE=nonexistent  TMPDIR=/nonexistent-xyz        rc=2 LAST=WAVE_RECONCILE error=selftest-setup:[Errno 2] No such file or directory: '/nonexistent-xyz/wave-reconcile-selftest-6jl71s7z'
CASE=nonexistent  TMPDIR=/nonexistent-xyz        rc=0 LAST=WAVE_RECONCILE: rows=6 met=6 unexpected=0
CASE=nonexistent  TMPDIR=/nonexistent-xyz        rc=2 LAST=REKEY_COST error=selftest-setup:[Errno 2] No such file or directory: '/nonexistent-xyz/rekey-cost-selftest-uvzgqp22'
CASE=nonexistent  TMPDIR=/nonexistent-xyz        rc=0 LAST=REKEY_ARMS: arms=7 meet=7 unexpected=0
--- fresh dir residue --- 0
```

Interpretation, per case:

- **fresh empty dir** — both selftests write only under it. strace of the
  write-capable syscalls (`openat`/`mkdir`/`mkdirat`/`unlinkat`) shows every
  write-intent path under `<TMPDIR>/wave-reconcile-selftest-*` and
  `<TMPDIR>/rekey-cost-selftest-*` (fixture files `SKILL.md`, `shared.md`,
  `beta.md`, `gamma.md`, `delta.md`, `old-only.md`, the copied
  `.ufo/evidence/round-18/measure.py`, its `__pycache__`, and the fixture
  ledger). Residue afterwards: 0 files.
- **TMPDIR empty** — both tools fall back to the stdlib default, by design
  (`os.environ.get('TMPDIR') or None`). strace proof of the fallback target:

  ```
  $ TMPDIR= strace -f -e trace=mkdir,mkdirat -o log \
      python3 -I -X utf8 tools/wave-reconcile.py --selftest
  wave selftest rc=0
  "/tmp/wave-reconcile-selftest-vhfx_ioe"
  ```

  This matches `tempfile.gettempdir()` semantics (an empty `TMPDIR` is
  treated as unset), and both runs still cleaned up (`ls -d
  /tmp/wave-reconcile-selftest-* /tmp/rekey-cost-selftest-*` -> 0). Counted
  as honoured, not a violation.
- **TMPDIR=/nonexistent-xyz** — the selftests **fail closed**: exit 2 with a
  single `error=selftest-setup:` line, no traceback, and no silent fallback
  write anywhere. The two modes that allocate no scratch (the standing
  sweep, `--arms`) are unaffected and keep their frozen lines, rc=0.

Verdict: both tools honour `TMPDIR`; `TMPDIR_VIOLATIONS=0`.

---

## 3. Misroot at the fleet root — MISROOT=3

```
$ date -Is
2026-11-03T22:09:57-03:00
$ git -C /home/vgpnk/Projects/shokunin status --porcelain
 M .scratch/goal-20261103-hyaku-run15.md
 M .scratch/run15-state.json
?? .scratch/run13-state.json
?? .scratch/run15-kernel.py
?? .ufo/reports/round-71/kama.md
?? after
```

Every untracked entry, and all 83 ignored non-repository files, were scanned
for lane/round tokens (`tameshi`, `round-73`, `round 73`, `T73W1`):

| file | git state | content match | attribution |
|---|---|---|---|
| `.scratch/run13-state.json` | untracked (`??`) | names lane `tameshi` (2 hits: `lanes.tameshi.block=[60,69]`, `trained.tameshi=60`), **no round-73 token** | orchestrator run-13 state, mtime Oct 30 |
| `.ufo/state/inline-dispatcher.log` | ignored | 210 round-73 hits | dispatcher runtime log |
| `.ufo/watchdog.log` | ignored | 1 round-73 hit | watchdog runtime log |

- `.scratch/run15-kernel.py`, `.ufo/reports/round-71/kama.md`, `after`:
  `tameshi=0 round73=0` — not this lane's material.
- **No untracked fleet-root file carries round-73 seat or artifact content,
  and none was written by this round.** MISROOT counts files that *name* the
  lane/round, not invocations of the lane: the count is 3, all
  orchestrator-owned runtime state that predates or schedules this wave.
- Adjacent observation (tracked, modified, out of the untracked count):
  `.scratch/run15-state.json` carries `"label": "TameshiR73"` — the
  orchestrator's live dispatch table. `.scratch/goal-...run15.md` mentions
  tameshi rounds 60/72 as history only.
- Scope note: nested sibling lane repositories (`audio-shokunin/`,
  `chousa-shokunin/`, ...) are independent git working trees that the fleet
  repo ignores wholesale; their own `round-73` files belong to their own
  rounds and were excluded. Nothing was deleted or modified at the fleet
  root.

---

## 4. Lane write scope — 0 inherited, 0 foreign

Sample at 22:09:57, HEAD `06ce20f7` (18 entries; the set grows while seats
work, so this is a timestamped sample, not a fixed inventory):

| entry | class |
|---|---|
| ` M corpus/lessons/round-73.md` | this round's (lesson-gate edit, in flight at sample) |
| `?? .ufo/evidence/round-73/additivity-b2-r73.txt` | this round's receipt |
| `?? .ufo/evidence/round-73/inherited-misses-r73.txt` | this round's receipt |
| `?? .ufo/evidence/round-73/instruments-tip-r73.txt` | this round's receipt |
| `?? .ufo/evidence/round-73/live-green-b2-r73.{json,out}` | this round's receipts |
| `?? .ufo/evidence/round-73/live-green-hist-b2-r73.{json,out}` | this round's receipts |
| `?? .ufo/evidence/round-73/live-revmode-b2-r73.{json,out}` | this round's receipts |
| `?? .ufo/evidence/round-73/mistake-exit-capture-r73.txt` | this round's receipt |
| `?? .ufo/evidence/round-73/mistake-spec-key-r73.txt` | this round's receipt |
| `?? .ufo/evidence/round-73/rekey-arms-r73.txt` | this round's receipt (C2) |
| `?? .ufo/evidence/round-73/wave-reconcile-live-r73.txt` | this round's receipt (C1) |
| `?? .ufo/evidence/round-73/wave-selftest-r73.txt` | this round's receipt (C1) |
| `?? .ufo/waves/round-73/w1.ready`, `w1.ready.dispatched` | this round's (dispatcher) |
| `?? .ufo/waves/round-73/w1/` | this round's (seat reports) |

All 18 entries are this round's; **inherited 0, foreign 0**. No entry touches
`tools/` (C2's `tools/rekey-cost.py` was committed at `7982619f`), `plans/`,
`LOG.md`, `SCORECARD.md`, `SKILL.md`, `PROVINCE.md`, or the fleet root.

Transient observation worth recording: at the 22:03 sample the worktree also
showed ` M .ufo/evidence/round-21/coldread/ledger.json` (+11,197/-0 lines)
and `?? .ufo/evidence/round-73/win-host/`; both were gone from
`git status` at 22:09 because commit `2e89e539` landed at 22:02:48 (read-only
`git reflog` confirms). That diff was the C1 cold-read rekey in flight — an
in-progress write, not an uncommitted residue.

Ignored byproducts created under the lane today (`git status --ignored`;
`.gitignore:4: __pycache__/`), none tracked:

```
./tools/__pycache__                                       2026-11-03 22:01
./.ufo/evidence/round-73/win-host/__pycache__             2026-11-03 22:06
```

`tools/__pycache__/wave-reconcile.cpython-314.pyc` shows the new C1 tool was
imported as a module by some harness; the `win-host` one (25,365 bytes, the
only binary artifact under the round dirs) was produced by executing the
copied precheck script. Both are gitignored, and the pyc embeds only in-tree
path fragments.

Round-wide tracked delta `git diff --name-status a3dd3574..HEAD` at
`06ce20f7` is **7 modified + 83 added**, and the 7 modified paths are exactly
the declared edit set plus its two by-products: `LOG.md`,
`corpus/QUALITY.md`, `corpus/SOURCES.md`, `plans/round-72.plan.md` (the
declared erratum), `tools/pointer-recheck.json`, `tools/rekey-cost.py` (C2)
and `.ufo/evidence/round-21/coldread/ledger.json` (the C1 rekey output). The
83 additions are the two C1 tool files, `corpus/lessons/round-73.md`,
`plans/round-73.plan.md`, and this round's evidence/wave receipts. No
unexpected tracked path.

---

## 5. Symlinks and write escapes

Symlinks and link hygiene:

```
$ find .ufo/evidence/round-73 .ufo/waves/round-73 -type l | wc -l
0
$ git ls-tree -r HEAD -- .ufo/evidence/round-73 .ufo/waves/round-73 tools/wave-reconcile.py tools/wave-reconcile.json \
  | awk '$1!="100644"'
100755 blob 0a90d1f815a4d2144aaf771ca127463885515f45	tools/wave-reconcile.py
$ find .ufo/evidence/round-73 .ufo/waves/round-73 -type f -links +1 | wc -l
0
$ find .ufo/evidence/round-73 .ufo/waves/round-73 \( -type f -o -type d \) -perm -002 | wc -l
0
```

No symlink in either round tree, no mode-120000 blob, no hardlinked artifact,
no world-writable file or directory. Modes are 644 throughout except
`w1/swarm-registry.json` (600, dispatcher-written, owner-readable only).

Declared write surfaces, statically and under strace:

- `tools/wave-reconcile.py` — writes: `open(out,'w')` only when `--json-out`
  is given (caller-declared path, `wave-reconcile.py:320`); the selftest
  scratch under `TMPDIR`; everything else is read-only git
  (`cat-file blob`, `ls-tree -r`) against the named `--repo`/`--extra-root`.
  strace of the standing sweep, with and without `--json-out`, shows the only
  write-intent path outside `TMPDIR` is the declared output / `/dev/null`.
- `tools/rekey-cost.py` — writes: `Path(a.json_out).write_text(...)`
  (`rekey-cost.py:342`, caller-declared); selftest fixture under `TMPDIR`.
  `--arms` writes nothing.

Both declared outputs were exercised (`--json-out` into scratch): each
produced exactly the named file, rc=0 with the frozen line
(`WAVE_RECONCILE: rows=6 met=6 unexpected=0`, `REKEY_COST sections=64
planned=1 at_risk=13 predicted_lost=13`).

**FOUND (write outside declared outputs, LOW).** `rekey-cost.py` loads the
frozen module from `<repo>/.ufo/evidence/round-18/measure.py` through
`importlib.util.spec_from_file_location` (`load_sectionizer`), so CPython
writes a bytecode cache *inside the tree named by `--repo`*. Reproduced on an
isolated scratch copy of the lane tree (three files copied, no writes to the
lane):

```
before_pycache=0
$ python3 -I tools/rekey-cost.py --repo /fast/scratch/.../fixture-repo --edit PROVINCE.md
RISK ## Standing rules | pins=PROVINCE.md
...
REKEY_COST sections=64 planned=1 at_risk=6 predicted_lost=6
rc=0
after_pycache=1
/fast/scratch/.../fixture-repo/.ufo/evidence/round-18/__pycache__/measure.cpython-314.pyc
```

In the real lane the same path already exists (`.ufo/evidence/round-18/
__pycache__`, mtime Oct 26) and is gitignored (`git check-ignore -v` ->
`.gitignore:4:__pycache__/`), so the impact is bounded: gitignored
`__pycache__` only, never a tracked file, no data outside the repo named by
the caller. **Smallest remediation:** set `sys.dont_write_bytecode = True` in
`load_sectionizer` (or `compile()`/`exec()` the frozen source), so the tool
writes nothing under `--repo`.

**Trust-boundary probes on the new C1 instrument** (untrusted manifest
records, scratch manifests, all read-only against the lane):

| probe | result |
|---|---|
| `record.path = ../../../../etc/hostname` | exit 2 `error=setup:git-failed:...fatal: '...' is outside repository` |
| `record.path = /etc/hostname` | exit 2 `fatal: path '/etc/hostname' exists on disk, but not in '<rev>'` |
| `record.rev = ../../etc` | exit 2 `error=setup:rev-unresolvable:../../etc` |
| row without `wave` / without `record` | exit 2 `error=setup:row-missing-results:<id>` |
| unknown `kind`, missing declaration form | exit 2 `kind-unknown` / `declaration-form-unknown` |
| empty or non-list `rows` | exit 2 `error=setup:zero-rows` |
| `record.printed` as string / float / bool | exit 2 `record-printed-absent` / `printed-not-in-span` |

Escapes through record paths and revs are refused by git and by the rev
regex before any row is measured — good. **FOUND (contract defect, LOW).**
An *undeclared row-level root* reaches an unguarded dict lookup at two sites
that lack the `if root not in readers: raise SetupError('unknown-root')`
guard the sibling `_artifact` path has:

```
$ grep -n 'readers\[' tools/wave-reconcile.py
144:    return readers[root], art['rev'], art[key]          # guarded by _artifact
152:    reader = readers[rec.get('root', 'lane')]            # UNGUARDED
216:    reader = readers[decl.get('root', 'lane')]           # UNGUARDED
304:        readers[name] = GitReader(path)
$ python3 -I -X utf8 tools/wave-reconcile.py --repo . --extra-root fleet=... --manifest .../root-undeclared.json
  File ".../tools/wave-reconcile.py", line 152, in _record_span
    reader = readers[rec.get('root', 'lane')]
KeyError: 'evilroot'
rc=1
$ python3 -I -X utf8 tools/wave-reconcile.py --repo . --extra-root fleet=... --manifest .../root-decl.json
  File ".../tools/wave-reconcile.py", line 216, in measure
    reader = readers[decl.get('root', 'lane')]
KeyError: 'evilroot'
rc=1
```

Impact: a manifest setup error produces an uncaught traceback with absolute
paths and **exit 1**, which collides with the tool's documented "a row
measured other than expected" exit 1 — a caller cannot distinguish drift
from a malformed manifest at the exit-code level, and the documented
`error=setup:` (exit 2) contract is bypassed. Not attacker-reachable in
normal operation (the manifest is a committed file), but it is the one place
the new instrument's own failure-mode contract is not enforced.
**Smallest remediation:** add the same `unknown-root` SetupError guard at
lines 152 and 216.

Minor, noted not scored: the manifest `schema` field is not validated at all
— a manifest with no `schema` key swept normally (`rows=1 met=1`, rc=0)
because only the four row kinds and `expect` are checked.

---

MISROOT=3 SECRETS=1 TMPDIR_VIOLATIONS=0
