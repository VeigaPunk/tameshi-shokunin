# Wave 1 — MutC1SelfPin: C1/C2 self-pin mutation probes

Scratch: `/tmp/tameshi-r42-MutC1SelfPin-1` (mutated), `/tmp/tameshi-r42-MutC1SelfPin-3` (pristine), both `git clone --shared` of the lane at 322b5cd32b4319a05340d249ae752d12a9e6b19f. Lane left untouched (bytes re-verified, see bottom).

Counting commands per contract: C1 `python3 .ufo/evidence/round-42/calibration/measure.py --lane LANE --rev REV --freeze FREEZE`; C2 `python3 .ufo/evidence/round-42/census/measure.py --lane LANE --rev REV --freeze FREEZE`. Freeze used throughout except the re-pin runs: 322b5cd32b4319a05340d249ae752d12a9e6b19f.

## Findings

1. **C1 self-pin refusal (mutated running file)** — append a comment line (`#`) to the clone's C1 counter, commit (`1a354fe3539ec593e6c0b86d19ffd056f2ca6d27`; sha 9782a5a0e6404d2f305a51db085c7606914a2c381b35da7f7927c804df914c0e → 58387405934248045841ed94b9ef9d9a2c92a61fc93df5cae1e83a7b97925c28), run `--rev HEAD --freeze 322b5cd...`:

   ```
   C1_R42: SETUP self_pin=0 pin=9782a5a0e6404d2f305a51db085c7606914a2c381b35da7f7927c804df914c0e rev=1a354fe3539ec593e6c0b86d19ffd056f2ca6d27 freeze=322b5cd32b4319a05340d249ae752d12a9e6b19f
   ```
   Exit **2**. The running file's sha ≠ the pin from the contract at freeze → refusal. Expected refusal confirmed.

2. **C1 refusal when only the REV copy is modified (running file pristine)** — pristine counter (`/tmp/tameshi-r42-MutC1SelfPin-3`) run with `--lane` = scratch-1 (whose tip holds the mutated copy) at `--rev 1a354fe...`:

   ```
   C1_R42: SETUP self_pin=0 pin=9782a5a0e6404d2f305a51db085c7606914a2c381b35da7f7927c804df914c0e rev=1a354fe3539ec593e6c0b86d19ffd056f2ca6d27 freeze=322b5cd32b4319a05340d249ae752d12a9e6b19f
   ```
   Exit **2**. The counter refuses on any of the three copies (at freeze, running, at REV) deviating from the pin.

3. **C1 lane run with `--rev HEAD` does NOT refuse on the current lane** — lane HEAD is 322b5cd (the freeze) and the lane's counter copies are unmodified, so all three copies equal the pin:

   ```
   MISMATCH m10 .ufo/waves/round-41/residual/receipt.json asserts present=false for .ufo/waves/round-41/residual/ResidualReceipts.md; tree says true
   MISMATCH records 3 of 6 round-41/42 records present
   C1_R42: self_pin=1 m6=0 m7=0 m8=0 m10=1 m11=0 total=1 records=3 sources_rows=109 rev=322b5cd32b4319a05340d249ae752d12a9e6b19f freeze=322b5cd32b4319a05340d249ae752d12a9e6b19f C1_R42_PASS=false
   ```
   Exit **1** (not a refusal). The task's premise "modified copy at REV" does not hold on the lane (HEAD == freeze, counter unmodified), so no refusal is expected or observed; the refusal mechanics are proven by probes 1–2 instead.

