# RR1 — cold-read re-read, SKILL.md 497-526 `## Fail-closed arm taxonomy`

- Read rev: `0ff273448ac4e62893c9b28a4cea7c580712df19` (clone `/tmp/tameshi-r17w3-RR1-kqbQWS/fleet/tameshi-shokunin`, detached, clean; `git rev-parse HEAD` → `0ff27344…`, `status --porcelain | wc -l` → 0).
- Page identity: `sha256sum SKILL.md` → `de6c2b083be6f35d2c35e011ca37874f57204a2cdd195a106ff638fbea723dbc`, 1903 lines — matches the pinned page sha.
- Section identity: `sed -n '497,526p' SKILL.md | sha256sum` → `d49662d4…` (piped, includes trailing newline); lines 497-526 **without the trailing newline** → `562a14fcc387b6a730fc1ad0adaf537617a1c365f3d776f24d7f192401f42c54` — matches the assigned section sha exactly. Heading `## Fail-closed arm taxonomy` is line 497. Convention note: section shas are trailing-newline-stripped.

## Method

The range is a taxonomy table + four doctrine bullets; it contains no executable instruction in the run/build sense. Verification was performed by opening every artifact the range cites and checking each claim against it — first as direct reads, then, per the L1 follow-up (measure.py credits only entries with `commands_executed_count>0` plus committed receipts), re-executed as **11 traced commands** under `trace-inputs.py` in the clone at `0ff27344` (receipts `.ufo/evidence/round-17/coldread/traces/RR1/1-11.json`, all exit 0, outputs identical to the direct reads — verdict unchanged). Sibling reads are pinned via `git -C kagi-shokunin show c2cab35b…:<path>` inside `bash -c`, as instructed. No lane tool was run against the live lane root; no git/jj writes outside the /tmp clone; no sibling repo was modified.

## Evidence opened (all from clone `C` unless marked sibling)

- `corpus/knowledge/gates-survey-kagi.md` (lane, 620 lines): ranges 93-143, 145-153, 187-206, 279-293.
- `corpus/knowledge/gates-survey-kumitate.md` (lane, 382 lines): ranges 70-81, 106-118, 287-292.
- Sibling `kagi-shokunin` HEAD `c2cab35bc92e57e39e5489bac3386db078345b3f` (2026-10-19 22:05:06 -0300, clean tree): `corpus/drift-pins.sh:142-148,252-258`; `corpus/claim-ledger.sh:158-190` (+ header/exit lines via grep: 72-92, 111-112, 212-216, 826-830, 946-976); `corpus/checklist-run.sh` exit/policy headers (35-42, 38-39, 83-88); `corpus/op-ref-probe.sh:25-50`.

## Commands and exits

| Command | Exit | Key output |
|---|---|---|
| clone + `checkout --detach 0ff27344` + hashes | 0 | HEAD `0ff27344…`; SKILL.md sha `de6c2b08…`; 1903 lines; slice sha variants above |
| `git -C $K log -1` + `sha256sum`/`stat` on kagi scripts ($K = kagi-shokunin) | 0 | drift-pins `c138d34c7f0dfe95…` / 19088 B (= survey pin, byte-identical); claim-ledger `93c58272…` / 79301 B / 1319 lines; op-ref-probe `0f1945e8…` / 34362 B / 789 lines; checklist-run `7e5ec98b…` / 24697 B (= survey pin); tree clean |
| `grep -nE 'drift-pins' gates-survey-kagi.md` | 0 | pins `corpus/drift-pins.sh` (451 lines, 19088 B, sha16 `c138d34c7f0dfe95`); "held on re-measure" §562-566 |
| `grep -nE '^# Exit'` on claim-ledger/checklist-run/op-ref-probe | 0 | claim-ledger:82 `0 clean · 1 … · 2 policy/setup error`; checklist-run:39 `… 2 usage/setup/shape` |
| `grep -nE 'exit 2'` on claim-ledger/checklist-run | 0 | claim-ledger:89 `claims are refused (POLICY, exit 2, never run)`; :946-947 `CLAIM_LEDGER: POLICY …` → `exit 2`; checklist-run:36 `shape/policy (exit 2): POLICY · SETUP` |

## Claim-by-claim verification

