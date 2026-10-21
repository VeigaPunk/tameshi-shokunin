# SourceS065: S065 re-opened for round-19 C1 (advisory)

Seat: TameshiR19-2.SourceS065 (scout, w1 BUILD advisory). Date: 2026-10-21.
Read-only seat. This seat changed no registry row, production file, or Git/JJ state. It installed or updated no tool. It ran no lane selftest, build, lint or formatter.
Scratch: `/tmp/tameshi-r19-S065/` (disposable).
Advisory finding. It closes nothing.

## Object

- Row `corpus/SOURCES.md:74` S065: Python json docs, https://docs.python.org/3/library/json.html
  - kind `docs`, tier `A`, status `mined`, opened 2026-10-20, recheck `on-release`.
  - used-by: `corpus/knowledge/guard-kill-closure.md`.
  - Anchor: §Standard Compliance and Interoperability › Infinite and NaN Number Values, and the json.load() parameter `parse_constant`. The row marks itself "version-coupled; no commit pin".
- The row line is byte-unchanged through round 19. `grep '^| S065' | sha256sum` gives `c48d0ed8c2e95aa02cbd2f925b118ce7fc4c20985cdd64894033e8aa67526260` at:
  - baseline `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`;
  - delivered `21e79329f8bdcf01a62be63b3e46db4a7de6b6f9`;
  - the worktree;
  - and in the round-18 receipt (`.ufo/waves/round-18/w2/ReopenS065.md:66`).
- Round-19 use today:
  - `corpus/lessons/round-19.md:27-40` sources C1 with S049 only. It says other openings are "advisory readings, not additional registry admissions".
  - No round-19 claim cites S065. A search of `round-19.md`, `QUALITY.md`, `contract.json` and `frozen-runs.json` found zero round-19 hits for `parse_constant`, NaN, non-finite or duplicate-key.

## Re-open (observed 2026-10-21)

- **Main page.** `curl -sSL https://docs.python.org/3/library/json.html` at 2026-10-21T05:49:23Z:
  - HTTP 200, 115104 B;
  - sha256 `312118060243dfcc79dfa0872810a618f342b467b0e2422a0cc1528c6f661880`;
  - title "json — JSON encoder and decoder — Python 3.15.0 documentation";
  - footer "Last updated on Oct 21, 2026 (01:57 UTC)."
- **Versioned copy.** `https://docs.python.org/3.15/library/json.html` is byte-identical (`cmp` exit 0).
- **Drift check against round 18.** I compared today's page with the round-18 w2 fetch (`/tmp/tameshi-r18w2-ReopenS065-1PITAC/json.html`, sha256 `c766c456…`, recorded at `ReopenS065.md:15`).
  - `diff` shows one changed line, :1201, the footer only: "Oct 20, 2026 (20:06 UTC)" became "Oct 21, 2026 (01:57 UTC)".
  - The content did not drift.
  - The page hash changes with every docs rebuild, so it is not a durable pin.
- **Host-version page.** `https://docs.python.org/3.14/library/json.html` is titled "Python 3.14.8 documentation", which matches the host `python3 --version` 3.14.8. Its sha256 is `ef5c5df8…`. It carries the same four sentences, each once (probe below).
- **Durable pin.** CPython `Doc/library/json.rst` @ `4cdf2e454d4f97c1e8b3d4698ff7f8e02f2c7f03`.
  - This is the latest commit touching that path on branch 3.15, per the GitHub commits API. Commit date 2026-09-21T12:57:17Z, subject "[3.15] gh-157571: Move json sort note from dumps to dump".
  - File sha256 `64429e9269df70c75e66d3588f22d59412fe1b93019c4bcf70075a91bbdc7622`.
  - Relevant lines: `.. function:: load` (:266), `:param parse_constant:` (:330-334), §Infinite and NaN Number Values (:684-689), deserializer sentence (:702-704).

## Quotes (each ≤25 words, accessed 2026-10-21)

- **Q1** (the mechanism round 19 uses). Location: §Basic Usage › json.load() › Parameters › parse_constant (`#json.load`; rst :331-332). 17 words:
  > "If set, a function that is called with one of the following strings: '-Infinity', 'Infinity', or 'NaN'."
