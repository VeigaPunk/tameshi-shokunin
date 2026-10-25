# SimplifierPredicate — Predicate match (C1)

## Task
Compare the C1 predicate sentence in `.ufo/evidence/round-39/contract.json`
with the docstring of `.ufo/evidence/round-39/guard/measure.py`; report any
word that differs.

## Finding
**No word differs.** The docstring contains the contract predicate verbatim.

- contract.json:13 — `"predicate": "C1_R39_PASS=true iff the round-39 contract
  at REV names a depth-guard regex, that regex's recorded_cases and
  depth_score equal canonical SCORECARD command D on the live runner and on a
  ledger-stripped copy of that runner, and the round-38 guard regex ^\\s*leg
  matches 0 lines of the live runner."`
- guard/measure.py:4-7 — identical sentence after the `Contract: ` prefix.

## Evidence
- Decoded-value comparison: 46 words vs 46 words, `difflib.ndiff` → no diff
  lines; `pred == sent_dec` → True.
- Raw-byte comparison: JSON encodes the regex `^\\s*leg`; the Python docstring
  source also encodes `^\\s*leg`. Both parsers (JSON, Python docstring) decode
  it to `^\s*leg`. Encoding is coincidentally identical byte-for-byte, not
  merely equal after decode.
- Line-wrapping inside the docstring (newline after `depth-guard`,
  `SCORECARD`, `and`) collapses to single spaces on word-join; no word-level
  effect.

## Non-differences worth noting (framing, not predicate drift)
- Docstring adds framing the contract does not contain: the title line
  (`measure.py:2`), the `Contract: ` prefix (`measure.py:4`), the control
  sentence "A missing round-39 contract is the do-nothing control and cannot
  pass." (`measure.py:8`, which restates contract.json:17 do_nothing_control
  in different words — not a verbatim copy, but not the predicate), and the
  exit-code line (`measure.py:10`).
- These are additive context; the predicate sentence itself is untouched.

## Command to reproduce
```
python3 - <<'EOF'
import json, re, difflib
lane = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
pred = json.load(open(f"{lane}/.ufo/evidence/round-39/contract.json"))["claims"]["C1"]["predicate"]
doc = open(f"{lane}/.ufo/evidence/round-39/guard/measure.py").read()
sent = " ".join(re.search(r"Contract: (.*?live runner\.)", doc, re.S).group(1).replace("\\\\", "\\").split())
print(pred == sent)          # True
print([d for d in difflib.ndiff(pred.split(), sent.split()) if d[0] != " "])  # []
EOF
```

## Conclusion
Predicate and docstring are word-identical. No differing words to report.
No edits made to the live lane checkout.
