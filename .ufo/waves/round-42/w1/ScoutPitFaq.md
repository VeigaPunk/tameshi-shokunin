# Scout: PIT FAQ (Source S156) — round 42, wave 1

Scout: L1Tameshi42.ScoutPitFaq — access date 2026-10-25
Milestone: Source S156. Findings first, evidence below.

## Findings

1. **Snapshot taken.** `curl -fsSL https://pitest.org/faq/` saved to
   `/tmp/tameshi-r42-ScoutPitFaq-l1/pit-faq.html`.
   - sha256: `ccf6ac493d6935e2f0a90b716254c57024973d5e2bf1bf3c1e8e60b9772629c1`
   - bytes: 20845
   - title: `FAQ` (from `<title>` of the fetched HTML)

2. **Results can differ between runs (verbatim, 24 words, line 293).**
   Raw source line 293 (inside section "Is it random?", heading at raw line 287):
   > Pitest works hard to be fully deterministic, but two factors might cause the
   > results to differ slightly between two runs with the same input.

3. **Timeouts are a cause (verbatim clause, 17 words, lines 298–299).**
   Under heading "Timeouts" (`<h3 id="timeouts">` at raw line 295); the sentence
   spans raw lines 298–299, and its cause clause is:
   > a mutant may be detected as timed out on one run, but killed or surviving on another.
   Full sentence (33 words, line 298–299): "Both these measurements can be
   affected by external factors (other processes on the machine etc), so a mutant
   may be detected as timed out on one run, but killed or surviving on another."
   Preceding sentence (line 297): "Mutants causing infinite loops are detected by
   comparing the time taken to run a test without the mutant to the time taken
   when the mutant is present."

4. **Staged recheck passes: count = 1** (row S160's expected value). Exact
   recheck command from `SOURCES.append.md` line 14, run against the live URL:
   ```
   $ curl -fsSL 'https://pitest.org/faq/' | grep -c 'timed out on one run'
   1
   ```
   The string also occurs exactly once in the snapshot (`grep` of the saved file
   gives the same count), so the row's anchor string is verified verbatim.

## Commands / evidence

- Snapshot:
  `mkdir -p /tmp/tameshi-r42-ScoutPitFaq-l1 && curl -fsSL https://pitest.org/faq/ -o /tmp/tameshi-r42-ScoutPitFaq-l1/pit-faq.html`
- Checksums:
  `sha256sum /tmp/tameshi-r42-ScoutPitFaq-l1/pit-faq.html` →
  `ccf6ac493d6935e2f0a90b716254c57024973d5e2bf1bf3c1e8e60b9772629c1`
  `wc -c /tmp/tameshi-r42-ScoutPitFaq-l1/pit-faq.html` → `20845`
- Title + line locations (python over the snapshot):
  - title: `FAQ`
  - `Is it random?` → raw line 287
  - `Timeouts` heading → raw line 295
  - `Pitest works hard …` sentence → raw line 293
  - `Both these measurements …` sentence → raw lines 298–299
  - `Static initializers` heading → raw line 301 (second factor named in the same FAQ answer)
- Recheck count: `1` (expect 1, per S160 row).

## Could not check

- Nothing. The live page fetched cleanly; the snapshot and the live recheck
  agree. No tools were installed (curl/grep/python3 already present; no
  tooling authorization record needed).
