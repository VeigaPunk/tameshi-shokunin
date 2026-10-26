# T48A2ExecLiveStability — live-fetch stability of the four C2 URLs

Seat `T48A2ExecLiveStability` (a2w1, leaf; no dispatch). Item: for each C2 target S026, S048, S093,
S108, fetch the receipt URL 6× into scratch, 10 s apart, and test whether the target's `C2-QUOTE`
line is located in each fetch by contract amendment 2's extraction; every fetch that does not
locate the quote is a finding (it predicts a live-check failure at the deciding run).

Base `473336d9d789f6081195e7376d17836a24666bc3`; content revision `c7586b9a`. Read-only on the lane
except this file: `git -C . status --porcelain` in the lane → `?? .ufo/waves/round-48/a2w1/` only,
so `corpus/`, `tools/` and `SCORECARD.md` are clean.

Scratch `S=/fast/scratch/hyaku/tameshi-r48/T48A2ExecLiveStability` (6.5 MB of fetches), deleted
before this report was finalised. No counter was run at the content revision and no counter mode was
run at all: the frozen counter's own functions (`extract`, `collapse`, `check_quote`,
`check_phrases`, `check_live`, `live_fetch`, `GATE_RE`, `REQUIRED`) were imported read-only from
`.ufo/evidence/round-48/freshness/measure.py` (module is `__main__`-guarded; nothing is written).
No tool installed or upgraded; no pacman call. Nothing here is scored.

**Verdict: no revealed instability. 48 live fetches (24 item-shaped + 24 counter-shaped) plus 17
transport shapes — 65 responses carrying the page — and the quote is located in every one.
`check_live` returns `ok` for all four targets. Two residuals, neither a predicate defect today:
receipt sha256 is not re-derivable live for S026 and S108 (their bodies carry per-generation nonces),
and the attempt-1 `3148`-char S108 variant was not reproduced in 29 S108 responses today — if it
recurs at the deciding run without the quote, live reads `absent` and C2 fails.**

## 1. Method (verbatim shapes)

Item shape, per target, 6×, 10 s apart, four targets in parallel (receipt url read from
`<T>.receipt.json`):

```
curl -sS -L -o "$S/raw/$t.$i" \
  -w '%{http_code} %{size_download} %{time_total} %{url_effective} %{content_type}' \
  --max-time 45 "$url"
```

Counter shape (the deciding run's actual code path, `measure.py:184-195` `live_fetch`:
`urllib.request`, UA `tameshi-c2-r48/1.0 (round-48 freshness counter)`, no `Accept-Encoding`,
`timeout=60`), 6× per target, 10 s apart:

```
m.live_fetch(rc['url'])  →  m.extract(raw)  →  quote in text
```

Location test (`measure.py:170-178` `extract`, amendment 2 verbatim: drop `<script>`/`<style>`
contents, strip tags, `html.unescape`, collapse whitespace; quote whitespace-collapsed, no case or
punctuation folding). Quotes are parsed from `corpus/lessons/round-48.md` with the counter's own
`GATE_RE`:

| target | Gate line | R | quote words | required phrase(s) | `check_quote` | `check_phrases` |
|---|---|---|---|---|---|---|
| S026 | `round-48.md:21` | S265 | 15 | `84%` | ok | ok |
| S048 | `round-48.md:22` | S266 | 21 | `should therefore be prioritised` | ok | ok |
| S093 | `round-48.md:23` | S267 | 25 | `--unshare-all`, `--unshare-cgroup-try` | ok | ok |
| S108 | `round-48.md:24` | S268 | 6 | `--update_goldens` | ok | ok |

All four are within the 25-word bound and each carries its required phrases inside the quote.

## 2. Fetch table — 2026-10-26 13:37:49Z–13:43:17Z, 6 curl + 6 urllib per target

`rc` column: 0 for every fetch. HTTP 200 and 0 redirects (`%{url_effective}` = the receipt url) for
every fetch. `==rcpt` compares the fetch's raw sha256 with the committed receipt/snapshot sha256.

