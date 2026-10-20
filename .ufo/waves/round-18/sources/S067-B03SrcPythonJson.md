# S067 — draft row (B03SrcPythonJson, round 18 wave 1)

Decision: ADMITTED as `mined` (provisional id S067). Duplicate check: `grep -rn 'docs.python.org/3/library/json' corpus/SOURCES.md` on the lane root returned no match (no `DUPLICATE`). Provisional id note: the committed registry at `183f87b899e6cae46be98d251cbc87fb5118f6ca` ends at S064 and states `Next unused id: S065` (`git show 183f87b:corpus/SOURCES.md`); S067 is the id this ticket assigns, so the L1 must confirm S065–S066 are not taken by sibling seats before the row lands.

## Row

| S067 | Python json — JSON encoder and decoder (Python 3.15.0 docs) — https://docs.python.org/3/library/json.html | docs | A | Python `json` decoder's default acceptance of NaN, Infinity and -Infinity, and the `parse_constant` hook that receives them | §Standard Compliance and Interoperability › Infinite and NaN Number Values; json.load() parameter `parse_constant` @ Python 3.15.0 docs, fetched 2026-10-20 (version-coupled; no commit pin) | json.loads accepts Infinity, -Infinity and NaN by default although RFC 7159 does not permit them; parse_constant is called with each such literal, so a registry loader can reject it by name instead of trusting the default | mined | 2026-10-20 | on-release | .ufo/evidence/round-18/defect-probes.py |

Cell check: 11 cells between 13 pipe-delimited fields (NF=13); no `|` inside any cell; tier A (official docs for the module's own behaviour); kind `docs`; status `mined` (used-by path is the P09 probe owner that will cite it; the census existence check passes only once that file lands); recheck `on-release` (docs are version-coupled, same cadence as S049 and S055).

## Gate

- URL: https://docs.python.org/3/library/json.html
- Access date: 2026-10-20 (read tool; fetched body titled "json — JSON encoder and decoder — Python 3.15.0 documentation"; no mirror needed).
- Anchor: section "Standard Compliance and Interoperability" › "Infinite and NaN Number Values" (page body lines 559–623 of the fetched text); and the json.load() parameter list entry for `parse_constant` (fetched lines 316–326 region of the parameter list).
- Quote (primary, verbatim from the fetched body in "Infinite and NaN Number Values"; 20 words by `wc -w`):
  > by default, this module accepts and outputs `Infinity`, `-Infinity`, and `NaN` as if they were valid JSON number literal values
- Quote (hook, verbatim from the json.load() `parse_constant` parameter entry; 14 words by `wc -w`):
  > This can be used to raise an exception if invalid JSON numbers are encountered.
- Second hook sentence (verbatim, Infinite and NaN section; 13 words): In the deserializer, the parse_constant parameter can be used to alter this behavior. (the source has `*parse_constant*` italics; the markup is dropped here.)
- Host cross-check (not a source claim; observation only): `python3 -c 'import json; print(json.loads("[NaN, Infinity, -Infinity]"))'` on Python 3.14.8 printed `[nan, inf, -inf]` (exit 0). Confirms the documented default on the host interpreter; P09's fixture must still run against the lane's own registry-check.

## Support for the purpose

Purpose: C2 P09 (registry-check must reject `timeout_s` given as NaN or Infinity). The page states the default acceptance and names the hook that makes rejection possible, so the probe's premise (the decoder accepts the literal unless the caller intervenes) is primary-sourced. Supports the purpose: yes. Not rejected.
