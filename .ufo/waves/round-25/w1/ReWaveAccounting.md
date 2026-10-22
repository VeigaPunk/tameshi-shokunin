# ReWaveAccounting — re-attack of round-23 wave-2 item WaveAccounting

Verdict: FINDING. The round-23 wave-2 counts hold: 30 completed, 34 dead, no replacement, and report presence was never counted as completion. The dispatched role mix also matches the actual swarm registry seat for seat. But the recorded basis for the 34 deaths is contradicted by the same file that records it. Every dead row says "child transcript ends without session_exit", yet every dead row also records a `session_exit` whose timestamp equals the transcript's last entry. A second, smaller defect: the claim that outputs were persisted "byte-exact" is false by one trailing newline in all 31 L1-persisted files. Both defects still apply unchanged at lane revision c9ff09fb41fb8aac5fc335faf10858ff606bd5df.

Axes checked: callback authority fidelity, absence of dead-seat replacement, report presence versus completion, role mix versus the actual registry, and provenance honesty of the recorded death basis.

## What holds (checked, AGREE)

- **Callbacks.** All 30 completed rows in `.ufo/waves/round-23/original-outcomes2.json` carry a callback.
  - Each callback's `callback_sha256` equals the SHA-256 of the stored callback text (30/30).
  - Each callback header carries `status="completed"` with the matching `id=` and `agent=` (role).
  - Each `callback_delivered_in_author_session_at` falls before the author died (the latest is 14:56:52.693Z; the author died at 14:57:01.318Z).
  - All 34 dead rows have `callback: null`, `callback_sha256: null` and `raw_status: null`.
- **No replacement.**
  - All 64 rows have `replaced: false`.
  - There is only one wave-2 dispatch (`dispatch2-attempt1.json`).
  - The w2 `swarm-registry.json` has 64 members, every one with `agentId == "TameshiR23." + name`. It was last updated at 14:51:29Z, before any death.
  - The accounting bundle's w2 outcomes match `original-outcomes2.json` on id, role, status and `replaced` for all 64 seats.
- **Report presence is never completion.**
  - Replay16 is the only seat that is failed but has a report file (`w2/Replay16.partial.md`, 2337 output characters). It stays failed.
  - Every other w2 report file belongs to a seat whose callback says completed. Replay40–43 each have both a seat-written `.md` and an L1 `.output.md`.
  - The gate reports Replay16 under `failed_with_report` and does not count it as completed.
- **Role mix versus the actual registry.** The four counts below are identical, and the seat-to-role maps match exactly:
  - the roles in `spec2.json` (and `spec2-draft.json`);
  - the roles in `task-call2.json`;
  - the roles in the w2 `swarm-registry.json`;
  - the roles in the `original-outcomes2.json` rows.

  The count is reviewer 20, connector 17, critic 12, simplifier 4, revenger 3, executor 3, scout 2, mutation-tester 1, sentinel 1, scribe 1. The `roles` block in `route-mix2.json` is the same. The mix reported at `corpus/lessons/round-23.md:124-126` matches. `route-mix-final.json` and `route-mix-before.json` belong to wave 1 (they match `spec1.json`), not wave 2. "All 20 reviewers are among the dead" holds: 20 of the 34 dead rows are reviewers.
- **Gate rerun at the lane revision.** I cloned into `/tmp/rewaveacct` and checked out c9ff09f, then ran `python3 tools/wave-accounting.py --bundle .ufo/evidence/round-23/accounting/bundle.json --expected .ufo/evidence/round-23/accounting/expected.json`.
  - Output: `WAVE_ACCOUNTING: clean`, `FINDINGS: ` (empty), `{"completed": 93, "dead": 35, "seats": 128}`, exit 0.
  - With `--json`, w2 shows completed 30, dead 34, `failed_with_report ['Replay16']`, report_artifacts 31.
  - The bundle's SHA-256 is 6e450f77…94db, which equals `expected.json`.

## Counterexample 1 — false death basis (main finding)

The claim, in three places:
- `original-outcomes2.json`: all 34 dead rows have `death_basis` = "no task-result callback retained: parent TameshiR23 session ended 2026-10-21T14:57:01Z; child transcript ends without session_exit".
- `corpus/lessons/round-23.md:129-131`: "each child transcript ends with `Request was aborted`, without session_exit, when the parent ended."
- `SCORECARD.md:1085`: "each transcript ends with `Request was aborted` when the parent ended."

What the same rows record:
- All 34 dead rows have `session_exit = {"reason": "dispose", "kind": "normal", "recordedAt": ...}`, recorded between 15:04:01.530Z and 15:04:01.852Z.
- In all 34, `last_entry_timestamp == session_exit.recordedAt`. So the last transcript entry is the session exit record, not the abort.
- The `Request was aborted` errors (`last_error_timestamp`) fall between 14:55:13Z and 14:57:01.337Z, about seven minutes before the last entry.
- The file was recorded at 15:09:32Z, after those exit records existed.

