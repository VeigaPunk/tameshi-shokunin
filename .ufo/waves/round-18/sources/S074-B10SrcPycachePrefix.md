# S074 draft — B10SrcPycachePrefix (provisional id; round-18 wave 1)

Decision: ADMIT as `mined` (not duplicate, not rejected). Duplicate check: `grep -rn 'using/cmdline\|PYTHONPYCACHEPREFIX\|PYTHONDONTWRITEBYTECODE' corpus/SOURCES.md` returned no lines (2026-10-20). No existing row has the URL.

Id note: `corpus/SOURCES.md` on the lane tip 183f87b ends at S064 and its own "Next unused id" line reads S065. The Target's provisional id S074 is used as given; S065–S073 stay unallocated in this file and the L1 must reconcile ids at integration.

## Registry row (13 cells)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S074 | Command line and environment (CPython 3.15.0 docs) — https://docs.python.org/3/using/cmdline.html | docs | A | CPython 3.15's definition of the two environment variables that redirect .pyc writes: PYTHONDONTWRITEBYTECODE and PYTHONPYCACHEPREFIX | §1.2 Environment variables, entries PYTHONDONTWRITEBYTECODE and PYTHONPYCACHEPREFIX (#envvar-PYTHONDONTWRITEBYTECODE, #envvar-PYTHONPYCACHEPREFIX) @ Python 3.15.0 docs, fetched 2026-10-20; served HTML sha256 a4863a38223e1dab199e8eb0974915561c859b23dbacc8ecff76bb06e589b734 | a non-empty PYTHONDONTWRITEBYTECODE equals -B and stops .pyc writes on import of source modules; a set PYTHONPYCACHEPREFIX writes .pyc files in a mirror tree at that path instead of __pycache__ (added in 3.8), so a fixture can keep bytecode out of the source tree by environment; the entries state write behaviour only and say nothing about reads | mined | 2026-10-20 | on-release | .ufo/evidence/round-18/ |

Column check: 11 visible cells, NF=13 once the leading and trailing pipes are counted; no `|` inside any cell.

## Gate

- URL: https://docs.python.org/3/using/cmdline.html (canonical link tag in the served page matches).
- Access date: 2026-10-20 (`curl -fsSL` → `/tmp/tameshi-r18w1-B10SrcPycachePrefix-rWvIZ0/cmdline.html`, sha256 a4863a38…b734; the page is the Python 3.15.0 documentation, title "1. Command line and environment").
- Exact section/anchor: §1.2 Environment variables → entry `PYTHONPYCACHEPREFIX` (`id="envvar-PYTHONPYCACHEPREFIX"`, served HTML line 1139), with its "Added in version 3.8." line.
- Quote, PYTHONPYCACHEPREFIX entry, verbatim (text with tags stripped; `grep -F` hit confirmed), 22 words (`wc -w` = 22):
  > If this is set, Python will write .pyc files in a mirror directory tree at this path, instead of in __pycache__ directories
- Second quote, PYTHONDONTWRITEBYTECODE entry (`id="envvar-PYTHONDONTWRITEBYTECODE"`, line 1131), verbatim, 14 words:
  > If this is set to a non-empty string, Python won’t try to write .pyc
- Support for the purpose: the C2 P06 probe is about where a trace collector's Python run writes bytecode. The two entries define exactly that write-location behaviour; they do not prove the collector's behaviour. The teaches cell is limited to the documented write effect.
- Limits recorded: the page is the 3.15.0 dev docs (version floor for PYTHONPYCACHEPREFIX is 3.8 per the entry); the page says nothing about reads or about child processes.
