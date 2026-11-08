#!/usr/bin/env python3
"""Write the twelve round-100 w1 seat specs (w1/specs/<NAME>.md)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
L = "/home/vgpnk/Projects/shokunin/tameshi-shokunin"
W = L + "/.ufo/waves/round-100/w1"
B = open(os.path.join(HERE, "base-rev.txt")).read().strip()
F = open(os.path.join(HERE, "freeze-rev.txt")).read().strip()
REC = " ".join("--record corpus/lessons/round-%d.md" % n for n in range(95, 100))
COMMON = """
Lane: `%s` (read-only for you except your own files under `%s/`). Base `%s`; freeze `%s`
(FREEZE below). Read `%s/plans/round-100.plan.md` and `%s/.ufo/waves/round-100/claims.json` first.
Run tools from FREEZE blobs (`git -C %s show FREEZE:<path> > $S/<file>`), never the worktree, with
`python3 -I`; TMPDIR=$S where S=/fast/scratch/hyaku/tameshi-r100/<YOUR-SEAT-NAME> (mkdir -p; `trap 'rm -rf -- "$S"' EXIT`;
remove before you yield). Any fixture repo: `D=$(mktemp -d "$S/fx.XXXXXX") && git -C "$D" init -q`, assert
`git -C "$D" rev-parse --show-toplevel` = $D before any commit; never pass an empty variable to `git -C`.
Every receipt you cite is a file under `%s/` whose first lines carry the exact command, the revision and
the sha256 of the tool bytes that ran, then the output, then `rc=N`. Report at `%s/<YOUR-SEAT-NAME>.md`:
findings numbered F1.., each with command, observed output and exit, and a verdict on each claim you
touched: `falsifies-wording` (the frozen sentence claims more than the instrument enforces — quote the
words), `falsifies-number`, or `neutral`, with the artifact path. An unrun check has not passed.
""" % (L, W, B, F, L, L, L, W, W)
SPECS = {
"R100E1": ("executor", "C1 independent replay and stub battery at FREEZE",
"""Re-derive C1 independently at FREEZE.
1. `python3 -I <FREEZE:tools/registry-check.py> --root %s --rev FREEZE --tag r100-c1` (cwd lane) — expect
   `REGISTRY_CHECK: held=12/12 superseded=0` rc 0; and `--rev %s --tag r100-c1` — expect rc 2.
