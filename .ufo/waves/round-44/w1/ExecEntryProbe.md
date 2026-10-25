# ExecEntryProbe — provenance trio

Axis: freshness.

No round-44 draft knowledge entry existed in the available wave/repo file listing, so used `corpus/knowledge/r43-survivor-resolution-rule.md` as the requested model. Its existing trio is at lines 3–5; the S160 page URL is confirmed by the frozen snapshot `.ufo/evidence/round-44/sources/stryker-equivalent-mutants.html` (title/URL metadata and equivalent-mutant passage at line 16). The probe is `/tmp/tameshi-r44-ExecEntryProbe-/probe.py`; it requires `source:` to contain both S160 and the Stryker equivalent-mutants URL, `verified-at:` to match YYYY-MM-DD, and `recheck:` to be YYYY-MM-DD or a supported cadence.

The model's original values correctly fail (source lacks S160/URL, verified-at includes non-date annotation):
```
source: FAIL (S089 (held, re-opened), S159 (new); S155 (held), S158 (held))
verified-at: FAIL (2026-10-25 (snapshots under .ufo/evidence/round-43/sources/, byte-identical double fetch))
recheck: PASS (180d)
total: FAIL
positive_exit=1
```

Synthetic conforming trio control:
```
source: S160 — https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/
verified-at: 2026-10-25
recheck: 180d
```
Output:
```
source: PASS (S160 — https://stryker-mutator.io/docs/mutation-testing-elements/equivalent-mutants/)
verified-at: PASS (2026-10-25)
recheck: PASS (180d)
total: PASS
positive_exit=0
```

Then removed `source:`; negative control:
```
source: FAIL (missing)
verified-at: PASS (2026-10-25)
recheck: PASS (180d)
total: FAIL
negative_exit=1
```

No lane checkout file changed; only the assigned report was written. No tools installed. Blocker/risk: the probe was exercised against the extant model and synthetic conforming control, not the future S160 knowledge entry (not available at probe time); parent should apply it to the eventual entry.