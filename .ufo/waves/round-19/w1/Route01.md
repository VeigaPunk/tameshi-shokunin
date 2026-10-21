# Route01 — R18-1 correction and predicate review (2026-10-21, round 19 w1)

Seat: TameshiR19-2.Route01 (reviewer, read-only). Scope: routed defect R18-1
only — `corpus/knowledge/guard-kill-closure.md:2` stale `verified-at:`
metadata ("PENDING metadata despite measured results", frozen
`contract.json` population). Verdict: **the delivered append-only correction
is exact and every mechanically checkable clause verifies; the landed
failure-capable predicate genuinely fails at baseline and passes at the
delivered revision. No blocking defect found in R18-1's content.** Wave-level
timing risk (F1) and four advisory findings below.

Axes (godspeed): (1) correction correctness — every clause of the erratum
re-derived from committed bytes; (2) predicate failure-capability — the ruler
must be able to say `open`; (3) no-harm — append-only, no fresh-tip claim, 18
survivors stay open; (4) durability — every number revision-bound.

## 1. Defect at baseline `7243e7f163f08978c8fd9b6c1ef67a2fefe7d190`

Observed (`git show 7243e7f…:corpus/knowledge/guard-kill-closure.md`):

- Line 2: `verified-at: 2026-10-20 at lane base 183f87b899e6cae46be98d251cbc87fb5118f6ca. Landed-tip results: PENDING (filled by L1 after landing).`
- No `## Erratum R18-1` section exists; baseline blob sha256
  `02670ef73ee5ff918ed99397ee42904f59a06b234b2d49d16301bc2e1987c859` equals
  `before.json` `inputs` pin for the note.
- `before.json` (tracked, clean at HEAD): `revision 7243e7f…, open=5,
  corrected=0, total=5`, `ruler_sha256 c538c33d6d80c9299183b6ff08a21da6f557fa66f99712f38820fdce1473e18e`.
- Motivating record: round-18 verifier §5 item 1
  (`corpus/lessons/round-18-verifier-spotcheck.md:182-186`, committed at
  `7243e7f`): "The knowledge entry's `verified-at:` line is the metadata
  contract" — the correction had to name that line, not a body statement.

## 2. The correction, as landed at `21e79329f8bdcf01a62be63b3e46db4a7de6b6f9`

`## Erratum R18-1 — verified-at metadata (2026-10-21, round 19)` at lines
171–190 of the 190-line note; `git diff 7243e7f 21e7932 -- <note>` = **21
insertions, 0 deletions** (`grep -c '^-[^-]'` → 0). Stale line 2 is retained
byte-identical; correction is purely additive. Delivered blob sha256
`7728d56acdcaded8cdf10f36058940799e71977d3cadcac724a66487dd50a5b4` equals
`after-21e7932.json` `inputs` pin for the note.

Clause-by-clause re-derivation (all observed this session, 2026-10-21):

