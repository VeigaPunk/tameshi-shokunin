# ReviewShonen — round 18 wave 2 — SHONEN.md at 01d586dd vs the canonical seed

Seat: TameshiR18.ReviewShonen (reviewer, leaf). Read rev `01d586ddbc5fcd78659557c4e93a6ee8517b87d1`
(tameshi). Canonical sources: `/home/vgpnk/Projects/kimi-shokunin` at `e737d2ea97f6`, with
`git status --porcelain` empty for both files below. Scratch: `/tmp/tameshi-r18w2-ReviewShonen-oyuyME`
holds the clone at the read rev (`git rev-parse HEAD` → `01d586dd…`, exit 0), with siblings symlinked.
This report is the only write. No tools were installed or updated.

Axes: (A) seed form, meaning byte-identical modulo name and marks; (B) exactly one evidence line per box;
(C) pointer resolvability at the read rev; (D) preservation of the prose removed from `SHONEN.md`.
Scoring guard: command C and the round-18 `measure.py` were run as no-harm checks.

## Inputs (sha256)

| Input | sha256 |
|---|---|
| `SHONEN.md` @01d586dd (12 lines, 739 B) | `de1b1d986087fe9299a32b927888668830a12b55f998477c7a834baa9b56e6e4` |
| `SHONEN.md` @183f87b (base, 13 lines, 1808 B) | `6b7acb015cb72fde3642ed7c5b5d2fbfdc762fd2b0d32ccab13436830d2c7f80` |
| `.ufo/waves/round-18/staged/SHONEN.md` @01d586dd | `de1b1d98…` (same bytes as landed; `diff` exit 0) |
| kimi `skills/shokunin/protocol/PROTOCOL.md` | `622b29a043046f0b3b3c7a2240fe62ab516898922885685dd8d89f50b1739fd0` |
| kimi `templates/mint/SHONEN.md` | `604dd7a4f6390ecf7ff865766fdd0b007cb9543ba25302e28452e24983adc623` |
| kimi `skills/shokunin/protocol/PROTOCOL-APPENDIX.md` | `90fc91af3c7467a1e131a9164717f81c3ee7ddff3e7bd357cb5e5f9aad322e30` |
| kimi `skills/shokunin/SKILL.md` (`## Promotion gates` :151-167) | `34be71885eb8bedaf16bd27e5e62741d95500904c696ef436349ea00b7477475` |
| kimi `scripts/mint-agent.sh` | `fa411a7014a296c9d45bc05d815f59b9a601648ac61d33165e9d026091d86937` |
| fleet `/home/vgpnk/Projects/shokunin/PROTOCOL.md` (`7c5b34f`) | `886e459b2aa79b8198912ad54bd57fbb025cc424d78684a02fb3d4c832d4411a` |
| `reports/round-1-calibration.md` @01d586dd | `fc46d59db204bc81fb2128aca326bd337d927f1f870e08eda4c91939c78e5472` |
| `LOG.md` @01d586dd | `766c6ee075212afc2d2879e1ec8db3b3bfe82dfec157cc07ff36a13a3af505f1` |
| `SCORECARD.md` @01d586dd | `be578181906c5f0e90557a4908ec27e9f56281f20cdf97e80dcd2994503ddf78` |
| `corpus/QUALITY.md` @01d586dd | `ffed5023df9d4d9bb63446ae1f23d567230f8f45fc4a2b974370ee0d0c8a83b0` |
| `PROVINCE.md` @01d586dd | `8006da5db27d2188ff2f3fc20ae402d0d30c7b5c5fcf9ca26c6793d2ff7e080f` |
| `corpus/lessons/round-16.md` @01d586dd | `46642f0c0bf1cdb263f15af46bdd238f65c04e3105e5cf4d3136a35e0defe298` |
| `corpus/lessons/round-16-verifier-spotcheck.md` @01d586dd | `5ca780d9fda123070b26faa8a6e319db6f10373d6bbc75e45238e09878d52e37` |
| `corpus/lessons/round-17-verifier-spotcheck.md` @01d586dd | `62869c87847e34d59df81140d45d459f6598841bc3a4465e88af7e986e63041c` |
| `.ufo/waves/round-18/w1/B17ShonenCanonical.md` @01d586dd | `2488f8b0f3700104dcc973df4724aada075f5b7ccc97b4ed458a71c9ac0623d1` |
| `.ufo/waves/round-18/w1/S14ShonenFormat.md` @01d586dd | `c6e6e378088024895fbdd4aac0ae256c0ff89ebcf38aff9f15e1130c0bca0aa1` |
| `.ufo/evidence/round-18/measure.py` @01d586dd | `7ffbcff6ef642ec662b233a90c606db68f0e6a7a41639a46b7d3b5aa8e00ee1f` |
| `.ufo/evidence/round-18/measure-explain-e08271a.json` @01d586dd | `525d3b529263ee8385221a6869934f1f212fa5345b6c000007dc0cf3f54c542e` |
| `.ufo/evidence/round-18/coldread/assemble.py` @01d586dd | `bf7c12f7b69dcdb004c7df546cd9655f6f1264ebb3e5565810a673c42dba5a0a` |

