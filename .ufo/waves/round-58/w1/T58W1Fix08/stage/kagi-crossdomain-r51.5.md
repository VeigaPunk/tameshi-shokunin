# Cross-domain evidence: R51.5 (kagi drift-pins)

**Defect.** Tameshi R51.5 routes an owed report of the unanchored verdict-word checks in kagi's `corpus/drift-pins.sh --selftest`; it explicitly says not to modify kagi. The inspected kagi tip is `c49023b773b69de983f0e6eb7e5867ceb5c2c634`. The current source shows the `run` helper capturing the command output at line 400 (`out=$(...)`); the verdict assertion at line 403 is `grep -q "$3" <<< "$out"`, which treats `$3` as a regular expression and does not anchor or escape the expected verdict. Its failure diagnostic at line 404 likewise prints `no /%s/ in output`. At line 158 the gate emits `DRIFT   %s %s` with the path and differences; this path-printing diagnostic can interfere with a verdict-word search if the search is not constrained to an exact verdict line. The routed item describes these as the three sites at approximately 400, 403 and 158 at the pinned leg revision; the current inspected checkout's exact lines are reported above, not asserted to be the historical pinned revision.

**Why it matters.** A matching substring or regex metacharacter can make a selftest accept unintended output, while path text in a DRIFT diagnostic can satisfy a verdict-word search unrelated to the actual verdict. This weakens the selftest's evidence that its expected verdict was emitted.

**Recommendation.** In kagi, use an exact, line-anchored verdict assertion that safely handles the expected value, and make the path-printing DRIFT assertion discriminate the actual verdict line from diagnostics. Preserve kagi's ownership: this is cross-domain evidence/recommendation only; no external file was edited.

**Evidence commands and output.**

- `nl -ba /home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/drift-pins.sh | sed -n '150,162p;392,407p'` printed line 158 `printf 'DRIFT   %s %s\n' "$p" "${diffs[*]}"`, line 400 `out=$(...)`, line 403 `elif ! grep -q "$3" <<< "$out"; then`, and line 404 the unanchored `no /%s/ in output` diagnostic.
- `git -C /home/vgpnk/Projects/shokunin/kagi-shokunin rev-parse HEAD` printed `c49023b773b69de983f0e6eb7e5867ceb5c2c634`.
- `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 2a32aa8228d5f86a85c81a923a3148bf792a9538:corpus/lessons/round-51-verifier-spotcheck.md | nl -ba | sed -n '120,136p'` printed R51.5 at line 130: report the three sites cross-domain and do not edit kagi.

**Status at base.** `open`: the routed item calls for cross-domain evidence in the next report, and the pinned round-51 lesson promises that filing. The staged note is the intended resolution evidence for the round-58 ledger row. Planned commit subject: `Record R51.5 kagi cross-domain drift-pins evidence`.