- **Q2** (the row's teaches). Location: §Standard Compliance and Interoperability › Infinite and NaN Number Values (rst :688-689); inline code markup removed. 20 words:
  > "by default, this module accepts and outputs Infinity, -Infinity, and NaN as if they were valid JSON number literal values"
  - This matches the round-18 Gate quote (`corpus/lessons/round-18.md:34`). It is still present, so S065 has not drifted.
  - That satisfies S065's share of the recheck at `guard-kill-closure.md:3`.

## Tier and limits

Tier A, scoped. The scope is official CPython documentation of the json module's own decoder behaviour: default acceptance of the three literals, and the `parse_constant` hook. Limits:

- **L1. Documentation only.** S065 states API semantics. It does not prove that any round-19 receipt was parsed strictly, and it does not prove any historical run.
- **L2. The hook covers three literal spellings only.** The page says nothing about numerals that overflow.
  - Probe on Python 3.14.8: `json.loads('1e400', parse_constant=<raises>)` returns `inf` (a float) and the hook never runs (`hook_saw=[]`).
  - So S065 cannot support the claim "parse_constant rejects every non-finite value".
  - The landed `tools/registry-check.py` at `921ef807…` uses both the hook (:356) and `math.isfinite` (:245). That is consistent with this limit.
- **L3. Version coupling.**
  - The `/3/` alias moves on each release.
  - The round-19 receipts do not record which interpreter produced them: searching `after-21e7932.json` for `python|version|interpreter|executable` gives 0 matches. [UNKNOWN] I cannot tell which interpreter parsed them; [INFERENCE] it was probably the host 3.14.8.
  - The 3.14 page carries the same sentences.
- **L4. Scope boundary.** The same URL also documents duplicate names (§Repeated Names Within an Object; `object_pairs_hook`). S065's scope and anchor exclude that section. Citing S065 for the ruler's duplicate-key refusal would overstate the row.
- **L5. RFC reference.** The page names RFC 7159. The authority for the JSON grammar is S066 (RFC 8259).

## Fit to round-19 C1

- **Where S065 would apply.** The ruler `.ufo/evidence/round-19/measure.py` has sha256 `c538c33d…e18e`, equal to `ruler_sha256` in `before.json` and `after-21e7932.json`.
  - Every receipt and snapshot goes through `strict_json` (:41-51): `json.loads(raw, object_pairs_hook=unique, parse_constant=constant)`, where `constant` raises `ValueError('nonfinite-json')`.
  - Q1 is the API contract for that call.
- **Where S065 does not apply.**
  - The R18-1…R18-5 corrections are metadata and receipt hygiene: the stale line-2 header, the stale S008 status line, five deleted lines versus four, the mis-invoked witness receipt, and the missing `4b7c682` receipt.
  - S065 bears on none of them, and not on the 0/5 → 5/5 count.
  - [INFERENCE, code read] The numeric fields the predicates read are already gated by `type(x) is int` (:66, :94, :131-135). NaN or inf in those fields therefore fails closed with or without the hook.
- **Failure-capability caution.** [INFERENCE, code read; not executed, because lane selftests were out of bounds]
  - The selftest fixture `nonfinite` is `{"exit":NaN}` (:193-194). It has no `argv` or `revision`, so `receipt()` returns None at :65 even without the hook. R18-4 opens either way, so deleting `parse_constant=constant` would survive this case.
  - The `duplicate-key` fixture (:191-192) is non-discriminating against `unique` for the same reason.
  - Discriminating fixtures would be:
    - the pristine witness receipt plus an extra key `"x": NaN` (R18-4 opens only with the hook);
    - the pristine receipt with `"exit": 64` followed by `"exit": 0` (R18-4 opens only with `unique`).
  - Round 19 currently claims neither refusal, so nothing is overstated today.

## Recommendation

- **USE: narrow, tier A, advisory.** Use S065 only as API-semantics support, and only if round-19 text says its ruler refuses NaN, Infinity and -Infinity literals through `parse_constant`. In that case:
  - L1 appends `corpus/lessons/round-19.md` to S065 `used-by` as an append-only registry change;
  - the receipt-loader application is labelled as lane design, not page content;
  - a discriminating fixture pins the claim.
- **REJECT as support for:**
  - the C1 count;
  - any of R18-1…R18-5;
  - "parse_constant rejects all non-finite values" (L2);
  - duplicate-key refusal (L4);
  - historical execution (L1).
- This seat recommends no registry change. The current lesson's S049-only sourcing is consistent with this reading.

## Observation / inference / unknown

- **Observed:**
  - the row hash is unchanged at both C1 revisions;
  - Q1 and Q2 are present on the /3/, /3.15/ and /3.14/ pages and in the pinned rst;
  - the only change since 2026-10-20 is the footer line;
  - the probe outputs below;
  - the ruler sha256 matches the receipts;
  - the landed registry-check uses both the hook and `isfinite`.
- **Inference:**
  - the int type gates make the hook redundant for the fields the ruler checks;
  - the `nonfinite` and `duplicate-key` selftest cases are non-discriminating;
  - the receipts were parsed by host 3.14.8.
- **Unknown:**
  - which interpreter produced the round-19 receipts;
  - whether a later 3.15.x docs release rewords Q1 or Q2 (the `on-release` recheck covers this).

## Receipts (commands → outcome)

- `curl -sSL -D headers.txt -o json.html -w 'http=%{http_code} size=%{size_download} url=%{url_effective}' https://docs.python.org/3/library/json.html` → `http=200 size=115104`; `sha256sum` → `3121180602…1880`.
- `curl … /3.15/library/json.html`; `cmp json.html json-3.15.html` → exit 0.
- `curl … /3.14/library/json.html` → `http=200 size=112740`, sha256 `ef5c5df861337417e763372133d110e88fdce8913a131c42cb3403549a29c620`.
- `diff /tmp/tameshi-r18w2-ReopenS065-1PITAC/json.html /tmp/tameshi-r19-S065/json.html` → `1201c1201` (footer only).
- `curl 'https://api.github.com/repos/python/cpython/commits?sha=3.15&path=Doc/library/json.rst&per_page=1'` → `4cdf2e45…`.
- `curl https://raw.githubusercontent.com/python/cpython/4cdf2e45…/Doc/library/json.rst` → 31963 B, sha256 `64429e92…7622`.
- `python3 -I -B /tmp/tameshi-r19-S065/probe.py json.html json-3.15.html json-3.14.html` → exit 0. Output:
  - each page: nan-section count=1 (20 words); parse_constant-load-param count=1 (17 words); parse_constant-raise count=2; deserializer-hook count=1;
  - interpreter 3.14.8;
  - `'NaN'`, `'Infinity'`, `'-Infinity'`, `'{"exit": NaN}'` → `ValueError(nonfinite-json)`, with the hook seeing each literal;
  - `'1e400'` → `inf` (float), hook saw `[]`; `'{"exit": 1e400}'` → `{'exit': inf}`, hook saw `[]`.
- `sha256sum .ufo/evidence/round-19/measure.py` → `c538c33d6d80c9299183b6ff08a21da6f557fa66f99712f38820fdce1473e18e`, equal to `ruler_sha256` in `before.json` and `after-21e7932.json`.
- `env -i HOME=/tmp PATH=/usr/bin:/bin GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 git show <rev>:corpus/SOURCES.md | grep '^| S065' | sha256sum`, for both C1 revisions → `c48d0ed8…6260`. This is a read only; no Git state changed.
- The same scrubbed `git show 921ef807…:tools/registry-check.py`, searched for `parse_constant`, `isfinite` and `_reject_json_constant` → :245 `math.isfinite(ts)`, :308 `def _reject_json_constant`, :331 and :356 `json.loads(... parse_constant=...)`.

## Probe code (`/tmp/tameshi-r19-S065/probe.py`, verbatim)

```python
"""Bounded S065 re-open probe (round 19, SourceS065 scout). Reads only the
fetched docs pages in this directory; writes nothing. Not lane code."""
import html
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
QUOTES = {
    'nan-section': 'by default, this module accepts and outputs Infinity, -Infinity, and NaN as if they were valid JSON number literal values',
    'parse_constant-load-param': "If set, a function that is called with one of the following strings: '-Infinity', 'Infinity', or 'NaN'.",
    'parse_constant-raise': 'This can be used to raise an exception if invalid JSON numbers are encountered.',
    'deserializer-hook': 'In the deserializer, the parse_constant parameter can be used to alter this behavior.',
}


def page_text(name):
    raw = (HERE / name).read_text(encoding='utf-8')
    text = html.unescape(re.sub(r'<[^>]+>', '', raw))
    text = text.replace('\u2018', "'").replace('\u2019', "'")
    return re.sub(r'\s+', ' ', text)


for name in sys.argv[1:]:
    text = page_text(name)
    title = re.search(r'json — JSON encoder and decoder — Python [0-9.a-z]+ documentation', text)
    print(name, 'title:', title.group(0) if title else None)
    for key, quote in QUOTES.items():
        print(f'  {key}: count={text.count(quote)} words={len(quote.split())}')

print('interpreter:', sys.version.split()[0])
seen = []


def constant(value):
    seen.append(value)
    raise ValueError('nonfinite-json')


for doc in ('NaN', 'Infinity', '-Infinity', '{"exit": NaN}', '1e400', '-1e400', '{"exit": 1e400}'):
    seen.clear()
    default = json.loads(doc)
    try:
        value = json.loads(doc, parse_constant=constant)
        strict = f'value={value!r} type={type(value).__name__}'
    except ValueError as exc:
        strict = f'ValueError({exc})'
    print(f'{doc!r}: default={default!r} | parse_constant={strict} | hook_saw={seen}')
```
