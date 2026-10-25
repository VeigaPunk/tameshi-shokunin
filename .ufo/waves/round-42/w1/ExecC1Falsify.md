# ExecC1Falsify — C1 false-pass hunt (round 42, wave 1)

Seat: `L1Tameshi42.ExecC1Falsify` (leaf). No subagents, no lane writes except this report.

Counter used for every run (exact command):
```
python3 /home/vgpnk/Projects/shokunin/tameshi-shokunin/.ufo/evidence/round-42/calibration/measure.py --lane /tmp/tameshi-r42-ExecC1Falsify/<name> --rev HEAD --freeze 322b5cd32b4319a05340d249ae752d12a9e6b19f
```
All trees are scratch clones (`git clone --shared` of the lane, checked out at the freeze commit `322b5cd32b4319a05340d249ae752d12a9e6b19f`, then one commit each). Counter sha/pin: `self_pin=1` verified in every run. Controls first, then findings.

## Controls (harness sanity)

| name | tree | counter line | result |
|---|---|---|---|
| `00_base_untouched` | freeze untouched | `m10=1 … records=3 … C1_R42_PASS=false` | matches contract `before_expected` (m10=1, records=3) |
| `01_healthy_control` | healthy tree only (6 records + covering superseding receipt) | `m6=0 m7=0 m8=0 m10=0 m11=0 total=0 records=6 sources_rows=109 … C1_R42_PASS=true`, exit 0 | harness works |
| `02_caught_m7` | healthy + bare `S155` in round-42 lesson | `MISMATCH m7 S155 cited but absent from the registry` → `m7=1 … PASS=false` | caught |
| `03_caught_m8` | healthy + single-line `` `tools/missing2.py` `` in round-42 lesson | `MISMATCH m8 tools/missing2.py cited in corpus/lessons/round-42.md does not resolve` → `m8=1 … PASS=false` | caught |

Note: the residual round-41 receipt (`.ufo/waves/round-41/residual/receipt.json`) asserts `present=false` for `ResidualReceipts.md` and asserts 7 more residual paths `present=true`. A superseding receipt that re-asserts only the one mismatch path does **not** clear it — coverage requires the superseder's asserted paths to be a superset of every asserted path of the superseded receipt (`theirs <= mine` over all 8). The healthy-control superseder re-asserts all 8; with that, m10=0.

## Findings — C1 prints PASS=true while a real disagreement remains (all 11)

All runs below: `self_pin=1 … total=0 records=6 sources_rows=109 … C1_R42_PASS=true`, exit 0. The disagreement is real in every tree (the injected artifact is committed at HEAD and contradicts the repo state).

| # | name | injected disagreement (committed at HEAD) | why the counter misses it | classification |
|---|---|---|---|---|
| 1 | `f1_m10_file_key` | wave receipt `.ufo/waves/round-42/f1/receipt.json` = `{"seats":{"A":{"file":"corpus/lessons/round-42.md","present":false}}}` — asserts an existing file is absent | `walk_present` (measure.py:177) reads only `report` (str) or `path`; key `file` is ignored → receipt not even registered | **real gap**, inside declared class m10 |
| 2 | `f2_m10_present_str` | wave receipt with `"present":"false"` (string) for existing lesson | `walk_present` (measure.py:178) requires `isinstance(obj.get('present'), bool)` → skipped | **real gap**, inside declared class m10 |
| 3 | `f3_m10_report_list` | wave receipt with `"report":["corpus/lessons/round-42.md"]` (list) + `present:false` | `report` not str → falls back to absent `path` → skipped | **real gap**, inside declared class m10 |
| 4 | `f4_m10_outside_waves` | tracked JSON receipt at `.ufo/evidence/round-42/falsify/receipt.json` (standard keys, asserts lesson absent) | `receipt_audit` scans only `repo.tracked('.ufo/waves')` (measure.py:190) | real disagreement but **out of declared class** (m10 is explicitly scoped to "tracked JSON under .ufo/waves/") |
| 5 | `f5_m10_nonjson` | wave receipt named `receipt.txt` (valid JSON body, asserts lesson absent) | filter `path.endswith('.json')` (measure.py:191) | real disagreement but **out of declared class** (declared class says JSON under waves) |
| 6 | `f6_m10_malformed` | wave `receipt.json` with truncated JSON (asserts lesson absent, unparseable) | `except Exception: continue` (measure.py:195-196) silently skips | **real gap** (silent skip); the assertion is unreadable by design |
| 7 | `f7_m8_crossline_path` | round-42 lesson cites dead path inside backticks split across lines: ``repo `corpus/missing-design`` ↵ ``doc.md` never resolves`` — `path_tokens()` extracts **zero** tokens (verified) | `BACKTICK_RE = re.compile(r'`([^`\n]+)`')` (measure.py:79) cannot span a newline | **real gap**; exactly the declared extraction rule ("backtick spans never cross a newline") |
| 8 | `f8_m7_r41_sid` | round-**41** record (corpus/lessons/round-41.md) cites `S777`, absent from the registry | m7 loop scans only `rec42` (measure.py:236); round-41 records are never checked for S-cites | **real gap**; the claim says "round-41 and round-42 records cite no unmined S-id" but the check is round-42-only |
| 9 | `f9_m7_spaced_sid` | round-42 lesson cites `S 155` (space between S and digits) | `S_CITE_RE = re.compile(r'(?<!staged:)\bS(\d{3,})\b')` (measure.py:78) requires digits adjacent to S | **real gap** (formatting variant of a bare S-cite) |
| 10 | `f10_m11_upper_hex` | round-42 lesson cites uppercase 40-hex `ABCDEF0123456789ABCDEF0123456789ABCDEF01` (not a lane or fleet commit) | `HEX40_RE` (measure.py:80) is lowercase-only (`[0-9a-f]{40}`); no match, no partial match | **real gap**; the claim says records cite no unreachable revision |
| 11 | `f11_m6_indented_row` | `corpus/SOURCES.md` gains a genuine row `| S199 | …` indented 4 spaces (line 442 at HEAD) | `S_ROW_RE = re.compile(r'^ {0,3}\|[ \t]*S(\d{3,})')` (measure.py:77) allows at most 3 leading spaces → row uncounted, `sources_rows=109` still equals standing "109 rows" | **real gap**; standing count blind to indented S-rows |

## The proposed escape variants that are CAUGHT (not gaps)

- **S-id written `S0155`** (leading zero) in a round-42 record: `MISMATCH m7 S0155 cited but absent from the registry` → `m7=1 … PASS=false` (`f12_m7_zero_padded`). Digit padding does not bypass m7; only the round-41/`S 155` forms above do.
- **Receipt keyed `path` vs `report`** with both keys present: `report` wins by precedence (measure.py:177) → `MISMATCH m10 … asserts present=false for corpus/lessons/round-42.md` → `m10=1 … PASS=false` (`f13_m10_dualkey`). Dual-key receipts are caught; only nonstandard-only keying (`file`) bypasses.

## What I could not check

- Everything above was checked by running the frozen counter against each scratch clone; nothing blocked. I did not run the counter against the lane's live tip (the deciding run is the L1's).
- No tool installs/updates were performed (channel directive N/A); only existing `git` and `python3` used.
- Scratch clones under `/tmp/tameshi-r42-ExecC1Falsify/` deleted on completion; the live lane checkout was never touched.
