#!/usr/bin/env python3
"""Generate the round-74 wave spec (12 seats). Lane-local evidence; the wave
validator is the authority on shape."""
import json
import os

LANE = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
SCRATCH = "$HYAKU_SCRATCH/tameshi-r74"
DPREFIX = ("/skill:godspeed\n\n"
           "You are a Godspeed-enabled subagent.\n\n"
           "1. **Name the axes.**\n"
           "2. **Iterate cheap, in parallel.**\n"
           "3. **Keep moves that improve any axis and harm none.**\n"
           "4. **Don't aim — let the frontier walk itself.**\n\n"
           "## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool "
           "calls concurrently in large batches. Do not serialize what can "
           "run in parallel. Do not output philosophical reasoning or verbose "
           "plans. Act directly via tool calls.\n\n")

COMMON = """
HARD BOUNDS (read first):
- You are a LEAF seat. Do not spawn subagents, do not start background services.
- READ-ONLY on the lane repo except your own report file (and an optional
  same-named subdirectory of receipts) under
  {lane}/.ufo/waves/round-74/w1/ . Never run git/jj mutating commands
  (add/commit/stash/checkout/reset/pull/push, jj commit/new/describe/squash/
  rebase/abandon/bookmark/undo) anywhere, never edit tracked files, never
  touch /home/vgpnk/Projects/shokunin (fleet repo), /home/vgpnk/Projects/shokuknow,
  or any sibling lane repo. Read them if your item says so.
- Scratch root: {scratch}/<your-seat-name>/ , created with mkdir -p and REMOVED
  before you finish (trap 'rm -rf -- "$S"' EXIT or a finally block). /tmp is for
  files under 50 MB only. Every clone is `git clone --shared` or a git
  archive/worktree copy; no full mirror of the lane.
- A fixture git repo is created only as D=$(mktemp -d) && git -C "$D" init -q
  and every later git call names -C "$D"; verify
  `git -C "$D" rev-parse --show-toplevel` equals $D before any commit. Never
  commit with a throwaway identity in a real repo.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade
  tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first
  (official channels only; record tool/version/channel/reason in your report).
  pacman guard (orchestrator ruling 2026-10-20): ALL pacman transactions are
  PAUSED host-wide; install via `uv tool` / `npx` / an official binary into
  ~/.local/bin, or file the need in your report. Never -Sy/-Syu/-U/-R.
- Honesty: an unrun check has not passed. Do not fabricate output; paste the
  exact command and its exact output. Mark inference as [INFERENCE].
- Every `Report:` trailer path the harness prints is relative to {lane} —
  write your report at {lane}/<that path>, i.e.
  {lane}/.ufo/waves/round-74/w1/<your-seat-name>.md .
- Your final message must be a compact findings summary: commands run, exact
  verdict lines, files written, and what you could NOT establish.
"""


def item(name, role, text):
    text = text.replace("{lane}", LANE).replace("{scratch}", SCRATCH)
    assert "{lane}" not in text and "{scratch}" not in text, name
    return {"name": name, "role": role,
            "axes": ["verification-fixture-craft"],
            "item": DPREFIX + text.strip() + "\n"}


CTX = """# Goal and authority
Tameshi lane (verification-fixture craft), round 74, wave w1. The L1 (agent id
`TameshiR74`) is the ONLY coordinator, writer, claim judge and committer. Two
claims are frozen BEFORE any of this wave's data in
{lane}/plans/round-74.plan.md — read it first; it carries the predicates,
counting commands, kill rules and controls. Seat outputs are evidence for the
L1's verdict, never verdicts themselves. Base revision
3d6ea1ee8e551e3baf94904384890e3a112088f0 = origin/master (the admitted
round-73 non-author closure).

R74-C1 (operability) — `{lane}/tools/wave-reconcile.py`: add three frozen
selftest arms (delimited-token rule, record-span substring rule,
`seat_reports` top-level-only counting) so the three mutants the round-73 wave
measured as survivors (`m2` `delimited := True`; the record-span removal;
`W2` any-depth counting) die on their named arms. Target after-state:
`WAVE_RECONCILE_SELFTEST: 15/15 pass` and `killed=3 survived=0` from a committed
runner spec against `tools/mutate-and-run.sh`.

R74-C2 (calibration) — `{lane}/tools/additivity-range.py` +
`tools/additivity-range.json`: every commit of a declared range measured per
file with a declared claim class (`append-only-raw` | `append-only-content`)
and `expect: hold|violated`, so the round-73 closure's two routed EOL rewrites
(LOG.md at `862e8844`, corpus/QUALITY.md at `21a7332f`) become MEASURED declared
violations. Target after-state: `ADDRANGE: rows=6 met=6 unexpected=0` exit 0.

# Fleet context
The fleet runs other lanes concurrently; their trees are read-only to you.
{common}
""".format(lane=LANE, scratch=SCRATCH,
           common=COMMON.format(lane=LANE, scratch=SCRATCH))

