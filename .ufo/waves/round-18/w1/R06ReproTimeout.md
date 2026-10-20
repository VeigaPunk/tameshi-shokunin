# R06 — Base P09/P10 timeout reproduction

## Evidence setup

Extracted the pinned base bytes with:

```sh
git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show 183f87b899e6cae46be98d251cbc87fb5118f6ca:tools/registry-check.py > /tmp/tameshi-r18w1-R06-Y1we4j/registry-check.py
sha256sum /tmp/tameshi-r18w1-R06-Y1we4j/registry-check.py
```

Exit 0; SHA-256 `0bf9d1d2971c9fe478823754c7b889315585b73361ee3146631f409c4c5a3765`.

## Findings

### P09 — non-finite timeout values reach subprocess execution (reproduced)

At the base, `registry_errors` only checks `ts` type and `ts <= 0` (`tools/registry-check.py:221-227`); `load_registry` uses default `json.loads` (`:273-287`). Thus `NaN` and `Infinity` are accepted by parsing/validation. The accepted value is passed to `proc.communicate(timeout=row["timeout_s"])` (`:382-386`).

Both synthetic registries used the normal schema and `/usr/bin/true` as the row command. The calls, run from the scratch root with inherited `GIT_*` variables unset, were:

```sh
python3 /tmp/tameshi-r18w1-R06-Y1we4j/registry-check.py --root /tmp/tameshi-r18w1-R06-Y1we4j/root --registry /tmp/tameshi-r18w1-R06-Y1we4j/nan.json
python3 /tmp/tameshi-r18w1-R06-Y1we4j/registry-check.py --root /tmp/tameshi-r18w1-R06-Y1we4j/root --registry /tmp/tameshi-r18w1-R06-Y1we4j/infinity.json
```

- `timeout_s: NaN`: exit **1**, traceback ends `ValueError: cannot convert float NaN to integer` (`selectors.py`, during `communicate`).
- `timeout_s: Infinity`: exit **1**, traceback ends `OverflowError: cannot convert float infinity to integer` (same path).

Neither produces the required invalid-registry exit 2 naming `timeout_s`; P09 is open at base.

### P10 — `setsid` child escapes the process group; return-time check is pipe-sensitive

The synthetic row was exactly `argv: ["sh", "-c", "setsid sleep 40 & sleep 40"]`, `timeout_s: 1`. A temporary PATH `sleep` wrapper set the sleep process's argv[0] to the unique marker `R06TimeoutMarker-20261020`, allowing `pgrep -f` to identify the detached process. The base starts a row in a new session and timeout cleanup signals only its process group (`tools/registry-check.py:306-323, 368-375, 382-393`).

First run used the marker wrapper with inherited stdout/stderr. Command:

```sh
python3 /tmp/tameshi-r18w1-R06-Y1we4j/registry-check.py --root /tmp/tameshi-r18w1-R06-Y1we4j/root --registry /tmp/tameshi-r18w1-R06-Y1we4j/setsid.json
```

Exit **1**, row output `ROW p10-setsid expect=0 got=timeout differs`; elapsed **40 s** despite `timeout_s: 1`; `pgrep -f '^R06TimeoutMarker-20261020([[:space:]]|$)'` found no process after the checker exited. **[INFERENCE]** The escaped sleeper retained the captured output pipes, so the post-timeout `proc.communicate()` (`:385-387`) waited until the sleeper's natural 40-second exit; that makes this literal after-return check miss the survivor.

To distinguish a clean kill from that wait-induced false negative, I reran the same row and registry with the temporary marker wrapper closing the sleep child's standard pipes. Exit **1**, same timeout row output, elapsed **1 s**. Immediately after registry-check exited, `pgrep`/`ps` found PID `3301177`, PGID/SID `3301177`, command `R06TimeoutMarker-20261020 40`. I sent TERM, then KILL after 0.2 s; a subsequent `pgrep` found none. This confirms a `setsid` descendant can remain alive after registry-check returns when it does not hold its capture pipes open. No marker process was left behind.

## Residual risk / verification gap

The base P10 cleanup does not kill descendants that leave the row process group. However, the prescribed “alive after registry-check returns” observation is not reliable with the unmodified inherited-pipe setup: the observed first run took 40 s and had no marker at return. A P10 fixture should close or redirect the escaped child's captured pipes (or otherwise observe liveness before `communicate()` can wait for natural exit) to make the return-time assertion discriminate this defect.

No source files were modified and no tools were installed.

**Verdict: partial — P09 reproduced open; P10 escape reproduced, but the literal inherited-pipe run is a return-time false negative.**
