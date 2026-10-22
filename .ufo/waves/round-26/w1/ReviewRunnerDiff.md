# ReviewRunnerDiff — round 26, wave 1 (runner and interop diff review)

Reviewer seat: TameshiR26.ReviewRunnerDiff (leaf member; no subagent dispatch). Date: 2026-10-22.

Scope reviewed: `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff 622d31d90b1fbc55c56e91a2b012bc18d6f1421a a08e85c5d7f899e8a5992e20517edb1a380d79eb -- tools/mutate-and-run.sh tools/mte-interop.py`, plus (a) a whole-file search of the runner and SKILL.md for "eight" and bare "8" tokens that refer to legs, (b) comment-accuracy checks of the new leg-9 prose against committed evidence, and (c) extraction and byte comparison of the embedded `js-cite-check` spec heredoc against the committed spec file.

Worktree freshness check: `git diff --stat a08e85c5d7f899e8a5992e20517edb1a380d79eb -- tools/mutate-and-run.sh tools/mte-interop.py SKILL.md` printed nothing, so every path:line below is both the committed state at a08e85c and the current bytes.

## Verdict

The target diff is complete and accurate. Every operative leg-count site in `tools/mutate-and-run.sh` and `tools/mte-interop.py` is updated to nine; the retained "eight" tokens in both tools are correct history; every new runner comment about leg 9 checks out against the committed sweep and pin evidence; and the embedded `js-cite-check` spec heredoc is byte-identical to the committed spec. The runner's selftest passes 97/97 on the committed bytes with calls=9 specs=9 nlegs=9.

The misses are all in SKILL.md: nine leg-count sites still carry present-tense "eight" / "N=8" / "cases=8" formulations tied to "since round 18", and the integration commit's only SKILL.md change is the appended 17-line ninth-case section (`git diff 622d31d..a08e85c -- SKILL.md`: "17 insertions(+), 0 deletions(-)", one hunk at file end), so none of those sites was touched.

## Findings — misses, with line numbers

