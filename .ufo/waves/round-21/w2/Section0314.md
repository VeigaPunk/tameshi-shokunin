verdict: done

# Section 314 — Kill-rate bands

## Finding

No blocking gaps; no false measured expectation in the current section at `790abd2129f153c13b471e381d454186edbde65e:SKILL.md:314-374`. The headline rates, controls, run counts, inconclusive status, and the host-gated kagi limitation agree with the historical measurement notes. The section is explicitly about rounds 2–3; treat its 43/43 and 16-case readings as dated records, not current results for the named live paths.

## Agreements and source checks

- `mutation-case-kimi-census.md:20-35` records control `43/43 pass`, 8/10 killed, D2/D10 survivors, held suite count, no inconclusive run, and the before/after digest, size, and mtime checks. The relevant historical source pin in that note is kumitate revision `175de6ba2e9e904010411b19cab27e0af9aad3d4`; `git show <pin>:scripts/kimi-census.mjs | sha256sum` yielded `83016d45049b009a6c9868dc392ff6ebcecb357c9abfe423f476459f2724f426`, matching the note. The cited mutation sites and assertions are present at that blob: `kimi-census.mjs:105,124,145,255,292,306,332,351-353,378,396,498,511-512,526`.
- `mutation-case-kagi-census.md:27-56` records 8/10, control `SELFTEST: PASS (16 cases)`, count held, no inconclusive run, 11.0 s / 11 runs, and restore checks. It explicitly distinguishes 14 executed hermetic cases from two host-gated skips (`:27-38`); SKILL `:369-371` does not conceal that limitation. Kagi revision `fecee8743e52eb8fb5fbb40782934cb619a1a96e` yields the note's expected source hash `275d8294a94e9eb74caa72043607e9ff12a30414c2d6298a37cbd62ddb53009f`. Relevant historical code sites are present, including the x-bit arm (`surface-census.sh:214-217`), skip path (`:817-824`), selftest summary (`:846-847`), and summary output (`:859-866`).
- The <50% admission policy is supported directly by `plans/round-2.plan.md:8-9`. The source notes explicitly mark coordinated rewrites, timing/timeout, and host stability as unmeasured (`mutation-case-kimi-census.md:193-207`; `mutation-case-kagi-census.md:193-206`). The cited cite-check limitation is accurate (`gates-survey-kumitate.md:51-58`).
- Restore/hash claims match `mutation-case-kimi-census.md:34-35` and `mutation-case-kagi-census.md:54-56`. The current section itself has no obsolete runnable command.

## Non-blocking citation and reproducibility caveats

1. **D1/D3 “14 shared” (`SKILL.md:361`) is true but not supported by its immediate citation.** `mutation-case-kimi-census.md:74-76` says 16 cases each and points to full lists in scratch `evidence/results.json`; it does not give the intersection. Earlier pinned audits document the rebuild and exact intersection: `RX9.md:47`, `CR06.md:97-103`, and `CR09.md:66-68`. Re-anchor the citation to retained audit evidence or preserve the case lists in the cited note. This is not a wrong expectation.
2. **PROVINCE range is off by one (`SKILL.md:340`).** The two-independent-lane bar spans `PROVINCE.md:15-16`; the cited `:16-17` omits “TWO” and includes the following sibling-gate sentence.
3. **Two loose citation attachments:** `SKILL.md:337` cites kimi `:185-191`, which is the D7 pre-run calibration miss, not the report convention. The 8/10 result/table is at `:29-35` and `:41-53`; the <50% anti-claim is `plans/round-2.plan.md:8-9`. `SKILL.md:329` cites kimi `:109-144` for naming classes outside the injected vocabulary; the fuller scope on untested coordinated edits is `:144-146`, beyond the cited range. These do not overturn the policy guidance.
4. **Current paths have drifted from the historical measurements.** At review time, live kumitate `scripts/kimi-census.mjs` is sha256 `7818970b80d4951b8edf15dcc8c5a16efe57f457f956a5ce019f049068538156` (46638 B), and live kagi `corpus/surface-census.sh` is `1e697b0179547a869b73fcf966ce05dd60b07adbe7094a95d3d0a2d4102de11d` (44220 B); neither matches its measured source pin. This section is historical, not a live count claim. However, the cited notes' reproduce commands (`mutation-case-kimi-census.md:171-177`; `mutation-case-kagi-census.md:242-249`) copy unpinned current paths and will not materialize the old artifact today. A replay must use the stated historical Git revisions and verify the expected hashes. I did not run those recipes or any selftest. The original `/tmp/tameshi-r2-1-work` and `/tmp/tameshi-r3-1-work` directories are absent, so the raw result bundles are not available for this review.

## Commands and exits

Inspection only; no build, test, lint, mutation rerun, or source edit. These reads and hash queries returned exit 0:

- `git show 790abd2129f153c13b471e381d454186edbde65e:SKILL.md` (section and boundaries).
- `git show 790abd2129f153c13b471e381d454186edbde65e:<cited note or policy path>` for `corpus/knowledge/mutation-case-kimi-census.md`, `corpus/knowledge/mutation-case-kagi-census.md`, `plans/round-2.plan.md`, `PROVINCE.md`, and `corpus/knowledge/gates-survey-kumitate.md`.
- `git -C ../kumitate-shokunin show 175de6ba2e9e904010411b19cab27e0af9aad3d4:scripts/kimi-census.mjs | sha256sum` → expected historical hash; same query at `../kagi-shokunin` revision `fecee8743e52eb8fb5fbb40782934cb619a1a96e` → expected historical hash.
- `git show 790abd2129f153c13b471e381d454186edbde65e:.ufo/waves/round-16/w3/RX9.md`, the pinned CR06, CR09, and CR07 reports → exit 0; these contain the prior D1/D3 rebuild and citation assessments.
- `sha256sum`/`stat` on the current sibling paths → different hashes and sizes listed above.
- Lookups for the two original `/tmp` evidence directories returned “Path not found”; no outputs were regenerated.

Evidence JSON: `.ufo/waves/round-21/w2/sections/314.json`.

Report trailer: `.ufo/waves/round-21/w2/Section0314.md`