ITEMS = [
    item("T74W1E1", "executor", """
TARGET: the before-state of R74-C1, measured on committed bytes.
Repo {lane}, base 3d6ea1ee (pristine tool: `git -C {lane} show 3d6ea1ee:tools/wave-reconcile.py`).
1. Materialise the pristine tool into {scratch}/T74W1E1/pristine/ and run
   `python3 -I -X utf8 <pristine>/wave-reconcile.py --selftest`; paste the exact
   last line and exit code.
2. Build THREE single-edit mutants from the pristine bytes in your scratch
   (python byte replacement that asserts count==1 before writing; sha256 the
   pristine file before and after to prove you never touched it):
   - `m2-delimited-tautology`: replace the body of `def delimited(...)` so it
     returns True for every input (the round-73 seat T73W1S02 mutant).
   - `span-rule-removed`: delete the two-line guard
     `if rec['span'].encode('utf-8') not in raw:` + its `raise SetupError(...)`
     in `_record_span`.
   - `w2-seatreports-any-depth`: in the `seat_reports` branch drop the
     `and '/' not in p[len(prefix):]` clause (the round-73 seat T73W1S10 mutant).
3. Run `--selftest` on each mutant; paste each `WAVE_RECONCILE_SELFTEST: n/12`
   line and say for each whether it SURVIVES (12/12) or is caught (name the
   failing arm lines).
4. Report the exact old/new byte strings of all three edits (they are inputs
   the L1 needs for the frozen mutant spec) and the pristine sha256.
Write findings to your report file; keep any receipt you cite in your
same-named subdirectory. Do NOT edit the lane.
"""),

    item("T74W1E2", "executor", """
TARGET: the `seat_reports` top-level-only rule (R74-C1 arm 15 design), measured
on a fixture repo.
1. Build a throwaway git repo in {scratch}/T74W1E2/D (mktemp -d, init -q,
   identity fixture-local, verify rev-parse --show-toplevel == $D). Commit:
   12 top-level `S<nn>.md` files in a wave dir plus one nested
   `wave/nested/deep.md` and a `wave/swarm-registry.json`.
2. Write a probe manifest for the PRISTINE tool (from
   `git -C {lane} show 3d6ea1ee:tools/wave-reconcile.py`) with one
   `seat_reports` row: record span `12 reports` + `printed: 12` in a record file
   you also commit, artifact dir/rev the wave dir. Run it and paste the
   `WAVE_ROW`/`WAVE_RECONCILE` lines (expected: top-level=12, `meet`).
3. Repeat with the any-depth mutant (drop `and '/' not in p[len(prefix):]`) and
   paste its lines (expected: `files=13`, `drift`). This is the discrimination
   the new arm must reproduce WITHOUT a real repo (in the selftest the fixture
   listing is a dict, so the arm must add the nested path to `SEAT_FILES`).
4. Propose the exact arm input for a frozen `arm15-seatreports-top-level-only`
   that (a) passes on the pristine tool, (b) FAILS on the any-depth mutant, and
   (c) does NOT change arms 3's outcome. State which fixture constant it must
   touch and why adding a nested path cannot leak into `seat_reports` rows of
   the standing six-row sweep.
Keep the fixture repo bytes (file list, commit ids) in your receipt subdir.
"""),

    item("T74W1E3", "executor", """
TARGET: prove the lane's own runner can express and score the three R74-C1
mutants — WITHOUT writing the lane repo.
Read {lane}/tools/mutate-and-run.sh (usage block, spec format v1) and
{lane}/plans/round-74.plan.md.
1. In {scratch}/T74W1E3/, copy the pristine tool from
   `git -C {lane} show 3d6ea1ee:tools/wave-reconcile.py`.
2. Write a draft defect spec (spec format v1: `@defect <id> | <desc>`,
   `@old`, `@new`; escapes \\n \\t \\r \\\\ only) for the three edits E1 names:
   delimited-tautology, span-rule-removed, seat_reports-any-depth. Every `@old`
   must occur exactly once — show the count check the runner prints.
3. Run:
   `bash {lane}/tools/mutate-and-run.sh --target <scratch>/wave-reconcile.py
    --defects <scratch>/draft.spec --suite 'python3 -I -X utf8 "$MUTANT" --selftest'
    --workdir <scratch>/work --label wave-reconcile-arms`
   and paste the control line, every per-defect verdict line and the summary.
   Expected today: all three SURVIVED (12/12) — that IS the before-state.
4. Report: the exact spec bytes that worked, the runner's exit code, and any
   spec-format obstacle (e.g. a two-line @old needing \\n escapes). Do not
   commit; the L1 lands `tools/wave-reconcile-mutants.spec` from your draft.
"""),

    item("T74W1E4", "executor", """
TARGET: an INDEPENDENT per-commit additivity scan of the round-73 range
(R74-C2's before-state), with your own code.
Read {lane}/plans/round-74.plan.md C2 first. Do not import
`tools/additivity-receipt.py`; read only its docstring.
1. For the range `a3dd3574..3d6ea1ee` in {lane}, and for each of
   `LOG.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `SCORECARD.md`: walk
   `git rev-list --reverse --first-parent a3dd3574..3d6ea1ee`, and for every
   commit whose blob for that file differs from its first parent, compute with
   your own code from `git cat-file blob <rev>:<path>`:
   raw_old_only, raw_new_only, norm_cr_old_only (CRLF/CR → LF),
   verbatim_prefix (CR-stripped, empty-dropped base content is a prefix of tip
   content), and eol_rewrite_disclosed.
2. Print one line per (commit, file) with the 12-char commit id, then a summary
   naming every commit that removed raw lines, and every commit where
   raw_old_only != norm_cr_old_only.
3. State explicitly the two routed-defect commits from round 73
   (`862e8844` LOG.md, `21a7332f` corpus/QUALITY.md) with their parent-pair
   numbers, and confirm or refute the numbers 3484 and 1593.
4. Also measure the two range-total pairs (a3dd3574 → 3d6ea1ee) per file and
   report those numbers beside the per-commit ones, so the L1 can freeze both
   views honestly.
Keep your script and its output in your receipt subdir (the L1 may cite it).
"""),

    item("T74W1S1", "scribe", """
TARGET: the sourced half of R74-C2 — open the source and draft the Gate block.
1. Fetch https://git-scm.com/docs/gitattributes with `curl -sS -D headers -o
   page.html` into your scratch; record HTTP date header, byte size and sha256.
   REDACT any `set-cookie`/credential header value to its name before quoting
   (round-73 sentinel finding: Cloudflare `set-cookie` leaked once).
2. Locate, verbatim, the passages that ground this sentence: end-of-line
   conversion is a declared per-path attribute layer applied at checkin and
   checkout, NOT a property of blob bytes, so `git cat-file` returns raw bytes
   and a CRLF→LF rewrite is invisible to a file-content comparison that strips
   CR. Give ≤25-word located quotes (quote, word count, page line numbers).
3. Check whether a NEW row is justified: `grep -c 'gitattributes'
   {lane}/corpus/SOURCES.md` (S294 already holds this page) and
   `grep -c 'git-scm.com/docs/git-diff[^-]' {lane}/corpus/SOURCES.md` for the
   `git-diff` page (`--ignore-cr-at-eol` option). For each candidate say ADMIT
   (with the row cells: id proposal, kind, tier, scope, anchor, teaches,
   status, opened, recheck) or REFUSE (with reason + flip condition).
4. Draft the `## Gate` block for `corpus/lessons/round-74.md` with: URL, access
   date, bytes, sha256, extract path proposal under
   `.ufo/evidence/round-74/sources/`, the located quotes, the admit/reject pair,
   and the S294 `used-by` old → new string the L1 must apply.
Do not edit corpus/SOURCES.md yourself. Give the exact row text if you recommend
an append.
"""),

    item("T74W1SC1", "scout", """
TARGET: recon for the round-73 closure's routed defect 5 (gate registry) — what
exactly is missing, and the cheapest honest way to pay it.
1. Read {lane}/tools/registry.json (schema, row fields, how `source` and
   `scratch_root` are used) and {lane}/tools/registry-check.py (modes, exit map,
   what a row must carry to be green).
2. Enumerate the lane's standing instruments named in
   `corpus/lessons/round-73-verifier-spotcheck.md` §6 item 5 (figure-attribution,
   count-recheck, anchor-drift-sweep, arm-liveness, pointer-recheck,
   receipt-commit-bind) plus the two this round touches (wave-reconcile,
   additivity-range) and report WHICH have a row today:
   `python3 -I -c "import json;d=json.load(open('{lane}/tools/registry.json'));
   print(sorted({r['name'] for r in d['rows']}))"` (paste the full sorted name
   list) and cross-check by argv tool name.
3. For the two round-74 instruments, propose the exact JSON row(s) (name, kind,
   argv, expect, timeout_s, source, status, tags; plus `scratch_root` text if
   the tool allocates scratch) that would pass `registry-check.py`. Say which
   `source` anchor string is honest today (the registry's anchors name SKILL.md
   lines — check whether SKILL.md documents these instruments at all).
4. Report the command that validates the registry and its current exit code.
Read-only. Do not edit registry.json.
"""),

    item("T74W1R1", "reviewer", """
TARGET: attack the R74-C1 arm design before it lands. Read
{lane}/plans/round-74.plan.md and the pristine tool
(`git -C {lane} show 3d6ea1ee:tools/wave-reconcile.py`).
1. For each proposed arm (13 delimited-token, 14 record-span substring,
   15 seat_reports top-level only), state the exact SetupError/measured value it
   must produce and find a way to make it PASS without the guarded rule:
   - arm13: can a `printed` value that is a substring-but-not-delimited token
     reach the seats comparison under some other row shape?
   - arm14: does `_record_claim` bind the span for every kind (r73 hardening),
     or does a row kind exist where an absent span is a silent pass?
   - arm15: does the fixture listing path (dict keyed by (rev, dir)) let a
     nested path leak into another arm's population? Which pre-existing arm
     reads the same listing?
2. Measure, do not assert: build the three proposed fixture inputs in scratch
   against a COPY of the pristine tool with the arms added yourself and paste
   the exact selftest lines (pristine vs each mutant).
3. Name every pre-existing arm whose outcome could move, and the invariant that
   proves it does not.
Deliver a ranked list of defects (each with the measurement that shows it) and
a verdict per arm: SOUND / WEAK / BROKEN.
"""),

    item("T74W1R2", "reviewer", """
TARGET: attack R74-C2 — can a do-nothing control reach the frozen line, and are
the six rows' expectations honest?
Read {lane}/plans/round-74.plan.md C2 and
`tools/additivity-receipt.py` (docstring + code).
1. Reproduce the do-nothing baseline on committed bytes:
   `python3 -I {lane}/tools/additivity-receipt.py --repo {lane} --base
   862e8844^ --tip 862e8844 --file LOG.md` and the same for
   `corpus/QUALITY.md` at `21a7332f`. Paste lines + exit codes.
2. Verify the six frozen rows against committed bytes with plain git: the
   commit ids, the first-parent pairs, and the raw/normalized old-only numbers
   the plan claims (3,484 / 1,593; holds at 17cd1939, e309f59f, be1199d3).
3. Build a stub that echoes each row's `expect` and show what it CAN and CANNOT
   print (the plan's kill rule names this control). State whether the plan's
   measured values (raw_old_only) make the stub insufficient, or whether the
   summary line alone is spoofable — if spoofable, say which per-row field the
   frozen line must carry to make the echo useless.
4. Check the class distinction claim: for both rewrite commits, compute the
   `append-only-content` judgement and confirm it reads `hold`.
Deliver defects with measurements and a verdict: does C2 admit a do-nothing
control?
"""),

    item("T74W1C1", "critic", """
TARGET: falsify the round's sizing, duplication and no-harm claims. Read
{lane}/plans/round-74.plan.md, {lane}/SCORECARD.md (round-73 and round-74
blocks) and {lane}/corpus/lessons/round-73.md.
1. Is R74-C1 an axis move or padding? The instrument already had 12 arms and a
   standing sweep. Argue with evidence: which decisions would a reader get
   wrong today that the three arms prevent? (Look for a place the repo's own
   records relied on the unguarded rule — e.g. a row/record whose correctness
   depended on the delimited-token or top-level-only property.)
2. Does R74-C2 duplicate existing instruments? Compare with
   `tools/additivity-receipt.py`, `tools/rekey-cost.py`, `tools/receipt-exists.py`
   and `tools/quoted-line-exists.py`: name the exact capability each already
   has and what the new range sweep adds that none of them measures.
3. Check the frozen kill rules for attainability (round-73 lesson: a plan's
   kill-rule wording was contradicted by its own green-only control). Quote the
   sentence that could misfire and say how to read it.
4. No-harm check: which axis could this round harm, and what would show it?
   (Monitored bytes: corpus/SOURCES.md and corpus/QUALITY.md are cold-read
   monitored — the r73 closure routed two EOL rewrites, so an append that
   changes EOLs is harm.)
Deliver: a verdict per claim (admit / admit-with-condition / reject) with the
measurement behind it.
"""),

    item("T74W1M1", "mutation-tester", """
TARGET: independent arm-liveness mutants for the R74-C1 arms — prove each new
arm is load-bearing and find arms that are dead.
Work from the PRISTINE tool (`git -C {lane} show 3d6ea1ee:tools/wave-reconcile.py`),
copied into {scratch}/T74W1M1/. For each of FOUR mutants you design yourself
(name them M-A..M-D; do not reuse E1's three):
- candidates: `delimited` narrowed to `value > 0`; the span check replaced by a
  truthiness test on `rec['span']`; `printed` accepted when it appears in the
  WHOLE record rather than in the span; `seat_reports` prefix filter inverted
  (count only nested files).
Then, for each mutant, apply the three NEW arms yourself in a second copy
(15 arms total) and measure which arm catches which mutant. Paste the exact
`SELFTEST armNN … FAIL` lines.
Deliver a kill matrix (mutant × new arm), name any new arm that catches NOTHING
(dead arm), and any mutant that survives ALL 15 arms. Also confirm the 12
pre-existing arms still pass on your arm-added copy.
"""),

    item("T74W1CN1", "connector", """
TARGET: sibling-overlap scan (read-only) for the two round-74 mechanisms.
Read {lane}/plans/round-74.plan.md.
1. Range/commit-walk additivity or EOL-disclosure instruments in sibling lanes:
   grep (read-only, no writes) under /home/vgpnk/Projects/shokunin/*-shokunin/
   for tools that walk a commit range and compare blobs for line removal —
   search terms: `rev-list --reverse`, `raw_old_only`, `append-only`,
   `ignore-cr-at-eol`, `crlf`, `norm_cr`. Report file paths + the exact
   command that found them, and whether the mechanism is a duplicate.
2. Selftest arm conventions for "count at top level vs any depth" or
   "delimited token" in sibling gates: does any sibling suite already ship an
   arm of this shape? Name it with path:line.
3. State whether either round-74 pattern is general on ≥2 independent lanes
   (PROVINCE.md's bar) or lane-local, and what a second-lane confirmation would
   require. Do not modify any sibling repo; do not run sibling gates.
"""),

    item("T74W1SN1", "sentinel", """
TARGET: secrets, scope and scratch discipline for round 74.
1. Secrets: the round fetches https://git-scm.com/docs/gitattributes. Reproduce
   the fetch with `curl -sS -D -` in scratch and grep the response headers for
   cookie/token/authorization fields; report presence (names only, values
   REDACTED), and whether any body content carries credential material. Check
   {lane}/.ufo/evidence/round-74/ for anything already committed that leaks.
2. Scratch: `bash {lane}/tools/mutate-and-run.sh --help | grep -n 'TMPDIR'`,
   and check that the runner honours TMPDIR for `--workdir` defaults; then check
   the new-tool design in `plans/round-74.plan.md` C2 for a hardcoded `/tmp`
   root (a routed defect per the round-73 contract) and name the exact line of
   the plan that would require honouring TMPDIR.
3. Scope: does any item in this wave require writing outside the lane's write
   scope? Check the 12 item texts in
   `{lane}/.ufo/waves/round-74/w1-spec.json` and name any that would.
4. `git -C {lane} status --porcelain | head` at your start: report whether the
   lane is clean (the L1's frozen-plan commit is the only expected entry).
Deliver SECRETS=<count of leaking fields>, TMPDIR findings, SCOPE violations,
and a redaction instruction for any field you found.
"""),
]


def main():
    spec = {"wave": "r74-w1", "maxLanes": 16,
            "reportDir": ".ufo/waves/round-74/w1", "hoist": False,
            "context": CTX, "items": ITEMS}
    out = os.path.join(LANE, ".ufo/waves/round-74/w1-spec.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(spec, fh, indent=1, ensure_ascii=True)
        fh.write("\n")
    print("wrote %s items=%d" % (out, len(ITEMS)))


if __name__ == "__main__":
    main()