All in SKILL.md at a08e85c. None breaks an executed gate (the gates read the runner's tables, not the prose); each is a stale count on a page that the same commit teaches "nine" elsewhere. Smallest safe correction is given per site.

1. SKILL.md:10 — "…are worked here (seven recorded since round 16; eight since round 18)…" — present-tense count of recorded cases, while the same page at :2086 opens "## Ninth recorded case — round 26". Correction: extend the parenthetical with "; nine since round 26".
2. SKILL.md:925 — "Four legs at that revision (r7-1; seven since round 16; eight since round 18)" — same pattern in the ledger-section prose. Same correction.
3. SKILL.md:931 — "…corpus/knowledge/fleet-kill-rate-ledger.md (eight rows since its round-18 block)." — true of the cited file today only because the ledger still has no measured js-cite-check row (ledger :94 is the round-5 probe, :107 says "full sweep open"); it desyncs from the nine-leg runner now and goes false the moment the ninth ledger row lands. Correction rides with the ledger row (see Adjacent 1); alternatively reword now.
4. SKILL.md:950 — "Cite `REGRESSION: PASS (cases=N passed=N; …)` (N=4 at r7-1, 7 since round 16, 8 since round 18)" — the receipt line this rule tells the reader to cite now prints cases=9 passed=9 (retained receipt, closing line). Correction: "9 since round 26".
5. SKILL.md:960-961 — "Current anchors: pins/revisions/tables `tools/mutate-and-run.sh:597-620`, first-four specs :648-829, inventory :82-100, eight dispatches :1314-1356." — both the count and the line anchors are stale, and the line claims present tense. Measured current anchors: nine leg dispatches at :1384-1424 (js-kimi-census :1384 through js-cite-check :1424, block closes :1428); PIN_CITECHECK :619, REV_CITECHECK :620, TABLE_JS…TABLE_CITECHECK :621-629; regression_specs (first spec heredoc) :657-659. Correction: "nine dispatches :1384-1428" and re-resolve the other three ranges.
6. SKILL.md:976 — "…N=8 since round 18)." — same receipt count; now 9.
7. SKILL.md:1390 — "`mutation-case-*.md` (six at round 11; seven since round 16; eight since round 18)" — still literally true only because the ninth entry file does not exist yet (see Adjacent 2). Becomes wrong when the note lands; update to "nine since round 26" together with that landing.
8. SKILL.md:1391 — "`tools/mutate-and-run.sh` | the instrument: `--selftest`, `--regression` (six-leg registry at round 11, seven since round 16, eight since round 18; git-materialized replay)" — the registry is nine legs. Correction: "nine since round 26".
9. SKILL.md:1762 — "`--regression` → `cases=7` at round 16; `cases=8` since round 18" — the same command's current receipt prints cases=9. Correction: "cases=9 since round 26".

Checked and deliberately kept (not misses): historical ordinals and dated receipts — runner :15 ("r18 adds the eighth measured leg"), :83 ("r16 seven; r18 eight; r26 nine"), :162 ("r18 extends it to eight, r26 to nine"), :100/:102/:113/:1023/:1924 ("leg 8" history); SKILL.md round-18 section :1905-1915 including "cases=8 passed=8" (a dated record; flagged in Residual risk because a fresh replay now prints 9).

## Verified clean — target diff

tools/mutate-and-run.sh (committed bytes sha256 fb91ef7621f5de67f9845dba2d3cba8fc567b0f05e4490cfc927622b0929f9de):

- Every operative count site updated: header :16-17; mode chain :83; leg table row :95; sources :101; leg-9 provenance :105-107; "All nine defect specs are embedded below" :108; selftest chain :162; options tuple :214-215; PIN/REV :619-620; TABLE_CITECHECK :629; regression_specs comment :657; spec heredoc :1082-1143 and nonempty chain :1145; REGRESSION_EXPECT :1372-1382; dispatch :1424-1428; nlegs=9 and nine-element status list :1430-1431; selftest :1925, :1935, :1944-1945, :1955, :1957-1958 (nine tuples, js-cite-check 10:5).
- Comment accuracy, leg 9 provenance sentence :105-107: sweep.txt records "MUTATE_DATE: 2026-10-22T10:02:07Z" and closes "MUTATE: DONE (… defects=10 killed=5 survived=5 inconclusive=0 kill-rate=50%)"; the control line reads "62/62 cases passed (hermetic)" — matching ":1084 62 cases", ":95 5/10 (50 %)", and "10/10 verdict predictions held" (predictions.json holds ten predictions; every results.tsv verdict matches its prediction: five K_* KILLED, five S_* SURVIVED). TABLE_CITECHECK (:629) equals the results.tsv rows in both order and verdicts.
- Pin re-derivation: `git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin show 1205c6621a2eccbb8ffceae86d9e7b79a7990b3a:scripts/cite-check.mjs | sha256sum` printed 40573448330f52fb7d45c59cb0b91d236b6e277a250d850a0e2585adc7c10c9f (= PIN_CITECHECK :619 and the spec header :1084); `| wc -l` printed 2537 (= header); `git ls-tree 1205c6621a… -- scripts/cite-check.mjs` printed mode 100755 (= header).
- Dynamic check (committed bytes copied to /tmp/tameshi-r26-w1-review/selftest/, run there): "PASS embedded leg specs: nine files written"; "PASS leg-count agreement: calls=9 specs=9 nlegs=9 (want 9)"; "PASS leg-count agreement: selftest leg tuples=9 (want 9)"; "PASS embedded leg js-cite-check: spec and recorded table agree"; "MUTATE_SELFTEST: 97/97 pass"; "VERDICT: PASS".

tools/mte-interop.py:

- LEG_TABLE gains `'js-cite-check': 'TABLE_CITECHECK'` (:75-78) and the only count-bearing string reads "…differs from the nine ledger legs…" (:318). Grep for `(?i)eight|(?<![0-9A-Za-z_.])8(?![0-9A-Za-z_.])` over the whole file: zero matches. The selftest judges synthetic reports and is leg-count agnostic, so the unchanged "17/17" registry figure in SKILL.md stays true (sixteen cases plus the emitter-location check).

Embedded spec heredoc byte identity (the acceptance item):

- Extracted the `cat >"$d/js-cite-check.spec" <<'EOT'` body (runner :1082 to its terminator) from `git show a08e85c:tools/mutate-and-run.sh` into /tmp: 3894 bytes.
- `cmp` results, all clean: heredoc == worktree `.ufo/evidence/round-26/cite-check/cite-check.defects.spec` (3894 bytes); heredoc == `git show 622d31d:…cite-check.defects.spec`; 622d31d spec == a08e85c spec ("SPEC_SAME_BOTH_REVS"); heredoc == the sweep's retained `sweep/spec.copy` ("SPEC_COPY_IDENTICAL").

## Adjacent observations (outside the two reviewed files; not defects of this diff)

1. corpus/knowledge/fleet-kill-rate-ledger.md (unchanged between 622d31d and a08e85c) carries no measured js-cite-check row: its cite-check cells are the round-5 probe row (:94) and "probe only, 1/4 … full sweep open" (:107). The sweep this commit records closes that cell. Wave-2 item; SKILL.md:931 depends on it.
2. SKILL.md:2095 (added by this commit) cites "Entry: corpus/knowledge/mutation-case-kumitate-cite-check.md", but the file does not exist at a08e85c (`ls`: No such file or directory; `git ls-tree a08e85c -- <path>`: empty). Presumably the planned wave-2 note; until it lands, the new section cites a missing file.
3. The sweep receipt names MUTATE_TOOL sha256 d22c4025… (sweep.txt:1), a pre-embedding runner build. Legitimate: that sweep ran in --target/--defects mode against the pinned copy with the committed spec (spec.copy identical), while the retained nine-leg regression receipt names the committed runner bytes exactly (REGRESSION_TOOL sha256=fb91ef76… == sha256sum of the committed tools/mutate-and-run.sh) and closes "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)".

## Residual risk and verification gaps

- I did not run `tools/mte-interop.py --check` or `--selftest`. The --check path re-runs all nine legs; the retained receipt (.ufo/evidence/round-26/cite-check/regression-worktree.stdout, REGRESSION_DATE 2026-10-22T10:04:24Z) is the receipt of the committed runner bytes. Suggested integrator checks: `uv run --no-project --with jsonschema==4.25.1 python3 tools/mte-interop.py --check --fleet-root /home/vgpnk/Projects/shokunin` and `python3 tools/mte-interop.py --selftest` (registry rows claim 9/9 and 17/17).
- No language server was reachable from this seat for shell or Python (no lsp device), so every caller/definition/diagnostic claim above rests on direct byte reads, grep, and the executed selftest — text evidence, labeled as such; no semantic-index evidence is claimed.
- SKILL.md:1915 "cases=8 passed=8" (round-18 section) was left unchanged as a dated record, but the same sentence phrasing ("Replay: … → cases=8 passed=8") now describes an output a fresh replay no longer produces (it prints 9; the retained receipt proves it). The integrator should pick one page convention: dated records stay, current-output phrasing gets the "since round 26" treatment.
- Count-sweep coverage: primary pattern `(?i)eight|(?<![0-9A-Za-z_.])8(?![0-9A-Za-z_.])` plus a form-gap pattern `(?i)(leg|legs) 8\.|eight\.|eight,|eight;` over all three files; the runner additionally enforces its own leg-count agreement at runtime (selftest PASS above). Residual: a leg count embedded in a string matching none of those shapes would be missed; none was found.

## Tooling record

No tools installed or upgraded this session (bash, git, sed/awk for extraction, and the copied selftest run sufficed; nothing met the strict-upgrade bar). All lane access was read-only with `GIT_OPTIONAL_LOCKS=0`; writes were limited to /tmp/tameshi-r26-w1-review/ and this report file.

## Sources (opened this session, 2026-10-22)

- tools/mutate-and-run.sh at a08e85c — :108 "All nine defect specs are embedded below"; :1430 "local nlegs=9 npass=0 nfail=0 nsetup=0 st".
- tools/mte-interop.py — :318 "…differs from the nine ledger legs…"; :75-78 LEG_TABLE ending "'js-cite-check': 'TABLE_CITECHECK'".
- SKILL.md — :10 "…eight since round 18)…"; :2086 "## Ninth recorded case — round 26"; :2095 "Entry: corpus/knowledge/mutation-case-kumitate-cite-check.md".
- .ufo/evidence/round-26/cite-check/sweep/sweep.txt — "MUTATE_DATE: 2026-10-22T10:02:07Z"; closing "killed=5 survived=5 inconclusive=0 kill-rate=50%".
- .ufo/evidence/round-26/cite-check/results.tsv — ten rows, K_UNRESOLVED_SEV KILLED through S_PIN_INCLUDES SURVIVED.
- .ufo/evidence/round-26/cite-check/predictions.json — "predicted_kill_rate": "5/10" with ten prediction entries.
- .ufo/evidence/round-26/cite-check/regression-worktree.stdout — "REGRESSION: PASS (cases=9 passed=9; ledger legs exact: killed-delta<=0 flips<=0)".
- .ufo/evidence/round-26/cite-check/cite-check.defects.spec — header "rev 1205c6621a… blob sha256 40573448… 2537 lines · mode 100755" (3894 bytes, cmp-verified).
- corpus/knowledge/fleet-kill-rate-ledger.md at a08e85c — :107 "probe only, 1/4 … full sweep open".
