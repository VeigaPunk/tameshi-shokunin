# T52W2RevR21 — round21-measure review

## Findings

- **Low — stale description:** `tameshi-shokunin/SKILL.md:1969` says the maintained facade supplies “public isolated fixture selftests.” Since CAND0, `tools/round21-measure.py:9-12,77-81` reads pinned sibling blobs from the subject counter's `FLEET` root; the c2 selftest is therefore fleet-bound, not isolated/hermetic. The newer SKILL row at `SKILL.md:2157` accurately documents this, but the round-21 prose remains stale. Command: `grep -n 'maintained facade supplies\|round21-measure' /home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md`.
- **Low — landed patch lost setup guards:** the landed implementation parses the literal with `re.search(...).group(1)` and invokes `git show` with `check=True` (`tools/round21-measure.py:77-81`). Compared with `w1/T52W1ExecR21Fix.patch`, it omits the `fleet_match is None` and `fleet.is_dir()` checks that returned 2 with a concise could-not-evaluate diagnostic. With a missing/malformed fleet root, landed code raises an unhandled exception (exit 1/traceback) rather than clean exit 2. The healthy path and advertised “fails where that fleet root is absent” statement remain true. The change from parsing the temporary package copy to `EVIDENCE` is behavior-equivalent here: the package copy is made from that same EVIDENCE file immediately beforehand (`tools/round21-measure.py:64-66`).

## Checks

- CAND0 changed bytes are `tools/round21-measure.py`; source uses no second hard-coded fleet root: it extracts `FLEET` from `.ufo/evidence/round-21/c2-count.py` (literal `Path("/home/vgpnk/Projects/shokunin")`, line 19). No `ROOT.parent` remains in the facade's fleet lookup.
- All 11 literals in C1 `R21_CASES` occur in CAND0 `tools/round21-measure.py` (lines 101, 106, 110, 115, 117, 121, 125, 129, 133, 136, 138); selftest executes 13 cases/checks.
- Exit 0/1 behavior and 64 usage handler are unchanged in the diff; both successful selftests printed `ROUND21_MEASURE_SELFTEST: 13/13 pass`, exit 0.
- A `git clone --shared` fixture outside the fleet root was pinned to CAND0 (toplevel asserted); `TMPDIR=$S python3 tools/round21-measure.py --selftest` there passed 13/13, as did the same command from the lane path (whose relevant bytes matched CAND0).
- Scratch `c2-count.py` copy pointed at an empty FLEET directory produced `classified=0/9`, nine `pin-unreadable` findings, exit 1. Receipt: `w2/T52W2RevR21-c2-red.stdout`.
- Counter FLEET literal is used by `check_surface` as `show(FLEET / frozen["repo"], ...)` (`.ufo/evidence/round-21/c2-count.py:45-55`); therefore the red result confirms fleet-root dependence, not a verdict on either round claim.

Commands exercised: `git -C LANE diff BASE CAND0 -- tools/round21-measure.py`; `git -C LANE show CAND0:tools/round21-measure.py`; `git clone --shared LANE "$S/clone"` then `git -C "$S/clone" checkout CAND0`; `TMPDIR="$S" python3 tools/round21-measure.py --selftest` from clone and lane; `TMPDIR="$S" python3 "$S/red/c2-count.py" --repo "$S/clone" --rev CAND0 --json`.

## Residual risk / verification gaps

The exact absent-directory failure mode was not run through a scratch copy of the facade; the empty-FLEET c2-count falsifier demonstrates the underlying missing sibling object failure. No tools were installed.

## Summary
- FLEET lookup follows the counter literal; no second hard-coded root.
- All 11 frozen case literals and 13 checks survive; clone and lane selftests pass.
- Empty-FLEET c2-count falsifier is red (0/9 classified, exit 1).
- SKILL.md:1969 “isolated” wording is stale; SKILL.md:2157 is accurate.
- Landed code omits wave-1 missing-root guards (exit 2 diagnostic → uncaught exit 1).