2. Your OWN stub battery (different from the L1's always-green stubs): in a `git clone --shared` scratch
   checkout of FREEZE, for each of the four tools write (a) an always-exit-1 stub — the green and selftest rows
   must differ; (b) a stub that execs the real tool but drops its last output line — some row must differ;
   (c) a stub that prints the red needle for every argv and exits 1. Run `registry-check --root <checkout>
   --tag r100-c1` each time; record held=N/12 and which rows differ. Any stub that keeps held=12/12 is a
   finding against the C1 wording "replacing any one of the four tools by an always-green stub" or its
   declared limit — say which.
3. Full registry at FREEZE: `registry-check --rev FREEZE` (takes ~6-8 min) — expect held=87/91
   superseded=7 and exactly the four base-differing rows (sources-census, verify-round15, mte-interop-check,
   receipt-bytes-tree). Explain for each of the four why it differs (read the row and its output tail).""" % (L, B)),
"R100E2": ("executor", "C2 independent pointer re-derivation without the tool",
"""Write your own checker (do NOT import or copy tools/gate-line-recheck.py) under the wave dir as
`R100E2-indep.py`: render each snapshot cited by the Gates of corpus/lessons/round-95..99.md at FREEZE
with your own implementation of the R93S1 rendering as described in its docstring/comments (script/style
blocks and comments removed, each tag -> one space, entities unescaped, NBSP -> space, lines right-trimmed),
locate each quoted span by word sequence, and decide per pointer whether the cited line (or line range)
is where the quote starts (ends). Extract pointers/quotes by hand-reading the Gates if parsing is hard —
list every `line N`/`lines N-M` occurrence in those five `## Gate` sections. Then run the tool
(`python3 -I <FREEZE:tools/gate-line-recheck.py> --repo %s --rev FREEZE %s`) and produce a per-pointer
comparison table: pointer, your verdict, tool verdict, agree?. Any pointer the tool grades `hit` that you
find does not start on the cited line is a false green (kills C2: report it prominently). Any pointer in
those Gates the tool did not list is a coverage gap against the wording `pointers=21`.""" % (L, REC)),
"R100E3": ("executor", "C2 out-of-set population probe over older lessons",
"""Run the tool at FREEZE over every other lesson with a `## Gate` section
(`git -C %s ls-tree --name-only FREEZE corpus/lessons/ | grep -E 'round-[0-9]+\\.md$'`, minus round-95..99),
one `--record` per file and also all together. Commit the full output as a receipt. Then hand-check at least
8 graded pointers (all `hit` lines first if fewer than 8 misses) by rendering the snapshot yourself
(`git show FREEZE:<snapshot>` + the R93S1 strip_tags) and reading the cited line: report any false hit,
any `miss` that is actually a correct pointer (tool grammar error), any `absent` caused by quote extraction
picking the wrong span, and any crash or setup exit. Summarise the class counts. This is out-of-set evidence:
it cannot change the frozen population numbers, but a false hit or a wrong quote extraction falsifies the
tool's grammar sentences in the plan.""" % L),
"R100R1": ("reviewer", "Review C1 rows and wording against tools/registry-check.py semantics",
"""Review the twelve `r100-c1` rows in `tools/registry.json` at FREEZE (`git show FREEZE:tools/registry.json`)
and `.ufo/evidence/round-100/c1/append-rows.py` against the registry schema and run semantics in
`tools/registry-check.py` (docstring lines 1-90). Check: each red row's needle actually discriminates
(would a broken tool that prints nothing and exits 1 hold the red row? — run it: a stub `sys.exit(1)` in a
scratch checkout); pinned revisions exist and are ancestors of FREEZE; `--rev R` clone semantics make the
historical `--rev 808a4377` arguments resolvable; append-only (diff base..FREEZE of tools/registry.json has
no deleted line); `source` field validity; whether "governs" in the claim title overreaches what the rows
enforce. Verdict each C1 wording clause (falsifies-wording / neutral) with the artifact."""),
"R100R2": ("reviewer", "Review tools/gate-line-recheck.py against its docstring and the C2 wording",
"""Line-by-line review of `tools/gate-line-recheck.py` at FREEZE versus its own docstring grammar and the
C2 wording in claims.json. Check at least: gate_blocks section bounds (`## Gate` exact match, next `## `),
bullet/paragraph splitting, POINTER_RE (does it catch `lines 4496–4497` with en dash, `line 84,`, `lines
135-137`; does it wrongly catch `line 2` inside a path or a word like `pipeline 3`?), find_quote's three
steps, snapshot binding order (explicit/sha/inherited/convention) and the `bind` label honesty,
`hit` semantics for single vs range, unbound accounting, exit codes, `-I` guard, the renderer compile
(only four defs? what if the blob defines a decorator or default-arg that runs code at def time?). Write a
small fixture per suspected defect (fixture repo under $S, recorded) and show the observed verdict.
Verdict each C2 wording clause and each docstring sentence you test."""),
"R100C1": ("critic", "Attack both claims: do-nothing controls, separability, axis naming, overreach",
"""Attack C1 and C2 as frozen. (1) Do-nothing: build the cheapest control that skips the claimed work and
score it with the frozen counters (C1: e.g. rows that call `true`/`false` with the same needles? would
registry-check hold them? C2: a tool that greps `line N` and always says miss for round-95 — does the
frozen predicate distinguish it from the real tool? what about the green arms?). (2) Separability: delete
the other claim's tool in a scratch checkout and re-run each counter. (3) Axis naming per §9: is C1 really
operability (surface moved) and C2 calibration (mismatches between self-assessment and repo state)? (4)
Universal words in the wording ("exactly", "any one of", "each") — does each counter enumerate the full
set? (5) Is the C2 population (21 pointers, 5 records) cherry-picked? Report each attack with command,
output, and verdict."""),
"R100M1": ("mutation-tester", "Mutation matrix for tools/gate-line-recheck.py",
"""Generate at least 14 single-edit mutants of `tools/gate-line-recheck.py` at FREEZE (copies under $S,
never the lane file): e.g. `a == n1` -> `a <= n1`, drop the range-end check, swap explicit/inherited
order, POINTER_RE without `s?`, WORD_COUNT_RE removed, INNER_TOKEN_RE count `== 0` -> `<= 1`,
`counts["hit"] == total` -> `>=`, `total > 0` removed, sha binding reversed order, `.htm` dropped,
unbound counted as hit, `rstrip` in renderer (if reachable), Gate end-bound off by one, isolation guard
removed. For each mutant run (a) `--selftest --repo <lane> --rev FREEZE`, (b) the frozen 5-record
population, (c) round-95-only and round-99-only. Table: mutant, selftest verdict, population summary,
killed-by. Name every survivor and whether it is equivalent or a missing arm; give a concrete fixture that
would kill each non-equivalent survivor."""),
"R100SN1": ("sentinel", "Hostile inputs and trust boundary of tools/gate-line-recheck.py",
"""Probe `tools/gate-line-recheck.py` at FREEZE with hostile fixtures (fixture repos under $S only):
a snapshot that is a symlink blob, a non-UTF-8 snapshot, a renderer blob whose `strip_tags` body or
default argument runs `os.system` (does the tool execute it? — the docstring says only four defs are
compiled; is code in a def's default arg / decorator executed at definition time?), a renderer blob
missing `locate`, `--rev` as a branch name / short hex / tag, `--record` with `../` or an absolute path,
a Gate with 10k pointers (time), a quote with a backtick, an HTML snapshot with CRLF, PYTHONPATH/
PYTHONHOME hostile env without -I. Report each with observed rc and output; classify as defect,
declared-limit, or fine. Recommend fixes; do not edit the lane."""),
"R100CN1": ("connector", "Cross-tool and sibling overlap scan for line-pointer and registry checks",
"""Map overlap: (a) inside the lane, compare `tools/gate-line-recheck.py` with `tools/pointer-recheck.py`
(manifest-pinned line spans), `tools/quoted-line-exists.py`, `tools/anchor-drift-sweep.py` and the round-99
reconciler: which classes each covers, where two now measure the same thing with different grammars
(round-99 spot-check item 4 asked for consolidation or a cross-check arm) — propose one concrete
cross-check arm with a command; (b) across sibling lanes under /home/vgpnk/Projects/shokunin/*-shokunin
(read-only): grep for gate/quote line-pointer checkers and registry monitors (`registry.json`,
`line-pointer`, `quote` + `line`), list path:line hits and whether any would detect the round-95 D1 class.
Never edit a sibling. Verdict on C1/C2 wording if your scan shows the claimed gap was already covered
in-lane (that would make C2 not a new capability)."""),
"R100RV1": ("revenger", "Reconstruct why the round-95 pointers drifted and whether round-96 re-pins match",
"""Reverse-engineer the round-95 Gate's line numbers: read `.ufo/waves/round-95/w1/R95S1.md` (§2
convention), the round-95 counter/probe scripts that produced the numbers (search `.ufo/waves/round-95/`
and `.ufo/evidence/round-95/`), and the round-95 spot-check D1. Determine which rendering produced 84 /
4399 / 4393 / 4493 / 2615 / 2355 (try candidates: no script/style removal, different newline handling,
1- vs 0-indexed, counting from <body>), and record the reproduction script and output. Then confirm the
round-96 re-pins (88, 4403, 4496-4497, 2618-2619, 2358-2359) under the canonical renderer and whether the
tool's `4395` start for "a single header row" vs the closure's `4396` is a grammar choice or an error.
Verdict on C2's sentence "the six pointers the round-95 closure's D1 found off" and its renderer-choice
control."""),
"R100SC1": ("scout", "Re-open S327/S328 independently and find one more candidate",
"""Independently re-fetch the two rows' sources (curl into $S, record HTTP date, bytes, sha256):
S327 Europe PMC REST `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.7717/peerj.1364&resultType=core&format=json`
and S328 `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1371/journal.pone.0184727&resultType=core&format=json`;
compare with the committed snapshots `.ufo/evidence/round-100/sources/s327.json`, `s328.json`; verify the
quotes "Studies indicate, however, that quotations not serving their purpose-quotation errors-may be
prevalent." (12 words) in S327 `abstractText` and "Previous reviews estimated that approximately 20 to
25% of assertions cited from original research articles, or "facts," are inaccurately quoted in the medical
literature." (24 words) in S328, word counts by `len(q.split())`. Judge: does S327 ground C2 (quote
pointers drift often enough to check), and is S328's rejection reason (same ground as S327, a ratio metric
the lane does not use) sound? Then search for ONE further candidate on citation/quotation location
accuracy or line-number drift in documentation, open it, and give admit/reject with a ≤25-word located
quote. Check the lane registry (`corpus/SOURCES.md`) for duplicate URLs first."""),
"R100S1": ("scribe", "Draft the knowledge entry and lesson Gate text for C2",
"""Draft (under the wave dir, NOT in corpus/) `R100S1-knowledge-draft.md`: a knowledge entry for
`corpus/knowledge/gate-line-pointer-recheck.md` in the lane's existing knowledge-entry style (read two
recent ones, e.g. `corpus/knowledge/tally-receipt-reconciliation.md`), covering: the class (quote present
but pointer wrong — round-95 D1), why quote-presence checks cannot see it, the tool's grammar and verdicts,
the frozen measurements from `.ufo/evidence/round-100/pre-freeze/` (cite receipt paths and exact lines),
declared limits, and S327 as source (cite `S327`; quote ≤25 words). Also draft a `## Gate` block for
`corpus/lessons/round-100.md` recording S327 (admit) and S328 (reject + flip) with URL, access date
2026-11-08, HTTP date from `.ufo/evidence/round-100/sources/s32{7,8}.headers`, bytes and sha256 (compute
them) and the located quotes. Every number you write must be copied from a receipt you cite."""),
}
os.makedirs(os.path.join(HERE, "w1", "specs"), exist_ok=True)
for name, (role, title, body) in SPECS.items():
    with open(os.path.join(HERE, "w1", "specs", name + ".md"), "w", encoding="utf-8") as f:
        f.write("# %s — %s — %s\n\n%s\n%s" % (name, role, title, body.replace("FREEZE", F) if False else body, COMMON.replace("YOUR-SEAT-NAME", name)))
print(len(SPECS))
