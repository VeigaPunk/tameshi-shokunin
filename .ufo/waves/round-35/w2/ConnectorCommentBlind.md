# Round-35 w2 — ConnectorCommentBlind (cross-lane comment-blindness scan)

Leaf connector, godspeed. Scan pin: **7da6e076c2e25936a3b60dde2a4080d8f05b7e5b** (lane tip at
dispatch). Scratch: `/fast/scratch/hyaku/tameshi-r35-seats/ConnectorCommentBlind/` (lane checkout
read-only, re-cloned fresh — the attempt-1 leftover clone predated the pin and could not read its
tree; `git clone` + `checkout --detach 7da6e076…` exit 0). No subagents, no labrat, no installs
(no `pacman`, nothing needed). The only lane-repo write is this report.

Pins verified at the scan pin (all exit 0, match `contract.json` frozen_artifacts):

```
sha256sum tools/tally-audit-v3.py    ef98fc5367cdb12c71b8b0ddfb5b83835100831f545f6510437dc84014865885
sha256sum tools/tally-audit-v2.py    7b11ba25aead93678aef50606b7521fb7c3a85bea47b5ec220a47865b3598d10
sha256sum tools/mutate-and-run.sh    a7d3f2dd7d47511a4769aab610dd85d1a37e77b32f14fd763f3af638dd912eb9
sha256sum .ufo/evidence/round-35/c1/c1-measure.py 515b0b1b00b970f31c08e80eb74512ecae0cf1082ddeccfcb373e810cd0559e8
sha256sum .ufo/evidence/round-35/c2/c2-measure.py 67bb71188cde259088646f960b6fda8e0a217fad5d8260e379054b381018f9cc
```

## 1. What I attacked

Assignment class A (counts name substrings without stripping comments) and class B (parser counts
braces/quotes char-wise), across every sibling gate in the lane's `tools/` registry surface that
structurally parses text: `tally-audit.py` (r32 object), `tally-audit-v2.py` (r35 control),
`tally-audit-v3.py` (the measured object — adjacency, not fix), `bash-witness-study.py`,
`mte-interop.py`, `trace-inputs.py`, `mutate-and-run.sh`'s embedded spec parser, and the round-35
counters. JSON/TSV-domain gates (`registry-check`, `evidence-disposition`, `witness-metadata`,
`pin-disposition`, `receipt-*`, `wave-*`, `context-capture`, `env-diff`, `repeat-control`) were
grep-swept for the classes (`.count(`, `findall`, char-wise `depth`/quote loops): no instances —
their counting is over structured lists, not source text (bounded negative).

## 2. Live probes (all commands run with `cwd=…/work`, system `python3`)

Five runner copies built from the pinned runner by single anchored `replace`s (bench:
`python3 bench.py`, **exit 0**, 84 s; p5 follow-ups separate, exits below). Anchors asserted
unique (`A_DONE`×1, `A_STJS`×1):

| copy | edit (inert) | sha256 |
|---|---|---|
| p1 | after tally `done`: `  local r35probe='}'` (close-brace in single-quoted DATA) | `448c11e5…4a7f3` |
| p2 | same, `  local r35probe='{'` (open-brace in DATA) | `1d1d5be1…e797` |
| p3 | after `st_js=$?`: `  # st_js is captured immediately above; inert comment` | `8c654bc7…3b57` |
| p4 | after `done`: no-op heredoc `: <<'R35NOTE'` whose body holds indented `  }` | `a29ee4d1…7cbe` |
| p5 | same heredoc, body line `}` at column 0 | `a79e745d…ac69` |

