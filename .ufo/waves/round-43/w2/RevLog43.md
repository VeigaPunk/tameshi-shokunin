# RevLog43 — round-43 LOG section vs the tree at the freeze

Scope: `LOG.md:2221-2260` (round-43 section), every factual claim in it checked against
`3aee2c078f8976499b587086af3577fc94dc8cf1`. `LOG.md` is byte-identical at the freeze
(`git diff --stat 3aee2c0 -- LOG.md` → empty), so these line numbers are the freeze's.
Counters were run only at `--rev/--freeze 487b8f0` (base) and `3aee2c0` (freeze); nothing was
run at `c5335c7`. Lane read-only; all work in `/tmp/tameshi-r43-w2-RevLog43-scratch` (a
`git clone --shared` checked out at the freeze, since removed). No tool installed.

Reproduce the whole measurement set from a scratch clone at the freeze:

```sh
git clone --shared -q /home/vgpnk/Projects/shokunin/tameshi-shokunin /tmp/tameshi-r43-w2-RevLog43-scratch
cd /tmp/tameshi-r43-w2-RevLog43-scratch && git checkout -q 3aee2c078f8976499b587086af3577fc94dc8cf1
python3 .ufo/evidence/round-43/mutants/measure.py    --lane . --rev 3aee2c0 --freeze 3aee2c0
python3 .ufo/evidence/round-43/calibration/measure.py --lane . --rev 3aee2c0 --freeze 3aee2c0
python3 .ufo/evidence/round-43/guard/measure.py       --lane . --rev 3aee2c0 --freeze 3aee2c0
```

---

## High

### H1. `LOG.md:2223` names the wrong freeze, and `LOG.md:2224-2225` undercounts the amendments

`LOG.md:2223-2225`:

> Contract frozen at `17f6ef0c72ec27e1aea305b5c95806b43bb2caef` before any seat and before the
> first deciding run (`amendments` A1–A3 pre-data; A4 the guard repair from a wave-1
> mutation-tester).

The freeze of record is `3aee2c078f8976499b587086af3577fc94dc8cf1` (assignment), and the contract
itself names a *later* freeze than the one the LOG prints:
`.ufo/evidence/round-43/contract.json:7` — "the freeze of record is
`114ffacd813d67286e369fc8f7b89f2c0418aaf4`, reached through 697d2f17 (first freeze) ->
f0f26367 (A1) -> 17f6ef0c (A2/A3) -> 5cd2154f (A4/A5) -> 114ffacd (A6/A7)". `17f6ef0c` is the
*A2/A3* step, three freeze commits and four amendments behind `114ffacd`, and five commits behind
the freeze of record.

Two further facts contradict the sentence as written:

* `contract.json:100` (A4) through `contract.json:148` (A10) all carry `"when": "during wave 1,
  before any deciding run"` — so a contract "frozen at 17f6ef0 before any seat" cannot also
  contain A4–A10, and the LOG's own next clause ("A4 the guard repair from a wave-1
  mutation-tester") refutes its "before any seat" for the rev it names.
* The LOG lists A1–A3 plus A4 and stops. The contract carries **ten** amendments; A5–A10 are
  unmentioned. (My assignment brief also says "A1-A9"; the contract has A10 — the brief and the
  LOG share the same drift.)

Reproduce:

```sh
cd /tmp/tameshi-r43-w2-RevLog43-scratch
git log --oneline 17f6ef0c72ec27e1aea305b5c95806b43bb2caef..3aee2c078f8976499b587086af3577fc94dc8cf1
# 53cb32b A8, 273c047 A9, c5335c7 records, 3aee2c0 A10  (four commits, not "the freeze")
python3 -c "import json;d=json.load(open('.ufo/evidence/round-43/contract.json'));print(len(d['amendments']),[a['id']+':'+a['when'] for a in d['amendments']])"
```

