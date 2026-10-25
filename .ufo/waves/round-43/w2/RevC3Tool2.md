# RevC3Tool2 — wave-2 falsification of `tools/staged-id-guard.py`

Seat: reviewer (C3 operability, rewritten guard). Lane: tameshi-shokunin.
Bytes reviewed: `tools/staged-id-guard.py` at the lane checkout (HEAD `bb36f80`), sha256
`2e8f2e891ea20417c141e16871819182d5040c6f33916a435e9454a94d4d6ff2` (matches
`contract.json:frozen_tools`). Registry bytes taken from the freeze blob
(`git show 3aee2c07:corpus/SOURCES.md`), never from the working tree; staged input read
read-only from `/home/vgpnk/Projects/shokuknow/merge/tameshi/SOURCES.append.md`.

**No counter was run at any revision** (`--rev` never passed). Every command below invokes
the guard tool only, in scratch `/tmp/tameshi-r43-w2-RevC3Tool2/`.

Method note: **no `lsp` device is mounted in this seat**, so `references`/`definition`/
`diagnostics` were unavailable; all checks are the tool's own executable behaviour plus
line-cited reading of the source. No installs, no upgrades.

Selftest at the reviewed bytes: `cases=24 failed=0 VERDICT: PASS` (exit 0) — the item's
"23 selftest cases" is off by one; see L5.

---

## Fixture recipe (reproduces every finding)

```bash
S=/tmp/tameshi-r43-w2-RevC3Tool2; rm -rf $S; mkdir -p $S
H='| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|'
R=/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/staged-id-guard.py
# reg.md: S001..S003 ; stg.md: indented S002 (collides) + S004
printf '%s\n| S001 | A — https://example.test/a | docs | A | x | y | z | mined | 2026-01-01 | 180d | — |\n| S002 | B — https://example.test/b | docs | A | x | y | z | mined | 2026-01-01 | 180d | — |\n| S003 | C — https://example.test/c | docs | A | x | y | z | mined | 2026-01-01 | 180d | — |\n' "$H" > $S/reg.md
printf '%s\n  | S002 | G — https://example.test/g | docs | A | x | y | z | queued | 2026-10-24 | 180d | — |\n| S004 | D — https://example.test/d | docs | A | x | y | z | queued | 2026-10-24 | 180d | — |\n' "$H" > $S/stg.md
```

Baseline on those bytes: `collisions=['S002'] cascade=['S004'] next_free=S004 safe_floor=S005`,
verdict `refused`, **exit 1**.

---

## HIGH

### H1 — the document rule is satisfied by incidental punctuation, so the undocumented refusal is bypassed (`staged-id-guard.py:111`)

```python
openable = '/' in head or re.search(r'\.[A-Za-z0-9]{2,6}$', head)
return head if len(head) > 8 and openable else ''
```

The key returned is the **whole prose cell**, which can never equal a registry document, yet
`analyse` treats the row as documented (`unmapped` empty, `refused` false) and
`validate_map` will renumber it.

```bash
printf '%s\n| S002 | see docs/README for the details | docs | A | x | y | z | queued | 2026-10-24 | 180d | — |\n' "$H" > $S/stg-prose.md
python3 -I $R --registry $S/reg.md --staged $S/stg-prose.md --json | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d["unmapped"],d["refused"],d["verdict"])'
echo '{"map":{"S002":"S010"}}' > $S/m-prose.json
python3 -I $R --registry $S/reg.md --staged $S/stg-prose.md --map $S/m-prose.json --json; echo exit=$?
```

Observed: `unmapped=[] refused=False verdict=answered` **exit 0**; with the map
`map_ok=True verdict=admitted` **exit 0**.
Second branch, same defect: `| S002 | see the act.scene |` → `unmapped=[]`, **exit 0**
(`.scene` is 5 chars, inside `{2,6}`).
Expected per the C3 sentence ("refuses a colliding row with no document"): `unmapped=['S002']`,
`refused`, **exit 1**.

### H2 — `URL_RE` truncates at `,` and `;`, fabricating a document identity and deduping away a real document (`:67`, `:105`)