**Behavioral identity (ground truth per the sealed rule):** each copy's TRUE tally tail (cut at the
function's real closing brace — heredoc-aware for p5) driven against pristine under **six**
(root,auto,KEEP) triples — the four audit triples plus the runner's REAL auto root
(`mktemp -d /tmp/tameshi-r4-2-regression.XXXXXX`, auto=1, KEEP∈{0,1}) — over vectors all-zero,
one-1/2/3/255, mixed `[1,2]`,`[0,1]`, `[1]×9`, `[2]×9`, trailing-1, comparing (exit, FULL stdout):
**identical-to-pristine=True for p1–p5 on every triple and vector** (bench §2, exit 0; p5 re-drive
after a heredoc-aware tail fix, exit 0 — a naive first-`}` cut had produced a false `False` that was
my extractor's artifact, not a divergence).

**Audit verdict matrix** (`python3 tools/tally-audit-{v3,v2,py} --runner <copy>`):

| copy | v3 (`ef98fc53`) | v2 | r32 |
|---|---|---|---|
| pristine | rc=0 PASS (30,316 vectors ×4 cfg) | rc=0 PASS | rc=0 PASS |
| p1 quoted `}` | **rc=2 SETUP** (driver: `unexpected EOF while looking for matching ''` — extracted block ends `…local r35probe='`) | rc=2 SETUP | rc=0 PASS |
| p2 quoted `{` | **rc=2 SETUP** (`run_regression() has unbalanced braces`) | rc=2 SETUP | rc=0 PASS |
| p3 comment names leg | rc=0 PASS (fix holds live) | **rc=1 FAIL `head`: "leg st_js appears 3 times … want exactly 2"** | rc=0 PASS |
| p4 heredoc `  }` | **rc=2 SETUP** (driver: `here-document … delimited by end-of-file (wanted 'R35NOTE')`) | rc=2 SETUP | rc=0 PASS |
| p5 heredoc `}` col 0 | **rc=2 SETUP** (same heredoc warning) | rc=2 SETUP | **rc=2 SETUP** (`0/331 results`) |

**The deciding counter shares the walk** (import of the frozen `c1-measure.py` is import-safe;
extraction on p1/p4 returns `block=333B` ending mid-token `…done\n\n  local r35probe='` /
`…done\n\n  : <<'R35NOTE'\n  `; p2 → `SystemExit: SETUP: unbalanced run_regression braces`) — its
`run_block` would fail identically, so the class is fail-closed at measurement too.

## 3. Findings (ranked)

### BOUND-1 — v3's brace walk is DATA-blind: quoted-string and heredoc braces still counted (fail-closed refusals of behaviorally pristine copies)
`tally-audit-v3.py:150-193` `code_view` blanks only comment text (quote state is used solely to
find `#`); `regression_body` (`:196-212`) then counts `{`/`}` **char-wise over that view**, so a
`}` or `{` inside single-quoted data (`:1432` region, after the tally loop) or inside a heredoc
body truncates or extends the audited span and the block slice ends mid-token. Four
behaviorally-identical copies (p1/p2/p4/p5, identity proven under the real auto root) are REFUSED
(rc=2, SETUP). Same bytes in `c1-measure.py:132-153`. Not a false accept — every truncation shape
I could construct cuts inside a quote/heredoc whose terminator trails the cut, so the extracted
block always breaks the oracle driver (p1/p2/p4/p5 all SETUP; the geometry is forced: the
net-zeroing brace is data by construction). The claim's surface member (3) says "every structural
scan runs on a quote-aware code view with comments blanked" — true to the letter, but S102's own
text (committed snapshot `.ufo/evidence/round-35/src/s102-posix-chap02.html:95-96`) classifies the
here-document as "another form of quoting", so "quote-aware" overstates: braces in ALL four quoting
mechanisms S102 names still drive the walk. The round-34 'comment `}` closes the body early' class
is half-closed — comments yes, quoted/heredoc data no. If any sealed accept specimen uses this
shape, `ho_accept` breaks and C1 honestly fails; none is in the landed panel (verified: the 8
committed panel JSONs at the pin are the A4 set), so **C1 as measured today is not falsified** —
this is a real accept-side coverage bound, fail-closed.

### BOUND-2 — r32's line-anchored slicer: different blind spot
`tally-audit.py:98-105` `text.find('\n}\n')` / `:111-115` `rindex('\n}\n')`: immune to quoted and
indented data braces (p1/p2/p4 PASS — a useful accidental contrast), but a column-0 `}` line inside
a heredoc refuses a pristine copy (p5 rc=2). Every tally-audit generation has a data-blind body
slicer; each is blind to a different subset.

### CONFIRMED (receipted) — v2 class A live at the pin
`tally-audit-v2.py:331-334` — the twice-only rule counts raw name substrings
(`cnt = head.count(nm)`); p3 → rc=1 `CHECK head FAIL … "leg st_js appears 3 times"`. This is the
round-35 control's own receipted discrimination (`c1-v2-control.stdout:3-5`); my direct run adds
the standalone command + exit at the pin. No class beyond the three receipted ones (comment-name,
comment-brace, comment-esac) found in v2 — its p1–p5 refusals are the same BOUND-1 walk it shares.

### BOUND-3 — the spec-parser trio re-implements the runner's parser with divergent comment semantics
Authoritative parser `mutate-and-run.sh:364-404`: blank→skip, **`line.lstrip().startswith('#')`**
→skip (indented comments are comments), anything else → `die('not a directive')`. Differential run
(exit 0, imported `parse_spec` from both tools; runner semantics transcribed from those lines):

| spec input | runner | bash-witness-study.py:287-295 | mte-interop.py:113-124 |
|---|---|---|---|
| `# plain comment` | ok | ok | ok |
| `   # indented comment` | ok (skip) | **Cannot "spec line 4: not a directive"** (requires col-0 `#`) | ok (skip) |
| stray non-directive line | **DIE** | Cannot | **ok — silently skipped** |
| `   @old a` (indented directive) | DIE | Cannot | silently skipped → `old=None` → own Setup check catches |

Two sibling gates parse the pinned spec format without the runner's comment/strictness semantics:
the study tool refuses runner-valid specs (fail-closed; its selftest has no indented-comment case
pinning the semantics — `bash-witness-study.py:1370-1399` covers only col-0 shapes), and
`mte-interop` leniently accepts a spec the authoritative runner would refuse (reachable only if a
kept `spec.copy` diverges from what the runner ran; its `source.count(@old)==1` check at `:150`
still guards the mutant build, so verdict impact is bounded). Both are adjacent evidence for
round-36: one parser, three behaviors.

### HYGIENE-1 — dead comment-blind brace helper retained in v3
`tally-audit-v3.py:215-223` (and v2 `:135-143`): `brace_depth_at` — char-wise brace count over the
RAW text prefix, no comment blanking — has **zero call sites** in either tool (grep
`brace_depth_at\(` matches only the two definitions). Dead code carrying exactly the round-34
class; delete or de-blind if round-36 ever revives it.

### HYGIENE-2 — counter's internal tool pin was stale at the dispatch pin (resolved by A6 mid-wave)
At 7da6e076, `c1-measure.py:46` still read `TOOL_SHA256 = 'da23d3a2…'` (freeze-time v3) while A4's
`pins_new` had re-pinned the tool to `ef98fc53…` (`contract.json:109-112`); deciding mode requires
equality (`:358` reads the tool at REV, `:374` `tool_sha_ok` with `a.tool=None`, `:445`
`ok=… and tool_sha_ok`), so every admissible post-A4 deciding rev scored `tool_sha_ok=0` →
`C1_R35_PASS=false` deterministically. Verified the live tip **68f25573** already fixes this
(counter pins `ef98fc53…`, counter sha `d27e6769…`, amendment **A6** `contract.json:129-138`
records `515b0b1b → d27e6769`). No action needed; recorded because it was a total fail-closed
blocker for the deciding run for part of this wave's lifetime.

## 4. What I could NOT break (proofs)

- **No false accept on v3 from data braces at this pin**: all five shapes refuse (matrix above);
  the cut geometry argument (BOUND-1) plus the four refusals bound the class to fail-closed.
- **v3's round-35 fixes hold live**: p3 (comment names a leg) PASSes v3 rc=0 with 30,316 vectors ×
  4 configs, 0 mismatches; pristine baseline PASS rc=0 on all three generations.
- **`trace-inputs.py:193-223`** (`split_args`): char-wise quote/escape/`()[]{}` nesting parser —
  over strace C-quoted argument strings, its correct domain; no shell-comment surface. Not a class
  instance.
- **`c2-measure.py`**: grep over the frozen counter for `count(`/`depth`/`brace`/`comment`/`quote`
  → no structural parsing at all; the pending C2 re-count at head is not exposed to either class.
- **v2**: no new class beyond the three receipted control lines; everything else it shares with
  v3 fails closed.

## 5. Connector move (one bounded proposal)

**Route BOUND-1 as the first round-36 Hold, with this fix direction:** extend `code_view` to blank
heredoc bodies and treat open single/double-quote spans as data for the brace walk (keep the
same-length, newline-preserving discipline the tool already documents), skip brace counting inside
quote spans, and pin it with new selftest seeds: quoted-`}` and quoted-`{` accept seeds, a heredoc
accept seed, and p5's column-0 heredoc shape — all must PASS while every receipted kill seed still
dies (the runtime oracle is untouched; only the slicer changes). Also land one spec parser shared
by runner/study/mte (BOUND-3) and delete `brace_depth_at` (HYGIENE-1). Axes: improves C1 depth
(accept-side completeness) and calibration hygiene; harms none — the direction is fail-closed-only
today, and widening what can be *parsed* cannot create a false accept because behavioral
comparison still decides. Risks: heredoc state tracking interacts with line continuations and
nested `<<` pairs; `${…}` inside double quotes must not be re-read as brace structure (skip the
whole quote span, as S102 §2.2.3 treats `${…}` inside double quotes by its own rule). Verification:
`python3 tools/tally-audit-v3.py --selftest` green with the new seeds; the p1–p5 copies (hashes in
§2, kept at `/fast/scratch/hyaku/tameshi-r35-seats/ConnectorCommentBlind/work/`) accepted; the
round-35 panel + sealed sets re-run by the frozen counter unchanged.

Evidence trail: `work/bench.py` (the full bench, exit 0) and its five copy files with the sha256s
above; the parser differential and p5 re-drive heredocs inline in this report's transcript; every
verdict line above is a verbatim audit stdout line with its exit code.