4. **C1 re-pin forgery** — edit the clone's contract `claims.C1.counter_sha256` to the mutated hash (58387405...), commit (`f2ad7e05a9ab82d7e4b94e929f201cbf18f3f66b`; contract sha 437afc7d692ca3e15288e488de0f4dd2ebb24c85bf0cf30cd463dab0caa3fc20 → b727071a30ead4c75194766edd4c711fd5da96b359cdce3847e814e93d7e6615), run `--rev HEAD --freeze HEAD`:

   ```
   MISMATCH m10 .ufo/waves/round-41/residual/receipt.json asserts present=false for .ufo/waves/round-41/residual/ResidualReceipts.md; tree says true
   MISMATCH records 3 of 6 round-41/42 records present
   C1_R42: self_pin=1 m6=0 m7=0 m8=0 m10=1 m11=0 total=1 records=3 sources_rows=109 rev=f2ad7e05a9ab82d7e4b94e929f201cbf18f3f66b freeze=f2ad7e05a9ab82d7e4b94e929f201cbf18f3f66b C1_R42_PASS=false
   ```
   Exit **1**. `self_pin=1`: a revision can agree with itself by carrying a re-pinned contract whose freeze is its own commit. A reader can detect it: (a) the printed `freeze=f2ad7e05...` ≠ the contract's freeze commit 322b5cd — the deciding run's kill rule fixes `--freeze` to 322b5cd, under which probe 1's refusal fires; (b) the contract at the fake freeze carries `counter_sha256` 58387405... ≠ the frozen contract's 9782a5a0... (contract sha differs from 437afc7d...); (c) the history shows an extra commit on top of 322b5cd.

5. **C2: identical behavior** — append a comment line to the clone's C2 counter, commit (`191014b063a573b145cd18e53e2fb8e5c0515bdd`; sha 3c3727ece033263f9e68ca2601012dc0170c6387cee44f3e7c09ee5744890ff2 → fef21b1604e1e41e27a641e3505ff2d25c90daae096c6165170adb2c5aaa0a4a):

   ```
   C2_R42: SETUP self_pin=0 pin=3c3727ece033263f9e68ca2601012dc0170c6387cee44f3e7c09ee5744890ff2 rev=191014b063a573b145cd18e53e2fb8e5c0515bdd freeze=322b5cd32b4319a05340d249ae752d12a9e6b19f
   ```
   Exit **2**. Pristine running file against the mutated REV copy: same refusal, exit **2**. Lane run `--rev HEAD` (unmodified): `C2_R42: tool_absent=1 v3_sha_ok=1 v2_sha_ok=1 live_unflagged_v3=3 rev=322b5cd... freeze=322b5cd... C2_R42_PASS=false`, exit **1** (no refusal; v4 tool does not exist at the freeze). Re-pin forgery (contract C2 pin → fef21b16..., commit `58b1986b6f42fb159b8dd0e2b8d0ced65058c4af`, contract sha → 47aec29a21d6b21304b4b29d1e9d8a0415295c634fbb487c5f0014d4295e15cf): `C2_R42: tool_absent=1 v3_sha_ok=1 v2_sha_ok=1 live_unflagged_v3=3 rev=58b1986b... freeze=58b1986b... C2_R42_PASS=false`, exit **1** — self_pin passed, run proceeded; same detection surface as C1.

## Verdict

- Mutant (appended comment byte on C1 counter) → **killed** (refusal, exit 2). Same for C2.
- C1/C2 self-pin is a working invariant: it refuses on running-file mutation, REV-copy mutation, and freeze-copy mutation. The only re-pin path requires editing the contract, which is externally detectable (freeze ≠ 322b5cd, non-official `counter_sha256`, extra commits).

## Environment

- No tools installed/updated; no pacman transactions (not needed).
- Lane checkout untouched: final `sha256sum .ufo/evidence/round-42/calibration/measure.py .ufo/evidence/round-42/census/measure.py .ufo/evidence/round-42/contract.json` = 9782a5a0e6404d2f305a51db085c7606914a2c381b35da7f7927c804df914c0e / 3c3727ece033263f9e68ca2601012dc0170c6387cee44f3e7c09ee5744890ff2 / 437afc7d692ca3e15288e488de0f4dd2ebb24c85bf0cf30cd463dab0caa3fc20; `git rev-parse HEAD` = 322b5cd32b4319a05340d249ae752d12a9e6b19f. Scratch clones deleted before return.
- Could not check: any hypothetical lane tip past the freeze (lane HEAD is the freeze itself); nothing else was unverifiable.
