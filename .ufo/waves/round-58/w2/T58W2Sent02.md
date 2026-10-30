# T58W2Sent02 — scratch + hygiene sentinel (round 58, wave 2)

Seat: scratch + hygiene sentinel · C0 = `8063d0a551fc5b3cb5a2d397da7353af53444534` (lane tip, verified) · 2026-10-30 07:49–09:12 -0300
Machine-readable twin: `T58W2Sent02.json` · Receipts: `T58W2Sent02-receipts/{disk.txt,tmp-residue.txt,fresh-writers.txt,greps.txt}`

## 0. Headline

- **MEDIUM — round-58-fresh /tmp litter during wave 2 (SENT02-1).** Six scratch dirs created **today 09:00–09:05** (`tameshi-mte-regression-kzakrvon` 0700 with all ten `mutate-and-run.sh --regression` legs; `tameshi-r4-2-regression.{ZdfeTt,3gCWbo}`; `tameshi-r17-MeasureV2-{j47nm6kj,7ttebcrt}`; `tameshi-r16-CRMeasure-tc4hz053`). Tools honour `TMPDIR` but default to `"${TMPDIR:-/tmp}"` (`tools/mutate-and-run.sh:1432`) and **keep the tree on FAIL/SETUP**; the lane's only hygiene guard (`no-harm.sh:47-48`) greps *source* for `dir\s*=\s*["']/tmp` and never inspects the host — so source-clean + host-littering passes invisibly. 116 accumulated entries, 597 MB, oldest 2026-10-27 → the pattern is per-round recurring, and it fired again this round, minutes before I measured it.
- **MEDIUM-LOW — hyaku config backup in /tmp (SENT02-2).** `/tmp/hyaku-cfg-backup/config.yml.20261028T121435.bak` (0600, 16 608 B) lists `xai-oauth/grok-*` and `alibaba-token-plan/*` entries [values never read; auth content is INFERENCE]. Config backups don't belong in a volatile world-listable dir.
- LOW ×3: 597 MB pre-round-58 `/tmp` residue (SENT02-3); stale `kaidoku-r50` scratch 7.9 GB incl. the only six >50 MB files on the scratch fs (SENT02-4); 2 822 MB of wave-1 seat scratch still present 30+ min after wave end (SENT02-5).
- **Clean sweeps (all with command + output in receipts):** no hardcoded `/tmp` in any round-58 instrument (three legitimate non-path hits only); all seven seat-written tool scripts — including C2's `attack.py` forgery artifact — contain **no** `/tmp` or credential strings; zero high-entropy credential formats and zero keyword-style credential assignments across round-58 evidence + waves + the new F9 knowledge file; the new fetched extracts (arxiv ×2, atlassian-live.html, dfcfw) carry no cookies/CSRF/session/bearer tokens — the only "api key" hits are public how-to prose; `/tmp` has no ≥50 MB top-level file; `/tmp/.aws`, `.codex`, `.agents`, `.git`, `.tmp*` are all **empty**.

## 1. Disk + scratch accounting (operability)

| check | result |
|---|---|
| `df -h /fast` | 804G total, 364G avail (55%) — no pressure |
| `du -sh /fast/scratch/hyaku/tameshi-r58` | **18G** at 08:57 → per-seat sum ~12.3G at 09:00 → **9145 MB** at 09:04 (22 dirs) — live churn, seats deleting scratch as they finish [O] |
| biggest round-58 dir | T58W2ExecC2 1455 MB (live wave-2 seat) |
| `/fast/scratch/hyaku/*` | kama-r64 **61.4G** (live lane, peer KamaR64 — monitored only), tameshi-r58 9.1G, kaidoku-r50 7.9G, kaidoku-r52 3.3G, kumitate-r69 1.7G, kasegi-r47 974M, souji-r44 299M |
| only >50 MB files on scratch fs | six ~139 MB git packs in `kaidoku-r50/w4-MutC1Counter/repo-A{0..5}` |

## 2. The seam SENT02-1 exploits (why the guard can't see the litter)

1. `tools/mutate-and-run.sh:1432` — `root=$(mktemp -d "${TMPDIR:-/tmp}/tameshi-r4-2-regression.XXXXXX")`; `:150-151` — *"removed on PASS unless --keep, kept on FAIL/SETUP"*.
2. `tools/registry.json` selftest rows: *"TMPDIR empty => unset, the platform default applies; a usable TMPDIR holds every mkdtemp and nothing is created under /tmp"* — tool contract satisfied, /tmp nonetheless used.
3. `.ufo/evidence/round-58/no-harm.sh:47-48` — `git grep -c -E "dir\s*=\s*[\"']/tmp" "$REV" -- tools/` expects 0: a **source-only** regex that `"${TMPDIR:-/tmp}"` never matches, and it never looks at the host.

So a seat that forgets `export TMPDIR` violates the round's scratch discipline (HYAKU_SCRATCH; `/tmp` only <50 MB) while every tool selftest stays green. Same blind-spot class the lane has hit before: the T58W1Panel07 receipt records a census regex missing `tempfile.mkdtemp` because it demanded `mkdir(at(`.

**Smallest remediation** (no tool code change needed): seats export `TMPDIR` under their `HYAKU_SCRATCH`; L1 routes a host-sweep arm for `no-harm.sh` (count `/tmp/tameshi-*`, RED if newer than round start); operator owns cleanup of the 597 MB (D7 precedent). [INFERENCE] Per-dir attribution to specific seats was not attempted — dirs are fingerprinted to tool families instead, to avoid touching live seats.

## 3. Credential material — none found (and what was excluded)

- High-entropy formats (AWS `AKIA…`, private-key blocks, `ghp_`/`github_pat_`/`xox`/`sk-ant`/`sk-proj`, `_authToken`, AWS session `AQIA…`): **0 matches** across `.ufo/waves/round-58/**`, `.ufo/evidence/round-58/**`, `corpus/knowledge/llm-mutant-equivalence-cost.md`.
- Keyword assignments: only `tokens = standing_cell(skill_text)`-shaped variable assignments (c2/measure.py:452 and quotes of it).
- New extracts: `atlassian-live.html:42068` is doc prose ("Get your Statuspage API key and page ID"); no `Set-Cookie`/CSRF/session/bearer anywhere.
- `/tmp/hyaku63` (Oct-28 extract workspace, checked for completeness): placeholder `api_key = "sk-no-key-required"` in public client docs, a gitbook CDN media token for a public icon, LLM-token identifiers in llama.cpp/vLLM sources — no secrets.
- `/tmp/.aws` et al.: empty dirs — nothing to leak.

## 4. Findings table

| id | sev | finding | evidence anchor |
|---|---|---|---|
| SENT02-1 | medium | 6 fresh /tmp scratch dirs during wave 2 (09:00–09:05); tool default `${TMPDIR:-/tmp}` + keep-on-FAIL + source-only guard | fresh-writers.txt; tmp-residue.txt (top 6 lines) |
| SENT02-2 | med-low | 0600 hyaku config backup in /tmp since Oct 28 (xai-oauth/alibaba plan entries) | tmp-residue.txt |
| SENT02-3 | low | 597 MB / 110 pre-round-58 tameshi+hyaku /tmp entries (r4-2 ×22, MeasureV2 ×~40, CRMeasure ×~20, registry-check ×2, …) | tmp-residue.txt (full dated inventory) |
| SENT02-4 | low | stale kaidoku-r50 = 7888 MB; six 139 MB packs; superseded by r51/r52 | disk.txt |
| SENT02-5 | low | 7 wave-1 dirs, 2822 MB, mtimes 08:33–08:36, still present 09:04 | disk.txt |

## 5. Hygiene of this seat

No `HYAKU_SCRATCH` dir was ever created by this seat (no `/fast/scratch/hyaku/tameshi-r58/T58W2Sent02` exists) — **nothing to delete, and `/tmp` was never written by this seat**. Writes limited to `T58W2Sent02.md`, `T58W2Sent02.json`, `T58W2Sent02-receipts/`. No lane file edited in place; `round-5[0-7]` evidence untouched. No tools installed/updated (none needed; pacman untouched per host pause).
