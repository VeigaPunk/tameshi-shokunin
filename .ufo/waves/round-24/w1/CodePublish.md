# CodePublish — `publish()` and the CLI exit/usage map of `tools/registry-replay.py`

**Verdict:** The refusal *branch* of `publish()` is correct — on `bundle is None` it writes nothing new — but the function is **not atomic** (three sequential writes, no temp+rename), it **never clears or invalidates artifacts left by a previous run in the same `--out`**, and the resulting directory can present a **self-consistent, digest-matching green bundle that the paired consumer gate accepts (exit 0, `finding_ids: []`) even though the current run refused**. Separately, the **exit/usage map diverges from the SKILL.md round24 row** in three concrete ways: an unusable `--out` exits **1 with a Python traceback and no stdout report** (the row reserves 1 for "refused (findings)" and 2 for "invalid or unavailable input"); the **exit-2 report shape differs between `--project` and `--run`** and never carries the `schema` key that exit 0/1 reports carry; and the row's **"writes only under `--out`"** scope cell is falsifiable for `--run`, because the tool's own git plumbing executes the operator's global `core.hooksPath` `post-checkout` hook, whose writes land outside `--out` (the tool *strips* a caller-supplied `GIT_CONFIG_GLOBAL=/dev/null` instead of pinning it, and its clone lacks the `-c core.hooksPath=/dev/null` that its own runner `tools/registry-check.py:787` sets).

No producer authentication, no promotion, no historical R17-CMD-BIND closure and no numeric score uplift is claimed or supported by this review.

**Reviewed revision:** `c8c5b88c8e961a929cdc351b95a7074c76958909` (delivered wave revision); base `6a1821a8897eea6e7d9669292160ec9593669409`.
**Tool bytes audited:** `tools/registry-replay.py` sha256 `9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714` — identical in the live tree and at `c8c5b88` (`git show c8c5b88:tools/registry-replay.py | sha256sum` → same digest), and equal to `instrument_sha256` in `.ufo/evidence/round-24/replay-command.json`.
**Authority compared against:** `SKILL.md:2050-2059` (the round24 registry row) and `tools/registry.json` (row `registry-replay-selftest`, `status: active`).

---

## Axes (godspeed)

| Axis | Question this lane answers |
|---|---|
| **Calibration** | Does the SKILL.md row's exit map match what the tool actually does for every input class? |
| **Honest write scope** | Does the tool write only under `--out`, as the row claims? |
| **Evidence integrity** | Can a refusal ever leave a directory that reads as a green published bundle? |
| **Single authority** | Does `publish()` re-validate what it writes, or trust its input blindly? |

---

## Method (read-only in the lane; probes confined to /tmp)

