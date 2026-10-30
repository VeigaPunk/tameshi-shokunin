# T57D4Panel — documentary panel-provenance review

Axes: six-id attribution accuracy; blindness disclosure fidelity; committed provenance completeness. Recommendation only: **UNVERIFIED; no admission**. No counter, candidate gate, test, build, exploit, or receipt generation was executed. No installation or production edit. LSP unavailable: `read xd://lsp` returned `No such tool`; the following is literal documentary evidence, not semantic-reference proof.

All paths below beginning `L/` expand to the absolute lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin/`. Source reads are the local candidate snapshot; read-only Git inventory observed HEAD `120a055d78b0f35f7f72c4c2a005ef7770f6d458`, not the assignment's earlier C0b. No claim that these are identical snapshots.

## Findings by severity

### High — six replacement seats lack the orchestrator results artifact required by canonical provenance logic

`L/.ufo/evidence/round-57/c1/panel.json:90-96,122-128,170-176` routes the six governed ids to three `T57W3Reseat*` seats. Their metadata is present and committed, but `L/.ufo/waves/round-57/w3-results.json` is absent locally and from the observed HEAD inventory. The w2-results literal search contains only the three original W2 seats, not replacement names.

Canonical source `L/.ufo/evidence/round-57/c1/measure.py:249-260` unions `results[].name` from w2/w3 results and requires `seat in listed`; lines 267-270 count each unmatched id. Thus the available evidence cannot support a zero provenance-shortfall claim for these six ids. **[INFERENCE from source, not executed]** With these source files and inventories, all six replacement ids lack the required name membership. Hash matching alone does not satisfy this arm. Supply genuine orchestrator-written replacement results at the deciding revision; do not synthesize or forge them.

Observed documentary commands/output:

```text
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin ls-tree HEAD -- .ufo/evidence/round-57/c1/panel.json .ufo/waves/round-57/w3-results.json .ufo/waves/round-57/w3/T57W3ReseatR515R516.json .ufo/waves/round-57/w3/T57W3ReseatR525R526.json .ufo/waves/round-57/w3/T57W3ReseatR542R543.json
100644 blob 99426161246ead1ba120d58282e9eb3ef4ba3cd0 .ufo/evidence/round-57/c1/panel.json
100644 blob f3c4570da9775cc1bb7ce96c1f7afac9fd9dfbfb .ufo/waves/round-57/w3/T57W3ReseatR515R516.json
100644 blob 33624953be3291c5ac37f37d64f90c6641349d46 .ufo/waves/round-57/w3/T57W3ReseatR525R526.json
100644 blob b5de0e4beaed50e7c2fe4f51b349c4aa6283e8f3 .ufo/waves/round-57/w3/T57W3ReseatR542R543.json
```

`glob` of absolute `L/.ufo/waves/round-57/*results*` returned only `w2-results.json`, `w1-results.json`. `grep` for `T57W[23](ReseatR(515R516|525R526|542R543)|PanelR(515R516|525R526|542R543))` over absolute w2/w3 results returned W2 names at w2-results lines 32,56,92, and `Skipped missing paths: /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3-results.json`.

### Medium — panel authenticity pin remains explicitly unfinished

`read /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-57/c1/measure.py:104-114` exposed line 111:

```text
PANEL_SHA256 = 'PIN_PENDING_SET_BY_L1_AFTER_THE_BLIND_PANEL'
```

`L/.ufo/evidence/round-57/contract.json:153-154` requires the digest of committed panel bytes before scoring. Its lines 145 and 201 acknowledge pending/unverified state, so this is a missing completion prerequisite, not evidence of a concealed pass. A matching seat-file hash does not finish the panel pin. Resolve the genuine committed-panel pin through the authorized integration process before any claim of calibration completion.

## Six-id comparison and blindness disclosures

| Governed id | W2 verdict | Candidate / clean W3 verdict | Candidate seat / commit |
|---|---|---|---|
| R51.5 | open | open | T57W3ReseatR515R516 / null |
| R51.6 | fixed | open | T57W3ReseatR515R516 / null |
| R52.5 | fixed | fixed | T57W3ReseatR525R526 / 218bc6b5c25d6a3c57dd44600febd552f0167cee |
| R52.6 | open | open | T57W3ReseatR525R526 / null |
| R54.2 | open | fixed | T57W3ReseatR542R543 / 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb |
| R54.3 | open | fixed | T57W3ReseatR542R543 / 9cf0146b94ddba12d454ebf7288ce6e5c5d535bb |

Evidence: candidate panel lines 13-14,21-22,33-34 and detail lines 90-96,122-128,170-176; each W2 and W3 seat JSON `:1-25` (W3 `:1-15`) under absolute `L/.ufo/waves/round-57/w2/` and `w3/`. All six candidate verdicts, seat names and commit fields agree with replacement JSON. The changed R52.5 fixing-commit attribution is preserved, not silently copied from the W2 `5b703c6...` attribution.

- `L/.ufo/waves/round-57/w2/T57W2PanelR515R516.json:16-23` explicitly voids both verdicts after out-of-clone fleet/sibling reads.
- `L/.ufo/waves/round-57/w2/T57W2PanelR542R543.json:4-5` marks `blind_panel_valid=false`, describes fleet/verdict-artifact reads and voids the verdicts.
- `L/.ufo/waves/round-57/w2/T57W2PanelR525R526.md:9-22` discloses a forbidden post-verdict lane status listing while calling verdicts unaffected. Its JSON `:1-15` omits this disclosure. The contract `:147-149` correctly treats all three W2 seats as breached and makes W3 authoritative; the current candidate does not use these six W2 verdicts. The JSON omission remains an audit limitation, not an observed contaminated replacement.
- Clean replacement scope is explicitly asserted in `L/.ufo/waves/round-57/w3/T57W3ReseatR515R516.md:5-11`, `T57W3ReseatR525R526.md:3-5`, `T57W3ReseatR542R543.md:3-5`. These are authors' disclosures, not independent transcript certification. Replacement JSONs contain no machine-readable blindness attestation; their reports supply that context.

Hash sweep (read-only; command `sha256sum` with the three absolute W3 JSON paths):

```text
7ad2034978b1d075bce75fa9dde2d4aaec96ade149ce1da9cd3cecd4bbf208c5  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3ReseatR515R516.json
80d3ed39cfd341fb9a3bf4205e65955992eb609117ef257725a8c3127896f3ce  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3ReseatR525R526.json
3dbbc188068808fcb6333d8e5fa3724e66d207314d4eeceb61d0627d6cb2e4ac  /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/waves/round-57/w3/T57W3ReseatR542R543.json
```

All match candidate `L/.ufo/evidence/round-57/c1/panel.json:286-288`. This establishes local byte linkage only, not the absent results membership or frozen authenticity pin.

## Residual risk and verification gaps

No independent replay of historical seat reads, no counter execution, and no freeze/admission verification. R51.5/R52.6 external-report availability and R54.2 supersession rather than external-byte repair are explicitly limited in replacement reports (respectively lines 19; 28-30; 24-26). This review does not re-adjudicate those underlying defects or claim 64/64 no-harm, saturation, or C1/C2 passage. The canonical panel-provenance function validates hash/verdict/name membership, not blindness, base identity, or detail.commit equality (`measure.py:242-270`); current six-item equality was therefore checked documentarily rather than attributed to the counter.

Self-evaluation: accuracy 4/5 (local snapshot, no transcript certification); completeness 4/5 (all six ids covered, runtime deliberately prohibited); clarity 4/5 (long absolute-path evidence abbreviated by an explicit prefix); actionability 4/5 (genuine results and pin prerequisites named, integration not authorized here); conciseness 4/5 (receipt excerpts add length). Overall 4.0/5. Highest-impact remaining evidence: authentic orchestrator membership, committed panel pin, independent blindness audit if required. These are gaps, not passes.