`URL_RE = re.compile(r'https?://[^\s|,;]+')` — both characters are legal RFC 3986
sub-delims. The truncated prefix then matches a *different* registry document, so the guard
tells the operator to **drop** the staged row.

```bash
printf '%s\n| S001 | A — https://example.test/a | docs | A | x | y | z | mined | 2026-01-01 | 180d | — |\n| S002 | B — https://example.test/b | docs | A | x | y | z | mined | 2026-01-01 | 180d | — |\n' "$H" > $S/reg2.md
printf '%s\n| S002 | G — https://example.test/a,b | docs | A | x | y | z | queued | 2026-10-24 | 180d | — |\n' "$H" > $S/stg-comma.md
python3 -I $R --registry $S/reg2.md --staged $S/stg-comma.md --json | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d["held"])'
echo '{"map":{"S002":"S001"}}' > $S/m-comma.json
python3 -I $R --registry $S/reg2.md --staged $S/stg-comma.md --map $S/m-comma.json --json; echo exit=$?
```

Observed: `held={"S002": "S001"}` and the dedupe map **admitted, exit 0**. The staged
document is `…/a,b`, the registry's is `…/a` — two documents; the guard certifies that the
first must not be appended. `;` behaves identically (`https://example.test/a;b` →
`held={"S002": "S001"}`, **exit 0**).
`document_key`'s `rstrip('.,;)]')` (`:105`) is the same class: a Wikipedia-style
`…/Foo_(bar)` and `…/Foo_(bar` collapse to one key.

### H3 — duplicate JSON keys are refused only for *raw* key equality; the `staged:` alias silently drops a decision, and the verdict depends on key order (`:204-206` vs `:404-411`)

`_no_duplicate_keys` compares raw strings; `validate_map` then canonicalises
`staged:S002` → `S002` and does `mapping[bare] = target` (last write wins).

```bash
echo '{"map": {"S002": "S010", "staged:S002": "S004"}}' > $S/m-alias-a.json
echo '{"map": {"staged:S002": "S004", "S002": "S010"}}' > $S/m-alias-b.json
python3 -I $R --registry $S/reg.md --staged $S/stg.md --map $S/m-alias-a.json --json; echo exit=$?
python3 -I $R --registry $S/reg.md --staged $S/stg.md --map $S/m-alias-b.json --json; echo exit=$?
```

Observed: order A → `map_entries=1`, reason `map targets are still staged ids: S004`,
verdict `inadmissible`, **exit 1**; order B, **same two decisions, reordered** →
`map_entries=1`, `map_ok=True`, verdict `admitted`, **exit 0**. The `S010` decision vanished
in A, the `S004` decision in B. True raw duplicates are caught
(`{"map":{…},"map":{…}}` → `setup_refusal`, **exit 2**), so the gap is exactly the alias.
`map_entries`/`map_targets` then under-report (1 instead of 2), and the injectivity check
runs on the collapsed set.

### H4 — `read_text` (`:413-431`) gates on a pre-read `stat` and hashes re-encoded text

**(a) size gate is TOCTOU — reproduced 11/80 runs.** `os.stat` (`:415`) then `open` (`:423`)
re-resolve the path; nothing bounds the bytes actually read.

```bash
python3 - <<'EOF'
import os, threading, subprocess, json, hashlib
S='/tmp/tameshi-r43-w2-RevC3Tool2'; R='/home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/staged-id-guard.py'
small=os.path.join(S,'small.md'); open(small,'w').write('| S001 | A — https://example.test/a | docs | A | x | y | z | m | d | 180d | — |\n')
huge=os.path.join(S,'huge.md'); open(huge,'wb').write(b'#'*(40*1024*1024))
link=os.path.join(S,'swap.md')
try: os.unlink(link)
except FileNotFoundError: pass
os.symlink(small, link); stop=False
def sw():
    i=0
    while not stop:
        t=os.path.join(S,'swap.tmp')
        try: os.symlink(huge if i%2 else small, t); os.replace(t, link)
        except OSError: pass
        i+=1
th=threading.Thread(target=sw); th.start(); hs=hashlib.sha256(open(huge,'rb').read()).hexdigest(); hit=0
try:
    for _ in range(80):
        p=subprocess.run(['python3','-I',R,'--registry',link,'--staged',small,'--json'],capture_output=True)
        for line in p.stdout.decode().splitlines():
            if line.startswith('{'):
                d=json.loads(line)
                if p.returncode==0 and d.get('registry_sha256')==hs: hit+=1
finally:
    stop=True; th.join()
print('reads past the 32MiB gate that exited 0:', hit)
EOF
```

