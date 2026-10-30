### Round-13 gate/probe registry

| Name | Kind | Entry command | Verdict map | Self-test command | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| six-leg content disposition | probe | `python3 tools/pin-disposition.py --manifest .ufo/evidence/round-13/pin-manifest.json --root /home/vgpnk/Projects/shokunin` | 0 observations, including changed/unavailable; 2 invalid input/could-not-evaluate; selftest 1 failed | `python3 tools/pin-disposition.py --selftest` | `.ufo/evidence/round-13/pin-manifest.json`; canonical leg mapping and literal selftest labels in tool | normal mode read-only lane/sibling files and git; selftest isolated temp repos only | tameshi |
| exposed witness provenance companion | gate | `python3 tools/witness-metadata.py --check --companion .ufo/evidence/round-13/witness-metadata.json` | 0 metadata_consistent/clean; 1 metadata_inconsistent/failed; 2 input_unavailable or snapshot_tampered/could-not-evaluate, including usage | `python3 tools/witness-metadata.py --selftest` | literal frozen input digests and expected kind/disclosure in tool; companion expected verdict; the companion `.ufo/evidence/round-13/witness-metadata.json` plus the four frozen round-12 files (`summary.json`, `declaration.json`, `declared.tsv`, `rerun-20261020T035435Z/summary.json`) — not `.ufo/evidence/round-13/expected.json`, which this gate never reads | check read-only lane inputs; selftest isolated temp trees only | tameshi |

No registry row changes rank, SHONEN authority, or the six recorded cases at
this write (a seventh case is recorded since round 16, `## Seventh recorded case and full-page cold-read — round 16`).
The historical summary's producer SHA names the producer that actually ran,
not the repaired current producer. No old evidence hash is regenerated.
PIT source clarification: S048 supersedes S047's object-specific
paraphrase; retain only the supported distinction “item 4 is
prioritisation, not a reuse skip”. No test-versus-mutation pronoun claim
is needed by this method.

