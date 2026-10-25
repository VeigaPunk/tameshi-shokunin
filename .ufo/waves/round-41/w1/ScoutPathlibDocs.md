# ScoutPathlibDocs — live fetch of docs.python.org/3/library/pathlib.html vs the round-41 snapshot

Round 41, wave w1. Read-only seat: the lane checkout was not edited, and neither counter was run
(no C1 `calibration/measure.py`, no C2 `census/measure.py`, not even against the base or with
`--control`/`--selftest`/`--rev work`; the deciding run is the L1's).

## Question answered

1. Live fetch status, byte count and sha256 of `https://docs.python.org/3/library/pathlib.html`.
2. Byte equality against `.ufo/evidence/round-41/sources/pathlib.html`.
3. The `Path.write_text` sentence beginning `Open the file pointed to in text mode`, verbatim,
   with its word count, and whether it supports "the receiver expression is the destination path".

## 1–2. Fetch and hash comparison

Exact commands (scratch dir `/tmp/tameshi-r41-scoutpathlib`, nothing written into the lane). The
scratch copy is a convenience only: every number below is re-derivable from the committed
snapshot with the self-contained script in **Appendix A**, so a `/tmp` sweep cannot dangle this
report's evidence:

```
mkdir -p /tmp/tameshi-r41-scoutpathlib
curl -sS -L --max-time 60 -o /tmp/tameshi-r41-scoutpathlib/pathlib.live.html \
  -w 'http_code=%{http_code} size_download=%{size_download} time_total=%{time_total} url=%{url_effective}\n' \
  https://docs.python.org/3/library/pathlib.html
sha256sum /tmp/tameshi-r41-scoutpathlib/pathlib.live.html \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/sources/pathlib.html
wc -c /tmp/tameshi-r41-scoutpathlib/pathlib.live.html
cmp /tmp/tameshi-r41-scoutpathlib/pathlib.live.html \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/sources/pathlib.html
```

Observed output:

```
http_code=200 size_download=271189 time_total=0.018823 url=https://docs.python.org/3/library/pathlib.html
exit=0
0044cae699c55963a41c93f1f6c2a59fbc3a9e1240a4099a7b14c88534e4f093  /tmp/tameshi-r41-scoutpathlib/pathlib.live.html
0044cae699c55963a41c93f1f6c2a59fbc3a9e1240a4099a7b14c88534e4f093  .../.ufo/evidence/round-41/sources/pathlib.html
271189 /tmp/tameshi-r41-scoutpathlib/pathlib.live.html
```

`cmp` printed nothing and exited 0 → byte-identical.

| Field | Value |
|---|---|
| HTTP status | `200` (HTTP/2) |
| Bytes downloaded | `271189` |
| Bytes on disk (live copy) | `271189` |
| `size_download` vs on-disk | equal |
| sha256 (live) | `0044cae699c55963a41c93f1f6c2a59fbc3a9e1240a4099a7b14c88534e4f093` |
| sha256 (snapshot `.ufo/evidence/round-41/sources/pathlib.html`) | `0044cae699c55963a41c93f1f6c2a59fbc3a9e1240a4099a7b14c88534e4f093` |
| **Equal to snapshot?** | **YES — byte-identical, 271189 bytes, 2580 lines** |

The hash reproduces the round-41 context pin for `pathlib.html` (`0044cae6…f093`), so the
snapshot is not stale relative to what the CDN serves now.

A second independent fetch (`-D headers.live.txt`) reproduced the same bytes
(`pathlib.live.html` vs `pathlib.live2.html`: `cmp` silent, exit 0) and gave the provenance
headers:

```
HTTP/2 200
server: nginx
content-type: text/html
last-modified: Sun, 25 Oct 2026 06:21:21 GMT
etag: "6add9fe1-42355"
content-length: 271189
via: 1.1 varnish, 1.1 varnish
date: Sun, 25 Oct 2026 06:38:22 GMT
age: 259
x-cache: HIT, HIT
x-served-by: cache-lga-kjfk8660044-LGA, cache-gig2250083-GIG
```

Header self-consistency (decoded): the nginx etag tail `0x42355` = `271189` = `content-length` =
on-disk size; the etag mtime `0x6add9fe1` = `1792909281` = `2026-10-25T06:21:21Z` = the
`last-modified` value; the request went out over IPv6 (`remote_ip=2a04:4e42:600::223`,
`num_connects=1`). The 18–22 ms `time_total` is a Fastly cache HIT (`x-cache: HIT, HIT`,
`age: 259`), not a local file read — corroborated by `via: … varnish` and by the second fetch
producing the identical byte stream.

## 3. The target sentence

### Location (path:line)

- Authoritative body paragraph: `.ufo/evidence/round-41/sources/pathlib.html:1563-1564` — the
  `<dd><p>` of `id="pathlib.Path.write_text"` (`:1561-1562` is the signature line, which reads
  `Path.write_text(data, encoding=None, errors=None, newline=None)`).
- Doctest attached to the same entry: `:1565-1571`.
- The file contains exactly one occurrence of the string `Open the file pointed to in text mode`
  (`grep -c` = 1), so there is no meta-tag decoy to exclude.

Raw HTML, newlines as in the file:

```html
1561: <dt class="sig sig-object py" id="pathlib.Path.write_text">
1562: <span class="sig-prename descclassname"><span class="pre">Path.</span></span>…<span class="pre">newline</span>…
1563: <dd><p>Open the file pointed to in text mode, write <em>data</em> to it, and close the
1564: file:</p>
1565: <div class="highlight-python3 notranslate"><div class="highlight"><pre><span></span><span class="gp">&gt;&gt;&gt; </span><span class="n">p</span> <span class="o">=</span> <span class="n">Path</span><span class="p">(</span><span class="s1">'my_text_file'</span><span class="p">)</span>
1566: <span class="gp">&gt;&gt;&gt; </span><span class="n">p</span><span class="o">.</span><span class="n">write_text</span><span class="p">(</span><span class="s1">'Text file contents'</span><span class="p">)</span>
1567: <span class="go">18</span>
1568: <span class="gp">&gt;&gt;&gt; </span><span class="n">p</span><span class="o">.</span><span class="n">read_text</span><span class="p">()</span>
1569: <span class="go">'Text file contents'</span>
1570: </pre></div>
```

### Verbatim tag-stripped sentence

> Open the file pointed to in text mode, write data to it, and close the file:

(`<em>` around `data` removed, the source line break between `close the` / `file:` collapsed to a
space, `html.unescape` applied — no other change. The trailing colon is the page's own
punctuation: it introduces the doctest that follows.)

### Word count

`Open`(1) `the`(2) `file`(3) `pointed`(4) `to`(5) `in`(6) `text`(7) `mode,`(8) `write`(9)
`data`(10) `to`(11) `it,`(12) `and`(13) `close`(14) `the`(15) `file:`(16)

- **Word count: 16**, stable across three conventions: whitespace split = 16, `[A-Za-z0-9_']+`
  token regex = 16, whitespace split after dropping the trailing colon = 16.
- If the quote is taken without the source colon (`…, and close the file`) it remains **16**.

### Does it support "the receiver expression is the destination path"?

**SUPPORTS it in substance (the receiver path object is the destination), does NOT support it as
a literal statement about a receiver *expression*.** Breakdown, each claim tagged:

- **OBSERVED**: the sentence itself never names the pointer — it says "the file pointed to" and
  the only argument is `data`. **OBSERVED**: the signature at `:1562` has no path/destination
  parameter at all (`Path.write_text(data, encoding=None, errors=None, newline=None)`), so the
  write target cannot come from the argument list.
- **INFERENCE (tight)**: with no destination parameter, "the file pointed to" must be the path
  object the method is bound to — i.e. the receiver.
- **OBSERVED**: the referent is fixed by sibling methods on the same class, which use the same
  idiom with an explicit pointer — `Path.open` at `:1512`: "Open the file pointed to by the
  path"; `Path.touch` at `:1815`: "Create a file at this given path".
- **OBSERVED**: the attached doctest (`:1565-1569`) binds `p = Path('my_text_file')`, calls
  `p.write_text('Text file contents')` (returns `18`), then `p.read_text()` returns
  `'Text file contents'`. The destination is therefore the path held by the receiver expression
  `p` — a plain variable name, which is exactly the variable-destination case the census must
  resolve, and the docs demonstrate that case directly.
- **OBSERVED**: the word `receiver` occurs **0** times in the 271189-byte page, and the page
  never says "expression" or discusses evaluating one. It says nothing about `os.path.join`,
  `+`, `/`, f-strings or calls in receiver position, so the sentence cannot underwrite any claim
  about *static resolution of a computed receiver* — only about the receiver's path value being
  the destination.
- **Caveat**: this is reference documentation, not the CPython implementation. It establishes
  the API contract the census encodes; it is not source-level proof of what the interpreter does.

So: the documented rule is "the receiver (the `Path` instance the method is called on) is the
destination", and the doctest's receiver is a variable — that is the supported part. The phrase
"the receiver **expression**" overstates the text only if it is read as a claim about resolving
arbitrary expressions; as "the expression you invoke the method on, once evaluated to a path",
the page's own example supports it.

## Cross-record check (outside the question, read-only)

- `corpus/knowledge/r41-variable-destination-writes.md` (sha256
  `be997a8afbe145495fa81b3b7f26b766747af7e612053275e0b9331ebcf56805`, mtime
  `2026-10-25 03:39:29 -0300`) at `:16-17` quotes the same S154 sentence as "(16 words)" and at
  `:12` gives the S153 `ast` sentence as "(15 words)". Both agree with my measurements here (16)
  and with `.ufo/waves/round-41/w1/ScoutAstDocs.md` (15), and its quote omits the trailing colon
  exactly as the count implies. No discrepancy in the current version. (A copy read minutes
  earlier, before 03:39, carried 17 / 16; the file was changed mid-flight and the current
  version is the consistent one — flagging only so the L1 does not score a stale copy.)
- **Path-resolution hazard for the record surfaces (m8), reported not acted on**: at the freeze
  revision `d4ee4e6` all four of `.ufo/evidence/round-41/sources/pathlib.html`,
  `.ufo/evidence/round-41/sources/ast.html`,
  `corpus/knowledge/r41-variable-destination-writes.md` and
  `.ufo/waves/round-41/w1/ScoutAstDocs.md` are **absent from git's object store**
  (`git cat-file -e d4ee4e6:<path>` fails for each; `git status --porcelain` shows them as
  `??`/untracked). `measure.py`'s `resolves()` uses `git cat-file -e REV:path`
  (`.ufo/evidence/round-41/calibration/measure.py:111-116`), and `round41_records()` reads only
  `corpus/lessons/round-41.md` plus the `## Round 41` SCORECARD section and the
  `## 2026-10-25 — round 41` LOG section (`:142-146`); m8 then checks backticked tokens with the
  prefixes `corpus/`, `tools/`, `.ufo/evidence/round-41/`, `.ufo/waves/round-41/`
  (`:181-190`, prefix tuple at `:46-51`), loop at `:238-241`. Consequence: a backticked citation of a snapshot path inside the LOG,
  SCORECARD or lesson round-41 sections counts `m8` unless the measurement revision tracks that
  file. `w1/*.md` reports themselves are outside the m8 scan surface. This report is a w1
  report, so its own citations cannot move m8.

## Confidence

- Status, bytes, sha256, equality: **high** — `sha256sum`, `cmp`, `content-length`, the decoded
  etag and a second independent fetch all agree, and the hash reproduces the context pin.
- Sentence text and 16-word count: **high** — single occurrence in a pinned `path:line`, counted
  three ways; the current knowledge doc independently states 16.
- Support verdict: **high for the factual parts** (0 occurrences of "receiver"; signature has no
  destination parameter; doctest receiver is the variable `p`; sibling `Path.open`/`Path.touch`
  wording). The one **INFERENCE** step (that "the file pointed to" resolves to the bound path
  object) is forced by the signature having no other destination candidate but is still marked as
  inference, not quotation.

## Unresolved gaps

- Bytes come from a CDN cache (`x-cache: HIT, HIT`, `age: 259`), so equality proves the snapshot
  matches what Fastly serves now; an origin-side change between cache fill and fetch is not
  observable from here. `last-modified` is same-day (`2026-10-25T06:21:21Z`), so the window is
  minutes, not a stale pin.
- Whether the measurement revision will track the two snapshots (m8 item above) is the L1's
  decision; not verifiable from this seat.
- Not checked (out of scope): the CPython implementation of `Path.write_text`, and whether any
  planned SOURCES `used-by` value pointing at the untracked knowledge doc is accepted by
  `sources-census.sh validate`.

## Tooling

No installs or upgrades were needed or attempted: system `curl 8.23.0 (x86_64-pc-linux-gnu,
libcurl/8.23.0 OpenSSL/3.6.5)`, system `python3`, coreutils `sha256sum`/`cmp`/`wc`/`stat`/`grep`
sufficed. No pacman transaction attempted (host-wide guard respected).

## Seat integrity

- Lane checkout `/home/vgpnk/Projects/shokunin/tameshi-shokunin`: not edited; the only file
  written by this seat is this report. The `/tmp/tameshi-r41-scoutpathlib/` scratch is a
  convenience copy that any external `/tmp` sweep may delete; no claim in this report depends on
  it, and Appendix A re-derives every figure from the committed snapshot alone.
- No counter invocation of any kind; no git write (only `git rev-parse`, `git ls-files`,
  `git status`, `git cat-file` read-only probes).
- `/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/contract.json` read, not
  modified.

## Appendix A — self-contained re-derivation (no scratch dependency)

Nothing above needs `/tmp` to survive. Run the script below as
`python3 appendix_a.py .ufo/evidence/round-41/sources/pathlib.html` (optionally pass a fetched
copy as a second argument for the byte-equality line); it re-derives the size, line count,
sha256, the sentence anchor, all three word counts and the sibling-wording counts from the
committed snapshot alone.

```python
#!/usr/bin/env python3
"""Self-contained re-derivation for ScoutPathlibDocs (round 41, wave w1).

usage: python3 appendix_a.py SNAPSHOT_HTML [FETCHED_HTML]
Prints size/lines/sha256, the tag-stripped Path.write_text sentence with its
line anchor and three word counts, the sibling-wording counts, and (when a
second path is given) a byte-equality verdict.
"""
import hashlib, html, re, sys

def sha(path):
    with open(path, 'rb') as handle:
        return hashlib.sha256(handle.read()).hexdigest()

def strip(fragment):
    text = html.unescape(re.sub(r'<[^>]+>', '', fragment))
    return re.sub(r'\s+', ' ', text).strip()

path = sys.argv[1]
raw = open(path, encoding='utf-8').read()
print('path      :', path)
print('bytes     :', len(raw.encode()))
print('lines     :', raw.count('\n') + 1)
print('sha256    :', sha(path))

needle = 'Open the file pointed to in text mode'
i = raw.find(needle)
print('occurrences:', raw.count(needle))
line = raw.count('\n', 0, i) + 1
fragment = raw[i:raw.find('</p>', i)]
sentence = strip(fragment)
print('anchor    : %s:%d (raw fragment spans %d-%d)' % (path, line, line, raw.count('\n', 0, raw.find('</p>', i)) + 1))
print('raw       : %r' % fragment)
print('sentence  :', sentence)
print('words split()          :', len(sentence.split()))
print('words [A-Za-z0-9_]+    :', len(re.findall(r"[A-Za-z0-9_']+", sentence)))
print('words split, no colon  :', len(sentence.rstrip(':').split()))
for label, probe in (
    ('receiver occurrences', 'receiver'),
    ('Path.open pointer   ', 'pointed to by the path'),
    ('Path.touch pointer  ', 'Create a file at this given path'),
    ('write_bytes sibling ', 'Open the file pointed to in bytes mode'),
):
    print('%s: %d' % (label, raw.count(probe)))

if len(sys.argv) > 2:
    other = sys.argv[2]
    same = open(other, 'rb').read() == raw.encode()
    print('compare   : %s %s (sha %s)' % (other, 'IDENTICAL' if same else 'DIFFERS', sha(other)))
```

Observed output (run from the lane root against the committed snapshot, with the then-live fetch
as the second argument; the `compare` line is the only part that needs the fetched copy):

```
path      : .ufo/evidence/round-41/sources/pathlib.html
bytes     : 271189
lines     : 2580
sha256    : 0044cae699c55963a41c93f1f6c2a59fbc3a9e1240a4099a7b14c88534e4f093
occurrences: 1
anchor    : .ufo/evidence/round-41/sources/pathlib.html:1563 (raw fragment spans 1563-1564)
raw       : 'Open the file pointed to in text mode, write <em>data</em> to it, and close the\nfile:'
sentence  : Open the file pointed to in text mode, write data to it, and close the file:
words split()          : 16
words [A-Za-z0-9_]+    : 16
words split, no colon  : 16
receiver occurrences: 0
Path.open pointer   : 1
Path.touch pointer  : 1
write_bytes sibling : 1
compare   : /tmp/tameshi-r41-scoutpathlib/pathlib.live.html IDENTICAL (sha 0044cae699c55963a41c93f1f6c2a59fbc3a9e1240a4099a7b14c88534e4f093)
```

Re-checked after the ~03:45 external sweep: `.ufo/evidence/round-41/sources/pathlib.html` is still
`271189` B / `0044cae6…f093` and `.ufo/evidence/round-41/sources/ast.html` still `362029` B /
`183a4f8c…5317`, so the snapshot citations above resolve; only the disposable `/tmp` copy is
outside any repo.

Report: .ufo/waves/round-41/w1/ScoutPathlibDocs.md
