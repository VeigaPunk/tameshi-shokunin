# ScoutAstDocs — live fetch of docs.python.org/3/library/ast.html vs the round-41 snapshot

Round 41, wave w1. Read-only seat: no lane checkout edits, no counters run (neither
C1 `calibration/measure.py` nor C2 `census/measure.py` was invoked; the deciding run is the L1's).

## Question answered

1. Live fetch status, byte count and sha256 of `https://docs.python.org/3/library/ast.html`.
2. Byte equality against `.ufo/evidence/round-41/sources/ast.html`.
3. The tag-stripped sentence beginning `The ast module helps Python applications`, verbatim,
   with word count and the `<= 25 words` verdict.

## 1–2. Fetch and hash comparison

```
mkdir -p /tmp/tameshi-r41-scoutast
curl -sS -L --max-time 60 -o /tmp/tameshi-r41-scoutast/ast.html \
  -w 'http_code=%{http_code}\nsize_download=%{size_download}\ntime_total=%{time_total}\nurl_effective=%{url_effective}\n' \
  https://docs.python.org/3/library/ast.html
sha256sum /tmp/tameshi-r41-scoutast/ast.html \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/sources/ast.html
cmp /tmp/tameshi-r41-scoutast/ast.html \
  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/sources/ast.html
```

Observed output:

```
http_code=200
size_download=362029
time_total=0.026661
url_effective=https://docs.python.org/3/library/ast.html

183a4f8c3d593be4c45dc64406df2622ebc7080cf5ca3c0f0102649e57545317  /tmp/tameshi-r41-scoutast/ast.html
183a4f8c3d593be4c45dc64406df2622ebc7080cf5ca3c0f0102649e57545317  .../.ufo/evidence/round-41/sources/ast.html

cmp: identical
```

| Field | Value |
|---|---|
| HTTP status | `200` (HTTP/2) |
| Bytes downloaded | `362029` |
| Bytes on disk (remote copy) | `362029` |
| `size_download` vs on-disk | equal |
| sha256 (live) | `183a4f8c3d593be4c45dc64406df2622ebc7080cf5ca3c0f0102649e57545317` |
| sha256 (snapshot `.ufo/evidence/round-41/sources/ast.html`) | `183a4f8c3d593be4c45dc64406df2622ebc7080cf5ca3c0f0102649e57545317` |
| **Equal to snapshot?** | **YES — byte-identical (`cmp` silent, both 362029 bytes)** |

Snapshot sha256 corroborates the known fact in the round-41 context
(`183a4f8c…5317`). Snapshot line/byte count: `3338` lines, `362029` bytes.

Response headers (`curl -sSI -L`), for liveness provenance:

```
HTTP/2 200
server: nginx
content-type: text/html
last-modified: Sun, 25 Oct 2026 06:21:21 GMT
etag: "6add9fe1-5862d"
content-length: 362029
x-cache: HIT, HIT
via: 1.1 varnish, 1.1 varnish
date: Sun, 25 Oct 2026 06:38:41 GMT
```

`content-length` agrees with the downloaded byte count; the object was a CDN cache HIT,
`last-modified` is same-day, so the snapshot is not stale relative to what the origin serves.

## 3. The target sentence

### Location (path:line)

- **Body paragraph (authoritative):**
  `.ufo/evidence/round-41/sources/ast.html:243` — the `<p>` opens with
  `<p>The <code class="xref py py-mod docutils literal notranslate"><span class="pre">ast</span></code> module helps Python applications …`.
- Trap for a naive grep: the same words also occur inside `<meta>` tags at
  `.ufo/evidence/round-41/sources/ast.html:11` (`og:description`), `:15` (`og:image:alt`) and
  `:16` (`name="description"`), each truncated with `…`/`...`. Those are metadata, not the
  prose sentence; the citation above is the rendered body text.

### Extraction method

Restricted to the body (`<section id="module-ast">` onward), selected the first `<p>` whose
text contains `module helps Python applications`, removed tags with `<[^>]+>`, applied
`html.unescape`, collapsed whitespace, then took the sentence from
`The ast module helps Python applications` to the first period. The exact script is inlined
verbatim in **Appendix A**, so this evidence does not depend on `/tmp` scratch surviving
(it was also run from `/tmp/tameshi-r41-scoutast/check.py`; that path is a convenience copy,
not the source of record).

Raw HTML of the paragraph (newlines as in the file, line 243 onward):

```html
<p>The <code class="xref py py-mod docutils literal notranslate"><span class="pre">ast</span></code> module helps Python applications to process trees of the Python
abstract syntax grammar.  The abstract syntax itself might change with each
Python release; this module helps to find out programmatically what the current
grammar looks like.</p>
```

### Verbatim tag-stripped sentence

> The ast module helps Python applications to process trees of the Python abstract syntax grammar.

### Word count

`The`(1) `ast`(2) `module`(3) `helps`(4) `Python`(5) `applications`(6) `to`(7) `process`(8)
`trees`(9) `of`(10) `the`(11) `Python`(12) `abstract`(13) `syntax`(14) `grammar.`(15)

- **Word count: 15** (whitespace-split; `grammar.` counted as one token, punctuation attached)
- **`<= 25 words`: YES (15 <= 25)**

The sentence ends at `grammar.`; the following `abstract syntax itself might change …` clause is
a separate sentence and was excluded. A leading `<strong>Source code:</strong> <a …>Lib/ast.py</a>`
line sits in the preceding `<p>`/`<hr>` block, not in this sentence, so it contributes no words.

## Confidence

- Fetch status, byte count, sha256 and equality: **high** — three independent checks agree
  (`sha256sum`, `cmp`, `content-length`), and the live hash reproduces the snapshot pin.
- Sentence text and 15-word count: **high** — derived from the identical byte stream at a pinned
  `path:line`, with the meta-tag decoys explicitly excluded.
- `<= 25` verdict: **high**, and robust to counting convention: even counting hyphen-free
  punctuation or the extra `Source code:` prefix line would stay far below 25.

## Unresolved gaps

- None material to the question. The page is served from a CDN cache (`x-cache: HIT`), so the
  byte identity proves the snapshot matches what the CDN serves now; an origin-side change
  between cache fill and fetch is not observable from here, but the `last-modified` timestamp is
  the same day as the fetch and the pin matches exactly.

## Tooling

No installs or upgrades were needed; `curl` (system), `python3` (system) and coreutils
`sha256sum`/`cmp`/`wc`/`awk` sufficed. No pacman transaction attempted (host-wide guard
respected).

## Seat integrity

- Lane checkout `/home/vgpnk/Projects/shokunin/tameshi-shokunin`: not edited. Only file written
  is this report.
- This report cites **no** `.ufo/waves/round-35/scratch/` path, and no `.ufo/waves/round-41/`
  scratch path. Its only scratch reference was `/tmp/tameshi-r41-scoutast/`, which is not
  load-bearing: the extraction script is inlined in Appendix A and the fetched bytes are pinned
  by sha256 against the surviving snapshot `.ufo/evidence/round-41/sources/ast.html` (verified
  still present, `362029` bytes, `183a4f8c…5317`).
- Advisory correction, verified rather than accepted: the round-35 tree that moved was the
  **mado** lane's, not this lane's. `mado-shokunin/.ufo/waves/round-35/scratch/` was relocated to
  `mado-shokunin/.ufo/waves/round-35/scratch-evidence/` (59 seat dirs; **235** files at
  checkpoint `4efaf63`, **261** tracked files at HEAD after `b632f0b`, `ca870e9`, `1bb25c7`).
  This lane's `.ufo/waves/round-35/` never held a `scratch/` tree at all — it contains
  `residual/`, `dispatch-w1.json`, `dispatch-w2.json`, `spec-w1.json`, `spec-w2.json`,
  `validate-w2.stderr`, `validate-w2.stdout`, `validate.exit`.
- `scratch/` is transient, so it is not an evidence locus: the mado `scratch/` directory was
  re-created at ~03:47 and was already gone again when re-listed minutes later. This report's
  evidence therefore lives in the report body plus the committed snapshot, not in scratch.
- No counter was run against the tip or any revision.

## Appendix A — extraction script, inlined verbatim

```python
import re, html, hashlib

REMOTE = '/tmp/tameshi-r41-scoutast/ast.html'
SAVED  = '/home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-41/sources/ast.html'

def sha(p):
    return hashlib.sha256(open(p,'rb').read()).hexdigest()

for p in (REMOTE, SAVED):
    print(f'{sha(p)}  {p}')

r = open(REMOTE,'rb').read(); s = open(SAVED,'rb').read()
print('byte_identical:', r == s, '| remote_bytes:', len(r), '| saved_bytes:', len(s))

txt = r.decode('utf-8')
body_start = txt.find('<section id="module-ast">')   # body region only: skip <head> meta tags
assert body_start != -1
seg = txt[body_start:]

paras = re.findall(r'<p>.*?</p>', seg, re.S)
target = None
for p in paras:
    stripped = html.unescape(re.sub(r'<[^>]+>', '', p))
    stripped = re.sub(r'\s+', ' ', stripped).strip()
    if 'module helps Python applications' in stripped:
        target = stripped
        break
assert target, 'paragraph not found'
print('PARAGRAPH_TAGSTRIPPED:', target)

i = target.find('The ast module helps Python applications')
assert i != -1, 'phrase not at sentence start'
m = re.match(r'(.+?\.)(?=\s|$)', target[i:])
sentence = m.group(1)
print('SENTENCE:', sentence)
words = sentence.split()
print('WORD_COUNT:', len(words))
print('LE_25:', len(words) <= 25)

for n, line in enumerate(txt.split('\n'), 1):
    if ('The <code class="xref py py-mod docutils literal notranslate"><span class="pre">ast</span>'
            '</code> module helps Python applications') in line:
        print('SAVED_LINE:', n)
```

Run as `python3 <script>` with the fetched file at `REMOTE`; the snapshot may substitute for
both paths since the file is byte-identical. Re-running it against the surviving snapshot today
reproduces `WORD_COUNT: 15` / `LE_25: True` and `SAVED_LINE: 243` without any network access.

Post-relocation reproduction (both variants executed after the ~03:45 mado-lane scratch
relocation, extracting this very code block from the report): the as-inlined form with `/tmp`
still present, and a snapshot-only variant with `REMOTE` set to
`.ufo/evidence/round-41/sources/ast.html`, each printed
`byte_identical: True`, `SENTENCE: The ast module helps Python applications … grammar.`,
`WORD_COUNT: 15`, `LE_25: True`, `SAVED_LINE: 243`. Deleting `/tmp/tameshi-r41-scoutast/`
therefore cannot void this report's evidence.

Report: .ufo/waves/round-41/w1/ScoutAstDocs.md