Observed: `reads past the 32MiB gate that exited 0: 11` (of 80). Each such run reports
`registry_sha256` equal to `sha256(40 MiB file)` and **exit 0**, i.e. the 33 554 432-byte cap
in `:420` was not applied to the bytes read. `/proc/self/status` is also accepted (st_size 0,
`S_ISREG` true, **exit 0**), which shows `st_size` is not a bound on the read at all.

**(b) the emitted digest is not the bytes read.** `open(path, encoding='utf-8')` (`:423`) uses
universal newlines, then `:471` hashes `registry_text.encode('utf-8')`.

```bash
printf '%s\n| S002 | G — https://example.test/g | docs | A | x | y | z | q | d | 180d | — |\n' "$H" | sed 's/$/\r/' > $S/stg-crlf.md
python3 -I $R --registry $S/reg.md --staged $S/stg-crlf.md --json | grep -o '"staged_sha256": "[0-9a-f]*"'
sha256sum $S/stg-crlf.md
printf '%s\n| S002 | G — https://example.test/g | docs | A | x | y | z | q | d | 180d | — |\n' "$H" | sed 's/$/\r/' | tr -d '\n' > $S/stg-cr.md   # lone-CR
python3 -I $R --registry $S/reg.md --staged $S/stg-cr.md --json | grep -o '"staged_sha256": "[0-9a-f]*"'
sha256sum $S/stg-cr.md
```

Observed: CRLF file — tool `2d641116…4f29c97f`, `sha256sum` `86fd07d0…2c5fbd8e` (242 bytes on
disk, 235 chars decoded), **exit 0**; lone-CR file — different bytes (`sha256sum`
`32ca362f…aa8ff43`) reporting the **same** `2d641116…4f29c97f`. Two distinct inputs therefore
carry one digest, and no digest matches `sha256sum` of the file. The module docstring's
"`registry_sha256` and `staged_sha256` (the bytes read)" (`:53-54`) is false, so the field
cannot be used to pin which bytes were judged.

---

## MEDIUM

### M1 — the whole-set exemption is gone from the code but still promised by both docstrings (`:32-34`, `:186-187`)

Amendment A10 removed it; the prose was not updated. Module docstring: "disjoint from the
staged set and at or above the safe floor **unless the map covers the whole staged set**";
`validate_map` docstring: "above the safe floor **for a partial map**". No `covers_all`
branch exists — `staged_clash` (`:227`) and `below_floor` (`:230`) are unconditional.

```bash
printf '%s\n| S001 | A — https://example.test/a | docs | A | x | y | z | m | d | 180d | — |\n| S002 | B — https://example.test/b | docs | A | x | y | z | m | d | 180d | — |\n| S010 | J — https://example.test/j | docs | A | x | y | z | m | d | 180d | — |\n' "$H" > $S/reg3.md
echo '{"map":{"S002":"S005","S004":"S006"}}' > $S/m-whole.json
python3 -I $R --registry $S/reg3.md --staged $S/stg.md --map $S/m-whole.json --json; echo exit=$?
```

Observed: reason `partial map targets are below the safe floor S011: S005,S006`, verdict
`inadmissible`, **exit 1** — while the docstring calls this map admissible. The code is the
side that matches the C3 sentence (every fresh target at/above the floor), so the defect is
documentation an operator will act on, plus the misnamed case below.

### M2 — `held`/dedupe are collision-scoped, so a duplicate document at a non-colliding staged id is admitted (`:145-148`)

`held` iterates `collisions` only; `validate_map` likewise. A package row that repeats a
registry document under a free id is invisible.