| target | kind i | http | bytes | raw sha256[:12] | extract chars | extract sha256[:12] | quote located | offset | ==rcpt |
|---|---|---|---|---|---|---|---|---|---|
| S026 | curl 1 | 200 | 236387 | `dfea6b9ba734` | 26246 | `6e8b4d19dffd` | yes | 2136 | no |
| S026 | curl 2 | 200 | 236387 | `dfea6b9ba734` | 26246 | `6e8b4d19dffd` | yes | 2136 | no |
| S026 | curl 3 | 200 | 236387 | `dfea6b9ba734` | 26246 | `6e8b4d19dffd` | yes | 2136 | no |
| S026 | curl 4 | 200 | 236387 | `dfea6b9ba734` | 26246 | `6e8b4d19dffd` | yes | 2136 | no |
| S026 | curl 5 | 200 | 236387 | `dfea6b9ba734` | 26246 | `6e8b4d19dffd` | yes | 2136 | no |
| S026 | curl 6 | 200 | 236387 | `dfea6b9ba734` | 26246 | `6e8b4d19dffd` | yes | 2136 | no |
| S026 | urllib 1-6 | 200 | 236387 | `dfea6b9ba734` | 26246 | `6e8b4d19dffd` | yes ×6 | 2136 | no |
| S048 | curl 1-6 | 200 | 8892 | `e9cbc3e1ab7c` | 3253 | `5ccb31d4d9a2` | yes ×6 | 1013 | **yes** |
| S048 | urllib 1-6 | 200 | 8892 | `e9cbc3e1ab7c` | 3253 | `5ccb31d4d9a2` | yes ×6 | 1013 | **yes** |
| S093 | curl 1-6 | 200 | 33289 | `2cb77df2f4be` | 16699 | `dd2a8895827a` | yes ×6 | 2641 | **yes** |
| S093 | urllib 1-6 | 200 | 33289 | `2cb77df2f4be` | 16699 | `dd2a8895827a` | yes ×6 | 2641 | **yes** |
| S108 | curl 1 | 200 | 111409 | `a04bb2c68bce` | 3496 | `e83fc1baae07` | yes | 2513 | no |
| S108 | curl 2 | 200 | 111409 | `da3820982279` | 3496 | `e83fc1baae07` | yes | 2513 | no |
| S108 | curl 3 | 200 | 111405 | `60ab04a42684` | 3496 | `e83fc1baae07` | yes | 2513 | no |
| S108 | curl 4 | 200 | 111409 | `8a39a2ed10fc` | 3496 | `e83fc1baae07` | yes | 2513 | no |
| S108 | curl 5 | 200 | 111405 | `aa711bb618d6` | 3496 | `e83fc1baae07` | yes | 2513 | no |
| S108 | curl 6 | 200 | 111409 | `1e090834df7b` | 3496 | `e83fc1baae07` | yes | 2513 | no |
| S108 | urllib 1 | 200 | 111409 | `48663bbf45b6` | 3496 | `e83fc1baae07` | yes | 2513 | no |
| S108 | urllib 2 | 200 | 111409 | `2b9d299bb3ac` | 3496 | `e83fc1baae07` | yes | 2513 | no |
| S108 | urllib 3 | 200 | 111405 | `299fe781bef5` | 3496 | `e83fc1baae07` | yes | 2513 | no |
| S108 | urllib 4 | 200 | 111409 | `6054f787ae65` | 3496 | `e83fc1baae07` | yes | 2513 | no |
| S108 | urllib 5 | 200 | 111409 | `6eb080df52c9` | 3496 | `e83fc1baae07` | yes | 2513 | no |
| S108 | urllib 6 | 200 | 111405 | `0ce0c73e4a3b` | 3496 | `e83fc1baae07` | yes | 2513 | no |

Summary (computed over the 12 item+counter fetches per target):

| target | fetches | distinct raw sha256 | sizes B | distinct extracted text | quote located |
|---|---|---|---|---|---|
| S026 | 12 | 1 | 236387 | 1 | **12/12** |
| S048 | 12 | 1 | 8892 | 1 | **12/12** |
| S093 | 12 | 1 | 33289 | 1 | **12/12** |
| S108 | 12 | 12 | 111409 ×8, 111405 ×4 | 1 | **12/12** |

Timing: `time_total` 0.01–0.85 s against the counter's 60 s `timeout` and the deciding run's single
fetch per URL — no timeout margin risk observed.

Counter-shape confirmation, one `check_live` call per target on the committed receipts
(`measure.py:336-345`), each fetching once and counting occurrences in the extracted text:

```
S026 check_live -> ok  occurrences=1 idx=2136  chars=26246
S048 check_live -> ok  occurrences=1 idx=1013  chars=3253
S093 check_live -> ok  occurrences=1 idx=2641  chars=16699
S108 check_live -> ok  occurrences=1 idx=2513  chars=3496
```