Everything in the lane repo was read-only (`git show`/`git log`/`git diff`, `grep`, `read`). No git or jj write command, no registry battery, no gate, no selftest was run in `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.

Executable probes ran **only** in `/tmp/CodePublish-r24/` on a byte-identical copy of the tool (`sha256 9fcd2dbb…5208714`) plus a synthetic one-row lane repo. The synthetic row runs `python3 -c "print('SYNTH-OK')"` — no lane code, no sibling repo, no network. Probe outputs are quoted verbatim below.

```
$ cp -p .../tools/registry-replay.py /tmp/CodePublish-r24/lab/registry-replay.py
$ sha256sum /tmp/CodePublish-r24/lab/registry-replay.py
9fcd2dbba737f0b1b412a9c955fe78e2bb7ea316bf56f98b40a475def5208714
```

---

## Findings by severity

### F1 — HIGH — a refusal leaves the previous run's green bundle in `--out`, and that stale pair still passes the consumer gate

`publish()` returns immediately when the projection refused, and never touches the files a previous run left behind:

```python
116: def publish(code, report, bundle, out):
117:     if bundle is None:
118:         return report
119:     out.mkdir(parents=True, exist_ok=True)
120:     raw = encode(bundle)
121:     report['bundle_sha256'] = hashlib.sha256(raw).hexdigest()
122:     (out / 'bundle.json').write_bytes(raw)
123:     (out / 'expected.json').write_bytes(encode({...}))
125:     (out / 'live-dependent.json').write_bytes(encode({...}))
```
(`tools/registry-replay.py:116-128`)

Probe — publish green into `OUT`, then refuse into the **same** `OUT`:

```
$ python3 registry-replay.py --project clean.json  --out OUT --json
{"bundle_sha256": "f737e6bc…", "finding_ids": [], …}
exit=0
$ python3 registry-replay.py --project refused.json --out OUT --json
{"bundle_sha256": null, "finding_ids": ["RUNNER_NOT_HELD"], "refused_rows": ["one"], …}
exit=1
--- OUT after refusal ---
bundle.json  expected.json  live-dependent.json     # all three from run 1
$ sha256sum OUT/bundle.json
f737e6bc9e4aa4d464f5dc4c34c92ebbfc8beec1890beddf461428cceffbfce8
$ cat OUT/expected.json
{"bundle_sha256": "f737e6bc…", "schema": "command-binding-expected-v1"}   # still pins run 1
$ python3 command-binding.py --bundle OUT/bundle.json --expected OUT/expected.json --json
{"bundle_sha256": "f737e6bc…", "exit": 0, "finding_ids": [], "schema": "command-binding-report-v1"}
consumer exit=0
```

The stale `bundle.json` and the stale `expected.json` remain **mutually consistent** — `expected.json` still pins the old bundle's digest — so the paired gate `tools/command-binding.py` cannot detect that they are stale. It returns exit 0 with an empty `finding_ids` list. A consumer that reads the `--out` directory rather than the tool's exit code gets a **false green**: "a bundle was published and it binds cleanly" for a run that in fact published nothing (`bundle_sha256: null` in the report).

This extends the already-recorded wave finding in `corpus/lessons/round-24.md` Erratum G ("A refused run leaves an earlier bundle in the same `--out` (CorpusSkill)") with two facts that line does not state: the stale pair is *self-certifying green* for the consumer, and in `--run` mode the directory becomes **mixed-vintage**.

Mixed-vintage probe (`--run` into a directory that already held a green bundle, with a row that fails):

```
$ python3 … --run --repo …/lanerepo2 --rev a3afcf4… --out mixedout
synthetic-fail 3 False
{"bundle_sha256": null, "finding_ids": ["RUNNER_NOT_HELD"], …}
exit=1
$ python3 -c "…"
observations revision: a3afcf465826d9275b1c57cfcecc82e24ef243c5
bundle revision      : 291cdddbe22a0669b5dd9fe21e70f1798bb68ef2
SAME RUN? False
bundle rows: 1 names: ['synthetic-ok']
observations rows: ['synthetic-fail']
```

`--run` writes `observations.json` at `tools/registry-replay.py:183` **before** projecting, so a refusal overwrites the observations of the committed run while the stale `bundle.json`/`expected.json`/`live-dependent.json` survive. The directory then holds observations from revision B and a bundle from revision A, and the pinned registry rows still do not cover it (`corpus/lessons/round-24.md` Erratum L: "No registry row pins the round24 replay bundle").

**Smallest safe correction:** `publish()` should make `--out` state reflect the current run only. On refusal, remove (or overwrite with a refusal marker) any `bundle.json`/`expected.json`/`live-dependent.json` left by an earlier run in that directory, and write the report itself into `--out` so a later reader can tell "refused" from "not run". Writing to a temp file and `os.replace`-ing it into place also removes the partial-set window of F2.

### F2 — HIGH — `publish()` is not atomic: a failure at the second write leaves a published `bundle.json` with no matching `expected.json`

`publish()` performs three independent `write_bytes` calls (`:122`, `:123-124`, `:125-127`) with no temp-file + `os.replace`. The first write therefore commits before the second can fail, and there is no rollback.

Probe — make the second write fail (pre-create `expected.json` as a directory):

```
$ mkdir -p o_part/expected.json
$ python3 registry-replay.py --project clean.json --out o_part --json
IsADirectoryError: [Errno 21] Is a directory: 'o_part/expected.json'
exit=1
--- o_part contents after the crash ---
-rw-r--r-- 1 vgpnk vgpnk  485 bundle.json      # <-- published
drwxr-xr-x 2 vgpnk vgpnk    6 expected.json
$ python3 command-binding.py --bundle o_part/bundle.json --expected o_part/expected.json --json
{"bundle_sha256": null, "exit": 2, "finding_ids": ["INVALID_INPUT"], …}
consumer exit=2
```

The failure mode is fail-closed *for the consumer that uses both files* (`INVALID_INPUT`, exit 2) — good — but the directory now presents a `bundle.json` with no valid digest pin, and the tool's own exit code is 1 with a traceback (see F3). A consumer that keys on "`bundle.json` exists ⇒ a bundle was published" is misled. The same window exists on any interruption between `:122` and `:123`.

**Smallest safe correction:** write each artifact to `<name>.tmp` in the same directory and `os.replace` it into position, so a file's presence always means its complete content; and write `bundle.json` **last**, after the digest pin exists, so the presence of `bundle.json` implies a pinnable bundle.

### F3 — MEDIUM-HIGH — the exit map does not match the SKILL.md round24 row

`SKILL.md:2052` declares the verdict map:

> `0 bundle published or plan printed; 1 refused (RUNNER_NOT_HELD, RUNNER_CLEANUP_FAILED, STREAM_LIMIT); 2 invalid or unavailable input, could-not-evaluate; 64 usage, could-not-evaluate`

Observed divergences (all from `tools/registry-replay.py`):

**(a) An unusable `--out` exits 1 with a traceback and no report.** `publish()` calls `out.mkdir(parents=True, exist_ok=True)` at `:119` with no error handling, so an `--out` that is an existing regular file or sits under an unwritable parent raises:

```
$ python3 registry-replay.py --project clean.json --out afile --json
FileExistsError: [Errno 17] File exists: 'afile'
exit=1
$ python3 registry-replay.py --project clean.json --out ro/sub --json
PermissionError: [Errno 13] Permission denied: 'ro/sub'
exit=1
```

Exit 1 is the documented *refused (findings)* code, and stdout carries **no JSON report at all** (only the traceback on stderr). This is the "invalid or unavailable input" class the row assigns to exit 2, and it is distinct from the already-recorded `--run` input-unavailability case (`corpus/lessons/round-24.md` Erratum G): here the failure is in the *output* path, inside `publish()` itself, and it hits `--project` too.

**(b) The exit-2 report shape is not stable across modes, and never carries `schema`.** Exit 0/1 reports carry `"schema": "registry-replay-report-v1"` plus `rows`, `refused_rows`, `live_dependent`, `max_stream_bytes`, `bundle_sha256`. The exit-2 reports do not:

```
$ python3 registry-replay.py --project nosuch.json --out OUT2 --json
{"finding_ids": ["INVALID_OBSERVATIONS"]}          # no schema, no rows
exit=2
$ python3 registry-replay.py --project bad.json --out OUT3 --json
{"finding_ids": ["INVALID_OBSERVATIONS"]}
exit=2
```

And in `--run` mode the exit-2 paths print **plain text on stderr and nothing on stdout** (`registry-replay.py:140`, `:145`, `:158`), so the machine-readable channel differs again:

```
$ python3 … --run … --requirements frozen-bad.json … > stdout.txt 2> stderr.txt
exit=2
stdout bytes: 0
stderr: registry-replay: frozen registry digest mismatch
```

A consumer that switches on `report["schema"]` raises `KeyError` on exit 2; a consumer that reads stdout for a report gets an empty string in `--run` mode. Neither behaviour is described by the row.

**(c) `--plan` accepts a non-existent or non-directory `--repo` and exits 0.** `plan()` (`:63-70`) only `realpath`s the argument and globs its parent; it never checks that the path exists or is a directory:

```
$ python3 registry-replay.py --plan --repo /tmp/CodePublish-r24/plainfile --json
{"fleet_root": "/tmp/CodePublish-r24", "repo": "/tmp/CodePublish-r24/plainfile", "siblings": []}
exit=0
```

The row says 0 means "bundle published **or plan printed**" — here a plan was printed, but it describes a fleet root derived from a regular file. (`corpus/lessons/round-24.md` Erratum G already records "`--plan` on a missing repo exits 0"; the file-not-directory case is the same defect class and is reproduced here for completeness.)

**(d) `--selftest` failure exits 1**, colliding with the refusal code, while printing a different stdout shape (`CASE … FAIL` lines plus `REGISTRY_REPLAY_SELFTEST: n/m pass`) than either machine mode. The `registry-replay-selftest` row pins `REGISTRY_REPLAY_SELFTEST: 10/10 pass` (10 = 9 projection cases + 1 plan case, `registry-replay.py:199-206`, `:243-245`), so the collision is detectable via the token, but the exit code alone does not disambiguate.

Usage errors themselves are correct: no mode, two modes, and `--max-stream-bytes 0` all exit 64 via `Parser.error` (`:46-50`, `:263-264`, `:285-286`).

### F4 — MEDIUM-HIGH — the row's "writes only under `--out`" is falsifiable in `--run` mode: the tool's own git plumbing runs the operator's global hooks

`SKILL.md:2052` Write-scope cell: *"writes only under `--out`; rows run in a private clone whose fleet mirror symlinks live siblings"*.

The tool's `env()` **strips** every `GIT_*` variable from the child environment rather than pinning the hardening values:

```python
57: def env():
58:     e = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
59:     e['PYTHONDONTWRITEBYTECODE'] = '1'
60:     return e
```

and its clone/checkout do not disable hooks:

```python
153:        subprocess.run(['git', 'clone', '--quiet', '--no-hardlinks', repo, str(clone)], check=True, env=e)
154:        subprocess.run(['git', '-C', str(clone), 'checkout', '--quiet', '--detach', revision], check=True, env=e)
```

Its own runner — the tool it wraps — does both hardenings: `tools/registry-check.py:156-165` sets `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL=os.devnull`, and `tools/registry-check.py:787` passes `-c core.hooksPath=/dev/null` to its clone. `registry-replay.py` is strictly weaker on both counts.

Probe — operator global config with `core.hooksPath`, hook writes one absolute path:

```
$ cat hookhome/.gitconfig
[core]
	hooksPath = /tmp/CodePublish-r24/hookhome/hooks
