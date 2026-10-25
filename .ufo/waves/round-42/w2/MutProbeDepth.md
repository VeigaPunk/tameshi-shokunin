# MutProbeDepth — MAX_DEPTH mutation probe on census v4 (round 42, wave 2)

Attacked thing: `tools/write-path-census-v4.py:71` `MAX_DEPTH = 8` and the knowledge-entry
sentence `corpus/knowledge/r42-attribute-and-outflag-destinations.md:48` "Resolution depth
rises from four to eight hops: the context-capture chain needs six."

## Findings

1. **The smallest depth the battery accepts is 7, not 6.** 8→7 survives. 8→6, 8→5 and 8→4
   are killed. 8→6 is killed by `tools/registry-replay.py:123`, not by context-capture.
2. **"The context-capture chain needs six" is accurate.** `context-capture.py:1682` and `:1685`
   pass at 6 and fail at 5 (`scratch=0`). The binding gate is `_resolve` (`v4.py:172`).
3. **The sentence leaves out the deepest chain.** `registry-replay.py:123` needs 7. That
   requirement comes from the `_parse_args_ns` gate (`v4.py:262`), on the path
   `_out_flag` (`:278`) → param-call trace → `parse_args` namespace. The record never names
   this requirement. A reader of `:48` would conclude that 6 is the floor.
4. **Coverage finding: 8→7 is a surviving mutant.** The frozen battery cannot tell the declared
   bound of eight (`v4.py:36` docstring, entry `:48`) from seven. No fixture or live site
   exercises the eighth level. This is a coverage finding only; it does not authorize a
   contract change.

## Assigned probes (via the pinned counter)

Live source `tools/write-path-census-v4.py` sha256
`784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5`. This equals
`git show a21845f…:tools/write-path-census-v4.py | sha256sum`. The counter sha256
`3c3727ece033263f9e68ca2601012dc0170c6387cee44f3e7c09ee5744890ff2` equals the contract
`claims.C2.counter_sha256` at freeze `322b5cd…`. The self-pin passed: no `SETUP` line.

Each mutant was a copy in `/tmp/tameshi-r42w2-MutProbeDepth-d<N>/v4.py`, with only line 71
rewritten (`sed -i "71s/^MAX_DEPTH = 8$/MAX_DEPTH = N/"`). Each copy was confirmed with exactly
one `MAX_DEPTH = N` line. Command (pre-run at the integration tip, CONTROL label):

```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-42/census/measure.py --lane /home/vgpnk/Projects/shokunin/tameshi-shokunin --rev a21845f523b75adbd3e3f7a62af91294db224ad9 --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f --probe-mutant /tmp/tameshi-r42w2-MutProbeDepth-d<N>/v4.py
```

| MAX_DEPTH | copy sha256 (16) | output `PROBE …` line | verdict |
|---|---|---|---|
| 8 (pristine baseline) | `784de4c0feef3364` | `PROBE outcome=survived detail=` | baseline clean |
| 7 | `096bc8c661b4d02f` | `PROBE outcome=survived detail=` | **survived** |
| 6 | `2f06525957260f14` | `PROBE outcome=killed detail=tools/registry-replay.py:123 explicit_out=0 want 1` | killed |
| 5 | `e2e7c8abd09eccd9` | `PROBE outcome=killed detail=F01_attr_scratch scratch=0 want 1` | killed |
| 4 | `003675ff96b330ae` | `PROBE outcome=killed detail=F01_attr_scratch scratch=0 want 1` | killed |
| 3, 2, 1 (extra) | `525bb4b9…`, `3b5825b5…`, `aa4fce7a…` | `PROBE outcome=killed detail=F01_attr_scratch scratch=0 want 1` | killed |
| 0 (extra) | `db23826e4b41f2c2` | `PROBE outcome=killed detail=F01_attr_scratch expected-value sites=0, want 1` | killed |

Every run ended `C2_R42_CONTROL: probe_outcome=<same> rev=a21845f… freeze=322b5cd…` with exit 0.

## All-fail breakdown (same battery, every case)

`oracle()` reports only `fails[0]` (`measure.py:311-317`). To get every failing case, a scratch
driver imported the pinned counter's own `stage()` and `battery()` (`measure.py:320`,
`:283`) at rev `a21845f…`. It ran:
`python3 /tmp/tameshi-r42w2-MutProbeDepth-driver/allfails.py 0 1 2 3 4 5 6 7 8`

| MAX_DEPTH | fixtures | cc:1682 | cc:1685 | rr:123 | other fails |
|---|---|---|---|---|---|
| 0 | 2/10 | expected=0 | expected=0 | expected=0 | F01–F08 expected-value sites=0 |
| 1–5 | 8/10 | scratch=0 | scratch=0 | explicit_out=0 | F01 scratch=0, F04 explicit_out=0 |
| 6 | 10/10 | ok | ok | **explicit_out=0 want 1** | — |
| 7 | 10/10 | ok | ok | ok | — |
| 8 | 10/10 | ok | ok | ok | — |

## Gate isolation (which `depth > MAX_DEPTH` check binds)

These variants rewrote a single gate and left `MAX_DEPTH = 8`. Same driver.

| variant | edit | cc:1682/1685 | rr:123 | fixtures |
|---|---|---|---|---|
| r5 | `:172` `_resolve` → `depth > 5` | scratch=0 (fail) | ok | 9/10 (F01 fails) |
| r6 | `:172` `_resolve` → `depth > 6` | ok | ok | 10/10 |
| p6 | `:262` `_parse_args_ns` → `depth > 6` | ok | explicit_out=0 (fail) | 10/10 |
| f6 | `:280` `_out_flag` → `depth > 6` | ok | ok | 10/10 |
| o6 | `:262` + `:280` → `depth > 6` | ok | explicit_out=0 (fail) | 10/10 |

The context-capture chain needs `_resolve` depth ≥ 6, which confirms the entry. The
registry-replay chain needs `_parse_args_ns` depth ≥ 7. Because `MAX_DEPTH` is one constant
shared by all three gates, the tool needs at least 7 overall.

## Restoration / isolation evidence

- The live lane file was never written. Its sha256 after all probes is still
  `784de4c0feef3364c4444632788af7ebb57d53032b79f60cc4330c094d122fe5`.
  `git -C <lane> status --porcelain -- tools/ .ufo/evidence/round-42/census/` printed nothing.
- The counter's sha256 after the probes is still `3c3727ec…0ff2`.
- The scratch copies and the driver were deleted with `rm -rf /tmp/tameshi-r42w2-MutProbeDepth-*`.
  A follow-up `ls` reports `No such file or directory`. No `/tmp/tameshi-r42-c2-*` work dirs
  were left over.
- Nothing ran in default (deciding) mode. Every counter run used `--probe-mutant` at the
  allowed pre-run rev `a21845f…`.
- Tools installed: none.
- Tool anomaly: the Read tool refused 7–26 KB files as "exceeds 100000 characters". I used
  Grep with context instead.

Verdict: SURVIVES — "the context-capture chain needs six" holds (passes at 6, fails at 5), but the battery floor is 7, set by `registry-replay.py:123` through `_parse_args_ns`; the record omits this, and the 8→7 mutant survives (coverage finding).