Each located occurrence is article prose, not boilerplate (context printed by the same run), e.g.
S108: `… test_case_last.expected 如何更新 .expected 文件？ 可以通过使用参数 --test_arg=--update_goldens
--test_strategy=local 运行受影响的测试目标来更新 .expected 文件。应检查由此产生的差异是否存在意外的变化。 如未另行说明…`
— verbatim from the live text at char 2513.

## 3. Findings

**F1 — S108 raw bytes are nondeterministic; the extraction is what makes the live check stable
(informational, no action).** 12 fetches produced 12 distinct raw sha256 and two sizes (111409,
111405). `diff` of snapshot (`S108.html`, `04e4c091715a…`) vs live fetch 1 changes 3 of 4090 lines:
`:4068` the `<script type="application/json" analytics>` dimension key order,
`:4079` the CSP `nonce-…`, `:4084` a devsite flag list. All three sit inside `<script>`/attribute
regions, so amendment 2's script/style drop yields one identical 3496-char text
(`e83fc1baae07`) in 12/12 and the quote at offset 2513 in 12/12. Show: `python3 table.py all` over
the scratch raws; `grep -n 'analytics\|nonce-' .../S108.html` → lines 4068, 4079.
Consequence: S108's receipt sha256 (`04e4c091715a…`) is **not re-derivable from the live URL**; it
is only checkable against the committed snapshot. That matches the counter, which never compares
live bytes with the snapshot (only `quote in extract(raw)`), and matches `corpus/lessons/round-48.md:371-376`.

**F2 — S026 is byte-stable live but differs from its receipt sha256 in a per-generation nonce
(informational, no action).** 12/12 fetches are identical (`dfea6b9ba734`, 236387 B) yet differ
from `S026.receipt.json` (`a4c5c46b4af9`). First differing byte 30028 is the Blogger dyncss token
`…/authorization.css?zx=<uuid>` inside a `<link href>`; the snapshot's uuid is
`53b770d4-0937-44d6-9629-2c6e97563f2f`, today's is `58977ca4-…`. 4 of 6172 lines change and the
extracted text is **identical** (`extract(snap) == extract(live)` → `True`, 26246 chars, quote at
2136 in 12/12). So the live check is stable; only receipt sha reproducibility is limited (same as
F1, structural, and the contract binds the receipt sha to the snapshot, not to a live fetch).

