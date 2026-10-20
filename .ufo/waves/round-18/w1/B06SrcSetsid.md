# B06SrcSetsid — round 18 wave 1 source-row report

Verdict: **built** — S070 drafted as `mined` (draft row + Gate in `.ufo/waves/round-18/sources/S070-B06SrcSetsid.md`); no duplicate; source supports the purpose except the killpg consequence, which is marked `[INFERENCE]`.

## Commands and exits

| step | command (cwd `/home/vgpnk/Projects/shokunin`) | exit | key output |
|---|---|---|---|
| open source | `read https://man7.org/linux/man-pages/man2/setsid.2.html` | ok | man-pages 6.19 page, footer 2026-06-05; §DESCRIPTION ¶2, §ERRORS EPERM, §NOTES |
| fetch bytes | `curl -sSL -o $T/setsid.html https://man7.org/linux/man-pages/man2/setsid.2.html && sha256sum` | 0 | `52cbc1904742df69556104f71d3279f93581756579881c85cee8e37be37c7f30` |
| quote check | strip tags, `tr -s ' \n' ' '`, `grep -o` the quote | 0 | "The calling process will be the only process in the new process group and in the new session." present |
| EPERM check | same, `grep -o` | 0 | "setsid() fails if the calling process is already a process group leader." present |
| word count | `echo "<quote>" \| wc -w` | 0 | 18 (purpose quote); 12 (EPERM quote) |
| duplicate sweep | `_grep` `setsid\|man2/setsid` on `tameshi-shokunin/corpus/SOURCES.md` | 0 | No matches found |
| SOURCES context | `_read` `tameshi-shokunin/corpus/SOURCES.md` (195 lines), `CORPUS.md` §SOURCES.md | ok | 13-cell row shape (11 columns, NF=13), tiers A/B/C, status enum, `Next unused id: S065` |
| used-by existence | `_glob` `tameshi-shokunin/.ufo/evidence/round-18/*` | ok | only `census-start.txt`; `defect-probes.py` absent |

Scratch: `/tmp/tameshi-r18w1-B06SrcSetsid-pNAIpm/setsid.html` (fetched copy). No git commands run; no lane git state touched.

## Decision evidence

- **Duplicate:** none. The only man-page rows are S060 (strace, man1) and the S001–S064 docs; no `setsid` text appears in `corpus/SOURCES.md`.
- **Reject?** No. The page states the caller "will be the only process in the new process group and in the new session" (§DESCRIPTION ¶2) and that setsid "fails if the calling process is already a process group leader" (§ERRORS EPERM). That supports the P10 premise that a setsid child leaves its old group and must fork first.
- **Not supported by the page:** that a `killpg` on the old group fails to reach the escaped process. The page never names killpg or signals. Recorded in `teaches` as `[INFERENCE]`; probe P10 must measure it.
- **Tier A:** the Linux man-pages project is the upstream reference for the Linux interface; scope is Linux setsid semantics only.

## Row (draft; full text in the owned file)

`S070 | Linux man-pages: setsid(2) — https://man7.org/linux/man-pages/man2/setsid.2.html | docs | A | ... | §DESCRIPTION ¶2 and §ERRORS EPERM @ man-pages 6.19 (footer 2026-06-05), fetched 2026-10-20 | ... | mined | 2026-10-20 | 180d | .ufo/evidence/round-18/defect-probes.py`

## Gate

- URL: https://man7.org/linux/man-pages/man2/setsid.2.html · access 2026-10-20 · anchor §DESCRIPTION ¶2 · man-pages 6.19
- Quote (18 words, verbatim): "The calling process will be the only process in the new process group and in the new session."

## Findings and caveats

1. **used-by is not yet a citing file.** `mined` requires a citing path; `.ufo/evidence/round-18/defect-probes.py` does not exist (glob). The census check `mined rows whose used-by paths do not exist` will print `missing:` until that file exists and cites S070. Fallback if it does not land this round: status `queued`, used-by `—`. Not decided by this seat.
2. **Id allocation.** Target assigns S070; `corpus/SOURCES.md` line 195 says `Next unused id: S065`. The L1 must reconcile the gap (S065–S069) before install, or renumber.
3. **Quote normalisation.** The one source line break is joined to a space; this is the only change. The word count is on the joined string.
4. **Mirror.** No mirror fallback was needed; man7.org answered both the `read` and `curl` fetches.

## Checks the main agent should run after install

- `awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md` → 0
- The `mined` used-by existence check (census line 147) → must print nothing once the citing file exists.

## Installs/updates

None. `curl` and `sha256sum` already present on the host.

## Out of scope / not done

- No edit to `corpus/SOURCES.md`, the registry, or any lane file (L1 installs).
- No knowledge or lesson entry written; the `## Gate` lives here until the round lesson exists.