$ python3 … --run --repo …/lanerepo --rev … --out runout3
tool exit=0
$ cat hooklog.txt
HOOK-RAN post-checkout cwd=/tmp/tameshi-registry-replay-zw375fn8/fleet/lanerepo args=0000…0000 291cddd… 1
HOOK-RAN post-checkout cwd=/tmp/tameshi-registry-replay-zw375fn8/fleet/lanerepo args=291cddd… 291cddd… 1
$ ls -la hook-wrote-outside-out.txt
-rw-r--r-- 1 vgpnk vgpnk 0 hook-wrote-outside-out.txt      # <-- written OUTSIDE --out
```

The hook runs **twice** (the clone's initial checkout and the explicit `checkout --detach`), and its write lands outside `--out`. The clone itself is deleted by the `TemporaryDirectory` context manager, but the hook's own write persists.

The stripping half is decisive: a caller that hardens its own environment is **disarmed**, because `env()` deletes the variables before the child sees them.

```
$ HOME=… GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 python3 … --run …
exit=1
$ cat hooklog.txt
HOOK-RAN post-checkout …                                    # still ran
```
Control — the same two variables honoured by plain git do suppress it:
```
$ HOME=hookhome GIT_CONFIG_GLOBAL=/dev/null git clone -q --no-hardlinks lanerepo2 ctl
hooklog.txt: (absent)                                        # suppressed
$ HOME=hookhome git clone -q --no-hardlinks lanerepo2 ctl2
HOOK-RAN post-checkout …                                      # not suppressed
```

So `registry-replay.py` is strictly less isolated than the runner it invokes, and the difference is observable in writes outside `--out`. This extends `corpus/lessons/round-24.md` Erratum M ("The clone omits `core.hooksPath=/dev/null` (CodeRunReplay)") with two facts that line does not state: the tool also **destroys a caller-supplied `GIT_CONFIG_GLOBAL`** hardening, and the resulting hook write demonstrably lands **outside `--out`**, contradicting the row's write-scope cell.

### F5 — LOW-MEDIUM — `--run` stdout is a mixed-format stream; `--json` is honoured only by `--plan`

`--run` prints one progress line per row to stdout (`:176`) and the JSON report last (`:186`), so stdout is not a single JSON document:

```
$ python3 … --run … --out out7 --json > run_json_stdout.txt
synthetic-ok 0 True
{"bundle_sha256": "9c1b1a14…", "finding_ids": [], …}
$ python3 -c "json.loads(open('run_json_stdout.txt').read())"
FAILS: Expecting value: line 1 column 1 (char 0)
```

`--project` stdout *is* a single JSON document, so the two machine-facing modes of the same tool disagree on the stdout contract. The committed evidence carries the mixed shape: `.ufo/evidence/round-24/replay-command.json` records 44 stdout lines, the last being the report object. The SKILL.md row advertises `--json` for `--project` only, which matches usage but leaves the `--run` stdout contract undescribed; `SimplifyReplay.md` already flags that `--json` is a no-op outside `--plan`.

### F6 — LOW — the two refusal paths leave different `--out` states, and a `--selftest` failure shares the refusal exit code

`--project` refusal creates **no** `--out` at all (`publish()` returns at `:117-118` before `mkdir`), whereas `--run` refusal creates it and writes `observations.json` (`:182-183`) before projecting:

```
$ ls -d OUT2 OUT3
ls: cannot access 'OUT2': No such file or directory
ls: cannot access 'OUT3': No such file or directory      # --project refusal: nothing created
$ ls out5
observations.json                                     # --run refusal: out dir + observations created
```

This asymmetry is what lets F1's stale-pair situation arise in `--run` but not in `--project` — and it is undocumented in the row.

---

## Overclaims and misstatements next to the audited row

1. **`SKILL.md:2052` "writes only under `--out`"** — falsified in `--run` mode by F4 (global `post-checkout` hook writes outside `--out`; the tool strips the caller's own `GIT_CONFIG_GLOBAL` hardening and omits the `-c core.hooksPath=/dev/null` its runner uses).
2. **`SKILL.md:2052` "1 refused (RUNNER_NOT_HELD, RUNNER_CLEANUP_FAILED, STREAM_LIMIT)"** — exit 1 also means *an unusable `--out`* (F3a) and *a failing `--selftest`* (F3d). The row's mapping is not injective.
3. **`SKILL.md:2052` "2 invalid or unavailable input, could-not-evaluate"** — the exit-2 report carries no `schema` key and no `rows`/`refused_rows` (F3b); in `--run` mode exit 2 produces **no stdout report at all**, only stderr prose.
4. **`SKILL.md:2052` Persisted-values cell** ("literal fixtures in the tool; frozen requirement/registry digests come from the caller's files") — does not name the four artifacts the tool actually persists under `--out` (`observations.json`, `bundle.json`, `expected.json`, `live-dependent.json`), nor that the report is stdout-only in `--project`/`--run`. `.ufo/evidence/round-24/replay/` contains exactly those four.
5. **Module docstring `tools/registry-replay.py:21` "Writes only under --out."** — same falsification as (1); the docstring does separately disclose that rows run in a clone whose fleet mirror symlinks live siblings (`:23-25`), which covers row writes but not the tool's own git plumbing.
6. **`tools/registry-replay.py:9` "each retained stdout/stderr is bounded by --max-stream-bytes"** — already recorded as Erratum E; the retained `observations.json` is 265,728 bytes with complete streams.

---

## What I checked and found sound

- **The refusal branch itself is correct.** `project()` returns `(1, report, None)` whenever any row has `cleanup_error` (`:86-88`), is not held (`:89-90`), or exceeds the byte bound (`:92-98`), and `publish()` writes nothing on `bundle is None` (`:117-118`). `--project` refusal creates no `--out`. Reproduced for `held=False`, `held=None`, `cleanup_error`, and an over-limit stream: exit 1, no `bundle.json` written.
- **The byte bound is a strict `>` on UTF-8 bytes**, not characters; a stream exactly at the limit publishes (`:96-98`, corroborated by `LabStreamBytes.md`).
- **`--project` publishes bundles that `command-binding.py` refuses** (relative cwd → `INVALID_BUNDLE`; duplicate requirement name → `DUPLICATE_REQUIREMENT`; string `exit` → `INVALID_RECEIPT`). Reproduced all three: the tool exits 0 with `finding_ids: []` and the consumer then exits 2. This is already recorded as `corpus/lessons/round-24.md` Erratum G (`CodeProjectInputs`); `publish()` performs no consumer-side validation of what it writes, so the row's "0 bundle published" does not imply "a bindable bundle was published".
- **The digest pin is correct for the bytes written**: `expected.json`'s `bundle_sha256` is `sha256` of exactly `raw` (`:120-124`), and the retained `.ufo/evidence/round-24/replay/expected.json` pin `4f4240230d4…` matches `sha256sum .ufo/evidence/round-24/replay/bundle.json` = `4f4240230d4…`. The round24 `replay-gate.json` receipt (exit 0, `finding_ids: []`) is consistent with the committed bytes.
- **Usage errors exit 64** (`Parser.error` at `:46-50`): no mode, two mutually exclusive modes, and `--max-stream-bytes 0` (`:263-264`) all confirmed 64.
- **The `--plan` realpath normalisation is correct** for the normal case: `plan-realpath` resolves `alias/peer-shokunin/../lane-shokunin` to the real lane path and reports the real fleet root and siblings.
- **The selftest is hermetic** — its scratch lives under a `TemporaryDirectory` (`:208`) and touches no live path; `registry-replay-selftest` expects `10/10 pass`, matching `len(cases) + 1` (`:199-206`, `:243`).

---

## Residual risk and verification gaps

- **Not re-executed in the lane**: I did not run `tools/registry-replay.py --selftest`, `tools/command-binding.py --selftest`, the registry battery, or `.ufo/evidence/round-24/measure.py` — none of them is in this item's scope and the lane bounds forbid running them in the lane repo. Every runtime claim above comes from a `/tmp` copy of the tool at the audited digest.
- **`--run` against the real 43-row fleet baseline was not replayed**; the `--run` findings (F1 mixed-vintage, F4 hooks) were produced against a synthetic one-row lane, which isolates the mechanism but not the 43-row interaction.
- **The hook in F4 is a caller-configured hook.** It demonstrates that the tool does not prevent arbitrary hook execution; it does not demonstrate that any particular operator has such a hook configured.
- **`TMPDIR` redirection was not treated as a finding.** `registry-replay.py:149` uses `tempfile.TemporaryDirectory`, which honours `TMPDIR`; a probe with `TMPDIR` inside the substrate left the scratch cleaned up (the context manager removed it), so no residue was observed. It remains a documented-write-surface question, not a demonstrated defect.
- **Concurrent runs into one `--out` were not tested.** F1/F2 are demonstrated for the sequential case; a concurrent writer would need its own probe.
- **Erratum overlap.** F1, F3(c), F3(a) and the consumer-refusal cases restate items already carried in `corpus/lessons/round-24.md` Errata G/M (wave-1 seats `CorpusSkill`, `CodeProjectInputs`, `CodeRunReplay`). I have flagged each overlap explicitly and kept only the new observable consequence (self-certifying green consumer verdict, mixed-vintage directory, write outside `--out`).

## Smallest safe correction (one change, four defects)

In `publish()` (`tools/registry-replay.py:116-128`):

1. On refusal (`bundle is None`), **remove** any `bundle.json` / `expected.json` / `live-dependent.json` already present in `out`, and write the report into `out` so the directory records *why* it is empty of a bundle (F1, F6).
2. Write each artifact via `<name>.tmp` + `os.replace`, and write `bundle.json` **last** (F2).
3. Wrap the `mkdir`/write block in `except OSError` and return **exit 2** with a `{"schema": "registry-replay-report-v1", "finding_ids": ["OUTPUT_UNAVAILABLE"], …}` report on stdout — never a bare traceback and never exit 1 (F3a/F3b).
4. Give the exit-2 report the same `schema` key as exit 0/1 in **both** `--project` and `--run` (F3b).

Alongside, in `env()` (`:57-60`) set `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=os.devnull` and pass `-c core.hooksPath=/dev/null` to the clone at `:153`, mirroring `tools/registry-check.py:156-165` and `:787` (F4).

If the wave prefers to land no tool change in round 24, the minimum honest action is to amend `SKILL.md:2052` so the exit map and the write-scope cell say what the tool does — that the row currently overclaims on all three points (F3a, F3b, F4) — and to record F1's consumer-verdict consequence in Erratum G.

---

## Compliance

- Files written outside the lane repo: **this report only** (`.ufo/waves/round-24/w1/CodePublish.md`) plus scratch under `/tmp/CodePublish-r24/` (tool copy, synthetic lane repo, fixtures, probe outputs). Nothing under `/home/vgpnk/Projects/shokunin/` outside `tameshi-shokunin/`.
- No git or jj write command was run in the lane repo or the fleet repo; no sibling lane's jj state or Git index was touched. The lane repo's pre-existing modifications (`LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/knowledge/replay-projection-hardening.md`, `corpus/lessons/round-24.md`, untracked `.ufo/waves/round-24/`) were already present at the start of this seat and were left untouched.
- No registry battery, gate, or selftest was run in `/home/vgpnk/Projects/shokunin/tameshi-shokunin`.
- **Tooling: none installed or updated.** No package manager, download, or service change was needed for this review.
- **Concurrent-seat note.** `git status --porcelain` at this seat's start showed ` M LOG.md`, ` M SCORECARD.md`, ` M corpus/QUALITY.md`, ` M corpus/knowledge/replay-projection-hardening.md`, ` M corpus/lessons/round-24.md`, `?? .ufo/waves/round-24/`; at the end it shows ` M .ufo/evidence/round-21/coldread/ledger.json` plus untracked `round-24/*-B*` evidence and `?? .ufo/waves/round-24/`. The difference is other seats landing their own work in the same lane during this seat; none of it was authored or modified by this seat. This seat's only lane-repo write is `.ufo/waves/round-24/w1/CodePublish.md`.