```bash
printf '%s\n| S001 | A — https://example.test/alpha | docs | A | x | y | z | m | d | 180d | — |\n| S002 | B — https://example.test/b | docs | A | x | y | z | m | d | 180d | — |\n' "$H" > $S/reg4.md
printf '%s\n| S002 | G — https://example.test/g | docs | A | x | y | z | q | d | 180d | — |\n| S050 | A again — https://example.test/alpha | docs | A | x | y | z | q | d | 180d | — |\n' "$H" > $S/stg-dupdoc.md
echo '{"map":{"S002":"S060"}}' > $S/m-dupdoc.json
python3 -I $R --registry $S/reg4.md --staged $S/stg-dupdoc.md --map $S/m-dupdoc.json --json; echo exit=$?
```

Observed: `held={}`, `map_ok=True`, verdict `admitted`, **exit 0** — the guard clears an
append that duplicates `https://example.test/alpha` (registry S001). Same shape for a
staged-internal duplicate: staged `S002` and `S050` both `https://example.test/g` → **exit 0**
admitted, one document entering twice under two ids.

### M3 — one document under two registry ids produces two mutually exclusive verdict fields (`:141`, `:216-222`, `:249-252`)

`registry_docs.setdefault` keeps the first id; `validate_map`'s `same` test accepts *any*
registry id carrying the document, and `map_held_moved` then refuses it.

```bash
printf '%s\n| S001 | A — https://example.test/alpha | docs | A | x | y | z | m | d | 180d | — |\n| S002 | B — https://example.test/b | docs | A | x | y | z | m | d | 180d | — |\n| S004 | A again — https://example.test/alpha | docs | A | x | y | z | m | d | 180d | — |\n' "$H" > $S/reg5.md
printf '%s\n| S002 | example.test/alpha — A3 | docs | A | x | y | z | q | d | 180d | — |\n' "$H" > $S/stg5.md
echo '{"map":{"S002":"S004"}}' > $S/m-two.json
python3 -I $R --registry $S/reg5.md --staged $S/stg5.md --map $S/m-two.json --json; echo exit=$?
```

Observed in one object: `map_dedupe={"S002": "S004"}` (the tool's own "same document, adopt
nothing" classification) **and** `map_held_moved=["S002"]` with reason `map moves a held
document off its registry id: S002 -> S004 (registry S001)`, verdict `inadmissible`,
**exit 1**. The refusal is safe, but a reader cannot tell which classification governs, and
the duplicate registry document itself is never reported as the anomaly.

### M4 — form-insensitivity stops exactly where the claim stops: fragment/query and resolver forms do not join (`:115-121`)

```bash
printf '%s\n| S001 | A — https://example.test/alpha#intro | docs | A | x | y | z | m | d | 180d | — |\n| S002 | B — https://example.test/b | docs | A | x | y | z | m | d | 180d | — |\n' "$H" > $S/reg6.md
printf '%s\n| S002 | A2 — https://example.test/alpha#body | docs | A | x | y | z | q | d | 180d | — |\n' "$H" > $S/stg6.md
python3 -I $R --registry $S/reg6.md --staged $S/stg6.md --json | python3 -c 'import json,sys;print(json.load(sys.stdin)["held"])'
```

Observed: `held={}`, verdict `answered`, **exit 0** (same for `?x=1` vs `?x=2`). The C3
sentence names only scheme/`www.`/case/trailing slash, so this is a capability gap rather
than a claim violation — but a `#intro`/`#body` pair of one document enters twice.
`https://doi.org/10.1234/x` and `doi:10.1234/x` likewise fail to join (`doi.org/…` vs
`doi:…`).

---

## LOW

**L1 — `next_free` is not free, and the numeric fields do not round-trip (`:168`).** Live run
on the freeze registry + staged package prints `next_free=S160`; `S160` is a staged id and is
the first cascade target (`cascade=['S160'…'S166']`). The field name asserts a property the
tool already knows to be false. `staged_max`/`registry_max`/`safe_floor` are `'S%03d'`-rebuilt,
so a package id written `S0004` is reported as `S004`, which appears nowhere in the file.

**L2 — the extractor is anchored to cell 1, one column over from the blindness it fixes
(`:66`).** `|  | S002 | https://example.test/g | docs | A | x | y | z | q | d | 180d | — |`
gives `collisions=[]`, `verdict=answered`, **exit 0** — a real collision invisible because the
id sits in the second cell. `ROW_RE` tolerates 0-3 leading spaces but no cell offset.

**L3 — numeric twins bypass collision detection.** Registry `S004` and staged `S0004` carrying
the same document: `collisions=[]`, `held={}`, **exit 0**, while `id_number` reads both as 4
and `safe_floor` is computed from that arithmetic. String-keyed collision detection plus
numeric flooring is inconsistent for a zero-padded package.

**L4 — exit 2 conflates setup refusal with CLI misuse.** `--bogus` → argparse prints usage and
exits **2**, the same code the docstring reserves for "setup refusal (missing or non-regular
file, oversized file, malformed row, malformed map)"; only the stderr text distinguishes them.