## What holds (verified)

**(A) The seed is byte-identical modulo name and marks.** I wrote an independent checker,
`check_shonen.py`, in the scratch directory. It extracts the indented seed block after
`PROTOCOL.md:453` (block `:455-462`, blank lines `''`), dedents it, and substitutes
`<name>` = `tameshi-shokunin`, the repo directory name per `PROTOCOL.md:446`. That gives 8 lines,
364 B, sha256 `94cf8471d7eaca396c8066d5524d1b37bd758e5c663812ec7985baed062c65fe`. The template body
after its wrapper comment hashes to the same `94cf8471…`. `SHONEN.md` with its evidence lines removed
and marks reset to `[ ]` also hashes to `94cf8471…`.

The literal `diff seed.md SHONEN.md` exits 1 with a single hunk, `5,8c5,12`: the four box lines change
`[ ]` → `[~]` and four indented evidence lines are added. Nothing else differs.

The fleet-root copy of the seed matches as well: `diff` of fleet `PROTOCOL.md:432,439-451` against
kimi `PROTOCOL.md:446,453-465` exits 0. The fleet-root copy has a different whole-file sha, but the
contract row and seed are byte-identical. The template's HTML wrapper is absent from `SHONEN.md`.
That is correct: the wrapper calls itself metadata about "the block below", and `PROTOCOL.md:446`
compares only the seed block. Sibling files kake, chousa and kasegi also omit it.

The file is newline-terminated, with no CR, tab, trailing space or trailing blank line. It has four
boxes, at `:5,:7,:9,:11`, all marked `[~]` and none `[x]`. A `[~]` needs no verifier-id
(`PROTOCOL.md:464-465`; kimi `SKILL.md:162-165`).

**(B) There is exactly one indented evidence line per box.** They are `SHONEN.md:6, :8, :10, :12`.
Each has exactly two leading spaces and exactly one markdown link, with no residue outside the link.

**(C) Boxes 1, 2 and 4 resolve.** They point to `reports/round-1-calibration.md`, which is tracked at
the read rev. Its headings `## box-1` (:71), `## box-2` (:105) and `## box-4` (:167) each produce a
unique slug, and each slug matches its anchor once.

**No harm to command C (`SCORECARD.md:75`).** At 183f87b, 58e5d53, e08271a and 01d586dd it prints the
same line: `boxes=4 checked=0 asserted=4 untouched=0 asserted_mark_upper_bound=8`.

**The checker can fail.** At base 183f87b it exits 1 with two failures: `box3-exactly-one-evidence-line`
(lines 10 and 11) and `box3-single-link-no-extra-text`, whose residue is the 570-byte `Correction (round 17…`
prose. In a /tmp fixture repo, the unmodified file exits 0. Five single-edit mutants each exit 1:

- box wording changed (`cited sources` → `cited source`): seed-compare fails;
- header name changed to `tameshi`: seed-compare fails;
- trailing space added to the intro line: seed-compare and whitespace checks fail;
- a second evidence line added under box 4: one-line and no-residue checks fail;
- box 1's evidence line deleted: the one-line check fails.