| SKILL claim (line) | Evidence | Result |
|---|---|---|
| SETUP: exit 2, named line (`ADJACENCY_SCOPE: SETUP (…)`), never bare death; fixture-dir-not-a-dir / `op` absent variants (503) | kagi:93-99 (`scope-gate.sh:184` SETUP line before exit 2; `op-ref-probe.sh:459-465` three SETUP variants); `--src` gone arm in kumitate:70-81/106-118 (exit 2, `--src … is missing`) | ✅ |
| Malformed data: census `die` exit 2 "not a verdict"; scope-gate BAD-ROW → DEFECT exit 1, opposite calls (504) | kagi:100-106 verbatim ("the two gates make *opposite* calls", "deliberately not a verdict") | ✅ |
| POLICY: non-regular / `op://` op-side paths refused before exec (505) | kagi:107-110 (`guard_op_file` :218 non-regular, :222 reference token); op-ref-probe.sh:28-35 live header: "SAFETY (structural, not procedural)" … "refuses (POLICY, exit 2, before exec)" non-regular + reference token | ✅ |
| 5-verb allowlist, quote-stripped matching, 23 denied verbs (505) | claim-ledger.sh:158 `ALLOWED_RE='^(bash|grep|sha256sum|wc|test)$'` (5); :183-184 quote-stripped copy then match; :164 `DENY_WORD_RE` enumerated verbs counted: **23** (op, the-janitor, git, rm, mv, cp, chmod, chown, curl, wget, sudo, ssh, scp, systemctl, tmux, kill, pkill, dd, truncate, shred, ln, rsync, tar) | ✅ (see note 1) |
| nested self-audit; stamp shrink without `--prune` (505) | kagi:117-118 (:218 `CLAIM_LEDGER_DEPTH`), :119-120 (:255 `--prune`); nesting refusal corroborated by live header claim-ledger.sh:212-216 ("refused when it is already inside a ledger run (exit 2)") | ✅ |
| checklist rows naming `op.env` (505) | kagi:134-135 (checklist-run.sh:75 `DENY_CHECK`, enforced :149-150); corroborated live checklist-run.sh:41-42 header | ✅ |
| hashing a no-hash path; drift-pins prints POLICY line, returns DRIFT verdict exit 1 (`:142-148`, `:252-258`) (505) | drift-pins.sh:142-148 read directly: `POLICY  … baseline sha must be `-` (secret-bearing path is never hashed)`, `f_bad++`, continue; :252-258: `((f_bad + s_bad))` → `DRIFT_PINS: DRIFT (…)`, `return 1`; file byte-identical to survey pin | ✅ |
| POLICY class: "refused before exec: exit 2 structural" (505) | claim-ledger.sh:89 + :946-947; checklist-run.sh:36 + :39; op-ref-probe.sh:28-35 + exit lattice :44-45 ("exit 2 SETUP/POLICY (cannot measure, or refused before exec)") | ✅ |
| Zero-work refused; measures-nothing gate must not exit 0 (506) | kagi:139-143 (claim-ledger.sh:757 no-round-tables, :762 vacuous cell audit; "[INF] a gate that measures nothing must not exit 0") | ✅ |
| Deferral: `DEFER … reason=substrate-absent`, counted, never FAIL; guards: tag in data file, both-paths selftest (507) | kagi:187-197 (`DEFER <id> reason=substrate-absent`, "declared, counted, and exit-neutral", "does not fail"); guard sentence completing at :198 ("selftest proves both paths, `:1313-1315`") | ✅ |
| Rule 1 counts: proxy 12/12, claims 5/5, kimi-census 1 token/3 cases, round-gate 7 declared/6 fired (`INTERNAL_ERROR` uncovered), surface-probe + cite-check no token enum, one CLI `--src` exit-2 arm each (511-515) | kumitate:287-292 verbatim on all six counts; `--src` arm asserted with `status === 2` in kumitate:70-81 (cite-check bare run) and :106-118 (surface-probe bare run "observed pass"); empty-scan mapping uncovered | ✅ |
| Rule 2: verdict names the arm; no enum ⇒ can neither declare nor assert coverage (516-518) | kumitate:106-118 ("failClosed is a free-text field … the suite cannot (and does not) assert arm coverage"); token convention evidenced by :287-292 | ✅ |
| Rule 3: `BREADTH-EXCEEDS` never fires, live counts far below pins; zero-POLICY surface question unrecorded (519-522) | kagi:279-291+292 (`exceeds=0` … "never fires because live child counts are far below their pins"); :145-153 (`[UNK] whether that absence is deliberate … is not recorded anywhere I read`) | ✅ |
| Rule 4: cite-check empty-scan exit-2 asserted only as in-process condition, not CLI `return 2` (523-525) | kumitate:70-81 ("asserts the **in-process condition** … does not exercise the CLI `return 2` mapping at 2527-2533") | ✅ |