| Erratum clause | Check | Observed |
|---|---|---|
| Dated heading (2026-10-21, round 19) | read :171 | present |
| Supersedes line 2's verbatim `Landed-tip results: PENDING (filled by L1 after landing)` | read :173-174; baseline line 2 | exact string match, line named |
| Supersedes staged/PENDING landed-tip statements at lines 10, 53, 65, 91, 97, 114, 118, 120, 122, 132, 134, 136 | `git show 7243e7f…` + awk per line | 11 of 12 carry the literal token `PENDING`; line 134 is the `Not run: no after-landing probe run…` bullet without the token (staged-class; defensible, see F4). No wrong line number found. |
| "describe base `183f87b…`, not the delivered round-18 tools" | consistent with EG-1 wave-2 erratum (:143-147) and §7 | consistent |
| Effective verified-at: tool revision `921ef8077440f90d092aab4b9fdc750a45de1224` | `git cat-file -e 921ef807^{commit}`; `git merge-base --is-ancestor` vs `refs/heads/master` and vs `4b7c682…` | exists; ancestor of both |
| measured by committed receipt `.ufo/evidence/round-18/final/probes.stdout` | `git log -1 --` and `ls-files` | committed at `5923d89` (2026-10-20T18:40:48-03:00) |
| `DEFECT_PROBES: open=0 closed=11 total=11` | `grep '^DEFECT_PROBES:'` | exact line; 11 `^PROBE P` rows, each `closed` (P01–P07 with `pristine_exit=0 mutant_exit=1`) |
| receipt SHA-256 recorded in `final/checks.json`, row `probes` | read checks.json | `probes.revision = 921ef807…`, `probes.exit = 0` (int), `probes.stdout_sha256 = d37c99e33eeb22b1b74b47b5fca26b228407792a5741bfaebc1b8be39aeb8cf0`; `sha256sum probes.stdout` reproduces the digest |
| spot-check independently reconciled that digest (§2 C2) | read spotcheck §2 C2 | spotcheck states the same digest and argv at its declared revision |
| Registry pinned at `5923d89ac491ec3d296905561a8ab0faf3fda65a` in `final/registry-branch-aligned.stdout`: 31 held, four superseded | `grep -o` on the receipt; ancestry | `"held": 31, "superseded": 4, "total": 31, "exit": 0, "rev": "5923d89…"`; `5923d89` ancestor of master |
| "historical revision-bound results, not new runs at the round-19 tip" | read :187-188 | bound stated; matches contract invariant "no numerical calibration score increase" |
| "EG-3's limits and all 18 mutation survivors remain open" | read :188-189 | 3+3+2+10 = 18 per EG-3 and QUALITY 29–31 |
| Recheck guidance forbids unpinned `<branch tip>` claims | read :189-190 | present; neutralizes the stale `recheck:` recipe's placeholder |

Tool-revision honesty: `git diff 921ef807 4b7c682 -- tools/` and `-- .ufo/evidence/round-18/defect-probes.py`
are both **empty** — the receipt's tool revision is byte-identical to the
round-18 landed tip, so "effective at the delivered tools" is true without a
fresh tip run. Metadata-contract conformity: QUALITY 37
(`corpus/QUALITY.md:337-343`, appended round 19) requires that "A metadata
correction names the exact stale provenance field and line" with a dated
erratum giving effective value, measured revision and evidence pointer; every
clause is met, and no second current-result implication remains at
`21e7932`.

## 3. Failure-capable predicate

(a) **Landed ruler** (`.ufo/evidence/round-19/measure.py`, blob at
`21e7932`, sha256 `c538c33d…e18e` — byte-identical to the `ruler_sha256`
pinned in **both** `before.json` and `after-21e7932.json`; the current
`ruler_sha256` = `sha256(git show 21e7932:.ufo/evidence/round-19/measure.py)`,
verified). Its R18-1 `guard()` predicate requires, per run:

1. an `## Erratum R18-1` section exists (absent → `IndexError` → status
   `open`) — QUALITY 37's own falsifier;
2. the erratum names `line 2`, `Effective verified-at:`, the
   `final/probes.stdout` path, `921ef807…`, and `18 mutation survivors`;
3. the stale sentence `Landed-tip results: PENDING (filled by L1 after
   landing).` is still present **before** the erratum — catches in-place
   rewrite (append-only violation);
4. machine agreement: `checks.json` `probes.revision == 921ef807…`, `exit == 0`
   (strict int), `stdout_sha256 == sha256(probes.stdout bytes)`, and
   `probes.stdout` contains `DEFECT_PROBES: open=0 closed=11 total=11`;
   `checks.json` parsed with duplicate-key and non-finite rejection.

Demonstrated failure capability: the same ruler at `7243e7f` returns
`corrected=0, open=5` (`before.json`, exit 1 per the lesson) — it fails on the
baseline rather than being calibrated to pass. Selftest uses isolated
synthetic fixtures and never executes receipt argv.

(b) **Independent auditor re-derivation** (this seat's commands; each can
fail independently of the ruler): the table in §2 is the check list. Fastest
full chain:

```
git show 7243e7f…:corpus/knowledge/guard-kill-closure.md | awk 'NR==2'   # stale line present at baseline
git diff --numstat 7243e7f… 21e7932… -- corpus/knowledge/guard-kill-closure.md   # expect 21  0
git show 21e7932…:corpus/knowledge/guard-kill-closure.md | sha256sum      # 7728d56a… == after.json pin
sha256sum .ufo/evidence/round-18/final/probes.stdout                      # d37c99e3… == checks.json pin
grep -c '^PROBE P[0-9]* closed' + grep '^DEFECT_PROBES:' probes.stdout    # 11 + open=0 closed=11 total=11
git merge-base --is-ancestor 921ef807… refs/heads/master                  # rc 0
```

