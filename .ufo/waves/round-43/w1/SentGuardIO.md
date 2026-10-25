# SentGuardIO — input/output safety review of `tools/staged-id-guard.py`

Seat: L1Tameshi43.SentGuardIO (sentinel). Milestone: guard input/output safety. Surface assigned:
write paths, subprocess, eval/exec, `--map` path handling, untrusted-map JSON, hostile registry /
staged content (write / hang / leak).

**Verdict: no write path, no subprocess, no eval/exec, no network — attested (§1). The `--map`
admission path is unsound in three independent ways (§S2, §S3, §S4) and, on the frozen bytes, its
multi-entry bug makes the C3 counter's `safe_admitted=1` unreachable (§S1). The frozen tool has also
been modified in place by a wave-1 seat, so the worktree and the artifact the counter measures are
no longer the same bytes (§S0).**

Read-only: no lane file was modified by this seat. Scratch under `/tmp/tameshi-r43-SentGuardIO-rev`
(deleted at the end). No tool installed (none needed).

---

## S0 — CRITICAL (provenance / chain of custody): the frozen tool is modified in the worktree; the counter still measures the frozen blob

`tools/staged-id-guard.py` in the working tree no longer hashes to the contract's `tool_sha256`:

```
$ sha256sum tools/staged-id-guard.py
efa5f129cba312c26c1fc453e6cd7f783efafeecccfac791e8c03d3d290f9b3c  tools/staged-id-guard.py
$ git show 17f6ef0c…:tools/staged-id-guard.py | sha256sum
8140945a816873562eee8bcc6862d5e098f95b8083b4760b087812568f97b762  -     (= contract tool_sha256)
$ git status --short
 M tools/staged-id-guard.py
```

The diff (7 insertions, 1 deletion) is an unauthorised post-freeze edit that fixes §S1 and adds a
selftest case; the added comment names the author: *“wave-1 mutation-tester MutC3Selftest, round
43”*. The frozen path was supposed to be exactly what the freeze committed.

Why it matters, and why it is not harmless:
* the C3 counter materialises the tool **from REV** (`guard/measure.py:153-176`:
  `show(lane, rev, TOOL_REL)` → written into a temp dir), so `tool_sha_ok=1` and the executed bytes
  both come from the frozen blob. The deciding run will therefore measure the **buggy** tool while
  the worktree reads green — a green worktree that cannot be cited as evidence about the frozen
  artifact;
