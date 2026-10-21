source: S082 — .ufo/waves/round-21/original-outcomes-final.json:1369 at 51d49d58ac81a1b4ea17607c4f2c4757ed6189ad; corpus/lessons/round-21.md, Outcome-accounting erratum; round22 frozen bundle and derivation.json
verified-at: 2026-10-21; final committed-revision execution is retained in .ufo/evidence/round-22/final/verification.json
recheck: python3 tools/wave-accounting.py --bundle .ufo/evidence/round-22/bundle.json --expected .ufo/evidence/round-22/expected.json --json

# Partial artifacts do not rehabilitate failed seats

This is a same-ground calibration repair, not a newly explored province.
Round21 retained two Markdown reports from provider-dead seats:
`ProfileBashTsukuroiCensus` and `V01WitnessTests`. Its appended erratum
preserves the original wrong inference and the actual terminal statuses.
The reusable rule is to separate three observations:

| Observation | What it establishes | What it cannot establish |
|---|---|---|
| registered exact name/agent ID/role | which dispatched identity belongs in the denominator | whether execution completed |
| retained terminal callback status | declared completed or failed outcome for that identity | cryptographic provider authenticity |
| Markdown report exists | an artifact was written, possibly partial | successful completion |

`tools/wave-accounting.py` checks a digest-pinned bundle, nonempty exact
membership, unique agent identities, final status vocabulary, identity/role
agreement, no declared replacement, and caller totals. It inventories
failed-with-report seats without changing their status. Report prose and
file presence never supply the completed count. It reads no live provider
or orchestration configuration and cannot authenticate an edited callback
snapshot whose expected digest is also intentionally replaced.

The frozen round22 bundle is an explicit projection, not the original raw
callback stream: `derivation.json` pins the source revision and source-file
hashes. Completed callbacks that omitted `replaced` receive `false` from
the explicit round21 no-replacement declaration, not from treating an absent
field as independent proof. Reports are a frozen basename-existence census;
their contents are not required to establish the callback count.

Reproduce from the lane root:

```sh
python3 tools/wave-accounting.py --selftest
python3 .ufo/evidence/round-22/measure.py --repo "$PWD"
python3 tools/wave-accounting.py --bundle .ufo/evidence/round-22/bundle.json --expected .ufo/evidence/round-22/expected.json --json
python3 tools/wave-accounting.py --bundle .ufo/evidence/round-22/wrong-count-bundle.json --expected .ufo/evidence/round-22/wrong-count-expected.json --json
```

The last command is deliberately red: only the preserved wrong claimed
wave2 totals differ from the corrected bundle; the expected digest matches
that wrong-count input, so the intended failure is `TOTAL_MISMATCH`, not
snapshot corruption. The final verification receipt records observed exits,
streams, instrument hashes and measured commit rather than borrowing a
historical success.

Keep denominators separate: eight synthetic rejection predicates are
capability discrimination, the complete retained population is146 seats,
and the original mistake class has two false-positive instances. Eight
tests do not mean eight historical defects; selftest green is not outside
claim admission, independent promotion evidence, or provider authentication.

Round22 source-retention addendum: build review identified that many original
outcome rows carried no raw callback text. The reachable local harness records
and retained wait recoveries have now been copied into
`.ufo/evidence/round-22/round21-callbacks.json`; the separate corroboration file
records146 matching identity/status/role observations. This repairs retention,
not authentication. It neither rewrites the old outcome files nor enlarges
the frozen eight-predicate claim denominator.