How I checked: a Python pass over `original-outcomes2.json` printed `dead rows with session_exit recorded: 34 all last_entry==exit: True`. All 34 dead rows have last_error `Request was aborted`, last stop reason `aborted`, and exit `dispose` / `normal`.

Impact:
- This is a provenance-honesty defect only. The dead status rests on the absence of a callback, which is independently true, so no count changes.
- The recorded mechanism of death is still false. It is also the basis that R23-ROUTED-3's "dead-falsifier coverage disposition" inherits.

Can it still be re-verified? No. The child transcripts named in every row (`…/TameshiR23/TameshiR23.<seat>.jsonl`) and the author transcript `…/TameshiR23.jsonl` no longer exist. That session directory was rewritten at 2026-10-22 04:06 -0300 and now holds only `.md` files; the wave-2 seat files I opened, such as `TameshiR23.Replay01.md` and `TameshiR23.WaveAccounting.md`, are 0 bytes. A `find /home/vgpnk -path '*01a15c83-baa6*' -name '*.jsonl*'` returns only the top-level orchestrator session file. So `transcript_sha256` can no longer be checked against bytes. The frozen JSON is the only remaining evidence, and it contradicts itself.

Still applies at c9ff09f: yes. `git show c9ff09f:corpus/lessons/round-23.md` lines 129-131 and `SCORECARD.md:1085` are unchanged. `git grep 'without session_exit' c9ff09f` still hits every dead row of `original-outcomes2.json`. No later erratum mentions `session_exit`.

Smallest safe correction: add an append-only erratum to the round-23 lesson and SCORECARD, leaving the frozen JSON unedited. It should say:
- the 34 dead transcripts' last recorded entry was a harness `session_exit` (reason dispose, kind normal) at 15:04:01.530–.852Z;
- this came after their final `Request was aborted` error at 14:55:13–14:57:01Z;
- the dead status rests only on the missing callback;
- the transcripts named by `transcript_sha256` were deleted on 2026-10-22, so those digests can no longer be checked.

## Counterexample 2 — "byte-exact" persistence is off by one LF

The claim:
- `corpus/lessons/round-23.md:138-139`: "L1 persisted the other completed outputs byte-exact (`w2-persisted-outputs.json`)".
- `w2-persisted-outputs.json`: `equals_final_output: true`.

What the files show, for all 31 L1-persisted files (27 seat reports, Replay16.partial and the four Replay40–43 `.output.md` files):
- The file's SHA-256 matches `w2-persisted-outputs.json`.
- The file's SHA-256 never equals the row's `final_output_sha256` in `original-outcomes2.json`.
- After stripping one trailing `\n`, the digest does equal `final_output_sha256`. The byte lengths are `final_output_chars + 1`; for example, Replay21 is 6183 bytes against 6182 characters.

Impact: low-severity calibration. The content is identical apart from an appended LF. But a consumer that checks file digest against `final_output_sha256` fails 31 out of 31.

Smallest safe correction: an append-only erratum saying "final output plus one trailing LF; file digest differs from `final_output_sha256`".

## Observation (not counted as a counterexample)

- `route-mix2.json` is a file-config prediction: zai 25, google-antigravity 17, openai-codex 17, xai-oauth 4, anthropic 1, and no opencode-go.
- The providers actually observed on the 34 dead seats were anthropic/claude-haiku-5-5 on 19 seats (17 reviewers and 2 revengers), opencode-go/deepseek-v4.1-flash on 12 (10 connectors and 2 scouts), and zai/glm-5.3-flash on 3 reviewers.
- The 30 completed rows have no `observed_provider` field, and no `answering-models2.json` exists. The actual provider mix for wave 2 is therefore unrecorded for 30 of 64 seats, and with the transcripts gone it can no longer be recovered.
- Round 23 already states that file-config routing is not answering-model evidence (`corpus/lessons/round-23.md:43`), so this is a gap, not an overclaim.
- Rerunning `tools/wave-route-mix.py --spec .ufo/waves/round-23/spec2.json` in the clone now gives `REFUSE … cursor=29/64` (exit 1), because the live config has changed. The route-mix receipt is not reproducible after the fact.

## Lane-revision tooling status

- `tools/wave-accounting.py` and `tools/wave-route-mix.py` are byte-identical at 549ede2 (round 23), c9ff09f and the working tree. Their SHA-256 digests are 96b3038a…fd8e and 1954c409…2782.
- `tools/command-binding.py` changed after round 23 (d533dc1e… to 9230c68e…). The only change is that the selftest now also loads `.ufo/evidence/round-24/extra-cases.json`; that does not affect accounting.
- The rows for `tools/wave-accounting.py` in `tools/registry.json` at c9ff09f still pin only the round-22 bundle (`wave-accounting-frozen-entry`, expecting 66/80/146). They do not cover the round-23 accounting receipt. Nothing in this finding depends on that row.

Commands run: only read-only Python and git reads with `GIT_OPTIONAL_LOCKS=0` in the lane. Tools were executed only in the `/tmp/rewaveacct` clone. No tools were installed or updated.

R23-REATTACK WaveAccounting: FINDING