* every seat that ran the worktree path (this review's first pass included) was testing different
  bytes than the frozen tool, and any seat that diffs the worktree gets a different `--map`
  behaviour (see §S1: `rc 1 inadmissible` frozen, `rc 0 admitted` worktree);
* if anyone commits the worktree, REV changes and `tool_sha_ok` drops to 0 — the claim fails
  loudly rather than silently, but the wave's evidence is already mixed.

Smallest remediation: restore the frozen bytes in the worktree (`git checkout -- tools/…` is the
owner's call, not this seat's), or record the edit as a contract amendment and re-freeze **before**
the deciding run. No seat should leave a frozen path dirty during a wave.

---

## 1. Surface inventory — the part that is clean

| asked surface | result | evidence (frozen blob line numbers) |
|---|---|---|
| write paths | **none** | only `open(path, encoding='utf-8')` in `read()`, `:321`, read mode; every other output is `print()` to stdout/stderr. |
| subprocess | **none** | no `subprocess` / `os.system` / `os.exec*` / `os.spawn*` / `shutil`. |
| eval/exec | **none** | no `eval`, `exec`, `compile`, `__import__`, `pickle`, `yaml`. |
| network / ctypes | **none** | no `socket`, `urllib`, `http`, `ctypes`. |
| traversal from the map JSON | **none** | `:165` uses only `map_doc['map']`; the map's own `staged`/`registry` path keys are never opened. |
| `--map` CLI path | by design: caller-supplied, same privilege | `read(args.map)` at `:346`; no privilege boundary crossed. |

Runtime attestation, PEP 578 audit hook (`open` mode+flags, `subprocess.Popen`, `exec`, `compile`,
`socket.__new__`, `ctypes.dlopen`) around `main()` with the full arg set:

```
total open events=92  write-opens=0  other-events=83   (all import machinery)
opened: the tool itself, /usr/lib/python3.14/**.py[c], then reg.md, stg.md, m_one.json only
```

`import os` at `:50` is unused (`grep -c 'os\.'` → 0). **A hostile registry or staged file cannot
make this tool write, and cannot exfiltrate its content**: refusal and result messages echo only
`S`-ids, line numbers, and caller-supplied paths. What hostile content *can* do is steer the verdict
— that is the rest of this report. All line numbers below are the frozen blob; the dirty worktree is
`+3` for lines after `:172`.

---

## S1 — CRITICAL (operability): on the frozen bytes every map with ≥2 entries is inadmissible, so C3's `safe_admitted=1` cannot be reached

`staged-id-guard.py:172` (frozen; fixed at worktree `:175`)

```python
if not re.fullmatch(r'S\d{3,}', ''.join(targets) or 'S0'):
    reasons.append('map has a target that is not an S-id')
```

`join(targets)` concatenates *all* values, then fullmatches a single-id pattern. Two entries become
`S010S011`, never match, and append a bogus reason; `map_ok = not reasons` (`:217`) then forces
`inadmissible` + exit 1. The check is correct only for the single-entry map the selftest uses.

Two-collision probe on the **frozen blob**:

```
$ python3 -I frozen-guard.py --registry reg2.md --staged stg2.md \
      --map <(echo '{"map": {"S002": "S010", "S003": "S011"}}') --json
verdict=inadmissible map_ok=False map_reasons=['map has a target that is not an S-id'] map_entries=2
# same file, worktree:  verdict=admitted map_ok=True map_reasons=[]
```

Counter-exact probe — registry at REV, live staged package, `safe_map` reconstructed exactly as
`guard/measure.py:205-221` builds it (`own_held` + sequential `S%03d` from `safe_floor`):

```
registry 17f6ef0/corpus/SOURCES.md (113 rows) + …/shokuknow/merge/tameshi/SOURCES.append.md (103 rows)
collisions=6  held=2  cascade=6  safe_map entries=6
frozen blob   -> rc=1 verdict=inadmissible reasons=['map has a target that is not an S-id']
worktree patched -> rc=0 verdict=admitted reasons=[]
```

Impact: `guard/measure.py:222` sets `safe_admitted=1` only for `rc == 0 and verdict == 'admitted'`,
and `:236` requires it for `C3_R43_PASS`. With the frozen blob that conjunct is **unsatisfiable**:
C3 as declared cannot measure true, independent of anything a seat does with fixtures.
Second-order: `naive_map_refused=1` (`:209`) is satisfied *spuriously* — the 6-entry naive map is
refused for the same bogus reason, not because of the cascade:

```
naive verdict=inadmissible
 reasons=['map has a target that is not an S-id',
          'map targets are still staged ids: S160,…,S166']
```

So C3's two discriminators collapse to one, and that one is red. Smallest remediation (this is the
worktree's fix, and it is correct):

```python
if not all(isinstance(t, str) and re.fullmatch(r'S\d{3,}', t) for t in targets):
```

Because the counter pins `tool_sha256`, the fix only reaches C3 through an amendment + re-freeze
(§S0). As it stands, the honest reading is: the no-map half of the guard works (the 0-3-space
extractor and the cascade detection are real), the map-admission half is dead on the frozen bytes.

---

## S2 — HIGH (integrity): `--map` ignores `held`; a duplicate document is admitted under a fresh id

`validate_map` computes `base = analyse(...)` at `:162` and then never consults `base['held']`
(`:177-194`). The no-map path says “dedupe to the registry id, don't append” (`:118-122`); the map
path lets the same row be re-pointed to a fresh id above the floor.

```
# staged row carries the same URL as registry S001
frozen,  no-map: verdict=answered held={'S002': 'S001'}
frozen,  --map {"S002":"S010"}: verdict=admitted map_ok=True map_reasons=[] map_dedupe={}
worktree --map {"S002":"S010"}: verdict=admitted map_ok=True map_reasons=[] map_dedupe={}   (same)
```

Impact: exit 0 / `admitted` on a package whose only correct outcome is “adopt nothing” → the
consumer appends a second registry row for a document the registry already holds, breaking the
append-only-keyed-by-document invariant the tool's own docstring cites. Smallest remediation, inside
the per-entry loop (`:177`):

```python
if staged_id in base['held'] and target != base['held'][staged_id]:
    reasons.append('map re-points a held document instead of deduping: %s' % staged_id)
    continue
```

## S3 — HIGH (integrity): `--map` ignores `unmapped`; the “arithmetic” refusal is bypassed by supplying a map

Same site. The no-map path refuses a colliding row with no document key precisely because “a renumber
decision that is not tied to a document is arithmetic” (`:17-20`, `:118-122`). `validate_map` never
reads `base['unmapped']`, so any arbitrary target is accepted for such a row.

```
# staged source cell "nothing here" -> document_key == ''
frozen,  no-map: verdict=refused unmapped=['S002'] refused=True
frozen,  --map {"S002":"S010"}: verdict=admitted map_ok=True   (same object also says refused=True)
```

Impact: the C3 claim's “admission only of a by-document map” is not enforced on the admission path.
The emitted object is also self-contradictory (`"refused": true` beside `"verdict": "admitted"`), so
a consumer reading `refused` and one reading `verdict` disagree about the same run. Remediation:
reject a mapping for any sid in `base['unmapped']`, and drop/normalise `result['refused']` when
`verdict == 'admitted'`.

## S4 — MEDIUM (integrity): document key is form-sensitive; URL vs bare host-path never matches

`document_key:86-98`. A URL is taken verbatim (`:88-91`); a non-URL source is reduced to a path-like
head (`:92-98`). The same document as `https://example.test/alpha` in the registry and
`example.test/alpha — Alpha` in the package yields two different keys, `held` stays empty, and the
map is admitted.

```
frozen no-map: verdict=answered held={} unmapped=[]
frozen --map {"S002":"S010"}: verdict=admitted map_ok=True map_dedupe={}
```

Impact: identical end state to §S2 (duplicate document appended), reached without any trick — only a
different citation style. Remediation: canonicalise before comparison (strip `^https?://`, lowercase
the host, strip a trailing `/`).

## S5 — MEDIUM (availability / contract): uncaught exceptions exit 1 — the documented “inadmissible” code — with no JSON

`read()` catches only `OSError` (`:323`); `main()` catches only `Refusal` (`:354`). Six untrusted
inputs escape as tracebacks and take exit code 1, which the docstring (`:32-34`) defines as “the map
is not admissible”; under `--json` stdout is empty, so a JSON consumer gets nothing.

| input | site | exception | rc |
|---|---|---|---|
| map key not an S-id, `{"map":{"ZZZ":"S100"}}` | sort key `id_number` at `:177` → `:102` | `ValueError` | 1 |
| integer / null target | `''.join` at `:172` | `TypeError` | 1 |
| list / dict target | `set(targets)` at `:170` | `TypeError` (unhashable) | 1 |
| 100 000-deep nested array | `json.loads` at `:346` | `RecursionError: Stack overflow` | 1 |
| invalid UTF-8 in registry/staged | `handle.read()` at `:322` | `UnicodeDecodeError` | 1 |
| `S` + 5000 digits (CPython int limit) in registry **or** as a map key | `int(sid[1:])` at `:102` | `ValueError: Exceeds the limit (4300 digits)` | 1 |

```
huge-registry-id rc=1 stdout='' stderr_tail='ValueError: Exceeds the limit (4300 digits) for
 integer string conversion: value has 5000 digits; ...'
m_deep.json    rc=1 stdout='' stderr_tail='RecursionError: Stack overflow (used 8144 kB) ...'
stg_badutf8.md rc=1 stdout='' stderr_tail="UnicodeDecodeError: ... can't decode byte 0xff ..."
```

Impact: a hostile map or registry makes a setup error indistinguishable from a real verdict at the
exit-code level the docstring publishes. The C3 counter is not fooled today (it additionally requires
`verdict`, `measure.py:209,222`), so this is contract debt, not a live counter bypass — but it is the
difference between “the guard answered no” and “the guard fell over”. Remediation: add
`except (ValueError, TypeError, UnicodeDecodeError, RecursionError) as exc:` beside `except Refusal`
(`:354`) and route it through the same `setup_refusal` / exit 2 body.

## S6 — LOW-MEDIUM (integrity, safe direction): hex-stripping and `rstrip` collapse distinct documents

`HEXISH.sub('', head)` at `:94` deletes any 7-40 character lowercase-hex run, so
`report-1234567.md` and `report-7654321.md` both become `report-.md`; `rstrip('.,;)]')` at `:91`
folds `…/alpha)` onto `…/alpha`.

```
frozen no-map: verdict=answered held={'S002': 'S001'}   # two distinct documents reported as held
```

Impact is under-adoption (a package row silently never adopted), not a false append. Remediation:
drop the hex substitution or strip only a 40-char hex token; document the `rstrip`.

## S7 — LOW (availability): unbounded read of a caller/package-controlled path

`read()` at `:319-324` slurps the whole file, follows symlinks, has no size cap and no timeout.

```
$ mkfifo fifo_reg; timeout 3 python3 -I frozen-guard.py --registry fifo_reg --staged stg.md --json
rc=124          # blocked in open()/read(); the tool has no internal deadline
```

`/dev/zero` or a multi-GB file is an unbounded memory read. Relevance: the staged path the guard is
built to consume lives **outside the lane** (`guard/measure.py:56`), so its size is set by another
repository. The counter's `subprocess.run(timeout=120)` contains this; the tool does not contain
itself. Remediation: `os.open(..., O_NOFOLLOW|O_NONBLOCK)` + `os.fstat` size cap, read at most N MiB.

## S8 — LOW (integrity): duplicate JSON object keys are silently last-wins

`json.loads` at `:346`: `{"map":{"S002":"S010","S002":"S011"}}` becomes a one-entry map
(`map_entries=1`, `verdict=admitted`). A hand-built map can carry a second, invisible target.
Remediation: `object_pairs_hook` that raises `Refusal` on a duplicate key.

## S9 — INFO: no traversal from untrusted JSON; path handling is caller-supplied only

`{"map": {…}, "staged": "/etc/shadow", "registry": "/etc/passwd"}` is accepted with rc=0 and the
extra keys are never opened (`:165`). Good. The `--map` CLI path is opened with the caller's
privileges by design; no privilege boundary is crossed, so it is not a traversal finding.

## S10 — INFO: the tool does not enforce its own `-I` requirement

The frozen interface says `python3 -I` (`:37-41`). Without `-I`, `PYTHONPATH` precedes the stdlib and
a same-named `json.py` beside the tool shadows the real module. Out of scope to police from inside
the tool; both the counter and the interface text use `-I`, so this is a note.

---

## Selftest blindness (calibration relevance)

```
$ python3 -I frozen-guard.py --selftest
STAGED_ID_GUARD_SELFTEST: cases=13 failed=0
VERDICT: PASS        (rc=0)
```

13/13 green and blind to §S1-§S3: the only admitted map is single-entry (`good`, `:286`); the only
multi-entry map (`dup`, `:305`) expects refusal for non-injectivity and passes for the wrong reason
once the bogus reason is appended; there is no case for an undocumented row, no case for a held row
mapped to a fresh id, no non-string target, and no multi-entry *positive* case. A green suite is
therefore consistent with a working admission path and with a dead one — exactly the overfit C3 is
supposed to expose. (The dirty worktree adds `T4_multi_entry_map_admitted`, which is why it reads
green; that case exists only in edited bytes.)

---

## Bottom line for C3

* **Write / subprocess / eval / leak: clean.** Hostile content cannot write, exec, or exfiltrate;
  the only sinks are stdout/stderr, and those echo ids and paths, never file content.
* **Admission is weaker than the tool's own no-map verdict** (§S2 held, §S3 unmapped) and
  form-sensitive on the document key (§S4): it can admit a duplicate-document append.
* **On the frozen bytes, `safe_admitted=1` is unreachable** (§S1) because the counter's own 6-entry
  safe map is rejected by `''.join(targets)`; `naive_map_refused=1` passes for the same spurious
  reason. As frozen, `C3_R43_PASS` cannot be true.
* **The frozen path was edited after the freeze** (§S0). The counter still runs the frozen blob, so
  the worktree's fix does not reach the measurement, and any evidence gathered from the worktree —
  including this review's first pass — is evidence about different bytes.

---

## Commands run (representative)

```
sha256sum tools/staged-id-guard.py ; git show 17f6ef0…:tools/staged-id-guard.py | sha256sum
git -C <lane> show 17f6ef0…:tools/staged-id-guard.py > /tmp/…/frozen-guard.py
python3 -I frozen-guard.py --selftest
python3 -I frozen-guard.py --registry reg2.md --staged stg2.md --map m_multi.json --json
python3 -I frozen-guard.py --registry reg2.md --staged stg_undoc.md --map m_one.json --json
python3 -I frozen-guard.py --registry reg2.md --staged stg_held.md  --map m_one.json --json
python3 -I frozen-guard.py --registry <REV:corpus/SOURCES.md> --staged <shokuknow SOURCES.append.md> --json
python3 -I frozen-guard.py --registry … --staged … --map safe2.json --json     # counter-exact safe map
printf '…0xff…' > stg_badutf8.md ; python3 -I frozen-guard.py --registry … --staged stg_badutf8.md --json
mkfifo fifo_reg ; timeout 3 python3 -I frozen-guard.py --registry fifo_reg …
python3 -c "print('['*100000+']'*100000)" > m_deep.json ; … --map m_deep.json
# PEP 578 audit hook around main(): 'open' / 'subprocess.Popen' / 'exec' / 'socket.__new__'
```

Tooling: none installed or upgraded (Python 3.14.8 present; pacman untouched).