**The landed bytes are the validated bytes.** `SHONEN.md` @01d586dd equals
`.ufo/waves/round-18/staged/SHONEN.md` (sha `de1b1d98…`, `diff` exit 0). Wave-1 S14 validated that
file (`S14ShonenFormat.md:133-157`) and B17 staged it (`B17ShonenCanonical.md:7-24`).

## Findings, by severity

### F1 — Medium: the box-3 pointer does not resolve at the read rev (pending, as the target expected)

`SHONEN.md:10` points to `.ufo/evidence/round-18/coldread/ledger.json`. Running
`git cat-file -e REV:.ufo/evidence/round-18/coldread/ledger.json` exits **128** at 58e5d53, e08271a
and 01d586dd. In the live lane, a read-only `ls` at 2026-10-20T17:32:18-03:00 found only `assemble.py`
and `traces/` in that directory. The ledger is created after this wave. The path is the right one:
`assemble.py:114` sets `DEFAULT_OUT = os.path.join(HERE, "ledger.json")`, which is the pointer's path.
So the pointer becomes resolvable only when the assembled ledger is **committed** at that default path.

Until then, box 3 is a `[~]` without a resolvable pointer. `PROTOCOL.md:446` and `:464`, and kimi
`SKILL.md:163-164`, require one ("`[~]` with a resolvable pointer").

Measured consequence at the read rev, from round-18 `measure.py` run in bwrap with the fleet
read-only (`--repo <clone> --rev 01d586dd…`, exit 0):

- `shonen.box3_ledger_link=true`, `box3_points=false`;
- `coldread.ledger_present=false`, `sections_covered=0`, `sections_total=60`, `box3_full_page=false`;
- `ledger_committed=false`, `calibration_restraint_score=6`.

The L1's own receipt `.ufo/evidence/round-18/measure-explain-e08271a.json` records the same state
(restraint 6, `box3_points` false, 0/60). No committed text overclaims 8 at this rev.

Process miss: wave-1 S14 set a landing constraint at `S14ShonenFormat.md:235-237`: install the staged
`SHONEN.md` "**in the same commit** as `.ufo/evidence/round-18/coldread/ledger.json`; a SHONEN-only
commit would leave box 3's pointer unresolvable". B17 recorded the same condition at
`B17ShonenCanonical.md:3`. 58e5d53 landed `SHONEN.md` without the ledger. That repeats the round-16
landing mistake: `corpus/lessons/round-16.md:61` says "SHONEN box 3 … cited
`.ufo/evidence/round-16/coldread/ledger.json` before it existed" and maps it to QUALITY 2 and 9.

Closure condition: at the round's record commit REV,
`git cat-file -e REV:.ufo/evidence/round-18/coldread/ledger.json` must exit 0, and `measure.py --rev REV`
must report `ledger_committed=true`, `box3_points=true`, 60/60. Any calibration claim of 8 must be
measured at that REV, never at 01d586dd.

### F2 — Medium: the removed prose is preserved in a committed wave report, but the LOG.md erratum is still owed

The diff at 58e5d53 (`git show 58e5d53 -- SHONEN.md`) removes three base lines from
`183f87b:SHONEN.md`:

- `:10`, the round-16 full-page box-3 evidence line;
- `:11`, the `Correction (round 17, routed R16-C2c): …` erratum line;
- `:13`, the box-4 label's PROVINCE clause, "PROVINCE.md Core list corrected by append (tsukuroi and
  mado gates), fleet round 1".

**Preserved verbatim, committed.** An exact-line test (`grep -nxF`) of each base line against
`01d586dd:.ufo/waves/round-18/w1/B17ShonenCanonical.md` matches lines **40, 42 and 44**. That file was
added in 58e5d53. Its section "Draft LOG.md lines" (`:32-47`) is labeled "Append to `LOG.md` (L1
installs; this seat does not edit LOG.md)".

**Not in LOG.md.** A 60-character prefix of each removed line is absent from `01d586dd:LOG.md`.
`git diff --numstat 183f87b 01d586dd -- LOG.md SCORECARD.md corpus/QUALITY.md SHONEN.md` lists only
`2 3 SHONEN.md` and `128 0 corpus/QUALITY.md`, and `git log 183f87b..01d586dd -- LOG.md` is empty.
`LOG.md` ends at :1083, inside `### Round 17`. A read-only grep of the live `LOG.md` for a round-18
heading or the B17 draft text exits 1. **The append is owed.**