**L5 — selftest accounting.** `--selftest` prints `cases=24` (not 23);
`T5_dedupe_to_registry_id` and `T5_document_form_insensitive` assert the **identical**
expression (`held['S002'] == 'S001'` on the same object), so the suite is 24 calls / 23
distinct assertions. `T12_whole_set_in_range_refused` does not exercise a whole-set map at
all — its map `{'S002':'S003','S004':'S003'}` is non-injective and hits a registry id, and the
assertion accepts `'not injective' or 'safe floor'`, so it passes regardless of any
whole-set logic. The C3 counter's threshold is `MIN_CASES = 13`
(`.ufo/evidence/round-43/guard/measure.py:62`), so the suite could lose eleven cases,
including every map-shape case, and still satisfy the predicate.

---

## Checks that hold (attacked, not broken)

- 0-3-space extraction and the indented-row proof: `collisions=['S002']`,
  `column0_miss=['S002']`, `extractor=0-3space` (T1 shape reproduced independently).
- Cascade refusal: naive map onto staged ids refused (**exit 1**); live
  `cascade=['S160'…'S166']`, every target a staged id.
- Undocumented refusal for a genuinely doc-free row (`nothing here`) → `unmapped=['S002']`,
  `refused`, **exit 1**; the same row decided by a map → `map_undocumented`, **exit 1**.
- Held-moved: `{S002: S010}` on a held row → `map_held_moved`, **exit 1**.
- Malformed shapes → `setup_refusal` **exit 2** with one JSON object, no traceback: missing
  path, 33 MiB registry, `/dev/null`, FIFO (no hang), non-UTF-8, >1 MiB map, int/null/list
  targets, non-S-id key, top-level duplicate key.
- Map logic: non-injective, uncovered collision, self-mapping, registry target, staged target
  → **exit 1**; `staged:` prefix accepted; `{"map": {}}` on a clean package admitted.
- A7's hash-word rule holds: `report-1234567.md` vs `report-7654321.md` → `held={}`.
- Live answer on freeze bytes: `collisions=['S153'…'S159']` (7), `held={S153:S105, S154:S106,
  S159:S155}`, `unmapped=[]`, `cascade` 7, `verdict=refused`, **exit 1**; `registry_docs=100`
  of 114 rows.

## Residual risk / gaps

1. **6 of 114 live registry rows have no document key** — `S031`, `S050`, `S051`, `S082`,
   `S083`, `S085`. Each carries its path *after* the em dash
   (`tameshi's mutation harness … — tools/mutate-and-run.sh`), and `document_key` splits on
   `\s+[—–]\s+` and keeps only the segment **before** the dash (`:106`), so `head` is the prose
   and the row is undocumented. Consequence on live data: those six documents can never be
   held, so a staged row citing `tools/mutate-and-run.sh` would be appended as a duplicate —
   M2's family, reachable from the real registry. No staged row triggers it today (all 103
   staged rows carry a URL).
2. The staged direction of the same rule is untested live: all 103 staged rows carry a URL, so
   `live_unmapped=0` cannot distinguish a correct document rule from H1's permissive one.
3. H4(a) is a race: 11/80 at 40 MiB on this host. It is reproduced, not deterministic, and a
   slow filesystem changes the rate.
4. No semantic cross-check was possible (no `lsp` device): the findings rest on the tool's
   executed behaviour and cited source lines, not on reference/diagnostic data.
