# VER-T8 — fifth-case verifier: independent re-derivation of ONE mutant outcome (B2)

Verification run 2026-10-14 19:19–19:23Z by lane VER-T8 (round-8 32-lane wave;
poll `/tmp/w8-ver-t8-poll.log` — 21 samples, 20 s cadence, note found 19:18:10Z;
scratch `/tmp/w8-ver-t8-work/`). **Read-only on every substrate**: the note,
`kagi-shokunin/` and `tameshi-shokunin/` were only read and byte-copied; the
mutant executed in `/tmp` against the selftest's own `mktemp -d` fixtures. The
only fleet file written by this lane is **this report**. No secret file read;
no external site; no substrate-mutating command. No file was edited.

**Artifact under verification.** `tameshi-shokunin/corpus/knowledge/
mutation-case-kagi-checklist.md`, sha256
`43da70e675b8a482c942fddf6360d84970cf0c29ee648039e11b3b819ae739e7`, 22 952 B,
367 L (`wc -lc`, 19:23Z). It landed 19:18:10Z and four distinct revisions were
observed during my read window (`25f50378…` → `ba390484…` → `8cc06046…` →
`43da70e6…`; sizes 22 810 → 22 881 → 22 957 → 22 952 B). It was stable across
four consecutive samples 19:19:44–19:20:29Z and unchanged at close (19:23Z).
Everything below binds to `43da70e6…` only; the B2 row and spec were re-read
**after** stabilization, and no claim here used an earlier revision.

**Chosen mutant — B2** (note §2 row `:117`; spec §9 `:301-303`; adjudication
§3 `:151-154`): by-hand non-space reason floor at `checklist-run.sh:160`,
`((ns >= 20))` → `((ns >= 0))`. Note's claim: **KILLED — exit 1, exactly 1 of
34 failing cases, label `padded reason: exit 0 want 2`**, under the §3 rule
(case loop ran to completion; n = number of label lines).

## 0. Method (my own tooling, not the producer's)

- O byte copy: `cp -p kagi-shokunin/corpus/checklist-run.sh
  /tmp/w8-ver-t8-work/pristine.sh`; `cmp` identical; sha256
  `7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf` = the
  note's pinned target = `git show HEAD:corpus/checklist-run.sh | sha256sum`
  blob digest (kagi HEAD `fecee87`, porcelain empty at open and at close).
- O one-edit driver `apply_edit.py` (written by this lane): refuses unless the
  `@old` string occurs exactly once; refuses a no-op. Two independent
  constructions of the same edit — (a) the full source line from my copy
  (8-space indent), (b) the note's literal `@old`/`@new` texts decoded per the
  harness convention (1 separator space → 4-space substring) — produced
  **byte-identical** mutants, sha256
  `7ac5b530be8522df27e5d9ea781f1ddda70ce4593ac881ac1629c340e84163db`.
- O edit shape: `diff -u pristine mutant` = exactly one changed line (`:160`),
  matching the note's §0 "exactly one changed line for all 15".
- O mode artifact (mine; recorded so a re-runner does not misread it): the
  selftest re-execs its own copy (`$SELF`), so the mutant must carry the
  pristine's 755 bit. My driver wrote 644 first → every case read
  `exit 126 want …` (34 ms; kept as `evidence/B2.artefact-644.out`); `chmod
  755` and re-ran. Not a finding about the note: the producer's harness copies
  keep the mode (its `sweep/` mutants stand 755).
- O suite runs: `bash mutant-B2.sh --selftest` ×2; same-window control
  `bash pristine.sh --selftest`. Independence order: the mutant was built and
  both mutant runs completed **before** any read of the producer's
  `sweep/results.tsv`; the sha cross-check in §1 came after.

## 1. Result — claim vs re-derivation

| cell | note (§2/§3) | my run (O) | match |
|---|---|---|---|
| verdict | KILLED | killed (rc 1) | ✓ |
| exit | 1 | 1 | ✓ |
| failing cases | 1 of 34 | 1 of 34 | ✓ |
| label | `padded reason: exit 0 want 2` | `checklist-selftest: FAIL padded reason: exit 0 want 2` | ✓ |
| final line | §3 rule → `FAIL (1/34 cases)` | `CHECKLIST_SELFTEST: FAIL (1/34 cases)` | ✓ |
| control | `PASS (34 cases)` | `PASS (34 cases)`, rc 0 | ✓ |

Verdict: **CONFIRMED** for B2 (the one mutant outcome, independently
re-derived on this host at the bound revisions).

Cross-check (O, after my runs): the producer's `sweep/results.tsv:5` reads
`B2 KILLED 1 1953 7ac5b530…163db` — the swept mutant is **byte-identical** to
my independently built one (same sha256), same exit, same single-label
outcome. Durations differ (1 953 ms swept; 2 044 / 2 041 ms mine) — host
timing, not verdicts.

## 2. Spot-checks (three, re-runnable)

- **SC1 — mutant identity + the sharpest label.** `sha256sum
  /tmp/w8-ver-t8-work/mutant-B2.sh` → `7ac5b530…163db` (= producer's
  per-mutant sha); `grep -c '^checklist-selftest: FAIL' evidence/B2.run1.out`
  → `1`; the single label plus final line are the two lines of
  `evidence/B2.run1.out`.
- **SC2 — control + determinism.** `bash pristine.sh --selftest` → rc 0,
  `CHECKLIST_SELFTEST: PASS (34 cases)`; mutant runs 1 and 2 are
  byte-identical (`cmp`), both rc 1 / `FAIL (1/34 cases)`; both controls
  (pre-note 19:11Z, 2 011 ms; same-window, 2 024 ms) are byte-identical too.
- **SC3 — write fence.** Live gate sha256 still `7e5ec98b…576bf`; `kagi git
  status --porcelain` → 0 lines (open and close); note sha unchanged
  `43da70e6…739e7`; `pristine.sh` still `cmp`-identical to the live file; all
  mutants and evidence under `/tmp/w8-ver-t8-work/` only.

## 3. Unknowns

- U1 — one row only: the other 14 mutants and the 7/15 headline were not
  re-derived here.
- U2 — revision binding: the note is append-only and its author may land
  errata; any edit after 19:23Z needs a re-run against the new sha.
- U3 — single host, 2026-10-14; wall-time varies run to run (control 1 870 ms
  noted vs 2 011 / 2 024 ms mine) — durations are not verdicts.
- U4 — the 644-mode artifact generalizes to any naive rewrite; that none of
  the producer's 15 mutants lost the exec bit is read from their files (755),
  not re-measured per mutant.
- U5 — the note's §4 survivor probes were not re-run (B2 is a kill; no probe
  row claims one).
- U6 — I did not execute the producer's harness; the sha equality shows the
  mutant bytes match, not that the harness stays byte-stable for other runs.

## 4. Evidence inventory (`/tmp/w8-ver-t8-work/`)

`pristine.sh` (`7e5ec98b…`) · `mutant-B2.sh`, `mutant-B2b.sh` (`7ac5b530…`) ·
`apply_edit.py` · `B2.old|new`, `B2.note-old|new` · `evidence/`:
`control.selftest.txt`, `control2.out|meta`, `B2.run1.out|meta`,
`B2.run2.out|meta`, `B2.artefact-644.out`, `kagi-pre-state.txt`; poll
`/tmp/w8-ver-t8-poll.log`.

## Errata (append-only)

(none yet — new entries go below this line, never edits above)