Failure modes caught: erratum removed or placed inline (numstat ≠ `21 0`, or
split hits nothing); stale line rewritten (predicate 3 / baseline line-2
check); receipt digest drift or argv/revision tamper (§2 rows 8–9); summary
line altered (DEFECT_PROBES check); unpinned revision claimed (ancestry +
revision equality). The audit must read blobs via `git show REV:path`, never
the worktree (see F6).

## 4. Findings by severity

- **F1 — High (wave timing, not correction content).** `after-21e7932.json`
  (the corrected=5/open=0 receipt) is still **untracked**, and LOG.md,
  SCORECARD.md, SHONEN.md, SKILL.md, QUALITY.md, README.md, SOURCES.md, both
  knowledge notes, `corpus/lessons/round-19.md` and `measure.py` are
  modified-uncommitted at observation (2026-10-21). Until L1 commits the
  after-receipt, C1's delivered-side measurement is not durable at a revision
  (FrozenPopulation Cx-1, concurred). Any further commit supersedes
  `21e7932` as tip and needs a fresh ruler receipt at the new tip; the
  `21e7932`-bound receipt remains valid as a historical record.
- **F2 — Low (delivered bytes).** The committed erratum's inventory covers the
  12 PENDING/staged lines but not the two conditional provenance phrases at
  lines 99 and 133 ("once its anchor is widened", "once B13 installs it"),
  which are now historical (S063 widened, S068 landed by `4b7c682`). The
  uncommitted worktree addendum covers exactly this; graded Low because they
  are not PENDING-marked result claims. Re-grade when it commits.
- **F3 — Low (ruler depth, Cx-2 class).** `guard()` does not verify the
  12-line list's accuracy, the registry citation, the checks.json citation,
  or the erratum date; a wrong-but-present fact there would pass. This seat's
  §2 re-derivation found all such facts accurate. Do not extend the frozen
  ruler mid-claim (`c538c33d…`); note for future rounds.
- **F4 — Info.** Line 134 lacks the literal `PENDING` token (it is the "Not
  run:" bullet); the erratum's "staged/PENDING landed-tip statement" wording
  covers it. Recorded for honesty, no action.
- **F5 — Info.** Cosmetic missing spaces in committed prose
  (`not4b7c682`, `exact4b7c682` in the round-19 lesson; `at4b7c682` in the
  uncommitted addendum). No predicate string is affected.
- **F6 — Info (discipline).** Worktree `measure.py` (a25f4c7c…) is an
  uncommitted edit; the pinned ruler is the committed blob (c538c33d…), which
  both receipts pin. Auditors must hash `git show <rev>:path`.

No Medium or Blocker finding within R18-1's delivered content.

## 5. Residual risk and verification gaps

- Receipts were **not re-executed** (lane prohibition on rerunning old
  tools); correctness rests on the digest chain (erratum ↔ checks.json ↔
  probes.stdout), all verified byte-level here, plus the round-18 non-author
  spot-check's independent §2 C2 reconciliation (read, not rerun).
- P01–P11 row-level probe correctness was not re-derived (out of scope;
  covered by the spot-check). I read all 11 rows: each reads `closed`.
- `before.json` is tracked and clean; `after-21e7932.json` carries no
  embedded timestamp (run time bounded only by commit times) — accepted,
  revision binding is the load-bearing field.
- No LSP server exists for this Markdown/corpus target; all checks were
  text/blob reads (`git`, `sha256sum`, `grep`, `awk`), used as ground truth.
- The worktree addendum's source claims (S063/S068/S075–S078 used-by) were
  not verified — uncommitted work outside R18-1's delivered scope.

## 6. Tooling statement

No tool installed or updated; no pacman transaction; no lane selftest,
build, lint, formatter, or ruler execution. Commands: read-only
`git log/status/show/diff/numstat/merge-base/cat-file/ls-files`,
`sha256sum`, `grep`, `awk` under the lane repo.