**The lane's own rule requires it.** `corpus/QUALITY.md:262-279` (criterion 35, landed 58e5d53) says a
"SHONEN correction" is "an appended, dated erratum. It names the false text, its replacement and both
revisions … The named erratum must exist in the file under its own dated heading." S14 §7
(`S14ShonenFormat.md:228-230`) also recommends the verbatim LOG append.

The B17 draft (`B17ShonenCanonical.md:36-45`) falls short of criterion 35. It names the false text and
the old rev (183f87b), but it has no dated heading. It also omits the replacement lines (new
`SHONEN.md:10` and `:12`) and the landing rev, 58e5d53. Add all three when appending.

**The substance survives elsewhere.** The correction's content is committed in
`corpus/lessons/round-16-verifier-spotcheck.md`:

- §2 :93-121 covers the `## Effective expectation reconciliation — round 14` bucket, `75ed934d` →
  `0673d2e5…`, and the exit 2;
- §6 item 4 :231 is R16-C2c.

The box-4 clause's substance is in `PROVINCE.md:35` and `LOG.md:576-578`. The full old bytes also
remain in history as `183f87b:SHONEN.md` (`6b7acb01…`). So nothing is lost today, but the
canonical-form repair is not yet recorded in the append-only log.

### F3 — Low: dated records still describe SHONEN content that is gone

Three committed records describe the old content in present tense:

- `SCORECARD.md:617-618` (round-17 record): "SHONEN box 3 carries an appended correction of the
  round-16 overclaim (R16-C2c) and links the round-17 ledger."
- `LOG.md:1072` (round 17): "SHONEN box-3 correction appended".
- `LOG.md:576-578` (round 1): "Box 4 evidence line notes the appended PROVINCE correction".

None is true of `SHONEN.md` @01d586dd. They are dated, append-only records, so they must not be
edited. The F2 erratum should name them, at least SCORECARD:617-618 and LOG:1072, as superseded, so a
reader who follows them knows the content moved.

### F4 — Low: the box 1/2/4 targets cite PROTOCOL.md by bare line numbers that have drifted

This does not affect resolvability. The anchors resolve, but the sections they lead to cite the
kimi `PROTOCOL.md` by line number with no rev:

- the source header at `reports/round-1-calibration.md:17-25` cites `PROTOCOL.md:419–428`, `:413` and
  `:430–431`;
- the box sections cite seed rows, e.g. box-4 at `:169` cites `PROTOCOL.md:428`.

Those numbers fit kimi `bc7d690`, where `grep -n` puts the seed heading at :419, the rows at
:425-428 and `Marks:` at :430. At `e737d2e`, `sed -n '413p;419,431p'` returns Gate-standard prose; the
seed is now at :453-462, the file contract at :446 and `Marks:` at :464-465. The report pins only the
lane baseline 284ab0f (`:6-7`).

This is the lane's own QUALITY 34 class (`corpus/QUALITY.md:251-261`: a line-only anchor into a moving
file the lane does not own). It is historical round-1 evidence, so the fix is an appended erratum, not
an edit. Not a SHONEN form defect.

### F5 — Info: label text on the evidence lines (conforms; optional trim not adopted)

All four evidence lines use the link text "lane assertion, no independent promotion verifier". They
satisfy the line rule: one line, one link, no residue. S14 called this "redundant prose" (D5,
`S14ShonenFormat.md:76-80`) and offered a pointer-only label variant (`:159-173`, sha `f36714bf…`). That
variant was not adopted, and a `git grep` at the rev finds no recorded reason. Fleet practice tolerates
labels: kagi, kotoba and kengaku carry longer prose on their evidence lines. No action required.

### F6 — Info, fleet scope (protocol owner, not tameshi): mint and PROTOCOL define `<name>` differently

kimi `scripts/mint-agent.sh:66` copies `templates/mint` verbatim (`cp -R`), wrapper comment included,
and `:71` substitutes `s/<name>/$ID/g`. That is the bare id, while the lane directory is
`${ID}-shokunin` (`:54`). `PROTOCOL.md:446` and the template's own comment (`:4`) define `<name>` as the
repo **directory** name. Observed effect: `chousa-shokunin/SHONEN.md:1` reads `# chousa — Promotion checklist`.

