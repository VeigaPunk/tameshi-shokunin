# B16QualityCriteria — round 18, wave 1

Seat: TameshiR18.B16QualityCriteria (leaf scribe). Base rev: `183f87b899e6cae46be98d251cbc87fb5118f6ca` (branch master).

## Scope and axes

- **Depth:** one appended criterion per round-17 spot-check §7 routed item, so every routed item has a falsifiable rule.
- **Calibration:** each criterion names what captured the failure and a check that can fail on the retained evidence. No criterion asserts that a check passes.
- Target: staged `corpus/QUALITY.md` only. No lane file, no tool, no gate, selftest, mutant, or measurement was run. No subagent was dispatched. No git write was performed; `git show` and `git status --porcelain` were read-only.

## Output

- Staged file: `.ufo/waves/round-18/staged/corpus/QUALITY.md` (18797 bytes, sha256 `ffed5023df9d4d9b…`).
- Base snapshot: `git show 183f87b…:corpus/QUALITY.md` (9866 bytes, sha256 `94572f6a1b47d846…`), written to scratch `/tmp/tameshi-r18w1-B16QualityCriteria-FXIauD/base.md`.
- Appended block: `/tmp/tameshi-r18w1-B16QualityCriteria-FXIauD/append.md` (scratch), beginning with a blank line and heading `## Criteria appended — round 18`, criteria 29–36.

Assembly and proof (all exit 0):

```
cat base.md append.md > staged/corpus/QUALITY.md
head -c 9866 staged/corpus/QUALITY.md | cmp - base.md          -> PREFIX_IDENTICAL
tail -c +9867 staged/corpus/QUALITY.md | cmp - append.md       -> SUFFIX_IS_APPEND
diff base.md staged/corpus/QUALITY.md | grep -c '^<'           -> 0 (no deleted lines)
diff base.md staged/corpus/QUALITY.md | grep -c '^>'           -> 128 (added lines)
git show 183f87b…:corpus/QUALITY.md | cmp - base.md            -> BASE_MATCHES_REV
git -C <lane> status --porcelain -- corpus/QUALITY.md          -> empty
```

The base ends at line 167 with `\n`; criterion 28 is the last base criterion, so the new block starts at 29.

## Criteria and routed-item mapping

| # | Criterion (short) | Routed item (lesson §7) |
|---|---|---|
| 29 | Guard counts as covered only if its removal makes the owning `--selftest` exit nonzero; survivors killed or named equivalent | Item 3, R17-GUARD-COVERAGE |
| 30 | Lane-state comparisons read `refs/heads/<branch>`, never bare HEAD; jj-colocated fixture | Item 5, R17-JJ-GUARDS |
| 31 | Config numbers finite/positive; timeouts kill setsid descendants | Item 6, R17-TIMEOUT |
| 32 | Every lane git subprocess scrubs `GIT_*`; canary test; pinned-tool fixes via appended waiver/manifest | Item 4, R17-GIT-ENV (keeps criterion 28 debt open) |
| 33 | Input-keyed credit is never described as command coverage; declared commands bound to trace argv | Item 2, R17-CMD-BIND |
| 34 | Citations into moving or unowned files anchored by function/symbol name and rev | Item 7, R17-CITATIONS |
| 35 | Corrections are appended dated errata; append-only files show zero deleted lines; unowned files get routed, not edited | Items 1 and 7, R17-KNOW-EXIT and CORRECTION-MECHANICS (extends criterion 26) |
| 36 | Stray live write is preserved, captured and routed; no ad hoc plumbing repair | Item 8, R17-INCIDENT |

## Source anchors verified at 183f87b

Anchors below were read with `git show 183f87b…:<path> | sed/grep -n` in this session, except where the row says otherwise.

| Anchor cited in criteria | Verified content |
|---|---|
| `tools/evidence-disposition.py:45-48`, `:179-180` | G2/G3 state "HEAD:<path>", "rev … ancestor of HEAD" |
| `tools/evidence-disposition.py:441-451` | `resolve_historical_rev`; `merge-base --is-ancestor … HEAD` at `:450`, return check at `:451` |
| `tools/evidence-disposition.py:518-540` (G2 range, via MutateDispositionV2 report) | Not independently re-read here; cited only in the descriptive text of the report |
| `tools/registry-check.py:221-227` | `ts = row.get("timeout_s")`; `ts <= 0` positive check; error at `:227` |
| `tools/registry-check.py:273`, `:281` | `load_registry` def; `json.loads(raw.decode("utf-8"))` at `:281` (no `parse_constant`) |
| `tools/registry-check.py:306-322`, `:386` | `_kill_group` def at `:306`, `os.killpg` at `:313` and `:321`; call at `:386` |
| `tools/bash-witness-study.py:337-342` | `subprocess.run(["git", "-C", …, "show", …])` with no env argument |
| `tools/bash-witness-study.py` GIT_ hits | Five hits, all identifier `TARGET_GIT_PATH` at lines 97, 339, 342, 359, 887; no `GIT_*` environment name or scrub |
| `.ufo/evidence/round-13/expected.json:11` | `"tools/bash-witness-study.py": "49e9e5e2…350ad80"` |
| `.ufo/waves/round-17/w2/MutateDispositionV2.md`, `MutateRegistryCheck.md`, `MutateTraceInputs.md` | Exist at base; cited for survivors per the lesson's list (not re-executed) |
| `corpus/lessons/round-17-verifier-spotcheck.md` §2 and §7 items 1–8 | Read in full; quoted claims match the text |

Not verified in this seat and carried as lesson-sourced claims: fleet `5d8a3b5` `detect_branch` line 115; SKILL:1029 and the five ER-jj/R3 note citations (criterion 34); the S060/S061 anchor details; the operator-runbook substitution and SOURCES footer details (criterion 35). They rest on the closure's §7 text, not on a re-read of the fleet repository.

## Judgment and caveats

- Criteria 29–36 are rules over evidence the lane already retains or can produce. Each check names the artifact or fixture it runs against; none is a placeholder.
- Criterion 32 does not close QUALITY28's debt. It states that the scrub lands through an appended waiver, consistent with 28.
- Criterion 35 extends criterion 26 from receipts to corpus prose and cites criterion 4 for append-only errata. It does not repeat 26.
- Criterion 36 is a rule about preservation and routing. It does not repair the round-17 incident, and it does not claim the incident is closed.
- Criterion 33's remedy is either a binding or a narrowing. The criterion requires the claim to match the evidence, and it does not choose the remedy.
- Line widths: a few lines exceed 80 bytes (the file's base maximum is 90 bytes). Accepted; no reflow was done so the base prefix stays byte-exact.

## Out of scope and routed

- Fleet/operator: the stray-write recovery helper and its moving line anchors (lesson §7 item 8 and its cross-domain note). Routed, not edited.
- mado: stale prose naming the old runner as the live harness. kaidoku: the staged-pin statement in `ConnFleetJjPractice.md:86-89`. Routed, not edited.
- Owners of `tools/bash-witness-study.py`, `tools/evidence-disposition.py`, `tools/registry-check.py`: the code and selftest repairs themselves. This seat drafted criteria only.

## Installs and tools

No tool was installed or updated. The only commands were `git show`, `git status --porcelain`, `cmp`, `diff`, `cat`, `head`, `tail`, `grep`, `sed`, `awk`, `wc`, `sha256sum`.

## Verdict

built — staged `corpus/QUALITY.md` = base (byte-identical prefix, 9866 bytes) + appended block `## Criteria appended — round 18` with criteria 29–36; no lane file edited; no check run.
