# ReviewSkillRecipe — SKILL.md one-line change review (round 31, wave 2)

Seat: TameshiR31.ReviewSkillRecipe

## Verdict

The change is a single-line edit (1 insertion, 1 deletion; line count unchanged, so no
other section's start line moves). It implements the recipe portion of round-30 routed
defect 2 (round-30-verifier-spotcheck.md:210-211) and the first two conjuncts of QUALITY
67 (corpus/QUALITY.md:762-766), and it is executable as written by a cold reader: the
flags it names are documented in the same file and are supported by the tool. One Low
finding: the kill rule omits QUALITY 67's ownership clause ("a process the seat did not
start is never killed") while citing that very policy, leaving the sentence's stated
authority partially unimplemented.

## The change

Command (read-only):

```
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin diff 36c1d3933f680125aeefc447f07db0f03004901a 2da841bd9913a2037d2bf612793382e572c9d205 -- SKILL.md
```

Observed: one hunk `@@ -1883,7 +1883,7 @@`, line 1886 changed:

```
-   the receipt lists the tracked files opened (`inputs`), untracked opens, and external fleet files.
+   the receipt lists the tracked files opened (`inputs`), untracked opens, and external fleet files. A seat gives every `--regression` a `--workdir` under its own scratch dir and kills only processes whose `/proc/<pid>/cwd` is inside that dir (round 31; QUALITY 67).
```

`git diff --numstat` → `1	1	SKILL.md`. Line count unchanged; later section start lines
are stable (verified: the hunk header spans 7 lines on both sides).

The sentence is present at the content revision itself: `git show 2da841bd9913a2037d2bf612793382e572c9d205:SKILL.md | grep -n "A seat gives every"` → line 1886.

## Requirement mapping

- Defect 2 (round-30-verifier-spotcheck.md:210-211): "Cold-read recipe: pass `--workdir`
  under the seat's own scratch on every `--regression` run, and require the cwd check
  before any kill (Mistake 5 fix); record the ColdA09 kill in ColdA09's section-26 note."
  - "pass `--workdir` under the seat's own scratch on every `--regression` run" -> "A
    seat gives every `--regression` a `--workdir` under its own scratch dir" — covered.
  - "require the cwd check before any kill" -> "kills only processes whose
    `/proc/<pid>/cwd` is inside that dir" — covered.
  - "record the ColdA09 kill in ColdA09's section-26 note" — not covered by the sentence
    (and need not be: it is an evidence-recording task for the ColdA09 seat, not a
    recipe instruction). Residual routing to verify this wave, see Residual risk.
- QUALITY 67 (corpus/QUALITY.md:762-766): "Every seat invocation of `--regression`
  passes `--workdir` with a directory beneath that seat's own scratch directory.
  Before any process is killed, the seat checks `/proc/<pid>/cwd` and verifies that it
  resolves beneath that seat's own scratch; a process the seat did not start is never
  killed."
  - Conjunct 1 (--workdir beneath own scratch) — covered.
  - Conjunct 2 (cwd check before kill) — covered.
  - Conjunct 3 (a process the seat did not start is never killed) — omitted (Finding 1).

## Findings

### Finding 1 (Low) — kill rule lacks the ownership clause, though it cites QUALITY 67

Evidence: SKILL.md:1886 (at 2da841bd) states "kills only processes whose
`/proc/<pid>/cwd` is inside that dir (round 31; QUALITY 67)". QUALITY 67
(corpus/QUALITY.md:765-766) adds the conjunct "a process the seat did not start is never
killed". The sentence's condition is necessary, not sufficient, against the policy it
cites: a cold reader following only SKILL.md could kill a process it did not start whose
cwd happens to resolve inside its scratch. That is the harm class of Mistake 5
(corpus/lessons/round-30.md:169-182: ColdA01 killed sibling processes via a broad
`pgrep`/kill on a shared scratch name pattern), so the ownership criterion is the
logically decisive guard, not decoration.

Impact: narrow in practice — with per-seat scratch dirs, a foreign process whose cwd
sits inside a seat's scratch is likely a containment breach anyway — but the sentence
claims QUALITY 67 as its authority while implementing only two of its three conjuncts.

Smallest safe correction (one clause): in SKILL.md:1886 change "kills only processes
whose `/proc/<pid>/cwd` is inside that dir" to "kills only processes it started whose
`/proc/<pid>/cwd` is inside that dir". This preserves the cwd check required by defect 2
and restores exact parity with QUALITY 67.

### Finding 2 (Info / residual routing) — defect 2's third clause is not in SKILL.md

The sentence does not (and need not) cover "record the ColdA09 kill in ColdA09's
section-26 note". Closure of defect 2 therefore still depends on that record landing in
ColdA09's round-31 section-26 note this wave. Check it in the wave-2 evidence; a missing
record leaves defect 2 partially open even though the recipe sentence is correct.

## Executability as written (cold reader)

Yes. The two flags named by the sentence are documented in the same committed file at the
same revision: SKILL.md:935-939 (at 2da841bd) — "One command replays every leg. `bash
tools/mutate-and-run.sh --regression [--workdir DIR] [--keep]` allocates a fresh default
scratch ... caller workdirs are never removed." The tool accepts `--workdir` (usage and
selftest: `--regression refuses --target (exit 64)`). "Its own scratch dir" is given by
the round-31 wave binding (each seat's working directory is its own scratch dir), which
the intended cold-read audience holds; a reader with only SKILL.md would know the
concept but not the concrete path, which is acceptable for this lane's readers.

## Residual risk / verification gaps

1. ColdA09's section-26 note record (defect 2, third clause) — confirm it lands this wave.
2. The "did not start" ownership clause is enforced only by the (recommended) one-word
   correction; the current text alone would not stop the residual kill scenario above.
3. No other SKILL.md changes exist in the reviewed range (numstat 1/1; one hunk), so no
   other section start line moves — confirmed at both the base and content revisions.