## Notes (non-blocking)

1. kagi:109 prose says "**22** denied verbs" while quoting the 23-alternative regex that `claim-ledger.sh:164` actually contains; SKILL.md's "23 denied verbs" matches the source of truth. Upstream survey prose miscount only — the section under review is correct.
2. `op-ref-probe.sh` has grown since the kagi survey pinned it (survey: 660 lines / 28660 B / sha16 `509f084ad33229db`; live: 789 / 34362 / `0f1945e8…`), so some of kagi's op-ref-probe line numbers may have shifted [INFERENCE]. This seat's verification did not rely on those line numbers — the POLICY claims were confirmed against the live header text directly. `drift-pins.sh` and `checklist-run.sh` are byte-identical to their survey pins.
3. Two kagi sentences cited by the section complete one line past their cited range (deferral guard 197→198; BREADTH "pins" 291→292). Cosmetic; the claims are fully supported.
4. No installs were needed (python3/git/sha256sum present); pacman untouched.

## Traced verification reads (L1 follow-up — receipts RR1/1-11.json)

All commands wrapped as `trace-inputs.py --root $C --cwd $C --out <receipt> -- <argv>`, rev auto-pinned `0ff273448ac4e62893c9b28a4cea7c580712df19`; **all exits 0**; outputs byte-identical to the direct reads above; receipts 1-7 record `inputs` shas matching the table above exactly.

| # | argv | Verifies |
|---|---|---|
| 1-4 | `sed -n` 93,143p / 145,153p / 187,198p / 279,293p `corpus/knowledge/gates-survey-kagi.md` | SETUP, malformed, POLICY, zero-work, zero-POLICY-unrecorded, deferral, BREADTH-EXCEEDS claims |
| 5-7 | `sed -n` 70,81p / 106,118p / 287,292p `corpus/knowledge/gates-survey-kumitate.md` | cite-check in-process-only hole, free-form failClosed / no-enum consequence, suite-by-suite arm counts |
| 8 | `bash -c "git -C …/kagi-shokunin show c2cab35b…:corpus/drift-pins.sh \| sed -n -e '142,148p' -e '252,258p'"` | POLICY line + DRIFT verdict `return 1` (the stated exception) |
| 9 | `bash -c "git -C … show c2cab35b…:corpus/claim-ledger.sh \| sed -n -e '82p' -e '89p' -e '158,190p' -e '212,216p' -e '946,947p'"` | POLICY exit 2, 5-verb allowlist, quote-strip, 23 verbs, nesting refusal |
| 10 | `bash -c "git -C … show c2cab35b…:corpus/checklist-run.sh \| sed -n -e '35,42p' -e '83,88p'"` | POLICY exit-2 class, `op.env` denial, usage exits |
| 11 | `bash -c "git -C … show c2cab35b…:corpus/op-ref-probe.sh \| sed -n '25,50p'"` | "structural, not procedural", POLICY exit 2 before exec, exit lattice |

## Verdict

Every checkable record claim in `## Fail-closed arm taxonomy` at `0ff27344` is true against its cited evidence and the ground-truth gate sources; no wrong expectation, no blocking gap. **Verdict: holds.**