**F3 — S108 content is UA-sensitive, and one UA class gets a 302 into OAuth (risk R1's mechanism).**
`curl -A 'Mozilla/5.0 … Chrome/130.0 …'` on the receipt url → `HTTP/2 302`,
`location: https://www.tensorflow.org/oauth2authorize?return_url=…golden_tests%3Fhl%3Dzh-cn…`,
`vary: Cookie`, `set-cookie: signin=autosignin`; with `-L` curl exits 47 (too many redirects) and leaves no body
file. The counter's UA (`tameshi-c2-r48/1.0 …`) and curl's default both get 200
(12/12). A Googlebot UA gets 200 but a different body (112362 B, 3944 chars, quote at 2961 —
located). Show: `curl -sS -A 'Mozilla/5.0 …' -D - -o /dev/null --max-redirs 0 '<url>'`.
Failure mode to know about: `live_fetch` follows the 302, receives the OAuth page with HTTP 200,
and `extract()` cannot contain the quote → `check_live` returns `absent` (not `unreachable`), so a
UA/sign-in policy change would surface as `refreshed=3` with no distinguishing field. Not a defect of
this revision; the counter's fixed UA is 200 today in 12/12.

**R1 — residual: the attempt-1 `3148`-char S108 text variant is unreproduced, and if it recurs
without the quote the deciding run fails.** `corpus/lessons/round-48.md:371-376` records 7 attempt-1
fetches with 2 extracted text variants (3496 and 3148 chars) and sizes including 104924 B; today's
29 S108 responses (12 in §2 + 17 transport shapes in §4) yield only the 3496-char text, except the
two Googlebot-shaped responses at 3944 chars — all containing the quote; **no 3148-char text
appeared**, and `a2w1/T48W2RefetchS108.md` §4 reports 8/8 the same. Geometric bound on the risk: the quote spans
extracted chars **2513–2619** of 3496; the tail after it is 877 chars (licence footer 150 chars +
the `[[["易于理解"…` thumb-rating template block, 727 chars), so a 348-char loss fits inside the tail
and would leave the quote located — consistent with the attempt-1 note that both variants carry
`--update_goldens`. But no capture of the short variant exists in the lane, so the quote's presence
in it is unverified here. If it recurred without the quote: `check_live` → `absent` for S108 →
`refreshed=3` → `C2_R48_PASS=false`. Only mitigation available before the deciding run: none that is
read-only — the variant was not reproducible from this host, and the counter (correctly) forbids a
second deciding invocation.

**Not findings.** S048 (pitest.org) and S093 (raw.githubusercontent.com `v0.13.1`, XML, `text/plain`)
are byte-identical to their snapshots in 12/12 fetches each — pinned upstreams, no variation. No
fetch in this seat failed to locate a quote, so no live-check failure is predicted for S048, S093 or
S026; S108 is predicted to pass with the caveat of R1.

## 4. Transport-shape census (S108, supplementary — explains the variants, not scored)

18 curl shapes against the receipt url: **17 returned HTTP 200** and the quote is located in all 17
(16 extract to 3496 chars, Googlebot to 3944); 1 (browser UA) returned 302; one
`--max-filesize 104924` probe aborted with rc 63 after 0 bytes (a client-side cap, not a server
answer). The 17: `plain` 111405/3496, `http1.1` 111405, `http2` 111409, `compressed` 111409
(`size_download` 21574, body 111409), `Accept-Encoding: br` 111409, `identity` 111409,
`-A tameshi-c2-r48/1.0 …` 111405, `-A Python-urllib/3.13` 111409, `Accept-Language: zh-CN` 111409,
`Accept-Language: en-US` 111405, `--no-alpn` 111409, `-4` 111405, `--http3` and `--http3-only`
111405 over HTTP/3, `Accept: text/html,…` 111405, `Cache-Control: no-cache` 111405,
`-A Googlebot/2.1 …` 112362/3944 (quote at 2961); plus `-A Chrome/130` **302 → oauth2authorize**
(see F3). Extraction stayed at 3496 chars (Googlebot 3944) with the quote present in every 200
response; no 3148-char text appeared.
`--compressed` also confirms `live_fetch`'s gzip branch (`measure.py:192-193`) is not exercised by
the counter (urllib sends no `Accept-Encoding`, so bodies arrive uncompressed: 111409/111405).

## 5. Reproduce

```
S=/fast/scratch/hyaku/tameshi-r48/T48A2ExecLiveStability; mkdir -p "$S/raw"
# item shape, 4 targets in parallel, 6 fetches each, 10 s apart
for t in S026 S048 S093 S108; do for i in 1 2 3 4 5 6; do
  curl -sS -L -o "$S/raw/$t.$i" -w "%{http_code} %{size_download}\n" --max-time 45 \
    "$(jq -r .url .ufo/evidence/round-48/freshness/sources/$t.receipt.json)"; sleep 10; done & done; wait
# counter shape + locate (imports the frozen counter read-only)
python3 - <<'PY'
import importlib.util,json
L='/home/vgpnk/Projects/shokunin/tameshi-shokunin'
s=importlib.util.spec_from_file_location('m',L+'/.ufo/evidence/round-48/freshness/measure.py')
m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
q={l.split(' ')[3].rstrip(':'):m.collapse(l.split('`')[1])
   for l in open(L+'/corpus/lessons/round-48.md',encoding='utf-8') if l.startswith('- C2-QUOTE ')}
c={}
for t in q:
    rc=json.load(open(L+'/.ufo/evidence/round-48/freshness/sources/%s.receipt.json'%t))
    print(t, m.check_live(True, rc, q[t], m.live_fetch, c), q[t] in m.extract(c[rc['url']][1]))
PY
```

## 6. Risks and blockers

- R1 above is the only residual that could flip C2 at the deciding run, and it cannot be closed from
  a read-only seat (the short variant was not reproducible in 25 fetches; a second deciding
  invocation is forbidden by amendment 8).
- F1/F2 mean the two receipts' sha256 are point-in-time records, not re-derivable: a reviewer who
  re-fetches S026 or S108 sees a different raw digest. Both are visible in the snapshot↔live diffs
  and neither is read by the counter; no action proposed.
- No blocker. Scratch `/fast/scratch/hyaku/tameshi-r48/T48A2ExecLiveStability` deleted (6.5 MB
  reclaimed); nothing written under `/tmp`; disk guard read before the pass (`/fast` 601 G free,
  `/tmp` 3 %) and no ENOSPC pressure at any point (604 G free after cleanup).