Downstream damage: `SCORECARD.md:2053` repeats "frozen at `17f6ef0c…`", and every counting command
printed in the round-43 SCORECARD table (`SCORECARD.md:2059-2061`) passes
`--freeze 17f6ef0c72ec27e1aea305b5c95806b43bb2caef`, i.e. a rev that is not the freeze of record.
At that rev the guard blob was `8140945a…`, the pre-A4 tool that refuses the counter's own safe
map (`.ufo/waves/round-43/w1/ExecC3Live.md:68`), so the C3 claim in `LOG.md:2242-2243` ("only a
by-document map at or above the safe floor `S256` admitted") is false of the freeze the LOG
names and true only of `3aee2c0`. The LOG's C3 numbers are right about the shipped bytes; the
rev they are attributed to is wrong.

### H2. `LOG.md:2234-2238` — C2's `total=0` is not met at the freeze: the frozen counter prints `m7=5 m8=3 total=8 C2_R43_PASS=false`

The LOG narrates the seven-class agreement, gives the before-state, and declares the target:

> Before `m12=1 m13=1 total=2`; target `total=0`.

At the freeze, the frozen C2 counter (sha256 `97609511…`, `self_pin=1`) prints:

```
C2_R43: self_pin=1 classes=7 m6=0 m7=5 m8=3 m10=0 m11=0 m12=0 m13=0 total=8 records=4
sources_rows=114 standing=114 receipts=17 revisions=2 m13_probe=standing=7_column0=113_valid=114
rev=3aee2c07… freeze=3aee2c07… C2_R43_PASS=false first=m7:corpus/lessons/round-43.md_unknown_S160
```

The eight hits, each a line in the records the LOG ships:

| class | file:line | text that trips it |
|---|---|---|
| m7 | `corpus/lessons/round-43.md:75` | `S160 is the next unused id` (prose order, not the masked `Next unused id: S###` form) |
| m7 | `corpus/lessons/round-43.md:83` | `lands on `S160`–`S166`, which are themselves staged ids` |
| m7 | `corpus/lessons/round-43.md:84` | ``The safe floor for a *partial* adoption is `S256` `` |
| m7 | `corpus/lessons/round-43.md:116` | `{'S153':'S105',…,'S158':'S259'}` (illustrative map target) |
| m7 | `LOG.md:2243` | ``only a by-document map at or above the safe floor `S256` admitted`` |
| m8 | `corpus/lessons/round-43.md:118` | `` `.ufo/waves/...` `` |
| m8 | `corpus/lessons/round-43.md:140` | `` `tools/*.py` `` |
| m8 | `SCORECARD.md:2059-2061` | `` `.ufo/evidence/round-43/after/` `` — that directory does not exist at the freeze |

The m8 `after/` hit survives any rev the deciding run can use: the records are byte-identical at
`c5335c7`, `3aee2c0` and `e20cf89` (`git diff --stat` empty for `SCORECARD.md LOG.md corpus/
README.md` between each pair), and `git ls-tree -r e20cf89 -- .ufo/evidence/round-43/after` is
empty — `e20cf89` re-ran only `before/` and `control/` receipts. So the deciding run cannot print
`total=0` without either a records edit or a counter edit after A10, and A10's `effect` claims the
predicate and targets are unchanged.

The LOG does not disclose any of this; it reports the m12/m13 repair as if it were the whole
distance to `total=0`. This is the calibration claim under attack, and it fails at the freeze.

### H3. m7 counts non-citations, contradicting its own stated extraction rule — so C2 is unsatisfiable on these records

`.ufo/evidence/round-43/calibration/measure.py:19-21` states the rule:

> m7 counts only citation ids: a `staged:S###` package token and a `Next unused id: S###`
> declaration are masked before extraction, because neither names a registry row.

The contract's class sentence is narrower still: "every S-id cited by the round-42/43 records **as
a source** is a mined row". The implementation (`measure.py:420-431`) runs
`ID_RE = re.compile(r'(?<!staged:)\bS\d{3,}\b')` (`measure.py:71`) over all non-masked text, so:

* `S256` — a computed safe floor, never a registry id (`S256 = max(registry 159, staged 255)+1`);
* `S259` — an invented map target inside an illustrative `--map` literal;
* `S160`/`S166` — the next-free id and the staged id range;

all read as "unknown ids". None is a source citation. Two consequences:

1. The counter cannot print `total=0` on this round's records even though the records cite no
   unmined source, so H2 is a counter/class mismatch as much as a records gap. A1/A6/A10 all
   declare `rule_changed: false` ("extraction only … class sentences unchanged in meaning"), and
   this is exactly the narrower/broader-extractor class wave 1 raised (`.ufo/waves/round-43/w1/
   RevC2Classes.md`).
2. `LOG.md:2243` — the LOG's own safe-floor sentence — is one of the five m7 hits. The LOG
   contributes a violation to the class it declares at zero.

Reproduce the hit list (read-only, imports the frozen counter's own helpers):

```sh
cd /tmp/tameshi-r43-w2-RevLog43-scratch && python3 - <<'EOF'
import importlib.util
spec=importlib.util.spec_from_file_location('c2','.ufo/evidence/round-43/calibration/measure.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
rev='3aee2c078f8976499b587086af3577fc94dc8cf1'; lane='.'
reg=(m.show(lane,rev,m.SOURCES_REL) or b'').decode(); rows=m.rows(reg); mined=m.mined_ids(reg)
rec={r:(m.show(lane,rev,r) or b'').decode() for r in m.RECORDS}
rn,block=m.newest_round_block((m.show(lane,rev,m.SCORECARD_REL) or b'').decode())
rec['SCORECARD.md#round-%d'%rn]=block
t=(m.show(lane,rev,m.LOG_REL) or b'').decode(); rec['LOG.md#round-%d'%rn]=t[t.find('round %d'%rn):]
for n,x in rec.items():
    mk=x
    for p,_ in m.MASK_IDS: mk=p.sub(' ',mk)
    for s in sorted(set(m.ID_RE.findall(mk))):
        if s not in rows or s not in mined: print(n,s)
EOF
```

---

## Medium

### M1. `LOG.md:2258-2260` — the no-harm re-run is attributed to a rev the seat did not use

> both re-run at the base and at the freeze by wave-1 seat ExecCommandD with byte-identical
> tool/`SHONEN.md`/monitor at both revs.

`.ufo/waves/round-43/w1/ExecCommandD.md:3-4` and its results table `:31` show the seat ran BASE
`487b8f0` and FREEZE **`17f6ef0`** — not `3aee2c0`. The claim's *numbers* do hold at the actual
freeze, which I measured independently:

```sh
cd /tmp/tameshi-r43-w2-RevLog43-scratch
for R in 487b8f0da89fa0e2b8bea6930068accbf36e70a9 3aee2c078f8976499b587086af3577fc94dc8cf1; do
  echo "REV=$R"
  git show $R:tools/mutate-and-run.sh | python3 -c 'import re,sys;n=len(re.findall(r"^#   (?:js|bash)-\S+\s+\S+\s+\d+/\d+",sys.stdin.read(),re.M));print("recorded_cases="+str(n)+" depth_score="+str(min(10,n)))'
  python3 .ufo/evidence/round-21/coldread/measure.py --repo "$PWD" --rev $R | grep calibration_restraint_score
done
git diff --stat 487b8f0 3aee2c0 -- tools/mutate-and-run.sh SHONEN.md .ufo/evidence/round-21/coldread/   # empty
```

Both revs: `recorded_cases=9 depth_score=9`, `"calibration_restraint_score": 6`, and the three
inputs are byte-identical across base..freeze. So "depth 9 → 9, calibration 6 → 6" is **true**;
the evidence pointer ("at the freeze by ExecCommandD") is **false**. Note the pointer matters:
ExecCommandD ran before A8/A9/A10 landed, so at the time of the seat the freeze it tested was the
one then current.

### M2. `LOG.md:2255-2257` — "recorded in the round report" names an artifact that does not exist

> Round shape, seat counts and dead seats are recorded in the round report.

At the freeze there is no round-43 report anywhere:

```sh
cd /tmp/tameshi-r43-w2-RevLog43-scratch
ls .ufo/reports/            # round-1   (only)
ls .ufo/waves/round-43/     # build-spec.py dispatch-w1.json dispatch-w1.stderr spec-w1.json w1
grep -rln "round 43" .ufo/reports/    # empty
```

`spec-w1.json` carries 34 tasks; no wave-2 spec exists yet, so the sentence is also prospective
("wave 2 fresh attackers after wave 1 returns") written in the past tense. The band half of the
sentence is correct: `/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json:88` records
the band as 32–64 ("only the wave band changed (16-32 -> 32-64)").

### M3. `LOG.md:2253-2254` — criterion 83's falsifier does not print the line it claims

> QUALITY criteria 83 … and 84 …, each with a falsifier that fails.

Criterion 84's falsifier works exactly as documented (`corpus/QUALITY.md:1092-1105`): on the
mirror with `S001` indented two spaces, column-zero prints 113 and the 0-3-space pattern 114.

Criterion 83's falsifier does not. `corpus/QUALITY.md:1079` says "The flattering line prints
`mutants_killed=6 dead_code_only=0`". Run that falsifier verbatim against the shipped counter at
the freeze (rev swapped to the freeze, the only permitted measurement rev):

```sh
cp .ufo/evidence/round-43/mutants/measure.py /tmp/m83.py
python3 - <<'EOF'
p='/tmp/m83.py'; s=open(p).read()
s=s.replace("{'expected': False, 'scratch': False, 'explicit_out': False, 'unflagged': False},\n        'self.destination()', 11)",
            "{'expected': True, 'scratch': False, 'explicit_out': False, 'unflagged': False},\n        'self.destination()', 11)")
open(p,'w').write(s)
EOF
python3 /tmp/m83.py --lane . --rev 3aee2c0 --freeze 3aee2c0
```

Actual: `fixtures_pass=11/12 … mutants_killed=5 dead_code_only=1 … C1_R43_PASS=false` — the
reachability gate added by A5/A9 already keeps the dead-code survivor out of the kill count, so
flipping the declared class no longer produces `killed=6 dead_code_only=0`. The criterion's own
argument ("the counter's own output is not the criterion") survives, but its printed demonstration
is stale and the LOG's "each with a falsifier that fails" is only half true. The criterion also
names `--rev 17f6ef0c`, i.e. a non-freeze rev, in the shipped command.

---

## Low

### L1. `LOG.md:2248` — "census exit 0 at start and end" has an exit receipt only at the start

`.ufo/evidence/round-43/census-sources/` holds `start.stdout`, `start.exit` (`start_exit=0`) and
`after.stdout` — no `after.exit`. The claim is nonetheless **true**: I re-ran the census read-only
at the freeze.

```sh
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --root /home/vgpnk/Projects/shokunin tameshi; echo "exit=$?"     # exit=0
# output is byte-identical to .ufo/evidence/round-43/census-sources/after.stdout
# (both sha256 bb8c4162239efce3e0e798ed19c66d0949873269df53b638fc147c3d037af621)
```

Warning set: 9 × W04 + 1 × W01, zero E codes — matching `corpus/lessons/round-43.md:91-95`. So
this is an evidence gap (missing `after.exit`), not a wrong number.

### L2. Adjacent record defects the LOG inherits (not LOG-line errors)

* `SCORECARD.md:2074` cites the capability's tool as `tools/staged-id-guard.py` @ `8140945a…`.
  The shipped bytes at the freeze are `2e8f2e891ea20417c141e16871819182d5040c6f33916a435e9454a94d4d6ff2`
  (`sha256sum tools/staged-id-guard.py`; contract `frozen_tools` pin; the guard counter's
  `tool_sha_ok=1`). `8140945a…` is the pre-A4 blob at `17f6ef0`, which
  `.ufo/waves/round-43/w1/ExecC3Live.md:68` records as refusing the safe map — the row points at
  bytes that cannot do the thing it claims.
* `SCORECARD.md:2059-2061` cite `.ufo/evidence/round-43/after/` and say "see the after
  subsection". That directory exists at neither `3aee2c0` nor `e20cf89`, and the round-43 block has
  no "after the deciding run" subsection (rounds 41 and 42 do: `SCORECARD.md:1969`, `:2022`).
  This is the m8 hit in H2.

---

## Claims checked and found correct at the freeze (calibration: what holds)

* `LOG.md:2247-2248` registry arithmetic: `corpus/SOURCES.md` is 113 rows at base and 114 at the
  freeze under both patterns; one row added, `S159` = Wikipedia, Mutation testing, `docs`/`A`/
  `mined`; `S089`, `S155`, `S158` gain the round-43 `used-by` exactly as `LOG.md:2251-2252` says;
  the Stryker row is absent. (`git show 3aee2c0:corpus/SOURCES.md | grep -cE '^ {0,3}\| S[0-9]{3} \|'` → 114.)
* `LOG.md:2239-2243` C3 numbers, at the freeze: `collisions = S153…S159` (7),
  `held = {S153:S105, S154:S106, S159:S155}` (3; S105 POSIX diff, S106 google/golden, S155 PIT
  basic concepts), naive map targets `S160…S166` (cascade 7) refused, `safe_floor = S256`
  (`max(registry 159, staged 255)+1`), safe by-document map admitted,
  `selftest_cases=24 selftest_failed=0`, `C3_R43_PASS=true`.
  (`python3 -I tools/staged-id-guard.py --registry corpus/SOURCES.md --staged <staged> --json`.)
* `LOG.md:2226-2233` C1, at the freeze: exact target line
  `mutants_declared=6 mutants_killed=5 dead_code_only=1 equivalent=0 unresolved=0
  kill_fixture_reachable=1 dead_code_arg_ok=1 fixtures_pass=12/12 C1_R43_PASS=true`;
  `F11_outflag_namespace` really is a `SimpleNamespace(out='golden')` whose attribute equals the
  `--out` dest with no unreachable statement (`mutants/measure.py:209-226`), `F12` really has a
  second top-level return after the first (`:230-244`), and the declared set is unchanged
  (`git diff 487b8f0 3aee2c0 -- .ufo/evidence/round-42/census/mutants.json` → empty). The tool's
  documented rule is as quoted (`tools/write-path-census-v4.py:27`, `:260-261`).
* `LOG.md:2238` before-state: `before/c2-at-base.stdout` prints
  `m6=0 m7=0 m8=0 m10=0 m11=0 m12=1 m13=1 total=2`, `first=m12:Planned_(round_43)`.
* `LOG.md:2236-2237` m13 before-state: base `SCORECARD.md:2020` carries
  ``grep -cE '^\| S[0-9]{3} \|'`` → 113; the freeze row `SCORECARD.md:2081` carries
  ``grep -cE '^ {0,3}\| S[0-9]{3} \|'`` → 114. The round-42 block has no `Planned (round 43)`
  field (`git show 487b8f0:SCORECARD.md | grep -n 'Planned (round 4[23])'` → empty).
* `LOG.md:2244-2246` knowledge entry: `corpus/knowledge/r43-survivor-resolution-rule.md` exists,
  its `source:` line reads "S089 (held, re-opened), S159 (new); S155 (held), S158 (held)", and it
  carries the PIT `EQUIVALENT(true)` divergence it declines to adopt (`:33-45`) plus both fixtures
  (`:78-79`).
* `LOG.md:2258` axis values: depth 9 and calibration 6 hold at base **and** at the freeze
  (commands in M1).

## Residual risk / verification gaps

* I did not run any counter at `c5335c7` or `e20cf89` (bounds). H2's rev-independence rests on
  `git diff` showing the records byte-identical at all three revs, not on a second counter run.
* H3 can be read two ways — counter over-matching (m7 broader than its class sentence) or record
  defect (the lesson/LOG should not name `S256`/`S259` bare). Either reading leaves H2 intact:
  with the frozen bytes the predicate is `false` at the freeze, and the LOG discloses neither the
  hits nor the mismatch.
* m8's `after/` hit is rev-dependent in principle; I checked both candidate revs and the directory
  is absent at each, so the hit is stable.
* I did not audit the wave-1 seat reports' internal numbers beyond the ones the LOG re-states
  (ExecCommandD, ExecC3Live); other seats are other seats' items.