```json
{
  "schema": "tameshi-coldread-report-v2",
  "seat": "RR1",
  "skill_sha256": "de6c2b083be6f35d2c35e011ca37874f57204a2cdd195a106ff638fbea723dbc",
  "read_rev": "0ff273448ac4e62893c9b28a4cea7c580712df19",
  "sections": [
    {
      "start": 497,
      "heading": "## Fail-closed arm taxonomy",
      "class": "record",
      "verdict": "verified-record",
      "blocking_gaps": [],
      "wrong_expectations": [],
      "minor_gaps": [],
      "commands_executed": [
        "sed -n 93,143p corpus/knowledge/gates-survey-kagi.md",
        "sed -n 145,153p corpus/knowledge/gates-survey-kagi.md",
        "sed -n 187,198p corpus/knowledge/gates-survey-kagi.md",
        "sed -n 279,293p corpus/knowledge/gates-survey-kagi.md",
        "sed -n 70,81p corpus/knowledge/gates-survey-kumitate.md",
        "sed -n 106,118p corpus/knowledge/gates-survey-kumitate.md",
        "sed -n 287,292p corpus/knowledge/gates-survey-kumitate.md",
        "bash -c \"git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show c2cab35bc92e57e39e5489bac3386db078345b3f:corpus/drift-pins.sh | sed -n -e '142,148p' -e '252,258p'\"",
        "bash -c \"git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show c2cab35bc92e57e39e5489bac3386db078345b3f:corpus/claim-ledger.sh | sed -n -e '82p' -e '89p' -e '158,190p' -e '212,216p' -e '946,947p'\"",
        "bash -c \"git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show c2cab35bc92e57e39e5489bac3386db078345b3f:corpus/checklist-run.sh | sed -n -e '35,42p' -e '83,88p'\"",
        "bash -c \"git -C /home/vgpnk/Projects/shokunin/kagi-shokunin show c2cab35bc92e57e39e5489bac3386db078345b3f:corpus/op-ref-probe.sh | sed -n '25,50p'\""
      ],
      "opened": [
        "SKILL.md:497-526 @0ff273448ac4e62893c9b28a4cea7c580712df19 (page sha de6c2b08…, section sha 562a14fc… as trailing-newline-stripped lines 497-526)",
        "corpus/knowledge/gates-survey-kagi.md:93-143,145-153,187-206,279-293",
        "corpus/knowledge/gates-survey-kumitate.md:70-81,106-118,287-292",
        "kagi-shokunin@c2cab35bc92e57e39e5489bac3386db078345b3f:corpus/drift-pins.sh:142-148,252-258",
        "kagi-shokunin@c2cab35bc92e57e39e5489bac3386db078345b3f:corpus/claim-ledger.sh:82,89,158-190,212-216,946-947",
        "kagi-shokunin@c2cab35bc92e57e39e5489bac3386db078345b3f:corpus/checklist-run.sh:35-42,83-88",
        "kagi-shokunin@c2cab35bc92e57e39e5489bac3386db078345b3f:corpus/op-ref-probe.sh:25-50"
      ],
      "inputs": {
        "corpus/knowledge/gates-survey-kagi.md": "4734f0a0bd28e90f78b0a766b2aa6dac8238936550e1b1b0ec3316b00e1294c6",
        "corpus/knowledge/gates-survey-kumitate.md": "3dca7a1a5c621bf0ec75948d0836839dec98651673bb2987861d9aa122579b0e"
      },
      "external_inputs": {
        "kagi-shokunin@c2cab35bc92e57e39e5489bac3386db078345b3f:corpus/drift-pins.sh": "c138d34c7f0dfe950fce0e5e6672cc788b5ad080bc388d4aef118db0e6c70feb",
        "kagi-shokunin@c2cab35bc92e57e39e5489bac3386db078345b3f:corpus/claim-ledger.sh": "93c5827202b9cdecd6874e75c5dac5281eeae07eddeeff3883bd0da14bfbcd29",
        "kagi-shokunin@c2cab35bc92e57e39e5489bac3386db078345b3f:corpus/op-ref-probe.sh": "0f1945e8d8a8fc56aaee256180cd7badde466bc8ac91503aa1e1853e79044f4c",
        "kagi-shokunin@c2cab35bc92e57e39e5489bac3386db078345b3f:corpus/checklist-run.sh": "7e5ec98b9e1d0afaa4d4d0f0d91f897236e8a8b4c7912ccad94d86492fd576bf"
      },
      "traces": [
        ".ufo/evidence/round-17/coldread/traces/RR1/1.json",
        ".ufo/evidence/round-17/coldread/traces/RR1/2.json",
        ".ufo/evidence/round-17/coldread/traces/RR1/3.json",
        ".ufo/evidence/round-17/coldread/traces/RR1/4.json",
        ".ufo/evidence/round-17/coldread/traces/RR1/5.json",
        ".ufo/evidence/round-17/coldread/traces/RR1/6.json",
        ".ufo/evidence/round-17/coldread/traces/RR1/7.json",
        ".ufo/evidence/round-17/coldread/traces/RR1/8.json",
        ".ufo/evidence/round-17/coldread/traces/RR1/9.json",
        ".ufo/evidence/round-17/coldread/traces/RR1/10.json",
        ".ufo/evidence/round-17/coldread/traces/RR1/11.json"
      ]
    }
  ]
}
```