tameshi's `# tameshi-shokunin — …` follows `PROTOCOL.md:446`, so it is not a defect here. The
mismatch belongs to the protocol owner and is reported as an observation only; no sibling file was
touched.

## Commands executed (all exits observed)

1. Clone, then `checkout --detach 01d586dd…` with GIT_* unset; `git rev-parse HEAD` → `01d586dd…`, exit 0.
2. `git show 01d586dd:SHONEN.md | cat -A | nl -ba` → exit 0. Also `cat -A` and `sha256sum` of the kimi
   template, exit 0. kimi `git rev-parse HEAD` → `e737d2ea…`; `git status --porcelain` for both files
   printed nothing.
3. `git log -- SHONEN.md` and `git show 58e5d53 -- SHONEN.md` → exit 0. The diff removes base
   `:10,:11,:13` and adds the round-18 box-3 line and the trimmed box-4 line.
4. `python3 check_shonen.py <clone> 01d586dd…` → **exit 1**. Only `box3-pointer-resolves` fails;
   the seed-compare and all one-line and no-residue checks pass.
5. `python3 check_shonen.py <clone> 183f87b…` → **exit 1**, the red-before control (two box-3 failures).
6. Six fixture runs in `/tmp/…/mutants`: the unmodified file exits 0; all five mutants exit 1.
7. `diff seed.md shonen-01d586d.md` → exit 1, single hunk `5,8c5,12`.
8. `diff` of the fleet `PROTOCOL.md` seed lines against the kimi seed lines → exit 0.
9. Command C at 183f87b, 58e5d53, e08271a and 01d586dd → exit 0; all four tallies are identical.
10. `git cat-file -e REV:.ufo/evidence/round-18/coldread/ledger.json` at 58e5d53, e08271a and
    01d586dd → 128 each.
11. `bwrap --ro-bind / / … --bind $W $W --unshare-net … env -i … python3 .ufo/evidence/round-18/measure.py
    --repo <clone> --rev 01d586dd…` → exit 0. Fields as in F1.
12. `grep -nxF` of base `SHONEN.md` lines 10, 11 and 13 → B17 lines 40, 42 and 44. The same prefixes
    are absent from `LOG.md`.
13. `git diff --numstat 183f87b 01d586dd -- LOG.md SCORECARD.md corpus/QUALITY.md SHONEN.md` → exit 0
    (output in F2). `git log 183f87b..01d586dd -- LOG.md` → empty.
14. Live lane, read-only, no git: `ls .ufo/evidence/round-18/coldread/` showed no `ledger.json`.
    `grep` of the live `LOG.md` for a round-18 heading or the B17 text → exit 1.
15. kimi `sed -n '413p;419,431p' PROTOCOL.md` returns Gate-standard text, and
    `git show bc7d690:…PROTOCOL.md | grep -n` returns the seed at 419-430 (F4).
    `grep -n` of `mint-agent.sh` for `TEMPLATES`, `cp` and `sed` gives F6.

## Residual risk and verification gaps

- I did not judge the ledger's content (60/60 coverage, carried entries). Only the pointer was checked.
- I did not re-audit whether `reports/round-1-calibration.md` `## box-1/2/4` support their boxes;
  I checked only that they resolve.
- The live-lane observations (F1, F2) are time-stamped snapshots of uncommitted state, not
  committed evidence.
- `check_shonen.py` is a scratch tool in /tmp, not a lane gate. Its slug rule handles the plain
  `## box-N` headings checked here; I did not test it against GitHub's full slugger.

Verdict: **partial**. `SHONEN.md` @01d586dd is canonical: the seed is byte-identical modulo
name and marks (sha `94cf8471…`), there is exactly one evidence line per box, and boxes 1, 2 and 4
resolve. But box 3's round-18 ledger pointer is unresolvable at 01d586dd (exit 128; the ledger is due
after this wave and must land committed), and the removed prose is preserved verbatim only in the
committed `B17ShonenCanonical.md:40,42,44`. The dated LOG.md erratum that QUALITY 35 requires is still
owed.
