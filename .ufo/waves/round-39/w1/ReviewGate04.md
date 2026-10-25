# ReviewGate04 — census classification attack: `tools/env-diff.py` (Tameshi round 39, wave w1)

Seat: ReviewGate04 (leaf, no dispatch). Frozen contract read, not edited. Live lane checkout not
edited. No tool installs performed (pacman paused; none needed). No LSP device was available in
this seat's inventory; findings rest on direct execution of the frozen patterns against the file —
which is the dispositive test here, since the census itself is a regex classifier, and on a
read-only census run.

## Axes named (godspeed)

- A1 **Completeness**: does the frozen `WRITE_RE` see every write site of gate `env-diff.py`?
- A2 **Honesty of the named limits**: does the tool docstring's limit list actually cover any gap?
- A3 **Gate impact**: can any miss flip `C2_R39_PASS`?

## Ground truth

- Working tree `tools/env-diff.py` is byte-identical to base rev
  `50aadd1bbd94e43cd3fcfb81459414394db2dc35` (verified with
  `git show 50aadd1b…:tools/env-diff.py | diff - tools/env-diff.py` → identical). Line citations
  therefore hold for REV-byte classification of this gate as of now.
- Census tool sha256 `bc8c660c56f871f85dad8912be28446293fd63f62b4fd1c16eb153f7a27edc62` —
  equals the contract C2 pin (context only; not my claim to judge).
- `python3 tools/write-path-census.py --census .` →
  `GATE env-diff.py write_sites=4 unflagged=0` (21/21 classified, exit 0).

## F1 (Medium — census completeness, not covered by a named limit): line 238 mkdir is a real, persistent, non-scratch write the frozen pattern cannot see

**Cite:** `tools/env-diff.py:238`

```python
        a.out.parent.mkdir(parents=True, exist_ok=True)
```

Every production run of env-diff.py creates directory entries on live disk outside any scratch
sandbox, immediately before the counted receipt write at line 239. `WRITE_RE`
(`open(...,'w…') | .write_text( | .write_bytes(`) is structurally blind to it.

**Evidence (exact command):**

```
python3 - <<'EOF'
import re
WRITE_RE = re.compile(r"""open\s*\([^)]*['"](?:w|a|w\+|a\+|wb|ab)['"]""" r"""|\.write_text\s*\(""" r"""|\.write_bytes\s*\(""")
EXTRA = re.compile(r'\bopen\(|\bwrite|\bmkdir|\bchmod|…')  # exhaustive write-ish vocabulary
for n, line in enumerate(open('tools/env-diff.py'), 1): …
EOF
```

Result: frozen pattern hits exactly lines **66, 171, 184, 239** (= the census's `write_sites=4`);
missed write-ish sites: **63, 64** (`(root / "home").mkdir()`, `(root / "tmp").mkdir()`, scratch),
**67** (`target.chmod(0o755)`, scratch, metadata), **170** (`repo.mkdir()`, scratch),
**174–179** (`git("init"/"add"/"commit")` child writes, scratch), and **238** (non-scratch,
persistent).

**Named-limit check** (tool docstring, `tools/write-path-census.py:2-7`): the three specific
limits do **not** apply to line 238:

1. *Shell redirects* — no; it is a Python `Path.mkdir` call, no shell involved.
2. *Writes whose path is not on the same line as the call* — no; `a.out.parent` is on the line.
3. *Not a claim that every write in every language is seen* — a cross-language hedge; line 238 is
   Python, the census's own implementation language, a plain single-line call with no lexer
   ambiguity. Only an unlimited reading of "not a claim that every write … is seen" swallows it —
   a reading under which `live_write_sites` is unfalsifiable and the census number is meaningless.

**Verdict:** the pattern's named limit does not cover it. `write_sites=4` for env-diff.py is a
lower bound; the true persistent-write site count is ≥5. `unflagged=0` is unaffected (line 238
matches no `EXPECTED_RE` string).

## F2 (Low — covered by the hedge, only with a stretch): child-process disk writes at lines 174–179

`tools/env-diff.py:177-179` — `git("init", "-q")`, `git("add", "target.sh")`,
`git("commit", "-qm", "fixture")` write a full `.git` object database to live disk during
selftest. Not shell redirects (argv-list `subprocess.run`, `write-path-census.py`'s own named
limit does not name subprocess side effects), but they are execution sites in the tool text
rather than write idioms, so the "not a full lexer / not every write is seen" hedge is the
plausible cover. Reported for depth; graded *covered-by-hedge*.

The remaining misses (63, 64, 170 `mkdir`; 67 `chmod`) are scratch-sandbox writes inside
`TemporaryDirectory`. The census's `SCRATCH_RE` vocabulary shows scratch is a recognized category,
but scratch writes are never counted at all — consistent with the census's content-write-API
reading; subsumed by F1's umbrella, no separate defect.

## Gate impact

`.ufo/evidence/round-39/census/measure.py` composes
`ok = planted_ok and mutant_killed == 1 and sha_ok == 1 and gates_ok`; `live_write_sites` and
`live_unflagged` are emitted but are not PASS conjuncts (matching contract C2 kill_rule:
"live_unflagged is reported, not a pre-declared PASS conjunct"). **No finding here can flip
`C2_R39_PASS`.** This is a depth finding on the honesty of the reported census numbers only.

## Residual risk and verification gaps

- `FLAG_RE` is file-level (`write-path-census.py` `classify_text`): any `--update`-ish string
  anywhere in a gate suppresses `unflagged` for **all** of its write sites. env-diff.py has no
  hit, so `unflagged=0` stands for this gate; other 20 gates not audited for flag absorption
  (outside this slice).
- `classify_text` counts lines, not sites: two writes on one line count once. No such line in
  env-diff.py; general caveat on `live_write_sites`.
- If the wave edits env-diff.py before the deciding run, line numbers shift and F1 must be
  re-checked against the new REV bytes (the mkdir idiom is the claim, not the number 238).
- Census run was read-only (`--census .` reads `tools/`, prints); no lane state, index, or
  sibling lane touched.
